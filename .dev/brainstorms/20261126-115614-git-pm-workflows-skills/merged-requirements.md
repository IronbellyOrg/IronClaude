---
topic: "Embed more Git and PM related workflows into skills @.dev/issues/326/issue-summary.md"
domain: architecture
strategy: systematic
depth: deep
adversarial_status: pass
convergence_score: 1.0
proposals: 3
blind: true
source: adversarial/adversarial/merged-output.md
created: 2026-11-26T16:30:00Z
---

<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant A -->
<!-- Merge date: 2026-11-26T15:54:27Z -->

# Requirements Specification: Modular `/sc:git`, Authorized Between-Task Commits in `/sc:implement`, and Submodule Operations (issue 326)

<!-- Source: Base (original) -->

Persona: architect. Priority: maintainability and extension scaffolding. Date: 2026-11-26.
Sources: `seed-brief.md`, `enrichment/codebase-context.md`, `enrichment/research-deep.md` (same brainstorm folder), `.dev/issues/326/issue-summary.md`, `.dev/issues/326/analysis/analyze-git.md`, and a read-only check of the repository in this worktree.

## 1. Overview and scope

<!-- Source: Base (original, modified) - subsections 1.6 Root causes, 1.7 Terms and 1.8 Seed constraints kept added per Changes #3, #2 and #39 -->

### 1.1 Notation

<!-- Source: Base (original, modified) - table given a "How to resolve" column and the <skill-dir>, <pkg-dir>, <run-dir> and <root-instructions> rows from Variant B, Path notation; aliases of Variants B and C mapped; merged per Change #1 -->

Some real paths contain the package name. This document writes them with the placeholders below. Each placeholder stands for exactly one real location that was checked in this worktree.

| Placeholder | Meaning | How to resolve |
|---|---|---|
| `<package>` | The single package directory name under `src/`, and the plugin folder name under `plugins/` | `ls src/` lists one entry; `pyproject.toml:6` (`name = ...`) |
| `<pkg>` | `src/<package>/`, the source of truth for commands, skills, agents, core files, hooks and package code | `pyproject.toml:79` (`packages = [...]`) |
| `<plugin>` | `plugins/<package>/`, the plugin mirror that the plugin build copies unchanged | `scripts/build_<package>_plugin.py:16` (`PLUGIN_SRC`) |
| `<cli>` | The package's console command. Installed primitives already call it, for example `<cli> review safety-scan` | `pyproject.toml:70-71` (`[project.scripts]`) |
| `<home>` | The per-user agent-host configuration directory that `<cli> install` writes to. It holds installed copies such as `<home>/commands/sc/`, `<home>/skills/`, `<home>/WORKER-CONTRACT.md` and `<home>/HOW-WE-WORK.md` | `<pkg>/cli/install_commands.py:29` |
| `<dev>` | The project-local, gitignored agent-host directory that `make sync-dev` fills | `Makefile:109-163`; `.gitignore:127-135` (tracked exceptions, see §1.5) |
| `<skill-dir>` | The resolved copy of the `/sc:git` protocol skill: `<home>/skills/sc-git-protocol/` first, then `<dev>/skills/sc-git-protocol/` (skills read the installed copy first) | The dual-surface rule in `<root-instructions>` |
| `<pkg-dir>` | The managed task package of the current `/sc:implement` run: the directory under `.dev/tasks/` that holds the plan, its ledger and its `artifacts/` | The managed ledger path, `refs/managed-workspace.md` |
| `<run-dir>` | The legacy run directory `.dev/implement/<slug>/` | `refs/ledger.md:7` |
| `<root-instructions>` | The repository's root agent-instructions file that holds the "ABSOLUTE RULE" sections | Repository root |
| `<Product>` | The capitalized product name used as a prefix in one developer-guide file name | `ls docs/developer-guide/` |

**Aliases used by the source variants.** The merge mapped these aliases onto the table above: Variant B `<name>` = `<package>` (and `<name> install`, `<name> issue-pipeline` = `<cli> install`, `<cli> issue-pipeline`); Variant B `<pkg-dir>` = `<pkg-dir>`; Variant B `<skill base>` = `<skill-dir>`; Variant B "root instructions file" = `<root-instructions>`; Variant B "developer guide" = `docs/developer-guide/<Product>-Developer-Guide-Commands-Skills-Agents.md`; Variant C `S`, `P`, `D`, `G` = `<pkg>`, `<plugin>`, `<dev>`, `<home>`; Variant C `<managed package>` = `<pkg-dir>`; Variant C `<legacy run>` = `<run-dir>`. Every implement ref is written `refs/<package>/implement/<slug>/...`. This document contains no model or vendor name; the placeholders above stand for paths that contain the package name.

### 1.2 Problem

<!-- Source: Base (original) -->

`/sc:git` (`<pkg>/commands/git.md`, 91 lines) is a prose command. It has no Options table, no STOP rules, no Activation, no submodule text and no backing skill. Its usage line is `/sc:git [operation] [args] [--smart-commit] [--interactive]` (line 22). It still shows a `merge ... --interactive` example (lines 72-77).

`/sc:implement` lists "Auto-commit, open PRs, or release" as a Will Not (`<pkg>/commands/implement.md:100`). Because of that, a long plan lands as one uncommitted change.

### 1.3 In scope

<!-- Source: Base (original, modified) - item 1 names a helper script in the protocol skill instead of the package CLI, per Change #6 -->

1. A modular `/sc:git`: a command file that follows the developer guide, a protocol skill with one ref per operation group, and a small read-only helper script in the protocol skill. The plugin mirror and the dev copy are kept in sync, and the legacy root copy is retired.
2. An explicitly authorized local commit between tasks in `/sc:implement`. It never runs inside a task or inside a parallel batch, and it reports a refused hook instead of bypassing it.
3. Defined submodule operations in `/sc:git`: status, update, and a pointer commit, under the same authorization rules.
4. Branch cleanup by reuse only. `/sc:git` routes to `/sc:worktrees`, which runs `scripts/worktree_cleanup.py` from PR 711.

### 1.4 Explicitly out of scope (decided)

<!-- Source: Base (original, modified) - standards reference renumbered to §4 per Change #5; push/fetch bullet states the one submodule update exception per Change #30 -->

- A central relay through which every command calls `/sc:git`. Commands cannot call another session, and `/sc:git` stays on the never-as-worker list (`<pkg>/core/WORKER-CONTRACT.md:23`).
- Push, pull, merge, rebase, PR creation and PR review, and any fetch `/sc:git` would make on its own. `/sc:git` never pushes; `submodule update` may clone or fetch from the `.gitmodules` URL only as FR-041 and FR-044 authorize (on the person's typed `submodule update` line after the network effect is disclosed, and for a clone only when that line repeats the URL; the one exception in NFR-001). PRs stay with `/sc:pr-submit`, which is also the only push path here (`<pkg>/core/WORKER-CONTRACT.md:245`).
- Remote branch deletion, anywhere.
- A second implementation of local branch cleanup. `_remove_branch` in `scripts/worktree_cleanup.py:2636-2647` stays the only one.
- Any change to the level table in `<pkg>/core/HOW-WE-WORK.md`. That table is copied into the core instructions file, so a change there would spread to every install.
- Fixing `docs/developer-guide/git-standards-protocols.md`. §4 explains why it conflicts with the hook this repository enforces.
- Nested submodules (submodules of submodules), `git submodule foreach`, and `update --remote`.
- New project-management workflows. Decision D6 explains why.

### 1.5 Baseline facts (verified in this worktree)

<!-- Source: Base (original, modified) - the conventional-pre-commit row replaced (hooks are configured, not installed; from Variant B, Section 10 R11) and a tracked <dev>/ files row added; merged per Change #4 -->

| Fact | Evidence |
|---|---|
| The source and plugin copies of `git.md` are byte-identical | `diff <pkg>/commands/git.md <plugin>/commands/git.md` exits 0 |
| The legacy root copy has a doubled prefix (`# /sc:sc:sc:git`, usage `/sc:sc:git`), 79 lines, last touched by commit `ff5f73adf` ("automated sync and namespace isolation from framework", 2026-07-22) | `commands/sc-git.md:10`, `:19`; `git log -- commands/sc-git.md` |
| Nothing installs or builds from the root `commands/` folder. Install reads `<pkg>`, and the plugin build reads `<plugin>`. The folder's README is stale (it says to edit `plugins/` first and mentions "v5.0") | `scripts/build_<package>_plugin.py:16,76`; `commands/sc-README.md` |
| The README of the commands folder names four plugin-mirrored commands (help, recommend, workflow, implement), and a test enforces it | `<pkg>/commands/README.md:9`; `tests/commands/test_routing_plugin_parity.py:41-47` |
| The plugin must ship the implement protocol with the same file set as `<pkg>` | `tests/commands/test_workflow_command.py:204-217` |
| `/sc:git` is never a worker | `<pkg>/core/WORKER-CONTRACT.md:23`; `tests/skills/test_worker_contract.py:474-485` |
| Per-task commits are parked here (K3): "only between a task's `complete` line and the next task's start, never inside a parallel batch" | `<pkg>/core/WORKER-CONTRACT.md:42` |
| A worker's own commit uses `git add -- <paths>` plus `.dev/tasks` and `git commit --only -- <paths>`. It never uses `--no-verify`, and "a command's own commit step stays off under `--unattended`" | `<pkg>/core/WORKER-CONTRACT.md:43` |
| The retry ladder requires HEAD unchanged during a task (`q0-head`) and excludes submodule paths from the revert | `<pkg>/skills/sc-implement-protocol/refs/retry.md:41`, `:212` |
| A legacy ledger under `.dev/implement/` is never staged. A managed ledger is under `.dev/tasks/`, which is always staged | `refs/ledger.md:3`; `refs/managed-workspace.md:36` |
| Resume treats any last line outside the known record kinds as `E-LEDGER-CORRUPT` | `refs/ledger.md:127` |
| The managed archive helper raises `E-ARCHIVE-LEDGER` on any line it cannot parse | `<pkg>/skills/sc-implement-protocol/scripts/archive_workspace.py:181-202` |
| The implement STOP table is closed: "No other `E-*` codes besides the rows above" | `<pkg>/skills/sc-implement-protocol/SKILL.md:51` |
| Parallel batches hold up to 3 tasks, write every member's `start` line before any member begins, and get no retry ladder | `SKILL.md:108-110` |
| The repository *configures* `conventional-pre-commit` at the `commit-msg` stage, and `markdownlint --fix`, `ruff-format`, `mixed-line-ending --fix=lf`, `end-of-file-fixer`, `check-added-large-files --maxkb=1000` and `detect-secrets` can rewrite or refuse files during a commit. In this clone none of these hooks is installed: the common hooks directory holds only `pre-push`, `pre-push.launch-level` and `*.sample`, and `core.hooksPath` is unset. Configured hooks are therefore not enforcement; the helper validates the message itself (FR-066) | `.pre-commit-config.yaml:9-45`, `:78-91`, `:130-134`; runtime check of the common hooks directory and `core.hooksPath` (2026-11-26) |
| `git ls-files <dev>/` lists `<dev>/settings.json` and `<dev>/cache/sc-recommend-lookup.yaml`; `.gitignore:127-135` keeps the cache entries as user-authorized exceptions. The project rule allows staging only `settings.json` without an explicit instruction in the session | `git ls-files <dev>/`; `.gitignore:127-135`; `<root-instructions>` |
| The launch-level guard blocks commits below level `full --submit` (`LL-COMMIT`), treats any push to `master`, `main` or `integration` as protected (`LL-PROTECTED`), classes `--no-verify` as TAMPER, and advises `git commit -F <file>` | `<pkg>/hooks/scripts/launch-level-guard.sh:46-49`, `:58-60`, `:135`, `:786` |
| The GitHub default branch is `integration`, but in this clone the local `refs/remotes/origin/HEAD` resolves to `origin/master` | `docs/developer-guide/branch-protection.md:16`; `git symbolic-ref --short refs/remotes/origin/HEAD` printed `origin/master` |
| The sweep probes run git as `git --no-optional-locks -C <path> -c core.fsmonitor=false` with `--ignore-submodules=all`, because a submodule's own config could start a program (issue 547) | `<pkg>/cli/sweep/probes.py:64-76` |
| The repository has one submodule under `.vendor/`, and it is uninitialized in this worktree (`-` prefix) | `.gitmodules`; `git submodule status` |
| The installed git is 2.47.3 | `git --version` |
| PR 711 cleanup deletes local branches with `git branch -d` only and refuses `-D`, `--force` and `--delete` | `scripts/worktree_cleanup.py:392`, `:2642`; `tests/worktree_cleanup/test_removal.py:209-211` |
| `/sc:worktrees` is for a person only, runs only in a checkout that has `scripts/worktree_cleanup.py`, and never deletes a remote branch | `<pkg>/commands/worktrees.md:17`, `:45`, `:80` |
| The routing fixture S23 says `/sc:git` is `self-contained`, expects `--smart-commit`, and pins three phrases from the routing guide | `tests/recommend/fixtures/routing_refresh_cases.json:312-331`; `tests/recommend/test_routing_refresh.py:482-496` |
| The worker-contract scan pins the two current `git.md` examples (`commit --smart-commit`, `merge feature-branch --interactive`) | `tests/skills/test_worker_contract.py:2945-2960` |
| A precedent exists for running a step "only when the user's own message starts with" a command line | `<pkg>/core/WORKER-CONTRACT.md:346` (`/sc:graph init`) |

### 1.6 Root causes

<!-- Source: Variant B, Section 2 (RC-1..RC-7), shortened, aliases mapped, front-matter sentence of RC-5 and tool names of RC-7 dropped; RC-6 plugin-parity point also in Variant C, Distribution (FR-009) - merged per Change #3 -->

§1.5 says what holds today. Each root cause below is a falsifiable claim, with its evidence, about why the design is constrained.

- **RC-1. `/sc:git` predates the command, skill and refs architecture, and tests pin its old shape.**
  - The developer guide makes a command a thin dispatch stub of about 80-150 lines with an `## Activation` handoff (`docs/developer-guide/<Product>-Developer-Guide-Commands-Skills-Agents.md:53`, `:63-75`). `git.md` has no `## Activation`, no `## Options`, no STOP rules and no `argument-hint` (`<pkg>/commands/git.md:1-91`).
  - Routing case S23 asserts that `/sc:git` is `"self-contained"` (`tests/recommend/fixtures/routing_refresh_cases.json:325`, enforced by `tests/recommend/test_routing_refresh.py:483-496`), and its two examples are pinned by exact text in the write-verb classification table (`tests/skills/test_worker_contract.py:2945-2960`).
  - Any refactor therefore has a guaranteed test cost.
- **RC-2. "A commit needs authorization" was written as prose with no mechanism behind it.**
  - The routing guide says "a commit needs authorization" (`HOW-WE-WORK.md:293`) but never says what counts as authorization. `/sc:implement` simply forbids commits (`implement.md:100`), and the worker contract parks per-task commits on this issue (K3, `WORKER-CONTRACT.md:42`).
  - The only mechanical commit gate is the launch-level guard. It governs only sessions the claim script launched ("every other session is ordinary and never blocked", `<pkg>/hooks/scripts/launch-level-guard.sh:5-7`) and allows `COMMIT` only at level `full --submit` (`:806-808`).
  - The project settings have no deny rule for `git commit` or `--no-verify` (the git-related permission entries in `<dev>/settings.json` contain none), and prompt-only rules are advisory in practice (`research-deep.md` §1). With nothing to build on, the only safe default was "never commit".
- **RC-3. `/sc:implement`'s recovery design depends on HEAD staying still.**
  - The retry ladder needs HEAD unchanged since the task's Q0 (`refs/retry.md:41`; `halt ... reason=head-moved`, `:454`). The coordinator's resume check requires HEAD to equal `<retries>/T<id>/q0-head` (`WORKER-CONTRACT.md:280`), and a frozen plan forbids any git command that moves HEAD (`:266`).
  - Q0 pins each task's start tree as `refs/<package>/implement/<slug>/T<id>` and deletes the pin at `complete` (`<pkg>/skills/sc-implement-protocol/SKILL.md:123-129`).
  - The ledger grammar is closed: an unknown last line is `E-LEDGER-CORRUPT` (`refs/ledger.md:127`). A commit inside a task would trip `head-moved`, and a new ledger record type would break resume parsing and the archive helper's ordering checks (`refs/managed-workspace.md:93`). These coupled constraints are why K3 was parked.
- **RC-4. Submodules were only ever handled defensively at the edges, and automation is shut out on purpose.**
  - Every existing consumer refuses or ignores submodules: `/sc:pr-submit` halts on a submodule conflict (`<pkg>/commands/pr-submit.md:71`; `<pkg>/pr_submit/conflicts.py:733`); the sweep passes `--ignore-submodules=all` because a submodule's own config could start a program (issue 547, `<pkg>/cli/sweep/probes.py:64-76`); the implement revert leaves gitlinks out and prints `SUBMODULE <p> <sha>` for a person to fix (`refs/retry.md:212`).
  - The launch-level guard's allow-table has no `submodule` subcommand (`launch-level-guard.sh:720`). It falls to `UNKNOWN` (`:724`), which is denied at every launch level (`:816`).
  - No command owns the positive operations, so none was ever defined (`analyze-git.md` F5). The repository's one submodule, under `.vendor/`, is not initialized in this checkout, so the code paths are real but rarely exercised.
- **RC-5. The "standards" the issue points to are not this repository's standards.**
  - `docs/developer-guide/git-standards-protocols.md` belongs to another project: its front matter id is `GFXAI-GIT-STANDARDS-PROTOCOLS` (`:2`) and its status is "To Do" (`:6`). It prescribes `main` as the only long-lived branch (`:233`) and the subject `[GFXA-XXX] Brief description` (`:431`), and calls Conventional Commits "encouraged ... non-blocking" (`:461`).
  - This repository configures the opposite: `.pre-commit-config.yaml:78-84` configures `conventional-pre-commit` at the `commit-msg` stage, which a `[GFXA-XXX]` header would fail, and the protected branches are `master` and `integration` (`docs/developer-guide/branch-protection.md`, "What is protected"; `.github/rulesets/protect-*.json`).
  - "Follow the standards" therefore cannot be executed literally. The design follows the enforced gates (pre-commit config, rulesets, routing guide) and says so.
- **RC-6. Four copies with no single parity rule make every edit expensive and drift-prone.**
  - `git.md` exists in four places: `<pkg>/commands/git.md`, `<plugin>/commands/git.md` (byte-identical today), the dev copy, and `commands/sc-git.md`, which carries the doubled title `/sc:sc:sc:git`. The legacy `commands/` directory is not packaged (`pyproject.toml:78-97`).
  - Only four commands are parity-tested (`<pkg>/commands/README.md:9`; `tests/commands/test_routing_plugin_parity.py:41-47`).
  - `make sync-dev` never touches `<plugin>` (`Makefile:109-163`), so `make verify-sync` is not proof of plugin parity. The parity of `/sc:git` holds by habit, and the legacy copy drifts with nothing to catch it.
- **RC-7. Existing tools do not solve this problem, so it has to be designed here.**
  - An existing marketplace commit plugin is a thin prompt with no handling of hooks, protected branches, submodules or parallel work, and its gone-branch cleanup force-deletes with `-D` (`research-deep.md` §3).
  - Session checkpoints are "not a replacement for version control" and miss shell edits (`research-deep.md` §1).
  - A tool that commits after every edit appears to skip hooks by default (`research-deep.md` §1, UNVERIFIED there).

### 1.7 Terms

<!-- Source: Base (original, modified) - glossary added for terms the base used before defining them, taken from repository vocabulary (SKILL.md, refs/ledger.md, refs/retry.md, WORKER-CONTRACT.md, launch-level-guard.sh), merged per Change #2; anchor-eligibility sentence in the Boundary row from review-3 note M3-4(c) -->

| Term | Meaning |
|---|---|
| Q0 START … Q8 NEXT | The per-task loop of the implement protocol: Q0 takes the start snapshot and writes the `start` line; Q1 EXEC implements; Q2 DIFF diffs against the start tree; Q3 REVIEW and Q4 VERDICT review and grade; Q5 FIX makes one fix pass; Q6 EXTRAS runs lint, typecheck and tests; Q7 GATE applies the Halt table and writes and flushes the verdict line; Q8 NEXT continues only after `complete` (`SKILL.md:121-150`) |
| Q8a, R0, L0 | The three commit-step positions this spec adds (FR-057) |
| Q0 pin, `q0-head` | The start tree pinned as `refs/<package>/implement/<slug>/T<id>`, and the 40-hex HEAD recorded at Q0 under `<retries>/T<id>/q0-head` (`refs/retry.md:28`) |
| Ruling | An operator acceptance given by the person in chat and recorded by the executor as `T<id>: Ruling: <what> — <why> — <cost-if-wrong>` (`refs/ledger.md:62-71`) |
| K3 | The item in the worker contract that parks per-task commits on this issue (`WORKER-CONTRACT.md:42`) |
| WC-4 | The worker-contract rule that an unattended command writes one `return-contract.yaml` with `worker_status` and, when failed, `reason` (`WORKER-CONTRACT.md:32`) |
| WC-9 | The rule that a worker makes no outward action and commits locally only by an explicit grant; "a command's own commit step stays off under `--unattended`" (`WORKER-CONTRACT.md:41-45`) |
| WC-11 | The rule on parallel-safe writes and when a worker needs its own child worktree (`WORKER-CONTRACT.md:47`) |
| P4 | The worker-contract rollout phase in which `/sc:implement` gains an `## Unattended mode` section; until then it has none |
| TAMPER | The launch-level guard's class for commands that touch the guard's store, hook settings or git config, and for `--no-verify` (`launch-level-guard.sh:777`, `:786`) |
| LL-COMMIT, LL-PROTECTED | The guard's refusals of a commit below level `full --submit` and of a push to `master`, `main` or `integration` |
| Boundary | The task, or the parallel batch (FR-058), that one commit covers; its anchor, key and eligibility are defined in FR-103. An anchor is eligible when it lies in an `on` segment. Due: FR-105. Pending, unsettled: FR-107. S (the commit set): FR-062, `commit_paths` plus, for a managed run, the FR-076 expansion; for `/sc:git commit`, FR-038 |

### 1.8 Seed constraints kept

<!-- Source: Base (original, modified) - checklist of the seed brief's constraints against the merged requirements, built from base §1.4, merged per Change #39 -->

| Constraint | Kept by |
|---|---|
| `/sc:git` never pushes, merges or opens a PR | FR-004, FR-005, D7, NFR-001 |
| No central relay | §1.4, FR-072, D2 |
| PRs stay with `/sc:pr-submit` | §1.4, FR-004 message |
| PR 711's local cleanup is reused and nothing deletes a remote branch | FR-080, FR-081, AC-11 |
| No `<dev>/` path other than `settings.json` is staged | FR-013, FR-031, FR-062, §1.5 |
| `.dev/tasks` is always staged and task evidence is committed (PR 288) | FR-061 step 5, FR-076, FR-038 |
| No installed primitive names a `src/<package>/` path | FR-009, FR-019, NFR-010 |
| No commit without authorization | FR-020, FR-050 |
| Destructive operations need confirmation | FR-022 (no `/sc:git` write is destructive), FR-080 (`/sc:worktrees` keeps `--apply`), FR-044 (URL repeat for a clone), FR-120..FR-126 (owner answer) |
| The commit step sits outside the task body and never inside a parallel batch | FR-056, FR-058, FR-077 |
| Behaviour changes have tests | §10 |

## 2. Structure of the refactored `/sc:git`

<!-- Source: Base (original, modified) - "package helper" becomes "helper script" per Change #6 -->

The design has three layers. The command file parses and stops. The protocol skill holds the behavior, with one ref loaded per operation. The helper script is read-only code that computes facts and plans: it decides, and the agent acts. Every write to the repository is a visible shell command run by the agent, never run inside the helper. That way the host's hooks (the launch-level guard, deny rules and pre-commit hooks) always see the real `git add` and `git commit`.

### 2.1 Command file `<pkg>/commands/git.md` (rewritten)

<!-- Source: Base (original, modified) - bare invocation runs status (Variant C, Section FR-007) per Change #9; submodule update usage form and the fetch-on-its-own Will Not wording per Change #30 -->

- **FR-001** The front matter has `name: git`, a one-line `description`, `category: version-control` and `complexity: moderate` (the values the developer guide lists in §3.1, `docs/developer-guide/<Product>-Developer-Guide-Commands-Skills-Agents.md:270-284`), `mcp-servers: []`, `personas: []`, and an `argument-hint` that lists exactly the operations in FR-002.
- **FR-002** The Usage block lists exactly these forms, and no others:
  - `/sc:git [status]`
  - `/sc:git add <path>...`
  - `/sc:git commit [<path>...] (--message "<text>" | --smart-commit)`
  - `/sc:git branch [list | create <name> | switch <name> | cleanup]`
  - `/sc:git submodule [status | update <path>... [--url <path>=<url>]... | commit-pointer <path> (--message "<text>" | --smart-commit)]`

  `--message` is new. `--smart-commit` is kept, because routing fixture S23 depends on it. `--interactive` and the `merge` example are removed.
- **FR-003** The body has these sections, in this order: `## Triggers`, `## Usage`, `## Options`, `## STOP rules (checked before Activation)`, `## Behavioral Flow` (parse, STOP, hand off, print), `## Activation` (contains exactly one line `> Skill sc:git-protocol` and names `<home>/skills/sc-git-protocol/SKILL.md`), `## Examples`, `## Outputs`, `## Boundaries` and `## Related Commands`. It has no `## Unattended mode` section.
- **FR-004** With no operation, `/sc:git` runs `status`. STOP rules print the usage block and run nothing in these cases: an unknown operation; `push`, `pull`, `fetch`, `merge`, `rebase`, `reset`, `clean`, `stash`, `tag` or `pr` as the operation (the message names `/sc:pr-submit` for push and PR, and says merge is not a `/sc:git` operation); `commit` or `commit-pointer` with neither `--message` nor `--smart-commit`, or with both; `create` or `switch` without a name; any token in the forbidden-flag list (FR-030); `--unattended` (the message says `/sc:git` never runs as a worker); and not inside a git work tree.
- **FR-005** Boundaries **Will Not** says, in plain words: push; fetch on its own (`submodule update` may clone or fetch from the `.gitmodules` URL only as FR-041 and FR-044 authorize); pull, merge, rebase, open or edit a PR, delete any branch (local or remote), force anything, stash, rewrite history (`--amend`, reset of a published commit), or stage a `<dev>/` path other than `settings.json`.

### 2.2 Protocol skill `<pkg>/skills/sc-git-protocol/` (new)

<!-- Source: Base (original, modified) - FR-007 branch list note on [gone] (Variant B, Section 7 FR-039) per Change #32; FR-008 checks helper verbs against vcs.py --help per Change #6 -->

- **FR-006** `SKILL.md` has the front matter `name: sc:git-protocol`, a `description`, and `allowed-tools: Read, Write, Bash`. It includes an **operation registry** table. Each row has: operation, class (`read`, `index`, `local-history`, `working-tree`), the authorizing message prefix (FR-020), the ref file, the helper verb, and the STOP and refusal tokens. The registry is the single place that lists what `/sc:git` can do.
- **FR-007** Refs are loaded on demand, one per operation group (developer guide §5.6, the refs pattern):
  - `refs/safety.md`: forbidden operations and flags, path rules, protected branches, hook-refusal handling and the message format. It applies to every write.
  - `refs/status.md`: the `status` and `branch list` reports. Upstreams shown as `[gone]` are printed as git prints them, with the note that `[gone]` is not proof of merge.
  - `refs/commit.md`: `add` and `commit`.
  - `refs/branch.md`: `create`, `switch` and `cleanup` (routing only).
  - `refs/submodule.md`: `submodule status`, `update` and `commit-pointer`.
- **FR-008 (extension scaffolding)** `SKILL.md` ends with an "Adding an operation" checklist: (1) a registry row; (2) a ref file or a section in an existing ref; (3) a helper verb, only if the operation needs computed facts; (4) a Usage and Options row in `git.md`; (5) tests per §10. A static test asserts that every registry row names an existing ref file and every helper verb the registry names appears in `vcs.py --help`.
- **FR-009** No file in the skill or the command names a `src/<package>/...` path. Cross-primitive references use `<home>/...` with the `<dev>/...` copy as the fallback (project rule "Never Hardcode ... Paths in Installed Primitives"; `tests/skills/test_primitive_dual_surface_lookup.py`).

<!-- Source: Variant B, Section 3.2 (FR-004) and Section 12 (NFR-011, NFR-002 size limits) - merged per Change #8 -->

- **FR-018** Each invocation loads at most two refs: the ref of its operation group, plus `refs/safety.md` for a write operation. A read operation (`status`, `branch list`, `submodule status`, `branch cleanup`) loads only its own group ref and never `refs/safety.md`. The registry row names the refs an operation loads, and T-13 checks it. `git.md` at most 150 lines; `SKILL.md` at most 500 lines; each ref at most 250 lines (NFR-012).

<!-- Source: Variant B, Section 5.1 (FR-023 helper resolution order) and Variant C, Section NFR-006 (no implicit install, no source-tree fallback) - merged per Change #6 -->

- **FR-019** The implement protocol and the git protocol resolve the helper at `<home>/skills/sc-git-protocol/scripts/vcs.py`, then at `<dev>/skills/sc-git-protocol/scripts/vcs.py`. If neither exists, or `vcs_contract` is not `"1"`, every requested write stops with `helper-missing` and reads still run. In `/sc:implement`, when `commits.md` exists and the helper is missing or `vcs_contract` is not `"1"`, Wave 0 stops `E-COMMIT-REFUSED reason=helper-missing` before task selection, with or without the flag (a flagged run has already stopped `E-COMMIT-PRECONDITION reason=helper-missing` at its preflight, FR-054). There is no implicit installation and no fallback to a `src/<package>/` path.

### 2.3 Read-only helper `vcs` (new skill script)

<!-- Source: Base (original, modified) - module split, single constants file and contract version kept; location moved to a mirrored skill script run with uv (Variant B, Section 3.1 and FR-019) and versioned results added (Variant C, FR-021 and NFR-006); merged per Change #6; dirty field dropped and symbolic_ref added to preflight per Change #17 -->

Files: `<pkg>/skills/sc-git-protocol/scripts/vcs.py` (entry point and verbs), `vcs_rules.py` (safety constants), `vcs_plan.py` (planning, verification, reconcile and resolution checks) and `vcs_submodules.py` (submodule facts). Standard library only, Python 3.10 or later. Both protocols run it as `uv run --no-project python "<skill-dir>/scripts/vcs.py" <verb> ...` (precedent: `refs/managed-workspace.md:54`). It is mirrored byte for byte to `<plugin>/skills/sc-git-protocol/scripts/` (FR-015). The launch-level guard's word classifier does not match the path `.../sc-git-protocol/scripts/vcs.py`.

- **FR-010** The verbs, all read-only (seven in all). Every verb prints one JSON object with `vcs_contract: "1"`, `status`, `reason`, and the HEAD before and after where relevant:
  - `vcs preflight [--cwd <dir>]` prints `top`, `branch`, `symbolic_ref` (the full `git symbolic-ref -q HEAD`), `detached`, `protected` (boolean plus a reason), `operation_in_progress` (merge, rebase, cherry-pick, revert or bisect marker), `index_lock`, `hooks_path`, `submodule_recurse` and `push_recurse_submodules`.
  - `vcs stage-plan (--path <p>... | --ledger <file> --run-dir <dir> [--package <dir>]) [--candidate] [--cwd <dir>]` prints `status` (`ok`, `nothing` or `refused`), `reason`, `tasks` (ledger mode), `add_argv`, `commit_argv`, `commit_paths`, `skipped` (`[{path, why}]`) and `message_path`. The `--candidate` mode, run after the prepared line, builds the frozen candidate tree and prints it (FR-061 step 4, FR-108).
  - `vcs check-message --file <f> [--implement]` reports `ok`, or `refused` with the violated rule in `reason`.
  - `vcs verify`, `vcs reconcile` and `vcs resolve-check` are specified in §7 (FR-130, FR-106, FR-123).
  - `vcs submodules [--cwd <dir>]` prints the rows of FR-040.

<!-- Source: Base (original, modified) - allow-list extended with private-index verbs (Variant B, Section 4.1 FR-019) and the object-write and visible-write disclosure; submodule-read rule from Variant B (Round 2, E6); merged per Change #7 -->

- **FR-011** The helper calls git only through one runner. That runner adds the prefix `git --no-optional-locks -c core.fsmonitor=false` (the same seam as `probes.py:65`) and allows only these verbs: `rev-parse`, `symbolic-ref` (including `-q HEAD`), `status`, `diff` (including `--name-status`, `--name-only -z`, `--quiet`), `ls-files` (including `-v`, `-z`, `--cached --others --exclude-standard`), `ls-tree`, `cat-file` (including `-e`), `check-ignore`, `config --get`, `submodule status`, `for-each-ref`, `rev-list`, `log`, `merge-base --is-ancestor`, `branch --show-current`, `branch -r --contains`, `hash-object` without `-w`, and `read-tree`, `add`, `write-tree` only when `GIT_INDEX_FILE` names a private temporary index. Any other argv raises an error before it executes. Implement-side reads use `--ignore-submodules=all`; only the person-invoked `/sc:git status` and `submodule status` use `--ignore-submodules=none`.

  Private-index calls write loose objects into the object store, as the Q0 snapshot does (`SKILL.md:124`). The helper writes no ref, no user index, no working-tree file and no config. Every ref pin, `git add` and `git commit` is a literal Bash call the agent runs, so the host's hooks see it. The launch-level guard does not gate the helper's own reads; this spec does not claim it does.

<!-- Source: Base (original) -->

- **FR-012** Exit codes: 0 when JSON was printed, whatever the `status`; 64 for a usage error; 69 when a lookup failed. These match the codes `/sc:worktrees` uses (`<pkg>/commands/worktrees.md:55`).

<!-- Source: Base (original, modified) - constants file renamed per Change #6; protected-branch floor that a resolved default only adds to, debate Round 2 C-017 resolutions plus Variant B, Section 6 FR-037 (submodule reads its own refs), per Change #11; MIN_GIT bullet matched to NFR-011 per Change #34 -->

- **FR-013** Safety constants are defined once, in `vcs_rules.py`:
  - `PROTECTED_BRANCHES = ("master", "main", "integration")`, the `LL-PROTECTED` set (`launch-level-guard.sh:58-60`). At run time the set also gains the target of `refs/remotes/origin/HEAD` when it resolves, and any further name the current repository's own instructions name as protected (the report names that source). A resolved default only adds a name; it never removes a fixed one. Inside a submodule, the default is read from the submodule's own refs.
  - `FORBIDDEN_FLAGS` (FR-030);
  - `DEV_MIRROR_ALLOW = ("settings.json",)`;
  - `MIN_GIT`: the higher of 2.23 (`git switch`) and the version that supports `--pathspec-from-file` for `git add` and `git commit` (NFR-011).

  The refs in §2.2 repeat these lists for the agent, and a parity test asserts the prose and the constants match.

### 2.4 Fate of `commands/sc-git.md`

<!-- Source: Base (original) -->

- **FR-014** Delete `commands/sc-git.md`, and add it to the absence test (the `_RETIRED` list in `tests/docs/test_retired_docs_absent.py:10-34` is the precedent). Leave the other `commands/sc-*.md` files alone (scope). See decision D5.

### 2.5 Plugin mirror and sync steps

<!-- Source: Base (original, modified) - FR-016 separates tracking from staging authority per Change #4; FR-017 keeps /sc:pr-submit out of the route steps (Variant B, Section 3.2 FR-009) per Change #28 -->

- **FR-015** Edit `<pkg>` first. Then copy byte-for-byte:
  - `<pkg>/commands/git.md` to `<plugin>/commands/git.md`;
  - `<pkg>/skills/sc-git-protocol/**` to `<plugin>/skills/sc-git-protocol/**`;
  - `<pkg>/commands/implement.md` to `<plugin>/commands/implement.md`;
  - `<pkg>/skills/sc-implement-protocol/**` to `<plugin>/skills/sc-implement-protocol/**`;
  - `<pkg>/core/HOW-WE-WORK.md` to `<plugin>/skills/sc-recommend/refs/HOW-WE-WORK.md`.

  Add `git.md` to the mirrored list in `<pkg>/commands/README.md:9`, and add `"git"` to the parametrization in `tests/commands/test_routing_plugin_parity.py:41`.
- **FR-016** Run `make sync-dev`, then `make verify-sync`. The verify step must exit 0. `<dev>/` copies are never staged. `<dev>/` holds tracked files other than `settings.json` (§1.5), but tracking is not authority to stage: the only `<dev>/` path this work may stage is `settings.json`, and this work does not change it.
- **FR-017** Update the `/sc:git` row in the Other commands table of `<pkg>/core/HOW-WE-WORK.md:293`. The new row must keep the three phrases that fixture S23 pins: "Status-only stays inspection", "a commit needs authorization" and "Do not append push, merge or PR creation". It removes "merge operations", names `/sc:worktrees` for cleanup, and names only flags that exist in `git.md`, because `tests/core/test_how_we_work_routing_table.py` checks the names the table uses. The row's route steps do not name `/sc:pr-submit`, which is fixture S23's competitor (`tests/recommend/test_routing_refresh.py:224-243`).

## 3. Authorization model

<!-- Source: Base (original, modified) - Extra guard of the between-task row points at §6 per Change #5 -->

The person's own typed line is the only thing that authorizes a write. No plan field, brief line, other command or agent message can authorize one (`WORKER-CONTRACT.md:57`, "executor-invented approval").

| Operation | Class | Authorized by | Extra guard |
|---|---|---|---|
| `status`, `branch list`, `branch cleanup`, `submodule status` | read | Any `/sc:git` invocation | None |
| `add <path>...` | index | The person's current message starts with `/sc:git add` | Path rules (FR-031) |
| `commit` | local-history | The person's current message starts with `/sc:git commit` | Preflight (FR-032) |
| `branch create`, `branch switch` | working-tree | The person's current message starts with `/sc:git branch` | Clean tree, submodules included (FR-034) |
| `submodule update <path>` | working-tree | The person's current message starts with `/sc:git submodule update` | Submodule state rules (FR-041) |
| `submodule commit-pointer <path>` | local-history | The person's current message starts with `/sc:git submodule commit-pointer` | Submodule state rules plus preflight |
| Between-task commit in `/sc:implement` | local-history | `--commit-tasks` on the `/sc:implement` invocation line | §6 |
| Push, fetch, pull, merge, rebase, reset, clean, stash, tag, any branch deletion, any force | forbidden | Nothing | STOP (FR-004) |

<!-- Source: Base (original, modified) - FR-020 refuses instead of printing a replayable dry run (Variant B, Section 4 FR-012) per Change #10 -->

- **FR-020** A write operation runs only when the person's current message starts with the authorizing prefix in the table. This follows the precedent at `WORKER-CONTRACT.md:346`. When `/sc:git` is reached any other way (an agent decides to run it, another skill suggests it, or the line comes from a plan or brief), every write operation refuses with `authorization: write operations need a person-typed /sc:git <operation>`. The refusal names the operation and prints no command lines. Read operations still run.

<!-- Source: Base (original) -->

- **FR-021** One authorizing line authorizes one operation. A follow-up write needs a new typed line.

<!-- Source: Base (original, modified) - write report from Variant B, Section 4 FR-018 and Variant C, Section NFR-001 and NFR-004, merged per Change #12 -->

- **FR-022** No write operation asks for a second confirmation, because none of them is destructive: nothing deletes, overwrites unsaved work, or rewrites history. After every write attempt, `/sc:git` prints the preconditions it checked, the exact argv of every git command it ran, the result (new commit SHA, refusal token or conflict list), HEAD before and after, and whether the index and the working tree changed. A refusal names the violated precondition. After a commit it prints, as advice it never runs, `git reset --soft <parent>` (keeps the changes staged; only for an unpushed commit) or `git revert <sha>`. Printed advice authorizes nothing. Diagnostics never print file contents, credentials or credential-bearing remote URLs.

<!-- Source: Variant C, Section FR-010 (grant scope: named repository and write set) - merged per Change #10 -->

- **FR-023** An authorizing line covers only the repository it runs in and the paths, branch name or submodule target it names. It never covers another repository, a later turn, or paths it did not name.

## 4. Commit rules shared by `/sc:git` and the implement step

<!-- Source: Base (original, modified) - section moved ahead of the sections that use it (was §6) per Change #5 -->

- **FR-030** The forbidden-flag list: `--no-verify`, `-n` (on commit), `--amend`, `--force`, `-f`, `-D`, `--delete`, `-A`, `--all`, `.` (as a pathspec), `-a`, `--allow-empty`, `--no-edit`, `--remote`, `--recurse-submodules=on-demand`, `--discard-changes`.

<!-- Source: Base (original, modified) - dev-copy-path refusal for tracked <dev>/ files (debate Round 2 evidence) per Change #4; FR-062 rules (c)-(e) extended to /sc:git per Change #13 -->

- **FR-031** Path rules for `add` and `commit <path>...` are the same as FR-062, without the ledger parts. A `<dev>/` path other than `settings.json` is refused. A gitlink is refused with a pointer to `submodule commit-pointer`. A tracked `<dev>/` path other than `settings.json` is refused with `dev-copy-path`; the refusal names the file and stops, and suggests no staging command. Tracking a file is not authority to stage it. Rules (c) to (e) of FR-062 also apply to `/sc:git add` and `/sc:git commit <path>...`.

<!-- Source: Base (original, modified) - default-branch notice and detached-HEAD scope added (debate Round 2 C-017 resolutions) per Change #11 -->

- **FR-032** Preflight for every local-history write: refuse on `detached-head`, `protected-branch` (FR-013), `operation-in-progress`, `index-locked`, or a git version below `MIN_GIT`. When `refs/remotes/origin/HEAD` is not set, print `default branch unknown: refs/remotes/origin/HEAD is not set; protected names: master, main, integration` and the local fix `git remote set-head origin <branch>`, then continue. No network lookup, no block. A detached HEAD in the repository that receives the commit is refused, including inside a submodule's work tree (FR-043). Only `commit-pointer` reads the submodule's detached HEAD, under FR-042.

<!-- Source: Base (original, modified) - pathless commit follows FR-038 per Change #20; stale hook-refusal sentence replaced per review-3 note M3-8 -->

- **FR-033** `/sc:git commit` with paths commits the working-tree content of exactly those paths (`--only`), so the person's other staged changes stay staged. Without paths, it follows FR-038. It refuses when the index holds a `<dev>/` path other than `settings.json`. Hook refusal follows FR-036 and FR-064's no-retry rules, printing the report instead of a sidecar line, with any rewritten pin under `refs/<package>/git/`. The message comes from `--message`, or from `--smart-commit`, which drafts it from `git diff --cached` in Conventional Commits form. In both cases it is checked by `check-message` (without `--implement`) and passed with `-F`.

<!-- Source: Base (original) -->

- **FR-034** `branch create <name>` runs `git switch -c <name>`, and refuses a name in `PROTECTED_BRANCHES` or a name that already exists. `branch switch <name>` runs `git switch <name>`, and refuses when `git status --porcelain=v2 --ignore-submodules=none` is not empty. Neither ever uses `--force` or `--discard-changes`. If git refuses because the branch is checked out in another worktree, the refusal is shown as is.

<!-- Source: Variant C, Section FR-018 and NFR-005 (literal path handling), with the debate Round 3 ruling INV-012 (pathspec transport) - merged per Change #13 -->

- **FR-035** Every `git add` and `git commit` in this spec passes its paths through a temporary NUL-delimited file outside the work tree: `git --literal-pathspecs add --pathspec-from-file=<file> --pathspec-file-nul` and `git --literal-pathspecs commit --only -F <message file> --pathspec-from-file=<file> --pathspec-file-nul`. The agent prints the complete path list before the call. The guard still classes the call as a commit (it skips global options before the subcommand), and a host denial stays authoritative; the file transport is not permission to hide a forbidden target. The one exception is a pathless `/sc:git commit` (FR-038, FR-117): it runs `git commit -F <message file>` with no `--only` and no pathspec file, so that exactly the index the person staged is committed and no unstaged edit in a partly staged file is pulled in.

<!-- Source: Variant B, Section 4.1 FR-021 (hook-failed, hook-rewrite, hook-rewrite-committed, guard) and its Round 2 hook-rewrite-pinned class, with the debate Round 3 rulings INV-020 and INV-029 - merged per Change #15 -->

- **FR-036** Shared hook-outcome classes, used by FR-033 and FR-064:
  - `blocked-by-host`: a host hook refused the Bash call before git ran; HEAD and index unchanged;
  - `hook-failed`: exit 1, HEAD unchanged, S unchanged; also a file over the size limit, named;
  - `hook-rewrite`: HEAD unchanged, product paths in S changed;
  - `hook-rewrite-evidence`: HEAD unchanged, only package evidence changed, not plan, source or product paths;
  - `hook-rewrite-committed`: HEAD moved but the committed tree differs from the pinned frozen candidate (FR-108);
  - `hook-rewrite-pinned`: the managed plan or source bytes no longer match the `PLAN:` pin;
  - `commit-error`: exit 128.

  A timeout or an exit above 128 is not classified here; it follows FR-116.

<!-- Source: Variant B (its version of the debate Round 3 ruling INV-024, staging order of /sc:git commit) - merged per Change #20 -->

- **FR-038** `/sc:git commit` never widens the person's commit. With paths named, it stages those paths plus `.dev/tasks` and commits `--only` the named paths. With no paths, it freezes the index change set as S before the call, commits the index as the person staged it, and runs `git add -- .dev/tasks` after the commit (also after a refusal). It warns when the staged set holds a `commits.md` with an unsettled boundary.

<!-- Source: Variant B, Section 4 FR-016 step 1 (message file outside the work tree) - merged per Change #14 -->

- **FR-039** `/sc:git commit --message` and `--smart-commit` write the message to a temporary file outside the work tree and pass it with `-F`.

**Standards conflict (recorded, not fixed here).** `docs/developer-guide/git-standards-protocols.md:430-439` asks for a `[GFXA-XXX] ...` subject. That file is a template from another project: its front matter id is `GFXAI-GIT-STANDARDS-PROTOCOLS` and its status is "To Do" (lines 1-9). This repository enforces Conventional Commits with `conventional-pre-commit` (`.pre-commit-config.yaml:78-84`). This spec follows the enforced hook.

## 5. Submodule operations in `/sc:git`

<!-- Source: Base (original) - section number unchanged; now placed after §4 per Change #5; requirement-level changes are tagged below -->

<!-- Source: Base (original, modified) - closed state list kept as one derived state with fixed precedence over independent nullable facts (Variant C, Section FR-024 and FR-025; Variant B, Section 6 FR-033 branch containment; debate Round 2 fixed precedence), merged per Change #29 -->

- **FR-040** `submodule status` reports one row per top-level registered submodule, built from `git submodule status` and `git status --porcelain=v2 --ignore-submodules=none` (the `S<c><m><u>` field), read through the FR-011 seam on the person's typed line only. Fields: `path`; `gitlink` (recorded SHA); `head` (checked-out SHA or null); `initialized`; `branch` (name or null when detached); `conflicted`; `commit_changed` (c), `tracked_dirty` (m), `untracked_dirty` (u); `target_local` (whether the gitlink object exists in the submodule, `git -C <path> cat-file -e <gitlink>^{commit}`); `contained` (whether HEAD is in a local or remote-tracking branch; null when unknown); `nested` (true when the submodule has its own `.gitmodules`; such entries are reported `nested-not-inspected`); `reason` when a value is unknown. A missing value is null, never a fabricated clean state. One derived `state` per row, first match wins: `conflict`, `dirty-tracked`, `dirty-untracked`, `detached-new-commits` (detached, HEAD ≠ gitlink, not contained), `uninitialized`, `target-not-local`, `submodule-ahead` (gitlink is an ancestor of HEAD), `submodule-diverged`, `pointer-moved`, `in-sync`. The report also prints the superproject branch and HEAD and the values of `submodule.recurse` and `push.recurseSubmodules`, telling unset apart from false; when `submodule.recurse` is true it warns that a later plain push may push submodules too. Rows are sorted by path; no submodules gives an empty list, not an error.

<!-- Source: Base (original, modified) - ancestor-only update and the submodule-ahead and submodule-diverged refusals (Variant B, Section 6 FR-034); missing target objects (debate Round 3 ruling INV-009); disclosed network effect and post-update revalidation (Variant C, Section FR-026); merged per Change #30 -->

- **FR-041** `submodule update <path>...` runs `git submodule update --init -- <path>` (never recursive) for a path only when its state is: `uninitialized` (and FR-044 holds); `pointer-moved` with the module clean and its HEAD an ancestor of the recorded gitlink; or `target-not-local` with the module clean and its HEAD contained in a local or remote-tracking branch, so no commit is orphaned (the fetch is disclosed first). It refuses `submodule-dirty`, `conflict`, `detached-new-commits` (stop and ask; print `git -C <path> switch -c <name>` as the way to keep the commits), `submodule-ahead` (use `commit-pointer`), `submodule-diverged` and `in-sync` (nothing to do). An `--is-ancestor` exit of 128 is never read as "diverged". After the update it re-reads the module HEAD; if it is not the recorded gitlink the result is `uncertain` and is reported. It never passes `--remote`, `--force`, `--checkout`, `--merge`, `--rebase` or `--recursive`.

<!-- Source: Base (original, modified) - clean module, submodule-unpublished refusal, one-path commit and message form (Variant B, Section 6 FR-035); exact selected target and post-commit check (Variant C, Section FR-027 and FR-028); last-fetch wording (debate Round 2); containment only through the .gitmodules remote (debate Round 3 ruling INV-030); merged per Change #31 -->

- **FR-042** `submodule commit-pointer <path>` runs only when all hold: (1) the superproject passes FR-032; (2) the top-level registered submodule is initialized, conflict-free and clean, else `submodule-dirty` ("commit inside the submodule first; run `/sc:git commit` from inside it"); (3) the module HEAD differs from the recorded gitlink, else `in-sync`, and the plan records that full target SHA; (4) the target is contained in a remote-tracking ref of the submodule remote whose `remote.<r>.url` equals the `.gitmodules` URL. If no such remote exists it refuses `submodule-unpublished reason=no-gitmodules-remote`; if the target is in no branch at all it refuses `detached-new-commits` with the `git -C <path> switch -c <name>` hint; otherwise, if it is not contained, `submodule-unpublished`. A detached HEAD at a contained target is eligible. The refusal says: "`<short-sha>` is not on a remote-tracking branch of `<path>`'s `.gitmodules` remote (local refs; last fetch: `<FETCH_HEAD file time, or never>`). Push it first, or run `git -C <path> fetch` yourself if it is already pushed. `/sc:git` never pushes and never fetches on its own; only `submodule update` may clone or fetch, from the `.gitmodules` URL, as FR-041 and FR-044 authorize." A success prints "on `<remote-ref>` as of last fetch `<time>`", labelled a local observation, not proof that others can fetch it. (5) The commit set is exactly `{<path>}`; `.gitmodules` and config are unchanged; the message is `chore(submodule): bump <path> to <short-sha>` with a body from `git diff --submodule=log -- <path>`; the argv is the FR-035 form and FR-117 applies. (6) The target SHA is re-checked just before the commit, and afterwards `git ls-tree HEAD -- <path>` must name it, else `uncertain`. No override flag. Residuals: stale refs can refuse a target that is in fact published; a later remote rewrite can make a contained target unavailable.

<!-- Source: Base (original) -->
- **FR-043** A commit inside a submodule is an ordinary `/sc:git commit` run from inside the submodule's work tree. The detached-HEAD refusal in FR-032 forces a branch first, which is the safe order the research describes.

<!-- Source: Variant C, Section FR-026 and FR-028 (network effect acknowledged, substituted remotes refused, per-module partial results, unique contribution U-021) with the debate Round 3 ruling INV-010; Variant B, Section 6 FR-037b (the guard denies every git submodule command, unique contribution U-009) - merged per Change #30 -->

- **FR-044 (network effect and approved URL)** For an uninitialized module, `update` prints the `.gitmodules` URL (with any credentials removed) and runs only when the person's typed line repeats that displayed, credential-free form as `--url <path>=<url>`, byte for byte; the comparison is always made against the displayed form, and it is revalidated just before the call. An initialized module whose `submodule.<name>.url` differs from `.gitmodules` refuses `remote-mismatch` and prints `git submodule sync -- <path>` for the person to run. Remotes are never substituted.
- **FR-045 (several paths)** Every named path is preflighted before any write. If a later path fails, the report lists completed, untouched and failed paths with old and new SHAs; earlier successes are not rolled back. Running the same line again reports satisfied paths as `in-sync`.
- **FR-046 (launched sessions)** The launch-level guard denies every `git submodule` command at every level, because `submodule` is not in its allow-table and falls to `UNKNOWN` (`launch-level-guard.sh:720`, `:724`, `:816`). The skill reports that refusal as `blocked-by-host` and never works around it; the guard is not changed.

## 6. Between-task commit behavior in `/sc:implement`

<!-- Source: Base (original) - renumbered from §4 per Change #5; requirement-level changes are tagged below -->

### 6.1 Opt-in switch

<!-- Source: Base (original, modified) - FR-050 gains the run-scoped grant and its accepted residual, FR-051 the off run line (debate Round 3 text for INV-001 with the Round 2 A-003 resolutions and the ruling INV-011), per Change #23; the after-revocation sentence from review-3 note M3-5 -->

- **FR-050** Add a new flag, `--commit-tasks`, to `/sc:implement`: to the Options table, the argument-hint (`implement.md:7`) and the Wave 0 option list (`SKILL.md:57`). It is off by default. It counts only as a standalone token in the option prefix, following the same rule as the other options at `SKILL.md:57-59`. After the source starts, the same text is part of the prompt.

  `--commit-tasks` counts only as a standalone token in the option prefix of a message the person typed that starts with `/sc:implement`. It is checked once, in the Wave 0 commit preflight (FR-054). Reached through another command, the Skill tool or an agent's own invocation, the run stops `E-COMMIT-PRECONDITION reason=not-person` before any commit-feature write. The grant covers the later turns of the same active run, including the in-chat Ruling that continues to the next task (`refs/qa.md:248`) and context compaction (the executor re-reads the ledger and `commits.md` from disk, `SKILL.md:118`). It ends when the run stops; a resume is a new run (`SKILL.md:76`) and needs the flag again. If the person says during the run to stop committing, the executor appends a revocation `run` line before the next attempt; plain words can narrow the grant, never widen it. After a revocation line, the run counts as "any other run" for FR-056 and FR-107; a boundary that is already due stops `unsettled` with the choices. A Ruling neither grants nor revokes it (`refs/ledger.md:239`). A stored `on` is evidence of what was typed, not proof of who typed it. Stated residual: an agent that resumes without running Wave 0 would read a stale `on`; the protocol forbids it and the `args=` record makes it auditable, but nothing prevents it mechanically.

  Accepted residual: Wave 0 has no unknown-option STOP (`SKILL.md:57-59`), so an already installed older protocol copy ignores the flag and commits nothing, which fails safe; it cannot be repaired by this spec. New copies print `commit-tasks=on run=<n>` as the first Wave 0 line and the commit count in the final summary, and FR-105 stops an old copy's later tasks from being committed after the fact.
- **FR-051** The flag is per invocation. A run without it makes no commit; if `commits.md` exists it appends an `off` run line (FR-101) and reconciles (FR-106).

<!-- Source: Base (original, modified) - runtime person check first (Variant B, Section 5.1 FR-022, now in FR-050) and the static file list widened to remove the base's own contradiction with FR-091, per Change #24 -->

- **FR-052** The runtime check in FR-050 is the guard. As a second, static check, no primitive except these files contains the string `--commit-tasks`: `<pkg>/commands/implement.md`, `<pkg>/skills/sc-implement-protocol/**`, `<pkg>/core/HOW-WE-WORK.md`, `<pkg>/core/WORKER-CONTRACT.md`, and their byte copies `<plugin>/commands/implement.md`, `<plugin>/skills/sc-implement-protocol/**` and `<plugin>/skills/sc-recommend/refs/HOW-WE-WORK.md`. In particular no `/sc:workflow` handoff, `/sc:issue` launch prompt, `/sc:task` text or `sc-git-protocol` file contains it. Primitives are the files under `<pkg>/{commands,skills,agents,core,hooks,templates}` and their `<plugin>` mirrors; tests and `.dev/` are not primitives.

<!-- Source: Base (original) -->
- **FR-053** Replace the Will Not at `implement.md:100` with "Commit without `--commit-tasks` on the invocation line, push, open PRs, or release (a managed archive is not any of these)".

### 6.2 Wave 0 preflight

<!-- Source: Base (original, modified) - placement after step 5 kept; not-person and helper-missing reasons from Variant B, Section 5.1 FR-022 and FR-023; inline-intake note from Variant C (Round 2); dirty reason removed; branch capture from the debate Round 3 ruling INV-002; merged per Change #17 -->

- **FR-054** When `--commit-tasks` is present, a new Wave 0 step runs after step 5 (resolve the ledger path) and before step 6 (open or create the ledger). It runs `vcs preflight` and reads any existing ledger and `commits.md` without writing. It STOPs with `E-COMMIT-PRECONDITION reason=<token>` before ledger creation, product edits or any commit-feature write on: `not-person` (FR-050); `unattended`; `helper-missing` (FR-019); `not-a-repo`; `detached-head`; `protected-branch`; `operation-in-progress`; `index-locked`; `git-too-old`. The existing inline-prompt intake (Wave 0 step 3) may already have written `<run-dir>/source.md`; this step does not change that.

  In a run with the flag, at every new Q0 the executor records the full symbolic branch beside `q0-head` (`<retries>/T<id>/q0-branch`). A run without the flag records nothing (NFR-018, AC-08), so a task started in an unflagged run has no record and its boundary refuses `branch-unproven`, which fails safe. The run line (FR-101) and the prepared line (FR-108) repeat it. Prepare refuses `branch-changed` when the current symbolic ref differs from the branch recorded at the first member's Q0, and `branch-unproven` when that record is missing; a branch read in a later run is never used as the original.

<!-- Source: Base (original, modified) - base FR-055 (the COMMIT: on ledger marker) deleted; run segments of FR-101 replace it, per Change #23 -->

### 6.3 When the commit step runs

<!-- Source: Base (original, modified) - FR-057 position detail from Variant C, Section FR-013 and FR-022, per Change #16; FR-056 and FR-058 replaced with the debate Round 3 text for INV-001 and the ruling INV-014, per Change #23 -->

- **FR-056** Define these terms over the ledger:
  - A task is **open** when its latest `start` line has no later `complete` verdict line for that task.
  - A boundary is **eligible**, **due**, **pending** or **settled** as FR-103, FR-105 and FR-107 define.
  - The commit step runs at Q8a, R0 and L0 only when the flag is present, no task is open, and a boundary is due (FR-107 decides whether it is prepared or stops) or FR-107 allows a new attempt on a pending or refused one.
- **FR-057** Positions in the loop:
  - **Q8a**, after Q7 has flushed a `complete` line and before Q8 starts the next task's Q0;
  - **R0**, at the start of a resume, before task selection (`refs/ledger.md:124-135`);
  - **L0**, after the last task's `complete` line and before the whole-list review or the managed FINAL.

  At every position the "no task is open" condition is rechecked from the ledger on disk.

  Q8a runs after Q7 has flushed the `complete` line and every task writer has finished and been joined, and before Q8 writes the next `start` line or takes the next Q0. R0 is the reconcile of FR-106, in its Wave 0 order. L0 runs after the last task's `complete` and before the whole-list review, the legacy all-complete stop or the managed FINAL.
- **FR-058** Parallel batches. Every member's `start` line is written before any member runs (`SKILL.md:110`, rule (a)), so "no task is open" holds only after every member is `complete`. Batch membership is the original overlapping start-to-first-verdict window set (`refs/retry.md:40`) and never changes on resume. The batch makes one commit listing every member, and only when every member's anchor is eligible. If a member halts, no commit is made until a resume completes it. An all-complete batch whose members are not all eligible (some completed in a flagged run, some not) is settled with `T<ids>: commit skipped key=<key> reason=mixed-authorization` and no partial commit; the summary lists the batch's files.
- **FR-059** The commit step never runs while any task has a `halt` or `blocked` record that is its latest record. So HEAD equals `q0-head` for every open or halted task: the retry check 3 (`refs/retry.md:41`) and the Ruling resume condition (6) (`WORKER-CONTRACT.md:280`) still hold.

<!-- Source: Debate Round 3 (settle before advance, ruling INV-022) with Variant C, Section FR-013 and FR-022 (writers joined; reconcile before task selection and the all-complete return) - merged per Change #16 -->

- **FR-077 (settle before advance)** While any boundary is unsettled (FR-107), no run writes a `start` line, takes a Q0, runs the legacy all-complete FINAL or stop (`refs/ledger.md:134`, `:139`), or enters the managed archive gate (`refs/managed-workspace.md:48`). A late preparation or a retry happens only in reconcile and only while no task is open, so HEAD never moves under an open task.
- **FR-079** The whole-list review and the managed FINAL keep judging the current contents of every delivery file (`refs/qa.md:311`), not `git diff HEAD`. T-24 pins this for legacy and managed runs.

### 6.4 How the commit is made

<!-- Source: Base (original, modified) - aliases per Change #1, helper call per Change #6, sidecar record forms per Change #22; FR-061 replaced by the ordered procedure of the debate Round 2 C-010 resolutions (Variant B, Section 5.5 FR-029; Variant C, Section FR-022) and the message step of Change #14, per Change #25; writer of the commit-paths file named per review-3 note M3-8 -->

- **FR-060** The step runs `uv run --no-project python "<skill-dir>/scripts/vcs.py" stage-plan --ledger <ledger> --run-dir <run-dir> [--package <pkg-dir>]` (the helper resolved by FR-019). It acts only on `status` and the printed argv:
  - `nothing`: append `T<ids>: commit skipped key=<key> reason=empty` (FR-100) and continue;
  - `refused`: record the refusal in the FR-064 form and STOP `E-COMMIT-REFUSED`;
  - `ok`: continue with FR-061 step (2).
- **FR-061** The commit step is this ordered procedure; each step is one visible call unless it says helper. Step (1) is the `stage-plan` call of FR-060, and steps (2)-(9) run only on `ok`:
  1. `vcs stage-plan` computes S (FR-062, FR-076) and checks FR-073..FR-075 and the branch (helper).
  2. Write the message with the Write tool to a temporary file outside the work tree (`message_path` from `stage-plan`; refusal logs stay in `<run-dir>/` or `<pkg-dir>/artifacts/`) and run `vcs check-message --implement` (one rewrite allowed; a second refusal is `reason=message`).
  3. The agent writes `commit-paths-<key>-a<n>.txt` beside the sidecar (FR-100), then appends the prepared line (FR-108).
  4. `vcs stage-plan --candidate` builds the frozen candidate (the parent plus S, including the managed sidecar's prepared bytes, FR-108) and prints its tree (helper); the agent pins `boundary/<key>-a<n>`.
  5. The agent runs the FR-035 `git add` for S, and `git add -- .dev/tasks` when it exists and is not ignored.
  6. The agent takes and pins the worktree snapshot (FR-111).
  7. The agent runs the FR-035 `git commit --only` with the timeout of FR-116.
  8. `vcs verify` (FR-130) (helper).
  9. Append the terminal line.

  The executor never edits the argv the helper printed.

<!-- Source: Base (original, modified) - <pkg-dir> alias per Change #1; literal-path rules (a)-(e) from Variant C, Section FR-015 and FR-018 with the debate Round 3 rulings INV-007 and INV-008, per Change #13; commit_paths built from anchor complete lines, the single definition of S and the literal package expansion, per Change #20 -->

- **FR-062** Path rules inside `stage-plan`:
  - `commit_paths` is the sorted union of the `files=` fields on the anchor `complete` lines (FR-103: the first valid `complete` after each member's `start`) of the members of the boundary being prepared. A later re-review `complete` repeats the same verdict fields (`refs/ledger.md:84-86`) and never changes the set.
  - **S** (the commit set of a boundary) is `commit_paths` plus, for a managed run, the FR-076 expansion. For `/sc:git commit`, S is the named paths, or the index change set frozen before the call (FR-038, FR-117).
  - For a managed run, S also contains the FR-076 expansion of `<pkg-dir>` (literal files, never the directory). It does not include all of `.dev/tasks`, so other packages stay out of the commit; they stay staged by FR-061 step (5).
  - Excluded, each listed in `skipped` with its reason: paths under `.dev/implement/` (`refs/ledger.md:3`); gitignored paths; paths outside the repository; gitlinks (mode `160000`, matching the revert exclusion at `refs/retry.md:212`); and `<dev>/` paths other than `settings.json`.
  - If nothing remains, the result is `nothing`.
  - (a) A `files=` path missing from the worktree but present in the index or HEAD is a deletion and is staged; only a path missing from all three is `skipped why=absent`.
  - (b) With `--commit-tasks` on, the Q1 touched set names deleted paths and both ends of a rename.
  - (c) Any path equal to or under a mode-160000 entry of HEAD, the index or the retained Q0 tree (prefix match on `<path>/`) is `skipped why=gitlink` before the add.
  - (d) A path the ledger cannot carry faithfully (comma, newline or control character; `refs/ledger.md` `files=` grammar) refuses `path-unrepresentable` before staging.
  - (e) Absolute paths, `..` traversal and paths that resolve through a symlink outside the repository refuse `outside-repo`.

<!-- Source: Base (original, modified) - argv shape is the FR-035 form per Change #13 -->

- **FR-063** `add_argv` and `commit_argv` have the FR-035 shape. They never contain `-A`, `--all`, `.`, `-a`, `--amend`, `--no-verify`, `-n`, `--force`, `-f`, `--allow-empty`, `-c` or `--no-edit`. A test asserts this over every planning case.

<!-- Source: Variant B, Section 5.3 FR-027 items 2-3 (foreign-change, no-snapshot) and Variant C, Section FR-017 (never absorb pre-existing work), with the debate Round 3 rulings INV-003 and INV-025 - merged per Change #19 -->

- **FR-073 (accepted tree)** Before flushing the first `complete` line of a task generation that will be eligible (FR-103), the executor pins the accepted candidate as `refs/<package>/implement/<slug>/accepted/T<id>-s<start ordinal>`. For a compliant `complete`, the pin points at the tree on the header of the review that gave the verdict (`refs/qa.md:178`). For a post-Ruling `complete`, it points at a fresh private-index snapshot, because a Ruling accepts the tree as it stands (`refs/retry.md:504`). If the review recorded `tree=none` (`refs/qa.md:182`) the boundary refuses `no-snapshot`; if the pin is missing it refuses `no-accepted-tree`. Neither weakens the check.
- **FR-074 (`changed-after-review`)** At prepare, every product path in S must equal the accepted tree. If Q6 extras or anything else rewrote a reviewed file, the boundary refuses `changed-after-review`, names the paths and prints, as advice, `git restore --source=<accepted ref> -- <paths>` with "compare first: this overwrites any newer edit". A later flagged run proceeds once the paths match again or after an actual renewed review or Ruling.
- **FR-075 (`foreign-change`)** For each product path p in S, the blob of p at `q0-head` must equal the blob of p in the Q0 start tree; otherwise `foreign-change`. The path carried the person's uncommitted change from before the task started. The executor never first-commits, stashes, resets or discards that work.

<!-- Source: Base (original, modified) - base FR-062 and D8 package rule refined to literal files by the debate Round 3 ruling INV-018 (accepted risk), merged per Change #20 -->

- **FR-076 (package expansion)** For a managed run, S includes the current package expanded to literal files with `git ls-files -z --cached --others --exclude-standard -- <pkg-dir>`, written into the FR-035 pathspec file. A `files=` entry that is a directory refuses `directory-entry`. `git add -- .dev/tasks` still runs, so other packages stay staged and are not committed. Accepted risk: a file a person adds inside the current package is committed with it, because nothing can tell it from evidence; the package has one owner (`refs/managed-workspace.md:94`). This does not relax path containment, plan/source hashes, the frozen-candidate check or the exclusion of other packages, and a known concurrent ownership conflict still stops.

### 6.5 Hook refusal

<!-- Source: Base (original, modified) - FR-064 uses the FR-036 classes and the rewritten/ pin, FR-065 allows a later attempt only after disclosure (Variant B, Section 4.1 FR-021; Variant C, Section FR-020 renewed review; debate Round 3 ruling INV-020); base automatic re-plan removed; merged per Change #15 -->

- **FR-064** Every non-success class (FR-036) appends `T<ids>: commit refused key=<key> attempt=<n> reason=<class>` to `commits.md` (FR-100), saves the first 40 lines of output to `<run-dir>/commit-refused-<n>.log` or `<pkg-dir>/artifacts/commit-refused-<n>.log`, and stops `E-COMMIT-REFUSED`. For `hook-rewrite`, `hook-rewrite-evidence` and `hook-rewrite-committed` the agent pins the rewritten tree as `refs/<package>/implement/<slug>/rewritten/<key>-a<n>`, and the refusal prints its `git diff --stat` against the accepted tree. The executor never retries in the same run, never uses `--no-verify`, `-n`, `SKIP=`, `commit-tree` or `--amend`, and never edits a hook or `core.hooksPath`.
- **FR-065** A later run with `--commit-tasks` may make a new attempt only as FR-107 allows: after `hook-rewrite-evidence`, with freshly rebuilt evidence and no product re-review; after `hook-rewrite`, only once the changed product paths are restored to the accepted tree, or pass an actual renewed review or Ruling given after the refusal displayed them. A flag typed before that disclosure is not that review. A `hook-rewrite-committed` refusal has moved HEAD, so it is never retried; it is settled only through the owner choices of FR-121 (FR-107, row "refused with HEAD ≠ parent").

### 6.6 Message format

<!-- Source: Base (original, modified) - code-point length (debate Round 3 ruling INV-015); Implement-Plan trailer from Variant B, Section 5.4 FR-028; boundary-key trailer from Variant C, Section FR-019; merged per Change #14 -->

- **FR-066** The subject is `<type>[(<scope>)][!]: <summary>`, at most 72 Unicode code points of the decoded header, counted without normalization; drafting cuts at the last space at or before code point 72, and `check-message` counts the same way. `<type>` is one of `feat`, `fix`, `refactor`, `docs`, `test`, `build`, `ci`, `chore`, `perf` or `style`. The second line is blank. The body has one line per task: `T<id>: <task title>`. The trailer block has `Implement-Plan: <slug>`; one `Implement-Task: T<id> (<verdict>)` line per member in source order; `Implement-Boundary: <64-hex key>` (FR-103); and `Implement-Ledger: <repo-relative ledger path>`. Attribution trailers that the session's own standing instructions require come after these; the helper adds none. `check-message --implement` enforces all of this.

<!-- Source: Base (original) -->

- **FR-067** A task completed by a Ruling (a non-compliant verdict with operator acceptance) is committed like any other task. Its trailer carries the non-compliant verdict, so the acceptance is visible in history. A Ruling never authorizes a commit (`refs/ledger.md:239`); only `--commit-tasks` does.

<!-- Source: Debate Round 2 (Variant A's note on refs/retry.md:504 and Variant B's note on the Ruling cost-if-wrong) - merged per Change #28 -->

- **FR-078 (Ruling text with commits on)** `refs/retry.md:504` "(no commit follows it)" becomes "(no commit follows it unless this run carries `--commit-tasks`; then the accepted task is committed at the next boundary, FR-073)". When the current `run` line is `on`, every Ruling request states in its cost-if-wrong that the accepted task will be committed at the next boundary (`refs/qa.md:254`). The Ruling still authorizes no commit (`refs/ledger.md:239`).

### 6.7 Ledger, STOP table and archive helper changes

<!-- Source: Base (original, modified) - base FR-068 and FR-069 (ledger COMMIT: records, archive parser change) deleted because commit state moves to the sidecar of FR-100 (Variant B, Section 5.5 FR-029), per Change #22 -->
<!-- Source: Base (original, modified) - two STOP codes kept; open reason class, transient E-RESUME-NEEDED reasons and the archive-gate refusal from the debate Round 3 text (ruling INV-023); merged per Change #18 -->

- **FR-070** The STOP table in `SKILL.md` gains two rows. `E-COMMIT-PRECONDITION`: a Wave 0 commit precondition failed (FR-054); product writes: no; ledger: no. `E-COMMIT-REFUSED`: a boundary refused, is unsettled, or its state is invalid; product writes: no next task; ledger: unchanged (the task stays `complete`); `commits.md`: the refused, uncertain or run line only. Its reasons form the open class `[a-z][a-z-]*`; the ones this spec uses are the FR-036 classes and `unsettled`, `out-of-protocol`, `uncertain`, `candidate-changed`, `sidecar-mismatch`, `sidecar-corrupt`, `branch-changed`, `branch-unproven`, `head-moved`, `foreign-change`, `changed-after-review`, `no-accepted-tree`, `no-snapshot`, `snapshot-failed`, `snapshot-unsupported`, `outside-changed`, `outside-unverified`, `pin-conflict`, `path-unrepresentable`, `outside-repo`, `directory-entry`, `message`, `helper-missing` (FR-019).

  `E-RESUME-NEEDED` gains two transient reasons, listed in `refs/retry.md` "Halts and transient stops": `commit-interrupted` (FR-116) and `index-locked` (`git rev-parse --git-path index.lock` exists). Neither writes a terminal line. Which code a lock gets: the Wave 0 commit preflight of a flagged run (FR-054) stops `E-COMMIT-PRECONDITION reason=index-locked` before the ledger is opened; a lock found by reconcile, at a commit position or after an interrupted commit stops `E-RESUME-NEEDED reason=index-locked` (FR-116).

  Managed archive gate step 1 (`refs/managed-workspace.md:52`) also refuses `E-ARCHIVE-BLOCKED reason=unsettled-boundary` before any move while a due, pending, refused or uncertain boundary exists. It reads the ledger and `commits.md` (a due boundary is found from the ledger's anchors, FR-103 and FR-105), and adds no record kind to the task ledger. This is a second line of defence behind FR-077.

  The sentence at `SKILL.md:51` is revised to name both new codes and to say that `E-RESUME-NEEDED` is the only code the retry ladder and the commit step's transient stops add.

<!-- Source: Base (original, modified) - summary reads the sidecar lines per Change #22 -->

- **FR-071** The final summary (`SKILL.md`, "Done") prints one line per `commit sha=` or `recovered` line of this ledger's `commits.md`: `<short sha> <tasks> <subject>`.

<!-- Source: Base (original, modified) - section references renumbered per Change #5; ref renamed refs/commit-step.md (Variant B, Section 5.5 FR-032) with the two-part load rule and the SKILL.md budget, per Change #21; FR-019, FR-071 and FR-078 placed in a part per review-3 note M3-6 (placement part only) -->

- **FR-072** The new ref `refs/commit-step.md` in `sc-implement-protocol` holds §6.3-§6.6 and §7. It is loaded when `--commit-tasks` is present or a `commits.md` exists in the ledger directory (legacy `<run-dir>/`, managed `<pkg-dir>/artifacts/`), and not otherwise, the same way `refs/retry.md` is loaded only when needed (`SKILL.md:17`). It has two parts. "Reconcile and settle" holds the rules every such run follows, with or without the flag: the `off` run line (FR-051), settle before advance (FR-077), FR-100..FR-108 as they read, verify and record existing state, the outside-S comparison of a resumed attempt (FR-113), FR-114..FR-116, owner resolution (FR-120..FR-125), pin lifetime and release (FR-131), the no-lock rule (FR-133), the implement-side helper check of FR-019 and the final summary (FR-071). "Commit procedure" holds the trigger, staging, commit, hook and message rules (§6.3-§6.6 apart from FR-077), FR-050's in-run grant rules (continuation and revocation), capture and snapshot (FR-110..FR-112), `verify` (FR-130), retry inputs (FR-132) and the Ruling text of FR-078, and applies only with the flag, as does the Wave 0 commit preflight (FR-054) in `SKILL.md`. The test requirements (FR-109, FR-118, FR-126) stay in the spec and are not copied into the ref. The `/sc:git` side of FR-110..FR-117 lives in `sc-git-protocol/refs/safety.md`, which every write loads (FR-018), so `commit` and `submodule commit-pointer` both get it. A run without the flag never prepares, stages, makes or retries a commit. `SKILL.md` itself gains only the Q8a line, the Wave 0 option and step, the two STOP rows and the load rule; `SKILL.md` grows by at most 15 lines (NFR-012). The load rule is one `SKILL.md` line and counts in that budget. The implement protocol never invokes `/sc:git` or `Skill sc:git-protocol`. `sc-git-protocol/refs/commit.md` keeps its name.

## 7. Commit state, recovery and owner resolution in `/sc:implement`

<!-- Source: Base (original, modified) - new section placed after §6 per Change #5; its content comes from Changes #22, #23, #25, #26 and #27 -->

### 7.1 State location and line forms

<!-- Source: Variant B, Section 5.5 FR-029 (sidecar commits.md) and Variant C, Section FR-022 and FR-023 (record before the attempt; a post-commit result is not part of its own commit, unique contribution U-017), with the debate Round 2 line forms - merged per Change #22 -->

- **FR-100 (state location and line forms)** Commit state lives only in `commits.md`: legacy `<run-dir>/commits.md`, never staged (like the legacy ledger, `refs/ledger.md:3`); managed `<pkg-dir>/artifacts/commits.md`, staged with `.dev/tasks`. Task-ledger record forms, the resume regex, `E-LEDGER-CORRUPT` and `archive_workspace.py` are unchanged. Line forms (one regex each, documented once in `refs/commit-step.md`, parsed by `vcs_plan.py`, pinned by parity test T-10):
  - `run <n>: commit-tasks=(on|off)[ reason=revoked] ledger-lines=<k> branch=(<full symbolic ref>|-) at=<ISO-8601> args="<option prefix>" source=<path|inline:<hash8>> worktree=<id>` (`branch=-` records a detached HEAD and is valid only on an `off` line; a `-` branch never satisfies FR-054 or its branch check)
  - `T<ids>: commit prepared key=<64-hex> attempt=<n> parent=<40-hex> branch=<ref> paths=<sha256 of the path list> accepted=<ref>[,<ref>...] plan=<hash|-> source=<hash|->`
  - `T<ids>: commit (sha|recovered)=<40-hex> key=<64-hex> attempt=<n>[ outside-changed=<n> wt=<ref>]`
  - `T<ids>: commit skipped key=<64-hex> reason=(empty|mixed-authorization)`
  - `T<ids>: commit (refused|uncertain) key=<64-hex> attempt=<n> reason=<token>[ rewritten=<ref>]`
  - the two `resolved` forms of FR-120.

  The exact path list of each attempt is saved beside the sidecar as `commit-paths-<key>-a<n>.txt`, where `<key>` is the full 64-hex key (FR-103) (NUL-delimited) and its SHA-256 is the `paths=` value. A record is appended and flushed before the side effect it announces. The parser rejects unknown forms, malformed lines and a truncated tail (FR-102); it never repairs. A terminal line written after a commit is not part of that commit: in a managed run it stays staged with `.dev/tasks` and enters the next boundary commit, and after the last boundary it stays staged and the final summary says so; in a legacy run the sidecar is never staged (see above), so the line stays in the untracked file and the final summary says so.

### 7.2 Run segments, eligibility and settlement

<!-- Source: Debate Round 3, INV-001 items 1-9 (Variant C's final text, the same mechanism as Variant B's HR-1.1..HR-1.8, with Variant A's settle before advance) and the ruling INV-014 - merged per Change #23 -->

- **FR-101 (run record and write order)** Every invocation with the flag, and every later invocation where `commits.md` already exists, appends a bounded `run` line (FR-100 form) after ledger validation (Wave 0 step 6) and before any new task record or ordinary run-evidence append. It holds a monotonically increasing `run`, `commit-tasks=on|off`, `ledger-lines=<k>`, the full symbolic `branch=`, the bounded option prefix and source identity (`inline:<hash8>` for an inline prompt; never the full prompt or credential-bearing text), a timestamp and the repository/worktree identity. A first unflagged invocation with no sidecar creates none. A revocation appends `commit-tasks=off reason=revoked` with its current offset before another attempt. Only the executor appends `run` lines.
- **FR-102 (counting and validation)** `k` is the number of newline bytes in the ledger plus one when the file is not empty and does not end in a newline. A ledger line at position `p` belongs to the last sidecar-ordered `run` line with `k < p`; equal offsets are resolved by sidecar order. Positions at or before the first offset have no grant. Decreasing offsets, an offset beyond the current ledger, or a `run` line that contradicts its own binding refuse `E-COMMIT-REFUSED reason=sidecar-mismatch`. An unparseable sidecar tail refuses `reason=sidecar-corrupt`, without silent repair; like `E-LEDGER-CORRUPT` it is the one state a person repairs by hand. Never concatenate a new ledger record onto an unterminated tail: stop for ledger recovery instead. Counting an existing line is not permission to repair it.
- **FR-103 (stable anchor and key)** A task generation is its actual `start` record occurrence, not its tree contents. Its **anchor** is the first valid `complete` line after that `start`. A boundary is **eligible** only when every member's anchor lies in an `on` segment. Later `complete` or re-review lines (`refs/ledger.md:84-86`) never create, revive or re-authorize that generation. The boundary **key** is SHA-256 over a canonical tuple of the repository/worktree identity, the ledger and source identity, the ordered task ids, and each member's start-record ordinal and full start SHA. Every stored key and machine reference uses all 64 hex characters; a 12-hex prefix is for display only. A task completed wholly outside an `on` segment, or before this feature existed, is never committed later.
- **FR-104 (proof before completion)** For an eligible first completion, the accepted candidate is pinned (FR-073) before the `complete` line is flushed and is bound to the same start occurrence. A missing tree refuses `no-accepted-tree` or `no-snapshot`. The Q0 pin, the original branch and `q0-head`, and the accepted pin are kept through every unsettled state, including a due boundary with no prepared line (pin lifetime: FR-131).
- **FR-105 (due versus moved-on)** An eligible all-complete boundary with no prepared or settling line is **due**. Late preparation is crash-explained only when no other task's `start` line follows any member's anchor and no task is open. Otherwise the run stops `E-COMMIT-REFUSED reason=out-of-protocol`, names the later `start` lines and offers the FR-121 choices; those later tasks are never committed automatically. Missing preserved proof also refuses; the absence of a prepared line is not proof that no eligibility existed.
- **FR-106 (reconcile order)** Wave 0 order: step 6 (ledger); for a managed run, resolve the location and verify the existing `PLAN:` and source pins (a changed plan stops `E-PLAN-CHANGED` before anything is committed); take any outstanding outside-S comparison of FR-113 **before** appending the new `run` line; append the `run` line; reconcile; then steps 7-9 (including the `codegraph.md` append), task selection, complete-task cleanup, the legacy all-complete return, FINAL and archive. The new `run` line never changes the frozen sidecar bytes against which an earlier commit is verified (FR-108). **`vcs reconcile`** reads the ledger, `commits.md`, whether this run carries the flag and, for a managed run, the `PLAN:` and source pins; it applies FR-102, FR-103, FR-105 and the FR-108 predicate and prints one JSON object listing each boundary with its full key, members, FR-107 state and the action this run may take, or a `sidecar-mismatch` or `sidecar-corrupt` refusal. It writes nothing; the agent makes every append.
- **FR-107 (settle before advance; state table)** Due, pending, refused and uncertain boundaries are **unsettled**; a terminal failed or refused attempt does not satisfy its boundary. FR-077 applies while any is unsettled. Behaviour per state:

  | State | Run with the flag | Any other run |
  |---|---|---|
  | due, crash-explained | Prepare now with the Q8a checks: HEAD equals the first member's `q0-head`, the branch check (FR-054), `foreign-change` (FR-075), accepted-tree equality (FR-074) | STOP `E-COMMIT-REFUSED reason=unsettled` with the FR-121 choices |
  | due, out-of-protocol | STOP `reason=out-of-protocol` with the choices | same |
  | pending (prepared, no terminal line, HEAD = parent), or refused with HEAD = parent | A new attempt only when the product paths equal the accepted tree or the `rewritten=` tree the refusal displayed, after FR-065's review rule; package evidence is rebuilt and frozen anew; otherwise append `refused reason=candidate-changed` and STOP with the choices | STOP `reason=unsettled` with the choices; may record a proved existing commit as `recovered`, never commits |
  | refused with HEAD ≠ parent | STOP with the choices | same |
  | uncertain | STOP `reason=uncertain` with the choices; never retried automatically | same |
  | settled (`sha=`, `recovered`, `skipped`, `resolved`) | nothing | nothing |

  There is no automatic retry in the same run. Every unsettled STOP offers the FR-121 choices.
- **FR-108 (prepared record and exact recovery predicate)** Before the first `git add` of an attempt, append the prepared line (FR-100) with the attempt number, full key, expected parent and branch, the path-list hash of exact S, the accepted binding, and the managed plan and source hashes. After that append, the helper builds the full final candidate tree from the parent plus S, including the managed sidecar's frozen prepared bytes, and the agent pins it with a literal `git update-ref refs/<package>/implement/<slug>/boundary/<key>-a<n> <tree>`. The tree hash lives in that external ref, never inside the sidecar it hashes. Only all of these prove `committed` (or `recovered` on a later run): HEAD has exactly one parent and it is the prepared parent; HEAD's tree equals the pinned candidate; the changed paths are the authorized subset of S; the `Implement-Boundary:` trailer carries the key; the managed plan and source bytes are unchanged. HEAD equal to the parent is pending, not success. Any other history, or incomplete proof (a prepared line without its pins), is `uncertain`. A person's later commit is not a reason to walk history or create a duplicate.
- **FR-109 (required tests; mapped to T-19)** Crash after the accepted pin and the `complete` flush but before preparation; resume flagged twice: exactly one commit. Resume unflagged first: no new `start`, no commit, no lost pin. Cover: an unflagged completion followed by a flagged re-review (not committed); revocation; equal segment offsets; an unterminated parseable last ledger line (counted in the earlier segment); decreasing and out-of-range offsets; a later `start` written by a stale installed copy (`out-of-protocol`); a changed managed plan (`E-PLAN-CHANGED` before reconcile prepares); repeated `complete` lines; a resumed batch and a mixed batch; `git gc --prune=now` between crash and resume; a crash after the commit and before the result in managed and legacy runs, where the new `run` line must cause neither a false recovery failure nor a false outside-S report.

### 7.3 Protecting work outside the commit set

<!-- Source: Debate Round 3, INV-021 items 1-9 (Variant C's final text, built on Variant B's HR-2.1..HR-2.7, with Variant C's per-attempt immutable pins and honest coverage); replaces the base Wave 0 dirty pre-check - merged per Change #26 -->

- **FR-110 (two independent proofs)** A candidate tree proves what the commit may contain; a worktree tree preserves content outside S. One never substitutes for the other. Each prepared attempt names two sibling refs, `refs/<package>/implement/<slug>/boundary/<key>-a<n>` and `refs/<package>/implement/<slug>/boundary-wt/<key>-a<n>`. Attempt numbers are durable and monotonic. Pins are create-once: an existing different target refuses `pin-conflict`, and a retry never overwrites an earlier recovery pin. Sibling names avoid the git rule that a ref cannot be created under an existing ref.
- **FR-111 (capture before commit)** After the visible `git add` calls and immediately before the visible commit, the agent builds the worktree snapshot with the Q0 private-index method (`SKILL.md:124`: private index, `read-tree HEAD`, `add -A`, `write-tree`), starting from HEAD rather than copying real-index flags, and pins it with a literal `git update-ref` before any commit call. A failed or incomplete snapshot or pin appends `refused reason=snapshot-failed` and makes no commit. A prepared attempt that lacks either pin is incomplete proof and is never retried as if preparation had succeeded. The helper performs no hidden commit, ref write or user-index change.
- **FR-112 (what the snapshot covers)** It covers tracked worktree contents and non-ignored additions, including real-index assume-unchanged and skip-worktree entries; unrelated staged entries are preserved separately by `--only`. It is not a backup of ignored files, empty directories, file metadata or submodule interiors. A configuration whose snapshot would not be lossless refuses `snapshot-unsupported` before the commit. Ignored data is never force-added. Concurrent writers in the same worktree and arbitrary trusted hook or filter behaviour stay outside the single-writer guarantee.
- **FR-113 (compare every attempt)** After any normally finished attempt, take a second snapshot before appending the result line or any log, and compare every path outside exact S with the before tree, including additions, deletions, modes and symlinks. For a resumed attempt, take the comparison before the new `run` line (FR-106). A failed or incomplete comparison stops `E-COMMIT-REFUSED reason=outside-unverified` and keeps the before pin; it is never read as "no changes". The whole set is compared; printing at most 20 entries, with the total count and a truncation notice, is only a display limit.
- **FR-114 (detected damage)** A result line records `outside-changed=<n>` when nonzero and names the attempt's worktree ref; the path details go to the bounded attempt log. The before pin is kept after any result, `resolved` line or package archive while that report is outstanding. The invocation stops `E-COMMIT-REFUSED reason=outside-changed` even when the commit itself verifies; the proved commit is not relabelled pending and no second commit is made. The next invocation reports the saved pin before it proceeds under its own flags; this report is not a second unsatisfied boundary, and the pin is never deleted silently.
- **FR-115 (recovery is explicit)** The STOP prints the saved ref and, for saved paths only, `git restore --source=<saved-ref> -- <literal-paths>`, with "compare first: this overwrites any newer edit". A path that did not exist in the before snapshot needs separate handling, never a blanket restore or delete. The report also names the real-index content and known hook patch and lock locations as additional evidence. The executor never restores, resets, stashes, deletes a lock or deletes a saved patch on its own. The pin stays until the owner directs its release.
- **FR-116 (timeout, interruption, quiescence)** The commit call uses the Bash tool's maximum timeout, 600000 ms; hooks and signing are never disabled to meet it. A reported timeout, or a git exit status above 128, leaves the prepared attempt open, writes no terminal line and stops `E-RESUME-NEEDED reason=commit-interrupted`, saying: check that no git or hook process is still running in this worktree before restoring anything or re-running. Read-only observations may be shown as provisional. A later invocation must establish that the earlier git and hook processes have stopped before the final comparison, classification, restoration, retry or owner resolution. An `index.lock` stops `E-RESUME-NEEDED reason=index-locked`; the absence of a lock alone is not proof that processes stopped. The executor never kills an orphan or reclaims a lock. Exit status 1 is a hook refusal (FR-036); 128 is `commit-error`.
- **FR-117 (shared scope)** FR-110..FR-116 also apply to `/sc:git commit` and to `submodule commit-pointer`, with `/sc:git` refs named `refs/<package>/git/boundary-wt/<timestamp>` and the report printed instead of a sidecar line. For a pathless `/sc:git commit`, S is the index change set frozen before the call (FR-038), and staging `.dev/tasks` never widens it. This grants no extra operation and weakens no host denial. Hooks always run normally: no bypass, no alternate hooks path, no `commit-tree`, no hidden wrapper commit. A `/sc:git` pin is deleted with a visible `git update-ref -d` call after a clean comparison, and kept only while an outside-change report about it is outstanding (FR-114, FR-115).
- **FR-118 (tests; mapped to T-20)** Hook-manager emulations that run the framework's exact command sequence and name the source revision they copy, plus one real-framework fixture skipped when the framework is not installed. Cover: normal success; rejection; SIGTERM to the process group; SIGTERM to git alone with an orphan hook; SIGKILL; timeout; a stale lock; staged, unstaged, assume-unchanged and skip-worktree edits outside S; deletion and mode changes; snapshot failure; an unsupported configuration. Prove that outside edits restore byte for byte from the saved pin and that unrelated index entries keep their meaning. A second failed attempt cannot overwrite the first pin; `git gc` cannot prune it; a success with outside damage stops without a duplicate commit; a legacy resume's own new `run` line causes no false report.

### 7.4 Owner resolution of an unsettled boundary

<!-- Source: Debate Round 3, INV-027 items 1-7 (Variant A's record form with Variant B's six amendments: full 64-hex key, reply only after the disclosure, abandon always offered, unattended behaviour, the consequence of abandoning, worktree pins kept) - merged per Change #27 -->

- **FR-120 (record forms)** The executor appends one validated line to `commits.md`, never to the task ledger. Two distinct forms:
  - `T<ids>: commit resolved key=<64-hex> as=abandoned at=<YYYY-MM-DD> quote="<owner words>"`
  - `T<ids>: commit resolved key=<64-hex> as=adopted head=<40-hex> basis=<candidate|accepted> differs=<n> at=<YYYY-MM-DD> quote="<owner words>"`

  Regexes: `^T([0-9A-Za-z.,-]+): commit resolved key=([0-9a-f]{64}) as=abandoned at=[0-9]{4}-[0-9]{2}-[0-9]{2} quote="((?:[^"\\]|\\.)+)"$` and `^T([0-9A-Za-z.,-]+): commit resolved key=([0-9a-f]{64}) as=adopted head=[0-9a-f]{40} basis=(candidate|accepted) differs=[0-9]+ at=[0-9]{4}-[0-9]{2}-[0-9]{2} quote="((?:[^"\\]|\\.)+)"$`. `head`, `basis` and `differs` are required for adoption and forbidden for abandonment. The decoded quote is 1 to 200 Unicode code points, escapes quotes and backslashes, has no raw newline or control character and is never silently truncated. If the reply cannot be represented, the executor asks for a short scoped reply instead of inventing a quote. The stored key is always the full key.
- **FR-121 (information before choice)** Every STOP for an unsettled boundary prints its full key, a unique short display label, the members, the state, the prepared parent or the original Q0 parent when known, current HEAD, exact S, and a bounded changed-path summary (`git diff --stat <accepted or candidate> HEAD -- <S>`). It always offers `abandon`; it offers `adopt` only when FR-123 holds. A missing comparison pin is shown as unavailable, never as zero differences. Missing proof does not prevent abandoning a known boundary whose identity and members are intact.
- **FR-122 (who may answer)** Only the person's own reply, given after that STOP in the same conversation. A unique displayed prefix may select a key; a reply naming no key counts only when exactly one key was displayed. Not a resolution: text typed earlier (the inline prompt, a plan or brief field), a generic "continue", another agent's message, or a coordinator's answer. A coordinator session may record its own user's qualifying chat confirmation under the owner-record rule; an agent-to-agent relay is not that confirmation. Under `--unattended` the gate is reported blocked and never asked, with no automatic default. Stored grant or resolution data is evidence, not proof of who answered.
- **FR-123 (`vcs resolve-check`, read-only)** It resolves the displayed key to one full known unsettled identity and validates the sidecar. Refusals, with no append: `unknown-boundary`, `ambiguous-key`, `already-settled`. `abandon` needs no ancestry or candidate pin. `adopt` needs a known parent, HEAD different from the parent, `git merge-base --is-ancestor <parent> HEAD` exiting 0, proved quiescence (FR-116) and an available disclosed comparison tree: the frozen candidate when one was prepared (`basis=candidate`), otherwise the accepted tree of the due boundary (`basis=accepted`). `differs` counts paths in S whose object id, mode or presence differ. Missing ancestry or objects refuse `adopt-not-descendant` or `adopt-unverifiable`; exit 128 is never success; `abandon` stays available. HEAD and the basis are re-read just before recording; if the disclosure changed, redisplay and ask again. The parent of a never-prepared boundary is the first member's `q0-head`.
- **FR-124 (meaning and limits)** `abandoned` settles the key permanently with no commit and no file change; later automatic attempts for the key are forbidden. Its STOP text says that remaining uncommitted product edits can make a later overlapping task refuse `foreign-change` until the person commits or reverts them. `adopted` records the owner's acceptance of the displayed history as settlement, even with `differs` nonzero; it is not a verified commit, not a changed QA verdict, not retroactive commit authority, and not a waiver of plan integrity, FINAL, archive or permission checks. Neither answer authorizes restoration, history repair or publication.
- **FR-125 (idempotent continuation and cleanup)** After the durable append, a repeated reply or a resumed reconcile recognizes the settlement and makes no commit and no second resolution line. Cleanup happens only after the append and can resume after a crash; failing to delete a pin does not undo the settlement. Ordinary boundary pins are released with visible `git update-ref -d` calls; every attempt pin that protects an outstanding outside-S report (FR-114) is kept, through archive too. Reconcile then runs again, and the run continues only if every other gate passes under its own flags. No resolution overrides corrupt sidecar or ledger recovery, live processes, a stale lock or `E-PLAN-CHANGED`.
- **FR-126 (tests; mapped to T-21)** Every unsettled state, in a flagged and an unflagged run, offers `abandon` (table-driven). A person's post-crash commit, `hook-rewrite-committed` and an out-of-protocol due state: adopt when justified, then resume and archive with no duplicate commit. Reject: a reply typed before the STOP, an agent-origin reply, an ambiguous prefix, a stored key shorter than 64 hex, adoption fields on an abandonment, missing adoption fields, HEAD changed after the disclosure, unrelated history, an unavailable comparison pin. Abandon a known boundary whose candidate pin is missing. Crash after the resolution append and before cleanup; resume twice; exactly one settlement. Earlier outside-S pins survive both answers.

### 7.5 Verification, pin lifetime, retry inputs and concurrency

<!-- Source: Debate Round 2 C-010 resolutions (prepared-before-add structure, pinned and frozen candidate, full key), Variant B, Section 5.5 FR-029 (pin deferral, resume Row 1 clause; Round 2 E7 pin rule for diff point C-011), the debate Round 3 ruling INV-004, and Variant C, Section FR-022 - merged per Change #25 -->

- **FR-130 (`verify`)** Inputs: the key, attempt, prepared parent, candidate ref, worktree ref, exit status. It applies FR-108 and returns one of `committed sha=<40-hex>`, `pending` (HEAD = parent), an FR-036 class, or `uncertain`, plus the FR-113 outside-S comparison. It writes nothing.
- **FR-131 (pin lifetime)** The Q0 pin, the accepted pin, the candidate pin and the worktree pin of every member of an unsettled boundary are kept until that boundary's settling line. Reviewed-tree refs (`retry/T<rid>/r<k>-<j>`) may still be deleted at `complete` once their tree is held by the accepted pin. Amend the Q7 cleanup sentence (`SKILL.md:129`) and resume Row 1 (`refs/ledger.md:157`) so that neither deletes an `accepted/`, `boundary/`, `boundary-wt/` or `rewritten/` pin, or the Q0 pin of a member of an unsettled boundary, on any run, flagged or not. After settlement the executor deletes ordinary boundary proof with literal `git update-ref -d` calls (except pins FR-114 keeps). The final summary lists every leftover pin with its `git update-ref -d` line.
- **FR-132 (retry inputs)** A retry or a late preparation compares only the product paths (the `files=` union) with the accepted tree or the disclosed `rewritten=` tree. Package evidence is always rebuilt and frozen anew for the new attempt, so the `codegraph.md` line every run appends (`SKILL.md:79`) never blocks a retry; a new attempt is never compared with the old package snapshot. Reconcile runs after the managed identity and `PLAN:` checks and before steps 7-9 (FR-106).
- **FR-133 (no lock)** One `/sc:implement` invocation writes a given ledger and `commits.md` at a time; there is no lock (`refs/ledger.md:149`). Worktree isolation is required only for workers (WC-11).

## 8. Branch cleanup reuse

<!-- Source: Base (original) - renumbered from §7 per Change #5; requirement-level changes are tagged below -->

<!-- Source: Variant C, Section FR-029 (route names every /sc:worktrees verb, unique contribution U-020) - merged per Change #32 -->

- **FR-080** `/sc:git branch cleanup` is a read-only routing operation. When the checkout has `scripts/worktree_cleanup.py` at its top level, it prints the `/sc:worktrees` route and stops, running nothing: `list` (read-only), `archive` (writes the finished worktree's `.dev` files to the evidence repository even without `--apply`, so it is not an inspection), and `retire` or `prune` (remove only with `--apply`). The person chooses. Otherwise it prints the notice of `worktrees.md:45`.

<!-- Source: Base (original, modified) - helper path renamed per Change #6 -->

- **FR-081** No new code anywhere runs `git branch -d`, `git branch -D`, `git branch --delete`, `git push --delete` or `git push <remote> :<branch>`. A repository-wide static test over `<pkg>/skills/sc-git-protocol/scripts/`, `sc-git-protocol` and `git.md` asserts this.

<!-- Source: Base (original) -->

- **FR-082** Local branches without a worktree are not cleaned by any command. That gap is recorded as accepted residual scope. It can be revisited only if the owner names it. It is not built here.

## 9. Interaction with the worker contract and unattended mode

<!-- Source: Base (original) - renumbered from §8 per Change #5; requirement-level changes are tagged below -->

- **FR-090** `/sc:git` stays on the never-as-worker list, unchanged (`WORKER-CONTRACT.md:23`; `NEVER_AS_WORKER` in `tests/skills/test_worker_contract.py:474-485`). `git.md` gets no `## Unattended mode` section, so the brief guard still refuses it under case 3.

<!-- Source: Base (original, modified) - delivered K3 rule with the commit positions and the unchanged WC-9 grant (Variant B, Section 8 FR-040; Variant C, Section FR-032), merged per Change #33 -->

- **FR-091** Rewrite the K3 sentence at `WORKER-CONTRACT.md:42` to the delivered rule: per-task commits are delivered as `/sc:implement --commit-tasks`, typed by the person in an ordinary attended session; they fall only at the commit positions Q8a, R0 and L0, between a task's `complete` line and the next task's start, and never while a member of a parallel batch lacks `complete`; `--commit-tasks` is refused under `--unattended` (`E-COMMIT-PRECONDITION reason=unattended`). The worker's own end-of-Task commit grant (WC-9, lines 42-43), including "A command's own commit step stays off under `--unattended`", does not change, and the new pins under `refs/<package>/implement/` stay within the refs line 45 already allows.

<!-- Source: Base (original) -->

- **FR-092** When the P4 conversion adds `## Unattended mode` to `implement.md`, that section lists `--commit-tasks` as refused before any work. It writes `worker_status: failed` with the flag in `reason` (WC-4).
- **FR-093** In launched sessions, the launch-level guard decides. At level `full --submit`, commits are allowed. At other levels, the commit Bash call is refused (`LL-COMMIT`) and maps to `reason=blocked-by-host` (FR-064). Nothing reads the guard's store or probes the launch level, because reading the store would be TAMPER (`launch-level-guard.sh:777`).

<!-- Source: Base (original, modified) - section reference renumbered per Change #5; trigger and settle-before-advance wording per Change #23 -->

- **FR-094** The coordinator's own commit rules (`WORKER-CONTRACT.md:247`) do not change. The commit-step trigger (FR-056) and settle before advance (FR-077) agree with the coordinator's freeze rule: no commit while a plan is halted (§6.3).

## 10. Test obligations

<!-- Source: Base (original, modified) - renumbered from §9 per Change #5; base test matrix kept with rows edited: T-02 per Change #13, T-09 per Change #21, T-12 per Changes #9 and #30, T-13 per Change #6, T-14 per Change #28 (Variant B, Section 9.2 consumer inventory), T-15 per Change #24, T-18 per Changes #33 and #35, T-01, T-04, T-06, T-07, T-08, T-10, T-11 and T-16 per Change #35; rows T-19..T-27 added from Variant C, Section FR-034 (fault injection) and the debate Round 3 test lists, per Change #35 -->

All tests run with `uv run pytest`. The new ones are proposed under `tests/vcs/` unless another file is named.

| ID | Test | What it proves |
|---|---|---|
| T-01 | `tests/vcs/test_stage_plan.py` on temporary git repos | Paths: ignored, `.dev/implement/`, gitlink, outside the repo and `<dev>/` are skipped; `<pkg-dir>` is included. Result `nothing` when nothing changed. The boundary cases are in T-19 |
| T-02 | `tests/vcs/test_argv_shape.py` | `add_argv` and `commit_argv` have the FR-035 shape and never contain an FR-063 token |
| T-03 | `tests/vcs/test_helper_readonly.py` with a recording runner | Every git argv the helper builds is in the FR-011 allow-list, with the `--no-optional-locks -c core.fsmonitor=false` prefix |
| T-04 | `tests/vcs/test_hook_refusal.py` | A failing `pre-commit` hook, a hook that rewrites a file and exits 1, and a hook that rewrites and commits, in a temporary repo: each outcome gives its FR-036 class and the `commits.md` refused line (FR-064); HEAD is unchanged where the class says so; the rewrite classes pin the `rewritten/` tree; there is no same-run retry; no argv has `--no-verify` |
| T-05 | `tests/vcs/test_only_semantics.py` | After `git add -- .dev/tasks` and `git commit --only -- <paths>`, other staged entries are still staged and not in the commit. This test checks the FR-033 and FR-062 assumption instead of trusting it |
| T-06 | `tests/vcs/test_check_message.py` | Subject regex, the 72-code-point limit (FR-066), blank line 2, implement trailers including `Implement-Plan:` and `Implement-Boundary:`. Every allowed type is accepted by the `conventional-pre-commit` default type list (UNVERIFIED until this test runs the pinned hook, `rev: v3.0.0`) |
| T-07 | `tests/vcs/test_submodules.py`, with a local superproject and a `file://` submodule | Each FR-040 state is classified correctly, including `target-not-local` (an unfetched gitlink), `submodule-ahead` and `submodule-diverged`; `update` and `commit-pointer` refuse as in FR-041 and FR-042 (including `submodule-unpublished` and the post-commit gitlink check); the `--url` repeat rule and `remote-mismatch` (FR-044); a two-path partial failure (FR-045); the `submodule.recurse` warning appears. Git 2.38.1 and later blocks `file://` submodules unless `protocol.file.allow=always` is set; the test sets it only in its own temporary repos (UNVERIFIED on the CI image) |
| T-08 | `tests/vcs/test_preflight.py` | Detached HEAD, `master`, `main`, `integration` and the `origin/HEAD` target are refused; merge-in-progress and `index.lock` are reported; the `origin/HEAD` notice of FR-032 is printed when the ref is not set; `git-too-old` below `MIN_GIT` (NFR-011) |
| T-09 | `tests/skills/test_implement_commit_rules.py` (static) | `implement.md` Options row and Will Not text (FR-050, FR-053); STOP rows and the revised closed-list sentence (FR-070); `refs/commit-step.md` exists; it is loaded when the flag is present or `commits.md` exists, and not otherwise; without the flag only its "Reconcile and settle" part applies and no commit call is made; the protocol never invokes `/sc:git` (FR-072) |
| T-10 | Sidecar parity test | The sidecar regexes documented in `refs/commit-step.md` equal the helper parser on the same example lines (FR-100), and `refs/ledger.md:127` is unchanged |
| T-11 | Archive test (extend `tests/skills/test_workflow_archive.py`) | A managed package with `commits.md` archives unchanged; an unsettled boundary blocks with `E-ARCHIVE-BLOCKED reason=unsettled-boundary` (FR-070) |
| T-12 | `tests/commands/test_git_command.py` (static) | Front matter (FR-001); Usage forms (FR-002); bare `/sc:git` runs status (FR-004); section order and a single Activation `> Skill sc:git-protocol` (FR-003); no `## Unattended mode`; no `merge`, `push`, `pull` or `fetch` operation in Usage; Will Not text (FR-005), including `push`, "fetch on its own" and the `submodule update` exception, matching §1.4 and NFR-001 |
| T-13 | `tests/skills/test_git_protocol.py` (static) | Registry rows point to existing refs, and every helper verb the registry names appears in `vcs.py --help` (FR-008); the prose lists equal the `vcs_rules.py` constants (FR-013); no `src/<package>/` path (FR-009) |
| T-14 | Fixture, table and consumer updates | S23 `activation` becomes `{"sc:git": "sc:git-protocol"}`, its top-level `mode_flags` stay `[]` and its repeat's `mode_flags` stay `["--smart-commit"]` (`routing_refresh_cases.json:318`, `:327`); `tests/skills/test_worker_contract.py:2953-2960` drops the merge example row; every new or changed line under `<pkg>/{skills,commands,agents}` that matches `WRITE_VERB_RE` (`test_worker_contract.py:1894-1897`) gets exactly one classification row (`never-worker` for `sc-git-protocol` lines; `deferred:P4` for the implement commit-step lines, reason "the per-task commit step is off under --unattended (WC-9); /sc:implement is converted in P4"), and stale rows are removed (`:3227`); the parity parametrization gains `git` (FR-015); `commands/sc-git.md` joins the absence list (FR-014); tests that pin the implement STOP table or option list accept the new rows and option (candidates: `tests/skills/test_task_workspace_lifecycle.py`, `test_implement_severity_static.py`, `test_implement_saved_prompt_rule.py`; which assertions are exact is UNVERIFIED); `tests/core/test_how_we_work_routing_table.py` stays green after the FR-017 edit; `tests/skills/test_primitive_dual_surface_lookup.py` and `tests/worktree_cleanup/` are unchanged and green. The implement-side amendments that ship with them: Q7 cleanup and Row 1 (FR-131), the archive gate (FR-070), the transient reasons in `refs/retry.md` (FR-116) and the `SKILL.md:51` sentence |
| T-15 | `--commit-tasks` scope test (FR-052) | The string appears only in the FR-052 files; the test lists exactly those paths |
| T-16 | No-flag regression | A legacy and a managed run without `--commit-tasks` and without `commits.md` create none; with an existing `commits.md`, an unflagged run loads `refs/commit-step.md`, appends one `off` run line, reconciles, STOPs `reason=unsettled` on an unsettled boundary before task selection, and makes no commit; the existing implement tests pass unchanged |
| T-17 | No-deletion scan (FR-081) | No branch-deletion or remote-deletion argv in the new code or primitives |
| T-18 | Gate | `make verify-sync` exits 0; `uv run pytest tests/core tests/commands tests/skills tests/recommend tests/docs tests/vcs tests/worktree_cleanup` passes, including `tests/skills/test_worker_contract.py` |
| T-19 | Eligibility and segments (FR-101..FR-109, FR-058) | The FR-109 cases, plus the boundary cases moved from T-01 in the merged terms (eligible and due boundaries, FR-103, FR-105): sequential tasks; a 3-member batch gives one commit; a halt gives no commit; a later flagged run makes a new attempt only as FR-107 allows; tasks completed outside an `on` segment are excluded; an open task means no step. S is built from the members' anchor `complete` lines (FR-062); expected output lines are the `commits.md` forms (FR-100) |
| T-20 | Worktree protection with hook-manager emulation (FR-110..FR-118) | The FR-118 cases |
| T-21 | Owner resolution (FR-120..FR-126) | The FR-126 cases |
| T-22 | Crash points (FR-108, FR-130) | Interrupt before the prepared line, after it, after staging, after the commit but before the terminal line, and after the terminal line; resume twice each time; at most one commit per key; a managed fixture gives no false `hook-rewrite-committed`; a person's commit on top gives `uncertain`; a hook rewriting `source.md` gives `hook-rewrite-pinned` |
| T-23 | Literal paths (FR-035, FR-062 a-e) | A file named `:(glob)*`, a name starting with `-n`, spaces, `d/how to merge.md` through the guard's classifier, a deletion staged, a path absent from all three skipped, a path under a gitlink skipped, a comma refused |
| T-24 | FINAL reads current files (FR-079) | The whole-list review and the managed FINAL judge the current delivery files in legacy and managed runs |
| T-25 | Grant provenance (FR-050) | `not-person`, a Ruling continuation followed by a committed boundary, revocation, an unflagged resume after a flagged run, a stale `on` line |
| T-26 | `/sc:git commit` staging order (FR-038) | The staging order and the frozen pathless S |
| T-27 | Tracked dev-copy refusal (FR-031) | A tracked `<dev>/` file other than `settings.json` refuses `dev-copy-path` |

## 11. Non-functional requirements

<!-- Source: Base (original) - renumbered from §10 per Change #5; requirement-level changes are tagged below -->

<!-- Source: Base (original, modified) - one stated clone/fetch exception for submodule update per Change #30 -->

- **NFR-001 (no outward action)** No new code or primitive pushes, pulls, merges or touches a remote, with one stated exception: `submodule update` may clone or fetch from the URL recorded in `.gitmodules`, which the person's typed line authorizes (FR-044). T-03 and T-17 check this.

<!-- Source: Base (original, modified) - path-list disclosure and separate verification call appended per Change #7; stale "performs no write" replaced per review-3 note M3-8 -->

- **NFR-002 (visible writes)** Every repository write runs as its own Bash call with argv the helper planned, so every host hook sees it. The helper writes no ref, no user index, no work-tree file and no config (FR-011). T-03 checks this. Before each commit the agent prints the full path list it will commit (the pathspec file of FR-035 hides paths from the command text, not from the person). Verification is a separate helper call after the commit.

<!-- Source: Base (original, modified) - constants file renamed per Change #6 -->

- **NFR-003 (single source for safety rules)** Protected branches, forbidden flags and path rules live once, in `vcs_rules.py`. The prose copies are pinned by a parity test (T-13). Changing one rule takes one constant edit plus one prose edit, and the test fails if only one of them changes.

<!-- Source: Base (original) -->

- **NFR-004 (extension cost)** A new `/sc:git` operation needs at most a registry row, one ref section, an optional helper verb, a Usage and Options row, and tests. No existing operation's text or code changes (FR-008).
- **NFR-005 (backward compatibility)** Without `--commit-tasks`, `/sc:implement` writes the same ledger records it writes today, and every existing implement, archive and worker-contract test passes (T-16).

<!-- Source: Base (original, modified) - determinism covers the sidecar and all helper JSON; display caps never apply to S (Variant C, Section NFR-003; Variant B, Section 12 NFR-004), per Change #34 -->

- **NFR-006 (determinism)** The same ledger, sidecar and tree give byte-identical helper JSON: paths sorted, ids in source order.
- **NFR-007 (bounded output)** Helper JSON is at most 64 KiB, path lists hold at most 200 entries with a `truncated` flag, and refusal logs keep at most 40 lines. Display lists stop at 200 entries (20 in a STOP) with a total and a truncation notice; comparisons always cover the full set (FR-113). The cap never applies to S, the pathspec file (FR-035) or the `paths=` hash: `stage-plan` writes the full list to the pathspec file, and a truncated S refuses.

<!-- Source: Base (original) -->

- **NFR-008 (latency)** Each helper verb finishes in 5 seconds or less on this repository with a warm file cache. This is a target; no baseline has been measured (UNVERIFIED).

<!-- Source: Base (original, modified) - "both skills" becomes "both protocols" per Change #6 -->

- **NFR-009 (version coupling)** The helper prints `vcs_contract: "1"`, and both protocols refuse any other value (`helper-missing`). A breaking change to the helper's JSON raises the number in one release, together with both protocols.

<!-- Source: Base (original, modified) - grep check from Variant B, Section 12 NFR-001; git floor raised for --pathspec-from-file; per Change #34 -->

- **NFR-010 (installed-path rule)** No new or edited primitive names `src/<package>/...` (FR-009). Checked with the project's grep rule and T-13: `grep -rn 'src/<package>' <pkg>/{commands,skills,agents,core,hooks}` gains no new unjustified hit.
- **NFR-011 (git version)** The helper refuses `git-too-old` below the version that supports `--pathspec-from-file` for both `git add` and `git commit` (believed to be 2.25; UNVERIFIED until T-08 checks it) and below 2.23 (`git switch`); `MIN_GIT` in `vcs_rules.py` holds the higher value. The environment has 2.47.3.

<!-- Source: Variant B, Section 12 NFR-002, NFR-003, NFR-005, NFR-007 and NFR-010 (unique contribution U-015) and Variant C, Section NFR-001, NFR-003 and NFR-007 - merged per Change #34 -->

- **NFR-012 (size budgets)** `git.md` at most 150 lines; `sc-git-protocol/SKILL.md` at most 500; each `sc-git-protocol/refs/*.md` and `sc-implement-protocol/refs/commit-step.md` at most 250; `sc-implement-protocol/SKILL.md` grows by at most 15 lines.
- **NFR-013 (integrity before convenience)** Every refusal names the violated precondition and says whether HEAD, the index and the worktree changed. Nothing discards work, repairs history automatically or implies a rollback across repositories. After a success, the parent, the changed-path set and the contents are verified; a mismatch is `uncertain`, never success.
- **NFR-014 (bounded execution)** Each helper git call has a 10-second timeout; the commit call uses 600000 ms (FR-116); captured output is bounded and truncation is disclosed; a run stops rather than wait on a signing-credential or authentication prompt; a timed-out write has an uncertain effect until it is read back.
- **NFR-015 (honest trust limits)** The helper enforces local state and path rules; protocol text verifies human authority. Neither is proof against a malicious same-user process or an arbitrary trusted hook. Standard hooks stay enabled. The spec documents this boundary and makes no prompt-only guarantee.
- **NFR-016 (fail closed)** A missing helper, unparseable helper output, a missing pin or `q0-head`, or an unknown token gives a refusal, never a commit.
- **NFR-017 (no history rewrite)** Nothing in this work runs `reset`, `rebase`, `--amend`, a force push, or `update-ref` on `refs/heads/*`; each boundary adds at most one commit.
- **NFR-018 (cost when off)** A run without `--commit-tasks` adds no Bash call and no file when no `commits.md` exists; otherwise it appends one `off` run line, plus any `recovered` or `resolved` line that reconcile (FR-107) or an owner answer (FR-120) produces, runs the reconcile of FR-106 (FR-051, FR-072), and makes no commit.

## 12. Risks and mitigations

<!-- Source: Base (original, modified) - root-cause, likelihood and impact columns from Variant B, Section 10 (root causes of R1-R13, the R1 follow-up); rows 2, 3, 4, 6, 9 and 13 updated per Changes #4, #11, #15, #19, #22 and #6; rows 15-23 added (row 17 debate Round 3 ruling INV-011, row 18 INV-018, row 19 INV-029, row 20 INV-028, row 22 Variant B R2, row 23 Variant B R10); merged per Change #37; row 2 mitigation replaced per review-3 note M3-8 -->

| # | Risk | Root cause | Likelihood | Impact | Mitigation | Residual |
|---|---|---|---|---|---|---|
| 1 | Prompt rules are only advice. An agent may run `git commit -a` or `--no-verify` by hand | RC-2: no mechanical gate outside launched sessions (`launch-level-guard.sh:5-7`; no deny rule in `<dev>/settings.json`) | Medium | High | Exact argv comes from the helper (FR-061); the launch-level guard classes `--no-verify` as TAMPER in launched sessions (`:786`); T-02 and T-04 | In ordinary sessions nothing enforces this mechanically. Recommended follow-up: a deny rule for `git commit` with `--no-verify` or `-n` in every session (not built) |
| 2 | Formatter hooks (`markdownlint --fix`, `ruff-format`) rewrite files and fail the commit | `markdownlint --fix`, `ruff-format` and `mixed-line-ending --fix=lf` rewrite files (`.pre-commit-config.yaml:34-35`, `:86-91`, `:130-134`) | Low here, Medium where hooks are installed | Medium | FR-036 classes; STOP; a later flagged run retries only as FR-065 and FR-107 allow | The person must review the rewrite. Where the hooks are not installed (this clone), formatter and secret checks do not run at all (FR-036; see the unscanned-evidence residual of this risk). Accepted residual: where no `detect-secrets` hook is installed, evidence committed at a boundary enters local history unscanned. No scanner or hook installation is added; the spec never promises secret safety and never bypasses a known-secret refusal. Owner follow-up, not built here: exclude `^\.dev/tasks/.*/artifacts/` from the fixer hooks |
| 3 | A sidecar format change breaks reconcile | RC-3: the task-ledger grammar is closed, so commit state lives in a sidecar that reconcile must parse (FR-100) | Low | Medium | One regex per form, parity test T-10 | None if they land together |
| 4 | The person's edits enter a task commit | Q0 snapshots the dirty tree (`SKILL.md:123-124`) | Low | High | FR-074, FR-075, `--only`, and the outside-path snapshot (FR-110..FR-118) | An edit by another writer to a task file between Q0 and the review passes all three checks; one writer per worktree is a precondition (`refs/ledger.md:149`) |
| 5 | Inspecting submodules loads the submodule's own config, which can run a program (issue 547) | The sweep's issue-547 rationale (`probes.py:66`) | Low | High | Same `-c core.fsmonitor=false` seam as `probes.py:65`; submodule inspection only runs on a person's `/sc:git submodule` line | Whether `-c` overrides reach every submodule child process and filter is UNVERIFIED |
| 6 | `origin/HEAD` names the wrong default (here `origin/master`, while GitHub's default is `integration`) | `refs/remotes/origin/HEAD` is local, often missing, and stale once it exists (FR-032) | Medium | Low | `PROTECTED_BRANCHES` always includes `integration` and matches `LL-PROTECTED` | Other projects with differently named shared branches. Shared branches with other names are protected only by server rules, which do not stop a local commit |
| 7 | In launched sessions below `full --submit`, the guard blocks the first commit, so the run stops after the first task | The guard allows `COMMIT` only at level `full --submit` (`launch-level-guard.sh:806-808`) | Medium | Low | `blocked-by-host` stops cleanly; FR-052 keeps the flag out of launch prompts | Lost time if a person adds the flag at the wrong level |
| 8 | An automated sync may re-create `commands/sc-git.md` (see commit `ff5f73adf`) | RC-6: the legacy copy has no parity check | Low | Low | Absence test (FR-014) | Whether that automation still runs is UNVERIFIED |
| 9 | The installed skill text and the installed helper script drift apart | Cross-skill dependency: the implement protocol runs a script shipped in `sc-git-protocol` | Medium | Low | `vcs_contract` check (NFR-009) | None beyond a clear refusal |
| 10 | A batch commit covers up to 3 tasks, which is coarser than one task per commit | Batch members share one `q0-head`; a commit per member would move HEAD under a sibling | High | Low | Trailers list each task; `files=` sets stay separate in the ledger | Accepted |
| 11 | The stash stack is shared across linked worktrees | Git keeps one stash stack per repository | Low | Low | `/sc:git` never stashes (FR-004) | None |
| 12 | Fixture and table churn (S23, worker-contract scan, routing table) | RC-1 and RC-6 | High | Low | Updated in the same change (T-14); the three pinned phrases are kept (FR-017) | None |
| 13 | A CI check may require a `## Generator-Constraint Considered` section in the PR body when a gate or validator file changes (user memory note) | The check keys on gate and validator files | Medium | Low | `archive_workspace.py` no longer changes, but the check may flag the archive-gate text or the helper; add the section if it does | Which files the check covers is UNVERIFIED |
| 14 | `allowed-tools` in front matter may not restrict tools; it may only pre-approve them | The host's semantics for the field are not documented here | Medium | Low | It is not treated as a security boundary; the safety comes from NFR-002 and FR-011 | Its exact semantics in the host are UNVERIFIED |
| 15 | A hook manager's stash loses edits outside S | The common pre-commit framework saves unstaged changes as a patch outside git and checks out the tree while hooks run; under `--only` every change outside S counts as unstaged | Medium | High | Worktree snapshot and outside-S comparison (FR-110..FR-118) | Ignored files, empty directories, concurrent writers |
| 16 | A crash between the commit and its record | The terminal line is written after the commit | Low | Medium | Prepared line, pinned candidate and exact recovery predicate (FR-108, FR-130) | `uncertain` needs the owner (FR-120) |
| 17 | A stale installed protocol copy ignores the flag | Wave 0 has no unknown-option STOP (`SKILL.md:57-59`) | Medium | Low | Fails safe: the old copy commits nothing, and FR-105 stops its later tasks from being committed after the fact (FR-050) | Accepted |
| 18 | A person-added file inside the package is committed | Nothing can tell a person-added package file from evidence | Low | Medium | Package expanded to literal files; the package has one owner (FR-076) | Accepted |
| 19 | Evidence enters history unscanned | No `detect-secrets` hook is installed in this clone (§1.5) | Medium | Medium | Disclosed (row 2, §1.5) | Accepted |
| 20 | Another writer edits a task file between Q0 and the review | No check can tell that writer's edit from the task's own | Low | High | Single-writer precondition (`refs/ledger.md:149`, FR-133) | Such an edit passes all three checks (row 4) |
| 21 | Stale remote-tracking refs judge a pointer target | Remote-tracking refs are local and change only on fetch | Medium | Medium | Local-observation wording with the last-fetch time (FR-042) | Stale refs can refuse a target that is in fact published (FR-042) |
| 22 | A wrapper script hides a commit from the guard | The guard classifies a command as git only from its text (`launch-level-guard.sh:555-557`) | Low | High | Literal visible calls; the helper writes no ref and makes no commit (FR-011) | — |
| 23 | Contributors follow the foreign standards document | RC-5 | Medium | Low | D10; the §4 standards-conflict note | Until that document is fixed |

## 13. Decisions on the seed brief's open questions

<!-- Source: Base (original, modified) - D1-D4 and D8 restated under the merged design, D6 and D7 extended (D6 reasons from Variant B, Section 11 Q6), D9-D11 and the mapping line added (D10 from Variant B, Section 11 D-7), merged per Change #38 -->

Seed open questions map to decisions: Q1 → D1, Q2 → D2, Q3 → D3, Q4 → D4, Q5 → D5, Q6 → D6.

- **D1. Structure of `/sc:git`.** Decision: a command file, the `sc-git-protocol` skill with an operation registry and five refs loaded on demand, and the read-only mirrored skill script `vcs.py` (§2.3). Rejected: a command file only (testable only statically; the second consumer would copy its rules).
- **D2. How `/sc:implement` calls the commit step.** Decision: an inline step in the implement protocol (`refs/commit-step.md`; positions Q8a, R0, L0) that calls the shared helper directly and never invokes `/sc:git` or `Skill sc:git-protocol`, so there is no relay and the never-as-worker rule is untouched. The helper plans and verifies; the agent runs every write as a visible call. Settle before advance (FR-077) keeps HEAD unchanged during every task body, so the retry check and the coordinator's resume check still hold.
- **D3. Authorization switch.** Decision: the per-invocation flag `--commit-tasks`, typed by the person as a standalone token in a message that starts with `/sc:implement`, checked once per run, recorded as a `run` line with ledger offsets, revocable in plain words, needed again on resume, refused under `--unattended`. Rejected: a plan field (written by automation, the "executor-invented approval" risk, `WORKER-CONTRACT.md:57`; a managed plan is hash-pinned after its first `start`); a free-text session instruction as the switch (it cannot be parsed or tested, and it does not survive resume).
- **D4. Submodule operations and the dirty or detached cases.** Decision: `status`, `update` and `commit-pointer`, top-level submodules only. A dirty submodule refuses every write. A detached HEAD with commits no branch contains is stop-and-ask. `update` runs only when no commit is orphaned, and a clone needs the person to repeat the `.gitmodules` URL. `commit-pointer` needs a clean module and containment through the `.gitmodules` remote. Never push, never fetch on its own, no `--remote`, `foreach` or recursion (§5).
- **D5. `commands/sc-git.md`.** Decision: remove it, and add it to the absence test (FR-014). Why: nothing reads that folder, the copy is stale with a doubled prefix, and a byte copy could not carry the protocol skill, so it would be a broken half-copy.
- **D6. Residual project-management scope.** Decision: none in this work. Issue and PR status and progress are already covered by `/sc:issue`, `/sc:closeout` and the `issue-pipeline` CLI verbs (`HOW-WE-WORK.md:292`, `:296`; `WORKER-CONTRACT.md:302`). Revisit only if the owner names a specific gap. In detail: `/sc:closeout` settles a merged PR, its issue, the work report entry and the Orca task; `/sc:issue` claims and creates issues; `<cli> issue-pipeline complete` posts one result comment per run (`WORKER-CONTRACT.md:302`); progress posts are coordinator-owned outward actions (`WORKER-CONTRACT.md:244`).
- **D7 (added). `merge` in `/sc:git`.** Decision: removed. The seed brief's constraint ("`/sc:git` never pushes, merges or opens PRs") overrides the "merge operations" wording in `HOW-WE-WORK.md:293`, which is rewritten in the same change (FR-017). `--interactive` goes with it; its only example was the merge.
- **D8 (added). What a managed commit includes.** Decision: the run's own package directory, expanded to literal files (FR-076), plus the authorized product paths; all of `.dev/tasks` stays staged.
- **D9 (added). Where commit state lives.** Decision: a sidecar `commits.md` beside the ledger; the ledger grammar and archive parser are unchanged; no journal directory, no lock (§7).
- **D10 (added). Standards source.** Decision: follow the enforced gates (`.pre-commit-config.yaml`, `.github/rulesets/`, `docs/developer-guide/branch-protection.md`, the routing guide); `docs/developer-guide/git-standards-protocols.md` is non-normative for this work (the §4 standards-conflict note stays).
- **D11 (added). A boundary that cannot settle.** Decision: the owner answers `abandon` or `adopt` in chat after the STOP, and the executor records it (FR-120..FR-126).

## 14. Acceptance criteria

<!-- Source: Base (original, modified) - AC-to-test mapping kept; Observation column with runnable shell observations from Variant B, Section 13; AC-03 per Change #6; AC-05, AC-07, AC-08 and AC-12 edited and AC-16..AC-21 added per Change #36; AC-03..AC-05 observations reassigned to the criteria they test (review-3 note M3-1; AC-05 observation adapted from Variant B, Section 13 AC-09); AC-05 and AC-06 checks point at T-19 because the boundary cases moved there from T-01 -->

A behavioural test outranks a text count.

| AC | Criterion | Check | Observation |
|---|---|---|---|
| AC-01 | `git.md` has the FR-001 front matter, the FR-002 usage, the FR-003 sections with one `> Skill sc:git-protocol`, and no `## Unattended mode` | T-12 | `grep -c '^## Activation' <pkg>/commands/git.md` prints 1 and `grep -c '^## Unattended mode' <pkg>/commands/git.md` prints 0 |
| AC-02 | `sc-git-protocol` exists with `SKILL.md`, the registry, the five refs and the extension checklist; registry rows resolve | T-13; `ls <pkg>/skills/sc-git-protocol/refs` lists `safety.md`, `status.md`, `commit.md`, `branch.md`, `submodule.md` | `ls <pkg>/skills/sc-git-protocol/refs` lists the five refs |
| AC-03 | `uv run --no-project python <pkg>/skills/sc-git-protocol/scripts/vcs.py --help` lists the seven verbs; the helper issues only allow-listed argv | T-03; running `uv run --no-project python <pkg>/skills/sc-git-protocol/scripts/vcs.py --help` | `uv run --no-project python <pkg>/skills/sc-git-protocol/scripts/vcs.py --help` lists the seven verbs |
| AC-04 | The source, the plugin mirror and the dev copy are in sync, and `commands/sc-git.md` is gone | `make verify-sync` exits 0; `tests/commands/test_routing_plugin_parity.py` includes `git`; absence test | `cmp <pkg>/commands/git.md <plugin>/commands/git.md` and `diff -r -x __pycache__ <pkg>/skills/sc-git-protocol <plugin>/skills/sc-git-protocol` print nothing; `make verify-sync` exits 0; `git ls-files commands/sc-git.md` prints nothing and `git ls-files commands/ \| wc -l` prints 20 |
| AC-05 | `/sc:implement --commit-tasks` commits between tasks only when no task is open, with exactly the planned paths plus the managed package directory, and writes `commit sha=` lines in `commits.md` | T-01, T-02, T-09, T-19 | In a fixture repository, two tasks run with `--commit-tasks` give two new commits and two `commit sha=` lines in `commits.md` |
| AC-06 | No commit inside a parallel batch; one commit after every member has `complete` | T-19 (batch case) | — |
| AC-07 | A refused or failed hook gives one FR-036 class, `E-COMMIT-REFUSED`, HEAD unchanged, no `--no-verify` or `--amend` | T-04 | — |
| AC-08 | Without the flag and with no `commits.md`, behavior is unchanged and no `commits.md` is created; with one, the run appends one `off` run line, plus any `recovered` or `resolved` line that reconcile (FR-107) or an owner answer (FR-120) produces, reconciles and makes no commit | T-16, T-21 | — |
| AC-09 | `--commit-tasks` together with `--unattended` gives `E-COMMIT-PRECONDITION reason=unattended`, and `/sc:git` stays never-as-worker | T-09; `tests/skills/test_worker_contract.py` passes with `NEVER_AS_WORKER` unchanged | — |
| AC-10 | The submodule `status`, `update` and `commit-pointer` operations classify and refuse as specified | T-07 | — |
| AC-11 | No local branch deletion outside `scripts/worktree_cleanup.py`, and no remote branch deletion anywhere | T-17; `tests/worktree_cleanup/` passes unchanged | `git diff --quiet origin/integration -- scripts/worktree_cleanup.py <pkg>/commands/worktrees.md <pkg>/hooks/scripts/launch-level-guard.sh` exits 0 |
| AC-12 | Managed archiving accepts a package with `commits.md`, and refuses `E-ARCHIVE-BLOCKED reason=unsettled-boundary` while a boundary is unsettled | T-11 | — |
| AC-13 | The routing guide row, fixture S23 and the worker-contract scan are updated, and their tests pass | T-14; `uv run pytest tests/core tests/recommend tests/skills/test_worker_contract.py` | `cmp <pkg>/core/HOW-WE-WORK.md <plugin>/skills/sc-recommend/refs/HOW-WE-WORK.md` prints nothing |
| AC-14 | No new or edited primitive names a `src/<package>/` path | T-13; the project's grep rule over commands, skills, agents, core and hooks | — |
| AC-15 | The full gate passes | T-18 | — |
| AC-16 | A crash at any of the five points never produces a second commit for a key | T-22, T-19 | — |
| AC-17 | Edits outside S are recoverable byte for byte after an interrupted hook | T-20 | — |
| AC-18 | Every unsettled state offers `abandon` in flagged and unflagged runs | T-21 | — |
| AC-19 | No task completed outside an `on` segment is ever committed | T-19 | — |
| AC-20 | Each seed constraint in §1.8 is met | The checks each §1.8 row lists pass | — |
| AC-21 | No new or edited primitive names `src/<package>/`. There is no vendor-name scan of primitives, because primitives must name the installed paths and the `refs/<package>/implement/` pins | T-13 | The NFR-010 `grep` observation gains no new unjustified hit |
