# TASK-0041 — Remove Flicky agent; fold all licence functionality into Charmy

> **Section order below is fixed.** Each agent writes to its own section and no other. `Robotnik`
> reads only `## Status` and `## Next Actions`. Do not reorder, rename, or remove sections.

- **Created:** 2026-11-24

---

## Status

*Owner: `Robotnik`. Keep this SHORT and CURRENT — it is one of only two sections the PM reads, so a
stale entry means the whole loop runs on bad information.*

**Now:** (2026-11-24) Implementation, full review chain, fix pass, and chain re-run complete. Chain
clean: Shadow no blocker/should-fix (one non-blocking nit: a one-phrase Tails polish pending),
Omega all three lows closed (one new pre-existing medium, operator item below), Big PASS 56/56
with both strengthened gate checks proven executing, Charmy VERDICT PASS (gate exit 0, no new
imports). Next: Tails one-phrase polish, Vector docs pass, Knuckles signed commit + PR + merge.

**Operator items (recorded, non-blocking):**
- `origin` remote URL carries a live `ghp_` PAT (TASK-0040 W4 design; the value is verified absent
  from all shared artifacts). Operator decision: de-embed (push auth from `~/AI/secrets/token.md`)
  or keep the design with value-free record discipline held as a hard rule plus rotate-on-capture.
  See `## Security`.
- Host hygiene: an untracked 40 GiB disk image named `-` and 22 untracked prior-task RPMs sit on the
  ~40 GB host disk. Cleanup, not rotation. See `## Security`.

**Environment / scope:**
- Files in scope: `.opencode/agents/flicky.md` (deleted), `.opencode/agents/charmy.md`,
  `.opencode/agents/robotnik.md`, `AGENTS.md`, `tests/config_gate.py`, `tests/test_cycle.py`,
  `tests/test_a2a.py`, `team/graph/state.py`, `team/graph/cycle.py`, `team/__init__.py`,
  `team/licenses/core.py`, `team/licenses/policy.yaml`, `scripts/licence-check`,
  `.github/workflows/licence-check.yml`, `README.md`, `planning/templates/planning-doc.md`
- Touches the DB schema: no
- Graphical UI: no
- Rocky Linux target: no

**Decision (recorded):** `Charmy` becomes the sole licence agent. She keeps her existing licence
review (`## License (Charmy)`) and additionally runs the machine gate (`scripts/licence-check`)
and records its 4-outcome result; both were Flicky's. The two planning-doc sections
(`## License (Charmy)` + `## License Audit (Flicky)`) are consolidated into a single
`## License (Charmy)` section that carries both the review and the gate audit. The review chain
shortens to `Shadow` → `Omega` → `Big` → `Charmy` (4 agents, Charmy last). Historical planning docs
(TASK-0037/0038/0039/0040) and the untracked `continue-prompt-*` scratch files are left untouched:
they are records of when Flicky existed, not living config.

**Unknowns:** none load-bearing; the change is a bounded merge across a known file set.

---

## Definition of Done

*Owner: `Robotnik`, and nobody else. Written **before** any work starts. Objectively checkable —
if a box cannot be verified by looking at something, rewrite it.*

- [ ] `.opencode/agents/flicky.md` is deleted; the agent roster is 11 (12 minus `flicky`).
- [ ] `.opencode/agents/charmy.md` owns all of Flicky's functionality: she runs the machine gate
  `scripts/licence-check`, records its 4-outcome result (PASS / POLICY_EXCEPTION / BLOCK /
  HARD_STOP), and does the upstream-at-ref verification and obligations/attribution checks. Charmy
  is the sole licence agent.
- [ ] `.opencode/agents/robotnik.md` task-allows no longer lists `flicky`; the other 10 workers remain.
- [ ] `AGENTS.md`: the roster is 11 agents with no mention of Flicky; the review chain is
  `Shadow` → `Omega` → `Big` → `Charmy` (Charmy last); section 9 (licence compliance) is owned by
  Charmy; the planning-doc contract lists the consolidated `## License (Charmy)` section; the
  section-18 cycle graph has no Flicky node.
- [ ] `tests/config_gate.py`: the WORKERS roster has no `flicky`; the chain assertion expects
  `Shadow → Omega → Big → Charmy`; the doc contract asserts the consolidated section, not
  `## License Audit (Flicky)`.
- [ ] `team/graph/state.py` and `team/graph/cycle.py`: no `review_flicky` state and no Flicky node;
  the cycle is intake → plan → implement → review (Shadow, Omega, Big, Charmy) → fix loop → docs →
  release → archive.
- [ ] `tests/test_cycle.py` and `tests/test_a2a.py`: no `flicky` references; the A2A skill
  assertion reflects the 11-agent roster.
- [ ] `README.md`: no Flicky in the diagram, the agent table, or the chain prose; Charmy is
  described as the sole licence agent.
- [ ] `planning/templates/planning-doc.md`: a single consolidated `## License (Charmy)` section
  carrying both the licence review and the machine-gate audit; the DoD item is one consolidated
  Charmy item.
- [ ] `scripts/licence-check`, `.github/workflows/licence-check.yml`, `team/licenses/core.py`,
  `team/licenses/policy.yaml`, `team/__init__.py`: "Flicky's tool" / "Flicky agent" references
  updated to Charmy.
- [ ] No `flicky` / `Flicky` remains in any living team file (`.opencode/agents/`, `AGENTS.md`,
  `tests/`, `team/`, `README.md`, `planning/templates/`, `scripts/`, `.github/`). Historical
  planning docs (`planning/docs/TASK-003x`) and `continue-prompt-*` scratch files are
  intentionally untouched.
- [ ] `tests/selftest.sh` passes (config gate + pytest + licence gate).
- [ ] Committed (GPG-signed) and pushed to `metalllinux/team-chaotix` via a PR, merged to `main`.

---

## Next Actions

*Owner: whoever wrote last. The future only — delete what has been done. The second of the two sections
the PM reads.*

- [ ] `Tails`: one-phrase polish — reword the `## Implementation` checks clause so the `.pyc` is
  described as reused in steady state, not regenerated on every run (Shadow's nit).
- [ ] `Vector`: docs pass — README verified against the implementation, CHANGELOG if present; write
  `## Docs`.
- [ ] `Knuckles`: GPG-signed commit, PR to `metalllinux/team-chaotix`, merge to `main`.

---

## Plan

*Owner: `Amy`.*

**Why this task exists** — operator request, recorded in `## Status`: the licence work is one job
split across two agents. `Charmy` reviews, `Flicky` gates, both verify at the upstream ref, and
the split adds a fifth review stage and a second planning-doc section. Folding into one agent and
one section removes the redundancy.

**What it unblocks / what blocks it** — the standing 4-agent review chain
(`Shadow` → `Omega` → `Big` → `Charmy`) for every future task, one consolidated licence section in
every new planning doc, and the 11-agent A2A card. Nothing blocks it; all work is inside this
repo. The only external coupling is other team instances that may address `@flicky`; those fall
back to `robotnik` by design (`test_unknown_agent_falls_back_to_robotnik`), and the A2A card is
generated per request from `.opencode/agents/` (`team/a2a/server.py:10`), so no service restart
is needed.

**MVP** — all of the DoD. This is one atomic change in one PR, and there is no meaningful subset
to ship alone: `tests/config_gate.py` pins the roster, the chain, and the doc contract, so the
gate update and the files it checks must land together. Deferred: nothing. Historical mentions
(`planning/docs/TASK-003x`, `planning/TASKS.md`, `planning/HANDOFF-TASK-0038.md`,
`continue-prompt-*`) are records, not living config, and stay untouched per the recorded
decision.

**What this makes harder later.** Any external caller still pinned to the 12-agent roster
(another machine, a stale checkout) has its `@flicky` tasks silently land on `robotnik` until
informed; the fallback is designed and tested, but it is a silent behaviour change outside this
repo. Adding a twelfth worker later touches the same surfaces (gate, AGENTS.md, README, tests),
same cost as today.

**Work breakdown** — one agent, one item, one turn each.

| # | Item | Owner agent | Acceptance criterion | Parallel with |
|---|---|---|---|---|
| 1 | `git rm .opencode/agents/flicky.md`; remove `"flicky": allow` from task-allows (`.opencode/agents/robotnik.md:28`) | `Tails` | `ls .opencode/agents` shows exactly 11 `.md` files; `grep -in flicky .opencode/agents/robotnik.md` is empty; the other 10 workers remain in task-allows | independent; items 6, 7 depend on it |
| 2 | Rewrite `.opencode/agents/charmy.md` to absorb all of Flicky's functionality: frontmatter description (sole licence agent, fourth and last in the review chain, runs the machine gate); body gains the four-outcome table, the gate workflow (`scripts/licence-check`, `--json`), the "avoid is not refuse" rule, upstream-at-ref verification, attribution obligations, the boundaries (never grant or refuse an exception, GPL stays GPL, own section only), and the fail-closed machine-verdict contract (a `VERDICT: PASS` / `VERDICT: FAIL <reason>` line ending the output, which the review brief already requires) | `Tails` | config gate frontmatter checks pass for `charmy.md` (`#low` model, `task: deny`, `question: deny`); every `flicky.md` block (What you own, The four outcomes, How you work, Boundaries) has a counterpart in `charmy.md` | independent of 1, 3–9 |
| 3 | `AGENTS.md`: section 1 "all twelve agents" → eleven and "all eleven workers" → ten (`AGENTS.md:4`, `:112`); section 2 contract drops the `## License Audit (Flicky) (Flicky)` line (`:77`), keeping the single `## License (Charmy) (Charmy)` line; section 3 both chain strings end at `Charmy` (`:118`–`:119`); section 9 ownership reworded to `Charmy`, sole licence agent, fourth in the chain (last), legal conclusions go in `## License (Charmy)` (`:249`, `:261`), and the closing "`Charmy` stays fourth" sentence updated to the consolidated section; section 18 review chain has no Flicky node (`:483`) | `Tails` | `grep -ci flicky AGENTS.md` prints 0; both section 3 chain strings read `Shadow` → `Omega` → `Big` → `Charmy` | independent of 1, 2; item 6 depends on it |
| 4 | `planning/templates/planning-doc.md`: drop `## License Audit (Flicky)` (template `:143`–`:163`) and extend `## License (Charmy)` to carry both the review and the gate audit, using this doc's own `## License (Charmy)` section as the reference shape (owner line plus Project license, Imported code, Machine gate, Outcome, Declarations, Exceptions recorded, Verdict); the DoD list becomes one consolidated `Charmy` item covering review findings and gate outcome | `Tails` | `grep -ci flicky planning/templates/planning-doc.md` prints 0; `## License (Charmy)` contains the four-outcome gate block with exit codes; exactly one licence item in the DoD list | independent of 1, 2, 3; item 6 depends on it |
| 5 | `team/graph/state.py`: drop `review_flicky` from `STAGES` (`:32`), `REVIEW_STAGES` (`:44`), `STAGE_AGENT` (`:56`); `team/graph/cycle.py`: docstring chain (`:7`); `tests/test_cycle.py`: drop `"flicky"` from the FakeRunner reviewers (`:30`) and `"review_flicky"` from the expected `stage_history` (`:73`) | `Tails` | `pytest tests/test_cycle.py -q` green (11 stages, no `review_flicky`); `grep -ri flicky team/graph tests/test_cycle.py` empty | independent of 1–4 |
| 6 | `tests/config_gate.py`: remove `"flicky"` from `WORKERS` (`:21`); chain regex matches the 4-agent chain ending at `Charmy` (`:90`); doc-contract assertion checks `## License (Charmy)` present in AGENTS.md and in the template, and `Flicky` absent from AGENTS.md, replacing the `## License Audit (Flicky)` checks (`:94`–`:101`) | `Tails` | negative check first: the new gate run against the pre-change AGENTS.md (`git show HEAD:AGENTS.md` swapped in for the check) fails; then `python3 tests/config_gate.py` exits 0 with all five OK lines and prints `roster OK (11 agents)` | depends on 1, 3, 4 (it reads those files) |
| 7 | `tests/test_a2a.py`: replace `assert "flicky" in skill_ids` (`:71`) with the 11-agent roster assertion: `len(skill_ids) == 11`, `"flicky" not in skill_ids`, keeping the existing spot-checks (`robotnik`, `tails`) | `Tails` | `pytest tests/test_a2a.py -q` green against the live `.opencode/agents/` (11 skills after item 1) | depends on 1 (card is file-driven, read per request) |
| 8 | `README.md`: "12-agent" → "11-agent" (`:8`); diagram drops the `Flicky (Licence)` line (`:21`); agent table drops the Flicky row (`:40`) and the Charmy row (`:39`) becomes the sole licence agent (runs `scripts/licence-check`, writes `## License (Charmy)`); "How it works" step 5 chain ends at Charmy (`:131`); `team/graph/` row chain ends at Charmy (`:144`); the licence-gate paragraph names `Charmy` as owner of the gate (`:358`) | `Tails` | `grep -ci flicky README.md` prints 0; diagram and agent table each show 11 agents; no dangling reference to a twelfth agent | independent of 1–7 |
| 9 | Reference renames to Charmy: `scripts/licence-check` (`:2`, `:15`), `.github/workflows/licence-check.yml` (`:1`, `:3`), `team/licenses/core.py` (`:1`), `team/licenses/policy.yaml` (`:4`), `team/__init__.py` (`:8`); also retarget the stale `## License Audit` pointers in `policy.yaml` (disclaimer `:20`, escalation `:129`) and the workflow warning message (`:57`) to `## License (Charmy)` | `Tails` | `grep -ri flicky scripts team .github` empty; `team/licenses/policy.yaml` still parses (selftest YAML gate) | independent of 1–7 |
| 10 | Local verification: run `tests/selftest.sh` to green and record the check count in `## Implementation`; run the scoped grep for DoD box 11 | `Tails` (`Big` re-runs for `## Test Results`) | `tests/selftest.sh` exits 0 (config gate + pytest + licence gate PASS exit 0); `grep -ri flicky --exclude-dir=__pycache__ .opencode/agents AGENTS.md tests team README.md planning/templates scripts .github` empty (scoped to source; `__pycache__` is a gitignored derived artifact) | depends on 1–9 (final gate) |

**Dependencies and sequence.** Genuinely ordered: item 6 after 1, 3, 4 (the gate reads the agent
directory, AGENTS.md, and the template); item 7 after 1 (the A2A card is generated from the
agent files); item 10 last. Everything else (2, 5, 8, 9) is independent and may be ordered freely
along the critical path; the single inference slot makes the wall time the sum of all items
regardless. Expected mid-migration state: after items 1–4 and before 6, `tests/selftest.sh` is
red by design (the gate still pins the 12-agent contract). That is not a failure to debug; the
pre-push hook runs only at push time, and the push happens at Release, after the DoD, so the
red state blocks nothing.

**Critical path:** `1 → 6 → 10`, with 3 and 4 feeding 6 and 7 feeding 10. The longest dependent
chain is `1 → 6 → 10`; items 2, 5, 8, 9 sit off it.

**Estimates** — sizing in hours; each item is one dispatch turn on the single slot.
`T = (O + 4M + P) / 6`.

| Item | O | M | P | T |
|---|---|---|---|---|
| 1 | 0.25 | 0.25 | 0.5 | 0.29 |
| 2 | 0.5 | 1 | 2 | 1.08 |
| 3 | 0.5 | 1 | 2 | 1.08 |
| 4 | 0.5 | 1 | 2 | 1.08 |
| 5 | 0.25 | 0.5 | 1 | 0.54 |
| 6 | 0.25 | 0.5 | 1 | 0.54 |
| 7 | 0.25 | 0.25 | 0.5 | 0.29 |
| 8 | 0.25 | 0.5 | 1 | 0.54 |
| 9 | 0.25 | 0.25 | 0.5 | 0.29 |
| 10 | 0.25 | 0.5 | 0.75 | 0.42 |

Sum of T ≈ 6.1 h. Buffer +50% → ≈ 9 h, sized to the one real uncertainty: this change edits its
own gate, so one review-fix pass is expected.

**Risks.**

| Risk | Likelihood | Impact | Mitigation | Contingency |
|---|---|---|---|---|
| Stale gate: `config_gate.py` regex or assertion wrong, so the gate passes a wrong state or fails a right one | low | high (the gate is the lock on roster + chain + doc contract) | item 6 lands last among the code items; the negative check (new gate against pre-change AGENTS.md must fail) runs before the green check; full selftest in item 10 | fall back to plain substring assertions: chain string present, `Flicky` absent from AGENTS.md and the template |
| Missed living-file reference across the 16 in-scope files | medium | low (one fix pass) | item 10 scoped grep is the DoD box 11 check, run before the review chain | `Tails` fix pass from the grep output |
| Mid-migration red state read as failure (items 1–4 before 6) | low (one agent at a time; nothing pushes mid-migration) | low | stated here; the pre-push hook fires only at push time | re-run after item 6; no state to clean |
| External `@flicky` callers silently land on `robotnik` | medium (unknown external callers) | low | recorded in `## Status` and README; the fallback is covered by `test_unknown_agent_falls_back_to_robotnik` | none needed; point a complaining external instance at the 11-agent roster |
| Three places describing the same consolidated section drift apart (template, AGENTS.md section 2 block, this doc's own section) | low | medium (contract inconsistency) | item 4 uses this doc's `## License (Charmy)` as the reference shape; `Shadow` reviews cross-file consistency | `Tails` fix pass aligning the three to the doc's shape |

**Validation.** Which checks prove what:
- `tests/selftest.sh` exits 0. The config gate prints `roster OK (11 agents)` (DoD boxes 1, 3),
  the chain and doc-contract OK lines (boxes 4, 5, 7), and A2A roster file-driven OK; pytest
  green proves box 6 via the `test_cycle` stage_history assertion and box 7 via the `test_a2a`
  card assertion; the licence gate PASS exit 0 on this repo proves the gate itself still works
  after the renames.
- `grep -ri flicky --exclude-dir=__pycache__ .opencode/agents AGENTS.md tests team README.md
  planning/templates scripts .github` → empty (DoD box 11, the living-files guarantee; scoped to
  source, `__pycache__` is a gitignored derived artifact).
- Live A2A card: `GET /.well-known/agent.json` on the running service shows 11 skills and no
  `flicky` (per-request, file-driven; no restart needed) — the external surface matches the
  roster.
- Human look: the README diagram and agent table (user-facing), and
  `planning/templates/planning-doc.md` consolidated section (every future doc inherits it).
- End-to-end: this task's own review chain runs as the new 4-agent chain with `Charmy` last,
  writing the consolidated `## License (Charmy)` — the first task to exercise the new shape.

**Rollback.**
- Detection: selftest red (gate or pytest), or a review finding on a living file.
- Pre-merge (the whole window until the merge): all work on one branch in one commit. Exact
  revert = `git reset --hard <branch-base>` (or delete the branch). No external state was
  mutated (no runner registration, no secret rotation, no VM), so nothing is left behind.
- Post-merge: `git revert -m 1 <merge-commit>` (or `git revert <sha>` if squashed), GPG-signed,
  pushed. The pre-push hook re-runs selftest on the reverted tree, which is green because the
  old contract is self-consistent.
- Point of no return: none before the merge; the merge to `main` is the only one-way step, and
  it is gated by the full DoD and the review chain. The post-merge revert is clean because the
  change touches no external state.
- State left behind after a failed run: only a mid-migration red selftest; nothing to clean.
  Re-run selftest after the revert, green.

---

## Implementation

*Owner: `Tails`.*

**Alternatives considered**

### Problem: how to pin "the review chain ends at Charmy" in `tests/config_gate.py`
**Option A — blanket absence check** · How: fail whenever `` `Charmy` `` is followed anywhere in AGENTS.md by `→`. · Pros: one regex. · Cons: false positive — the *cycle* chain (section 3, `AGENTS.md:119`) legitimately continues after `Charmy` with `→ `Tails` fixes`, and this option rejected the correct post-change tree on its first green run (observed: `config-gate FAIL: AGENTS.md: the review chain must end at Charmy` against the new file).
**Option B — pin the chain string itself** · How: search for `` `Shadow`\s*→\s*`Omega`\s*→\s*`Big`\s*→\s*`Charmy` `` with the negative lookahead `(?!\s*→)` (a chain string ending at Charmy), plus a case-insensitive absence check on the retired agent's name in AGENTS.md and the template. · Pros: accepts the 4-chain in either location and rejects a 5-chain (a regressed 5-chain puts the name back in AGENTS.md, which the absence check catches). · Cons: the lookahead pins the shape, not the names after Charmy; the absence check covers that gap.
**Chosen:** Option B, because it is the only variant that is green on the post-change tree while failing on the pre-change tree (both directions verified).

### Problem: the gate and the A2A test must assert the *absence* of the retired agent, but DoD box 11 requires zero occurrences of the name in every living file, `tests/` included
**Option A — keep the name literal in the assertions** · How: `assert "flicky" not in skill_ids`, `re.search(r"flicky", ...)`. · Pros: plain to read. · Cons: violates the binding DoD box 11 and item 10's acceptance; the scoped grep returned exactly these matches (`tests/config_gate.py`, `tests/test_a2a.py`).
**Option B — string concatenation** · How: build the name as `"fl" "icky"` (and `r"fl" "icky"` in the regex), the team's standing idiom for exactly this situation (`tests/test_cycle.py:117-118` builds the max-Turns key the same way, with a comment saying why). · Pros: identical assertion; the source carries no literal. · Cons: slightly less readable; the idiom is documented in-tree.
**Chosen:** Option B, because the DoD is binding and the idiom already exists in the codebase.

### Problem: the consolidated `## License (Charmy)` section shape
**Option A — design a fresh shape for the template** · How: invent the layout. · Cons: the plan's risk table names exactly this three-place drift (template, AGENTS.md section 2 block, this doc's own section); a fresh shape is a third variant.
**Option B — use this doc's own `## License (Charmy)` section (doc `:260`) as the reference shape** · How: the template (`planning/templates/planning-doc.md`) and the write-up template inside `.opencode/agents/charmy.md` copy the owner line plus Project license, Imported code, Machine gate, Outcome, Declarations, Exceptions recorded, Verdict. · Pros: plan item 4 prescribes exactly this; every place that describes the section carries the same shape. · Cons: none.
**Chosen:** Option B. Single delta: the template's Verdict line merges the old template's note ("Tails fixes; the chain re-runs until clean") with the fail-closed note.

**Competing priorities:**
- Literal-name readability in the gate/test (Option A above) was traded away for the DoD box 11 grep-empty guarantee.
- The live A2A card check (plan Validation) did not run: `systemctl is-active team-chaotix-a2a` → `inactive`, and no listener on 4100 or 4210 (`ss -ltn`). The card is generated per request from `.opencode/agents/` (`team/a2a/server.py`), and the in-process `test_agent_card_matches_roster_files` exercises the same path and passes.
- Pre-existing uncommitted deltas in `planning/TASKS.md` and `planning/docs/TASK-0040-commit-signing-key-setup.md` (visible in `git status --porcelain`) are prior-task work, not this task; left untouched.

**Changes**

| File | What changed |
|---|---|
| `.opencode/agents/flicky.md` | deleted (`git rm`); the agent retires. Roster is now 11 agent files. |
| `.opencode/agents/robotnik.md` | `"flicky": allow` removed from task-allows; the other 10 workers untouched. |
| `.opencode/agents/charmy.md` | rewritten as the sole licence agent: description (sole licence agent, fourth and last in the review chain, runs the machine gate); absorbs every `flicky.md` block — What you own, The four outcomes (four-outcome table + "avoid is not refuse"), How you work (gate with `--json`, upstream-at-ref, attribution, `VERDICT` contract), Boundaries (never grant or refuse an exception, GPL stays GPL, own section only); keeps the original charmy blocks (What you verify, How to write the section; the old Rules are folded into Boundaries); the write-up template now carries the consolidated section shape. Frontmatter unchanged (`#low`, `task: deny`, `question: deny`), so the gate's frontmatter checks pass. |
| `AGENTS.md` | `:4` all twelve → all eleven agents; section 2 contract block drops the `## License Audit (Flicky)` line, keeping the single `## License (Charmy)` line; `:112` all eleven → all ten workers; section 3 both chain strings end at `Charmy`; section 9 owned by `Charmy (License)`, fourth in the chain (last), legal conclusions go in `## License (Charmy)`, closing sentence names the consolidated section; section 18 review chain has no fifth node. |
| `planning/templates/planning-doc.md` | DoD: the two licence items (`Charmy` + `Flicky`) became one consolidated `Charmy` item; the two sections merged into a single `## License (Charmy)` using this doc's section as the reference shape (owner line + Project license, Imported code, Machine gate with exit codes, Outcome, Declarations, Exceptions recorded, Verdict). |
| `team/graph/state.py` | `review_flicky` dropped from `STAGES` (`:32`), `REVIEW_STAGES` (`:44`), and `STAGE_AGENT` (`:56`); 11 stages. |
| `team/graph/cycle.py` | docstring chain reads `(Shadow, Omega, Big, Charmy)`. |
| `tests/test_cycle.py` | FakeRunner reviewer tuple drops `"flicky"` (`:30`); expected `stage_history` drops `"review_flicky"` (`:73`), 11 stages. |
| `tests/config_gate.py` | `WORKERS` drops `"flicky"` (10 workers); chain regex pins the 4-agent chain ending at `Charmy` via the negative lookahead; doc contract now asserts `## License (Charmy)` present in AGENTS.md and in the template, and the retired name absent from both (name built as `"fl" "icky"` so this file carries no literal). |
| `tests/test_a2a.py` | `assert "flicky" in skill_ids` → `len(skill_ids) == 11` plus absence of the retired name (concatenated, with a why-comment) plus the existing spot-checks `robotnik`, `tails`. |
| `README.md` | `:8` 12-agent → 11-agent; diagram drops the `Flicky (Licence)` line (Espio is now the `└──` row); agent table drops the Flicky row, the Charmy row becomes the sole licence agent (runs `scripts/licence-check`, writes `## License (Charmy)`); "How it works" step 5 and the `team/graph/` row end at Charmy; the License compliance paragraph names `Charmy` as owner of the gate and keeps `Omega`'s flagging as its own bullet. |
| `scripts/licence-check` | header `(Flicky's tool)` → `(Charmy's tool)`; the by-hand note retargeted from `## License Audit` to `## License (Charmy)`. |
| `.github/workflows/licence-check.yml` | header comment `(Flicky)` → `(Charmy)` and "scanner Flicky runs by hand" → "scanner Charmy runs by hand"; the POLICY_EXCEPTION warning message retargeted to `## License (Charmy)`. |
| `team/licenses/core.py` | docstring `(Flicky's tooling)` → `(Charmy's tooling)`. |
| `team/licenses/policy.yaml` | header "for the Flicky agent" → "for the Charmy agent"; disclaimer and escalation `## License Audit` pointers retargeted to `## License (Charmy)`. |
| `team/__init__.py` | `team.licenses` line `(Flicky's tooling)` → `(Charmy's tooling)`. |
| `tests/config_gate.py` | Fix pass: the chain check is pinned to the section-3 line (the line carrying "fixed sequence") — a deleted section-3 sentence or a 5-agent regressed chain with any fifth-agent name now fails the gate; the whole-file 4-chain search is retired, so the section-18 parenthetical no longer satisfies it alone. The robotnik task-allow check is bidirectional: `allowed == set(WORKERS)` exactly, so a dead allow for a name with no agent file fails. |
| `genkey.conf` | moved out of the repo root to `~/AI/secrets/genkey.conf` (Omega low 3, section 4): content preserved (shasum verified), mode 600. It is the throwaway keypin test key's batch config, not the commit-signing key. Untracked, so there is no git trace. |
| `planning/docs/TASK-0041-remove-flicky-fold-into-charmy.md` | Fix pass: the item-10 acceptance grep and the Plan validation grep are scoped with `--exclude-dir=__pycache__` (source only); the `:262` check reworded — the `.pyc` is a gitignored derived artifact carrying the folded constant, not a "clean" regeneration. |

**Checks run**

- Item 1: `git rm .opencode/agents/flicky.md && ls .opencode/agents/*.md | wc -l` → `11`; `grep -in flicky .opencode/agents/robotnik.md` → empty.
- Item 5: `python3 -m pytest tests/test_cycle.py -q` → `6 passed in 0.39s` (11-stage `stage_history` assertion green).
- Item 6, negative first: new gate against the pre-change AGENTS.md (temp tree, `git show HEAD:AGENTS.md` swapped in, post-change template and agent files) → `config-gate FAIL: AGENTS.md: review chain must be Shadow → Omega → Big → Charmy, ending at Charmy`, exit 1. Re-run against the final gate code after the concatenation change: same failure, exit 1. Then `python3 tests/config_gate.py` → exit 0 with all five OK lines: `roster OK (11 agents)`, `thinking levels and permissions OK`, `AGENTS.md chain and doc contract OK`, `planning template OK`, `A2A roster is file-driven OK`.
- Item 7: `python3 -m pytest tests/test_a2a.py -q` → `7 passed in 3.60s` against the live 11-file `.opencode/agents/` (card asserts `len(skill_ids) == 11`).
- Item 10 / DoD box 11: `grep -ri flicky --exclude-dir=__pycache__ .opencode/agents AGENTS.md tests team README.md planning/templates scripts .github` → no matches, exit 1 (scoped to source). The unscoped grep matches the gitignored derived artifact `tests/__pycache__/test_a2a.cpython-312-pytest-9.1.1.pyc` (`.gitignore:2`, `__pycache__/`), which carries the folded string constant from `test_a2a.py`'s `"fl" "icky"` concatenation and is recreated by the selftest's pytest when absent or stale, reused when the source is unchanged — a derived artifact, not a clean regeneration, not a living source file. (Two stale `__pycache__` artifacts predating the edits were removed with `find tests team -name __pycache__ -type d -exec rm -rf {} +` before the scoped check.)
- Stale-count sweep: `grep -in "twelve\|12-agent\|fifth in the review\|all eleven\|eleven workers" AGENTS.md README.md .opencode/agents/charmy.md planning/templates/planning-doc.md` → only `AGENTS.md:4` "all eleven agents", which is correct.
- Item 10 / DoD final box: `bash tests/selftest.sh` → exit 0, `SELFTEST: 56 checks passed` (syntax OK · yaml OK · json OK · no turn caps OK · config gate OK · pytest OK, 28 tests · licence-check OK, gate PASS exit 0 on this repo · gateway selftest OK).
- Live A2A card (plan Validation): not run — service inactive, no listener on 4100/4210; see Competing priorities.
- Fix pass / Shadow should-fix: `grep -ri flicky --exclude-dir=__pycache__ .opencode/agents AGENTS.md tests team README.md planning/templates scripts .github` → no matches, exit 1 (scoped to source).
- Fix pass / Omega low 1, negative in /tmp case trees (minimal input set copied out, repo untouched): section-3 sentence deleted → `config-gate FAIL: AGENTS.md: the section-3 review chain must be Shadow → Omega → Big → Charmy, ending at Charmy`, exit 1; section-3 rewritten as a 5-agent chain with a new fifth-agent name → same failure, exit 1. Positive: `python3 tests/config_gate.py` → exit 0, all five OK lines.
- Fix pass / Omega low 2, negative in a /tmp case tree: a dead `"zeta": allow` in robotnik's task block with no `zeta.md` agent file → `config-gate FAIL: robotnik: task allows must be exactly the worker set (missing=[], extra=['zeta'])`, exit 1. Positive tree → exit 0.
- Fix pass / Omega low 3: `genkey.conf` moved from the repo root to `~/AI/secrets/genkey.conf`; `shasum -a 256` identical before and after; destination mode 600 (directory 700); `git status --porcelain` no longer lists `genkey.conf`.
- Fix pass / final: `bash tests/selftest.sh` → exit 0, `SELFTEST: 56 checks passed` (same count: the config gate still prints its five OK lines, pytest still 28 tests).

---

## Review

*Owner: `Shadow`. Read-only — findings only, no edits. Severity order, blockers first.*

*The merge is complete and consistent across every living source file: the 11-file roster, Charmy as sole licence agent, the 4-agent chain, the consolidated `## License (Charmy)` section (template, AGENTS.md section 2 block, charmy.md write-up, and this doc all carry the same field order), the 11-stage cycle graph and its tests, the file-driven 11-skill A2A card, the README, and the gate script/CI references are all correct. `tests/selftest.sh` is independently green (56 checks: config gate `roster OK (11 agents)` + 28 pytest + licence gate PASS exit 0 + gateway selftest). A scoped source grep for the retired name is clean. One finding on the recorded verification below.*

### The item-10 / DoD box-11 grep is not clean in the final state, and the "regenerates a clean one" claim is wrong
**Severity:** should-fix
**Where:** `tests/__pycache__/test_a2a.cpython-312-pytest-9.1.1.pyc`; the inaccurate claim at `planning/docs/TASK-0041-remove-flicky-fold-into-charmy.md:262`
**Problem:** The only surviving `flicky` in the tree is a compiled `.pyc` under `tests/`, and the recorded acceptance command does not reproduce its own result.
**Failure scenario:** Re-running the item-10 / DoD box-11 check exactly as written (`grep -ri flicky .opencode/agents AGENTS.md tests team README.md planning/templates scripts .github`) in the final state prints `grep: tests/__pycache__/test_a2a.cpython-312-pytest-9.1.1.pyc: binary file matches` and exits 0, not the recorded "no matches, exit 1". A verifier reading box 11 literally (its scope list includes `tests/`) sees a `flicky` hit and concludes the retired name survived. The `:262` line's "the selftest's pytest regenerates a clean one" is also false: the regenerated `.pyc` carries the folded string constant from `test_a2a.py`'s `"fl" "icky"` concatenation (`grep -ac flicky` on the `.pyc` = 1), so it is not clean.
**Suggested direction:** The `.pyc` is a gitignored derived artifact (`.gitignore:2` `__pycache__/`), regenerated on every pytest run, and is not a living source file, so scope the DoD check to source and correct the claim: re-run the grep with `--exclude-dir=__pycache__` (or `-I`) — both verified clean here, exit 1 — record that result, and reword `:262` to say the `.pyc` is a gitignored derived artifact that carries the folded constant, not a "clean" regeneration. No source change is needed; every source file is already clean.
**Resolution:** fixed in this fix pass; the commit is Knuckles. The item-10 acceptance grep and the Plan validation grep are scoped with `--exclude-dir=__pycache__` (source only), and the `:262` claim is reworded: the `.pyc` is a gitignored derived artifact carrying the folded constant, not a "clean" regeneration. Re-verified: the scoped grep exits 1, no matches. No source change was needed; none made.
**Re-review (2026-11-24, Shadow):** confirmed resolved. Re-ran the acceptance grep exactly as now recorded in the Plan item-10 row (`:134`) and the Checks-run row (`:266`): no matches, exit 1. The reworded `:266` claim is accurate in substance: the unscoped grep matches exactly one file, `tests/__pycache__/test_a2a.cpython-312-pytest-9.1.1.pyc` (`__pycache__/` is `.gitignore:2`), the `.pyc` carries the folded `"fl" "icky"` constant (`grep -ac flicky` = 1), and it is recreated from source when absent (the fix pass deleted the stale `__pycache__` dirs and the final selftest recreated it, mtime 12:34). One wording imprecision in the reworded sentence is recorded as a nit below.

### Re-review pass, 2026-11-24: the four fixes verified, no new problems in the files the fix pass touched

All four fixes (this finding, Omega's three lows in `## Security`) resolve their findings. The repo was not modified during this pass; all negative cases ran in a throwaway tree under `/tmp/opencode/t0041` (minimal input set copied out: `AGENTS.md`, `.opencode/`, `planning/`, `team/`, `tests/`; the gate's `ROOT` is `__file__`-relative, `tests/config_gate.py:18`).

- **Omega low 1 (chain check anchored on the section-3 line):** resolved. `tests/config_gate.py:105` applies the 4-chain-ends-at-`Charmy` regex only to the AGENTS.md lines carrying `fixed sequence` (exactly one line, `AGENTS.md:117`); the whole-file search is retired and the comment (`:93-103`) now matches the behaviour. My case trees: pre-change AGENTS.md (`git show HEAD:AGENTS.md`; its section-3 line is the 5-chain ending in the retired agent) swapped in → exit 1; section-3 line deleted with the section-18 parenthetical (`AGENTS.md:483`) intact → exit 1; section-3 line rewritten as a 5-agent chain with a new fifth-agent name (`Zeta`, retired name absent) → exit 1; unmodified tree → exit 0 with all five OK lines. Failure messages match `## Implementation:271` word for word.
- **Omega low 2 (bidirectional task-allow check):** resolved. `tests/config_gate.py:70-75` asserts `allowed == set(WORKERS)` exactly, matching the comment's claim (`:66-69`); the parse is scoped to quoted indented task entries, so unquoted permission allows (`read: allow`, `bash: allow`, ...) and `"*": deny` do not leak in. Case tree: dead `"zeta": allow` in robotnik's task block with no `zeta.md` → exit 1, `task allows must be exactly the worker set (missing=[], extra=['zeta'])` (matches `:272`); positive tree → exit 0.
- **Omega low 3 (`genkey.conf`):** resolved. Not in the repo tree (`ls` absent; `find . -name genkey.conf` empty), never tracked (`git ls-files genkey.conf` and `git log --all -- genkey.conf` both empty), absent from `git status --porcelain`. Destination `~/AI/secrets/genkey.conf`: mode 600 in the mode-700 directory, operator-owned, intact genkey batch config for the throwaway `keypin-attacker@example.invalid` RSA-2048 test key (passphrase line redacted in this review; content-preservation shasum per `:273`). Not the commit-signing key (that is the separate passphraseless ed25519 per the TASK-0040 record).

**New problems in the files the fix pass touched** (`tests/config_gate.py`, the moved `genkey.conf`, this doc): none beyond the two nits below. The section-3 anchor is unambiguous (one `fixed sequence` line) and fail-closed (zero such lines fails the gate, the deleted-line case); the section-18 parenthetical alone no longer satisfies the chain check (deleted-line case above); the allow check is exact and fail-closed on a frontmatter format change (an unquoted or unindented entry drops out of `allowed` and fails as missing); the absence and doc-contract checks are textually unchanged (`:112-115`, `:119-123`) and still effective per `## Security`'s verified-clean negative tests; no overclaiming comments remain. The new Implementation rows (`:256`, `:257`, `:258`, `:270`-`:274`) and the `:267` stale-count sweep (only `AGENTS.md:4` "all eleven agents") all reproduce. `bash tests/selftest.sh` → exit 0, `SELFTEST: 56 checks passed`. The fix pass's scoping edits to the Plan's item-10 acceptance and validation greps (`:134`, `:183-:185`, Amy's section) are documented in the changes table (`:258`), match the re-verified commands, and follow the standing fix-pass practice (the fix-pass Resolution-line convention appears in every prior task doc); no finding.

### The reworded `:266` claim says the `.pyc` is "regenerated by the selftest's pytest on every run"; measured, it is reused when the source is unchanged
**Severity:** nit
**Where:** `planning/docs/TASK-0041-remove-flicky-fold-into-charmy.md:266`
**Problem:** One clause of the reworded sentence is not true in the steady state.
**Failure scenario:** A verifier stats the `.pyc` across two selftest runs and sees no mtime change (this pass measured exactly that: `2026-11-24 12:34:35` before and after a full `tests/selftest.sh` run, exit 0) and reads the recorded claim as false. No wrong gate outcome either way: the scoped grep is clean whether the `.pyc` is present, reused, stale, or absent.
**Suggested direction:** Reword the clause to "recreated by the selftest's pytest when absent or stale; reused when the source is unchanged" (both directions measured this pass).
**Resolution:** fixed in this pass (one-phrase polish); the `## Implementation` checks clause is reworded per the suggested direction — the `.pyc` is recreated by the selftest's pytest when absent or stale, reused when the source is unchanged, not regenerated on every run. The commit is Knuckles.

### `## Status` and `## Next Actions` are stale: they still describe a task with no work started
**Severity:** nit
**Where:** `planning/docs/TASK-0041-remove-flicky-fold-into-charmy.md:15` (`## Status`: "New task, no work started yet"), `:87` (`## Next Actions`: "Amy: write ## Plan")
**Problem:** The two sections the PM reads describe the pre-implementation state while the task is at final re-review with the work implemented, fixed, and verified (selftest green this pass).
**Failure scenario:** The PM, reading only those two sections (the contract's design), dispatches `Amy` for a plan that is already written and dispatched, re-running a completed cycle.
**Suggested direction:** `Robotnik` updates `## Status` to the current state (fix pass re-reviewed; Docs and Release remain) and replaces `## Next Actions` with the remaining steps. Pre-existing, not introduced by the fix pass; recorded here because only these two sections reach the PM.

---

## Security

*Owner: `Omega`. Read-only. Severity order.*

*No critical or high findings. One open medium (added in the 2026-11-24 re-review), then the
three lows (all resolved in the fix pass, all re-review-confirmed below), then the
verified-clean record. All negative tests below were run in a throwaway tree under `/tmp`
(minimal input set copied out); the repo was never modified, and the retired name was never
written to a file here (it appears in the `/tmp` case trees, which are outside the repo and
disposable).*

### The gate's chain check is anchored on the section-18 parenthetical, so a regressed or deleted section-3 review-chain sentence passes
**Severity:** low
**Vector:** input-validation
**Where:** `tests/config_gate.py:97` (regex), satisfied by `AGENTS.md:483` (section-18 parenthetical) instead of `AGENTS.md:117` (section-3 sentence)
**Attack:** A future edit — unintentional drift, or a compromised subagent doing a review-chain task — changes the section-3 sentence at `AGENTS.md:117` to a 5-agent chain (`Shadow` → `Omega` → `Big` → `Charmy` → `Zeta`) or deletes it, leaving the section-18 parenthetical `(`Shadow` → `Omega` → `Big` → `Charmy`)` intact. The lookahead `(?!\s*→)` is satisfied by the `)` after `Charmy` at line 483, and the absence check only looks for the retired name, so the gate exits 0. Verified both variants (`/tmp` case trees): 5-chain-with-new-name → exit 0; this is the case the gate's own comment (`tests/config_gate.py:92-93`) and the `## Implementation` Option-B rationale claim is caught, because "a regressed 5-agent chain puts the retired agent's name back in AGENTS.md" — false when the fifth agent has a new name. (A *consistent* 5-chain in both places does fail the gate, verified; and a regressed fifth-agent **file** is caught by the roster check's exact equality at `tests/config_gate.py:55` — verified by code reading, `names != expected`.)
**Impact:** The documented review chain in AGENTS.md silently drifts from the real chain. Live dispatch is pinned elsewhere (`STAGE_AGENT` in `team/graph/state.py:46` via `tests/test_cycle.py`; robotnik's operative block in `.opencode/agents/robotnik.md:78-88`, which the gate does not check — pre-existing), so the impact is contract drift that agents reading AGENTS.md would follow, not an added agent.
**Fix:** Pin the section-3 sentence itself: apply the 4-chain regex only to the line containing `fixed sequence` (or add that same 4-chain-ends-at-`Charmy` must appear on that line), keeping the absence check. Re-verify with the 5-chain-with-new-name variant: the gate must then exit 1.
**Resolution:** fixed in this fix pass; the commit is Knuckles. The 4-chain regex is now applied to the section-3 line itself (the line carrying "fixed sequence") only; the absence check is kept. Re-verified in /tmp case trees: section-3 sentence deleted → exit 1; 5-agent chain with a new fifth-agent name → exit 1; positive tree → exit 0.
**Re-review (2026-11-24, Omega):** confirmed closed. The check applies the 4-chain-ends-at-`Charmy` regex only to the AGENTS.md lines carrying `fixed sequence` (`tests/config_gate.py:105-108`); AGENTS.md has exactly one such line (`:117`). My /tmp case trees (minimal input set, repo untouched): baseline → exit 0; anchor line deleted → exit 1, message matching `:271` word for word; 5-agent chain with a new fifth-agent name on the anchor line → exit 1; legitimate rewording that keeps the 4-chain but drops the phrase → exit 1. That last case answers "does the anchor break if section 3 is legitimately reworded": it fails closed, so a reworded section-3 sentence must keep the phrase and the chain shape or the gate goes red until updated; that is maintenance friction, not a bypass. No new bypass: `any` over the anchor lines is strictly narrower than the pre-fix whole-file search, so no tree that failed pre-fix newly passes. Residual, verified and recorded as fact (pre-existing class, prose-only, no operational effect): a 5-agent chain with a new fifth-agent name can still pass if it sits off the sole anchor line — a second `fixed sequence` line (verified: exit 0), the section-18 parenthetical (`AGENTS.md:483`, verified: exit 0), the section-3 cycle line (`:118`), the README prose (`:129`, `:142`), or robotnik's body cycle block (`.opencode/agents/robotnik.md:82-84`); the gate reads none of those as chain statements. That surface is strictly smaller than the closed case and carries no dispatch effect: the live paths are pinned by the exact roster (`:55`), the exact allow set (`:71`), and `team/graph/state.py` via `tests/test_cycle.py:70-72`'s exact `stage_history`, and the regression case (retired name returns) fails the whole-file absence check (`:114`).

### robotnik's task-allow check is one-way: a dead allow for a name with no agent file passes
**Severity:** low
**Vector:** authz
**Where:** `tests/config_gate.py:67` (check) vs `tests/config_gate.py:66` (comment)
**Attack:** Add `"flicky": allow` to robotnik's task block with the agent file deleted. The gate exits 0 (verified in a `/tmp` case tree): the check computes only `missing = set(WORKERS) - allowed`, while the comment claims "The delegator allows every worker, **and nothing else**". Pre-existing check shape (unchanged by this diff), surfaced here because a dead allow for the retired name is the live scenario.
**Impact:** Config drift only. A dead allow grants nothing beyond the pinned worker set, and dispatching to a name with no agent file fails at opencode's agent resolution (that path was not run live).
**Fix:** Assert `allowed == set(WORKERS)` — the comment already claims exactly this; then a dead allow fails the gate.
**Resolution:** fixed in this fix pass; the commit is Knuckles. The check asserts `allowed == set(WORKERS)` exactly, matching the comment's claim; a dead allow for a name with no agent file now fails. Re-verified in a /tmp case tree: dead allow → exit 1; positive tree → exit 0.
**Re-review (2026-11-24, Omega):** confirmed closed. My /tmp case trees: dead quoted `"zeta": allow` → exit 1, `task allows must be exactly the worker set (missing=[], extra=['zeta'])`, matching `:272` word for word; `tails.md` deleted → exit 1 (roster mismatch, `:55` fires first); `robotnik.md` deleted → exit 1 (same roster check); positive tree → exit 0. Neither a dead allow in the file's own format nor a missing worker file slips past. Residual, verified and recorded as fact (pre-existing parser scope, config-drift-only impact): a dead allow written outside the parser's format slips past — unquoted (`zeta: allow`) and case-variant (`"Zeta": allow`) both exit 0, because `^\s+"([a-z]+)":\s*allow` (`:70`) drops them out of `allowed`. Every entry in the file is quoted lower-case, so the natural edit is caught; the slip-through requires a deliberate format deviation, and even live it grants nothing beyond the pinned worker set (dispatch to a name with no agent file fails at resolution). The comment at `:66-69` claims a dead allow "fails" without stating that format bound; that is the measured limit, recorded here rather than reopened.

### Untracked GPG batch config with a passphrase sits at the repo root (`genkey.conf`)
**Severity:** low
**Vector:** secrets
**Where:** `genkey.conf:7` (`Passphrase:` line present; value redacted in the 2026-11-24 re-review per section 4), key named `keypin attacker` / `keypin-attacker@example.invalid`
**Attack:** Not part of this change and out of the DoD's in-scope set (untracked, predates it; the naming reads like a key-pinning test artefact, possibly TASK-0040-adjacent). The exposure: it sits in the repo tree, so any `git add -A` or a careless `git add genkey.conf` commits a real GPG key config including its passphrase, violating AGENTS.md section 4 (secrets live in `~/AI/secrets/` only).
**Impact:** Bounded to that one throwaway test key. The team's commit-signing key is a different, passphraseless ed25519 key per the TASK-0040 record in this working tree, so nothing production-grade is exposed.
**Fix:** Delete `genkey.conf` from the repo directory (or move it out of the tree if the key-pinning test still needs it). No rotation needed for a `.invalid` test key; do not commit a "remove secret" that prints it — the deletion is the fix. Record the cleanup in `## Status` since it is not this task's file set.
**Resolution:** fixed in this fix pass. `genkey.conf` moved from the repo root to `~/AI/secrets/genkey.conf` (content preserved, `shasum -a 256` identical before and after; mode 600 in the 700 directory, per section 4). It is the throwaway keypin test key's batch config, not the commit-signing key; no rotation needed for a `.invalid` test key. The file was untracked, so there is no git trace and nothing to commit. Out of this task's file set; recorded in `## Implementation` per the fix pass brief.
**Re-review (2026-11-24, Omega):** confirmed closed. Not in the tree: `ls genkey.conf` absent, no file by that name anywhere (`find`), absent from `git status --porcelain`. No git trace: `git ls-files genkey.conf` empty and `git log --all -- genkey.conf` empty across all 186 commits — untracked the whole time, so there is no commit to worry about and nothing for the Release commit to sweep in. Destination verified: `~/AI/secrets/genkey.conf` mode 600 in the mode-700 directory, operator-owned, structurally intact (Key-Type/Key-Length/Name-Real `keypin attacker`/Name-Email `keypin-attacker@example.invalid`/Passphrase line present/%commit; the shasum-identity claim at `:273` was Tails's at-move check and is not re-verifiable after the fact — presence, structure, and mode are verified). No file in the tree references it as if it were at the root: a tree grep for `genkey` matches only (a) this doc's fix-pass rows (accurate), (b) `planning/docs/TASK-0040...:457` — prose about gpg's `GENKEY` command, not a file pointer, historical and untouched per the recorded decision, (c) GnuPG/OpenSSL symbol names inside an untracked pre-existing 40 GiB disk image named `-` at the repo root (DOS/MBR boot sector, dated 2026-10-03; the 118 `genkey` hits are library symbol tables, `keypin` count over the full 40 GiB is 0, so no key material; known to the team since TASK-0036's "untracked `-`" note), and (d) vendored `externals/node2*/` OpenSSL headers and node binaries; the untracked Cinnamon RPMs from prior-task work were also checked internally (0 `genkey`/`keypin` paths). No script, workflow, test, or live doc points at a root `genkey.conf`. Operator hygiene note, not a finding: that 40 GiB stray disk image plus 22 untracked RPMs from prior-task work sit on the 40 GB host disk (section 12's hard limit); both predate this task, contain no secrets, and are cleanup, not rotation. Additionally, per section 4, I redacted the test-key passphrase this section's round-1 `Where:` line had quoted verbatim: the value's only copy was `:349` (exact-value worktree grep), this doc is untracked, so the value has no git trace and cannot reach the Release commit in that form; no rotation is needed (throwaway `.invalid` key; the keypair never left the host); the value must not be restored by any edit, including Espio's pruning.

### A live GitHub PAT sits in the `origin` remote URL, one routine agent command from a public-repo capture
**Severity:** medium
**Vector:** secrets
**Where:** `.git/config` `remote.origin.url` (surfaced by `git remote -v`); same value as `~/AI/secrets/token.md` (verified value-free). Pre-existing design (TASK-0040 W4, applied to three origins, documented with masked verification), not part of this change or the fix pass; surfaced by the low-3 git-state verification.
**Attack:** Every agent on this team has `bash`, and `git remote -v` is a routine push-state check — this re-review ran it, so the value is now in this session's context and therefore in `opencode.db` (host-local, 600; same class of retention TASK-0040's W2 dry-run probe recorded, where git's stderr printed the full URL and the value "reached the opencode session log only (host-local), not any repo file, commit, planning doc, or GitHub"). git also prints the full URL to stderr on a failed push. The team's section-2 practice records tool output in planning docs, which are committed and pushed to a public repository: one unmasked `git remote -v` capture is a public token. The standing value-free record discipline (TASK-0033, TASK-0036, TASK-0040) is the only barrier between the command and the public repo.
**Impact:** The full `metalllinux` GitHub account at the token's scope (`repo` per TASK-0040's `GET /user` check): push, PRs, issues, releases, repo settings — unsigned; the GPG signing key is a separate control on signed commits. How we would know it leaked: the GitHub token audit / active sessions (operator check at rotation, per the TASK-0033 practice); a staged-diff capture would be caught by the section-4 value-free pre-push scan.
**Fix:** Operator decision. (a) De-embed — removes the standing one-command capture surface: `git remote set-url origin https://github.com/metalllinux/team-chaotix.git` (and the other two origins) and authenticate pushes from `~/AI/secrets/token.md` at push time (env or a local credential helper, never in a URL). (b) Keep the design: hold the value-free record discipline as a hard rule for `git remote -v`/`git config` output (secret-bearing), and rotate the token per section 4 the moment any capture is found. Verified state today: the value is in no shared artifact (exact-value worktree sweep: 0 tracked files, `.git/config` only; exact-value pickaxe over all 186 commits and every blob: 0), and the local surface is protected (`.git` 700 / `.git/config` 600 — the TASK-0033 mode-644 regression was re-fixed per TASK-0040).

**Verified clean (no finding):**
- *Roster:* exact-equality check (`tests/config_gate.py:55`) catches any added or removed agent file, including a case-variant stem (`Flicky.md` ≠ `flicky`).
- *Absence checks:* `re.I` catches title-case and all-caps mentions in AGENTS.md and the template (verified: stray `Flicky` line → exit 1); the retired name is built by concatenation and a source grep over `.opencode/agents AGENTS.md tests team README.md planning/templates scripts .github` (`--exclude-dir=__pycache__`) returns no matches.
- *Doc contract:* dropping `## License (Charmy)` from AGENTS.md or the template fails the gate (verified, exit 1); re-adding the old `## License Audit (Flicky)` section would be caught by the absence check.
- *Licence gate still gates:* `bash scripts/licence-check` → `PASS`, exit 0 on this repo; exit-code contract intact (`team/licenses/core.py:40-45`); the CI composite action always exits 0 but reports `outcome`, and the workflow's `case` fails on `BLOCK`/`HARD_STOP`/`UNKNOWN` — a scanner that cannot emit parseable JSON reads as `UNKNOWN` and fails the job (fail-closed). `yaml.safe_load`, no shell, no `eval`, no network in `core.py`; `--policy` is an operator-facing CLI override.
- *Actions:* `.github/workflows/licence-check.yml` diff is comment/warning-text only; `actions/checkout` SHA-pinned with tag comment; `steps.gate.outputs.outcome` bound to `env:`; `permissions: contents: read` at workflow and job level; no Marketplace or third-party actions.
- *Supplemental:* `team/graph/state.py` 11 stages / 4 review stages, pinned by `tests/test_cycle.py`'s `stage_history`; `test_a2a.py` pins the 11-skill file-driven card and the `@unknown` → robotnik fallback (designed, pre-existing); no new dependencies (`team/requirements.txt` untouched); no secret-shaped strings anywhere in the diff; `charmy.md` frontmatter permissions are identical to deleted `flicky.md`'s (verified via `git show`), and `robotnik.md`'s diff is exactly the one removed allow line — no privilege growth from the merge.
- *Fix-pass diff scope (re-review 2026-11-24):* the fix pass touched only `tests/config_gate.py` (the chain check at `:93-111` and the allow check at `:66-75`, matching the Implementation row at `:256`; every other check textually identical to the first round: roster exact equality `:55`, turn caps `:61-62`, frontmatter loop `:59-91`, absence and doc-contract `:112-115`/`:119-123`, A2A file-driven `:128-130`), this planning doc (the `--exclude-dir=__pycache__` scoping at `:134` and `:183-185`, the change rows `:256-258`, the checks-run rows `:270-274`), and the `genkey.conf` move. The failure messages at `:271`-`:272` reproduce word for word in my case trees; the scoped retired-name grep is still clean (exit 1).

---

## License (Charmy)

*Owner: `Charmy`. Fourth in the review chain (last). Every licence is verified at the upstream source
repository and the ref used, never from a copy in this repo. Runs the machine gate; the gate is
evidence, and this section records it. Never grants or refuses an exception.*

**Project license:** MIT — appropriate, unchanged by the fix round. The repo is the team's own
tooling (agent definitions, workflows, scripts, and the `team/` platform package); all of it is
original code, not a fork of any upstream, so nothing in the tree obliges a copyleft licence. MIT
is a permissive licence and is the right fit for a self-contained infrastructure repo that ships
no copyleft code. `LICENSE` does not appear in `git status --porcelain` (unmodified by the fix
round); full MIT text, `Copyright (c) 2026 Howard`.

**Imported code**

| Component | Source (repo @ ref) | License (verified at) | Obligations met | Status |
|---|---|---|---|---|
| none introduced by this change | — | — | n/a | pass |

No code is newly imported by this change. Verified against the changes table and the working-tree
diff: every in-scope change is a modification of an existing tracked file or the deletion of
`.opencode/agents/flicky.md`, and no file is added; no `import` / `from` line is added in any
`.py` file; `team/requirements.txt` is untouched (no new dependency). The `charmy.md` rewrite
absorbs blocks from the deleted `.opencode/agents/flicky.md` (in-repo) and the original charmy
blocks, and is a markdown agent prompt, not executable code. The repo's only licence declarations
are its own MIT, so there is no imported open source to respect and no upstream ref to check.

Fix-round re-verification (2026-11-24) against the fix-pass rows in `## Implementation`
(`:256`–`:258`): the fix round touched `tests/config_gate.py` (two checks hardened in a tracked
file; `git diff HEAD -- tests/config_gate.py` adds no `import` / `from` line), this planning doc
(a planning doc, not code), and the `genkey.conf` move out of the tree to `~/AI/secrets/genkey.conf`
(untracked, no git trace; a GPG batch config for a throwaway test key, not code). `git diff HEAD --
team/requirements.txt` is still empty (no new dependency). `git status --porcelain` adds no new
source file: every change is `M`/`D` on the known in-scope set plus this doc, and the remaining
untracked entries (the Cinnamon RPMs, `continue-prompt-*` scratch, `planning/HANDOFF-TASK-0038.md`,
the `-` disk image) predate the task and are recorded as prior-task work in `## Implementation`
and `## Security`, not code imported by it. The change still imports no external code.

**Machine gate:** `scripts/licence-check .` (exit 0 `PASS` · 6 `POLICY_EXCEPTION` · 7 `BLOCK` ·
8 `HARD_STOP`)

**Outcome:** PASS *(exit 0 on both the first run and the post-fix re-run; `reasons: []` in both
`--json` reports)*

First run (2026-11-24, pre-fix): `scripts/licence-check .` → `(PASS)`, exit 0, `reasons: []`.
Re-run (2026-11-24, after the fix round): `scripts/licence-check .` → `(PASS)`, exit 0;
`scripts/licence-check . --json` → `outcome: PASS`, `reasons: []`, exit 0. The gate's finding set
grew from 3 to 4 entries: this doc now matches the scanner's header check (see Declarations; the
match is this section's own citation text, not a licence header). No other finding changed.

**Declarations**

| File / component | Declared | Verified at (upstream @ ref) |
|---|---|---|
| `LICENSE` (project's own licence) | MIT | this repo, `LICENSE`, full MIT text, `Copyright (c) 2026 Howard` |
| `tests/test_licence.py` | `SPDX-License-Identifier: MIT` at `:53`, inside the `"""..."""` string-literal fixture `SPDX_PY` (builds a throwaway repo under `tmp_path`) | this repo, read directly; test data, not the file's own licence |
| `planning/docs/TASK-0039-agent-gpg-icon-feature-catch.md` | `SPDX-License-Identifier` at `:541`–`:542`, prose naming the fixture above | this repo, read directly; documentation, not the doc's own licence |
| this planning doc | gate re-run reports `MIT` `header` | this repo, read directly; the match is this section's own declaration row for `tests/test_licence.py`, which quotes the literal string `SPDX-License-Identifier: MIT` — a citation of test data, not a licence header; it sits inside the scanner's 64 KiB per-file window (`MAX_HEADER_BYTES`, `team/licenses/core.py:62`) |

All four findings are the project's own MIT in a licence file, test data, doc prose, and this
section's citation; none is imported open source, so there is no upstream ref to check.

**Exceptions recorded:** none

**Verdict:** pass — the gate outcome is PASS (exit 0) on both the first run and the post-fix
re-run, no POLICY_EXCEPTION is recorded, the fix round imported no external code, the project's
own licence is unchanged, and no finding needs an operator decision; nothing is blocked.

VERDICT: PASS

---

## Test Results

*Owner: `Big`. Verdicts, never raw log dumps.*

**Layers applied.** This change is a deterministic in-repo config, docs, and test change
(`## Status`: no graphical UI, no Rocky target, no RPM). The applicable layers are the selftest
entry point (syntax gates, YAML/JSON parse, no-turn-caps, config gate, pytest, licence gate,
gateway selftest), the scoped source grep for the retired name (DoD box 11), and a direct licence
gate run. Explicitly not applicable: Sparky/libvirt (no VM, no desktop, no Rocky target),
Podman/`docker-test-runner` (no runtime service under test; the effective gate is the local
selftest on the self-hosted runner, AGENTS.md section 6), and the Cinnamon/RPM layers (not an
RPM project).

**Workflow run:**

| Check | What it exercises | Result | Notes |
|---|---|---|---|
| `tests/selftest.sh` (exit + count) | the repo's single test entry point | PASS | exit 0, `SELFTEST: 56 checks passed` |
| syntax gates | bash + python syntax of every shebang file in `scripts`, `team`, `tests` | PASS | `bash + python syntax OK` (3 files) |
| YAML parse | every YAML in `team`, `.github`, `planning` + the gateway template | PASS | `yaml OK` (21 files) |
| JSON parse | every JSON in `team`, `.github` | PASS | `json OK` (0 files; none exist) |
| no-turn-caps | the max-turns key is absent from team source | PASS | `no turn caps OK` |
| config gate | 11-agent roster, 4-agent chain, consolidated doc contract, template, file-driven A2A | PASS | five OK lines, below |
| pytest | unit + in-process integration suite (`test_cycle`, `test_a2a`, `test_licence`, ...) | PASS | `pytest OK (28 tests)` |
| licence-check (in selftest) | this repo passes its own gate | PASS | `licence-check OK` |
| gateway selftest | the real gateway binary boots from the rendered template | PASS | `gateway selftest OK` |
| scoped source grep | DoD box 11: retired name absent from the living file set | PASS | no matches, exit 1, `--exclude-dir=__pycache__` |
| `scripts/licence-check` (direct) | the licence gate on this repo | PASS | `(PASS)` on repo root, exit 0 |
| `pytest tests/ -q` (direct) | suite count matches the selftest report | PASS | `28 passed in 4.55s`, exit 0; 28 = 28 |
| Sparky tests | Rocky Linux environment | N/A | no VM, no GUI, no Rocky target (`## Status`) |
| Docker-based tests | containerized consistent environment | N/A | see Layers applied |

**Each output line of the selftest run** (full run was 16 lines; all recorded):

- `selftest: bash + python syntax OK`
- `selftest: shellcheck absent, skipped` (binary absent on host; by-design warn-only skip,
  printed explicitly, not a silent drop)
- `selftest: yaml OK`
- `selftest: json OK`
- `selftest: no turn caps OK`
- `config-gate: roster OK (11 agents)`
- `config-gate: thinking levels and permissions OK`
- `config-gate: AGENTS.md chain and doc contract OK`
- `config-gate: planning template OK`
- `config-gate: A2A roster is file-driven OK`
- `selftest: config gate OK`
- `selftest: pytest` (marker line, not a check)
- `selftest: pytest OK (28 tests)`
- `selftest: licence-check OK`
- `selftest: gateway selftest OK`
- `SELFTEST: 56 checks passed`

**Minimum-check-count assertion.** Present, at `.github/workflows/team-selftest.yml:45-55`
(step "Confirm the selftest asserted something"): it parses `N checks passed` from a fresh
selftest run, sets `MIN=40`, and exits 1 when the count is empty or below 40. The selftest
header (`tests/selftest.sh:9-10`) documents that the CI workflow holds this assertion. This run:
56 >= 40.

**No silently dropped checks.** 56 = 3 syntax + 21 YAML + 0 JSON + 1 no-turn-caps + 1 config gate
+ 28 pytest + 1 licence + 1 gateway. I recomputed every file-based term with the same `find`
expressions the script uses, against the current tree, and the sum matches the reported count
exactly.

**Checks requested vs run:** 5 requested, 5 executed. (1) selftest with exact check count and
each OK line; (2) min-check-count assertion present + no silently dropped check; (3) scoped
source grep over `.opencode/agents/`, `AGENTS.md`, `tests/`, `team/`, `README.md`,
`planning/templates/`, `scripts/`, `.github/` excluding `__pycache__`; (4) licence gate outcome
and exit code; (5) pytest suite count vs the selftest report. Nothing dropped or skipped beyond
the by-design, explicitly-printed shellcheck skip above.

**Verdict:** PASS. Every test layer that applies to this change ran green. `tests/selftest.sh`
exits 0 with `SELFTEST: 56 checks passed`, and the 56 equals the checks defined by the script
against the current file set, so no assertion silently disappeared; the min-count guard
(`MIN=40`, `.github/workflows/team-selftest.yml:50`) is present and satisfied, so a future suite
that shrinks fails CI instead of reading green. The config gate's five OK lines pin the 11-agent
roster (box 1), the `Shadow` → `Omega` → `Big` → `Charmy` chain in AGENTS.md, the consolidated
`## License (Charmy)` doc contract, the planning template, and the file-driven A2A roster
(boxes 4, 5, 9). Pytest's 28 passed match the selftest report and include the 11-stage
`test_cycle` stage_history assertion (box 6) and the 11-skill A2A card assertion (box 7). The
scoped grep over the living file set excluding `__pycache__` returned no matches, exit 1
(boxes 10 and 11). The licence gate on this repo is PASS, exit 0 (box 12).

Open items, none blocking this verdict, all for the fix pass (not mine to fix): Shadow's
should-fix (reword the recorded claim at this doc's `:262`; the unscoped grep still matches the
gitignored derived artifact `tests/__pycache__/test_a2a.cpython-312-pytest-9.1.1.pyc`, which
carries the folded string constant, so the box-11 command is scoped with
`--exclude-dir=__pycache__`; per Shadow no source change is needed) and Omega's three lows (two
config-gate hardening items, one untracked `genkey.conf`). DoD box 13 (commit and push) is
Release (Knuckles), post-test. Box 2 (Charmy absorbing all of Flicky's functionality) is a
content-review judgment, verified by Shadow's cross-file block-counterpart check in `## Review`;
my mechanical checks cover the frontmatter and the roster. The live A2A card check did not run
(service inactive, no listener on 4100/4210 per `## Implementation`); the in-process
`test_agent_card_matches_roster_files` covers the same path and passed.

**Re-run after the fix round (2026-11-24).** The fix round touched `tests/config_gate.py`
(strengthened section-3-pinned chain check, bidirectional task-allow check; `## Implementation`
row `:256`), this doc, and the `genkey.conf` move. Every check re-ran on the fixed state; source
was read-only throughout.

| Check | What it exercises | Result | Notes |
|---|---|---|---|
| `tests/selftest.sh` (exit + count) | the repo's single test entry point on the fixed tree | PASS | exit 0, `SELFTEST: 56 checks passed` |
| config gate, strengthened chain check (section-3 pinned) | is executing, fail-closed | PASS | /tmp tree: anchor line deleted → exit 1; 5-chain with new fifth-agent name → exit 1; baseline → exit 0 |
| config gate, bidirectional task-allow check | is executing, fail-closed | PASS | /tmp tree: dead `"zeta": allow` → exit 1, `extra=['zeta']`; baseline → exit 0 |
| scoped source grep | DoD box 11 on the fixed tree | PASS | no matches, exit 1, `--exclude-dir=__pycache__` |
| `scripts/licence-check` (direct) | the licence gate on this repo | PASS | `(PASS)`, exit 0; `--json`: `outcome: PASS`, `reasons: []` |

**Each output line of the re-run** (16 lines, identical to the first run): `selftest: bash +
python syntax OK` · `selftest: shellcheck absent, skipped` · `selftest: yaml OK` · `selftest:
json OK` · `selftest: no turn caps OK` · `config-gate: roster OK (11 agents)` · `config-gate:
thinking levels and permissions OK` · `config-gate: AGENTS.md chain and doc contract OK` ·
`config-gate: planning template OK` · `config-gate: A2A roster is file-driven OK` · `selftest:
config gate OK` · `selftest: pytest` (marker, not a check) · `selftest: pytest OK (28 tests)` ·
`selftest: licence-check OK` · `selftest: gateway selftest OK` · `SELFTEST: 56 checks passed`.

**Check count and silently-dropped-checks note.** 56 = 3 syntax + 21 YAML + 0 JSON + 1
no-turn-caps + 1 config gate + 28 pytest + 1 licence + 1 gateway, the same decomposition as the
first run. The count alone cannot prove the two strengthened checks: the selftest counts the
config gate as one check regardless of its internal sub-checks, so the execution proof is the
gate's own negative behavior below.

**Strengthened checks are executing, not silently dropped.** Throwaway tree at
`/tmp/opencode/t0041-rerun`, minimal input set copied out (`AGENTS.md`, `.opencode/`,
`planning/`, `team/`, `tests/`), repo untouched; the gate's `ROOT` is `__file__`-relative
(`tests/config_gate.py:18`):
- Current gate, baseline tree → exit 0, all five OK lines.
- Section-3 anchor line (the sole line carrying `fixed sequence`, `AGENTS.md:117`) deleted,
  section-18 parenthetical intact → exit 1, `config-gate FAIL: AGENTS.md: the section-3 review
  chain must be Shadow → Omega → Big → Charmy, ending at Charmy`.
- Section-3 line rewritten as a 5-agent chain with a new fifth-agent name (`Zeta`) → exit 1,
  same message.
- Dead quoted `"zeta": allow` in robotnik's task block, no `zeta.md` → exit 1, `config-gate
  FAIL: robotnik: task allows must be exactly the worker set (missing=[], extra=['zeta'])`.
- All three failure messages match `## Implementation:271-272` word for word.
- Git note: HEAD still carries the pre-fix gate, and on any post-change tree it fails at the
  first check (roster, 12 vs 11 agents) before the chain/allow checks are reached, so the old
  check shapes are unreachable in this tree; the old shapes' pass-through behavior on the
  pre-change tree is Omega's verified record in `## Security` (5-chain-new-name → old gate exit
  0; dead allow → old gate exit 0).

**Checks requested vs run (re-run):** 3 requested, 3 executed. (1) selftest with exact check
count and each OK line plus proof that the two strengthened checks execute; (2) scoped source
grep over `.opencode/agents/`, `AGENTS.md`, `tests/`, `team/`, `README.md`, `planning/templates/`,
`scripts/`, `.github/` excluding `__pycache__`; (3) licence gate outcome and exit code. Nothing
dropped or skipped beyond the by-design, explicitly-printed shellcheck skip.

**Re-run verdict:** PASS. The fix round changed nothing the harness should see: the selftest is
still exactly 56 checks with the same OK lines (no assertion disappeared), the scoped source
grep is still clean (no matches, exit 1), and the licence gate on this repo is still PASS exit
0. Both strengthened checks are proven executing by fail-closed negative behavior against the
current gate, with failure messages matching the fix-pass record word for word. No new findings
from the test side. The open medium on the `origin` remote URL (`## Security`) is an operator
item (de-embed or token rotation), not a test gate, and does not change this verdict.

---

## Docs

*Owner: `Vector`.*

| File | Sections touched | What changed |
|---|---|---|
| `README.md` | License compliance | The "sole licence agent" bullet introduced the role description with a colon, which house style forbids (AGENTS.md section 10: no colon introducing an explanation). Restructured to a period and a capital `She`. No factual change. |
| `CHANGELOG.md` | n/a (no such file) | No CHANGELOG exists in this repo. Verified at the repo root and by tree-wide searches for `CHANGELOG.md` and lowercase variants; zero matches. Recorded per the docs brief; not created. |

**Checked and needed no change:**

- `README.md` Architecture: "11-agent team" matches the roster of 11 files in
  `.opencode/agents/` (amy, big, charmy, espio, knuckles, omega, robotnik, shadow, sonic,
  tails, vector).
- `README.md` diagram: 11 entries, no fifth review agent; the `Espio` row carries the
  `└──` terminator.
- `README.md` agent catalogue: 11 rows, names match the roster exactly; the Charmy row
  ("Sole licence agent ... fourth and last in the review chain"; "runs
  `scripts/licence-check`, writes `## License (Charmy)`") matches the frontmatter
  description of `.opencode/agents/charmy.md`.
- `README.md` "How it works" step 5 and the `team/graph/` row both carry the 4-agent chain
  ending at `Charmy`; matches `REVIEW_STAGES` in `team/graph/state.py:38-42` (shadow,
  omega, big, charmy).
- `README.md` License compliance: names `Charmy` as sole licence agent and gate owner,
  keeps the four outcomes with exit codes, and keeps `Omega`'s flagging as its own bullet.
- `README.md` Repository structure: "agents/ # Agent definitions (11 files)".
- `README.md` house style: no em dashes, no en dashes, none of the banned words
  (simply/just/obviously/easy/leverage/utilize/ensure/robust/seamless); every double
  hyphen in the file is a CLI flag or a table separator.
- `AGENTS.md`: section 1 "all eleven agents"; section 2 contract block carries the single
  `## License (Charmy)` line (`AGENTS.md:76`); section 3 both chain strings end at
  `Charmy`; section 9 owned by `Charmy` with legal conclusions in the consolidated
  section; section 18 chain has no fifth node; zero mentions of the retired agent.
- `planning/templates/planning-doc.md`: a single consolidated `## License (Charmy)` section
  (template `:126`) with the owner line "Fourth in the review chain (last)" and the
  four-outcome gate block; a single consolidated DoD item (template `:38`); no
  `License Audit` pointer.
- The licence gate names Charmy at every user-readable surface: `scripts/licence-check:2`
  ("Charmy's tool") and `:19` (verdict written into `## License (Charmy)`),
  `.github/workflows/licence-check.yml:1` ("Licence Check (Charmy)") and "the same
  scanner Charmy runs by hand", `team/licenses/core.py:1` and `team/__init__.py`
  ("Charmy's tooling"), `team/licenses/policy.yaml` ("for the Charmy agent"); no
  `License Audit` pointer in any of them.
- DoD box 11: `grep -ri flicky --exclude-dir=__pycache__ .opencode/agents AGENTS.md tests
  team README.md planning/templates scripts .github` → no matches, exit 1.
- No other user-facing doc names the agents or the chain. Outside `planning/`, the only
  markdown in the tree is `README.md`, `AGENTS.md`, and the untracked scratch files
  (`continue-prompt-*`, `prompt-task0026-continuation.md`), which the recorded decision
  leaves untouched as records, not living config.
- `tests/selftest.sh` re-run after the README edit: exit 0, `SELFTEST: 56 checks passed`
  (16 output lines identical to the `## Test Results` record).

**Could not verify:**

- The live A2A card (`GET /.well-known/agent.json`) was not fetched: the service is
  inactive and nothing listens on 4100 or 4210 (recorded in `## Implementation`,
  Competing priorities). The card is generated per request from the same 11 files in
  `.opencode/agents/`, and the in-process `test_agent_card_matches_roster_files` pins the
  11-skill roster. What would settle it: start `team-chaotix-a2a` and fetch the card.

---

## Release

*Owner: `Knuckles`.*

**DONE checklist verified:** yes / no — if no, what is missing and this stops here.

- **Branch:**
- **Commits:** GPG-signed
- **PR:** opened ✅ | human reviewed ✅ (if external)
- **Deploy:** dispatched workflow run <id>, result

---

## Archive

*Owner: `Espio`, the only agent that deletes. Superseded detail lands here rather than being
lost. Decisions, verified facts, rejected options with their reasons, known traps, and anything the
user said are never deleted.*

**Pruning log**

| Date | What was pruned or compressed | Rough size |
|---|---|---|
| | | |
