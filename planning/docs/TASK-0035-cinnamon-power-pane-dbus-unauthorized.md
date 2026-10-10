# TASK-0035 — Cinnamon Control Center Power pane: D-Bus Unauthorized (36) traceback at cs_power.py:883

> **Section order below is fixed.** Each agent writes to its own section and no other. `Robotnik`
> reads only `## Status` and `## Next Actions`. Do not reorder, rename, or remove sections.

- **Created:** 2026-10-10

---

## Status

*Owner: `Robotnik`. Keep this SHORT and CURRENT — it is one of only two sections the PM reads, so a
stale entry means the whole loop runs on bad information.*

### 2026-10-10: intake — Power pane D-Bus `Unauthorized (36)` error split out of the TASK-0034/TASK-0026 Big gate findings

Source: planning/docs/TASK-0034-cinnamon-shell-no-render.md `## Test Results`, dated Big entry 2026-10-08 ("### 2026-10-08: Big — 12-pane screenshot gate"), and planning/docs/TASK-0026-cinnamon-control-center-comparison.md `## Test Results`, dated Big entry 2026-10-08. Machine: `Rocky_Linux_10_Cinnamon` (192.168.122.4), session 2 (wayland/gdm-password, seat0/tty2). Defect: launching the Power pane (`power` module → `cs_power.py`) of `cinnamon-settings` emits a traceback at `cs_power.py:883 on_my_value_changed`, D-Bus `Unauthorized (36)`; the process survived through the pane and was killed by the recorded pid; the other 11 of 12 panes are clean (ERR_LINES=0, stderr empty). It was not routed to Tails as a blocker during the gate; recorded for the review chain. PM decision (recorded in the TASK-0026 `## Status` 2026-10-10 entry): open as a new task after the TASK-0026 item 4 review chain. TASK-0026 DoD box 2 ("All panes ... load without console errors") stays open on this task's verdict. Login: `howard`, password at `~/AI/secrets/pass.txt` (never written to any file). Every virsh command passes `-c qemu:///system`.

**Now:** diagnosis not started; next is `Amy`'s plan.

**Environment / scope:**
- Files in scope: VM session state on `Rocky_Linux_10_Cinnamon` first; `Fedora_45_Cinnamon` for reproduction; `cinnamon-control-center` source in the canonical checkout (~/Linux/projects/cinnamon-for-rocky10) only if a port bug is found
- Touches the DB schema: no
- Graphical UI: no (console/stderr evidence only; the no-render limitation applies, so screenshot-level verification is impossible)
- Rocky Linux target: yes

**Unknowns:**
- Whether the error reproduces on `Fedora_45_Cinnamon` (evidence in the two source docs; check before planning).
- Which D-Bus interface/method `cs_power.py:883` (`on_my_value_changed`) calls, and why the reply is `Unauthorized (36)` (interface policy, method rules, or missing service).
- Whether Power pane functionality is degraded despite the surviving process.

---

## Definition of Done

- [ ] Root cause established with command + output evidence: what `cs_power.py:883` (`on_my_value_changed`) is calling, and why the D-Bus call returns `Unauthorized (36)` on `Rocky_Linux_10_Cinnamon` (interface, method, policy/permission path).
- [ ] Reproduction established on `Fedora_45_Cinnamon` (reproduces or does not, with evidence).
- [ ] Classification recorded: Cinnamon port bug versus upstream behavior versus VM session/environment configuration, with evidence.
- [ ] If fixable in this environment: fix in the canonical checkout plus process-level verification (Power pane of `cinnamon-settings` launches with no D-Bus `Unauthorized` traceback, app survives, killed by recorded pid). Screenshot-level verification is not possible pending the no-render limitation (TASK-0026/TASK-0034).
- [ ] `## Test Results` updated with the final verdict.

---

## Next Actions

- [ ] `Amy`: plan the diagnosis (root cause of the D-Bus `Unauthorized (36)` error, reproduction on `Fedora_45_Cinnamon`, classification, and the fix path if a port bug). Read only the two dated source entries named in `## Status`, not the whole docs.

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

## License (Charmy)

*Owner: `Charmy`. Fourth in the review chain. Every license is verified at the upstream source
repository and the ref used, never from a copy in this repo.*

**Project license:** <license> — appropriate | finding

**Imported code**

| Component | Source (repo @ ref) | License (verified at) | Obligations met | Status |
|---|---|---|---|---|
| | | | yes/no + what | pass/finding |

**Verdict:** pass | findings *(Tails fixes; the chain re-runs until clean)*

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
