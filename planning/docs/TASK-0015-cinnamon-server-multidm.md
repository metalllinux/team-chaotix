# TASK-0015 — Cinnamon RPMs: minimal-server install + LightDM/SDDM session support and test matrix

> **Section order below is fixed.** Each agent writes to its own section and no other. `Robotnik`
> reads only `## Status` and `## Next Actions`. Do not reorder, rename, or remove sections.

- **Created:** 2026-08-30

---

## Status

*Owner: `Robotnik`. Keep this SHORT and CURRENT — it is one of only two sections the PM reads, so a
stale entry means the whole loop runs on bad information.*

**Now (2026-08-30): task created from the user's request; waiting on the TASK-0008 merge before
work starts.** User wants: (1) the Cinnamon RPMs to install cleanly on a minimal Rocky Linux 10
"server" system with **no login manager and no windowing system at all**, with tests built around
that scenario; (2) support for other display managers (LightDM, SDDM — the one KDE uses) with
tests for each. New scope of the 2026-08-30 user request, alongside the TASK-0008 branch merge to
main.

**Environment / scope:**
- Files in scope: clone `~/Linux/projects/cinnamon-for-rocky10/` — `vm-test/` harness,
  `tasks/lib/`, the RPM spec files (exact paths to be confirmed by `Amy`), `INSTALL.md`,
  `README.md`, the DNF repo build.
- Touches the DB schema: no (not a DB project)
- Graphical UI: yes — display-manager greeters and the Cinnamon session; VM-based testing required
- Rocky Linux target: yes (Rocky Linux 10.2, self-hosted libvirt VMs per AGENTS.md §7)

**Bare-metal real-hardware target (2026-08-30):** `howard@192.168.1.103` is the user's Rocky
10.2 minimal-server machine (ssh port open from the PM host; password in `~/pass.txt` on the
PM host — read there, never write it anywhere; sudo passwordless on the machine). Its recorded
baseline state (no DM, no windowing system) and the RPM install test run under the TASK-0008
chain count as **real-hardware evidence** for DoD boxes 2–4 (server install, no DM pulled in,
session entries present). The LightDM/SDDM matrix still runs in VMs for clean reproducible
re-runs; the bare-metal machine is a real-hardware spot check where its state allows (it ends
the TASK-0008 chain with Cinnamon + GDM installed).

**Unknowns:**
- Whether `lightdm` and `sddm` exist in the Rocky Linux 10.2 repos at all. The 2c-1 precedent
  (TASK-0008) proved Xorg absent by in-guest evidence and the plan's premise was wrong; availability
  here must be verified the same way, never assumed. If a DM is absent, the plan records a re-scope
  with the evidence.
- Whether the current Cinnamon spec force-pulls a display manager or X server as a hard dependency.
  The minimal-server install test decides; if so, the spec needs a fix (Recommends/optional), a
  rebuild, and a DNF repo regeneration.
- Where the current spec installs the session entries (`cinnamon.desktop`,
  `cinnamon-wayland.desktop`) and whether both are installed.
- Whether the existing GDM harness (`vm-test/test-gdm-login.sh` + `tasks/lib/`) can be generalized
  to drive the LightDM and SDDM greeters, or whether per-DM drivers are needed (a11y trees differ
  per greeter).

---

## Definition of Done

*Owner: `Robotnik`, and nobody else. Written **before** any work starts. Objectively checkable —
if a box cannot be verified by looking at something, rewrite it.*

- [ ] `lightdm` and `sddm` availability in the Rocky Linux 10.2 repos established with repo
      evidence (`dnf` query on a minimal guest, repo name + package version), or a re-scope
      decision recorded in `## Status` with that evidence.
- [ ] **Server-install test:** a fresh minimal Rocky Linux 10.2 VM (no display manager, no X
      server, no desktop packages) installs the documented Cinnamon RPM set from the local DNF
      repo with zero unresolved dependencies; command evidence in `## Test Results`.
- [ ] After the server install, no display manager is installed or enabled (`rpm -qa` shows no
      gdm/lightdm/sddm; `systemctl list-unit-files` shows no DM unit) and the system still works
      as a server (ssh in, `dnf` functional).
- [ ] After the server install, the Cinnamon session entries exist in the standard
      xsessions/wayland-sessions directories (paths listed with evidence).
- [ ] On that same server VM, installing + enabling GDM afterwards yields a Cinnamon (Wayland)
      login via the GDM harness: PASS, evidence in `## Test Results`.
- [ ] **LightDM test** (if available per box 1): fresh VM, `lightdm` installed + enabled; the
      Cinnamon session is listed at the greeter and a login succeeds: PASS, evidence in
      `## Test Results`.
- [ ] **SDDM test** (if available per box 1): fresh VM, `sddm` installed + enabled; the Cinnamon
      session is listed at the greeter and a login succeeds: PASS, evidence in `## Test Results`.
- [ ] All new scenarios are part of the repo's `vm-test/` matrix with named entrypoints, and
      `## Test Results` shows requested-vs-run counts with no silently dropped checks.
- [ ] If the server-install or DM tests expose spec defects (forced DM/X deps, missing session
      files), the spec is fixed, the RPMs rebuilt, and the DNF repo regenerated before the
      re-run passes.
- [ ] `INSTALL.md` documents the minimal-server install and the supported display managers;
      `README.md` reflects it.
- [ ] `Shadow`: no unresolved blockers or should-fix findings in `## Review`.
- [ ] `Omega`: no unresolved findings above `low` in `## Security`.
- [ ] `Big`: all harness checks PASS, with no silently dropped checks.
- [ ] Merged to `metalllinux/cinnamon-for-rocky10` main via PR by `Knuckles`.

---

## Next Actions

*Owner: whoever wrote last. The future only — delete what has been done. The second of the two sections
the PM reads.*

- [ ] `Robotnik`: after TASK-0008's branch is merged to main, create the work branch here from
      the updated main and dispatch `Amy`.
- [ ] `Amy`: write `## Plan` — verify DM package availability in Rocky 10.2 with evidence (no
      assumptions, the 2c-1 lesson), the spec-dependency question, harness generalization vs
      per-DM drivers, the VM matrix shape and per-VM time budget, rollback. Read this doc's
      `## Status`, `## Definition of Done`, and `## Next Actions` plus the repo files it names;
      do not read other planning docs in full.

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
lost. Decisions, verified facts, rejected options with their reasons, known traps, and anything
the user said are never deleted.*

**Pruning log**

| Date | What was pruned or compressed | Rough size |
|---|---|---|
| | | |
