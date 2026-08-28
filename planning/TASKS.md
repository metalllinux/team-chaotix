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
| TASK-0007 | Git worktrees support for parallel projects | Robotnik | planning/docs/TASK-0007-git-worktrees.md | In Progress |
| TASK-0008 | Fix GDM Cinnamon-session login Authentication Error; widen VM test matrix | Robotnik | planning/docs/TASK-0008-cinnamon-gdm-auth-fix.md | In Progress |
| TASK-0009 | Standardize desktop application testing on Sparky + pyatspi2 | Robotnik | planning/docs/TASK-0009-pyatspi2-desktop-testing-standard.md | Planning |
| TASK-0010 | Fix EVO-X2 iGPU wedge killing llama-server (Q5) sessions | Robotnik | planning/docs/TASK-0010-evox2-gpu-wedge-fix.md | In Progress |
| TASK-0011 | Set Q4_K_XL Qwen 3.8 as the team's default model | Robotnik | planning/docs/TASK-0011-default-model-q4kxl.md | In Progress |
| TASK-0012 | Align team dispatch to single-slot endpoint (--parallel 1) | Robotnik | planning/docs/TASK-0012-single-slot-sequencing.md | Done |
| TASK-0013 | README: GMKtec EVO-X2 + Qwen 3.8 UD-Q4_K_XL model host setup | Robotnik | planning/docs/TASK-0013-evox2-readme-setup.md | In Progress |

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
