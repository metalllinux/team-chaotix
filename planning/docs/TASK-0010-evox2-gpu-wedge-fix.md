# TASK-0010 — Fix the EVO-X2 iGPU wedge that kills llama-server (Q5) sessions

> **Section order below is fixed.** Each agent writes to its own section and no other. `Robotnik`
> reads only `## Status` and `## Next Actions`. Do not reorder, rename, or remove sections.

- **Created:** 2026-08-25

---

## Status

*Owner: `Robotnik`. Keep this SHORT and CURRENT — it is one of only two sections the PM reads, so a
stale entry means the whole loop runs on bad information.*

**Now (2026-08-25): new urgent task, user-directed. Tails dispatched for item 1 (diagnose +
runtime mitigation).** The Strix Halo iGPU (Radeon 8060S, gfx1151) on EVO-X2 (192.168.1.106)
wedged twice during TASK-0008 item 2 attempt 4 (wedge count 13 → 15; attempt dispatched ~05:54
UTC, stream errors 05:55 UTC, session cancelled 06:29 UTC). Each amdgpu compute-ring reset kills
the Vulkan device, crashes llama-server, and the multi-minute model reload kills in-flight
opencode subagent sessions (no stream retry). The user ordered the wedge fixed now
(2026-08-25); this supersedes the 2026-08-25 config freeze ("wedge risk accepted, no unit
changes") for the purpose of finding a durable fix. The frozen llama-server flags (`-fa on`,
q8_0 KV, `-c 262144`, `--parallel 1`) stay intact unless the user approves a change.

**Evidence so far (Robotnik, read-only, 2026-08-25):**
- Root cause and config history: `/home/howard/AI/projects/qwen-38-q5-fixes/qwen38-q5-fixes.md`
  (2026-08-25 section). 26 wedge events since the 2026-08-23 boot at that writing; `-fa off` is
  not a valid mitigation (q8_0 V-cache quantization requires flash_attn).
- GPU baseline: `power_dpm_force_performance_level=auto`; `pp_dpm_sclk` states
  600/2656/2900 MHz, current 2656 MHz; kernel `7.0.12-1.el10.elrepo.x86_64`; llama-server running
  (service `llama-server-qwen3.8-27b-q5.service` active).
- Monitoring command: `ssh howard@192.168.1.106 'journalctl -k --no-pager | grep -cE
  "device wedged"'` (count 15 at dispatch time).

**Critical constraint:** EVO-X2 serves the Q5 endpoint that this team (including `Robotnik` and
any dispatched subagent) runs on. A llama-server restart or host reboot kills in-flight opencode
sessions. Read-only diagnosis and reversible runtime (sysfs) tuning may proceed; anything that
requires a restart or reboot must be staged, not executed, and escalated to the user for
approval before it runs.

**Environment / scope:**
- Files in scope: EVO-X2 sysfs (`/sys/class/drm/card0/device/`), the llama-server systemd unit
  (only with user approval), kernel boot parameters (only with user approval), the fixes doc
  `/home/howard/AI/projects/qwen-38-q5-fixes/qwen38-q5-fixes.md`. No metalllinux repo code.
- Touches the DB schema: no
- Graphical UI: no
- Rocky Linux target: no (EVO-X2 is the model-host infrastructure, not the project under test)

**Unknowns:**
- What drives the wedge: sustained compute load, thermal, or power. Needs sensor/power readings
  correlated against wedge timestamps.
- Whether runtime power/frequency capping is even exposed for this chip (Strix Halo sysfs
  power-limit support unverified).
- Whether an effective fix requires a restart-level (llama-server flags) or reboot-level (kernel
  parameters) change, and whether the user accepts the resulting downtime.

---

## Definition of Done

*Owner: `Robotnik`, and nobody else. Written **before** any work starts. Objectively checkable —
if a box cannot be verified by looking at something, rewrite it.*

- [ ] The wedge trigger is characterized with evidence (sustained load vs thermal vs power):
      wedge timestamps from the EVO-X2 kernel journal correlated with GPU power/temperature/
      utilization readings, recorded in `## Implementation` with the commands and outputs.
- [ ] At least one runtime (no-restart) mitigation is tried: before/after wedge counts under
      equivalent load are measured and recorded in `## Test Results`. If it works, the setting
      is made to survive reboot (persistent) or the manual re-apply step is documented in the
      fixes doc.
- [ ] The user-frozen llama-server configuration (`-fa on`, q8_0 KV, `-c 262144`,
      `--parallel 1`) is unchanged, or any change has explicit user approval recorded in
      `## Status`.
- [ ] Every change that requires a llama-server restart or host reboot is staged (exact files,
      commands, and revert written into this doc) and NOT executed; user approval is recorded in
      `## Status` before any such change runs.
- [ ] Every modified unit or sysfs setting has its prior state backed up (standing rule:
      `cp <unit> /tmp/<unit>.bakN.$(date +%s)` for units; prior sysfs values recorded in the
      doc), with the backup location recorded.
- [ ] A new wedge baseline count plus the monitoring command are recorded in this doc, and
      `/home/howard/AI/projects/qwen-38-q5-fixes/qwen38-q5-fixes.md` is updated with the fix
      (what was tried, what worked, what remains).
- [ ] `Shadow`: no unresolved blockers or should-fix findings in `## Review`.
- [ ] `Omega`: no unresolved findings above `low` in `## Security`.

---

## Next Actions

*Owner: whoever wrote last. The future only — delete what has been done. The second of the two sections
the PM reads.*

- [ ] `Tails` (dispatched 2026-08-25): on EVO-X2 (`ssh howard@192.168.1.106`), item 1 diagnose:
      pull wedge timestamps from the kernel journal with surrounding context (what was running,
      what preceded each wedge), read GPU power/temperature/clock state and the amdgpu sysfs
      surface, characterize the trigger. Then item 2: try runtime mitigations (record prior
      values first, apply one at a time, measure wedge count under equivalent llama-server
      load, keep what works, revert what does not). Checkpoint to `## Implementation` and
      `## Test Results` early and often; a wedge can kill this session at any time.
- [ ] `Tails`: stage (do not execute) any restart-level or reboot-level option with exact
      commands and revert; list them under `## Implementation` → "Staged, awaiting user
      approval".
- [ ] `Robotnik`: relay staged options to the user; on approval, schedule the restart/reboot
      window (it kills in-flight opencode sessions; nothing dispatches during it).
- [ ] `Shadow` ∥ `Omega`: review the applied/staged changes once Tails checkpoints them.
- [ ] `Robotnik`: when the endpoint is stable (measurably lower wedge rate), resume the
      TASK-0008 critical path: re-dispatch item 2 with the same resume brief (orphan
      `gdm-login-vm` adoption), then 9a, Amy (TASK-0009), 4 → 5 → 6 → Shadow ∥ Omega → Big →
      8 → 10 → (11) → 12 → 13 → 14.

---

## Plan

*Owner: `Amy`.*

Deferred (Robotnik decision 2026-08-25): urgent infrastructure task with an already-established
root cause (see Status evidence); the lightweight plan is the Next Actions sequence. If the fix
grows beyond runtime tuning into a multi-option decision (flags, kernel parameters, recovery
automation), Amy writes the full plan here before Tails executes the staged options.

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
| | | | |

**Checks requested vs run:** N requested, N executed. *If any were dropped or skipped, say so here
explicitly — a truncated run reporting green reads as full coverage.*

**Verdict:** prose.

---

## Docs

*Owner: `Vector`.*

| File | Sections touched | What changed |
|---|---|---|
| | | |

**Checked and needed no change:** listing these saves the next person re-checking.
**Could not verify:** what, and what would settle it.

---

## Release

*Owner: `Knuckles`.*

**DONE checklist verified:** yes / no — if no, what is missing and this stops here.

- **Branch:** n/a (no metalllinux repo artifact; fix lives on EVO-X2 + the fixes doc)
- **Commits:** n/a
- **PR:** n/a
- **Deploy:** n/a (changes applied directly on EVO-X2 under user approval; record here)

---

## Archive

*Owner: `Espio`, the only agent that deletes. Superseded detail lands here rather than being
lost. Decisions, verified facts, rejected options with their reasons, known traps, and anything the
user said are never deleted.*

**Pruning log**

| Date | What was pruned or compressed | Rough size |
|---|---|---|
| | | |
