# TASK-0005 — Validate INSTALL.md on fresh VM

> **Section order below is fixed.** Each agent writes to its own section and no other. Robotnik
> reads only `## Status` and `## Next Actions`. Do not reorder, rename, or remove sections.

- **Created:** 2026-08-13

---

## Status

**Now:** All 10 Cinnamon RPMs build and install in TASK-0004 test VM. Need to validate the documented installation process in INSTALL.md on a fresh Rocky Linux 10.2 VM with no pre-installed dependencies.

**Environment / scope:**
- Files in scope: `~/Linux/projects/cinnamon-for-rocky10/INSTALL.md`, `~/Linux/projects/cinnamon-for-rocky10/rpms/`
- Touches the DB schema: no
- Graphical UI: no
- Rocky Linux target: yes

**Known constraints:**
- VM test harness exists at `~/Linux/projects/cinnamon-for-rocky10/vm-test/`
- INSTALL.md documents prerequisites, quick install, and step-by-step install
- Need to verify both installation methods work on a fresh VM

**Unknowns:**
- Whether the prerequisite list in INSTALL.md is complete
- Whether the step-by-step installation order matches actual dependency requirements

---

## Definition of Done

- [ ] Fresh Rocky Linux 10.2 VM provisioned with no pre-installed dependencies
- [ ] Prerequisites from INSTALL.md install successfully
- [ ] Quick install method (`sudo dnf install ./rpms/*.rpm`) works
- [ ] Step-by-step install method works in documented order
- [ ] All 10 base packages verify as installed
- [ ] Binary verification passes (ldd + --version checks)
- [ ] GDM session configuration instructions verified
- [ ] Shadow: no unresolved blockers or should-fix findings in `## Review`
- [ ] Omega: no unresolved findings above `low` in `## Security`
- [ ] Vector: INSTALL.md updated if any corrections needed
- [ ] Knuckles: changes pushed to metalllinux/cinnamon-for-rocky10
- [ ] Espio: planning doc pruned when complete

---

## Next Actions

- [ ] Amy: Write validation plan for INSTALL.md testing
- [ ] Tails: Adapt test harness to validate INSTALL.md steps
- [ ] Big: Execute INSTALL.md validation test
- [ ] Shadow: Review test results and INSTALL.md
- [ ] Omega: Security review of installation process
- [ ] Vector: Update INSTALL.md if corrections needed
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

*Owner: Espio, the only agent that deletes.*

No archive yet.
