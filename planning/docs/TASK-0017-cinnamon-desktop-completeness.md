# TASK-0017 — Complete the Cinnamon desktop: missing subpackages, Rocky wallpaper, branding, terminal

> **Section order below is fixed.** Each agent writes to its own section and no other. `Robotnik`
> reads only `## Status` and `## Next Actions`. Do not reorder, rename, or remove sections.

- **Created:** 2026-08-30

---

## Status

*Owner: `Robotnik`. Keep this SHORT and CURRENT — it is one of only two sections the PM reads, so a
stale entry means the whole loop runs on bad information.*

**Now (2026-08-30): task created from direct user feedback.** The user boots into Cinnamon (Wayland)
on the bare-metal host `howard@192.168.1.103` (GDM auth from TASK-0008 works), but the desktop is
substantially incomplete. Reported items: (1) black wallpaper — wants a Rocky Linux 10 wallpaper
from the Rocky wallpaper RPM installed and set automatically on first login; (2) the tray/panel
shows the Cinnamon logo, not the Rocky Linux logo; (3) Cinnamon applets, themes, and extensions do
not load; (4) the only application that loads is the file manager (nemo); (5) the Cinnamon Settings
menu is missing; (6) the terminal (gnome-terminal) won't open. User took screenshots in `~/Pictures`
(only one found: `Screenshot 2026-08-30 21-49-39.146.png`, 3840x2160; user said "multiple" and the
message cut off at "There does" — request the rest). **Model limitation: no image input, so the
screenshots cannot be viewed by any agent; diagnosis runs on the user's text + package/log evidence,
and the screenshot is retained as an artifact.**

**Evidence gathered (2026-08-30):** the installed and built Cinnamon set is a **subset** of 13
runtime RPMs — `cinnamon`, `cinnamon-control-center`, `cinnamon-desktop`, `cinnamon-menus`,
`cinnamon-session`, `cinnamon-settings-daemon`, `cjs`, `mozjs115`, `muffin`, `muffin-clutter`,
`muffin-cogl`, `nemo`, `xapps-lib` (48 total in `rpms/` incl. debuginfo/debugsource/devel). A full
Cinnamon 6.7 desktop additionally needs the monorepo subpackages (themes, international/applets/
desklets, extension-manager, plugin-applet/desklet/file-manager/screensaver, screensaver,
translations, desktop-filesystem) plus a terminal — none are built or installed. `rocky-logos`
**is** installed (so the branding assets exist but are not applied). **Root-cause hypothesis
(unverified): the build only produces a subset of the cinnamon monorepo subpackages.**

**Environment / scope:**
- Files in scope: the Cinnamon build system (specs + build scripts) and the RPM set in
  `metalllinux/cinnamon-for-rocky10`; the cinnamon monorepo source (subpackages); wallpaper/
  branding/terminal config; the "Cinnamon set" definition (coordinates with TASK-0016's INSTALL.md).
- Touches the DB schema: no
- Graphical UI: yes — the desktop session itself; VM + bare-metal testing required
- Rocky Linux target: yes (Rocky Linux 10.2)

**Unknowns:**
- The exact full set of cinnamon subpackages a complete 6.7 desktop needs, and which are present in
  the source tree but not built. (Investigate.)
- The build system's structure and how new subpackage builds are added. (Investigate.)
- The Rocky wallpaper package name and which wallpaper to default to. (Verify, do not guess.)
- The mechanism to set the wallpaper automatically on first login. (Design.)
- How the tray/panel branding is switched from the Cinnamon logo to the Rocky logo using
  `rocky-logos`. (Investigate.)
- Which terminal to ship (gnome-terminal from the base repo vs. another). (Design.)
- Why the Cinnamon Settings menu is absent although `cinnamon-control-center` is installed (missing
  `.desktop`/menu generation vs. launch failure). (Diagnose.)

**Coordination / priority:** this task redefines "the Cinnamon RPM set" from the 13-subset to the
complete set. It is the current priority (the user's active ask). TASK-0016's INSTALL.md doc-writing
is **paused** until this task lands, so the docs can describe the complete set. TASK-0015's multi-DM
matrix should test the **complete** set, so it also follows this task.

**Infra note (2026-08-30):** the first two `Amy` plan dispatches for this task died with
"Connection reset by server" — the EVO-X2 model endpoint flapping (HTTP 200 on probe, drop under
inference load); the TASK-0010 GPU-wedge problem is live. Endpoint recovered after a 60s cooldown;
retrying. If dispatches keep dying, the block is the endpoint, not the agent — escalate to the user
rather than burning retries.

---

## Definition of Done

*Owner: `Robotnik`, and nobody else. Written **before** any work starts. Objectively checkable —
if a box cannot be verified by looking at something, rewrite it.*

- [ ] **Complete package set.** The missing cinnamon monorepo subpackages required for a full 6.7
      desktop are built and added to the RPM set and the documented install set. The exact list is
      established by the plan/diagnosis (recorded in `## Plan`/`## Implementation`), not guessed.
- [ ] **Terminal.** A working terminal (gnome-terminal) is part of the desktop set/install and opens
      from the Cinnamon session.
- [ ] **Wallpaper.** The Rocky Linux 10 wallpaper (from the Rocky wallpaper RPM) is installed and is
      set automatically on first login — the session does not start with a black wallpaper.
- [ ] **Branding.** The tray/panel shows the Rocky Linux logo, not the Cinnamon logo (using
      `rocky-logos`).
- [ ] **Applets load.** The default Cinnamon applets are present and load in the panel (no missing/
      erroring applets).
- [ ] **Themes load.** `cinnamon-themes` is present, the default theme applies, and themes are
      selectable without breakage.
- [ ] **Extensions work.** The extension/applet/desklet manager is present and functional (can list
      and enable the shipped extensions/applets/desklets).
- [ ] **Settings menu.** The Cinnamon Settings menu is present in the menu and opens control-center.
- [ ] **File manager still works.** nemo opens and functions (regression check).
- [ ] **VM end-to-end.** On a fresh minimal Rocky 10.2 VM: install the complete set, log in via GDM
      (Cinnamon Wayland), and every item above is verified working. Recorded in `## Test Results`
      with evidence.
- [ ] **Bare-metal end-to-end.** On `192.168.1.103`: update to the complete set and every item above
      is verified working. Recorded in `## Test Results`.
- [ ] `Shadow`: no unresolved blockers or should-fix findings in `## Review`.
- [ ] `Omega`: no unresolved findings above `low` in `## Security`.
- [ ] `Big`: all harness checks PASS, with no silently dropped checks.
- [ ] `Vector`: `INSTALL.md`/`README.md` updated to describe the complete set (coordinates with
      TASK-0016).
- [ ] `Knuckles`: merged to `metalllinux/cinnamon-for-rocky10` main via PR.

---

## Next Actions

*Owner: whoever wrote last. The future only — delete what has been done. The second of the two sections
the PM reads.*

- [ ] `Amy`: investigate and write `## Plan` — the complete subpackage list (what a full 6.7 desktop
      needs, what's in the source tree, what's missing), the build-system strategy for adding the
      missing subpackages, the Rocky wallpaper package (verified name) + first-login mechanism, the
      tray/panel branding mechanism via `rocky-logos`, the terminal choice, the Cinnamon-Settings-menu
      diagnosis, and the VM + bare-metal test matrix. Read this doc's `## Status`, `## Definition of
      Done`, `## Next Actions` plus the repo build system and source tree; do not read other planning
      docs in full.
- [ ] `Tails`: build the missing subpackages and add them to the set; add the terminal; implement the
      first-login wallpaper; implement the tray/panel branding; fix the Cinnamon Settings menu.
- [ ] `Big`: verify end-to-end on a fresh minimal VM and on `192.168.1.103`; record in `## Test
      Results`.
- [ ] `Shadow` → `Omega` → `Big`: review chain on the diff.
- [ ] `Tails`: fix anything the chain returns.
- [ ] `Vector`: update `INSTALL.md`/`README.md` for the complete set (resume TASK-0016's doc work here).
- [ ] `Knuckles`: PR to main, merge.

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

## Test Results

*Owner: `Big`. Verdicts, never raw log dumps.*

**Workflow run:**

| Check | What it exercises | Result | Notes |
|---|---|---|---|
| compile | changed files | PASS/FAIL | |
| linter | style and correctness | PASS/FAIL | |
| unit tests | individual functions | PASS/FAIL | |
| integration tests | end-to-end flows | PASS/FAIL | |
| Sparky tests | Rocky Linux UI (if applicable) | PASS/FAIL | |

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
lost. Decisions, verified facts, rejected options with their reasons, known traps, and anything
the user said are never deleted.*

**Pruning log**

| Date | What was pruned or compressed | Rough size |
|---|---|---|
| | | |
