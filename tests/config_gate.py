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
    "amy", "big", "charmy", "espio", "knuckles",
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
            # The delegator allows every worker, and nothing else, via task:
            # allowed must equal set(WORKERS) exactly, so a dead allow for a
            # name with no agent file fails instead of passing a one-way
            # missing-set check.
            allowed = set(re.findall(r'^\s+"([a-z]+)":\s*allow', fm, re.M))
            if allowed != set(WORKERS):
                fail("robotnik: task allows must be exactly the worker set "
                     "(missing=%s, extra=%s)"
                     % (sorted(set(WORKERS) - allowed),
                        sorted(allowed - set(WORKERS))))
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

    # The review chain in AGENTS.md section 3 must name the sole licence
    # agent last. The check is pinned to the section-3 line itself (the
    # line that carries "fixed sequence"): the section-18 cycle
    # parenthetical carries the same chain, and a whole-file search would
    # let a deleted section-3 sentence, or a 5-agent regressed chain with a
    # new fifth-agent name, pass on that match. The cycle chain also runs
    # Charmy and then continues to `Tails` fixes, so "ends at Charmy" is
    # pinned on the chain string itself: the Shadow → Omega → Big → Charmy
    # sequence with no arrow after Charmy. The absence check below still
    # runs. The retired name is built by concatenation so this file never
    # carries the literal (same idiom as test_cycle.py's max-Turns check).
    agents_md = (ROOT / "AGENTS.md").read_text()
    section3 = [ln for ln in agents_md.splitlines() if "fixed sequence" in ln]
    chain = any(re.search(r"`Shadow`\s*→\s*`Omega`\s*→\s*`Big`\s*→\s*`Charmy`(?!\s*→)",
                          ln)
                for ln in section3)
    if not chain:
        fail("AGENTS.md: the section-3 review chain must be Shadow → Omega → Big → Charmy, "
             "ending at Charmy")
    if "## License (Charmy)" not in agents_md:
        fail("AGENTS.md: the doc contract must list ## License (Charmy)")
    if re.search(r"fl" "icky", agents_md, re.I):
        fail("AGENTS.md: must not reference the retired licence agent")
    print("config-gate: AGENTS.md chain and doc contract OK")

    # The planning template must carry the consolidated section in order.
    tpl = (ROOT / "planning" / "templates" / "planning-doc.md").read_text()
    if "## License (Charmy)" not in tpl:
        fail("planning template: ## License (Charmy) section missing")
    if re.search(r"fl" "icky", tpl, re.I):
        fail("planning template: must not reference the retired licence agent")
    print("config-gate: planning template OK")

    # The A2A server's roster must not hardcode the team: it reads the
    # agent files, so the gate checks that the old static list is gone.
    a2a = (ROOT / "team" / "a2a" / "server.py").read_text()
    if "ROSTER = [" in a2a:
        fail("a2a server: the static ROSTER list must stay retired (roster comes from .opencode/agents)")
    print("config-gate: A2A roster is file-driven OK")


if __name__ == "__main__":
    main()
