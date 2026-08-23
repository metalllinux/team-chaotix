# TASK-0009 — Standardize desktop application testing on Sparky + pyatspi2

> **Section order below is fixed.** Each agent writes to its own section and no other. `Robotnik`
> reads only `## Status` and `## Next Actions`. Do not reorder, rename, or remove sections.

- **Created:** 2026-08-21

---

## Status

*Owner: `Robotnik`. Keep this SHORT and CURRENT — it is one of only two sections the PM reads, so a
stale entry means the whole loop runs on bad information.*

**Now:** The 2026-08-22 `Amy` dispatch for `## Plan` died with the rest of that fan-out (all
five subagents hit the 64k context wall on Q5; record: TASK-0008 `## Status`). `## Plan` is still
an empty stub. Q5 now serves 1 slot x 262144 alongside Q6 (PM session on Q6); Amy dispatches as a
single subagent immediately after the user's Q6 decision (TASK-0008 Next Actions). User directive
(2026-08-21): for any desktop application testing, the team uses Sparky + pyatspi2
(https://gitlab.gnome.org/GNOME/pyatspi2). The deliverable is the updated team configuration in
`metalllinux/team-chaotix` (this repo), pushed to main.

**Model note (user, 2026-08-22):** the team model is `Qwen3.8-27B-UD-Q5_K_XL`; the re-target
landed (`2fe0c8b`), so Tails' scope here stays section 7 + big.md. The Q5 endpoint serves the
full 262144 context (verified 2026-08-23 after the fit-degradation fix; record: TASK-0008 `##
Status`).

**Environment / scope:**
- Files in scope: `AGENTS.md` (section 7, testing strategy), `.opencode/agents/big.md`, `README.md`,
  `.github/actions/sparky-test-runner/` (if affected), plus any other team config that names the
  desktop testing stack (workflows, docs)
- Touches the DB schema: no
- Graphical UI: no (this task configures the team; it governs UI testing)
- Rocky Linux target: yes (the standard concerns UI testing on Rocky Linux)

**Constraint (2026-08-22, from the TASK-0008 incident):** a 5-way subagent fan-out on a
1-slot endpoint killed all five sessions overnight (record: TASK-0008 `## Status`). The AGENTS.md
update for this task should record the concurrency ceiling, and it must reflect the hardware fit,
not just the endpoint: Q5 serves 1 slot x 262144 while Q6 runs and 3 slots x 262144 with Q6
retired (92GB unified memory; record: TASK-0008 `## Status`), so future plans do not
over-fan-out.

**Unknowns:**
- Where pyatspi2 (Python) sits relative to Sparky's Raku/Sparrow tasks: a Python driver invoked from
  tasks, or a separate layer. Must be decided against the Sparky source, not assumed.
- Whether the GDM greeter exposes an a11y bus at all. TASK-0008 item 3 will produce evidence; until
  then the standard needs a documented carve-out for raw-input drivers (e.g. xdotool) on surfaces
  where a11y is unavailable.
- How pyatspi2 is installed in test VMs (package name and availability on Rocky Linux 10, or a
  source build). Must be verified on the host or in a VM, not guessed.

---

## Definition of Done

*Owner: `Robotnik`, and nobody else. Written **before** any work starts. Objectively checkable —
if a box cannot be verified by looking at something, rewrite it.*

- [ ] `AGENTS.md` section 7 states the standard: desktop application testing uses Sparky +
      pyatspi2, with the pyatspi2 URL, how pyatspi2 drives UI inside the Sparky/Sparrow setup, and
      the documented carve-out for raw-input drivers on surfaces where a11y is unavailable.
- [ ] `Big`'s agent definition (`.opencode/agents/big.md`) names the same standard, so future test
      strategy decisions default to Sparky + pyatspi2 for desktop UI.
- [ ] Every other file that names the desktop testing stack is updated as affected, or listed in
      `## Docs` as "checked and needed no change" (candidates: `README.md`,
      `.github/actions/sparky-test-runner/`, workflows that provision UI-test VMs).
- [ ] The pyatspi2 install method for test VMs is verified (package or source, on the actual Rocky
      Linux 10 environment) and recorded in `## Test Results` with the command and output.
- [ ] `Shadow`: no unresolved blockers or should-fix findings in `## Review`.
- [ ] `Omega`: no unresolved findings above `low` in `## Security`.
- [ ] `Vector`: `README.md` updated as affected.
- [ ] `Knuckles`: committed and pushed to `metalllinux/team-chaotix` main (internal repo, standing
      permission, no human review required); `## Release` filled.

---

## Next Actions

*Owner: whoever wrote last. The future only — delete what has been done. The second of the two sections
the PM reads.*

- [x] `Robotnik` (2026-08-22, corrected 2026-08-23): Q5 endpoint verified up; that verification
      missed the fit-to-device context degradation, now root-caused and fixed (record:
      TASK-0008 `## Status`).
- [ ] `Robotnik`: dispatch `Amy` for `## Plan` (the 2026-08-22 dispatch died; brief unchanged:
      exact file list, pyatspi2 integration approach against the Sparky source, validation,
      rollback, and the AGENTS.md concurrency-ceiling note including the hardware fit). Then
      `Tails`, then `Shadow` ∥ `Omega` (then `Big`), then `Vector`, then `Knuckles`. Sequencing
      with TASK-0008 Wave 0 follows the Q6 decision (TASK-0008 Next Actions).

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
