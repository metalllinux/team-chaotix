# TASK-0013 — README: GMKtec EVO-X2 + Qwen 3.8 UD-Q4_K_XL model host setup

> **Section order below is fixed.** Each agent writes to its own section and no other. `Robotnik`
> reads only `## Status` and `## Next Actions`. Do not reorder, rename, or remove sections.

- **Created:** 2026-08-28

---

## Status

*Owner: `Robotnik`. Keep this SHORT and CURRENT — it is one of only two sections the PM reads, so a
stale entry means the whole loop runs on bad information.*

**Now:** user request (2026-08-27): a README section in `metalllinux/team-chaotix` documenting how
to set up the GMKtec EVO-X2 with `Qwen3.8-27B-UD-Q4_K_XL` as the team's model host — systemd
settings (user supplied the unit file; it matches the reference machine), firewall, model
download from Hugging Face, directory layout, opencode client config, and GPU-wedge avoidance
guidance. `Vector` turn complete 2026-08-28: section written (new `## EVO-X2 model host setup`,
README lines ~398-601, plus a cross-reference sentence in `## Model`), `## Docs` filled, unverified
items marked (unit file beyond `ExecStart`, live firewalld state, ryzenadj purpose, binary
provenance — all settle via `ssh howard@192.168.1.106`, which Vector's loaded bash set blocks;
see TASK-0014). The uncommitted work was shipped by Tails on the TASK-0014 turn in commit
`9e1f0c9` (mixed-scope commit, stated in the message), pushed to main; verification in
`ad9632c`, local HEAD == remote main. Review chain complete 2026-08-29: Shadow round 1 (1
should-fix, 2 nits) + Omega round 1 (3 lows) all fixed in `1da994a`; Shadow round 2 (1 nit)
fixed in `0a58642`; rounds verified clean (Shadow r3, Omega r2). The four "Could not verify"
items were settled by read-only ssh on the fix turn (unit file line-for-line, live firewalld
state, ryzenadj purpose self-evident and now documented, binary provenance partly settled).
Final pushed state `c4cbf63`. All DoD boxes ticked 2026-08-29; `Knuckles` verified DONE = yes and
recorded `## Release` 2026-08-29 (`2678b28` + `0d45aca`, final remote state `0d45aca`). `Espio`
pruning is the last step. The exact ssh verification commands are pinned rules in `Vector`'s bash
set (TASK-0014), usable from the next opencode restart.

**Environment / scope:**
- Files in scope: `README.md` (team-chaotix repo, `/home/howard/AI/projects/team-chaotix/`)
- Touches the DB schema: no
- Graphical UI: no
- Rocky Linux target: yes (reference host runs Rocky Linux 10.2 + elrepo kernel)

**Verified reference-machine facts (Robotnik, via `ssh howard@192.168.1.106`, 2026-08-27/28):**
- GMKtec EVO-X2 at 192.168.1.106; Radeon 8060S iGPU (gfx1151, Strix Halo); 92 GiB RAM;
  Rocky Linux 10.2; kernel `7.0.12-1.el10.elrepo.x86_64`.
- llama-server `version: 9671 (c1304d7b2)`, built with GNU 14.3.1, at
  `/usr/local/bin/llama-server` (Vulkan backend; frozen flags include `--n-gpu-layers 99 -fa on`).
- Model dir `/mnt/data/models/qwen3.8-27b-q4/` (`Qwen3.8-27B-UD-Q4_K_XL.gguf` +
  `mmproj-F16.gguf`); endpoint port 8092, `--host 0.0.0.0`.
- **User-level** systemd unit `llama-server-qwen3.8-27b-q4.service` in
  `~/.config/systemd/user/`, **enabled** (exact file supplied by the user and matching the
  machine; auto-restart demonstrated in TASK-0010 — ~5 s after a GPU wedge).
- firewalld running, `public` zone on `eno1`; open ports include 8092/tcp (plus 8080–8088,
  8090, 8084 for the other model endpoints); services: cockpit, dhcpv6-client, ssh.
- opencode client: provider entry `evo-x2-qwen3.8-q4` in `~/.config/opencode/opencode.json`
  (baseURL `http://192.168.1.106:8092/v1`, model `Qwen3.8-27B-UD-Q4_K_XL`, context 262144,
  output 131072).
- Model import procedure: team skills `~/.config/opencode/skills/add-ai-model/SKILL.md` and
  `~/.config/opencode/skills/new-model-import/SKILL.md` (EVO-X2-specific, incl. the Hugging
  Face source).
- GPU wedge record: `planning/docs/TASK-0010-evox2-gpu-wedge-fix.md` — characterization in
  checkpoint 3.1 (power-cap stress; single ~201k cold prefill wedges a fresh chip in ~29 min;
  small delta-prompt work ran 4.5 h clean), runtime surface exhausted in 3.3 (no sysfs knob
  works on the elrepo 7.0.12 driver build; `low` = 4.5x slower, rejected), fresh-chip repro in
  3.4, user decision (accept risk) in the 2026-08-27 12:13 UTC Status entry.
- The reference machine also runs a system-level `ryzenadj.service` — purpose unverified;
  `Vector` verifies on the machine before documenting; omit if not verifiable.

**Unknowns:** the exact HF repo for the model (should be in the skills; verify there, do not
guess); the ryzenadj configuration; whether the llama.cpp binary is a release build or local
build (ask/verify; record what is found, mark the rest unverified).

---

## Definition of Done

*Owner: `Robotnik`, and nobody else. Written **before** any work starts. Objectively checkable —
if a box cannot be verified by looking at something, rewrite it.*

- [x] `README.md` has a new section on setting up a GMKtec EVO-X2 model host with
      `Qwen3.8-27B-UD-Q4_K_XL`, covering: hardware/OS/kernel requirements; the llama-server
      binary (Vulkan build, the verified version); downloading the model from Hugging Face per
      the team skills; the model directory layout; the user-level systemd unit (exact file +
      user-level enablement + what it does on boot/wedge); the firewall rule for 8092/tcp
      (firewalld, public zone); the opencode provider entry; and the GPU-wedge section (what a
      wedge is, the verified characterization, what works — unit auto-restart, `--mlock`,
      moderate request sizes, the monitoring command — what does not — the exhausted runtime
      sysfs surface — and the correction that the context window was **not** reduced,
      `-c 262144` stays).
- [x] Every factual claim in the section verified against the reference machine
      (`ssh howard@192.168.1.106`) or cited from a team artifact (planning doc, skills,
      opencode.json); no invented paths, flags, or versions; unverified items marked as such.
      (Four read-only ssh verifications run 2026-08-29 on the fix turn; remaining marked item:
      pristine-vs-modified build tree state.)
- [x] AGENTS.md §10 writing style applied (no em/en dashes, no colons introducing an
      explanation, prose over bullets for explanation, take a position).
- [x] `Shadow`: no unresolved blockers or should-fix findings in `## Review`.
- [x] `Omega`: no unresolved findings above `low` in `## Security`.
- [x] `Big`: N/A — docs-only change, no executable code (recorded here).
- [x] Committed + pushed to `metalllinux/team-chaotix` main; local HEAD == remote HEAD
      (verified with `git ls-remote`; final state `c4cbf63`, Knuckles re-verifies in `## Release`).

---

## Next Actions

*Owner: whoever wrote last. The future only — delete what has been done. The second of the two sections
the PM reads.*

- [x] `Knuckles` (complete 2026-08-29): DONE verified yes; `## Release` recorded (`2678b28` +
      `0d45aca`); final remote state `0d45aca`; deferred `ef884e4` verification carried.
- [x] `Espio` (pruning complete 2026-08-29): superseded `## Docs` "Could not verify" list +
      "Commit status" paragraph and the full text of the resolved round-1/2 `## Review` findings
      moved to `## Archive`; `## Review` now carries one-liners with the fixing shas (`1da994a`,
      `0a58642`). Decisions, verified facts, and source pointers untouched.
- [ ] Ship the pruning (both TASK-0013 and TASK-0014 docs): commit with prefix `TASK-0013:`
      stating scope, push to main, verify local HEAD == remote HEAD with `git ls-remote`, and
      record the commit sha in both docs' pruning logs. Espio's loaded permission set is
      `bash: deny` (`.opencode/agents/espio.md:17`), so the dispatch's ship step cannot run from
      this role; a bash-capable agent (Tails or Knuckles) must ship under the standing push
      permission (user, 2026-08-21).

---

## Plan

*Owner: `Amy`.*

**Why this task exists** — the user request or issue it serves.
**What it unblocks / what blocks it** — including dependencies outside this repo.
**MVP** — the smallest version that delivers value, and what is deferred.
**What this makes harder later.**

**Work breakdown** — decomposed until one agent finishes one item in one turn.

| # | Item | Owner agent | Acceptance criterion | Parallel with |
|---|---|---|---|---|
| 1 | | | | |

**Critical path:**
**Validation:** which files, which checks, which pages need a human look. Name them.
**Rollback:** how we detect failure, the exact revert, and where the point of no return is.

---

## Implementation

*Owner: `Tails`.*

**Fix turn 2026-08-29** (dispatch in `## Next Actions`): fixes Shadow's should-fix + two nits and
Omega's three lows, runs the four read-only ssh verifications from `## Docs` "Could not verify"
plus the supporting read-only checks the fix list requires, and upgrades the README's
marked-unverified items where they now verify. Strict constraint honored. Every remote command
was read-only, nothing on the host was created, modified, or restarted.

**Alternatives considered**

### Problem: the README's marked-unverified items and three Omega lows all need values read from the reference machine, and the should-fix needs the current listener state
**Option A — run all four named verifications plus the supporting read-only checks in one turn (`sha256sum`, `pip show`, `free -h`, `ss -tln`, `ldd`/provenance follow-ups) and rewrite every affected README passage against the live output** · How: `ssh howard@192.168.1.106` with read-only commands only, each recorded below with its result. · Pros: every affected value is machine-verified as of 2026-08-29, the "Could not verify" list settles in one pass, and the GB/GiB nit gets the machine reading Shadow offered instead of a unit copy. · Cons: the turn runs more remote commands than the four named (mitigated. every extra command is read-only and directly settles a named finding, and each is listed below so the surface is auditable).
**Option B — run only the four named verifications and leave the pin, the hashes, and the unit sourced from the 2026-08-27/28 Status** · How: skip `pip show`, `sha256sum`, `free -h`. · Pros: minimal remote surface. · Cons: Omega's fix list explicitly forbids guessing the pin ("Read the version from the reference machine ... rather than guessing, per AGENTS.md §5") and requires the hashes "computed once from the verified files on the reference machine", so two of the three lows would ship unfilled, and the nit would stay a unit copy.
**Chosen:** A, because the fix list names the reference machine as the source of the pin and the hashes, and the extra commands are read-only under the task's strict constraint.
**Competing priorities:** minimal remote surface was traded for settled values. The trade is bounded. every command is recorded below, none writes, and the host's standing state is unchanged.

**Remote verification record** — all commands run 2026-08-29 as `ssh howard@192.168.1.106 '<cmd>'` (key auth, `BatchMode`), read-only. No command wrote, installed, stopped, or restarted anything on the host.

1. `cat ~/.config/systemd/user/llama-server-qwen3.8-27b-q4.service` (named verification 1)
   - Output: the file matches the README block line for line, all 14 lines (`Description`, `After`, `Wants`, `Type`, `LimitMEMLOCK`, `ExecStart`, `Restart`, `RestartSec`, `WantedBy` and the section headers).
   - Settled. The whole file is verified on the machine, not just `ExecStart`. README upgraded (the note now says the whole file was read back and matches line for line).
2. `sudo firewall-cmd --list-all` (named verification 2)
   - Output. zone `public` (default, active), `interfaces: eno1`, `services: cockpit dhcpv6-client ssh`, `ports: 8080/tcp 8081/tcp 8082/tcp 8083/tcp 8087/tcp 8085/tcp 8086/tcp 8088/tcp 8090/tcp 8084/tcp 8092/tcp`, `protocols:` empty, `forward: yes`, `masquerade: no`, no rich rules, no source-ports.
   - Settled. The live state matches the README's open-port set (8092 plus 8080-8088 plus 8090) and service set (cockpit, dhcpv6-client, ssh) exactly. README upgraded (the Firewall subsection now states the live state read 2026-08-29).
3. `systemctl cat ryzenadj.service` (named verification 3)
   - Output. unit at `/etc/systemd/system/ryzenadj.service` with `Description=Set RyzenAdj APU power limits`, `After=systemd-modules-load.service`, `Type=oneshot`, `ExecStart=/usr/bin/ryzenadj --fast-limit=100000 --tctl-temp=88`, `RemainAfterExit=yes`, `WantedBy=multi-user.target`.
   - Follow-up (read-only). `systemctl is-enabled ryzenadj.service` → `enabled`; `systemctl is-active ryzenadj.service` → `active`.
   - Settled. The purpose is self-evident from the unit (set APU power limits at boot), so per the task instruction it is documented. New `**The power limits.**` paragraph in the README's GPU-wedge subsection.
4. Binary provenance inspection of `/usr/local/bin/llama-server` (named verification 4)
   - `ls -l /usr/local/bin/llama-server` → `-rwxr-xr-x. 1 root root 16712 Jun 16 22:12 /usr/local/bin/llama-server`
   - `file /usr/local/bin/llama-server` → `ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=65396b8511b63de93334ac201f3ef65a75da7f08, for GNU/Linux 3.2.0, not stripped`
   - `rpm -qf /usr/local/bin/llama-server` → `file /usr/local/bin/llama-server is not owned by any package`
   - `/usr/local/bin/llama-server --version` → `version: 9671 (c1304d7b2)` and `built with GNU 14.3.1 for Linux x86_64` (matches the recorded facts in `## Status`)
   - `ldd /usr/local/bin/llama-server` → the server and backend code resolve to shared libraries in `/usr/local/lib64` (`libllama-server-impl.so`, `libllama-common.so.0`, `libmtmd.so.0`, `libllama.so.0`, `libggml.so.0`, `libggml-cpu.so.0`, `libggml-vulkan.so.0`, `libggml-base.so.0`); the 16 KB executable is the launcher
   - `ls -d ~/llama.cpp /opt/llama.cpp /usr/local/src/llama.cpp` → none of the three exist (no source tree in the usual build locations)
   - Running process. `pgrep -x llama-server` → pid 17168; `readlink /proc/17168/exe` → `/usr/local/bin/llama-server` (the serving process runs exactly this binary)
   - Upstream commit check (local, web). `https://github.com/ggml-org/llama.cpp/commit/c1304d7b2` resolves; commit title "ui: add source toggle to mermaid and svg blocks (#24652)". The version identifier is anchored to an existing upstream commit.
   - Settled in part. The binary is a source install under `/usr/local` (not package-owned, launcher plus shared libraries, not an upstream release artifact), built from a tree whose commit exists upstream. Whether the checkout was pristine or locally modified remains unrecorded, and the README says so (the provenance paragraph was upgraded from "not recorded whether release or local build" to the verified layout plus that one remaining unknown).
5. Supporting checks (read-only) for the named findings
   - `which hf` → `/home/howard/.local/bin/hf`; `pip show huggingface_hub` → `Version: 1.19.0`, `Location: /home/howard/.local/lib/python3.12/site-packages`. Settles the pin for Omega low 2. README row now reads `pip install "huggingface_hub==1.19.0"`.
   - `sha256sum /mnt/data/models/qwen3.8-27b-q4/Qwen3.8-27B-UD-Q4_K_XL.gguf /mnt/data/models/qwen3.8-27b-q4/mmproj-F16.gguf` → `3f227079003add2511437e5b1e94812e363385225bf6a9b47b0054a72bc8b01e` (weights) and `cbb841a9ee0636b2ec172f5bb8df2ea8dfeb01e90fe7c6126581d662a0b4e43e` (mmproj). Settles Omega low 3. Both values are in the README's Model files table, and `sha256sum` is item 2 of the verification list.
   - `free -h` → `Mem: 92Gi total` (37Gi used, 34Gi free, 21Gi buff/cache, 55Gi available). Settles Shadow's GB/GiB nit with the machine reading. README now says 92 GiB with the source and date; the "92 GB pool" mention in the unit subsection was aligned to 92 GiB.
   - `ss -tln` → listeners `0.0.0.0:8092`, `0.0.0.0:22`, `[::]:22`, `*:9090`. In the 8080-8099 model range the only listener is 8092. Settles the current listener state for the should-fix. The README sentence now states only verified facts (firewall keeps the sibling ports open, client entries exist, only 8092 listens as of 2026-08-29, one active model at a time).

**Changes**

| File | What changed |
|---|---|
| `README.md` (the `## EVO-X2 model host setup` section only) | Shadow should-fix. The "also serves the sibling quantizations on 8080-8088 and 8090" sentence (former `README.md:447`) now states only verified facts, per Shadow's suggested direction. Shadow nit 1. "92 GB of unified memory" (former `README.md:407`) → "92 GiB" with the `free -h` source and date; the same fact in the "Run one active model at a time" paragraph aligned to "92 GiB pool". Shadow nit 2. The ceiling claim (former `README.md:479-481`) now carries the Q5 attribution. The fit table is measured on the heavier Q5 sibling (2026-08-23), the Q4 ceiling is stated as unmeasured. Omega low 1. One sentence added to the Firewall subsection. the HTTP API is unauthenticated, the firewalld rule is the only access control, and on a network that is not fully trusted the port should be restricted to the team's segment. Omega low 2. `pip install huggingface_hub` pinned to `huggingface_hub==1.19.0`, read from the reference machine (not guessed). Omega low 3. SHA-256 column added to the Model files table (computed on the reference machine), the download-verification sentence now includes `sha256sum`, and a `sha256sum` item added to the verification list (now item 2). Upgrades. The unit note states the whole file was read back from the machine on 2026-08-29 and matches line for line; the Firewall subsection states the live firewalld state read 2026-08-29; the provenance paragraph records the verified install layout (16 KB launcher plus `/usr/local/lib64` shared libraries, not package-owned, commit confirmed to exist upstream, no source tree in the usual locations) and the one remaining unknown (pristine vs locally modified checkout); a new `**The power limits.**` paragraph documents `ryzenadj.service` because its purpose is self-evident from the unit |
| `planning/docs/TASK-0013-evox2-readme-setup.md` | This `## Implementation` record; the six round-1 finding Resolution lines filled (the fix-sha reference is completed in the follow-up commit per the TASK-0011 convention). Also ships, unedited by Tails, Robotnik's `## Next Actions` bookkeeping and the `## Review` / `## Security` sections as written by Shadow and Omega |
| `planning/docs/TASK-0014-vector-bash-permissions.md` | Ships, unedited by Tails, Robotnik's bookkeeping (amended DoD box, `## Next Actions`, `## Review` round 2, `## Security` round 2). Tails fills the eight outstanding Resolution lines in the same commit. H-1 stays open (user-owned, AGENTS.md §4), H-2 and H-3 are resolved against `ef884e4` per Omega round 2, the four low items are recorded as resolved or residual, and the DoD-box nit is fixed by the box rewording this commit ships |

**Checks run**

- `git diff ef884e4 -- README.md` reviewed line by line. Only the `## EVO-X2 model host setup` section changed; the `## Model` cross-reference and every other part of the README are untouched.
- AGENTS.md §10 on the file. `grep -n '—\|–' README.md` → no matches (exit 1); banned-word grep (`simply|just|obviously|easy|leverage|utilize|ensure|robust|seamless|Not only`) → no matches in `README.md`; colons inside the section (lines 398-627) appear only in the JSON block, timestamps, and URLs, all permitted technical contexts.
- Cross-check. Every new factual claim in the section maps to a line in the remote verification record above (unit file, firewalld state, ryzenadj plus its enabled/active state, provenance chain, pip version, the two hashes, `free -h`, `ss -tln`, the upstream commit page).
- Compile / linter / harness. n/a, docs-only change (`Big` is N/A per `## Definition of Done`).

**Commit and remote verification** — per the TASK-0011 convention (`planning/docs/TASK-0011-default-model-q4kxl.md:219`. "follow-up commit records the sha here"):

- Fix commit (README + 2 planning docs, 3 files, +284/-78): `1da994a` (full
  `1da994a12321dda2a3329d41e8775272b13ced76`), pushed with `git push origin main` →
  `ef884e4..1da994a  main -> main`.
- `git ls-remote origin main` after the push, actual output:
  `1da994a12321dda2a3329d41e8775272b13ced76	refs/heads/main`.
  Local HEAD (`git rev-parse HEAD`) `1da994a12321dda2a3329d41e8775272b13ced76` == remote HEAD. PASS.
- This follow-up commit (planning docs only) completes the fix-sha references in the six
  TASK-0013 finding Resolution lines and the one TASK-0014 DoD-box-nit Resolution line. After
  its push, local HEAD == remote HEAD is re-verified with `git ls-remote origin main`, and that
  final output line is the state `Knuckles` re-verifies for `## Release`.

**Settlement of `## Docs` "Could not verify"** — Vector's section is left untouched per the section rule; this record supersedes it.
- Unit file text beyond `ExecStart` → settled, verified (record item 1).
- Current live firewalld state → settled, verified (record item 2).
- `ryzenadj.service` purpose → settled, self-evident from the unit, documented (record item 3).
- llama.cpp binary provenance → settled in part (record item 4). The pristine-vs-locally-modified question stays marked as unrecorded in the README, per the task instruction to leave it marked if it stays unclear.

**Final fix turn 2026-08-29** (Shadow round-2 nit in `## Review`): the 100 W fast limit in
the `**The power limits.**` paragraph (`README.md:582-586` pre-fix) sits two paragraphs below
the roughly 120 W sustained cap in `**The trigger.**` (`README.md:574-580`) with no bridge
between them. Fixed with one bridging sentence appended to the ryzenadj paragraph, using the
"mark the relationship unverified" option rather than a claim about which limit governs. No
other line of the README touched.

**Alternatives considered**

### Problem: two power figures adjacent without a bridge, a new reader may see a contradiction
**Option A — state which limit governs sustained load** · How: add a sentence asserting the 100 W fast limit is transient-only and that sustained load runs against the ~120 W cap. · Pros: most informative; a reader reasoning about wedge causes or power tuning gets a complete picture. · Cons: no team artifact establishes the relationship on the machine. The TASK-0010 record shows PPT pinned at 119-120 W for the entire 32.7 min of the stress run under `auto` (`planning/docs/TASK-0010-evox2-gpu-wedge-fix.md:471-475`), but that is a measurement under the standing configuration, not a statement that the ryzenadj fast limit does not bind, and the TASK-0010 runs predate the ryzenadj paragraph. Asserting it would be an unverified claim (AGENTS.md §5); settling it properly needs a machine run, which this turn does not scope.
**Option B — one bridging sentence that marks the relationship unverified** · How: append one sentence to the ryzenadj paragraph stating that the ~120 W figure is the sustained PPT cap measured in the TASK-0010 stress run, that the 100 W fast limit is what `ryzenadj` configures on the reference machine, and that whether the fast limit is in effect under sustained load is unverified. · Pros: every clause is already sourced (the first to the TASK-0010 stress run, the second to the `## Implementation` remote record item 3 read 2026-08-29), no new machine verification needed, and the reader is told exactly what is and is not known. · Cons: the reader still cannot tell which cap governs sustained load until someone verifies it on the machine.
**Chosen:** B, per the dispatch instruction to mark the relationship unverified rather than claim which limit governs. It is also the only option whose every clause is already verified.
**Competing priorities:** informativeness traded for verification. The sentence names the gap precisely ("whether the fast limit is in effect under sustained load"), so the next turn that has the ssh channel knows exactly what to settle.

**Changes**

| File | What changed |
|---|---|
| `README.md` | One sentence appended to the `**The power limits.**` paragraph (now `README.md:582-589`). The roughly 120 W figure in the trigger paragraph is identified as the sustained PPT cap measured in the TASK-0010 stress run, the 100 W fast limit as what `ryzenadj` configures on the reference machine, and whether the fast limit is in effect under sustained load as unverified. No other line of the README touched |
| `planning/docs/TASK-0013-evox2-readme-setup.md` | This `## Implementation` record. Also ships, unedited by Tails, the round-2 additions already in the working tree (Shadow's `## Review` round 2, including the nit this turn fixes, and Omega's `## Security` round 2). `git diff` shows exactly those two hunks, 138 insertions, so no `## Status` or `## Next Actions` bookkeeping is part of this commit |

**Checks run**

- Scope. `git diff HEAD -- README.md` shows a single hunk, the appended sentence inside the `**The power limits.**` paragraph. No other line of the README changed.
- AGENTS.md §10 on the file. No em or en dashes anywhere in `README.md` (grep, no matches), no banned words (word-boundary grep, no matches; the substring hit on "adjusted" at line 330 is outside the section and predates this change), and the new sentence carries no colon introducing an explanation. Prose, not bullets.
- Cross-check. The ~120 W sustained PPT claim traces to `planning/docs/TASK-0010-evox2-gpu-wedge-fix.md:471-475` (PPT pinned 119-120 W for the entire 32.7 min under `auto`), the source the trigger paragraph already carries. The 100 W fast limit traces to the `## Implementation` remote record item 3 (the verified `ryzenadj.service` `ExecStart`, read 2026-08-29). The unverified marking adds no new factual claim.
- Compile / linter / harness. n/a, docs-only change (`Big` is N/A per `## Definition of Done`).

**Commit and remote verification** — per the TASK-0011 convention (`planning/docs/TASK-0011-default-model-q4kxl.md:218`. "follow-up commit records the sha here"):

- Fix commit (README + this planning doc, 2 files, +178/-1, mixed scope stated in the message,
  prefixed `TASK-0013:`): `0a58642` (full `0a58642da8c5111102ed7efa978e3f90f36cbe76`), pushed
  with `git push origin main` → `109ee7c..0a58642  main -> main`.
- `git ls-remote origin main` after the push, actual output:
  `0a58642da8c5111102ed7efa978e3f90f36cbe76	refs/heads/main`.
  Local HEAD (`git rev-parse HEAD`) `0a58642da8c5111102ed7efa978e3f90f36cbe76` == remote HEAD. PASS.
- This follow-up commit (planning doc only) completes this commit record. After its push, local
  HEAD == remote HEAD is re-verified with `git ls-remote origin main`, and that final output line
  is the state `Knuckles` re-verifies for `## Release`.

---

## Review

*Owner: `Shadow`. Read-only — findings only, no edits. Severity order, blockers first.*

### Round-1 findings (all resolved and shipped; full text in `## Archive`)

- **should-fix — "serves" on the sibling endpoint ports overstates the verified facts** (former
  `README.md:447`): fixed in `1da994a`. The sentence now states only verified facts. The firewall
  keeps 8080-8088 and 8090 open, the opencode client carries entries for them, and as of
  2026-08-29 the only listener in the 8080-8099 range is this endpoint on 8092 (`ss -tln`,
  `## Implementation` remote record item 5), machine-verified rather than sourced from the
  newest team record.
- **nit — memory unit differs between the README and the ssh-verified Status** (former
  `README.md:407`): fixed in `1da994a`. Settled with the `free -h` reading on 192.168.1.106
  (2026-08-29, `Mem: 92Gi total`). The README now says "92 GiB of unified memory" with the
  source and date; the "92 GB pool" mention in the one-active-model paragraph was aligned to
  "92 GiB pool". The "~91 GB visible to the Vulkan device" figure is a different quantity
  (device-visible memory) and keeps the unit as recorded in its source.
- **nit — "the measured ceiling on this hardware" lacks the Q5 attribution the next sentence
  carries** (former `README.md:479-481`): fixed in `1da994a`. Both suggested directions
  combined. `--parallel 1` at 262144 is now stated as the team's operating point and, per the
  fit table, the measured ceiling on this hardware, and the next sentence states the fit table
  was measured on the heavier sibling Q5 model (2026-08-23) so the Q4 ceiling is unmeasured,
  though the Q4 weights are smaller.

**Verified clean (2026-08-28, `Shadow`):**
- The user-requested correction is present and unambiguous at `README.md:588-589` ("The context window was not reduced. The unit still requests `-c 262144` and the endpoint serves it."), and the user decision of 2026-08-27 12:13 UTC is accurately restated at `README.md:590-592` against `planning/docs/TASK-0010-evox2-gpu-wedge-fix.md:32-34`.
- The `ExecStart` line at `README.md:466` matches the live-process record flag for flag (`planning/docs/TASK-0010-evox2-gpu-wedge-fix.md:503-505`, `:513`), and the remaining unit lines match the `add-ai-model` skill template (`~/.config/opencode/skills/add-ai-model/SKILL.md:81-101`) and are marked as template-derived at `README.md:474-475`.
- The provider entry at `README.md:525-541` is verbatim `~/.config/opencode/opencode.json:121-137` (baseURL, timeout 3600000, context 262144, output 131072).
- All GPU-wedge numbers trace to their sources. 26 wedges in about two days of Q5 load (`qwen38-q5-fixes.md:116-117`), the 120 W cap with 0 throttle events and the 201k/29-min fresh-chip repro (`planning/docs/TASK-0010-evox2-gpu-wedge-fix.md:466-480`, Status lines 15-27), the 27-29 min cascade and the TASK-0008 2c death at 02:33 UTC (`:458-464`), the 5-11 s restarts and 5.1 s reload (`:432-433`, Status lines 29-31), the exhausted sysfs surface and the `low` numbers 55.5/255.8 and 2.83/11.87 t/s at about 4.5x (`:582-598`, `:614-619`), the 12 s empty `/v1/models` window (`qwen38-q5-fixes.md:99-101`), the 40 GB sibling hold (`qwen38-q5-fixes.md:78-83`), and the monitoring command verbatim (`planning/docs/TASK-0010-evox2-gpu-wedge-fix.md:93-94`).
- Unverified items are handled per the DoD. Binary provenance is marked at `README.md:418-419`, the unit file beyond `ExecStart` is marked at `README.md:474-475`, and `ryzenadj` is absent from the README (grep, no matches) per the omit-if-not-verifiable instruction.
- AGENTS.md §10 holds for the whole file. No em or en dashes anywhere in `README.md` (grep, no matches), no banned words (grep, no matches), colons appear only inside the JSON block, timestamps, and URLs, all permitted technical contexts, explanations are prose rather than bullets (tables enumerate reference values, the numbered list is an ordered verification procedure), and the section takes positions ("takes the trade anyway", "The standing decision is to keep `auto`").
- Internal consistency holds. Port 8092, IP 192.168.1.106, the model name `Qwen3.8-27B-UD-Q4_K_XL`, the unit name, and the model directory are identical across the `## Model` cross-reference (`README.md:393-396`), the new section, and `~/.config/opencode/opencode.json:121-137`. The port list 8092 plus 8080-8088 and 8090 is the complete verified open-port set from `## Status` lines 46-47 (8084 falls inside 8080-8088).

### Round 2 (targeted re-review of the fix diff `ef884e4` → `109ee7c`, 2026-08-29, `Shadow`)

**Scope and method.** Reviewed the fix diff (`git diff ef884e4 109ee7c`, README hunks all inside the
`## EVO-X2 model host setup` section, old lines 404-603; the `## Model` cross-reference and every
other part of the README untouched) against the pushed text at `109ee7c` (working tree clean,
`git status` shows branch up to date with `origin/main`). Every new factual claim was checked
against the `## Implementation` remote verification record (2026-08-29, read-only ssh). The unit
block itself (`README.md:470-485`) is byte-identical to the pre-fix state, so the round-1
verification of the block against the skill template and the live-process record carries over.

**Round-1 findings, verified resolved in the pushed text (all fixed in `1da994a`; the six
Resolution lines carry that sha, completed by follow-up `109ee7c`, per the diff
`1da994a` → `109ee7c` on this doc):**
- should-fix, "serves" (former `README.md:447`): now `README.md:456-460`. States only verified facts, per the suggested direction. The port set "8080-8088 and 8090" matches the live `firewall-cmd --list-all` port list exactly (record item 2: 8080-8088 contiguous plus 8090 plus 8092), the client-entry claim was verified in round 1 against `~/.config/opencode/opencode.json`, and "as of 2026-08-29 the only listener in that range is this endpoint on 8092" matches `ss -tln` (record item 5: 8092, 22, 9090; 22 and 9090 are outside 8080-8099). The one-active-model rule is cross-referenced to the systemd unit subsection, where it sits (`README.md:520-522`).
- nit, GB/GiB (former `README.md:407`): now `README.md:407-408`, "92 GiB of unified memory (`free -h` on the reference machine, 2026-08-29)", matching record item 5 (`Mem: 92Gi total`) and the ssh-verified Status. "92 GB pool" aligned to "92 GiB pool" at `README.md:520`. The "~91 GB visible to the Vulkan device" keeps GB as recorded in its own source (`/home/howard/AI/projects/qwen-38-q5-fixes/qwen38-q5-fixes.md:5`), which is the right call for a different quantity.
- nit, Q5 attribution (former `README.md:479-481`): now `README.md:493-498`. The ceiling is qualified as "the team's operating point and, per the fit table, the measured ceiling on this hardware", followed by "The fit table was measured on the heavier sibling Q5 model (2026-08-23), so the Q4 ceiling is unmeasured, though the Q4 weights are smaller." The date matches the source heading (`qwen38-q5-fixes.md:62`, "Measured memory ceiling (2026-08-23, Q5 alone, Q6 stopped)"), and the 4 x 65536 sentence keeps its attribution ("same Q5 measurement"). Both suggested directions applied.
- Omega low 1, unauthenticated endpoint: now `README.md:534-537`, the exact sentence Omega proposed, in the Firewall subsection. The verified `ExecStart` (`README.md:479`) is unchanged.
- Omega low 2, unpinned CLI: now `README.md:417`, `pip install "huggingface_hub==1.19.0"`, the version read from the machine via `pip show` (record item 5), not guessed.
- Omega low 3, no hash: SHA-256 column added at `README.md:435-438`; both values character-identical to record item 5 (`3f227079...` weights, `cbb841a9...` mmproj). The download-verification sentence leads with `sha256sum` and keeps the magic-header check (`README.md:453-454`), and the verification list carries `sha256sum` as item 2 (`README.md:622-623`).

**ssh-verification upgrades, each supported by the record:**
- Unit note (`README.md:487-489`): the whole 14-line block read back on 2026-08-29 and matching line for line (record item 1; the block at `README.md:471-484` is exactly 14 lines including the two blanks and three section headers, consistent with the record's enumeration).
- Firewalld live state (`README.md:532-534`): `public` zone on `eno1`, ports 8092 plus 8080-8088 and 8090, services cockpit, dhcpv6-client, ssh. Matches record item 2 exactly.
- `**The power limits.**` paragraph (`README.md:582-586`): path, description, oneshot type, the verbatim `--fast-limit=100000 --tctl-temp=88` flags, `RemainAfterExit=yes`, and the enabled/active state all match record item 3. The "100 W" and "88 C" readings are the standard ryzenadj flag units (mW, deg C); the flags themselves are quoted verbatim from the verified unit.
- Provenance paragraph (`README.md:419-428`): 16 KB launcher (record: 16712 bytes), the eight `/usr/local/lib64` library names identical to record item 4 in order, `BuildID[sha1]` `65396b85...` character-identical, not package-owned, the commit confirmed to exist upstream, no source tree in the three checked locations, and the pristine-vs-locally-modified question left explicitly marked as not recorded, per the task instruction.

**Verified clean (round 2, 2026-08-29, `Shadow`):**
- AGENTS.md §10 holds for the whole file after the fix. Zero em or en dashes in `README.md` (grep with `include: README.md`, no matches), zero banned words (same method, no matches), and colons inside the section (lines 398-627) appear only in the JSON block (`README.md:544-556`), the two UTC timestamps (`README.md:591`, `:615`), and the two URLs (`README.md:548`, `:624`), all permitted technical contexts.
- No self-contradiction introduced. The port set, the three memory figures (each with its own source and date), the unit name, the model name, the IP, and the `(see the systemd unit subsection)` cross-reference are consistent across the section and the `## Model` cross-reference.
- Commit scope matches the record. `git diff --stat ef884e4 1da994a` = 3 files, +284/-78, exactly as recorded; `git diff --stat 1da994a 109ee7c` = planning docs only, exactly as recorded.

### Round-2 nit (resolved and shipped; full text in `## Archive`)

- **nit — the 100 W fast limit and the ~120 W sustained cap are adjacent without a bridge**
  (`README.md:574-586`): fixed in `0a58642`. One bridging sentence appended to the ryzenadj
  paragraph (now `README.md:586-589`), using the "mark the relationship unverified" option. The
  ~120 W figure is identified as the sustained PPT cap measured in the TASK-0010 stress run, the
  100 W fast limit as what `ryzenadj` configures on the reference machine, and whether the fast
  limit is in effect under sustained load as unverified. No claim about which limit governs
  sustained load.

### Round 3 (targeted check of fix `0a58642`, 2026-08-29, `Shadow`)

**Scope and method.** Checked the pushed text at `c4cbf63` (working tree clean, up to date with
`origin/main`, `git status`) on the three dispatch points. The reviewed text is the pushed text,
because `git diff 0a58642 c4cbf63 --stat` shows the follow-up commit touched only this planning
doc.

- **(a) Factual consistency.** The ~120 W clause traces to `planning/docs/TASK-0010-evox2-gpu-wedge-fix.md:471-475`, which records PPT pinned 119-120 W for the entire 32.7 min with the chip at the package power cap, "consistent with sustained at-power-cap operation" under `auto`. The 100 W clause traces to the verified `ryzenadj.service` `ExecStart` (`## Implementation` remote record item 3, `--fast-limit=100000`, read 2026-08-29, 100000 mW = 100 W). The sentence makes no claim about which limit governs sustained load; its third clause marks that relationship unverified, which is the option `## Implementation` records as chosen.
- **(b) AGENTS.md §10.** Zero em or en dashes in `README.md` (grep, no matches), zero banned words (word-boundary grep, no matches), no colon in the new sentence (commas only), prose rather than bullets.
- **(c) Scope.** `git diff 109ee7c 0a58642 -- README.md` is a single hunk, one line modified (the sentence appended inside the `**The power limits.**` paragraph), no other README line changed.

**Outcome.** Round-2 nit resolved in `0a58642`. No new findings. Every finding in this section now
carries a Resolution line with its fixing sha; no unresolved blocker or should-fix remains, so the
DoD box "`Shadow`: no unresolved blockers or should-fix findings in `## Review`" is satisfiable
from this section.

---

## Security

*Owner: `Omega`. Read-only. Severity order.*

### Unauthenticated inference API on all interfaces, exposure not stated in the README
**Severity:** low
**Vector:** authz
**Where:** `README.md:466` (`--host 0.0.0.0` in `ExecStart`), `README.md:508-518` (Firewall)
**Attack:** the llama-server OpenAI-compatible HTTP API has no authentication layer, and the unit binds it to `0.0.0.0`. Any host in the network segment covered by the `public` zone (on the reference machine the home LAN on `eno1`, this doc `## Status` lines 46-47) can reach 8092/tcp. The attacker needs no credential. A compromised LAN device, a guest laptop, or an IoT endpoint can send arbitrary prompts to `http://192.168.1.106:8092/v1` and query `/v1/models`. The README documents the firewall rule and the zone, but nowhere says the endpoint is unauthenticated or that the firewalld rule is the only access control. A reader who follows the section onto an untrusted segment (guest Wi-Fi, a borrowed network) sees the firewall rule as the whole picture and does not notice the box is serving anonymous inference.
**Impact:** availability and compute, not confidentiality. The team runs on this single-slot endpoint (`--parallel 1`, `README.md:393`), so a hostile or malfunctioning client on the segment can saturate it and stall every agent dispatch, or burn GPU time on its own prompts. No credential is exposed, and the API does not return other sessions' context (single slot, per-request responses only).
**Fix:** one sentence in the Firewall subsection (or the unit subsection). The HTTP API is unauthenticated, the firewalld rule is the only access control, and on a network that is not fully trusted the port should be restricted to the team's segment instead of opened in the `public` zone. Do not change the verified `ExecStart`.
**Resolution:** fixed in `1da994a` (this turn's fix commit; the push and ls-remote lines are recorded in the `## Implementation` follow-up below). One sentence added to the Firewall subsection, exactly the fix named. "The llama-server HTTP API is unauthenticated, so the firewalld rule is the only access control, and on a network that is not fully trusted the port should be restricted to the team's segment instead of opened in the `public` zone." The verified `ExecStart` was not changed.

### Download procedure installs `huggingface_hub` without a version pin
**Severity:** low
**Vector:** supply-chain
**Where:** `README.md:416` (Hardware and software table, Model download row)
**Attack:** the documented setup installs the `hf` CLI unpinned (`pip install huggingface_hub`). The attacker is the PyPI supply chain itself, a compromised or malicious future release of `huggingface_hub`. A reader who follows the README later installs whatever is current at that time and executes it on the model host at setup. The same CLI is the tool that fetches the model weights, so a malicious release can also serve tampered files in place of the download.
**Impact:** code execution on the model host at setup time. That host serves the team's only inference endpoint, so a compromise reaches every agent session, but the window is setup time and the attacker must own the package name.
**Fix:** pin the CLI to the version the team actually verified and record it, e.g. `pip install "huggingface_hub==<verified version>"`. Read the version from the reference machine (`pip show huggingface_hub` over the ssh channel that opens after the next opencode restart) rather than guessing, per AGENTS.md §5.
**Resolution:** fixed in `1da994a` (this turn's fix commit; the push and ls-remote lines are recorded in the `## Implementation` follow-up below). The Hardware and software table row now reads `pip install "huggingface_hub==1.19.0"`, with the note that 1.19.0 is the version on the reference machine. The version was read from the machine via `pip show huggingface_hub` (2026-08-29, `## Implementation` remote record item 5), not guessed. The `hf` CLI sits at `/home/howard/.local/bin/hf` in the user site.

### Downloaded weights are verified by format only, with no hash
**Severity:** low
**Vector:** supply-chain
**Where:** `README.md:443-444`
**Attack:** the only integrity check documented for the downloaded GGUF files is file size plus the GGUF magic header (`4747 5546`), which verifies the container format, not the content. An attacker who can redirect the model host's download (a compromised router or DNS on the LAN) serves a different model file that passes both checks, and the team runs it as the inference endpoint. This is the same supply-chain surface as the unpinned-CLI finding, one step further down the chain.
**Impact:** a substituted or adversarial model becomes the team's endpoint and every agent session then runs on attacker-influenced weights. The precondition, LAN-level redirection of an HTTPS download, makes this unlikely on the reference network. Rated low on exploitability, not on impact.
**Fix:** record a SHA-256 for each of the two files in the Model files subsection (computed once from the verified files on the reference machine) and add `sha256sum` to the verification list. If the team considers that overkill for a home LAN, say so in the section so the format-only check is a stated choice rather than an omission.
**Resolution:** fixed in `1da994a` (this turn's fix commit; the push and ls-remote lines are recorded in the `## Implementation` follow-up below). The Model files table gained a SHA-256 column with both hashes computed on the reference machine (2026-08-29, `## Implementation` remote record item 5. `3f227079...` for the weights, `cbb841a9...` for the projector). The download-verification sentence now leads with `sha256sum` against the table and keeps the GGUF magic-header check, and the Verification after setup list gained item 2, a `sha256sum` match of both files. The hash check is documented as the standard, not an optional extra, so the format-only check is no longer the only stated control.

**Verified clean (2026-08-29, `Omega`):**
- No credentials, tokens, or API keys in the section or introduced by `9e1f0c9`. Grep of the pushed README for credential patterns (`password|token|secret|api-key|Bearer|ghp_|hf_|AKIA`): the section's only hits are the word "token" in model token counts (`README.md:479`, `:559`, `:563`). The provider entry (`README.md:524-541`) carries no `apiKey` field, consistent with the unauthenticated endpoint. `hf download` is documented without an HF token. The LAN IP, the `howard` username (`README.md:577`), and the filesystem paths are not secrets per the task brief. `gitleaks` is not installed on this host (`command not found`), so the scanner of record for the pushed state is the CI `secret-scan-self.yml` workflow (gitleaks on push and weekly). The commit's non-README files contain no secret values; the PAT reference in `planning/docs/TASK-0014-vector-bash-permissions.md:334` is value-free and its absence from the repo and history was verified in that task's `## Security`.
- The working tree matches the pushed section. `git diff 9e1f0c9 HEAD -- README.md` shows only the agent catalogue row (line 34, TASK-0014 follow-up) changed after `9e1f0c9`; lines 398-601 are byte-identical to the pushed state.
- The firewall command (`README.md:510-514`) adds exactly `8092/tcp` in the `public` zone and nothing else. It does not ask the reader to open ssh, cockpit, or any other service. The statement of the reference machine's existing open ports and services (`README.md:516-518`) is a fact about the machine, not a setup instruction.
- The systemd unit guidance does not weaken security. The unit is user-level, runs as the model host user, uses no `sudo`, no root, and no capability beyond the user's own. `LimitMEMLOCK=infinity` (`README.md:465`) is required by `--mlock` for a model of this size and is scoped to that user service. `Restart=on-failure` with `RestartSec=5` is availability, not a security property.
- No metacharacter traps for copy-paste. Every code block in the section (lines 434-441, 457-472, 498-502, 510-514, 524-542, 576-578) and every inline command in the verification list (`README.md:596-600`) was inspected. All arguments are fixed literals, there is no variable, no leading-dash value, and no argument-injection surface. The only special characters anywhere are `|` and `"` inside the single-quoted ssh remote command (`README.md:577`), which paste literally (single quotes, no `!`, so no history expansion). A README-scoped grep for literal `$` returns only lines 188, 205, 247, 297, 299, 623, 624, all outside the section, and a README-scoped grep for `!` returns zero matches.
- License: no misstatement and no missing attribution for a docs-only change. The section makes no license claim about llama.cpp, identifying it by version 9671, commit `c1304d7b2`, and binary path (`README.md:414`) with the provenance explicitly marked unrecorded (`README.md:418-419`), and it attributes the weights to the source repo `unsloth/Qwen3.8-27B-GGUF` (`README.md:430`). Neither the README nor the source skill (`~/.config/opencode/skills/add-ai-model/SKILL.md`) states a model license. If the team ever redistributes the weights instead of documenting a download, the upstream license must be named at that point.
- The ssh monitoring command (`README.md:577`) uses plain key-based ssh, not the `sshpass -p` pattern from the source skill (`SKILL.md:31` and following). The README does not document the skill's plaintext password file (`~/ai_machine_pass.md`, `SKILL.md:10-11` and `:161`), which is correct. The agent-facing risk of the ssh channel itself is tracked as H-2 in `planning/docs/TASK-0014-vector-bash-permissions.md:353-360`, a Vector bash-set issue, not a README issue.

### Round 2 (targeted re-review of the fix diff `ef884e4` → `109ee7c`, 2026-08-29, `Omega`)

**Scope and method.** Reviewed the fix diff (`git diff ef884e4 109ee7c`. The README change is all in
commit `1da994a`; `109ee7c` is planning-docs only, per Shadow's stat check) against the pushed text
at `109ee7c` (working-tree README byte-identical to `origin/main`, `git status`). Re-ran the
round-1 secret and metacharacter scans over the section, and compared the new SHA-256 and BuildID
values character for character against `## Implementation` remote record items 4 and 5.

**Round-1 findings, verified resolved in the pushed text (all fixed in `1da994a`):**
- Low, unauthenticated endpoint. Now `README.md:534-537`, the exact sentence from the fix, in the
  Firewall subsection. The verified `ExecStart` (`README.md:479`) is unchanged. Resolved in `1da994a`.
- Low, unpinned `huggingface_hub`. Now `README.md:417`, `pip install "huggingface_hub==1.19.0"`,
  the version read from the reference machine via `pip show` (record item 5) rather than guessed,
  with the "the version on the reference machine" note. Resolved in `1da994a`.
- Low, no hash. SHA-256 column at `README.md:435-438`; both digests character-identical to record
  item 5 (extracted from both files with a 64-hex-char grep and compared). The download-verification
  sentence (`README.md:453-454`) leads with `sha256sum` against the table and keeps the magic-header
  check, and the verification list carries `sha256sum` as item 2 (`README.md:622-623`). Resolved in
  `1da994a`.

**New content, assessed:**

- **ryzenadj power-limits paragraph (`README.md:582-586`).** Safe for a reader to copy. It is
  descriptive, not instructional. The README gives no install step and no run command for
  `ryzenadj`; the only copyable string is the quoted `ExecStart`
  (`/usr/bin/ryzenadj --fast-limit=100000 --tctl-temp=88`), fixed literals only, no variables, no
  leading-dash values, no metacharacters, and it reproduces the reference machine's own verified
  state rather than directing a change. The values are conservative. A 100 W transient cap and an
  88 C TCTL limit (standard ryzenadj flag units, mW and deg C, read the same way by Shadow) are
  protective settings, not performance overrides, so a reader who copies them onto identical
  hardware lands on a known-good state. The section offers no documented path to a dangerous
  change. The wedge subsection's actionable advice stays the verified what-works and what-does-not-
  work lists, and nothing in the new paragraph tells a reader to touch the limits. The residual
  risk is a reader misreading which cap governs sustained load (fast 100 W versus the measured
  roughly 120 W sustained PPT) and going off-script. That is a documentation-clarity issue, and it
  is captured by Shadow's round-2 nit in `## Review` ("The 100 W fast limit and the ~120 W sustained
  cap are adjacent without a bridge"). It is not a security vector because the README supplies no
  action to take. All factual claims match record item 3 verbatim (path, description, oneshot,
  flags, `RemainAfterExit=yes`, enabled/active). No new exposure.
- **Unit file quoted in full (`README.md:470-485`).** Nothing new exposed beyond the already-scoped
  `LimitMEMLOCK`. The block is byte-identical to the pre-fix text (no diff hunk touches it); the
  only new claim is the note at `README.md:487-489` ("read back ... matches this block line for
  line"), which record item 1's `cat` supports (14-line enumeration = 9 directives + 3 section
  headers + 2 blanks, exactly the block). The full file adds only ordering and availability lines
  (`After=`/`Wants=network-online.target`, `Type=simple`, `Restart=on-failure`, `RestartSec=5`,
  `WantedBy=default.target`). No `Environment=`, no `ExecStartPre`, no `User=`/`Group=` override,
  no capabilities, no `ReadWritePaths`, no sudo, no root. It remains a user-level unit running as
  the model host user. The one security-relevant line in the block, `--host 0.0.0.0` in
  `ExecStart`, is the known unauthenticated surface and is now documented at `README.md:534-537`.
- **Binary-provenance paragraph (`README.md:419-428`).** No secrets exposed. The BuildID
  (character-identical to record item 4), the eight library names, and the install paths are not
  sensitive. The paragraph asserts more than round 1 (source install, not package-owned, not a
  release artifact, 16 KB launcher plus `/usr/local/lib64` libraries, commit exists upstream, no
  source tree in the three checked locations) and leaves the one unknown explicitly marked
  (pristine versus locally modified checkout). Supply-chain note for the record. The team's only
  endpoint binary is a non-release local source build whose tree state is not recorded, so its
  integrity anchors are the version, the commit (which exists upstream but whose tree state is not
  recorded), and the BuildID. The attacker for this surface (a modified checkout at build time)
  needs build-host access at build time, is outside the remote-attacker model, and is not reachable
  through the README, which provides no build recipe and nothing copyable. The current marking is
  the correct treatment and is consistent with the round-1 clean statement. If the team wants a
  stronger guarantee, the fix is a recorded build recipe plus a pinned source commit, which is a
  build-host question for the user, not a README defect. Not a finding.
- **Verification list, `sha256sum` guidance (`README.md:619-627`).** Sufficient as written for the
  threat it is designed for (download-path tampering, the round-1 low-3 model). Item 2 names both
  files by directory, points at the table, and the table carries both filenames and the full
  64-hex digests, so the digest-to-file mapping is unambiguous. A reader who ran the download block
  is already in the model directory (`README.md:446`) and compares the digest field of `sha256sum`
  output against the table. The only omission is the literal command, which is trivial to derive
  from the filenames in the same table. The check sits in the right order, after the download
  (`README.md:453-454`) and before the endpoint is declared healthy. Structural boundary, noted for
  completeness, not a defect. The trusted digests live in the same document as the procedure, so an
  attacker who can rewrite the README can rewrite both, and the check defends the download path,
  not the document. That is inherent to in-repo hashes and is bounded by repository governance
  (team-controlled `metalllinux` repo), not by the README text.

**Verified clean (round 2, 2026-08-29, `Omega`):**
- Secret scan re-run over the section (case-insensitive grep for
  `password|token|secret|api-key|Bearer|ghp_|hf_[A-Za-z0-9]|AKIA|BEGIN ... PRIVATE KEY` over the
  pushed README). The section's only hits are the word "token" in model token counts
  (`README.md:493`, `:578`, `:588`). No new credential, token, or key in the new paragraphs.
  `gitleaks` is still not installed on this host, so the scanner of record for the pushed state
  remains the CI `secret-scan-self.yml` workflow.
- Metacharacter scan re-run. A README-wide grep for `$` or `!` returns only lines 188, 205, 247,
  297, 299, 650, 651, all outside the section (the round-1 set shifted by the section's growth;
  zero `!` anywhere). All new inline code (the `pip install` pin, the quoted `ryzenadj` flags, the
  `sha256sum` item) is fixed literals. No new copy-paste trap.
- Attacker-surface check over the new text. Nothing the diff adds is reachable by a remote
  attacker. The system unit's path and `ExecStart`, the power-limit values, the BuildID, and the
  weight digests are all trivially readable locally by anyone who already has host access, and the
  README adds no credential, no new network exposure, and no new remotely runnable command.
- License. No change. The provenance paragraph makes no license claim about llama.cpp and adds no
  redistribution path. The round-1 license statement stands.

**Outcome.** No new findings. The three round-1 lows are resolved in `1da994a` and verified in the
pushed text at `109ee7c`. The four new content items (ryzenadj paragraph, full unit quote,
provenance paragraph, verification list) add nothing above `low` and no actionable security
finding. The DoD box "no unresolved findings above `low` in `## Security`" is satisfiable from
this section.

---

## Test Results

*Owner: `Big`. Verdicts, never raw log dumps.*

**Workflow run:**

| Check | What it exercises | Result | Notes |
|---|---|---|---|
| compile | changed files | PASS/FAIL | |
| linter | style and correctness | PASS/FAIL | |
| unit tests | individual functions | PASS/FAIL | |
| integration tests | end-to-end flows | PASS/FAIL | |
| Sparky tests | Rocky Linux UI (if applicable) | PASS/FAIL | |

**Checks requested vs run:** N requested, N executed. *If any were dropped or skipped, say so here
explicitly — a truncated run reporting green reads as full coverage.*

**Verdict:** prose. For each FAIL: the failing check, the evidence, and whether it is a code bug (goes
to `Tails`) or a harness bug (stays with `Big`).

---

## Docs

*Owner: `Vector`.*

| File | Sections touched | What changed |
|---|---|---|
| `README.md` | `## Model` (cross-reference sentence appended, line 395-396); new `## EVO-X2 model host setup` (lines 398-601) with subsections Hardware and software, Model files, The systemd unit, Firewall, The opencode client, The GPU wedge, Verification after setup | New section documents the EVO-X2 model host per `## Status` facts and `## Definition of Done`. Hardware/OS/kernel (Ryzen AI MAX+ 395 Strix Halo, Radeon 8060S gfx1151, 92 GB unified, Rocky 10.2, elrepo kernel `7.0.12-1.el10.elrepo.x86_64`); llama.cpp Vulkan binary version 9671 (commit `c1304d7b2`), built with GNU 14.3.1; HF download per the `add-ai-model` skill (repo `unsloth/Qwen3.8-27B-GGUF`, `hf` CLI, magic-header check); model dir `/mnt/data/models/qwen3.8-27b-q4/` layout; user-level unit with the `ExecStart` line verified on the live process (TASK-0010 checkpoint 3.2, `planning/docs/TASK-0010-evox2-gpu-wedge-fix.md:503-505`) and the remaining lines from the team unit template (`~/.config/opencode/skills/add-ai-model/SKILL.md:81-101`); firewalld rule for 8092/tcp (public zone on eno1, ports and services per `## Status`); opencode provider entry verbatim (`~/.config/opencode/opencode.json:121-137`); GPU wedge section with the verified characterization (TASK-0010 checkpoints 3.1/3.3/3.4), what works (unit auto-restart 5-11 s, `--mlock` 5.1 s reload, moderate request/session sizes, `journalctl` monitoring command per `planning/docs/TASK-0010-evox2-gpu-wedge-fix.md:93-94`), what is exhausted (sysfs surface, `low` at 4.5x slower), and the correction that the context window was not reduced and `-c 262144` stays |

**Verified by `Vector` this turn (local artifacts, read directly):**
- Provider entry `evo-x2-qwen3.8-q4` in `~/.config/opencode/opencode.json:121-137` (baseURL
  `http://192.168.1.106:8092/v1`, timeout 3600000, context 262144, output 131072)
- Download procedure and unit template in `~/.config/opencode/skills/add-ai-model/SKILL.md`
  (HF repo `unsloth/Qwen3.8-27B-GGUF`, `hf` CLI, GGUF magic `4747 5546`, port range 8080-8099,
  one active model at a time); `new-model-import/SKILL.md` best practices
- TASK-0010 wedge guidance, targeted reads: 11:10 UTC and 12:13 UTC Status entries (lines
  15-36), checkpoint 3.1 (lines 397-484), 3.3 (lines 551-598), 3.4 (lines 611-640), monitoring
  command (lines 93-94)
- `/home/howard/AI/projects/qwen-38-q5-fixes/qwen38-q5-fixes.md` (hardware spec lines 3-5,
  monitoring lines 142-144, fit-degradation table lines 64-69, 12 s load window lines 99-101,
  26-wedge history lines 113-122, 40 GB pool hold lines 78-83)
- Reference-machine facts cited from `## Status` above (Robotnik, ssh-verified 2026-08-27/28),
  which the DoD permits as team artifacts

**Checked and needed no change:**
- `AGENTS.md` (Model line already matches the reference endpoint, `evo-x2-qwen3.8-q4` port 8092
  `--parallel 1`; no setup detail belongs there)
- `planning/docs/TASK-0010-evox2-gpu-wedge-fix.md` (read-only source, untouched)
- Both team skills and `~/.config/opencode/opencode.json` (read-only sources, untouched)
- No `CHANGELOG.md` exists in this repository, so no changelog entry
- `planning/docs/TASK-0011-default-model-q4kxl.md` (Status read; its `--parallel 4` note is
  historical, dated 2026-08-25, predating the single-slot change) and
  `TASK-0012-single-slot-sequencing.md` (Status read via grep; records the user's `--parallel 1`
  decision, which is the state the README documents). The `--parallel 1` deviation from the skill
  template is explained in the README with the measured fit ceiling and the accepted queuing
  trade

**Could not verify:** all four items (unit file text beyond `ExecStart`, current live firewalld
state, `ryzenadj.service` purpose, llama.cpp binary provenance) were settled by the 2026-08-29
read-only ssh record in `## Implementation` (see the Settlement block there, record items 1-4).
The `Commit status` paragraph that followed (work uncommitted, `git` ship blocked by Vector's
permission set) is superseded by the ship in commit `9e1f0c9`. Full text of both blocks:
`## Archive`.

---

## Release

*Owner: `Knuckles`.*

**DONE checklist verified:** yes. All seven boxes in `## Definition of Done` ticked 2026-08-29.
The underlying evidence is in this doc. README section and verified claims per `## Docs` and
the `## Implementation` remote verification record (2026-08-29, read-only ssh), §10 style per
Shadow's round-2 and round-3 clean statements, Shadow box per `## Review` round 3 outcome
(no unresolved blocker or should-fix), Omega box per `## Security` round 2 outcome (no
unresolved findings above `low`), Big N/A recorded in the box itself, and box 7 (committed +
pushed, local HEAD == remote HEAD at `c4cbf63`) re-verified in the Remote HEAD verification
item below.

- **Branch:** `main`. Direct push to `metalllinux/team-chaotix` under the standing 2026-08-21
  user permission for `metalllinux` repos. No feature branch, no PR. Internal repo, AGENTS.md
  §8.
- **Commits:** `9e1f0c9` (`9e1f0c91579a3f9b17ec5c490041b2bb4146e3ae`, initial ship, mixed
  scope stated in the message) → `109ee7c` (`109ee7c970b49565a107e2c6668fb927b381ebdb`, fix
  follow-up, planning docs) → `c4cbf63` (`c4cbf63cf6334325797430e988a6054fe6eacf2a`, final
  follow-up, current main). GPG-signed: no. `commit.gpgsign` is not set in this repo (`git
  config --get commit.gpgsign` → empty, 2026-08-29) and the recent history is unsigned (`git
  log --format='%h %G?' -12` → `N` on every line).
- **PR:** n/a. Internal repo shipped by direct push under the standing permission. No PR
  required, AGENTS.md §8.
- **Deploy:** n/a. Docs-only change (README + team config). No deployment to dispatch.
- **Remote HEAD verification (2026-08-29, Knuckles):** `git ls-remote origin main`, actual
  output, quoted verbatim:
  `c4cbf63cf6334325797430e988a6054fe6eacf2a	refs/heads/main`.
  Local HEAD (`git rev-parse HEAD`) `c4cbf63cf6334325797430e988a6054fe6eacf2a` == remote HEAD.
  PASS. This line also carries the deferred `ef884e4` verification from TASK-0014. `ef884e4`
  (`ef884e468614944e8ec4e75050622115d6447645`) is an ancestor of `c4cbf63` on `main` (`git
  merge-base --is-ancestor ef884e4 c4cbf63` → exit 0, 2026-08-29), so the pushed main HEAD
  confirms the TASK-0014 final state on the remote.
- **Release record commit (follow-up per the TASK-0011 convention):** this `## Release` record
  shipped in commit `2678b28` (full `2678b2853916b2f3095b0bc6755192ccdde76709`), pushed with
  `git push origin main` → `c4cbf63..2678b28  main -> main`. `git ls-remote origin main` after
  that push, actual output, quoted verbatim:
  `2678b2853916b2f3095b0bc6755192ccdde76709	refs/heads/main`.
  Local HEAD (`git rev-parse HEAD`) `2678b2853916b2f3095b0bc6755192ccdde76709` == remote HEAD.
  PASS (2026-08-29, Knuckles).

---

## Archive

*Owner: `Espio`, the only agent that deletes. Superseded detail lands here rather than being
lost. Decisions, verified facts, rejected options with their reasons, known traps, and anything
the user said are never deleted.*

**Pruning log**

| Date | What was pruned or compressed | Rough size |
|---|---|---|
| 2026-08-29 | Superseded `## Docs` "Could not verify" list (4 items, all settled by the 2026-08-29 read-only ssh record in `## Implementation`) and "Commit status" paragraph (work shipped as `9e1f0c9`) moved here, `## Docs` left with a pointer | ~22 lines |
| 2026-08-29 | Round-1 `## Review` findings (1 should-fix, 2 nits, all fixed in `1da994a`) and round-2 nit (fixed in `0a58642`) compressed to one-liners in `## Review`; full finding text moved here | ~38 lines |
| 2026-08-29 | Ship of this pruning (commit + push + `git ls-remote`) pending: Espio's loaded set is `bash: deny` (`.opencode/agents/espio.md:17`). Commit sha to be recorded here by the shipping commit | n/a |

### Superseded `## Docs` "Could not verify" list (Vector, 2026-08-28)

**Could not verify (and what would settle it):**
- Unit file text beyond `ExecStart` (Description, After/Wants, Type, LimitMEMLOCK, WantedBy).
  Vector's bash permission set (exact `git status`, `git log*`, `git diff*`, `rg *` only) blocks
  `ssh howard@192.168.1.106`, so the file could not be read on the machine. The README marks
  `ExecStart` as the verified line and the rest as the team template. Settled by
  `ssh howard@192.168.1.106 'cat ~/.config/systemd/user/llama-server-qwen3.8-27b-q4.service'`
- Current live firewalld state. Cited from Robotnik's 2026-08-27/28 verification in `## Status`.
  Settled by `sudo firewall-cmd --list-all` on the machine
- `ryzenadj.service` purpose. Omitted from the README per the task instruction (document only if
  verifiable); no team artifact records its purpose. Settled by
  `systemctl cat ryzenadj.service` plus its config file on the machine
- llama.cpp binary provenance (upstream release or local build). Not claimed in the README.
  Settled by asking the user or inspecting the build host

All four items settled 2026-08-29 by the read-only ssh record in `## Implementation` (record
items 1-4, plus the "Settlement of `## Docs` 'Could not verify'" block).

### Superseded `## Docs` "Commit status" paragraph (Vector, 2026-08-28)

**Commit status:** the README change is written but uncommitted. Vector's permission set also
denies `git commit`, `git push`, and `git ls-remote`, so the commit + push + remote-HEAD
verification in `## Definition of Done` could not run from this role. `git status` shows the
working tree dirty with `README.md` and this planning doc modified, and `git log --oneline -1`
shows HEAD at `d476221` (unchanged, up to date with `origin/main`). Knuckles or the user must
commit both files, push, and verify the remote HEAD.

Superseded: the uncommitted work shipped in commit `9e1f0c9` (see `## Status` and TASK-0014).

### Superseded `## Review` round-1 finding: "serves" on the sibling endpoint ports overstates the verified facts (Shadow, 2026-08-29)

**Severity:** should-fix
**Where:** `README.md:447`
**Problem:** the sentence asserts active serving on 8080-8088 and 8090, but the verified facts establish only that those ports are open in the firewall (this doc `## Status` lines 46-47, Robotnik ssh 2026-08-27/28) and that client entries exist (`~/.config/opencode/opencode.json:5-120`), while the newest verified listener state shows 8084, inside that range, has no listener and the team runs Q4 only (`planning/docs/TASK-0010-evox2-gpu-wedge-fix.md:49-54` 2026-08-26 12:50 UTC entry, `planning/docs/TASK-0010-evox2-gpu-wedge-fix.md:498-502` checkpoint 3.2).
**Failure scenario:** a new team member reads the present-tense "also serves the sibling quantizations on 8080-8088 and 8090", expects sibling endpoints to be up, points a client at 8084 and gets connection refused, and cannot reconcile the sentence with the section's own "Run one active model at a time" rule two subsections later (`README.md:504-506`) or with the section intro's "Every value below is verified against the reference machine or the team's records of it" (`README.md:401-402`), which this unmarked claim does not meet.
**Suggested direction:** state only what is verified. The firewall keeps 8080-8088 and 8090 open for the sibling model endpoints, the opencode client carries entries for them, and per the newest verified state only the Q4 endpoint on 8092 is active. Alternatively mark the current listener state explicitly as unverified. The firewall subsection (`README.md:516-518`) already phrases this correctly and needs no change.
**Resolution:** fixed in `1da994a` (this turn's fix commit; the push and ls-remote lines are recorded in the `## Implementation` follow-up below). The sentence now states only verified facts. The firewall keeps 8080-8088 and 8090 open, the opencode client carries entries for them, and as of 2026-08-29 the only listener in the 8080-8099 range is this endpoint on 8092 (`ss -tln`, `## Implementation` remote record item 5), with the one-active-model rule cross-referenced. The current listener state is now machine-verified rather than merely sourced from the newest team record.

### Superseded `## Review` round-1 finding: Memory unit differs between the README and the ssh-verified Status (Shadow, 2026-08-29)

**Severity:** nit
**Where:** `README.md:407`
**Problem:** the README says "92 GB of unified memory" (following `/home/howard/AI/projects/qwen-38-q5-fixes/qwen38-q5-fixes.md:4-5`, "92 GB unified memory") while the ssh-verified Status says "92 GiB RAM" (this doc `## Status` lines 37-38).
**Failure scenario:** a reader cross-referencing the planning Status against the README sees two unit spellings for the same machine fact and cannot tell which is the measured reading without going to the machine.
**Suggested direction:** pick one unit, preferably the ssh-verified Status's, and note the source, or settle it with a `free -h` reading on 192.168.1.106 when the ssh channel opens.
**Resolution:** fixed in `1da994a` (this turn's fix commit; the push and ls-remote lines are recorded in the `## Implementation` follow-up below). Settled with the `free -h` reading Shadow offered. `free -h` on 192.168.1.106 (2026-08-29) reports `Mem: 92Gi total`, so the README now says "92 GiB of unified memory" with the source and date, matching the ssh-verified Status. The same fact in the "Run one active model at a time" paragraph ("92 GB pool") was aligned to "92 GiB pool". The "~91 GB visible to the Vulkan device" figure is a different quantity (device-visible memory, from the team incident record `/home/howard/AI/projects/qwen-38-q5-fixes/qwen38-q5-fixes.md:4-5`) and keeps the unit as recorded there.

### Superseded `## Review` round-1 finding: "the measured ceiling on this hardware" lacks the Q5 attribution the next sentence carries (Shadow, 2026-08-29)

**Severity:** nit
**Where:** `README.md:479-481`
**Problem:** the fit table behind the claim was measured on the Q5 sibling only (`/home/howard/AI/projects/qwen-38-q5-fixes/qwen38-q5-fixes.md:62-69`, heading "Measured memory ceiling (2026-08-23, Q5 alone, Q6 stopped)"), and the "(measured on the sibling Q5 model)" attribution at `README.md:481` attaches only to the 4 x 65536 sentence, leaving "which is the measured ceiling on this hardware" at `README.md:479` unqualified.
**Failure scenario:** a reader setting up this Q4 endpoint, whose weights are smaller than Q5's, concludes that `--parallel 2` will silently degrade context on Q4, when the only fit measurement is the heavier Q5 model and the Q4 ceiling is unmeasured.
**Suggested direction:** extend the Q5 attribution to the ceiling claim as well, or reword the ceiling as the measured Q5 ceiling or the team's operating point rather than a hardware-wide fact.
**Resolution:** fixed in `1da994a` (this turn's fix commit; the push and ls-remote lines are recorded in the `## Implementation` follow-up below). Both suggested directions combined. The sentence now reads that `--parallel 1` at 262144 is the team's operating point and, per the fit table, the measured ceiling on this hardware, and the next sentence states the fit table was measured on the heavier sibling Q5 model (2026-08-23, `/home/howard/AI/projects/qwen-38-q5-fixes/qwen38-q5-fixes.md:62-69`) so the Q4 ceiling is unmeasured, though the Q4 weights are smaller. The 4 x 65536 degradation sentence keeps its Q5 attribution, now phrased "same Q5 measurement".

### Superseded `## Review` round-2 nit: The 100 W fast limit and the ~120 W sustained cap are adjacent without a bridge (Shadow, 2026-08-29)

**Severity:** nit
**Where:** `README.md:574-586` (trigger paragraph and the new power-limits paragraph)
**Problem:** the trigger paragraph says the chip "sits at the roughly 120 W package power cap" under the failing workloads (sourced from `planning/docs/TASK-0010-evox2-gpu-wedge-fix.md:471-475`, PPT pinned 119-120 W), and the new paragraph two paragraphs later says the ryzenadj unit sets "a 100 W fast power limit". Both are correct and both are sourced, but the section never states that the unit sets only the fast (transient) limit and the TCTL threshold and does not touch the sustained cap that the failing workloads actually run against.
**Failure scenario:** a new team member reads the power-limits paragraph to understand why the chip wedges at the power cap, or to lower the power to avoid wedges. They see the 100 W figure, scroll up to the 120 W figure, and cannot tell which one governs sustained load. They either conclude the section contradicts itself and discount the rest of it, or assume the box is capped at 100 W and cannot later explain monitoring that shows sustained PPT at ~120 W.
**Suggested direction:** add one bridging clause to the ryzenadj paragraph. The unit sets the fast limit and the TCTL threshold only, and the ~120 W figure in the trigger paragraph is the measured sustained PPT cap at which the failing workloads operate. If the team has not confirmed on the machine which limit governs sustained operation, say that the relationship is unverified rather than leaving it implicit.
**Resolution:** fixed in `0a58642` (pushed, main at `c4cbf63`; the push and `git ls-remote` lines are recorded in `## Implementation`). One bridging sentence appended to the ryzenadj paragraph (now `README.md:586-589`), using the "mark the relationship unverified" option. The ~120 W figure is identified as the sustained PPT cap measured in the TASK-0010 stress run, the 100 W fast limit as what `ryzenadj` configures on the reference machine, and whether the fast limit is in effect under sustained load as unverified. No claim about which limit governs sustained load.
