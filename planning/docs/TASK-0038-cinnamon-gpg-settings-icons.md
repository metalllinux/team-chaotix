# TASK-0038 — Cinnamon for Rocky 10: GPG signing + install, System Settings, icon parity

> **Section order below is fixed.** Each agent writes to its own section and no other. `Robotnik`
> reads only `## Status` and `## Next Actions`. Do not reorder, rename, or remove sections.

- **Created:** 2026-10-24

---

## Status

*Owner: `Robotnik`. Keep this SHORT and CURRENT — it is one of only two sections the PM reads, so a
stale entry means the whole loop runs on bad information.*

**Now (2026-10-24):** Task opened from the operator's report on
`~/Linux/projects/cinnamon-for-rocky10/`. Three problem areas: (1) a consumer that has set up the
Cinnamon repo in `/etc/yum.repos.d` cannot install the RPMs under `gpgcheck=1` (the operator had to
set `gpgcheck=0`), and the install instructions in the repo are wrong; (2) System Settings
(cinnamon-control-center) does not open and its icon is broken; (3) multiple desktop icons differ
from the Fedora 45 Cinnamon baseline. Comparison screenshots live in
`~/Linux/projects/cinnamon-for-rocky10/screenshots/` (`rl10/` vs `f45-beta/`). Signing material:
secret key + passphrase at `~/AI/secrets/` (`gpg-secret-key.asc`, `gpg-passphrase.txt`); tracked
public key at `keys/cinnamon-rocky10-public.asc`. Prior work: TASK-0024 (signing, done), TASK-0027
and TASK-0033 (the host reinstall destroyed the old key; the team generated a new keypair and
republished the `-3` set; `INSTALL.md` records fingerprint
`1689676AF4D4F6FEC142B4429C0A8912FDA02785`).

**Environment / scope:**
- Files in scope: `repo-setup/` (`setup-repo.sh`, `sign-rpms.sh`, `cinnamon-rocky10.repo`),
  `keys/cinnamon-rocky10-public.asc`, `INSTALL.md`, `README.md`, `rpms/` (published set +
  `repodata/`), and the System Settings / icon packages (cinnamon-control-center, cinnamon, icon
  theme).
- Touches the DB schema: no
- Graphical UI: yes (System Settings launch + desktop icons; screenshot/Sparky verification)
- Rocky Linux target: yes

**Unknowns:**
- Root cause of the `gpgcheck=1` failure (not yet established): a key/signature mismatch (old vs
  new signing key), a missing key import on the consumer path, or an RPM that is unsigned in the
  consumer's copy.
- Whether the tracked public key and the recorded fingerprint are currently consistent with the
  key that signed the `-3` republish (a new keypair was generated in TASK-0033).
- The exact cause of System Settings not launching and of its broken icon.
- The full list of icon differences (to be enumerated from the screenshots).

---

## Definition of Done

*Owner: `Robotnik`, and nobody else. Written **before** any work starts. Objectively checkable —
if a box cannot be verified by looking at something, rewrite it.*

GPG signing and install:
- [ ] Root cause of the `gpgcheck=1` failure identified and recorded in `## Implementation` (which
  key signed each RPM, vs the key in `keys/cinnamon-rocky10-public.asc`, vs the fingerprint recorded
  in `INSTALL.md`, and whether the key import is missing from the documented consumer path).
- [ ] Signature/key consistency: every published RPM in `rpms/` (the 64 set plus the `-3`
  republish) verifies against the tracked public key (`rpm --checksig` / `rpm -K` all OK; output
  in `## Test Results`).
- [ ] The fingerprint recorded in `INSTALL.md` equals the fingerprint of
  `keys/cinnamon-rocky10-public.asc` and of the key that signed the RPMs (recorded).
- [ ] Fresh-consumer end-to-end: on a fresh Rocky 10.2 consumer VM, following only the documented
  procedure (`setup-repo.sh` or the `INSTALL.md` manual steps, `gpgcheck=1`, no `gpgcheck=0`), the
  full RPM set installs and dnf verifies signatures (evidence in `## Test Results`).
- [ ] Negative test still holds: dnf refuses a tampered RPM under `gpgcheck=1` (recorded).
- [ ] Install instructions accurate: the repo file, `baseurl`, the key import step, and the
  `dnf install` package set in `INSTALL.md` / `setup-repo.sh` are internally consistent and match
  the published set (no stale fingerprint, no wrong path, no unsubstituted placeholder in the
  documented path).

System Settings:
- [ ] System Settings (cinnamon-control-center) launches without crashing on the Rocky 10 Cinnamon
  VM and its window renders (screenshot + evidence in `## Test Results`).
- [ ] The System Settings icon renders correctly (not broken/missing), matching the F45 Cinnamon
  baseline (screenshot evidence).

Icon parity:
- [ ] Every icon that differs between `screenshots/rl10` and `screenshots/f45-beta` is either fixed
  to match the F45 Cinnamon baseline or documented in `## Implementation` as an accepted difference
  with reason + evidence. At minimum these must match: the menu button icon, the desktop icons
  (Computer / Home / Rubbish Bin), and the panel icons.

Review chain and release:
- [ ] `Shadow`: no unresolved blockers or should-fix findings in `## Review`
- [ ] `Omega`: no unresolved findings above `low` in `## Security`
- [ ] `Big`: all harness checks PASS, no silently dropped checks (fresh-VM `gpgcheck=1` install,
  desktop boot, System Settings launch, icon verification)
- [ ] `Charmy`: no unresolved findings in `## License (Charmy)`
- [ ] `Flicky`: gate outcome `PASS`, or a `POLICY_EXCEPTION` recorded in `## License Audit (Flicky)`
- [ ] `Vector`: `INSTALL.md` / `README` updated to match the shipped reality

---

## Next Actions

*Owner: whoever wrote last. The future only — delete what has been done. The second of the two sections
the PM reads.*

- [ ] `Amy`: write `## Plan` — root-cause hypotheses for the three problem areas, work breakdown,
  fresh-consumer-VM validation, and rollback. Read `## Status`, `## Definition of Done`, and this
  section first. Signing material is at `~/AI/secrets/`; comparison screenshots are at
  `~/Linux/projects/cinnamon-for-rocky10/screenshots/`.

---

## Plan

*Owner: `Amy`.*

**Why this task exists** — the operator could not install the published Cinnamon set with signature verification. On a consumer that had the repo set up per the docs, dnf refused packages under `gpgcheck=1` (the operator had to set `gpgcheck=0`), and the docs themselves record a key that is not the one in the repo. System Settings (cinnamon-control-center) also does not open on the Rocky 10 desktop and its icon is broken, and desktop icons differ from the Fedora 45 Cinnamon baseline (one screenshot per environment under `screenshots/`). The task serves the project goal. A Cinnamon desktop on Rocky 10 that consumers install with signature verification, with UI parity to F45.

**What it unblocks / what blocks it**
Unblocks. The trusted consumer install path (the foundation of every future update and republish), a working System Settings, icon parity, and the new tag `v1.0.1` for Knuckles to release.
Blocks, all local or in-repo:
- Re-signing needs the secret key and passphrase. Present at `~/AI/secrets/gpg-secret-key.asc` and `~/AI/secrets/gpg-passphrase.txt` (paths only, values never read in this session). The dedicated keyring `~/.gnupg-cinnamon-rocky10` is absent after the host reinstall. Recreating it is mechanical (item 4).
- Fresh-VM validation needs the cloud image at `/var/lib/libvirt/images/cinnamon-test/Rocky-10-GenericCloud.qcow2` (`vm-test/provision-vm.sh:38`, `vm-test/lib.sh:72`). Neither the directory nor the file exists. One-time download from the Rocky image site (the team's known-good URL and sha256 are in the team AGENTS.md section 12; the expected filename differs from the team golden name, Tails reconciles and records the sha256). The team golden image `/var/lib/libvirt/images/rocky-10-golden.qcow2` is also missing, so the team `scripts/vm-create` is unusable for this task. The project harness is the path.
- If a fix needs an RPM rebuild, the build environment (build deps, `spec/`, `src/`, component sources) must be restored on the reinstalled host. Status unknown (risk R3).
- Outside the repo. `INSTALL.md` tells consumers to compare the fingerprint against the out-of-band publication on metalinux.dev. The site must carry the new fingerprint `2274BFE1BF28C051CD98675BEBD13108EB7FEF99`. The operator updates the site. Recorded in ## Status, not asked.

**MVP** — the GPG fix plus the accurate consumer path. Every published RPM verifies against the tracked key, and a fresh consumer VM installs the 22-name set under `gpgcheck=1` following only the docs (the DoD GPG items). That alone restores the product's core value. Without it the System Settings and icon fixes cannot reach a consumer. Then the System Settings launch and icon fixes, then full icon parity from the diff list. Deferred to the tail of the critical path. Icon parity items beyond the DoD minimum list (menu button, desktop icons Computer/Home/Rubbish Bin, panel icons). They ship in the same tag if ready. Anything not fixable ships as a documented accepted difference, which the DoD allows.

**What this makes harder later.**
- Re-signing in place adds a second (new-key) signature to the 64 old-signed files. The old signature remains in the file bytes. A consumer holding only the new key must still accept the dual-signed file (item 5 carries the empirical sub-check. If rpm requires every signature to verify, the alternatives are a rebuild or publishing the old public key).
- The old public key (fingerprint `1689676AF4D4F6FEC142B4429C0A8912FDA02785`) stays in the `v1.0.0` tree. Anyone pinned to `v1.0.0` still verifies against it. The new tag is the only forward path. The docs must point consumers at the latest tag.
- Dropping the leftover csd 6.7.2-2 triplet changes the published bytes (67 to 64 files). Consumers with -2 installed get -3 as an update, which is fine. The raw -2 bytes then remain only at `v1.0.0` and in the item-1 snapshot.
- Every future System Settings or icon change inside an RPM is a rebuild, re-sign, new-tag cycle. The build path must stay reproducible. Record it under `spec/`.
- The working-tree git repo is broken (F9). If not repaired now, the next task inherits an unverifiable tree.

**Facts (verified 2026-10-24, with the command that produced each)**
- F1. The tracked key `keys/cinnamon-rocky10-public.asc` is primary keyid `EBD13108EB7FEF99` (fingerprint `2274BFE1BF28C051CD98675BEBD13108EB7FEF99`) plus signing subkey keyid `14CF2C0A8A47323C` (fingerprint `CD4958E1A421CBD6B56B7C5614CF2C0A8A47323C`), uid `metallinux Cinnamon for Rocky Linux (repo signing) <repo-signing@metalinux.dev>`, created 2026-10-19. Command: `gpg --with-colons --list-keys` against a throwaway keyring holding only that file.
- F2. `~/AI/secrets/gpg-secret-key.asc` is exactly that key (same primary and subkey). Command: `gpg --show-keys --with-colons` on the file.
- F3. `repo-setup/sign-rpms.sh:66` holds `EXPECTED_FINGERPRINT="2274BFE1BF28C051CD98675BEBD13108EB7FEF99"` = the tracked key. The script signs with the signing subkey (`sign-rpms.sh:146-157`) and reads the passphrase only from `~/.gnupg-cinnamon-rocky10.passphrase/passphrase` (never echoed, refuses under `set -x`).
- F4. Per-file signatures, all 67 files in `rpms/`. 64 files signed with the old key (64-bit keyid `9C0A8912FDA02785`, short form `fda02785`, fingerprint `1689676AF4D4F6FEC142B4429C0A8912FDA02785`). The 3 csd 6.7.2-3 files signed with keyid `14CF2C0A8A47323C` = the tracked key's signing subkey. Commands: `rpm -qpi <file> | grep -i 'key ID'` and `rpm -K <file>` per file. The full table is recorded in ## Implementation by item 3.
- F5. The host rpm keyring holds `gpg-pubkey-eb7fef99-6ad5798e` (the tracked key) plus three unattributed `gpg-pubkey` packages (`6fedfc85`, `d38b4796`, `e37ed158`). It does not hold the old key (`fda02785`). Command: `rpm -qa | grep -i gpg`.
- F6. The old key's public half survives in git history. `git show v1.0.0:keys/cinnamon-rocky10-public.asc` exports it (fingerprint `1689676AF4D4F6FEC142B4429C0A8912FDA02785`, created 2026-09-21). The `v1.0.0` tree is internally consistent (old key file, 64 old-signed RPMs, docs recording the old fingerprint).
- F7. Working-tree `rpms/` = 67 .rpm files + `SHA256SUMS` (67 lines) = the `v1.0.0` set (64 rpm + `SHA256SUMS`) plus the csd-3 triplet. The republish left the old csd 6.7.2-2 triplet published. `INSTALL.md` says "64 RPMs" (lines 5, 228, 251), stale against 67. Self-consistent again after the -2 triplet is dropped.
- F8. Stale key records. Fingerprint `1689676A…` at `INSTALL.md:188`, `INSTALL.md:283`, `README.md:156`. `setup-repo.sh:42` holds `KEY_ID="fda02785"` (comments at :37-41). The `setup-repo.sh` assertion at :139-141 (`rpm -q gpg-pubkey-fda02785*`) fails after the tracked key is imported, so **the tracked `setup-repo.sh` aborts on every fresh consumer before writing the repo file**, independent of the signature state.
- F9. The git repo is broken. `HEAD` points at `refs/heads/main` but `git log`/`git status` fail (`fatal: bad object HEAD`). The local ref `feature/TASK-0024-rpm-signing-gpgcheck` points at a missing object. `git fetch origin` fails (`fatal: unresolved deltas left after unpacking`). Remote refs (ls-remote): `main` = `8d41fc99`, `feature/TASK-0027-csd-3-signed-republish` = `b2d7a49f`, `feature/TASK-0016/0017/0024`, tag `v1.0.0` = `954c14a0` (objects local). The working tree's relationship to the remote refs is unknown until the fetch is repaired (item 2).
- F10. `rpms/cinnamon-settings-daemon-6.7.2-3…rpm` and `rpms-local/cinnamon-settings-daemon-6.7.2-3…rpm` differ (sha256 `b1b39b…` vs `7ee128…`). `rpms-local/` also holds `cinnamon-6.7.4-4` (a local build newer than the published -3).
- F11. VM state. One VM running, `Fedora_45_Cinnamon_Howards` (the F45 baseline, read-only for this task). No Rocky Cinnamon VM defined. Project harness: `vm-test/provision-vm.sh` (cloud image + virt-customize, SSH keys only, idempotent `--destroy`, `--name` default `cinnamon-test-vm` per `vm-test/lib.sh:43`, image dir `/var/lib/libvirt/images/cinnamon-test` per `vm-test/lib.sh:72`), `vm-test/run-tests.sh` (copies `rpms/` to the VM, installs via dnf direct).
- F12. Screenshots. Exactly one per environment. `screenshots/rl10/2026-10-24/Screenshot 2026-10-24 20-35-44.210.png`, `screenshots/f45-beta/2026-10-24/Screenshot 2026-10-24 20-36-49.511.png`.
- F13. Host dnf is broken for any repo operation. `/etc/yum.repos.d/cinnamon-rocky10.repo` is enabled on the host pointing at the project `rpms/`, but the tree has no `repodata/` (untracked by design, `.gitignore:13`). Any dnf command touching that repo fails until `createrepo_c` generates `repodata/` or the repo is disabled.
- F14. The `origin` remote URL in the local `.git/config` embeds a GitHub PAT (machine-local, not committed). Flagged for ## Security (Omega). The value is not recorded here.
- F15. `adwaita-icon-theme` (0:46.0-3.el10) is available in the EL10 base repos on this host (the same repos a fresh consumer sees). A candidate no-rebuild fix path for missing icons.
- F16. Root cause of the `gpgcheck=1` failure, from F4 + F5 + F8. A consumer following either documented path imports the tracked key (the new key), but every package in the 22-name install set is signed with the old key, whose public half is no longer published. dnf under `gpgcheck=1` therefore refuses them. In addition, `setup-repo.sh` aborts at its stale `KEY_ID` assertion (F8) even before an install. The documented install has been broken for every consumer since the TASK-0027 republish. This matches the operator's report exactly.

**Hypotheses (open, for Tails to confirm; not facts)**
- H1. The working-tree `rpms/`/`keys/`/docs may differ from what the remote carries (`main`, `feature/TASK-0027-csd-3-signed-republish`). The fetch failure (F9) blocks the comparison. `rpms-local/` already differs from the published csd-3 file (F10). Item 2 establishes the canonical bytes.
- H2. The System Settings launch failure is a runtime crash (missing dependency, missing gsettings schema, or a D-Bus API skew between cinnamon-control-center 6.7.2-1 and settings-daemon 6.7.2-3). Unknown until reproduced on a fresh VM (item 7). The broken icon is a separate symptom, most likely a missing icon theme asset (no icon theme package in the 22-name set) or a wrong `Icon=` reference.
- H3. The icon parity differences are fixable without a rebuild (adding `adwaita-icon-theme` per F15 to the documented install set, or config in `cinnamon-rocky-defaults`, which per `INSTALL.md` sets the menu button logo). Per-icon confirmation is items 6 and 8.

**Work breakdown** — decomposed until one agent finishes one item in one turn.

| # | Item | Owner agent | Acceptance criterion | Parallel with |
|---|---|---|---|---|
| 1 | Snapshot the pre-change state. Tarball of the project tree (including `rpms/`, `keys/`) plus a sha256 manifest of every file in `rpms/`, plus a `git show-ref`/`ls-remote` dump, to a persistent location. Path recorded in ## Implementation | Tails | Snapshot exists, manifest line count == file count, path recorded | — (first; before any change, including git repair and VM provisioning) |
| 2 | Repair the git state and establish canonical bytes. Retry `git fetch` (on failure: `git gc`, or re-clone to a temp dir and reconcile). Compare the working-tree `rpms/`, `keys/`, and docs against remote `main`, `feature/TASK-0027-csd-3-signed-republish`, and `v1.0.0` per file (blob cmp). Fix HEAD so `git status`/`git log` work | Tails | Per-ref match table in ## Implementation, `git status` exits 0, canonical-bytes decision recorded | after 1; independent of 3, 4, 6, 7 |
| 3 | Complete the per-file signature audit. Every file's signer key ID via `rpm -qpi` (the `%{SIGPGP:pgpsig}` queryformat returns empty on this rpm 4.19 and must not be used). Verify each file's signature against (a) a scratch keyring holding only the tracked key, (b) a scratch keyring holding only the old key (export per F6). Record the full table in ## Implementation | Tails | Per-file table in ## Implementation matches F4 (64 old / 3 new) or corrects it with evidence | after 1; independent of 2, 4, 6, 7 |
| 4 | Recreate the dedicated signing keyring from `~/AI/secrets` (no values echoed). `~/.gnupg-cinnamon-rocky10` (700, secret key imported), `~/.gnupg-cinnamon-rocky10.passphrase` (700) + `passphrase` (600, by `cp`, no cat/echo). `sign-rpms.sh` preflight passes the keyring checks without signing | Tails | Preflight reaches the rpms/ step; keyring fingerprint == `sign-rpms.sh:66` | after 1; independent of 2, 3, 6, 7 |
| 5 | Re-sign and repair the published set (Option A, recommended). Sign on a staging copy: `rpm --addsign` (via item-4 keyring, `sign-rpms.sh` protocol) on every file lacking a tracked-key signature. Sub-check on the copy first: consumer simulation holding only the tracked key (`rpm -K`, plus dnf `gpgcheck=1` if a host consumer exists) passes for every file, and dual-signature behavior is recorded in ## Implementation. Drop the csd 6.7.2-2 triplet. Regenerate `SHA256SUMS` (64 lines). Swap the staging set into `rpms/` only after the sub-check passes. If it fails: Option B (publish the old public key per F6, no byte change) or a rebuild, decision recorded | Tails | Every file in `rpms/` verifies against the tracked key only. `sha256sum -c SHA256SUMS` → 64 OK. File count == 64. Mechanism decision (A or B) recorded | after 3, 4; independent of 6, 7 (converges at 9/10) |
| 6 | Enumerate icon differences. Read both screenshots (multimodal). Per-difference list: menu button icon, desktop icons (Computer/Home/Rubbish Bin), panel icons, anything else. Each: where, what rl10 shows, what f45-beta shows, suspected source (package/asset) | Tails | Diff list in ## Implementation covers every DoD minimum icon | after 1; independent of 2, 3, 4, 5, 7 |
| 7 | Root-cause System Settings. Download the cloud image to the harness path (blocker note above). Provision a fresh VM (`vm-test/provision-vm.sh`). Install the set via the direct-RPM path (`vm-test/run-tests.sh`, works without keys). Reproduce the launch failure (`cinnamon-control-center` from a terminal + `journalctl` + `coredumpctl`). Record root cause and the minimal fix | Tails | Root cause + chosen fix in ## Implementation with log evidence | after 1; independent of 2, 3, 4, 5, 6 |
| 8 | Implement the System Settings launch fix and the icon fixes (item-6 list). Config-only, dependency additions (e.g. `adwaita-icon-theme` per F15), or package rebuilds (verify `spec/` + `src/` build deps first). Sign affected RPMs with the recreated keyring. Fold into the set | Tails | System Settings launches and renders its window on the VM (screenshot). Each icon difference fixed (screenshot) or documented as an accepted difference with evidence | after 4, 6, 7 |
| 9 | Update docs and scripts for the final key and set. `INSTALL.md:188`/`:283` fingerprint → `2274BFE1…`, `README.md:156`, `setup-repo.sh:37-42` `KEY_ID="eb7fef99"` (last 8 of the fingerprint; the host package is `gpg-pubkey-eb7fef99-…`), "Verifying the release" clone tag → `v1.0.1`, verify the "64 RPMs" count. Grep audit: no unannotated old-fingerprint or `fda02785` reference remains | Tails | Grep audit clean; docs match the published state byte for byte | after 5, 8 |
| 10 | Republish. Commit all changes (`rpms/`, `keys/`, `repo-setup/`, `INSTALL.md`, `README.md`), push to a `feature/TASK-0038-…` branch, new tag `v1.0.1` (forward-only, no history rewrite). Record tag + commit in ## Release | Knuckles | Remote tag `v1.0.1` exists; fresh clone at the tag reproduces the bytes (`sha256sum -c SHA256SUMS` all OK) | after 9 |
| 11 | Fresh-consumer VM acceptance. A second fresh VM (`vm-test/provision-vm.sh --name <new>`). Follow only the documented path (`setup-repo.sh` or the manual steps), `gpgcheck=1`, no `gpgcheck=0`, the 22 names + `gdm`/`gnome-shell`, boot, Wayland login. Negative test: a 1-byte-flipped copy of an RPM in a separate test repo dir with its own `repodata/`; dnf under `gpgcheck=1` must refuse it | Big | DoD GPG items (fresh install + negative test) PASS in ## Test Results with evidence | after 10 |
| 12 | System Settings + icon verification on the acceptance VM. Launch from the menu, window screenshot. Desktop screenshot vs `f45-beta`. Every DoD minimum icon matches or is documented | Big | DoD System Settings + icon parity items PASS in ## Test Results | after 11 |
| 13 | Review chain. Shadow → Omega → Big → Charmy → Flicky | each | DoD review-chain boxes | after 12 |
| 14 | Docs final pass. `INSTALL.md`/`README` match the shipped reality (tag, fingerprint, package tables, counts, out-of-band note) | Vector | ## Docs section filled | after 13 |
| 15 | Release record. DONE checklist, branch/commits (GPG-signed), PR (internal, metalllinux, autonomous), tag `v1.0.1` | Knuckles | ## Release filled; PR merged | after 14 |

**Estimates** — agent turns (one item is one turn unless noted).

| Item | O | M | P |
|---|---|---|---|
| 1 | 1 | 1 | 1 |
| 2 | 1 | 1 | 3 |
| 3 | 1 | 1 | 2 |
| 4 | 1 | 1 | 1 |
| 5 | 1 | 2 | 5 |
| 6 | 1 | 1 | 1 |
| 7 | 1 | 2 | 5 |
| 8 | 1 | 2 | 6 |
| 9 | 1 | 1 | 1 |
| 10 | 1 | 1 | 2 |
| 11 | 2 | 3 | 5 |
| 12 | 1 | 1 | 2 |
| 13 | 4 | 5 | 7 |
| 14 | 1 | 1 | 2 |
| 15 | 1 | 1 | 1 |
| **Total** | **17** | **22** | **45** |

T = (O + 4M + P) / 6 = (17 + 88 + 45) / 6 = **25 turns**.
Buffer. +30% for the two unknowns (the H2 diagnosis, the build environment) → plan at ~32 turns.
Wall clock. VM provisioning + boot is ~10-20 min each, outside the turn count. Two task VMs max (one slot is the baseline).

**Risks**
| # | Risk | L | I | Mitigation | Contingency |
|---|---|---|---|---|---|
| R1 | H2 System Settings root cause unknown; fix may need multi-package rebuilds | medium | high (blocks the republish) | Reproduce before fixing (item 7). Prefer config-only. Probe the build env early | If the build env cannot be restored: ship the GPG + icon fixes in v1.0.1, record the launch failure as a blocker in ## Status, continue (no task split without evidence) |
| R2 | Dual-signed files (old + new signature) may not pass a consumer holding only the new key, if rpm verifies every signature | medium | high (invalidates the re-sign mechanism) | Item-5 sub-check on copies against a consumer keyring holding only the tracked key | Option B (publish the old public key per F6, no RPM byte change) or a full rebuild |
| R3 | Build environment (build deps, `spec/`, `src/`) unverified after the reinstall | medium | high | Probe by building the smallest affected spec (e.g. `cinnamon-rocky-defaults`, noarch) before committing | As R1 |
| R4 | Git repair may show working tree ≠ remote (unpushed work or lost pushes) | low-medium | high (wrong bytes published) | Item-1 snapshot before any change; item 2 establishes the match before the republish | Restore from the snapshot, re-run item 2 |
| R5 | Secret leak during keyring recreation / signing | low | critical | Only the `sign-rpms.sh` protocol touches the passphrase (preset via `gpg-connect-agent`, never echoed, refuses under `set -x`); keyring dir 700, passphrase file 600; no secret value in docs or commits; Omega reviews | On leak: rotate (new keypair). Blast radius is the signing trust of the entire published set |
| R6 | VM capacity and host disk (4 vCPU/8 GB per VM, max 3; the worn 40 GB disk) | low | low-medium | Two task VMs max; destroy after use; one-time cloud image download | Reuse a single VM sequentially (item 7 then destroy, item 11 re-provisions) |
| R7 | Out-of-band fingerprint on metalinux.dev is stale (old key) | certain until the operator updates | low (fail-safe: a comparing consumer refuses correctly) | Record the operator action in ## Status | — |

**Dependencies and sequence**
Genuinely ordered. 1 before everything (the snapshot precedes any change, including git repair). 3+4 before 5 (no re-sign without the audit and the keyring). 5+8 before 9 (docs describe the final set). 9 before 10 (docs commit with the tree; the tag name is known in advance, the process fixes the next number after v1.0.0). 10 before 11 (the acceptance test exercises the published tag and docs). 11 before 12 (same VM, one slot). 12 before 13 (the chain reviews the shipped state). 13 before 14. 14 before 15.
Only look ordered, are actually independent. After 1, items 2, 3, 4, 6, 7 are mutually independent (the single inference slot serializes execution; their order along the critical path is free). The GPG track (2, 3, 4, 5) and the System Settings / icons track (6, 7, 8) are independent and converge at 9/10. Items 6 and 7 may swap (item 8 needs both the 6-list and the 7-diagnosis; item 6 needs only the already-captured screenshots).
VMs. Item 7's VM and item 11's VM use different names and can both run (capacity 3, one slot is the baseline). Item 12 reuses item 11's VM.

**Critical path:** 1 → 7 → 8 → 9 → 10 → 11 → 12 → 13 → 14 → 15, with the GPG track 1 → 2/3/4 → 5 → 9 converging at 9. The critical path is the System Settings / icons track when item 7's diagnosis outlasts the GPG track (likely: H2 is unknown and 8 may need rebuilds). Expected length ~16 M-turns (1+2+2+1+1+3+1+4+1+1).

**Validation:**
Files. `rpms/*.rpm` (64), `rpms/SHA256SUMS` (64 lines), `keys/cinnamon-rocky10-public.asc` (fingerprint `2274BFE1…`, unchanged), `repo-setup/setup-repo.sh` (`KEY_ID="eb7fef99"`), `repo-setup/sign-rpms.sh` (`EXPECTED_FINGERPRINT` unchanged), `INSTALL.md`, `README.md`, `vm-test/install-set.txt` (22 names; must still match the installed set).
Checks.
1. Per-file signer. Every file's `rpm -qpi | grep -i 'key ID'` shows `14cf2c0a8a47323c` (the signing subkey), or the recorded dual-signature behavior. No file signed only by `fda02785`, no unsigned file. (The `%{SIGPGP:pgpsig}` queryformat returns empty on this rpm 4.19; do not use that route.)
2. Host consumer simulation. The host keyring already holds the tracked key (F5). `rpm -K` on every file → `digests signatures OK` for the new-key signature; dual-signature behavior recorded (R2).
3. `cd rpms && sha256sum -c SHA256SUMS` → 64 OK.
4. Fresh consumer VM. `setup-repo.sh` → `=== Repository setup complete ===` exit 0. `dnf install` of the 22 names (`vm-test/install-set.txt`) under `gpgcheck=1`. `dnf install gdm gnome-shell`. Boot. GDM login as Cinnamon (Wayland). `loginctl` session `Type=wayland`.
5. Negative test. 1-byte-flipped copy of an RPM in a separate test repo dir with its own `repodata/`; dnf under `gpgcheck=1` refuses it.
6. System Settings. Launch from the menu (screenshot) and `cinnamon-control-center` from a terminal. No crash, no `journalctl` errors, window renders (screenshot).
7. Icons. Desktop screenshot from the acceptance VM. The item-6 diff list fully resolved (fixed, or documented accepted differences). At minimum the menu button icon, the desktop icons (Computer/Home/Rubbish Bin), and the panel icons match `f45-beta`.
8. Regression. `vm-test/run-tests.sh` (direct-RPM path) still passes on a fresh VM.
VMs. Fresh Rocky 10.2 consumer VMs via `vm-test/provision-vm.sh` (cloud image per the blocker note). Item 7's VM is the default name `cinnamon-test-vm`; item 11's VM a fresh `--name`. Screenshots via `virsh screenshot`/VNC. `Fedora_45_Cinnamon_Howards` is the read-only baseline; never modify it.
Human look (operator). (a) the acceptance VM desktop screenshot, (b) the System Settings window screenshot, (c) the icon diff screenshots next to `f45-beta`, (d) the planning doc `## Test Results` and the PR at tag `v1.0.1`. The agents read the screenshots with `read` and record what they show; the operator confirms the final parity.

**Rollback:**
Detection. Any DoD check fails (per-file audit, host `rpm -K`, fresh-VM `gpgcheck=1` install, negative test, System Settings launch, icon diff list). Canary: `dnf makecache` on the acceptance VM.
Exact revert.
- Local tree. Restore the item-1 snapshot tarball over the tree (the manifest verifies the restore).
- Host rpm keyring. No change expected (the tracked key is already imported per F5). If the task added a key, remove it with `rpm -e gpg-pubkey-<keyid8>-*`. The three unattributed packages (F5) predate this task; leave them, note for Omega.
- Generated `rpms/repodata/`. Delete if created (untracked, `.gitignore:13`).
- The dedicated keyring. Leave it (host-local, needed for future signing; not repo state).
- Remote. The new branch and tag `v1.0.1` are additive. Revert = `git push origin :refs/heads/feature/TASK-0038-…` and `git push origin :refs/tags/v1.0.1`. Consumers who installed from `v1.0.1` in the meantime: `dnf remove` the Cinnamon set and reinstall from the corrected tag; record the blast radius in ## Status.
- VMs. `vm-test/provision-vm.sh --destroy-only` per VM.
Point of no return. Publishing the new RPM bytes to the remote (tag `v1.0.1`). After that, consumers who pulled them cannot get the previous bytes from that tag; the old bytes survive only at `v1.0.0` and in the item-1 snapshot. No history rewrite or force push in this plan (forward-only tags). VM destruction after screenshots is also irreversible.
State a failed run leaves behind (a retry must tolerate). A half-provisioned VM (harness `--destroy` is idempotent). An already-imported key (re-import is a no-op per the script's comment). `repodata/` generated in the tree (delete to re-test the generation path). A staging signing dir under /tmp (disposable). The signing works on copies first (item 5), so `rpms/` is never half-signed.

---

## Implementation

*Owner: `Tails`.*

**Alternatives considered**

### Problem: where the item-1 snapshot lives, and what the tarball covers
**Option A — home-dir location outside the project tree (`/home/howard/snapshots/TASK-0038/`), tarball = whole tree minus top-level `.git`** · How: `tar -czf … --exclude='./.git' -C <project> .`, plus a `sha256sum` manifest of `rpms/`, plus the git ref dumps. Pros: persistent (`df -h /home/howard` showed 780G free on `/home`), outside the tree so a rollback restore cannot clobber the snapshot's own manifest, outside any git index. Cons: none.
**Option B — inside the project tree or under `/tmp`** · How: same contents in-tree. Pros: none. Cons: `/tmp` is not persistent (the plan says persistent location); an in-tree path pollutes the tarball and the restore.
**Option C — exclude every `.git` directory from the tarball (top-level and nested)** · How: `--exclude='.git'` (basename match). Pros: smaller archive. Cons: ten component directories (`cinnamon/`, `cinnamon-control-center/`, `muffin/`, `nemo/`, `cjs/`, `xapps/`, `cinnamon-settings-daemon/`, `cinnamon-session/`, `cinnamon-menus/`, `cinnamon-desktop/`) each hold their own `.git`, and the plan's rollback restores the tree byte for byte, so the nested git state must be included. First build used this exclude; the tree-vs-tar diff caught it (12843 tar file entries vs 13512 tree files, 669 missing = the nested `.git` trees) and the tarball was rebuilt.
**Chosen:** A, excluding only the top-level `.git` (the pattern `./.git` contains a slash, so GNU tar matches it against the full entry name and leaves the nested `.git` dirs in place). Because the plan's Rollback section restores "the item-1 snapshot tarball over the tree", and item 2 re-establishes the top-level git state from the ref dumps.
**Competing priorities:** none. Item 1 is read-only; no project-tree file was written.

### Item 1 — pre-change state snapshot (done 2026-10-25)

Path (persistent, outside the project tree): `/home/howard/snapshots/TASK-0038/`. Taken 2026-10-25 at the start of item 1, before any change made by this task (before git repair, before VM provisioning, before re-signing).

| Artifact | Path | Command / evidence |
|---|---|---|
| Tree tarball (whole tree, top-level `.git` excluded, 493857868 bytes) | `/home/howard/snapshots/TASK-0038/tree-20261025-000945.tar.gz` | `tar -czf … --exclude='./.git' -C /home/howard/Linux/projects/cinnamon-for-rocky10 .` |
| `rpms/` manifest, all 68 files | `/home/howard/snapshots/TASK-0038/rpms.sha256` | from the project root, `find rpms -type f -print0 \| LC_ALL=C sort -z \| xargs -0 sha256sum` |
| `git show-ref` dump | `/home/howard/snapshots/TASK-0038/git-show-ref.txt` | `git show-ref` (exit 0) |
| `git ls-remote origin` dump | `/home/howard/snapshots/TASK-0038/git-ls-remote.txt` | `git ls-remote origin` (exit 0) |
| `git status` output | `/home/howard/snapshots/TASK-0038/git-status.txt` | `git status` (exit 128, `error: bad tree object HEAD`; F9, pre-existing) |
| `git log -1` output | `/home/howard/snapshots/TASK-0038/git-log-1.txt` | `git log -1 --oneline` (exit 128) |
| Remote URL with userinfo redacted | `/home/howard/snapshots/TASK-0038/remote-url-redacted.txt` | `git config --get remote.origin.url` piped through a sed that masks the userinfo (F14; the token value is never recorded) |
| Tarball checksum | `/home/howard/snapshots/TASK-0038/tree-20261025-000945.tar.gz.sha256` | `sha256sum` on the tarball |

New evidence for item 2, from the dumps above (hypotheses stay hypotheses until item 2 runs):
- Local `refs/heads/main` = `8d41fc99a1da0be80d9b07b4dc060904579cc89d`, equal to remote `main` and remote `HEAD` per `git ls-remote origin`; every other local branch ref matches its remote sha byte for byte.
- `git log -1 --oneline` fails with `Could not read b59da1298836e266916782ef6f079f1626501705` then `Failed to traverse parents of commit 8d41fc99…`, i.e. the local refs are intact and the object store is what is missing (consistent with F9's broken fetch).
- `rpms/` holds 68 files (67 `.rpm` + `SHA256SUMS`), consistent with F7.
- Component sizes for context: top-level `.git` 469M, `rpms/` 217M, `rpms-local/` 2.5M, tree total 1.6G (command `du -sh .git rpms rpms-local keys spec src screenshots`).

**Changes**

| File | What changed |
|---|---|
| `/home/howard/snapshots/TASK-0038/tree-20261025-000945.tar.gz` | created (outside the project tree) |
| `/home/howard/snapshots/TASK-0038/rpms.sha256` | created, 68 lines |
| `/home/howard/snapshots/TASK-0038/git-show-ref.txt`, `git-ls-remote.txt`, `git-status.txt`, `git-log-1.txt`, `remote-url-redacted.txt` | created |
| `/home/howard/snapshots/TASK-0038/tree-20261025-000945.tar.gz.sha256` | created |
| `~/Linux/projects/cinnamon-for-rocky10/` (whole project tree) | unchanged; every command in this item was read-only |

**Checks run:** no compile or linter applies to item 1; the checks are snapshot integrity.
- `wc -l < rpms.sha256` → 68; `find rpms -type f | wc -l` → 68 (acceptance: manifest line count == file count).
- `sha256sum -c rpms.sha256 --quiet` from the project root → OK (all 68 lines).
- `find . -path ./.git -prune -o -type f -print | wc -l` → 13512; `tar -tzf tree-20261025-000945.tar.gz | grep -cv '/$'` → 13512 (tarball complete for the tree minus top-level `.git`).
- `tar -tzf … | grep -c '^\.?/\.git'` → 0 (top-level `.git` absent from the archive); nested component `.git` entries present (879 listing lines under `*/.git/`).
- `sha256sum -c tree-20261025-000945.tar.gz.sha256 --quiet` → OK; recorded sha256 of the tarball: `7fbca8ad290cdd619e61a5c2b9d5290c37b16e92f23ed20d94e92bec4292757f`.
- `git status` exited 128 both before and after the snapshot (pre-existing F9; item 1 changed nothing).

Stopped here at a clean boundary. Item 1 acceptance met (snapshot exists, manifest line count == file count, path recorded). Next item: 2 (repair the git state, establish canonical bytes).

### Item 2 — git repair and canonical bytes (done 2026-10-25)

**Alternatives considered**

Problem: restore the missing objects without moving any ref.
- **Option A — plain `git fetch origin` retry (plan step 1).** The fetch client advertises every local ref tip as "have"; the server sends only objects unreachable from those tips. Every missing object is reachable from an advertised tip, so a negotiated fetch structurally cannot restore it. Empirically: EXIT 0, nothing transferred (pack dir unchanged, fsck still 26 missing).
- **Option B — `git gc` (plan step 2).** Cannot create missing objects. EXIT 128, `fatal: failed to run repack` / `error: Could not read b59da129…`.
- **Option C — targeted `git fetch origin <sha>` for exactly the 26 objects fsck named.** Transferred 25 of 26 (258 objects landed in a new pack; the server sends the want's reachable closure). Withheld exactly one: commit `b59da129`, the parent of advertised tip `8d41fc99` — the server assumes everything reachable from that tip is already local.
- **Option D — re-clone origin to a temp dir and fetch the clone (plan step 3).** Same negotiation block (the clone's ref tips equal main's ref tips, so nothing transfers), plus a 256MB temp clone carrying the PAT in its config. Rejected.
- **Option E — `git fetch origin --refetch --prune` (chosen).** `--refetch` = "fetch all objects as if this were a fresh clone": no have advertisement; the only fetch form that can deliver `b59da129`. Cost: one full pack (262560232 bytes). `--prune` removes the two remote-tracking refs whose branches no longer exist on the remote.
**Chosen:** C then E. C recovered 25/26 and proved all missing objects exist on the remote; E completed it. A and B were run and recorded as plan steps.

**Damage model (evidence).** Pre-repair store: 704 loose objects (468MB, including loose 86M/84M RPM blobs), one 7795-byte pack (4 objects), no LFS (`grep lfs .gitattributes` empty, no `.git/lfs`; command `git count-objects -v`, `du -sh .git/*`, `find .git -type f -size +5M`). `git fsck --full` (EXIT 10) named 26 missing objects reachable from refs (1 commit `b59da129`, 7 trees, 18 blobs) plus 8 `invalid reflog entry` lines; the two reflog-referenced commits (`f85db02f`, `46a7b5b0`, the TASK-0033 amend chain) were missing locally as well — 28 total. Of the 18 missing blobs, 6 are the worktree blobs of in-scope files that differ from `v1.0.0` (`INSTALL.md`, `keys/cinnamon-rocky10-public.asc`, `repo-setup/sign-rpms.sh`, the three csd 6.7.2-3 RPMs; the worktree `SHA256SUMS` blob survived). All missing objects are referenced from post-`v1.0.0` history (commits `b59da129`/`8d41fc99` and the TASK-0024/0027 branch tips); the `v1.0.0` commit `a70aedc6` and its tree were present locally pre-repair. The two reflog commits do not exist on the remote (`remote error: upload-pack: not our ref`) — unrecoverable from origin.

**Repair sequence (commands + results).**
1. `git fetch origin` → EXIT 0, nothing transferred (pack dir unchanged; fsck still 26 missing). [Option A]
2. `git gc` → EXIT 128 (`fatal: failed to run repack`). [Option B]
3. `git fetch origin <26 shas from fsck>` → EXIT 1 (`did not send all necessary objects`); 25 of 26 landed. [Option C]
4. `git fetch origin f85db02f…` / `46a7b5b0…` → `remote error: upload-pack: not our ref` (absent on the remote).
5. `git fetch origin --refetch --prune` → EXIT 0. Single pack `pack-3bd0bd5b…` (262560232 bytes, 716 objects, 0 loose); `.git` 694M→251M; pruned `refs/remotes/origin/feature/TASK-0004-mozjs115-runtime-muffin-fix` and `refs/remotes/origin/feature/TASK-0006-dnf-repo-setup` (deleted on the remote). [Option E]
6. Reflog repair — **flagged destructive:** deleted exactly the 8 reflog lines referencing the two unrecoverable commits (`.git/logs/HEAD`, `.git/logs/refs/heads/feature/TASK-0024-rpm-signing-gpgcheck`; TASK-0033 commit/amend entries, timestamps 1791217797/1791218230/1791218328). The complete `.git/logs` tree was preserved first at `/home/howard/snapshots/TASK-0038/reflogs-20261025/logs/` (14 files). Reflogs are local diagnostic state, not part of the canonical bytes; refs, objects, working tree, and the remote are unaffected by this step.

**State after repair.** `git fsck --full` EXIT 0 (dangling objects only, informational). `git status` EXIT 0: on `main`, up to date with `origin/main`, zero modified tracked files, 15 untracked entries (component source dirs, `rpms-local/`, `screenshots/`, `AGENTS.md`, `INSTALL.md.legacy-2026-08-11`, `agent_creation_prompt.md` — untracked by design). `git log -1 --oneline` → `8d41fc9 feat(release): TASK-0027 signed -3 republish: settings-daemon 6.7.2-3 plus rotated signing key`, EXIT 0. `git show-ref` vs the pre-repair dump: exactly the two pruned remote-tracking refs removed, all other refs byte for byte unchanged. `HEAD` = `refs/heads/main` (unchanged; `git symbolic-ref HEAD`).

**Canonical-bytes decision.**
- The working-tree bytes are canonical for the in-scope paths (`rpms/**`, `keys/**`, `INSTALL.md`, `README.md`, `repo-setup/**`), verified byte for byte against the item-1 snapshot: `sha256sum -c /home/howard/snapshots/TASK-0038/rpms.sha256 --quiet` from the project root → EXIT 0 (68/68); full-tree check: `tar -xzf tree-20261025-000945.tar.gz` to a temp dir plus `diff -r <temp> <tree>` → exactly one line, `Only in <tree>: .git` (excluded from the tarball by design). The repair changed zero tree bytes.
- The refs are canonical for history, and this repair moved none (only the two prunes above).
- Per the match table: worktree == `main` == `feature/TASK-0027-csd-3-signed-republish` on all 74 in-scope files; `v1.0.0` differs only where expected (old key file, old `sign-rpms.sh`, old 64-line `SHA256SUMS`, old `INSTALL.md`, no csd-3 triplet). **H1 resolved:** no unpushed divergence on in-scope paths; `rpms-local/` remains untracked (F10).
- Consequence: item 5 operates on the worktree bytes (== `main` == TASK-0027), and the item-10 commit publishes exactly those bytes under the new tag.

**Per-ref match table.** Method: `git ls-tree -r <ref> -- rpms keys INSTALL.md README.md repo-setup` vs `git hash-object <file>` per worktree file (identical blob sha == identical bytes). Full shas: `/home/howard/snapshots/TASK-0038/item2-blob-cmp.txt`. Tag `v1.0.0` object `954c14a06724189600963fa216752a438b157951` peels to commit `a70aedc6c1fc8bc2a48a8e9aa4e0becd5ddc5071` (`git rev-parse 'refs/tags/v1.0.0^{commit}'`).

Summary: `main` 74/74 · `feature/TASK-0027-csd-3-signed-republish` 74/74 · `v1.0.0` 67/74 match (3 not-in-ref = csd 6.7.2-3 triplet; 4 differ, listed).

| path | worktree==main | worktree==TASK-0027 | worktree==v1.0.0 |
|---|---|---|---|
| `INSTALL.md` | match | match | differ wt `8802abc57635` vs ref `ed17b2d76424` |
| `README.md` | match | match | match |
| `keys/cinnamon-rocky10-public.asc` | match | match | differ wt `67e5f7c2f8f3` vs ref `890f299af220` (old key at the tag) |
| `repo-setup/cinnamon-rocky10.repo` | match | match | match |
| `repo-setup/setup-repo.sh` | match | match | match |
| `repo-setup/sign-rpms.sh` | match | match | differ wt `4da08bb676c2` vs ref `654c86a32ef3` |
| `rpms/SHA256SUMS` | match | match | differ wt `117ecc0561eb` (67 lines) vs ref `3294686c2795` (64 lines) |
| `rpms/cinnamon-6.7.4-3.el10.x86_64.rpm` | match | match | match |
| `rpms/cinnamon-control-center-6.7.2-1.el10.x86_64.rpm` | match | match | match |
| `rpms/cinnamon-control-center-debuginfo-6.7.2-1.el10.x86_64.rpm` | match | match | match |
| `rpms/cinnamon-control-center-debugsource-6.7.2-1.el10.x86_64.rpm` | match | match | match |
| `rpms/cinnamon-control-center-devel-6.7.2-1.el10.x86_64.rpm` | match | match | match |
| `rpms/cinnamon-debuginfo-6.7.4-3.el10.x86_64.rpm` | match | match | match |
| `rpms/cinnamon-debugsource-6.7.4-3.el10.x86_64.rpm` | match | match | match |
| `rpms/cinnamon-desktop-6.7.2-2.el10.x86_64.rpm` | match | match | match |
| `rpms/cinnamon-desktop-debuginfo-6.7.2-2.el10.x86_64.rpm` | match | match | match |
| `rpms/cinnamon-desktop-debugsource-6.7.2-2.el10.x86_64.rpm` | match | match | match |
| `rpms/cinnamon-desktop-devel-6.7.2-2.el10.x86_64.rpm` | match | match | match |
| `rpms/cinnamon-menus-6.7.0-1.el10.x86_64.rpm` | match | match | match |
| `rpms/cinnamon-menus-debuginfo-6.7.0-1.el10.x86_64.rpm` | match | match | match |
| `rpms/cinnamon-menus-debugsource-6.7.0-1.el10.x86_64.rpm` | match | match | match |
| `rpms/cinnamon-menus-devel-6.7.0-1.el10.x86_64.rpm` | match | match | match |
| `rpms/cinnamon-rocky-defaults-1.0-2.el10.noarch.rpm` | match | match | match |
| `rpms/cinnamon-session-6.7.3-1.el10.x86_64.rpm` | match | match | match |
| `rpms/cinnamon-session-debuginfo-6.7.3-1.el10.x86_64.rpm` | match | match | match |
| `rpms/cinnamon-session-debugsource-6.7.3-1.el10.x86_64.rpm` | match | match | match |
| `rpms/cinnamon-settings-daemon-6.7.2-2.el10.x86_64.rpm` | match | match | match |
| `rpms/cinnamon-settings-daemon-6.7.2-3.el10.x86_64.rpm` | match | match | not in v1.0.0 (wt `28cb639db85d`) |
| `rpms/cinnamon-settings-daemon-debuginfo-6.7.2-2.el10.x86_64.rpm` | match | match | match |
| `rpms/cinnamon-settings-daemon-debuginfo-6.7.2-3.el10.x86_64.rpm` | match | match | not in v1.0.0 (wt `7ec9daaf3ea4`) |
| `rpms/cinnamon-settings-daemon-debugsource-6.7.2-2.el10.x86_64.rpm` | match | match | match |
| `rpms/cinnamon-settings-daemon-debugsource-6.7.2-3.el10.x86_64.rpm` | match | match | not in v1.0.0 (wt `b461f833a56e`) |
| `rpms/cjs-6.4.0-1.el10.x86_64.rpm` | match | match | match |
| `rpms/cjs-debuginfo-6.4.0-1.el10.x86_64.rpm` | match | match | match |
| `rpms/cjs-debugsource-6.4.0-1.el10.x86_64.rpm` | match | match | match |
| `rpms/cjs-devel-6.4.0-1.el10.x86_64.rpm` | match | match | match |
| `rpms/gdk-pixbuf-parsers-2.42.12-2.el10.x86_64.rpm` | match | match | match |
| `rpms/gdk-pixbuf-parsers-debuginfo-2.42.12-2.el10.x86_64.rpm` | match | match | match |
| `rpms/gdk-pixbuf-parsers-debugsource-2.42.12-2.el10.x86_64.rpm` | match | match | match |
| `rpms/gnome-terminal-3.54.5-1.el10.x86_64.rpm` | match | match | match |
| `rpms/gnome-terminal-debuginfo-3.54.5-1.el10.x86_64.rpm` | match | match | match |
| `rpms/gnome-terminal-debugsource-3.54.5-1.el10.x86_64.rpm` | match | match | match |
| `rpms/gtk-layer-shell-0.10.1-1.el10.x86_64.rpm` | match | match | match |
| `rpms/gtk-layer-shell-debuginfo-0.10.1-1.el10.x86_64.rpm` | match | match | match |
| `rpms/gtk-layer-shell-debugsource-0.10.1-1.el10.x86_64.rpm` | match | match | match |
| `rpms/gtk-layer-shell-devel-0.10.1-1.el10.x86_64.rpm` | match | match | match |
| `rpms/mozjs115-115.29.0-1.el10.x86_64.rpm` | match | match | match |
| `rpms/mozjs115-debuginfo-115.29.0-1.el10.x86_64.rpm` | match | match | match |
| `rpms/mozjs115-debugsource-115.29.0-1.el10.x86_64.rpm` | match | match | match |
| `rpms/mozjs115-devel-115.29.0-1.el10.x86_64.rpm` | match | match | match |
| `rpms/mozjs115-devel-debuginfo-115.29.0-1.el10.x86_64.rpm` | match | match | match |
| `rpms/muffin-6.7.4-3.el10.x86_64.rpm` | match | match | match |
| `rpms/muffin-clutter-6.7.4-3.el10.x86_64.rpm` | match | match | match |
| `rpms/muffin-clutter-debuginfo-6.7.4-3.el10.x86_64.rpm` | match | match | match |
| `rpms/muffin-clutter-devel-6.7.4-3.el10.x86_64.rpm` | match | match | match |
| `rpms/muffin-cogl-6.7.4-3.el10.x86_64.rpm` | match | match | match |
| `rpms/muffin-cogl-debuginfo-6.7.4-3.el10.x86_64.rpm` | match | match | match |
| `rpms/muffin-cogl-devel-6.7.4-3.el10.x86_64.rpm` | match | match | match |
| `rpms/muffin-debuginfo-6.7.4-3.el10.x86_64.rpm` | match | match | match |
| `rpms/muffin-debugsource-6.7.4-3.el10.x86_64.rpm` | match | match | match |
| `rpms/muffin-devel-6.7.4-3.el10.x86_64.rpm` | match | match | match |
| `rpms/nemo-6.7.4-2.el10.x86_64.rpm` | match | match | match |
| `rpms/nemo-debuginfo-6.7.4-2.el10.x86_64.rpm` | match | match | match |
| `rpms/nemo-debugsource-6.7.4-2.el10.x86_64.rpm` | match | match | match |
| `rpms/nemo-devel-6.7.4-2.el10.x86_64.rpm` | match | match | match |
| `rpms/python3-pillow-12.3.0-2.el10.x86_64.rpm` | match | match | match |
| `rpms/python3-setproctitle-1.3.7-2.el10.x86_64.rpm` | match | match | match |
| `rpms/python3-tinycss2-1.5.1-2.el10.x86_64.rpm` | match | match | match |
| `rpms/python3-webencodings-0.5.1-2.el10.x86_64.rpm` | match | match | match |
| `rpms/python3-xapp-3.0.2-1.el10.x86_64.rpm` | match | match | match |
| `rpms/xapps-debugsource-3.3.3-1.el10.x86_64.rpm` | match | match | match |
| `rpms/xapps-devel-3.3.3-1.el10.x86_64.rpm` | match | match | match |
| `rpms/xapps-lib-3.3.3-1.el10.x86_64.rpm` | match | match | match |
| `rpms/xapps-lib-debuginfo-3.3.3-1.el10.x86_64.rpm` | match | match | match |

**Changes**

| File / path | What changed |
|---|---|
| `.git` object store (project repo) | restored: 26 objects fetched (25 via targeted fetch, `b59da129` via `--refetch`); consolidated into single pack `pack-3bd0bd5b…` (262560232 bytes, 716 objects, 0 loose); `.git` 694M→251M |
| `.git/logs/HEAD`, `.git/logs/refs/heads/feature/TASK-0024-rpm-signing-gpgcheck` | 8 reflog lines referencing the two unrecoverable commits deleted (full `.git/logs` preserved at `/home/howard/snapshots/TASK-0038/reflogs-20261025/logs/`) |
| `refs/remotes/origin/feature/TASK-0004-mozjs115-runtime-muffin-fix`, `refs/remotes/origin/feature/TASK-0006-dnf-repo-setup` | deleted (`--prune`; branches no longer on the remote) |
| `/home/howard/snapshots/TASK-0038/item2-blob-cmp.txt`, `/home/howard/snapshots/TASK-0038/reflogs-20261025/logs/` | created (evidence, outside the project tree) |
| `/tmp/opencode/task38-*.txt` | created (fetch/fsck/status/diff outputs; machine-local temp) |
| working tree (all 13512 files), `refs/heads/*`, `refs/tags/*`, `HEAD` | unchanged (verified against the snapshot) |

**Checks run.**
- `git fsck --full` → EXIT 0 [pre-repair: EXIT 10; 26 missing + 21 error lines]
- `git status` → EXIT 0 [pre-repair: EXIT 128, `error: bad tree object HEAD`]
- `git log -1 --oneline` → EXIT 0, `8d41fc9…` [pre-repair: EXIT 128]
- `diff <snapshot git-show-ref dump> <git show-ref after repair>` → only the two pruned remote-tracking refs removed
- `sha256sum -c /home/howard/snapshots/TASK-0038/rpms.sha256 --quiet` from the project root → EXIT 0, 68/68
- `diff -r <extracted snapshot tarball> <tree>` → exactly one line: `Only in <tree>: .git`
- per-ref blob cmp (`git ls-tree -r` vs `git hash-object`) → `main` 74/74, TASK-0027 74/74, `v1.0.0` 67/74 (table above)
- `git count-objects -v` → `count: 0, in-pack: 716, packs: 1, prune-packable: 0`
- `git ls-remote origin` (pre-repair) → EXIT 0, byte for byte identical to the snapshot dump (network + auth healthy before any change)

**Competing priorities / trade-offs.**
- Chose the one-time 256MB `--refetch` over leaving `b59da129` missing: `git log` (acceptance) cannot traverse parent `b59da129`, and no negotiated fetch can deliver it (Option C, empirically).
- No `git gc` run for consolidation: the fetch already consolidated the store (0 loose, 0 prune-packable); a further gc would have changed nothing.
- Dangling objects left in place (informational only; fsck EXIT 0).
- The `origin` URL carries a PAT (F14): every command whose output could print it was run through a userinfo-masking sed; the token value is never recorded here. Flag for `## Security` (Omega).
- Item 2 acceptance met: per-ref match table above, `git status` EXIT 0, canonical-bytes decision recorded. Next item: 3 (per-file signature audit) — the GPG track is ready (store and refs restored); items 4, 6, 7 remain independent.

### Item 3 — per-file signature audit (done 2026-10-25)

**Result.** The audit matches F4: 64 of 67 RPMs signed with the old key, 3 (the csd 6.7.2-3 triplet) signed with the tracked key. No dual-signed files (the two per-file OK sets are disjoint and cover all 67), no unsigned files. The three-way consistency check **fails**: the tracked public key, the fingerprint recorded in `INSTALL.md`, and the keys that signed the RPMs are not mutually consistent. The fingerprint recorded in `INSTALL.md` is the old key's, not the tracked key's.

**Alternatives considered**

Problem: verify each signature against exactly one public key, without touching the host rpm keyring (F5 state is evidence for the rollback section).
- **Option A — `rpm --root` sandboxes (chosen).** A fake root per keyring: `rpm --root R --initdb` then `rpm --root R --import <one key>` gives a keyring holding exactly that key; `rpm -K --root R <file>` verifies against it. Pros: zero host-state change, exactly one key per keyring, uses rpm's own verifier (same code path dnf uses). Cons: two disposable fake roots under `/tmp/opencode/task38/`.
- **Option B — swap the host's `/var/lib/rpm/gpg-pubkey-*` files (host keys aside, import the scratch key, restore).** Pros: exercises the "real" path. Cons: modifies host state the rollback section records; restore must be byte exact; rejected.
- **Option C — extract the embedded PGP signature and `gpg --verify` manually.** Pros: no rpm db. Cons: reimplements what `rpm -K` does (reassembling the signed lead+header+payload); format risk; rejected.
- **Option D — trust `rpm -qpi`'s Key ID without cryptographic verification.** Pros: fastest. Cons: the plan requires verification against both scratch keyrings; the embedded key ID alone is not verification; rejected (the Key ID is kept as the per-file signer column only).

**Method (commands).**
1. Per-file signer: `rpm -qpi <file> | grep -i 'key ID'` (the `%{SIGPGP:pgpsig}` queryformat route returns empty on this rpm 4.19 and was not used, per the plan).
2. Key identities: throwaway `GNUPGHOME` keyrings (the F1 method): `GNUPGHOME=<scratch> gpg --batch --import <file>` then `GNUPGHOME=<scratch> gpg --with-colons --list-keys`.
3. Verification sandboxes: `RA=/tmp/opencode/task38/root-tracked`, `RB=/tmp/opencode/task38/root-old`; `rm -rf R && mkdir -p R/var/lib/rpm && rpm --root R --initdb && rpm --root R --import <key>`; isolation check `rpm -qa --root R | grep -i gpg`. Then per file: `rpm -K --root $RA <file>` and `rpm -K --root $RB <file>`.
4. Old key source per F6: `git show v1.0.0:keys/cinnamon-rocky10-public.asc > /tmp/opencode/task38/oldkey.asc`.

**Key identities (verified in this run).**

| Identity | Key ID | Fingerprint | Evidence |
|---|---|---|---|
| Tracked public key, primary | `EBD13108EB7FEF99` | `2274BFE1BF28C051CD98675BEBD13108EB7FEF99` | `gpg --with-colons --list-keys` after importing `keys/cinnamon-rocky10-public.asc` into a throwaway keyring |
| Tracked key, signing subkey (signs the 3 new RPMs) | `14CF2C0A8A47323C` | `CD4958E1A421CBD6B56B7C5614CF2C0A8A47323C` | same listing |
| Old key, primary (no subkey; the primary signed) | `9C0A8912FDA02785` | `1689676AF4D4F6FEC142B4429C0A8912FDA02785` | same, after importing `/tmp/opencode/task38/oldkey.asc` (the F6 export) |
| Fingerprint recorded in the docs | — | `1689676AF4D4F6FEC142B4429C0A8912FDA02785` | `grep -n` at `INSTALL.md:188`, `INSTALL.md:283`, `README.md:156`; `repo-setup/setup-repo.sh:42` `KEY_ID="fda02785"` |

Both keys carry uid `metallinux Cinnamon for Rocky Linux (repo signing) <repo-signing@metalinux.dev>` (old key created 2026-09-21, tracked key 2026-10-19). `repo-setup/sign-rpms.sh:66` holds `EXPECTED_FINGERPRINT="2274BFE1BF28C051CD98675BEBD13108EB7FEF99"` (the tracked key), so the signing script and the published docs already disagree.

**Per-file table.** All 67 files in `rpms/`. Keyring A holds only the tracked key (`gpg-pubkey-eb7fef99-6ad5798e`), keyring B only the old key (`gpg-pubkey-fda02785-6ab101f4`), verified via `rpm -qa --root`. Columns A/B are the `rpm -K` result under each keyring; exact rpm strings: `digests signatures OK` / `digests SIGNATURES NOT OK`.

| RPM | signer Key ID (`rpm -qpi`) | A tracked-only | B old-only |
|---|---|---|---|
| `cinnamon-6.7.4-3.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `cinnamon-control-center-6.7.2-1.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `cinnamon-control-center-debuginfo-6.7.2-1.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `cinnamon-control-center-debugsource-6.7.2-1.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `cinnamon-control-center-devel-6.7.2-1.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `cinnamon-debuginfo-6.7.4-3.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `cinnamon-debugsource-6.7.4-3.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `cinnamon-desktop-6.7.2-2.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `cinnamon-desktop-debuginfo-6.7.2-2.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `cinnamon-desktop-debugsource-6.7.2-2.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `cinnamon-desktop-devel-6.7.2-2.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `cinnamon-menus-6.7.0-1.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `cinnamon-menus-debuginfo-6.7.0-1.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `cinnamon-menus-debugsource-6.7.0-1.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `cinnamon-menus-devel-6.7.0-1.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `cinnamon-rocky-defaults-1.0-2.el10.noarch.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `cinnamon-session-6.7.3-1.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `cinnamon-session-debuginfo-6.7.3-1.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `cinnamon-session-debugsource-6.7.3-1.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `cinnamon-settings-daemon-6.7.2-2.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `cinnamon-settings-daemon-6.7.2-3.el10.x86_64.rpm` | `14cf2c0a8a47323c` | OK | NOT OK |
| `cinnamon-settings-daemon-debuginfo-6.7.2-2.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `cinnamon-settings-daemon-debuginfo-6.7.2-3.el10.x86_64.rpm` | `14cf2c0a8a47323c` | OK | NOT OK |
| `cinnamon-settings-daemon-debugsource-6.7.2-2.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `cinnamon-settings-daemon-debugsource-6.7.2-3.el10.x86_64.rpm` | `14cf2c0a8a47323c` | OK | NOT OK |
| `cjs-6.4.0-1.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `cjs-debuginfo-6.4.0-1.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `cjs-debugsource-6.4.0-1.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `cjs-devel-6.4.0-1.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `gdk-pixbuf-parsers-2.42.12-2.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `gdk-pixbuf-parsers-debuginfo-2.42.12-2.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `gdk-pixbuf-parsers-debugsource-2.42.12-2.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `gnome-terminal-3.54.5-1.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `gnome-terminal-debuginfo-3.54.5-1.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `gnome-terminal-debugsource-3.54.5-1.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `gtk-layer-shell-0.10.1-1.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `gtk-layer-shell-debuginfo-0.10.1-1.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `gtk-layer-shell-debugsource-0.10.1-1.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `gtk-layer-shell-devel-0.10.1-1.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `mozjs115-115.29.0-1.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `mozjs115-debuginfo-115.29.0-1.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `mozjs115-debugsource-115.29.0-1.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `mozjs115-devel-115.29.0-1.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `mozjs115-devel-debuginfo-115.29.0-1.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `muffin-6.7.4-3.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `muffin-clutter-6.7.4-3.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `muffin-clutter-debuginfo-6.7.4-3.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `muffin-clutter-devel-6.7.4-3.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `muffin-cogl-6.7.4-3.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `muffin-cogl-debuginfo-6.7.4-3.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `muffin-cogl-devel-6.7.4-3.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `muffin-debuginfo-6.7.4-3.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `muffin-debugsource-6.7.4-3.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `muffin-devel-6.7.4-3.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `nemo-6.7.4-2.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `nemo-debuginfo-6.7.4-2.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `nemo-debugsource-6.7.4-2.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `nemo-devel-6.7.4-2.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `python3-pillow-12.3.0-2.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `python3-setproctitle-1.3.7-2.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `python3-tinycss2-1.5.1-2.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `python3-webencodings-0.5.1-2.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `python3-xapp-3.0.2-1.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `xapps-debugsource-3.3.3-1.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `xapps-devel-3.3.3-1.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `xapps-lib-3.3.3-1.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |
| `xapps-lib-debuginfo-3.3.3-1.el10.x86_64.rpm` | `9c0a8912fda02785` | NOT OK | OK |

**Consistency verdict (the diagnostic).** Not mutually consistent, in two places:
- Recorded fingerprint vs tracked public key: `INSTALL.md:188` and `:283` (and `README.md:156`) record `1689676AF4D4F6FEC142B4429C0A8912FDA02785` (the old key); `keys/cinnamon-rocky10-public.asc` is `2274BFE1BF28C051CD98675BEBD13108EB7FEF99` (the tracked key). The docs and the key file the documented consumer path imports disagree. The tracked fingerprint does not appear anywhere in `INSTALL.md`.
- Signers vs tracked public key: 3 of 67 RPMs verify (the csd 6.7.2-3 triplet, signed by subkey `14CF2C0A8A47323C`); 64 of 67 do not (each: `digests SIGNATURES NOT OK` under keyring A).
- Signers vs recorded fingerprint: 64 of 67 RPMs verify (signed by the old primary `9C0A8912FDA02785`); 3 of 67 do not (the csd 6.7.2-3 triplet).
- Exactly which RPMs mismatch and under which key: the 64 rows of the table above with signer `9c0a8912fda02785` do not verify against the tracked public key; each is signed under the old key, fingerprint `1689676AF4D4F6FEC142B4429C0A8912FDA02785`. The 3 rows with signer `14cf2c0a8a47323c` do not verify against the key whose fingerprint `INSTALL.md` records.
- Root cause (resolves the plan's hypothesis, F16, with one correction): a consumer following the documented path imports the tracked key (per `INSTALL.md` line 187: the key is at `keys/cinnamon-rocky10-public.asc`) and dnf under `gpgcheck=1` refuses the 64 old-signed RPMs; `setup-repo.sh` aborts earlier still at its stale `KEY_ID="fda02785"` assertion (F8). Correction to F16's phrasing: `vm-test/install-set.txt:20` lists `cinnamon-settings-daemon` by name without a version pin, so dnf resolves it to 6.7.2-3 (tracked-key signed). Of the 22 install-set names, 21 resolve to old-signed RPMs and that one resolves to the new-key-signed -3; the install still fails, on the 21 old-signed RPMs.
- The 68th artifact, `SHA256SUMS`, is not an RPM and has no GPG signature. `cd rpms && sha256sum -c SHA256SUMS` → 67 OK / 0 FAIL, EXIT 0. Cross-check against the item-1 manifest: `sha256sum -c /home/howard/snapshots/TASK-0038/rpms.sha256` from the project root → 68 OK / 68, EXIT 0.

**Changes**

| File / path | What changed |
|---|---|
| Project tree (all 13512 files) | unchanged; every command in this item was read-only |
| `/tmp/opencode/task38/kr-tracked/`, `kr-old/` | created (throwaway GNUPGHOME keyrings for the key-identity listings) |
| `/tmp/opencode/task38/root-tracked/`, `root-old/` | created (`rpm --root` sandboxes; one `gpg-pubkey` package each) |
| `/tmp/opencode/task38/oldkey.asc` | created (the F6 export from `v1.0.0`; public key only) |
| `/tmp/opencode/task38/item3-table.txt`, `sha256sums-check.txt`, `snap-manifest-check.txt` | created (raw audit logs; machine-local temp, not committed) |
| This planning doc, `## Implementation` | this section |

**Checks run.**
- Counts: `ls rpms/*.rpm | wc -l` → 67; `wc -l < rpms/SHA256SUMS` → 67 (67-line manifest for 67 RPMs).
- Key identities: `gpg --with-colons --list-keys` in throwaway `GNUPGHOME` keyrings → tracked key = primary `EBD13108EB7FEF99` + signing subkey `14CF2C0A8A47323C` (fprs in the identity table); old key = single primary `9C0A8912FDA02785`, no subkey.
- Sandbox isolation: `rpm -qa --root $RA | grep -i gpg` → exactly `gpg-pubkey-eb7fef99-6ad5798e`; `--root $RB` → exactly `gpg-pubkey-fda02785-6ab101f4`.
- Method check before the full run (one old-signed file, one new-signed file): results invert as expected across the two sandboxes (`digests signatures OK` / `digests SIGNATURES NOT OK` in the matching sandbox each).
- Per-file signer: 67/67 files print exactly one `Key ID` line from `rpm -qpi`: 64 × `9c0a8912fda02785`, 3 × `14cf2c0a8a47323c`, 0 unsigned. (This rpm 4.19.1.1 prints the key ID in lowercase hex; F4 recorded it uppercase — same IDs, no correction.)
- `rpm -K --root $RA` over all 67: 3 `digests signatures OK`, 64 `digests SIGNATURES NOT OK`. `rpm -K --root $RB`: the exact inverse (64 OK, 3 NOT OK). Full log: `/tmp/opencode/task38/item3-table.txt` (67 lines).
- `cd rpms && sha256sum -c SHA256SUMS` → 67 OK / 0 FAIL, EXIT 0.
- `sha256sum -c /home/howard/snapshots/TASK-0038/rpms.sha256` (project-root cwd) → 68 OK / 68, EXIT 0.

**Competing priorities / trade-offs.**
- The audit is read-only: the host rpm keyring (F5), the user's gnupg, and the project tree are untouched; `rpm --root` sandboxes give one-key-per-keyring isolation without host-state changes (Option A).
- The 67-row table is recorded in full, as the plan requires; the raw log additionally lives at `/tmp/opencode/task38/item3-table.txt` (machine-local temp, not committed).

Item 3 acceptance met: the per-file table matches F4 (64 old / 3 new) with no correction needed. Next item: 4 (recreate the dedicated signing keyring from `~/AI/secrets`); items 6 and 7 remain independent.

### Item 4 — dedicated signing keyring recreation (done 2026-10-25)

**Result.** The dedicated keyring and its sibling passphrase location are recreated exactly as `sign-rpms.sh` mandates: `~/.gnupg-cinnamon-rocky10` (mode 700) holds exactly one secret key, primary fingerprint `2274BFE1BF28C051CD98675BEBD13108EB7FEF99` (== `sign-rpms.sh:66` `EXPECTED_FINGERPRINT`), with its signing subkey `14CF2C0A8A47323C`; `~/.gnupg-cinnamon-rocky10.passphrase` (700) + `passphrase` (600) recreated by `cp` from `~/AI/secrets/gpg-passphrase.txt`. The preflight, run as the script's own lines 1-204 verbatim, passes every keyring check and reaches the rpms/ step: `Found 67 RPM files.`, exit 0. No RPM was signed; the project tree is byte for byte the item-1 snapshot (68/68). A disposable detached signature proved the passphrase file's bytes unlock the key (the preflight cannot: `PRESET_PASSPHRASE` answers OK for any valid hex, `sign-rpms.sh:224-230`). No passphrase or key value was printed, cat'ed, echoed, or written to any repo file, doc, or log.

**Alternatives considered**

Problem 1: how to run the preflight without signing. The tracked script's preflight block (lines 112-204) is directly followed by the passphrase preset (`:236`) and an in-place sign loop (`:280-291`); a full run would sign the 64 old-signed RPMs in place in `rpms/`, which is item 5's staging work and must not happen yet.
- **Option A — byte-identical truncated copy (chosen).** `sed -n '1,204p'` of the tracked script (the preflight ends at line 204, `info "Found ${RPM_TOTAL} RPM files."`), plus a trailer that prints a marker and exits 0. Prefix verified byte for byte against the tracked script (`diff <(head -n 204 <tracked>) <(head -n 204 <copy>)` → empty, recorded as `PREFIX-IDENTICAL`). Every preflight line runs verbatim, including the exactly-one-secret-key check, the fingerprint equality against `EXPECTED_FINGERPRINT` (`:142-144`), the keygrip/uid derivation, the passphrase dir/file modes and single-line shape (`:165-181`), the host rpm keyring check (`:196-198`), and the rpms/ step (`:200-204`). No passphrase read, no preset, no signature.
- **Option B — real script against a scratch `PROJECT_ROOT` with an empty `rpms/`.** It reaches the rpms/ step but dies at `sign-rpms.sh:203` (`No .rpm files found`), i.e. the run ends in failure and the rpms/ presence check is not part of the pass. Rejected.
- **Option C — real script in full, relying on idempotency.** 64 of 67 RPMs are unsigned (item 3), so a full run signs them in place. That is item 5's job, on a staging copy, with the consumer sub-check first. Rejected outright.

Problem 2: the passphrase bytes.
- **Chosen:** `cp` from `~/AI/secrets/gpg-passphrase.txt` (the plan spec for this item: "by `cp`, no cat/echo"), then explicit `chmod 600`. Plain `cp` without `-p` applies the umask to the source's 644, so the chmod is required to reach the mandated 600. Shape verified without printing: byte count (49), newline count (1), ends-with-newline test (yes) — the same checks the script runs at `:175-181`, so a 48-character single-line passphrase with one trailing newline.
- **Alternative:** retype or re-derive the passphrase. The source file is the byte source of truth (it is the key material); retyping invites transcription error and requires the value into a terminal. Rejected.

Problem 3: verifying the passphrase actually matches the key.
- **Option A — disposable detached signature through the script's own preset protocol (chosen).** The preflight cannot verify the bytes (its own comment, `:224-230`). So: the idempotent `allow-preset-passphrase` in the keyring `gpg-agent.conf` (the script's own step, `:211-216`), `PRESET_PASSPHRASE` with the signing keygrip, then `gpg --detach-sign` over a throwaway `/tmp` file (not an RPM, never published), `gpg --verify`, then `CLEAR_PASSPHRASE`, agent kill, file removal. Only the OK line, the public Good-signature lines, and the signer keyid are printed.
- **Option B — no test; let item 5's first `rpm --addsign` surface a wrong passphrase.** The script's own failure point is there (`:229-230`), but a failure mid signing-loop is a worse failure point than one before any signing work. Rejected.

**Method (commands).** All by path; no value printed anywhere in this item.
1. `mkdir -m 700 ~/.gnupg-cinnamon-rocky10`; `GNUPGHOME=~/.gnupg-cinnamon-rocky10 gpg --batch --import ~/AI/secrets/gpg-secret-key.asc` (an import never needs the passphrase).
2. Secret listing: `GNUPGHOME=… gpg --with-colons -K` filtered to `sec:/ssb:/fpr:/uid:/grp:` lines (all public fields).
3. `mkdir -m 700 ~/.gnupg-cinnamon-rocky10.passphrase`; `cp ~/AI/secrets/gpg-passphrase.txt …/passphrase`; `chmod 600 …/passphrase`.
4. Preflight: `sed -n '1,204p' repo-setup/sign-rpms.sh` + `exit 0` trailer → `/tmp/opencode/task38/item4-preflight.sh`; prefix identity `diff` → empty; run against the real project root, exit 0.
5. Dummy-sign verification per Problem 3 Option A; the dummy file was removed and the preset cleared afterward.

**Keyring state (verified in this run).**

| Property | Value | Evidence |
|---|---|---|
| Keyring path / mode | `~/.gnupg-cinnamon-rocky10` / 700 | `stat -c '%a'` |
| Secret keys | exactly one key: one `sec:` (primary) + one `ssb:` (signing subkey) | `gpg --with-colons -K` in the dedicated keyring; the preflight's `grep -c '^sec:'` == 1 check (`:137-140`) passed |
| Primary fingerprint | `2274BFE1BF28C051CD98675BEBD13108EB7FEF99` | first `fpr:` line; equals `sign-rpms.sh:66`; the preflight's `die` at `:142-144` did not fire |
| Signing subkey | `14CF2C0A8A47323C` (fpr `CD4958E1A421CBD6B56B7C5614CF2C0A8A47323C`), signing capability | `ssb:`/`fpr:` lines; the keygrip the script selects (subkey preferred per its awk) is `CB22A20E1EEEED712E3629F31C4F7AA58B918239` (primary keygrip `A4F2A163B2EE16FF0E47F483AD78874BB74229CB`); keygrips are public (derived from the public key; the script prints them in its own INFO line) |
| uid | `metallinux Cinnamon for Rocky Linux (repo signing) <repo-signing@metalinux.dev>` | `uid:` line; the preflight's uid check (`:161-162`) passed |
| Passphrase dir / file | `~/.gnupg-cinnamon-rocky10.passphrase` 700 / `passphrase` 600, 49 bytes, single line, trailing newline | `stat -c '%a'`; `wc -c` / `tr -cd '\n' \| wc -c` / `tail -c 1 \| wc -l`; the preflight's mode and shape checks (`:165-181`) passed |
| Host rpm keyring | `gpg-pubkey-eb7fef99-6ad5798e` present, unchanged | `rpm -q 'gpg-pubkey-eb7fef99-*'`; the preflight's check at `:196-198` passed |

**Changes**

| Path | What changed |
|---|---|
| `~/.gnupg-cinnamon-rocky10/` (700) | created; secret key imported from `~/AI/secrets/gpg-secret-key.asc` (path only, never printed); one `sec:` + one `ssb:` |
| `~/.gnupg-cinnamon-rocky10/gpg-agent.conf` | `allow-preset-passphrase` added (the script's own idempotent step, `:211-216`; required by the preset protocol) |
| `~/.gnupg-cinnamon-rocky10.passphrase/` (700) + `passphrase` (600) | created; `cp` from `~/AI/secrets/gpg-passphrase.txt` (bytes unchanged); value never printed, cat'ed, or echoed |
| `/tmp/opencode/task38/item4-preflight.sh` | created (preflight lines 1-204 verbatim + exit-0 trailer; machine-local temp, not committed) |
| `/tmp/opencode/task38/item4-dummy/` | created and removed (disposable sign test; no RPM bytes involved) |
| `rpms/` (67 RPMs + `SHA256SUMS`), rest of the project tree, host rpm keyring | unchanged (verified below) |
| This planning doc, `## Implementation` | this section |

**Checks run.**
- Preflight (the item's acceptance): `bash /tmp/opencode/task38/item4-preflight.sh <project root>` → every check passed, output ends `INFO: Found 67 RPM files.` then the completion marker, EXIT 0. Keyring checks all pass: exactly one secret key, fingerprint == `sign-rpms.sh:66`, signing keygrip derived, uid present, passphrase dir 700 / file 600 / single line, host rpm keyring holds `gpg-pubkey-eb7fef99-*`, `rpms/` holds 67 RPMs.
- Prefix identity: `diff <(head -n 204 repo-setup/sign-rpms.sh) <(head -n 204 item4-preflight.sh)` → empty (`PREFIX-IDENTICAL`); the run is the tracked script's own preflight, not a reimplementation.
- Secret listing: one `sec:`, first `fpr:` == `2274BFE1BF28C051CD98675BEBD13108EB7FEF99`, one `ssb:` with signing capability, uid as above.
- Dummy-sign: `PRESET_PASSPHRASE` reply `OK`; `gpg --verify` → `Good signature from "metallinux Cinnamon for Rocky Linux (repo signing) <repo-signing@metalinux.dev>"`, signer keyid `14CF2C0A8A47323C` (`gpg --list-packets` on the throwaway file), primary fingerprint in the verify output `2274 BFE1 BF28 C051 CD98 675B EBD1 3108 EB7F EF99`; `CLEAR_PASSPHRASE` reply `OK`; gpg-agent killed; dummy dir removed.
- Secret hygiene: no command in this item cats, echoes, or prints the passphrase file or the secret-key file; only `stat`/`wc`/`tr`/`tail | wc`/`grep -c` on them. The secret key file was only ever read by `gpg --import`.
- Tree integrity after the item: `sha256sum -c /home/howard/snapshots/TASK-0038/rpms.sha256 --quiet` from the project root → EXIT 0, 68/68 (`TREE-OK`).

**Competing priorities / trade-offs.**
- The real script was not run in full: zero signatures written, so item 5's staging protocol starts from snapshot bytes. The preflight evidence comes from a byte-identical prefix copy, so it is not a reimplementation of the checks.
- The `allow-preset-passphrase` line was added ahead of item 5's run; the script's idempotent check (`:212`) then skips its kill step. No competing state.
- The dummy-sign test used the real key over a throwaway `/tmp` file: it proves the unprotect path end to end (the exact failure R5 fears) while touching no repo byte; the file was removed, the preset cleared, and the agent killed.
- The passphrase file's bytes equal the source's bytes (`cp`, no transformation). If item 5 ever surfaces an unprotect error, the source file itself is suspect, not the copy.

Item 4 acceptance met: the preflight reaches the rpms/ step (`Found 67 RPM files.`) and the keyring fingerprint == `sign-rpms.sh:66`. Next item: 5 (re-sign and repair the published set, Option A, staging first); its prerequisites, items 3 and 4, are both done. Items 6 and 7 remain independent.

### Item 5 — re-sign and repair the published set, Option A (done 2026-10-25)

**Result.** Option A executed, with one mechanism substitution forced by rpm: the plan's `rpm --addsign` is infeasible on this rpm (4.19.1.1), so the 64 old-key RPMs were re-signed with `rpm --resign`, which replaces the old signature with the tracked-key signature instead of adding a second one. The 3 tracked-key-signed RPMs (the csd 6.7.2-3 triplet) stayed byte-identical. The csd 6.7.2-2 triplet was dropped. `SHA256SUMS` regenerated at 64 lines, `repodata/` regenerated (untracked, `.gitignore:13`). The staged set passed every sub-check, then was swapped into `rpms/`. All 64 published RPMs now verify against the tracked key only: tracked-only `rpm --root` sandbox `rpm -K` 64/64 `signatures OK`, per-file `rpm -qpi` signer `14cf2c0a8a47323c` on all 64, old-key-only sandbox 0/64 (old signatures are gone from every file), `sha256sum -c SHA256SUMS` 64 OK, and the dnf `gpgcheck=1` consumer simulation accepts the set under the tracked key and refuses it under the old key (positive/negative pair below). Payload bytes of every re-signed file are unchanged (`rpm2cpio` digest compare, 63/63 identical). Mechanism decision recorded: Option A; not Option B, no rebuild.

**Alternatives considered**

Problem 1: the re-sign mechanism.
- **Option A (plan wording) — `rpm --addsign`, dual-sign every old-key file.** Infeasible on this rpm: `rpm --addsign` refuses files that already carry a signature (`already contains a legacy signature`), so a second (tracked-key) signature cannot be added to the 64 files. Probed on a staging copy before any bulk work.
- **Option B (plan fallback) — publish the old public key (F6), no byte change.** Keeps the old signatures verifiable, but the published set would then verify under two different keys and the old key (fingerprint `1689676A…`) stays in circulation in the new tag. Conflicts with the DoD GPG boxes that require the tracked key to be the consumer's only key. Rejected.
- **Option C — full rebuild of all 64 RPMs, sign fresh.** Correct bytes, but needs the build environment (risk R3, unverified after the host reinstall) and is not required: signature replacement works and is verifiable. Rejected as disproportionate.
- **Chosen — `rpm --resign --define "_gpg_name <uid>" <file>` under the item-4 keyring.** Replaces the old signature with one by the tracked signing subkey. Probe result that settled it: a resigned sample verifies `signatures OK` in the tracked-only sandbox and `SIGNATURES NOT OK` in the old-key-only sandbox, i.e. the old signature is removed, not carried along. Consequence: every published file carries exactly one signature, by the tracked subkey. This resolves risk R2 in the strong form: there is no dual-signed file for which "every signature must verify" could even be evaluated.

Problem 2: the preset-passphrase protocol (root cause of the prior session's failures).
- **Chosen — the pinned protocol from `sign-rpms.sh:236-239`:** preset via heredoc/stdin to `gpg-connect-agent --homedir <keyring>`, one `PRESET_PASSPHRASE <subkey-keygrip> -1 <hex>` line, `/bye`; the hex is the raw passphrase file hex-encoded (`printf '%s' "$PASS" | xxd -p | tr -d '\n'` → 96 hex digits for the 48-char raw value); clear with `CLEAR_PASSPHRASE <keygrip>` in the same form. This signs: 64/64 in the loop, zero unprotect errors.
- **Rejected (both cost the prior session):** passing `PRESET_PASSPHRASE` as CLI arguments makes gpg-connect-agent mis-parse (the `-1 <hex>` gets consumed; `ERR 67108992 Missing value`), and using the passphrase file's content directly as the hex argument instead of hex-encoding the raw bytes is a wrong-bytes failure that surfaces only as an unprotect error at sign time. The keybox was never the problem (`--list-keys`/`--list-secret-keys` RC=0, `pubring.kbx` byte-stable; a throwaway key with a real passphrase generated and signed fine host-wide).

Problem 3: the dnf `gpgcheck=1` consumer sub-check. Three designs were dead ends before the one that works; all four are recorded because the negative control is what makes the positive one mean anything.
- **Rejected 1 — host `dnf install --downloadonly`.** The 22 install-set names are already installed on the host from the prior acceptance run, so dnf reports "already installed" and downloads nothing to verify.
- **Rejected 2 — `dnf download` (plugin) with only `task38staged` enabled.** Downloads 22/22 from staging with RC=0, but dnf 4.20.0's `download` command does not enforce `gpgcheck`: the identical run with `gpgkey` = the old key also completes 22/22, RC=0. Not a verification path.
- **Rejected 3 — `file://` repo in the install path.** `do_transaction` (dnf 4.20 `cli/cli.py:287-303`) downloads and then runs `gpgsigcheck`, which verifies each package via `rpmkeys --checksig --root <installroot>` against the installroot's rpm keyring, importing the repo `gpgkey` only when a check comes back `NOKEY`. A `file://` repo changes nothing about that keyring, and the host keyring already holds the tracked key (F5), so a copied installroot verifies the staged set with the old-key `gpgkey` configured and never references it. Negative control passes vacuously.
- **Chosen — local HTTP server over the staged tree + throwaway installroot.** `python3 -m http.server 18484 --bind 127.0.0.1` serving `staging/rpms/`; installroot = a copy of the host rpm DB with (a) every `gpg-pubkey` entry erased from the copy (so the check starts at `NOKEY` and must use the repo `gpgkey`) and (b) the 22 install-set names erased from the copy (so all 22 must resolve and download); `dnf install -y --downloadonly` with only `task38staged` enabled, `gpgcheck=1`, `gpgkey` = tracked key for the positive run, old key for the negative. Two sub-facts cost time and are recorded: on this system `%_dbpath` is the absolute macro `/usr/lib/sysimage/rpm`, so `rpm`/`dnf --root` look at `$ROOT/usr/lib/sysimage/rpm` (a DB copied to `$ROOT/var/lib/rpm` is invisible to them), and this rpm refuses a bare `rpm -e gpg-pubkey` (`specifies multiple packages`), so each key NEVRA must be erased individually.
- The sub-check covers the 22 runtime names from `vm-test/install-set.txt:14-35` (the documented install set); `rpm -K` in the sandboxes covers all 64 files.

Problem 4: what "drop the csd 6.7.2-2 triplet" touches. `grep '6.7.2-2'` matches 7 files: the 3 `cinnamon-settings-daemon-6.7.2-2` files plus 4 `cinnamon-desktop-6.7.2-2` files of a different package. Only the 3 settings-daemon files were dropped; the 4 desktop files stayed (and are in the final 64).

**Mechanism decision and dual-signature behavior (recorded per plan).** Decision: Option A. `rpm --addsign` is refused on the old-key files (`already contains a legacy signature`), so no file in the published set carries a dual signature; the empirical dual-signature question the plan posed (does a consumer holding only the new key accept a dual-signed file) is answered in the strong form: there is exactly one signature per file, by the tracked subkey, and tracked-key-only consumers accept all 64 while old-key-only consumers reject all 64 (the old key remains published only at `v1.0.0`, per F6).

**Execution (commands).**
1. Backup: `cp -a` of staging to `/tmp/opencode/task38/staging-pre-resign` (68 files; `diff -rq` identical).
2. Re-sign loop `/tmp/opencode/task38/item5-resign-loop.sh`: `PRESET_PASSPHRASE` once (signing subkey keygrip `CB22A20E1EEEED712E3629F31C4F7AA58B918239`), then per non-tracked file `GNUPGHOME=~/.gnupg-cinnamon-rocky10 rpm --resign --define "_gpg_name metallinux Cinnamon for Rocky Linux (repo signing) <repo-signing@metalinux.dev>" <file>`; `CLEAR_PASSPHRASE` and agent kill on EXIT. Output: `total=67 resigned=64 skipped=3` RC=0 (skipped = the csd 6.7.2-3 triplet).
3. Drop exactly the 3 `cinnamon-settings-daemon-6.7.2-2` files from staging; 64 RPMs remain.
4. `SHA256SUMS` regenerated from the staged bytes (64 lines); `createrepo_c` on `staging/rpms/`.
5. Consumer sub-check per Problem 3 (script `/tmp/opencode/task38/item5-dnf-http-check.sh`), positive then negative, installroot rebuilt between runs.
6. Swap: `cp -a rpms /tmp/opencode/task38/item5-pre-swap-rpms` (`diff -rq` identical), `cp -a staging/rpms rpms.new`, verify `rpms.new` in full, then `rm -rf rpms && mv rpms.new rpms`.

**Changes**

| Path | What changed |
|---|---|
| `rpms/` (project root) | 64 RPMs now: 61 changed bytes (old-key signature replaced by tracked-subkey signature; payload untouched, `rpm2cpio` digests identical), 3 unchanged (csd 6.7.2-3 triplet, byte-identical to pre-change bytes); 3 deleted (csd 6.7.2-2 triplet) |
| `rpms/SHA256SUMS` | regenerated, 64 lines, all OK |
| `rpms/repodata/` | regenerated by `createrepo_c` (untracked, `.gitignore:13`; 4 files) |
| git state | `git status --short`: 62 `M` (61 RPMs + `SHA256SUMS`), 3 `D` (csd 6.7.2-2), 15 `??` (pre-existing untracked project files, not from this item) |
| host packages | installed this session: `rpm-sign-4.19.1.1-23.el10.x86_64`, `strace-6.12-3.el10.x86_64`, `dnf-plugins-core-4.7.0-10.el10.noarch` (provides `dnf download`) |
| `/tmp/opencode/task38/` | machine-local, not committed: `staging/` (the swapped set), `staging-pre-resign/` and `item5-pre-swap-rpms/` (restore points), `item5-resign-loop.sh`, `item5-dnf-http-check.sh`, `dnf-installroot/` (throwaway root), `dnf-http-pos.log` / `dnf-http-neg.log`, sandboxes `item5-root-tracked/` / `root-old/` |
| `~/.gnupg-cinnamon-rocky10` | used for signing; preset cleared and agent killed after the loop; keyring itself retained (host-local, needed for future signing) |

**Checks run.**
- Re-sign loop: `total=67 resigned=64 skipped=3`, RC=0.
- Tracked-only sandbox (`/tmp/opencode/task38/item5-root-tracked`), `rpm --root … -K` per file: staged 67/67 `signatures OK` after the loop; final 64/64 after the drop.
- Old-key-only sandbox (`/tmp/opencode/task38/root-old`): staged 67 → `OK=0 NOTOK=67`; final 64 → `OK=0 NOTOK=64`. Old signatures absent from every file.
- Byte identity of the 3 kept tracked files: `cmp` of each against `staging-pre-resign/` → all 3 identical.
- Payload identity: `rpm2cpio <file> | sha256sum` on every file present in both `staging-pre-resign/` and `staging/` → 63/63 identical (61 re-signed + the 2 tracked debug files the glob caught; the 3rd tracked file byte-identical per above).
- Drop: exactly the 3 `cinnamon-settings-daemon-6.7.2-2` files gone; `cinnamon-desktop-6.7.2-2` files (4) retained; 64 RPMs remain.
- `sha256sum -c SHA256SUMS` from `staging/rpms` and from published `rpms/` → 64 OK each, RC=0; `wc -l SHA256SUMS` → 64.
- `createrepo_c` on `staging/rpms/` → `64 packages`, RC=0; `repodata/` = 4 files; `dnf makecache` with `gpgcheck=1` on the staged repo → RC=0 (`Metadata cache created`).
- dnf consumer, POSITIVE (tracked `gpgkey`): RC=0; output shows `Importing GPG key 0xEB7FEF99` from `keys/cinnamon-rocky10-public.asc`, `Key imported successfully`, 22/22 packages downloaded from `task38staged`, `Complete!`.
- dnf consumer, NEGATIVE (old `gpgkey`, installroot rebuilt): RC=1; output shows `Importing GPG key 0xFDA02785` from `/tmp/opencode/task38/oldkey.asc`, `Key imported successfully`, `Import of key(s) didn't help, wrong key(s)?`, 22 × `Public key for … is not installed`, `Error: GPG check FAILED`.
- dnf-downloaded bytes: `sha256sum` of the 22 RPMs in the installroot dnf cache vs staged `SHA256SUMS` → 22/22 match (the consumer transferred the staged bytes).
- Per-file signer, published tree: `rpm -qpi <file> | grep -i 'key ID'` on all 64 → `14cf2c0a8a47323c` in every case, 0 unexpected (includes the 3 tracked files, which were never re-signed).
- Swap verification: `rpms.new` before the swap: 64 RPMs, `sha256sum -c` 64 OK, tracked-only sandbox 64/64, per-file signer 64/64; after the swap: `diff -rq staging/rpms rpms` → identical.
- `git status --short` after the swap: 62 `M` / 3 `D` / 15 pre-existing `??` (breakdown above).

**Competing priorities / trade-offs.**
- Replace, not dual-sign: consumers pinned to `v1.0.0` are unaffected (that tag keeps the old bytes and the old key); consumers of the new tag get a single-signature set. The old public key is deliberately not part of the new tag's published bytes.
- The dnf sub-check ran against a throwaway installroot holding a copy of the host rpm DB: host rpm state is unchanged (the keyring erase and the 22-package erase happened in the copy; the key imports happened into the copy during the runs). The only host-side side effects are the three installed packages (recorded) and one `rm -rf /var/cache/dnf` before the cache-relocation was found (host dnf package cache re-fetched on next use).
- Published `rpms/` now carries `repodata/` (untracked by design, F13): the host's broken `cinnamon-rocky10` repo file can now at least find metadata in the tree; the repo file's missing `baseurl` and the `setup-repo.sh` `KEY_ID` fix remain items 9's documented-path work, not this item's.
- `repodata/` hashes and `SHA256SUMS` describe the re-signed bytes; the item-1 snapshot manifest (`/home/howard/snapshots/TASK-0038/rpms.sha256`) no longer matches the 61 changed RPMs by design. Restore points: `staging-pre-resign/` (pre-sign) and `item5-pre-swap-rpms/` (pre-swap published tree).

**Flag for `## Security` (for Omega).** During the prior session's diagnosis, a `gpg --debug all`/ipc log captured the hex-encoded passphrase in a machine-local file. The log was destroyed, the preset was cleared, and the agent was killed; the value was never committed, pushed, uploaded, or moved off the machine, and no key rotation was performed (the value never left the host). Omega to assess whether rotation is warranted; if so, that is a new keypair plus re-sign cycle, recorded as its own step.

Item 5 acceptance met: every file in `rpms/` verifies against the tracked key only (tracked-only sandbox 64/64, old-key-only 0/64, per-file signer `14cf2c0a8a47323c` ×64), `sha256sum -c SHA256SUMS` → 64 OK, file count == 64, mechanism decision recorded (Option A via `rpm --resign`; `--addsign` infeasible, dual-signature behavior recorded). Next items: 6 and 7 remain independent; item 9 now has its GPG-side prerequisite done.

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
| | | | | |

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
