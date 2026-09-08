# TASK-0020: quiet-hours mechanism — stop scheduled background work, do not throttle I/O

**Context** — the production media server (192.168.1.107, Rocky Linux 10, kubeadm cluster) shows hard
drive activity during the user's quiet hours. The repo's code identifies the scheduled background I/O
sources on the ZFS mirror: the hourly `jellyfin-library-refresh` CronJob
(`manifests/cronjobs/jellyfin-library-refresh.yaml:10`) and the hourly `sanoid.timer` snapshot runs
(`modules/12-sanoid.sh:128-138`). The PM decision (2026-09-07, `## Status`) requires the mechanism to
target background I/O sources, never break active playback, and never modify production.

**Options**

| Option | Trade-off |
|---|---|
| A. Stop scheduled background work in-window (host systemd timer + state-machine script; suspend the CronJob, delete in-flight refresh jobs, stop `sanoid.timer`; CLI override) | Only quiets the known scheduled sources, so the target list must be confirmed by read-only investigation first (plan item 1 gates it). Zero playback impact: the streaming path is never touched. Self-heals every 15-minute tick, fails soft to loud. |
| B. Per-process I/O throttling (`ionice` / cgroup `io.max` on the Jellyfin pod) | Catches any source, but the library scan runs inside the Jellyfin server process (the CronJob only POSTs to its `/Library/Refresh` API, `jellyfin-library-refresh.yaml:26-28`), so throttling that process throttles active playback reads too. Violates the PM decision. Needs cgroup v2 plumbing around containerd on a production host. |
| C. Drive spin-down in-window (`hdparm -S` / APM) | Maximum quiet (drives actually sleep), but playback wake latency of seconds to minutes, APM is unsupported territory on 10.9T CMR enterprise drives in a ZFS mirror (`CLAUDE.md:117-123`), and it breaks the playback guarantee. |

**Recommendation** — A. It is the only option that quiets the verified scheduled sources without
touching the playback path, uses moving parts that already exist on every installed host (kubectl,
systemd, the two units above), and fails soft: every transition step is independent, logged, and
retried on the next tick. The investigation gate in plan item 1 confirms the target list on
production before implementation; if the top I/O source is only stoppable by breaking playback or
recording, the trade-off is surfaced before implementation, per the PM decision.

**Consequences** — commits the installer to a new module 21 (`modules/21-quiet-hours.sh`), a host
service/timer pair, a user CLI (`project-tv-quiet-hours enable|disable|status`), and two new persistent
files on installed hosts (`/etc/project-tv/quiet-hours.conf`, a state file under
`/var/lib/project-tv/`). Cost is roughly 30 agent turns including investigation, review, tests, docs,
and release. Every future app module that adds scheduled I/O must register its units with the
quiet-hours target list (config-driven, so the change is one config line plus one test).

**Reversibility** — cheap both ways. Repo: `git revert` of the merge commit. Host: documented uninstall
procedure (disable timer, restore `suspend: false`, start `sanoid.timer`, delete files). The per-tick
state machine heals partial transitions, so there is no point of no return short of the PR merge,
which is itself cheaply revertible.
