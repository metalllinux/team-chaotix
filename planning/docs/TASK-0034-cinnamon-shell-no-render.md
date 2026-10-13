# TASK-0034 — Cinnamon shell no-render: panel and app windows not rendered on Rocky_Linux_10_Cinnamon

> **Section order below is fixed.** Each agent writes to its own section and no other. `Robotnik`
> reads only `## Status` and `## Next Actions`. Do not reorder, rename, or remove sections.

- **Created:** 2026-10-07

---

## Status

### 2026-10-12: Espio pruning pass — nothing qualified; no edits made

Standard pass (one contiguous ~140-line chunk, at most three edits, span re-read before edit). No span qualifies as superseded narration or a resolved-and-shipped finding: the DoD boxes, the final verdict and gate evidence (`## Test Results`), and the command + output evidence (`## Implementation` parts 1-3, cited by the 2026-10-10 closure entry) are load-bearing; the Plan's risk and rollback rows, the `-4` RPM re-apply procedure, the 3x3 moving-block A/B exclusion, and the `pkill -f` self-match are standing traps; the work-breakdown item numbers and the four first-diagnostic directions are still referenced; and the only candidate spans (the Plan's estimates/dependencies/critical-path tables, the mid-run harness-bug findings) are pre-task data tables and unresolved traps, not narration. Nothing moved to `## Archive`; the pruning log is unchanged.

### 2026-10-10: PM closure — DoD boxes verified against the box map and ticked; task DONE

DoD boxes verified against the box map recorded in the 2026-10-08 handoff entry and ticked in `## Definition of Done`: box 1 (root cause, four diagnostic directions) verified by the `## Implementation` part-2 entry (items 3-7, each with command + output; moving block identified as an autonomous compositor-composited external element, X1 anomaly resolved as Xwayland-on-:1 plus stale X0, wallpaper source established as nemo-desktop layer-shell surface, compositor GL state established as llvmpipe plus CPU copy path). Box 2 (classification) verified by part-2 item 7: environment limitation (VM display/GPU pipeline); the other two categories explicitly ruled out; bounded uncertainty stated. Box 3 (fix) verified as N/A, condition false per part-3 item 8 (host QEMU 10.1.0: no 3D display device, no virglrenderer code or linkage, nothing installable via dnf; zero VM state change, rollback not triggered). Box 4 (testability) verified by the `## Test Results` Tails item-8 entry (environment-limitation verdict plus the what-would-make-it-testable list). Box 5 (final verdict) verified by the `## Test Results` Big entry (gate FAIL as expected, 14 frames / 4 distinct md5s, all requested checks executed, none dropped; not a code bug, not a harness bug). TASK-0034 is DONE. The Power pane D-Bus `Unauthorized (36)` error is split out as TASK-0035 (planning/docs/TASK-0035-cinnamon-power-pane-dbus-unauthorized.md). The item-8 bounded uncertainty (compositor software-path bug not fully exonerated pending a hardware-GL control) remains open as recorded in `## Test Results`.

### 2026-10-08: TASK-0034 items complete (verdict: environment limitation); PM handoff to fresh session

`Tails` dispatch (plan items 8-9, `## Implementation` part-3 entry): the named fix is not possible in this environment — host QEMU 10.1.0 has no 3D display device (only virtio-gpu-device/virtio-gpu-pci/virtio-vga; zero virglrenderer code; nothing installable via dnf) — so the guest's Mesa stays llvmpipe-only and the no-render stands; no fix applied, zero VM state change, rollback not triggered; verdict plus testability list in `## Test Results`. `Big` dispatch (plan item 10, dated `## Test Results` entry lines 464-547, gate table lines 385-414): 12-pane gate FAIL as expected, all requested checks executed, none dropped (14 frames, 4 distinct md5s); verdict: not a code bug, not a harness bug, item-8 environment limitation stands. Findings recorded in both this doc and TASK-0026: one console error (Power pane, `cs_power.py:883` D-Bus Unauthorized (36), app survived, killed by recorded pid; not routed to Tails as a blocker), the moving block appears on both VMs at the same 3x3 grid with the same size class (identity unresolved, Status unknown 1), harness bugs fixed mid-run and the gate re-run cleanly. TASK-0026 item 3 is unblocked and done (that doc, dated Big entry lines 1427-1483): DoD box 3 PASS, box 4 mixed (no window rendered on Fedora either — Wayland vs X11 and 6.7.4-4.el10 vs 6.7.5^unstable, identical bare-virtio video XML), box 5 comparison table. DoD box map for verification: boxes 1-2 = `## Implementation` part-2 entry, box 3 = N/A (not fixable here), box 4 = part-3 entry, box 5 = Big `## Test Results` entry. PM handoff (session context too large for the child to inherit, r001): continue from `/tmp/opencode/continue-in-new-session.md` — next is TASK-0026 item 4 (review chain), then TASK-0027 (Amy). Carried forward: the Power pane D-Bus error becomes a new task after the review chain (evidence in both docs' dated entries).

### 2026-10-08: Tails diagnosis run died after items 1-2 (PM session context too large for child); part 1 complete and recorded; work continues in a fresh PM session

The `Tails` diagnosis dispatch (plan items 1-7) died mid-run: `Compaction summary reached the output token limit` (session ses_ee90563d8ffesDVfIkD6aGURXA). Partial work exists and is recorded in `## Implementation` (part-1 entry, items 1-2 complete): checkpoint snapshot `2026-10-07-task0034-pre` created (internal per the recorded plan deviation; parent `2026-10-04T11:36`; `Current: yes`), baseline capture complete (VNC `127.0.0.1:5901` / qemu-kvm pid 18687; no websockify 6080 on the host, operator path = Cockpit Machines 9090; session 2 idle ~2 days; `X0` stale, no process holds it; `renderD128` open by no process; session stdout/stderr go to the journal, which resolves TASK-0026 open question 8). VM running, domain id unchanged, no other state change. Root cause per learned rule r001 plus the 2026-10-05 precedent: the PM session context is too large for the child to inherit, and a re-dispatch from that session cannot succeed (context only grows). Operator step (config territory, recorded not asked): start a new opencode session in /home/howard/AI/projects/team-chaotix and continue from this doc's `## Next Actions`. Candidate lesson for the fresh session's PM to propose via agentsmd: a child that dies on a compaction-summary size error may have left a partial part-N `## Implementation` entry; the continuing run verifies the part-N claims against live state before doing further work.

### 2026-10-07: intake — no-render defect split out of TASK-0026 item 2 (separate task per Tails' recommendation)

Source: planning/docs/TASK-0026-cinnamon-control-center-comparison.md, `## Implementation`, Tails entry 2026-10-06. Machine: `Rocky_Linux_10_Cinnamon` (192.168.122.4), session 2 (wayland/gdm-password, seat0/tty2), in-process compositor `/usr/bin/cinnamon --replace` (pid 2961 at record time), `Xwayland :0`; snapshot `2026-10-04T11:36` intact for restore. Defect: neither the shell's own in-process panel nor externally launched app windows (e.g. `cinnamon-settings`) render a visible window although the apps start and stay alive; A/B pixel-diff (app alive vs killed) is 0 pixels; X11 `_NET_CLIENT_LIST` empty; zero panel/compositor errors logged. Tails' classification: environment/compositor-level defect below the app layer, out of scope for TASK-0026 item 2. First-diagnostic directions from that entry: the moving external block's identity, the `X1` anomaly, the wallpaper-source question, and the compositor's output/GL state. Login: `howard`, password at `~/AI/secrets/pass.txt` (never written to any file). Every virsh command passes `-c qemu:///system`.

**Now:** diagnosis not started; TASK-0026 item 3 (Big 12-pane screenshot gate) is BLOCKED on this task's fix landing.

**Environment / scope:**
- Files in scope: VM session state on `Rocky_Linux_10_Cinnamon` first; Cinnamon component checkouts under ~/Linux/projects/cinnamon-for-rocky10 (cinnamon/, muffin/, nemo/) only if a port bug is found
- Touches the DB schema: no
- Graphical UI: yes (text-only screenshot evidence: md5/PIL, no image reads)
- Rocky Linux target: yes

**Unknowns:**
- Identity of the moving external block (present in the pre-test baseline, md5 `4cf21192c11668653b0631b7ceff04e2`, appears only at 3x3 grid centers, not an X11 `:0` window).
- Why the in-process panel surfaces do not appear (compositor output/GL state unverified).
- The `X1` display in `/tmp/.X11-unix/` with ESTAB pairs attributed to `Xwayland` (unexplained).
- Wallpaper source: nemo Wayland surface versus compositor output background (deliberately untested; killing `nemo-desktop` would disturb the operator's live desktop).
- Whether a session restart (which would also run the -4 compositor binary instead of the in-memory -3) changes rendering.

---

## Definition of Done

- [x] Root cause established with command + output evidence: why the shell's in-process panel and externally launched app windows produce no visible window on `Rocky_Linux_10_Cinnamon`, covering the four first-diagnostic directions in `## Status` (moving block identity, `X1` anomaly, wallpaper source, compositor output/GL state).
- [x] Classification recorded: environment limitation (VM display/GPU pipeline) versus session configuration defect versus Cinnamon port bug, with evidence.
- [x] If fixable in this environment: fix applied (VM session state and/or source in the canonical checkout) and verified with text-only screenshot evidence (md5/PIL): the panel bar renders (rows 0-39 are no longer wallpaper texture only) and an app window (`cinnamon-settings`) is a visible window (non-zero pixel difference against the app-killed baseline). — verified as N/A: the fix condition is false, host QEMU 10.1.0 has no 3D display device, no virglrenderer code or linkage, and nothing installable via dnf (`## Implementation` part 3, item 8); no fix applied, zero VM state change.
- [x] If environment limitation: documented in `## Test Results` with what would make it testable (real display/GPU pipeline or different QEMU display configuration).
- [x] `## Test Results` updated with the final verdict.

---

## Next Actions

- [x] `Amy`: plan the diagnosis. — done: `## Plan` written (10-item breakdown; items 1-9 `Tails`, item 10 `Big`; rollback via the `2026-10-04T11:36` snapshot plus a `2026-10-07-task0034-pre` checkpoint; verification gate consistent with TASK-0026 item 3).
- [x] `Tails` (diagnosis, plan items 3-7; items 1-2 complete per the 2026-10-08 part-1 entry in `## Implementation`): first verify the part-1 claims against live state (snapshot-list shows `2026-10-07-task0034-pre` with `Current: yes`; VM running; VNC on 5901), then the four first-diagnostic directions (moving block, `X1` anomaly, wallpaper source, compositor output/GL state) and the classification plus the named fix path. Append to `## Implementation` (part 2 of up to 3, per-item sub-headers with command + output evidence); if the turn budget runs out, stop cleanly at the last completed item and record which remain. Read-only; never kill `nemo-desktop` or disturb the operator's live desktop; every virsh command passes `-c qemu:///system`.
- [x] `Tails` (fix, plan items 8-9, after the diagnosis): apply the named fix (VM session state and/or source) and verify with text-only screenshot evidence (md5/PIL); conditional rollback if it fails. Write to `## Implementation`.
- [x] `Big` (item 10, after the fix): the 12-pane screenshot gate on `Rocky_Linux_10_Cinnamon` consistent with TASK-0026 item 3, plus the final verdict in `## Test Results`.

---

## Plan

*Owner: `Amy`.*

**Why this task exists** — TASK-0026 item 3 (Big 12-pane screenshot gate) cannot pass on
`Rocky_Linux_10_Cinnamon`: neither the shell's in-process panel nor app windows render, so the gate
would re-hit the identical BLOCKED state with zero new information (TASK-0026 `## Status` 2026-10-07).
This task is the no-render defect split out of TASK-0026 item 2 per Tails' recommendation
(TASK-0026 `## Implementation` 2026-10-06). It serves the project goal of verifying the Cinnamon
port's GUI on Rocky 10 (TASK-0026 DoD boxes 1-2).

**What it unblocks / what blocks it** — Unblocks: TASK-0026 item 3 (12-pane gate), then item 4
(Fedora comparison, DoD boxes 3-5), then the review chain and checkpoint commit. It also holds a
candidate shared root cause for TASK-0027 (brightness no-effect: backlight/GL, unverified). Blocks
it: nothing in this repo and no CI. Everything blocking is external machine state: the VM is the
operator's live desktop (concurrent use is the leading hypothesis for the moving external block),
and the only rollback asset is the external snapshot `2026-10-04T11:36` (verified present 2026-10-07,
state `shutoff`, `Location: external`, `Metadata: yes`).

**MVP** — root cause established with command + output evidence, classification recorded (DoD boxes
1-2). That is the value: TASK-0026 item 3 needs a verdict either way. The fix plus verification is
the stretch (DoD box 3). The environment-limitation documentation (DoD box 4) is a valid terminal
state, not a failure. Deferred (downstream, not this task): the 12-pane gate itself (Big,
TASK-0026 item 3), the Fedora comparison, the review chain, `Knuckles`/`Vector`/`Espio`.

**What this makes harder later.** (a) If the fix is VM session/display state rather than source, the
fix lives in this VM's state and this doc only; the vm-deploy skill (TASK-0028/0031) has no record
of the display configuration that works. `## Implementation` must therefore record the working
configuration in a copyable form. (b) Operator concurrent use is permanent: every future
screenshot A/B on this VM must exclude the operator block region (test hygiene, standing). (c) If
the verdict is environment limitation, the 12-pane gate stays blocked in this VM and is testable
only under the conditions `## Test Results` documents.

**Assumptions** (stated, not silent):
- A1. The operator's concurrent desktop use on this VM is accepted; disruptive actions (kill a
  session component, session restart, VM restart, snapshot revert) are in scope per DoD box 3
  ("VM session state") and are ordered last, always after item 1.
- A2. Creating a pre-task checkpoint external snapshot is accepted rollback infrastructure
  (VM state addition; no repo change, no secret).
- A3. "Fixable in this environment" includes VM session state and QEMU XML display config. The
  source checkouts (`cinnamon/`, `muffin/`, `nemo/` under `~/Linux/projects/cinnamon-for-rocky10/`,
  all present) only if a port bug is found (per `## Status` scope line).
- A4. Login `howard`, password at `~/AI/secrets/pass.txt`, never written to any file (per `## Status`).
- A5. Video device is bare `<model type='virtio' heads='1' primary='yes'/>` with no 3d/virgl
  element, VNC display `127.0.0.1` (verified 2026-10-07 via `virsh dumpxml`). Hypothesis input,
  not a finding.
- A6. Libvirt on Rocky 10.2 supports external snapshot revert to a `running`-state snapshot with the
  domain running. The `2026-10-04T11:36` (`shutoff`-state) revert path is the verified-safe one by
  construction (shutoff snapshot, shutoff domain).

**Work breakdown** — one agent, one item, one turn. Briefs point at this doc and the `## Status`
first-diagnostic directions; they do not restate evidence. Record one-line findings plus the
command that produced each (no log dumps).

| # | Item | Owner agent | Acceptance criterion | Parallel with |
|---|---|---|---|---|
| 1 | Pre-task checkpoint: `df` free-space check (>= 4 GB), `qemu-img info` on the active delta, then `virsh snapshot-create-as` external snapshot `2026-10-07-task0034-pre` on the running VM | `Tails` | `virsh snapshot-list` shows `2026-10-07-task0034-pre` (state `running`) plus `2026-10-04T11:36` (`shutoff`); free space recorded | Blocks all |
| 2 | Read-only baseline capture: `virsh vncdisplay` and `ss -ltnp` (VNC port and the 6080 websockify target; XML says 5901 autoport, TASK-0026 recorded 5910), `dumpxml` display/serial/graphics, guest `/dev/dri`, `/tmp/.X11-unix` listing, `ss -xp` for all X11/Wayland sockets, `loginctl list-sessions` (GDM session type), pid 2961 `/proc/<pid>/fd` + `/proc/<pid>/maps` (libEGL/mesa/renderD), full `ps` | `Tails` | Everything recorded in `## Implementation` with command + output; zero VM state change | Blocks all (after 1) |
| 3 | Direction 1: moving external block identity. Read-only | `Tails` | Block's origin identified with command + output (process, fd, surface, or display); at least two competing explanations weighed, rejected ones with reasons | Independent of 4, 5, 6 |
| 4 | Direction 2: the `X1` anomaly. Read-only | `Tails` | The server process owning `/tmp/.X11-unix/X1`, its cmdline/environ, the ESTAB clients, and whether any app window could map there: answered with command + output | Independent of 3, 5, 6 |
| 5 | Direction 3: wallpaper source. Disruptive (kills `csd-background`/`nemo-desktop`); run last of the diagnostics | `Tails` | Wallpaper source determined (which process's Wayland surface, or compositor output background) with A/B screenshots (md5 + pixel diff) around the kill; if items 3 or 6 settle it without a kill, record that instead | Independent of 3, 4, 6; ordered last |
| 6 | Direction 4: compositor output/GL state. Read-only (includes where `/proc/2961/fd/1-2` point, i.e. where session output goes, and a short `strace -p` on pid 2961 if needed) | `Tails` | Compositor output state determined with command + output: GL context/render node present or absent, output attachment, any error text found | Independent of 3, 4, 5 |
| 7 | Classification + fix path | `Tails` | Exactly one of environment limitation / session configuration defect / Cinnamon port bug, with evidence citing items 2-6; named fix path (session config change, display pipeline change, or source fix) or, for environment limitation, what would make it testable | Depends on 2-6 |
| 8 | Fix (only if 7 says fixable in this environment): apply per 7's named path; session restart if 7 says so (note: the running session holds the in-memory -3 compositor binary; post-restart verification is the -4 steady state, per TASK-0026 side-effect note) | `Tails` | DoD box 3: text-only screenshot evidence (md5/PIL, no image reads) showing the panel bar renders (band analysis rows 0-39 no longer wallpaper texture only; baseline dominant rgb(12,6,19)) and `cinnamon-settings` is a visible window (non-zero pixel diff vs app-killed baseline, excluding operator block regions) | Depends on 7 |
| 9 | Rollback (conditional: item 8 fails, or any item leaves the VM in a worse state): revert per the Rollback section | `Tails` | VM back at pre-task state; if the revert was to `2026-10-04T11:36`, the -4 RPM re-applied from `rpms-local/`; state left behind recorded | Conditional branch, not a chain member |
| 10 | Verification gate + final verdict | `Big` | `## Test Results`: text-only screenshot gate with the TASK-0026 item 3 procedure (pairwise-distinct md5s, byte-diff counts, session journal capture for the test window) and the final verdict per DoD boxes 4-5 | Depends on 8, or on 7 if environment limitation |

**Dependencies and sequence.** 1 to 2 to {3, 4, 5, 6} to 7 to 8 to 10. Items 3-6 are
**independent, explicitly** — nothing orders them against each other; the single inference slot
forces a physical order and the table order is the suggested one (read-only first, disruptive
last). 7 depends on all of 2-6. 8 depends on 7 and is skipped when 7 classifies environment
limitation, in which case 10 follows 7 directly. 9 is a conditional branch.

**Critical path.** 1 to 2 to 3 to 4 to 5 to 6 to 7 to 8 to 10: 9 turns (8 if item 5's kill is
made unnecessary). The longest dependent chain is the whole chain; there is no shorter off-chain
path.

**Estimates** (hours; three-point `T = (O + 4M + P) / 6`):

| # | Item | O | M | P | T |
|---|---|---|---|---|---|
| 1 | Checkpoint snapshot | 0.25 | 0.5 | 1 | 0.5 |
| 2 | Baseline capture | 0.5 | 1 | 2 | 1.1 |
| 3 | Block identity | 1 | 2 | 4 | 2.2 |
| 4 | X1 anomaly | 1 | 2 | 3 | 2.0 |
| 5 | Wallpaper source | 1 | 2 | 4 | 2.2 |
| 6 | Compositor GL state | 1 | 3 | 6 | 3.2 |
| 7 | Classification | 0.5 | 1 | 2 | 1.1 |
| 8 | Fix + verify | 2 | 4 | 8 | 4.3 |
| 10 | Big gate + verdict | 1 | 2 | 4 | 2.2 |
| | **Total nominal** | | | | **18.7** |
| 9 | Rollback (conditional) | 0.5 | 1 | 2 | 1.1 |

Buffer: unknown root cause, operator-live machine, single inference slot: +35% (about 6.5 h).
**Planned total about 25 h** (three business days single-threaded).

**Risks.**

| Risk | Likelihood | Impact | Mitigation | Contingency |
|---|---|---|---|---|
| Checkpoint fails or disk full (old environment disks are gone; no second copy of this disk exists) | Low | High (no rollback) | `df` gate and `qemu-img info` in item 1 before anything else | Read-only diagnosis (items 2-7) still completes; fix path blocked; record in `## Status` via PM |
| `snapshot-revert` fails at rollback time (external chain damaged) | Low | Severe | Item 1 records `qemu-img info` on both chain files; `snapshot-info` re-checked before any revert | Reinstall Cinnamon RPM set from signed `rpms/`, re-apply the -4 RPM (artifact verified present 2026-10-07 at `~/Linux/projects/cinnamon-for-rocky10/rpms-local/cinnamon-6.7.4-4.el10.x86_64.rpm`), manual session restore |
| Fix needs VM/session restart: disturbs the operator's live desktop (expected: DoD fixes are session/display state) | High | Medium | Disruptive items ordered last (5, 8); checkpoint always first; time of disturbance recorded in `## Implementation` | Restore via checkpoint revert (running-state snapshot, revert with domain running per A6); operator re-logs in via GDM |
| 32k turn cap truncates an evidence-heavy turn (already happened on this team) | Medium | Medium | Briefs carry at most three file edits; findings as one-liners plus commands, never output dumps; small passes per AGENTS.md section 14 | Re-dispatch with a smaller brief; detect via session DB (`finish: "length"`, `tokens.output = 32000`) per section 14 |
| Verdict is environment limitation (GL pipeline unfixable under this QEMU config) | Medium | None (valid DoD outcome) | Item 6 tests it directly (render node presence, GL context) | `## Test Results` documents what would make it testable (3d display config, real GPU, different QEMU display) per DoD box 4 |
| `/tmp` screenshot artifacts lost (host reboot) | Low | Low | md5s, sizes, and band-analysis numbers recorded in the doc | Re-capture next turn |
| -4 RPM lost on revert to `2026-10-04T11:36` (snapshot predates the install; the delta holds it) | Certain if that path is taken | Low | Rollback names the re-apply; artifact existence verified 2026-10-07 | Re-apply: `scp` to VM `/tmp/` plus `sudo dnf install --nogpgcheck` (VM repo gpgcheck=1; -4 is unsigned) per the TASK-0026 procedure; mandatory before TASK-0026 item 3 can pass (`cinnamon-settings` crashes at startup without it) |
| Session restart changes the running compositor binary (in-memory -3 to on-disk -4) | Certain if a session restart happens | Low | Controlled variable, not a risk: post-restart verification is the -4 steady state; if -4 also no-renders, the -4 install is exonerated | Record both observations in `## Implementation` |

**Validation.** Environment: `Rocky_Linux_10_Cinnamon` (192.168.122.4), session 2, seat0/tty2;
all `virsh` with `-c qemu:///system`; SSH as `howard` (password per A4, never written). Checks:
(1) items 2-6 each land command + output in `## Implementation`; a before/after read-only diff
(screenshot md5s, band analysis, `/tmp/.X11-unix`, `ss -xp`) proves no accidental VM change from
the read-only phase. (2) The fix gate (item 8), text-only, no image reads: `virsh screenshot` to
`/tmp`, panel = band analysis rows 0-39 no longer wallpaper texture only, app = A/B pixel diff
(alive vs killed) non-zero with operator block regions excluded. (3) Consistency with TASK-0026
item 3: the same procedure as Big's 12-pane gate (pairwise-distinct md5s, byte-diff counts,
`journalctl --user` capture for the test window), so the 12-pane gate runs immediately after the
fix lands with zero new procedure. (4) `## Test Results` final verdict written by `Big`.
(5) TASKS.md row status updated by `Robotnik`. If item 8 changed repo files, the standard review
chain (Shadow to Omega to Big to Charmy) runs over the diff before the `Knuckles` checkpoint
commit (TASK-0026 pattern; the `cinnamon/` checkout is never pushed, per the TASK-0026
2026-10-07 PAT resolution); if the fix is VM state only, item 10's gate plus the `## Test Results`
verdict is the gate and the `Knuckles` checkpoint covers the planning docs.

**Rollback.** Detection: panel band analysis still wallpaper-only after item 8; A/B diff still 0;
VM fails to boot or GDM login breaks after a restart; a snapshot-revert error. Exact reverts:
- Preferred (preserves the -4 RPM): `sudo virsh -c qemu:///system snapshot-revert Rocky_Linux_10_Cinnamon 2026-10-07-task0034-pre`. Snapshot state is `running`, so revert with the domain running (A6).
- Full baseline: `sudo virsh -c qemu:///system shutdown Rocky_Linux_10_Cinnamon` (graceful; `destroy` only if shutdown fails), then `sudo virsh -c qemu:///system snapshot-revert Rocky_Linux_10_Cinnamon 2026-10-04T11:36` (state `shutoff`, so the VM must be shutoff), boot, and re-apply the -4 RPM (see risk table; mandatory before TASK-0026 item 3).
- Point of no return: none for the disk while the external chain is intact (worst case is a known
  recoverable state: VM at `2026-10-04T11:36` plus the -4 RPM re-applied). The real one is a
  `destroy` (not `shutdown`) of the running VM mid-delta-write, which can corrupt the delta file
  and lose all post-2026-10-04 state; mitigate by always trying `shutdown` first. The
  operator's in-memory session state is not recoverable (accepted, A1).
- State left behind after a failed run and checkpoint revert: VM at pre-task state (the -4 RPM
  present), fresh screenshots in `/tmp` (harmless), Tails' entries in `## Implementation` (the
  durable record). A retry re-enters at item 2 (state re-capture) or at item 8 with a new
  hypothesis from item 7's re-run.

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

### 2026-10-08: Tails diagnosis items 1-7 (part 1 of up to 3: items 1-2)

**Item 1 — pre-task checkpoint.** Command + output:
- `df -h /` before anything: 39G free on `/` (4 GB gate: pass).
- `sudo -n qemu-img info /var/lib/libvirt/images/Rocky_Linux_10_Cinnamon.2026-10-04T11:36` on the live file failed (QEMU holds the exclusive lock); run on a `sudo cp` copy in `/tmp/opencode/` (copy deleted after): `file format: qcow2, virtual size: 20 GiB, disk size: 720 MiB, backing file: /var/lib/libvirt/images/Rocky_Linux_10_Cinnamon.qcow2, corrupt: false`.
- `virsh -c qemu:///system snapshot-create-as Rocky_Linux_10_Cinnamon 2026-10-07-task0034-pre` → `Domain snapshot 2026-10-07-task0034-pre created` (rc=0).
- `virsh -c qemu:///system snapshot-list Rocky_Linux_10_Cinnamon` → `2026-10-04T11:36  2026-10-04 20:36:44 +0900  shutoff` and `2026-10-07-task0034-pre  2026-10-08 00:35:55 +0900  running`.
- `virsh -c qemu:///system snapshot-info ... 2026-10-07-task0034-pre` → `State: running, Location: internal, Parent: 2026-10-04T11:36, Current: yes, Metadata: yes`.
- `qemu-img info` on a fresh delta copy: `Snapshot list: ID 1 TAG 2026-10-07-task0034-pre 1.62 GiB 2026-10-08 00:35:55` (the checkpoint physically lives in the delta file's qcow2 header).
- VM stayed running throughout: `dominfo` state `running`, CPU time monotonic (1043.9s → 1045.5s), domain id 2 unchanged.

**Plan deviation (recorded, acceptance criteria met):** the plan says "external snapshot". libvirt 11.10.0 on Rocky 10.2 creates an **internal** snapshot by default for a running domain; external snapshots are created only of shutoff domains (the known error path is `Operation not supported: live disk snapshot not supported with this QEMU binary`), so on a running VM internal is the only form that does not disturb the operator's desktop. Acceptance criteria (`snapshot-list` shows both snapshots with the right states; free space recorded) are met. Revert semantics, documented evidence (a live revert test is destructive to the operator's session and was not done): libvirt `virsh` man page says a revert to an active state from a running domain reuses the existing hypervisor except for provably incompatible configuration or an inactive snapshot combined with `--start`/`--paused`; libvirt's own docs state internal snapshots are "fully supported by libvirt (creation, revert, and deletion)"; the libvirt-11.2/11.3 internal-revert regression is fixed in 11.10.0 (release notes). Second rollback tier unchanged: `2026-10-04T11:36` (external, shutoff) plus the -4 RPM re-apply path.

**Item 2 — read-only baseline capture.** Zero VM state change (all reads; the only writes this task so far are item 1's snapshot and this doc).
- `virsh -c qemu:///system vncdisplay Rocky_Linux_10_Cinnamon` → `127.0.0.1:1` (port 5901).
- `ss -ltnp` (host, `sudo -n` for process names): `127.0.0.1:5901` → `qemu-kvm` pid 18687 (this VM's VNC); `127.0.0.1:5900` → `qemu-kvm` pid 18651 (the other VM, `Fedora_45_Cinnamon`). **No 6080/websockify listener exists on the host** (the item-2 parenthetical's 6080 target is absent; the operator's path is Cockpit Machines on 9090, which proxies VNC itself).
- `virsh dumpxml` (this VM): `<graphics type='vnc' port='5901' autoport='yes' listen='127.0.0.1'/>`; `<video><model type='virtio' heads='1' primary='yes'/></video>` — **A5 confirmed: no 3d/virgl element**; `<serial type='pty'>` source `/dev/pts/3`, `<model name='isa-serial'/>` target port 0; `<channel type='unix'>` virtio-serial `org.qemu.guest_agent.0` state connected; `<audio id='1' type='none'/>`; `<input type='tablet' bus='usb'/>`.
- Guest `/dev/dri`: `card0` (226:0, root:video, 0660) and `renderD128` (226:128, root:render, 0666) — the virtio GPU exposes both DRM nodes.
- Guest `/tmp/.X11-unix`: `X0`, `X1` (both howard, both created 2026-10-05 15:10:59.250285710 — same microsecond) and `X1024`, `X1025` (gdm, 15:10:37).
- Guest `ss -xp`: 554 ESTAB unix sockets, **0 LISTEN lines** (guest ss quirk; listener sockets were identified from the fd tables instead). Key pairs: `@/tmp/.X11-unix/X1` server sockets held by `Xwayland` pid 3003 (fd 6/9/10/11/12) with clients `csd-xsettings` 3114 fd3, `csd-clipboard` 3123 fd3, `csd-power` 3124 fd3, `csd-media-keys` 3125 fd3, `cinnamon` 2961 fd64; `/run/user/1000/wayland-0` ESTAB pairs attributed to pid 2961 (in-process Wayland clients); `/run/user/1000/pulse/native` client end in `cinnamon` fd 78 (peer `pipewire-pulse` 3159 fd 27).
- **Session output location:** `cinnamon`/`Xwayland`/`ibus-daemon` all hold fd1+fd2 → socket inodes 16550/16551, and ino 16551 is bound to `/run/systemd/journal/stdout` (peer held by journald). So session stdout/stderr go to the journal (this answers TASK-0026 open question 8, which had it unverified); fd0 → `/dev/null`.
- `loginctl list-sessions`: session 2 (howard, seat0, tty2, class `user`, leader 2848 `gdm-session-worker [pam/gdm-password]`), session 3 (manager, leader 2859), session 38 (this SSH, transient). Session 2 `IDLE SINCE`: **2 days ago** (no operator input currently).
- `ps aux` (full; kernel threads `[...]`, 105 lines, omitted here): the session user-space set, verbatim relevant lines:
  - `howard 2859 /usr/lib/systemd/systemd --user`; `2883 /usr/libexec/gdm-wayland-session --handle-registration cinnamon-session-cinnamon --wayland`; `2898 /usr/libexec/cinnamon-session-binary --session cinnamon-wayland`; **`2961 /usr/bin/cinnamon --replace`** (alive, started Oct 05, tty2); `3003 /usr/bin/Xwayland :0 -rootless -noreset -accessx -core -auth /run/user/1000/.muffin-Xwaylandauth.2T7LW3 -listen 4 -listen 5 -displayfd 6 -initfd 7`; `3102 csd-settings-remap`; **`3103 csd-background`** (tty2); `3108 csd-screensaver-proxy`; `3112 csd-a11y-settings`; **`3114 csd-xsettings`**; `3121 csd-housekeeping`; **`3123 csd-clipboard`**; **`3124 csd-power`**; `3125 csd-media-keys`; `3127 csd-keyboard`; `3063 ibus-daemon --panel disable`; `3157 pipewire` / `3158 wireplumber` / `3159 pipewire-pulse`; `3297 seapplet`; **`3299 gnome-software --gapplication-service`**; `3306 nemo-desktop` (tty2); `3341 xdg-desktop-portal`; `3376 xdg-desktop-portal-gtk`; `1265 /usr/sbin/gdm`; `1206 sshd`.
- `/proc/2961/fd`: fd0 `/dev/null`; fd1,2 `socket:[16550]` (journal, above); fd3 `socket:[17524]` (env `WAYLAND_SOCKET=3`, the Wayland client socket); **fd11,14,20 `/dev/dri/card0`** (DRM master node, three fds); fd15 `/dev/udmabuf`; fd16 `/memfd:lp_dma_buf`; fd17 `/dmabuf:`; fd33,75 `/memfd:muffin-shared`; fd25-29 `/dev/input/event0..4`; fd38 `/run/user/1000/wayland-0.lock`; fd59,60 `socket:[17050]` and fd65,66 `socket:[19083]` (both-ends-in-2961 = Wayland server sockets on `wayland-0`); fd78 `socket:[20877]` (PipeWire native client end).
- `/proc/2961/maps` (GL/dri lines): `libgallium-25.2.7.so`, `libEGL_mesa.so.0.0.0`, `libEGL.so.1.1.0`, `libGLX.so.0.0.0`, `libGLdispatch.so.0.0.0`, `libgbm.so.1.0.0`, `libGL.so.1.7.0` all mapped; four `/dev/dri/card0` GEM buffer mappings (`rw-s 101810000`, `rw-s 101400000`, `-w-s 1003f0000`, `-w-s 1003ec000`); `/home/howard/.cache/mesa_shader_cache/index` mapped. **No fd anywhere in 2961 points at `renderD128`** (all DRI fds are `card0`).
- `/proc/2961/environ`: `DESKTOP_SESSION=cinnamon-wayland`, `XDG_SESSION_TYPE=wayland`, `XDG_SESSION_ID=2`, `XDG_SEAT=seat0`, `XDG_VTNR=2`, `XDG_CURRENT_DESKTOP=X-Cinnamon`.
- `/proc/3003/environ` (Xwayland): `DISPLAY=:0`, **`GNOME_SETUP_DISPLAY=:1`**, `WAYLAND_DISPLAY=wayland-0`, `WAYLAND_SOCKET=3`, `XAUTHORITY=/run/user/1000/.muffin-Xwaylandauth.2T7LW3`.
- `/proc/3003/fd` (all 13): fd0 `/dev/null`; fd1,2 journal; fd3 Wayland client; fd4,5 `socket:[17499/17500]` (the two `-listen` TCP sockets); fd6-12 the five `@/tmp/.X11-unix/X1` ESTAB sockets (fd6 `[17126]`, fd9 `[17129]`, fd10 `[17132]`, fd11 `[17135]`, fd12 `[17139]`); **no fd holds the `/tmp/.X11-unix/X0` socket (ino 1276945) — and no process on the guest holds it at all** (checked `/proc/[0-9]*/fd`): X0 is a stale file.
- `dri` fd sweep across all howard processes: only pids 2961 (fd11/14/20) open DRI nodes, all `card0`; `renderD128` is open by nobody.
- `/sys/class/drm`: `card0`, `card0-Virtual-1` (connector, `status=connected`), `renderD128`.

*— Tails, 2026-10-08, part 1 of up to 3 (items 1-2 complete) —*

### 2026-10-08: Tails diagnosis items 1-7 (part 2 of up to 3: live-state verification + items 3-7)

**Live-state verification (part-1 claims).** All verified against live state, zero VM state change (reads only; the only writes this task has made are item 1's snapshot and this doc):
- `virsh -c qemu:///system dominfo Rocky_Linux_10_Cinnamon` → `Id: 2`, `State: running`, CPU time 1299.5s (monotonic from part-1's 1045.5s, i.e. the VM kept running).
- `virsh -c qemu:///system snapshot-list Rocky_Linux_10_Cinnamon` → `2026-10-04T11:36  shutoff` and `2026-10-07-task0034-pre  running`.
- `virsh -c qemu:///system snapshot-info ... 2026-10-07-task0034-pre` → `Current: yes`, `State: running`, `Location: internal`, `Parent: 2026-10-04T11:36`.
- `virsh -c qemu:///system vncdisplay Rocky_Linux_10_Cinnamon` → `127.0.0.1:1` (port 5901); host `sudo -n ss -ltnp` → `127.0.0.1:5901` held by `qemu-kvm` pid 18687 (the same pid as part-1).
- Record: this host's `virsh screenshot` has no `--format` option (default output is PNG, not raw); part-1's `qemu-img`-on-a-copy and the rest stand unchanged.

**Item 3 — moving external block identity.** Command: `virsh -c qemu:///system screenshot Rocky_Linux_10_Cinnamon <file>` (PNG) + `md5sum` + PIL (text-only; no image reads to the model).
- The block is a sparse cluster of bright (white) pixels, ~180x58 (b0 bright region x128-308, y355-412), ~24% white (2059 white px of 10440 in the crop; top colour (254,254,254)). It is NOT a solid white box; the content is sparse text/icons on the dark wallpaper.
- Motion, tracked across 5 screenshots (t0/t8/t15/t27/t39s): the block sits at 3x3 grid-cell centres and JUMPS between them, static in between. b0: middle-left (121,355). b1: middle-center (548,355). b2: middle-center (md5 `afd1bda7…`). b3: middle-center (md5 identical to b2, i.e. static for 12s). b4: bottom row (?,622) (md5 `e464651d…`, bright content appears lower). So it is mostly static with occasional position jumps, not continuous motion.
- Not an X11 window: `xprop -display :0 -root` and `xprop -display :1 -root` both show `_NET_CLIENT_LIST` empty (zero X11 clients on either display).
- Not a session-daemon window: the session's user-space apps are nemo-desktop (3306), csd-background (3103), csd-* (3114/3123/3124/3125/3127), seapplet (3297), gnome-software (3299) — background daemons; none opens a ~180x58 white text/icons window.
- It is present even though the session is idle (`loginctl show-session 2` → `State=active`, `IdleHint=yes`, no operator input ~2 days) yet it still jumps position, so it is AUTONOMOUS, not operator-driven. This contradicts TASK-0026's "operator concurrent use" hypothesis for the current state.
- Competing explanations (weighed): (A) compositor-drawn cursor/OSD — fits "renders + moves + not a window" but 180x58 is an atypical cursor size and the ASCII shape (a row of verticals/diagonals) is not an arrow, so not confirmed; (B) a re-mapped surface such as a gnome-software update notification — the journal has `Oct 07 10:12:23 JS LOG: Failed to find flatpak app for notification with desktop-entry hint: org.gnome.Software` (twice), which fits "text + icons + occasional jumps", but the block persists ~2 days after that log (notifications auto-dismiss), so not confirmed; (C) operator concurrent use (TASK-0026) — rejected for the current state because the session is idle yet the block moves.
- Origin (answer): an external, compositor-composited, moving element that is NOT a session X11 or Wayland app window and that moves between 3x3 grid cells. It is a CONFUNDER for A/B screenshot tests and must be EXCLUDED (per the plan's standing hygiene note).
- Key point for the no-render: the block RENDERS (it is composited), so the compositor presents SOME content (the background layer + the block); the no-render is therefore SELECTIVE (the panel + app windows don't present), not "the compositor presents nothing".

**Item 4 — the X1 anomaly.**
- `/tmp/.X11-unix/X1` (ino 1276949) is owned by **Xwayland (pid 3003)**, a child of the compositor (`ps -o ppid` → PPID 2961).
- Xwayland's cmdline says `:0` but it actually serves display **:1**: its environ has `GNOME_SETUP_DISPLAY=:1` and it owns the X1 socket; the display number is passed at runtime via `-displayfd 6` (a file descriptor), overriding the cmdline `:0` placeholder.
- `/tmp/.X11-unix/X0` (ino 1276945) is STALE: no process holds it (not in 3003's `/proc/3003/fd`, not in 2961's, and part-1's full `/proc/[0-9]*/fd` sweep found no holder; still true now).
- X1's ESTAB clients (the session's X11 clients): csd-xsettings (3114), csd-clipboard (3123), csd-power (3124), csd-media-keys (3125), cinnamon/compositor (2961).
- The session env (nemo, csd-*, all daemons) has `DISPLAY=:0` (stale) but `WAYLAND_DISPLAY=wayland-0` (live). So Wayland apps use wayland-0 (live); an X11 app would use `DISPLAY=:0` → the STALE X0 → "Cannot open display" (it cannot reach the live X server on :1).
- Can app windows map there: X11 apps point at the dead :0 (no); Wayland apps go to wayland-0 (the compositor). So the X1 anomaly (a display-number mismatch: the session's X11 is on :1 but the env says :0, plus a stale X0) is a REAL but SECONDARY issue — it would break X11 apps, but it does NOT cause the in-process panel no-render (the panel is Wayland, see item 6).
- Why Xwayland is on :1: the compositor (2961) launches Xwayland (PPID 2961) and passes the display number via `-displayfd` from `GNOME_SETUP_DISPLAY=:1` (set by the session setup), so the session's X11 is assigned to :1.

**Item 5 — wallpaper source.**
- Wallpaper config: `gsettings get org.cinnamon.desktop.background picture-uri` → `file:///usr/share/backgrounds/rocky-default-10-gemstone-skies-time.xml` (a GNOME day/night XML wallpaper), `picture-options` → `zoom`. The on-screen wallpaper (dark purple, dominant rgb(10,6,19)) matches the NIGHT variant of that wallpaper.
- The wallpaper is drawn by **nemo-desktop (pid 3306)**, a live Wayland client (journal `nemo-desktop: using Wayland backend, gtk-layer-shell supported`), as a layer-shell BACKGROUND-layer surface. (csd-background (3103), from `cinnamon-settings-daemon-6.7.2-2.el10`, is also a Wayland client with the same `gtk-layer-shell supported` log.)
- The wallpaper IS visible (presented) → the compositor IS compositing + presenting at least one client surface (nemo's background-layer surface).
- NOT settled by a kill: the plan's destructive A/B kill test (kill nemo-desktop/csd-background) was NOT done, because it would disturb the operator's live desktop (read-only constraint, do-not-kill-nemo-desktop). It was instead determined by (a) the on-screen wallpaper matches the configured wallpaper file that nemo reads, (b) nemo is a live layer-shell Wayland client, and (c) the wallpaper is visible. This is consistent but not 100% conclusive between nemo and csd-background (both are layer-shell clients); nemo is the primary desktop/wallpaper drawer in Cinnamon.
- Key point: a client surface (the wallpaper) presenting PROVES the compositor presents client surfaces; so the no-render is selective (top layer + normal windows), not "no client surfaces present".

**Item 6 — compositor output/GL state.** Command: `journalctl _PID=2961`, `/proc/2961/{fd,maps}`, `/sys/class/drm/`.
- GL state: `GL renderer: llvmpipe (LLVM 21.1.8, 256 bits)` — the compositor is on **software GL (llvmpipe)**, not a hardware GPU.
- `Failed to initialize accelerated iGPU/dGPU framebuffer sharing: Do not want to use software renderer (llvmpipe ...), falling back to CPU copy path` — the compositor REFUSES the accelerated framebuffer-sharing path (because it is on a software renderer) and uses the **"CPU copy path"** fallback.
- `/proc/2961/maps`: `libEGL_mesa`, `libgallium-25.2.7`, `libGL`, `libGLX`, `mesa_shader_cache` (Mesa/gallium present). `/proc/2961/fd`: `/dev/dri/card0` (fd11/14/20); **no fd points at renderD128** (all DRI fds are card0; renderD128 is open by nobody — consistent with part-1).
- DMABUF: `DMABUF: native backend, 1 GPU(s): GPU /dev/dri/card0 [PRIMARY]`, `primary device path = /dev/dri/renderD128`, `advertising zwp_linux_dmabuf_v1 version 4 (main_device set)`. So the compositor advertises a render node (renderD128) to Wayland clients for dmabuf, even though it is itself rendering in software (llvmpipe).
- Xwayland (3003): `Refusing to try glamor on llvmpipe`, `EGL setup failed, disabling glamor`, `Failed to initialize glamor, falling back to sw` — Xwayland is also on software (no GL).
- Output: `/sys/class/drm/card0-Virtual-1/status` → `connected`; `modes` includes `1280x800` (the active mode). Single output (card0-Virtual-1), 1280x800; the compositor is the DRM master (only 2961 holds card0).
- Frame callback: `0xa0000b: frame_complete callback never occurred for frame 2` (ONE surface, at session start 15:11:02). Only ONE such warning (not systemic) → it is specific to that surface (0xa0000b), not a global presentation failure.
- Where `/proc/2961/fd/1-2` point: `socket:[16550]` (the journal stdout socket; session output goes to the journal — part-1).
- No `strace` run (it would stop the process = disruptive; the journal + fd + maps + sysfs already answer the GL state).

**Item 7 — classification + fix path.**
- Root cause (evidence from items 2-6): the compositor (muffin, in-process `cinnamon --replace`, pid 2961) is **not compositing/presenting the in-process panel (top layer) or launched app windows (normal windows)** into the output frame. It DOES composite/present the background layer (nemo's wallpaper, item 5) + one moving element (the block, item 3). The no-render is SELECTIVE. The top (panel) band (rows 0-39) shows the wallpaper texture (dominant rgb(10,6,19)), not a panel bar (b0 band analysis).
- The compositor is on **software GL (llvmpipe) + "CPU copy path"** (item 6) because the guest's virtio-gpu device is NOT providing a hardware GL context to the guest (so the guest's Mesa falls back to llvmpipe). The VM's display config is a bare virtio with no 3D (A5, part-1). The HOST has GPUs (Intel TigerLake-H UHD + NVIDIA GA107M RTX 3050; `/dev/dri/renderD128` + `renderD129`), so hardware 3D is potentially available to the guest but is not being used.
- The X display mismatch (item 4) is a REAL but SECONDARY issue (it would break X11 apps); it does NOT cause the in-process panel no-render (the panel is Wayland).
- **Classification: environment limitation (VM display/GPU pipeline).** The guest's display pipeline is not providing hardware 3D acceleration, forcing the compositor into the software llvmpipe + "CPU copy path", under which the compositor composites/presents the background layer (wallpaper) but not the top layer (in-process panel) or normal windows (launched apps). It is NOT a session configuration defect (the session is correctly configured; X1 is a separate secondary issue). It is NOT confirmed to be a Cinnamon port bug: a compositor software-path bug (upstream muffin or the port) CANNOT be fully exonerated without a hardware-GL test or source inspection (bounded uncertainty, stated).
- **Named fix path** (in scope per A3; requires a VM restart per A1/DoD box 3): **enable hardware 3D acceleration for the guest's display** so the guest's Mesa gets a hardware GL context (instead of llvmpipe) and the compositor uses the accelerated framebuffer-sharing path. Concretely: configure the QEMU virtio-gpu to use the host's render node (`/dev/dri/renderD128` or `renderD129`) for 3D (QEMU XML `<video>` config + ensure the QEMU process can access the host's render node, SELinux context). If the guest then uses a hardware GL context (not llvmpipe), the compositor should composite + present all surfaces (panel + app windows).
- What would make it testable if the fix does not land here: if after enabling 3D the guest STILL falls back to llvmpipe (host GPU not usable by QEMU — SELinux, driver, or the GPU not exposing a usable render node to QEMU), then the defect is a compositor software-path bug (upstream muffin or the Cinnamon port) and would require (a) source inspection of the port's compositor presentation path, (b) a Fedora-VM comparison (same display config) to see whether it is config-specific, or (c) a different QEMU display device (virgl/qxl 3D, or GPU passthrough) to make it testable.
- **Remaining (not done this part):** item 8 (apply the fix + verify with text-only screenshot evidence) and item 9 (conditional rollback) are NOT done — they are a separate dispatch per the plan (the fix requires a disruptive VM restart, in scope per A1/DoD box 3). Item 10 (Big gate + final verdict) follows.

*— Tails, 2026-10-08, part 2 of up to 3 (items 3-7 complete) —*

### 2026-10-08: Tails fix items 8-9 (part 3 of up to 3: named fix path; fix not possible in this environment; zero VM state change)

**Item 8 — named fix (hardware 3D for the guest display via QEMU virtio-gpu on the host render node): not possible in this environment; fix not applied.**
- Pre-fix state (read-only, all `virsh -c qemu:///system`): `dominfo` → Id 2, running, CPU time 1352.3s (monotonic from part 2's 1299.5s); `snapshot-list` → `2026-10-04T11:36` shutoff + `2026-10-07-task0034-pre` running; `vncdisplay` → 127.0.0.1:1; host `df -h /` → 37G free.
- Defect still live (pre-fix screenshot, text-only md5/PIL, no image reads): `sudo virsh -c qemu:///system screenshot Rocky_Linux_10_Cinnamon /tmp/opencode/prefix.png` → md5 `10a602297f86214ebdf9819af5c07d22`, 1280x800. Band rows 0-39 (51200 px): 47.3% within ±6 of the baseline dominant rgb(12,6,19); 94.5% (48401 px) in the wallpaper dark range (max channel < 40); top-10 colours all wallpaper dark-purple family: rgb(10,6,19) 13.8%, rgb(10,5,19) 6.0%, rgb(11,6,19) 4.2%, rgb(13,6,19) 3.0%, rgb(38,9,20) 2.6%, rgb(23,7,19) 2.5%, rgb(40,10,20) 2.3%, rgb(14,6,19) 2.3%, rgb(15,6,19) 2.2%, rgb(12,6,19) 2.1% (the baseline dominant is present); the 5.5% non-dark pixels are also wallpaper family (top rgb(40,10,20)). No grey/white panel-family colour anywhere in the band → **rows 0-39 still wallpaper texture only**.
- Host 3D capability (decisive; host-side, read-only):
  - Binary `/usr/libexec/qemu-kvm`, `--version | head -1` → `QEMU emulator version 10.1.0 (qemu-kvm-10.1.0-16.el10_2.5)`; the only QEMU display binary on the host (`/usr/bin` holds qemu-edid/img/io/keymap/nbd/pr-helper/storage-daemon only).
  - `qemu-kvm -device help | grep -iE 'virtio-gpu|qxl|virtio-vga|virtio-ramfb'` → only `virtio-gpu-device` (virtio bus), `virtio-gpu-pci` (PCI, alias `virtio-gpu`), `virtio-vga` (PCI) — **no qxl, no virtio-gpu-3d display device in this build**.
  - `strings /usr/libexec/qemu-kvm | grep -cE 'virglrenderer|virtio-gpu-3d|libvirgl'` → 0 (no 3D/virgl code compiled in).
  - `ldd /usr/libexec/qemu-kvm | grep -iE 'virgl|spice|libegl|gbm|libdrm'` → empty (no virgl/egl/gbm linkage).
  - `rpm -qa | grep -iE 'virgl|spice'` → empty (no virglrenderer installed).
  - `dnf -q list available | grep -iE 'qemu-kvm|virgl|spice'` → only `qemu-kvm-block-curl` 18:10.1.0-16.el10_2.5 (appstream), `spice-protocol` 0.14.4-7.el10 (crb), `spice-vdagent` 0.22.1-7.el10 (appstream) — **no package on this host provides a virglrenderer or a 3D display device, and no alternative qemu-kvm build exists**.
  - libvirt XML probe (scratch domain, never left defined): `sudo virsh -c qemu:///system define /tmp/opencode/schematest-3d.xml` on a minimal domain with the classic 3D form `<video><model type='qxl' vram='16777216' heads='1' vram64='yes' primary='yes'><acceleration 3d='on'/></model></video>` → `error: at line 17: error parsing attribute name` at `3d` (not parseable by libvirt 11.10.0-12.4.el10_2.5); `dumpxml --inactive` empty, `undefine` → `failed to get domain 'task0034-schematest'` (nothing was defined); scratch qcow2 + XML deleted. Moot in any case: the QEMU build has no 3D device for any XML form to map to.
- Conclusion: this host's QEMU cannot hand the guest a hardware GL context through any display device (no 3D display device, no virglrenderer linkage or code, nothing installable to provide it), so the guest's Mesa can only obtain llvmpipe on the bare virtio device and the compositor stays in the llvmpipe + "CPU copy path" state (part 2 item 6). The named fix path cannot be applied in this environment. Per the operator brief: stop and record the environment-limitation verdict in `## Test Results` with what would make it testable (done; see `## Test Results`).
- Host render nodes (for the testability record): `udevadm info /dev/dri/renderD128` → `DEVPATH=/devices/pci0000:00/0000:00:02.0/drm/renderD128` → Intel TigerLake-H UHD (`lspci`: `00:02.0 ... Intel TigerLake-H GT1 [UHD Graphics]`); `udevadm info /dev/dri/renderD129` → `DEVPATH=/devices/pci0000:00/0000:00:01.0/0000:01:00.0/drm/renderD129` → NVIDIA GA107M (`lspci`: `01:00.0 ... NVIDIA GA107M [GeForce RTX 3050 Mobile]`). `/sys/class/drm`: card1 (NVIDIA) holds all host display connectors (card1-eDP-1, card1-DP-1, card1-HDMI-A-1, card1-HDMI-A-2); card0 (Intel iGPU) has none — headless, so offscreen virgl on renderD128 would not contest the host's live display. `getenforce` → Enforcing; the domain's SELinux label is `system_u:system_r:svirt_t:s0:c253,c1003` (`dominfo`); s virt access to the render nodes was never reached or tested (the component gap precedes it).
- Guest-side readiness (recorded for the testability record; guest, via `howard`): `rpm -q cinnamon mesa-dri-drivers` → `cinnamon-6.7.4-4.el10.x86_64` (the -4 steady state is on disk) + `mesa-dri-drivers-25.2.7-4.el10.rocky.0.1.x86_64`; qxl kernel module present: `ls /lib/modules/6.12.0-211.61.1.el10_2.x86_64/kernel/drivers/gpu/drm/qxl/` → `qxl.ko.xz`; Mesa monolith `/usr/lib64/libgallium-25.2.7.so`: `strings | grep -c` → `qxl: 0`, `virtio: 1` (the one line is `virtio_gpu`, the virtio-gpu DRM driver name), `virgl: 7`; virgl strings include `No virgl contexts available on host`, `VIRGL_DEBUG`, `virgl_shader_sync`, `/tmp/.virgl_test` → the **Mesa virtio gallium screen driver (virgl client) is compiled in**, the legacy qxl gallium driver is not; the virtio-gpu kernel driver is already loaded (the guest's live display, part 1/2). No guest-side change is needed for the named fix path.
- No VM session restart was performed: the fix requires applying the display config first, and it cannot be applied here. The operator's session is untouched: session 2 active, IdleHint=yes, same pids as part 1/2 (`cinnamon` 2961, `Xwayland` 3003).

**Item 9 — conditional rollback: not triggered.**
- Plan triggers (item 8 fails after a change, VM in a worse state, boot/login failure, snapshot-revert error): none met — no fix was applied and no change was made to the VM.
- State left behind (post-run, all `virsh -c qemu:///system`): `dominfo` → Id 2 running; `snapshot-list` → both snapshots intact, same states (`2026-10-04T11:36` shutoff, `2026-10-07-task0034-pre` running); `vncdisplay` → 127.0.0.1:1; guest session pids unchanged (2961/3003); guest `/dev/dri` unchanged (card0, renderD128). No revert executed.
- Host artifacts: `/tmp/opencode/prefix.png` (pre-fix screenshot; harmless, left in place); scratch `qcow2` + schema XML created and deleted; no scratch domain left defined.

*— Tails, 2026-10-08, part 3 of up to 3 (items 8-9) —*

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

**Workflow run:** 2026-10-08, `Big` — 12-pane screenshot gate on `Rocky_Linux_10_Cinnamon` (plan
item 10; consistent with TASK-0026 item 3). Run start 2026-10-08T09:51:05Z (epoch 1791453065).
Text-only evidence (md5/PIL); no image reads. Full evidence: the dated `Big` entry below.

| Check | What it exercises | Result | Notes |
|---|---|---|---|
| Baseline screen capture | Pre-launch display state | PASS | frame 00 md5 `57f2e2080f54a92fa9bb40cff7117872`, 527694 B, 5703 unique |
| Guest session state over SSH | Live desktop session before test | PASS | session 2 active (Wayland, `cinnamon-wayland`) |
| Pane-to-module mapping | 12 panes resolve to `cs_` modules | PASS | 11 resolved from `SidePage(` titles; Updates has no module (screenshot only) |
| 12 launches, per-pane screenshot | Control Center + all panes launch | FAIL (expected) | all 12 ALIVE (pids 21482-22492), all killed by recorded pid; no pane window rendered |
| Pairwise pane md5 | Distinct panes produce distinct frames | FAIL (expected) | 14 frames, 4 distinct md5s; within-group consecutive diffs 0/0 |
| Byte diff vs previous frame | Frame change equals rendering | FAIL (expected) | non-zero diffs = time-based wallpaper animation + moving external block only |
| Per-pane console errors | Pane load errors | FINDING | 11/12 clean; Power pane: D-Bus `Unauthorized (36)` traceback, app survived |
| Session journal, test window | Session/app log for the window | N/A | no user-journal files on Rocky; system scope: 291 lines, sshd/logind only |
| Final state verification | No residue, session intact | PASS | session pids unchanged; no leftover `cinnamon-settings`; 25 guest artifacts |

**Checks requested vs run:** all requested gate checks executed (baseline, session state, module
mapping, 12 launches + screenshots, pairwise pane md5s, byte-diff counts vs previous frame,
journal both scopes, final state). No checks dropped or skipped. Two harness bugs were hit and
fixed mid-run (a `pkill -f` pattern that matched and killed the remote shell's own cmdline;
unquoted parentheses in a remote `bash -c` echo arg); the gate was then re-run once cleanly.

**Verdict:** gate FAIL, as expected: the no-render state is recorded as-is (no fix attempted).
Not a code bug (the item-8 environment-limitation verdict stands) and not a harness bug. DoD
box 3 (fix + verify) is N/A — not fixable in this environment per item 8; box 4 is satisfied by
the Tails item-8 entry (environment limitation plus what would make it testable); box 5 is this
verdict plus the dated `Big` entry below. The Power-pane D-Bus `Unauthorized (36)` is a real
console error in an app that survived; recorded for the review chain, not routed to `Tails`.
The item-8 bounded uncertainty (a compositor software-path bug cannot be fully exonerated
without a hardware-GL control) remains open.

### 2026-10-08: Tails item 8 — environment-limitation verdict (recorded in `## Test Results` per the
operator brief for this dispatch; `Big`'s item 10 final verdict and 12-pane gate follow)

**Verdict: environment limitation (confirmed and sharpened by item 8).** The named fix — hardware 3D
for the guest display via QEMU virtio-gpu on the host render node — is **not possible in this
environment**. The host's QEMU (qemu-kvm-10.1.0-16.el10_2.5, `/usr/libexec/qemu-kvm`) has no 3D
display device (`-device help`: only `virtio-gpu-device`, `virtio-gpu-pci`, `virtio-vga`), no
3D/virgl code in the binary (`strings | grep -cE 'virglrenderer|virtio-gpu-3d|libvirgl'` → 0), no
virgl/egl/gbm linkage (`ldd`), and no virglrenderer or 3D renderer package installed or available on
this host (`rpm -qa`; `dnf -q list available | grep -iE 'qemu-kvm|virgl|spice'` → only
`qemu-kvm-block-curl`, `spice-protocol`, `spice-vdagent`). Therefore the guest's Mesa can only
obtain llvmpipe on the bare virtio display device, the compositor's llvmpipe + "CPU copy path" state
(part 2 items 6-7) is the only reachable state in this environment, and the selective no-render
(panel + app windows do not present; wallpaper + the moving block do — pre-fix screenshot md5
`10a602297f86214ebdf9819af5c07d22`, rows 0-39 still wallpaper texture only, 94.5% in the wallpaper
dark range) cannot be tested against a hardware-GL control here. The part 2 classification
(environment limitation, VM display/GPU pipeline) stands; its bounded uncertainty (a compositor
software-path bug cannot be fully exonerated without a hardware-GL test) remains **open**, not
closed, because the hardware-GL control is unreachable in this environment.

**What would make it testable:**
1. A host with a QEMU that has a 3D display device and links virglrenderer (a QEMU built with
   virglrenderer plus a virglrenderer package — neither exists in this host's EL10 repos), plus a
   libvirt 3D video XML for that QEMU (the classic qxl `<acceleration 3d='on'/>` form is not
   parseable by libvirt 11.10.0-12.4.el10_2.5 — "error parsing attribute name" at `3d`; the working
   XML form must be established with that QEMU/libvirt pair), a host render node accessible to the
   QEMU `svirt_t` domain, and a guest Mesa virtio gallium screen driver. The guest side is already
   ready (no guest change needed): `/usr/lib64/libgallium-25.2.7.so` contains the virgl client
   (strings `No virgl contexts available on host`, `virgl_shader_sync`; the one `virtio` string is
   `virtio_gpu`), the virtio-gpu kernel driver is loaded, and the qxl kernel module `qxl.ko.xz` is
   present in guest kernel 6.12.0-211.61.1.el10_2. Host render nodes: `/dev/dri/renderD128` =
   Intel TigerLake-H UHD (`udevadm info` DEVPATH `0000:00:02.0`), headless (no connectors in
   `/sys/class/drm`) and therefore contest-free for offscreen virgl; `/dev/dri/renderD129` =
   NVIDIA GA107M (DEVPATH `0000:01:00.0`), which holds the host's live display outputs
   (card1-eDP-1/DP-1/HDMI-A-1/HDMI-A-2). SELinux is enforcing; `svirt_t` access to the render nodes
   is untested (the component gap precedes it) — check `ausearch -m avc` after the device starts.
2. A different QEMU display device without virgl: GPU passthrough (NVIDIA GA107M via vfio — requires
   a host IOMMU/GRUB change and a host reboot, out of scope here) or a real display/GPU pipeline
   (DoD box 4).
3. If the guest obtains a hardware GL context under (1) or (2) and the no-render persists, the
   defect is a compositor software-path bug (upstream muffin or the Cinnamon port) per part 2 item
   7, testable by source inspection of the port's compositor presentation path or a Fedora-VM
   comparison with the same display config.

**VM state at record:** running, session 2 active idle, zero state change by the item 8 dispatch
(all command + output evidence in `## Implementation` part 3). Checkpoints intact:
`2026-10-07-task0034-pre` (internal, running, Current) and `2026-10-04T11:36` (external, shutoff).

### 2026-10-08: Big — 12-pane screenshot gate (plan item 10); current no-render state recorded as-is

**Scope.** Operator brief: run the 12-pane gate on `Rocky_Linux_10_Cinnamon` consistent with
TASK-0026 item 3 and record the current state as-is; no fix attempted (the item-8
environment-limitation verdict stands). Text-only evidence (md5/PIL); no image reads.

**Environment.** `Rocky_Linux_10_Cinnamon` (virsh id 2, 192.168.122.4), session 2 active (the
operator's live desktop, idle ~3 days; the gate's app launches/kills are the accepted
disturbance). Run start 2026-10-08T09:51:05Z (epoch 1791453065). All guest commands over SSH as
`howard` (sshpass). Artifacts: host `/tmp/opencode/big-t0034-<NN>-<pane>.png` (14 frames,
00-base to 13-accessibility); guest `/tmp/big-t0034-app-<NN>.log` + `.pid` (12 pairs) and
`/tmp/big-t0034-journal.log` (25 artifacts total).

**Procedure.** Launch = `setsid env <session env> cinnamon-settings [module]` with the session
environment captured from session 2 (`HOME=/home/howard USER=howard LANG=en_GB.UTF-8
XDG_RUNTIME_DIR=/run/user/1000 XDG_SESSION_ID=2 XDG_SESSION_TYPE=wayland
DESKTOP_SESSION=cinnamon-wayland XDG_CURRENT_DESKTOP=X-Cinnamon
DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus WAYLAND_DISPLAY=wayland-0`); pid recorded
to a pidfile; stderr/stdout to the pane log; one screenshot after each launch; kill by recorded
pid (never `pkill -f`, which self-matches the remote shell's own cmdline). Pane-to-module
mapping from `SidePage(` titles in `/usr/share/cinnamon/cinnamon-settings/modules/`:

| Pane (DoD order) | Module | Launch pid | Frame |
|---|---|---|---|
| (CC overview) | none | 21482 | 01-overview |
| Desktop | `desktop` | 21572 | 02-desktop |
| Applications | `default` (Preferred Applications) | 21657 | 03-applications |
| Settings | `general` | 21743 | 04-settings |
| Appearance | `themes` | 21830 | 05-appearance |
| Power | `power` | 21918 | 06-power |
| Accounts | `user` | 22020 | 07-accounts |
| Region & Language | `calendar` | 22106 | 08-region-lang |
| Notifications | `notifications` | 22192 | 09-notifications |
| System | `info` | 22275 | 10-system |
| Updates | no `cs_` module (screenshot only, no launch) | — | 11-updates |
| Keyboard | `keyboard` | 22404 | 12-keyboard |
| Accessibility | `accessibility` | 22492 | 13-accessibility |

**Frame data (PIL, text-only).** 14 frames, 4 distinct md5s. Rows 0-39 (top 40 rows, 51200 px)
are 98.1-98.2% wallpaper-dark in every frame: no panel bar in any frame.

| Frame | Pane | md5 | Size (B) | Unique | Raw diff vs prev | Block-excluded diff |
|---|---|---|---|---|---|---|
| 00 | baseline | `57f2e2080f54a92fa9bb40cff7117872` | 527694 | 5703 | — | — |
| 01 | overview | `30ca8c00276d07e4ec227c38a227d57d` | 463608 | 3708 | 1019823 | 760604 |
| 02 | Desktop | = 01 | 463608 | 3708 | 0 | 0 |
| 03 | Applications | `7175fc4a1b35688546cafc73738e3ac5` | 452113 | 3638 | 390966 | 84827 |
| 04 | Settings | = 03 | 452113 | 3638 | 0 | 0 |
| 05 | Appearance | = 03 | 452113 | 3638 | 0 | 0 |
| 06 | Power | `bac74d7cff9d1f24fe08aa5f64c4e3d7` | 452036 | 3807 | 7546 | 2672 |
| 07 | Accounts | = 06 | 452036 | 3807 | 0 | 0 |
| 08 | Region & Language | = 06 | 452036 | 3807 | 0 | 0 |
| 09 | Notifications | = 06 | 452036 | 3807 | 0 | 0 |
| 10 | System | `8d819d294874c26f9c1bc6eb3b84d662` | 451564 | 3823 | 7904 | 3026 |
| 11 | Updates | = 10 | 451564 | 3823 | 0 | 0 |
| 12 | Keyboard | = 10 | 451564 | 3823 | 0 | 0 |
| 13 | Accessibility | = 10 | 451564 | 3823 | 0 | 0 |

Block-excluded = diff with the 3x3 moving-block cells removed (box centers x in {121, 548, 974},
y in {88, 355, 622}; 240x120 boxes). All four non-zero transitions (00->01, 02->03, 05->06,
09->10) are the time-based wallpaper animation (`gemstone-skies-time.xml`) plus moving-block
repositioning; none contains a window. Decisive no-window datum: 06->07, where the app was
killed and a new app launched, is 0/0.

**Console errors.** 11/12 panes: ERR_LINES=0, stderr empty. Power pane only: traceback in
`cs_power.py:883 on_my_value_changed`, D-Bus `Unauthorized (36)`; the process survived through
the pane and was killed by pid. No other console output in any pane log.

**Journal, test window.** User scope: N/A — no user journal files exist on this Rocky guest (no
`/run/user/1000/systemd/user/`, no `~/.local/state/systemd/user/`); session stdout/stderr are
therefore unobservable per part-1 item 2. System scope: 291 lines in the window, sshd/logind
only, zero session/app lines.

**Final state.** Session pids unchanged (2883/2898/2961/3003/3297/3299/3306); no leftover
`cinnamon-settings` process; all 25 guest artifacts present. Nothing else touched.

**Verdict (DoD box 5).** No-render persists, recorded as-is: every frame presents wallpaper
texture and the moving block only. The gate fails for the expected reason and this is the
environment limitation classified in item 8 (bare virtio display, llvmpipe + CPU copy path, no
hardware GL reachable on this host) — not a code bug, not a harness bug. The Power-pane D-Bus
`Unauthorized (36)` is a genuine console error in a surviving app; it is recorded for the
review chain and does not change the no-render verdict. The item-8 bounded uncertainty
(a compositor software-path bug cannot be fully exonerated) stays open pending a hardware-GL
control.

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
