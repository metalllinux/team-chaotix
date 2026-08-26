# TASK-0010 — Fix the EVO-X2 iGPU wedge that kills llama-server (Q5) sessions

> **Section order below is fixed.** Each agent writes to its own section and no other. `Robotnik`
> reads only `## Status` and `## Next Actions`. Do not reorder, rename, or remove sections.

- **Created:** 2026-08-25

---

## Status

*Owner: `Robotnik`. Keep this SHORT and CURRENT — it is one of only two sections the PM reads, so a
stale entry means the whole loop runs on bad information.*

**Now (2026-08-26 12:50 UTC): host rebooted; Q5 no longer served; team runs Q4 only; zero
wedges since boot.** EVO-X2 uptime 1:25 at 12:50 UTC (boot ~12:25 UTC / 21:25 JST); kernel
journal shows **zero** `device wedged` events since boot (monitoring command above). `ss -ltnp`
shows only llama-server pid 1817 on 8092 (Q4, `n_ctx: 262144` per `/v1/models`); 8084 (Q5) has
no listener. The team's endpoint is Q4 only (TASK-0011, user-directed); the wedging Q5 workload
is no longer served to the team. The host reboot has **no recorded approval in this doc**
(who performed it is unverified; user action is the standing pattern for EVO-X2 ops). Tails
attempt 2 (dispatched 2026-08-25 10:25 UTC) left no completion entry in `## Next Actions`; its
checkpoints, if any, are in `## Implementation` / `## Test Results`. Consequence (corrected 2026-08-26 19:55 UTC): the `virsh list --all` here ran without
`sudo` (empty user libvirt session); the system-instance `gdm-login-vm` domain (created by
TASK-0008 attempt 5 at 14:51 UTC) has run continuously, and the libvirt host was not rebooted
(up since Aug 15) — the EVO-X2 reboot above is the model host, which is the part that matters
for this task.
TASK-0008 item 2 re-dispatched on Q4 with the existing VM and before/after wedge-count
monitoring.

**Now (2026-08-25 10:25 UTC): Tails attempt 1 dead (cancelled 10:12:57 UTC, session
`ses_fc83e6361...` "Aborted"); 16th wedge at ~10:15:25 UTC briefly errored the PM session;
endpoint is up and generating (9.44 t/s) as of 10:23 UTC. Re-dispatching Tails with a defensive
resume brief: write the first checkpoint (wedge timestamps + context) within the first few
minutes, then apply the safest runtime mitigation early to lower the wedge rate and protect the
session, then characterize the trigger.** Wedge count 15 → 16. Wedge pattern so far (needs the
trigger characterized): pairs ~30 min apart, then gaps — 18:59+19:32 UTC Aug 24, 05:54+06:25
UTC Aug 25, 10:15 UTC Aug 25. The kernel journal is EVO-X2 local time (UTC+9/JST): the 16th
wedge logged as "Aug 25 19:15:25" = 10:15:25 UTC, matching the opencode.log stream errors
10:15:27–34 UTC.

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

- [x] `Tails` (attempt 1, dispatched 2026-08-25, cancelled/killed 10:12:57 UTC): see Status;
      any checkpoints it wrote are in `## Implementation` / `## Test Results` — attempt 2
      resumes from them.
- [x] `Robotnik` (2026-08-26 12:50 UTC): recorded the host reboot (~12:25 UTC, no approval in
      this doc, provenance unverified), Q5 down (8084 no listener), team on Q4 only, zero wedges
      since boot, orphan `gdm-login-vm` dead. Endpoint-stability decision made: sufficient to
      resume TASK-0008 item 2, with wedge-count monitoring before/after (record: `## Status`).
- [ ] `Tails` (attempt 2, dispatched 2026-08-25 10:25 UTC): on EVO-X2 (`ssh
      howard@192.168.1.106`), resume from the last checkpoint (do not redo it). First action:
      pull the kernel-journal wedge timestamps with surrounding context and write that
      checkpoint to `## Implementation` within the first few minutes. Then record prior
      sysfs values and apply the safest runtime mitigation (performance level via
      `power_dpm_force_performance_level`, or a power cap if exposed) to lower the wedge rate
      and protect this session; measure the wedge count under equivalent load, keep what
      works, revert what does not. Then characterize the trigger (correlate power/
      temperature/clock against the wedge timestamps). Checkpoint to `## Implementation` and
      `## Test Results` early and often; a wedge can kill this session at any time.
- [ ] `Tails`: stage (do not execute) any restart-level or reboot-level option with exact
      commands and revert; list them under `## Implementation` → "Staged, awaiting user
      approval".
- [ ] `Robotnik`: relay staged options to the user; on approval, schedule the restart/reboot
      window (it kills in-flight opencode sessions; nothing dispatches during it).
- [ ] `Shadow` ∥ `Omega`: review the applied/staged changes once Tails checkpoints them.
- [ ] `Robotnik`: item 2 re-dispatched 2026-08-26 (TASK-0008 `## Next Actions`); after it
      completes, continue the chain: 9a (Tails, Sparrow suite), Amy (TASK-0009 plan),
      4 → 5 → 6 → Shadow → Omega → Big → 8 → 10 → (11) → 12 → 13 → 14.

---

## Plan

*Owner: `Amy`.*

Deferred (Robotnik decision 2026-08-25): urgent infrastructure task with an already-established
root cause (see Status evidence); the lightweight plan is the Next Actions sequence. If the fix
grows beyond runtime tuning into a multi-option decision (flags, kernel parameters, recovery
automation), Amy writes the full plan here before Tails executes the staged options.

---

## Implementation

*Owner: `Tails`. Checkpointed 2026-08-25 ~17:35 JST (diagnosis complete, experiment not yet started).*

### Diagnosis (completed 2026-08-25, Tails)

**Trigger characterization: sustained continuous full-power GPU load. Not thermal throttling, not OOM, not PCIe.**

Evidence base, all on EVO-X2 (`ssh howard@192.168.1.106`), host `trip`, kernel
`7.0.12-1.el10.elrepo.x86_64`, boot 0 since 2026-08-23 07:13:10 JST.

**1. Wedge events (15, all in current boot).**
Command: `journalctl -k --no-pager | grep -E "device wedged"` (count 15 at 16:13 JST, unchanged at
17:30 JST). Every event has the same shape (sample, 2026-08-25T15:25:51+09:00):

```
amdgpu 0000:c4:00.0: ring comp_1.2.0 timeout, signaled seq=12133338, emitted seq=12133340
  Process llama-server pid 26063 thread llama-server pid 26063
amdgpu 0000:c4:00.0: Starting comp_1.2.0 ring reset
amdgpu 0000:c4:00.0: reset compute queue (1:2:0)
amdgpu 0000:c4:00.0: Ring comp_1.2.0 reset succeeded
amdgpu 0000:c4:00.0: [drm] device wedged, but recovered through reset
```

All 15 are compute-ring timeouts on `comp_1.1.0` or `comp_1.2.0`, all attributed to
`llama-server`. 0 full GPU resets (`grep -c "GPU reset begin"` = 0). Recovery is ring-level.
13 additional milder hangs: `Fence fallback timer expired on ring comp_1.x.0` (3 of them within
3 min of a full wedge).

**2. What was in flight at each wedge (llama-server user journal, `journalctl --user -u
llama-server-qwen3.8-27b-q5.service`, covered back to 2026-08-22 16:17 JST).** Two signatures:

*Signature A (11/15): a single giant prefill, wedged 30.2-32.0 min into it.* Prefill progress
lines (`slot print_timing: ... prompt processing, n_tokens = N, progress = P, t = T s / X tokens
per second`) show:

| wedge (JST) | PID | tokens processed at last line | t at wedge | prefill rate | total prompt (est) |
|---|---|---|---|---|---|
| 08-24 02:45:54 | 5841 | 192512 (93%) | 1857 s | 103.7 t/s | ~207k |
| 08-24 03:17:01 | 6494 | 190464 (92%) | 1821 s | 104.6 t/s | ~207k |
| 08-24 03:47:59 | 6607 | 190464 (92%) | 1821 s | 104.6 t/s | ~207k |
| 08-24 08:18:05 | 6717 | 196608 (95%) | 1876 s | 104.8 t/s | ~207k |
| 08-24 08:18:37 | 6717 | 198656 (96%) | 1908 s | 104.1 t/s | ~207k |
| 08-24 08:50:51 | 7152 | 198656 (96%) | 1909 s | 104.0 t/s | ~207k |
| 08-24 16:49:44 | 8022 | 194560 (98%) | 1843 s | 105.6 t/s | ~199k |
| 08-24 17:20:37 | 8157 | 192512 (97%) | 1812 s | 106.3 t/s | ~198k |
| 08-25 03:59:57 | 9394 | 198656 (80%) | 1916 s | 103.7 t/s | ~248k |
| 08-25 04:32:34 | 9531 | 198656 (80%) | 1918 s | 103.6 t/s | ~248k |
| 08-25 15:25:51 | 26063 | 190464 (97%) | 1813 s | 105.1 t/s | ~196k |

The 08:18:05 -> 08:18:37 pair is the same PID 6717: the process survived the first ring reset,
kept prefilling, and wedged again 32 s later. The trigger is a function of accumulated load state,
re-triggered immediately by the same continuing load.

*Signature B (4/15): continuous high-churn request processing (GPU busy, sub-30 s gaps), wedged
during a request after >=60 min of it.* Windows 2026-08-24 16:18:02, 2026-08-24 21:18:21,
2026-08-25 03:27:13, 2026-08-25 14:54:53: 937-1102 `print_timing` lines in the prior 60 min,
last `all slots are idle` only 20-30 s before each wedge.

**3. Threshold.** Aggregating every prefill >100k tokens since boot (script
`/tmp/prefill_agg.sh` on EVO-X2): 5 completed, 10 wedged. Longest completed: 180,135 tokens at
1679 s (28.0 min, 107 t/s). Shortest wedged: 190,464 tokens at 1812 s (30.2 min, 105 t/s).
**The wedge threshold sits at ~190-199k processed prefill tokens / ~30-32 min of sustained
~105 t/s prefill.** (Last progress line is always a multiple of 2048 due to logging cadence; true
wedge point is within the next batch.)

**4. Ruled out:**
- *Thermal throttling:* `power_dpm_force_performance_level=auto`; sysfs
  `thermal_throttling_logging` is **enabled** (60 s interval) and the kernel journal has **zero**
  throttling events in 2 d 9 h across all 15 wedges (`journalctl -k | grep -icE throttl` = 0).
  Under 99%-busy load the package sits at 81.0 C edge / 119.1 W PPT (`/sys/class/hwmon/hwmon2/`),
  i.e. far below any trip point.
- *OOM:* 0 in kernel journal.
- *PCIe/AER:* 0 real errors (only boot-time PME/pciehp noise).
- *Clock state:* `pp_dpm_sclk` states 600/2896/2900 MHz, running 2896 MHz (state 1 of 3) under
  load; `pp_dpm_mclk` 1000 MHz (max); `pp_dpm_socclk` 600-1472 MHz. No stuck low-clock state.

**5. Live power/temp/clock at wedge time was never recorded** (no sensor logger was running).
This is the gap the baseline reproduction below closes: a controlled ~200k-token prefill (the
exact Signature A trigger) with 5 s sensor sampling, so power/temperature/clock can be read at
the wedge moment for the first time.

**6. Count discrepancy note:** the fixes doc (2026-08-25) cites "26 wedge events"; the monitoring
command counts 15, all in boot 0, and the archived journal (boots back to 2026-06-16) contains no
older `device wedged` lines. The 26 appears to be a double count (2 lines per event matched);
15 is authoritative per the monitoring command.

**7. Unrelated separate failure mode (not a wedge, no action in this task):** 2026-08-25
09:19:29-09:20:04 JST, five consecutive `llama-server` segfaults in `libllama.so.0.0.9671`
(null-deref at ip+0xd0770) ~8 s apart = crash loop while the service was being restarted around
the user's 10:04 JST unit restore. CPU-side, did not recur. Flagged for the record.

### Alternatives considered

**Problem: how to characterize the trigger and find a durable runtime fix without restarting
llama-server or rebooting.**

**Option A - Historical sensor correlation only.** Read past power/temp/clock at wedge times from
logs. How: journal + any sensor logger. Pros: no load needed. Cons: **no sensor logger was
running; no historical sensor data exists.** Dead end as the primary method.
**Option B - Controlled reproduction with live sampling.** Run the exact Signature A trigger
(~200k-token prefill) in the background while sampling sysfs sensors every 5 s and tracking the
wedge count; capture power/temp/clock at the wedge moment; then repeat under each candidate
mitigation and compare. Pros: direct evidence at the failure point; doubles as the "equivalent
llama-server load" measurement the task requires; each run is a normal (extreme) endpoint use, no
restart or reboot involved. Cons: takes ~30 min per run at current clocks; a wedge during a run
kills llama-server for the restart window (~15-30 s measured: 15:25:51 wedge -> 15:26:03 new
slot) and any in-flight request; risk of killing this opencode session if a wedge hits mid-token.
**Chosen: B**, because A has no data and the task explicitly requires measuring wedge count under
equivalent load. The reproduction is staged so the session survives a mid-run wedge: the prefill
runs in a background process on EVO-X2, results land in files on EVO-X2 and in this doc, and the
session's own checkpoint is written before the run starts.

**Competing priorities:** endpoint availability during the ~30 min test windows (other queued
requests wait behind the test prefill on the single slot) was traded for definitive trigger data
and mitigation A/B evidence. The frozen llama-server flags are untouched by the test; only a
prompt is sent through the existing service.

### Prior sysfs state (recorded 2026-08-25 ~17:30 JST, before any change)

| File | Value |
|---|---|
| `/sys/class/drm/card0/device/power_dpm_force_performance_level` | `auto` |
| `power_dpm_state` | `performance` (under 99% busy load) |
| `pp_cur_state` | `0` |
| `pp_dpm_sclk` | states `600 / 2896* / 2900` MHz (current 2896) |
| `pp_dpm_mclk` | states `400 / 800 / 1000*` MHz |
| `pp_dpm_fclk` | states 400..2000 MHz (8 states) |
| `pp_dpm_socclk` | states 600..1472 MHz (8 states) |
| `pp_od_clk_voltage` | (present, rw; not yet read in full) |
| `thermal_throttling_logging` | enabled, 60 s interval (leave as is) |
| `tuned` profile | `throughput-performance` |
| kernel cmdline (GPU-relevant) | `amd_iommu=off amdgpu.gttsize=90112 ttm.pages_limit=23068672 ttm.page_pool_size=23068672 amdgpu.no_system_mem_limit=1` |
| hwmon writable power cap | **none** (no `power1_crit`/`power1_max`; `stapm_power_limit` null in `amdgpu_top`) |

Writable mitigation surface: `power_dpm_force_performance_level` (auto/low/medium/high/manual),
`pp_dpm_sclk`/`pp_dpm_mclk` (clock states, manual mode), `pp_od_clk_voltage` (over/undervolt).

### Experiment plan (in progress)

1. **Baseline reproduction** (~30 min): background `bash /tmp/wedge_repro.sh baseline` on EVO-X2
   samples `gpu_busy_percent`, `temp1_input`, `power1_input`, `freq1_input` every 5 s to
   `/tmp/gpu_samples_baseline.csv`, polls the `device wedged` journal count each tick, then
   POSTs a ~200k-token prompt to `http://127.0.0.1:8084/completion` (n_predict=1). Expected:
   wedge at ~30 min, sensors captured through the failure.
2. **Mitigation 1** (~30-45 min): apply one sysfs change (leading candidate: cap `pp_dpm_sclk`
   to ~2500 MHz via `power_dpm_force_performance_level=manual`, since no power cap exists and the
   trigger is sustained power/clock at the 2896 MHz ceiling), record prior values, repeat the
   identical prefill, compare wedge outcome + power/temp profile. Keep if it works, revert if not.
3. Further mitigations only if #2 fails, one at a time.
4. Staged (not executed) restart/reboot-level options under "Staged, awaiting user approval".

**Status at checkpoint: baseline run STARTED 2026-08-25 ~18:40 JST** (`/tmp/wedge_repro.sh baseline`,
sampler PID in `/tmp/sampler_pid_baseline`, results in `/tmp/gpu_samples_baseline.csv`,
`/tmp/repro_end_baseline.txt`, `/tmp/prefill_result_baseline.json`). Prompt payload 951,423 chars
(~220-250k tokens est); total prompt size verifiable from the first `prompt processing` progress
line (total = 4096/progress). If total < 190k: kill curl + sampler (`kill $(cat
/tmp/sampler_pid_baseline)`), regenerate bigger, restart. Expected wedge ~30 min after prefill
start; sensor rows around the wedge epoch are the key artifact. A wedge during the run kills any
in-flight endpoint request (accepted risk, see Alternatives considered).

### Staged, awaiting user approval

*(none yet - being written after the baseline + mitigation runs; nothing above requires a restart
or reboot)*

### Changes

| File | What changed |
|---|---|
| EVO-X2 sysfs | **no changes yet** (read-only so far) |
| `/tmp/wedge_profile.sh`, `/tmp/prefill_agg.sh`, `/tmp/busy_run.sh` (EVO-X2) | diagnosis scripts (read-only journal access) |
| `planning/docs/TASK-0010-evox2-gpu-wedge-fix.md` | this section + Test Results checkpoint |

### Checks run

- `journalctl -k | grep -cE "device wedged"` = 15 (stable 16:13 -> 17:30 JST)
- `journalctl -k | grep -icE "throttl"` = 0 with throttling logging enabled
- `journalctl -k | grep -icE "AER|pcieport|PCIe Bus Error|..."` = 11, all boot-time PME/pciehp noise
- `journalctl -k | grep -c -iE "out of memory|oom-kill"` = 0
- `amdgpu_top -J` decode of `gpu_metrics` (rev 3, 264 B) matches sysfs: socket power 119.05 W at 99%
  busy vs 11-47 W in inter-token gaps; no `Throttle Status` field in v3 metrics, `stapm_power_limit` null

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

*Owner: `Big`. Verdicts, never raw log dumps. Note: `Tails` records raw before/after measurement
data here per the 2026-08-25 dispatch instruction ("checkpoint findings to ## Implementation and
## Test Results early and often"); `Big` converts to verdicts at review time.*

**Measurement record (Tails, 2026-08-25):**

| # | Check | What it exercises | Result | Notes |
|---|---|---|---|---|
| 1 | Wedge count baseline | `journalctl -k --no-pager \| grep -cE "device wedged"` on EVO-X2 | 15 (16:13 JST), 15 (17:30 JST) | all in boot 0 (since 2026-08-23 07:13:10 JST); no wedges in archived boots back to 2026-06-16 |
| 2 | Thermal throttling evidence | kernel journal throttling events while `thermal_throttling_logging` enabled (60 s) | 0 events in 2 d 9 h | logging confirmed enabled via sysfs status string; rules out thermal throttling as trigger |
| 3 | Load profile at wedges | llama-server user journal, last in-flight work per wedge | 11/15 wedges mid-prefill at 30.2-32.0 min (190,464-198,656 tokens processed, ~104-106 t/s); 4/15 after >=60 min continuous high-churn | threshold: 180,135 tokens/1679 s completed OK, 190,464/1812 s wedged |
| 4 | OOM / PCIe / full-reset scan | kernel journal greps | 0 OOM, 0 real PCIe/AER, 0 full GPU resets | 13 milder "Fence fallback timer expired" hangs; 5 llama-server segfaults 2026-08-25 09:19 (separate, CPU-side) |
| 5 | Live sensor baseline (99% busy, this session's load) | hwmon2 + gpu_busy_percent + amdgpu_top JSON | 81.0 C edge, 119.1 W PPT, sclk 2896 MHz, mclk 1000 MHz | idle gaps: 11-47 W, 54-55 C gfx |

**Checks requested vs run:** 4 requested by dispatch (trigger characterization, mitigation
before/after under equivalent load, baseline count + monitoring command, fixes-doc update). 3
executed so far (rows 1-5 cover rows 1+3+4 of the request); **mitigation before/after under
equivalent load NOT yet executed** (baseline reproduction staged, start pending) and the fixes-doc
update is pending. No checks silently dropped.

**Verdict:** diagnosis complete: trigger is sustained continuous full-power load (see
Implementation). No mitigation applied yet; endpoint unchanged; frozen flags intact.

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
