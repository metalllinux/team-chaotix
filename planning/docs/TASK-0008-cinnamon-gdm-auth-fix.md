# TASK-0008 — Fix GDM Cinnamon-session login Authentication Error; widen VM test matrix

> **Section order below is fixed.** Each agent writes to its own section and no other. `Robotnik`
> reads only `## Status` and `## Next Actions`. Do not reorder, rename, or remove sections.

- **Created:** 2026-08-20

---

## Status

*Owner: `Robotnik`. Keep this SHORT and CURRENT — it is one of only two sections the PM reads, so a
stale entry means the whole loop runs on bad information.*

**Now (2026-08-30, fourth entry): user instruction — merge all 13 branch commits to main now.**
User directed (2026-08-30, second explicit ask) that **all** commits on `task-0008-gdm-auth` be
pushed to main. Branch state: tip `f259dd5` = origin, 13 commits ahead of `main`
(`b15dfcb`..`f259dd5`: 5 harness commits + 3 batch-A security fixes + 5 batch-B
verdict-integrity fixes), tree clean. **DoD deviation recorded (AGENTS.md §5):** the Omega gate
is satisfied (high + 2 medium fixed in batch A); the Shadow gate is **not** — should-fixes #2
(ukey uppercase drop), #5 (prereq checks), #6 (hardcoded 48), #10 (provisioning dup) plus the
vnc-grab question (batch C) and 7 nits remain, and the trio re-run + bare-metal interactive
matrix have not run. The merge proceeds on explicit user instruction; `Knuckles` executes it
via PR; the remaining items are tracked in `## Next Actions` and land on main as a follow-up
merge after batches C/D + the clean re-run. The outstanding key evidence is the bare-metal
interactive matrix (start GDM, log in as `howard`, no-glitch check) in Big's re-run.

**Now (2026-08-30, third entry): trio complete (Shadow → Omega → Big); merge gate blocked;
fixes sequenced as four small-context batches.** Big (12/12 checks run, none dropped): non-VM
layers PASS with findings — `vnc-grab.py` proven **non-functional against any spec-conformant
RFB server** (5 protocol defects; it never worked — 2c-3b's screenshots came from QMP
`virsh screenshot`, so the 2c-3b login/PAM evidence stands); Shadow #3 false-PASS rc checks
confirmed live. Bare-metal env prep PASS: dedicated key installed (alias `cinnamon-bm103`,
`~/pass.txt` tightened to 600), baseline 674 packages with no DM / no X / no desktop, 48-RPM
set (sha256-verified) installed cleanly pulling 157 packages with **no login manager and no X
server** (mesa Wayland + X11 libs only), both session entries present, GDM 47 + gnome-shell
49.4 installed, enabled, not started, Wayland-only. **Xorg re-confirmed absent from every repo
on the machine; Xwayland is the X11-compat path** — that answers the user's Xorg question.
Machine state: "Cinnamon+GDM installed and enabled, not started", at the getty; evidence
`~/t0008-*.txt` on the machine. Observation channel decision (Robotnik): no VNC exists on the
machine (vnc-grab inapplicable there by architecture) — primary channel for the interactive
matrix is a11y + journal + ukey input, with the user at the physical console for visual
"no glitches" confirmation; a cheap Wayland screenshot bridge is optional. The vnc-grab.py
question (rewrite per RFB spec vs replace with the proven QMP `virsh screenshot` and delete)
is Tails' call, recorded in `## Implementation`. Fix batches, single-deliverable per the safe
regime: **A** = Omega high + 2 medium (known_hosts pinning — fingerprints in Big's checkpoint 2
in `## Test Results` — key-permission checks, setup-repo.sh assertion); **B** = Shadow's five
verdict-integrity fixes (#3, #4, #7, #8, #9); **C** = vnc-grab decision + implementation;
**D** = remaining should-fixes (#5, #6, #10) + nits. Then the trio re-runs; Big's re-run = VM
harness re-run + the bare-metal interactive matrix (start GDM, log in as `howard`, verify
session, no-glitch evidence).

**Now (2026-08-30, second entry): bare-metal test host available; fix path unblocked.** User
provided a Rocky Linux 10.2 **minimal-server** bare-metal machine for real-hardware testing:
`howard@192.168.1.103` (ssh port 22 open from the PM host; the user password is in
`~/pass.txt` on the PM host — read it there, never write it to docs/logs/commits/transcripts;
sudo on the machine is passwordless; no key authorized yet). Real-hardware scenario per the
user: (a) deploy the latest Cinnamon RPMs and verify they install from a minimal state with no
login manager and no windowing system, (b) Cinnamon (Wayland) login via GDM works and the
desktop is navigable with no glitches or breakage, (c) check whether Xorg works. Plan risk R2
(the fix path gated on the user's real-machine logs) is **unblocked**: the team tests the
machine directly. Chain order holds (Shadow complete: 0 blockers / 10 should-fix / 7 nits); the
bare-metal **interactive** matrix (login + navigation) runs in Big's re-run after Tails fixes
the harness, because should-fix #1 (`vnc-grab.py` endianness) and #2 (`ukey.c` uppercase drop)
directly affect screenshot and typed-input reliability. Big's first pass does env prep
(one-time `ssh-copy-id` so later access is key-based) plus the non-interactive part: baseline
minimal-state evidence, RPM install from the local DNF repo, what gets pulled in (any DM? any X
server?), session entries, GDM install + enable. Xorg expectation: 2c-1 already verified in-guest
that `xorg-x11-server-Xorg` is in no Rocky 10.2 repo — the machine re-verifies it; if absent
there too, that is the recorded answer.

**Now (2026-08-30): user decision — merge `task-0008-gdm-auth` to main now; new scope is
TASK-0015.** User request (2026-08-30): as much of the branch as possible onto main, plus new
scope (minimal-server install without any login manager or windowing system, and LightDM/SDDM
support, both tested). Branch state verified: `task-0008-gdm-auth` = `097702e` = origin, 5
commits ahead of `main` (`1f00da5`), all VM-test harness code that produced the 2c-3b PASS;
working tree clean. Decision: the harness is verified (item 2 PASS), so the **whole branch is
shippable**; it goes through the standard chain Shadow → Omega → Big → Tails fixes → Vector →
Knuckles (PR + merge), then TASK-0015 starts from the updated main. The fix path (items 4–6)
stays gated on the user's real-machine logs (`journalctl -u gdm`, `/var/log/secure`), requested
again 2026-08-30; if the logs show an RPM defect, it proceeds on a new branch off the merged
main. Item 9a (Sparrow suite) is deferred into TASK-0015, where the widened matrix lands; the
TASK-0009 plan stays in Planning.

**Now (2026-08-28 05:41 UTC): item 2 complete — 2c-3b PASS; the Authentication Error
root-caused to the harness, not to Cinnamon.** 2c-3b (02:21–03:21 UTC, VM work 43 min, all
safeguards held): `gdmtest` logged in and Cinnamon (Wayland) session 512 is active (loginctl +
process verified), zero new PAM failures. The 2c-2 failures are explained by the `ukey.c`
keycode corruption — the old `KEY_A + (c - 'a')` mapping mistypes every letter except `a`
(Linux keycode space is non-contiguous: a=30…l=38, z=44, x=45, c=46, v=47, b=48); the 2c-2
caps-lock theory was a red herring (record: checkpoint `### Item 2 — 2c-3`). With a correct
input layer the VM does **not** reproduce the user's failure; no RPM fix is indicated by VM
evidence. Consequence (plan risk R2): the fix path (items 4–6) is gated on the user's
real-machine logs (`journalctl -u gdm`, `/var/log/secure`), requested from the user this
session. Meanwhile the chain proceeds with 9a (Tails, Sparrow suite) and Amy (TASK-0009 plan),
both independent of the fix path.

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
- [x] `Tails` (item 2c-3b, dispatched 2026-08-28): **complete 2026-08-28 ~03:05 UTC,
      PASS** — Cinnamon (Wayland) session 512 active for gdmtest (loginctl + process
      verified), zero new PAM failures; the Authentication Error root-caused to the
      harness `ukey.c` keycode corruption (letters non-contiguous in keycode space),
      not the Cinnamon RPMs; ~43 min, all safeguards held; record: checkpoint
      `### Item 2 — 2c-3`.
- [x] `Tails` (item 2c-3, after 2c-2): complete via 2c-3b — textofext probe +
      probe-typed caps pre-pass + ukey fix committed at `097702e`, re-run PASS (the
      input-layer suspect is closed; no PAM defect found, so H1–H4 are not promoted);
      record: checkpoint `### Item 2 — 2c-3`. The checkpoint's consequence note
      (VM no longer reproduces the user's failure; route on the user's machine logs
      per plan risk R2) awaits `Robotnik`'s call on the next dispatch.
- [x] `Robotnik` (2026-08-28 05:41 UTC): 2c-3b PASS recorded (Status); item 2 (harness)
      complete. Fix path (items 4–6) gated on the user's real-machine logs (plan risk R2);
      requested. Meanwhile: 9a and Amy (TASK-0009 plan) dispatch — both independent of the fix
      path.
- [x] `Robotnik` (2026-08-30): user re-prioritized — merge the branch to main first (record:
      Status). Item 9a (Sparrow suite) deferred to TASK-0015, where the widened matrix
      (minimal-server install + LightDM/SDDM) lands; the TASK-0009 plan stays in Planning.
- [x] `Shadow` (complete 2026-08-30): 0 blockers, 10 should-fix, 7 nits in `## Review`.
- [x] `Omega` (complete 2026-08-30): 0 critical, 1 high, 2 medium, 4 low in `## Security`;
      merge blocked until high + medium resolved (DoD).
- [x] `Big` (complete 2026-08-30): non-VM 12/12 run, PASS with findings (vnc-grab
      non-functional; #3 false-PASS live); bare-metal env prep + install PASS — machine at
      "Cinnamon+GDM installed, enabled, not started" (record: Status + `## Test Results`).
- [x] `Tails` (batch A, complete 2026-08-30): `1c16045` (host-key pinning on all 12
      ssh/scp/rsync channels, fail-closed, per-VM pin files seeded out-of-band — the cloud
      image ships no host keys), `af3a9ff` (key-permission assertion + target-aware keying,
      bare-metal host never gets the fleet key), `cd6860c` (setup-repo.sh statelessness
      asserted; canary regression caught). Omega high + 2 medium resolved, verified live.
- [x] `Tails` (batch B, complete 2026-08-30): `85f629e` (#3 exact-rc comparison), `921de9f`
      (#4 --destroy-only proves end state, teardown recorded from rc), `9ce6cb5` (#7
      waiteditable dispatch deleted — no definition, no basis), `6f6b1b5` (#8 abort rcs
      propagate before any wait), `f259dd5` (#9 ChannelError + shared wait_for, broken channel
      vs missing node reported separately). All five verified per finding; record: `##
      Implementation` `### Fix batch B`.
- [ ] `Knuckles` (dispatched 2026-08-30, **user instruction**): open the PR
      `task-0008-gdm-auth` → main and merge all 13 commits (`b15dfcb`..`f259dd5`). The DoD
      deviation is recorded in `## Status` (Shadow gate not met: #2, #5, #6, #10 + vnc-grab +
      7 nits remain; trio re-run + interactive matrix pending) — the user has explicitly
      authorized this merge with those tracked as follow-ups; record the deviation + follow-up
      list in `## Release`.
- [ ] `Tails` (batch C): vnc-grab decision (rewrite per RFB spec vs replace with QMP `virsh
      screenshot` + delete) recorded in `## Implementation` with alternatives, then implement.
      Checkpoint `### Fix batch C`.
- [ ] `Tails` (batch D): remaining should-fixes (#2 ukey uppercase drop, #5 prerequisite
      checks, #6 hardcoded 48-RPM check, #10 provisioning dedup) + nits. Checkpoint
      `### Fix batch D`.
- [ ] `Shadow` (re-run): verify batches A–D resolved all findings in `## Review`.
- [ ] `Omega` (re-run): verify all findings above low resolved in `## Security`.
- [ ] `Big` (re-run): VM harness re-run (re-establish login evidence with the fixed harness) +
      bare-metal interactive matrix (start GDM, log in as `howard`, a11y + journal + ukey
      verification, user at the physical console for visual confirmation, record no-glitch
      evidence) in `## Test Results`.
- [ ] `Vector`: update the repo README + INSTALL.md for the verified state (GDM Wayland login
      PASS, harness location and usage); write to `## Docs`. Lands with the follow-up merge.
- [ ] `Knuckles` (follow-up): land batches C + D + re-run results + docs on main (second PR
      from the same branch or a new one — shape is Knuckles' call); then the task is DONE.
- [ ] `Robotnik`: after the merge, start the TASK-0015 chain (work branch from the updated
      main, then Amy). The fix path (items 4–6) is no longer gated on the user's logs — the
      bare-metal matrix on `192.168.1.103` is the real-machine evidence; its results decide
      whether items 4–6 proceed at all.

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

### Item 2 — 2c-3 (item 2c-3b: resume + discrimination run, 2026-08-28, Q4 endpoint)

*Resume dispatch from `097702e` per `## Next Actions` (2026-08-28). Ran
02:21:31–03:05 UTC (~43 min), inside the 80-min bound. All guest commands over
ssh (root, `~/.ssh/cinnamon-test-key`) to 192.168.122.15; every command output
truncated before context entry (`tail -c` ≤ 2000); a11y probes returned only
targeted readbacks (tree/text dumps went to in-VM evidence files, never to
context). **Outcome: PASS — the Cinnamon (Wayland) session logged in with the
correct password (this run 02:45 UTC; a second independent PASS by the dead
2c-3 session at 01:39:26 UTC), and the greeter Authentication Error is
root-caused to the harness input driver (`ukey.c`), not to the Cinnamon RPMs.***

**Root cause (found by the dead 2c-3 session via strace + readback, re-verified
end-to-end by 2c-3b):** `ukey.c` mapped letters as `KEY_A + (c - 'a')`. Letters
are not contiguous in Linux keycode space (home row a=30…l=38, then bottom row
z=44, x=45, c=46, v=47, b=48, n=49, m=50), so every letter except `a` was
mistyped in the greeter: `ukey type abc` sent KEY_A/KEY_S/KEY_D (strace) and
the a11y Text readback of the username entry showed "asd" for typed "abc".
With the test password's hex charset (0-9, a-f) the corruption was b→s, e→g,
f→h — exactly the minimal alteration both 2c-2 `pam_unix` rejections were
consistent with. 2c-2's caps-lock diagnosis was a misattribution: the caps
machinery was a red herring (record: `tasks/lib/ukey.c:133-143`, the
evidence-chain comment; fix at `tasks/lib/ukey.c:145`, `letter_to_key()`).
The fix, the `textofext` probe (`tasks/lib/gdm-a11y.py:456`), and the
probe-typed caps pre-pass (`tasks/lib/gdm-drive.sh:381`,
`gdm_caps_probe_normalize`, wired into `gdm_login` at
`tasks/lib/gdm-drive.sh:582`) were already committed at `097702e`; 2c-3b
verified them against the live greeter and ran the login.

**Verification (step 2, 02:42–02:44 UTC):** greeter state confirmed clean
(face list up, `gdmtest` face visible, no dialog, no gdmtest session, caps
LED 0). Harness synced from clone `097702e` (scp of `gdm-a11y.py`,
`gdm-drive.sh`, `ukey.c`); `ukey` rebuilt in the VM (`gcc -O2 -Wall -Wextra`,
02:41 UTC, no warnings) because the in-VM binary predated the fix and
`gdm_build_driver` skips when the binary exists. `gdm_caps_probe_normalize
gdmtest` rc=0: entry @(489,465 302x20), **typed 'abc', readback 'abc'** (the
pre-fix binary reads back 'asd'), compositor caps verified LOWERCASE by
readback, 0 toggles, password stage up. `bash -n gdm-drive.sh` and
`python3 -m py_compile gdm-a11y.py` clean on the host.

**Login run (step 3, t0 = 2026-08-28 02:45:02 UTC):** `gdm_login gdmtest
/root/gdmtest.pass cinnamon-wayland` rc=0 (pre-pass re-verified lowercase;
'Login Options' clicked @(1160,744) → 'Cinnamon (Wayland)' @(1162,638);
password typed; Return). `gdm_wait_session` rc=0: **VERIFIED session 512
type=wayland state=active proc='cinnamon'**; `loginctl list-sessions`:
session 512, UID 1000 `gdmtest`, seat0, tty2, class user. Desktop processes
(`pgrep -u gdmtest -af cinnamon`): `gdm-wayland-session --handle-registration
cinnamon-session-cinnamon --wayland` (26185), `cinnamon-session-binary
--session cinnamon-wayland` (26195), `/usr/bin/cinnamon --replace` (26256).
PAM view: **zero new `authentication failure` lines** in `/var/log/secure`
(count stayed 2, both the Aug 27 2c-2 attempts at 17:38:01 and 20:30:10) and
`pam_unix(gdm-password:session): session opened for user gdmtest(uid=1000)`
at 02:46:25. `pam_unix` does not log auth successes by default on RHEL, so
no-new-failures + session-opened + active desktop is the success evidence.
SELinux Permissive. Evidence: VM `/root/evidence/cinnamon-attempt-2c3/`
(journal-gdm, journal-uid, secure-tail, loginctl-sessions,
loginctl-session-512, getenforce, sessions-available, a11y-tree, a11y-text).

**Reproducibility:** the dead 2c-3 session had already run this same flow to
PASS at 01:39:26 UTC (session 498) before dying at 02:07 UTC; its `run.log`
in the evidence dir records `PHASE_RESULT VERDICT cinnamon login PASS (session
+ cinnamon-session process verified; password verified lowercase by probe
readback; logged out to greeter)`, and its `01-pre-*`, `04-loginctl-detail.log`,
`05-post-logout-*` files are from that run (this run's capture appended the
journal/secure/loginctl/a11y set). Two PASSes, same code, no reboot between.

**VM left as found:** after the run, `loginctl terminate-session 512`; greeter
back on tty1 (session c4), face list up, `gdmtest` face visible, no gdmtest
session, caps LED 0, ssh OK, SELinux permissive. No guest reboot, no
re-provision. Evidence dirs `/root/evidence/cinnamon-attempt-2c2/`,
`cinnamon-attempt-2c2b/`, `cinnamon-attempt-2c3/` in place.

**What this establishes (hypothesis routing, per the 2c-2 "For 2c-3" note):**
PASS closes the input-layer suspect — the VM's Authentication Error was a
harness artifact (`ukey.c` keycode corruption), and the pre-fix Cinnamon RPMs
do not break GDM Wayland login in this configuration (GDM+GNOME baseline,
SELinux permissive, live install, no reboot). H1–H4, as explanations of the
VM failure, are closed with no PAM or packaging defect found. **Consequence
for the task (AGENTS.md §5, stated plainly):** the user's real failure was
typed by a human on a real keyboard, so this VM configuration does not
reproduce it, and no RPM fix is indicated by the VM evidence. The remaining
discriminating path is the user's own machine logs (plan risk R2: ask the
user for `journalctl -u gdm` + `/var/log/secure` from the real machine). This
changes the shape of item 2 from "reproduce, then fix the RPMs" to
"reproduction not achievable in-VM with a correct input layer; route on the
user's logs", and is recorded here for `Robotnik` to sequence the next
dispatch accordingly.

**Changes this run:**

| File | Change | Why |
|---|---|---|
| VM `/root/gdm-harness/{gdm-a11y.py,gdm-drive.sh,ukey.c}` | re-synced from clone `097702e` (scp, byte-identical to the committed files) | the committed textofext probe + caps pre-pass + ukey fix had to be in the VM |
| VM `/root/gdm-harness/ukey` | rebuilt (`gcc -O2 -Wall -Wextra`, 02:41 UTC, no warnings) | the in-VM binary predated the `ukey.c` fix; `gdm_build_driver` skips an existing binary, so the rebuild was manual |
| VM `/root/evidence/cinnamon-attempt-2c3/` | this run's evidence set appended to the dead session's pre/post files | always-capture per the harness design; the PASS evidence |

**Alternatives considered:** (a) trust the in-VM `ukey` binary (mtime 01:21
UTC, set by the dead session) without rebuilding — rejected: mtime cannot
distinguish a pre- from a post-fix build, and the functional readback would
then have tested an unknown binary; rebuilding from the committed source is
deterministic and one second. (b) run the login directly from the password
stage, skipping the pre-pass, to save time — rejected: the committed
`gdm_login` flow is the flow under test, and the pre-pass is the verification
that the password is not corrupted; skipping it would have weakened the PASS.
(c) leave the `gdmtest` session active after the run — rejected: "leave the
VM as found" means the greeter face list up; `loginctl terminate-session`
restored it and the greeter came back cleanly (session c4).

**Safeguard compliance:** 80-min bound met with ~37 min to spare (02:21:31 →
03:05 UTC); no step failed even once (no two-failure stop triggered); every
command output was truncated before entering context (`tail -c` ≤ 2000 on all
ssh commands); a11y probes printed only targeted readbacks (the `textofext`
value, visibility checks as exit codes); no large log was cat'd into context
(evidence files were grepped in the VM, ≤ 2 lines per grep).

### Fix batch A (Omega 1 high + 2 medium, 2026-08-30, `Tails`)

*Scope: `## Security` finding 1 (high: every channel ran
`StrictHostKeyChecking=no`), finding 2 (medium: fleet key blast radius),
finding 3 (medium: setup-repo.sh safety on unasserted ordering). One commit
per finding on `task-0008-gdm-auth`: finding 1 = `1c16045`, finding 2 =
`af3a9ff`, finding 3 = `cd6860c`; all pushed, remote branch = local HEAD
(verified `git ls-remote`: `cd6860cb79a76aeb0cf0e54f87efe1e5d1ce6b05`),
working tree clean.*

*Clone path (AGENTS.md §5): the brief names
`/home/howard/AI/projects/cinnamon-for-rocky10/`, which does not exist on
this host. The real clone is `/home/howard/Linux/projects/cinnamon-for-rocky10/`
(the path Shadow, Omega and Big all recorded); work happened there. No other
brief deviation.*

**Evidence that shaped the design (collected 2026-08-30 ~15:20–16:00 JST,
before any edit):**

- The cloud image
  `/var/lib/libvirt/images/cinnamon-test/Rocky-10-GenericCloud.qcow2` ships
  **no host keys**: `sudo virt-cat <image> /etc/ssh/` lists only
  moduli/ssh_config/sshd_config (no `ssh_host_*`).
- Guests generate host keys at first boot: in-guest journal shows
  `sshd-keygen@{ecdsa,ed25519,rsa}.service` running at boot; key mtimes =
  boot time.
- Two VMs from the same image present **different** keys in all three
  types: `ssh-keyscan` + `ssh-keygen -lf` on the standing `gdm-login-vm`
  (192.168.122.15) vs a fresh scratch VM (192.168.122.201), e.g. ed25519
  `SHA256:jhToRyI+...` vs `SHA256:fdmwjXC1...`. Consequence: no per-image
  key can be committed in advance.
- A running VM holds an exclusive qcow2 lock that blocks direct
  `qemu-img info`/`virt-cat` ("Failed to get shared write lock"); `cp` of
  the qcow2 + `virt-cat` of the copy works and yields exactly the keys the
  VM presents (extracted fingerprints == keyscan fingerprints, scratch VM).
  This is the seeding mechanism.
- OpenSSH command-line behavior, verified empirically:
  `-o UserKnownHostsFile=a,b` (comma list) and repeated
  `-o UserKnownHostsFile=` flags do **not** accumulate on the command line
  (only the first file is consulted); `-o HostKeyAlias=<name>` makes ssh
  look the pinned key up under `<name>` regardless of the connected IP and
  works for ssh, scp and `rsync -e`. Hence one pin file per connection.
- Re-`ssh-keyscan` of 192.168.1.103 from the PM host matches Big's
  checkpoint 2 fingerprints exactly (RSA-3072 `SHA256:OxbuXvwV...`, ECDSA
  `SHA256:NAvJMVH7...`, ED25519 `SHA256:kAu+xhNL...`), so the committed
  key material is the TOFU record.

**Pinning approach — alternatives considered (finding 1):**

- **Option A** (Omega's first option): commit a `known_hosts` with the
  cloud image's host keys, pinned under a stable `HostKeyAlias`. Rejected
  by the evidence above: the image ships no keys and each first boot
  generates new ones; there is no per-image key to commit.
- **Option B**: per-VM pin file seeded *from the network* (ssh-keyscan the
  fresh VM into `vm-test/results/`). Rejected: the seed would be read over
  the same untrusted channel the pin protects — a MITM's key would get
  pinned (TOFU re-introduced by another door).
- **Option C (chosen)**: per-VM pin file seeded **out-of-band** — `cp` the
  qcow2 (the lock forces a copy; measured ~7 ms warm) + `virt-cat` the
  three `ssh_host_*_key.pub` from the copy, validate each with
  `ssh-keygen -lf`, write `vm-test/results/known-hosts/<vm-name>`
  (gitignored, per Omega's "keep it under `vm-test/results/`"). The
  provisioner's wait loop seeds first, then probes with
  `StrictHostKeyChecking=yes` + `HostKeyAlias=<vm-name>`: **no connection
  ever runs with verification off, including the first one**; the trust
  anchor is the host's own storage, not the LAN. Alias (not IP) pinning
  because VM IPs are DHCP-assigned and can change across reboots
  (`reboot_and_wait` already re-resolves them). A missing pin file is a
  hard error on non-wait channels (fail-closed), and "not ready yet"
  inside wait loops while the guest boots.
- **Option D**: generate a host keypair on the PM host and inject it into
  the image at provision time (virt-customize), pinning to it. Rejected for
  this batch: a file created by the libguestfs appliance in `/etc/ssh/`
  risks a wrong SELinux context on a targeted image (sshd is confined; a
  mismatch breaks sshd at boot) — a new failure mode in a load-bearing
  provisioning step. Option C gives the same guarantee (no unpinned
  connection) without touching image customization.
- **Option E**: per-VM static DHCP leases (pin by IP). Rejected: changes
  provisioning (MAC/lease management), breaks the orphan/`--ip` attach
  mode, and still needs per-VM files.
- Residual exposure (accepted): none in the evidence chain. Every verdict
  input (PHASE_RESULT probes, scp/rsync of rpms and evidence, dnf output)
  flows over a pinned channel; a MITM can only stall provisioning (answer
  nothing), not forge a key, because the pinned key comes from the disk.
- **Stale-pin hazard found and fixed during verification**: a re-provision
  under the same VM name generates new guest keys, so all destroy paths
  (`destroy_vm` in provision-vm.sh and test-repo-setup.sh,
  `destroy_single_vm` in validate-install.sh) now remove the pin file with
  the disk. The first cold-start test failed for exactly this reason
  (stale pin from the pre-fix run; 120 s of pinned-probe failures), then
  passed after the fix (ready in 5 s).

**Changes (per finding):**

| File | Change | Why |
|---|---|---|
| `vm-test/known_hosts` (new) | committed pin file: 192.168.1.103's three host keys (TOFU fingerprints) + policy header documenting the VM seeding model | the bare-metal host key must be committed; VM keys cannot be (per-boot) |
| `vm-test/lib.sh` (f1) | pinning machinery: shared `IMG_DIR`, `KNOWN_HOSTS_FILE`, `VM_PIN_DIR`, `BAREMETAL_HOST`, `vm_pin_file()`, `seed_vm_pin()` (out-of-band cp+virt-cat seeding, keys validated), `ssh_pin_opts()` (fail-closed), `ssh_cmd()` pinned | single shared source for the pinning |
| `vm-test/provision-vm.sh` (f1) | `wait_for_ssh` seeds then probes pinned; `destroy_vm`/`--destroy-only` remove the pin file; `IMG_DIR` moved to lib.sh; header updated | cold-start first contact pinned; a stale pin must not outlive its VM |
| `vm-test/test-gdm-login.sh` (f1) | `try_ssh` seeds then probes pinned; 3 scp sites pinned; attach branch fails closed up front for un-pinnable targets (no pin file and no seedable disk); header documents the attach pin requirement | every channel pinned; legacy/orphan attach is fail-closed, not silent |
| `vm-test/test-repo-setup.sh` (f1) | `wait_for_ssh` seeds then probes pinned; 2 rsync sites pinned; `destroy_vm` removes the pin file | same |
| `vm-test/run-tests.sh` (f1) | 2 scp sites pinned | same |
| `vm-test/test-quick-install.sh` (f1) | 1 scp site pinned | same |
| `vm-test/test-step-by-step-install.sh` (f1) | 1 scp site pinned | same |
| `vm-test/validate-install.sh` (f1) | now sources lib.sh; `wait_for_vm` seeds then probes pinned (per-vm-name alias); `destroy_single_vm` removes the pin file | last self-contained script brought under the shared machinery |
| `vm-test/lib.sh` (f2) | `assert_ssh_key()` (exists, owner = invoking user, no group/other bits; 600 standard, 400 accepted — ssh's own requirement; once per key per process) called from `ssh_cmd` on every channel; `BAREMETAL_USER`/`BAREMETAL_KEY`; `ssh_cmd` target-aware (BM: howard + dedicated key; VM: root + fleet key); header states the credential blast radius | finding 2(a) permission checks, (b) dedicated-key wiring, (c) blast-radius statement |
| `vm-test/provision-vm.sh` (f2) | `check_prereqs` calls `assert_ssh_key` before the fleet key is injected | fail fast at provision time |
| `vm-test/test-repo-setup.sh` (f2) | `provision_vm` calls `assert_ssh_key` before injecting the fleet key | its own provisioner path |
| `vm-test/validate-install.sh` (f2) | `provision_single_vm` calls `assert_ssh_key` before injecting the fleet key | its own provisioner path |
| `vm-test/test-repo-setup.sh` (f3) | phase 0 test 3 now snapshots host state before the root run (createrepo_c presence, `cinnamon-rocky10.repo` presence, md5sum of every `/etc/yum.repos.d/*.repo` — also catches a CRB enable — and files created/modified under the working tree's `rpms/` since a timestamp marker) and records a new "Error-path statelessness" check (FAIL + diff on any change) | asserts statelessness instead of relying on the unasserted ordering |
| `repo-setup/setup-repo.sh` (f3) | header documents the statelessness contract and the load-bearing ordering (error path must die at project-root resolution before any state-changing step) | the contract is visible to the future editor whose one-edit-away refactor would break it |

**Checks run:**

- `bash -n` on all 9 touched scripts: PASS.
- `shellcheck 0.10.0 --external-sources` on all 9: 0 errors; warnings =
  pre-existing classes only (SC2034 `setup_rc`/`SYSTEM_DEPS`/`install_rc`,
  SC2046 `test-repo-setup.sh:212` [pre-existing, line shifted], SC2034
  `IMG_DIR` false positive in the shared lib, SC1091 source-follow
  tooling artifacts) — nothing new vs Big's baseline.
  `repo-setup/setup-repo.sh`: clean.
- `grep -rn 'StrictHostKeyChecking=no' vm-test tasks repo-setup` → 0 hits.
- Live, scratch VM `t0008-keycheck-vm` (provisioned for this, destroyed at
  the end): cold provision with the new `provision-vm.sh` — first ssh
  pinned, "SSH is ready on 192.168.122.215 after 5s (host key pinned from
  ...)"; pinned scp + rsync round-trips via `SSH_PIN_OPTS`; fail-closed for
  an unpinned target (`[lib] ERROR: no pinned host key ...`, rc=1).
- Live, legacy path: `gdm-login-vm` (old code, still running for the
  re-run) was refused before seeding and connected after one
  `seed_vm_pin` from its own disk; its pin file
  (`vm-test/results/known-hosts/gdm-login-vm`) is kept for the re-run's
  attach flow.
- Live, 192.168.1.103 (read-only: `echo` + `hostname` only, machine state
  untouched): pinned ssh via the committed `known_hosts` → `silver`,
  rc=0; negative control with `/dev/null` known_hosts → "Host key
  verification failed", rc=255, refused before auth.
- Finding 2, unit: `assert_ssh_key` — 600/own key passes; a 644 key →
  mode error rc=1; a root-owned key → owner error rc=1;
  `ssh_cmd 192.168.1.103` connects as `howard@silver` with the dedicated
  key (fleet key not presented).
- Finding 3, live on the host (phase 0 executed via a `/tmp` copy of the
  script with `main` replaced by `test_error_handling`; no VM
  provisioning): 9/9 PASS including the new statelessness check.
  Regression simulation: a copy of `setup-repo.sh` with a state-changing
  step (canary file in `/etc/yum.repos.d/`) inserted before
  project-root resolution → the error-message check still PASSes while the
  statelessness check records FAIL with a diff, proving detection is
  independent of the script's output. Canary removed afterwards; host state
  verified restored (repo file list, createrepo_c presence, `rpms/`
  unmodified).
- Push verification: `git ls-remote` remote branch == local HEAD
  `cd6860c`; local `origin/task-0008-gdm-auth` ref updated to match (it was
  not advanced by the URL push).

**Not verified (boundaries of this batch):**

- No full `test-gdm-login.sh` or `test-repo-setup.sh` VM-phase re-run —
  that is Big's re-run, which exercises these pinned paths end to end.
  The individual channels they use are verified live above.
- `validate-install.sh`, `run-tests.sh`, `test-quick-install.sh`,
  `test-step-by-step-install.sh` full flows: syntax + lint + shared channel
  code only; not provisioned here (would be 2+ VMs).
- The dnf metadata cache is deliberately outside the statelessness
  assertion (transient by design; rewritten by any concurrent dnf). A
  regression that reached only `dnf makecache` on the host — no repo file,
  no package, no working-tree change — would not be caught; the three
  persistent state classes are.
- `ssh_pin_opts` defaults the alias to the script's `VM_NAME`: a manually
  passed IP belonging to a *different* VM fails the pin (visible error)
  rather than cross-connecting silently.
- The bare-metal *client* key fingerprint
  (`SHA256:CvnIXRjnu7QUErfiExqbQ3q5zncY8ZPCLXo3PZ6TTSM`, Big's checkpoint
  2) is a record for `## Docs` (Vector's section — untouched per dispatch).
  The `known_hosts` entries are host keys, not client keys.
- `## Security` Resolution lines: not filled (dispatch: write only to
  `## Implementation`); the shas above (`1c16045` / `af3a9ff` / `cd6860c`)
  are what the re-run cites.

**Observation for `Robotnik`:** the token embedded in the `origin` URL is
stale — `git push origin` fails with "Invalid username or token". The
pushes in this batch went through a plain
`https://github.com/metalllinux/cinnamon-for-rocky10.git` URL via the
configured credential helper (`credential.https://github.com.helper` →
`~/token.md`, valid; `gh auth status` shows the separate `GH_TOKEN` env var
is also invalid). The origin URL was left as-is per the user's
2026-08-21 decision.

### Fix batch B (Tails, 2026-08-30)

Shadow's five verdict-integrity findings (#3, #4, #7, #8, #9 in
`## Review`), one commit each, on `task-0008-gdm-auth` atop batch A
(`cd6860c`). Clone `~/Linux/projects/cinnamon-for-rocky10/` (the
brief's `/home/howard/AI/projects/cinnamon-for-rocky10/` path does
not exist on the runner; same branch, same commits, per Shadow's
note in `## Review`).

| # | Fix | Commit |
|---|---|---|
| 3 | remote rc checks, `vm-test/test-repo-setup.sh` | `85f629e` |
| 4 | teardown rc, `vm-test/provision-vm.sh` + `vm-test/test-gdm-login.sh` | `921de9f` |
| 7 | `waiteditable` dispatch, `tasks/lib/gdm-a11y.py` | `9ce6cb5` |
| 8 | `gdm_login_and_verify`, `tasks/lib/gdm-drive.sh` | `6f6b1b5` |
| 9 | a11y wait loops, `tasks/lib/gdm-a11y.py` | `f259dd5` |

**#3 — rc checks (`85f629e`).** The three remote rc checks at
`vm-test/test-repo-setup.sh:400,548,589` (the review's 311/459/500,
shifted by batch A) used `echo "$rc" | grep -q "0$"`, which matches
any code whose last digit is 0 (rc 10/20/30 → PASS with the literal
detail "exit code 0"). Now `[ "$rc" = "0" ]` at all three sites
(setup-repo.sh execution, `dnf install cinnamon`, `dnf install` of
the extra packages); the ssh-failure sentinel 255 needs no special
case — any value other than exactly 0 falls through to FAIL.
Alternatives considered: a shared `rc_is_zero` helper (rejected, the
comparison is one line and a helper adds indirection); capturing the
rc over the same ssh as the captured output (rejected, out of scope —
the double-remote-run pattern predates this fix and re-running
setup-repo.sh is idempotent). Verified: `bash -n`; `shellcheck -S
warning` shows only the two pre-existing findings (SC2046 line 248,
SC2034 `setup_rc` line 387 — both present on the stashed
pre-batch-B tree); truth table over rc 0/1/10/20/30/255 → PASS only
for 0.

**#4 — teardown rc (`921de9f`).** `provision-vm.sh --destroy-only`
now (a) proves libvirt is reachable (`virsh list --all`) before
anything else, so a permission failure on the system driver cannot
read as "VM not present"; (b) after the destroy, verifies the domain
is actually gone (`virsh domstate`) and the disk file is gone,
exiting non-zero with the observed domstate when either still
exists. The idempotent "missing VM is a success" path is unchanged.
`test-gdm-login.sh` records PASS/FAIL from that rc (the destroy
output is captured into the failure detail instead of `>/dev/null`),
exits 1 on a teardown that cannot verify the VM is gone (header
exit-code note updated in the same commit), and `write_summary`
moved after the teardown block so the teardown verdict is persisted
in `summary.txt` (previously the summary ran before the teardown
record, so the record only reached `run.log`). Alternatives
considered: making `destroy_vm` itself return a meaningful rc
(rejected — its `|| true` exists for idempotent re-runs on the
pre-provision path, and the post-hoc `domstate` is the state-based
verdict this harness is built around; it catches both destroy and
undefine failure modes, e.g. the busy-disk case). Verified: `bash -n`
both files; `shellcheck -S warning` clean both; hermetic PATH-shim
runs of `--destroy-only` (no real libvirt state touched): ghost
domain absent → rc 0; libvirt unreachable → rc 1 "cannot query
libvirt"; destroy failing with the domain surviving → rc 1 "still
present after destroy (domstate: running)"; the harness rc-capture
idiom under `set -euo pipefail` on both outcomes (no set -e abort on
the failure path; output preserved for the detail line).

**#7 — `waiteditable` (`9ce6cb5`).** Deleted the dispatch at
`tasks/lib/gdm-a11y.py:516-517` (`cmd_waiteditable` defined nowhere,
absent from the docstring's command list; the branch raised
NameError). Deleted rather than implemented (Shadow's two stated
options): the verified in-VM evidence (item 2c-3, recorded in the
`gdm_caps_probe_normalize` comment, `tasks/lib/gdm-drive.sh:349-350`)
shows the greeter's a11y state sets come back EMPTY for every node,
so an editable-state-based wait has no basis on the gdm-47 Wayland
greeter; the verified entry targeting is point-based
(`findrolex`/`textofext`). Verified: zero `waiteditable` references
repo-wide (`grep -rn`); `py_compile` clean; `gdm-a11y.py
waiteditable` now exits 1 with the usage doc (was: NameError
traceback).

**#8 — `gdm_login_and_verify` (`6f6b1b5`).** `gdm_login`'s rc is
propagated on non-zero before any wait (`tasks/lib/gdm-drive.sh`,
the `gdm_login_and_verify` block), with an explicit "credentials not
submitted" diagnostic: rc 2 (session not selectable), 3 (no login
surface), 4 (caps pre-pass failed) no longer surface as "no verified
session after 120s". Return codes documented on the helper:
gdm_login's 2/3/4 on abort, otherwise gdm_wait_session's (0
verified, 3 no session appeared, 4 session without the expected
process). Kept rather than deleted (Shadow's alternative): the file
header names the Sparky/Sparrow matrix (9a/TASK-0015) as the
intended consumer and the fixed helper is a safe convenience; a
repo-wide search confirmed zero callers either way (verified, not
assumed). Verified: `bash -n`; `shellcheck -S warning` shows only
the two pre-existing SC2034s in `gdm_caps_probe_normalize` (lines
461/476); boundary stub test with `gdm_login`/`gdm_wait_session`
stubbed at the rc level: rc 2/3/4 propagate with the wait skipped;
rc 0 proceeds and returns the wait's rc (0/3/4) — 6/6 checks pass.

**#9 — a11y wait exception swallow (`f259dd5`).** A second gap found
while fixing: `connect()` and `greeter_nodes()` exited via
`sys.exit` inside the poll loop, so a transient channel blip (the
greeter still coming up) aborted the wait on its first poll; and the
`except Exception: pass` meant a persistently raising channel was
indistinguishable from "node never appeared" (all failure modes
converged on bare rc 1). Design: `ChannelError` (new) marks channel
failures; `connect()` and `greeter_nodes()` raise it instead of
`sys.exit`; the four wait commands are thin probes over a shared
`wait_for()` that counts raising polls and remembers the last
exception, polls to the deadline, and exits the timeout with one of
two diagnostics — "a11y channel broken during wait (N failed
poll(s), last: ...)" vs "target never appeared". Non-wait commands
are behavior-preserved: `main()` converts `ChannelError` to the
byte-identical exit message as before (verified, test T6/T6b).
Alternatives considered: per-command try/except instead of the
shared helper (rejected — four copies of the same loop is where the
finding lived); counting failures without keeping the last exception
(rejected — the last exception is the diagnostic that points at the
journal). Verified: `py_compile`; module test suite 7/7 (target-
absent timeout; channel-broken timeout with the last exception;
transient blip then success; waitvis success prints the find-format
line; ChannelError reported at timeout; non-wait message
preservation for `tree` and `has`; unknown command is a usage exit);
end-to-end CLI run against the absent in-VM a11y bus on this host:
`wait "Not listed?" 2` exits 1 after 2.0s with the channel-broken
diagnostic and the real `DBusException` as the last error (old code:
immediate abort on the first poll).

**Checks run (batch B).** `bash -n` on all four touched shell
scripts: clean. `shellcheck -S warning` on all four: only the four
pre-existing warnings (test-repo-setup.sh SC2046:248, SC2034:387;
gdm-drive.sh SC2034:461, SC2034:476), all present on the stashed
pre-batch-B tree. `python3 -m py_compile tasks/lib/gdm-a11y.py`:
clean (pyflakes is not installed on the runner). Per-finding
functional tests as above (shimmed `virsh`, stubbed driver boundary,
monkeypatched channel boundary): no real libvirt domain, VM, or
network target was touched; the one live smoke test was read-only (a
2s wait against the absent in-VM a11y bus socket). Batch A
compatibility: `git diff cd6860c..HEAD -- vm-test/lib.sh
vm-test/known_hosts` empty; every `ssh_pin_opts`/`seed_vm_pin`/
`StrictHostKeyChecking=yes` call site intact in the touched files;
no batch B diff line touches a pinning or ssh-option line.

**Competing priorities.** #4: exit-1 on teardown failure stretches
the header's original contract ("1 when a harness phase failed
*before it could produce its evidence*"); the contract note was
updated in the same commit because a surviving domain reported as
destroyed is the false-PASS class this batch exists to remove. #9:
the wait commands now emit a stderr line on timeout (previously bare
rc 1); all current callers redirect stderr, so no caller behavior
changes — the line is for the operator running the tool by hand. #8:
kept the helper over Shadow's deletion alternative to give the
coming Sparky suite a safe convenience; dead-code risk is bounded by
the now-correct semantics.

**Not verified (could not).** No full `test-gdm-login.sh` or
`test-repo-setup.sh` run: that requires a provisioned VM and is Big's
re-run (Next Actions); verified instead is the changed verdict logic
in isolation (shim/stub/boundary tests) plus syntax and lint.
`--destroy-only` against a real surviving domain: exercised via the
shim only; the real-libvirt path of the post-verify `domstate` was
deliberately not run (destroying a real domain as a test would
disturb the running fleet state). #7/#9 in-guest behavior against a
live greeter: the module tests exercise the same code paths with a
synthetic channel; the in-guest re-run (Big) confirms against the
real greeter.

**Note for `Robotnik`:** pushed. `origin/task-0008-gdm-auth` =
`f259dd5` (verified by fetch after the push; same plain-URL push
method as batch A's note, since the `origin` URL's embedded token is
stale). `## Review` Resolution lines left unfilled per the write-
only-to-`## Implementation` dispatch; the shas above are what the
re-run cites.

---

## Review

*Owner: `Shadow`. Read-only — findings only, no edits. Severity order, blockers first.*

*Executed 2026-08-30 by `Shadow`. Scope: `git diff main..task-0008-gdm-auth` (5 commits
`b15dfcb`..`097702e`, 9 files, 3394 insertions / 6 deletions). Verified with `git status`
(clean tree on `task-0008-gdm-auth`, = origin) and `git log --oneline main..task-0008-gdm-auth`
(the five commits named in the brief). The working clone is
`~/Linux/projects/cinnamon-for-rocky10/` (per `## Status` and `vm-test/lib.sh:29`), not
`~/AI/projects/cinnamon-for-rocky10/` as the brief states; same branch, same commits.*

*What is good, plainly: the evidence discipline in `gdm-drive.sh` (capture on both outcomes,
state-based verdicts, the caps pre-pass verified by AT-SPI readback before any credential is
sent) is the design the plan asked for; the test password is generated in the VM and never
leaves it; `gdm_ensure_greeter` plus the `--destroy` flags make re-runs idempotent, and the
superseded paths are annotated with the evidence that killed them. The findings below are the
gaps. No blocker found; nothing here invalidates the 2c-3b PASS (the verified run used the
QMP screenshot channel and lowercase hex input, so findings 1 and 2 could not have bitten).*

### vnc-grab.py decodes pixel bytes with the endianness inverted
**Severity:** should-fix
**Where:** `tasks/lib/vnc-grab.py:118`
**Problem:** `fmt = ">I" if not pixfmt["big_endian"] else "<I"` maps the RFB big-endian flag
to the wrong struct format; a server that advertises little-endian pixel data (flag 0, which
is what QEMU's VNC server sends on an x86 host: flag 0 plus host-byte-order pixel data) is
decoded as big-endian.
**Failure scenario:** any `vnc-grab.py <host> 5900 out.png` against a QEMU VM. For the
standard 32bpp format (shifts 16/8/0, maxima 255), a wire pixel `[B,G,R,A]` is read as
`0xBBGGRRAA`, so every screenshot comes out with red and green swapped and blue pinned to
255. The tool is the documented pixel channel for domain-less VMs and for any VM that
exposes a VNC display, so TASK-0015 runs would collect corrupted evidence that looks
plausible. The 2-byte path (`tasks/lib/vnc-grab.py:138`) inherits the same `fmt`.
**Suggested direction:** invert the mapping (flag 1 means the pixel data is big-endian, so
flag 1 takes `>I`), and sanity-check the decode against a known pattern once.
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

### ukey `type` silently drops uppercase letters
**Severity:** should-fix
**Where:** `tasks/lib/ukey.c:182` (guard at `tasks/lib/ukey.c:153`, skip at `tasks/lib/ukey.c:423-428`)
**Problem:** `case 'A' ... 'Z'` sets shift and calls `letter_to_key(c)`, but `letter_to_key`
rejects every non-lowercase input (`c < 'a'` is true for 'A'-'Z'), so the case range always
returns -1 and the type loop skips the character with no diagnostic.
**Failure scenario:** the first time a password contains an uppercase letter (the current
hex charset never does, which is why 2c-3b did not catch it): `ukey type aBc` emits only
`ac`; the login fails at PAM with no hint that one character was never sent. This is the
same silent-corruption class that cost 2c-2.
**Suggested direction:** lowercase the character before the table lookup so the shift cases
actually work, or delete the 'A'-'Z' cases and document that `type` is lowercase-only;
either way, warn on stderr when a character is dropped.
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

### test-repo-setup.sh records PASS for any exit code that ends in 0
**Severity:** should-fix
**Where:** `vm-test/test-repo-setup.sh:311, 459, 500`
**Problem:** the three remote rc checks use `echo "$rc" | grep -q "0$"`, which matches every
non-zero code whose last digit is 0, and the `!= 255` guard does not cover that case.
**Failure scenario:** the second `dnf install` pass exits 10 (a transaction failure):
`grep -q "0$"` matches, the guard passes, and the check is recorded PASS with the literal
detail "exit code 0" while the install failed; the run can exit 0 on a broken install.
**Suggested direction:** compare the value directly, e.g. `[ "$install_rc" = "0" ]`; the
ssh-failure sentinel 255 then needs no special case.
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

### test-gdm-login.sh records "teardown PASS" unconditionally
**Severity:** should-fix
**Where:** `vm-test/test-gdm-login.sh:678-679`
**Problem:** the destroy call swallows output and rc (`bash ... --destroy-only >/dev/null 2>&1 || true`),
and `--destroy-only` itself always exits 0 (its inner `virsh destroy`/`undefine` lines carry
`|| true`, see `vm-test/provision-vm.sh:125-133`), so the PASS record prints whether or not
the VM actually went away.
**Failure scenario:** the runner lacks permission on the libvirt system driver (see the
prerequisites finding below) or the disk is busy: the domain survives, the summary says
"teardown PASS - VM destroyed", the run exits 0, and the next operator starts from a phantom
state; repeated runs accumulate 4GB disks against the plan's one-VM-at-a-time guard.
**Suggested direction:** make `--destroy-only` verify the domain is actually gone afterwards
(`virsh domstate`) and return non-zero when it is not, and let the harness record
PASS/FAIL from that rc instead of `|| true`.
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

### Required host prerequisites are neither documented nor checked
**Severity:** should-fix
**Where:** `vm-test/lib.sh:18-19`, `vm-test/provision-vm.sh:44-50`
**Problem:** the harness forces `LIBVIRT_DEFAULT_URI=qemu:///system` (the comment says the
session pool has no networks) and assumes the invoking user can talk to the system driver,
can write `/var/lib/libvirt/images/cinnamon-test/`, and has passwordless `sudo`
(`vm-test/test-repo-setup.sh` phase 0 runs `sudo bash setup-repo.sh`); `orphan_vm_ip`
additionally assumes `jq` (`vm-test/test-gdm-login.sh:188`). `check_prereqs` verifies
binaries, the cloud image, and the SSH key, but none of these.
**Failure scenario:** a new team member (or the runner user on a reinstalled host) runs
`test-gdm-login.sh` without libvirt group membership: every `virsh` call fails quietly
(most call sites redirect stderr) and the run dies at "no IP after provisioning" with no
hint that permissions are the cause. The 2026-08-26 entry in `## Status` records exactly
this failure mode on this host (unsuffixed `virsh` saw the empty user session).
**Suggested direction:** add canaries to `check_prereqs` (a `virsh list --all` against the
forced URI, a write test for the image dir, `command -v jq` on the orphan path) and list the
prerequisites in the script headers.
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

### Hardcoded "48 RPMs" in the copy check
**Severity:** should-fix
**Where:** `vm-test/test-repo-setup.sh:277`
**Problem:** the expected RPM count is a magic number, while the 14-package list below it
degrades to WARN on version drift by design, so the two checks disagree about what is
acceptable.
**Failure scenario:** TASK-0015 lands one extra RPM in `rpms/` (or a rebuild drops one): the
check fails with "expected 48 RPMs, found 49" on a perfectly good copy, and the operator
must edit the script to discover that the set changed.
**Suggested direction:** count `rpms/*.rpm` locally and compare local vs remote counts;
that also detects a truncated rsync, which is what this check exists for.
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

### gdm-a11y.py dispatches a command that does not exist
**Severity:** should-fix
**Where:** `tasks/lib/gdm-a11y.py:516-517`
**Problem:** `main()` routes `waiteditable` to `cmd_waiteditable`, which is defined nowhere
in the file (and is absent from the docstring's command list), so the branch raises
NameError. A repo-wide search for `waiteditable` finds only this dispatch.
**Failure scenario:** anyone who tries `gdm-a11y.py waiteditable ...` (a plausible name
given the a11y state API, and the obvious next probe when a state-based lookup misbehaves)
gets a Python traceback instead of a usage or timeout exit.
**Suggested direction:** delete the dispatch (the greeter's state sets come back empty per
the verified in-VM evidence, so the command has no basis), or implement it if the a11y
suite needs it.
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

### gdm_login_and_verify hides a no-credentials abort behind a 120s wait
**Severity:** should-fix
**Where:** `tasks/lib/gdm-drive.sh:661-665`
**Problem:** the helper runs `gdm_login ... || true` and then unconditionally waits
`GDM_LOGIN_WAIT` for a session, so gdm_login rc 2 (requested session not selectable,
credentials deliberately not submitted) and rc 3/4 (no login surface) all surface as "no
verified session after 120s".
**Failure scenario:** a Sparky task in 9a/TASK-0015 calls it with `cinnamon-wayland` on an
install that lost the wayland session file: no credentials are ever sent, but the caller
reads the result as a failed login and starts hunting PAM, repeating the 2c-2 misdiagnosis
this task exists to prevent.
**Suggested direction:** propagate the gdm_login rc on non-zero before waiting, or delete
the helper (a repo-wide search finds no caller).
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

### The a11y wait loops swallow every probe exception
**Severity:** should-fix
**Where:** `tasks/lib/gdm-a11y.py:321-324` (same pattern at lines 373, 394, 431)
**Problem:** `cmd_wait`, `cmd_waitvis`, `cmd_waitvisrole`, `cmd_waitvisrolex` catch
`Exception` and `pass` inside the poll loop, so a persistently broken a11y channel (bus up
but queries raising) is indistinguishable from "the node never appeared".
**Failure scenario:** the greeter process dies mid-poll and AT-SPI queries raise every
second: after the timeout the harness reports "greeter a11y UI not ready ('Not listed?' not
visible after 60s)", pointing the operator at a missing UI node while the real fact (greeter
process dead, visible in the journal) never surfaces in the harness output.
**Suggested direction:** remember the last exception (or count failures) and include it in
the timeout exit path, so "channel broken" and "node absent" are separate diagnostics.
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

### test-repo-setup.sh carries a second provisioning implementation
**Severity:** should-fix
**Where:** `vm-test/test-repo-setup.sh:71-161` (duplicates `vm-test/provision-vm.sh:52-79`)
**Problem:** the script re-implements `destroy_vm`, `wait_for_ssh`, and full
`virt-customize`/`virt-install` provisioning with its own `CLOUD_IMAGE`/`DISK_PATH`/`VCPUS`/
`MEMORY` constants (lines 30-35), instead of calling `provision-vm.sh`, which this same
branch extended with the `--name` flag it needs.
**Failure scenario:** a future fix to provisioning (image path, firewall masking, IP wait)
lands in `provision-vm.sh` only; `test-repo-setup.sh` keeps the old behavior and starts
failing or passing differently with no visible reason. The copies already diverge
(separate SSH wait timeouts and log files).
**Suggested direction:** call `provision-vm.sh --destroy --name cinnamon-test-repo` and
drop the local copies and duplicated constants.
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

### vnc-grab.py truncates the server's refusal reason to one byte
**Severity:** nit
**Where:** `tasks/lib/vnc-grab.py:73`
**Problem:** the SecurityResult reason length is a 4-byte big-endian value, but the code
reads it as `recv_exact(sock, 4)[0]`, i.e. the high byte.
**Failure scenario:** a VNC server with a password set refuses the zero-password response
with a short reason: the high byte is 0, so the error prints "server refused connection: "
with an empty reason and the operator cannot tell why.
**Suggested direction:** unpack the 4 bytes as `>I` before reading that many bytes.
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

### Zero-package repo yields a garbled count in test-repo-setup.sh
**Severity:** nit
**Where:** `vm-test/test-repo-setup.sh:395`
**Problem:** `grep -c` prints "0" and exits 1 on no match, so `|| echo "0"` appends a second
line and `pkg_count` becomes "0\n0".
**Failure scenario:** the repo is broken and lists no packages: the `-ge 30` test errors
with "integer expression expected" on stderr and the FAIL detail reads "only 0\n0 packages".
The verdict is still FAIL, but the evidence line is unusable.
**Suggested direction:** drop the `|| echo "0"` (grep -c already prints 0) or normalize the
captured value.
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

### gdm_caps_lock_off has no callers
**Severity:** nit
**Where:** `tasks/lib/gdm-drive.sh:307-325`
**Problem:** the superseded LED-driven toggle is kept "for callers that only have the LED",
but no caller exists (a repo-wide search finds only the definition and a cross-reference
comment).
**Failure scenario:** none today; the risk is a future caller reaching for the superseded
path and reintroducing the blind-toggle behavior that 2c-2 proved wrong.
**Suggested direction:** delete it, keeping the documented history in the comment above
`gdm_caps_probe_normalize`.
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

### Leftover narration comment in provision_vm
**Severity:** nit
**Where:** `vm-test/test-repo-setup.sh:99-100`
**Problem:** "# Use the standard VM name from lib.sh for provisioning, then rename /
Actually, let's use our own VM name directly" is decision narration, and the first clause
is wrong about what the code does.
**Failure scenario:** none; a reader gets a false statement of intent in the code.
**Suggested direction:** replace with a one-line statement of what is done (dedicated VM
name so this test does not clobber `cinnamon-test-vm`).
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

### The 1280x800 coupling is spread over three places with no cross-check
**Severity:** nit
**Where:** `tasks/lib/ukey.c:85-86` (ABS range), `tasks/lib/gdm-drive.sh:352-354, 417` (fixed probe point)
**Problem:** the absolute pointer range, the caps-probe point, and the a11y extents all
assume the greeter's 1280x800 framebuffer, and nothing cross-checks them at run time.
**Failure scenario:** a greeter running at another resolution: absmove either dies with a
range error (points beyond 1279x799) or, for in-range points, lands at a scaled position,
so the probe misses the entry and the attempt aborts. All three failures are loud, so this
is fragility, not a silent bug.
**Suggested direction:** read the a11y root panel extents at start and verify they match the
ukey range, failing with a named mismatch.
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

### run.log may lose its final lines
**Severity:** nit
**Where:** `vm-test/test-gdm-login.sh:319`
**Problem:** `exec > >(tee ...)` spawns an async tee the script never waits for; bash can
exit before the subshell's buffer drains.
**Failure scenario:** a run that ends at teardown or in the final log lines: `summary.txt`
and `run.log` are missing the last few lines (the teardown record is exactly such a line),
so the persisted evidence understates what happened.
**Suggested direction:** wait on the process substitution before exiting (bash 4.4+), or
log to the file directly and drop the exec-tee.
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

### ukey's exit codes do not match its contract, and the wrappers ignore them
**Severity:** nit
**Where:** `tasks/lib/ukey.c:57, 88`, `tasks/lib/gdm-drive.sh:214-216`
**Problem:** the header promises "0 ok, 2 usage error, 3 device error", but `die()` (used
for a failed `write()` on the device) exits 2, and `gdm_type`/`gdm_key`/`gdm_click` discard
the rc entirely.
**Failure scenario:** a /dev/uinput write fails mid-password: ukey exits 2 (looks like a
usage error), the driver wrapper ignores it, and the harness proceeds to a PAM rejection
that the evidence must then explain by hand. The caps pre-pass catches pipeline breakage
before credentials, which is why this stayed latent.
**Suggested direction:** give device write failures the documented 3, and have the wrappers
check the rc and return it.
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

**Verdict (2026-08-30): 0 blockers, 10 should-fix, 7 nits.** The should-fixes are small and
local. Findings 3, 4, 5, and 8 are the ones that can produce a wrong verdict or a
misleading diagnosis (a PASS on a failed install, a PASS on an undestroyed VM, a
permissions failure masquerading as a provisioning failure, and a no-credentials abort
masquerading as a login failure); the rest are latent or cosmetic. The DoD's Shadow gate
applies to all ten should-fixes.

---

## Security

*Owner: `Omega`. Read-only. Severity order.*

*Executed 2026-08-30 by `Omega`. Scope: `git diff main..task-0008-gdm-auth` (5 commits
`b15dfcb`..`097702e`, 9 files, 3394 insertions / 6 deletions). Verified with `git status`
(clean tree on `task-0008-gdm-auth`, = origin) and `git log --oneline main..task-0008-gdm-auth`
in the clone `~/Linux/projects/cinnamon-for-rocky10/` (the brief's `~/AI/projects/` path does
not exist; same branch and commits as Shadow's note). All nine diff files read in full.
Deployment context per `## Status`: the harness merges to main and will also drive the
bare-metal host `howard@192.168.1.103`; the `~/pass.txt` password is never referenced in the
diff (`git grep -iE 'pass\.txt|192\.168\.1\.' task-0008-gdm-auth -- vm-test tasks .gitignore`
returns nothing).*

*Clean, briefly: no secrets committed anywhere in the branch (`git grep` for private-key
blocks, GitHub token patterns, `192.168.1.x`, `pass.txt` across the whole tree returns no
hits); the origin-URL token (user decision, `## Status`) sits in untracked `.git/config` and
the harness never runs `git remote` or echoes it. The test password is generated in the
guest, chmod 600, and never leaves the VM: the phase-9 scp collects only `/root/evidence`
(`vm-test/test-gdm-login.sh:664-666`) while the pass file lives at `/root/gdmtest.pass`
(`vm-test/test-gdm-login.sh:434-436`). The `ukey` build interpolates no untrusted input into
gcc (`tasks/lib/gdm-drive.sh:81`); the C file range-checks its coordinates
(`tasks/lib/ukey.c:473-488`) and commits no binary. In-VM scripts travel as quoted heredocs
(`vm-test/test-gdm-login.sh:387` et seq.), so no host-side expansion; the one dynamic
argument (`SELINUX_MODE`) is allowlisted (`vm-test/test-gdm-login.sh:292-295`). The
`--graphics vnc` console is bound to 127.0.0.1 by libvirt default (the generated XML carries
no `listen` attribute; I did not verify the live domain XML) and the greeter framebuffer
holds no secret (the password field is masked, `tasks/lib/gdm-a11y.py:43-49`).*

### Every harness channel runs with host-key verification off; the evidence chain is forgeable by an on-path attacker
**Severity:** high
**Vector:** crypto
**Where:** `vm-test/lib.sh:39` (`ssh_cmd`, consumed at `vm-test/test-gdm-login.sh:154,225,265,341,377,519,664`), `vm-test/provision-vm.sh:66`, `vm-test/test-repo-setup.sh:84,264,270` (the same pre-existing pattern also sits in `vm-test/run-tests.sh:68,182`, `vm-test/test-quick-install.sh:66`, `vm-test/test-step-by-step-install.sh:180`, `vm-test/validate-install.sh:142`, out of diff scope; the shared `ssh_cmd` is in the diff)
**Attack:** any host with a position on the segment the target sits on. From 2026-08-30 the harness will drive `192.168.1.103` on the physical LAN, so any device on 192.168.1.0/24 qualifies: ARP-spoof the target (or the gateway), run a rogue sshd, and accept the harness's public key (readable from `~/.ssh/cinnamon-test-key.pub` on the PM host, or from `/root/.ssh/authorized_keys` in any test VM, since the same key is injected into every VM, `vm-test/provision-vm.sh:170`). Every `StrictHostKeyChecking=no` connection then authenticates against the attacker's server. For the libvirt VMs the same position is available to any compromised sibling VM on the shared flat L2 (finding 4).
**Impact:** the attacker answers the harness's probes and forges its verdict inputs: the `PHASE_RESULT PASS` markers (`vm-test/test-gdm-login.sh:265-275`), the `exit code 0` checks (`vm-test/test-repo-setup.sh:311,459,500`), and the whole evidence stream (journalctl, `/var/log/secure`, loginctl, a11y trees, screenshots). A Cinnamon login that never happened records as PASS; every command the harness runs is readable. The DoD's evidence requirement is defeated end to end.
**Fix:** pin host keys. Commit a `vm-test/known_hosts` containing (a) the cloud image's host key (all VMs boot from one image; verify once, extract with `virt-cat`/`ssh-keyscan` from a fresh VM, and commit; if the image regenerates keys on first boot, seed it in the provision step after `wait_for_ssh` and keep it under `vm-test/results/`) and (b) `192.168.1.103`'s host key (one-time human TOFU, fingerprint recorded in `## Docs`). Switch `ssh_cmd` and every inline `ssh`/`scp`/`rsync -e` site to `-o StrictHostKeyChecking=yes -o UserKnownHostsFile=...`.
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

### One SSH key is the sole root credential for every test VM and will unlock the real bare-metal host
**Severity:** medium
**Vector:** secrets
**Where:** `vm-test/lib.sh:28` (`SSH_KEY`), `vm-test/provision-vm.sh:49` (only the `.pub` existence is checked), `vm-test/provision-vm.sh:170` (injection into every VM), `## Next Actions` (Big's one-time `ssh-copy-id` to `howard@192.168.1.103`)
**Attack:** the key's blast radius today is root in every current and future test VM; the `ssh-copy-id` extends it to the real machine (passwordless sudo per `## Status`, i.e. root). If, as likely since the harness drives the machine with `SSH_KEY`, the fleet key is the one copied, one stolen private key opens the whole fleet plus the real host. The attacker reads the key locally on the PM host: the harness never checks its permissions (`check_prereqs`, `vm-test/provision-vm.sh:44-50`, tests existence only), and I could not verify the actual mode from this review's read-only toolset (no `stat`/`ls -l` access). `--keep-vm` runs leave the key authorized in live VMs for days (standing practice, `## Status`).
**Impact:** root in the whole VM fleet and root-equivalent on the real machine from one file; no per-target revocation (rotation re-provisions everything); no way to tell which target a given use of the key hit.
**Fix:** (a) `check_prereqs` asserts the private key is mode 0600 and owned by the invoking user; (b) Big's `ssh-copy-id` uses a key dedicated to the bare-metal host, not the fleet key, and that key's fingerprint goes into the finding-1 `known_hosts`; (c) the blast radius is stated in the `vm-test/lib.sh` header.
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

### test-repo-setup.sh runs the packaging script as root on the PM host; its safety rests on an unasserted ordering
**Severity:** medium
**Vector:** input-validation
**Where:** `vm-test/test-repo-setup.sh:199` (`sudo bash "${PROJECT_DIR}/repo-setup/setup-repo.sh" /tmp/nonexistent-dir-$(date +%s)`)
**Attack:** a future editor or agent changes the test argument to an existing directory containing `rpms/` (e.g. `${PROJECT_DIR}`, exactly what the in-guest call at `vm-test/test-repo-setup.sh:300` passes), or relaxes `setup-repo.sh` pre-flight ordering (moving the root check first is the most natural refactor). Current state, verified by tracing `repo-setup/setup-repo.sh` (not executed): with the nonexistent-dir argument the script dies at line 45 (`cd -P` under `set -euo pipefail`) before the root check (line 61) and every state-changing step (lines 82-144); the "No such file" message satisfies the test's grep (`vm-test/test-repo-setup.sh:200,207`) and is recorded PASS with no host state change. The no-argument non-root call (line 181) dies at the root check (line 61). So today it is stateless; the finding is the latent one-edit-away.
**Impact:** when triggered, the "error handling" test performs the full setup on the PM host as root: `dnf install createrepo_c` (host), `createrepo_c` over `rpms/` (writes gitignored `repodata/` into the working tree, invisible to `git status`), a host `/etc/yum.repos.d/cinnamon-rocky10.repo` with a `file://` baseurl into the working tree, CRB enabled on the host, `dnf makecache` on the host. Unannounced persistent host modification from a test; the host repo then trusts the working tree's `rpms/` (finding 5).
**Fix:** do not run the real script as root on the host: test the error paths against a stub (a copy with the state-changing sections replaced by echoes), or assert no side effects before/after (`/etc/yum.repos.d/cinnamon-rocky10.repo` absent, `rpm -q createrepo_c` unchanged, `dnf repolist` unchanged), and document the contract in the script header.
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

### A compromised harness VM can reach and root every other harness VM (masked firewall, flat L2, shared key)
**Severity:** low
**Vector:** authz
**Where:** `vm-test/provision-vm.sh:172-173` and `vm-test/test-repo-setup.sh:114-115` (`systemctl mask firewalld`), `vm-test/provision-vm.sh:187` (`--network network=default`, one shared L2), `vm-test/provision-vm.sh:170` (same public key injected everywhere)
**Attack:** any code running in any harness VM (a malicious RPM from the local repo, finding 5, or an `--in-vm` experiment) pivots: the firewall is masked, sshd listens, the sibling's IP is on the same L2, and the attacker's VM holds a copy of the public key the sibling trusts, so `ssh root@<sibling>` from inside works.
**Impact:** cross-VM lateral movement; the attacker can tamper with a running test's evidence (`/root/evidence`, `/var/log/secure`, `/root/gdmtest.pass` on `gdm-login-vm`) before phase 9 collects it, forging a verdict with no network position at all.
**Fix:** accept and document the disposable-VM assumption, or issue per-VM keypairs (generated during provisioning, injected per VM) and/or a per-test libvirt network; at minimum document the flat-L2 + shared-key assumption in the script headers.
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

### The local repo installs with gpgcheck=0, and the harness asserts that rather than flagging it
**Severity:** low
**Vector:** supply-chain
**Where:** `repo-setup/cinnamon-rocky10.repo` (`gpgcheck=0`, pre-existing), `vm-test/test-repo-setup.sh:229-235` (test 6 records FAIL when gpgcheck is not 0), `vm-test/test-gdm-login.sh:532-538` (in-guest `dnf install` from the `file://` repo, as root)
**Attack:** anyone with write access to `rpms/` in the PM-host working tree (every agent has it; a compromised build step would too) replaces or adds an RPM before the scp at `vm-test/test-gdm-login.sh:519-522`. Mitigant: `rpms/` is gitignored and rebuilt from spec, so tampering shows as untracked/modified files in `git status`, which is part of every agent's loop.
**Impact:** root code execution in the test VM (disposable); a poisoned package can rewrite the evidence before collection, producing a forged PASS (compounds the finding-4 pivot).
**Fix:** sign the local repo (repo GPG key, `gpgcheck=1`, `repo_gpgcheck`), or at minimum verify a checksum manifest of `rpms/*.rpm` committed to the repo before the scp.
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

### `--name` is unvalidated: path traversal into `cp` and `rm -f`
**Severity:** low
**Vector:** input-validation
**Where:** `vm-test/provision-vm.sh:104-108` (argument), `vm-test/provision-vm.sh:116-119` (`DISK_PATH`), `vm-test/provision-vm.sh:163` (cp), `vm-test/provision-vm.sh:56` (rm); also the `VM_NAME` env var (`vm-test/lib.sh:26`, `vm-test/test-gdm-login.sh:290,325`)
**Attack:** an operator, or a manipulated agent, passes `--name '../../../x'` or sets `VM_NAME` with path separators. The caller already has host access, so this is a footgun more than an external attack.
**Impact:** `cp` overwrites and `rm -f` deletes files outside `/var/lib/libvirt/images/cinnamon-test/` (within the invoking user's permissions) before the libvirt calls fail on the invalid domain name.
**Fix:** allowlist `^[A-Za-z0-9][A-Za-z0-9._-]*$` (libvirt domain-name rules) for both `--name` and the env var, dying on mismatch.
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

### New code carries no license headers; the repo is GPLv2; no incompatibility found
**Severity:** low
**Vector:** license
**Where:** `tasks/lib/ukey.c`, `tasks/lib/gdm-drive.sh`, `tasks/lib/gdm-a11y.py`, `tasks/lib/vnc-grab.py`, `vm-test/test-gdm-login.sh`, `vm-test/test-repo-setup.sh` (none carry a copyright or license notice; `git grep -iE 'GPL|license' task-0008-gdm-auth -- vm-test tasks .gitignore` returns nothing, which includes the pre-existing scripts, so this is the repo-wide convention, not a new deviation)
**Attack:** n/a (compliance gap, not an attack path).
**Impact:** the repo `LICENSE` is GPLv2. The six new files are original: I reviewed each, `ukey.c` is a standard uinput pattern, `gdm-a11y.py` is a direct AT-SPI2 D-Bus client (not pyatspi2 code), `vnc-grab.py` is a self-contained RFB implementation, the bash files are original. No copied code with stripped headers, no relicensing, no GPL-3.0/AGPL mixing. The gap is notice: GPLv2 section 1 requires license notices to be kept on distributed copies, and the license's "How to Apply" section recommends per-file notices.
**Fix:** add a GPLv2-or-later header matching `LICENSE` to the six new files; backfill the pre-existing `vm-test/` scripts in the same change.
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

**Verdict (2026-08-30): 0 critical, 1 high, 2 medium, 4 low.** Per the DoD Omega gate (no
unresolved findings above `low`), findings 1-3 block the merge until `Tails` fixes them and
the Shadow → Omega → Big re-run is clean. Finding 1 is the only one that can silently corrupt
the task's core deliverable (the evidence chain), and the bare-metal deployment makes it live
rather than theoretical.

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

### Branch diff verification + bare-metal env prep (2026-08-30, `Big`)

*Checkpoint 1/4. Scope: (a) non-VM test layers for `main..task-0008-gdm-auth`; (b)
non-interactive bare-metal prep on `howard@192.168.1.103` (baseline, RPM install, GDM
enable; stop before interactive login). Existing evidence base: 2c-3b PASS (checkpoint
`### Item 2 — 2c-3`). All command outputs truncated before entering context.*

**Environment notes.** Clone at `~/Linux/projects/cinnamon-for-rocky10/` (the brief's
`~/AI/projects/` path does not exist; same branch/commits as Shadow and Omega noted).
`git status` clean; `git log --oneline main..task-0008-gdm-auth` = the five commits
`b15dfcb`..`097702e`; `git diff --stat` = 9 files, 3394 insertions / 6 deletions. Linters
were absent on the PM host; installed `ShellCheck-0.10.0-3.el10_0` +
`python3-ruff-0.15.4-2.el10_2` from EPEL (`sudo dnf install -y ShellCheck python3-ruff`)
so the linter gate could actually run. `rpms/` holds 48 RPMs plus a valid `repodata/`
(`repomd.xml` present), so `setup-repo.sh` skips metadata generation on the target.

**Applicable test layers per AGENTS.md §7, treatment this pass:**

| Layer | Rationale | Treatment this pass |
|---|---|---|
| Unit (language-native) | diff has a C driver, 2 Python modules, 5 bash scripts | `gcc -Wall -Wextra` compile of `ukey.c`; `python3 -m py_compile` both .py files |
| Linter/static | bash + python in diff | `bash -n` x5; `shellcheck` 5 bash files; `ruff` 2 python files |
| Repo test entrypoint, no VM | `test-repo-setup.sh` phase 0 is host-side error handling (header line 15; `main()` line 674) | all 8 checks run individually; the script itself NOT run (it would proceed to VM provisioning, line 689) |
| Docker/podman | harness needs libvirt system driver, uinput, sudo, a LAN | N/A: containerizing changes the environment under test; the repo has no containerized entrypoint |
| VM / Sparky-Sparrow | graphical target; harness exists (`test-gdm-login.sh`) | not re-run this pass: 2c-3b PASS is the standing evidence; re-run after Tails' should-fixes, because the harness has 5 independently confirmed false-verdict/protocol paths (below + `## Review`) |
| Bare-metal | user's real machine, minimal-server | in progress (checkpoints 2-4) |

**(a) Results.**

| Check | Target | Result |
|---|---|---|
| `bash -n` | `vm-test/{lib,provision-vm,test-gdm-login,test-repo-setup}.sh`, `tasks/lib/gdm-drive.sh` | PASS 5/5 |
| `python3 -m py_compile` | `tasks/lib/{gdm-a11y,vnc-grab}.py` | PASS 2/2 |
| `gcc -Wall -Wextra` | `tasks/lib/ukey.c` | PASS, rc=0, zero warnings; binary runs (usage on no args) |
| `shellcheck 0.10.0` | 5 diff bash files | 0 errors; 7 warnings/notes (4x SC2034 unused vars, SC2046 `test-repo-setup.sh:199`, 2x SC2018/2019 locale classes); 3x SC1091 are tool artifacts (dynamic `source "${SCRIPT_DIR}/lib.sh"` not statically followable). `repo-setup/setup-repo.sh` clean |
| `ruff 0.15.4` | 2 python files | 2 errors: F821 `cmd_waiteditable` undefined (`gdm-a11y.py:517`); F841 unused `max_depth` (`gdm-a11y.py:277`) |
| `test-repo-setup.sh` phase 0 (8 host-side checks, run individually) | `setup-repo.sh` + `.repo` template | PASS 8/8: syntax; non-root rejection (rc=1, "must be run as root"); missing-dir rejection (dies at line 45 `cd -P`, stateless per Omega's trace); template exists with `BASEURL_PLACEHOLDER`, `gpgcheck=0`, `enabled=1`, `metadata_expire=0` |

**Independent verification of review findings (no VM needed):**

- Shadow should-fix #3 (false-PASS rc check) — **confirmed**. The exact expression at
  `vm-test/test-repo-setup.sh:311,459,500` (`echo "$rc" | grep -q "0$" && [ "$rc" != "255" ]`)
  records rc=10, 20, 30 as PASS; only rc=255 is guarded.
- Shadow should-fix #7 (`waiteditable` dispatch) — **confirmed by execution**:
  `python3 tasks/lib/gdm-a11y.py waiteditable` -> uncaught
  `NameError: name 'cmd_waiteditable' is not defined`, rc=1. ruff F821 flags the same line
  statically.
- Omega medium #2 (key mode unverifiable in a read-only review) — resolved: `stat` on the
  PM host shows `cinnamon-test-key` 600 howard:howard (private), 644 (pub). Mode is not
  the issue; the single-key fleet-wide blast radius still stands as a design issue.
- Shadow should-fix #5 (no prerequisite canary) — **failure mode live on this host**:
  plain `virsh list --all` (user session) returns an empty table, rc=0; `sudo virsh
  list --all` shows `gdm-login-vm` Id 3 running. The harness forces
  `LIBVIRT_DEFAULT_URI=qemu:///system` (`vm-test/lib.sh:19`) with no check that the
  invoking user can reach the system driver.
- ruff F841 `max_depth` unused (`gdm-a11y.py:277`) — new nit, not in `## Review`.

**NEW FINDING (supersedes the framing of Shadow #1): `vnc-grab.py` is non-functional
end-to-end against a spec-conformant RFB 3.8 server.** Verified with a spec-conformant
fake server (`/tmp/opencode/t0008/fake_vnc.py`: security None, 16-byte PixelFormat,
big_endian flag 0, LE host-order pixels, raw encoding) plus a socketpair isolation of the
post-handshake path (`/tmp/opencode/t0008/iso_test.py`):

1. ServerInit: `vnc-grab.py:79` reads 16 bytes; the spec's fixed part is 24 (2+2 + 16-byte
   PixelFormat + 4 name-len). `pf[10:13]` is a 2-byte slice -> uncaught `struct.error` at
   line 84. Full CLI run against the fake server: `struct.error: unpack requires a buffer
   of 3 bytes`, rc=1, during handshake.
2. FramebufferUpdateRequest: `vnc-grab.py:120` packs `>2B4I` = 18 bytes; the spec is 10
   (`>2B` + four uint16). A conformant server reads x=y=w=h=0 and the 8 trailing bytes
   desync its input stream.
3. FBU header: `vnc-grab.py:122-125` reads 8 bytes (spec: 4) and takes `n_rects` from
   `[6:8]` (spec: `[2:4]`). The full-frame rect at (0,0) that a full grab always produces
   makes `[6:8]` the rect's x,y = 0 -> isolation test result:
   `ProtocolError: framebuffer update carried no rects`.
4. Rect header: `vnc-grab.py:128` reads 10 bytes and unpacks with `>HHHBB` (8-byte
   format) -> `struct.error` guaranteed for any non-(0,0) rect (encoding is a uint32; the
   spec rect header is 12 bytes, `>HHHHI`).
5. Endianness (Shadow #1, `vnc-grab.py:118`): with the QEMU-on-x86 format (flag 0) the
   code picks `fmt='>I'`; wire bytes `[11 22 33 00]` decode to R=0x22 G=0x33 B=0x00
   (swapped/zeroed) vs the correct LE decode R=0x33 G=0x22 B=0x11.

Consequence: the documented pixel channel for domain-less VMs has never worked. The 2c-3b
PASS screenshots came from the QMP channel (consistent with Shadow's note that findings 1
and 2 "could not have bitten"). All five defects are in this branch's new file. Goes to
`Tails`; until fixed, any run relying on `vnc-grab.py` gets rc=1 with no screenshot at
all, not just a color-swapped one.

**Checkpoint 2 — bare-metal access + baseline (192.168.1.103, hostname `silver`).**

Access setup (one-time):

- Dedicated key per Omega finding 2: `~/.ssh/baremetal-103` (ed25519), fingerprint
  `SHA256:CvnIXRjnu7QUErfiExqbQ3q5zncY8ZPCLXo3PZ6TTSM` (public key material, recorded for
  the finding-1 `known_hosts` work). The fleet key `cinnamon-test-key` was **not** copied to
  this host.
- Host keys of `192.168.1.103` (OpenSSH_9.9) recorded via `ssh-keyscan` before first contact
  (TOFU): RSA-3072 `SHA256:OxbuXvwVOoYM017va5yZQ4b8907VHI/Tw7VmBhevXZ0`, ECDSA
  `SHA256:NAvJMVH7DOSWeJz/5fBXXiLXbZHCasrYx2YAmQsxq2c`, ED25519
  `SHA256:kAu+xhNLhmmJi65Rl6WpuyqdE8xJL/OxoJlzxi4T9qY`.
- One-time `sshpass -f ~/pass.txt ssh-copy-id ...`: password read from the file in place,
  never printed, never in arguments; output "Number of key(s) added: 1", rc=0.
- Key auth verified: `ssh -o BatchMode=yes cinnamon-bm103` rc=0 (BatchMode excludes any
  password fallback). Passwordless `sudo` confirmed (`sudo -n true` rc=0, per `## Status`).
  ssh config alias `cinnamon-bm103` (dedicated `IdentityFile`, `IdentitiesOnly yes`).
- `~/pass.txt` on the PM host tightened 644 -> 600.

Baseline minimal state (recorded before any modification):

- Rocky Linux 10.2 (Red Quartz), kernel `6.12.0-211.16.1.el10_2.0.1`, 12 cores, 19 GB RAM,
  SELinux `Enforcing`.
- 674 packages.
- Login manager: **none**. `rpm -q gdm lightdm sddm` -> all not installed;
  `systemctl is-enabled gdm` -> `not-found`; `is-active` -> `inactive`.
- X server: **none**. `xorg-x11-server-Xorg` not installed; `rpm -qa | grep -iE
  'xorg-x11-server|mesa|wayland|pipewire|pulseaudio'` -> zero packages.
- Desktop packages: **0** (`rpm -qa | grep -icE 'cinnamon|gnome-shell|gnome-session|mate-desktop|xfce|plasma-desktop'` -> 0).
- Session dirs: `/usr/share/xsessions/` and `/usr/share/wayland-sessions/` exist, both empty.
- Active targets: `multi-user.target` + prerequisites; no `graphical.target`.
- Repos: `appstream`, `baseos`, `extras` (CRB currently disabled; the setup script enables it).
- Console: getty on tty1; only howard's SSH sessions.

**Checkpoint 3 — Cinnamon RPM install from the local DNF repo (192.168.1.103).**

Procedure (INSTALL.md quick start, local-repo variant):

- Transferred `repo-setup/` + `rpms/` (48 RPMs + `repodata/`) to
  `~/cinnamon-for-rocky10/` via rsync over the dedicated key; **all 48 RPM sha256s
  identical local==remote** (manifests diffed, empty).
- `sudo bash ~/cinnamon-for-rocky10/repo-setup/setup-repo.sh ~/cinnamon-for-rocky10` ->
  rc=0, `=== Repository setup complete ===`. Installed `createrepo_c-1.1.2-4.el10` + libs
  (2 packages, appstream); used the clone's shipped `repodata/` (skipped generation); wrote
  `/etc/yum.repos.d/cinnamon-rocky10.repo` with
  `baseurl=file:///home/howard/cinnamon-for-rocky10/rpms`; enabled CRB; `dnf makecache` for
  the local repo OK.
- `sudo dnf install -y cinnamon` -> rc=0, `Complete!`.
- `sudo dnf install -y cinnamon-session cinnamon-settings-daemon cinnamon-control-center
  nemo mozjs115-devel` -> rc=0 (5/5), `Complete!`.
- `sudo ldconfig` -> rc=0.

What it pulled in (snapshot diff of `rpm -qa` before/after via `comm -13`; full list saved
on the machine at `~/t0008-new.txt`, snapshots `~/t0008-{before,after}.txt`):

- **157 new packages** total (674 -> 831).
- **No login manager**: gdm/lightdm/sddm neither installed nor pulled in
  (`rpm -q gdm` -> not installed, `systemctl is-enabled gdm` -> not-found).
- **No X server**: no `xorg-x11-server-*` in the new set. Graphics pull-in is the
  **mesa stack for Wayland**: `mesa-dri-drivers`, `mesa-filesystem`, `mesa-libEGL`,
  `mesa-libgbm`, `mesa-libGL` (all 25.2.7-4.el10.rocky.0.1) plus 15 X11 *library*
  packages (link-time deps, not a server).
- Other notable pull-ins (from dnf's `Installed:` list): pipewire 1.4.11 + wireplumber
  0.5.10 + pulseaudio-libs 17.0 (audio), tracker 3.7.3 + tracker-miners 3.7.4,
  xdg-desktop-portal 1.20.0 + xdg-desktop-portal-gtk 1.15.3, upower 1.90.10,
  sound-theme-freedesktop, rtkit, webrtc-audio-processing, poppler + poppler-glib,
  xprop, startup-notification, xcb-util.
- **All 14 target packages present at the INSTALL.md table versions** (`rpm -q`):
  mozjs115/mozjs115-devel 115.29.0, cjs 6.4.0, muffin/muffin-clutter/muffin-cogl 6.7.4-3,
  cinnamon-desktop 6.7.2, xapps-lib 3.3.3, cinnamon-session 6.7.3,
  cinnamon-settings-daemon 6.7.2, cinnamon-control-center 6.7.2, cinnamon-menus 6.7.0,
  nemo 6.7.4, cinnamon 6.7.4.
- **Session entries**: `/usr/share/xsessions/cinnamon.desktop` +
  `/usr/share/wayland-sessions/cinnamon-wayland.desktop`, both present (matches `###
  Item 3` F3 and the 2c-1 bonus finding).

Verdict so far: the RPM set installs cleanly on a minimal state with no DM and no X
server; it installs **neither a login manager nor an X server**, and pulls the mesa
Wayland graphics stack. The machine is now "Cinnamon installed, no login path yet" — GDM
next.

**Checkpoint 4 — GDM install + enable; final state; summary (192.168.1.103).**

GDM phase (root operation on the target; blast radius = that machine's package DB):

- `sudo dnf install -y gdm` -> rc=0, `Complete!`. Pulled **105 packages** (gnome-shell
  greeter stack; full list `~/t0008-new-gdm.txt`, snapshots `~/t0008-{pre,after}-gdm.txt`).
  Installed: `gdm-47.0-22.el10_2`, `gnome-shell-49.4-8.el10_2.rocky.0.2`,
  `xorg-x11-server-Xwayland-24.1.9-4.el10_2.3`, xdg-desktop-portal-gnome 47.3, wpa_supplicant,
  switcheroo-control, vulkan-loader, xkbcomp, and the rest of the GNOME greeter deps.
- **Xorg re-verified absent on bare metal** (the 2c-1 question, machine answer):
  `dnf list available xorg-x11-server-Xorg` -> `Error: No matching Packages to list`;
  `dnf list available 'xorg-x11-server*'` -> only `xorg-x11-server-Xwayland-devel` (crb).
  No `xorg-x11-server-Xorg` in any enabled repo (appstream, baseos, extras, crb,
  cinnamon-rocky10). X11 compatibility in the Wayland session is via Xwayland, which the
  GDM install pulled.
- **GDM 47 is Wayland-only, re-verified**: `rpm -ql gdm | grep -c gdm-x-session` -> 0;
  `grep -c gdm-wayland-session` -> 1 (`/usr/libexec/gdm-wayland-session`).
- **Enablement**: `systemctl is-enabled gdm` -> `enabled` (set by the package post-install;
  no manual `systemctl enable` needed), `is-active` -> `inactive`. `systemctl list-unit-files
  gdm.service` -> `gdm.service enabled enabled`. **GDM was NOT started; the machine stays at
  the getty on tty1. Stopped before interactive login, as instructed.**
- **Session entries after GDM**: `/usr/share/xsessions/` -> `cinnamon.desktop`;
  `/usr/share/wayland-sessions/` -> `cinnamon-wayland.desktop`, `gnome.desktop`,
  `gnome-wayland.desktop`.

**Machine state at stop (192.168.1.103, `silver`):**

- Rocky 10.2 minimal-server baseline (674 pkgs) + 14 Cinnamon packages + 157 pulled deps +
  GDM 47 + 105 pulled deps = 831 + 105 packages. SELinux Enforcing throughout.
- Login path: GDM enabled, will present at next boot (or `sudo systemctl start gdm`).
  Cinnamon selectable as `Cinnamon` (Wayland) and `GNOME`/`GNOME Wayland`; the X11
  `Cinnamon` entry exists but has no Xorg to run on (recorded answer, re-run to confirm).
- Access: key-based only (dedicated `~/.ssh/baremetal-103`, alias `cinnamon-bm103`),
  passwordless sudo. Evidence files on the machine: `~/t0008-{before,after,pre-gdm,
  after-gdm,new,new-gdm}.txt`.

**Workflow run (this pass):**

| Check | What it exercises | Result | Notes |
|---|---|---|---|
| compile | `ukey.c` (gcc -Wall -Wextra), `py_compile` x2 | PASS | zero warnings; binaries/scripts load |
| linter | shellcheck 0.10.0 (5 bash), ruff 0.15.4 (2 py), bash -n (5) | PASS w/ findings | shellcheck 0 errors / 7 notes; ruff 2 errors (1 = Shadow #7 confirmed, 1 new nit F841) |
| unit tests | `test-repo-setup.sh` phase 0 host-side checks (8), run individually | PASS 8/8 | script not run whole (would provision a VM) |
| integration tests | vnc-grab.py vs spec-conformant fake RFB server + socketpair isolation; waiteditable exec; rc-0$ expression; virsh canary; bare-metal install flow | **FAIL (tool) / PASS (env prep)** | vnc-grab.py non-functional (5 protocol defects, new finding); all bare-metal steps rc=0 |
| Sparky tests | Rocky Linux UI, interactive login + navigation | NOT RUN (deferred) | requires the fixed harness (should-fixes #1/#2 + new vnc-grab finding) and post-merge state; 2c-3b PASS is the standing VM evidence |

**Checks requested vs run:** 12 requested, 12 executed. (a): layer determination,
static/syntax pass, linter pass, repo VM-free entrypoints, independent verification of
harness verdicts. (b): ssh-copy-id, baseline, RPM install, pull-in record, session entries,
GDM install+enable, stop-before-login, Xorg re-verification. Nothing dropped: the VM
re-run and the interactive bare-metal matrix are explicitly out of scope for this pass
(pending Tails' fixes), not silently skipped.

**Verdict:**

- **(a) Branch diff, non-VM layers: PASS with two code findings for `Tails`.** No syntax,
  compile, or template defects. The linter pass confirms one should-fix (Shadow #7, F821)
  and adds one nit (F841 `max_depth` unused, `gdm-a11y.py:277`). The independent
  verification did not trust the harness's PASS markers and found the harness's own
  false-PASS expression live (Shadow #3: rc 10/20/30 recorded PASS), the permissions
  failure mode live on this host (Shadow #5), and a **new major finding: `vnc-grab.py`
  is non-functional against any spec-conformant RFB server** (5 defects, checkpoint 1) —
  this supersedes the latent-ness of Shadow #1: no screenshot evidence of any kind is
  obtainable from that tool today. All of these are code bugs (go to `Tails`), not
  harness-of-verification bugs.
- **(b) Bare-metal env prep: PASS, all steps rc=0.** Minimal-state baseline recorded; the
  48-RPM set (checksum-verified transfer) installs cleanly via the local DNF repo with
  zero login managers and zero X servers pulled in (mesa Wayland stack only); both
  Cinnamon session entries present; all 14 packages at the INSTALL.md versions; GDM 47
  installed and enabled (Wayland-only, Xorg re-confirmed absent from all repos); machine
  left at the getty, not booted into the greeter, no interactive login attempted.
  The machine is ready for the re-run's interactive matrix.
- **Merge gate status (for the chain):** still blocked, as expected — `## Review` has 10
  unresolved should-fixes (3 of them now independently confirmed to produce wrong
  verdicts), `## Security` has 1 high + 2 medium unresolved, and this pass adds the
  vnc-grab protocol rewrite and one nit. Nothing here blocks env prep; it all blocks the
  re-run and the merge.

**What the re-run still needs:**

1. `Tails` fixes: the 10 should-fixes (independently confirmed: #3 rc-0$ false PASS, #5
   no prerequisite canary, #7 waiteditable NameError; #1 endianness is subsumed by the
   new vnc-grab finding which requires fixing the ServerInit read, FBU request size, FBU
   header size/offset, and rect header before the endianness line is even reachable),
   the new nit (F841), and Omega's 1 high + 2 medium (known_hosts pinning — use the
   host-key fingerprints recorded in checkpoint 2; dedicated bare-metal key — done for
   the host, `~/.ssh/baremetal-103`, harness wiring is Tails' part; root-on-host test
   stub).
2. Re-run of the VM harness (`test-gdm-login.sh`) after the fixes to re-establish the
   2c-3b evidence with a verdict-trustworthy harness.
3. Interactive bare-metal matrix: start GDM (`systemctl start gdm` or reboot), log in as
   `howard` (password available in `~/pass.txt` on the PM host, never written anywhere)
   selecting `Cinnamon (Wayland)`, verify the session is active (loginctl + processes)
   and navigable; then record the X11-session question (the `cinnamon.desktop` X entry
   has no Xorg to run on — confirm GDM's behavior for it).
4. **Open design question for the re-run (observation channel on a physical machine):**
   the machine exposes no VNC, so `vnc-grab.py` is inapplicable by architecture, not
   just by bug. Options: (a) a11y over the system bus + loginctl/journal evidence with
   the user physically observing the screen; (b) install a remote-desktop observation
   agent in the greeter/session (gnome-remote-desktop or wevnc class). Decide before the
   interactive run; input injection is not a problem (ukey/uinput is display-protocol
   independent and the machine has passwordless root for `/dev/uinput`).

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

**DONE checklist verified:** no (recorded, user-authorized deviation; the merge proceeded per
explicit user instruction, 2026-08-30, asked twice; record in `## Status` fourth entry). Missing
from the DoD: the Shadow gate (should-fixes #2, #5, #6, #10 plus 7 nits unresolved), the
vnc-grab decision (batch C), the trio re-run (Shadow, Omega, Big), Big's bare-metal interactive
matrix (start GDM, log in as `howard`, no-glitch check), and the Vector doc update. Met: the
Omega gate (high + 2 medium fixed in batch A, only low findings remain) and Big's first pass
(non-VM 12/12 PASS with findings; bare-metal env prep + RPM install PASS).

- **Branch:** task-0008-gdm-auth (pre-existing; does not match the `feature/TASK-XXXX-slug`
  house pattern; the user instructed to merge this branch as-is)
- **Commits:** GPG-signed no (`commit.gpgsign` not set in the repo or globally; the 13 commits
  are unsigned)
- **PR:** opened ✅ | merged ✅ (#3, internal `metalllinux` repo, no human review required)
- **Deploy:** N/A (repo-only change, no deployment, no workflow dispatched)

**PR #3:** https://github.com/metalllinux/cinnamon-for-rocky10/pull/3, title `feat(vm-test):
add GDM login harness + security and verdict-integrity fixes`, base `main`, head
`task-0008-gdm-auth`, opened and merged 2026-08-30, merged 2026-08-30T11:35:06Z via GitHub
rebase merge. The house default is squash-merge; squash was rejected for this PR because the
user's instruction requires all 13 commits to land on main and be verifiable there. The rebase
merge kept the history linear, no merge commit.

**Merge result:** pre-merge main was `1f00da5`; post-merge main is
`4880e0b87f5758786de36e34a4c654bc2a07c672` (local main = origin/main = GitHub API main head).
The rebase merge rewrote the 13 commits with new SHAs (author preserved, committer changed to
the GitHub bot identity); subjects and trees are identical. Old → new mapping:
`b15dfcb`→`72a2e51`, `959d01d`→`5dac468`, `456ce71`→`e3d3a3e`, `ddac27e`→`d100218`,
`097702e`→`140a667`, `1c16045`→`abbc1d2`, `af3a9ff`→`188f972`, `cd6860c`→`017506f`,
`85f629e`→`d72867e`, `921de9f`→`1dc224a`, `9ce6cb5`→`53011a5`, `6f6b1b5`→`816d3a7`,
`f259dd5`→`4880e0b`.

**Verification (post-merge, clone `~/Linux/projects/cinnamon-for-rocky10/`):**

- `git rev-list --count 1f00da5..main` = 13
- `git diff f259dd5..main` = empty (main tip tree byte-identical to the branch tip tree)
- all 13 commits present on main in order, each checked per pair (old vs new subject + tree),
  all OK
- local main = origin/main = GitHub API main = `4880e0b`
- remote branch `task-0008-gdm-auth` retained on origin (follow-up batches C/D build on it)

**Tracked follow-ups (from `## Next Actions`, land via the second PR):** Tails batch C
(vnc-grab decision + implementation), Tails batch D (should-fixes #2 ukey uppercase drop, #5
prerequisite checks, #6 hardcoded 48-RPM check, #10 provisioning dedup + nits), Shadow re-run,
Omega re-run, Big re-run (VM harness re-run + bare-metal interactive matrix), Vector (README +
INSTALL.md), Knuckles second PR, then the task is DONE; Robotnik starts the TASK-0015 chain
from the updated main after this merge.

**Process notes / deviations from the brief:**

- Clone location: the brief said `/home/howard/AI/projects/cinnamon-for-rocky10/`; the actual
  clone is `/home/howard/Linux/projects/cinnamon-for-rocky10/` (the path used throughout the
  planning doc). Same branch, same tip `f259dd5`, clean tree.
- Push quirk confirmed and worked around as instructed: the token embedded in the origin URL
  is stale (401 against the GitHub API; the repo is public, so anonymous fetch works). The
  configured credential helper (`credential.https://github.com.helper` =
  `/home/howard/.local/bin/git-cred-token-md`, reads `/home/howard/token.md`, token verified
  valid with a 200 from `/user`) is the working credential. No git push was needed (the branch
  was already at `f259dd5` on origin); the `gh` API calls (PR create + merge) used the same
  token via `GH_TOKEN` in the process environment, never written to a file, doc, or commit.
- **Security note (escalate to the user):** during verification, one `git config --local
  --list` run displayed the origin URL with the embedded token unmasked in agent tool output.
  The token was not written to the repo, a doc, or a commit. It is already invalid against
  the API, but if it is still valid for any purpose the user should revoke it. Recorded here
  rather than in `## Security` because Knuckles' write scope for this task is `## Release`
  only; `Omega` or the user should pick it up in `## Security`.

---

## Archive

*Owner: `Espio`, the only agent that deletes. Superseded detail lands here rather than being
lost. Decisions, verified facts, rejected options with their reasons, known traps, and anything the
user said are never deleted.*

**Pruning log**

| Date | What was pruned or compressed | Rough size |
|---|---|---|
| | | |
