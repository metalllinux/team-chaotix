# TASK-0029 — VM scripts repair (align scripts/ with AGENTS.md section 12)

> **Section order below is fixed.** Each agent writes to its own section and no other. `Robotnik`
> reads only `## Status` and `## Next Actions`. Do not reorder, rename, or remove sections.

- **Created:** 2026-10-02

---

## Status

*Owner: `Robotnik`. Keep this SHORT and CURRENT — it is one of only two sections the PM reads, so a
stale entry means the whole loop runs on bad information.*

**Now:** Intake complete (2026-10-02). Follow-up task created from the TASK-0028 review chain: the
VM scripts in `scripts/` diverge from AGENTS.md section 12 and carry security defects; the shipped
skill documents them as known defects, this task fixes them. Awaiting plan.

**Findings source:** `planning/docs/TASK-0028-vm-deploy-skill.md`, the `## Review`, `## Security`,
and `## Test Results` sections plus the 2026-10-02 PM Status entries; the shipped Known Script
Defects list in `~/.config/opencode/skills/vm-deploy/SKILL.md`.

**Environment / scope:**
- Files in scope: `scripts/vm-create-rocky.sh`, `scripts/vm-create-fedora-cinnamon.sh`,
  `scripts/vm-destroy` (repo). Host-state items: the stub files in `/var/lib/libvirt/images` (see DoD).
- Touches the DB schema: no
- Graphical UI: no
- Rocky Linux target: yes (scripts run on this host; a transient test VM may be created and
  destroyed within one run)

**Unknowns:** the create scripts are only verified up to roughly line 40-50 so far; the plan must
read both in full first. The `cinnamon-1` domain is undefined in libvirt (an orphaned QEMU holds
its disk; recovery is tracked in the TASK-0026 doc), so a test VM must not collide with its VNC
port, disk, or network state.

---

## Definition of Done

*Owner: `Robotnik`, and nobody else. Written **before** any work starts. Objectively checkable —
if a box cannot be verified by looking at something, rewrite it.*

- [ ] `scripts/vm-create-rocky.sh`: disk existence check exits with a clear error only when the disk
  exists (today it is inverted, exiting "disk already exists" when the disk is absent); the disk is a
  qcow2 thin overlay of `/var/lib/libvirt/images/rocky-10-golden.qcow2` created in
  `/var/lib/libvirt/images` (not a blank disk, not `/dev/shm`), per AGENTS.md section 12.
- [ ] Generated XML of both create scripts: disk `<driver type='qcow2'>` element present, VNC listen
  `127.0.0.1` (no `0.0.0.0` anywhere), serial console, default NAT network, 4 vCPU / 8 GB defaults
  preserved.
- [ ] Both create scripts: NAME validated against a safe charset (no XML or path injection), no temp
  XML file left on disk (trap cleanup), no hardcoded public key (read `~/.ssh/team-vm.pub`), guest
  setup commands target Rocky (dnf, not apt).
- [ ] `scripts/vm-create-fedora-cinnamon.sh`: prefers a local ISO when one exists and rejects any ISO
  smaller than 1 GB before use (catches the 1.8KB stubs); the 40G disk in
  `/var/lib/libvirt/images` is preserved.
- [ ] `scripts/vm-destroy`: execute bit set (755); destroys, undefines, removes the disk, and removes
  the portless alias per AGENTS.md section 12.
- [ ] `scripts/vm-create-rocky.sh`: every `virsh` invocation pinned to `qemu:///system` (lines 51, 52,
  and 55 are bare `virsh` and land on `qemu:///session` — verified live 2026-10-02, see the TASK-0031
  skill update), so the script's existence check, `define`, `start`, and `domifaddr` all see the
  same instance.
- [ ] One transient test VM created and destroyed within a single run (capacity rule: at most three
  concurrent work VMs); afterwards no domain, no disk, no portless alias, no temp file remain.
- [ ] Host cleanup, blast radius recorded before execution: the stub/junk files in
  `/var/lib/libvirt/images` (the 19B/1.8KB/7KB `Fedora-*-Cinnamon-DVD.iso` files and the 856B
  `cinnamon-1-vm.xml`) are removed after verifying nothing references them.
- [ ] `Shadow`: no unresolved blockers or should-fix findings in `## Review`
- [ ] `Omega`: no unresolved findings above `low` in `## Security`
- [ ] `Big`: all harness checks PASS, with no silently dropped checks (including the transient
  test-VM run)
- [ ] `Charmy`: no unresolved findings in `## License (Charmy)`
- [ ] `Vector`: AGENTS.md section 12 cross-checked against the repaired scripts (flag residual
  divergence; AGENTS.md itself is not edited)
- [ ] `Knuckles`: script changes committed

---

## Next Actions

*Owner: whoever wrote last. The future only — delete what has been done. The second of the two sections
the PM reads.*

- [ ] `Amy`: write `## Plan`. Read both create scripts and `scripts/vm-destroy` in full, the TASK-0028
  doc sections named in Status, and the Known Script Defects section of the shipped skill.
- [ ] `Tails`: implement per `## Plan`.
- [ ] `Shadow` → `Omega` → `Big` → `Charmy`: review chain.
- [ ] `Vector`: AGENTS.md section 12 cross-check.
- [ ] `Knuckles`: commit the script changes.
- [ ] `Espio`: prune this doc.

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

*Owner: `Tails`.*

**Alternatives considered**

### Problem: <what needed solving>
**Option A — <approach>** · How: · Pros: · Cons:
**Option B — <approach>** · How: · Pros: · Cons:
**Chosen:** , because .
**Competing priorities:** what was traded away, explicitly.

**Changes**

| File | What changed |
|---|---|
| | |

**Checks run:** compile · linter · harness

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

## License (Charmy)

*Owner: `Charmy`. Fourth in the review chain. Every license is verified at the upstream source
repository and the ref used, never from a copy in this repo.*

**Project license:** <license> — appropriate | finding

**Imported code**

| Component | Source (repo @ ref) | License (verified at) | Obligations met | Status |
|---|---|---|---|---|
| | | | yes/no + what | pass/finding |

**Verdict:** pass | findings *(Tails fixes; the chain re-runs until clean)*

---

## Test Results

*Owner: `Big`. Verdicts, never raw log dumps.*

**Workflow run:**

| Check | What it exercises | Result | Notes |
|---|---|---|---|
| scripts parse (bash -n) | changed files | PASS/FAIL | |
| rocky script fresh run | create-then-destroy of a test VM | PASS/FAIL | |
| fedora script dry checks | XML/ISO/disk behavior without a full install | PASS/FAIL | |
| vm-destroy run | cleanup of the test VM | PASS/FAIL | |
| host-state sweep | no leftover domain/disk/alias/temp file | PASS/FAIL | |

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
lost. Decisions, verified facts, rejected options with their reasons, known traps, and anything the
user said are never deleted.*

**Pruning log**

| Date | What was pruned or compressed | Rough size |
|---|---|---|
| | | |
