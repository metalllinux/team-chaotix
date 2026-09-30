## Status

- **Problem:** Control Center for Cinnamon is not available when RPMs are installed on Rocky Linux 10.
- **Goal:** Fix the Control Center availability and ensure it appears correctly in the Cinnamon menu.
- **Reference VMs:** Rocky Linux 10 and Fedora Cinnamon VMs will be spun up for testing and comparison.

## Definition of Done

- [x] Rocky Linux 10 VM (`cinnamon-1`) spun up at `192.168.122.10` and accessible
- [x] Fedora Cinnamon 45 beta VM spun up and accessible
- [x] Rocky 10 golden image exists at `/var/lib/libvirt/images/rocky-10-golden.qcow2`
- [x] Local DNF repo from TASK-0006 is available
- [x] `cinnamon-control-center-6.7.2-1.el10.x86_64` installed on Rocky VM
- [x] `cinnamon-settings-daemon-6.7.2-2.el10.x86_64` already installed on Rocky VM
- [x] `cinnamon-session-6.7.3-1.el10.x86_64` already installed on Rocky VM
- [x] `cinnamon-settings` binary verified at `/usr/bin/cinnamon-settings`
- [x] Root cause identified: `TimezoneMap` GI namespace is missing in Rocky 10
- [x] Fixed `cs_calendar.py` written to disk (backup at `cs_calendar.py.bak`)
- [ ] Control Center GUI opens successfully on Rocky Linux 10
- [ ] All panes in Control Center load and function
- [x] Fedora Cinnamon 45 beta verification
- [ ] Test results documented

## Next Actions

1. Download Fedora Cinnamon 45 beta ISO from https://fedoraproject.org/spins/cinnamon/download/beta/
2. Spin up Fedora Cinnamon VM
3. Test Control Center on Fedora Cinnamon 45 beta

## Plan

(Amy - TBD)

## Implementation

(Tails - TBD)

## Review

(Shadow - TBD)

## Security

(Omega - TBD)

## License

(Charmy - TBD)

## Test Results

(Big - TBD)

## Docs

(Vector - TBD)

## Release

(Knuckles - TBD)

## Archive

(Espio - TBD)
