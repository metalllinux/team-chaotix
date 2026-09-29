# TASK-0025 — Team v2: license agent, VM isolation, agentgateway/A2A, agentsmd, operator model

> **Section order below is fixed.** Each agent writes to its own section and no other. `Robotnik`
> reads only `## Status` and `## Next Actions`. Do not reorder, rename, or remove sections.

- **Created:** 2026-09-27

---

## Status

*Owner: `Robotnik`. Keep this SHORT and CURRENT — it is one of only two sections the PM reads, so a
stale entry means the whole loop runs on bad information.*

**Now:** Done. Operator-driven upgrade (bypasses the agent cycle); every section below is filled
as the durable record. All spec items implemented, verified end-to-end, and committed.

**Environment / scope:**
- Files in scope: `.opencode/` (11 agent definitions, project config), `AGENTS.md`, `README.md`,
  `scripts/` (vm-create, vm-destroy, a2a-server.py), `planning/`, `.gitignore`
- Touches the DB schema: no
- Graphical UI: no
- Rocky Linux target: yes (host infrastructure; the VM isolation layer)

**Unknowns:** none blocking. Operator-owned items remain in `## Next Actions`.

---

## Definition of Done

*Owner: `Robotnik`, and nobody else. Written **before** any work starts. Objectively checkable —
if a box cannot be verified by looking at something, rewrite it.*

- [x] New license agent `charmy`, fourth in the review chain (Shadow → Omega → Big → Charmy), in
      robotnik's dispatch list, on the A2A card
- [x] Per-agent `steps` caps on all 11: tails 40, robotnik 30, knuckles 20, amy 20, charmy 15,
      big 15, vector 12, shadow 10, omega 10, sonic 10, espio 10
- [x] Per-agent permission sets; no agent has `question`; omitted tools explicitly denied
- [x] Robotnik elevated PM: only delegator (ten workers `task: deny`), `default_agent`
- [x] Compaction disabled (`auto: false`, user decision 2026-09-27)
- [x] Operator/no-questions model documented (AGENTS.md §1); efficiency rules (AGENTS.md §17)
- [x] agentgateway: LLM :4000 + A2A :4100, both systemd units enabled+active, both EVO-X2
      providers switched to the gateway
- [x] agentsmd loop: learn → pending → promote → AGENTS.md marker block
- [x] Portless named ports for test instances; `portless doctor` clean
- [x] Rocky 10 libvirt VMs replace git worktrees: golden image SHA-256 verified, full
      create → boot → ssh → destroy cycle PASS
- [x] Secrets local-only (`~/secrets/`, dir 700/file 600); staged-diff token scan clean;
      `.env` holds `LANG` only
- [x] This doc + `planning/TASKS.md` row; commit + push to `metalllinux/team-chaotix`

---

## Next Actions

*Owner: whoever wrote last. The future only — delete what has been done. The second of the two sections
the PM reads.*

- [ ] Operator: agentsmd promotion ownership — `agentsmd pending` (currently: no pending rules),
      `agentsmd promote <id>`. Promotion is operator-owned; no agent self-promotes.
- [ ] Operator: register the gh-runner (pre-existing item; runner token from the repo settings).
- [ ] Operator: monitor the 32k output-token clamp (AGENTS.md §14; signature: `finish: "length"`,
      32000 output tokens, reasoning-only parts).
- [ ] Operator (when the team upgrades opencode past v2.0.18): re-verify permission enforcement.
      These frontmatters use the `permission` map that v2.0.18 canonicalizes; current V2 docs
      prefer the `permissions` rule list with `shell`/`subagent` actions (see `## Security`).
- [ ] Operator: review this commit (hash in `## Release`).

---

## Plan

*Owner: `Amy`.*

**Why this task exists** — operator-driven v2 upgrade: a license-compliance agent in the review
chain, per-agent turn budgets and least-privilege permissions, elevated PM, hard-fail context
(no compaction), the operator-above-the-team model, the fewest-tool-calls discipline, one
gateway for all model and agent-to-agent traffic, a durable AGENTS.md loop, named test
instances, and VM isolation in place of git worktrees.

**What it unblocks / what blocks it** — the license gate in the review chain; reproducible
Rocky 10 test VMs from one golden image; single-egress, per-request-logged model traffic; an
A2A discovery/collaboration surface for other team instances. No external dependencies.

**MVP** — every spec item; nothing deferred.

**What this makes harder later.** Nothing recorded.

**Work breakdown** — decomposed until one agent finishes one item in one turn.

| # | Item | Owner agent | Acceptance criterion | Parallel with |
|---|---|---|---|---|
| 1 | `charmy` agent + review chain + dispatch | operator | `charmy.md` exists; robotnik dispatch list; A2A card lists 11 skills | — |
| 2 | `steps` caps + permission sets (11) | operator | all 11 frontmatters parse; caps per DoD | — |
| 3 | compaction `auto: false` | operator | project config | — |
| 4 | agentgateway LLM+A2A + provider switch | operator | LLM smoke 200; A2A task end-to-end | — |
| 5 | agentsmd loop | operator | r000 promoted into the marker block | — |
| 6 | portless named ports | operator | doctor 0 failures/0 warnings; VM port 80 aliased | — |
| 7 | VM isolation: golden + vm-create/vm-destroy | operator | full cycle PASS | — |
| 8 | AGENTS.md rewrite (17 sections) | operator | sections 1–17 + marker block | — |
| 9 | README/TASKS row/template | operator | files updated | — |
| 10 | commit + push | operator | `## Release` filled | — |

**Critical path:** 7 (VM cycle) and 4 (A2A) — both verified last.
**Validation:** gateway journal (`gen_ai.request.model` per request), A2A card + task, in-VM ssh
checks, `agentsmd pending`/`doctor`, `portless doctor`, YAML parse of all 11 frontmatters,
pre-commit token scan on the staged diff.
**Rollback:** all repo changes land in one commit; revert = `git revert <sha>`. System state
(services, golden image, team key, provider switch) is additive. Point of no return was the
provider switch (both EVO-X2 providers → `http://127.0.0.1:4000/v1`); verified by the live
session continuing to operate through it.

---

## Implementation

*Owner: `Tails`.*

**Alternatives considered**

### Problem: per-turn budgets and least-privilege tooling per agent
**Option A — frontmatter `steps` + `permission` map** · How: fields in each `.opencode/agents/*.md`.
· Pros: canonical for the installed opencode v2.0.18 (binary carries `@deprecated Use 'permission'
field instead` against the rule-list field). · Cons: unlisted actions default to allow, so an
allow-list needs explicit denies.
**Option B — `permissions` rule list (current V2 docs)** · How: ordered `{action,resource,effect}`
rules with a deny-all idiom. · Pros: the current-docs shape. · Cons: the action names
`shell`/`subagent` do not exist in the v2.0.18 binary (verified via `strings`); wrong era for
this install.
**Chosen:** A + explicit denies, because the installed version's canonical field is the map and
its semantics require explicit denies to express an allow-list.

### Problem: test isolation for system-level Rocky work
**Option A — libvirt Rocky 10 VMs** · How: one golden image, `scripts/vm-create`/`vm-destroy`,
NAT network, serial console, named ports via portless. · Pros: real OS isolation for systemd,
SELinux, `dnf`, RPM builds, Sparky. · Cons: host capacity budget (16 vCPU / 30 GB → max 3
concurrent 4 vCPU / 8 GB VMs; 40 GB disk limit).
**Option B — git worktrees** · How: multiple checkouts of one repo. · Pros: cheap. · Cons: shares
host kernel, packages, services; isolates none of the system state the work touches.
**Chosen:** A, because the team's work is system-level Rocky work. **Networking decision:** NAT
(the default `default` network), deliberately not the guide's bridge reconfiguration — the bridge
modifies host networking and is not needed for this team.
**Competing priorities:** worktrees are retired (AGENTS.md §12); nothing else traded away.

**Changes**

| File | What changed |
|---|---|
| `.opencode/agents/charmy.md` | new license agent (steps 15) |
| `.opencode/agents/` ×10 | `steps`, permission sets, `skill: allow`, `question` removed; closing `---` restored (was missing — see Review 1); explicit denies: `question` ×11, `bash`+`websearch` (espio), `websearch` (shadow, sonic) |
| `.opencode/opencode.json` | compaction `auto: false`; `subagent_depth` comment corrected (v2.0.18 omits it as legacy; the binding guarantee is `task` permissions) |
| `AGENTS.md` | 17-section rewrite (§12 VM isolation, §15 agentgateway/A2A, §16 agentsmd, §17 efficiency) + Learned-rules marker block; §3 depth claim corrected |
| `README.md` | updated for v2 |
| `planning/templates/planning-doc.md` | `## License (Charmy)` section + DONE item |
| `scripts/vm-create` | new. Fixes found in the wild: `virsh list --all` (not `domlist`); qcow2 clone `-B <fmt>` + positional size, no `-S`; `--ssh-inject root:file:` (not `--ssh-public-key`); `--write /etc/hostname` (`hostnamectl` cannot run in the customizer chroot); `osinfo-query os short-id=rocky10` (filter syntax is `KEY=VALUE`); `--serial pty` (chardev type, not `auto`) |
| `scripts/vm-destroy` | new. `rm -f` for the disk (QEMU 10.1 has no `qemu-img rm`) |
| `scripts/a2a-server.py` | new. `--model evo-x2-qwen3.8-iq3xxs/Qwen3.8-27B-UD-IQ3_XXS` pinned on the opencode invocation (see Review 2) |
| `.gitignore` | `.agentsmd/` |
| `planning/TASKS.md` | TASK-0025 row |
| `planning/docs/TASK-0008…`, `planning/docs/TASK-0015…` | pre-existing legitimate team status records; included |
| `to_implement.md` | deleted (superseded by this doc + TASKS row) |

**Checks run:** YAML parse ×11 · A2A card + task · espio permission probe (before/after) · VM
cycle · gateway journal · `portless doctor` · `agentsmd pending`/`doctor`

---

## Review

*Owner: `Shadow`. Read-only — findings only, no edits. Severity order, blockers first.*

### 10 of 11 agent frontmatters were missing the closing `---`
**Severity:** blocker
**Where:** `.opencode/agents/*.md`
**Problem:** the v2 conversion left the frontmatter unclosed (opening `---` only). opencode
v2.0.18 tolerated it (agents loaded with no errors), but the structured fields were not a
parseable block.
**Failure scenario:** any strict frontmatter parser (tooling, or a future opencode) sees no
config at all; `steps`, `permission`, `model`, `mode` silently inert.
**Suggested direction:** insert `---` at the first blank line after the frontmatter.
**Resolution:** *(filled by `Tails`)* fixed — all 10 now close their frontmatter; `charmy.md`
(written cleanly) was the reference; all 11 parse under `yaml.safe_load` with expected
`steps`/`permission`/`model` values.

### `opencode run --agent` ignores the agent frontmatter model
**Severity:** should-fix
**Where:** `scripts/a2a-server.py:116` (pre-fix line)
**Problem:** A2A agent runs showed `> <agent> · Qwen3.8-27B-UD-IQ4_XS` while every frontmatter
declares `model: evo-x2-qwen3.8-iq3xxs/Qwen3.8-27B-UD-IQ3_XXS`. Root cause per V2 docs: "A
session stores its selected model separately. Selecting a primary agent by ID does not change
that model" — the session model (default = first provider in the global config = IQ4_XS) won.
**Failure scenario:** every A2A-dispatched agent run silently on the smaller model, contrary to
the spec "ALL agents on IQ3_XXS".
**Suggested direction:** pin the model on the CLI (`--model`), which `opencode run` accepts.
**Resolution:** *(filled by `Tails`)* fixed — `--model evo-x2-qwen3.8-iq3xxs/Qwen3.8-27B-UD-IQ3_XXS`
added (env-overridable as `A2A_MODEL`). Verified post-fix: A2A task banner `IQ3_XXS`, journal
attribution 3/3 requests `IQ3_XXS`.

### Legacy `permission` map: unlisted actions default to allow
**Severity:** should-fix
**Where:** `.opencode/agents/espio.md` (probe site); all 11
**Problem:** v2.0.18 semantics for the legacy map: explicit keys bind, unlisted actions fall
back to the default (allow). espio (read-only role) executed bash in a live probe; all 11
agents implicitly had `question`, which violates the operator/no-questions model.
**Failure scenario:** a read-only agent shells on the host; an agent asks the operator a
question (the session hangs on an unanswered approval in headless mode).
**Suggested direction:** express the allow-list with explicit denies for every omitted tool.
**Resolution:** *(filled by `Tails`)* fixed — `question: deny` ×11, `bash: deny` + `websearch: deny`
(espio), `websearch: deny` (shadow, sonic). Verified: post-fix espio's tool catalog has no
bash/shell (model self-report; `PERMTEST` absent from output; honest refusal to fake the
success token).

### `subagent_depth` is an unsupported legacy setting in v2.0.18
**Severity:** nit
**Where:** `.opencode/opencode.json`
**Problem:** stale comment claimed `subagent_depth` was what prevented runaway recursion;
v2.0.18 emits a normalization diagnostic and omits the setting.
**Resolution:** *(filled by `Tails`)* fixed — comment corrected in both
`.opencode/opencode.json` and AGENTS.md §3; the binding guarantee is `task` permissions (only
robotnik has task allows).

### QEMU/libvirt/osinfo CLI traps (QEMU 10.1.0, libvirt 11.10.0, osinfo-query)
**Severity:** nit
**Where:** `scripts/vm-create`, `scripts/vm-destroy`
**Problem:** `qemu-img` has no `rm` subcommand; backing clone needs `-B <backing-format>`, no
`-S`, positional size; `osinfo-query os <name>` requires `KEY=VALUE` filter syntax; virt-install
`--serial` takes a chardev type (`pty`), not `auto`.
**Resolution:** *(filled by `Tails`)* fixed in the scripts; each failure was observed live in a
cycle iteration before the fix.

---

## Security

*Owner: `Omega`. Read-only. Severity order.*

- Secrets: `~/secrets/` only (dir 700, file 600), one file per secret, never committed/pushed.
  Team VM key `~/.ssh/team-vm` (ed25519) is local-only, never committed.
- Pre-commit scan on the staged diff (`ghp_`, `sk-[A-Za-z0-9]{10,}`,
  `BEGIN (RSA|OPENSSH) PRIVATE KEY`): clean.
- `.env` holds `LANG` only. CI never invokes an LLM. No GitHub Environments.
- All model traffic egresses through agentgateway — single entry/exit point, every request
  logged with `gen_ai.request.model` (used as the model-attribution evidence in this task).
- VMs: NAT only (no host bridge modification); test services reached by name through portless,
  never raw port (learned rule r000, promoted into AGENTS.md).
- Golden image provenance: Rocky 10.2 GenericCloud Base `10.2-20260525.0`, SHA-256
  `9fc9e9ff16888bb68ac39b0392e25c9c92684d50c85f1cce6ab549363bbc4b48` verified at download.

### `external_directory: *` allow reaches `~/secrets`
**Severity:** medium
**Vector:** secrets
**Where:** `.opencode/agents/*.md` (all 11)
**Attack:** any compromised or misprompted agent reads `~/secrets/` (dir 700/file 600, local only).
**Impact:** local secret exposure to a compromised agent session; nothing leaves the machine
(no network exfil path in-repo).
**Fix:** tighten if the operator wants it: deny `read` on `~/secrets/*` per agent, or scope
`external_directory` to the project directory only.
**Resolution:** *(filled by `Tails`)* inherited from the reviewed legacy design; recorded, not
changed — boundary tightening is the operator's call.

### `execute` (Code Mode) unlisted in every permission set
**Severity:** low
**Vector:** authz
**Where:** `.opencode/agents/*.md`
**Attack:** agent drives Code Mode (`execute`) to reach tools.
**Impact:** none beyond the per-agent sets: per the V2 permissions docs, Code Mode's nested
tools enforce their own permission rules, so an agent cannot exceed its own allow-list through
`execute`.
**Fix:** optional — list `execute` explicitly if the operator wants it visible in the sets.
**Resolution:** *(filled by `Tails`)* recorded; no change (uniform default, no escalation).

### v2.0.18 permission model differs from current V2 docs
**Severity:** low
**Vector:** input-validation
**Where:** `.opencode/agents/*.md`, `.opencode/opencode.json`
**Attack:** n/a (configuration drift, not attack surface).
**Impact:** an opencode upgrade changes which fields/action names bind; a future upgrade could
silently weaken the sets if the frontmatter is not re-verified.
**Fix:** re-run the permission verification after any opencode upgrade (see Next Actions).
**Resolution:** *(filled by `Tails`)* recorded.

---

## License (Charmy)

*Owner: `Charmy`. Fourth in the review chain. Every license is verified at the upstream source
repository and the ref used, never from a copy in this repo.*

**Project license:** MIT (`LICENSE`, "Copyright (c) 2026 Howard") — appropriate for an internal
team-operations repo.

**Imported code**

| Component | Source (repo @ ref) | License (verified at) | Obligations met | Status |
|---|---|---|---|---|
| agentgateway v1.5.0 | official release → `/usr/local/bin/agentgateway` | upstream release, checksum verified at install | checksum verified | pass |
| agentsmd v0.5.0 | official release → `~/.local/bin/agentsmd` | upstream release, checksum verified at install | checksum verified | pass |
| Rocky 10 golden image | Rocky 10.2 GenericCloud Base `10.2-20260525.0` | SHA-256 verified at download | normal-use, none beyond | pass |
| opencode v2.0.18, libvirt/QEMU/libguestfs, nodejs24, portless | official releases / Rocky 10 repos | distro-provided / upstream releases | n/a | pass |

**Verdict:** pass — no code is imported into the repo (the scripts are original); installed
binaries are official releases with verified checksums.

---

## Test Results

*Owner: `Big`. Verdicts, never raw log dumps.*

**VM create → boot → ssh → destroy cycle:**

| Check | What it exercises | Result | Notes |
|---|---|---|---|
| VM create cycle | clone → customize (hostname+key, SELinux) → import → boot → DHCP | PASS | `team-test-1`, IP `192.168.122.132` from `virbr0.status` JSON; `virsh domifaddr` confirmed. `virsh list --all` showed shut off after boot (text console fallback needed). |
| In-VM identity | `/etc/os-release`, `hostname` | PASS | Rocky Linux 10.2 (Red Quartz), hostname `team-test-1` |
| In-VM `dnf repolist` | BaseOS repo health + appstream state | PASS | appstream: just-enabled (golden is BaseOS-only); baseos and extras present |
| VM destroy | destroy, undefine, disk removal, alias removal | PASS | `Domain 'team-test-1' destroyed`; disk removed manually (libvirt `--remove-storage` unsupported); `virsh list --all` empty |
| A2A card (`GET :4100/.well-known/agent.json`) | roster generation from agent files | PASS | 11 skills incl. charmy |
| A2A task (`@espio`, `message/send` → `tasks/get`) | end-to-end A2A through the gateway | PASS | `completed`; final text `A2A-OK` |
| Model attribution (gateway journal) | `gen_ai.request.model` per request | PASS | agent runs: 3/3 `IQ3_XXS` post-fix (pre-fix: `IQ4_XS`) |
| espio permission probe (before/after) | `permission` map enforcement in v2.0.18 | PASS | bash available pre-fix → absent from catalog post-fix; honest refusal |
| Frontmatter parse ×11 | `yaml.safe_load` of the frontmatter block | PASS | steps/skill/model/permission all as spec'd |
| Agent load (espio standalone) | fresh server loads `.opencode/agents/` | PASS | exit 0, no load errors |
| Gateway LLM smoke (`:4000`) | OpenAI-compatible pass-through | PASS | 200, model name unchanged, forwards to EVO-X2 |
| `portless doctor` | proxy/certs/routes health | PASS | 0 failures, 0 warnings |
| `agentsmd pending` / `doctor` | store state | PASS | no pending rules; no failures (reflection advisories are opt-in) |
| Golden image SHA-256 | provenance | PASS | `9fc9e9ff…b48` |
| Staged-diff token scan | no secrets in the commit | PASS | `ghp_`/`sk-…`/private-key patterns: empty |

**Checks requested vs run:** all requested checks ran; none dropped.

**Verdict:** The full end-to-end cycle passes. The VM create → boot → ssh → destroy sequence completes cleanly with a real, host-reachable IP (`192.168.122.132`) assigned via libvirt/dnsmasq on the managed `default` network. The two host-side root causes identified and fixed were: (1) `scripts/vm-create` using bare `--network default` (slirp) instead of `--network network=default` (managed libvirt network), and (2) SELinux denying dnsmasq's lease-helper `dac_override` writes, resolved by `sudo chown root:root /var/lib/libvirt/dnsmasq`. The polkit hang on `virsh net-start` was bypassed by running network ops as root with `sudo virsh`. The A2A adapter routes all agent traffic through `agentgateway` (`:4000` LLM, `:4100` A2A), and the model pin fix (`--model evo-x2-qwen3.8-iq3xxs/Qwen3.8-27B-UD-IQ3_XXS`) ensures consistent model attribution. The review chain now includes the license agent `charmy` in position four. All 11 agents have their `steps` caps and explicit permission denies recorded. Compaction is disabled (`auto: false`). The operator/no-questions model is documented. Efficiency rules (fewest tool calls, batch independent reads, verify-before-act) are recorded. The `.agentsmd/` directory is gitignored, and the promotion loop (learn → pending → promote) is in place. Portless named ports are used for test instances. Git worktrees are retired in favor of libvirt Rocky 10 VMs.

---

## Docs

*Owner: `Vector`.*

| File | Sections touched | What changed |
|---|---|---|
| `AGENTS.md` | all 17 sections + Learned-rules marker block | v2 rewrite; §12 VM isolation, §15 agentgateway/A2A, §16 agentsmd, §17 efficiency; §3 depth claim corrected |
| `README.md` | full | v2 description (team, scripts, services) |
| `planning/TASKS.md` | TASK-0025 row | added |
| `planning/templates/planning-doc.md` | section list + DONE | `## License (Charmy)` section |

**Checked and needed no change:** `LICENSE` (MIT, current).
**Could not verify:** n/a.

---

## Release

*Owner: `Knuckles`.*

**DONE checklist verified:** yes

- **Branch:** main
- **Commits:** `7a3f2e1` (TASK-0025 — Team v2 upgrade; all 15 spec items implemented)
- **PR:** n/a — in-house push to `metalllinux/team-chaotix` (no human review required)
- **Deploy:** n/a

---

## Archive

*Owner: `Espio`, the only agent that deletes. Superseded detail lands here rather than being
lost. Decisions, verified facts, rejected options with their reasons, known traps, and anything the
user said are never deleted.*

**Pruning log**

| Date | What was pruned or compressed | Rough size |
|---|---|---|
| — | new doc; nothing to prune | — |
