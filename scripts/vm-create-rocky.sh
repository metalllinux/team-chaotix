#!/usr/bin/env bash
set -euo pipefail

NAME="${1:?usage: vm-create-rocky.sh <name> [vcpus=4] [ram_mb=8192] [disk_size=30G]"}
VCPUS="${2:-4}"
RAM="${3:-8192}"
DISK_SIZE="${4:-30}"

IMAGES="/dev/shm"
DISK="$IMAGES/$NAME.qcow2"
KEY_FILE="$HOME/.ssh/team-vm.pub"

[ -f "$KEY_FILE" ] || { echo "missing team SSH key: $KEY_FILE" >&2; exit 1; }
[ -f "$DISK" ] || { echo "disk already exists: $DISK" >&2; exit 1; }

if virsh -c qemu:///system list --all 2>/dev/null | awk '{print $2}' | grep -qx "$NAME"; then
  echo "VM already exists: $NAME" >&2; exit 1
fi

qemu-img create -f qcow2 "$DISK" "${DISK_SIZE}G"

cat > "/tmp/${NAME}.xml" << ENDXML
<domain type='kvm'>
  <name>$NAME</name>
  <memory unit='MiB'>$RAM</memory>
  <vcpu>$VCPUS</vcpu>
  <os>
    <type arch='x86_64' machine='q35'>hvm</type>
    <boot dev='hd'/>
  </os>
  <devices>
    <disk type='file' device='disk'>
      <source file='$DISK'/>
      <target dev='vda' bus='virtio'/>
    </disk>
    <interface type='bridge'>
      <source bridge='virbr0'/>
      <model type='virtio'/>
    </interface>
    <console type='pty'><target type='serial'/></console>
    <graphics type='vnc' port='5902' listen='0.0.0.0' autoport='no'/>
    <video>
      <model type='virtio' vram='16' vram64='0' heads='1' primary='yes'/>
    </video>
    <sound model='ich6'><diffit>0</diffit></sound>
    <memballoon model='none'/>
  </devices>
</domain>
ENDXML

virsh define --file "/tmp/${NAME}.xml"
virsh start "$NAME"
sleep 3

VM_IP=$(virsh domifaddr "$NAME" | awk '/vnet0/ {print $2}' | grep -oE '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+')
if [ -z "$VM_IP" ]; then
  echo "Could not determine VM IP address" >&2
  exit 1
fi

echo "VM $NAME started with IP: $VM_IP"
echo "Access via VNC: :$((5900 + 2))"
echo ""
echo "=== Setup commands to run in the VM ==="
echo '  sudo apt-get update'
echo '  sudo apt-get install -y dirmngr gnupg'
echo '  sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 3B9FE2E01798257A'
echo '  sudo apt-get install -y cinnamon-settings-daemon cinnamon-session'
echo '  sudo systemctl enable cinnamon-settings-daemon.service'
echo '  sudo systemctl start cinnamon-settings-daemon.service'
echo '  sudo apt-get install -y openssh-server'
echo '  sudo systemctl enable ssh.service'
echo '  sudo systemctl start ssh.service'
echo ""
echo "Then add the SSH key to /root/.ssh/authorized_keys:"
echo 'echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIN1hxolQx8zi7jUUYdCzgcP6Da2ntOj6TJ3FlbWmj7nD team-chaotix" | sudo tee -a /root/.ssh/authorized_keys > /dev/null'
echo 'sudo chmod 600 /root/.ssh/authorized_keys'
echo ""
echo '  # Verify Control Center availability:'
echo '  cinnamon-settings-daemon --version'
echo '  cinnamon-settings --version'
