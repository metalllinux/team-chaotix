# TASK-0020 handoff prompt

Paste the block below into a new opencode session (it is addressed to Robotnik).

---

Continue TASK-0020 (TV project: quiet hours for hard drive activity) as Robotnik. The planning doc
is `planning/docs/TASK-0020-quiet-hours.md`; read its `## Status` and `## Next Actions` to
re-establish state.

**Checkpoint verified by Robotnik (2026-09-08):** the last Tails dispatch (item 10 fix round) was
cancelled by a connection reset and left no persistent work. `git status` on
`/home/howard/Linux/projects/project_tv_rocky_linux` shows exactly: modified `install.sh`,
`test/run_tests.sh`, `test/scripts/test_installer.sh`; untracked `quiet-hours/`,
`modules/21-quiet-hours.sh`, `test/scripts/test_quiet_hours.sh`; branch
`task-0020-quiet-hours` (uncommitted by design, committing is Knuckles' item). `## Implementation`
has no item 10 section, and `## Next Actions` already points at Tails for the fix round.

**State:** plan approved. Implementation items 1-6 complete: read-only production investigation
(gate PASS, target list `QUIET_K8S_CRONJOBS="jellyfin-library-refresh"`,
`QUIET_SYSTEMD_UNITS="sanoid.timer plocate-updatedb.timer"`), core state machine
`quiet-hours/quiet-hours.sh`, CLI `project-tv-quiet-hours` plus systemd service/timer, installer
module 21 wired into `install.sh`, 94/94 TAP, 12/12 installer. The review chain ran once on the
pre-fix tree: Shadow = 4 should-fix + 3 nits, Omega = 2 lows (DoD gate met, nothing above low),
Big = all executable checks PASS with the full `run_tests.sh` VM run skipped (no libvirt VM on the
team host; stays an open release gate).

**Next, strictly sequential, one dispatch at a time (endpoint runs `--parallel 1`):**
1. `Tails`: item 10 fix round. Cover every open finding with a sha in its `Resolution:` line:
   `## Review` (4 should-fix + 3 nits), `## Security` (2 lows), plus Big's two items in
   `## Test Results` (the `test_installer.sh` exit-code harness bug, and regression checks pinning
   the unit-testable should-fix scenarios).
2. Re-run the chain `Shadow` → `Omega` → `Big` until clean (no unresolved should-fix-or-above;
   Big also closes or explicitly waives the VM gate).
3. `Vector`: README and user-facing docs, including the stale-IP fix at `CLAUDE.md:117`
   (192.168.1.191 is a stale IP; the live host is 192.168.1.107, hostname `vector`).
4. `Knuckles`: GPG-signed commit, PR to `metalllinux/project-tv-rocky-linux-edition` (in-account,
   no human gate required), verify the release commit contains only this task's changes with no
   mode-bit drift, merge.
5. `Espio`: prune the planning doc.

**Standing constraints:** production 192.168.1.107 is read-only without user consultation; the
howard password lives in `~/pass.txt` on the team host and credentials must never be written to a
doc, commit, or log; active TV playback must keep working during quiet hours (PM decision in
`## Status`).
