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
| **Sonic (Triage)** | Classifies GitHub Issues and PRs | subagent | GitHub CLI, read-only git |
| **Big (Testing)** | Test strategy, CI workflows, verification | subagent | Full bash for test infrastructure |
| **Shadow (Reviewer)** | Code quality and correctness review | all | Read-only, linters, git inspection |
| **Omega (Security)** | Attack surface analysis, secrets, license compliance | subagent | Read-only, gitleaks, trufflehog |
| **Amy (Task Planner)** | Planning docs, decision docs, CI/CD strategy | subagent | Read/write docs, read-only bash |
| **Vector (Documentation)** | README, changelog, user-facing content | subagent | Read/write docs, read-only git |
| **Espio (Context Curator)** | Planning doc pruning and context hygiene | subagent | File operations only, no bash |
| **Knuckles (Release Manager)** | Releases, PRs, branching, deployment | subagent | Full bash for git operations |

Key permission patterns:

- `external_directory: "*": allow` on all agents (prevents silent stalls in headless runs)
- `task: deny` on all subagents (prevents recursion beyond depth 1)
- Read-only agents (`Shadow`, `Omega`, `Espio`) cannot edit files
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

Team Chaotix supports working on multiple projects simultaneously using git worktrees. Each
worktree is an independent working directory linked to the same repository.

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
5. After implementation, Robotnik fans out Shadow, Omega, and Big in parallel
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

## Tailoring the team for a project

The V1 team is general-purpose. To specialise it for a particular project:

1. **Adjust agent prompts** in `.opencode/agents/` to reference the specific project, its stack,
   and conventions.
2. **Add project-specific workflows** to `.github/workflows/`.
3. **Add project-specific custom actions** to `.github/actions/`.
4. **Update AGENTS.md** with project-specific operating rules.
5. **Create a project directory** outside the team repo where work artifacts are stored.

For example, the Cinnamon Desktop porting project would have:

- `Tails` tuned for Python/C desktop development with Rocky Linux packaging
- `Big` configured with Sparky tests for Cinnamon panel, Nemo, and applets
- `Amy` planning for RPM package builds and SELinux policies
- A project directory at `~/linux/projects/cinnamon_4_rocky10/`

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

All agents use `evo-x2-qwen3.6/Qwen3.6-27B-UD-Q4_K_XL` running on a local llama.cpp instance.

## Updating the team

Changes to the agentic team are committed to this repository and pushed to
`https://github.com/metalllinux/team-chaotix`. To pull updates:

```bash
cd ~/AI/projects/team-chaotix/team-chaotix
git pull origin main
```

**Propagating changes to worktrees:**

After updating the main repo, worktrees need to pull the configuration changes:

```bash
# Update main repo
cd ~/AI/projects/team-chaotix/team-chaotix
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
