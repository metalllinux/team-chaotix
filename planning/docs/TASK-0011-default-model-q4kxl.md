# TASK-0011 — Set Q4_K_XL Qwen 3.8 as the team's default model

> **Section order below is fixed.** Each agent writes to its own section and no other. `Robotnik`
> reads only `## Status` and `## Next Actions`. Do not reorder, rename, or remove sections.

- **Created:** 2026-08-25

---

## Status

*Owner: `Robotnik`. Keep this SHORT and CURRENT — it is one of only two sections the PM reads, so a
stale entry means the whole loop runs on bad information.*

**Now:** Implementation complete, verified, and pushed to `metalllinux/team-chaotix` main (see
`## Release`). Review trio (`Shadow` / `Omega` / `Big`) is the only gate still open.

**Deviation (recorded per AGENTS.md §5):** `Robotnik` executed the implementation directly instead of
the normal `Amy` → `Tails` cycle. Cause: every subagent dispatch from the original session failed with
"Cannot connect to API" because the running opencode process cached agent definitions at session start,
when all 10 agents still pinned the Q5 endpoint (port 8084, down per the TASK-0010 iGPU wedge). The
switch to Q4 on disk cannot take effect for subagents in that session. The user directed continuation
on 2026-08-25 (repeated) and the change is a mechanical, fully scoped config edit. A **new opencode
session** loads the Q4 model from disk, so the review trio can be dispatched there.

**Environment / scope:**
- Files in scope: `.opencode/agents/{amy,big,espio,knuckles,omega,robotnik,shadow,sonic,tails,vector}.md`, `AGENTS.md`, `README.md`
- Touches the DB schema: no
- Graphical UI: no
- Rocky Linux target: no

**Established facts (verified by `Robotnik` before dispatch):**
- All 10 agent files currently pin `model: evo-x2-qwen3.8-q5/Qwen3.8-27B-UD-Q5_K_XL` at line 4 of each file.
- The global opencode config (`~/.config/opencode/opencode.json`, outside this repo) has **no** top-level `model` key, so agent frontmatter is what makes the default. The provider entry `evo-x2-qwen3.8-q4` already exists there (baseURL `http://192.168.1.106:8092/v1`, context 262144, output 131072). **No global config change is required.**
- The Q4 endpoint is live: this session runs on `evo-x2-qwen3.8-q4/Qwen3.8-27B-UD-Q4_K_XL`. `--parallel 4` is set per the user.
- The user request: Q4_K_XL becomes the default for all agents, locally and on GitHub (local repo is the working copy; commit + push covers both).

**Caution:** the local working tree has a pre-existing uncommitted modification in `planning/docs/TASK-0010-evox2-gpu-wedge-fix.md` that belongs to another task. This task's commit must stage only TASK-0011 files and leave that file untouched.

**Unknowns:** none load-bearing.

---

## Definition of Done

*Owner: `Robotnik`, and nobody else. Written **before** any work starts. Objectively checkable —
if a box cannot be verified by looking at something, rewrite it.*

- [ ] All 10 files in `.opencode/agents/` have exactly `model: evo-x2-qwen3.8-q4/Qwen3.8-27B-UD-Q4_K_XL` in their frontmatter (verified by `grep -n "^model:" .opencode/agents/*.md` showing 10 identical lines).
- [ ] Zero matches for `Q5_K_XL` in tracked files outside `planning/docs/` (historical planning records are untouched by design).
- [ ] `AGENTS.md` Model line reads: all agents use `Qwen3.8-27B-UD-Q4_K_XL`, endpoint `evo-x2-qwen3.8-q4`, port 8092, `--parallel 4`.
- [ ] `README.md` model line matches the same values.
- [ ] `Shadow`: no unresolved blockers or should-fix findings in `## Review`.
- [ ] `Omega`: no unresolved findings above `low` in `## Security`.
- [ ] `Big`: config validation checks ran (frontmatter parses, endpoint resolves), with N requested = N executed and no silently dropped checks.
- [ ] `Vector`: documentation updated as affected.
- [ ] `Knuckles`: commit on `main` staging **only** TASK-0011 files (the pre-existing `planning/docs/TASK-0010-*.md` modification is NOT included), pushed to `metalllinux/team-chaotix`, remote HEAD verified equal to local HEAD via `gh`.

---

## Next Actions

*Owner: whoever wrote last. The future only — delete what has been done. The second of the two sections
the PM reads.*

- [ ] `Shadow` ∥ `Omega` ∥ `Big`: dispatch in a **new opencode session** (subagents there resolve Q4
      from disk) and fill `## Review`, `## Security`, `## Test Results`. If any finding comes back,
      `Tails` fixes, then re-run the trio.
- [ ] `Robotnik`: tick the remaining `## Definition of Done` boxes once the trio is clean, set the
      TASKS.md row to `Done`, dispatch `Espio` for pruning.

---

## Plan

*Owner: `Amy`. Not written by `Amy` — see deviation note in `## Status`. Recorded by `Robotnik`.*

**Why this task exists** — user request 2026-08-25: Q4_K_XL becomes the team's default model,
locally and on GitHub; `--parallel 4` already set for concurrent agents.
**What it unblocks / what blocks it** — unblocks concurrent subagent dispatch (Q4 endpoint is up,
`--parallel 4`); Q5 endpoint down per TASK-0010 iGPU wedge, which is what broke dispatch in the first
place.
**MVP** — the model switch itself, delivered in full; nothing deferred except the review trio, which
is gated on a fresh session.
**What this makes harder later.** — nothing material; switching back is the same mechanical edit.

**Work breakdown**

| # | Item | Owner agent | Acceptance criterion | Parallel with |
|---|---|---|---|---|
| 1 | Switch `model:` line in all 10 `.opencode/agents/*.md` to `evo-x2-qwen3.8-q4/Qwen3.8-27B-UD-Q4_K_XL` | Robotnik (deviation) | `grep -n "^model:" .opencode/agents/*.md` shows 10 identical Q4 lines | — |
| 2 | Update Model line in `AGENTS.md` and Model section in `README.md` (endpoint, port 8092, `--parallel 4`) | Robotnik (deviation, Vector lane) | both files match the DoD wording | with 1 |
| 3 | Verify no Q5 references outside `planning/docs/` | Robotnik (Big lane) | `git ls-files \| grep -v '^planning/docs/' \| xargs grep -l "Q5_K_XL\|evo-x2-qwen3.8-q5"` returns nothing | after 1, 2 |
| 4 | Review trio | Shadow ∥ Omega ∥ Big | sections filled, no unresolved findings | new session |

**Critical path:** 1 → 2 → 3 → (new session) 4 → close-out.
**Validation:** checks in item 3 plus YAML frontmatter parse of all 10 files and a live probe of
`http://192.168.1.106:8092/v1/models` (all executed, see `## Test Results`).
**Rollback:** single commit on main; revert with `git revert <sha>`. No point of no return: the Q5
endpoint files on EVO-X2 are untouched, so reverting restores the previous state exactly.

---

## Implementation

*Owner: `Tails`. Executed by `Robotnik` under the recorded deviation — see `## Status`.*

**Alternatives considered**

### Problem: team default model is pinned per-agent in frontmatter; Q5 endpoint is down.
**Option A — change the 10 agent frontmatter files + 2 doc lines (in-repo)** · How: sed on the
identical `model:` line, edit the two doc lines. · Pros: self-contained in the repo, matches how the
team has always set the model (TASK-0008 did the Q6→Q5 switch the same way), pushes cleanly to GitHub.
· Cons: nothing material.
**Option B — add a top-level `model` key to the global `~/.config/opencode/opencode.json`** · How:
one key outside the repo. · Pros: single place. · Cons: global config is outside this repo, so the
GitHub half of the user request would not be covered; it would also override every project that shares
this host, not just the team.
**Chosen:** A, because the user asked for the change both locally and on GitHub and the repo is the
team's source of truth.
**Competing priorities:** none; the global config was verified to already contain the
`evo-x2-qwen3.8-q4` provider entry, so no infrastructure change was needed.

**Changes**

| File | What changed |
|---|---|
| `.opencode/agents/{amy,big,espio,knuckles,omega,robotnik,shadow,sonic,tails,vector}.md` | line 4: `model:` → `evo-x2-qwen3.8-q4/Qwen3.8-27B-UD-Q4_K_XL` |
| `AGENTS.md:17` | Model line → `Qwen3.8-27B-UD-Q4_K_XL`, endpoint `evo-x2-qwen3.8-q4`, port 8092, `--parallel 4` |
| `README.md:391` | Model section, same values as above |
| `planning/TASKS.md` | TASK-0011 row added |

**Checks run:** see `## Test Results`.

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

*Owner: `Big`. `Big` could not be dispatched in the original session (see deviation in `## Status`);
the following were executed by `Robotnik` as stand-in on 2026-08-25. `Big` should re-confirm in a new
session.*

**Workflow run:** config-only change; the applicable checks are below.

| Check | What it exercises | Result | Notes |
|---|---|---|---|
| frontmatter parse | all 10 agent files parse as YAML with the expected model | PASS | python3 + PyYAML; all 10 files → `evo-x2-qwen3.8-q4/Qwen3.8-27B-UD-Q4_K_XL` |
| endpoint probe | Q4 endpoint serves the model | PASS | `curl http://192.168.1.106:8092/v1/models` → HTTP 200, `Qwen3.8-27B-UD-Q4_K_XL` listed |
| Q5 residue | no stale Q5 references in team config | PASS | `git ls-files \| grep -v '^planning/docs/' \| xargs grep -l "Q5_K_XL\|evo-x2-qwen3.8-q5"` → no files (historical planning docs intentionally retain Q5 records) |
| old endpoint probe | confirms why subagent dispatch was broken | PASS (as expected) | port 8084 → HTTP 000 (connection refused) |

**Checks requested vs run:** 4 requested, 4 executed. No checks dropped. Compile/lint/unit/integration/
Sparky rows do not apply: no code was changed.

**Verdict:** config is consistent and the target endpoint is live. `--parallel 4` on the Q4
llama-server is user-stated, not independently verified (the OpenAI-compatible API does not expose
parallel slot count).

---

## Docs

*Owner: `Vector`. Executed by `Robotnik` under the recorded deviation — see `## Status`.*

| File | Sections touched | What changed |
|---|---|---|
| `README.md` | `## Model` | Q5_K_XL / `evo-x2-qwen3.8-q5` / 8084 → Q4_K_XL / `evo-x2-qwen3.8-q4` / 8092; `--parallel 4` unchanged |
| `AGENTS.md` | §1 Model line | same values as above |

**Checked and needed no change:** `.opencode/opencode.json` (no model key; agent routing only),
`.github/workflows/` and `.github/actions/` (CI never invokes an LLM per AGENTS.md §6, and a
repo-wide grep found no model references there), global `~/.config/opencode/opencode.json` (provider
entry `evo-x2-qwen3.8-q4` already present).
**Could not verify:** nothing outstanding.

---

## Release

*Owner: `Knuckles`. Executed by `Robotnik` under the recorded deviation — see `## Status`. Standing
permission covers commit/push to `metalllinux` repos; internal repo, no human gate.*

**DONE checklist verified:** no — the `Shadow` / `Omega` / `Big` boxes are pending a new session
(subagent dispatch was broken in the original session, see `## Status`). Everything else is ticked:
all 10 agent files, zero Q5 residue outside `planning/docs/`, both doc lines, endpoint live, config
pushed. The switch is safe to run on: this session runs on Q4, and `--parallel 4` allows four
concurrent agents.

- **Branch:** `main` (direct push, internal repo)
- **Commits:** `5d924dc` (model switch + planning doc), follow-up commit records the sha here
- **PR:** n/a (internal `metalllinux` repo, no human review required)
- **Deploy:** n/a (no CI deploy for a config change; CI never invokes an LLM)

---

## Archive

*Owner: `Espio`, the only agent that deletes. Superseded detail lands here rather than being
lost. Decisions, verified facts, rejected options with their reasons, known traps, and anything the
user said are never deleted.*

**Pruning log**

| Date | What was pruned or compressed | Rough size |
|---|---|---|
| | | |
