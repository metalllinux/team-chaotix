# TASK-0008 — new-session prompt (verbatim original task brief)

> Paste everything below this line into a fresh opencode (Robotnik) session to continue TASK-0008.
> The planning doc `planning/docs/TASK-0008-cinnamon-gdm-auth-fix.md` carries all state.

---

Task for Robotnik: find out why GDM login fails with an Authentication Error when the Cinnamon
session is selected on Rocky Linux 10, fix it in the cinnamon-for-rocky10 repository, and widen the
Cinnamon VM test coverage.

## What the user hit

1. Installed the Cinnamon RPMs from the local DNF repo on the user's Rocky Linux 10.2 machine,
   following the INSTALL.md in the repository.
2. Logged out, selected the Cinnamon session from GDM, entered the password.
3. Got an Authentication Error instead of the desktop.
4. Had to reboot the machine to get a working session back.

The machine works again after the reboot. The failure must be reproduced in a libvirt VM before
any fix is claimed.

## What this task must deliver

1. **Root cause with evidence.** Reproduce the failed Cinnamon-session login in a VM, capture
   `journalctl -u gdm` and `/var/log/secure` from the failed attempt and from a successful GNOME
   login, and compare. State the cause in the planning doc with the log lines that prove it.
2. **Fix in the repository.** Repo is `metalllinux/cinnamon-for-rocky10` (main branch), project
   directory `~/Linux/projects/cinnamon_4_rocky10/`. After the fix, a system that already has
   GDM plus GNOME must be able to switch to the Cinnamon session in GDM and log in successfully.
3. **Wider test matrix.** Big owns this. Every scenario runs on a libvirt Rocky Linux 10 VM and
   every scenario has a written Sparky/Sparrow (Raku) test, because all Rocky Linux testing goes
   through Sparky. Scenarios, minimum:
   - Fresh Rocky Linux 10 with GDM and GNOME installed (the user's exact configuration). Install
     the Cinnamon RPMs, switch to the Cinnamon session in GDM, log in, and verify the session comes
     up.
   - Fresh Rocky Linux 10 with LightDM installed. Install the Cinnamon RPMs, then log in to the
     Cinnamon session through LightDM and verify it works.
   - Fresh Rocky Linux 10 with no login manager at all (blank install). Install the Cinnamon RPMs
     and verify the Cinnamon session is available and login works.
   - Uninstall. After a successful install, remove the Cinnamon RPMs and verify the system is not
     left broken. No broken or dangling packages, no leftover session entries, no PAM breakage, and
     the previous login path still works.
   - As many additional configuration combinations as are practical. The point is the widest
     sensible coverage, not just the one configuration the user hit.
4. **Reusable tests.** Each scenario gets a real Sparrow task that can be re-run, not a one-off
   manual check. Big decides the Sparky harness layout and records results in the planning doc.

## Context pointers

- Repo: https://github.com/metalllinux/cinnamon-for-rocky10
- INSTALL.md in that repository is the procedure the user followed.
- Prior history: planning/docs/TASK-0002 through TASK-0006 cover the RPM builds, the first VM
  testing round, the DNF repo, and INSTALL.md validation.
- Testing strategy rules are in AGENTS.md section 7 (libvirt VMs, Sparky, Raku install procedure).

Create the TASK-0008 planning doc, write a Definition of Done that covers all four deliverables
above, add the TASKS.md row, and start the cycle.
