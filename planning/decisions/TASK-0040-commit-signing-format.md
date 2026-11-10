# TASK-0040 — Commit-signing format and registration level

**Decision owner:** `Amy` (plan) · **Task doc:** `planning/docs/TASK-0040-commit-signing-key-setup.md`

## 1. Problem

Commits the team pushes from this host carry no signature, and GitHub cannot attribute them.
Evidence (observed 2026-11-08 unless cited):

- TASK-0039 `## Status` (2026-10-25, DONE entry): the merged commit "is not GPG-signed (no
  commit-signing key on this host; the pre-existing team-wide provisioning gap, open follow-up
  per TASK-0022/0030)".
- `git config --global --list` → `fatal: unable to read config file '/home/howard/.gitconfig':
  No such file or directory`. No global git configuration exists.
- `gpg --list-secret-keys` on the default home lists no secret keys; `ls -la ~/.gnupg` shows
  an empty `private-keys-v1.d`. `gpg --version | head -1` → `gpg (GnuPG) 2.4.5`.
- `~/AI/secrets/` (dir 700) holds the house secrets, all mode 600: `token.md` (41 B),
  `gpg-secret-key.asc` (7589 B, the RPM signing secret key export), `gpg-passphrase.txt` (49 B),
  `pass.txt` (17 B), `ai_machine_pass.md` (9 B).
- Both team repos authenticate through a PAT embedded in `remote.origin.url`
  (`https://ghp_…@github.com/…`; value deliberately not recorded, AGENTS.md §4):
  `metalllinux/team-chaotix` and `metalllinux/cinnamon-for-rocky10`.
- `command -v gh` → absent (matches the 2026-10-18 record in the task doc `## Status`).
- `~/secrets` (the path AGENTS.md §4 names) does not exist; `~/AI/secrets` is the live house
  directory.

Operator direction (2026-11-08, task doc `## Status`): key material in `~/AI/secrets`, in place
before the next push to `metalllinux/cinnamon-for-rocky10`, no history re-signing (the 15
pre-existing unsigned commits stand).

## 2. Background

- The RPM signing key set the house pattern: rsa4096, uid
  `metallinux Cinnamon for Rocky Linux (repo signing) <repo-signing@metalinux.dev>`, primary
  fingerprint `2274BFE1BF28C051CD98675BEBD13108EB7FEF99` plus signing subkey
  `CD4958E1A421CBD6B56B7C5614CF2C0A8A47323C` (TASK-0036). Canonical keyring
  `~/.gnupg-cinnamon-rocky10/` (700); armored secret-key export plus passphrase copy in
  `~/AI/secrets/` (600); public key tracked in the cinnamon repo at
  `keys/cinnamon-rocky10-public.asc`. The old public key
  `1689676AF4D4F6FEC142B4429C0A8912FDA02785` is "also on GitHub" (TASK-0036 `## Implementation`:139) —
  GitHub already holds at least one GPG key for this account; the W2 read probes will show at
  which level.
- The 2026-10-18 token probe (TASK-0027 `## Security`:479) found `x-oauth-scopes: repo,workflow`
  on `GET /user` (login `metalllinux`): classic full `repo` scope. That probe predates the current
  `token.md` and is prior expectation only; the live re-probe is W2.
- Egress warning (TASK-0033 `## Release`:1392, 2026-10-18): five `POST` write probes to
  `api.github.com` all returned the fake `404 {"message": "Not Found", ...}` while `GET` worked
  and `PATCH /pulls/7` returned 200; the merge fell back to git. An API `POST /gpg_key` from
  this host may hit the same block; W2 pre-probes the write path with an invalid body (no key
  created) and classifies the response.
- TASK-0036 (2026-10-20): the host auto-backup covers `~/AI`. Operator-directed placement of the
  new secret key in `~/AI/secrets` therefore puts it into that backup. Recorded in the task doc
  `## Status`; not a question.

## 3. Options

### Option A: GPG, passphraseless ed25519, default `~/.gnupg` home (recommended)

- **How it works:** batch-generate an ed25519 signing-only key with `%no-protection` in the
  default `~/.gnupg` (700), uid `Team Chaotix (Commit Signing) <chaotix@metallinux.dev>`, no
  expiry. Armored exports `~/AI/secrets/gpg-commit-signing-secret.asc` and
  `gpg-commit-signing-public.asc` (600 in the 700 dir, house pattern). New `~/.gitconfig`:
  `commit.gpgsign=true`, `user.signingkey=<fingerprint>`, `user.name=Team Chaotix`,
  `user.email=chaotix@metallinux.dev` (`gpg.program` unset; git's default `gpg`).
- **Pros:** house toolchain — the RPM key already manages a gpg keyring under `~/AI/secrets/`
  (task doc `## Status`), so export, scratch-keyring verification (TASK-0036 pattern) and
  directory layout all reuse existing procedure. `commit.gpgsign` is git's long-standing
  default; no signing-format setting. Passphraseless is the only format where `git commit`
  signs non-interactively with zero daemon. The default home means any shell or future CI
  signs correctly without `GNUPGHOME` plumbing. Ed25519: small, fast, signing-only (no
  encryption subkey needed).
- **Cons:** passphraseless means file access (or auto-backup access) is signing authority. There
  is no at-rest protection beyond the 600/700 modes and the backup boundary.
- **Effort:** ~6 turns (W3–W6 in the plan).

### Option B: GPG, passphrase-protected, gpg-agent preset

- **How it works:** same key shape with a passphrase; passphrase file in `~/AI/secrets/` (house
  pattern, `gpg-passphrase.txt` sibling); `gpg-agent` with `allow-preset-passphrase`; the
  passphrase preset from the file after boot and before signing; git signs through the agent.
- **Pros:** at-rest protection of the keyring entry, same class as the RPM key.
- **Cons:** adds a daemon to every commit git makes: the agent must be running with the key
  preset, and a rebooted agent breaks signing until the preset runs again. Git has no
  passphrase channel of its own, so the agent is the only path. That failure surface sits on
  the critical path of every future team commit, for a key whose material is already in a 600
  file inside the auto-backup (operator-directed) — the protection a passphrase would add is
  already conceded at the backup boundary. The RPM key takes a passphrase because its scripted
  republish flow pins `--passphrase-file`; that constraint does not exist for git.
- **Effort:** Option A plus agent configuration, a reboot re-preset test, and a signing-path
  dependency: ~+3 turns.

### Option C: SSH commit signing

- **How it works:** an ed25519 SSH key held by `ssh-agent`; `commit.gpgsign=true` with the SSH
  signing format (git ≥ 2.32; the exact config spelling is unverified here, and the option is
  rejected on other grounds regardless); GitHub verifies the SSH signature.
- **Cons:** not the house toolchain (no SSH keyring precedent under `~/AI/secrets/`; the RPM
  flow is gpg). Needs `ssh-agent` running, the same agent-lifecycle problem as B with a
  different daemon. Zero SSH-signing precedent in any planning doc. Depends on the host git
  version supporting the format (unverified), while gpg 2.4.5 is confirmed.
- **Effort:** comparable to B. Rejected.

## 4. Recommendation

**Option A**: ed25519, passphraseless, default home, no expiry.

Reasoning. (1) The house tooling is GPG: reusing the RPM key's export and verification procedure
and directory is the cheapest correct path, and the operator's placement direction already
assumes it. (2) Passphraseless is the only format that makes `git commit` sign with no daemon.
The counterargument (at-rest protection) is neutralized by the operator-directed
`~/AI/secrets` placement, which puts the key material into the TASK-0036 auto-backup
regardless. (3) The default `~/.gnupg` home means no `GNUPGHOME` anywhere in the signing path.
The RPM key's dedicated home exists because its script pins `GNUPGHOME` explicitly; host-default
commit signing wants the default home.

Registration level, the secondary decision, resolved against the W2 probe:

- **Account level** (`POST /gpg_key`) if the probe allows it: one registration covers
  `metallinux/cinnamon-for-rocky10`, `metalllinux/team-chaotix` and every future metalllinux
  repo. Matches the DoD's "account-level on `metalllinux` if the token's scopes allow".
- **Repo level** (`POST /repos/{owner}/{repo}/gpg_key`) otherwise: on the named repo (the
  binding requirement) plus `team-chaotix` if that level also allows.
- **No writable level:** if the probe shows scope denial at every writable level, or the egress
  block signature (fake 404, TASK-0033), stop and record. The fallback is operator manual
  registration of the public key in the GitHub web UI (step-stop; the team passes the file
  path, never the value).
- What would change this: a W2 result showing the token can write keys at no level and no
  operator-manual path is wanted (then the task is blocked, not re-designed), or gpg 2.4.5
  refusing the ed25519 batch spec (fallback: rsa3072, same option, recorded in W3).

No-expiry consequence: rotation is a manual procedure — generate, register, switch
`user.signingkey`, delete the old registration. Recorded, not automated (deferred).

## 5. Risks and mitigations

| Risk | Likelihood | Impact | Mitigation | Contingency |
|---|---|---|---|---|
| Token N lacks public-key write scope | med | high | W2 live probe before key generation; no orphan key | Stop after recording; operator token/scope action via `## Status` |
| Egress blocks `POST` to `api.github.com` (TASK-0033 precedent) | med | high | W2 write-path pre-probe with invalid body (creates nothing); classify 422/404/403 | Operator manual web-UI registration (step-stop); record the level |
| Secret value leaks into a doc, log or command (AGENTS.md §4) | low | critical | Token bound to shell env from the file, never echoed; record fingerprint + short key ID only; remote URLs recorded redacted | Treat the key as leaked: regenerate from W3, re-run; never reuse the leaked value |
| Keyring confusion with the RPM key | low | med | Default home ≠ `~/.gnupg-cinnamon-rocky10`; W3 asserts the new fingerprint ≠ `2274BFE1…F99` and ≠ `1689676A…02785` | Stop on mismatch; delete the new key |
| Push of the verification branch fails (auth / protection) | low | med | `git push --dry-run` before the real push (W6) | Record; fix the token/remote issue first (may be the scope/egress class) |
| `state=valid` but `verified=false` (author email not on the account) | low | low | The proof commit keeps the repo-local author `87049949+metallinux@users.noreply.github.com` (the account noreply email) | Record the value; the DoD requires `state=valid` only |
| Auto-backup captures the secret key | certain | accepted (operator-directed) | Recorded in task doc `## Status`; Omega records the blast radius | None in scope |
| gpg 2.4.5 rejects the ed25519 batch spec | low | low | W3 round-trip test before anything else runs | rsa3072, same option, recorded in W3 |

## 6. Plan and validation

Sequenced steps, owners, estimates, dependencies, the critical path, the full validation list
and per-step rollback live in the task doc `## Plan` (single source of truth; this doc holds
the decisions).

### Success criteria

- `~/AI/secrets/` holds exactly two new files, both 600 in the 700 dir:
  `gpg-commit-signing-secret.asc`, `gpg-commit-signing-public.asc`.
- `gpg --list-secret-keys --with-fingerprint` shows the new ed25519 key, uid `Team Chaotix
  (Commit Signing) <chaotix@metallinux.dev>`, fingerprint distinct from both existing keys.
- `git config --global --list` shows `commit.gpgsign=true` and `user.signingkey=<fingerprint>`.
- `GET` at the achieved registration level lists the key with an ID matching the last 16 hex
  characters of the fingerprint.
- `GET /repos/metallinux/cinnamon-for-rocky10/commits/<sha>` for the pushed verification commit
  reports `verification.state == valid`.
- No secret value appears in any repo file, commit, planning doc or log (AGENTS.md §4).

### Rollback

Per-destructive-step rollback, detection, exact revert and point-of-no-return analysis: task
doc `## Plan`, Rollback. Short form: every step is reversible on the host (branch delete,
registration `DELETE`, `~/.gitconfig` delete, key plus files delete), in that reverse order.
The only capture the team cannot undo is the auto-backup of the key material, which is
operator-directed and recorded.
