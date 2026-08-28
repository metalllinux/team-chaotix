# TASK-0013 — README: GMKtec EVO-X2 + Qwen 3.8 UD-Q4_K_XL model host setup

> **Section order below is fixed.** Each agent writes to its own section and no other. `Robotnik`
> reads only `## Status` and `## Next Actions`. Do not reorder, rename, or remove sections.

- **Created:** 2026-08-28

---

## Status

*Owner: `Robotnik`. Keep this SHORT and CURRENT — it is one of only two sections the PM reads, so a
stale entry means the whole loop runs on bad information.*

**Now:** user request (2026-08-27): a README section in `metalllinux/team-chaotix` documenting how
to set up the GMKtec EVO-X2 with `Qwen3.8-27B-UD-Q4_K_XL` as the team's model host — systemd
settings (user supplied the unit file; it matches the reference machine), firewall, model
download from Hugging Face, directory layout, opencode client config, and GPU-wedge avoidance
guidance. `Vector` turn complete 2026-08-28: section written (new `## EVO-X2 model host setup`,
README lines ~398-601, plus a cross-reference sentence in `## Model`), `## Docs` filled, unverified
items marked (unit file beyond `ExecStart`, live firewalld state, ryzenadj purpose, binary
provenance — all settle via `ssh howard@192.168.1.106`, which Vector's loaded bash set blocks;
see TASK-0014). The uncommitted work was shipped by Tails on the TASK-0014 turn in commit
`9e1f0c9` (mixed-scope commit, stated in the message), pushed to main; verification in
`ad9632c`, local HEAD == remote main. Pending: Shadow → Omega review of the README section
against the pushed state; if findings need a fix, Tails fixes + pushes, then `Knuckles` verifies
the DONE checklist and records `## Release`. The ssh verification channel opens for `Vector`
after the next opencode restart.

**Environment / scope:**
- Files in scope: `README.md` (team-chaotix repo, `/home/howard/AI/projects/team-chaotix/`)
- Touches the DB schema: no
- Graphical UI: no
- Rocky Linux target: yes (reference host runs Rocky Linux 10.2 + elrepo kernel)

**Verified reference-machine facts (Robotnik, via `ssh howard@192.168.1.106`, 2026-08-27/28):**
- GMKtec EVO-X2 at 192.168.1.106; Radeon 8060S iGPU (gfx1151, Strix Halo); 92 GiB RAM;
  Rocky Linux 10.2; kernel `7.0.12-1.el10.elrepo.x86_64`.
- llama-server `version: 9671 (c1304d7b2)`, built with GNU 14.3.1, at
  `/usr/local/bin/llama-server` (Vulkan backend; frozen flags include `--n-gpu-layers 99 -fa on`).
- Model dir `/mnt/data/models/qwen3.8-27b-q4/` (`Qwen3.8-27B-UD-Q4_K_XL.gguf` +
  `mmproj-F16.gguf`); endpoint port 8092, `--host 0.0.0.0`.
- **User-level** systemd unit `llama-server-qwen3.8-27b-q4.service` in
  `~/.config/systemd/user/`, **enabled** (exact file supplied by the user and matching the
  machine; auto-restart demonstrated in TASK-0010 — ~5 s after a GPU wedge).
- firewalld running, `public` zone on `eno1`; open ports include 8092/tcp (plus 8080–8088,
  8090, 8084 for the other model endpoints); services: cockpit, dhcpv6-client, ssh.
- opencode client: provider entry `evo-x2-qwen3.8-q4` in `~/.config/opencode/opencode.json`
  (baseURL `http://192.168.1.106:8092/v1`, model `Qwen3.8-27B-UD-Q4_K_XL`, context 262144,
  output 131072).
- Model import procedure: team skills `~/.config/opencode/skills/add-ai-model/SKILL.md` and
  `~/.config/opencode/skills/new-model-import/SKILL.md` (EVO-X2-specific, incl. the Hugging
  Face source).
- GPU wedge record: `planning/docs/TASK-0010-evox2-gpu-wedge-fix.md` — characterization in
  checkpoint 3.1 (power-cap stress; single ~201k cold prefill wedges a fresh chip in ~29 min;
  small delta-prompt work ran 4.5 h clean), runtime surface exhausted in 3.3 (no sysfs knob
  works on the elrepo 7.0.12 driver build; `low` = 4.5x slower, rejected), fresh-chip repro in
  3.4, user decision (accept risk) in the 2026-08-27 12:13 UTC Status entry.
- The reference machine also runs a system-level `ryzenadj.service` — purpose unverified;
  `Vector` verifies on the machine before documenting; omit if not verifiable.

**Unknowns:** the exact HF repo for the model (should be in the skills; verify there, do not
guess); the ryzenadj configuration; whether the llama.cpp binary is a release build or local
build (ask/verify; record what is found, mark the rest unverified).

---

## Definition of Done

*Owner: `Robotnik`, and nobody else. Written **before** any work starts. Objectively checkable —
if a box cannot be verified by looking at something, rewrite it.*

- [ ] `README.md` has a new section on setting up a GMKtec EVO-X2 model host with
      `Qwen3.8-27B-UD-Q4_K_XL`, covering: hardware/OS/kernel requirements; the llama-server
      binary (Vulkan build, the verified version); downloading the model from Hugging Face per
      the team skills; the model directory layout; the user-level systemd unit (exact file +
      user-level enablement + what it does on boot/wedge); the firewall rule for 8092/tcp
      (firewalld, public zone); the opencode provider entry; and the GPU-wedge section (what a
      wedge is, the verified characterization, what works — unit auto-restart, `--mlock`,
      moderate request sizes, the monitoring command — what does not — the exhausted runtime
      sysfs surface — and the correction that the context window was **not** reduced,
      `-c 262144` stays).
- [ ] Every factual claim in the section verified against the reference machine
      (`ssh howard@192.168.1.106`) or cited from a team artifact (planning doc, skills,
      opencode.json); no invented paths, flags, or versions; unverified items marked as such.
- [ ] AGENTS.md §10 writing style applied (no em/en dashes, no colons introducing an
      explanation, prose over bullets for explanation, take a position).
- [ ] `Shadow`: no unresolved blockers or should-fix findings in `## Review`.
- [ ] `Omega`: no unresolved findings above `low` in `## Security`.
- [ ] `Big`: N/A — docs-only change, no executable code (recorded here).
- [ ] Committed + pushed to `metalllinux/team-chaotix` main; local HEAD == remote HEAD
      (verified with `git ls-remote`).

---

## Next Actions

*Owner: whoever wrote last. The future only — delete what has been done. The second of the two sections
the PM reads.*

- [ ] `Shadow` (dispatched 2026-08-28): review the new `## EVO-X2 model host setup` README
      section (lines ~398-601) and the `## Model` cross-reference sentence against `## Status`
      verified facts, `## Definition of Done`, and AGENTS.md §10 style; check the cited sources
      actually say what the section claims. Findings to `## Review`.
- [ ] `Omega` (after Shadow): security pass on the same section — no credentials or tokens in
      the README, firewall guidance least-privilege, documented commands safe to copy. Findings
      to `## Security`.
- [ ] `Knuckles` (after both reviews clean, or after the fix commit if findings required one):
      work already shipped as `9e1f0c9`; verify the DONE checklist, confirm local HEAD == remote
      HEAD with `git ls-remote`, record in `## Release`.

---

## Plan

*Owner: `Amy`.*

**Why this task exists** — the user request or issue it serves.
**What it unblocks / what blocks it** — including dependencies outside this repo.
**MVP** — the smallest version that delivers value, and what is deferred.
**What this makes harder later.**

**Work breakdown** — decomposed until one agent finishes one item in one turn.

| # | Item | Owner agent | Acceptance criterion | Parallel with |
|---|---|---|---|---|
| 1 | | | | |

**Critical path:**
**Validation:** which files, which checks, which pages need a human look. Name them.
**Rollback:** how we detect failure, the exact revert, and where the point of no return is.

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
**Where:** `path/to/file:line`
**Problem:** one sentence.
**Failure scenario:** concrete inputs/state → the wrong outcome.
**Suggested direction:** what to do instead.
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

---

## Security

*Owner: `Omega`. Read-only. Severity order.*

### <short claim>
**Severity:** critical | high | medium | low
**Vector:** injection | authz | secrets | input-validation | crypto | supply-chain | actions | license
**Where:** `path/to/file:line`
**Attack:** who the attacker is, what they control, the concrete steps.
**Impact:** what the attacker gains.
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
| `README.md` | `## Model` (cross-reference sentence appended, line 395-396); new `## EVO-X2 model host setup` (lines 398-601) with subsections Hardware and software, Model files, The systemd unit, Firewall, The opencode client, The GPU wedge, Verification after setup | New section documents the EVO-X2 model host per `## Status` facts and `## Definition of Done`. Hardware/OS/kernel (Ryzen AI MAX+ 395 Strix Halo, Radeon 8060S gfx1151, 92 GB unified, Rocky 10.2, elrepo kernel `7.0.12-1.el10.elrepo.x86_64`); llama.cpp Vulkan binary version 9671 (commit `c1304d7b2`), built with GNU 14.3.1; HF download per the `add-ai-model` skill (repo `unsloth/Qwen3.8-27B-GGUF`, `hf` CLI, magic-header check); model dir `/mnt/data/models/qwen3.8-27b-q4/` layout; user-level unit with the `ExecStart` line verified on the live process (TASK-0010 checkpoint 3.2, `planning/docs/TASK-0010-evox2-gpu-wedge-fix.md:503-505`) and the remaining lines from the team unit template (`~/.config/opencode/skills/add-ai-model/SKILL.md:81-101`); firewalld rule for 8092/tcp (public zone on eno1, ports and services per `## Status`); opencode provider entry verbatim (`~/.config/opencode/opencode.json:121-137`); GPU wedge section with the verified characterization (TASK-0010 checkpoints 3.1/3.3/3.4), what works (unit auto-restart 5-11 s, `--mlock` 5.1 s reload, moderate request/session sizes, `journalctl` monitoring command per `planning/docs/TASK-0010-evox2-gpu-wedge-fix.md:93-94`), what is exhausted (sysfs surface, `low` at 4.5x slower), and the correction that the context window was not reduced and `-c 262144` stays |

**Verified by `Vector` this turn (local artifacts, read directly):**
- Provider entry `evo-x2-qwen3.8-q4` in `~/.config/opencode/opencode.json:121-137` (baseURL
  `http://192.168.1.106:8092/v1`, timeout 3600000, context 262144, output 131072)
- Download procedure and unit template in `~/.config/opencode/skills/add-ai-model/SKILL.md`
  (HF repo `unsloth/Qwen3.8-27B-GGUF`, `hf` CLI, GGUF magic `4747 5546`, port range 8080-8099,
  one active model at a time); `new-model-import/SKILL.md` best practices
- TASK-0010 wedge guidance, targeted reads: 11:10 UTC and 12:13 UTC Status entries (lines
  15-36), checkpoint 3.1 (lines 397-484), 3.3 (lines 551-598), 3.4 (lines 611-640), monitoring
  command (lines 93-94)
- `/home/howard/AI/projects/qwen-38-q5-fixes/qwen38-q5-fixes.md` (hardware spec lines 3-5,
  monitoring lines 142-144, fit-degradation table lines 64-69, 12 s load window lines 99-101,
  26-wedge history lines 113-122, 40 GB pool hold lines 78-83)
- Reference-machine facts cited from `## Status` above (Robotnik, ssh-verified 2026-08-27/28),
  which the DoD permits as team artifacts

**Checked and needed no change:**
- `AGENTS.md` (Model line already matches the reference endpoint, `evo-x2-qwen3.8-q4` port 8092
  `--parallel 1`; no setup detail belongs there)
- `planning/docs/TASK-0010-evox2-gpu-wedge-fix.md` (read-only source, untouched)
- Both team skills and `~/.config/opencode/opencode.json` (read-only sources, untouched)
- No `CHANGELOG.md` exists in this repository, so no changelog entry
- `planning/docs/TASK-0011-default-model-q4kxl.md` (Status read; its `--parallel 4` note is
  historical, dated 2026-08-25, predating the single-slot change) and
  `TASK-0012-single-slot-sequencing.md` (Status read via grep; records the user's `--parallel 1`
  decision, which is the state the README documents). The `--parallel 1` deviation from the skill
  template is explained in the README with the measured fit ceiling and the accepted queuing
  trade

**Could not verify (and what would settle it):**
- Unit file text beyond `ExecStart` (Description, After/Wants, Type, LimitMEMLOCK, WantedBy).
  Vector's bash permission set (exact `git status`, `git log*`, `git diff*`, `rg *` only) blocks
  `ssh howard@192.168.1.106`, so the file could not be read on the machine. The README marks
  `ExecStart` as the verified line and the rest as the team template. Settled by
  `ssh howard@192.168.1.106 'cat ~/.config/systemd/user/llama-server-qwen3.8-27b-q4.service'`
- Current live firewalld state. Cited from Robotnik's 2026-08-27/28 verification in `## Status`.
  Settled by `sudo firewall-cmd --list-all` on the machine
- `ryzenadj.service` purpose. Omitted from the README per the task instruction (document only if
  verifiable); no team artifact records its purpose. Settled by
  `systemctl cat ryzenadj.service` plus its config file on the machine
- llama.cpp binary provenance (upstream release or local build). Not claimed in the README.
  Settled by asking the user or inspecting the build host

**Commit status:** the README change is written but uncommitted. Vector's permission set also
denies `git commit`, `git push`, and `git ls-remote`, so the commit + push + remote-HEAD
verification in `## Definition of Done` could not run from this role. `git status` shows the
working tree dirty with `README.md` and this planning doc modified, and `git log --oneline -1`
shows HEAD at `d476221` (unchanged, up to date with `origin/main`). Knuckles or the user must
commit both files, push, and verify the remote HEAD.

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
lost. Decisions, verified facts, rejected options with their reasons, known traps, and anything
the user said are never deleted.*

**Pruning log**

| Date | What was pruned or compressed | Rough size |
|---|---|---|
| | | |
