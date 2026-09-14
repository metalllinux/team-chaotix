# TASK-0010 — Fix the EVO-X2 iGPU wedge that kills llama-server (Q5) sessions

> **Section order below is fixed.** Each agent writes to its own section and no other. `Robotnik`
> reads only `## Status` and `## Next Actions`. Do not reorder, rename, or remove sections.

- **Created:** 2026-08-25

---

## Status

 *Owner: `Robotnik`. Keep this SHORT and CURRENT — it is one of only two sections the PM reads, so a
 stale entry means the whole loop runs on bad information.*

**Now (2026-09-14 17:20 JST, Robotnik): review chain complete; Tails citation-refresh pass
dispatched; user gate on F1 staged mitigations.** Shadow attempt 2 done (no new blockers;
stale-citation nits routed to a Tails refresh pass). Omega attempt 3 done: F1 **high, open** —
0.0.0.0:8093, CORS `*`, no API key (zero-auth LAN-wide DoS of the single inference slot); M1-M5
staged, nothing applied; F2 low (11 stale firewall ports); escalation condition: if the router
port-forwards 8093, F1 is critical (one-look user check). Omega's ssh probe was blocked by its
bash allowlist, so live state rests on documented evidence (E1-E3 in `## Security`). Big done:
5/5 re-verification checks PASS; monitor still running (final line at hard stop 22:44:43 JST).
DoD gate NOT met: F1 open pending the user-approved window for M1 (unit change + service restart)
/ M2 (firewalld pin).

**Now (2026-09-14 15:15 JST, Robotnik): Omega attempt 2 LOST (zero writes again); attempt 3
dispatches with mechanical write rules + narrow scope; doc checkpoint 7d8e59c.** Session
`ses_f61985895…` ran 23 steps / 31 tool calls (all reads/greps, chunked per the brief), died on a
100,951-token request with **zero doc edits** — the exhortation-only "write-first discipline" brief
did not hold (same failure mode as attempt 1; lesson: this model defers all writes to a final pass).
Attempt 3 brief is mechanical: first tool call MUST be an edit creating the attempt-3 subsection in
`## Security`, at most 2 consecutive reads without an intervening write, scope narrowed to the live
exposure surface + verifying the pre-existing `## Security` findings. Machine calm at 14:31: 0
wedges since boot, 8093 listening (0.0.0.0).

**Now (2026-09-14 14:31 JST, Robotnik): Omega attempt 2 dispatched (write-first discipline);
machine calm.** 0 wedges since boot (17 h 01 m uptime, load 0.27), 8093 listening (0.0.0.0).
Chain position: Shadow attempt 2 done (11:45), Omega attempt 1 lost (13:10 entry), Big next after
Omega. If Omega attempt 2 also returns empty, check the session DB (finish=tokens.output per
AGENTS.md §14) before re-dispatching a third time.

**Now (2026-09-14 13:10 JST, Robotnik): truncation mechanism pinned; Omega attempt 1 LOST (zero
writes), re-dispatch with write-first discipline; service clean-restarted 10:46:49 JST.**
- Empty task results on today's dispatches are **server-side window exhaustion**: the EVO-X2
  journal shows Omega's final request at `n_tokens = 98303, truncated = 1` (12:39:40 JST, session
  end 12:39:40) — accumulated session context filled the `-c 98304` window, the server truncated
  the turn (finish=length, no text/tool part → empty result). Not the 32k output clamp (separate,
  still real). The session-DB per-message `tokens.input` is NOT the full request context (Omega's
  final turn reported in=181 in the DB; the server saw 98,303) — the server journal is the truth.
- Shadow attempt 2: work survived (incremental writes; only the closing summary lost). Omega
  attempt 1: work LOST (111 parts of investigation, zero doc edits — all writes deferred to a
  final pass that never happened). Re-dispatching with write-first discipline.
- llama-server clean-restarted 10:46:49 JST (systemd Stopping/Stopped/Started, no crash, wedge
  count 0; unit mtime unchanged 2026-09-13 17:51:56, `-c 98304` intact, pid 9144, 8093
  listening). Provenance consistent with the user's 10:46 reconfiguration (opencode.json edit
  10:46:27, opencode start 10:46:40); the W3 pid-1907 record is superseded. The 24 h monitor is
  still valid (kernel-journal based). Big's box-13 live verification covers current state.
- Security lead for Omega from the 10:46:49 startup log: llama.cpp on 0.0.0.0:8093 with CORS `*`
  and no API key (the server's own warning).

**Now (2026-09-14 11:45 JST, Robotnik): Shadow attempt 2 DONE (empty result verified, not a
death).** Shadow returned an empty task result; session-DB check (ses_f6255d03…): final turn
finish=length, in=4,632 out=382, reasoning-only part, no text part, no doc part — the closing
summary turn truncated, not the 32k reasoning pattern (the session never approached the 98,304
window; the aligned client limits + incremental writes held). The `## Review` "Attempt 2
verification" subsection (2140-2261) is complete: passes 1, 2, 3a-3d all marked done with a clean
terminator; lost content is summary-level only (a stale-citation note at W1 1693, same known
stale-citation nit class that pass 2 already routes to Tails's refresh pass). No new blockers from
Shadow. Omega dispatches next in the chain.

**Now (2026-09-14 11:00 JST, Robotnik): client config aligned; Shadow re-dispatches on the fresh
session.** The user set the iq4xs limit to context 98304 / output 49152
(`~/.config/opencode/opencode.json:148-151`; output 49152 vs the 32000 requested, harmless — the
gateway's 32,000 output clamp is independent of the client declaration, TASK-0019). Config mtime
10:46:27 JST precedes this opencode start (pid 51205, 10:46:40 JST), so this session and every
subagent loaded the aligned limits. Machine calm: 0 wedges since boot (13.5 h uptime, load 0.32),
8093 listening, 24 h monitor running (last sample 10:59:45 JST wedge_count=0, hard stop 22:44 JST).
Shadow dispatches now with incremental `## Review` writes.

**Now (2026-09-14 07:40 JST, Robotnik): Shadow attempt 1 died to window exhaustion; client config
mismatch identified, change requested from the user.** Shadow's session (87 parts) accumulated to
the 98,304 window across many turns; the FIRST request was only 10,408 tokens, so the b1867bf
checkpoint reset worked and the injected diff was not the cause — plain tool-result accumulation
was. Last turn: input 97,918, output 388, finish "length", zero doc writes (session DB
`ses_f6321b7d…`). Client-side mismatch: `~/.config/opencode/opencode.json` declares the iq4xs
limit context 262144 / output 131072, while the live server runs `-c 98304` (verified 2026-09-14
07:25 JST via pid 1907 cmdline + unit ExecStart) and the gateway clamps output at 32,000
(TASK-0019, 2026-09-02). PM edit permission covers `planning/**` only (least privilege), so the
user was asked to set the iq4xs `limit` to context 98304 / output 32000; it takes effect at the
next opencode start and does not affect the running session. Shadow re-dispatches with incremental
`## Review` writes so findings survive a mid-review death.

**Now (2026-09-14 07:20 JST, Robotnik): review chain starts; machine calm.** 0 wedges since the
2026-09-13 21:29 JST reboot (9 h 50 m uptime, load 0.34); service active (pid 1907, 8093); 24 h
monitor still running (pid 6647, last sample 07:14 JST wedge_count=0, hard stop 2026-09-14 22:44
JST). Shadow dispatches now; chain runs sequentially Shadow → Omega → Big. Monitor result to be
checked before Knuckles.

**Now (2026-09-13 23:05 JST, Robotnik): W3 DONE; dispatch-failure root cause found and fixed.**
W3: kernel 7.2.5 live, build 2000 confirmed via /proc/1907/exe, wedge baseline 0, 24 h monitor
running (pid 6647, log /tmp/wedge-monitor-20260913-224443.log, hard stop 2026-09-14 22:44 JST).
The first Shadow dispatch hard-failed with zero work: request 98591 tokens vs the 98304 window.
Root cause: opencode injects the working-tree diff (vs git HEAD) of files touched by the session
into every subagent's initial request; the planning doc carried 1,420 uncommitted insertions
(148KB diff vs the Aug 27 commit), injected into every brief. That, not the subagents' own
doc-reading, dominated request size (the 24-min Tails session's full reads were an aggravating
factor, not the cause). Fix: mid-task checkpoint commit d26a115 (doc only; other tasks' files
untouched); the injected patch is now empty until the next edit. Lesson: keep planning docs
committed as work progresses; under the 98304 cap, uncommitted doc growth is a dispatch
availability risk, not just a hygiene issue. Shadow re-dispatches.

**Now (2026-09-13 21:00 JST, Robotnik): W1 DONE; W2 dispatches now and kills the PM session with
the reboot (expected, approved).** W1: t/s verification PASS (live decode 11.95 t/s at ~57.9k vs
baseline 12.1-12.3 t/s; prefill 174.96 t/s; fingerprint b2000-5266f24d), checkpoint in
`## Implementation`, ticked in `## Next Actions`. Machine calm: wedge count 10 since boot, stable
through the W1 benchmark. W2 = Stage 3 (grub default to 7.2.5 by exact menuentry title, Shadow
blocker 1) + reboot. The W2 Tails session dies issuing the reboot (checkpoint precedes the
command); the PM session dies with it because it runs on 8093. After the reboot: wait for 8093,
then dispatch W3 (post-reboot verification + bounded 24 h wedge monitor, pid recorded). The
review chain (Shadow → Omega → Big), Vector, Knuckles follow W3.

**Now (2026-09-13 19:52 JST, user): keep `-c 98304`.** Options presented 122880 (recommended),
131072 (ceiling), keep 98304; the user chose keep. Wedge-risk priority over pipeline headroom.
Consequence: the whole dispatch chain runs under strict no-full-read discipline (grep-first,
chunked reads with offset/limit, one section-sized read per pass) on the 1828-line doc. W1
re-dispatches under that discipline; only the t/s verification + checkpoint remain (the Stage 1
restart already happened at 17:51:56 JST, provenance unverified).

**Now (2026-09-13 19:30 JST, Robotnik): W1 attempt 2 hard-failed at the 98304 context cap; the
cap is structurally too small for the dispatch chain on this doc.** The fresh Tails session ran
24 min (13 turns, Stage 1 recon complete, zero doc changes), then the next request hit 99264
tokens vs the 98304 window and opencode refused it. Cause: three full reads of the 1828-line
planning doc (each ~27k tokens, no offset/limit) plus a 34k-byte reasoning part. Consequence:
every agent in the chain (Shadow/Omega/Big, later Espio) faces the same wall at 98304; Espio
cannot read the doc at all. The 98304 value was user-confirmed 2026-09-13 with 131072 as the
documented ceiling "only if a task genuinely needs it"; the team's own operation now
demonstrably needs >98304. Escalated to the user with three options (122880 recommended: below
the 126.5k largest prefill verified clean; 131072 ceiling; keep 98304 with strict read
discipline). If a new value is approved it lands in the unit file now (backed up, no restart)
and takes effect at the W2 reboot already in the approved window.

**Now (2026-09-13 18:48 JST, Robotnik): W1 attempt 1 died to context exhaustion; Stage 1 was
already applied externally.** The W1 Tails session (18:10–18:46 JST) ran 20 read-only steps, then
the final turn truncated (`finish: length`, 539 output tokens, reasoning only, zero doc changes);
session-DB check: the input context had filled, not the 32k cap. Its recon found Stage 1 applied
between 16:17 and 17:51 JST (provenance unverified, likely user): staged-name backups in /tmp
(`llama-unit.bak1.1789287454`, `llama-bin-bak1.1789287454/`, `llama-libs-bak1.1789287454/`,
`cmdline.bak1`, build log `/tmp/llama-build-v0.4.0.log`), unit diff vs backup = only the `-c 98304`
flag, binary build 2000 (5266f24d), service running under the user unit since 17:51:56 JST.
Remaining W1: t/s verification against the iq4xs baseline + checkpoint. Fresh small-context Tails
session dispatched for the remainder.

**Now (2026-09-13 18:01 JST, Robotnik): dispatch pause lifted; Stage 1's `-c` change is already
live, provenance unverified.** Machine calm: the ~200k retry loop has stopped; last wedge
13:20:49 JST (10 total since boot), ~4.7 h wedge-free, load 0.43. The iq4xs unit file was modified
at 17:51:56 JST and now carries `-c 98304`; the service restarted at that moment (pid 24367,
running under the user unit, 8093 listening); binary build 2000 (commit 5266f24d); kernel still
7.0.12-1.el10.elrepo. Provenance unverified (likely user action, the standing pattern for EVO-X2
ops). `W1` dispatched with a reconcile brief: apply only the missing Stage 1 parts (no redundant
second restart), verify against the iq4xs baseline.

**Now (2026-09-13, user): context-size question for the iq4xs unit; `Robotnik`
recommendation (evidence-based): `-c 98304` (96k).** A 96k cold prefill runs ~15.6 min at
~105 t/s vs the 26–31 min fresh-chip wedge boundary (1.7x margin); 96k cached is well below
the 185–196k hot zone where all 12 hot wedges occurred; 126.5k is the largest prefill
verified clean. Conservative: 65536. Absolute ceiling: 131072, only if a task genuinely
needs it. Consequence: a ~200k-context task no longer fits (truncated, not wedged) — that is
the point; the task needs redesign. **User confirmed `-c 98304` (2026-09-13); the change
folds into the Stage 1 restart of the approved window (one restart, unit backed up per the
standing rule).**

**Now (2026-09-13, user): window approved — "go ahead and start this now" for Stage 1 +
Stage 3 (llama.cpp update + service restart, then kernel 7.2.5 + reboot).** `Robotnik`
decision, recorded: both stages apply in the single window per the user's instruction; if the
wedges stop, Stage 1 vs Stage 3 attribution is ambiguous (accepted for the "stop the wedges"
goal; bisect one stage at a time only if wedges persist). The 24 h wedge-count verification
starts after the reboot and is checked at the next turn via a bounded 24 h monitor. The
~200k-context retry-loop task was not confirmed stopped by the user; if still active it doubles
as the Stage 3 test workload and keeps killing concurrent sessions during observation.

**Now (2026-09-13 13:30 JST, Robotnik): wedges #8–#10 (12:25:41 / 12:53:15 / 13:20:49 JST) —
a ~200k-context retry loop is still active from a client outside the team (almost certainly the
user's own long task; the journal carries no client identity), ~27-min cadence, and the
fix-round-1 dispatch died to wedge #8 (connection reset; two small tool-call turns, zero parts).
While that loop runs the machine wedges roughly every 27 min and every concurrent session is
reset, so further dispatches are paused (each adds load to the accumulating stress). Escalated
to the user with the full findings: stop or shrink the ~200k task, and approve a window for
staged Stages 1 + 3. Pending after the machine is calm: Tails fix round (Shadow's 3 blockers +
should-fixes in `## Review`), then Omega, Big, Vector, Knuckles.

**Now (2026-09-13, Robotnik): 3 more wedges (boot 0 total 6), same ~200k-context retry loop;
T5b's first attempt died to a transport reset, not a wedge.** Wedges 16:04:20 / 16:31:58 /
17:00:08 UTC (Sep 13 01:04 / 01:31 / 02:00 JST), ~28-min cadence: the 01:04 JST one is hot
mode again (task 212721, incremental prefill against the same ~200k cached context, which had
been running 7 h; prompt cache is RAM-resident, 8192 MiB limit). Session owner unattributable
from the journal (no client identity); consistent with a long opencode task on the endpoint.
The T5b repro dispatch (18:26 JST Sep 12) died with "connection reset by server" 90 s in with
zero output parts and **no wedge and no service restart in the window** (llama-server healthy,
decoding a small task at 12 t/s) — transport-level reset, recorded as an open secondary issue
(llama.cpp v9671 HTTP layer resetting a queued connection, or LAN blip; one instance, unverified).
T5b re-dispatches fresh.

**Now (2026-09-12 09:25 UTC): 3 wedges under the iq4xs service on the current boot; the
investigation's own sessions are triggering the hot mode.** Boot 0 (03:47 UTC): wedges
08:22:22, 08:51:01, 09:18:35 UTC (rings comp_1.1.0 / comp_1.2.0), each followed by a 5–7 s
systemd auto-restart (NRestarts=3; service active, 8093 listening). The 08:22 wedge coincides
exactly with Tails' resumed session's T4 turn (T1–T3 context accumulated). T5-correlation
(2026-09-12, `## Implementation`) settled the rest: all three wedges were the same ~197–200k
opencode context (that session) — wedge 1 hot mode (incremental prefill, wedged 5 s after
launch), wedges 2–3 cold mode (opencode's retry re-prefilled the identical context from
scratch on each restarted process; hang point degraded 89% → 87%, cumulative stress). The
earlier "PM session's own turns" reading was a wall-time coincidence: with `--parallel 1` the
PM's requests were queued behind the re-prefill, not in flight. **Lesson recorded: a long resumed subagent
session is itself a hot-wedge trigger**; the rest of the task runs fresh small-context
sessions, one plan item per turn, never resuming a session that has grown large. The T4 turn
died to the 08:22 wedge (connection reset, zero output parts in the session DB); T4
re-dispatches fresh.

**Now (2026-09-12, user): repo-update requirement added.** Once the solution is in place,
update the `metalllinux/team-chaotix` GitHub repo with the latest findings: planning doc +
README via `Vector`, commit/push via `Knuckles` (boxes added to `## Definition of Done` and
`## Next Actions`).

**Now (2026-09-12, user directive): scope escalation — find the root cause and stop the
wedges.** The user no longer accepts wedge risk (supersedes the 2026-08-27 "accept the wedge
risk" decision for this task). Mission: attribute the wedge to kernel vs AMD driver (amdgpu
kmod + Mesa RADV) vs llama.cpp vs the systemd unit vs heat, each with evidence; state the
trigger in one sentence; answer the distro question (Rocky 10 vs Fedora vs NixOS, anything but
Ubuntu) with evidence; deliver a solution with step-by-step reverts. **Hard constraint (user,
2026-09-12):** the current model service `llama-server-qwen3.8-27b-iq4xs.service` (user-level
unit; name per the user, state to be verified) is never stopped for any reason during the
investigation — it serves this team's inference. Restart/reboot-level changes stay staged.
Chain: `Amy` → `Tails` → `Shadow` → `Omega` → `Big`.

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
approval" section was never filled (still "none yet"). **Operational note (corrected
2026-08-27 12:13 UTC): llama-server is NOT a manual process.**
`llama-server-qwen3.8-27b-q4.service` exists as a **user-level** unit (`~/.config/systemd/user/`;
the earlier `systemctl` checks ran system-level and saw nothing): **enabled, active, running**,
parent of pid 13071. Auto-restart demonstrated: pid 1852 → 13071 within ~5 s at 10:41 UTC, and
~11 s restarts on the previous boot. The checkpoint 3.2 "manual process / nothing restarts it"
claim (and this entry's amplification of it) is withdrawn. **User decision (2026-08-27 12:13
UTC): accept the wedge risk; the enabled user-level unit stays as-is (no re-enable needed); no
kernel-upgrade window.** `Robotnik` decision (recorded): the team operates in the **safe
regime** — small-context dispatches; the 2a/2b delta-prompt regime ran 4.5 h with zero
in-window wedges, and the cascade is only lethal when a session's context approaches ~200k.

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

- [ ] Root cause attributed with evidence, per hypothesis: kernel (amdgpu kmod
      `7.0.12-1.el10.elrepo`), AMD userspace driver (Mesa RADV), llama.cpp (version + flags),
      systemd unit config, thermal/heat. Each hypothesis is marked supported or excluded in
      `## Implementation` with the commands and outputs that decide it.
- [ ] The trigger is stated in one sentence (workload event + machine state → wedge), backed
      by the wedge-timestamp correlation against load/thermal/power history in
      `## Implementation`.
- [ ] The distro question is answered with evidence: the kernel and driver versions Rocky 10
      provides today vs Fedora/NixOS, and whether the fix is reachable on Rocky without a
      distro switch.
- [ ] At least one runtime (no-restart) mitigation is tried, or ruled out with evidence:
      before/after wedge counts under equivalent load in `## Test Results`.
- [ ] A staged solution: every fix requiring a llama-server restart or host reboot is written
      into `## Implementation` → "Staged, awaiting user approval" with exact commands,
      pre-change backups, and step-by-step reverts; none executed without a user-approved
      window.
- [ ] The user-frozen llama-server configuration is unchanged, or any change has explicit
      user approval recorded in `## Status`.
- [ ] `llama-server-qwen3.8-27b-iq4xs.service` is never stopped by the team: the journal is
      checked for team-initiated stops (zero allowed); wedge-triggered systemd auto-restarts
      are system behavior, counted in `## Test Results`, not prevented.
- [ ] Every modified unit or sysfs setting has its prior state backed up (units:
      `cp <unit> /tmp/<unit>.bakN.$(date +%s)`; sysfs: prior values in the doc), backup
      location recorded; the fixes doc
      `/home/howard/AI/projects/qwen-38-q5-fixes/qwen38-q5-fixes.md` is updated with the
      findings.
- [ ] A wedge baseline count plus the monitoring command are recorded in this doc.
- [ ] `Vector` + `Knuckles`: the `metalllinux/team-chaotix` repo is updated with the latest
      findings — README (EVO-X2 section) reflects the final root cause and fix status, and the
      planning doc + README are committed and pushed to GitHub (user requirement, 2026-09-12).
- [ ] `Shadow`: no unresolved blockers or should-fix findings in `## Review`.
- [ ] `Omega`: no unresolved findings above `low` in `## Security`.
- [ ] `Big`: the evidence cited in `## Implementation` is re-verified with re-run read-only
      commands, verdict in `## Test Results`, no silently dropped checks.

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
- [x] `Robotnik` (2026-08-27 12:13 UTC): user decision recorded (accept risk; the unit is
      already enabled user-level — nothing to re-enable; no kernel-upgrade window); the
      unit-management misread is corrected (record: `## Status`).
- [x] `Amy` (2026-09-12): plan rewritten for the new scope (H1–H5 hypothesis matrix with
      decision rules, T1–T7 work breakdown, staged-fix template with reverts; first attempt
      lost to the 32k turn cap, re-dispatched with small-pass discipline; plan now in `## Plan`).
- [x] `Tails` (attempt 4; T1-T7 all done and checkpointed in `## Implementation`; **fresh
       small-context session per item — never resume a session that has grown large**, that is
       itself a hot-wedge trigger): T4 distro comparison done, T5 correlation done (covers the
       Sep 12 wedges), T5-H2 repro done (WEDGED at 2.7 min on the stressed chip, hung job
       attributed to llama-server's own delta prefill; record + H2 adjudication input in
       `## Implementation` → "T5-H2 minimal repro"), T6 verdict done (2026-09-13: H1-H5
       verdicts, one-sentence trigger, distro answer, H2/H3 ambiguity weighed, staged solution
       table, `## Implementation` → "T6 adjudication"), staged fixes filled (`## Implementation`
       → "Staged, awaiting user approval", T7 corrections recorded), T7 fixes-doc update done
       (2026-09-13; backup `/tmp/qwen38-q5-fixes.md.bak.1789250153`; record `## Implementation`
       → "T7 checkpoint"). Never stop the service.
- [x] `Tails`: stage (do not execute) every restart/reboot-level fix with exact commands and
       step-by-step reverts under `## Implementation` → "Staged, awaiting user approval";
       update `/home/howard/AI/projects/qwen-38-q5-fixes/qwen38-q5-fixes.md` (pending since
       2026-08-27, now with the new findings). — done 2026-09-13 (T7): Stages 1-4 filled with
       backups + reverts, staged not applied; fixes doc updated; backup
       `/tmp/qwen38-q5-fixes.md.bak.1789250153`.
- [x] `Tails` (W1, window approved 2026-09-13; Stage 1 already applied externally at 17:51:56
      JST, provenance unverified; user kept `-c 98304` at 19:52 JST): DONE 2026-09-13 (fresh
      small-context Tails session). t/s verification vs the **iq4xs** baseline (not the Q4 11.87)
      **PASS**: live decode 11.95 t/s at ~57.9k context vs recorded baseline 12.1-12.3 t/s at
      ~58-60k (within ~3%, inside the 20% band); prefill 174.96 t/s; fingerprint b2000-5266f24d.
      Checkpoint in `## Implementation` ("W1 checkpoint: t/s verification vs the iq4xs baseline").
      No restart.
- [x] `Tails` (W2, window approved): apply Stage 3 per the staged section with the grub
      default set by **exact menuentry title** (Shadow blocker 1), then reboot. The Tails
      session dies with the endpoint; the "reboot issued" checkpoint must precede the command.
      DONE 2026-09-13 21:25 JST: default set by exact BLS identifier
      `aad6cfa1c71c461bbc6543c87712d7f1-7.2.5-1.el10.elrepo.x86_64` (BLS host; the blocker 1
      resolution's executable form of "exact entry identity"); checkpoint in `## Implementation`
      ("W2 checkpoint: Stage 3 applied, reboot issued").
- [x] `Tails` (W3): post-reboot verification (uname -r = 7.2.5, service active, 8093,
      llama.cpp version, wedge baseline) and start the bounded 24 h wedge monitor (pid
      recorded, hard stop). DONE 2026-09-13 22:45 JST (fresh small-context session): kernel
      7.2.5-1.el10.elrepo.x86_64, service active (user unit auto-start), 8093 listening,
      pid 1907, `-c 98304` intact, binary build 2000 / commit 5266f24d at
      /usr/local/bin/llama-server, wedge baseline 0 since boot; monitor pid 6647, log
      /tmp/wedge-monitor-20260913-224443.log, started 2026-09-13 22:44:43 JST, hard stop
      2026-09-14 22:44:43 JST; checkpoint in `## Implementation` ("W3 checkpoint").
- [x] `Shadow` → `Omega` → `Big` (2026-09-14): chain complete. Shadow attempt 2 done (no new
      blockers); Omega attempt 3 done (F1 high open, M1-M5 staged in `## Security`; F2 low); Big
      done (5/5 re-verification checks PASS, monitor still running). DoD gate pending F1 closure.
- [ ] `Tails` (citation refresh pass): fix the stale line citations routed by Shadow's attempt-2
      notes (doc-only, no machine change, no service actions); then one final `Shadow`
      verification pass over the refresh.
- [ ] `Robotnik`: check the 24 h monitor's final line after the hard stop (2026-09-14 22:44:43
      JST, log /tmp/wedge-monitor-20260913-224443.log) before Knuckles.
- [ ] `Vector`: update the `metalllinux/team-chaotix` README (EVO-X2 section) with the final
      root cause, fix status, and operational guidance (user requirement, 2026-09-12).
- [ ] `Knuckles`: verify the DoD checklist is fully ticked, then commit the planning doc +
      README and push to `metalllinux/team-chaotix` (user requirement, 2026-09-12).
- [ ] `Robotnik`: relay the staged solution + reverts to the user, now including Omega's M1-M5 in
      `## Security`: F1 closure needs M1 (`--api-key` in the unit, service restart window) and
      M2 (firewalld pin of 8093); also ask the user to check the router's 8093 port-forward
      status (F1 escalation condition). On approval, schedule the restart window (it kills
      in-flight opencode sessions; nothing dispatches during it).

---

## Plan

*Owner: `Amy`.*

**Framing.** This exists because EVO-X2 serves this team's only inference endpoint and the user
no longer accepts wedge risk (Status, 2026-09-12). It unblocks the Shadow/Omega/Big review chain
and the user's window decision for any staged fix; nothing blocks it except read-only access to
EVO-X2. MVP: attribution per the matrix below, the one-sentence trigger, and staged fixes with
reverts, nothing executed. Deferred: executing any staged fix (user window), a distro switch (only
if the matrix forces it), any frozen-flag change (user approval per DoD). What this makes harder:
until the wedge is fixed the team stays in the small-context safe regime, and every restart window
must run with zero dispatches in flight.

**Hard constraints.** `llama-server-qwen3.8-27b-iq4xs.service` is never stopped by the team (name
per the user; T1 verifies the real name and records it). No llama-server restart or host reboot
outside a user-approved window. Until the window: read-only probes plus reversible runtime
(logger/sysfs) changes only. Frozen flags (`-fa on`, q8_0 KV, `-c 262144`, `--parallel 1`) stay
unchanged.

**Hypothesis matrix.** Tails marks each row supported or excluded in `## Implementation` with the
deciding command and output.

| H | Candidate | Decision rule |
|---|---|---|
| H1 | kernel / amdgpu kmod `7.0.12-1.el10.elrepo` | Supported if the ring-reset signatures match a known amdgpu gfx1151 bug, or the staged newer-kernel test (Stage 3) removes the wedge under the same workload. Excluded if the wedge persists on the newer kernel with Mesa and llama.cpp unchanged. |
| H2 | Mesa RADV userspace | Supported if a bounded, non-llama RADV compute workload shaped like a ~201k cold prefill wedges the chip with llama.cpp out of the loop. Excluded if that run finishes clean while llama wedges on the same chip. |
| H3 | llama.cpp version + flags | Supported if the wedge rate changes when a frozen flag or the version is varied inside an approved window (staged; the user decides). Excluded if H2 reproduces the wedge without llama.cpp. `-fa on` is not toggleable: the q8_0 V-cache requires flash-attn. |
| H4 | systemd unit | Excluded as a wedge cause by construction (the unit manages lifecycle, it does not drive the GPU). Evaluate recovery behavior only: `Restart=`, `RestartSec=`, `TimeoutStartSec=`, memory limits, from the unit file and `systemctl --user show`. A slow reload is a Stage 1 unit edit, not a root cause. |
| H5 | heat / power | Supported if sensor history shows temperature at the limit or a throttle/fan event just before each wedge. Excluded if every wedge moment is well below the limit with no throttle. Runtime knobs are exhausted (2026-08-27, `low` rejected at 4.5x slower), so a H5 win points at workload shape (Stage 1) or kernel power management (Stage 3), not a sysfs knob. |

**Trigger (template; Tails confirms or rewords with the correlation).** "A single ~201k-token cold
prefill at the 120 W cap, sustained ~29 min, drives the Strix Halo iGPU (8060S, gfx1151) past the
amdgpu compute-ring reset threshold; no accumulated stress is required." Backed by the 2026-08-27
fresh-chip repro (rc=52, 1 wedge, 1760 s, `/tmp/run_end_repro201k_auto.txt`). Final sentence only
after the full wedge-timestamp list is correlated against sensor history (T3 + T2).

**Distro question (Rocky 10 vs Fedora vs NixOS; no Ubuntu).** T1 first establishes EVO-X2's
current distro and exact versions (do not assume: elrepo kernel in evidence suggests RHEL-family,
verify with `/etc/os-release`). Then T4 compares what each distro offers today, with real outputs:
- Rocky 10: `dnf repoquery` for kernel and mesa on base + elrepo (elrepo already supplies the
  running 7.0.12 kernel).
- Fedora (current stable): same `repoquery` against the Fedora repos, or the packages site if the
  repo is not reachable from EVO-X2.
- NixOS: nixpkgs stable kernel + mesa package versions.
Decision rule: the answer follows the matrix. If the winning fix is a kernel or Mesa version
obtainable on Rocky (elrepo or a rebuild), stay on Rocky and update the package (staged reboot).
A distro switch is recommended only if the required version is unobtainable on Rocky and a
self-build is unattractive. NixOS pins a known-good kernel + mesa pair declaratively but costs a
full reinstall of the model host (disk image first; that is the point of no return). Fedora is the
middle option: newer mesa/kernel than Rocky base, same RHEL tooling, cheaper switch (reinstall,
not migration).

**Read-only evidence checklist (order T1 to T5).** All via `ssh howard@192.168.1.106`; every item
is read-only or adds a reversible process; none touches the service.
1. T1: `cat /etc/os-release`; `uname -r`; `rpm -qa | grep -iE 'mesa|amdgpu|kernel'`;
   `vulkaninfo --summary`; the unit name/state; the llama.cpp command line from
   `/proc/<MainPID>/cmdline` and the server startup log version.
2. T1: the unit file content plus `systemctl --user show` for `Restart=`, `RestartSec=`,
   `TimeoutStartSec=`, memory limits.
3. T3: `journalctl -k --no-pager | grep -nE "device wedged"` (count + timestamps; the journal is
   JST = UTC+9, convert) and the full ±60 s context around each event for the ring-reset signature.
4. T2: one read of the amdgpu hwmon (temp/power/fan under `/sys/class/drm/card0/device/`), then a
   bounded background logger (5 s interval, append to a `/tmp` file, pid recorded in
   `## Implementation` so it can be killed at the end of T5 and is never orphaned).
5. T4: the three distro comparisons above, with the commands that produced each line.
6. T5: H2 minimal repro, only when no other dispatch is in flight, bounded to 15 min, wedge count
   taken before and after, and the repro killed immediately if the count increments.

**Staged fix template (T7 fills every cell from the T6 verdicts; nothing executes without a
user-approved window).**

| Stage | Change (fill) | Pre-change backup | Apply (exact commands) | Verify after | Revert (step by step) |
|---|---|---|---|---|---|
| 1. restart-level | flag change or unit recovery fix, only if H3 or H4-recovery wins | `cp <unit> /tmp/<unit>.bakN.$(date +%s)` + command line recorded in the doc | unit edit, `systemctl --user daemon-reload`, service restart inside the window | 24 h wedge count; t/s within 20% of baseline 11.87 | restore the backed-up unit, `daemon-reload`, restart inside the window |
| 2. package-level | Mesa/RADV or llama.cpp package, if H2 or H3 wins | `rpm -qa > /tmp/rpms.bakN` + the named rpm files copied to /tmp | `dnf` update of the named package, service restart inside the window | same as Stage 1 plus `vulkaninfo` version check | reinstall the backed-up rpm, restart inside the window |
| 3. reboot-level | newer kernel (elrepo or mainline) or a boot parameter named by the T3 evidence, if H1 or H5 wins | `rpm -qa kernel > /tmp/kernels.bakN` + current grub default recorded | install the kernel keeping the old one, set the new one default, reboot inside the window | 24 h wedge count on the new kernel under the same workload | `grub2-set-default` back to the old kernel entry, reboot (the old kernel was never removed) |
| 4. distro switch | NixOS or Fedora reinstall, only if the T4 matrix forces it | full disk image to external storage, checksum recorded | reinstall per the distro docs, redeploy model + user unit | 24 h wedge count + endpoint t/s | restore the disk image; keep the image until the switch has run clean for 2 weeks |

Rules for every stage: the backup location is recorded in `## Implementation`; the service is
restarted only inside the window and never stopped outside it; the old kernel/rpm is never removed
during the test window; Robotnik schedules the window with zero dispatches in flight.

**Work breakdown (one item per Tails turn; owner `Tails` throughout).**
- T1 checkpoint [wedge count + timestamps, the real service name and state, distro, kernel/mesa/
  llama.cpp versions + command line, unit file, all recorded in `## Implementation` within minutes
  of start].
- T2 sensor baseline + logger [baseline sample in the doc, logger pid recorded, logger stopped
  and confirmed stopped before T3 starts].
- T3 journal forensics [±60 s context for every wedge event in the doc, ring-reset signature
  classified, wedge timestamp list converted to UTC and final].
- T4 distro comparison [Rocky/Fedora/NixOS version table in the doc, each line with the command
  that produced it].
- T5 H2 minimal repro [bounded run, wedge count before/after, stop-on-wedge honored].
- T6 adjudication [each of H1-H5 marked supported or excluded with its deciding command, the
  one-sentence trigger written, the distro answer written].
- T7 staged fixes + fixes doc [all four stage rows filled with exact commands and reverts under
  `## Implementation` → "Staged, awaiting user approval"; the fixes doc
   `/home/howard/AI/projects/qwen-38-q5-fixes/qwen38-q5-fixes.md` updated].

Sequence: T1 → T2 → T3 → T4 → T5 → T6 → T7. T4 is independent of T2/T3/T5 (it may run in any
position after T1). T6 needs T2 through T5; T7 needs T6. After T7: `Shadow` → `Omega` → `Big`,
with Big re-verifying the cited evidence per the DoD.

**Rollback.** Detection: the wedge count (checklist item 3, run before and after every action),
in-flight stream errors in opencode, and service restarts in the user journal (system behavior;
count them, do not prevent them). Exact revert: per stage in the table above; the runtime logger
reverts with `kill <pid>` and log removal. Point of no return: only the Stage 4 disk-image path
(distro switch); the image is checksum-verified before the switch and kept for 2 weeks after.
Leftover state after a failed window: the model is cold (first generations slow) and the wedge
count may have risen; a retry must tolerate both, and every wedge inside the window counts toward
the baseline.

**Assumptions (verify in T1, flag any that fail).** EVO-X2 runs a RHEL-family distro (elrepo
kernel in the 2026-08-25 evidence); the service name is exactly
`llama-server-qwen3.8-27b-iq4xs.service`; the 120 W cap figure from 2026-08-27; the journal
timezone is JST (UTC+9).

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

Filled 2026-09-13 (T7) from the T6 adjudication verdicts (below, "T6 adjudication"); T7
corrections to the T6 draft cells are recorded in the "T7 checkpoint". Staged only; nothing
executed; the service is never stopped outside a user-approved window with zero dispatches in
flight; backups are taken before every change (paths recorded in this section); the old
kernel/rpm is never removed during the test window; Stages run in whatever order the user
approves ("live" = indicated by the T6 verdicts, "dormant" = only if earlier stages fail).

| Stage | Change | Pre-change backup | Apply (exact commands, inside the window) | Verify after | Revert (step by step) |
|---|---|---|---|---|---|
| 1. restart-level, llama.cpp (live: H3 not excluded) | llama.cpp version bump or user-approved flag change; frozen flags (`-fa on`, q8_0 KV, `-c 262144`, `--parallel 1`) stay unchanged unless the user approves a specific frozen-flag change; target version chosen and recorded at window time | `UNIT=$(systemctl --user show llama-server-qwen3.8-27b-iq4xs.service --value --property=FragmentPath)`; `cp "$UNIT" /tmp/llama-unit.bak1.$(date +%s)`; `tr '\0' ' ' < /proc/$(systemctl --user show llama-server-qwen3.8-27b-iq4xs.service --value --property=MainPID)/cmdline > /tmp/cmdline.bak1` (both backup paths recorded in this doc) | edit the unit's `ExecStart` for the chosen change (flag, or new binary path); `systemctl --user daemon-reload`; `systemctl --user restart llama-server-qwen3.8-27b-iq4xs.service` | 24 h wedge count under the same workload (`journalctl -k --no-pager \| grep -cE "device wedged"` before and after) and decode t/s within 20% of baseline 11.87 | `cp /tmp/llama-unit.bak1.<ts> "$UNIT"`; `systemctl --user daemon-reload`; restart inside the window; restore the old binary if one was swapped |
| 2. package-level, Mesa/RADV (live: H2 partially supported) | `dnf` update of `mesa-vulkan-drivers` (owns the RADV ICD; T1 record: installed `25.2.7-4.el10.rocky.0.1`); note per the T4 record: no Mesa newer than 25.2.7 is in any Rocky repo today, so if a specific newer Mesa version is the winning fix the switch target is Fedora 44 (Stage 4) | `rpm -qa > /tmp/rpms.bak2.$(date +%s)`; `PKG=$(rpm -qf /usr/share/vulkan/icd.d/radeon_icd.x86_64.json)` (verify the path at window time; if absent, take PKG from the T1 `rpm -qa \| grep -iE 'mesa'` listing); `dnf download --destdir=/tmp/rpmbak2 $PKG` (the exact installed version; file recorded in this doc) | `dnf update $PKG`; `systemctl --user restart llama-server-qwen3.8-27b-iq4xs.service` (the service loads libvulkan/ICD at startup) | same as Stage 1 plus `vulkaninfo --summary` shows the new RADV version | `dnf reinstall /tmp/rpmbak2/<backed-up rpm file>`; restart inside the window |
| 3. reboot-level, elrepo kernel 7.2.5 (live: H1 deciding test) | install the elrepo `kernel-ml` 7.2.5 keeping 7.0.12, set it default, reboot; the boot-parameter variant is not indicated from the record at hand (T3's classification governs) | `rpm -qa \| grep -E '^kernel' > /tmp/kernels.bak3.$(date +%s)`; `grub2-editenv list > /tmp/grubdefault.bak3` (current saved entry, recorded in this doc); `cp /etc/yum.repos.d/elrepo.repo /tmp/elrepo-kernel.repo.bak3` (resolved 2026-09-13: the repo file is `/etc/yum.repos.d/elrepo.repo`, the `[elrepo-kernel]` section, currently `enabled=0`; the host is BLS, so `grub2-editenv list` records `saved_entry=<BLS identifier>`) | enable the `[elrepo-kernel]` section of `/etc/yum.repos.d/elrepo.repo` (`enabled=0` -> `enabled=1`); `dnf install kernel-ml` (7.2.5; installonly keeps the old kernel; the kernel package creates the 7.2.5 BLS entry file); the host is BLS (no `menuentry` lines in `/boot/grub2/grub.cfg`; `GRUB_DEFAULT=saved`; `grubenv` holds `saved_entry`; verified 2026-09-13), so set the default by the exact BLS entry identifier, not a number: `N=$(ls /boot/loader/entries/*-7.2.5-1.el10.elrepo.x86_64.conf 2>/dev/null \| wc -l)` (must be 1 or stop); `BLSID=$(ls /boot/loader/entries/*-7.2.5-1.el10.elrepo.x86_64.conf \| head -1 \| xargs -n1 basename \| sed 's/\.conf$//')`; `grub2-set-default "$BLSID"`; `grub2-editenv list` (confirm `saved_entry=$BLSID`, the exact entry identifier); `reboot` | `uname -r` = `7.2.5-1.el10.elrepo.x86_64`; 24 h wedge count under the same workload on the new kernel | `OLDSAVED=$(grep '^saved_entry=' /tmp/grubdefault.bak3 \| cut -d= -f2-)` (the backup records the saved BLS identifier of the old default); `grub2-set-default "$OLDSAVED"` (valid: the old kernel's BLS file still exists, the old kernel was never removed); `grub2-editenv list` (confirm `saved_entry=$OLDSAVED`); `reboot`; `uname -r` = `7.0.12-1.el10.elrepo.x86_64`; restore the elrepo-kernel repo file (`/etc/yum.repos.d/elrepo.repo`) from its backup (or leave enabled, user's call) |
| 4. distro switch (dormant: only if Stages 1-3 all fail and the T4 matrix forces it) | NixOS or Fedora reinstall (choice per the T4 record: Fedora 44 middle option, NixOS 26.05 last resort); redeploy model + user unit | full disk image to external storage: `dd if=<root-disk device> of=/mnt/<external>/evox2-$(date +%F).img bs=8M status=progress`; `sha256sum` of the image recorded in this doc | reinstall per the distro docs; redeploy model + user unit | 24 h wedge count + endpoint t/s within 20% of 11.87 | `dd if=/mnt/<external>/evox2-<date>.img of=<root-disk device>`; keep the image until the switch has run clean for 2 weeks |

Rules carried from the plan (lines 547-549): the backup location is recorded in this section; the
service is restarted only inside the window and never stopped outside it; the old kernel/rpm is
never removed during the test window; Robotnik schedules the window with zero dispatches in
flight. Every wedge inside a window counts toward the baseline (plan rollback section).

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

### Attempt 4 (dispatched 2026-09-12, Tails)

**T1 checkpoint (2026-09-12 ~06:00 UTC / 14:5x JST). All probes read-only, via
`ssh howard@192.168.1.106`. Service never touched.**

**Assumption check (plan §Assumptions):** (1) RHEL-family distro: CONFIRMED, Rocky Linux 10.2
(Red Quartz), `platform:el10` (`cat /etc/os-release`). (2) Service name exactly
`llama-server-qwen3.8-27b-iq4xs.service`: CONFIRMED (user-level unit, see below). (3) 120 W cap:
not yet re-verified (T2 hwmon). (4) Journal timezone JST/UTC+9: CONFIRMED, `timedatectl` →
`Time zone: Asia/Tokyo (JST, +0900)`.

**Distro / kernel.** `uname -r` → `7.0.12-1.el10.elrepo.x86_64` (rpm
`kernel-ml-7.0.12-1.el10.elrepo`; same elrepo ml kernel as the 2026-08-25/27 evidence). Base
Rocky kernels `6.12.0-211.16.1.el10_2.0.1` and `6.12.0-211.22.1.el10_2` also installed. Kernel
command line (this boot): `amd_iommu=off amdgpu.gttsize=90112 ttm.pages_limit=23068672
ttm.page_pool_size=23068672 amdgpu.no_system_mem_limit=1` (+ `rhgb quiet`, crashkernel, lvm,
resume). Boot: `uptime -s` → `2026-09-12 12:47:07` JST = **03:47:07 UTC**; uptime 2:03 at 05:50
UTC. The 2026-08-26 and today's reboots have no recorded approval in this doc (provenance
unverified, per the standing pattern).

**Mesa / Vulkan.** `rpm -qa | grep -iE 'mesa|amdgpu'` → `mesa-vulkan-drivers-25.2.7-4.el10.rocky.0.1`
(+ `mesa-filesystem-25.2.7-4.el10.rocky.0.1`). `vulkaninfo --summary` → GPU0 `Radeon 8060S
Graphics (RADV GFX1151)`, deviceID `0x1586`, INTEGRATED_GPU, `DRIVER_ID_MESA_RADV`,
`driverInfo: Mesa 25.2.7`, Vulkan API 1.4.318; GPU1 llvmpipe.

**llama.cpp.** `/usr/local/bin/llama-server --version` → `version: 9671 (c1304d7b2)`, built with
GNU 14.3.1. Not an rpm: `/usr/local/bin/` install (llama.cpp full toolchain present).

**Service (real name + state).** `llama-server-qwen3.8-27b-iq4xs.service` — user-level unit at
`/home/howard/.config/systemd/user/` (549 B, mtime Sep 9 02:26). `systemctl --user list-units`
→ `loaded active running`, `UnitFileState=enabled`. `systemctl --user show` → `MainPID=1826`,
`ExecMainStartTimestamp=Sat 2026-09-12 12:47:15 JST` (8 s after boot), `NRestarts=0`,
`Result=success`, `Restart=on-failure`, `RestartSec=5`, no `TimeoutStartSec` override,
`MemoryMax=infinity`, `LimitMEMLOCK=infinity`. MainPID cmdline (from `/proc/1826/cmdline`,
matches unit `ExecStart`):
`/usr/local/bin/llama-server --model /mnt/data/models/qwen3.8-27b-iq4xs/Qwen3.8-27B-UD-IQ4_XS.gguf
--mmproj /mnt/data/models/qwen3.8-27b-iq4xs/mmproj-F16.gguf --alias Qwen3.8-27B-UD-IQ4_XS
--host 0.0.0.0 --port 8093 --n-gpu-layers 99 -fa on --parallel 1 -t 32 -tb 32 -ub 2048
-ctk q8_0 -ctv q8_0 --mlock -c 262144`. Frozen flags (`-fa on`, q8_0 KV, `-c 262144`,
`--parallel 1`) intact. New vs the 2026-08-27 unit: `-mmproj` (multimodal) added; user-journal
startup log confirms multimodal model loaded.

**Unit file (full, `/home/howard/.config/systemd/user/llama-server-qwen3.8-27b-iq4xs.service`):**
```
[Unit]
Description=Llama server for Qwen3.8-27B-UD-IQ4_XS
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
LimitMEMLOCK=infinity
ExecStart=/usr/local/bin/llama-server --model /mnt/data/models/qwen3.8-27b-iq4xs/Qwen3.8-27B-UD-IQ4_XS.gguf --mmproj /mnt/data/models/qwen3.8-27b-iq4xs/mmproj-F16.gguf --alias Qwen3.8-27B-UD-IQ4_XS --host 0.0.0.0 --port 8093 --n-gpu-layers 99 -fa on --parallel 1 -t 32 -tb 32 -ub 2048 -ctk q8_0 -ctv q8_0 --mlock -c 262144
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
```
Older sibling units (q4/q5/q6/q8/qwen3.6/gemma4/deepseek-coder) exist in the same directory but
are inactive; only the iq4xs unit is running. H4 (unit as wedge cause) is excluded by
construction per the matrix; recovery behavior = `Restart=on-failure` + `RestartSec=5` (wedge →
llama-server dies → systemd restarts it in ~5 s, matching the 2026-08-27 observed ~5-11 s
restarts).

**Wedge count (T1 scope: current boot).** `journalctl -k --no-pager -b -0 | grep -cE "device
wedged"` → **0** since the 2026-09-12 03:47:07 UTC boot. Three milder `Fence fallback timer
expired on ring comp_1.2.0` events in boot 0 (two at Sep 12 14:45:10 / 14:45:43 JST, ~5 min
before this checkpoint; third pending T3). No full wedge in the current boot so far.

**Journal availability (critical for T3).** Per-boot kernel journals are queryable for boots
-7..0 (command: `journalctl -k -b N --no-pager | grep -cE "device wedged"` per boot):

| boot | span (JST) | wedges | fence fallbacks |
|---|---|---|---|
| -7 | Aug 25 21:11:16 → 21:20:14 | 0 | 0 |
| -6 | Aug 25 21:20:21 → 21:40:14 | 0 | 0 |
| -5 | Aug 25 21:40:21 → Aug 26 21:25:07 | 0 | 2 |
| -4 | Aug 26 21:25:14 → Aug 27 15:55:09 | 5 | 10 |
| -3 | Aug 27 17:00:47 → Sep 03 17:11:57 | 33 | 25 |
| -2 | Sep 05 13:04:49 → Sep 06 14:22:19 | 4 | 5 |
| -1 | Sep 06 14:22:27 → Sep 10 05:53:44 | 9 | 15 |
| 0 | Sep 12 12:47:10 → now | 0 | 3 |

Total in journal: **51 full wedges, 58 fence fallbacks** (58 corrected in T3 checkpoint). Boot -4 matches the 2026-08-27 02:45
UTC Status entry (5 events). Boot -3 contains the 2026-08-27 ~201k repro burst (19:46 JST) and
ran 7 days. Gaps (machine off): Sep 03 17:11 → Sep 05 13:04, Sep 10 05:53 → Sep 12 12:47 JST.
Journal files pre-Aug 16 (2026-08-23/24 boots with the 26+ wedges from the 2026-08-25 evidence)
are gone; that history stands only as recorded in the 2026-08-25/27 checkpoints. Caveat:
unbounded `journalctl -k` returns only boot 0 (1238 lines) on this host, while `journalctl`
(all facilities) reaches back to Jun 16 and per-boot `-b N -k` works for all listed boots — T3
therefore queries per boot, never unbounded.

**Next:** T2 sensor baseline + bounded logger (plan checklist item 4).

**T2 checkpoint (2026-09-12 ~06:33 UTC / 15:3x JST).** Read-only probes + the plan-permitted
bounded logger. Service untouched; nothing written on EVO-X2 outside `/tmp`.

**hwmon layout** (probe: `readlink -f /sys/class/drm/card0/device/hwmon/hwmon*` →
`/sys/devices/pci0000:00/0000:00:08.1/0000:c4:00.0/hwmon/hwmon2`, `name=amdgpu`):

| entry | value (baseline) | unit |
|---|---|---|
| `temp1_input` (label `edge`) | 65000 | m°C = 65.0 °C |
| `power1_input` (label `PPT`) | 96015000 | µW = 96.0 W |
| `power1_average` | 96029000 | µW |
| `freq1_input` (label `sclk`) | 2445000000 | Hz = 2445 MHz |
| `in0_input`/`in1_input` (vddgfx/vddnb) | 0 | not exposed |
| fan* | **absent** | no fan entry in hwmon |
| power1_max / power cap | **absent** | consistent with attempt 3 ("no power-cap hwmon entry"); the "120 W cap" is a firmware (STAPM) plateau, not a sysfs max |

**Baseline sample (the one read, 15:31 JST):** edge 65.0 °C, PPT 96.0 W (avg 96.03 W), sclk
2445 MHz. The sample caught an active decode burst (this session's own inference runs on the
endpoint): logger rows 5 s apart show the full oscillation — `67.0 °C / 98.03 W / 2491 MHz`
then `52.0 °C / 4.08 W / 613 MHz`. Idle floor ≈ 4 W / 613 MHz; active decode ≈ 98 W / ~2.5 GHz
at the moment sampled.

**Bounded logger (running now).**
- Script: `/tmp/t2_sensor_logger.sh` (on EVO-X2, 1086 B, `chmod +x`), read-only cats of
  `temp1_input`, `power1_input`, `power1_average`, `freq1_input` + per-iteration
  `journalctl -k -b -0 | grep -cE "device wedged"` (real-time wedge detection for T5).
- Log: `/tmp/t2_sensor_log.csv`, header
  `ts_epoch,jst,temp1_mC,ppt_mW,ppt_avg_mW,sclk_Hz,wedges_boot0`, 5 s interval, append-only.
- Launch (exact): `nohup bash /tmp/t2_sensor_logger.sh >/dev/null 2>&1 & echo $! > /tmp/t2_sensor_log.pid`
- **PID: 4119** (user `howard`, PPID 4095, launched 15:31 JST).
- Hard stop: built-in `MAX_SECS=14400` (4 h) self-terminates with a marker line, so the logger
  can never be orphaned even if not manually killed.
- Kill command (for T3 start / T5 end): `kill "$(cat /tmp/t2_sensor_log.pid)"` then confirm
  `ps -p $(cat /tmp/t2_sensor_log.pid)` is empty and the last CSV line is the stop marker or a
  constant wedge count.
- Verified running and killable: `ps -o pid,ppid,user,etime,cmd -p 4119` →
  `4119 4095 howard 00:08 bash /tmp/t2_sensor_logger.sh`; `kill -0 4119` → pass (signal-0
  permission check, does not kill); CSV grew header → 2 rows in 8 s at 5 s cadence.
- Status at checkpoint: **running, will be stopped and confirmed stopped before T3 starts**
  (work-breakdown T2 acceptance).

**T3 checkpoint (2026-09-12 ~07:05 UTC / 16:0x JST).** Read-only journal forensics. First action:
logger killed and confirmed stopped — `kill "$(cat /tmp/t2_sensor_log.pid)"` (pid 4119),
`ps -p 4119` empty, CSV final 103 lines (15:31:55–15:40:24 JST, 0 wedges in window). Service
untouched throughout.

**Method.** Per-boot kernel journals dumped on EVO-X2 to `/tmp/t3_kernel_bootN.txt`
(`journalctl -k -b N --no-pager`), pulled locally; per-wedge workload context from
`journalctl --user -b N -u llama-server-qwen3.8-27b-q4.service --since @epoch --until @epoch`
windows (±2–15 min) around all 51 wedge timestamps. All queries read-only.

**Signature classes (51 full wedges + 58 fence fallbacks in journal).**

| class | count | kernel sequence |
|---|---|---|
| A: ring reset recovered | 47 | `ring comp_1.x.0 timeout, signaled seq=S, emitted seq=S+2` → `Process llama-server pid P thread llama-server pid P` → `Starting comp_1.x.0 ring reset` → `reset compute queue (x)` → `Ring comp_1.x.0 reset succeeded` → `[drm] device wedged, but recovered through reset` |
| B: ring reset failed → full GPU reset | 4 (all boot -3) | same start, then `Ring comp_1.2.0 reset failed` → `GPU reset begin!. Source:  1` → `GPU reset succeeded, trying to resume` → `GPU reset(N) succeeded!` → `[drm] device wedged, but recovered through reset` (N = 1, 14, 18, 30) |
| C: fence fallback (mild, no reset) | 58 | `Fence fallback timer expired on ring comp_1.x.0` |

Rings: 11 on `comp_1.1.0`, 40 on `comp_1.2.0`; all compute rings. Every full wedge also precedes
`Dumping IP State` + `AMDGPU device coredump file has been created`
(`/sys/class/drm/card0/device/devcoredump/data`, not read). **Userspace, identical in all 51:**
`radv/amdgpu: The CS has been cancelled because the context is lost. This context is innocent.`
→ `terminate called after throwing an instance of 'vk::DeviceLostError'`
(`vk::Queue::submit: ErrorDeviceLost`) → SIGABRT, `Main process exited, code=dumped,
status=6/ABRT`, `Failed with result 'core-dump'`. Crash backtrace (sample, boot -3 12:36:14):
`common_prompt_checkpoint::update_tgt → llama_context::state_seq_get_data →
llama_io_write_host → ggml_backend_sched_graph_compute_async`. llama.cpp 9671 does not handle
`VK_ERROR_DEVICE_LOST` and aborts; the Vulkan device is destroyed by the ring reset, the abort is
a consequence, not a cause. **±60 s context (checked programmatically across all 5 boot dumps):
zero non-amdgpu kernel lines within ±60 s of any of the 51 wedges** — no PCIe/AER, no thermal, no
OOM, no power events; each wedge is a self-contained amdgpu ring-level event.

**Final UTC wedge list (JST = UTC+9; ring: 1.1 = comp_1.1.0, 1.2 = comp_1.2.0).**

boot -4 (Aug 26 21:25:14 → Aug 27 15:55:09 JST; Q4 service):

| # | JST | UTC | ring | class | pid | state at wedge (last user-journal evidence) |
|---|---|---|---|---|---|---|
| 1 | Aug 27 10:08:08 | 01:08:08 | 1.1 | A | 1817 | hot: long decode done (3689 tok @ 8.07 t/s, 457 s), new task just launched |
| 2 | Aug 27 10:36:48 | 01:36:48 | 1.2 | A | 4369 | cold ~198k prefill, n=178176 p=0.88, t=1696 s, 105 t/s |
| 3 | Aug 27 10:37:18 | 01:37:18 | 1.2 | A | 4369 | same prefill 30 s later, n=180224 p=0.89 (process survived reset 2) |
| 4 | Aug 27 11:05:28 | 02:05:28 | 1.2 | A | 4478 | cold ~198k prefill, n=176128 p=0.87, t=1665 s |
| 5 | Aug 27 11:33:17 | 02:33:17 | 1.2 | A | 4596 | cold ~198k prefill, n=174080 p=0.86, t=1631 s (TASK-0008 2c session died to this one, 02:33:18 UTC) |

boot -3 (Aug 27 17:00:47 → Sep 3 17:11:57 JST; Q4 service, 7 days):

| # | JST | UTC | ring | class | pid | state at wedge |
|---|---|---|---|---|---|---|
| 1 | Aug 27 19:46:26 | 10:46:26 | 1.1 | **B** | 1852 | cold ~201k repro prefill (Tails attempt 3, manual llama-server), n=186368 p=0.97, t=1738 s |
| 2 | Aug 27 19:46:39 | 10:46:39 | 1.1 | A | 13022 | 13 s later, q4 service process, same prefill p=0.97 |
| 3 | Aug 28 02:41:22 | Aug 27 17:41:22 | 1.1 | A | 13071 | hot: decode done (409 tok @ 8.07 t/s), task 191004 launched 11 s earlier |
| 4 | Aug 28 03:11:38 | 18:11:38 | 1.2 | A | 14120 | cold ~204k prefill, n=190464 p=0.91, t=1773 s |
| 5 | Aug 28 03:42:04 | 18:42:04 | 1.2 | A | 14243 | cold ~204k prefill, n=190464 p=0.91, t=1774 s |
| 6 | Aug 28 12:36:14 | 03:36:14 | 1.2 | A | 14347 | hot: incremental prefill done (2255 tok, 4 s) vs ~185k context, 6 s later |
| 7 | Aug 28 13:05:34 | 04:05:34 | 1.2 | A | 15483 | cold ~184k prefill, n=184320 p=0.98, t=1714 s |
| 8 | Aug 28 13:34:46 | 04:34:46 | 1.2 | A | 15599 | cold ~184k prefill, n=184320 p=0.98, t=1715 s |
| 9 | Aug 28 16:52:57 | 07:52:57 | 1.1 | A | 15709 | hot: decode done (2335 tok @ 7.95 t/s, 294 s), task 78309 launched 5 s earlier |
| 10 | Aug 28 17:23:43 | 08:23:43 | 1.2 | A | 16132 | cold ~209k prefill, n=192512 p=0.90, t=1803 s |
| 11 | Aug 28 17:54:56 | 08:54:56 | 1.2 | A | 16256 | cold ~209k prefill, n=194560 p=0.91, t=1836 s |
| 12 | Aug 28 19:59:14 | 10:59:14 | 1.2 | A | 16371 | cold ~209k prefill, n=194560 p=0.91, t=1834 s |
| 13 | Aug 28 20:30:59 | 11:30:59 | 1.2 | A | 16606 | cold ~209k prefill, n=196608 p=0.92, t=1865 s |
| 14 | Aug 28 21:02:08 | 12:02:08 | 1.2 | **B** | 16732 | cold ~209k prefill, n=194560 p=0.91, t=1832 s → ring reset failed → GPU reset(14) |
| 15 | Aug 28 21:32:49 | 12:32:49 | 1.2 | A | 16890 | cold ~209k prefill, n=184320 p=0.86, t=1710 s |
| 16 | Aug 28 22:04:27 | 13:04:27 | 1.2 | A | 17008 | cold ~209k prefill, n=194560 p=0.91, t=1834 s |
| 17 | Aug 31 00:55:38 | Aug 30 15:55:38 | 1.2 | A | 17168 | hot: incremental prefill done (6950 tok, 77 s) vs ~188k context, 10 s later |
| 18 | Aug 31 01:25:57 | 16:25:57 | 1.2 | **B** | 22325 | cold ~185k prefill, n=189852 p=1.00, t=1769 s → ring reset failed → GPU reset(18) |
| 19 | Aug 31 01:58:41 | 16:58:41 | 1.2 | A | 22442 | hot: incremental prefill in flight (4098 tok p=0.98, 33 s) vs ~191k context |
| 20 | Aug 31 02:30:14 | 17:30:14 | 1.1 | A | 22570 | cold ~195k prefill, n=195295 p=0.98, t=1852 s |
| 21 | Aug 31 03:00:29 | 18:00:29 | 1.2 | A | 22686 | cold ~194k prefill, n=190464 p=0.96, t=1775 s |
| 22 | Aug 31 04:40:40 | 19:40:40 | 1.2 | A | 22797 | hot: incremental prefill done (5123 tok, 50 s) vs ~193k context, 6 s later |
| 23 | Aug 31 05:11:42 | 20:11:42 | 1.1 | A | 23030 | cold ~192k prefill, n=192343 p=0.98, t=1803 s |
| 24 | Aug 31 05:12:13 | 20:12:13 | 1.2 | A | 23030 | 31 s later, same process, prefill p=1.00 (re-wedge) |
| 25 | Aug 31 05:40:50 | 20:40:50 | 1.2 | A | 23169 | cold ~191k prefill, n=184320 p=0.94, t=1680 s |
| 26 | Aug 31 07:55:34 | 22:55:34 | 1.2 | A | 23285 | hot: incremental prefill done (5894 tok, 63 s) vs ~196k context, 6 s later |
| 27 | Aug 31 07:55:42 | 22:55:42 | 1.2 | A | 23285 | 8 s later, same process (re-wedge) |
| 28 | Aug 31 08:27:55 | 23:27:55 | 1.2 | A | 23557 | cold ~194k prefill, n=198264 p=1.00, t=1893 s |
| 29 | Aug 31 08:59:08 | 23:59:08 | 1.1 | A | 23671 | cold ~194k prefill, n=194420 p=0.98, t=1832 s |
| 30 | Aug 31 18:00:55 | 09:00:55 | 1.2 | **B** | 23795 | hot: decode done (5807 tok @ 7.72 t/s, 752 s), task 208767 launched 5 s earlier → ring reset failed → GPU reset(30) |
| 31 | Aug 31 18:31:49 | 09:31:49 | 1.2 | A | 24675 | cold ~224k prefill, n=192512 p=0.84, t=1807 s |
| 32 | Aug 31 19:02:02 | 10:02:02 | 1.2 | A | 24786 | cold ~224k prefill, n=190464 p=0.83, t=1776 s |
| 33 | Sep 01 00:34:30 | Aug 31 15:34:30 | 1.2 | A | 25004 | cold ~188k prefill, n=188416 p=0.98, t=1748 s (last full wedge of boot) |

boot -2 (Sep 5 13:04:49 → Sep 6 14:22:19 JST; Q4 service):

| # | JST | UTC | ring | class | pid | state at wedge |
|---|---|---|---|---|---|---|
| 1 | Sep 05 23:19:44 | 14:19:44 | 1.1 | A | 3080 | hot: decode done (3788 tok @ 8.28 t/s, 457 s), incremental prefill (2797 tok, 13 s) vs ~186k context, 6 s later |
| 2 | Sep 05 23:51:00 | 14:51:00 | 1.2 | A | 3928 | cold ~184k prefill, n=188829 p=1.00, t=1834 s |
| 3 | Sep 06 00:22:17 | 15:22:17 | 1.2 | A | 4046 | cold ~184k prefill, n=188829 p=1.00, t=1834 s |
| 4 | Sep 06 14:03:34 | 05:03:34 | 1.2 | A | 4185 | cold ~184k prefill, n=186368 p=0.99, t=1787 s |

boot -1 (Sep 6 14:22:27 → Sep 10 05:53:44 JST; Q4 service until Sep 8 17:32 UTC, then q4+
iq4xs concurrent):

| # | JST | UTC | ring | class | pid | state at wedge |
|---|---|---|---|---|---|---|
| 1 | Sep 08 00:35:39 | Sep 07 15:35:39 | 1.1 | A | 1826 | cold ~190k prefill, n=192512 p=0.99, t=1809 s |
| 2 | Sep 08 01:07:08 | 16:07:08 | 1.2 | A | 5593 | cold ~190k prefill, n=194726 p=1.00, t=1844 s |
| 3 | Sep 08 01:37:54 | 16:37:54 | 1.2 | A | 5723 | cold ~190k prefill, n=192512 p=0.99, t=1809 s |
| 4 | Sep 08 23:18:35 | 14:18:35 | 1.1 | A | 6459 | hot: decode done (6378 tok @ 8.19 t/s, 778 s), incremental prefill (2372 tok, 6 s) vs ~193k context, 11 s later |
| 5 | Sep 08 23:48:58 | 14:48:58 | 1.2 | A | 8226 | cold ~190k prefill, n=190464 p=0.98, t=1777 s |
| 6 | Sep 09 00:19:46 | 15:19:46 | 1.2 | A | 8326 | cold ~190k prefill, n=192512 p=0.99, t=1811 s |
| 7 | Sep 09 01:07:43 | 16:07:43 | 1.2 | A | 8461 | cold ~192k prefill, n=190464 p=0.97, t=1778 s |
| 8 | Sep 09 01:38:38 | 16:38:38 | 1.2 | A | 8614 | cold ~192k prefill, n=192512 p=0.98, t=1812 s |
| 9 | Sep 09 02:07:19 | 17:07:19 | 1.2 | A | 8723 | cold ~191k prefill, n=184320 p=0.94, t=1684 s |

boot 0: 0 wedges (3 fence fallbacks: Sep 12 14:45:10, 14:45:43 JST, +1 earlier, all comp_1.2.0).

**Workload findings (what was happening in each window).**
1. **All 51 wedges ran under `llama-server-qwen3.8-27b-q4.service`** (Q4_K_XL). Every wedge is
   followed by a `Started llama-server-qwen3.8-27b-q4` line 5–7 s later (`Restart=on-failure` +
   `RestartSec=5`). Four extra `Stopped`+`Started` pairs (Aug 28 21:04:03, 22:08:25; Aug 31
   19:32:05; Sep 2 10:46:27 JST) are manual restarts, not wedges.
2. **Two wedge modes.** (a) **Cold (39):** a fresh ~185–224k-token prompt prefill (client
   resends its full context), wedged at t = 1568–1893 s (26.1–31.6 min) into the prefill, at
   84–100% progress, sustained ~103–110 t/s (first 7 s burst ~585 t/s). (b) **Hot (12):** a new
   task's incremental prefill (2–7k new tokens) against a slot context already at ~185–196k
   tokens (after 5–13 min of continuous decode @ ~7.7–8.3 t/s), wedged ~5–77 s after task
   launch. Three cold-window "(none)" prefill cases (boot -3 #3, #9, #30) resolve to hot mode:
   `launch_slot_` logged 5–11 s before the wedge, the first prefill line lands at/after it.
3. **Accumulation lowers the threshold.** Fresh process/chip: wedge at ~29 min of cold prefill
   (Aug 27 19:46 burst, 201k repro). After 3–12 h of accumulated sustained compute: wedge within
   ~5–11 s of a new task. The trigger is sustained full-power compute with total context
   ≥ ~185k tokens, with accumulated load state deciding where in the workload it fires.
4. **The same ~200k prompt is resubmitted after every restart** — the first post-restart line is
   uniform across all 51 events (`n_tokens = 4096, progress = 0.02, ~585 t/s` → total ≈ 204,800
   tokens): the client (opencode session context) re-sends its full context, so a wedge cycle
   re-arms the identical workload.
5. **~30-min cadence** inside clusters (inter-wedge 28–48 min, e.g. Sep 8 23:18–Sep 9 02:07:
   30m23/30m48/47m57/30m55/28m41 s) = the dispatch cycle re-arming the 200k prefill.
6. **iq4xs (the current service) has wedged zero times**: it started Sep 8 17:32 UTC (boot -1)
   and has run through the rest of boot -1 and all of boot 0 with zero wedges — but under the
   small-context safe-regime workload only; not yet a clean exoneration of the workload shape.
   On boot 0 the legacy q4 unit was **manually stopped** at Sep 12 12:55:06 JST (03:55:06 UTC),
   8 min after boot (`Reload requested from client PID 2980 ('systemctl')` + stop), provenance
   unverified, not a wedge.

**Correction to T1 checkpoint:** total fence fallbacks is **58** (10+25+5+15+3), not 60.

**Next:** T4 distro comparison (Rocky/Fedora/NixOS kernel + Mesa versions, per plan).

**T4 checkpoint (2026-09-12 ~10:20 UTC / 19:20 JST).** Read-only distro comparison per plan
checklist item 5. No packages installed, no repo config changed (`--enablerepo` and
`--repofrompath` are per-invocation, nothing persisted on EVO-X2), service untouched
throughout. Only this doc was modified.

**Version table** (running, per T1: kernel `7.0.12-1.el10.elrepo` = kernel-ml, Mesa
`25.2.7-4.el10.rocky.0.1` RADV on gfx1151).

| distro | kernel, newest reachable | mesa, newest reachable | vs running |
|---|---|---|---|
| Rocky 10.2 base (baseos/appstream) | `6.12.0-211.54.1.el10_2` (22 point releases, .16.1-.54.1) | `25.2.7-4.el10.rocky.0.1` | kernel older; mesa identical |
| Rocky + elrepo-kernel (repo file present, **currently disabled**) | `kernel-ml 7.2.5-1.el10.elrepo` (7.2.4 also in metadata; elrepo keeps only the recent window) | none (no mesa in elrepo, none in epel) | kernel newer (2 minor versions ahead) |
| Fedora 44 (current stable) | `6.19.10-300.fc44` | `26.0.3-4.fc44` (vulkan-drivers, dri-drivers, libEGL, libGL, libgbm) | kernel older; mesa ~8 minor versions ahead |
| NixOS 26.05 (current stable) | default `6.18` LTS (`linux_default`); `7.2.4` available as `linux_latest` | `26.1.8` | default older; latest ~level with elrepo (1 patch behind) |

**Commands and key outputs** (all via `ssh howard@192.168.1.106` unless noted):

- Rocky repos: `dnf repolist --enabled` → appstream, baseos, elrepo, epel, extras.
  `dnf repolist all | grep elrepo` → `elrepo` enabled; `elrepo-extras`, `elrepo-kernel`,
  `elrepo-testing` **disabled**. The installed `kernel-ml-7.0.12-1.el10.elrepo`
  (`rpm -qa | grep ^kernel`) came from `elrepo-kernel`, which is why `dnf repoquery kernel-ml`
  on the enabled repos returns empty.
- Rocky mesa: `dnf repoquery --qf "%{name} %{version}-%{release} (%{repoid})" "mesa*"` →
  mesa-dri-drivers/-libEGL/-libGL/-libgbm/-vulkan-drivers/-filesystem all
  `25.2.7-4.el10.rocky.0.1` (appstream); mesa-compat-libOSMesa/-libxatracker `25.0.7-2.el10.0.1`.
  `dnf repoquery --repo=elrepo "mesa*"` and `--repo=epel "mesa*"` → both empty.
- Rocky kernel: `dnf repoquery --qf "%{name} %{version}-%{release} (%{repoid})" kernel` →
  baseos, newest `6.12.0-211.54.1.el10_2`. `dnf --enablerepo=elrepo-kernel repoquery --qf
  "%{name} %{version}-%{release} (%{repoid})" kernel-ml` → `kernel-ml 7.2.5-1.el10.elrepo
  (elrepo-kernel)`.
- Fedora release ID: `curl -sI .../pub/fedora/linux/releases/44/Everything/x86_64/os/repodata/repomd.xml`
  → 302 to a mirror (repo present); releases 45/46/47 → 404; `.treeinfo` confirms family Fedora,
  release 44. So 44 is the current stable.
- Fedora versions: `dnf --disablerepo="*" --repofrompath=f44,https://download.fedoraproject.org/pub/fedora/linux/releases/44/Everything/x86_64/os/ repoquery --qf "%{name} %{version}-%{release} (%{repoid})" kernel`
  → `kernel 6.19.10-300.fc44` (metadata downloaded fresh, 15 MB). Same invocation with `"mesa*"`
  → `mesa-vulkan-drivers 26.0.3-4.fc44` (RADV lives here on Fedora), plus mesa-dri-drivers/
  libEGL/libGL/libgbm `26.0.3-4.fc44`. There is no top-level `mesa` package on Fedora.
- NixOS stable: `curl -s https://api.github.com/repos/NixOS/nixpkgs/tags?per_page=100` → newest
  stable tag `26.05` (`26.11-pre` is dev). (`releases.nixos.org/nixos/` → 404; the channels page
  is JS-rendered, so the GitHub API is the machine-readable source.)
- NixOS mesa: `nixos-26.05: pkgs/development/libraries/mesa/common.nix` → `version = "26.1.8"`.
- NixOS kernel: `nixos-26.05: pkgs/top-level/linux-kernels.nix:737-739` →
  `linux_default = packages.linux_6_18; linux_latest = packages.linux_7_2;`;
  `pkgs/os-specific/linux/kernel/kernels-org.json` → `"7.2": {"version": "7.2.4", "lts": false}`;
  `nixos/modules/system/boot/kernel.nix:61` → boot default `pkgs.linuxPackages` (the standard
  kernel, i.e. `linux_default` = 6.18 LTS; 7.2.4 is declaratively selectable).

**Decision-rule outcome** (plan §Distro question, applied to the table):

- **H1 (kernel is the fix):** a kernel newer than 7.0.12 **is obtainable on Rocky**: kernel-ml
  7.2.5-1.el10.elrepo in elrepo-kernel. Caveat of record: the elrepo-kernel repo file is on the
  host but disabled, so the package is not visible to `dnf` until the repo is enabled; that is a
  one-line reversible config change, part of the Stage 3 apply step. 7.2.5 is also the newest
  kernel of all four rows (Fedora 6.19.10 and NixOS default 6.18 are older than what is running;
  NixOS `linux_latest` 7.2.4 is one patch behind elrepo). **Stay on Rocky, staged reboot.**
- **H2 (Mesa is the fix):** any Mesa newer than 25.2.7 is **not obtainable on Rocky from any
  repo** (appstream frozen at 25.2.7, no mesa in elrepo or epel); the only Rocky path is a
  self-build, which the rule treats as unattractive. If T6 names a Mesa version as the winning
  fix, the switch target is **Fedora 44** (Mesa 26.0.3, same RHEL tooling, reinstall not
  migration). **NixOS 26.05** (Mesa 26.1.8, declarative kernel 7.2.4 pin) only if a version
  beyond 26.0.3 is required, at the cost of a full reinstall of the model host (Stage 4, disk
  image first, point of no return).
- **H3 (llama.cpp/flags):** source build in /usr/local, not a repo package; no distro impact.

**Distro recommendation:** stay on Rocky 10.2. On the kernel axis a distro switch is not
justified at all: the fix version (7.2.5) is reachable on Rocky and is newer than what Fedora
44 or NixOS 26.05 ship by default. On the Mesa axis a switch is only on the table if T6
exonerates the kernel and names a Mesa version; then Fedora 44 is the recommended middle
option and NixOS 26.05 the last resort.

**Next:** T5 H2 minimal repro (bounded 15 min, only when no other dispatch is in flight,
wedge count before and after, stop-on-wedge honored).

### T5-correlation (2026-09-12 ~09:40 UTC / 18:40 JST, Tails)

Read-only correlation of today's 3 wedges with the llama-server user journal. No service
touch; no writes on EVO-X2. Commands (all via `ssh howard@192.168.1.106`, JST times):
- `journalctl -k -b -0 --no-pager | grep -B6 -A2 "device wedged"` (wedge times, rings, pids)
- `journalctl --user -u llama-server-qwen3.8-27b-iq4xs.service --since ... --until ...` for
  17:19-17:24, 17:30-18:00, 18:00-18:25 JST, filtered with
  `grep -E "print_timing|launch_slot|all slots|Main process|Started llama|model loaded|Failed with result"`
- Boot-0 request sequence: same unit, 12:47-17:25 JST, filtered with
  `grep -E "model loaded|n_tokens = +4096, progress|launch_slot_|Main process|Started llama-server|Stopped llama-server"`

**Per-wedge table.**

| Wedge (JST / UTC) | Kernel (ring, pid) | In flight at wedge (user journal) | Prompt size | Cached fraction | Client |
|---|---|---|---|---|---|
| 17:22:22 / 08:22:22 | comp_1.1.0, pid 1826 | task 169934, launched 17:22:17, wedge ~5 s after start; no print_timing line (died before completion); prior tasks 162711-169319 were small incremental prefill + decode (20-1642 new tokens, 181-11910 decoded) | full context 197-200k (in-flight task's own new tokens not logged; size from the immediate re-send below) | ~99%+ (incremental against cached context; new tokens 100-700 per this session's pattern, not logged for the in-flight task) | opencode session with ~197-200k context; per the PM dispatch record in `## Status` this is the Tails T4 resumed session (T1-T3 accumulated); the llama.cpp log carries no client identity |
| 17:51:01 / 08:51:01 | comp_1.2.0, pid 7216 | task 0 on the fresh process, cold prefill started 17:22:59 (37 s after the restart); at the wedge: n=176128, p=0.89, t=1671.3 s (27.9 min), 105.4 t/s | 197-200k (196,923-200,037 from n/progress lines) | 0 (cold prefill, empty KV on the restarted process) | same ~197-200k session's retry (re-arm, T3 finding 4) |
| 18:18:35 / 09:18:35 | comp_1.2.0, pid 7313 | task 0 on the fresh process, cold prefill started 17:51:32 (31 s after the restart); at the wedge: n=172032, p=0.87, t=1609.6 s (26.8 min), 106.9 t/s | 197-200k (196,923-200,037) | 0 (cold prefill, empty KV) | same ~197-200k session's retry (re-arm) |

**Restart lines** (all systemd auto-restarts per `Restart=on-failure` + `RestartSec=5`; zero
`Stopped llama-server-qwen3.8-27b-iq4xs` lines in the boot-0 user journal, so the DoD
"never stopped by the team" holds for this window):
- 17:22:23 `Main process exited, code=dumped, status=6/ABRT` + `Failed with result 'core-dump'` → 17:22:28 `Started` → 17:22:33 `model loaded` (pid 7216). Wedge→Started 6 s, wedge→ready 11 s.
- 17:51:02 exited ABRT → 17:51:07 Started → 17:51:12 model loaded (pid 7313). 6 s / 11 s.
- 18:18:36 exited ABRT → 18:18:42 Started → 18:18:46 model loaded (pid 7434). 7 s / 11 s.

**Evidence lines** (verbatim, abbreviated):
- Wedge 1 in flight: `Sep 12 17:22:17 ... slot launch_slot_: id 0 | task 169934 | processing task, is_child = 0` is the last llama-server line before `Sep 12 17:22:23 ... Main process exited ... status=6/ABRT`. Prior task 169319 finished 17:22:17 with `prompt eval time = 3825.29 ms / 172 tokens` and `eval time = 67678.65 ms / 612 tokens`.
- Wedge 1 re-send start: `Sep 12 17:22:59 ... slot launch_slot_: id 0 | task 0` then `prompt processing, n_tokens = 4096, progress = 0.02, t = 7.60 s / 538.91 tokens per second`.
- Wedge 2 in flight: `Sep 12 17:50:51 ... task 0 | prompt processing, n_tokens = 176128, progress = 0.89, t = 1671.29 s / 105.38 tokens per second` (last line 10 s before the wedge).
- Wedge 3 in flight: `Sep 12 18:18:22 ... task 0 | prompt processing, n_tokens = 172032, progress = 0.87, t = 1609.61 s / 106.88 tokens per second` (last line 13 s before the wedge).
- Post-wedge-3: the first request on pid 7434 is a different, much smaller context: `prompt processing, n_tokens = 57834, progress = 1.00, t = 319.08 s / 181.25 tokens per second` (completes 18:24:41), then normal small traffic (task 375: 153 new prompt tokens + 182 decoded @ 12.14 t/s; task 560 at 18:24:58).

**Client attribution (inference, flagged).** The llama.cpp user journal does not log client
identity, so the client column is inferred from (a) context size (the ~197-200k re-send
identifies the owning session's full context) and (b) the dispatch record in `## Status`
(Tails T4 resumed was the active dispatch at 08:22 UTC; a Tails session with T1-T3
accumulated, including the large T3 journal pulls, matches the 197-200k size; the PM
session, which reads only `## Status` and `## Next Actions`, is far smaller). The `## Status`
hypothesis that wedges 2-3 "coincide with this PM session's own turns" is a wall-time
coincidence only: with `--parallel 1` the in-flight GPU work at 17:51:01 and 18:18:35 was the
197-200k cold re-prefill of the big session; any PM request at those moments was queued
behind it, not in flight. The 57.8k post-wedge-3 request is a different session (inferred:
PM or the fresh Tails T4 dispatch; the big session's turn died with zero output parts per
`## Status`, and its context cannot shrink from ~197k to 57.8k with compaction disabled).

**Open question (does not affect the correlation):** task 164155 (17:11:30-17:12:46) decoded
at 12.19-12.31 t/s while its neighbors decoded at 9.0-9.3 t/s, the 12.2 t/s rate matching a
~58-60k context (cf. the post-wedge-3 57.8k context at 12.14-12.25 t/s); no cold prefill for a
second client appears in the window (inter-task gaps < 5 s), so how a smaller-context request
ran without a visible re-prefill is unresolved.

**Verdict on the hot-mode hypothesis.** Hypothesis under test: each wedge coincided with a
request carrying a very large cached context (an opencode subagent or PM session running on
the endpoint), matching the hot wedge mode (incremental prefill against a ~200k cached
context).
- Very large context in flight at each wedge: **supported for all three** (197-200k).
- Hot mode (incremental prefill against a ~200k cached context): **supported for wedge 1
  only** (task 169934, ~5 s after task launch, against a ~197-200k cached context; matches the
  T3 hot signature "wedged 5-77 s after task launch").
- Wedges 2-3: **cold mode, not hot mode.** The in-flight work was a cold re-prefill of the same
  197-200k context on the restarted process (cached fraction 0), started 31-37 s after each
  restart: the opencode retry re-arming the identical workload (T3 finding 4). Each wedge
  destroys the cache that hot mode needs, so the cascade re-arms in cold mode, and the hang
  point degrades with cumulative stress: 89% (t=1671 s) then 87% (t=1610 s) of the prefill,
  the same self-perpetuating loop as the Aug 27 boot (T3, wedges 2-5).
- After the big session's turn died (no retry after wedge 3), the endpoint completed a 57.8k
  cold prefill in 319 s at 180.9 t/s and ran small-context traffic at 12.14 t/s decode: the
  wedge risk on this boot is tied to the ~197-200k context, not to the iq4xs service itself.
- Trigger refinement for T6: a request carrying a ~197-200k-token context wedges the chip
  either hot (incremental, seconds after task launch, after accumulated load) or cold
  (26.8-27.9 min into a re-prefill, hang point degrading 89% -> 87% with each retry).

**Next:** T6 adjudication (H1-H5 verdicts, one-sentence trigger, distro answer) + staged fixes
per plan; the H2 minimal repro (plan item 6) remains, bounded 15 min, only when no dispatch is
in flight.

### T5-H2 minimal repro (2026-09-13, Tails)

Plan item 6 (H2), dispatched fresh after the Sep 12 18:26 JST attempt died to a transport reset
(`## Status`; that death was not a wedge and touched nothing). llama.cpp fully out of the loop:
a standalone RADV Vulkan compute workload on the same iGPU, no 8093 traffic, service never
touched. The plan's 15-min bound is superseded by the dispatch brief's ~28 min (DURATION=1680):
the wedge threshold is 26.1-31.6 min of sustained compute (T3), so a sub-threshold run could
not resolve H2. Stop-on-wedge watchdog at 10 s cadence; sampler hard self-stop at DURATION+600 s.

**Repro started checkpoint (written before the run could complete).**
- Launch (exact, on EVO-X2): `nohup bash /tmp/h2_repro.sh 1680 h2run > /tmp/h2_h2run_runner.log 2>&1 &`
- Runner pid: 14044; workload pid: 14058 (`/tmp/h2_h2run/workload.pid`); sampler pid: 14059
- Start: 2026-09-12 19:13:30 UTC (`/tmp/h2_h2run/meta`) = 2026-09-13 04:13:30 JST; readback
  epoch 1789240414 (19:13:34 UTC)
- Pre-run wedge count, boot 0 (since 2026-09-12 03:47:07 UTC): **6** (`journalctl -k -b -0
  --no-pager | grep -cE "device wedged"`; the 6 = 3 on Sep 12 17:22/17:51/18:18 JST + 3 on
  Sep 13 01:04/01:31/02:00 JST)
- Workload: `/tmp/h2_workload 1680`, binary = `/tmp/h2_workload3` (v3: 16 independent
  dependent-FMA chains, 200k FMA per thread per dispatch, 4096 groups x 256 threads, ~19
  TFLOPS FP32). Rebuilt from the Sep 12 session's `/tmp/h2_*.c` sources after two fixes:
  (a) the original build segfaulted because the pipeline layout did not reference set layout 0
  (the shader declares `layout(binding = 0)`); the set layout is now created before the pipeline
  layout and referenced; (b) a device-name log line was added. Device selection skips llvmpipe
  (CPU-type device). Device line in `workload.log`: `Radeon 8060S Graphics (RADV GFX1151)
  type=1` (INTEGRATED_GPU).
- Shape (120 s smokes of v1/v2/v3 before launch): busy=100 throughout, PPT pinned 100.0 W
  (v1 2750 MHz; v2 = ALU + DRAM at ~2.7 GB/s prefill-like: 2580 MHz; v3 = 2x FLOP rate of v1:
  2730-2747 MHz), edge 82-88 C, clean exit rc=0. **Deviation of record:** the ~201k prefill
  pins PPT 119-120 W; every pure-compute variant tested pins at exactly 100.0 W (ALU-only,
  ALU+DRAM, 1x/2x FLOP rate) - the chip's demand ceiling for pure ALU compute under auto DPM;
  the prefill's extra ~20 W comes from its kernel mix (int ALU, LDS, exp, deep queue) that a
  minimal repro does not replicate. The run is at the plateau a pure-compute workload reaches:
  100% busy, power pinned, 28 min.
- Artifacts (on EVO-X2): `/tmp/h2_h2run/{meta,wedges_before,workload.pid,sampler.pid,sensors.csv,
  workload.log,end_marker[,wedge_marker]}`
- If the chip wedges mid-run: the watchdog kills the workload within 10 s of the wedge-count
  increment; the systemd user unit auto-restarts llama-server in ~6-11 s (system behavior,
  DoD-allowed, counted not prevented); this session may die on the next inference; this
  checkpoint + the artifacts are the record.

**Outcome (2026-09-13): WEDGED — the kernel journal shows the ring timeout + "device wedged"
line; the run did not complete cleanly.** Stop-on-wedge honored; the service was never stopped
by the team.

- End marker (`/tmp/h2_h2run/end_marker`): `rc=143` (watchdog SIGTERM), `wedges_before=6`,
  `wedges_after=7`, `start_epoch=1789240410`, `end_epoch=1789240571`, `wall_s=161`,
  `outcome=WEDGE_KILLED`. Wedge #7 of boot 0 at 2026-09-12 19:16:03 UTC (04:16:03 JST), 161 s
  (2.7 min) after the 19:13:31 start; watchdog kill at 19:16:11 (`wedge_marker`:
  `wedge_detected epoch=1789240571 wedges=7 before=6`).
- Workload process (h2_workload v3, pid 14058): ran the full 161 s at busy=100, PPT pinned
  100.0 W, sclk 2700-2747 MHz, edge 80-87 C (sensors.csv rows 1789240410-1789240561) with no
  Vulkan error (workload.log = device line only); killed by the watchdog, not a driver failure.
- Kernel (04:16:03 JST): `ring comp_1.2.0 timeout, signaled seq=5219170, emitted seq=5219172`
  → `Process llama-server pid 12170 thread llama-server pid 12170` → `Starting comp_1.2.0 ring
  reset` → `Ring comp_1.2.0 reset succeeded` → `[drm] device wedged, but recovered through
  reset`. **The timed-out job was attributed to llama-server (pid 12170), not to h2_workload
  (pid 14058).**
- llama-server side (user journal 04:16:03-04:16:14 JST): task 69288 launched 04:15:31 JST
  (= 19:15:31 UTC; this session's own checkpoint turn): context **126,248 tokens** (context
  checkpoint 32/32, n_tokens=126248), delta prefill of 95,903 new tokens against the 30,345
  cached prefix, interrupted 32 s after launch — the hot-mode signature (new task against a
  large cached context on a stressed chip; T3 class). Then the T3 userspace signature verbatim:
  `radv/amdgpu: The CS has been cancelled because the context is lost. This context is innocent.`
  → `terminate called after throwing ... 'vk::DeviceLostError'` (`vk::Queue::submit:
  ErrorDeviceLost`) in `ggml_backend_sched_graph_compute_async` → SIGABRT, core dump, `Main
  process exited, code=dumped, status=6/ABRT` → systemd auto-restart (restart counter 7)
  04:16:10, model loaded 04:16:14, 8093 listening. `grep -c "Stopped llama-server"` over the
  boot-0 user journal = **0** → zero team-initiated stops (DoD holds); the restart is
  wedge-triggered system behavior, counted (NRestarts 6 → 7).
- Rearm (T3 finding 4): 11 s after the restart, opencode's retry re-sent the full context —
  task 0 cold prefill 126,562 tokens (last progress line 112,640/0.89) — which completed
  clean: wedge count held at 7; later tasks (e.g. task 16627: 11,510-token delta prefill @
  73.71 t/s + 4,870 decode @ 9.82 t/s) ran to completion by 05:11:37 JST, `all slots are
  idle`.
- H2 adjudication input (T6 decides): a bounded non-llama RADV compute run wedged the chip in
   2.7 min — the fastest wedge recorded in the cold-mode class (a fresh full-power
   stressor start, no incremental prefill against a cached context; hot-mode wedges are faster
   in absolute time, 5-11 s after task launch after hours of load, 5-77 s over the full T3
   record, but a different regime; cold prefills wedge 26.1-31.6 min into the prefill)
   — on a chip with 6 prior wedges
  this boot (15.5 h of mixed load). The stressor was the non-llama workload (100% busy, power
  pinned); the hung job was llama.cpp's small-context delta prefill (a job class that ran
  thousands of times in the safe regime without wedging). Per the matrix, H2 is "supported" in
  the sense that a non-llama RADV workload wedged the chip, but "llama.cpp fully out of the
  loop" was not strictly satisfied (llama-server was serving this session's traffic and its
  job hung), so H3's exclusion rule ("excluded if H2 reproduces the wedge without llama.cpp")
  does not fire cleanly. A clean H2/H3 split would need a run with zero concurrent
  llama-server jobs, which is impossible while any team session runs on the endpoint.
- Post-run state: no h2 processes (`pgrep` clean; workload confirmed stopped), runner exited
  after writing the end marker; service active (pid 14313), 8093 listening; wedge count 7.
- Operational note: this session's context is ~126.5k tokens (journal-verified: 126,248 at
  04:15:31 JST) and grows with every turn — inside the range where a restart re-arm becomes a
  large cold prefill. This run's 126.5k re-arm completed clean (below the ~185k threshold),
  but the margin is shrinking. T6/T7 must run in fresh small-context sessions; nothing
   further is appended to this session.

### T6 adjudication (2026-09-13, Tails)

Scope: read-only adjudication from `## Plan` (lines 469-584) and the T5-H2 repro-started
checkpoint + outcome (lines 1461-1555). No remote commands run this turn; the session was kept
small per the T5-H2 operational note. `llama-server-qwen3.8-27b-iq4xs.service` was never touched
(zero team-initiated stops still hold: `grep -c "Stopped llama-server"` over the boot-0 user
journal = 0, T5-H2 record). Wedge count at T6 start: **7** (boot 0, per the T5-H2 post-run state;
not re-checked this turn). Per the dispatch brief the staged solution is filled here; T7 carries
it to the fixes doc.

**H1-H5 verdict table.**

| H | Verdict | Deciding evidence (command -> output) | Consequence for the staged solution |
|---|---|---|---|
| H1 kernel / amdgpu `7.0.12-1.el10.elrepo` | **Undetermined; Stage 3 is the deciding test.** Neither matrix branch is met yet. | The T5b kernel signature (`ring comp_1.2.0 timeout ... Ring comp_1.2.0 reset succeeded ... device wedged, but recovered through reset`, T5-H2 outcome) is the same class as every prior wedge; whether it matches a known amdgpu gfx1151 bug is T3's classification (recorded in `## Implementation`, not re-read this turn). Both matrix branches (known-bug match; newer-kernel test) resolve only when Stage 3 runs. | Stage 3 (elrepo kernel 7.2.5, same workload, 24 h wedge count) is the H1 decider; it also re-tests the kernel power-management path of H5. |
| H2 Mesa RADV userspace | **Partially supported.** A bounded non-llama RADV compute workload wedged the chip, but the matrix's strict supported-condition (llama.cpp out of the loop) was not met, and the excluded branch (clean run while llama wedges) was not met either. | T5-H2: h2_workload v3 (pure RADV, 100% busy, PPT pinned 100.0 W, ~19 TFLOPS FP32) in flight at wedge #7, 161 s (2.7 min) after start, the fastest cold-mode-class wedge recorded (hot-mode wedges are faster in absolute time, 5-77 s after task launch per T3, but a different regime); the kernel attributed the timed-out job to llama-server (pid 12170), not to h2_workload (pid 14058); the workload logged no Vulkan error and was killed by the watchdog, not a driver failure. | Stage 2 (Mesa update) is live. The H2/H3 split stays open; see the ambiguity note below. |
| H3 llama.cpp version + flags | **Not excluded, not supported.** H3's exclusion rule fires only on a clean H2, which did not happen; the supported branch (wedge rate changes when a frozen flag or the version is varied) is untested and needs a window. | T5-H2: the hung job was llama-server's 95,903-token delta prefill against a 126,248-token context (hot mode), a job class that ran thousands of times in the safe regime without wedging; the correlation is with chip stress state, not a llama.cpp defect. `-fa on` is not toggleable (q8_0 V-cache requires flash-attn, Plan line 495); the frozen flags stay unchanged per the hard constraints. | Stage 1 (llama.cpp version bump or user-approved flag change inside a window) is the H3 decider. |
| H4 systemd unit | **Excluded as a wedge cause** (by construction, Plan line 496: the unit manages lifecycle, it does not drive the GPU). Recovery behavior evaluated and acceptable. | T5-H2: the wedge-triggered restart was systemd's (04:16:10), model loaded 04:16:14, 8093 listening, restart counter 7; zero team-initiated stops over boot 0. | No Stage 1 unit edit indicated (5-11 s restarts are in the acceptable band); the unit stays as-is. |
| H5 heat / power | **Excluded as an independent trigger.** | 0 thermal-throttling events in a 2 d 9 h window with `thermal_throttling_logging` enabled (Test Results row 2, line 1370; documented conclusion: rules out thermal throttling as trigger); the T5b wedge moment ran at edge 80-87 C, sclk 2700-2747 MHz, PPT pinned 100.0 W, with no throttle/fan event in the recorded outcome. Runtime knobs are exhausted (`low` rejected at 4.5x slower, Plan line 497). | The "sustained full power" aspect lives in the trigger sentence; if power management is implicated it is via the kernel (Stage 3), not a sysfs knob. |

**The T5b ambiguity (weighed).** The kernel attributed the timed-out job to llama-server's
95,903-token delta prefill, which was running concurrently with the h2 workload pinned at
100.0 W; the post-wedge 126.5k cold prefill re-arm (126,562 tokens) completed clean 11 s after
the restart, wedge count holding at 7. Weighing: (a) the ring timeout is chip-level, amdgpu
reports whichever job was in flight at timeout, so the attribution names the victim, not the
cause; the stressor was the 100 W-pinned, 100%-busy pure-compute plateau the h2 workload applied
for 161 s. (b) The clean re-arm rules out a persistent chip state and confirms the reset
recovered ("recovered through reset"). (c) The delta-prefill job class has a clean history in the
safe regime, so its presence at the timeout moment is a stress correlation, not a code-path
defect. Net: the evidence favors H2 (sustained RADV/compute stressor) with the H3 thread kept
open, because a clean zero-llama split is impossible while any team session runs on the endpoint
(T5-H2, lines 1547-1548). That is why the staged solution keeps Stage 1 and Stage 2 live and
makes Stage 3 the kernel decider.

**The one-sentence trigger.** (Confirmed and reworded per Plan lines 499-503 with the T5b
correlation.) A single sustained full-power iGPU compute load at or near the 120 W cap, a ~201k
cold prefill at 119-120 W for ~29 min on a fresh chip (`/tmp/run_end_repro201k_auto.txt`, rc=52,
1760 s, 1 wedge) or a 100 W-pinned pure-compute plateau for 2.7 min on a chip with 6 prior
wedges this boot (T5-H2), drives the Strix Halo iGPU (8060S, gfx1151) past the amdgpu
compute-ring timeout/reset threshold; no accumulated stress is required to wedge, but
time-to-wedge shortens as wedges accumulate (fresh chip 26.1-31.6 min -> 2.7 min after 6 this
boot).

**Distro answer.** Stay on Rocky 10. The kernel fix (7.2.5) is obtainable on Rocky via elrepo
(per the dispatch brief; the T4 repoquery record sits in `## Implementation` and was not
re-read this turn) and the Mesa update via dnf, so the T4 decision rule (Plan lines 513-515:
stay on Rocky if the winning fix is a kernel or Mesa version obtainable on Rocky) does not force
a switch. Stage 4 is a dormant fallback, executed only if Stages 1-3 all fail.

**Staged solution (plan template, filled from the T6 verdicts; staged, awaiting user approval;
nothing executes without a user-approved window with zero dispatches in flight).**

| Stage | Change | Pre-change backup | Apply (exact commands, inside the window) | Verify after | Revert (step by step) |
|---|---|---|---|---|---|
| 1. restart-level, llama.cpp (live: H3 not excluded) | llama.cpp version bump or user-approved flag change; frozen flags (`-fa on`, q8_0 KV, `-c 262144`, `--parallel 1`) stay unchanged unless the user approves a specific frozen-flag change; target version chosen and recorded at window time | `UNIT=$(systemctl --user show llama-server-qwen3.8-27b-iq4xs.service --value --property=FragmentPath)`; `cp "$UNIT" /tmp/llama-unit.bak1.$(date +%s)`; `tr '\0' ' ' < /proc/$(systemctl --user show llama-server-qwen3.8-27b-iq4xs.service --value --property=MainPID)/cmdline > /tmp/cmdline.bak1` (both backup paths recorded in this doc) | edit the unit's `ExecStart` for the chosen change (flag, or new binary path); `systemctl --user daemon-reload`; `systemctl --user restart llama-server-qwen3.8-27b-iq4xs.service` | 24 h wedge count under the same workload (`journalctl -k --no-pager \| grep -cE "device wedged"` before and after) and t/s within 20% of baseline 11.87 | `cp /tmp/llama-unit.bak1.<ts> "$UNIT"`; `systemctl --user daemon-reload`; restart inside the window; restore the old binary if one was swapped |
| 2. package-level, Mesa/RADV (live: H2 partially supported) | `dnf` update of the mesa package owning the RADV ICD (package named from the T1 `rpm -qa \| grep -iE 'mesa'` listing recorded in `## Implementation`; target version per the T4 record) | `rpm -qa > /tmp/rpms.bak2.$(date +%s)`; `PKG=$(rpm -qf /usr/share/vulkan/icd.d/radeon_icd.x86_64.json)` (verify the path at window time; if absent, take PKG from the T1 listing); `dnf download --destdir=/tmp/rpmbak2 $PKG` (the exact installed version; file recorded in this doc) | `dnf update $PKG`; `systemctl --user restart llama-server-qwen3.8-27b-iq4xs.service` (the service loads libvulkan/ICD at startup) | same as Stage 1 plus `vulkaninfo --summary` shows the new RADV version | `dnf reinstall /tmp/rpmbak2/<backed-up rpm file>`; restart inside the window |
| 3. reboot-level, elrepo kernel 7.2.5 (live: H1 deciding test) | install the elrepo 7.2.5 kernel keeping 7.0.12, set it default, reboot; the boot-parameter variant is not indicated from the record at hand (T3's classification governs) | `rpm -qa \| grep -E '^kernel' > /tmp/kernels.bak3.$(date +%s)`; `grub2-editenv list > /tmp/grubdefault.bak3` (current saved entry, recorded in this doc) | `dnf install kernel-ml` (installonly keeps the old kernel; the kernel package creates the 7.2.5 BLS entry file); the host is BLS (no `menuentry` lines in `/boot/grub2/grub.cfg`; `GRUB_DEFAULT=saved`; verified 2026-09-13), so set the default by the exact BLS entry identifier, not a number: `N=$(ls /boot/loader/entries/*-7.2.5-1.el10.elrepo.x86_64.conf 2>/dev/null \| wc -l)` (must be 1 or stop); `BLSID=$(ls /boot/loader/entries/*-7.2.5-1.el10.elrepo.x86_64.conf \| head -1 \| xargs -n1 basename \| sed 's/\.conf$//')`; `grub2-set-default "$BLSID"`; `grub2-editenv list` (confirm `saved_entry=$BLSID`, the exact entry identifier); `reboot` | `uname -r` = `7.2.5-1.el10.elrepo.x86_64`; 24 h wedge count under the same workload on the new kernel | `OLDSAVED=$(grep '^saved_entry=' /tmp/grubdefault.bak3 \| cut -d= -f2-)` (the backup records the saved BLS identifier of the old default); `grub2-set-default "$OLDSAVED"`; `grub2-editenv list` (confirm `saved_entry=$OLDSAVED`); `reboot`; `uname -r` = `7.0.12-1.el10.elrepo.x86_64` (the old kernel was never removed; its BLS file still exists) |
| 4. distro switch (dormant: only if Stages 1-3 all fail and the T4 matrix forces it) | NixOS or Fedora reinstall (choice per the T4 record); redeploy model + user unit | full disk image to external storage: `dd if=<root-disk-device-per-T1> of=/mnt/<external>/evox2-$(date +%F).img bs=8M status=progress`; `sha256sum` of the image recorded in this doc | reinstall per the distro docs; redeploy model + user unit | 24 h wedge count + endpoint t/s within 20% of 11.87 | `dd if=/mnt/<external>/evox2-<date>.img of=<root-disk-device>`; keep the image until the switch has run clean for 2 weeks |

Rules carried from the plan (lines 547-549): backup locations are recorded in this section; the
service is restarted only inside the window and never stopped outside it; the old kernel/rpm is
never removed during the test window; Robotnik schedules the window with zero dispatches in
flight. Stages run in whatever order the user approves; the verdict column marks which are live.

**Session-context operational mitigation (codified, effective immediately, no window needed).**
1. T6/T7 and every subsequent dispatch for this task runs in a fresh small-context session (one
   new opencode session per dispatch; the planning doc is the bus, AGENTS.md section 2).
2. Each session keeps its context below the ~185k-token re-arm threshold (the recorded boundary:
   the 126.5k re-arm completed clean, T5-H2 line 1553); a re-arm above ~185k is a 26-32 min
   prefill that can itself wedge.
3. Findings are checkpointed to this doc before any long remote wait, so a session killed by a
   wedge-triggered restart loses nothing (the T5b pattern: the checkpoint + /tmp artifacts were
   the record); opencode's retry re-sends the full context as a cold prefill after the restart,
   so the re-arm cost scales with the session's context at the moment of the wedge.
4. The wedge count is checked before and after every action: `journalctl -k --no-pager |
   grep -cE "device wedged"`; every wedge inside a window counts toward the baseline (Plan,
   rollback, lines 572-579).

**Checks run this turn:** none on the host (read-only per the brief; the session kept small per
the T5-H2 operational note). No compile/lint/test applies (no code changed). The only change is
this section of the planning doc.

### T7 checkpoint (2026-09-13, Tails)

Fresh small-context session, per the T6 operational mitigation. Plan item T7 done: fixes doc
updated + "Staged, awaiting user approval" filled. No remote commands run this turn (the fixes
doc lives on this machine per the dispatch brief; nothing on EVO-X2 was touched). The service was
never touched; the zero-team-initiated-stops record is unchanged (T5-H2: `grep -c "Stopped
llama-server"` over the boot-0 user journal = 0).

- Fixes-doc backup of record (taken before the edit, exact command
  `cp qwen38-q5-fixes.md /tmp/qwen38-q5-fixes.md.bak.$(date +%s)` in
  `/home/howard/AI/projects/qwen-38-q5-fixes/`): **`/tmp/qwen38-q5-fixes.md.bak.1789250153`**
  (original 144 lines / 9085 bytes, verified present after the copy).
- Fixes doc `/home/howard/AI/projects/qwen-38-q5-fixes/qwen38-q5-fixes.md` updated: new section
  `## 2026-09-12/13: GPU wedge modes, H1-H5 verdicts, staged solution (TASK-0010)` appended,
  containing: the two wedge modes (cold 39/51, hot 12/51) with the ~200k-context retry-loop
  evidence (uniform first post-restart line across all 51 events, ~30-min cadence, boot-0 loop
  17:22/17:51/18:18 Sep 12 + 01:04/01:31/02:00 Sep 13 JST, hang point degrading 89% -> 87%);
  the H1-H5 verdict table; the one-sentence trigger (T6 wording, carried verbatim); the
  stay-on-Rocky distro answer (kernel 7.2.5 via elrepo; no Mesa newer than 25.2.7 in any Rocky
  repo; Fedora 44 the Mesa switch target if needed; Stage 4 dormant); and the staged solution
  Stages 1-4 with backups and reverts, marked **STAGED - awaiting user approval; NOTHING
  APPLIED**.
- `## Implementation` -> "Staged, awaiting user approval" filled (was "none yet") with the same
  four stage rows. T7 corrections to the T6 draft cells, recorded (not silent): (a) Stage 3
  apply now includes the elrepo-kernel repo enable step and names the package `kernel-ml` (the
  T6 draft cell said `dnf install elrepo-kernel`, which is the repo name, not a package; the T4
  record lines 1331-1340 establishes the package `kernel-ml 7.2.5-1.el10.elrepo` and that the
  repo file is on the host but disabled); the repo file backup was added to Stage 3's backup
  cell. (b) Stage 2 names the package `mesa-vulkan-drivers` explicitly (T1 record, line 1054) and
  carries the T4 note that no newer Mesa is obtainable on Rocky today. (c) T6's distro-answer
  phrase "the Mesa update via dnf" compressed the T4 finding that no newer Mesa is in any Rocky
  repo; the fixes doc states the T4 finding explicitly, the decision (stay on Rocky, Stage 4
  dormant) is unchanged.
- Nothing staged was executed; no unit, sysfs, repo, or kernel state changed anywhere.

Changes:

| File | What changed |
|---|---|
| `/home/howard/AI/projects/qwen-38-q5-fixes/qwen38-q5-fixes.md` | appended the 2026-09-12/13 section (findings + staged solution, staged not applied) |
| `planning/docs/TASK-0010-evox2-gpu-wedge-fix.md` | "Staged, awaiting user approval" filled; this checkpoint; Next Actions updated |

Checks run: no host commands (no code changed, nothing to compile/lint/test). Backup verified to
exist after the copy (`ls -la` on the backup path).

### T5-correlation addendum: boot-0 wedges #4-#6 (2026-09-13, Tails, fix round 1)

Re-correlation of boot-0 wedges #4-#6 with the T5-correlation method (Blocker 3 of the 2026-09-13
review). Read-only on EVO-X2 (`ssh howard@192.168.1.106`): kernel journal `-b 0` 01:00-02:05 JST;
user journal windows 01:00-01:10 / 01:27-01:42 / 01:55-02:20 JST and the gap window Sep 12
18:24 - Sep 13 01:04 JST. No service touch; the service was never stopped by the team.

**Per-wedge table.**

| Wedge (JST / UTC) | Kernel (ring, pid) | In flight at wedge (user journal) | Context size | Cached fraction | Mode |
|---|---|---|---|---|---|
| 01:04:20 / Sep 12 16:04:20 | comp_1.1.0, pid 7434 | task 212721 launched 01:04:15, wedge 5 s after launch (hot signature, T3); prior task 211967 finished 01:04:15 (1576 tok prompt eval + 751 decoded @ 8.96 t/s, 83.8 s decode); no print_timing for 212721 (died before completion) | ~199-201k (from the post-wedge-4 re-send: 172032/0.86 -> 198,881-201,207) | the ~200k context cached on pid 7434 (created 00:00-00:32 JST, below) | hot |
| 01:31:58 / Sep 12 16:31:58 | comp_1.2.0, pid 11951 | task 0 on the fresh process (re-send started 01:04:54, 22 s after model load); last line n=172032, p=0.86, t=1610.14 s (26.8 min; 13 s before the wedge) | ~199-201k (172032/0.86 -> 198,881-201,207) | 0 (cold re-prefill) | cold |
| 02:00:08 / Sep 12 17:00:08 | comp_1.2.0, pid 12065 | task 0 on the fresh process (re-send started 01:32:30, 21 s after model load); last line n=174080, p=0.87, t=1640.58 s (27.3 min; 18 s before the wedge) | ~199-201k (174080/0.87 -> 198,949-201,249) | 0 (cold re-prefill) | cold |

Restart lines (systemd auto-restarts, `Restart=on-failure` + `RestartSec=5`): wedge->Started 6-7 s,
->model loaded 11-12 s (01:04:27/01:04:32 pid 11951; 01:32:05/01:32:09 pid 12065; 02:00:14/02:00:19
pid 12170). One class-C fence fallback (01:05:35, 75 s after wedge 4, comp_1.1.0), not a wedge.

**The ~200k context behind #4-#6 was created Sep 13 00:00-00:32 JST, not "running 7 h".** Gap
window, pid 7434 (running uninterrupted since the post-wedge-3 restart 18:18:46 JST Sep 12: no
`Started`/`Main process`/`Stopped` lines in the window): task 195105, a cold prefill of
**172,727 tokens** (started ~00:00:56 JST; last progress line n=172723, p=1.00, t=1633.20 s;
completion `prompt eval time = 1657238.96 ms / 172727 tokens / 104.23 t/s`, printed 00:32:40 JST
after decode). It **completed clean** on a chip with 3 prior wedges this boot (27.6 min, inside
the 26.1-31.6 min cold band but below the ~185k re-arm threshold, consistent with the clean
57.8k / 75.7k / 126.5k re-arms). The first request on pid 7434 was the 57.8k prefill
(18:19-18:24 JST, T5-correlation, a different small session); the 172.7k context then sat cached
while small tasks ran (task counter continuous on pid 7434: 195105 ~00:01 JST -> 212721
01:04:15 JST).

**Session identity (the journal carries no client identity; per-session attribution is inference).**
The #4-#6 owner's context was 172,727 tokens at 00:00 JST and ~199-201k by 01:04 JST (intra-session
growth; compaction disabled). The #1-#3 owner's context was >= 196,608 tokens at 08:51-09:18 UTC
(172032/0.87 and 176128/0.89 with two-decimal progress rounding; T5-correlation derived
196,923-200,037). 172,727 < 196,608 and a session's context cannot shrink with compaction disabled,
so **the #4-#6 loop is a different session from the #1-#3 loop**: two distinct ~200k-class opencode
sessions. Most likely identities (inference from the `## Status` dispatch record): #1-#3 = the
Tails T4 resumed session (T1-T3 accumulated, ~197k); #4-#6 = the fresh T4 (Attempt 4) session,
running since ~08:25 UTC and grown to 172.7k by 00:00 JST.

**Retry cadence.** #4->#5 27 m 38 s, #5->#6 28 m 10 s; #2->#3 (Sep 12) was 27 m 34 s
(T5-correlation). Each spacing = the re-send prefill's time to the wedge (1610.14 / 1640.58 s to
the last logged progress line, wedge 13-18 s after it) + 19-34 s restart and retry latency; the T3
cluster cadence was 28-48 min. The loop ends when the owning session stops retrying: the
post-wedge-6 re-send (task 0, pid 12170, started 02:00:27 JST, 8 s after model load) is
**75,671 tokens** (`prompt eval time = 467581.24 ms / 75671 tokens / 161.83 t/s`, completed clean
02:08:41 JST) - a different, smaller session (the ~200k owner did not re-send ~200k a third time;
context cannot shrink), then small traffic (tasks 343, 1157, 4447, 6961, 7502 by 02:19:55 JST).

**Conflict with `## Status` (named here, not edited; Status is Robotnik's section).** The
2026-09-13 Status entry attributes #4-#6 to "the same ~200k-context retry loop" with "the same
~200k cached context, running 7 h". The journal contradicts both clauses: the ~200k context was
created 00:00-00:32 JST (32-63 min before wedge 4, not 7 h) and belongs to a different session
than #1-#3 (size arithmetic above). T5-correlation's "no retry after wedge 3" (its verdict on the
#1-#3 owner) **stands**: the ~197k session never re-prefilled on pid 7434; the 57.8k re-send and
the 172.7k prefill are two other sessions.

**Trigger sentence: not corrected.** All new data points sit inside the stated trigger: a hot wedge
5 s after task launch on a chip with 3 prior wedges this boot (hot mode), cold wedges at 26.8/27.3
min (inside the 26.1-31.6 min band), and the one clean large prefill (172.7k) below the ~185k
re-arm threshold. The review finding 10 wording defects (the 100 W vs 120 W power clause; the
fresh-chip range label) remain open for the next round.

**Checks run:** the journal pulls above (kernel `-b 0` + user journal windows, filtered with
`grep -E`); `grub2-editenv list`, `head /boot/grub2/grub.cfg`, `ls /boot/loader/entries/`,
`grep GRUB_DEFAULT /etc/default/grub`, `grep -A6 elrepo-kernel /etc/yum.repos.d/elrepo.repo` (all
read-only; sudo used for root-owned files only). No service touch; no writes on EVO-X2.

### W1 checkpoint: t/s verification vs the iq4xs baseline (2026-09-13, Tails, fresh session)

**Purpose.** Close the W1 remaining work per `## Next Actions`: verify the live 8093 service's
decode t/s against the **iq4xs** baseline, not the Q4 11.87 the staged table's Stage 1/4 verify
still cites (Review finding at `planning/docs/TASK-0010-evox2-gpu-wedge-fix.md:1717`). No restart;
the service was never touched.

**Recorded iq4xs baseline (found via targeted grep, not re-derived).** Small-context decode
**12.1-12.3 t/s** at a ~58-60k context: T5-correlation task 164155 at 12.19-12.31 t/s
(`:1304-1306`), the post-wedge-3 57.8k context at 12.14-12.25 t/s and "small-context traffic at
12.14 t/s" (`:1325`), the 57.8k cold prefill at 180.9 t/s (`:1325`). Boot-wide decode range
9.82-12.31 t/s depending on context (`:1720`).

**Live verification (this turn, against the live 8093 service).** Matched-context completion,
`curl -s -X POST http://192.168.1.106:8093/v1/completions` (body 290,455 prompt chars,
`max_tokens 400`, `min_tokens 300`, `temperature 0`). llama-server `timings` block:
- total prompt **57,462** tokens (40,542 cached from the earlier probe this turn, 16,920 new)
- new prefill **174.96 t/s** (16,920 tok / 96.7 s)
- decode **400 tok / 33.4 s = 11.95 t/s** at decode context ≈ **57,862**
- `finish_reason: length` (full 400 generated), `system_fingerprint: b2000-5266f24d` (build 2000
  / 5266f24d confirmed live on 8093)

An earlier 71-token probe on the same service this turn decoded at 13.98 t/s (the small-context
regime, faster than the ~58k baseline by construction); the matched-context number above is the
one compared to the baseline.

**Verdict.** Live decode **11.95 t/s at ~57.9k context** vs the recorded iq4xs baseline
**12.1-12.3 t/s at ~58-60k context**: ~1.2-2.9% below the baseline range, inside the Stage 1/4
"within 20% of baseline" band. Prefill 174.96 t/s is within ~3.3% of the recorded 180.9 t/s
cold-prefill figure. The Stage 1 changes (build 2000 binary, `-c 98304` kept by the user) have not
degraded decode performance. **W1 t/s verification: PASS.**

**Checks run:** `curl /v1/models` (model `Qwen3.8-27B-UD-IQ4_XS`, `n_ctx` 98304, ftype IQ4_XS);
the 71-token and 57.5k completion probes above; `curl /health` = `{"status":"ok"}`. No service
restart; no writes on EVO-X2; no wedge re-arm (57.5k prefill is far below the ~185k re-arm
threshold and the ~2 min of new compute is far below the 26-32 min sustained-compute band).

### W2 checkpoint: Stage 3 applied, reboot issued (2026-09-13 21:25 JST, Tails, fresh session)

Stage 3 applied exactly per the staged section (`## Implementation` → "Staged, awaiting user
approval", line 749), inside the user-approved window ("go ahead and start this now", 2026-09-13).
All commands ran on EVO-X2 (hostname `trip`, 192.168.1.106) as `howard` over ssh from shadow
(192.168.1.102); `sudo` only for the root-owned steps (`dnf install`, `grub2-set-default`, the
`/boot/loader/entries/` listing). Shadow blocker 1 resolution honored: the grub default is set by
**exact BLS entry identifier**, not a numeric ordinal (host is BLS: `GRUB_DEFAULT=saved`, zero
`menuentry` lines in `/boot/grub2/grub.cfg` — verified again this session). The service unit was
not touched (user kept `-c 98304`). Wedge count at change time: 10 since boot (matches `## Status`).

**Commands run (in order), with results:**

1. Pre-change backups (staged section, verbatim paths):
   - `rpm -qa | grep -E "^kernel" > /tmp/kernels.bak3.1789301554` (TS=1789301554; 16 kernel
     packages listed, 7.0.12 kernel-ml + two base 6.12.0 kernels)
   - `grub2-editenv list > /tmp/grubdefault.bak3` — content:
     `saved_entry=aad6cfa1c71c461bbc6543c87712d7f1-7.0.12-1.el10.elrepo.x86_64`,
     `menu_auto_hide=1`, `boot_success=1`, `boot_indeterminate=0`
   - `cp /etc/yum.repos.d/elrepo.repo /tmp/elrepo-kernel.repo.bak3`
2. Read-only availability check before install: `dnf --enablerepo=elrepo-kernel list available
   kernel-ml` → `kernel-ml.x86_64 7.2.5-1.el10.elrepo` (the exact planned version; no surprise
   newer version in the repo). `/boot` had 1.2 G free.
3. Repo enable: `dnf config-manager` is not installed on the host (`command -v dnf-config-manager`
   empty), so the staged `enabled=0 -> enabled=1` change was made with a section-scoped sed:
   `sudo sed -i '/^\[elrepo-kernel\]/,/^\[elrepo-extras\]/ s/^enabled=0/enabled=1/'
   /etc/yum.repos.d/elrepo.repo`. `diff /tmp/elrepo-kernel.repo.bak3 /etc/yum.repos.d/elrepo.repo`
   shows exactly one line changed (line 35: `enabled=0` → `enabled=1`); all other sections
   untouched.
4. `sudo dnf -y install kernel-ml` → installed `kernel-ml-core-7.2.5-1.el10.elrepo.x86_64`,
   `kernel-ml-modules-7.2.5-1.el10.elrepo.x86_64`, `kernel-ml-7.2.5-1.el10.elrepo.x86_64`
   (transaction "Complete!"; installonly, 7.0.12 kept). **Observed side effect (not a staged step,
   not a failure):** a DKMS scriptlet warned that `ryzen_smu/0.1.7` cannot build for 7.2.5 because
   `kernel-ml-devel` for 7.2.5 is not installed. `sudo dkms status`: ryzen_smu installed for
   6.12.0-211.22.1 and 7.0.12-1.el10.elrepo only. The in-kernel amdgpu driver (elrepo kernel-ml
   tree) is unaffected — `modinfo amdgpu` shows
   `/lib/modules/7.0.12-1.el10.elrepo.x86_64/kernel/drivers/gpu/drm/amd/amdgpu/amdgpu.ko.xz`.
   Deliberately not built now: the H1 deciding test should run 7.2.5 stock, and adding a module
   build would change the power-management surface mid-test. **W3 note:** if the ryzen_smu sysfs
   interface is needed under 7.2.5, `sudo dnf install kernel-ml-devel` + `sudo dkms autoinstall`
   (no reboot required).
5. BLS guard + set default, per the staged section verbatim (run as a script
   `/tmp/stage3-setdefault.sh` via `sudo bash` to keep the guard atomic):
   `N=$(ls /boot/loader/entries/*-7.2.5-1.el10.elrepo.x86_64.conf 2>/dev/null | wc -l)` → **N=1**
   (guard passed); `BLSID=aad6cfa1c71c461bbc6543c87712d7f1-7.2.5-1.el10.elrepo.x86_64`;
   `grub2-set-default "$BLSID"`; `grub2-editenv list` confirms
   `saved_entry=aad6cfa1c71c461bbc6543c87712d7f1-7.2.5-1.el10.elrepo.x86_64` (the staged
   "confirm" step). The 7.2.5 BLS file
   `aad6cfa1c71c461bbc6543c87712d7f1-7.2.5-1.el10.elrepo.x86_64.conf` was created by the kernel
   package; `ls /boot/loader/entries/` shows 5 entries (0-rescue, two 6.12.0 base, 7.0.12, 7.2.5).

**Planned revert (staged section, verbatim; the old kernel was never removed):**

```
OLDSAVED=$(grep '^saved_entry=' /tmp/grubdefault.bak3 | cut -d= -f2-)
# OLDSAVED = aad6cfa1c71c461bbc6543c87712d7f1-7.0.12-1.el10.elrepo.x86_64
grub2-set-default "$OLDSAVED"
grub2-editenv list   # confirm saved_entry=$OLDSAVED
reboot
uname -r   # expect 7.0.12-1.el10.elrepo.x86_64
# restore the repo file from /tmp/elrepo-kernel.repo.bak3 (or leave enabled, user's call)
```

**Reboot issued** (`reboot` on EVO-X2, sudo) at 21:25 JST after this checkpoint was written and
flushed. This Tails session and the PM session die with the endpoint on 8093; that is expected and
approved (window 2026-09-13).

**Post-reboot (W3, `## Next Actions`):** wait for 8093; verify `uname -r` =
`7.2.5-1.el10.elrepo.x86_64`, service active on 8093, llama.cpp version; record the wedge baseline
(count at first check; 10 at change time was pre-reboot); start the bounded 24 h wedge monitor
(pid recorded, hard stop); resolve the ryzen_smu note above if the interface is needed.

---

### W3 checkpoint: post-reboot verification, 24 h wedge monitor started (2026-09-13 22:45 JST, Tails, fresh session)

Post-reboot state, verified pre-session per the W3 brief (boot ~21:29-21:30 JST after the W2
reboot at 21:25 JST; first kernel journal lines at 21:29:41 JST): kernel
`7.2.5-1.el10.elrepo.x86_64`; service `llama-server-qwen3.8-27b-iq4xs.service` active (user unit
auto-started); 8093 listening; pid 1907; unit carries `-c 98304` intact; load ~0.05; wedge count
0 since boot.

This session ran over ssh as howard, direct from the team host; the service was not touched.

- **Binary version confirmed** (expected build 2000, commit 5266f24d). Command:
  `PID=$(systemctl --user show llama-server-qwen3.8-27b-iq4xs.service --value --property=MainPID); BIN=$(readlink -f /proc/$PID/exe); "$BIN" --version`
  Result: `pid=1907`, `bin=/usr/local/bin/llama-server`, `version: 0.4.0-dev (build 2000,
  commit 5266f24d)`, `built with GNU 14.3.1 for Linux x86_64`. Matches the W1 live fingerprint
  b2000-5266f24d.
- **Wedge baseline (t=0, first monitor tick):** `wedge_count=0` at 22:44:43 JST (log line 2),
  consistent with the pre-session verified count of 0 since boot.
- **Bounded 24 h wedge monitor started, detached.** Script `/tmp/wedge_monitor_w3.sh` (scp'd from
  the team host, 1446 bytes); log `/tmp/wedge-monitor-20260913-224443.log`; **pid 6647**
  (cross-verified three ways: launcher `$!`, `pgrep -af wedge_monitor_w3.sh`, the script's own
  `pid=$$` in log line 1); started **2026-09-13 22:44:43 JST**, hard stop **2026-09-14 22:44:43
  JST** (start + 86400 s, enforced by the loop condition `now < END`; a `monitor-stopped` line is
  appended after the bound). Every 300 s it appends `timestamp wedge_count=N`, N =
  `journalctl -k --no-pager | grep -cE "device wedged"` (plain journal access verified working as
  howard without sudo before launch; a defensive branch records `err-journalctl` instead of a
  bogus 0 if journal access ever fails). Launch:
  `nohup bash /tmp/wedge_monitor_w3.sh </dev/null >/dev/null 2>&1 &`.
- **ryzen_smu note (carried from the W2 checkpoint):** left as-is. The H1 deciding test runs 7.2.5
  stock and the in-kernel amdgpu driver is the stock elrepo kernel-ml tree; revisit only if the
  ryzen_smu sysfs interface is needed under 7.2.5 (then `sudo dnf install kernel-ml-devel` +
  `sudo dkms autoinstall`, no reboot required).

**Monitor outcome (next):** the final `wedge_count=` line in the log at ~2026-09-14 22:44 JST is
the Stage 3 verification number per the staged section ("24 h wedge count under the same workload
on the new kernel").

### Citation refresh checkpoint

2026-09-14, Tails. Doc-only pass, session 2 (restart: session 1 died at the context
window with the mapping complete and the in-place fixes unapplied). No machine changes,
no ssh, no service actions.
Scope. Stale line citations reported in `## Review` (Shadow). Citations sitting in a
non-protected section are fixed in place and verified with grep. Citations sitting in
`## Review`, `## Security`, or `## Test Results` are listed below with the owning
section and not edited.

Placement note. This subsection sits at the end of `## Implementation`, below every
citation target it records, so appending here cannot invalidate the corrected values
written above it.

Reported stale (from dispatch brief, to be located):

- Shadow finding. "T6's line citations are stale after the doc grew."
- Shadow finding. W1 stale-citation nit.

Citations found and fixed (appended as work proceeds):

Located 2026-09-14 by grep `TASK-0010[^ )]*:[0-9]+|[Ll]ine [0-9]{3,4}` on the current file.

Fixable (in `## Implementation`):

- L1454-1455 area (T6 verdict cites): per Shadow, 'Plan (lines 259-376)' and 'lines 1244-1326' - to read and confirm.
- L1573-1575 (hypothesis matrix H3/H4/H5 rows): 'Plan line 285', 'Plan line 286', 'Test Results row 2, line 1370', 'Plan line 287' - to read and confirm.
- L1625: 'T5-H2 line 1324' - to read and confirm.
- L1667: 'T1 record, line 828' - to read and confirm.
- L1757: cite of a Review finding at `planning/docs/TASK-0010-evox2-gpu-wedge-fix.md:1717` - to read and confirm.
- L1793: 'line 648' - to read and confirm.
- T6 scope/verdict/trigger/draft cells: session 2 scanned L1350-1407, no stale doc 'lines NNN' cites there (the ranges above were stale pointers ~209 lines low; the true cells sit in the T6 section L1557-1637 and are enumerated below; the only line-number-like strings in L1350-1407 are external file:line cites, e.g. linux-kernels.nix:737-739, which are correct as-is).

List-only (protected sections, not edited):

- `## Review`: L1949, L1968, L1981, L1999, L2007, L2015, L2016, L2023, L2024, L2025, L2031, L2039, L2047, L2055, L2063, L2064, L2066, L2071, L2079, L2080, L2081, L2092, L2099, L2113, L2128, L2135, L2200, L2215, L2250.
- `## Security`: L2380, L2382, L2501.

T6 adjudication is at L1557-1637 (grep `^### T[0-9]`; Shadow's own T6 line numbers in
`## Review` are stale even as of their writing). Stale cites inside T6, confirmed by read:

- L1559-1560 (scope): '## Plan (lines 259-376)' and 'T5-H2 repro-started checkpoint + outcome (lines 1244-1326)'
- L1573 (H3 row): 'Plan line 285' (-fa / q8_0 V-cache note)
- L1574 (H4 row): 'Plan line 286' (unit manages lifecycle)
- L1575 (H5 row): 'Test Results row 2, line 1370' (0 thermal-throttle events) and 'Plan line 287' (low rejected 4.5x)
- L1588 (ambiguity): '(T5-H2, lines 1318-1319)' (zero-llama split impossible)
- L1591 (trigger): 'Plan lines 289-293' (one-sentence trigger template)
- L1602 (distro): 'Plan lines 303-305' (T4 decision rule)
- L1616 (staged rules): 'plan (lines 337-339)'
- L1625 (mitigation 2): 'T5-H2 line 1324' (126.5k re-arm clean)
- L1632-1633 (mitigation 4): 'Plan, rollback, lines 362-369'

Session 2: L1667 'T1 record, line 828' -> 1054, fixed; L1665 'lines 1105-1114' -> 1331-1340,
fixed; L1757 Review-finding cite and L1793 'line 648' (the staged section, L749-769) lines pending.

Confirmed by read of L1639-1700:

- L1667 (T7): 'Stage 2 names the package `mesa-vulkan-drivers` explicitly (T1 record, line 828)'
  - target: the T1 `rpm -qa | grep -iE 'mesa'` listing line. T1 section location to map.
- L1665 (T7): 'the T4 record lines 1105-1114 establishes the package `kernel-ml
  7.2.5-1.el10.elrepo`' - target: the T4 elrepo-kernel repoquery lines. T4 section location to map.

Grep gap noted: the first locate grep used `[Ll]ine [0-9]{3,4}` (singular) and missed plural
'lines NNNN' cites (e.g. the T6 scope cite at L1559-1560 was found by read, not grep). A second
grep with `lines [0-9]{3,4}` is required to catch the rest.

Second locate grep done. New fixable cite found: L765 (in `### Staged, awaiting user approval`,
L749-769): 'Rules carried from the plan (lines 337-339)' - same target as the T6 instance at
L1616, i.e. Plan 547-549.

Subsection map (bash `grep -n '^### '`, current file): Staged L749, Attempt 3 L787, Attempt 3
session 2 L878, Attempt 4 L1034, T5-correlation L1384, T5-H2 L1461, T6 L1557, T7 L1639,
addendum L1684, W1 L1753, W2 L1790, W3 L1864, Citation refresh checkpoint L1900.

T1/T4 targets located by content grep (offset check: 1054-828 = 226, 1331-1105 = 226, consistent
with the upper-doc growth since T7 was written):

- L1667 'T1 record, line 828' (mesa listing) -> L1054 ('**Mesa / Vulkan.** `rpm -qa |
  grep -iE 'mesa|amdgpu'` -> `mesa-vulkan-drivers-25.2.7-4.el10.rocky.0.1`'), in Attempt 4.
- L1665 'T4 record lines 1105-1114' (kernel-ml 7.2.5 + repo file on host but disabled) -> T4
  record block in the distro comparison, L1316-1356 area; exact 10-line current range to pin by
  reading L1316-1345.

Plan targets measured (Plan section is L469-584 now; every internal target sits at a constant
+210 offset from its old value, verified against the read of L469-584):

- old 259-376 (whole Plan) -> 469-584
- old 285 (H3 row, `-fa on` not toggleable) -> 495
- old 286 (H4 row, unit manages lifecycle) -> 496
- old 287 (H5 row, `low` rejected 4.5x) -> 497
- old 289-293 (trigger template) -> 499-503
- old 303-305 (T4 decision rule) -> 513-515
- old 337-339 (rules for every stage) -> 547-549
- old 362-369 (rollback block) -> 572-579

T5-H2 section is L1461-1555 now (grep `^### T[0-9]`). Targets:

- old 1244-1326 (T5-H2 repro-started + outcome, whole section) -> 1461-1555
- old 1324 (126.5k re-arm completed clean) -> 1553 (confirmed by read)
- old 1318-1319 (zero-llama split impossible) -> 1547-1548 (confirmed by read: "A clean H2/H3
  split would need a run with zero concurrent llama-server jobs, which is impossible while any
  team session runs on the endpoint.")

---

## Review

*Owner: `Shadow`. Read-only — findings only, no edits. Severity order, blockers first.*

### Review verdict (Shadow, 2026-09-13): record is coherent overall; 3 blockers, 10 should-fix, 1 nit

Scope read: `## Definition of Done`, `## Plan`, the T1-T7 checkpoints in `## Implementation`, the
'Staged, awaiting user approval' table, and the fixes doc
`/home/howard/AI/projects/qwen-38-q5-fixes/qwen38-q5-fixes.md` plus its backup
`/tmp/qwen38-q5-fixes.md.bak.1789250153` (verified present, 144 lines, pre-edit state; the
appended TASK-0010 section is present in the fixes doc).
What holds: the H4 and H5 verdicts are fully backed by the checkpoints (H4: unit file and
Restart/RestartSec at T1:856-891, restart behavior at T5-H2:1319-1323; H5: the T3 ±60 s check at
992-994 plus wedge-moment sensors at 1304-1306; the verdict stands, only the citation is wrong,
finding 7). The H1, H2, H3 verdict directions are honest and match the matrix's third-state
reality; the defects are in the cited evidence, not the verdicts. All four staged stages carry
complete backup + apply + verify + revert cells. No invented package names (`kernel-ml` and
`mesa-vulkan-drivers` are T4/T1-verified, lines 848, 1116). No missing reverts. DoD box mapping:
boxes 2, 3, 5, 6, 8, 9 map to verifiable record content (with the defects below); boxes 4 and 7
point at a stale `## Test Results` (finding 12); box 1 is not met as written (finding 11);
boxes 10-13 are future work, correctly unticked.

### Blocker: Stage 3 apply sets the wrong boot entry (grub.cfg line number is not the grub2-set-default index)
**Severity:** blocker
**Where:** `planning/docs/TASK-0010-evox2-gpu-wedge-fix.md:556` (Stage 3 apply); same cell in the T6 draft at 1404; fixes doc `qwen38-q5-fixes.md:228` repeats it
**Problem:** `NEWIDX=$(grep -n '^menuentry' /boot/grub2/grub.cfg | grep -F '7.2.5' | head -1 | cut -d: -f1)` computes the file line number of the 7.2.5 menuentry, but `grub2-set-default`'s numeric argument is the 1-based ordinal of the entry among menuentry lines, not its line number in the file.
**Failure scenario:** in the reboot window the 7.2.5 entry starts on, say, line 15 of grub.cfg but is the 3rd menuentry; `grub2-set-default 15` saves the 15th menuentry as default (a different kernel, e.g. a 6.12 base kernel without the elrepo amdgpu tree, or an out-of-range index) and the model host reboots into the wrong state; the follow-up `grub2-editenv list` 'confirm saved=$NEWIDX' cannot match either, since grubenv stores the entry title, not a number.
**Suggested direction:** set the default by exact menuentry title (extract the 7.2.5 title from `/boot/grub2/grub.cfg` and pass the title to `grub2-set-default`), or compute the 1-based menuentry ordinal; confirm `grub2-editenv list` shows `saved=<7.2.5 title>` before the reboot. Also resolve the `<elrepo-kernel repo file>` placeholder before the window (T4:1123 records the repoid `elrepo-kernel` as disabled but not the file path), and word the revert cell's 'old index' as 'the saved title from /tmp/grubdefault.bak3' (the backup file contains `saved=<title>`).
**Resolution:** fixed (Tails, 2026-09-13, fix round 1): Stage 3 apply + revert now set the default
boot entry by exact entry identity, not a numeric ordinal, in the staged section and the T6 draft
of this doc and in the fixes doc (`5f6ff07d`, `git hash-object qwen38-q5-fixes.md`; that directory
is not a git repo). The review's literal direction (menuentry title from `/boot/grub2/grub.cfg`) is
not executable on this host: it is BLS (verified 2026-09-13: `GRUB_DEFAULT=saved`, `grubenv` holds
`saved_entry=<BLS identifier>`, zero `menuentry` lines in grub.cfg; `grub2-set-default(8)`:
"MENU_ENTRY is a number, a menu item title or a menu item identifier"). The command now derives the
exact BLS identifier for 7.2.5 from `/boot/loader/entries/` (with a must-be-1 match guard) and
confirms `saved_entry=<id>` before the reboot; the revert reads the saved identifier from
`/tmp/grubdefault.bak3`. The `<elrepo-kernel repo file>` placeholder resolves to
`/etc/yum.repos.d/elrepo.repo`; the T6 draft cell's `dnf install elrepo-kernel` (a repo name, not a
package) is corrected to `kernel-ml` in the same pass.

### Blocker: 'the fastest wedge ever recorded' contradicts the T3 hot-mode record
**Severity:** blocker
**Where:** `planning/docs/TASK-0010-evox2-gpu-wedge-fix.md:1330` (T5-H2 outcome); 1363 (T6 H2 cell); fixes doc `qwen38-q5-fixes.md:192`
**Problem:** the 161 s (2.7 min) T5-H2 wedge is called 'the fastest wedge ever recorded' while the same sentence's parenthetical and T3 both record hot-mode wedges that fired 5-11 s after task launch (T3 workload finding (b) at 1081; T5-correlation at 1237), which is faster than 161 s.
**Failure scenario:** Big's re-verification (DoD box 13) compares the claim against the T3 tables and finds 12 hot wedges with 5-77 s time-to-wedge; the superlative is false on the record's own numbers, and it feeds the trigger sentence's accumulation story.
**Suggested direction:** reword to 'the fastest wedge from a controlled bounded-stressor start (no hours of prior load)' or drop the superlative; update the T5-H2 outcome, the T6 H2 cell, and the fixes doc in one pass.
**Resolution:** fixed (Tails, 2026-09-13, fix round 1): reworded in all three locations — the T5-H2
outcome, the T6 H2 cell (this doc), and the fixes doc H2 cell (`5f6ff07d`). The superlative now
reads "the fastest wedge recorded in the cold-mode class (a fresh full-power stressor start, no
incremental prefill against a cached context; hot-mode wedges are faster in absolute time, 5-11 s
after task launch after hours of load, 5-77 s over the full T3 record, but a different regime; cold
prefills wedge 26.1-31.6 min into the prefill)".

### Blocker: boot-0 wedges #4-#6 ownership contradicts T5-correlation, and no checkpoint correlates them
**Severity:** blocker
**Where:** `planning/docs/TASK-0010-evox2-gpu-wedge-fix.md:1244` (T5-correlation verdict) vs 15-20 (`## Status`, 2026-09-13 entry); no `## Implementation` checkpoint covers Sep 12 16:04/16:31/17:00 UTC
**Problem:** T5-correlation concludes the ~197-200k owning session's turn died after wedge 3 with no retry and the endpoint ran small-context traffic; the Sep 13 Status entry attributes the next three wedges to 'the same ~200k-context retry loop' with 'the same ~200k cached context, running 7 h' (owner 'unattributable from the journal'), and as written the two checkpoints disagree on whether the owning session was still retrying.
**Failure scenario:** if a different long session owned #4-#6, Status's 'the same' is wrong; if the big session kept retrying, T5-correlation's 'died (no retry after wedge 3)' is wrong. Either way Big cannot re-verify the 6-wedge boot-0 accumulation the trigger sentence leans on ('2.7 min after 6 this boot'), because the #4-#6 correlation (ring, pid, in-flight task, context size) is not in `## Implementation` and the T3 'final' UTC wedge list predates all seven boot-0 wedges.
**Suggested direction:** one fresh small-context Tails session re-correlates #4-#6 from the boot-0 kernel journal + iq4xs user journal with the T5-correlation method, writes a checkpoint in `## Implementation`, and states which claim holds; if client identity is genuinely unattributable from the journal (the record's own stated limitation), record that explicitly and note the Status wording conflict in `## Implementation` (Status is Robotnik's section; name the conflict, do not edit it).
**Resolution:** fixed (Tails, 2026-09-13, fix round 1): new "T5-correlation addendum: boot-0 wedges
#4-#6" checkpoint in `## Implementation` (this doc) — per-wedge table (rings, pids, in-flight
tasks, context sizes, modes), the 172,727-token prefill that created the ~200k context on pid 7434
(00:00-00:32 JST Sep 13, completed clean), the retry cadence (27 m 38 s / 28 m 10 s, matching
#2->#3's 27 m 34 s), and the session-identity determination: the #4-#6 loop is a **different**
session from the #1-#3 loop (172,727 < 196,608 with compaction disabled; the journal carries no
client identity, per-session attribution flagged as inference). T5-correlation's "no retry after
wedge 3" stands for the #1-#3 owner; the `## Status` wording conflict ("the same ~200k cached
context, running 7 h") is named in the checkpoint (Status not edited, it is Robotnik's section).
Trigger sentence checked against the new evidence and not corrected (all new data points sit inside
the stated trigger).

### Stage 2 revert: `dnf reinstall` does not take a local rpm file path
**Severity:** should-fix
**Where:** `planning/docs/TASK-0010-evox2-gpu-wedge-fix.md:555` (Stage 2 revert); 1403 (T6 draft); fixes doc `qwen38-q5-fixes.md:227`
**Problem:** `dnf reinstall /tmp/rpmbak2/<backed-up rpm file>` is not a valid dnf spec; reinstall resolves package names from repositories, and a local file path fails with 'No match for argument'.
**Failure scenario:** inside the window, `dnf update $PKG` runs, then the revert step errors before the backed-up rpm is restored; the host is left on a different Mesa than the backup with no working one-line restore, and the window's revert procedure is not trustworthy.
**Suggested direction:** restore from the file with `rpm -Uvh --force /tmp/rpmbak2/<file>`, or verify the dnf local-file reinstall syntax on the host before the window and record what actually works.
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

### Stage 2 apply is a guaranteed no-op on Rocky per the T4 evidence
**Severity:** should-fix
**Where:** `planning/docs/TASK-0010-evox2-gpu-wedge-fix.md:555` (Stage 2 Change + Apply cells); T4 record at 1130, 1160-1166
**Problem:** T4 establishes no Mesa newer than 25.2.7 exists in any Rocky repo (appstream frozen at 25.2.7; elrepo and epel carry no mesa), so `dnf update $PKG` has nothing to update and the verify cell ('vulkaninfo shows the new RADV version') can never pass; the row is staged 'live' with a change it cannot make.
**Failure scenario:** the user approves the Stage 2 window; the window runs; `dnf update` reports no packages marked for update; verification fails; the only effective Mesa paths (Stage 4 / Fedora 44, or a self-build) were already known at staging time, so the window was consumed by a no-op.
**Suggested direction:** relabel Stage 2 as dormant on Rocky with the Mesa path stated as Stage 4 (Fedora 44) or a documented self-build, or make the apply step the self-build; if the dnf attempt should still run, mark its expected outcome 'no-op' in the cell.
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

### Stages 1 and 4 verify against 11.87 t/s, a Q4-model baseline, not iq4xs
**Severity:** should-fix
**Where:** `planning/docs/TASK-0010-evox2-gpu-wedge-fix.md:554, 557` (verify cells); 1402, 1405 (T6 draft); plan template at 336; fixes doc `qwen38-q5-fixes.md:226, 229`
**Problem:** 't/s within 20% of baseline 11.87' uses the Q4_K_XL decode baseline from checkpoint 3.4 (2026-08-27, Q4 service, line 801); the service being fixed is iq4xs (IQ4_XS), whose recorded decodes this boot are 9.82-12.31 t/s depending on context (T5-H2 1327, T5-correlation 1209, 1225).
**Failure scenario:** a Stage 1 llama.cpp version bump that shifts iq4xs decode by 15% is judged against a different model's number, so the verify can report the fix broken (or fine) for a reason unrelated to the change.
**Suggested direction:** record an iq4xs t/s baseline (prefill + decode under the same small-context workload) in the doc before the window and use it in the Stage 1/4 verify; the 'before' reading the verify already requires can be promoted to the recorded baseline.
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

### H5 verdict cites the wrong location and a stale window
**Severity:** should-fix
**Where:** `planning/docs/TASK-0010-evox2-gpu-wedge-fix.md:1366` (T6 H5 cell)
**Problem:** the cell cites 'Test Results row 2, line 1370'; Test Results row 2 is at line 1517, line 1370 is inside T6's own section, and row 2's '0 events in 2 d 9 h' window is the 2026-08-25 measurement (previous boot, Aug 23-25), not the current 51-wedge journal.
**Failure scenario:** Big re-verifying H5 follows the citation, lands inside T6's ambiguity note at line 1370, finds no throttle count, and cannot confirm the verdict from the cited evidence; the actually deciding per-wedge evidence (T3 ±60 s check, 'no thermal, no power events' around all 51 wedges, lines 992-994) is not cited.
**Suggested direction:** re-cite to the T3 ±60 s check plus the T5-H2 wedge-moment sensor rows (edge 80-87 C, lines 1304-1306); the verdict itself is supported, only the citation is wrong.
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

### H1 cell attributes to T3 a 'known gfx1151 bug' classification T3 never made
**Severity:** should-fix
**Where:** `planning/docs/TASK-0010-evox2-gpu-wedge-fix.md:1362` (T6 H1 cell)
**Problem:** 'whether it matches a known amdgpu gfx1151 bug is T3's classification' misstates T3, whose classification is the signature classes (A ring-reset-recovered 47, B ring-reset-failed 4, C fence fallback 58, lines 976-980); no checkpoint in the record establishes a match to a known gfx1151 bug.
**Failure scenario:** a re-verifier looks in T3 for the bug-match statement, finds only the A/B/C table, and either wrongly 'confirms' the known-bug branch of the matrix or has to redo a search the record never performed; the H1 verdict (undetermined, neither branch met) is correct, but the evidence cell overstates what T3 established.
**Suggested direction:** reword to 'T3 classified the signature shape; no record in the doc establishes a known-bug match; the known-bug branch of the matrix remains open'; the verdict and the Stage 3 decider are unchanged.
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

### H2 cell omits the unmet 'shaped like a ~201k cold prefill' matrix condition
**Severity:** should-fix
**Where:** `planning/docs/TASK-0010-evox2-gpu-wedge-fix.md:1363` (T6 H2 cell); matrix condition at 288; deviation of record at 1282-1287
**Problem:** the matrix's supported condition requires the workload to be 'shaped like a ~201k cold prefill'; the record's deviation of record states every pure-compute variant pinned at exactly 100.0 W, ~20 W below the prefill's 119-120 W plateau, with a kernel mix (int ALU, LDS, exp, deep queue) the repro does not replicate; the H2 cell acknowledges only the llama-in-the-loop gap.
**Failure scenario:** a later reader of the H2 verdict (or of the fixes doc verdict table) infers the repro matched the prefill's power profile and over-credits 'partially supported'; the Stage 2 'live' status rests on the over-stated H2.
**Suggested direction:** add the shape/power mismatch to the H2 evidence cell ('the workload reached the 100 W pure-compute plateau, not the prefill's 119-120 W profile, per the T5-H2 deviation of record').
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

### One-sentence trigger mislabels the power regime and the fresh-chip range
**Severity:** should-fix
**Where:** `planning/docs/TASK-0010-evox2-gpu-wedge-fix.md:1382-1389` (T6 trigger); fixes doc `qwen38-q5-fixes.md:199-204` carries it verbatim
**Problem:** (a) the sentence opens 'at or near the 120 W cap' and then exemplifies with 'a 100 W-pinned pure-compute plateau'; 100 W is the record's pure-compute demand ceiling, ~17% below the cap (deviation of record, lines 1282-1287). (b) '(fresh chip 26.1-31.6 min)' mislabels the range: 26.1-31.6 min is T3's cold-mode range across all 39 cold wedges on mixed chips (lines 1077-1078); the fresh-chip data point is a single 29.3 min (1760 s, lines 656-661, 821-825).
**Failure scenario:** the DoD box 2 check ('the trigger is stated in one sentence, backed by the wedge-timestamp correlation') fails on inspection: the sentence's two power figures (120 W cap vs 100 W plateau) and its fresh-chip range do not match the cited records; the trigger is the headline result the user is asked to approve a window on.
**Suggested direction:** reword the power clause to cover both plateaus ('~100 W pure-compute plateau or ~120 W prefill plateau'), and the accumulation clause to 'cold prefills wedge at 26.1-31.6 min (fresh chip: single 29.3 min repro) → 2.7 min after 6 prior wedges on this boot (T5-H2)'; update the fixes doc copy in the same pass.
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

### DoD box 1 ('each hypothesis supported or excluded') is not met by the T6 verdicts
**Severity:** should-fix
**Where:** `planning/docs/TASK-0010-evox2-gpu-wedge-fix.md:169` (DoD box 1); 1360-1366 (T6 verdict table)
**Problem:** the box requires every hypothesis to be 'marked supported or excluded'; T6 marks H1 undetermined, H2 partially supported, H3 neither - three of five sit in a third state the box does not provide for.
**Failure scenario:** at DoD close the box cannot be ticked from the record as written: Knuckles's 'verify the DoD checklist is fully ticked' (Next Actions) stalls on box 1 even though the T6 verdicts are the honest terminal state of a read-only investigation.
**Suggested direction:** Robotnik (DoD owner) either amends box 1 to accept 'undetermined + decider stage recorded' as a terminal state for this task, or keeps it open until Stage 3 runs and the H1/H2/H3 split resolves; record the decision in the box's note.
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

### `## Test Results` is stale: it still says the mitigation evidence is 'NOT yet executed'
**Severity:** should-fix
**Where:** `planning/docs/TASK-0010-evox2-gpu-wedge-fix.md:1522-1526` (Test Results, 'Checks requested vs run'); DoD box 4 at 179 and box 7 at 187
**Problem:** box 4 points at `## Test Results` for the runtime-mitigation evidence and box 7 requires wedge-triggered auto-restarts to be 'counted in ## Test Results'; the section is the 2026-08-25 record and still says 'mitigation before/after under equivalent load NOT yet executed' (line 1524), while the runtime surface was exhausted on 2026-08-27 (checkpoint 3.3/3.4: every knob EINVAL or unusable, `low` rejected at 4.5x, wedge count 0 through the runs) and the T5-H2 run has before/after counts (6→7, lines 1299-1303) - none of it in `## Test Results`.
**Failure scenario:** Big's re-verification (box 13) and the DoD close look at `## Test Results` for the mitigation + restart-count evidence, find the stale 'NOT yet executed' line, and either drop the checks (forbidden by box 13: 'no silently dropped checks') or have to re-derive the verdicts from `## Implementation` against the section's own claim.
**Suggested direction:** Tails/Big add a final 2026-09-12/13 row-set to `## Test Results` (or correct line 1524): the runtime-surface exhaustion with the deciding probes, the T5-H2 before/after wedge counts, and the boot-0 wedge-triggered restart count (7 by T5-H2, NRestarts 6→7, one per wedge), each pointing at the Implementation checkpoint that records it.
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

### The zero-team-stops check covers boot 0 only, not the iq4xs service's full lifetime
**Severity:** should-fix
**Where:** `planning/docs/TASK-0010-evox2-gpu-wedge-fix.md:1321-1322` (T5-H2 `grep -c "Stopped llama-server"` over the boot-0 user journal); 1197-1199 (T5-correlation, boot 0); DoD box 7 at 187; service start at 1055, 1094-1096
**Problem:** the check was run over the boot-0 user journal (since Sep 12 03:47 UTC), but the iq4xs unit has run since Sep 8 17:32 UTC (boot -1), so the Sep 8 17:32 → Sep 12 03:47 window has no recorded check; manual stops do occur on this host (the q4 unit was manually stopped at Sep 12 12:55:06 JST, provenance unverified, lines 1097-1099).
**Failure scenario:** a team-initiated stop of iq4xs in the Sep 8-12 window (e.g. during the q4→iq4xs cutover) violates box 7's 'zero allowed' but is invisible to the record; the box gets ticked on partial evidence.
**Suggested direction:** extend the same `Stopped` grep to boot -1 for the iq4xs unit (`journalctl --user -b -1 -u llama-server-qwen3.8-27b-iq4xs.service`) and record the count in a checkpoint or `## Test Results`.
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

### T6's line citations are stale after the doc grew
**Severity:** nit
**Where:** `planning/docs/TASK-0010-evox2-gpu-wedge-fix.md:1350-1351` (T6 scope), 1364, 1365, 1366, 1382, 1393, 1407, 1423
**Problem:** T6 cites 'Plan (lines 259-376)' (now 263-379), 'Plan line 285' for the -fa note (now 289), and 'T5-H2 ... lines 1244-1326' (now 1255-1346); the 4-20 line offsets mean the doc was edited after T6 was written (T7's staged-table insertion and other growth) without refreshing the citations.
**Failure scenario:** a re-verifier jumping to 'Plan line 285' lands on the H2 row instead of the H3 row; jumping to 'line 1370' (the H5 citation) lands inside T6's own section; minor, but it costs time on every re-verification.
**Suggested direction:** refresh T6's line citations in the same pass that fixes the findings above, or cite by section name only.
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

### Post-window review (Shadow, 2026-09-13, after W1-W3): window executed per the staged section; 3 blockers resolved, 11 initial-review findings still open, 4 new findings

Scope read this round: staged section (644-663), W1-W3 (1648-1795), T5-H2 outcome (1396-1450), T6 (1452-1532), T7 (1534-1577), the T5-correlation addendum (1579-1646), DoD (243-283), Test Results (1974-1997), the T3 clause at 1195-1197, and the fixes doc
`/home/howard/AI/projects/qwen-38-q5-fixes/qwen38-q5-fixes.md` in full (current state, 235 lines). T1-T4, T5-correlation, and Attempt 3/4 regions were not re-read this round; their verification stands on the initial review (1801-1817).

### W3 monitor's recorded count command is unscoped, but the t=0 value only fits a boot-scoped count
**Severity:** should-fix
**Where:** `planning/docs/TASK-0010-evox2-gpu-wedge-fix.md:1774` (t=0 value); 1782 (count command)
**Problem:** the checkpoint defines the monitor's count as `journalctl -k --no-pager | grep -cE "device wedged"` (no boot scope), but the monitor's first tick recorded `wedge_count=0` and the checkpoint reconciles that with "0 since boot" — an unscoped grep over the full journal would return the cumulative count (at least 51, the T3 record of 51 full wedges across boots -4..0, plus the 15 of the Aug 23-25 boot per Test Results row 1), not 0.
**Failure scenario:** at the 2026-09-14 22:44 JST hard stop the monitor appends its final line, and the staged Stage 3 verify ("24 h wedge count under the same workload on the new kernel", staged section 657) is read from it. If the script is boot-scoped (as the t=0 value implies) but the reader trusts the recorded command (cumulative), the final number is misread by tens; if the script is cumulative and the t=0 "0" is a mis-record, the baseline is wrong. Either way the Stage 3 verification number is not interpretable from the record as written.
**Suggested direction:** in the post-monitor checkpoint, quote the script's exact journal line (the script is on EVO-X2 at `/tmp/wedge_monitor_w3.sh`, 1446 bytes, still present per W3:1776-1779), state the boot scope explicitly, and reconcile the t=0 value against the known cumulative vs since-boot counts.

### W1 records only the t/s half of the staged Stage 1 verify; the user-applied Stage 1 change has no recorded backup or deployment timestamp
**Severity:** should-fix
**Where:** `planning/docs/TASK-0010-evox2-gpu-wedge-fix.md:1648-1683` (W1); staged Stage 1 cell at 655; DoD box 8 at 269-273
**Problem:** the staged Stage 1 verify is "24 h wedge count under the same workload before and after AND decode t/s within 20% of baseline"; W1 ran only the t/s half (11.95 t/s at ~57.9k context, PASS, 1674-1678). For the user-applied change (build 2000 binary, `-c 98304`, 1677-1678) there is no 24 h wedge-count before/after pair, no record of the staged pre-change backups (`/tmp/llama-unit.bak1.<ts>`, `/tmp/cmdline.bak1` per the staged backup cell), and no deployment timestamp for build 2000 anywhere in the doc.
**Failure scenario:** Big's re-verification (DoD box 13) looks for the Stage 1 before/after wedge pair and finds none, and cannot split the 10 boot-0 wedges (W2:1694) into pre- and post-Stage 1 because the deployment time is unrecorded; and if build 2000 later misbehaves, the staged revert cell (655) is not executable as written because `/tmp/llama-unit.bak1.<ts>` does not exist in the record, so the documented revert has nothing to restore.
**Suggested direction:** one checkpoint (or a W1 addendum) recording: the build 2000 deployment time (unit file mtime or the unit's Started lines in the journal), the wedge count before and after that time, and the location of any unit/cmdline backup the user kept (or an explicit statement that none was kept, per DoD box 8).

### Fixes doc still says "NOTHING APPLIED" after Stages 1 and 3 were applied
**Severity:** should-fix
**Where:** `/home/howard/AI/projects/qwen-38-q5-fixes/qwen38-q5-fixes.md:216-218` ("STAGED - awaiting user approval; NOTHING APPLIED"; "Nothing below has been executed")
**Problem:** the fixes doc's staged-solution section still carries the pre-window header, but Stage 1 was applied by the user (W1:1677-1678) and Stage 3 was applied in the approved window (W2:1685-1750; kernel 7.2.5 live per W3:1762-1765).
**Failure scenario:** the fixes doc is the standalone artifact DoD box 8 (269-273) points at; a reader (user or agent) consulting it after the window sees Stage 3 as unapplied and either re-runs the apply (reboot + grub default change on a host already booted into 7.2.5) or reports the wrong current state at DoD close.
**Suggested direction:** update the fixes doc header to the applied state (Stage 1 user-applied with the W1 t/s PASS; Stage 3 applied 2026-09-13 21:25 JST, 7.2.5 live, 24 h verify pending the monitor) and record the update in a checkpoint with the T7 pattern (backup of the pre-edit file + `git hash-object`).

### W3 monitor is a nohup process, not a service; a host reboot inside the 24 h window kills it without re-arm
**Severity:** nit
**Where:** `planning/docs/TASK-0010-evox2-gpu-wedge-fix.md:1776-1785` (W3)
**Problem:** the monitor runs under nohup with no systemd unit and no documented restart; if EVO-X2 reboots during the window the monitor dies and nothing re-arms it.
**Failure scenario:** the host reboots at hour 12 of the 24 h (power loss, user action, kernel panic); the final `wedge_count=` line never appears, the Stage 3 verify has no number, and the gap is only discoverable by noticing the missing 300 s ticks in the log.
**Suggested direction:** state the gap check (log ticks, 300 s cadence) explicitly in the post-monitor checkpoint's plan, or run the monitor as a transient systemd user service with `Restart=on-failure`; either way, record which in the next checkpoint.

### Initial-review finding status (post-window, 2026-09-13)

| # | Finding (initial review, 1801-1955) | Status | Where it stands now |
|---|---|---|---|
| B1 (1819) | Stage 3 sets the wrong boot entry | **Resolved** | staged 657 + T6 draft 1508 + fixes doc 228: set-default by exact BLS identifier, N=1 guard, `saved_entry` confirm; executed per W2:1726-1734 (N=1, BLSID recorded, confirm recorded); revert reads the saved identifier from `/tmp/grubdefault.bak3` (W2:1736-1746) |
| B2 (1838) | "fastest wedge ever recorded" superlative | **Resolved** | T5-H2 1431-1434, T6 H2 cell 1467, fixes doc 192: now "fastest cold-mode-class wedge" with the hot-mode contrast (5-11 s after launch; 5-77 s over the T3 record; different regime) |
| B3 (1851) | boot-0 wedges #4-#6 ownership | **Resolved** | addendum 1579-1646: per-wedge table, the 172,727-token prefill (00:00-00:32 JST Sep 13) that created the ~200k context, retry cadence 27m38s/28m10s vs #2->#3's 27m34s, #4-#6 = a different session from #1-#3 (size arithmetic, compaction disabled); the `## Status` wording conflict named, not edited (1629-1635) |
| SF1 (1869) | `dnf reinstall` takes no local rpm path | Open | staged 656, T6 draft 1507, fixes doc 227 all still `dnf reinstall /tmp/rpmbak2/<file>`; Resolution line unfilled; closes with `rpm -Uvh --force` (or a host-verified dnf local-file syntax) in all three cells |
| SF2 (1877) | Stage 2 apply is a guaranteed no-op on Rocky | Open (mitigated) | the Change cell carries the T4 note since T7 (656; T7:1562-1566) but the row is still "(live: H2 partially supported)" and the apply cell has no expected-no-op note; closes by relabeling dormant or marking the expected outcome |
| SF3 (1885) | Stage 1/4 verify cites 11.87 (Q4 baseline) | Partially resolved | the iq4xs baseline is recorded (W1:1655-1659: decode 12.1-12.3 t/s at ~58-60k context, prefill 180.9 t/s) and W1 verified against it (PASS); the verify cells still cite 11.87 in staged 655/658, T6 draft 1506/1509, fixes doc 226/229 |
| SF4 (1893) | H5 cell cites wrong location and stale window | Open (mitigated) | H5 cell 1470 still cites "Test Results row 2, line 1370" (line 1370 is inside the T5-H2 checkpoint, not Test Results); the T5-H2 wedge-moment sensor evidence was added (edge 80-87 C, 100.0 W) but the T3 ±60 s check (992-994) is still not cited |
| SF5 (1901) | H1 cell attributes a "known gfx1151 bug" classification to T3 | Open | H1 cell 1466 unchanged: "whether it matches a known amdgpu gfx1151 bug is T3's classification" |
| SF6 (1909) | H2 cell omits the unmet shape/power condition | Open (mitigated) | H2 cell 1467 states "PPT pinned 100.0 W" but does not contrast it with the prefill's 119-120 W profile nor cite the T5-H2 deviation of record (1383-1388) |
| SF7 (1917) | Trigger mislabels the power regime and fresh-chip range | Open | T6 1486-1493 and fixes doc 199-204 unchanged ("at or near the 120 W cap" ... "a 100 W-pinned pure-compute plateau"; "fresh chip 26.1-31.6 min"); the addendum explicitly leaves it open (1640-1641) |
| SF8 (1925) | DoD box 1 not met by the T6 verdicts | Open | box 1 (248-251) unchanged; H1 undetermined / H2 partially supported / H3 neither; closure path is now concrete: post-monitor verdict update for H1 + Robotnik's box-1 wording decision |
| SF9 (1933) | `## Test Results` stale | Open | 1974-1997 unchanged: "mitigation before/after under equivalent load NOT yet executed" (1992) and "fixes-doc update is pending" (1993, since done by T7) |
| SF10 (1941) | zero-team-stops check covers boot 0 only | Open | the `Stopped llama-server` greps remain boot-0-only (1422, 1457, 1539); no boot -1 check in W1-W3; closes with the boot -1 grep for the iq4xs unit recorded in a checkpoint |
| nit (1949) | T6 line citations stale after doc growth | Open | T6 1454-1455 still cites "Plan (lines 259-376)" (Plan is at 364) and "lines 1244-1326" (T5-H2 is at 1356); new instance: W1:1652 cites the review finding at line 1717 (it is at 1885) |

### W1/W2/W3 execution record vs the staged section

- **W1 (Stage 1, user-applied change).** Verification-only; the service was never touched by Tails (1650-1653, 1681). Matches the staged verify's t/s intent but against the iq4xs baseline (see SF3). Gaps recorded as findings above: the 24 h wedge-count half of the staged verify, the staged pre-change backups, and the build 2000 deployment timestamp are not in the record.
- **W2 (Stage 3).** Matches the staged cell command-for-command. All three staged backups taken with the exact staged paths; `grubdefault.bak3` content recorded (1698-1704). Repo enable: staged "enabled=0 -> enabled=1" done via a section-scoped sed because `dnf config-manager` is not installed, diff-verified to exactly one line (1708-1713). Install: the exact planned version 7.2.5-1, installonly, 7.0.12 kept (1714-1716). BLS: guard N=1 passed, BLSID derived, `saved_entry` confirmed before the reboot (1726-1734) — the blocker 1 resolution executed as designed. Revert: staged revert documented verbatim with the real `OLDSAVED` value (the 7.0.12 identifier from the backup); the old kernel was never removed (1736-1746). Two additions, both honestly labeled as not staged steps: the pre-install availability check (1705-1707) and the DKMS `ryzen_smu` side effect with analysis (`modinfo` evidence that the in-kernel amdgpu driver is unaffected), the deliberate decision not to build mid-test, and the remedy note carried to W3 (1716-1725). The reboot was issued only after the checkpoint was written and flushed, and the expected session deaths are recorded as expected and approved (1748-1750).
- **W3 (post-reboot).** Staged Stage 3 verify item 1 met: `uname -r` = 7.2.5-1.el10.elrepo.x86_64, service active (auto-started), 8093 listening, `-c 98304` intact, binary build 2000/5266f24d confirmed via `/proc/PID/exe` and matching the W1 fingerprint (1761-1773). Item 2 (24 h wedge count) in progress via the bounded monitor: pid 6647 (cross-verified three ways), hard stop 2026-09-14 22:44:43 JST, 300 s cadence, `err-journalctl` defensive branch (1774-1785); the count-scope ambiguity is recorded as a finding above. The `ryzen_smu` note carried from W2, left as-is with the rationale (1786-1789).
- **Verdict on the execution record:** the window was executed per the staged section; all staged backups were taken; the revert is documented and executable (backups on EVO-X2, old kernel kept); the two deviations (sed instead of config-manager; the BLS guard run as an atomic script) are documented, minimal, and verified by diff and confirm steps.

### Overall verdict on the implementation evidence (T1-T7 + W1-W3)

The record is coherent and complete as a read-only investigation plus one applied window. The chain holds end to end: the T3 forensics (51 wedges, two modes, the retry-loop correlation) → the T5-H2 controlled repro (a non-llama RADV stressor wedged the chip; the kernel's attribution of the hung job to llama-server weighed as victim-not-cause, T6 1472-1484) → the T6 third-state verdicts (honest terminal states for a read-only investigation) → the T7 staged table with complete backup/apply/verify/revert cells → the W2 command-for-command application → the W3 post-reboot verification. The blocker 3 addendum closes the last correlation gap (#4-#6 ownership) and names the `## Status` conflict without editing it (1629-1635). The T3 clause "iq4xs has wedged zero times" (1195-1197) is scoped by its tail clause to the small-context safe-regime workload and does not contradict the boot-0 wedge record.
No new blockers. Open items: the 10 initial-review should-fixes + 1 nit (three of them partially mitigated, per the status table) and the 3 new should-fixes + 1 nit above. DoD box 11 (278, "no unresolved blockers or should-fix findings") is therefore not yet met. None of the open items affect the physical state of the host (7.2.5 live, service active on 8093, `-c 98304` intact, monitor running with a hard stop) or the executability of the Stage 3 revert. The H1 deciding test has run but not resolved: the Stage 3 verification number is the monitor's final line at ~2026-09-14 22:44 JST (W3:1791-1793), and DoD box 1 (SF8) has a defined closure path from there.

### Post-window review verification (Shadow, 2026-09-14): deliverables (1)-(3) verified against the current doc state; no new blockers; 2 new nits

Re-verification of the post-window review above (1970-2032). The doc gained 13 lines above W1
after that review was written (its scope line cites W1 at 1648; W1 is now 1661; the same +13 holds
across the initial-review, addendum, T6/T7, and W2/W3 citations). Read this round: staged section
(657-677), W1 (1661-1696), W2 (1698-1770), W3 (1772-1808), T5-correlation addendum (1592-1659),
Test Results (2051-2075), the `## Changes` table (678-684), and the fixes doc
`/home/howard/AI/projects/qwen-38-q5-fixes/qwen38-q5-fixes.md` current state (185-235, file ends
at 235).

**Deliverables (1)-(3) stand; their claims check out against the current doc state.**

- (1) Finding status (2003-2020). B1: the BLS step is at 1739-1747 (N=1 guard, BLSID recorded,
  `saved_entry` confirm) and the revert at 1749-1759 reads `OLDSAVED` from the recorded
  `/tmp/grubdefault.bak3` content (1714-1716); resolved in W2 by design, as claimed. B2: the
  corrected "fastest cold-mode-class wedge" wording with the hot-mode contrast is verified in the
  fixes doc H2 cell (192); the T5-H2 and T6 cells stand on the initial round's verification, not
  re-read this round. B3: the addendum (1592-1659) carries the per-wedge table, the 172,727-token
  prefill created 00:00-00:32 JST (1611-1621), the retry cadence 27m38s/28m10s vs 27m34s
  (1633-1635), the session-identity arithmetic (1623-1631), and the named-not-edited `## Status`
  conflict (1642-1648); resolved as claimed. SF1-SF10 and the nit remain open as the table states;
  spot-verified this round: `dnf reinstall /tmp/rpmbak2/<file>` still in staged 669 and fixes doc
  227 (SF1); Stage 2 row still "(live: H2 partially supported)" with no expected-no-op note
  (SF2, staged 669); 11.87 baseline still in staged 668/671 and fixes doc 226/229 (SF3); "at or
  near the 120 W cap" and "fresh chip 26.1-31.6 min" unchanged in fixes doc 199-204 (SF7); H1
  undetermined / H2 partially supported / H3 not excluded, not supported per fixes doc 191-193, so
  DoD box 1 remains unmet (SF8); Test Results still "NOT yet executed" and "fixes-doc update is
  pending" (2069-2070, SF9). SF4, SF5, SF6, SF10 not re-read this round; their open status stands
  on the post-window review.
- (2) Execution record (2022-2027). W2 matched the staged cell command-for-command with the two
  documented deviations (section-scoped sed, diff-verified to one line, 1721-1726; BLS guard run
  as an atomic script, 1739-1740); all three staged backups taken at the staged paths with the
  timestamp (1711-1717); the revert is documented with the real `OLDSAVED` value and the old
  kernel was never removed (1749-1759). W1 was verification-only: no service touch (1663-1666,
  1694-1695), t/s PASS against the iq4xs baseline (1668-1691); its gaps (the 24 h wedge pair, the
  staged pre-change backups, the build 2000 deployment time) remain open per the finding at 1982.
  W3 met the staged verify item 1 with the binary fingerprint cross-check (1774-1786) and item 2
  is in progress under the bounded monitor (1787-1798).
- (3) Overall verdict (2029-2032). Consistent with everything re-verified this round. Host state
  not re-probed (no live EVO-X2 access from this toolset); the standing state is the W3 record
  plus the dispatch brief: 7.2.5 live, service on 8093, monitor to the 2026-09-14 22:44:43 JST
  hard stop.

**Open until the post-monitor checkpoint:** the Stage 3 verification number is the monitor's final
`wedge_count=` line; before it is used, record the script's exact count command line and boot
scope (finding 1975), and update the fixes doc header (finding 1989) and Test Results (SF9) in
the same pass. No new blockers; DoD box 11 (no unresolved blockers or should-fix) remains unmet
while the 11 initial-review findings and 4 new findings stay open.

### Post-window review line citations are uniformly stale (+13) against the current doc
**Severity:** nit
**Where:** `planning/docs/TASK-0010-evox2-gpu-wedge-fix.md:1972-2032`
**Problem:** 13 lines were inserted above W1 after the post-window review was written, so every
line citation in it points 13 lines early; citations to sections below the Review additionally
carry the review block's own length.
**Failure scenario:** a re-verifier following "W2:1726-1734" for the BLS guard lands on the dnf
install / DKMS text (the BLS step is now 1739-1747); following "Test Results (1974-1997)" lands
inside the post-window review's own section (Test Results is now 2051); following "initial review
(1801-1817)" lands on the tail of the initial nit (the verdict is now 1814-1830).
**Suggested direction:** refresh the citations in the pass that closes the other open items, or
replace line numbers with section-name citations ("W2 BLS step", "Test Results 'checks requested
vs run' paragraph").
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

### `## Changes` table still says "no changes yet (read-only so far)" after Stage 3 was applied
**Severity:** nit
**Where:** `planning/docs/TASK-0010-evox2-gpu-wedge-fix.md:682`
**Problem:** the EVO-X2 Changes row carries the diagnosis-phase header, but Stage 3 was applied in
the window (kernel-ml 7.2.5 installed, `saved_entry` changed, elrepo-kernel repo enabled; W2
1700-1763).
**Failure scenario:** a reader scanning `## Implementation` for what changed on the host stops at
the Changes table (the section's first summary table) and concludes EVO-X2 is unchanged,
contradicting the W2/W3 checkpoints ~900 lines below.
**Suggested direction:** Tails updates the row in the post-monitor pass: EVO-X2 now carries
the Stage 3 change set (kernel, grubenv, repo file) with the W2/W3 checkpoint references; the sysfs
claim can stay scoped to sysfs if that is what was meant.
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

### Attempt 2 verification (Shadow, 2026-09-14, re-dispatch after the attempt 1 window-exhaustion death)

Scope: verify the three blocker fixes (B1-B3) landed as specified in their Resolution lines,
re-confirm the open should-fix/nit state against the current doc, and compare the window changes
(Stage 1: llama.cpp v0.4.0 build 2000 / commit 5266f24d + `-c 98304`; Stage 3: grub default to
7.2.5 by exact BLS identifier + reboot) against `## Definition of Done` (275-314) and the
`## Implementation` records (T6 adjudication, staged section, W1/W2/W3 checkpoints). Read
discipline: grep-first (`rg -n`), chunked reads of ~200 lines; no full-doc read. Live EVO-X2
state is not re-probed from this toolset (no ssh in Shadow's permissions); that is Big's
box-13 job. Findings below are recorded pass by pass as each completes, so a mid-review death
leaves verified results in the doc.

**Pass 1 (done): Review-section state + staged section (676-695) + `## Changes` header (697-699).**
Staged Stage 3 (689) carries the B1 fix in its final form: default set by exact BLS entry
identifier derived from `/boot/loader/entries/` with the `N=1` guard, `grub2-set-default "$BLSID"`,
`grub2-editenv list` confirm of `saved_entry=$BLSID` before `reboot`; the revert reads `OLDSAVED`
from `/tmp/grubdefault.bak3`; the repo-file placeholder is resolved to
`/etc/yum.repos.d/elrepo.repo` `[elrepo-kernel]` `enabled=0`. Staged Stage 1 (687) and Stage 2
(688) retain the open should-fix defects exactly as the status table (2026-2039) states: 11.87
baseline in the Stage 1/4 verify cells (687, 690) and `dnf reinstall /tmp/rpmbak2/<file>` in the
Stage 2 revert (688). The `## Changes` table (697+) is checked for the 2117 nit in the next pass.

**Pass 2 (done): `## Changes` table (697-703) cross-check for the 2117 nit.**
Nit confirmed; remains open as a nit. Line 701 is unchanged: `| EVO-X2 sysfs | **no changes yet**
(read-only so far) |`. The sysfs scope itself is net accurate: checkpoints 3.3/3.4 (880-943) wrote
to sysfs as root (`power_dpm_force_performance_level` auto/low/high/manual verified by write +
readback, the `low` probe, `pp_dpm_sclk` / `pp_od_clk_voltage` EINVAL probes) and reverted
everything to `auto` (verified after each experiment, 915-916, 943) against the prior state at
633-652; the net sysfs state equals the pre-task state, but "read-only so far" understates those
transient writes. The nit's host-level scenario holds: the table (699-703) lists only sysfs, the
three diagnosis scripts, and this doc; the Stage 1 change set (unit `ExecStart`: build 2000
binary + `-c 98304`, user-applied per W1) and the Stage 3 change set (kernel-ml 7.2.5-1
installed, `saved_entry` set to the 7.2.5 BLS identifier, `[elrepo-kernel]` enabled=1, per W2)
and the W3 monitor script `/tmp/wedge_monitor_w3.sh` are absent from the table. Scope note for
Tails's update pass: the nit's Where line (682) and the verification round's own scope citations
(2057-2060) are +19 stale against the current doc (row now at 701; staged 676-695, W1 1680-1716,
W2 1717-1790, W3 1791-1828, Changes 697-703, Test Results 2170) — same stale-citation class as
the 2102 nit; refresh in the same pass.

**Pass 3a (done): DoD (275-315) + T6 adjudication (1484-1564) cross-check against the window
changes.**
DoD box mapping for the applied window: box 5 (staged solution, exact commands/backups/reverts,
user-approved window) met for Stages 1+3 — staged table 685-690 is complete and the user approval
is recorded in `## Status` 107-114 ("go ahead and start this now", both stages in one window, the
Stage 1 vs Stage 3 attribution ambiguity accepted as a recorded decision, 109-111). Box 6 (frozen
config unchanged, or explicit user approval recorded in `## Status`) met for the
`-c 262144` → `-c 98304` change: `-c 262144` is on the staged frozen-flag list (687), the user
confirmed 98304 (Status 97-105) and re-confirmed keeping it over 122880/131072 (Status 57-62);
the staged cell's frozen-flag exception ("unless the user approves a specific frozen-flag
change") is exactly this case. Box 8 (prior-state backups, location recorded; fixes doc updated)
met for Stage 1 — the staged-name backups are recorded in Status 81-84 (`llama-unit.bak1.1789287454`
plus `llama-bin-bak1.1789287454/`, `llama-libs-bak1.1789287454/`, `cmdline.bak1`, build log
`/tmp/llama-build-v0.4.0.log`); the fixes-doc header staleness remains the open 2008 finding.
Box 3 (distro question) met per the T6 distro answer 1527-1531 (stay on Rocky 10; kernel 7.2.5
obtainable via elrepo; Stage 4 dormant). Boxes 1, 2, 4, 7, 9, 10, 11, 12, 13 unchanged from the
prior rounds: box 1 unmet per SF8 (H1/H2/H3 third states; closure path is the post-monitor verdict
plus Robotnik's box-1 wording decision); box 2 per SF7; boxes 4/7 per SF9 + SF10; box 9 met
(baseline count + monitoring command recorded, Test Results 2174-2195 and the W3 monitor); boxes
10-13 await Vector/Knuckles, this review's close, Omega, and Big. T6 cross-check: the verdict
table (1496-1502) drives the staged rows correctly (H1 undetermined → Stage 3 decider; H2
partial → Stage 2 live; H3 neither → Stage 1 decider; H4 excluded → no unit edit indicated; H5
excluded → no sysfs knob); the B2-fixed superlative wording is present in the T6 H2 cell (1499).
The T6 draft staged table (1536-1541) still carries the open SF1 (1539) and SF3 (1538, 1541)
defects and lacks the T7 Stage 3 additions (repo-file backup + `/etc/yum.repos.d/elrepo.repo`
resolution, 689) — expected, the staged section 685-690 is canonical per T7. The T6 trigger
sentence (1518-1525) still carries the SF7 defects; the T6 scope line citations remain stale per
the open nit. No new T6 defects this pass.

**Pass 3b (done): Stage 1 record (W1 1680-1715 + `## Status` 57-95) verification.**
The Stage 1 change (llama.cpp v0.4.0 build 2000/5266f24d + `-c 98304`) is consistently recorded:
W1 confirms build 2000/5266f24d live on 8093 via `system_fingerprint: b2000-5266f24d` and
`n_ctx` 98304 from `/v1/models` (1699-1700, 1712), t/s PASS at 11.95 t/s against the iq4xs
baseline 12.1-12.3 (1706-1710), service untouched by Tails (1684-1685, 1713-1715). Status records
the application: user-applied between 16:17 and 17:51 JST, unit diff vs backup = only the
`-c 98304` flag, service under the user unit since 17:51:56 JST (77-95). **Correction to the W1
finding at 2001-2006 (post-window round):** two of its three claims are refuted by `## Status`,
which that round's read scope (1991-1992) did not include — the staged pre-change backups ARE
recorded (Status 81-84, staged-name paths matching the staged backup cell 687 plus binary/libs
backups the staged cell does not name) and the build 2000 deployment timestamp IS recorded
(17:51:56 JST, Status 91-92). The open remainder of that finding narrows to: no explicitly
labeled 24 h before/after wedge pair for Stage 1 alone — the record brackets the deployment with
count 10 since boot at 13:20:49 JST (last wedge) and count 10 through the W1 benchmark (Status
50), i.e. zero wedges 17:51:56 → 21:29 JST, and the single-window design makes Stage 1-alone
attribution ambiguous by the recorded decision (Status 109-111); the W3 monitor is the 24 h
verification for the combined window state. Resolution direction for Tails: point the finding's
Resolution at Status 81-84 and 91-92 for the two refuted claims and record the 10→10 bracket as
the Stage 1 before/after evidence.

**Pass 3c (done): Stage 3 record (W2 1717-1789) verification.**
Verified against the staged Stage 3 cell (689): all three staged backups taken at the exact staged
paths with contents recorded (kernels 16 packages incl. 7.0.12, `grubdefault.bak3` holding
`saved_entry=...7.0.12...`, repo backup; 1730-1736); the exact planned kernel 7.2.5-1 installed,
installonly, 7.0.12 kept (1746-1747); repo enable via section-scoped sed because
`dnf config-manager` is absent, diff-verified to exactly one line (1740-1745); the BLS guard ran
with N=1, the exact identifier `aad6cfa1c71c461bbc6543c87712d7f1-7.2.5-1.el10.elrepo.x86_64`
derived, `grub2-set-default "$BLSID"`, and `grub2-editenv list` confirmed `saved_entry=$BLSID`
before the reboot (1758-1766) — the blocker 1 resolution executed as designed. The planned revert
is recorded verbatim with the real `OLDSAVED` value from the backup content, the old kernel was
never removed, and the repo-file restore leaves the enabled/restore choice to the user (1768-1778).
The DKMS `ryzen_smu` side effect is documented with the `modinfo amdgpu` evidence that the in-kernel
driver is unaffected and the deliberate decision not to build mid-test (1748-1757). The reboot was
issued at 21:25 JST only after the checkpoint was written and flushed, session deaths expected and
approved (1780-1782). Wedge count at change time 10 since boot, matching `## Status` (1726), which
closes the pre-deployment side of the Stage 1/3 bracket. No new findings; the two deviations (sed,
atomic guard script) are the minimal documented set.

**Pass 3d (done): post-reboot state (W3 1791-1827) verification.**
Staged Stage 3 verify item 1 met: `uname -r` = `7.2.5-1.el10.elrepo.x86_64`, service
`llama-server-qwen3.8-27b-iq4xs.service` active (auto-started), 8093 listening, pid 1907,
`-c 98304` intact (1794-1797). Binary fingerprint: `version: 0.4.0-dev (build 2000, commit
5266f24d)` via `/proc/1907/exe` → `/usr/local/bin/llama-server`, matching the W1 live fingerprint
b2000-5266f24d (1801-1805). Item 2 (24 h wedge count) in progress under the bounded monitor:
`/tmp/wedge_monitor_w3.sh` (scp'd, 1446 bytes), log `/tmp/wedge-monitor-20260913-224443.log`,
pid 6647 cross-verified three ways, start 2026-09-13 22:44:43 JST, hard stop 2026-09-14 22:44:43
JST, 300 s cadence, t=0 `wedge_count=0` consistent with 0 since boot (1806-1817, 1823-1825). The
recorded count command (1813-1814, `journalctl -k --no-pager | grep -cE "device wedged"`, no boot
scope) plus the t=0 value 0 (1806) corroborate the premise of the open W3 monitor count-scope
finding (1994-1999); its suggested direction (quote the script's exact journal line and boot scope
in the post-monitor checkpoint) is unchanged. `## Status` 28-32 (07:20 JST Sep 14) confirms the
monitor still running with `wedge_count=0` as of this morning; the Stage 3 verification number is
therefore still pending the monitor's final line. No new findings.

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

### Security review (Omega, 2026-09-14)

Scope: attack surface of the EVO-X2 model endpoint (0.0.0.0:8093, llama.cpp), secrets exposure,
supply chain (llama.cpp build 2000 / commit 5266f24d, elrepo kernel 7.2.5-1), and license
compliance. Findings are appended below as each pass settles, one edit at a time.

Method note (2026-09-14): Omega's permission set is read-only repo commands (`git`, `rg`,
`gitleaks`, `trufflehog`, `shellcheck`). Live re-verification on EVO-X2 (ssh) is not available
in this role, so live-state claims rest on the documented evidence cited below (Status 10:46:49
journal warning, unit `ExecStart` verbatim, firewalld reads recorded in TASK-0022). Anything I
could not verify is said so.

### Unauthenticated model endpoint on 0.0.0.0:8093, CORS `*`, no API key
**Severity:** high
**Vector:** authz
**Where:** unit `llama-server-qwen3.8-27b-iq4xs.service` `ExecStart` (verbatim at
`planning/docs/TASK-0010-evox2-gpu-wedge-fix.md:1051` and `TASK-0022-team-model-iq4xs.md:42`,
`--host 0.0.0.0 --port 8093`, no `--api-key`); startup warning recorded at
`planning/docs/TASK-0010-evox2-gpu-wedge-fix.md:31-32` (Status, 10:46:49 JST journal: "CORS is
set to allow all origins ('*') and no API key is set"); firewalld `8093/tcp` open in the `public`
zone on `eno1`, verified 2026-09-09 (`TASK-0022-team-model-iq4xs.md:647-648`).
**Attack:** any principal on the EVO-X2 LAN segment (192.168.1.0/x) — a compromised device, a
guest, or another VM on the same switch — reaches `http://192.168.1.106:8093` with zero
authentication. The server runs `--parallel 1`: one inference slot, no rate limiting. A sustained
stream of `POST /v1/completions` requests starves the single slot; the PM session and every
subagent run on this endpoint, so the attacker halts the whole team on demand (the documented
failure mode where an endpoint death kills the PM session). CORS `*` additionally lets any web
page a host's browser visits issue cross-origin requests and read the responses, i.e. remote
resource abuse without even being on the LAN if a browser on the LAN is the vector.
**Impact:** team-wide denial of service plus model-compute abuse. No direct read of other
sessions' contexts (each request is an independent context; the API does not expose other slots'
prompts), and no code execution — that is why this is high, not critical. Blast radius if abused:
every dispatched task fails or stalls until the server is restarted by a human.
**Fix:** (1) the 10:46:49 warning text references an API-key setting, so this build likely
supports `--api-key`; confirm with `llama-server --help` on the host before staging, and if
present add `--api-key <generated>` to the unit `ExecStart`, restart in an approved window. Store
the key only in the opencode provider config on the team host (env-based if opencode supports
it), never in the README, the planning doc, or any committed file, and never print it under
`set -x`-style logging. (2) Regardless of the key: restrict firewalld `8093/tcp` to the team
host's IP with a rich rule (deny from `not src=192.168.1.102`), keeping the port closed to the
rest of the segment. (3) Record how we would detect abuse: the journal request log lines and the
wedge monitor's cadence already give a footprint; add a note to the monitor log if request-rate
anomalies are observed.

### Attempt 3 (2026-09-14)

Scope: (a) live model-host exposure surface. llama.cpp bound to 0.0.0.0:8093, CORS `*`, no API
key (server startup warning, 10:46:49 JST). Verify current state read-only via
ssh howard@192.168.1.106: which llama ports actually listen, firewalld state. Assess severity.
Stage mitigations (apply nothing). (b) re-verify each pre-existing finding above: resolved /
still-open / stale, with evidence.

Note: the 2026-09-14 method note above ("live re-verification on EVO-X2 (ssh) is not available in
this role") is superseded for this attempt by the dispatch, which grants read-only ssh.

Findings (written as confirmed): see "Findings (attempt 3)" below (F1 still-open high, F2 new
low); evidence trail E1-E3 in between.

Evidence E1 (documented live state, most recent first): `## Status` 22-23 (Robotnik,
2026-09-14 14:31 JST): "0 wedges since boot, 8093 listening (0.0.0.0)". `## Status` 42-44
(Robotnik, 2026-09-14 13:10 JST): llama-server clean-restarted 10:46:49 JST, pid 9144, "8093
listening", unit mtime unchanged 2026-09-13 17:51:56, `-c 98304` intact. `## Status` 47-48:
"llama.cpp on 0.0.0.0:8093 with CORS `*` and no API key (the server's own warning)" from the
10:46:49 startup log. Interpretation: the exposure state (0.0.0.0 bind, no key) was re-confirmed
by the server's own log today at 10:46:49 and the socket by Robotnik at 14:31 JST; the unit file
is unchanged since 2026-09-13 17:51:56, so the `ExecStart` flags below are current. Not observed
directly by this agent (ssh denied); recency is same-day.

Evidence E2 (unit + flags, live read-back 2026-09-12, `git grep -n "ExecStart"` on this doc):
unit is a user-level unit at `/home/howard/.config/systemd/user/llama-server-qwen3.8-27b-iq4xs.service`
(1043-1044); MainPID cmdline from `/proc` matches unit `ExecStart` (1048-1055): `--host 0.0.0.0
--port 8093 ... --parallel 1 ...` with **no `--api-key`**; full unit text at 1057-1073. Stage 1
(2026-09-13) changed only the binary (build 2000 / commit 5266f24d) and `-c 98304` (2189,
2254-2255), not the bind flags; W3 (2099) and the 10:46:49 startup log (E1) confirm build 2000
live on 8093 today. Sibling model units (q4/q5/q6/q8/qwen3.6/gemma4/deepseek-coder) existed in
the same directory but were **inactive**; only the iq4xs unit running (1074). No documented
change to that since 2026-09-12; no live enumeration possible (ssh denied), so "which other llama
ports listen today" is not verifiable from this role.

Evidence E3 (firewalld, only documented read is 2026-09-09, `TASK-0022-team-model-iq4xs.md:645-652`,
live `ssh howard@192.168.1.106` by Tails): `sudo -n firewall-cmd --zone=public --list-all` → `public`
zone on `eno1`, ports `8080 8081 8082 8083 8084 8085 8086 8087 8088 8090 8092 8093` (all /tcp),
services `cockpit dhcpv6-client ssh`; `ss -tln` showed `0.0.0.0:8092` and `0.0.0.0:8093` listening
that day (q4 unit active). No firewalld read after 2026-09-09 exists in either doc; Stages 1 and 3
(2189) touched binary, `-c` flag, and grub default only, so the 09-09 rule set is presumed current
but unverified since that date. The firewall is therefore NOT a mitigating control for 8093, and
the 11 other open ports are a latent exposure (see finding F2 below).

Attempt 3 constraint (recorded 2026-09-14): the dispatch requested live verification via
`ssh howard@192.168.1.106`, but this role's permission set denies it. A single read-only ssh
probe (`ss -tlnp`, `ps`, `systemctl cat`, `firewall-cmd` listings) was attempted and blocked
by the bash permission rules (allowed patterns are `git`, `gh`, `rg`, `shellcheck`, `gitleaks`,
`trufflehog` only). No live socket or firewall state was observed in this attempt. Live-state
claims therefore rest on the most recent documented evidence in the planning docs, each cited;
where no documented evidence exists for the current moment, that is said explicitly. This
supersedes nothing in the 2026-09-14 method note, it confirms it for attempt 3.

Severity assessment (attempt 3): the pre-existing high finding stands as **high**, not critical.
Same-day evidence (E1) re-confirms 0.0.0.0:8093 with the server's own CORS-`*`/no-key warning and
`--parallel 1` (E2); E3 shows the port firewalled open to the whole `public` zone. Attacker model:
any principal on the 192.168.1.0/x segment (compromised IoT device, guest machine, or another VM
on the same switch) needs zero credentials for `http://192.168.1.106:8093`; a sustained
`POST /v1/completions` stream starves the single inference slot and halts the whole team (PM +
every subagent) on demand, plus unbounded compute abuse; CORS `*` extends the vector to any web
page opened in a browser on the segment. Not critical because the API exposes no cross-session
context and no code execution. Internet reachability is **not verifiable** from this role: the
host sits on a private 192.168.1.x LAN, and router NAT/port-forward state decides external
exposure. If 8093 is port-forwarded, the same zero-auth endpoint is internet-reachable and this
finding becomes critical. Flagged for the user to check the router once.

Staged mitigations (attempt 3; nothing applied, each needs an approved host window):
- M1 (key): on the host, confirm `--api-key` exists in build 2000 via `llama-server --help`, then
  add `--api-key <generated on host>` to the unit `ExecStart` and restart in the window. The key
  lives only in the opencode provider config on the team host (verify the provider schema supports
  an API key for this endpoint before staging that line; env-based if supported). Never in a doc,
  commit, README, or under `set -x`-style logging.
- M2 (firewall): `sudo firewall-cmd --permanent --zone=public --add-rich-rule='rule family=ipv4
  source not addr=<team-host-IP> port port=8093 protocol=tcp reject'` + `sudo firewall-cmd
  --reload`. The pre-existing fix line proposes 192.168.1.102 as the team-host IP; re-verify with
  `hostname -I` on the team host at apply time (not verifiable from this role).
- M3 (CORS): check `llama-server --help` for an origin-restricting CORS option in build 2000; if
  absent, accept residual CORS `*` behind M1+M2 (a key-authenticated, LAN-restricted endpoint no
  longer yields cross-origin abuse to third-party pages without the key).
- M4 (port sweep, at the M2 window): review the 11 other open model ports (8080-8088, 8090, 8092;
  E3) against what actually runs and close what is unused, so a started sibling unit does not come
  up LAN-exposed by default.
- M5 (detection, no change needed): the server's journal request log and the 24 h wedge monitor
  cadence already give an abuse footprint; note request-rate anomalies in the monitor checkpoint.

Findings (attempt 3):

F1 — pre-existing finding "Unauthenticated model endpoint on 0.0.0.0:8093, CORS `*`, no API key"
(high, authz): **still-open**, re-verified 2026-09-14 against E1+E2+E3. No mitigation applied
(staged M1-M5); severity high, unchanged. Scope (b) inventory: `## Security` holds exactly this
one pre-existing finding (plus the template placeholder); the first pass recorded no supply-chain
or license findings, so (b) has nothing else to re-verify, and this attempt did not re-audit those
areas (out of scope). Citation nit in the original: its `Where` cites the verbatim `ExecStart` at
`TASK-0010...:1051`; the current doc has the `/proc` cmdline read-back at 1048-1055 and the full
unit at 1057-1073 (doc grew; same stale-citation class Shadow routed at 2166-2184). The
TASK-0022:647-648 firewalld citation is accurate.

F2 — 11 stale open model ports in firewalld `public` zone
**Severity:** low
**Vector:** authz
**Where:** firewalld `public` zone on EVO-X2 `eno1` (documented `TASK-0022-team-model-iq4xs.md:646-649`)
**Attack:** not executable today: the sibling llama units are documented inactive (this doc 1074,
2026-09-12 read-back), so the ports refuse connections. The exposure becomes real when any sibling
unit (q4 on 8092; others on 8080-8088/8090) is started, because the firewall rules persist and the
unit then comes up LAN-reachable with whatever auth it has.
**Impact:** latent; same class as F1 per unit started.
**Fix:** M4, at the M2 window.

Severity summary (attempt 3): high ×1 (F1, still-open, staged M1-M5, needs an approved host
window); low ×1 (F2, latent, staged M4); none critical. **DoD gate ("no unresolved findings above
`low` in `## Security`"): NOT met** — F1 (high) remains open; applying M1/M2 is explicitly outside
this attempt (apply nothing) and requires the user-approved window the `## Implementation` staged
section already uses. Re-check the gate after M1/M2 are applied and re-verified.

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

### Big re-verification (2026-09-14)

Re-run of the `## Implementation` W1/W2/W3 checkpoint evidence plus the 24 h wedge monitor
status, read-only over `ssh howard@192.168.1.106` (small-context probes only, no sustained
load). Prior review-chain attempts were lost to window exhaustion with zero writes; this pass
is mechanical. Rules: this edit is the first write (after the 100-line read the edit tool
requires before any edit); no 2 consecutive read/grep/bash calls without an intervening edit,
with one documented exception (the section-locating grep and the section-tail read ran
back-to-back to resolve the insertion anchor; the subsection was already composed, so nothing
was lost); doc read in 100-200 line chunks only. Placement: after the pre-existing Tails
2026-08-25 measurement record (diagnosis phase; remains valid as the baseline record).

**Checks planned** (exact commands to be taken from the `## Implementation` W1/W2/W3 evidence):

| # | Check | What it exercises | Result |
|---|---|---|---|
| 1 | W1 kernel | running kernel is 7.2.5-1.el10.elrepo | PASS |
| 2 | W2 service | llama-server unit active, listening on 8093 | PASS |
| 3 | W3 binary | /usr/local/bin/llama-server fingerprint is build 2000 / commit 5266f24d | PASS |
| 4 | Wedge baseline | 0 wedges since boot | PASS |
| 5 | 24 h monitor | /tmp/wedge-monitor-20260913-224443.log finished vs still running (hard stop 2026-09-14 22:44 JST), final wedge count | PASS (still running at probe time; 0 so far; final line due 22:44:43 JST) |

**Findings log** (updated as checks run):

- 2026-09-14: subsection created; checks 1-5 not yet run. Pre-existing content in this
  section: Tails 2026-08-25 measurement record (15 wedges at the time, pre-fix diagnosis).
- 2026-09-14: section map (grep `^## `): Status 10, Definition of Done 329, Next Actions 371,
  Plan 450, Implementation 569-1882, Review 1883, Security 2309, Test Results 2482, Docs 2538,
  Release 2551, Archive 2564. W1/W2/W3 evidence is inside `## Implementation` (1,314 lines);
  locating its `###` subsections next.
- 2026-09-14: checkpoint subsections located: W1 at 1734 (t/s vs iq4xs baseline), W2 at 1771
  (Stage 3 applied, reboot issued), W3 at 1845 (post-reboot verification, 24 h monitor started).
  Reading 1734-1883 next for the exact evidence and commands.
- 2026-09-14: W1/W2/W3 evidence extracted (read 1734-1883).
  - W1 (`:1734-1769`): t/s PASS (11.95 t/s at ~57.9k ctx vs 12.1-12.3 baseline); live
    `system_fingerprint: b2000-5266f24d` on 8093 (build 2000 / commit 5266f24d); `/health` ok.
  - W2 (`:1771-1841`): kernel-ml 7.2.5-1.el10.elrepo installed, BLS default set by exact entry
    id, reboot issued 2026-09-13 21:25 JST; wedge count 10 at change time (pre-reboot); unit
    untouched.
  - W3 (`:1845-1879`): kernel 7.2.5 live; **user unit** `llama-server-qwen3.8-27b-iq4xs.service`
    active, 8093 listening, pid 1907 at the time, `-c 98304` intact; fingerprint command:
    `PID=$(systemctl --user show ... --value --property=MainPID); BIN=$(readlink -f /proc/$PID/exe);
    "$BIN" --version` -> `bin=/usr/local/bin/llama-server`, `version: 0.4.0-dev (build 2000,
    commit 5266f24d)`; wedge baseline 0 since boot (t=0 22:44:43 JST); monitor pid 6647, log
    /tmp/wedge-monitor-20260913-224443.log, hard stop 2026-09-14 22:44:43 JST, sample every 300 s
    via `journalctl -k --no-pager | grep -cE "device wedged"`, appends a `monitor-stopped` line
    after the bound.
  - Context deltas to account for: unit is a user unit (systemctl --user); service
    clean-restarted 2026-09-14 10:46:49 JST (pid 9144 per `## Status`), so W3 pid 1907 is
    superseded; Shadow finding `:2048` notes the monitor's recorded count command is unscoped
    while the t=0 value only fits a boot-scoped count (run both scoped and unscoped).
- 2026-09-14 16:59 JST (probe A, `ssh howard@192.168.1.106`, read-only): `date` = Mon 14 Sep
  16:59:12 JST 2026 (hard stop 22:44:43 JST still ahead, ~5 h 45 m); `uname -r` =
  7.2.5-1.el10.elrepo.x86_64 (**check 1 PASS**); `uptime` = 19:29; `systemctl --user is-active
  llama-server-qwen3.8-27b-iq4xs.service` = active; `ss -ltn | grep 8093` = LISTEN 0.0.0.0:8093
  (**check 2 PASS**); `curl /health` = {"status":"ok"}; `curl /v1/models` =
  Qwen3.8-27B-UD-IQ4_XS, n_ctx 98304, ftype IQ4_XS (`-c 98304` intact live). No sustained load;
  only small-context/ metadata probes.
- 2026-09-14 ~17:00 JST (probe B, same ssh, read-only): `ls -la /usr/local/bin/llama-server` =
  -rwxr-xr-x howard:howard 16712 B, mtime Sep 13 17:30; `/usr/local/bin/llama-server --version` =
  `version: 0.4.0-dev (build 2000, commit 5266f24d)`, `built with GNU 14.3.1` (**check 3 PASS**,
  matches W1 live fingerprint b2000-5266f24d); `MainPID=9144`; `readlink -f /proc/9144/exe` =
  /usr/local/bin/llama-server (running process is the fingerprinted binary; W3's pid 1907
  superseded as expected); `journalctl -k --no-pager -b | grep -cE "device wedged"` = 0 and the
  monitor's unscoped command `journalctl -k --no-pager | grep -cE "device wedged"` = 0 (**check 4
  PASS**; unscoped=0 corroborates Shadow `:2048` observation that howard's visible kernel
  journal yields the boot-scoped count); monitor pid 6647 still running
  (`pgrep -af wedge_monitor_w3.sh`), last 5 log lines all `wedge_count=0` (16:39:47 through
  16:59:47 JST, 300 s cadence intact), zero `monitor-stopped` lines (**check 5: still running,
  count 0 so far**; hard stop 22:44:43 JST not yet reached).

**Checks requested vs run:** 5 requested, 5 executed (checks 1-5 in the table above). No check
dropped, no command blocked by the bash allowlist (ssh to 192.168.1.106 permitted; every probe
read-only, small-context only, no sustained load).

**Verdict:** The TASK-0010 implementation record re-verifies clean against the live machine.
All five checks PASS at 2026-09-14 16:59-17:00 JST: kernel 7.2.5-1.el10.elrepo.x86_64 (W1),
user unit `llama-server-qwen3.8-27b-iq4xs.service` active with 8093 listening on 0.0.0.0,
`/health` ok, `n_ctx` 98304 intact (W2), `/usr/local/bin/llama-server` is build 2000 / commit
5266f24d with the running process (pid 9144) resolving to that exact path (W3; the W3 record's
pid 1907 is superseded by the 2026-09-14 10:46:49 clean restart, consistent with `## Status`),
wedge count 0 since boot and 0 under the monitor's own unscoped command (baseline), and the 24 h
monitor still running (pid 6647) with every sample at `wedge_count=0` and the 300 s cadence
intact. The monitor has NOT finished: hard stop is 2026-09-14 22:44:43 JST, ~5 h 45 m after this
probe, so the final wedge count does not exist yet; the current count is 0 (last sample
16:59:47 JST). No FAIL, hence no code-bug or harness-bug routing. The one outstanding item is
the monitor's final `wedge_count=` line at the hard stop, which `## Status` already routes to the
pre-Knuckles check; nothing in this re-verification changes that.

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
