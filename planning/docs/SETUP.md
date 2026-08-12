# Team Chaotix Development Environment Setup

This document captures every step needed to deploy the Team Chaotix development environment on a
fresh Rocky Linux 10.2 machine. Follow these steps in order to avoid crashes and build failures.

## 1. System prerequisites

**Rocky Linux 10.2 (Red Quartz)** is the only supported host. No other distribution is tested.

### User permissions

The development user must be in the `wheel` group with NOPASSWD sudo:
```
sudo visudo
# Add: %wheel  ALL=(ALL)       NOPASSWD: ALL
```

## 2. CRB repository

Enable the CodeReady Builder repo before any package installation:
```
sudo dnf config-manager --set-enabled crb
```

## 3. Core build tools

```
sudo dnf install -y gcc gcc-c++ make cmake autoconf automake git rpm-build meson ninja-build
```

## 4. Cinnamon build dependencies

Install these in one transaction to avoid dependency resolution issues:
```
sudo dnf install -y \
  gtk3-devel gdk-pixbuf2-devel gobject-introspection-devel systemd-devel \
  libxml2-devel libcanberra-devel pulseaudio-libs-devel xkeyboard-config-devel \
  gettext python3 libseccomp-devel fontconfig-devel cairo-devel pango-devel \
  harfbuzz-devel libX11-devel libXrandr-devel libXdamage-devel libXext-devel \
  libXfixes-devel libXi-devel libXtst-devel libICE-devel libSM-devel \
  libxkbfile-devel glib2-devel atk-devel at-spi2-atk-devel dbus-devel \
  graphene-devel json-glib-devel libwacom-devel pipewire-devel \
  libdrm-devel mesa-libEGL-devel readline-devel iso-codes-devel \
  gudev-devel libxkbcommon-devel libxkbcommon-x11-devel \
  wayland-devel
```

## 5. Wayland protocols (manual install)

Rocky Linux 10 does not ship `wayland-protocols`. Build from source:
```
cd /tmp
git clone --depth 1 https://gitlab.freedesktop.org/wayland/wayland-protocols.git
cd wayland-protocols
sudo mkdir -p /usr/share/wayland-protocols/{stable,staging,include,unstable/{idle-inhibit,keyboard-shortcuts-inhibit,linux-dmabuf,pointer-constraints,pointer-gestures,primary-selection}}
sudo cp -r stable/* /usr/share/wayland-protocols/stable/
sudo cp -r staging/* /usr/share/wayland-protocols/staging/
sudo cp -r include/* /usr/share/wayland-protocols/include/

# Create unstable protocol symlinks (wayland 1.49 renamed many protocols)
sudo ln -sf /usr/share/wayland-protocols/staging/ext-idle-notify/ext-idle-notify-v1.xml \
  /usr/share/wayland-protocols/unstable/idle-inhibit/idle-inhibit-unstable-v1.xml
sudo ln -sf /usr/share/wayland-protocols/staging/ext-session-lock/ext-session-lock-v1.xml \
  /usr/share/wayland-protocols/unstable/keyboard-shortcuts-inhibit/keyboard-shortcuts-inhibit-unstable-v1.xml
sudo ln -sf /usr/share/wayland-protocols/staging/linux-drm-syncobj/linux-drm-syncobj-v1.xml \
  /usr/share/wayland-protocols/unstable/linux-dmabuf/linux-dmabuf-unstable-v1.xml
sudo ln -sf /usr/share/wayland-protocols/staging/cursor-shape/cursor-shape-v1.xml \
  /usr/share/wayland-protocols/unstable/pointer-constraints/pointer-constraints-unstable-v1.xml
sudo ln -sf /usr/share/wayland-protocols/staging/pointer-warp/pointer-warp-v1.xml \
  /usr/share/wayland-protocols/unstable/pointer-gestures/pointer-gestures-unstable-v1.xml
sudo ln -sf /usr/share/wayland-protocols/staging/ext-data-control/ext-data-control-v1.xml \
  /usr/share/wayland-protocols/unstable/primary-selection/primary-selection-unstable-v1.xml

# Create pkgconfig file
sudo tee /usr/lib64/pkgconfig/wayland-protocols.pc > /dev/null << 'WPC'
prefix=/usr
datadir=${prefix}/share
Name: wayland-protocols
Description: Wayland protocols
Version: 1.49
pkgdatadir=${datadir}/wayland-protocols
wayland_protocols_stable_dir=${pkgdatadir}/stable
wayland_protocols_include_dir=${pkgdatadir}/include
wayland_protocols_staging_dir=${pkgdatadir}/staging
WPC
```

## 6. mozjs115 (manual install)

mozjs115 is not in Rocky Linux 10 repos. Extract headers from Fedora 44 RPM:
```
curl -sL "https://kojipkgs.fedoraproject.org/packages/mozjs115/115.29.0/2.fc44/x86_64/mozjs115-devel-115.29.0-2.fc44.x86_64.rpm" \
  -o /tmp/mozjs115-devel.rpm
cd /tmp && rpm2cpio mozjs115-devel.rpm | cpio -idmv
sudo cp -r /tmp/usr/include/mozjs-115 /usr/include/
sudo cp /tmp/usr/lib64/pkgconfig/mozjs-115.pc /usr/lib64/pkgconfig/
sudo ln -sf /usr/lib64/gjs/libmozjs-115.so /usr/lib64/libmozjs-115.so
sudo ldconfig
```

Verify: `pkg-config --modversion mozjs-115` should output `115.29.0`.

## 7. Podman + podman-docker

```
sudo dnf install -y podman podman-docker
sudo systemctl enable --now podman
```

## 8. libvirt + QEMU/KVM

Package name is `libvirt-daemon` on EL10 (not `libvirt-daemon-system`):
```
sudo dnf install -y libvirt-daemon libvirt-daemon-config-network libvirt-daemon-driver-qemu \
  qemu-kvm bridge-utils virt-install
sudo systemctl enable --now libvirtd
sudo usermod -aG libvirt $USER
```

## 9. CRITICAL: Prevent system crash (ninja parallelism)

**This is the most important step.** Without it, `ninja` will default to 16 parallel jobs on
a 16-core machine, consuming 24+ GB RAM and triggering an OOM kill crash.

```
# Limit meson/ninja to 2 parallel jobs
mkdir -p ~/.config/meson
echo 'maxjobs = 2' > ~/.config/meson/meson.conf

# Limit RPM builds to 2 parallel jobs
echo '%_smp_mflags -j2' >> ~/.rpmmacros
```

Always use `ninja -j2` explicitly for safety.

## 10. Git configuration

```
git config --global user.name "Team Chaotix"
git config --global user.email "chaotix@metallinux.dev"
```

Set git credential for GitHub (replace TOKEN):
```
git config --global url."https://<user>:<TOKEN>@github.com/".insteadOf "https://github.com/"
```

## 11. Raku (for Sparky testing)

Raku is not in Rocky Linux 10 repos. Install from pre-built binary:
```
curl -sL "https://rakudo.org/dist/rakudo-moar-2026.07-01-linux-x86_64-gcc.tar.gz" \
  -o /tmp/rakudo-moar.tar.gz
tar xzf /tmp/rakudo-moar.tar.gz -C /opt/
ln -s /opt/rakudo/bin/* /usr/local/bin/
```

## 12. GitHub CLI

```
sudo dnf install -y gh
gh auth login --with-token <<< "$GITHUB_TOKEN"
```

## Muffin build options

Muffin requires specific options on Rocky Linux 10 (missing wayland protocols):
```
meson setup builddir \
  -Dnative_backend=false \
  -Dudev=false \
  -Dstartup_notification=false \
  -Dwayland=false \
  -Degl=enabled
```

For the `-Dwayland=false` build, muffin will compile as X11-only window manager, which is
sufficient for the Cinnamon desktop environment.

## Memory monitoring during builds

Watch memory usage during builds:
```
watch -n 5 'free -h'
```

If RAM usage exceeds 75%, stop the build: `kill %1`.

## Verification checklist

After setup, verify:
- [ ] `gcc --version` outputs GCC 14.x
- [ ] `meson --version` outputs 1.4.x
- [ ] `ninja --version` outputs 1.11.x
- [ ] `pkg-config --modversion mozjs-115` outputs 115.29.0
- [ ] `pkg-config --modversion wayland-protocols` outputs 1.49
- [ ] `podman ps` runs without error
- [ ] `virsh list --all` runs without error
- [ ] `cat ~/.config/meson/meson.conf` shows `maxjobs = 2`
- [ ] `cat ~/.rpmmacros | grep smp` shows `-j2`
