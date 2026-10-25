# TASK-0039 — Update team agents to catch GPG, icon, and feature-parity issues

> **Section order below is fixed.** Each agent writes to its own section and no other. `Robotnik`
> reads only `## Status` and `## Next Actions`. Do not reorder, rename, or remove sections.

- **Created:** 2026-10-25

---

## Status

*Owner: `Robotnik`. Keep this SHORT and CURRENT — it is one of only two sections the PM reads.*

**Now (2026-10-25):** Operator request: update the team-chaotix agents so they are "updated
appropriately to catch" the issue classes the operator hit on the Cinnamon-for-Rocky10 project
(TASK-0038), then commit and merge the change. The three issue classes, with the concrete failure
modes from TASK-0038 that the agents must catch:
1. **GPG signing.** Consumer `gpgcheck=1` install of the published RPM set fails because some RPMs
   are signed under a key that does not match the key the docs ship/import; the recorded
   fingerprint is stale. (TASK-0038: 64 of 67 RPMs signed under an old key, docs shipped/imported
   only the new key, recorded the old fingerprint.)
2. **Icon parity.** The target desktop's icons do not match the reference/baseline desktop
   (Fedora Cinnamon); differences exist and are uncaught.
3. **Feature parity.** Features present in the reference desktop (Fedora Cinnamon) are missing
   from the target RPMs (Rocky 10 Cinnamon); the gap is uncaught.

This is a change to the **team repo** (`metalllinux/team-chaotix`): `.opencode/agents/*.md` and,
where the check is a test layer, the test strategy in `AGENTS.md` section 7. It is not a change to
the Cinnamon project repo. TASK-0038 remains In Progress (paused while this runs; single inference
slot, so the two tasks do not run at once).

**Environment / scope:**
- Files in scope: `.opencode/agents/*.md` (primarily `big` and `shadow`; any other agent the plan
  names), `AGENTS.md` (section 7 test strategy).
- Touches the DB schema: no
- Graphical UI: no (markdown/config change; no Sparky)
- Rocky Linux target: no

**Unknowns:**
- Which agent(s) own "catching" each issue class (Big vs Shadow vs others) — for `Amy` to decide
  and `Tails` to implement.
- The exact concrete check steps to add. They must reference the specific TASK-0038 failure modes
  so the agent instructions are actionable, not vague awareness.

---

## Definition of Done

*Owner: `Robotnik`, and nobody else. Written **before** any work starts. Objectively checkable —
if a box cannot be verified by looking at something, rewrite it.*

- [ ] The agent definitions in `.opencode/agents/` are updated so the team's agents carry explicit,
  actionable responsibility to catch each issue class, with concrete check steps (commands or
  observations), not vague awareness:
  - **(a) GPG signing:** on a fresh consumer, `gpgcheck=1` installs the full published RPM set with
    dnf verifying every signature; every published RPM verifies against the documented key; the
    recorded fingerprint equals the fingerprint of the key that actually signed the RPMs. The
    instruction must name the failure mode it guards against (RPMs signed under a key that does not
    match the shipped/imported key, so `gpgcheck=1` fails).
  - **(b) Icon parity:** the target desktop's icons are compared against the reference/baseline
    desktop (e.g. Fedora Cinnamon) and every difference is either fixed or documented as an
    accepted difference with evidence.
  - **(c) Feature parity:** features present in the reference desktop (Fedora Cinnamon) are
    enumerated and compared against the target RPMs (Rocky 10 Cinnamon); missing features are
    either added or documented as out of scope with a reason.
- [ ] The responsible agent(s) are named in the change and their definitions carry the check steps.
  At minimum `big` (test layers) and `shadow` (completeness); the plan may name more.
- [ ] Where a check is a test layer, the test strategy (`AGENTS.md` section 7 and/or `big`'s
  definition) includes it as a standard layer for Cinnamon/desktop RPM projects.
- [ ] The change respects the team's own rules: agent roster unchanged, no new turn caps,
  least-privilege permissions preserved; `tests/config_gate.py` passes.
- [ ] `tests/selftest.sh` passes end-to-end (no model invoked).
- [ ] `Shadow`: no unresolved blockers or should-fix findings in `## Review`.
- [ ] `Omega`: no unresolved findings above `low` in `## Security`.
- [ ] `Big`: selftest passes with no silently dropped checks.
- [ ] `Charmy`: no unresolved findings in `## License (Charmy)`.
- [ ] `Flicky`: gate outcome `PASS` (markdown/config change; no new imports expected).
- [ ] `Vector`: documentation updated as affected (`AGENTS.md` / `README.md` if changed).
- [ ] `Knuckles`: committed (GPG-signed), pushed, PR opened and merged to `main` on
  `metalllinux/team-chaotix` (within-account, autonomous per AGENTS.md section 8), PR closed.

---

## Next Actions

*Owner: whoever wrote last. The future only — delete what has been done.*

- [ ] `Amy`: write `## Plan` — decide which agent(s) own catching each issue class, the concrete
  check steps to add (referencing the TASK-0038 failure modes in `## Status`), the work breakdown,
  and validation (`tests/selftest.sh` + `tests/config_gate.py`). Read `## Status` and `##
  Definition of Done` first.

---

## Plan

*Owner: `Amy`.*

**Why this task exists** — TASK-0038 (Cinnamon-for-Rocky10) shipped a broken consumer story
and the team's agents caught none of it: (1) a consumer `gpgcheck=1` install of the published
RPM set fails because 64 of 67 RPMs are signed under an old key while the docs ship/import
only the new key and record the old fingerprint; (2) the target desktop's icons do not match
the reference Fedora Cinnamon desktop; (3) features present on the reference desktop are
missing from the target RPMs. This task turns catching those three classes into explicit,
actionable agent responsibility in the team repo, so the next port's review chain catches them.

**What it unblocks / what blocks it** — Unblocks TASK-0038 resuming (it is paused; single
inference slot, so the two tasks do not run at once). The new layers take effect on the next
TASK-0038 run, not retroactively. Nothing in this repo blocks it: the failure modes are
already recorded in this doc's `## Status`. Outside this repo: the Cinnamon project repo is
not touched; the GPG check's fresh consumer VM is provisioned during TASK-0038 execution, not
here.

**MVP** — three check steps in `big.md` (GPG, icon, feature parity), one completeness item in
`shadow.md`, and the same three layers in `AGENTS.md` section 7. Deferred, with reason:
parity-diff automation scripts (they belong in the Cinnamon project repo, TASK-0038's
concern); a new CI workflow in this repo (this repo's CI is the team's own selftest, it does
not test Cinnamon); new Sparky tasks (no graphical change in this task).

**What this makes harder later** — `big.md` mirrors `AGENTS.md` section 7, so a future
test-strategy change must edit both (drift risk; named so the next agent knows). Agent
definitions grow, adding per-turn context cost to every agent (bounded; 190k context).
`shadow.md`'s heading retitles from "five things" to "six things"; verified nothing else
references the old heading (grep at planning time: only `shadow.md:39` itself).

**Ownership decision.** All three classes, check execution: `big` (test layers, runs the
checks in the environment, records pass/fail). All three classes, completeness review:
`shadow` (does the change contain everything it claims; does every parity difference have a
documented disposition). No other agent is named. Justification: GPG *verification* is a
test in an environment, not a security finding in this repo (an `omega` vector would be a
real key leak in the Cinnamon project, out of scope here); icon and feature parity are
completeness issues, not license, docs, or release issues. Naming more owners would split
accountability across the same three checks.

**Constraints (non-negotiable, from DoD).** Roster unchanged (12 agents, enforced by
`tests/config_gate.py:20-23`); no turn caps (`tests/selftest.sh:71` greps `maxTurns|
max_turns` across `.opencode/agents` among others); least-privilege permissions preserved
(frontmatter of both files is untouched; all edits are body text).

**Concrete check steps.** The text Tails implements; each layer names the TASK-0038 failure
mode it guards against. Commands below were verified on this host (Rocky 10.2, dnf 4.20.0,
GnuPG 2.4.5) on 2026-10-25.

`.opencode/agents/big.md` — new section `## Cinnamon / desktop RPM projects`, inserted after
`## Testing strategy by project type` (`big.md:68`):

1. **GPG signature verification on a fresh consumer** — guards TASK-0038: 64 of 67 published
   RPMs signed under an old key; the docs ship/import only the new key; the recorded
   fingerprint is stale, so a `gpgcheck=1` install of the full set fails.
   - Provision a fresh Rocky 10 consumer (`scripts/vm-create <name>` from the golden image);
     import the documented signing key exactly as the project docs instruct (the consumer's
     path, not the build machine's); with `gpgcheck=1`, install the full published RPM set.
     Pass: dnf verifies every signature and the complete set installs.
   - For every published RPM: `rpm -K <file>.rpm` must report digests/signatures OK.
   - For every published RPM: `rpm -qp --qf '%{SIGPGP:pgpsig}\n' <file>.rpm` prints the
     signing key ID (`(none)` means unsigned, which is a failure for a published set);
     compare each key ID against the documented key's fingerprint via
     `gpg --show-keys --with-fingerprint <key>`.
   - The fingerprint recorded in the project docs must equal the fingerprint of the key
     that actually signed the RPMs.
   - Assumption (marked): the consumer VM's dnf may differ from the host's dnf 4.20.0, so
     the exact `gpgcheck=1` configuration location is verified on the consumer during
     TASK-0038. The per-RPM `rpm -K` plus key-fingerprint check is dnf-independent and
     catches the failure mode regardless.
2. **Icon parity against the reference desktop** — guards TASK-0038: target desktop icons do
   not match the reference Fedora Cinnamon desktop; differences went uncaught.
   - Capture reference baseline screenshots (Fedora Cinnamon: panel, menus, applets, file
     manager) and the same screens on the target (Rocky 10 Cinnamon).
   - Read both sets with `read` and enumerate every icon difference. Per `AGENTS.md`
     section 7, the visual read is the primary evidence; a `diff -rq` of the installed
     icon-theme directories is auxiliary text evidence alongside it.
   - Every difference is fixed or documented as an accepted difference with evidence.
     Pass: zero undischarged icon differences.
3. **Feature parity against the reference desktop** — guards TASK-0038: features present on
   the reference desktop are missing from the target RPMs; the gap went uncaught.
   - Enumerate the features present on the reference desktop: `dnf list installed`,
     Cinnamon components, panels, applets, sessions.
   - Enumerate the same on the target and compare. Every feature present on the reference
     must be present on the target or documented out of scope with a reason. Pass: no
     missing feature without a documented disposition.

`.opencode/agents/shadow.md` — add a sixth item under `## The five things you check`
(`shadow.md:39`) and retitle that heading to `## The six things you check`:

6. **Completeness — does the change contain everything it claims?**
   - For RPM/port changes, the published artifact set matches the documented set: every
     documented package is present, and nothing undocumented is added.
   - The fingerprint recorded in the docs equals the fingerprint of the key that actually
     signed the artifacts (failure mode: TASK-0038 — 64 of 67 RPMs signed under an old key,
     recorded fingerprint stale).
   - Every icon/feature difference against the reference desktop has a documented
     disposition: fixed, or accepted/out-of-scope with evidence.
   - A silently dropped feature is a finding: a feature present on the reference and missing
     from the target must be added or documented out of scope.

`AGENTS.md` section 7 — insert one bullet group between the "All Rocky Linux projects"
bullet (`AGENTS.md:208`) and the "Unit and integration tests" bullet (`AGENTS.md:209`):

- **Cinnamon / desktop RPM projects:** GPG signature verification on a fresh consumer
  (`gpgcheck=1` install of the full published set; per-RPM `rpm -K`; the signing key's
  fingerprint matches the documented key and the recorded fingerprint); icon parity against
  the reference desktop (every difference fixed or documented); feature parity against the
  reference desktop (missing features added or documented out of scope).
- The edit must not touch the section 3 review-chain string or `## License Audit (Flicky)`;
  `tests/config_gate.py:90-95` asserts both.

**Work breakdown** — items 1-4 are one Tails turn each, one section-sized edit each
(`AGENTS.md` section 14).

| # | Item | Owner agent | Acceptance criterion | Parallel with |
|---|---|---|---|---|
| 1 | Edit `.opencode/agents/big.md`: add the `## Cinnamon / desktop RPM projects` section with the three check steps above; frontmatter untouched | `Tails` | all three layers present with the concrete commands above; frontmatter byte-identical | independent of 2, 3 |
| 2 | Edit `.opencode/agents/shadow.md`: retitle "five things" to "six things", add item 6 above; frontmatter untouched | `Tails` | the completeness item is present and names the TASK-0038 failure mode; frontmatter byte-identical | independent of 1, 3 |
| 3 | Edit `AGENTS.md` section 7: add the Cinnamon/desktop RPM project layer; grep for `The five things you check` first (planning-time grep: zero references outside `shadow.md:39`) | `Tails` | the layer is present between `AGENTS.md:208` and `:209`; the section 3 chain string and `## License Audit (Flicky)` are untouched | independent of 1, 2 |
| 4 | Run `bash tests/selftest.sh` | `Tails` | exit 0 with a printed check count; `python3 tests/config_gate.py` exit 0 | after 1, 2, 3 |
| 5 | Review chain: `Shadow` → `Omega` → `Big` → `Charmy` → `Flicky` | each named agent | no unresolved blocker/should-fix in `## Review`; no `## Security` finding above low; selftest re-verified in `## Test Results` | sequential (single inference slot) |
| 6 | `## Docs`: record changed files | `Vector` | `AGENTS.md` row filled; `README.md` listed under "checked and needed no change" | after 5 |
| 7 | Branch from `main` (head `8e7411b`), GPG-signed commit, push, open PR, merge, close | `Knuckles` | PR merged to `main`; the pre-push selftest gate passes | after 6 |

**Dependencies and sequence.** Items 1, 2, 3 touch different files with no shared state:
independent, order free. Item 4 depends on all three. Items 5-7 are the fixed
review/release cycle and run one at a time on the single inference slot. The only true
ordering is 1-3 → 4 → 5 → 6 → 7.

**Critical path:** 1 → 2 → 3 → 4 → 5 → 6 → 7 (everything runs sequentially on the single
slot; the longest chain is the whole plan).

**Estimates.** Three-point, `T = (O + 4M + P) / 6`, in minutes.

| Item | O | M | P | T |
|---|---|---|---|---|
| 1 big.md | 10 | 15 | 25 | 19 |
| 2 shadow.md | 10 | 15 | 25 | 19 |
| 3 AGENTS.md §7 | 10 | 15 | 25 | 19 |
| 4 selftest | 2 | 3 | 5 | 3 |
| 5 review chain (5 × 11) | | | | 55 |
| 6 docs | 5 | 10 | 15 | 10 |
| 7 release | 10 | 15 | 30 | 20 |
| **Total** | | | | **145** |

Buffer 25% (about 36 min) for review findings that send a Tails fix loop and the dnf-version
assumption. Planned total about 3 h.

**Risks.**
1. Check steps land vague instead of actionable (DoD requires commands or observations).
   Likelihood medium, impact high (the task fails its own DoD). Mitigation: the text above
   is the implementation source; Tails implements from the plan, not from memory.
   Contingency: `Shadow`'s review checks that every layer carries a concrete command or
   observation.
2. An edit regresses a gate (frontmatter damage, a stray `maxTurns` string, the section 3
   chain string disturbed). Likelihood low, impact high (blocks the merge). Mitigation:
   frontmatter is untouched by design; item 4 runs the selftest before release.
   Contingency: fix loop, re-run.
3. The dnf-version assumption is wrong (consumer VM dnf differs from the host's dnf
   4.20.0). Likelihood medium, impact low: the agent text is behavior-level
   (`gpgcheck=1`) and the per-RPM `rpm -K` plus fingerprint check is dnf-independent.
   Mitigation: assumption marked in the check steps. Contingency: TASK-0038 re-runs the
   consumer check with the correct configuration.
4. Roster, thinking level, or permissions drift. Likelihood low, impact high. Mitigation:
   `tests/config_gate.py` asserts all four (roster, `#low`, `task: deny`, `question: deny`)
   and item 4 runs it. Contingency: rollback below.

**Validation.**
- `bash tests/selftest.sh` exit 0 — it runs the syntax gates, the no-turn-caps grep,
  `tests/config_gate.py`, pytest, the licence gate on this repo, and the gateway selftest.
- `python3 tests/config_gate.py` exit 0 explicitly: roster 12 unchanged, workers on `#low`
  with `task: deny` and `question: deny`, the `AGENTS.md` review-chain string and
  `## License Audit (Flicky)` present, planning template OK, A2A roster file-driven.
- Files needing a human look (the operator): `.opencode/agents/big.md`,
  `.opencode/agents/shadow.md`, `AGENTS.md` (section 7 only) — the only three files that
  change — plus the merged PR diff.
- DoD mapping: box 1 = the three check steps above; box 2 = `big` and `shadow` named;
  box 3 = the section 7 layer; box 4 = config gate; box 5 = selftest.

**Rollback.**
- Detection: the pre-push hook runs the selftest and blocks the push on failure (immediate);
  review findings; post-merge, a CI selftest failure or an agent misbehaving.
- Exact revert: the change lands as one GPG-signed commit merged to `main`. Revert with
  `git revert <merge-commit-sha>` (the squash commit's sha if Knuckles squash-merges), then
  `git push`. The change is pure markdown: no migrations, no runner state, no workflow
  dispatch, no secrets.
- Point of no return: the merge pushed to GitHub (public repo). Before it: close the PR and
  the change is gone. After it: history keeps the change; the revert adds a commit and does
  not rewrite history (history rewriting is not attempted, per section 5).
- State left behind after a failed run that a retry must tolerate: none. The selftest is
  deterministic and idempotent; no VMs, containers, or secrets are touched by this task.
  A failed push leaves a local commit on a branch; retry from the same state.

---

## Implementation

*Owner: `Tails`.*

**Alternatives considered**

### Problem: where in `big.md` the three Cinnamon/desktop-RPM check steps live
**Option A — new top-level section `## Cinnamon / desktop RPM projects` after `## Testing strategy by project type`** · How: inserted between the "All Rocky Linux projects" group and `## Sparky testing`, with the plan's three numbered check steps verbatim. · Pros: matches the plan's prescribed heading and anchor (`big.md:68`); the three numbered steps with sub-bullets read as a standalone section. · Cons: one more top-level heading, longer file.
**Option B — fourth bold subgroup inside `## Testing strategy by project type`** · How: a `**Cinnamon / desktop RPM projects:**` group after the "All Rocky Linux projects" group. · Pros: consistent with the three existing subgroups. · Cons: deviates from the plan's prescribed text (the plan is the implementation source, its risk 1); the three-step numbered structure does not fit bullet-subgroup style.
**Chosen:** Option A, because the plan prescribes the section heading and text verbatim and the DoD maps box 1 to exactly those three check steps.

### Problem: how `shadow.md` carries the completeness responsibility
**Option A — sixth numbered item plus heading retitle** · How: add `### 6. Completeness` after item 5, retitle `## The five things you check` to `## The six things you check`, after a grep for old-heading references. · Pros: plan and DoD box 2 prescribe it; completeness (artifact set, recorded fingerprint, parity dispositions) is a distinct review question from item 5's per-change success criteria. · Cons: heading count changes; required the reference grep first (done, see Checks run).
**Option B — fold completeness into item 5 (Clear success criteria)** · How: extend item 5 with the artifact-set and parity bullets. · Pros: no heading change. · Cons: conflates two distinct questions; deviates from plan and DoD box 2.
**Chosen:** Option A, because the plan and DoD prescribe it and the grep showed no live reference to the old heading outside `shadow.md:39` itself.

### Problem: where in `AGENTS.md` section 7 the layer goes
**Option A — between the "All Rocky Linux projects" and "Unit and integration tests" bullets** · How: one bullet group, plan text verbatim, at `AGENTS.md:208`→`:209`. · Pros: plan-prescribed position; keeps the layer grouped with the project-type bullets; the section 3 chain string and `## License Audit (Flicky)` that `tests/config_gate.py:90-95` asserts are not touched. · Cons: none.
**Option B — after the "Unit and integration tests" bullet** · How: same text, different position. · Pros: none over A. · Cons: deviates from the plan; places a project-type layer after the generic test bullet.
**Chosen:** Option A, because the plan prescribes the exact position.

**Changes**

| File | What changed |
|---|---|
| `.opencode/agents/big.md` | Added `## Cinnamon / desktop RPM projects` with the three check steps (GPG signature verification on a fresh consumer; icon parity against the reference desktop; feature parity against the reference desktop), inserted after `## Testing strategy by project type` before `## Sparky testing`. Frontmatter untouched. Plan item 1; DoD boxes 1a–1c, 2, 3. |
| `.opencode/agents/shadow.md` | Retitled `## The five things you check` to `## The six things you check`; added item 6 `### 6. Completeness` (published artifact set matches docs; recorded fingerprint equals signing key's fingerprint, naming the TASK-0038 failure mode; every icon/feature difference has a documented disposition; silently dropped feature is a finding). Frontmatter untouched. Plan item 2; DoD box 2. |
| `AGENTS.md` | Section 7: inserted the `**Cinnamon / desktop RPM projects:**` layer bullet between the "All Rocky Linux projects" and "Unit and integration tests" bullets. Section 3 chain string and `## License Audit (Flicky)` untouched. Plan item 3; DoD box 3. |
| `planning/docs/TASK-0039-agent-gpg-icon-feature-catch.md` | Wrote `## Implementation` (this section). |

Note: `git diff --stat` also shows `planning/TASKS.md` (+2 lines, the TASK-0038 and TASK-0039 index rows). That change pre-existed this turn in the working tree (made when the task was created); it was not made by Tails and is listed so the release diff is accounted for.

**Checks run**

- `bash tests/selftest.sh` → exit 0, output ends `SELFTEST: 56 checks passed`. Internal gates: syntax OK, shellcheck absent (skipped), yaml OK, json OK, no turn caps OK, config gate OK, pytest OK (28 tests), licence-check OK, gateway selftest OK. Re-run with exit code captured directly (first run piped through `tail`, which masked the pipeline exit code; the re-run used `bash tests/selftest.sh > /tmp/opencode/selftest-t0039.log 2>&1; echo $?` → `SELFTEST_EXIT=0`).
- `python3 tests/config_gate.py` → exit 0: `roster OK (12 agents)`, `thinking levels and permissions OK`, `AGENTS.md chain and doc contract OK`, `planning template OK`, `A2A roster is file-driven OK`.
- `git diff --stat` → `.opencode/agents/big.md +37`, `.opencode/agents/shadow.md +13/-1`, `AGENTS.md +5`; the diff hunks contain no frontmatter lines in either agent file (frontmatter byte-identical, roster/thinking/permissions untouched).
- `grep 'The five things you check'` (pre-edit) → matches only `shadow.md:39` (the heading itself) plus the planning doc's own lines 182 and 214 (the plan naming the heading as the edit anchor). Zero references from any other agent file or code.
- Markdown/config change, so there is no compile or linter step beyond the selftest's syntax, YAML/JSON, and no-turn-caps gates, all of which passed above.

**Competing priorities**

- The plan's work breakdown frames items 1–4 as one Tails turn each; the dispatch brief assigned all four in this dispatch. Resolved by keeping the turn-size bound the plan targets: exactly one section-sized edit per file, both gates in one batch.
- No commit, push, or PR in this stage: items 5–7 are the review chain, `Vector`, and `Knuckles` on the single inference slot, in the fixed cycle order.
- No Sparky/VM work run here: the plan states no VMs, containers, or secrets are touched by this task; the check steps are executable text for TASK-0038's runs.
- `big.md` mirrors `AGENTS.md` section 7 by design (plan, "What this makes harder later"); the mirror text was kept consistent between the two files in this change.

Items 1–4 complete. Next (not this stage): item 5 review chain `Shadow` → `Omega` → `Big` → `Charmy` → `Flicky`.

**Fix pass (2026-10-25) — the three nits from `## Review`**

**Alternatives considered** — nit 1 offered two directions in `## Review`: append the qualifiers
to the §7 bullet, or leave §7 as the summary and note that `big.md` is authoritative for pass
criteria. Chosen: append the qualifiers, because it keeps the two files word-for-word in
agreement without adding a cross-file "see" pointer that the next reader has to follow; the
qualifiers are three words total.

**Changes**

| File | What changed | Why |
|---|---|---|
| `AGENTS.md` §7, `AGENTS.md:209-214` | The Cinnamon/desktop RPM bullet now reads "every difference fixed or documented **with evidence**" and "missing features added or documented out of scope **with a reason**". | Nit 1: the bullet dropped the evidence/reason qualifiers that the `big.md` pass criteria carry (`big.md:114`, `big.md:121`); §7 and `big.md` now agree. |
| `.opencode/agents/shadow.md` item 6, `shadow.md:85-87` | "For RPM/port changes, ... every documented package is present" is now "For changes that publish RPMs or other documented artifacts in a porting project, ... every documented artifact is present". | Nit 2: "RPM/port changes" reads as network port and did not clearly cover a documented artifact set that ships no RPM; the trigger now spells out its scope and the check covers non-RPM artifacts, so the artifact-set-vs-docs check cannot be skipped on a reading of the trigger. |
| `.opencode/agents/big.md` step 3, `big.md:116-126` | The enumeration source is now named as "the installed packages (`dnf list installed`) and the Cinnamon component classes (components, panels, applets, sessions)", the unit of comparison is stated as "the feature, not the package", the comparison is "at feature level", and "package-name churn is not a missing feature". | Nit 3: the old step compared a package set against a feature-level pass criterion, so package-name churn (a meta-package renamed upstream, same feature under a new name) could false-positive a missing feature; the comparison is now explicitly feature-level. |

**Checks run**

- `bash tests/selftest.sh > /tmp/opencode/selftest-t0039-fix.log 2>&1; echo $?` →
  `SELFTEST_EXIT=0`; the log ends `SELFTEST: 56 checks passed`, the same count as the first
  pass (no check added or dropped).
- `python3 tests/config_gate.py > /tmp/opencode/configgate-t0039-fix.log 2>&1; echo $?` →
  `CONFIGGATE_EXIT=0`; all five assertion lines OK: `roster OK (12 agents)`, `thinking
  levels and permissions OK`, `AGENTS.md chain and doc contract OK`, `planning template OK`,
  `A2A roster is file-driven OK`. The `AGENTS.md chain and doc contract OK` line is the gate's
  assertion on the section 3 review-chain string and `## License Audit (Flicky)`, so the §7
  bullet edit did not disturb them.
- Direct confirmation of the chain strings: `grep -n 'Shadow` → `Omega` → `Big` → `Charmy` →
  `Flicky'` AGENTS.md` → lines 118, 119, 482; `grep -n '## License Audit (Flicky)' AGENTS.md`
  → lines 77, 261. The §7 bullet at `AGENTS.md:209-214` contains no such string, and both
  greps confirm the asserted strings are intact after the edit.
- `git diff --stat` → `.opencode/agents/big.md +41`, `.opencode/agents/shadow.md +14/-1`,
  `AGENTS.md +6`, `planning/TASKS.md +2` (63 insertions, 1 deletion). The `+41/+14/-1/+6`
  counts against `HEAD` include the first-pass change (nothing is committed yet): relative
  to the first pass this fix adds 4 lines in `big.md` (step 3 rewrite), 1 in `shadow.md`
  (trigger bullet grew 2 → 3 lines), and 1 in `AGENTS.md` (bullet rewrap 5 → 6 lines). The
  `planning/TASKS.md +2` pre-existed from task creation and is not part of this fix.
- `git diff AGENTS.md .opencode/agents/big.md .opencode/agents/shadow.md` → the hunks are
  exactly the three changes above: the `big.md` hunk is the whole Cinnamon section with the
  rewritten step 3, the `shadow.md` hunk is the retitle plus item 6 with the rewritten
  trigger, the `AGENTS.md` hunk is the six-line §7 bullet with both qualifiers. No hunk
  touches either agent file's frontmatter, the section 3 chain string, or
  `## License Audit (Flicky)`.
- `git status --porcelain` → the only tracked modifications are the three files above plus
  `planning/TASKS.md`; the untracked TASK-0038 RPM artifacts and this planning doc remain
  untracked and unstaged (Flicky's observation in `## License Audit` holds).

---

## Review

*Owner: `Shadow`. Read-only — findings only, no edits. Severity order, blockers first.*

**Verdict (2026-10-25):** no blockers, no should-fix. All three issue classes carry
concrete, actionable check steps that name the TASK-0038 failure mode they guard
against; the five→six retitle is consistent; the `AGENTS.md` §7 bullet is at the
plan-prescribed position and matches what `big.md` instructs. Three nits, in file
order.

Verified during review: the plan's host claim is accurate (dnf 4.20.0, GnuPG 2.4.5
on this host); `scripts/vm-create` exists and is executable; `git diff` hunks are
`big.md:87 +37`, `shadow.md:39` (retitle) and `shadow.md:83 +12`, `AGENTS.md:206 +5`
— none in the frontmatter (lines 1-21 of either agent file), none near the section 3
chain string or `## License Audit (Flicky)`; grep for `The five things you check`
across the repo outside this doc returns zero matches. The GPG step's layering is
correct: a PGP signature packet is self-verifying, so `rpm -K` alone passes even an
old-key RPM, and the check's teeth are the `SIGPGP` key-ID plus fingerprint
comparison, which it includes.

### AGENTS.md §7 bullet drops the evidence/reason qualifiers `big.md` carries
**Severity:** nit
**Where:** `AGENTS.md:209-213` vs `.opencode/agents/big.md:114-122`
**Problem:** the bullet says icon differences are "fixed or documented" and missing
features "added or documented out of scope", but `big.md` requires the documentation
to carry "with evidence" / "with a reason".
**Failure scenario:** an agent or reader working from `AGENTS.md` §7 closes an
accepted icon difference documented without evidence as satisfied; `Big`'s pass
criterion in `big.md` (evidence required, zero undischarged differences) then fails
and forces a fix loop that §7 alone would not have predicted.
**Suggested direction:** append "with evidence" / "with a reason" to the two
parentheticals in the §7 bullet, or leave §7 as the summary and note that `big.md`
is authoritative for pass criteria.
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

### "RPM/port changes" scope trigger in shadow.md item 6 is ambiguous
**Severity:** nit
**Where:** `.opencode/agents/shadow.md:85`
**Problem:** "RPM/port changes" uses "port" as team jargon for a porting project; it
also reads as network port, and the trigger does not clearly cover a change that
publishes a documented artifact set without shipping RPMs.
**Failure scenario:** a Cinnamon project change publishes a documented config-file
set but no RPM; the reviewer reads "RPM/port changes" as not applicable and skips
the artifact-set check, so a documented-vs-published mismatch goes unreviewed.
**Suggested direction:** spell the trigger out, e.g. "changes that publish RPMs or
other documented artifacts in a porting project".
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

### Feature-parity step enumerates packages where the issue is features
**Severity:** nit
**Where:** `.opencode/agents/big.md:116-122`
**Problem:** step 3's enumeration source is `dnf list installed` plus component
classes, i.e. packages; packages and features are different sets, so the comparison
is package-set diffing against a feature-level pass criterion.
**Failure scenario:** the reference ships a feature via a meta-package renamed
upstream and the target ships the same feature under a different package name; the
package diff flags a false "missing feature" and forces a documented disposition for
a feature that is present, or a real gap is buried in package-name churn.
**Suggested direction:** word the enumeration as packages and component classes
being the enumeration source for features, so the comparison is explicitly
feature-level.
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

---

## Security

*Owner: `Omega`. Read-only. Severity order.*

**Verdict (2026-10-25):** clean. No findings on any of the four requested vectors. The change
is markdown instruction text only; it introduces no executable surface. Diff verified as
exactly the three files with plan-conforming hunks (`git diff HEAD --stat`: `big.md +37`,
`shadow.md +13/-1`, `AGENTS.md +5`), and both agent files' frontmatter is byte-identical to
`HEAD` (line 1-21 `diff` per file), so no permission, model, or roster change.

**Secrets handling — clean.** The GPG steps (`big.md:89-106`) use public key material only:
documented public-key import, `rpm -K`, `rpm -qp --qf '%{SIGPGP:pgpsig}\n'` (prints key IDs),
`gpg --show-keys --with-fingerprint` (prints fingerprints), fingerprint equality. There is no
passphrase reference anywhere in the three files (`grep -rin passphrase` over them: zero
matches), so no private-key material is ever in scope of the instructions; nothing can be
echoed, logged, or committed that is not already public. No instruction writes key material to
a repo file, doc, or log; the only value recorded is a fingerprint match (a public
identifier). The failure-mode text recorded in this doc's `## Status` carries no secret
values.

**Least privilege — clean.** The new text uses only tools the agents already hold: `bash` for
`scripts/vm-create`, `rpm`, `gpg`, `dnf list installed`, and `read` for screenshots. No new
permission, escalation, or tool is implied. `scripts/vm-create` is the team's own provisioning
path (AGENTS.md section 12) with the golden image SHA-256 pinned; VM provisioning is existing
operator-granted host configuration, not something this change adds. `shadow.md` item 6
adds review-side checks only, no tooling.

**Verification weakening — clean.** No silently-accepts-unverified path for the named failure
mode. Layering: the `gpgcheck=1` install of the full set fails if any RPM is signed under a
key other than the documented import key; per-RPM `rpm -K` runs against a keyring that does
not contain the project's old key (fresh consumer from the pinned golden image), so stale
signatures fail BAD; the per-RPM `SIGPGP` key-ID comparison against the documented key's
fingerprint catches key mismatch independently, and `(none)` is explicitly a failure; and the
recorded-fingerprint equality check closes the docs side. Under the marked dnf-version
assumption, the per-RPM layers are dnf-independent and still catch the failure mode (stated
in `big.md:103-106`). No skip, fallback, or `|| true` instruction exists, and a missing or
empty keyring fails closed (`rpm -K` reports BAD, not OK).

**Supply chain — clean.** No new fetch: no URL, `curl`, or `wget` anywhere in the added text;
no third-party or marketplace component. `scripts/vm-create` is host-local with the SHA-256
pinned golden image; the key import and the published RPM set are sourced by the project's
own docs (Cinnamon project repo, out of scope for this change); the reference baseline
screenshots are captured or operator-provided per AGENTS.md section 7, not fetched.

**No injection surface.** Nothing executed: no workflow or `run:` block change, no `${{ }}`
interpolation, and the `<key>`/`<file>.rpm` placeholders are instructional, not
interpolated. No hardcoded credentials (grep clean). No license signal: no imports, the
touched files are the team's own markdown, so nothing to hand to `## License (Charmy)`.

---

## License (Charmy)

*Owner: `Charmy`. Fourth in the review chain. Every license is verified at the upstream source
repository and the ref used, never from a copy in this repo.*

**Project license:** MIT (`LICENSE` at repo root, `Copyright (c) 2026 Howard`) — appropriate.
The project is the team's own platform (its own agent definitions, `team/` package, scripts,
workflows); it forks no upstream project, so there is no inherited copyleft to respect, and
MIT is consistent with what the project is and does.

**Imported code**

| Component | Source (repo @ ref) | License (verified at) | Obligations met | Status |
|---|---|---|---|---|
| none in this change | diff scope: `big.md +37`, `shadow.md +13/-1`, `AGENTS.md +5`, `planning/TASKS.md +2` (53 added, 1 deleted); `git diff HEAD --diff-filter=A` → no new files | n/a — nothing imported | n/a — no code, no URL (grep of the 53 added lines for `https?://` → 0 matches), no vendored file, no new dependency, no frontmatter change (Shadow/Omega verified byte-identical frontmatter) | pass |

**Verdict:** pass. There is nothing new to verify. The change is markdown instruction text in
three of the team's own files (`big.md`, `shadow.md`, `AGENTS.md` section 7) plus the
`planning/TASKS.md` index row, and it introduces no imported open-source code, no vendored
file, no new dependency, and no new URL or fetched content. The only added lines matching an
import-like signal are two prose mentions of GPG public-key import (`.opencode/agents/big.md`
check step 1), which are instructions to run existing host tools, not code imports.

---

## License Audit (Flicky)

*Owner: `Flicky`. Fifth in the review chain. Runs the machine gate; the gate is evidence, and
this section records it. Never grants or refuses an exception.*

**Gate:** `scripts/licence-check .` (run at repo root `/home/howard/AI/projects/team-chaotix`,
2026-10-25; `--json` for the machine report)

**Outcome:** PASS — exit code **0** (the exact code the gate printed: `EXIT_CODE=0`)

**Declarations**

| File / component | Declared | Verified at (upstream @ ref) |
|---|---|---|
| `LICENSE` (repo root) | MIT, `Copyright (c) 2026 Howard` (full MIT text, 21 lines) | no upstream: the project is the team's own platform, not a fork of any upstream project; nothing to fetch |
| `tests/test_licence.py` | gate finding `header`/MIT | see note below; effectively the repo's own MIT `LICENSE` |

Note on the `tests/test_licence.py` finding (gate vs judgement, stated per the gate-is-evidence
rule): the gate's `header` kind for this file is a scanner artifact, not a real header. The only
`SPDX-License-Identifier` strings in the file are inside Python string-literal test fixtures —
`tests/test_licence.py:53` (`SPDX_PY = """# SPDX-License-Identifier: MIT`) and
`tests/test_licence.py:110` (a `GPL-3.0-only` C comment fixture) — used to build throwaway
fixture repos under `tmp_path` (the file's own docstring, lines 1-5, says so). Lines 1-5 are a
plain docstring with no SPDX line. The file is the team's own test code, covered by the repo's
MIT `LICENSE`; there is no external licence declaration in it. The gate's MIT classification is
right for the file's effective licence either way, and it does not change the PASS outcome.

**Change scope (what the gate read against):** `git diff HEAD --stat` →
`.opencode/agents/big.md +37`, `.opencode/agents/shadow.md +13/-1`, `AGENTS.md +5`,
`planning/TASKS.md +2` — markdown/config only. Verified on the added lines:
`git diff HEAD | grep -E '^\+' | grep -cE 'https?://'` → 0 (no new URLs), and no added line
carries `SPDX`, `License`, or `Copyright`. No code, no vendored file, no new dependency, no
frontmatter change. No package metadata files exist in the tree (`pyproject.toml`, `setup.cfg`,
`package.json`, `Cargo.toml` all absent; `team/requirements.txt` is a pre-existing pip
requirements list — langgraph, langchain-core, langgraph-checkpoint-sqlite, PyYAML, pytest —
not touched by this change, not code vendored into the tree).

**Upstream verification:** nothing to verify upstream. No upstream project is forked, no import
is added, no dependency is added, and the added lines introduce no URL or fetched content, so
there is no ref to `webfetch`. The only declared licence in scope (repo MIT) is the team's own
declaration.

**Exceptions recorded:** none.

**Observation for `Knuckles`:** the working-tree root carries untracked TASK-0038 RPM
artifacts (`cinnamon-*.rpm`, `muffin-*.rpm`, `gtk-layer-shell-*.rpm`, etc., visible in
`git status --porcelain`). They are untracked, not part of this change's diff, and the gate
read no licence metadata from them. They must not be staged into the release commit.

**Verdict:** pass

VERDICT: PASS

---

## Test Results

*Owner: `Big`. Verdicts, never raw log dumps.*

**Workflow run (2026-10-25):**

| Check | What it exercises | Result | Notes |
|---|---|---|---|
| selftest | full `tests/selftest.sh`: bash/python syntax (3 files), YAML (21 files incl. gateway template), JSON (0 files), no-turn-caps grep, config gate, pytest (28 tests), licence gate on this repo, gateway selftest | PASS | exit code captured directly, not through a pipe; output ends `SELFTEST: 56 checks passed` |
| config gate | `tests/config_gate.py` run standalone: roster, thinking levels, permissions, AGENTS.md chain string and doc contract, planning template, A2A roster source | PASS | exit code captured directly; all five assertion lines OK (below) |
| check-count cross-check | requested vs executed; no silently dropped checks | PASS | independent component recount equals the printed count; CI minimum not binding |
| content presence | DoD boxes 1–3: the three check steps in `big.md`, item 6 in `shadow.md`, the §7 layer in `AGENTS.md` | PASS | grep evidence below; old heading gone from agent files and template |

**Commands and exit codes (captured directly, not through a pipe):**

- `bash tests/selftest.sh > /tmp/opencode/t0039-selftest.log 2>&1; echo $?` → `SELFTEST_EXIT=0`;
  log ends `SELFTEST: 56 checks passed`.
- `python3 tests/config_gate.py > /tmp/opencode/t0039-configgate.log 2>&1; echo $?` →
  `CONFIGGATE_EXIT=0`.
- Component recount from disk: `SYN=3` (bash/python shebang files under `scripts team tests`),
  `YAML=20+1` (plus `team/gateway/agentgateway.yaml.template`), `JSON=0`, `+1` no-turn-caps, `+1`
  config gate, `+28` pytest, `+1` licence-check, `+1` gateway selftest →
  `3+21+0+1+1+28+1+1 = 56`, exactly the printed count.
- Content greps: `grep -n` over the three changed files (evidence below);
  `grep -rn 'The five things you check' .opencode/ planning/templates` → zero matches.

**Checks requested vs run:** 56 requested, 56 executed. The selftest's printed count (56) equals
the independent component recount (56), and both are above the CI minimum of 40
(`.github/workflows/team-selftest.yml:50`). One skip, disclosed not silent: `shellcheck absent,
skipped` (0 checks) — shellcheck is not installed on this host, and the selftest's rule for absent
tools is to print the skip in the output (`tests/selftest.sh:49`), so the reduced coverage is
visible in the log, not silent. No other check was dropped.

**Config gate detail** (all five assertion lines present in the log):

- `config-gate: roster OK (12 agents)` — the 11 workers plus robotnik, unchanged.
- `config-gate: thinking levels and permissions OK` — every worker on the `#low` variant with
  `task: deny` and `question: deny`; robotnik `mode: primary` with task allows for all 11 workers
  and full thinking.
- `config-gate: AGENTS.md chain and doc contract OK` — the `Shadow → Omega → Big → Charmy →
  Flicky` chain string and `## License Audit (Flicky)` intact after the §7 edit.
- `config-gate: planning template OK` — `planning/templates/planning-doc.md` still carries
  `## License Audit (Flicky)` in section order.
- `config-gate: A2A roster is file-driven OK` — no static `ROSTER = [` in `team/a2a/server.py`.

No-turn-caps, verified twice: the selftest grep over `team scripts tests .github AGENTS.md
.opencode/agents planning/templates` found no `maxTurns`/`max_turns` string, and the config gate
parsed the frontmatter of all 12 agent files.

**Content presence (DoD boxes 1–3, grep evidence):**

- `.opencode/agents/big.md:87` — `## Cinnamon / desktop RPM projects`, with the three numbered
  steps: GPG signature verification on a fresh consumer (lines 89–106: fresh consumer via
  `scripts/vm-create`, `gpgcheck=1` install of the full set, per-RPM `rpm -K`, `SIGPGP:pgpsig`
  key-ID vs documented-key fingerprint comparison, recorded-fingerprint equality, dnf-version
  assumption marked at 103–106), icon parity (107–114), feature parity (116–122).
- `.opencode/agents/shadow.md:39` — heading is `## The six things you check`;
  `.opencode/agents/shadow.md:83` — `### 6. Completeness — does the change contain everything it
  claims?` with the TASK-0038 failure mode named.
- `AGENTS.md:209` — `- **Cinnamon / desktop RPM projects:** GPG signature verification on a fresh
  consumer …`, the §7 layer bullet at the plan-prescribed position (between the "All Rocky Linux
  projects" and "Unit and integration tests" bullets).

**Verdict:** PASS. Both machine gates exit 0 with exit codes captured directly, so a masked
failure cannot read as green; the executed check count (56) equals the requested count on both
senses of "requested" — the selftest's own component structure, recounted from disk, and the CI
minimum (40) — with the single skip (shellcheck, absent on this host) disclosed in the output
rather than silent. The change's content is present in all three files and names the TASK-0038
failure modes it guards against. DoD box "`Big`: selftest passes with no silently dropped
checks" is satisfied. No code bug, no harness bug. The three nits in `## Review` are
`Shadow`/`Tails` items outside my scope; none affects a gate I ran.

---

## Docs

*Owner: `Vector`.*

| File | Sections touched | What changed |
|---|---|---|
| `README.md` | none, checked end to end | no statement this change affects; see the checked list below |
| `AGENTS.md` | section 7, Testing strategy | the `**Cinnamon / desktop RPM projects:**` layer bullet at `AGENTS.md:209-214`, between the "All Rocky Linux projects" and "Unit and integration tests" bullets. This bullet is the user-facing documentation for the new test layer and shipped as part of the change (implementation item 3). Verified against the check steps in `big.md:87-126`, and the two files agree including the "with evidence" and "with a reason" qualifiers that `Shadow`'s review required |

**Checked and needed no change:**

- `README.md` in full. The roster statements (the "12-agent team" line, the architecture diagram, the agent catalogue) are unaffected, and the change adds no agent. The `Big (Testing)` catalogue row "Test strategy, CI workflows, verification" already covers the three new Cinnamon/desktop RPM test layers, which are test layers that `Big` executes. The `Shadow (Reviewer)` row "Code quality and correctness review" already covers the new completeness item, and the README enumerates none of `Shadow`'s check items, so the five-to-six retitle changes nothing it says. The "How it works" review chain order is untouched. The "Active projects" Cinnamon row describes that project's own status, and this task does not change it (the layers take effect on the next TASK-0038 run, per the plan). A grep of the README for `five things`, `completeness`, `GPG`, `icon`, and `feature parity` returns only the unrelated `deploy.yml` GPG preflight row.
- No `CHANGELOG.md` exists in this repo, so there is no changelog entry to add.
- No other user-facing documentation exists in the repo. `team/` has no README, and the two prompt files at the repo root are operator drafts for other tasks.

**Could not verify:** nothing. The shipped state of all three changed files was read directly (`big.md:87-126`, `shadow.md:39` and `shadow.md:83-94`, `AGENTS.md:209-214`).

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
