# TASK-0036 — Host reinstall: back up the state that lives outside ~/AI and ~/Linux

> **Section order below is fixed.** Each agent writes to its own section and no other. `Robotnik`
> reads only `## Status` and `## Next Actions`. Do not reorder, rename, or remove sections.

- **Created:** 2026-10-20

---

## Status

*Owner: `Robotnik`. Keep this SHORT and CURRENT — it is one of only two sections the PM reads, so a
stale entry means the whole loop runs on bad information.*

**Now:** Operator will reinstall Rocky Linux 10 on this host (2026-10-20). Operator statement:
anything placed under `~/AI` or `~/Linux` is automatically backed up. Everything the team owns
outside those two roots is in scope.

**Environment / scope:**
- Files in scope: `~/.gnupg-cinnamon-rocky10/` (new signing secret key, the only copy), `~/.gnupg-cinnamon-rocky10.passphrase/passphrase` (49 B, 600), host rpm keyring old public key `gpg-pubkey-fda02785-6ab101f4` (exists only in host and VM rpm keyrings, not in the repo), `/var/lib/libvirt/images/` (VM disks plus snapshots, 47.1 G total), `~/.config/team-chaotix/agentgateway.yaml` (758 B), `~/.local/bin/agentsmd` (8.8 MB standalone binary, not in any repo), `/usr/local/lib/node_modules/portless/` (npm module, symlink in `/usr/local/bin`)
- Already covered (verified 2026-10-20): `~/AI/projects/team-chaotix` (auto-backup plus GitHub origin), `~/Linux/projects/cinnamon-for-rocky10` (auto-backup plus GitHub origin), `~/AI/secrets/` (GitHub token, VM password; auto-backup), new signing public key (tracked in the canonical repo `keys/cinnamon-rocky10-public.asc`)
- Touches the DB schema: no
- Graphical UI: no
- Rocky Linux target: yes (the host itself)

**Unknowns:**
- Where the operator's automatic backup stores its copies (operator-owned, not verifiable from this host)
- Whether `portless` is a published npm package (if yes, the `/usr/local` copy is insurance, not the only copy)

**Operator steps (exactly):** (1) confirm the automatic backup picked up `~/AI/secrets/` (the two GPG files) and `~/AI/setup-backup/2026-10-20-host-reinstall/` (old public key, both Rocky VM files, agentgateway.yaml, agentsmd, portless/, SHA256SUMS). (2) Do not boot the installer until every DoD box is verified green. No other operator step.

---

## Definition of Done

*Owner: `Robotnik`, and nobody else. Written **before** any work starts. Objectively checkable —
if a box cannot be verified by looking at something, rewrite it.*

- [ ] Armored export of the new signing secret key in `~/AI/secrets/` (file mode 600, per the §4 one-file-per-secret pattern), verified: imports into a scratch keyring, primary fingerprint `2274BFE1BF28C051CD98675BEBD13108EB7FEF99` plus signing subkey `CD4958E1A421CBD6B56B7C5614CF2C0A8A47323C`, and the passphrase copy unlocks it
- [ ] Passphrase copy in `~/AI/secrets/` (file mode 600), byte-identical to `~/.gnupg-cinnamon-rocky10.passphrase/passphrase` (sha256 match, value never printed)
- [ ] Old public key `gpg-pubkey-fda02785-6ab101f4` extracted to a file under the auto-backup root, verified: it verifies an old-key-signed repo RPM (a `-2` RPM from `rpms/`) in a scratch rpmdb
- [ ] `Rocky_Linux_10_Cinnamon.qcow2` plus its `2026-10-04T11:36` snapshot copied under `~/AI`, byte-verified against the source (sha256 or cmp); the Fedora VM is recorded as re-provisionable (state fully recorded in TASK-0033) instead of copied, because `/` has 34 G free and all four VM files are 47.1 G
- [ ] `agentgateway.yaml`, the `agentsmd` binary, and the `portless` module directory copied under `~/AI` with sha256 recorded for each
- [ ] No secret value (passphrase, secret key material, token) written to any planning doc, commit, log, or command string in this task
- [ ] `Shadow`: no unresolved blockers or should-fix findings in `## Review`
- [ ] `Omega`: no unresolved findings above `low` in `## Security`
- [ ] `Big`: all harness checks PASS, with no silently dropped checks
- [ ] `Charmy`: no unresolved findings in `## License (Charmy)`
- [ ] Any operator step that remains is written exactly in `## Status`

---

## Next Actions

*Owner: whoever wrote last. The future only — delete what has been done. The second of the two sections
the PM reads.*

- [ ] Review chain: `Shadow`, then `Omega`, then `Big`, then `Charmy`.
- [x] `Knuckles`: commit and push the planning-doc bookkeeping for this round (team-chaotix `planning/` only).

---

## Plan

*Owner: `Amy`.*

**Why this task exists** — the operator reinstalls Rocky Linux 10 on this host (2026-10-20). Operator rule: anything under `~/AI` or `~/Linux` is automatically backed up; everything the team owns outside those roots is wiped. This task creates byte-verified copies of the in-scope assets under those roots before the wipe: the new signing key material (the only copy), the old public key (only in host and VM rpm keyrings), the Rocky VM disk plus its snapshot (25 G of the 47.1 G of all four VM files), and the three host-installed tools (`agentgateway.yaml`, `agentsmd`, `portless`).

**What it unblocks / what blocks it** — unblocks the safe reinstall: after this task, the operator can boot the installer without losing signing capability or the only copy of the Rocky VM state. Nothing blocks it in-repo. One external dependency: the operator's automatic backup actually covering `~/AI` (operator-attested; storage location unverifiable from this host, `## Status` unknown #1).

**MVP** — all artifacts plus their verifications; no subset. A partial backup is indistinguishable from a lost asset, so there is no smaller version that delivers value. Deferred: the Fedora VM disk copy (space: 34 G free on `/` against 47.1 G of all four VM files; the Fedora VM is re-provisionable, state recorded in TASK-0033) and the restore procedure (post-reinstall task, not this one).

**What this makes harder later.**
- The signing secret then exists in three places: the live keyring, `~/AI/secrets/`, and the operator's off-host auto-backup store. Each copy is a credential; the store's security is operator-owned.
- The 25 G disk copy sits under `~/AI`. If the operator's auto-backup has a size limit, this is the part most likely to be silently dropped (`## Status` unknown #1).
- The Fedora VM is re-creatable only from the TASK-0033 record. After the reinstall, any inaccuracy in that record is permanent.
- The old public key backup is extracted from git history (`a70aedc`); if the canonical repo's history is ever rewritten (the git-squash fallback has happened here before), the standalone `.asc` in the backup directory is the surviving copy.

**Work breakdown** — all `Tails`-owned, one item per turn. All paths, sizes, and modes below were verified 2026-10-20 (facts block at the end of this section). Naming of the two secret files follows the TASK-0027 2026-10-18 handoff convention (`gpg-secret-key` / `gpg-passphrase`); extensions are the real formats. Constraint held in every item: no secret value enters any doc, log, or command string; digests and paths only.

| # | Item | Owner agent | Acceptance criterion | Parallel with |
|---|---|---|---|---|
| 1 | Preflight inventory (read-only): every source at expected size/mode; `df /` free ≥ 26 G; `sudo -n` works; `virsh list --all` shows no Cinnamon domain running; `a70aedc:keys/cinnamon-rocky10-public.asc` reachable with old-key fingerprint; a `-2` RPM candidate present in `rpms/`; create backup dir `~/AI/setup-backup/2026-10-20-host-reinstall/` (mode 700) | `Tails` | Inventory block recorded in `## Implementation`, every line matches, no gate fails | — (first) |
| 2 | Export the secret key: `gpg --homedir ~/.gnupg-cinnamon-rocky10 --armor --export-secret-keys` to `~/AI/secrets/gpg-secret-key.asc`; copy the passphrase to `~/AI/secrets/gpg-passphrase.txt`; both mode 600; sha256 both files source and copy; no value ever printed | `Tails` | `stat` mode 600 on both; sha256 source == copy for each (digests recorded, value never printed) | after 1; ∥ with 4, 5, 6 |
| 3 | Verify the export in a scratch keyring `/tmp/opencode/t0036-gnupg-*`: import, `--list-secret-keys --with-fingerprint`, loopback sign with `--passphrase-file ~/AI/secrets/gpg-passphrase.txt` (the copy, not the source), `--verify`; then shred the scratch keyring and test files, remove the directory | `Tails` | primary `2274BFE1...F99` and subkey `CD4958E1...3C` both listed; sign plus verify OK (proves the passphrase copy unlocks the export); scratch directory gone | after 2 |
| 4 | Extract the old public key: `git show a70aedc:keys/cinnamon-rocky10-public.asc > ~/AI/setup-backup/2026-10-20-host-reinstall/gpg-pubkey-fda02785-6ab101f4.asc`; check fingerprint via `gpg --show-keys`; scratch rpmdb: `rpm --root /tmp/opencode/t0036-rpmroot --initdb`, `rpm --root ... --import <file>`, `rpm --root ... -Kv <the -2 RPM from rpms/>` | `Tails` | fingerprint == `1689676AF4D4F6FEC142B4429C0A8912FDA02785`; `rpm -Kv` reports signature OK on a `-2` RPM from `rpms/` | after 1; ∥ with 2/3, 5, 6 |
| 5 | Copy `Rocky_Linux_10_Cinnamon.qcow2` (21 G) and `Rocky_Linux_10_Cinnamon.2026-10-04T11:36` (4.0 G) into the backup directory: `sudo cp -a`, then `chown howard:howard`, `chmod 600`; re-check `virsh list --all` and `df` immediately before copying; sha256 both files source and copy (source hashed after the copy); record `sudo qemu-img info` for both files (backing chain, for restore knowledge) | `Tails` | sizes match; 2×2 sha256 pairs match; no Cinnamon domain running at copy time; `qemu-img info` recorded | after 1; ∥ with 2/3, 4, 6 |
| 6 | Copy `agentgateway.yaml` (758 B), `agentsmd` (8831160 B), `portless/` (504 K) into the backup directory (`cp -p` / `cp -a`); sha256 each small file source and copy; `portless/` per-file sha256 manifest both sides, diff empty; record the local portless version and the symlink target `/usr/local/bin/portless -> ../lib/node_modules/portless/dist/cli.js` | `Tails` | all digests and the manifest match, recorded | after 1; ∥ with 2/3, 4, 5 |
| 7 | Write `SHA256SUMS` in the backup directory (non-secret digests only); self-audit: no secret value (passphrase, key material, token) in any doc, log, or command string of this task; re-verify the scratch keyring is shredded; complete `## Implementation` evidence | `Tails` | every DoD box verifiable from file state plus `## Implementation` | after 2, 3, 4, 5, 6 |

**Critical path:** 1 → 2 → 3 → 7 (the secret-credential chain: export, then its functional verification, then the audit). Items 4, 5, and 6 are independent of 2/3 and of each other (different sources, disjoint destination files); they may run in any order after 1. Item 5 is the longest in wall time (≈ 25 G copied plus 50 G hashed) but is not on the dependency chain. Total: 7 `Tails` turns plus one spare re-brief against §14 truncation.

**Estimates.** Wall-clock minutes, three-point, `T = (O + 4M + P) / 6`.

| Item | O | M | P | T |
|---|---|---|---|---|
| 1 | 3 | 5 | 10 | 5.2 |
| 2 | 2 | 4 | 8 | 4.3 |
| 3 | 3 | 6 | 12 | 6.3 |
| 4 | 3 | 6 | 15 | 7.2 |
| 5 | 15 | 25 | 45 | 25.0 |
| 6 | 2 | 4 | 8 | 4.3 |
| 7 | 3 | 5 | 10 | 5.2 |

ΣT ≈ 57.5 min plus a 30 min buffer (≈ 30%: gpg/rpm edge cases, disk I/O variance) ≈ 90 min.

**Risks.**

| Risk | Likelihood | Impact | Mitigation | Contingency |
|---|---|---|---|---|
| Truncated disk copy (disk fills) | low | high | preflight plus pre-copy `df` gate (≥ 26 G free); size check; sha256 both sides | delete the truncated copy (the revert), free space, re-run item 5 |
| Source changed during/after the copy (a Cinnamon VM running) | low | high | preflight plus pre-copy `virsh list` gate (no Cinnamon domain exists today); source hashed after the copy, so even a mid-copy change fails sha256 | stop and report; PM decides (shut the domain down for a consistent copy) |
| Old-key source gap: the `a70aedc` file differs from the rpmdb key or is unreachable | low | high | item 1 checks reachability plus fingerprint; the DoD oracle (scratch `rpm -Kv`) is the final arbiter | stop and report; worst case the old key is host-lost and the 64 old RPMs are unverifiable under `gpgcheck=1`, operator decides |
| Passphrase copy wrong or un-usable | low | critical | sha256 byte-identity; item 3's unlock test uses the copy, a functional proof | re-copy from the source (the source survives until the reinstall) |
| Scratch keyring (holds the secret key) left in `/tmp` | low | medium | item 3 acceptance includes shred plus removal; item 7 re-verifies | `shred -u` then `rm -rf` on sight |
| Auto-backup silently drops the 25 G copy (size limit) | unknown | high | files live under `~/AI` per the operator's statement; item 7 emits the exact file list for operator confirmation (`## Status` unknown #1) | operator copies the two paths off-host manually before the reinstall |

**Validation.** Files and checks (no UI pages; `Graphical UI: no`):
- `~/AI/secrets/gpg-secret-key.asc` (600): scratch-keyring import lists primary `2274BFE1BF28C051CD98675BEBD13108EB7FEF99` plus subkey `CD4958E1A421CBD6B56B7C5614CF2C0A8A47323C`; loopback sign with `--passphrase-file` plus `--verify` OK.
- `~/AI/secrets/gpg-passphrase.txt` (600): sha256 == `~/.gnupg-cinnamon-rocky10.passphrase/passphrase` (49 B); value never printed.
- `~/AI/setup-backup/2026-10-20-host-reinstall/gpg-pubkey-fda02785-6ab101f4.asc`: `gpg --show-keys` fingerprint `1689676AF4D4F6FEC142B4429C0A8912FDA02785`; scratch rpmdb `--import` plus `rpm -Kv` on `rpms/cinnamon-desktop-6.7.2-2.el10.x86_64.rpm` reports "digests signatures OK".
- `Rocky_Linux_10_Cinnamon.qcow2` and `Rocky_Linux_10_Cinnamon.2026-10-04T11:36`: sizes match, sha256 source == copy for each.
- `agentgateway.yaml`, `agentsmd`, `portless/`: sha256 source == copy (`portless/`: per-file manifest, diff empty).
- Human look: the operator reads the two remainder steps in `## Status` before the reinstall; no other page.

**Rollback.** The work is copies-only: no source is modified, no service is touched, `sudo` is used only to read the `qemu:qemu` 600 disks and to `chown`/`chmod` the copies.
- What makes a copy invalid: (1) truncation from a full disk → size or sha256 mismatch; (2) source changed during the copy (a running domain) → sha256 source-vs-copy mismatch (source is hashed after the copy, so this is always detectable); (3) wrong old-key revision → fingerprint check fails; (4) partial secret-key export (missing subkey) → the fingerprint-list check fails; (5) passphrase copy of a different file → sha256 mismatch.
- Exact revert: `rm` the bad copy (and `rm -rf` the scratch directory). Sources are untouched in every case.
- Point of no return: the operator's reinstall itself. During team work there is none (every output is a new, deletable file). Once the installer boots, the sources (host rpmdb, `/var/lib/libvirt`, `/usr/local`, `~/.config`, `~/.local/bin`, `~/.gnupg-*`) are gone and an invalid or missing copy can no longer be remediated. Gate: every DoD box green before the operator starts.

**Operator remainder** (exactly; Robotnik transcribes to `## Status`):
1. Before starting the reinstall, confirm the operator's automatic backup picked up `~/AI/secrets/gpg-secret-key.asc`, `~/AI/secrets/gpg-passphrase.txt`, and `~/AI/setup-backup/2026-10-20-host-reinstall/` (the whole directory); if coverage is in doubt, copy those two paths off-host manually first.
2. Do not boot the installer until every DoD box in this doc is verified.
No other operator step. Restore knowledge for the post-reinstall task (recorded in `## Implementation`): import the `.asc` into a fresh keyring and recreate the passphrase file at the sign-rpms.sh-mandated location; `rpm --import` the old public key; re-create the VMs from the TASK-0033 record (backing chain recorded by item 5); reinstall `portless` (published on npm, 0.15.8; the local copy is insurance) plus the `/usr/local/bin` symlink.

**Facts verified by Amy (2026-10-20).**
- `df -h /`: 70 G total, 37 G used, 34 G free. `ls -lh /var/lib/libvirt/images/`: `Rocky_Linux_10_Cinnamon.qcow2` 21 G plus `Rocky_Linux_10_Cinnamon.2026-10-04T11:36` 4.0 G (both mode 600, `qemu:qemu`), `Fedora_45_Cinnamon.qcow2` 21 G plus `Fedora_45_Cinnamon.2026-10-04T11:37` 1.1 G, all four 47.1 G. `virsh list --all`: no Cinnamon domain exists (`win10-2026-10-20` running only), so no live-write risk on the disks. `sudo -n -l`: `howard` has `NOPASSWD: ALL`.
- `gpg --homedir ~/.gnupg-cinnamon-rocky10 --list-secret-keys --with-fingerprint`: primary `2274BFE1BF28C051CD98675BEBD13108EB7FEF99` [SCEAR] present (created 2026-10-19); keyring dir mode 700. `ls -la ~/.gnupg-cinnamon-rocky10.passphrase/`: `passphrase` file, 49 B, mode 600.
- `rpm -q gpg-pubkey-fda02785-6ab101f4`: present in the host rpmdb; `rpm -ql` on it: "(contains no files)" (key bytes live only in the rpmdb). `git show a70aedc:keys/cinnamon-rocky10-public.asc | gpg --show-keys --with-fingerprint`: old key, fingerprint `1689676AF4D4F6FEC142B4429C0A8912FDA02785`; `git merge-base --is-ancestor a70aedc origin/main`: yes (old key also on GitHub). Current tree `gpg --show-keys keys/cinnamon-rocky10-public.asc`: new key `2274BFE1...F99` only, so "not in the repo" holds for the working tree.
- `ls -l rpms/cinnamon-desktop-6.7.2-2.el10.x86_64.rpm`: 330746 B, the `-2` verification candidate. `du -sh /usr/local/lib/node_modules/portless`: 504 K; `npm view portless version`: 0.15.8 (published; local copy is insurance). `ls -l ~/.config/team-chaotix/agentgateway.yaml ~/.local/bin/agentsmd`: 758 B and 8831160 B. `ls -la ~/AI/secrets/`: dir mode 700 holding three existing mode-600 files, no name collision with `gpg-secret-key` / `gpg-passphrase`. `/tmp/opencode` exists for the scratch keyring and rpmdb.

---

## Implementation

*Owner: `Tails`.*

**Alternatives considered**

### Problem: integrity proof for the 25 G disk copy against a source that could change mid-copy
**Option A — `cp -a` plus sha256 of source and copy, source hashed after the copy.** How: `sudo cp -a` (read-only on the source), then `sha256sum` both sides. Pros: catches both truncation and mid-copy drift (a source that changes during the copy surfaces as a source-vs-copy mismatch); digests are permanent restore records. Cons: hashes 50 G.
**Option B — `rsync --checksum`.** How: one pass that copies and checksums. Pros: single pass. Cons: no portable source-vs-copy digest record; the checksum lives inside rsync, not in a manifest.
**Option C — `cmp` byte compare.** How: `cmp source copy`. Pros: fast. Cons: no digest for the manifest; records nothing the operator can re-check later.
**Chosen:** A, because the DoD requires recorded sha256 pairs and the post-copy source hash is the only way to detect a source that changed during the copy (task hard rule).
**Competing priorities:** wall time. Item 5 hashes 50 G and item 7 re-hashes the whole manifest via `sha256sum -c SHA256SUMS`, traded for a final gate over every file in the backup dir.

### Problem: where the scratch keyring (which briefly holds the secret key) and the scratch rpmdb live
**Option A — `/tmp/opencode` (the pre-approved scratch root).** How: fresh dir, mode 700, `shred -u` every file, `rm -rf`, verify absence. Pros: approved for scratch; isolated from the live keyring and the host rpmdb; item 1 verified `/tmp` is on `/`, so shred passes are real. Cons: /tmp is a shared location on the host.
**Option B — inside the backup dir.** How: scratch under `~/AI/setup-backup/...`. Pros: same filesystem as the artifacts. Cons: any shred leftover sits next to artifacts and could ride into the operator's auto-backup; the backup dir should hold only finished artifacts.
**Chosen:** A, because the backup dir must contain only verified artifacts and the plan fixes the scratch root at `/tmp/opencode`.
**Competing priorities:** shred strength depends on the storage not being tmpfs or encrypted at rest; item 1 verified `/tmp` is on the root filesystem, so shred is real.

### Problem: how to functionally verify the old public key without touching host state
**Option A — scratch rpmdb via `rpm --root` + `--initdb`.** How: `rpm --root <scratch> --initdb`, `--import`, `rpm -Kv` on the -2 RPM. Pros: zero impact on the host rpmdb; exactly the DoD oracle. Cons: `--initdb` is deprecated (still functional in RPM 4.19.1.1, verified in item 1).
**Option B — import into the host rpmdb, verify, remove.** How: `rpm --import` globally, then `rpm -e gpg-pubkey-fda02785-6ab101f4`. Pros: no scratch. Cons: modifies host state mid-task, against the copies-only rollback constraint, and the removal step has its own failure modes.
**Chosen:** A, because the rollback section forbids modifying any source and the scratch root is destroyed after verification.

**Competing priorities (task-wide):** the Fedora VM disk copy was skipped (34 G free against 47.1 G of all four VM files; the Fedora VM is re-provisionable from the TASK-0033 record) and the restore procedure was deferred (post-reinstall task, per plan MVP).

**Changes**

| File | What changed |
|---|---|
| `~/AI/secrets/gpg-secret-key.asc` (new, 600) | armored export of the new signing secret key (primary plus signing subkey); the only off-keyring copy of the secret material |
| `~/AI/secrets/gpg-passphrase.txt` (new, 600) | byte-identical copy of `~/.gnupg-cinnamon-rocky10.passphrase/passphrase` (sha256 match; value never printed) |
| `~/AI/setup-backup/2026-10-20-host-reinstall/` (new, 700) | backup dir per plan |
| `.../gpg-pubkey-fda02785-6ab101f4.asc` | old public key extracted from `a70aedc:keys/cinnamon-rocky10-public.asc` (cinnamon repo) |
| `.../Rocky_Linux_10_Cinnamon.qcow2` (600) | read-only `cp -a` copy of the VM disk |
| `.../Rocky_Linux_10_Cinnamon.2026-10-04T11:36` (600) | read-only `cp -a` copy of the snapshot disk |
| `.../agentgateway.yaml`, `.../agentsmd`, `.../portless/` | `cp -p` / `cp -a` copies of the three host-installed tools |
| `.../SHA256SUMS` (600) | non-secret digest manifest for the whole dir |
| `/tmp/opencode/t0036-gnupg`, `/tmp/opencode/t0036-rpmroot` (plus the one-shot `t0036-initdb-probe` probe root and the two portless manifest files) | scratch keyring / scratch rpmdb; created, verified, shredded, removed |
| `planning/docs/TASK-0036-host-reinstall-backup.md` | this section (evidence) |

**Checks run:** no compile / linter / harness applies (shell-only task). Verification is the per-item gates below; final gate `sha256sum -c SHA256SUMS` in item 7: PASS (12/12 files OK).

### Item 1 — preflight inventory (read-only), 2026-10-20

Commands: `df -h /`, `df -h /tmp`, `virsh list --all`, `sudo -n -l`, `stat -c` per source, `gpg --homedir ~/.gnupg-cinnamon-rocky10 --list-secret-keys --with-fingerprint --fingerprint`, `git show a70aedc:keys/cinnamon-rocky10-public.asc | gpg --show-keys --with-fingerprint` (run in `~/Linux/projects/cinnamon-for-rocky10`), `rpm -q gpg-pubkey-fda02785-6ab101f4`, `ls -l /var/lib/libvirt/images/`, `stat -c` on tool files, `mkdir -p` plus `chmod 700` on the backup dir (the only write).

- `df -h /`: `/` 70 G total, 34 G free (>= 26 G gate: PASS). `df -h /tmp`: `/tmp` is on `/` (same filesystem, so shred of scratch files is real, not tmpfs).
- `virsh list --all`: only `win10-2026-10-20` running; no Cinnamon domain exists (no live-write risk on the VM disks).
- `sudo -n -l`: `howard` has passwordless sudo (gate: PASS).
- `~/.gnupg-cinnamon-rocky10`: mode 700 howard:howard. Live keyring lists primary `2274BFE1BF28C051CD98675BEBD13108EB7FEF99` [SCEAR] and subkey `CD4958E1A421CBD6B56B7C5614CF2C0A8A47323C` [SEA]; both match the DoD.
- `~/.gnupg-cinnamon-rocky10.passphrase/passphrase`: 49 B, mode 600, howard:howard.
- `/var/lib/libvirt/images/`: `Rocky_Linux_10_Cinnamon.qcow2` 21478375424 B and `Rocky_Linux_10_Cinnamon.2026-10-04T11:36` 4262592512 B, both mode 600 qemu:qemu (plus the two Fedora files, out of scope).
- `~/.config/team-chaotix/agentgateway.yaml`: 758 B. `~/.local/bin/agentsmd`: 8831160 B. `portless/`: 504 K.
- Old key: `a70aedc` is a commit in `~/Linux/projects/cinnamon-for-rocky10` (`git merge-base --is-ancestor a70aedc origin/main`: yes), and `git show a70aedc:keys/cinnamon-rocky10-public.asc | gpg --show-keys --with-fingerprint` gives `1689676AF4D4F6FEC142B4429C0A8912FDA02785`. Host rpmdb has `gpg-pubkey-fda02785-6ab101f4`. Current tree key: the new key only.
- -2 RPM candidate: `~/Linux/projects/cinnamon-for-rocky10/rpms/cinnamon-desktop-6.7.2-2.el10.x86_64.rpm`, 330746 B. Deviation from the plan's relative path `rpms/`: that dir is in the cinnamon project, not in team-chaotix; the file and size match the plan's facts, so this is a plan path slip, not a missing file.
- `~/AI/secrets/`: mode 700, holds `githubtoken.md`, `pass.txt`, `token.md`; no name collision with `gpg-secret-key` / `gpg-passphrase`.
- No pre-existing `/tmp/opencode/t0036-*` scratch dirs; `/tmp/opencode` exists.
- Backup dir created: `~/AI/setup-backup/2026-10-20-host-reinstall`, mode 700 howard:howard.

Gate: every line matches the plan's facts block; no gate failed.

### Item 2 — secret key export and passphrase copy, 2026-10-20

Commands: `cp` of the source passphrase to `~/AI/secrets/gpg-passphrase.txt` (mode 600), then `gpg --homedir ~/.gnupg-cinnamon-rocky10 --pinentry-mode loopback --passphrase-file ~/AI/secrets/gpg-passphrase.txt --armor --export-secret-keys > ~/AI/secrets/gpg-secret-key.asc` (mode 600), then `stat -c` and `sha256sum` on both copies plus the source passphrase. No secret value entered any command string; output was digests and metadata only.

- `~/AI/secrets/gpg-secret-key.asc`: 7589 B, mode 600 howard:howard, sha256 `f01d0cfbff9c0c06360e748cd3ac6c6bc5e61499954c0a066c1eecaba33d5c4f`.
- `~/AI/secrets/gpg-passphrase.txt`: 49 B, mode 600 howard:howard, sha256 `61cd6d2e2b9616244e5cb01658ca5de20bf85b778abefd86afc3ff342c282a21`.
- Source `~/.gnupg-cinnamon-rocky10.passphrase/passphrase`: 49 B, mode 600, sha256 `61cd6d2e2b9616244e5cb01658ca5de20bf85b778abefd86afc3ff342c282a21` — copy == source: PASS. Value never printed in either direction.

Gate: both copies mode 600; passphrase copy sha256-identical to source; secret-key digest recorded. PASS.

### Item 3 — scratch keyring functional verification, 2026-10-20

Commands (scratch homedir `/tmp/opencode/t0036-gnupg`, mode 700): `gpg --homedir <scratch> --import` of the exported `.asc`; `--list-secret-keys --with-fingerprint`; loopback clearsign of a scratch test message with `--pinentry-mode loopback --passphrase-file ~/AI/secrets/gpg-passphrase.txt` (the copy, not the source); `--verify` of the resulting signature; then `shred -u` of every scratch file and `rm -rf` of the directory.

- Import: exit 0.
- `--list-secret-keys --with-fingerprint`: primary `2274BFE1BF28C051CD98675BEBD13108EB7FEF99` and subkey `CD4958E1A421CBD6B56B7C5614CF2C0A8A47323C` both listed (matches the DoD).
- Loopback clearsign: exit 0 — the passphrase copy unlocks the export.
- `--verify`: "Good signature from metallinux Cinnamon for Rocky Linux (repo signing)".
- Teardown: `shred -u` plus `rm -rf` ran in the same script (tail of that output was truncated in the session record); verified this turn: `ls -d /tmp/opencode/t0036-gnupg` fails with "No such file or directory" (exit 2), no `t0036-gnupg*` entry remains in `/tmp/opencode`, and no scratch gpg-agent process runs (`pgrep -af 'gpg-agent.*t003[6]'`: no match).

Gate: both fingerprints listed; sign plus verify OK; scratch directory gone. PASS.

### Item 4 — old public key extraction and scratch rpmdb verification, 2026-10-20

Commands (run in `~/Linux/projects/cinnamon-for-rocky10`): `git show a70aedc:keys/cinnamon-rocky10-public.asc > ~/AI/setup-backup/2026-10-20-host-reinstall/gpg-pubkey-fda02785-6ab101f4.asc`; `gpg --show-keys --with-fingerprint` on the extracted file; `sha256sum`; scratch rpmdb: `mkdir -p /tmp/opencode/t0036-rpmroot`, `rpm --root <scratch> --initdb`, `rpm --root <scratch> --import <extracted file>`, `rpm --root <scratch> -Kv rpms/cinnamon-desktop-6.7.2-2.el10.x86_64.rpm`; then `shred -u` on every scratch file and `rm -rf` of the root.

- Extracted key `gpg-pubkey-fda02785-6ab101f4.asc`: 1713 B, mode 644, sha256 `5a0e4db80a4b514e0b8143a22c73f606278871d17ead787ea22369abed2a2e74`.
- `gpg --show-keys --with-fingerprint`: `1689 676A F4D4 F6FE C142 B442 9C0A 8912 FDA0 2785`, i.e. `1689676AF4D4F6FEC142B4429C0A8912FDA02785` (matches the plan); uid "metallinux Cinnamon for Rocky Linux (repo signing) <repo-signing@metalinux.dev>", rsa4096, created 2026-09-21.
- Scratch rpmdb (`rpm --version`: 4.19.1.1): `--initdb` exited 255 with no output and created no files (deprecated no-op in this build, confirmed on a fresh empty probe root the same turn); `--import` exited 0, auto-creating the db (modern rpm creates the db on first write); `rpm -Kv` on `rpms/cinnamon-desktop-6.7.2-2.el10.x86_64.rpm` (330746 B): exit 0, "Header V4 RSA/SHA256 Signature, key ID fda02785: OK" plus Header/Payload/MD5 digest lines all OK — the signature was checked against the key imported into the scratch root, not the host rpmdb.
- Teardown: every scratch file shredded, root removed; `ls -d /tmp/opencode/t0036-rpmroot` fails with "No such file or directory" (exit 2).

Gate: fingerprint matches; `rpm -Kv` reports signature OK on the -2 RPM. PASS.

### Item 5 — VM disk copies, 2026-10-20

Commands: `virsh list --all` plus `df -h /` immediately before the copy; `stat -c` on both sources; `sudo cp -a` of both sources into `~/AI/setup-backup/2026-10-20-host-reinstall/`; `chown howard:howard` plus `chmod 600` on both copies; `sha256sum` on both copies; `sudo sha256sum` on both sources (hashed after the copy); `qemu-img info` on both copies.

- Pre-copy gates: only `win10-2026-10-20` running, no Cinnamon domain; `/` 34 G free (>= 26 G). Sources: `Rocky_Linux_10_Cinnamon.qcow2` 21478375424 B and `Rocky_Linux_10_Cinnamon.2026-10-04T11:36` 4262592512 B, both mode 600 qemu:qemu.
- `sudo cp -a`: exit 0. Both copies mode 600 howard:howard, sizes equal to the sources (21478375424 B, 4262592512 B).
- sha256 (source hashed after the copy): main disk `7df7261fbcf470b102253a0468a760b62839a40c7885a6e68aa1ad7313954eab` copy == source: PASS; snapshot `8f4c5059eefc425b7e1704b8a72103f43932918c627d4f896a12c9ac8a9e5325` copy == source: PASS.
- `qemu-img info` (on the copies): main disk is qcow2, virtual 20 GiB, disk 10.5 GiB, no backing file (top of chain), compat 1.1. The snapshot file is qcow2 with backing file `/var/lib/libvirt/images/Rocky_Linux_10_Cinnamon.qcow2` (absolute source path, so a restore must rebase it via `qemu-img rebase` or place the pair at that same path) and one embedded snapshot `2026-10-07-task0034-pre` (1.62 GiB, dated 2026-10-08).

Gate: sizes match; both sha256 pairs match; no Cinnamon domain running at copy time; `qemu-img info` recorded. PASS.

### Item 6 — three host-tool copies, 2026-10-20

Commands: `cp -p` of `~/.config/team-chaotix/agentgateway.yaml` and `~/.local/bin/agentsmd`, and `cp -a` of `/usr/local/lib/node_modules/portless/`, all into `~/AI/setup-backup/2026-10-20-host-reinstall/`; `stat -c` plus `sha256sum` on both small files, source and copy; per-file sha256 manifest of `portless/` on both sides (`find . -type f -print0 | sort -z | xargs -0 sha256sum`, run from each directory) compared with `diff`; `find -type l` on both sides (symlink check); `grep '"version"'` on the local `package.json`; `ls -l /usr/local/bin/portless`.

- `agentgateway.yaml`: 758 B, mode 644, sha256 `ce303a3cd6db76987983830eb39b64f2cfe7bc7140ccce68cce6e38511280748` source == copy: PASS.
- `agentsmd`: 8831160 B, mode 755, sha256 `1575c365144886e71ffaba88c7e5bab7609489f9567d3b46dd0df9772cd76774` source == copy: PASS.
- `portless/`: 504 K, 7 regular files, no symlinks on either side; per-file manifest diff empty (exit 0).
- Local portless version: 0.15.6 (`/usr/local/lib/node_modules/portless/package.json`). Note: the newest published npm version was 0.15.8 at item 1, so restoring from this copy yields exactly 0.15.6, the version the host was running, not the newer published one.
- Symlink to recreate: `/usr/local/bin/portless -> ../lib/node_modules/portless/dist/cli.js`.

Gate: all digests and the manifest match, recorded. PASS.

### Item 7 — manifest, final gate, self-audit, 2026-10-20

Commands: from the backup directory, `find . -type f -not -name SHA256SUMS -print0 | sort -z | xargs -0 sha256sum > SHA256SUMS`, `chmod 600 SHA256SUMS`, `sha256sum -c SHA256SUMS` (final gate; re-hashes the whole directory); `ls -la` of the backup directory; `sha256sum` of the two `~/AI/secrets/` files (digests only); `ls -d /tmp/opencode/t0036-*`; `grep -n "BEGIN PGP PRIVATE KEY BLOCK"` plus a long-line scan on this doc.

- `SHA256SUMS`: 1112 B, mode 600 howard:howard; covers all 12 files in the backup dir (`agentgateway.yaml`, `agentsmd`, `gpg-pubkey-fda02785-6ab101f4.asc`, the 7 `portless/` files, both VM disks). Non-secret digests only.
- Final gate `sha256sum -c SHA256SUMS`: all 12 files OK, exit 0.
- Backup dir contents (for operator confirmation): `agentgateway.yaml` 758 B, `agentsmd` 8831160 B, `gpg-pubkey-fda02785-6ab101f4.asc` 1713 B, `portless/` (7 files), `Rocky_Linux_10_Cinnamon.qcow2` 21478375424 B (600), `Rocky_Linux_10_Cinnamon.2026-10-04T11:36` 4262592512 B (600), `SHA256SUMS` 1112 B (600); dir mode 700.
- Secret re-check: sha256 of `~/AI/secrets/gpg-secret-key.asc` is `f01d0cfbff9c0c06360e748cd3ac6c6bc5e61499954c0a066c1eecaba33d5c4f` and of `gpg-passphrase.txt` is `61cd6d2e2b9616244e5cb01658ca5de20bf85b778abefd86afc3ff342c282a21`, unchanged since item 2; values never re-printed.
- Scratch re-verification: no `t0036-*` entry remains in `/tmp/opencode` (scratch keyring, scratch rpmdb, the one-shot `t0036-initdb-probe` probe root, and the two portless manifest files all shredded/removed).
- Doc self-audit: the "BEGIN PGP PRIVATE KEY BLOCK" marker string occurs in prose references (the item 7 command list and this sentence), never as a standalone armor line; the no-leak proof does not rest on that marker; no line in this doc is a base64-only run (an armored key line is at most 64 chars, and there are zero base64-only lines), so no armored private-key block is present and a block cannot hide in a long line; 47 lines exceed 250 chars, all plan/Status prose or table rows (longest 584, the plan's Why paragraph); no command string of this task ever `cat`/`echo`ed a secret value — every passphrase operation used `--passphrase-file` and printed digests only.

Gate: final gate PASS; every DoD box within Tails' scope is verifiable from file state plus this section.

---

## Review

*Owner: `Shadow`. Read-only — findings only, no edits. Severity order, blockers first.*

### Operator remainder steps not transcribed into ## Status
**Severity:** should-fix
**Where:** plan `## Plan` Operator remainder, line 129 ("Robotnik transcribes to `## Status`"), vs `## Status` (lines 10-27) and `## Next Actions` (lines 51-57)
**Problem:** the two operator remainder steps from the plan are not in `## Status`, and no action in `## Next Actions` assigns the transcription, so the DoD box "Any operator step that remains is written exactly in `## Status`" is false and unowned.
**Failure scenario:** operator begins the reinstall by reading `## Status` (the plan's own "Human look" validation says the operator reads "the two remainder steps in `## Status`" before the reinstall) → the step "confirm the automatic backup picked up `~/AI/secrets/gpg-secret-key.asc`, `~/AI/secrets/gpg-passphrase.txt`, and the whole backup dir" and the gate "do not boot the installer until every DoD box is verified" are not visible at the decision point → if the automatic backup silently dropped the 25 G copy (the plan's risk row rates this "unknown" likelihood), the only copies of the VM state and the secret key material are lost with the reinstall, and the gate that was meant to stop that never appears.
**Suggested direction:** Robotnik transcribes the two steps verbatim into `## Status` (Robotnik's section, not a Tails fix). Tails adds a `## Next Actions` line naming the transcription as a Robotnik action, so the box is visibly owned and can be checked only after the transcription lands.
**Resolution:** resolved by Robotnik 2026-10-20 (section owner): operator steps transcribed to `## Status` verbatim per the operator model; no `## Next Actions` agent line needed since the operator is not a dispatched agent

### DoD box verification against recorded evidence (no blockers)

| DoD box | Verdict | Recorded evidence |
|---|---|---|
| Secret key export in `~/AI/secrets/`, mode 600, scratch import, both fingerprints, passphrase-copy unlock | PASS | item 2: `gpg-secret-key.asc` 7589 B, mode 600, digest recorded; item 3: scratch import exit 0, `--list-secret-keys` lists `2274BFE1…F99` plus `CD4958E1…3C`, loopback clearsign with `--passphrase-file ~/AI/secrets/gpg-passphrase.txt` (the copy, not the source) exit 0, `--verify` OK; item 7 re-checks: no `t0036-*` entry left, no scratch gpg-agent process |
| Passphrase copy mode 600, byte-identical to source, value never printed | PASS | item 2: 49 B, mode 600, sha256 `61cd6d2e…2a21` == source; every passphrase operation in the recorded commands uses `cp` or `--passphrase-file`, output is digests and metadata only |
| Old public key extracted under the auto-backup root, verifies a `-2` RPM in a scratch rpmdb | PASS | item 4: extracted file 1713 B, fingerprint `1689676AF4D4F6FEC142B4429C0A8912FDA02785`; fresh scratch root whose keyring contains exactly one import (the extracted file, `--import` exit 0); `rpm -Kv` on `rpms/cinnamon-desktop-6.7.2-2.el10.x86_64.rpm` (330746 B) exit 0 with "key ID fda02785: OK" |
| Rocky VM disk plus `2026-10-04T11:36` snapshot copied under `~/AI`, byte-verified; Fedora VM recorded as re-provisionable | PASS | item 5: sizes 21478375424 B / 4262592512 B match the sources, both sha256 pairs match with the sources hashed after the copy, no Cinnamon domain running at copy time, `qemu-img info` recorded (main disk top of chain, snapshot carries the absolute backing path, embedded snapshot `2026-10-07-task0034-pre` noted); Fedora deferral per plan MVP, TASK-0033 exists and records the Fedora VM state (session state, 13-package inventory, screenshots) |
| `agentgateway.yaml`, `agentsmd`, `portless/` copied under `~/AI` with sha256 each | PASS | item 6: sha256 source == copy for `agentgateway.yaml` (758 B) and `agentsmd` (8831160 B); `portless/` 7-file per-file manifest diff empty (exit 0), no symlinks on either side; local version 0.15.6 and the `/usr/local/bin/portless` symlink target recorded |
| No secret value in any planning doc, commit, log, or command string of this task | PASS | item 7 self-audit (no armor marker, zero base64-only lines, `--passphrase-file` only, digests only) plus my full read of this doc: no "BEGIN PGP" line anywhere, no 49 B token-like value, the 47 lines over 250 chars are plan/Status prose and table rows; the Knuckles commit carries this doc only |
| `Shadow` / `Omega` / `Big` / `Charmy` boxes | open | this review: no blockers, one should-fix open (owner Robotnik); Omega, Big, Charmy pending in the chain |
| Any operator step written exactly in `## Status` | OPEN | finding above |

`SHA256SUMS` gate: 12 files = `agentgateway.yaml` + `agentsmd` + `gpg-pubkey-fda02785-6ab101f4.asc` + 7 `portless/` files + 2 VM disks; `sha256sum -c SHA256SUMS` exit 0, all 12 OK (item 7). The count matches the backup-dir contents list in the same item. The two `~/AI/secrets/` files are correctly outside the manifest (different directory); their digests are recorded in items 2 and 7 and re-checked unchanged in item 7.

### Recorded deviations, soundness

- **`rpm --initdb` exit 255, no-op (item 4):** sound. The one-shot probe root (`t0036-initdb-probe`, shredded per item 7) confirms the no-op is this RPM 4.19.1.1 build's behavior (no files created), not a broken db; `--import` exit 0 auto-created the db, so the subsequent `rpm -Kv` ran against a scratch root whose keyring holds exactly one key, the extracted file. "key ID fda02785: OK" therefore proves the extracted key, not the host rpmdb, verified the `-2` RPM.
- **`qemu-img rebase` restore gotcha (item 5):** sound and correctly recorded. The main disk is top of chain (no backing file); only the snapshot file carries the absolute backing path `/var/lib/libvirt/images/Rocky_Linux_10_Cinnamon.qcow2`, so a restore rebases it or places the pair at that same path. The embedded snapshot lives inside the snapshot file and survives a byte copy.
- **portless 0.15.6 vs 0.15.8 (items 1 and 6):** sound, no contradiction. The backup is of what the host was running (0.15.6 per the local `package.json`); the plan's 0.15.8 is the npm-published version, an availability note ("the local copy is insurance"), and the item 6 note disambiguates: restore from the backup dir yields exactly 0.15.6, a fresh npm install would yield 0.15.8. Faithful restore is 0.15.6.

**Verdict:** no blockers. Every Tails-owned DoD box verifies against the recorded evidence; internal consistency holds (byte sizes match between items 1 and 5, the 12-file gate matches the dir listing, the export size 7589 B is consistent with primary plus one RSA-4096 signing subkey). One should-fix, owner Robotnik (the `## Status` transcription); Tails' share of it is the `## Next Actions` line.

---

## Security

*Owner: `Omega`. Read-only. Severity order.*

### Item 7 self-audit claim is self-referentially false as written (marker string present in the doc's own prose)
**Severity:** low
**Vector:** secrets
**Where:** `planning/docs/TASK-0036-host-reinstall-backup.md:271` (item 7 "Doc self-audit"), marker occurrences at `:264` and `:271`
**Attack:** no external attacker; the failure mode is internal. The recorded audit states "no 'BEGIN PGP PRIVATE KEY BLOCK' marker in this doc", but the marker string appears exactly twice in the doc, both as prose: the item 7 command list (`:264`, quoting the `grep -n` command) and the audit sentence itself (`:271`). The grep evidently ran before the line quoting it was written. A future reader, reviewer, or `Espio` who re-runs the audit's own grep to confirm the DoD box gets 2 hits and a key block looks present where none is; the doc's one evidence line that a leak did not happen is not reproducible.
**Impact:** no key material is exposed (verified independently, see verdict below). Impact is loss of a clean, reproducible no-leak proof in a doc whose DoD box depends on that proof, and a false-positive alarm if the check is ever re-run mechanically.
**Fix:** Tails rewrites the item 7 audit sentence to state what is true: the marker string occurs only in prose references (the item 7 command list and this sentence), `END PGP PRIVATE KEY BLOCK` occurs zero times, and no base64-only line of 100+ chars exists (armor lines are <= 64 chars), so no armored block is present.
**Resolution:** resolved by Tails 2026-10-20 (item 7 audit sentence, line 271): the audit no longer claims the marker is absent from the doc; it states the marker string occurs in prose references (the item 7 command list and the audit sentence) and never as a standalone armor line, and that the no-leak proof rests on the base64-line property (zero base64-only lines; armor lines at most 64 chars), not on the marker. Re-running the audit's grep now returns only prose hits (line 264, line 271, line 322), so the no-leak proof is reproducible and depends on no marker string. One-line text-only change in `## Implementation`; no verified fact, digest, or fingerprint changed.

**Verdict: no findings above low.** Secret-handling surface verified against live state 2026-10-20 (all checks value-free; no secret value was printed by this review):

- **Modes/ownership.** `~/AI/secrets` 700 `howard:howard`; `gpg-secret-key.asc` 600 `howard:howard` 7589 B, sha256 `f01d0cfb…d5c4f`; `gpg-passphrase.txt` 600 `howard:howard` 49 B, sha256 `61cd6d2e…2a21` — all identical to items 2 and 7, so nothing changed after Tails' audit. Backup dir 700, both VM disk copies 600, `SHA256SUMS` 600.
- **Value in doc / commit / log / command string.** The passphrase value (matched via `grep -Ff` against the file, never printed) is absent from the planning doc, `~/.bash_history`, `~/.local/share/opencode/opencode.db` (all session records), the working-tree diff of `planning/`, and every untracked file at the repo root. `END PGP PRIVATE KEY BLOCK`: 0 hits; base64-only lines of 100+ chars: 0. No commit carries this doc yet (it is untracked), so no commit can contain it; the pickaxe over all refs for the marker hits only TASK-0024 commits, where it is historical prose. Every recorded passphrase operation used `--passphrase-file <path>`; no value in any command string.
- **Exposure surface, auto-backup path vs mandated keyring location.** Locally the posture is identical to the mandated keyring: 700 dir / 600 files / `howard:howard`, matching `~/.gnupg-cinnamon-rocky10` (700). The widening is real but inherent to the task's purpose and operator-attested design: both files sit under the auto-backup root, so the signing secret and its passphrase ride into the operator's off-host backup store, making it a third copy of the credential (live keyring, `~/AI/secrets/`, off-host store). The plan's "What this makes harder later" records this. Blast radius of a store leak: the ability to sign RPMs that verify for every consumer trusting the published public key (`gpgcheck=1`); the key cannot be revoked (revocation needs the secret), only replaced. Detection would come from the store's own security, operator-owned. Not a fixable finding. The plan's "digests and paths only" constraint is honored throughout; the recorded sha256 of the passphrase is not exploitable (48 chars, high entropy; the digest only enables offline confirmation, not a shortcut).
- **Scratch keyring and scratch rpmdb teardown.** No `t0036-*` entry in `/tmp/opencode` (keyring, rpmdb root, probe root, manifests). Only one gpg-agent process runs: `--homedir /home/howard/.gnupg-cinnamon-rocky10` (the live keyring's normal daemon). No scratch-homedir agent. Note for the record: Tails' `pgrep -af 'gpg-agent.*t003[6]'` pattern could not match a scratch agent (the homedir is not in the agent's command line); the absence is established instead by the deleted homedir directory plus the full process list.
- **Old public key extraction source (git history blob) is sound.** `git show a70aedc:keys/cinnamon-rocky10-public.asc` is byte-identical to the extracted file (both sha256 `5a0e4db8…e74`); fingerprint `1689676AF4D4F6FEC142B4429C0A8912FDA02785` matches the plan; the key-ID tail `FDA02785` matches both the host rpmdb package name `gpg-pubkey-fda02785-6ab101f4` and the "key ID fda02785" that the scratch rpmdb (exactly one import) reported OK on for the `-2` RPM. `a70aedc` re-verified live as an ancestor of `origin/main`. (`rpm --queryformat '%{PUBKEY}'` is an unknown tag in this RPM 4.19.1.1 build, so the direct rpmdb-bytes comparison was done via the key-ID correlation instead; the full 8-hex key-ID plus fingerprint match is conclusive.)
- **Notes, not findings.** A zero-byte untracked file named `-` exists at the repo root (mode 666): clean (no value, no marker), but Knuckles should leave it uncommitted. `~/AI/secrets/` also holds pre-existing files (`pass.txt`, `token.md`, `githubtoken.md`); they ride the same auto-backup widening but pre-date this task and are out of scope.

---

## License (Charmy)

*Owner: `Charmy`. Fourth in the review chain. Every license is verified at the upstream source
repository and the ref used, never from a copy in this repo.*

**Project license:** MIT — `LICENSE` at the repo root (Copyright (c) 2026 Howard). Appropriate. Both imported components in this backup are Apache-2.0 (permissive, compatible with MIT); no GPL code is involved in this task and nothing was relicensed.

**Imported code**

| Component | Source (repo @ ref) | License (verified at) | Obligations met | Status |
|---|---|---|---|---|
| `portless/` (7 files, v0.15.6) | `vercel-labs/portless` @ tag `v0.15.6`, published as npm `portless@0.15.6` | Apache-2.0. Verified at: repo `LICENSE` @ `v0.15.6` (appendix "Copyright 2025 Vercel Inc."), npm registry license field for 0.15.6, and the copied manifest's `license` field. No `NOTICE` at the tag (404) | Yes. Backup copy is byte-identical to the published npm tarball 0.15.6 (verified this turn: `diff -r` of the backup dir's `portless/` against a fresh `npm pack` tarball, empty). The tarball ships no LICENSE/NOTICE file, matching upstream packaging (`files: ["dist"]`); the manifest's `license` + `author` fields and the README ride with the copy. Apache-2.0 §4 obligations attach to distribution, and this backup copy is not a distribution | pass |
| `agentsmd` (8831160 B, v0.5.0) | `rudrakshkarpe/agentsmd-cli` @ tag `v0.5.0` | Apache-2.0. Verified at: repo `LICENSE` @ `v0.5.0`. The binary embeds the Go module path `github.com/rudrakshkarpe/agentsmd-cli` and self-identifies as v0.5.0 (`agentsmd --version`). No `NOTICE` at the tag (404) | Yes. External standalone Go binary, not team-authored (no source or history for it in this repo, `git log --all -- '*agentsmd*'` empty; only the gitignored `.agentsmd/` data dir exists). Stripped; zero embedded license/copyright strings (`strings \| grep -icE "license\|copyright"` = 0). The team runs it and does not distribute it, so no §4 obligation is triggered; nothing in the backup combines it with project source | pass |
| `gpg-pubkey-fda02785-6ab101f4.asc` (1713 B) | Team's own key material, extracted from cinnamon-for-rocky10 `a70aedc:keys/cinnamon-rocky10-public.asc` | None expected. Verified: file starts `-----BEGIN PGP PUBLIC KEY BLOCK-----`, zero private-key markers | n/a — a GPG public key carries no license content | pass |
| `agentgateway.yaml` (758 B) | Team's own configuration (AGENTS.md §15) | None expected. Verified: YAML config, no code | n/a | pass |

The two VM disk copies are team-owned VM state (the host reinstall target), not imported code; outside the imported-code verification for this task.

**Verdict:** pass. No findings. For the record, not a finding on this task: if the backup dir contents are ever redistributed, Apache-2.0 §4(a) requires the license text to accompany the `portless/` code (source: `LICENSE` @ `v0.15.6`) and the `agentsmd` binary.

---

## Test Results

*Owner: `Big`. Verdicts, never raw log dumps.*

Independent re-verification pass (re-runnable, value-free checks only). No secret value entered this
section or any command string; the passphrase was used exclusively via `--passphrase-file`. All
scratch material was shredded after use (see finding 7).

**Workflow run:** (local re-verification; no CI workflow applies to a file-backup task)

| Check | What it exercises | Result | Notes |
|---|---|---|---|
| SHA256SUMS gate (12/12) | backup dir integrity, incl. 25 GB re-hash of both VM disks | PASS | `cd ~/AI/setup-backup/2026-10-20-host-reinstall && sha256sum -c SHA256SUMS` exit 0, all 12 OK, incl. `Rocky_Linux_10_Cinnamon.qcow2` (21478375424 B) and `Rocky_Linux_10_Cinnamon.2026-10-04T11:36` (4262592512 B) |
| Secret-file digests | `~/AI/secrets/` files unmodified (digests only, values never read) | PASS | `sha256sum`: `gpg-secret-key.asc` = `f01d0cfb…5c4f` (== line 210), `gpg-passphrase.txt` = `61cd6d2e…a21` (== line 211 == source `~/.gnupg-cinnamon-rocky10.passphrase/passphrase`); both 600 howard:howard, 7589 B / 49 B |
| Scratch keyring: import + unlock + verify | exported secret key imports into a fresh keyring and unlocks with the exported passphrase | PASS | evidence chain in finding 1; scratch material shredded after |
| Scratch rpmdb `-Kv` on the `-2` RPM | old public key verifies a repo RPM, isolated from the host rpmdb | PASS | `rpm --root /tmp/opencode/t0036-big-rpmroot -Kv ~/Linux/projects/cinnamon-for-rocky10/rpms/cinnamon-desktop-6.7.2-2.el10.x86_64.rpm` exit 0: "Header V4 RSA/SHA256 Signature, key ID fda02785: OK" plus Header/Payload/MD5 OK; scratch db held exactly one package (`gpg-pubkey-fda02785-6ab101f4`), so only the imported key verified |

**Checks requested vs run:** 4 requested, 4 executed. The scratch-keyring check was
environmentally blocked on the first two attempts (harness finding 2), resolved in this pass. No
coverage was dropped.

Not re-run, with reasons:
- Original export command from the live keyring: would mutate the backup files; the digest match
  against line 210 plus Tails' export record (Implementation line 119) is the verification.
- Tails' item-1 environment facts (`df`, `virsh`, per-source `stat`): cited from Implementation;
  my gate re-run confirms the backup dir is intact.
- Host live-keyring state: cited from Implementation (lines 138, 194); my scratch tests were
  isolated, and post-test `pgrep -af 'gpg-agent|scdaemon'` showed only the live pair (705355 /
  705357, homedir `/home/howard/.gnupg-cinnamon-rocky10`).
- VM / Sparky / Podman layers: N/A. The target is a file backup, not a project build; no desktop
  component is under test.

**Findings (all resolved, no defect found):**

1. **Restoration chain closed.** (a) exported `.asc` sha256 == line 210; (b) passphrase copy sha256
   == source passphrase sha256; (c) `gpg --homedir <scratch> --import < ~/AI/secrets/gpg-secret-key.asc`
   → `secret keys imported: 1` (two 5088 B `.key` files, mode 600, in `private-keys-v1.d/`); (d)
   loopback sign with `--passphrase-file` exit 0; (e) that signature verified in a fresh keyring
   holding only the backup pubkey: `Good signature`, primary `2274 BFE1 BF28 C051 CD98 675B EBD1
   3108 EB7F EF99` (key ID EBD13108EB7FEF99) and subkey `CD49 58E1 A421 CBD6 B56B 7C56 14CF 2C0A
   8A47 323C` [SEA], both == DoD (line 39) and the live-keyring record (Implementation line 194);
   key created 2026-10-19 [SCEAR]/[SEA].
2. **Scratch-import timeout root cause (harness, Big's).** First two attempts: `gpg: key
   EBD13108EB7FEF99: error sending to agent: Timeout`, exit 2. Cause: the on-demand gpg-agent
   launch raced the first skey send (agent still mid-startup when the import connected). An
   isolated retry failed identically, ruling out a key-specific property. Fix: pre-launch the
   agent (`gpgconf --homedir <scratch> --launch gpg-agent`) and drop the stale
   `GPG_TTY=/dev/pts/6`; the import then succeeded on the first attempt. Scratch homedirs held no
   secret material before the successful import (`pubring.kbx` 3091 B only), so no partial secret
   ever sat on disk.
3. **gpg 2.4.5 option fact for the reinstall runbook:** `--import-secret-keys` is not a valid
   option in this build (`gpg: invalid option`); `gpg --import` on a file containing secret
   material imports both the public and secret parts.
4. **Doc marker anomaly resolved.** All five `-----BEGIN` hits in this doc are prose
   (Implementation lines 264, 271; Security lines 322, 324, 330). Zero armored blocks, no secret
   in the doc. Tails' self-audit claim was true when written (it predates the Security section).
5. **Correction to the Security record:** the two orphaned gpg-agent processes (PIDs 712698,
   713212) were launched with `--homedir /tmp/opencode/t0036-big-gnupg`; all orphaned scratch
   material is now shredded/removed.
6. **Date cross-check (no anomaly):** new key created 2026-10-19 (both sec and ssb lines); old key
   `1689676AF4D4F6FEC142B4429C0A8912FDA02785` created 2026-09-21; the `-2` RPM (mtime
   2026-10-18 14:22:59) is signed by the old key, which predates it. Consistent.
7. **Cleanup verified.** `ls -d /tmp/opencode/t0036*` → none. Shredded: both scratch homedirs
   (including the two `.key` secret files), test files, signature, agent log (0 `-----BEGIN`
   markers), pubkey-only export. Scratch socket dirs under `/run/user/1000/gnupg` removed; the
   live agent's socket dir preserved (re-identified live via `ss -xlp` against PID 705355 before
   any removal).
8. **Harness self-match note:** one `pgrep -f` kill loop matched its own shell (the pattern
   appeared in the bash command line) and terminated itself after killing the two scratch
   agents; the remainder was completed by explicit PID. The live pair never matched.

**Verdict:** PASS. The backup is intact and restorable: the 12/12 SHA256SUMS gate passes (both VM
disks re-hashed), both secret-file digests match the recorded values, the exported secret key
imports into a fresh keyring and unlocks with the exported passphrase, and the resulting
signature verifies against the backup pubkey; the old public key verifies the `-2` RPM in an
isolated scratch rpmdb. No FAILs. The single environmental block was a harness bug (stays with
`Big`), root-caused and fixed; no defect was found in the backup or in the `Tails`
implementation.

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

**DONE checklist verified:** yes

Verified 2026-10-20 by Knuckles. All eleven DoD boxes are met by the recorded evidence, which is file state plus the sections below (nothing re-run in this step; no box requires it). The secret-credential chain verifies as recorded: export in `~/AI/secrets/` mode 600 with scratch import, both fingerprints, and the passphrase copy unlocking the loopback sign (## Implementation items 2-3, independently re-verified by Big in ## Test Results), the passphrase copy byte-identical to the source (item 2), the old public key verifying the `-2` RPM in a scratch rpmdb (item 4), the VM disk plus snapshot byte-verified against the source with the Fedora VM recorded as re-provisionable per the plan deferral (item 5), the three host-tool copies digest-matched (item 6), and the no-secret-value audit (item 7, re-checked independently in ## Security). The four review gates are closed: Shadow no blockers with the single should-fix resolved by Robotnik (the operator steps are transcribed to ## Status verbatim), Omega no finding above low with the single low fixed by Tails (item 7 audit sentence), Big PASS 4/4 with no silently dropped checks, Charmy pass with no findings. The remaining operator steps are written exactly in ## Status (DoD box 11).

- **Branch:** `main`. Planning-doc bookkeeping lands directly on `main` per the planning-doc checkpoint convention (no feature branch for planning-only changes).
- **Commits:** GPG-signed no. `commit.gpgsign` is unset at repo level and the recent house commits are all unsigned (`git log --format='%G?' -5` returns `N` on all five).
- **PR:** n/a. In-account planning bookkeeping under the standing permission, no PR, per house convention.
- **Deploy:** n/a. No deployment workflow for this task; the host reinstall is operator-driven and gated on ## Status.

### Final bookkeeping commit (2026-10-20)

The post-release state of this doc is committed to `main` as this commit and pushed to `origin` of `metalllinux/team-chaotix` (in-account standing autonomy; no feature branch, per the planning-doc checkpoint convention). Commit message: `chore(planning): record TASK-0036 release step and carried TASK-0027/TASK-0033 prunes`. The commit carries planning/ files only, exactly four: this doc (the ## Release record and the Knuckles ## Next Actions tick), `planning/TASKS.md` (TASK-0033 row updated, TASK-0036 row added), and the two carried Espio prunes `planning/docs/TASK-0027-cinnamon-brightness-fix.md` and `planning/docs/TASK-0033-cinnamon-project-environment.md`. Pre-push secret scan on the staged diff, value-free: 0 added armored private-key block lines, 0 hits for the passphrase value (`grep -Ff` against `~/AI/secrets/gpg-passphrase.txt`; value never printed), 0 base64-only lines of 100+ chars, 0 `ghp_` token prefixes. The out-of-scope working-tree entries are excluded from the commit and left untouched: `cinnamon-1-vm.xml` (tracked, modified, out of scope for this task), and the untracked `-` (zero-byte; the file Omega noted in ## Security), `continue-prompt-2026-10-05.md`, `prompt-task0026-continuation.md`.

---

## Archive

*Owner: `Espio`, the only agent that deletes. Superseded detail lands here rather than being
lost. Decisions, verified facts, rejected options with their reasons, known traps, and anything the
user said are never deleted.*

**Pruning log**

| Date | What was pruned or compressed | Rough size |
|---|---|---|
| | | |
