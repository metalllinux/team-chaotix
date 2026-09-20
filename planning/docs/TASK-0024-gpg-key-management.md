# GPG signing key for the Cinnamon RPM repo: where it lives and how the sign step gets it

*Decision doc for TASK-0024 (planning/docs/TASK-0024-rpm-signing-gpgcheck.md). Six-pager per the
template, because this touches credentials, is expensive to reverse, and spans multiple components
(setup-repo.sh, INSTALL.md, the sign script, the release process).*

## 1. Problem

The public install path (metalllinux/cinnamon-for-rocky10, repo is Public, verified 2026-09-19 in
TASK-0016 `## Security`) ships 64 RPMs from a `file://` repo with `gpgcheck=0`
(`repo-setup/setup-repo.sh:119-128` writes the `.repo`; the manual block in
`INSTALL.md:177-189` matches). No signature is ever checked, and the documented sha256 step
(`INSTALL.md:93-99`) verifies the copy, not the origin. A compromised `metalllinux` account or a
bad merged in-account PR altering `rpms/` (in-account PRs merge without human review per
AGENTS.md §8) runs attacker code as root on a follower's machine. Source:
`planning/docs/TASK-0016-install-md-minimal-server.md:447-454` (Omega finding 3, low, supply-chain).

TASK-0024 closes that gap. The open design question this doc settles is the GPG key: where it is
generated, where the private half lives, and how the sign step obtains it, under two house rules
that appear to conflict:

- AGENTS.md §4 (AGENTS.md:111, rule at AGENTS.md:113): no credential, token, key, or password is
  ever written to a file, a commit, a log, a planning doc, or a GitHub Issue.
- AGENTS.md §13, Credential storage (AGENTS.md:296-297): "GitHub Secrets only. No local credential
  files, no Keychain, no pass store."

Read strictly, the private key may only live in GitHub Secrets. But signing happens on the build
host inside the local build loop (section 2), and local agents cannot read GitHub Secrets. The
strict reading therefore either forces a process change or makes the task infeasible. This doc
resolves the conflict explicitly, per the TASK-0024 brief and the Definition of Done line that
requires the key-management decision to be recorded in `## Plan`.

## 2. Background

- `rpms/` is built locally from `spec/` by the agent (rpmbuild on the host); there is no CI build.
  The project repo has no `.github/` directory (verified 2026-09-21, `glob .github/**` returned
  nothing). `spec/` is the canonical source; a clean-checkout rebuild reproduces the published set
  except build-environment artifacts (README.md:68-71, README.md:87-94, verified 2026-09-19).
- The team already holds host-local key material: the VM-fleet SSH key
  `~/.ssh/cinnamon-test-key` (vm-test/lib.sh:45) and the bare-metal key
  `~/.ssh/baremetal-103` (vm-test/lib.sh:85), both mode-600 local private-key files outside the
  repo. Strict "no local credential files" is therefore already not applied to operational
  host-local keys. The binding constraint in practice, and in the TASK-0024 DoD, is §4: no key
  material in the repo, commits, logs, or planning docs.
- The self-hosted GitHub Actions runner is extracted to `~/gh-runner/` on the same host
  (AGENTS.md §13, System configuration; `actions-runner.tar.gz` sits in the team-chaotix repo
  root). A "sign inside a workflow from a GitHub secret" design materializes the private key on
  the same disk.
- The repo has no tags (GitHub API `repos/metalllinux/cinnamon-for-rocky10/tags`, 2026-09-21: empty
  list). This will be the first signed release, tagged `v1.0.0`.
- The Release template checks "Commits: GPG-signed" (planning-doc template). Any git commit
  signing key the user has is a different key with a different scope. A dedicated keyring keeps
  the repo-signing key isolated from it.

## 3. Options

### Option A: host-local key, dedicated keyring

- **How it works:** generate one RSA 4096 key on the agent/build host (which is the libvirt host
  192.168.1.102 where the `rpms/` tree and the builds live; item 1 of `## Plan` confirms the host
  identity) inside a dedicated GNUPGHOME (`~/.gnupg-cinnamon-rocky10/`, mode 700), no passphrase,
  uid "Cinnamon for Rocky Linux 10 <repo-signing@metalinux.dev>" (domain to be confirmed by the
  user). The public key is exported to `keys/cinnamon-rocky10-public.asc` and committed. The
  private key stays in the dedicated keyring, mode 600, and never leaves the host. A committed
  script `repo-setup/sign-rpms.sh` reads the key from `GNUPGHOME` (env var, defaulting to the
  dedicated directory), asserts the expected fingerprint (the fingerprint is public data; it ships
  inside the public key), and runs `rpm --addsign` over `rpms/*.rpm`. Fingerprint and key path are
  documented in INSTALL.md and README.md.
- **Pros:** fits the existing build loop (agent builds and republishes `rpms/` locally, no
  round-trip). Zero new infrastructure. §4 is fully honored. Verification (`rpm --checksig`) works
  locally with the public key only. The key's protection model is the one the team already accepts
  for the fleet SSH key (lib.sh:45).
- **Cons:** it is a recorded exception to the strict reading of §13 (this doc is the record). A
  compromise of the `  howard` account on the build host can sign. The no-passphrase trade-off
  (below) means file mode 600 is the only barrier.
- **Effort:** one-time ~30 min key generation plus ~1 h for the sign script. No per-release cost.

Passphrase note: a passphrase-protected key would break unattended `rpm --addsign` unless the
passphrase is stored somewhere, which creates a second secret file and is strictly worse. The
accepted model is a no-passphrase key whose entire protection is host access control (mode 700
keyring, mode 600 key file, dedicated key, no key material in any doc or log). This is the same
model as the fleet SSH key, and it is the trade-off the user is asked to ratify.

### Option B: private key in a GitHub repo secret, sign inside a workflow

- **How it works:** store the armored private key as a GitHub repo secret. A new workflow
  (project repo) is dispatched by the agent with `gh` carrying the PR branch ref. The job on the
  self-hosted runner materializes the secret via `printenv VAR > file` (AGENTS.md §4 pattern),
  runs `rpm --addsign` over the 64 RPMs, regenerates `rpms/SHA256SUMS`, commits the result back to
  the PR branch, and deletes the key file.
- **Pros:** strict §13 compliance. The key file exists only transiently inside a workflow job.
  Signing is auditable as a workflow run.
- **Cons:** the runner runs on the same host as the same user, so the key materializes on the same
  disk as Option A; the security gain is thin. Every republish becomes a workflow round-trip the
  agent cannot verify locally. It requires adding a `.github/` to a repo that has none, a new
  secret, a new workflow, and a push-back mechanism (workflow committing to the agent's branch).
  It is a cross-task process change for a task whose purpose is the signature gap itself, and it
  removes ad-hoc signing (single-package rebuilds) from the agent's reach.
- **Effort:** 1-2 days including workflow and push-back plumbing, plus a standing per-release
  dependency on the runner being available.

### Option C: hybrid — Option A now, Option B as the named migration path

- **How it works:** Option A is adopted for this task. Option B is recorded as the migration path
  for when builds move off this host (e.g., a remote CI runner on a different machine) or when the
  user explicitly demands strict §13. Migration is a one-time human operation (export the private
  key into the secret store) documented in `## Release` when it happens.
- **Pros:** unblocks the task. The strict-§13 path stays available and the exception has a named
  exit condition instead of being "temporary forever".
- **Cons:** the exception remains on the record until the migration happens.
- **Effort:** Option A effort plus ~1 h of migration note.

## 4. Recommendation

Option A, with Option C's migration trigger recorded: if builds move off this host, or the user
explicitly wants strict §13, move the private key to a GitHub secret and adopt Option B's
workflow.

Why A wins: the threat model this task addresses (compromised account, bad merged PR altering
`rpms/`) is closed by the signature itself, which the attacker cannot forge without the private
key. Option B's only additional protection is keeping the key file permanently off the host, which
on a same-host self-hosted runner is not real protection, while the process cost is real. The team
already operates the fleet SSH key under exactly Option A's protection model (lib.sh:45, lib.sh:85).
What would change this decision: the user declining the §13 exception, or builds moving to a
machine where the key is not already present.

The exception, stated plainly for the record: AGENTS.md §13's "no local credential files" does not
bind this one key, by recorded decision with this rationale. AGENTS.md §4 binds in full: no
private key material in the repo, commits, logs, or planning docs (verified by `git grep` over the
merged tree per the DoD). Only public data is committed: the public key, the fingerprint, the key
id.

Key parameters (assumptions; the user confirms before item 1 runs, since generation is one-way):

| Parameter | Value | Note |
|---|---|---|
| Type | RSA 4096 | The rpm/dnf verify path on EL10 demonstrably handles RSA GPG signatures (the distro-standard path). Ed25519 gpg-signature support in the dnf verify path is not verified; do not introduce a key type the toolchain has not demonstrated the day the key becomes one-way. |
| Expiry | none | A repo key that expires mid-lifecycle strands every follower's `dnf` on an expiry event. Rotation is manual and deliberate (section 5). |
| Passphrase | none | See the passphrase note in Option A. |
| uid | Cinnamon for Rocky Linux 10 <repo-signing@metalinux.dev> | `metalinux.dev` is the user's domain; confirm before generation. The uid cannot be changed later. |

## 5. Risks and mitigations

| Risk | Likelihood | Impact | Mitigation | Contingency |
|---|---|---|---|---|
| Private key leaks (host compromise, `howard` account compromise) | low | critical. The attacker can forge future RPMs that pass signature verification on every machine that imports the key | mode 600 key file, mode 700 dedicated keyring, no key material in any doc or log, key isolated from the user's main GNUPGHOME | Re-key, re-sign the set, new tag, followers re-run `setup-repo.sh` (re-imports the new key), public notice. Machines that already installed cannot distinguish a genuine update from a forged one; accepted and recorded. |
| Private key lost (host disk death, keyring corruption) | low | high. No future package can be signed under this key. The key is not backed up by the team: a backup is a copy of the key, which §4 keeps out of the repo, so any backup is a human action in the user's own off-host storage, never an agent action | The user keeps an offline armored export in their own secure storage (ratified or declined at the key-parameter review) | Re-key path as above. Every machine that imported the old key must re-run `setup-repo.sh` from the new tag before it can install updates. |
| Signing key lands in the user's main keyring by mistake | low | medium. Hygiene breach, key sprawl | `sign-rpms.sh` uses an explicit GNUPGHOME; item 1 acceptance: the dedicated keyring holds exactly one secret key; the script refuses to run if the keyring holds more than one | Regenerate the key (cheap, pre-sign); remove the stray copy from the main keyring. |
| No-passphrase key misused in an interactive context (shell history, `set -x`) | low | medium | The script never places key material or passphrases on a command line; `set -euo pipefail`, no `set -x`; a no-passphrase key needs no prompt at all | Re-key. |
| uid email domain wrong or unowned | low | cosmetic | User confirms the uid before generation (human-look page) | The uid cannot be changed later; a new key is only needed if the uid becomes actively misleading. |

## 6. Plan and validation

Steps 1-4 of `## Plan` in the TASK-0024 doc execute this decision. Key acceptance:

- The dedicated keyring exists (mode 700) and holds exactly one RSA 4096 key;
  `keys/cinnamon-rocky10-public.asc` is in the working tree; the fingerprint is recorded in
  `## Plan` (public data).
- `git status` over the branch shows no private key material; Omega re-verifies with `git grep`
  over the branch commits (DoD).
- `rpm --checksig` over the signed set reports valid signatures for all 64 files (item 3 on the
  host, re-verified by Big on the fresh VM in item 10).

Success criteria: a follower's `dnf` with `gpgcheck=1` verifies every package by signature
(positive run), and a tampered package whose repodata was regenerated to match the tampered bytes
is refused with a signature error (negative run). That pair of results proves the key is in the
verification path, not merely present in the tree.

Rollback: the key cannot be un-generated. The pre-sign state (unsigned `rpms/`, `gpgcheck=0`) is
restored by reverting the PR before merge. After merge plus tag, the two points of no return
(repo state, key state) are defined in `## Plan`, Rollback.
