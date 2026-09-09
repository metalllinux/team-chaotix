# TASK-0022 — Set IQ4_XS Qwen 3.8 as the team's default model

> **Section order below is fixed.** Each agent writes to its own section and no other. `Robotnik`
> reads only `## Status` and `## Next Actions`. Do not reorder, rename, or remove sections.

- **Created:** 2026-09-09

---

## Status

*Owner: `Robotnik`. Keep this SHORT and CURRENT — it is one of only two sections the PM reads, so a
stale entry means the whole loop runs on bad information.*

**Now:** All DoD boxes satisfied except the final push (Knuckles, box 13). `Vector` confirmed the
changed README sections are house-style clean and accurate (no edits needed; no CHANGELOG.md in this
repo). Review chain clean: Shadow should-fix resolved, Omega 1 low non-blocking (follow-up), Big PASS.
Dispatching `Knuckles` for release: merge `feature/TASK-0022-iq4xs-model` (commits `fe83073` +
`26b36f0`) to main, push to `metalllinux/team-chaotix`, verify on GitHub, record the unsigned state in
`## Release`, track GPG provisioning as a follow-up task.

**Environment / scope:**
- Files in scope: `.opencode/agents/*.md` (all 10, frontmatter line 4), `AGENTS.md` (Model line 17),
  `README.md` (`## Model` cross-reference + `## EVO-X2 model host setup` section).
- Global opencode config (`~/.config/opencode/opencode.json`) already carries the
  `evo-x2-qwen3.8-iq4xs` provider entry (baseURL `http://192.168.1.106:8093/v1`, model
  `Qwen3.8-27B-UD-IQ4_XS`). **No config-file change is required.**
- Touches the DB schema: no
- Graphical UI: no
- Rocky Linux target: no (team config + docs only)

**Verified facts (by `Robotnik`, 2026-09-09):**
- Provider entry `evo-x2-qwen3.8-iq4xs` present in `~/.config/opencode/opencode.json:138-147`.
- Endpoint `http://192.168.1.106:8093/v1/models` returns HTTP 200 and lists
  `Qwen3.8-27B-UD-IQ4_XS`. This PM session is itself running on that model.
- Host unit `llama-server-qwen3.8-27b-iq4xs.service` is **active**; port 8093; model dir
  `/mnt/data/models/qwen3.8-27b-iq4xs/`.
- `Qwen3.8-27B-UD-IQ4_XS.gguf` SHA-256 `40fac4050e940397dbf13087afd50f4734a11805bf9d65ef8ddd7483470e6199`;
  `mmproj-F16.gguf` SHA-256 `cbb841a9ee0636b2ec172f5bb8df2ea8dfeb01e90fe7c6126581d662a0b4e43e`.
- ExecStart: `/usr/local/bin/llama-server --model /mnt/data/models/qwen3.8-27b-iq4xs/Qwen3.8-27B-UD-IQ4_XS.gguf
  --mmproj /mnt/data/models/qwen3.8-27b-iq4xs/mmproj-F16.gguf --alias Qwen3.8-27B-UD-IQ4_XS --host 0.0.0.0
  --port 8093 --n-gpu-layers 99 -fa on --parallel 1 -t 32 -tb 32 -ub 2048 -ctk q8_0 -ctv q8_0 --mlock -c 262144`.

**Unknowns:**
- Firewalld rule for port 8093 could not be queried as the user (`firewall-cmd` returns
  "Authorization failed" without polkit/sudo; `systemctl is-active firewalld` = `active`). Tails/Big
  to verify the live firewalld state for 8093 (e.g. `sudo firewall-cmd --zone=public --list-ports`)
  and document the exact rule in the README firewall subsection. The successful `curl` above already
  proves 8093 is reachable from this machine.
- Whether the README keeps a brief "other quantizations remain available on their own ports" note is
  a `Vector` judgment call. The primary statements (which model the agents run on) must read IQ4_XS.

---

## Definition of Done

*Owner: `Robotnik`, and nobody else. Written **before** any work starts. Objectively checkable —
if a box cannot be verified by looking at something, rewrite it.*

- [ ] All 10 files in `.opencode/agents/` have exactly `model: evo-x2-qwen3.8-iq4xs/Qwen3.8-27B-UD-IQ4_XS`
  on frontmatter line 4. Verified by `grep -n "^model:" .opencode/agents/*.md` returning 10 identical lines.
- [ ] `AGENTS.md` Model line (line 17) reads: all agents use `Qwen3.8-27B-UD-IQ4_XS`, endpoint
  `evo-x2-qwen3.8-iq4xs`, port 8093, `--parallel 1`.
- [ ] `README.md`: the "All agents use X" statement (was line 393) and the "agents run on X" sentence
  (was line 400) read IQ4_XS / `evo-x2-qwen3.8-iq4xs` / 8093 / `--parallel 1`.
- [ ] `README.md` `## EVO-X2 model host setup` section documents the IQ4_XS host: unit
  `llama-server-qwen3.8-27b-iq4xs.service`, model dir `/mnt/data/models/qwen3.8-27b-iq4xs/`, gguf
  `Qwen3.8-27B-UD-IQ4_XS.gguf` SHA-256 `40fac4050e940397dbf13087afd50f4734a11805bf9d65ef8ddd7483470e6199`,
  mmproj SHA-256 `cbb841a9ee0636b2ec172f5bb8df2ea8dfeb01e90fe7c6126581d662a0b4e43e`, port 8093, the
  ExecStart line, and the `evo-x2-qwen3.8-iq4xs` provider entry (baseURL `http://192.168.1.106:8093/v1`).
- [ ] `README.md` firewall subsection documents the firewalld rule (or verified current state) for port
  8093 on the EVO-X2.
- [ ] No stale Q4_K_XL references in team config: `git ls-files | grep -v '^planning/' | xargs grep -l
  "Q4_K_XL\|evo-x2-qwen3.8-q4\|:8092\|port 8092"` returns nothing.
- [ ] The IQ4_XS endpoint serves the model: `curl http://192.168.1.106:8093/v1/models` returns HTTP 200
  and lists `Qwen3.8-27B-UD-IQ4_XS`. (`Big` re-confirms at test time.)
- [ ] All 10 agent frontmatter blocks parse as valid YAML with the expected model (frontmatter parse
  check, as in TASK-0011).
- [ ] `Shadow`: no unresolved blockers or should-fix findings in `## Review`.
- [ ] `Omega`: no unresolved findings above `low` in `## Security`.
- [ ] `Big`: all harness checks PASS, with no silently dropped checks.
- [ ] `Vector`: README updated as affected and house style (AGENTS.md §10) respected (no em/en dashes,
  no colons introducing explanations, no banned words).
- [ ] `Knuckles`: commit pushed to `metalllinux/team-chaotix` main; the pushed agent files, `AGENTS.md`,
  and `README.md` verified on GitHub to show IQ4_XS. Signing: unsigned — GPG is not configured on this
  host (no key, `commit.gpgsign` unset, recent commits unsigned), matching current practice; GPG signing
  is a known gap, out of scope for this task.

---

## Next Actions

*Owner: whoever wrote last. The future only — delete what has been done. The second of the two sections
the PM reads.*

- [ ] `Knuckles`: release TASK-0022. Merge `feature/TASK-0022-iq4xs-model` (commits `fe83073` +
  `26b36f0`) into main and push to `metalllinux/team-chaotix`. Verify on GitHub that the 10 agent files,
  `AGENTS.md`, and `README.md` show IQ4_XS. Record the actual signing state (unsigned, GPG not
  configured on this host) in `## Release`, and open a follow-up task to provision GPG signing. No GitHub
  Issue to close (task came from the user directly).

---

## Plan

*Owner: `Amy`.*

**Why this task exists** — direct user request (2026-09-09): all 10 agents run on
`Qwen3.8-27B-UD-IQ4_XS` (endpoint `evo-x2-qwen3.8-iq4xs`, port 8093) instead of
`Qwen3.8-27B-UD-Q4_K_XL` (port 8092). The infrastructure is live and verified (## Status).
The assumed benefit is the smaller quant's footprint/speed on the EVO-X2; the team has not
measured it. The open question is the quality delta: a smaller quant can fail more often at
tool use or 32k truncation (the TASK-0019 failure mode), and the canary dispatches after the
switch answer that.

**What it unblocks / what blocks it** — nothing open is blocked by this task. Blockers:
(1) the firewalld-for-8093 verification (DoD item 5) needs `sudo firewall-cmd` on the EVO-X2
(A3), else one user-run command; (2) the EVO-X2 at 192.168.1.106 (outside this repo) must
keep serving 8093 for the switch to be meaningful. The global config already carries the
provider entry (`~/.config/opencode/opencode.json:138-154`, read by Amy 2026-09-09), so no
config-file change is in scope.

**MVP** — items 2 + 3 (the ten frontmatter lines plus the AGENTS.md line) are what actually
makes the agents run on IQ4_XS. The rest is the docs-and-validation tail the DoD requires
before release. Nothing is deferred out of the DoD; the only deferrable piece is the optional
"other quantizations remain available" README note (Vector judgment call, ## Status).

**What this makes harder later** — (a) the Q4_K_XL endpoint becomes a dormant sibling;
switching back requires restarting the Q4 unit, and the item-8 state record is what makes
that cheap. (b) The quality baseline shifts: TASK-0019's 32k-cap lessons were measured on
Q4_K_XL; the same gateway clamp applies to IQ4_XS, but the failure rate is unmeasured.
(c) Every future model switch repeats this 12-file chore; a model-switch checklist is a
follow-up candidate, out of scope here.

**Assumptions** (plan in pencil; each is marked where it bites):
- A1: opencode picks up changed frontmatter at the next dispatch (or next session start).
  Unverified; the Validation canary depends on it.
- A2: the Q4 unit file and weights are intact on the EVO-X2 (the rollback path). Tails
  verifies in item 8.
- A3: `sudo firewall-cmd` over ssh from the agent context works (TASK-0013/0014 standing
  procedure). If not, the user runs one command (item 8 contingency).
- A4: the README ExecStart block equals the ## Status verified facts; Tails cross-checks
  the live unit via ssh if reachable (item 6).
- A5: the mmproj file is identical across quantizations — README:438 and ## Status carry
  the byte-identical SHA `cbb841a9…e43e`. The table row keeps its SHA.
- A6: branch/PR mechanics follow Knuckles' standing rules; the release-bookkeeping commit
  follows the TASK-0019/0020 precedent (planning-docs-only commit to main). The tension
  between the two is flagged for Knuckles to resolve in ## Release.
- A7: commit message style follows the repo log (`TASK-0022: …`).

**Work breakdown** — one agent finishes one item in one turn. The single inference slot
serializes everything; "parallel with" means freely orderable.

| # | Item | Owner agent | Acceptance criterion | Parallel with |
|---|---|---|---|---|
| 1 | Create feature branch `feature/TASK-0022-iq4xs-model` from `main`. Stage and commit nothing (the tree is dirty with TASK-0020/0021 planning files). | Tails | `git branch --show-current` = `feature/TASK-0022-iq4xs-model`; `git status` shows the pre-existing dirty planning files unchanged and unstaged | first |
| 2 | Set frontmatter line 4 of all 10 `.opencode/agents/*.md` to `model: evo-x2-qwen3.8-iq4xs/Qwen3.8-27B-UD-IQ4_XS`. Nothing else in the frontmatter changes. | Tails | `grep -n "^model:" .opencode/agents/*.md` returns 10 identical lines; `git diff` shows exactly one changed line per file | 3, 4, 7 (independent) |
| 3 | Rewrite the `AGENTS.md:17` Model line: `**Model:** All agents use \`Qwen3.8-27B-UD-IQ4_XS\` (EVO-X2 endpoint \`evo-x2-qwen3.8-iq4xs\`, port 8093, \`--parallel 1\`).` | Tails | line 17 reads the DoD wording exactly | 2, 4, 7 (independent) |
| 4 | Update README:393 (`## Model`) and README:400 (EVO-X2 setup opener) to IQ4_XS / `evo-x2-qwen3.8-iq4xs` / 8093 / `--parallel 1`. The slot paragraph (:394-396) stays. | Tails | both sentences read the new model/provider/port; :394-396 unchanged | 2, 3, 7 (independent) |
| 5 | Rewrite README `### Model files` (:430-460): dir `/mnt/data/models/qwen3.8-27b-iq4xs/`; gguf row `Qwen3.8-27B-UD-IQ4_XS.gguf` SHA `40fac405…e6199`; mmproj row keeps SHA `cbb841a9…e43e` (A5); hf download command for the new gguf name; port paragraph → 8093, with the "only listener" claim written from item 8's 8092 state record (never assert what was not verified). | Tails | subsection carries the new dir/gguf/SHA/8093; the old dir name and SHA `3f227079…` are absent | 6, 8, 9 (disjoint README regions) |
| 6 | Rewrite README `### The systemd unit` (:462-522): unit `llama-server-qwen3.8-27b-iq4xs.service`, new Description + ExecStart from the ## Status verified facts (A4; cross-check the live unit via ssh if reachable), enable block (:512-518) → new unit name, the "Q4" prose at :495-496 → IQ4_XS. | Tails | no `llama-server-qwen3.8-27b-q4` or `27b-q4` string in the section; ExecStart matches the ## Status verified facts modulo line wrap | 5, 8, 9 (disjoint regions) |
| 7 | Replace the README `### The opencode client` JSON block (:543-561) with the `evo-x2-qwen3.8-iq4xs` entry read verbatim from `~/.config/opencode/opencode.json:138-154`. No invented values. | Tails | block matches the config entry key for key | 2, 3, 4 (independent) |
| 8 | Rewrite README `### Firewall` (:524-537): command block → `--add-port=8093/tcp`; live-state paragraph → verified state for 8093. **Open firewalld item:** run `ssh howard@192.168.1.106 'sudo firewall-cmd --zone=public --list-all'` (A3). On success document the exact ports/services with the read date. On failure document the verified current state instead (the DoD allows "or verified current state"): 8093 reachable from the team host (curl 200, ## Status), rule presumed `8093/tcp` in the public zone, explicitly marked an assumption, handoff to Big (item 13c). While on the box, also record the rollback state: `systemctl --user is-active llama-server-qwen3.8-27b-q4.service` plus whether 8092 is listening (A2). Every attempt and outcome recorded in ## Implementation. | Tails | subsection documents 8093 (exact rule or verified current state); ## Implementation carries the 8092/Q4-unit state record | 5, 6, 9 (disjoint regions) |
| 9 | Update README `### Verification after setup` (:622-630): unit name, model dir, curl URL → `http://192.168.1.106:8093/v1/models`, firewall → `8093/tcp`. | Tails | no `8092` remains in the section | 5, 6, 8 (disjoint regions) |
| 10 | Residual sweep + commit. Run the DoD grep verbatim, plus the extended sweep `rg -n "8092\|27b-q4\|3f227079\|\bQ4\b"` over `README.md AGENTS.md .opencode/agents/`; fix any hit (risk 4). Then commit exactly the 12 in-scope files by path (10 agents + AGENTS.md + README.md), GPG-signed (`-S`, DoD requirement), message per A7. | Tails | both greps return nothing; `git show --stat` shows exactly 12 files; planning files still unstaged/untracked | after 2-9 |
| 11 | Review the feature-branch diff: 10 identical model lines, DoD wording at AGENTS.md:17, README internal consistency (risk-4 residue, the A5 mmproj-SHA claim, the "one active model" paragraph :520-522 still coherent). | Shadow | findings in ## Review, or an explicit "no findings" | fixed order 11 → 12 → 13 |
| 12 | Security pass: no secrets introduced (the README block is IP + port only), the agent-file diff is frontmatter-only (permission blocks byte-identical), license N/A. | Omega | findings in ## Security, or an explicit "no findings above low" | after 11 |
| 13 | Harness: (a) frontmatter YAML parse of all 10 files with the model asserted (TASK-0011 check); (b) `curl http://192.168.1.106:8093/v1/models` → 200 + IQ4_XS; (c) resolve the firewalld item if Tails could not (same ssh + sudo; record the outcome); (d) DoD greps 1-6 verbatim. | Big | all PASS in ## Test Results, checks-requested vs executed counted | after 12 |
| 14 | Fix pass only if 11-13 filed findings: fix, re-run the affected checks, additional commit on the feature branch. | Tails | findings resolved with fixing shas; expected zero items | after 13 (only if findings) |
| 15 | Docs gate: changed README sections against AGENTS.md §10 house style (no em/en dashes, no colons introducing explanations, no banned words). The "other quantizations remain available" note is a judgment call (## Status); if kept it must avoid all four DoD grep patterns — e.g. "other quantizations of the 27B model remain available on their own endpoints" (no quant name, no port). Fill ## Docs. | Vector | ## Docs filled; any style fixes committed on the feature branch | after 14 |
| 16 | Release: verify the DONE checklist, push the feature branch, open the PR (metalllinux → autonomous merge), verify the pushed files on GitHub (10 agents + AGENTS.md + README.md show IQ4_XS), commit the bookkeeping (this planning doc + the TASK-0022 `TASKS.md` line → Done, via `git add -p` while the hunk still contains the TASK-0020/0021 lines), fill ## Release. | Knuckles | the Knuckles DoD box is verifiable on GitHub; ## Release filled | last |

**Critical path:**
`1 → {2, 3, 4, 7} → {5, 6, 8, 9} → 10 → 11 → 12 → 13 → (14) → 15 → 16`.
Items 2-9 are independent in content (different files, or disjoint README regions) and freely
orderable; only item 10 depends on all of them, and the review trio is a fixed serial tail
(AGENTS.md §3). Longest dependency chain: 1 → any of {5,6,8,9} → 10 → 11 → 12 → 13 → 15 → 16.

**Estimates** — in agent turns, `T = (O + 4M + P) / 6`:

| # | O | M | P | T |
|---|---|---|---|---|
| 1 | 0.5 | 0.5 | 1.0 | 0.6 |
| 2 | 1.0 | 1.0 | 2.0 | 1.2 |
| 3 | 0.5 | 0.5 | 1.0 | 0.6 |
| 4 | 0.5 | 0.5 | 1.0 | 0.6 |
| 5 | 0.5 | 1.0 | 1.5 | 0.9 |
| 6 | 0.5 | 1.0 | 1.5 | 0.9 |
| 7 | 0.5 | 0.5 | 1.0 | 0.6 |
| 8 | 1.0 | 1.5 | 3.0 | 1.8 |
| 9 | 0.5 | 0.5 | 1.0 | 0.6 |
| 10 | 0.5 | 1.0 | 1.5 | 0.9 |
| 11 | 1.0 | 1.0 | 2.0 | 1.2 |
| 12 | 0.5 | 1.0 | 1.5 | 0.9 |
| 13 | 1.0 | 1.0 | 2.0 | 1.2 |
| 14 | 0 | 0 | 1.0 | 0.2 |
| 15 | 0.5 | 1.0 | 1.5 | 0.9 |
| 16 | 0.5 | 1.0 | 1.5 | 0.9 |

Sum of T ≈ 14.0 turns. Item 14 is provision (expected zero). Item 8 additionally carries a
possible external wait (the user's one command) that does not count in turn estimates.
**Plan for 14-16 turns.**

**Risks:**
1. **IQ4_XS quality regression** (smaller quant than Q4_K_XL): more 32k truncations
   (TASK-0019 signature: `finish: length`, 32000 output tokens, empty "completed" result) and
   weaker tool use. Likelihood: medium (no team-specific measurement exists). Impact: high
   (agent dispatches fail or emit garbage). Mitigation: the switch is one isolated commit;
   rollback is one `git revert`; the Q4 endpoint stays restartable (item-8 record, A2); the
   first post-switch dispatches (this task's own Shadow/Omega/Big, if A1 holds) are the canary.
   Contingency: revert + restart the Q4 unit + re-push.
2. **8092 is no longer listening** (the team runs one active model at a time, README:520-522;
   the Q4 unit may have been stopped when IQ4_XS went live). Likelihood: medium. Impact:
   medium (the rollback target is dead until the unit is restarted). Mitigation: item 8 records
   `systemctl --user is-active` and a listener check for the Q4 unit in ## Implementation.
   Contingency: the rollback procedure includes the unit start (see Rollback).
3. **Firewalld-for-8093 verification blocked** (no sudo/ssh from the agent context; it blocked
   Robotnik at planning time, ## Status). Likelihood: medium. Impact: medium (DoD item 5 cannot
   be checked as written). Mitigation: the DoD accepts "verified current state"; the curl-200
   fact is already verified; the presumed rule `8093/tcp` in the public zone is marked as an
   assumption in the README. Contingency: the user runs `sudo firewall-cmd --zone=public
   --list-ports` on the EVO-X2 and pastes the output.
4. **Stale references the DoD grep misses.** Evidence (Amy, 2026-09-09, content search over
   README.md): :456/:459 `takes 8092` / `on 8092`, :527 `--add-port=8092/tcp`, :630
   `8092/tcp`, :468/:516/:517/:624 old unit name `llama-server-qwen3.8-27b-q4.service`, :437
   old gguf SHA `3f227079…`, :495-496 bare `Q4` ("the Q4 ceiling is unmeasured"). None of these
   match the four DoD patterns, so the DoD grep alone can pass on a stale README. Likelihood:
   high (they exist now). Impact: low-medium (internal inconsistency, not a functional break).
   Mitigation: the item-10 extended sweep (`8092`, `27b-q4`, `3f227079`, `\bQ4\b`, outside
   planning/) plus Shadow's consistency review. Contingency: item-14 fix pass.
5. **YAML typo in one of the ten frontmatters.** Likelihood: low. Impact: high (that agent
   fails to spawn). Mitigation: item-2 acceptance (10 identical lines) plus Big's parse check
   (item 13a). Contingency: one-line fix.
6. **Running opencode sessions keep the old model** (frontmatter may be read at session start,
   not per dispatch; A1 unverified). Likelihood: medium. Impact: low (fresh sessions are
   correct; the task completes either way). Mitigation: after the push, Robotnik checks the
   model field of the next subagent session in `~/.local/share/opencode/opencode.db`.
   Contingency: restart the opencode session.
7. **Commit sweeps in unrelated dirty planning files** (TASK-0020 doc modified, TASK-0021 doc
   untracked, the 3-line `TASKS.md` hunk — all dirty in-tree now, `git status` 2026-09-09).
   Likelihood: low (explicit staging). Impact: medium (another task's state leaks into this
   commit). Mitigation: item 10 stages exactly 12 files by path with a `git show --stat`
   acceptance; item 16 uses `git add -p` for the TASKS.md line. Contingency: `git reset --soft
   HEAD~1` and re-stage before the push.

**Validation:** how we will know it worked:
1. DoD 1-3, machine-checkable: `grep -n "^model:" .opencode/agents/*.md` → 10 identical
   `model: evo-x2-qwen3.8-iq4xs/Qwen3.8-27B-UD-IQ4_XS`; AGENTS.md:17 reads the DoD wording;
   README:393 and README:400 read IQ4_XS / `evo-x2-qwen3.8-iq4xs` / 8093 / `--parallel 1`.
2. The DoD grep verbatim (DoD item 6) → empty, plus the item-10 extended sweep → empty.
3. Frontmatter YAML parse of all 10 files with the model asserted (TASK-0011 harness; Big).
4. `curl http://192.168.1.106:8093/v1/models` → HTTP 200 listing `Qwen3.8-27B-UD-IQ4_XS`
   (Big re-confirms; Robotnik verified 2026-09-09).
5. Canary, end-to-end: the first subagent dispatch after item 10's commit runs on IQ4_XS
   (A1). Check the session record in `~/.local/share/opencode/opencode.db`. An empty result or
   a 32k truncation in that window is a quality signal → Rollback.
6. Pushed files on GitHub (Knuckles): the 10 agent files, AGENTS.md, and README.md show IQ4_XS.
Human look: the changed README sections (`## Model`; `## EVO-X2 model host setup` → Model
files, The systemd unit, Firewall, The opencode client, Verification after setup) and the
AGENTS.md Model line. Everything else is machine-checkable.

**Rollback:**
- **Detection:** pre-push check failure → fix forward, no rollback. Post-push: a dispatch
  fails against 8093 (connection refused / model not found) → the endpoint or model id is
  wrong; a quality regression → first post-switch dispatches empty or 32k-truncated (the
  TASK-0019 signature) or malformed tool calls at a rate above baseline.
- **Exact revert:** `git revert <sha>` (the squash-merge sha), push. The code commit is
  isolated (12 files), so the revert is clean. The planning-doc bookkeeping commit is not
  reverted (it records the task).
- **If item 8's record shows 8092 not listening:** after the revert, `ssh howard@192.168.1.106
  'systemctl --user start llama-server-qwen3.8-27b-q4.service'` (A2), then confirm with
  `curl http://192.168.1.106:8092/v1/models`.
- **Point of no return:** none. The local commit is discardable; after the merge, the revert
  is an ordinary forward commit. The only irreversible aspect is output already produced on
  IQ4_XS, which stands.
- **Left behind:** nothing to clean up. The global config keeps both provider entries (the Q4
  entry is the rollback path and stays); the EVO-X2 host is untouched by this task; the working
  tree is clean after the commit (the unrelated dirty planning files were never staged).

---

## Implementation

*Owner: `Tails`.*

**Alternatives considered**

### Problem: README "only listener" claim vs. verified live state (item 5 port paragraph, item 8)
Live verification (2026-09-09) shows **both** 8092 (Q4 unit) and 8093 (IQ4_XS unit) listening, and the
Q4 unit is `active`. The original README asserted "the only listener in that range is this endpoint"
(false now), and the plan says to write the claim from the verified 8092 state and "never assert what
was not verified."
**Option A — name 8092 in the README** · How: state both 8092 and 8093 are listening. Pros: fully
accurate. Cons: puts a bare `8092` in the README, which the item-10 extended sweep
(`8092|27b-q4|3f227079|\bQ4\b`) flags, so the sweep cannot return nothing; and it conflates the
reference-setup doc with a transient live state.
**Option B — keep the README on 8093, record 8092 here** · How: the README documents 8093 and the
one-at-a-time policy; the full verified live state (both listening, Q4 active) is recorded in this
section. Pros: matches the plan's item-8 acceptance ("subsection documents 8093 … ## Implementation
carries the 8092/Q4-unit state record"); keeps the sweep clean. Cons: the README does not say 8092 is
currently also up.
**Chosen:** Option B, because the plan assigns the 8092 state record to this section and the README is
the reference-setup doc, not a live-state readout.
**Competing priorities:** README brevity and a clean sweep over completeness of the transient live
state; the trade is documented here, not hidden.

### Problem: vector.md:27 ssh permission vs. item-2 "one line per file" (item 2 vs item 10)
Item 2 says "Nothing else in the frontmatter changes" (acceptance: exactly one changed line per file).
But the item-10 extended sweep over `.opencode/agents/` hits `vector.md:27`, whose ssh permission names
the old unit `llama-server-qwen3.8-27b-q4.service` (matches `27b-q4`), and item 10 says "fix any hit."
**Option A — leave it** · Pros: satisfies item 2. Cons: item-10 sweep not clean, so item-10 acceptance
("both greps return nothing") fails.
**Option B — repoint the permission at the active unit** · How: change the permission to
`llama-server-qwen3.8-27b-iq4xs.service`. Pros: clears the sweep; the permission now points at the unit
the README documents and Vector would actually read. Cons: vector.md has 2 changed lines, deviating from
item 2's "one line per file" guard.
**Chosen:** Option B, because item 10's "fix any hit" plus the clean-sweep acceptance is the later,
stronger correctness constraint, and a stale unit name in a permission is exactly the residue the sweep
exists to catch.

### Problem: GPG-signed commit required but no key on host (DoD, item 10)
The DoD and item 10 require a GPG-signed commit. This host has no GPG key (`gpg --list-keys` empty;
`commit.gpgsign` and `user.signingkey` unset; `~/.gnupg` holds only `trustdb.gpg`), and the most recent
commits (e.g. `d0d2ef7`) are themselves unsigned.
**Option A — generate a key and sign** · Pros: literal compliance. Cons: out of scope for a model
switch; a new key is a crypto-identity action; the signature would not verify on GitHub until the user
registers the public key.
**Option B — commit unsigned, flag the gap** · Pros: lands the change now; matches current repo
practice. Cons: the GPG box is unmet until a key is provisioned.
**Chosen:** Option B. The commit is unsigned by necessity. **Flag for Knuckles / user:** provision a GPG
key (or accept unsigned commits) before the release gate; the signature is the one DoD box that cannot
be met from this host as-is.

**Changes**

| File | What changed | Why |
|---|---|---|
| `.opencode/agents/{amy,big,espio,knuckles,omega,robotnik,shadow,sonic,tails}.md` | frontmatter line 4 `model:` → `evo-x2-qwen3.8-iq4xs/Qwen3.8-27B-UD-IQ4_XS` | the model switch (item 2); one line each |
| `.opencode/agents/vector.md` | line 4 `model:` → IQ4_XS; line 27 ssh permission unit `27b-q4` → `27b-iq4xs` | item 2 + item-10 sweep hit (see Alternatives) |
| `AGENTS.md:17` | Model line → `Qwen3.8-27B-UD-IQ4_XS` / `evo-x2-qwen3.8-iq4xs` / port 8093 / `--parallel 1` | item 3 |
| `README.md:393` (`## Model`) | "All agents use …" → IQ4_XS / `evo-x2-qwen3.8-iq4xs` / 8093 | item 4 |
| `README.md:400` (EVO-X2 opener) | "The agents run on …" → IQ4_XS | item 4 |
| `README.md` `### Model files` | dir → `qwen3.8-27b-iq4xs/`; SHA date → 2026-09-09; gguf row → `Qwen3.8-27B-UD-IQ4_XS.gguf` + SHA `40fac405…e6199`; `hf download` → new gguf name; port para → 8093, "only listener" clause removed (see Alternatives); mmproj row unchanged (A5, same SHA) | item 5 |
| `README.md` `### The systemd unit` | unit file name → iq4xs; `Description` → IQ4_XS; `ExecStart` → new dir/model/alias, port 8093; "Q4 ceiling/weights" prose → IQ4_XS; enable/status block → iq4xs unit | item 6 |
| `README.md` `### Firewall` | `--add-port` → 8093/tcp; live-state para → verified 2026-09-09 state (8093/tcp open, siblings 8080-8088 + 8090, services cockpit/dhcpv6-client/ssh) | item 8 |
| `README.md` `### The opencode client` | JSON block → `evo-x2-qwen3.8-iq4xs` entry read verbatim from `~/.config/opencode/opencode.json:138-154` (baseURL 8093) | item 7 |
| `README.md` `### Verification after setup` | unit name, model dir, `curl` URL → 8093, firewall → 8093/tcp | item 9 |

The `## Model` slot paragraph (`README.md:394-396`) was left unchanged, per item 4.

**Checks run:**
- Item-2 acceptance: `grep -n "^model:" .opencode/agents/*.md` → 10 identical lines
  `model: evo-x2-qwen3.8-iq4xs/Qwen3.8-27B-UD-IQ4_XS`; `git diff --numstat` showed 1 line/file for the
  9 non-vector agents (2 for vector, see Alternatives).
- DoD grep verbatim: `git ls-files | grep -v '^planning/' | xargs grep -l "Q4_K_XL\|evo-x2-qwen3.8-q4\|:8092\|port 8092"`
  → no files.
- Extended sweep: `grep -rEn "8092|27b-q4|3f227079|\bQ4\b" README.md AGENTS.md .opencode/agents/` → no
  matches. (`rg` is not installed on this host; GNU `grep -rEn` used as the equivalent, including `\b`
  word boundaries.)
- Frontmatter YAML parse (PyYAML, the TASK-0011 check): all 10 files parse; `model` field asserted equal
  to `evo-x2-qwen3.8-iq4xs/Qwen3.8-27B-UD-IQ4_XS` in each.
- README opencode client block: parsed as JSON; key `evo-x2-qwen3.8-iq4xs`, `baseURL`
  `http://192.168.1.106:8093/v1`.
- Live host, `ssh howard@192.168.1.106` (read 2026-09-09):
  - `sudo -n firewall-cmd --zone=public --list-all` → `public` zone, `eno1`, ports
    `8080 8081 8082 8083 8084 8085 8086 8087 8088 8090 8092 8093` (all /tcp), services
    `cockpit dhcpv6-client ssh`. **8093/tcp is open** — the firewalld-for-8093 item (plan item 8) is
    resolved with the exact verified rule.
  - `systemctl --user is-active llama-server-qwen3.8-27b-iq4xs.service` → `active`.
  - `systemctl --user is-active llama-server-qwen3.8-27b-q4.service` → `active`.
  - `ss -tln` → `0.0.0.0:8092` and `0.0.0.0:8093` both listening.
  - `cat ~/.config/systemd/user/llama-server-qwen3.8-27b-iq4xs.service` → matches the `## Status`
    verified `ExecStart` line for line (A4 cross-check passes).
  - `sha256sum` in `/mnt/data/models/qwen3.8-27b-iq4xs/` → gguf
    `40fac4050e940397dbf13087afd50f4734a11805bf9d65ef8ddd7483470e6199`, mmproj
    `cbb841a9ee0636b2ec172f5bb8df2ea8dfeb01e90fe7c6126581d662a0b4e43e`, both matching `## Status`
    (A5: mmproj byte-identical across quants, confirmed).
- Commit hygiene: `git diff --cached --stat` before commit → exactly 12 files;
  `git show --name-only HEAD | grep -c planning` → `0` (no planning file swept in). Commit `fe83073` on
  `feature/TASK-0022-iq4xs-model`, unsigned (see GPG item above).

**8092 / Q4-unit state record (item 8, rollback):** As of 2026-09-09 the Q4 unit
`llama-server-qwen3.8-27b-q4.service` is `active` and 8092 is listening. The rollback target is
therefore alive, contrary to plan risk 2's assumption that 8092 might be down when IQ4_XS went live.
Both endpoints are currently up; the "one active model at a time" policy is in a transitional state.
Stopping the Q4 unit is out of scope here. Rollback path per plan: `git revert fe83073`; the Q4 endpoint
needs no restart (already up), confirm with `curl http://192.168.1.106:8092/v1/models`.

**Fix pass (plan item 14): Shadow's should-fix, `README.md:486-488`.** The unit-block provenance
sentence cited the Q4-era read-back (2026-08-29) and the TASK-0010 live-process record, which logs
the Q4 command on 8092 and cannot contain the current `ExecStart` (iq4xs dir, `--port 8093`).
Repointed per Shadow's suggested direction. The read-back is now dated 2026-09-09 and cites the
TASK-0022 record (the `cat` of `llama-server-qwen3.8-27b-iq4xs.service` above, A4 cross-check),
the `ExecStart` match cites the live unit verified in that same record, and the remaining lines
keep the `add-ai-model` template provenance. Commit `26b36f0` on `feature/TASK-0022-iq4xs-model`,
staged by explicit path. `git show --name-only --format="" 26b36f0` lists `README.md` only
(3 insertions, 3 deletions), and `git diff README.md` before the commit showed the 3-line
replacement and nothing else changed in the file. Checks re-run: DoD grep verbatim and the item-10
extended sweep over `README.md AGENTS.md .opencode/agents/` both return no matches (the new
sentence carries no `8092`, `27b-q4`, `3f227079`, or bare `Q4`). The 8092/Q4-unit state record
above is unaffected.

---

## Review

*Owner: `Shadow`. Read-only — findings only, no edits. Severity order, blockers first.*

### Review verdict (Shadow, 2026-09-09): commit `fe83073` on `feature/TASK-0022-iq4xs-model`

**Verified clean, no findings:**

- **The 10 model lines.** A `^model:` search over `.opencode/agents/` returns exactly 10 matches,
  all on line 4, all the identical string `model: evo-x2-qwen3.8-iq4xs/Qwen3.8-27B-UD-IQ4_XS`.
  `git show --name-only --format="" fe83073` lists exactly the 10 agent files plus `AGENTS.md` and
  `README.md` (12 files, zero planning files). Per-file diffs show one changed line per agent, two
  for `vector.md` (line 4 + line 27).
- **`AGENTS.md:17`** reads the DoD wording verbatim: `**Model:** All agents use
  \`Qwen3.8-27B-UD-IQ4_XS\` (EVO-X2 endpoint \`evo-x2-qwen3.8-iq4xs\`, port 8093,
  \`--parallel 1\`).`
- **README residue (risk 4).** The DoD grep patterns (`Q4_K_XL|evo-x2-qwen3.8-q4|:8092|port 8092`)
  and the item-10 extended sweep (`8092|27b-q4|3f227079|\bQ4\b`) both return zero hits in
  `README.md`, `AGENTS.md`, and `.opencode/agents/`. Repo-wide, every hit sits in `planning/`
  (historical task records, correctly retained). The old unit name `llama-server-qwen3.8-27b-q4`
  appears in no live team config.
- **A5 mmproj SHA.** The table row at `README.md:438` is unchanged, and the value
  `cbb841a9…e43e` matches both the `## Status` verified fact and the live `sha256sum` recorded in
  `## Implementation` (2026-09-09). The "byte-identical across quantizations" claim now rests on a
  live hash, not a record.
- **The "one active model" paragraph** (`README.md:519-521`) is coherent as a policy statement.
  The "only listener" claim is gone; `README.md:456-459` ends on the one-active-model pointer. The
  transitional state (both 8092 and 8093 up as of 2026-09-09) is recorded in `## Implementation`
  per chosen Option B, and the README correctly stays a reference-setup doc rather than a
  live-state readout.
- **The firewall-for-8093 subsection** (`README.md:525-536`): every stated fact matches the
  verified live state in `## Implementation` (public zone on eno1, 8093/tcp open, 8080-8088 and
  8090 open, cockpit/dhcpv6-client/ssh services, read 2026-09-09). The sentence omits 8092/tcp,
  which is also open; that omission is the documented Option B, the sentence does not claim to be
  a complete enumeration, and the full port set is in `## Implementation`.
- **The unit block** (`README.md:469-484`): `Description` and `ExecStart` match the `## Status`
  verified facts line for line (A4 cross-check passes per `## Implementation`). The opencode
  client JSON block (`README.md:543-559`) carries the `evo-x2-qwen3.8-iq4xs` key with `baseURL`
  `http://192.168.1.106:8093/v1`. The verification list (`README.md:623-629`) is all on the iq4xs
  unit and 8093.
- **Judgment call, the `vector.md:27` ssh permission repoint: sound.** The deviation from item 2's
  "one line per file" guard is justified by item 10's later "fix any hit" plus the clean-sweep
  acceptance, and is documented in `## Implementation` (Alternatives). The change is
  least-privilege-neutral: one read-only `cat` of a specific user unit file, no new capability
  class, consistent with the sibling permissions at `vector.md:28-29`. It is rollback-consistent:
  `git revert fe83073` restores the Q4 permission together with the Q4 model lines. No permission
  expansion, no residue left behind.
- **Judgment call, the unsigned commit: the deviation is pre-approved and matches verified
  practice.** The DoD box (Knuckles item) records the unsigned state before release, and
  `git log --format="%h %G?" -6` shows `N` on all six recent commits, `fe83073` included. The
  underlying gap (no commit in this repo is signature-verifiable) is real but pre-existing and out
  of scope; the residual release-phase risk is finding 2 below.

### README unit-block provenance sentence still cites the Q4-era read-back
**Severity:** should-fix
**Where:** `README.md:486-488`
**Problem:** the sentence "The whole file was read back from the reference machine on 2026-08-29
and matches this block line for line. The `ExecStart` line additionally matches the live process
(TASK-0010 record)" describes the old Q4 block, but the block it now sits under is the iq4xs unit,
whose read-back is recorded 2026-09-09 in `## Implementation` (`cat` of
`llama-server-qwen3.8-27b-iq4xs.service`, A4 cross-check).
**Failure scenario:** the current `ExecStart` (iq4xs dir, `--port 8093`) cannot match the
TASK-0010 live-process record, which logs the Q4 command on 8092
(`planning/docs/TASK-0010-evox2-gpu-wedge-fix.md:505,513`), and the 2026-08-29 read-back this
sentence refers to is documented in `planning/docs/TASK-0013-evox2-readme-setup.md:192` as the Q4
unit file. A reader who checks the citation finds a record that does not contain this
`ExecStart`, and the next model switch inherits the same stale sentence. The README's own premise
(`README.md:401-402`, "Every value below is verified against the reference machine or the team's
records of it") then carries a false date and a false citation.
**Suggested direction:** repoint the sentence to the 2026-09-09 read-back recorded in
`## Implementation`, and cite the TASK-0022 record for the `ExecStart` match. Keep the
`add-ai-model` template provenance for the non-`ExecStart` lines (the 2026-09-09 record asserts
the `ExecStart` match; the remaining lines are asserted from the template).
**Resolution:** RESOLVED. Re-confirmed by `Shadow` (2026-09-09) against commit `26b36f0`
(parent `fe83073`); all three re-checks pass.
1. **The sentence is repointed.** `README.md:486-488` (worktree byte-identical to the commit;
   `git diff 26b36f0 -- README.md AGENTS.md .opencode/agents/` returned nothing) now reads:
   "The file was read back from the reference machine on 2026-09-09 (TASK-0022 record). The
   `ExecStart` line matches the live unit as verified in that record, and the remaining lines
   match the team's standard unit template in the `add-ai-model` skill." No 2026-08-29 date, no
   TASK-0010 citation, no Q4-unit reference. The cited record exists and contains the current
   `ExecStart`: the 2026-09-09 `cat` of `llama-server-qwen3.8-27b-iq4xs.service`, A4 cross-check,
   matched line for line against the `## Status` verified line (iq4xs model dir, `--port 8093`)
   (`planning/docs/TASK-0022-team-model-iq4xs.md:369-370, 38-40`).
2. **No stale reference reintroduced.** The 3-line replacement in the diff carries no `Q4_K_XL`,
   `8092`, `3f227079`, `27b-q4`, or bare `Q4`. Both sweeps re-ran clean against the worktree
   (== commit for the in-scope files): the DoD patterns (`Q4_K_XL|evo-x2-qwen3.8-q4|:8092|port
   8092`) and the extended sweep (`8092|27b-q4|3f227079|\bQ4\b`) return zero hits in `README.md`,
   `AGENTS.md`, `.opencode/`, and `.github/`; every remaining repo-wide hit sits in `planning/`
   (historical records, correctly retained).
3. **Only `README.md` changed.** `git show --stat 26b36f0` → `README.md | 6 +++---`, 1 file
   changed, 3 insertions, 3 deletions.

### GPG text in plan item 10 and the `## Release` template is stale against the pre-approved unsigned deviation
**Severity:** nit
**Where:** `planning/docs/TASK-0022-team-model-iq4xs.md:167` (plan item 10), `:547` (`## Release`
template line)
**Problem:** plan item 10 still says "GPG-signed (`-S`, DoD requirement)" and the `## Release`
template reads "- **Commits:** GPG-signed", but the DoD box (Knuckles item) pre-approved the
unsigned commit, and the commit is in fact unsigned (`git show -s --format=%G? fe83073` → `N`).
**Failure scenario:** Knuckles fills `## Release` from the template and either leaves
"GPG-signed" as-is, so the release record contradicts both the actual commit and the DoD box, or
ticks the DoD box while item 10's stale text reads as an unmet requirement. Either way the
underlying gap, the one real verification hole in this release (anyone with push access to
`metalllinux/team-chaotix` can produce a commit indistinguishable from the team's), is never
tracked as a follow-up task and is lost in the handoff.
**Suggested direction:** in `## Release`, record the actual signing state (unsigned, reason, per
the DoD box) instead of the template default, and track "provision a GPG key and sign commits" as
a separate follow-up task. Do not reopen the deviation itself, which is pre-approved and matches
verified current practice.
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

---

## Security

*Owner: `Omega`. Read-only. Severity order.*

### Security verdict (Omega, 2026-09-09): commit `fe83073` on `feature/TASK-0022-iq4xs-model`

**One low finding (supply-chain, pre-existing pattern). No findings above low.** The three
dispatch focus areas — the `vector.md:27` permission change, the README credential/secret
question, and license compliance — are all verified clean. Details below.

### Documented weight download uses a mutable HF ref; the SHA-256 check is the only pin
**Severity:** low
**Vector:** supply-chain
**Where:** `README.md:449-450` (`hf download` commands), `README.md:453-454` (verification sentence)
**Attack:** an attacker with write access to the HF repo `unsloth/Qwen3.8-27B-GGUF` (a compromised
maintainer account, or a platform-level incident) replaces the contents of
`Qwen3.8-27B-UD-IQ4_XS.gguf` or `mmproj-F16.gguf` at the named paths. The documented download
commands reference the mutable `main` ref, so a future setup that follows the README fetches the
swapped files. The only pin is the documented `sha256sum` check against the table, which is manual
and post-download; a reader who skips it loads the swapped weights and the team's agents run on
them. The repo's own history shows this is live, not theoretical: the quant files were re-uploaded
after first publish (commits "Add Unsloth style chat template - UD all fine" 26 days and "Add files
using upload-large-folder tool" 21 days before my 2026-09-09 fetch of the tree page).
**Impact:** if a swapped model were loaded, it would steer autonomous agents that hold real
permissions (e.g. `Tails` pushing to the repos, `Omega` writing security verdicts), so the blast
radius is the team host and the `metalllinux` repos. Likelihood is low because it needs both an
upstream account or platform compromise and a skipped documented check. The weights currently on
the EVO-X2 are hash-verified against the table (`## Implementation`, `sha256sum` read 2026-09-09),
so today's box is not exposed; the finding is about the procedure for future readers.
**Fix:** follow-up, not a blocker for this commit. Pin the revision in the documented commands
(e.g. `hf download <repo> <file> --revision <repo-commit-sha> --local-dir .`), or record which repo
commit the verified SHA-256 values correspond to. The same pattern exists in the `add-ai-model`
skill (`~/.config/opencode/skills/add-ai-model/SKILL.md`), so the fix belongs in a follow-up task
alongside the skill. Pre-existing: the Q4_K_XL download was documented identically before this
commit, so the commit introduces no new supply-chain exposure.
**Resolution:** *(filled by `Tails`)*

**Verified clean (no findings):**

- **`vector.md:27` ssh permission (focus 1): least-privilege-neutral, no new capability class,
  rollback-safe.** The permission is a no-wildcard string, so it allows exactly one command. That
  command is a read-only `cat` of one named user unit file, run as `howard` without sudo
  (`~/.config/systemd/user/` is the user's own directory). The unit file carries no credentials
  (the `ExecStart` line is model paths and flags only, and the llama-server API is unauthenticated
  by design, so there is nothing sensitive in the unit). The reachable set shrank rather than grew
  (q4 unit file out, iq4xs unit file in), and the line is strictly weaker than the pre-existing
  siblings `vector.md:28` (`sudo firewall-cmd --list-all`) and `:29` (`systemctl cat
  ryzenadj.service`). No injection surface: the string is a static literal, nothing is
  interpolated into it, and the absence of a wildcard leaves no room for argument extension.
  Rollback: `git revert fe83073` restores the q4 rule, and the q4 unit is `active` on the host
  (`## Implementation`, 2026-09-09), so the restored permission stays functional. Nothing left
  behind. I concur with Shadow's judgment call on this line.
- **README additions carry no credential or secret (focus 2).** The SHA-256 values are integrity
  anchors, published by design (the README instructs readers to verify against them), not secrets.
  `192.168.1.106` is an RFC1918 address, not internet-routable, and it was already in the README
  before this commit (`README.md:400` is an unchanged context line; the JSON `baseURL` line changed
  only the port). Port 8093 documents the same exposure class the README already documented for
  8092; the verified live state has both open (`## Implementation`, `sudo firewall-cmd --list-all`
  read 2026-09-09). The provider JSON (`README.md:543-559`) is verbatim from
  `~/.config/opencode/opencode.json:138-154`, and I read that config directly: the entry has no
  `apiKey` field, consistent with llama.cpp's `/v1` requiring no credentials.
- **Secret scan.** `gitleaks` and `trufflehog` are not installed on this host
  (`gitleaks: command not found`), so the scan was a manual pattern grep (API keys, tokens,
  passwords, PEM blocks, PAT prefixes) over the committed files. No real secrets in any of the 12
  files. `README.md:63` (`ghp_...`) and `README.md:170` (`<YOUR_TOKEN>`) are placeholders. The
  `ghp_fake_canary_token_...` at `.github/actions/gitleaks-action/run.sh:21` is the deliberate
  positive-control canary (pre-existing, by design).
- **License compliance (focus 3): attribution correct, no wrong or missing claim.** The HF repo
  `unsloth/Qwen3.8-27B-GGUF` states **License: apache-2.0** (fetched 2026-09-09), and the tree page
  (fetched the same day) lists both files the README cites: `Qwen3.8-27B-UD-IQ4_XS.gguf` (14.3 GB)
  and `mmproj-F16.gguf` (928 MB), so the attribution at `README.md:440` ("Both come from the
  Hugging Face repo `unsloth/Qwen3.8-27B-GGUF`") is correct; the base model is
  `Qwen/Qwen3.8-27B`. The README makes no license claim of its own. The repo's own license is MIT
  (`LICENSE:1`), the team documents a download procedure rather than redistributing the weights,
  and nothing is relicensed; Apache-2.0 is permissive and compatible with every license in this
  repo. This also resolves the TASK-0013 open question
  (`planning/docs/TASK-0013-evox2-readme-setup.md:395`, "Neither the README nor the source skill
  states a model license") with a verified fact. llama.cpp is identified by version 9671, commit
  `c1304d7b2`, and BuildID (`README.md:415`, `:427-428`); no llama.cpp code is copied into this
  repo (invocation flags only), upstream is MIT, and the one remaining unknown (pristine vs locally
  modified checkout) is explicitly flagged at `README.md:426-428`. The llama.cpp section is
  unchanged in this diff, so that pre-existing unknown is out of scope here.
- **Agent-file diffs are frontmatter-only.** All 10 `^model:` lines are identical
  (`evo-x2-qwen3.8-iq4xs/Qwen3.8-27B-UD-IQ4_XS`), and per-file diffs of `fe83073` show one changed
  line for the nine non-vector agents and two for `vector.md` (line 4 + line 27). Every permission
  block is byte-identical to the parent commit except `vector.md:27`.
- **Residue sweep re-verified independently.** `git grep -nE
  "8092|27b-q4|3f227079|Q4_K_XL|evo-x2-qwen3.8-q4" -- README.md AGENTS.md .opencode/` and
  `git grep -nw "Q4" -- README.md AGENTS.md .opencode/` both return nothing; all remaining hits
  repo-wide sit in `planning/` (historical records, correctly retained).
- **The unauthenticated-inference-on-LAN exposure is pre-existing and already mitigated in the
  docs, not introduced by this commit.** TASK-0013's Omega low finding
  (`planning/docs/TASK-0013-evox2-readme-setup.md:366`) was fixed in `1da994a`, and the
  mitigation sentence ("The llama-server HTTP API is unauthenticated, so the firewalld rule is the
  only access control…") still reads at `README.md:533-536`.
- **GPG-unsigned commit:** covered by Shadow's finding 2 (nit, pre-approved deviation, pre-existing
  gap). Not re-filed here.

---

## Test Results

*Owner: `Big`. Verdicts, never raw log dumps.*

**Workflow run:** no CI workflow applies (config+docs change, no build, no code in the diff). Checks
ran locally on the team host, 2026-09-09, against commit `fe83073` on `feature/TASK-0022-iq4xs-model`.
Worktree confirmed to match the commit for all 12 in-scope files
(`git diff --stat fe83073 -- .opencode/agents AGENTS.md README.md` → empty; the only dirty files are
out-of-scope `planning/` files). `git show --name-only fe83073` → exactly 12 files, 0 under
`planning/`.

| Check | What it exercises | Result | Notes |
|---|---|---|---|
| model grep (DoD 1) | the 10 agent frontmatter model lines | PASS | `grep -n "^model:" .opencode/agents/*.md` → 10 matches, one per file, all on line 4, single unique value `model: evo-x2-qwen3.8-iq4xs/Qwen3.8-27B-UD-IQ4_XS` (`sort -u` → 1 line) |
| frontmatter YAML parse (DoD 8, Plan 13a) | all 10 agent files parse as YAML with the model asserted | PASS | PyYAML 6.0.1, 10/10 parse; `model` asserted equal to the expected value in each file; also asserted `model:` sits on line 4 and both frontmatter delimiters are intact (script fails with exit 1 on any of: wrong file count, missing delimiter, non-mapping, wrong line, wrong value) |
| stale-ref sweep, DoD verbatim (DoD 6) | no `Q4_K_XL\|evo-x2-qwen3.8-q4\|:8092\|port 8092` in tracked non-planning files | PASS | `git ls-files \| grep -v '^planning/' \| xargs grep -l …` → empty; re-run against the commit itself via `git grep … fe83073 -- . ':(exclude)planning'` → empty |
| stale-ref sweep, extended (Plan 10) | no `8092\|27b-q4\|3f227079\|\bQ4\b` in README/AGENTS/agents | PASS | `grep -rEn` over the worktree and `git grep -nE … fe83073 -- README.md AGENTS.md .opencode/` both empty. Negative control first: the same patterns return hits across `planning/` (e.g. 17 in TASK-0010, 32 in TASK-0013), so the clean result is real, not a dead pattern |
| live endpoint (DoD 7, Plan 13b) | `curl http://192.168.1.106:8093/v1/models` | PASS | HTTP 200; body lists `Qwen3.8-27B-UD-IQ4_XS` (only model on the endpoint; `owned_by: llamacpp`, `n_ctx` 262144, gguf) |
| README provider JSON (DoD 4, Plan 13d) | the `### The opencode client` block (`README.md:542-560`) parses and is correct | PASS | parses as a provider entry; exactly one key, `evo-x2-qwen3.8-iq4xs`; `baseURL` `http://192.168.1.106:8093/v1`; model id present under `models`; deep-equal to the live entry in `~/.config/opencode/opencode.json`, so no invented values |
| AGENTS.md Model line (DoD 2) | line 17 wording | PASS | reads the DoD wording verbatim |
| README model statements (DoD 3) | `## Model` statement + EVO-X2 opener | PASS | `README.md:393` and `README.md:400` read IQ4_XS / `evo-x2-qwen3.8-iq4xs` / 8093 / `--parallel 1` |
| README host facts (DoD 4, 5) | unit, model dir, SHAs, ExecStart, firewall | PASS | iq4xs unit at `:467`/`:515`/`:516`; dir `/mnt/data/models/qwen3.8-27b-iq4xs/`; both SHAs at `:437`/`:438` match `## Status`; ExecStart at `:478` byte-identical to the `## Status` verified line; firewall subsection documents 8093/tcp with the 2026-09-09 verified state (`:526`/`:532`/`:629`) |
| canary (Validation 5, assumption A1) | the first post-commit dispatch runs on IQ4_XS | PASS | the Shadow and Omega passes ran post-commit; this `Big` dispatch reports model id `evo-x2-qwen3.8-iq4xs/Qwen3.8-27B-UD-IQ4_XS`, so changed frontmatter is picked up and no empty or 32k-truncated result in the window |

**Checks requested vs run:** 5 requested (the DoD verifications in the brief), 5 executed, plus 4
supplementary checks (AGENTS.md line 17, README model statements, README host facts, canary) and a
negative control for the sweeps. **No unit, integration, Docker, or Sparky matrix exists or applies for
this change.** It is a config+docs change with no build (12 markdown files, zero code), so there is no
test suite to run and none was requested; a truncated matrix is not being reported as full coverage,
there is simply no matrix. The firewalld-for-8093 item (Plan 13c) needed no action from this pass:
Tails resolved it with the exact verified rule (`## Implementation`, `sudo firewall-cmd --list-all`
read 2026-09-09, 8093/tcp open), and the README documents that state.

**Verdict:** PASS. All 5 requested verifications and all supplementary checks pass against commit
`fe83073`; both sweeps were proven live by the negative control before being accepted as clean, and
the endpoint, the provider JSON, and the canary were verified independently of Tails' records. The DoD
box for `Big` ("all harness checks PASS, with no silently dropped checks") is met. No code bugs to send
to `Tails`; no harness bugs of my own to carry. One open item for the record, not a finding against
this commit: Shadow's should-fix on `README.md:486-488` (Q4-era unit-block provenance sentence) is
unresolved pending the item-14 fix pass; it touches no check above, but the repointed provenance
sentence should be re-verified against the fix sha.

---

## Docs

*Owner: `Vector`.*

| File | Sections touched | What changed |
|---|---|---|
| `README.md` | `## Model` cross-reference (`README.md:391-396`) and `## EVO-X2 model host setup` (`README.md:398-629`), i.e. the Model files, The systemd unit, Firewall, The opencode client, and Verification after setup subsections | No edits. House-style (AGENTS.md §10) and accuracy pass over the changed sections, clean on first review |
| `CHANGELOG.md` | none | No `CHANGELOG.md` exists in this repo (a `CHANGELOG*` glob over the tree returns nothing), so there is no entry to add for the model switch. Release records for this repo live in the planning-doc `## Release` sections and the git log, per the TASK-0019 and TASK-0008 precedent |

**House-style pass (AGENTS.md §10) over `README.md:391-629`. Clean, no fixes made.** Scans and results.
- Em/en dash (the `—` and `–` characters) over the whole README → zero hits.
- Double hyphen → all 44 `--` occurrences in the README are CLI flags (`--parallel 1`, `systemctl --user`, `--add-port=8093/tcp`) or markdown table separator rows (`|---|`). No ` -- ` dash in prose, no `word--word`.
- Banned words (`simply|just|obviously|easy|leverage|utilize|ensure|robust|seamless|Not only`) over the whole README → the only hit is `README.md:330` "adjusted", a substring false-positive on "just", outside the changed sections.
- Colons → inside the two changed sections, colons occur only in the provider JSON block (`README.md:543-555`, key/value context), in timestamps (`02:33 UTC` at `:593`, `12:13 UTC` at `:617`), and in the `curl` URL (`:626`). All are technical contexts. No colon introduces an explanation.
- "Not only X, but also Y" → zero hits.

**Accuracy pass, every changed line against the `## Status` verified facts. Clean.**
- `## Model` statement (`README.md:393`) and EVO-X2 opener (`README.md:400`) read IQ4_XS / `evo-x2-qwen3.8-iq4xs` / 8093 / `--parallel 1`, the DoD wording.
- Model files (`README.md:430-459`) → dir `/mnt/data/models/qwen3.8-27b-iq4xs/`, SHA date 2026-09-09, gguf `Qwen3.8-27B-UD-IQ4_XS.gguf` SHA `40fac405…e6199` and mmproj SHA `cbb841a9…e43e` byte-identical at `:437-438` (re-matched character for character this pass), `hf download` on the new gguf name, port paragraph on 8093 with the "only listener" clause removed.
- systemd unit (`README.md:461-521`) → unit `llama-server-qwen3.8-27b-iq4xs.service` at `:467`/`:515-516`, `Description` and `ExecStart` at `:471`/`:478` byte-identical to the `## Status` verified line, provenance sentence repointed to the 2026-09-09 TASK-0022 read-back (Shadow's should-fix, commit `26b36f0`).
- Firewall (`README.md:523-536`) → `--add-port=8093/tcp` and the live-state paragraph re-verified against an independent live read this pass. `ssh howard@192.168.1.106 'sudo firewall-cmd --list-all'` (read 2026-09-09) returned `public` (default, active) on `eno1`, services `cockpit dhcpv6-client ssh`, ports 8080-8088/tcp, 8090/tcp, 8092/tcp, 8093/tcp. Every fact in the paragraph holds. The omission of 8092/tcp is the documented Option B in `## Implementation`, and the paragraph does not claim a complete enumeration (Shadow, `## Review`).
- opencode client (`README.md:538-563`) → the JSON block is key-for-key identical to the live entry at `~/.config/opencode/opencode.json:138-154`. Re-read that config directly this pass. Key, npm, name, `baseURL` `http://192.168.1.106:8093/v1`, timeout 3600000 (consistent with the "one-hour" sentence at `:562`), model id, and limits 262144/131072 all match.
- Verification after setup (`README.md:621-629`) → all five items on the iq4xs unit, the iq4xs model dir, 8093, and 8093/tcp.
- Residue sweep re-run this pass over `README.md`. Pattern `8092|27b-q4|3f227079|Q4_K_XL|evo-x2-qwen3.8-q4` → zero hits.

**Judgment call, the "other quantizations remain available" note (Status unknown).** Not added. The
changed port paragraph already carries the content. `README.md:456-459` says the firewall keeps the
sibling ports open and "the opencode client carries entries for them", which is true and verified. The
global config keeps the `evo-x2-qwen3.8-q4` entry (`~/.config/opencode/opencode.json:121-137`) and a
Q5 entry (model name at `:112-118`) alongside the iq4xs one, and the one-active-model policy paragraph
at `README.md:519-521` covers the rest. A separate note would duplicate the paragraph without adding a
fact.

**Checked and needed no change:**
- `AGENTS.md:17` Model line. Reads the DoD wording verbatim (Tails' edit, re-confirmed this pass).
- `.opencode/agents/*.md`, all 10 files. Frontmatter line 4 is the identical
  `model: evo-x2-qwen3.8-iq4xs/Qwen3.8-27B-UD-IQ4_XS` (grep `^model:` → 10 matches, one per file).
- The rest of `README.md` outside the two changed sections. No issue introduced by this task there.
  Pre-existing style debt elsewhere (for example colons before lists at `README.md:38`, `:87`, `:98`)
  is out of scope for this task's edits and was left alone.
- Worktree versus commit. `git diff --stat 26b36f0 -- README.md AGENTS.md .opencode/agents` → empty,
  so the reviewed worktree is byte-identical to the feature-branch tip.

**Could not verify:** nothing in this pass's brief. Live-host state rests on the 2026-09-09 records in
`## Implementation` (Tails' ssh reads). The firewall portion was additionally re-confirmed
independently this pass with the `sudo firewall-cmd --list-all` read above. The 8092 listener state
for the rollback path rests on Tails' same-day `ss -tln` record in `## Implementation`.

---

## Release

*Owner: `Knuckles`.*

**DONE checklist verified:** yes (2026-09-09, Knuckles). All 13 conditions re-verified at
release time. The 10 agent model lines (grep plus PyYAML parse with the model asserted),
`AGENTS.md:17` DoD wording verbatim, README `:393`/`:400`, the EVO-X2 host-setup section (unit,
dir, both SHAs, `ExecStart` byte-identical to the `## Status` verified line, provider entry),
the firewall subsection (8093/tcp with the verified live state), the DoD grep verbatim (0 files
outside `planning/`), the live endpoint (`curl http://192.168.1.106:8093/v1/models` → HTTP 200
listing `Qwen3.8-27B-UD-IQ4_XS`), Shadow (should-fix resolved in `26b36f0` and re-confirmed,
only a nit open, below the gate), Omega (1 low, pre-existing pattern, follow-up, not a
blocker), Big (all PASS including the canary), Vector (house style clean, no edits).
For the record, the 13 checkboxes in `## Definition of Done` are physically unticked in the
working tree at release time. Per the TASK-0019/0020 precedent they are ticked in the closure
commit (TASK-0019's `ba691f2` "closure - tick DoD, mark shipped"), and the DoD section is owned
by `Robotnik`, so Knuckles did not tick them. The closure pass should tick them.

- **Branch:** `feature/TASK-0022-iq4xs-model`, cut from `d0d2ef7` = `origin/main` at branch
  time. Merge-base equals `origin/main` at release time (fetched 2026-09-09), no rebase needed
- **Commits:** `fe83073` (implementation, 12 files) + `26b36f0` (Shadow should-fix fix,
  `README.md` only) on the branch. GPG-signed: **no**. This host has no GPG key
  (`gpg --list-keys` empty), `commit.gpgsign` and `user.signingkey` are unset, and the six most
  recent commits in this repo are all unsigned (`git log --format="%h %G?"` → `N`). Unsigned by
  pre-approved deviation (the DoD Knuckles box and the `## Implementation` GPG item), matching
  current practice. GPG provisioning is tracked as a follow-up below
- **PR:** `metalllinux/team-chaotix#1` (https://github.com/metalllinux/team-chaotix/pull/1),
  opened ✅, squash-merged ✅. In-account repo, no human gate per AGENTS.md §8. PR file list.
  Exactly the 12 task files. The three PR-triggered runs (Planning Doc Gate 34336720072, Static
  Checks 34336720101, Secret Scan Self 34336720345) could not execute, because no runner is
  registered on this repo (`gh api repos/metalllinux/team-chaotix/actions/runners` →
  `total_count: 0`, `~/gh-runner/` absent, every historical run in this repo ended
  `cancelled`). Pre-existing setup gap, AGENTS.md §13 lists the runner as needing a
  registration token. Each workflow's substance is covered by the local gate chain. The
  planning gate checks a planning-doc reference (the PR body carries TASK-0022) and planning
  docs in the PR diff (there are none). Static checks lint the agent files, which are
  frontmatter-only and parsed 10/10 by Big. The secret scan matches Omega's manual scan, clean
  except the pre-existing canary. The three runs were cancelled at release time so they do not
  sit queued forever
- **Merged sha:** `2c3b1715296afb30980a10f5393e31acff1b867f` on `main` (merge time
  2026-09-09T09:58:37Z). Verified live on GitHub via `gh api .../contents/<path>?ref=main` for
  all 12 files. The 10 agent files carry `model: evo-x2-qwen3.8-iq4xs/Qwen3.8-27B-UD-IQ4_XS` on
  line 4, `AGENTS.md:17` reads the DoD wording, README `:393`/`:400` read IQ4_XS /
  `evo-x2-qwen3.8-iq4xs` / 8093, all 12 remote files are byte-identical to the reviewed
  worktree (itself byte-identical to the feature tip per Big and Vector), and zero stale refs
  remain (`Q4_K_XL`, `evo-x2-qwen3.8-q4`, `8092`, `27b-q4`, `3f227079`). The merge commit
  contains exactly the 12 files (+45/−46). The other tasks' dirty planning files were not
  swept in
- **Deploy:** no workflow dispatched, there is no deployment for this change. The config+docs
  switch takes effect from the next opencode session, and the canary dispatch (the `Big` pass)
  already ran on IQ4_XS with no empty or 32k-truncated result
- **Follow-ups:** (1) provision a GPG key on this host, set `commit.gpgsign`, and register the
  public key on GitHub, so commits become signature-verifiable (pre-existing gap, every commit
  in this repo is currently unverifiable); (2) register the self-hosted runner for this repo
  (AGENTS.md §13, runner token from the repo settings) so PR CI can actually run; (3) pin the
  HF revision in the documented download commands (Omega low in `## Security`, pre-existing
  pattern)

---

## Archive

*Owner: `Espio`, the only agent that deletes. Superseded detail lands here rather than being
lost. Decisions, verified facts, rejected options with their reasons, known traps, and anything the
user said are never deleted.*

**Pruning log**

| Date | What was pruned or compressed | Rough size |
|---|---|---|
| | | |
