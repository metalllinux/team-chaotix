# TASK-0008 — Fix GDM Cinnamon-session login Authentication Error; widen VM test matrix

> **Section order below is fixed.** Each agent writes to its own section and no other. `Robotnik`
> reads only `## Status` and `## Next Actions`. Do not reorder, rename, or remove sections.

- **Created:** 2026-08-20

---

## Status

*Owner: `Robotnik`. Keep this SHORT and CURRENT — it is one of only two sections the PM reads, so a
stale entry means the whole loop runs on bad information.*

**Now (2026-08-28 02:13 UTC): 2c-3 session lost to the context hard limit (263,315 > 262,144
tokens) after ~5 h; progress checkpointed as `097702e`; the time bound was not self-enforced.**
Session ran ~21:0x (Aug 27) → 02:07:19 UTC, 91+ steps; the fatal request followed a 21-min
command (01:46→02:07 UTC). No new GPU wedges during the run (count stable at 5 since the
08:01 UTC boot) — this death is a context overflow, compaction off. Progress: textofext probe +
caps pre-pass work + ukey updates (388 lines added) in `tasks/lib/gdm-a11y.py`,
`tasks/lib/gdm-drive.sh`, `tasks/lib/ukey.c`; uncommitted at death; `Robotnik` committed +
pushed as `097702e`. **Structural lesson: subagents cannot self-enforce wall-clock bounds**
(the ~90-min bound / 70-min stop instruction was not honored; the model has no time sense),
and unbounded command output (a11y tree dumps) is what grows the context to the wall. 2c-3b
safeguards: (a) every command output truncated before it enters context (`tail -c 2000`; the
a11y probe returns only the targeted readback, never a tree dump), (b) a prescribed minimal
step sequence with a hard stop after two failures of any step, (c) explicit `date -u`
bookkeeping — record the start, re-check after every VM command, stop + checkpoint at 80 min.

**Now (2026-08-27 19:09 UTC): 2c-2 session lost at 18:42:04 UTC (third wedge in an hour);
Wayland harness adaptation checkpointed as `456ce71`.** The 2c-2 session ran ~5 h (~13:4x–
18:42 UTC), survived two wedges (17:41:22, 18:11:38 — the user-level unit auto-restarted
llama-server in seconds and opencode retried), and died on the third (18:42:04, "Connection
reset by server"; 5 wedges since the 08:01 UTC boot). Progress: Wayland harness adaptation in
`tasks/lib/gdm-a11y.py`, `tasks/lib/gdm-drive.sh`, `vm-test/test-gdm-login.sh` (173 lines
added) — uncommitted at death; `Robotnik` committed + pushed it as `456ce71` on
`origin/task-0008-gdm-auth`. No doc checkpoint written (died first). Lesson reinforcing the
safe-regime rule: the 5 h run kept the GPU under sustained load and accumulated stress (3
wedges in its final hour); 2c-2b must finish inside ~60 min.

**Now (2026-08-27 13:38 UTC): 2c-1 blocked as specified — RHEL 10 does not ship Xorg;
decision: re-scope 2c-2 to the Wayland greeter (option D).** `Tails` completed 2c-1 with the
full evidence chain (checkpoint `### Item 2 — 2c-1`): `xorg-x11-server-Xorg` exists in no
Rocky 10.2 repo (no binary, no drivers, no SRPM in the AppStream source tree), GDM 47 ships
`gdm-wayland-session` but no `gdm-x-session` (flipping `WaylandEnable=false` would break the
greeter — deliberately not touched; guest left unchanged). This contradicts the plan's
decision doc (X11-forced greeter, option A), which assumed Xorg was available on the target
OS; that premise is disproven by in-guest evidence and the deviation is recorded here per
AGENTS.md §5. **Decision (Robotnik): option D — 2c-2 tests the Wayland greeter.** Rationale:
the Cinnamon install added a launchable `cinnamon-wayland.desktop` entry; the harness's
pyatspi2 a11y and ukey uinput drivers are display-protocol independent; the "Authentication
Error" is a PAM failure in the greeter; and the user's real failure was on a Rocky 10.2
Wayland greeter, so this is the faithful reproduction. No external release-note confirmation
of the Xorg removal was obtainable (docs.redhat.com 403); the in-guest evidence stands alone.

**Now (2026-08-27 11:10 UTC): item 2c re-scoped into three small-context phases (2c-1/2/3);
safe-regime operating rule in force.** From the TASK-0010 record (attempt 3, checkpoints
3.1–3.4): the wedge cascade is only lethal when a session's context approaches ~200k (the dead
2c session was at ~201k; the 2a/2b delta-prompt regime ran 4.5 h with zero in-window wedges),
and no runtime GPU mitigation exists on this driver build. Item 2c therefore runs as 2c-1
(Xorg + GDM config in the guest), 2c-2 (login run + evidence), 2c-3 (doc completion +
commit), each a fresh small-context dispatch with a single deliverable; briefs name the exact
doc sections to read and never the whole doc.

**Now (2026-08-27 02:45 UTC): 2c session lost to a Q4 GPU wedge at 02:33 UTC; harness
checkpoint pushed as `959d01d`.** opencode.log (run `4408203b`): session
`ses_fc000ab1fffeaWBIiIQoN0mi5V` ran 01:08–02:33 UTC, survived one `Loading model` reload
(01:08:17), died 02:33:18 with "The socket connection was closed unexpectedly". EVO-X2 kernel
journal: **5** `device wedged` events since the 2026-08-26 12:25 UTC boot (0 at 12:50 UTC) —
the Q4 endpoint is **not** wedge-immune; the TASK-0010 problem is live on Q4 (~1 wedge per
4.7 h). The dead session left uncommitted harness edits (`tasks/lib/gdm-drive.sh`,
`tasks/lib/ukey.c`, `vm-test/test-gdm-login.sh`); `Robotnik` committed + pushed them as
`959d01d` on `origin/task-0008-gdm-auth`. Decision: dispatch the TASK-0010 runtime
mitigation (Tails, attempt 3) **before** re-dispatching 2c — cheap protection before the
long dispatch.

**Now (2026-08-26 19:55 UTC): item 2a (attempt 7) complete — and my orphan/reboot misread is
corrected.** `Tails` finished 2a with a non-empty final message (record: its `### Item 2 —
attempt 7` checkpoint in `## Implementation`, commit `425afa7`). **Correction (AGENTS.md §5):**
my `virsh list --all` checks (12:50, 16:45, 19:1x UTC) ran **without `sudo`**, which queries
the user libvirt session — always empty here. The system instance (`sudo virsh list --all`)
shows `gdm-login-vm` running (Id 3), **persistent**, QMP-live, XML on disk, managed
continuously since attempt 5's `virt-install` at 14:51 UTC. The domain was never removed, and
the libvirt host was **never** rebooted (up since Aug 15; the ~12:25 UTC reboot was EVO-X2,
the model host — that part of the TASK-0010 record stands, its "orphan died" consequence does
not). The Aug 25 orphan (QEMU PID 324361) is separately confirmed dead (gone by 14:40 UTC).
Inventory: 804 packages, **zero Cinnamon**, phase-3 baseline only (gdm, gnome-shell); the
INSTALL.md Cinnamon install (phase 6) never ran — that is 2b. Findings for 2c: the greeter is
Wayland-only (Xorg absent) while the committed harness assumes X11 — 2c installs
`xorg-x11-server-Xorg` + `WaylandEnable=false` or extends the driver; `provision-vm.sh:163`
clobbers this disk in place under the same name — 2c must use a different `--name` or destroy
first, with 2b before any destroy. VM left running at the greeter, ssh at
192.168.122.15 (root, `~/.ssh/cinnamon-test-key`), `virsh autostart` enabled as protection.
Item 2b (RPM install) dispatches next.

**Now (2026-08-26 19:30 UTC): attempt 6 also exited the loop with an empty final message;
the test VM is ALIVE as an orphan QEMU.** opencode.log (run `4408203b`) session
`ses_fc0ff7665ffe9MyRmvZb8V1nDG`: 27 steps ~18:35–19:06 UTC, zero errors, `exiting loop`
19:06:46 UTC. No doc writes, no commits, no registered VM. But: QEMU PID 390197
(`-name guest=gdm-login-vm`, `domain-3-gdm-login-vm`) has run 4h25m since ~14:40 UTC
(attempt 5's `virt-install.log` 14:51 UTC: "Domain creation completed") and holds
`/var/lib/libvirt/images/cinnamon-test/gdm-login-vm.qcow2` (2.28 GB, grown from the 545 MB
cloud base = guest-side dnf activity happened inside it). The domain definition was removed (corrected 2026-08-26 19:55 UTC: never removed — the
unsuffixed `virsh` checks saw the empty user session; `sudo virsh` shows the domain running
and persistent, record above). ARP shows
192.168.122.15 on virbr0 (52:54:00:a0:8b:34, STALE). **Pattern: two consecutive Q4 sessions
(attempts 5, 6) exited the loop with an empty final message before the item 2 deliverable.**
New approach: item 2 is split into single-deliverable dispatches — 2a recover + inventory the
VM, 2b install the RPMs in it, 2c run the harness and write `### Item 2` — each requiring a
non-empty final message.

**Now (2026-08-26 16:50 UTC): attempt 5 ran to loop exit with an empty final message;
progress preserved, VM never provisioned.** opencode.log (run `4408203b`) records session
`ses_fc197dc78ffeR41BULZ1t9QxIv` running 55 steps ~14:20–16:38 UTC, then `message="exiting
loop"` with no error, abort, or stream failure. Q4 endpoint healthy throughout (wedge count
0, no reboot, load ~0.3). Progress: checkpoint commit `b15dfcb` pushed to
`origin/task-0008-gdm-auth` (local working tree clean); checkpoint section `### Item 2 —
attempt 5` written in `## Implementation` (line 1016). Not reached: VM provisioning (host `virsh list --all` empty — corrected 2026-08-26 19:55 UTC:
check lacked `sudo`; the domain **was** created at 14:51 UTC during this attempt and has run
since), harness completion, `### Item 2`, Next Actions update. This is a
Q4 behaviour (loop exits with an empty final message), not an infrastructure failure. Note:
the 2026-08-25 20:19 UTC `exceeds the available context size (65536)` error in the log was
the **old** opencode run (`5ce7e912`) with stale cached limits; the current run and
`opencode.json` both carry the Q4 limit `context: 262144, output: 131072` — no config fix
needed. Attempt 6 re-dispatches from the attempt 5 checkpoint with a non-empty final message
required.

**Now (2026-08-26 12:50 UTC): item 2 re-dispatching now, on the Q4 endpoint, with a new VM.**
EVO-X2 was rebooted 2026-08-26 ~12:25 UTC (record: TASK-0010 `## Status`): zero wedges since
boot, Q5 (8084) no longer served, team runs Q4 (8092, `n_ctx: 262144`) and this session proves
dispatch from a fresh session. The orphan `gdm-login-vm` did **not** survive the reboot
(`virsh list --all` empty — corrected 2026-08-26 19:55 UTC: that check lacked `sudo`; the Aug 25 orphan QEMU PID 324361 was in fact dead by 14:40 UTC, and attempt 5 provisioned a new domain at 14:51 UTC which is running), so item 2 provisions a **new** VM instead of adopting the orphan.
Local clone `~/Linux/projects/cinnamon-for-rocky10/` branch `task-0008-gdm-auth` is at `1f00da5`
(= origin/main) with the attempts 3/4 working tree: modified `vm-test/lib.sh`,
`vm-test/provision-vm.sh`; untracked `vm-test/test-gdm-login.sh`, `vm-test/test-repo-setup.sh`,
`tasks/`. Tails commits that state to the branch and pushes it to origin first, as a
checkpoint, then continues. Wedge count is checked before and after the dispatch (command:
TASK-0010 `## Status`); the dispatch is cancelled if wedges appear.

**Now (2026-08-25, new session): item 2 attempt 4 lost to the wedge; TASK-0010 (fix the GPU
wedge) is now the gating task, in progress.** Attempt 4 dispatched ~05:54 UTC with the orphan
VM verified alive (QEMU PID 324361, ssh OK, wedge count 13 = baseline). Wedge count rose to 15
during the run; opencode.log shows stream errors 05:55 UTC (endpoint down, model reloading);
session cancelled 06:29 UTC. No `### Item 2` written (orphan VM state to be re-verified on the
next dispatch). User ordered the GPU wedge fixed now (2026-08-25); see TASK-0010
(`planning/docs/TASK-0010-evox2-gpu-wedge-fix.md`). Item 2 re-dispatch waits for a measurably
stable endpoint.

**Now (2026-08-25 05:15 JST): Q5 endpoint crash-looping; both item 2 attempts lost to it; work
preserved in an orphan VM.** opencode.log shows 10 Q5 crash/restart events since 2026-08-22 08:33
UTC (Aug 24: 07:18, 08:20, 12:18, 18:27, 19:32). Each is "Unable to connect" + "Loading model"
= process down, systemd cold-restart (`Restart=on-failure`, `RestartSec=5` per the unit record in
`/home/howard/AI/projects/qwen-38-q5-fixes/qwen38-q5-fixes.md`), minutes-long model load during
which opencode kills in-flight subagent sessions (no stream retry). Item 2 attempt 1 (03:50-08:20
UTC, 4.5h) and attempt 3 (12:31-19:32 UTC, 7h) both died this way; attempt 3 did real harness work
(permission log 14:54-18:12 UTC). Root cause found 2026-08-25 (EVO-X2 kernel journal, SSH key access granted by user 08:55 JST):
the Strix Halo iGPU wedges under llama-server load, amdgpu compute-ring timeouts (26 wedge events
since the 2026-08-23 boot; exact time correlation with the opencode.log errors), each ring reset
kills the Vulkan device and the process. Full record:
`/home/howard/AI/projects/qwen-38-q5-fixes/qwen38-q5-fixes.md` (2026-08-25 section). A `-fa off`
mitigation attempt broke startup (q8_0 V-cache quantization requires flash_attn; constraint now
documented); user restored the unit from backup at 10:04 JST and froze the config (user decision
2026-08-25: keep `-fa on` + q8_0 KV + 262144, no further unit changes). Standing rule (user):
always back up the unit before modifying it. Wedge risk accepted; mitigation is process-level
(checkpoint to this doc early and often, keep the VM as durable state, compare wedge counts
before/after runs). Service verified healthy 10:40 JST (`n_ctx: 262144`, zero error lines since
restore).
Work preserved: attempt 3's test VM is an ORPHAN QEMU process (libvirt domain deleted, process
alive since 14:53 UTC Aug 24, 4GB RAM). Guest `gdm-login-vm`, disk
`/var/lib/libvirt/images/cinnamon-test/gdm-login-vm.qcow2` (2.3G), VNC 127.0.0.1:5900,
ssh root@192.168.122.29 with `~/.ssh/cinnamon-test-key`. Verified inside (2026-08-25 05:05 JST):
`/root/gdm-harness/` (`gdm-a11y.py` pyatspi2 finder, `gdm-drive.sh`, `ukey`+`ukey.c` uinput
micro-driver), `/root/gdmtest.pass`, `/tmp/{holddev,holddev2,holddev3,xlisten,xtest-test}`; GDM +
gnome-shell installed, `gdmtest` user, SELinux permissive. Do not kill the orphan process.
Neither attempt wrote `### Item 2` to this doc.

**Now (2026-08-23 21:45 JST):** Q5 context wall root-caused and fixed; endpoint layout final.
Root cause: the q5 unit forced `--n-gpu-layers 99`, so llama.cpp's fit-to-device step (on by
default) silently shrank context 262144 to 65536 per slot; the 2026-08-22 "verified `-c 262144`"
entry was a misread of `/proc/PID/cmdline` (flag present, not in effect; evidence: startup log
`n_ctx_seq (65536) < n_ctx_train (262144)`, `/v1/models` n_ctx=65536). The second Wave 0
re-dispatch (2026-08-22 19:55 JST, run `e9706ca3`) died on that wall: all five subagents errored
"exceeds the available context size (65536)" within 10 min (amy's first call 70043 tokens); the
previous PM session died the same way at 20:32 JST. Fix: unit now has no `--n-gpu-layers` (fit
picks the split) and `--parallel 1`; full config, before/after, and the measured memory ceiling
in `/home/howard/AI/projects/qwen-38-q5-fixes/qwen38-q5-fixes.md`. Hardware ceiling (measured
with Q6 stopped): only one 262144-context slot fits; 2 slots degrade to 131072 each, 3 to 87552,
4 to 65536. Q6/8090 retired (stopped + autostart disabled; user decision 2026-08-23; PM session
on Q5). Q8/8088 down; its unit needs the same `-ngl` fix before fallback use. Provider entry, 10
agent frontmatter, AGENTS.md: retargeted and pushed (`2fe0c8b`); docs pushed (`ab17e18`). Branch
`task-0008-gdm-auth` exists in the clone (at main, no commits yet). `## Plan` complete (Amy,
2026-08-20): reproduction design, H1-H4, fix approach, 6-scenario Sparky/Sparrow matrix,
rollback; decision doc `planning/DECIDE-gdm-login-test-automation.md`. Wave 0 starts now, one
subagent at a time (see Next Actions).

**Incident (2026-08-21 → 22): the Wave 0 fan-out lost all five sessions overnight.** Five
concurrent subagent sessions ran against the single-slot model endpoint
(`llama-server-qwen3.8-27b-q6`, port 8090, `--parallel 1`; 1h request timeout in
`~/.config/opencode/opencode.json`). Queued model calls hit the 60-min limit; opencode.log shows
each session's final stream erroring at exactly +60 min (01:04→02:04 … 01:40→02:40 UTC) with no
retry, killing the session. Partial artifacts only: interrupted Raku install (`~/.raku` has zef,
no `raku` binary), Big's scratch VM `cinnamon-inspect-vm` (domain gone by 12:45 JST Aug 22, disk
kept under `/var/lib/libvirt/images/cinnamon-test/`). No planning-doc or repo changes landed.

**Endpoint state (2026-08-22):** Q6/8090 (the endpoint agents actually use; AGENTS.md: "All
agents use Qwen3.8-27B-UD-Q6_K_XL") is up and healthy. Q8/8088 was down (unit missing, model file
present) — restored as `llama-server-qwen3.8-27b-q8.service` with `--parallel 4`, verified
(`/v1/models` + timed generation, 2026-08-22). The 2026-08-20 "retarget to Q8/8088" note is
superseded. Team repo HEAD `7f0c6a4` (2026-08-21) re-targeted all agents to Q6/8090, matching
AGENTS.md and the live config.

**Model decision (user, 2026-08-22):** the team model is `Qwen3.8-27B-UD-Q5_K_XL`; all agents
use it. Supersedes the Q6 re-target (`7f0c6a4`) and the Q8 one before it (`afade6e`). Verified
gap at write time: no Q5 model file on EVO-X2 (`find /mnt/data -iname '*q5*'` empty) and no Q5
service (only 8088/8090 listening). Standing up the Q5 endpoint (model file, `--parallel 4`
systemd user unit on a free even port, `evo-x2-qwen3.8-q5` provider entry in
`~/.config/opencode/opencode.json`, the `model:` line in all 10 `.opencode/agents/*.md`,
AGENTS.md section 1, commit) is the first action of the next session and gates every dispatch.
Q6/8090 and Q8/8088 remain fallbacks. Full setup steps:
`planning/docs/TASK-0008-new-session-prompt.md` (Prompt 3).

**Dispatch policy (endpoint-bound, final 2026-08-23):** Q5 is 1 slot x 262144 and that is the
hardware ceiling (measured: 2- and 3-slot x 262144 do not fit even with Q6 stopped), so
subagents run one at a time and the PM polls from the same endpoint (its requests queue briefly;
the 1h timeout is no longer a risk at 262k). The plan's parallel waves run sequentially: Wave 0
in order 1, 3, 2, 9a with Amy (TASK-0009) interleaved; review fan-out Shadow, Omega, then Big.
Commit target stays feature branch `task-0008-gdm-auth` in the clone; item 13 PRs it to main. A7
guard stands: one 4GB VM at a time, check `free -g` first.
User's failure recap: GDM "Authentication Error" selecting the Cinnamon session on Rocky Linux
10.2 (Cinnamon RPMs from the local DNF repo per INSTALL.md, GDM + GNOME pre-existing); a reboot
restored the session.
Decision (user, 2026-08-21): the GitHub token embedded in this repo's `origin` remote URL
(`.git/config`) stays as-is. Verified not committed (2026-08-21): token-fragment pickaxe across
all history and the tracked working tree returned no hits; `.git/` is untracked. Agents must
never write the token to a file, doc, commit, or GitHub issue.
Decision (user, 2026-08-21): for any desktop application testing, the team standard is Sparky +
pyatspi2 (https://gitlab.gnome.org/GNOME/pyatspi2), tracked as TASK-0009. Item 3's input-driver
decision must weigh it; raw-input drivers (xdotool) remain candidates for surfaces where a11y is
unavailable (e.g. the GDM greeter) — to be settled by evidence, not assumption.
Decision (user, 2026-08-20): team model retargeted to
`evo-x2-qwen3.8-q8/Qwen3.8-27B-UD-Q8_K_XL` on port 8088 (live). The old BF16 endpoint 8086 was
down and was silently killing subagent dispatches (two empty `Amy` runs, no file changes) —
if a dispatch comes back empty again, suspect the endpoint before the agent.

**Environment / scope:**
- Files in scope: `metalllinux/cinnamon-for-rocky10` repo (main), project dir
  `~/Linux/projects/cinnamon_4_rocky10/` (spec files, session files, PAM-related packaging);
  new Sparky/Sparrow test harness (location decided by `Big`)
- Verified (2026-08-20): the git clone of the repo is `~/Linux/projects/cinnamon-for-rocky10/`
  (default branch `main`, confirmed via `gh repo view`). The project dir
  `~/Linux/projects/cinnamon_4_rocky10/` holds the upstream source trees and INSTALL.md and has
  no `.git` — commits go to the clone, not the project dir.
- Touches the DB schema: no
- Graphical UI: yes (GDM/LightDM login screens, desktop sessions) — Sparky testing required
- Rocky Linux target: yes

**Unknowns:**
- Root cause of the GDM Authentication Error is unestablished. It must be reproduced in a VM with
  log evidence before any fix is claimed.
- Whether LightDM and no-login-manager configurations are equally affected is unknown. The test
  matrix will establish it.
- How a blank install (no login manager) gets a working login from the Cinnamon RPMs is
  unverified. The plan must confirm what the package set depends on.
- Whether the failure is caused by the RPMs' PAM/session files or by interaction with the existing
  GNOME install is unknown.

---

## Definition of Done

*Owner: `Robotnik`, and nobody else. Written **before** any work starts. Objectively checkable —
if a box cannot be verified by looking at something, rewrite it.*

- [ ] **Reproduction before fix.** `Big` reproduces the failed Cinnamon-session login in a libvirt
      Rocky Linux 10 VM with GDM + GNOME pre-installed (the user's exact configuration), before
      any fix lands, and records it in `## Test Results`.
- [ ] **Evidence captured.** `## Test Results` quotes the relevant log lines, not paraphrases, from
      `journalctl -u gdm` and `/var/log/secure`, for both the failed Cinnamon login and a
      successful GNOME login on the same VM.
- [ ] **Root cause stated.** `## Test Results` states the root cause in one to three sentences, and
      the quoted log lines prove that cause.
- [ ] **Fix committed.** `Tails` commits the fix to `metalllinux/cinnamon-for-rocky10` main via
      PR. Changes are confined to the repo (spec/packaging/session files); no user-machine config
      changes are part of the deliverable.
- [ ] **Fix verified in VM.** On a fresh VM with GDM + GNOME and the fixed RPMs installed, selecting
      the Cinnamon session in GDM and entering the correct password yields a working Cinnamon
      desktop: no Authentication Error, no reboot required. GNOME login still works on the same VM.
- [ ] **Full matrix.** Every scenario below is run by `Big` on a fresh libvirt Rocky Linux 10 VM and
      recorded in `## Test Results`:
      - GDM + GNOME pre-installed (user's config): install Cinnamon RPMs, switch to the Cinnamon
        session in GDM, log in, verify the session comes up
      - LightDM pre-installed: install Cinnamon RPMs, log in to the Cinnamon session through
        LightDM, verify it works
      - No login manager (blank install): install Cinnamon RPMs, verify the Cinnamon session is
        available and login works
      - Uninstall: after a successful install, remove the Cinnamon RPMs and verify no broken or
        dangling packages, no leftover session entries, no PAM breakage, and the previous login
        path still works
      - Additional configuration combinations as practical, with the final list recorded in
        `## Test Results`
- [ ] **Reusable tests.** Every scenario has a re-runnable Sparky/Sparrow (Raku) task committed to
      the repo; paths recorded in `## Test Results`. No scenario depends on manual steps.
- [ ] **Nothing dropped.** `Big` records an explicit "checks requested vs run" count in
      `## Test Results`; no check is silently dropped or skipped.
- [ ] `Shadow`: no unresolved blockers or should-fix findings in `## Review`
- [ ] `Omega`: no unresolved findings above `low` in `## Security`
- [ ] `Vector`: `README.md` and `INSTALL.md` updated as affected (INSTALL.md must remain a correct
      procedure, and must cover switching to the Cinnamon session on an existing GDM + GNOME system)
- [ ] `Knuckles`: PR merged to main. No human review required (internal `metalllinux` repo, no
      deployment).

---

## Next Actions

*Owner: whoever wrote last. The future only — delete what has been done. The second of the two sections
the PM reads.*

- [x] `Amy` (2026-08-20): `## Plan` written. Decision doc:
      `planning/DECIDE-gdm-login-test-automation.md`. Wave 0 fan-out available now: items 1, 2, 3, 9a
      are independent (see `## Plan` → Dependencies and sequence). Reproduction and matrix execution
      are owned by `Big` per the Definition of Done; `Tails` writes the harness scripts.
- [x] `Robotnik` (2026-08-21): Wave 0 dispatched in a single message (items 1 ∥ 2 ∥ 3 ∥ 9a).
- [x] `Robotnik` (2026-08-22): Q5 endpoint verified up (record: Status); branch
      `task-0008-gdm-auth` created in the clone; Wave 0 re-dispatched on 4 slots (items 1 ∥ 2
      ∥ 3 ∥ 9a, Amy/TASK-0009 as fifth client).
- [x] `Robotnik` (2026-08-23): Q5 64k wall root-caused (fit-to-device degradation under forced
      `-ngl 99`); second dead Wave 0 (2026-08-22 19:55 JST: all five subagents + the PM session)
      confirmed in opencode.log and the EVO-X2 journal; Q5 reconfigured to 1 slot x 262144
      alongside Q6; PM session on Q6 (user switch ~09:52 JST).
- [x] `Robotnik` (2026-08-23 21:45 JST): PM session switched to Q5 (user); Q6 stopped +
      autostart disabled; 2-slot and 3-slot x 262144 configs tested and rejected (fit degrades
      them to 131072 and 87552); Q5 final at 1 slot x 262144, verified; fixes documented in
      `/home/howard/AI/projects/qwen-38-q5-fixes/qwen38-q5-fixes.md`.
- [x] `Robotnik` (2026-08-24): session resumed. Q5 re-verified up (`/v1/models` on 8084 shows
      `n_ctx: 262144`, no fit degradation). Clone `~/Linux/projects/cinnamon-for-rocky10/` branch
      `task-0008-gdm-auth` verified at `1f00da5` = `origin/main` (no local commits). User reminder
      (2026-08-24): keep `metalllinux/cinnamon-for-rocky10` main current on GitHub. Path: work
      commits to feature branch, item 13 PRs it to main and `Knuckles` merges; nothing lands on
      main before the fix is verified.
- [x] `Robotnik` (2026-08-25 05:15 JST): item 2 post-mortem done (record in Status). Both item 2
      attempts died to Q5 endpoint crash-restarts, not agent failure.
- [x] `User` (2026-08-25): granted SSH key access from shadow to EVO-X2 (08:55 JST); restored the
      Q5 unit from backup after the `-fa off` breakage (10:04 JST); froze the config (keep `-fa on`
      + q8_0 KV + 262144, no further unit changes); set the standing backup-before-change rule.
- [x] `Robotnik` (2026-08-25 10:45 JST): wedge root cause recorded (Status + fixes doc); service
      verified healthy after user restore. Wedge risk accepted per user config freeze; mitigation
      is process-level checkpointing.
- [x] `Robotnik` (2026-08-25, new session): Q5 verified up (`n_ctx: 262144`); orphan
      `gdm-login-vm` verified alive (QEMU PID 324361, ssh OK); wedge count 13 = baseline. Item 2
      attempt 4 dispatched to Tails with the resume brief (adopt orphan VM, no new VM, verify
      prior state, finish the GDM harness, write `### Item 2`, checkpoint early and often).
- [x] `Robotnik` (2026-08-25): attempt 4 post-mortem: wedge count 13 → 15 during the run
      (stream errors 05:55 UTC in opencode.log); session cancelled 06:29 UTC. User ordered the
      GPU wedge fixed now; TASK-0010 created, Tails dispatched for diagnosis + runtime
      mitigation (see TASK-0010 Next Actions).
- [x] `Robotnik` (2026-08-26): endpoint-stability decision recorded (Status): host rebooted
      ~12:25 UTC, zero wedges since, Q5 no longer served, team on Q4. Orphan VM dead (reboot),
      so item 2 re-dispatches with a new VM; wedge count monitored before/after.
- [x] `Tails` (item 2, attempt 5, dispatched 2026-08-26 ~14:20 UTC): ran 55 steps, exited the
      loop at 16:38 UTC with an empty final message (no error; record: Status). Progress:
      checkpoint commit `b15dfcb` pushed to `origin/task-0008-gdm-auth` (working tree clean);
      checkpoint section `### Item 2 — attempt 5` written in `## Implementation`. Not reached:
      VM provisioning, harness completion, `### Item 2`, this section.
- [x] `Tails` (item 2, attempt 6, dispatched 2026-08-26 ~18:35 UTC): 27 steps, exited the
      loop at 19:06:46 UTC with an empty final message (no errors; record: Status). No doc
      writes, no commits. Left the guest running as orphan QEMU PID 390197 with the
      domain definition removed (record: Status).
- [x] `Robotnik` (2026-08-26 19:30 UTC): item 2 re-scoped into single-deliverable dispatches
      2a/2b/2c after two consecutive empty-exit Q4 sessions (record: Status).
- [ ] `Tails` (item 2a, attempt 7, dispatched 2026-08-26): recover and inventory the orphan
      guest — QEMU PID 390197, likely 192.168.122.15 on virbr0, image
      `/var/lib/libvirt/images/cinnamon-test/gdm-login-vm.qcow2`, domain definition gone.
      Verify ssh (root key per the attempt 5 section), re-register the domain in libvirt
      without disturbing the running QEMU (or record why not), inventory what is already
      installed in the guest (attempts 5/6 did guest-side dnf work; disk grew 545 MB →
      2.28 GB), and write a checkpoint in `## Implementation`. Leave the VM running.
      Deliverable: live, ssh-verified, libvirt-managed VM + inventory checkpoint. Read only
      the `### Item 2 — attempt 5` section (line ~1016) plus `## Status` and `## Next
      Actions`; end with a **non-empty final message**.
- [x] `Tails` (item 2b, attempt 8): complete — 14 cinnamon-family packages, zero dependency
      errors, ldd sweep of 43 binaries + 6 libs clean, VM left untouched; checkpoint `###
      Item 2 — attempt 8`, commit `bf8c623` (record: Status).
- [x] `Robotnik` (2026-08-27 02:45 UTC): 2c post-mortem (record: Status); dead session's
      harness edits committed + pushed as `959d01d`; re-sequenced: TASK-0010 runtime
      mitigation (Tails, attempt 3) before the 2c re-dispatch.
- [x] `Tails` (item 2c-1, 2026-08-27): **blocked as specified** — `xorg-x11-server-Xorg`
      does not exist in any Rocky 10.2 repo (no binary, no drivers, no SRPM; GDM 47 ships
      no X session launcher; full evidence chain in checkpoint `### Item 2 — 2c-1`). No
      guest state change; VM left running at the Wayland greeter. Bonus finding: the
      Cinnamon install added a launchable `cinnamon-wayland.desktop` session entry.
- [x] `Robotnik` (2026-08-27 13:38 UTC): 2c-1 blocker resolved — option D approved: 2c-2
      tests the Wayland greeter (record: Status; the plan decision doc's X11 premise is
      disproven by in-guest evidence).
- [x] `Tails` (item 2c-2, dispatched 2026-08-27 ~13:4x UTC): ran ~5 h, survived two wedges
      (17:41:22, 18:11:38 UTC), died on the third (18:42:04; record: Status). Progress:
      Wayland harness adaptation in `tasks/lib/gdm-a11y.py`, `tasks/lib/gdm-drive.sh`,
      `vm-test/test-gdm-login.sh` (173 lines added), no doc checkpoint; committed + pushed
      by Robotnik as `456ce71`.
- [x] `Tails` (item 2c-2b, 2026-08-27): complete — login run executed (FAIL: the
      Authentication-Error reproduction, twice, with the account + PAM stack proven sound
      via the su control); adaptation finished with the proven caps-corruption bug fixed
      in `gdm-drive.sh` (static greeter caps label → LED-parity normalization); evidence in
      guest `/root/evidence/cinnamon-attempt-2c2b/`; checkpoint `### Item 2 — 2c-2`.
      (Ran ~82 min vs the ~60 min bound; the time-bound deviation is recorded in the
      checkpoint.)
- [x] `Tails` (item 2c-3, dispatched 2026-08-27 ~21:0x UTC): ran 91+ steps to 02:07:19 UTC,
      died on a 263,315-token request (context hard limit; record: Status). No new wedges.
      Progress: textofext probe + caps pre-pass + ukey updates (388 lines), no doc checkpoint;
      committed + pushed by Robotnik as `097702e`.
- [ ] `Tails` (item 2c-3b, dispatched 2026-08-28): resume from `097702e` + the `### Item 2 —
      2c-2` "For 2c-3" note. Read only `## Status`, `## Next Actions`, and the `### Item 2 —
      2c-2` section. Prescribed sequence: (1) `date -u` start; (2) verify/finish the textofext
      probe + caps pre-pass against the VM; (3) ONE login run with `gdmtest` selecting Cinnamon
      (Wayland) — PASS = session active (loginctl), FAIL = capture PAM evidence; (4) checkpoint
      `### Item 2 — 2c-3` + commit + push. Every command output truncated before it enters the
      context (`tail -c 2000`; the a11y probe returns only the targeted readback, never a tree
      dump); `date -u` after each VM command; **stop immediately with checkpoint + summary if
      elapsed > 80 min or any step fails twice**. End with a non-empty final message.
- [ ] `Tails` (item 2c-3, after 2c-2): per the 2c-2 checkpoint's "For 2c-3": add
      `gdm-a11y.py textofext`, add the probe-typed caps pre-pass to `gdm_login`, re-run
      the flow (PASS closes the input-layer suspect; a second FAIL with a verified
      lowercase password promotes the PAM hypotheses H1–H4); then write the `### Item 2`
      completion in `## Implementation` + a completion entry here; commit + push harness
      fixes to `task-0008-gdm-auth`.
- [ ] `Robotnik`: after 2c, the rest of the chain: 9a (Tails, Sparrow suite), Amy
      (TASK-0009 plan), 4 → 5 → 6 → Shadow → Omega → Big → 8 → 10 → (11) → 12 → 13 → 14.

---

## Plan

*Owner: `Amy`. Written 2026-08-20. Decision doc: `planning/DECIDE-gdm-login-test-automation.md` (GDM
login test automation approach, option A: X11-forced greeter + `xdotool`, libvirt for reproduction,
Sparky QEMU for the matrix).*

### Strategic framing

**Why this task exists** — the user hit a blocking GDM "Authentication Error" selecting the Cinnamon
session on Rocky Linux 10.2 with GDM + GNOME pre-installed, using the DNF-repo install from
INSTALL.md; a reboot restored the session. Every prior test (TASK-0003/0005/0006) was a headless
package install: no test in this project has ever logged a user into a graphical session. The
install path documented in INSTALL.md is broken for the most common target configuration until this
is fixed.

**What it unblocks / what blocks it** — Unblocks: a trustworthy Cinnamon install for existing
GDM+GNOME users (the common case), and the first reusable Sparky/Sparrow GUI test harness for all
future Cinnamon work (remaining TASK-0002 items: settings UI, SELinux policy). Blocks: nothing
external. Internal prerequisites, all present or planned: cloud image at
`/var/lib/libvirt/images/cinnamon-test/Rocky-10-GenericCloud.qcow2` (used by
`vm-test/provision-vm.sh:25`), libvirt + QEMU running on the host, the 48 RPMs in
`~/Linux/projects/cinnamon-for-rocky10/rpms/`, host internet (Raku/zef deps, VM `dnf`). The user's
machine is **not** a dependency: reproduction happens in a VM.

**MVP** — reproduce the failure in a VM with log evidence, state the root cause, land the fix, and
verify the user's exact configuration (GDM + GNOME, Cinnamon session login) on a fresh VM. The full
six-scenario matrix is DoD-required, not deferred, but it runs **after** the fix so it validates the
fixed RPMs. Deferred: a full custom Cinnamon SELinux policy (only a minimal policy/context fix is in
scope, and only if the root cause demands it); Wayland Cinnamon support and cjs 140 (pre-existing
blockers, TASK-0004); the README 10-vs-14 package count discrepancy (folded into item 12 as a
drive-by).

**What this makes harder later** — (1) The matrix is pinned to the X11 greeter; a future Wayland
Cinnamon session needs a new input driver, not an extension of this one. (2) `main.raku` + `tasks/`
at the repo root mix test scaffolding into the product repo; the exit route is a dedicated Sparky
repo. (3) The host carries permanent additive state: Raku, Sparky, port 4000, a sudoers drop-in, a
firewall rule (removal steps in the decision doc). (4) Spec `%prep` sed-patching diverges further
from upstream sources per fix; this is existing house style, now compounding.

### Verified facts this plan rests on

- `spec/cinnamon.spec:136-137,151` — the `cinnamon` package installs
  `/usr/share/xsessions/cinnamon.desktop`, `/usr/share/wayland-sessions/cinnamon-wayland.desktop`,
  and `/etc/pam.d/cinnamon`.
- `cinnamon/data/xsessions/cinnamon.desktop.in` — `Exec=cinnamon-session-cinnamon`,
  `TryExec=@bindir@/cinnamon`, `Type=XSession`. Both paths are in the `cinnamon` package
  (`spec/cinnamon.spec:100,117`), so the session entry only exists once `cinnamon` is installed.
- `cinnamon/data/pam/cinnamon.pam` — RHEL-style stack (`include system-auth` for auth/account/
  password/session, `-auth sufficient pam_selinux_permit.so`, `-auth optional pam_gnome_keyring.so`).
  Faces sane; installed content must still be diffed against this (build-time `configure_file`).
  GDM does not use this service for interactive password login (assumption A3), so this file is
  unlikely to be the trigger by itself.
- `cinnamon/files/usr/bin/cinnamon-session-cinnamon` — dispatches X11 vs `--wayland` correctly;
  the X11 entry runs `cinnamon-session --session cinnamon`.
- `cinnamon/cinnamon.session.in:3` — `RequiredComponents=cinnamon;nemo-autostart;@REQUIRED@cinnamon-killer-daemon;`.
  `nemo-autostart` comes from the `nemo` package, which is **not** a hard dependency of
  `cinnamon` (TASK-0006 `## Test Results`: `dnf install cinnamon` pulls 9 of 14 base packages).
  A missing required component is a live session-launch failure candidate.
- `spec/cinnamon-session.spec:49-64` — `%files` lists **no** systemd user unit, but meson installs
  `cinnamon-session/data/systemd/user/cinnamon-session.target` when `enable_systemd` is true
  (`cinnamon-session/meson.build:61-75`, spec builds with `-Dsystemd=auto` and `systemd-devel`
  BuildRequires). Whether that unit is actually in the shipped RPM is unverified — a 1-minute
  `rpm -qlp` check in item 3. If it is installed-but-unlisted the build would have failed, so it is
  most likely absent from the RPM: a packaging gap to record even if not the root cause.
- Harness: `vm-test/provision-vm.sh` provisions headless cloud-image VMs (`--graphics none`,
  virt-customize, SSH-key-only, `LIBVIRT_DEFAULT_URI=qemu:///system` in `vm-test/lib.sh:19`).
  `repo-setup/setup-repo.sh` is the user-facing `file://` repo method validated in TASK-0006
  (51 PASS / 0 FAIL / 6 SKIP / 1 WARN). INSTALL.md:27-48 is the exact install procedure the user
  followed; INSTALL.md:152-164 is the thin GDM section that must be rewritten (item 12).
- Known environment gotchas (TASK-0003/0004 `## Test Results`): Xvfb is not in EL10 repos;
  duplicate/old-version RPMs in `rpms/` cause dnf conflicts (clean before re-repoing); all prior
  harness VMs ran **SELinux permissive** (TASK-0003 Run 2) while the user's machine is almost
  certainly enforcing (Rocky default).

### Assumptions

- **A1** Cloud image + `dnf install gdm gnome-shell` (X server, test user) approximates the
  user's GDM+GNOME machine for GDM login behavior (same GDM from the same repos). The user's
  machine is probably a DVD install; this equivalence is unverified. Fallback if behavior
  diverges: kickstart from `~/ISOs/Rocky-10.2-x86_64-dvd1.iso` with the GNOME desktop group
  (a `vm-test/rocky10.ks` already exists as a starting point).
- **A2** The user's machine runs SELinux **enforcing**. All prior harness runs were permissive, so
  the matrix includes an enforcing scenario and every baseline task sets the mode deterministically
  (`setenforce` + `/etc/selinux/config`), never relying on the image default.
- **A3** GDM uses the `gdm-password` PAM service for interactive password login regardless of the
  selected session (GDM architecture knowledge, not verified here). The reproduction confirms this
  from the service tag in `/var/log/secure` (e.g. `pam_unix(gdm-password:auth): ...`). If the Cinnamon
  attempt shows a *different* service, the hypothesis routing in H2 changes.
- **A4** "Authentication Error" is GDM's login-failure dialog. The exact journal wording per failure
  phase (auth vs session-open vs session-launch) is identified from captured logs in item 4.
- **A5** The fix lands in the spec/packaging of the git clone
  `~/Linux/projects/cinnamon-for-rocky10/` (branch `main`). The project dir
  `~/Linux/projects/cinnamon_4_rocky10/` has no `.git` and is not modified.
- **A6** Fresh Sparky QEMU (KVM-backed) VMs per scenario satisfy the DoD's "fresh libvirt Rocky
  Linux 10 VM" isolation intent; the interactive reproduction phase (items 4, 5) uses the libvirt
  harness. The Sparrow tasks are VM-manager-agnostic, so the matrix could be re-pointed at
  libvirt-provisioned disks without rewriting tasks if Robotnik reads the DoD more strictly.
- **A7** Host RAM supports one 4GB VM at a time (existing harness baseline). Matrix scenarios run
  sequentially by default; `Big` may fan out two Sparky jobs if the host has ≥12GB free, recorded in
  `## Test Results`.
- **A8** `xdotool` or a fallback input driver is obtainable in the VM. Item 3 checks
  `dnf provides /usr/bin/xdotool` before any driver code is written; fallback ladder in risk R1.
- **A9** Host has outbound internet (Raku/zef deps, VM `dnf`), as in all prior runs.

### VM reproduction design (DoD boxes 1 and 2)

VM: fresh cloud image via `vm-test/provision-vm.sh`, modified (item 2) to add `--graphics vnc` so
the agent can observe the greeter while the driver works. Baseline (user's configuration, A1):
`dnf install gdm gnome-shell xorg-x11-server-Xorg` (+ whatever the control GNOME login needs — the
item-2 script records the exact package set in `## Test Results`), `WaylandEnable=false` in
`/etc/gdm/custom.conf` to force the X11 greeter (required for `xdotool`), GDM enabled, a test user
with an **ephemeral random password generated inside the VM at task start** (never committed, never
leaves the VM). SELinux permissive for the base reproduction (matches the user's failure only if the
user's machine is permissive — hence S5 enforcing is a first-class matrix scenario, not a stretch).

Login drive (shared library `tasks/lib/gdm-drive.sh`, also used by the matrix):
1. Extract XAUTHORITY from the running Xorg: `tr '\0' '\n' < /proc/$(pgrep -x Xorg | head -1)/environ | grep ^XAUTHORITY=`.
2. Wait for the greeter; open the session selector (GDM greeter shortcut Ctrl+Alt+Down —
   GDM-docs knowledge, confirmed by VNC observation in item 2); select the target session.
3. Type username, Tab, type password, Enter. Wait up to 120s.
4. Verdict by **state, not pixels**: `loginctl list-sessions` shows an online session for the user
   with `Type=x11`; the session's desktop process is running (`pgrep -u <user> cinnamon` or
   `gnome-shell`); greeter no longer owns the console.
5. Evidence capture, always (both outcomes): `journalctl -u gdm --since <t0>`,
   `journalctl _UID=<uid> --since <t0>` (the session-launch view), `tail -n 200 /var/log/secure`,
   `loginctl show-session <id>`, `getenforce`, best-effort greeter screenshot (`xwd -root`,
   package installed by the task if missing). Evidence lands in `vm-test/results/` (gitignored)
   and the *quoted lines* go to `## Test Results` per the DoD.

Sequence on one VM (item 4): baseline → INSTALL.md install (setup-repo.sh + the two `dnf install`
commands + `ldconfig`, exactly INSTALL.md:27-48) → **Cinnamon login attempt (expected FAIL, the
reproduction)** → evidence → **GNOME login attempt (expected PASS, the control)** → evidence →
**reboot → Cinnamon login retry** (the user's recovery path; expected to tell us whether the failure
is first-attempt-only) → evidence.

### Root-cause hypotheses, test order

The reproduction's journal decides which phase failed; the hypotheses are ordered by cost of
discrimination, cheapest first. H2's evidence comes for free from the reproduction.

| # | Hypothesis | Evidence that confirms | Evidence that kills |
|---|---|---|---|
| H1 (inspect first, item 3) | **Session-file/packaging content**: installed session entry or its referenced files are wrong or missing — missing `RequiredComponents` (e.g. `nemo-autostart` absent if nemo missing), missing session definition, missing systemd user unit, wrong `Exec`/`TryExec` | `rpm -ql`/`rpm -V`/installed-file diff shows a gap; failed-login journal shows `cinnamon-session` reporting a missing component or missing file | All installed files match upstream expectations and the failure phase is PAM auth (H2) |
| H2 (free with item 4) | **PAM auth failure**: `pam_unix(gdm-password:auth)` (or another module) rejects the Cinnamon attempt | `/var/log/secure` shows an auth failure tagged with the service GDM actually used for the Cinnamon attempt, absent for the GNOME attempt | `pam_unix` succeeds for the failed attempt → failure is in session-open/launch, not auth. Because the PAM service is session-independent (A3), a Cinnamon-only PAM failure would itself be the finding |
| H3 (experiments, item 5) | **Transient first-login state after live install** (fits "reboot restored the session"): systemd unit not registered until reboot (scriptlet/user-unit gap — see verified facts), GDM user/session state, first-run dconf profile initialization for a pre-existing GNOME user | Install→reboot→login succeeds while install→immediate-login fails; or install→`systemctl daemon-reload`→login succeeds; journal diff between failed and post-reboot successful attempts shows the state delta | Both immediate and rebooted installs fail identically (then it is not transient) |
| H4 (S5 scenario) | **SELinux enforcing + GDM/GNOME interaction**: AVC denials in the Cinnamon launch path on the user's (enforcing) machine; all prior tests ran permissive | Enforcing-VM reproduction fails with `audit`/AVC lines correlated to the Cinnamon path, absent for GNOME | Enforcing VM behaves like permissive (no AVCs, same or no failure) |

Experiments (item 5), each a fresh VM: **B** install → reboot → Cinnamon login (reboot-before-first-
login); **C** install → `systemctl daemon-reload` (+ `loginctl`/user-manager state check) → Cinnamon
login without reboot. B and C split H3's sub-hypotheses: if B passes and C passes, the fix is a
reboot/daemon-reload in the install path (or a spec scriptlet); if B passes and C fails, it is
unit-registration state; if both fail, H3 is out.

### Fix approach (item 3 of the task brief)

- **Where**: commits go to the clone `~/Linux/projects/cinnamon-for-rocky10/` (branch `main`,
  feature branch per house practice, PR, Knuckles merges). The project dir
  `~/Linux/projects/cinnamon_4_rocky10/` (upstream source trees, no `.git`) is not modified
  (A5).
- **How**: the spec files in the repo are the single source of truth for packaging. Per-root-cause
  shape, following existing house style (`spec/cinnamon.spec:52-85` shows the established
  `%prep` sed-patch pattern):
  - H1 (file missing/mispackaged): add the file to `%files`, or ship a corrected copy via
    `%prep`/`%install`; fix `RequiredComponents` via a `%prep` patch if the `.session` content is
    wrong for EL10.
  - H2 (PAM): replace/patch `/etc/pam.d/cinnamon` content in the spec, or drop the file from
    `%files` if it serves no purpose on RHEL (it is not in GDM's login path) — decision from the
    evidence, recorded in `## Implementation` alternatives.
  - H3 (unit/scriptlet gap): add the unit to `%files` and add the `%post` `systemctl daemon-reload`
    scriptlet (or the `%systemd_post` macro) so live installs register units without a reboot.
  - H4 (SELinux): minimal fix in packaging (correct file contexts, a small policy module, or a
    relabel step) — a *full* Cinnamon SELinux policy is a follow-up task.
- **Rebuild**: affected packages only, host `rpmbuild` at `-j2` (established OOM constraint,
  TASK-0002). `spec/` owns the rebuild; the item records build time and artifacts.
- **Repo hygiene before re-repoing** (known gotcha, TASK-0004): remove the superseded old-version
  RPMs from `rpms/`, regenerate `repodata/` with `createrepo_c`, verify package count (48) and
  versions with `dnf list` on a scratch VM.
- **No user-machine config changes** are part of the deliverable (DoD fix-committed box).

### Sparky/Sparrow test matrix (DoD boxes 6 and 7)

Framework facts (Rocky docs, `sparky_getting_started`): Sparky is a Raku CI server (`sparkyd` +
`cro run`, web UI `:4000`) that boots QEMU VMs from the `qemu_image` list in
`~/.sparky/templates/vars.yaml`, installs a Sparrow client into the image, and runs Sparrow tasks
(Raku) from the `use_case_repo` git repos. A test project is `main.raku` (`task-run "tasks/x"`)
plus `tasks/<name>/task.bash`. Host prerequisites per AGENTS.md §7: Raku via the raku-install
script (not in EL10 repos), Sparky from `github.com/melezhik/sparky` via zef, `Sparky::JobApi`.

**Scenarios** (each a fresh VM; the first four are DoD-mandated, S5/S6 are the practical additions
this breakdown absorbs):

| ID | Scenario | Baseline | Steps | Verdict checks |
|---|---|---|---|---|
| S1 | GDM + GNOME (user's config) | GDM + GNOME, X11 greeter | INSTALL.md install → Cinnamon login → GNOME login (control) → in-session verify | Cinnamon login PASS, no Authentication Error; GNOME login PASS; session processes running |
| S2 | LightDM | LightDM (X11 seat) | INSTALL.md install → Cinnamon login via LightDM → verify | Cinnamon login PASS; LightDM greeter back after logout |
| S3 | No login manager | bare cloud image | INSTALL.md install → assert session available, no DM pulled in → install GDM → Cinnamon login | `/usr/share/xsessions/cinnamon.desktop` + `TryExec` binary present; `dnf repoquery` shows no DM in the install set; Cinnamon login PASS after GDM install (answers the Status unknown "how a blank install gets a working login") |
| S4 | Uninstall | S1 baseline | install → Cinnamon login OK → remove all `cinnamon-rocky10` packages → verify clean → reboot → GNOME login | `dnf check` clean; no dangling `Requires`; `xsessions/cinnamon.desktop` and `/etc/pam.d/cinnamon` gone; no PAM breakage; GNOME login PASS |
| S5 | SELinux enforcing | S1 baseline, enforcing (A2) | same as S1 | both logins PASS; `ausearch -m avc -ts recent` empty (or every denial explained in `## Test Results`) |
| S6 | Reboot-first | S1 baseline | install → reboot → **first** Cinnamon login after boot | Cinnamon login PASS (regression for the H3 class: first login must work even before any post-install reboot) |

**Harness layout** (committed to `metalllinux/cinnamon-for-rocky10`; final paths recorded in
`## Test Results` per DoD):

```
cinnamon-for-rocky10/
├── main.raku                          # Sparky entry: one task-run chain per scenario
├── tasks/
│   ├── lib/gdm-drive.sh               # shared: XAUTHORITY extract, session select, input, evidence
│   ├── gdm-gnome/{01-baseline,02-install-cinnamon,03-login-cinnamon,04-login-gnome,05-verify-session}/task.bash
│   ├── lightdm/{01-baseline,02-install-cinnamon,03-login-cinnamon,04-verify-session}/task.bash
│   ├── no-dm/{01-baseline,02-install-cinnamon,03-session-available,04-install-gdm,05-login-cinnamon}/task.bash
│   ├── uninstall/{01-baseline,02-install-cinnamon,03-login-cinnamon,04-remove,05-verify-clean,06-login-gnome}/task.bash
│   ├── selinux-enforcing/{01-baseline,02-install-cinnamon,03-login-cinnamon,04-login-gnome,05-avc-check}/task.bash
│   └── reboot-first/{01-baseline,02-install-cinnamon,03-reboot,04-login-cinnamon,05-login-gnome}/task.bash
├── sparky/
│   ├── vars.yaml.template             # qemu_image (seeded image), use_case_repo, qemu_machine, ssh_key_path
│   ├── seed-image.sh                  # cloud qcow2 → seeded qcow2 (rpms/ + repo-setup/ at /opt/cinnamon-for-rocky10)
│   └── README.md                      # one-time host setup + how to run each scenario
└── vm-test/                           # existing libvirt harness
    └── test-gdm-login.sh              # new (item 2): reproduction + experiments driver
```

Each `task.bash`: `#!/bin/bash -`, `set -euo pipefail`, explicit `PASS`/`FAIL`/`SKIP` lines,
evidence to `/root/evidence/` inside the VM, exit code = verdict. The login tasks source
`tasks/lib/gdm-drive.sh` (the whole repo is the `use_case_repo` clone, so relative paths resolve).
The test user's password is generated inside the VM at baseline-task start and stays there.

**RPM transfer to Sparky VMs**: primary mechanism is the **seeded image** —
`sparky/seed-image.sh` copies the cloud qcow2 and `virt-customize --upload`s
`rpms/` + `repo-setup/` to `/opt/cinnamon-for-rocky10/`, then the scenario's
`02-install-cinnamon` task runs the shipped `setup-repo.sh` against that path (the real user
procedure, `file://` baseurl). This keeps scenarios self-contained and re-runnable with no host
service. Fallbacks if Sparky's QEMU networking or image handling resists: host HTTP server
(`python3 -m http.server`) with the VM pulling from `10.0.2.2` (slirp), or a plain
`dnf install http://...` list. Item 9a resolves the mechanism against the cloned Sparky source and
records it in `sparky/README.md`. Re-seed the image whenever `rpms/` changes (the script is
idempotent and records the `rpms/` git hash in the image name).

**Execution and parallelism**: scenarios are independent (fresh VM each) but share the host; run
sequentially by default (A7), two-at-a-time only if `Big` verifies headroom. Item 10 runs all six
against the **fixed** RPMs and records the "checks requested vs run" count (≈30–40 checks per
scenario class; `Big` counts them explicitly — DoD nothing-dropped box).

### Work breakdown

One agent, one turn per item. Reproduction and matrix execution are owned by `Big` per the
Definition of Done; `Tails` writes the harness scripts (house pattern from TASK-0003).

| # | Item | Owner agent | Acceptance criterion | Parallel with |
|---|---|---|---|---|
| 1 | Host Sparky infrastructure: Raku (raku-install script), Sparky clone + zef install, `Sparky::JobApi`, `Sparky_Rocky` `sync_project.sh` (`~/.sparky`, `~/sparky.yaml`), QEMU binary/machine verification per docs, firewall `:4000`, sudoers drop-in (NOPASSWD `mount`/`umount`), start `sparkyd` + `cro run` | Tails | `curl -sS localhost:4000` serves the web UI; both services running; a no-op scaffold test project (docs pattern) runs end-to-end to "succeed"; setup notes written to `## Implementation` (item 9a moves them into `sparky/README.md`) | 2, 3, 9a |
| 2 | GDM login harness (libvirt): `vm-test/test-gdm-login.sh` + `tasks/lib/gdm-drive.sh` — VNC-graphics provisioning, GDM+GNOME baseline + ephemeral test user, `xdotool` greeter driver (XAUTHORITY from `/proc/<Xorg>/environ`, Ctrl+Alt+Down session select, input, 120s wait), state-based verdict, evidence capture, `--reboot-after-install` / `--daemon-reload-after-install` / `--selinux {enforcing,permissive}` modes | Tails | On a fresh GDM+GNOME VM the harness: (a) logs the test user in to **GNOME** (control) and reports PASS with evidence files; (b) after the INSTALL.md repo install, attempts **Cinnamon** login and reports PASS or FAIL with the same evidence set, handling the failure path gracefully (no abort before capture); driver behavior confirmed by VNC observation | 1, 3 |
| 3 | Static packaging inspection: host `rpm -qlp`/`rpm -q --scripts` over all 48 RPMs (xsessions/pam/session/systemd files; the cinnamon-session user-unit question); scratch-VM installed-state check (diff `/etc/pam.d/cinnamon` vs source, `xsessions/cinnamon.desktop`, `sessions/cinnamon.session` + `RequiredComponents` presence incl. `nemo-autostart`, `rpm -V` all 14, `ldd`); availability probes (`dnf provides /usr/bin/xdotool`, `ydotool`, `dogtail`; `dnf provides /usr/bin/lightdm`; `getenforce` on the cloud image) | Big | Findings in a `## Test Results` pre-section with command + output for every claim; each of H1–H4 marked supported/unsupported; the input-driver choice and LightDM availability decided and recorded | 1, 2 |
| 4 | Reproduction run (pre-fix RPMs): fresh GDM+GNOME VM → INSTALL.md install → Cinnamon login (expected FAIL) → evidence → GNOME login (expected PASS) → evidence → reboot → Cinnamon login retry → evidence | Big | DoD reproduction + evidence boxes: `## Test Results` quotes `journalctl -u gdm` and `/var/log/secure` lines for both the failed Cinnamon attempt and the successful GNOME login on the same VM; the failure phase (auth / session-open / session-launch) is identified; the reboot-retry outcome is recorded | 2, 3 |
| 5 | Root-cause experiments: VM-B install→reboot→Cinnamon login; VM-C install→daemon-reload→Cinnamon login; failed-launch user-session journals (`journalctl _UID=`); route H1–H4 to a final root cause | Big | DoD root-cause box: 1–3 sentences plus the quoted log lines proving it; B/C experiment table in `## Test Results`; hypothesis routing explained | 4 |
| 6 | Fix: implement in the clone per root cause (spec `%prep`/`%files`/scriptlets or session files; no user-machine config), rebuild affected RPMs at `-j2`, snapshot pre-fix `rpms/` as a tarball (path recorded), replace `rpms/` (remove old versions), regenerate `repodata`, commit on a feature branch | Tails | `rpmbuild` clean; `rpm -K` OK; fixed RPMs install from the repo on a scratch VM (`dnf list` shows new versions, count 48); diff confined to spec/packaging/session files; `## Implementation` filled (alternatives, changes table, checks run, build times) | 5 |
| 7a | Review: fix diff + harness/task changes | Shadow | Findings in `## Review`; no unresolved blockers or should-fix | 7b, 7c |
| 7b | Security: PAM file content (if changed), ephemeral-test-user credential pattern, `gpgcheck=0` scope of the local repo, host sudoers/firewall/port changes | Omega | Findings in `## Security`; nothing unresolved above `low` | 7a, 7c |
| 7c | Fix verification: fresh GDM+GNOME VM with fixed RPMs — Cinnamon login works (no Authentication Error, no reboot), GNOME login still works | Big | DoD fix-verified box satisfied, evidence in `## Test Results` | 7a, 7b |
| 8 | Resolve 7a/7b/7c findings; rebuild/re-repo if packaging changed; re-verify | Tails | All findings resolved with `Resolution` filled; 7c green again if anything changed | 7a, 7b, 7c |
| 9a | Sparky/Sparrow task suite, core scenarios: `main.raku` + `tasks/{gdm-gnome,lightdm,no-dm,uninstall}` + `tasks/lib`, `sparky/{vars.yaml.template,seed-image.sh,README.md}`; resolve the RPM-transfer mechanism against the Sparky source | Tails | `bash -n` clean on every `task.bash`; `main.raku` parses under Raku (needs item 1); `seed-image.sh` idempotent, produces a bootable image (boot check passes); README records layout, final paths, transfer mechanism | 1, 2 (sync driver changes from 2 into tasks here if 2 landed first) |
| 9b | Sparky/Sparrow task suite, extended scenarios: `selinux-enforcing`, `reboot-first`; sync any driver changes discovered in items 2/4/5 into all tasks | Tails | Same as 9a for the new tasks; driver logic identical across all six scenarios | 5, 9a |
| 10 | Full Sparky matrix: all six scenarios on fresh VMs against the fixed RPMs; harness bugs fixed by `Big` in place; code bugs routed to `Tails` | Big | DoD full-matrix + reusable-tests + nothing-dropped boxes: per-scenario PASS/FAIL with evidence in `## Test Results`, committed task paths recorded, "checks requested vs run" count explicit, no silent skips | 8, 9a, 9b |
| 11 | Fix matrix FAILs that are code bugs; re-run affected scenarios with `Big` | Tails | Matrix green, or each remaining FAIL explicitly blocked with evidence and named in `## Test Results` | 10 (loop) |
| 12 | Docs: INSTALL.md (rewrite the GDM section: switching to Cinnamon on an existing GDM+GNOME system; first-login/reboot behavior if root cause is H3; Authentication-Error troubleshooting with the journal commands), README.md (incl. the 10-vs-14 package count discrepancy carried from TASK-0006) | Vector | DoD docs box: README + INSTALL updated as affected; INSTALL.md remains a correct end-to-end procedure | 10 |
| 13 | Release: PR to `main` (internal `metalllinux` repo, no human review), merge, push | Knuckles | DoD release box; `## Release` filled (branch, PR, merge commit) | 12 |
| 14 | Prune planning doc (superseded plan detail → `## Archive`) | Espio | `## Archive` updated; doc pruned per house rules | 13 |

### Dependencies and sequence

Genuinely ordered: 2 → 4 → 5 → 6 → (7a ∥ 7b ∥ 7c) → 8 → 10 → 12 → 13 → 14, plus 9b → 10 and
6 → 9b is not required (9b only needs the root-cause outcome from 5 for scenario expectations).

Explicitly parallel:
- **Wave 0 (all independent, start together)**: 1 ∥ 2 ∥ 3 ∥ 9a. Item 9a's Raku parse check waits
  on 1; its bash work does not.
- **Wave 4**: 7a ∥ 7b ∥ 7c on the same diff (the standard review fan-out).
- 10's scenarios are mutually independent once started; sequential-by-default execution is a
  resource choice (A7), not a dependency.

Items that only *look* ordered: 3 before 4 (the inspection informs the reproduction's focus, but the
reproduction script runs the same way regardless) — kept sequential anyway because 3's
input-driver decision (A8) gates 2's final form, and 4 needs 2. 9a before 6 is **not** required:
the tasks test behavior, not RPM content, and run against whatever `rpms/` holds at item 10.

### Critical path

2 → 4 → 5 → 6 → 7c → 8 → 10 → 12 → 13. (1, 3, 9a, 7a, 7b overlap earlier waves; 9b and 11 feed
into 10/its loop; 14 is tail.)

### Estimates

Three-point, hours, `T = (O + 4M + P) / 6`.

| # | Item | O | M | P | T |
|---|---|---|---|---|---|
| 1 | Sparky host infra | 1 | 3 | 6 | 3.2 |
| 2 | GDM login harness | 2 | 4 | 8 | 4.3 |
| 3 | Static inspection | 0.5 | 1 | 2 | 1.1 |
| 4 | Reproduction run | 1 | 2 | 4 | 2.2 |
| 5 | Root-cause experiments | 1 | 2 | 4 | 2.2 |
| 6 | Fix + rebuild + re-repo | 1 | 4 | 10 | 4.5 |
| 7a | Shadow review | 0.5 | 1 | 2 | 1.1 |
| 7b | Omega security | 0.5 | 1 | 2 | 1.1 |
| 7c | Fix verification | 0.5 | 1.5 | 3 | 1.6 |
| 8 | Finding fixes + re-verify | 0 | 2 | 4 | 2.0 |
| 9a | Sparrow core tasks + harness | 1 | 2 | 4 | 2.2 |
| 9b | Sparrow extended tasks | 0.5 | 1.5 | 3 | 1.6 |
| 10 | Full matrix | 2 | 5 | 10 | 5.3 |
| 11 | Code-bug fix loop | 0 | 2 | 5 | 2.2 |
| 12 | Vector docs | 0.5 | 1 | 2 | 1.1 |
| 13 | Knuckles release | 0.25 | 0.5 | 1 | 0.5 |
| 14 | Espio prune | 0.25 | 0.5 | 1 | 0.5 |

Critical path sum: **23.7h**. Buffer: +10h (~40%) — the GDM driver is unproven on this stack
(A8), Sparky is a first run on this host, and the root cause is unknown until item 5. **Planned
total ≈ 34h** of agent work; wall time is dominated by VM provisioning and login waits in items 2,
4, 5, 10 (each VM cycle ≈10–20 min).

### Risks

| # | Risk | Likelihood | Impact | Mitigation | Contingency |
|---|---|---|---|---|---|
| R1 | Greeter automation fails: `xdotool` absent from EL10 repos, XAUTHORITY quirks, GDM shortcut differences | Medium | High | Item 3 probes availability before driver code; X11 greeter forced; VNC channel lets the agent watch and correct; verdicts are state-based, not pixel-based | Fallback ladder `ydotool` → `dogtail` → in-VM XTest micro-driver compiled from `xorg-x11-devel` (guaranteed feasible, test-only, never shipped in the Cinnamon repo) |
| R2 | Failure does not reproduce in the VM (DVD-vs-cloud base, enforcing-vs-permissive, user-specific state) | Medium | High | Enforcing variant is a first-class scenario (S5); both greeter modes checked; A1 fallback is a DVD kickstart | Ask the user (human gate) for `journalctl -u gdm` + `/var/log/secure` from the real machine; if still unreproducible, the DoD reproduction box is **not** met — stop and escalate, do not ship a guessed fix |
| R3 | Sparky host infra fails (Raku/zef on EL10, port 4000, firewall) | Medium | Medium | Documented install path (Rocky docs target Rocky); item 1 is time-boxed and isolated from the reproduction path | Run the committed Sparrow tasks without the Sparky server: boot the same seeded image via the libvirt harness and invoke the tasks with the Sparrow client directly; tasks stay committed and re-runnable; deviation recorded in `## Test Results` |
| R4 | Rebuild cost: `cinnamon` is the heaviest package; host OOMed at `-j16` (TASK-0002) | Low | Medium | Rebuild affected packages only; `-j2` + `maxjobs=2` | Split across turns if a single build overruns; partial state recorded in `## Implementation` |
| R5 | Stale/old-version RPMs in `rpms/` break matrix installs (known gotcha, TASK-0004) | Medium | Medium | Item 6 snapshots pre-fix `rpms/`, removes old versions, re-`createrepo_c`, verifies count 48 | Restore `rpms/` from the snapshot and re-repo |
| R6 | LightDM not in EL10 repos | Low | Low | Item 3 probes `dnf provides /usr/bin/lightdm` | Scenario S2 recorded as blocked with the `dnf` evidence in the checks-requested-vs-run count — explicit, not silent |
| R7 | RPM transfer to Sparky VMs blocked by its QEMU networking | Low | Medium | Seeded-image mechanism is primary (no runtime host service) | Host HTTP server + slirp `10.0.2.2` pull, or direct `dnf install http://` list; mechanism recorded in `sparky/README.md` |

### Validation

Environments: host (Rocky Linux 10.2 runner), libvirt VMs for items 2/4/5/7c (cloud image, 2 vCPU,
4GB, default network, VNC), Sparky QEMU VMs for item 10 (same image, seeded, fresh per scenario,
SELinux mode set per scenario).

Checks, mapped to the DoD:
- Reproduction + evidence: `## Test Results` quotes `journalctl -u gdm` + `/var/log/secure` for the
  failed Cinnamon and successful GNOME logins, same VM (items 4).
- Root cause: 1–3 sentences + proving log lines (item 5).
- Fix: PR diff confined to spec/packaging/session files in `metalllinux/cinnamon-for-rocky10`
  (item 6); `rpmbuild` + `rpm -K` + scratch-VM `dnf list`.
- Fix verified: fresh VM, Cinnamon login clean, GNOME login intact (item 7c).
- Full matrix + reusable tests + nothing dropped: six scenarios, committed task paths, explicit
  checks-requested-vs-run count (item 10).
- Gates: `## Review` clean (Shadow), `## Security` ≤ low (Omega), README/INSTALL updated (Vector),
  PR merged (Knuckles).

Human look: **INSTALL.md** (item 12) — it is the user-facing procedure the user already followed
once, and it must be correct before the user retries the install. The merged PR is internal and
needs no review per AGENTS.md §8; the user may still want to see the diff.

### Rollback

- **Detection**: harness PASS/FAIL + captured journals (per-VM, immediate); red Sparky runs (per
  scenario, immediate); post-merge, a user report of the error recurring after upgrading RPMs
  (days-scale — the only slow signal, since nothing is auto-deployed to user machines).
- **Exact revert**: `git revert -m 1 <merge-sha>` on `metalllinux/cinnamon-for-rocky10` `main`,
  push (Knuckles), then rebuild the superseded RPMs and re-`createrepo_c` so `rpms/` matches
  pre-fix state; restore `rpms/` from the item-6 tarball snapshot instead if the rebuild is
  undesirable. Test VMs: `provision-vm.sh --destroy` (idempotent) / Sparky job `qemu_shut`.
  Host state from item 1 is additive and removed per the decision doc (Sparky/Raku installs,
  firewall rule, sudoers drop-in).
- **Point of no return**: none for users — nothing deploys, user machines are untouched, the fix is
  proven only in VMs before merge. The single destructive local step is the `rpms/` replacement in
  item 6, covered by the pre-fix tarball snapshot.
- **Leftover state after a failed run** (retries must tolerate it): VM disks under
  `/var/lib/libvirt/images/cinnamon-test/` (rm), Sparky image cache under `~/.sparky/`,
  `rpms/repodata/` (regenerable), in-VM test users and `/root/evidence/` (disposable with the VM),
  the host HTTP server if the R7 fallback was used (pkill by port). All harness entry points are
  idempotent by design (`--destroy`, seeded-image rebuild).

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

### Item 1

*Executed 2026-08-24 (00:30 to 01:26 JST). All four acceptance criteria met. No files in
`metalllinux/cinnamon-for-rocky10` were touched, per the item brief.*

**Acceptance criteria status**

| Criterion | Status | Evidence |
|---|---|---|
| `curl -sS localhost:4000` serves the web UI | MET | HTTP 303 to `/builds_latest`, HTML `<title>~SPARKY CI WEB~ \| latest builds</title>` (command + output below) |
| Both services running | MET | tmux sessions `sparkyd` and `cro-run` (login-shell PATH), processes `rakudo ~/.raku/bin/sparkyd.raku` and `cro run`, `ss -ltn` shows `LISTEN 0.0.0.0:4000` |
| No-op scaffold test project (docs pattern) runs end-to-end to "succeed" | MET | Trigger id `kvtmfqgjopawhnudicbr.283564`; `sqlite3 db.sqlite3 "SELECT id,project,state FROM builds"` returns state=1 (ok) for all three builds `sparky-rocky`, `qemu-session.default`, `test-use-case.default`; the in-VM task printed `no-op task ran OK` |
| Setup notes written to `## Implementation` | MET | This subsection (item 9a moves it into `sparky/README.md`) |

**Deviation from AGENTS.md section 7 (documented, not silent)**

- The section 7 command `curl -sL https://raw.githubusercontent.com/SuperBiBi20/raku-install/master/raku-install | bash`
  cannot be executed. The raw URL returns 404 and the GitHub account `SuperBiBi20` no longer exists
  (profile fetch also 404; verified 2026-08-24 with `curl` and `webfetch`).
- The current Rocky docs page for this exact task (
  `https://docs.rockylinux.org/10/guides/automation/sparky_getting_started/`, updated 2026-06-26)
  recommends for x86_64 the `rakudo-pkg` package repo (GPG-signed cloudsmith channel) as method 1 and
  rakubrew as method 2; the SuperBiBi20 script is no longer referenced.
- The interrupted Wave 0 session (2026-08-22) had already installed `rakudo-pkg 2026.7.0-01` from
  `/etc/yum.repos.d/nxadm-pkgs-rakudo-pkg.repo` (GPG key imported, dnf signature-verified) and added
  the PATH line at `~/.bash_profile:9`. I completed the documented remaining steps instead of
  rebuilding from source. **Recommendation to the user: update the Raku line in AGENTS.md section 7
  to the rakudo-pkg procedure** (user-facing file, I did not edit it).
- Chosen over a source build because a GPG-verified dnf package is a stronger supply-chain position
  than `curl | bash` from a now-deleted personal repo, and the binary was already half-installed and
  healthy.

**Security observations (for Omega / user, redacted per section 4)**

- `~/Code/sparky/.git/config` origin remote embeds a `metalllinux` GitHub token in the URL
  (`https://metalllinux:ghp_...@github.com/melezhik/sparky.git`). Not committed anywhere; local git
  config only. Same pattern as the cinnamon clone origin the user decided (2026-08-21, `## Status`)
  to keep as-is. Token value deliberately not recorded here.
- `~/.gitconfig` carries a global `url.https://metalllinux:ghp_...@github.com/.insteadOf=https://github.com/`
  rewrite, so every git operation this user performs against github.com authenticates with that token.
  Pre-existing user configuration; not modified.
- `raku db-init.raku` prints the local Sparky API token to stdout (it is in `~/sparky.yaml`, a 15-char
  random string for local Sparky auth, not a GitHub credential). Value not recorded here.
- None of the above is committed, and none was written to any file or doc by this item.

**Commands run and evidence** (in order)

1. State inspection: `~/.raku/bin/` had only the zef wrapper (which `exec`s `rakudo`, absent from
   PATH); `~/.zef/store` empty; `rpm -q rakudo-pkg` -> `2026.7.0-01 @nxadm-pkgs-rakudo-pkg`;
   `/opt/rakudo-pkg/bin/raku --version` -> `Rakudo v2026.07, Raku v6.d, MoarVM 2026.07`.
2. Dependencies per docs: `dnf list installed` over the 13 docs packages -> all present except `vim`
   (provided by installed `vim-minimal` 9.1.083-9.el10; `which vim` -> `/usr/bin/vim`;
   `sudo dnf install -y vim` -> "Nothing to do").
3. Raku completion: `/opt/rakudo-pkg/bin/add-rakudo-to-path` -> "PATH already in ~/.bash_profile.
   Skipped." (line 9 already covers the three dirs); `/opt/rakudo-pkg/bin/install-zef` -> zef 1.1.3
   reinstalled, `Testing [OK]`; fresh login shell check
   `bash -lc 'which raku rakudo zef; raku -v | head -1; zef --version'` ->
   `/opt/rakudo-pkg/bin/raku`, `/opt/rakudo-pkg/bin/rakudo`, `/home/howard/.raku/bin/zef`,
   `Welcome to Rakudo v2026.07.`, `1.1.3`.
4. Sparky from clone (`~/Code/sparky` pre-existing, in sync with origin/master at `add1b02`, tag
   0.2.32; `git fetch && git status -sb` clean). Documented three-stage install, logged to
   `/tmp/opencode/sparky-zef-install.log`: `zef install DBIish --/test` (rc=0) ->
   `zef install cro --deps-only` (rc=0) -> `zef install cro` (rc=0) -> `zef install .` (rc=0),
   every module `Testing [OK]`. Installed set: Sparky 0.2.32, Sparky-Job-Api 0.0.13, cro 0.8.10,
   Cro::Core 0.8.10, Cro::HTTP 0.8.13, Cro::TLS 0.8.10, Cro::WebApp 0.10.1, Cro::WebSocket 0.8.10,
   DBIish 0.6.8, DBIish::Pool 1.1.0, Sparrow6 0.0.93, Sparrowdo 0.1.55. Bin scripts in
   `~/.raku/bin`: `sparkyd`, `sparrowdo`, `sparman`, `sparky-runner`, `sparky-web.raku`, `s6`, `rakurl`.
5. `cd ~/Code/sparky && raku db-init.raku` -> rc=0, "SQLite db populated as
   /home/howard/.sparky/projects/db.sqlite3".
6. `zef install Sparky::JobApi` -> "All candidates are currently installed" (the success line the
   docs promise).
7. `cd ~/Code/Sparky_Rocky && bash scripts/sync_project.sh` -> the exact expected five lines
   (Creating project folder / Checking for ~/sparky.yaml / Creating API Key in ~/sparky.yaml /
   Checking for ~/.sparky/templates/vars.yaml / Copying project files). Created
   `~/.sparky/projects/sparky-rocky/` (sparrowfile, sparky.yaml, tasks: check-ssh, container,
   kickstart-bootstrap, run-qemu-box, setup-qemu-image, stop-qemu-box),
   `~/.sparky/templates/vars.yaml`, `~/sparky.yaml`.
8. QEMU verification per docs: `which qemu-kvm` -> absent; `/usr/libexec/qemu-kvm` present
   (QEMU 10.1.0, qemu-kvm-10.1.0-16.el10_2.2); created `ln -s /usr/libexec/qemu-kvm ~/bin/qemu-kvm`
   (chosen over the docs' alias because Sparky invokes the binary from Raku, not from bash);
   `qemu-kvm -machine help` -> best non-deprecated machine `pc-q35-rhel10.2.0` (alias `q35`);
   set in `~/.sparky/templates/vars.yaml` (`qemu.machine`, with comments at the edit site).
9. SSH per docs: `~/.ssh/id_ed25519` already present (created 2026-08-22 by the interrupted
   session); `vars.yaml` `ssh_key_path` set to `~/.ssh/id_ed25519.pub` (replacing the template's
   `id_rsa.pub`).
10. Sudoers drop-in: wrote `/etc/sudoers.d/sparky` (0440 root:root) with
    `howard ALL=(ALL) NOPASSWD: /usr/bin/mount,/usr/bin/umount`; `sudo visudo -c -f` -> "parsed OK";
    functional check `sudo -n mount --version` runs passwordless; `sudo -n -l` shows the rule.
    Drop-in chosen over editing `/etc/sudoers` per house package-ownership/least-privilege rules.
11. Firewall: **N/A on this host.** `systemctl is-active firewalld` -> `inactive`; no firewall
    daemon is running, so there is no live rule to add and the UI is already reachable on
    localhost. Enabling firewalld would switch the whole machine to default-deny and could break
    unrelated services (e.g. the model endpoint on 192.168.1.106:8084); that is a system-wide
    posture change outside item 1 and was not done unilaterally. If firewalld is ever enabled, run
    `sudo firewall-cmd --add-port=4000/tcp --permanent && sudo firewall-cmd --reload`.
12. Services: `tmux new-session -d -s sparkyd 'bash -lc "cd ~/Code/sparky && exec sparkyd ..."'` and
    same for `cro-run` (`cro run`); `ss -ltn` -> `LISTEN 0.0.0.0:4000`;
    `curl -sS -i localhost:4000` -> `HTTP/1.1 303 See Other, Location: /builds_latest`;
    `curl -sS -L localhost:4000` -> the web UI HTML (title above).
13. No-op scaffold per the docs pattern ("Writing new tests -> Creating a repository"):
    `~/Code/sparky-noop/` with `README.md`, `main.raku`
    (`#!raku` + `task-run "tasks/check-noop";`), `tasks/check-noop/task.bash`
    (`#!/bin/bash -` + echo); `git init` + commit `850bb2a` (local repo, no remote needed because
    `Sparky_Rocky/sparrowfile` supports local dirs, `sparrowfile:174` `if $use_case_repo.IO ~~ :d`);
    added `~/Code/sparky-noop` to `use_case_repo` in `~/.sparky/templates/vars.yaml`
    (the template's own comment endorses local directories).
14. End-to-end run: `curl -c cj -d 'login=admin&password=admin' localhost:4000/default_login`
    -> 303 "user [admin] logged in" (default admin/admin account seeded at
    `lib/Sparky.rakumod:57-59`, matching the docs);
    `curl -b cj --data-urlencode 'tags=test_env=qemu,version=Rocky-10-GenericCloud:https://dl.rockylinux.org/pub/rocky/10/images/x86_64/Rocky-10-GenericCloud-Base.latest.x86_64.qcow2,releasever=10.2,use_case_repo=/home/howard/Code/sparky-noop,qemu_binary=qemu-kvm,qemu_machine=pc-q35-rhel10.2.0,ssh_key_path=~/.ssh/id_ed25519.pub,bootstrap=True,qemu_shut=True' --data-urlencode 'description=...' localhost:4000/build-with-tags/project/sparky-rocky`
    -> 200, trigger id `kvtmfqgjopawhnudicbr.283564` at 01:20:35 JST.
    - Pre-verified the VM-side bootstrap dependency first: the COPR `grayeul/TestProj` epel-10
      chroot repo is live (`.repo` served at
      `copr.fedorainfracloud.org/coprs/grayeul/TestProj/repo/epel-10/grayeul-TestProj-epel-10.repo`,
      baseurl `download.copr.fedorainfracloud.org/results/grayeul/TestProj/epel-10-x86_64/`), and its
      `primary.xml` lists `rakudo`, `moarvm`, `nqp`, `zef`, `raku-sparrow6`, `raku-sparrowdo`,
      `raku-sparky-job-api` plus the raku-* dependencies. (An earlier probe of
      `copr.fedorainfracloud.org/repo/grayeul/...` 404'd because that path scheme is not the one dnf
      uses; the `dnf copr enable` flow fetches the `.repo` file above.)
    - Result: `sqlite3 ~/.sparky/projects/db.sqlite3 "SELECT id,project,state FROM builds ORDER BY id"`
      -> `1|sparky-rocky|1`, `2|qemu-session.default|1`, `3|test-use-case.default|1` (state 1 = ok
      per the web UI's state mapping, `templates/builds_latest.crotmp`).
    - Report evidence in `~/.sparky/projects/.reports/`:
      - `qemu-session.default/build-2.txt`: VM reached the `Rocky Linux 10.2 (Red Quartz)` login
        prompt; task check `# qemu should reach login prompt` -> `True`.
      - `test-use-case.default/build-3.txt`: in-VM bootstrap installed curl/openssl-devel/wget/perl-*,
        enabled the COPR (GPG key imported), installed moarvm-2026.07, nqp-2026.04, rakudo-2026.04,
        zef-1.1.1, raku-sparrow6-0.0.93, raku-sparky-job-api-0.0.12 plus deps; framework pre-tasks ran
        (scm dir, echo OK, `sudo dnf install -y python3-pip`, rl-releasever -> releasever 10.2);
        `use_case_repo.tar` fetched from `http://10.0.2.2:4000/file/...` and unpacked;
        `load scenario from main.raku`; `tasks/check-noop` -> `no-op task ran OK`.
      - `sparky-rocky/build-1.txt`: `job succeeded` (exit 0); `qemu_shut=True` ->
        `tasks/stop-qemu-box` killed the QEMU process.
    - Wall time 01:20:35 to 01:25:42 JST (~5 min) including the 545MB image download at ~4.2MB/s.

**Alternatives considered**

**Problem: get a working Raku on this host per the item brief**
**Option A — raku-install script from AGENTS.md section 7.** How: `curl | bash` as written. Pros:
letter of the brief. Cons: the URL is dead (404, account gone); nothing to execute.
**Option B — rakudo-pkg package repo (current Rocky docs, method 1).** How: keep the
`rakudo-pkg 2026.7.0-01` the interrupted session installed and finish the documented
`add-rakudo-to-path` / `install-zef` steps. Pros: GPG-signed dnf package (best supply-chain
position), already partially installed and healthy, minutes instead of a 30-60 min source build.
Cons: deviates from the section 7 line, which must be updated by the user.
**Option C — rakubrew source build (docs method 2).** How: `rakubrew download moar-...`. Pros:
from source. Cons: long build, a second Raku alongside a working one, no gain.
**Chosen:** B, because A is impossible and B is the docs' recommended path with a verifiable
signature chain.

**Problem: put `qemu-kvm` on PATH**
**Option A — bash alias (docs option 1).** Cons: aliases do not apply in non-interactive Raku
invocations, which is how Sparky launches QEMU.
**Option B — symlink `~/bin/qemu-kvm` (docs option 3).** How: `ln -s /usr/libexec/qemu-kvm ~/bin/qemu-kvm`
(`~/bin` is already on PATH). Pros: works from any context.
**Chosen:** B.

**Problem: host the no-op scaffold repo**
**Option A — push a public GitHub repo under metalllinux.** Cons: an external artifact for a
host-local infrastructure check; not needed.
**Option B — local directory.** How: `~/Code/sparky-noop` added to `use_case_repo`; the
Sparky_Rocky sparrowfile archives local dirs instead of git-cloning (`sparrowfile:174`).
**Chosen:** B; item 9a's real suite will use the git-URL path in `cinnamon-for-rocky10` itself.

**Problem: trigger the test build**
**Option A — write a trigger file directly into `~/.sparky/projects/sparky-rocky/.triggers/`.**
Cons: bypasses the auth path.
**Option B — web API: login (admin/admin) then `POST /build-with-tags`.** Pros: exercises exactly
what the UI does, including cookie auth and tag encoding.
**Chosen:** B.

**Changes** (host state; nothing in any git repo under management, except the new local
`~/Code/sparky-noop` repo commit `850bb2a`)

| Path | What changed |
|---|---|
| `/etc/sudoers.d/sparky` | new drop-in, 0440 root:root, NOPASSWD `mount`/`umount` for `howard` |
| `~/bin/qemu-kvm` | new symlink to `/usr/libexec/qemu-kvm` |
| `~/.bash_profile` | untouched by me; line 9 (raku PATH) added by the interrupted session, left as-is |
| `/etc/yum.repos.d/nxadm-pkgs-rakudo-pkg.repo` + `rakudo-pkg` | pre-existing from the interrupted session (2026-08-22), verified working, left as-is |
| `~/.raku/` | zef 1.1.3 and all Sparky/cro/DBIish/Sparrow modules (home install); bin scripts for sparkyd, sparrowdo, sparman, sparky-runner, sparky-web.raku |
| `~/.zef/store/` | module store populated (was empty) |
| `~/Code/sparky/` | pre-existing clone, in sync at `add1b02` (0.2.32); new `sparkyd.log`, `cro-run.log` |
| `~/Code/Sparky_Rocky/` | pre-existing clone at `57decf1`, unchanged |
| `~/Code/sparky-noop/` | new local git repo (commit `850bb2a`), the no-op scaffold |
| `~/.sparky/` | new: `projects/sparky-rocky/` (from sync_project.sh), `templates/vars.yaml` (machine, ssh key, no-op repo edits), `db.sqlite3`, `.reports/`, `work/` |
| `~/sparky.yaml` | new: `SPARKY_API_TOKEN` (local random, value not recorded here) |
| `~/rocky-linux-distro/default/` | new: `distro.Rocky-10-GenericCloud.qcow2` (545MB cache, reused on re-runs), `distro.qcow2` working copy, `.version` |
| tmux sessions `sparkyd`, `cro-run` | new: the two running services |

**Checks run**

- `bash -lc 'which raku rakudo zef'` + versions: PASS (evidence step 3)
- four `zef install` steps: 4/4 rc=0, all module tests OK (log `/tmp/opencode/sparky-zef-install.log`)
- `raku db-init.raku`: rc=0
- `zef install Sparky::JobApi`: "All candidates are currently installed"
- `sudo visudo -c -f /etc/sudoers.d/sparky`: "parsed OK"; `sudo -n mount --version`: PASS
- `qemu-kvm --version` / `-machine help`: 10.1.0 / `pc-q35-rhel10.2.0`
- `ss -ltn | grep :4000`: LISTEN
- `curl -sS localhost:4000`: web UI served
- `sqlite3` builds query: 3/3 state=1 (ok)
- report files `build-1.txt`, `build-2.txt`, `build-3.txt`: evidence quoted above

**Competing priorities and leftover state (explicit)**

- Firewall rule recorded as N/A rather than enabling firewalld; a system-wide default-deny switch
  was not worth it for an already-reachable localhost service, and it risked unrelated services.
- Reused the interrupted session's artifacts (rakudo-pkg install, both clones) instead of a clean
  rebuild; they were verified healthy, and the deviation is recorded above.
- `qemu_shut=True` on the no-op run to free the 6GB VM after the test. Note for item 10 (`Big`):
  the cached `distro.Rocky-10-GenericCloud.qcow2` now has the Sparrow client and pre-tasks baked
  in, and `~/.sparky/work/*/...` plus `~/rocky-linux-distro/default/.version` will suppress
  re-bootstrap for the same version. Fresh-image-per-scenario isolation (a DoD requirement) needs
  the `bootstrap` flag, distinct `prefix` values, or re-seeding per the plan's `sparky/seed-image.sh`
  design.
- Orphaned paused QEMU process `cinnamon-inspect-vm` (pid 216968, ~1.5GB RSS, running since
  2026-08-22; `virsh list --all` shows no domain, so the domain record is gone while the process
  survived). This matches the `## Status` incident note ("domain gone by 12:45 JST Aug 22, disk
  kept"). Left as-is: it is `Big`'s artifact, paused (no CPU), holds no port (its networking was the
  libvirt bridge, not hostfwd), and killing it is outside item 1. Flagged for cleanup.
- Item 9a should move this subsection's setup notes into `sparky/README.md` per the plan, and the
  AGENTS.md section 7 Raku line needs the user's update (dead URL).

**Re-verification (Tails, 2026-08-24 09:22 to 09:48 JST)**

Re-dispatched to execute item 1. The subsection above was written by an earlier Tails session
(execution window 00:30 to 01:26 JST the same day). Before redoing anything, I verified all four
acceptance criteria against live host state, then re-ran the no-op end-to-end check fresh. All
four criteria currently hold; no repair work was required.

**Acceptance criteria (live re-check)**

| Criterion | Status | Evidence |
|---|---|---|
| `curl -sS localhost:4000` serves the web UI | MET | `curl -sS -i localhost:4000` -> `HTTP/1.1 303 See Other`, `Location: /builds_latest`; `curl -sS -L localhost:4000` -> HTTP 200, `<title>~SPARKY CI WEB~ \| latest builds</title>` |
| Both services running | MET | `tmux ls` -> sessions `sparkyd` and `cro-run`, both created Aug 24 00:45:19 JST; `ss -ltnp` -> `LISTEN 0.0.0.0:4000` held by pid 283564 `/opt/rakudo-pkg/bin/raku -Ilib bin/sparky-web.raku` (child of `rakudo ~/.raku/bin/cro.raku run`, pid 283539); sparkyd is pid 283538 `rakudo ~/.raku/bin/sparkyd.raku`, etime 08:38:55 (`ps -eo pid,etime,cmd`); error scan `grep -icE 'error\|panic\|exception\|died'` -> 0 matches in `sparkyd.log` (7689 lines) and `cro-run.log` (1 line) |
| No-op scaffold runs end-to-end to "succeed" | MET | Re-ran fresh at 09:44:26 JST. `curl -c cj -d 'login=admin&password=admin' localhost:4000/default_login` -> 303, `Location: /?message=user [admin] logged in`; `curl -b cj --data-urlencode 'tags=...' localhost:4000/build-with-tags/project/sparky-rocky` (identical tags to the 01:20 run) -> 200, trigger id `ucyhfxtwnmgdkpzlorqb.283564`; by 09:48:03 JST `sqlite3 ~/.sparky/projects/db.sqlite3 "SELECT id,project,job_id,state FROM builds WHERE id>3"` -> rows 4/5/6 (`sparky-rocky`, `qemu-session.default`, `test-use-case.default`) all `state=1`; state mapping `1=ok, 0=run, -1=fail, -11=terminated` per `~/Code/sparky/templates/builds_latest.crotmp:106-124`; in-VM evidence: `build-5.txt:1489-1490` `# qemu should reach login prompt` -> `True`, `build-6.txt:190-193` `load scenario from main.raku` -> `[task run: task.bash - tasks/check-noop]` -> `no-op task ran OK`, `build-4.txt` tail `stop-qemu-box` killed pid 295795 -> `done`; `pgrep -af rocky-linux-distro` -> empty (QEMU shut per `qemu_shut=True`); wall time 09:44:26 to 09:46:45 JST; no image download (0 `download distro` lines in `build-5.txt`, cached qcow2 reused) |
| Setup notes written to `## Implementation` | MET | the earlier session's notes above; this block adds the live re-check and the fresh run |

**Live state checks (command -> result, 09:22 to 09:31 JST)**

1. `bash -lc 'which raku rakudo zef; raku -v | head -1; zef --version'` -> `/opt/rakudo-pkg/bin/raku`,
   `/opt/rakudo-pkg/bin/rakudo`, `/home/howard/.raku/bin/zef`; `Welcome to Rakudo v2026.07.`; `1.1.3`.
2. `bash -lc 'zef list'` -> store contains Sparky 0.2.32, Sparky-Job-Api 0.0.13, Sparrow6 0.0.93,
   Sparrowdo 0.1.55, Cro::Core 0.8.10, Cro::HTTP 0.8.13, Cro::TLS 0.8.10, Cro::WebApp 0.10.1,
   Cro::WebSocket 0.8.10, DBIish 0.6.8, DBIish::Pool 1.1.0 (plus older cached versions).
3. `grep -n rakudo ~/.bash_profile` -> line 9, the raku PATH export.
4. `rpm -q rakudo-pkg` -> `rakudo-pkg-2026.7.0-01.x86_64`; `/etc/yum.repos.d/nxadm-pkgs-rakudo-pkg.repo` present.
5. `git -C ~/Code/sparky status -sb` + `git log --oneline -1` -> `## master...origin/master`, HEAD `add1b02`;
   `git -C ~/Code/Sparky_Rocky log --oneline -1` -> `57decf1`; `git -C ~/Code/sparky-noop log --oneline -1` -> `850bb2a`.
6. `ls -la ~/.sparky/` -> `projects/{db.sqlite3,sparky-rocky,qemu-session.default,test-use-case.default,.reports,work}`,
   `templates/vars.yaml`; `~/sparky.yaml` present (34 B).
7. `cat ~/.sparky/templates/vars.yaml` -> `use_case_repo` includes `~/Code/sparky-noop`;
   `qemu.binary: qemu-kvm`; `qemu.machine: "pc-q35-rhel10.2.0"`; `ssh_key_path: ~/.ssh/id_ed25519.pub`.
8. `bash -lc 'qemu-kvm --version | head -1'` -> `QEMU emulator version 10.1.0 (qemu-kvm-10.1.0-16.el10_2.2)`;
   `-machine help` -> `pc-q35-rhel10.2.0` (alias `q35`); `~/bin/qemu-kvm` is a symlink to `/usr/libexec/qemu-kvm`.
9. `sudo ls -la /etc/sudoers.d/sparky` -> 0440 root:root, content `howard ALL=(ALL) NOPASSWD: /usr/bin/mount,/usr/bin/umount`;
   `sudo visudo -c -f /etc/sudoers.d/sparky` -> "parsed OK"; `sudo -n mount --version` -> `mount from util-linux 2.40.2` (passwordless).
10. `systemctl is-active firewalld` -> `inactive` (port-4000 rule remains N/A, as recorded above).
11. `sqlite3 ~/.sparky/projects/db.sqlite3 "SELECT id,project,job_id,state,dt FROM builds ORDER BY id"` -> rows 1-3 all
    `state=1`; row 1 `job_id` `kvtmfqgjopawhnudicbr.283564` matches the trigger id recorded above
    (dt `2026-08-23 16:20:39` UTC = 01:20:39 JST).
12. `ls -la ~/rocky-linux-distro/default/` -> `distro.Rocky-10-GenericCloud.qcow2` (544997376 B, mtime May 26 09:21),
    `distro.qcow2` (905314304 B, Aug 24 01:25), `.version` (Aug 24 01:21).

**Resolved discrepancy (image cache mtime).** `distro.Rocky-10-GenericCloud.qcow2` carries mtime
May 26 09:21, which looks older than the 01:24 JST download recorded above; it is not a
pre-existing cache. `build-2.txt:30-34` shows the download ran 01:21:32 to 01:24:09 and the
`.cache` file was moved into place at 01:24:09; the mtime is the upstream image's Last-Modified,
preserved by the downloader. (The same lines give 544997376 B in 157 s, a 3.5 MB/s average; the
earlier "~4.2MB/s" figure was an estimate, the log timestamps are the evidence.)

**Carried-forward flags (unchanged by this re-check)**

- The orphaned paused `cinnamon-inspect-vm` QEMU pid 216968 is still present (RSS 1528796 KB,
  STAT `Sl`, elapsed 2d 02:39; `virsh list --all` shows no domain), matching the `## Status`
  incident note. Still Big's artifact, still flagged for cleanup; not touched here.
- Host headroom at re-run time: `free -g` -> 30 GB total, 19 GB available; the re-run VM used
  6024 MB (qemu command line in `build-5.txt`); the A7 one-VM-at-a-time constraint held.
- The web-login cookie jar was removed after the run; no credentials persisted anywhere.

**Verdict:** item 1 remains MET as of 2026-08-24 09:48 JST; no repair work was required. No files
in `metalllinux/cinnamon-for-rocky10` were touched. Next per `## Next Actions`: item 3 (Big,
static inspection). I updated the item-1 clause in `## Next Actions` accordingly (last-writer
convention for that section).

### Item 2

*In progress since 2026-08-25 11:45 JST (attempt 4). Orphan VM `gdm-login-vm`
adopted per the resume brief: no new VM created, orphan QEMU process PID 324361 not touched.
Checkpoints land here as the run proceeds; the VM is the durable state.*

**Prior state of the adopted VM (verified, not assumed)**

- Host: QEMU PID 324361 alive, `Sl`, RSS 2759848 KB, elapsed 11:43:48 at first check
  (`ps -p 324361 -o pid,stat,etime,rss,cmd`); command line confirms `-vnc 127.0.0.1:0`
  (VNC :0 = 127.0.0.1:5900), disk `/var/lib/libvirt/images/cinnamon-test/gdm-login-vm.qcow2`,
  4GB, 2 vCPU. `virsh list --all` shows no domain: the VM is outside libvirt control.
- Guest reachable: `ssh -i ~/.ssh/cinnamon-test-key root@192.168.122.29` OK;
  `date` -> `Tue Aug 25 02:42:00 AM UTC 2026`; `uptime` -> up 11:00, load 0.00.
- `id gdmtest` -> `uid=1000(gdmtest) gid=1000(gdmtest) groups=1000(gdmtest)`.
- `getenforce` -> `Permissive`; `/etc/selinux/config` -> `SELINUX=permissive`,
  `SELINUXTYPE=targeted`.
- `rpm -q gdm gnome-shell` -> `gdm-47.0-22.el10_2.x86_64`,
  `gnome-shell-49.4-8.el10_2.rocky.0.2.x86_64`; `systemctl is-enabled gdm` -> `enabled`;
  `systemctl is-active gdm` -> `active`.
- `/root/gdm-harness/` (attempt 3 artifacts): `gdm-a11y.py` (7020 B, 15:51), `gdm-drive.sh`
  (13682 B, 15:51), `ukey.c` (13648 B, 16:21), `ukey` built binary (17816 B, 16:21).
  `/root/gdmtest.pass` present (25 B, mode 600; value not recorded here).
- `/tmp/` attempt-3 experiment artifacts: `holddev{,2,3}` (+ `.c` sources, uinput device
  lifetime probes), `xlisten` (ELF, links `libX11` only; event listener), `xtest-test`
  (ELF, links `libXtst`; uses `XTestFakeButtonEvent`/`XTestFakeMotionEvent`/
  `XTestQueryExtension` per `strings`). All superseded by the uinput design (below);
  left in place, disposable.
- Greeter live at check time: `loginctl list-sessions --no-legend` -> session `c1`,
  uid 42 (`gdm`), seat0, tty1, CLASS `greeter`, STATE idle, since 8h ago; process tree
  `/usr/sbin/gdm` (1015) -> `gdm-session-worker [pam/gdm-launch-environment]` (1021) ->
  `/usr/libexec/gdm-wayland-session ... gnome-session --autostart
  /usr/share/gdm/greeter/autostart` (1173) -> `/usr/bin/gnome-shell` (1462) +
  `/usr/bin/Xwayland :1024 -rootless` (2100).
- Cinnamon **not** installed yet: `rpm -q cinnamon cinnamon-session nemo` -> all "not
  installed"; `/usr/share/xsessions/` empty; `/usr/share/wayland-sessions/` has only
  `gnome.desktop`, `gnome-wayland.desktop`.

**Design claims of the attempt-3 harness, independently verified (this session)**

The attempt-3 design pivots from the plan's X11 greeter + `xdotool`/XTest to a Wayland
greeter driven by a uinput keyboard/pointer (`ukey`) + AT-SPI2 state reader
(`gdm-a11y.py`). I verified every load-bearing claim rather than trusting the comments:

1. No X server installable from the EL10 repos (in the VM):
   `dnf list available "xorg-x11-server*"` -> `Error: No matching Packages to list`.
2. No X server on the 10.2 DVD (host, ISO mounted at `/tmp/opencode/dvd`): the only
   `xorg-x11-server*` RPM under `AppStream/Packages/x/` or `BaseOS/Packages/x/` is
   `xorg-x11-server-Xwayland-24.1.9-4.el10_2.x86_64.rpm`; no `xorg-x11-server-Xorg`.
   (EPEL 10 check for the same package still pending at this checkpoint; item 3 F9
   already established EPEL 10 lacks xdotool/ydotool/dogtail/lightdm.)
3. gdm-47 is Wayland-only (in the VM): `rpm -ql gdm | grep '^/usr/libexec/'` ->
   `gdm-auth-config-redhat`, `gdm-new-session`, `gdm-runtime-config`,
   `gdm-session-worker`, `gdm-wayland-session`. No `gdm-x-session`.

Consequence (matches attempt 3's finding, now evidence-backed): the greeter is
gnome-shell/mutter on Wayland; the plan's `WaylandEnable=false` X11-greeter baseline
(`## Plan`, VM reproduction design) is infeasible on EL10; input must come from
display-server-agnostic sources (uinput), and greeter UI state from AT-SPI2. This is a
supersession of the plan's XAUTHORITY/xdotool steps, not a deviation: the plan's risk R1
fallback ladder and A8 anticipated it, and item 3 F9 removed the off-the-shelf rungs.

**Orphan-VM constraint (affects the harness run, recorded now)**

Because the libvirt domain record is gone, `virsh` cannot reach this VM: `--attach` in
`vm-test/test-gdm-login.sh` (which calls `virsh domstate`), `host_shot` (`virsh
screenshot`), `reboot_and_wait` (`virsh reboot`), and the VNC-display lookup are all
unavailable. For this run I drive the phases over SSH (the in-VM scripts are
self-contained) and capture pixel evidence with a minimal RFB framebuffer grabber
against 127.0.0.1:5900 (to be added to `tasks/lib/` as host-side tooling). A reboot, if
needed, goes through `ssh ... reboot` with IP re-polling. This deviation is specific to
the adopted orphan VM; a fresh libvirt VM (items 4, 5, 7c) uses the harness unchanged.

**Run state at this checkpoint:** prior state verified; no VM modification yet made in
this session. Next: EPEL check, a11y-bus smoke test, ukey input smoke test, then the
phase sequence (GNOME control login -> INSTALL.md install -> Cinnamon attempt) with
evidence.

### Item 2 — attempt 5 (2026-08-26, dispatched ~14:20 UTC, Q4 endpoint)

*Resumed after the EVO-X2 reboot of 2026-08-26 ~12:25 UTC (record: TASK-0010 `## Status`).
Deviation from the attempt-4 resume brief, per `## Status`: the orphan `gdm-login-vm` is
dead (`virsh list --all` empty at 14:21 UTC this session), so a **new** VM is provisioned
per the plan instead of adopting the orphan.*

**Wedge monitoring (per dispatch):** baseline count **0** at 14:22 UTC (`ssh
howard@192.168.1.106 'journalctl -k --no-pager | grep -cE "device wedged"'`; EVO-X2
uptime 1:57, matching TASK-0010 "zero wedges since boot"). Re-checked before teardown;
if the count rises, checkpoint here and stop.

**Orphan leftover state:** the disk `/var/lib/libvirt/images/cinnamon-test/gdm-login-vm.qcow2`
(2.3G) survived the host reboot. No state is needed from it: the repo working tree is the
superset of its `/root/gdm-harness/` (repo `gdm-a11y.py` 10356 B / `gdm-drive.sh` 16050 B /
`ukey.c` 13716 B vs VM 7020 / 13682 / 13648 B, plus repo-only `vnc-grab.py` and the
`--attach --ip` orphan mode in `test-gdm-login.sh`). `provision-vm.sh:163`
(`cp "$CLOUD_IMAGE" "$DISK_PATH"`) overwrites it when the new VM provisions under the same
name, so no stale-state risk; the file is the new VM's disk after the run.

**Working-tree checkpoint (verified, not assumed, 14:25 UTC):**

- Branch `task-0008-gdm-auth` at `1f00da5` = `origin/main`; `git status -sb`: modified
  `vm-test/lib.sh`, `vm-test/provision-vm.sh`; untracked `tasks/`,
  `vm-test/test-gdm-login.sh`, `vm-test/test-repo-setup.sh`. Matches the brief.
- Syntax checks all clean (14:25 UTC): `bash -n` on `test-gdm-login.sh`, `gdm-drive.sh`,
  `test-repo-setup.sh`, `provision-vm.sh`, `lib.sh`; `python3 -m py_compile` on
  `gdm-a11y.py` + `vnc-grab.py`; `gcc -fsyntax-only -Wall -Wextra` on `ukey.c`.
- `tasks/lib/__pycache__/` (bytecode from the py_compile check) is excluded from the
  commit; `__pycache__/` added to `.gitignore`.
- `vm-test/test-repo-setup.sh` (TASK-0006-era harness) is committed per the brief; Big
  had flagged it in item 3 as "not mine; left as-is; flagged for Tails/Knuckles".

**Harness contents at this checkpoint (the committed working tree):**

- `vm-test/test-gdm-login.sh` (665 lines): 9-phase orchestrator. (1) provision with
  `--graphics vnc`; (2) scp harness files to `/root/gdm-harness/`; (3) baseline:
  deterministic SELinux mode (`--selinux`, default permissive per the plan's base
  reproduction) + `dnf install gdm gnome-shell` + ephemeral `gdmtest` user with a random
  hex password generated inside the VM + ukey build; (4) reboot into
  `graphical.target`, wait for the greeter session + a11y UI; (5) **GNOME control login**
  (state-based verdict, then logout to the greeter); (6) INSTALL.md install exactly
  (`setup-repo.sh` + the two `dnf install` commands + `ldconfig`); (7) optional
  `--reboot-after-install` (item 5 experiment B) / `--daemon-reload-after-install`
  (experiment C); (8) **Cinnamon login attempt**, reported as `VERDICT` (not FAIL) so the
  result under test cannot abort the harness before evidence capture; (9) collect
  `/root/evidence` to `vm-test/results/gdm-login-<TS>/` (gitignored); teardown via
  `--destroy-only` unless `--keep-vm`. Verdicts are state-based (`loginctl` session type
  x11/wayland + desktop process), pixel evidence is best-effort `virsh screenshot`.
- `tasks/lib/gdm-drive.sh` (438 lines): in-VM driver library. ukey build (gcc +
  kernel-headers); logind session-state helpers (the `loginctl list-sessions` column
  layout verified on EL10 / systemd 257 in the attempt-4 observation pass); greeter
  wait with the dual-mode UI (face list with "Not listed?" vs username dialog with
  "Log In", attempt-4 finding); login drive (click the user's face, or "Not listed?" +
  type username + Return; wait for the "Login code:" label; for Cinnamon, Ctrl+Alt+Down
  session select with the entry found by name in the a11y tree and ukey-clicked at its
  screen extents; type password; Return); `gdm_wait_session` verdict;
  `gdm_capture_evidence` (the plan's step-5 set: `journalctl -u gdm --since t0`,
  `journalctl _UID=<uid> --since t0`, `tail -n 200 /var/log/secure`, `loginctl`
  session state, `getenforce`, session entries, a11y tree + text).
- `tasks/lib/ukey.c` (429 lines): uinput keyboard + relative-pointer micro-driver
  (`type` / `key` / `combo` / `move` / `click`), built in the VM.
- `tasks/lib/gdm-a11y.py` (326 lines): AT-SPI2 reader (`tree` / `text` / `has` /
  `wait` / `find` / `waitvis` / `textof`), `waitvis`/`find` print screen-space extents
  for ukey clicks.
- `tasks/lib/vnc-grab.py` (185 lines): host-side RFB framebuffer grabber, the attempt-4
  orphan-mode observation channel. Not needed for a libvirt-domain run (`virsh
  screenshot` covers pixels); committed for the orphan path and item 9a.
- `vm-test/provision-vm.sh` + `vm-test/lib.sh`: item-2 diffs per the working tree
  (`--graphics <type>`, `--destroy-only`, `--name`, `VM_NAME` env override in lib.sh).

**Run plan (attempt 5):**

1. Commit the working tree to `task-0008-gdm-auth` and push the branch (checkpoint).
2. `bash vm-test/test-gdm-login.sh` with defaults (name `gdm-login-vm`, SELinux
   permissive, no post-install mode): phases 1-6 + 8 + 9 = the item 2 acceptance run.
   Item 5's experiments B/C run later on fresh VMs with the `--*` flags.
3. Phase results + evidence paths checkpointed here as they land.
4. Final `### Item 2` text: alternatives, changes table, checks run, verdict.

**Next:** commit + push, then the harness run.

### Item 2 — attempt 7 (item 2a: recover + inventory the orphan VM, 2026-08-27, Q4 endpoint)

*Single-deliverable dispatch 2a per `## Next Actions` (2026-08-26 19:30 UTC). The dispatch
premise "domain definition gone" is **wrong** — see the premise check below. No QEMU process
and no guest state was touched; the only state change made is one protective libvirt flag
(autostart).*

**Premise check — contradicts `## Status` (2026-08-26 19:30 UTC, "the domain definition was
removed"):** the domain is fully registered and libvirt-managed. There was nothing to
re-register; no `virsh define` was run. Evidence (2026-08-27 04:40 JST = 19:40 UTC):

- `sudo virsh list --all` -> `3  gdm-login-vm  running`
- `sudo virsh dominfo gdm-login-vm` -> `State: running`, `Persistent: yes`, `Autostart:
  disable` (at check time), UUID `671de411-6a1f-4885-a112-7a4db95a1288` (equals the QEMU
  cmdline `-uuid` of PID 390197)
- `sudo virsh qemu-monitor-command gdm-login-vm --cmd '{"execute":"query-status"}'` ->
  `{"return":{"status":"running","running":true},"id":"libvirt-27"}` (live QMP path through
  the libvirt QEMU driver)
- Persistent XML present: `sudo ls /etc/libvirt/qemu/` -> `gdm-login-vm.xml`
- Registration is continuous, not re-established: the libvirt QEMU driver
  (`virtqemud`, PID 307826; this host uses the RHEL 10 split-daemon layout, no monolithic
  `libvirtd`) has run unbroken since 2026-08-24 05:58 UTC (`systemctl show virtqemud`), which
  brackets the domain's creation at 14:51 UTC.

The "orphan" label is inherited from the Aug 25 incident (record: Status) and does not apply
to this VM. The 16:50 UTC Status entry ("Not reached: VM provisioning, `virsh list --all`
empty") and the 19:30 UTC entry disagree with the observed state; how those checks came back
empty is unverified, surfaced per AGENTS.md section 5. Related: the 12:50 UTC entry's "the
orphan `gdm-login-vm` did not survive the reboot" cannot be the runner's reboot — the runner
(192.168.1.102) has been up since 2026-08-15 14:10 JST (`uptime -s`), so the 2026-08-26
~12:25 UTC reboot was EVO-X2 only. The old orphan (PID 324361, alive at 2026-08-25 05:54 UTC)
was gone before the new VM's 14:51 UTC provisioning; how it died is unverified.

**SSH verified:** `ssh -i ~/.ssh/cinnamon-test-key root@192.168.122.15` -> OK. Guest:
`localhost.localdomain`, Rocky Linux 10.2, kernel `6.12.0-211.16.1.el10_2.0.1`, `up 4:27` at
19:45 UTC (boot 15:18 UTC per `last reboot`). 192.168.122.15 confirmed by `ip neigh show dev
virbr0` (52:54:00:a0:8b:34 REACHABLE; MAC equals the QEMU cmdline `mac`).

**Protective change (the only state change made):** `sudo virsh autostart gdm-login-vm` ->
"Domain 'gdm-login-vm' marked as autostarted"; `dominfo` now `Autostart: enable` (was
disable). Reason: this VM holds the only copy of the attempts 5/6 guest-side state that 2b/2c
need, and the prior VM was lost when its host-side state died. Non-destructive to the running
QEMU (affects the next libvirt start only). Revert: `sudo virsh autostart --disable
gdm-login-vm`.

**Guest inventory (all via ssh, 19:40-19:50 UTC):**

- **Cinnamon packages: zero** (`rpm -qa | grep -c cinnamon` -> 0; 804 packages total).
  Harness phase-3 baseline present: `gdm-47.0-22.el10_2`,
  `gnome-shell-49.4-8.el10_2.rocky.0.2`. `dnf history list`: tx#3 `install -y gdm gnome-shell`
  (351 pkgs) and tx#4 `install -y gcc kernel-headers` (9 pkgs), both 14:52 UTC; no dnf
  activity since. The INSTALL.md Cinnamon install (harness phase 6) was **never executed**:
  `dnf repolist` shows only Rocky baseos/appstream/extras, no file:// repo. This is what 2b
  must do.
- Users: `gdmtest` (uid 1000); password file `/root/gdmtest.pass` (25 B, the harness random
  hex). No other non-system users.
- SELinux: `getenforce` -> `Permissive`; `SELINUX=permissive` in `/etc/selinux/config`
  (harness sets this deterministically).
- GDM: `systemctl is-enabled/is-active gdm` -> enabled/active. Greeter session `c1` on
  `seat0`/`tty1`, Type=**wayland**, online; `gdmtest` in the face list, "Login code:" prompt
  present (the dual-mode UI). `/var/log/secure`: **zero** `gdm-password` lines — no GUI
  password login has ever been attempted. Phase 5 (GNOME control login) never completed: its
  15:21 UTC evidence (`/root/evidence/gnome-control/`) still shows the greeter a11y tree and
  `journal-uid.log` = `-- No entries --` (no uid-1000 session ever).
- Harness at `/root/gdm-harness/`: `gdm-a11y.py` (10356 B), `gdm-drive.sh` (16050 B),
  `ukey.c` (13716 B) — **md5-identical** to the committed repo files at `b15dfcb`
  (`a2961c22...`, `2c662a40...`, `c14f531b...` on both sides) — plus built `ukey` binary
  (17816 B, 14:52 UTC) and attempt-5 scratch `state-dump.py` (609 B, 16:03 UTC; not in repo).
- Evidence at `/root/evidence/`: `baseline-{dnf,driverdeps,packages,repos}.log` (15:17),
  `greeter-ui-{text,tree}.log` (15:18), `gnome-control/` (15:18-15:21: a11y trees, loginctl,
  secure tail, getenforce=Permissive, sessions-available).
- Resources: `/dev/vda4` 2.2G used of 8.4G (6.2G free); 4GB RAM, ~2G available.

**Finding for 2c (recorded, not fixed): the greeter is Wayland-only; no X server is
installed.** `rpm -q xorg-x11-server-Xorg` -> not installed; `/usr/share/xsessions/` empty;
available sessions are `gnome.desktop` + `gnome-wayland.desktop` (wayland-sessions dir only);
greeter Type=wayland. The committed harness selects the session with Ctrl+Alt+Down
(`tasks/lib/gdm-drive.sh`), X11 GDM behavior. 2c must either install `xorg-x11-server-Xorg`
and set `WaylandEnable=false` in `/etc/gdm/custom.conf` before the Cinnamon login attempt, or
extend the driver for the Wayland greeter's session menu. Decision belongs to 2c.

**Landmine for 2c:** `vm-test/provision-vm.sh:163` does `cp "$CLOUD_IMAGE" "$DISK_PATH"`.
Provisioning a new VM under the same name `gdm-login-vm` would overwrite this disk in place
while QEMU holds it open (the guest state above destroyed). Any 2c harness run must use a
different `--name`/`VM_NAME`, or destroy this domain first — and 2b must run before any
destroy.

**State left as found:** VM running under libvirt (`sudo virsh list`: Id 3 running), ssh
working, autostart enabled (the single change above), guest sitting at the GDM greeter with
`gdmtest` in the face list. Nothing killed, no guest modification.

**Next (2b):** install the Cinnamon RPMs inside (local repo + the INSTALL.md dnf commands),
then 2c decides the Wayland/X11 question and runs the login attempt.

---

### Item 2 — attempt 8 (item 2b: install the Cinnamon RPMs, 2026-08-27, Q4 endpoint)

*Single-deliverable dispatch 2b per `## Next Actions` (2026-08-26 19:30 UTC). The VM was not
destroyed, re-provisioned, or rebooted. No GDM restart and no greeter session configuration
change (the Wayland/Xorg decision stays in 2c's scope). All guest commands ran over ssh
(root, `~/.ssh/cinnamon-test-key`) at 192.168.122.15. Times below are guest-local (UTC) with
JST in parentheses; the guest clock is UTC (boot 15:18 UTC + uptime 5:44 at 21:02).*

**Pre-check (21:02 UTC / 06:02 JST): state matches the attempt 7 inventory exactly.**
`rpm -qa | grep -c cinnamon` -> 0; `dnf repolist` -> appstream/baseos/extras only (no file://
repo); `/root/` holds only `evidence/`, `gdm-harness/`, `gdmtest.pass`; `/dev/vda4` 6.2G free;
uptime 5h44m (boot 15:18 UTC, unchanged).

**Host-side metadata check (why no `createrepo_c` re-run on the host):** the host
`~/Linux/projects/cinnamon-for-rocky10/rpms/` already contains valid `repodata/` (generated
2026-08-14 07:54 JST, after the newest RPM mtime 2026-08-13 19:34). `primary.xml` lists all
48 package names on disk (per-RPM `rpm -qp --qf '%{NAME}'` vs metadata names, `diff` rc=0).
The "49 RPMs" from the first `ls | wc -l` was 48 RPMs + the `repodata` directory
(`ls -1 *.rpm | wc -l` -> 48). Metadata is current; no regeneration needed.

**Procedure — harness phase 6 verbatim (test-gdm-login.sh:510-543 = INSTALL.md quick start):**

1. `scp -r rpms/ repo-setup/ root@192.168.122.15:/root/` (test-gdm-login.sh:513-516). Verified
   on the guest: 48 RPMs, 213M; md5 of `cinnamon-6.7.4-1.el10.x86_64.rpm`
   (`717b4d6c...`) and `mozjs115-115.29.0-1.el10.x86_64.rpm` (`c6118e02...`) match host.
2. `bash /root/repo-setup/setup-repo.sh /root` (test-gdm-login.sh:526) -> rc=0 (log
   `/root/evidence/install-setup-repo.log`): installed createrepo_c 1.1.2-4.el10 (dnf tx#5,
   2 pkgs), reused the existing repodata (generation skipped), wrote
   `/etc/yum.repos.d/cinnamon-rocky10.repo` with `baseurl=file:///root/rpms`, enabled CRB,
   `dnf makecache` OK. `dnf repolist` then lists `cinnamon-rocky10`; `dnf list available
   --repo cinnamon-rocky10` serves the local packages.
3. `dnf install -y cinnamon` (test-gdm-login.sh:528) -> rc=0, "Complete!", zero
   error/failed/nothing-provides lines (log `/root/evidence/install-cinnamon.log`, dnf tx#6).
   9 packages: cinnamon 6.7.4, cinnamon-desktop 6.7.2, cinnamon-menus 6.7.0, cjs 6.4.0,
   mozjs115 115.29.0, muffin 6.7.4-3, muffin-clutter 6.7.4-3, muffin-cogl 6.7.4-3,
   xapps-lib 3.3.3 (exactly the 8 hard deps in INSTALL.md + cinnamon).
4. `dnf install -y cinnamon-session cinnamon-settings-daemon cinnamon-control-center nemo
   mozjs115-devel` (test-gdm-login.sh:530-532) -> rc=0, "Complete!", zero error lines (log
   `/root/evidence/install-core.log`, dnf tx#7). 5 packages.
5. `ldconfig` -> rc=0 (log `/root/evidence/install-ldconfig.log`).

**Verification (21:11-21:18 UTC / 06:11-06:18 JST):**

- `rpm -q cinnamon cinnamon-session nemo` -> all present; `/usr/share/xsessions/cinnamon.desktop`
  present, 152 B (log `/root/evidence/install-versions.log`). Cinnamon-family total: 14
  packages (`rpm -qa | grep -cE 'cinnamon|cjs|muffin|mozjs115|nemo|xapps'` -> 14), exactly the
  INSTALL.md "Installed packages" table set; no debuginfo/debugsource installed.
- ldd sweep: 43 binaries in `/usr/bin` matching `cinnamon|cjs|muffin|nemo` + 6 shared
  libraries -> **0 "not found" lines total**. The ELF binaries that actually link resolve
  fully: `cinnamon` (133 libs), `cjs` (44), `muffin` (108), `nemo` (73); the remaining 39
  entries are scripts (0 libs, expected).
- The INSTALL.md troubleshooting check (`ldd /usr/lib64/libcinnamon-desktop.so.4 | grep
  "not found"`) -> 0 lines.
- ld cache (`ldconfig -p`): libcjs.so.0, libmuffin.so.0, libcinnamon-desktop.so.4,
  libcinnamon-menu-3.so.0, libcinnamon-control-center.so.1, libxapp.so.1, all under /lib64.
- The `/usr/lib64/muffin/` subdirectory (libmuffin-clutter-0.so.0, libmuffin-cogl-0.so.0,
  -cogl-pango, -cogl-path) is **not** in the ld cache (no `/etc/ld.so.conf.d/` entry). Those
  libs resolve via RPATH baked into the binaries: `objdump -p /usr/bin/cinnamon` ->
  `RPATH /usr/lib64/muffin:/usr/lib64/cinnamon`; `libmuffin.so.0` and the `muffin/` libs
  carry `RPATH /usr/lib64/muffin`. `ldd /usr/bin/cinnamon` maps all four `muffin/` libs to
  their real paths. Package design choice, not a defect; ldd (which honors RPATH) reports
  everything resolved.

**VM state (unchanged, per the dispatch constraint):** `systemctl is-active gdm` -> active;
greeter session c1 on seat0/tty1 (Type=wayland) elapsed 4h39m at check time — not restarted,
not disturbed. `dnf history list` shows tx#5-7 = this attempt's three transactions (21:09-21:11
UTC). VM left running under libvirt, ssh working, load 0.

**Not done (2c scope):** no greeter session configuration touched; no `systemctl restart gdm`
(harness phase 6 contains no GDM restart — restart/reboot are phase 7 experiments,
test-gdm-login.sh:545-574). The session file `/usr/share/xsessions/cinnamon.desktop` now
exists for 2c's session selection. The `provision-vm.sh:163` disk-clobber landmine (record:
attempt 7) stands: any 2c harness run needs a different `--name` or a destroy first.

**Next:** 2c — decide the Wayland/Xorg question (attempt 7 finding: greeter is Wayland-only,
the committed harness drives X11 GDM with Ctrl+Alt+Down), then run the login attempt.

---

### Item 2 — 2c-1 (item 2c-1: Xorg install + GDM X11 switch, 2026-08-27, Q4 endpoint)

*Single-deliverable dispatch 2c-1 per `## Next Actions` (2026-08-27 11:10 UTC). **The
deliverable as specified is not achievable on Rocky 10.2: RHEL 10 does not ship the Xorg
X server** (no binary package, no driver packages, no source RPM, and the installed GDM
47 has no X session launcher). Blocker recorded first, per the dispatch brief. **No state
change was left in the guest** (no config edit, no GDM restart, no re-provisioning; the one
file created, a backup, was verified byte-identical and deleted). Guest left running at the
Wayland greeter, exactly as left at the end of attempt 8. All guest commands ran over ssh
(root, `~/.ssh/cinnamon-test-key`) to 192.168.122.15, 12:31–13:12 UTC.*

**Contradicts the attempt 7 premise.** Attempt 7 (line 1281) recorded: "2c must either
install `xorg-x11-server-Xorg` and set `WaylandEnable=false` in `/etc/gdm/custom.conf`
before the Cinnamon login attempt, or extend the driver for the Wayland greeter's session
menu. Decision belongs to 2c." The install path is closed on this platform: the package
does not exist in any Rocky 10.2 repository. Evidence:

1. `dnf install -y xorg-x11-server-Xorg` -> `Error: Unable to find a match:
   xorg-x11-server-Xorg`, rc=1. No transaction created (failed at package resolution).
2. `dnf repolist enabled` -> appstream, baseos, cinnamon-rocky10 (local), crb, extras.
   `dnf search xorg` -> the only server package offered is `xorg-x11-server-Xwayland`.
3. `dnf --refresh repoquery "xorg-x11-server*"` (mirror metadata force-refetched
   2026-08-27 ~12:37 UTC) -> only `xorg-x11-server-Xwayland` (24.1.9) + `-devel`
   (appstream/crb). Stale metadata ruled out.
4. `dnf repoquery "xorg-x11-drv-*"` -> **zero** packages (no X drivers either).
5. `dnf provides "*/bin/Xorg"` -> `Error: No matches found` (file-provides, fresh
   metadata).
6. Installed `gdm-47.0-22.el10_2` contents (`rpm -ql gdm`): ships
   `/usr/libexec/gdm-wayland-session`, **no `/usr/libexec/gdm-x-session`**. Repo query
   `dnf repoquery "gdm*"` -> only `gdm`, `gdm-devel`, `gdm-pam-extensions-devel` exist —
   no X-session subpackage to install.
7. `strings /usr/sbin/gdm`: the GDM 47 daemon still parses `WaylandEnable` (string also
   present in `/usr/libexec/gdm-runtime-config`), and for the X11 display execs
   `/usr/libexec/gdm-x-session` (absent per item 6); built-in failure message:
   `GdmLocalDisplayFactory: Both Wayland and Xorg are unavailable`. Flipping
   `WaylandEnable=false` on this guest would break the greeter (no X server binary and no
   X session launcher), which is why the config change was **not** made.
8. Source tree: `http://dl.rockylinux.org/pub/rocky/10.2/AppStream/source/tree/`
   `repomd.xml` -> primary.xml.gz (fetched 13:00 UTC, 564800 B) contains exactly one
   `xorg-x11-server*` package name: `xorg-x11-server-Xwayland`. Building from an
   RHEL-10 SRPM is also impossible.

External confirmation (RHEL 10 release notes / deprecation list) was not obtained
(docs.redhat.com returned 403 from this host); the in-guest evidence 1–8 stands on its
own.

**New fact for 2c-2 (attempt 8 under-recorded):** the Cinnamon install added
`/usr/share/wayland-sessions/cinnamon-wayland.desktop` (owner `cinnamon-6.7.4-1.el10`):
`Name=Cinnamon (Wayland)`, `Exec=cinnamon-session-cinnamon --wayland`. The Wayland
greeter's session menu now offers GNOME (Wayland) plus Cinnamon in two entries (Wayland
and the X11 entry from `/usr/share/xsessions/cinnamon.desktop`). The Cinnamon Wayland
session (muffin 6.7, experimental) is potentially launchable on this guest — relevant to
the re-scope below.

**State left (as found at end of attempt 8):** GDM active; greeter session `c1` on
seat0/tty1, Type=wayland, State=active, Timestamp=2026-08-26 15:18:04 UTC (boot; running
continuously since boot — the `loginctl list-sessions` "11h ago" column is a display
artifact, `show-session` properties are authoritative); `rpm -q xorg-x11-server-Xorg`
-> not installed; `/etc/gdm/custom.conf` unmodified (`#WaylandEnable=false` still
commented; the pre-edit backup made at 12:35 UTC was md5-identical `48e4c1ca7d728f4180d2abf8791bd14a`
and was deleted); no dnf transactions from this attempt; ssh OK; guest running under
libvirt.

**Revert:** nothing to revert — no persistent guest change was made (the temporary
`/etc/gdm/custom.conf.bak-2c1` was deleted; the original file is untouched). Any later
dispatch that does make changes must define its own revert.

**Alternatives considered:**

- **A. Install Xorg from Rocky 10.2 repos + `WaylandEnable=false` (dispatch as written):
  closed.** Evidence items 1–8.
- **B. Mix Fedora Xorg RPMs into the guest: rejected.** An X 21.x server pulls a
  mismatched libX11/mesa/wayland/libinput set against the RHEL 10 userland; fragile and
  unsupported, and it would be a *less* faithful reproduction — the user's failure report
  is on Rocky Linux 10.2, where the stock greeter is likewise Wayland-only (RHEL 10 ships
  no X server, per items 1–8).
- **C. Re-provision a RHEL 9 / Rocky 9 guest: rejected.** Violates the no-re-provisioning
  constraint (attempt 7 landmine, `provision-vm.sh:163` clobbers the disk under the same
  name), destroys the attempts 5/6/8 guest state (Cinnamon install, harness, evidence),
  and diverges from the user's Rocky 10.2 environment.
- **D. Re-scope 2c to the Wayland greeter (attempt 7's second option): recommended.** The
  harness already has pyatspi2 a11y access to this greeter (attempt 7 evidence
  `/root/evidence/greeter-ui-tree.log` captured its a11y tree, "Login code:" prompt
  present) and a uinput raw-input driver (`ukey`) whose events reach the Wayland greeter
  through kernel input (attempts 5/7 already drove this greeter). 2c-2 would drive the
  greeter's session menu (Cinnamon entries now present, see new fact above) instead of
  the X11-only Ctrl+Alt+Down shortcut. The failure mode being reproduced ("Authentication
  Error") is a PAM failure in the greeter's auth stage, which is display-protocol
  independent (inference, well-grounded: gdm auth runs in the greeter process for both
  backends).

**Decision requested (Robotnik):** approve re-scoping 2c-2 to the Wayland greeter
(option D) or direct otherwise (options B/C carry the stated costs). No guest work is
blocked on the decision; the guest is stable for either path.

---

### Item 2 — 2c-2 (item 2c-2b: resume + Wayland login run, 2026-08-27, Q4 endpoint)

*Resume dispatch from `456ce71` per `## Next Actions` (2026-08-27). Ran 19:18–20:40 UTC,
all guest commands over ssh (root, `~/.ssh/cinnamon-test-key`) to 192.168.122.15.
**Outcome: FAILURE — the Authentication-Error reproduction is confirmed twice, with the
account and the PAM stack proven sound outside the greeter.** The in-progress Wayland
harness adaptation was already complete at `456ce71`: the repo and in-VM copies of
`tasks/lib/gdm-a11y.py`, `tasks/lib/gdm-drive.sh`, `tasks/lib/ukey.c` are
byte-identical (verified by `diff` of `cat` over ssh, all three no output), and the
login drive (`gdm_login` → face click → password stage by role `password text` →
Login Options menu → `Cinnamon (Wayland)` entry → password → Return) executes end to
end on the live greeter. One real bug found and fixed in the adaptation: the caps
handling (below).*

**Attempt A (previous dead 2c-2 session, 17:36–17:40 UTC, evidence
`/root/evidence/cinnamon-attempt-2c2/`):** session `Cinnamon (Wayland)` selected,
password submitted, `journal-gdm.log` 17:38:01:
`pam_unix(gdm-password:auth): authentication failure; ... user=gdmtest` and
`secure-tail.log`: `unix_chkpwd[17893]: password check failed for user (gdmtest)`;
post-attempt a11y text shows the greeter dialog "Sorry, password authentication
didn’t work. Please try again."; no gdmtest session in `loginctl-sessions.log`.

**Attempt B (this run, 20:29–20:32 UTC, evidence
`/root/evidence/cinnamon-attempt-2c2b/`):** `gdm_login gdmtest
/root/gdmtest.pass cinnamon-wayland` rc=0 (input sent): a11y-verified clicks on
`gdmtest` face (597,349), `Login Options` (1160,744), `Cinnamon (Wayland)`
(1162,638); the new caps normalization logged `caps LED off; no toggle sent`;
`journal-gdm.log` 20:30:10: same `pam_unix ... authentication failure; ...
user=gdmtest`; `gdm_wait_session` rc=3 (no session after 120 s); post-attempt tree
shows the failure dialog visible @(443,505 394x40) and the password stage; no
gdmtest session in `loginctl-sessions.log`. **Control: the same password
authenticates through PAM outside the greeter** — `echo "$(cat
/root/gdmtest.pass)" | su -c 'id -un' gdmtest` → `gdmtest`, rc=0
(`04-su-control.log`, 20:32:23). The password is also crypt-verified against the
`/etc/shadow` hash in the same window (python3 `crypt.crypt(pw, shadow) ==
shadow` → `match: True`; passfile 24 hex chars, charset digits + `b`,`e`,`f`,
unchanged since baseline Aug 26 15:17).

**Diagnosis (what the evidence establishes, in order):**

1. **The account and the PAM stack are sound.** Control in Attempt B (su, same
   `pam_unix` service path) accepts the passfile password; the hash matches.
   Whatever the greeter's PAM received was not the passfile content.
2. **The password is corrupted in the input layer, most plausibly by caps lock.**
   Only the `b`/`e`/`f` chars of the password are shift-sensitive; a caps-on
   state uppercases exactly those and leaves the digits intact — the minimal
   alteration consistent with a `pam_unix` rejection.
3. **Proven harness bug (root cause of Attempt A):** the greeter's "Caps lock is
   on" label is a **static display**. Evidence (this run, greeter session c2):
   two ukey `Caps_Lock` presses flipped the kernel's cross-device caps LED
   (`/sys/class/leds/input1::capslock/brightness` 0 → 1 → 0, read between
   presses) while the label stayed visible the whole time, and the a11y clock
   node advanced in the same window (the a11y tree is live; the label is not
   updating). The label also survived a full greeter restart (visible at 15:59
   pre-restart in `2c2-pre-greeter-restart/a11y-text.log` and at 17:37 on the
   restarted greeter) and at 20:32 reports collapsed extents 80x0. The old
   `gdm_caps_lock_off` (label-driven, "toggle until the label is gone, 3 tries
   max") therefore sent all 3 presses whenever the label was visible: starting
   from caps OFF it ends caps **ON**, uppercasing the password's `b`/`e`/`f`
   chars — the exact corruption Attempt A shows. **Fixed** in
   `tasks/lib/gdm-drive.sh` (`gdm_caps_lock_off`): the label is no longer read;
   normalization is from the kernel caps LED (one press iff the LED is on), and
   `gdm_login` proves the input pipeline live by the face click before any
   password typing. Attempt B ran the fixed code (`caps LED off; no toggle
   sent`), which removes the proven corruption path.
4. **Open hypothesis (not yet proven): the compositor's caps state has diverged
   from the kernel LED.** Even with the LED off and no toggle sent, Attempt B's
   password was still rejected. The kernel LED is the parity proxy only while
   every caps press reaches the compositor; the 2c-2 session already observed a
   total input freeze on the previous greeter instance (01:07 UTC, record
   `2c2-pre-greeter-restart/diagnosis.log`), so a press that reached the kernel
   but not mutter would break parity. The compositor's caps state is currently
   unread: the label is static (item 3), the password field reads back empty by
   design (AT-SPI), and the username field's a11y node has an **empty name**,
   which `gdm-a11y.py textof` cannot target (probe attempt 20:36 UTC: typed
   `beef42` into the field node at (555,335), readback empty).
5. **Consistency with the user's original report** (Authentication Error
   selecting Cinnamon; a reboot restored the session): a stuck compositor caps
   state fits both details (reboot clears the greeter process's keyboard state),
   so does a transient PAM-state cause (H1–H4 remain open). The S-matrix
   scenarios (post-install reboot etc.) are the discriminator; this item
   establishes the reproduction and the input-layer suspect, not the fix.

**Changes this run:**

| File | Change | Why |
|---|---|---|
| `tasks/lib/gdm-drive.sh` (clone, synced to in-VM `/root/gdm-harness/`) | `gdm_caps_lock_off` rewritten: label-driven 3-toggle loop → kernel-LED-parity normalization (one press iff `/sys/class/leds/*capslock*/brightness` is 1); comment records the static-label evidence chain | Proven cause of Attempt A's password corruption; the label is unusable as a state source on the gdm-47 Wayland greeter |
| guest `/root/evidence/cinnamon-attempt-2c2b/` (new) | Attempt B evidence set: pre/post a11y, journal-gdm, journal-uid, secure-tail, loginctl, getenforce, sessions-available, 03-state-after, 04-su-control | The failure evidence + diagnosis for the item 2 verdict |
| host `/tmp/opencode/gdm-2c2b/` | `00-greeter-before.png`, `01-post-attempt.png` (`sudo virsh screenshot gdm-login-vm`) | Pixel record of both states |

**Alternatives considered:** (a) re-run Attempt B with the old label-driven caps
code — rejected, it is the proven corruptor; (b) extend `gdm-a11y.py` with a
`textof`-by-extents (index) so the username field can read back typed text, then
a probe-typed-caps-verify loop in `gdm_login` — the right next step but beyond
this dispatch's time bound (recorded for 2c-3); (c) reboot the guest to clear
any stuck compositor state — rejected as a first move: it would destroy the
unreproduced state (the live divergence evidence) and the no-re-provisioning
constraint applies to reboots that clobber the greeter's history.

**Time-bound note (AGENTS.md §5, stated plainly):** the ~60-min bound was
exceeded (~82 min). At the 50-minute mark (≈20:08 UTC) the login run had not yet
started; the run under test was the single decisive deliverable action and had
not been executed, so stopping would have left the outcome unrecorded. The
session stayed in the safe regime throughout (short commands, long idle gaps,
small context — the wedge risk is sustained long-run load, not command count).

**VM left as found:** running at the greeter (session c2, seat0/tty1, face list
up, `gdmtest` face visible — verified 20:38 UTC), no gdmtest session, ssh OK,
SELinux permissive, no guest reboot, no re-provision. Evidence dirs
`/root/evidence/cinnamon-attempt-2c2/` and `cinnamon-attempt-2c2b/` in place.

**For 2c-3 (next dispatch):** add `gdm-a11y.py textofext <x> <y>` (Text
interface on the visible node at given screen extents, no name needed); add a
caps pre-pass to `gdm_login` that types a probe into the username field, reads
it back, and toggles `Caps_Lock` until the readback is lowercase (max 3);
re-run the flow. A PASS then closes the input-layer suspect and points the fix
work at PAM/session launch (H1–H4); a second FAIL with a verified-lowercase
password promotes the PAM hypotheses.

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

### Item 3

*Executed 2026-08-24 (11:30 to 12:20 JST). Static packaging inspection per `## Plan` work
breakdown item 3. Host: Rocky Linux 10.2 runner. Scratch VM `cinnamon-test-vm` (2 vCPU / 4GB,
cloud image, provisioned by `vm-test/provision-vm.sh --destroy`, IP 192.168.122.52, destroyed
after the checks). No files in `metalllinux/cinnamon-for-rocky10` were modified. Clone at
`1f00da5` = `origin/main`, branch `task-0008-gdm-auth`. Scratch payloads kept under
`/tmp/opencode/item3/` (host, disposable).*

**Environment notes (not findings):**

- `rpms/` holds 48 RPM files plus `repodata/` (`ls rpms/*.rpm | wc -l` -> `48`).
- The clone has one untracked file, `vm-test/test-repo-setup.sh` (TASK-0006-era harness, never
  committed). Not mine; left as-is; flagged for `Tails`/`Knuckles`.
- Leftover state from the interrupted 2026-08-22 session removed as part of this item (both were
  `Big` artifacts, flagged for cleanup in `## Status` and `### Item 1`): orphaned paused QEMU
  `cinnamon-inspect-vm` pid 216968 (user `qemu`, RSS ~1.5GB, no domain record; `sudo kill 216968`
  -> gone) and its disk `/var/lib/libvirt/images/cinnamon-test/cinnamon-inspect-vm.qcow2`
  (1003552768 B; `rm` per the plan's rollback leftover-state rule). Host `free -g` after
  cleanup: 22 GB available.

**F1. Session/PAM/systemd file surface, all 48 RPMs (host).** Method: `rpm -qlp` on each of the
48 RPMs, filtered on `^/etc/pam\.d/|^/usr/share/(xsessions|wayland-sessions)/|\.session$|^/usr/lib/systemd/`.
Exactly two RPMs match; the other 46 have no files on this surface.

- `cinnamon-6.7.4-1.el10.x86_64.rpm` (5 files): `/etc/pam.d/cinnamon`,
  `/usr/share/cinnamon-session/sessions/cinnamon.session`,
  `/usr/share/cinnamon-session/sessions/cinnamon-wayland.session`,
  `/usr/share/xsessions/cinnamon.desktop`, `/usr/share/wayland-sessions/cinnamon-wayland.desktop`
- `cinnamon-session-6.7.3-1.el10.x86_64.rpm` (1 file): `/usr/lib/systemd/user/cinnamon-session.target`

**F2. The cinnamon-session user-unit question (plan, verified facts, `spec/cinnamon-session.spec:49-64`
expectation "most likely absent").** The unit **is** shipped, contradicting that expectation:

- `rpm -qlp --dump rpms/cinnamon-session-6.7.3-1.el10.x86_64.rpm` ->
  `/usr/lib/systemd/user/cinnamon-session.target 339 1786320000 5dcfc138... 0100644 root root 0 0 0 X`
- Installed on the scratch VM after the full install: `-rw-r--r--. 1 root root 339 Aug 10 00:00
  cinnamon-session.target` in `/usr/lib/systemd/user/`.
- Content (quoted from the RPM payload): a passive target, no `[Service]` section:
  `Wants=graphical-session.target` / `Before=graphical-session.target` /
  `Wants=graphical-session-pre.target` / `PropagatesStopTo=graphical-session.target` /
  `CollectMode=inactive-or-failed`.
- The session manager starts it itself: `cinnamon-session/csm-manager.c:1544`
  `csm_util_start_systemd_unit ("cinnamon-session.target", "replace", NULL);` (stop at `:892`), so
  registration happens at session start; the file lives in a standard user-unit path, which the
  user manager scans without per-user enablement or `daemon-reload`.
- It is **not** listed in `spec/cinnamon-session.spec:49-64` (`%files`). See F5.

**F3. X11 `RequiredComponents` chain.** Installed
`/usr/share/cinnamon-session/sessions/cinnamon.session` (identical in the `rpm2cpio`-extracted RPM
payload):

```
[Cinnamon Session]
Name=Cinnamon
RequiredComponents=cinnamon;nemo-autostart;cinnamon-killer-daemon;
DesktopName=X-Cinnamon
```

- `@REQUIRED@` in the source template (`cinnamon/cinnamon.session.in:3`) resolves to empty because
  `spec/cinnamon.spec:91` builds with `-Dnm_agent=internal`
  (`cinnamon/meson.build:63` `session_conf.set('REQUIRED', '')`).
- Components resolve as **desktop files, not binaries**: `cinnamon-session/csm-session-fill.c:128`
  calls `csm_util_find_desktop_file_for_app_name` (`csm-util.c:88`, `g_key_file_load_from_dirs` on
  `<name>.desktop` across the desktop/autostart dirs).
- Resolution state on the VM after the full 14-package install (all verified present):
  `cinnamon` -> `/usr/share/applications/cinnamon.desktop` (cinnamon RPM, `Exec=/usr/bin/cinnamon-launcher`,
  binary present); `nemo-autostart` -> `/usr/share/applications/nemo-autostart.desktop` (**nemo
  RPM only**, `Exec=nemo-desktop`, `/usr/bin/nemo-desktop` present); `cinnamon-killer-daemon` ->
  `/usr/share/applications/cinnamon-killer-daemon.desktop` (cinnamon RPM, `/usr/bin/cinnamon-killer-daemon`
  present, `#!/usr/bin/python3`, `python3` present at `/usr/bin/python3`).
- **Conditional gap:** if the installer skips the second command of INSTALL.md (`INSTALL.md:38-39`,
  which includes `nemo`), `nemo-autostart.desktop` is absent and the session manager cannot fulfill
  a required component. Item 3 cannot establish what the user actually installed; the matrix (S1)
  uses the full INSTALL.md procedure.
- `xsessions/cinnamon.desktop` Exec chain intact on the VM: `/usr/bin/cinnamon-session-cinnamon`
  (`#!/usr/bin/sh`, `exec cinnamon-session --session cinnamon "$@"`) -> `/usr/bin/cinnamon-session`
  (`#!/usr/bin/sh` wrapper) -> `/usr/libexec/cinnamon-session-binary`.
- Wayland session (outside the X11 path, recorded for completeness):
  `cinnamon-wayland.session` has `RequiredComponents=cinnamon-wayland;nemo-autostart;`; the
  `cinnamon-wayland` component resolves to `/usr/share/applications/cinnamon-wayland.desktop`
  (`Exec=cinnamon --replace`), but no RPM ships `/usr/bin/cinnamon-wayland`.

**F4. PAM file (host + VM).** The installed `/etc/pam.d/cinnamon` is byte-identical to the RPM
payload and to the source template. `md5sum` on all three:

```
e6aef20bcd9e897876e28b2e659b1e6c  (VM) /etc/pam.d/cinnamon
e6aef20bcd9e897876e28b2e659b1e6c  (rpm2cpio payload)
e6aef20bcd9e897876e28b2e659b1e6c  ~/Linux/projects/cinnamon_4_rocky10/cinnamon/data/pam/cinnamon.pam
```

Content is the standard RHEL-style stack: `auth`/`account`/`password`/`session` all
`include system-auth`, `-auth sufficient pam_selinux_permit.so`, `-auth optional pam_gnome_keyring.so`.
GDM's interactive login uses the `gdm-password` service (assumption A3), not the `cinnamon`
service; `/etc/pam.d/cinnamon` is the only PAM file any of the 48 RPMs writes (F1). Even if it were
used, its auth stack is the same `system-auth` includes as `gdm-password`, so no packaged content
makes Cinnamon auth diverge from GNOME.

**F5. Spec-to-RPM drift (repo-wide): the shipped RPMs were not built from the committed specs.**
Method: each spec's `%files` entries macro-expanded with `rpm --eval` and compared against
`rpm -qlp`; every entry below re-verified with direct `rpm -qlp | grep -qx` and the spec lines
read from the clone.

- `cinnamon-session` (the package the plan flagged): the spec lists **6 paths absent from the RPM**:
  `/usr/bin/cinnamon-session-calculate-display-type`, `-debug`, `-launch-desktop`, `-restart-x`,
  `-workspaces-client`, `/usr/libexec/cinnamon-session`. The RPM contains **11 files the spec does
  not claim**: the systemd user unit (F2), `/usr/libexec/cinnamon-session-binary`,
  `/usr/libexec/cinnamon-session-check-accelerated`,
  `/usr/libexec/cinnamon-session-check-accelerated-helper`, 6 `cinnamon-session-properties` icons,
  and `/usr/share/glib-2.0/schemas/org.cinnamon.SessionManager.gschema.xml` (the spec's glob
  `org.cinnamon.desktop.session*.gschema.xml` at `spec/cinnamon-session.spec:60` does not match
  that name).
- `cinnamon-settings-daemon`: spec claims `/usr/bin/cinnamon-settings-daemon`,
  `/usr/libexec/cinnamon-settings-daemon`, `/usr/share/cinnamon-settings-daemon`,
  `/usr/share/dbus-1/services/org.cinnamon.settings_daemon.service`; all four **absent** from the
  RPM (`rpm -qlp | grep -qx` -> ABSENT for each). The RPM ships `csd-*` binaries instead
  (`/usr/bin/csd-a11y-settings` ... `/usr/bin/csd-xsettings`).
- `nemo`: spec claims `/usr/bin/nemo-file-properties`, `/usr/bin/nemo-pathbar-popup` (absent) and
  `Nemo-6.0.typelib` / `Nemo-6.0.gir` (the RPM has `Nemo-3.0.*`). The spec also declares a
  `%files -n %{name}-python` subpackage; **no `nemo-python` RPM exists in `rpms/`** and no
  `/usr/lib64/nemo/python3` path exists in any RPM.
- `cinnamon-desktop`: spec claims `/usr/lib64/libcinnamon-desktop.so` and `/usr/lib64/libcvc.so`
  (bare soname symlinks); the RPM contains only the versioned `libcinnamon-desktop.so.4[.0.0]`
  and `libcvc.so.0[.0.0]`.
- `cinnamon-menus`: spec claims `Menu-3.0.typelib` / `Menu-3.0.gir`; the RPM has `CMenu-3.0.*`.
- `cinnamon` (818 files): all 32 exact spec entries and all 19 glob patterns are present in the
  RPM; drift limited to the auto-added `/usr/lib/.build-id/*` files (standard rpmbuild/debugedit
  behavior). This is the one base package whose spec matches its RPM.

Timing evidence: the RPM mtimes are `Aug 12 11:10`; every drifted spec was introduced in commit
`d5cfacd` (2026-08-12 11:14 JST, "Complete Cinnamon 6.7.x build") four minutes later
(`git log --follow -- spec/cinnamon-session.spec` -> only `d5cfacd`;
`git diff d5cfacd..HEAD -- spec/cinnamon-session.spec` -> empty). Conclusion: the committed specs
were written after the build and do not describe the built files. Consequence for item 6:
rebuilding any of the five drifted packages from the current specs fails in both directions
(rpmbuild "File not found" for the missing `%files` paths; "File not owned by any package" for the
unclaimed buildroot files). `%files` must be regenerated from actual build output before the
rebuild.

**F6. Scriptlets, all 48 RPMs (host).** `rpm -q --scripts -p` on each RPM: 8 RPMs carry
scriptlets, all identical (`postinstall program: /sbin/ldconfig`,
`postuninstall program: /sbin/ldconfig`): `cinnamon-control-center`, `cinnamon-desktop`,
`cinnamon-menus`, `cinnamon-settings-daemon`, `cjs`, `mozjs115`, `muffin`, `nemo`. The other 40
have none, **including `cinnamon` and `cinnamon-session`**. No systemd-related scriptlet exists in
any RPM. `cinnamon` ships 2 `.so` files without an `ldconfig` scriptlet; that is mitigated by the
manual `sudo ldconfig` at `INSTALL.md:47`, which is part of the user procedure and the matrix.

**F7. Scratch VM installed state (Part B).**

- Provision: `bash vm-test/provision-vm.sh --destroy` ->
  `VM 'cinnamon-test-vm' provisioned and ready.`, `IP: 192.168.122.52`, from
  `/var/lib/libvirt/images/cinnamon-test/Rocky-10-GenericCloud.qcow2` (2 vCPU / 4GB).
- **Baseline before any modification:** `getenforce` -> `Enforcing`;
  `/etc/selinux/config`: `SELINUX=enforcing`, `SELINUXTYPE=targeted`;
  `cat /etc/redhat-release` -> `Rocky Linux release 10.2 (Red Quartz)`;
  `rpm -q gdm gnome-shell` -> `package gdm is not installed` / `package gnome-shell is not installed`.
  The cloud image boots **enforcing** by default.
- Repo: `scp -r rpms repo-setup` to `/root/` (48 RPMs verified on the VM);
  `bash /root/repo-setup/setup-repo.sh /root` -> `=== Repository setup complete ===`.
- Install, the exact INSTALL.md procedure: `dnf install -y cinnamon` -> `Complete!`;
  `dnf install -y cinnamon-session cinnamon-settings-daemon cinnamon-control-center nemo mozjs115-devel`
  -> `Complete!`; `ldconfig` -> rc=0.
- Installed set, `rpm -q` per package (all 14 packages of the INSTALL.md table, exact versions):
  `mozjs115-115.29.0-1.el10.x86_64`, `mozjs115-devel-115.29.0-1.el10.x86_64`,
  `cjs-6.4.0-1.el10.x86_64`, `muffin-6.7.4-3.el10.x86_64`, `muffin-clutter-6.7.4-3.el10.x86_64`,
  `muffin-cogl-6.7.4-3.el10.x86_64`, `cinnamon-desktop-6.7.2-1.el10.x86_64`,
  `xapps-lib-3.3.3-1.el10.x86_64`, `cinnamon-session-6.7.3-1.el10.x86_64`,
  `cinnamon-settings-daemon-6.7.2-1.el10.x86_64`, `cinnamon-control-center-6.7.2-1.el10.x86_64`,
  `cinnamon-menus-6.7.0-1.el10.x86_64`, `nemo-6.7.4-1.el10.x86_64`,
  `cinnamon-6.7.4-1.el10.x86_64`.
- `rpm -V` on all 14: no output for any package (no file-integrity diffs).
- File contexts under enforcing after the full install (`ls -Z`):
  `system_u:object_r:etc_t:s0 /etc/pam.d/cinnamon`, `bin_t:s0 /usr/bin/cinnamon`,
  `bin_t:s0 /usr/libexec/cinnamon-session-binary`,
  `systemd_unit_file_t:s0 /usr/lib/systemd/user/cinnamon-session.target`,
  `usr_t:s0` on the three component `.desktop` files, both session files, and the xsessions entry.
  All standard default contexts; no custom policy needed for the files to exist.
  `ausearch -m avc -ts recent` -> `<no matches>` after the full install; `getenforce` still
  `Enforcing` afterwards.

**F8. `ldd` sweep (VM).** Method: `ldd <target> | grep -c "not found"`; every target returned 0.
Targets, all `OK`: `/usr/bin/cinnamon`, `/usr/bin/cinnamon-launcher`,
`/usr/libexec/cinnamon-session-binary`, `/usr/bin/muffin`, `/usr/bin/nemo`,
`/usr/bin/nemo-desktop`, `/usr/bin/csd-power`, `/usr/bin/csd-xsettings`, `/usr/bin/csd-media-keys`,
`/usr/lib64/libcinnamon-desktop.so.4`, `/usr/lib64/libmuffin.so.0`, `/usr/lib64/libcjs.so.0`.

**F9. Availability probes (Part C, in the VM).**

- Default repos (`appstream`, `baseos`, `crb`, `extras`, local `cinnamon-rocky10`;
  `dnf repolist`): `dnf provides /usr/bin/xdotool` -> `Error: No matches found.`; same result for
  `dnf provides /usr/bin/ydotool`, `dnf provides /usr/bin/dogtail`, `dnf provides dogtail`
  (package name), and `dnf provides /usr/bin/lightdm`.
- EPEL 10 (`dnf install -y epel-release`, then
  `dnf --disablerepo="*" --enablerepo=epel list available "xdotool*" "ydotool*" "dogtail*" "lightdm*"`):
  `Error: No matching Packages to list`. All four names are absent from EPEL 10 as well.
- Micro-driver feasibility (fallback ladder, plan risk R1):
  `dnf provides /usr/include/X11/Xlib.h` -> `libX11-devel-1.8.10-1.el10.x86_64` (appstream);
  `dnf provides /usr/include/X11/extensions/XTest.h` -> `libXtst-devel-1.2.4-8.el10.x86_64`
  (appstream); `dnf list available gcc make` -> `gcc-14.3.1-4.4.el10` (appstream),
  `make-4.4.1-9.el10` (baseos). All build inputs are in the default repos.
- SELinux surface: none of the 48 RPMs ships any SELinux file
  (`rpm -qlp` scan on `selinux|\.te$|file_contexts|semanage` -> no matches in any RPM); the VM
  carries stock `selinux-policy-targeted-42.1.18-4.el10.noarch`.

**Decisions (acceptance criteria).**

- **Input driver (A8, R1): the in-VM XTest micro-driver.** `xdotool`, `ydotool`, and `dogtail`
  are all absent from the default Rocky 10 repos and from EPEL 10 (F9), so the first three rungs of
  the plan's fallback ladder are unavailable. The fourth rung (an XTest micro-driver compiled in
  the VM from `libX11-devel` + `libXtst-devel` + `gcc` + `make`, all present in default repos per
  F9) is the only repo-sourced option. It is test-only, built at task start inside the VM, and is
  never shipped in the `cinnamon-for-rocky10` repo. `Tails` (item 2) must therefore include the
  driver source and an in-VM build step in the harness.
- **LightDM (R6): scenario S2 is blocked at the repo level.** `lightdm` is not in the default EL10
  repos and not in EPEL 10 (F9). S2 is excluded from the item 10 matrix and counted explicitly in
  the checks-requested-vs-run below, per the plan's contingency ("recorded as blocked with the
  `dnf` evidence", not silent).

**H1-H4 marks.**

- **H1 (session-file/packaging content): not supported as a cause of the installed-state failure.**
  Every session-surface file installed is correct and internally consistent (F1-F4, F7, F8):
  session entries, PAM file, `.session` content, and the full `RequiredComponents` chain all
  resolve after the full INSTALL.md install. Two caveats: (a) the `nemo-autostart` component
  resolves only if the `nemo` package was installed (F3); if the user skipped INSTALL.md:38-39,
  session launch would fail on a missing required component. (b) The spec-to-RPM drift (F5) is a
  real packaging-integrity defect in the repo, but it does not affect the installed state the user
  has; it blocks item 6's rebuild until `%files` is regenerated.
- **H2 (PAM auth failure): not assessable statically; neutral.** The package set never touches
  GDM's `gdm-password` path, and the one PAM file it ships is a standard `system-auth` stack (F4).
  Nothing in the RPMs makes Cinnamon auth behave differently from GNOME. Confirmation of A3 (the
  service tag in `/var/log/secure` for a failed Cinnamon attempt) comes from item 4.
- **H3 (transient first-login state): the unit-registration sub-hypothesis is not supported.**
  The user unit ships, installs to the standard user-unit path, and is started by the session
  manager itself (F2); no scriptlet or per-user enablement is required for it to be visible. The
  remaining sub-hypotheses (GDM/logind state, first-run dconf for a pre-existing GNOME user) are
  open and are decided by items 4 and 5.
- **H4 (SELinux enforcing): not assessable statically; baseline recorded.** The cloud image boots
  enforcing (F7), matching the assumed user-machine default (A2), while all prior harness runs were
  permissive. Installed files carry standard default contexts with zero AVCs during the full
  install (F7), and no RPM ships SELinux content (F9). The enforcing behavior question is decided
  by scenario S5.

**Checks requested vs run (item 3):** 17 requested, 17 executed. Nothing dropped.

| # | Check (per the plan's item 3) | Status |
|---|---|---|
| 1 | `rpm -qlp` over all 48 RPMs, session/pam/systemd surface | run (48/48, F1) |
| 2 | `rpm -q --scripts` over all 48 RPMs | run (48/48, F6) |
| 3 | cinnamon-session user-unit question | run (F2) |
| 4 | VM: diff `/etc/pam.d/cinnamon` vs source | run (md5-identical, F4) |
| 5 | VM: `xsessions/cinnamon.desktop` | run (F3, F7) |
| 6 | VM: `sessions/cinnamon.session` + `RequiredComponents` incl. `nemo-autostart` | run (F3) |
| 7 | VM: `rpm -V` all 14 packages | run (14/14 clean, F7) |
| 8 | VM: `ldd` | run (12 launch-chain targets, F8) |
| 9 | `dnf provides /usr/bin/xdotool` | run (F9) |
| 10 | `dnf provides` ydotool | run (F9) |
| 11 | `dnf provides` dogtail | run (binary + package name, F9) |
| 12 | `dnf provides /usr/bin/lightdm` | run (F9) |
| 13 | `getenforce` on the cloud image | run (Enforcing, F7) |
| 14 | Findings with command + output for every claim | this subsection |
| 15 | H1-H4 each marked supported/unsupported | this subsection |
| 16 | Input-driver choice decided and recorded | this subsection |
| 17 | LightDM availability decided and recorded | this subsection |

Additional evidence gathered beyond the letter of the item (EPEL probes, micro-driver
feasibility, component-resolution code trace, spec-to-RPM comparison, file contexts, AVC check):
listed in F3, F5, F7, F9. No check was reduced.

**Verdict:** item 3 acceptance criteria met. The static inspection found no defect in the
*installed* session surface that would explain the GDM Authentication Error (H1 not supported for
installed content; H2 neutral; H3 unit sub-hypothesis not supported; H4 baseline recorded). It did
find two repo-level defects that matter downstream: the spec-to-RPM drift (F5, blocks item 6's
rebuild until `%files` is regenerated, goes to `Tails`) and the absence of every off-the-shelf
greeter input driver from EL10 + EPEL repos (F9, forces the XTest micro-driver in item 2, goes to
`Tails`). LightDM scenario S2 is blocked at the repo level and is recorded as such, not skipped
silently. Next per `## Next Actions`: item 2 (Tails, GDM harness), informed by F9.

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
