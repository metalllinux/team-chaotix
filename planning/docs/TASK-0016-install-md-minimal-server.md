# TASK-0016 — INSTALL.md: verify all instructions + add minimal-server (no login manager) install-and-run section

> **Section order below is fixed.** Each agent writes to its own section and no other. `Robotnik`
> reads only `## Status` and `## Next Actions`. Do not reorder, rename, or remove sections.

- **Created:** 2026-08-30

---

## Status

*Owner: `Robotnik`. Keep this SHORT and CURRENT — it is one of only two sections the PM reads, so a
stale entry means the whole loop runs on bad information.*

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

- [ ] `Tails`: audit every existing `INSTALL.md` instruction (verify each step against the repo and
      by execution; record discrepancies) and produce the verified minimal-server procedure
      (install RPM set + GDM + set-default graphical + reboot + Cinnamon (Wayland) session),
      reconciling the package count. Write to `## Implementation`.
- [ ] `Vector`: write the corrected + extended `INSTALL.md` (and `README.md` if affected) from the
      verified procedure; write to `## Docs`.
- [ ] `Big`: run the exact minimal-server procedure from the updated doc on a fresh minimal Rocky
      10.2 VM to prove it is executable end-to-end; record in `## Test Results`.
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
lost. Decisions, verified facts, rejected options with their reasons, known traps, and anything
the user said are never deleted.*

**Pruning log**

| Date | What was pruned or compressed | Rough size |
|---|---|---|
| | | |
