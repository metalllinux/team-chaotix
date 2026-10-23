"""Agent configuration gate for Team Chaotix.

Checks that the agent files and AGENTS.md agree with the team's standing
rules. This is the machine-readable half of "least privilege plus one
unrestricted delegator": a grep cannot see ordering or omissions, so the
gate parses the frontmatter and asserts the roster, the thinking levels,
the permissions, and the no-turn-caps requirement.

Run by tests/selftest.sh and by CI. Exits non-zero on the first failure.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AGENTS = ROOT / ".opencode" / "agents"
WORKERS = [
    "amy", "big", "charmy", "espio", "flicky", "knuckles",
    "omega", "shadow", "sonic", "tails", "vector",
]
ROBOTNIK = "robotnik"


def fail(msg: str) -> None:
    print("config-gate FAIL:", msg, file=sys.stderr)
    sys.exit(1)


def frontmatter(path: Path) -> str:
    lines = path.read_text().splitlines()
    if not lines or lines[0].strip() != "---":
        fail(f"{path.name}: no frontmatter")
    out = []
    for line in lines[1:]:
        if line.strip() == "---":
            break
        out.append(line)
    else:
        fail(f"{path.name}: unterminated frontmatter")
    return "\n".join(out) + "\n"


def model_ref(fm: str) -> str:
    m = re.search(r'^model:\s*"?([^"\n]+)"?', fm, re.M)
    return m.group(1).strip().strip('"') if m else ""


def main() -> None:
    files = sorted(AGENTS.glob("*.md"))
    names = [p.stem for p in files]
    expected = sorted(WORKERS + [ROBOTNIK])
    if names != expected:
        fail("roster mismatch: got %s, expected %s" % (sorted(names), expected))
    print("config-gate: roster OK (%d agents)" % len(names))

    for p in files:
        fm = frontmatter(p)
        if re.search(r"[m]axTurns", fm) or re.search(r"^\s*steps:", fm, re.M):
            fail(f"{p.name}: turn caps are not allowed on this team")
        if p.stem == ROBOTNIK:
            if not re.search(r"^mode:\s*primary", fm, re.M):
                fail("robotnik: mode must be primary")
            # The delegator allows every worker, and nothing else, via task.
            allowed = set(re.findall(r'^\s+"([a-z]+)":\s*allow', fm, re.M))
            missing = set(WORKERS) - allowed
            if missing:
                fail("robotnik: task allows missing for %s" % sorted(missing))
            if "question: deny" not in fm:
                fail("robotnik: question must stay denied")
            # The delegator is the only agent with full thinking.
            model = model_ref(fm)
            if "#low" in model:
                fail("robotnik: the delegator keeps full thinking")
        else:
            # Every worker: low thinking, no delegation, no questions.
            model = model_ref(fm)
            if "#low" not in model:
                fail(f"{p.stem}: workers must run the #low variant")
            if not re.search(r"^\s*task:\s*deny", fm, re.M):
                fail(f"{p.stem}: workers must have task: deny")
            if "question: deny" not in fm:
                fail(f"{p.stem}: question must stay denied")
    print("config-gate: thinking levels and permissions OK")

    # The review chain in AGENTS.md must name the licence agent last.
    agents_md = (ROOT / "AGENTS.md").read_text()
    chain = re.search(r"`Shadow`\s*→\s*`Omega`\s*→\s*`Big`\s*→\s*`Charmy`\s*→\s*`Flicky`",
                      agents_md)
    if not chain:
        fail("AGENTS.md: review chain must be Shadow → Omega → Big → Charmy → Flicky")
    if "## License Audit (Flicky)" not in agents_md:
        fail("AGENTS.md: the doc contract must list ## License Audit (Flicky)")
    print("config-gate: AGENTS.md chain and doc contract OK")

    # The planning template must carry the section in order.
    tpl = (ROOT / "planning" / "templates" / "planning-doc.md").read_text()
    if "## License Audit (Flicky)" not in tpl:
        fail("planning template: ## License Audit (Flicky) section missing")
    print("config-gate: planning template OK")

    # The A2A server's roster must not hardcode the team: it reads the
    # agent files, so the gate checks that the old static list is gone.
    a2a = (ROOT / "team" / "a2a" / "server.py").read_text()
    if "ROSTER = [" in a2a:
        fail("a2a server: the static ROSTER list must stay retired (roster comes from .opencode/agents)")
    print("config-gate: A2A roster is file-driven OK")


if __name__ == "__main__":
    main()
