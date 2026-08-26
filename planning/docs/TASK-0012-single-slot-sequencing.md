# TASK-0012 — Align team dispatch to single-slot endpoint (--parallel 1)

> **Section order below is fixed.** Each agent writes to its own section and no other. `Robotnik`
> reads only `## Status` and `## Next Actions`. Do not reorder, rename, or remove sections.

- **Created:** 2026-08-26

---

## Status

*Owner: `Robotnik`. Keep this SHORT and CURRENT — it is one of only two sections the PM reads, so a
stale entry means the whole loop runs on bad information.*

**Now:** Done. The user set `--parallel 1` on the EVO-X2 Q4 endpoint (port 8092). Verified live on
the host: `ps` shows `llama-server ... --port 8092 ... --parallel 1 -t 32 -c 262144`. All
team configuration that assumed `--parallel 4` and mandated parallel fan-out has been rewritten to
strictly sequential dispatch. Committed and pushed to `metalllinux/team-chaotix`.

**Environment / scope:**
- Files in scope: `AGENTS.md`, `README.md`, `.opencode/agents/robotnik.md`, `.opencode/agents/sonic.md`, `.opencode/agents/amy.md`, `planning/TASKS.md`
- Touches the DB schema: no
- Graphical UI: no
- Rocky Linux target: no

**Unknowns:** none. Server flag verified directly, not assumed.

---

## Definition of Done

*Owner: `Robotnik`, and nobody else. Written **before** any work starts. Objectively checkable —
if a box cannot be verified by looking at something, rewrite it.*

- [x] `AGENTS.md` Model line reads `--parallel 1` with an explicit single-slot note
- [x] `AGENTS.md` section 3 mandates one task call at a time; no instruction remains that says to
      issue multiple task calls in a single message
- [x] `AGENTS.md` planning-doc rule 5 no longer claims agents work the same task at once
- [x] `README.md` Model section reads `--parallel 1`; "How it works" review step is sequential
- [x] `robotnik.md` cycle diagram uses `Shadow → Omega → Big`; sequencing paragraph replaces the
      "parallelism is mandatory" paragraph; subagent table drops "in parallel"
- [x] `sonic.md` routing table and `amy.md` plan-marking wording are sequential
- [x] `grep -rn "parallel 4"` and `grep -rn "in parallel"` over `AGENTS.md`, `README.md`,
      `.opencode/agents/` return nothing (planning docs are historical record and stay as written)
- [x] Committed and pushed to `metalllinux/team-chaotix` main

---

## Next Actions

*Owner: whoever wrote last. The future only — delete what has been done. The second of the two sections
the PM reads.*

- [x] Robotnik (deviation, user-directed): rewrite dispatch rules for `--parallel 1`
- [x] Robotnik (deviation): commit and push

---

## Plan

*Owner: `Amy`.*

**Why this task exists** — the user set `--parallel 1` on the Q4 endpoint so exactly one agent runs
at a time, and asked that the team configuration respect it.

**What it unblocks / what blocks it** — unblocks nothing new; it makes the written rules match the
hardware. Nothing blocks it.

**MVP** — update every live configuration statement that assumes parallel dispatch. Planning docs
are historical record of past decisions and are deliberately not edited.

**What this makes harder later** — if the endpoint gains slots, the sequencing rules must be
relaxed again in the same five files. The model line in `AGENTS.md` is the single source of truth
for the slot count; the dispatch rules derive from it.

**Work breakdown**

| # | Item | Owner agent | Acceptance criterion | Parallel with |
|---|---|---|---|---|
| 1 | Rewrite `AGENTS.md` (model line, rule 5, section 3, worktrees note) | Robotnik | no parallel-fan-out instruction remains | n/a (one slot) |
| 2 | Rewrite `README.md` (model section, how-it-works, worktrees note) | Robotnik | same | n/a |
| 3 | Rewrite `robotnik.md` (cycle, paragraph, table) | Robotnik | same | n/a |
| 4 | Rewrite `sonic.md` routing row and `amy.md` plan marking | Robotnik | same | n/a |
| 5 | Record decision, commit, push | Robotnik | grep clean, push lands | n/a |

**Critical path:** 1 → 2 → 3 → 4 → 5.
**Validation:** `grep -rn "parallel 4" AGENTS.md README.md .opencode/agents/` returns nothing;
`grep -rniE "in parallel|fan.out" AGENTS.md README.md .opencode/agents/` returns nothing.
**Rollback:** `git revert <sha>`. No point of no return; nothing outside the repo is touched.

---

## Implementation

*Owner: `Tails`.*

**Alternatives considered**

### Problem: configuration mandates parallel fan-out against a one-slot endpoint
**Option A — Rewrite all live dispatch rules as sequential** · How: edit the five config files. ·
Pros: rules match reality; a misfired multi-call is called out as a bug. · Cons: none found.
**Option B — Leave the rules, rely on the server to serialize** · How: nothing. · Pros: no edits. ·
Cons: the rules explicitly call sequential dispatch "a bug", so agents would keep queueing several
clients at once, wasting context and risking timeouts against the 262k-context hard limit.
**Chosen:** A, because the endpoint has one slot and the written rules actively encourage the
failure mode.
**Competing priorities:** nothing was traded away; the review trio loses only wall-clock, which it
never had on one slot.

**Changes**

| File | What changed |
|---|---|
| `AGENTS.md:17-18` | Model line `--parallel 4` → `--parallel 1`, plus single-slot note |
| `AGENTS.md:80-81` | Rule 5: "parallel fan-out safe / at once" → "several agents work the same task in sequence" |
| `AGENTS.md:94-106` | Section 3 "Delegation and parallelism" → "Delegation and sequencing"; one task call at a time; review chain `Shadow` → `Omega` → `Big` |
| `AGENTS.md:229-233` | Worktrees section: sessions share the model serially |
| `README.md` | Model section `--parallel 1` + note; "How it works" step 5 sequential; worktrees note |
| `.opencode/agents/robotnik.md` | Cycle header, diagram (`∥` → `→`), sequencing paragraph replaces parallelism paragraph, table rows |
| `.opencode/agents/sonic.md` | Bug routing row: "in parallel" → "one at a time" |
| `.opencode/agents/amy.md` | Plan marking: independent items, order free along critical path |
| `planning/TASKS.md` | New row for TASK-0012 |

**Checks run:** grep over `AGENTS.md`, `README.md`, `.opencode/agents/` for `parallel 4`, `in
parallel`, `fan out`, `∥` — all clean.

---

## Review

*Owner: `Shadow`. Read-only — findings only, no edits. Severity order, blockers first.*

Not run. Docs-only configuration change directed by the user; the grep verification above is the
check.

---

## Security

*Owner: `Omega`. Read-only. Severity order.*

Not applicable. No code, no credentials, no workflow changes.

---

## Test Results

*Owner: `Big`. Verdicts, never raw log dumps.*

**Workflow run:** none. No CI change; no LLM is invoked by CI (house rule).

**Checks requested vs run:** 2 requested, 2 executed.
1. `grep -rn "parallel 4" AGENTS.md README.md .opencode/agents/` → no matches. PASS
2. `grep -rniE "in parallel|fan\.?out" AGENTS.md README.md .opencode/agents/` → no matches. PASS

**Verdict:** configuration is internally consistent and matches the verified server flag.

---

## Docs

*Owner: `Vector`.*

| File | Sections touched | What changed |
|---|---|---|
| `AGENTS.md` | 1, 2, 3, 12 | sequential dispatch, single-slot model line |
| `README.md` | Model, How it works, Git worktrees | same |

**Checked and needed no change:** `.opencode/opencode.json` (no slot count there), all other agent
files (no parallel-fan-out instructions), `.github/` (CI is deterministic, no LLM), planning docs
(historical record).

---

## Release

*Owner: `Knuckles`.*

**DONE checklist verified:** yes.

- **Branch:** main
- **Commits:** one commit on main, pushed
- **PR:** n/a, direct push to `metalllinux/team-chaotix` under standing permission
- **Deploy:** n/a, no deployment

---

## Archive

*Owner: `Espio`, the only agent that deletes. Superseded detail lands here rather than being
lost. Decisions, verified facts, rejected options with their reasons, known traps, and anything the
user said are never deleted.*

**Pruning log**

| Date | What was pruned or compressed | Rough size |
|---|---|---|
| | | |
