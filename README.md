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
3. **Self-hosted GitHub Actions runner** on Rocky Linux (see Runner setup below)

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
  .opencode/
    opencode.json       # Project configuration
    agents/             # Agent definitions (10 files)
  planning/
    TASKS.md            # Master task index
    docs/               # Per-task planning documents
    templates/          # Doc templates
  AGENTS.md             # Shared operating rules (auto-loaded)
  README.md             # This file
```

## Model

All agents use `evo-x2-qwen3.6/Qwen3.6-27B-UD-Q4_K_XL` running on a local llama.cpp instance.

## Updating the team

Changes to the agentic team are committed to this repository and pushed to
`https://github.com/metalllinux/team-chaotix`. To pull updates:

```bash
cd ~/ai/projects/team-chaotix/team-chaotix
git pull origin main
```
