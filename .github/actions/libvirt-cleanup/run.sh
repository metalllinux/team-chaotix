#!/usr/bin/env bash
set -euo pipefail

# Libvirt cleanup
# Destroys VMs and cleans up libvirt resources

echo "::group::Libvirt cleanup"

vm_name="${VM_NAME:-test-vm}"
remove_disks="${REMOVE_DISKS:-false}"

# Destroy the VM
if virsh dominfo "$vm_name" >/dev/null 2>&1; then
  echo "Destroying VM: $vm_name"
  virsh destroy "$vm_name" 2>/dev/null || true
  virsh undefine "$vm_name" --remove-all-storage 2>/dev/null || true
  echo "VM destroyed: $vm_name"
else
  echo "VM not found: $vm_name (already cleaned up)"
fi

# Clean up any stale VMs matching the pattern
stale_vms=$(virsh list --all --name 2>/dev/null | grep -E "^test-vm|^sparky-vm" || true)
if [ -n "$stale_vms" ]; then
  echo "Cleaning up stale VMs..."
  echo "$stale_vms" | while IFS= read -r stale_vm; do
    virsh destroy "$stale_vm" 2>/dev/null || true
    virsh undefine "$stale_vm" --remove-all-storage 2>/dev/null || true
  done
fi

# Remove disk images if requested
if [ "$remove_disks" = "true" ]; then
  echo "Removing disk images..."
  find "${HOME}/.cache/team-chaotix/images" -name "*.qcow2" -delete 2>/dev/null || true
fi

# Clean up network interfaces
echo "Cleaning up network interfaces..."
virsh net-autostart --disable default 2>/dev/null || true

echo "Libvirt cleanup complete"
echo "::endgroup::"
