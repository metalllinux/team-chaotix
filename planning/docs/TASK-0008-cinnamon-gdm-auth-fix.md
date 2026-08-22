# TASK-0008 — Fix GDM Cinnamon-session login Authentication Error; widen VM test matrix

> **Section order below is fixed.** Each agent writes to its own section and no other. `Robotnik`
> reads only `## Status` and `## Next Actions`. Do not reorder, rename, or remove sections.

- **Created:** 2026-08-20

---

## Status

*Owner: `Robotnik`. Keep this SHORT and CURRENT — it is one of only two sections the PM reads, so a
stale entry means the whole loop runs on bad information.*

**Now:** Wave 0 re-dispatch is the first action of the next session (Prompt 3 at
`planning/docs/TASK-0008-new-session-prompt.md`), after an infra incident (below). `## Plan`
complete
(Amy, 2026-08-20): reproduction design, root-cause hypotheses H1-H4, fix approach, 6-scenario
Sparky/Sparrow matrix, rollback. Decision doc: `planning/DECIDE-gdm-login-test-automation.md`.

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

**Dispatch policy (endpoint-bound):** on the 4-slot Q5 endpoint, run the plan's parallel waves
as written (Wave 0: 1 ∥ 2 ∥ 3 ∥ 9a, Amy as fifth client or held; review fan-out: Shadow ∥
Omega, then Big). Until Q5 is up, at most 2 subagents concurrently on Q6/8090 (one slot + 1h
request timeout). Commit target stays feature branch `task-0008-gdm-auth` in the clone; item 13
PRs it to main. A7 guard stands: one 4GB VM at a time, check `free -g` first.
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
- [ ] `Robotnik` (next session, Prompt 3): first stand up the Q5 endpoint and retarget the
      agent config (gates everything; steps in Status and in Prompt 3). Then dispatch Wave 0
      per the plan on 4 slots (1 ∥ 2 ∥ 3 ∥ 9a, plus Amy or held), then the critical path:
      4 → 5 → 6 → (Shadow ∥ Omega, then Big) → 8 → 10 → (11) → 12 → 13 → 14. If a dispatch
      comes back empty, suspect the endpoint before the agent (see Status).

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
