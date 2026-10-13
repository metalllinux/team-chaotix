# TASK-0035 — Cinnamon Control Center Power pane: D-Bus Unauthorized (36) traceback at cs_power.py:883

> **Section order below is fixed.** Each agent writes to its own section and no other. `Robotnik`
> reads only `## Status` and `## Next Actions`. Do not reorder, rename, or remove sections.

- **Created:** 2026-10-10

---

## Status

*Owner: `Robotnik`. Keep this SHORT and CURRENT — it is one of only two sections the PM reads, so a
stale entry means the whole loop runs on bad information.*

### 2026-10-13: items 1-4 complete; classification (b) upstream Cinnamon behavior; item 5 skipped (N/A); item 6 is Big's

Tails executed ## Plan items 1-4 (evidence in ## Implementation). Reproduces on both VMs (controlled launches, exact traceback at `cs_power.py:883`, D-Bus `Unauthorized (36)`; `cs_power.py` md5 identical on both VMs and in the canonical checkout). Root cause: the answering service is base-OS `tuned-ppd` (owns both candidate names; `power-profiles-daemon` not installed); the rejection is inside the service — polkit gate on `Set`/`ActiveProfile`, action `net.hadess.PowerProfiles.switch-profile` requires interactive auth; SELinux ruled out. Classification (b) upstream Cinnamon behavior (unguarded init self-trigger); excludes the port-bug and environment-configuration boxes. Item 5 skipped (fix path N/A in this environment); item 6 (final verdict) is Big's. Shadow done: no blockers; five findings (3 should-fix — user-click path untested vs intake Unknown "functionality degraded?", `allow_active` misattribution sentence, redundant no-op `Set` unstated; 2 nit — service-code citation path, Vector PPD-comparison scope note). Omega done: two findings — high/secrets = the standing TASK-0033 `~/AI/secrets/` mode step-stop (already blocked there for operator action); medium/authz confirms Shadow finding 2 (misdirection real; the only sanctioned fix location is upstream Cinnamon code). Standing PAT origin-URL risk verified resolved (plain origin URL, no repo credential, `~/.git-credentials` mode 600). Big done: PASS, zero FAILs; final verdict in ## Test Results (6 checks requested, 5 executed, 1 N/A — item 5 conditional branch not taken); TASK-0026 DoD box 2 stays open for the Power pane until upstream changes, this doc is the standing reference. Charmy done: pass, no license work this task; out-of-domain flag — live PAT embedded in the project root repo's local origin URL (distinct instance from the `cinnamon/` subrepo URL Omega verified plain). Next: Tails fix round (Shadow should-fix 1-3 + nits 4-5; Omega's high stays the operator-owned TASK-0033 step-stop). Tails fix round done: all five carried items addressed in ## Implementation with new evidence (user-click flagged inferred-not-tested, intake Unknown resolved, misattribution corrected with `polkit.py:24 flags = 1`, no-op `Set` framed, citations completed, Note for Vector recorded). Re-run the chain: Shadow done — clean, all five items verified resolved, no new findings. Next: Omega re-run — done, clean (medium/authz resolved against the corrected text; high stays the operator-owned TASK-0033 step-stop). Next: Big re-run — done: PASS, re-verified (fix-round claims independently spot-checked; no-op chain verified end-to-end from source; PASS strengthened, not reversed). Next: Charmy re-run — done: clean (license-neutral fix round; pass verdict stands). Re-run chain fully clean. Vector done: README third known-issue paragraph added (uncommitted, rides the canonical push per the TASK-0026/0027 precedent), upstream report for `linuxmint/cinnamon` drafted in ## Docs (operator step-stop per AGENTS.md §8, not submitted), no other doc change needed. Next: Knuckles.

### 2026-10-10: intake — Power pane D-Bus `Unauthorized (36)` error split out of the TASK-0034/TASK-0026 Big gate findings

Source: planning/docs/TASK-0034-cinnamon-shell-no-render.md `## Test Results`, dated Big entry 2026-10-08 ("### 2026-10-08: Big — 12-pane screenshot gate"), and planning/docs/TASK-0026-cinnamon-control-center-comparison.md `## Test Results`, dated Big entry 2026-10-08. Machine: `Rocky_Linux_10_Cinnamon` (192.168.122.4), session 2 (wayland/gdm-password, seat0/tty2). Defect: launching the Power pane (`power` module → `cs_power.py`) of `cinnamon-settings` emits a traceback at `cs_power.py:883 on_my_value_changed`, D-Bus `Unauthorized (36)`; the process survived through the pane and was killed by the recorded pid; the other 11 of 12 panes are clean (ERR_LINES=0, stderr empty). It was not routed to Tails as a blocker during the gate; recorded for the review chain. PM decision (recorded in the TASK-0026 `## Status` 2026-10-10 entry): open as a new task after the TASK-0026 item 4 review chain. TASK-0026 DoD box 2 ("All panes ... load without console errors") stays open on this task's verdict. Login: `howard`, password at `~/AI/secrets/pass.txt` (never written to any file). Every virsh command passes `-c qemu:///system`.

**Now:** diagnosis not started; next is `Amy`'s plan.

**Environment / scope:**
- Files in scope: VM session state on `Rocky_Linux_10_Cinnamon` first; `Fedora_45_Cinnamon` for reproduction; `cinnamon-control-center` source in the canonical checkout (~/Linux/projects/cinnamon-for-rocky10) only if a port bug is found
- Touches the DB schema: no
- Graphical UI: no (console/stderr evidence only; the no-render limitation applies, so screenshot-level verification is impossible)
- Rocky Linux target: yes

**Unknowns:**
- Whether the error reproduces on `Fedora_45_Cinnamon` (evidence in the two source docs; check before planning).
- Which D-Bus interface/method `cs_power.py:883` (`on_my_value_changed`) calls, and why the reply is `Unauthorized (36)` (interface policy, method rules, or missing service).
- Whether Power pane functionality is degraded despite the surviving process.

---

## Definition of Done

- [x] Root cause established with command + output evidence: what `cs_power.py:883` (`on_my_value_changed`) is calling, and why the D-Bus call returns `Unauthorized (36)` on `Rocky_Linux_10_Cinnamon` (interface, method, policy/permission path).
- [x] Reproduction established on `Fedora_45_Cinnamon` (reproduces or does not, with evidence).
- [x] Classification recorded: Cinnamon port bug versus upstream behavior versus VM session/environment configuration, with evidence.
- [x] If fixable in this environment: fix in the canonical checkout plus process-level verification (Power pane of `cinnamon-settings` launches with no D-Bus `Unauthorized` traceback, app survives, killed by recorded pid). Screenshot-level verification is not possible pending the no-render limitation (TASK-0026/TASK-0034). (Conditional box, not applicable: classification (b) upstream Cinnamon behavior, item 5 skipped per the plan conditional, no in-environment fix exists, the fix belongs upstream in `linuxmint/cinnamon`.)
- [x] `## Test Results` updated with the final verdict.

---

## Next Actions

- [x] `Amy`: plan the diagnosis (root cause of the D-Bus `Unauthorized (36)` error, reproduction on `Fedora_45_Cinnamon`, classification, and the fix path if a port bug). Read only the two dated source entries named in `## Status`, not the whole docs. (done 2026-10-12, see ## Plan)
- [x] `Tails`: execute ## Plan items 1-4 (Rocky reproduction, Rocky root cause, Fedora reproduction, classification); item 5 is conditional on the item 4 verdict, item 6 is Big's final verdict. (done 2026-10-13: classification (b) upstream behavior, item 5 skipped N/A, see ## Implementation)
- [x] `Shadow`: review the diagnosis (no code change; findings in ## Implementation) against ## Plan and the DoD; first of the fixed chain Shadow → Omega → Big → Charmy, write to ## Review. (done 2026-10-13: no blockers, five findings, see ## Review)
- [x] `Omega`: review the diagnosis for attack surface; second of the fixed chain, write to ## Security. (done 2026-10-13: two findings, see ## Security; high maps to the standing TASK-0033 step-stop)
- [x] `Big`: plan item 6 — the final verdict in ## Test Results, per the DoD; third of the fixed chain. (done 2026-10-13: PASS, zero FAILs, see ## Test Results)
- [x] `Charmy`: license compliance review; fourth of the fixed chain, write to ## License (Charmy). (done 2026-10-13: pass, no license work, see ## License (Charmy))
- [x] `Tails`: fix round — Shadow should-fix 1-3 (user-click path / intake Unknown, `allow_active` misattribution, no-op `Set` framing) + nits 4-5; Omega's medium/authz corroborates finding 2. Write fixes and new evidence to ## Implementation. (done 2026-10-13, see ## Implementation)
- [x] `Shadow`: re-run after the fix round — verify findings 1-3 and nits 4-5 are resolved in ## Implementation; first of the re-run Shadow → Omega → Big → Charmy, write the verdict to ## Review. (done 2026-10-13: clean, see ## Review)
- [x] `Omega`: re-run — verify the medium/authz finding against the corrected ## Implementation text; second of the re-run chain, write the verdict to ## Security. (done 2026-10-13: clean, see ## Security)
- [x] `Big`: re-run — re-verify the final verdict in ## Test Results against the post-fix ## Implementation; third of the re-run chain, write the verdict to ## Test Results. (done 2026-10-13: PASS re-verified, see ## Test Results)
- [x] `Charmy`: re-run — re-verify license compliance against the post-fix ## Implementation; fourth of the re-run chain, write the verdict to ## License (Charmy). (done 2026-10-13: clean, see ## License (Charmy))
- [x] `Vector`: update README/docs to match the implementation (diagnosis, no code change); handle the Note for `Vector` recorded in ## Implementation (upstream report framing, missing PPD-comparison data point, external-repo issue is an operator step-stop per AGENTS.md §8). Write what changed to ## Docs. (done 2026-10-13, see ## Docs)
- [ ] `Knuckles`: release step — verify the DoD checklist, commit + push what is pushable per house rules, handle the uncommitted canonical-repo README change (rides the push) and the upstream-report draft in ## Docs (external repo, operator step-stop per §8), record exact operator steps where the standing TASK-0033 rotation step-stop blocks a push, close the GitHub Issue for this task if one exists. Write the outcome to ## Release.

---

## Plan

*Owner: `Amy`.*

**Why this task exists** — TASK-0026 DoD box 2 ("all panes ... load without console errors")
stays open on this task's verdict (TASK-0026 `## Status` 2026-10-10 decision). The 2026-10-08
Big 12-pane gate (TASK-0034 `## Test Results`, dated Big entry) found exactly one console error
of 12 panes: the Power pane (`power` module, `cs_power.py`) traceback at `cs_power.py:883
on_my_value_changed`, D-Bus `Unauthorized (36)`, process survived, killed by recorded pid;
the other 11 panes clean (ERR_LINES=0, stderr empty). This task is that diagnosis, split out of
the gate per the recorded PM decision. It serves the project goal of a clean, verifiable Cinnamon
port on Rocky 10.

**What it unblocks / what blocks it** — Unblocks: TASK-0026 DoD box 2, then the TASK-0026
release gate (the signed rebuild, whose publish is already held on the operator PAT rotation in
TASK-0024/TASK-0033 territory); a console-clean 12-pane gate once the no-render state is resolved;
the Power-pane behavior record for an upstream report. Blocks it: nothing in this repo, no CI.
Everything blocking is external: `Rocky_Linux_10_Cinnamon` (192.168.122.4) and
`Fedora_45_Cinnamon` (192.168.122.176) VM state, the operator's live desktop on Rocky
(session 2, Wayland), and only if the classification is upstream behavior, the upstream Cinnamon
repo (out of scope; an external issue is a step-stop per AGENTS.md section 8).

**MVP** — DoD boxes 1-3: root cause with command + output evidence, reproduction on
`Fedora_45_Cinnamon` (reproduces or does not, with evidence), classification. That is the value:
TASK-0026 box 2 needs a verdict either way. DoD box 4 (fix) is the conditional branch, not the
default (see A5: a port-introduced defect is effectively pre-ruled-out). Screenshot-level
verification is not deferred, it is impossible under the no-render limitation (A7); process-level
only.

**What this makes harder later.** (a) If item 5 runs, the fix is a ninth dirty port file in the
`cinnamon/` checkout, one more upstream divergence to reconcile at every future sync, and the
ported file no longer matches upstream line-for-line (the diff must be recorded in
`## Implementation`). (b) If the verdict is upstream behavior, the traceback persists on both VMs
until upstream changes; the 12-pane gate's console-clean criterion stays open for the Power pane,
and this doc is the standing reference for that gate. (c) If the verdict is environment
configuration (a policy file on the Rocky guest), the fix lives in guest state, not in this repo;
`## Implementation` must record the working state in copyable form (file path plus content, or
package version).

**Assumptions** (stated, not silent):
- A1. Login `howard`, password at `~/AI/secrets/pass.txt` (verified present, 9 bytes, mode 644;
  `sshpass -f`, never written to any file), every `virsh` command with `-c qemu:///system` (per
  `## Status`).
- A2. The installed `cs_power.py` on the Rocky guest is identical to the canonical checkout file
  (verified 2026-10-12: the file is not among the 8 dirty port files in the `cinnamon/` checkout;
  `git diff HEAD -- files/.../cs_power.py` and `git diff origin/master -- files/.../cs_power.py`
  both empty; the recorded traceback line 883 equals checkout line 883, the `proxy.Set` call).
- A3. The failing call, deduced from source (live confirmation is item 1): `cs_power.py:208`
  opens the SYSTEM bus; `:211-218` probes bus names in order `net.hadess.PowerProfiles` then
  `org.freedesktop.UPower.PowerProfiles`, at object path `/` plus the dotted name, on interface
  `org.freedesktop.DBus.Properties`, and keeps the first whose `Get Profiles` succeeds; `:883`
  is method `Set` on that interface with body `(ssv)`: (dbus_name, "ActiveProfile", variant
  string), i.e. the three-argument (interface, property, value) form. The pane log prints the
  winning name (`Found power profiles on Dbus at <name>`, `:217`). Open question, not a fact:
  the standard GDBus Properties interface advertises `Set` as two-argument (property, value);
  item 2's introspection reads the signature the service actually advertises.
- A4. For the line 883 traceback to fire, `Get Profiles` (`:216`), `Get ActiveProfile` (`:891`),
  and the `set_active_iter` (`:892`, which fires `changed` at `:869` and thus
  `on_my_value_changed` at `:878-883`, which has no try/except) must all succeed. The combo
  exists only if `Get Profiles` succeeded, so the service is present on the Rocky system bus and
  "missing service" is ruled out by deduction (marked: deduction; item 1 confirms the name
  live). The error is a rejection of the `Set`, not of the service.
- A5. The port packages neither `power-profiles-daemon` nor `upower` (verified 2026-10-12:
  `spec/` lists neither; `upower-devel` is a BuildRequires of `muffin.spec` only;
  `upower-glib-devel` is commented out "not available" in `cinnamon-control-center.spec` and
  `cinnamon-settings-daemon.spec`). The answering service is a base-OS package on each VM.
  "Cinnamon port bug" is possible only via the ported `cs_power.py` file, which per A2 is
  unmodified upstream code; item 4 rules the box out formally with evidence (md5 plus the
  dirty-file list).
- A6. The error string `Unauthorized (36)` has two candidate readings, both to be settled live;
  stated as uncertainty, not fact: (i) a dbus-daemon policy rejection, D-Bus error name
  `org.freedesktop.DBus.Error.AccessDenied` (the text "Unauthorized" is consistent with the
  daemon's reply text), GLib `GDBusError` 26 from memory; or (ii) the service refusing a write
  to a read-only property, D-Bus error name `org.freedesktop.DBus.Error.PropertyReadOnly`,
  GLib `GDBusError` 36 from memory. The enum numbering is from memory and not certain; item 2's
  raw wire reproduction is decisive.
- A7. The no-render limitation applies (per `## Status`): console/stderr evidence only;
  screenshot-level verification is impossible.
- A8. No Fedora per-pane data exists: the 2026-10-08 comparison launched only the CC overview on
  Fedora (checked in the two source entries named in `## Status`). The reproduction must be run
  fresh (item 3).
- A9. The `cinnamon/` checkout is a shallow clone of `github.com/linuxmint/cinnamon` (verified
  2026-10-12: `git rev-parse --is-shallow-repository` = true, no tags, HEAD `61695c7` one ahead
  of `origin/master` `e9ba28a`). File-version comparison across VMs must be done on the installed
  files (md5), not from local tags.

**Work breakdown** — one agent, one item, one turn. Briefs point at this doc; they do not restate
evidence. Record one-line findings plus the command that produced each (no log dumps). Every
guest command over SSH as `howard` via `sshpass -f`; every `virsh` with `-c qemu:///system`.

| # | Item | Owner agent | Acceptance criterion | Parallel with |
|---|---|---|---|---|
| 1 | Rocky controlled reproduction. Preflight: `virsh -c qemu:///system list` plus `snapshot-list` (record the `2026-10-07-task0034-pre` checkpoint state). Check the guest `/tmp/big-t0034-app-05.log` (2026-10-08 Power pane log) for presence, record its `Found power profiles on Dbus at <name>` line if present. Then one `cinnamon-settings power` launch on `Rocky_Linux_10_Cinnamon` with the session 2 env replay per the 2026-10-08 gate procedure (`setsid env <session env>`, pidfile, stderr log), killed by the recorded pid; record the launch time (disturbance record) | `Tails` | Dated `## Implementation` entry: reproduces (traceback at `cs_power.py:883` with the `Unauthorized (36)` string) or does not; the matched dbus_name from the `:217` print; launch pid plus kill confirmed; old-log state (present with the line, or absent) | Blocks 2 |
| 2 | Rocky root cause. Identify the service and the rejection layer: `busctl --system list` (which of the two names is present); `busctl --system introspect <name> <path>` for `org.freedesktop.DBus.Properties` and the service's own interface (`ActiveProfile` property flags; whether a dedicated setter method exists, e.g. `SetActiveProfile`; the advertised `Set` in-arg signature); `rpm -q`/`rpm -qf` for the service's D-Bus policy file (from `rpm -ql <pkg>`, expect `/usr/share/dbus-1/system.d/`) and for the installed `cs_power.py`; read the policy file and record the lines that bear on `ActiveProfile`/`Set`; polkit action files for power; `systemctl status` of the service unit; raw reproduction as `howard` over the system bus of `Properties.Set` with (dbus_name, "ActiveProfile", variant) via `dbus-send --print-reply` (or `gdbus call`) yielding the exact D-Bus error name plus text; control: the same `Properties.Get ActiveProfile` succeeds; system journal for the service around the item 1 window (dbus-daemon denial, polkit decision, SELinux denials via the audit stream) | `Tails` | Root-cause statement with command + output per fact: the exact D-Bus error name on the wire; the rejecting component (daemon policy file:line, or service property flag, or polkit action, or SELinux denial with context); service package name plus version; guest `cs_power.py` md5 | Depends on 1 |
| 3 | Fedora reproduction. One `cinnamon-settings power` launch on `Fedora_45_Cinnamon` (X11): capture the session env from the running session process (`tr '\0' '\n' < /proc/<pid>/environ`; rediscover the pid via `loginctl list-sessions` plus `pgrep -u howard` if it changed), `setsid env <session env>`, pidfile, stderr log, killed by the recorded pid; then `rpm -qf` of the installed `cs_power.py` (package plus version), the file md5 on both VMs, the matched dbus_name from the pane log, `busctl --system list` for the power names | `Tails` | Dated `## Implementation` entry: reproduces or does not (evidence is the stderr line); Fedora service identity (name, package, version); cross-VM `cs_power.py` md5 (same or different; if different, both recorded) | Independent of 1, 2 |
| 4 | Classification plus fix-path decision. Exactly one of: (a) Cinnamon port bug, (b) upstream Cinnamon behavior (unmodified code; reproduces on both VMs against base-OS services), (c) VM session/environment configuration (base-OS package/policy difference on Rocky), with evidence from items 1-3; fix-path decision: in-environment fix only if a port-introduced defect is found (item 5 runs), otherwise N/A with what would settle it recorded | `Tails` | Dated `## Implementation` entry: the classification line plus the fix-path decision plus the reasoning, citing items 1-3 | Depends on 2, 3 |
| 5 | Fix (only if item 4 says fixable in this environment). Implement in the canonical checkout `cinnamon/files/usr/share/cinnamon/cinnamon-settings/modules/cs_power.py` (dirty-tree practice; commit at checkpoint). Candidate fix shapes (item 4 picks on item 2 evidence): call the service's dedicated setter method instead of `Properties.Set`; suppress the startup self-trigger (block `changed` during `on_my_setting_changed` so pane init does not send `Set`); or wrap `:883` in try/except per the existing style at `:893-894`. Verification is file-level on the guest: record the pre-place md5, place the file, re-run the single Power-pane launch | `Tails` | DoD box 4: dated `## Implementation` entry with the Changes table row and process-level evidence: no D-Bus `Unauthorized` traceback in stderr, app survives (pid alive after launch), killed by the recorded pid; pre-place md5 recorded | Depends on 4 (skipped if N/A) |
| 6 | Final verdict. `## Test Results`: checks requested vs run; verdict prose covering DoD boxes 1-5 (root cause, reproduction, classification, fix status or N/A); the 2026-10-08 12-pane gate recorded as reference (no gate re-run: the Power pane is the only in-scope pane, the other 11 are clean per the gate) | `Big` | All DoD boxes verifiable from the doc; checks table complete; verdict prose names each FAIL's evidence and owner | Depends on 5, or on 4 |

**Dependencies and sequence.** 1 to 2 to 4 to 6, with 3 **independent of 1-2, explicitly**
(different VM, no shared state) and merging at 4; 5 is a conditional branch off 4 (skipped when
the fix path is N/A, which is the expected path per A5). The single inference slot forces a
physical order; the suggested order is 1, 2, 3, 4, (5), 6 (Rocky work together, then Fedora, then
classification).

**Critical path.** 1 to 2 to 4 to 5 to 6: 5 turns when a fix applies; 1 to 2 to 4 to 6: 4 turns
on the expected no-fix path (3 inserted before 4). The longest dependent chain is 1-2-4-5-6.

**Estimates** (hours; three-point `T = (O + 4M + P) / 6`):

| # | Item | O | M | P | T |
|---|---|---|---|---|---|
| 1 | Rocky controlled reproduction | 0.5 | 1 | 2 | 1.2 |
| 2 | Rocky root cause | 1 | 2 | 4 | 2.3 |
| 3 | Fedora reproduction | 0.5 | 1 | 2 | 1.2 |
| 4 | Classification plus fix decision | 0.5 | 1 | 2 | 1.1 |
| 5 | Fix plus verify (conditional) | 1 | 2 | 4 | 2.3 |
| 6 | Big verdict | 0.5 | 1 | 2 | 1.1 |
| | **Total nominal** | | | | **9.2** |

Buffer: two live VMs (one of them the operator's desktop), unknown root cause, single inference
slot: +35% (about 3.2 h). **Planned total about 12 h** with the fix path; about 10 h without.

**Risks.**

| Risk | Likelihood | Impact | Mitigation | Contingency |
|---|---|---|---|---|
| Old gate log `/tmp/big-t0034-app-05.log` gone (guest reboot or tmpfs since 2026-10-08) | Medium | Low (the re-run is primary evidence anyway) | Item 1 checks and records either state | None needed; item 1's launch re-establishes the traceback |
| Item 1/3 launches disturb the operator's live desktop (Rocky session 2) | Certain (small) | Medium | Accepted-disturbance precedent (the 2026-10-08 gate ran exactly this); single launch, killed by recorded pid (never `pkill -f`), short window, time recorded in `## Implementation` | Reschedule if the operator is active (PM judgment); no snapshot needed (no state change beyond launch/kill) |
| Reproduction nondeterministic (clean launch on re-run) | Low | High (root cause blocked) | Item 1: up to 3 controlled re-runs with the state recorded each time (service active, `Get` results); if still clean, proceed to item 2 on the recorded 2026-10-08 gate evidence | Verdict "not reproducible on the re-run date; root cause bounded to the gate window"; classification proceeds with the bounded uncertainty stated |
| Error string ambiguous (A6: AccessDenied vs PropertyReadOnly) | Medium | Medium | Item 2's raw wire reproduction reads the exact D-Bus error name; no reliance on memory of the enum | If the wire name matches neither candidate, record the raw name and re-derive the mapping |
| Fedora session env capture fails (session leader pid changed or session dead) | Low | Medium (item 3 blocked) | Rediscover via `loginctl list-sessions` plus `pgrep -u howard`; `/proc/<pid>/environ` is readable by the owner (`howard`) | If the X11 session is dead, the reproduction needs an operator re-login: record and stop, PM judgment (no automated re-login) |
| SELinux denials on Rocky mask a polkit/permission denial as `Unauthorized` | Low | Medium | Item 2 checks the audit stream around the item 1 window | Record the denials plus context; classification is environment (SELinux) with the policy note |
| Item 5 leaves the guest file diverged from the -4 payload | Certain if 5 runs | Low | Pre-place md5 recorded; `rpm -V` state recorded | Rollback restores the pre-place file (see Rollback) |
| 32k turn cap truncates an evidence-heavy turn (section 14) | Medium | Medium | Briefs carry at most three file edits; one-line findings plus commands, no output dumps; small passes | Re-dispatch with a smaller brief; detect via the session DB (`finish: "length"`, `tokens.output = 32000`) |
| PAT embedded in the `cinnamon/` subrepo origin URL (local `.git/config`, uncommitted, never pushed; the value is never written to any doc) | Standing | High if leaked | Flagged for Omega in `## Security`; no command in this plan pushes from that checkout | Rotation per the TASK-0033 `## Security` step (operator-owned); not touched by this task |
| `~/AI/secrets/pass.txt` mode is 644 (AGENTS.md section 4 requires 600/700) | Standing | Medium | Flagged for Omega; this task uses `sshpass -f` only, never cats, never writes | Operator chmod (operator-owned, not an agent step) |
| No-render: window-level verification impossible | Certain | Low (DoD scoped to process level) | A7; the verdict is process-level only | Re-verification deferred until the no-render state is resolved (TASK-0026/TASK-0034 territory) |

**Validation.** Environment: `Rocky_Linux_10_Cinnamon` (192.168.122.4) and
`Fedora_45_Cinnamon` (192.168.122.176); every `virsh` with `-c qemu:///system`; SSH as `howard`
via `sshpass -f` (password never written); console/stderr evidence only (A7). Checks:
(1) item 1's entry shows the reproduction (or bounded non-reproduction) plus the matched
dbus_name; (2) item 2's entry shows the exact D-Bus error name on the wire plus the rejecting
component with file:line; (3) item 3's entry shows the Fedora reproduction yes/no plus the
`cs_power.py` md5 on both VMs plus package identity; (4) item 4's entry shows exactly one
classification line plus the fix decision; (5) if item 5 ran: pre/post md5 plus the clean
single-pane re-run (no `Unauthorized` traceback in stderr, pid alive after launch, killed by
pid); (6) `## Test Results` (`Big`) shows checks requested vs run with the 2026-10-08 gate
recorded as reference. No human-look pages: nothing is published, nothing is pushed, the
`cinnamon/` checkout is never pushed. TASKS.md row status is `Robotnik`'s.

**Rollback.** Detection: item 5's re-run still shows the `Unauthorized` traceback (fix
ineffective) or shows a new traceback (fix regression); a launched process left running
(`pgrep` check after each kill); a guest `cs_power.py` md5 drift not recorded in
`## Implementation`. Exact reverts:
- No item 5 ran: nothing to revert. Items 1-3 are launches plus read-only probes; every launch is
  killed by its recorded pid; pidfiles are recorded.
- Item 5 ran: restore the pre-place `cs_power.py` (md5 recorded in the item 5 entry), re-run the
  single Power-pane launch, record the state. The baseline state has the traceback (that is the
  pre-fix state); restoring it is the rollback, not a new defect.
- Source checkout: the item 5 change is uncommitted dirty per practice; revert is
  `git -C ~/Linux/projects/cinnamon-for-rocky10/cinnamon checkout -- files/usr/share/cinnamon/cinnamon-settings/modules/cs_power.py`
  (restores the HEAD `61695c7` content). If committed at checkpoint, `git revert <sha>`.
- VM level (only if a VM is left in a worse state): item 1 re-verifies `virsh -c qemu:///system
  snapshot-list`; the Rocky checkpoint `2026-10-07-task0034-pre` (running, Current) and the
  Fedora `2026-10-04T11:37` (shutoff) are the revert assets (both verified present in the
  2026-10-08/2026-10-10 entries).
- Point of no return: none. No published artifact is touched, nothing is pushed, the -4 RPM
  stays in `rpms-local/`, and the snapshots are intact.

---

## Implementation

*Owner: `Tails`.*

**Alternatives considered**

### Problem: session 2 env replay for the controlled launches (items 1, 3)
**Option A — capture from the loginctl session leader pid** · How: `loginctl show-session 2 -p Leader` then `tr '\0' '\n' < /proc/<leader>/environ`. · Pros: matches the plan's stated procedure. · Cons: the leader is root-owned on both VMs (Rocky `gdm-session-worker [pam/gdm-password]` pid 2848, Fedora `lightdm --session-child` pid 1035), so `/proc/<pid>/environ` is unreadable by `howard`; the first Rocky run launched with zero captured vars (SSH-inherited env, app reported `session type: tty`).
**Option B — capture from a user-owned session process** · How: scan `ps -u howard -o pid=,cmd=` for a desktop session process whose environ is readable and contains a display var (`nemo-desktop` on Rocky, `cinnamon --replace` on Fedora); replay that full environ. · Pros: owner-readable; on Rocky it yields exactly the gate's recorded env list (`WAYLAND_DISPLAY=wayland-0`, `XDG_SESSION_ID=2`, `XDG_SESSION_TYPE=wayland`, `XDG_CURRENT_DESKTOP=X-Cinnamon`). · Cons: one extra discovery step; the picked process can differ between runs.
**Chosen:** B, with A recorded as the failed first attempt, because the leader environ is root-only and B reproduces the gate env list verbatim.
**Competing priorities:** byte-identical env to the gate's list was not required; the D-Bus call under test does not depend on display env (proven: the env-broken first Rocky run reproduced the identical traceback).

### Problem: raw wire reproduction of the failing call (item 2)
**Option A — `gdbus call`** · How: GLib-level call, same library as the app. · Pros: mirrors the app. · Cons: spelling the `(ssv)` variant argument on the command line is awkward.
**Option B — `dbus-send --system --print-reply`** · How: `org.freedesktop.DBus.Properties.Set string:<iface> string:ActiveProfile variant:string:balanced`. · Pros: unambiguous signatures, exact wire-level reply (error name plus message). · Cons: none material.
**Chosen:** B, because A6 (the from-memory error-name candidates) is settled by the wire reply; the GLib layer is read separately with a python-gi replay of the exact app call.
**Competing priorities:** none material.

### Problem: resolving the user-click path (Shadow finding 1) under the no-render limitation
**Option A — live UI click test.** How: click a profile in the Power pane on `Rocky_Linux_10_Cinnamon`; record whether a polkit auth dialog appears, whether the switch succeeds with the password, and whether the `:883` traceback fires. · Pros: directly tests the click path. · Cons: impossible under the no-render limitation (A7): the auth dialog needs a live display plus a polkit agent interaction that cannot be observed or completed headlessly; a UI click cannot be driven or verified without a rendered display.
**Option B — source-based determination plus flag.** How: read the service's polkit-check flags (`tuned/utils/polkit.py`) to settle interactive-vs-not, verify a polkit agent is installed and running, and flag the live-desktop click outcome as inferred-not-tested. · Pros: text-only (consistent with A7), decisive on the mechanism (the check is interactive, `flags = 1`), and bounds the live outcome honestly. · Cons: does not produce a live click observation.
**Chosen:** B, because A is impossible under no-render; B settles the mechanism (interactive check, `flags = 1`) and the agent precondition (a `gnome-keyring-daemon` agent is installed and running), and flags the live-desktop click outcome (prompt plus password success) as inferred, not tested.
**Competing priorities:** a live click observation was not achievable; the inference is bounded to the documented precondition (a polkit agent attached to the caller's session), which holds for a live desktop but not for the tested `setsid` env-replay context.

### 2026-10-12: item 1, Rocky controlled reproduction (REPRODUCES)

**Preflight (host).** `virsh -c qemu:///system list`: both VMs running (id 1 `Fedora_45_Cinnamon`, id 2 `Rocky_Linux_10_Cinnamon`). `virsh -c qemu:///system snapshot-list Rocky_Linux_10_Cinnamon`: `2026-10-04T11:36` (shutoff), `2026-10-07-task0034-pre` (running). `virsh -c qemu:///system snapshot-current Rocky_Linux_10_Cinnamon`: current = `2026-10-07-task0034-pre`, state running, parent `2026-10-04T11:36` (the expected checkpoint state).

**Old gate log.** `/tmp/big-t0034-app-05.log` present (408 B, mtime 2026-10-08 18:51 guest-local = 09:51 UTC, the gate window) plus `/tmp/big-t0034-app-05.pid`; the `Found power profiles on Dbus at <name>` line is NOT in the current content and the `Unauthorized` traceback is not in the current content either (content ends at `Loading Themes module`); verified over SSH with `ls -la` + `tail -n 25`. The gate's Power-pane Set attempt is corroborated by the service's own log (item 2): `2026-10-08 18:51:53,503 INFO tuned.exports.dbus_exporter: action 'net.hadess.PowerProfiles.switch-profile' requested by caller ':1.733' wasn't authorized, ignoring the request` in `/var/log/tuned/tuned-ppd.log`.

**Run 1 (env capture broken, recorded).** 2026-10-12T17:02:10Z. Leader pid 2848 environ unreadable (`/proc/2848/environ: Permission denied`; the leader is root's `gdm-session-worker [pam/gdm-password]`, `ps -o pid,user,cmd -p 2848`), so the launch ran with the SSH-inherited env (0 captured vars); app reported `KeybindingWidgets session type: tty`. Launch = `setsid env <captured env> PYTHONUNBUFFERED=1 cinnamon-settings power > /tmp/tails-t0035-rocky-power.log 2>&1 &`, pid to `/tmp/tails-t0035-rocky-power.pid`, killed by the recorded pid. Result: REPRODUCED, traceback at `cs_power.py:883 on_my_value_changed`, `GDBus.Error:org.freedesktop.DBus.Python.dbus.exceptions.DBusException: Unauthorized (36)`; matched name from the `:217` print `Found power profiles on Dbus at net.hadess.PowerProfiles`; pid 36616, kill confirmed (17:02:23Z). `PYTHONUNBUFFERED=1` was added as a logging aid: without it the stdout `Found` line is lost on kill (stdout is block-buffered when redirected); the gate-era log's missing `Found` line is consistent with that.

**Run 2 (gate-conformant env replay, the record).** 2026-10-12T18:23:00Z, window epochs 1791829380-1791829392. Env captured from user-owned session process `nemo-desktop` pid 3306 (`tr '\0' '\n' < /proc/3306/environ`): 42 vars; the session vars equal the gate's recorded list (`XDG_SESSION_ID=2 XDG_SESSION_TYPE=wayland DESKTOP_SESSION=cinnamon-wayland XDG_CURRENT_DESKTOP=X-Cinnamon DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus WAYLAND_DISPLAY=wayland-0 XDG_RUNTIME_DIR=/run/user/1000`); app reported `session type: wayland`. Same launch/kill procedure, artifacts `/tmp/tails-t0035-rocky-power2.log` + `.pid`. Result: REPRODUCED, identical traceback at `cs_power.py:883` with the `Unauthorized (36)` string; matched name `net.hadess.PowerProfiles`; pid 37485, kill confirmed (18:23:13Z).

**Item 1 verdict.** Reproduces on `Rocky_Linux_10_Cinnamon`: traceback at `cs_power.py:883 on_my_value_changed` with the `Unauthorized (36)` string; matched dbus_name `net.hadess.PowerProfiles`; two launches, each killed by its recorded pid (36616, 37485); old gate log present with neither the `Found` line nor the traceback in its current content.

### 2026-10-12: item 2, Rocky root cause (REJECTING LAYER IDENTIFIED)

**Service identity.** `busctl --system list` (over SSH): both candidate names owned by one service, `net.hadess.PowerProfiles` and `org.freedesktop.UPower.PowerProfiles` both to `tuned-ppd` pid 1471, unit `tuned-ppd.service` (root); `upowerd` (`org.freedesktop.UPower`, `upower.service`) is a separate, unrelated service. `rpm -q tuned-ppd`: `tuned-ppd-2.27.0-2.el10_2.noarch`; `systemctl status tuned-ppd`: active (running), description `PPD-to-TuneD API Translation Daemon`, main pid 1471, `/usr/bin/python3 -Es /usr/sbin/tuned-ppd -l`. `rpm -q power-profiles-daemon`: not installed. Object paths per `tuned/consts.py:106-121` (`PPD_DBUS_NAMES`): `/net/hadess/PowerProfiles` (legacy) and `/org/freedesktop/UPower/PowerProfiles`.

**Introspection.** `busctl --system introspect org.freedesktop.UPower.PowerProfiles /org/freedesktop/UPower/PowerProfiles` (same shape on the legacy path): interfaces `org.freedesktop.DBus.Introspectable`, `org.freedesktop.DBus.Properties` with advertised `Set` in-arg signature `ssv` (out `-`), `Get ss→v`, `GetAll s→a{sv}`, and `org.freedesktop.UPower.PowerProfiles` with methods `HoldProfile`/`ReleaseProfile` and signal `ProfileReleased`; no property rows and no dedicated setter method (e.g. no `SetActiveProfile`): the property semantics live in service code, not in the introspection data.

**Raw wire reproduction (as `howard`, `dbus-send --system --print-reply`).** Control PASS: `Properties.Get` `Profiles` returns the three profiles (`power-saver`, `balanced`, `performance`, each `{Profile, Driver=tuned}`) and `Properties.Get ActiveProfile` returns `string "balanced"` (both `method return` from `:1.23`, exit 0). FAIL, on both object paths: `Properties.Set` with `(<iface>, "ActiveProfile", variant:string:balanced)` exits 1 with `Error org.freedesktop.DBus.Python.dbus.exceptions.DBusException: Unauthorized` (captures `/tmp/tails-set{,2}.{out,err}`). **Exact wire error: name `org.freedesktop.DBus.Python.dbus.exceptions.DBusException`, message `Unauthorized`** — a dbus-python Python-exception-to-error conversion (the name is the Python exception class), so the rejection is inside the service, not the daemon.

**The ` (36)` decomposed (A6 settled without from-memory enums).** python-gi replay of the exact app call (`Gio.DBusProxy` on `net.hadess.PowerProfiles` at `/net/hadess/PowerProfiles`, `proxy.Set('(ssv)', "net.hadess.PowerProfiles", "ActiveProfile", GLib.Variant.new_string("balanced"))` as `howard`): `GLib.Error` with `domain: g-io-error-quark`, `code: 36`, `message: GDBus.Error:org.freedesktop.DBus.Python.dbus.exceptions.DBusException: Unauthorized`, and `str(e) == "g-io-error-quark: GDBus.Error:...: Unauthorized (36)"`, byte-identical to the app traceback line. The wire message is `Unauthorized`; ` (36)` is the GLib GDBusError code that python-gi appends in `str()`. A6's two from-memory candidates are both wrong on the name; the wire name is the Python exception class.

**Rejecting component, layer by layer.**
- dbus-daemon policy: NOT the rejector. `/usr/share/dbus-1/system.d/net.hadess.PowerProfiles.conf` (owned by `tuned-ppd-2.27.0-2.el10_2`, `rpm -qf`) grants `<policy context="default">` (all users) `send_interface="org.freedesktop.DBus.Properties"` to the name; the message reached the service (a daemon denial would be `org.freedesktop.DBus.Error.AccessDenied`, which is not what arrived).
- Service code: the rejector. `tuned/exports/dbus_exporter_with_properties.py:45-51` (`_auth_wrapper`): `new_args = self._polkit_auth(action_name, *args); if new_args[-1] == "": raise DBusException("Unauthorized")` — **file:line `/usr/lib/python3.12/site-packages/tuned/exports/dbus_exporter_with_properties.py:49`** (package `tuned-2.27.0-2.el10_2`; the python tree is owned by `tuned`, not `tuned-ppd`). The exported `Set` handler (same file `:34-39`) and `property_setter` (`:70-76`) route the `ActiveProfile` setter through it; `tuned/ppd/controller.py` registers `@exports.property_setter("ActiveProfile", "switch-profile")` on `set_active_profile`, while `ActiveProfile`/`Profiles` are plain `property_getter`s with no auth wrapper (matching the passing `Get` controls).
- polkit: the authorization check is `tuned/exports/dbus_exporter.py:125-144` (`_polkit_auth`): `action_id = <namespace> + "." + action_name` (i.e. `net.hadess.PowerProfiles.switch-profile`), `ret = self._polkit.check_authorization(caller, action_id)`; `ret == 0` (not authorized) sets `caller = ""`, which triggers the raise above. Action file `/usr/share/polkit-1/actions/net.hadess.PowerProfiles.policy` (owned by `tuned-ppd`): action `net.hadess.PowerProfiles.switch-profile` with `<allow_any>no</allow_any> <allow_inactive>no</allow_inactive> <allow_active>yes</allow_active>` — `allow_active=yes` is the PERMISSIVE clause (it permits an active-session user to be authorized via interactive authentication, i.e. an auth dialog), not the restrictor. The check is interactive in code: `tuned/utils/polkit.py:24` sets `flags = 1` (`POLKIT_CHECK_AUTHORIZATION_FLAGS_ALLOW_USER_INTERACTION`) on the `CheckAuthorization` call, so polkit prompts only when a polkit agent is attached to the caller's session. In the tested contexts (controlled reproduction, raw `dbus-send`) the caller's connection was not associated with an agent-attached session (`setsid` env-replay, no `PA_SESSION_ID`), so the check returned not-authorized (0) without prompting and the wrapper raised `Unauthorized`; in a live desktop (a polkit agent attached to the caller's session servicing the action) the same check would prompt and an active-session user is authorized on entering the password.
- Service log (the decision, direct evidence): `/var/log/tuned/tuned-ppd.log`, one `INFO tuned.exports.dbus_exporter: action 'net.hadess.PowerProfiles.switch-profile' requested by caller '<unique>' wasn't authorized, ignoring the request` line per denied call: gate `2026-10-08 18:51:53,503 ... ':1.733'`, run 1 `2026-10-13 02:02:10,861 ... ':1.1224'`, run 2 `2026-10-13 03:23:00,975 ... ':1.1258'` (guest-local JST; the raw reproductions have their own lines for both paths).
- SELinux: `getenforce` → Enforcing; `/var/log/audit/audit.log` unreadable as `howard` (Permission denied, no passwordless sudo); `dmesg | grep -i avc` → no lines. Not the rejector either way: the rejection is a well-formed D-Bus error reply produced by the service, which a SELinux denial cannot produce.

**Root-cause statement.** `cs_power.py:883` calls `Properties.Set` with `(self.dbus_name, "ActiveProfile", variant string)` where `dbus_name` is the first probed name (`net.hadess.PowerProfiles`, `cs_power.py:211-217`); on this guest that name is owned by the base-OS `tuned-ppd-2.27.0-2.el10_2` (PPD-to-TuneD translation daemon, python/dbus-python), whose exported `Set` wraps the `ActiveProfile` setter in a polkit gate for action `net.hadess.PowerProfiles.switch-profile`; the action's `allow_active=yes` is the permissive clause (it permits an active-session user to be authorized via interactive authentication) and the check is interactive in code (`tuned/utils/polkit.py:24`, `flags = 1`) but prompts only when a polkit agent is attached to the caller's session, so in the tested non-agent contexts any non-root caller is denied (not authorized, no prompt); the wrapper raises `DBusException("Unauthorized")` (`/usr/lib/python3.12/site-packages/tuned/exports/dbus_exporter_with_properties.py:49`), which dbus-python ships as error name `org.freedesktop.DBus.Python.dbus.exceptions.DBusException` with message `Unauthorized`; GLib/python-gi renders it with GDBusError code 36 as `Unauthorized (36)`; `cs_power.py:878-883` has no try/except, so the startup self-trigger (`:871` → `:892` → `:869` → `:878` → `:883`) raises the traceback. The dbus-daemon policy allows the send; polkit denies the authorization; the service converts the denial into the wire error. The `:883` `Set` in the startup self-trigger is a no-op: it writes back the profile just read at `:891` (the combo is set at `:892` before the failing `Set`), so the displayed profile is already correct and the startup traceback has no effect on the displayed value; a user-initiated click instead writes the user-selected profile (a real change) through the same check.

**Guest `cs_power.py` md5.** `ab9499015f1484b20add77d54385660d` (`md5sum` over SSH) — identical to the canonical checkout file (same md5, host `md5sum`) and to the Fedora guest (item 3).

### 2026-10-12: item 3, Fedora reproduction (REPRODUCES)

**Launch.** `Fedora_45_Cinnamon`, X11 session (session 2, seat0). First attempt: session leader pid 1035 is root's `lightdm --session-child 13 20` (environ unreadable); the launch with zero captured env died at GTK (`Gtk-ERROR **: Can't create a GtkStyleContext without a display connection`, pid 23496 aborted) — invalid attempt, recorded, no kill needed (already dead). Valid attempt: env captured from the user-owned shell process `cinnamon --replace` pid 1374 (`tr '\0' '\n' < /proc/1374/environ`): 44 vars incl. `XDG_SESSION_TYPE=x11 DISPLAY=:0 XDG_SESSION_ID=2 XDG_CURRENT_DESKTOP=X-Cinnamon DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus XDG_RUNTIME_DIR=/run/user/1000`; same `setsid env <session env> PYTHONUNBUFFERED=1 cinnamon-settings power` + pidfile + kill-by-pid procedure. 2026-10-12T18:10:43Z, window epochs 1791828643-1791828655, pid 23732, kill confirmed.

**Result: reproduces.** Pane log `/tmp/tails-t0035-fedora-power.log` (evidence is the stderr line): `session type: x11` → `Found power profiles on Dbus at net.hadess.PowerProfiles` → identical traceback at `cs_power.py:883 on_my_value_changed` with `GDBus.Error:org.freedesktop.DBus.Python.dbus.exceptions.DBusException: Unauthorized (36)`. Service-log corroboration: `/var/log/tuned/tuned-ppd.log` line `2026-10-13 03:10:44,038 INFO ... action 'net.hadess.PowerProfiles.switch-profile' requested by caller ':1.518' wasn't authorized` (guest-local JST = 18:10:44Z).

**Fedora service identity.** `busctl --system list`: `net.hadess.PowerProfiles` + `org.freedesktop.UPower.PowerProfiles` both owned by `tuned-ppd` (pid 869, `tuned-ppd.service`, root). `rpm -q tuned-ppd`: `tuned-ppd-2.27.0-3.fc45.noarch` (same upstream 2.27.0 as Rocky's `2.27.0-2.el10_2`, different distro packaging).

**Cross-VM `cs_power.py` md5: SAME.** Rocky `ab9499015f1484b20add77d54385660d`, Fedora `ab9499015f1484b20add77d54385660d`, canonical checkout `ab9499015f1484b20add77d54385660d` (three-way `md5sum`). Package identity of the file: Rocky `rpm -qf` → `cinnamon-6.7.4-4.el10.x86_64`, Fedora `rpm -qf` → `cinnamon-6.7.5^unstable-3.fc45.x86_64` (different package versions, identical file content).

### 2026-10-12: item 4, classification and fix-path decision

**Classification: (b) upstream Cinnamon behavior** — unmodified code; reproduces on both VMs against base-OS services.

**Reasoning (citing items 1-3).** The port is exonerated: the guest `cs_power.py` on both VMs is md5-identical to the canonical checkout (items 2 and 3: `ab9499015f1484b20add77d54385660d`), so the failing path is upstream code as shipped, not a port modification (the file is not among the dirty port files per A2), and the port packages neither `power-profiles-daemon` nor `upower` (A5), so it supplies none of the answering service. It reproduces on both VMs (item 1 Rocky Wayland, item 3 Fedora X11) with the identical wire error against the base-OS `tuned-ppd` service on both (items 2 and 3: `2.27.0-2.el10_2` / `2.27.0-3.fc45`, same polkit-gated setter design, same action file shape, same `wasn't authorized` log line), which excludes box (c) VM session/environment configuration: no Rocky-specific setting is involved. What is upstream behavior: `cs_power.py` (unmodified) sends a non-authenticated `Properties.Set ActiveProfile` at pane init via the self-trigger and has no try/except around it (its sibling `:889-895` wraps its `Get` in try/except, `:883` does not), so against an answering service that gates profile switching behind polkit interactive auth, any non-root session in a non-agent context raises the traceback (the check is interactive, `tuned/utils/polkit.py:24` `flags = 1`, but prompts only when a polkit agent is attached to the caller's session; the tested launches had none). The user-click path is the same `on_my_value_changed` → `:883` `Set` → same interactive check, so it is INFERRED, not tested: in a live desktop (a polkit agent attached to the caller's session servicing the action) it would prompt and succeed with the password (no traceback); in a non-agent context it fires the same `:883` traceback. Intake Unknown (line 34, 'functionality degraded?') is resolved: display intact (the `:883` startup `Set` is a no-op, combo set at `:892` before it), profile switching auth-gated by design. The defect is the upstream file's assumption, not anything this port or these VMs configured.

**Fix-path decision: N/A in this environment (item 5 skipped).** No port-introduced defect was found, so the plan's conditional fix branch does not run. What would settle it, recorded: the fix belongs upstream in `linuxmint/cinnamon` (`modules/cs_power.py`): suppress the startup self-trigger so pane init does not send `Set`, or wrap `:883` in try/except per the existing style at `:893-894`; an upstream report is external (AGENTS.md section 8 step-stop, `Vector` drafts, operator decides). No in-guest knob changes the polkit design without masking the upstream behavior, and a guest-local file patch is exactly the upstream divergence the classification says is not a port bug.

### 2026-10-13: fix round — Shadow findings 1-5 (Omega medium/authz corroborates #2)

**Scope.** Address the carried-open items: Shadow should-fix 1-3 and nits 4-5. No code change (classification (b) stands); the fixes are to the diagnostic record in this section. New evidence below; each fact cites the command that produced it.

**New evidence (commands plus output).** All guest commands over SSH as `howard` via `sshpass -f` (password from `~/AI/secrets/pass.txt`, never written to any file); no `virsh` needed this pass (no VM state change; both VMs already running per `virsh -c qemu:///system list`: id 1 `Fedora_45_Cinnamon`, id 2 `Rocky_Linux_10_Cinnamon`).
- Service polkit-check flags (decisive for finding 1): `cat -n /usr/lib/python3.12/site-packages/tuned/utils/polkit.py` → line 24 `flags = 1            # AllowUserInteraction flag`, line 26 `subject = ("system-bus-name", {"name" : sender})`, line 28 `ret = self._authority.CheckAuthorization(subject, action_id, details, flags, cancellation_id)[0]`, line 41 `return 1 if ret else 0`. The `CheckAuthorization` call is made with `POLKIT_CHECK_AUTHORIZATION_FLAGS_ALLOW_USER_INTERACTION` (1): polkit prompts only when a polkit agent is attached to the caller's session, and returns not-authorized (0) otherwise. The same call path (`_polkit_auth` → `check_authorization`) serves both the startup `Set` and a user-click `Set` (both route through `on_my_value_changed` → `:883`).
- Cited-file full guest paths plus owning package (nit 4): `rpm -qf /usr/lib/python3.12/site-packages/tuned/exports/dbus_exporter.py /usr/lib/python3.12/site-packages/tuned/exports/dbus_exporter_with_properties.py` → both `tuned-2.27.0-2.el10_2.noarch`; `rpm -ql tuned-ppd` → only `/etc/tuned/ppd.conf`, `/usr/lib/systemd/system/tuned-ppd.service`, `/usr/sbin/tuned-ppd` (the python tree is owned by `tuned`, not `tuned-ppd`).
- polkit agent availability (bounds the live-desktop inference): `rpm -qa | grep -iE "keyring|cinnamon-polkit|polkit-agent"` → `gnome-keyring-42.1-20.el10.x86_64` (plus `gnome-keyring-pam-42.1-20.el10.x86_64`, `polkit-125-4.el10_2.1`, `polkit-libs-125-4.el10_2.1`, `polkit-pkla-compat-0.1-30.el10.x86_64`); `pgrep -af "polkit-agent|pk-agent|keyring-daemon"` → `2873 /usr/bin/gnome-keyring-daemon --daemonize --login` (running). So a polkit agent is installed and running for the login session (`gnome-keyring-daemon`, which registers a polkit agent; no general `cinnamon-polkit` agent was found in the installed set), though no-render prevents confirming which agent (if any) is attached to session 2 for the `switch-profile` action specifically; no agent process was attached to the caller in the tested `setsid` env-replay context (the captured env had no `PA_SESSION_ID`), which is why the tested check returned not-authorized.
- No-op confirmation (should-fix 3): `sed -n '875,895p'` of the canonical checkout `cs_power.py` → `:891` `active_profile = self.proxy.Get('(ss)', self.dbus_name, "ActiveProfile")` (succeeds), `:892` `self.content_widget.set_active_iter(self.option_map[active_profile])` (sets the combo, firing `changed`), and `:878-883` `on_my_value_changed` where `:883` `self.proxy.Set('(ssv)', self.dbus_name, "ActiveProfile", value)` writes back `value` = the combo's current profile = the just-read `active_profile`. So the startup `:883` `Set` is a no-op (writes back the value read at `:891`), and the combo is set at `:892` before the failing `Set`.

**Fixes applied (this section).**
- Finding 1 (user-click path / intake Unknown line 34): the click case is now flagged as INFERRED-not-tested in item 4 (the same `on_my_value_changed` → `:883` → interactive check; the live-desktop outcome is inferred from `polkit.py:24` `flags=1` plus the running `gnome-keyring-daemon` agent, not live-tested under no-render), and intake Unknown line 34 is resolved: display intact (no-op, combo set at `:892` before the failing `:883` `Set`), profile switching auth-gated by design (the service's interactive polkit check; a live-desktop click prompts and succeeds with the password, a non-agent context fires the `:883` traceback). See the Alternative entry above for why a live click test was not run.
- Finding 2 (misattribution, corroborated by Omega medium/authz): the item 2 polkit bullet and the root-cause statement now restate that `allow_active=yes` is permissive and the denial is the unsatisfied interactive check in a non-agent context, citing `tuned/utils/polkit.py:24` `flags=1`.
- Finding 3 (no-op framing): the root-cause statement now states the `:883` startup `Set` is a no-op (writes back the `:891` read), the combo is set at `:892` before it, and the displayed value is correct.
- Nit 4 (full path): the service-code bullet and root-cause statement now cite the full guest path `/usr/lib/python3.12/site-packages/tuned/exports/dbus_exporter_with_properties.py:49` plus the owning package `tuned-2.27.0-2.el10_2`.
- Nit 5 (PPD comparison): recorded below as an explicit note for `Vector`.

**Note for `Vector` (upstream report; Shadow nit 5, out-of-scope evidence).** The (b) classification and root cause are established for THIS environment (base-OS `tuned-ppd`, polkit-gated, interactive check). Whether upstream Mint's default service (`power-profiles-daemon`, not installed here) exhibits the same `:883` traceback is NOT verified by this task and is the missing piece for the report's framing: it decides whether the issue is (i) a Cinnamon bug reproducing against Cinnamon's own default service (PPD) or (ii) a Cinnamon-meets-tuned-ppd integration issue. Settling it requires a scratch VM with `power-profiles-daemon` installed, repeating the single Power-pane launch, and observing whether the `:883` traceback fires. That comparison is OUT OF SCOPE for this diagnostic task (it is a second environment, not the one under diagnosis); record it as the report's open framing question, not a defect of this task.

**Checks run (this pass):** no compile (no source change); no linter (n/a); read-only source reads over SSH (`tuned/utils/polkit.py`, `tuned/exports/dbus_exporter*.py`, `cs_power.py:875-895`) plus `rpm -qf` / `rpm -ql` / `rpm -qa` / `pgrep` identity and agent checks (polkit agent `gnome-keyring-daemon` present and running); no launches, no state change (no VM disturbance; the /tmp artifacts from items 1-3 are unchanged).

**Changes**

| File | What changed |
|---|---|
| `planning/docs/TASK-0035-cinnamon-power-pane-dbus-unauthorized.md` (`## Implementation`) | items 1-4 recorded: Rocky reproduction (2 launches), Rocky root cause (wire error, rejecting file:line, policy/polkit/unit evidence, SELinux due diligence), Fedora reproduction (1 launch), classification plus fix-path decision; no other agent section touched |
| `planning/docs/TASK-0035-cinnamon-power-pane-dbus-unauthorized.md` (`## Implementation`) — fix round | Shadow findings 1-5 fixed in place: polkit misattribution restated (`allow_active=yes` permissive; the denial is the unsatisfied interactive check in a non-agent context, `tuned/utils/polkit.py:24` `flags=1`), no-op framing added (the `:883` startup `Set` writes back the `:891` read; combo set at `:892` before it; displayed value correct), full guest path plus owning package `tuned-2.27.0-2.el10_2` added to the `dbus_exporter_with_properties.py:49` citation, user-click case flagged inferred-not-tested plus intake Unknown line 34 resolved, PPD-comparison note recorded for `Vector`; new evidence: `polkit.py` `flags=1` read, polkit agent (`gnome-keyring-daemon`) presence, no-op source read; no other agent section touched |
| guest `Rocky_Linux_10_Cinnamon`: `/tmp/tails-t0035-rocky-power{,2}.{log,pid}`, `/tmp/tails-set{,2}.{out,err}` | launch artifacts (pane log, pidfile) and raw Set reproduction captures, guest-local only, not in any repo |
| guest `Fedora_45_Cinnamon`: `/tmp/tails-t0035-fedora-power.{log,pid}` | same, guest-local only |

**Checks run:** no compile (no source change this pass; item 5 skipped per item 4) · no linter (n/a) · harness: 3 valid controlled launches all reproducing (Rocky pids 36616, 37485; Fedora pid 23732; each killed by its recorded pid) + 1 recorded invalid Fedora attempt (env-less, GTK abort, pid 23496) + raw wire `Properties.Set` on both object paths (FAIL, exit 1, exact error name plus message) + 2 control `Properties.Get` (PASS) + 1 python-gi replay of the exact app call (decomposes the ` (36)`) + journal/audit/ppd-log window checks (journal: only the SSH session scope lines in the run-1 window; audit: unreadable without root; ppd log: one `wasn't authorized` line per denied call including the 2026-10-08 gate line) · fix round (2026-10-13): read-only source reads over SSH (`tuned/utils/polkit.py` `flags=1`, `tuned/exports/dbus_exporter*.py`, `cs_power.py:875-895`) plus `rpm -qf` / `rpm -ql` / `rpm -qa` / `pgrep` identity and agent checks (polkit agent `gnome-keyring-daemon` present and running); no launches, no state change.

---

## Review

*Owner: `Shadow`. Read-only — findings only, no edits. Severity order, blockers first.*

No blockers. The evidence chain is sound and the (b) classification is well-supported under the DoD framing: wire-level `dbus-send` reproduction with the exact error name, the python-gi replay byte-identical to the app line (decomposing the ` (36)`), the service-log denial lines including the 2026-10-08 gate line, the daemon-policy read that exonerates dbus-daemon, the polkit action file, the SELinux due diligence, and the three-way `cs_power.py` md5 (both VMs plus canonical checkout). The `Alternatives considered` entries (env-capture failure, gdbus-vs-dbus-send choice) are a strength. Findings below are completeness and precision, severity order.

### User-click traceback is inferred, not tested; intake Unknown (line 34) left open
**Severity:** should-fix
**Where:** `planning/docs/TASK-0035-cinnamon-power-pane-dbus-unauthorized.md:294` (item 4) and `:34` (intake Unknown)
**Problem:** The item 4 claim "any non-root session raises the traceback" is verified only for the startup self-trigger; the user-initiated profile switch (the same `on_my_value_changed` → `cs_power.py:883` `Set`) is inferred, not tested, and not flagged as such, and intake Unknown line 34 ("Whether Power pane functionality is degraded despite the process surviving") is neither resolved nor closed.
**Failure scenario:** If the click's polkit check is interactive (agent attached, `allow_active=yes`), the click shows an auth dialog and the switch succeeds with the password (no traceback), so the pane is functionally intact and line 294 overstates severity; if it is non-interactive (like the tested startup denial), the click fires the same `:883` traceback and the user cannot switch profiles at all. The upstream report (Vector) cannot set severity until this is known.
**Suggested direction:** Test one user-initiated profile switch on `Rocky_Linux_10_Cinnamon` (click a profile; record whether a polkit auth dialog appears, whether the switch succeeds with the password, and whether the `:883` traceback fires); or, if out of scope, explicitly close intake Unknown line 34 as N/A with the reasoning and flag line 294's click case as inferred-not-tested.
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

### Polkit denial sentence misattributes the denial to `allow_active=yes`, which is permissive, not restrictive
**Severity:** should-fix
**Where:** `planning/docs/TASK-0035-cinnamon-power-pane-dbus-unauthorized.md:272` (item 2, polkit bullet) and `:276` (root-cause statement, same sentence)
**Problem:** "the action's `allow_active=yes` requires interactive authentication, so any non-root caller is denied" attributes the denial to `allow_active=yes`; but `allow_active=yes` is permissive (it is what *allows* an active-session user to be authorized via interactive auth) — the denial occurs because the startup `Set`'s polkit check is non-interactive and returns not-authorized without prompting.
**Failure scenario:** A security reviewer (Omega, next in the chain) or a fix author reading the sentence in isolation concludes the polkit *action* is the defect and the fix is to change the action (e.g. drop the auth requirement) — a security-weakening change; the correct fix (item 5) is in Cinnamon code, not polkit policy, and item 5 correctly rejects the policy change, but the intermediate sentence in both locations points the wrong way.
**Suggested direction:** Restate at both locations as: the startup `Set`'s polkit check is non-interactive and returns not-authorized for the non-root caller (no prompt shown); `allow_active=yes` is why an interactively-authenticated caller or root would pass.
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

### The `:883` Set is a redundant no-op; the no-op framing (and display-intact consequence) is implied but not stated
**Severity:** should-fix
**Where:** `planning/docs/TASK-0035-cinnamon-power-pane-dbus-unauthorized.md:276` (root-cause statement) and `:294` (item 4)
**Problem:** The root cause documents the self-trigger chain (`:892 set_active_iter` → `:869 changed` → `:878-883 on_my_value_changed` → `:883 Set`) but does not state that the `Set` writes the profile back to the value just read at `:891` (balanced → balanced), i.e. a no-op, and does not state that the combo is set correctly before the failing `Set`.
**Failure scenario:** A new reader of the root-cause statement concludes the pane is attempting a real profile change at startup and failing; the fix for a real change attempt (authenticate at startup) differs from the fix for a no-op (suppress the self-trigger, which item 5 already recommends). The no-op framing is also what makes the startup failure cosmetic (display already correct), which is the severity basis.
**Suggested direction:** Add one sentence to the root-cause statement / item 4: the `:883` `Set` writes the current profile back (no-op), the combo is set at `:892` before the failing `Set`, so the displayed profile is correct and the startup traceback has no effect on the displayed value.
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

### Service-code file:line citation lacks a full guest path or RPM/source ref
**Severity:** nit
**Where:** `planning/docs/TASK-0035-cinnamon-power-pane-dbus-unauthorized.md:271` (item 2, service-code bullet)
**Problem:** The rejecting line is cited as `tuned/exports/dbus_exporter_with_properties.py:49` without the full guest path or the tuned-ppd RPM/source ref, so a new reader cannot open the cited line directly.
**Failure scenario:** A new reader (or a future re-verification) cannot locate the cited line without first finding where tuned-ppd installs its python tree; the empirical evidence (wire error plus service log) still corroborates the mechanism, so this is citability, not validity.
**Suggested direction:** Add the full guest path (or the tuned-ppd package plus source ref) next to the file:line.
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

### Complete for this environment; the upstream report needs a PPD comparison this task does not provide
**Severity:** nit
**Where:** `planning/docs/TASK-0035-cinnamon-power-pane-dbus-unauthorized.md:292` (item 4, classification) and `:296` (item 5)
**Problem:** The (b) classification and reasoning correctly identify tuned-ppd plus polkit gate for this environment, but do not verify (or record as a hypothesis) whether upstream Mint's default service (power-profiles-daemon, not installed here) exhibits the same traceback; scope note, not a defect — the label is the DoD's bucket-(b) wording and the reasoning is precise.
**Failure scenario:** The upstream report (Vector, downstream) cannot frame the issue as either (i) a Cinnamon bug reproducing against Cinnamon's own default service (PPD) or (ii) a Cinnamon-meets-tuned-ppd integration issue; the framing (and where the fix belongs) depends on the PPD comparison, which this task does not provide.
**Suggested direction:** Record as an explicit note for Vector: the PPD comparison (install PPD in a scratch VM, repeat the launch, observe whether the `:883` traceback fires) would settle the upstream report's framing and is out of scope for this diagnostic task.
**Resolution:** *(filled by `Tails`)* fixed in `<sha>` | disputed, because

### 2026-10-13: re-run after the Tails fix round

Verdict: clean. All five items are resolved in ## Implementation (the fix round entry, line 309). No code change (classification (b) stands); the fixes are to the diagnostic record, verified in place:

- **Finding 1 (user-click path / intake Unknown, should-fix): resolved.** The click case is flagged INFERRED-not-tested in item 4 (line 305). The mechanism my failure scenario left open is now settled from source, not left to inference: `tuned/utils/polkit.py:24` `flags = 1` (`POLKIT_CHECK_AUTHORIZATION_FLAGS_ALLOW_USER_INTERACTION`, the read at line 314) makes the check interactive-capable, so a live desktop with a polkit agent attached to the caller's session prompts and authorizes on the password (no traceback), while a non-agent context (the tested `setsid` env replay, no `PA_SESSION_ID`, line 316) returns not-authorized and fires the `:883` traceback. Both branches of the original failure scenario are covered, with the determining condition named. Intake Unknown line 34 is resolved (display intact, profile switching auth-gated by design), not left open. The live outcome is honestly bounded: `gnome-keyring-daemon` pid 2873 is installed and running (line 316), and no-render prevents confirming which agent, if any, is attached to session 2 for the action (lines 253 and 256); the rejected live-click option is recorded with the reason (line 253).
- **Finding 2 (allow_active misattribution, should-fix): resolved in both places.** The polkit bullet (line 283) and the root-cause statement (line 287) now state `allow_active=yes` is the permissive clause and attribute the denial to the unsatisfied interactive check in a non-agent context, citing `polkit.py:24`. Record note: the fix's mechanism wording supersedes the original direction's "non-interactive" phrasing. The check is interactive-capable (`flags = 1`); the no-prompt in the tested contexts is the absent agent, not a non-interactive flag. The substantive correction asked for (no polkit-action misdirection, the security-weakening fix path gone) is in place, and item 5's rejection of the guest-side polkit knob stands (line 307).
- **Finding 3 (no-op framing, should-fix): resolved.** The root-cause statement (line 287) now states the `:883` startup `Set` is a no-op (writes back the value read at `:891`, the combo is set at `:892` before the failing `Set`, the displayed value is correct and the traceback has no effect on it), with the source read as evidence (line 317). Item 4 carries the same framing (line 305).
- **Nit 4 (citation path): resolved.** The service-code bullet (line 282) and the root-cause statement (line 287) cite the full guest path `/usr/lib/python3.12/site-packages/tuned/exports/dbus_exporter_with_properties.py:49` plus the owning package `tuned-2.27.0-2.el10_2`; the `rpm -qf` / `rpm -ql` evidence (line 315) confirms the python tree is owned by `tuned`, not `tuned-ppd`.
- **Nit 5 (PPD comparison): resolved.** The explicit note for Vector (line 326) records the unverified PPD comparison (scratch VM, `power-profiles-daemon` installed, repeat the single Power-pane launch, observe whether the `:883` traceback fires) as the upstream report's open framing question, out of scope for this diagnostic task.

No new findings. The fix round's new evidence is internally consistent with item 2's wire and service-log evidence: the `flags = 1` read (line 314), the agent check (line 316), and the no-op source read (line 317) all agree with the wire error name and the `wasn't authorized` denial lines, and the pass stayed read-only with no VM state change (line 328). Handoff note: the per-finding Resolution placeholders above remain unfilled (`Tails` to fill per the template). Next in the re-run chain is Omega.

---

## Security

*Owner: `Omega`. Read-only. Severity order.*

Diagnostic task, no code change, no new artifact. Findings: one secrets exposure verified live (it subsumes the plan's two standing secrets risk rows, lines 192 and 193; the line-192 PAT row is resolved in the other direction), one authz finding on the fix direction the doc's polkit sentence implies. The rest is checked clean.

### `~/AI/secrets/` is world-readable: directory 755, all five files 644, holding a GitHub token, the VM password, and the AI-machine password
**Severity:** high
**Vector:** secrets
**Where:** `~/AI/secrets/` (`pass.txt`, `githubtoken.md`, `token.md`, `ai-machine-password.md`, `temp_pass.md`); plan risk rows `planning/docs/TASK-0035-cinnamon-power-pane-dbus-unauthorized.md:192` and `:193`; AGENTS.md section 4 (600/700 requirement)
**Attack:** Any host-local process running as a uid other than `howard` (a container, a service, a second local account, a future CI job under another user; or any `howard`-level compromise that specifically targets credentials) reads the world-readable files and obtains: the GitHub token(s) in `githubtoken.md`/`token.md` (41 B each, scope unverified, content not read), the `howard` password for both VMs (`pass.txt`), the AI-machine password (`ai-machine-password.md`), and whatever `temp_pass.md` still holds (live or stale: unverified).
**Impact:** The GitHub token unlocks the `metalllinux` account at its scope (the plan's own line-192 row rates this class "High if leaked"); `pass.txt` unlocks user login on `Rocky_Linux_10_Cinnamon` (192.168.122.4) and `Fedora_45_Cinnamon` (192.168.122.176) and is the same value as the operator's live Rocky desktop session (intake `:21`); `ai-machine-password.md` unlocks the model host. Exploitability today is bounded: the host is single-user, so the current reader set is {howard, root} and `howard` already owns all of these; the exposure is the AGENTS.md section 4 hard requirement plus any future non-`howard` uid on this host.
**Verification (this pass):** `stat -c '%a %U %s %n'` on the directory and files plus `ls -la ~/AI/secrets/` (names only; no file content read): directory `755 howard`, all five files `644 howard` (9/41/41/41/9 B); the compliant store `~/secrets/` exists at `700`, so two secret stores exist and only one meets section 4. The plan's line-192 row (PAT in the `cinnamon/` checkout origin URL) is resolved: `git -C ~/Linux/projects/cinnamon-for-rocky10/cinnamon config --get remote.origin.url` returns plain `https://github.com/linuxmint/cinnamon.git`, no repo-level `credential.helper` is set, and `~/.git-credentials` is mode `600` — the token is no longer in `.git/config`.
**Fix:** Operator step: `chmod 700 ~/AI/secrets` plus `chmod 600` on each file, or consolidate into `~/secrets/` (already 700) per section 4; check whether `temp_pass.md` is still live and delete it if not. This task's own handling of `pass.txt` is clean: `sshpass -f` (password read from the file into sshpass memory, not argv, so it does not appear in `ps`), no `set -x` near the credential, no `echo` of the value, no write of it to any file; the doc references the path, never the value.
**Resolution:** *(filled by `Tails`)*

### The doc's polkit sentence points at the gate as the defect; the fix it implies (guest polkit policy edit) is a security weakening and is not the fix
**Severity:** medium
**Vector:** authz
**Where:** `planning/docs/TASK-0035-cinnamon-power-pane-dbus-unauthorized.md:272` (item 2 polkit bullet) and `:276` (root-cause statement); Shadow's finding #2 in `## Review` names the same misattribution
**Attack:** A fix author (Tails in a later dispatch, or any downstream agent) reads `:272` in isolation — "the action's `allow_active=yes` requires interactive authentication, so a non-root session user is never authorized without an auth dialog" — concludes the polkit action file is the defect, and edits `/usr/share/polkit-1/actions/net.hadess.PowerProfiles.policy` on the guest (drops the auth requirement or sets `allow_any=yes`) to silence the traceback.
**Impact:** The polkit interactive-auth gate on `net.hadess.PowerProfiles.switch-profile` is removed or weakened: any local user, and any D-Bus client, can switch power profiles without authentication; the upstream Cinnamon defect (unguarded `Set` at `:883`, no try/except) is masked, not fixed, and resurfaces whenever guest policy is reset. Bounded to the guest (test infrastructure), but it degrades the one effective authz control on a service reachable from the whole system bus and sets the precedent of editing base-OS security policy to silence an app traceback.
**Fix:** Do not touch guest polkit policy. The effective control is the in-service polkit gate in `tuned-ppd`, and it is working, per this task's own evidence: the raw `Properties.Set` as `howard` was denied on the wire (`Unauthorized`), the service log records `wasn't authorized` per denied call, and `allow_active=yes` is the *permissive* clause (it is what lets an interactively-authenticated caller pass), not the restrictor — the denial happens because the startup check is non-interactive (no agent attached), per Shadow's finding #2. The only sanctioned fix location is upstream Cinnamon code (item 4 fix path: suppress the startup self-trigger, or guard `:883`), consistent with the guest fix being N/A.
**Resolution:** *(filled by `Tails`)*

Checked, no finding:
- Injection. No new shell, eval, template, or SQL surface. The recorded launches are fixed-argument `setsid env ...` commands with env captured from a user-owned `/proc/<pid>/environ` (an attacker would need to be a local user on the VM to influence the environ; no such path exists); the `dbus-send`/`gdbus` reproductions use fixed strings; no `set -x` in the recorded commands.
- D-Bus daemon policy. The broad `send_interface="org.freedesktop.DBus.Properties"` grant in `/usr/share/dbus-1/system.d/net.hadess.PowerProfiles.conf` is by design for the PPD/tuned-ppd model (all users may send; the service gates); the gate's enforcement is demonstrated live by this task's denials, so no finding. Editing that policy file is exactly the weakening to avoid (see the polkit finding above).
- Actions/CI. No workflow change, no new action, no runner exposure; no CI involved.
- Supply chain. No new dependency pulled; `tuned-ppd` is base-OS, unchanged by this task.
- License. No new imported file (no code change), no license signal; verdict belongs to `## License (Charmy)`.
- Guest /tmp artifacts (`/tmp/tails-t0035-*.{log,pid}`, `/tmp/tails-set{,2}.{out,err}` on both VMs). Full content not verified (no guest session this pass); the doc's env var list contains no credentials and the files are app stderr plus D-Bus error captures. Recorded as unverified, not as a finding.
- The diagnosis introduced no new attack surface: three valid controlled launches, each killed by its recorded pid, all probes read-only, no state change beyond the guest /tmp artifacts (Changes table).

### 2026-10-13: re-run after the Tails fix round

Verdict: clean. The medium/authz finding is resolved against the corrected `## Implementation` text; no remaining findings from this re-run. Carried, not re-opened: the high/secrets finding (`~/AI/secrets/` world-readable) is operator-owned (the standing TASK-0033 step-stop); the fix round did not address it and it is unchanged.

Re-verified by reading the corrected text (no new commands this pass; no code change, classification (b) stands):

- The misdirecting sentence is gone from both cited locations (the text moved to the polkit bullet at `planning/docs/TASK-0035-cinnamon-power-pane-dbus-unauthorized.md:284` and the root-cause statement at `:288`). Both now state `allow_active=yes` is the permissive clause ("not the restrictor") and attribute the denial to the unsatisfied interactive check in a non-agent context (`setsid` env-replay, no `PA_SESSION_ID`, no agent attached), citing `tuned/utils/polkit.py:24` `flags = 1`. A fix author reading either location in isolation now sees a working gate (non-root, no-agent callers denied), not a defective action file.
- The security-weakening fix direction is still not sanctioned: the fix-path decision (`:308`) rejects the guest-side knob ("No in-guest knob changes the polkit design without masking the upstream behavior") and names upstream Cinnamon code as the only fix location (suppress the startup self-trigger, or guard `:883`). The recorded attack path — a fix author editing `/usr/share/polkit-1/actions/net.hadess.PowerProfiles.policy` to drop the auth requirement — has no supporting text left in the doc.
- The corrected technical claim is accurate against polkit semantics (`ALLOW_USER_INTERACTION` prompts only with an attached agent; otherwise returns not-authorized without prompting), consistent with the tested non-agent denials (the wire error name plus the one `wasn't authorized` service-log line per denied call).
- No new surface from the fix round: read-only source reads over SSH plus `rpm` / `pgrep` identity and agent checks; no launches, no state change, no new artifacts (fix-round checks run at `:329`); the recorded env var lists contain no credentials.

---

## License (Charmy)

*Owner: `Charmy`. Fourth in the review chain. Every license is verified at the upstream source
repository and the ref used, never from a copy in this repo.*

**Project license:** GPL-2.0 — appropriate

- Declared: project root `~/Linux/projects/cinnamon-for-rocky10` (remote `metalllinux/cinnamon-for-rocky10`) has a root `LICENSE` (18,092 B, the standard FSF GPL-2.0 text; tracked, `git log -1 -- LICENSE` = `8c96d5d`) plus per-package `License:` fields in `spec/*.spec`. The package that ships the file under review, `spec/cinnamon.spec` (`cinnamon` 6.7.4-4.el10), declares `License: GPLv2+` and ships the text (`%license COPYING` at `spec/cinnamon.spec:110`).
- Upstream match: `linuxmint/cinnamon` @ `e9ba28a87f0f69594487a08e940840d494bb3ea0` (the checkout's `origin/master`, 2026-08-10, "Fix typo in System Administration Keyword Filters (#13781)"): `COPYING` at that ref is the full GNU GPL Version 2 text (verified by fetching `COPYING` at that exact ref from `raw.githubusercontent.com`; the local checkout HEAD `61695c722d01dcd64f17701a559a895e2810bb2b` is one commit ahead and touches only `cs_calendar.py` per `git show --stat`, dated 2026-10-07, pre-dating this task, so for `cs_power.py` and `COPYING` the in-use revision's content equals upstream at that ref). Local `cinnamon/COPYING` (17,991 B) is the same GPL-2.0 text (byte difference vs the root `LICENSE` is the FSF address revision; both GPL-2.0).
- Appropriateness: the project is a Cinnamon port and each component keeps its upstream license (the `spec/` `License:` fields match the upstream `COPYING`); GPL-2.0 code remains GPL-2.0 and nothing here was re-licensed. The file under review is unmodified upstream code (three-way md5 in `## Implementation`), so this task cannot change any licensing.

**Imported code**

| Component | Source (repo @ ref) | License (verified at) | Obligations met | Status |
|---|---|---|---|---|
| None in this task | — | — | — | pass |
| Standing, file under review: `cinnamon/files/usr/share/cinnamon/cinnamon-settings/modules/cs_power.py` | `linuxmint/cinnamon` @ `e9ba28a87f0f69594487a08e940840d494bb3ea0` (`origin/master`; HEAD `61695c7` differs only in `cs_calendar.py`) | GPL-2.0, verified at upstream `COPYING` at that ref (full GPL-2.0 text) | yes: file byte-identical to upstream (md5 `ab9499015f1484b20add77d54385660d` three-way, both VMs plus checkout; `git diff origin/master` on the file empty); no per-file copyright header upstream either (grep `copyright|license|GPL` on the file empty), so nothing was lost; license text present (`cinnamon/COPYING`) and declared (`spec/cinnamon.spec` `License: GPLv2+`, `%license COPYING` at `:110`) | pass |

Evidence checked that this task imported nothing:
- `## Implementation` Changes table: only the planning doc plus guest-local `/tmp` artifacts, each marked "not in any repo".
- No source change: plan item 5 (the only step that can change code) was skipped per item 4; `## Test Results` spot check has `git status --porcelain` on `cs_power.py` empty; the checkout's 8 dirty entries are the pre-existing port files (A2) and none mentions `cs_power` (checked this pass: `git -C <checkout> status --porcelain | grep -c cs_power` = 0).
- No new dependency: `tuned-ppd` is a base-OS package on both VMs, unchanged by this task (`## Security` supply-chain line); it is a guest service, not code this project imports or distributes, so it is not a row.
- No packaging change: no `spec/` file touched (Changes table); root-repo HEAD `9edabed` (2026-10-13) is the TASK-0026/TASK-0027 docs commit, not this task.

Out-of-domain observation (security, not license; recorded here because `## Security` has already run; no credential value written here):
the project root repo's origin URL in local `.git/config` (`~/Linux/projects/cinnamon-for-rocky10/.git/config`, remote `origin` pointing at `github.com/metalllinux/cinnamon-for-rocky10`) embeds a live PAT in the URL userinfo. It is not committed and cannot be committed (`.git/` is untracked), but it is a credential in a local file outside `~/secrets/`. Distinct instance from the `cinnamon/` subrepo URL Omega verified plain (different repo, different remote). For Omega/operator action; not a license finding; the verdict below is unaffected.

**Verdict:** pass — no license work in this task (no new imports, no packaging change, no license change; classification (b) upstream behavior per `## Test Results`). The standing licensing posture of the file under review is verified at upstream at the ref in use. No Tails fix on license.

### 2026-10-13: re-run after the Tails fix round

Verdict: clean. The fix round is license-neutral: no code change, no new imports, no packaging or license change. No remaining license findings.

Re-verified against the post-fix `## Implementation` (fix round entry, `planning/docs/TASK-0035-cinnamon-power-pane-dbus-unauthorized.md:312`):

- **No code change.** The fix round's Changes rows are this planning doc (`:338`) plus the guest `/tmp` artifact rows from items 1-3, each marked "guest-local only, not in any repo" (`:339-:340`). No source file, no `spec/` file, no `COPYING`/`LICENSE` touched; the entry's own Checks-run line states no compile, no source change, no launches, no state change (`:331`).
- **No new imports.** The fix round's new evidence is read-only observation of base-OS packages already on the guests: `tuned-2.27.0-2.el10_2` (`polkit.py`, `dbus_exporter*.py`; identity via `rpm -qf`/`rpm -ql`), `gnome-keyring`/`polkit` presence (`rpm -qa`, `pgrep`). Nothing was copied into the project. The short line-level excerpts in the record (`polkit.py:24`, `dbus_exporter_with_properties.py:49`, `cs_power.py:875-895`) are diagnostic citations in this private planning doc, not redistributed code.
- **In-use ref unchanged, so the standing row's upstream verification still applies.** Re-run this pass (read-only): canonical checkout `git rev-parse --short HEAD` = `61695c7` (shallow clone, one ahead of `origin/master` `e9ba28a87f0f69594487a08e940840d494bb3ea0`), `git status --porcelain` on `cs_power.py` empty, `md5sum` = `ab9499015f1484b20add77d54385660d` (matches the three-way chain; agrees with Big's re-run spot check in `## Test Results`). A git ref's content is immutable, so the earlier upstream verification (`linuxmint/cinnamon` @ `e9ba28a`, `COPYING` fetched at that exact ref from `raw.githubusercontent.com` = full GPL-2.0 text) remains the verification for the file under review; no re-fetch needed.
- **Project license unchanged.** Re-run this pass: root repo (`metallinux/cinnamon-for-rocky10`) `git log -1` = `9edabed` (the TASK-0026/TASK-0027 docs commit, not this task), `git status --porcelain` has no entry touching `LICENSE`/`COPYING`/`spec/`/`cs_power`, root `LICENSE` present at 18,092 B. The GPL-2.0 declaration and the `spec/` `License:` fields are untouched.
- The standing imported-code row above (`cs_power.py` @ `e9ba28a`, GPL-2.0) therefore remains pass. The out-of-domain PAT observation stands as recorded (security, not license; distinct instance from the `cinnamon/` subrepo URL).

**Verdict (re-run):** clean. No license work to re-run, no findings for `Tails`. The pass verdict above stands against the post-fix `## Implementation`.

---

## Test Results

*Owner: `Big`. Verdicts, never raw log dumps.*

**Workflow run:** none. No CI in this task: it is a diagnosis (no source change, no workflow, no
published artifact). Verification ran on the two VMs as controlled process-level launches plus raw
D-Bus wire reproductions per plan items 1-4 (evidence in `## Implementation`), plus Big's
host-side independent spot checks (2026-10-13, read-only, no VM disturbance): `md5sum` of the
canonical checkout `cinnamon/files/usr/share/cinnamon/cinnamon-settings/modules/cs_power.py`
= `ab9499015f1484b20add77d54385660d` (matches the three-way chain in `## Implementation` items 2-3);
`sed -n '878,895p'` of that file confirms line 883 is `self.proxy.Set('(ssv)', self.dbus_name,
"ActiveProfile", value)` in `on_my_value_changed` (the recorded traceback site; also corroborates
the doc's line refs: `:891` `Get`, `:892` `set_active_iter`, `:889-895` sibling try/except);
`git status --porcelain` on the file is empty (not a dirty port file, per A2; the dirty files are
the pre-existing port files).

| Check | What it exercises | Result | Notes |
|---|---|---|---|
| Rocky controlled reproduction (item 1) | Power-pane startup D-Bus call on the Rocky guest; traceback site; matched dbus_name | PASS (reproduces) | 2 controlled launches, identical traceback at `cs_power.py:883 on_my_value_changed` with `Unauthorized (36)`, matched name `net.hadess.PowerProfiles`; pids 36616, 37485, each killed by recorded pid; old gate log state recorded (neither the `Found` line nor the traceback in current content) |
| Rocky root cause (item 2) | exact D-Bus error on the wire; rejecting component with file:line; exoneration of the other layers | PASS | raw `Properties.Set` via `dbus-send` on both object paths reproduces (exit 1): error name `org.freedesktop.DBus.Python.dbus.exceptions.DBusException`, message `Unauthorized`; control `Properties.Get` (`Profiles`, `ActiveProfile`) PASS; python-gi replay of the exact app call byte-identical to the app traceback line (decomposes the ` (36)`); rejecting component is the in-service polkit gate in `tuned-ppd` at `tuned/exports/dbus_exporter_with_properties.py:49`; dbus-daemon policy grants the send (exonerated); SELinux excluded |
| Fedora reproduction (item 3) | reproduction on the second VM; cross-VM file identity | PASS (reproduces) | 1 controlled launch (pid 23732, kill confirmed), identical traceback; answering service `tuned-ppd` (`2.27.0-3.fc45`); three-way `cs_power.py` md5 `ab9499015f1484b20add77d54385660d` (both VMs plus canonical checkout; checkout side re-verified by Big); the invalid env-less attempt (GTK abort, pid 23496) is recorded and excluded |
| Classification plus fix decision (item 4) | exactly one DoD classification box with evidence | PASS | (b) upstream Cinnamon behavior; fix N/A in this environment; item 5 skipped per the plan conditional; what would settle it is recorded (upstream fix) |
| Fix plus clean re-run (item 5) | in-environment fix plus process-level clean launch | N/A | skipped: no port-introduced defect (classification (b)); the plan's expected path (A5); conditional branch not taken, stated here explicitly, not silently dropped |
| Final verdict (item 6) | all DoD boxes verifiable from the doc; checks requested vs run; 2026-10-08 12-pane gate recorded as reference | PASS | this entry |
| compile | changed files | N/A | no source change this task (item 5 skipped; checkout file clean, re-verified by Big) |
| linter | style and correctness | N/A | no source change |
| unit tests | individual functions | N/A | no source change; no code artifact in this task |
| integration tests | end-to-end flows | N/A | no code artifact to test; the end-to-end pane flow (launch → probe → `Get` → self-trigger → `Set` → `Unauthorized` → traceback, process survives) is exercised by rows 1 and 3, each meeting its acceptance criterion |
| Sparky tests | Rocky Linux UI (if applicable) | N/A | no-render limitation (A7): UI-level and screenshot-level verification impossible; DoD scoped to process level; re-verification deferred until the no-render state is resolved (TASK-0026/TASK-0034) |

**Checks requested vs run:** 6 requested (plan Validation (1)-(6)); 5 executed, 1 N/A. (5) is N/A
because item 5 (the conditional fix) did not run; the plan's expected path per A5, stated here
explicitly. House-standard rows: 5 of 5 N/A, each with reason above (no source change; no-render).

**Verdict:** PASS — the diagnostic task meets every DoD box; zero FAILs. There is no in-scope code
change to fix (classification (b)), so nothing goes to `Tails` as a code bug, and no harness bug
occurred (all checks ran as recorded).

DoD boxes:
1. **Root cause — established** (item 2). `cs_power.py:883` (Big-verified: line 883 is the
   `proxy.Set` call) sends `Properties.Set` with `(net.hadess.PowerProfiles, "ActiveProfile",
   variant string)` on the system bus. The answering service is base-OS `tuned-ppd` (owns both
   candidate names; `power-profiles-daemon` not installed). The dbus-daemon policy grants the send
   (a daemon denial would be `AccessDenied`; exonerated). The in-service polkit gate (action
   `net.hadess.PowerProfiles.switch-profile`, `allow_active=yes`, interactive authentication
   required) denies the non-interactive startup check; the wrapper raises
   `DBusException("Unauthorized")` at `tuned/exports/dbus_exporter_with_properties.py:49`; the
   wire name is the Python exception class (`org.freedesktop.DBus.Python.dbus.exceptions.DBusException`,
   message `Unauthorized`); python-gi appends GDBusError code 36 to render `Unauthorized (36)`;
   `:883` has no try/except (its sibling `:889-895` does), so the startup self-trigger raises the
   traceback.
2. **Reproduction — reproduces on both VMs.** Rocky (item 1, Wayland, 2 controlled launches) and
   Fedora (item 3, X11, 1 controlled launch): identical traceback, identical wire error,
   `tuned-ppd` answering on both (`2.27.0-2.el10_2` / `2.27.0-3.fc45`). Three-way `cs_power.py`
   md5 `ab9499015f1484b20add77d54385660d` (both VMs plus canonical checkout; checkout side
   re-verified by Big).
3. **Classification — (b) upstream Cinnamon behavior** (item 4). Box (a) port bug excluded: file
   md5-identical to the canonical checkout, not a dirty port file, port packages neither PPD nor
   upower. Box (c) environment excluded: reproduces identically on Fedora; no Rocky-specific
   setting is involved.
4. **Fix — N/A in this environment.** DoD box 4 is conditional ("If fixable in this environment");
   no port-introduced defect exists, so item 5 correctly did not run. The fix belongs upstream in
   `linuxmint/cinnamon` (suppress the startup self-trigger, or guard `:883`); an upstream report
   is an external step-stop (AGENTS.md section 8: `Vector` drafts, operator decides).
5. **Test Results** — this entry.

Open items carried forward (none is a FAIL of this task's DoD; none is a harness bug; all bear on
the diagnostic record):
- **Owner `Tails`, before `Vector`'s upstream report** — Shadow should-fix #1: the user-click path
  is untested. Item 4's "any non-root session raises the traceback" is verified only for the
  startup self-trigger; the user-initiated profile switch (the same `:883`) is inferred, and
  intake Unknown (line 34, pane functionality degraded?) is left open. Under no-render,
  UI-level click testing is impossible (an interactive polkit dialog needs a live display plus
  agent). The residual uncertainty bounds the upstream report's severity framing (pane functionally
  intact if the click's check is interactive; user cannot switch profiles if it is non-interactive),
  not this task's DoD.
- **Owner `Tails`** — Shadow should-fix #2, corroborated by Omega medium/authz: the polkit
  sentence in item 2 and in the root-cause statement misattributes the denial to
  `allow_active=yes` (permissive); the denial is the non-interactive startup check. Must be
  corrected before `Vector` drafts: the misreading points at the polkit action as the defect, and
  a fix following it (guest policy edit) would be a security weakening per Omega.
- **Owner `Tails`** — Shadow should-fix #3: state that the `:883` `Set` is a no-op (writes back the
  profile just read at `:891`) and that the combo is set at `:892` before the failing `Set`, so
  the displayed value is correct.
- **Owner `Tails`** — Shadow nit #4: add the full guest path to the
  `dbus_exporter_with_properties.py:49` citation.
- **Owner `Vector` (note, out-of-scope evidence)** — Shadow nit #5: the PPD comparison (install
  `power-profiles-daemon` in a scratch VM, repeat the launch) settles the upstream report's
  framing; recorded as not provided by this task.
- **Owner operator (standing; not this task's failure)** — Omega high/secrets: `~/AI/secrets/`
  directory 755 and files 644 (AGENTS.md section 4 requires 700/600) — the standing TASK-0033
  step-stop, already blocked there for operator action. This task's own `pass.txt` handling was
  verified clean by Omega (`sshpass -f`; the value never written to any file, never echoed).

**Reference record (per plan item 6):** the 2026-10-08 12-pane gate (TASK-0034 `## Test Results`,
dated Big entry 2026-10-08) is the standing reference: exactly one console error of 12 panes (the
Power pane; the other 11 clean, ERR_LINES=0). No gate re-run: the Power pane is the only in-scope
pane. Consequence for TASK-0026 DoD box 2 ("all panes ... load without console errors"): it stays
open for the Power pane until upstream Cinnamon changes; this doc is the standing reference for
that gate. The verdict is process-level only (no-render, A7); screenshot-level re-verification is
deferred until the no-render state is resolved.

### 2026-10-13: re-run after the Tails fix round

Re-verifies the item 6 final verdict (PASS) against the post-fix `## Implementation` (fix-round entry). Shadow re-run: clean (`## Review`). Omega re-run: clean (`## Security`). No code change (classification (b) stands), so this is a verdict re-verification, not a re-run of items 1-5. Those stand as originally executed and PASSed: no new environment work, no guest state change (fix-round "Checks run" line 330).

**Independently re-run this pass** (read-only, no VM disturbance, no state change):
- Host canonical checkout `cs_power.py`: `md5sum` = `ab9499015f1484b20add77d54385660d` (still matches the three-way chain in items 2-3); `git status --porcelain` on the file empty (not a dirty port file) and `git status --porcelain | grep -c cs_power` = 0 (no pre-existing dirty port file is this file); `git rev-parse --short HEAD` = `61695c7`, `--is-shallow-repository` = true (unchanged).
- No-op framing (should-fix #3), verified end-to-end from source (lines 855-896): `:871` `on_my_setting_changed()` at pane init, `:891` `Get ActiveProfile` into `active_profile`, `:892` `set_active_iter(option_map[active_profile])`, `:869` `connect('changed', on_my_value_changed)`, `:878` `on_my_value_changed`, `:883` `Set` writes back `value` = the active row's profile = the just-read `active_profile` (no-op); the combo is set at `:892` before the failing `:883`, so the displayed value is correct; the `on_my_value_changed` `Set` path (`:878-883`) carries no try/except of its own (consistent with the observed traceback firing at `:883`). Confirms the root-cause statement and the basis of the intake-Unknown resolution ("display intact").
- Guest `tuned/utils/polkit.py` (Rocky): `flags = 1  # AllowUserInteraction flag` (line 24), `CheckAuthorization(..., flags, ...)`, `return 1 if ret else 0` (line 41). Confirms the fix-round "decisive for finding 1" claim: the check is interactive-capable and returns not-authorized (0) when no agent is attached.
- Guest polkit agent (Rocky): `gnome-keyring-daemon --daemonize --login` running (pid 2873). Confirms the agent-availability bound on the live-desktop inference.

**Carried-forward open items** (the original `## Test Results` list) all resolved in the post-fix `## Implementation`, except the operator-owned secrets step-stop:
- Shadow should-fix #1 (user-click path, intake Unknown line 34): resolved. Click case flagged INFERRED-not-tested (item 4); intake Unknown resolved (display intact per the no-op verified above; profile switching auth-gated by design); the inference is bounded by the verified `flags = 1` plus the running agent.
- Shadow should-fix #2 (allow_active misattribution, corroborated by Omega medium/authz): resolved in both places (polkit bullet, root-cause statement). `allow_active=yes` is stated as the permissive clause; the denial is attributed to the unsatisfied interactive check in a non-agent context, citing the verified `polkit.py:24` `flags = 1`; the security-weakening guest-polkit fix direction has no supporting text left.
- Shadow should-fix #3 (no-op framing): resolved, verified end-to-end from source above.
- Shadow nit #4 (citation path): resolved. Full guest path `/usr/lib/python3.12/site-packages/tuned/exports/dbus_exporter_with_properties.py:49` plus owning package `tuned-2.27.0-2.el10_2`.
- Shadow nit #5 (PPD comparison): resolved. Explicit note for `Vector` records the out-of-scope PPD comparison as the upstream report's open framing question.
- Omega high/secrets (`~/AI/secrets/` 755/644): carried, not resolved here. Operator-owned standing TASK-0033 step-stop; the fix round correctly did not address it; not a failure of this task's DoD.

**Checks this pass:** re-verification only. Items 1-5 not re-run (no code change, no new environment work; unchanged and originally PASSed), stated explicitly, not silently dropped. House-standard rows (compile/linter/unit/integration/Sparky) remain N/A as in the original verdict (no source change; no-render A7).

**Verdict:** PASS, re-verified. The post-fix `## Implementation` is accurate against the canonical checkout (three-way md5, clean git status, the no-op chain) and the Rocky guest (the `flags = 1` polkit check, the running agent). Every DoD box still stands: root cause (box 1), reproduction on both VMs (box 2), classification (b) (box 3), fix N/A (box 4), this entry (box 5). Zero FAILs. All five carried-forward Tails/Vector items are resolved in the post-fix record; the only carried item is the operator-owned secrets step-stop, which is not a failure of this task. Nothing goes to `Tails` (no code bug, no harness bug); the diagnostic record is now accurate and the PASS is strengthened, not reversed.

---

## Docs

*Owner: `Vector`.*

### 2026-10-13: docs update after the review and re-run chains (diagnosis, no code change)

| File | Sections touched | What changed |
|---|---|---|
| `~/Linux/projects/cinnamon-for-rocky10/README.md` (working tree, uncommitted; no git operations run; the canonical repo's commits stay local pending the TASK-0033 operator rotation, per the TASK-0026 and TASK-0027 precedent) | "What the complete set adds" | Added a third "Known issue." paragraph after the backlight one, same pattern as the two existing entries. The Power pane D-Bus `Unauthorized (36)` traceback at `cs_power.py:883 on_my_value_changed` on pane startup; process survives; displayed profile correct (the failing `Set` is a no-op, the combo is set before it). Root cause as verified in ## Implementation (base-OS `tuned-ppd` owns both candidate names, `power-profiles-daemon` not installed; the polkit gate on `net.hadess.PowerProfiles.switch-profile` rejects the unguarded startup `Set` in sessions with no attached polkit agent). Reproduces on both test VMs (Rocky 10.2 Wayland, Fedora 45 X11, identical error). The live-desktop click outcome is flagged inferred (the team's test VMs cannot drive an interactive dialog, no-render). The fix belongs upstream in `linuxmint/cinnamon` (guard the `Set` or suppress the startup self-trigger); no fix in this environment; persists on the published set. This is the entry the TASK-0026 `## Docs` 2026-10-10 entry anticipated ("Surfaces when TASK-0035 reaches a verdict") |
| `planning/docs/TASK-0035-cinnamon-power-pane-dbus-unauthorized.md` | `## Docs` | This entry plus the upstream report draft below (the Note for `Vector` from ## Implementation, Shadow nit 5) |

**Checked and needed no change:**
- `CHANGELOG.md` — no project-level changelog exists in the canonical repo (no `CHANGELOG.md` at root; the only ChangeLog files are inside the untracked upstream component checkouts; re-verified this pass, same finding as the TASK-0026 and TASK-0027 `## Docs` entries). No spec change this task (diagnosis, item 5 skipped), so no `%changelog` entry either
- `~/Linux/projects/cinnamon-for-rocky10/INSTALL.md` — the only pane reference is the Installed-packages row `cinnamon-control-center 6.7.2-1.el10, System Settings app (32 panels)` (name and version only, no pane-behavior claim, accurate); the Troubleshooting section has no known-issue pattern, and the TASK-0026 precedent documented known issues in the README only
- `README.md` (team repo, `metalllinux/team-chaotix`) — no Power-pane, `cs_power`, or 12-pane reference anywhere in the file; the stale "Active projects" Cinnamon subsection is pre-existing staleness flagged in the TASK-0026 `## Docs` 2026-10-10 entry, not part of this landed state
- `vm-test/` documentation and `tasks/` — test infrastructure, not user-facing; the no-render limitation is test-VM state (TASK-0034), not published-artifact behavior, and stays documented where it is
- The published set (`rpms/`, `rpms/SHA256SUMS`, `rpms-local/`) — untouched; the README entry describes behavior of the file the set ships (md5 `ab9499015f1484b20add77d54385660d`, the unmodified upstream file the published 6.7.4-3 and the local 6.7.4-4 both carry), not the set itself

**Could not verify:**
- The PPD comparison (the Note for `Vector` in ## Implementation, Shadow nit 5): whether Cinnamon's own default service `power-profiles-daemon` fires the same `:883` traceback. Unverified by this task; it is the missing data point for the upstream report's framing and decides whether the issue is a Cinnamon bug reproducing against Cinnamon's own default service or a Cinnamon-meets-`tuned-ppd` integration issue. What settles it: a scratch VM with `power-profiles-daemon` installed, one Power-pane launch, observation of whether the `:883` traceback fires. Per the Note it is the report's open framing question, not a defect of this task, so it is carried into the draft below, not into the README

### Upstream report draft — `linuxmint/cinnamon` (AGENTS.md §8 step-stop)

**Status: draft only, not submitted.** The issue targets a repository outside
`metalllinux`, so per AGENTS.md §8 `Vector` drafts and stops; the operator
reviews and edits this content, and only a separate request has `Knuckles`
submit it. Nothing was submitted from this dispatch. The missing
PPD-comparison data point is carried as the draft's open framing question,
as the Note for `Vector` directs.

**Title (candidate):**

Control Center: Power pane logs a D-Bus `Unauthorized (36)` traceback at
`cs_power.py:883` on startup

**Body (candidate):**

```
## Summary

Opening the Power pane of the Control Center (`cinnamon-settings power`,
module `power`) logs a traceback at `modules/cs_power.py:883`
(`on_my_value_changed`):

    GDBus.Error:org.freedesktop.DBus.Python.dbus.exceptions.DBusException: Unauthorized (36)

The process survives and the pane stays usable.

## Environment (verified)

- `cs_power.py` as of upstream commit `e9ba28a87f0f69594487a08e940840d494bb3ea0`
  (md5 `ab9499015f1484b20add77d54385660d`, byte-identical to the file installed
  on both test VMs; unmodified upstream code)
- Rocky Linux 10.2 guest, Wayland session, `cinnamon` 6.7.4 RPM
- Fedora 45 guest, X11 session, `cinnamon` 6.7.5^unstable RPM
- Answering service on both VMs: base-OS `tuned-ppd`
  (`2.27.0-2.el10_2` / `2.27.0-3.fc45`), which owns both candidate names
  `net.hadess.PowerProfiles` and `org.freedesktop.UPower.PowerProfiles`.
  `power-profiles-daemon` is not installed on either VM.

## Reproduction

Launch the Power pane in a user session (`cinnamon-settings power`).
Reproduced on Rocky 10.2 (2 controlled launches) and Fedora 45
(1 controlled launch), identical traceback and identical wire error.

A raw wire reproduction without Cinnamon, as a regular user on the
system bus:

    dbus-send --system --print-reply \
      --dest=org.freedesktop.UPower.PowerProfiles \
      /org/freedesktop/UPower/PowerProfiles \
      org.freedesktop.DBus.Properties.Set \
      string:org.freedesktop.UPower.PowerProfiles string:ActiveProfile \
      variant:string:balanced

returns exit 1 with
`Error org.freedesktop.DBus.Python.dbus.exceptions.DBusException: Unauthorized`.
The matching `Properties.Get` calls (`Profiles`, `ActiveProfile`) succeed.

## Root cause

`cs_power.py` sends the `Set` at `:883` without a try/except (its sibling
`Get` at `:889-895` is wrapped). In the startup self-trigger the `:883`
call is a no-op: it writes back the profile value the pane just read at
`:891` (the combo is set at `:892` before the failing `Set`), so the
displayed profile is correct and the startup failure is cosmetic.

The rejection is inside the answering service. `tuned-ppd` wraps the
`ActiveProfile` setter in a polkit gate for the action
`net.hadess.PowerProfiles.switch-profile` (action file
`/usr/share/polkit-1/actions/net.hadess.PowerProfiles.policy`,
`allow_active=yes`); the check is interactive-capable
(`POLKIT_CHECK_AUTHORIZATION_FLAGS_ALLOW_USER_INTERACTION`), so it
authorizes an active-session user who authenticates, and returns
not-authorized without prompting when no polkit agent is attached to the
caller's session. In a session with no agent the service raises
`DBusException("Unauthorized")`, which dbus-python ships as the error
name above and GLib renders with GDBusError code 36 as
`Unauthorized (36)`.

## Open framing question (not yet verified)

Whether the same traceback fires against `power-profiles-daemon`
(Cinnamon's own default service, not installed on the test VMs) has not
been verified. That data point decides the framing of this report:

- if PPD also rejects the unauthenticated startup `Set`, this is a
  Cinnamon bug reproducing against Cinnamon's own default service;
- if PPD authorizes it, this is a Cinnamon-meets-`tuned-ppd`
  integration issue, a base-OS service answering Cinnamon's bus names
  with a stricter authorization model.

To settle it: install `power-profiles-daemon` in a scratch VM, launch
the Power pane once, and observe whether the `:883` traceback fires.

## User impact

- Displayed profile at pane startup: correct (the failing `Set` is a no-op).
- Profile switching by a user click on a live desktop: goes through the
  same gate; inferred to prompt for authentication and succeed with the
  user's password (the check is interactive and a polkit agent is
  attached to a live session). Inferred, not live-tested.
- Profile switching in a session with no attached polkit agent: the same
  `:883` traceback fires on the click.

## Suggested fix

Either guard the `:883` `Set` in try/except, matching the existing style
at `:893-894`, or suppress the startup self-trigger so pane
initialization does not send a `Set` at all.
```

---

## Release

*Owner: `Knuckles`.*

**DONE checklist verified:** yes

Verified 2026-10-13 by Knuckles. Boxes 1-3 are ticked against `## Implementation` items 1-4 (root cause with the exact wire error name plus the rejecting component at file:line, Fedora reproduction with evidence, classification (b) upstream Cinnamon behavior), re-verified in the 2026-10-13 re-run chain (Big: PASS, zero FAILs; Shadow, Omega, Charmy: clean). Box 4 is conditional and not applicable: no in-environment fix exists (classification (b), item 5 skipped per the plan conditional; the fix belongs upstream in `linuxmint/cinnamon`), so the box is satisfied as N/A and ticked. Box 5: `## Test Results` carries the final verdict (Big: PASS; re-run: PASS re-verified).

- **Branch:** `main` in `metalllinux/team-chaotix` (planning-doc commit, the team-repo convention for planning-doc state, no feature branch); `feature/TASK-0024-rpm-signing-gpgcheck` in the canonical repo `~/Linux/projects/cinnamon-for-rocky10` (the README change commits on the existing branch, per the TASK-0026/TASK-0027 precedent)
- **Commits:** GPG-signed no (`commit.gpgsign` unset in both repos; the branch history is all-unsigned, so the commit is unsigned per branch convention, author `Team Chaotix <chaotix@metallinux.dev>`)
- **PR:** none opened this step. No open PR on the canonical branch (GitHub API check 2026-10-13). The 8 local commits on the branch (including this step's README commit) enter `main` via a new PR in the next release step, after the TASK-0033 rotation step-stop lifts (the TASK-0027 `## Release` precedent: "that is the next release step, not this one"). The external upstream-report issue is a draft at the operator step-stop (`## Docs`), not submitted, human review pending on the operator
- **Deploy:** n/a. No deployment workflow for this task (diagnosis, no source change, no published artifact); nothing is published and nothing is pushed from the canonical repo this step

### Canonical repo: README known-issue change (committed, rides the held push)

Committed `22aa49ced2553cda093affa331f66e34489a2ea6` ("docs: record Power pane D-Bus Unauthorized known issue in README (TASK-0035)") on `feature/TASK-0024-rpm-signing-gpgcheck`, 1 file changed, 25 insertions (the "Known issue." paragraph Vector drafted per `## Docs`; the diff was reviewed before commit, no secret in it). The branch is now 8 commits ahead of `origin` (`8cde059`, `620ceb4`, `9d1eb46`, `0b3773b`, `ec49438`, `5e081c4`, `9edabed`, `22aa49c`); the working tree is clean apart from the untracked component checkouts and `rpms-local/` (left untouched).

### Blocked by the standing TASK-0033 rotation step-stop

Push probe this step (`GIT_TERMINAL_PROMPT=0 git push --dry-run origin feature/TASK-0024-rpm-signing-gpgcheck`, a dry run, no remote state change; URL masked; no secret value in this record):

```
fatal: could not read Password for 'https://***@github.com': terminal prompts disabled
rc=128
```

The push still fails at the credential stage, the same mode as the TASK-0027 `## Release` probe: the store credential helper has no usable entry for this URL. State change since that record: the local origin URL in `.git/config` now embeds a token in the userinfo (verified by `git remote -v` this step; the value is not recorded here; Charmy's out-of-domain observation in `## License (Charmy)` names the same instance). That token is not a fix, it is part of the exposure the rotation removes. The canonical push therefore stays blocked by the standing TASK-0033 operator rotation step-stop, and the 8 local commits stay local.

Operator steps (exact; no agent may complete them, per the standing step-stop; supersedes the TASK-0027 `## Release` list by the two deltas marked):

1. Revoke the live `metalllinux` classic PAT. Live state per the record: the team-chaotix origin URL embeds a token whose value matches `~/AI/secrets/githubtoken.md` (repo,workflow scope, verified live 2026-10-12, TASK-0027 `## Security` finding 1); the canonical-repo origin URL now embeds a token (this step's record, value not recorded); the global `~/.gitconfig` `insteadOf` rewrite carries a distinct token (verified dead 2026-10-12). Revoke whatever the operator recognizes as live, and check the account audit log and token last-used for unexpected use.
2. Create the replacement PAT at least-scope for what the team needs, and store it per AGENTS.md section 4 (one file in `~/secrets/`, file mode 600, directory mode 700). Delete `~/AI/secrets/githubtoken.md`.
3. Remove the credential state the tokens ride: `git config --global --unset $(git config --global --list --name-only | grep -i insteadof)` (the substitution keeps the value off the command line); in team-chaotix, `git remote set-url origin https://github.com/metalllinux/team-chaotix.git`, then unset the local `credential.username`, `credential.password`, `credential.helper` keys; **in the canonical repo, `git -C ~/Linux/projects/cinnamon-for-rocky10 remote set-url origin https://github.com/metalllinux/cinnamon-for-rocky10.git` (delta: the URL now carries a token; it was credential-free when the TASK-0027 list was written)**; remove the token lines from `~/.git-credentials` and `~/.netrc`; `chmod 600 ~/.gitconfig`. SSH-key auth is the preferred end state, because then no token exists on this machine.
4. Fix the `~/AI/secrets/` modes (`chmod 700 ~/AI/secrets` and `chmod 600` on each file) or consolidate into `~/secrets/`; decide the fate of `temp_pass.md`, `token.md`, `ai-machine-password.md` (TASK-0033 `## Security` finding 2).
5. Re-run the blocked push: `git -C ~/Linux/projects/cinnamon-for-rocky10 push origin feature/TASK-0024-rpm-signing-gpgcheck` (**delta: carries 8 local commits, not 7: `8cde059`, `620ceb4`, `9d1eb46`, `0b3773b`, `ec49438`, `5e081c4`, `9edabed`, `22aa49c`**).
6. Verify the origin state after the push: fresh clone of the branch, the README "Known issue." Power-pane paragraph present, `grep '^Release:' spec/cinnamon-settings-daemon.spec` returns `3.el10`, then run the signing-step checks in the TASK-0027 `## Release` prerequisites list and open the new PR for the branch to `main`.

### Upstream report draft (external repo, AGENTS.md section 8 step-stop)

The draft in `## Docs` (title plus body, candidate) targets `linuxmint/cinnamon`, a repository outside `metalllinux`. Per AGENTS.md section 8 it is an operator step-stop: `Vector` drafted and stopped; nothing was submitted this step, and no agent submits it. Exact operator steps:

1. Review and edit the draft in `## Docs`. The open framing question (the PPD comparison) is the missing data point; the draft carries it as such, per the Note for `Vector` in `## Implementation`.
2. Submit the issue on `linuxmint/cinnamon` from the operator's own GitHub account (web UI or CLI). If a team submission is wanted instead, that is a separate request to `Knuckles` after the rotation steps above (a submission from this host needs a working credential, which the rotation provides).

### GitHub Issue

Searched open issues in `metalllinux/cinnamon-for-rocky10` and `metalllinux/team-chaotix` (GitHub API, anonymous, 2026-10-13): zero open in both, and a title/body search for `TASK-0035` in each repo plus a `power pane` search across the `metalllinux` org return zero in all states. No issue exists for this task, so nothing to close.

### team-chaotix push

This doc is committed to `main` (`chore(planning)` checkpoint convention, no feature branch for planning-doc state) and pushed to `origin` on `metalllinux/team-chaotix` (in-account, standing autonomy); this entry lands as the commit recording the step, pushed in the same sequence. Working tree state: the out-of-scope entries (`cinnamon-1-vm.xml`, `planning/docs/TASK-0027-cinnamon-brightness-fix.md`, `planning/docs/TASK-0034-cinnamon-shell-no-render.md`, and the untracked `-`, `continue-prompt-2026-10-05.md`, `prompt-task0026-continuation.md`) are excluded from the commit and left untouched, per the TASK-0026 `## Release` precedent.

---

## Archive

*Owner: `Espio`, the only agent that deletes. Superseded detail lands here rather than being
lost. Decisions, verified facts, rejected options with their reasons, known traps, and anything the
user said are never deleted.*

**Pruning log**

| Date | What was pruned or compressed | Rough size |
|---|---|---|
| | | |
