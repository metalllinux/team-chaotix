# TASK-0024 — Sign the Cinnamon RPMs, enable gpgcheck, publish the release manifest

> **Section order below is fixed.** Each agent writes to its own section and no other. `Robotnik`
> reads only `## Status` and `## Next Actions`. Do not reorder, rename, or remove sections.

- **Created:** 2026-09-19

---

## Status

*Owner: `Robotnik`. Keep this SHORT and CURRENT — it is one of only two sections the PM reads, so a
stale entry means the whole loop runs on bad information.*

**Now (2026-09-21, user decision): key parameters ratified WITH A MODIFICATION — the signing key
is passphrase-protected.** The user approved Amy's 6-pager storage design (dedicated host-local
keyring, RSA 4096, the recorded §13 exception) but rejected the no-passphrase choice; the key is
passphrase-protected. Consequences recorded here so the plan and implementation do not drift: the
sign step must supply the passphrase without it ever entering the repo, commits, logs, or planning
docs (AGENTS.md §4) — Amy's plan D1 must be adjusted to name the mechanism (e.g.
`gpg --batch` with `gpg-preset-passphrase`, or a 600-mode passphrase file host-side, her call with
a stated reason); the §13 exception now covers key + passphrase, both host-side; key loss/leak is
still one-way (re-key, re-sign, new tag) and the passphrase does not change that. `## Plan` D1 and
item 1 carry the adjustment before Tails generates anything.

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
- ~~Where the GPG signing key lives and how it is managed~~ — **resolved 2026-09-21**: host-local
  dedicated keyring, passphrase-protected (user decision), public key + fingerprint ship in the
  repo, private key + passphrase never leave the host (AGENTS.md §4 intact, §13 exception recorded
  in the 6-pager). Sign-step passphrase mechanism: `## Plan` D1 (Amy's adjustment pending).
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

- [x] User ratified the key parameters (2026-09-21): host-local dedicated keyring, RSA 4096,
      recorded §13 exception — **with the modification that the key is passphrase-protected** (the
      no-passphrase choice was rejected). Recorded in `## Status`.
- [ ] `Amy`: adjust `## Plan` D1 + item 1 to the passphrase-protected key — name the sign-step
      passphrase mechanism (how the passphrase is supplied without ever entering the repo,
      commits, logs, or this doc; where it lives host-side), and the key-generation command now
      takes a passphrase.
- [ ] `Robotnik`: dispatch item 1 (key generation) to `Tails`, then the `## Plan` sequence
      (14 items, critical path 1 → 3 → 4 → 5 → 7 → 8 → 9 → 10 → 11 → 14).

---

## Plan

*Owner: `Amy`.*

**Why this task exists.** Closes Omega's supply-chain finding from TASK-0016
(`planning/docs/TASK-0016-install-md-minimal-server.md:447-454`): the documented install path of
a public repo ships 64 RPMs from a `file://` repo with `gpgcheck=0`
(`repo-setup/setup-repo.sh:119-128`), no signature is ever checked, and the sha256 step
(`INSTALL.md:93-99`) verifies the copy, not the origin. A compromised `metalllinux` account or a
bad merged in-account PR altering `rpms/` (in-account PRs merge without human review per
AGENTS.md §8) runs attacker code as root on a follower's machine. This task signs the set, ships
the public key, turns on `gpgcheck=1`, and publishes a release manifest pinned by a git tag.

**What it unblocks / what blocks it.** Unblocks: the first trusted, tagged public release of the
project (the README already claims "Ready for the release PR", README.md:12), and every future
republish, which then carries signature verification as a standing property. Blocks: nothing
external. The one human dependency is confirmation of the key parameters before generation (uid,
no-passphrase trade-off, the §13 exception) — item 1 is gated on that look. All work is inside
`metalllinux/cinnamon-for-rocky10` (PR merge plus tag, no human gate per AGENTS.md §8) plus the VM
host `192.168.1.102` for verification. **Assumption (item 1 confirms in writing):** the agent host
is the libvirt host `192.168.1.102` — the harness calls `virsh` locally
(vm-test/lib.sh:36, vm-test/provision-vm.sh:50-54) and the DoD pins the verification VM to that
host.

**MVP.** Sign the existing 64 RPMs in place, ship the public key, `gpgcheck=1` in
`setup-repo.sh` and the docs, manifest plus tag, fresh-VM verification plus the negative test.
That is the whole DoD; there is no smaller slice that closes the gap. Deferred, named and not
silent: (a) a deterministic CI workflow re-running `rpm --checksig` and `sha256sum -c` on push to
the project repo — the project repo has no `.github/` today (verified 2026-09-21); adding one is
a separate task; (b) an offline backup of the private key — a human action in the user's own
storage, never an agent action (6-pager section 5); (c) a full key-rotation runbook beyond the
re-key contingency recorded in the 6-pager.

**What this makes harder later.** (1) Every future republish must re-sign and regenerate the
manifest; the unsigned-republish habit is dead by design. (2) Re-keying is a stranding event:
machines that imported the old key fail to install updates until they re-run
`setup-repo.sh` from the new tag (6-pager section 5). (3) The documented fallback path
(`dnf install ./rpms/*.rpm`, `INSTALL.md:200-214`) is recorded as unverified-by-signature until
item 11c proves otherwise; the repo path is canonical. (4) The tag pins the manifest; every new
set gets a new tag, because republishing at the same tag is not a thing we do.

**Key decisions.** Full record for the credential decision:
`planning/docs/TASK-0024-gpg-key-management.md` (6-pager).

- **D1, key storage.** Host-local private key in a dedicated keyring
  (`~/.gnupg-cinnamon-rocky10/`, mode 700), generated once on the agent host, RSA 4096, no
  expiry, no passphrase, uid "Cinnamon for Rocky Linux 10 <repo-signing@metalinux.dev>" (domain
  to confirm). Public key committed at `keys/cinnamon-rocky10-public.asc`; the fingerprint (public
  data, ships inside the public key) is committed in `sign-rpms.sh` and the docs. The sign step
  obtains the key via `GNUPGHOME` (env var, defaulting to the dedicated directory) and asserts
  the expected fingerprint before signing. This is a **recorded exception to the strict reading of
  AGENTS.md §13** ("GitHub Secrets only", AGENTS.md:296-297), justified by: the build loop is
  local (the project repo has no CI), the self-hosted runner runs on the same host so
  secret-store signing buys nothing, agents cannot read GitHub Secrets, and the team already runs
  the fleet SSH key under the same model (vm-test/lib.sh:45, vm-test/lib.sh:85). AGENTS.md §4
  (AGENTS.md:113) is honored in full: no private key material in repo, commits, logs, or planning
  docs.
- **D2, sign in place, not rebuild.** `rpm --addsign` over the existing 64 files. A rebuild from
  `spec/` reproduces the set only modulo build-environment artifacts (README.md:87-94: LTO
  build-ids, pip direct_url paths), which would invalidate the 2026-09-19 end-to-end evidence and
  force a mozjs115 rebuild (full Mozilla ESR source build) for no functional gain. `--addsign`
  touches only the signature header; item 3 proves payload identity by per-RPM payload-digest
  comparison before and after signing. **Flip condition:** if a payload digest does not match,
  rebuild that package from `spec/` (canonical, README.md:68-71), sign it, and record the flip in
  `## Implementation`.
- **D3, key import mechanism.** `setup-repo.sh` runs `rpm --import` on
  `keys/cinnamon-rocky10-public.asc` and writes the `.repo` with `gpgcheck=1` and **no** `gpgkey=`
  line; dnf verifies against the imported rpm keyring, the same model as the EL base repos. No
  `gpgkey=` because a `file://` gpgkey pointing into the clone breaks when a follower moves the
  clone, while the imported key is path-independent. The fresh-VM positive run plus the negative
  refusal (items 10-11) prove the check is live, so the design is self-verifying.
- **D4, manifest and tag.** `rpms/SHA256SUMS` (sha256sum format, basenames, sorted, generated
  from the signed bytes) committed next to the RPMs; the documented check is
  `cd rpms && sha256sum -c SHA256SUMS`. The first signed release is tagged **`v1.0.0`** (annotated
  tag on the merge commit, pushed; the repo has no tags today, verified 2026-09-21). The tag is
  the pin: INSTALL.md tells followers to clone at the tag. Division of labor, stated in the docs:
  the sha256 manifest catches transfer corruption and drift from the trusted baseline; the
  signature catches origin tampering, because an attacker without the private key cannot re-sign.
  That is what Omega asked for — "verify against a trusted baseline instead of against the tree
  they just cloned" (TASK-0016 doc :453). `createrepo_c` only ingests RPM files, so
  `SHA256SUMS` in `rpms/` is inert for metadata (assumption, cheaply falsified by item 10's
  `dnf makecache`).

**Work breakdown** — decomposed until one agent finishes one item in one turn.

| # | Item | Owner agent | Acceptance criterion | Parallel with |
|---|---|---|---|---|
| 1 | Generate the signing key in the dedicated keyring; export the public key to `keys/cinnamon-rocky10-public.asc`; record the fingerprint in this section | Tails | Dedicated GNUPGHOME (mode 700) holds exactly one RSA 4096 key, no passphrase; public key file in the working tree; fingerprint recorded below (public data); `git status` shows no private key material; host-identity assumption confirmed in writing (hostname/IP of the agent host) | Independent of 2 |
| 2 | Write `repo-setup/sign-rpms.sh`: GNUPGHOME-scoped, asserts the expected fingerprint, signs unsigned RPMs in place, verifies the full set with `rpm --checksig`, idempotent, fails loud naming the offending file | Tails | `bash -n` clean; run against a scratch keyring without the key exits non-zero with a fingerprint error; run against the current unsigned set reports all 64 as unsigned | Independent of 1; both required before 3 |
| 3 | Sign all 64 in place; capture payload-identity evidence | Tails | `rpm --checksig` over all 64 (public key imported into the verifying user's rpm keyring first) reports only valid signatures; per-RPM payload digests (`rpm2cpio`) identical before/after signing, recorded in `## Implementation`; `git diff --stat` shows only `rpms/*.rpm` changed | After 1 and 2 |
| 4 | Generate and commit `rpms/SHA256SUMS` from the signed set | Tails | `cd rpms && sha256sum -c SHA256SUMS` passes 64/64; file is sorted, basenames only | After 3 |
| 5 | `setup-repo.sh`: import the key (`rpm --import`, then assert the key is in the rpm keyring via `rpm -q gpg-pubkey-<keyid>`, exact keyid width determined at implementation), write the `.repo` with `gpgcheck=1`; update the reference file `repo-setup/cinnamon-rocky10.repo:11`; preserve the statelessness contract (setup-repo.sh:19-26) — the import is state-changing and stays after project-root resolution (setup-repo.sh:51-58) | Tails | `bash -n` clean; the bad-argument error path is unchanged (exits before the root check, no host state changed, so the `vm-test/test-repo-setup.sh` assertion still holds by inspection); the written `.repo` block contains `gpgcheck=1` | Independent of 6 |
| 6 | Docs: Quick start (script imports the public key, dnf verifies signatures), Manual section (key-import step plus `gpgcheck=1`, INSTALL.md:177-189), new "Verifying the release" section (clone at tag, `sha256sum -c`, `rpm --checksig`), README.md signing section (key path, fingerprint, how to check it). House style per AGENTS.md §10 | Tails | All four surfaces updated; `gpgcheck=0` appears in the docs only when describing the old behavior | Independent of 5 |
| 7 | Push the branch, open the PR to `main` | Tails | PR exists with a description that lists the DoD; `metalllinux`-internal, no human gate (AGENTS.md §8) | After 4, 5, 6 |
| 8 | Review | Shadow | No unresolved blocker or should-fix in `## Review`; specifically checks the statelessness-contract change and the sign script's error paths | After 7 |
| 9 | Security review | Omega | No findings above `low` in `## Security`; verifies no key material in the branch commits (`git grep`), that the committed fingerprint is public data, and that the §13 exception is recorded (this section plus the 6-pager) | After 8 (fixed order Shadow → Omega → Big, AGENTS.md §3) |
| 10 | Fresh minimal Rocky 10.2 VM on `192.168.1.102`, documented procedure with `gpgcheck=1`: 22 names installed, GDM Wayland login, five surfaces | Big | The DoD fresh-VM box: the install command from the docs succeeds under a `.repo` with `gpgcheck=1` (evidence: the installed `.repo` file, the imported-key query, dnf history); `loginctl` session `Type=wayland`; 5/5 surfaces with the existing harness (same evidence shape as TASK-0016, `vm-test/evidence/task0016-minimal/2026-09-19/`); evidence lands in `vm-test/evidence/task0024-gpg/` | After 9; independent of 11 (second VM) |
| 11 | Negative test: (a) tamper one RPM's payload, then re-run `createrepo_c` on the tampered set so repodata matches the tampered bytes and only the signature can catch it; `dnf install` under `gpgcheck=1` must fail with a signature error, exact wording recorded. (b) The same tampered package under `gpgcheck=0` (fresh VM, or before the desktop is installed) must install; record that as what the old path silently accepted. (c) Characterize the fallback path: `dnf install ./rpms/<tampered>.rpm` with the key imported | Big | (a) The refusal is a signature/fingerprint error, not a checksum error (assert on the wording); (b) the tampered package installs, recorded; (c) the behavior is recorded either way, and item 6's wording is corrected by Tails in item 12 if needed | Ordered after 10 (shares the provisioning pattern); independent of 10 |
| 12 | Fixes from items 8-11 | Tails | Each finding closed in `## Review` / `## Security` with the fixing sha | As needed |
| 13 | Docs verification | Vector | `## Docs` records every user-facing change; house style checked | After 12 (or after 11 when there are no fixes) |
| 14 | Merge the PR to `main`; create and push annotated tag `v1.0.0` on the merge commit; fresh clone at the tag: `sha256sum -c` plus `rpm --checksig` over all 64 | Knuckles | Tag exists on GitHub pointing at the merge commit; clone-at-tag checks pass 64/64; `## Release` filled | After 13 |

**Fingerprint (recorded by Tails in item 1; public data):** _pending_

**Dependencies and sequence.** Genuinely ordered: 1+2 → 3 → 4 (sign before manifest, because the
manifest hashes the signed bytes); 5, 6 → 7 (the PR carries the script and the docs); 7 → 8 → 9
(review chain, fixed internal order per AGENTS.md §3); 9 → 10 → 11 (tests run on reviewed code);
13 → 14 (release last). **Explicitly independent:** 1 from 2; 5 from 6; 10 from 11 (separate
VMs, separate evidence). The single inference slot runs everything one at a time anyway
(AGENTS.md §3), so the ordering above is the critical path, not a parallelism plan.

**Critical path:** 1 → 3 → 4 → 5 → 7 → 8 → 9 → 10 → 11 → 14, with 2 joining at 3, 6 at 7, 12/13
between 11 and 14 as needed. Longest dependent chain: key → sign → manifest → PR → review →
fresh-VM run → negative test → release.

**Estimates.** Three-point, hours, `T = (O + 4M + P) / 6`.

| Item | O | M | P | T |
|---|---|---|---|---|
| 1 Key | 0.25 | 0.5 | 1 | 0.5 |
| 2 Sign script | 0.5 | 1 | 2 | 1.2 |
| 3 Sign 64 + evidence | 0.5 | 1 | 2 | 1.2 |
| 4 Manifest | 0.25 | 0.5 | 1 | 0.5 |
| 5 setup-repo.sh | 0.5 | 1 | 2 | 1.2 |
| 6 Docs | 1 | 2 | 4 | 2.2 |
| 7 PR | 0.25 | 0.5 | 1 | 0.5 |
| 8 Shadow | 0.5 | 1 | 2 | 1.2 |
| 9 Omega | 0.5 | 1 | 2 | 1.2 |
| 10 Fresh VM | 2 | 4 | 8 | 4.3 |
| 11 Negative test | 1 | 2 | 4 | 2.2 |
| 12 Fixes (expected small) | 0 | 0.5 | 2 | 0.8 |
| 13 Vector | 0.25 | 0.5 | 1 | 0.5 |
| 14 Release | 0.5 | 1 | 2 | 1.2 |
| **Total** | | | | **~18.7** |

Buffer: +6 h (~30%), sized to where the uncertainty concentrates: the fresh-VM run (GDM/Wayland
flake history, TASK-0008), gpg/rpm tooling edges (keyring scoping, `--addsign` behavior), and the
unverified dnf local-file signature behavior (item 11c). **Total ≈ 25 h ≈ 3 working days** on the
single slot.

**Risks.**

| Risk | Likelihood | Impact | Mitigation | Contingency |
|---|---|---|---|---|
| `--addsign` changes more than the header (payload identity breaks) | low | high. Invalidates the 2026-09-19 evidence; D2 flips | Per-RPM payload-digest comparison before/after signing (item 3) | Rebuild the affected packages from `spec/`, sign them, record the flip in `## Implementation` |
| One RPM resists signing (corrupt archive) | low | medium | The script fails loud and names the file | Rebuild that one package from `spec/` (canonical, README.md:68-71) and sign it |
| Negative test catches the tamper via checksum instead of signature (repodata trap) | medium | medium. Proves the wrong thing | Re-run `createrepo_c` on the tampered set before the test (item 11 design); assert on the error wording | Re-run with regenerated repodata; the signature-error assertion is the acceptance criterion |
| dnf fallback path (local file install) skips signature verification | medium | low. Docs only | Characterize in item 11c | INSTALL.md marks the fallback unverified-by-signature; the repo path is canonical |
| Fresh-VM desktop flake (GDM auth history) | medium | medium. Schedule | The harness is proven (TASK-0016, 2026-09-19); re-provision on flake | Record the flake, re-run; do not weaken the check |
| Private key lands in the user's main keyring | low | medium. Hygiene | Dedicated GNUPGHOME; the script refuses a keyring holding more than one secret key (6-pager section 5) | Regenerate pre-sign; remove the stray copy |
| Key lost or leaked after release | low | critical (6-pager section 5) | Mode 600/700, no key material in any doc, dedicated keyring | Re-key, re-sign, new tag, re-import; the stranding window is documented in Rollback below |

**Validation.**
- **Host (agent host):** `rpm --checksig` over all 64 (item 3); `cd rpms && sha256sum -c
  SHA256SUMS` (item 4); `bash -n` on both scripts; `git grep` for key material over the branch
  (Omega, item 9).
- **Fresh minimal Rocky 10.2 VM on `192.168.1.102` (items 10-11):** documented procedure with
  `gpgcheck=1` → 22 names installed with signatures verified by dnf, GDM Wayland login, 5/5
  surfaces, `loginctl` `Type=wayland`. Tampered RPM with regenerated repodata → refused with a
  signature error (exact wording recorded). Same tampered RPM under `gpgcheck=0` → installs
  (recorded as what the old path silently accepted). Fallback-path behavior characterized.
- **Clone at tag (item 14):** `sha256sum -c` plus `rpm --checksig` on a fresh clone of `v1.0.0`
  pass 64/64. This is the check that pins the tag.
- **Pages needing a human look, named:** (1) the 6-pager key parameters — uid/domain, the
  no-passphrase trade-off, and the §13 exception itself — the user ratifies before item 1 runs;
  (2) the tag name `v1.0.0`; (3) the public `INSTALL.md`/`README.md` wording before merge (the
  repo is Public); (4) the item 11b evidence, confirming the old-path-accepts-tampered-RPM risk
  claim with the actual dnf output.

**Rollback.**
- **Detection:** pre-merge — a review finding or a failed VM test; do not merge, nothing has been
  deployed. Post-merge — a follower reports a dnf signature error; verify with a fresh clone
  (`sha256sum -c` plus `rpm --checksig`). Suspected key compromise — re-key (6-pager section 5).
- **Exact revert (pre-merge, fully reversible):** `git revert` of the merge commit (public repo:
  revert, never force-push); delete the tag if it was pushed
  (`git push origin :refs/tags/v1.0.0`). No follower machine that installed nothing is affected.
- **Point of no return — two distinct lines.**
  1. **Repo state:** the merge to `main` plus the pushed tag. After this, a follower who
     installed the signed set has packages signed by our key on the machine. Reverting the repo
     to the unsigned/`gpgcheck=0` state does not touch installed machines and re-opens the exact
     gap this task closes — so after a successful release, "rollback" is not a revert; it is a
     forward fix (a new signed release at a new tag).
  2. **The key (the real line):** the moment the private key is lost or leaked is one-way. Loss:
     no future package can be signed under it; the remedy is re-key plus re-sign plus a new tag,
     and every machine that imported the old key must re-run `setup-repo.sh` from the new tag
     before it can install updates — a machine mid-migration (repo configured, install half done)
     is stranded in that window. Leak: assume every future package is forgeable; already-installed
     machines cannot distinguish a genuine update from a forged one; the remedy is re-key plus a
     public notice. This is the standing cost of D1's no-passphrase choice, recorded.
- **State a failed run leaves behind, and what a retry must tolerate:** a partially signed
  `rpms/` (the sign script is idempotent and resumable; item 3 re-runs cleanly); a VM with a
  `gpgcheck=1` `.repo` but no imported key (interrupted `setup-repo.sh` — re-run it, it is
  idempotent); a running VM left behind (destroy after evidence capture, the harness `--destroy`
  pattern, vm-test/provision-vm.sh:5-8); a regenerated `rpms/repodata/` on a follower's machine
  (untracked, gitignored at .gitignore:13, always regenerable).

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
