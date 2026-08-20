# TASK-0008 — Fix GDM Cinnamon-session login Authentication Error; widen VM test matrix

> **Section order below is fixed.** Each agent writes to its own section and no other. `Robotnik`
> reads only `## Status` and `## Next Actions`. Do not reorder, rename, or remove sections.

- **Created:** 2026-08-20

---

## Status

*Owner: `Robotnik`. Keep this SHORT and CURRENT — it is one of only two sections the PM reads, so a
stale entry means the whole loop runs on bad information.*

**Now:** Planning, paused for handoff. User hit a GDM "Authentication Error" selecting the
Cinnamon session on Rocky Linux 10.2 (Cinnamon RPMs installed from the local DNF repo per
INSTALL.md, GDM + GNOME pre-existing); a reboot restored the session. `## Plan` not yet written.
Decision (user, 2026-08-20): team model retargeted to
`evo-x2-qwen3.8-q8/Qwen3.8-27B-UD-Q8_K_XL` on port 8088 (live). The old BF16 endpoint 8086 is
down and was silently killing subagent dispatches (two empty `Amy` runs, no file changes).
Config edits are owned by a Build agent session because Robotnik's edit scope is intentionally
`planning/**` only; a fresh Robotnik session then dispatches `Amy`.

**Environment / scope:**
- Files in scope: `metalllinux/cinnamon-for-rocky10` repo (main), project dir
  `~/Linux/projects/cinnamon_4_rocky10/` (spec files, session files, PAM-related packaging);
  new Sparky/Sparrow test harness (location decided by `Big`)
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

- [ ] `Build` (user-switched session, this repo): retarget the team model, then commit and push
      to `metalllinux/team-chaotix` main:
      - `.opencode/agents/{amy,big,espio,knuckles,omega,robotnik,shadow,sonic,tails,vector}.md`
        line 4: `model: evo-x2-qwen3.8/Qwen3.8-27B-BF16` ->
        `model: evo-x2-qwen3.8-q8/Qwen3.8-27B-UD-Q8_K_XL`
      - `AGENTS.md:17-20` and `README.md:391-394`: replace the Model paragraph to name
        `evo-x2-qwen3.8-q8/Qwen3.8-27B-UD-Q8_K_XL` at `http://192.168.1.106:8088/v1`, with the
        Qwen3.8-BF16 (8086) and Qwen3.6-27B (8085) services disabled because the models do not
        share GPU memory
      - verify afterwards: `grep -rn "Qwen3.8-27B-BF16\|:8086" .opencode AGENTS.md README.md`
        returns nothing
- [ ] `user`: start a fresh opencode session from this directory and paste
      `planning/docs/TASK-0008-new-session-prompt.md` (the original task brief, verbatim)
- [ ] `Amy` (fresh session): write `## Plan` — VM reproduction plan, root-cause hypotheses to
      check (PAM, session files, packaging deps, GDM/GNOME interaction), fix approach,
      Sparky/Sparrow test matrix and harness layout, rollback. Before the first dispatch, verify
      the 8088 endpoint is up: `curl -sS -m 10 http://192.168.1.106:8088/v1/models`.

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
