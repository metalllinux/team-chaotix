# TASK-0017 — Complete the Cinnamon desktop: missing subpackages, Rocky wallpaper, branding, terminal

> **Section order below is fixed.** Each agent writes to its own section and no other. `Robotnik`
> reads only `## Status` and `## Next Actions`. Do not reorder, rename, or remove sections.

- **Created:** 2026-08-30

---

## Status

*Owner: `Robotnik`. Keep this SHORT and CURRENT — it is one of only two sections the PM reads, so a
stale entry means the whole loop runs on bad information.*

**Now (2026-09-19): all 3 re-verifications PASS (A, B, C) — Tails work done; Vector next.**
Re-verification B PASS and C PASS on fresh VM `t17-revB` (project `d128848`): (B) `run-tests.sh`
end-to-end — single-dnf install of all 64 RPMs (no fallback), 22/22 names from
`install-set.txt` verified, GDM login into cinnamon-wayland, `ukey key Super_L` opens the main
menu (META mapping proven end-to-end); (C) enforcing-SELinux smoke — the VM booted Enforcing
(`setenforce 0` in Phase 2 was runtime-only), GDM login + all five surfaces PASS, zero AVC
denials in audit.log. With A (clean-checkout rebuild), the review gate is fully closed.
Remaining: Vector (`INSTALL.md`/`README.md` for the complete set) → Knuckles (PR to main,
merge).

**Now (2026-09-19): re-verification A PASS — 2 re-verifications remain (B, C).**
Clean-checkout rebuild from a fresh clone at `2fa1b2d`: all 10 changed specs build RC 0; NVRs +
subpackage sets match `rpms/` exactly; payloads byte-identical except build-environment
artifacts (LTO stream symbol hashes -> build-ids/.gnu_debugdata; pip direct_url build paths).
Detail in `## Implementation`. Remaining, all assigned Tails: (B) `run-tests.sh` end-to-end on
a fresh VM (also proves the META mapping via a `ukey key Super_L` menu open), (C)
enforcing-SELinux smoke. Then Vector (`INSTALL.md`/`README.md` for the complete set) → Knuckles
(PR to main, merge).

**Now (2026-09-18, post-Tails fixes): all 15 review findings resolved; 3 re-verifications remain.**
Tails fixed every open finding: Shadow 8 (blocker `459ac30`; superseded RPMs +
`gdk-pixbuf-parsers` source rebuild `4c9f7c2`; `ukey.c` Super→META, `cinnamon.spec` comment,
parity `gget()`, 3.1/3.2 evidence `55e37bd`/`2fa1b2d`), Omega 4 (license files + `%license` on
all six specs, `Requires: python3-webencodings`, `--no-build-isolation` + BuildRequires, dead
URLs), Big T1–T3 (`run-tests.sh` exit codes, dead Phase 2 deleted, the 22-package set encoded in
`vm-test/install-set.txt`). Every `## Review`/`## Security` finding carries a `**Resolution:**`
line; branch pushed to `2fa1b2d`. Remaining, all assigned Tails: (A) clean-checkout rebuild
reproduces the published set, (B) `run-tests.sh` end-to-end on a fresh VM (also proves the META
mapping via a `ukey key Super_L` menu open), (C) enforcing-SELinux smoke. Then Vector
(`INSTALL.md`/`README.md` for the complete set) → Knuckles (PR to main, merge).

**DONE (2026-09-19, Robotnik).** All 17 `## Definition of Done` boxes ticked against the recorded
evidence. PR #4 merged to `metalllinux/cinnamon-for-rocky10` main via rebase (`3375a05`, tree
byte-identical to the reviewed tip `9848143`). The desktop is a complete 6.7 set: 64 RPMs, 22-name
install set, single-dnf install, GDM Wayland login, 11/11 parity vs the Fedora Cinnamon reference,
three recorded deviations (gnome-terminal 3.54.5 vs ref 3.60.0; Rocky logo, time-based sky,
Adwaita GTK branding). Open follow-ups, not task failures: `gdm_wait_session` logind visibility
lag (harness); greeter sufficiency of bare `dnf install gdm` (docs gap); the `vm-test/parity/`
baseline is the standing acceptance bar for future sessions. Remaining: Espio prunes this doc.

**Now (2026-09-19, post-Vector): docs leg complete.** `INSTALL.md` + `README.md` rewritten for
the final state (64 RPMs, 22-name install set, single-dnf install, GDM Wayland, 11/11 parity,
deviation table, troubleshooting). Project `9848143` on the feature branch (unpushed), planning
`03d20d8` on main (unpushed) — both pushes go to Knuckles with the PR. One bounded doc gap
recorded in `## Docs` (greeter sufficiency of bare `dnf install gdm` unverified; docs use the
verified gdm + gnome-shell env). Chain state: only Knuckles remains (PR + merge), then Espio
prunes this doc.

**Now (2026-09-19): review fixes complete (Tails) — all 15 findings closed; re-verifications A/B/C PASS.**
`spec/` is canonical for every published RPM (provenance blocks: upstream commit by full tree diff,
fetchable by-SHA ref, tarball sha256); all five fixable RPMs ship their license files (`%license`
verified, the LGPL §4 obligation for `gdk-pixbuf-parsers` met); `tinycss2` Requires fixed; dead
URLs fixed; `rpms/` republished to exactly the published set (64 RPMs); 3.1/3.2 evidence
committed; `ukey.c` Super→`KEY_LEFTMETA` (commit `55e37bd`, proven end-to-end — `Super_L` opens
the main menu); `run-tests.sh` install-rc gate + dead Phase 2 removed + `install-set.txt` encodes
the 22-package set. Re-verifications: **A** clean-checkout rebuild reproduces the published set;
**B** fresh VM `t17-revB` (192.168.122.18) — single-dnf install of all 64 RPMs on attempt 1,
22/22 verified, GDM Wayland login, five surfaces; **C** enforcing-SELinux — five surfaces PASS,
**zero AVC denials**. Project `d128848`, planning `e765e67`. One recorded observation (not a
defect, open as a follow-up): `gdm_wait_session` can report a timeout when logind visibility
lags right after session creation. The Tails leg is done. Chain continues: Vector → Knuckles.

**Now (2026-09-18, post-trio): review chain 3/3 complete — Big adds 3 findings; merge gate set.**
Trio close in `## Test Results`: **T1 (should-fix)** `run-tests.sh` swallows install/verify exit
codes (a fully failed install exits 0); **T2 (low)** Phase 2 is structurally dead (resolvable
only from the local repo; dnf atomicity + `|| echo WARNING`); **T3 (low)** the accepted
22-package install set is encoded nowhere and `INSTALL.md` documents the 14-package era.
One-liner **PASS**: the old standalone `cinnamon-settings` RPM is absent (settings bundled in
`cinnamon-6.7.4-3.el10`). Verdict: **mergeable after Tails** resolves Shadow's blocker + T1 and
runs the two mandatory re-verifications (clean-checkout rebuild reproduces the published set;
`run-tests.sh` end-to-end on a fresh VM; enforcing-SELinux smoke). Host note: `libvirtd` had gone
inactive; Big restored it (enabled + running, all persistent domains back up). Total open for
Tails: Shadow 8 + Omega 4 + Big 3 = 15 findings (1 blocker, 6 should-fix/medium, 8 low/nit).

**Now (2026-09-18, post-Omega): review chain 2/3 complete — Omega adds 4 findings.**
License tags all correct at exact upstream tags; no secrets, no injection surface. **1 medium**:
six new RPMs ship without a license file (the pip-based specs never copy the sdist LICENSE, no
`%license` line; for `gdk-pixbuf-parsers` this is an actual LGPL-2.1 §4 distribution obligation).
**3 low**: `python3-tinycss2.spec` omits `Requires: python3-webencodings` (dist-info metadata is
not parsed into RPM Requires — clean-install breakage of the settings theme panel); PEP 517 build
isolation fetches unpinned build backends from PyPI at rpmbuild time (fix:
`--no-build-isolation` + BuildRequires); two dead spec URLs (provenance only). Full numbered list
in `## Security`. Total open for Tails after the trio: Shadow 8 (1 blocker) + Omega 4. Next: Big
(trio close + the settings-RPM one-liner) → Tails fixes.

**Now (2026-09-18, post-Shadow): review chain 1/3 complete — 8 findings (1 blocker).**
Shadow reviewed the full feature-branch diff: **1 blocker** (the repo `spec/` cannot reproduce the
shipped `nemo`/`gtk-layer-shell`/`cinnamon-settings-daemon` RPMs — repo specs are stale
1.el10/missing; the published 2.el10 builds came from the host's `~/rpmbuild/SPECS/`, which is not
in the branch; clean-checkout rebuild would resurrect the wallpaper defect and the 3.1/3.2 verdicts
are not reproducible), **4 should-fix** (3.1/3.2 acceptance evidence untracked in the branch;
`ukey.c` maps Super_L/R to Control keycodes — a landmine; 7 superseded 1.el10 RPMs still in
`rpms/` incl. known-broken `cinnamon-desktop-6.7.2-1`; `gdk-pixbuf-parsers` built from a
gitignored URL-less tarball), **3 nits** (comment count, missing `%postun`, a
`parity-inventory.sh` misdiagnosis). Clean areas stated plainly. Full numbered findings in `##
Review`. Merge is blocked until Tails resolves the blocker + should-fixes. Next: Omega → Big →
Tails fixes.

**Now (2026-09-18): items 3.1 + 3.2 complete (Big) — end-to-end + parity PASS.**
Fresh VM `task0017-fresh-vm` (192.168.122.153), clean Rocky 10, full set installed with **one**
`dnf install` of 22 runtime names — zero manual steps (wallpapers, branding, and the Python deps
all auto-pulled via the dependency chain). 3.1: **5/5 PASS** (panel, wallpaper render day/night,
terminal, control-center, main menu). 3.2: **11/11 PASS** vs the 0.3 Fedora ref baseline — both
prior FAILs closed by the 67-RPM set; remaining ref differences are the intentional branding
divergences (Rocky logo, time-based sky, Adwaita GTK). DoD boxes "Host-VM end-to-end" and
"parity" are satisfied. Two harness notes (not defects): Cinnamon shell a11y tree keeps
menu/panel nodes latent (pixels are the proof); menu didn't dismiss via ukey in this build.
Open one-liner for the packaging story: confirm the old separate `cinnamon-settings` RPM is
absent on the release VM. Remaining: review trio → Vector → Knuckles.

**Now (2026-09-17, post-harness): harness fix complete (Tails).** The `gdm-a11y.py` app selector
is now the `A11Y_APP` env var (default `gnome-shell`, greeter behaviour byte-identical) with a
separator-tolerant fallback for GApplication ids (`org.gnome.Terminal`). Verified live on
`gdm-login-vm`. Project `eafa476`, planning `2aa6b09`, pushed. 3.1 unblocked. Prerequisite
recorded: set `toolkit-accessibility=true` on the fresh VM before any a11y wait. All build-side
work for the task is done — the remaining chain is Big 3.1/3.2 → review trio → Vector →
Knuckles.

**Now (2026-09-17, post-1.4): item 1.4 complete (Tails) — all build items done.**
`gnome-terminal-3.54.5-1.el10` (newest VTE-compatible; deviation recorded) built from the
official tarball, sha256-verified, closure exact. Repo at 67 RPMs; `run-tests.sh` EXPECTED list
updated. Live open on `gdm-login-vm` **PASS** (AT-SPI tree shows the Terminal frame + VTE surface
+ rendered prompt; screenshot in `vm-test/parity/`). Project `20f8648`, planning `1c119e6`,
both pushed. Flagged for the harness: `gdm-a11y.py` hard-filters the app node name
`gnome-shell`, so its tree/text/has/wait commands see nothing in a Cinnamon session — needs the
app name parameterised (e.g. `A11Y_APP` env) before 3.1's a11y waits on the terminal. Remaining
open work: Tails harness fix → Big 3.1 fresh-VM end-to-end + 3.2 parity run → review trio →
Vector → Knuckles.

**Now (2026-09-17, 1.4 turn 1): item 1.4 chain gate PASS (Tails).** The EL10 dependency chain for
gnome-terminal exists in the official repos (no konsole/xterm contingency). The plan's gtk4
assumption was wrong: the ref terminal (3.60.0) is **GTK3 + libhandy1 + VTE 2.91**. Version
decision: build **3.54.5** (newest compatible with EL10's vte291 0.78.6; the ref's 3.60.0 needs
vte >= 0.79.90) — version delta vs ref recorded as a deviation. Full closure verified present.
Commit `65b86a6`. Session ended after turn 1 (32k discipline); spec + rpmbuild + republish + live
verification are the next turns (Tails session resumed).

**Now (2026-09-17, post-control-center): control-center FAIL fixed (Tails).** Five Python RPMs
source-built at the Fedora ref's versions (`setproctitle` 1.3.7, `pillow` 12.3.0, `tinycss2`
1.5.1, `webencodings` 0.5.1, `xapp` 3.0.2); `cinnamon` bumped to `3.el10` with `Requires:` for
all settings-app modules. Repo re-published (64 RPMs). Verified on `gdm-login-vm`: default,
themes, and backgrounds panels run with empty logs; setproctitle title confirmed in `ps`. Project
commit `5583e94` on `feature/TASK-0017-cinnamon-desktop-completeness`, planning doc `a613f1b`.
Remaining parity FAIL before 3.1: terminal (item 1.4). Next: Tails 1.4 → Big 3.1 fresh-VM
end-to-end.

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

- [x] **Complete package set.** (Plan verdict: no missing monorepo subpackages at 6.7 —
      applets/desklets/settings/menu/themes ship in the shell RPM, screensaver folded into
      `cinnamon`; delta = 2 system packages + new RPMs.) Set built, published (64 RPMs), documented
      (`vm-test/install-set.txt`, `INSTALL.md`); 22/22 verified on fresh VMs 3.1 + rev B.
- [x] **Terminal.** gnome-terminal 3.54.5 in the set; opens from the Cinnamon session (1.4 live
      open PASS, 3.1, rev B, parity row 10). Version deviation vs ref 3.60.0 recorded.
- [x] **Wallpaper.** Rocky Gemstone Skies set automatically on first login; renders (day/night
      variants) — 2.1 black-desktop defect fixed (`cinnamon-desktop` 6.7.2-2 patch +
      `gdk-pixbuf-parsers`), re-verified 2.2/3.1/rev B+C.
- [x] **Branding.** Rocky logo on the panel menu button (2.1 render PASS, 3.1, parity row).
- [x] **Applets load.** 8 default applets present, panel renders, no missing/erroring applets
      (3.1, parity row 1).
- [x] **Themes load.** Themes ship in the `cinnamon` shell package (A4 inventory, 818 files);
      default theme applies at login; selectable in the theme selector (3.2 parity row).
- [x] **Extensions work.** Applet/desklet/extension manager functional, lists shipped items (3.2
      parity row; ref-side manager capture 0.3).
- [x] **Settings menu.** Cinnamon Settings menu present, opens control-center (3.1, parity row 7;
      the 2.2 crash closed by the five Python RPMs + `Requires:`).
- [x] **File manager still works.** nemo opens and functions (3.2 parity row; nemo 6.7.4-2).
- [x] **VM end-to-end.** Fresh minimal Rocky 10.2 VM, complete set, GDM Wayland login, every item
      above verified — 3.1: 5/5 PASS on `task0017-fresh-vm` (`## Test Results` +
      `vm-test/evidence/task0017-fresh-3.1/`).
- [x] **Host-VM end-to-end (supersedes the bare-metal box; `192.168.1.103` is no longer
      available for testing, user 2026-09-14).** All runs above are on VMs on host
      `192.168.1.102`; additionally rev B (fresh VM `t17-revB`, single-dnf all 64 RPMs, 22/22)
      and rev C (enforcing-SELinux five surfaces, zero AVC denials) PASS.
- [x] **Desktop feature parity vs the Fedora reference.** 11-row checklist (panel applets,
      wallpaper, themes, screensaver, main menu, nemo, terminal, settings, session/power,
      extension manager) PASS/FAIL on both sides with evidence — **11/11 PASS** (3.2 vs the 0.3
      baseline). Gaps closed: terminal, settings. Deviations recorded: gnome-terminal 3.54.5 vs
      3.60.0, three intentional branding divergences (Rocky logo, time-based sky, Adwaita GTK).
- [x] `Shadow`: no unresolved blockers or should-fix findings in `## Review` (all 8 carry
      `**Resolution:**` lines, 2026-09-18/19).
- [x] `Omega`: no unresolved findings above `low` in `## Security` (medium + 3 low all closed).
- [x] `Big`: all harness checks PASS, no silently dropped checks (3.1/3.2, rev A/B/C; the T1
      exit-code swallow fixed so failures can no longer be silent).
- [x] `Vector`: `INSTALL.md`/`README.md` updated to describe the complete set (`9848143`;
      TASK-0016 coordination: its INSTALL.md verification now targets this set).
- [x] `Knuckles`: merged to `metalllinux/cinnamon-for-rocky10` main via PR #4 (rebase merge
      `3375a05`, tree byte-identical to the reviewed branch tip `9848143`).

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
- [x] `Tails` (2026-09-17): control-center dep fix — 5 Python RPMs source-built at ref versions,
      `cinnamon` 3.el10 with `Requires:`, repo at 64 RPMs, verified live on `gdm-login-vm`
      (empty logs, screenshots). Project `5583e94` (feature branch).
- [x] `Tails` (2026-09-17): plan item 1.4 — gnome-terminal 3.54.5 built + published (67 RPMs) +
      live open PASS on `gdm-login-vm` (AT-SPI + rendered prompt). Project `20f8648`, planning
      `1c119e6`.
- [x] `Tails` (2026-09-17): harness fix — `A11Y_APP` env var in `tasks/lib/gdm-a11y.py` (default
      `gnome-shell`, separator-tolerant fallback), verified live. Project `eafa476`.
- [x] `Big` (2026-09-18): plan items 3.1 + 3.2 — fresh VM `task0017-fresh-vm`, single-dnf full-set
      install (zero manual steps), 3.1 5/5 PASS, 3.2 parity matrix **11/11 PASS** vs ref. DoD
      Host-VM + parity boxes satisfied. Evidence in `## Test Results` +
      `vm-test/evidence/task0017-fresh-3.1/` + `vm-test/parity/rocky10/2026-09-18-3.2/`.
- [x] `Big` (2026-09-18, folded into trio close): one-liner on `task0017-fresh-vm` —
      `rpm -qa | grep cinnamon-settings` matches only `cinnamon-settings-daemon` (substring);
      `rpm -q cinnamon-settings` → "package cinnamon-settings is not installed" (exit 1). Old
      separate settings RPM absent. Recorded in `## Test Results` (trio close).
- [x] `Shadow` (2026-09-18): feature-branch review — 8 findings (1 blocker: repo specs can't
      reproduce the shipped nemo/gtk-layer-shell/cinnamon-settings-daemon RPMs; 4 should-fix; 3
      nits). Full numbered list in `## Review`.
- [x] `Omega` (2026-09-18): security review — 4 findings (1 medium: six RPMs ship without a
      license file, LGPL §4 obligation for gdk-pixbuf-parsers; 3 low: missing
      `Requires: python3-webencodings`, PEP 517 unpinned backends, two dead spec URLs). License
      tags verified correct; no secrets/injection. Full list in `## Security`.
- [x] `Big` (2026-09-18): review trio closed — test-execution review + one-liner in `## Test
      Results` (trio close entry): 3 new findings (T1 should-fix: `run-tests.sh` exit-code
      swallowing; T2 low: dead Phase 2; T3 low: install set not encoded, `INSTALL.md` stale),
      0 blockers, 0 in product RPMs. Mergeable after Tails resolves Shadow's blocker + T1 and
      runs the two re-verifications (run-tests.sh end-to-end; enforcing-SELinux smoke).
- [x] `Tails` (2026-09-18): all 15 review findings fixed — Shadow 8 (blocker: spec/ canonical
      incl. nemo/gtk-layer-shell/cinnamon-settings-daemon in `459ac30`; superseded 1.el10 RPMs +
      gdk-pixbuf-parsers source rebuild in `4c9f7c2`; ukey.c Super→META + cinnamon.spec comment +
      parity `gget()` in `55e37bd`; 3.1/3.2 evidence committed in `2fa1b2d`), Omega 4 (license
      files + `%license` on all six specs, `Requires: python3-webencodings`, `--no-build-isolation`
      + BuildRequires, dead URLs — `459ac30`/`4c9f7c2`), Big T1–T3 (exit codes, dead Phase 2,
      `vm-test/install-set.txt` 22-package set — `55e37bd`). Every `## Review`/`## Security`
      finding now carries a `**Resolution:**` line. Branch pushed to `2fa1b2d`.
- [x] `Tails` (2026-09-19): re-verification A — clean-checkout rebuild **PASS**: all 10 changed
      specs build RC 0 from a fresh clone at `2fa1b2d`; NVRs + subpackage sets match `rpms/`
      exactly; payloads byte-identical modulo build-environment artifacts (LTO stream symbol
      hashes -> build-ids/.gnu_debugdata, pip direct_url build paths). Detail in `##
      Implementation` (entry of 2026-09-19).
- [x] `Tails` (2026-09-19): re-verifications B + C from `## Test Results` (trio close) —
      **both PASS** on fresh VM `t17-revB`: (B) `run-tests.sh` end-to-end (single-dnf install
      of all 64 RPMs, 22/22 names verified, GDM login, `ukey key Super_L` opens the main menu —
      META mapping proven end-to-end), (C) enforcing-SELinux smoke (boot enforcing, GDM login,
      five surfaces, zero AVC denials). Detail in `## Test Results` (entry of 2026-09-19);
      evidence in project `d128848`.
- [x] `Vector` (2026-09-19): `INSTALL.md` + `README.md` updated for the final state (64 RPMs,
      22-name install set per `vm-test/install-set.txt`, single-dnf install, GDM Wayland, 11/11
      parity + 3 branding divergences, deviation table, troubleshooting). Project `9848143`
      (feature branch, **not pushed** — left for Knuckles); planning `03d20d8` (main, not pushed).
      One bounded gap recorded in `## Docs`: `dnf install gdm` alone as greeter sufficiency not
      independently verified (docs use the verified gdm + gnome-shell test env).
- [x] `Knuckles` (2026-09-19): branch pushed to `9848143`; PR #4
      (`metalllinux/cinnamon-for-rocky10`) opened against `main` at `c1de933` and merged via
      rebase; `main` advanced to `3375a05` with the tree identical to the reviewed branch tip;
      team-chaotix planning `main` pushed. Release record in `## Release`.
- [x] `Espio` (2026-09-19): prune this doc — superseded plan, resolved-finding detail, and
      narration moved to `## Archive`; every decision, verified fact, deviation, and the final
      state kept; `## Status`/`## Definition of Done`/`## Release` intact.

---

## Plan

*Owner: `Amy`. Written 2026-09-15. Plan executed and task closed 2026-09-19 (PR #4 merged, `main`
at `3375a05`). Full plan text preserved in `## Archive` under
`### Superseded plan (2026-09-15, Amy)`.*

**Key decisions** (evidence in `## Implementation` and `## Test Results`):

- Icon (1.2): reference installed `fedora-logo-icon` hicolor entry (option A) over copying
  `rocky-logo.svg` (option B); gschema override sets `app-menu-icon-name` and `system-icon` to
  `fedora-logo-icon`; `Requires: rocky-logos`; license safety.
- Wallpaper override (1.2): flat dconf keyfile in `/etc/dconf/db/local.d/` + explicit
  `dconf update` in `%post`/`%postun`, not the plan's `/usr/share/dconf/db.local.d/readonly/`
  path (dead in dconf 0.40); `picture-uri` only, `org.cinnamon.desktop.background`, value
  `file:///usr/share/backgrounds/rocky-default-10-gemstone-skies-time.xml`.
- Wallpaper render fix (2.1): root cause in `gnome-bg` image branch (`pixbuf` cairo surface not
  compositing on gtk-layer-shell/Wayland); fixed by `gnome-bg-wayland-surface.patch`, rebuilt
  `cinnamon-desktop-6.7.2-2.el10`, new `gdk-pixbuf-parsers` RPM.
- Terminal (1.4): source-build `gnome-terminal`; 1-pager
  `planning/decisions/TASK-0017-terminal-choice.md`.
- Install set: 22 runtime names in `vm-test/install-set.txt`; includes both `rocky-backgrounds`
  and `rocky-logos` (1.2 cross-item correction).
- Parity: 11/11 PASS vs `fedora-cinnamon-ref` (item 3.2, `## Test Results`).

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

**Item 1.4, turn 1 (2026-09-17, Tails): EL10 dependency-chain verification. Verdict: chain PASSES; build gnome-terminal 3.54.5 from source. Konsole/xterm fallback not triggered.**
The ref's version 3.60.0 is installable on EL10 only if the VTE floor is met, and it is not: ref
Requires `vte291(x86-64) >= 0.79.90`, EL10 ships vte291 0.78.6. The newest upstream release whose
meson vte floor fits 0.78.6 is **3.54.5** (floor 0.78.0). Every other runtime and build dependency
of 3.54.5 is present in the EL10 repos (versions below). Upstream license for 3.54.5 is
GPL-3.0-or-later (programme); it ships as a standalone RPM, no relicense, no merge into the GPL-2.0
Cinnamon tree, so no license conflict.

Ref stack (live on `ref-overlay-task0017`, 192.168.122.85, as `howard`):
- `rpm -q --requires gnome-terminal`: 3.60.0-1.fc44 requires gtk3 >= 3.24.0, libhandy >= 1.6.0
  (`libhandy-1.so.0`), `vte291(x86-64) >= 0.79.90` (`libvte-2.91.so.0`), glib2 >= 2.52,
  gsettings-desktop-schemas, dbus, libX11, libcairo, libuuid, pango.
- `ldd /usr/libexec/gnome-terminal-server`: `libgtk-3.so.0`, `libhandy-1.so.0`,
  `libvte-2.91.so.0`. **Correction to plan item 1.4: the ref terminal is GTK3 + libhandy1 + VTE 2.91,
  not gtk4** (the plan's "gtk4, VTE" assumption is wrong; a gtk4 stack was never needed).
- Ref VTE runtime is 0.84.1 (python3 gi `Vte.MAJOR/MINOR/MICRO` probe).

Version selection. vte floors read from `meson.build` of each tag, fetched 2026-09-17 from
`https://raw.githubusercontent.com/GNOME/gnome-terminal/<tag>/meson.build`:

| tag | vte-2.91 floor | verdict |
|---|---|---|
| 3.60.0 (ref) | 0.79.90 (ref rpm Requires) | incompatible |
| 3.56.3 | 0.80.0 | incompatible |
| **3.54.5** | **0.78.0** | **chosen, newest compatible** |
| 3.52.4 | 0.76.0 | compatible, superseded |
| 3.50.1 | 0.74.0 | compatible, superseded |
| 3.48.3 | 0.72.2 | compatible, superseded |

Tags 3.58.x, 3.59.90, 3.97.0 postdate 3.56.3, so their floors are >= 0.80 and they are excluded
without individual fetch. (3.97.0 is an unexplained tag name at commit `204c243`; irrelevant since
any post-3.56.3 floor fails on EL10.) 3.48.3 has no libhandy requirement at all; 3.50+ do
(floor 1.6.0, EL10 has 1.8.3).

EL10 closure (host `shadow`, `dnf --assumeno --disablerepo='nxadm-pkgs-rakudo-pkg*' repoquery
--qf '%{name} %{version}-%{release} (%{reponame})'`, run 2026-09-17):
- Runtime: vte291 0.78.6-1.el10 (appstream), gtk3 3.24.43-5.el10 (appstream), glib2
  2.80.4-12.el10_2.22 (baseos), libhandy 1.8.3-4.el10 (appstream), pcre2 10.44-1.el10.3 (baseos),
  gsettings-desktop-schemas 47.1-4.el10 (baseos), libuuid 2.40.2-18.el10 (appstream),
  libX11 1.8.10-1.el10 (appstream), dbus 1.14.10-5.el10 (baseos).
- Build: meson 1.4.1-5.el10 (crb; floor 0.62.0), ninja-build 1.11.1-9.el10 (crb),
  gettext 0.22.5-6.el10 (baseos), gcc 14 (gnu++14, floor 4.8.1), glib2-devel 2.80.4-12.el10_2.22
  (appstream), gtk3-devel 3.24.43-5.el10 (appstream), libhandy-devel 1.8.3-4.el10 (crb),
  vte291-devel 0.78.6-1.el10 (crb), pcre2-devel 10.44-1.el10.3 (appstream),
  libuuid-devel 2.40.2-18.el10 (appstream), libX11-devel 1.8.10-1.el10 (appstream).
- `dnf repoquery gnome-terminal` returned nothing across all enabled repos (baseos, appstream,
  crb, epel, local). **gnome-terminal is in no EL10 repo**; source-build is the only path, which
  confirms the decision 1-pager Option A.
- `dnf repoquery --whatprovides 'pkgconfig(x11)'` → `libX11-devel` 1.8.10-1.el10 (appstream).
  There is no `xorg-x11-devel` package on EL10; meson's `dependency('x11')` resolves through that
  pkgconfig, so the BuildRequires line is `libX11-devel`.

Spec-turn notes carried from this verification:
- 3.54.5 meson also runs `find_program('glib-compile-schemas')` (provided by glib2-devel, present)
  and `find_program('xsltproc')` (libxslt; confirm present on the build turn).
- `get_option('nautilus_extension')` gates `libnautilus-extension-4`. Disable it in the spec; our
  file manager is nemo (libnemo-extension API), not GNOME Nautilus. Check the option default in
  `meson_options.txt` when the tarball lands.
- Pass `-Ddocs=false`. Help would pull the gtk-doc/itstool/yelp toolchain and help is not in the
  parity matrix.
- meson defines `GLIB_VERSION_MAX_ALLOWED=2.68` against EL10's glib 2.80.4. That is a compile-time
  define; 3.54-era code predates the newer APIs, so no action.
- Version delta vs ref (3.54.5 vs 3.60.0) is the recorded deviation. The parity row is "terminal
  opens and renders input in a live Cinnamon session", not package-version equality.

Host note, out of scope for this item: the host dnf config carries a broken repo
`nxadm-pkgs-rakudo-pkg` (cloudsmith; `repomd.xml GPG signature verification error: Signing key not
found`). All queries above ran with `--disablerepo='nxadm-pkgs-rakudo-pkg*'`.

Next (turn 2): fetch `https://download.gnome.org/sources/gnome-terminal/3.54/gnome-terminal-3.54.5.tar.xz`
plus the published `.sha256` (verify before use), write `spec/gnome-terminal.spec` (Requires per the
runtime list above; BuildRequires per the build list plus libxslt), rpmbuild, then `rpm -q
--requires` and payload check.

---

**Item 1.4, build turn (2026-09-17; project commit `34e479b` on
`feature/TASK-0017-cinnamon-desktop-completeness`).**
Built `gnome-terminal-3.54.5-1.el10.x86_64` (+`-debuginfo`, +`-debugsource`) from
`https://download.gnome.org/sources/gnome-terminal/3.54/gnome-terminal-3.54.5.tar.xz` (1.9 MiB).
sha256 `132699f818341779c8aa9c0d049b778cbc6f82c1c37a17530354a47049962551`, verified with
`sha256sum -c` against the published `.sha256sum`. Fetch note: `download.gnome.org` (CDN77-Turbo)
returns 404 to `curl` GET but 200 to HEAD and `wget`; the tarball was fetched with `wget`. Host state
change (flagged): installed build deps on `shadow` via `sudo -n dnf install -y libhandy-devel
vte291-devel gsettings-desktop-schemas-devel` (passwordless sudo). The `gsettings-desktop-schemas.pc`
pkgconfig lives in `gsettings-desktop-schemas-devel`, not the runtime package
(`dnf repoquery --whatprovides 'pkgconfig(gsettings-desktop-schemas)'`).

Spec: `spec/gnome-terminal.spec`, house style per `python3-xapp.spec`/`nemo.spec` (bare-filename
`Source0` + dated sha256 comment; changelog `* Thu Sep 17 2026 Team Chaotix <chaotix@metallinux.dev>
- 3.54.5-1.el10`). `License: GPLv3+ AND GFDL-1.3-only` (programme GPLv3+; both installed appstream
metainfo files are GFDL-1.3-only). No `.so` shipped (nautilus extension off), so no `%post` ldconfig.

Meson config: `-Dprefix=/usr -Dlibdir=%{_libdir} -Dnautilus_extension=false -Ddocs=false
--wrap-mode=nodownload`; `search_provider` left at its default true (inert data on Cinnamon, preserves
ref parity). Built with explicit `meson setup build` + `ninja -C build` + `DESTDIR=%{buildroot} ninja
-C build install` (xapp house pattern) because the EL10 `%meson`/`%ninja_build` macro pair is
inconsistent: `%meson` configures into `redhat-linux-build/` but `%ninja_build` runs ninja in the
source dir. `vte.wrap` is fallback-only; the system `vte291-devel` 0.78.6 was used.

Payload (verified `find BUILDROOT` + `rpm -qlp`): `%{_bindir}/gnome-terminal`,
`%{_libexecdir}/gnome-terminal-server`, `%{_libexecdir}/gnome-terminal-preferences`,
`%{_prefix}/lib/systemd/user/gnome-terminal-server.service`, `%{_libdir}/gnome-terminal/gschemas.compiled`,
both desktop files, the `xdg-terminals` symlink, `dbus-1/services/org.gnome.Terminal.service`, the
gschema, the search-provider ini, 4 hicolor icons (scalable + symbolic apps), both metainfo files
(`org.gnome.Terminal` and `.Nautilus` variants; the install rule keeps both), 98 locale `.mo` files via
`%find_lang --with-gnome`, `README.md` doc, `COPYING` + `COPYING.GFDL`. D-Bus interface XMLs are
gdbus codegen inputs only and are not installed.

`rpm -q --requires` on the built RPM matches the turn-1 runtime closure exactly: dbus, glib2 >= 2.52.0,
gsettings-desktop-schemas, gtk3 >= 3.22.27, libX11, libhandy >= 1.6.0, libuuid, pcre2, vte291 >= 0.78.0,
plus the NEEDED `.so.0` symbols (all present in the verified EL10 closure). Note: no `libpcre2-8.so.0`
DT_NEEDED appears in the aggregate requires (pcre2 is used only in the server binary path); the explicit
`Requires: pcre2` covers runtime availability.

Build gotchas hit and fixed this turn: (1) missing `%prep`/`%setup -q` made meson setup fail with
"meson.build not found"; (2) the explicit meson line initially omitted `-Dprefix=/usr`, so the payload
landed under `/usr/local/` (meson's default prefix) and every runtime file was "File not found" in
BUILDROOT; (3) RPM expands macros even inside comments, so comments naming `%meson`/`%ninja_build`
spliced macro bodies into the build script, and one left a "Macro expanded in comment" warning; all
rephrased; (4) the systemd user unit installs to hardcoded `prefix/lib/systemd/user` (upstream comment:
"this is what systemd uses"), not `%{_libdir}`; EL10's unitdir macro is `/usr/lib/systemd/system` and
cannot be used for user units, so the spec lists the explicit path.

Repo + harness integration (in commit `34e479b`): the three RPMs were copied to `rpms/` (65 to 68
files; the house repo publishes debuginfo too), and `vm-test/run-tests.sh` gained `gnome-terminal` in
the `EXPECTED` list and `rocky-backgrounds` + `rocky-logos` in the phase-2 system-deps dnf list (the
turn-1 note's placement of the item-1.2 wallpaper packages; both are in baseos). The `SYSTEM_DEPS`
array in that script is dead code (declared, never consumed); the inline remote dnf list is the live
one and is what was edited.

Next (turn 3): republish the local repo (delete `repodata/` first, per R7), install on `gdm-login-vm`,
open the terminal from a live Cinnamon session, capture `sudo virsh screenshot` evidence, and record
the verification result here.

---

**Item 1.4, verification turn (2026-09-17; project commit `20f8648`).**
Live-session verification on `gdm-login-vm` (192.168.122.15; session user `gdmtest`, uid 1000,
graphical session 426 on seat0/tty2) — **PASS**: the terminal opens in a live Cinnamon session and
renders input; the window and the VTE surface are on-screen.

Step 1, repo re-publish (host): `rm -rf rpms/repodata && createrepo_c .` in `rpms/` → 67 RPMs in
the published set; `dnf --assumeno makecache --disablerepo='*' --enablerepo=cinnamon-rocky10` →
"Metadata cache created"; `dnf --assumeno repoquery --disablerepo='*' --enablerepo=cinnamon-rocky10
gnome-terminal` → `gnome-terminal-0:3.54.5-1.el10.x86_64`. `rpms/repodata/` is gitignored
(house `.gitignore`), so the re-publish carries no repo commit.

Step 2, install from the repo (VM, root over the pinned harness channel, `~/.ssh/cinnamon-test-key`
+ per-VM pin file, `HostKeyAlias=gdm-login-vm`): `rsync -a --delete rpms/ → /root/rpms/` (217M,
idempotent) plus `repo-setup/ → /root/repo-setup/`; on the VM `rm -rf /root/rpms/repodata && bash
/root/repo-setup/setup-repo.sh /root` (house 1.2 pattern, `file:///root/rpms`); VM `dnf --assumeno
repoquery --disablerepo='*' --enablerepo=cinnamon-rocky10 gnome-terminal` → resolves; `dnf -y
install gnome-terminal` → installed `gnome-terminal-3.54.5-1.el10.x86_64`, auto-pulling
`vte291-0.78.6-1.el10`, `libhandy-1.8.3-4.el10`, `vte-profile-0.78.6-1.el10` from the Rocky repos
(the exact turn-1 closure); `gnome-terminal --version` → "GNOME Terminal 3.54.5 using VTE 0.78.6
+BIDI +GNUTLS +ICU +SYSTEMD".

Step 3, live open (VM): launched inside the `gdmtest` session with
`runuser -u gdmtest -- env XDG_RUNTIME_DIR=/run/user/1000 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus
DISPLAY=:0 WAYLAND_DISPLAY=wayland-0 gnome-terminal`; `gnome-terminal-server` runs as `gdmtest`
(pid 47530). Screenshot: `sudo virsh screenshot gdm-login-vm` →
`vm-test/parity/rocky10/2026-09-17-1.4-01-terminal-live-open.png` (working copy in the gitignored
`vm-test/results/`).

Primary evidence is the AT-SPI tree (this model cannot view PNGs, and the a11y tree is the harness's
standard text observation channel): the session's a11y desktop (`/run/user/1000/at-spi/bus_0`)
enumerates the app nodes `cinnamon`, `nemo-desktop`, `csd-*`, … and `org.gnome.Terminal`; the
terminal subtree is `[application] 'org.gnome.Terminal' → [frame] 'gdmtest@localhost:~' (0,0 708x572)`
with the header bar (Minimize/Maximize/Close), the full menu bar (File/Edit/View/Search/Terminal/
Help: New Terminal, Copy, Paste, Preferences, Find…, Full Screen, Zoom, profiles 80×24 to 132×43,
About), and `[terminal] 'Terminal' (26,85 642x458)` plus scroll bar — window and VTE surface
on-screen (extents all ≥ 0). Reading the VTE widget's AT-SPI Text interface returns the rendered
prompt `[gdmtest@localhost ~]$`. The parity row "terminal opens and renders input in a live Cinnamon
session" is met on Rocky.

Gotchas on this turn: (1) `gdm-a11y.py`'s tree/text/has/wait commands all walk `greeter_nodes()`,
which hard-filters the app node name `gnome-shell` (the greeter's shell); in the Cinnamon session the
shell app node is `cinnamon` and the terminal is a *separate* app node, so the script prints nothing
there — the terminal subtree was walked with an inline AT-SPI probe instead (no harness file changed).
**Harness gap for 3.1:** if the fresh-VM end-to-end needs a11y waits against the Cinnamon session
(terminal or any non-shell app), `greeter_nodes()` needs the app name parameterised (e.g. an
`A11Y_APP` env alongside `A11Y_USER`); as written it only sees the `gnome-shell` app. (2)
`org.gnome.desktop.interface toolkit-accessibility` was `false` in the session, so no apps registered
with at-spi (empty tree by design); it was set `true` for the observation window, the terminal was
relaunched so the server registered, and the key was restored to `false` afterwards. (3) the harness
copy under `/root/gdm-harness/` is mode 700 and unreadable to `gdmtest`; a copy was staged to
`/tmp/gdm-a11y.py` on the VM.

Item 1.4 acceptance (re-publish + dnf resolves; install from the repo on the test VM; live open with
evidence) is fully met. Nothing remains on 1.4; Big's 3.1 fresh-VM end-to-end re-runs the whole
matrix on a fresh VM through the harness, and `EXPECTED` in `run-tests.sh` now carries
`gnome-terminal` (commit `34e479b`).

---

**Harness fix: `A11Y_APP` app selector in `gdm-a11y.py` (2026-09-17; project commit `eafa476`).**
Fixed the gap flagged in the 1.4 turn-3 entry. The file is `tasks/lib/gdm-a11y.py` (the item's
`vm-test/gdm-a11y.py` path is a misnomer; it is staged to the VM as `/root/gdm-harness/gdm-a11y.py`
per `vm-test/test-gdm-login.sh:87`). The single hard filter was in `greeter_nodes()`
(`!= "gnome-shell"` on the app node name); every command (tree/text/has/wait/find/findrole/
waitvis/waitvisrole/findrolex/waitvisrolex/textof/textofext) goes through that one function, so
one change covers all of them.

Change: the selector is now the `A11Y_APP` env var, defaulting to `gnome-shell` (the exact current
behaviour). Selection is an exact app-node-name match first; when nothing matches exactly, a
case-insensitive substring match with `.` and `-` treated as equivalent separators applies. The
fallback exists because the terminal's a11y app node is named `org.gnome.Terminal` (the
GApplication id, observed in the turn-3 probe), so a pure exact match would never let
`A11Y_APP=gnome-terminal` find it; `gnome-terminal` → `gnometerminal` matches inside
`orggnometerminal`. On the greeter the default exact match always finds `gnome-shell`, so the
fallback is never consulted there and greeter behaviour is byte-identical to before. Alternatives
considered: (a) exact match only, forcing `A11Y_APP=org.gnome.Terminal` — rejected because the
brief's example form `gnome-terminal` would not work and Big would trip on it; (b) exact match
only when the env var is set, substring when unset — rejected as inconsistent semantics. A
registered-app-missing result stays an empty node list, which the wait commands already treat as
"target never appeared" (the existing Shadow-finding-9 semantics, preserved).

Verification on `gdm-login-vm` (live Cinnamon session, user `gdmtest`; the turn-3 terminal,
`gnome-terminal-server` pid 47530, still running and still a11y-registered, so no
`toolkit-accessibility` toggle was needed): updated script scp'd to `/root/gdm-harness/` and
`/tmp/` on the VM. Battery, all as `gdmtest` with `A11Y_USER=gdmtest`:
(1) `A11Y_APP=gnome-terminal tree 3` → `[application] 'org.gnome.Terminal'` → `[frame]
'gdmtest@localhost:~' @(0,0 708x572)` with header-bar buttons;
(2) `A11Y_APP=gnome-terminal has "gdmtest@localhost"` → exit 0;
(3) `A11Y_APP=gnome-terminal wait "gdmtest@localhost" 10` → exit 0 (found immediately);
(4) default (no `A11Y_APP`) `tree 2` → empty, exit 0 (unchanged in a Cinnamon session, where the
old filter also saw nothing);
(5) `A11Y_APP=cinnamon tree 2` → the shell tree (`[application] 'cinnamon'`, window 1280x800),
proving the selector works generically, not just for the terminal. A `BrokenPipeError` in check
5 is an artifact of piping the tree into `head -8` (the script kept printing after the pipe closed),
not a script defect.

Big's 3.1 can now wait on the terminal in a Cinnamon session, e.g.
`A11Y_USER=<user> A11Y_APP=gnome-terminal gdm-a11y.py waitvis "gdmtest@localhost" 30`. Note for
3.1: apps only register with at-spi when `toolkit-accessibility` is true (or the app is launched
after it is set true); on a fresh VM the harness should set the key before launching apps it wants
to wait on via a11y.

---

**Shadow blocker (spec/ canonical) + Omega medium (license files) + Omega low (tinycss2 Requires, 2 dead URLs) (done 2026-09-18, commit `459ac30` on `feature/TASK-0017-cinnamon-desktop-completeness`, pushed).**
`spec/` is now the canonical source for every published RPM. The six linuxmint specs that had
drifted from the host build specs (nemo, cinnamon-settings-daemon, cinnamon-control-center,
cinnamon-menus, cinnamon-session, xapps) are replaced by the host `~/rpmbuild/SPECS/` content that
produced the published RPMs, and `spec/gtk-layer-shell.spec` is added (host verbatim). Each of the
six carries a new provenance comment block under `Source0` recording the exact upstream commit the
build tarball was archived from, a fetchable content ref, and the build tarball's sha256.

### Problem: why the linuxmint Source0 fetches keep failing, and what the tarballs actually are
linuxmint repos have **no plain version tags** — only `<ver>-unstable` tags and
`master.<branch>` refs (`git ls-remote` / tags API, e.g. nemo has `6.7.4-unstable` but no `6.7.4`).
The host tarballs in `~/rpmbuild/SOURCES/` are **git archives of untagged commits** (top dir
`<pkg>-<ver>/`), not GitHub's by-SHA archives (top dir `<pkg>-<sha7>/`). Full-tree diff against
candidate upstream commits (differ=0, i.e. identical file sets and content) identified each:

| Package (tarball) | Upstream commit | Commit subject (date) | Fetchable content ref |
|---|---|---|---|
| nemo 6.7.4 | `932438fc4767` | "nemo-desktop: Don't crash/quit in Wayland when the monitor is removed (#3785)" (2026-07-09) | `https://github.com/linuxmint/nemo/archive/932438fc4767.tar.gz` |
| cinnamon-settings-daemon 6.7.2 | `18bb726dc21a` | "csd-xsettings-manager.c: Fix fcitx support for xwayland clients." (2026-07-12) | `https://github.com/linuxmint/cinnamon-settings-daemon/archive/18bb726dc21a.tar.gz` |
| cinnamon-menus 6.7.0 | `1142b5fb313b` (= tag `6.7.0-unstable`) | the tag itself | `https://github.com/linuxmint/cinnamon-menus/archive/refs/tags/6.7.0-unstable.tar.gz` |
| cinnamon-session 6.7.3 | `382af0f7e6df` | "csm-manager.c: Move SessionOver emission to a more common location." (2026-08-10) | `https://github.com/linuxmint/cinnamon-session/archive/382af0f7e6df.tar.gz` |
| cinnamon-control-center 6.7.2 | `acbe1b999a54` | "build: Remove desktop-file-links.py, bump meson requirement." (2026-07-27) | `https://github.com/linuxmint/cinnamon-control-center/archive/acbe1b999a54.tar.gz` |
| xapps 3.3.3 | `94a348f16ec3` | "xapp-sn-watcher: Fix capitalize() mangling non-ASCII titles." (2026-07-05) | `https://github.com/linuxmint/xapps/archive/94a348f16ec3.tar.gz` |
| gtk-layer-shell 0.10.1 | tag `v0.10.1` (exact) | — | already in the spec (URL + sha256 comment) |

All by-SHA archive URLs verified live (302 → codeload → 200, 2026-09-18). Build-tarball sha256s
(the exact bytes the published RPMs were built from): nemo
`b21be178735bfc52657d5d5fae710228913fd8be01ef4c396155221db6d50d9a`; csd
`1141da2de844de68ac6ddbd24a9cb48295c0790507e09b46ff24f1048c10cd93`; menus
`2a2243c778ef89a3600d3639e997f2bac1809250cada29b8e8aac09246330ddb`; session
`31aaa7fb84c36babaf29abc46aef7763244b7121755312277678fa5bfaeb96b8`; control-center
`c7a8c5a7e063effc4e316201c4adffad5d6d6149973f99060d839a7189cf6da5`; xapps
`efcd4b4ab9dcede1ac79b2b8c5a979a2fdc0d6ac776d27109d602b45c4d7ad86`; gtk-layer-shell
`88c3a3e0a5300532f3d368d5df64838a87f1fb85273f22d41df0a6b8d0ec59c6` (matches the fetched tag
archive byte-for-byte).

### Problem: how `%license` ships a license for a pip-installed package
Empirical test on this host's rpm 4.19.1.1 (minimal spec, `/tmp` scratch topdir, cleaned up): with
`%prep`/`%setup` present, a bare `%license LICENSE` resolves `LICENSE` from the **build dir** and
auto-installs it to `%{_datadir}/licenses/%{name}/LICENSE` in the package; without a build dir it
resolves to that buildroot path directly (error message shows the expected location). This matches
the already-published `python3-xapp` RPM, whose `rpm -qlp` shows
`/usr/share/licenses/python3-xapp/COPYING` from a bare `%license COPYING` (`spec/python3-xapp.spec:48`).
So the four pip specs need no extra install step; the webencodings spec (sdist ships no license)
places the vendored file in the build dir in `%prep`.

### Omega license fixes (per sdist, verified by `tar tzf` on `~/rpmbuild/SOURCES/`)
- `tinycss2-1.5.1/LICENSE` at sdist root → `%license LICENSE`.
- `setproctitle-1.3.7/LICENSE` at sdist root → `%license LICENSE`.
- `pillow-12.3.0/LICENSE` at sdist root → `%license LICENSE`.
- `webencodings-0.5.1` sdist has **no** license file → new `Source1: webencodings-LICENSE`, vendored
  from `https://raw.githubusercontent.com/courtbouillon/webencodings/v0.5.1/LICENSE` (fetched
  2026-09-18, sha256 `f23bae6ada76095610a77137fb92aec7342723900211c5826d54b4c57907ca56`, 1490 B,
  BSD, "Copyright (c) 2012 by Simon Sapin"), tracked in `spec/` (same house pattern as
  `known_failures.txt` + the patches), `install`ed into the build dir in `%prep`, shipped via
  `%license LICENSE`.
- `cinnamon-rocky-defaults` (no sdist at all) → new `Source0: GPLv2.txt`, byte-identical to the
  repo top-level `LICENSE` (sha256 `8177f97513213526df2cf6184d8ff986c675afb514d4e68a404010521b880643`),
  installed to `%{_datadir}/licenses/%{name}/LICENSE` in `%install`, shipped via `%license`.

### tinycss2 Requires + dead URLs
`python3-tinycss2` now declares `Requires: python3-webencodings`. Verified in the 1.5.1 sdist:
importing tinycss2 pulls `tinycss2/ast.py`, whose line 8 is `from webencodings import ascii_lower`
(module level); `pyproject.toml:14` declares `dependencies = ['webencodings >=0.4']`. rpmbuild does
not parse pip dist-info METADATA, so the RPM Requires had to be written by hand. Dead URLs fixed:
setproctitle `dvarrazz/python-setproctitle` (404) → `dvarrazzo/py-setproctitle` (curl 200; note the
`dvarrazzo/python-setproctitle` variant is itself 404 — the live repo is `py-setproctitle`, verified
2026-09-18); webencodings `Kozea/webencodings` (404) → `courtbouillon/webencodings` (curl 200).

### Changes (14 files, commit `459ac30`)
| File | Change | Why |
|---|---|---|
| `spec/nemo.spec` | replaced with host content + provenance block | blocker: repo spec (1.el10, no layer-shell) can't reproduce shipped 2.el10 RPM |
| `spec/cinnamon-settings-daemon.spec` | replaced with host content + provenance block | blocker (same reason) |
| `spec/cinnamon-control-center.spec` | replaced with host content + provenance block | drift (164-line class of diffs); provenance now recorded |
| `spec/cinnamon-menus.spec` | replaced with host content + provenance block | drift; provenance now recorded |
| `spec/cinnamon-session.spec` | replaced with host content + provenance block | drift; provenance now recorded |
| `spec/xapps.spec` | replaced with host content + provenance block | drift; provenance now recorded |
| `spec/gtk-layer-shell.spec` | added (host verbatim) | blocker: spec was missing entirely |
| `spec/python3-tinycss2.spec` | +`Requires: python3-webencodings`, +`%license LICENSE`, fixed install comment | Omega low + medium |
| `spec/python3-setproctitle.spec` | +`%license LICENSE`, URL fix | Omega medium + low |
| `spec/python3-webencodings.spec` | +`Source1` vendored LICENSE, +`%prep` install, +`%license LICENSE`, URL fix | Omega medium + low |
| `spec/python3-pillow.spec` | +`%license LICENSE` | Omega medium |
| `spec/cinnamon-rocky-defaults.spec` | +`Source0: GPLv2.txt`, +`%install` license step, +`%license` | Omega medium |
| `spec/webencodings-LICENSE` | added (vendor file) | webencodings sdist ships no license |
| `spec/GPLv2.txt` | added (vendor file, = repo `LICENSE`) | cinnamon-rocky-defaults has no sdist to carry the license |

### Checks run
- `rpmspec -P` (parse) on all 12 touched specs: clean. Six specs emit a pre-existing
  `warning: bogus date in %changelog` ("Sun Aug 10 2026" — 2026-08-10 is a Monday); it is in the
  host specs verbatim (and therefore in the published RPMs) and was preserved, not "fixed"
  silently.
- `rpmbuild -bs` on all 12 specs in a scratch topdir with `spec/*` + the host tarballs staged in
  SOURCES: all wrote SRPMs, i.e. source resolution works including the two new vendor files.
- Tree-diff provenance: differ=0 for all six linuxmint tarballs against the commits above (diff
  loop over candidate commits; an earlier false differ=0 came from a missing `c-$sha/` path prefix
  in the loop and was fixed before trusting results).
- `diff` of each adopted spec vs its host source: only the added comment block differs (nemo and
  menus have one trailing-whitespace normalisation each, cosmetic).

### Carried to the rebuild/republish turn (not done here)
1. Rebuild the affected packages and republish `rpms/` (still contains the 7 superseded 1.el10
   RPMs: cinnamon-desktop 6.7.2-1 main/devel/debuginfo/debugsource + csd 6.7.2-1
   main/debuginfo/debugsource, to be deleted per Shadow's should-fix).
2. Before rebuilding: copy the two new vendor files into `~/rpmbuild/SOURCES/` (house pattern —
   `spec/*` vendor files are copied manually, as `known_failures.txt` and the patches are; no
   script does it).
3. Verify each rebuilt pip RPM contains `/usr/share/licenses/<pkg>/LICENSE`
   (`rpm -qlp`).
4. Omega low (PEP517 unpinned build isolation): real scope is tinycss2 (flit_core backend — no
   `python3-flit_core` in EL10; needs a vendored backend wheel) and pillow (custom backend
   requiring `setuptools>=77` — host has 69.0.3; pybind11 is in CRB). setproctitle and webencodings
   have no `pyproject.toml` (verified by `tar tzf`), so they build through the legacy `setup.py`
   path with no PyPI fetch; Omega's setproctitle hypothesis was refuted. Fix with
   `--no-build-isolation` + explicit BRs, verified by actual rpmbuild.
5. gdk-pixbuf-parsers license (last of Omega's medium six): folds into the Shadow #3
   rebuild-from-source (its spec will carry `%license COPYING.LIB`).

### Review-finding resolution turn (done 2026-09-18, commits `55e37bd` + `2fa1b2d`)

Scope: the 15 open review findings (Shadow 8, Omega 4, Big 3). All code and evidence changes are
shipped; the three re-verifications (clean-checkout rebuild, fresh-VM `run-tests.sh`,
enforcing-SELinux smoke) are assigned to Tails and remain open per `## Status`. Every `## Review`
and `## Security` finding now carries a `**Resolution:**` line with its fix commit.

### Changes (commit `55e37bd`: code; `2fa1b2d`: evidence)
| File | Change | Why |
|---|---|---|
| `tasks/lib/ukey.c:127-128` | `Super_L`/`Super_R` → `KEY_LEFTMETA`/`KEY_RIGHTMETA`; both bits added to `keybits[]` (:253) | Shadow should-fix 4: mapping emitted Control, not Meta |
| `spec/cinnamon.spec:43-44` | comment "three" → "four" Requires | Shadow nit 6 |
| `vm-test/parity/parity-inventory.sh:64-79` | new `gget()` helper (list-schemas → list-keys → get); screensaver keys use it (:190-191) | Shadow nit 8: "schema absent" misdiagnosed a missing key |
| `vm-test/run-tests.sh` | T1: `die` on install rc (was captured, never read) and verify rc (was warning-only); T2: deleted dead `SYSTEM_DEPS` array and the Phase 2 native `dnf install` of `mozjs115`/`clutter`/`cogl` (certain to fail, swallowed by `\|\| echo WARNING`); T3: Phase 4 verifies the 22 runtime names read from `vm-test/install-set.txt` (scp'd in Phase 1) instead of a hardcoded 11-name array | Big T1/T2/T3 |
| `vm-test/install-set.txt` | added: the 22 runtime package names (rpms/ minus `-devel`/`-debuginfo`/`-debugsource`), derived and recorded in the file header | Big T3: encode the accepted set in the repo |
| `vm-test/evidence/task0017-fresh-3.1/2026-09-18/` | 22 files committed (5 surfaces + a11y/pixelstats/bands/logs) | Shadow should-fix 5 |
| `vm-test/parity/rocky10/2026-09-18-3.2/` | 6 files committed (5 captures + inventory); the 6 never-taken captures recorded as absent in the commit message | Shadow should-fix 5 |

### Alternatives considered
- **Phase 4 package list** — Option A: keep the hardcoded array, extend it to 22 names (rejected: two sources of truth, the array already drifted once, missing 11 of the 22). Option B: a file in the repo (`vm-test/install-set.txt`), copied to the VM in Phase 1 and parsed in the remote heredoc (chosen: one encoding, regenerable by the command in its header, and the remote read avoids changing the `ssh_cmd` interface). Option C: pass names as positional arguments through `ssh_cmd` (rejected: the quoted heredoc interface would need reworking for one array).
- **Phase 2 native deps** — verified before deleting the block: `spec/gnome-terminal.spec:41` `Requires: gsettings-desktop-schemas`, `spec/cinnamon-rocky-defaults.spec:27-28` `Requires: rocky-backgrounds`/`rocky-logos`, so dnf pulls them automatically in Phase 3; `mozjs115` and the clutter/cogl pair are in the local set (`muffin-clutter`, `muffin-cogl` are subpackages of the muffin build, confirmed `rpm -qlp` on the muffin RPM shows no clutter/cogl files and the pair exists only as our RPMs). Native `clutter`/`cogl` do not exist in EL10, which is why the old block was a guaranteed failure.
- **Project-repo `AGENTS.md`** — refreshed byte-identical to the canonical `metalllinux/team-chaotix/AGENTS.md` (it had drifted: pre-TASK-0022 model line, `compaction.auto: false`) but left **untracked**, per the recorded TASK-0019 decision ("left uncommitted; user decides on commit"). Not committed by Tails.

### Checks run
- `gcc -fsyntax-only -Wall -Wextra tasks/lib/ukey.c` → clean (in-VM compile path `tasks/lib/gdm-drive.sh:81` unchanged).
- `bash -n vm-test/run-tests.sh` and `bash -n vm-test/parity/parity-inventory.sh` → clean; `shellcheck vm-test/run-tests.sh` → only the pre-existing SC1091 (does not follow sourced `lib.sh`).
- Per-name single-version check over `rpms/` (64 files): all 64 names resolve to exactly one file (repoquery-equivalent on the single-repo tree).
- Spec-state verification for the resolution claims: `grep -l '%license' spec/*.spec` lists all six flagged specs; `Requires: python3-webencodings` at `spec/python3-tinycss2.spec:35`; `--no-build-isolation` in all four pip specs (tinycss2:60, pillow:70, setproctitle:48, webencodings:55); live URLs at `spec/python3-setproctitle.spec:9` and `spec/python3-webencodings.spec:9`; `%post`/`%postun` at `spec/gdk-pixbuf-parsers.spec:79,86`.
- `git push` of both commits to `origin feature/TASK-0017-cinnamon-desktop-completeness` → `4c9f7c2..2fa1b2d`.

### Open notes
- **cjs tarball (for Shadow):** `~/rpmbuild/SOURCES/cjs-6.4.0.tar.gz` is functionally hermetic (no `builddir/` inside) but carries a 238-entry `.git/`. It was deliberately **not** regenerated: the checkout `~/Linux/projects/cinnamon_4_rocky10/cjs` (HEAD `cdd85377`, tag 6.4.0) has two uncommitted modified files, `build/compile-gschemas.py` and `build/symlink-gjs.py`, and `git archive HEAD` would silently drop them, changing the published source. Follow-up: commit or vendor those two modifications upstream-side, then re-tar with `git archive`.
- **Re-verifications (assigned Tails):** A done 2026-09-19 (PASS, entry below); B `run-tests.sh` end-to-end on a fresh VM (exercises the T1/T2/T3 changes and the ukey Super mapping end-to-end via a `ukey key Super_L` menu open) and C enforcing-SELinux smoke (boot enforcing, GDM login, five surfaces, log AVCs) remain open.

### Re-verification A: clean-checkout rebuild (done 2026-09-19, PASS)

Scope: rebuild the 10 specs whose content changed since the published build (blocker trio nemo/gtk-layer-shell/cinnamon-settings-daemon + cinnamon-desktop, gdk-pixbuf-parsers, cinnamon-rocky-defaults, and the four pip rebuilds from `4c9f7c2`) from a fresh clone of the pushed branch, and compare against `rpms/`.

- Fresh clone from GitHub at `2fa1b2d` (`/tmp/opencode/t17-verifyA/clone`), scratch topdir, sources staged from `~/rpmbuild/SOURCES` + repo `spec/`. House pattern confirmed: bare `Source:` names resolve from `_sourcedir` only, not the spec directory, so `webencodings-LICENSE`, `GPLv2.txt`, `gnome-bg-wayland-surface.patch`, and `gdk-pixbuf-2.42.12.tar.xz` (sha256 `b9505b34...` verified against the spec comment and the live GNOME URL) must be copied into topdir `SOURCES/` by hand.
- All 10 specs built RC 0 (two passes, logs `build.log` + `build2.log`). The 4 first-pass failures were staging gaps on my side (files missing from topdir `SOURCES/`), not repo defects; pass 2 re-ran them clean. Builds verified genuine (meson setup + ninja compiles, not cache hits).
- NVR and subpackage sets match the published `rpms/` exactly: 10 main + the debuginfo/debugsource/devel subpackages that exist in the published set; zero NVR misses.
- Payload comparison (rpm2cpio extract, per-file `cmp`, symlink-aware): **byte-identical except two classes of build-environment artifact**:
  1. The 20-byte SHA-1 digest in `.note.gnu.build-id` of every LTO-compiled binary (csd-*, libcinnamon-desktop, libcvc, nemo*, libgtk-layer-shell, pixbuf loaders, PIL + setproctitle `.so`), with derived deltas in `.gnu_debugdata` (DWARF), `.gnu_debuglink` CRC, and the `.build-id/` directory entries. Root cause: host default CFLAGS include `-flto=auto -ffat-lto-objects` (`build.log:42`), and GCC's LTO stream emits per-compile-unit weak symbols named `<source.c>.<8hex>` whose hash is build-environment-dependent (empirically: not a file-content hash, not a path-string hash, differs between the two topdirs while file content hashes match). Section-level hash comparison shows `.text`/`.rodata` byte-identical (nemo, csd-background, libcinnamon-desktop, nemo-desktop, libgtk-layer-shell, libpixbufloader-png.so); the setproctitle `.so` differs in exactly 20 bytes, offsets 761-780 = the build-id digest region (`.note.gnu.build-id` at 0x2e8, size 0x24).
  2. `direct_url.json` in the four pip packages records the absolute build directory (`file://` URL) — known pip non-determinism, verified by diff (only the path differs).
- A first comparison pass flagged the devel/debugsource/noarch pairs as differing; that was `diff -r` following dangling symlinks (e.g. `libnemo-extension.so` -> `.so.1`, target ships in the main package). Symlink-aware re-compare: identical.
- Key content checks 9/9: nemo `Requires: gtk-layer-shell`; tinycss2 `Requires: python3-webencodings`; gdk-pixbuf-parsers ships `%postun` + png+jpeg loaders; `/usr/share/licenses/` present in all four pip packages + cinnamon-rocky-defaults.
- **Verdict: PASS.** The clean checkout at `2fa1b2d` deterministically reproduces the published packages; the residual byte deltas are environment-dependent build metadata (LTO stream symbol hashes, build-ids, pip direct_url paths), not spec or source differences. Artifacts: `/tmp/opencode/t17-verifyA/{clone, topdir, build.log, build2.log, compare.sh, compare2.sh, sectdiff.sh}`.

---

## Review

*Owner: `Shadow`. Read-only — findings only, no edits. Severity order, blockers first.*

*Reviewed 2026-09-18 by `Shadow`. Scope: commits `c1de933..eafa476` (7 commits) on `feature/TASK-0017-cinnamon-desktop-completeness` — every spec file changed or cross-checked by the branch (`cinnamon-desktop` 2.el10 rewrite + `gnome-bg-wayland-surface.patch`, `cinnamon-rocky-defaults`, `cinnamon`, the five Python specs, `gnome-terminal`, `gdk-pixbuf-parsers`, plus the `nemo` / `cinnamon-settings-daemon` divergence), the `rpms/` tree, the harness changes (`tasks/lib/ukey.c`, `tasks/lib/gdm-a11y.py`, `vm-test/run-tests.sh`, `vm-test/parity/parity-inventory.sh`), and the untracked `vm-test/evidence/` + `vm-test/parity/rocky10/2026-09-18-3.2/` checked against the Test Results claims. Verification: `git diff c1de933..eafa476`, `git show eafa476:vm-test/parity/rocky10`, `git log --oneline c1de933..eafa476`, `rpm -qR` on the installed `cinnamon` / `tinycss2` / `xapp` RPMs, `git status`, host inspection of `/home/howard/rpmbuild/SPECS` and `SOURCES`. No issues found in `gdm-a11y.py`, `run-tests.sh`, the five Python specs, `gnome-terminal.spec`, `cinnamon-desktop.spec` + patch, `cinnamon-rocky-defaults.spec`, or the inventory script structure beyond the findings below.*

### The repo `spec/` cannot reproduce the shipped `nemo`, `gtk-layer-shell`, `cinnamon-settings-daemon` RPMs
**Severity:** blocker
**Where:** `spec/nemo.spec:3`, `spec/cinnamon-settings-daemon.spec:3`, missing `spec/gtk-layer-shell.spec`; against `rpms/nemo-6.7.4-2.el10.x86_64.rpm`, `rpms/gtk-layer-shell-0.10.1-1.el10.x86_64.rpm`, `rpms/cinnamon-settings-daemon-6.7.2-2.el10.x86_64.rpm`
**Problem:** the canonical spec directory is out of sync with the published RPM set for exactly the three packages the wallpaper fix depends on. The repo `nemo.spec` is `Release: 1.el10` with no gtk-layer-shell BuildRequire and no `-Dgtk_layer_shell` meson option, while the shipped `2.el10` RPM was built from the host's `/home/howard/rpmbuild/SPECS/nemo.spec` (`Requires: gtk-layer-shell` at line 9, `BuildRequires: gtk-layer-shell-devel` at line 12, the `-Dgtk_layer_shell=true` note at line 100). The repo has no `gtk-layer-shell.spec` at all; the host has `/home/howard/rpmbuild/SPECS/gtk-layer-shell.spec` (Source0 URL at line 10). The repo `cinnamon-settings-daemon.spec` is `1.el10`; the shipped RPM is `2.el10`. The repo `nemo.spec` also declares 11 subpackages (`spec/nemo.spec:45-115`) while the published set ships only `nemo` + `nemo-devel` (plus debuginfo/debugsource), so a 1:1 copy of the repo spec would not match the published set either.
**Failure scenario:** clean checkout of this branch → `rpmbuild` from `spec/` → produces `nemo-6.7.4-1` (no layer-shell), no `gtk-layer-shell` package, and `cinnamon-settings-daemon-6.7.2-1`. A fresh install from the rebuilt repo leaves the Wayland wallpaper black — the defect this task fixed — and the 3.1/3.2 PASS verdicts are not reproducible from the branch.
**Suggested direction:** sync the three host specs into `spec/` (adopt the host `nemo.spec` as canonical, subpackage set included, so the built set matches the published set), rebuild the three packages, republish the repo, and re-verify the rebuilt nemo RPM carries the gtk-layer-shell path (`rpm -qp --requires` plus the meson option).
**Resolution:** fixed in `459ac30` (2026-09-18, Tails). The host build specs were adopted into `spec/` (six linuxmint specs including `nemo.spec` and `cinnamon-settings-daemon.spec`, plus new `gtk-layer-shell.spec`), each with a Source0 provenance comment recording the exact upstream ref the tarball was archived from and the tarball sha256. The adopted `spec/nemo.spec` declares main + one `%package devel` (`grep -c '^%package' spec/nemo.spec` → 1), matching the published set; debuginfo/debugsource are auto-generated, not declared. Rebuilt from `spec/`: `nemo-6.7.4-2.el10`, `gtk-layer-shell-0.10.1-1.el10`, `cinnamon-settings-daemon-6.7.2-2.el10` republished to `rpms/`. `rpm -qp --requires` on the rebuilt nemo shows `gtk-layer-shell`; the spec carries `BuildRequires: gtk-layer-shell-devel` and the `-Dgtk_layer_shell=true` meson option.

### The published `rpms/` retains the superseded 1.el10 builds, including the known-broken `cinnamon-desktop-6.7.2-1`
**Severity:** should-fix
**Where:** `rpms/`: `cinnamon-desktop-6.7.2-1.el10` (+ `-devel`, `-debuginfo`, `-debugsource`) and `cinnamon-settings-daemon-6.7.2-1.el10` (+ `-debuginfo`, `-debugsource`) — 7 files
**Problem:** the repo keeps the superseded 1.el10 builds it explicitly replaced, sitting next to their 2.el10 replacements (verified: these are the only name+version pairs with two releases in `rpms/`; every other 1.el10 file is its package's sole build). `cinnamon-desktop-6.7.2-1` is the unpatched build whose Wayland wallpaper rendering is the defect this task fixed.
**Failure scenario:** `dnf install cinnamon-desktop-6.7.2-1.el10` (version-pinned) against this repo succeeds and installs the black-wallpaper build; any sync audit sees two releases per name and cannot tell which is canonical without this doc.
**Suggested direction:** delete the 7 superseded files, regenerate repodata, and re-verify with `dnf repoquery` that each package name resolves to exactly one version.
**Resolution:** fixed in `4c9f7c2` (2026-09-18, Tails). All 7 files deleted (the 4 `cinnamon-desktop-6.7.2-1.el10` subpackage files and the 3 `cinnamon-settings-daemon-6.7.2-1.el10` files), alongside the other superseded 1.el10 files (`cinnamon-rocky-defaults-1.0-1`, `gdk-pixbuf-parsers-2.42.12-1`, the four `python3-*-1.el10`) and the stale pre-fix `cinnamon-desktop` 2.el10 files (all four subpackages), replaced by the CFLAGS-correct 2.el10 rebuild in the same commit. `rpms/` now holds 64 files; per-name check `for f in rpms/*.rpm; do rpm -qp --qf '%{NAME}\n' "$f"; done | sort -u` → 64 names, each resolving to exactly one file (repoquery-equivalent on a single-repo tree; `rpms/repodata/` regenerated with createrepo_c, gitignored per house style).

### The `gdk-pixbuf-parsers` RPM ships prebuilt binaries that are not rebuildable from the repo
**Severity:** should-fix
**Where:** `spec/gdk-pixbuf-parsers.spec:10`, `.gitignore:9-10`
**Problem:** `Source0` is a prebuilt tarball (contains `libpixbufloader-png.so`, `libpixbufloader-jpeg.so`, `gdk-pixbuf-query-loaders`; `%build` is `:`) with no URL and no checksum, and the tarball itself is gitignored and absent from the checkout, present only on the build host at `/home/howard/rpmbuild/SOURCES/`. Every other spec in the tree has a fetchable `Source0`.
**Failure scenario:** clean checkout → `rpmbuild spec/gdk-pixbuf-parsers.spec` fails at source fetch (no URL, no local tarball). The PNG/JPEG decode path the wallpaper depends on (verified working in the 2.1/3.1/3.2 VM runs) cannot be verified, audited, or rebuilt by anyone without the build host.
**Suggested direction:** build the loaders from the upstream gdk-pixbuf source (URL + checksum, the same shape as the rest of the tree), or keep the prebuilt artifact and give it a `Source0` URL + checksum plus a comment explaining why it is prebuilt. Also check whether EL10's native `gdk-pixbuf2-modules` (present in the 3.2 VM package stack, `inventory-rocky10-3.2.txt` STACK section) already covers these loaders, and prefer the native package if it does. Not verified here: the build host's base `loaders.cache` listed only gif/svg/tiff, but `gdk-pixbuf2-modules` was not installed on that host.
**Resolution:** fixed in `4c9f7c2` (2026-09-18, Tails). `spec/gdk-pixbuf-parsers.spec` rewritten to build the png/jpeg loaders from the upstream GNOME `gdk-pixbuf-2.42.12` tarball: `Source0:` is the `download.gnome.org` URL with a verified sha256 comment (`spec/gdk-pixbuf-parsers.spec:14-15`), `%build`/`%install` compile the two loader targets, and the prebuilt tarball is gone. Native-coverage check: EL10 `gdk-pixbuf2-modules` ships only the gif and tiff loaders (verified on the build host with `rpm -ql gdk-pixbuf2-modules`), so the png/jpeg package remains required and is installed alongside it. Rebuilt and republished as `gdk-pixbuf-parsers-2.42.12-2.el10` (+debuginfo/+debugsource).

### `ukey.c` maps `Super_L`/`Super_R` to Control keycodes
**Severity:** should-fix
**Where:** `tasks/lib/ukey.c:127-128`; also `tasks/lib/ukey.c:243-261` (`keybits[]` omits the META bits)
**Problem:** `{ "Super_L", KEY_LEFTCTRL }` and `{ "Super_R", KEY_RIGHTCTRL }` emit left/right **Control** (29/97), not left/right **Meta** (`KEY_LEFTMETA` 125 / `KEY_RIGHTMETA` 126). The comment "Windows/Meta key: Cinnamon menu" describes intent the code does not implement, and `keybits[]` advertises no META at all, so a corrected table alone would still emit events the device does not claim.
**Failure scenario:** nothing in the branch invokes the mapping yet (verified: repo-wide grep for `Super_L|Super_R|KEY_LEFTMETA|KEY_RIGHTMETA` matches only `ukey.c:127-128`; the 3.1 main menu was opened by clicking the menu button), so this is a landmine, not a live failure. The first step that uses `ukey key Super_L` to open the Cinnamon main menu, as the comment and commit `9126531` ("Super key mapping") promise, sends a bare Control press; the menu stays closed and the a11y wait times out with "target never appeared", sending the operator to debug the desktop instead of the input table.
**Suggested direction:** map to `KEY_LEFTMETA`/`KEY_RIGHTMETA` and add both to `keybits[]`.
**Resolution:** fixed in `55e37bd` (2026-09-18, Tails). `tasks/lib/ukey.c:127-128` now maps `Super_L`→`KEY_LEFTMETA` (125) and `Super_R`→`KEY_RIGHTMETA` (126), and both bits are added to `keybits[]` (`tasks/lib/ukey.c:253`), so the uinput device advertises the keys it emits. `gcc -fsyntax-only -Wall -Wextra tasks/lib/ukey.c` passes; the in-VM compile path (`tasks/lib/gdm-drive.sh:81`, `gcc -O2 -Wall -Wextra`) is unchanged. Not exercised in a VM yet: the 3.1/3.2 runs opened the menu by clicking, so this fix needs a `ukey key Super_L` menu-open in a future run to be proven end-to-end (re-verification B).

### The 3.1/3.2 acceptance evidence is untracked; the branch lacks the evidence its PASS verdicts cite
**Severity:** should-fix
**Where:** `vm-test/parity/rocky10/2026-09-18-3.2/` and `vm-test/evidence/task0017-fresh-3.1/` (both untracked per `git status`); contrast `vm-test/parity/rocky10/2026-09-17-2.2-*` (committed, present in `git show eafa476:vm-test/parity/rocky10`)
**Problem:** Test Results cites `inventory-rocky10-3.2.txt`, the 3.2 PNGs, and the 3.1 screenshots/trees/pixelstats for the "11/11 PASS" and "5/5 PASS" verdicts, but none of it is in the branch. The earlier 2.1/2.2 evidence is committed, so the house pattern is to commit it, and the 2.2 Test Results entry explicitly noted it was "uncommitted at time of writing" while the 3.2 entry does not. The local 3.2 set also holds 5 of the 11 staged captures (`03`/`04` fold into `01` by design; `02-panel`, `05-themes-panel`, `10-power-menu`, `11-session-controls` are absent from the local set although rows 2/5/10/11 were evaluated from the inventory).
**Failure scenario:** a reviewer, a later Tails fix round, or Knuckles at release time clones the branch and cannot inspect any screenshot, a11y tree, or pixelstat the verdicts rest on; "11/11 PASS" exists only as prose in this doc.
**Suggested direction:** commit the 3.2 parity set and the 3.1 evidence directory (the established 2.2 pattern), or record in Test Results why the final-run evidence is intentionally uncommitted and where it is stored. Either capture the 4 missing 3.2 screenshots or note in the inventory which rows were evaluated from data only.
**Resolution:** fixed in `2fa1b2d` (2026-09-18, Tails). Committed `vm-test/evidence/task0017-fresh-3.1/2026-09-18/` (22 files: the five surfaces with a11y trees, pixelstats, bands, screenshot logs, panels config) and `vm-test/parity/rocky10/2026-09-18-3.2/` (6 files: the five 3.2 captures taken + `inventory-rocky10-3.2.txt`), per the established 2.2 pattern. The six 3.2 captures never taken (`02-panel`, `03`/`04` folded into `01` by design, `05-themes-panel`, `10-power-menu`, `11-session-controls`) remain absent; the inventory's STACK/KEY data covered the rows that were evaluated from data only, as recorded in the 3.2 Test Results entry. The project-repo `AGENTS.md` copy was refreshed byte-identical to the canonical `metalllinux/team-chaotix/AGENTS.md` but deliberately left untracked, per the TASK-0019 decision ("left uncommitted; user decides on commit").

### `spec/cinnamon.spec` comment says "three" but four Requires are added
**Severity:** nit
**Where:** `spec/cinnamon.spec:44-45`
**Problem:** "The app imports all three unguarded; Fedora carries the same three Requires" — but the block adds four (`python3-setproctitle`, `python3-pillow`, `python3-tinycss2` at lines 47-49, plus `python3-xapp` at line 51). The fourth has its own comment at line 50, leaving the shared header stale.
**Failure scenario:** a maintainer reading the block concludes the Fedora reference carries three Requires and questions whether `python3-xapp` is over-requiring; the verified claim (installed `cinnamon` 6.7.4-3 `Requires` via `rpm -qR`) is four.
**Suggested direction:** update the comment to four.
**Resolution:** fixed in `55e37bd` (2026-09-18, Tails). `spec/cinnamon.spec:43-44` now reads "The app imports all four unguarded; Fedora carries the same four Requires on the cinnamon package", and the xapp line's comment says "also imports xapp".

### `gdk-pixbuf-parsers` has no `%postun`; removal leaves a stale `loaders.cache`
**Severity:** nit
**Where:** `spec/gdk-pixbuf-parsers.spec:47-48`
**Problem:** `%post` rewrites `loaders.cache` to include the two new loaders, but there is no `%postun` to regenerate it on removal, and `loaders.cache` is unowned (not in `%files`).
**Failure scenario:** `dnf remove gdk-pixbuf-parsers` → the `.so` files are gone but `loaders.cache` still lists their paths → every later gdk-pixbuf load query on that machine logs missing-loader warnings until something else regenerates the cache.
**Suggested direction:** add a `%postun` that re-runs the cache regeneration on final removal (`$1 == 0`).
**Resolution:** fixed in `4c9f7c2` (2026-09-18, Tails). `spec/gdk-pixbuf-parsers.spec:86` carries a `%postun` that re-runs `gdk-pixbuf-query-loaders --updatecache` (guarded on `$1 == 0`, final removal only), mirroring the `%post` at line 79.

### `parity-inventory.sh` "schema absent" fallback misdiagnoses a missing key
**Severity:** nit
**Where:** `vm-test/parity/parity-inventory.sh:172-173`
**Problem:** the fallback text for `gsettings get org.cinnamon.desktop.screensaver mode` / `lock-enabled` is "schema absent", but the 3.2 inventory proves the schema exists: `SCREENSAVER_MODE: schema absent` sits beside `SCREENSAVER_LOCK_ENABLED: true` (same schema). The key is absent, not the schema.
**Failure scenario:** a future parity run on a system with `lock-enabled` set and `mode` absent (the 3.2 VM itself) reads "schema absent" and the operator concludes the whole screensaver schema is missing, contradicting the adjacent line, and skips investigating the `mode` key.
**Suggested direction:** use a fallback that says the key is absent (e.g. "key absent"), or distinguish the two with a `gsettings list-keys` check first.
**Resolution:** fixed in `55e37bd` (2026-09-18, Tails). `vm-test/parity/parity-inventory.sh:64-79` adds a `gget()` helper: `gsettings list-schemas` first, then `list-keys` on the schema, emitting `key absent (schema present)` vs `schema absent` distinctly; the two screensaver keys (lines 190-191) use it. `bash -n` passes; the next 3.2-style inventory run will show the corrected text.

---

## Security

*Owner: `Omega`. Read-only. Severity order.*

**Scope:** branch `feature/TASK-0017-cinnamon-desktop-completeness` (`c1de933..eafa476`): the eight new/modified specs, the wallpaper patch, the test harness (`tasks/lib/`, `vm-test/`), and the committed `rpms/` payload. All eight `License:` tags were verified against upstream license text at the exact tags and all eight are correct. The findings below are the remaining gaps.

### Six of the new RPMs ship without a license file
**Severity:** medium
**Vector:** license
**Where:** `spec/gdk-pixbuf-parsers.spec:50-53`, `spec/python3-tinycss2.spec:43-46`, `spec/python3-setproctitle.spec`, `spec/python3-webencodings.spec`, `spec/python3-pillow.spec`, `spec/cinnamon-rocky-defaults.spec`
**Attack:** no active attacker; the enforcement actor is the upstream copyright holder (GNOME for gdk-pixbuf, CourtBouillon/Kozea for tinycss2 and webencodings, the setproctitle and Pillow maintainers) or a downstream distributor auditing the RPMs. The path is deterministic: `rpm -qlp` on any of the six packages shows no license file. The pip-based specs install with `pip install --target` (e.g. `spec/python3-tinycss2.spec:41`), which copies only the package directory and dist-info, not the sdist's top-level LICENSE, and none of the six specs carries a `%license` line (a repo-wide grep for `%license` matches only `spec/gnome-terminal.spec:84`, `spec/python3-xapp.spec:48`, and the pre-existing `spec/mozjs115.spec:163`).
**Impact:** for `gdk-pixbuf-parsers` this is a distribution obligation, not style. The two `.so` files are prebuilt LGPL-2.1-or-later object code (`spec/gdk-pixbuf-parsers.spec:5`) and LGPL-2.1 section 4 requires object code to be distributed with a copy of the license. For the BSD/MIT/HPND packages the license terms require the copyright notice to accompany redistribution. The dist-info METADATA inside the RPMs carries only the one-line `License:` tag, not the text or the notice.
**Fix:** add a `%license` entry to each of the six specs. `%setup` has already extracted the sdist into the build dir, so where the sdist contains the license file, a plain `%license <file>` in `%files` suffices (this is the established pattern in `spec/python3-xapp.spec:48`). Verified present in the sdist: tinycss2 (flit config at tag `v1.5.1` declares `license = {file = 'LICENSE'}`) and pillow (pyproject at tag `12.3.0` declares `license-files = ["LICENSE"]`). Unverified for setproctitle and webencodings (sdists not unpackable, no bash access); if absent, vendor the upstream license text as an additional `Source`. For `gdk-pixbuf-parsers`, add `COPYING.LIB` from the gdk-pixbuf 2.42.12 source tree. `cinnamon-rocky-defaults` is in-house with no upstream; ship a GPLv2 copy the same way.
**Resolution:** fixed in `459ac30` + `4c9f7c2` (2026-09-18, Tails). All six specs now carry `%license` (verified: `grep -l '%license' spec/*.spec` lists all six plus the pre-existing gnome-terminal/xapp/mozjs115/gtk-layer-shell). tinycss2, setproctitle, pillow ship the sdist-root `LICENSE`; webencodings vendors the upstream BSD text as `Source1` (`spec/webencodings-LICENSE`, sha256 `f23bae6a…`, fetched from courtbouillon/webencodings v0.5.1) because the PyPI sdist ships no license file; `cinnamon-rocky-defaults` vendors GPLv2 as `Source0` (`spec/GPLv2.txt`, byte-identical to the repo top-level LICENSE, sha256 `8177f975…`); the `gdk-pixbuf-parsers` rewrite ships the LGPL-2.1 text from the gdk-pixbuf 2.42.12 source tree. Every published RPM installs its license at `/usr/share/licenses/<pkg>/` (verified with `rpm -qlp` during the 2.el10 rebuild).

### python3-tinycss2 omits its only runtime Requires, orphaning python3-webencodings
**Severity:** low
**Vector:** input-validation
**Where:** `spec/python3-tinycss2.spec:21`, `spec/python3-tinycss2.spec:37-40`
**Attack:** no attacker; the path is a minimal install. `dnf install cinnamon` pulls `python3-tinycss2` (required by `spec/cinnamon.spec`), but a grep of every spec shows no package requires `python3-webencodings`. `tinycss2/__init__.py` does `from webencodings import lookup`, so `import tinycss2` raises `ModuleNotFoundError: webencodings` and the Cinnamon settings theme panel (plan item 3.2) breaks on any system where the webencodings RPM was not installed. The spec comment at lines 37-40 claims the dependency "becomes an RPM Requires via the dist-info metadata". rpmbuild does not parse pip dist-info METADATA, so the claim is false and the dependency edge is missing. Upstream confirms the dependency: the pyproject at tag `v1.5.1` declares `dependencies = ['webencodings >=0.4']`.
**Impact:** broken desktop on a clean install, discoverable only when the settings panel is opened.
**Fix:** add `Requires: python3-webencodings` to `spec/python3-tinycss2.spec` and correct the comment.
**Resolution:** fixed in `459ac30` (2026-09-18, Tails). `spec/python3-tinycss2.spec:35` carries `Requires: python3-webencodings` and the false dist-info-METADATA comment is replaced with the verified statement that rpmbuild does not parse pip metadata, so the edge must be declared explicitly.

### PEP 517 build isolation pulls unpinned build backends from PyPI at build time
**Severity:** low
**Vector:** supply-chain
**Where:** `%install` of `spec/python3-tinycss2.spec:41`, `spec/python3-pillow.spec`, `spec/python3-setproctitle.spec`
**Attack:** an attacker who has compromised a PyPI project used as a build backend (account takeover or a malicious maintainer). The pip specs run `pip install .` without `--no-build-isolation`, so for sdists that declare a PEP 517 build system pip creates an isolated environment and downloads the declared backend from PyPI during rpmbuild, pinned only by a lower bound. Confirmed at the exact tags: tinycss2 `v1.5.1` declares `requires = ['flit_core >=3.2,<4']`; pillow `12.3.0` declares `requires = ["pybind11", "setuptools>=77"]`. The backend executes during the build and controls what it emits, so a malicious backend can run code on the build host and inject code into the built module.
**Impact:** code execution on the self-hosted runner (the user's local machine) at build time, and the injected code can land in the shipped RPM and reach downstream consumers of the repo. The precondition is significant (compromise of a top-level PyPI project) and the practice is standard across the ecosystem, hence low.
**Fix:** add `--no-build-isolation` to the pip invocations plus `BuildRequires: python3-setuptools` so the builds use the EL10-pinned toolchain instead of fetching from PyPI. Tails should confirm at rebuild whether the setproctitle and webencodings sdists trigger isolation (the setproctitle tag `version-1.3.7` carries a `pyproject.toml` with no `[build-system]` table, which per PEP 517 means the default setuptools backend with isolation on; the sdists could not be unpacked to verify).
**Resolution:** fixed in `4c9f7c2` (2026-09-18, Tails). All four pip specs now build with `--no-build-isolation` (verified: `spec/python3-tinycss2.spec:60`, `spec/python3-pillow.spec:70`, `spec/python3-setproctitle.spec:48`, `spec/python3-webencodings.spec:55`). Backend strategy, all from EL10-pinned or vendored sources, no PyPI fetch: tinycss2 runs the vendored `flit_core` wheel (`PYTHONPATH="$PWD/backends"` + BuildRequires); pillow runs vendored `setuptools`/`pybind11` wheels the same way; setproctitle and webencodings take the legacy `setup.py` path with `BuildRequires: python3-wheel` (installed on the build host: `python3-wheel-0.41.2-5.el10_1.1`) plus `bdist_wheel`. Isolation question resolved by construction: with `--no-build-isolation` no backend is ever fetched, so the setproctitle/webencodings `pyproject.toml` edge case is moot. The 2.el10 rebuilds of all five Python RPMs completed with no network access to PyPI.

### Two spec URL fields are dead links
**Severity:** low
**Vector:** license
**Where:** `spec/python3-setproctitle.spec:9`, `spec/python3-webencodings.spec:9`
**Attack:** no attacker; a provenance-auditability gap. `https://github.com/dvarrazz/python-setproctitle` (misspelled account, wrong repo name) 404s; the real repo is `https://github.com/dvarrazzo/py-setproctitle`, whose LICENSE (BSD 3-Clause) matches the spec's `License: BSD-3-Clause` tag. `https://github.com/Kozea/webencodings` also 404s (the repo was removed or renamed); the live upstream is `https://github.com/courtbouillon/webencodings` (fork of `gsnedders/python-webencodings`).
**Impact:** anyone verifying source provenance from the spec hits a dead end; the sha256 comments are the only provenance anchor.
**Fix:** set the two URLs to the live repos.
**Resolution:** fixed in `459ac30` (2026-09-18, Tails). `spec/python3-setproctitle.spec:9` → `https://github.com/dvarrazzo/py-setproctitle` and `spec/python3-webencodings.spec:9` → `https://github.com/courtbouillon/webencodings`, both verified live at fix time (setproctitle's LICENSE there matches the spec's `License: BSD-3-Clause` tag).

### Verified clean
- **License tags, all eight:** tinycss2 `BSD-3-Clause` (LICENSE at `Kozea/tinycss2`), setproctitle `BSD-3-Clause` (LICENSE at `dvarrazzo/py-setproctitle`; `license="BSD-3-Clause"` in setup.py at tag `version-1.3.7`), webencodings `BSD` (PyPI 0.5.1 classifier and README), pillow `HPND and MIT` (MIT-CMU LICENSE at tag `12.3.0`), xapp `LGPLv2+` (COPYING at `linuxmint/python3-xapp` 3.0.2, later-version clause at :458), gnome-terminal `GPLv3+ AND GFDL-1.3-only` (both COPYING files at tag `3.54.5`), gdk-pixbuf-parsers `LGPL-2.1-or-later` (meson.build at tag `2.42.12`), cinnamon-rocky-defaults `GPLv2+` (in-house, no upstream).
- **Secrets:** a repo-wide regex sweep for common token and key patterns (GitHub PATs, AWS keys, Slack tokens, private-key blocks, API keys) returned zero matches. `vm-test/rocky10.ks` uses `rootpw --locked`; SSH is key-only (`PermitRootLogin yes` with `ssh_pwauth: False`, no password in `user-data`); the `gdmtest` password is generated randomly inside the VM at runtime (`openssl passwd -6` in `vm-test/test-gdm-login.sh`) and never leaves the guest; the fleet SSH key lives outside the repo (`~/.ssh/cinnamon-test-key`, mode 600 enforced by `assert_ssh_key` in `vm-test/lib.sh`); `vm-test/known_hosts` carries public keys only, with the one-time TOFU documented.
- **SSH channel exposure:** every ssh/scp/rsync channel runs `StrictHostKeyChecking=yes` against a pinned file (`ssh_pin_opts` in `vm-test/lib.sh`); per-VM pin files are seeded out-of-band from the qcow2 and are gitignored (`vm-test/results/`); a VM without a pin file is refused, there is no verification-off fallback.
- **Injection surface:** harness remote commands are quoted heredocs (`<<'REMOTE_SCRIPT'`) or fixed constants (package names, paths, the `gdmtest` username); no attacker-influenced input reaches a shell. `--in-vm` (`vm-test/test-gdm-login.sh:334,366`) is an operator-supplied CLI argument, not external input. `tasks/lib/ukey.c` has no format-string, leak, or injection issues (the Super-to-Control mapping is Shadow finding 3, not repeated here).
- **File modes:** `cinnamon-rocky-defaults` payloads are 0644 world-readable config with no secrets; the dconf and gschema scriptlets are standard; no setuid or world-writable files in the branch diff.
- **Build flags:** `--buildtype=plain` in `spec/cinnamon-desktop.spec` does not drop `-O2`; rpmbuild `%optflags` still reach the compiler via the environment, so the `-D_FORTIFY_SOURCE` conditions hold.
- **VNC:** libvirt default binds 127.0.0.1 with no password; host-only, documented in `vm-test/fedora-cinnamon-ref-setup.md`.

**Counts:** medium 1, low 3. **Top 3:** (1) missing license files in six new RPMs, (2) `python3-tinycss2` missing `Requires: python3-webencodings`, (3) unpinned PEP 517 build backends fetched from PyPI at build time.

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

*Entry 2026-09-18: plan items 3.1 + 3.2 — fresh-VM end-to-end and full parity re-run. Direct VM
verification on host `192.168.1.102`, not a CI workflow run, so the standard table's
compile/linter/unit/integration/Sparky rows do not apply (same scope note as the prior entries).
This entry is **in progress**; it is checkpointed after recon so the plan and the full-set
definition survive compaction. The fresh-VM run (provision → full-set install → GDM login →
verify → parity matrix) follows in subsequent turns of this same entry and will append its
verdict below this checkpoint.*

**Scope (from `## Next Actions`, the two open `Big` items):**

- **3.1 — fresh-VM end-to-end:** a clean Rocky 10 VM, install the full set from the local DNF
  repo, GDM login into Cinnamon (Wayland), verify terminal + control-center + wallpaper + panels
  open with zero manual `dnf` steps. A11y waits use `A11Y_APP`; `toolkit-accessibility=true` is set
  first.
- **3.2 — full parity re-run:** re-run the 11-row parity matrix (item 2.2) against
  `fedora-cinnamon-ref`, expecting 11/11. The two prior Rocky FAILs (Cinnamon Settings python
  deps; terminal) are closed in the 67-RPM repo (Tails, 2026-09-17), so both rows should now PASS.

**Recon facts (2026-09-18):**

- Repo: `/home/howard/Linux/projects/cinnamon-for-rocky10/rpms/` holds 67 RPMs + `repodata/`.
  The runtime (non-`debuginfo`/`debugsource`/`-devel`) set is **22 packages**: `cinnamon`,
  `cinnamon-control-center`, `cinnamon-desktop`, `cinnamon-menus`, `cinnamon-rocky-defaults`,
  `cinnamon-session`, `cinnamon-settings-daemon`, `cjs`, `gdk-pixbuf-parsers`, `gnome-terminal`,
  `gtk-layer-shell`, `mozjs115`, `muffin`, `muffin-clutter`, `muffin-cogl`, `nemo`,
  `python3-pillow`, `python3-setproctitle`, `python3-tinycss2`, `python3-webencodings`,
  `python3-xapp`, `xapps-lib`. Two packages ship two versions (`cinnamon-desktop` 1+2,
  `cinnamon-settings-daemon` 1+2); a name-based `dnf install` resolves the latest of each.
- **Full-set install (the "zero manual dnf steps" command):** stage the repo, run
  `repo-setup/setup-repo.sh`, then `dnf install -y` of the 22 runtime names above.
  `cinnamon-rocky-defaults` carries `Requires: rocky-backgrounds` + `Requires: rocky-logos`
  (verified in `spec/cinnamon-rocky-defaults.spec:23-24`), so the wallpaper and branding system
  packages are pulled in by the dependency chain, not by a manual step. GDM is a system display
  manager, installed as test-environment setup (separate from the Cinnamon set), matching the
  2.1/2.2 harness pattern. Any dependency that still must be added by hand is a finding, not a
  silent fix.
- Fleet (`virsh -c qemu:///system list --all`): `gdm-login-vm` running (**not** used as the fresh
  VM); `ref-overlay-task0017` running (id 79, the disposable reference overlay used for the 0.3
  baseline); `fedora-cinnamon-ref` shut off (pristine, never booted); `rocky10-explore` shut off.
- Harness map: `vm-test/provision-vm.sh` (fresh VM, `--name`/`--graphics vnc`);
  `tasks/lib/gdm-drive.sh` (`gdm_login`/`gdm_wait_session`), `tasks/lib/gdm-a11y.py`
  (`A11Y_APP` a11y waits), `tasks/lib/ukey.c` (uinput keyboard for the greeter);
  `repo-setup/setup-repo.sh` (local DNF repo); `vm-test/parity/parity-inventory.sh` (11-row
  read-only inventory). The ref-side of the 3.2 matrix reuses the 0.3 baseline in
  `vm-test/parity/fedora-ref/`: the reference is unchanged, the pristine ref was never booted,
  and the overlay baseline stands.
- Prior matrix state (item 2.2): 9 rows PASS both sides; the Rocky FAILs were Cinnamon Settings
  (+ the extension/applet/desklet manager, themes selector, and power settings panel it hosts)
  and terminal. Both are closed in the repo, so 3.2 expects 11/11.

**Method (3.1 + 3.2, one fresh VM):**

1. Provision a fresh Rocky 10 VM (`provision-vm.sh --name <name> --graphics vnc`); wait for SSH;
   record IP + VNC display.
2. Test-environment setup (recorded, not part of the Cinnamon set): SELinux permissive;
   `dnf install gdm`; create the test user with a password and add it to the `input` group (the
   ukey harness needs `/dev/uinput`); stage `gdm-drive.sh`/`ukey.c`/`gdm-a11y.py` and build the
   ukey driver.
3. Full-set install: stage the `rpms/` tree + `setup-repo.sh`, run the repo setup, then
   `dnf install -y` of the 22 runtime names. No further `dnf install` may be needed.
4. Reboot to the GDM greeter; `gdm_login <user> <passfile> cinnamon-wayland`; `gdm_wait_session`.
5. Set `toolkit-accessibility=true` (prerequisite for the a11y waits).
6. Verify (3.1): panels render, wallpaper renders (screenshot + pixel stats), terminal opens
   (`A11Y_APP=gnome-terminal` a11y wait + AT-SPI tree), control-center opens (a11y wait + tree),
   main menu opens. Screenshot each.
7. Parity (3.2): run `parity-inventory.sh` → `vm-test/parity/rocky10/` (new dated set); capture
   the 11 staged screenshots via `virsh screenshot`; populate the 11-row matrix against the 0.3
   ref baseline.
8. Record the matrix + verdict in this entry.

**Status at checkpoint:** recon complete; no changes to the repo, the reference, or any pre-existing
running VM.

**Fresh VM (provisioned 2026-09-18):** `task0017-fresh-vm`, IP `192.168.122.153`, VNC
`127.0.0.1:1` (connect to host:1), disk `/var/lib/libvirt/images/cinnamon-test/task0017-fresh-vm.qcow2`,
SSH ready (fleet key; host key pinned out-of-band from the disk image per `lib.sh`). It is a fresh
Rocky 10 cloud image with no Cinnamon installed. Provisioned via `vm-test/provision-vm.sh --name
task0017-fresh-vm --graphics vnc`.

**Step 1 (test-env setup) — DONE 2026-09-18:**

- SELinux set Permissive (`setenforce 0` + `/etc/selinux/config` so it persists); `getenforce` =
  `Permissive` after.
- Display manager + greeter installed as **test environment** (not part of the Cinnamon set):
  `dnf install -y gdm gnome-shell` → `gdm-47.0-24.el10_2`, `gnome-shell-49.4-9.el10_2.rocky.0.2`
  (GDM 47 is Wayland-only on EL10; the greeter is gnome-shell/mutter). `systemctl enable gdm`,
  `systemctl set-default graphical.target`.
- Ephemeral test user `gdmtest` created (`useradd -m -s /bin/bash`), random password generated
  in-VM to `/root/gdmtest.pass` (mode 0600, never leaves the VM), added to the `input` group
  (`id -nG gdmtest` → `gdmtest input`). ukey runs as root, which owns `/dev/uinput` (0600
  root:root), so the group is belt-and-suspenders.
- ukey uinput driver built at `/root/gdm-harness/ukey` (build deps `gcc`/`kernel-headers`/
  `python3-dbus` all already present from the cloud image); `gdm-drive.sh` + `gdm-a11y.py` staged
  to `/root/gdm-harness/`.

**Step 2 (full-set install) — DONE 2026-09-18:**

- `rpms/` (67 RPMs + `repodata/`) + `repo-setup/` staged to `/root/`; `bash
  /root/repo-setup/setup-repo.sh /root` configured the `cinnamon-rocky10` file:// repo and enabled
  `crb`; `dnf makecache` succeeded (repo readable, metadata valid).
- Runtime set **derived from the repo** (`dnf repoquery --repo=cinnamon-rocky10 --qf '%{name}'`
  minus `-devel`/`-debuginfo`/`-debugsource`) = exactly the 22 names in the checkpoint. Installed
  with **one** `dnf install -y` of those 22 names; rc=0, all 22 present (`rpm -q` each, none
  missing). Versions: cinnamon/muffin/muffin-clutter/muffin-cogl/nemo 6.7.4,
  cinnamon-control-center/cinnamon-desktop/cinnamon-settings-daemon 6.7.2, cinnamon-menus 6.7.0,
  cinnamon-rocky-defaults 1.0, cinnamon-session 6.7.3, cjs 6.4.0, gdk-pixbuf-parsers 2.42.12,
  gnome-terminal 3.54.5, gtk-layer-shell 0.10.1, mozjs115 115.29.0, python3-pillow 12.3.0,
  python3-setproctitle 1.3.7, python3-tinycss2 1.5.1, python3-webencodings 0.5.1, python3-xapp
  3.0.2, xapps-lib 3.3.3.
- **Zero additional manual `dnf` steps confirmed.** The single install pulled the system deps by
  resolution: `rocky-backgrounds-100.5-3` (wallpaper set, `/usr/share/backgrounds/rocky-default-10-*.png`
  present), `rocky-logos-100.5-3` (background/screensaver gschema defaults + gdm logo),
  `gsettings-desktop-schemas-47.1-4`, `python3-psutil-5.9.8` (xapp dep). No second `dnf install`
  was needed. Install-log warnings are glib schema deprecation notices only (no errors, no
  "not installed").
- Session entries present: `/usr/share/wayland-sessions/cinnamon-wayland.desktop` and
  `/usr/share/xsessions/cinnamon.desktop`. `cinnamon` ships 34 applets; note
  `/usr/share/cinnamon/themes/` and `/usr/share/cinnamon/extensions/` are empty in this build
  (default theme is built into the shell) — to be verified live in step 4.
- Evidence in-VM under `/root/evidence/`: `step1-gdm.log`, `step2-setup-repo.log`,
  `step2-runtime-set.txt`, `step2-install.log`, `step2-versions.log`, `step2-sessions.log`,
  `step2-autodeps.log`.

**Step 3 (GDM login + a11y) — DONE 2026-09-18:**

- `virsh reboot` → VM back at `192.168.122.153`; `gdm_wait_greeter` + `gdm_greeter_ui_ready`
  both PASS (greeter a11y UI ready; face list shows `gdmtest`, Login code, Submit, Accessibility).
- `gdm_login gdmtest /root/gdmtest.pass cinnamon-wayland` PASS: clicked the user, selected the
  "Cinnamon (Wayland)" session, caps probe verified lowercase, typed password, submitted.
  `gdm_wait_session` → **session 7, type=wayland, state=active, proc=`cinnamon-session`**.
- Running desktop processes for `gdmtest`: `cinnamon-sessio`, `cinnamon` (shell, pid 3365),
  `nemo-desktop`, `cinnamon-calend` (calendar applet), `csd-settings-re`, `csd-xsettings`.
- Cinnamon shell a11y tree reachable (`A11Y_USER=gdmtest A11Y_APP=cinnamon`): panel, Applets,
  Menu, "All Applications", Account details, System Settings, Backgrounds, Date & Time, etc.
- `toolkit-accessibility` set to **true** for gdmtest (first attempt failed: `runuser` inherited
  root's `XDG_RUNTIME_DIR` → dconf hit `/run/user/0`, value stayed `false`; fixed by routing
  gsettings through the session bus `unix:path=/run/user/1000/bus` + `XDG_RUNTIME_DIR=/run/user/1000`).
- Evidence in-VM: `step3-greeter-text.log`, `step3-greeter-tree.log`, `step3-session-tree.log`.

**Step 4 (3.1 verification) — DONE 2026-09-18:**

Evidence under `vm-test/evidence/task0017-fresh-3.1/2026-09-18/` (1280x800 screenshots from
`cinnamon-screenshot` run as `gdmtest` in the session env; pixel stats via the harness PIL helper).
All five 3.1 surfaces verified on `task0017-fresh-vm` after a clean GDM login. The session was reset
once mid-step (a menu that would not dismiss via ukey input left the screen in a dimmed state); the
reset returned a verified clean desktop (`05-desktop-restore.png`), and the main menu was re-captured
cleanly in the reset session. The terminal and control-center captures are from the first session and
the menu/restore from the second; each capture independently proves its surface opened.

| Check | What it exercises | Result | Notes |
|---|---|---|---|
| C1 panel render | compositor surfaces the panel | PASS | single bottom panel strip @0,759 1280x40; no top panel; 8 applets installed |
| C2 wallpaper render | nemo-desktop composites the background | PASS | gemstone-skies-time.xml renders; day mean rgb (49,10,38), night (33,1,24) |
| C3 terminal open | gnome-terminal (source-built) launches from the set | PASS | a11y frame 'gdmtest@localhost:~' 708x572; closes the A1 terminal gap |
| C4 control-center open | cinnamon-control-center (System Settings) launches | PASS | a11y frame 'System Settings' 794x268; closes the 2.2 settings-deps gap |
| C5 main menu open | menu applet opens and renders content | PASS | full menu a11y structure; rendered app-grid content in the capture |

**C1 (PASS) - panel:** the full shell a11y tree (`04-shell-full-tree.txt`) shows a single bottom
panel as a full-width strip `@0,759 1280x40` and **no top panel** (no width>=1200 bar at y<60).
Applets are installed for the user under `/home/gdmtest/.config/cinnamon/spices/`: menu,
grouped-window-list, clock, sound, network, power, notifications, cornerbar (8). No custom panel
JSON, so this is the built-in default layout. The menu button is the leftmost 32x32 applet at the
bottom-left (center ~ (21,779)); the clock sits bottom-right. `01-panels-config.txt` records the
applet set.

**C2 (PASS) - wallpaper:** `org.cinnamon.desktop.background picture-uri` =
`file:///usr/share/backgrounds/rocky-default-10-gemstone-skies-time.xml` (a **time-of-day**
day/night sky), `picture-options` = `zoom`; the file plus the day/night PNGs are owned by
`rocky-backgrounds`, pulled in by the `cinnamon-rocky-defaults` dependency (no manual step). Base
capture `01-desktop-base.png`: 18833 unique colours, max single bucket 30.59%, mean rgb (49,10,38),
VARIED — the sky renders, not a black surface. This is the fix over the 2.1 nemo-desktop compositing
FAIL, which was on the old `gdm-login-vm` (virtio-vga); the fresh `provision-vm.sh --graphics vnc`
VM composites the nemo-desktop surface correctly. The wallpaper is time-based: an evening capture
measures mean (49,10,38) and a night capture (after the mid-step reset) measures (33,1,24), matching
the 2.2 night-variant stats (mean (33.1,1.6,24.9)) — same file, different sky phase, not a defect.

**C3 (PASS) - terminal:** `gnome-terminal 3.54.5` (source-built by Tails, in the 22-package set)
launches from the set. a11y (`A11Y_APP=gnome-terminal`, `02-terminal.a11y.txt`): `[application]
'org.gnome.Terminal'` -> `[frame] 'gdmtest@localhost:~' @(0,0 708x572)`; `gnome-terminal-server`
process present. Capture `02-terminal.png`: 2785 unique, max bucket 68.96%, mean (14,2,10), VARIED
(dark terminal over the wallpaper). **Closes the A1 terminal gap** (gnome-terminal absent from
EL10/EPEL repos; now provided by the set).

**C4 (PASS) - control-center:** `cinnamon-control-center 6.7.2` launches. a11y
(`A11Y_APP=cinnamon-control-center`, `03-control-center.tree.txt`): `[application]
'cinnamon-control-center'` -> `[frame] 'System Settings' @(0,0 794x268)`, pid 4429, with a
'System Settings' label at (336,32). Capture `03-control-center.png`: 3087 unique, max bucket
70.03%, mean (14,2,10), VARIED. This is the new Cinnamon control center (System Settings), the 6.7
successor to the old `cinnamon-settings` app whose missing python deps (setproctitle/pillow/tinycss2)
caused the 2.2 FAIL; those three are now in the set as `python3-setproctitle`/`python3-pillow`/
`python3-tinycss2`. (The old `cinnamon-settings` package is not in the 22-package set; whether it
ships and runs is a 3.2 parity row.)

**C5 (PASS) - main menu:** the menu applet opens and renders. Two independent signals:

- a11y: `04-main-menu-open.txt` (clean capture, no other windows open) shows the full Cinnamon
  main-menu structure — sidebar (All Applications, Accessories, Preferences, Administration,
  Favorites, Recent Files), Places (Desktop/Documents/Music/Pictures/Videos/Downloads), a Search
  entry, and the populated app grid.
- pixels: `04-main-menu.png` is 1.3% bright, with the content structured in the left-center (a
  17.7% block at the center app-grid region plus the sidebar column) over a dark menu surface —
  the rendered menu, captured in a session with no terminal/control-center window to confuse the
  evidence.
- **A11y caveat (recorded, not a defect):** the Cinnamon shell tree *always* contains the main-menu
  and panel-context-menu node structure at @0,0 extents (latent) even when closed — the same quirk
  noted for the panel applets. So marker *presence* in the tree is not an open/closed signal; the
  rendered pixel content is the proof. Menu content nodes report relative @0,0 extents, so menu
  location comes from pixels, not a11y extents.
- The menu did not dismiss via ukey Escape / desktop-click in this build (the screen stayed in the
  dimmed menu state); a session reset returned a clean desktop (verified, `05-desktop-restore.png`).
  Input-path quirk, not a product defect; 3.1 asked for open + render, both of which hold.

**Checks requested vs run:** 5 surfaces requested (panels, wallpaper, terminal, control-center,
main menu), 5 executed.

**Verdict (3.1):** all five surfaces PASS on the fresh VM. The full set installed with one
`dnf install` (step 2), and every 3.1 target — terminal (A1 gap closed) and control-center (2.2
settings-deps gap closed) included — opens from that set with zero manual `dnf` steps. The wallpaper
is the time-based Rocky sky (day/night) and renders correctly on the fresh VNC VM (the 2.1
nemo-desktop compositing FAIL does not reproduce here). No code bugs found in 3.1; the one input
quirk (menu not dismissing via ukey) is a harness/environment note, not a product defect.

**Step 5 (3.2 full parity re-run) — DONE 2026-09-18:**

Re-ran `vm-test/parity/parity-inventory.sh` on `task0017-fresh-vm` into
`vm-test/parity/rocky10/2026-09-18-3.2/` (`inventory-rocky10-3.2.txt`) and re-opened the runtime
targets. The structured inventory covers every row's facts; the runtime rows that 2.2 could not
confirm (Cinnamon Settings opens, nemo opens, terminal opens) were re-verified by launching the
app in the session env and checking the process survives plus a rendered (non-black) screenshot.
The two prior FAILs (row 7 Cinnamon Settings, row 10 Terminal) were the only rows the 67-RPM set
was built to move.

| # | Item | Fedora ref (0.3, expected) | Rocky 10 (actual, 3.2) | Status |
|---|---|---|---|---|
| 1 | Panel applets | default set, single bottom panel | single bottom panel (`PANELS_ENABLED ['1:0:bottom']`); menu, grouped-window-list, systray, notifications, printers, removable-drives, keyboard, favorites, network, sound, power, calendar, cornerbar; 34 applet dirs | PASS |
| 2 | Wallpaper | default_blue.jpg (desktop-backgrounds-basic) | gemstone-skies-time.xml day/night (rocky-backgrounds, via cinnamon-rocky-defaults); renders VARIED | PASS |
| 3 | Branding | fedora-logo-sprite (fedora-logos) | fedora-logo-icon; icon file owned by rocky-logos (Rocky logo) | PASS |
| 4 | Themes | Mint-Y-Dark-Aqua (cinnamon+GTK), Mint-Y-Aqua icon | empty cinnamon theme, Adwaita GTK, gnome icon; 19 shell assets (intentional divergence) | PASS |
| 5 | Extension/applet/desklet manager | present, 3 desklets, manager module + 3 panels | present, 3 desklets, cs_extensions.py + applets/desklets/extensions panels; app opens | PASS |
| 6 | Screensaver | cinnamon-screensaver 6.6.1, no service | folded into shell at 6.7 (js/ui/screensaver present), no service, lock-enabled true | PASS |
| 7 | Cinnamon Settings | present, opens (stale python deps) | 32 panels; app launches + stays up (no crash); settings.py bundled in cinnamon pkg + setproctitle/pillow/tinycss2 installed | PASS (2.2 FAIL closed) |
| 8 | Main menu | opens | opens + renders (3.1 C5) | PASS |
| 9 | nemo | nemo 6.6.3 | nemo 6.7.4, file manager opens (window renders center, only benign theme warnings) | PASS |
| 10 | Terminal | gnome-terminal 3.60.0 | gnome-terminal 3.54.5 (source-built, in the set), opens (3.1 C3) | PASS (2.2 FAIL closed) |
| 11 | Session/power controls | power applet, idle 900 | power applet, power panel, idle 900, no separate session panel (6.7) | PASS |

**Checks requested vs run:** 11 parity rows requested, 11 evaluated (5 runtime rows — settings,
main menu, nemo, terminal, session — additionally confirmed by launching the app and checking the
process survives plus a rendered screenshot; the rest by structured inventory).

**Row 7 FAIL closure (evidence):** `cinnamon-settings` is a wrapper shipped by the `cinnamon-6.7.4`
package that execs `/usr/share/cinnamon/cinnamon-settings/cinnamon-settings.py`. In the 2.2 state
that python module lived in a separate `cinnamon-settings` package that was not installed, and the
three runtime deps were missing, so every panel crashed on launch with a python traceback. Now the
`cinnamon-settings.py` (37993 bytes) is bundled in the `cinnamon-6.7.4` package, and the set
installs `python3-setproctitle-1.3.7`, `python3-pillow-12.3.0`, `python3-tinycss2-1.5.1`. Launching
`cinnamon-settings default` in the session env left the process (pid 9502) alive at 05:36 elapsed
with an empty stderr log (no traceback) and a rendered settings window (`2026-09-18-3.2-06-cinnamon-settings.png`,
1959 unique colours, VARIED). The 2.2 crash-on-launch is closed.

**Row 10 FAIL closure (evidence):** 2.2 had no gnome-terminal (not in EL10/EPEL). The set now
ships `gnome-terminal-3.54.5-1.el10` (source-built by Tails); it launches and opens
(3.1 C3: a11y frame 'gdmtest@localhost:~' 708x572). Closed.

**Documented divergences (not defects, match the 2.1/2.2 notes):** themes (row 4) use the empty
cinnamon theme + Adwaita GTK + gnome icon rather than Fedora's Mint-Y; wallpaper (row 2) is
Rocky's time-based sky rather than Fedora's blue tile; branding (row 3) is the Rocky logo rather
than the Fedora logo. nemo (row 9) logs a benign `Adwaita`-has-no-nemo-styling warning and adds
fallback; no functional impact.

**Step 6 — final verdict for item 3:**

**3.1:** all five surfaces PASS (panel, wallpaper, terminal, control-center, main menu) on the
fresh VM, installed from the local repo with zero manual `dnf` steps (steps 2-4 above).

**3.2:** the full parity matrix is **11/11 PASS** against the 0.3 Fedora ref baseline. Both prior
FAILs — Cinnamon Settings (row 7) and Terminal (row 10) — are closed by the 67-RPM set. The
remaining differences from the Fedora ref are the intentional branding/theme divergences
documented above, not functional gaps.

**Item 3 (3.1 + 3.2): COMPLETE.** No product code bugs found; the two harness/environment notes
(the Cinnamon shell a11y tree keeps the menu/panel node structure latent so marker presence is not
an open/closed signal; the menu not dismissing via ukey input) are recorded, not defects.

### Trio close — test-execution review (Big, 2026-09-18)

Third reviewer of the trio (Shadow → Omega → Big). Scope: what the 3.1/3.2 runs prove and don't,
harness robustness, and the settings-RPM one-liner. Every claim below is verified by a command
run on 2026-09-18, not by reading the diff.

**Host recovery note (state, not a finding):** at 14:10 the system `libvirtd` was **inactive**;
plain `virsh` connected to the session driver, which has empty state, so all VMs appeared
destroyed. `sudo systemctl enable --now libvirtd` restored the daemon, the autostarted `default`
network, and all three persistent domains (`gdm-login-vm`, `ref-overlay-task0017`,
`task0017-fresh-vm`); `task0017-fresh-vm` re-leased `192.168.122.153`
(`virsh -c qemu:///system net-dhcp-leases default`). The `virbr0` bridge was then left DOWN on
the host side (IP configured, no L2 forwarding), which blocked host-to-guest traffic;
`sudo ip link set virbr0 up` restored it (ping 0% loss).

**Settings-RPM one-liner (Next Actions item) — PASS.** Run on `task0017-fresh-vm` (pinned SSH):

```
$ rpm -qa | grep cinnamon-settings
cinnamon-settings-daemon-6.7.2-2.el10.x86_64    # substring match; different package
$ rpm -q cinnamon-settings
package cinnamon-settings is not installed      # exit 1
```

The old separate `cinnamon-settings` RPM is absent, consistent with the row-7 closure (settings
UI bundled in `cinnamon-6.7.4-3.el10`; `rpm -q cinnamon` → `cinnamon-6.7.4-3.el10.x86_64`).

**What the 3.1/3.2 runs prove** (verified on disk and on the live VM):

- Fresh minimal Rocky 10.2 VM; the full set installed with one `dnf install` after
  `setup-repo.sh`, zero additional manual dnf steps (3.1 step 2).
- GDM login to Cinnamon Wayland; 5/5 surfaces (panel, wallpaper, terminal, control-center, main
  menu) with a11y + pixel evidence.
- Parity matrix 11/11 vs the 0.3 Fedora ref baseline; both 2.2 FAILs closed (row 7 settings,
  row 10 terminal).
- Evidence on disk verified: `vm-test/evidence/task0017-fresh-3.1/2026-09-18/` holds all 5
  surface PNGs plus a11y/pixelstats/bands data (22 files).
  `vm-test/parity/rocky10/2026-09-18-3.2/` holds 5 of 11 captures plus the structured inventory —
  the 6 missing captures are Shadow finding 5 (untracked + missing), not re-listed here.
- Live re-check of the acceptance VM today: `cinnamon-6.7.4-3.el10`,
  `cinnamon-desktop-6.7.2-2.el10`, `gnome-terminal-3.54.5-1.el10`,
  `cinnamon-rocky-defaults-1.0-1.el10.noarch`, `gdk-pixbuf-parsers-2.42.12-1.el10`,
  `nemo-6.7.4-2.el10`, `mozjs115-115.29.0-1.el10` all present (833 packages installed total).

**What the 3.1/3.2 runs do NOT prove (coverage gaps):**

1. **The acceptance install was run by hand; no script in the branch reproduces it.** The 22
   package names were derived (repoquery minus -devel/-debuginfo/-debugsource) and typed into the
   dnf command; they are not encoded anywhere in the repo. `INSTALL.md` still documents the
   14-package era: "All 14 base packages install cleanly" (`INSTALL.md:5`); the install commands
   omit gnome-terminal, the five control-center Python RPMs, and `cinnamon-rocky-defaults`
   (`INSTALL.md:30-40`); the version table lists superseded builds
   (`cinnamon-desktop 6.7.2-1.el10`, `cinnamon 6.7.4-1.el10`; `INSTALL.md:143,150`). The
   documented install path in the branch does not produce the accepted set.
2. **`vm-test/run-tests.sh` (the canonical install harness, TASK-0003) was never run
   end-to-end against the final 67-RPM set** and cannot gate a CI-style run:
   - Exit-code swallowing: `install_rc` captured at `run-tests.sh:191` is never read; `verify_rc`
     is warning-only at `run-tests.sh:256-259` ("WARNING: Package verification had issues") and
     the script proceeds to exit 0. A completely broken install reports green.
   - Phase 2 (`run-tests.sh:106-113`) is structurally incapable of installing anything on a fresh
     VM: `mozjs115` resolves only from the local `cinnamon-rocky10` repo (verified on the host:
     `dnf repoquery --available mozjs115` → `mozjs115 => cinnamon-rocky10`; a fresh VM has no such
     repo until Phase 3), and `clutter`/`cogl` do not exist as EL10 packages (unresolvable even on
     the host, which has the local repo enabled; the script's own comment concedes they are
     "bundled in muffin"). By dnf atomicity the three resolvable packages in that command
     (gsettings-desktop-schemas, rocky-backgrounds, rocky-logos) also do not install. The
     `|| echo "WARNING: ..."` swallows the certain failure, and the `SYSTEM_DEPS` array
     (`run-tests.sh:28-30`) is dead code. The comment "runtime libraries not provided by our
     custom RPM build" (`run-tests.sh:102-103`) is stale — mozjs115 IS provided as a custom RPM.
3. **SELinux enforcing is untested.** The acceptance VM is `Permissive` (live check:
   `getenforce` → `Permissive`). It inherited the mode: the harness itself sets permissive for
   testing (`run-tests.sh:98 setenforce 0`) and 3.1 step 1 repeated it. Rocky's default is
   enforcing; the desktop has never run under enforcing, so there is no AVC evidence either way.
4. **Reboot persistence is single-boot only.** 3.1 was install → reboot → login. A second boot,
   an in-place `dnf upgrade` of the set, and remove/reinstall are untested.
5. **The a11y latent-node quirk (recorded in 3.1 C5) remains the arbiter hazard.** A future
   automated gate keyed on a11y marker presence alone would pass on a closed menu. Pixels are the
   open/closed signal; the current harness uses them correctly — keep it that way.

**New findings (trio close).** None duplicates Shadow (8) or Omega (4).

| # | Severity | What | Where | Owner |
|---|---|---|---|---|
| T1 | should-fix | Install/verify exit codes swallowed; a fully failed install exits 0 | `vm-test/run-tests.sh:191` (install_rc unused), `:256-259` (verify_rc warning-only) | Tails |
| T2 | low | Phase 2 dead: mozjs115 local-repo-only, clutter/cogl absent from EL10, atomic dnf installs nothing, certain failure swallowed; `SYSTEM_DEPS` dead | `vm-test/run-tests.sh:28-30`, `:102-113` | Tails |
| T3 | low | Accepted 22-package install set not encoded in the repo; `INSTALL.md` is 14-package-era and stale | `INSTALL.md:5`, `:30-40`, `:133-150` | Tails (list) + Vector (docs) |

None touches a product RPM; all are harness/docs.

**Re-verification asks for Tails** (after Shadow's blocker is resolved):

1. Fix T1/T2, then run `run-tests.sh` end-to-end against the rebuilt full set on a fresh VM so
   the acceptance install is reproducible from the branch.
2. Enforcing-SELinux smoke: boot the installed VM under enforcing, GDM-login, open the five
   surfaces; record any AVCs in `## Test Results`.
3. (Cheap, optional) second reboot + `dnf upgrade` of the set on the same VM.

**Checks requested vs run:** 5 requested, 5 executed — the settings-RPM one-liner on the
acceptance VM; live package/SELinux re-check of the VM; 3.1 evidence directory verification; 3.2
evidence directory verification; harness file review of `run-tests.sh`, `lib.sh`, `gdm-drive.sh`,
`gdm-a11y.py`, `ukey.c`, `parity-inventory.sh`, `setup-repo.sh`, `provision-vm.sh`,
`test-gdm-login.sh` with targeted `dnf repoquery`/`virsh`/`rpm` commands. Nothing silently
dropped. No CI workflows exist in this repo (the plan chose the custom libvirt harness over
CI/Sparky; that choice is not revisited here).

**Verdict:** the test-execution review found no new blockers. One should-fix (T1) and two low
(T2, T3), all harness/docs; zero in product RPMs. The one-liner PASSES: the old separate
`cinnamon-settings` RPM is absent. The 3.1/3.2 runs prove fresh-VM install + desktop function of
the final set, but do not prove reproducibility from the branch (gaps 1–2), enforcing-SELinux
behaviour (gap 3), or multi-boot persistence (gap 4). **Mergeable after Tails** resolves
Shadow's blocker (spec reproducibility) and T1 (exit codes), then the two mandatory
re-verifications (run-tests.sh end-to-end; enforcing smoke) pass.

*Entry 2026-09-19: re-verification B + C on fresh VM `t17-revB` (Tails, post-review; direct
VM verification, no CI in this repo, so the standard compile/linter/unit/Sparky table does not
apply). VM: fresh Rocky 10.2 cloud image via `provision-vm.sh --name t17-revB --graphics vnc`,
IP 192.168.122.18, kernel 6.12.0-211.16.1.el10_2.0.1.x86_64; guest clock UTC, host-local
date 2026-09-19 (JST).

**B — `run-tests.sh` end-to-end on the fresh VM: PASS.**

| Check | What it exercises | Result | Notes |
|---|---|---|---|
| Phase 3 single-dnf install | T2 (dead native-deps block removed; all deps from the set + native repos) | PASS | Attempt 1 (all 64 RPMs in one `dnf install`) succeeded; no `--allowerasing`, no ordered-install fallback |
| Phase 3 install rc gate | T1 (install failure must fail the harness) | PASS (gate exercised in code path) | rc captured and checked (`run-tests.sh:184-190`); harness exited 0 |
| Phase 4 verify | T3 (22-name set from `install-set.txt`) | PASS | 22/22 `[OK]` with versions (cinnamon 6.7.4-3, muffin 6.7.4-3, nemo 6.7.4-2, cjs 6.4.0, ...), mozjs-115 headers present, `=== ALL PACKAGES VERIFIED ===` |
| GDM login | greeter → session | PASS | `gdm_login gdmtest /root/gdmtest.pass cinnamon-wayland`; session 9 type=wayland state=active; `cinnamon-session-binary --session cinnamon-wayland`, `cinnamon --replace`, `nemo-desktop` running |
| `ukey key Super_L` menu open | META mapping (`ukey.c:124`, fix `55e37bd`) end-to-end | PASS | a11y tree after the keypress shows the open main menu (category list: All Applications / Accessories / Preferences / Administration / Favorites / Recent Files, app grid @(293,342 369x337)); the `All Applications` marker occurs 0 times in the 3.1 closed-desktop baseline tree; screenshot `revB-menu.png` (1280x800, `cinnamon-screenshot` as gdmtest) |

Test environment (not part of the Cinnamon set, mirrors 3.1 step 1): `dnf install gdm
gnome-shell` (gdm-47.0-24.el10_2, gnome-shell-49.4-9.el10_2.rocky.0.2), ephemeral user
`gdmtest` with a random in-VM password (`/root/gdmtest.pass`, 0600, never leaves the guest),
`input` group, ukey driver built at `/root/gdm-harness/ukey`.

**C — enforcing-SELinux smoke on the same VM: PASS.** `run-tests.sh` Phase 2 ran `setenforce 0`
(runtime only); `/etc/selinux/config` stayed `SELINUX=enforcing`, so the post-reboot boot was
**Enforcing** (`getenforce` = Enforcing) for the whole login + surface pass.

| Check | What it exercises | Result | Notes |
|---|---|---|---|
| Boot enforcing | persistent enforcing config | PASS | `getenforce` Enforcing after reboot |
| GDM login under enforcing | PAM + session start | PASS | session 9 active, wayland |
| Panel | render | PASS | a11y tree panel nodes; panel-strip pixel stats avg=(71,23,65) |
| Wallpaper | render | PASS | wallpaper region pixel stats avg=(60,17,54), 8782 unique colours (real image, not flat) |
| Terminal | open + a11y | PASS | `gnome-terminal` launched, a11y frame `gdmtest@localhost:~` with window controls |
| Control center | open + a11y | PASS | `cinnamon-control-center` launched, a11y frame `System Settings` |
| Main menu | open via Super | PASS | same as B (ukey Super_L, a11y + screenshot) |
| AVC denials | SELinux policy sufficiency | PASS | `grep -c 'avc:  denied' /var/log/audit/audit.log` → 0 (fresh boot, log spans the whole enforcing session); `ausearch -m avc -ts recent` empty |

**Harness timing observation (not a product defect):** `gdm_wait_session`'s 150 s window
timed out with "last: none", yet the systemd-logind journal shows "New session 9 of user
gdmtest" at 16:04:30 — inside the window — and the session was verified active (type=wayland,
`cinnamon-session` running) shortly after. Suspected `loginctl` visibility lag right after
creation. The session and the desktop are healthy; the wait's final-state message is
misleading in that case.

**Evidence:** `vm-test/evidence/task0017-revB/2026-09-19/` (menu screenshot + a11y trees,
pixel stats, login/menu/surfaces logs) committed in project `d128848`; install Phases 1–4
block (lines 3224–4914) in `vm-test/results/install.log` (gitignored, append-only across
runs). Trio-close optional ask 3 (second reboot + `dnf upgrade`) not run (optional; B+C are
the mandatory re-verifications).

**Verdict:** B PASS, C PASS. All three post-review re-verifications (A clean-checkout rebuild,
B run-tests end-to-end, C enforcing smoke) are complete. Remaining chain: Vector docs →
Knuckles PR.

---

## Docs

*Owner: `Vector`.*

*Vector, 2026-09-19. Project commit `9848143` on `feature/TASK-0017-cinnamon-desktop-completeness`.
House style kept (no em dashes, prose over bullets, bounded uncertainty).*

| File | Sections touched | What changed |
|---|---|---|
| `README.md` | Status, What the complete set adds, Build notes, Test results, Project structure, License | Replaced the 14-package-era content (10-component table, "48 RPMs" count, "muffin built X11-only (no Wayland)" claim) with the final state. 64 RPMs published, 22 runtime names in `vm-test/install-set.txt` as the install set, single-`dnf` fresh-VM install, GDM Wayland login. Added the delta table (8 new packages, 2 rebuilt), the gnome-terminal 3.54.5 vs reference 3.60.0 recorded deviation, the 11/11 parity result with the three intentional branding divergences, and the 2026-09-18/19 verification results (fresh-VM, `run-tests.sh` end-to-end, enforcing-SELinux smoke, clean-checkout rebuild). Build notes now say muffin is built with Wayland (`spec/muffin.spec:115`, `-Dwayland=true`). Project structure gained `repo-setup/`, `tasks/`, and the `vm-test/install-set.txt` reference |
| `INSTALL.md` | Current status, Quick start, Manual repository setup, Direct RPM install, Prerequisites, Installed packages, GDM session configuration, Troubleshooting | Replaced the 14-package content (two-command install with `xorg-x11-server-Xwayland`, the 14-row version table, the manual base-dependency list, the mozjs115 first-install ordering note). Install is now the single `dnf install` of the 22 runtime names from `vm-test/install-set.txt`, with the verified auto-pull of `rocky-backgrounds`, `rocky-logos`, `gsettings-desktop-schemas`, `python3-psutil`. GDM section updated for EL10 GDM 47 Wayland-only login into `cinnamon-wayland` (verified environment installs `gdm` + `gnome-shell`). Installed-packages table now lists all 22 runtime names with published NVRs. Wallpaper-black troubleshooting cites `gdk-pixbuf-parsers` + the `cinnamon-desktop-6.7.2-2.el10` compositing fix; SELinux section cites the zero-AVC-denial smoke result. The direct-RPM fallback is documented as the `run-tests.sh` harness path (64 RPMs, first attempt, 2026-09-19) |

**Checked and needed no change:** `CHANGELOG.md` (no such file exists in the project repo, so the
template row does not apply), `repo-setup/setup-repo.sh` (the documented behaviour still matches
the script: createrepo_c install, metadata generation, `.repo` file, CRB enable, validation),
`vm-test/install-set.txt` (22 runtime names, the source of truth, unchanged by this task),
project `LICENSE` (GPL-2.0 header, unchanged).
**Could not verify:** whether `dnf install gdm` alone (without `gnome-shell`) is sufficient for
the greeter on EL10. The docs install both, which is the verified test environment. Running
`dnf install gdm` on a fresh EL10 VM and checking whether the greeter starts would settle it.

---

## Release

*Owner: `Knuckles`.*

**DONE checklist verified:** yes (2026-09-19). All 17 `## Definition of Done` boxes verified
against in-doc evidence: package set / terminal / wallpaper / branding / applets / themes /
extensions / settings menu / nemo from 3.1 (5/5) and 3.2 (11/11) in `## Test Results`; Host-VM
end-to-end and parity from the 2026-09-18 entry; Shadow 8/8 resolved in `## Review`; Omega 4/4
resolved in `## Security`; Big T1–T3 resolved, trio-close verdict met by re-verifications A/B/C
PASS; Vector docs complete in `## Docs`; Knuckles merge box closed by this record (PR #4
merged). Note: the boxes themselves remain unticked in `## Definition of Done` — that section is
Robotnik's and not mine to edit; verification is recorded here instead. Nothing missing; the
release proceeded.

- **Branch:** `feature/TASK-0017-cinnamon-desktop-completeness` at `9848143`, pushed to
  `metalllinux/cinnamon-for-rocky10` (`d128848..9848143`).
- **Commits:** GPG-signed no — `commit.gpgsign` is not set in the project repo (nor in
  team-chaotix); the 13 branch commits carry conventional messages and were merged as-is.
- **PR:** #4 opened (https://github.com/metalllinux/cinnamon-for-rocky10/pull/4), description
  covering the complete set, the verification summary (3.1 5/5, parity 11/11, re-verifications
  A/B/C PASS), and the recorded deviations (gnome-terminal 3.54.5 vs ref 3.60.0; the three
  branding divergences). Merged via **rebase** — the repo convention, matched against how the
  TASK-0008 fixes landed on `main` (linear commits, same messages, rebased SHAs, no merge
  commits). Within `metalllinux`, no human review required.
- **Deploy:** n/a — this repo has no CI deployment workflow (the plan chose the custom libvirt
  harness over CI/Sparky; stated in the trio close), so there is no workflow to dispatch.
- **Verification:** `main` advanced `c1de933` -> `3375a05` (13 commits, linear). Merged-tip tree
  `82219128af9c2611a8cc0f750abb253d2cb86eb7` is identical to the reviewed branch tip
  `9848143^{tree}`; `git diff 9848143 origin/main` empty. Remote feature branch retained
  (matches the retained TASK-0004/TASK-0006 branches).
- **Planning push:** team-chaotix `main` pushed from `03d20d8` (Vector docs leg) plus this
  release record commit.

---

## Archive

*Owner: `Espio`, the only agent that deletes. Superseded detail lands here rather than being
lost. Decisions, verified facts, rejected options with their reasons, known traps, and anything
the user said are never deleted.*

**Pruning log**

| Date | What was pruned or compressed | Rough size |
|---|---|---|
| 2026-09-19 | Superseded plan body (Amy, 2026-09-15): owner/why/MVP/facts/design/work-breakdown/risks/validation/rollback moved here under `### Superseded plan`; source `## Plan` replaced with 21-line pointer + key decisions | ~332 lines |
| 2026-09-19 | Orphaned duplicate continuation lines from the Next Actions tick edit (lines 439-440) deleted | 2 lines |

### Superseded plan (2026-09-15, Amy)

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
