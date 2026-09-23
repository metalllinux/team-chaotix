# TASK-0024 — Sign the Cinnamon RPMs, enable gpgcheck, publish the release manifest

> **Section order below is fixed.** Each agent writes to its own section and no other. `Robotnik`
> reads only `## Status` and `## Next Actions`. Do not reorder, rename, or remove sections.

- **Created:** 2026-09-19

---

## Status

*Owner: `Robotnik`. Keep this SHORT and CURRENT — it is one of only two sections the PM reads, so a
stale entry means the whole loop runs on bad information.*

**Now (2026-09-21, fix pass complete): Tails cleared all six chain findings; re-running the chain.**
Project branch at `ba7babf` (pushed). Blocker cleared (harness now ships `keys/` to the VM, so the
positive fresh-VM line is unblocked); signer now pinned via a scratch rpm keyring (deviation from
Omega's suggested `%{SIGPGP}`, which does not exist on this rpm); RPM count 48→64; nits cleared;
`set -x` guard probes `$-` (deviation: `BASHOPTS` does not list `xtrace` in a script shell);
INSTALL.md points the follower at the metalinux.dev out-of-band fingerprint. Pre-push greps clean,
passphrase absent from the diff. Re-running `Shadow` → `Omega` → `Big`; Big re-runs the positive
fresh-VM line (item 10) and the skipped fallback (item 11c).

**Now (2026-09-21, review chain complete): implementation items 1-6 done; chain returned 1
blocker + 2 should-fix, dispatching Tails fixes.** Review chain ran on the full branch diff
(`feature/TASK-0024-rpm-signing-gpgcheck` vs `main` `893b22a`). Shadow: 7 findings (1 blocker, 2
should-fix, 4 nits) in `## Review` — the blocker is that `vm-test/test-repo-setup.sh` ships no
`keys/` to the VM, so `setup-repo.sh`'s new key-import step dies there and the DoD's fresh-VM
end-to-end is unreachable as-is. Omega: no security blockers (1 medium — no out-of-band
fingerprint anchor; 3 low) in `## Security`. Big: negative tamper test PASS (gpgcheck=1 refuses a
payload flip, gpgcheck=0 accepts it), positive fresh-VM line BLOCKED (not failed) by the harness
`keys/` gap in `## Test Results`; RPM-size question closed with evidence. Tails is fixing the
blocker + should-fixes + nits; the chain re-runs after.

**Now (2026-09-21, implementation): items 1-5 complete, item 6 (docs) dispatching to Tails.**
Key generated (fingerprint `1689676AF4D4F6FEC142B4429C0A8912FDA02785`, passphrase-protected,
proven by signing); all 64 RPMs signed in place (payload identity 64/64, `rpm --checksig` 64/64
OK, runtime no-leak proven); `rpms/SHA256SUMS` published from the signed set; `setup-repo.sh`
imports the public key and writes `gpgcheck=1` (no `gpgkey=` line); key-material `.gitignore`
guard committed; `~/password.txt` deleted (user-approved). Branch
`feature/TASK-0024-rpm-signing-gpgcheck` at `55a38ba`, pushed, pre-push greps clean every time.
Next: item 6 docs (Tails), then the review chain, then Big's functional verification (items 7-11),
then Vector, then Knuckles (item 14, tag `v1.0.0` on the merge).

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
      the repo tree; the final merged tree passes `git grep` for `BEGIN PGP PRIVATE KEY BLOCK`
      with zero hits, and `git grep` for `private-keys-v1.d` hits only the `.gitignore` guard
      line itself (no keyring, cert, or passphrase path in the tree); a `.gitignore` on the
      branch covers key-material paths;
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
- [x] `Tails` (2026-09-21): items 4 + 5 executed — `rpms/SHA256SUMS` generated from the signed
      set (`sha256sum *.rpm | sort -k2`, 64 lines, `sha256sum -c` 64/64 OK) as project-repo
      `1b57ac8`; `setup-repo.sh` imports `keys/cinnamon-rocky10-public.asc` (assert
      `rpm -q "gpg-pubkey-fda02785*"`, 8-hex keyid width pinned), writes `gpgcheck=1` with no
      `gpgkey=` line; reference template flipped to `gpgcheck=1` and harness test 6 updated to
      match (conflict noted in `## Implementation`, flagged for Shadow); statelessness re-proven
      on the host; `55a38ba` pushed, pre-push grep zero hits. Execution records in
      `## Implementation`.
- [ ] `Robotnik`: dispatch item 6 (docs: Quick start, Manual, new "Verifying the release"
      section, README signing section) to `Tails` — critical path continues 6 → 7 → 8 → 9 →
      10 → 11 → 14.
- [x] `Tails` (2026-09-21): item 6 executed — all four doc surfaces updated (Quick start
      gpgcheck=1 + key import, Manual 6 steps with key import and `gpgcheck=1` template, new
      "Verifying the release" section with the manifest/signature division of labor, README
      signing section); `gpgcheck=0` no longer appears in either doc; project-repo `e6ee370`
      pushed, pre-push greps zero hits, passphrase absent from the committed diff. Execution
      record in `## Implementation`. Critical path continues at item 7 (open the PR to main).
- [x] `Shadow` → `Omega` → `Big`: review chain run on the full branch diff. Shadow: 7 findings
      (1 blocker, 2 should-fix, 4 nits) in `## Review`. Omega: no security blockers (1 medium, 3
      low) in `## Security`. Big: negative tamper PASS, positive fresh-VM BLOCKED by the harness
      `keys/` gap in `## Test Results`.
- [x] `Tails`: fix the chain's findings — (1) BLOCKER: `vm-test/test-repo-setup.sh` phase 1 must
      ship `keys/` to the VM before `setup-repo.sh` runs; (2) should-fix: `repo-setup/sign-rpms.sh`
      pin the signing key so verification checks the expected fingerprint, not any keyring key
      (consolidates with Omega low #1); (3) should-fix: `vm-test/test-repo-setup.sh:369-373` RPM
      count 48 → 64; (4) nits: `sign-rpms.sh` dead hex round-trip comment (:178-180), add `xxd`/`stat`
      to the tool pre-flight (:105-107), guard the `rpm -qa | grep` SIGPIPE (:150); (5) Omega low:
      refuse to run under `set -x` (check `BASHOPTS` for `xtrace`); (6) Omega medium: add one line
      to INSTALL.md telling the follower to compare the fingerprint against the out-of-band value
      published on metalinux.dev (the metalinux.dev publish itself is a separate follow-up, not
      blocking). Record each fix in `## Implementation`.
- [ ] Re-run the chain (`Shadow` → `Omega` → `Big`) after the fixes; `Big` re-runs the positive
      fresh-VM line (item 10) and the skipped fallback (item 11c) for a clean pass.
- [ ] `Vector`: docs pass (consistency/house style) on the item 6 surfaces.
- [ ] `Knuckles`: open the PR to main, merge, cut tag `v1.0.0` on the merge (plan item 14).
      *PM sequencing note: the plan's item 7 "open the PR" is folded into this Knuckles release
      step per house rules; the PR is not opened before the review chain.*
- [ ] Follow-up (non-blocking, Omega medium): publish the fingerprint on metalinux.dev so there is
      an out-of-band anchor before the first public tag.

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

*Owner: `Tails`. Item 1 complete 2026-09-21 (key `1689676AF4D4F6FEC142B4429C0A8912FDA02785`; public key, fingerprint, and key-material `.gitignore` guard committed as project-repo `7d47a02`); item 2 complete 2026-09-21 (`repo-setup/sign-rpms.sh`, project-repo `b84ce3f`); item 3 complete 2026-09-21 (all 64 RPMs signed in place, project-repo `db60bb6`); item 4 complete 2026-09-21 (`rpms/SHA256SUMS` from the signed set, project-repo `1b57ac8`); item 5 complete 2026-09-21 (`setup-repo.sh` key import + `gpgcheck=1`, project-repo `55a38ba`); item 6 complete 2026-09-21 (docs: Quick start, Manual, new "Verifying the release" section, README signing section, project-repo `e6ee370`). Branch `feature/TASK-0024-rpm-signing-gpgcheck` pushed; no key material in the branch (pre-push grep in the item 1, item 5, and item 6 records).*

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

**Item 4 executed (2026-09-21, `Tails`).** `rpms/SHA256SUMS` generated from the signed set (generated on `feature/TASK-0024-rpm-signing-gpgcheck` at tip `db60bb6`, so every hash covers the signed bytes per the item 3 record). Committed as project-repo `1b57ac8` ("TASK-0024 item 4: add rpms/SHA256SUMS manifest for the signed set"), one file, 64 insertions.

- **Generation command:** `cd rpms && sha256sum *.rpm | sort -k2 > SHA256SUMS` (D4 format: sha256sum output, basenames only, sorted by filename). `wc -l` → 64 lines; `sort -c -k2` clean; zero path separators in any field 2 (`awk '{print $2}' SHA256SUMS | grep -c '/'` → 0). `git check-ignore rpms/SHA256SUMS` → rc=1 (not ignored; only `rpms/repodata/` and `rpms/.repodata/` are gitignored, .gitignore:13-14).
- **Acceptance:** `cd rpms && sha256sum -c SHA256SUMS` → 64/64 `: OK`, zero FAILED, rc=0 (full output host-local at `/tmp/opencode/task0024-item4-verify.txt`).
- `createrepo_c` only ingests RPM files, so `SHA256SUMS` in `rpms/` is inert for repodata (plan assumption, D4; cheaply falsified by item 10's `dnf makecache`). The tag pin (D4) is Knuckles' at item 14, not cut here.

**Item 5 executed (2026-09-21, `Tails`).** `setup-repo.sh` now imports the public key per D3 and writes `gpgcheck=1`. Committed as project-repo `55a38ba` ("TASK-0024 item 5: import GPG public key in setup-repo.sh, write gpgcheck=1"): `repo-setup/setup-repo.sh` (+49/−5 lines), `repo-setup/cinnamon-rocky10.repo` (1 line), `vm-test/test-repo-setup.sh` (test 6, 7/6 lines). Pushed `db60bb6..55a38ba` (the push also carried `1b57ac8`).

**Keyid width, determined at implementation (the plan row's open question).** rpm 4.19 on the host names the imported key package **8 hex chars, lowercase**: `rpm -qa | grep gpg-pubkey` → `gpg-pubkey-fda02785-6ab101f4` (keyid `fda02785` = last 8 of the fingerprint, timestamp `6ab101f4` = per-machine import time). So the script sets `KEY_ID="fda02785"` (setup-repo.sh:42) and asserts with a prefix glob, because the timestamp suffix makes a full-name query non-portable. Glob behavior pinned on the host: `rpm -q "gpg-pubkey-fda02785*"` → `gpg-pubkey-fda02785-6ab101f4`, rc=0; `rpm -q "gpg-pubkey-00000000*"` → "not installed", rc=1.

**Changes**

| File | What changed |
|---|---|
| `repo-setup/setup-repo.sh` | new step 3 (setup-repo.sh:117-142): `KEY_FILE="${PROJECT_ROOT}/keys/cinnamon-rocky10-public.asc"`, existence check, `rpm --import`, assert via `rpm -q "gpg-pubkey-${KEY_ID}*"`, fails loud naming the expectation; subsequent steps renumbered (4 .repo write, 5 CRB, 6 makecache) and the header list updated (setup-repo.sh:10-17); the .repo printf's gpgcheck argument `"0"` → `"1"` (setup-repo.sh:156-165) with no `gpgkey=` line per D3; `KEY_ID` constant with the width evidence in the comment (setup-repo.sh:37-42) |
| `repo-setup/cinnamon-rocky10.repo` | reference template line 11: `gpgcheck=0` → `gpgcheck=1` (the plan row's named edit) |
| `vm-test/test-repo-setup.sh` | test 6 only: the template assertion `grep -q "gpgcheck=0"` → `grep -q "gpgcheck=1"` (see the conflict note below) |

**Statelessness contract preserved (the plan row's second acceptance point).** The new step is state-changing and sits below project-root resolution (setup-repo.sh:59-66) and the root check, so the bad-argument path still dies before any state-changing step. Re-ran the harness test-3 pattern on the host: `sudo bash repo-setup/setup-repo.sh /tmp/nonexistent-task0024-<ts>` → rc=1 at `cd -P` (line 62, "No such file or directory"), with before/after snapshots identical for: createrepo_c install state, `/etc/yum.repos.d/cinnamon-rocky10.repo` presence, md5 of every `/etc/yum.repos.d/*.repo`, `rpm -qa | grep gpg-pubkey` (the keyring the new step would touch), and `find rpms -type f -newer <marker>`. The `vm-test/test-repo-setup.sh` statelessness assertion therefore still holds, by inspection and by this run.

**Import idempotency.** Re-ran `sudo rpm --import keys/cinnamon-rocky10-public.asc` on the host (key already present since item 1): rc=0, `rpm -qa | grep gpg-pubkey` byte-identical before/after — no duplicate keyring package, so a re-run of `setup-repo.sh` (the rollback section's interrupted-VM case) is idempotent.

**The `.repo` block the script now writes** (the script's exact printf, run with this clone's baseurl):

```
[cinnamon-rocky10]
name=Cinnamon for Rocky Linux 10 (local)
baseurl=file:///home/howard/Linux/projects/cinnamon-for-rocky10/rpms
enabled=1
gpgcheck=1
metadata_expire=0
module_hotfixes=0
keepcache=0
```

**Checks run**

| Test | Command | Result |
|---|---|---|
| Syntax | `bash -n repo-setup/setup-repo.sh`; `bash -n vm-test/test-repo-setup.sh` | both clean |
| Bad-argument path, as root | `sudo bash repo-setup/setup-repo.sh /tmp/nonexistent-task0024-<ts>` + state snapshots | rc=1 at line 62 (`cd -P`), zero host state change including the `gpg-pubkey-*` keyring |
| Keyring assertion | `rpm -q "gpg-pubkey-fda02785*"` / `rpm -q "gpg-pubkey-00000000*"` | rc=0, package named / rc=1, not installed |
| Import idempotency | `sudo rpm --import keys/cinnamon-rocky10-public.asc` (re-run) | rc=0, keyring unchanged |
| Written `.repo` block | the script's printf verbatim to a `/tmp` file | `gpgcheck=1` present, no `gpgkey=` line |
| Pre-push key-material | `git grep -il "BEGIN PGP PRIVATE KEY BLOCK" HEAD` at `55a38ba` | zero hits (rc=1); `git grep -il "private-keys-v1.d" HEAD` → only `HEAD:.gitignore` (the pattern line itself, same as item 1); `git grep -l "BEGIN PGP" HEAD` → only `keys/cinnamon-rocky10-public.asc` |

**Alternatives considered (the keyring assertion form).**
- **Option A — full-name query `rpm -q gpg-pubkey-fda02785-<timestamp>`** · Cons: the timestamp is the import time on that machine; unknowable in the script.
- **Option B — `rpm -qa | grep fda02785`** · Cons: matches any package whose name merely contains the string, and departs from the `rpm -q` form the plan row names.
- **Option C — prefix glob `rpm -q "gpg-pubkey-${KEY_ID}*"` (chosen)** · Pros: the plan-named `rpm -q` form, stable across machines, matches exactly the one package name rpm 4.19 produces for this key (width evidence above).

**Conflict with the existing harness, surfaced (AGENTS.md §5).** `vm-test/test-repo-setup.sh` test 6 (lines 314-320 pre-change) asserted `gpgcheck=0` in the reference template — the old, unsigned value. Item 5's plan row flips that value in the template, so the old assertion would go red against the correct new behavior. Test 6 was updated to assert `gpgcheck=1` and recorded here; flagged for `Shadow` (item 8, which specifically checks the statelessness-contract change). No other test in the file references gpgcheck. The end-to-end proof that a follower actually gets dnf signature verification remains items 10-11 (fresh VM, negative test); on the host the components are each proven as above, and the host's keyring already held the key since item 1, so this run exercised the idempotent path, not a first import.

**Item 6 executed (2026-09-21, `Tails`).** All four doc surfaces from the plan row updated on `feature/TASK-0024-rpm-signing-gpgcheck`, committed as project-repo `e6ee370` ("TASK-0024 item 6: document signing, gpgcheck=1, and release verification"), pushed `55a38ba..e6ee370`. Only `INSTALL.md` and `README.md` changed (99 insertions, 7 deletions).

**Before/after by surface**

- **(a) INSTALL.md, Quick start step 2.** Before: the step described the script as writing the `.repo` file, enabling CRB, and validating readability, with no mention of signatures. After: the step states that the script imports the public GPG key from `keys/cinnamon-rocky10-public.asc` into the rpm keyring and writes the `.repo` with `gpgcheck=1`, so dnf verifies the signature of every package it installs, the same model as the EL base repositories.
- **(b) INSTALL.md, Manual repository setup.** Before: 5 steps; the `.repo` template carried `gpgcheck=0`; no key import. After: 6 steps. New step 3 imports the key (`sudo rpm --import keys/cinnamon-rocky10-public.asc` from the project root, fingerprint stated, re-import noted as a no-op). Step 4's template flipped to `gpgcheck=1` with the explanation of what the line does and why there is no `gpgkey=` line (the key already lives in the rpm keyring, D3). CRB and install renumbered to 5 and 6. The old template's `gpgcheck=0` was the only occurrence of that string in either doc; it no longer appears anywhere.
- **(c) INSTALL.md, new "Verifying the release" section** (after "Direct RPM install (fallback)", before "Prerequisites"). Opens with clone-at-tag (`git clone --depth 1 --branch v1.0.0`, per D4 the first signed release is `v1.0.0` and every future republish gets a new tag). Three subsections. "The sha256 manifest, corruption and drift" gives `cd rpms && sha256sum -c SHA256SUMS` (64/64 `OK` required) and states what the check cannot catch, a tree in which both the RPMs and the manifest were changed together, because the tree is its own baseline. "The GPG signature, origin tampering" covers dnf under `gpgcheck=1` plus the direct path (`sudo rpm --import` then `rpm --checksig` over all 64, expected output `digests signatures OK`, the pinned string from the item 2 record), with the key path and fingerprint. "Why both" states the division of labor Omega asked for (TASK-0016 doc, carried into this plan's D4) in one place. The manifest verifies the copy against the trusted baseline pinned at the tag and catches transfer corruption and drift. The signature verifies the origin and catches a tampered set that a matching manifest would accept, because re-signing needs the private key.
- **(d) README.md, new "Signing and release verification" section** (before "## Installation"). Short, one paragraph plus the facts. The 64 RPMs are signed with a dedicated GPG key, the repository installs with `gpgcheck=1`, the public key ships at `keys/cinnamon-rocky10-public.asc` (fingerprint), `setup-repo.sh` imports it, each release is pinned to a git tag, the manifest is `rpms/SHA256SUMS`, and INSTALL.md's "Verifying the release" section carries the two checks with the one-line division of labor.

**Checks run**

| Test | Command | Result |
|---|---|---|
| `gpgcheck=0` absent from docs | `grep -n "gpgcheck=0" INSTALL.md README.md` | zero hits (rc=1) |
| House style, em/en dashes | `grep -nP '[\x{2014}\x{2013}]' INSTALL.md README.md` | zero hits (rc=1) |
| Fingerprint present | `grep -n 1689676AF4D4F6FEC142B4429C0A8912FDA02785 INSTALL.md README.md` | 3 hits. Manual step 3, the signature subsection, README (public data, permitted) |
| Diff scope | `git diff --cached --stat` before commit | only `INSTALL.md` and `README.md`, 99 insertions / 7 deletions |
| Pre-push private key block | `git grep -il "BEGIN PGP PRIVATE KEY BLOCK" HEAD` at `e6ee370` | zero hits (rc=1) |
| Keyring dir name in branch | `git grep -il "private-keys-v1.d" HEAD` | exactly one hit, `HEAD:.gitignore` (the pattern line itself, same as items 1 and 5) |
| Only public block in tree | `git grep -l "BEGIN PGP" HEAD` | only `keys/cinnamon-rocky10-public.asc` |
| Passphrase in committed diff | value loaded into a shell variable from the 600-mode sibling file (never printed), `grep -qF` on `git diff 55a38ba e6ee370` | zero matches (the staged-diff check before commit was also clean) |

**Alternatives considered**

- **Placement of "Verifying the release".** Option A, before the Quick start, because verification precedes trust. Rejected. The section's own first step is clone-at-tag, and it cross-references the Quick start and Manual steps by name, so it reads as the answer to "how do I know what I cloned is what it claims" once the install methods are in hand. Option B, after "Direct RPM install (fallback)", chosen. It closes the block of install methods and precedes the reference sections.
- **Naming `v1.0.0` in the docs before the tag exists.** D4 names the tag and says INSTALL.md tells followers to clone at the tag, and the DoD manifest box requires the doc tie to a tag, so the name goes in now. The tag is cut at item 14 after merge, which is also when the docs stop being branch-only. Recorded as a known short window, not a defect.
- **README section placement.** Before "## Installation", chosen, because signing is a property of what the reader is about to install and the section sits next to the INSTALL.md pointer. Rejected, after "Build notes", which is about how the set was built, not how the release is verified.

**Competing priorities**

- The "Direct RPM install (fallback)" section is deliberately untouched by this item. Item 11c will characterize the local-file signature behavior, and item 11's acceptance row explicitly lets Tails correct item 6's wording afterward if needed. Labeling the fallback "unverified-by-signature" now would state a claim (likelihood medium per the plan risk table) that is neither proven nor refuted yet.
- The docs repeat the fingerprint in three places (Manual step 3, the signature subsection, README) rather than pointing to a single location. Traded for a follower who never opens the key file still having the public value to compare against, and the fingerprint is public data that ships inside the key.
- House style held to AGENTS.md §10. Prose over bullets in the new section, no em/en dashes (grep-verified), no colons introducing explanations, and the division of labor stated as a position (run both checks) rather than presented as equal options.

**Fix pass executed (2026-09-23, `Tails`).** All six chain findings cleared on `feature/TASK-0024-rpm-signing-gpgcheck`, committed as project-repo `ba7babf` ("TASK-0024 fix pass: clear the review chain findings", 3 files, +98/−30), pushed `e6ee370..ba7babf`.

- (1) BLOCKER, `vm-test/test-repo-setup.sh`: phase 1 now rsyncs `keys/` to the VM after the `rpms/` copy and before phase 2, with a `record` check that `keys/cinnamon-rocky10-public.asc` landed (new "public key copied to VM" record); header step 2 updated to name `keys/`.
- (2) should-fix, `repo-setup/sign-rpms.sh` signer pinning: the final verification now runs against a scratch rpm keyring, not the host keyring. `mktemp -d` (mode 700) + `rpm --root $S --import keys/cinnamon-rocky10-public.asc`, then per RPM `rpm --root $S -K file | grep -qi "signatures OK"` or die. No sudo; the scratch dir is removed by the EXIT trap (renamed `cleanup`). The final report names the pinned fingerprint.
- (3) should-fix, `vm-test/test-repo-setup.sh`: remote RPM count assertion 48 → 64 (comment cites the item 3 record).
- (4) nits, `repo-setup/sign-rpms.sh`: dropped the tautological hex round-trip check (`unhex(hex(x))=x` cannot fail; a malformed file is rejected by gpg-agent, which then answers without an OK line and the preset step dies); added `xxd`/`stat` to the tool pre-flight; replaced `rpm -qa | grep -q` with `rpm -q "gpg-pubkey-${KEYID8}-*"`. The glob is required, a bare prefix matches nothing (verified rc=1 on the host with the key installed); same naming rule as `setup-repo.sh:139`.
- (5) Omega low, `repo-setup/sign-rpms.sh`: startup refusal under `set -x`/`bash -x`. Deviation from the brief, recorded: the brief said check `BASHOPTS` for `xtrace`, but on this host `BASHOPTS` does not list `xtrace` in a script shell even when launched with `bash -x` (verified, identical BASHOPTS under `bash -x` and plain, `$-` differs `hxBc` vs `hBc`). The guard probes `$-` instead. Verified: `bash -x repo-setup/sign-rpms.sh /nonexistent` → refusal to stderr, rc=1, trace stops at 5 lines.
- (6) Omega medium, `INSTALL.md`: one line in "Verifying the release" telling the follower to compare the fingerprint against the out-of-band value on metalinux.dev before trusting the key.

**Alternatives considered**

- **Pinning mechanism for (2).** Option A, extract the public key embedded in the RPM signature header (`rpm -qp --qf '%{SIGPGP}'`, per Omega's note) and build the keyring from that. Rejected after verification: this rpm does not embed the key, `%{SIGPGP}`/`%{SIGGPG}` return `(none)`, `%{PGPSIG}`/`%{PGP}` are unknown tags, and numeric tags (`%{1005}`) are unsupported in queryformat on rpm 4.19.1.1. Option B, chosen, the `rpm --root` scratch keyring importing the repository's public key file. Pinning proven in all four directions: throwaway-signed pkg vs real-only keyring → NOT OK rc=1; throwaway-signed vs throwaway keyring → OK rc=0; real-signed vs throwaway-only keyring → NOT OK rc=1; real-signed vs real-only keyring → OK rc=0. Also verified: `rpm --initdb --root` fails rc=255 silently and creates nothing, so the script skips it and relies on `--import` auto-initializing the rpmdb.
- **Idempotency gate kept on host-keyring semantics.** `is_signed()` (used to skip already-signed packages) still consults the host keyring; only the final claim is pinned. A package signed by a different key would be skipped as already signed and then fail the pinned verification, so nothing unpinned passes the script. Traded away: a second `rpm -K` per package in the sign loop, not worth it for a run that skips 64/64 in steady state.

**Checks run**

| Check | Command | Result |
|---|---|---|
| Syntax, both scripts | `bash -n repo-setup/sign-rpms.sh`, `bash -n vm-test/test-repo-setup.sh` | both OK |
| Pinned loop, full set | scratch keyring via `rpm --root --import`, per-RPM `rpm --root -K` grep, all 64 RPMs | 64 pass, 0 fail, 1 s |
| End-to-end script run | `bash repo-setup/sign-rpms.sh` | rc=0; "Signed now 0 / Already signed 64 / Total verified 64"; trap cleared the preset |
| Files unchanged by the run | `sha256sum -c rpms/SHA256SUMS` after the run | 0 non-OK lines |
| xtrace guard | `bash -x repo-setup/sign-rpms.sh /nonexistent` | refusal, rc=1, 5 trace lines |
| Keyring preflight pattern | `rpm -q "gpg-pubkey-fda02785-*"`, `rpm -q "gpg-pubkey-00000000-*"` | rc=0 present, rc=1 absent |
| Lint | `shellcheck -x repo-setup/sign-rpms.sh`, `shellcheck vm-test/test-repo-setup.sh` | sign-rpms clean; harness warnings only pre-existing (SC1091 lib.sh path, SC2046:248, SC2034:410), none on new lines |
| Pre-push, private key block | `git grep -il "BEGIN PGP PRIVATE KEY BLOCK" HEAD` at `ba7babf` | zero hits (rc=1) |
| Pre-push, passphrase | value loaded from the 600-mode file (never printed), `git show HEAD \| grep -cFf` | 0 matches |

---

## Review

*Owner: `Shadow`. Read-only — findings only, no edits. Severity order, blockers first.*

### Harness ships no `keys/` to the VM; the new setup-repo.sh key step always dies there
**Severity:** blocker
**Where:** `vm-test/test-repo-setup.sh:349-364` (phase 1 copies), `repo-setup/setup-repo.sh:127-130` (new requirement)
**Problem:** phase 1 rsyncs only `repo-setup/` and `rpms/` to the VM, but item 5 added a step to `setup-repo.sh` that requires `${PROJECT_ROOT}/keys/cinnamon-rocky10-public.asc` and dies without it.
**Failure scenario:** fresh VM after phase 1; phase 2 runs `bash ./repo-setup/setup-repo.sh /root/cinnamon-for-rocky10` (test line 392) → the `[ ! -f "$KEY_FILE" ]` test at `setup-repo.sh:128` is true (no `keys/` on the VM) → die at line 129 → cascading FAILs: "setup-repo.sh execution" (test line 408), "completion message" (line 415), ".repo file installed" (line 432), "dnf repolist includes repo" (line 481), phase 4 `dnf install cinnamon` (line 558). The DoD items "Fresh-VM end-to-end" and "Big: all harness checks PASS" are unreachable on this branch as-is.
**Suggested direction:** rsync `keys/` to the VM in phase 1 alongside the existing two copies, and update the header comment at test line 9 and the phase-1 log lines to match. Re-run the harness to green.
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

### sign-rpms.sh verification does not pin the signing key; the summary claim is stronger than the check
**Severity:** should-fix
**Where:** `repo-setup/sign-rpms.sh:245` (per-RPM check), `repo-setup/sign-rpms.sh:257` (final claim)
**Problem:** verification is `rpm --checksig | grep -qi "signatures OK"`, which accepts a valid signature from *any* key in the host rpm keyring, but the script then reports "All RPMs in ... carry a valid signature from ${FPR}".
**Failure scenario:** a host whose rpm keyring holds the project key plus at least one other key (any imported key qualifies); one RPM is swapped for a copy signed by that other key → `rpm --checksig` reports signatures OK → line 245 passes → the script certifies the whole set as signed by `1689676AF4D4F6FEC142B4429C0A8912FDA02785` when it is not. The pre-flight at line 150 proves the project key is present, not that it is the only key in the rpm keyring. The current set is unaffected (signed by the sole secret key in the dedicated keyring, item 3 evidence), but the script's standing guarantee is weaker than its output.
**Suggested direction:** pin the expected signer in the verification step (assert the signing key identity in each RPM's signature data matches the expected fingerprint/keyid) so the line-257 claim matches what was actually checked.
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

### Harness asserts 48 RPMs on the VM; the repo ships 64
**Severity:** should-fix
**Where:** `vm-test/test-repo-setup.sh:369-373`
**Problem:** the "RPMs copied to VM" check asserts exactly 48, but the published set is 64 RPMs.
**Failure scenario:** verified pre-existing on main (`git show 893b22a:vm-test/test-repo-setup.sh` line 366 carries the same `-eq 48`; `git show 893b22a:rpms` lists 64 RPMs), so the check FAILs on every run on either branch: 64 files land on the VM, the count test fails, the suite is red, and the DoD item "Big: all harness checks PASS" cannot be met. The branch already modifies this file (commit `55a38ba`), so the fix belongs here.
**Suggested direction:** raise the constant to 64, or better, derive the expected count from the source tree (count `*.rpm` in `${PROJECT_DIR}/rpms` the same way line 368 counts the remote side) so the assertion cannot go stale again.
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

### Passphrase round-trip check is dead code and its comment is factually wrong
**Severity:** nit
**Where:** `repo-setup/sign-rpms.sh:178-180`
**Problem:** the "round-trip check" compares `xxd -r -p` of the hex encoding against the original, but hex encoding/decoding is an exact identity for any byte sequence (both sides undergo the same command-substitution trailing-newline stripping), so the comparison can never fail and the `die "passphrase file must be a single line"` at line 180 is unreachable; the comment at line 178 ("a multi-line file would not survive the hex round trip") is wrong.
**Failure scenario:** none functionally — that is the point: a multi-line passphrase file passes the check and would work end-to-end through the hex protocol (hex represents every byte), so the documented "single line" invariant (header line 35) is simply never enforced.
**Suggested direction:** either enforce the invariant on the raw file bytes (e.g. newline count in the file) or drop the invariant from the header and delete the check.
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

### `xxd` and `stat` are used but missing from the tool pre-flight
**Severity:** nit
**Where:** `repo-setup/sign-rpms.sh:105-107` (pre-flight loop), first use of `xxd` at line 177
**Problem:** the pre-flight checks `gpg gpg-connect-agent rpm` only, but the script also requires `xxd` (line 177; shipped by `vim-common` on RHEL, not guaranteed on a minimal server) and `stat` (lines 141, 143).
**Failure scenario:** a host without `vim-common` → line 177 aborts under `set -euo pipefail` with the bare shell message "xxd: command not found" and a non-zero rc, instead of the pre-flight's actionable "required tool not found: ..." die.
**Suggested direction:** add `xxd` and `stat` to the pre-flight loop.
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

### `rpm -qa | grep -q` under pipefail is a host-dependent latent false positive in the keyring pre-flight
**Severity:** nit
**Where:** `repo-setup/sign-rpms.sh:150` (with `set -o pipefail` at line 42)
**Problem:** if the `rpm -qa` output exceeds the pipe buffer (~64 KB, i.e. roughly 1300+ installed packages) and the `gpg-pubkey-fda02785-*` line is not the last line, `grep -q` exits as soon as it matches, the next write from `rpm -qa` hits SIGPIPE (rc 141), and pipefail makes the pipeline return 141.
**Failure scenario:** a host that grew past ~1300 packages after the key import → line 150's `if !` sees rc 141 → dies with "public key fda02785 is not in the rpm keyring" although the key is present; the message misdirects the operator to re-import a key that is already there. Not triggered on the release host today (item 3 ran clean; the key's db entry sits near the end of the list, so grep reads to the end) — it is a degradation path, not a current failure.
**Suggested direction:** query the keyring directly with no pipeline, as `repo-setup/setup-repo.sh:139` already does (`rpm -q "gpg-pubkey-<keyid>*"`).
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

### DoD "zero hits" wording is unsatisfiable on a correctly guarded tree
**Severity:** nit
**Where:** Definition of Done, `planning/docs/TASK-0024-rpm-signing-gpgcheck.md:88`
**Problem:** the DoD requires the merged tree to pass `git grep` for `private-keys-v1.d` "with zero hits", but the guard that makes the tree safe is itself the literal pattern line `private-keys-v1.d/` in `.gitignore:22` (verified via `git show feature/TASK-0024-rpm-signing-gpgcheck:.gitignore`), so `git grep private-keys-v1.d` returns exactly one hit on the merged tree.
**Failure scenario:** merge the branch as-is → the literal DoD check fails on a tree that has no key material, because the .gitignore guard line matches the search string.
**Suggested direction:** reword to "zero hits for `BEGIN PGP PRIVATE KEY BLOCK`, and for `private-keys-v1.d` only the `.gitignore` guard line". (DoD is Robotnik's section; flagged here, not edited.)
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

---

**Verified, no finding.** The following were checked and cleared: passphrase handling in `sign-rpms.sh` (read from the 600-mode file, hex-encoded, sent on `gpg-connect-agent` stdin only, never in argv; `PASS`/`PASS_HEX` wiped at lines 181/194; `clear_preset` EXIT trap covers all exit paths, lines 199-208); `setup-repo.sh` statelessness contract (bad argument dies at the `cd -P` resolution, lines 61-62, before the root check at line 78 and every state-changing step, matching the contract at lines 21-28); the `is_signed` grep (lowercase "signatures OK" cannot match the failure string "SIGNATURES NOT OK", lines 213-221); harness test 6's flip to `gpgcheck=1` (asserts the new intended behavior, `vm-test/test-repo-setup.sh:314-323`; the template and the script's printf both carry `gpgcheck=1` with no `gpgkey=`, consistent); the public key file's fingerprint subpacket decodes exactly to `1689676AF4D4F6FEC142B4429C0A8912FDA02785`, and `KEY_ID="fda02785"` is its last 8 hex chars (`repo-setup/setup-repo.sh:42`); `rpms/SHA256SUMS` structure (64 lines, basenames only, 1:1 with the tree listing) plus the commit-range argument that no `rpms/*.rpm` changed after the manifest commit (`git log --stat db60bb6..1b57ac8` and `1b57ac8..e6ee370`), on top of the recorded item 4 evidence (`sha256sum -c` 64/64 OK). Note: the hashes themselves were not independently re-computed — this review has no `sha256sum` permission — so the manifest's correctness rests on the recorded item 4 run plus the commit-range argument.

---

## Security

*Owner: `Omega`. Read-only. Severity order.*

**Review scope.** Branch `feature/TASK-0024-rpm-signing-gpgcheck` (tip `e6ee370`) against main
`893b22a`, 6 commits. Read-only: `git diff`/`git show`/`git grep` against branch objects, `gh` on the
repo, web fetch of metalinux.dev (2026-09-22). No `rpm`, `gpg`, or `sha256sum` in this review's tool
set, so signature and digest claims rest on the recorded item runs, Shadow's `## Review`
verification, and byte inspection of git objects (`git grep -a` is reliable only for patterns
without the 0x0A byte; validated here with control patterns).

### No out-of-band anchor for the signing fingerprint; a key swap is undetectable inside the account
**Severity:** medium
**Vector:** supply-chain
**Where:** `keys/cinnamon-rocky10-public.asc`, `INSTALL.md:188`, `INSTALL.md:282`, `README.md:102`, `repo-setup/setup-repo.sh:38`
**Attack:** the attacker is a compromised `metalllinux` GitHub account (named in the threat model at task origin, this doc line 54). One in-account PR or commit does all of: (a) replace `keys/cinnamon-rocky10-public.asc` with the attacker's public key, (b) re-sign all 64 RPMs with the attacker's key, (c) update the fingerprint strings in `INSTALL.md` and `README.md`, (d) regenerate `rpms/SHA256SUMS`. A follower running `setup-repo.sh` imports the attacker's key into the rpm keyring, `gpgcheck=1` then passes on the attacker's packages, and attacker code runs as root (the threat model states packages install as root). Every in-repo check passes: signatures verify against the shipped (attacker) key, the manifest matches the re-signed RPMs, and the documented manual `rpm --checksig` procedure verifies against whatever key was imported.
**Impact:** RCE as root on every follower who installs from a tag cut after the swap. The signing layer does close the stated `rpms/`-tampering threat with the key held constant (a PR altering only `rpms/` is caught: the altered packages do not verify against the shipped key). The key-swap variant requires the same capability as account compromise, so this is the residual of the named threat, not a hole in the implemented design.
**Evidence for severity.** No out-of-band copy of the fingerprint exists. Checked metalinux.dev homepage and the Linux Journey index (2026-09-22): no article publishes it, and the key (generated 2026-09-21) postdates any Cinnamon article the project could have written. The fingerprint is published only inside `metalllinux` account territory: the project repo (the five locations above) and this planning doc. The user's memory is the only current out-of-band knowledge.
**Fix:** non-blocking; recommended before the first public tag. Publish the fingerprint on metalinux.dev (separate domain and hosting, a distinct trust domain) and add one line to the `INSTALL.md` manual procedure telling the follower to compare the imported key's fingerprint against that out-of-band value before trusting the repo. This converts a silent key swap into a detectable one.
**Resolution:** *(filled by `Tails`)*

### Final verification does not pin the signing key, and the completion log overstates the guarantee
**Severity:** low
**Vector:** crypto
**Where:** `repo-setup/sign-rpms.sh:241-246` (verification loop, die at :245), `repo-setup/sign-rpms.sh:257` (log), `repo-setup/sign-rpms.sh:219-221` (`is_signed`)
**Attack:** `rpm --checksig`/`rpm -K` verifies "a valid signature by a key in the rpm keyring, or by the public key embedded in the package", not "by key 1689...FDA02785". An RPM in `rpms/` re-signed with a key absent from the host's rpm keyring would be accepted through the embedded-key fallback by both the skip check (`is_signed`, :220) and the final verification (:245). Exploiting this needs write access to `rpms/` on the release host (or to the script itself), and an attacker with that capability does not need this path, so the exposure is robustness, not a reachable vulnerability. On the release host the check is in fact pinned: the pre-flight (:150-151) guarantees key `fda02785` is in the rpm keyring before anything runs, so verification resolves by key ID.
**Impact:** a future run against pre-placed re-signed packages would log "All RPMs in rpms/ carry a valid signature from 1689...FDA02785" (:257) for packages that do not carry such a signature. False assurance in recorded evidence, not a broken current signature: for this run the guarantee holds, byte inspection of the committed git objects shows the key-ID tail `fda02785` embedded in the branch blobs (2 hits in the `cinnamon-rocky-defaults` sample) and absent from the main blobs (0 hits).
**Fix:** consolidate with Shadow's should-fix on these same lines (no duplicate work). Pin the key in verification, for example by extracting the embedded public key (`rpm -qp --qf '%{SIGPGP}'`) and comparing its fingerprint to `EXPECTED_FINGERPRINT`, and reword the :257 log to state what was actually checked.
**Resolution:** *(filled by `Tails`)*

### "Never run with set -x" warning is not enforced
**Severity:** low
**Vector:** secrets
**Where:** `repo-setup/sign-rpms.sh:24-26` (warning) versus the script body (no guard)
**Attack:** the header warns that running under `set -x` prints the passphrase via the trace (AGENTS.md section 4), but nothing enforces it. `bash -x repo-setup/sign-rpms.sh` (or a wrapper that sources it into an xtrace shell) traces lines 177 and 179 with the expanded cleartext passphrase (and its hex form) on stderr, because `printf '%s' "$PASS"` and `printf '%s' "$PASS_HEX"` are traced with their arguments expanded. Line 175 (`PASS=$(cat ...)`) does not leak (the trace shows the command, not the substitution result), and the heredoc at :186-190 is not traced.
**Impact:** the passphrase lands in the operator's terminal, shell history, or any captured log of the signing run. Host-local only: the script never runs in CI, output stays on the release host, and the attacker is the operator misusing the script or a local process reading the terminal or log.
**Fix:** refuse to run when xtrace is active, near the top of the script after :42: `case "${BASHOPTS:-}" in *xtrace*) die "refusing to run under set -x: the passphrase would be traced (AGENTS.md section 4)";; esac`.
**Resolution:** *(filled by `Tails`)*

### All 64 signed RPMs are byte-identical in size to the unsigned baseline
**Severity:** low
**Vector:** crypto
**Where:** `rpms/*.rpm` (all 64); `## Implementation` item 3 record
**Attack:** none. This is a records gap, not an attack path. `git diff --stat 893b22a..e6ee370` shows all 64 RPMs as `Bin N -> N` (unchanged size, for example `cinnamon-rocky-defaults-1.0-2.el10.noarch.rpm` 15241 to 15241). Ordinary `rpm --addsign` with an RSA-4096 key grows the file by roughly 1 KB (signature plus embedded public key). The Implementation record attributes the identity to "the signature landing in a fixed header slot", a mechanism this review could not verify (no `rpm`/`gpg` access). Byte inspection of the git objects (patterns without 0x0A, validated by control) confirms the committed branch blobs carry the key-ID tail `fda02785` and the main blobs do not, so the committed bytes do carry a signature from the expected key.
**Impact:** if the size identity ever turned out to mask a malformed signature, the recorded `rpm -K` evidence (item 3, run against exactly these bytes, Shadow verified no `rpms/*.rpm` changed after the manifest commit) would already have failed. The realistic risk is a gap in the evidence trail, not a broken signature.
**Fix:** no code change. The item 14 fresh-clone run should record per-file sizes and the full `rpm --checksig` output in `## Test Results`, closing the anomaly on the record.
**Resolution:** *(filled by `Big` at item 14)*

### Verified, no finding
- **Secrets in history.** `git log -S "BEGIN PGP PRIVATE KEY BLOCK"` on the branch range: 0 hits. `git log -S "private-keys-v1"`: 1 hit, commit `7d47a02`, whose diff scope (via `--stat`) is `.gitignore` +19, `keys/cinnamon-rocky10-public.asc` +30, `sign-rpms.sh` +7/-6, i.e. the guard, not key material. `git log -S "BEGIN PGP"`: only `7d47a02`. The planning doc holds no passphrase value: roughly 100 "passphrase" hits, all mechanism, reference, or byte-length; the user's passphrase is referenced as the contents of `~/password.txt`, never written (AGENTS.md section 4 upheld).
- **No new GitHub secrets or variables.** `gh secret list` and `gh variable list` on `metalllinux/cinnamon-for-rocky10` both return empty. The section 13 exception (host-local keyring, user-approved 2026-09-21, six-pager `planning/docs/TASK-0024-gpg-key-management.md` sections 4-5) adds no workflow secrets, and the project repo has no `.github/`. The precedent cited for the exception, the fleet test SSH key, is verified as claimed at `vm-test/lib.sh:45` and `:85` (host-local key files under `$HOME/.ssh`, not GitHub secrets).
- **Key material shipped is public-only.** `keys/cinnamon-rocky10-public.asc` is a 30-line `PGP PUBLIC KEY BLOCK`; the UID matches the spec; the fingerprint subpacket decodes to `1689676AF4D4F6FEC142B4429C0A8912FDA02785` (Shadow, `## Review`, line 717). `.gitignore` guards cover the keyring directory, passphrase file names, `private-keys-v1.d/`, and `openpgp-revocs.d/` (a leaked revocation cert is a key-revocation DoS, so this is covered).
- **No injection surface in the new scripts.** All expansions reaching the shell are quoted; the `rpms/` glob expands to absolute paths (no leading-dash argument injection); gpg colon output is consumed field-wise and never re-interpreted as shell.
- **License (AGENTS.md section 9).** The diff adds no forked code; no license-header or compatibility concern.

**Verdict.** No security blockers. The medium finding is residual by design of the single-account model, documented in the six-pager risk table, and non-blocking: the signing layer closes the stated `rpms/`-tampering threat, and the key-swap variant is the named account-compromise residual with a documented response (re-key). Recommend merge on security grounds. The out-of-band fingerprint publication should land before the first public tag (follow-up task or a small docs addition; it touches metalinux.dev content, so it is the user's call). Tails must still clear Shadow's Review blocker (the harness ships no `keys/` to the VM, so item 10's test 6 cannot pass) before item 10 runs; that is a Review item, not a Security one.

---

## Test Results

*Owner: `Big`. Verdicts, never raw log dumps.*

**Scope.** Functional verification of the signing + `gpgcheck=1` change on a libvirt VM
(`task0024-tamper`, Rocky Linux 10.2, dnf 4.20.0, rpm 4.19.1.1), branch
`feature/TASK-0024-rpm-signing-gpgcheck` tip `e6ee370`. Signing key
`1689676AF4D4F6FEC142B4429C0A8912FDA02785` (short ID `fda02785`). Two tamper vectors, each with
`createrepo_c --update` so repodata matches the tampered bytes: a payload byte flip (offset 11803,
0x9e to 0x9f) and a PGP-signature byte flip (offset 400, 0x56 to 0x57). This is a signing/repo task,
not a UI task, so Sparky does not apply. Evidence in `/tmp/opencode/task0024/` (host-local, not in the
repo). The VM is destroyed; all artifacts are pulled.

**Checks run (VM functional verification):**

| Check | What it exercises | Result | Notes |
|---|---|---|---|
| Positive control, gpgcheck=1 | pristine signed package installs | PASS | `dnf install` rc=0, `rpm -q` confirms |
| Negative: payload flip, gpgcheck=1 (item 11a) | payload tamper caught by the signature | PASS | `dnf install` rc=1, `does not verify: no signature`; `rpm --test` rc=1, same message |
| Negative: payload flip, gpgcheck=0 (item 11b) | the gap gpgcheck=1 closes | PASS | `dnf install` rc=0, package installs. The old path accepts payload tamper |
| Negative: pgpsig flip, gpgcheck=1 (added) | signature tamper caught | PASS | `dnf install` rc=1, `Header V4 RSA/SHA256 Signature, key ID fda02785: BAD` |
| Negative: pgpsig flip, gpgcheck=0 (added) | corrupted signature under the old path | REFUSED | `dnf install` rc=1, `…Signature: BAD`. dnf4 4.20.0 refuses a present-but-BAD signature even at gpgcheck=0 |
| Negative: unsigned package, gpgcheck=0 (added) | absent signature under the old path | ACCEPTED | `dnf install` rc=0. gpgcheck=0 accepts a package with no signature |
| Fresh-VM full harness (item 10) | end-to-end repo setup + 22-name install + desktop | FAIL | `harness-run1.log`: 16 PASS / 41 FAIL / 2 WARN, `OVERALL: FAIL` |
| "no signature" mechanism | why the payload flip reports "no signature" | RESOLVED | below |

**Checks requested vs run.** Item 11a (payload flip + regenerated repodata, gpgcheck=1 refuses) is
run and PASS; the exact wording is `does not verify: no signature`. Item 11b (the same payload-flipped
package under gpgcheck=0 installs) is run and PASS. Item 11c (the fallback
`dnf install ./rpms/<tampered>.rpm` with the key imported) was NOT run; there is no evidence of it in
the record. The pgpsig-flip and unsigned rows are additional vectors I ran beyond the plan; the
pgpsig-flip result (refused under both gpgcheck settings) refines the plan's assumption that gpgcheck=0
accepts any tampered package, it does not contradict item 11b, whose vector is the payload flip. Item
10 (fresh-VM full harness: 22-name install, GDM Wayland login, five surfaces) is BLOCKED, not run to
completion. Not silently dropped. The harness copies `repo-setup/` but not `keys/` to the VM, so
`setup-repo.sh` dies at the key check (`harness-run1.log:99`, `ERROR: GPG public key not found`) before
any install. This is a harness bug (stays with `Big`) and matches Shadow's Review blocker (`## Review`
line 663) and the Omega note (`## Security` line 776).

**The "no signature" question, resolved.** The payload flip reports `does not verify: no signature`
even though the package is signed and the real failure is the BAD payload digests. The transaction sinfo
table is identical between the pristine and flipped packages except the payload digest rc (pristine
`[5] NOTFOUND, [6] OK, [9] OK`; flipped `[5] BAD, [6] BAD, [9] BAD`), decoded in `gdb-decode.out`
(flipped) and `gdb-decode-4.out` (pristine). The mechanism, from the Rocky `rpmvsVerify` disassembly
(`rpmvsVerify-rocky.dis`):

1. The payload SHA256 digest entry `[6]` is wrapped (`wrapped=1`), so it is promoted to signature
   strength (`testb $0x1,0x50(%rsp)` at `0x51b95`).
2. On a digest OK, the verify sets `verified[type] |= range` and `verified[strength] |= range`
   (`0x51e59` to `0x51e68`). Pristine `[6]` OK sets `verified[SIG]` to `0x3` (HEADER|PAYLOAD); flipped
   `[6]` BAD leaves `verified[SIG]` at `0x1` (HEADER).
3. The second loop's skip condition is `required = sinfo->range & (range & ~verified[SIG])`, skipping a
   `NOTFOUND` entry only when `required == 0` (`andn` at `0x51c0a`). The absent payload DSA/RSA
   signature entries `[7]`/`[8]` (range `0x3`, rc NOTFOUND in both cases):
   - Pristine: `0x3 & (0x3 & ~0x3) = 0`, so skipped.
   - Flipped: `0x3 & (0x3 & ~0x1) = 0x2`, so required and passed to the callback (`0x51c67`).
4. The callback sets `no signature` for the NOTFOUND signature entries and continues past the BAD digest
   entries without overwriting that message (trace `gdb-cb3.out`, final message `no signature`;
   `gdb-cb4.out` shows the pristine run exits 0).
5. `prc` is non-zero because the real failure is the BAD payload digests, and `verifyPackageFiles` adds
   the problem with `vd.msg`, which is `no signature` (`transaction.c:1310` to `1311`).

So the transaction is correctly refused; only the message is masked. A corrupted payload digest fails to
mark the payload range signature-verified, which makes the (absent) payload signatures required, which
triggers the `no signature` callback text. This is an rpm/rpmvs reporting quirk in the wrapped-digest
promotion path, not a defect in this task's code and not a security issue (the refuse is correct). The
Rocky `vfyCb` source is static (not breakable by name) and could not be read directly; its
continue-past-BAD and preserve-`no-signature` behavior is confirmed empirically from the trace.

**Verdict.** The negative tamper test PASSES on the plan's vector. A payload-tampered package with
regenerated repodata is refused under gpgcheck=1 (item 11a) and accepted under gpgcheck=0 (item 11b),
which is exactly the gap the signing + gpgcheck=1 change closes. Two findings to carry forward. First,
dnf4 4.20.0 refuses a present-but-BAD signature even under gpgcheck=0, so gpgcheck=0 is not a blanket
accept for any tampered package, only for payload tamper and for absent signatures. Second, the fresh-VM
full harness (item 10) is blocked by a harness bug: the harness does not ship `keys/` to the VM, so the
positive DoD line (22-name install + working Cinnamon Wayland desktop) is not yet verified. That fix
(copy `keys/` to the VM before `setup-repo.sh` runs) stays with `Big`; it is the only blocker on the
positive DoD line. The "no signature" message is explained and is a reporting quirk, not a code bug.

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
