# TASK-0032 — operator-directed text corrections (2026-10-02)

> **Section order below is fixed.** Each agent writes to its own section and no other. `Robotnik`
> reads only `## Status` and `## Next Actions`. Do not reorder, rename, or remove sections.

- **Created:** 2026-10-02

---

## Status

*Owner: `Robotnik`. Keep this SHORT and CURRENT — it is one of only two sections the PM reads, so a
stale entry means the whole loop runs on bad information.*

**Now:** Complete (2026-10-03). Both corrections are in the site repo's
woodwork draft `_pages/module-pc-shelf-build.md` (`~/Linux/projects/github_pages`, untracked,
under operator review): (1) "simply" removed from "that simply stacks"; (2) "I'm actually proud
of" is now "I went off the rails on" inside the dash-framed clause. Local edits only, no commit,
no push, per the create-article skill rule. AGENTS.md is back to its committed state.

**Interpretation on record (PM):** "Remove this: 'simply'" was first read as a change to the
AGENTS.md section 10 banned list and applied; on locating the proud-of phrase in the woodwork
draft, that reading was superseded — the operator was proofreading the draft against their own
banned list (the draft contained "simply"), and the proud-of correction came from the same
reading session. The AGENTS.md line is reverted to its committed state; the draft's "simply" is
removed instead. The proud-of replacement string ("and this is the part I went off the rails on")
overlaps the clause's existing lead-in; applied as the swap "I'm actually proud of" to
"I went off the rails on" inside the existing dash-framed clause — the only reading that keeps
the sentence grammatical.

**Environment / scope:**
- Files in scope: `AGENTS.md` (this repo) and
  `/home/howard/Linux/projects/github_pages/_pages/module-pc-shelf-build.md` (site repo).
- Touches the DB schema: no
- Graphical UI: no
- Rocky Linux target: no (text-only)

**Deviation on record:** review chain skipped (two one-line text edits, no code surface; same
rationale as TASK-0030 and TASK-0031). PM verifies both edits against the scoped diffs.

**2026-10-03 (PM, verified, task closed):**
- Article line 15 verified on disk: "that stacks" (no "simply") and "and — this is the part I went
  off the rails on — the whole stack is held together with bolts and nuts".
- AGENTS.md verified: scoped diff empty, line 243 back to the committed banned list.
- Site repo: no commit, no push (draft remains untracked under operator review).
- All DoD boxes satisfied; TASKS.md row Done.

---

## Definition of Done

*Owner: `Robotnik`, and nobody else. Written **before** any work starts. Objectively checkable —
if a box cannot be verified by looking at something, rewrite it.*

- [ ] AGENTS.md: unchanged from its committed state (the interim "simply" removal is reverted;
  scoped diff is empty).
- [ ] `_pages/module-pc-shelf-build.md` line 15: "that simply stacks" is now "that stacks", and
  the clause reads "and — this is the part I went off the rails on — the whole stack is held
  together with bolts and nuts"; no other file change.
- [ ] No commit and no push of the site repo (draft under operator review; create-article skill
  rule: push only on explicit request).
- [ ] No commit needed: AGENTS.md is reverted to its committed state and the site draft stays
  untracked (create-article skill rule: push only on explicit request).
- [ ] PM verifies both edits (scoped git diff of AGENTS.md; read of the changed article line).
- [ ] TASKS.md row to Done.

---

## Next Actions

*Owner: whoever wrote last. The future only — delete what has been done. The second of the two
sections the PM reads.*

- [ ] PM: verify (article line 15; AGENTS.md scoped diff empty), then close (row to Done).

---

## Plan

*Owner: `Amy`.*

Not planned by Amy: operator-directed text corrections with a PM-written Definition of Done; the
plan content is the two operator instructions plus the interpretation note in Status.

---

## Implementation

*Owner: `Tails`.*

Done (2026-10-02). Both edits applied as one-line changes, re-read from disk before editing.

1. `AGENTS.md` (this repo), section 10, line 243: `- No "simply", "just", "obviously", "easy". ...` is now `- No "just", "obviously", "easy". No "leverage", "utilize", "ensure", "robust",` (continuation line `"seamless".` untouched). `git diff --stat AGENTS.md` reports `1 file changed, 1 insertion(+), 1 deletion(-)`; diff shows only the one line.
2. `/home/howard/Linux/projects/github_pages/_pages/module-pc-shelf-build.md` line 15: "I'm actually proud of" became "I went off the rails on"; the clause now reads "and — this is the part I went off the rails on — the whole stack is held together with bolts and nuts". Verified with `sed -n '15p'`. File is untracked (`git status --short` shows `??`), so no commit and no push was made; local edit only, per the Definition of Done.

No apostrophe/dash byte check was needed: both `edit` matches succeeded on first attempt against the text as read from disk. No other file touched in either repo.

---

## Review

*Owner: `Shadow`. Read-only — findings only, no edits. Severity order, blockers first.*

Skipped on record (see Status deviation); no code to review.

---

## Security

*Owner: `Omega`. Read-only. Severity order.*

Skipped on record (see Status deviation); no new attack surface.

---

## License (Charmy)

*Owner: `Charmy`. Fourth in the review chain. Every license is verified at the upstream source
repository and the ref used, never from a copy in this repo.*

Skipped on record (see Status deviation); no code added.

---

## Test Results

*Owner: `Big`. Verdicts, never raw log dumps.*

PM verifies the edits (see Status deviation); no harness applies to two text-line changes.

---

## Docs

*Owner: `Vector`.*

The article change is the doc change; it stays an untracked draft under operator review.

---

## Release

*Owner: `Knuckles`.*

N/A — AGENTS.md is back to its committed state; the site draft stays untracked under operator
review.

---

## Archive

*Owner: `Espio`, the only agent that deletes. Superseded detail lands here rather than being
lost. Decisions, verified facts, rejected options with their reasons, known traps, and anything the
user said are never deleted.*
