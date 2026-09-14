# TASK-0023 — Install ripgrep (rg) on the agent host

> **Section order below is fixed.** Each agent writes to its own section and no other. `Robotnik`
> reads only `## Status` and `## Next Actions`. Do not reorder, rename, or remove sections.

- **Created:** 2026-09-14

---

## Status

*Owner: `Robotnik`. Keep this SHORT and CURRENT — it is one of only two sections the PM reads, so a
stale entry means the whole loop runs on bad information.*

**Now (2026-09-14 07:55 JST, Robotnik):** user request (mid-TASK-0010): install `rg` on whatever
machine runs the opencode sessions. Verified 2026-09-14 07:45 JST (Robotnik, read-only): `rg`
absent on the host (`command -v rg` empty); `virsh list --all` shows **zero** libvirt VMs, so the
installable scope is the host only; `ripgrep-14.1.1-1.el10_0` is available from EPEL (1.5 MB,
license string recorded in `## Implementation` after install). Landmine: the local
`cinnamon-rocky10` repo is broken (points at
`/home/howard/cinnamon_test/cinnamon-for-rocky10/rpms/repodata/repomd.xml`, which does not exist)
and fails every plain `dnf` command; the workaround is `--disablerepo=cinnamon-rocky10`.
**Decision (Robotnik, recorded):** this is a host package install with no metalllinux repo code
change, so the Shadow/Omega/Big review chain and Vector/Knuckles release steps are out of scope
for this task; the DoD below is the complete acceptance set. Tails dispatched for the install.

**Environment / scope:**
- Files in scope: none in the repo (host package install only); this doc records the evidence
- Touches the DB schema: no
- Graphical UI: no
- Rocky Linux target: yes (the host itself, Rocky 10.2)

**Unknowns:** none load-bearing. The broken `cinnamon-rocky10` repo file is not in scope to fix
here; it is recorded so future agents use the workaround.

---

## Definition of Done

*Owner: `Robotnik`, and nobody else. Written **before** any work starts. Objectively checkable —
if a box cannot be verified by looking at something, rewrite it.*

- [ ] `ripgrep` installed on the host via `dnf` (package name + version recorded in
      `## Implementation`)
- [ ] `rg --version` succeeds on the host; the output is recorded in `## Implementation`
- [ ] The broken `cinnamon-rocky10` repo landmine and the `--disablerepo=cinnamon-rocky10`
      workaround are recorded in `## Implementation` with the exact error output that exposes it
- [ ] VM scope settled: no libvirt VM exists (`virsh list --all` output recorded in
      `## Implementation`); the same install command is recorded for any future VM
- [ ] The package license string is recorded in `## Implementation` (Omega's license box, applied
      inline per the Status decision)
- [ ] This planning doc is committed to the repo

---

## Next Actions

*Owner: whoever wrote last. The future only — delete what has been done. The second of the two sections
the PM reads.*

- [ ] `Tails`: install ripgrep on the host with the recorded workaround, verify, and record all
      DoD evidence in `## Implementation` (package version, `rg --version`, license string,
      `virsh list --all`, the dnf error from the broken repo). Fresh small-context session; this
      is a three-command job, keep it under one turn if possible.
- [ ] `Robotnik`: check the DoD boxes against `## Implementation`, commit this doc, mark Done.

---

## Plan

*Owner: `Amy`.*

Not used for this task per the Status decision: a host package install needs no plan, no staged
fixes, no rollback beyond `dnf remove ripgrep`.

---

## Implementation

*Owner: `Tails`.*

---

## Review

*Owner: `Shadow`. Read-only — findings only, no edits. Severity order, blockers first.*

Not run for this task per the Status decision (no repo code change to review).

---

## Security

*Owner: `Omega`. Read-only. Severity order.*

License check applied inline by `Robotnik` per the Status decision: the EPEL `ripgrep` license
string (recorded in `## Implementation`) is all permissive or permissive-OR, no GPL, no
incompatibility with the team's MIT-licensed repos. No other attack surface: a package install
from the configured EPEL repo, no secrets, no workflow change.

---

## Test Results

*Owner: `Big`. Verdicts, never raw log dumps.*

Not run for this task per the Status decision; verification evidence lives in
`## Implementation` per the DoD.

---

## Docs

*Owner: `Vector`.*

Not applicable: no README or user-facing doc describes host packages. If the team README gains a
"host prerequisites" section later, `ripgrep` belongs in it.

---

## Release

*Owner: `Knuckles`.*

Not applicable per the Status decision: no PR, no deploy. The planning doc commit closes the task.

---

## Archive

*Owner: `Espio`, the only agent that deletes. Superseded detail lands here rather than being
lost. Decisions, verified facts, rejected options with their reasons, known traps, and anything the
user said are never deleted.*

**Pruning log**

| Date | What was pruned or compressed | Rough size |
|---|---|---|
| | | |
