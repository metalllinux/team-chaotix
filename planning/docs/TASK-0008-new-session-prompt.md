# TASK-0008 — new-session prompts

Three prompts below. Prompt 1 is the verbatim original task brief, kept as the record of what
the user asked. Prompt 2 (2026-08-21, post-plan) is superseded by the overnight dispatch
incident it did not anticipate. **To continue the work, paste Prompt 3** (2026-08-22,
post-incident, includes the Q5 model decision). The planning docs
`planning/docs/TASK-0008-cinnamon-gdm-auth-fix.md` and
`planning/docs/TASK-0009-pyatspi2-desktop-testing-standard.md` carry all state.

---

## Prompt 1 — original task brief (verbatim, superseded)

Task for Robotnik: find out why GDM login fails with an Authentication Error when the Cinnamon
session is selected on Rocky Linux 10, fix it in the cinnamon-for-rocky10 repository, and widen the
Cinnamon VM test coverage.

## What the user hit

1. Installed the Cinnamon RPMs from the local DNF repo on the user's Rocky Linux 10.2 machine,
   following the INSTALL.md in the repository.
2. Logged out, selected the Cinnamon session from GDM, entered the password.
3. Got an Authentication Error instead of the desktop.
4. Had to reboot the machine to get a working session back.

The machine works again after the reboot. The failure must be reproduced in a libvirt VM before
any fix is claimed.

## What this task must deliver

1. **Root cause with evidence.** Reproduce the failed Cinnamon-session login in a VM, capture
   `journalctl -u gdm` and `/var/log/secure` from the failed attempt and from a successful GNOME
   login, and compare. State the cause in the planning doc with the log lines that prove it.
2. **Fix in the repository.** Repo is `metalllinux/cinnamon-for-rocky10` (main branch), project
   directory `~/Linux/projects/cinnamon_4_rocky10/`. After the fix, a system that already has
   GDM plus GNOME must be able to switch to the Cinnamon session in GDM and log in successfully.
3. **Wider test matrix.** Big owns this. Every scenario runs on a libvirt Rocky Linux 10 VM and
   every scenario has a written Sparky/Sparrow (Raku) test, because all Rocky Linux testing goes
   through Sparky. Scenarios, minimum:
   - Fresh Rocky Linux 10 with GDM and GNOME installed (the user's exact configuration). Install
     the Cinnamon RPMs, switch to the Cinnamon session in GDM, log in, and verify the session comes
     up.
   - Fresh Rocky Linux 10 with LightDM installed. Install the Cinnamon RPMs, then log in to the
     Cinnamon session through LightDM and verify it works.
   - Fresh Rocky Linux 10 with no login manager at all (blank install). Install the Cinnamon RPMs
     and verify the Cinnamon session is available and login works.
   - Uninstall. After a successful install, remove the Cinnamon RPMs and verify the system is not
     left broken. No broken or dangling packages, no leftover session entries, no PAM breakage, and
     the previous login path still works.
   - As many additional configuration combinations as are practical. The point is the widest
     sensible coverage, not just the one configuration the user hit.
4. **Reusable tests.** Each scenario gets a real Sparrow task that can be re-run, not a one-off
   manual check. Big decides the Sparky harness layout and records results in the planning doc.

## Context pointers

- Repo: https://github.com/metalllinux/cinnamon-for-rocky10
- INSTALL.md in that repository is the procedure the user followed.
- Prior history: planning/docs/TASK-0002 through TASK-0006 cover the RPM builds, the first VM
  testing round, the DNF repo, and INSTALL.md validation.
- Testing strategy rules are in AGENTS.md section 7 (libvirt VMs, Sparky, Raku install procedure).

Create the TASK-0008 planning doc, write a Definition of Done that covers all four deliverables
above, add the TASKS.md row, and start the cycle.

---

## Prompt 2 — continuation, post-plan (2026-08-21)

> Paste everything below this line into a fresh opencode (Robotnik) session to continue
> TASK-0008.

Task for Robotnik: continue TASK-0008 — find the root cause of the GDM "Authentication Error"
when the Cinnamon session is selected on Rocky Linux 10, fix it in the cinnamon-for-rocky10
repository, and widen the Cinnamon VM test matrix.

Setup is complete: planning doc, Definition of Done, TASKS.md row, and Amy's `## Plan` all
exist. The planning doc `planning/docs/TASK-0008-cinnamon-gdm-auth-fix.md` carries all state —
read its `## Status` and `## Next Actions`, then run the plan: dispatch Wave 0 (plan items
1 ∥ 2 ∥ 3 ∥ 9a) as parallel task calls in a single message, then follow the critical path in
`## Plan`: 4 → 5 → 6 → Shadow ∥ Omega ∥ Big → 8 → 10 → (11) → 12 → 13 → 14. Reproduction and
matrix execution are owned by `Big`; `Tails` writes the harness scripts.

Before the first dispatch, verify the model endpoint is up:
`curl -sS -m 10 http://192.168.1.106:8088/v1/models`. If a dispatch comes back empty with no
file changes, suspect the endpoint before the agent (2026-08-20: the old 8086 endpoint was down
and silently killed dispatches).

Standing rules for this task:
- Launch opencode from `~/AI/projects/team-chaotix` (agents and AGENTS.md only load from there).
- Commits and pushes to `metalllinux` repositories need no user confirmation (standing
  permission 2026-08-21, AGENTS.md section 1).
- A GitHub token is intentionally embedded in this repo's `origin` remote URL
  (`~/AI/projects/team-chaotix/.git/config`) and stays there (user decision, 2026-08-21).
  Never write it into a file, commit, planning doc, or GitHub issue; never stage anything
  under `.git/`.
- The git clone of the repo under fix is `~/Linux/projects/cinnamon-for-rocky10/`; the project
  dir `~/Linux/projects/cinnamon_4_rocky10/` has no `.git` — commits go to the clone.

---

## Prompt 3 — continuation, post-incident (2026-08-22)

> Paste everything below this line into a fresh opencode (Robotnik) session to continue
> TASK-0008 and TASK-0009. This session runs on Qwen3.8-27B-UD-Q5_K_XL per the user's
> decision below, and all team agents are re-targeted to that same model as the first
> action.

Task for Robotnik: continue TASK-0008 (reproduce and root-cause the GDM "Authentication
Error" for the Cinnamon session on Rocky Linux 10, fix it in cinnamon-for-rocky10, widen
the VM test matrix) and TASK-0009 (standardize desktop application testing on Sparky +
pyatspi2). Both planning docs have current `## Status` and `## Next Actions`; read those
two sections of each doc first, then proceed. No work item is finished. Everything runs
fresh.

### Where we stand (catalogued 2026-08-22)

**TASK-0008.** Plan complete (14 items, critical path in the doc). Zero items finished.
Wave 0 was dispatched 2026-08-21 ~20:38 JST as five parallel subagent sessions (items 1,
2, 3, 9a, plus Amy for TASK-0009). All five died overnight. Root cause, verified in
`~/.local/share/opencode/log/opencode.log`: five concurrent sessions on the single-slot
model endpoint (`llama-server-qwen3.8-27b-q6`, port 8090, `--parallel 1`) with a 1h
request timeout (`timeout: 3600000` in `~/.config/opencode/opencode.json`). Each
session's final model call queued past 60 minutes, errored "The operation timed out."
with no retry, and the session died. Dead session IDs for the log:
`ses_fdbe211d4ffei0W0blD65cynuQ` (Amy), `ses_fdbe11b18ffe6h4kyZmAW3Q5UI` (Tails item
1), `ses_fdbdfd5a8ffeF50rRM1bMA8esH` (Tails item 2), `ses_fdbdea588ffekUY38RR5Alsc34`
(Big item 3), `ses_fdbdd653dffeLaw7z5qqdPjJ7U` (Tails item 9a).

Leftover state from the dead sessions:

- Interrupted Raku install: `~/.raku` exists (bin/ has zef, no raku binary),
  `~/.zef/store` exists. Item 1 must repair or complete the install first.
- Big's scratch VM `cinnamon-inspect-vm` is gone (domain deregistered by ~12:50 JST
  2026-08-22; exact stop time uncertain, the host and EVO-X2 clocks disagreed by
  ~40 min). Its disk is kept at
  `/var/lib/libvirt/images/cinnamon-test/cinnamon-inspect-vm.qcow2` (951MB). `virsh
  list` is empty. Recreate fresh for item 3.
- No branches, no new files, no doc sections. The clone
  `~/Linux/projects/cinnamon-for-rocky10/` is on main with only the pre-existing
  untracked file `vm-test/test-repo-setup.sh`.

**TASK-0009.** Doc, DoD, and TASKS.md row exist. `## Plan` is an empty stub (Amy died
before writing it). Scope: `AGENTS.md` section 7, `.opencode/agents/big.md`,
`README.md`, and `.github/actions/sparky-test-runner/` if affected. The doc also asks
for the subagent concurrency ceiling to be recorded in AGENTS.md (see the endpoint
note below).

**Model decision (user, 2026-08-22): the next team model is
`Qwen3.8-27B-UD-Q5_K_XL` and all agents should use it.** This supersedes the Q6
re-target (team repo commit `7f0c6a4`) and the Q8 re-target before it (commit
`afade6e`). Verified gap at the time of writing: no Q5 model file on EVO-X2
(`find /mnt/data` for `*q5*` returned nothing, 2026-08-22) and no Q5 service (only
8088 and 8090 were listening). The Q5 endpoint must exist before any subagent
dispatch:

1. Model file on EVO-X2 under `/mnt/data/models/` (a Q5_K_XL gguf from the same
   Hugging Face repo the q6/q8 files came from; the `add-ai-model` skill at
   `~/.config/opencode/skills/add-ai-model/SKILL.md` documents the full workflow).
2. systemd user unit on EVO-X2 modeled on the q6/q8 units
   (`~/.config/systemd/user/llama-server-qwen3.8-27b-q6.service`), next free even
   port (check the firewall; 8088 and 8090 are taken), `--parallel 4` (single-slot
   parallelism is what killed the 2026-08-21 fan-out).
3. Provider entry `evo-x2-qwen3.8-q5` in `~/.config/opencode/opencode.json` (global
   config, outside the repo), matching the shape of the existing `evo-x2-*` entries.
4. Retarget the `model:` frontmatter line in all 10 files under
   `.opencode/agents/*.md` (currently
   `evo-x2-qwen3.8-q6/Qwen3.8-27B-UD-Q6_K_XL`) plus the Model line in AGENTS.md
   section 1. Repo precedent for this exact change: commits `afade6e` and `7f0c6a4`.
   Commit and push.

If the user has already stood the Q5 endpoint up by the time the session starts,
verify it with curl and go straight to step 4.

**EVO-X2 access (192.168.1.106).** `ssh howard@192.168.1.106`. Publickey auth fails.
Use `sshpass -p "$(sed -n 2p ~/ai_machine_pass.md)"` (line 2 of that file is the
password, line 1 the username; never print it or write it down). Model services are
systemd user units under `~/.config/systemd/user/` on the remote. Machine RAM: 92GB.

**Endpoint state at write time (2026-08-22).** Q6/8090
(`llama-server-qwen3.8-27b-q6`, `--parallel 1`) up, ~7.1 t/s, 15GB resident.
Q8/8088 (`llama-server-qwen3.8-27b-q8`, `--parallel 4`) was down when the incident
began (unit missing); it was restored and verified that day. Both stay as fallbacks
after the Q5 re-target.

**What `--parallel` means.** It is the number of concurrent inference slots the
llama.cpp server exposes; each slot has its own KV cache. One slot means every client
queues behind one generation, which is what turned five parallel sessions into five
queued requests each waiting past the 1h timeout. Four slots means up to four
generations in flight. Slots share the same GPU compute, so parallelism buys
concurrency and latency isolation, not 4x throughput. Per-slot KV memory at the 262k
context was not extracted from the logs; the 4-slot Q8 service (30GB weights) loaded
and served fine on the 92GB machine, so four slots fit.

**Dispatch policy (endpoint-bound, also recorded in TASK-0008 `## Status`).** Until
the team runs on the 4-slot Q5 endpoint, at most 2 subagents concurrently
(Q6/8090 is one slot plus a 1h request timeout). Once Q5 is up, run the plan's
parallel waves as written (cap 4): Wave 0 is items 1 ∥ 2 ∥ 3 ∥ 9a, with Amy
(TASK-0009) as the fifth client or held until one finishes. The later review fan-out
is Shadow ∥ Omega together, then Big. Commit target for all cinnamon-for-rocky10
work: feature branch `task-0008-gdm-auth` in the clone (create from main); item 13
PRs it to main. A7 guard: one 4GB VM at a time on the host; check `free -g` before
starting a VM.

**Per-item dispatch notes** (the dead sessions never ran, so these ride along with
the re-dispatch):

- Item 1 (Tails): Sparky host infrastructure per the plan's acceptance criterion.
  Repair the partial Raku install in `~/.raku` first. No commits to the cinnamon
  repo.
- Item 2 (Tails): GDM harness. Owns `tasks/lib/gdm-drive.sh`. xdotool for greeter
  input per the plan; pyatspi2 for post-login verification where an a11y bus exists
  (user standard below). Commits to `task-0008-gdm-auth`.
- Item 3 (Big): static packaging inspection. Read-only on the repo. Writes the
  `## Test Results` pre-section, marks H1–H4 with evidence, decides the input driver
  and LightDM availability, and probes pyatspi2 availability in the VM (verify the
  real package name, do not assume).
- Item 9a (Tails): core Sparrow task suite. Must not write
  `tasks/lib/gdm-drive.sh` (item 2 owns it); reference it only.
- Amy (TASK-0009): exact file list, pyatspi2 integration approach against the Sparky
  source or docs, how the config change is validated, rollback, plus the AGENTS.md
  concurrency-ceiling note.

**The pyatspi2 standard (user, 2026-08-21).** For any desktop application testing
the team uses Sparky plus pyatspi2
(https://gitlab.gnome.org/GNOME/pyatspi2). Recorded in both planning docs' Status. It
feeds item 3's driver decision and item 9a's task design, and it is the substance of
TASK-0009.

**How to run subagents on this local endpoint** (learned the hard way 2026-08-21/22).
The Task tool returns "The operation timed out." after ~60–90s. That is normal; the
subagent session keeps running in the background. Do NOT re-dispatch, which creates
duplicate agents. Poll instead: one bash call, `sleep 600`–`900` with the tool
timeout set above the sleep, then check the artifacts (planning doc sections, `grep
'^### Item'` on the doc; git branch in the clone; `~/.raku/bin/raku`; `curl -sS
localhost:4000`; `virsh list`). A session is done when its deliverable is in its doc
section. It is dead when its last line in `~/.local/share/opencode/log/opencode.log`
is `level=ERROR`, or when no new line appears for ~30+ minutes. If dead, check the
endpoint first (curl), then re-dispatch that one item only.

**First actions of the new session.**

1. Verify the Q5 endpoint (`curl -sS -m 10` against its `/v1/models`). If it is
   absent, stand it up per the four steps in the model decision above. This gates
   everything; no subagent dispatch until the agents' configured model is up.
2. Read `## Status` and `## Next Actions` in both planning docs.
3. Dispatch Wave 0 per the dispatch policy (on 4-slot Q5: items 1 ∥ 2 ∥ 3 ∥ 9a in one
   message, plus Amy or held), then follow each item to completion by polling.
4. Follow the critical paths. TASK-0008: 4 → 5 → 6 → (Shadow ∥ Omega, then Big) →
   8 → 10 → (11) → 12 → 13 → 14. TASK-0009 in parallel once Amy's plan lands:
   Tails → (Shadow ∥ Omega, then Big) → Vector → Knuckles.
5. Keep `## Status` and `## Next Actions` current after every dispatch and every
   completion.

**Standing rules.**

- Launch opencode from `~/AI/projects/team-chaotix` (agents and AGENTS.md only load
  from there).
- Commits and pushes to `metalllinux` repositories need no user confirmation
  (standing permission 2026-08-21).
- A GitHub token is intentionally embedded in this repo's `origin` remote URL
  (`.git/config`) and stays there (user decision, 2026-08-21). Never write it into a
  file, commit, planning doc, or GitHub issue; never stage anything under `.git/`.
- The git clone of the repo under fix is `~/Linux/projects/cinnamon-for-rocky10/`;
  the project dir `~/Linux/projects/cinnamon_4_rocky10/` has no `.git`. Commits go to
  the clone.
- If a dispatch comes back empty with no file changes, suspect the endpoint before
  the agent.
