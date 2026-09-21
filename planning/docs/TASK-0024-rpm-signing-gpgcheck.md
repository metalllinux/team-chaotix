# TASK-0024 — Sign the Cinnamon RPMs, enable gpgcheck, publish the release manifest

> **Section order below is fixed.** Each agent writes to its own section and no other. `Robotnik`
> reads only `## Status` and `## Next Actions`. Do not reorder, rename, or remove sections.

- **Created:** 2026-09-19

---

## Status

*Owner: `Robotnik`. Keep this SHORT and CURRENT — it is one of only two sections the PM reads, so a
stale entry means the whole loop runs on bad information.*

**Now (2026-09-21, user decision, item 1 execution): passphrase and uid settled.** The user
specified the key passphrase by reference: the contents of `~/password.txt` (17 bytes, was 644).
Uid decided: `metallinux Cinnamon for Rocky Linux (repo signing) <repo-signing@metalinux.dev>`.
Item 1 execution change (ratification substance intact): the agent places the passphrase into the
sibling 700/600 location by pure file operations (contents never read or displayed by any agent),
runs the key generation non-interactively with `--pinentry-mode loopback --passphrase-file`, and
writes the passphrase nowhere new; the user approved deleting the 644 source file after the copy.
The passphrase never enters a transcript, commit, log, or doc (AGENTS.md section 4).

**Now (2026-09-21): plan complete and ratified; implementation starting.** Amy's 14-item plan is
written and adjusted to the user-ratified passphrase-protected key; the 6-pager carries the
ratified design as the current recommendation. Dispatching `Tails` for the implementation
sequence. Note: item 1 (key generation) is user-supervised — the passphrase is entered by the
user at generation and written to the 600-mode file by the user; no agent ever writes it.

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
      project (documented path); no private key material appears anywhere in the public repo, any
      commit, any log, or any planning doc: the keyring and passphrase live in `$HOME`, outside
      the repo tree; the final merged tree passes `git grep` for `BEGIN PGP PRIVATE KEY BLOCK` and
      `private-keys-v1.d` with zero hits; a `.gitignore` on the branch covers key-material paths;
      the key-management decision is recorded in `## Plan`. (User instruction 2026-09-21: key
      material must never reach the public GitHub repository.)
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
- [x] `Amy` (2026-09-21): `## Plan` D1 + items 1-2 adjusted to the passphrase-protected key —
      sign-step mechanism is gpg-agent preset via `gpg-connect-agent` on stdin (rejected:
      `gpg-preset-passphrase` argv exposure, direct-gpg flags unreachable from `rpm --addsign`);
      passphrase lives in a sibling 700-mode location, never written by any agent; D2/D3/D4
      unchanged; estimates +0.4 h.
- [x] `Amy` (2026-09-21): 6-pager `planning/docs/TASK-0024-gpg-key-management.md` updated to the
      ratified design — Option A rewritten, superseded no-passphrase recommendation preserved as a
      dated block with the user's rejection attached, §3.1 mechanism section added, standing cost
      and risks updated.
- [x] `Tails` (2026-09-21): item 1 executed — passphrase-protected RSA 4096 key
      `1689676AF4D4F6FEC142B4429C0A8912FDA02785` in `~/.gnupg-cinnamon-rocky10` (protection
      proven by signing), sibling passphrase location 700/600, public key + fingerprint +
      key-material `.gitignore` guard committed as project-repo `7d47a02` and pushed;
      `~/password.txt` deleted (user-approved); pre-push grep clean (only hit: the
      `.gitignore` line itself). Execution record in `## Implementation`.
- [x] `Tails` (2026-09-21): item 3 executed — all 64 RPMs signed in place with
      `1689676AF4D4F6FEC142B4429C0A8912FDA02785`; payload identity proven (per-RPM
      `rpm2cpio | sha256sum` digests identical before/after, 64/64, no D2 flip);
      `rpm --checksig` 64/64 `digests signatures OK`; runtime no-leak proven (ps/environ
      samples, run log, shell history all clean); project-repo `db60bb6` on
      `feature/TASK-0024-rpm-signing-gpgcheck` pushed, pre-push grep zero hits. Execution
      record in `## Implementation`.
- [ ] `Robotnik`: dispatch item 4 (generate and commit `rpms/SHA256SUMS` from the signed set)
      to `Tails` — critical path continues 4 → 5 → 7 → 8 → 9 → 10 → 11 → 14 (item 6 joins at
      7).

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
external. The key parameters (uid, passphrase-protected key, §13 exception) were ratified
2026-09-21 with the passphrase modification; the remaining human dependency is the user supplying
the passphrase at key generation (item 1), which gates the sign chain. All work is inside
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
  expiry, **passphrase-protected** (user decision 2026-09-21; the no-passphrase choice was
  rejected), uid "Cinnamon for Rocky Linux 10 <repo-signing@metalinux.dev>" (domain to confirm).
  **Key generation (item 1) is interactive and user-supervised:** `gpg --full-generate-key` under
  the dedicated `GNUPGHOME`; the user selects RSA 4096, no expiry, the uid, and enters the
  passphrase at the pinentry prompt. The generation batch file must not contain `%no-protection`
  (which forces a key without passphrase) and never contains the passphrase. The passphrase is
  chosen by the user at generation time and written by the user to a **sibling 700-mode
  location** (`~/.gnupg-cinnamon-rocky10.passphrase/`, directory mode 700, file `passphrase` mode
  600); no agent writes, reads, or records the passphrase, and it appears in no command, batch
  file, log, or doc. Sibling, not co-located in the keyring, deliberately: one 700 directory
  holding both key and passphrase makes them a single protection target, which defeats the point
  of passphrase protection; the sibling keeps them separate at the cost of a second path in backup
  and re-key, recorded here and in the Rollback re-key contingency. Both locations live in
  `$HOME`, outside the project repo tree (`~/Linux/projects/cinnamon-for-rocky10/`), so neither
  can be committed even by accident. Public key committed at
  `keys/cinnamon-rocky10-public.asc`; the fingerprint (public data, ships inside the public key)
  is committed in `sign-rpms.sh` and the docs.
  **Passphrase mechanism at sign time (chosen: gpg-agent preset).** The sign step is
  `rpm --addsign` (D2), which invokes gpg internally; handing that internal gpg a
  `--passphrase-file` would mean overriding rpm's internal signing command (a version-fragile
  macro), so the passphrase is instead **preset into the gpg-agent** before the sign run: the
  sign script reads the 600-mode file and feeds it to `gpg-connect-agent`'s `/PRESET_PASSPHRASE`
  (for the key's keygrip) **on stdin, never argv** (heredoc input, so also invisible to `set -x`
  traces; the script additionally runs without `set -x`), `rpm --addsign` then finds the
  passphrase cached in the agent and signs without a pinentry prompt, and the script clears the
  preset from the agent after the run. Chosen over `gpg --sign --passphrase-file` to a direct gpg
  call because a detached gpg signature is not a valid RPM signature (rpm's header signature
  format requires `rpm --addsign`/`rpmsign`), and over `gpg-preset-passphrase --preset PASSWD=...`
  because that form puts the passphrase in the process arguments. Tails pins the exact preset
  command (keygrip derivation, mode flags) against the host's gpg version in item 2 and proves in
  item 3 that the sign run leaves the passphrase out of `ps`, shell history, and logs. The sign
  step obtains the key via `GNUPGHOME` (env var, defaulting to the dedicated directory) and
  asserts the expected fingerprint before signing. This is a **recorded exception to the strict
  reading of AGENTS.md §13** ("GitHub Secrets only", AGENTS.md:296-297), now covering key and
  passphrase, both host-side, justified by: the build loop is local (the project repo has no CI),
  the self-hosted runner runs on the same host so secret-store signing buys nothing, agents cannot
  read GitHub Secrets, and the team already runs the fleet SSH key under the same model
  (vm-test/lib.sh:45, vm-test/lib.sh:85). AGENTS.md §4 (AGENTS.md:113) is honored in full: no
  private key material and no passphrase in repo, commits, logs, or planning docs.
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
| 1 | Generate the passphrase-protected signing key in the dedicated keyring (interactive `gpg --full-generate-key`; the passphrase is chosen by the user at generation time, entered at the pinentry prompt, and written by the user to the sibling 600-mode file — never written by any agent); export the public key to `keys/cinnamon-rocky10-public.asc`; record the fingerprint in this section | Tails (passphrase entry and file write are user actions) | Dedicated GNUPGHOME (mode 700) holds exactly one passphrase-protected RSA 4096 key; the sibling passphrase location exists (dir 700, file 600), verified by existence and mode only, content never read; public key file in the working tree; fingerprint recorded below (public data); `git status` shows no private key material and no passphrase; host-identity assumption confirmed in writing (hostname/IP of the agent host). Acceptance is the fingerprint recorded plus the public key exported, never the passphrase | Independent of 2 |
| 2 | Write `repo-setup/sign-rpms.sh`: GNUPGHOME-scoped, asserts the expected fingerprint, presets the passphrase from the 600-mode sibling file into the gpg-agent via `gpg-connect-agent` on stdin (never argv; no `set -x`), signs unsigned RPMs in place with `rpm --addsign`, clears the preset from the agent, verifies the full set with `rpm --checksig`, idempotent, fails loud naming the offending file | Tails | `bash -n` clean; run against a scratch keyring without the key exits non-zero with a fingerprint error; run against the current unsigned set reports all 64 as unsigned; the exact preset command (keygrip derivation, mode flags) is pinned against the host's gpg version and recorded in `## Implementation`; by inspection the passphrase is only read from the 600-mode file and passed on stdin, never argv (runtime proof in item 3) | Independent of 1; both required before 3 |
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
| 2 Sign script (incl. passphrase preset) | 0.75 | 1.5 | 3 | 1.6 |
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
| **Total** | | | | **~19.1** |

Buffer: +6 h (~30%), sized to where the uncertainty concentrates: the fresh-VM run (GDM/Wayland
flake history, TASK-0008), gpg/rpm tooling edges (keyring scoping, `--addsign` behavior, the
agent-preset passphrase mechanism in item 2), and the unverified dnf local-file signature
behavior (item 11c). **Total ≈ 25 h ≈ 3 working days** on the single slot.

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
  (Omega, item 9); the item 3 sign run leaves the passphrase out of `ps` output, shell history,
  and logs (AGENTS.md §4 — preset to the agent via stdin, never argv).
- **Fresh minimal Rocky 10.2 VM on `192.168.1.102` (items 10-11):** documented procedure with
  `gpgcheck=1` → 22 names installed with signatures verified by dnf, GDM Wayland login, 5/5
  surfaces, `loginctl` `Type=wayland`. Tampered RPM with regenerated repodata → refused with a
  signature error (exact wording recorded). Same tampered RPM under `gpgcheck=0` → installs
  (recorded as what the old path silently accepted). Fallback-path behavior characterized.
- **Clone at tag (item 14):** `sha256sum -c` plus `rpm --checksig` on a fresh clone of `v1.0.0`
  pass 64/64. This is the check that pins the tag.
- **Pages needing a human look, named:** (1) the 6-pager key parameters — uid/domain, the
  passphrase-protected key and the sibling passphrase location, and the §13 exception itself —
  ratified by the user 2026-09-21 with the passphrase modification, before item 1 runs;
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
      is stranded in that window. Leak: if both the private key and the passphrase are exposed,
      assume every future package is forgeable; already-installed machines cannot distinguish a
      genuine update from a forged one; the remedy is re-key plus a public notice. If only the key
      file leaks (the passphrase stays in the sibling 600-mode file), the key is not immediately
      usable, but treat it as compromised and re-key. Loss of the key or of the passphrase is
      one-way (a re-key event): a passphrase-protected key cannot be recovered from the key file
      alone, and the offline backup must carry both. This is the standing cost of D1, recorded.
- **State a failed run leaves behind, and what a retry must tolerate:** a partially signed
  `rpms/` (the sign script is idempotent and resumable; item 3 re-runs cleanly); a VM with a
  `gpgcheck=1` `.repo` but no imported key (interrupted `setup-repo.sh` — re-run it, it is
  idempotent); a running VM left behind (destroy after evidence capture, the harness `--destroy`
  pattern, vm-test/provision-vm.sh:5-8); a regenerated `rpms/repodata/` on a follower's machine
  (untracked, gitignored at .gitignore:13, always regenerable).

---

## Implementation

*Owner: `Tails`. Item 1 complete 2026-09-21 (key `1689676AF4D4F6FEC142B4429C0A8912FDA02785`; public key, fingerprint, and key-material `.gitignore` guard committed as project-repo `7d47a02`); item 2 complete 2026-09-21 (`repo-setup/sign-rpms.sh`, project-repo `b84ce3f`). Branch `feature/TASK-0024-rpm-signing-gpgcheck` pushed; no key material in the branch (pre-push grep in the item 1 record).*

**Alternatives considered**

### Problem 1: unattended signing of a passphrase-protected key under `rpm --addsign` (D1)
**Option A — per-invocation loopback pinentry** (`gpg --pinentry-mode loopback --passphrase-fd 0`) · How: inject loopback flags into every gpg call · Pros: no agent state · Cons: `rpm --addsign` shells out to `rpmsign`, which invokes gpg with fixed arguments (`%__gpg_sign_cmd`, `/usr/lib/rpm/macros:624`); loopback cannot be injected without overriding rpm's macro and forking the invocation.
**Option B — the `gpg-preset-passphrase` wrapper** (gnupg-tools; source `agent/preset-passphrase.c`) · How: call the wrapper with the keygrip · Pros: upstream tool, one command · Cons: an extra binary dependency and the script does not own the exact assuan line.
**Option C — raw agent protocol via `gpg-connect-agent` (D1, ratified)** · How: heredoc stdin, hex passphrase, assert the OK line · Pros: no extra dependency, the exact pinned command lives in the script, clearable after the run · Cons: the script owns protocol details that a wrapper would hide.
**Chosen:** C, because D1 pins it and the protocol is verified against the host's gpg 2.4.5 below.
**Competing priorities:** protocol ownership stays in the script (more code to review) rather than delegating to a wrapper binary.

### Problem 2: passphrase encoding on the assuan line
**Option A — raw passphrase on the line** · Cons: byte-unsafe on a line protocol; cleartext persists in agent debug logs.
**Option B — hex** · How: `xxd -p` of the file content, matching the upstream reference tool (`agent/preset-passphrase.c:162` sends `PRESET_PASSPHRASE %s%s -1 %s` with `bin2hex`) · Pros: byte-safe, upstream-blessed, cleartext never crosses a process boundary.
**Chosen:** B, because it matches the reference implementation exactly. Cost: the line is 2x the passphrase length.

### Problem 3: full-set verification (item 2: "verifies the full set with `rpm --checksig`")
**Option A — `gpg --verify` against a scratch gpg homedir** · Cons: requires extracting signatures out of RPM headers; not the path a dnf consumer exercises.
**Option B — `rpm --checksig` (alias of `rpm -K`)** · How: verifies against the system rpm keyring (installed `gpg-pubkey-*` packages in the rpmdb), the same path dnf uses at install time · Cons: requires a one-time root `rpm --import` of the public key (a non-root import fails with `can't create transaction lock on /usr/lib/sysimage/rpm/.rpm.lock (Permission denied)` — verified on the host).
**Chosen:** B, because it is the consumer's verification path. The script pre-flights the rpm keyring and prints the exact import command when the key is absent.
**Competing priorities:** one host-state change outside the dedicated keyring (a keyring package in the system rpmdb) traded for verification on the consumer's exact path.

### Problem 4: which keygrip to preset
**Option A — always the primary keygrip** · Cons: wrong when a signing subkey exists; gpg signs with the subkey and the agent's unprotect looks up the subkey's keygrip (`agent/findkey.c`).
**Option B — colon-format parse, signing subkey preferred, primary fallback** · How: `sec`/`ssb` lines, capability field 12, `grp` field 10 · Pros: mirrors gpg's own key selection; handles both subkey and primary-only layouts (item 1's `--full-generate-key` yields a subkey; a primary-only key is also acceptable per the key-parameter table).
**Chosen:** B, because the layout is decided by the user at item 1 and both must work.

**Pinned protocol (host gpg 2.4.5, `gnupg2-2.4.5-4.el10_1`; source read from the extracted source RPM, now removed — citations are the record)**

| Fact | Pinned value | Evidence |
|---|---|---|
| Preset command | `PRESET_PASSPHRASE <KEYGRIP> -1 <HEX>` | handler `agent/command.c:2549`; arg 2 is a **timeout** and only `-1` is accepted (any other value → `ERR 67108933 Not implemented`, verified empirically) |
| Command prefix | none. A leading `/` makes it a local control command (`unknown command`, verified empirically) | `gpg-connect-agent` man page, local command list |
| Clear command | `CLEAR_PASSPHRASE <KEYGRIP>` (separate command, not a flag) | `agent/command.c` handler; verified empirically (re-sign hangs after clear) |
| Termination | lowercase `/bye` | uppercase `/BYE` → unknown command, verified empirically |
| Keygrip case | uppercase, exactly as displayed by `gpg --with-colons -K` (`grp` line, field 10) | cache match is case-sensitive `strcmp` (`agent/cache.c`); agent debug log (`debug 0x40`, DBG_CACHE, `agent/agent.h:206`) showed the internal lookup key is uppercase on this build |
| Passphrase form | hex (`xxd -p`), round-trip checked in the script | reference tool `agent/preset-passphrase.c:162` |
| Agent prerequisite | `allow-preset-passphrase` in `gpg-agent.conf` (off by default; absent → `ERR 67108924 Not supported`) | verified empirically; script ensures it idempotently + `gpgconf --kill gpg-agent` |
| `gpg-connect-agent` exit status | returns 0 even on `ERR` replies | script asserts the `OK` line, not the exit code (verified empirically) |
| rpm's gpg invocation | `%__gpg_sign_cmd` = `gpg --no-verbose --no-armor --no-secmem-warning -sbo <sig> -- <plain>` | `/usr/lib/rpm/macros:624` |
| rpm macro requirement | `%_gpg_name` must be set or `rpmsign` errors (`You must set "%_gpg_name" in your macro file`); script passes `--define` | verified empirically |
| `rpm -K` strings | verified signature → `digests signatures OK` (lowercase); unverifiable → `SIGNATURES NOT OK` (uppercase); unsigned → `digests OK` | verified empirically; the script's case-insensitive `signatures OK` match cannot hit the failure string, which inserts `NOT` |
| `rpmsign` ownership | package `rpm-sign` (BaseOS), not `rpm-plugin-rpmsign` | `rpm -qf /usr/bin/rpmsign`; **host state change made: `sudo dnf install -y rpm-sign` → `rpm-sign-4.19.1.1-23.el10`** (reversible: `sudo dnf remove rpm-sign`) |

**Proof (throwaway keys in `/tmp` scratch; all artifacts destroyed after the run, rpm keyring import erased)**

- Two throwaway RSA-4096 keys generated in scratch keyrings (`--quick-generate-key`, loopback, passphrase on stdin; fingerprints `D6EC9260...7AC2B97E` and `977CE5CB...45EF7A2` are public data; passphrases existed only in shell variables and a 600-mode `/tmp` file, both now deleted).
- gpg cycle (key 1, single file): preset `OK` → `gpg --batch --yes --detach-sign` rc=0 with no prompt → `gpg --verify` "Good signature" → `CLEAR_PASSPHRASE` `OK` → re-sign hangs on pinentry (killed by timeout), proving the clear.
- Full-set run (key 2): all 64 real RPMs copied to a `/tmp` scratch project; the committed script run with `GNUPGHOME` pointed at the throwaway keyring and a sed-substituted fingerprint → rc=0, 64 signed, all 64 pass `rpm --checksig`, embedded signature key ID `d45ef7a2` matches the throwaway fingerprint. Re-run → rc=0, 0 signed, 64 skipped (idempotency), all 64 verified.
- Real `rpms/` untouched: 64/64 report `digests OK` (unsigned) before and after the scratch runs.
- The throwaway public key was `sudo rpm --import`ed temporarily to exercise the verification path, then erased (`sudo rpm --erase gpg-pubkey-d45ef7a2-6ab0df1c`); `rpm -qa` confirms only the three pre-existing `gpg-pubkey-*` packages remain.

**Changes**

| File | What changed |
|---|---|
| `repo-setup/sign-rpms.sh` (project repo, `b84ce3f`) | new, 256 lines: the item 2 artifact. Pre-flight (fingerprint, single secret key, keygrip derivation, passphrase-file modes, rpm-keyring presence), preset/clear around the sign loop, `rpm --checksig` verification, idempotent skip, fails loud naming the offending file |
| `planning/docs/TASK-0024-rpm-signing-gpgcheck.md` (team repo) | this section |

**Checks run**

| Test | Command | Result |
|---|---|---|
| Syntax | `bash -n repo-setup/sign-rpms.sh` | clean |
| Placeholder fingerprint | `GNUPGHOME=<scratch> bash sign-rpms.sh` | rc=1, `EXPECTED_FINGERPRINT is not recorded yet (TASK-0024 item 1 pending)` |
| Empty keyring, fingerprint substituted | sed'd copy, `GNUPGHOME=<empty scratch>` | rc=1, `keyring must hold exactly one secret key, found 0` |
| Full-set sign (64 copies, throwaway key) | `GNUPGHOME=<keyring2> bash sign-rpms.sh` on the scratch project | rc=0, 64 signed, 64 verified, preset cleared on exit |
| Idempotent re-run | same | rc=0, 0 signed, 64 skipped, 64 verified |
| Real set untouched | `rpm -K` loop over `rpms/*.rpm` | 64/64 `digests OK` (unsigned) |
| Passphrase exposure, by inspection | script review | read only from the 600-mode file into a shell variable, hex-encoded, sent on `gpg-connect-agent` stdin via heredoc; never in argv; no `set -x`; hex and cleartext wiped (`PASS=""`, `PASS_HEX=""`) after use; cleared from the agent on every exit path via the EXIT trap |

**Competing priorities**

- The rpm-keyring pre-flight makes the one-time root import a hard dependency of the script rather than a suggestion; traded because the verification claim is only as strong as the consumer's path.
- Hex encoding doubles the assuan line length; traded for byte-safety and exact match with the upstream reference tool.
- The script appends `allow-preset-passphrase` to the keyring's own `gpg-agent.conf` when missing and restarts the agent: a host-local, idempotent, one-line change inside a dedicated keyring, traded against requiring the user to pre-configure the agent at item 1.
- The fingerprint is asserted by string equality against `EXPECTED_FINGERPRINT`, currently `PENDING-ITEM-1`: the script is intentionally inert until item 1 records the real fingerprint; no signing is possible before then by design.

**Item 1 executed (2026-09-21, `Tails`).** User-directed change from the handoff (superseded by this record): the passphrase is the contents of `~/password.txt` (17 bytes, was 644); the agent placed the 600-mode copy by pure file operations (`mkdir -m 700` the sibling, `install -m 600` the copy) and generated the key non-interactively with `--pinentry-mode loopback --passphrase-file`; the user approved deleting `~/password.txt` after the copy. The passphrase contents were never read, echoed, displayed, logged, or recorded by any agent (AGENTS.md §4).

**Fingerprint (public data, ships inside the public key): `1689676AF4D4F6FEC142B4429C0A8912FDA02785`**, keygrip `F8F7A85609E1F45830A76F68E66D97DFA7AA05D0`. Recorded in `sign-rpms.sh` `EXPECTED_FINGERPRINT` (replacing `PENDING-ITEM-1`), project-repo `7d47a02`.

Key, as generated (`GNUPGHOME=~/.gnupg-cinnamon-rocky10 gpg --with-colons -K`):

- Exactly one secret key (one `sec:` line, no `ssb:`): RSA 4096, capabilities `sc`, no expiry (colon field 7 empty), primary-only layout (the handoff's "primary-only RSA 4096 sign key also acceptable" branch)
- uid exactly as ratified 2026-09-21: `metallinux Cinnamon for Rocky Linux (repo signing) <repo-signing@metalinux.dev>` (the pending-domain note in the handoff is resolved by this ratification)
- Passphrase-protected, proven by signing: a loopback sign without a passphrase fails (`gpg: Sorry, we are in batchmode - can't get input`, rc=2); with `--passphrase-file` on the 600-mode sibling copy, a scratch clearsign succeeds and verifies `Good signature from "metallinux Cinnamon for Rocky Linux (repo signing) <repo-signing@metalinux.dev>"` (scratch artifacts destroyed)
- Generation command (rc=0): `gpg --batch --yes --pinentry-mode loopback --passphrase-file <600-mode copy> --quick-generate-key "metallinux Cinnamon for Rocky Linux (repo signing) <repo-signing@metalinux.dev>" rsa4096 sign never`

Host identity, confirmed in writing per item 1 acceptance (carried over from the handoff, unchanged): hostname `shadow`, 192.168.1.102 (`enp2s0`), libvirt bridge 192.168.122.1 (`virbr0`), user `howard`, matches the plan's agent-host assumption (the libvirt host).

**Pinned gpg 2.4.5 key-generation behavior** (throwaway keys in a `/tmp` scratch dir, all destroyed after the run; the throwaway passphrases were test strings, never the real one):

| Fact | Pinned value | Evidence |
|---|---|---|
| Non-interactive generation | `--batch --yes --pinentry-mode loopback --passphrase-file FILE --quick-generate-key uid rsa4096 sign never` produces a passphrase-protected RSA 4096 primary `[SC]`, no subkey, no expiry | man page (gpg 2.4.5): with `--batch` + loopback + one of the passphrase options "the supplied passphrase is used for the new key and the agent does not ask for it"; empirically, two throwaway keys generated exactly this way |
| `usage sign` on a primary | yields `[SC]` (sign+certify), not sign-only, and no subkey is created ("If algo or usage are given, only the primary key is created") | throwaway listing `sec rsa4096 ... [SC]` with no `ssb`; man page: the default for a primary is certification+signing, `cert` is the only alternative usage value |
| Trailing newline | gpg strips a trailing newline from the passphrase file/fd on both generation and signing | four probes on a throwaway key generated from a file containing `X\n`: signing with `--passphrase X` (exact argv), `--passphrase-fd` given `X\n`, `--passphrase-file` with `X`, and with `X\n` all succeeded → the key holds `X` (stripped at generation) and the fd/file paths strip too |
| Consequence for item 3 | the script's `PASS=$(cat file)` (bash strips trailing newlines, sign-rpms.sh:174) presets the same effective passphrase gpg used at generation, whether or not the file ends in a newline; the multi-line round-trip check (sign-rpms.sh:178-179) still rejects anything else | the two rows above + inspection of the script |

**Host state after the run** (verified with `stat`/`ls`; passphrase contents never read):

| Path | Mode | Check |
|---|---|---|
| `~/.gnupg-cinnamon-rocky10/` | 700 | dedicated keyring; `private-keys-v1.d/` 700 holding exactly one 600-mode key file (`F8F7A856...05D0.key`); `openpgp-revocs.d/` 700 (revocation certificate, host-local); `pubring.kbx` 644 (public data); `trustdb.gpg` 600 |
| `~/.gnupg-cinnamon-rocky10.passphrase/` | 700 | sibling location (D1) |
| `~/.gnupg-cinnamon-rocky10.passphrase/passphrase` | 600 | 17 bytes; `cmp` against the source reported byte-identical before the source was deleted |
| `~/password.txt` | deleted | user-approved; was 644, 17 bytes; `rm` rc=0, absence confirmed by `ls` |
| system rpm keyring | — | one-time `sudo rpm --import keys/cinnamon-rocky10-public.asc` rc=0 → `gpg-pubkey-fda02785-6ab101f4` (key id `FDA02785` = last 8 of the fingerprint); the three pre-existing `gpg-pubkey-*` packages (from the item 2 session's baseline) untouched |

**Changes** (project repo, commit `7d47a02` on `feature/TASK-0024-rpm-signing-gpgcheck`, pushed to origin):

| File | What changed |
|---|---|
| `keys/cinnamon-rocky10-public.asc` (new) | the public key, armored; grep on the committed blob: exactly one `BEGIN PGP PUBLIC KEY BLOCK`, zero private blocks |
| `repo-setup/sign-rpms.sh` | `EXPECTED_FINGERPRINT` `PENDING-ITEM-1` → `1689676AF4D4F6FEC142B4429C0A8912FDA02785`; header uid updated to the ratified string; `bash -n` clean |
| `.gitignore` | new section guarding key material: `.gnupg-cinnamon-rocky10/`, `.gnupg-cinnamon-rocky10.passphrase/`, `private-keys-v1.d/`, `openpgp-revocs.d/`, `passphrase`, `*.passphrase`, `*-secret.asc`, `*-private.asc`, `*-secret.key`, `*-private.key`. Verified with `git check-ignore` on real on-disk paths: every key-material path ignored, `keys/cinnamon-rocky10-public.asc` still trackable |

**Pre-push proof** (on the committed tree, `git grep ... HEAD` at `7d47a02`):

| Check | Command | Result |
|---|---|---|
| No private key block in the branch | `git grep -il "BEGIN PGP PRIVATE KEY BLOCK" HEAD` | zero hits (rc=1) |
| Keyring dir name in the branch | `git grep -il "private-keys-v1.d" HEAD` | exactly one hit, `HEAD:.gitignore`: the `.gitignore` pattern line itself, anticipated by the item 1 brief |
| Only public block in the tree | `git grep -l "BEGIN PGP" HEAD` | only `keys/cinnamon-rocky10-public.asc` |

`git status` in the project tree shows no private key material and no passphrase (the untracked `AGENTS.md` in the project root pre-dates this run, is not key material, and was left untracked). The passphrase now exists only in the 600-mode sibling file on the host.

**Alternatives considered (the handoff deviation).** The handoff specified interactive `gpg --full-generate-key` with the user entering the passphrase at the pinentry prompt.
- **Option A, interactive generation as handed off** · Cons: the user's 2026-09-21 directive settled the passphrase by reference to `~/password.txt`, and an interactive prompt cannot consume a file without the user retyping the value; rejected against the user directive.
- **Option B, `--passphrase <value>` on argv** · Cons: the value is visible in `ps` for the duration of the keygen; rejected (AGENTS.md §4).
- **Option C, a batch file with `%passphrase <file>`** · Pros: documented non-interactive path · Cons: an extra artifact to manage, and the user named the flag combination; the batch file would also sit on disk during the run.
- **Option D, `--pinentry-mode loopback --passphrase-file <600-mode copy>` (chosen)** · Pros: exactly the user-named combination, the value stays inside gpg (never argv), generation and the item 3 script consume the identical artifact, and the trailing-newline semantics were pinned on throwaway keys before the real generation · Cons: none material.

Notes carried over: the uid cannot be changed after generation. The handoff's same-passphrase-on-subkey constraint is moot (no subkey exists; the script's keygrip derivation handles both layouts and takes the primary grip on this one). The §13 exception now covers this key plus its sibling passphrase file, both host-side, as ratified.

**Item 3 executed (2026-09-21, `Tails`).** Production sign run on `feature/TASK-0024-rpm-signing-gpgcheck` (project repo, `db60bb6`, pushed). No script fixes were needed; `sign-rpms.sh` is unchanged since `7d47a02`. Evidence files in `/tmp/opencode/task0024-item3/` (host-local, not in the repo).

**Pre-sign baseline.** 64/64 unsigned: `for f in *.rpm; do rpm -K "$f"; done | sed 's|.*/||' | awk -F': ' '{print $2}' | sort | uniq -c` → `64 digests OK`. Per-RPM payload digests captured BEFORE signing with `for f in $(ls *.rpm | sort); do printf '%s  %s\n' "$(rpm2cpio "$f" | sha256sum | awk '{print $1}')" "$f"; done > payload-before.txt` (64 lines; `rpm2cpio` emits the file payload stream, so the header signature slots are excluded by construction).

**Sign run.** `bash repo-setup/sign-rpms.sh` (production path: default keyring `~/.gnupg-cinnamon-rocky10`, default sibling passphrase location), rc=0: 64 signed, 0 skipped, 64 verified, preset cleared on exit. The run added `allow-preset-passphrase` to the keyring's `gpg-agent.conf` (idempotent, it was absent) and restarted the agent — the one host-local change, already recorded under item 2's competing priorities. Post-run agent state: a batch sign without passphrase now fails (`gpg: Sorry, we are in batchmode - can't get input`, rc=2), proving the preset was really cleared, not just reported as.

**Payload identity (D2).** The identical digest command after signing → `payload-after.txt`; `diff payload-before.txt payload-after.txt` empty → **64/64 identical**. The D2 flip condition did not trigger; no `spec/` rebuilds.

**Full-set verification.** `for f in *.rpm; do rpm --checksig "$f"; done | sed 's|.*/||' | awk -F': ' '{print $2}' | sort | uniq -c` → `64 digests signatures OK`. All 64 valid against key `1689676AF4D4F6FEC142B4429C0A8912FDA02785` (public key in the rpm keyring as `gpg-pubkey-fda02785-6ab101f4` since item 1).

**Runtime no-leak proof** (`## Plan` validation: the sign run leaves the passphrase out of `ps`, shell history, and logs). The passphrase value was loaded into an in-memory shell variable only for the checks below; it was never printed, and the commands reference only the 600-mode path.

| Check | Method | Result |
|---|---|---|
| process argv, whole run | background sampler for the duration of the sign run: `ps -eo args=` (every process on the host) plus `tr '\0' '\n' /proc/<pid>/environ` for the `sign-rpms.sh` process(es), 95 samples at ~0.4 s spacing (each sample ~45 KB; 4.3 MB total, `ps-samples.txt`) | zero matches (`grep -qF` on the in-memory value) |
| run log | the sign run's stdout+stderr captured to `sign-run.log` | zero matches |
| shell history | `grep -qF` on `~/.bash_history` | zero matches |
| logs on disk | keyring directory listing: no log files (agent logging is off by default, none enabled) | clean |

**Commit and push.** `git diff --stat` before committing: 64 files changed, all `rpms/*.rpm`, nothing outside `rpms/` (0 non-RPM paths; file sizes unchanged, signatures land in fixed header slots). Committed as `db60bb6` ("TASK-0024 item 3: sign all 64 RPMs in place with the repo signing key"); pre-push `git grep -il "BEGIN PGP PRIVATE KEY BLOCK" HEAD` → zero hits (rc=1); pushed `7d47a02..db60bb6`. GitHub's advisory warning that two pre-existing mozjs115 debuginfo RPMs exceed 50 MB (tracked before this task; sizes unchanged by signing) — noted for the release, not a failure.

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
