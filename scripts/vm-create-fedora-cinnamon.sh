#!/usr/bin/env bash
# vm-create-fedora-cinnamon — provision a Fedora Cinnamon VM for reference.
#
# Usage: scripts/vm-create-fedora-cinnamon <name> [vcpus=4] [ram_mb=8192]
#   <name>  VM and disk name; convention <project>-<n> (e.g. cinnamon-fedora-1)
#
set -euo pipefail

NAME="${1:?usage: scripts/vm-create-fedora-cinnamon <name> [vcpus=4] [ram_mb=8192]}"
VCPUS="${2:-4}"
RAM="${3:-8192}"
IMAGES=/var/lib/libvirt/images
DISK="$IMAGES/$NAME.qcow2"
KEY="$HOME/.ssh/team-vm.pub"

[ -f "$KEY" ] || { echo "missing team SSH key: $KEY" >&2; exit 1; }
[ ! -f "$DISK" ] || { echo "disk already exists: $DISK" >&2; exit 1; }
if virsh -c qemu:///system list --all | awk '{print $2}' | grep -qx "$NAME"; then
  echo "VM already exists: $NAME" >&2; exit 1
fi
if ! id -nG "$(id -un)" | tr ' ' '\n' | grep -qx libvirt; then
  echo "not in libvirt group; run: sg libvirt -c 'bash $0 $*'" >&2; exit 1
fi

# Use Fedora 40 Cinnamon (latest available in virt-install osinfo)
VERSION="40"
ARCH="x86_64"
URL="https://mirrors.kernel.org/fedora/linux/releases/${VERSION}/Cinnamon/ISOs/${ARCH}/Fedora-${VERSION}-Cinnamon-DVD.iso"
ISO="$IMAGES/Fedora-${VERSION}-Cinnamon-DVD.iso"

# Download Fedora Cinnamon ISO if it doesn't exist
if [ ! -f "$ISO" ]; then
  echo "Downloading Fedora Cinnamon ISO ($VERSION)..."
  curl -L -o "$ISO" "$URL"
  chmod 644 "$ISO"
  echo "ISO downloaded: $ISO ($(du -h "$ISO" | cut -f1))"
fi

# Create disk from scratch
qemu-img create -f qcow2 "$DISK" 40G

# Generate a MAC address (use a fixed one for consistency)
MAC="525400"$(printf '%04x' $RANDOM)$(printf '%04x' $RANDOM)

# Create the domain XML using virt-install directly
virt-install \
  --connect qemu:///system \
  --name "$NAME" \
  --ram "$RAM" --vcpus "$VCPUS" \
  --disk path="$DISK",size=40,bus=virtio \
  --os-variant "fedora40" \
  --network network=default \
  --graphics none \
  --serial pty \
  --cdrom "$ISO" \
  --boot cdrom

# Start the VM
virsh -c qemu:///system start "$NAME"

echo "VM $NAME running (serial console: virsh console $NAME)"
