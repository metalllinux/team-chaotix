# TASK-0037 — Team platform: cycle graph, A2A, portless, licence gate, gateway; new Flicky licence agent

> **Section order below is fixed.** Each agent writes to its own section and no other. `Robotnik`
> reads only `## Status` and `## Next Actions`. Do not reorder, rename, or remove sections.

- **Created:** 2026-10-23

---

## Status

*Owner: `Robotnik`. Keep this SHORT and CURRENT — it is one of only two sections the PM reads, so a
stale entry means the whole loop runs on bad information.*

**Now:** landed on main as `28e4b2a` (branch `improvements/team-platform-2026-10-23`, merged
2026-10-24). Local selftest green: 55 checks, 28 pytest tests, licence gate PASS. Review chain
sections below are still to be filled by the agents.

**Environment / scope:**
- Files in scope: `team/` (new package), `tests/` (new), `scripts/` (a2a-server.py, a2a-send,
  licence-check), `.opencode/agents/` (flicky new; robotnik task-allows), `AGENTS.md`,
  `README.md`, `planning/templates/planning-doc.md`, `.github/workflows/` (team-selftest.yml,
  licence-check.yml), `.github/actions/licence-gate/`, `.gitignore`
- Touches the DB schema: no (SQLite run checkpoints live in `.runs/`, gitignored)
- Graphical UI: no
- Rocky Linux target: yes (selftest runs on the host runner)

**Unknowns:** none. (The runner question is resolved: the repo is public, and GitHub does not
allow self-hosted runner registration on public repos. Operator decision 2026-10-24: keep it
public; the local pre-push selftest is the effective gate.)

---

## Definition of Done

*Owner: `Robotnik`, and nobody else. Written **before** any work starts. Objectively checkable —
if a box cannot be verified by looking at something, rewrite it.*

- [x] `team/` package implements graph, a2a, portless, licenses, gateway with tests under `tests/`
- [x] `tests/selftest.sh` passes locally on the host and is the CI entry point
- [x] No turn caps anywhere in team source (selftest gate)
- [x] All workers on `#low`, robotnik full thinking, robotnik the only delegator (config gate)
- [x] `flicky` agent exists, fifth in the review chain, owns `## License Audit (Flicky)`
- [x] `scripts/licence-check` emits the four outcomes with exits 0/6/7/8 and passes on this repo
- [x] Workflows `Team Selftest` and `Licence Check` defined, no LLM calls (self-hosted runner
  registration is N/A while the repo is public; local pre-push selftest is the effective gate per
  operator decision 2026-10-24)
- [x] A2A surface: agent card from roster files, message/send, message/stream, tasks/get,
  tasks/cancel, contextId
- [x] portless CLI installed at `~/.local/bin/portless`; registry machine-local
- [x] agentgateway template + `gateway.sh` (apply/up/down/status/selftest)
- [ ] `Shadow`: no unresolved blockers or should-fix findings in `## Review`
- [ ] `Omega`: no unresolved findings above `low` in `## Security`
- [ ] `Big`: all harness checks PASS, with no silently dropped checks
- [ ] `Charmy`: no unresolved findings in `## License (Charmy)`
- [ ] `Flicky`: gate outcome `PASS`, or a `POLICY_EXCEPTION` recorded in `## License Audit (Flicky)`
- [ ] `Vector`: documentation updated as affected
- [ ] Human review completed (if external PR or deployment)

---

## Next Actions

*Owner: whoever wrote last. The future only — delete what has been done. The second of the two sections
the PM reads.*

- [ ] `Robotnik`: enable the pre-push hook on fresh clones (`git config core.hooksPath scripts/hooks`)
- [ ] `Shadow`, `Omega`, `Big`, `Charmy`, `Flicky`: run the review chain over this doc (sections
  below are the placeholders)
- [ ] `Flicky`: first real gate run on a target project (not this repo) to prove the path end to end

---

## Plan

*Owner: `Amy`.*

**Why this task exists** — operator requirement (2026-10-23): the team gets a real platform, not
just agent files. The cycle in AGENTS.md is documented prose; it becomes a runnable, checkpointed
state machine. The A2A adapter becomes file-driven (roster from `.opencode/agents/`) with
`contextId` and cancellation. portless, documented in AGENTS.md sections 7 and 12, becomes real
tooling. The licence gate gets a dedicated agent and a machine-checkable scanner with a house
policy. agentgateway gets a template and a wrapper. Testing moves to GitHub Actions on the
self-hosted runner. Standing constraints: no max-turns or turn caps anywhere; every agent but
robotnik runs `#low`; robotnik is the only delegator and is unrestricted in what it may update.

**What it unblocks / what blocks it** — unblocks: durable multi-stage runs that survive process
death (checkpoints keyed by contextId), other team instances discovering and addressing this team
by agent card, named services on one machine without port bind collisions. Blocked by: nothing
inside this repo; the runner registration needs the repo's own token.

**MVP** — the python package plus tests plus the two workflows. Deferred: systemd units for the
adapter and proxy (the wrapper scripts are the entry points; units can follow as tasks of their
own), the TLS proxy path on machines without openssl.

**What this makes harder later.** The cycle graph becomes the dispatch backbone; any change to
the stage set is a graph change, so stage renames must update `team/graph/state.py`, the
config gate, and AGENTS.md together.

**Work breakdown** — decomposed until one agent finishes one item in one turn.

| # | Item | Owner agent | Acceptance criterion | Parallel with |
|---|---|---|---|---|
| 1 | `team/graph/` state, cycle, checkpoint | Tails | cycle runs start→archive with a fake runner; fix loop recovers; halt at max revisions; checkpoint persists under thread id | |
| 2 | `team/a2a/` server + client | Tails | card generated from roster files; send/stream/get/cancel exercised in tests; contextId minted once | 1 |
| 3 | `team/portless/` registry + proxy + CLI | Tails | alias/resolve/list/rm/probe tested; Host-routed proxy test over HTTP | 1 |
| 4 | `team/licenses/` scanner + policy | Tails | four outcomes with exits 0/6/7/8; passes on this repo; fixture repos cover MIT/Apache/GPL/BUSL/header cases | 1 |
| 5 | `team/gateway/` template + gateway.sh | Tails | template renders; selftest boots on ephemeral ports and probes | 1 |
| 6 | `flicky` agent + robotnik task-allows + AGENTS.md/README/template contract | Amy | config gate passes: roster of 12, chain ends in Flicky, template carries the section | 1 |
| 7 | `tests/selftest.sh` + CI workflows | Tails | selftest asserts a minimum check count; workflows run on the self-hosted runner without LLM calls | 2–6 |

**Critical path:** 1 → (2,3,4,5,6 in parallel) → 7 → merge → CI green.
**Validation:** `bash tests/selftest.sh` locally; `Team Selftest` and `Licence Check` in CI;
`scripts/licence-check` on this repo; `tests/config_gate.py`.
**Rollback:** everything is additive except `scripts/a2a-server.py` (rewritten as a thin entry
point over `team/a2a/server.py`) and two agent files. Revert the merge commit and the old
static-roster server file comes back with it; `.runs/` never existed in git.

---

## Implementation

*Owner: `Tails`.*

**Alternatives considered**

### Problem: <what needed solving>
**Option A — thin wrappers over a new package (chosen)** · How: `team/` holds the
implementation; `scripts/` keeps the entry points so existing service definitions and muscle
memory survive. Pros: testable without a model (injected runners), one source of truth, existing
names keep working. Cons: two locations for a2a until the old file is retired (retired: it is
now a five-line entry point).
**Option B — rewrite in place** · How: grow `scripts/a2a-server.py` into the platform.
Pros: no new package. Cons: untestable shell-script shape, roster stays hardcoded, no place
for the graph or the licence engine.
**Chosen:** A, because the operators' standing requirement is a deterministic test gate, and a
package with injected runners is the only shape that makes CI runnable without a model.
**Competing priorities:** what was traded away, explicitly. The single inference slot is
untouched (the graph runs stages one at a time, as the team always has). The VM isolation rule
(section 12) is untouched; this task's worktree is for this repo's own development, which the
operator directed.

**Changes**

| File | What changed |
|---|---|
| `team/graph/{state,cycle,checkpoint}.py` | langgraph StateGraph of the cycle; langchain-core messages in state; SQLite checkpoints under `.runs/` keyed by A2A contextId; `max_revisions` loop guard only |
| `team/a2a/{server,client}.py` | A2A server (roster from `.opencode/agents/`, contextId, tasks/cancel, agent card) + stdlib client |
| `team/portless/{core.py,portless}` | name registry + Host-routed proxy with local `*.localhost` CA; CLI |
| `team/licenses/{core.py,policy.yaml}` | scanner + house policy; four outcomes, exits 0/6/7/8 |
| `team/gateway/{agentgateway.yaml.template,gateway.sh}` | config template + apply/up/down/status/selftest wrapper |
| `tests/{selftest.sh,conftest.py,config_gate.py,test_*.py}` | single test entry point; agent config gate; suites with injected fakes |
| `scripts/a2a-server.py` | rewritten as the entry point over `team/a2a/server.py` |
| `scripts/a2a-send`, `scripts/licence-check` | new entry points |
| `.opencode/agents/flicky.md` | new dedicated licence agent, `#low`, fifth in the review chain |
| `.opencode/agents/robotnik.md` | task-allows gains `flicky`; everything else unchanged |
| `AGENTS.md` | twelve agents; chain ends in Flicky; section 9 (licence), 11 (no turn caps), 15 (A2A), 18 (team platform) |
| `planning/templates/planning-doc.md` | `## License Audit (Flicky)` section + DoD item |
| `.github/workflows/team-selftest.yml`, `licence-check.yml` | CI gates on the self-hosted runner, SHA-pinned checkout, no LLM calls |
| `.github/actions/licence-gate/` | composite action wrapping the gate for CI |
| `.gitignore` | `.runs/` (run checkpoints are machine-local evidence) |

**Checks run:** compile · linter · harness — `bash tests/selftest.sh` (syntax gates, YAML/JSON
parse, no-turn-caps rule, config gate, pytest, licence gate on this repo).

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

## License (Charmy)

*Owner: `Charmy`. Fourth in the review chain. Every license is verified at the upstream source
repository and the ref used, never from a copy in this repo.*

**Project license:** <license> — appropriate | finding

**Imported code**

| Component | Source (repo @ ref) | License (verified at) | Obligations met | Status |
|---|---|---|---|---|
| | | | yes/no + what | pass/finding |

**Verdict:** pass | findings *(Tails fixes; the chain re-runs until clean)*

---

## License Audit (Flicky)

*Owner: `Flicky`. Fifth in the review chain. Runs the machine gate; the gate is evidence, and
this section records it. Never grants or refuses an exception.*

**Gate:** `scripts/licence-check <project-root>` (exit 0 `PASS` · 6 `POLICY_EXCEPTION` ·
7 `BLOCK` · 8 `HARD_STOP`)

**Outcome:** PASS | POLICY_EXCEPTION | BLOCK | HARD_STOP *(state the exit code that produced it)*

**Declarations**

| File / component | Declared | Verified at (upstream @ ref) |
|---|---|---|
| | | |

**Exceptions recorded:** *(each POLICY_EXCEPTION with the clause quoted and why it is lawful,
or "none")*

**Verdict:** pass | findings *(fail-closed: a gate run that cannot be read is FAIL)*

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
