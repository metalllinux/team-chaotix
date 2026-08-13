# TASK-0004 — Build mozjs115 runtime, update cjs to upstream 140.0, fix muffin circular dependency

> **Section order below is fixed.** Each agent writes to its own section and no other. Robotnik
> reads only `## Status` and `## Next Actions`. Do not reorder, rename, or remove sections.

- **Created:** 2026-08-12

---

## Status

**Now:** TASK-0003 identified 3 build issues blocking cjs, muffin, and cinnamon RPM installation. Additionally, cjs is at version 6.4.0 but upstream is at 140.0, and mozjs115 is at 115.15.0 but upstream is at ~115.29+. This task updates cjs to 140.0, rebuilds mozjs115 to 115.29.0 with runtime, and fixes muffin circular dependency.

**Environment / scope:**
- Files in scope: `~/Linux/projects/cinnamon-for-rocky10/`
- Touches the DB schema: no
- Graphical UI: no
- Rocky Linux target: yes

**Known constraints:**
- mozjs115 runtime RPM not in Rocky Linux 10 repos
- muffin-cogl requires muffin, muffin requires muffin-clutter which requires muffin-cogl
- cinnamon depends on cjs and muffin (transitive)
- cjs 6.4.0 is outdated; upstream is at 140.0
- mozjs115 115.15.0 is outdated; upstream is at ~115.29+

**Unknowns:**
- mozjs115 source availability and build requirements for 115.29.0
- Whether cjs 140.0 has different meson build requirements than 6.4.0
- Whether muffin spec files can be adjusted to break the circular dependency

---

## Definition of Done

- [ ] mozjs115 updated to 115.29.0 with runtime RPM built and installed in VM
- [ ] cjs updated to 140.0 and RPM rebuilt with updated mozjs115 dependency
- [ ] muffin sub-package circular dependency resolved
- [ ] cjs RPM installs successfully in VM
- [ ] muffin RPM installs successfully in VM
- [ ] cinnamon RPM installs successfully in VM
- [ ] All 10 Cinnamon RPMs install and pass verification in VM
- [ ] Shadow: no unresolved blockers or should-fix findings in `## Review`
- [ ] Omega: no unresolved findings above `low` in `## Security`
- [ ] Big: all VM test checks PASS, with no silently dropped checks
- [ ] Vector: documentation updated with final test results
- [ ] Knuckles: changes pushed to metallinux/cinnamon-for-rocky10
- [ ] Espio: planning doc pruned when complete

---

## Next Actions

- [ ] Amy: Write build plan for mozjs115 115.29.0, cjs 140.0, and muffin spec fix
- [ ] Tails: Update mozjs115 to 115.29.0, cjs to 140.0, fix muffin spec files
- [ ] Big: Re-run full VM test with all 10 RPMs
- [ ] Shadow: Review build scripts and spec changes
- [ ] Omega: Security review of new build artifacts
- [ ] Vector: Update documentation
- [ ] Knuckles: Push changes to GitHub
- [ ] Espio: Prune planning doc

---

## Plan

*Owner: Amy.*

### Strategic framing

**Why this task exists.** TASK-0003 testing revealed 3 of 10 Cinnamon base packages cannot install in the Rocky Linux 10 VM: cjs (needs `libmozjs-115.so()(64bit)`), muffin (circular sub-package dependency), and cinnamon (transitive dependency on both). Additionally, cjs is at version 6.4.0 but upstream is at 140.0, and mozjs115 is at 115.15.0 but upstream is at ~115.29+. This task resolves all three issues so all 10 RPMs install cleanly at current upstream versions.

**What it unblocks.** Every subsequent Cinnamon testing task (TASK-0005+) requires a fully installable RPM set. This is a gate.

**What blocks it.** Nothing external. All fixes are spec-file changes plus updated source. Build happens on the existing Rocky 10.2 host with CRB enabled.

**MVP.** mozjs115 runtime RPM at 115.29.0 that provides `libmozjs-115.so.0`, cjs updated to 140.0 with correct mozjs115 dependency, plus muffin spec changes that let dnf resolve all 5 muffin RPMs without cycles. Deferred: full mozjs115 EL10 port with source SRPM, signing, and repository packaging.

**What this makes harder later.** Adapting the Fedora mozjs115 spec to EL10 may require ICU version adjustments (EL10 has ICU 74, Fedora 44 has ICU 77). Any ICU-related patches are frozen into the spec and may need revisiting when EL10 updates ICU. cjs 140.0 may have different meson build requirements than 6.4.0, requiring spec adjustments.

---

### Work breakdown

#### A1 — Update mozjs115 to 115.29.0 (Tails)

Download and build mozjs115 115.29.0 from `ftp://ftp.mozilla.org/pub/firefox/releases/115.29.0/source/`. Adapt the Fedora 44 mozjs115.spec for EL10:

- Change `Release:` from `2.fc44` to `2.el10`
- Adapt `URL:` tag
- Replace any Fedora-specific macros with EL10 equivalents
- Verify all `BuildRequires` are available via `dnf` on Rocky 10.2 with CRB
- **Critical:** If ICU version in the Fedora `.pc` file or spec conflicts with EL10's ICU version, patch the `.pc` file in `%install` to use the EL10 ICU version
- The spec must produce a main package (`mozjs115`) that provides `libmozjs-115.so.0` and a `-devel` sub-package that provides headers and `mozjs-115.pc`

**Acceptance criterion:** `rpmbuild -ba spec/mozjs115.spec` completes without errors and produces `mozjs115-115.29.0-2.el10.x86_64.rpm` (runtime) and `mozjs115-devel-115.29.0-2.el10.x86_64.rpm`.

#### A2 — Update cjs to 140.0 (Tails)

Download cjs 140.0 from upstream and rebuild the RPM spec:

- Fetch cjs 140.0 source from `https://github.com/linuxmint/cjs/releases/tag/140.0` or `https://github.com/linuxmint/cjs/archive/refs/tags/140.0.tar.gz`
- Update `spec/cjs.spec` to use source 140.0 instead of 6.4.0
- Adjust `mozjs115` dependency in meson.build or spec file (cjs 140.0 may require different mozjs115 API)
- Verify meson build works with mozjs115 115.29.0
- Update version in spec to `140.0`

**Acceptance criterion:** `rpmbuild -ba spec/cjs.spec` completes and produces `cjs-140.0-1.el10.x86_64.rpm` that depends on `mozjs115 >= 115.29.0`.

#### A3 — Build mozjs115 and cjs RPMs (Tails)

Build both RPMs on the host system with `-j2` to avoid OOM:

```
rpmbuild -ba spec/mozjs115.spec
rpmbuild -ba spec/cjs.spec
```

Copy resulting RPMs to `rpms/`. Replace existing `mozjs115-devel-115.15.0-2.el10.x86_64.rpm` and `cjs-6.4.0-1.el10.x86_64.rpm` with the newly built versions.

**Acceptance criterion:** `rpms/` contains `mozjs115-115.29.0-*.rpm`, `mozjs115-devel-115.29.0-*.rpm`, `cjs-140.0-*.rpm`. Runtime RPM provides `libmozjs-115.so()(64bit)`.

#### A4 — Fix muffin circular dependency (Tails)

Modify `spec/muffin.spec` to break the circular dependency chain:

**Current chain (from TASK-0003 Big test results):**

```
muffin -> muffin-clutter (libmuffin-clutter-0.so.0) -> muffin-devel -> muffin
muffin -> muffin-cogl (libmuffin-cogl-0.so.0) -> muffin
```

**Fix:** Remove explicit `Requires:` directives from the bundled library sub-packages that reference the main `muffin` package or `muffin-devel`. These sub-packages are standalone libraries -- they do not need the main muffin package to function.

Specific changes to `spec/muffin.spec`:

1. **Line 79** (`%package -n muffin-clutter`): Remove `Requires: %{name}-devel = %{version}-%{release}`. The Clutter library sub-package does not need muffin-devel. If it needs muffin-cogl, keep `Requires: muffin-cogl = %{version}-%{release}` (no cycle).

2. **Line 93** (`%package -n muffin-cogl`): Remove `Requires: %{name} = %{version}-%{release}`. The Cogl library sub-package does not need the main muffin package.

3. Verify that muffin's **main** `%files` section will auto-generate correct runtime dependencies via RPM's automatic SONAME detection. The muffin binary links against `libmuffin-clutter-0.so.0` and `libmuffin-cogl-0.so.0`, which are owned by `muffin-clutter` and `muffin-cogl` respectively. RPM auto-generates `Requires:` from these SONAMEs, creating the correct dependency direction: `muffin -> muffin-clutter` and `muffin -> muffin-cogl`.

4. Keep `muffin-devel -> muffin` (line 72), `muffin-clutter-devel -> muffin-clutter` (line 86), and `muffin-cogl-devel -> muffin-cogl` (line 100) -- these are correct parent->child dependencies.

**Resulting dependency graph (acyclic):**

```
muffin -> muffin-clutter (auto SONAME)
muffin -> muffin-cogl (auto SONAME)
muffin-devel -> muffin
muffin-clutter-devel -> muffin-clutter
muffin-cogl-devel -> muffin-cogl
```

**Acceptance criterion:** `rpmbuild -ba spec/muffin.spec` succeeds. The 5 muffin RPMs can be installed together via `dnf install muffin-*.rpm` with no circular dependency error.

#### A5 — Rebuild muffin RPMs with fixed spec (Tails)

```
rpmbuild -ba spec/muffin.spec
```

Copy resulting RPMs to `rpms/`, replacing existing muffin-*.rpm files.

**Acceptance criterion:** `rpms/` contains 5 new muffin RPMs (`muffin-`, `muffin-devel-`, `muffin-clutter-`, `muffin-cogl-`, plus debuginfo/debugsource) built from the fixed spec.

#### A2 — Create mozjs115.spec for EL10 (Tails)

Adapt the Fedora 44 mozjs115.spec for Rocky Linux 10:

- Change `Release:` from `2.fc44` to `2.el10`
- Adapt `URL:` tag
- Replace any Fedora-specific macros (e.g., `%bcond_with`, `%fedora`, `%el`) with EL10 equivalents
- Verify all `BuildRequires` are available via `dnf` on Rocky 10.2 with CRB:
  - `nspr-devel`, `nss-devel`, `icu-devel`, `python3`, `yasm`, `rust`, `perl`, `gcc-c++`, `mozjs115` needs the Mozilla build infrastructure
- **Critical:** If ICU version in the Fedora `.pc` file or spec conflicts with EL10's ICU version, patch the `.pc` file in `%install` to use the EL10 ICU version. The TASK-0002 notes document ICU 77 vs 74 as the blocker that forced the manual header extraction approach.
- The spec must produce a main package (`mozjs115`) that provides `libmozjs-115.so.0` and a `-devel` sub-package that provides headers and `mozjs-115.pc`.
- Write spec to `spec/mozjs115.spec`.

**Acceptance criterion:** `rpmbuild -ba spec/mozjs115.spec` completes without errors and produces at minimum `mozjs115-115.29.0-2.el10.x86_64.rpm` and `mozjs115-devel-115.29.0-2.el10.x86_64.rpm`.

#### A3 — Build mozjs115 RPMs (Tails)

Build the mozjs115 RPMs on the host system:

```
rpmbuild -ba spec/mozjs115.spec
```

Copy resulting RPMs to `rpms/`. Replace the existing `mozjs115-devel-115.29.0-2.el10.x86_64.rpm` with the newly built version if it supersedes it.

**Acceptance criterion:** `rpms/` contains `mozjs115-*.rpm` (runtime) and an updated `mozjs115-devel-*.rpm`. Runtime RPM provides `libmozjs-115.so()(64bit)`.

#### A4 — Fix muffin circular dependency (Tails)

Modify `spec/muffin.spec` to break the circular dependency chain:

**Current chain (from TASK-0003 Big test results):**

```
muffin -> muffin-clutter (libmuffin-clutter-0.so.0) -> muffin-devel -> muffin
muffin -> muffin-cogl (libmuffin-cogl-0.so.0) -> muffin
```

**Fix:** Remove explicit `Requires:` directives from the bundled library sub-packages that reference the main `muffin` package or `muffin-devel`. These sub-packages are standalone libraries -- they do not need the main muffin package to function.

Specific changes to `spec/muffin.spec`:

1. **Line 79** (`%package -n muffin-clutter`): Remove `Requires: %{name}-devel = %{version}-%{release}`. The Clutter library sub-package does not need muffin-devel. If it needs muffin-cogl, keep `Requires: muffin-cogl = %{version}-%{release}` (no cycle).

2. **Line 93** (`%package -n muffin-cogl`): Remove `Requires: %{name} = %{version}-%{release}`. The Cogl library sub-package does not need the main muffin package.

3. Verify that muffin's **main** `%files` section will auto-generate correct runtime dependencies via RPM's automatic SONAME detection. The muffin binary links against `libmuffin-clutter-0.so.0` and `libmuffin-cogl-0.so.0`, which are owned by `muffin-clutter` and `muffin-cogl` respectively. RPM auto-generates `Requires:` from these SONAMEs, creating the correct dependency direction: `muffin -> muffin-clutter` and `muffin -> muffin-cogl`.

4. Keep `muffin-devel -> muffin` (line 72), `muffin-clutter-devel -> muffin-clutter` (line 86), and `muffin-cogl-devel -> muffin-cogl` (line 100) -- these are correct parent->child dependencies.

**Resulting dependency graph (acyclic):**

```
muffin -> muffin-clutter (auto SONAME)
muffin -> muffin-cogl (auto SONAME)
muffin-devel -> muffin
muffin-clutter-devel -> muffin-clutter
muffin-cogl-devel -> muffin-cogl
```

**Acceptance criterion:** `rpmbuild -ba spec/muffin.spec` succeeds. The 5 muffin RPMs can be installed together via `dnf install muffin-*.rpm` with no circular dependency error.

#### A5 — Rebuild muffin RPMs with fixed spec (Tails)

```
rpmbuild -ba spec/muffin.spec
```

Copy resulting RPMs to `rpms/`, replacing existing muffin-*.rpm files.

**Acceptance criterion:** `rpms/` contains 5 new muffin RPMs (`muffin-`, `muffin-devel-`, `muffin-clutter-`, `muffin-cogl-`, plus debuginfo/debugsource) built from the fixed spec.

---

### Dependencies and sequence

```
A1 (mozjs115 spec) -> A3 (build mozjs115)
A2 (cjs spec) -> A3 (build cjs)
A4 (fix muffin spec) -> A5 (rebuild muffin)

A1, A2, and A4 are INDEPENDENT and can run in parallel.
A3 depends on A1 and A2 being complete.
```

The only genuine ordering is within each chain. Mozjs115 work, cjs work, and muffin work have zero dependency on each other except that cjs needs mozjs115 to be built first for the dependency check.

---

### Critical path

A1 -> A2 -> A3 (mozjs115 chain) is the critical path. mozjs115 is a Mozilla build (~150M source tarball, complex configure.js system, NSPR/NSS/ICU dependencies). Muffin is a simple meson rebuild.

---

### Estimates (three-point)

| Item | Optimistic (min) | Most likely (min) | Pessimistic (min) | T = (O+4M+P)/6 |
|---|---|---|---|---|
| A1: Update mozjs115 spec | 15 | 30 | 90 | 37.5 |
| A2: Update cjs spec | 15 | 30 | 60 | 30 |
| A3: Build mozjs115 + cjs RPMs | 30 | 90 | 180 | 90 |
| A4: Fix muffin spec | 5 | 15 | 30 | 15 |
| A5: Rebuild muffin RPMs | 5 | 15 | 30 | 15 |

**Sequential total (critical path):** A1(38) + A3(90) = 128 min (A2 runs in parallel with A1)
**Parallel total:** max(128, 15+15) = 128 min
**Buffer (20% for ICU adaptation risk):** 26 min
**Estimated total: ~154 minutes (~2.5 hours)**

---

### Risks

| Risk | Likelihood | Impact | Mitigation | Contingency |
|---|---|---|---|---|
| mozjs115 build fails due to ICU version mismatch (EL10 ICU 74 vs Fedora 44 ICU 77) | High | Build blocked | Patch `.pc` file and any ICU version checks in spec during `%install` phase | Fall back to Fedora 41 spec which may use ICU 74, or manually adjust ICU_VERSION in spec |
| mozjs115 build fails due to missing BuildRequires in EL10 repos | Medium | Build blocked | Verify each BuildRequires with `dnf repoquery` before build | Skip problematic BR or patch source to remove dependency |
| mozjs115 build takes too long (3+ hours on 2-core) | Low | Schedule impact | Use `-j2` to match build environment from other packages | Accept longer build time; this is a one-time operation |
| cjs 140.0 has different meson build requirements than 6.4.0 | Medium | Build blocked | Compare meson.build between 6.4.0 and 140.0 before spec update | Adapt spec to handle new build options or fall back to 6.4.0 if 140.0 is incompatible |
| cjs 140.0 requires mozjs115 >= 115.29.0 but older version available | Medium | Runtime failure | Ensure mozjs115 115.29.0 is built and available before cjs build | Adjust cjs spec to require mozjs115 >= 115.29.0 explicitly |
| Removing muffin sub-package Requires breaks runtime functionality | Low | Runtime crash | The bundled libraries are self-contained; they only need each other, not muffin binary | Restore the Requires and instead use `--nodeps` for install, or restructure sub-packages differently |
| RPM auto-generated SONAME deps create unexpected requirements | Low | Install failure | Verify with `rpm -qp --requires` after build | Add explicit `Obsoletes:` or `Provides:` to control auto-generated deps |

---

### Validation

**Build-time checks (Tails):**

1. `rpm -qp --provides rpms/mozjs115-*.rpm | grep 'libmozjs-115.so'` -- confirms runtime library is provided
2. `rpm -qp --requires rpms/mozjs115-devel-*.rpm | grep mozjs115` -- confirms devel depends on runtime
3. `rpm -qp --requires rpms/cjs-140.0-*.rpm | grep mozjs115` -- confirms cjs depends on mozjs115 >= 115.29.0
4. `rpm -qp --requires rpms/muffin-6.7.4-1.el10.x86_64.rpm | grep muffin` -- confirms muffin main depends on sub-packages (auto SONAME)
5. `rpm -qp --requires rpms/muffin-cogl-6.7.4-1.el10.x86_64.rpm | grep muffin` -- confirms no circular dep (should show zero muffin main deps)
6. `rpm -qp --requires rpms/muffin-clutter-6.7.4-1.el10.x86_64.rpm | grep -E 'muffin(-devel)? '` -- confirms no circular dep

**VM install checks (Big, next task):**

1. `dnf install -y rpms/*.rpm` succeeds without `--nodeps` or fallback ordered install
2. `rpm -V mozjs115 cjs muffin cinnamon` returns clean (no file verification failures)
3. `ldd /usr/bin/cjs | grep mozjs` shows `libmozjs-115.so` resolved
4. `ldd /usr/bin/muffin | grep -E 'muffin|clutter|cogl'` shows all libraries resolved
5. All 10 base packages report installed via `rpm -q`
6. `cjs --version` outputs 140.0
7. `mozjs115 --version` outputs 115.29.0

---

### Rollback

**Detection:** Any `rpmbuild` failure is immediately visible in build output. RPM install failures in VM are caught by dnf's dependency resolver before any package is installed.

**Revert procedure:**

- **mozjs115:** If the new spec produces broken RPMs, delete `spec/mozjs115.spec` and any new `rpms/mozjs115-*.rpm`. The existing `mozjs115-devel-115.29.0-2.el10.x86_64.rpm` remains available as fallback. No system state is modified by a failed build.
- **cjs:** If cjs 140.0 fails to build or install, restore `spec/cjs.spec` from git (`git checkout -- spec/cjs.spec`). Rebuild with original spec (cjs 6.4.0). The existing `cjs-6.4.0-1.el10.x86_64.rpm` remains available as fallback.
- **muffin:** If the fixed spec breaks functionality, restore `spec/muffin.spec` from git (`git checkout -- spec/muffin.spec`). Rebuild with original spec.
- **Point of no return:** None. All changes are spec-file edits. No system packages are installed or modified until VM testing validates them.
- **Leftover state after failed build:** `~/rpmbuild/` may contain partial build artifacts. Clean with `rm -rf ~/rpmbuild/BUILD/mozjs115-* ~/rpmbuild/BUILD/cjs-*`. No retry conflicts -- rpmbuild is idempotent on a clean BUILD directory.

---

## Implementation

*Owner: Tails.*

Pending.

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

*Owner: Espio, the only agent that deletes.*

No archive yet.
