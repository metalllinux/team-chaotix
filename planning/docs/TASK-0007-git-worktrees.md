# TASK-0007 — Git Worktrees Support for Team Chaotix

> **Section order below is fixed.** Each agent writes to its own section and no other. Robotnik
> reads only `## Status` and `## Next Actions`. Do not reorder, rename, or remove sections.

- **Created:** 2026-08-14

---

## Status

**Now:** Need to add git worktrees support to Team Chaotix to enable parallel opencode sessions working on different projects simultaneously without file conflicts.

**Environment / scope:**
- Files in scope: `~/AI/projects/team-chaotix/` (main repo), worktrees for each project
- Touches the DB schema: no
- Graphical UI: no
- Rocky Linux target: yes

**Known constraints:**
- opencode resolves project config from its cwd
- Launching opencode inside a project directory loads zero custom agents and no AGENTS.md
- Need each worktree to have its own .opencode configuration
- Need agents to understand worktree boundaries

**Unknowns:**
- Whether opencode can be configured to load agents from parent repo when launched in worktree
- How to handle .gitignore and other shared files across worktrees

---

## Definition of Done

- [ ] Git worktree infrastructure documented and tested
- [ ] README.md updated with worktree setup instructions
- [ ] AGENTS.md updated with worktree conventions
- [ ] .opencode/ configuration works from worktrees
- [ ] Agent toolkits understand worktree boundaries
- [ ] Shadow: no unresolved blockers or should-fix findings in `## Review`
- [ ] Omega: no unresolved findings above `low` in `## Security`
- [ ] Vector: documentation updated
- [ ] Knuckles: changes pushed to metalllinux/team-chaotix
- [ ] Espio: planning doc pruned when complete

---

## Next Actions

- [ ] Amy: Write worktree implementation plan
- [ ] Tails: Implement worktree configuration and update docs
- [ ] Shadow: Review worktree setup
- [ ] Omega: Security review
- [ ] Vector: Finalize documentation
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
