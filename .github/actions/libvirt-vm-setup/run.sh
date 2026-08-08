#!/usr/bin/env bash
set -euo pipefail

# Libvirt VM setup
# Provisions a Rocky Linux VM for Sparky testing

echo "::group::Libvirt VM setup"

os="${VM_OS:-rocky-10}"
ram="${VM_RAM:-4096}"
cores="${VM_CORES:-4}"
disk_size="${VM_DISK_SIZE:-40}"
vm_name="${VM_NAME:-test-vm}"

# Ensure libvirt is running
if ! virtylist 2>/dev/null; then
  echo "Starting libvirtd..."
  sudo systemctl start libvirtd 2>/dev/null || sudo libvirtd -d 2>/dev/null || true
fi

# Check if VM already exists and destroy it
if virsh dominfo "$vm_name" >/dev/null 2>&1; then
  echo "Destroying existing VM: $vm_name"
  virsh destroy "$vm_name" 2>/dev/null || true
fi

# Download base image if not cached
image_dir="${HOME}/.cache/team-chaotix/images"
mkdir -p "$image_dir"

case "$os" in
  rocky-10)
    image_name="rocky-10.qcow2"
    ;;
  rocky-9)
    image_name="rocky-9.qcow2"
    ;;
  *)
    echo "::error::Unsupported OS: $os"
    exit 1
    ;;
esac

image_path="${image_dir}/${image_name}"
if [ ! -f "$image_path" ]; then
  echo "Image not cached: $image_path"
  echo "Download Rocky Linux $os image or create from ISO"
  # In production, download from Rocky mirrors
  # For now, create a placeholder
  qemu-img create -f qcow2 "$image_path" "${disk_size}G"
  echo "Created placeholder image: $image_path"
fi

# Define VM XML
vm_xml=$(cat <<EOF
<domain type='kvm'>
  <name>${vm_name}</name>
  <memory unit='MiB'>${ram}</memory>
  <vcpu>${cores}</vcpu>
  <os>
    <type arch='x86_64' machine='pc-q35-7.2'>hvm</type>
    <boot dev='hd'/>
  </os>
  <devices>
    <disk type='file' device='disk'>
      <source file='${image_path}'/>
      <target dev='vda' bus='virtio'/>
    </disk>
    <interface type='network'>
      <source network='default'/>
      <model type='virtio'/>
    </interface>
    <graphics type='vnc' port='-1' autoport='yes'/>
    <console type='pty'>
      <target type='serial' port='0'/>
    </console>
  </devices>
</domain>
EOF
)

echo "$vm_xml" > "/tmp/${vm_name}.xml"
virsh define "/tmp/${vm_name}.xml"
echo "VM defined: $vm_name"

# Start the VM
virsh start "$vm_name"
echo "VM started: $vm_name"

# Wait for SSH to be available
echo "Waiting for VM to boot..."
sleep 5

echo "Libvirt VM setup complete"
echo "::endgroup::"
