# TASK-0024 — Sign the Cinnamon RPMs, enable gpgcheck, publish the release manifest

> **Section order below is fixed.** Each agent writes to its own section and no other. `Robotnik`
> reads only `## Status` and `## Next Actions`. Do not reorder, rename, or remove sections.

- **Created:** 2026-09-19

---

## Status

*Owner: `Robotnik`. Keep this SHORT and CURRENT — it is one of only two sections the PM reads, so a
stale entry means the whole loop runs on bad information.*

**Now (2026-09-19): task created from Omega's security review of TASK-0016 (low #3, supply-chain,
pre-existing, carried into the public docs).** The documented install path ships 64 RPMs from a
`file://` repo with `gpgcheck=0` (`repo-setup/setup-repo.sh`): no signature is ever checked, and
the doc's sha256 step verifies the copy, not the origin. A compromised `metalllinux` account or a
bad merged PR altering `rpms/` would run attacker code as root on a follower's machine. This task
closes the gap: sign the RPMs, ship the public key, turn on `gpgcheck=1`, and publish a sha256
manifest for the release as the trusted baseline. Source: `planning/docs/
TASK-0016-install-md-minimal-server.md` `## Security` (2026-09-19 entry) and `## Release`
(follow-up note, Knuckles).

**Environment / scope:**
- Files in scope: `repo-setup/setup-repo.sh`, the `.repo` block it writes, `rpms/` (all 64 RPMs
  re-signed), a new key/manifest location in `metalllinux/cinnamon-for-rocky10`, `INSTALL.md`,
  `README.md`. Project clone at `~/Linux/projects/cinnamon-for-rocky10/` (main at `893b22a`).
- Touches the DB schema: no
- Graphical UI: no
- Rocky Linux target: yes (Rocky Linux 10.2 VM verification on host `192.168.1.102`)

**Unknowns:**
- Where the GPG signing key lives and how it is managed. AGENTS.md §4: no key material in the
  repo, commits, logs, or planning docs; AGENTS.md §13: credential storage is GitHub Secrets only,
  no local credential files. The plan must settle key generation, private-key storage (host-side,
  outside the repo), and how the build/sign step obtains it without it ever entering git.
- Whether to re-sign the existing 64 RPMs in place or rebuild; the plan must pick and record why.
- Where the sha256 manifest lives (`rpms/SHA256SUMS`? repo root? release tag?) and what pins it.

---

## Definition of Done

*Owner: `Robotnik`, and nobody else. Written **before** any work starts. Objectively checkable —
if a box cannot be verified by looking at something, rewrite it.*

- [ ] **Signing key.** A GPG signing key for the repo exists; the **public** key ships in the
      project (documented path); no private key material appears anywhere in the repo, any commit,
      any log, or any planning doc (verified by `git grep` over the merged tree + the key-management
      decision recorded in `## Plan`).
- [ ] **RPMs signed.** Every one of the 64 published RPMs in `rpms/` carries a valid signature
      from that key: `rpm --checksig` over the full set reports only valid signatures, with the
      command and output recorded in `## Test Results`.
- [ ] **gpgcheck on.** `setup-repo.sh` installs the public key and writes the `.repo` file with
      `gpgcheck=1`; a follower running the documented procedure gets signature verification from
      dnf (not just a copy check).
- [ ] **Release manifest.** A sha256 manifest of the released set is published in the repo and
      tied to a git tag; `INSTALL.md` documents verifying against it.
- [ ] **Fresh-VM end-to-end.** On a fresh minimal Rocky 10.2 VM on host `192.168.1.102`: the
      documented procedure with `gpgcheck=1` installs the complete 22-name set (signatures
      verified by dnf) and reaches a working Cinnamon (Wayland) desktop; recorded in `## Test
      Results` with evidence.
- [ ] **Negative test.** A tampered copy of one RPM is detected: dnf refuses the install with a
      signature/repodata error (recorded in `## Test Results`); this is what the old `gpgcheck=0`
      path silently accepted.
- [ ] `Shadow`: no unresolved blockers or should-fix findings in `## Review`
- [ ] `Omega`: no unresolved findings above `low` in `## Security`
- [ ] `Big`: all harness checks PASS, with no silently dropped checks
- [ ] `Vector`: `INSTALL.md`/`README.md` updated to describe signing, key installation, and
      manifest verification
- [ ] `Knuckles`: merged to `metalllinux/cinnamon-for-rocky10` main via PR

---

## Next Actions

*Owner: whoever wrote last. The future only — delete what has been done. The second of the two sections
the PM reads.*

- [ ] `Amy`: write `## Plan` — key generation and private-key storage (host-side, outside the
      repo, per AGENTS.md §4/§13), sign-in-place vs rebuild, manifest location + tag scheme,
      `setup-repo.sh` changes, the fresh-VM + negative-test verification design.

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
