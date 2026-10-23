"""Licence scanning and policy engine (Flicky's tooling).

Scans a project tree for licence declarations and evaluates them against
the team's house policy (``policy.yaml``, next to this file). Four
outcomes, deliberately not two:

- ``PASS``              approved and compatible            (exit 0)
- ``POLICY_EXCEPTION``  lawful, on the avoid list          (exit 6)
- ``BLOCK``             incompatible, or a blocker licence  (exit 7)
- ``HARD_STOP``         no licence at all, or a hard-stop   (exit 8)

"Avoid" is not "refuse". Inherited copyleft is frequently the only lawful
option: a derivative of a GPL upstream published under that GPL is correct,
and relicensing it would be the violation. So inherited copyleft is an
exception to be recorded, not a block.

The scanner is evidence, not a lawyer: it reads what is declared (LICENSE
files, SPDX headers, package metadata, attribution files) and applies the
policy file. Legal conclusions belong in the planning doc, with the
upstream ref cited.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

import yaml

#: Outcome severities, worst last.
OUTCOME_PASS = "PASS"
OUTCOME_EXCEPTION = "POLICY_EXCEPTION"
OUTCOME_BLOCK = "BLOCK"
OUTCOME_HARD_STOP = "HARD_STOP"

EXIT_CODES = {
    OUTCOME_PASS: 0,
    OUTCOME_EXCEPTION: 6,
    OUTCOME_BLOCK: 7,
    OUTCOME_HARD_STOP: 8,
}

SPDX_HEADER_RE = re.compile(
    r"SPDX-License-Identifier:\s*([A-Za-z0-9.\-+ ]+(?:\s+(?:OR|AND|WITH)\s+[A-Za-z0-9.\-+ ]*)*)",
    re.IGNORECASE,
)

LICENSE_FILE_NAMES = ("LICENSE", "LICENSE.md", "LICENSE.txt", "LICENCE", "LICENCE.md",
                      "LICENCE.txt", "COPYING", "COPYING.md")

ATTRIBUTION_NAMES = ("NOTICE", "NOTICE.txt", "NOTICE.md", "AUTHORS", "AUTHORS.txt")

SKIP_DIRS = {
    ".git", "node_modules", "__pycache__", ".pytest_cache", "bin", "externals",
    "images", "scratch", ".runs", ".agentsmd", ".venv", "venv",
}

MAX_HEADER_BYTES = 64 * 1024

#: Recognised declarations, keyed by SPDX id. Values are (kind, severity).
#: kind: permissive | copyleft | source_available | not_osi
#: severity is only used for avoid-list entries from policy.yaml.
KNOWN = {
    "MIT": "permissive",
    "Apache-2.0": "permissive",
    "BSD-2-Clause": "permissive",
    "BSD-3-Clause": "permissive",
    "ISC": "permissive",
    "Zlib": "permissive",
    "0BSD": "permissive",
    "Unlicense": "public_domain",
    "GPL-2.0-only": "copyleft",
    "GPL-2.0-or-later": "copyleft",
    "GPL-3.0-only": "copyleft",
    "GPL-3.0-or-later": "copyleft",
    "LGPL-2.1-only": "copyleft",
    "LGPL-2.1-or-later": "copyleft",
    "LGPL-3.0-only": "copyleft",
    "LGPL-3.0-or-later": "copyleft",
    "AGPL-3.0-only": "copyleft",
    "BUSL-1.1": "source_available",
    "BUSL-1.0": "source_available",
    "SSPL-1.0": "source_available",
    "CC-BY-4.0": "non_code",
    "CC0-1.0": "public_domain",
}

_COPYLEFT_VARIANTS = {
    "GPL-2.0": "GPL-2.0-only",
    "GPLv2": "GPL-2.0-only",
    "GPL-3.0": "GPL-3.0-only",
    "GPLv3": "GPL-3.0-only",
    "LGPL-2.1": "LGPL-2.1-only",
    "LGPL-3.0": "LGPL-3.0-only",
    "AGPL": "AGPL-3.0-only",
}


def normalize_spdx(raw: str) -> str | None:
    """Map a declared string onto a known SPDX id, or None."""
    raw = (raw or "").strip()
    if not raw:
        return None
    if raw in KNOWN:
        return raw
    for variant, canonical in _COPYLEFT_VARIANTS.items():
        if raw.upper() == variant.upper():
            return canonical
    # "GPL-2.0" style without -only/-or-later suffix
    m = re.match(r"^(GPL|LGPL|AGPL)-(\d+(?:\.\d+)?)(?:-(only|or-later))?", raw)
    if m:
        base = "%s-%s" % (m.group(1), m.group(2))
        suffix = m.group(3)
        guess = "%s-%s" % (base, suffix) if suffix else base + "-only"
        return guess if guess in KNOWN else (base + "-only" if base in KNOWN or base + "-only" in KNOWN else None)
    return raw if raw in KNOWN else None


def detect_license_text(text: str) -> str | None:
    """Read a LICENSE file body and classify it."""
    head = text[:8192]
    up = head.upper()
    if "BUSINESS SOURCE LICENSE" in up or "BUSL" in up:
        return "BUSL-1.1"
    if "SERVER SIDE PUBLIC LICENSE" in up:
        return "SSPL-1.0"
    if "GNU AFFERO GENERAL PUBLIC LICENSE" in up:
        return "AGPL-3.0-only"
    if "GNU LESSER GENERAL PUBLIC LICENSE" in up:
        return "LGPL-3.0-only" if "VERSION 3" in up else "LGPL-2.1-only"
    if "GNU GENERAL PUBLIC LICENSE" in up:
        if re.search(r"VERSION 3", up):
            return "GPL-3.0-only"
        return "GPL-2.0-only"
    if "APACHE LICENSE" in up or "APACHE LICENSE, VERSION 2.0" in up or "APACHE-2.0" in up:
        return "Apache-2.0"
    if "MIT LICENSE" in up:
        return "MIT"
    if re.search(r"REDISTRIBUTION AND USE IN SOURCE AND BINARY FORMS", up):
        return "BSD-3-Clause"
    if "CREATIVE COMMONS" in up and "CC BY" in up.replace(" ", ""):
        return "CC-BY-4.0"
    return None


def _iter_files(root: Path):
    for p in sorted(root.rglob("*")):
        if p.is_file() and not any(part in SKIP_DIRS for part in p.parts):
            yield p


@dataclass
class Finding:
    path: str
    spdx: str
    kind: str          # repo_license | header | package_meta | attribution
    note: str = ""


@dataclass
class ScanResult:
    root: str
    outcome: str = OUTCOME_PASS
    findings: list = field(default_factory=list)
    reasons: list = field(default_factory=list)

    def to_json(self) -> dict:
        return {
            "root": self.root,
            "outcome": self.outcome,
            "exit": EXIT_CODES[self.outcome],
            "findings": [
                {"path": f.path, "spdx": f.spdx, "kind": f.kind, "note": f.note}
                for f in self.findings
            ],
            "reasons": self.reasons,
        }


def load_policy(policy_path: str | Path | None = None) -> dict:
    p = Path(policy_path) if policy_path else Path(__file__).parent / "policy.yaml"
    with open(p, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def scan(root: str | Path) -> ScanResult:
    """Collect every licence declaration in the tree."""
    root = Path(root).resolve()
    if not root.is_dir():
        raise FileNotFoundError(root)
    result = ScanResult(root=str(root))
    seen_paths: set[str] = set()

    # 1. Licence files at the root (the project's own licence).
    for name in LICENSE_FILE_NAMES:
        p = root / name
        if p.is_file():
            text = p.read_text(errors="replace")
            spdx = detect_license_text(text)
            if spdx is None:
                result.findings.append(Finding(name, "UNRECOGNIZED", "repo_license",
                                               "licence file present but unclassified"))
            else:
                result.findings.append(Finding(name, spdx, "repo_license"))
            seen_paths.add(str(p))

    # 2. Attribution files (Apache-2.0 obligations, copyright notices).
    for name in ATTRIBUTION_NAMES:
        p = root / name
        if p.is_file():
            result.findings.append(Finding(name, "ATTRIBUTION", "attribution"))

    # 3. SPDX headers and package metadata across the tree.
    for p in _iter_files(root):
        rel = str(p.relative_to(root))
        if str(p) in seen_paths:
            continue
        if p.name in LICENSE_FILE_NAMES and p.parent == root:
            continue
        if p.suffix in (".py", ".sh", ".c", ".h", ".rs", ".go", ".js", ".ts",
                        ".java", ".cs", ".rb", ".raku", ".pl", ".toml",
                        ".yml", ".yaml", ".json", ".md"):
            try:
                head = p.open("rb").read(MAX_HEADER_BYTES)
            except OSError:
                continue
            head = head.decode("utf-8", errors="replace")
            m = SPDX_HEADER_RE.search(head)
            if m:
                spdx = normalize_spdx(m.group(1)) or m.group(1)
                result.findings.append(Finding(rel, spdx, "header"))
        if p.name == "package.json":
            try:
                data = json.loads(p.read_text(errors="replace"))
            except (OSError, json.JSONDecodeError):
                continue
            lic = data.get("license")
            if isinstance(lic, dict):
                lic = lic.get("type")
            if isinstance(lic, str) and lic and lic.lower() != "unlicensed":
                spdx = normalize_spdx(lic) or lic
                result.findings.append(Finding(rel, spdx, "package_meta"))
        if p.name == "pyproject.toml":
            spdx = _pyproject_license(p)
            if spdx:
                result.findings.append(Finding(rel, spdx, "package_meta"))
        if p.name == "setup.cfg":
            m = re.search(r"^\s*license\s*=\s*(.+)$",
                          p.read_text(errors="replace"), re.M | re.I)
            if m:
                spdx = normalize_spdx(m.group(1)) or m.group(1).strip()
                result.findings.append(Finding(rel, spdx, "package_meta"))
        if p.name == "Cargo.toml":
            m = re.search(r'^\s*license\s*=\s*"(.+)"',
                          p.read_text(errors="replace"), re.M)
            if m:
                spdx = normalize_spdx(m.group(1)) or m.group(1)
                result.findings.append(Finding(rel, spdx, "package_meta"))
    return result


def _pyproject_license(p: Path) -> str | None:
    try:
        import tomllib
    except ImportError:
        return None
    try:
        data = tomllib.loads(p.read_text(errors="replace"))
    except Exception:
        return None
    project = data.get("project", {})
    lic = project.get("license")
    if isinstance(lic, dict):
        lic = lic.get("text") or lic.get("expression")
    if isinstance(lic, str) and lic:
        spdx = normalize_spdx(lic) or lic
        return spdx
    return None


def evaluate(root: str | Path, policy: dict | None = None) -> ScanResult:
    """Scan, then apply the house policy."""
    result = scan(root)
    policy = policy or load_policy()
    approved = [e["spdx"] for e in policy.get("approved", {}).get("code", [])]
    avoid = policy.get("avoid", [])
    avoid_ids = {e["spdx"]: e.get("severity", "policy_exception") for e in avoid}
    hard_ids = {e["spdx"] for e in policy.get("hard_stop_licences", [])}

    repo_spdxs = [f.spdx for f in result.findings if f.kind == "repo_license"]

    # Hard stops first: no licence at all, or a hard-stop licence anywhere.
    if not repo_spdxs:
        result.outcome = OUTCOME_HARD_STOP
        result.reasons.append(
            "no licence declared for the project root (no LICENSE file). "
            "Code with no licence is proprietary by default; that is the "
            "most restrictive finding, not the least.")
    for f in result.findings:
        if f.spdx in hard_ids:
            result.outcome = OUTCOME_HARD_STOP
            result.reasons.append(
                "%s (%s) is a hard-stop licence per policy" % (f.spdx, f.path))

    if result.outcome == OUTCOME_HARD_STOP:
        return result

    # Blockers: incompatible combinations and blocker-severity avoid entries.
    for f in result.findings:
        sev = avoid_ids.get(f.spdx)
        if sev == "blocker":
            result.outcome = OUTCOME_BLOCK
            result.reasons.append(
                "%s (%s) is on the avoid list with blocker severity" % (f.spdx, f.path))
    if result.outcome == OUTCOME_BLOCK:
        return result

    # Copyleft mix: permissive root plus a copyleft dependency is a licence
    # CHANGE on the combined work, so it is an exception to record, not a
    # pass and not a block.
    root_copyleft = [
        f.spdx for f in result.findings
        if f.kind == "repo_license" and KNOWN.get(f.spdx) == "copyleft"
    ]
    dep_copyleft = [
        f for f in result.findings
        if f.kind in ("header", "package_meta") and KNOWN.get(f.spdx) == "copyleft"
    ]
    if root_copyleft and any(
        KNOWN.get(f.spdx) == "permissive"
        for f in result.findings
        if f.kind in ("header", "package_meta")
    ):
        result.outcome = OUTCOME_EXCEPTION
        result.reasons.append(
            "project root is copyleft (%s) while permissive components are "
            "declared: the combined work's licence is in question; record "
            "the position in the planning doc." % ", ".join(root_copyleft))

    # Avoid list (policy exception severity): record, never silent.
    for f in result.findings:
        sev = avoid_ids.get(f.spdx)
        if sev == "policy_exception":
            result.outcome = OUTCOME_EXCEPTION
            result.reasons.append(
                "%s (%s) is on the avoid list: lawful, but needs a recorded "
                "exception, not a silent pass." % (f.spdx, f.path))

    if result.outcome == OUTCOME_PASS:
        if not root_copyleft:
            for spdx in repo_spdxs:
                if spdx not in approved:
                    result.outcome = OUTCOME_EXCEPTION
                    result.reasons.append(
                        "project licence %s is not on the approved list" % spdx)
                    break
    return result


def main(argv: list[str] | None = None) -> int:
    import argparse

    argv = sys.argv[1:] if argv is None else argv
    ap = argparse.ArgumentParser(prog="licence-check",
                                 description="Team Chaotix licence gate")
    ap.add_argument("path", nargs="?", default=".", help="project root to scan")
    ap.add_argument("--json", action="store_true", help="machine-readable report")
    ap.add_argument("--policy", default=None, help="policy.yaml override")
    args = ap.parse_args(argv)

    result = evaluate(args.path, load_policy(args.policy) if args.policy else None)
    if args.json:
        print(json.dumps(result.to_json(), indent=2, sort_keys=True))
    else:
        print("licence-check: %s (%s)" % (args.path, result.outcome))
        for f in result.findings:
            print("  %-40s %-18s %s" % (f.path, f.spdx, f.kind))
        for r in result.reasons:
            print("  reason: %s" % r)
    return EXIT_CODES[result.outcome]


if __name__ == "__main__":
    raise SystemExit(main())
