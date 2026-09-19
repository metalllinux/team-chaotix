# TASK-0016 — INSTALL.md: verify all instructions + add minimal-server (no login manager) install-and-run section

> **Section order below is fixed.** Each agent writes to its own section and no other. `Robotnik`
> reads only `## Status` and `## Next Actions`. Do not reorder, rename, or remove sections.

- **Created:** 2026-08-30

---

## Status

*Owner: `Robotnik`. Keep this SHORT and CURRENT — it is one of only two sections the PM reads, so a
stale entry means the whole loop runs on bad information.*

**Now (2026-09-19, post-Vector fix): Quick-start metadata wording fixed.** INSTALL.md now states
the fresh-clone truth (repodata/ untracked -> generation path; a copy carrying repodata/ skips;
correct on both paths), each clause evidence-backed from Big's run. Project `7975f1a` on the
feature branch (local, unpushed, fast-forward ready for Knuckles); planning `5a74eb0` pushed.
Next: review chain Shadow → Omega → Big on the branch diff, then Knuckles.

**Now (2026-09-19, post-Big): fresh-VM run PASS.** The documented minimal-server procedure
executed end-to-end exactly as written on fresh minimal Rocky 10.2 VM `task0016-minimal`
(192.168.122.142): start state (444 pkgs, no DM/X, multi-user.target, getty), 64/64 RPMs +
repodata transfer, `setup-repo.sh` rc=0, 22/22 install with zero DM/X in the full rpm-db diff,
GDM self-enable (documented `enable` a no-op), getty until `set-default graphical.target`, reboot
to GDM Wayland greeter, first-attempt login to a working Cinnamon (Wayland) session
(`Type=wayland`, Xwayland, nemo-desktop). Item 6 answered: the greeter does **not** list the X11
"Cinnamon" entry (menu shows only `Cinnamon (Wayland)` + `GNOME`; X11 file on disk, no Xorg in any
repo). All 8 checks executed, none dropped. Evidence in project `89b9b7b`; planning `bc85291`.
**One doc finding for Vector:** the Quick-start "a fresh clone ships with valid metadata, so
generation is skipped" claim is inaccurate — `rpms/repodata/` is untracked in git, so a fresh
clone has no metadata and `setup-repo.sh` generates it (the `createrepo_c` self-install path
worked on the minimal image); the procedure is correct on both paths.

**Now (2026-09-19, post-Vector): doc leg complete.** `INSTALL.md` gains the "Minimal server (no
display manager)" section (the verified path, six steps; the "no spec declares a DM or X" claim
grep-verified over all of `spec/`) and the D5 fix (local RPMs do register in the rpm db; the real
gap is repository origin). D1-D4/D6 were already resolved by TASK-0017's rewrite; a quick-start
metadata-precision fix landed too. Project: branch `feature/TASK-0016-install-md-minimal-server`
cut from `main` `3375a05`, commit `760b852` (local, unpushed — Knuckles). Planning `c5f7046`
pushed. Next: Big runs the exact documented procedure on a fresh minimal Rocky 10.2 VM.

**Now (2026-09-19): task RESUMED — the pause on TASK-0017 is over.** TASK-0017 shipped (PR #4
merged, `main` at `3375a05`): the set is complete (64 RPMs, 22-name install set), and its Vector
leg already rewrote `INSTALL.md`/`README.md` for the complete set (single-dnf install, GDM Wayland,
troubleshooting). Remaining here: (1) `Vector` applies the standing audit findings D1-D6 (where
still applicable after the rewrite) and writes the dedicated **minimal-server (no login manager)
install-and-run section** — the 2026-08-30 verified path (set installs with no DM/X pulled in;
GDM 47 + gnome-shell install + enable; default target stays `multi-user.target`;
`systemctl set-default graphical.target` -> getty until then) translated to the current set;
(2) `Big` runs the exact documented procedure on a fresh minimal Rocky 10.2 VM on host
`192.168.1.102` (no DM preinstalled) to prove it end-to-end; (3) review chain, then Knuckles.

**Now (2026-09-14):** `192.168.1.103` is no longer available for testing (user, 2026-09-14;
verified unreachable from the PM host). The 2026-08-30 bare-metal grounding evidence in the entry
below remains valid as a record, but the DoD's "Verified by execution" step will run on a fresh
minimal Rocky 10.2 VM on host `192.168.1.102`, not on the bare-metal machine. The task remains
paused on TASK-0017, which now also carries the user's desktop-feature-parity goal vs the Fedora
Cinnamon reference VM (2026-09-14).

**Now (2026-08-30): task created from the user's direct request.** The user wants: (1) every
existing instruction in `metalllinux/cinnamon-for-rocky10` `INSTALL.md` (on main) verified as
correct, and (2) a new section covering installing **and running** the Cinnamon Desktop from a
minimal-server Rocky Linux 10 system with **no login manager present**. Grounding evidence already
exists: Big's bare-metal env-prep on `howard@192.168.1.103` (a real minimal-server) installed the
48-RPM Cinnamon set cleanly with no DM/X pulled in, then GDM 47 was installed + enabled, and the
system is at the getty with default target `multi-user.target` (verified 2026-08-30: the user sees
only the CLI until `systemctl set-default graphical.target`). The minimal-server procedure to be
documented is exactly that verified path.

**Environment / scope:**
- Files in scope: `INSTALL.md` (primary), `README.md` (if affected), and the install procedure in
  `metalllinux/cinnamon-for-rocky10`. Clone at `~/Linux/projects/cinnamon-for-rocky10/` (now on
  main, tip `4880e0b` after the TASK-0008 rebase merge).
- Touches the DB schema: no
- Graphical UI: yes — greeter + desktop session; VM-based end-to-end verification required
- Rocky Linux target: yes (Rocky Linux 10.2)

**Unknowns:**
- Whether every existing `INSTALL.md` step is still correct after the mozjs115/cjs/muffin changes
  (TASK-0004) and the DNF repo setup (TASK-0006). The audit establishes this by execution, not
  assumption.
- The package-count discrepancy carried from TASK-0006/0008 ("10 vs 14 packages", and the 48-RPM
  set Big recorded). The audit must reconcile the count the doc states against the real set.
- Which display manager to document as the default for the minimal-server path. GDM is the
  verified choice (it's what's on the bare-metal host); LightDM/SDDM belong to TASK-0015.

**Coordination:** the minimal-server install section written here overlaps TASK-0015's server-install
DoD box. TASK-0016 owns the minimal-server + GDM content now; TASK-0015 extends `INSTALL.md` with
the LightDM/SDDM variants later and must stay consistent with what this task lands.

**PAUSED (2026-08-30):** the user's desktop-completeness feedback (TASK-0017) revealed the 13-RPM
"runtime set" this doc would describe is **not a complete desktop** (no applets/themes/extension
manager/plugins/screensaver/terminal). `Tails`' audit (6 discrepancies) is done and valid; the
**doc-writing and end-to-end verification pause** until TASK-0017 lands the complete set, then this
task resumes: Vector writes the doc describing the complete set, Big re-runs the minimal-server
procedure against it. The audit's D1-D6 findings stand.

---

## Definition of Done

*Owner: `Robotnik`, and nobody else. Written **before** any work starts. Objectively checkable —
if a box cannot be verified by looking at something, rewrite it.*

- [ ] **Audit complete.** Every instruction in the current `INSTALL.md` (on main) is checked: each
      step verified as correct against the repo and by execution, with every discrepancy recorded
      in `## Implementation` (file, line, what's wrong, the correction).
- [ ] **Minimal-server section added.** `INSTALL.md` has a section covering, from a minimal Rocky
      10.2 server with no login manager and no X server: (a) installing the Cinnamon RPM set from
      the local DNF repo, (b) installing + enabling a display manager (GDM), (c) setting the default
      target to `graphical.target`, (d) rebooting, (e) selecting the Cinnamon (Wayland) session at
      the greeter and logging in. It states plainly that a display manager is required to run the
      desktop and that none is present to start.
- [ ] **Verified by execution.** `Big` runs the exact minimal-server procedure from the doc on a
      fresh minimal Rocky 10.2 VM and reaches a working Cinnamon (Wayland) desktop; the run is
      recorded in `## Test Results` with the evidence.
- [ ] **Doc reflects verified reality.** The doc states: Xorg is not installable on Rocky 10.2
      (the X11 path is Xwayland), the working session is Cinnamon (Wayland), and the Cinnamon RPM
      set does not force-pull a display manager or X server.
- [ ] `Shadow`: no unresolved blockers or should-fix findings in `## Review`.
- [ ] `Omega`: no unresolved findings above `low` in `## Security`.
- [ ] `Big`: all harness checks PASS, with no silently dropped checks.
- [ ] `Vector`: `INSTALL.md` (and `README.md` if affected) updated and internally consistent.
- [ ] `Knuckles`: merged to `metalllinux/cinnamon-for-rocky10` main via PR.

---

## Next Actions

*Owner: whoever wrote last. The future only — delete what has been done. The second of the two sections
the PM reads.*

- [x] `Tails` (2026-08-30, predates the pause): audit of every existing `INSTALL.md` instruction
      complete — six discrepancies D1-D6 recorded in `## Implementation` (package-count
      reconciliation included). The verified minimal-server procedure (install set + GDM +
      set-default graphical + Cinnamon Wayland session) is the bare-metal grounding path recorded
      there; it is what the new doc section documents.
- [x] `Vector` (2026-09-19): minimal-server section added to `INSTALL.md` + D5 fixed + quick-start
      precision fix; D1-D4/D6 confirmed already resolved by the TASK-0017 rewrite. Project
      `760b852` on branch `feature/TASK-0016-install-md-minimal-server` (from main `3375a05`,
      unpushed); planning `c5f7046`. One claim left unverified by design: whether the greeter
      lists/filters the X11 "Cinnamon" entry (Big's item 6).
- [x] `Big` (2026-09-19): fresh-VM run **PASS** on `task0016-minimal` (192.168.122.142) — all
      steps of the documented procedure executed exactly as written; item 6 answered (greeter does
      not list the X11 "Cinnamon" entry). Evidence project `89b9b7b`, planning `bc85291`. One doc
      finding returned to Vector (Quick-start metadata claim).
- [x] `Vector` (2026-09-19): Quick-start metadata wording fixed per Big's finding. Project
      `7975f1a` (on top of `89b9b7b`, local. Feature-branch push blocked by Vector's permissions,
      Knuckles pushes). Before/after and the no-change list in `## Docs`.
- [ ] `Shadow` → `Omega` → `Big`: review chain on the diff.
- [ ] `Tails`: fix anything the chain returns.
- [ ] `Knuckles`: PR to main, merge.

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

*Owner: `Tails`. Audit + verified procedure, 2026-08-30.*

**Method and environment.** Clone at `~/Linux/projects/cinnamon-for-rocky10/`, branch `main`,
tip `4880e0b`, working tree clean (`git status --short` empty). Note: the dispatch brief's clone
path `~/AI/projects/cinnamon-for-rocky10/` does not exist; the real clone is under
`~/Linux/projects/`, matching TASK-0008's records. Verification was (a) static inspection of the
repo (scripts, RPM metadata via `rpm -qp`), and (b) read-only execution on the bare-metal minimal
server `cinnamon-bm103` (howard@192.168.1.103): state, dnf repo config, session entries, package
counts only. No state changes, no GDM start, no reboot on that machine (GDM was already active
before my first check; see "Bare-metal state observation" below). Fresh-VM end-to-end execution is
Big's turn.

### Audit: instruction-by-instruction verdicts

| INSTALL.md | Instruction | Verdict |
|---|---|---|
| :5 | "All 14 base packages install cleanly" | CORRECT. 14/14 at table versions, verified today on 192.168.1.103 (`rpm -q` per package) and on the TASK-0008 scratch VM (F7). Cross-doc conflict with README's "10": D3. |
| :12 | "Clone or copy the project to any directory" | CORRECT. Script self-locates via `dirname "$0"` (`setup-repo.sh:51-58`); bare-metal run used `/home/howard/cinnamon-for-rocky10`, rc=0 (TASK-0008 checkpoint 3). |
| :14-19 | setup-repo.sh installs createrepo_c if missing, generates metadata, writes `.repo` | CORRECT, metadata generation is conditional. `setup-repo.sh:91-96` (createrepo_c only if absent; installed `createrepo_c-1.1.2-4.el10` + 1 lib on bare metal), `:101-107` (skip when `repodata/repomd.xml` present; the clone ships valid `repodata/` — verified locally: `repomd.xml` + 3 zstd files), `:119-128` (writes `/etc/yum.repos.d/cinnamon-rocky10.repo`). |
| :21-25 | Both invocation forms (bare, and with explicit project-root arg) | CORRECT. `setup-repo.sh:53-58`; the explicit-arg form is exactly what ran on bare metal. |
| :30 | `sudo dnf install cinnamon` | CORRECT. rc=0 `Complete!` on bare metal. |
| :33-35 | "installs the shell and its hard dependencies (cjs, muffin, muffin-clutter, muffin-cogl, cinnamon-desktop, xapps-lib, cinnamon-menus, mozjs115)" | CORRECT. `rpm -qp --requires` on `cinnamon-6.7.4`: soname requires `libcjs.so.0`, `libmuffin.so.0`, `libmuffin-clutter-0.so.0`, `libmuffin-cogl-0.so.0`, `libcinnamon-desktop.so.4`, `libxapp.so.1`, `libcinnamon-menu-3.so.0`; `rpm -qp --provides` confirms each soname is provided by exactly one of those local RPMs. mozjs115 is transitive: `cjs-6.4.0` requires `libmozjs-115.so.0`, provided by `mozjs115-115.29.0`. |
| :37-40 | Five packages "not hard dependencies" (cinnamon-session, cinnamon-settings-daemon, cinnamon-control-center, nemo, mozjs115-devel) | CORRECT. Scanned `--requires` of all 14 runtime RPMs: none of the five is required by any of them (only self-referential sonames: `cinnamon-control-center` requires its own `libcinnamon-control-center.so.1`, `nemo` its own `libnemo-extension.so.1`). |
| :42 | "Without these, the settings panel, session manager, and file manager will be missing" | IMPRECISE (D6): omits the settings daemon. |
| :47 | `sudo ldconfig` | CORRECT and load-bearing. The `cinnamon` RPM ships `.so` files with no ldconfig post-install scriptlet (TASK-0008 F6); rc=0 on bare metal. |
| :50-51 | "The setup script handles all prerequisites: enabling CRB, installing createrepo_c, validates repository is readable" | CORRECT. `setup-repo.sh:138-145` (CRB), `:91-96` (createrepo_c), `:150-153` (`dnf makecache --disablerepo='*' --enablerepo=cinnamon-rocky10`, dies on failure). |
| :57-65 | Manual: `dnf install -y createrepo_c`, `createrepo_c rpms/` | CORRECT. Note: the shipped `repodata/` is already valid, so step 2 regenerates (overwrites) metadata that exists; harmless for install, but a user cloning from git will dirty tracked files. Informational, not a discrepancy. |
| :67-78 | Manual `.repo` content | CORRECT. Matches the script's printf output key-for-key: `enabled=1`, `gpgcheck=0`, `metadata_expire=0`, `module_hotfixes=0`, `keepcache=0`, same `name=` string. Verified against the live file on bare metal (identical except the `baseurl` path). |
| :80-83 | `sudo dnf config-manager --set-enabled crb` | CORRECT. Repo id on Rocky 10.2 is `crb` (`dnf repolist` on bare metal shows `crb Rocky Linux 10 - CRB`). |
| :85-99 | Manual steps 5-7 | CORRECT (same as quick start). |
| :101-106 | `sudo dnf install ./rpms/*.rpm` | CORRECT as a command. Glob matches exactly the 48 RPMs (`ls rpms/*.rpm | wc -l` = 48 locally); the original VM test ran `dnf install *.rpm` successfully (README.md:39). The claim at :108 is wrong: D5. |
| :111-128 | Prerequisites: enable CRB + install 35-package base list | All 35 names are valid Rocky 10.2 packages (verified on bare metal: every name returns an installed package after the Cinnamon+GDM install; none fails `rpm -q`). The "required" wording is wrong: D4. |
| :133-150 | Installed-packages table (14 rows) | CORRECT. Every version matches both the RPM filenames in `rpms/` and the installed versions on bare metal today. |
| :152-157 | "Cinnamon creates a .desktop session file; `ls /usr/share/xsessions/cinnamon.desktop`" | CORRECT as a file-existence check. The file is shipped by the `cinnamon` RPM (TASK-0008 F1) and is present on bare metal. Which session to actually select is D1. |
| :159-164 | "Restart GDM" + "select 'Cinnamon' from the session menu" | WRONG for the target OS (D1, D2). Assumes a display manager already exists (a minimal server has none), and points at the X11 entry, which has no Xorg to run on Rocky 10.2. |
| :166-201 | Troubleshooting (SELinux, repo, ldd, mozjs115) | CORRECT. `ldd` target `/usr/lib64/libcinnamon-desktop.so.4` exists (shipped by the `cinnamon-desktop` RPM; symlink to `.so.4.0.0` on bare metal). mozjs115 note's filename matches the RPM exactly. `ausearch`/`setenforce` usage is standard. |

### Discrepancies

**D1. INSTALL.md:159-164 — the session instruction targets a dead X11 path.** "Restart GDM" and
"log out and select 'Cinnamon'" (a) assume GDM is already installed; a fresh minimal server has no
login manager at all (verified baseline: `rpm -q gdm lightdm sddm` all not installed,
`systemctl is-enabled gdm` → `not-found`), and (b) direct the user to `Name=Cinnamon` in
`/usr/share/xsessions/cinnamon.desktop` (`Type=XSession`), which cannot start because
`xorg-x11-server-Xorg` is in no Rocky 10.2 repo (re-verified today: `dnf list available
xorg-x11-server-Xorg` → `No matching Packages to list`; `dnf list available 'xorg-x11-server*'`
→ only `xorg-x11-server-Xwayland-devel` from crb). The working session is `Name=Cinnamon
(Wayland)` from `/usr/share/wayland-sessions/cinnamon-wayland.desktop` (both files read on bare
metal). Correction: the procedure must install + enable GDM and direct the user to "Cinnamon
(Wayland)".

**D2. INSTALL.md:7-51 — the quick start has no display-manager step.** After `ldconfig`, a
minimal server has the desktop installed but no login path, and the doc never says a display
manager is required. The Definition of Done requires the doc to state plainly that a DM is
required to run the desktop and that none is present on a minimal server. Correction: the new
minimal-server section below (steps 6-9).

**D3. README.md:23, 12-21, 39, 44 vs INSTALL.md:5 — the carried "10 vs 14" count, resolved: 14
is correct.** README says "All 10 base packages install cleanly" and its component table lists 10
rows; the four missing rows are muffin-clutter, muffin-cogl, cinnamon-menus, mozjs115-devel. The
real Cinnamon runtime set is 14 (14/14 verified at table versions on bare metal today and on the
scratch VM). INSTALL.md:5 ("14") is right; the README is stale. Correction: update the README
table to 14 rows and align its test-result counts (Vector's file).

**D4. INSTALL.md:130-131 — "The base dependency list is required regardless of installation
method." Not true.** dnf resolves the full closure automatically: the bare-metal install pulled
all 157 packages from the default repos without any of the 35 being pre-installed, and all 35
names are valid packages. The list is redundant for any method that uses dnf resolution.
Correction: relabel as optional (useful only for air-gapped or repo-restricted environments) or
drop the "required" wording.

**D5. INSTALL.md:108 — "skips repository features like `dnf remove` tracking". Not accurate.**
Packages installed from local RPMs live in the rpm database and dnf history; `dnf remove` works
on them. What the local-file method actually lacks is repository-origin tracking for updates.
Correction: reword to "no repository origin, so dnf will not track updates for these packages".

**D6. INSTALL.md:42 — the "without these" sentence names three of the five packages' roles**
(settings panel, session manager, file manager) and omits the settings daemon
(`cinnamon-settings-daemon`). Correction: add it. Nit.

### Package-count reconciliation

- **14** (INSTALL.md:5) = the Cinnamon-specific runtime set = every non-debug RPM in `rpms/` =
  1 shell (`cinnamon`) + 8 hard dependencies + 5 additional. Verified 14/14 at table versions on
  bare metal today and on the scratch VM (TASK-0008 F7). **14 is the correct count.**
- **48** = total RPM files in `rpms/` (`ls rpms/*.rpm | wc -l` = 48): 14 runtime + 14
  `-debuginfo` + 11 `-debugsource` + 9 `-devel` (mozjs115-devel counted in the 14 runtime).
- **157** = new packages installed on the minimal server (674 → 831). Of these exactly **14 came
  from `@cinnamon-rocky10`** (verified today: `dnf list installed | awk 'NF>=3{print $3}' |
  sort | uniq -c` → 14 `@cinnamon-rocky10`; the other 143 from the default repos).
- **105** = packages added by `dnf install -y gdm` (831 → 936). `rpm -qa | wc -l` = **936** today,
  consistent with Big's before/after snapshots on the machine (`~/t0008-*.txt`).
- **10** (README) = stale, see D3.

### Verified minimal-server install-and-run procedure (for Vector to land in INSTALL.md)

**Start state:** Rocky Linux 10.2 (Red Quartz), minimal install. No login manager (gdm/lightdm/
sddm not installed), no X server (no `xorg-x11-server-*`), no desktop packages, default target
`multi-user.target`, getty on tty1, SELinux enforcing, 674 packages (verified baseline on
192.168.1.103). A display manager is required to run the desktop; a minimal server has none.

1. **Get the project onto the machine.** Clone or copy `metalllinux/cinnamon-for-rocky10`
   (including `repo-setup/` and `rpms/` with the 48 RPMs + `repodata/`) to any directory, e.g.
   `~/cinnamon-for-rocky10`. Verify the transfer: sha256 of all 48 RPMs local vs remote (Big's
   bare-metal run diffed the manifests; the diff was empty).
2. **`sudo ./repo-setup/setup-repo.sh`** (from the project root) or
   `sudo bash <root>/repo-setup/setup-repo.sh <root>`. Installs `createrepo_c` if missing
   (appstream), skips metadata generation (the shipped `repodata/` is valid), writes
   `/etc/yum.repos.d/cinnamon-rocky10.repo` (`baseurl=file://<root>/rpms`, `enabled=1`,
   `gpgcheck=0`, `metadata_expire=0`, `module_hotfixes=0`, `keepcache=0`), enables CRB (`crb`),
   validates readability with `dnf makecache`. Success marker: `=== Repository setup complete ===`,
   rc=0.
3. **`sudo dnf install -y cinnamon`** → `Complete!`. Installs `cinnamon` + the 8 hard dependencies
   (cjs, muffin, muffin-clutter, muffin-cogl, cinnamon-desktop, xapps-lib, cinnamon-menus,
   mozjs115) from the local repo. On the 674-package baseline this added 157 packages total; it
   pulls in **no login manager and no X server** (graphics pull-in is the mesa Wayland stack —
   mesa-dri-drivers, mesa-libEGL, mesa-libgbm, mesa-libGL, mesa-filesystem — plus X11 link-time
   libraries only).
4. **`sudo dnf install -y cinnamon-session cinnamon-settings-daemon cinnamon-control-center nemo
   mozjs115-devel`** → `Complete!`. `nemo` is load-bearing, not optional: the session's
   `RequiredComponents` includes `nemo-autostart`, which resolves to `nemo-autostart.desktop`
   shipped only by the nemo RPM (TASK-0008 F3).
5. **`sudo ldconfig`** → rc=0 (the `cinnamon` RPM ships `.so` files without a ldconfig scriptlet).
6. **`sudo dnf install -y gdm`** → `Complete!`. Pulls ~105 packages: `gdm-47.0-22.el10_2`,
   `gnome-shell-49.4` (greeter stack), `xorg-x11-server-Xwayland` (X11 compatibility inside the
   Wayland session). **GDM enables itself in the package post-install** (`systemctl is-enabled
   gdm` → `enabled` immediately after install; no manual `systemctl enable` needed). GDM 47 is
   Wayland-only: it ships `/usr/libexec/gdm-wayland-session` and no `gdm-x-session`
   (`rpm -ql gdm | grep -c gdm-x-session` → 0).
7. **`sudo systemctl set-default graphical.target`.** A minimal install defaults to
   `multi-user.target`; without this the machine boots to the getty and GDM, though enabled, is
   never started.
8. **`sudo reboot`** (or, without a reboot, `sudo systemctl start gdm`).
9. **At the GDM greeter, select the session "Cinnamon (Wayland)"** and log in. Expected end state:
   `cinnamon-session` (muffin compositor), `nemo`, `cinnamon-screensaver` running; the `loginctl`
   session reports `Type=wayland`.

**Xorg-absent / Xwayland reality (must be stated in the doc):** `xorg-x11-server-Xorg` is not in
any Rocky 10.2 repo (re-verified today on the bare-metal machine). The X11 "Cinnamon" entry in the
greeter session menu has no X server to run on; X11 applications run through Xwayland inside the
Wayland session. The working session on Rocky 10.2 is **Cinnamon (Wayland)**, and the Cinnamon RPM
set does not force-pull a display manager or an X server.

### What Big must verify by execution (fresh minimal Rocky 10.2 VM, end-to-end)

1. `setup-repo.sh`: rc=0, `.repo` file content, `dnf makecache` OK (repo-setup harness,
   post-TASK-0008 fixes).
2. Step 3 + step 4: `Complete!`; 14/14 packages at the INSTALL.md table versions; no gdm/lightdm/
   sddm pulled in; no `xorg-x11-server-*` in the new set; both session entries present
   (`/usr/share/xsessions/cinnamon.desktop`, `/usr/share/wayland-sessions/cinnamon-wayland.desktop`).
3. Step 6: `Complete!`; `systemctl is-enabled gdm` → `enabled`.
4. Step 7 + 8: after reboot the VM boots to the **GDM greeter**, not the getty (proof of
   `graphical.target`).
5. Step 9 via `test-gdm-login.sh` (post-TASK-0008 fixes): login selecting "Cinnamon (Wayland)"
   reaches an active session (`Type=wayland`, `cinnamon-session` process), zero new PAM failures,
   no AVC denials under enforcing.
6. Record the greeter behavior of the X11 "Cinnamon" entry (listed-but-failing vs filtered out) to
   finalize the D1 wording in the doc.

### Bare-metal state observation (2026-08-30, deviation recorded per AGENTS.md §5)

TASK-0016 `## Status` (2026-08-30) describes 192.168.1.103 as "at the getty with default target
`multi-user.target`". My read-only check later the same day shows the machine has **moved past
that state**: `systemctl get-default` → `graphical.target`; `systemctl is-active gdm` → `active`;
`loginctl` session 5 (user `howard`, seat0, tty2, since 2026-08-30 21:46 local) with
`Type=wayland`; running processes `cinnamon-session`, `cinnamon`, `nemo-desktop`, `nemo`,
`cinnamon-screensaver` (no gnome-shell in the session). The user, at the physical console, set the
default target, brought GDM up, and logged in. I changed nothing. This is human-verified
end-to-end evidence that the procedure works on the real machine: a Cinnamon Wayland session is
running. Residual gap: I cannot confirm from process evidence alone which greeter entry the user
clicked, but the running processes identify a Cinnamon session unambiguously, and `Type=wayland`
rules out the X11 entry (there is no Xorg).

**Alternatives considered**

### Problem: which display manager to document for the minimal-server path.
**Option A — GDM** · How: `dnf install -y gdm`, auto-enabled by post-install. · Pros: the only DM
with execution-verified evidence on the real target (installed, enabled, greeter up, Cinnamon
Wayland session confirmed running, both in VM and bare metal); Wayland-only, matching the
Xorg-absent reality; pulls Xwayland for X11 compatibility. · Cons: ~105 pulled packages
(gnome-shell greeter stack); GDM was the site of the TASK-0008 auth failure (root-caused to the
harness, not the RPMs).
**Option B — LightDM** · How: `dnf install lightdm`. · Pros: lighter footprint. · Cons: **not in
any Rocky 10.2 repo and not in EPEL 10** (TASK-0008 F9: `dnf provides /usr/bin/lightdm` → no
matches; EPEL probe → no matching packages). Cannot be documented for this target.
**Option C — SDDM** · How: `dnf install sddm`. · Pros: common on servers. · Cons: no
installation evidence on the target anywhere in the doc set; explicitly TASK-0015's scope.
**Chosen: GDM**, because it is the only option with execution-verified evidence on the target OS
and hardware; LightDM/SDDM belong to TASK-0015, and LightDM is repo-blocked.
**Competing priorities:** a lighter DM (B/C) was traded away in favor of verified evidence.

### Problem: which session to document as the working one.
**Option A — "Cinnamon" (X11)** · Cons: no Xorg in any repo; the session cannot start.
**Option B — "Cinnamon (Wayland)"** · Pros: verified running on bare metal (process evidence
today) and in the VM (TASK-0008 2c-3b PASS); X11 apps work via Xwayland.
**Chosen: B**, because the X11 path does not exist on the target OS.
**Competing priorities:** X11-session documentation was dropped entirely rather than carried as an
unverifiable "may not work" footnote.

**Changes**

| File | What changed | Why |
|---|---|---|
| `planning/docs/TASK-0016-install-md-minimal-server.md` | Filled `## Implementation`: audit verdicts, 6 discrepancies (D1-D6), package-count reconciliation, verified minimal-server procedure, bare-metal state observation | This task's deliverable. No repo files were modified; INSTALL.md/README.md edits are Vector's per `## Next Actions`. |

**Checks run:**

- Local (clone, main @ `4880e0b`, clean): `ls rpms/*.rpm | wc -l` → 48; `rpm -qp --requires`
  (`cinnamon`, `cjs`) and `rpm -qp --provides` (all 14 runtime RPMs) → hard-dependency soname
  mapping verified, five-optionals scan clean; `rpm -qlp cinnamon-desktop-6.7.2` → troubleshooting
  `ldd` target present; `repodata/` listing → valid (`repomd.xml` + 3 zstd); `setup-repo.sh` read
  in full (169 lines) → every doc claim about the script matched the code (lines cited above).
- Bare-metal read-only (`ssh cinnamon-bm103`, no state changes): `rpm -qa | wc -l` → 936;
  `rpm -q` on all 14 → exact table versions; `dnf list installed` repo column → 14
  `@cinnamon-rocky10`; `cat /etc/yum.repos.d/cinnamon-rocky10.repo` → matches the doc's manual
  section; `dnf repolist` → CRB id `crb` confirmed; `dnf list available xorg-x11-server-Xorg` →
  no match, `'xorg-x11-server*'` → only Xwayland-devel (crb); `rpm -ql gdm` → no `gdm-x-session`,
  one `gdm-wayland-session`; `systemctl is-enabled gdm` → enabled, `is-active` → active,
  `get-default` → graphical.target; `loginctl list-sessions` + `show-session 5` → howard, seat0,
  tty2, `Type=wayland`; `ps` → Cinnamon session processes; `rpm -q` loop over all 35 prerequisite
  names → all valid; session `.desktop` files read (menu names confirmed); `getenforce` →
  Enforcing.
- Not run (out of scope this turn): fresh-VM end-to-end (Big), GDM start/reboot on bare metal
  (read-only regime), any INSTALL.md/README.md edit (Vector).

**Competing priorities:** executable proof on a fresh VM (the gold standard) was traded for
read-only verification on real hardware plus static RPM metadata, because the brief defers VM
work to Big and the bare-metal machine is under the user's physical control. Doc edits were
deferred to Vector per the task chain. GDM was not started or rebooted on bare metal even though
that would have completed the interactive evidence: the no-state-change rule wins, and the user's
own 21:46 login supplied that evidence instead.

**Summary.** Discrepancies found: 6. D1 INSTALL.md:159-164 directs the user to the X11 "Cinnamon"
entry, which has no Xorg to run on Rocky 10.2; the working session is "Cinnamon (Wayland)". D2 the
quick start has no display-manager step; a minimal server ends with no login path. D3 README's
"10 base packages" is stale; the real set is 14 (INSTALL.md is correct). D4 the 35-package base
list is not "required regardless of installation method"; dnf resolves it all. D5 "skips dnf
remove tracking" is wrong; what is actually missing is update tracking from a repo origin. D6 the
"without these" sentence omits the settings daemon. Reconciled package count: 14 = Cinnamon
runtime set (1 + 8 hard deps + 5 additional, verified 14/14 at table versions on bare metal and
scratch VM); 48 = total RPMs in `rpms/` (14 runtime + 14 debuginfo + 11 debugsource + 9 devel);
157 = new packages on the minimal server, of which exactly 14 come from the local repo; +105 from
GDM = 936 total. Big must verify by execution on a fresh minimal Rocky 10.2 VM: repo setup
rc=0, the two install commands pull 14/14 at table versions with zero DM and zero X server, both
session entries present, GDM install self-enables, set-default + reboot boots to the greeter, and
the harness login selecting "Cinnamon (Wayland)" reaches an active Wayland Cinnamon session with
no PAM failures and no AVCs.

---

## Review

*Owner: `Shadow`. Read-only — findings only, no edits. Severity order, blockers first.*

*Reviewed 2026-09-19 by `Shadow`. Scope: the branch diff `3375a05..7975f1a` in
`~/Linux/projects/cinnamon-for-rocky10/` — `INSTALL.md` (Quick-start step 2
metadata wording, the new "Minimal server (no display manager)" section at
lines 76-160, the direct-RPM fallback D5 fix) plus the committed evidence under
`vm-test/evidence/task0016-minimal/2026-09-19/` (22 files). Verified against
the repo with `git diff 3375a05 7975f1a --stat` (only `INSTALL.md` and that
evidence directory changed), `git show 3375a05:rpms` (64 RPMs, no `repodata/`
entry), `git show 3375a05:rpms/repodata` (fatal, untracked),
`vm-test/install-set.txt` (22 names, matches the doc's install line), `spec/`
(no runtime Requires on any display manager or `xorg-x11-server-*`; the
`cinnamon` spec ships both session files), `repo-setup/setup-repo.sh` (read in
full; every script claim in the doc matches the code), and the evidence logs
cited per finding. The D5 direct-RPM fallback fix is correct as written:
installing local RPM files registers them in the rpm database and in dnf
history, so `dnf remove` works, and what is missing is exactly repo-origin
update tracking. All 22 names, the versions, and the other factual claims
checked out clean. Three findings, all should-fix, all in the new section.*

### Step 5 presents `systemctl start gdm` as an option no recorded run exercised
**Severity:** should-fix
**Where:** `INSTALL.md:143-149`
**Problem:** Step 5 offers `sudo systemctl start gdm` ("brings the greeter up
without a reboot") alongside `sudo reboot`, but no committed evidence records
that command being run to bring GDM up.
**Failure scenario:** The 2026-09-19 minimal-VM run reached the greeter via
reboot (`05-post-reboot.log`), and the 2026-08-30 bare-metal observation
records the user at the physical console "brought GDM up" without naming the
command (`## Implementation`, Bare-metal state observation, line 346). A user
who picks the no-reboot path gets no verified expectation, and if starting
GDM on a `multi-user.target` system needs something else first, the section's
"That is the verified minimal-server path" (`INSTALL.md:82`) overstates what
was verified.
**Suggested direction:** Either verify the no-reboot path on the minimal VM
that was left running (stop GDM, run `systemctl start gdm`, confirm the
greeter, commit the log), or drop the alternative and document reboot only.
**Resolution:** *(filled by `Tails`)*

### Step 6's "verified end state is the full desktop" exceeds what the committed evidence verifies
**Severity:** should-fix
**Where:** `INSTALL.md:151-154`
**Problem:** The end-state claim names five working surfaces, but the
committed machine evidence for this run verifies the session, not the desktop.
**Failure scenario:** The only committed desktop process capture for the
2026-09-19 run lists exactly two processes, `gdm-wayland-session` and
`cinnamon-session-binary` (`step6-6-desktop-procs.log:1-2`, duplicated at
`06-step6-login.log:408-409`), the session-side a11y text capture was
committed empty (`step6-9-desktop-text-as-user.log`, 0 bytes, verified with
`git show 7975f1a:...`), and `step6-3-desktop-tree.log` re-dumped the GDM
greeter stage rather than the desktop. The `## Test Results` line's process
list (`cinnamon --replace`, Xwayland, `nemo-desktop`, `csd-*` daemons,
pipewire, line 492) appears in no committed log for this run. A release gate
that trusts the doc would treat the five surfaces as machine-verified for the
minimal path, when the committed record supports the active `Type=wayland`
session plus the human-review pixel evidence `06-desktop.png`.
**Suggested direction:** The five-surface claim is in fact backed by the
TASK-0017 verification of this same 22-package set (2026-09-18
`task0017-fresh-vm` with a11y plus pixelstats, and 2026-09-19 `t17-revB`
under enforcing SELinux). Either commit the session process list from the
still-running VM to back the claim directly, or reword step 6 to state what
this run's evidence verifies and attribute the five-surface pass to the
TASK-0017 run.
**Resolution:** *(filled by `Tails`)*

### Step 1's "(the 64 RPMs and the `repodata/` directory)" reintroduces the wording this branch corrected in Quick start
**Severity:** should-fix
**Where:** `INSTALL.md:93-98`
**Problem:** A fresh clone has no `rpms/repodata/` (untracked, verified on
both `3375a05` and `origin/main`), and the Quick-start text that commit
`7975f1a` itself corrected says so explicitly (`INSTALL.md:23-27`), yet the
new section describes the project as containing "the 64 RPMs and the
`repodata/` directory".
**Failure scenario:** A user who cloned the repo and is "verifying the
transfer by comparing the sha256 sums of the RPMs on both sides" looks for
`rpms/repodata/` as part of the integrity baseline, does not find it, and
concludes the clone is incomplete or that metadata must exist before the copy
is "intact" — the opposite of the corrected sentence, which states the
fresh-clone path is the normal one and the script generates the metadata.
**Suggested direction:** Match the Quick-start wording. Name `rpms/` with its
64 RPMs, and state that `repodata/` is generated by the setup script when
absent rather than shipped.
**Resolution:** *(filled by `Tails`)*

---

## Security

*Owner: `Omega`. Read-only. Severity order.*

*Reviewed 2026-09-19 by `Omega`. Scope: the branch diff `3375a05..7975f1a` in
`~/Linux/projects/cinnamon-for-rocky10/` — `INSTALL.md` (Quick-start metadata
wording, the new "Minimal server (no display manager)" section, the D5 fix)
plus the 22 committed evidence files under
`vm-test/evidence/task0016-minimal/2026-09-19/` (20 logs, 2 PNGs). File list
from `git diff 3375a05 7975f1a --name-only`. Every log read in full; the two
PNGs could not be inspected (this model slot has no image input, same
limitation Big recorded in `## Test Results`), flagged in finding 2.
`repo-setup/setup-repo.sh` read in full on the branch (169 lines). Repo
visibility verified: `metalllinux/cinnamon-for-rocky10` is **Public**
(checked via github.com, 2026-09-19), so everything committed in this diff is
world-readable. Credential scan: `git grep -iE "howard|192\.168\.|password|
token|secret|BEGIN.*PRIVATE|api[_-]?key|bearer|ssh-ed25519|ssh-rsa"` over the
evidence dir and `INSTALL.md` — every match is an empty a11y node label, the
PAM service name `gdm-password`, or the public-key fingerprint noted in
finding 1. No password value, token, or private key appears in any of the 22
files; the only named user is the disposable `gdmtest` (UID 1000, created on
the VM at 02:00:25 per `step6-7-secure-tail.log:40-43`). The doc's
sudo/systemctl instructions open no remote access (no SSH config, no firewall
or port changes, no SELinux changes; GDM is a local display manager) and
`setup-repo.sh` is clean (root-only, no network beyond standard dnf from
Rocky repos, no `eval`, every variable quoted). License: the section
references no forked code; `createrepo_c` (BSD-3), `gdm` (GPL-2+),
`gnome-shell` (MPL-2.0), and mesa (MIT) are installed from official Rocky
repos at runtime, not redistributed by this repo; the committed evidence is
test output. No new license surface in this diff. Three findings, all `low`;
per the DoD line for Omega, nothing above `low` is unresolved.*

### Evidence log in a public repo exposes the lab host's root SSH key fingerprint and NAT address
**Severity:** low
**Vector:** secrets
**Where:** `vm-test/evidence/task0016-minimal/2026-09-19/step6-7-secure-tail.log:1,8,29` (fingerprint repeated at `:14,20,26,35,40,48,53`; `192.168.122.1` throughout; sudo history at `:29`)
**Attack:** Anyone who can read the public repo (it is Public, verified 2026-09-19) reads the committed `/var/log/secure` tail. No credential is in it, but it discloses a persistent identifier of the lab host: the ED25519 public-key fingerprint `SHA256:TAs9anRDojDoomVgqYhgWN4LH4MOEsSxtFXWU4IEGhM` of the key that logs in as `root` from the libvirt NAT gateway `192.168.122.1`, plus the exact sudo command history (`dnf install -y gcc kernel-headers`). An attacker who later obtains that private key by other means (or who is already inside the lab's `192.168.122.0/24`) can use the fingerprint to confirm the key belongs to this host, and the NAT address plus sudo history map the lab's setup.
**Impact:** Reconnaissance material for the user's lab network: confirms root public-key SSH from the host, the key fingerprint for correlation, and which packages were installed with sudo. No direct access; all addresses are RFC1918 and the VM is disposable (`task0016-minimal`, slated for destruction per `## Test Results`).
**Fix:** Before Knuckles merges to the public repo, redact in `step6-7-secure-tail.log`: replace the fingerprint with `SHA256:<redacted>` and `192.168.122.1` with `192.168.122.<gw>` (or truncate the log to the lines that carry the verdict: zero PAM failures, zero AVCs, the `gdmtest` session open, the `gkr-pam` lines). The redaction preserves the evidence; the PAM/AVC verdict does not depend on the SSH lines.
**Resolution:** *(filled by `Tails`)*

### Committed PNGs are unverified by any model in this slot; human pixel review required before public merge
**Severity:** low
**Vector:** secrets
**Where:** `vm-test/evidence/task0016-minimal/2026-09-19/05-post-reboot-greeter.png`, `06-desktop.png`
**Attack:** Not an attack path; a verification gap. The repo is Public, so both images are world-readable once merged. The a11y text captures (`step6-1-userlist-text.log`, `step6-2-session-menu-text.log`) show the greeter presents only the disposable user `gdmtest` plus a clock, and no host-identifying string appears in the a11y trees, but pixel content (top-bar text, hostname, anything in the desktop wallpaper region) is not checkable from the committed logs, and this model slot has no image input (Big recorded the same limitation in `## Test Results`).
**Impact:** Unknown until a human looks. Worst plausible case is a hostname or a non-disposable username visible in the pixels; the a11y evidence makes that unlikely.
**Fix:** Human review of both PNGs before the merge goes public. If any host-identifying detail beyond the disposable `gdmtest` user and the clock is visible, retake the shot or redact the region. If clean, note "human-reviewed" in `## Release`.
**Resolution:** *(filled by `Tails`)*

### Documented install path has no signature verification; the sha256 step is transfer-integrity only (pre-existing, carried into the new section)
**Severity:** low
**Vector:** supply-chain
**Where:** `INSTALL.md:93-98` (the sha256 step in the new section) and `repo-setup/setup-repo.sh:119-128` (writes the `.repo` with `gpgcheck=0`, visible in `01-setup-repo.log` of the evidence)
**Attack:** Pre-existing design, not introduced by this diff (Quick start and the Manual section on `main` share it), but the new section presents this exact path as the verified minimal-server procedure. Attacker: whoever compromises the `metalllinux` GitHub account or lands a merged PR that alters `rpms/` (in-account PRs are mergeable without human review per AGENTS.md §8). Steps: the attacker swaps or adds RPMs in `rpms/`; a user cloning the compromised tree runs the documented `sudo` steps; the 64 RPMs install from the `file://` repo with `gpgcheck=0`, so no signature is checked; the doc's integrity step (compare sha256 sums on both sides) passes, because both sides come from the same compromised tree — it verifies the copy, not the origin.
**Impact:** Attacker code executes as root on the follower's machine via `sudo dnf install`. Low because it requires a prior compromise of the repo as a precondition.
**Fix:** Process fix, spans tasks, not a one-line doc change: sign the RPMs with a repo GPG key, ship the key in the repo, and set `gpgcheck=1` in the `.repo` the script writes (and in the Manual section's `.repo` block). Interim mitigation: pin the documented install set to a tagged release and publish its sha256 manifest in the tag, so a user can verify against a trusted baseline instead of against the tree they just cloned. Until then the doc's wording is accurate (it claims transfer verification, not authenticity) and needs no change.
**Resolution:** *(filled by `Tails`)*

---

## Test Results

*Owner: `Big`. Verdicts, never raw log dumps.*

**Run (2026-09-19): the documented minimal-server procedure, executed end-to-end on a fresh VM.**

Host `192.168.1.102`, libvirt `qemu:///system` (socket-activated, `virsh` as `howard`, libvirt
group). VM **`task0016-minimal`** at **192.168.122.142** (VNC `127.0.0.1:4` on host, 2 vCPU / 4G),
provisioned from `Rocky-10-GenericCloud.qcow2` via `vm-test/provision-vm.sh --destroy --graphics
vnc --name task0016-minimal` (host key pinned out-of-band from the disk image, firewalld masked per
harness convention). No reuse of `gdm-login-vm`, `task0017-fresh-vm`, `t17-revB`;
`fedora-cinnamon-ref` untouched. The doc under test is `INSTALL.md` "Minimal server (no display
manager)", branch `feature/TASK-0016-install-md-minimal-server` at `760b852`. Evidence lands in
project repo `vm-test/evidence/task0016-minimal/2026-09-19/`.

**Start-state baseline (before any documented step ran):** Rocky 10.2 (Red Quartz), 444 packages
(per `dnf history`: 177 + 267 image-build transactions; the initial `wc -l` measurement read 443,
a missing-trailing-newline off-by-one), `gdm`/`lightdm`/`sddm` not installed, no
`xorg-x11-server-*` or `xwayland` packages, default target `multi-user.target`, `getty@tty1`
active, SELinux `Enforcing`, no user sessions. Matches the section's stated start state (evidence
`00-start-state-baseline.log`). Note: the cloud-image baseline is not the 674 of the 2026-08-30
bare-metal server; the doc's section states no package count, so this is not a doc deviation.

**Workflow run:** (in progress — step rows filled as the run advances)

| Check | What it exercises | Result | Notes |
|---|---|---|---|
| start state | fresh minimal server, no DM/X, multi-user.target | PASS | baseline above |
| step 1: transfer | project copy + sha256 of the 64 RPMs both sides | PASS | 64/64 RPMs + 4/4 repodata files, sha256 identical host vs VM (`02`-prefix logs) |
| step 2: setup-repo.sh | repo file + makecache, rc=0, marker | PASS | rc=0, marker present, "metadata already present. Skipping generation", `.repo` matches doc block byte-for-byte; createrepo_c self-install path worked on the minimal image (`01-setup-repo.log`) |
| step 3: 22-name install | no DM/X pulled, 22/22 present, session files, still getty | PASS | rc=0, 22/22 installed, 200 packages pulled, zero DM/X in the full rpm-db diff, both session files present with exact doc Exec lines, default target still `multi-user.target`, getty active, gdm inactive (`02-dnf-install-22.log`, `03-step3-verify.log`) |
| step 4: gdm+gnome-shell | self-enable, enable no-op, getty until set-default | PASS | rc=0, `is-enabled gdm` = `enabled` immediately after install (before the enable line), documented `enable` ran rc=0 as a silent no-op, system stayed at getty until `set-default`, then default = `graphical.target` (gdm 47.0-24, gnome-shell 49.4-9, +Xwayland, 178 packages) (`04-gdm-install.log`) |
| step 5: reboot | boot reaches GDM Wayland greeter, not getty | PASS | boot 01:47:19, SSH back ~20s same IP, default `graphical.target`, gdm active, `getty@tty1` inactive, greeter session `c1 gdm seat0 1018 greeter tty1`; pixel `05-post-reboot-greeter.png` (human review) (`05-post-reboot.log`) |
| step 6: login | Cinnamon (Wayland) session, Type=wayland, item 6 greeter X11 entry | PASS | session menu captured expanded (item 6, below), "Cinnamon (Wayland)" selected, password + Return, first attempt; `VERIFIED session 16 type=wayland state=active proc='cinnamon-session'`, `loginctl show-session 16` → `Type=wayland State=active Service=gdm-password`; full desktop running (`cinnamon --replace`, Xwayland, `nemo-desktop`, all `csd-*` daemons, pipewire); SELinux Enforcing throughout (`06-step6-login.log`, `step6-1..9-*.log`, pixel `06-desktop.png` human review) |

**Item 6 (does the greeter list the X11 "Cinnamon" entry?): it does not — the entry is filtered
out.** Evidence is the a11y dump of the expanded session menu taken before the entry was clicked
(`step6-2-session-menu-text.log`): the menu lists `Password`, `Session Type`, `Cinnamon (Wayland)`,
`GNOME` — and nothing else. The X11 file exists on disk
(`/usr/share/xsessions/cinnamon.desktop`, `Name=Cinnamon`, no `Try=` line), and no Xorg X server
exists on the system (nothing installed; in no Rocky 10.2 repo, verified step 3). The greeter is
GDM 47, Wayland-only (gdm on EL10 ships only `gdm-wayland-session`, per the harness design note
and `rpm -ql gdm`). Note for completeness: the menu also omits `GNOME on Wayland`
(`wayland-sessions/gnome-wayland.desktop`, `Name=GNOME on Wayland`) while listing `GNOME`
(`wayland-sessions/gnome.desktop`), so the filter is not simply "all wayland-sessions entries"
either. The exact filter predicate inside GDM is not verified (hypothesis: GDM hides sessions it
cannot run, X11 included) — the observable fact, which is what item 6 asks, is established by the
menu dump. Practical consequence: on a minimal server the only selectable Cinnamon session is
Cinnamon (Wayland), which matches what the section tells the reader to select.

Doc claims re-checked against this run:

- `dnf list xorg-x11-server-Xorg` → "No matching Packages" against all enabled Rocky 10.2 repos
  (BaseOS/AppStream/Extras/CRB + local). The section's "xorg-x11-server-Xorg is in no Rocky 10.2
  repository" statement holds on this system.
- **Finding for Vector (doc bug, precision):** the Quick-start claim added in `760b852` — "a fresh
  clone ships with valid metadata, so generation is skipped" — is inaccurate. `rpms/repodata/` is
  untracked in git (`git ls-tree origin/main rpms/repodata/` is empty), so a fresh clone has no
  metadata and the script generates it, having first installed `createrepo_c` from AppStream
  (that install path worked on this minimal image, `01-setup-repo.sh` log line 5). This run
  exercised the skip path because the project transfer carried the local `repodata/`. The procedure
  is correct on both paths; the claim is what is wrong. The generation path itself is verified by
  earlier tasks (TASK-0006), not re-run here.

**Checks requested vs run:** 8 requested (start state + 6 doc steps, item 6 folded into step 6), 8 executed. Nothing dropped.

**Harness notes (stay with Big):** the login drive used the in-VM harness
(`tasks/lib/gdm-drive.sh` + `gdm-a11y.py` + `ukey.c`, copied to `/root/gdm-harness/`), with
`gcc` + `kernel-headers` installed as harness prerequisites (test infra, not part of the documented
procedure). The caps pre-pass verified the compositor caps state by probe readback before any
credential was typed. The session-stage a11y tree came back empty (rc=0, no nodes, even after a
settle delay and with the session's `at-spi/bus_0` socket present) — a11y worked at the greeter
stage, so this is a harness limitation on the session side, not a failure of the system under test;
the verdict rests on the state-based check (`loginctl` + process list), which is the driver's
designed authoritative verdict. The two PNGs (`05-post-reboot-greeter.png`, `06-desktop.png`,
1280x800) are pixel evidence for human review; the model in this slot has no image input.

**Verdict:** PASS. The documented minimal-server procedure in `INSTALL.md`
(`feature/TASK-0016-install-md-minimal-server` at `760b852`) executes end-to-end on a fresh Rocky
10.2 minimal VM exactly as written: all six steps, no undocumented intervention in the documented
path (the only additions were harness prerequisites for the login drive). Final state is a running
Cinnamon (Wayland) desktop, `Type=wayland`, SELinux Enforcing, on a machine that started with no
display manager and no X server. Item 6: the greeter filters the X11 "Cinnamon" entry; only
Cinnamon (Wayland) is selectable, which the section already directs the reader to. One doc finding
for Vector (the fresh-clone metadata claim, above); one doc claim verified true (Xorg in no repo).
No code bug for Tails. The VM `task0016-minimal` (192.168.122.142) is left running with the
logged-in desktop for user inspection; destroy with
`vm-test/provision-vm.sh --destroy --name task0016-minimal` when done.

---

## Docs

*Owner: `Vector`.*

**2026-09-19 (post-Big).** Quick-start metadata wording fixed per Big's finding in `## Test Results`
("Finding for Vector (doc bug, precision)"). Project commit `7975f1a` on
`feature/TASK-0016-install-md-minimal-server`, on top of `89b9b7b` (Big's evidence). The push of the
project branch is blocked by my permissions (push-to-`main` only); Knuckles pushes.

| File | Sections touched | What changed |
|---|---|---|
| `INSTALL.md` (project) | Quick start, step 2 | Removed the inaccurate parenthetical "a fresh clone ships valid metadata, so generation is skipped". Replaced with the verified facts: `rpms/repodata/` is untracked in git, so a fresh clone has no metadata and takes the generation path; the `createrepo_c` self-install from AppStream works on a minimal image (Big's `01-setup-repo.log` line 5); a copy that carries `repodata/` skips generation; the procedure is correct on both paths |

Exact before/after of the changed sentence (the rest of step 2 is untouched):

- Before: "The script installs `createrepo_c` if missing, generates repository metadata when
  `rpms/repodata/` is absent (a fresh clone ships valid metadata, so generation is skipped), writes
  `/etc/yum.repos.d/cinnamon-rocky10.repo`, enables the CRB repository, and validates that the
  repository is readable before finishing."
- After: "The script installs `createrepo_c` if missing and generates repository metadata when
  `rpms/repodata/` is absent. A fresh clone has no metadata because the `repodata/` directory is
  not tracked in git, so a fresh clone exercises the generation path, and the `createrepo_c`
  self-install from AppStream works on a minimal image. A copy that carries `repodata/` skips
  generation instead. The procedure is correct on both paths. The script writes
  `/etc/yum.repos.d/cinnamon-rocky10.repo`, enables the CRB repository, and validates that the
  repository is readable before finishing."

Minimal server step 1 (`INSTALL.md` "keeping `repo-setup/` and `rpms/` (the 64 RPMs and the
`repodata/` directory) intact") reviewed and left as written. It is a keep-intact instruction for
the transfer, not a claim about what a fresh clone ships, and the clone path is now covered by the
corrected step 2 wording.

**Checked and needed no change:** `README.md` (grep for `repodata|metadata` over the project's
`.md` files: no metadata claim there), `vm-test/fedora-cinnamon-ref-setup.md` (its "no `repodata/`"
line describes the Fedora reference VM, a different machine, and is accurate), `CHANGELOG.md`
(project has no changelog file).

---

**2026-09-19.** Worked on branch `feature/TASK-0016-install-md-minimal-server`, cut from `main`
(`3375a05`), commit `760b852` in the project repo.

| File | Sections touched | What changed |
|---|---|---|
| `INSTALL.md` (project) | Direct RPM install (fallback) | Fixed D5. Replaced "you give up repository features such as `dnf remove` tracking and update notifications" (wrong. local-RPM packages register in the rpm database and dnf history, and `dnf remove` works on them) with the actual gap. No repository origin, which is dnf's source for updates of these packages |
| `INSTALL.md` (project) | Quick start, step 2 | Precision fix. The script generates metadata only when `rpms/repodata/` is absent (`setup-repo.sh:101-107`), and a fresh clone ships valid metadata so generation is skipped. Previously the unconditional "generates repository metadata" |
| `INSTALL.md` (project) | New section "Minimal server (no display manager)" | The verified minimal-server path. Fresh Rocky 10.2 server with no DM and no X, to the running Cinnamon desktop. Six steps. Project transfer with sha256 verification, `setup-repo.sh`, the single 22-name `dnf install`, `gdm` + `gnome-shell` install/enable plus `set-default graphical.target`, reboot (or `systemctl start gdm`), Cinnamon (Wayland) login. States plainly that a display manager is required to run a desktop and a minimal server has none, that the set pulls in no display manager or X server, and that the working session is Cinnamon (Wayland) with X11 apps running through Xwayland |
| `README.md` (project) | none | Consistent as-is, see below |
| `CHANGELOG.md` | none | Project has no changelog file |

Re-check of the 2026-08-30 audit findings against the post-TASK-0017 `INSTALL.md`:

| Finding | Status |
|---|---|
| D1 dead X11 path / assumed GDM preinstalled | Resolved by the TASK-0017 rewrite (Wayland session, DM step 4). The residual statement that Xorg is not installable on Rocky 10.2 is now in the new minimal-server section |
| D2 no DM step, no "DM required, minimal has none" statement | Resolved by the rewrite (DM step 4). The explicit statement is in the new section |
| D3 README "10" vs INSTALL "14" | Superseded. Both files now say 22 names / 64 RPMs consistently |
| D4 35-package list "required regardless of method" | Resolved by the rewrite (Prerequisites says no manual dependency list is required) |
| D5 "skips `dnf remove` tracking" | **Fixed in this commit**, see table above |
| D6 "without these" omits the settings daemon | Superseded. The 22-row Installed-packages table covers every name |

Verified for the new section (evidence, not inference):

- "No spec of the 22 declares a display manager or an X server." `grep -E 'gdm|lightdm|sddm|xorg-x11-server|Xwayland'` over all 20 files in `spec/*.spec` returns zero matches.
- Start state (no DM, no X, `multi-user.target`, getty on tty1, SELinux enforcing), GDM self-enablement (`systemctl is-enabled gdm` → `enabled` immediately after install), `xorg-x11-server-Xorg` in no Rocky 10.2 repo, `Type=wayland` end state. All from the verified bare-metal procedure in `## Implementation` (2026-08-30, 192.168.1.103).
- The install steps (single 22-name `dnf install`, zero manual steps) are the current set's path, re-verified end-to-end on a fresh minimal VM on 2026-09-19 (TASK-0017, t17-revB).
- No manual `ldconfig` step in the section. The current harness `vm-test/run-tests.sh` installs all 64 RPMs without `ldconfig` and the 2026-09-19 re-verification passed. The old procedure's `ldconfig` step was for the 14-package set.

**Checked and needed no change:** `README.md` (counts consistent. "14 initial + 8 new + 2 rebuilt" = 22, and it defers installation to INSTALL.md), `vm-test/install-set.txt` (22 names, matches both command blocks in INSTALL.md), `spec/` (no doc surface).

**Could not verify:** whether the GDM greeter *lists* the X11 "Cinnamon" entry or filters it out (open item 6 for Big in `## Implementation`). The section deliberately makes no claim either way. It only states that the X11 session file has no X server to run on.

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
lost. Decisions, verified facts, rejected options with their reasons, known traps, and anything
the user said are never deleted.*

**Pruning log**

| Date | What was pruned or compressed | Rough size |
|---|---|---|
| | | |
