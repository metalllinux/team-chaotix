# TASK-0017: terminal for the Rocky 10 Cinnamon desktop — source-build gnome-terminal

**Context** — the DoD names gnome-terminal ("a working terminal (gnome-terminal) is part of the
desktop set/install and opens from the Cinnamon session"), and the user's 2026-09-14 order is
feature parity against `fedora-cinnamon-ref`, which ships gnome-terminal. Item 0.1 (Big,
2026-09-15, `## Test Results` in the task doc) settled A1 as FAIL: gnome-terminal is in no Rocky 10
repo (AppStream, CRB, BaseOS, Extras) and not in EPEL; the only terminal packages available are
`xterm` (BaseOS) and `konsole` (EPEL). The plan's fallback (pick the closest available alternative,
record a deviation) is open, or the DoD can be met as written by building gnome-terminal from
source, like the rest of the Cinnamon stack in this repo.

**Options**

| Option | Trade-off |
|---|---|
| A. Source-build gnome-terminal as an RPM in this repo (plan item 1.4), dependency chain verified before the spec is written | Meets the DoD as written, matches the ref for the parity run, no third-party repo in the install set. Cost: one non-Cinnamon spec, an unverified EL10 dependency chain (gtk4, VTE), and item 1.4's estimate grows from 1 to 5 turns |
| B. `xterm` from BaseOS (the plan fallback, first-party) | Zero build cost, zero external repos. But xterm is a minimal terminal (no tabs, no settings UI) and the weakest choice against a desktop parity goal; still needs a recorded deviation from the DoD's gnome-terminal |
| C. `konsole` from EPEL (the plan fallback, full-featured) | Full-featured, one dnf line. But it puts EPEL into the install set of a desktop whose packaging story is "Rocky 10 plus this repo", needs epel-release on every fresh test VM, and still records a deviation from the DoD |

**Recommendation** — A. It is the only option that satisfies the DoD as written and matches the
Fedora ref, the parity bar the user set on 2026-09-14. The repo already source-builds the whole
Cinnamon stack; one more spec is an incremental pattern, not new capability. The unknown is
bounded: item 1.4 verifies the dependency chain with `dnf repoquery` in its first turn, before any
spec is written, and carries the konsole/xterm fallback inside it if that verification fails.

**Consequences** — commits this repo to a non-Cinnamon spec and to gnome-terminal's EL10 dependency
chain as a build-time and install-time fact; the install set gains one RPM from this repo (plus
`rocky-logos`). Cost is about 4 extra dispatch turns in item 1.4 (budget 42 to 47). `INSTALL.md`
(Vector, item 3.2) must describe the source-built terminal. A later terminal switch is a
set-plus-spec-plus-docs change.

**Reversibility** — cheap. The spec and RPM are additive files in the repo; `git revert` removes
them and the install set falls back to option C (or B) with a recorded deviation. No point of no
return before the PR merge; the merge itself is revertible.
