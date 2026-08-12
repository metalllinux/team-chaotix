# TASK-0003 — VM Testing: Cinnamon RPMs on Rocky Linux 10.2

> **Section order below is fixed.** Each agent writes to its own section and no other. Robotnik
> reads only `## Status` and `## Next Actions`. Do not reorder, rename, or remove sections.

- **Created:** 2026-08-12

---

## Status

**Now:** All 10 Cinnamon RPMs built and ready for VM testing. Need to verify RPM installation and runtime in a clean Rocky Linux 10.2 libvirt VM.

**Environment / scope:**
- Files in scope: `~/Linux/projects/cinnamon-for-rocky10/rpms/`, `~/ISOs/Rocky-10.2-x86_64-dvd1.iso`
- Touches the DB schema: no
- Graphical UI: yes (libvirt VM with X11 display)
- Rocky Linux target: yes
- VM testing via libvirt/QEMU on host system

**Known constraints:**
- Host: Rocky Linux 10.2, libvirt running, QEMU/KVM available
- ISO at `~/ISOs/Rocky-10.2-x86_64-dvd1.iso`
- 10 RPM packages to test in dependency order
- No GitHub auth available currently (gh auth login needed)

**Unknowns:**
- Whether VM needs graphical display or can run headless with script verification
- How to verify cinnamon desktop functionality without direct X11 display access in VM

---

## Definition of Done

- [ ] VM setup script created that provisions a Rocky Linux 10.2 VM from ISO
- [ ] All 10 RPMs install in a clean VM without dependency errors
- [ ] The cinnamon binary runs without missing dependency errors (ldd check)
- [ ] Core components verified: cinnamon-settings, nemo, cinnamon-control-center
- [ ] Dependency order validated and documented
- [ ] Shadow: no unresolved blockers or should-fix findings in `## Review`
- [ ] Omega: no unresolved findings above `low` in `## Security`
- [ ] Big: all VM test checks PASS, with no silently dropped checks
- [ ] Vector: README.md and INSTALL.md updated with test results
- [ ] Knuckles: changes pushed to metalllinux/cinnamon-for-rocky10
- [ ] Espio: planning doc pruned when complete

---

## Next Actions

- [ ] Sonic: Check cinnamon-for-rocky10 GitHub Issues/PRs (blocked on auth)
- [ ] Amy: Create VM testing plan with work breakdown
- [ ] Tails: Write VM setup script and test harness
- [ ] Big: Execute VM tests (after Tails provides harness)
- [ ] Shadow: Review VM setup scripts and test harness
- [ ] Omega: Security review of spec files and patches
- [ ] Vector: Update documentation with test results
- [ ] Knuckles: Push changes to GitHub
- [ ] Espio: Prune planning doc

---

## Plan

*Owner: Amy.*

Pending.

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

*Owner: Espio.*

**Pruning log**

| Date | What was pruned or compressed | Rough size |
|---|---|---|
| | | |
