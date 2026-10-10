# TASK-0031 — vm-deploy skill update: dual libvirt instance gotcha and boot-diagnosis caveats

> **Section order below is fixed.** Each agent writes to its own section and no other. `Robotnik`
> reads only `## Status` and `## Next Actions`. Do not reorder, rename, or remove sections.

- **Created:** 2026-10-02

---

## Status

*Owner: `Robotnik`. Keep this SHORT and CURRENT — it is one of only two sections the PM reads, so a
stale entry means the whole loop runs on bad information.*

**Now:** Complete (2026-10-02). Skill updated (instance-pinning rule plus the three gotchas),
PM-verified against live state; row Done. No commit involved (skill is outside the repo).

**Evidence source:** the dated `## Implementation` entry of
`planning/docs/TASK-0026-cinnamon-control-center-comparison.md` (2026-10-02 boot-diagnosis run).

**Environment / scope:**
- Files in scope: `~/.config/opencode/skills/vm-deploy/SKILL.md` only.
- Touches the DB schema: no
- Graphical UI: no
- Rocky Linux target: yes (live host state on this machine)

**Unknowns:** which libvirt instance `scripts/vm-create*` actually uses (unsuffixed `virsh` =
session vs `sudo virsh` = system) — the instance-pinning rule depends on it; Tails verifies against
the scripts.

**Deviation on record:** review chain skipped (documentation-only change to a file outside the
repo; same rationale as TASK-0030). PM verifies every added claim against live state or the cited
evidence.

**2026-10-02 (PM, after Tails, task closed):**
- Tails' additions verified by PM: the instance-pinning rule (skill lines 46-56) and the pinned workflow `virsh` commands are in place; the three gotchas (dual libvirt instance, silent serial console, stale console client) sit in Hard-won Gotchas with the verified evidence; pre-existing gotchas, frontmatter, and the Known Script Defects section are untouched.
- Live spot-checks (PM): `virsh uri` → `qemu:///session`; the session list shows `cinnamon-1` running (Id 4) plus `fedora-cinnamon-fallback-1` shut off; the system list shows the stale `cinnamon-1` definition plus `cinnamon-fedora-1` and `team-test-1` shut off (both recorded as host state for the TASK-0026 doc); `scripts/vm-create`, `scripts/vm-create-fedora-cinnamon.sh`, and `scripts/vm-destroy` all pin `-c qemu:///system`; `scripts/vm-create-rocky.sh:51,52,55` bare `virsh` confirmed — the outlier the skill flags.
- Consequence recorded: the bare-`virsh` outlier is added to the TASK-0029 Definition of Done (pin every `virsh` in the rocky script).
- All DoD boxes satisfied; row to Done.

---

## Definition of Done

*Owner: `Robotnik`, and nobody else. Written **before** any work starts. Objectively checkable —
if a box cannot be verified by looking at something, rewrite it.*

- [ ] The skill documents the dual libvirt instance gotcha with a deployer rule: the procedure pins
  one libvirt instance — the one `scripts/vm-create*` actually uses (verified against the scripts) —
  and the gotcha entry records the verified evidence (the running domain lives on
  `qemu:///session` with state under `~/.config/libvirt/qemu/lib/`; the `qemu:///system` copy is
  stale and shows a different XML, here `type='raw'`; never define on one instance and operate
  from the other).
- [ ] The skill records the silent-serial-console caveat: the guest serial console can be fully
  silent during a firmware-stage boot stall (no GRUB/kernel text); diagnosis must combine
  framebuffer state (`virsh screenshot` md5 plus PIL color count) and QEMU process state
  (CPU time, cmdline).
- [ ] The skill records the stale console client caveat: a stale `virsh console` client can hold
  the console for hours and block fresh attaches; check for and kill stale console processes
  before capturing.
- [ ] Every added claim is verified against live state or the cited evidence (no invented paths or
  commands); nothing else in the skill changes (frontmatter and existing sections untouched,
  Known Script Defects section intact).
- [ ] PM verifies each added claim against live state or the documented evidence.
- [ ] TASKS.md row to Done.

---

## Next Actions

*Owner: whoever wrote last. The future only — delete what has been done. The second of the two sections
the PM reads.*

- [ ] `Tails`: apply the three additions (facts in the PM dispatch brief; evidence in the TASK-0026
  doc `## Implementation` dated entry).
- [ ] PM: verify the skill additions against live state.
- [ ] PM: close (row to Done); then continue the TASK-0026 boot work (instance reconciliation, DHCP
  state repair, stopped-VM `qemu-img check` — the open items of the diagnosis run).

---

## Plan

*Owner: `Amy`.*

Not planned by Amy: operator-directed documentation update with a PM-written Definition of Done;
the plan content is the operator instruction plus the evidence pointer above.

---

## Implementation

*Owner: `Tails`.*

### 2026-10-02: Tails run, vm-deploy skill updated with the three TASK-0026 findings

Target: `~/.config/opencode/skills/vm-deploy/SKILL.md` (outside the repo, no git). Additions only;
frontmatter, all pre-existing sections, and Known Script Defects untouched.

1. **Instance-pinning rule** (top of `## Step-by-Step Workflow`, the skill's virsh procedure,
   SKILL.md lines 46-56). Verified against the scripts. `scripts/vm-create` pins `qemu:///system`
   (domain ops as plain `virsh -c qemu:///system`, no sudo; `virt-install --connect qemu:///system`
   at `scripts/vm-create:76`; `sudo virsh -c qemu:///system` only for `net-*`,
   `scripts/vm-create:23-38`). `scripts/vm-create-fedora-cinnamon.sh` (`--connect qemu:///system`
   line 47, `virsh -c qemu:///system start` line 59) and `scripts/vm-destroy`
   (`virsh -c qemu:///system` lines 10-12) pin it the same way. Outlier:
   `scripts/vm-create-rocky.sh:51-52` (`virsh define`, `virsh start`) and `:55`
   (`virsh domifaddr`) are bare `virsh` (no `-c`), which for howard resolves to `qemu:///session`
   (live: `virsh uri` → `qemu:///session`). No-sudo `virsh -c qemu:///system` works for domain ops
   (howard is in the `libvirt` group, verified via `id -nG howard`); live `virsh -c qemu:///system
   list --all --name` returns the system domains without sudo.
2. **Gotcha "Dual libvirt instance (session vs system)"** (`## Hard-won Gotchas (TASK-0026)`,
   SKILL.md lines 144-152). Evidence re-verified live today. `virsh -c qemu:///session list --all`
   shows `cinnamon-1` running (Id 4); state dir `~/.config/libvirt/qemu/lib/domain-4-cinnamon-1/`
   holds monitor.sock and master-key.aes; QEMU pid 318174 (howard, ppid 4053, the systemd --user
   process per the TASK-0026 run) whose cmdline shows `driver":"qcow2"` on both blockdev format
   entries (overlay and golden backing). `virsh -c qemu:///system list --all` shows `cinnamon-1`
   shut off; `sudo virsh -c qemu:///system dumpxml cinnamon-1` line 21 is still
   `<driver name='qemu' type='raw'/>`. `virtqemud` pid 316107 and `libvirtd` pid 163568 confirmed
   via `sudo ss -xlp` / `ps`. The split was created by the recovery run's bare
   `virsh undefine` / `virsh define` / `virsh start` (no `-c`; step list in the TASK-0026
   `## Implementation` entry, lines 543-544), which landed on `qemu:///session`.
3. **Gotcha "Serial console is silent at firmware-stage stalls"** (SKILL.md lines 154-165).
   Cited evidence: TASK-0026 entry lines 572, 592-595 (zero guest output over a ~20 s attach,
   exactly 1.0 vCPU at 100%, 2-color solid framebuffer). Live re-verified: the running domain's
   serial is a pty (`-chardev pty,id=charserial0` in the QEMU cmdline; `<serial type='pty'>` in
   both instances' `virsh dumpxml`).
4. **Gotcha "Stale `virsh console` clients block new attaches"** (SKILL.md lines 167-177).
   Cited evidence: TASK-0026 entry line 582 (`script -c timeout 30 virsh console cinnamon-1
   /dev/null`, started 13:29, held the console ~3 h, the 30 s timeout did not kill `virsh`,
   client SIGTERMed, passive attach with no guest impact). Live check at update time: no stale
   console clients (`ps aux | grep -E "virsh console|console cinnamon-1" | grep -v grep` clean).

**Checks run:** `grep -n` over all four `scripts/vm-create*` / `vm-destroy` files for virsh
instance usage; live `virsh uri` (both users), `virsh -c qemu:///session list --all`,
`virsh -c qemu:///system list --all`, `sudo virsh -c qemu:///system dumpxml cinnamon-1` (driver
line), `ls ~/.config/libvirt/qemu/lib/`, `sudo ss -xlp` (virtqemud/libvirtd sockets), `ps -o
pid,ppid` on the QEMU, `ps aux` for stale console clients. No state was modified.

**Alternatives considered:** Pin the skill to `qemu:///session` instead of `qemu:///system`.
Rejected. `qemu:///system` is the instance the canonical provisioning script (`scripts/vm-create`,
AGENTS.md section 12), the Fedora script, and `vm-destroy` all pin, and it is what the skill's
own workflow already uses; `qemu:///session` is only where a bare `virsh` silently falls back
for this user. The rule therefore pins `qemu:///system` and names `scripts/vm-create-rocky.sh`
as the outlier that deploys to the session instance.

**Competing priorities:** The `scripts/vm-create-rocky.sh` bare-`virsh` defect is recorded in the
skill as a gotcha and deployer rule, not fixed in the script (out of scope for this task; the
skill's Known Script Defects section is PM/TASK-0030-adjacent territory and was left intact).

---


## Review

*Owner: `Shadow`. Read-only — findings only, no edits. Severity order, blockers first.*

Skipped on record (see Status deviation); documentation-only change, no code to review.

---

## Security

*Owner: `Omega`. Read-only. Severity order.*

Skipped on record (see Status deviation); no new attack surface.

---

## License (Charmy)

*Owner: `Charmy`. Fourth in the review chain. Every license is verified at the upstream source
repository and the ref used, never from a copy in this repo.*

Skipped on record (see Status deviation); no code added.

---

## Test Results

*Owner: `Big`. Verdicts, never raw log dumps.*

PM verifies the added claims against live state (see Status deviation); no harness applies to a
documentation-only change of a file outside the repo.

---

## Docs

*Owner: `Vector`.*

The skill file itself is the doc change; it lives outside the repo (operator-specified location),
so no README or CHANGELOG change applies.

---

## Release

*Owner: `Knuckles`.*

N/A — the skill is outside the repo; nothing to commit or merge.

---

## Archive

*Owner: `Espio`, the only agent that deletes. Superseded detail lands here rather than being
lost. Decisions, verified facts, rejected options with their reasons, known traps, and anything the
user said are never deleted.*
