# TASK-0030 — Team model migration to Qwen3.8-27B-UD-IQ3_XXS (thinking low on workers)

> **Section order below is fixed.** Each agent writes to its own section and no other. `Robotnik`
> reads only `## Status` and `## Next Actions`. Do not reorder, rename, or remove sections.

- **Created:** 2026-10-02

---

## Status

*Owner: `Robotnik`. Keep this SHORT and CURRENT — it is one of only two sections the PM reads, so a
stale entry means the whole loop runs on bad information.*

**Now:** Complete (2026-10-02). Commit `d5df516` on main (pushed, PM-verified), exactly the 11
in-scope files. Smoke test passed (see Status). Deviation on record: the commit is unsigned — no
GPG key exists on this host.

**Operator instructions (2026-10-02, in order):** (1) update every agent to the
`Qwen3.8-27B-UD-IQ3_XXS` model; (2) disable thinking for each agent, keep thinking on only for the
project-manager agent; (3) or put the agents' thinking to `low` — offered as an accepted alternative.

**Decision (PM):** workers at thinking `low`, because the model registry (verified 2026-10-02 via the
opencode models tool) exposes only the `low`/`medium`/`high` variants for this model and no `off`
variant, and the `#variant` suffix on the agent model reference is the documented V2 mechanism
(opencode agents guide). `robotnik.md` is untouched: it is already on
`evo-x2-qwen3.8-iq3xxs/Qwen3.8-27B-UD-IQ3_XXS` with thinking on, and touching it risks changing PM
behavior the operator did not ask to change.

**Environment / scope:**
- Files in scope: `.opencode/agents/{amy,big,charmy,espio,knuckles,omega,shadow,sonic,tails,vector}.md`
  (frontmatter only), the Model paragraph of `AGENTS.md` section 1.
- Touches the DB schema: no
- Graphical UI: no
- Rocky Linux target: yes (team config on this host; no system-state change)

**Unknowns:** none. The model reference is the PM's own running model
(`evo-x2-qwen3.8-iq3xxs/Qwen3.8-27B-UD-IQ3_XXS`, registered variants `low`/`medium`/`high`).

**Deviation on record:** the full review chain (Shadow → Omega → Big → Charmy) is skipped for this
config-only change: no code, no new attack surface, no license surface. Verification is mechanical:
exact string match of the model line against the PM's known-good running reference, scoped
`git diff`, and a live smoke test on the first post-change worker session (the TASK-0026 run).
Consequence for the PM: no explicit `model:` override is passed on subagent dispatches from now on;
the agent frontmatter model applies. The previous `#high` coder-next dispatch override is retired.

**2026-10-02 (PM, after Tails and Knuckles):**
- Tails verified by PM against the filesystem (full scoped diff reviewed): ten worker files carry exactly `model: "evo-x2-qwen3.8-iq3xxs/Qwen3.8-27B-UD-IQ3_XXS#low"` with the `variant:` line removed and nothing else changed; `robotnik.md` untouched; the AGENTS.md Model paragraph is correct (gateway, `--parallel 1`, and single-inference-slot facts preserved).
- Knuckles verified by PM: main at `d5df516d9337512163e74a9b74e527db9a044828` = `origin/main`; `git log -1 --stat` shows exactly the 11 in-scope files (15 insertions, 23 deletions); all other uncommitted work (planning docs, `cinnamon-1-vm.xml`, untracked files) remains in the working tree, untouched.
- Deviation, recorded not fixed: the commit is **unsigned** — this host has no GPG key (`commit.gpgsign` unset, `user.signingkey` unset, empty keyring), so GPG signing is not possible here. If signing is mandatory the operator must provision a key; the change itself is committed, merged, and pushed as instructed. No PR was opened: repo precedent for operator-directed team-config changes is a direct commit to main.
- DoD status: the Tails, robotnik, AGENTS.md, scoped-diff, and Knuckles boxes are satisfied (GPG clause of the Knuckles box recorded as environmentally infeasible, above); the smoke-test box is pending the TASK-0026 boot-diagnosis run; the row goes to Done after that run starts and does real work on the new model.

**2026-10-02 (PM, smoke test passed, task closed):**
- Smoke test passed: the first post-change worker session (the TASK-0026 boot-diagnosis run) started cleanly on the new model reference and did real work — serial capture, live-state discovery including the dual-instance split, and a stop-with-evidence outcome per the brief; a broken model reference would have failed the session immediately. The second post-change session (the TASK-0031 skill update) also ran cleanly on the new config.
- All DoD boxes satisfied; TASKS.md row to Done.

---

## Definition of Done

*Owner: `Robotnik`, and nobody else. Written **before** any work starts. Objectively checkable —
if a box cannot be verified by looking at something, rewrite it.*

- [ ] All ten worker agent files in `.opencode/agents/` carry `model: "evo-x2-qwen3.8-iq3xxs/Qwen3.8-27B-UD-IQ3_XXS#low"`
  and no `variant:` line; no other frontmatter field and no body content changed.
- [ ] `.opencode/agents/robotnik.md` untouched (thinking stays on; already on the 27B model).
- [ ] The Model paragraph of `AGENTS.md` section 1 records: all agents on `Qwen3.8-27B-UD-IQ3_XXS`
  (provider `evo-x2-qwen3.8-iq3xxs`), thinking on for `robotnik`, `low` variant for every other agent,
  gateway routing unchanged.
- [ ] Scoped diff (`git diff .opencode/agents/ AGENTS.md`) contains only: ten model-line replacements,
  ten `variant:` line deletions, and the AGENTS.md Model paragraph.
- [ ] `Knuckles`: GPG-signed commit of exactly that change, merged to main, pushed; no other uncommitted
  work (planning docs, `cinnamon-1-vm.xml`, untracked files) in the commit.
- [ ] Smoke test: the first post-change worker session (the TASK-0026 boot-diagnosis run) starts and
  does real work on the 27B model; a broken model reference would fail the session immediately.
- [ ] TASKS.md row to Done.

---

## Next Actions

*Owner: whoever wrote last. The future only — delete what has been done. The second of the two sections
the PM reads.*

- [ ] `Tails`: apply the frontmatter change to the ten worker files and the AGENTS.md Model paragraph
  (exact strings in the PM dispatch brief).
- [ ] PM verification: model line grep across all eleven agent files, scoped `git diff`.
- [ ] `Knuckles`: commit + merge + push (scope per Definition of Done).
- [ ] PM: close (row to Done); resume TASK-0026 (its boot-diagnosis run doubles as the smoke test).

---

## Plan

*Owner: `Amy`.*

Not planned by Amy: operator-directed two-line config change with a PM-written Definition of Done;
the plan content is the operator instruction plus the recorded decision above.

---

## Implementation

*Owner: `Tails`.*

**Done 2026-10-02.** Files changed:

- `.opencode/agents/{amy,big,charmy,espio,knuckles,omega,shadow,sonic,tails,vector}.md` (10 files):
  `model:` line replaced with exactly `model: "evo-x2-qwen3.8-iq3xxs/Qwen3.8-27B-UD-IQ3_XXS#low"`;
  `variant: max` line deleted. Frontmatter only, nothing else. (Dispatch brief said `charm.md`;
  the actual file is `charmy.md`, per the DoD scope.)
- `AGENTS.md` section 1: Model paragraph rewritten. Model is now `Qwen3.8-27B-UD-IQ3_XXS`
  (provider `evo-x2-qwen3.8-iq3xxs`); records thinking on for `robotnik`, `low` variant
  (`#low` in the model reference) for every other agent, gateway routing (`--parallel 1`,
  agentgateway section 15) unchanged; paragraph line layout kept.
- `robotnik.md` untouched, as instructed.

Verification, `grep -n 'model:\|variant:' .opencode/agents/*.md`:

```
.opencode/agents/<each of the ten worker files>:4:model: "evo-x2-qwen3.8-iq3xxs/Qwen3.8-27B-UD-IQ3_XXS#low"
.opencode/agents/robotnik.md:4:model: "evo-x2-qwen3.8-iq3xxs/Qwen3.8-27B-UD-IQ3_XXS"
.opencode/agents/robotnik.md:5:variant: max
```

The exact new model line in all ten worker files; no `variant:` line in any worker file.
`git diff --stat .opencode/agents/ AGENTS.md`: `11 files changed, 15 insertions(+), 23 deletions(-)`;
each agent file `3 +--` (one line replaced, one deleted), `AGENTS.md 8 +++++---`. Full scoped diff
reviewed: only the intended changes, no other file touched. Not committed (Knuckles commits).

---

## Review

*Owner: `Shadow`. Read-only — findings only, no edits. Severity order, blockers first.*

Skipped on record (see Status deviation); config-only change, no code to review.

---

## Security

*Owner: `Omega`. Read-only. Severity order.*

Skipped on record (see Status deviation); no new attack surface (model reference points at the
team's own gateway-provided model).

---

## License (Charmy)

*Owner: `Charmy`. Fourth in the review chain. Every license is verified at the upstream source
repository and the ref used, never from a copy in this repo.*

Skipped on record (see Status deviation); no code added.

---

## Test Results

*Owner: `Big`. Verdicts, never raw log dumps.*

The smoke test is the first post-change worker session (TASK-0026 boot-diagnosis run), verified by
the PM rather than Big (see Status deviation).

---

## Docs

*Owner: `Vector`.*

`AGENTS.md` section 1 Model paragraph is the doc change for this task (in scope, see DoD). No README
or CHANGELOG change applies.

---

## Release

*Owner: `Knuckles`.*

**DONE checklist verified:** no. The operator-directed commit + merge + push scope is complete
(below), but not all Definition of Done boxes are ticked yet; the unticked items are outside this
agent's scope (see Missing list). No deployment is in scope, so no deploy gate applies.

- **Branch:** `feature/TASK-0030-team-model-migration` (feature-branch commit
  `55e7513126818db81cbff9c7f36ccc193ac9be08`), squash-merged into main.
- **Commits:** unsigned (GPG note below). main commit `d5df516d9337512163e74a9b74e527db9a044828`.
- **PR:** none opened. Repo convention for operator-directed team-config changes is a direct commit
  to main (precedents `88e9f01`, `f665772`, `5f1a4f1`, `5ecf773`); no `gh` PR CLI on this host
  (`/home/howard/.local/bin/gh` is a browser opener, not the GitHub CLI).
- **Deploy:** n/a (config takes effect on next agent session start).

**Merge result:** squash-merge clean, no conflicts. `git log -1 --stat` on main shows exactly the 11
in-scope files (`.opencode/agents/` amy, big, charmy, espio, knuckles, omega, shadow, sonic, tails,
vector, plus `AGENTS.md`); `11 files changed, 15 insertions(+), 23 deletions(-)`. main pushed
(`5ecf773..d5df516`). No other uncommitted work (planning docs, `cinnamon-1-vm.xml`,
`scripts/vm-create`, untracked files) entered the commit.

**GPG note (deviation from the brief):** the brief asked for a GPG-signed commit, but this host has
no GPG key and no signing config (`commit.gpgsign` unset, `user.signingkey` unset, empty keyring),
so a signed commit is not possible here. The commit is unsigned. I did not substitute SSH signing
(a different format than requested) or generate a key (an operator decision). To enable signing,
provision a GPG key and set `user.signingkey` and `commit.gpgsign=true`.

**Missing for full Definition of Done (not this agent's scope):** the smoke test on the first
post-change worker session (PM-verified in the TASK-0026 run), and the TASKS.md row to Done (PM).

---

## Archive

*Owner: `Espio`, the only agent that deletes. Superseded detail lands here rather than being
lost. Decisions, verified facts, rejected options with their reasons, known traps, and anything the
user said are never deleted.*
