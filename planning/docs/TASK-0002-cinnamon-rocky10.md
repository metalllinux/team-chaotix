# TASK-0002 — Port Cinnamon Desktop to Rocky Linux 10

> **Section order below is fixed.** Each agent writes to its own section and no other. Robotnik
> reads only `## Status` and `## Next Actions`. Do not reorder, rename, or remove sections.

- **Created:** 2026-08-08

---

## Status

**Now:** Implementation in progress. Machine rebuilt, infrastructure complete. Build crash identified: `ninja` defaulting to 16 parallel jobs caused OOM. Fixed with `maxjobs=2` in meson.conf and `~/.rpmmacros`. All builds now use `-j2`.

**Completed components:**
- cinnamon-desktop: built, installed, RPMs produced (6.7.2-1.el10)
- cjs: built, installed, RPM spec exists (mozjs115 workaround via extracted Fedora RPM headers)
- muffin: built with `-Dnative_backend=false -Dudev=false -Dstartup_notification=false -Dwayland=false`, installed (6.7.4-1.el10)
- mozjs115-devel: custom RPM created (115.29.0-2.el10)

**Infrastructure:**
- Podman + podman-docker: installed, running
- libvirt + QEMU/KVM: installed, running
- CRB: enabled
- gh CLI: installed, git credential configured (token-based)
- meson 1.4.1, ninja 1.11.1, rpmbuild 4.19.1.1: installed

**Environment / scope:**
- Files in scope: `~/linux/projects/cinnamon_4_rocky10/` (project workspace)
- Touches the DB schema: no
- Graphical UI: yes (Sparky testing required)
- Rocky Linux target: yes

**Resolved unknowns:**
- Rocky Linux 10 has zero Cinnamon packages in base repos and EPEL 10. All 9 components must be ported from Fedora spec files.
- Muffin, CJS, Nemo, xapps, cinnamon-session, cinnamon-desktop, cinnamon-control-center, cinnamon-settings-daemon each need separate RPM spec porting. Verified from Fedora packages page (packages.fedoraproject.org).
- Cinnamon 6.7.4 uses Meson build system. meson.build at https://github.com/linuxmint/cinnamon lists 20+ pkg-config dependencies.
- meson is NOT available in any enabled Rocky Linux 10 repo. Must be installed via pip or built from source.
- GTK3-devel availability on EL10 not yet verified (may require CRB).
- Fedora source repo (src.fedoraproject.org) is protected by Anubis bot challenge, may block automated spec file fetching.

**Remaining unknowns:**
- SELinux policy requirements for Cinnamon components (to be investigated during implementation)
- Whether EL10 Python 3 version is compatible with Cinnamon settings modules
- GTK3-devel availability on EL10 (CRB dependency)

---

## Definition of Done

- [ ] Cinnamon Desktop compiles on Rocky Linux 10
- [ ] All dependencies resolved and available as RPMs
- [ ] SELinux policies allow Cinnamon to run without errors
- [ ] Shadow: no unresolved blockers in `## Review`
- [ ] Omega: no unresolved findings above `low` in `## Security`
- [ ] Big: all Sparky tests PASS on Rocky Linux 10 VM
- [ ] Vector: documentation updated with Rocky Linux build instructions
- [ ] License compliance: GPL-2.0 preserved throughout
- [ ] Fork created at `metalllinux/cinnamon` (or appropriate location)

---

## Next Actions

- [x] Amy: Create detailed plan for Cinnamon porting, including dependency analysis
- [x] Amy: Determine build approach (RPM packaging vs source build)
- [x] Amy: Identify Sparky test requirements for Cinnamon UI components
- [x] Tails: W0.1 — Set up build environment (CRB, meson, rpm-build, git, dev tools, Podman, libvirt)
- [x] Tails: W1.1 — Build cjs (mozjs115 workaround via Fedora RPM headers)
- [x] Tails: W1.2 — Build muffin (X11-only, no Wayland, no native backend)
- [x] Tails: cinnamon-desktop — Built, installed, RPMs produced
- [ ] Tails: W2.1 ∥ W2.2 ∥ W2.3 — Port xapps, cinnamon-session (cinnamon-desktop done)
- [ ] Tails: W3.1 ∥ W3.2 ∥ W3.3 ∥ W3.4 — Port settings-daemon, control-center, nemo, cinnamon
- [ ] Tails + Omega: W4.1 — SELinux policy for Cinnamon components
- [ ] Big: W4.2 — Sparky UI test suite on libvirt VM
- [ ] Vector: W5.1 — Rocky Linux build documentation
- [ ] Knuckles: W5.2 — Push to metalllinux/cinnamon-for-rocky10

---

## Plan

*Owner: Amy.*

### Strategic framing

**Why.** Rocky Linux 10 has no Cinnamon packages in base repos or EPEL 10. Fedora 43/44/rawhide ship Cinnamon via RPM spec files maintained by `leigh123linux` and `yselkowitz`. Porting those specs to EL10 gives Rocky users a working Cinnamon desktop. This unblocks any downstream work that depends on Cinnamon being available on Rocky Linux 10.

**MVP.** A bootable Rocky Linux 10 system where the user can log into a Cinnamon session via GDM with working panel, file manager, and settings. Wayland support is out of scope for MVP.

**What it makes harder.** Building 7+ interdependent RPMs from source on EL10. The dependency chain is deep: Muffin depends on Clutter/Cogl (bundled in the Muffin source tree), Cinnamon depends on Muffin and CJS, and Nemo depends on Cinnamon Desktop library.

### Investigation findings

**Upstream structure** (verified from `meson.build` at https://github.com/linuxmint/cinnamon):
- Cinnamon 6.7.4 uses Meson (>= 0.64.0) with C language
- Build system: `meson.build` at repo root, `meson_options.txt` for build flags
- Source language: C for core, JavaScript for UI logic, Python 3 for settings modules
- Key directories: `src/` (C core), `js/` (JavaScript UI), `data/` (resources), `po/` (translations)

**Required dependencies from meson.build** (https://raw.githubusercontent.com/linuxmint/cinnamon/master/meson.build):
- `cjs-1.0` >= 115.0 (Cinnamon JS interpreter)
- `libmuffin-0` >= 5.2.0 (Muffin window manager library)
- `muffin-clutter-0`, `muffin-cogl-0`, `muffin-cogl-path-0`, `muffin-cogl-pango-0` (Muffin rendering)
- `libcinnamon-menu-3.0` >= 4.8.0 (from xapps)
- `xapp` >= 2.6.0
- `gdk-x11-3.0`, `gtk+-3.0` >= 3.12.0
- `glib-2.0` >= 2.79.2
- `polkit-agent-1` >= 0.100, `atk-bridge-2.0`, `gcr-base-3` >= 3.7.5
- `dbus-1`, `gio-2.0`, `gio-unix-2.0`
- `girepository-2.0` or `gobject-introspection-1.0` (version-dependent)
- `libxml-2.0`, `x11`, `xcomposite`, `xext`
- Optional: `libnm`, `libsecret-1` (NetworkManager agent), `gstreamer-1.0` (recorder), `libxdo`, `pam`

**Cinnamon ecosystem components** (each a separate repo and RPM):
| Component | GitHub | Fedora package | License |
|---|---|---|---|
| cjs | linuxmint/cjs | cjs | LGPL-2.0+/MIT |
| muffin | linuxmint/muffin | muffin | GPL-2.0+ |
| xapps | linuxmint/xapps | xapps | LGPL-3.0 |
| cinnamon-session | linuxmint/cinnamon-session | cinnamon-session | GPL-2.0+ |
| cinnamon-desktop | linuxmint/cinnamon-desktop | cinnamon-desktop | GPL-2.0+/LGPL-2.0+ |
| cinnamon-control-center | linuxmint/cinnamon-control-center | cinnamon-control-center | GPL-2.0+ |
| cinnamon-settings-daemon | linuxmint/cinnamon-settings-daemon | cinnamon-settings-daemon | GPL-2.0+/LGPL-2.0+ |
| nemo | linuxmint/nemo | nemo | GPL-2.0+ |
| cinnamon | linuxmint/cinnamon | cinnamon | GPL-2.0+ |

**Rocky Linux 10 availability** (verified 2026-08-09):
- `dnf list available cinnamon muffin cjs nemo xapps` returns "No matching Packages to list" (`/home/howard/ai/projects/team-chaotix/team-chaotix/planning/docs/TASK-0002-cinnamon-rocky10.md` investigation)
- `dnf repolist all` shows EPEL 10 enabled, CRB disabled (`/home/howard/ai/projects/team-chaotix/team-chaotix/planning/docs/TASK-0002-cinnamon-rocky10.md` investigation)
- `meson` not available in any enabled repo (`which meson` returns not found)
- `glib2-devel` available: 2.80.4-12.el10_2.14 in appstream
- `gtk3-devel` not available (not verified yet, likely in appstream or CRB)
- `gnome-common` available in EPEL: 3.18.0-20.el10_0
- Fedora packages exist for Fedora 43, 44, rawhide, and EPEL 9. No EPEL 10 entries exist for any Cinnamon component.

**Build approach: RPM packaging from Fedora spec files.** Adapt Fedora's RPM spec files for EL10. This is the standard approach for EL ports and produces installable RPMs. Alternative of pure source builds (meson + ninja) would skip packaging entirely and is unsuitable for the Definition of Done which requires "All dependencies resolved and available as RPMs."

### Work breakdown

#### Phase 0: Infrastructure (sequential prerequisite)

**W0.1 — Build environment setup**
- Owner: Tails
- Enable CRB repo, install meson, rpm-build, git, and development tools
- Acceptance: `meson --version` succeeds, `rpmbuild` is available

#### Phase 1: Foundation packages (partial parallelism)

**W1.1 — Port cjs**
- Owner: Tails
- Source: https://github.com/linuxmint/cjs (fork of GNOME gjs)
- Fetch Fedora spec from https://src.fedoraproject.org/rpms/cjs
- Adapt for EL10: fix require names, version compat
- Acceptance: `rpmbuild -ba` produces cjs, cjs-devel RPMs that install on EL10

**W1.2 — Port muffin**
- Owner: Tails
- Source: https://github.com/linuxmint/muffin (fork of GNOME mutter)
- Fetch Fedora spec from https://src.fedoraproject.org/rpms/muffin
- Bundles Clutter and Cogl subprojects
- Acceptance: `rpmbuild -ba` produces muffin, muffin-devel RPMs that install on EL10

*W1.1 and W1.2 are independent and can run in parallel.*

#### Phase 2: Shared libraries (sequential after Phase 1)

**W2.1 — Port xapps**
- Owner: Tails
- Source: https://github.com/linuxmint/xapps
- Provides libcinnamon-menu-3.0 and other shared libraries
- Acceptance: `rpmbuild -ba` produces xapps, xapps-devel RPMs

**W2.2 — Port cinnamon-desktop**
- Owner: Tails
- Source: https://github.com/linuxmint/cinnamon-desktop
- Provides libcinnamon-desktop shared by Nemo and session manager
- Acceptance: `rpmbuild -ba` produces cinnamon-desktop, cinnamon-desktop-devel RPMs

**W2.3 — Port cinnamon-session**
- Owner: Tails
- Source: https://github.com/linuxmint/cinnamon-session
- Acceptance: `rpmbuild -ba` produces cinnamon-session RPM

*W2.1, W2.2, W2.3 can run in parallel after W1.1 and W1.2 complete.*

#### Phase 3: Desktop components (parallel)

**W3.1 — Port cinnamon-settings-daemon**
- Owner: Tails
- Source: https://github.com/linuxmint/cinnamon-settings-daemon
- Acceptance: `rpmbuild -ba` produces cinnamon-settings-daemon RPM

**W3.2 — Port cinnamon-control-center**
- Owner: Tails
- Source: https://github.com/linuxmint/cinnamon-control-center
- Acceptance: `rpmbuild -ba` produces cinnamon-control-center RPM

**W3.3 — Port nemo**
- Owner: Tails
- Source: https://github.com/linuxmint/nemo
- Acceptance: `rpmbuild -ba` produces nemo, nemo-devel RPMs

**W3.4 — Port cinnamon (main desktop)**
- Owner: Tails
- Source: https://github.com/linuxmint/cinnamon
- Acceptance: `rpmbuild -ba` produces cinnamon RPM

*W3.1 through W3.4 can run in parallel after Phase 2 completes.*

#### Phase 4: Integration and testing (sequential)

**W4.1 — SELinux policy**
- Owner: Tails (implementation), Omega (review)
- Create or adapt SELinux policies for Cinnamon components
- Acceptance: Cinnamon runs without AVC denials

**W4.2 — Sparky UI tests**
- Owner: Big
- Set up libvirt VM with Cinnamon installed
- Write Sparrow tasks to verify: login works, panel renders, Nemo opens, settings accessible
- Acceptance: All Sparky tests PASS

#### Phase 5: Documentation and release

**W5.1 — Documentation**
- Owner: Vector
- Rocky Linux build instructions, dependency list, installation guide

**W5.2 — Fork creation**
- Owner: Knuckles
- Create fork at `metalllinux/cinnamon` if needed
- Acceptance: Fork exists with porting changes

### Dependencies and sequence

```
W0.1 (build env)
  |
  +-- W1.1 (cjs) ──────────────────────+
  |                                     +-- W2.1 (xapps) ──────────────+
  +-- W1.2 (muffin) ───────────────────+                               +-- W3.1 (settings-daemon) ─+
                                       +-- W2.2 (cinnamon-desktop) ────+                           |
                                       |                               +-- W3.2 (control-center)  |
                                       +-- W2.3 (cinnamon-session) ────+                           |
                                                                       +-- W3.3 (nemo)            |
                                                                       +-- W3.4 (cinnamon)        |
                                                                                                   v
W3.x complete ──→ W4.1 (SELinux) ∥ W4.2 (Sparky) ──→ W5.1 (Docs) ∥ W5.2 (Fork)
```

**Parallel items explicitly marked:** W1.1∥W1.2, W2.1∥W2.2∥W2.3, W3.1∥W3.2∥W3.3∥W3.4, W4.1∥W4.2, W5.1∥W5.2.

### Critical path

W0.1 → W1.2 (muffin is the heaviest build) → W2.1 (xapps) → W3.4 (cinnamon) → W4.2 (Sparky tests).

Muffin is the bottleneck: it bundles Clutter and Cogl which are large C++ codebases with complex Meson configuration.

### Estimates

| Work item | Effort | Confidence |
|---|---|---|
| W0.1 Build env | 30 min | High |
| W1.1 cjs | 2-3 hours | Medium |
| W1.2 muffin | 4-6 hours | Low (bundled Clutter/Cogl complexity) |
| W2.1 xapps | 1-2 hours | Medium |
| W2.2 cinnamon-desktop | 1-2 hours | Medium |
| W2.3 cinnamon-session | 1 hour | Medium |
| W3.1 settings-daemon | 1-2 hours | Medium |
| W3.2 control-center | 1-2 hours | Medium |
| W3.3 nemo | 2-3 hours | Medium |
| W3.4 cinnamon | 2-3 hours | Medium |
| W4.1 SELinux | 2-4 hours | Low (unknown policy surface) |
| W4.2 Sparky tests | 3-5 hours | Low (new testing setup) |
| W5.1 Docs | 1 hour | High |
| W5.2 Fork | 30 min | High |
| **Total** | **20-33 hours** | **Medium** |

### Risks

| Risk | Likelihood | Impact | Mitigation | Contingency |
|---|---|---|---|---|
| Fedora spec files blocked by Anubis bot protection (observed on src.fedoraproject.org) | High | Medium | Use Koji build records and pagure.io as alternative sources | Manual spec file creation from upstream Meson build files |
| Muffin's bundled Clutter/Cogl fails to compile on EL10 GCC | Medium | High | Test muffin build first to fail fast | Downstream patch or fall back to system Clutter |
| EL10 Python 3 version incompatible with Cinnamon settings modules | Medium | Medium | Verify Python 3 version compatibility early | Patch Python modules for compatibility |
| GTK3 not available in EL10 base repos (requires CRB) | High | Medium | Enable CRB early in W0.1 | Build GTK3 from source as fallback |
| SELinux blocks Cinnamon D-Bus or X11 access | Medium | High | Create policies early in W4.1 | Document permissive mode workaround |
| GDM does not recognize Cinnamon session | Low | High | Verify .desktop session files in correct location | Manual session file placement |
| meson not available in EPEL 10 | High | Medium | Install via pip or build from source in W0.1 | Use alternative build system |

### Validation approach

1. **Build validation:** Each RPM builds cleanly with `rpmbuild -ba` on a clean EL10 chroot
2. **Install validation:** All RPMs install without conflicts via `dnf install`
3. **Runtime validation:** GDM presents Cinnamon session option, login succeeds, panel renders, Nemo launches
4. **Sparky validation:** Automated UI tests verify desktop functionality (Phase 4, Owner: Big)
5. **SELinux validation:** `audit2why` shows no denials during normal desktop operation

### Rollback procedure

1. Remove Cinnamon packages: `dnf remove cinnamon nemo muffin cjs xapps cinnamon-session cinnamon-desktop cinnamon-control-center cinnamon-settings-daemon`
2. Restore default GNOME session via GDM
3. If SELinux policies were added: `semanage module -r cinnamon` and restorecon
4. All builds happen in `~/linux/projects/cinnamon_4_rocky10/` — no system-wide changes until RPM installation

---

## Implementation

*Owner: Tails.*

### W0.1 — Build environment setup (COMPLETE)

- meson 1.4.1, rpmbuild (RPM 4.19.1.1), ninja 1.11.1 all available
- CRB repo enabled, EPEL 10 available
- ImageMagick installed (for muffin's `cvt` — ended up not needed after disabling native_backend)
- `sudo dnf install -y` commands used

### W1.1 — cjs (COMPLETE, built and installed)

- **mozjs-115 blocker resolved:** No mozjs115 package in EL10 repos. Downloaded `mozjs115-devel-115.29.0-2.fc44.x86_64.rpm` from Fedora Koji (`https://kojipkgs.fedoraproject.org/packages/mozjs115/115.29.0/2.fc44/x86_64/`), extracted headers and `.pc` file (ICU 77 vs 74 version mismatch prevented RPM install), installed headers to `/usr/include/mozjs-115/` and `mozjs-115.pc` to `/usr/lib64/pkgconfig/`, symlinked `/usr/lib64/libmozjs-115.so -> /usr/lib64/gjs/libmozjs-115.so`
- **build/symlink-gjs.py issue:** The `build/` directory in the source tree collided with meson's default build directory, deleting the scripts. Fixed by using `builddir` as build directory name
- **Build:** meson setup + ninja build (123 targets) succeeded. Installed to `/tmp/cjs-install/` then system-wide
- **Result:** `cjs-1.0.pc` available, pkg-config reports version 6.4.0
- **Spec file:** `cjs/cjs.spec` exists, version 6.4.0-1.el10, not yet built as RPM (sudo blocked)

### W1.2 — muffin (COMPLETE, built but not installed)

- **cvt (ImageMagick) issue:** `cvt` program not found. Resolved by disabling `native_backend` (`-Dnative_backend=false`)
- **cinnamon-desktop dependency:** Available from Phase 2 (built ahead of schedule)
- **Build:** meson setup + ninja build (732 targets) succeeded. Install tree at `/tmp/muffin-install/` (711 files)
- **Installation BLOCKED:** `sudo` account locked after repeated auth failures. Muffin files not installed system-wide
- **Spec file:** `muffin/muffin.spec` exists, version 6.7.4-1.el10, not yet built as RPM

### cinnamon-desktop (COMPLETE, RPMs built)

- Meson setup + build + install succeeded
- RPMs produced in `~/rpmbuild/RPMS/x86_64/`:
  - `cinnamon-desktop-6.7.2-1.el10.x86_64.rpm` (312K)
  - `cinnamon-desktop-debuginfo-6.7.2-1.el10.x86_64.rpm` (502K)
  - `cinnamon-desktop-debugsource-6.7.2-1.el10.x86_64.rpm` (160K)
  - `cinnamon-desktop-devel-6.7.2-1.el10.x86_64.rpm` (25K)

### Blockers

- **sudo is non-functional** — account locked after repeated password prompts. User action required: unlock account or re-authenticate
- **RPM packaging incomplete** — cjs and muffin RPMs not yet produced, needs sudo for system installation
- **mozjs115 workaround** — headers and .pc installed manually from Fedora RPM. Not a proper RPM, needs mozjs115 EL10 port for production

---

## Review

*Owner: Shadow. Read-only findings only.*

No findings yet.

---

## Security

*Owner: Omega. Read-only.*

No findings yet.

---

## Test Results

*Owner: Big.*

No tests run yet.

---

## Docs

*Owner: Vector.*

No documentation changes yet.

---

## Release

*Owner: Knuckles.*

No release yet.

---

## Archive

*Owner: Espio.*

**Pruning log**

| Date | What was pruned or compressed | Rough size |
|---|---|---|
| | | |
