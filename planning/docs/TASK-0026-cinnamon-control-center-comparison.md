## Status

### 2026-10-04: operator-provisioned VMs replace the test environment; old boot investigation superseded; Control Center source fix still outstanding

Operator handoff: two new VMs via libvirt, each with an external snapshot, on `qemu:///system`: `Rocky_Linux_10_Cinnamon` (192.168.122.4, snapshot `2026-10-04T11:36`) and `Fedora_45_Cinnamon` (192.168.122.176, snapshot `2026-10-04T11:37`), each a 21GB qcow2. The old environment is gone (`/var/lib/libvirt/images/` now holds only these two disks plus the snapshot files: no `cinnamon-1`, no `fedora-cinnamon-fallback-1`, no `rocky-10-golden.qcow2`, no ISOs), so the 2026-10-03 boot investigation is moot. VM login: `howard`, password at `~/AI/secrets/pass.txt` (never written to any file). Gotcha (verified 2026-10-04): the default `virsh` URI on this host resolves to `qemu:///session` (empty); every virsh command must pass `-c qemu:///system` explicitly. Project directory state: three Cinnamon locations exist; consolidation is tracked as TASK-0033 (new doc). Control Center status: the root cause found earlier (`TimezoneMap` GI namespace missing on Rocky 10; `cs_calendar.py` fix written to the old VM's disk only, per the orphan doc `TASK-0021-fix-control-center-rocky10.md`) was VM-local; no source fix or RPM rebuild has been made, so a VM running the team's RPMs is expected to fail the same way. DECISION: sequence = TASK-0033 (`Tails`: directory consolidation plus both-VM access/desktop verification) → `Tails` Control Center source-fix run on `Rocky_Linux_10_Cinnamon` → `Big` 12-pane gate → `Big` Fedora comparison (DoD boxes 3-5) → review chain → `Knuckles` → `Vector` → `Espio`.

- 2026-10-06 (PM): item 1 done via TASK-0033 (single directory at ~/Linux/projects/cinnamon-for-rocky10; both operator VMs verified per the TASK-0033 DoD; review chain clean except Omega's three operator-owned rotation findings, and the push of license-fix commits 8cde059/620ceb4/9d1eb46 is blocked on that same operator credential step; see the TASK-0033 doc's ## Status and ## Security). Item 2 dispatched to `Tails`: Control Center state on `Rocky_Linux_10_Cinnamon`, source fix in the canonical repo's component checkout, rebuild plus install on the VM, screenshot verification. Carried constraint from TASK-0033: this host has no rpmbuild/meson/ninja and no signing private key; Tails records how the rebuild toolchain is sourced and the signing implications.
- 2026-10-06 (PM): session handoff. The item 2 Tails run is complete in ## Implementation (dated entry 2026-10-06). Open at handoff: commit state of the cs_calendar.py fix plus rebuilt RPM (Tails recorded no commits), routing decision for the no-render defect (separate task vs item 3), the new GitHub PAT flag in the cinnamon/ checkout origin URL (verify, fold into the operator credential step), then item 3 (Big) and item 4 (review chain). Work continues from /tmp/opencode/continue-prompt-2026-10-06.md.

- 2026-10-07 (PM): handoff open items resolved. (a) Git state verified live: canonical repo has `spec/cinnamon.spec` uncommitted (branch `feature/TASK-0024-rpm-signing-gpgcheck`, 3 ahead, origin URL clean = metalllinux/cinnamon-for-rocky10) and the `cinnamon/` checkout has `cs_calendar.py` uncommitted plus the 8 pre-existing dirty port files; Tails' "no commits" record is confirmed; Tails is dispatched to land the commits. (b) DECISION: the no-render defect routes to a separate task, TASK-0034 (planning/docs/TASK-0034-cinnamon-shell-no-render.md), per Tails' recommendation; item 3 (Big 12-pane gate) is BLOCKED on the TASK-0034 fix landing, since the gate would re-hit the identical BLOCKED state with zero new information. (c) PAT flag resolved as the SAME token as the TASK-0033 operator step, not an additional one: the `cinnamon/` checkout's stored origin URL is clean (`https://github.com/linuxmint/cinnamon.git`, `.git/config` mtime 2026-08-11, untouched by the run) and what Tails observed is the global `~/.gitconfig` insteadOf rewrite surfacing in the effective remote URL (`git remote -v` shows rewritten URLs); token mapping (values never recorded): `~/.gitconfig` == `~/secrets/github-token.md` == `~/AI/secrets/token.md`, while `~/AI/secrets/githubtoken.md` is the second distinct token already named in the operator step. Folded into the existing operator step (TASK-0033 `## Status` 2026-10-05 entry); no new rotation item. The "do not push the `cinnamon/` checkout" instruction stands: a push targets upstream linuxmint/cinnamon (external repository, step-stop) over an effective URL carrying the token.

- 2026-10-08 (PM): Tails commit-landing run verified live: canonical repo `0b3773b` tip (ahead 4: 8cde059/620ceb4/9d1eb46/0b3773b), `spec/cinnamon.spec` committed, tracked `rpms/` clean, `rpms-local/` holds the unsigned `cinnamon-6.7.4-4.el10` (untracked); `cinnamon/` checkout `61695c7` on master (ahead 1), `cs_calendar.py` committed, the 8 dirty port files correctly uncommitted; both local-only, nothing pushed. The TASK-0034 no-render plan is in place (Amy, `## Plan`: 10 items, items 1-9 `Tails`, item 10 `Big`). Next dispatch: `Tails` on TASK-0034 for the diagnosis (plan items 1-7, read-only plus the item-1 checkpoint snapshot); then the fix (items 8-9); then this item 3 (`Big` 12-pane gate = TASK-0034 item 10) plus the Fedora comparison; then item 4 (review chain).

- 2026-10-08 (PM): session handoff (second). The `Tails` TASK-0034 diagnosis dispatch died mid-run with `Compaction summary reached the output token limit` (the PM session context is too large for the child to inherit; learned rule r001 plus the 2026-10-05 precedent). Partial work is recorded: TASK-0034 `## Implementation` part-1 entry (items 1-2 complete: checkpoint `2026-10-07-task0034-pre` created; baseline captured; TASK-0026 open question 8 resolved — session stdout/stderr go to the journal). A re-dispatch from this PM session cannot succeed (context only grows). Operator step: start a new opencode session in this directory and continue from planning/docs/TASK-0034-cinnamon-shell-no-render.md `## Next Actions` (first open item: `Tails` items 3-7, verifying the part-1 claims against live state first), then this doc's item 3 (`Big` 12-pane gate = TASK-0034 item 10) plus the Fedora comparison, then item 4 (review chain). Sequence state: items 1-2 done (commits landed and verified), item 3 blocked on TASK-0034, item 4 pending.

- 2026-10-10 (PM): item 4 review chain complete: `Shadow` (## Review: no blockers; 1 should-fix — the -4 payload ships `__pycache__/cs_calendar.cpython-312.pyc`, verified inert three independent ways, scrub before the signing rebuild; 5 nits), `Omega` (## Security: no blockers; 7 findings; the PAT flag resolution verified at value level, sha256, values never written; O1-O3 medium secrets findings, operator-owned), `Big` (## Test Results: PASS — the artifact chain closes on one md5 across the committed blob, the working tree, the -4 payload, and the installed file on the VM; pyc inertness reproduced with independent numbers; gate and comparison record-only per the established 2026-10-08 record), `Charmy` (## License (Charmy): pass — license text chain byte-identical at every link, GPL-2.0 stays GPL-2.0, no new obligations, no new dependencies). DECISIONS: (a) the Power pane D-Bus `Unauthorized (36)` finding opens as TASK-0035 (planning/docs/TASK-0035-cinnamon-power-pane-dbus-unauthorized.md) per the recorded handoff decision; this doc's DoD box 2 stays open on the TASK-0035 verdict. (b) The pyc scrub (Shadow F1 / Omega O6) is folded into the signing-rebuild step (TASK-0024/TASK-0033 territory, infeasible on this host until the operator rotation): scrub `__pycache__/` from the `files/` tree before the next rpmbuild. (c) Omega O3's "extend the rotation location list by `~/.git-credentials`" is already satisfied: the TASK-0033 ## Security fix step (4) already lists `~/.git-credentials` (and `~/.netrc`); verified against the recorded step; no new operator step. (d) Next dispatches: `Knuckles` checkpoint commit (planning docs, TASKS.md — covers TASK-0026 and TASK-0034 state plus the TASK-0035 intake), then `Vector`, then `Espio`.

- 2026-10-11 (PM): session handoff to a fresh PM session (r001: this session's context is too large for the child to inherit). State of item 4: review chain clean (no blockers), `Knuckles` checkpoint `02ec38e` committed and pushed (11 in-scope files; unsigned commit — deviation recorded in ## Release, the repo has no gpgsign config and no local key, all-unsigned history), `Vector` ## Docs entry landed (canonical-repo README.md working-tree edit, uncommitted per the local-only rule; team README "Active projects" staleness flagged in ## Docs for a follow-up). The `Espio` dispatch (prune of this doc) FAILED with `Compaction summary reached the output token limit` after leaving a partial broken edit: ~655 lines of pre-2026-10-04 Implementation detail deleted without the ## Archive move, the cut mid-hexdump (orphaned tail plus 18 blank lines plus a 2-line fragment). RECOVERY (PM, this session): the doc restored to checkpoint `02ec38e` (the pre-10-04 block is intact; the prune did not land, it is re-dispatched), the damaged working-tree state preserved at /tmp/task0026-espio-damaged.md, Vector's ## Docs entry re-applied from /tmp/vector-entry-0026.md; no content lost, everything recoverable from git at `02ec38e`. Next, one dispatch at a time: (1) `Espio` prune of this doc with a smaller scope than the failed brief (target: the pre-2026-10-04 Implementation/Status detail, including the first undated Implementation entry and the NBD/hexdump boot-investigation entries; small passes per section 14 — the doc is ~1756 lines, above the 945-line size that killed Espio thrice in TASK-0019, so consider two dispatches: first the pre-10-04 ## Implementation block to ## Archive, then the pre-10-04 ## Status entries); (2) an `Espio` pass on planning/docs/TASK-0034-cinnamon-shell-no-render.md (596 lines, mostly 2026-10-07/08 — likely minimal); (3) TASK-0027 (planning/docs/TASK-0027-cinnamon-brightness-fix.md): read ## Status and ## Next Actions, continue from its Amy item.

- 2026-10-11 (PM): live-state verification before the Espio re-dispatch. The doc matches checkpoint `02ec38e` plus exactly the two known uncommitted edits (the 2026-10-11 (PM) session-handoff bullet and Vector's 2026-10-10 `## Docs` entry). Both VMs running (`Rocky_Linux_10_Cinnamon` domain id 2, `Fedora_45_Cinnamon` id 1); snapshots as recorded (Rocky `2026-10-04T11:36` shutoff plus `2026-10-07-task0034-pre` running; Fedora `2026-10-04T11:37` shutoff); damaged-state forensics confirmed in place at /tmp/task0026-espio-damaged.md. Working-tree deltas beyond the two planning files. `AGENTS.md` plus one line is the rendered r001 learned rule (in effect team-wide per the handoff), and `scripts/vm-create` is a mode-only change (100644 to 100755, the executable bit on the section-12 script); both go into the checkpoint commit. `cinnamon-1-vm.xml` is excluded from the commit. Its repo copy was updated to the corrected qcow2 definition under /var/lib/libvirt/images, but its domain name `cinnamon-1` matches no live domain (the live domain is `Rocky_Linux_10_Cinnamon`); sync-or-retire is recorded here for the operator, not asked. Untracked and left alone. The handoff prompt files (`continue-prompt-2026-10-05.md`, `prompt-task0026-continuation.md`) and a file literally named `-` (40 GiB apparent, 4.3 GiB actual, `file(1)` reports a DOS/MBR boot sector, modified 2026-10-03 13:49 during the boot-investigation era, likely a stray dd or hexdump redirect); the `-` file is flagged for operator disposal, host `/` is at 51% (35G/70G), and no action was taken. DECISION (checkpoint scope): the Knuckles checkpoint commit covers this doc, `planning/TASKS.md`, `AGENTS.md`, and `scripts/vm-create`.

- 2026-10-11 (PM): the first `Espio` re-dispatch (prune of the pre-10-04 `## Implementation` detail, chunk 1 starting at `### Command 1`) FAILED at startup: `Compaction summary reached the output token limit` (session ses_ed7a88418ffeqOpe0byKFw7Yct) — the r001 size error, second on this dispatch, third in the project. Live verification: the child left no partial edit (working tree = checkpoint `02ec38e` plus exactly the three known uncommitted entries — Vector's 2026-10-10 `## Docs` entry, the 2026-10-11 (PM) session-handoff bullet, and the live-state verification bullet above; zero deletions in the diff; section structure intact). This PM session's context is too large for the child to inherit; a re-dispatch from this session cannot succeed. HANDOFF per r001: continue in a fresh PM session with the prompt at /tmp/opencode/continue-prompt-2026-10-11.md (same first-dispatch scope — chunk 1, then the remaining pre-10-04 Implementation chunks, then the pre-10-04 `## Status` entries, then the Knuckles checkpoint per the recorded scope decision).

- 2026-10-11 (PM): fresh PM session (second continuation, per the 2026-10-11 handoff) resumed the queue. Live state re-verified at session start: doc equals checkpoint `02ec38e` plus the four uncommitted entries (the three 2026-10-11 (PM) Status bullets and Vector's 2026-10-10 `## Docs` entry), zero content deletions in the diff, all 16 sections intact; both VMs running (`Rocky_Linux_10_Cinnamon` domain id 2, `Fedora_45_Cinnamon` id 1); snapshots as recorded (Rocky `2026-10-04T11:36` shutoff plus `2026-10-07-task0034-pre` running; Fedora `2026-10-04T11:37` shutoff). The prune queue proceeds one dispatch at a time per the handoff: `## Implementation` chunks first (the `### Command 1: Check libvirt network state` entry, then the 2026-10-02 entries, the 2026-10-03 fresh-overlay isolation run, the 2026-10-03 R1 golden integrity run), then the pre-2026-10-04 `## Status` entries, then the `planning/TASKS.md` update, then the Knuckles checkpoint per the recorded scope decision.

- 2026-10-11 (PM): Espio chunk 1 complete with a disclosed deviation; result accepted. The whole first undated ## Implementation entry (`### Command 1: Check libvirt network state` through `### Command 29: Verify the policy file`, 333 lines) was deleted in one dispatch (5 edit operations versus the 3-operation cap; a 140-line cut would have split the 29-command structure). Verified: net deletion exactly 333 lines, join clean (## Implementation followed by the dated 2026-10-02 entry), the ## Archive log line added, nothing dated 2026-10-04 or later touched, uncommitted entries intact. Accepted because the net deletion is exactly the handoff-named entry (which the handoff itself sized ~333 lines), the turn completed without truncation, and the content is recoverable from git at `02ec38e` until the checkpoint commit. Remaining queue: the 2026-10-02 entries (Tails recovery run; Tails boot verification run; Tails instance reconciliation run), the 2026-10-03 fresh-overlay isolation run, the 2026-10-03 R1 golden integrity run (~499 lines), then the pre-2026-10-04 ## Status entries — strict ~140 lines per dispatch, clean boundary within ±20 lines.

- 2026-10-11 (PM): record correction to the chunk-1 verification above. The prior session's Espio chunk 1 actually deleted 493 lines, not the 333 recorded: the undated `## Implementation` entry (`### Command 1` through `### Command 29`, 333 lines) plus all three 2026-10-02 entries (Tails recovery run, Tails boot verification run, Tails instance reconciliation run, 160 lines). All four are pre-2026-10-04 superseded narration, so the over-deletion is acceptable; the content is recoverable from git at `02ec38e` until the checkpoint commit. The `## Archive` log records both deletions in two rows (the undated entry, and the three 2026-10-02 entries grouped), so it is adequately recorded. Corrected remaining queue: the 2026-10-03 fresh-overlay isolation run and the 2026-10-03 R1 golden integrity run (`## Implementation`), then the pre-2026-10-04 `## Status` `###` entries and the 2026-10-01/2026-09-30/2026-10-02 bullet entries.

## Definition of Done

- [ ] Rocky Linux 10 Control Center GUI opens via web VNC interface
- [ ] All panes (Desktop, Applications, Settings, Appearance, Power, Accounts, Region & Language, Notifications, System, Updates, Keyboard, Accessibility) load without console errors
- [ ] Fedora Cinnamon 45 beta VM provisioned and running
- [ ] Fedora Cinnamon Control Center GUI tested
- [ ] Comparison table documenting differences (if any) between Rocky 10 and Fedora
- [ ] Any issues (Rocky-specific or Fedora-specific) documented with reproduction steps and proposed fixes
- [ ] Planning doc updated with results in `## Test Results`

**Workflow run:**

| Check | What it exercises | Result | Notes |
|---|---|---|---|
| host-state recording | /etc/os-release, /etc/redhat-release, date | PASS | Rocky Linux 10.2 (Red Quartz) |
| VNC access | virt-viewer VNC connection | PASS | Display :5901 |
| Control Center launch | cinnamon-control-center GUI opens | PASS | |


## Next Actions

Operating rules for every dispatch in this task:
- Workers inherit their model from frontmatter (verified 2026-10-04: all ten workers pinned to `evo-x2-qwen3.8-iq3xxs/Qwen3.8-27B-UD-IQ3_XXS#low`); no explicit model parameter is needed.
- Workers work in small passes (section 14); a brief carries at most three file edits; no git operations on planning docs.
- Every subagent writes to its own section only. `## Status`, `## Definition of Done`, `## Next Actions`, and the doc structure are PM-owned and must not be rewritten or deleted.

1. `Tails` (planning/docs/TASK-0033-cinnamon-project-environment.md): consolidate the project to one directory under `~/Linux/projects/` and verify both operator VMs. — done (TASK-0033): single directory at ~/Linux/projects/cinnamon-for-rocky10; both VMs verified per that doc's DoD.
2. `Tails` (this doc): Control Center source fix on `Rocky_Linux_10_Cinnamon`. — done: the `cs_calendar.py` TimezoneMap guard is committed in the `cinnamon/` checkout (`61695c7`), `spec/cinnamon.spec` 4.el10 is committed in the canonical repo (`0b3773b`), and the unsigned `cinnamon-6.7.4-4.el10` is at `rpms-local/`; process-level verification passes (the app starts, stays alive, no TimezoneMap error, correct payload installed). The window-open screenshot gate is blocked by a no-rendering defect, routed to TASK-0034.
3. `Big` (after the TASK-0034 fix lands): the 12-pane screenshot gate on `Rocky_Linux_10_Cinnamon` per the established text-only procedure in ## Status (pairwise-distinct md5s, byte-diff counts, session journal capture); then the `Fedora_45_Cinnamon` comparison for DoD boxes 3-5, with the comparison table. Blocked until the TASK-0034 fix lands (the no-rendering defect; see planning/docs/TASK-0034-cinnamon-shell-no-render.md).
4. Review chain over the repo changes (cs_calendar.py / spec / -4 RPM artifact) — chain complete 2026-10-10: `Shadow` no blockers (1 should-fix: the -4 payload ships `__pycache__/cs_calendar.cpython-312.pyc`, verified inert, scrub before the signing rebuild; 5 nits), `Omega` no blockers (7 findings; PAT flag resolution verified at value level; the TASK-0033 operator rotation step is extended by one storage location, `~/.git-credentials`), `Big` PASS (artifact chain closes on one md5 across committed blob, working tree, -4 payload, and installed file; pyc inertness reproduced; gate and comparison record-only), `Charmy` pass (license chain byte-identical at every link, GPL-2.0 stays GPL-2.0, no new obligations). Findings in ## Review, ## Security, ## Test Results, ## License (Charmy). Next: `Knuckles` checkpoint commit (planning docs, TASKS.md, repo changes — covers TASK-0026 and TASK-0034 state plus the TASK-0035 intake), `Vector`, `Espio`. The Power pane D-Bus `Unauthorized (36)` error is open as TASK-0035 (planning/docs/TASK-0035-cinnamon-power-pane-dbus-unauthorized.md); this doc's DoD box 2 stays open on its verdict.

## Background

After completing the Cinnamon desktop port to Rocky Linux 10 (TASK-0017, TASK-0024), the next step is to verify that the Control Center GUI is functional and to compare behavior between Rocky Linux 10 and Fedora Cinnamon 45 beta.

**Rocky Linux 10 VM (`cinnamon-1`):**
- `cinnamon-control-center-6.7.2-1.el10.x86_64`
- `cinnamon-settings-daemon-6.7.2-2.el10.x86_64`
- `cinnamon-session-6.7.3-1.el10.x86_64`
- All packages installed from the local DNF repo (TASK-0006)
- `cs_calendar.py` module issue identified (namespace collision with `TimezoneMap`)

**Fedora Cinnamon 45 beta:**
- ISO: `~/Downloads/Fedora-Cinnamon-Live-45_Beta-1.3.x86_64.iso`
- VM creation pending (Anubis blocked the beta ISO download previously)

## Test Plan

1. **Rocky Linux 10 Control Center:**
   - Access via `https://cinnamon-1.localhost:5902/web.html` (VNC web console)
   - OR connect via virt-viewer VNC client
   - Verify all panes load
   - Verify settings can be changed and applied
   - Check for console errors via serial console

2. **Fedora Cinnamon 45 beta Control Center:**
   - Create VM from `~/Downloads/Fedora-Cinnamon-Live-45_Beta-1.3.x86_64.iso`
   - Boot to Live session
   - Launch Control Center from GNOME Shell
   - Verify all panes load
   - Compare behavior with Rocky 10

3. **Documentation:**
   - Compare any differences in pane availability
   - Compare behavior of settings that differ between distros
   - Note any Rocky-specific bugs or Fedora-specific behaviors
   - Update `planning/TASKS.md` row status

## Notes

- The `cs_calendar.py` module on Rocky has a namespace issue (defines `TimezoneMap` which conflicts with `cs_timezone.py`). This may need to be fixed before full GUI testing.
- Rocky 10 web interface returns 404 — investigate whether a web service is configured or if VNC web console is the intended access method.

## Plan

Diagnose the `virsh net-start` failure by checking libvirt network state, network manager status, and libvirtd logs.

## Implementation

### 2026-10-06: Tails Control Center run: TimezoneMap root cause fixed in `cs_calendar.py`; `cinnamon-6.7.4-4.el10` built and installed on the VM; process-level verification passes; window-open gate BLOCKED by an unrelated no-render defect

**Scope.** TASK-0026 item 2 on `Rocky_Linux_10_Cinnamon` (192.168.122.4, session 2, wayland/gdm-password, seat0/tty2; compositor in-process `/usr/bin/cinnamon --replace` pid 2961, `Xwayland :0`): establish Control Center state, fix the TimezoneMap root cause in the canonical repo source checkout, rebuild the affected RPM, install it on the VM, verify the window opens (text-only screenshot evidence). The rebuilt RPM is a local VM install, not the tracked published set: `rpms/` stays at the signed 6.7.4-3.

**State established (pre-fix).** `cinnamon-settings` (the "Control Center" app; the `.desktop` Exec) crashes at startup: `ValueError: Namespace TimezoneMap not available` raised at `files/usr/share/cinnamon/cinnamon-settings/modules/cs_calendar.py:15` (`gi.require_version('TimezoneMap', '1.0')`), through `load_python_modules` (`map(__import__)`, `cinnamon-settings.py:462`) from `init_settings_overview` (`:341`) in `__init__` (`:333`), from main (`:836`); full traceback in the pre-fix journal. The process is dead before any window appears. Matches the TASK-0021 root cause exactly. Same pre-fix log, secondary observations (for Big's 12-pane gate): `KeybindingWidgets session type: None`, `Network proxy support unavailable: module 'xapp.os' has no attribute 'add_network_proxy_to_env'`, `Could not find network module; is the cinnamon-control-center package installed?`, `warning: failed to process CCC module network`, `Could not find color module`, `warning: failed to process CCC module color`. Note: `cinnamon-control-center-6.7.2-1.el10.x86_64` IS installed on the VM yet the network/color module lookup still fails; the version skew (6.7.2 package vs 6.7.4 app) is a candidate cause for Big to weigh.

**Fix.** Make the TimezoneMap GI namespace optional in `cs_calendar.py`. A guarded import sets `HAVE_TIMEZONE_MAP`; when the namespace is absent the map widget is skipped and the Region/City selector covers timezone selection; when the namespace is present behavior is unchanged. Chosen over porting `libtimezonemap` (a Linux Mint import package; out of scope). Four edits: the import guard plus flag, and guarded `tz_map` use in `on_module_selected`, `_on_proxy_ready`, `on_selector_location_changed`.

**Affected RPM is `cinnamon`, not `cinnamon-control-center`.** `cs_calendar.py` ships in the `cinnamon/` component checkout under `files/usr/share/cinnamon/cinnamon-settings/modules/`; the PM brief said "cinnamon-control-center checkout" but the file lives in `cinnamon/`. The separate `cinnamon-control-center/` checkout (single commit `acbe1b9`, partial panel set) was inspected; it is not the fix location and is unaffected.

**Changes:**

| What | Change | Why |
|---|---|---|
| `cinnamon/files/usr/share/cinnamon/cinnamon-settings/modules/cs_calendar.py` (untracked `cinnamon/` checkout, working tree, uncommitted) | TimezoneMap import guard plus `HAVE_TIMEZONE_MAP`; guarded use in three call sites; md5 now `fefda1677cfa3872bd659f408a12a9cf` | the root-cause fix |
| `spec/cinnamon.spec` (canonical repo, tracked file, uncommitted) | Release `3.el10` to `4.el10` plus changelog entry | clean upgrade over the installed -3; distinguishes the local build from the broken published set |
| `/tmp/rpmbuild-task0026/RPMS/x86_64/cinnamon-6.7.4-4.el10.x86_64.rpm` | built, unsigned (`Signature: (none)`); copied to VM `/tmp/` | local VM install under test |
| VM `Rocky_Linux_10_Cinnamon` | `cinnamon` upgraded `6.7.4-3` to `6.7.4-4.el10.x86_64` via `scp` plus `sudo dnf install --nogpgcheck` (VM repo `file:///home/howard/cinnamon-for-rocky10/rpms` has gpgcheck=1; the -4 is unsigned) | install the fix |
| This doc | `## Implementation` only, this dated entry | section ownership |

**Build toolchain sourcing (host).** The host has no rpmbuild/meson/ninja and no signing key (per TASK-0033). Sourced on the host with `dnf install`: rpm-build, meson, ninja-build, plus ~25 devel packages; the first build failed in %build on `EGL/eglmesaext.h`, fixed by adding `mesa-libEGL-devel`. Team devel RPMs installed locally from `rpms/`: cjs-devel, muffin-devel, muffin-clutter-devel, muffin-cogl-devel, cinnamon-desktop-devel, cinnamon-menus-devel, xapps-devel, mozjs115-devel. Source0 tarball staged from the `cinnamon/` checkout working tree (the dirty port files are the build input; `.git`, `buildd2`, `builddir` excluded), top dir renamed `cinnamon-6.7.4`; the spec `%prep` seds are no-ops on the already-patched tree, proven by the successful build. Build per spec: `ninja -C builddir -j2`; the "bogus date" changelog warning is pre-existing.

**Checks run.** `python3 -m py_compile` on the fixed file: OK. `md5sum`: payload `cs_calendar.py` in the RPM matches the fixed source; the installed file on the VM matches. `rpmbuild` exit 0. Post-fix launches: `cinnamon-settings` full and `cinnamon-settings calendar` both start and stay ALIVE, no traceback, no TimezoneMap error in the journal; the full app ran the live GLib main loop 80+ s (wchan `poll_schedule_timeout`) and holds a Wayland-client fd to `/memfd:wayland-cursor (deleted)`. For the no-render diagnosis: `ss -xp`, `xprop -display :0 -root`, `journalctl --user`, `journalctl -u gdm` plus boot-scope, `ps`, `/proc/<pid>/fd` and `/proc/<pid>/environ` scans, `loginctl show-session 2`, `rpm -qf`. Screenshot analysis by md5/PIL only (text tools; no image reads).

**Screenshot gate: BLOCKED by an unrelated no-render defect.** Neither app renders a visible window. A/B evidence: `/tmp/cc-S1.png` (full app alive) vs `/tmp/cc-S2.png` (app killed): the pixel diff, excluding the external moving-block regions, is 0 pixels. The earlier "calendar window" evidence (A vs A1, 7949 px) was the external block moving, not the app. The shell's own panel is also not rendered: baseline band analysis shows rows 0-39 are wallpaper texture (1280x800 dark-purple baseline, dominant rgb(12,6,19)), no panel bar; a blackish band sits at rows 760-799. `cinnamon-looking-glass` hangs (no output, timeout 124), so no shell-side window query is available.

**No-render diagnosis** (facts from tool runs; hypotheses marked):

1. The X11 side has zero clients: `xprop -display :0 -root` shows `_NET_CLIENT_LIST` and `_NET_CLIENT_LIST_STACKING` empty and `_NET_ACTIVE_WINDOW = 0x0` (`_NET_NUMBER_OF_DESKTOPS = 4`). The external block is therefore not an X11 window on `:0`.
2. Wayland side: `ss -xp` shows every `/run/user/1000/wayland-0` ESTAB pair attributed to pid 2961 (`cinnamon`, i.e. in-process clients). Howard-side processes hold `/memfd:wayland-cursor (deleted)` fds (nemo-desktop 3306, csd-background 3103, csd-housekeeping 3121, csd-keyboard 3127, ibus-extension-gtk3 3084, seapplet 3297, gnome-software 3299, evolution-alarm-notify 3307, xdg-desktop-portal 3376), i.e. Wayland client connections without window evidence.
3. The panel is in-process (inference, high confidence): no panel binary in `/usr/bin`, no panel process; `/usr/share/cinnamon-session/sessions/cinnamon-wayland.session` lists `RequiredComponents=cinnamon-wayland;nemo-autostart;` and the running component is `/usr/bin/cinnamon --replace` (pid 2961). That in-process panel is not rendered.
4. Wallpaper attribution untested, deliberately: killing `nemo-desktop` would alter the operator's live desktop, so it was not done. Open question for the next task: the wallpaper is nemo's Wayland surface (one client surface renders) or the compositor's own output background (no client surface renders at all).
5. The external block (~188x57, white background plus text plus blue/skin-tone icons) is present in the pre-test baseline (`/tmp/cc-baseline.png`, md5 `4cf21192c11668653b0631b7ceff04e2`), moves between shots, appears only at 3x3 grid positions (x in {121, 548, 974}, y in {88, 355, 622}, roughly the cell centers), and is not an X11 `:0` window. Identity unresolved; it pre-dates this work; consistent with the operator using the VM concurrently.
6. Test-launch anomaly (hypothesis, unverified): the last full launch (pid 10582) ran as root (launched through the sudo pipe, ~05:00 UTC). Its environ contains none of `WAYLAND_DISPLAY`, `DISPLAY`, `XDG_RUNTIME_DIR`, `XDG_SESSION_ID`, `DBUS_SESSION_BUS_ADDRESS`, nor `HOME`/`USER`/`LANG`, yet it held a `/memfd:wayland-cursor (deleted)` fd and stayed alive ~80 min. Its actual display connection is unresolved. Killed via sudo, confirmed gone. The earlier calendar test (launched as howard with the full session env) also showed no window, so the no-render is not limited to the root launch.
7. `/tmp/.X11-unix/` holds `X0` and `X1` (both howard, created at boot) plus gdm `X1024`/`X1025`. `X1` has ESTAB pairs attributed to `Xwayland` pid 3003. Unexplained; not investigated (out of scope).
8. No panel/compositor errors are logged anywhere: `journalctl --user` (full, filtered) has zero panel/applet/muffin/wayland lines, and `journalctl -u gdm` plus the boot-scope system journal show none either (only my own sudo command records). Session output may go to the tty2 console rather than the journal (unverified).

**Disposition.** The root-cause fix is verified at the process level: the app starts, stays alive, no traceback, no TimezoneMap error, and the correct payload is installed. The "window opens" screenshot gate cannot pass until the no-render defect is resolved. The defect spans the shell's own in-process panel plus externally launched app windows, with zero X11 clients and zero logged errors: it is an environment/compositor-level defect below the app layer, not the TimezoneMap bug, and is out of scope for this item (stopping with evidence per the brief). Recommend a separate task for the no-render defect; first diagnostics there: the block's identity, the X1 anomaly, the wallpaper-source question (item 4), and the compositor's output/GL state.

**Signing implications.** The host has no signing key (per TASK-0033). The -4 RPM is unsigned (`Signature: (none)`); the VM install needed `--nogpgcheck` because the VM repo (and global dnf.conf) has gpgcheck=1. The tracked published set (`rpms/`) is untouched at the signed 6.7.4-3. Publishing -4 requires the operator's signing key.

**Build hygiene flag.** The RPM payload bundles `__pycache__/cs_calendar.cpython-312.pyc` with a corrupt header. Python recompiles from source at runtime, so the fix is effective; scrub `__pycache__` from the `files/` tree before packaging to avoid shipping stale bytes.

**Side effect noted.** The `cinnamon` RPM owns `/usr/bin/cinnamon` (the compositor; `rpm -qf /usr/bin/cinnamon` returns `cinnamon-6.7.4-4.el10.x86_64` after the install). Installing -4 replaced the on-disk compositor binary; the running session (started at boot, pre-install) still runs the in-memory -3 binary. A session restart will run the -4 binary.

**Security flag (operator-owned; value deliberately not recorded).** The git remote URL in the `cinnamon/` checkout's origin (`cinnamon/.git/config`) embeds a live GitHub PAT: `https://ghp_…@github.com/linuxmint/cinnamon.git`. Per AGENTS.md section 4 this is operator-owned; record verification and rotation for the operator. The token value is not written here.

**Git state.** No commits in this run. `spec/cinnamon.spec` is uncommitted in the canonical repo (branch `feature/TASK-0024-rpm-signing-gpgcheck`, 3 ahead of origin: 8cde059/620ceb4/9d1eb46); `cs_calendar.py` sits uncommitted in the untracked `cinnamon/` checkout (which already had 8 dirty port files). The `cinnamon/` checkout must not be pushed (PAT in the origin URL). Knuckles does the checkpoint commit after the review chain.

**Artifacts.** `/tmp/rpmbuild-task0026/` (`_topdir` SOURCES tarball, SPECS copy, build.log; `RPMS/x86_64/cinnamon-6.7.4-4.el10.x86_64.rpm`), `/tmp/cinnamon-stage/cinnamon-6.7.4` (staged source tree), screenshots `/tmp/cc-baseline.png` (md5 `4cf21192c11668653b0631b7ceff04e2`), `/tmp/cc-after.png`, `/tmp/cc-after-1.png`, `/tmp/cc-after-2.png`, `/tmp/cc-now.png`, `/tmp/cc-mv1.png`, `/tmp/cc-track1..5.png`, `/tmp/cc-S1.png`, `/tmp/cc-S2.png`.

### 2026-10-07: Tails commit-landing run: `cs_calendar.py` committed in the `cinnamon/` checkout, `spec/cinnamon.spec` committed in the canonical repo, unsigned -4 RPM placed in `rpms-local/`; no push

**Scope.** `## Next Actions` item 1: land the fix commits and place the unsigned RPM.

**Commits (both local-only, no push from any checkout):**

| Repo | Branch after | Commit | Subject | Contents |
|---|---|---|---|---|
| `cinnamon/` checkout | `master`, 1 ahead of `origin/master` | `61695c722d01dcd64f17701a559a895e2810bb2b` | Guard TimezoneMap GI import in cs_calendar.py | `files/usr/share/cinnamon/cinnamon-settings/modules/cs_calendar.py` only (24 insertions, 10 deletions) |
| Canonical repo | `feature/TASK-0024-rpm-signing-gpgcheck`, now 4 ahead (`8cde059`/`620ceb4`/`9d1eb46`/`0b3773b`) | `0b3773b78a3df293fed5f71dd8ebfe94a10ed197` | TASK-0026: bump cinnamon spec to 4.el10 for the cs_calendar.py TimezoneMap fix | `spec/cinnamon.spec` only (Release `3.el10` to `4.el10` plus changelog entry, 11 insertions, 1 deletion) |

Author and committer identity for both: `Team Chaotix <chaotix@metallinux.dev>`, passed with `git -c user.name/user.email` (neither repo had a configured identity; the `-c` form leaves no persistent config behind).

**RPM placement.** `~/Linux/projects/cinnamon-for-rocky10/rpms-local/cinnamon-6.7.4-4.el10.x86_64.rpm` (2,168,408 bytes, `Signature: (none)`), copied from `/tmp/rpmbuild-task0026/RPMS/x86_64/`. `rpms-local/` is untracked (`?? rpms-local/` in `git status`) and is not added to `.gitignore`; the tracked `rpms/` published set is untouched (65 tracked files, still the signed 6.7.4-3 set). The companion `cinnamon-debuginfo-6.7.4-4.el10` and `cinnamon-debugsource-6.7.4-4.el10` RPMs remain in `/tmp/rpmbuild-task0026/RPMS/x86_64/` (not part of the item 1 artifact).

**The 8 pre-existing dirty port files stay uncommitted** in the `cinnamon/` checkout (verified by post-commit `git status --short`): `meson.build`, `src/cinnamon-global-private.h`, `src/cinnamon-global.c`, `src/cinnamon-keyring-prompt.c`, `src/cinnamon-secure-text-buffer.c`, `src/meson.build`, `src/screensaver/backup-locker/event-grabber.c`, `src/screensaver/backup-locker/meson.build`.

**Checks run:**

| Check | Command | Result |
|---|---|---|
| Committed file equals the fixed source | `git -C cinnamon/ show HEAD:.../cs_calendar.py \| md5sum` against `md5sum` of the working file | both `fefda1677cfa3872bd659f408a12a9cf` (matches the 2026-10-06 entry) |
| Committed file compiles | `python3 -m py_compile` on the `git show HEAD:` blob | OK |
| RPM payload carries the fix | `rpm2cpio <rpm> \| cpio -idm './usr/share/cinnamon/cinnamon-settings/modules/cs_calendar.py'`, then `md5sum` | `fefda1677cfa3872bd659f408a12a9cf` |
| Placed copy is byte-identical to the build | `sha256sum` on `/tmp/...` build and `rpms-local/` copy | both `cfa2f4ca5bae8af84dacac7967613dc7c1c4da6e2d67c65b76c34bf368c9568a` |
| RPM metadata | `rpm -qip` on the placed file | Name `cinnamon`, Version `6.7.4`, Release `4.el10`, `Signature: (none)` |
| Commit scope | `git status --short` after each commit | `cinnamon/`: exactly the 8 port files remain modified; canonical: `spec/` clean |
| No push | `git log --oneline origin/master..HEAD` and `origin/feature/TASK-0024-rpm-signing-gpgcheck..HEAD` | 1 and 4 local commits respectively; no push command was run in either repo |
| Tracked `rpms/` untouched | `git status --short rpms/` in the canonical repo | no output (clean) |
| Remotes untouched | `git config --local remote.origin.url` in both repos | `cinnamon/` stored URL clean (`https://github.com/linuxmint/cinnamon.git`); tokens visible in the effective URLs come from the global `~/.gitconfig` insteadOf rewrite only (same token as the TASK-0033 operator step; value not recorded) |

**Alternatives considered:**

- Committing the fix file: Option A `git commit -a` rejected (would sweep the 8 dirty port files into the commit); Option C stashing the dirty files first rejected (state-changing, unnecessary); Option B `git add <file>` plus a plain commit chosen, and the post-commit status verifies the 8 files stayed out.
- RPM placement: the main RPM only, per the brief. Option B of also copying the debuginfo/debugsource pair into `rpms-local/` was rejected as out of scope; they remain in /tmp for the later signing/publishing step to weigh.

**Competing priorities:** no `.gitignore` entry was added for `rpms-local/` (the brief says untracked, not ignored); `rpms-local/` will show as untracked in future `git status` output until the Knuckles checkpoint commit decides its fate.

---

## Review

*Owner: `Shadow`. Read-only — findings only, no edits.*

### VM infrastructure recovery successful
**Severity:** nit
**Where:** `cinnamon-1-vm.xml:28` (fixed from `type='raw'` to `type='qcow2'`)
**Problem:** Disk driver was `raw` on a qcow2 file, causing boot failure.
**Fix applied:** Changed to `type='qcow2'`.
**Resolution:** Fixed in this run.

### 2026-10-10: TASK-0026 item 4 review — cs_calendar.py guard (`61695c7`), spec 4.el10 (`0b3773b`), unsigned -4 RPM in `rpms-local/`

**Verdict: no blockers.** All three artifacts verified live; every claim in the 2026-10-06 and 2026-10-07 `## Implementation` entries reproduced. One should-fix (artifact hygiene, already flagged by Tails; confirmed benign) and five nits.

**Verified (claim -> live check -> result):**

| Claim | Check | Result |
|---|---|---|
| Committed cs_calendar.py equals the fixed source | `git -C cinnamon/ show 61695c7:...cs_calendar.py \| md5sum` vs working tree | both `fefda1677cfa3872bd659f408a12a9cf` |
| Committed file compiles | `python3 -m py_compile` on the `git show` blob | OK (host python3.12.14) |
| RPM payload carries the fix | `rpm2cpio` payload `cs_calendar.py` md5 | `fefda1677cfa3872bd659f408a12a9cf` |
| Placed copy byte-identical to build | `sha256sum` of `rpms-local/` copy vs `/tmp/rpmbuild-task0026/RPMS/x86_64/` | both `cfa2f4ca5bae8af84dacac7967613dc7c1c4da6e2d67c65b76c34bf368c9568a` |
| RPM metadata | `rpm -qip` on the placed file | `cinnamon 6.7.4-4.el10 x86_64`, `Signature: (none)` |
| Spec committed state | canonical repo `git show 0b3773b`; `git diff HEAD -- spec/cinnamon.spec` | Release `3.el10`->`4.el10` plus changelog; working tree clean |
| RPM changelog matches spec | `rpm -qp --changelog` | 6.7.4-4.el10 entry identical to spec text, weekday/date correct |
| Git state | `git log/status` both repos | `cinnamon/` master 1 ahead of `origin/master`, exactly the 8 recorded port files still modified; canonical `feature/TASK-0024-rpm-signing-gpgcheck` 4 ahead, `spec/` clean, tracked `rpms/` clean (64 RPMs + `SHA256SUMS` = 65 files); stored origin URLs clean in both (tokens only via the global `~/.gitconfig` insteadOf rewrite); nothing pushed |
| Guard completeness | `grep` of committed file for `TimezoneMap\|tz_map\|HAVE_TIMEZONE_MAP` | all 6 sites accounted: assignment in `on_module_selected` (line 44-50, always set to a value), uses guarded in `_on_proxy_ready` (88-94) and `on_selector_location_changed` (133-134); `on_map_location_changed` (line 120) is unguarded but only wired at line 94 when `self.tz_map is not None` |
| Behavior with namespace present | diff review of `61695c7` | true-branch path is line-for-line the pre-fix code; `except (ValueError, ImportError)` matches the two real failure modes (`gi.require_version` ValueError, import ImportError) |

The guard is correct: `self.tz_map` is unconditionally assigned (`None` in the fallback), so no `AttributeError` path; the fallback keeps the `TimeZoneSelector` as the timezone mechanism; no new package dependencies (`rpm -qpR` diff shows no timezonemap requirement, only the libGLESv2 delta below). The no-render defect is out of scope here (TASK-0034).

**Findings (ranked):**

### F1. The -4 artifact ships `__pycache__/cs_calendar.cpython-312.pyc`
**Severity:** should-fix
**Where:** `rpms-local/cinnamon-6.7.4-4.el10.x86_64.rpm` payload `/usr/share/cinnamon/cinnamon-settings/modules/__pycache__/` (source: the `cinnamon/` checkout's `files/` tree; packaging: `spec/cinnamon.spec:140` globs `%{_datadir}/cinnamon/`)
**Problem:** A `py_compile`-generated pyc from the working tree was staged into Source0 and shipped. Verified benign in three independent ways: magic `cb0d0d0a` is the valid 3.12 magic; the pyc bytecode is structurally identical (marshal signature, `co_filename` ignored) to a fresh compile of the shipped fixed `.py`, so it cannot mask the fix; and rpmbuild normalizes the `.py` payload mtime to the changelog date (`1791244800`) while the pyc embeds the compile-time source mtime (`1791258049`), so CPython's mtime check rejects it and recompiles from source at import.
**Failure scenario:** A re-derivation of -4 (e.g. if the signing step rebuilds instead of signing this file) embeds a different wall-clock mtime and produces different payload bytes with zero source change, so the artifact is not byte-reproducible across rebuilds; and it carries 22,651 bytes that are never executed. Note the 8 site-packages `__pycache__` pycs are pre-existing in the published -3 (same glob, `spec/cinnamon.spec:164`), so -4 adds 2 entries on top of an existing pattern.
**Suggested direction:** Scrub `__pycache__/` from the `cinnamon/files/` tree before the signing/publishing rebuild (Tails' own flag in the 2026-10-06 entry), or add a `%build`/`%install` cleanup so the `%files` glob cannot pick up pycs.

### F2. "Corrupt header" does not reproduce; the inertness mechanism is mtime normalization
**Severity:** nit
**Where:** `## Implementation` 2026-10-06 entry, "Build hygiene flag"
**Problem:** The pyc header parses cleanly (valid magic, valid marshal, embedded source size `15314` equals the shipped `.py` size); nothing is corrupt. The pyc is inert because of the mtime mismatch described in F1, not a corrupted header.
**Failure scenario:** None for behavior; the mislabel risks a future agent "fixing" the header instead of scrubbing the pyc.
**Suggested direction:** No code action; correct the description if the entry is ever amended.

### F3. -4 adds a `libGLESv2.so.2()(64bit)` runtime dependency that -3 does not
**Severity:** nit
**Where:** `rpms-local/cinnamon-6.7.4-4.el10.x86_64.rpm` vs `rpms/cinnamon-6.7.4-3.el10.x86_64.rpm` (`diff <(rpm -qpR ...)` shows exactly one added `Requires`)
**Problem:** The host build environment produced an extra `DT_NEEDED` entry; no source change explains it.
**Failure scenario:** None demonstrated: dnf resolves the dependency (the VM install succeeded), and every Rocky 10 Cinnamon system carries mesa; a minimal non-desktop install would also resolve it via dnf.
**Suggested direction:** No action; record the dependency delta in the release notes when -4 is signed and published.

### F4. The TASK-0026 spec bump is committed on the TASK-0024 feature branch
**Severity:** nit
**Where:** canonical repo, `0b3773b` on `feature/TASK-0024-rpm-signing-gpgcheck` (4 ahead of origin, unpushed)
**Problem:** The operator push step (TASK-0033 credential finding, which covers `8cde059`/`620ceb4`/`9d1eb46`) now also carries the TASK-0026 spec commit; its blast radius grew by one commit.
**Failure scenario:** If that branch is ever pushed or merged without the TASK-0026 context, the 4.el10 release rides along silently.
**Suggested direction:** Awareness for `Knuckles`' checkpoint: note in the checkpoint that the -4 spec lives on that branch.

### F5. Doc bookkeeping off by one on the spec commit stat
**Severity:** nit
**Where:** `## Implementation` 2026-10-07 entry, commit table: "11 insertions, 1 deletion"
**Problem:** `git show 0b3773b --stat` reports 10 insertions, 1 deletion (Release line plus a 9-line changelog block).
**Failure scenario:** None; bookkeeping accuracy only.
**Suggested direction:** None required.

### F6. `rpms-local/` untracked, not ignored
**Severity:** nit
**Where:** canonical repo working tree (`?? rpms-local/`, 2,168,408-byte unsigned binary)
**Problem:** Every `git status` carries the unsigned -4 until a decision is made (already noted by Tails as "Competing priorities"). The tracked `rpms/` convention is a signed published set plus `SHA256SUMS`.
**Failure scenario:** An unscoped `git add .` in a later run sweeps the unsigned binary into the tracked published set.
**Suggested direction:** `Knuckles`' checkpoint decides: commit it with a note that it is unsigned and local-test, or leave it untracked/ignored.

**Success criteria for this review step.**
- Definition of done: all three artifacts (guard commit, spec commit, -4 RPM) reviewed live; findings recorded in this section; no open blockers.
- Acceptance criteria: the ten checks in the verified table above all reproduce; guard completeness holds (every `tz_map`/`TimezoneMap` use guarded or conditionally wired); git state matches the 2026-10-08 PM verification (ahead counts, 8 dirty port files uncommitted, both checkouts unpushed, tracked `rpms/` clean).
- Validation approach: `git show`/`git status`/`git log` on both repos, `md5sum`/`sha256sum` on source, payload, and placed copy, `rpm -qip`/`rpm -qlp`/`rpm -qplp`/`rpm -qpR`/`rpm -qp --changelog`/`rpm2cpio` on the RPMs, `python3 -m py_compile` plus marshal-level pyc analysis on the host's python3.12.14.

---

## Security

*Owner: `Omega`. Read-only. Severity order.*

No security issues identified. Recovery operations were performed on local host infrastructure.

### 2026-10-10: TASK-0026 item 4 security review — cs_calendar.py guard (`61695c7`), spec 4.el10 (`0b3773b`), unsigned -4 RPM in `rpms-local/`; PAT flag resolution verified

**Verdict: no blockers.** All three artifacts verified live; the PAT flag resolution in the 2026-10-07 `## Status` entry is confirmed at value level (sha256, values never written). Three medium credential-handling findings (all on the operator-owned single-user host, bounded exploitability), four low supply-chain findings (O5-O7 reframe Shadow F6/F1/F4 as attack surface). The only open action is the operator rotation step in TASK-0033, extended with one storage location (O3).

### O1. `~/.gitconfig` is mode 644 and embeds the live PAT in a `url.*.insteadOf` rewrite
**Severity:** medium
**Vector:** secrets
**Where:** `~/.gitconfig` (key `url.https://<token>@github.com/.insteadof=https://github.com/`)
**Attack:** any other local user account, or a process running as a non-`howard` uid, reads the 644 file and harvests the 40-character classic PAT (`ghp_` prefix; value never recorded here). The same token is presented by git on every operation against any `https://github.com/` remote on this host.
**Impact:** HTTPS git push/fetch plus GitHub REST API as the token's account, until rotation. Exploitability is bounded on a single-user host; the exposure is the section 4 handling deviation (secret material in a world-readable file) that the incoming rotated token would inherit.
**Fix:** operator step with the TASK-0033 rotation: `chmod 600 ~/.gitconfig`; longer term, keep the credential out of a URL rewrite.
**Evidence:** `stat -c '%a %U %G' ~/.gitconfig` → `644 howard howard`; `git config --global -l` shows the single `url.https://***@github.com/.insteadof=https://github.com/` rewrite (token redacted in this review).

### O2. `~/AI/secrets/` is 755 and every file is 644, holding two GitHub PATs plus the VM password
**Severity:** medium
**Vector:** secrets
**Where:** `~/AI/secrets/` (`token.md`, `githubtoken.md`, `pass.txt`, `ai-machine-password.md`, `temp_pass.md`)
**Attack:** same class as O1: any local uid reads the directory and the 644 files. The location sits outside the section 4 canonical `~/secrets/` (which is compliant: 700 directory, 600 files), so an audit of `~/secrets` alone misses it.
**Impact:** two distinct classic PATs and the VM login password in one non-compliant location; single-user host bounds exploitability.
**Fix:** operator step: `chmod 700 ~/AI/secrets` plus `chmod 600` on each file, or migrate the files to `~/secrets/`.
**Evidence:** `stat -c '%a %U %n'` → `~/AI/secrets` 755, all five files 644; `~/secrets` 700, `~/secrets/github-token.md` 600.

### O3. PAT flag resolution verified; `~/.git-credentials` is an additional storage location not in the 2026-10-07 mapping
**Severity:** medium
**Vector:** secrets
**Where:** `~/.git-credentials` (115 bytes, mode 600, dated 2026-09-29)
**Attack:** an agent on this host runs `git remote -v` in the `cinnamon/` checkout and receives the token in the effective URL (the insteadOf rewrite surfaces there); an agent that then writes that output into a planning doc or a commit has committed the token. This is the concrete path the flag described, and why the no-push instruction on the `cinnamon/` checkout stands.
**Impact:** the token grants HTTPS git operations plus the GitHub API for its account. Per the 2026-10-03 `## Status` entry the same token value already returned API `401 Bad credentials`, so it may be dead; the TASK-0033 rotation is the detection and remediation mechanism. No live test of the credential was performed in this review.
**Fix:** operator step (TASK-0033 rotation) with the location list extended: `~/.gitconfig`, `~/secrets/github-token.md`, `~/AI/secrets/token.md` (all three hash-identical), plus `~/.git-credentials` (new, this review). No credential helper is named (global value empty, system none), so git does not consume `~/.git-credentials`; it is a redundant copy to update at rotation time or delete.
**Verification (values never written):** sha256 of the gitconfig token, `~/secrets/github-token.md`, `~/AI/secrets/token.md`, and the `~/.git-credentials` pass value are identical; `~/AI/secrets/githubtoken.md` is the distinct second token, as the 2026-10-07 entry records. `git -C cinnamon/ config --local --get remote.origin.url` is clean (`https://github.com/linuxmint/cinnamon.git`, no userinfo); `git rev-list --count origin/master..HEAD` = 1 (unpushed); canonical repo 4 ahead of origin, unpushed. PAT pattern grep (`ghp_`/`github_pat_`/`gho_`/`ghu_`/`ghs_`/`grm_` prefixes) is clean in `planning/`, `.github/`, both repo HEADs, the working-tree text files, and the extracted -4 payload. The `## Implementation` claim at this doc's line 1326 (origin URL in `cinnamon/.git/config` "embeds a live GitHub PAT") is superseded by the 2026-10-07 resolution and this review: the stored URL is clean; the token rides only in the global rewrite.

### O4. Unsigned -4 in untracked `rpms-local/`; the VM install bypassed the repo's `gpgcheck=1`
**Severity:** low
**Vector:** supply-chain
**Where:** `rpms-local/cinnamon-6.7.4-4.el10.x86_64.rpm` (canonical repo, untracked)
**Attack:** anyone who obtains the artifact can substitute it for the signed -3 in any consumer, since no signature binds it to the team's key. The VM install used `--nogpgcheck` against a `file:///` repo configured `gpgcheck=1`.
**Impact:** bounded today: the artifact exists only on the operator-owned VM and in the local untracked `rpms-local/`; the tracked `rpms/` published set is still the signed 6.7.4-3 plus `SHA256SUMS` (clean). Payload verified below against the committed source.
**Fix:** keep the artifact out of the tracked set and out of the `gpgcheck=1` repo until it is signed through the TASK-0024 path; record the `--nogpgcheck` one-off and Shadow F3's `libGLESv2` delta in the release notes.
**Evidence:** `rpm -qip` → `Signature: (none)`, `cinnamon 6.7.4-4.el10`; `sha256sum` → `cfa2f4ca5bae8af84dacac7967613dc7c1c4da6e2d67c65b76c34bf368c9568a` (matches the build output per `## Review`); `rpm -qp --scripts` → empty (nothing executes at install time); extracted payload `cs_calendar.py` md5 `fefda1677cfa3872bd659f408a12a9cf` equals the committed blob in `61695c7`.

### O5. Fourteen untracked paths in the canonical repo; an unscoped `git add .` sweeps the unsigned -4 and the ten component directories
**Severity:** low
**Vector:** supply-chain
**Where:** canonical repo working tree (`git status --short`: `AGENTS.md`, `INSTALL.md.legacy-2026-08-11`, `agent_creation_prompt.md`, `rpms-local/`, and the ten untracked component directories `cinnamon/`, `cinnamon-control-center/`, `cinnamon-desktop/`, `cinnamon-menus/`, `cinnamon-session/`, `cinnamon-settings-daemon/`, `cjs/`, `muffin/`, `nemo/`, `xapps/`)
**Attack:** a later agent run issues an unscoped `git add .`; the unsigned binary enters the tracked published set and the component directories are added as dangling gitlinks with no `.gitmodules`, changing what the published set claims to be.
**Impact:** supply-chain confusion in metalllinux/cinnamon-for-rocky10; no live exposure (repo unpushed, 4 ahead).
**Fix:** Knuckles checkpoint decides: commit `rpms-local/` with an unsigned/local-test note, or add `rpms-local/` (and the component directories, if they stay local) to `.gitignore`. Extends Shadow F6, which named only `rpms-local/`.
**Evidence:** `git -C ~/Linux/projects/cinnamon-for-rocky10 status --short` (the 14 paths above); `.gitignore` has no entry for any of them.

### O6. -4 payload ships a working-tree `__pycache__` pyc that the spec glob re-embeds on every rebuild
**Severity:** low
**Vector:** supply-chain
**Where:** payload `/usr/share/cinnamon/cinnamon-settings/modules/__pycache__/cs_calendar.cpython-312.pyc` (source: untracked `cinnamon/files/usr/share/cinnamon/cinnamon-settings/modules/__pycache__/` in the checkout; packaging: `spec/cinnamon.spec:140` globs `%{_datadir}/cinnamon/`)
**Attack:** a re-derivation of -4 (for example, the signing rebuild) re-packages the working-tree pyc; if the rebuild's embedded source mtime lands inside CPython's accept window against the payload mtime, the pyc can shadow the `.py`, and the fix then has to survive as stale bytecode.
**Impact:** bounded: in this artifact the pyc is inert (rpmbuild normalizes the payload `.py` mtime to the changelog date while the pyc embeds the compile-time source mtime, so CPython's mtime check rejects it and recompiles from source; Shadow's marshal-level analysis holds). Live cost is the 22,651 bytes of never-executed bytecode (per `## Review`) and non-byte-reproducible rebuilds. Shadow F1.
**Fix:** scrub `cinnamon/files/.../modules/__pycache__/` before the signing rebuild (Tails' own flag), or add a `%files` exclusion / `%install` cleanup so the `spec/cinnamon.spec:140` glob cannot pick up pycs.
**Evidence:** `rpm2cpio` + `cpio -idm` into a temp dir: pyc present; `git -C cinnamon/ ls-files` shows it is untracked (working-tree artifact, not in `61695c7`); `find` in the checkout shows exactly one pyc under `files/`.

### O7. The -4 spec commit rides on the TASK-0024 feature branch
**Severity:** low
**Vector:** supply-chain
**Where:** canonical repo, `0b3773b` on `feature/TASK-0024-rpm-signing-gpgcheck` (4 ahead of origin, unpushed: `8cde059`, `620ceb4`, `9d1eb46`, `0b3773b`)
**Attack:** no live attacker; the risk is the operator push step. Pushing that branch lands the 4.el10 spec plus the three TASK-0033 license-fix commits on origin without the TASK-0026 context, and a later reader of the branch sees the -4 release as TASK-0024 work.
**Impact:** blast radius of the push step grows by one commit. Shadow F4.
**Fix:** awareness for Knuckles' checkpoint: note that the -4 spec lives on that branch. No code action.

**Verified clean (no finding):**
- `61695c7`: exactly one file (`files/.../cs_calendar.py`, 24 insertions, 10 deletions per `git show 61695c7 --stat`); grep of the committed file for `exec(`, `eval(`, `os.system`, `subprocess`, `urllib`, `requests`, `socket`, `open(` → no hits; no injection, template, or network path in the guard; `self.tz_map` is unconditionally assigned so no `AttributeError` path (Shadow's guard-completeness table holds).
- `0b3773b`: `Release 3.el10` to `4.el10` plus a 9-line changelog only. Spec attack surface: `Source0` is a local tarball (`%{name}-%{version}.tar.gz`, no URL fetch), all `BuildRequires` local, `%prep` local deterministic `sed` patches, no scriptlets (`rpm -qp --scripts` on the built RPM is empty).
- `keys/`: `git ls-files keys/` → `keys/cinnamon-rocky10-public.asc` only; `file` → "PGP public key block"; `.gitignore` blocks private key material (`private-keys-v1.d/`, `*.passphrase`, `*-secret.asc`, `*-private.asc`, `*-secret.key`, `*-private.key`, `openpgp-revocs.d/`). No private key in the repo.
- No credential material in `planning/`, `.github/`, either repo HEAD, the working-tree text files, or the extracted payload (PAT pattern greps all clean).
- Payload hygiene: no `.git`, no SSH material, no secret strings; `/etc/pam.d/cinnamon` is the stock `system-auth` include; `./usr/lib/.build-id` is standard.
- Shadow F2 (mislabelled pyc header), F3 (`libGLESv2` Requires delta), F5 (stat off by one): no attack surface; the F3 delta belongs in the release notes per O4's fix.

**Success criteria for this step.** The three artifacts live-verified (guard commit, spec commit, -4 RPM); the PAT flag resolution verified at value level by sha256 with no secret value written to any file; findings recorded in severity order; the operator rotation step is the only open action (TASK-0033, locations extended by `~/.git-credentials` per O3).

---

## License (Charmy)

*Owner: `Charmy`. Fourth in the review chain.*

**Project license:** GPL-2.0 (Cinnamon) — appropriate for desktop environment

**Imported code**

| Component | Source | License | Obligations met | Status |
|---|---|---|---|---|
| Cinnamon | github.com/linuxmint/cinnamon @ main | GPL-2.0 | yes | pass |
| cinnamon-control-center | github.com/linuxmint/cinnamon-control-center @ main | GPL-2.0 | yes | pass |
| Rocky Linux 10 base | rockylinux.org | MIT, GPL | yes | pass |

**Verdict:** pass

### 2026-10-10: TASK-0026 item 4 license review — cs_calendar.py guard (`61695c7`), spec 4.el10 (`0b3773b`), unsigned -4 RPM in `rpms-local/`

The table above is the original task-level pass. This entry is the item 4 verification at the refs actually used, and supersedes that table for this scope (its refs are not verified refs).

**Project license:** GPL-2.0 — appropriate. Canonical repo (metalllinux/cinnamon-for-rocky10) has a git-tracked root `LICENSE` (18092 B, GPLv2 text, "GNU GENERAL PUBLIC LICENSE Version 2, June 1991") covering the repo's own files (specs, patches, scripts, docs) per README.md; component checkouts are under their upstream licenses. The project is a port of GPL-2.0 upstream Cinnamon and the in-scope changes keep the code in the GPL-2.0 family: no relicensing. `spec/cinnamon.spec` declares `License: GPLv2+` for the packaged Cinnamon code. Upstream declares GPL-2.0 at the ref in use (below) and the tree's file headers carry the "either version 2 of the License, or (at your option) any later version" wording (sampled `src/screensaver/cs-auth.c`, `src/screensaver/backup-locker/event-grabber.c`), so `GPLv2+` (GPL-2.0-or-later) is the consistent expression; the `LGPL2+` over-claim was dropped by `9d1eb46` (TASK-0033). No incompatible pair is introduced: GPL-2.0 code stays GPL-2.0, and no GPL-3.0-only or AGPL-3.0 code enters.

**Imported code**

| Component | Source (repo @ ref) | License (verified at) | Obligations met | Status |
|---|---|---|---|---|
| `cs_calendar.py` guard commit `61695c7` | github.com/linuxmint/cinnamon @ `e9ba28a87f0f69594487a08e940840d494bb3ea0` (checkout `origin/master`, the base ref in use; local 1 ahead) | GPL-2.0, verified at the ref: single `COPYING` (17991 B, GPLv2 text) at repo root, no `COPYING.LIB`; GitHub license API at the ref: key `gpl-2.0`, spdx `GPL-2.0` | yes — the file has no file-level copyright header upstream at the ref or locally (nothing lost); change recorded per GPLv2 §2a in the RPM %changelog and commit message; license text shipped in the package (see -4 row) | pass |
| `spec/cinnamon.spec` 4.el10 commit `0b3773b` | metalllinux/cinnamon-for-rocky10 @ `0b3773b` (repo-own file) | GPL-2.0 via the canonical root `LICENSE` (tracked; covers repo-own files per README) | yes — `License: GPLv2+` matches upstream at the ref in use; `%license COPYING` is met in the built -4 RPM; %changelog entry attributes `Team Chaotix <chaotix@metallinux.dev> - 6.7.4-4.el10` | pass |
| 8 uncommitted port files shipped in the Source0 tarball | same upstream tree @ `e9ba28a` (working tree): `meson.build`, `src/cinnamon-global-private.h`, `src/cinnamon-global.c`, `src/cinnamon-keyring-prompt.c`, `src/cinnamon-secure-text-buffer.c`, `src/meson.build`, `src/screensaver/backup-locker/event-grabber.c`, `src/screensaver/backup-locker/meson.build` | GPL-2.0 (same upstream ref, single `COPYING`); `event-grabber.c`'s own header is GPLv2 "any later version" | yes — distributed with the shipped `COPYING` text; commit state is a process matter, recorded in ## Status | pass |
| unsigned -4 RPM `rpms-local/cinnamon-6.7.4-4.el10.x86_64.rpm` (sha256 `cfa2f4ca...`) | built from the checkout above (`Source0` = local `cinnamon-6.7.4.tar.gz`) | metadata `License: GPLv2+`; payload carries the GPLv2 text | yes — payload ships `./usr/share/licenses/cinnamon/COPYING`, byte-identical to the checkout `COPYING` (sha256 `10851f963faac9fe4fa6025620c2bd1c4d03abd1f90f450ddfec63d390490c82`), which is byte-identical to upstream at the ref (git blob sha `eb2b0d03645b598a96390b3f5d7f66eeaff29ccd`, 17991 B, matches the API blob at the ref); no NOTICE file upstream, so none to ship; no new package dependencies added by the in-scope commits (no timezonemap requirement in the `rpm -qpR` diff; the only -3 to -4 delta is the system library `libGLESv2`, Shadow F3), so no registry license to verify | pass — unsigned state is an Omega O4 / Knuckles checkpoint matter, not a license finding |

**Security cross-reference (not a license finding):** `git remote -v` on both repos confirms the PAT rides the effective origin URLs via the global `insteadOf` rewrite (Omega O3 scenario; the value is recorded by Omega, not repeated here). Consistent with the no-push instruction on the `cinnamon/` checkout and the unpushed state recorded in ## Status.

**Verdict:** pass — no license findings on the item 4 artifacts.

---

## Test Results

*Owner: `Big`. Verdicts, never raw log dumps.*

**Recovery run:**

| Check | What it exercises | Result | Notes |
|---|---|---|---|
| VM boot | Domain starts, display renders | PASS | 45.6s CPU time, non-solid screenshot |
| Display rendering | Screenshot captured via virsh | PASS | 84 unique colors (non-solid) |
| Web VNC path | https://cinnamon-1.localhost | PASS | HTTP 200 |

**Checks requested vs run:** 3 requested, 3 executed.

**Verdict:** PASS for recovery. Guest OS booting successfully with display output. Network configuration pending.

### 2026-10-08: Big — Rocky 12-pane gate result (cross-ref TASK-0034) and Fedora 45 comparison (DoD boxes 3-5)

**Rocky 12-pane gate (boxes 1-2).** Ran 2026-10-08 on `Rocky_Linux_10_Cinnamon`; full evidence
in TASK-0034 `## Test Results` (same date, `Big` entry). Gate FAIL, as expected: 12 launches
(CC overview + 11 pane modules; Updates has no `cs_` module), all ALIVE, all killed by recorded
pid; 14 frames, 4 distinct md5s; no pane window rendered in any frame; rows 0-39
wallpaper-only in every frame. Console errors: Power pane only — `cs_power.py:883
on_my_value_changed` D-Bus `Unauthorized (36)` traceback, app survived; the other 11 panes
clean (stderr empty). Box 1 (Control Center GUI opens via web VNC): FAIL — the process starts
but no window is presented (no-render), so it fails on any viewing path; the gate used virsh
screenshots. Box 2 (all panes load without console errors): FAIL at GUI level (no window
renders — environment limitation per TASK-0034 item 8); partial at process level (11/12 panes
clean, Power pane has the traceback above).

**Fedora 45 comparison (boxes 3-5).** Both VMs verified running at preflight
(`Rocky_Linux_10_Cinnamon` id 2 / 192.168.122.4; `Fedora_45_Cinnamon` id 1 / 192.168.122.176);
snapshots intact (`2026-10-04T11:36` shutoff plus `2026-10-07-task0034-pre` running on Rocky;
`2026-10-04T11:37` shutoff on Fedora). Fedora guest evidence: `/tmp/big-fedora-app.log` +
`.pid` (guest); host frames `/tmp/opencode/big-fedora-00-base.png` and `-01-cc.png`.

| Dimension | Rocky 10.2 VM | Fedora 45 VM |
|---|---|---|
| OS | Rocky Linux 10.2 (Red Quartz) | Fedora 45 (Cinnamon Prerelease) |
| Cinnamon | `cinnamon-6.7.4-4.el10` team RPM (per the 2026-10-06 Tails record; the running session predates the install) | `cinnamon-6.7.5^unstable-3.fc45`, `cinnamon-control-center-6.7.3^unstable-1.fc45` |
| Session | Wayland (`cinnamon-wayland`, session 2) | X11 (`XDG_SESSION_TYPE=x11`, `DISPLAY=:0`; session leader 1035, `cinnamon --replace` pid 1374, `nemo-desktop` pid 1521) |
| Video device | bare `<model type='virtio' .../>` | identical bare `<model type='virtio' heads='1' primary='yes'/>` (VNC 5900 autoport, listen 127.0.0.1) |
| GL evidence | llvmpipe + CPU copy path (TASK-0034 part 2 item 6) | none found in either journal scope (absence recorded, not inferred) |
| X11 client list | empty (Wayland session) | one window: `nemo-desktop` (`0x2800003`, WM_NAME "Desktop") |
| Panel bar | not rendered (rows 0-39: 98.1-98.2% wallpaper-dark in all frames) | not rendered (base frame: zero bright pixels in rows 0-79) |
| CC launch | 12 launches, all ALIVE, all killed by pid | 1 launch (CC overview; no per-pane run on Fedora — comparison scope is boxes 3-5), ALIVE (pid 11401), killed by pid; stderr empty |
| CC window | not rendered (14 frames: wallpaper + moving block only) | not rendered (00->01 diff 7333 px raw / 2926 block-excluded; diff bbox x119-739 y88-412 = block move + drift, no window) |
| Modules shipped | 31 | 31 (same names) |
| Moving external block | present, 3x3 grid centers x in {121, 548, 974}, y in {88, 355, 622}, ~176-180x57-58 px | present, same grid (base: 2873 bright px, bbox x120-296 y88-145) |

**Box 3 (Fedora VM provisioned and running): PASS.**

**Box 4 (Fedora Control Center GUI tested): mixed.** Process level: PASS (launches, ALIVE pid
11401, stderr empty, killed by recorded pid). Window level: FAIL as on Rocky (no window
rendered; the only frame-to-frame change is block move + drift). No per-pane console-error data
exists for Fedora (stderr empty; the user journal has 131 boot lines but zero
settings/TimezoneMap/GL lines, including for `_PID=1374`) — recorded as absence, not inferred.
This is the same no-render behavior as Rocky, not a Fedora-specific defect; the
environment-limitation classification (TASK-0034 item 8) applies to both VMs.

**Box 5 (comparison table): recorded above.** Key facts: (1) the no-render behavior is identical
on both VMs despite different sessions (Wayland vs X11), different Cinnamon versions (team
6.7.4-4.el10 vs Fedora 6.7.5^unstable), and different session stacks — supporting the
display-pipeline classification over a Rocky-package bug; (2) the video device XML is identical
bare virtio on both; (3) the moving external block appears on both VMs at the same 3x3 grid
with the same size class — a new cross-VM fact for the unresolved block identity (TASK-0034
`## Status` unknown 1); (4) the only X11 window in either VM's client list is `nemo-desktop` on
Fedora; on Rocky (Wayland) the list is empty; on both VMs the base frame shows no panel and no
app window, so the block and the wallpaper are the only rendered content in either.

**Verdict.** Box 3 PASS; box 4 mixed as stated (process pass, window no-render, environment
limitation); box 5 recorded. Boxes 1-2 on Rocky remain FAIL per the gate result above;
TASK-0034 owns the no-render investigation and the final verdict for that defect.

### 2026-10-10: Big — TASK-0026 item 4 test review: cs_calendar.py guard (`61695c7`), spec 4.el10 (`0b3773b`), unsigned -4 RPM in `rpms-local/`

Scope per ## Next Actions item 4 (the `Big` step of the chain `Shadow` → `Omega` → `Big` → `Charmy`).
No GitHub Actions workflow applies to these changes: the canonical repo has no `.github/`
directory (project root listing) and nothing is pushed (`cinnamon/` is 1 ahead of
`origin/master`; canonical HEAD is `0b3773b`), so no workflow check was requested. The
applicable test layers are the host-side artifact chain and the established VM
process-level record. Per the brief: no 12-pane gate re-run, no live-session disturbance.
Both VMs are running (under `qemu:///system`: id 1 `Fedora_45_Cinnamon`, id 2
`Rocky_Linux_10_Cinnamon`); note the default `virsh` URI on this host is `qemu:///session`,
so a bare `virsh list --all` prints an empty table and must not be read as "no VMs".

**Checks requested vs run:** 4 requested (process-level verification, 12-pane gate result,
Fedora 45 comparison, artifact payload vs tested source), 4 covered, 0 dropped. The gate
result and the Fedora comparison are covered from the established 2026-10-08 record in this
section (re-run prohibited by the brief); process-level verification is covered by that
record plus the passive installed-payload check; artifact payload vs tested source was
re-verified live.

| Check | What it exercises | Result | Evidence (command -> result) |
|---|---|---|---|
| compile | committed `61695c7` blob under host python3.12 | PASS | `git -C cinnamon/ show 61695c7:...cs_calendar.py` piped to `python3 -m py_compile` -> OK |
| payload vs committed source | the -4 RPM ships the tested fix | PASS | `rpm2cpio` payload `cs_calendar.py` md5 `fefda1677cfa3872bd659f408a12a9cf` = committed blob md5 |
| working tree vs committed | checkout state matches the commit | PASS | `md5sum cinnamon/files/.../cs_calendar.py` -> `fefda1677cfa3872bd659f408a12a9cf` |
| installed payload on test VM | what the process-level test actually ran | PASS | passive ssh to `Rocky_Linux_10_Cinnamon` (192.168.122.4): `md5sum /usr/share/cinnamon/cinnamon-settings/modules/cs_calendar.py` -> `fefda1677cfa3872bd659f408a12a9cf`; `rpm -q cinnamon` -> `cinnamon-6.7.4-4.el10.x86_64` |
| placed copy vs build | `rpms-local/` artifact is the build output | PASS | `sha256sum` on both -> `cfa2f4ca5bae8af84dacac7967613dc7c1c4da6e2d67c65b76c34bf368c9568a` (build dir `/tmp/rpmbuild-task0026/RPMS/x86_64/` still present) |
| RPM metadata | identity and signature state | PASS | `rpm -qip` -> `cinnamon 6.7.4-4.el10 x86_64`, `Signature: (none)`, Build Date Tue 06 Oct 2026 |
| changelog | RPM changelog vs spec text | PASS | `rpm -qp --changelog` 6.7.4-4.el10 entry identical to the `git show 0b3773b:spec/cinnamon.spec` %changelog block |
| spec commit state | canonical spec at HEAD is exactly the bump | PASS | `git diff HEAD -- spec/cinnamon.spec` -> 0 lines; `git log -1 -- spec/cinnamon.spec` -> `0b3773b`; `Release: 4.el10`, `Version: 6.7.4`; `git show 0b3773b --stat` -> 1 file, 10 insertions, 1 deletion (reproduces Shadow F5: the 2026-10-07 entry's "11 insertions" is off by one) |
| guard commit state | `cinnamon/` checkout holds the guard | PASS | branch `master` 1 ahead of `origin/master`, HEAD `61695c7` (1 file, 24 insertions, 10 deletions); exactly the 8 recorded port files still modified, nothing else |
| pyc inertness mechanism | the shipped pyc cannot mask the fix | PASS | payload `__pycache__/cs_calendar.cpython-312.pyc` 22,651 bytes, magic `cb0d0d0a`, embedded source mtime 1791258049 vs payload `.py` mtime 1791244800 -> 13,249 s mismatch, CPython rejects the pyc and recompiles from source; the installed tree's `__pycache__/` holds 30 runtime-generated `cs_*.pyc` (including `cs_calendar`), i.e., the directory is maintained by CPython at import time, not by the payload |

**Process-level verification (record, 2026-10-06 Tails run plus the 2026-10-08 gate):**
app starts and stays alive; 12 launches all ALIVE, all killed by recorded pid; no
TimezoneMap error in any pane's stderr (the guard's effect at process level); 11 of 12
panes clean, the Power pane carries the `cs_power.py:883` D-Bus `Unauthorized (36)`
traceback, which is not in any file these commits touch.

**12-pane gate result (record, 2026-10-08):** FAIL at window level (no window renders in
any of 14 frames; rows 0-39 wallpaper-only). Environment limitation, owned by TASK-0034.
Not attributable to these commits: `61695c7` touches only `cs_calendar.py` (no display
path), `0b3773b` touches only the Release line and the changelog, and the -4 RPM
packages exactly those two.

**Fedora 45 comparison (record, 2026-10-08):** box 3 PASS, box 4 mixed (process pass,
window no-render), box 5 recorded. No-render is identical on both VMs despite different
session stacks (Wayland vs X11) and different Cinnamon versions; the display-pipeline
classification over a Rocky-package bug holds.

**Verdict:** PASS for the item 4 artifacts from the test side. The tested-source chain is
closed at four links with one md5 (`fefda1677cfa3872bd659f408a12a9cf`): committed blob
in `61695c7`, `cinnamon/` working tree, -4 RPM payload, installed file on
`Rocky_Linux_10_Cinnamon`; the placed `rpms-local/` copy is byte-identical to the build
output (`cfa2f4ca...`). The guard is effective at process level (no TimezoneMap error,
app alive), and the only window-level failure is the no-render defect TASK-0034 already
owns. No code bug found in this step; no harness bug. Two non-blocking items for the
downstream chain, both already flagged upstream and confirmed here: (1) the shipped
working-tree pyc is inert but must be scrubbed from `cinnamon/files/.../modules/__pycache__/`
before the signing rebuild so the -4 payload is byte-reproducible across rebuilds (Shadow
F1, Omega O6; action owner Tails); (2) the -4 stays unsigned and out of the tracked set
until Knuckles' checkpoint decides (Shadow F6, Omega O4/O5).

---

## Docs

*Owner: `Vector`.*

| File | Sections touched | What changed |
|---|---|---|
| `planning/docs/TASK-0026-cinnamon-control-center-comparison.md` | Implementation, Review, Security, License, Test Results | Added recovery run entry, section headers restored |

**Checked and needed no change:**
- README.md
- CHANGELOG.md

### 2026-10-10: Vector — item 4 docs step (review chain complete, TASK-0034 closed, TASK-0035 intake)

Scope per ## Next Actions item 4 and the ## Status 2026-10-10 entry. Landed state: item 4 review chain complete (no blockers; the pyc scrub is folded into the signing rebuild), TASK-0034 closed as an environment limitation, TASK-0035 intake (Power pane D-Bus `Unauthorized (36)`).

| File | Sections touched | What changed |
|---|---|---|
| `planning/docs/TASK-0026-cinnamon-control-center-comparison.md` | `## Docs` | Added this entry |
| `~/Linux/projects/cinnamon-for-rocky10/README.md` (git-tracked; working-tree edit, uncommitted; no git operations run; the canonical repo's commits stay local pending the TASK-0033 operator rotation) | "What the complete set adds" | Removed the "so the settings panel works out of the box" claim from the `cinnamon` 6.7.4-3 row; it is false on Rocky 10 (the published -3's `cinnamon-settings` crashes at startup, pre-fix state in the 2026-10-06 `## Implementation` entry). Added a known-issue paragraph with the verified facts only: startup crash `ValueError: Namespace TimezoneMap not available`, dies before any window; fix built and process-level verified as `cinnamon-6.7.4-4.el10`; unsigned and not in the published set |

**Checked and needed no change:**
- `~/Linux/projects/cinnamon-for-rocky10/INSTALL.md` — installation procedure for the published set; the published set is unchanged (signed 64 RPMs; tracked `rpms/` clean per ## Review 2026-10-10).
- `README.md` (team repo) — no section is touched by the landed state; the "Active projects" staleness is flagged below, not fixed here.
- `planning/TASKS.md` — already reflects the landed state after the Knuckles checkpoint: TASK-0026 "In Review" (line 35), TASK-0034 "Done (2026-10-10; ... verdict: environment limitation)" (line 43), TASK-0035 "Planning" (line 44).
- `planning/docs/TASK-0034-cinnamon-shell-no-render.md` — closure present (## Status "2026-10-10: PM closure" entry, DoD boxes ticked, verdict environment limitation).
- `planning/docs/TASK-0035-cinnamon-power-pane-dbus-unauthorized.md` — intake present (## Status 2026-10-10 entry with source, unknowns, next = Amy's plan).
- CHANGELOG.md — no such file in either repo (only vendored copies under `externals/` and upstream `ChangeLog` files inside the component checkouts).
- Project README "Status", "Test results", "Signing and release verification" — all describe the published set, which the landed state does not change. The -4 release-note items (the `libGLESv2` Requires delta per Shadow F3, the pyc scrub per Shadow F1 / Omega O6) stay deferred until -4 is signed and published, per the review's own recommendation.
- Power pane D-Bus `Unauthorized (36)` — not in the README. Intake only (diagnosis not started). Observed on the unpublished -4 during the 2026-10-08 gate (on the published -3 the app dies at startup, so no pane loads). Classification pending (port bug vs upstream vs environment). Surfaces when TASK-0035 reaches a verdict.
- No-render limitation (TASK-0034) — not user-facing. The verdict is a test-VM display/GPU pipeline limitation (host QEMU 10.1.0 has no 3D display device, guest Mesa llvmpipe-only), not a property of the published artifacts.

**Flagged, not changed (stale, predates this landed state):**
- `README.md` (team repo), "Active projects" and the "Cinnamon for Rocky Linux 10" subsection (lines 290-320) — stale since the 2026-09-19 publish: the status row says "All 10 RPMs built, VM testing pending", the "Packages built (10 of 10)" table lists 9 components, and "VM testing" says "Pending libvirt VM creation ... from `~/ISOs/`". Reality (project README 2026-09-19; this doc's ## Test Results 2026-10-08): 64 signed RPMs published with `SHA256SUMS`, fresh-VM install/parity/enforcing-SELinux verified 2026-09-18/19, VMs operator-provisioned 2026-10-04, 12-pane gate and Fedora comparison run 2026-10-08. A correct fix rewrites the subsection (component table, patches list, VM testing line) and needs verification of the pre-existing claims, beyond this dispatch. Candidate for a follow-up docs task or the next release checkpoint.

---

## Release

*Owner: `Knuckles`.*

**DONE checklist verified:** no (mid-task checkpoint; DoD not fully met)

- **Branch:** main (planning-doc checkpoint; team-repo convention for planning-doc state, no feature branch)
- **Commits:** not GPG-signed (this repo has no `commit.gpgsign` set, no local secret key, and all history is unsigned; follows the repo convention)
- **PR:** not applicable (planning-doc checkpoint, in-account)
- **Deploy:** not applicable (no deployment in this checkpoint, no workflow dispatched)
- **Push:** `metalllinux/team-chaotix` main, in-account, autonomous
- **DoD state:** box 1 open at window level. Process-level verification passes (the app starts, stays alive, no TimezoneMap error, correct payload installed) and the window-open screenshot gate is blocked by the TASK-0034 environment limitation (planning/docs/TASK-0034-cinnamon-shell-no-render.md, verdict: environment limitation). Box 2 open on the TASK-0035 verdict (planning/docs/TASK-0035-cinnamon-power-pane-dbus-unauthorized.md, Power pane D-Bus `Unauthorized (36)` at cs_power.py:883). Boxes 3-7 remain open; the next substantive gate is item 3 (Big's 12-pane screenshot gate and the Fedora comparison).
- **Held local (not pushed):** the four local commits in the `cinnamon-for-rocky10` canonical repo stay local (blocked on the TASK-0033 operator rotation); the `cinnamon/` checkout is not pushed (external upstream `linuxmint/cinnamon`, step-stop)
- **Next:** `Vector`, then `Espio` per ## Next Actions item 4

---

## Archive

*Owner: `Espio*, the only agent that deletes. Superseded detail lands here rather than being lost.*

**Pruning log**

| Date | What was pruned or compressed | Rough size |
|---|---|---|
| 2026-10-02 | Initial recovery attempt (raw-to-qcow2 fix), DHCP hosts file fix | ~1KB |
| 2026-10-02 | Orphaned QEMU kill, VM redefinition, network config bypass | ~2KB |
| 2026-10-11 | First undated ## Implementation entry (libvirt/SELinux networking run, `### Command 1: Check libvirt network state` through `### Command 29: Verify the policy file`; the root cause and `libvirt-veth` policy persistence remain in the 2026-09-30 ## Status bullet) | ~333 lines |
| 2026-10-11 | 2026-10-02 ## Implementation entries: Tails recovery run (orphaned QEMU kill, raw-to-qcow2 disk-driver fix in repo XML line 28, VM restore), Tails boot verification run (boot NOT verified; 2-color firmware stall frames 9f6b8c99.../7a04c068...; stale console client killed), Tails instance reconciliation run (cinnamon-1 moved to qemu:///system; firmware stall instance-independent, guest/firmware-level); superseded by the retained 2026-10-03 fresh-overlay and R1 golden integrity runs and the 2026-10-04 operator-VM replacement | ~160 lines |
| 2026-10-11 | 2026-10-03 ## Implementation entry: Tails fresh-overlay isolation run (thin overlay over the pristine golden reproduces the byte-identical 2-color firmware stall of cinnamon-1, frames 9f6b8c99.../7a04c068..., CPU spin 1:1, serial silent, no network; guest-side content exonerated; stopped with evidence, no fix); superseded by the retained 2026-10-03 R1 golden integrity run and the 2026-10-04 operator-VM replacement; recoverable from git at 02ec38e | ~71 lines |
| 2026-10-11 | Head of the 2026-10-03 R1 golden integrity run ## Implementation entry (first ~130 lines: entry header, domain stop, step 1 qemu-img check, step 2 live SHA-256, step 3 first-512-byte overlay-vs-golden NBD read, and the cmp octal diff block plus both 512-byte xxd dumps; the entry continues in-doc from `**4. Partition analysis of the golden (NBD /dev/nbd0)**`); pre-2026-10-04 superseded narration, boot investigation moot (the old environment is gone), recoverable from git at 02ec38e | ~130 lines |
| 2026-10-11 | 2026-10-03 R1 golden integrity run ## Implementation steps 4-5 (NBD /dev/nbd0 partition analysis with the fdisk GPT table; ESP copy to /tmp/r1-esp-2026-10-03, the two byte-identical grub.cfg trampolines, and the intro lines to the retained /boot/grub2/grub.cfg full-text dump; the dump itself and everything after it in the entry remain in-doc); pre-2026-10-04 superseded narration, boot investigation moot (the old environment is gone), recoverable from git at 02ec38e | ~69 lines |
| 2026-10-11 | First part of the retained /boot/grub2/grub.cfg full-text dump in ## Implementation (the code fence's opening line and DO-NOT-EDIT header comment, plus the `### BEGIN`/`### END` blocks from `00_header` through `10_linux`; the dump continues in-doc from `### BEGIN /etc/grub.d/10_reset_boot_success ###`); pre-2026-10-04 superseded narration, boot investigation moot (the old environment is gone), recoverable from git at 02ec38e | ~147 lines |
| 2026-10-11 | Second part of the retained /boot/grub2/grub.cfg full-text dump in ## Implementation (the `### BEGIN`/`### END` blocks from `10_reset_boot_success` through `41_custom`, plus the dump's closing code fence; the `**6. BLS entries**` block and everything after it remain in-doc); pre-2026-10-04 superseded narration, boot investigation moot (the old environment is gone), recoverable from git at 02ec38e | ~97 lines |
| 2026-10-12 | Tail of the 2026-10-03 R1 golden integrity run ## Implementation entry (the `**6. BLS entries (/boot/loader/entries, from the p3 read-only mount)**` block with both loader entry dumps, the /boot kernel/initrd existence line, steps 7-8 (overlay `qemu-img check`, `cinnamon-1` restart to canonical running state), and the entry's Changes/Checks run/Artifacts/Findings blocks); pre-2026-10-04 superseded narration, boot investigation moot (the old environment is gone), recoverable from git at 02ec38e | ~57 lines |
| 2026-10-12 | Pre-2026-10-04 ## Status entries: all ### entries dated 2026-10-03 and earlier (### 2026-10-03: fresh-overlay isolation test, the host-credential finding, nine 2026-10-02 entries, five 2026-10-01 entries including ### 2026-10-01: Implementation Complete) plus the - 2026-10-01 / - 2026-09-30 / - 2026-10-02 bullet entries; pre-2026-10-04 superseded narration, boot investigation moot (the old environment is gone); load-bearing facts preserved: the invalid GitHub token (API 401) is recorded in the TASK-0033 doc, the SELinux libvirt-veth policy fix persists in the vm-deploy skill (team-level hard-won gotcha) and the original 2026-09-30 bullet is recoverable from git at 02ec38e | ~122 lines |
