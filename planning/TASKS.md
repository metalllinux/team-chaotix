# TASKS — Team Chaotix

Master index of every task the team is working or has worked. One row per task, one planning doc per
task. `Robotnik` owns this file.

Statuses: `Planning` · `In Progress` · `In Review` · `In Test` · `Releasing` · `Done` · `Blocked`

| Key | Title | Owner agent | Planning doc | Status |
|---|---|---|---|---|
| TASK-0001 | Team Chaotix V1 Setup | Robotnik | n/a, built ahead of the team | Done |
| TASK-0002 | Port Cinnamon Desktop to Rocky Linux 10 | Robotnik | planning/docs/TASK-0002-cinnamon-rocky10.md | Done |
| TASK-0003 | VM Testing: Cinnamon RPMs on Rocky Linux 10.2 | Robotnik | planning/docs/TASK-0003-cinnamon-vm-testing.md | In Test |
| TASK-0004 | Build mozjs115 115.29.0, update cjs to 140.0, fix muffin circular dependency | Robotnik | planning/docs/TASK-0004-mozjs115-runtime-muffin-fix.md | Done |
| TASK-0005 | Validate INSTALL.md on fresh VM | Robotnik | planning/docs/TASK-0005-install-validation.md | Done |
| TASK-0006 | Local DNF Repository for Cinnamon RPMs | Robotnik | planning/docs/TASK-0006-dnf-repo-setup.md | Done |
| TASK-0007 | Git worktrees support for parallel projects | Robotnik | planning/docs/TASK-0007-git-worktrees.md | Done |
| TASK-0008 | Fix GDM Cinnamon-session login Authentication Error; widen VM test matrix | Robotnik | planning/docs/TASK-0008-cinnamon-gdm-auth-fix.md | In Progress |
| TASK-0009 | Standardize desktop application testing on Sparky + pyatspi2 | Robotnik | planning/docs/TASK-0009-pyatspi2-desktop-testing-standard.md | Done |
| TASK-0010 | EVO-X2 iGPU wedges: root cause + durable fix | Robotnik | planning/docs/TASK-0010-evox2-gpu-wedge-fix.md | Done |
| TASK-0011 | Set Q4_K_XL Qwen 3.8 as the team's default model | Robotnik | planning/docs/TASK-0011-default-model-q4kxl.md | Done |
| TASK-0012 | Align team dispatch to single-slot endpoint (--parallel 1) | Robotnik | planning/docs/TASK-0012-single-slot-sequencing.md | Done |
| TASK-0013 | README: GMKtec EVO-X2 + Qwen 3.8 UD-Q4_K_XL model host setup | Robotnik | planning/docs/TASK-0013-evox2-readme-setup.md | Done |
| TASK-0014 | Vector agent: extend bash permissions to finish TASK-0013 DoD items | Robotnik | planning/docs/TASK-0014-vector-bash-permissions.md | Done |
| TASK-0015 | Cinnamon RPMs: minimal-server install + LightDM/SDDM test matrix | Robotnik | planning/docs/TASK-0015-cinnamon-server-multidm.md | Planning |
| TASK-0016 | INSTALL.md: verify all instructions + add minimal-server install-and-run section | Robotnik | planning/docs/TASK-0016-install-md-minimal-server.md | Done (2026-09-19; PR #5 merged, main `893b22a`) |
| TASK-0017 | Complete Cinnamon desktop: missing subpackages, Rocky wallpaper, branding, terminal | Robotnik | planning/docs/TASK-0017-cinnamon-desktop-completeness.md | Done (2026-09-19; PR #4 merged, main `3375a05`) |
| TASK-0018 | Provision reference + explore VMs for Cinnamon-for-Rocky10 | Robotnik | planning/docs/TASK-0018-vm-reference-explore-provisioning.md | Done |
| TASK-0019 | Diagnose Espio empty-result failures; harden team against the 32k turn cap | Robotnik | planning/docs/TASK-0019-espio-32k-turn-cap.md | Done |
| TASK-0020 | TV project: quiet hours for hard drive activity (installer option + override commands) | Robotnik | planning/docs/TASK-0020-quiet-hours.md | Done |
| TASK-0021 | Team lesson: interactive-input test stubs fed via `$(...)` lose in-subshell state | Robotnik | planning/docs/TASK-0021-subshell-input-stub-lesson.md | Done |
| TASK-0022 | Set IQ4_XS Qwen 3.8 as the team's default model | Robotnik | planning/docs/TASK-0022-team-model-iq4xs.md | Done |
| TASK-0023 | Install ripgrep (rg) on the agent host | Robotnik | planning/docs/TASK-0023-rg-host.md | Done |
| TASK-0024 | Sign the Cinnamon RPMs, enable gpgcheck, publish the release manifest | Robotnik | planning/docs/TASK-0024-rpm-signing-gpgcheck.md | Done (2026-09-24; PR #6 merged, main `a70aedc`, tag `v1.0.0`; all 11 DoD ticked) |
| TASK-0025 | Team v2: license agent, VM isolation, agentgateway/A2A, agentsmd, operator model | Robotnik | planning/docs/TASK-0025-team-v2-upgrade.md | Done (2026-09-29; all spec items implemented, verified end-to-end, committed) |
| TASK-0026 | Cinnamon Control Center GUI test: Rocky Linux 10 vs Fedora Cinnamon 45 beta | Robotnik | planning/docs/TASK-0026-cinnamon-control-center-comparison.md | Blocked (box 1 open at window level on TASK-0034 no-render; box 2 open on upstream change in linuxmint/cinnamon — TASK-0035 verdict in; upstream report declined by operator 2026-10-16) |
| TASK-0027 | Cinnamon brightness: Settings and keyboard shortcuts have no effect | Robotnik | planning/docs/TASK-0027-cinnamon-brightness-fix.md | Done (2026-10-19; signed -3 republish landed on main as 8d41fc9 via PR #8, fresh-clone validation 67/67 plus rpm -K OK; consumer-path gap open, follow-up option A recorded, see ## Release) |
| TASK-0028 | Rocky 10 + Fedora Cinnamon VM deploy skill | Shadow | planning/docs/TASK-0028-vm-deploy-skill.md | Done |
| TASK-0029 | VM scripts repair (align scripts/ with AGENTS.md section 12) | Robotnik | planning/docs/TASK-0029-vm-scripts-repair.md | Planning |
| TASK-0030 | Team model migration to Qwen3.8-27B-UD-IQ3_XXS (thinking low on workers) | Robotnik | planning/docs/TASK-0030-team-model-migration.md | Done |
| TASK-0031 | vm-deploy skill update (dual libvirt instance gotcha, boot caveats) | Tails | planning/docs/TASK-0031-vm-deploy-skill-update.md | Done |
| TASK-0032 | Operator-directed text corrections (site woodwork draft: banned word + phrase) | Tails | planning/docs/TASK-0032-operator-text-corrections.md | Done |
| TASK-0033 | Cinnamon-for-Rocky10 environment: single project directory, both VMs verified | Tails | planning/docs/TASK-0033-cinnamon-project-environment.md | In Progress (push and merge complete 2026-10-18, origin main = b59da12; signed -3 republish landed on main as 8d41fc9 via PR #8 on 2026-10-19; remainder per ## Next Actions, includes the operator GitHub-side token revoke) |
| TASK-0034 | Cinnamon shell no-render: panel and app windows not rendered on Rocky_Linux_10_Cinnamon | Robotnik | planning/docs/TASK-0034-cinnamon-shell-no-render.md | Done (2026-10-10; all five DoD boxes verified and ticked; verdict: environment limitation) |
| TASK-0035 | Cinnamon Control Center Power pane: D-Bus Unauthorized (36) at cs_power.py:883 | Robotnik | planning/docs/TASK-0035-cinnamon-power-pane-dbus-unauthorized.md | Done (canonical push awaits the operator's token rotation, see ## Release; upstream report declined by operator 2026-10-16) |
| TASK-0036 | Host reinstall: back up the state outside ~/AI and ~/Linux (GPG signing key, old public key, VM disks, team files) | Robotnik | planning/docs/TASK-0036-host-reinstall-backup.md | In Progress (operator 2026-10-20: ~/AI and ~/Linux are auto-backed up; the rest is this task) |
| TASK-0037 | Team platform: cycle graph, A2A, portless, licence gate, gateway wrapper; new Flicky licence agent | Robotnik | planning/docs/TASK-0037-team-platform.md | In Progress (implementation landed on main as 28e4b2a 2026-10-24; selftest 55 checks green; review chain pending; runner registration N/A while repo is public, operator decision — local pre-push selftest is the gate) |
| TASK-0038 | Cinnamon for Rocky 10: fix GPG signing/install, System Settings launch+icon, icon parity vs F45 | Robotnik | planning/docs/TASK-0038-cinnamon-gpg-settings-icons.md | In Progress (items 1-5 done: git repair, signature audit, keyring, re-sign staged+swapped; GPG root cause = 64 RPMs under old key vs docs shipping only new key) |
| TASK-0039 | Update team agents to catch GPG, icon, and feature-parity issues | Robotnik | planning/docs/TASK-0039-agent-gpg-icon-feature-catch.md | Done (2026-10-25; merged to main as dfbd140 via PR #2; selftest 56/56 + config gate green; commit-signing gap recorded as team-wide follow-up) |

The "Team Chaotix V1 Setup" row is the pipeline itself, built before the team existed to build it.
It has no planning doc because there was no team to write one. Every row after this one follows the
normal shape.

---

## How a row gets here

1. A task arrives from the user or from an upstream issue or pull request.
2. `Robotnik` creates `planning/docs/TASK-XXXX-<slug>.md` from
   `planning/templates/planning-doc.md` and writes `## Definition of Done` itself. Nobody else writes
   that section.
3. The row is added here.

## How a row leaves

It does not. Rows stay at `Done` as the project's record, and the planning doc stays with them. Closed
docs are how the team remembers what was decided and why. `Espio` prunes their contents; it
never deletes a doc.

## Conventions

- **`Owner agent`** is whoever the work is with *right now*, not who will finish it.
- **`Blocked`** always has a reason in the planning doc's `## Status`, naming what would unblock it.
- The `Planning doc` cell links to the file.

