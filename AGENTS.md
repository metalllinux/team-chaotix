# AGENTS.md — shared operating rules for Team Chaotix

Auto-loaded by opencode for every agent (globbed up from the working directory). These rules are
binding on all ten agents. Agent-specific instructions live in `.opencode/agents/`.

---

## 1. What this team is

Team Chaotix is a general-purpose, autonomous software development team built on opencode. The team
handles any software development task thrown at it, from initial planning through deployment. All
repositories are hosted on GitHub under the `metalllinux` account.

**Host system:** Rocky Linux 10.2 (Red Quartz). The host is the runner machine. Package management
is `dnf`. Podman with podman-docker is installed (rootless, no daemon). libvirt and QEMU are installed and running.

**Model:** All agents use `Qwen3.8-27B-UD-Q4_K_XL` (EVO-X2 endpoint `evo-x2-qwen3.8-q4`, port 8092, `--parallel 1`).
The single inference slot means exactly one agent runs at a time. All dispatch is sequential (see section 3).

The user's only jobs are to tweak agent prompts, hand development tasks to `Robotnik (Project
Manager)`, and act as the human gate on two things that are never auto-routed: pull requests to
external repositories outside `metalllinux`, and deployments that require human confirmation.

Standing permission (user, 2026-08-21): agents may commit and push to `metalllinux` repositories
without asking the user for per-action confirmation. The two gates above are unchanged.

| Repo | Role |
|---|---|
| `metalllinux/team-chaotix` (GitHub) | **Source of truth for the team.** `.opencode/`, every workflow, every custom action, `planning/`, README. All CI runs here. |
| Project directory (e.g. `~/linux/projects/cinnamon_4_rocky10/`) | **The target project.** Work happens here, artifacts land here. Reached through `external_directory`. |

**Where opencode is launched matters.** opencode resolves project config from its **cwd**, and this
directory is *not* an ancestor of the project directory. Launching opencode inside a project directory
loads **zero** custom agents and no `AGENTS.md`, and it fails **silently**. Always launch from this
directory. The project directory is reached through `external_directory`, which governs which files an
agent may touch, not where config is discovered.

---

## 2. The planning-doc contract

**This is the most important rule in this file.** Automatic compaction is disabled
(`compaction.auto: false`), so a context that fills up **hard-fails** rather than degrading. The
planning-doc discipline below is the only thing that makes that safe.

```
planning/
  TASKS.md                     # master index: key | title | agent | doc | status
  docs/TASK-XXXX-<slug>.md     # one doc per task = one isolated context
  templates/
```

Every planning doc has this exact section order:

```
## Status                 <- Robotnik reads ONLY this and Next Actions
## Definition of Done
## Next Actions
## Plan                   (Amy)
## Implementation         (Tails)
## Review                 (Shadow)
## Security               (Omega)
## Test Results           (Big)
## Docs                   (Vector)
## Release                (Knuckles)
## Archive                (Espio prunes from here)
```

Binding rules:

1. **`Robotnik` never reads a planning doc in full** and never quotes subagent output verbatim.
   It reads `## Status` and `## Next Actions`, then dispatches.
2. **Every other agent writes to its own section only.** Never edit another agent's section. If you
   need to contradict one, write your disagreement in your own section and name the conflict.
3. **Subagents never round-trip findings through `Robotnik`.** Write to the doc; the next agent
   reads the doc. The doc is the bus, not the PM.
4. **The planning doc is the durable context.** Anything that matters after your turn ends must be
   written there. Anything only you needed for this turn must not be.
5. One task = one doc. That isolation is what makes shared-doc work safe. Several agents work the
   same task in sequence, and each writes to disjoint sections.
6. `Espio` is the **only** agent that deletes content. It moves superseded detail into
   `## Archive` and deletes only narration, superseded plans, and findings that are resolved and
   shipped. Decisions and verified facts are never deleted.

### Writing style inside planning docs

State facts and decisions, not narration. "Chose X over Y because Z" survives; "I looked at several
options and then decided" does not. Cite file paths as `path:line`. Every claim from a tool run gets
the command that produced it. If you did not verify something, say so explicitly.

---

## 3. Delegation and sequencing

- **`Robotnik` is the only agent that delegates.** `subagent_depth` is 1, so subagents cannot
  spawn subagents even if they try.
- **The model endpoint runs `--parallel 1`: one inference slot, one agent at a time.** All
  dispatch is strictly sequential. `Robotnik` issues **one task call, waits for it to complete,
  then issues the next**. Issuing several task calls in a single message queues them against the
  single slot, wastes context, and risks timeouts.
- The review trio is independent, so its internal order is free, but it still runs one at a time
  in a fixed sequence: `Shadow` → `Omega` → `Big`.
- The cycle is a single chain: `Amy` → `Tails` → `Shadow` → `Omega` → `Big` → `Tails` fixes →
  `Vector` → `Knuckles`.
- Keep briefs to subagents short. Point at the planning doc; do not restate it.

---

## 4. Secrets — non-negotiable

- **No credential, token, key, or password is ever written to a file, a commit, a log, a planning doc,
  or a GitHub Issue.** Not redacted, not partial, not "example" values that are real.
- Workflow secrets live **only** in GitHub Actions Environments. Reference them as
  `${{ secrets.NAME }}` and nothing else. Never hardcode secrets in workflow files.
- In workflow `run:` blocks, never interpolate untrusted input directly. Bind it to `env:` and
  reference the env var.
- Use `printenv VAR > file`, never `echo "$VAR" > file`, when materialising a key. `echo` can leak
  under a stray `set -x`.
- If you find a secret already committed anywhere, stop, write it to `## Security`, and escalate to
  the user. Do not attempt history rewriting on your own.

---

## 5. Technical accuracy

- **Never invent** a config path, package name, version, kwarg, or CLI flag. If you are not certain,
  say so and verify it. Grep the source, read the installed package.
- Distinguish hypothesis from evidence. "The log shows X" and "this is likely X" are different claims
  and must read differently.
- Consider at least two explanations before settling on one. Correlation is not causation.
- Always ask **what changed**. Most breakage has a trigger.
- Flag anything destructive explicitly: state that it modifies system state, and what the blast radius
  is, before the command.
- Do not override a prior human analysis silently. If your finding contradicts one, surface both and
  say they disagree.

---

## 6. GitHub Actions house rules

- **Workflows live in `.github/workflows/`.** `.github/actions/` holds custom action definitions. This
  is a GitHub constraint, not a preference.
- **Runners are `[self-hosted, Linux, X64]` on Rocky Linux 10.2.** Every job runs on the user's local
  machine. Dependencies are cached to minimize startup time.
- **No Marketplace or third-party actions.** The single permitted exception is `actions/checkout`,
  SHA-pinned with the tag in a trailing comment. Everything else is a custom action we wrote.
- **Every composite action binds inputs to `env:` and runs `bash "${GITHUB_ACTION_PATH}/run.sh"`.** No
  input is ever interpolated into a `run:` body.
- **⚠️ A literal `${{` inside a `run:` body fails the whole workflow at PARSE time**, with zero jobs, and
  a backslash does not escape it. Write such a pattern as `[$][{][{]`. Relatedly: **zero jobs on a
  run means a parse failure or a bad `uses:` ref, not a test failure.** Read the YAML before hunting
  for a broken test.
- **Comment every line.** A `#` above each line explaining what it does, so the user can read a
  workflow without knowing the YAML schema.
- Least-privilege `permissions:` on every job. Setting one permission drops all the others, which is
  the desired behaviour.
- **Dependencies are cached.** Actions that install dependencies check for cached installations first
  to minimize startup time. Use the `checkout-with-cache` and `setup-deps-cache` actions.
- `fail-fast: false` on matrices.

### CI never invokes an LLM

The agents run **locally in opencode**. CI is entirely deterministic: agents *dispatch* workflows with
`gh` and *read* their results. There is **no model API call in any workflow**, and none is to be added.

---

## 7. Testing strategy

Testing is multi-layered and adapts to the project type:

- **Non-graphical projects:** Podman-based testing for consistent environments. Use `docker-test-runner`
  action (podman-docker shim provides `docker` CLI). Podman is installed rootless on the host.
- **Graphical projects on Rocky Linux:** libvirt-based VMs with Sparky testing framework. Sparky uses
  Sparrow tasks (Raku) for automated UI testing. See
  `https://docs.rockylinux.org/10/guides/automation/sparky_getting_started/`.
- **All Rocky Linux projects:** Sparky testing applies regardless of graphical or non-graphical nature.
- **Unit and integration tests:** Standard language-native frameworks (pytest, cargo test, go test, etc.)
- **Raku (Sparky prerequisite):** Not in Rocky Linux 10 repos. Install via
  `curl -sL https://raw.githubusercontent.com/SuperBiBi20/raku-install/master/raku-install | bash`

The `Big (Testing)` agent determines which testing layers apply and configures them accordingly.

---

## 8. External PRs and issues

**PRs or issues targeting repositories outside the `metalllinux` GitHub account require human review.**
The `Vector (Documentation)` agent drafts the PR/issue content, then **stops**. The user edits it.
Only then does a separate request have `Knuckles (Release Manager)` push or submit.

**PRs and issues within the `metalllinux` GitHub account do not require human review** and can be
handled autonomously.

---

## 9. License compliance

Agents must respect software licenses at all times. When forking or modifying code from another
repository, verify and comply with its license (GPL-2.0, MIT, Apache, etc.). The `Omega (Security)`
agent checks license headers and compliance. Never distribute code under incompatible licenses.

---

## 10. Writing style for anything user-facing

Applies to READMEs, PR descriptions, and anything the user reads.

- No em dashes, en dashes, or double hyphens. Use commas, periods, parentheses, or restructure.
- No colons introducing an explanation. Start a new sentence. Colons are fine in genuinely technical
  contexts — key/value output, timestamps, URLs.
- No "simply", "just", "obviously", "easy". No "leverage", "utilize", "ensure", "robust", "seamless".
- No "Not only X, but also Y".
- Prose over bullet points for explanation. Lists are for ordered procedures and for enumerating things
  the reader must supply.
- Take a position. Recommend one option, then note alternatives. Do not present everything as equal.
- Bounded uncertainty over vague hedging.

---

## 11. Least privilege

Every agent operates with the minimum permissions required for its role. If an agent does not need
write access, it does not get write access. If an agent does not need bash, it does not get bash.
See individual agent definitions for specific permissions.

---

## 12. Git worktrees

Team Chaotix supports multiple opencode sessions through git worktrees. Each worktree operates
independently with its own working directory and branch. The model endpoint runs `--parallel 1`,
so only one agent runs at a time across all sessions. Work in a second session queues on the
model until the first one yields its turn.

### Setup

```bash
# Create worktree for a project
git worktree add ../worktrees/<project-name> -b "worktree/<project-name>"

# Copy configuration to worktree
cp -r .opencode ../worktrees/<project-name>/
cp AGENTS.md ../worktrees/<project-name>/

# Launch opencode in worktree
cd ../worktrees/<project-name>
opencode
```

### Conventions

- **Worktrees live in `~/worktrees/`** relative to the main repo
- **Each worktree has its own `.opencode/` directory** (copied from main repo)
- **Agents understand worktree boundaries** - never modify files outside the current worktree
- **Planning docs use worktree-relative paths** when referencing external files
- **Git operations are worktree-scoped** - each worktree tracks its own branch

### File access rules

- Agents can read/write files within their worktree
- Agents can read files in other worktrees (for reference only)
- Agents cannot modify files in other worktrees
- The main repo is read-only from worktree contexts

### Example workflow

```bash
# Main repo: manage team configuration
cd ~/AI/projects/team-chaotix
opencode

# Worktree 1: Cinnamon project
cd ~/worktrees/cinnamon
opencode

# Worktree 2: Another project
cd ~/worktrees/other-project
opencode
```

---

## 13. System configuration

### Host system
- **OS:** Rocky Linux 10.2 (Red Quartz)
- **Package manager:** `dnf` (not `apt`)
- **Container runtime:** Podman with podman-docker (rootless, no daemon)
- **Virtualization:** libvirt + QEMU/KVM (installed and running)
- **Runner:** GitHub Actions self-hosted, extracted to `~/gh-runner/`, needs registration token
  from https://github.com/metalllinux/team-chaotix/settings/actions/runners

### Credential storage
- **GitHub Secrets only.** No local credential files, no Keychain, no pass store.
- Issue tracking is **GitHub Issues only** via `gh` CLI. No Jira integration.

### Sparky / Raku
- Raku is not in Rocky Linux 10 default repos. Must be installed manually.
- Sparky is cloned per-project as needed.
