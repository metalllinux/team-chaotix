# TASKS — Team Chaotix

Master index of every task the team is working or has worked. One row per task, one planning doc per
task. `Robotnik` owns this file.

Statuses: `Planning` · `In Progress` · `In Review` · `In Test` · `Releasing` · `Done` · `Blocked`

| Key | Title | Owner agent | Planning doc | Status |
|---|---|---|---|---|
| TASK-0001 | Team Chaotix V1 Setup | Robotnik | n/a, built ahead of the team | Done |
| TASK-0007 | Git worktrees support for parallel projects | Robotnik | planning/docs/TASK-0007-git-worktrees.md | Done |
| TASK-0010 | EVO-X2 iGPU wedges: root cause + durable fix | Robotnik | planning/docs/TASK-0010-evox2-gpu-wedge-fix.md | Done |
| TASK-0011 | Set Q4_K_XL Qwen 3.8 as the team's default model | Robotnik | planning/docs/TASK-0011-default-model-q4kxl.md | Done |
| TASK-0012 | Align team dispatch to single-slot endpoint (--parallel 1) | Robotnik | planning/docs/TASK-0012-single-slot-sequencing.md | Done |
| TASK-0013 | README: GMKtec EVO-X2 + Qwen 3.8 UD-Q4_K_XL model host setup | Robotnik | planning/docs/TASK-0013-evox2-readme-setup.md | Done |
| TASK-0014 | Vector agent: extend bash permissions to finish TASK-0013 DoD items | Robotnik | planning/docs/TASK-0014-vector-bash-permissions.md | Done |
| TASK-0019 | Diagnose Espio empty-result failures; harden team against the 32k turn cap | Robotnik | planning/docs/TASK-0019-espio-32k-turn-cap.md | Done |
| TASK-0020 | TV project: quiet hours for hard drive activity (installer option + override commands) | Robotnik | planning/docs/TASK-0020-quiet-hours.md | Done |
| TASK-0021 | Team lesson: interactive-input test stubs fed via `$(...)` lose in-subshell state | Robotnik | planning/docs/TASK-0021-subshell-input-stub-lesson.md | Done |
| TASK-0022 | Set IQ4_XS Qwen 3.8 as the team's default model | Robotnik | planning/docs/TASK-0022-team-model-iq4xs.md | Done |
| TASK-0023 | Install ripgrep (rg) on the agent host | Robotnik | planning/docs/TASK-0023-rg-host.md | Done |
| TASK-0025 | Team v2: license agent, VM isolation, agentgateway/A2A, agentsmd, operator model | Robotnik | planning/docs/TASK-0025-team-v2-upgrade.md | Done (2026-09-29; all spec items implemented, verified end-to-end, committed) |
| TASK-0028 | Rocky 10 + Fedora Cinnamon VM deploy skill | Shadow | planning/docs/TASK-0028-vm-deploy-skill.md | Done |
| TASK-0029 | VM scripts repair (align scripts/ with AGENTS.md section 12) | Robotnik | planning/docs/TASK-0029-vm-scripts-repair.md | Planning |
| TASK-0030 | Team model migration to Qwen3.8-27B-UD-IQ3_XXS (thinking low on workers) | Robotnik | planning/docs/TASK-0030-team-model-migration.md | Done |
| TASK-0031 | vm-deploy skill update (dual libvirt instance gotcha, boot caveats) | Tails | planning/docs/TASK-0031-vm-deploy-skill-update.md | Done |
| TASK-0032 | Operator-directed text corrections (site woodwork draft: banned word + phrase) | Tails | planning/docs/TASK-0032-operator-text-corrections.md | Done |
| TASK-0036 | Host reinstall: back up the state outside ~/AI and ~/Linux (GPG signing key, old public key, VM disks, team files) | Robotnik | planning/docs/TASK-0036-host-reinstall-backup.md | In Progress (operator 2026-10-20: ~/AI and ~/Linux are auto-backed up; the rest is this task) |
| TASK-0037 | Team platform: cycle graph, A2A, portless, licence gate, gateway wrapper; new Flicky licence agent | Robotnik | planning/docs/TASK-0037-team-platform.md | In Progress (implementation landed on main as 28e4b2a 2026-10-24; selftest 55 checks green; review chain pending; runner registration N/A while repo is public, operator decision — local pre-push selftest is the gate) |
| TASK-0039 | Update team agents to catch GPG, icon, and feature-parity issues | Robotnik | planning/docs/TASK-0039-agent-gpg-icon-feature-catch.md | Done (2026-10-25; merged to main as dfbd140 via PR #2; selftest 56/56 + config gate green; commit-signing gap recorded as team-wide follow-up — resolved by TASK-0040) |
| TASK-0040 | Commit signing key for Team Chaotix, key material in ~/AI/secrets | Robotnik | planning/docs/TASK-0040-commit-signing-key-setup.md | In Progress (2026-11-10: W1-W6 complete; final key F9261D151316FD60 uid Team Chaotix <howard.a.vanderwal@protonmail.com> in ~/AI/secrets (600/700), ~/.gitconfig applied and backed up, three remotes wired, proof commit b1ea2c3a…0a8e on verification/TASK-0040-commit-signing (single signed empty commit off origin/main, not merged); operator web-UI done: final key registered at account level, prior team registrations deleted, protonmail address verified on the account; operator browser confirmation done: green Verified; 9/10 DoD boxes ticked; review chain re-run on the identity change complete (2026-11-11: Shadow pass 3 clean, Omega pass, Big PASS 6/6, Charmy pass, Flicky gate PASS exit 0); Knuckles doc-delta commit + Espio prune next; box 7 open on egress root cause (external, router/ISP) + PAT rotation + auto-backup destination) |

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

