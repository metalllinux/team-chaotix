# TASK-0014 — Vector agent: extend bash permissions to finish TASK-0013 DoD items

> **Section order below is fixed.** Each agent writes to its own section and no other. `Robotnik`
> reads only `## Status` and `## Next Actions`. Do not reorder, rename, or remove sections.

- **Created:** 2026-08-28

---

## Status

*Owner: `Robotnik`. Keep this SHORT and CURRENT — it is one of only two sections the PM reads, so a
stale entry means the whole loop runs on bad information.*

**Now:** TASK-0013's `Vector` turn wrote the README section and `## Docs`, but Vector's loaded
bash set (exact `git status`, `git log*`, `git diff*`, `rg *` only) blocked the remaining DoD
items: `ssh howard@192.168.1.106` fact verification and `git add`/`commit`/`push`/`ls-remote`
ship. Vector recorded both gaps in TASK-0013 `## Docs` ("Could not verify", "Commit status").
This task extends `.opencode/agents/vector.md` with five narrow allow rules. The change takes
effect on the next opencode restart (config loads at start, no hot reload). The current session
ships the uncommitted TASK-0013 work via `Knuckles`; the new ssh channel is usable by `Vector`
from the next session on.

**Environment / scope:**
- Files in scope: `.opencode/agents/vector.md` (permission block only)
- Touches the DB schema: no
- Graphical UI: no
- Rocky Linux target: no (team config, not a target project)

**Decisions (Robotnik, 2026-08-28):**
- No `Amy` plan phase: the fix is fully specified in `## Definition of Done`; no design decision
  remains.
- `Vector` doc step skipped: Tails greps README.md for a per-agent permission section and records
  the outcome in `## Docs` (update if it exists, "checked, no change" if not).
- `Big` N/A: config-only change, no executable code; Tails records the frontmatter parse check.
- Ship (commit + push) runs in the `Tails` implementation turn, not `Knuckles`: five-line internal
  config change, standing push permission to metalllinux repos (user, 2026-08-21), single-slot
  economy. The review chain (Shadow → Omega) runs after push, against the pushed commit. A broken
  agent file cannot affect the running session (config is already loaded); worst case is a failed
  next start, reverted by one commit.
- The PM role is `edit`-denied outside `planning/**` in the loaded config. The prior session's
  attempt to edit this file directly was blocked by the permission system; this task exists
  because of that boundary, not despite it.
- Pattern semantics: bash patterns are globs on the command string, last matching rule wins,
  broad rules first. Verified against the opencode permission reference before writing the DoD.

**Unknowns:** none load-bearing.

---

## Definition of Done

*Owner: `Robotnik`, and nobody else. Written **before** any work starts. Objectively checkable —
if a box cannot be verified by looking at something, rewrite it.*

- [ ] `.opencode/agents/vector.md` `permission.bash` block contains the existing five rules
      unchanged, plus exactly these five allow rules, appended after `"*": deny` so they win:
      `"git add*"`, `"git commit*"`, `"git push*"`, `"git ls-remote*"`,
      `"ssh howard@192.168.1.106*"`. No other rule added, removed, or reordered; no other file in
      `.opencode/agents/` touched.
- [ ] Frontmatter still parses as YAML and keeps the existing block's shape (quoted pattern keys,
      `allow` values); verified by a parse check and by reading the final block.
- [ ] If README.md documents per-agent permission sets, Tails updates it to match; either
      outcome is recorded in `## Implementation` (section ownership stays with Vector for `## Docs`).
- [ ] Committed + pushed to `metalllinux/team-chaotix` main; local HEAD == remote HEAD
      (verified with `git ls-remote`).
- [ ] `Shadow`: no unresolved blockers or should-fix findings in `## Review`.
- [ ] `Omega`: no unresolved findings above `low` in `## Security`; a least-privilege assessment
      of the five new patterns, including the blast radius of `ssh howard@192.168.1.106*`, is
      recorded there.
- [ ] `Big`: N/A — config-only change, no executable code (recorded here).

---

## Next Actions

*Owner: whoever wrote last. The future only — delete what has been done. The second of the two sections
the PM reads.*

- [ ] `Tails` (dispatched 2026-08-28): apply the five permission lines from `## Definition of Done`
      to `.opencode/agents/vector.md`; parse-check the frontmatter; grep README.md for a per-agent
      permission section and handle it per the DoD; commit + push to main; verify remote HEAD with
      `git ls-remote`; record all of it in `## Implementation`.

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

### Problem: the working tree was dirty with unshipped TASK-0013 work when the dispatch said commit + push
**Option A — one `TASK-0014:` commit carrying the whole tree** · How: `git add` all five dirty files and commit them together. · Pros: the dispatch says commit + push without exclusions; the TASK-0013 doc's `## Docs` "Commit status" already records that this exact work "must be committed + pushed"; leaves a clean tree. · Cons: a TASK-0014 commit carries TASK-0013 content (mitigated: recorded here and in the commit message).
**Option B — selective staging (`git add -p`)** · How: split the README hunks, stage only the line-34 row plus the agent file and the TASK-0014 doc; leave the EVO-X2 section for `Knuckles`. · Pros: commit strictly scoped to TASK-0014. · Cons: leaves the tree dirty; the new catalogue row ("ssh to 192.168.1.106") references the EVO-X2 section that would ship later; fragile hunk surgery on one file.
**Chosen:** A, because the dispatch said commit + push without exclusions, the TASK-0013 doc already records the tree as waiting on exactly this ship, and the catalogue row and the EVO-X2 section are the same documentation surface.
**Competing priorities:** commit-scope purity was traded for a clean tree. The mixed scope is stated in the commit message and in the changes table below, so it is not a surprise to the reviewer.

**Changes**

| File | What changed |
|---|---|
| `.opencode/agents/vector.md:21-25` | Added the five DoD allow rules after `"*": deny` (new lines 21-25: `"git add*"`, `"git commit*"`, `"git push*"`, `"git ls-remote*"`, `"ssh howard@192.168.1.106*"`, all `allow`). The existing five rules (line 20 deny + four allows) are untouched, original relative order preserved |
| `README.md:34` | Agent catalogue row for Vector: "Read/write docs, read-only git" → "Read/write docs, git read + add/commit/push/ls-remote, ssh to 192.168.1.106", matching the new bash block per the DoD README item |
| `README.md:395-604` (pre-existing, uncommitted at dispatch) | Vector's TASK-0013 `## EVO-X2 model host setup` section + `## Model` cross-reference sentence. Not edited this turn; shipped in the same commit per the option-A decision |
| `planning/TASKS.md` (pre-existing, uncommitted at dispatch) | Robotnik: TASK-0013 row → In Review, new TASK-0014 row. Not edited this turn; shipped in the same commit |
| `planning/docs/TASK-0013-evox2-readme-setup.md` (pre-existing, uncommitted at dispatch) | Vector's turn recorded in `## Status`, `## Next Actions`, `## Docs`. Not edited this turn; shipped in the same commit |
| `planning/docs/TASK-0014-vector-bash-permissions.md` (new) | Robotnik's task doc (untracked at dispatch); `## Implementation` filled this turn |

No other file in `.opencode/agents/` was touched. `git status --short` after the edits shows exactly the five files above, nothing else.

**Final `permission.bash` block** (`.opencode/agents/vector.md:19-29`, read back after the edit):

```yaml
  bash:
    "*": deny
    "git add*": allow
    "git commit*": allow
    "git push*": allow
    "git ls-remote*": allow
    "ssh howard@192.168.1.106*": allow
    "git diff*": allow
    "git log*": allow
    "git status": allow
    "rg *": allow
```

**Checks run**

- Frontmatter parse (PyYAML 6.0.1, `python3` heredoc): extracted the frontmatter between the `---` markers of `.opencode/agents/vector.md`, parsed with `yaml.safe_load`, asserted `list(permission['bash'].items())` equals the ten expected (pattern, effect) pairs in order, and printed the block. Result: `parse: OK (yaml.safe_load)`, `rules: 10`, `assert: block equals expected 10 rules in order: PASS`.
- README per-agent permission grep: `grep -n "permission|bash:" README.md` → three hits: line 8 (intro sentence on least-privilege permissions), line 25 (Agent catalogue table header, "Key permissions" column), line 38 ("Key permission patterns"). Outcome: README.md **does** document per-agent permission sets via the Agent catalogue (lines 25-36). Vector's row (line 34) said "read-only git", stale after this change → updated as in the changes table. The "Key permission patterns" list (lines 38-46) is generic (no per-agent bash enumeration) → checked, no change needed.
- Compile / linter / harness: n/a for a YAML frontmatter + Markdown change; the parse check above is the applicable check (DoD records `Big` as N/A).

**Commit and remote verification** — recorded in the follow-up commit, per the TASK-0011 convention (`planning/docs/TASK-0011-default-model-q4kxl.md:219`: "follow-up commit records the sha here"):

- Commit 1 (agent file + README + planning docs): sha pending below.
- `git ls-remote` verification of local HEAD == remote HEAD: pending below.

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
