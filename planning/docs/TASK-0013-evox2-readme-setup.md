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
guidance. `Vector` dispatched 2026-08-28.

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

- [ ] `Vector` (dispatched 2026-08-28): write the README section per `## Status` (verified
      facts + source pointers) and `## Definition of Done`. Verify each fact before writing:
      unit file + firewalld state via `ssh howard@192.168.1.106` (sudo available); download
      procedure from the two team skills; provider entry from `~/.config/opencode/opencode.json`;
      wedge guidance from the TASK-0010 doc (2026-08-27 11:10 UTC + 12:13 UTC Status entries,
      checkpoints 3.1/3.3/3.4 — targeted reads, the doc is long). Include the correction the
      user asked for: the context window was not reduced; `-c 262144` stays; wedge avoidance is
      the auto-restarting unit + moderate request/session sizes + monitoring. Style per
      AGENTS.md §10. Commit + push to main, verify remote HEAD, fill `## Docs`.

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
| `README.md` | | |

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
lost. Decisions, verified facts, rejected options with their reasons, known traps, and anything
the user said are never deleted.*

**Pruning log**

| Date | What was pruned or compressed | Rough size |
|---|---|---|
| | | |
