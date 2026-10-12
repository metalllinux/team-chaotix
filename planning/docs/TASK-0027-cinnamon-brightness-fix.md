# TASK-0027 — Cinnamon brightness: Settings and keyboard shortcuts have no effect

> **Section order below is fixed.** Each agent writes to its own section and no other. `Robotnik`
> reads only `## Status` and `## Next Actions`. Do not reorder, rename, or remove sections.

- **Created:** 2026-10-01

---

## Status

### 2026-10-12: items 1-4 complete; verdict BOTH (P1 port bug + E1 environment limitation); fix phase unblocked

Tails executed ## Plan items 1-4 (evidence in ## Implementation). P1: `/usr/libexec/csd-backlight-helper` is absent from Rocky's `cinnamon-settings-daemon` RPM (present in Fedora's); on Rocky `GetPercentage` fails ENOENT and `StepUp` is a no-op. E1: no backlight on either VM (empty `/sys/class/backlight`, virtio GPU), so end-to-end brightness verification is impossible in this environment by design. Not a D-Bus authorization issue; TASK-0035 not implicated. DoD box 4 (fix path) applies. Tails executed ## Plan items 5-7: spec-only fix (canonical repo commit `ec49438b38`: Release 2→3.el10, `libgudev-devel`/`upower-devel` build deps, `-Duse_gudev=disabled` removed, no source change), rebuild (unsigned, local-only `rpms-local/`), install on `Rocky_Linux_10_Cinnamon`, E1-bounded verification passed (helper runs; failure signature byte-identical to the Fedora comparison; end-to-end brightness impossible in this environment by design). DoD boxes 5-6 await `Big`. Review chain: Shadow done (no blockers on the change; three should-fix closeout findings in ## Review — DoD box 4 reworded per finding 1; findings 2-3 are `Knuckles`/`## Release` prerequisites; one note for Omega). Omega done: four findings — 1 high + 2 medium are the standing TASK-0033 rotation operator step-stop (live PAT world-readable in `~/AI/secrets/` and in a remote URL via global `insteadOf`; `~/AI/secrets/` 755/644 vs §4 700/600; dead second PAT still wired), already blocked there for operator rotation; 1 low (unsigned -3 RPM left in VM `/tmp`, `rpms-local/` untracked = operator-confusion risk). Change itself verified clean; Omega corrects Shadow's PAT note on mechanism (global `insteadOf` rewrite, not `.git/config`). Big done: all applicable layers independently re-run and PASS (compile/unit/integration; Sparky not run, justified and stated), final verdict in ## Test Results — P1 fixed at the RPM layer and verified live on the target VM, E1 confirmed live on both VMs, no FAIL, remainder is operator hardware. Charmy done: pass, no findings (verified at the upstream source at the exact ref used; spec-only change imports no new code, new `libgudev`/`upower` deps compatible). Review chain clean; no Tails fix round. Next: Vector.

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

- [x] Target machine identified and its brightness hardware state recorded with evidence (backlight sysfs, `brightnessctl` output, `lspci` display info).
- [x] Root cause established in `## Implementation` with command + output evidence: why Cinnamon Settings and the keyboard shortcuts do not change brightness.
- [x] Classification recorded: environment limitation (no backlight hardware, e.g. a VM) versus Cinnamon port bug (missing package, daemon plugin, unbound shortcut).
- [x] If port bug: fix in the Cinnamon package, rebuilt, installed on the target machine, and brightness verified to the maximum extent possible in this environment per the E1-bounded criteria in ## Implementation, with before/after evidence; the E1-blocked remainder (end-to-end on real hardware) documented in ## Test Results. (Reworded 2026-10-12 per Shadow finding 1: the original wording was unsatisfiable under the BOTH verdict.)
- [x] If environment limitation: documented in `## Test Results` with what would make it testable (hardware with a real display).
- [x] `## Test Results` updated with the final verdict.

---

## Next Actions

- [x] `Amy`: plan the diagnosis on `Rocky_Linux_10_Cinnamon` (machine identified; see ## Status): probe the brightness stack (backlight sysfs, `brightnessctl`, settings-daemon plugin state, keybindings via gsettings), classify per the DoD, and define the fix path. Use TASK-0033's package inventory for versions. `Fedora_45_Cinnamon` is the comparison machine. (done 2026-10-12, see ## Plan)
- [x] `Tails`: execute ## Plan items 1-4 (probe, comparison diff, root cause, classification); items 5-7 are conditional on the item 4 verdict. (done 2026-10-12, verdict P1+E1, see ## Implementation)
- [x] `Tails`: execute ## Plan items 5-7 (fix phase, unblocked by the P1 verdict); VM verification bounded by E1 per the plan. (done 2026-10-12, see ## Implementation)
- [x] `Shadow`: review the change (spec fix + rebuild + E1-bounded verification, evidence in ## Implementation) against ## Plan and the DoD; first of the fixed chain Shadow → Omega → Big → Charmy, write to ## Review. (done 2026-10-12: no blockers, three should-fix closeout findings, see ## Review)
- [x] `Omega`: review the change for attack surface; second of the fixed chain, write to ## Security. (done 2026-10-12: four findings, see ## Security; high/medium map to the standing TASK-0033 rotation step-stop, low is RPM artifact hygiene)
- [x] `Big`: run the applicable test layers and write the final verdict in ## Test Results per DoD boxes 5-6, including the Shadow finding 1 split (satisfied clauses vs E1/hardware-deferred); third of the fixed chain. (done 2026-10-12: all layers PASS, no FAIL, see ## Test Results)
- [x] `Charmy`: license compliance review; fourth of the fixed chain, write to ## License (Charmy). (done 2026-10-12: pass, no findings, see ## License (Charmy))
- [x] `Vector`: update README/docs to match the implementation (spec fix + -3 RPM); write what changed to ## Docs. (done 2026-10-12: README known-issue block added, left uncommitted to ride the canonical-repo push; see ## Docs)
- [x] `Knuckles`: release step — commit + push what is pushable per house rules, execute the `## Release` prerequisites (Shadow findings 2-3, Vector's README change), record the exact operator step where the standing TASK-0033 rotation step-stop blocks a push, close the GitHub Issue for this task if one exists. Write the outcome to ## Release. (done 2026-10-13, see ## Release)

---

## Plan

*Owner: `Amy`.*

### Strategic framing

**Why this task exists.** The operator reports that on the team's Cinnamon + Rocky Linux 10 environment, brightness cannot be changed through Cinnamon Settings or the keyboard shortcuts (`## Status`). The port stands or falls on "Cinnamon works on Rocky 10", so a brightness path that does nothing is either a port defect or an environment limit that cannot be tested here, and the DoD demands the distinction with evidence. Cross-task note: TASK-0035 (planning/docs/TASK-0035-cinnamon-power-pane-dbus-unauthorized.md) opened 2026-10-10 for a D-Bus `Unauthorized (36)` traceback in the Power pane of `cinnamon-settings` on this same VM and same session, diagnosis not started. The brightness control in Control Center is a pane that talks to the settings daemon over D-Bus, so the two tasks share the daemon-layer question. Item 2 records the D-Bus state that task will need.

**What it unblocks / what blocks it.** Unblocks a defensible status for the Cinnamon port. Brightness is currently unverified, and if the probe finds a port bug, the fix feeds the same RPM pipeline that TASK-0026 and TASK-0024 use. Nothing in this repo blocks it. External dependencies: (1) signing. The host build toolchain works (TASK-0026 built the unsigned `cinnamon-6.7.4-4` RPM on the host, 2026-10-10), but no signing private key is on the host (public key is in the RPM keyring. Operator rotation is pending per TASK-0033 `## Security`). A fix-path RPM is therefore unsigned and local-install-for-verification only. (2) VM state. TASK-0035 may land a D-Bus or policy change on this VM before or after this task. The probes are read-only and idempotent, and evidence is timestamped, so state change forces a re-run, not a redo. (3) Hardware. Neither VM has a real backlight (QEMU virtual GPU, assumption A4). "The display got brighter" verification is impossible in this environment by design. The DoD environment-limitation branch is the expected outcome, and the port-bug branch stays open until the probes close it.

**MVP.** Items 1 through 4: the full brightness-stack probe on both VMs plus root cause and classification per the DoD. That satisfies DoD lines 1 through 3 (hardware state, root cause, classification) and answers the operator's question. Deferred: the fix path (items 5 through 7, conditional on a port bug), Sparky-based brightness UI automation (on a backlight-less VM a UI test can only assert slider state and errors, not display effect. Revisit when hardware exists. `Big` decides the test layer if item 7 runs), and end-to-end verification on real hardware (out of scope, operator hardware).

**What this makes harder later.** (1) An environment-limitation verdict closes end-to-end brightness verification on this VM infrastructure. Future Cinnamon brightness regressions will be undetectable here. (2) The fix path rebuilds a component RPM on the host, unsigned, and lands it in untracked `rpms-local/`. The tracked `rpms/` set (65 files, gpgcheck=1) does not move until the operator signs, so the fix is live on the VM but not in the repo until then. (3) If the culprit is `cinnamon-rocky-defaults` (the only team-authored desktop package, a keybinding-override candidate), every future defaults change must re-verify brightness. (4) This task and TASK-0035 share the D-Bus authorization question. If 0035 changes policy or configuration on the VM, the evidence baseline here shifts and the affected probes re-run.

### Recorded facts (verified 2026-10-12)

- Both VMs running: `sudo -n virsh -c qemu:///system list` returned `Fedora_45_Cinnamon` Id 1 and `Rocky_Linux_10_Cinnamon` Id 2.
- Snapshots (TASK-0033, last checked unchanged): Rocky `2026-10-04T11:36` (shutoff), Fedora `2026-10-04T11:37` (shutoff). Restoring either reverts work after 2026-10-04 (on Rocky, the TASK-0026 unsigned `cinnamon-6.7.4-4` install. On Fedora, the sshd enablement). This plan never restores.
- Package baseline (TASK-0033 inventories, el10 vs fc45 tags). The probes re-verify `rpm -qa` at run time and cite whatever they find:
  - Rocky, 7 packages: `cinnamon-6.7.4-3.el10`, `cinnamon-control-center-6.7.2-1.el10`, `cinnamon-desktop-6.7.2-2.el10`, `cinnamon-menus-6.7.0-1.el10`, `cinnamon-rocky-defaults-1.0-2.el10`, `cinnamon-session-6.7.3-1.el10`, `cinnamon-settings-daemon-6.7.2-2.el10`.
  - Fedora, 13 packages: `cinnamon-6.7.5^unstable-3.fc45`, `cinnamon-session-6.7.4^unstable-1.fc45`, `cinnamon-desktop-6.7.3^unstable-1.fc45`, `cinnamon-control-center-6.7.3^unstable-1.fc45`, `cinnamon-settings-daemon-6.7.3^unstable-1.fc45`, `cinnamon-menus-6.7.0^unstable-2.fc45`, `cinnamon-calendar-server-6.7.5^unstable-3.fc45`, `cinnamon-themes-2.4.0-1.fc45`, `cinnamon-translations-6.7.0^unstable-2.fc45`, `cinnamon-control-center-filesystem-6.7.3^unstable-1.fc45`, `fedora-release-cinnamon-45-0.10`, `fedora-release-identity-cinnamon-45-0.10`, `slick-greeter-cinnamon-2.2.6-4.fc45`.
  - Neither inventory contains a `cinnamon-keybindings` package. Where the keybinding schemas come from is itself an open question that item 2 answers via `rpm -qf` on the schema files.
- Session types (TASK-0033): Rocky is Wayland (`gdm-password`, X apps via Xwayland). Fedora is X11 (`lightdm`, Xorg). A software brightness path based on XRandR gamma (if CSD has one) applies only on X11. The two VMs therefore differ in two variables at once (packaging and session type), and the diff table must attribute findings per variable.
- Host build toolchain: `rpmbuild`, `meson`, `ninja` plus the team devel RPMs from `rpms/`, installed per TASK-0026 (2026-10-10). Re-verify with `command -v` before any build (A6).
- Guest login: `howard`, password from `~/AI/secrets/pass.txt` via `sshpass -f`, never written to any file, commit, log, or doc. Every virsh command passes `-c qemu:///system`. No blind-GUI key injection in this plan (TASK-0033 run 2 reliability and incident precedent).

### Assumptions (plan in pencil)

- A1: the Rocky VM still carries the TASK-0026 unsigned `cinnamon-6.7.4-4.el10` install (Big's 2026-10-10 verdict says the installed file on the VM matches the -4 payload. Not re-verified here). The probe's `rpm -qa` is the source of truth.
- A2: the CSD D-Bus bus name and the xrandr plugin object path are not recorded in this plan. Item 2 discovers them with `busctl --user` and records the real names.
- A3: the gsettings schema that holds the brightness shortcuts is not recorded in this plan. Item 2 discovers it via `gsettings list-schemas` plus recursive dumps and attributes ownership via `rpm -qf`.
- A4: a QEMU VM with a virtual GPU exposes no backlight device. Near-certain, and the probe proves it (DoD line 1).
- A5: the Fedora VM is not a working reference. It is also a backlight-less VM. Its role is packaging, plugin, and keybinding comparison, and it is the only place in this environment where an X11 software-brightness path could be exercised.
- A6: the host build toolchain is intact as of TASK-0026. The fix phase re-verifies before building.

### Work breakdown

All guest items are `Tails`. One item, one turn, one machine. Each item's evidence block lands in `## Implementation` with command + output per line (AGENTS.md section 2).

| # | Item | Owner agent | Acceptance criterion | Parallel with |
|---|---|---|---|---|
| 1 | Rocky hardware-layer probe. Backlight sysfs (`ls /sys/class/backlight/`, per-device `brightness`/`max_brightness`/`backlight_type`). `brightnessctl -l` and `info` (recorded absence if the binary is missing). `lspci -k` display lines plus `/sys/class/drm/` driver links. `rpm -qa \| grep -iE 'cinnamon|backlight'` state fingerprint. `uptime` and session state | Tails | The question "backlight present?" answered by two independent sources (sysfs listing and either `brightnessctl` or `rpm -qf` on the sysfs node). Every command + output recorded | independent |
| 2 | Rocky daemon-layer probe. CSD process and service state (`pgrep -a`, `systemctl --user status`). Plugin file list from `rpm -ql cinnamon-settings-daemon`, confirmed on disk. D-Bus: `busctl --user list` for the CSD name, introspect to find the xrandr object, read the brightness-related properties. gsettings: `list-schemas` filtered to cinnamon, recursive dumps of the keybinding, settings-daemon, and control-center display schemas, `rpm -qf` on each relevant schema file. One scripted D-Bus brightness call (the programmatic equivalent of the Settings slider) with property read-back, and a user-journal capture around it to record any authorization error. Shortcut trigger attempted by the best available method (`xdotool key <combo>` if installed, otherwise record the absence) with result plus journal | Tails | Plugin presence or absence. D-Bus object plus property values before and after the scripted call. Brightness up/down shortcuts bound or unbound with the exact combos. Schema ownership (Rocky package name). Scripted-call outcome including the exact error if any. The one guest write (the scripted D-Bus call) flagged and recorded | independent of 1 |
| 3 | The same probe set as items 1 and 2 on `Fedora_45_Cinnamon`, same commands, same recording format | Tails | Parallel evidence blocks plus a per-probe Rocky-vs-Fedora diff table. Each diff row attributes the difference to packaging or session type where possible | independent of 1 and 2 (order free. Runs after 2 so the format is settled) |
| 4 | Root cause and classification in `## Implementation` per the decision tree below. If port bug, name the exact missing artifact (plugin file, schema file, keybinding, D-Bus permission) and the owning package | Tails | A root-cause paragraph where every claim maps to a command + output from items 1 through 3. A classification statement (environment limitation, port bug, or both) citing the evidence lines. DoD lines 1 through 3 tickable | waits on 1, 2, 3 |
| 5 | Fix (only if 4 finds a port bug). Source and/or spec fix in the canonical repo. Component checkout `~/Linux/projects/cinnamon-for-rocky10/<component>` and/or `spec/<pkg>.spec` (team-authored packages such as `cinnamon-rocky-defaults` have no separate checkout. The spec in the canonical repo is the fix site) | Tails | The component diff addresses the named artifact. `## Implementation` records the files and the reason | waits on 4 |
| 6 | Fix build. Re-verify the toolchain (`command -v rpmbuild meson ninja`). Stage Source0 from the working tree (TASK-0026 method). Build. Unsigned. Place in untracked `rpms-local/` | Tails | `rpmbuild` exit 0. Checksum of the fixed payload recorded. RPM md5 and sha256 recorded. `Signature: (none)` recorded as expected | waits on 5 |
| 7 | Fix verification. Record the prior NEVRA of the affected packages on the VM. `rpm -Uvh` the new RPM. Re-run item 2's daemon probe. Confirm the scripted D-Bus call now changes the property and the journal is clean. Before/after values recorded | Tails | Before/after property values. Prior NEVRA recorded before the install. No new journal errors | waits on 6 |

### Classification decision tree (for item 4)

- E1, environment limitation. No backlight device (item 1), no working software-brightness path for the session in question, and the Rocky stack is complete against Fedora (plugin present, daemon running, D-Bus object present, shortcut bound). Verdict: environment limitation, documented in `## Test Results` with what would make it testable (hardware with a real display and backlight).
- P1, port bug. Any of these present on Fedora but absent or broken on Rocky: (a) the xrandr plugin file missing from the `cinnamon-settings-daemon` file list or from disk. (b) the xrandr D-Bus object absent. (c) the brightness shortcut unbound when it is bound on Fedora, with `cinnamon-rocky-defaults` owning the override. (d) a gsettings schema file present on Fedora but absent on Rocky. (e) the scripted D-Bus call fails on Rocky with an authorization or service error and succeeds, or fails differently, on Fedora. Verdict: port bug, named artifact, fix path (items 5 through 7).
- Both. E1 plus one or more P1 findings. The DoD fix branch applies to the P1 findings, and the environment limitation is documented separately. The classification records both.
- Ambiguity rule. A probe that cannot run (missing tool, VM drift) is recorded as a gap, not a finding. Hardware presence requires two agreeing independent sources before E1 is claimed (risk row 1).

### Dependencies and sequence

- Items 1, 2, 3 are genuinely independent. No ordering constraint among them.
- 4 depends on 1, 2, 3. 5 depends on 4. 6 depends on 5. 7 depends on 6. The only items that only look ordered are 1 and 3 against 2. There is no dependency among the probes, and the dispatch order after 2 is free.
- Cross-task, no hard order: TASK-0035 (same VM, same D-Bus layer). If 0035 lands a fix on the VM between this task's items, the affected items re-run and the evidence cites both states. TASK-0026's remaining steps (checkpoint, docs, archive) do not touch the VM.
- The single inference slot runs one agent at a time anyway. The order above is the critical-path order, not a concurrency plan.

### Critical path

2 → 4 → 5 → 6 → 7 (longest chain, the fix branch). Items 1 and 3 are off-critical. Running them before or after does not extend the chain.

### Estimates

Three-point, hours, `T = (O + 4M + P) / 6`.

| Item | O | M | P | T |
|---|---|---|---|---|
| 1 | 0.5 | 1 | 2 | 1.1 |
| 2 | 1 | 2 | 3 | 2.0 |
| 3 | 0.5 | 1 | 2 | 1.1 |
| 4 | 1 | 2 | 4 | 2.2 |
| 5 | 2 | 4 | 8 | 4.3 |
| 6 | 2 | 4 | 10 | 4.7 |
| 7 | 1 | 2 | 4 | 2.2 |

Diagnosis subtotal (items 1 through 4) is about 6.4h, plus a 25% buffer for unknown schema and D-Bus name discovery, about 8h. Fix subtotal (items 5 through 7) is about 11.2h, plus a 5h buffer sized to the highest uncertainty in the plan (the bug class is unknown until item 4), about 16h.

### Risks

| Risk | Likelihood | Impact | Mitigation | Contingency |
|---|---|---|---|---|
| Probe misread. Absence of the `brightnessctl` binary gets recorded as "no backlight" | low | medium | Two independent sources for hardware presence (sysfs plus `brightnessctl` or `rpm -qf`), made a rule in the decision tree | Add a third source (`backlight_type`, driver `readlink`) |
| Wayland-vs-X11 confound. The two VMs differ in packaging and session type at once, so a diff row may be misattributed | certain | medium | Each diff row names the variable it attributes to. The X11 software-fallback question is only answerable on the Fedora VM, and the plan says so | Record both candidate causes and mark the row unattributed |
| Plan assumptions A2 and A3 (D-Bus names, schema names) are wrong | high | low | Discovery by construction. Item 2 runs `busctl --user` and `gsettings list-schemas` and records the real names. The plan asserts no names | None. Discovery is the design |
| TASK-0035 fixes or operator activity change the VM state between items | medium | medium | Every evidence block records `uptime`, a timestamp, and the `rpm -qa` fingerprint. Re-run on drift | Re-run the affected items and cite both states |
| Fix-path RPM is unsigned and cannot enter the tracked `rpms/` set (gpgcheck=1, no private key) | certain | medium | Follow the TASK-0026 precedent. Unsigned RPM to untracked `rpms-local/`, local install for verification, no push into `rpms/`. Signing deferred to operator key availability. `## Release` records the unsigned state and why | If the operator rotates the key, sign and rebuild per the TASK-0024 procedure |
| Password-echo recurrence (guest terminal scrollback) | low | medium | No blind-GUI key injection in this plan. All probes over SSH. The one near-GUI action (shortcut trigger) is SSH-scripted with fallback to binding evidence only | Stop, record, operator rotation per the TASK-0033 procedure |
| Operator restores a 2026-10-04 snapshot, silently reverting TASK-0026's VM work (and any fix from this task) | low | high (for other tasks) | This plan never restores. Rollback uses NEVRA reinstall. The snapshot trap is already recorded in TASK-0033 run 3 (finding 5) | Re-verify VM state for both tasks after any restore |

### Validation

- Environments: `Rocky_Linux_10_Cinnamon` (target), `Fedora_45_Cinnamon` (comparison), host (read-only virsh).
- Host checks: `sudo virsh -c qemu:///system list` before and after (both running). `snapshot-list` per VM unchanged (one each, same names and states).
- Guest checks per the DoD: backlight sysfs evidence. `brightnessctl` output or recorded absence. `lspci` display info. CSD process and plugin state. D-Bus object and property values. gsettings keybinding values on both VMs. Version table against the TASK-0033 baseline plus the TASK-0026 -4 state (A1).
- Evidence standard: every claim in `## Implementation` maps to a command + output. The classification statement cites its evidence lines. The DoD box ticks line by line.
- Human look: the operator reads the classification and the diff table (via `## Status`). If the fix path runs, the before/after D-Bus property values.

### Rollback

- Detection: the items are read-only except item 2's single scripted D-Bus call. The failure mode is an incomplete probe or VM-state drift, detected by the per-item acceptance checks plus the before/after `virsh list`.
- Exact revert: no guest configuration changes, so there is nothing to revert in the diagnosis phase. Evidence artifacts live only in this planning doc. The fix phase records the prior NEVRA before the install. Revert is `rpm -Uvh` of the prior RPMs from the tracked `rpms/` set (or `rpm -e` plus reinstall). The `/tmp` build directory is deletable. `rpms-local/` is untracked and deletable.
- Point of no return: none in the diagnosis phase. In the fix phase, (a) installing the new RPM on the guest, mitigated by the prior-NEVRA record plus the tracked `rpms/` copy. (b) committing a rebuilt RPM into the tracked `rpms/` set, which this plan does not do (unsigned, signing deferred). That point of no return stays outside this task until the operator signs.

---

## Implementation

*Owner: `Tails`.*

*Executed 2026-10-12, plan items 1-4 (diagnosis) and items 5-7 (fix phase, unblocked by the BOTH verdict: P1 fixed in the spec, E1-bounded verification).*

All guest commands ran as `howard` via `sshpass -f ~/AI/secrets/pass.txt ssh howard@<IP>` (Rocky `192.168.122.4`, Fedora `192.168.122.176`). The password file is never read by any tool and its content appears in no output. `XDG_RUNTIME_DIR=/run/user/1000` was exported for user-bus commands (`busctl`, `systemctl --user`, `gsettings`). Format: `$`-prefixed line is the command, following lines are verbatim output.

### Item 1 — Rocky hardware-layer probe (Rocky_Linux_10_Cinnamon)

**P1.1 — Target state: uptime, sessions**
```
$ date -u +%Y-%m-%dT%H:%M:%SZ
2026-10-12T06:45:15Z
$ uptime
 15:45:15 up 7 days, 34 min,  2 users,  load average: 0.00, 0.00, 0.00
$ loginctl list-sessions
SESSION  UID USER   SEAT  LEADER CLASS   TTY  IDLE SINCE
    145 1000 howard -     34528  user    -    no   -
      2 1000 howard seat0 2848   user    tty2 yes  6 days ago
      3 1000 howard -     2859   manager -    no   -
3 sessions listed.
```
Session 2 (seat0/tty2, 6 days) is the Cinnamon session; the `gdm-wayland-session` bus connection seen in item 2 confirms the Wayland session type.

**P1.2 — Backlight sysfs**
```
$ ls -la /sys/class/backlight/
total 0
drwxr-xr-x.  2 root root 0 Oct 12 15:45 .
drwxr-xr-x. 74 root root 4096 Oct  5 15:10 ..
```
Empty directory: no backlight device, so no per-device `brightness`/`max_brightness`/`backlight_type` to read.

**P1.3 — brightnessctl (recorded absence of binary)**
```
$ command -v brightnessctl || echo 'brightnessctl: binary not installed'
brightnessctl: binary not installed
$ brightnessctl -l
bash: line 18: brightnessctl: command not found
exit=127
```
Gap per the ambiguity rule: no `brightnessctl` binary on the VM, so the udev-side corroboration of hardware presence is unavailable; the second independent source is the PCI display controller (P1.4/P1.5).

**P1.4 — PCI display controller**
```
$ lspci -k | grep -iE -B1 -A2 'vga|3d|display'
	Subsystem: Red Hat, Inc. QEMU Virtual Machine
00:01.0 VGA compatible controller: Red Hat, Inc. Virtio 1.0 GPU (rev 01)
	Subsystem: Red Hat, Inc. QEMU
	Kernel driver in use: virtio-pci
```

**P1.5 — DRM driver links**
```
$ ls -l /sys/class/drm/
total 0
lrwxrwxrwx. 1 root root   0 Oct 12 15:45 card0 -> ../../devices/pci0000:00/0000:00:01.0/drm/card0
lrwxrwxrwx. 1 root root   0 Oct  8 01:18 card0-Virtual-1 -> ../../devices/pci0000:00/0000:00:01.0/drm/card0/card0-Virtual-1
lrwxrwxrwx. 1 root root   0 Oct 12 15:45 renderD128 -> ../../devices/pci0000:00/0000:00:01.0/drm/renderD128
-r--r--r--. 1 root root 4096 Oct  5 15:10 version
$ readlink -f /sys/class/drm/card0
/sys/devices/pci0000:00/0000:00:01.0/drm/card0
```
Single virtual output (`card0-Virtual-1`) on the QEMU Virtio GPU.

**P1.6 — Package state fingerprint**
```
$ rpm -qa | grep -iE 'cinnamon|backlight' | sort
cinnamon-6.7.4-4.el10.x86_64
cinnamon-control-center-6.7.2-1.el10.x86_64
cinnamon-desktop-6.7.2-2.el10.x86_64
cinnamon-menus-6.7.0-1.el10.x86_64
cinnamon-rocky-defaults-1.0-2.el10.noarch
cinnamon-session-6.7.3-1.el10.x86_64
cinnamon-settings-daemon-6.7.2-2.el10.x86_64
```
7 packages, matching the TASK-0033 el10 inventory except `cinnamon-6.7.4-4.el10`, which is the TASK-0026 unsigned -4 install, re-verified at run time (A1 confirmed). No package name matches `backlight`.

**Item 1 verdict — backlight present? NO.** Two independent sources agree: (1) `/sys/class/backlight` is empty (P1.2); (2) the only display controller is a QEMU Virtio 1.0 GPU driven by `virtio-pci` (P1.4/P1.5), a virtual GPU with no backlight hardware. `brightnessctl` absence is a recorded gap, not a finding (P1.3).

### Item 2 — Rocky daemon-layer probe (Rocky_Linux_10_Cinnamon)

**P2.1 — CSD process and service state**
```
$ pgrep -af 'cinnamon-settings-daemon'
no cinnamon-settings-daemon process
$ systemctl --user status cinnamon-settings-daemon
Unit cinnamon-settings-daemon.service could not be found.
$ pgrep -af 'csd-'
3102 /usr/bin/csd-settings-remap
3103 /usr/bin/csd-background
3108 /usr/bin/csd-screensaver-proxy
3112 /usr/bin/csd-a11y-settings
3114 /usr/bin/csd-xsettings
3121 /usr/bin/csd-housekeeping
3123 /usr/bin/csd-clipboard
3124 /usr/bin/csd-power
3125 /usr/bin/csd-media-keys
3127 /usr/bin/csd-keyboard
```
CSD is not a systemd unit on this VM. The plugins run as per-user autostart processes (`/usr/bin/csd-*`). 10 of the 12 shipped plugin binaries run. Not running / not shipped: `csd-color`, `csd-wacom`, `csd-printer`, `csd-print-notifications`, `csd-datetime-mechanism`, `csd-backlight-helper` (P2.3, P2.8).

**P2.2 — User autostart units**
```
$ systemctl --user list-unit-files | grep -iE 'cinnamon'
app-cinnamon\x2dsettings\x2ddaemon\x2da11y\x2dsettings@autostart.service     generated -
app-cinnamon\x2dsettings\x2ddaemon\x2dbackground@autostart.service           generated -
app-cinnamon\x2dsettings\x2ddaemon\x2dclipboard@autostart.service            generated -
app-cinnamon\x2dsettings\x2ddaemon\x2dhousekeeping@autostart.service         generated -
app-cinnamon\x2dsettings\x2ddaemon\x2dkeyboard@autostart.service             generated -
app-cinnamon\x2dsettings\x2ddaemon\x2dmedia\x2dkeys@autostart.service        generated -
app-cinnamon\x2dsettings\x2ddaemon\x2dpower@autostart.service                generated -
app-cinnamon\x2dsettings\x2ddaemon\x2dscreensaver\x2dproxy@autostart.service generated -
app-cinnamon\x2dsettings\x2ddaemon\x2dsettings\x2dremap@autostart.service    generated -
app-cinnamon\x2dsettings\x2ddaemon\x2dxsettings@autostart.service            generated -
cinnamon-session.target                                                      static    -
```

**P2.3 — RPM file list (`cinnamon-settings-daemon-6.7.2-2.el10`) and on-disk confirmation**
```
$ rpm -ql cinnamon-settings-daemon | grep -E '/bin/|libexec|autostart'
/etc/xdg/autostart/cinnamon-settings-daemon-a11y-settings.desktop
/etc/xdg/autostart/cinnamon-settings-daemon-background.desktop
/etc/xdg/autostart/cinnamon-settings-daemon-clipboard.desktop
/etc/xdg/autostart/cinnamon-settings-daemon-housekeeping.desktop
/etc/xdg/autostart/cinnamon-settings-daemon-keyboard.desktop
/etc/xdg/autostart/cinnamon-settings-daemon-media-keys.desktop
/etc/xdg/autostart/cinnamon-settings-daemon-power.desktop
/etc/xdg/autostart/cinnamon-settings-daemon-screensaver-proxy.desktop
/etc/xdg/autostart/cinnamon-settings-daemon-settings-remap.desktop
/etc/xdg/autostart/cinnamon-settings-daemon-xsettings.desktop
/usr/bin/csd-a11y-settings
/usr/bin/csd-automount
/usr/bin/csd-background
/usr/bin/csd-clipboard
/usr/bin/csd-housekeeping
/usr/bin/csd-input-helper
/usr/bin/csd-keyboard
/usr/bin/csd-media-keys
/usr/bin/csd-power
/usr/bin/csd-screensaver-proxy
/usr/bin/csd-settings-remap
/usr/bin/csd-xsettings
/usr/lib64/cinnamon-settings-daemon/  (same 12 binaries)
/usr/libexec/                        (same 12 binaries)
```
No `csd-backlight-helper`, no `csd-xrandr`, no `csd-color`, no `csd-wacom*`, no `csd-print*`, no `csd-datetime-mechanism` in the file list. All listed files confirmed on disk (`ls` on the plugin dirs matched the RPM list). Shipped schemas confirmed on disk: `org.cinnamon.settings-daemon.{enums,peripherals,peripherals.wacom,plugins.color,plugins,plugins.housekeeping,plugins.media-keys,plugins.power,plugins.xrandr,plugins.xsettings}` under `/usr/share/glib-2.0/schemas/`.

**P2.4 — Session bus names (discovery, plan assumption A2)**
```
$ busctl --user list | grep -iE 'cinnamon'   (brightness-relevant excerpt)
org.cinnamon.SettingsDaemon.KeybindingHandler  3125 csd-media-keys  howard :1.49  session-2.scope
org.cinnamon.SettingsDaemon.Power              3124 csd-power       howard :1.45  session-2.scope
org.cinnamon.SettingsDaemon.Power.Keyboard     3124 csd-power       howard :1.45  session-2.scope
org.cinnamon.SettingsDaemon.Power.Screen       3124 csd-power       howard :1.45  session-2.scope
```
The brightness surface is `org.cinnamon.SettingsDaemon.Power.Screen`, owned by the running `csd-power` (PID 3124). It is the only brightness-named interface on the user bus. No separate xrandr bus name exists (plan A2 resolved: there is no `csd-xrandr` plugin binary in this RPM, P2.3). No `org.cinnamon.SettingsDaemon.Color` on Rocky (csd-color not shipped, P2.1/P2.3).

**P2.5 — D-Bus introspection and property read (before any call)**
```
$ busctl --user introspect org.cinnamon.SettingsDaemon.Power /org/cinnamon/SettingsDaemon/Power
NAME                                       TYPE      SIGNATURE RESULT/VALUE FLAGS
org.cinnamon.SettingsDaemon.Power          interface -         -            -
.GetDevices                                method    -         a(sssusduut) -
.GetPrimaryDevice                          method    -         (sssusduut)  -
.Icon                                      property  s         ""           emits-change
.Percentage                                property  u         0            emits-change
org.cinnamon.SettingsDaemon.Power.Keyboard interface -         -            -
.GetPercentage                              method    u         -            -
.GetStep                                   method    u         -            -
.SetPercentage                              method    u         u          -
.StepDown                                  method    -         u            -
.StepUp                                    method    -         u            -
.Toggle                                   method    -         u            -
.Changed                                  signal    -         -            -
org.cinnamon.SettingsDaemon.Power.Screen   interface -         -            -
.GetPercentage                              method    -         u            -
.SetPercentage                              method    u         u          -
.StepDown                                  method    -         uii        -
.StepUp                                    method    -         uii        -
.AmbientLightSupported                     property  b         false        emits-change
.Changed                                  signal    -         -            -
```
(Object path `/org/cinnamon/SettingsDaemon/Power`; standard `org.freedesktop.DBus.*` interfaces elided.) For methods, `RESULT/VALUE` is the output signature: `Screen.GetPercentage` takes no input and returns `u`; `Screen.StepUp` takes no input and returns `uii`; `Screen.SetPercentage` takes `u` and returns `u`. Brightness-related values before the call: `Power.Percentage = 0`, `Power.Screen.AmbientLightSupported = false`.

**P2.6 — gsettings keybinding and schema values**
```
$ gsettings list-recursively org.cinnamon.desktop.keybindings.media-keys   (brightness-relevant keys)
org.cinnamon.desktop.keybindings.media-keys screen-brightness-down ['XF86MonBrightnessDown']
org.cinnamon.desktop.keybindings.media-keys screen-brightness-up ['XF86MonBrightnessUp']
org.cinnamon.desktop.keybindings.media-keys kbd-brightness-down ['XF86KbdBrightnessDown']
org.cinnamon.desktop.keybindings.media-keys kbd-brightness-toggle ['XF86KbdLightOnOff']
org.cinnamon.desktop.keybindings.media-keys kbd-brightness-up ['XF86KbdBrightnessUp']
$ gsettings list-recursively org.cinnamon.settings-daemon.plugins.power   (brightness-relevant keys)
org.cinnamon.settings-daemon.plugins.power idle-brightness 30
org.cinnamon.settings-daemon.plugins.power minimum-display-brightness uint32 2
org.cinnamon.settings-daemon.plugins.power backlight-helper-force false
org.cinnamon.settings-daemon.plugins.power backlight-helper-preference-order ['firmware', 'platform', 'raw']
```
Screen brightness shortcuts are BOUND: up = `['XF86MonBrightnessUp']`, down = `['XF86MonBrightnessDown']`. Full recursive dumps of `org.cinnamon.settings-daemon.plugins.{power,media-keys,xrandr,plugins}`, `org.cinnamon.control-center.display` (single key `show-fractional-scaling-controls false`) and `org.cinnamon.desktop.keybindings.media-keys` are in the probe output. The CSD-internal media-keys schema (`org.cinnamon.settings-daemon.plugins.media-keys`) contains no brightness keys (same on Fedora, P3.7).

**P2.7 — Schema file ownership (`rpm -qf`)**
```
$ rpm -qf /usr/share/glib-2.0/schemas/org.cinnamon.settings-daemon.plugins.power.gschema.xml
cinnamon-settings-daemon-6.7.2-2.el10.x86_64
$ rpm -qf /usr/share/glib-2.0/schemas/org.cinnamon.settings-daemon.plugins.media-keys.gschema.xml
cinnamon-settings-daemon-6.7.2-2.el10.x86_64
$ rpm -qf /usr/share/glib-2.0/schemas/org.cinnamon.settings-daemon.plugins.xrandr.gschema.xml
cinnamon-settings-daemon-6.7.2-2.el10.x86_64
$ rpm -qf /usr/share/glib-2.0/schemas/org.cinnamon.control-center.display.gschema.xml
cinnamon-control-center-6.7.2-1.el10.x86_64
$ rpm -qf /usr/share/glib-2.0/schemas/org.cinnamon.desktop.keybindings.media-keys.gschema.xml
cinnamon-desktop-6.7.2-2.el10.x86_64
```
The keybinding schema lives in `cinnamon-desktop`, not `cinnamon-settings-daemon`. No `cinnamon-keybindings` package exists on either VM; that answers the plan's open question (the schemas come from `cinnamon-desktop`).

**P2.8 — Missing helper: file search**
```
$ ls -l /usr/libexec/csd-backlight-helper
ls: cannot access '/usr/libexec/csd-backlight-helper': No such file or directory
$ find /usr /opt -name 'csd-backlight-helper'
(no output)
$ rpm -qf /usr/libexec/csd-backlight-helper
error: file /usr/libexec/csd-backlight-helper: No such file or directory
```

**P2.9 — Scripted D-Bus brightness call (the one guest write of the diagnosis phase)**
```
$ busctl --user call org.cinnamon.SettingsDaemon.Power /org/cinnamon/SettingsDaemon/Power org.cinnamon.SettingsDaemon.Power.Screen GetPercentage   # BEFORE
Call failed: Failed to execute child process “/usr/libexec/csd-backlight-helper” (No such file or directory)
$ busctl --user call org.cinnamon.SettingsDaemon.Power /org/cinnamon/SettingsDaemon/Power org.cinnamon.SettingsDaemon.Power.Screen StepUp
uii 0 0 0
$ busctl --user call org.cinnamon.SettingsDaemon.Power /org/cinnamon/SettingsDaemon/Power org.cinnamon.SettingsDaemon.Power.Screen GetPercentage   # AFTER
Call failed: Failed to execute child process “/usr/libexec/csd-backlight-helper” (No such file or directory)
```
`GetPercentage` (what the Settings slider reads) fails: CSD spawns `/usr/libexec/csd-backlight-helper` for brightness get/set and the file does not exist (P2.8). `StepUp` (the shortcut path) returns output `uii 0 0 0` (exit 0), interpreted as `(percentage, min, max) = (0, 0, 0)` (tuple semantics are inference): a no-op on a degenerate range. Two earlier `StepUp` attempts failed client-side on busctl argument syntax (`Failed to parse 'i' as unsigned 32-bit integer`, `Unknown signature type 1.`) and never reached the daemon; final syntax on systemd 257 is `busctl --user call NAME PATH IFACE Method [SIGNATURE [ARGUMENT...]]`. `SetPercentage` was not exercised; it shares the helper as CSD's only brightness backend (P2.8/P3.5) — its failure is inference, not verified.

**P2.10 — Journal capture and shortcut trigger**
```
$ journalctl --user -n 20 --no-pager
No journal files were found.
-- No entries --
$ command -v xdotool
xdotool: binary not installed
```
Gap: the user journal is unavailable from the SSH session context on this VM (it works on Fedora, P3.6); the D-Bus error string in P2.9 is the direct record. No authorization error occurred (the failure is spawn-ENOENT, not D-Bus authorization denial). `xdotool` is not installed: the shortcut trigger attempt is recorded as absent per the plan's fallback; the binding evidence in P2.6 stands in.

**Item 2 acceptance.** Plugin presence: `csd-power` runs (the brightness plugin is active); `csd-backlight-helper` absent from file list and disk. D-Bus object `/org/cinnamon/SettingsDaemon/Power` with `Power.Screen` present; before/after the scripted call `GetPercentage` fails identically (helper ENOENT) and `StepUp` returns `0 0 0`. Shortcuts bound: `['XF86MonBrightnessUp']` / `['XF86MonBrightnessDown']`. Schema ownership: `cinnamon-settings-daemon` (daemon schemas), `cinnamon-control-center` (display), `cinnamon-desktop` (keybindings). Scripted-call outcome including exact error: P2.9. The one guest write is flagged (P2.9) and changed nothing (the call failed or was a no-op).

### Item 3 — Comparison probe on Fedora_45_Cinnamon (192.168.122.176), same probe set

**P3.1 — Uptime and session**
```
$ date -u +%Y-%m-%dT%H:%M:%SZ
2026-10-12T07:19:04Z
$ uptime
 16:19:04 up 7 days,  1:08,  2 users,  load average: 0.42, 0.29, 0.24
$ loginctl list-sessions
SESSION  UID USER   SEAT  LEADER CLASS   TTY IDLE SINCE
      2 1000 howard seat0 1035   user    -   yes  1 week 0 days ago
     21 1000 howard -     22099  user    -   no   -
      3 1000 howard -     1089   manager -   no   -
3 sessions listed.
```
X11 session (lightdm/Xorg per TASK-0033): seat0 session leader 1035, no Wayland session process.

**P3.2 — Backlight sysfs / brightnessctl / PCI / DRM**
```
$ ls -la /sys/class/backlight/
total 0
drwxr-xr-x.  2 root root 0 Oct 12 16:19 .
drwxr-xr-x. 70 root root 4096 Oct  5 15:10 ..
$ command -v brightnessctl || echo 'brightnessctl: binary not installed'
brightnessctl: binary not installed
$ brightnessctl -l
bash: line 19: brightnessctl: command not found
exit=127
$ lspci -k | grep -iE -B1 -A2 'vga|3d|display'
00:01.0 VGA compatible controller: Red Hat, Inc. Virtio 1.0 GPU (rev 01)
	Subsystem: Red Hat, Inc. QEMU
	Kernel driver in use: virtio-pci
$ ls -l /sys/class/drm/
total 0
lrwxrwxrwx. 1 root root 0 Oct  5 15:10 card0 -> ../../devices/pci0000:00/0000:00:01.0/drm/card0
lrwxrwxrwx. 1 root root 0 Oct  5 15:10 card0-Virtual-1 -> ../../devices/pci0000:00/0000:00:01.0/drm/card0/card0-Virtual-1
lrwxrwxrwx. 1 root root 0 Oct  5 15:10 renderD128 -> ../../devices/pci0000:00/0000:00:01.0/drm/renderD128
-r--r--r--. 1 root root 4096 Oct  5 15:10 version
```
No backlight device on the comparison VM either; same Virtio GPU topology.

**P3.3 — Package fingerprint**
```
$ rpm -qa | grep -iE 'cinnamon|backlight' | sort
cinnamon-6.7.5^unstable-3.fc45.x86_64
cinnamon-calendar-server-6.7.5^unstable-3.fc45.x86_64
cinnamon-control-center-6.7.3^unstable-1.fc45.x86_64
cinnamon-control-center-filesystem-6.7.3^unstable-1.fc45.x86_64
cinnamon-desktop-6.7.3^unstable-1.fc45.x86_64
cinnamon-menus-6.7.0^unstable-2.fc45.x86_64
cinnamon-session-6.7.4^unstable-1.fc45.x86_64
cinnamon-settings-daemon-6.7.3^unstable-1.fc45.x86_64
cinnamon-themes-2.4.0-1.fc45.noarch
cinnamon-translations-6.7.0^unstable-2.fc45.noarch
fedora-release-cinnamon-45-0.10.noarch
fedora-release-identity-cinnamon-45-0.10.noarch
slick-greeter-cinnamon-2.2.6-4.fc45.noarch
```
13 packages, matching the TASK-0033 fc45 inventory.

**P3.4 — Running csd-* processes**
```
$ pgrep -af 'csd-'
1195 /usr/bin/csd-print-notifications
1196 /usr/bin/csd-a11y-settings
1197 /usr/bin/csd-color
1198 /usr/bin/csd-screensaver-proxy
1199 /usr/bin/csd-background
1202 /usr/bin/csd-housekeeping
1204 /usr/bin/csd-settings-remap
1209 /usr/bin/csd-clipboard
1217 /usr/bin/csd-keyboard
1219 /usr/bin/csd-wacom
1220 /usr/bin/csd-media-keys
1221 /usr/bin/csd-xsettings
1223 /usr/bin/csd-power
1330 /usr/libexec/csd-printer
```
`csd-power` (1223) owns `org.cinnamon.SettingsDaemon.Power{,.Keyboard,.Screen}` on the Fedora user bus, same names as Rocky; `csd-color` and `csd-wacom` own `org.cinnamon.SettingsDaemon.Color` / `org.cinnamon.SettingsDaemon.Wacom` (absent on Rocky).

**P3.5 — RPM file list (`cinnamon-settings-daemon-6.7.3^unstable-1.fc45`) and helper**
```
$ rpm -ql cinnamon-settings-daemon | grep -E '/bin/|libexec|autostart'   (binaries; autostart entries analogous to P2.2 plus color, print-notifications, wacom)
/usr/bin/csd-a11y-settings
/usr/bin/csd-automount
/usr/bin/csd-background
/usr/bin/csd-backlight-helper
/usr/bin/csd-clipboard
/usr/bin/csd-color
/usr/bin/csd-datetime-mechanism
/usr/bin/csd-housekeeping
/usr/bin/csd-input-helper
/usr/bin/csd-keyboard
/usr/bin/csd-media-keys
/usr/bin/csd-power
/usr/bin/csd-print-notifications
/usr/bin/csd-printer
/usr/bin/csd-screensaver-proxy
/usr/bin/csd-settings-remap
/usr/bin/csd-wacom
/usr/bin/csd-xsettings
/usr/libexec/csd-… (same set, plus /usr/libexec/csd-wacom-led-helper and /usr/libexec/csd-wacom-oled-helper)
$ ls -l /usr/libexec/csd-backlight-helper
-rwxr-xr-x. 1 root root 15704 Aug 15 09:00 /usr/libexec/csd-backlight-helper
$ rpm -qf /usr/libexec/csd-backlight-helper
cinnamon-settings-daemon-6.7.3^unstable-1.fc45.x86_64
```
The helper is present on the comparison VM and owned by the fc45 settings-daemon RPM. Neither RPM ships a `csd-xrandr` binary (see item 4, P1(a) resolution).

**P3.6 — D-Bus: introspection, scripted call, journal**
```
$ busctl --user introspect org.cinnamon.SettingsDaemon.Power /org/cinnamon/SettingsDaemon/Power
(identical to P2.5, same object path, same interfaces, AmbientLightSupported = false, Power.Percentage = 0)
$ busctl --user call org.cinnamon.SettingsDaemon.Power /org/cinnamon/SettingsDaemon/Power org.cinnamon.SettingsDaemon.Power.Screen GetPercentage   # BEFORE
Call failed: csd-backlight-helper failed: Could not get or set the value of the backlight: No backlight devices present
$ busctl --user call org.cinnamon.SettingsDaemon.Power /org/cinnamon/SettingsDaemon/Power org.cinnamon.SettingsDaemon.Power.Screen StepUp
uii 0 0 0
$ busctl --user call org.cinnamon.SettingsDaemon.Power /org/cinnamon/SettingsDaemon/Power org.cinnamon.SettingsDaemon.Power.Screen GetPercentage   # AFTER
Call failed: csd-backlight-helper failed: Could not get or set the value of the backlight: No backlight devices present
$ journalctl --user -n 20 --no-pager
(works: sshd-session and systemd tmpfiles entries; nothing from csd-power around the call)
```
The helper is spawned and reports that no backlight device exists. `StepUp` is the same no-op `(0, 0, 0)` as on Rocky.

**P3.7 — gsettings: same schemas, same values**
`gsettings list-recursively` on the same six schemas (`org.cinnamon.settings-daemon.plugins.{power,media-keys,xrandr,plugins}`, `org.cinnamon.control-center.display`, `org.cinnamon.desktop.keybindings.media-keys`): output identical to item 2 except one user-level value (`org.cinnamon.settings-daemon.plugins.color night-light-last-coordinates (35.65…, 139.74…)` vs Rocky `(91.0, 181.0)` — a user setting, not packaging). In particular: `screen-brightness-up ['XF86MonBrightnessUp']` and `screen-brightness-down ['XF86MonBrightnessDown']` (bound), no CSD-internal media-keys brightness keys, `org.cinnamon.settings-daemon.plugins.power backlight-helper-*` keys identical, `org.cinnamon.control-center.display` single key identical. Schema ownership by `rpm -qf` on the same five files: `cinnamon-settings-daemon-6.7.3^unstable-1.fc45` (power/media-keys/xrandr), `cinnamon-control-center-6.7.3^unstable-1.fc45` (display), `cinnamon-desktop-6.7.3^unstable-1.fc45` (keybindings).

**P3.8 — xdotool**
```
$ command -v xdotool
xdotool: binary not installed
```
Same as Rocky: no synthetic-key trigger on either VM; the binding evidence stands in per the plan's fallback.

**Rocky-vs-Fedora diff (per probe)**

| # | Probe | Rocky_Linux_10_Cinnamon | Fedora_45_Cinnamon | Attribution |
|---|---|---|---|---|
| D1 | `/sys/class/backlight` | empty (P1.2) | empty (P3.2) | environment (both VMs, no backlight hardware) |
| D2 | `brightnessctl` | absent, exit 127 (P1.3) | absent, exit 127 (P3.2) | gap, both (probe tool missing) |
| D3 | PCI display | Virtio 1.0 GPU, `virtio-pci` (P1.4) | same (P3.2) | environment |
| D4 | CSD version | 6.7.2-2.el10 (P1.6) | 6.7.3^unstable-1.fc45 (P3.3) | packaging (version) |
| D5 | `csd-power` running | yes, PID 3124 (P2.1) | yes, PID 1223 (P3.4) | — |
| D6 | `/usr/libexec/csd-backlight-helper` | **absent** (P2.8) | **present**, 15704 B, owned by fc45 RPM (P3.5) | **packaging — the port gap** |
| D7 | `Power.Screen` D-Bus object | present (P2.5) | present, introspection identical (P3.6) | — |
| D8 | `GetPercentage` (scripted) | fails: `Failed to execute child process "/usr/libexec/csd-backlight-helper" (No such file or directory)` (P2.9) | fails: `csd-backlight-helper failed: … No backlight devices present` (helper ran) (P3.6) | packaging (D6) + environment (D1) |
| D9 | `StepUp` (scripted) | `uii 0 0 0`, no-op (P2.9) | `uii 0 0 0`, no-op (P3.6) | environment (no backlight on either) |
| D10 | `screen-brightness-up` binding | `['XF86MonBrightnessUp']` (P2.6) | same (P3.7) | — |
| D11 | `screen-brightness-down` binding | `['XF86MonBrightnessDown']` (P2.6) | same (P3.7) | — |
| D12 | CSD-internal media-keys schema | no brightness keys (P2.6) | no brightness keys (P3.7) | — |
| D13 | probed schema files | all present (P2.3, P2.7) | all present (P3.5, P3.7) | — |
| D14 | other CSD plugin binaries | `csd-color`/`-wacom`/`-print*`/`-datetime-mechanism` absent (P2.1, P2.3) | present (P3.4, P3.5) | packaging (adjacent, out of brightness scope — recorded) |
| D15 | session type | Wayland (`gdm-wayland-session`, P1.1/P2.4) | X11/lightdm (P3.1) | session type |
| D16 | `xdotool` | absent (P2.10) | absent (P3.8) | gap, both (trigger attempt recorded as absent) |
| D17 | `journalctl --user` | "No journal files were found" (P2.10) | works (P3.6) | Rocky-side context gap (SSH session) |

No unattributed rows: every row names the variable it attributes to (packaging vs session type vs environment vs gap). D14 is recorded as an adjacent packaging observation outside this task's brightness scope (night light, wacom, printing, datetime mechanism).

### Item 4 — Root cause and classification

**Root cause.** The Cinnamon Settings brightness slider and the `XF86MonBrightnessUp`/`XF86MonBrightnessDown` keyboard shortcuts both resolve to the session-bus interface `org.cinnamon.SettingsDaemon.Power.Screen` (object `/org/cinnamon/SettingsDaemon/Power`, methods `GetPercentage`/`SetPercentage`/`StepUp`/`StepDown`) (P2.5, P2.6). It is the only brightness API on the user bus (P2.4), so any Cinnamon brightness control talking to the settings daemon must use it (the pane-to-daemon wiring is the plan's strategic-framing premise plus this uniqueness argument; the GUI pane itself was not exercised in this pass). The CSD power plugin `csd-power` implements those methods by spawning `/usr/libexec/csd-backlight-helper` for brightness get/set (P2.9 error string proves the spawn; the binary is shipped at that exact path by the fc45 RPM, P3.5). On `Rocky_Linux_10_Cinnamon` the helper is installed by no package: absent from disk (P2.8), absent from the `rpm -ql` file list of `cinnamon-settings-daemon-6.7.2-2.el10` (P2.3), and `rpm -qf` finds no owning package (P2.8). Consequence, verified: every screen-brightness get/set fails with `Failed to execute child process "/usr/libexec/csd-backlight-helper" (No such file or directory)` — the slider's read (`GetPercentage`) errors (P2.9 BEFORE/AFTER identical) and the shortcut path (`StepUp`) returns the degenerate `(0, 0, 0)` state, a no-op (P2.9). That is the operator's "no effect" in both Cinnamon Settings and the keyboard shortcuts. On the comparison VM the same calls fail differently — the helper runs and reports `No backlight devices present` (P3.6) — so the Rocky failure is a packaging artifact, not a D-Bus authorization problem (no authorization error on either VM; TASK-0035's question is not implicated here) and not a missing schema or unbound shortcut (D10-D13 identical).

**Classification: BOTH — port bug (P1) plus environment limitation (E1).**

- **P1 (port bug), named artifact: `/usr/libexec/csd-backlight-helper`** (and its `/usr/bin/` copy), owning package `cinnamon-settings-daemon` (the Rocky RPM must ship it; CSD hardcodes the invocation path, P2.9). Decision-tree basis, P1(e): the scripted D-Bus call fails on Rocky with a service error (helper ENOENT, P2.9) and fails differently on Fedora (helper ran, no backlight, P3.6). Sub-checks: (a) no `csd-xrandr` plugin binary exists in either distro's RPM — the plan's xrandr-plugin hypothesis is resolved: the brightness path is the power plugin plus the helper, and the xrandr schema is present on both (P2.3, P3.5); (b) the brightness D-Bus object is present on both (P2.5, P3.6); (c) the shortcuts are bound identically on both (P2.6, P3.7) — no override exists to own, so `cinnamon-rocky-defaults` is not implicated; (d) every probed schema file is present on both (P2.7, P3.7).
- **E1 (environment limitation).** No backlight device on the target (two agreeing sources: empty `/sys/class/backlight`, P1.2; QEMU Virtio 1.0 GPU with `virtio-pci` driver, P1.4/P1.5; `brightnessctl` absence recorded as a gap, P1.3) and on the comparison VM (P3.2). No working brightness path exists for a VM session: even with the helper present (Fedora), `StepUp` is a no-op `(0, 0, 0)` and `GetPercentage` reports no backlight devices (P3.6). End-to-end "the display got brighter" verification is impossible in this environment by design. What would make it testable: hardware with a real display and backlight (a physical machine with a backlight-capable panel; no QEMU GPU model exposes a backlight device).
- **Consequence for the fix phase (items 5-7, deferred this pass):** the DoD fix branch applies to the P1 finding. The fix is to include `csd-backlight-helper` in the Rocky `cinnamon-settings-daemon` RPM (spec/source fix; where the source target lives is determined in item 5). Even after the fix, brightness will not change on this VM (E1), so VM verification is limited to: helper present, `GetPercentage` failing with the helper's "No backlight devices present" instead of ENOENT, `StepUp` returning `(0, 0, 0)`, no new errors. Full brightness verification requires real hardware.
- **Inference, not verified:** that with the helper present, brightness actually changes on real backlight hardware, inferred from the spawn path (P2.9) and the fc45 packaging (P3.5). No such hardware exists in this environment.

**Alternatives considered**

### Problem: exercising/verifying the brightness path with no backlight and no GUI tooling
**Option A — install `xdotool` and synthesize the keypress.** How: `dnf install xdotool`, `xdotool key XF86MonBrightnessUp`. Pros: exercises the literal shortcut. Cons: a package install is guest state change beyond the read-only probes; on the target's Wayland session `xdotool` (X11-only) cannot inject into the Wayland compositor, so the trigger would be unreliable even with the tool; absent on both VMs.
**Option B — programmatic D-Bus call (chosen).** How: `busctl --user call` on `Power.Screen` (`GetPercentage`/`StepUp`) with property read-back before/after and journal capture. Pros: zero guest state change, exact programmatic equivalent of what the slider calls, works from SSH on both session types. Cons: does not exercise the physical key path (mitigated: binding evidence P2.6/P3.7, recorded per the plan's fallback).
**Chosen:** B, because the plan's acceptance criterion accepts recorded absence for the trigger, and B produces the before/after property values item 4 needs.
**Competing priorities:** physical-key evidence traded for zero-state-change probes; Rocky user-journal capture traded (unavailable over SSH, P2.10) — the D-Bus error string is a stronger record than the journal anyway.

**Changes**

| File | What changed |
|---|---|
| `planning/docs/TASK-0027-cinnamon-brightness-fix.md` | This section: items 1-4 evidence, per-probe diff table, root cause, classification. No source/spec files modified (diagnosis pass only). `## Definition of Done` lines 1-3 ticked (evidence above satisfies them; plan acceptance criterion "DoD lines 1-3 tickable"). |

**Checks run:** no compile/linter (no code change). Probe runs: item 1 (1 SSH run), item 2 (4 SSH runs: static state, D-Bus discovery, gsettings + scripted call, helper search + corrected call), item 3 (1 SSH run, full probe set), host `sudo -n virsh -c qemu:///system list` before and after (both VMs running, Ids 1 and 2 unchanged). `snapshot-list` after: Rocky `2026-10-04T11:36` (shutoff) + `2026-10-07-task0034-pre` (running, from TASK-0034 — not created by this pass), Fedora `2026-10-04T11:37` (shutoff); unchanged, no restore performed. No secret content in any output (password file used only via `sshpass -f`).

### Items 5-7 — Fix phase (2026-10-12), unblocked by the item 4 verdict (P1 + E1)

**Fix (item 5) — spec-only; the named artifact is built by a gudev gate the spec disabled on a false "unavailable" premise.** The helper is built only under `if gudev.found()` in `cinnamon-settings-daemon/plugins/power/meson.build:74` (dependency declared at `meson.build:55`: `gudev = dependency('gudev-1.0', required: get_option('use_gudev'))`); the spec passed `-Duse_gudev=disabled` with the comment `# BuildRequires: gudev-devel  # not available, feature disabled`. The premise is wrong on Rocky: the package exists under the RHEL name, and `gudev-devel` (the Fedora name) is the one that does not exist. Verified on the host:

```
$ dnf -q list available gudev-devel
Error: No matching Packages to list
$ dnf -q list installed libgudev libgudev-devel upower-devel
Installed Packages
libgudev.x86_64                       238-7.el10                      @anaconda
libgudev-devel.x86_64                 238-7.el10                      @appstream
upower-devel.x86_64                   1.90.10-2.el10                  @crb
$ pkg-config --modversion gudev-1.0
238
```

`libgudev-devel` was already installed on the host (AppStream; the earlier `gudev-devel` name is the one that does not exist in the Rocky repos), and it provides the `gudev-1.0` pkg-config file meson looks for. A second build dependency surfaced when the build ran: the `upower-glib` pkg-config file that `csd-power` links against (the -2 RPM requires `libupower-glib.so.3`) is provided by `upower-devel` (CRB), was never declared in the spec, and was not installed on the host at build time:

```
$ rpm -qpR rpms/cinnamon-settings-daemon-6.7.2-2.el10.x86_64.rpm | grep -i upower
libupower-glib.so.3()(64bit)
$ dnf -q provides '/usr/lib64/pkgconfig/upower-glib.pc'
upower-devel-1.90.10-2.el10.x86_64 : Headers and libraries for UPower
```

The fix therefore declares both and enables the feature; no source change (the `cinnamon-settings-daemon/` checkout stays clean at `18bb726dc21a`, Source0 byte-identical to upstream — see item 6). `spec/cinnamon-settings-daemon.spec` in the canonical repo, commit `ec49438b38aca571aa663654c568f4d6bb2933f4` (branch `feature/TASK-0024-rpm-signing-gpgcheck`, on top of `0b3773b`):

```
-Release:        2.el10
+Release:        3.el10
-# BuildRequires:  upower-glib-devel >= 0.99.11  # not available
+# Provides the upower-glib pkg-config file and headers that csd-power links against.
+BuildRequires:  upower-devel
-# BuildRequires:  gudev-devel  # not available, feature disabled
+# gudev: RHEL package name is libgudev-devel (Fedora calls it gudev-devel).
+# csd-power spawns csd-backlight-helper for every brightness get/set, so the
+# helper must be built: it is the only brightness backend (TASK-0027).
+BuildRequires:  libgudev-devel
     -Duse_cups=disabled \
-    -Duse_gudev=disabled \
     -Duse_wacom=disabled \
 %changelog
+* Mon Oct 12 2026 Team Chaotix <chaotix@metallinux.dev> - 6.7.2-3
+- Build and ship csd-backlight-helper: enable gudev (libgudev-devel on
+  Rocky, ...) so the backlight helper the csd-power plugin spawns for
+  every brightness get/set is installed. ... (TASK-0027 P1).
+- Declare upower-devel, which provides the upower-glib pkg-config file
+  csd-power links against (was undeclared).
```

Full diff: `git show ec49438 --stat` (1 file changed, 17 insertions, 4 deletions). The `%files` section needed no change: it already globs `%{_libexecdir}/csd-*`, `%{_bindir}/csd-*`, `%{_libdir}/cinnamon-settings-daemon/csd-*` — the -2 RPM simply never contained the files because they were never built.

**Build (item 6).**

Toolchain re-verified (plan item 6 first line):

```
$ command -v rpmbuild meson ninja
/usr/bin/rpmbuild
/usr/bin/meson
/usr/bin/ninja
```

Host state change (build dependencies, TASK-0026 precedent — host state had drifted since the -2 build, whose dependency closure is no longer fully installed): `sudo dnf install -y upower-devel colord-devel cups-devel lcms2-devel libcanberra-devel libnotify-devel libwacom-devel nss-devel rpms/gtk-layer-shell-0.10.1-1.el10.x86_64.rpm rpms/gtk-layer-shell-devel-0.10.1-1.el10.x86_64.rpm`. The first `rpmbuild` run failed its dep check on 8 BuildRequires (`colord-devel`, `cups-devel`, `gtk-layer-shell-devel`, `lcms2-devel`, `libcanberra-devel`, `libnotify-devel`, `libwacom-devel`, `nss-devel`); 7 of the 8 are in the Rocky repos, `gtk-layer-shell-devel` only as the team RPM in `rpms/` (installed together with its runtime pair). `libgudev-devel` was already installed (above).

Source0 staged from the clean working tree (plan: TASK-0026 method — same staging method as the provenance note, `git archive`), top dir `cinnamon-settings-daemon-6.7.2`:

```
$ git -C cinnamon-settings-daemon status --short
(empty — clean tree)
$ git -C cinnamon-settings-daemon rev-parse HEAD
18bb726dc21ac7127f50e7b2c9c3885d66dd34b6
$ git -C cinnamon-settings-daemon archive --format=tar.gz --prefix=cinnamon-settings-daemon-6.7.2/ HEAD > /tmp/rpmbuild-task0027/SOURCES/cinnamon-settings-daemon-6.7.2.tar.gz
$ sha256sum .../SOURCES/cinnamon-settings-daemon-6.7.2.tar.gz
272d5cb32ff4cd9a00f3c39446db95821b7b34e1befaface933a4cb44dd77b1b
$ md5sum .../SOURCES/cinnamon-settings-daemon-6.7.2.tar.gz
a766cdeb522f2ae186823b02ab563706
$ tar xzf ... -C /tmp/src0-verify && diff -r /tmp/src0-verify/cinnamon-settings-daemon-6.7.2 <checkout> --exclude=.git --exclude=builddir --exclude=buildd2
CONTENT-IDENTICAL
```

The tarball sha256 differs from the spec provenance note (`1141da2d...`) — that note records an earlier tarball; content identity against the clean checkout is verified above, which is the claim that matters (tar metadata differs between tarballs, content is identical).

Build:

```
$ rpmbuild --define '_topdir /tmp/rpmbuild-task0027' -ba spec/cinnamon-settings-daemon.spec
rpmbuild rc=0   (only warning: pre-existing "bogus date in %changelog", noted in TASK-0026)
```

Artifact checks:

```
$ rpm -qpl .../cinnamon-settings-daemon-6.7.2-3.el10.x86_64.rpm | grep backlight
/usr/bin/csd-backlight-helper
/usr/lib64/cinnamon-settings-daemon/csd-backlight-helper
/usr/libexec/csd-backlight-helper
$ rpm -qpl ... | grep -c 'csd-'     # -2 RPM: 141
144   # +3 = exactly the helper set (bin symlink, libexec, libdir copy)
$ rpm -qpi ... | grep -iE '^(Name|Version|Release|Signature)'
Name        : cinnamon-settings-daemon
Version     : 6.7.2
Release     : 3.el10
Signature   : (none)
$ md5sum / sha256sum ...
13da5875d3787034a30a670507fabe4f
7ee1281cb410dcb01a6ce2d7da7d99091bcb18918814ce776cb0eda78be7e3b6   (373076 bytes)
$ rpm -qpR ... | grep -iE 'gudev|upower'
libgudev-1.0.so.0()(64bit)      # new Requires vs -2
libupower-glib.so.3()(64bit)    # unchanged vs -2
$ rpm2cpio ... | cpio -idm; sha256sum usr/libexec/csd-backlight-helper
f231af260e3fca19804dcb9ec51640ef15ea7e693c1fa922b95e41f14c714d16   (15832 B, stripped ELF)
$ ls -l usr/bin/csd-backlight-helper
lrwxrwxrwx ... usr/bin/csd-backlight-helper -> ../libexec/csd-backlight-helper
```

Host smoke test of the extracted helper (`/sys/class/backlight` is empty on the host too):

```
$ ldd /tmp/helper-verify/usr/libexec/csd-backlight-helper | grep -E 'not found|gudev'
libgudev-1.0.so.0 => /lib64/libgudev-1.0.so.0 (0x...)
$ .../csd-backlight-helper --get-brightness
Warning: no backlight sources have been configured.
Check org.cinnamon.settings-daemon.plugins.power to configure some.
Could not get or set the value of the backlight: No backlight devices present
helper exit=5
```

Placement: `rpms-local/cinnamon-settings-daemon-6.7.2-3.el10.x86_64.rpm` (untracked, main RPM only — the debuginfo/debugsource pair stays in `/tmp/rpmbuild-task0027/RPMS/x86_64/` per the TASK-0026 placement precedent). `rpms/` tracked set untouched.

**Verification (item 7) — E1-bounded per the item 4 consequence paragraph.**

Host, before/after: `sudo -n virsh -c qemu:///system list` both times: `Fedora_45_Cinnamon` Id 1 running, `Rocky_Linux_10_Cinnamon` Id 2 running. `snapshot-list` after: Rocky `2026-10-04T11:36` (shutoff) + `2026-10-07-task0034-pre` (running, TASK-0034's), Fedora `2026-10-04T11:37` (shutoff) — unchanged, no restore.

Prior NEVRA and dependency state on `Rocky_Linux_10_Cinnamon`:

```
$ rpm -q cinnamon-settings-daemon
cinnamon-settings-daemon-6.7.2-2.el10.x86_64
$ rpm -q libgudev
libgudev-238-7.el10.x86_64     # new Requires satisfied, nothing to install
$ ls /usr/libexec/csd-backlight-helper
ls: cannot access '/usr/libexec/csd-backlight-helper': No such file or directory
```

Install (the one guest write of the fix phase; sudo password piped over the ssh stdin channel to `sudo -S`, file never read by any tool, content in no output):

```
$ scp rpms-local/cinnamon-settings-daemon-6.7.2-3.el10.x86_64.rpm howard@192.168.122.4:/tmp/
$ sudo -S rpm -Uvh /tmp/cinnamon-settings-daemon-6.7.2-3.el10.x86_64.rpm
Updating / installing...
cinnamon-settings-daemon-6.7.2-3.el10 ########################################
Cleaning up / removing...
cinnamon-settings-daemon-6.7.2-2.el10 ########################################
install rc=0
```

Helper presence, ownership, and binary identity on the VM:

```
$ rpm -q cinnamon-settings-daemon
cinnamon-settings-daemon-6.7.2-3.el10.x86_64
$ rpm -qf /usr/libexec/csd-backlight-helper
cinnamon-settings-daemon-6.7.2-3.el10.x86_64
$ ls -l /usr/libexec/csd-backlight-helper /usr/bin/csd-backlight-helper
lrwxrwxrwx. 1 root root   31 Oct 12 09:00 /usr/bin/csd-backlight-helper -> ../libexec/csd-backlight-helper
-rwxr-xr-x. 1 root root 15832 Oct 12 09:00 /usr/libexec/csd-backlight-helper
$ sha256sum /usr/libexec/csd-backlight-helper
f231af260e3fca19804dcb9ec51640ef15ea7e693c1fa922b95e41f14c714d16   # = RPM payload (chain closed)
$ ldd /usr/libexec/csd-backlight-helper | grep -c "not found"
0
$ ldd /usr/libexec/csd-backlight-helper | grep gudev
libgudev-1.0.so.0 => /lib64/libgudev-1.0.so.0 (0x...)
$ rpm -V cinnamon-settings-daemon
(no output, rc=0)
```

Helper standalone, invoked exactly as `csd-power` invokes it (`<libexecdir>/csd-backlight-helper --get-brightness -b firmware -b platform -b raw`, per `csd-power-manager.c:2465` plus the one-`-b`-per-entry preference construction at `csd-power-manager.c:2424-2434`, preference order from gsettings `backlight-helper-preference-order = ['firmware', 'platform', 'raw']`, P2.6):

```
$ /usr/libexec/csd-backlight-helper --get-brightness -b firmware -b platform -b raw
Could not get or set the value of the backlight: No backlight devices present
get exit=5
$ /usr/libexec/csd-backlight-helper --get-max-brightness -b firmware -b platform -b raw
Could not get or set the value of the backlight: No backlight devices present
max exit=5
```

The helper runs and reports the absence of backlight hardware — the same behavior class as the comparison VM (P3.6), not a spawn failure.

Item 2 daemon probe re-run (D-Bus, `XDG_RUNTIME_DIR=/run/user/1000`):

```
$ busctl --user get-property org.cinnamon.SettingsDaemon.Power /org/cinnamon/SettingsDaemon/Power org.cinnamon.SettingsDaemon.Power Percentage   # BEFORE
u 0
$ busctl --user call org.cinnamon.SettingsDaemon.Power /org/cinnamon/SettingsDaemon/Power org.cinnamon.SettingsDaemon.Power.Screen GetPercentage   # BEFORE
Call failed: csd-backlight-helper failed: Could not get or set the value of the backlight: No backlight devices present
$ busctl --user call org.cinnamon.SettingsDaemon.Power /org/cinnamon/SettingsDaemon/Power org.cinnamon.SettingsDaemon.Power.Screen StepUp
uii 0 0 0
$ busctl --user call org.cinnamon.SettingsDaemon.Power /org/cinnamon/SettingsDaemon/Power org.cinnamon.SettingsDaemon.Power.Screen GetPercentage   # AFTER
Call failed: csd-backlight-helper failed: Could not get or set the value of the backlight: No backlight devices present
$ busctl --user get-property org.cinnamon.SettingsDaemon.Power /org/cinnamon/SettingsDaemon/Power org.cinnamon.SettingsDaemon.Power Percentage   # AFTER
u 0
$ journalctl --user -n 20 --no-pager
No journal files were found.
-- No entries --
```

Reading against the pre-fix state (P2.9): `GetPercentage` no longer fails with `Failed to execute child process "/usr/libexec/csd-backlight-helper" (No such file or directory)` — the spawn now succeeds and the failure is the helper's own no-backlight report, byte-identical to the Fedora comparison signature (P3.6). `StepUp` is still `uii 0 0 0` — identical to pre-fix Rocky (P2.9) and to Fedora (P3.6): a no-op on a degenerate range, which is what E1 dictates. `Power.Percentage` property before/after: `0` → `0` — unchanged, expected: there is no backlight to change (E1). The plan's original item 7 line "Confirm the scripted D-Bus call now changes the property" is unreachable on this VM by design (item 4 consequence paragraph); the E1-bounded criteria in that paragraph are the ones verified here: helper present (above), `GetPercentage` failing with the helper's "No backlight devices present" instead of ENOENT (above), `StepUp` returning `(0, 0, 0)` (above), no new errors (install rc=0, helper exit 5 with the expected message, D-Bus output exactly the E1 signature). Journal: the user journal remains unavailable from the SSH session (same context gap as P2.10, recorded gap, not a finding); the D-Bus error strings are the direct record. `csd-power` is still PID 3124 (no restart — the helper is spawned per call, and the D-Bus results prove the spawn now succeeds). The installed RPM was left in `/tmp` on the VM (install artifact, deletable). Rollback: `sudo rpm -Uvh` of `rpms/cinnamon-settings-daemon-6.7.2-2.el10.x86_64.rpm` (tracked set) or `rpm -e` plus reinstall.

**E1-bounded verdict for the fix phase.** P1 is fixed at the RPM layer: the named artifact ships in the package (`rpm -qf` → the new NEVRA), the helper executes, and the D-Bus failure class moved from spawn-ENOENT (packaging artifact) to the helper's no-backlight report (environment). Brightness itself still cannot change on this VM — no backlight hardware (E1), so `GetPercentage` has no value to return and `StepUp` is a no-op (`StepDown` was not exercised in this pass; it shares the helper backend). End-to-end "the display got brighter" through both Cinnamon Settings and the keyboard shortcuts requires real backlight hardware (a physical machine with a backlight-capable panel; no QEMU virtual GPU exposes a backlight device). What that verification needs: a machine where `/sys/class/backlight` is non-empty, the -3 (or signed successor) RPM installed, then `GetPercentage` read-back around `SetPercentage` and a `StepUp` delta.

**Alternatives considered**

### Problem: how to get the helper into the Rocky RPM
**Option A — source patch: rewrite `csd_backlight_helper_get_best_backlight` to scan `/sys/class/backlight` directly (no gudev).** How: replace the `g_udev_client_query_by_subsystem` enumeration with a `GDir` scan of `/sys/class/backlight/*` reading each device's `type` attribute (semantics-preserving: gudev reads the same sysfs attribute), drop the `gudev.found()` guard in `plugins/power/meson.build`. Pros: no new runtime dependency. Cons: permanent source divergence from upstream on a file that is trivial upstream; the port would track a different code path than the Fedora comparison reference; the dependency is actually available, so the premise that forces the patch does not exist.
**Option B — spec-only: enable gudev under its RHEL package name (chosen).** How: `BuildRequires: libgudev-devel`, remove `-Duse_gudev=disabled`. Pros: zero source divergence (Source0 byte-identical to upstream @ `18bb726dc21a`, content-verified above); the helper builds through exactly the upstream code path that the Fedora reference RPM uses; smallest possible diff (one release bump plus two BuildRequires lines plus one option removal). Cons: the package gains a runtime requirement `libgudev-1.0.so.0` (satisfied: `libgudev-238-7.el10` was already installed on the VM before the fix; the -2 build's dependency closure was never the issue, the build gate was).
**Chosen:** B, because the original spec comment's "not available" was a package-name miss, not an availability fact — correcting the spec corrects the build without touching source.
**Competing priorities:** a new runtime dependency was accepted (already satisfied on the VM) in exchange for zero source divergence. The `upower-devel` declaration (a pre-existing undeclared build dependency, found when the build failed the dep check) was folded into the same release because the host no longer carries the undeclared pkg-config file and the release cannot build without the declaration.

**Changes**

| File | What changed |
|---|---|
| `spec/cinnamon-settings-daemon.spec` (canonical repo) | Release `2.el10` → `3.el10`; commented `gudev-devel` → `BuildRequires: libgudev-devel`; `-Duse_gudev=disabled` removed from `%build`; commented `upower-glib-devel` → `BuildRequires: upower-devel`; changelog entry. Commit `ec49438b38aca571aa663654c568f4d6bb2933f4`. No source files modified; the `cinnamon-settings-daemon/` checkout stays at `18bb726dc21a` (clean). |
| `rpms-local/cinnamon-settings-daemon-6.7.2-3.el10.x86_64.rpm` | Placed (untracked, 373076 B, unsigned — `Signature: (none)`). debuginfo/debugsource remain in `/tmp/rpmbuild-task0027/RPMS/x86_64/`. |
| Host state | `dnf install`: `upower-devel` (CRB), `colord-devel`, `cups-devel`, `lcms2-devel`, `libcanberra-devel`, `libnotify-devel`, `libwacom-devel`, `nss-devel` (AppStream/CRB), plus team `gtk-layer-shell-0.10.1-1` runtime + devel from `rpms/`. `libgudev-devel-238-7.el10` was already installed. |
| VM state (the one guest write) | `rpm -Uvh` of the -3 RPM, replacing -2 (`/tmp/...rpm` left in place). |
| `planning/docs/TASK-0027-cinnamon-brightness-fix.md` | This section: items 5-7. |

**Checks run:** no compile/linter beyond the build itself. `rpmbuild` rc=0 (single pre-existing bogus-date warning). RPM digests recorded (md5 `13da5875...`, sha256 `7ee1281c...`); `Signature: (none)`; payload file list (helper in all three locations; 144 `csd-` files vs 141 in -2); payload→VM sha256 identity of the helper binary (`f231af26...` both); `ldd` on host and VM (0 unresolved); helper standalone runs on host and VM (exit 5, expected message, exact csd-power invocation form); D-Bus before/after re-run (above); `rpm -V` rc=0; `rpm -qf` ownership; virsh list before/after (both running, Ids unchanged); `snapshot-list` unchanged (no restore); no secret content in any output (password file only ever `cat`-ed into a pipe and passed to `sshpass -f`).

**Competing priorities:** the unsigned -3 is local-only (`rpms-local/`, untracked); the tracked `rpms/` set (gpgcheck=1) is untouched — signing defers to operator key availability (plan risk table, certain/medium). User-journal capture remains unavailable over SSH (gap, P2.10) — the D-Bus error string is the stronger record anyway. The plan's item 7 acceptance line "the scripted D-Bus call now changes the property" was traded for the E1-bounded criteria in the item 4 consequence paragraph (property `0` → `0` recorded above in lieu). debuginfo/debugsource placement was traded as out of scope (TASK-0026 precedent), left in `/tmp` for the signing/publishing step to weigh.

---

## Review

*Owner: `Shadow`. Read-only — findings only, no edits. Severity order, blockers first.*

No blockers. The change as executed is sound and the evidence holds up under re-verification (list below). Three should-fix record/completeness gaps, blockers of task closure, not of the change.

### DoD line 43 is unsatisfiable as written under the BOTH verdict
**Severity:** should-fix
**Where:** `planning/docs/TASK-0027-cinnamon-brightness-fix.md:43` (DoD box 4); bounded criteria defined at `:585` (item 4 consequence), applied at `:812`-`:814`
**Problem:** the port-bug branch demands "brightness verified working through both Cinnamon Settings and the keyboard shortcuts with before/after evidence", but under the established E1 (no backlight on any VM here, P1.2/P3.2) that clause is unreachable; the E1-bounded criteria exist only in `## Implementation`, so box 4 can never be ticked as written.
**Failure scenario:** final-verdict step: `Big` cannot tick box 4 (the hardware verification never happens) and cannot honestly leave it unticked (fix, rebuild, install, bounded before/after D-Bus evidence all done, items 5-7); the task can never reach Definition of Done in this environment, and a box-checking reader sees box 4 as failed work when the environment, not the work, failed.
**Suggested direction:** `Big` records in `## Test Results` which clauses of line 43 items 5-7 satisfy (fix in package, rebuild, install on target, E1-bounded before/after evidence) and which are deferred to backlight hardware (end-to-end brightness through Settings and shortcuts, per the item 4 consequence paragraph at `:585`). The wording of line 43 is the planner's to amend (e.g. "verified working" to "verified to the extent the environment allows"); the conflict is named here, and the box stays unticked until the wording and the hardware remainder are both settled.
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

### Rebuild from origin silently produces -2: the fix lives in an unpushed local commit
**Severity:** should-fix
**Where:** `planning/docs/TASK-0027-cinnamon-brightness-fix.md:629` (commit `ec49438b38`, branch `feature/TASK-0024-rpm-signing-gpgcheck`); verified 2026-10-12: branch is ahead of origin by 5 commits, `ec49438b38` on that branch only (`git branch --contains`)
**Problem:** the only artifact carrying the fix is the local commit; origin (metalllinux) still carries the -2 spec, so a rebuild from a fresh clone (the signing step's natural procedure) builds -2, whose payload has no helper, and that build succeeds.
**Failure scenario:** operator key becomes available; the signing rebuild runs from a fresh clone of `metalllinux/cinnamon-for-rocky10`; `rpmbuild` exits 0; the signed RPM ships without `/usr/libexec/csd-backlight-helper`; installing it returns the VM to the ENOENT state (the original operator bug) with no error anywhere in the chain.
**Suggested direction:** record as a hard prerequisite of `## Release`: push `feature/TASK-0024-rpm-signing-gpgcheck` (carrying `ec49438b38`) before any signing or rebuild, and check the rebuilt payload before signing (`rpm -qpl <rpm> | grep -i backlight` must show exactly the 3 helper paths). `Tails` records the prerequisite; the push is `Knuckles`' step per the release workflow.
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

### Spec provenance note records the -2 build tarball hash, now stale
**Severity:** should-fix
**Where:** `spec/cinnamon-settings-daemon.spec:15-16`; the conflicting -3 tarball recorded at `planning/docs/TASK-0027-cinnamon-brightness-fix.md:678`
**Problem:** the note says "sha256 of this build tarball (git archive, top dir cinnamon-settings-daemon-6.7.2/): `1141da2d...`" — that is the -2 build's tarball; the -3 build staged a fresh tarball (sha256 `272d5cb3...`, content-verified against the clean checkout per `:678`/`:685`), so the note now contradicts every reproducible -3 build.
**Failure scenario:** the signing step (or any future rebuild) stages Source0 fresh per the spec method, computes the sha256, compares against the note, gets a mismatch, and concludes per the note's own framing that the tree is not the claimed upstream content — a false provenance failure that blocks or wrongly rejects a correct -3 rebuild.
**Suggested direction:** rework the note to carry the stable content anchor only (upstream commit `18bb726dc21a` plus the fetchable archive URL, both already at `spec/cinnamon-settings-daemon.spec:10-13`), and either drop the per-build tarball hash or relabel it as a non-reproducible -2 example (tar metadata differs between tarballs); record the `diff -r`-against-clean-checkout as the provenance check, since that is what the -3 build actually verified.
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

### Verified, no action
- Spec diff equals the doc's quotation: `git show ec49438b38` → 1 file, 17 insertions, 4 deletions; Release `2.el10`→`3.el10`; `BuildRequires: upower-devel` and `BuildRequires: libgudev-devel`; `-Duse_gudev=disabled` removed (no `use_gudev` occurrences left in the spec); `%changelog` entry present; `%files` globs at `spec/cinnamon-settings-daemon.spec:83-85` unchanged as claimed.
- Mechanism: `meson_options.txt:26-29` — `use_gudev` is `type: 'feature'`, `value: 'enabled'`, so removing the `-D` flag enables gudev (a `disabled` default would have voided the fix); `meson.build:55` dependency; `plugins/power/meson.build:74` helper under `if gudev.found()`; install scripts at `:87`/`:89` account for all three payload locations; `backlight_sources` holds only the helper's source.
- Helper spawn paths: `plugins/power/csd-power-manager.c:2465` (direct) and `:2555` (pkexec) are the only paths to the helper — the doc's "SetPercentage/StepDown share the helper backend" inferences are sound.
- RPM artifact (`rpms-local/cinnamon-settings-daemon-6.7.2-3.el10.x86_64.rpm`): md5 `13da5875...`, sha256 `7ee1281c...`, 373076 B, `Release: 3.el10`, `Signature: (none)`, 144 `csd-` files, exactly 3 backlight paths, `Requires` `libgudev-1.0.so.0` (new) + `libupower-glib.so.3` (unchanged), payload helper sha256 `f231af26...` (15832 B), `/usr/bin` a symlink to `../libexec/` — all match the doc.
- Rollback target intact: tracked `rpms/cinnamon-settings-daemon-6.7.2-2.el10.x86_64.rpm` present, 141 `csd-` files, no backlight files, `Release: 2.el10`.
- `rpms-local/` untracked (`git status`); tracked `rpms/` set untouched (`git ls-files rpms/ | wc -l` → 65).
- Source provenance: checkout clean at `18bb726dc21a`, remote `linuxmint/cinnamon-settings-daemon` — "byte-identical to upstream" holds; `dnf provides '/usr/lib64/pkgconfig/gudev-1.0.pc'` → `libgudev-devel-238-7.el10` (the new BR name is correct).
- DoD boxes 1-3 ticked with supporting evidence (items 1-3); plan items 1-7 acceptance lines met as recorded, except item 7's "the scripted D-Bus call now changes the property" line, unreachable under E1 by design (finding 1).

**Note for `Omega` (## Security):** the `cinnamon-settings-daemon` checkout's origin URL in `.git/config` embeds a live GitHub PAT. It is in no repo, commit, or planning doc, and it sits outside the `~/secrets/` convention. Flagged for classification; no token value recorded here.

---

## Security

*Owner: `Omega`. Read-only. Severity order.*

### Live `metalllinux` classic PAT with `repo,workflow` scope is world-readable (644) in two files, one of them a repo remote URL
**Severity:** high
**Vector:** secrets
**Where:** `~/AI/secrets/githubtoken.md` (644); `~/Linux/projects/github_pages/.git/config` (644, `remote.origin.url` for `metalllinux/metalllinux.github.io`); same token value in both (verified by shell comparison, no value recorded here)
**Attack:** the token's scope was verified live with a read-only probe (`curl -H "Authorization: token ..." api.github.com/user` → `HTTP/2 200`, login `metalllinux`, `x-oauth-scopes: repo,workflow`). `repo` = read/write on every metalllinux repo; `workflow` = may push `.github/workflows/` changes. Attacker: any process running on this host as a uid other than `howard` (the host has exactly two uid>=1000 users, `howard` and `nobody`; a root-owned daemon running as `nobody`, or a host backup that picks up 644 files) reads the file and owns the account surface. Concrete steps: read `~/AI/secrets/githubtoken.md`; clone `metalllinux/team-chaotix` with the token; modify a workflow (e.g. `.github/workflows/test-runner.yml`) to exfiltrate `~/AI/secrets/` and `~/secrets/`; push (the token authenticates, `workflow` scope permits the workflow change); the next workflow run executes on the self-hosted runner on this host as `howard` and yields `pass.txt` (VM sudo password) and `ai-machine-password.md`.
**Impact:** full control of the metalllinux GitHub account (every repo, every workflow) plus, via the self-hosted runner, this host, both VMs, and the AI machine.
**Fix:** (1) now: `chmod 700 ~/AI/secrets && chmod 600 ~/AI/secrets/*`; (2) remove the token from `~/Linux/projects/github_pages/.git/config` — set the remote to a token-free URL and authenticate via the existing operator/`gh` mechanism (or an SSH URL); (3) consolidate to a single `~/secrets/<name>.md` (600/700) per AGENTS.md §4 — the compliant directory already exists and currently holds only the dead token; (4) operator decides rotation (a live max-scope token in a world-readable file is rotation-worthy; per §4 the rotation step must be recorded in `## Status` for the operator — that section is Robotnik's, flagged here, not written); (5) check the metalllinux account audit log / token last-used for unexpected use.
**Resolution:** *(filled by `Tails`)*

### `~/AI/secrets/` holds live passwords world-readable (644 files in a 755 dir), including `pass.txt` used in this task
**Severity:** medium
**Vector:** secrets
**Where:** `~/AI/secrets/` (`drwxr-xr-x`): `pass.txt`, `ai-machine-password.md`, `temp_pass.md`, `token.md`, `githubtoken.md` all 644 (verified `ls -la ~/AI/secrets/`); §4 requires dir 700 / file 600, and the compliant `~/secrets` (700) exists in parallel
**Attack:** the same local reader as above (non-`howard` uid process, host backup) reads the passwords with no code execution: `pass.txt` is the sudo password for `howard` on `Rocky_Linux_10_Cinnamon` / `Fedora_45_Cinnamon` (this task's install used it via `sudo -S`, see ## Implementation item 7), `ai-machine-password.md` covers the AI machine.
**Impact:** root on both VMs via sudo, plus the AI machine. Rated medium, not high, because the marginal reader surface on this single-user host is narrow (only `howard` and `nobody` exist at uid>=1000; a root-class reader already has more) and no content was observed in any output this pass.
**Fix:** `chmod 700 ~/AI/secrets; chmod 600 ~/AI/secrets/*`; migrate to `~/secrets/` per §4 (one location, not two); operator decides whether to delete superseded files (`temp_pass.md`, `token.md`).
**Resolution:** *(filled by `Tails`)*

### Dead PAT still wired as this host's active git credential, in non-standard files, and copied into this session's log by this review
**Severity:** medium
**Vector:** secrets
**Where:** `~/.gitconfig` (644; `[credential] username/pass` plus global `url.https://<token>@github.com/.insteadOf=https://github.com/`), `~/.netrc` (600, non-standard: repo-URL line + raw-token line), `~/.git-credentials` (600, non-standard `[credential]` file), `~/AI/secrets/token.md` (644), `~/secrets/github-token.md` (700 dir); new copy this turn: `~/.local/share/opencode/opencode.db` (unmasked `git remote -v` output in my first verification pass)
**Attack / state:** that token returns 401 on `GET /user` and on both repo probes — it is dead. It is nonetheless what the global insteadOf rewrite injects into every `https://github.com/` git URL on this host (verified: `git remote -v` in both the canonical repo and the checkout shows it in the effective URL while the `.git/config` files themselves are clean). Consequence: every https `git clone/fetch/push` to github on this host fails auth until the rewrite is fixed (availability, not security), and any command that captures remote URLs (`git remote -v`, `git config --list`) prints the token — which is exactly how it reached my session log.
**Impact:** no live exposure (the token is dead). Standing risks: (1) whoever repairs the 401 by dropping a new token into these files recreates the 5-location proliferation that produced this state; (2) `~/.gitconfig` is 644; (3) the session-log copy is a §4 "no secret in any log" violation even though the copied value is dead.
**Fix:** remove the dead token: `git config --global --unset-all url."https://<token>@github.com/".insteadOf` (or re-point the rewrite at a token-free/SSH base), empty the non-standard `~/.netrc` / `~/.git-credentials` contents (or migrate the live token out per finding 1 and retire the files), `chmod 600 ~/.gitconfig`, delete `~/AI/secrets/token.md` (dead value); no history rewrite of the session store (per §4, that is the operator's call). Going forward, pipe any command whose output may contain a remote URL through a credential mask before it is recorded.
**Resolution:** *(filled by `Tails`)*

### Unsigned -3 RPM left in VM `/tmp`; `rpms-local/` (untracked) is the fix's only artifact location
**Severity:** low
**Vector:** supply-chain
**Where:** `/tmp/cinnamon-settings-daemon-6.7.2-3.el10.x86_64.rpm` on `Rocky_Linux_10_Cinnamon`; `rpms-local/cinnamon-settings-daemon-6.7.2-3.el10.x86_64.rpm` (untracked, `Signature: (none)`)
**Attack:** a local user on the VM (no privilege needed) can read and copy the unsigned RPM from `/tmp`; installing requires root, so no escalation. The concrete risk is operator confusion: a later manual `rpm -Uvh` from `/tmp` or from untracked `rpms-local/` after the signed successor exists installs the unsigned artifact with no error anywhere in the chain (file installs are not signature-checked).
**Impact:** an unsigned artifact remains a selectable install candidate past the signed release.
**Fix:** delete the `/tmp` copy on the VM (the doc already marks it deletable); keep `rpms-local/` untracked until signing; the `## Release` step installs only the signed artifact from tracked `rpms/`.
**Resolution:** *(filled by `Tails`)*

### Verified clean (no finding)

- **Spec diff** (`ec49438b38`, 1 file, 17+/4-): two repo-signed `BuildRequires` plus one meson-option removal; no shell, template, SQL, or URL construction; `%files` globs unchanged (Shadow-verified) — no new execution or injection surface.
- **polkit/authz:** `rpm -qpl` on -3 vs -2 shows the same two `.policy` files in both payloads — no new authorization surface on the helper's pkexec path (`csd-power-manager.c:2555`, unchanged upstream code per Shadow).
- **Source0:** no source change; byte-identical to upstream at `18bb726dc21a` (Tails `diff -r`, Shadow re-verified). The helper compiles from source already present in the -2 checkout: no new import, no new license exposure — the license verdict stays with `## License (Charmy)`.
- **Build deps:** `upower-devel`, `libgudev-devel`, `colord-devel`, `cups-devel`, `lcms2-devel`, `libcanberra-devel`, `libnotify-devel`, `libwacom-devel`, `nss-devel` from Rocky AppStream/CRB (repo-signed, version-pinned); the only file-installed RPM is the team `gtk-layer-shell-0.10.1-1.el10` (pre-existing TASK-0026 practice, host build-time only, not in the -3 payload).
- **Password handling in this task:** `sshpass -f` reads the file directly (no echo); `sudo -S` takes it over the stdin pipe; no `set -x`; the password appears in no recorded output in ## Implementation (verified by reading the section). The file-mode problem is finding 2, not the handling.
- **Helper input surface:** helper arguments derive from user-owned gsettings (`backlight-helper-preference-order`); the D-Bus user bus is per-user; no cross-user injection path introduced by this change.
- **No committed token copies:** worktree sweep (`grep -rInE` for `ghp_`/`gho_`/`github_pat_`/`x-access-token` and the `https://user:token@github.com` URL form, excluding `.git`) over `team-chaotix` (including `planning/`) and the canonical repo found only redacted `USER:***` references in TASK-0008 / TASK-0014 / SETUP.md; Shadow verified no copies in commits.

---

## License (Charmy)

*Owner: `Charmy`. Fourth in the review chain. Every license is verified at the upstream source
repository and the ref used, never from a copy in this repo.*

**Project license:** GPL-2.0 — appropriate

The canonical repo declares a license. Root `LICENSE` is the full GNU General Public License v2 text (339 lines, `head -6 LICENSE` and `wc -l LICENSE` in `/home/howard/Linux/projects/cinnamon-for-rocky10`). GitHub license detection for `metalllinux/cinnamon-for-rocky10` reports `spdx_id: GPL-2.0` (`GET https://api.github.com/repos/metalllinux/cinnamon-for-rocky10`). Tracked repo content is team-authored packaging, not component source: `spec/` (34 files), `rpms/` (65 RPMs), `vm-test/`, `tasks/`, `repo-setup/`, `src/cinnamon/0001-make-libxdo-optional.patch` (the `cinnamon` package, not this task), `keys/` (public key only) (`git ls-files | awk -F/ '{print $1}' | sort | uniq -c | sort -rn`). The component source checkouts are untracked build working copies, not repo content. So the root GPL-2.0 governs the team's own files, and each packaged Cinnamon component keeps its upstream license as declared in its spec `License:` tag and shipped in its RPM payload. For this task's package the declaration matches the upstream CSD license at the ref used (table below). No upstream code is re-licensed by this change, and no GPL-3.0-only or AGPL code enters the project, so no incompatible pair is introduced.

**Imported code**

| Component | Source (repo @ ref) | License (verified at) | Obligations met | Status |
|---|---|---|---|---|
| `cinnamon-settings-daemon` source, including `plugins/power/csd-backlight-helper.c` (the newly shipped helper) | `linuxmint/cinnamon-settings-daemon` @ `18bb726dc21a` | `COPYING` = GPLv2 and `COPYING.LIB` = LGPL-2.1, both full texts fetched raw at ref `18bb726dc21a`; no `LICENSE` file at that ref (404, upstream declares via COPYING); commit exists upstream, author and message match the spec provenance note (`GET https://api.github.com/repos/linuxmint/cinnamon-settings-daemon/commits/18bb726dc21a`, note at `spec/cinnamon-settings-daemon.spec:10-13`) | yes. Helper copyright header present: `Copyright (C) 2010-2011 Richard Hughes`, GPL v2 "or (at your option) any later version" (`sed -n '1,25p'` on the checkout, clean at the ref, `git -C cinnamon-settings-daemon rev-parse HEAD` = `18bb726dc21a`). Spec `License: GPLv2+` matches upstream. `%license COPYING COPYING.LIB` (`spec/cinnamon-settings-daemon.spec:81`) ships both texts; found at `/usr/share/licenses/cinnamon-settings-daemon/` in the -3 payload. Source0 content-identical to the ref (Tails `diff -r`, re-verified by Shadow) | pass |
| `libgudev` / `libgudev-devel` (new `BuildRequires`; new runtime `Requires: libgudev-1.0.so.0`) | Rocky 10 repo, `libgudev-238-7.el10`, `libgudev-devel-238-7.el10` | LGPL-2.1-or-later (`dnf -q repoquery --qf '%{license}' libgudev libgudev-devel`) | yes. Repo-signed dnf packages; devel headers are build-time only and not shipped; the runtime library is a dnf-managed dependency, compatible with the GPLv2+ binary | pass |
| `upower-devel` (new `BuildRequires`) | Rocky 10 repo, `upower-devel-1.90.10-2.el10` | GPL-2.0-or-later (`dnf -q repoquery --qf '%{license}' upower-devel`) | yes. Repo-signed, build-time only, not shipped | pass |
| `upower-libs` (provides `libupower-glib.so.3`; that `Requires` is unchanged from -2) | Rocky 10 repo, `upower-libs-1.90.10-2.el10` | GPL-2.0-or-later (`dnf -q repoquery --qf '%{license}' upower-libs`) | yes. Pre-existing runtime dependency, repo-signed | pass |

Notes:

- No new code was imported by this task. The helper source file was already in the -2 Source0 tree (same commit `18bb726dc21a`); the spec change only removes the `-Duse_gudev=disabled` build gate, so it adds no new license exposure. The -3 payload adds exactly the three helper files and changes no license file.
- The -3 payload contains only `csd-*` executables (GPLv2+ per the per-file headers) and no shared library, so `GPLv2+` covers everything shipped. `COPYING.LIB` is shipped for the LGPL-2.1 library portion of the upstream tree, which the RPM does not ship.
- The pre-existing `Requires: gtk-layer-shell` is a team-built package under the repo's own GPL-2.0, not imported code.
- The unsigned -3 RPM (`Signature: (none)`) is a signing state, not a license state; the license obligations above are met in the payload either way.

**Verdict:** pass

---

## Test Results

*Owner: `Big`. Verdicts, never raw log dumps.*

**Workflow run:**

This change is a local `rpmbuild` artifact, not a CI pipeline output, so there is no workflow run.
The checks below are host and VM verifications of the built RPM and its installed state on the
target. All guest commands ran as `howard` over SSH, the same read-only set as ## Implementation
item 7. No new guest writes.

| Check | What it exercises | Result | Notes |
|---|---|---|---|
| compile | the spec builds into the -3 RPM | PASS | `rpmbuild -ba` rc=0 (Tails). I re-verified the artifact. 373076 B, md5 `13da5875...`, sha256 `7ee1281c...`, `Release: 3.el10`, `Signature: (none)` (unsigned, local-only per plan). 144 `csd-` files, exactly 3 backlight paths (`/usr/bin/`, `/usr/libexec/`, `/usr/lib64/cinnamon-settings-daemon/`). Requires `libgudev-1.0.so.0` (new) + `libupower-glib.so.3`. I did not re-run `rpmbuild`. The artifact is the unit of change and is fully verified. |
| linter | spec well-formedness | N/A | No linter applies to a spec-only change. `rpmbuild` parsed the spec (rc=0), which is the strongest spec linter. Folded into compile. |
| unit tests | the named artifact runs | PASS | Helper standalone, the exact `csd-power` invocation form (`--get-brightness -b firmware -b platform -b raw`). Host payload and target VM both run and print `No backlight devices present`, exit 5. That is the expected E1 behavior, not a crash. `ldd` unresolved = 0 on the VM. No source change (checkout clean at `18bb726dc21a`, re-verified), so no source unit tests. |
| integration tests | CSD brightness D-Bus surface to helper | PASS | `GetPercentage` and `StepUp` on `org.cinnamon.SettingsDaemon.Power.Screen`, both VMs. Rocky `GetPercentage` now fails with the helper's `No backlight devices present`, not the pre-fix spawn-ENOENT, byte-identical to Fedora. `StepUp` = `uii 0 0 0` (no-op). `Power.Percentage` 0 to 0. The remaining no-effect is E1, not the port. |
| Sparky tests | Rocky Linux UI | not run | Justified below. No-render limitation plus E1. The D-Bus integration test exercises the same brightness surface at a lower level and captures the same assertion. |

**Checks requested vs run:** 5 requested, 3 executed (compile, unit, integration). linter folded into
compile (`rpmbuild` rc=0 parse is the spec linter). Sparky not run, justified in the table and
below. No check silently dropped.

**Shadow finding 1 split (DoD line 43).**

*Satisfied by items 5-7, verified in this run:*
- Fix in the Cinnamon package. The named artifact `/usr/libexec/csd-backlight-helper` is shipped by
  `cinnamon-settings-daemon-6.7.2-3.el10` (spec `ec49438b38`. `-Duse_gudev=disabled` removed,
  `libgudev-devel` and `upower-devel` declared). `rpm -qf` on the helper returns the new NEVRA.
  The helper is at all three payload locations.
- Rebuild. `rpmbuild -ba` rc=0. Payload helper sha256 `f231af26...`.
- Install on the target machine. `rpm -Uvh` on `Rocky_Linux_10_Cinnamon`, NEVRA -2 to -3.
  `rpm -V` rc=0.
- E1-bounded before/after evidence. `GetPercentage` failure signature moved from spawn-ENOENT
  (pre-fix, P2.9) to the helper's `No backlight devices present` (post-fix, verified live),
  byte-identical to the Fedora comparison. `StepUp` = `uii 0 0 0` (no-op). `Power.Percentage` 0 to
  0. No new errors (helper exit 5 with the expected message, `ldd` unresolved 0).

*Deferred to backlight hardware (E1, impossible in this environment by design):*
- End-to-end brightness through Cinnamon Settings (Display/Power pane) and the keyboard shortcuts.
  The display actually getting brighter, with `GetPercentage`/`SetPercentage`/`StepUp` returning a
  real value and changing it. This requires hardware with a real display and backlight.

**DoD box 5 (environment limitation, E1).**

No backlight device on the target (empty `/sys/class/backlight`, confirmed live. QEMU Virtio 1.0
GPU) or the comparison VM. What would make it testable is hardware with a real display and
backlight, specifically a physical machine with a backlight-capable panel (no QEMU virtual GPU
exposes a backlight device). On such a machine, with the -3 (or signed successor) RPM installed and
`/sys/class/backlight` non-empty, the verification is a `GetPercentage` read-back around
`SetPercentage` and a `StepUp` delta.

**Verdict.** The P1 port bug is fixed at the RPM layer and verified live on the target VM. The
helper ships in `cinnamon-settings-daemon-6.7.2-3.el10`, executes, and the D-Bus failure class
moved from spawn-ENOENT (a packaging artifact) to the helper's no-backlight report (environment),
byte-identical to the Fedora comparison. The E1 environment limitation is confirmed live on both
VMs. End-to-end brightness (the display getting brighter) is impossible in this environment by
design, which is the E1 remainder the DoD itself defers to real hardware (DoD line 43 reworded per
Shadow finding 1). Every test layer executable in this environment passes. The remainder is a
hardware dependency (operator hardware), not a code bug for `Tails` and not a harness bug for
`Big`. No FAIL.

---

## Docs

*Owner: `Vector`.*

Executed 2026-10-12. The doc surface for this change is `README.md` and
`INSTALL.md` in the canonical checkout
(`/home/howard/Linux/projects/cinnamon-for-rocky10`, branch
`feature/TASK-0024-rpm-signing-gpgcheck`). The tracked `rpms/` set is
untouched, so every doc that describes the published set stays accurate
as-is.

| File | Sections touched | What changed |
|---|---|---|
| `README.md` | new "Known issue." paragraph after the TASK-0026 TimezoneMap one (working tree, uncommitted) | The operator-reported bug and the fix state, same pattern as the TimezoneMap block. The published `cinnamon-settings-daemon` 6.7.2-2 was built with gudev disabled and does not ship `csd-backlight-helper` (the only brightness backend, the spec comment plus `csd-power-manager.c:2465`/`:2555`), so the Cinnamon Settings brightness slider read fails and the `XF86MonBrightnessUp`/`XF86MonBrightnessDown` shortcut step is a no-op, both at the D-Bus surface (## Implementation P2.9). The fix is built as unsigned `cinnamon-settings-daemon-6.7.2-3.el10`, verified at the D-Bus level on `Rocky_Linux_10_Cinnamon` (helper runs, reports the absence of backlight hardware instead of the ENOENT), and is unsigned and not in the published set, so the published 6.7.2-2 still lacks the helper. End-to-end brightness needs a display with a real backlight (E1). |
| `CHANGELOG.md` | n/a | No project-level changelog exists in this repo (no `CHANGELOG.md` at root; the only ChangeLog files are inside the untracked upstream checkouts). The packaging changelog is the spec's `%changelog`, updated by Tails in `ec49438b38` (the 6.7.2-3 entry). |

**Checked and needed no change:**

- `INSTALL.md` — the "Installed packages" table (line 319) lists
  `cinnamon-settings-daemon 6.7.2-2.el10` under "the versions published
  in `rpms/`"; the published set is untouched, so it is accurate.
  "Current status" (64 RPMs), the install paths, and "Verifying the
  release" (tag-pinned) are unchanged by this task. The Troubleshooting
  section has no known-issue pattern, and the TASK-0026 precedent
  documented its unsigned fix in the README only, so no troubleshooting
  entry was added.
- `rpms/SHA256SUMS` and the tracked `rpms/` set (65 files: 64 RPMs plus
  the manifest, `git ls-files rpms/ | wc -l` at 2026-10-12) — the -3 is
  unsigned (`Signature: (none)`) and stays in untracked `rpms-local/`.
  The manifest and the set describe the signed published set
  (gpgcheck=1), and adding the unsigned RPM would be wrong.
- `vm-test/install-set.txt` — names only, no version pinning.
- `vm-test/test-repo-setup.sh:670` and
  `vm-test/verify-install-packages.sh:47` — pin
  `cinnamon-settings-daemon|6.7.2-2.el10` to verify the published set.
  Correct while the published set is -2. When the signed -3 (and the
  TASK-0026 -4) replace the published RPMs, these pins move with `rpms/`
  and `SHA256SUMS` in the republish step.
- `spec/cinnamon-settings-daemon.spec` — the packaging doc itself,
  updated by Tails in `ec49438b38` (Release 3.el10, `BuildRequires:
  upower-devel` and `BuildRequires: libgudev-devel`,
  `-Duse_gudev=disabled` removed, `%changelog` entry). Its provenance
  comment still records the -2 build tarball sha256; that is Shadow
  finding 3, open, in Tails's resolution slot, and a spec comment rather
  than a user-facing doc.
- The untracked checkout `cinnamon-settings-daemon/` — upstream source,
  not repo content (its `ChangeLog` is upstream).
- `README.md` "Status" block ("Updated: 2026-09-19", "State: complete.
  All review findings resolved, all re-verifications PASS. Ready for the
  release PR") — a project-level release-state claim. The current state
  (two unsigned in-flight fixes, signing pending on the operator key per
  TASK-0033) is a release-flow judgment, and the TASK-0026 precedent left
  the block untouched.

**Could not verify / open items:**

- The GUI pane itself (the slider and shortcuts through the Control
  Center UI) was not exercised in this pass; the README's verification
  claims are scoped to the D-Bus surface the two controls use, which is
  what ## Implementation verifies. A Sparky/GUI run of the Display/Power
  pane on a machine with backlight hardware would settle it.
- Committing the README edit is deferred to the release flow, on purpose.
  The working tree already carried the TASK-0026 known-issue block
  uncommitted at task start (`git diff README.md`), and committing only
  this task's hunk would split one file's doc state across a commit and
  the working tree. The push is already a `## Release` prerequisite
  (Shadow finding 2, verified 2026-10-12 via `git ls-remote --heads
  origin`: origin's `feature/TASK-0024-rpm-signing-gpgcheck` is at
  `2466b70e`, five commits behind the local HEAD `ec49438b38`), and the
  README change should ride with it.

---

## Release

*Owner: `Knuckles`.*

**DONE checklist verified:** yes

Verified 2026-10-13 by Knuckles. Boxes 1-3 are ticked by Tails (## Implementation items 1-3). Boxes 4-6 verified against the evidence and ticked by Knuckles in this step. Box 4, fix in package, rebuild, install on the target, and E1-bounded before/after evidence per ## Implementation items 5-7, with the E1-blocked remainder documented in ## Test Results. Box 5, E1 documented in ## Test Results (DoD box 5 section). Box 6, final verdict in ## Test Results (Big, No FAIL).

- **Branch:** feature/TASK-0024-rpm-signing-gpgcheck in /home/howard/Linux/projects/cinnamon-for-rocky10, remote origin https://github.com/metalllinux/cinnamon-for-rocky10. The local remote URL is credential-free; the host's global gitconfig insteadOf rewrite is what injects a token into every https github URL (## Security finding 3). At step start the branch was 5 commits ahead of origin (origin 2466b70e, local HEAD ec49438b38, per ## Docs verification 2026-10-12), so the fix commit ec49438b38 lived on that branch only (Shadow finding 2).
- **Commits:** GPG-signed no (commit.gpgsign unset in the repo; branch convention is unsigned, author Team Chaotix <chaotix@metallinux.dev>, matching ec49438b38). New commits this step, in order: 5e081c4dc7 (spec provenance note, Shadow finding 3) and 9edabeda96 (README known issues, Vector's uncommitted change). The branch is now 7 commits ahead of origin.
- **PR:** PR #6 (head: this branch, "feat(release): TASK-0024 signed RPM set with gpgcheck=1 and SHA256 manifest") merged to main 2026-09-24 (a70aedc). No open PR on the branch (GitHub API check 2026-10-13). The commits made after that merge (8cde059, 620ceb4, 9d1eb46, 0b3773b, ec49438b38, plus the two from this step) need a new PR to enter main; that is the next release step, not this one.
- **Deploy:** n/a. No deployment workflow for this task. The -3 RPM is unsigned and local-only (untracked rpms-local/, installed on Rocky_Linux_10_Cinnamon by Tails); publishing awaits operator signing (TASK-0024, standing TASK-0033 rotation).

### Prerequisites executed (## Review findings 2-3, ## Docs)

- Shadow finding 2 (push the branch before any signing or rebuild): the push is blocked by the credential state, recorded below. The prerequisite stands. No signing or rebuild from a fresh clone until origin carries ec49438b38.
- Shadow finding 3 (stale Source0 provenance note; open in Tails's resolution slot per ## Docs): executed by Knuckles at release time in 5e081c4dc7 (## Review stays Shadow's section; recorded here per section 2 rule 2). The note now carries the stable content anchors (upstream commit 18bb726dc21a, fetchable archive URL) plus the diff -r-against-clean-checkout as the provenance check; the per-build tarball sha256 is dropped, per the finding's suggested direction.
- Vector's uncommitted README change: committed in 9edabeda96, rides the branch push.
- Standing checks for the signing step (findings 2-3 plus Omega finding 4): rebuild from a fresh clone of the branch and confirm the spec shows Release: 3.el10; the rebuilt payload must carry exactly the 3 helper paths, `rpm -qpl <rpm> | grep -i backlight` returning /usr/bin/csd-backlight-helper, /usr/libexec/csd-backlight-helper, /usr/lib64/cinnamon-settings-daemon/csd-backlight-helper; delete /tmp/cinnamon-settings-daemon-6.7.2-3.el10.x86_64.rpm from Rocky_Linux_10_Cinnamon; keep rpms-local/ untracked until signing; install only the signed artifact from tracked rpms/.

### Blocked by the standing TASK-0033 rotation step-stop

The canonical push failed at the credential stage (URL masked; no secret value in this record):

```
$ git push origin feature/TASK-0024-rpm-signing-gpgcheck   # GIT_TERMINAL_PROMPT=0
fatal: could not read Password for 'https://***@github.com': terminal prompts disabled
rc=128
```

The effective URL is the local credential-free URL plus the global insteadOf rewrite (the masked `***` is the token the rewrite injects; ## Security finding 3 verified that token live as dead on 2026-10-12). The configured store credential helper has no valid entry for this URL, and with prompts disabled the push cannot complete. This is the credential gap TASK-0033 flagged on 2026-10-05 and still holds open (its DoD Omega box is gated on it). The ## Status flag for the operator is Robotnik's to write per Omega's note in ## Security; the exact steps are recorded below. The team-chaotix push was not blocked: its local remote URL carries a live token (see the security flag below), the pre-commit probe `git ls-remote origin` returned rc=0, and this doc's push completed after the commit.

Operator steps (exact; no agent may complete them, per the standing step-stop):

1. Revoke the live metalllinux classic PAT (scope repo,workflow, verified live 2026-10-12 in ## Security finding 1). Its value is in ~/AI/secrets/githubtoken.md and embedded in the team-chaotix remote URL (same-value comparison 2026-10-13, no value recorded here). The global rewrite carries a distinct token (verified dead 2026-10-12) and the github_pages remote URL carries a value distinct from the team-chaotix one (not compared against the secret file; the operator reconciles). Revoke whatever the operator recognizes as live, and check the account audit log and token last-used for unexpected use.
2. Create the replacement PAT at least-scope for what the team needs, and store it per AGENTS.md section 4. One file in ~/secrets/, file mode 600, directory mode 700. Delete ~/AI/secrets/githubtoken.md.
3. Remove the credential state the tokens ride: `git config --global --unset $(git config --global --list --name-only | grep -i insteadof)` (the substitution keeps the value off the command line); in team-chaotix, `git remote set-url origin https://github.com/metalllinux/team-chaotix.git`, then unset the local credential.username, credential.password, credential.helper keys; in github_pages, set the remote to a token-free URL; remove the token lines from ~/.git-credentials and ~/.netrc; `chmod 600 ~/.gitconfig`. SSH-key auth is the preferred end state, because then no token exists on this machine.
4. Fix the file modes (## Security finding 2, AGENTS.md section 4): `chmod 700 ~/AI/secrets` and `chmod 600 ~/AI/secrets/*`, or consolidate into ~/secrets/. Decide the fate of temp_pass.md, token.md, ai-machine-password.md (## Security finding 2).
5. Re-run the blocked push: `git -C /home/howard/Linux/projects/cinnamon-for-rocky10 push origin feature/TASK-0024-rpm-signing-gpgcheck` (carries the 7 local commits: 8cde059, 620ceb4, 9d1eb46, 0b3773b, ec49438b38, 5e081c4dc7, 9edabeda96).
6. Verify the origin state after the push: fresh clone of the branch, `grep '^Release:' spec/cinnamon-settings-daemon.spec` returns 3.el10, then run the signing-step checks in the prerequisites list above.

### GitHub Issue

Searched open issues in metalllinux/cinnamon-for-rocky10 and metalllinux/team-chaotix (GitHub API, 2026-10-13): none open in either repo. No issue to close.

### Security flag (recorded per section 2 rule 2; ## Security is Omega's)

- The team-chaotix remote URL (local .git/config, never committed) embeds a classic PAT whose value matches ~/AI/secrets/githubtoken.md (same-value comparison in shell, no value read or printed). That file holds the live PAT with repo,workflow scope verified live in ## Security finding 1, so the team-chaotix remote authenticates with a live repo-scope token from a non-compliant location. The value surfaced in Knuckles's verification output on 2026-10-13 (session log) when the remote was printed, which makes it rotation-worthy in its own right. All of this is covered by the operator steps above.

---

## Archive

*Owner: `Espio`, the only agent that deletes. Superseded detail lands here rather than being
lost. Decisions, verified facts, rejected options with their reasons, known traps, and anything the
user said are never deleted.*

**Pruning log**

| Date | What was pruned or compressed | Rough size |
|---|---|---|
| | | |
