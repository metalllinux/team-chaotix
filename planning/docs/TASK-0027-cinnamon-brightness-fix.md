# TASK-0027 — Cinnamon brightness: Settings and keyboard shortcuts have no effect

> **Section order below is fixed.** Each agent writes to its own section and no other. `Robotnik`
> reads only `## Status` and `## Next Actions`. Do not reorder, rename, or remove sections.

- **Created:** 2026-10-01

---

## Status

### 2026-10-04: target machine identified; environment rebuilt by operator

Operator request: continue the brightness work. The old test machine (`cinnamon-1`) is gone. New environment (details in planning/docs/TASK-0033-cinnamon-project-environment.md): `Rocky_Linux_10_Cinnamon` (192.168.122.4) on `qemu:///system` is the diagnosis target (the operator's brightness report referred to a machine with the team's Cinnamon RPMs; the package inventory is pending in TASK-0033); `Fedora_45_Cinnamon` (192.168.122.176) is the comparison machine. Being a VM, the target has no physical backlight — the environment-limitation classification in the DoD is likely, but the port-bug path (settings plugin, keybindings, settings-daemon wiring) must still be established per the DoD. Login: `howard`, password at `~/AI/secrets/pass.txt`. Note: every virsh command on this host must pass `-c qemu:///system` (the default URI resolves to the empty `qemu:///session`).

**Now:** Operator-reported bug on the test Cinnamon + Rocky Linux 10 machine: brightness cannot be
changed via Cinnamon Settings (Display/Power pane) or via the keyboard shortcuts. Diagnosis not
started.

**Environment / scope:**
- Files in scope: the Cinnamon packages in the repo (cinnamon-settings-daemon, control center, keybindings); the test machine to be identified
- Touches the DB schema: no
- Graphical UI: yes (Sparky testing may be required)
- Rocky Linux target: yes

**Unknowns:**
- Which machine the operator tested: the `cinnamon-1` VM (no physical backlight) or a physical machine.
- Whether a backlight is present (backlight sysfs, `brightnessctl`) and which brightness backend Cinnamon uses on it.
- Whether cinnamon-settings-daemon is running and whether its brightness plugin is active.
- Whether the brightness keyboard shortcuts are bound (cinnamon-keybindings / gsettings).

---

## Definition of Done

- [ ] Target machine identified and its brightness hardware state recorded with evidence (backlight sysfs, `brightnessctl` output, `lspci` display info).
- [ ] Root cause established in `## Implementation` with command + output evidence: why Cinnamon Settings and the keyboard shortcuts do not change brightness.
- [ ] Classification recorded: environment limitation (no backlight hardware, e.g. a VM) versus Cinnamon port bug (missing package, daemon plugin, unbound shortcut).
- [ ] If port bug: fix in the Cinnamon package, rebuilt, installed on the target machine, and brightness verified working through both Cinnamon Settings and the keyboard shortcuts with before/after evidence.
- [ ] If environment limitation: documented in `## Test Results` with what would make it testable (hardware with a real display).
- [ ] `## Test Results` updated with the final verdict.

---

## Next Actions

- [ ] `Amy`: plan the diagnosis on `Rocky_Linux_10_Cinnamon` (machine identified; see ## Status): probe the brightness stack (backlight sysfs, `brightnessctl`, settings-daemon plugin state, keybindings via gsettings), classify per the DoD, and define the fix path. Use TASK-0033's package inventory for versions. `Fedora_45_Cinnamon` is the comparison machine.

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
