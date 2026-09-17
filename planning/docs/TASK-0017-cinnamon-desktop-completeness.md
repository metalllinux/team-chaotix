# TASK-0017 — Complete the Cinnamon desktop: missing subpackages, Rocky wallpaper, branding, terminal

> **Section order below is fixed.** Each agent writes to its own section and no other. `Robotnik`
> reads only `## Status` and `## Next Actions`. Do not reorder, rename, or remove sections.

- **Created:** 2026-08-30

---

## Status

*Owner: `Robotnik`. Keep this SHORT and CURRENT — it is one of only two sections the PM reads, so a
stale entry means the whole loop runs on bad information.*

**Now (2026-09-17, post-2.2): items 2.2 + 0.3 complete (Big); parity matrix 9/11 PASS.**
Wallpaper fix re-verified: the initially-dark 2.2 capture was the **night variant** of the
animated Gemstone Skies wallpaper (screenshot stats match
`rocky-default-10-gemstone-skies-night.png` almost exactly; the capture ran at night) — the fix
holds. Ref-side baseline capture (0.3) complete. 11-row parity matrix vs
`fedora-cinnamon-ref`: PASS on both sides — panel applets, wallpaper, themes, screensaver, main
menu, nemo, session/power controls. Rocky FAILs: (1) **Cinnamon Settings (control-center)** —
3 Python modules absent from every EL10 and EPEL repo (`setproctitle`, `PIL`, `tinycss2`; the
unguarded import at `cinnamon-settings.py:11` kills the whole app) — routed to `Tails`
(source-build the modules or patch the imports, decision recorded); (2) **terminal** — expected,
item 1.4 pending. Next: Tails control-center dep fix → Tails 1.4 → Big 3.1 fresh-VM end-to-end.

**Now (2026-09-17): 2.1 defect root-caused + fixed (Tails).** The `gnome-bg` image branch of
`libcinnamon-desktop` built its surface with an API that does not composite on the
gtk-layer-shell/Wayland background window, so photo wallpapers painted black (the solid-color
branch was already correct — flat colors showed, photos did not). Fix: patch (Patch0) rendering
onto a window-similar surface, `cinnamon-desktop` rebuilt as `6.7.2-2.el10`, plus a new
`gdk-pixbuf-parsers` RPM (stock EL10 `gdk-pixbuf2` ships no PNG/JPEG loaders). Verified on
`gdm-login-vm` fresh first login (nonblack 1.000, colorful 0.950, 2551 distinct colors). Repo
re-published with the fixed set (specs + patch in the canonical `spec/` dir). Next: Big item 2.2
re-verification, then Tails 1.4 (terminal source build) and the 3.x end-to-end + parity runs.

**Now (2026-09-15, post-2.1): item 2.1 complete (Big) — one open defect.** GDM login, panel,
menu-button branding, and wallpaper config all **PASS** (the Rocky logo renders in the panel; the
A5 pixmaps gap is closed). Wallpaper **render FAIL**: the desktop region is 100% black (VNC +
`virsh screenshot` agree) — the nemo-desktop Wayland surface is not composited on the virtio-vga
path while the panel is; static-PNG, nemo-desktop respawn, and desktop-icon tests all negative.
Ref A/B not run (`fedora-cinnamon-ref` has no logged-in Cinnamon session path yet; greeter-only
capture saved). Open question: defect vs environment limitation. Decision: `Tails` investigates
with a disposable **qcow2 overlay** of the ref disk for the A/B (the pristine golden ref is never
touched; methodology recorded). If the ref renders on identical VM hardware, it is our defect and
gets fixed; if the ref is also black, it is an environment limitation and gets recorded in `##
Status` as a deviation with evidence.

**Now (2026-09-15, post-1.2): item 1.2 complete (Tails).** Host repo baseurl fixed;
`cinnamon-rocky-defaults-1.0-1.el10.noarch` built, published (49 RPMs), verified install/uninstall
on `gdm-login-vm`. Two evidence-forced plan deviations recorded in `## Implementation`: the dconf
override ships flat at `/etc/dconf/db/local.d/` (EL10 dconf reads only that path, A/B tested live),
and no icon file is shipped (the `fedora-logo-icon` hicolor entry from rocky-logos is provably the
Rocky logo; avoids the trademark clause). Cross-item correction: the wallpaper files are owned by
`rocky-backgrounds`, not `rocky-logos` (plan fact 1 wrong; both in the install set, the RPM
`Requires:` both). Commit `a971031` on `feature/TASK-0017-cinnamon-desktop-completeness`. Next:
Big item 2.1 (live-session render check).

**Now (2026-09-15): item 0.1 complete (Big); plan refinements owed.** A1 **FAIL** (gnome-terminal
in no Rocky 10 or EPEL repo — the terminal decision reopens; Amy's plan fallback must be made
concrete). A2 PASS refined (the Cinnamon background schema has `picture-uri` but no
`picture-uri-dark` — the dconf override targets `picture-uri` only). A4 PASS (shell RPM: 34 applet
dirs, 3 desklets, settings desktops, sessions present). A5 PASS refined (menu icon =
`org.cinnamon app-menu-icon-name`, icon-theme based; Rocky assets must ship as an icon-theme entry
+ compiled gschema override, the Fedora baseline pattern). Environment repairs recorded in `## Test
Results`: `fedora-cinnamon-ref` had a **re-armed repair-boot trap** (contradicting TASK-0018's
removal record; root cause unidentified, process gap flagged) — fixed, the VM now boots installed
Fedora 44 at 192.168.122.156; host `/etc/yum.repos.d/cinnamon-rocky10.repo` baseurl is a dead
path (blocker for item 1.2). Next: Amy updates `## Plan` to reflect the verdicts, then Tails 1.x/2.x.

**Now (2026-09-14): resumed per user instruction; testing environment changed; parity goal added.**
User orders (2026-09-14): (1) continue Cinnamon-for-Rocky-10 development; (2) the bare-metal
machine `192.168.1.103` is **no longer available for testing** (no ICMP reply from the PM host,
verified 2026-09-14); (3) **all testing stays on this host (`192.168.1.102`)** via libvirt VMs;
(4) the Rocky 10 Cinnamon desktop must reach **desktop feature parity with the Fedora Cinnamon
VM** — `fedora-cinnamon-ref` (Fedora 44, cinnamon 6.6.7, lightdm; verified state per TASK-0018)
is the comparison baseline, and work continues until features match. DoD updated: the bare-metal
box is superseded by a host-VM box; a parity box is added. Environment verified 2026-09-14:
libvirt socket-activated and answering; `gdm-login-vm` running (TASK-0008's live GDM+Cinnamon
VM, VNC 127.0.0.1:5900); `fedora-cinnamon-ref` and `rocky10-explore` defined, shut off; clone
`~/Linux/projects/cinnamon-for-rocky10/` on main at `c1de933` (TASK-0008's fixes are on main via
the rebase merge; the local `task-0008-gdm-auth` branch is stale, tip `f259dd5`). `Amy`'s plan
dispatch (two deaths 2026-08-30, endpoint flapping) re-dispatches now with the parity goal in
scope.

**Now (2026-08-30): task created from direct user feedback.** The user boots into Cinnamon (Wayland)
on the bare-metal host `howard@192.168.1.103` (GDM auth from TASK-0008 works), but the desktop is
substantially incomplete. Reported items: (1) black wallpaper — wants a Rocky Linux 10 wallpaper
from the Rocky wallpaper RPM installed and set automatically on first login; (2) the tray/panel
shows the Cinnamon logo, not the Rocky Linux logo; (3) Cinnamon applets, themes, and extensions do
not load; (4) the only application that loads is the file manager (nemo); (5) the Cinnamon Settings
menu is missing; (6) the terminal (gnome-terminal) won't open. User took screenshots in `~/Pictures`
(only one found: `Screenshot 2026-08-30 21-49-39.146.png`, 3840x2160; user said "multiple" and the
message cut off at "There does" — request the rest). **Model limitation: no image input, so the
screenshots cannot be viewed by any agent; diagnosis runs on the user's text + package/log evidence,
and the screenshot is retained as an artifact.**

**Evidence gathered (2026-08-30):** the installed and built Cinnamon set is a **subset** of 13
runtime RPMs — `cinnamon`, `cinnamon-control-center`, `cinnamon-desktop`, `cinnamon-menus`,
`cinnamon-session`, `cinnamon-settings-daemon`, `cjs`, `mozjs115`, `muffin`, `muffin-clutter`,
`muffin-cogl`, `nemo`, `xapps-lib` (48 total in `rpms/` incl. debuginfo/debugsource/devel). A full
Cinnamon 6.7 desktop additionally needs the monorepo subpackages (themes, international/applets/
desklets, extension-manager, plugin-applet/desklet/file-manager/screensaver, screensaver,
translations, desktop-filesystem) plus a terminal — none are built or installed. `rocky-logos`
**is** installed (so the branding assets exist but are not applied). **Root-cause hypothesis
(unverified): the build only produces a subset of the cinnamon monorepo subpackages.**

**Environment / scope:**
- Files in scope: the Cinnamon build system (specs + build scripts) and the RPM set in
  `metalllinux/cinnamon-for-rocky10`; the cinnamon monorepo source (subpackages); wallpaper/
  branding/terminal config; the "Cinnamon set" definition (coordinates with TASK-0016's INSTALL.md).
- Touches the DB schema: no
- Graphical UI: yes — the desktop session itself; VM + bare-metal testing required
- Rocky Linux target: yes (Rocky Linux 10.2)

**Unknowns:**
- The exact full set of cinnamon subpackages a complete 6.7 desktop needs, and which are present in
  the source tree but not built. (Investigate.)
- The build system's structure and how new subpackage builds are added. (Investigate.)
- The Rocky wallpaper package name and which wallpaper to default to. (Verify, do not guess.)
- The mechanism to set the wallpaper automatically on first login. (Design.)
- How the tray/panel branding is switched from the Cinnamon logo to the Rocky logo using
  `rocky-logos`. (Investigate.)
- Which terminal to ship (gnome-terminal from the base repo vs. another). (Design.)
- Why the Cinnamon Settings menu is absent although `cinnamon-control-center` is installed (missing
  `.desktop`/menu generation vs. launch failure). (Diagnose.)

**Coordination / priority:** this task redefines "the Cinnamon RPM set" from the 13-subset to the
complete set. It is the current priority (the user's active ask). TASK-0016's INSTALL.md doc-writing
is **paused** until this task lands, so the docs can describe the complete set. TASK-0015's multi-DM
matrix should test the **complete** set, so it also follows this task.

**Infra note (2026-08-30):** the first two `Amy` plan dispatches for this task died with
"Connection reset by server" — the EVO-X2 model endpoint flapping (HTTP 200 on probe, drop under
inference load); the TASK-0010 GPU-wedge problem is live. Endpoint recovered after a 60s cooldown;
retrying. If dispatches keep dying, the block is the endpoint, not the agent — escalate to the user
rather than burning retries.

---

## Definition of Done

*Owner: `Robotnik`, and nobody else. Written **before** any work starts. Objectively checkable —
if a box cannot be verified by looking at something, rewrite it.*

- [ ] **Complete package set.** The missing cinnamon monorepo subpackages required for a full 6.7
      desktop are built and added to the RPM set and the documented install set. The exact list is
      established by the plan/diagnosis (recorded in `## Plan`/`## Implementation`), not guessed.
- [ ] **Terminal.** A working terminal (gnome-terminal) is part of the desktop set/install and opens
      from the Cinnamon session.
- [ ] **Wallpaper.** The Rocky Linux 10 wallpaper (from the Rocky wallpaper RPM) is installed and is
      set automatically on first login — the session does not start with a black wallpaper.
- [ ] **Branding.** The tray/panel shows the Rocky Linux logo, not the Cinnamon logo (using
      `rocky-logos`).
- [ ] **Applets load.** The default Cinnamon applets are present and load in the panel (no missing/
      erroring applets).
- [ ] **Themes load.** The Cinnamon theme files are present on the installed system (per the plan's
      verified subpackage inventory, themes ship inside the `cinnamon` shell package at 6.7; there
      is no standalone `cinnamon-themes` package — D1, 2026-09-14), the default theme applies at
      login, and themes are selectable in the theme selector without breakage.
- [ ] **Extensions work.** The extension/applet/desklet manager is present and functional (can list
      and enable the shipped extensions/applets/desklets).
- [ ] **Settings menu.** The Cinnamon Settings menu is present in the menu and opens control-center.
- [ ] **File manager still works.** nemo opens and functions (regression check).
- [ ] **VM end-to-end.** On a fresh minimal Rocky 10.2 VM: install the complete set, log in via GDM
      (Cinnamon Wayland), and every item above is verified working. Recorded in `## Test Results`
      with evidence.
- [ ] **Host-VM end-to-end (supersedes the bare-metal box; `192.168.1.103` is no longer
      available for testing, user 2026-09-14).** On a Rocky 10.2 VM on host `192.168.1.102`:
      install or update to the complete set and every item above is verified working. Recorded
      in `## Test Results` with evidence.
- [ ] **Desktop feature parity vs the Fedora reference.** A documented comparison of the Rocky 10
      Cinnamon desktop against `fedora-cinnamon-ref`: a feature checklist established in `## Plan`
      (at minimum: panel applets, themes, extension/applet/desklet manager, screensaver,
      Cinnamon Settings, main menu, nemo, terminal, session/power controls), each item PASS/FAIL
      on both sides with evidence, recorded in `## Test Results`. Every gap is either closed in
      this task or recorded in `## Status` as a deviation with the reason. Goal (user, 2026-09-14):
      the features match the Fedora Cinnamon VM.
- [ ] `Shadow`: no unresolved blockers or should-fix findings in `## Review`.
- [ ] `Omega`: no unresolved findings above `low` in `## Security`.
- [ ] `Big`: all harness checks PASS, with no silently dropped checks.
- [ ] `Vector`: `INSTALL.md`/`README.md` updated to describe the complete set (coordinates with
      TASK-0016).
- [ ] `Knuckles`: merged to `metalllinux/cinnamon-for-rocky10` main via PR.

---

## Next Actions

*Owner: whoever wrote last. The future only — delete what has been done. The second of the two sections
the PM reads.*

- [x] `Amy` (2026-09-14): `## Plan` written (lines 159–445). Key decisions: wallpaper =
      `rocky-logos` (Gemstone Skies) applied via a new small RPM `cinnamon-rocky-defaults`
      (dconf readonly override; the rocky-logos override targets GNOME, not Cinnamon); branding via
      the same defaults package; terminal = gnome-terminal (assumption A1); **no missing monorepo
      subpackages** (applets/desklets/settings/menu/themes already ship in the shell RPM; screensaver
      folded into `cinnamon` at 6.7) — delta is 2 system packages + 1 new RPM + spec/run-tests fixes;
      parity = read-only `parity-inventory.sh` on `fedora-cinnamon-ref` (baseline) + our fresh VM.
      14 work items (0.1–4.3), budget 42 dispatch turns. **D1 flagged to Robotnik: DoD themes box
      named a `cinnamon-themes` package that does not exist in 6.7 — resolved 2026-09-14 by
      rewriting the DoD box to the functional check.**
- [x] `Big` (2026-09-15): plan item 0.1 — environment verification on host `192.168.1.102`,
      assumptions A1/A2/A4/A5 settled (verdicts in `## Test Results`; summary in `## Status`).
      A1 FAIL (no gnome-terminal in any Rocky 10/EPEL repo) reopens the terminal decision; A2/A5
      pass with mechanism refinements.
- [x] `Amy` (2026-09-15): `## Plan` updated per the item 0.1 verdicts — terminal decision
      concrete: **source-build gnome-terminal as an RPM in this repo** (item 1.4; fallback konsole
      from EPEL with a recorded deviation if the EL10 dependency chain fails; 1-pager
      `planning/decisions/TASK-0017-terminal-choice.md`); wallpaper override `picture-uri`-only;
      branding = Rocky logo as icon-theme entry + compiled gschema override (Fedora baseline
      pattern); dead-baseurl fix is the first step of item 1.2; ref-VM repair-boot trap re-check in
      the baseline-capture procedure. Budget: 47 dispatch turns (2 consumed).
- [x] `Tails` (2026-09-15): plan item 1.2 — host repo baseurl fixed; `cinnamon-rocky-defaults`
      built + published (49 RPMs) + verified on `gdm-login-vm`; two evidence-forced deviations
      recorded in `## Implementation` (dconf flat path; no icon shipped — uses `fedora-logo-icon`);
      cross-item correction: wallpaper owned by `rocky-backgrounds` (plan fact 1). Commit `a971031`.
- [x] `Big` (2026-09-15): plan item 2.1 — live-session render check. PASS: GDM login, panel,
      menu-button branding (Rocky logo rendered), wallpaper config. **FAIL: wallpaper render**
      (desktop 100% black; nemo-desktop Wayland surface not composited on virtio-vga). Ref A/B not
      run (no logged-in Cinnamon path on the ref yet). Evidence in `## Test Results` +
      `vm-test/parity/` PNGs.
- [x] `Tails` (2026-09-17): 2.1 defect resolved — root cause: `gnome-bg` image branch surface
      API does not composite on the gtk-layer-shell/Wayland background window (photo → black;
      solid color was fine). Fix: Patch0 + `cinnamon-desktop` 6.7.2-2.el10 + new
      `gdk-pixbuf-parsers` RPM; verified on `gdm-login-vm` fresh first login. Record in `##
      Implementation`. Re-verification via Big (item 2.2).
- [x] `Big` (2026-09-17): plan item 2.2 (+ 0.3 baseline) — wallpaper fix re-verified (night
      wallpaper variant explained the dark capture; fix holds); ref baseline captured; 11-row
      parity matrix written (9 PASS both sides; Rocky FAILs: control-center deps, terminal).
      Evidence in `## Test Results` + `vm-test/parity/`.
- [ ] `Tails`: control-center Python dependency fix — `setproctitle`, `PIL`, `tinycss2` absent
      from every EL10/EPEL repo (root cause per Big's 2.2 entry); source-build them or patch the
      imports (decide + record in `## Implementation`), republish the repo, verify
      cinnamon-settings opens on `gdm-login-vm`.
- [ ] `Tails`: plan items 1.x/2.x — the `cinnamon-rocky-defaults` RPM (wallpaper + branding),
      spec fixes, install-set + `run-tests.sh` EXPECTED-list updates, Cinnamon-Settings-menu fix.
- [ ] `Big`: plan items 3.x — fresh-VM end-to-end + the parity comparison run vs
      `fedora-cinnamon-ref`; record in `## Test Results`.
- [ ] `Shadow` → `Omega` → `Big`: review chain on the diff.
- [ ] `Tails`: fix anything the chain returns.
- [ ] `Vector`: update `INSTALL.md`/`README.md` for the complete set (resume TASK-0016's doc work here).
- [ ] `Knuckles`: PR to main, merge.

---

## Plan

*Owner: `Amy`. Written 2026-09-15. Facts below were verified this session by reading upstream
sources (webfetch of `linuxmint/cinnamon` 6.7.4-unstable, `linuxmint/cinnamon-settings-daemon`
master, `rocky-linux/rocky-logos` r10) and the local repo at `main` `c1de933`. Anything not
verified here is an assumption, each with the command that settles it. Updated 2026-09-15 to
reflect the item 0.1 verdicts (Big, `## Test Results` 2026-09-15 entry): A1 FAIL made the terminal
decision concrete (1-pager in `planning/decisions/TASK-0017-terminal-choice.md`), A2 refined to a
`picture-uri`-only wallpaper override, A5 settled to icon-theme entry plus compiled gschema
override (the Fedora baseline pattern), and the two environment repairs (host repo file baseurl,
ref repair-boot trap) are now explicit prerequisites.*

**Why this task exists** — the DoD (user 2026-09-14): the Rocky 10 Cinnamon desktop must be a
complete 6.7 desktop, not a partial one. Full subpackage set, a terminal, Rocky wallpaper set
automatically on first login, Rocky branding in the panel, working applets/themes/extension
manager/Cinnamon Settings menu, nemo regression check, end-to-end on a VM on host
`192.168.1.102` only, and a documented feature-parity comparison against `fedora-cinnamon-ref`.

**What it unblocks** — a shippable, documented desktop set (TASK-0016's doc work depends on the
final set); later session/wayland/packaging work builds on a verified complete baseline.
**What blocks it** — nothing external. All inputs are local (this repo, the VMs on 102) or
reachable via webfetch. No dependency on other repos or tasks.

**MVP** — the RPM set (including the new `cinnamon-rocky-defaults` and `gnome-terminal` RPMs, the
latter source-built per the 2026-09-15 decision) plus the system package `rocky-logos`, that make
a fresh minimal Rocky 10.2 VM log in via GDM (Cinnamon Wayland) into a working session: terminal
opens, Rocky wallpaper set, Rocky logo on the menu button, applets loaded, Cinnamon Settings menu
present. Deferred: filling the 8 empty
nemo subpackage RPMs (packaging defect, handled as a check, not a feature), wayland session polish
beyond the default `wayland=true` build, `cinnamon-screensaver` as a separate package (folded into
`cinnamon` at 6.7, fact 7, no action).

**What this makes harder later.** The set gets pinned into `INSTALL.md` by Vector, so every later
addition is another doc round. The source-built gnome-terminal (decision 2026-09-15, A1 failed)
makes a later terminal switch a set-plus-spec-plus-docs change and adds one non-Cinnamon spec to
the repo's maintenance surface. The parity checklist becomes the de facto acceptance bar for
future sessions, so deviations should be recorded narrow and few.

**Verified facts** (source in parentheses):

1. **Wallpaper package is `rocky-logos`** (`rocky-linux/rocky-logos`, branch `r10`, GitHub tree
   listing). `backgrounds/` ships `rocky-default-10-*.{png,jpg,xml}` to `/usr/share/backgrounds/`
   plus `desktop-backgrounds-default.xml` and the gschema override
   `10_org.gnome.desktop.background.default.gschema.override`.
2. **Default wallpaper is Gemstone Skies.** The override sets `org.gnome.desktop.background
   picture-uri` to `file:///usr/share/backgrounds/rocky-default-10-gemstone-skies-time.xml`
   (day/night pair, `-day.png` / `-night.png`). (Read the override file.)
3. **That override targets the GNOME schema, not Cinnamon's.** `org.gnome.desktop.background`, not
   `org.cinnamon.desktop.background`, so `rocky-logos` alone does not set the wallpaper in a
   Cinnamon session. The Cinnamon background schema is not in `cinnamon-settings-daemon/data/`
   (plugin schemas only) nor in the shell's `files/usr/share/` (no glib-2.0 dir). Provider and keys
   are assumption A2.
4. **Default themes ship inside the `cinnamon` (shell) RPM.** `data/meson.build`
   (6.7.4-unstable): `install_subdir('theme', install_dir: pkgdatadir, ...)` →
   `/usr/share/cinnamon/theme/`. No separate theme component in the 6.7.4 tree;
   `linuxmint/cinnamon-themes` is archived (2018, superseded by `mint-themes`, Mint-specific).
5. **`wayland = true` by default** (`meson_options.txt`); the shell installs
   `cinnamon-wayland.session`; `spec/muffin.spec` builds `-Dwayland=true -Dnative_backend=true`
   (the README's "X11-only" wording is stale, flag for Vector).
6. **The shell RPM already covers applets, desklets, the settings UI, and menu entries.**
   Top-level `meson.build` (6.7.4-unstable): `install_subdir('js')` → `/usr/share/cinnamon/js`
   (34 applets, desklets, `cinnamon-settings/` incl. the extensions panel, all
   `cinnamon-settings-*.desktop` files incl. `cinnamon-settings-default.desktop` = the "Cinnamon
   Settings" menu entry, `desktop-directories/`, icons, polkit actions);
   `install_subdir('files', install_dir: '/', strip_directory: true)`. There is no `skeletons/`
   directory in the tree, the default panel layout is created in code (js/ui/) on first login. A
   missing menu/applet is therefore an RPM-content issue (A4) or a runtime issue (A3), not a
   missing skeleton package.
7. **Screensaver is folded into the `cinnamon` package at 6.7.** `debian/control`:
   `Breaks/Replaces: cinnamon-screensaver (<< 6.7)`; the tree ships `src/screensaver/` and
   `cinnamon-screensaver-command`. No separate screensaver RPM is needed.
8. **Our build flags diverge from upstream defaults.** `spec/cinnamon-settings-daemon.spec`:
   `-Duse_color/cups/smartcard/gudev/wacom/polkit/logind=disabled` (upstream builds these in,
   parity gap D2). `spec/xapps.spec`: `-Dapp-lib-only=true -Dstatus-notifier=disabled` (library
   only, no `xapp` binary). The shell spec does NOT pass Debian's
   `-Dexclude_info_settings` / `-Dexclude_users_settings`, so those panels are included
   (parity-positive).
9. **The harness exists and is mostly sound.** `vm-test/run-tests.sh` (copies `rpms/*.rpm`,
   installs `gsettings-desktop-schemas`, SELinux permissive, `dnf install -y *.rpm`, verifies the
   EXPECTED list) but `cinnamon-menus` is MISSING from its EXPECTED list (harness bug, item 1.1).
   `vm-test/first-boot-setup.sh` is a test-VM aid (root SSH, firewalld off), not a first-login
   wallpaper mechanism. `vm-test/fedora-cinnamon-ref-setup.md` documents the golden ref (Fedora 44,
   cinnamon 6.6.7, lightdm, 4 GiB / 4 vCPU q35, VNC 5901 via `ssh -L 5901:127.0.0.1:5901`,
   192.168.122.156, `@cinnamon-desktop` group plus gnome-terminal, 1531 packages).
10. **The repo is consistent at `main` `c1de933`:** 11 spec files (README says "10", INSTALL.md
    says "14", both stale, flag for Vector). `repo-setup/setup-repo.sh` publishes with
    createrepo_c; known pitfall: it skips metadata regeneration when `repodata/repomd.xml` exists,
    so delete `repodata/` before re-running after adding RPMs.
11. **Item 0.1 verdicts (Big, 2026-09-15, `## Test Results` 2026-09-15 entry).** A1 FAIL:
    gnome-terminal is in no Rocky 10 repo (AppStream/CRB/BaseOS/Extras) and not in EPEL; the only
    terminal packages are `xterm` (BaseOS) and `konsole` (EPEL). A2 PASS with refinement:
    `org.cinnamon.desktop.background` is present (owned by `cinnamon-desktop-6.7.2-1.el10`) and has
    `picture-uri` but **no** `picture-uri-dark`; `/etc/dconf/profile/user` contains
    `system-db:local`. A4 PASS: 34 applet dirs, 3 desklets, the settings desktops and both
    sessions ship in the installed shell RPM. A5 PASS: the menu button icon is the schema key
    `org.cinnamon app-menu-icon-name` (upstream default `cinnamon-symbolic`), resolved via
    `Gtk.IconTheme`; the Fedora baseline is a compiled gschema override
    (`10_cinnamon-common.gschema.override` in `cinnamon-6.6.7-7.fc44`), and the icon asset must be
    a real icon-theme entry, not a pixmap. Environment facts carried into the plan: all libvirt
    operations on 102 use `virsh -c qemu:///system`; host dnf needs `--assumeno` (a cloudsmith
    repo triggers an interactive GPG prompt); the host repo file
    `/etc/yum.repos.d/cinnamon-rocky10.repo` has a dead baseurl (R10); the ref VM's repair-boot
    triple was found re-armed (baseline-capture prerequisite).

**Discrepancies (surfaced, not resolved here)**

- **D1 — DoD "cinnamon-themes is present" vs reality.** The DoD themes item names a
  `cinnamon-themes` package, but default themes ship inside the `cinnamon` RPM from `data/theme/`
  (fact 4) and the standalone repo is archived/Mint-specific. The correct check is functional:
  theme files present under `/usr/share/cinnamon/theme/` in the installed `cinnamon` package,
  default theme applies, theme selector works. `Robotnik` should rewrite the DoD item to drop the
  package name and keep the functional check (I cannot edit the DoD).
- **D2 — settings-daemon is built with fewer features than upstream** (fact 8). If the parity run
  shows a feature the ref has that we lack (color management, media keys, ...), the fix is
  re-enabling the matching `-D` flag in `spec/cinnamon-settings-daemon.spec` and rebuilding, not a
  missing package. The parity run decides which flags matter.

**Assumptions (settled in item 0.1, 2026-09-15; A3 stays open until the 2.1 run)**

- **A1 — gnome-terminal is in the Rocky 10 repos: FAILED (0.1).** `dnf repoquery` over AppStream,
  CRB, BaseOS, Extras and EPEL found no gnome-terminal (only xterm, konsole). Decision made
  2026-09-15: source-build gnome-terminal in this repo (1-pager in
  `planning/decisions/TASK-0017-terminal-choice.md`), item 1.4, with the konsole (EPEL) / xterm
  (BaseOS) fallback inside that item if the EL10 dependency chain fails verification.
- **A2 — the Cinnamon background schema and keys: PASS with refinement (0.1).** The schema is
  `org.cinnamon.desktop.background`, present and owned by `cinnamon-desktop-6.7.2-1.el10`; the
  keys include `picture-uri` and there is **no `picture-uri-dark`**; the dconf override therefore
  targets `picture-uri` only (see Wallpaper below). `/etc/dconf/profile/user` has
  `system-db:local`, so the profile-branch of the wallpaper design is moot.
- **A3 — cjs 6.4.0 + mozjs115 115.29.0 suffices for the 6.7 applets/settings UI** (mozjs 140 is
  blocked by EL10 GLib 2.86, prior session decision). If applets or the settings UI fail at runtime
  with JS API errors, this is the first suspect. The full-set parity run is the test. *(open)*
- **A4 — the installed shell RPM contains the full `data/` tree: PASS (0.1).** 34 applet dirs,
  3 desklets, the `cinnamon-settings-*.desktop` files (incl. `cinnamon-settings-default.desktop`)
  and both sessions present in `cinnamon-6.7.4-1.el10`. The plan's "expect 34" counts dirs,
  verified exactly.
- **A5 — the menu button's icon is resolvable and overridable: PASS (0.1).** Mechanism is the
  schema key `org.cinnamon app-menu-icon-name`, icon-theme resolved (see Branding below); the
  Fedora baseline (compiled gschema override plus a theme-resolvable asset) is the pattern to
  follow. The DoD names `rocky-logos` as the logo source.

**Complete set (working list).** Current repo builds 11 specs: `cjs`, `mozjs115`, `muffin`,
`xapps`, `cinnamon-desktop`, `cinnamon-session`, `cinnamon-settings-daemon`,
`cinnamon-control-center`, `nemo` (plus subpackages), `cinnamon` (shell), `cinnamon-menus`. What a
full 6.7 desktop additionally needs, and where it comes from:

- **Terminal (missing):** `gnome-terminal` — A1 failed (0.1): in no Rocky 10 or EPEL repo. Now a
  new spec in this repo (source build, decision 2026-09-15, 1-pager in
  `planning/decisions/TASK-0017-terminal-choice.md`), built in item 1.4 and added to the
  documented install set.
- **Wallpaper (missing):** `rocky-logos` (Rocky AppStream repo) plus a first-login override, new
  package below. Added to the documented install set.
- **`cinnamon-menus`:** already in the repo, but missing from the harness EXPECTED list (item 1.1).
- **nemo subpackages:** 10 declared, only `-python` / `-devel` carry %files, so 8 would build as
  empty RPMs. Item 1.3 fills or drops them.
- **Everything else:** present. The shell RPM already covers applets/desklets/settings UI/menu
  entries/themes (facts 4, 6); screensaver is folded in (fact 7). No further monorepo subpackage is
  needed for the desktop.

The delta is therefore: 1 system package in the install set (`rocky-logos`), 2 new RPMs in this
repo (`cinnamon-rocky-defaults`, `gnome-terminal`), 1 nemo spec check, 1 harness fix, and the
parity run.

**Wallpaper: first-login mechanism (design).** A dconf system override, shipped in a new small RPM
`cinnamon-rocky-defaults` (new spec in this repo; no upstream spec divergence):

- Ship `/usr/share/dconf/db.local.d/readonly/10_cinnamon_rocky_wallpaper` setting `picture-uri`
  (only; the cinnamon schema has no `picture-uri-dark` key, A2 2026-09-15) to the Gemstone Skies
  day/night pair `file:///usr/share/backgrounds/rocky-default-10-gemstone-skies-time.xml` (fact 2)
  under `org.cinnamon.desktop.background` (A2 confirmed the schema present, owned by
  `cinnamon-desktop-6.7.2-1.el10`; the GNOME-schema fallback branch is retired with A2's pass).
- Semantics: a readonly system-db entry applies to every user at session start and is overridden
  the moment the user changes the wallpaper in Cinnamon Settings (user-db wins in the dconf
  profile chain). That is "set automatically on first login" without any first-login state
  tracking. `/etc/dconf/profile/user` must contain `system-db:local` (checked in A2); if it does
  not, the package ships the corrected profile and the decision is recorded in Implementation.
- The RPM's `%post`/`%postun` run `dconf update /usr/share/dconf/db.local` (or rely on the
  `dconf` package's existing triggers, whichever the VM shows is correct, decided in item 1.2;
  0.1 confirmed `/usr/share/dconf/db.local.d/` does not exist yet, so the new RPM creates it).
- `rocky-logos` provides the image files (fact 1); it joins the install set (item 1.4).

**Branding (design; mechanism settled by A5, 2026-09-15).** The menu button icon is not applet
config: `Menu._updateIconAndLabel()` reads the schema key `org.cinnamon app-menu-icon-name`
(upstream default `cinnamon-symbolic`, the Cinnamon logo currently shown on our VM) and resolves
it through a `Gtk.IconTheme` name lookup (`js/ui/applet.js:705`, 0.1 evidence). Fedora's baseline
does exactly this: `cinnamon-6.6.7-7.fc44` ships
`/usr/share/glib-2.0/schemas/10_cinnamon-common.gschema.override` setting
`app-menu-icon-name='fedora-logo-sprite'` and `system-icon='fedora-logo-sprite'`, compiled into
`gschemas.compiled`.

`cinnamon-rocky-defaults` follows the same pattern with two payloads:

- The Rocky logo as a real icon-theme entry, installed from the `rocky-logos` assets (exact source
  file confirmed in item 1.2 by `rpm -ql rocky-logos | grep -i logo`) as
  `/usr/share/icons/hicolor/scalable/apps/rocky-logo.svg`, icon name `rocky-logo`; the icon cache
  is refreshed in `%post` (or the distro's icon-theme trigger, whichever the VM shows, decided in
  item 1.2). 0.1's finding that the ref's pixmaps-only sprite is not theme-resolvable is why the
  asset must be a theme entry, not a pixmaps drop.
- A compiled gschema override:
  `/usr/share/glib-2.0/schemas/10_cinnamon_rocky_defaults.gschema.override` setting both
  `app-menu-icon-name` and `system-icon` to `rocky-logo`, compiled by `glib-compile-schemas` in
  `%post`/`%postun` (the RPM ships the override source; Fedora ships the compiled result, same end
  state).

No change to the shell RPM. The ref's own menu button most likely renders the missing-image
fallback (sprite not theme-resolvable, 0.1); the Rocky implementation is correct by construction.

**Terminal (decision, 2026-09-15; A1 failed).** gnome-terminal is in no Rocky 10 or EPEL repo
(0.1: only xterm/BaseOS and konsole/EPEL among terminal packages). Decision (1-pager:
`planning/decisions/TASK-0017-terminal-choice.md`): **source-build gnome-terminal as an RPM in
this repo**, like the other Cinnamon-stack packages, in item 1.4. It meets the DoD as written (the
DoD names gnome-terminal), matches the Fedora ref for the parity run, and keeps the install set
free of third-party repos. Contingency inside item 1.4: if the EL10 dependency-chain verification
(first turn, `dnf repoquery`; the chain includes gtk4 and VTE, names to be confirmed not guessed)
fails, fall back to konsole (EPEL) and record a deviation, xterm (BaseOS) if an EPEL dependency is
unacceptable. The DoD check "opens from the Cinnamon session" is verified in item 2.1 either way.

**Cinnamon Settings menu (diagnosis).** The menu entry is the `cinnamon-settings-default.desktop`
file plus `desktop-directories/`, both installed by the shell RPM (fact 6); the menu applet builds
the submenu from the installed `.desktop` files at runtime. A4 (0.1) eliminated the RPM-content
explanation: `cinnamon-settings-default.desktop` is present in the installed shell RPM (33
`cinnamon-settings-*.desktop` files verified). The remaining suspicion is runtime: the file is
present but the menu does not render the submenu (cjs 6.4.0 runtime issue, A3 still open, or
missing desktop-database registration in `%post`) → check the session log in item 2.1, fix per
evidence.

The DoD item is then verified in item 2.1: "Cinnamon Settings" present in the main menu and opens
control-center.

**Parity design vs `fedora-cinnamon-ref`.**

*Baseline capture (one-time, item 0.3).* **Repair-trap re-check first (added 2026-09-15):**
`virsh -c qemu:///system dumpxml fedora-cinnamon-ref` must contain no `<kernel>`, `<initrd>`, or
`<cmdline>` line; the triple was found re-armed on 2026-09-15 (0.1) despite TASK-0018's removal
record, so this check runs before every start of the ref, not just baseline capture. If present:
`virsh destroy`, edit the XML to remove the three lines, `virsh define`, re-check clean, then start
(the 0.1 repair procedure). Then boot the ref on 102 (defined; VNC 5901 via
`ssh -L 5901:127.0.0.1:5901 howard@192.168.1.102`), log in, and run a new read-only inventory
script `vm-test/parity/parity-inventory.sh` (item 0.2) that collects: `rpm -qa | grep -i
cinnamon`; the installed applet instances (panel screenshot plus the applet registry under
`~/.config/cinnamon/applets/`); theme names via gsettings (both cinnamon and gnome interface
schemas, whatever A2 shows exist); `ls /usr/share/cinnamon/theme`; extension manager open with the
shipped extensions listed (screenshot); screensaver state (service plus
`cinnamon-screensaver-command --version`, noting the ref is 6.6.7 where screensaver is still a
separate package); main menu with the Cinnamon Settings submenu (screenshot); nemo open
(screenshot plus `nemo --version`); terminal open (screenshot plus `gnome-terminal --version`);
panel power menu (screenshot); session controls in Cinnamon Settings (screenshot);
`ls /usr/share/backgrounds`; and the dconf background values. Output plus screenshots land in
`vm-test/parity/fedora-ref/`. The ref is used read-only; it is never modified.

*Checklist (the parity matrix, filled in item 2.2).* Rows = the DoD minimum set (panel applets,
themes, extension/applet/desklet manager, screensaver, Cinnamon Settings, main menu, nemo,
terminal, session/power controls) plus wallpaper and branding rows. Columns = Fedora ref (expected,
from the baseline), our Rocky VM (actual), status (PASS/FAIL/deviation plus reason). Every FAIL is
either closed in this task (item 3.1) or recorded in `## Status` as a deviation with the reason,
exactly as the DoD allows. Known accepted deviations to record up front: the ref uses lightdm and
6.6.7 while we use GDM and 6.7.x (DoD mandates GDM login; parity is on desktop features, not
package versions or display managers).

*Run procedure (item 2.1 plus 2.2).* Fresh minimal Rocky 10.2 VM on 102 via the existing harness
(`vm-test/provision-vm.sh`, `vm-test/run-tests.sh`), install the complete set including
`cinnamon-rocky-defaults`, `rocky-logos`, and gnome-terminal, log in via GDM (Cinnamon Wayland),
verify each DoD item with VNC evidence (item 2.1), then run the same inventory script and save to
`vm-test/parity/rocky10/` (item 2.2). One VM does both; the VM is disposable.

**Work breakdown.** One agent, one item, one turn. The endpoint runs `--parallel 1`, so dispatch is
strictly sequential; "Parallel with" marks items whose order along the critical path is free, not
items that run concurrently.

| # | Item | Owner agent | Acceptance criterion | Parallel with |
|---|---|---|---|---|
| 0.1 | Environment verification on 102: boot `fedora-cinnamon-ref`, confirm/create the Rocky test VM; run A1, A2, A4, A5 checks (exact commands in the Assumptions list) and the ref-side logo/icon inspection | `Big` | Each of A1, A2, A4, A5 has a recorded answer with command output in `## Test Results` (done 2026-09-15); ref booted to a Cinnamon session | none, first item |
| 0.2 | Write `vm-test/parity/parity-inventory.sh` (read-only inventory, no state changes, schema names from 0.1) | `Big` | Script runs on a Cinnamon VM and emits a structured report covering every checklist row plus screenshots | independent of 1.x (different files); ordered after 0.1 for the A2 schema names |
| 0.3 | Capture the Fedora ref baseline: **repair-trap re-check first (no `<kernel>`/`<initrd>`/`<cmdline>` in the persistent XML; added 2026-09-15)**, then boot ref, log in, run 0.2, save to `vm-test/parity/fedora-ref/` | `Big` | Trap check clean and recorded; baseline files exist for every checklist row with screenshot plus inventory evidence | ordered after 0.1 and 0.2; off the critical path |
| 1.1 | Fix `vm-test/run-tests.sh` EXPECTED list (add `cinnamon-menus`, reconcile against the published set) | `Big` | EXPECTED matches the published RPM set; script passes on the current set | independent of 0.x and 1.2-1.4, order free |
| 1.2 | **Prerequisite (host, first step, added 2026-09-15):** fix the dead baseurl in `/etc/yum.repos.d/cinnamon-rocky10.repo` (currently `file:///home/howard/cinnamon_test/cinnamon-for-rocky10/rpms`, a nonexistent path; the project lives at `/home/howard/Linux/projects/cinnamon-for-rocky10`) to point at the real `rpms/` dir, then verify `dnf` resolves the repo (host dnf needs `--assumeno`: the cloudsmith repo triggers an interactive GPG prompt). Then: build `cinnamon-rocky-defaults` (new spec): wallpaper dconf override (`org.cinnamon.desktop.background`, `picture-uri` only, A2) and the branding pair (icon-theme entry plus gschema override, A5/Fedora pattern); add to the build and re-publish the repo (delete `repodata/` first) | `Tails` | Repo file fixed and resolving; RPM builds; files land at the verified paths; `dnf` on a test VM resolves the new package | ordered after 0.1 |
| 1.3 | nemo subpackage %files audit: fill or drop the 8 empty subpackage declarations | `Tails` | Build produces zero empty RPMs; nemo main package unchanged | independent of 1.2 (different spec), order free |
| 1.4 | Terminal per the 2026-09-15 decision: verify the EL10 dependency chain with `dnf repoquery` (first turn, before writing the spec), then build `gnome-terminal` from source (new spec in this repo); add it and `rocky-logos` to the documented install set and to the harness install list (docs themselves are Vector's item 3.2) | `Tails` | gnome-terminal RPM builds on the host and opens from the Cinnamon session on the test VM (verified in 2.1); the set list in this doc and `run-tests.sh` install both packages; if the dependency chain fails, the konsole (EPEL) fallback is taken and the deviation recorded | independent of 1.2 and 1.3 (disjoint specs), order free |
| 2.1 | Full end-to-end on a fresh minimal VM: install complete set, GDM Cinnamon Wayland login, verify every DoD item (first-login wallpaper, branding, applets, Settings menu, nemo, terminal) with VNC evidence | `Big` | Every DoD item recorded PASS/FAIL with screenshot or command evidence in `## Test Results` | ordered after 1.2, 1.3, 1.4 |
| 2.2 | Parity run: run the inventory on the same VM, save to `vm-test/parity/rocky10/`, fill the checklist, list the gaps | `Big` | Checklist complete for every row with both sides and evidence; gaps listed | ordered after 2.1 (same VM) |
| 3.1 | Close the gaps found in 2.1/2.2 that are fixable here (spec fixes, D2 flags, branding path) | `Tails` | Each fixed gap re-verified by the matching 2.1/2.2 check | ordered after 2.2 |
| 3.2 | Update `INSTALL.md` / `README.md` for the final set (resume TASK-0016 doc work; includes the stale package counts and the X11-only wording, facts 5, 10) | `Vector` | Docs describe the final set including the new packages and the parity deviations | ordered after 3.1 |
| 4.1 | Review chain on the diff: `Shadow`, then `Omega`, then `Big` | `Shadow`, `Omega`, `Big` | No unresolved blockers or findings above `low` | ordered after 3.2 |
| 4.2 | Fix anything the chain returns | `Tails` | Chain findings resolved, re-verified | ordered after 4.1 |
| 4.3 | PR to `metalllinux/cinnamon-for-rocky10` main, merge | `Knuckles` | Merged PR | ordered after 4.2 |

**Dependencies and sequence.** Genuinely ordered: 0.1 before 1.2 (mechanism evidence; 1.2's host
repo-file baseurl fix is a first step inside 1.2, not a separate item), 0.1 and 0.2 before 0.3 and
2.2 (inventory script plus baseline; 0.3 opens with the ref repair-trap re-check, added
2026-09-15), 1.2/1.3/1.4 before 2.1 (nothing to install otherwise), 2.1 before 2.2 (same VM),
2.2 before 3.1 (gaps define the fixes), 3.1 before 3.2 (docs describe the final set), 3.2 before
4.1 (review the final diff), 4.1 before 4.2, 4.2 before 4.3. Only looks ordered: 1.1, 1.3, 1.4
relative to each other and to 0.x (disjoint files and specs, any order works; 1.4 now carries the
gnome-terminal spec build per the 2026-09-15 decision but stays independent of 1.2/1.3); 0.3
relative to 1.x (the baseline does not need our build).

**Critical path:** 0.1 → 1.2 → 2.1 → 2.2 → 3.1 → 3.2 → 4.1 → 4.2 → 4.3. Off-path: 0.2 and 0.3
(needed by 2.2 but can be slotted anywhere after 0.1), 1.1, 1.3, 1.4.

**Estimates** (dispatch turns, three-point `T = (O + 4M + P) / 6`, rounded up): 0.1 = (1,2,4) → 2
(spent 2026-09-15); 0.2 = (1,2,3) → 2; 0.3 = (1,2,3) → 2 (the trap re-check added 2026-09-15 is a
grep on the XML, no estimate change); 1.1 = (1,1,2) → 1; 1.2 = (1,2,4) → 2 (the host repo-file
fix is a one-line edit, absorbed); 1.3 = (1,1,3) → 1; 1.4 = (2,4,8) → 5 (gnome-terminal source
build per the 2026-09-15 decision; was 1); 2.1 = (2,4,8) → 5; 2.2 = (1,2,4) → 3; 3.1 = (1,3,6) →
3; 3.2 = (1,2,3) → 2; 4.1 = (2,4,8) → 5; 4.2 = (1,2,4) → 2; 4.3 = (1,1,2) → 1. Total = 36 turns;
plus 30 percent buffer for the open-ended parts (3.1 scope is unknown until 2.2; the
gnome-terminal build is new territory on EL10). **Budget: 47 dispatch turns (2 consumed by 0.1;
45 remaining).**

**Risks.**

| # | Risk | Likelihood | Impact | Mitigation | Contingency |
|---|---|---|---|---|---|
| R1 | **Resolved 2026-09-15 (A2 PASS).** `org.cinnamon.desktop.background` confirmed present (owned by `cinnamon-desktop-6.7.2-1.el10`) with a `picture-uri` key; the wallpaper override targets it, `picture-uri` only | — | — | 0.1 evidence gates 1.2 | — |
| R2 | **Resolved 2026-09-15 (A1 FAIL), decision made.** gnome-terminal is in no Rocky 10 or EPEL repo; the plan's fallback was replaced by the source-build decision (1-pager in `planning/decisions/TASK-0017-terminal-choice.md`). Residual risk moved to R9 | — | — | Decision 2026-09-15; dependency verification is the first turn of 1.4 | See R9 |
| R3 | **Resolved 2026-09-15 (A5 PASS).** The menu icon is the schema key `org.cinnamon app-menu-icon-name`, icon-theme resolved; the Fedora compiled-override baseline is the pattern (see Branding) | — | — | 0.1 evidence gates 1.2 | — |
| R4 | cjs 6.4.0 / mozjs115 runtime incompatibility breaks 6.7 applets or the settings UI (A3, still open) | medium | high | Full-set run 2.1 surfaces it with session logs; cjs stays 6.4.0 because mozjs 140 is blocked by EL10 GLib 2.86 (prior decision) | Escalate as a recorded deviation or scope split; do not silently bump mozjs |
| R5 | Parity gaps are larger than expected (D2 disabled features, xapps app-lib-only) | medium | medium | D2 decision rule: re-enable a flag only when the parity run shows a user-visible gap | Record the remaining gaps as deviations in `## Status` with the reason, as the DoD allows |
| R6 | Test-VM provisioning on 102 fails (disk, network, libvirt state) | low | medium | Existing harness is proven by earlier runs; `rocky10-explore` (VNC 5902) exists as a fallback; if that fallback activates, run the same repair-trap re-check on its XML first (unchecked as of 0.1) | Reuse the existing VM instead of a fresh install; record which VM was used |
| R7 | `setup-repo.sh` skips repodata regeneration and dnf cannot see the new RPMs | high (known pitfall) | low | Runbook for 1.2 deletes `repodata/` before re-running | Run `createrepo_c` directly on the repo dir |
| R8 | A 32,000-token turn cap truncates a large dispatch (AGENTS.md section 14) | medium | medium | Every work item is sized to one turn; inventory script is small and focused | An empty subagent result means check `~/.local/share/opencode/opencode.db` for `finish: "length"` and re-dispatch with a smaller brief |
| R9 | gnome-terminal's EL10 dependency chain (gtk4, VTE; names to be confirmed by `dnf repoquery`, not guessed) is incomplete, so the source build fails | low-medium | high (DoD names it) | Item 1.4 verifies the chain before writing the spec (decision 2026-09-15) | Fall back to konsole (EPEL) as the terminal and record the deviation; xterm (baseos) if an EPEL dependency is unacceptable |
| R10 | The host repo file `/etc/yum.repos.d/cinnamon-rocky10.repo` has a dead baseurl (0.1 fact), blocking dnf resolution of the republished repo | certain until fixed (known) | medium (blocks 1.2 and the 2.1 dnf checks) | 1.2's first step fixes the baseurl to the real project path and verifies resolution | Rename the repo file out of `/etc/yum.repos.d/` on the host, or feed the repo to the test VM via `--repofrompath` |

**Validation.** How we know it worked, all on host `192.168.1.102` VMs only:

- **Fresh-VM end-to-end (item 2.1):** `dnf list installed` shows the complete set plus
  `cinnamon-rocky-defaults`, `rocky-logos`, and the gnome-terminal RPM from this repo (decision
  2026-09-15); GDM login offers and starts the Cinnamon Wayland session; first login shows the
  Gemstone Skies wallpaper (VNC screenshot, DoD "no black wallpaper"); the menu button shows the
  Rocky logo (screenshot); the panel applet list has no missing/erroring entries (session log plus
  screenshot); the main menu contains the "Cinnamon Settings" submenu and it opens control-center
  (screenshot); the extension manager lists the shipped extensions/applets/desklets (screenshot);
  nemo opens (screenshot); the terminal opens from the session (screenshot).
- **Parity (item 2.2):** the checklist is filled for every row with both sides and evidence,
  baseline in `vm-test/parity/fedora-ref/`, ours in `vm-test/parity/rocky10/`; every gap closed or
  recorded as a deviation.
- **Repo level:** the published repo resolves the new packages (R7 check, after the R10 baseurl
  fix), `run-tests.sh` EXPECTED passes with `cinnamon-menus` in the list, and the build produces
  zero empty RPMs (1.3).
- **Records:** `## Test Results` carries the verdicts and evidence; `## Status` carries the
  deviations; `## Docs` carries the doc changes.

**Rollback.** Detection: any harness FAIL, any 2.1 DoD-item FAIL, an rpmbuild error, or dnf
failing to resolve the new packages (R7/R10 symptom). Revert: the repo changes are additive files
(two new specs, the nemo spec, harness edits, docs, parity artifacts), so the exact revert is a
`git revert` of the PR commits, or simply not merging until item 4.3. The one host change is the
baseurl line in `/etc/yum.repos.d/cinnamon-rocky10.repo`; revert is restoring the old line or
deleting the file (it pointed at a dead path anyway). The published repo on the host is restored
by deleting the added RPMs and re-running `setup-repo.sh` after removing `repodata/`. The test VMs
are disposable (destroy); `fedora-cinnamon-ref` is used read-only and is never modified, so it is
unaffected. **Point of no return: none.** Nothing in this plan modifies the ref VM or anything
outside the repo, the disposable test VMs, and the one-line host repo file (reversible as above);
the only state that survives a revert is the published repo dir (fixed by re-publish) and the
recorded deviations (docs, intentionally kept).

---

## Implementation

*Owner: `Tails`.*

**Item 1.2 (done 2026-09-15, commit `a971031` on `feature/TASK-0017-cinnamon-desktop-completeness`).**
Scope per the plan table row 1.2 plus the Wallpaper/Branding design sections: (a) fix the dead host
baseurl in `/etc/yum.repos.d/cinnamon-rocky10.repo` and verify dnf resolves it, (b) write and build
a new spec `cinnamon-rocky-defaults` carrying the wallpaper dconf override
(`org.cinnamon.desktop.background` `picture-uri` only, A2) and the branding pair (gschema override
pointing at the installed `fedora-logo-icon` hicolor entry, no new icon file, deviation recorded
below), (c) add the RPM to the published repo (delete `repodata/` first, per R7) and verify dnf on
the test VM resolves the new package. All four acceptance criteria met (baseurl fixed and resolving;
RPM builds; files land at verified paths, verified live on the VM; VM dnf resolves the package).
Two forced deviations from the plan, both with evidence below: the dconf override path and the icon
asset/name. One cross-item correction: the wallpaper files are owned by `rocky-backgrounds`, not
`rocky-logos` (plan "fact 1" is wrong; affects item 1.4's install set).
Work branch: `feature/TASK-0017-cinnamon-desktop-completeness`, cut from `main` `c1de933`
(the plan does not name the branch inline; the team house pattern per Knuckles' agent rules is
`feature/TASK-XXXX-slug`).

### Problem: which icon asset from `rocky-logos` becomes the menu button icon, and how does GTK resolve it
*(facts verified 2026-09-15 on host 192.168.1.102, same OS as the test VMs)*
**Option A — reference the installed `fedora-logo-icon` hicolor entry (chosen).** How: the gschema
override sets `app-menu-icon-name='fedora-logo-icon'` and `system-icon='fedora-logo-icon'`; the RPM
ships no icon file; `Requires: rocky-logos`. Pros: zero redistribution of logo bytes, so the
rocky-logos `COPYING` trademark clause ("grants the right to use the Package only during the normal
operation of software programs that call upon the Package. No other copyright or trademark license
granted herein") is not engaged; the asset is already on the target system and theme-resolvable via
the hicolor fallback theme. Cons: the icon name is the legacy Fedora-era name, not `rocky-logo`.
**Option B — install `/usr/share/icons/hicolor/scalable/apps/rocky-logo.svg` copied from the
rocky-logos SVG (the plan's literal wording).** How: copy the SVG from `rocky-logos` into the hicolor
theme as `rocky-logo.svg`. Pros: matches the plan wording; clean icon name. Cons: (1) redistributes
logo bytes that the package-level trademark license does not grant for that use; the repo's
`CC-BY-SA-4.0` file licenses the artwork, but the package `COPYING` text is the conservative
governing reading; (2) the only SVG shipped by rocky-logos,
`/usr/share/rocky-logos/fedora_logo.svg`, is the 907x415 "Rocky" wordmark lockup, the wrong asset
shape for a square menu button (the Fedora pattern uses the square mark); (3) the square mark is
already installed and theme-resolvable.
**Chosen: Option A**, because the installed entry is provably the Rocky logo and referencing it
redistributes nothing. Evidence it is the Rocky gem mark and not the Fedora F: (1) upstream source
`icons/hicolor/scalable/apps/fedora-logo-icon.svg` on the `r10` branch is the two-path gem mark with
`fill="#10B981"` (fetched 2026-09-15 from raw.githubusercontent.com/rocky-linux/rocky-logos); (2) the
installed 256x256 PNG's average color over opaque pixels is (16,184,128) = #10B880, i.e. Rocky green
#10B981 (measured 2026-09-15 with a stdlib Python PNG decoder; the Fedora F is blue/purple). The name
`fedora-logo-icon` is a legacy from the fedora-logos fork; the Rocky team ships it unchanged
(`system-logo-icon` is the identical file, same sha256).
**Competing priorities:** a clean `rocky-logo` icon name (plan fidelity) vs. license safety (no
redistribution). Chose license safety; the name is a theme key invisible to users. If a cosmetic
`rocky-logo` name is ever wanted, the license-clean way is a separately authored asset, not a copy.

### Problem: where the wallpaper dconf override lives, and how the system db refreshes
**Option A — keyfile flat in `/etc/dconf/db/local.d/` + explicit `dconf update` in `%post`/`%postun` (chosen).**
How: ship `/etc/dconf/db/local.d/10_cinnamon_rocky_wallpaper`; scriptlets run `dconf update`
(default DBDIR `/etc/dconf/db`) and `glib-compile-schemas /usr/share/glib-2.0/schemas`;
`Requires: dconf` for the binary at install time. Pros: the documented and source-verified location
for `system-db:local` keyfiles; the refresh is explicit and testable. Cons: a scriptlet and one
extra `Requires`.
**Option B — the plan's path `/usr/share/dconf/db.local.d/readonly/` + `dconf update /usr/share/dconf/db.local`.**
How: ship the keyfile under `/usr/share/dconf/db.local.d/readonly/`, scriptlets run the plan's
invocation. Pros: matches the plan wording; world-readable location. Cons: the path is dead on
dconf 0.40, see evidence below.
**Chosen: Option A**, because dconf 0.40 (the exact EL10 version, `dconf-0.40.0-17.el10`,
`rpm -q dconf`) does not read the plan's path at all. Evidence, all from the 0.40.0 source
(fetched 2026-09-15) plus a live host test: (1) runtime source
`engine/dconf-engine-source-system.c:50`: `filename = g_build_filename (SYSCONFDIR "/dconf/db",
source->name, NULL)` — `system-db:local` resolves only to `/etc/dconf/db/local`; nothing under
`/usr/share/dconf/` is ever read; (2) `bin/dconf.c` `list_directory()` (lines 647-688) enumerates
flat regular files directly under `<db>.d/` only — no subdirectory recursion, `locks/` is the only
special-cased subdir — so even a `readonly/` subdir is not scanned; (3) live A/B test on the host
(temporary keyfiles, fully cleaned up and final state verified): keyfile flat in
`/etc/dconf/db/local.d/` → compiled db grew 104→330 bytes and `dconf read
/org/cinnamon/desktop/background/primary-color` returned the override value `'#10B981'`; keyfile in
the `readonly/` subdir → db stayed 104 bytes, no value; keyfile in the plan's path with the plan's
exact invocation `dconf update /usr/share/dconf/db.local` → `error: Error opening directory
"/usr/share/dconf/db.local"`, and no effect on the effective value. Also: `rpm -q --qf
'%{triggerspost}\n' dconf` is an unknown tag on this rpm, so the dconf package trigger could not be
inspected; the explicit scriptlet call is the safe mechanism regardless of triggers.
**Competing priorities:** plan path fidelity vs. a path that actually works on dconf 0.40. Chose the
working path; both deviations (top-level dir and no `readonly/` subdir) are forced by the dconf
source, not preference. The semantics the plan wanted (system-wide, user-overridable, no first-login
state) are preserved exactly: `/etc/dconf/profile/user` contains `system-db:local` (checked A2), so
the override applies at every user's session start until the user changes the wallpaper in Cinnamon
Settings (user-db wins in the profile chain).

**Cross-item correction (affects 1.4 install set).** The wallpaper files
(`/usr/share/backgrounds/rocky-default-10-gemstone-skies-time.xml` + the day/night PNGs) are owned
by `rocky-backgrounds-100.5-3.el10.noarch`, not `rocky-logos` as plan "fact 1" states (verified with
`rpm -qf` on the host). The install set needs **both** `rocky-backgrounds` and `rocky-logos`; the new
RPM `Requires:` both, so a plain `dnf install cinnamon-rocky-defaults` pulls them in automatically
(verified on the VM, which pulled `rocky-backgrounds` from the Rocky AppStream repo).

**Changes**

| File | What changed |
|---|---|
| `/etc/yum.repos.d/cinnamon-rocky10.repo` (host, outside the repo) | Line 3 baseurl `file:///home/howard/cinnamon_test/cinnamon-for-rocky10/rpms` (nonexistent) → `file:///home/howard/Linux/projects/cinnamon-for-rocky10/rpms`; verified resolving with `dnf --assumeno makecache --disablerepo='*' --enablerepo=cinnamon-rocky10` |
| `spec/cinnamon-rocky-defaults.spec` (new, commit `a971031`) | New noarch spec. Two config files written inline in the install section (house `.gitignore` keeps source tarballs out of git and the package has no upstream tarball, so the spec is the single source of truth). `%post`/`%postun` run `dconf update` + `glib-compile-schemas /usr/share/glib-2.0/schemas`. `Requires: dconf glib2 cinnamon cinnamon-desktop rocky-backgrounds rocky-logos` (each verified as the owner of a binary or file the package needs at install or runtime) |
| `rpms/cinnamon-rocky-defaults-1.0-1.el10.noarch.rpm` (new, commit `a971031`) | Payload is exactly two files: the dconf keyfile and the gschema override |
| `rpms/repodata/` (regenerated) | Deleted, then `createrepo_c rpms/` per the plan's re-publish procedure; 49 RPMs in the published set |

**Checks run**

- rpmbuild: `rpmbuild -ba spec/cinnamon-rocky-defaults.spec` → Wrote SRPM +
  `cinnamon-rocky-defaults-1.0-1.el10.noarch.rpm`. One build failure during development: the first
  inline-spec build died with `error: line 35: second %install` because a header comment contained
  the literal text `%install` and rpmbuild macro-expands inside comments; fixed by rewording the
  comment, rebuild clean.
- RPM inspection: `rpm -qpl` → exactly the two files at the verified paths
  (`/etc/dconf/db/local.d/10_cinnamon_rocky_wallpaper`,
  `/usr/share/glib-2.0/schemas/10_cinnamon_rocky_branding.gschema.override`); `rpm -qp --scripts` →
  post/postun as designed; `rpm -qpR` → the six `Requires` above.
- Payload: `rpm2cpio | diff -r` between the first (tarball) build and the final (inline) build →
  byte-identical, so the VM verification performed against the first build applies to the published
  RPM.
- Host dnf: after the baseurl fix, `dnf --assumeno makecache --disablerepo='*' --enablerepo=cinnamon-rocky10`
  → "Metadata cache created"; `dnf --assumeno repoquery ... cinnamon-rocky-defaults` →
  `cinnamon-rocky-defaults-0:1.0-1.el10.noarch`.
- Test VM (`gdm-login-vm`, 192.168.122.15, root SSH per the harness key): `rpms/` + `repo-setup/`
  scp'd to `/root/`, `bash /root/repo-setup/setup-repo.sh /root` → OK, `dnf repoquery` resolves the
  package; `dnf -y install cinnamon-rocky-defaults` → installed, auto-pulled
  `rocky-backgrounds-100.5-3.el10.noarch`; post-install: `dconf read /org/cinnamon/desktop/background/picture-uri`
  → `'file:///usr/share/backgrounds/rocky-default-10-gemstone-skies-time.xml'`,
  `gsettings get org.cinnamon app-menu-icon-name` and `system-icon` → `'fedora-logo-icon'`;
  `rpm -e` → override gone (dconf read empty, `app-menu-icon-name` back to schema default
  `'cinnamon-symbolic'`); reinstall → restored. The glib-compile-schemas deprecation warnings for
  `org.gnome.system.proxy*` during install are pre-existing on the base system, unrelated to this
  package.
- Host dconf A/B test cleanup verified: after removing all temporary keyfiles and re-running
  `dconf update`, `/etc/dconf/db/local` is back to 104 bytes (empty db), no test files remain under
  `/etc/dconf/db/local.d/` or `/usr/share/dconf/`, and `picture-uri` is back to the schema default
  value.

**Not yet done (outside 1.2 scope):** visual confirmation that the menu button and the wallpaper
render correctly in a logged-in Cinnamon session (item 2.1, `Big`, with VNC evidence); `rocky-logos`
and `rocky-backgrounds` in the documented install set and the harness install list (item 1.4, Tails,
then 3.2 Vector for the docs).

### Item 2.1 wallpaper-render FAIL: the reference A/B (defect vs environment limitation), 2026-09-16

**Question.** `gdm-login-vm` (Rocky 10) composites the Cinnamon panel but the nemo-desktop Wayland
surface is 100% black (Big 2.1, B5/B6). Open question in `## Status`: defect in our RPM set vs
environment limitation of the virtio-vga + Wayland path. This entry settles it.

**Method (disposable overlay; pristine golden never touched).** qcow2 overlay
`/home/howard/vm-disks/fedora-cinnamon-ref-task0017-overlay.qcow2` backed by the pristine
`/home/howard/vm-disks/fedora-cinnamon-ref.qcow2` (Fedora 44, Cinnamon 6.6.7); domain
`ref-overlay-task0017`, MAC `52:54:00:7f:23:ae`, DHCP `192.168.122.85`. All changes live only in the
overlay. To give the reference a logged-in Cinnamon session (the piece missing from Big 2.1's B7): the
overlay runs GDM (the golden ships lightdm, plan fact 9) with a GDM auto-login config
(`/etc/gdm/custom.conf` `[daemon] AutomaticLoginEnable=True / AutomaticLogin=howard`; original backed
up to `/root/custom.conf.bak-task0017`), and `sshd` is enabled. Two overlay-side obstacles fixed
before the session would start, both recorded: (1) the reference's re-armed repair-boot trap, repaired
per Big 0.1; (2) `/etc/shadow` had lost its SELinux label (`unlabeled_t`) because `chpasswd` ran in an
`init=/bin/bash` shell with SELinux disabled, so PAM/GDM accounting failed and no session started
(AVC denials for `unix_chkpwd` / `systemd-userdbd` / `accounts-daemon` reading `shadow`); fixed with
`chcon system_u:object_r:shadow_t:s0 /etc/shadow`.

**Forcing the exact path under test.** The reference has both Cinnamon and GNOME installed. GDM
auto-login first picked GNOME (gnome-shell / mutter) — the wrong compositor for this A/B. Our VM runs
**Cinnamon Wayland (muffin)** and B5 is specifically the nemo-desktop **Wayland** surface, so the
reference must run Cinnamon Wayland. On the overlay, `mv`'d `/usr/share/wayland-sessions/gnome.desktop`
and both `/usr/share/xsessions/cinnamon*.desktop` to `/root/*.bak-task0017`, leaving
`cinnamon-wayland.desktop` (`Exec=cinnamon-session-cinnamon --wayland`) as the only session. (A first
reboot without removing the X sessions gave Cinnamon **X11** — `gdm-x-session` / `Xorg` /
`cinnamon --x11` — which also rendered non-black, but that is not the surface under test.)

**Result: the reference renders the Cinnamon Wayland desktop (2026-09-16).**
- `virsh screenshot` → `/tmp/opencode/ref-cinnamon-wayland.png`: **100% non-black**, a blue gradient
  wallpaper (top colors (0,64,192) / (0,64,160) / (0,96,192) / (0,32,160) / (0,32,128)) — a real
  wallpaper image (multi-shade gradient), not a solid compositor fallback.
- Session processes (user howard): `gdm-wayland-session --handle-registration
  cinnamon-session-cinnamon --wayland` → `cinnamon-session-binary --session cinnamon-wayland` →
  `/usr/bin/cinnamon --replace` (compositor backend **muffin**, confirmed by its
  `Xwayland ... muffin-Xwaylandauth` child) → `/usr/bin/nemo-desktop`. `loginctl` → `Type=wayland`,
  `State=active`; `/run/user/1000/` holds the `wayland-0` socket and `.muffin-Xwaylandauth.*`.

**Verdict: defect in our RPM set, not an environment limitation.** Identical virtio-vga + Wayland
hardware composites a full non-black nemo-desktop wallpaper under the reference Cinnamon 6.6.7 Wayland
(muffin) session. The environment demonstrably can do it; our Rocky 10 build (Cinnamon 6.7.4-1.el10)
does not, so the black nemo-desktop surface is a defect in our stack. This closes Big 2.1's B7 caveat
("cannot be settled until the ref is put in a session").

**Confounds, handled.** (a) Reference is Fedora 44 / Cinnamon 6.6.7 vs our Rocky 10.2 / 6.7.4-1.el10;
the A/B isolates the *environment* (hardware + display path) — the reference proves that environment
composites the surface, so the difference is in the OS/RPM layer (our build), not the hardware. (b)
The reference session is Wayland (muffin), the same compositor path as our VM's nemo-desktop surface
(B5). (c) The rendered blue is a multi-shade image, so nemo-desktop is compositing a wallpaper, not
muffin's solid default.

**Next (root cause, still Tails).** Both VMs are now directly comparable: reference Cinnamon Wayland
healthy at `192.168.122.85`; our Rocky black at `192.168.122.15`. Big 2.1 already found our
nemo-desktop is "software-rendering (no DRM fd, libcairo only)" while the panel composites — that is
the first lead. Diagnosis next: compare the two nemo-desktop rendering paths, the muffin / Cinnamon
build flags (`-Dwayland`, `-Dnative_backend`), and the background dconf values; fix; re-verify via
Big 2.1.

### Item 2.1 wallpaper-render FAIL: root cause (Tails), 2026-09-16

**Root cause: our `nemo` RPM was built without the gtk-layer-shell Wayland backend, so
nemo-desktop forces the X11 backend even in a Wayland session, and the desktop background is
never composited by muffin.**

Evidence chain (all verified 2026-09-16):
1. Journal A/B (`journalctl _UID=1000`), both sessions are `cinnamon-wayland`
   (XDG_SESSION_TYPE=wayland, GDMSESSION=cinnamon-wayland, WAYLAND_DISPLAY=wayland-0):
   - Reference (nemo 6.6.3-3.fc44): `nemo-desktop: session is cinnamon, establishing proxy`
     (no "using X11").
   - Our Rocky (nemo 6.7.4-1.el10): `nemo-desktop: using X11` then
     `nemo-desktop: session is x11 cinnamon, establishing proxy`.
   - Only nemo env difference: reference has `XDG_SESSION_EXTRA_DEVICE_ACCESS=render:accel`,
     ours does not.
2. Setting the wallpaper to a plain PNG (`gsettings set ... picture-uri
   file:///usr/share/backgrounds/rocky-default-10-gemstone-skies-day.png`) + respawn did NOT
   change the black result (`analyze-shot.py` non-black 0.001). Rules out the GNOME `*-time.xml`
   slideshow content as the cause.
3. Source (linuxmint/nemo `src/nemo-desktop-main.c:121-134`): the Wayland backend is behind
   `#ifdef HAVE_GTK_LAYER_SHELL`. Our RPM logged the `#else` line ("using X11"), so
   `HAVE_GTK_LAYER_SHELL` was **not** defined at build time. That branch also calls
   `gdk_set_allowed_backends("x11")`, overriding any `GDK_BACKEND` env.
4. meson: `meson_options.txt:15` `option('gtk_layer_shell', type:'boolean', value:false, ...)`
   defaults **false**; `meson.build:142-146` only sets HAVE_GTK_LAYER_SHELL when the option is on
   and `dependency('gtk-layer-shell-0','>=0.8')` is found.
5. Spec `/home/howard/rpmbuild/SPECS/nemo.spec` (changelog 6.7.4-1 "Initial port to Rocky Linux
   10"): BuildRequires has no gtk-layer-shell-devel; `%build` `meson setup` (lines 56-61) passes
   `-Dxmp=false -Ddeprecated_warnings=false` but **no `-Dgtk_layer_shell=true`**. The port never
   enabled it.
6. `rpm -q gtk-layer-shell` on gdm-login-vm → not installed; `dnf list available
   gtk-layer-shell*` across appstream/baseos/crb/extras/epel/cinnamon-rocky10 → no match. It is not
   shipped for Rocky 10, so it must be built.

**Fix decision (Tails, in progress).** Rebuild nemo with the Wayland backend:
1. Build `gtk-layer-shell` from source (wmww/gtk-layer-shell, MIT) as a Rocky 10 RPM; add to the
   `cinnamon-rocky10` local repo.
2. Update the nemo spec: add `BuildRequires: gtk-layer-shell-devel` and runtime
   `Requires: gtk-layer-shell`; add `-Dgtk_layer_shell=true` to the `meson setup` line.
3. Rebuild the `nemo` RPM; add to the local repo.
4. Install `gtk-layer-shell` + the new `nemo` on gdm-login-vm; restart the cinnamon session or
   reboot.
5. Re-verify: nemo-desktop must log `using Wayland backend, gtk-layer-shell supported` (not
   "using X11") and the desktop renders non-black (Big 2.1 re-run).

**Alternatives rejected.** (a) `GDK_BACKEND=wayland` env — the `#else` path calls
`gdk_set_allowed_backends("x11")`, overriding the env; the backend is compiled in. (b) Patch
nemo-desktop to force Wayland without gtk-layer-shell — gtk-layer-shell IS the designed Wayland
backend (renders the background as a `zwlr_layer_shell` layer surface); that is the upstream
approach, and a patch would duplicate it. (c) Ship the reference Fedora nemo RPM — version mismatch
(6.6.3 vs 6.7.4) and not our build.

Note: multiple nemo spec/build locations exist on the host (`/home/howard/rpmbuild/SPECS/nemo.spec`,
`/home/howard/Linux/projects/cinnamon-for-rocky10/spec/nemo.spec`, build tree
`/home/howard/Linux/projects/cinnamon_4_rocky10/nemo/`). Confirm the authoritative build path before
rebuilding; the installed 6.7.4-1.el10 RPM's changelog matches the `rpmbuild/SPECS/nemo.spec` one.

### Item 2.1 wallpaper-render: final fix, gnome-bg image branch (Tails), 2026-09-17

**Status: FIXED and verified on first login.** The prior entry's nemo / gtk-layer-shell
prerequisite (nemo 6.7.4-2) was necessary but not sufficient: after that rebuild the desktop
still rendered black. The second and final root cause is in the shared `gnome-bg` image branch
of `libcinnamon-desktop`. The wallpaper is a photo, so the image branch runs; that branch built
its `cairo_surface_t` with `gdk_cairo_surface_create_from_pixbuf()`, and a pixbuf-derived surface
does not composite on the gtk-layer-shell / Wayland background window, leaving it black. The
solid-color branch was already correct, which is why a flat `primary-color` showed but the photo
did not.

**Root cause (verified 2026-09-17).**
1. The defect is in the shared library, so one fix covers both background renderers.
   `csd-background` calls `gnome_bg_create_and_set_gtk_image`
   (`cinnamon-settings-daemon/plugins/background/csd-background-manager.c:100`), and the function
   is `gnome-bg.c:1811`; `nemo-desktop` links the same `libcinnamon-desktop`.
2. Original image branch (`gnome-bg.c`, ~line 1855, the non-color `else`):
   `surface = gdk_cairo_surface_create_from_pixbuf (pixbuf, scale, window);`. A pixbuf-derived
   surface paints black when composited into the Wayland layer-shell window.
3. GSettings rule out a misconfigured dark fallback. As `gdmtest`
   (`sudo -u gdmtest env XDG_RUNTIME_DIR=/run/user/1000
   DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus gsettings get
   org.cinnamon.desktop.background <key>`), the schema has `primary-color` = `#00ff00`,
   `secondary-color` = `#000000`, `picture-options` = `zoom`, `picture-uri` =
   `file:///usr/share/backgrounds/rocky-default-10-gemstone-skies-day.png`.
4. The "black" screenshots captured during diagnosis were the live wallpaper dimmed to ~30% by the
   idle screen (no input for > `idle-delay` = 900 s), not a render failure. Example pixel pair,
   bright top-left `(158,46,86)` vs idle "black" `(47,14,26)`; `(47,14,26)` is ~0.30x of
   `(158,46,86)`. No sysfs backlight node and no input-injection tooling existed on the VM to wake
   the display, so a fresh GDM login was used to re-arm it.

**Fix (Tails, applied).**
1. Patched the image branch to render the pixbuf onto a window-similar surface the same way the
   solid-color branch does: `gdk_window_create_similar_image_surface()` (or
   `cairo_image_surface_create()` with no window), then `gdk_cairo_set_source_pixbuf()` +
   `cairo_paint()`. Patch: `gnome-bg-wayland-surface.patch`, now at
   `/home/howard/Linux/projects/cinnamon-for-rocky10/spec/gnome-bg-wayland-surface.patch`.
2. Rebuilt `cinnamon-desktop` as `6.7.2-2.el10` with `Patch0` applied (`%patch0 -p1`):
   `/home/howard/rpmbuild/SPECS/cinnamon-desktop.spec`, now synced to
   `/home/howard/Linux/projects/cinnamon-for-rocky10/spec/cinnamon-desktop.spec`.
3. Added the missing gdk-pixbuf loaders as a separate RPM, `gdk-pixbuf-parsers-2.42.12-1.el10`
   (spec `.../cinnamon-for-rocky10/spec/gdk-pixbuf-parsers.spec`), which installs
   `libpixbufloader-png.so` / `libpixbufloader-jpeg.so` and regenerates `loaders.cache` in `%post`.
   The stock `gdk-pixbuf2-2.42.12-4.el10_1.5` ships neither the PNG/JPEG loaders nor
   `gdk-pixbuf-query-loaders`.

**Verification (all on gdm-login-vm, 2026-09-17, re-checked after the fix).**
1. Installed library is the patched build: `/usr/lib64/libcinnamon-desktop.so.4.0.0` is 451936
    bytes, md5 `cc58f80f19bb3b353851efde2250018c`
    (`md5sum /usr/lib64/libcinnamon-desktop.so.4.0.0`); a freshly built unpatched control library
    is 452992 bytes, md5 `c1b9fd3a7e1ccf94bd3bdc942781b7c1`. They differ, proving the patch is in
    the installed RPM.
2. Loaders present and cache current: `loaders.cache` lists gif/jpeg/png/svg/tiff
    (`grep -oE 'libpixbufloader-[a-z]+\.so' /usr/lib64/gdk-pixbuf-2.0/2.10.0/loaders.cache`); a
    fresh `gdmtest` process decodes the wallpaper via a PyGDK pixbuf load (`PNG OK 4000 2250`).
3. Fresh first login (`systemctl restart gdm` to force a clean autologin), captured with
    `sudo virsh screenshot gdm-login-vm /tmp/opencode/TASK0017-freshlogin.png`, renders the
    wallpaper: center `(67,18,56)`, nonblack `1.000`, colorful `0.950`
    (`python3 /tmp/opencode/analyze-shot2.py /tmp/opencode/TASK0017-freshlogin.png`); multi-region
    `2551` distinct colors, saturated fraction `0.955`
    (`python3 /tmp/opencode/analyze-multi.py /tmp/opencode/TASK0017-freshlogin.png freshlogin`);
    the 64x64 grid matches the earlier verified green state (top-left `(158,46,86)`, panel row
    `(51,51,55)`).

**Durable artifacts.** In the local `cinnamon-rocky10` DNF repo
(`/home/howard/Linux/projects/cinnamon-for-rocky10/rpms/`, VM mirror `/root/rpms/`,
`baseurl=file:///root/rpms`), freshly resolved by `createrepo_c` (repodata verified to contain
each):
- `cinnamon-desktop-6.7.2-2.el10.x86_64.rpm` (+ `-devel`), supersedes the broken `6.7.2-1.el10`.
- `gdk-pixbuf-parsers-2.42.12-1.el10.x86_64.rpm` (PNG/JPEG loaders + cache helper).
- Prerequisite rebuilds from the prior entry: `nemo-6.7.4-2.el10` (gtk-layer-shell Wayland
  backend), `gtk-layer-shell-0.10.1-1.el10`, `cinnamon-settings-daemon-6.7.2-2.el10`.

Specs and the gnome-bg patch are now in the canonical project `spec/` dir; the host
`/home/howard/rpmbuild/` tree remains the authoritative build path (per the note above). The `-2`
RPMs, `-devel`, and specs are staged in the working repo for `Knuckles` to commit/publish;
`repodata/` is generated and not tracked.

**Alternatives rejected.** (a) Keep unpatched `cinnamon-desktop-6.7.2-1` and set a solid
`primary-color` instead of a photo: the DoD requires the Gemstone Skies photo, not a flat color,
and the image branch is the real defect. (b) Patch nemo-desktop's background code directly rather
than the shared `gnome-bg`: that duplicates the gnome-bg logic and leaves `csd-background` still
broken, since both consume `libcinnamon-desktop`. (c) Ship the Fedora reference
`libcinnamon-desktop`: version mismatch and it is not our build.

Note: the "black" screenshots during diagnosis were idle screen dimming (~30% of the live image),
not a regression from adding `gdk-pixbuf-parsers`. The green evidence and the fresh-login evidence
above are the valid render results.

### Cinnamon Settings (control-center) Python deps: source-build the three modules as RPMs (Tails, 2026-09-17)

**Decision: source-build the missing Python modules as RPMs in this repo and add `Requires:` to
`spec/cinnamon.spec`. Do not patch the imports.** The full closure (discovered progressively on the
live VM, see work log): source-build `python3-setproctitle-1.3.7`, `python3-pillow-12.3.0`,
`python3-tinycss2-1.5.1`, `python3-webencodings-0.5.1` (tinycss2's declared dependency, absent from
EL10), and `python3-xapp-3.0.2` (imported at `bin/SettingsWidgets.py:10` and `xapp.os` at
`cinnamon-settings.py:33`; source is the separate `linuxmint/python3-xapp` project, also absent
from EL10). `psutil` is a runtime dependency of `xapp.os` but **is not source-built**:
`python3-psutil-5.9.8-6.el10` ships in EL10 appstream and is a `Requires:` of
`python3-xapp.spec`. Final spec state: `cinnamon.spec` at 3.el10 with `Requires:` for
`python3-setproctitle`, `python3-pillow`, `python3-tinycss2`, `python3-xapp`.

**Option A — source-build the three modules (chosen).** The Fedora ref carries exactly this
solution: `rpm -q --requires cinnamon` on `ref-overlay-task0017` shows the ref's
`cinnamon-6.6.7-7.fc44` Requires `python3-pillow(x86-64)`, `python3-setproctitle(x86-64)`,
`python3-tinycss2`; the ref imports all three (verified 2026-09-17: `PIL 12.3.0`,
`tinycss2 1.5.1`, `setproctitle 1.3.7` import OK on its Python 3.14.7). Building the same modules
and adding the same `Requires:` keeps our installed Cinnamon source tree byte-identical to
upstream 6.7.4 (zero divergence) and the runtime behavior identical to the ref. Versions match the
ref's upstream versions exactly, so parity is on module behavior, not just module presence. All
modules build cleanly on the host's Python 3.12.13 (same as the VM): setproctitle is a small C
extension (BuildRequires gcc, python3-devel), tinycss2 is pure Python, pillow is a C extension
built against libjpeg-turbo 3.0.2 + libpng 1.6.40 + zlib headers, giving JPEG/PNG support like the
ref's full-featured Pillow. EL10 note: there is no `zlib-devel` package; the headers come from
`zlib-ng-compat-devel` (`rpm -qf /usr/include/zlib.h` → `zlib-ng-compat-devel-2.2.3-3.el10_1`),
which is what the pillow spec BuildRequires.

**Option B — patch the imports to optional (rejected).** (1) It diverges from upstream: the fix
would be sed/patch hunks in the `cinnamon` spec touching `cinnamon-settings.py:11` (unguarded
`from setproctitle import setproctitle`), `bin/imtools.py:21-24`, `bin/eyedropper.py:6`,
`modules/cs_backgrounds.py:16`, `modules/cs_user.py:17` (unguarded PIL), and `modules/cs_themes.py:5`
(unguarded `import tinycss2`), every one of them carried and re-verified on every upstream refresh.
(2) It degrades behavior instead of restoring it: the unguarded imports are functional, not
cosmetic. Dropping `setproctitle` loses the process title (cosmetic, but a diff vs the ref);
dropping PIL breaks the wallpaper preview render (`imtools`, `cs_backgrounds`), the color
eyedropper, and the user panel's image handling; dropping `tinycss2` at `cs_themes.py:5` takes the
theme panel's CSS-override path out of the build (only `CinnamonGtkSettings.py:7` is already
guarded, and that guard exists upstream, so the panel is expected to have the module). The parity
goal is "features match the Fedora Cinnamon VM"; B guarantees a mismatch on every panel that uses
one of the three.

**Spec target correction.** The app in the FAIL row is the Python GTK app `cinnamon-settings`,
shipped by the **`cinnamon` shell RPM**, not by `cinnamon-control-center` (verified on
`gdm-login-vm` 2026-09-17: `rpm -qf /usr/bin/cinnamon-settings` → `cinnamon-6.7.4-1.el10`; tree at
`/usr/share/cinnamon/cinnamon-settings/`; `cinnamon-settings-default.desktop` and all 33
`cinnamon-settings-*.desktop` entries `Exec=cinnamon-settings <module>`). The C
`cinnamon-control-center` package (`/usr/bin/cinnamon-control-center`, compiled panels) is a
separate legacy host that does not import the three modules; the `Requires:` go in
`spec/cinnamon.spec`.

**Build notes (EL10-specific).** Host and VM both run Python 3.12.13, so host-built RPMs are
binary-compatible with the VM. EL10's `python3-rpm-macros` (3.12-11.el10) is the reduced variant:
it defines `python3_sitelib` (`/usr/lib/python3.12/site-packages`) but **no** `%pyproject_build` /
`%pyproject_install` / `%pybytecompile` macros and no `brp-python-bytecompile` *package* in the
minimal set, so the pip-based specs install via
`python3 -m pip install --no-cache-dir --no-deps --target %{buildroot}%{python3_sitelib} .` from
the verified sdist and ship the dist-info. Correction to an earlier note in this entry: byte
compilation is **not** skipped. The brp *scripts* ship with the `rpm` package itself
(`/usr/lib/rpm/redhat/brp-python-bytecompile` exists and ran during every build; only the
standalone `brp-python-bytecompile` package is absent), so the RPMs ship `.pyc`/`__pycache__`
files (verified in the pillow RPM file list, 308 files). `python3-xapp` is the exception: it has
no pip metadata, so its spec builds with `meson setup build -Dprefix=/usr` +
`DESTDIR=%{buildroot} ninja -C build install` (the default `/usr/local` prefix would land the
package outside the RPM; `-Dprefix=/usr` puts it on `%{python3_sitelib}` exactly). pip's hash
verification against PyPI metadata is the checksum step for the pip-built modules; the sdist
sha256s are recorded in each spec, and `python3-xapp`'s sha256
(`2078766e2553eea0ff2ee598212d4883a226df63d014d060756c6274db024823`, GitHub tag tarball) is
recorded in its spec. Naming follows Fedora (`python3-setproctitle`, `python3-pillow`,
`python3-tinycss2`, `python3-xapp`) so `Requires:` and `repoquery` match the ref.

**Work log (Tails, 2026-09-17).**

- Specs added to `spec/`: `python3-setproctitle.spec` (BSD-3-Clause), `python3-pillow.spec`
  (HPND and MIT), `python3-tinycss2.spec` (BSD-3-Clause), `python3-webencodings.spec` (BSD),
  `python3-xapp.spec` (LGPLv2+). All carry `%global debug_package %{nil}`, a sha256 comment under
  Source0, and a `6.7.4-.../3.0.2-1.el10` changelog entry.
- rpm spec gotchas hit and fixed while authoring: (1) a `%section` name inside a `#` comment
  opens a section in the scanner (`# ... in %install` → `error: second %install`; minimal repro
  kept in `/tmp/opencode/spectest/`), comments reworded; (2) without `%global debug_package
  %{nil}` the auto `debuginfo` subpackage collides; (3) `%setup -q` needs `-n <sdist-dir>` for the
  pip sdists (top dirs lack the `python3-` prefix); (4) pillow's dist-info dir is PEP 503
  normalized `pillow-12.3.0.dist-info`, not `PIL-...`; (5) `ninja` takes DESTDIR from the
  environment, not as a positional.
- Built in `/home/howard/rpmbuild/RPMS/x86_64/`: `python3-setproctitle-1.3.7-1.el10`,
  `python3-pillow-12.3.0-1.el10` (308 files, `_imaging.cpython-312-x86_64-linux-gnu.so` with
  `jpeg_start_compress@LIBJPEG_6.2` per `nm -D`), `python3-tinycss2-1.5.1-1.el10`,
  `python3-webencodings-0.5.1-1.el10`, `python3-xapp-3.0.2-1.el10` (77 files: 12 `.py` + 60 `.mo`
  + license), and `cinnamon-6.7.4-3.el10` + debuginfo/debugsource.
- `spec/cinnamon.spec`: 1.el10 → 3.el10, four `Requires:` (the three above + `python3-xapp`),
  two changelog entries (2.el10, 3.el10). Pre-existing `bogus date in %changelog` warning on the
  `Sun Aug 10 2026` entry is not from this change.
- Repo `rpms/`: now 64 RPMs + `repodata/` (`createrepo_c` after each change). Removed
  `cinnamon-6.7.4-1.el10`/`2.el10` main+debuginfo+debugsource as superseded. Verified via
  `zstd -d -c repodata/*-primary.xml.zst`: `cinnamon 6.7.4-3.el10` carries the four python
  requires; `python3-xapp` requires `python3-psutil`, `xapps-lib`, `python3-gobject`.
- VM (`gdm-login-vm`): repo `file:///root/rpms` rsynced; `dnf install`/`upgrade` succeeded.
  Installed set: the five new RPMs, `python3-psutil-5.9.8-6.el10` (appstream, not our repo),
  `cinnamon-6.7.4-3.el10`. The first `dnf upgrade` attempt failed on
  `python3.12dist(webencodings) >= 0.4 needed by python3-tinycss2` — that failure is what added
  `python3-webencodings` to the plan.
- Missing-module chain found live on the VM (each fix unblocked the next import):
  `setproctitle` (`cinnamon-settings.py:11`) → `xapp` (`bin/SettingsWidgets.py:10`,
  `cinnamon-settings.py:32`) → `psutil` (`xapp/os.py:4` via `cinnamon-settings.py:33`
  `import xapp.os`). The `xapp` Python package is not in the `xapps`/`xapp` C-library source
  (checked tags 3.0.1/3.2.3/3.3.3: only `pygobject/XApp.py`), it comes from the separate
  `linuxmint/python3-xapp` project (ref package `python3-xapp-3.0.2-2.fc44`, LGPLv2+, meson
  build); our build matches the ref's file list.
- Verification on the VM (all as `gdmtest` in the Wayland session,
  `WAYLAND_DISPLAY=wayland-0 XDG_RUNTIME_DIR=/run/user/1000
  DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus`):
  - Import probes pass in the app's own form: `from setproctitle import setproctitle`,
    `from xapp.SettingsWidgets import SettingsWidget, SettingsLabel`, `tinycss2 1.5.1`,
    `PIL 12.3.0` with JPEG support True and JPEG+PNG roundtrips OK.
  - Live app: `cinnamon-settings default` runs (empty log, no traceback; PID stable across
    minutes), `cinnamon-settings themes` runs (tinycss2 path), `cinnamon-settings backgrounds`
    runs (PIL path). `ps` shows comm `cinnamon-settin` / args `cinnamon-settings` — the
    setproctitle process title is applied, direct evidence the module is live.
  - Screenshot evidence in `vm-test/parity/rocky10/`:
    `2026-09-17-control-center-01-desktop.png` (baseline), `-02-settings-main.png`,
    `-03-settings-themes.png`, `-04-settings-backgrounds.png`. Captured with `sudo virsh
    screenshot gdm-login-vm` (host side; `tasks/lib/vnc-grab.py` times out on this VM's VNC
    5900/5903). `-02` differs from the baseline (252 KB vs 529 KB, different md5) consistent
    with the settings window open; image content not visually inspected (no vision in this
    model) — flag for Big's 3.1 re-verification to eyeball the panels.
- What remains for this item: nothing on the build side. Big's 3.1 fresh-VM verification should
  (a) install from the repo on a clean session and confirm the app opens with no manual
  `dnf install` steps, and (b) visually confirm the three panels render.

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

*Entry 2026-09-15: plan item 0.1, environment verification on host 192.168.1.102. This was direct
host/VM verification, not a CI workflow run; no code existed to compile or unit-test yet, so the
compile/linter/unit/integration/Sparky rows of the standard table do not apply to this entry.*

**Checks:**

| Check | What it exercises | Result | Notes |
|---|---|---|---|
| A1 gnome-terminal in Rocky 10 repos | terminal availability for DoD | FAIL | xterm (baseos) and konsole (EPEL) are the only terminals |
| A2 Cinnamon background schema | dconf override target for wallpaper | PASS | `picture-uri` only, no `picture-uri-dark` in the cinnamon schema |
| A4 shell RPM data tree | applets/desklets/settings payloads ship in `cinnamon` | PASS | 34 applet dirs, 3 desklets, settings desktops present |
| A5 menu button icon | which icon the menu button loads, and how | PASS | schema key `org.cinnamon app-menu-icon-name`; ref value `fedora-logo-sprite` |
| env: host identity | 192.168.1.102 is the expected host | PASS | `shadow`, Rocky Linux 10.2, dnf 4.20.0 |
| env: 192.168.1.103 | bare-metal reference host | FAIL (gone) | 100% ping loss, "Destination Host Unreachable" |
| env: ref VM boot | fedora-cinnamon-ref boots from disk | PASS after repair | repair-boot trap re-armed in XML; removed, see below |

**Checks requested vs run:** 4 assumption checks requested (A1, A2, A4, A5; A3 out of scope per
brief), 4 executed. Plus the environment facts above.

**Environment facts (2026-09-15):**

- Host `shadow` (192.168.1.102): `. /etc/os-release` → "Rocky Linux 10.2 (Red Quartz)"; `dnf --version` → 4.20.0.
- libvirt is socket-activated: `systemctl is-active libvirtd` → `inactive` (dead but enabled); split daemons `virtqemud`, `virtnetworkd`, `virtlogd` active. For user `howard` the default URI is rootless `qemu:///session`, which lists no domains. **All libvirt operations here must use `virsh -c qemu:///system`.**
- Fleet (`virsh -c qemu:///system list --all`): `gdm-login-vm` running (192.168.122.15, VNC 127.0.0.1:5900, disk `/var/lib/libvirt/images/cinnamon-test/gdm-login-vm.qcow2`); `fedora-cinnamon-ref` shut off at start of this item (VNC 5901, disk `/home/howard/vm-disks/fedora-cinnamon-ref.qcow2`); `rocky10-explore` shut off (VNC 5902, disk `/home/howard/vm-disks/rocky10-explore.qcow2`).
- `gdm-login-vm` guest: Rocky 10.2, `cinnamon-6.7.4-1.el10`, `gdm-47.0-22.el10_2` (`rpm -q cinnamon gdm`).
- Host repo defect: `/etc/yum.repos.d/cinnamon-rocky10.repo` has baseurl `file:///home/howard/cinnamon_test/cinnamon-for-rocky10/rpms`, a path that does not exist (project lives at `/home/howard/Linux/projects/cinnamon-for-rocky10`). Any default-repo dnf query fails with "All mirrors were tried". Blocks R7 / plan item 1.2 republish until fixed.
- dnf quirk: the `nxadm-pkgs-rakudo-pkg` (cloudsmith) repo triggers an interactive GPG key import prompt; pass `--assumeno` to keep queries non-interactive.

**A1 (FAIL) — gnome-terminal not in Rocky 10 repos:**

- `dnf -q --assumeno --disablerepo='*' --enablerepo=appstream,crb,baseos,extras repoquery --available | grep -E 'terminal|konsole|xterm'` → only `xterm-0:389-4.el10.x86_64` and `xterm-resize-0:389-4.el10.x86_64`.
- EPEL (23960 packages): same grep → `konsole-0:25.12.3-1.el10_2.x86_64` (konsole family) matches; no gnome-terminal.
- Conclusion: gnome-terminal is absent from AppStream, CRB, BaseOS, Extras, and EPEL. Available alternatives: `xterm` (baseos), `konsole` (epel). The plan's fallback (pick closest alternative, record deviation) applies; the pick is Amy's/Tails', not Big's. This is an assumption failure, not a code or harness bug.

**A2 (PASS, one refinement) — background schema:**

- `gsettings list-schemas | grep -i background` on gdm-login-vm → `org.cinnamon.desktop.background`, `org.cinnamon.desktop.background.slideshow`, `org.gnome.desktop.background`.
- `gsettings list-recursively org.cinnamon.desktop.background` → keys: `color-shading-type`, `picture-opacity`, `picture-options`, `picture-uri` (default `file:///usr/share/themes/Adwaita/backgrounds/adwaita-timed.xml`), `primary-color`, `secondary-color`. **The cinnamon schema has no `picture-uri-dark` key.** The dconf override must therefore target `picture-uri` only. (The ref's Fedora overrides use `picture-uri-dark` because they target `org.gnome.desktop.background`, which does have both keys.)
- `rpm -qf /usr/share/glib-2.0/schemas/org.cinnamon.desktop.background.gschema.xml` → `cinnamon-desktop-6.7.2-1.el10` (our build provides the schema).
- `/etc/dconf/profile/user` contains `system-db:local`; `/usr/share/dconf/db.local.d/` does not exist yet (the new RPM creates it). Pre-existing override `10_org.gnome.desktop.background.default.gschema.override` (rocky-logos) targets only `org.gnome.desktop.background`.

**A4 (PASS) — shell RPM ships the full data/ tree:**

- On gdm-login-vm, `rpm -ql cinnamon` → 818 files total.
- `rpm -ql cinnamon | grep -c applets` → 183 (files); distinct dirs under `/usr/share/cinnamon/applets/` → exactly **34**: a11y, calendar, cornerbar, expo, favorites, grouped-window-list, inhibit, keyboard, menu, network, nightlight, notifications, on-screen-keyboard, panel-launchers, power, printers, recent, removable-drives, scale, separator, settings, settings-example, show-desktop, slideshow, sound, spacer, systray, trash, user, window-list, windows-quick-list, workspace-switcher, xapp-status, xrandr. (The plan's "expect 34" counts dirs, not files.)
- Desklets: 3 (clock, launcher, photoframe) under `/usr/share/cinnamon/desklets/`.
- `/usr/share/applications/cinnamon-settings-default.desktop` present; 33 `cinnamon-settings-*.desktop` files; 19 theme files under `/usr/share/cinnamon/theme/`; `cinnamon.session` and `cinnamon-wayland.session` present.

**A5 (PASS) — menu button icon mechanism:**

- Code path (ref, cinnamon 6.6.7): `class Menu` in `/usr/share/cinnamon/applets/menu@cinnamon.org/applet.js:1110` binds settings `menu-custom`/`menu-icon`/`menu-icon-size`/`menu-label` (lines 1173-1176). In `_updateIconAndLabel()` (~line 1521), when `menuCustom` is false the icon comes from `global.settings.get_string('app-menu-icon-name')` → `set_applet_icon_name()` in `/usr/share/cinnamon/js/ui/applet.js:705` → `St.Icon.set_icon_name()` → `Gtk.IconTheme` name lookup, i.e. **icon-theme based resolution**.
- The key lives in schema `org.cinnamon` (`/usr/share/glib-2.0/schemas/org.cinnamon.gschema.xml:580`), upstream default `"cinnamon-symbolic"`.
- Fedora's mechanism: `cinnamon-6.6.7-7.fc44` ships `/usr/share/glib-2.0/schemas/10_cinnamon-common.gschema.override`, which sets `app-menu-icon-name='fedora-logo-sprite'` and `system-icon='fedora-logo-sprite'` (plus `app-menu-label`, the default `enabled-applets` panel layout, `panels-height`, sounds, and theme). The override is compiled into `gschemas.compiled`. Verified: `gsettings get org.cinnamon app-menu-icon-name` → `'fedora-logo-sprite'`, with no user dconf (`~/.config/dconf/` absent), no dconf system override, and a single schema copy on the box, so the value comes from the compiled override.
- **Gap found on the ref:** `fedora-logo-sprite` exists only as `/usr/share/pixmaps/fedora-logo-sprite.{png,svg}`; `find /usr/share/icons -name "fedora-logo-sprite*"` → empty, and the active icon theme is Mint-Y-Aqua. `Gtk.IconTheme` cannot resolve the name, so the ref's menu button most likely renders the missing-image fallback. On-screen confirmation needs VNC (Sparky layer, outside this item). Consequence for the Rocky implementation: the logo asset must be installed as a real icon-theme entry (e.g. `/usr/share/icons/hicolor/scalable/apps/`); a pixmaps drop is insufficient.
- Current Rocky state (gdm-login-vm): `gsettings get org.cinnamon app-menu-icon-name` → `'cinnamon-symbolic'` (the Cinnamon logo, i.e. the status quo the task replaces); `system-icon` → `''`. `cinnamon-6.7.4-1.el10` ships no `org.cinnamon` gschema override; `cinnamon-symbolic.svg` is owned by the cinnamon package (84 hicolor icon files in that RPM).

**Ref VM repair-boot trap (environment repair, recorded for the record):**

- First `virsh start fedora-cinnamon-ref` fired a repair-boot trap. The persistent XML contained `<kernel>/home/howard/ISOs/fc-inst/vmlinuz</kernel>`, `<initrd>/home/howard/ISOs/fc-inst/initramfs.img</initrd>`, `<cmdline>root=UUID=0b414dcc-4a3e-400f-b7f3-66821c61ff97 rw rootflags=subvol=root console=tty0,115200n8 console=ttyS0,115200n8 init=/bin/bash</cmdline>`.
- TASK-0018 records this triple as removed and verified 2026-09-01, and the 2026-09-14 status check only confirmed "defined, shut off", so the triple was re-armed sometime between. Root cause of the re-arm is not identified. Process flag: any future `virsh define`/edit of this VM must re-run the trap check before start.
- Fix: `virsh destroy` → `virsh dumpxml` → removed the three lines → `virsh define` (trap check clean) → `virsh start` (exit 0). Disk SELinux label verified (`svirt_image_t` on `/home/howard/vm-disks/fedora-cinnamon-ref.qcow2`); no CDROM devices; single virtio `vda`, boot order 1.
- After repair the ref boots the installed Fedora 44 ("Forty Four", systemd), howard has an active user session, and the DHCP lease is 192.168.122.156, matching the pinned keys in `~/.ssh/known_hosts` (3 entries: ed25519/rsa/ecdsa).
- `rocky10-explore`'s XML was not checked for the same trap; do so if the R6 fallback activates.

**Verdict:** A1 FAIL, A2 PASS, A4 PASS, A5 PASS.

- A1 is the only failed check. It is a repos fact, not a code bug (nothing to send to `Tails`) and not a harness bug: gnome-terminal simply does not exist in Rocky 10 or EPEL. The plan's fallback governs; `xterm` (baseos) is the first-party option and `konsole` (EPEL) the full-featured one. The pick and the recorded deviation are Amy's/Tails'.
- A2 passes with the refinement that the override targets `picture-uri` only (no dark variant in the cinnamon schema).
- A4 passes as-is; the plan's "34" is dir count, verified exactly.
- A5 passes with two actionable facts for the implementation: the icon is controlled by the single schema key `org.cinnamon app-menu-icon-name` (override-able via gschema override file or dconf system db, Fedora precedent is the former), and the asset must land in an icon-theme directory, not pixmaps. The ref's own icon rendering (sprite not theme-resolvable) stays unverified until a Sparky/VNC screenshot; that does not change A5, which asked for the icon name and mechanism.
- Environment side effects to carry forward: use `virsh -c qemu:///system` on this host; fix the broken `cinnamon-rocky10.repo` baseurl before item 1.2; treat the ref repair-trap re-arm as an open process gap.

*Entry 2026-09-15: plan item 2.1, live-session render check on `gdm-login-vm` (Rocky) and
`fedora-cinnamon-ref` (Fedora 44 ref). Like entry 0.1 this was direct VM verification, not a CI
workflow run, so the compile/linter/unit/integration/Sparky rows of the standard table do not
apply to this entry. Evidence PNGs live under `vm-test/parity/` in the project repo at commit
`a971031` (branch `feature/TASK-0017-cinnamon-desktop-completeness`). Captures are 1280x800 from
QEMU VNC (127.0.0.1:5900/5901) via a purpose-built grabber; the session frame was independently
re-confirmed with `virsh screenshot`, so the grab path is not a variable.*

**Checks:**

| Check | What it exercises | Result | Notes |
|---|---|---|---|
| B1 GDM login to Cinnamon (Wayland) | harness drives the greeter to a real session | PASS | session 53, wayland, active, seat0/tty2 |
| B2 panel render | compositor surfaces the panel | PASS | bottom 40px, bg (26,26,31), white icons |
| B3 menu button branding | Rocky logo replaces the Cinnamon logo | PASS | green (16,185,129) logo, icon owned by `rocky-logos` |
| B4 wallpaper config | wallpaper files + dconf value | PASS | animated XML + day/night PNGs present, `picture-uri` set |
| B5 wallpaper render | nemo-desktop composites the background | FAIL | desktop region 100% black, see below |
| B6 desktop icon render | nemo-desktop composites icons | FAIL | test file on `~/Desktop` not rendered |
| B7 ref comparison | Fedora ref desktop A/B | NOT RUN | ref has no live Cinnamon session, no login path |

**Checks requested vs run:** 2 requested (wallpaper render, menu button branding), 2 executed.
B1, B2, B4, B6 are supporting checks. B7 was not runnable for the reason recorded below; that
coverage drop is explicit, not silent.

**B1 (PASS) - login:** `source /root/gdm-harness/gdm-drive.sh; gdm_login gdmtest /root/gdmtest.pass cinnamon-wayland` -> rc=0; `gdm_wait_session gdmtest 120 cinnamon-session` -> rc=0. `loginctl` -> session 53, type=wayland, state=active, seat0/tty2; processes `cinnamon-session` (13714), `cinnamon` (13771), `nemo-desktop` (15027 after respawn). The greeter pre-capture `vm-test/parity/rocky10/2026-09-15-2.1-01-greeter-before.png` shows black with a thin gray-170 text band (x 520..748, y 386..398); the ref shows the identical regime, so the black greeter screen is normal GDM Wayland state on this virtio display, not a defect.

**B2 (PASS) - panel:** in `vm-test/parity/rocky10/2026-09-15-2.1-02-cinnamon-session.png` the bottom 40px (y 760..800) render: bg (26,26,31), border (51,51,55), white icons/text, Cinnamon green (16,185,129) accent.

**B3 (PASS) - menu button is the Rocky logo:**

- Session capture, bottom-left panel: green logo, sampled (16,185,129) + alpha, matching the Cinnamon accent hue.
- `gsettings get org.cinnamon app-menu-icon-name` -> `'fedora-logo-icon'`; `system-icon` -> `'fedora-logo-icon'`. Value comes from the compiled gschema override in `cinnamon-rocky-defaults` (`spec/cinnamon-rocky-defaults.spec`, `Requires: rocky-logos`), the same mechanism Fedora uses (A5).
- `/usr/share/icons/hicolor/{16,22,24,32,48,64,128,256}px/apps/fedora-logo-icon.png` -> `rpm -qf` -> `rocky-logos-100.5-3.el10.x86_64`. The name is a Fedora upstream naming holdover; the asset is the Rocky logo from the official `rocky-logos` package. Local analysis of the 256px copy (`/tmp/opencode/fedora-logo-icon-256.png`): monochrome green (16,185,129,255) + alpha, shape = rounded mass + diagonal + center diamond.
- This closes the A5 gap: the ref's `fedora-logo-sprite` is pixmaps-only and unresolvable by the icon theme; the Rocky implementation installs the asset as a real icon-theme entry under hicolor/apps, resolvable by the active theme (`gnome`).

**B4 (PASS) - wallpaper config:** dconf (read as gdmtest) `org.cinnamon.desktop.background picture-uri` = `file:///usr/share/backgrounds/rocky-default-10-gemstone-skies-time.xml` (animated day/night), `picture-options` = `'zoom'`. The XML plus `rocky-default-10-gemstone-skies-day.png` (6.2MB) and `-night.png` (3.8MB) all exist under `/usr/share/backgrounds/`, owned by `rocky-backgrounds`.

**B5/B6 (FAIL) - the nemo-desktop surface is not composited:**

- Desktop region (y 0..758) of the session capture is 100% pure black, 0 non-black pixels; `virsh screenshot` independently matches the VNC capture.
- Static test: `picture-uri` set to the plain `rocky-default-10-gemstone-skies-day.png` (dconf written as gdmtest via `runuser -u gdmtest` with `XDG_RUNTIME_DIR`/`DBUS_SESSION_BUS_ADDRESS`; as root dconf fails with "Broken pipe") -> still 99.6% black. Rules out the animated-XML path.
- Process test: `kill -9` of nemo-desktop, respawn -> still black. Rules out a wedged process state.
- Icon test: created `/home/gdmtest/Desktop/TASK0017-wptest.txt` -> icon not rendered (0 non-black pixels in the top-left quadrant). Background and icons live on the same nemo-desktop surface, and no fullscreen app was running to occlude the desktop, while the panel (a mutter surface) composites fine.
- nemo-desktop itself is healthy: alive, software-rendering (no DRM fd, libcairo only), ~40MB RSS, no errors in journal.
- Classification: a compositing failure of the nemo-desktop Wayland surface on the virtio-vga display path. Not a wallpaper file or config problem. Defect in the Rocky/Cinnamon stack vs environment limitation: undetermined, because the ref could not be put in a session for the A/B (B7).

**B7 (NOT RUN) - ref comparison:** `vm-test/parity/fedora-ref/2026-09-15-2.1-01-greeter-current.png` captured (greeter only). The ref has no live Cinnamon session: only a lingering headless `howard` session (39 user, 40 manager, no seat/tty), no cinnamon/gdm/nemo processes, `~/Desktop` absent. Login as howard is impossible (no root, no `/root/gdm-harness` access, no login password). The ref's greeter regime (black + centered gray-170 text) matches the Rocky greeter capture, which is what B7 could still confirm.

**Cleanup:** wallpaper restored to the original animated XML; test file removed; `~/Desktop` empty. VM left in logged-in session 53 (gdmtest, wayland).

**Verdict:** menu button branding PASS. Wallpaper config PASS, wallpaper render FAIL.

- B3 is a full pass on both the pixel evidence and the package-ownership evidence, and it closes the A5 icon-theme gap by design (hicolor/apps entry, not pixmaps).
- B5/B6 is not a harness bug: the harness logged in, the capture was triple-verified (VNC, virsh, diagnostic re-captures), and the config was proven correct by the static-PNG test. The black desktop is a compositing failure of the nemo-desktop surface. It goes to `Tails` as the suspected defect with one open caveat: "defect vs virtio-vga environment limitation" cannot be settled until the ref is put in a Cinnamon session, which needs a howard login path on `fedora-cinnamon-ref` (password or harness access).
- B7's coverage drop is recorded above; the ref comparison side exists only as a greeter capture.

---

*Entry 2026-09-17: plan item 2.2 (Rocky parity re-run on `gdm-login-vm` after the 2.1 wallpaper fix) plus plan item 0.3 (Fedora reference baseline). Direct VM verification, not a CI workflow run, so the standard table's compile/linter/unit/integration/Sparky rows do not apply to this entry (same scope note as the prior entries). Evidence in the project repo at `vm-test/parity/rocky10/` and `vm-test/parity/fedora-ref/` (uncommitted at time of writing; `vm-test/parity/` is a new untracked directory; the Tails spec and RPM changes in that repo are separate from this entry). The ref baseline was captured on `ref-overlay-task0017` (192.168.122.85, libvirt id 79), a disposable qcow2 overlay of the reference disk per the 2026-09-15 post-2.1 decision. The pristine `fedora-cinnamon-ref` was powered off and untouched throughout; the 0.3 repair-trap re-check is N/A (the pristine reference was never booted and the overlay is a fresh definition that cannot inherit the trap).*

**Parity matrix (item 2.2):** rows = DoD minimum set plus wallpaper plus branding. Ref = Fedora 44, Cinnamon 6.6.7, lightdm. Rocky = Rocky 10.2, Cinnamon 6.7.4, GDM (DM and version delta are pre-accepted deviations, plan lines 485-487).

| Row | Fedora ref (expected) | Rocky 10 (actual) | Status |
|---|---|---|---|
| Panel applets | 14 enabled: menu, show-desktop, grouped-window-list, keyboard, systray, xapp-status, notifications, printers, removable-drives, network, nightlight, power, calendar, sound; 34 available; icons render (0.3-01) | 15 enabled: same set with separator, favorites, cornerbar in place of show-desktop and nightlight; 34 available; icons render (2.2-01) | PASS both; composition delta is a default layout difference, not a defect |
| Wallpaper | `tiles/default_blue.jpg` renders (0.3-01) | `rocky-default-10-gemstone-skies-time.xml` (day 8AM-6PM, night after) renders the night variant: screenshot mean rgb (33.1, 1.6, 24.9) vs night PNG (34.0, 0.1, 23.9), nonblack 0.788 vs 0.735, colorful 0.217 vs 0.251 (2.2-01, identical thresholds) | PASS both; 2.1 fix holds; the 2.1 verification numbers (nonblack 1.000, colorful 0.950, 2551 colors) came from a daytime capture, and the day PNG measures nonblack 1.000 at the same threshold |
| Branding | `fedora-logo-sprite` configured; asset is pixmaps-only and unresolvable by the icon theme (A5 gap) | `fedora-logo-icon` from the `rocky-logos` hicolor entry renders in the panel (2.2-01; B3) | Rocky PASS; ref renders per the A5 note |
| Themes | Mint-Y-Dark-Aqua (cinnamon-themes package) applied; dark aqua UI in every capture | default Cinnamon theme, GTK Adwaita, icon theme gnome (inventory) | PASS both (default applies); the selector UI on Rocky is blocked by the settings crash |
| Extension/applet/desklet manager | opens; applet list renders (0.3-06b); 34 applets, 3 desklets, 0 shipped extensions | cannot open; `cinnamon-settings` crashes (see below) | ref PASS; Rocky FAIL |
| Screensaver | `cinnamon-screensaver-6.6.1` package, lock enabled, service inactive | in-shell at 6.7 (`js/ui/screensaver`), lock enabled, `cinnamon-screensaver-command` present | PASS both; lock enabled on both sides; service architecture differs by design |
| Cinnamon Settings | opens (PID 9573), home icon grid renders (0.3-03); singleton module switch works (applet view, 0.3-06b) | crash on launch: `ModuleNotFoundError: No module named 'setproctitle'` (detail below); 2.2-03 shows desktop only | ref PASS; Rocky FAIL |
| Main menu | opens via the applet API, `isOpen: true`, 83,874 px diff vs desktop, search band and app grid render (0.3-02); settings entry registered (inventory) | opens; search, app grid and settings category render (2.2-02) | PASS both; settings submenu not visually confirmed on ref (data present per inventory) |
| nemo | 6.6.3 opens; home dir icon view with sidebar and grid (0.3-04) | 6.7.4 opens (2.2-04) | PASS both |
| Terminal | gnome-terminal 3.60.0 (VTE 0.84.1) opens; typed input and output render (0.3-05) | absent (A1: no package in EL10 or EPEL); 2.2-05 not captured | ref PASS; Rocky FAIL (1.4 source build pending) |
| Session/power controls | power popover opens (0.3-06); contents Power Saver, Balanced, Performance, Power Settings (API label walk); power panel registered; idle 900; wayland session only | power popover opens (2.2-06); power panel registered; idle 900; wayland and X sessions; session settings panel absent on both sides (consistent) | PASS both |

**Checks requested vs run:** item 0.3 requested the trap re-check, boot, login, inventory, and baseline files. Executed: trap re-check N/A (documented above), boot PASS, login PASS (howard active session), inventory saved (`inventory-fedora-ref-0.3.txt`, 209 lines), 8 screenshots saved (01-06 plus 06b). Item 2.2 requested the wallpaper re-verify, inventory, the 11-row matrix, and the gap list. Executed: wallpaper re-verify PASS (measured, row above), inventory saved (`inventory-rocky10-2.2.txt`, 228 lines), all 11 rows populated, 5 screenshots saved (the 05/06/11 staged captures are not possible on Rocky because the settings app cannot start; single root cause, no separate evidence needed). No checks silently dropped.

**Rocky FAIL detail, Cinnamon Settings (code bug, goes to Tails):**

- Launch as gdmtest in the session environment: `cinnamon-settings` -> `cinnamon-settings.py` line 11 `from setproctitle import setproctitle` -> `ModuleNotFoundError: No module named 'setproctitle'` (reproduced 2026-09-17).
- Import probe (python3, gdmtest): `setproctitle` MISSING, `PIL` MISSING, `tinycss2` MISSING, `gi` OK, `XApp` typelib OK (xapps-lib ships it).
- Usage in the tree: `setproctitle` only at `cinnamon-settings.py:11` (process title; the unguarded import kills the whole app); `PIL` in `bin/imtools.py:21-24`, `bin/eyedropper.py:6`, `modules/cs_backgrounds.py:16`, `modules/cs_user.py:17`; `tinycss2` unguarded at `modules/cs_themes.py:5`, guarded at `bin/CinnamonGtkSettings.py:7`.
- Repo availability: `dnf --assumeno repoquery --available` across appstream, crb, baseos, extras, epel: no `python3-setproctitle`, no `python3-pillow`, no `python3-tinycss2` in any repo. A plain `Requires:` cannot close this; Tails must source-build the three (setproctitle and tinycss2 are small; pillow needs the libjpeg, libpng, zlib dev packages) or patch the imports to optional.
- Screenshot: `vm-test/parity/rocky10/2026-09-17-2.2-03-settings-power.png` (desktop only, no settings window).

**Rocky FAIL detail, terminal (repo fact, 1.4 pending):** A1 (entry 0.1) verified gnome-terminal absent from AppStream, CRB, BaseOS, Extras, EPEL. The ref runs 3.60.0. The 1.4 source build (Tails) closes this; not a harness bug.

**Environment notes (2026-09-17):**

- Ref access is howard-only: no root, no sudo, no input group, `/dev/uinput` is root:root 0600, no `ukey` on the ref.
- The ref VNC pointer is dead: the guest QEMU USB Tablet (event4) has broken sysfs (no `name`/`capabilities`/`abs_*`, PROP=0), so absolute pointer events are dropped; PS/2 relative gave zero diff. Input paths used instead: keyboard via `virsh send-key` (codeset linux), applet menu and popover open/close via LookingGlass D-Bus (`org.Cinnamon` on the user bus, object `/org/Cinnamon/LookingGlass`, `Eval` + `GetResults`; applets located through `Main.AppletManager.definitions`, driven via `applet.menu.open()`/`.close()`).
- Rocky environment fixes made during 2.2, recorded for reproducibility: `usermod -aG input gdmtest` + re-login (the ukey harness needs `/dev/uinput`); `gsettings set org.cinnamon.desktop.screensaver idle-activation-enabled false` as gdmtest (stops the two idle lock events during captures; the lock itself stays enabled).
- The applet composition delta ref vs Rocky (show-desktop + nightlight vs separator + favorites + cornerbar) is the default panel layout difference between 6.6.7 and 6.7.4; recorded as a deviation, not a defect.

**Verdict:** wallpaper re-verify PASS (2.1 fix holds; the night variant matches the source PNG statistics). Parity matrix complete: PASS on both sides = panel applets, wallpaper, themes (default applies), screensaver, main menu, nemo, session/power controls. FAIL (Rocky, all code or repo fact, all go to Tails via 3.1): Cinnamon Settings and everything hosted inside it (extension/applet/desklet manager UI, themes selector, power settings panel) = 3 missing Python modules, none available in EL10 or EPEL repos; terminal = A1 repo fact with the 1.4 build pending. No harness bugs in this entry. Both FAIL rows need recording in `## Status` as deviations (Robotnik).

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
