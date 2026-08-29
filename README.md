# Team Chaotix

A general-purpose, autonomous software development team built on opencode. Team Chaotix handles any
software development task thrown at it, from initial planning through deployment.

## Architecture

Team Chaotix uses a 10-agent team with strict least-privilege permissions. Each agent has a specific
role and is restricted to only the capabilities it needs.

```
Robotnik (PM) ── delegates to ──┬── Amy (Task Planner)
                                ├── Tails (Coder)
                                ├── Shadow (Reviewer)
                                ├── Omega (Security)
                                ├── Big (Testing)
                                ├── Vector (Documentation)
                                ├── Sonic (Triage)
                                ├── Knuckles (Release Manager)
                                └── Espio (Context Curator)
```

## Agent catalogue

| Agent | Role | Mode | Key permissions |
|---|---|---|---|
| **Robotnik (Project Manager)** | Orchestrates development cycle, delegates work | primary | Full access, delegates to all agents |
| **Tails (Coder)** | All software development and implementation | subagent | Read/write files, full bash |
| **Sonic (Triage)** | Classifies GitHub Issues and PRs | subagent | GitHub CLI, jq, read-only git |
| **Big (Testing)** | Test strategy, CI workflows, verification | subagent | Full bash for test infrastructure |
| **Shadow (Reviewer)** | Code quality and correctness review | all | Read-only code, writes Review section, linters, git inspection |
| **Omega (Security)** | Attack surface analysis, secrets, license compliance | subagent | Read-only code, writes Security section, gitleaks, trufflehog |
| **Amy (Task Planner)** | Planning docs, decision docs, CI/CD strategy | subagent | Read/write docs, read-only bash |
| **Vector (Documentation)** | README, changelog, user-facing content | subagent | Read/write docs, git read + add + commit -m + push origin main + ls-remote, exact ssh verification commands to 192.168.1.106 |
| **Espio (Context Curator)** | Planning doc pruning and context hygiene | subagent | File operations only, no bash |
| **Knuckles (Release Manager)** | Releases, PRs, branching, deployment | subagent | Full bash for git operations |

Key permission patterns:

- `external_directory: "*": allow` on all agents (prevents silent stalls in headless runs)
- `task: deny` on all subagents (prevents recursion beyond depth 1)
- `Shadow`, `Omega`, and `Espio` are read-only on code. Their only writes go to the planning doc,
  into their own section (`Espio` additionally archives within existing sections)
- `Robotnik`, `Amy`, `Sonic` may only edit files under `planning/`
- Bash-restricted agents have explicit allowlists of permitted commands
- No agent can access credential stores directly

## Getting started

### Prerequisites

1. **opencode** installed and configured
2. **Git** with access to `metalllinux/team-chaotix` on GitHub
3. **GitHub token** with `repo` and `workflow` scopes (see below)
4. **Self-hosted GitHub Actions runner** on Rocky Linux (see Runner setup below)

### GitHub authentication

Sonic, Knuckles, and Robotnik use `gh` CLI to read Issues, create PRs, and dispatch workflows. The
token must be available as the `GH_TOKEN` environment variable before launching opencode:

```bash
export GH_TOKEN="ghp_..."
opencode
```

The token needs `repo` and `workflow` scopes. That covers reading Issues and PRs, creating pull
requests, and triggering GitHub Actions workflow runs.

Do not commit the token to the repository. Keep it in `~/.bashrc` or a secret store. Token files
named `githubtoken*.md` are in `.gitignore` to prevent accidental commits.

### Quick start

```bash
# Clone the team configuration
git clone https://github.com/metalllinux/team-chaotix.git
cd team-chaotix/team-chaotix

# Launch opencode (this loads all agents from .opencode/agents/)
opencode

# Hand your first task to Robotnik
# "Port the Cinnamon Desktop to Rocky Linux 10"
```

**Important:** Always launch opencode from the `team-chaotix/team-chaotix/` directory. Launching
from a project directory loads zero custom agents and no `AGENTS.md`, and fails silently. The
project directory is reached through `external_directory`.

### Git worktrees for parallel projects

Team Chaotix supports working on multiple projects using git worktrees. Each worktree is an
independent working directory linked to the same repository. The model endpoint has a single
inference slot (`--parallel 1`), so work in different worktrees shares the model serially:
one agent runs at a time, and the rest queue.

**Creating a worktree for a project:**

```bash
cd ~/AI/projects/team-chaotix/team-chaotix
git worktree add ../worktrees/cinnamon -b worktree/cinnamon
cp -r .opencode ../worktrees/cinnamon/
cp AGENTS.md ../worktrees/cinnamon/
```

**Launching opencode in a worktree:**

```bash
cd ~/worktrees/cinnamon
opencode
```

Each worktree maintains its own branch, so changes don't conflict between projects. The main
repo at `~/AI/projects/team-chaotix/team-chaotix/` remains the source of truth for team
configuration, while worktrees handle project-specific development.

**Listing and removing worktrees:**

```bash
# List all active worktrees
git worktree list

# Remove a worktree
git worktree remove ../worktrees/cinnamon
git branch -D worktree/cinnamon
```

**Multiple simultaneous projects:**

```bash
# Terminal 1: Cinnamon project
cd ~/worktrees/cinnamon
opencode

# Terminal 2: Another project
cd ~/worktrees/another-project
opencode

# Both sessions run independently without file conflicts
```

### How it works

1. The user hands a task to Robotnik
2. Robotnik creates a planning doc and dispatches Amy for planning
3. Amy produces a plan with work breakdown
4. Robotnik dispatches Tails for implementation
5. After implementation, Robotnik dispatches Shadow, then Omega, then Big, one at a time
6. If any findings are raised, Tails fixes them and the cycle repeats
7. Once clean, Vector updates documentation
8. Knuckles handles branching, PR, and merge
9. Espio prunes the planning doc when the task is complete

## Self-hosted runner setup

Team Chaotix requires a self-hosted GitHub Actions runner on Rocky Linux 10.

### Install runner

```bash
# Install prerequisites on Rocky Linux 10
sudo dnf install -y curl git jq podman libvirt-daemon-client libvirt-daemon-config-network qemu-kvm

# Download runner (get latest URL from GitHub repo settings)
curl -o actions-runner.tar.gz -L https://github.com/actions/runner/releases/latest/download/actions-linux-x64-<version>.tar.gz
tar xzf actions-runner.tar.gz

# Configure runner with your GitHub token
./config.sh --url https://github.com/metalllinux/team-chaotix --token <YOUR_TOKEN> \
  --name "local-runner" --unattended --replace

# Install as service
sudo ./svc.sh install
sudo ./svc.sh start
```

### Podman for testing

Rocky Linux ships with Podman. The `docker-test-runner` action uses the Docker CLI,
which is available via `podman-docker`:

```bash
# Install Podman and docker compatibility shim
sudo dnf install -y podman podman-docker

# Add user to libvirt group for VM access
sudo usermod -aG libvirt $USER
newgrp libvirt

# Verify
podman ps
```

### Libvirt for Sparky testing

```bash
# Install libvirt on Rocky Linux 10
sudo dnf install -y libvirt-daemon-system libvirt-daemon-client bridge-utils virtinst

# Start and enable
sudo systemctl enable --now libvirtd

# Add user to libvirt group
sudo usermod -aG libvirt $USER
```

### Sparky setup for Rocky Linux testing

For Sparky testing on Rocky Linux projects:

```bash
# Clone Sparky
git clone https://github.com/rocky-linux/sparky.git
cd sparky

# Install dependencies (Raku for Sparrow tasks)
sudo dnf install -y raku

# Configure Sparky
# See https://docs.rockylinux.org/10/guides/automation/sparky_getting_started/
```

### ISO storage location

Rocky Linux ISOs are stored in `~/ISOs/` on the host system. The Rocky Linux 10.2 ISO used
for testing Cinnamon packages is at:

```
~/ISOs/Rocky-10.2-x86_64-dvd1.iso
```

This location is referenced by `Big` when creating libvirt VMs for Sparky testing.

### Libvirt setup on Rocky Linux 10.2

Reference: https://docs.rockylinux.org/10/guides/virtualization/libvirt-rocky/

```bash
# Install libvirt packages
sudo dnf install -y libvirt-daemon-system libvirt-daemon-client qemu-kvm

# Start and enable libvirt
sudo systemctl enable --now libvirtd

# Add user to libvirt group for VM access
sudo usermod -aG libvirt $USER

# Verify libvirt is running
virsh list

# Create VM from ISO (for testing)
virt-install \
  --name rocky10-test \
  --ram 4096 \
  --vcpus 2 \
  --disk size=20 \
  --cdrom ~/ISOs/Rocky-10.2-x86_64-dvd1.iso \
  --os-type linux \
  --os-variant rocky-10.0 \
  --graphics none \
  --console pty,target_type=serial \
  --extra-args 'console=ttyS0,115200n8 serial'
```

## CI/CD workflows

| Workflow | Trigger | Purpose |
|---|---|---|
| `static-checks.yml` | push, PR | Lint and syntax checks |
| `secret-scan.yml` | reusable | Secret detection (gitleaks + trufflehog) |
| `secret-scan-self.yml` | push, weekly | Scan this repository |
| `test-runner.yml` | dispatch, reusable | Podman or Sparky test execution |
| `planning-doc-gate.yml` | PR | Ensures review/security/testing happened |
| `deploy.yml` | dispatch only | Manual deployment with GPG preflight |

## Custom actions

All actions are hand-written. No Marketplace actions are used (except `actions/checkout`).

| Action | Purpose |
|---|---|
| `checkout-with-cache` | Repository checkout with git bundle caching |
| `setup-deps-cache` | Dependency cache restore/save |
| `docker-cleanup` | Remove stale Podman containers and images |
| `docker-test-runner` | Run tests in Podman containers (via podman-docker shim) |
| `libvirt-vm-setup` | Provision Rocky Linux VM via libvirt |
| `libvirt-cleanup` | Destroy VMs and clean pools |
| `gitleaks-action` | Secret detection with positive control canary |
| `shellcheck-action` | Bash script linting |
| `sparky-test-runner` | Execute Sparky/Sparrow tests in VM |
| `security-audit` | Combined gitleaks + trufflehog + dependency check |

## Secrets management

- **No secrets in the repository.** All credentials live in GitHub Environments.
- Workflow secrets are referenced as `${{ secrets.NAME }}` and nothing else.
- In workflow `run:` blocks, untrusted input is bound to `env:` first, never interpolated.
- `printenv VAR > file` is used instead of `echo "$VAR" > file` when materialising keys.
- If a secret is found committed anywhere, the security agent escalates to the user.

## Active projects

| Project | Repository | Status |
|---|---|---|
| Cinnamon for Rocky Linux 10 | `metalllinux/cinnamon-for-rocky10` | All 10 RPMs built, VM testing pending |

### Cinnamon for Rocky Linux 10

Porting Cinnamon 6.7.x desktop environment to Rocky Linux 10.2. All components build via
meson/ninja and install to `/usr/local`.

**Packages built (10 of 10):**

| Component | Version | RPMs |
|---|---|---|
| cinnamon-desktop | 6.7.2 | main, devel |
| cjs | 6.4.0 | main, devel |
| muffin | 6.7.4 | main, clutter, cogl (+devel) |
| xapps | 3.3.3 | lib (+devel) |
| cinnamon-session | 6.7.3 | main |
| cinnamon-settings-daemon | 6.7.2 | main |
| cinnamon-control-center | 6.7.2 | main, devel |
| nemo | 6.7.4 | main, devel |
| cinnamon | 6.7.4 | main |

**Patches applied:**
- libxdo made optional (not available in EL10 repos)
- gcr-4 API migration (GcrPromptIface → GcrPromptInterface)
- cjs version requirement adjusted (115.0 → 6.4.0 for upstream versioning)

**VM testing:** Pending libvirt VM creation with Rocky Linux 10.2 ISO from `~/ISOs/`.

## License compliance

Agents respect software licenses at all times. When forking or modifying upstream code:

- Verify and comply with the upstream license
- GPL-2.0 code remains GPL-2.0, never relicensed
- Include original copyright headers and license files
- `Omega` checks license headers and compatibility

## External PRs

PRs targeting repositories outside the `metalllinux` GitHub account require human review. The agent
drafts the PR content and stops. The user edits and approves before submission.

PRs within `metalllinux` are handled autonomously.

## Planning documentation

The planning doc is the durable context that makes `compaction.auto: false` safe.

```
planning/
  TASKS.md                          # Master task index
  docs/TASK-XXXX-<slug>.md          # One doc per task
  templates/
    planning-doc.md                  # Planning doc template
    one-pager.md                     # Simple decision doc
    six-pager.md                     # Deep decision doc
```

Each agent writes to its own section in the planning doc. Robotnik reads only `## Status` and
`## Next Actions`. Subagents never round-trip findings through Robotnik.

## Repository structure

```
team-chaotix/
  .github/
    workflows/          # CI/CD workflow definitions
    actions/            # Custom composite actions
    scripts/            # Helper scripts (worktrees, etc.)
  .opencode/
    opencode.json       # Project configuration
    agents/             # Agent definitions (10 files)
  planning/
    TASKS.md            # Master task index
    docs/               # Per-task planning documents
    templates/          # Doc templates
  AGENTS.md             # Shared operating rules (auto-loaded)
  README.md             # This file
  worktrees/            # Git worktrees for parallel projects (auto-created)
```

**Worktrees directory** (`worktrees/`): Each project gets its own worktree directory with
isolated working files. Worktrees are git worktrees that share the same repository but
maintain independent working directories.

## Model

All agents use `Qwen3.8-27B-UD-Q4_K_XL` (EVO-X2 endpoint `evo-x2-qwen3.8-q4`, port 8092, `--parallel 1`).
The endpoint has a single inference slot, so exactly one agent runs at a time and every dispatch
is strictly sequential. The machine that serves this endpoint, a GMKtec EVO-X2, is documented in
the EVO-X2 model host setup section below.

## EVO-X2 model host setup

The agents run on `Qwen3.8-27B-UD-Q4_K_XL`, which a dedicated GMKtec EVO-X2 at 192.168.1.106
serves through llama.cpp. This section documents the reference setup. Every value below is
verified against the reference machine or the team's records of it.

### Hardware and software

The reference machine is a GMKtec EVO-X2 with an AMD Ryzen AI MAX+ 395 (Strix Halo) and the
integrated Radeon 8060S GPU (gfx1151). It has 92 GiB of unified memory (`free -h` on the
reference machine, 2026-08-29), roughly 91 GB of which is visible to the Vulkan device. The
model runs with all layers on that iGPU.

| Component | Reference value |
|---|---|
| OS | Rocky Linux 10.2 |
| Kernel | `7.0.12-1.el10.elrepo.x86_64`. The stock `6.12.0-211.49.1.el10_2` carries an older amdgpu driver and is not used |
| llama.cpp | Vulkan source install under `/usr/local`, version 9671 (commit `c1304d7b2`), built with GNU 14.3.1 |
| Firewall | firewalld |
| Model download | `hf` CLI (`pip install "huggingface_hub==1.19.0"`, the version on the reference machine) |

The binary is a source install under `/usr/local`, not a package (`rpm -qf` reports it owned by
none) and not an upstream release artifact. It is a 16 KB dynamically linked launcher, and
`ldd` resolves the server and the Vulkan backend to shared libraries in `/usr/local/lib64`
(`libllama-server-impl.so`, `libllama-common.so.0`, `libmtmd.so.0`, `libllama.so.0`,
`libggml.so.0`, `libggml-cpu.so.0`, `libggml-vulkan.so.0`, `libggml-base.so.0`), all read on
2026-08-29. The commit exists in upstream `ggml-org/llama.cpp` (checked 2026-08-29), and no
source tree sits in `~/llama.cpp`, `/opt/llama.cpp`, or `/usr/local/src/llama.cpp` (checked the
same day), so whether the build used a pristine upstream checkout or a locally modified one is
not recorded. The working identifiers are the version and the commit, plus the binary's
`BuildID[sha1]` `65396b8511b63de93334ac201f3ef65a75da7f08`.

### Model files

The model lives in `/mnt/data/models/qwen3.8-27b-q4/` with two files. The SHA-256 values were
computed on the reference machine (2026-08-29).

| File | Role | SHA-256 |
|---|---|---|
| `Qwen3.8-27B-UD-Q4_K_XL.gguf` | the 27B model, UD-Q4_K_XL quantization | `3f227079003add2511437e5b1e94812e363385225bf6a9b47b0054a72bc8b01e` |
| `mmproj-F16.gguf` | the vision projector | `cbb841a9ee0636b2ec172f5bb8df2ea8dfeb01e90fe7c6126581d662a0b4e43e` |

Both come from the Hugging Face repo `unsloth/Qwen3.8-27B-GGUF`. The team's `add-ai-model`
skill (`~/.config/opencode/skills/add-ai-model/SKILL.md`) is the standing procedure for adding
models to this box. For this model the download is

```bash
mkdir -p /mnt/data/models/qwen3.8-27b-q4
cd /mnt/data/models/qwen3.8-27b-q4

# Weights first, then the vision projector
hf download unsloth/Qwen3.8-27B-GGUF Qwen3.8-27B-UD-Q4_K_XL.gguf --local-dir .
hf download unsloth/Qwen3.8-27B-GGUF mmproj-F16.gguf --local-dir .
```

Verify the result by SHA-256 (`sha256sum` against the table above) and by the GGUF magic
header. The first line of `xxd` should start with `4747 5546`.

Model endpoints on this box take ports in the 8080-8099 range, and this endpoint takes 8092.
The firewall keeps 8080-8088 and 8090 open for the sibling model endpoints, and the opencode
client carries entries for them, but as of 2026-08-29 the only listener in that range is this
endpoint on 8092, and the team runs one active model at a time (see the systemd unit
subsection).

### The systemd unit

The server runs under a user-level systemd unit, not a system one. Inspect it with
`systemctl --user`, because bare `systemctl` sees nothing. The wedge investigation in TASK-0010
wasted time on exactly that mixup.

The file is `~/.config/systemd/user/llama-server-qwen3.8-27b-q4.service`.

```ini
[Unit]
Description=Llama server for Qwen3.8-27B-UD-Q4_K_XL
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
LimitMEMLOCK=infinity
ExecStart=/usr/local/bin/llama-server --model /mnt/data/models/qwen3.8-27b-q4/Qwen3.8-27B-UD-Q4_K_XL.gguf --mmproj /mnt/data/models/qwen3.8-27b-q4/mmproj-F16.gguf --alias Qwen3.8-27B-UD-Q4_K_XL --host 0.0.0.0 --port 8092 --n-gpu-layers 99 -fa on --parallel 1 -t 32 -tb 32 -ub 2048 -ctk q8_0 -ctv q8_0 --mlock -c 262144
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
```

The whole file was read back from the reference machine on 2026-08-29 and matches this block
line for line. The `ExecStart` line additionally matches the live process (TASK-0010 record),
and the remaining lines match the team's standard unit template in the `add-ai-model` skill.

The flags worth knowing. `--n-gpu-layers 99` pins every layer to the iGPU. `-fa on` turns on
flash attention, which the quantized KV cache (`-ctk q8_0 -ctv q8_0`) requires at startup.
`--mlock` pins the weights in RAM. `--parallel 1` serves a single 262144-token slot, which is
the team's operating point and, per the fit table, the measured ceiling on this hardware. The
fit table was measured on the heavier sibling Q5 model (2026-08-23), so the Q4 ceiling is
unmeasured, though the Q4 weights are smaller. With four slots the llama.cpp fit step silently
degrades the context to 4 x 65536 per slot instead of failing (same Q5 measurement), so check
the effective context in the startup log (`new slot, n_ctx = 262144`) or in `/v1/models`
rather than trusting the command line.

The `add-ai-model` skill defaults its template to `--parallel 4` and warns that one slot queues
every client behind a single generation. That warning is real. A 2026-08-21 fan-out died on
request timeouts against a one-slot endpoint. The reference machine takes the trade anyway,
because only one full-context slot fits and the team's dispatch is strictly sequential (see
Model).

The unit is enabled at the user level, and the reference machine has come back up under it
after host reboots. On any crash, including a GPU wedge, `Restart=on-failure` brings it back
after `RestartSec=5`. The measured restart after a wedge is about 5-11 seconds, most of it the
model reload.

On a fresh setup, enable the unit with

```bash
systemctl --user daemon-reload
systemctl --user enable --now llama-server-qwen3.8-27b-q4.service
systemctl --user status llama-server-qwen3.8-27b-q4.service
```

Run one active model at a time. A sibling 27B endpoint held about 40 GB of the 92 GiB pool
while running (measured), so when a different quantization becomes the team's endpoint, stop
and disable the other `llama-server-*.service` user units.

### Firewall

```bash
sudo firewall-cmd --zone=public --add-port=8092/tcp --permanent
sudo firewall-cmd --reload
sudo firewall-cmd --list-all
```

The reference machine runs firewalld. The live state read on 2026-08-29 is the `public` zone on
`eno1`, with open ports 8092/tcp for this endpoint plus 8080-8088 and 8090 for the sibling
endpoints, and enabled services cockpit, dhcpv6-client, and ssh. The llama-server HTTP API is
unauthenticated, so the firewalld rule is the only access control, and on a network that is not
fully trusted the port should be restricted to the team's segment instead of opened in the
`public` zone.

### The opencode client

The provider entry in `~/.config/opencode/opencode.json`, verified on the reference workstation.

```json
"evo-x2-qwen3.8-q4": {
  "npm": "@ai-sdk/openai-compatible",
  "name": "EVO-X2 Qwen3.8-27B-UD-Q4_K_XL (llama.cpp)",
  "options": {
    "baseURL": "http://192.168.1.106:8092/v1",
    "timeout": 3600000
  },
  "models": {
    "Qwen3.8-27B-UD-Q4_K_XL": {
      "name": "Qwen3.8-27B-UD-Q4_K_XL (EVO-X2)",
      "limit": {
        "context": 262144,
        "output": 131072
      }
    }
  }
}
```

The model id must match the unit's `--alias`. The one-hour request timeout is the team standard
for large models.

### The GPU wedge

The Strix Halo iGPU wedges under sustained compute load. The kernel journal reports
`amdgpu ... ring comp_1.x.0 timeout ... device wedged, but recovered through reset`, the
compute-ring reset kills the Vulkan device, llama-server dies, and every in-flight agent
session is lost, because opencode does not retry the model stream. In early August 2026 the
reference machine logged 26 wedge events in about two days of Q5 load.

**The trigger.** Sustained full-power load accumulates chip-level stress that a compute-ring
reset does not clear. In the failing workloads the chip sits at the roughly 120 W package power
cap with the clock oscillating between 2500 and 2900 MHz, edge temperature drifting from 84 to
92 C, and zero throttle events. This is operation at the power cap, not thermal throttling. A
single cold prefill of about 201k tokens wedges even a fresh chip in about 29 minutes. Hours of
small delta-prompt work (4.5 h measured) produce no in-window wedges, but they do accumulate
stress.

**The power limits.** The box also runs a system-level `ryzenadj.service` (`enabled` and
`active`, read 2026-08-29), a oneshot unit at `/etc/systemd/system/ryzenadj.service` with the
description "Set RyzenAdj APU power limits". It runs `/usr/bin/ryzenadj --fast-limit=100000
--tctl-temp=88` at boot, a 100 W fast power limit and an 88 C TCTL temperature limit, with
`RemainAfterExit=yes` so the unit stays active after the boot run.

**The cascade.** A wedge destroys the KV cache. When a session's context is near 200k tokens,
the retry must cold re-prefill the entire context, which wedges again in 27-29 minutes, and the
loop repeats until the session dies. That loop, not any single wedge, is what killed the
TASK-0008 2c dispatch at 02:33 UTC on 2026-08-27.

**What works.** The auto-restarting unit bounds the cost of a single wedge to about 5-11
seconds of downtime. That is the 5-second restart delay plus the roughly 5.1-second model
reload, and the reload is fast because `--mlock` keeps the weights in RAM and the model store
is NVMe-backed. Keeping requests and session sizes moderate keeps the retry after any wedge
small enough to survive, which is why the team operates in the safe regime of small-context
dispatches. The wedge count is checked before and after runs with the command below. A delta
plus a dead session means a wedge took the session.

```bash
ssh howard@192.168.1.106 'journalctl -k --no-pager | grep -cE "device wedged"'
```

**What does not work.** The runtime sysfs surface is exhausted on the elrepo 7.0.12 driver
build. The performance level file accepts only auto, low, high, and manual (medium is
rejected), manual mode rejects every clock write, there is no hwmon power cap entry, and the
`ppfeaturemask` file does not exist. No knob cuts sustained power while holding speed within
20%. Pinning `low` (600 MHz) measured about 4.5x slower overall (prefill 55.5 vs 255.8 t/s,
decode 2.83 vs 11.87 t/s) and was rejected, because the whole team runs on this endpoint. The
standing decision is to keep `auto`.

**The context window was not reduced.** The unit still requests `-c 262144` and the endpoint
serves it. Wedge avoidance is the auto-restarting unit, `--mlock`, moderate request and
session sizes, and the monitoring command above. The user decision of 2026-08-27 12:13 UTC
accepts the residual risk, leaves the enabled unit as is, and rules out a kernel upgrade
window.

### Verification after setup

1. `systemctl --user status llama-server-qwen3.8-27b-q4.service` shows active and enabled.
2. `sha256sum` of both files in `/mnt/data/models/qwen3.8-27b-q4/` matches the SHA-256 table in
   the Model files subsection.
3. `curl http://192.168.1.106:8092/v1/models` returns the model with `n_ctx` 262144. Poll it,
   because the list is empty during the roughly 12-second load window after each (re)start.
4. The startup log shows `new slot, n_ctx = 262144` with no `n_ctx_seq` warning.
5. `sudo firewall-cmd --list-all` lists 8092/tcp in the public zone.

## Updating the team

Changes to the agentic team are committed to this repository and pushed to
`https://github.com/metalllinux/team-chaotix`. To pull updates:

```bash
cd ~/AI/projects/team-chaotix
git pull origin main
```

**Propagating changes to worktrees:**

After updating the main repo, worktrees need to pull the configuration changes:

```bash
# Update main repo
cd ~/AI/projects/team-chaotix
git pull origin main

# Update each worktree's configuration
for worktree in ~/worktrees/*/; do
    cp -r .opencode "$worktree/"
    cp AGENTS.md "$worktree/"
done
```

Or use the worktree management script:

```bash
# Create worktree with proper configuration
./.github/scripts/manage-worktrees.sh create <project-name>

# List active worktrees
./.github/scripts/manage-worktrees.sh list

# Remove worktree
./.github/scripts/manage-worktrees.sh remove <project-name>
```
