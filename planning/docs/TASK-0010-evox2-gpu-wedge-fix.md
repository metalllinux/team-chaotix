# TASK-0010 — Fix the EVO-X2 iGPU wedge that kills llama-server (Q5) sessions

> **Section order below is fixed.** Each agent writes to its own section and no other. `Robotnik`
> reads only `## Status` and `## Next Actions`. Do not reorder, rename, or remove sections.

- **Created:** 2026-08-25

---

## Status

*Owner: `Robotnik`. Keep this SHORT and CURRENT — it is one of only two sections the PM reads, so a
stale entry means the whole loop runs on bad information.*

**Now (2026-08-27 11:10 UTC): attempt 3 complete — trigger characterization solid, runtime
mitigation exhausted, `auto` kept; a FRESH chip wedges on a single ~201k prefill.** Tails
session 2 (08:35–10:4x UTC) delivered checkpoints 3.2–3.4 (record: `## Implementation`): every
writable sysfs surface probed (level file accepts only auto/low/high/manual, `medium`=EINVAL;
`pp_dpm_sclk` in manual mode: all writes EINVAL; `pp_od_clk_voltage`: EINVAL; no power-cap
hwmon entry; no `ppfeaturemask`) → **no runtime knob can cut sustained power while holding
speed within 20%**. `low` measured and rejected (4.5x slower: 55.5/2.83 t/s vs 255.8/11.87).
The decisive ~201k cold-prefill repro on a fresh chip: **FAILED — rc=52, 0→1 wedges, wall
1760 s (29.3 min)** (`/tmp/run_end_repro201k_auto.txt`): a single ~201k prefill at the 120 W
cap is itself the trigger; no accumulated stress needed. The session then died in the wedge
burst (10:46:26 + 10:46:39 UTC, both "recovered through reset"); the "Staged, awaiting user
approval" section was never filled (still "none yet"). **Operational note: llama-server is now
a manual process** (unit `llama-server-qwen3.8-27b-q4.service` inactive; pid 13071 since
10:41 UTC) — a wedge kills it and **nothing restarts it**; the recovery command of record is
in checkpoint 3.2. `Robotnik` decision (recorded): the team operates in the **safe regime** —
small-context dispatches; the 2a/2b delta-prompt regime ran 4.5 h with zero in-window wedges,
and the cascade is only lethal when a session's context approaches ~200k. Restart/reboot-level
options await the user's decision.

**Now (2026-08-27 02:45 UTC): Q4 wedges too — 5 events since the 2026-08-26 12:25 UTC boot;
the TASK-0008 2c dispatch died to one at 02:33 UTC.** Kernel journal shows 5 `device wedged`
events since boot (0 at 12:50 UTC on Aug 26; 11:42 UTC now, uptime 14:17). The 2c session
(opencode run `4408203b`) survived one `Loading model` reload (01:08:17 UTC) and died
02:33:18 UTC with "socket connection was closed unexpectedly". Rate ≈ 1 wedge per 4.7 h: the
"measurably stable" decision (2026-08-26 12:50 UTC) is **withdrawn**. Tails attempt 3
(runtime mitigation, the user-approved scope in `## Definition of Done`) dispatches now,
resuming from any attempt 2 checkpoint in `## Implementation` / `## Test Results`. First
usable load-correlation data now exists: 5 wedge timestamps vs the known dispatch activity
windows (2a/2b ~20:00–00:30 UTC, 2c 01:08–02:33 UTC, Aug 26/27).

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
      since boot, orphan `gdm-login-vm` dead (corrected 2026-08-26 19:55 UTC in the
      TASK-0008 doc: the unsuffixed `virsh` check; the domain had run since 14:51 UTC).
      Endpoint-stability decision made: sufficient to
      resume TASK-0008 item 2, with wedge-count monitoring before/after (record: `## Status`).
- [x] `Robotnik` (2026-08-27 02:45 UTC): Q4 wedge record (record: `## Status`): 5 events
      since the 2026-08-26 12:25 UTC boot; the TASK-0008 2c dispatch died to one at 02:33 UTC;
      the 2026-08-26 12:50 UTC stability decision is withdrawn.
- [x] `Tails` (attempt 3, sessions 1+2, 2026-08-27): characterization complete (checkpoint
      3.1: power-cap stress, ~201k cold-prefill cascade, reload ~5.1 s); runtime surface
      exhausted, `auto` kept, `low` rejected with numbers (3.3/3.4); 201k repro executed on a
      fresh chip: wedged at 29.3 min (end marker on EVO-X2). Session died in the 10:46 UTC
      wedge burst; staged options NOT written (section still "none yet").
- [ ] `Robotnik`: user decision on the remaining options (accept risk / re-enable the systemd
      unit / kernel-upgrade window); record the decision in `## Status`.
- [ ] `Tails` (only if the user picks a kernel-upgrade window): research + stage the exact
      commands and revert under "Staged, awaiting user approval" (research-only, nothing
      executes).
- [ ] `Shadow` → `Omega`: review the applied/staged changes once Tails checkpoints them.
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

### Attempt 3 (dispatched 2026-08-27 ~05:10 UTC, Tails)

**Checkpoint 3.1 (2026-08-27 05:20 UTC): state snapshot + trigger characterization complete.**

State: host `trip` (EVO-X2), kernel `7.0.12-1.el10.elrepo.x86_64`, boot 2026-08-26 12:25 UTC
(uptime 16:48 at 05:13 UTC). Q4 endpoint: `llama-server-qwen3.8-27b-q4.service`, pid 4707 on
8092, model `/mnt/data/models/qwen3.8-27b-q4/Qwen3.8-27B-UD-Q4_K_XL.gguf`; frozen flags intact
(`-fa on`, `-ctk q8_0 -ctv q8_0`, `-c 262144`, `--parallel 1`; plus `-t 32 -tb 32 -ub 2048 --mlock
--n-gpu-layers 99 --mmproj ...`). Q5 (8084): no listener. Wedge count 5
(`journalctl -k --no-pager | grep -cE "device wedged"`); fence-fallback hangs 7; throttling events
0 with logging enabled.

Sysfs prior state (05:13 UTC, light load) — the backup of record per DoD:

| File | Value |
|---|---|
| `power_dpm_force_performance_level` | `auto` |
| `power_dpm_state` | `performance` |
| `pp_cur_state` | `0` |
| `pp_dpm_sclk` | `0: 600 / 1: 2728* / 2: 2900` MHz |
| `pp_dpm_mclk` | `0: 400 / 1: 800 / 2: 1000*` MHz |
| `pp_dpm_socclk` | `600..1472` MHz (8 states) |
| hwmon2 | edge 74.0 C, PPT 99.1 W, sclk 2726 MHz, busy 89% (mid-session sample) |
| `tuned` profile | `throughput-performance` |

Revert of record for the mitigation to be applied:
`echo "600 2728 2900" > /sys/class/drm/card0/device/pp_dpm_sclk && echo auto > /sys/class/drm/card0/device/power_dpm_force_performance_level`.

**The 5 wedges (UTC, `journalctl -k --utc`):** 01:08:08 (comp_1.1.0, pid 1817), 01:36:48
(comp_1.2.0, pid 4369), 01:37:18 (comp_1.2.0, pid 4369, 30 s later, same process), 02:05:28
(comp_1.2.0, pid 4478), 02:33:17 (comp_1.2.0, pid 4596). All 5 fall inside the 2c dispatch window
(01:08-02:33 UTC). Zero wedges during the 2a/2b window (2026-08-26 20:00 -> 2026-08-27 00:30 UTC)
or after 02:34 UTC. Fence fallbacks: 01:38:11, 01:38:43 (right after the 01:37:18 wedge),
02:34:42 (right after 02:33:17), 04:47:18 (during idle).

**Service lifecycle (user journal, UTC):** 1817 listening 12:25:30 -> wedge 01:08:08; 4369
01:08:21 -> wedges 01:36:48 + 01:37:18; 4478 01:37:30 -> wedge 02:05:28; 4596 02:05:39 -> wedge
02:33:17 (= the 2c death at 02:33:18); 4707 02:33:28 -> now. **Model reload takes ~5.1 s**
(`loading model` -> `model loaded` on NVMe + mlock), so per-wedge downtime is ~6-10 s, not the
"multi-minute model reload" recorded in `## Status` (that description predates the Q4 boot).

**In-flight work at each wedge (Q4 user journal, epoch-bounded windows):**
- Wedges 2/4/5 were each a **cold ~201k-token prefill of the 2c session's full context**, starting
  within ~6 s of each restart (opencode retrying the same request on the fresh process, empty KV):
  - Wedge 2 (pid 4369): started 01:08:26, total = 102400/0.51 ~= 200,784 tokens, rate 146.07 ->
    123.81 t/s; last confirmed progress 137,216 (68.3%) at 01:26:54 (t=1108 s), then **no progress
    lines for 9.9 min** and the ring timeout fired 01:36:48 (t=1702 s, 28.4 min): a silent hang
    after 137k tokens.
  - Wedge 4 (pid 4478): started 01:37:37, total = 126976/0.63 ~= 201,549; last line 176,128
    (87.4%) at 02:05:22 (t=1665 s), wedge 02:05:28 (t=1671 s, 27.9 min) ~6 s later, ~176.8k
    tokens (87.7%).
  - Wedge 5 (pid 4596): started 02:05:39, total = 124928/0.62 ~= 201,497; last line 174,080
    (86.4%) at 02:33:11 (t=1631 s), wedge 02:33:17 (t=1638 s, 27.3 min) ~6 s later, ~174.8k
    tokens (86.8%).
  - The cold-prefill hang point degrades with cumulative chip stress: 68.3% -> 87.7% -> 86.8%
    of a ~201k prompt (the fresh-chip Q5 threshold from attempt 1 was ~190-198k, i.e. 96-99%).
- Wedge 1 (pid 1817): the request in flight at 01:08:08 started after 01:07:51 (previous request
  completed 01:07:51: 623-token delta prefill + 3675-token decode at 8.07 t/s; `all slots are
  idle` 01:07:51). No progress line logged before the wedge: in-flight work was a small delta
  prefill on an intact ~200k context, 17 s in. Not a cold 200k prefill. The chip had carried
  2a/2b churn since ~20:00 UTC (4.5 h, zero wedges inside that window) plus 2c start
  (00:30-01:08 UTC).

**Correlation verdict:** all 5 wedges inside the 2c window, zero in 2a/2b or after 02:34. The
2a/2b-style churn (sampled 2026-08-26 15:30-17:33 UTC: delta prompts 348-4034 tokens at 52-164
t/s + 1-2.3k-token decodes at 8-11 t/s, idle gaps 17 s-8 min) does not wedge in-window but
accumulates stress; wedge 1 fired on the next request after ~12 h of mixed load. The cascade
(wedges 2-5) is self-perpetuating: each wedge kills the KV cache, forcing a cold ~201k re-prefill
on retry, which wedges again at 27-28 min. The 2c session could never complete its ~201k request
inside this loop (died 02:33:18).

**Characterization (updated, supersedes attempt 1 wording):** trigger = sustained continuous
full-power load accumulating chip-level stress that a compute-ring reset does NOT clear. Two
observed regimes: (1) hours of high-churn delta work (2a/2b: 4.5 h, 0 in-window wedges, set up
wedge 1); (2) a single cold ~200k prefill (wedges 2-5: 27.3-28.4 min, hang point degrading
68-88% with cumulative stress). First live readings at a wedge moment (baseline repro CSV, 16th
wedge, `auto`, 2026-08-25 09:42-10:15 UTC, `/tmp/gpu_samples_baseline.csv`): PPT pinned
119-120 W for the entire 32.7 min (chip at the package power cap; sclk oscillating 2513 -> 2836
MHz to stay under it), edge 84 -> 92 C drifting up, 100% busy, 0 throttle events. Power flat at
the cap, temperature far below any trip point: consistent with sustained at-power-cap operation,
not thermal throttling.

**Mitigation implication:** under `auto` the ceiling is power-limited at ~120 W with sclk
2500-2900 MHz. Pinning sclk to 2500 MHz should drop steady PPT to ~105-110 W and slow stress
accumulation. Decisive test: the same ~201k cold prefill must COMPLETE under the pin (it hangs at
68-88% under `auto` on this already-stressed chip).

Next (in order): baseline speed at `auto` (16k cold prefill + 64 decode, 3 runs) -> apply
`manual` + `pp_dpm_sclk 2500` -> verify clocks under load -> re-measure speed -> 201k cold-prefill
repro under the pin (background, 5 s sampling) -> keep/revert.

### Attempt 3, session 2 (re-dispatched 2026-08-27 ~08:35 UTC, Tails)

**Checkpoint 3.2 (2026-08-27 08:45 UTC): new-boot context + fresh sysfs snapshot.**

Context added since checkpoint 3.1 (per dispatch brief): EVO-X2 fully shut down and rebooted,
user-confirmed. **Time discrepancy (flagged, not silently overridden):** the brief says the
reboot was "~17:01 UTC"; host evidence says boot ~08:01 UTC = 17:01 JST (`date -u` = 08:42:24
UTC with `uptime` = 41 min at 08:42 UTC). The brief's "17:01" is JST (EVO-X2 local time, UTC+9).
All times in this checkpoint are UTC. The previous boot's journal is gone: the 5 wedges recorded
in checkpoint 3.1 are the complete record of the previous boot as of 02:45 UTC; any wedges
between 02:45 UTC and the ~07:5x shutdown are unrecoverable (gap, recorded).

State (08:42 UTC): kernel `7.0.12-1.el10.elrepo.x86_64`; wedge count **0** (monitoring command
`journalctl -k --no-pager | grep -cE "device wedged"`). 8092: llama-server **pid 1852, running as
a manual process since boot** (user-confirmed); systemd unit
`llama-server-qwen3.8-27b-q4.service` reports **inactive** — recorded per dispatch instruction,
unit management not changed. 8084 (Q5): no listener. Frozen flags intact per
`tr "\0" " " < /proc/1852/cmdline`: `-fa on -ctk q8_0 -ctv q8_0 -c 262144 --parallel 1` (plus
`-t 32 -tb 32 -ub 2048 --mlock --n-gpu-layers 99 --mmproj`), model
`/mnt/data/models/qwen3.8-27b-q4/Qwen3.8-27B-UD-Q4_K_XL.gguf`.

**Recovery command of record** (risk: this is a manual process, so a wedge kills it and
**nothing restarts it** — unlike the previous boot, where the unit auto-restarted ~10 s after
each wedge. If a wedge hits, run this to restore the endpoint; using the unit instead is the
user's call, recorded only):

```
nohup /usr/local/bin/llama-server --model /mnt/data/models/qwen3.8-27b-q4/Qwen3.8-27B-UD-Q4_K_XL.gguf --mmproj /mnt/data/models/qwen3.8-27b-q4/mmproj-F16.gguf --alias Qwen3.8-27B-UD-Q4_K_XL --host 0.0.0.0 --port 8092 --n-gpu-layers 99 -fa on --parallel 1 -t 32 -tb 32 -ub 2048 -ctk q8_0 -ctv q8_0 --mlock -c 262144 > /tmp/llama-server-manual.log 2>&1 &
```

Sysfs prior state (08:42 UTC, mid-session load, busy 98) — backup of record for this boot:

| File | Value |
|---|---|
| `power_dpm_force_performance_level` | `auto` |
| `power_dpm_state` | `performance` |
| `pp_cur_state` | `0` |
| `pp_dpm_sclk` | `0: 600 / 1: 1100 / 2: 2900*` MHz |
| `pp_dpm_mclk` | `0: 400 / 1: 800 / 2: 1000*` MHz |
| `pp_dpm_socclk` | `600 / 736 / 883 / 981 / 1104 / 1261 / 1472 / 1472` MHz |
| hwmon2 (`name=amdgpu`) | `temp1=edge` 64.0 C, `power1=PPT` 111.1 W at busy 98 |
| `thermal_throttling_logging` | enabled, 60 s interval |
| `tuned` profile | `throughput-performance` |

**The DPM sclk state table changed between boots (open question, recorded):** checkpoint 3.1
(05:13 UTC, previous boot) read `600 / 2728* / 2900`; this boot reads `600 / 1100 / 2900*`.
Consequence for the mitigation surface: `power_dpm_force_performance_level` maps
low/medium/high to states 0/1/2, so on this boot `low`=600 (unusable), `medium`=**1100**
(~2.6x slower than 2728, too slow for the team), `high`=2900 (pinned top state, no mitigation
versus auto's oscillation). The checkpoint 3.1 plan therefore still stands as the right lever:
`power_dpm_force_performance_level=manual` + `pp_dpm_sclk=2500`. A `medium` probe run is planned
to record the rejection with a number.

Revert of record for this boot: `echo "600 1100 2900" > /sys/class/drm/card0/device/pp_dpm_sclk && echo auto > /sys/class/drm/card0/device/power_dpm_force_performance_level`.

`/tmp` survived the reboot (not tmpfs): attempt 1 artifacts `/tmp/wedge_repro.sh` and
`/tmp/gpu_samples_baseline.csv` (16th wedge, Q5) still present; payload files gone. Python
3.12.13 present. New test script written this session: `/tmp/run_test.sh` (see checkpoint 3.3).

Next (in order, supersedes the checkpoint 3.1 "Next" list): baseline speed at `auto` (3x
~16k cold prefill + 64 decode, 2 s power sampling) -> apply `manual` + `pp_dpm_sclk 2500` ->
verify clocks under load -> re-measure speed (keep if prefill and decode slowdowns are both
<= 20%, otherwise revert) -> `medium` probe (1 small run, for the record) -> restore pin ->
201k cold-prefill repro under the pin (background, 5 s sampling, single long wait) -> keep/revert.

**Checkpoint 3.3 (2026-08-27 ~09:35 UTC): runtime mitigation surface is exhausted on this
driver build; keeping `auto`. Corrections to checkpoint 3.2 included.**

Corrections (evidence below):
1. **`pp_dpm_sclk` middle entry is the LIVE clock, not a fixed DPM state.** Values observed at
   different moments: `1100*` (08:42, marker actually on state 2 = 2900), `2843*` then `902*`
   2 s apart (~09:10, no GPU load between commands), `1410*`, `2713*`, `2682*`, `2756*`.
   Interpretation consistent with all readings: the file shows `[min state, current sclk, max
   state]` and `*` marks the entry equal to the current clock (state 2 when current = max).
   Checkpoint 3.2's "medium = 1100, too slow" claim is withdrawn.
2. **`power_dpm_force_performance_level=medium` is rejected** on this driver build:
   `echo medium | sudo tee .../power_dpm_force_performance_level` -> `tee: Invalid argument`.
   Accepted values (verified by write + readback): `auto`, `low`, `high`, `manual`.
3. **Sysfs writes require root.** Files are `-rw-r--r-- root root`; user `howard`
   (uid 1000, groups wheel) gets `Permission denied` on direct writes. `howard` has
   passwordless sudo (`sudo -n true` OK); all writes this session used `echo ... | sudo tee`.

Baseline speed at `auto` (this boot, 09:15-09:25 UTC, 3 runs, unique payloads per run so
`cache_n=0` cold prefill each time; `/tmp/run_test.sh`, tag `auto16k_{1,2,3}`, 76000 chars =
15392 prompt tokens, n_predict=64):

| run | prefill t/s | decode t/s | PPT mean/max (W) | sclk range (MHz) | edge max (C) |
|---|---|---|---|---|---|
| auto16k_1 | 254.7 | 11.90 | 119.1 / 133.1 | 1893-2887 | 91.0 |
| auto16k_2 | 256.3 | 11.82 | 117.5 / 133.1 | 600-2887 | 88.0 |
| auto16k_3 | 256.3 | 11.88 | 117.4 / 133.1 | 600-2896 | 87.0 |

PPT pinned at the 120 W cap on average (120,002,000 uW read live), 133-134 W transient spikes,
sclk oscillating 600-2900 under the cap — same signature as the 16th-wedge baseline CSV
(checkpoint 3.1). Wedge count stayed 0 through all runs.

Mitigation surface, empirically probed (all writes as root via `sudo tee`):

| Surface | Probes | Result |
|---|---|---|
| `power_dpm_force_performance_level` | auto/low/high/manual accepted; **medium rejected (EINVAL)** | writable |
| `pp_dpm_sclk` (manual mode) | `2500`, `2500 2500`, `600 2500`, `600 2500 2900`, `2500000`, `2500000 2500000`, `600000 2500000`, state indexes `0`/`1`/`2`, `600 2900` | **all EINVAL — no clock settable in manual mode on this build** |
| `pp_od_clk_voltage` | multi-line `OD_SCLK:`/`OD_RANGE:` block, `2500`, single-line `OD_RANGE:` | all EINVAL (read shows default 2-anchor table 600/2900, no voltage data exposed) |
| hwmon2 power cap | full file survey | **none** (only edge temp, PPT, sclk freq, vddgfx/vddnb=0; `power` entry is a PCI device dir) |
| `ppfeaturemask` | `ls` | does not exist in this build |

**Decision: no effective runtime (sysfs) mitigation is available on this driver build.**
The level file can only pin 600 (`low`, ~4x too slow for the team), 2900 (`high`, top state,
no power benefit over auto's PPT-clamped oscillation — not tested, reasoned from the 120 W cap
being firmware-enforced), or leave clocks unmanaged (`manual` with no settable clock behaves
like auto: live clocks 2682-2798 observed during manual). Reverted everything to `auto`
(verified). The checkpoint 3.1 plan (manual + 2500 pin) is dead on this build; it is not
retried.

Wedge-count under load is still measurable: the decisive ~201k cold-prefill repro (checkpoint
3.1) now runs under `auto` on a fresh chip as the baseline "under load" data point (does a
201k prefill complete on a fresh chip at all? the 5 wedges of the previous boot were on an
already-stressed chip, the old Q5 fresh-chip threshold was ~190-199k). It doubles as the
first full-window live sensor profile on this boot. Risk accepted per dispatch: a wedge kills
the manual llama-server (pid 1852) and this session; recovery command is in checkpoint 3.2 and
all artifacts land on EVO-X2.

Next: `low` probe (1 small run, records the rejection with a number) -> 201k repro under `auto`
(background, 5 s sampling, single long wait) -> keep/revert final -> staged options -> fixes doc.

**Checkpoint 3.4 (2026-08-27 ~09:55 UTC): `low` probe rejected with numbers; runtime decision
final = keep `auto`; 201k repro starting now.**

`low` (600 MHz pin) probe, 2000 chars = 415 tokens, n_predict=16 (tag `low600_probe`):
prefill 55.5 t/s, decode 2.83 t/s, PPT mean 21.6 W. Versus `auto` (255.8 / 11.87 t/s baseline):
**prefill 78% slower, decode 76% slower, ~4.5x slower overall**. Rejected — the whole team runs
on this endpoint. It does confirm the power drop at low clocks is real (21.6 W vs 117 W), but
the price is unacceptable. `pp_num_states` = "states: 1 / 0 default", `pp_force_state` empty
(no additional surface).

**Runtime-surface decision (final): keep `auto`.** No writable knob on this driver build can cut
sustained power while holding speed within 20%. The effective mitigation must be
restart/reboot-level (staged under "Staged, awaiting user approval") or host/BIOS-level
(out of scope for this task). Everything is reverted to `auto` (verified after each experiment).

Starting now: the decisive ~201k cold-prefill repro under `auto` on a fresh chip.
- Launch: `nohup bash /tmp/run_test.sh repro201k_auto 951423 1 5 3600 &` (951,423-char payload,
  same size as the checkpoint 3.1 repro = ~200,784-201,549 tokens on the same model; n_predict=1;
  5 s sampling; pid in `/tmp/repro_pid_auto`).
- Artifacts: `/tmp/run_end_repro201k_auto.txt` (completion marker + summary),
  `/tmp/gpu_samples_repro201k_auto.csv` (ts busy edge PPT sclk hwmon_sclk wedges),
  `/tmp/run_resp_repro201k_auto.json`, `/tmp/repro_log_auto.txt`.
- Expected duration ~25-30 min (previous-boot wedges fired at 27.3-28.4 min of the same prompt
  at 123-146 t/s; a fresh chip may be faster).
- Outcomes: (a) completes, 0 wedges -> a fresh chip survives a 201k prefill under auto, i.e. the
  wedges need accumulated stress (refines the characterization); (b) wedge -> first fresh-chip
  201k wedge point + live sensor profile through the failure; the manual llama-server (pid 1852)
  dies and is NOT auto-restarted (unit inactive), and this session dies at its next inference;
  restore with the checkpoint 3.2 command. All artifacts survive on EVO-X2 either way.
- If the wait call below times out (~48 min): re-check the end marker; data is safe on EVO-X2.

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
