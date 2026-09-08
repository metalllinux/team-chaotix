# TASK-0020 — TV project: quiet hours for hard drive activity

> **Section order below is fixed.** Each agent writes to its own section and no other. `Robotnik`
> reads only `## Status` and `## Next Actions`. Do not reorder, rename, or remove sections.

- **Created:** 2026-09-07

---

## Status

*Owner: `Robotnik`. Keep this SHORT and CURRENT — it is one of only two sections the PM reads, so a
stale entry means the whole loop runs on bad information.*

**Now:** Review chain complete on the post-fix tree (2026-09-08): Shadow verified 11/11 closures
(2 new nits), Omega verified both lows (1 new low), Big PASS (8 requested, 7 executed, VM run
explicitly waived, no libvirt VM on the team host, conditions recorded in `## Test Results`).
User decision 2026-09-08: the three open non-blocking items are deferred, no pre-commit folding;
release proceeds. Tree is exactly Big's verified state (118/118, 12/12, failure path rc 1,
credential audit clean, no mode drift); the cancelled Tails re-dispatch made 0 tool calls, no
drift. Next: Vector (item 11), then Knuckles (item 12).

**Environment / scope:**
- Files in scope: `/home/howard/Linux/projects/project_tv_rocky_linux` (local clone of
  `metalllinux/project-tv-rocky-linux-edition`, branch `main`). Primary target `install.sh` plus
  whatever modules/lib it uses. Upstream repo is `metalllinux/project-tv-rocky-linux-edition`.
- Touches the DB schema: no
- Graphical UI: no
- Rocky Linux target: yes (production media server at 192.168.1.107, Rocky Linux)

**Decisions (PM, 2026-09-07):**
- Quiet hours must not break active TV playback. The mechanism must target the background HDD I/O
  sources, not suspend the whole media stack. If the investigation shows the only viable mechanism
  stops playback, the plan must surface that trade-off explicitly before implementation.
- Production instance 192.168.1.107 is **read-only** for this task. No changes of any kind without
  explicit user consultation. The `howard` password lives in `~/pass.txt` on the team host.
  Credentials must never be written to this doc, to a commit, or to a log.
- The user's existing uncommitted local changes are out of scope for this task. The release
  commit must contain only this task's changes.
- Host conflict resolved 2026-09-08: identity gate PASS on 192.168.1.107 (hostname `vector`,
  single-node k8s v1.32.13, full project-tv stack), independently confirmed by the user.
  `CLAUDE.md:117`'s 192.168.1.191 is a stale IP for the same host; Vector fixes it.

**Decisions (user, 2026-09-08):**
- Production write permission: the user granted full permission for write changes on
  192.168.1.107 to apply the quiet-hours changes. The 2026-09-07 read-only rule is lifted for
  the apply step only. Final deliverable after the release push: a prompt file for applying the
  changes to production, written so no credential ever appears in it (the password stays in
  `~/pass.txt` on the team host, read at runtime).
- All task changes must be pushed to `metalllinux/project-tv-rocky-linux-edition` (in-account,
  no human gate; Knuckles verifies the push landed on GitHub).

**Unknowns:**
- (Resolved 2026-09-08, evidence in `## Implementation` item 1) HDD activity sources on the
  12T pool: `plocate-updatedb.timer` (daily 00:18 full-library walk, the largest scheduled
  contributor), `sanoid.timer` (daily ~00:00 snapshot pass; hourly runs verified no-ops), and the
  `jellyfin-library-refresh` CronJob (hourly, 4s incremental scan). All three sit inside the
  window and are quiable; target list `QUIET_K8S_CRONJOBS="jellyfin-library-refresh"`,
  `QUIET_SYSTEMD_UNITS="sanoid.timer plocate-updatedb.timer"` (plocate added via the gate's
  extension clause). Playback dominates the pool (~253MB read in 88 min during TV viewing) and
  stays loud by the PM decision above; if the user finds that insufficient it is a new decision,
  not a fix.
- (Resolved 2026-09-07, PM) Pre-existing uncommitted changes: verified mode-only, 755 to 644 on
  7 files, zero content lines (`git diff --summary` on the project checkout). Restored by
  Tails' item 2 (tree == HEAD, guard satisfied); Knuckles still verifies no mode bit leaks into
  the release commit.

---

## Definition of Done

*Owner: `Robotnik`, and nobody else. Written **before** any work starts. Objectively checkable —
if a box cannot be verified by looking at something, rewrite it.*

- [ ] Plan approved: `## Plan` names a concrete quiet-hours mechanism with rationale, grounded in
      read-only verification of the HDD activity source on production. PM approval recorded in
      `## Status`.
- [ ] Activity source verified: findings in this doc name the process(es)/container(s) producing
      the HDD writes/reads, with the exact commands that produced the evidence, run on
      192.168.1.107. Only read-only commands were used (verifiable from the command list).
- [ ] No production changes: nothing on 192.168.1.107 was modified, installed, or restarted by the
      team, per the PM decision in `## Status`.
- [ ] Installer option: the installer offers a quiet-hours option with configurable start and end
      hour, defaulting to 20:00-07:00, and the option is visible in installer help/usage output.
- [ ] Mechanism: during the configured window, HDD I/O from the verified source(s) is limited while
      active playback continues to work (PM decision). The mechanism fails soft: on error it logs
      and leaves the system in normal (loud) operation, never a broken media server.
- [ ] Override commands: a user-facing command enables quiet hours immediately outside the window,
      and a second command removes them. The override persists until the disable command is run,
      including the documented behaviour across reboots.
- [ ] Time correctness: the window calculation is correct across the midnight wrap (20:00-07:00)
      and across DST transitions, with unit tests as evidence.
- [ ] Credentials: the 192.168.1.107 password appears nowhere in this doc, in commits, or in logs.
- [ ] Code compiles / linters pass: `bash -n` and the project's existing lint/test tooling on all
      changed files.
- [ ] `Shadow`: no unresolved blockers or should-fix findings in `## Review`
- [ ] `Omega`: no unresolved findings above `low` in `## Security` (includes license check on added
      code)
- [ ] `Big`: unit tests for the window calculation and the override state machine, plus installer
      dry-run checks, all PASS, with no silently dropped checks
- [ ] `Vector`: README and user-facing docs updated (the option, its default, the override
      commands, the behaviour during quiet hours)
- [ ] `Knuckles`: PR to `metalllinux/project-tv-rocky-linux-edition` contains only this task's
      changes, merges to `main`. The user's pre-existing uncommitted changes were not swept in.
- [ ] Planning doc pruned by `Espio`

---

## Next Actions

*Owner: whoever wrote last. The future only — delete what has been done. The second of the two sections
the PM reads.*

- [ ] `Espio` (handoff from Knuckles, 2026-09-08, item 12 done): prune this doc per the `##
  Archive` rules — superseded detail into `## Archive` (item 1 command list and interim
  measurement notes, resolved unknowns A1-A6, fix-round narration superseded by the merged sha),
  decisions and verified facts stay, add a row to the pruning log.
- [ ] `Robotnik` (after pruning): closure — tick the last DONE item ("Planning doc pruned by
  Espio"), mark TASK-0020 shipped in `planning/TASKS.md`, and note the remaining user-decision
  deliverable (production apply prompt file for 192.168.1.107, credential-free) if not yet tracked.

---

## Plan

*Owner: `Amy`. Written 2026-09-07 from read-only investigation of the local tree at
`/home/howard/Linux/projects/project_tv_rocky_linux` (branch `main`, tip `c520226`,
`git log --oneline -15`) and of this doc's `## Status`/`## Definition of Done`. The production host
was not reached from the planner seat: this agent's shell is restricted to git/gh/rg, so no SSH is
possible from here. Item 1 below is the read-only production investigation, executed by `Tails`, who
has bash. Everything in "Verified local facts" was checked in the working tree; everything labelled
assumption is not yet verified.*

**Decision doc:** `planning/decisions/TASK-0020-quiet-hours-mechanism.md` (one-pager, mechanism choice).

**Why this task exists** — the user wants the production media server's hard drives to go quiet at
night (default 20:00-07:00) while TV playback must keep working (PM decision, `## Status`). The repo's
code shows the scheduled background I/O sources: the hourly `jellyfin-library-refresh` CronJob
(`manifests/cronjobs/jellyfin-library-refresh.yaml:10`, schedule `0 * * * *`) whose job only POSTs to
Jellyfin's `/Library/Refresh` API (`jellyfin-library-refresh.yaml:26-28`), so the scan runs inside the
Jellyfin server process; and the hourly `sanoid.timer` ZFS snapshot runs
(`modules/12-sanoid.sh:128-138`, `OnCalendar=${timer_calendar}`, default `hourly` at
`modules/12-sanoid.sh:60`). Optional `media-sync.timer` (rsync, monthly default,
`modules/13-rsync.sh:62-93`) exists only if the user ran module 13, which is not in `MODULE_ORDER`
(`install.sh:50`). No ZFS scrub is scheduled anywhere in the repo (`rg scrub` over the tree: no match).

**The mechanism (concrete).** A host-level systemd timer runs a small state-machine script
`/usr/local/lib/project-tv/quiet-hours.sh` every 15 minutes and once at boot. It reads
`/etc/project-tv/quiet-hours.conf` (`QUIET_START_HOUR=20`, `QUIET_END_HOUR=7`, `QUIET_ENABLED=1`,
`QUIET_OVERRIDE=0`, `QUIET_K8S_CRONJOBS="jellyfin-library-refresh"`,
`QUIET_SYSTEMD_UNITS="sanoid.timer"`) and computes the desired state: quiet if the override flag is set
or the current local hour is in the window (start inclusive, end exclusive; wrap-aware, so 20-07 means
hours 20-23 and 0-6). On a state change it transitions:

- loud→quiet, per target, each step independent, logged, retried next tick on failure (fail-soft:
  on any error the script logs to the journal and exits 0, leaving the system loud or partially quiet,
  never broken):
  1. `kubectl -n project-tv patch cronjob <name> --type merge -p '{"spec":{"suspend":true}}'` for each
     CronJob in `QUIET_K8S_CRONJOBS`;
  2. delete in-flight jobs of that CronJob (list `kubectl -n project-tv get jobs -o name`, delete each
     name matching `<cronjob-name>-*`; no `| grep` pipelines, per the pipefail trap at
     `CLAUDE.md:170-173`);
  3. `systemctl stop <unit>` for each unit in `QUIET_SYSTEMD_UNITS` (`sanoid.timer`; the `Persistent=true`
     at `modules/12-sanoid.sh:134` means missed runs catch up after restore).
- quiet→loud: patch `suspend: false`, `systemctl start <unit>`.

The applied state is written to `/var/lib/project-tv/quiet-hours/state` (`loud`/`quiet`) only when all
steps of a transition succeed; otherwise the file keeps its old value and the next tick retries. The
streaming path (Jellyfin pod reads) is never touched, which is why playback keeps working. This is why
per-process throttling was rejected: the scan and the stream share one process, so `ionice`/cgroup
`io.max` on the Jellyfin pod would throttle playback too (see decision doc, option B).

**User-facing surface.**
- Installer option, new module 21 (`modules/21-quiet-hours.sh`, module number 21 is free; the old VNC
  module 21 was removed in `e86b7b7`): prompts enable yes/no, start hour (0-23, default 20), end hour
  (0-23, default 7) via `ask_number` (`lib/prompts.sh:67`), rejects start==end with a re-prompt, then
  installs the script, CLI, and both units, writes the config, `systemctl daemon-reload`,
  `systemctl enable --now project-tv-quiet-hours.timer`, runs the service once to apply the current
  state. If `kubectl` is missing it warns and skips the k8s targets (fail-soft, module completes).
  Wiring in `install.sh`: `MODULE_DESC[21]="Quiet hours (HDD activity)"`, append `21` to `MODULE_ORDER`
  (after 20, so k8s and sanoid exist first), and widen the module prompt at `install.sh:234` from
  `(0-20)` to `(0-21)`. Visibility per DoD: the module menu (`install.sh:151-164`) auto-lists
  `MODULE_DESC`, so `21  Quiet hours (HDD activity)` appears there; the module prints its own usage text
  with the 20:00-07:00 default at its prompts.
- Override CLI `/usr/local/bin/project-tv-quiet-hours` (root): `status` (config, desired vs applied
  state, next transition), `enable` (sets `QUIET_OVERRIDE=1`, triggers the service immediately so quiet
  applies outside the window too), `disable` (clears the flag, triggers immediately). The flag lives in
  `/etc/project-tv/quiet-hours.conf`, so it persists across reboots until `disable` is run; at boot the
  service's one-shot run re-applies quiet if the flag is on or the window is active. Documented in the
  README (Vector).

**Verified local facts** (working tree, 2026-09-07):
- `git status` on the project: 7 modified files, all mode-only. `git diff` shows `old mode 100755 /
  new mode 100644` on `install.sh`, `test/run_tests.sh`, `test/scripts/test_installer.sh`,
  `test/scripts/test_k8s_apps.sh`, `test/scripts/test_rpm_install.sh`, `test/scripts/test_zfs.sh`,
  `drivers/px4_drv/build_rpm.sh`; `git diff --stat` reports `0 insertions(+), 0 deletions(-)`.
- The project's own test requires `install.sh` executable (`test/scripts/test_installer.sh:19-23`,
  B-01), so the 644 bits break the repo's own suite; they are treated as accidental (assumption A4).
- `test/run_tests.sh` invokes test scripts explicitly, not by glob (`test/run_tests.sh:98,102,106`);
  `scp -r "$SCRIPT_DIR/scripts/"` copies the whole directory (`test/run_tests.sh:88`), so a new TAP
  script lands in the VM automatically and needs one added invocation line.
- `install.sh` uses `set -euo pipefail` (`install.sh:9`), modules are sourced and expose `run()`
  (`install.sh:102`), `STATUS_FILE` tracks per-module state (`install.sh:53`).
- The TV project repo has no `.github/` (glob: no match), so it has no CI of its own; its test tooling
  is the TAP scripts + `run_tests.sh` on a VM.
- Team-chaotix CI exists and runs on push: `gh run list` shows `Static Checks` and `Secret Scan Self`
  workflows on `main`. `Secret Scan Self` is the credential DoD gate for this doc.

**Assumptions (labelled, to be confirmed or killed by item 1):**
- A1. 192.168.1.107 is the k8s media server. Conflict: `CLAUDE.md:117` says the deployment target is
  `vector` / 192.168.1.191. The PM's `## Status` names 192.168.1.107 and is binding for the
  investigation target; item 1's gate commands verify the role. If they fail, item 1 stops and reports.
- A2. The top HDD I/O sources in the quiet window are the two scheduled sources above. Unverified until
  item 1 samples I/O in-window. If the top source is EPGStation live recording or Jellyfin streaming
  itself, the only mechanisms that stop it break playback or recording: per the PM decision the
  trade-off is surfaced before implementation and the cycle returns to `Amy`.
- A3. `sshpass` exists (or is installable via `dnf`) on the team host. Unverified; item 1 checks and
  records the fallback used.
- A4. The 7 mode-only local changes are accidental. Evidence above; the project's own B-01 test fails
  on them. If the user objects at release, Knuckles stops and consults (PM decision).
- A5. The production host's timezone is Asia/Tokyo (`config/defaults.conf:6`, module 01), so it has no
  DST; DST correctness is still unit-tested per DoD.
- A6. `howard` can read kubectl/zfs/journal output directly or via read-only sudo. Unverified; item 1
  records any permission denial as a limitation rather than working around it.

**Item 1 — read-only investigation command list** (run on 192.168.1.107 as `howard`; credential from
`~/pass.txt` on the team host, passed only via `SSHPASS` env var to `sshpass -e`, never on any command
line, never in this doc, commit, or log. Read-only commands only; no sudo unless a read-only command is
permission-denied as `howard`, in which case sudo with the same credential and the exact sudoed command
is recorded. The I/O sample (section 3) must straddle a top-of-hour inside the user's reported window
(20:00-07:00 local) so the hourly CronJob and sanoid fire during the sample):

```
# 1. Identity gate (A1): is this the media server?
hostname
head -3 /etc/os-release
kubectl get nodes -o wide
kubectl get pods -A --no-headers | head -40

# 2. Storage topology and scrub state
zpool status
zfs list -o name,mountpoint,used | head -20
grep -E ' sda | sdb ' /proc/diskstats

# 3. I/O attribution, 3-minute per-process sample straddling :00, in-window
command -v pidstat iotop sysstat
pidstat -d 5 36
# fallbacks if sysstat absent: iotop -b -n 3 -d 60 -o, or two /proc/[0-9]*/io snapshots 60s apart
# diffed for read_bytes/write_bytes per pid

# 4. What is scheduled
systemctl list-timers --all --no-pager
kubectl -n project-tv get cronjobs
kubectl -n project-tv get cronjob jellyfin-library-refresh -o jsonpath='{.spec.schedule} {.spec.suspend}'
kubectl -n project-tv get jobs -o wide

# 5. Per-component confirmation (last 12h)
kubectl -n project-tv logs deploy/jellyfin --since=12h --tail=2000 | grep -iE 'scanning|refresh|library' | tail -25
journalctl -u sanoid.service --since "12h ago" --no-pager | tail -30
zfs list -t snapshot -o name,creation | tail -20
kubectl -n project-tv logs deploy/epgstation --since=12h --tail=2000 | grep -iE 'record' | tail -25
df -h /var/lib/project-tv /mnt 2>/dev/null
```

**Gate (item 1 exit):** PASS when the top-3 I/O sources are all within the quietable target list
(extend `QUIET_K8S_CRONJOBS`/`QUIET_SYSTEMD_UNITS` if the sample shows `media-sync.timer` or another
scheduled unit active). STOP-and-report when the top source is only stoppable by breaking
playback/recording (trade-off, back to `Amy`), or when the identity gate fails (A1 conflict, back to PM
for user consultation). Findings + every command actually run + output summaries go to `##
Implementation` (Tails' section) before any implementation starts.

**MVP** — module 21 + the mechanism above targeting `jellyfin-library-refresh` + `sanoid.timer`, the
override CLI, and the window/override unit tests. Deferred: per-target toggles (e.g. "keep sanoid
running"), recording-aware suppression (shrink the window around EPGStation recordings), a Prometheus
dashboard for quiet-hours state, and minute-granularity windows (15-minute tick is the resolution;
adequate for hour-scale windows).

**What this makes harder later** — the target list is a named contract: every future app module that
adds scheduled I/O must register its unit, or it will be loud at night unexplained. New persistent
host state (`/etc/project-tv/quiet-hours.conf`, the state file) must be handled by future reinstall and
backup work. The 15-minute tick caps transition precision; a later minute-scale feature needs a
finer timer or a long-running service.

**Work breakdown** — one agent finishes one item in one turn; sequential dispatch per AGENTS.md §3.

| # | Item | Owner agent | Acceptance criterion | Parallel with |
|---|---|---|---|---|
| 1 | Read-only production investigation per the command list above; record findings, exact commands run, and gate verdict in `## Implementation`; credential via `SSHPASS` env only; verify after the fact with `grep -Ff ~/pass.txt` on this doc (pattern-from-file, never argv) | `Tails` | Findings name the top-3 HDD I/O sources with command evidence; gate verdict (PASS / STOP-trade-off / STOP-identity) recorded; zero write commands used (verifiable from the recorded command list); password absent from doc, verified by the grep above | Independent of 2 (remote vs local); on the critical path before 3 |
| 2 | Restore the 7 mode-only bits (`chmod +x` on the 7 files listed in Verified local facts) and create branch `task-0020-quiet-hours` from `origin/main`; guard: `git diff --stat` on those 7 files is empty and `git status` shows no content changes before any task commit; record in `## Implementation` | `Tails` | Working tree matches HEAD except this task's files; B-01 of `test_installer.sh` passes in-tree | Independent of 1; must land before item 3's first commit |
| 3 | Core script `quiet-hours/quiet-hours.sh`: window calc (start inclusive, end exclusive, wrap-aware; start==end treated as full 24h defensively), config parse with fail-soft, state machine, apply/release with per-step error isolation, env-overridable paths (`QUIET_HOURS_CONF`, `QUIET_HOURS_STATE`) for tests | `Tails` | `bash -n` passes; functions sourceable without side effects; no secret material in the file | After 1 (target list confirmed) and 2 |
| 4 | CLI `quiet-hours/project-tv-quiet-hours` (`status`/`enable`/`disable`/usage with the 20:00-07:00 default visible) + systemd units `quiet-hours/project-tv-quiet-hours.{service,timer}` (15-min timer, oneshot, runs once at boot) | `Tails` | `bash -n` passes; usage output shows the default window; units contain the required `[Unit]/[Service]/[Timer]/[Install]` sections | After 3; independent of 5a |
| 5a | TAP unit tests in new `test/scripts/test_quiet_hours.sh`: window matrix (20-07 wrap, 10-14 no-wrap, boundary inclusivity), DST cases with fixed timestamps under `TZ=America/New_York` (spring-forward and fall-back 2026) and `TZ=Europe/Berlin` plus `TZ=Asia/Tokyo` control, override state machine with stubbed apply/release (enable outside window, disable, reboot simulation with reset state file, config parse error, failed apply step leaves state file unchanged) | `Tails` | All TAP lines `ok`; zero silently dropped checks; runs on the team host without a VM | After 3 |
| 5b | Structural tests appended to `test_quiet_hours.sh` (module 21 file exists and defines `run()`, `MODULE_DESC[21]` and `21` in `MODULE_ORDER` in `install.sh`, quiet-hours files present, `bash -n` on all changed files, CLI usage shows the default) + one invocation line in `test/run_tests.sh` (file has the mode-only local change; content edit is this task's) | `Tails` | Full TAP file passes in-tree; `run_tests.sh` line placed next to the other script invocations (`test/run_tests.sh:98-106` pattern) | After 4 |
| 6 | Installer module `modules/21-quiet-hours.sh` + `install.sh` wiring (`MODULE_DESC[21]`, `MODULE_ORDER` append, prompt range `(0-20)`→`(0-21)` at `install.sh:234`) | `Tails` | Module appears in the module menu listing; prompts default to 20/7; decline path marks the module skipped; kubectl-missing path warns and skips k8s targets; re-run overwrites cleanly | After 5b (reviews see the final tree) |
| 7 | Review: code review, findings in `## Review` | `Shadow` | No unresolved blocker/should-fix | After 6; fixed sequence 7→8→9 per AGENTS.md §3 |
| 8 | Security review: no credentials in any changed file, config/state file permissions, root-only CLI, license check on added code (all original, no third-party code introduced), findings in `## Security` | `Omega` | No unresolved findings above `low` | After 7 |
| 9 | Test run: `test_quiet_hours.sh` on the team host, `test_installer.sh` in-tree (regression, B-01 included), `bash -n` on all changed files; full `run_tests.sh` VM run at Big's discretion (recorded if skipped); verdicts in `## Test Results` | `Big` | All requested checks PASS with counts; any dropped check named explicitly | After 8 |
| 10 | Fix round for findings (only if 7/8/9 found something) | `Tails` | Each finding resolved with a sha in its Resolution line | Contingent branch off 7/8/9 |
| 11 | Docs: `README.md` quiet-hours section (option, 20:00-07:00 default, override commands, in-window behaviour, reboot behaviour, uninstall), `docs/ja/README.md` kept in sync (repo convention, `CLAUDE.md:234`), `CLAUDE.md` module order + common tasks updated; table in `## Docs` | `Vector` | English and Japanese sections present and consistent; `## Docs` table complete | After 10 (or 9 if no fixes) |
| 12 | Release: verify tree contains only this task's files (`git status --short`, `git diff --stat` on the 7 files empty), commit per-file (`git add <file>`, never `git add -A`) with `TASK-0020:` prefix, PR to `metalllinux/project-tv-rocky-linux-edition` (internal account, no human gate per AGENTS.md §8), verify PR diff contains only this task's files, merge, record sha + `git ls-remote origin main` in `## Release`; planning-doc update committed to team-chaotix (gated by its `Static Checks` + `Secret Scan Self` CI) | `Knuckles` | PR merged; `## Release` filled; user's 7 mode bits absent from every commit (`git show --stat` on the release commits shows only task files) | After 11 |

**Dependencies and sequence.** Genuinely ordered: 1→3 (the gate confirms the target list), 3→4→5b→6,
6→7→8→9 (fixed review-trio sequence, AGENTS.md §3), 9→10→11→12. Item 10 is contingent, not sequential:
it runs only on findings. Item 2 is independent of 1 (local vs remote) and item 4 is independent of 5a;
with one inference slot the order of independent items is free along the critical path, so they are
listed above in a sensible order, not a mandate.

**Critical path:** 1 → 3 → 4 → 5b → 6 → 7 → 8 → 9 → 11 → 12 (item 10 branches off 7/8/9 when needed;
items 2 and 5a sit off the path).

**Estimates** (agent turns, three-point, `T = (O + 4M + P) / 6`):

| # | O | M | P | T |
|---|---|---|---|---|
| 1 | 1 | 2 | 4 | 2.2 |
| 2 | 1 | 1 | 2 | 1.2 |
| 3 | 2 | 3 | 5 | 3.2 |
| 4 | 1 | 2 | 3 | 2.0 |
| 5a | 2 | 3 | 6 | 3.3 |
| 5b | 1 | 1 | 2 | 1.2 |
| 6 | 1 | 2 | 3 | 2.0 |
| 7 | 1 | 2 | 3 | 2.0 |
| 8 | 1 | 2 | 3 | 2.0 |
| 9 | 1 | 2 | 4 | 2.2 |
| 10 | 0 | 1 | 3 | 1.3 (contingent) |
| 11 | 1 | 2 | 3 | 2.0 |
| 12 | 1 | 2 | 4 | 2.2 |

Total ≈ 26.8 turns expected (≈25 median). Buffer +30% for window scheduling (item 1 must wait for an
in-window top-of-hour slot), review rounds, and 32k turn-cap truncation retries (AGENTS.md §14):
**plan at 35 agent turns.**

**Risks:**

| Risk | Likelihood | Impact | Mitigation | Contingency |
|---|---|---|---|---|
| R1: 192.168.1.107 is not the media server (A1 conflict with `CLAUDE.md:117`) | medium | high (investigation wasted) | Identity gate commands run first in item 1 | STOP, record, PM consults the user for the correct target |
| R2: top I/O source only stoppable by breaking playback/recording (A2) | low-medium | high (mechanism invalid) | Gate in item 1 before any implementation; decision doc rejects throttling up front | Surface trade-off in `## Implementation`, back to `Amy` to re-plan (options: narrower window around recordings, or user accepts the source) |
| R3: `sshpass` missing on the team host (A3) | medium | low (item 1 delay) | `command -v sshpass` first in item 1 | `dnf install -y sshpass` (team host, recorded) or expect-based fallback |
| R4: credential leaks into doc, commit, or log | low | critical (DoD failure) | `SSHPASS` env only, never argv; post-verification `grep -Ff ~/pass.txt` on this doc (pattern-from-file); team-chaotix `Secret Scan Self` CI on the doc push | If found: stop, write to `## Security`, escalate to user per AGENTS.md §4 (no history rewriting by the team) |
| R5: the mode bits were deliberate, not accidental (A4) | very low | low | Evidence recorded (B-01 requires executable; HEAD is 755); change documented in `## Implementation` | Knuckles stops and consults the user at release (PM decision); the release commit itself is unaffected except `install.sh`, which must stay 755 to be runnable |
| R6: window logic wrong across DST or the midnight wrap | low | medium (host has no DST per A5, but DoD demands correctness) | Hour-granular set semantics (no arithmetic across the wrap), TZ-matrix unit tests in 5a | Tests catch it pre-merge; the 15-min tick self-heals any one-hour drift on a transition day |
| R7: kubectl absent or cluster down when the service ticks | low | low | Per-step error isolation: log, continue, exit 0, retry next tick; state file only updated on full success | Worst case is 15 extra minutes of the previous state, self-healing; module 21 warns if kubectl is missing at install |
| R8: 32k turn-cap truncation kills a dispatch (TASK-0019) | medium | medium (wasted turns) | One item per turn per the breakdown; findings checkpointed to the doc after each item; small briefs | Re-dispatch with a smaller brief; detect via the session DB per AGENTS.md §14 rule 4 |

**Validation:**
- Syntax: `bash -n` on `install.sh`, `modules/21-quiet-hours.sh`, `quiet-hours/quiet-hours.sh`,
  `quiet-hours/project-tv-quiet-hours`, `test/scripts/test_quiet_hours.sh`, `test/run_tests.sh` (item 9).
- Unit/structural: `test/scripts/test_quiet_hours.sh` all `ok` on the team host, no VM needed (item 9).
- Regression: `test/scripts/test_installer.sh` in-tree, 12/12 including B-01 after item 2 (item 9).
- Investigation audit: the command list recorded in `## Implementation` contains only the read-only
  commands from item 1's list (or their recorded sudo variants); DoD "No production changes" is verified
  from that list, not by assertion.
- Credential audit: `grep -Ff ~/pass.txt` over the doc returns nothing (item 1 post-check, re-run by
  Knuckles before push); `Secret Scan Self` CI green on the planning-doc push.
- Human look: the PR file list (Knuckles shows `git diff --stat` of the merge), the README quiet-hours
  section (user-facing wording), and the investigation findings (the user's own hypothesis about
  Jellyfin is confirmed or refuted there).

**Rollback:**
- Detect: pre-merge, CI/tests in item 9 and the PR diff check. Post-merge, the change is inert until
  the user re-runs the installer on a host; on a host, `project-tv-quiet-hours status` and
  `journalctl -u project-tv-quiet-hours` show the state and any fail-soft log lines. Failure mode is
  bounded by design: the mechanism fails to loud, never to a broken media stack.
- Exact revert, repo: `git revert -m 1 <merge-sha>` on `main` of
  `metalllinux/project-tv-rocky-linux-edition`, push, re-verify with `git ls-remote origin main`.
- Exact revert, host (if module 21 was applied): `systemctl disable --now project-tv-quiet-hours.timer;
  systemctl stop project-tv-quiet-hours.service; kubectl -n project-tv patch cronjob
  jellyfin-library-refresh --type merge -p '{"spec":{"suspend":false}}'; systemctl start sanoid.timer;
  systemctl daemon-reload; rm /etc/systemd/system/project-tv-quiet-hours.service
  /etc/systemd/system/project-tv-quiet-hours.timer /usr/local/lib/project-tv/quiet-hours.sh
  /usr/local/bin/project-tv-quiet-hours /etc/project-tv/quiet-hours.conf` (documented in the README by
  Vector; only targets actually present, per the host's config).
- Point of no return: none in practice. The PR merge is cheaply revertible; the only persistent host
  state the mechanism writes is the CronJob `suspend` flag and the sanoid timer state, both restored by
  the revert above. A partially applied transition is healed by the next 15-minute tick (state file only
  advances on full success), so a failed run leaves at most 15 minutes of the previous state behind,
  which a retry tolerates by construction.
- Deployment note for `## Release`: no deployment to dispatch. Production 192.168.1.107 is read-only
  (PM decision); the installer change takes effect only when the user next runs the installer, on their
  schedule, out of scope for this task.

---

## Implementation

*Owner: `Tails`.*

**Alternatives considered**

### Problem: how to run the read-only investigation on 192.168.1.107 without leaking the credential
**Option A — `sshpass -e` with `SSHPASS` from `~/pass.txt`** · How: `export SSHPASS="$(cat ~/pass.txt)"` in a single team-host shell, then `sshpass -e ssh howard@192.168.1.107 '<read-only commands>'`. The password exists only as an env var of that shell; never on any command line, never on the remote host, never written to any file. · Pros: exactly the path the plan prescribes (item 1); auditable; production host untouched. · Cons: needs `sshpass` (verified present: `command -v sshpass` → `/usr/bin/sshpass`; A3 resolved).
**Option B — SSH key or expect** · How: provision a keypair (requires a write on production), or script the password prompt with an expect script. · Pros: none over A in this setup. · Cons: key provisioning modifies the production host (forbidden by the PM read-only decision); expect requires the password in a script file.
**Chosen:** Option A, because it is the plan-prescribed path and the only one that keeps the production host untouched.
**Competing priorities:** convenience (key-based ssh for later items) traded away in favour of the read-only decision; if the user later wants key auth they can provision it themselves.

### Problem: how to attribute HDD I/O to processes when the media stack runs in k8s pods
**Option A — host-level `pidstat -d` + `/proc/diskstats` deltas** · How: `pidstat -d 5 N` as `howard` on the node; correlate per-process rows with device counters on sda/sdb. · Pros: one standard tool (sysstat installed); pod processes turned out to be visible in the host `/proc` on this node (verified: PID 13016 `jellyfin`, cgroup `/kubepods.slice/kubepods-burstable.slice/...`; both `ps` and `pidstat` list it), so per-pod attribution works. · Cons: depends on that visibility, which is node-specific.
**Option B — per-pod `kubectl exec ... cat /proc/self/io` or cAdvisor/Prometheus scrape** · How: read io counters inside each container, or query `container_fs_*` metrics. · Pros: works even under full PID-namespace isolation. · Cons: `exec` into a pod is a stronger action than the plan's host-level list; Prometheus endpoint/auth unverified; `/proc/self/io` in an exec sees only the exec'd process.
**Chosen:** Option A, because the visibility assumption was verified true on this node during the investigation itself; the per-process rows are the evidence the gate needs.
**Competing priorities:** generality across arbitrary nodes traded away; on this node Option A is strictly sufficient and stays inside the plan's command list.

**Item 1 — investigation findings (192.168.1.107, user `howard`, 2026-09-07 19:59-21:15 JST, all commands read-only)**

**Identity gate: PASS.** `hostname` → `vector` (matches the hostname at `CLAUDE.md:117`), `head -3 /etc/os-release` → Rocky Linux 10.1 (Red Quartz), `kubectl get nodes -o wide` → single-node control-plane `vector` at INTERNAL-IP 192.168.1.107, k8s v1.32.13, containerd 2.2.2. `kubectl get pods -A --no-headers | head -40` shows the full `project-tv` stack: jellyfin, epgstation, mirakurun, mariadb, navidrome, tubearchivist, elasticsearch, redis, grafana, prometheus, node-exporter, plus the `jellyfin-library-refresh` jobs. The node is unambiguously the production media server. **Discrepancy recorded for Vector:** `CLAUDE.md:117` names 192.168.1.191 as the production IP; the live host is 192.168.1.107. The hostname matches, so this is a stale IP, not a different machine (A1 resolved, nuance recorded).

**Disk topology (why the user hears the HDDs):** `lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINT` shows two 10.9T SATA disks `sda`/`sdb` (both `zfs_member` of pool `vector` — the audible media drives) and one 476.9G `nvme0n1` holding `/boot`, `/` (LVM `rl_project--tv-root` 70G, 67% used) and `/home`. Consequence: all container state under `/var/lib/project-tv/*` (mariadb, redis, elasticsearch, tube-archivist cache, jellyfin config+cache, prometheus, grafana) lives on the **NVMe, not the HDDs**. Only these touch the ZFS pool: jellyfin media reads (`media-*` hostPaths → `/mnt/vector/*`, verified via `kubectl -n project-tv get deploy jellyfin -o jsonpath='{range .spec.template.spec.volumes[*]}{.name}={.hostPath.path}{"\n"}{end}'`), epgstation recordings (`recorded=/mnt/vector/tv`, verified on the live deployment), navidrome music reads (`/mnt/vector/music`), and sanoid snapshots. `zpool status`: `vector` ONLINE, mirror of `ata-ST12000NM0127` ×2 (Seagate 12TB IronWolf Pro), no errors. `zfs list -o name,mountpoint,used | head -25`: 2.15T used across 10 datasets (`films` 1.18T, `children_shows` 645G, `shows` 220G, `tv` 6.14G, `live_shows` 20.6G, `music` 37.4G, `photos` 21G, `anime` 39.4G, `skateboarding` 8.46G, `dance_videos` 1.19G).

**HDD I/O sources, verified per source:**
1. **`jellyfin-library-refresh` CronJob (hourly, `0 * * * *`, suspend=false — `kubectl -n project-tv get cronjob jellyfin-library-refresh -o jsonpath='{.spec.schedule} {.spec.suspend}'`)** — the 20:00 job completed in 4s (`kubectl -n project-tv get jobs -o wide`); the resulting scan is short: jellyfin log (20:00:05) `Scan Media Library Completed after 0 minute(s) and 4 seconds` (incremental; the library monitor keeps the DB current between scans). Negligible I/O, but a real scheduled pool reader. **Quiable: yes (CronJob suspend).**
2. **`sanoid.timer` (hourly, `systemctl list-timers`)** — the live config `cat /etc/sanoid/sanoid.conf` has `hourly = 0, daily = 30` (mtime 2026-04-06 09:09:51 = install time, unchanged since). `journalctl -u sanoid.service --since "12h ago"` shows the 19:00 and 20:00 runs print `taking snapshots...` and exit in <1s **without taking any snapshot** (no-op). The only snapshots taken are daily: the 18:14:50-52 post-reboot Persistent catch-up created one `_daily` snapshot per dataset (11 datasets, ~3s total). So the only real sanoid pool I/O in the quiet window is the **~00:00 daily snapshot pass**. **Quiable: yes (timer stop; `Persistent=true` defers the daily snapshot to the next start).**
3. **`plocate-updatedb.timer` (daily 00:18, inside the window — `systemctl list-timers`)** — `/etc/plocate.ignore` does not exist (verified: `ls -l` → No such file), so `updatedb` walks every mounted filesystem, including the 2.15T pool. The 18:50:57 post-reboot run rebuilt `/var/lib/plocate/plocate.db` (23,161,218 bytes, i.e. ~hundreds of thousands of indexed entries, consistent with the `photos`/`music` datasets) in 3s on a warm cache (`journalctl -u plocate-updatedb.service`). The nightly 00:18 run walks the same tree from a cold cache: real, scattered HDD reads. **Quiable: yes (timer stop) — not in the plan's target list; recommended addition to `QUIET_SYSTEMD_UNITS`.**
4. **Jellyfin playback (user watching TV)** — the dominant potential pool reader in the window, and **not quiable by design** (PM decision: playback must keep working). Not a background source; listed so the gate reasoning is complete.
5. **EPGStation recording — eliminated (A2 resolved, no trade-off).** `reserve` table: 0 rows; `recorded` table: 0 rows (read-only `SELECT COUNT(*)` via `kubectl exec deploy/mariadb -- mysql -u epgstation`, password supplied through the mysql client's stdin password prompt, never on argv, never printed). The only file on disk is one 2026-04-20 recording (`find /mnt/vector/tv -type f -printf '%TY-%Tm-%Td %TH:%TM %p\n' | sort -r | head -8`); no files modified in `/mnt/vector/tv` or `/mnt/vector/live_shows` in the last 24h (`find ... -mtime -1` → empty). The only epgstation activity in 12h is the 10-min `all reservation update` DB sync (NVMe).
6. **Tube Archivist — not a pool source.** Its `/youtube` hostPath targets `/mnt/mediapool/youtube`, which does not exist on this host (`ls -ld /mnt/mediapool` → No such file; the pool mounts at `/mnt/vector`), so TA writes stay on the NVMe. 6h of logs show only celery beat hourly restarts, `thumbnail_check`, `backend_cleanup`.
7. **Navidrome** — reads `/mnt/vector/music` only during playback/library scan (no periodic scanner timer found in the host's `systemctl list-timers`).
8. **Other host timers** (`systemctl list-timers --all`): `dnf-makecache` (20:20, ran 20:20:30), `logrotate` (00:31), `unbound-anchor` (00:00), `sysstat-collect` (10-min), `sysstat-rotate/summary` (00:00/00:07), `fstrim` (Mon 00:24), `tmpfiles-clean`, `raid-check` (weekly, no md raid present) — all NVMe or negligible for the pool. No `media-sync.timer` (module 13 never applied), consistent with the plan.

**Measurement:** `grep -E ' sd[a-z]+ ' /proc/diskstats` snapshots at 20:14:32, 20:27:54 and 20:3x show **identical sda/sdb counters** — zero I/O to the media pool for 13.5+ minutes, spanning the 20:00 hourly event. Lifetime counters since the ~18:14 reboot: ~155MB read / ~13MB written to the pool (boot-time jellyfin library validation + the 18:50 plocate warm-cache walk). **Interim conclusion:** every scheduled pool I/O source in the window is either negligible (4s scan) or once-a-day (~00:00 sanoid, ~00:18 plocate), all quiable; the user's hypothesis "Jellyfin (container)" is confirmed as the *scan* source but the scan itself is 4 seconds, and playback is the only large pool reader and is out of scope by the PM decision. The formal in-window top-of-hour sample straddling 22:00 (below) records the per-process evidence.

**Pod-process visibility (methodology fact):** `ps -o pid,ppid,uid,user,etime,comm -p 13016,13455,14440` + `cat /proc/<pid>/cgroup` show the jellyfin server (PID 13016, UID 1000) and elasticsearch JVMs (13455/14440) in `kubepods.slice/...` cgroups, visible in the host PID namespace on this node. This is what makes host-level `pidstat -d` attribution valid here.

**Exact commands run (remote, as `howard@192.168.1.107`; all read-only; no sudo was ever needed, A6 resolved):**
- Identity: `hostname`; `head -3 /etc/os-release`; `kubectl get nodes -o wide`; `kubectl get pods -A --no-headers | head -40`
- Tooling/baseline: `command -v pidstat iotop`; `grep -E ' sd[a-z]+ ' /proc/diskstats` (3 times); `pidstat -d 5 12` (60s post-20:00 sample)
- Process identity: `ps -o pid,ppid,uid,user,etime,comm -p 13016,13455,14440`; `cat /proc/13016/cgroup /proc/13455/cgroup /proc/14440/cgroup`
- Storage: `zpool status`; `zfs list -o name,mountpoint,used | head -25`; `zfs list -t snapshot -o name,creation | tail -15`; `df -h /var/lib/project-tv /mnt/vector`
- Scheduled: `systemctl list-timers --all --no-pager | head -30`; `kubectl -n project-tv get cronjobs`; `kubectl -n project-tv get cronjob jellyfin-library-refresh -o jsonpath='{.spec.schedule} {.spec.suspend} {.spec.concurrencyPolicy}'`; `kubectl -n project-tv get jobs -o wide`
- Components: `kubectl -n project-tv logs deploy/jellyfin --since=12h --tail=2000 | grep -iE 'scanning|refresh|library' | tail -25`; `journalctl -u sanoid.service --since "12h ago" --no-pager | tail -25`; `journalctl -u plocate-updatedb.service --since "18:00" --no-pager | tail -12`; `kubectl -n project-tv logs deploy/epgstation --since=12h --tail=3000 | grep -iE 'record' | tail -20`; `kubectl -n project-tv logs deploy/epgstation --since=2h --tail=3000 | grep -E '2026-09-07 20:' | tail -15`; `kubectl -n project-tv logs deploy/tubearchivist --since=2h --tail=300 | tail -15`; `kubectl -n project-tv logs deploy/tubearchivist --since=6h --tail=2000 | grep -iE 'download|process|import' | tail -10`
- Topology: `lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINT`; `cat /proc/diskstats`; `cat /etc/sanoid/sanoid.conf`; `stat -c '%y %n' /etc/sanoid/sanoid.conf`; `cat /etc/plocate.ignore` (→ no such file); `ls -la /var/lib/plocate/`; `ls -ld /mnt/mediapool /mnt/mediapool/youtube`; `df -h /mnt/mediapool`
- Volume maps: `kubectl -n project-tv get deploy jellyfin -o jsonpath='{range .spec.template.spec.volumes[*]}{.name}={.hostPath.path}{"\n"}{end}'`; same for `epgstation`
- File activity: `find /mnt/vector/tv /mnt/vector/live_shows -type f -mmin -120 | head -15`; `find /mnt/vector/tv /mnt/vector/live_shows -type f -mtime -1 | head -15`; `find /mnt/vector/tv -type f -printf '%TY-%Tm-%Td %TH:%TM %p\n' | sort -r | head -8`; `ls -lt /mnt/vector/tv | head -8`
- **Extension of section 5 (recorded, per A2):** read-only MariaDB queries inside the mariadb pod to answer "is anything scheduled to record tonight": `kubectl -n project-tv get secret mariadb-secret -o jsonpath=...` (values kept in remote shell vars, never printed), then `printf '%s\n' "$PW" | kubectl -n project-tv exec -i deploy/mariadb -- mysql -u epgstation -p epgstation -e '...'` running only `SHOW TABLES`, `SHOW COLUMNS FROM reserve; SHOW COLUMNS FROM recorded`, `SELECT COUNT(*) FROM reserve`, `SELECT COUNT(*) FROM recorded`, and column-limited `SELECT ... LIMIT` on `reserve`/`recorded`. No `INSERT/UPDATE/DELETE/CREATE/ALTER/DROP` anywhere.
- **Credential handling:** the howard password was passed only as `SSHPASS` env to `sshpass -e`; the MariaDB password only via the mysql client's stdin password prompt; neither value appears in any command line, file, or log. Post-hoc `grep -Ff ~/pass.txt` over this doc: run after the final verdict (below).

**Formal in-window sample (22:00 straddle, per plan item 1 section 3):** one remote session from 21:56:26 to 22:02:46 JST: `grep -E ' sd[a-z]+ | nvme' /proc/diskstats` (T0), `pidstat -d 5 40` (samples 21:56:31-22:00:50, straddling the 22:00:00 CronJob + sanoid firing), `iostat -xd 20 10`, diskstats (T1), `kubectl -n project-tv get jobs -o wide`, `journalctl -u sanoid.service --since "21:59"`. Raw output preserved on the team host at `/tmp/opencode/task-0020-pidstat-2200.txt` (289 lines, not committed, no credential material).
- `pidstat`: exactly four processes had any I/O in any of the 40 samples, all UID 1000: `jellyfin` (avg 4.32 kB/s **writes**, its SQLite/log state on the NVMe), two `java` (elasticsearch JVMs, ~0.7 kB/s writes), `rustdesk` (0.32 kB/s). **Zero `kB_rd/s` in every sample.** No sanoid, zfs, plocate, or job-pod process appeared: the 22:00 sanoid run (journal: started 22:00:00, `taking snapshots...`, deactivated in <1s, no snapshot taken) and the 22:00 refresh job (`jellyfin-library-refresh-29813100`, Complete, 4s) produced no measurable pool I/O.
- `iostat` intervals 2-10 (21:57:04-22:00:50, covering 22:00:00 exactly): sda and sdb **all zeros** (0 r/s, 0 w/s). The first interval is the since-boot average (boot ~18:14), not a burst. NVMe carried all background writes (9-26 w/s, ES/mariadb/jellyfin state).
- diskstats T0 (21:56:26) → T1 (22:02:46): sda/sdb counters **identical** — zero pool I/O across the hourly event.
- **Cross-window delta (the finding that explains the user's complaint):** 20:27:54 → 21:56:26 sda read counters moved 303048 → 797576 sectors = **~253MB of reads, zero writes** to the pool in 88 min. The only pool readers are media playback, trickplay generation (writes would follow; there were none) and the 4s scan (too small). Conclusion: **media playback dominated the pool's I/O in the observation window**; the scheduled sources contributed ≈0 (4s scan) or are once-daily (~00:00 sanoid, ~00:18 plocate). Quiet hours cannot silence playback by design (PM decision); they silence exactly the scheduled residue, which is what the mechanism targets.

**Gate verdict: PASS.** Identity gate PASS (above). I/O gate PASS: the top-3 *scheduled* HDD I/O sources in the 20:00-07:00 window are (1) `jellyfin-library-refresh` CronJob scan — quiable via CronJob `suspend`, (2) `sanoid.timer` — quiable via timer stop (daily ~00:00 pass is the only real snapshot I/O; `Persistent=true` defers it to the next start), (3) `plocate-updatedb.timer` — quiable via timer stop (**add to `QUIET_SYSTEMD_UNITS`**, the gate's extension clause). No STOP condition: no source is only stoppable by breaking playback/recording (recording is inactive — 0 reservations, 0 history, last file on disk 2026-04-20; playback is out of scope by the PM decision, and the mechanism never touches the streaming path). **Target list for implementation: `QUIET_K8S_CRONJOBS="jellyfin-library-refresh"`, `QUIET_SYSTEMD_UNITS="sanoid.timer plocate-updatedb.timer"`.**
**Assumptions resolved:** A1 PASS (IP discrepancy → Vector doc fix), A2 no trade-off (recording inactive), A3 `sshpass` present at `/usr/bin/sshpass`, A5 host TZ is JST (no DST), A6 no sudo was ever needed — all reads succeeded as `howard` directly.
**Credential audit:** `grep -Ff ~/pass.txt planning/docs/TASK-0020-quiet-hours.md` → no match (pattern-from-file, run 2026-09-07 after the sample); raw sample file also checked clean. The howard password and the MariaDB password appear in no command line, file, commit, or log. Item 1 complete; production host was not modified in any way (only read-only commands, per the list above).

**Item 2 — mode-bit restore + branch (2026-09-07):**
- `git fetch origin` on the checkout showed `origin/main` had moved `c520226` → `b892a70` during item 1 (one new upstream commit, `b892a70` "Add TO DO section to English and Japanese READMEs", touching only `README.md` and `docs/ja/README.md`, +6 lines each). The branch was therefore cut from the new tip `b892a70`, per the plan's "from `origin/main`".
- `chmod +x` on the 7 files (`install.sh`, `test/run_tests.sh`, `test/scripts/test_installer.sh`, `test/scripts/test_k8s_apps.sh`, `test/scripts/test_rpm_install.sh`, `test/scripts/test_zfs.sh`, `drivers/px4_drv/build_rpm.sh`) restored the 755 bits; `git status --short` and `git diff --stat` are empty afterwards (tree == HEAD, zero content diff, guards satisfied).
- Branch `task-0020-quiet-hours` created from `origin/main` (b892a70); local `main` left untouched.
- `bash test/scripts/test_installer.sh <repo>` in-tree (full suite, local file checks only): **11/12**. B-01 (`install.sh` executable) **ok** — item 2 acceptance met. **B-11 fails, pre-existing at upstream tip (not caused by this task):** `manifests/prometheus/rbac.yaml` is a valid multi-document YAML (3 docs: ServiceAccount, ClusterRole, ClusterRoleBinding; `grep -c '^---'` → 2), but B-11 validates with single-document `yaml.safe_load` → `ComposerError: expected a single document in the stream`; `yaml.safe_load_all` parses all 3 docs cleanly. Harness bug, recorded for item 5b: a 2-token fix (`safe_load(open(...))` → `list(safe_load_all(open(...)))`) is applied there so item 9's regression run reports true 12/12; that is a scope extension, recorded here so the reviewers see it.

**Item 3 — core script `quiet-hours/quiet-hours.sh` (2026-09-07):**

**Alternatives considered**
- *Timezone resolution: frozen at source time vs per-call.* Chosen per-call (`local_tz_hour` helper inside `desired_state_at`), because a frozen value computed once when the file is sourced goes stale when the environment changes (the smoke test's TZ-switching cases proved it), and the helper is the single place that can implement the empty-TZ rule below.
- *Empty-TZ handling.* Chosen: pass `TZ` to `date` **only when non-empty**. Empirically verified on the team host (glibc): with `/etc/localtime` → Asia/Tokyo and `TZ` unset, `TZ= date` returns **UTC**, not local time, and `TZ=JST` (bare abbreviation) also returns UTC. A frozen empty `TZ=` prefix would have run the whole window math in UTC on a JST host (9 h off). Only `TZ` unset or a valid IANA zone gives the system local time, hence the conditional.
- *Job-name filtering: `kubectl get jobs -o name | grep "^<cronjob>-"` vs bash prefix match.* Chosen pure bash `[[ "$job" == "${name}-"* ]]` per the pipefail/`grep -q` SIGPIPE trap (`CLAUDE.md:170-173`); `--ignore-not-found` keeps the step idempotent for next-tick retries when a job completes between list and delete.
- *State-file semantics on missing/invalid file: hard error vs "unknown".* Chosen "unknown": a fresh install (installer runs the service once to seed it) or a deleted file degrades to one extra idempotent transition run, never to a crash. The file still only advances on full transition success, per the plan.
- *Config parse: `source` the file vs explicit KEY=VALUE loop.* Chosen explicit loop (no code execution from config, interior spaces in list values preserved, per-key validation; unknown keys logged and skipped for forward compatibility; invalid known values fail the whole load so a garbage hour can never silently corrupt the window).

**Design (as implemented):** `load_config` (validates 0-23 with `10#` to kill the 08/09 octal trap), `hour_in_window` (start inclusive / end exclusive; `start==end` → full 24 h; wrap via set membership, no arithmetic across the wrap — this is what makes DST correct: a repeated wall-clock hour is quiet twice, a skipped hour never occurs), `desired_state_at <epoch>` (enabled → override → window; unresolvable clock fails soft to loud; always returns 0), `read_state`/`write_state` (atomic tmp+mv; "loud"/"quiet"/"unknown"), `cronjob_set_suspend` / `cronjob_delete_inflight_jobs` / `unit_set` (per-step; kubectl/systemctl stderr captured into the journal log line), `apply_quiet` / `release_quiet` (every step runs even after a failure; rc=0 only when all succeeded — the only case `main` advances the state file), `main` (always `exit 0`). Sourcing guard `[[ "${BASH_SOURCE[0]}" == "$0" ]]` makes the file side-effect-free when sourced (acceptance criterion). Env overrides: `QUIET_HOURS_CONF`, `QUIET_HOURS_STATE`, `QUIET_HOURS_NAMESPACE`, `QUIET_HOURS_TZ`.

**Checks run (item 3):** `bash -n` PASS · smoke suite `/tmp/opencode/qh-smoke.sh` (team host, not committed) **71/71 ok**: window matrix (20-07 wrap 11 in / 13 out, 10-14 no-wrap, 10-10 degenerate full-24h), boundary inclusivity (start in, end out), config parse (valid/missing/invalid hour/invalid flag/`09` no-octal), DST fixed-epoch cases (America/New_York 2026-03-08 spring + 2026-11-01 fall incl. both passes of 01:30 and post-rollback 07:00; Europe/Berlin 2026-03-29 spring + 2026-10-25 fall incl. both passes of 02:30; Asia/Tokyo control), override/enabled flags, and the full state machine with stubbed `kubectl`/`systemctl` (fresh in-window tick applies quiet + issues `suspend:true`/stop of both units; already-quiet tick is a no-op; outside-window tick releases; **failed systemctl step → exit 0 and state file NOT written**; reboot simulation re-applies; override outside window). The smoke run also caught and proved fixed the frozen-TZ and empty-TZ bugs above. No secret material in the file (pure logic; re-verified in item 9).

**Changes**

| File | What changed |
|---|---|
| `quiet-hours/quiet-hours.sh` (new) | Core state machine: window calc, config parse, state machine, per-step fail-soft apply/release, env-overridable paths |
| (project checkout, working tree) | 7 files mode-only 644 → 755 (restored to HEAD state, zero content diff); branch `task-0020-quiet-hours` cut from `origin/main` b892a70 |
| (none in the team repo yet — planning doc updates only) | |

**Checks run:** `bash -n` on `quiet-hours.sh` PASS · smoke suite 71/71 (see above) · `test_installer.sh` in-tree 11/12 (B-01 ok; B-11 pre-existing harness bug, evidence above) · credential audit clean (`grep -Ff ~/pass.txt` on this doc and on the raw sample file)

**Item 4 — CLI + systemd units (2026-09-08):**

**Alternatives considered**
- *Where the CLI resolves the core script.* Chosen: `QUIET_HOURS_LIB` env override, then the installed path `/usr/local/lib/project-tv/quiet-hours.sh`, then the repository layout next to the CLI (`$(dirname BASH_SOURCE)/quiet-hours.sh`). Option B (hardcode the installed path only) rejected: the structural test (item 5b H-CLI) runs `bash quiet-hours/project-tv-quiet-hours usage` from the checkout on a host with nothing installed, and would fail.
- *Root requirement.* Chosen: `usage`/`help`/no-arg run without root; `status`/`enable`/`disable` call `require_root`. The structural test invokes the CLI as the unprivileged team-host user, so the usage path must not demand root. Option B (all commands root) rejected on that ground; Option A keeps the three mutating/state-reading commands root-only, matching the plan ("Override CLI `/usr/local/bin/project-tv-quiet-hours` (root)").
- *How the override flag is written.* Chosen: line-by-line rewrite that replaces the single `^QUIET_OVERRIDE=` line (appending it if absent), preserving every other line verbatim, then atomic `tmp`+`mv` with `chmod 0644`. The config is data, never executed, so it is rewritten not sourced. Option B (`sed -i` in place) rejected: a full rewrite is easier to reason about for a 6-key file and guarantees the surrounding comment block and key order survive a repeated enable/disable.
- *Immediate-apply path.* Chosen: `systemctl start` the one-shot service; if the unit is absent, run the core script directly (exactly what the service does); if that also fails, warn and let the 15-minute tick pick the change up. The core script always exits 0 (fail-soft), so a non-zero return here means the change could not be applied at all.
- *Units.* Chosen: service is `Type=oneshot` with `ExecStart=/usr/local/lib/project-tv/quiet-hours.sh`, `After=`/`Wants=network-online.target` so the k8s steps have a chance to reach the API server at boot (a not-ready cluster fails soft and the timer retries). Timer is `OnBootSec=2min` (boot run), `OnCalendar=*:0/15` (15-min cadence, the same calendar form module 12 already uses), `Persistent=true` (catch missed runs, same as `sanoid.timer`), `WantedBy=timers.target`.

**Design (as implemented):** `quiet-hours/project-tv-quiet-hours` sources the core script for `load_config`/`desired_state`/`read_state`/`local_tz_*` (sourcing is side-effect free because the core guards `main` on `BASH_SOURCE`), then dispatches `status`/`enable`/`disable`/`usage`. `status` prints config path, window, enabled, override, targets, local time, desired vs applied state, an in-sync line, and a next-transition hint computed by stepping candidate epochs so it stays sane across DST. `enable`/`disable` rewrite the flag via `set_override` and call `trigger_now`. `quiet-hours/project-tv-quiet-hours.{service,timer}` as above.

**Checks run (item 4):** `bash -n project-tv-quiet-hours` PASS · `bash project-tv-quiet-hours usage` → rc 0, output contains `20:00-07:00` (grep count 1) · no-arg → usage rc 0 · `bogus` → rc 1 · `status` as non-root → rc 1 with "must be run as root" (root gate works) · service and timer contain the required sections (verified by item 5b H7/H8).

**Item 5a — TAP unit tests `test/scripts/test_quiet_hours.sh` (2026-09-08):**

**Alternatives considered**
- *Driving `main` with a controlled clock.* Chosen: a bash `date()` wrapper that intercepts only the exact `date +%s` call (returning `FAKE_NOW`) and passes everything else to `command date`, plus running each state-machine case as `( main )` in a subshell. Option B (inject a clock function the core calls) rejected: the core (item 3) is already written and its `desired_state` hardcodes `date +%s`; the wrapper is the least invasive way to freeze time without touching the core. The subshell is required because `main` ends in `exit 0`, which would otherwise kill the test process.
- *Stubbing the executors.* Chosen: redefine `kubectl()` and `systemctl()` as bash functions that append every invocation to a log file (and `systemctl` honours `STUB_FAIL_UNIT` to simulate a failing step). Bash function lookup shadows the real binaries, so no PATH manipulation is needed. Option B (fake binaries on `PATH`) rejected: functions are simpler and the log file gives a precise assertion target for "which commands would have run".
- *TAP cleanliness.* Chosen: after sourcing the core, redefine `log() { :; }` so the core's journal lines never leak into the TAP stream (only `ok`/`not ok` lines and `#` diagnostics are emitted).

**Design (as implemented):** 94 checks in eight sections. A window matrix (wrap 20-07: 11 in / 13 out; no-wrap 10-14; degenerate 10-10 full day). B boundary inclusivity named (start in, end out). C DST/fixed-epoch correctness with real glibc `date` under `QUIET_HOURS_TZ`: America/New_York 2026-03-08 spring-forward (incl. "skipped hour 02 never occurs") and 2026-11-01 fall-back (both passes of 01:30 quiet); Europe/Berlin 2026-03-29 spring and 2026-10-25 fall (both passes of 02:30 quiet); Asia/Tokyo no-DST control. D config parse (valid six-key, missing file rc 1, hour 24 rc 1, `09` → decimal 9, unknown key skipped, flag 2 rc 1, quoted list keeps interior spaces). E state machine with stubs + fake clock (fresh in-window tick applies quiet + advances state; already-quiet no-op; outside-window release; failed step → exit 0 and state NOT written; reboot-with-override re-applies outside window; corrupt config → no actions and state untouched; disable override → release). F enabled/override precedence. G state-file round-trip + garbage/missing → unknown, no tmp left. H structural (see item 5b).

**Checks run (item 5a):** first in-tree run 87/94, 7 failures — all in H (module 21 and install.sh wiring not yet written, expected) plus one real bug: C-NY-spring check 33 failed because the test overwrote `E_EPOCH` (06:30 UTC) with 07:30 UTC before the check ran. Fixed by deleting the stray duplicate assignment (test bug, not core bug — the core was never at fault). After item 6 landed, full in-tree run is 94/94 (see Final regression below).

**Item 5b — structural tests + harness wiring (2026-09-08):**
- Structural section H appended to `test_quiet_hours.sh`: module 21 file exists and defines `run()`; `install.sh` has `MODULE_DESC[21]` and `MODULE_ORDER` ending in 21; all four quiet-hours deliverables present; service unit has `[Unit]`/`[Service]`, `Type=oneshot`, correct `ExecStart`; timer unit has `[Unit]`/`[Timer]`/`[Install]`, `OnBootSec=`, `OnCalendar=*:0/15`, `WantedBy=timers.target`; `bash -n` on all seven changed files; CLI usage output shows `20:00-07:00`; `run_tests.sh` invokes `test_quiet_hours.sh`.
- `test/run_tests.sh`: one invocation block added (same `ssh … | tee "$RESULTS_DIR/*.tap"` shape as the neighbours, at `test/run_tests.sh:105-107`), so the VM run picks the suite up automatically; the existing `scp -r "$SCRIPT_DIR/scripts/"` at `test/run_tests.sh:88` already copies the new script into the VM.
- B-11 harness fix applied (the 2-token scope extension recorded in item 2): `test/scripts/test_installer.sh:119` `yaml.safe_load(open('$yaml'))` → `list(yaml.safe_load_all(open('$yaml')))`, so the multi-document `manifests/prometheus/rbac.yaml` (3 docs) parses. This is what takes `test_installer.sh` from 11/12 to a true 12/12.

**Item 6 — installer module 21 + install.sh wiring (2026-09-08):**

**Alternatives considered**
- *Decline path.* Chosen: on "no" the module calls `set_module_status "21" "skipped"` and returns 0, and `install.sh` `run_module` was changed to preserve an explicit `skipped` mark instead of clobbering it with `completed`. Option B (module returns 1 to force a non-completed state) rejected: `run_module` maps any non-zero to `failed`, which is the wrong label for a user decline. Option C (leave `run_module` as-is, accept `completed`) rejected: the plan's acceptance is "decline path marks the module skipped", and `show_status` would display `[OK]` for a feature the user turned off. The `run_module` change is minimal and only preserves a status the module set deliberately; no other module sets `skipped`, so existing behaviour is unchanged.
- *Which targets go in the config.* Chosen: the module detects what is actually present (`systemctl cat <unit>` for `sanoid.timer`/`plocate-updatedb.timer`, `kubectl get cronjob jellyfin-library-refresh` in `$K8S_NAMESPACE`) and writes only those into `QUIET_SYSTEMD_UNITS`/`QUIET_K8S_CRONJOBS`. Option B (always write the plan's fixed target list) rejected: naming a unit or CronJob that does not exist makes that step fail every tick, which blocks the state file from advancing and turns a host without sanoid into a permanently half-quiet, log-spamming system. Detection is defensive, not a behaviour change: on the reference host both units and the CronJob are present, so the installed config matches the plan's target list exactly.
- *kubectl-missing path.* Chosen: warn and skip the k8s target, module completes (plan: "If `kubectl` is missing it warns and skips the k8s targets (fail-soft, module completes)"). If neither a unit nor the CronJob is found, warn and install with an empty target list (inert until a target is added) rather than failing the module.
- *start==end.* Chosen: re-prompt loop around `ask_number` (the helper validates range but not cross-field equality).

**Design (as implemented):** `modules/21-quiet-hours.sh` `run()`: explains the behaviour, `ask_yes_no` to enable, prompts start hour (0-23, default 20) and end hour (0-23, default 7, exclusive) with a start==end re-prompt, detects present targets, `install -m 0755` the core script and CLI, `install -m 0644` the two units, writes `/etc/project-tv/quiet-hours.conf` (0644) with the chosen window and detected targets, `systemctl daemon-reload`, `systemctl enable --now project-tv-quiet-hours.timer`, one-shot `systemctl start project-tv-quiet-hours.service` to seed the state file, prints a summary with the three override commands. `install.sh` wiring: `MODULE_DESC[21]="Quiet hours (HDD activity)"`, `21` appended to `MODULE_ORDER` (after 20, so k8s and sanoid exist first), module-number prompt widened `(0-20)`→`(0-21)` (`install.sh:241`), and the `run_module` skip-preservation change.

**Checks run (item 6):** `bash -n modules/21-quiet-hours.sh` PASS · structural H1-H4 PASS (module exists, defines `run()`, `MODULE_DESC[21]` present, `MODULE_ORDER` ends 21) · sandboxed functional run of `run()` with stubbed `log_*`/`ask_*`/`systemctl`/`kubectl` (no host writes): decline path returns 0 and marks `21:skipped`; start==end re-prompt fires and then accepts 20/7; k8s target correctly skipped with a warning when the CronJob is absent; empty-target warning fires; install/enable/start sequence emitted in the right order. The module's real `systemctl`/`install` side effects were not executed (would require root on a live host); that is the VM run in item 9, at Big's discretion.

**Final regression (2026-09-08, all on the team host, branch `task-0020-quiet-hours`):**
- `bash -n` on all seven changed files: PASS (`install.sh`, `modules/21-quiet-hours.sh`, `quiet-hours/quiet-hours.sh`, `quiet-hours/project-tv-quiet-hours`, `test/scripts/test_quiet_hours.sh`, `test/run_tests.sh`, `test/scripts/test_installer.sh`).
- `test/scripts/test_quiet_hours.sh "$PWD"`: **94/94 ok**, rc 0 (0 `not ok`).
- `test/scripts/test_installer.sh "$PWD"`: **12/12 ok**, rc 0, including B-01 (install.sh executable) and B-11 (after the multi-doc YAML fix).
- Credential re-audit: `grep -Ff ~/pass.txt` over this doc → no match; over every new/changed task file (`quiet-hours/*`, `modules/21-quiet-hours.sh`, `test/scripts/test_quiet_hours.sh`) → no match. Pattern-from-file, never argv.
- Tree purity: `git status --short` shows only this task's files (`M install.sh`, `M test/run_tests.sh`, `M test/scripts/test_installer.sh`, `?? modules/21-quiet-hours.sh`, `?? quiet-hours/`, `?? test/scripts/test_quiet_hours.sh`). `git diff --summary` on the 7 mode-bit files is empty (no mode or content drift on them). The two test-file `M` entries are this task's content edits (B-11 fix; run_tests.sh line), not the pre-existing mode bits.

**Changes (items 4-6)**

| File | What changed |
|---|---|
| `quiet-hours/project-tv-quiet-hours` (new) | Override CLI: `status`/`enable`/`disable`/`usage`; root-gated mutating commands; atomic flag rewrite; immediate-apply trigger |
| `quiet-hours/project-tv-quiet-hours.service` (new) | oneshot unit running the core script, ordered after network-online |
| `quiet-hours/project-tv-quiet-hours.timer` (new) | 15-min `OnCalendar` + `OnBootSec` boot run, `Persistent=true` |
| `test/scripts/test_quiet_hours.sh` (new) | 94 TAP checks: window/DST/config/state-machine unit tests + structural section H |
| `test/run_tests.sh` | One added invocation block for `test_quiet_hours.sh` (VM run) |
| `test/scripts/test_installer.sh` | B-11 multi-document YAML fix (`safe_load` → `list(safe_load_all(...))`) |
| `modules/21-quiet-hours.sh` (new) | Installer module: prompts, target detection, install, config, enable+seed |
| `install.sh` | `MODULE_DESC[21]`, `MODULE_ORDER` +21, prompt range `(0-21)`, `run_module` preserves an explicit `skipped` mark |

**Checks run (items 4-6):** `bash -n` 7/7 PASS · `test_quiet_hours.sh` 94/94 · `test_installer.sh` 12/12 · credential audit clean on doc and all task files · `git status --short` contains only this task's files · 7 mode-bit files show no mode/content drift.

**Competing priorities:**
- *B-11 fix is a scope extension.* It changes a pre-existing harness line, not quiet-hours behaviour. Recorded in item 2 and applied here so item 9's regression reports a true 12/12; flagged so Shadow/Omega see it is deliberate, not quiet-hours code.
- *`run_module` skip-preservation is a core-installer change.* One guarded branch added to `install.sh` so a declined optional module reads `skipped`, not `completed`. Traded a small change to shared installer logic for an honest status display; no other module is affected.
- *Module 21 detects targets rather than hardcoding the plan list.* Slightly more code at install time, in exchange for a config that never names a missing unit/CronJob (the failure mode that would otherwise leave a sanoid-less host permanently half-quiet). On the reference host the detected set equals the plan's list, so the installed config is identical.

**Item 10 — fix round for the review findings (2026-09-08, team host, branch `task-0020-quiet-hours`, tree uncommitted)**

Closed all nine open findings (Shadow's 4 should-fix + 3 nits, Omega's 2 low) plus Big's two
items, each with a `Resolution:` line and sha. The tree is uncommitted, so the shas are
`git hash-object` of the working-tree files (item 12's release commit supersedes them); the
changes table carries the full shas.

**Alternatives considered**

- *Namespace persistence: config key vs service drop-in.* Chosen the config key
  (`QUIET_K8S_NAMESPACE`, honoured by `load_config`), because it is one source of truth the CLI
  `status` can display and a later edit of the CronJob list in the config stays consistent with
  its namespace; the drop-in would fork the truth into two files that could drift.
- *Namespace precedence.* Chosen: env `QUIET_HOURS_NAMESPACE` (test-suite override) > config
  key > default `project-tv`, implemented with a provenance marker (`QUIET_HOURS_NAMESPACE_ENV`)
  captured at source time, so `load_config` never clobbers a test override. Option B (re-source
  the core per test case) rejected: heavier, and the marker keeps the precedence explicit in one
  place.
- *In-place upgrade: one suggested direction vs both.* Chosen both: `init_status` backfill
  (root fix; `main` calls it before every menu/status path) and `get_module_status` totality
  (missing line → `pending`, rc 0). Backfill alone would still let a hand-edited file kill the
  installer; totality alone would leave `set_module_status` (a sed substitution) unable to ever
  record module 21, so it would display as pending forever.
- *Allowlist character sets.* Omega's proposed classes accept the attack token itself
  (`--foo` matches both `[a-z0-9-]+` and `[A-Za-z0-9._:@-]+`), so CronJob names use the full
  DNS-1123 label form (alphanumeric first and last) and unit names must not start with a dash.
  Recorded in the `## Security` Resolution as a deliberate refinement.
- *Module testability.* Chosen a module-specific `QUIET_HOURS_CONF_PATH` override rather than
  reusing the core's `QUIET_HOURS_CONF`: the module runs inside `install.sh` where the user's
  environment is uncontrolled, and coupling the installer to the runtime test variable would let
  a stray env var redirect the installed config.
- *Regression-test answer scripting.* `ask_number` is scripted through a file (one answer per
  line, `sed -i 1d`), because the module reads each answer in a `$(...)` subshell: a variable
  counter never advances and the re-prompt loop runs forever. Found while verifying this round
  (the first sandbox attempt hung until the 120 s tool timeout). An exhausted queue yields an
  empty answer, which aborts the module's `10#` arithmetic instead of looping.

**Changes**

| File | `git hash-object` | What changed |
|---|---|---|
| `install.sh` | `d6bdc59a` | `init_status` backfills missing `MODULE_ORDER` entries into an existing status file; `get_module_status` is total (missing line → `pending`, rc 0) |
| `modules/21-quiet-hours.sh` | `205554f6` | `10#` start==end comparison + post-loop normalisation; `QUIET_OVERRIDE` carry-over with summary note; `QUIET_K8S_NAMESPACE` written into the config; `QUIET_HOURS_CONF_PATH` test hook; both `mkdir -p` routed through `log_cmd` |
| `quiet-hours/quiet-hours.sh` | `0ad1fdb0` | namespace provenance + `QUIET_K8S_NAMESPACE` key handling in `load_config`; allowlist validation for both target lists and the namespace (fails the whole load, like an invalid hour) |
| `quiet-hours/project-tv-quiet-hours` | `e81b634d` | `CORE_PATH` recorded in `load_core` and executed by `trigger_now` (with a `-f` guard); dead `now_hour` deleted; `status` prints the resolved namespace |
| `test/scripts/test_quiet_hours.sh` | `569befc3` | new section I: 24 regression checks (all 4 should-fix scenarios, Omega low 1, all 3 nits); plan `1..94` → `1..118` |
| `test/scripts/test_installer.sh` | `ad185f7e` | B-11 path via `sys.argv[1]` (no string interpolation); `[[ "$FAIL" == "0" ]]` exit code |

`test/run_tests.sh` is unchanged this round: once `test_installer.sh` tells the truth, its
`set -euo pipefail` + `ssh | tee` pipeline fails fast by design, so no orchestrator change was
needed.

**Checks run (all on the team host, 2026-09-08):**
- `bash -n` on all 7 changed files: 7/7 PASS.
- shellcheck 0.10.0 `-S warning` on the same 7 files: no new findings; the only remaining hits
  are the two already classified in `## Review` (SC1090 dynamic source in `install.sh`, SC2120
  on `load_config` — the test suite passes arguments from another file); SC2034 (`now_hour`) is
  gone. Two warnings introduced mid-round (SC2034 on a dead `QUIET_K8S_NAMESPACE` global,
  2× SC1007 on empty-env prefixes in the test) were found and fixed before the final run.
- `test/scripts/test_quiet_hours.sh "$PWD"`: **118/118 ok**, rc 0, plan `1..118` matches,
  0 `not ok` (was 94/94 pre-fix; +24 = section I). TAP kept at
  `/tmp/opencode/task0020-quiet-hours-item10.tap` (team host, not committed).
- `test/scripts/test_installer.sh "$PWD"`: **12/12 ok**, rc 0. Exit-code fix demonstrated:
  empty-directory run → 9 `not ok`, **rc 1** (previously 0). TAP kept at
  `/tmp/opencode/task0020-installer-item10.tap`.
- Hand verification of the in-place upgrade: a status file with entries 00-20 →
  `get_module_status 21` rc 0 `pending`; `init_status` backfills exactly one `21:pending`;
  `set_module_status 21 completed` round-trips; the call survives under `set -e`.
- Hand verification of the module sandbox (the same stubs section I uses): 7/07 re-prompt fires
  once and the config gets normalised 7/8; a re-run carries `QUIET_OVERRIDE=1` and prints the
  carry-over note; `K8S_NAMESPACE=media` lands in the config and in the kubectl detection call;
  both mkdirs appear in the `log_cmd` record.
- Credential audit: `grep -Fqf ~/pass.txt` over the 7 task files and this doc: clean.
- Tree purity: `git status --short` shows only this task's paths (`M install.sh`,
  `M test/run_tests.sh`, `M test/scripts/test_installer.sh`, `?? modules/21-quiet-hours.sh`,
  `?? quiet-hours/`, `?? test/scripts/test_quiet_hours.sh`); `git diff --summary` empty (no
  mode-bit drift).

**Competing priorities:**
- *The blob shas are provisional.* They identify the working-tree content exactly, but item
  12's commit supersedes them; every `Resolution:` line says so.
- *`QUIET_HOURS_CONF_PATH` is a new env var.* Small production surface (a user who exports it
  redirects the module's config write) in exchange for a sandboxable module; the core/CLI
  already expose `QUIET_HOURS_CONF` with the same property.
- *Strict allowlist.* A hand-edited config with a token outside the allowlist now fails the
  whole load and the state machine fails soft to the current state (the documented contract),
  with a journal line naming the bad value. Chosen strictness over leniency: the tokens go to
  root `systemctl`/`kubectl`.
- *The section I module sandbox does not exercise real `install`/`systemctl` side effects*
  (the `log_cmd` stub records without executing). Those remain covered only by the full VM run,
  which stays an open release gate (no VM on the team host at Big's run).

---

## Review

*Owner: `Shadow`. Read-only — findings only, no edits. Severity order, blockers first.*

Reviewed 2026-09-08: diff against b892a70 plus the untracked `quiet-hours/`,
`modules/21-quiet-hours.sh`, `test/scripts/test_quiet_hours.sh` on branch
`task-0020-quiet-hours`. Verified in this review: `bash -n` 7/7 PASS on all changed files (run on
the team host); `shellcheck` on the same files (the only actionable hit is folded into the nits
below; SC2120/SC2119 are false positives, the test suite passes arguments); tree purity matches
`## Implementation` (`git status` shows exactly the 3 modified + 3 untracked task paths); the TAP
plan `1..94` matches 94 check sites counted statically in `test_quiet_hours.sh`; the DST
fixed-epoch cases in section C were re-derived against the 2026 US/EU transition dates and are
correct. The two flagged scope items are sound: the B-11 `safe_load_all` fix is minimal and
correct (`test/scripts/test_installer.sh:119`), and the `run_module` skip-preservation branch
(`install.sh:103-112`) only preserves an explicit `skipped` mark, leaves the failure path
unchanged, and is safe under `set -e`/`set -u` (conditional context). The core state machine
(`quiet-hours/quiet-hours.sh`) meets the fail-soft contract: per-step isolation, state file
advancing only on full success, atomic tmp+mv writes, and the glibc empty-`TZ` handling are all
correct. No blockers.

### k8s namespace is lost between install and runtime
**Severity:** should-fix
**Where:** `modules/21-quiet-hours.sh:56`; `quiet-hours/quiet-hours.sh:28,97-102`
**Problem:** the module detects the CronJob target in the installer-configurable
`$K8S_NAMESPACE` (`config/defaults.conf:14`), but the config it writes has no namespace key and
the core only reads `QUIET_HOURS_NAMESPACE` from the environment (default `project-tv`), which
the systemd service never sets.
**Failure scenario:** user sets `K8S_NAMESPACE="media"` in `config/defaults.conf` (supported
customization; module 04 creates that namespace) and runs a fresh install. Detection succeeds in
`media` and the CronJob is written into the config. Every tick the core then patches the CronJob
in `project-tv`, where it does not exist: the patch fails, the state file never advances, the
systemd units churn stop/start with a journal line every 15 minutes, and the real CronJob in
`media` keeps scanning hourly. The primary target is never silenced and `status` reports
permanent out-of-sync.
**Suggested direction:** persist the namespace in the config (new key, honoured by
`load_config`) or emit a service drop-in with `Environment=QUIET_HOURS_NAMESPACE=` at install
time, so detection and runtime read the same value.
**Resolution:** fixed in `205554f6` (`git hash-object modules/21-quiet-hours.sh`) + `0ad1fdb0`
(`git hash-object quiet-hours/quiet-hours.sh`), working tree on `task-0020-quiet-hours`
(uncommitted; item 12's release commit supersedes the blob shas). Chose the config key over the
drop-in: one source of truth the CLI `status` can display, and a later config edit of the
CronJob list stays consistent with its namespace. The module writes
`QUIET_K8S_NAMESPACE=${K8S_NAMESPACE}`; `load_config` applies it to `QUIET_HOURS_NAMESPACE`
only when the env var did not set it (precedence: env test override > config key > default
`project-tv`, via a provenance marker captured at source time), and validates it as a DNS-1123
label. Pinned: section I checks "module persists the detection namespace", "detection ran
kubectl in the configured namespace", "core resolves the namespace from the config key",
"env QUIET_HOURS_NAMESPACE wins over the config key", "namespace defaults to project-tv".

### Module re-run silently resets a live override
**Severity:** should-fix
**Where:** `modules/21-quiet-hours.sh:78-90`
**Problem:** re-running the module regenerates `/etc/project-tv/quiet-hours.conf` with
`QUIET_OVERRIDE=0` unconditionally, discarding a live override set by the CLI.
**Failure scenario:** user runs `project-tv-quiet-hours enable` (per the DoD the override
persists until `disable`, including reboots). Later the user re-runs module 21 (a supported
flow; the installer tracks per-module status precisely for re-runs). The config is rewritten
with `QUIET_OVERRIDE=0`, the forced quiet ends with no disable command, and nothing in the
module output mentions it.
**Suggested direction:** read the existing `QUIET_OVERRIDE` from the old config before
overwriting and write it back; mention the carry-over in the install summary.
**Resolution:** fixed in `205554f6` (`git hash-object modules/21-quiet-hours.sh`), working tree
on `task-0020-quiet-hours` (uncommitted). The module reads the old config's last
`QUIET_OVERRIDE=` line before rewriting (only a clean 0/1 is honoured; anything else starts
fresh at 0, matching the core's own flag validation), writes it back, and the summary prints a
"kept on from the previous install" line when it is 1. Pinned: section I checks "re-run carries
a live QUIET_OVERRIDE=1", "re-run applies the new window (20/7)", "mentions the override
carry-over in the summary".

### start==end guard is bypassed by leading-zero input
**Severity:** should-fix
**Where:** `modules/21-quiet-hours.sh:33`
**Problem:** the equality check compares `ask_number` string output, but `ask_number`
(`lib/prompts.sh:82-87`) accepts leading-zero hours ("07" passes its range test as octal 7) and
echoes them verbatim, so "7" and "07" compare as different hours.
**Failure scenario:** user enters start `7` and end `07` (or vice versa). No re-prompt fires,
the config gets start=end=7, and the core treats `start == end` as a full 24-hour window
(`quiet-hours.sh:123-125`). The CronJob stays suspended and sanoid/plocate stay stopped
permanently while the user believes a bounded night window was configured.
**Suggested direction:** normalise both values before comparing, e.g.
`(( 10#$start_hour == 10#$end_hour ))`.
**Resolution:** fixed in `205554f6` (`git hash-object modules/21-quiet-hours.sh`), working tree
on `task-0020-quiet-hours` (uncommitted). The guard now compares
`(( 10#$start_hour == 10#$end_hour ))` exactly as suggested, and both values are additionally
normalised after the loop (`start_hour=$((10#$start_hour))`), so the config holds plain decimal
hours ("07" no longer reaches the config file). Pinned: section I checks "leading-zero input
(7 vs 07) trips the re-prompt" and "config gets the normalised window (7/8, no leading zeros)".

### In-place upgrade kills the installer on the new module number
**Severity:** should-fix
**Where:** `install.sh:76-83` (`get_module_status`), `install.sh:57-63` (`init_status`), call sites `install.sh:128,164,179`
**Problem:** adding `21` to `MODULE_ORDER` exposes a pre-existing trap: when the status file
has no line for a module, `get_module_status` returns grep's rc 1 (the `grep | cut` pipeline
under `set -o pipefail` at `install.sh:9`), and `init_status` only seeds entries when the file
is absent.
**Failure scenario:** a host installed with a pre-TASK-0020 repo has `logs/.install-status`
holding entries 00-20. The user updates the checkout in place and re-runs the installer:
`status=$(get_module_status "21")` (module menu `install.sh:164`, status view `install.sh:128`,
full install `install.sh:179`) hits the missing line and `set -e` exits the installer. Every
use of menu options 2/3 and every full install dies. The new `run_module` branch
(`install.sh:106`) is in a conditional context and is unaffected.
**Suggested direction:** make `get_module_status` return 0 with empty output when no line
matches, or have `init_status` append entries for modules missing from an existing file.
**Resolution:** fixed in `d6bdc59a` (`git hash-object install.sh`), working tree on
`task-0020-quiet-hours` (uncommitted). Both suggested directions applied, because neither alone
closes the finding: `init_status` backfills missing `MODULE_ORDER` entries into an existing
status file (the root fix: `main` calls it before any menu/status path), and
`get_module_status` is now total (missing line reads as `pending` with rc 0, so no call site can
trip `set -e` even if the file is hand-edited later). Note: "empty output" was implemented as
"echo `pending`" instead, because the call sites treat both identically and an explicit status
word keeps the function's contract (always echo a status) intact. Verified by hand: a 00-20
status file upgrades cleanly, `21:pending` is backfilled, `21:completed` round-trips. Pinned:
section I checks "missing status line reads as pending with rc 0", "init_status backfills the
new module into the old file", "status is recorded for the new module after the backfill".

### `now_hour` is dead and can raise an arithmetic error
**Severity:** nit
**Where:** `quiet-hours/project-tv-quiet-hours:157`
**Problem:** `now_hour` is computed but never used (shellcheck SC2034); if
`local_tz_hour` ever returns empty, `$((10#))` raises an arithmetic error to stderr in the
middle of `status` output.
**Failure scenario:** `status` on a host where `date -d` fails (broken `/etc/localtime`):
`bash: 10#: value too great for base` interleaves into the status output; the value is unused
regardless.
**Suggested direction:** delete the variable; `cur_state` already carries the current state.
**Resolution:** fixed in `e81b634d` (`git hash-object quiet-hours/project-tv-quiet-hours`),
working tree on `task-0020-quiet-hours` (uncommitted). Variable and its assignment deleted from
`next_transition`; `cur_state` already carries the state. SC2034 no longer fires (shellcheck
re-run, item 10). Pinned: section I check "dead now_hour is gone from the CLI".

### `trigger_now` fallback ignores the repo-layout core path
**Severity:** nit
**Where:** `quiet-hours/project-tv-quiet-hours:142`
**Problem:** the immediate-apply fallback re-derives the core script as
`${QUIET_HOURS_LIB:-/usr/local/lib/project-tv/quiet-hours.sh}` instead of reusing
`core_script_path`, which also resolves the repository layout next to the CLI.
**Failure scenario:** the CLI is run from a repo checkout on a host with nothing installed
(the exact structural-test layout): `systemctl start` fails (no unit) and the fallback runs
the nonexistent `/usr/local` path, so `enable`/`disable` always end in the 15-minute warning
even though the core script sits next to the CLI.
**Suggested direction:** have `load_core` remember the resolved core path and `trigger_now`
execute it.
**Resolution:** fixed in `e81b634d` (`git hash-object quiet-hours/project-tv-quiet-hours`),
working tree on `task-0020-quiet-hours` (uncommitted). `load_core` records the resolved path in
`CORE_PATH` and `trigger_now` executes it (with a `-f` guard, so a stale `QUIET_HOURS_LIB`
falls through to the 15-minute warning instead of a broken exec), replacing the
`${QUIET_HOURS_LIB:-/usr/local/lib/project-tv/quiet-hours.sh}` literal. Pinned: section I
checks "trigger_now fallback uses the resolved core path (CORE_PATH)" (structural), "runs the
core directly when the unit is absent" and "executed the resolved repo-layout core" (functional
harness: the CLI functions are extracted next to a stand-in core that logs its own path, and a
stubbed `systemctl` refuses the unit).

### Two `mkdir -p` calls bypass `log_cmd`
**Severity:** nit
**Where:** `modules/21-quiet-hours.sh:70,77`
**Problem:** every other state-changing command in the module goes through `log_cmd`; the two
`mkdir -p` calls do not, so the install log has no "Running:" line for them.
**Failure scenario:** `/usr/local` is unwritable (read-only filesystem): `mkdir` fails, the
installer dies under `set -e`, and the log shows only the last successful command with no
record of what failed.
**Suggested direction:** route the `mkdir` calls through `log_cmd` like their neighbours.
**Resolution:** fixed in `205554f6` (`git hash-object modules/21-quiet-hours.sh`), working tree
on `task-0020-quiet-hours` (uncommitted). Both `mkdir -p` calls now go through `log_cmd`; the
config-directory one targets `$(dirname "$conf_path")`, where `conf_path` defaults to
`/etc/project-tv/quiet-hours.conf` and is overridable via `QUIET_HOURS_CONF_PATH` (test-suite
hook, documented in the module header; production behaviour unchanged). Pinned: section I
checks "lib-directory mkdir is routed through log_cmd" and "config-directory mkdir is routed
through log_cmd".

### Re-review: item 10 fix round (2026-09-08, Shadow)

**Method.** Verified against the working tree at `/home/howard/Linux/projects/project_tv_rocky_linux`
(the dispatch brief's `/home/home/...` path is a typo; the doc's path is the real one), branch
`task-0020-quiet-hours`, tip `b892a70`, tree uncommitted (`git status`: 3 modified
[`install.sh`, `test/run_tests.sh`, `test/scripts/test_installer.sh`] + 3 untracked task paths;
`git diff --summary` empty, no mode-bit drift). All seven task files read in full. Per-finding
verification is by direct content inspection at the cited lines. Re-run this round: `bash -n`
7/7 PASS on all seven changed files; `shellcheck -S warning` on the same seven, with only the
hits already classified in the first review (SC1090 `install.sh:121` dynamic source, SC2120
`quiet-hours/quiet-hours.sh:79` and `quiet-hours/project-tv-quiet-hours:54` — false positives,
the callers pass arguments); SC2034 for `now_hour` is gone. TAP plan verified statically:
`test_quiet_hours.sh:19` declares `1..118`; per-section check-site count is A 30, B 2, C 14,
D 8, E 17, F 2, G 4, H 17 (= 94, the pre-fix plan) + section I 24
(`test_quiet_hours.sh:444-662`) = 118. Section I's I6 block branches on whether
`/usr/local/lib/project-tv/quiet-hours.sh` exists, but both branches emit exactly two checks, so
the plan holds on any host. Limitations of this re-review: `git hash-object` is not in this
agent's permitted command set, so the blob shas in the item 10 changes table were not
independently recomputed (content verification stands in for them); the two suites were not
re-run here, so the 118/118 and 12/12 rc 0 results stand on Tails' recorded runs (item 10,
`## Implementation`).

**Verdicts on the 11 closed findings:**

1. "k8s namespace is lost between install and runtime" — **VERIFIED FIXED.** The module detects
   with `$K8S_NAMESPACE` (`modules/21-quiet-hours.sh:65`) and writes the same value into the
   config (`modules/21-quiet-hours.sh:116`); `K8S_NAMESPACE` is always set because `install.sh:20`
   sources `config/defaults.conf:14`. The core captures env provenance at source time
   (`quiet-hours/quiet-hours.sh:38-39`) and `load_config` applies the config key only when the
   env var did not set it, after a DNS-1123 label check
   (`quiet-hours/quiet-hours.sh:142-151`). Precedence env > config key > default holds as
   claimed. `status` displays the resolved namespace
   (`quiet-hours/project-tv-quiet-hours:205`). Pinned by I3's five checks
   (`test_quiet_hours.sh:509-540`).
2. "Module re-run silently resets a live override" — **VERIFIED FIXED**, with one new nit below.
   The module reads the old config's last `QUIET_OVERRIDE=` line
   (`modules/21-quiet-hours.sh:88-93`), honours only a clean 0/1, writes it back
   (`modules/21-quiet-hours.sh:115`), and the summary prints the carry-over line
   (`modules/21-quiet-hours.sh:131-133`). Pinned by I2's three checks
   (`test_quiet_hours.sh:488-502`).
3. "start==end guard is bypassed by leading-zero input" — **VERIFIED FIXED.** The guard compares
   `(( 10#$start_hour == 10#$end_hour ))` (`modules/21-quiet-hours.sh:40`) and both values are
   normalised after the loop (`modules/21-quiet-hours.sh:47-48`), so a leading-zero hour never
   reaches the config. Pinned by I1 (`test_quiet_hours.sh:447-459`).
4. "In-place upgrade kills the installer on the new module number" — **VERIFIED FIXED.**
   `init_status` backfills missing `MODULE_ORDER` entries into an existing status file
   (`install.sh:63-74`) and `main` calls it before the menu loop (`install.sh:245`);
   `get_module_status` is total, a missing line reads as `pending` with rc 0
   (`install.sh:91-97`), so no call site (`install.sh:124,146,182,197`) can trip `set -e`.
   Pinned by I5's three checks (`test_quiet_hours.sh:576-600`), which simulate exactly the
   pre-upgrade 00-20 file.
5. "`now_hour` is dead and can raise an arithmetic error" — **VERIFIED FIXED** as stated; the
   same failure class survives at one live site, logged as a new nit below. `now_hour` has no
   occurrence left in the 259-line CLI and SC2034 no longer fires. Pinned by I7
   (`test_quiet_hours.sh:657-662`).
6. "`trigger_now` fallback ignores the repo-layout core path" — **VERIFIED FIXED.** `load_core`
   records the resolved path in `CORE_PATH` (`quiet-hours/project-tv-quiet-hours:89-92`) and
   `trigger_now` executes it under a `-f` guard, with no `/usr/local` literal left in the
   fallback (`quiet-hours/project-tv-quiet-hours:141-155`). Pinned by I6
   (`test_quiet_hours.sh:602-655`), structural on hosts with an installed copy, functional
   (stand-in core + refusing `systemctl` stub) otherwise.
7. "Two `mkdir -p` calls bypass `log_cmd`" — **VERIFIED FIXED.** Both calls route through
   `log_cmd` (`modules/21-quiet-hours.sh:96,103`); the config-directory one targets
   `$(dirname "$conf_path")` with the documented `QUIET_HOURS_CONF_PATH` test hook
   (`modules/21-quiet-hours.sh:80`). Pinned by I1's two mkdir checks
   (`test_quiet_hours.sh:465-474`). The adjacent `chmod 0644 "$conf_path"`
   (`modules/21-quiet-hours.sh:120`) also bypasses `log_cmd`, but a chmod failure on a file the
   module just created is not a realistic scenario, so it is noted here, not raised as a
   finding.
8. `## Security` "Config target lists flow into systemctl/kubectl without allowlist
   validation" — **VERIFIED FIXED.** `valid_cronjob_list` uses the full DNS-1123 label form and
   `valid_unit_list` forbids a leading dash (`quiet-hours/quiet-hours.sh:60-72`); both reject
   the attack token `--foo` (a dash is not in either first-character class) while accepting the
   legitimate multi-target lists and empty lists. `load_config` fails the whole load on a bad
   value (`quiet-hours/quiet-hours.sh:128-147`) and `main` exits 0 leaving the current state
   (`quiet-hours/quiet-hours.sh:404-407`), so the documented fail-soft contract holds. The
   recorded deviation over Omega's proposed character sets is implemented exactly as described
   in the Resolution line. Pinned by I4's four checks (`test_quiet_hours.sh:542-566`).
9. `## Security` "B-11 test check interpolates repo file paths into a python -c string" —
   **VERIFIED FIXED.** The path now goes via `sys.argv[1]`
   (`test/scripts/test_installer.sh:122`); nothing from the tree is interpolated into the
   `-c` string.
10. `## Test Results` harness bug — **VERIFIED FIXED.** `[[ "$FAIL" == "0" ]]` is the final
    statement (`test/scripts/test_installer.sh:161`), so the suite's exit code now carries the
    result and the `run_tests.sh` `ssh | tee` pipeline under `set -euo pipefail` aborts on a
    failing suite. The `test/run_tests.sh` diff is only the quiet-hours VM-run wiring
    (4 lines), consistent with item 10's "unchanged this round".
11. `## Test Results` coverage gaps — **VERIFIED FIXED.** Section I
    (`test_quiet_hours.sh:409-662`) pins all four should-fix scenarios, Omega low 1, and all
    three nits; its 24 checks take the plan from `1..94` to `1..118`
    (`test_quiet_hours.sh:19`), matching the static count above.

### `next_transition` leaves the R5 failure class unguarded at the hour step
**Severity:** nit (new in re-review)
**Where:** `quiet-hours/project-tv-quiet-hours:168`
**Problem:** the deleted `now_hour` was the dead instance of the
`$((10#$(local_tz_hour ...)))` pattern; the live instance in `next_transition`'s loop is
unguarded, and the variable it feeds is referenced under `set -u` on the next line.
**Failure scenario:** a host with a broken or missing `/etc/localtime`: `local_tz_hour`
returns empty, `hour=$((10#))` raises `value too great for base` to stderr, the assignment
fails and `hour` stays unset, then `hour_in_window "$hour"` (line 170) hits `hour: unbound
variable` under `set -uo pipefail` and `status` dies mid-output. The core state machine is
unaffected: its clock path is guarded (`quiet-hours/quiet-hours.sh:228-232`), so the system
keeps working; only the diagnostic command breaks.
**Suggested direction:** guard the hour the same way `desired_state_at` does (treat an
unresolvable hour as "no transition found" for that candidate), or default the assignment so
`hour` is never unset.

### Override carry-over regex does not trim, unlike the core's flag validation
**Severity:** nit (new in re-review)
**Where:** `modules/21-quiet-hours.sh:90`
**Problem:** the carry-over honours only `^QUIET_OVERRIDE=([01])$`, while `load_config` trims
whitespace before validating (`quiet-hours/quiet-hours.sh:98-99,117-121`), so a trailing space
makes the two disagree about whether the override is live.
**Failure scenario:** config line `QUIET_OVERRIDE=1 ` (trailing space, hand edit): the core
runs quiet, the user re-runs module 21, the module's regex does not match, the new config gets
`QUIET_OVERRIDE=0`, and the forced quiet ends with no `disable` command — the exact outcome
the R2 finding forbids, reachable only through a hand-edited config (the generated heredoc has
no trailing whitespace).
**Suggested direction:** trim the line before matching, or reuse the same trim-then-validate
sequence as the core.

**Net:** all 11 closures verified against the tree; no blocker or should-fix remains open. The
two new nits above are non-blocking for the DoD (`## Review` gate: no unresolved blockers or
should-fix); Tails may fold them into a pre-commit cleanup or leave them, at Knuckles'
discretion at item 12.

---

## Security

*Owner: `Omega`. Read-only. Severity order.*

Reviewed 2026-09-08: diff against `b892a70` plus the untracked `quiet-hours/` (4 files),
`modules/21-quiet-hours.sh`, `test/scripts/test_quiet_hours.sh` on branch
`task-0020-quiet-hours`. All nine files read in full; `shellcheck` on all four shell
deliverables (only hits are the ones Shadow already logged as nits/false positives);
credential-pattern `git grep` over the changed files (only hit is the B-09 test harness
itself, no credential values). No critical, high, or medium findings. Two low findings,
both non-blocking per the DoD.

### Config target lists flow into systemctl/kubectl without allowlist validation
**Severity:** low
**Vector:** input-validation
**Where:** `quiet-hours/quiet-hours.sh:97-102` (lists stored verbatim), `quiet-hours/quiet-hours.sh:299` (`systemctl "$action" "$unit"`), `quiet-hours/quiet-hours.sh:252-253,276-288` (kubectl patch/list/delete)
**Attack:** a root-equivalent actor edits `/etc/project-tv/quiet-hours.conf` (root:root 0644, only root can write it) and sets `QUIET_SYSTEMD_UNITS="--foo bar.timer"` or a `QUIET_K8S_CRONJOBS` value containing spaces. The root timer service then word-splits the value and passes the attacker's tokens to `systemctl`/`kubectl`: argument injection into the 15-minute root run.
**Impact:** none beyond what the actor already holds. Writing the config requires root, and root can already run arbitrary `systemctl`/`kubectl`; this is defense-in-depth, not a privilege escalation. It matters for the future: the plan makes the target list a growing named contract, and a later module or user edit could supply less-controlled values.
**Fix:** in `load_config`, validate each list value against an allowlist before accepting it (CronJob names: k8s DNS-1123 `[a-z0-9-]+`; unit names: `[A-Za-z0-9._:@-]+`), failing the whole load exactly like an invalid hour does, so a bad value fails soft to the current state.
**Resolution:** fixed in `0ad1fdb0` (`git hash-object quiet-hours/quiet-hours.sh`), working tree
on `task-0020-quiet-hours` (uncommitted). `load_config` validates both lists and the new
namespace key, failing the whole load exactly like an invalid hour. One refinement over the
suggested character sets, recorded so it is seen as deliberate: the attack token `--foo` itself
matches both proposed classes (the dash is inside `[a-z0-9-]+` and `[A-Za-z0-9._:@-]+`), so
CronJob names use the full DNS-1123 label form (alphanumeric first and last) and unit names must
not start with a dash. Empty lists (no targets) stay valid, because the module writes them when
nothing is detected. Pinned: section I checks "unit list with an option token is rejected",
"cronjob list with an option token is rejected", "malformed namespace is rejected", "empty
target lists are accepted".

### B-11 test check interpolates repo file paths into a python -c string
**Severity:** low
**Vector:** injection
**Where:** `test/scripts/test_installer.sh:119`
**Attack:** a contributor with push access to `metalllinux/project-tv-rocky-linux-edition` adds a manifest whose filename contains a single quote plus python, e.g. `manifests/x'); import os; os.system('id').yaml` (`find -name '*.yaml'` still matches it). When the suite runs, the assembled command `python3 -c "import yaml; list(yaml.safe_load_all(open('<path>')))"` executes the injected statement as the test-runner user (team-host user or `testuser` in the VM).
**Impact:** code execution on whatever machine runs the test suite. Does not raise the attacker's ceiling: the same push access can already ship a malicious installer module, which `run_module` sources and executes as root (`install.sh:103`). The interpolation pattern is pre-existing; this diff only changed `safe_load` to `list(safe_load_all(...))` on the same line.
**Fix:** pass the path via argv instead of string-building: `python3 -c "import sys, yaml; list(yaml.safe_load_all(open(sys.argv[1])))" "$yaml"`.
**Resolution:** fixed in `ad185f7e` (`git hash-object test/scripts/test_installer.sh`), working
tree on `task-0020-quiet-hours` (uncommitted). B-11 now passes the path via `sys.argv[1]`
exactly as suggested; in-tree run 12/12 rc 0.

**Verified clean (no finding):**
- **Secrets:** no credential material in any of the nine task files (read in full); the two systemd units contain no secrets; the module writes only a `$(date)` comment into the generated config. The 192.168.1.107 password appears nowhere in this doc (read in full; only the host IP, which `## Status` already records) and nowhere in the task files. Tails' `grep -Ff ~/pass.txt` audits (`## Implementation`, items 1 and final regression) are consistent with this. The raw investigation sample is on the team host, not committed.
- **Injection:** the config is never sourced — `load_config` parses KEY=VALUE lines (`quiet-hours/quiet-hours.sh:48-109`), so no code execution from config. Installer hour input is digit-validated 0-23 by `ask_number` (`lib/prompts.sh:82`) and flows only into config lines and `printf`. Module-menu input is matched against exact `MODULE_DESC` keys before use (`install.sh:246-250`); the associative-array subscript is not arithmetic-evaluated, so no injection path. The kubectl patch payload is built from the fixed values `true`/`false` (`quiet-hours.sh:252-253`); in-flight job selection is a pure-bash prefix match with the `delete` argument quoted (`quiet-hours.sh:280-288`). The CLI echoes unknown commands rather than executing them and takes no free-text arguments.
- **Authz:** `status`/`enable`/`disable` are root-gated by `require_root` (`project-tv-quiet-hours:54-59,234-244`); `usage` is deliberately unrooted so the structural test can run it on the unprivileged team host (documented in the file header and plan item 4). The service runs as root, which `systemctl` and `kubectl` require; it acts only on the configured targets. The config and state file contain no secret material, so their 0644 root-owned mode is adequate.
- **Actions:** the repo has no `.github/` (verified in plan, "Verified local facts"); the `run_tests.sh` addition (`test/run_tests.sh:105-107`) is a VM test-harness block identical in shape to its neighbours, including the pre-existing `StrictHostKeyChecking=no` toward the throwaway libvirt test VM. No CI surface is added.
- **Supply chain:** no new dependencies, downloads, `curl | bash`, container images, or lock files. The module uses only host tools (`install`, `systemctl`, `kubectl`).
- **License:** the repo is MIT (`LICENSE:1-3`); all added code is original to this task (read in full), no third-party code was introduced, no forked copyright headers or NOTICE files are implicated, and no license-compatibility question arises. License check passes.

Cross-reference, not a duplicate finding: Shadow's should-fix "start==end guard is bypassed by
leading-zero input" has an availability consequence (a 24/7 quiet window keeps `sanoid.timer`
stopped, so snapshot protection silently disappears). It is tracked in `## Review`; the fix there
covers it. Likewise the namespace-loss finding is functional, not a security issue.

### Re-review: item 10 fix round (2026-09-08, Omega)

**Method.** Verified against the working tree at
`/home/howard/Linux/projects/project_tv_rocky_linux`, branch `task-0020-quiet-hours`, tip
`b892a70`, uncommitted: `git status` shows exactly the 3 modified + 3 untracked task paths and
`git diff --summary` is empty (no mode-bit drift). All nine task files read in full (the 3
modified files as complete `git diff b892a70` diffs, the 6 new files end to end);
`shellcheck 0.10.0 -S warning` on the 7 shell files (3 hits, all already classified in the first
review, SC2034 gone); secret-pattern sweep over the task files (only benign hits: the word
"token" in allowlist comments, TAP description text, the pre-existing B-09 harness at
`test/scripts/test_installer.sh:92-98`). TAP plan re-counted statically from the file: A 30,
B 2, C 14, D 8, E 17, F 2, G 4, H 17 (= 94) + I 24 (I1 5, I2 3, I3 5, I4 4, I5 3, I6 3, I7 1)
= 118, matching `test_quiet_hours.sh:19`. Limitations: `git hash-object`, the suite runs, and
the password-file pattern audit (`grep -Ff ~/pass.txt`) are outside this agent's permitted
command set, and no secret scanner is installed in this shell (rg/gitleaks/trufflehog absent);
the blob shas, the 118/118 and 12/12 results, and the credential audit stand on Tails' item 10
runs and Big's audit, both 2026-09-08 on this tree.

**The two Resolution lines:**
1. "Config target lists flow into systemctl/kubectl without allowlist validation" —
   **VERIFIED FIXED.** `valid_cronjob_list` (`quiet-hours/quiet-hours.sh:60-63`) is the full
   DNS-1123 label form (alphanumeric first and last per token, space-separated, empty valid)
   and `valid_unit_list` (`:69-72`) forbids a leading dash; both reject `--foo`, `-foo`,
   `foo-`, `;`, quotes, and `$(...)`. `load_config` fails the whole load on a bad list
   (`:128-141`) and `main` exits 0 leaving the state untouched (`:404-407`), so the fail-soft
   contract holds. The recorded deviation over my proposed character sets is implemented
   exactly as the Resolution line says. Pinned by I4's four checks
   (`test_quiet_hours.sh:542-566`), verified present and matching the claims. The unquoted
   word-splitting at the use sites (`:363,:367`) is safe: tokens are allowlisted (no leading
   dash, no glob characters, line-based parsing rules out newlines) and every
   `kubectl`/`systemctl` argument is quoted (`:301,:325,:332,:348`); in-flight job names from
   `get jobs -o name` are DNS labels by k8s naming rules and are quoted at delete (`:332`).
2. "B-11 test check interpolates repo file paths into a python -c string" —
   **VERIFIED FIXED.** `test/scripts/test_installer.sh:122` passes the path via
   `sys.argv[1]`; nothing from the tree is interpolated into the `-c` string.

**Fix-round surface (new since the first review):**
- **Namespace precedence.** Provenance marker captured at source time
  (`quiet-hours/quiet-hours.sh:38-39`); the config key applies only when the env var did not
  set the namespace (`:148-150`); env > config key > default. The module detects in
  `$K8S_NAMESPACE` (`modules/21-quiet-hours.sh:65`, always set: `install.sh:20` sources
  `config/defaults.conf:14`) and writes the same value into the config (`:116`); `status`
  displays the resolved namespace (`quiet-hours/project-tv-quiet-hours:205`). I3 pins all
  three precedence paths, each in a fresh `bash -c` with `$CORE`/`$CONF` as positional
  arguments, nothing interpolated (`test_quiet_hours.sh:522-540`). Side benefit: a malformed
  `K8S_NAMESPACE` in `defaults.conf` (e.g. `--foo`) now fails detection at install time and is
  rejected by the load-time validation, so it can no longer reach kubectl at runtime.
- **Override carry-over.** The module reads the last `QUIET_OVERRIDE=` line of the old config,
  honours only a clean 0/1, writes it back, and prints the carry-over note in the summary
  (`modules/21-quiet-hours.sh:86-93,115,131-133`); the `|| true` at `:89` keeps the grep safe
  under the installer's pipefail. I2 pins three checks (`test_quiet_hours.sh:476-502`).
  Shadow's re-review nit on the same code (the regex does not trim, unlike the core's
  trim-then-validate, so a hand-edited trailing space makes the two disagree) is a behavioural
  consistency issue reachable only by root hand-edit; tracked in `## Review`, not duplicated
  here.
- **`QUIET_HOURS_CONF_PATH` hook.** `${QUIET_HOURS_CONF_PATH:-/etc/project-tv/quiet-hours.conf}`
  (`modules/21-quiet-hours.sh:80`), documented in the module header (`:12-13`); every use is
  quoted (`:88,103,104,120`), so a hostile value is a literal path, not a command. The trust
  boundary is the installer's invoker (root), who already owns the machine; item 10's
  competing-priorities note records the surface. No escalation.
- **Section I harness.** The module sandbox stubs `log_cmd` to record without executing
  (`test_quiet_hours.sh:422-442`), so `install`/`mkdir`/`systemctl` never touch the host;
  real writes stay in the `mktemp` scratch dir; the `ask_number` stub is fed by a
  test-controlled answer file. I5 `eval`s function bodies extracted verbatim from
  `install.sh` (`:571-574`); the eval target is the file under test, and push access to the
  repo already buys arbitrary root code through `run_module`'s source (`install.sh:121`), so
  the harness adds no new ceiling. I6's functional branch writes and runs a scratch script in
  which only `$WORK` (mktemp output) is interpolated (`:627-655`).
- **install.sh and run_tests.sh.** The backfill (`install.sh:57-75`) and status totality
  (`:87-101`) touch only fixed `MODULE_ORDER` numbers and fixed status words; the
  skip-preservation branch (`:121-130`) sits in conditional context and is `set -e` safe.
  `test/run_tests.sh` adds a 4-line VM invocation block identical in shape to its neighbours;
  no new surface (the pre-existing `StrictHostKeyChecking=no` toward the throwaway VM was
  noted in the first review).
- **Units and CLI.** `project-tv-quiet-hours.{service,timer}` are unchanged and contain no
  secrets or env material; the CLI's `CORE_PATH` fallback
  (`quiet-hours/project-tv-quiet-hours:89-92,141-155`) executes only the path
  `core_script_path` resolved, under a `-f` guard.

**Credential audit (this round):** full read of all nine task files plus the pattern sweep
above; no credential material in any of them. The password-file pattern audit is outside this
agent's command set (see Method) and stands on the two recorded 2026-09-08 runs against this
exact tree. This doc, read in full, contains no credential values.

### Empty `QUIET_K8S_NAMESPACE` passes validation and clobbers the namespace default
**Severity:** low
**Vector:** input-validation
**Where:** `quiet-hours/quiet-hours.sh:144,148-150`
**Attack:** a root-equivalent actor edits `/etc/project-tv/quiet-hours.conf` (root:root 0644)
and sets `QUIET_K8S_NAMESPACE=` (empty) while keeping a non-empty `QUIET_K8S_CRONJOBS`. The
empty value passes the namespace check because `:144` explicitly accepts `-z "$value"`, and
with no env override `:149` overwrites the `project-tv` default with the empty string. The
installer cannot produce the harmful combination: an empty `K8S_NAMESPACE` makes the module's
detection kubectl call fail, which also leaves the CronJob list empty, and the namespace is
consumed only by the CronJob steps, so a generated config is inert. Only the hand edit reaches
a live effect.
**Impact:** every tick's kubectl steps run against an empty namespace (kubectl's exact error
for `-n ""` is not verified from this seat; erroring every tick or misrouting, both are broken
states). The state file never advances, the CronJob is never suspended in-window, and the
journal logs a failure every 15 minutes: the feature silently degrades to exactly the
out-of-sync failure class the namespace fix was meant to eliminate. No privilege escalation;
writing the config already requires root.
**Fix:** in the `QUIET_K8S_NAMESPACE` case of `load_config`, apply the key only when
non-empty (`if [[ -n "$value" && -z "$QUIET_HOURS_NAMESPACE_ENV" ]]`), so an empty value means
"no key" and the default survives, or reject empty like the other keys. Add a section I check
("empty namespace key leaves the default"). Not pinned by I4: its namespace case uses
`media;rm -rf /`, which does not cover the empty branch.

**Verdict (re-review):** both `low` Resolution lines are verified against the tree; the fix
round's new surface (allowlists, namespace precedence, override carry-over, the
`QUIET_HOURS_CONF_PATH` hook, section I) is clean apart from the one new `low` above. No
unresolved finding above `low` remains, so the `## Security` DoD gate is satisfied. The three
open non-blocking items (this empty-namespace `low`, Shadow's untrimmed carry-over regex at
`modules/21-quiet-hours.sh:90`, Shadow's unguarded `10#` at
`quiet-hours/project-tv-quiet-hours:168`) are for Tails to fold into a pre-commit cleanup or
leave, at Knuckles' discretion at item 12.

---

## Test Results

*Owner: `Big`. Verdicts, never raw log dumps.*

Run 2026-09-08 on the team host (Rocky Linux 10.2) against branch
`task-0020-quiet-hours` (tip `b892a70`), uncommitted tree: 3 modified + 3 untracked task paths,
`git diff --summary` empty (no mode-bit drift). TAP streams kept at
`/tmp/opencode/task0020-quiet-hours.tap` and `/tmp/opencode/task0020-installer.tap` (team host,
not committed, no credential material).

**Workflow run:**

| Check | What it exercises | Result | Notes |
|---|---|---|---|
| compile (`bash -n`) | all 7 changed files | PASS | 7/7: `install.sh`, `modules/21-quiet-hours.sh`, `quiet-hours/quiet-hours.sh`, `quiet-hours/project-tv-quiet-hours`, `test/scripts/test_quiet_hours.sh`, `test/run_tests.sh`, `test/scripts/test_installer.sh` |
| linter (shellcheck 0.10.0, `-S warning`) | same 7 files | PASS | 4 hits, all accounted for: SC2034 unused `now_hour` (`quiet-hours/project-tv-quiet-hours:157`) is Shadow nit 2; SC1090 (`install.sh:103`, dynamic module source) and SC2120 ×2 are the false positives already classified in `## Review`. No new findings |
| unit tests (`test/scripts/test_quiet_hours.sh`, team host, no root/cluster) | window matrix (wrap 20-07, no-wrap 10-14, degenerate 10-10), boundary inclusivity, DST fixed-epoch (America/New_York and Europe/Berlin 2026 spring + fall, Asia/Tokyo control), config parse, override state machine with stubbed kubectl/systemctl and fake clock, state-file round-trip, structural wiring (section H) | PASS | 94/94 ok, rc 0; TAP plan `1..94` matches 94 emitted checks, 0 `not ok`; no silently dropped checks. Static count of check sites in the file is 94, matching the plan |
| integration tests (`test/scripts/test_installer.sh`, in-tree) | installer structure regression, B-01 (install.sh executable) and B-11 (multi-doc YAML) included | PASS | 12/12 ok, B-01 ok, B-11 ok after the `safe_load_all` fix. Verdict taken from the TAP count, not the exit code: see the harness bug below |
| Sparky tests | Rocky Linux environment | N/A | Non-graphical project (`## Status`: Graphical UI: no); this repo has no Sparky/Sparrow tasks. The Rocky Linux environment layer for this task is the project's own libvirt VM harness, recorded on the VM-run line below |
| full VM run (`test/run_tests.sh`) | both suites on a fresh Rocky 10 VM, plus the pre-existing `test_rpm_install.sh` and `test_zfs.sh` | SKIPPED (recorded) | Not executable: no libvirt VM exists on the team host (`virsh list --all` empty, no `~/test-results`). Also the tree is pending the item 10 fixes (4 should-fix across module 21, `install.sh`, CLI, core), so a VM run now would validate a superseded tree. The in-tree runs cover the same two suites on the same OS family (team host is Rocky 10.2; both suites are environment-independent local file checks per their headers). The full VM run stays an open release gate after item 10 if a VM is provisioned |
| credential audit (DoD) | 192.168.1.107 password absent from doc and task files | PASS | `grep -Fqf ~/pass.txt` (pattern-from-file, `-q`, nothing printed) over the planning doc and all 7 task files: clean |
| installer option visibility (DoD) | option in help/usage, default 20:00-07:00, override commands, configurable hours | PASS | CLI `usage` rc 0 shows the 20:00-07:00 default, `status`/`enable`/`disable`, and reboot persistence; `MODULE_DESC[21]` present (structural H3); `MODULE_ORDER` ends in 21 (`install.sh:51`, structural H4); module prompts take 0-23 with defaults 20/7 (`modules/21-quiet-hours.sh:31-32`) |

**Checks requested vs run:** 7 requested (compile, linter, quiet-hours unit suite, installer
regression, full VM run, credential audit, installer option visibility), 6 executed, 1 skipped
with explicit reasons (full VM run). No other check was dropped; nothing was reduced silently.

**Harness bug found (pre-existing, demonstrated):** `test/scripts/test_installer.sh` exits 0 when
checks fail. The script ends with the results `echo` (`test/scripts/test_installer.sh:151-152`)
and never exits on `$FAIL`, unlike `test_quiet_hours.sh:411`. Demonstrated 2026-09-08: run against
an empty directory yields 9 of 12 `not ok` and exit code 0. Any wrapper that checks the exit code
(the `ssh ... | tee` pipeline in `run_tests.sh` under `set -euo pipefail` would abort the whole
orchestrator the moment this script started telling the truth) sees a green suite. Fix is one line,
`[[ "$FAIL" == "0" ]]` at the end; include it in the item 10 round so it ships in the release
commit. Pre-existing: the file predates this task, which only changed the B-11 line 119.
**Resolution (Tails, 2026-09-08):** fixed in `ad185f7e` (`git hash-object
test/scripts/test_installer.sh`), working tree on `task-0020-quiet-hours` (uncommitted).
`[[ "$FAIL" == "0" ]]` appended after the results echo. Demonstrated: the empty-directory run
now reports 9 `not ok` and exits 1 (previously 0); the in-tree run is 12/12 rc 0. The
`run_tests.sh` `set -euo pipefail` + `ssh | tee` interaction is now fail-fast by design: a
failing suite aborts the orchestrator at the failing step instead of reporting green, so no
`run_tests.sh` change was needed.

**Coverage gaps vs the review findings (input to item 10):** the committed suite does not yet
exercise any of Shadow's four should-fix scenarios: the namespace lost between install and runtime
(no test feeds a namespace into the config), module re-run resetting a live override, the
start==end guard bypassed by leading-zero input, and the in-place-upgrade trap in
`get_module_status` (`install.sh:76-83`). Omega low 1 (target-list allowlist) is also untested;
no section D case feeds an injection token such as `--foo` into a list value. The fix round should
add a regression check for each fix where unit-testable (at minimum the start==end normalisation
and the namespace persistence) so the fixes stay fixed.
**Resolution (Tails, 2026-09-08):** fixed in `569befc3` (`git hash-object
test/scripts/test_quiet_hours.sh`), working tree on `task-0020-quiet-hours` (uncommitted). New
section I adds 24 regression checks (plan `1..94` → `1..118`): all four should-fix scenarios
(leading-zero start==end, namespace persistence, override carry-over, in-place upgrade), Omega
low 1 (allowlist, incl. empty-list acceptance), and the three nits (now_hour gone, trigger_now
repo-layout fallback via a functional harness, mkdir through log_cmd). Suite: 118/118 ok, rc 0,
on the team host 2026-09-08.

**Verdict:** PASS for plan item 9 as far as it can run on this tree: every executable check is
green, the TAP counts match their plans exactly, no check was silently dropped, and the credential
audit is clean. The tree under test is pre-fix. Shadow's 4 should-fix + 3 nits (`## Review`) and
Omega's 2 low findings (`## Security`) are not resolved here and are not yet pinned by tests (see
coverage gaps); they drive the item 10 round. The full VM run is skipped with explicit reasons and
remains a gate after the fixes. The test run itself found no code bug in the quiet-hours
deliverables; the only defect found is the `test_installer.sh` exit-code harness bug, which is a
harness bug (Big's finding, one-line fix, lands in item 10 with the rest).

**Run 2 (2026-09-08, post-fix verification of the item 10 tree, plan item 9 re-run)**

Tree: branch `task-0020-quiet-hours`, tip `b892a70`, uncommitted; `git status --short` shows
exactly the 3 modified + 3 untracked task paths; `git diff --summary` empty (no mode-bit drift).
TAP streams at `/tmp/opencode/task0020-quiet-hours-rerun.tap`,
`/tmp/opencode/task0020-installer-rerun.tap`,
`/tmp/opencode/task0020-installer-failpath.tap` (team host, not committed, no credential material).

**Workflow run:**

| Check | What it exercises | Result | Notes |
|---|---|---|---|
| compile (`bash -n`) | all 7 task files | PASS | 7/7: `install.sh`, `modules/21-quiet-hours.sh`, `quiet-hours/quiet-hours.sh`, `quiet-hours/project-tv-quiet-hours`, `test/scripts/test_quiet_hours.sh`, `test/run_tests.sh`, `test/scripts/test_installer.sh` |
| linter (shellcheck 0.10.0, `-S warning`) | same 7 files | PASS | 3 hits, all pre-classified in `## Review` at their current line numbers: SC1090 dynamic source (`install.sh:121`), SC2120 x2 (`quiet-hours/quiet-hours.sh:79`, `quiet-hours/project-tv-quiet-hours:54`; the callers pass arguments from another file). No new findings; SC2034 (`now_hour`) is gone |
| unit tests (`test/scripts/test_quiet_hours.sh`, team host) | window matrix, boundary inclusivity, DST fixed-epoch, config parse incl. allowlist rejection (section I), override state machine with stubbed kubectl/systemctl, state-file round-trip, structural section H, all four should-fix regressions (section I) | PASS | 118/118 ok, rc 0; plan `1..118` (`test_quiet_hours.sh:19`) equals the 118 emitted checks, 0 `not ok`; no silently dropped checks |
| installer regression (`test/scripts/test_installer.sh`, in-tree) | installer structure, B-01 executable, B-11 multi-doc YAML via `sys.argv[1]` | PASS | 12/12 ok, rc 0 |
| installer failure path (exit code) | suite exit code carries the result | PASS | empty-directory run: 9 `not ok`, **rc 1** (was 0 before the fix); the `[[ "$FAIL" == "0" ]]` at `test_installer.sh:161` now makes the `set -euo pipefail` + `ssh \| tee` pipeline in `run_tests.sh:13,102` fail fast on a failing suite |
| credential audit (DoD) | 192.168.1.107 password absent | PASS | `grep -Fqf ~/pass.txt` (pattern-from-file, `-q`, nothing printed) over the planning doc, all 7 task files, and both systemd units: clean |
| tree purity | release commit contains only this task's files | PASS | `git diff --summary` empty; `git status --short` shows only `M install.sh`, `M test/run_tests.sh`, `M test/scripts/test_installer.sh`, `?? modules/21-quiet-hours.sh`, `?? quiet-hours/`, `?? test/scripts/test_quiet_hours.sh` |
| full VM run (`test/run_tests.sh`) | all four suites on a fresh Rocky 10 VM (rpm, installer, quiet hours, zfs) | WAIVED (explicit, below) | not executable on the team host: `virsh list --all` empty, `~/test-results` absent; `run_tests.sh:8-10,45-48` requires a pre-existing libvirt VM with a `base-install` snapshot and cannot create one itself |

**Full VM run: explicitly waived, not skipped silently.** Reason: no libvirt VM exists on the
team host (`virsh list --all` returns no entries; `~/test-results` does not exist), and
`run_tests.sh` reverts a pre-existing VM to its `base-install` snapshot rather than provisioning
one (`run_tests.sh:45-48`). Coverage is not reduced silently by this waiver: both task suites are
environment-independent local checks (per `test_quiet_hours.sh:3-5`, no root and no cluster
required) and were executed 118/118 and 12/12 on this same OS family (team host is Rocky Linux
10.2; the VM is Rocky 10). When the VM run is eventually executed, these must hold:
1. A VM with the `base-install` snapshot and a built `px4_drv-dkms` RPM are present
   (`run_tests.sh:8-10,81`).
2. All four TAP suites pass in the VM: `test_rpm_install.sh`, `test_installer.sh` (12/12, rc 0),
   `test_quiet_hours.sh` (118/118, rc 0), `test_zfs.sh`. The orchestrator reaches its summary
   step (`run_tests.sh:124-148`) only if every `ssh | tee` pipeline succeeded, by `set -euo
   pipefail` (`run_tests.sh:13`) plus the now-fixed installer exit code; a green summary is
   therefore evidence of a green run, not just of the last suite.
3. The quiet-hours invocation block (`run_tests.sh:104-106`) picks the suite up in the VM and
   reports the same 118/118.
4. The VM run is the only layer that exercises module 21's real install side effects (`install`,
   `mkdir`, `systemctl daemon-reload`, `enable --now`, the one-shot state seed): section I's
   sandbox stubs those via `log_cmd` (records without executing), so a green VM run retires the
   last unverified assumption in this task.

**Checks requested vs run:** 8 requested (quiet-hours suite, installer in-tree, installer failure
path, `bash -n`, shellcheck, credential audit, tree purity, full VM run), 7 executed, 1 explicitly
waived (full VM run, reason above). No other check was dropped.

**Verdict (post-fix):** PASS. Every executable check is green and the counts match their plans
exactly (118/118 against plan `1..118`; 12/12; failure path rc 1). All eleven closed findings
from the review chain remain pinned: section I's 24 checks are all ok in this run. The three open
non-blocking items are not pinned by tests and stay with the pre-commit discretion recorded in
`## Next Actions`: Omega `low` (empty `QUIET_K8S_NAMESPACE` passes validation,
`quiet-hours/quiet-hours.sh:144,148-150`), Shadow nit (untrimmed carry-over regex,
`modules/21-quiet-hours.sh:90`), Shadow nit (unguarded `10#` in `next_transition`,
`quiet-hours/project-tv-quiet-hours:168`). This run found no code bug and no harness bug; the two
run-1 defects (installer exit code, coverage gaps) are fixed and demonstrated. The only remaining
test layer is the waived VM run, with the conditions above.

---

## Docs

*Owner: `Vector`.*

Done 2026-09-08 on branch `task-0020-quiet-hours`; tree left uncommitted for item 12. Feature
facts from `## Implementation` (items 3-6, 10), each verified against the working tree before
writing (`modules/21-quiet-hours.sh` in full, `quiet-hours/project-tv-quiet-hours` in full,
`quiet-hours/quiet-hours.sh` header, both units, the `install.sh` diff with `MODULE_ORDER`
ending in 21, `test/run_tests.sh` diff, `test_quiet_hours.sh` header).

| File | Sections touched | What changed |
|---|---|---|
| `README.md` | menu option 2; module execution order list; Architecture tree; Module details; new `## Quiet hours` section | module count 20 → 21 with range `(00-12, 14-21)`; new `**Quiet hours:** 21` order group matching the `MODULE_ORDER` tail; Architecture tree gains the optional systemd-timer line; new `### Module 21: Quiet hours (HDD activity)` subsection (enable prompt, 20:00-07:00 default with end-exclusive hours, start==end re-prompt, target detection, decline → skipped, override carry-over on re-run); new top-level section covering in-window behaviour (CronJob `suspend` + in-flight job deletion, `sanoid.timer`/`plocate-updatedb.timer` stop, 15-minute tick, fail-soft contract, state file), the `status`/`enable`/`disable` commands, override persistence across reboots and boot re-apply, window editing, and the per-host uninstall |
| `docs/ja/README.md` | mirror of every `README.md` change above | Japanese translation of the same sections, kept in sync per the repo convention (`CLAUDE.md:237`); same facts, no JA-only content |
| `CLAUDE.md` | hardware layout heading (was line 117); Project structure; Module execution order; Testing; Common tasks | stale IP 192.168.1.191 → 192.168.1.107 (live host, hostname `vector`; the identity gate in `## Status`); structure block gains `quiet-hours/` and the module glob becomes `modules/NN-name.sh` (module 21 exists); order block gains `→ 21 Quiet hours`; Testing lists `test/scripts/test_quiet_hours.sh` (no root or cluster needed); Common tasks gains the quiet-hours config task (config keys, allowlist validation, `status` command) |

**Checked and needed no change:**
- `CHANGELOG.md` — does not exist in this repo (`glob *CHANGELOG*`: no match); the template row does not apply.
- `test/TEST_PLAN.md` — category-level test plan; the quiet-hours suite already reaches the VM run through the `test/run_tests.sh` invocation block (`test/run_tests.sh:104-106`, Tails item 5b). Adding a plan category is a testing-process change, not a docs change.
- `test/PLATFORM_NOTES.md` — read in full; platform/version comparison only, no module inventory and no quiet-hours surface.
- Code files (`install.sh`, `modules/21-quiet-hours.sh`, `quiet-hours/*`, `test/scripts/test_quiet_hours.sh`) — header comments were written by Tails and are accurate; item 11 touches documentation only, no code edits.
- Pre-existing, out of scope, left untouched: the `docs/ja/README.md` monitoring order line lists module 13 (`13 → 19 → 20`), which is not in `MODULE_ORDER` (`install.sh` diff), and the JA file has a module 13 section the English README lacks. Not introduced by this task.

**Could not verify:** the uninstall procedure is the plan's `## Rollback` host sequence extended
to `plocate-updatedb.timer` (the target the item 1 gate added), with the README note to restore
only targets present on the host. It has not been executed on a live host; the waived VM run
(`## Test Results`) or a user re-run would settle it.

---

## Release

*Owner: `Knuckles`.*

**DONE checklist verified:** yes (2026-09-08, Knuckles). Shadow: no unresolved blockers or
should-fix, 2 non-blocking nits open. Omega: no unresolved findings above `low`, 1 non-blocking
low open. Big: PASS (118/118, 12/12, failure path rc 1; full VM run explicitly waived, no
libvirt VM on the team host). Vector: docs complete. The three open non-blocking items (Omega
low, empty `QUIET_K8S_NAMESPACE`; Shadow nits, untrimmed carry-over regex and unguarded `10#`)
are deferred by user decision 2026-09-08 and were not folded into this release, per the brief.

- **Branch:** `task-0020-quiet-hours` (cut from `b892a70` = `origin/main` at branch time;
  `git fetch` before commit showed `origin/main` still at `b892a70`, merge-base identical, no
  rebase needed)
- **Commits:** `10e114f765e092c73567d994d84fac110642ac2f` on the branch, `TASK-0020: feat(installer):
  quiet hours for hard drive activity (module 21)`, staged per-file (never `git add -A`), 12 files
  (+1708/−13), only this task's paths (`git show --stat`). GPG-signed: **no** — no GPG signing key
  exists in this environment (`gpg --list-secret-keys` empty) and `commit.gpgsign` is unset in the
  repo, so the commit is unsigned by necessity, recorded here rather than papered over.
- **PR:** `metalllinux/project-tv-rocky-linux-edition#1` (https://github.com/metalllinux/project-tv-rocky-linux-edition/pull/1) opened ✅,
  squash-merged ✅. In-account repo, no human gate per AGENTS.md §8. PR file list verified: exactly
  the 12 task paths, nothing else. The repo has no CI of its own (no `.github/`; `gh run list` on
  the branch: zero runs), so no checks gated the merge.
- **Merged sha:** `8623cc3df38f96bc32fe85608bfd62dd4d3e253c` on `main` (merge time
  2026-09-08T08:17:34Z). Live on GitHub, verified 2026-09-08 by `git ls-remote origin main` →
  `8623cc3df38f96bc32fe85608bfd62dd4d3e253c` and `git show --stat 8623cc3`: only the 12 task files,
  no mode-bit changes on existing files, the user's pre-existing uncommitted changes not swept in.
- **Deploy:** no workflow dispatched (plan `## Rollback`: no deployment to dispatch). The merged
  change is inert until the user re-runs the installer; applying it to production 192.168.1.107 is
  a separate post-release step under the user decision 2026-09-08 (write permission granted for
  the apply step only; the apply prompt file is the follow-up deliverable).

---

## Archive

*Owner: `Espio`, the only agent that deletes. Superseded detail lands here rather than being
lost. Decisions, verified facts, rejected options with their reasons, known traps, and anything the
user said are never deleted.*

**Pruning log**

| Date | What was pruned or compressed | Rough size |
|---|---|---|
| | | |
