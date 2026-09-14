# TASK-0021 — Team lesson: interactive-input test stubs fed via `$(...)` lose in-subshell state

> **Section order below is fixed.** Each agent writes to its own section and no other. `Robotnik`
> reads only `## Status` and `## Next Actions`. Do not reorder, rename, or remove sections.

- **Created:** 2026-09-08

---

## Status

*Owner: `Robotnik`. Keep this SHORT and CURRENT — it is one of only two sections the PM reads, so a
stale entry means the whole loop runs on bad information.*

**Now:** Setup complete, awaiting Amy's plan. The lesson is verified with evidence in TASK-0020
item 10: a stub that increments a counter inside a `$(...)` subshell never advanced, hanging the
re-prompt loop forever; file-based answer queueing fixed it.

**Environment / scope:**
- Files in scope: `AGENTS.md` in this repo (`metalllinux/team-chaotix`); the README only if it
  restates testing guidance
- Touches the DB schema: no
- Graphical UI: no
- Rocky Linux target: no (the lesson is about shell test harnesses in general; the change is
  team-repo documentation)

**Unknowns:** none load-bearing. The lesson's content is established in
`planning/docs/TASK-0020-quiet-hours.md` `## Implementation` item 10.

---

## Definition of Done

*Owner: `Robotnik`, and nobody else. Written **before** any work starts. Objectively checkable —
if a box cannot be verified by looking at something, rewrite it.*

- [ ] The lesson is recorded in `AGENTS.md` (Amy picks the exact home in `## Plan`; the default is
  §7 Testing strategy) and states all of: (a) a stub that feeds interactive input to a function
  that reads via `$(...)` command substitution runs in a subshell; (b) in-memory state such as
  counters or variables does not persist across calls, so a re-prompt loop can hang forever;
  (c) use file-based answer queueing or another mechanism that persists across subshells
- [ ] The wording cites the origin, the `ask_number` hang in TASK-0020 item 10
  (`planning/docs/TASK-0020-quiet-hours.md`)
- [ ] The wording follows the house style in `AGENTS.md` §10 (no em or en dashes, no colons
  introducing an explanation, no banned words)
- [ ] `Shadow`: no unresolved blockers or should-fix findings in `## Review`
- [ ] `Omega`: no unresolved findings above `low` in `## Security`
- [ ] `Big`: requested-vs-executed check count recorded; every executed check PASS (doc-only
  change; Big decides which checks are relevant and states the rest as n/a)
- [ ] `Vector`: confirms the README needs no change, or updates it if it does
- [ ] `Knuckles`: GPG-signed commit, PR to `metalllinux/team-chaotix` merged and pushed
  (in-account, no human gate)
- [ ] `Espio`: planning doc pruned

---

## Next Actions

*Owner: whoever wrote last. The future only — delete what has been done. The second of the two sections
the PM reads.*

- [ ] `Amy`: write `## Plan` (the placement decision for the lesson in `AGENTS.md`, the wording
  approach, and rollback as a single-commit revert)

---

## Plan

*Owner: `Amy`.*

**Why this task exists** — the user request or issue it serves.
**What it unblocks / what blocks it** — including dependencies outside this repo.
**MVP** — the smallest version that delivers value, and what is deferred.
**What this makes harder later.**

**Work breakdown** — decomposed until one agent finishes one item in one turn.

| # | Item | Owner agent | Acceptance criterion | Parallel with |
|---|---|---|---|---|
| 1 | | | | |

**Critical path:**
**Validation:** which files, which checks, which pages need a human look. Name them.
**Rollback:** how we detect failure, the exact revert, and where the point of no return is.

---

## Implementation

*Owner: `Tails`.*

**Alternatives considered**

### Problem: <what needed solving>
**Option A — <approach>** · How: · Pros: · Cons:
**Option B — <approach>** · How: · Pros: · Cons:
**Chosen:** , because .
**Competing priorities:** what was traded away, explicitly.

**Changes**

| File | What changed |
|---|---|
| | |

**Checks run:** compile · linter · harness

---

## Review

*Owner: `Shadow`. Read-only — findings only, no edits. Severity order, blockers first.*

### <short claim>
**Severity:** blocker | should-fix | nit
**Where:** `path/to/file:123`
**Problem:** one sentence.
**Failure scenario:** concrete inputs or state → the wrong outcome.
**Suggested direction:** what to do instead.
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

---

## Security

*Owner: `Omega`. Read-only. Severity order.*

### <short claim>
**Severity:** critical | high | medium | low
**Vector:** injection | authz | secrets | input-validation | crypto | supply-chain | actions | license
**Where:** `path/to/file:123`
**Attack:** who the attacker is, what they control, the concrete steps.
**Impact:** what they get.
**Fix:** the specific change.
**Resolution:** *(filled by `Tails`)*

---

## Test Results

*Owner: `Big`. Verdicts, never raw log dumps.*

**Workflow run:**

| Check | What it exercises | Result | Notes |
|---|---|---|---|
| compile | changed files | PASS/FAIL | |
| linter | style and correctness | PASS/FAIL | |
| unit tests | individual functions | PASS/FAIL | |
| integration tests | end-to-end flows | PASS/FAIL | |
| Sparky tests | Rocky Linux UI (if applicable) | PASS/FAIL | |

**Checks requested vs run:** N requested, N executed. *If any were dropped or skipped, say so here
explicitly — a truncated run reporting green reads as full coverage.*

**Verdict:** prose. For each FAIL: the failing check, the evidence, and whether it is a code bug (goes
to `Tails`) or a harness bug (stays with `Big`).

---

## Docs

*Owner: `Vector`.*

| File | Sections touched | What changed |
|---|---|---|
| `README.md` | | |
| `CHANGELOG.md` | | |

**Checked and needed no change:** listing these saves the next person re-checking.
**Could not verify:** what, and what would settle it.

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
