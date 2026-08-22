# How to automate GDM login testing for the Cinnamon port

**Context** — TASK-0008's Definition of Done requires reproducing a GDM "Authentication Error" in a
running VM and running a six-scenario GUI login matrix as re-runnable Sparky/Sparrow (Raku) tasks.
No GUI login automation exists today: TASK-0003/0005/0006 all tested headless package installs
(Xvfb is absent from EL10 repos, confirmed in TASK-0003 `## Test Results`). The driver choice and
VM-management choice fix the shape of every test script that follows.

**Options**

| Option | Trade-off |
|---|---|
| A. Drive an X11-forced GDM greeter with `xdotool` from inside a headless VM (virtual GPU, VNC as observation channel) | Small, standard, fully scriptable, works headless. Pins the matrix to the X11 greeter (Wayland greeter untested). `xdotool` availability in EL10 repos unverified; needs XAUTHORITY extraction from the running Xorg. |
| B. OpenQA with needlematch (screenshot/OCR) | Display-manager and protocol agnostic, Wayland-capable. Large new host infrastructure, needle baselines for a greeter that repaints between runs, and it is not the framework AGENTS.md section 7 names. Overkill for six scenarios. |
| C. No GUI driving; verify login by state only (session files, PAM config, `logind` after an autologin trigger) | Zero display dependence. Autologin is a different GDM code path from interactive password auth, so it cannot reproduce the user's "Authentication Error". DoD reproduction box unmeetable. |

**Recommendation** — Option A. It is the only option that exercises the user's exact failure path
(interactive password entry, session selected in the greeter). Availability of `xdotool` is verified
in work-breakdown item 3 before any driver code is written; the fallback ladder is `ydotool`,
`dogtail`, then a small XTest-based driver compiled inside the VM from the `xorg-x11-devel` headers
(XTest is core X11, so this last step is guaranteed feasible). The interactive reproduction phase
runs on the existing libvirt harness (VNC-graphics VM); the re-runnable matrix runs on Sparky's
QEMU VMs with a pre-seeded qcow2 (RPMs baked in via `virt-customize --upload`) so scenarios are
self-contained and re-runnable without host services.

**Consequences** — `main.raku` and `tasks/` land at the root of `metalllinux/cinnamon-for-rocky10`
(test scaffolding in the product repo; exit route is a dedicated Sparky repo if it grows). The host
gains permanent additive state: Raku, Sparky (`~/Code/sparky`), port 4000, a sudoers drop-in
(NOPASSWD `mount`/`umount` for the Sparky user), and a firewall rule. The matrix covers the X11
greeter only. One-time cost: image seed step per RPM set (~10 min).

**Reversibility** — Cheap to undo while we hold the only artifacts: delete `tasks/` and `main.raku`,
remove the Sparky/Raku installs, revert the sudoers drop-in and firewall rule. The one-way part is
strategic, not mechanical: if Cinnamon ever ships a Wayland session, this driver set is not
reusable and a Wayland input driver is needed then. That is future work, not a lock-in we regret.
