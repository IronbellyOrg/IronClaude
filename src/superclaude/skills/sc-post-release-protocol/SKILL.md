---
name: sc:post-release-protocol
description: "Post-release follow-through protocol backing the /sc:post-release command. Synchronizes and creates a shipped version's entire EXTERNAL SURFACE — user docs, technical docs, install/deploy scripts (validated by real end-to-end runs), and human-run e2e test guides — so a freshly tagged release is fully documented, installable by a brand-new user, and hand-testable. Invoked ONLY by /sc:post-release (e.g. /sc:post-release v1.4.1)."
allowed-tools: Read, Glob, Grep, Edit, Write, Bash, Task, TodoWrite, Skill
argument-hint: "<version> — an existing release tag (e.g. v1.4.1). Optional: --output <dir>"
---

<!-- Extended metadata (for documentation, not parsed):
category: documentation
complexity: high
mcp-servers: [sequential, serena]
personas: [scribe, devops, qa, analyzer]
-->

<!--
allowed-tools note: Bash is intentionally unrestricted. Workstream C runs the real
new-user install/deploy path to green on whatever the repo actually is — pip/pipx in a
throwaway venv, `docker`/`compose` for a service, `go build`/`make` for a Go binary,
or install scripts on a deploy VM. That surface can't be enumerated ahead of time, so a
narrowed Bash allowlist would break the skill's core "prove it installs" guarantee.
The safety boundary that matters here is behavioral: scanners are read-only, all
file creation is gated behind the consolidated plan, and outward-facing/hard-to-reverse
actions are confirmed first (see Boundaries + Guardrails).
-->

# /sc:post-release — Post-Release Follow-Through Protocol

## Triggers

`sc:post-release-protocol` is invoked ONLY by the `sc:post-release` command via `Skill sc:post-release-protocol` in the command's `## Activation` section. It is never invoked directly by users.

Activation conditions:

- User runs `/sc:post-release <version>` in Claude Code (primary invocation surface).
- Any flags (`--output <dir>`) are passed through from the command.

Do NOT invoke this skill directly. Use the `/sc:post-release` command.

## Purpose & Identity

The release gate tags the version. This protocol is the **follow-through**: it brings the release's *external surface* — everything a user, operator, or sysop touches — into agreement with what actually shipped, and creates whatever is missing.

Concretely it drives five workstreams:

- **A — User documentation**: docs for end users and operators.
- **B — Technical documentation**: docs for implementers and engineers.
- **C — Install & deploy scripts**: the path a brand-new user follows to get the version running, *proven by a real end-to-end run*.
- **D — User-facing e2e human-test guides**: step-by-step walkthroughs so a human can hand-verify every user capability.
- **E — Sysop-facing e2e human-test guides**: the same, for admin/operator-only capabilities (only if any exist).

Each workstream **scans** the real code and release, **updates** what exists, **detects** what's missing, and **creates** the gaps — then records what it did in a manifest so the *next* release only has to touch the delta.

### Why this protocol exists (and why it works the way it does)

A release is not done when the tag lands. It's done when a stranger can find the docs, follow them to a working install, and verify the thing works — and when the next engineer can read how it's built. Those artifacts rot the instant code changes, and nobody notices until a new user hits a broken install or a stale doc.

Three design choices make this reliable rather than theatrical:

1. **Scan before you write, from the real code — never from memory, and from the *right* code.** Every claim about a feature, a flag, an expected result, or an install step is derived from source, `--help` output, or a real run. Docs written from memory are how staleness enters. Just as important: derive the surface from **the version's tagged commit, not whatever happens to be in the working tree.** A working tree can be ahead of (or behind) the release you're documenting; testing `<version>` against the wrong tree silently mis-targets the whole run. When the tree and tag diverge, that divergence is itself a finding worth surfacing.
2. **Fan out to go deep, consolidate before you touch anything.** Read-only scanner agents build the inventory in parallel; a consolidator produces the coverage matrix and gap list; only then do writer agents create files. This keeps any one agent from having to hold the whole surface in context, and it gates all file creation behind a reviewed plan.
3. **Evidence and honesty are the whole point** (the release "golden rule"). A documented gap or a script that genuinely doesn't work *yet* is a **correct** outcome — report it. Never fabricate coverage, expected results, or an e2e pass. See `refs/golden-rule-evidence.md`; it governs every workstream and overrides any pressure to look complete.

---

## Wave 0: Prerequisites & Inputs

**Entry criteria:** the `/sc:post-release` command has invoked this skill with a `<version>` argument (and optional `--output <dir>`).

**Resolve inputs:**

- **Required:** `<version>` (e.g. `v1.4.1`). Resolve its tag: prefer an exact tag match (`git tag --list <version>`), else the tag whose name contains it. If the version isn't tagged yet, say so and confirm before proceeding — this protocol runs *after* the tag.
- **STOP** if no `<version>` argument is given — the protocol has no target release to work from.
- **STOP** if `<version>` resolves to no tag AND the user has not confirmed a pre-tag run — this protocol runs *after* the tag lands.
- **WARN** (and record as a release-integrity finding) if the resolved tag is not an ancestor of the mainline, or the working tree's version metadata disagrees with the tag — then continue, anchored to the tag.
- **WARN** if the output-directory convention is ambiguous — confirm, else use the default and state where artifacts landed.
- **Detect previous release tag** (for additive mode): `git tag --sort=-creatordate` and pick the highest tag strictly below `<version>` under the repo's version scheme. Record it; the diff uses `<prev_tag>..<this_tag>`.
- **Locate release artifacts** for this version: PRD/TDD/spec under the discovered release directory (commonly `.dev/releases/current/<version>/` or `.dev/releases/complete/<version>/`), plus `CHANGELOG.md` and `RELEASES.md` if present. Release dirs may be **tag-fuzzy** — a dir named `v1.3` for tag `v1.3.0`, or `v1-MVP` for the first GA — and may all live under `current/` (no `complete/`). If no per-version dir maps to the tag, treat `CHANGELOG.md` + `RELEASES.md` (and the version's section within them) as the release-intent source rather than assuming there is none.

**Golden-rule honesty discipline:** acknowledge up front (load `refs/golden-rule-evidence.md` once) that this protocol never fabricates coverage, expected results, or an e2e pass; a documented gap is a correct outcome.

**Output:** a validated input set (version, tag, previous-tag-or-none, release-artifact locations, output directory); `<output-dir>/audit.log` opened in append mode (see the "audit.log lifecycle" subsection under Wave 5 — the file is created here in Wave 0 so the RUN header can write to it in Wave 2).

**Exit criteria:** `<version>`/tag validated, previous tag detected or marked `none`, release artifacts located, output directory resolved, `<output-dir>/audit.log` opened, golden-rule discipline acknowledged.

---

## Wave 1: Tag / Branch / Release-Artifact Resolution + Run-Mode Detection

**Entry criteria:** the raw `<version>` argument has been validated in Wave 0.

**Anchor the scan to the tagged commit.** Once the tag is resolved, read the release's code surface **at that tag** — e.g. `git show <tag>:<path>`, `git ls-tree <tag>`, or a `git worktree add` / `git archive` checkout of the tag — rather than the current working tree. Confirm the tag actually belongs to the release lineage (`git merge-base --is-ancestor <tag> <default-branch>`); if it is **not** an ancestor of the mainline, or the tree's version metadata disagrees with the tag, treat that as a release-integrity finding and report it before proceeding. **Auto-detect the default branch** (e.g. `git symbolic-ref refs/remotes/origin/HEAD`) — do not assume `main`/`master`.

### Two run modes (auto-detect — do not ask)

Detect the mode from whether a prior manifest exists for this repo. Search these locations, newest first:
`.dev/releases/**/post-release-manifest.json`, `docs/testing/**/post-release-manifest.json`, and any `post-release-manifest.json` under the discovered release directory.

- **Ground-up (first run)** — no prior manifest found. Treat the whole external surface as needing a from-scratch pass across all five workstreams.
- **Additive (subsequent runs)** — a prior manifest exists. Compute the delta between the previous release tag and this one and do **incremental** updates only. Do **not** rewrite unchanged docs/scripts. The additive procedure — how to diff code + release PRD/TDD, map the delta to workstreams, and reconcile the manifest — is in `refs/additive-diff.md`.

State the detected mode and the evidence for it (found manifest path, or "none found → ground-up") in the report's header. When in genuine doubt, prefer ground-up for a workstream (a full pass is safe; a skipped delta is a silent gap).

**Output:** resolved tag + auto-detected default branch + chosen run-mode (ground-up vs additive) + located release artifacts.

**Exit criteria:** tag anchored, default branch auto-detected, run-mode ground-up vs additive chosen with stated evidence, release artifacts located.

---

## Wave 2: Surface Discovery + Install-Surface Classification

**Entry criteria:** resolved tag, default branch, and run-mode from Wave 1.

**Discovery is generic — hardcode no paths.** Different repos lay out docs, deploy assets, and e2e runbooks differently, so discover them at runtime rather than assuming. The concrete glob sets and classification rules live in `refs/workstream-playbook.md`; the short version:

| Surface | Where to look (examples, not requirements) |
|---|---|
| User docs (A) | `README.md`, top-level `*.md`, `docs/{user-guide,getting-started,guides}/**`, anything addressed to end users/operators |
| Technical docs (B) | `docs/{decisions,runbooks,developer-guide,reference,architecture,design}/**`, `ARCHITECTURE.md`, `docs/perf.md`, `docs/governance.md`, tech notes under `.dev/`; **API/contract surface** `proto/**`, `*.proto`, `*.pb.go`, `api/**`, `openapi*` |
| Install/deploy (C) | `deploy/**`, `install*.sh`, `configs/**`, `systemd/**`, `Dockerfile*`, `docker-compose*`, packaging manifests (`pyproject.toml`, `package.json`, `Cargo.toml`, `go.mod`…), `charts/`/`helm/`, `.github/workflows/*deploy*`, Makefile build/install targets, **DB schema** `migrations/**`/`*.sql`/`db/**` |
| E2E/VM target (C) | runbooks matching `*e2e*`/`*vm-access*`/`*deploy*`; files naming a throwaway/deploy VM and its access coordinates |
| Release (mode + delta) | `.dev/releases/**`, `CHANGELOG.md`, the version tag |

If a surface genuinely doesn't exist in this repo, that is a finding, not an error — record it and (where useful) propose the missing artifact rather than inventing a fake target.

### Install-surface classification (Workstream C)

The install surface is classified into one of four classes, **decided from discovery evidence, not assumed** — a Go/Docker service is VM/e2e or local-deploy, a Python/npm package is package class, and so on:

- **`vm-e2e` class** — deploy scripts + an e2e/VM runbook with target coordinates → provision the throwaway VM per the runbook, run clean-state → working-install, capture the transcript.
- **`local-deploy` class** — deploy scripts but no VM (compose/local) → run to green in a clean local container/env.
- **`package` class** — ships as a language package (pyproject/package.json/Cargo/…) with no deploy scripts → validate the real install path in a **fresh throwaway environment** (clean venv / container / `pipx install .` / `npm i -g` / `go install`), then exercise the entry point (`--version`, `--help`, a smoke command).
- **`no-install-surface` class** — nothing installable → say so honestly, propose an install quickstart, and do **not** fabricate a pass.

Record the chosen class and the evidence in the manifest and report.

**Output:** discovery-glob coverage across A/B/C/D/E surfaces + the classified install-surface class.

**Exit criteria:** the four install-surface classes have been considered and one chosen with stated evidence; every surface either located or honestly recorded as absent.

---

## Wave 3: Per-Workstream Planning + Scanner Fan-Out + Consolidated Coverage Matrix

**Entry criteria:** classified install surface + generic discovery globs from Wave 2.

### Controller behavior (per workstream)

For **each** workstream, first weigh complexity and risk, then pick the lightest approach that will actually hold:

- **One-shot** — if the objective is small and low-risk (a handful of docs, an obvious update, no real e2e needed), just do it directly: scan → consolidate → write. Don't build machinery you won't use.
- **Decompose** — if the surface is large, the gaps are many, the change is cross-cutting, or it needs real e2e validation, run the full loop:
  1. **Research/scan** — fan out read-only scanner agents (see `refs/fan-out-pattern.md`).
  2. **Design an itemized worklist** — if the host project provides a task-decomposition / itemized-tasklist tool, reuse it **only if it's actually loadable**, so writing/creation is checklist-driven and verifiable. Probe for the tool's availability; a task-directory convention on disk means the *format* has been used before, not that the tool is installed.
  3. **Execute** — run the worklist through the project's task-execution loop, or directly if it has none.
  4. **Verify** — run a reflection/verification gate (the project's, if it ships one) over the produced/edited files against the coverage plan before declaring the workstream done.

Prefer parallel fan-out for the scanning phase in both paths; consolidate to a single coverage matrix + gap list before any file is written. The judgment of one-shot vs. decompose is per workstream — B might be one-shot while D is a full tasklist.

**Portability — these reuse hooks are optional.** A task-decomposition tool, a task-execution loop, and a reflection/verification gate are conveniences some projects ship, not requirements. In a repo that has none of them, do **not** fabricate or hard-depend on them: fall back to a direct `scan → consolidate → write` pass with your own inline verification (re-read created/edited files against the coverage plan and the code), and note in the report that the heavier tooling wasn't available. The five-workstream logic, discovery, mode detection, and the manifest are fully portable on their own.

### Fan-out / agent-team pattern

Every workstream uses the same team shape, described fully in `refs/fan-out-pattern.md`:

1. **Scanners (read-only, parallel)** — partitioned by directory or feature area. They build inventory and never write source/doc files. Keeping them read-only is what lets you run many at once without them stepping on each other or on the repo.
2. **Consolidator** — dedups the scanner inventories into one coverage matrix (feature × doc/guide/script) and an explicit gap list. This is the gate: nothing gets created until the plan is consolidated.
3. **Writers/creators** — each takes a consolidated, approved item and updates or creates one artifact. For large/creation-heavy workstreams, route the writers through an itemized tasklist + execution loop (the project's, if it has one) rather than free-handing them.

**Output:** a five-workstream (A–E) plan + a consolidated coverage matrix + an explicit gap list.

**Exit criteria:** the per-workstream one-shot-vs-decompose decisions are made, scanners have fanned out read-only, and the consolidator has produced a single coverage matrix + gap list that gates all file creation.

---

## Wave 4: Artifact Updates / Creation + Workstream C e2e Evidence

**Entry criteria:** consolidated coverage matrix + gap list from Wave 3.

### The five workstreams

Each follows the same shape — **scan → consolidate (coverage matrix + gap list) → update existing → create missing → verify**. Full per-workstream playbooks (scanner partitions, what "update" means, what counts as a gap, acceptance) are in `refs/workstream-playbook.md`. Summaries:

**A — User documentation.** Scan all user-facing docs, map them to the release's features, update them to reflect `<version>`, and create the user docs that should exist but don't. Keep the audience straight: user docs are for people *using/operating* the software, not building it. A feature that shipped in `<version>` with no user-facing mention is a gap.

**B — Technical documentation.** Same discipline for engineering docs — decisions/ADRs, runbooks, architecture/design notes, perf, governance, tech references. Update them to reflect how `<version>` is actually implemented; detect and create missing technical docs. Verify claims against real code (a doc that describes a call chain must match the source).

**C — Install & deploy scripts (with real e2e validation).** Scan every install/deploy asset and make the new-user setup for `<version>` correct and easy. This workstream is only "done" when the install path has been **run to green on a real target** and the transcript captured as evidence. The target depends on the repo's install surface — this is the **discover-and-adapt** part, detailed in `refs/workstream-playbook.md#workstream-c`. The four classes (`vm-e2e`, `local-deploy`, `package`, `no-install-surface`) were classified in Wave 2. A script that hasn't been run to green is not "done." If it fails, report the failure with the transcript — that's a valid, valuable outcome.

**D — User-facing e2e human-test guides.** Scan every user-facing functional feature to learn its purpose, correct usage, and expected behavior *from the code*, then author walkthrough documents that take a human tester through each capability: **preconditions → actions → expected result → pass/fail**. These are authored guides for a person to run by hand, not automated tests. Expected results come from real code, never guesses. One guide per capability (or cohesive capability group); together they must cover the user-facing surface. Use `templates/user-test-guide.md`.

**E — Sysop-facing e2e human-test guides.** First **determine whether sysop-only capabilities even exist** — gated admin/debug/overlay/spawn/watch/maintenance features, privileged flags, operator-only commands. If they do, author matching human-test guides with `templates/sysop-test-guide.md`. If they don't, **say so explicitly** — "no sysop-only surface found in `<version>`" is the correct deliverable; do not invent coverage to look thorough.

### Workstream C e2e — run to green

Run the install path to green on the classified target (from Wave 2); capture the transcript. Honestly report a red result — a real install failure with the failure point + transcript is a valid outcome, never mark C done on a failed or un-attempted install.

**Output:** updated + newly-created user docs (A), technical docs (B), install/deploy scripts (C), user-facing test guides (D), sysop-facing test guides (E); Workstream C real-install e2e evidence captured (or an honest RED account).

**Exit criteria:** each workstream's existing artifacts updated, gaps created, Workstream C e2e run to green (or honestly RED), per-workstream verification gate passed.

---

## Wave 5: Validation / Report / Manifest / Return-Contract

**Entry criteria:** draft artifacts from Wave 4.

### Reference files (load on demand — do not pre-load)

Keep only the ref(s) for the current phase in context (progressive disclosure / lazy-loading):

| Ref | Load when |
|---|---|
| `refs/golden-rule-evidence.md` | once, up front — the honesty discipline governs every workstream |
| `refs/fan-out-pattern.md` | before spawning any workstream's scanner → consolidator → writer team |
| `refs/workstream-playbook.md` | when executing a specific workstream (scan partitions, gap criteria, acceptance; `#workstream-c` for install classification) |
| `refs/additive-diff.md` | only in additive mode (a prior manifest was found) |

### Outputs & artifacts

- Updated + newly-created **user docs (A)**, **technical docs (B)**, **install/deploy scripts (C)**, **user-facing test guides (D)**, **sysop-facing test guides (E)**.
- **`post-release-report.md`** — the per-run summary. For each workstream: what was scanned, what was updated, what gaps were found, what was created, and — for C — the full e2e validation transcript (or an honest account of why it couldn't run to green). Use `templates/post-release-report.md`.
- **`post-release-manifest.json`** — the machine-readable record the *next* run diffs against: version, tag, previous tag, run mode, install-surface class, per-workstream files touched/created, feature inventory, and coverage checklist. Use `templates/post-release-manifest.json`.
- **Test guides** land in a discoverable location — default `docs/testing/<version>/` (fall back to `.dev/releases/current/<version>/test-guides/` if the repo keeps release artifacts under `.dev/`). Put the report + manifest alongside them (or under the release directory) so the pair travels together.

Confirm the exact output directory with the user if the repo's convention is ambiguous; otherwise use the default and state where things went.

### audit.log lifecycle

`<output-dir>/audit.log` is the durable, machine-readable record of every `SC:POST-RELEASE:RUN` / `SC:POST-RELEASE:RESULT` emission across runs of this protocol against the same output directory.

- **Creation** — once `<output-dir>` is resolved in Wave 0, open `<output-dir>/audit.log` in **append mode** (`>>`). If the output dir is not writable, fail loudly at that point (this is a hard error in Wave 0, not a deferred one — a non-writable audit sink must block the run, since every later header emission depends on it).
- **RUN line** — the RUN header is appended as the first `SC:POST-RELEASE:RUN` line in the file (it is the first run against this dir, or appends after any prior run's lines).
- **RESULT line** — the RESULT header is appended as the last matching `SC:POST-RELEASE:RESULT` line for this run.
- **Aborted runs** — on a non-zero exit / abort before RESULT, append a final `{wave: exit, status: aborted, reason}` line so the audit log records why the run did not reach RESULT.
- **Chat-side mirroring** — the chat-side RUN/RESULT messages mirror the first and last matching audit.log lines for this run (the chat is the authoritative channel; the file is durable evidence).

### Machine-readable headers

This protocol emits two HTML-comment header blocks (style follows `sc-auggie-review-protocol/SKILL.md` and the dev-guide "Machine-Readable Headers" spec). The RUN header opens the run; the RESULT header closes it.

**Field sources.**

- `caller` — the slash command that invoked this skill: `/sc:post-release` if invoked directly; the parent skill name if invoked from another skill; `none` if invoked interactively without a slash command.
- `mcps_available` — the pipe-joined subset of `{auggie, serena, context7, tavily, sequential}` whose tools are present in the runtime tool list this session; `none` if empty. Presence in the tool list is the only signal — do NOT probe network endpoints, and note the tool list may be a superset of the frontmatter `mcp-servers`.
- `duration_sec` — integer wall-clock seconds between the moment the RUN header is emitted and the moment the RESULT header is emitted. It appears ONLY in a RESULT header (it is meaningless without one). If the run aborts before emitting RESULT, do NOT synthesize a RESULT block just to carry `duration_sec`; instead append a final `{wave: exit, status: aborted, reason, elapsed_sec}` line to `audit.log` (see "audit.log lifecycle" → Aborted runs) and surface the abort reason in chat — the RESULT block (and therefore `duration_sec`) is emitted only on runs that reach RESULT.

**RUN block — the RUN header is the FIRST chat message whose body is an HTML-comment `SC:POST-RELEASE:RUN` block, emitted immediately after Wave 2 completes (the install-surface class is chosen and the consolidated input set is locked). Waves 0–2 may emit progress messages before it. It is also the first `<output-dir>/audit.log` line (see the audit.log lifecycle below):

```text
<!-- SC:POST-RELEASE:RUN
version: {{version}}
previous_tag: {{previous_tag|none}}
run_mode: {{ground-up|additive}}
install_surface_class: {{vm-e2e|local-deploy|package|no-install-surface}}
output_dir: {{abs-output-dir}}
report_path: pending
manifest_path: pending
caller: {{caller|none}}
mcps_available: {{auggie|serena|context7|tavily|sequential|none}}
-->
```

**RESULT block — emit as the final chat message + final `<output-dir>/audit.log` line + first HTML-comment block at the top of `post-release-report.md`:**

```text
<!-- SC:POST-RELEASE:RESULT
status: {{success|partial|failed}}
run_mode: {{ground-up|additive}}
install_surface_class: {{vm-e2e|local-deploy|package|no-install-surface}}
report_path: {{abs-path}}
manifest_path: {{abs-path}}
workstream_results: {{"A":{"updated":N,"created":N,"gaps":N,"verified":bool},"B":{...},"C":{...},"D":{...},"E":{...}}}
c_e2e_result: {{green|red|carried-forward|not-applicable}}
gap_list: {{[{workstream,gap,evidence,remedy},...]}}
duration_sec: {{N}}
-->
```

The RESULT block carries the 8 return-contract fields tabulated below PLUS the convention-only `duration_sec` field (per research file 07 §3, `duration_sec` is explicitly a convention — not part of the return contract; it appears only in the RESULT header so the run's wall-clock duration is grep-able alongside the other scalars). `workstream_results` and `gap_list` are emitted as single-line JSON to preserve the grep-ability of the scalar fields. Do not add `duration_sec` to the Return Contract table — the asymmetry (9 header fields, 8 contract fields) is intentional and spec-correct.

**Emission failure (dual-channel semantics).** The chat emission of RUN and RESULT is mandatory: the run must not be considered to have started until the RUN block appears in the chat, and must not be considered finished until the RESULT block appears in the chat. The file emissions are tiered: (1) the **`audit.log` line for RUN/RESULT** is a hard dependency — the audit sink's writability is established once in Wave 0 (see "audit.log lifecycle" Creation bullet), so by emission time the file is already open and a write failure there is an unexpected runtime error, recorded as a `release_integrity_findings`-style note and retried; (2) the **top-of-report HTML comment for RESULT** is best-effort — if `post-release-report.md` cannot be opened at RESULT time, record the failure as a `release_integrity_findings`-style note in the report body (or in the chat if the report itself is the thing that can't be written) and continue, since the chat emission is the authoritative channel. A missing file emission is never silent. (The Wave 0 hard-stop covers only the initial audit-sink open; later best-effort handling covers transient/runtime write failures and the report file, not a re-litigation of the Wave 0 writability gate.)

### Return contract

On completion, report these fields (and emit the RESULT header above) for a calling command/skill or the user:

| Field | Type | Description |
|---|---|---|
| `status` | string | `success`, `partial`, or `failed` |
| `run_mode` | string | `ground-up` or `additive` |
| `install_surface_class` | string | `vm-e2e`, `local-deploy`, `package`, or `no-install-surface` |
| `report_path` | string | path to `post-release-report.md` |
| `manifest_path` | string | path to `post-release-manifest.json` |
| `workstream_results` | map | per-workstream A–E: `{updated, created, gaps, verified}` |
| `c_e2e_result` | string | `green`, `red`, `carried-forward`, or `not-applicable` (+ transcript path) |
| `gap_list` | list | honest gaps across all workstreams (each: workstream, gap, evidence, remedy) |

### Error handling

| Scenario | Behavior | Fallback |
|---|---|---|
| No `<version>` argument | STOP with a clear message | none |
| `<version>` not tagged | STOP; confirm a pre-tag run before proceeding | none |
| Tag not an ancestor of mainline / tree version disagrees | WARN, record as a release-integrity finding, continue anchored to the tag | report the defect |
| A discovery surface is absent (no deploy assets, no sysop surface) | Record as a finding; propose the artifact where useful | honest "none", never fabricate |
| Workstream C e2e cannot reach green | Report RED with the failure point + transcript; do NOT mark C done | valid honest outcome |
| A fan-out scanner/subagent fails | Retry once, then proceed with the remaining scanners; note reduced coverage | narrow the partition |
| No task-decomposition / reflection tooling in this repo | Fall back to a direct scan→consolidate→write with an inline verification pass | note the reduced rigor |
| Secret appears in an e2e transcript | Scrub before saving; never commit | redacted transcript |

**Output:** `post-release-report.md` + `post-release-manifest.json` written; golden-rule honesty check passed; RUN/RESULT headers emitted at the right wave boundaries; 8 return-contract fields emitted (plus the convention-only `duration_sec` in the RESULT header).

**Exit criteria:** report + manifest written, golden-rule honesty check passed (no fabricated coverage/results/e2e pass), RESULT header emitted as the final chat message + final audit.log line + first block of the report, and all 8 return-contract fields populated (the RESULT header additionally carries `duration_sec` as a convention-only field; see the header-block prose above).

---

## Execution overview

1. **Wave 0 — Resolve inputs** — validate `<version>`/tag; detect previous tag; locate release artifacts.
2. **Wave 1 — Detect mode** — ground-up vs additive (manifest search); state the evidence.
3. **Wave 2 — Discover surfaces** — generic globs for A/B/C/D/E targets; classify the install surface (C).
4. **Wave 3 — Per workstream A→E** — decide one-shot vs decompose; fan out scanners; consolidate to coverage matrix + gap list.
5. **Wave 4 — Update/create + Workstream C e2e** — update existing; create gaps (via the project's tasklist tooling when heavy); run Workstream C e2e to green; run the reflection/verification gate.
6. **Wave 5 — Assemble + present** — write `post-release-report.md` and `post-release-manifest.json`; emit RUN/RESULT headers; summarize per-workstream results, the coverage matrix, the honest gap list, and where every artifact landed. Offer the commit/PR as a next step (see guardrails).

---

## Boundaries

**Will:**

- Scan the real code **at the release tag**, fan out read-only scanners, consolidate a coverage matrix + gap list, then update/create the external-surface artifacts (A–E).
- Run the new-user install/deploy path to green on the classified target and capture the transcript as evidence.
- Report gaps, stale docs, and RED installs honestly, and write a manifest that makes the next release additive.

**Will Not:**

- Fabricate coverage, expected results, or an e2e pass; mark a workstream "done" without evidence.
- Write source/docs/scripts before the consolidated-plan gate, or let a read-only scanner mutate the repo.
- Commit, push, open a PR, provision a VM, or run installs against a shared/real target without confirmation (or standing authorization).
- Stage a host repo's machine-generated / sync-output directories, retarget a PR at anything other than the repo's own `origin`, or write secrets into any artifact.

---

## Guardrails

- **Branch discipline** — work on a feature branch off the repo's **auto-detected default branch**; never commit directly to that branch. Commit/push only when the user asks.
- **PR target** — open PRs against the repo's own `origin`, with `--base <default-branch>` and its contribution conventions. **Never retarget a PR at anything other than `origin`** (a fork's upstream, or any other repo) without explicit user authorization in the same session. A wrong PR target is a high-cost mistake — especially when a plausible sibling repo exists in the same org, which is exactly when a hardcoded owner/name would misfire. Resolve the target from `git remote -v` at runtime, never from memory.
- **Never stage machine-generated / sync-output dirs** — respect whatever the host repo marks as generated or vendored (check its `.gitignore` and docs) and don't `git add` those paths. Note the convention varies: some repos gitignore such dirs, others commit them — follow the host repo's actual practice, don't assume.
- **No secrets, ever** — deploy creds/tokens live only on the target host. Never write them into docs, scripts, transcripts, or the manifest. Scrub any that appear in an e2e transcript before saving it.
- **Confirm outward-facing / hard-to-reverse actions** — provisioning a VM, running install scripts against a real target, committing, and opening a PR all get confirmed first unless the user pre-authorized them this session.
- **Additive path is first-class** — even on a ground-up run, write the manifest cleanly and completely so the next release's additive diff is trivial. A good manifest now is what makes future runs incremental instead of another full pass.
- **Respect the host repo's own conventions** — a project may have its own contribution rules (PR targets, protected paths, generated dirs that must not be staged). Read them from the repo (`CONTRIBUTING`, its agent/AI guidance file, `.gitignore`) at runtime and follow them; never carry one project's rules into another's output.
- **Skill directory MUST be named `sc-post-release-protocol`** — not the bare `sc-post-release`. The installer's `_has_corresponding_command` helper in `src/superclaude/cli/install_skills.py` strips only the `sc-` prefix when deciding whether a skill is "served by a command"; a bare `sc-post-release` would be treated as served-by-command (`post-release`) and silently skipped during a standalone `superclaude install`. The `-protocol` suffix defeats that match and ensures the skill is installed on its own.
