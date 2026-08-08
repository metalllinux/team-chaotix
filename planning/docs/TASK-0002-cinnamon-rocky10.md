# TASK-0002 — Port Cinnamon Desktop to Rocky Linux 10

> **Section order below is fixed.** Each agent writes to its own section and no other. Robotnik
> reads only `## Status` and `## Next Actions`. Do not reorder, rename, or remove sections.

- **Created:** 2026-08-08

---

## Status

**Now:** Task created. Team Chaotix V1 is deployed and ready. First real task is porting Cinnamon
Desktop to Rocky Linux 10.

**Environment / scope:**
- Files in scope: `~/linux/projects/cinnamon_4_rocky10/` (project workspace)
- Touches the DB schema: no
- Graphical UI: yes (Sparky testing required)
- Rocky Linux target: yes

**Unknowns:**
- Exact Rocky Linux 10 package availability for Cinnamon dependencies
- Whether Muffin, Nemo, and other components need separate porting
- SELinux policy requirements for Cinnamon components

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

- [ ] Amy: Create detailed plan for Cinnamon porting, including dependency analysis
- [ ] Amy: Determine build approach (RPM packaging vs source build)
- [ ] Amy: Identify Sparky test requirements for Cinnamon UI components

---

## Plan

*Owner: Amy.*

To be filled by Amy during task planning phase.

---

## Implementation

*Owner: Tails.*

To be filled during implementation.

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
