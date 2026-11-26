# Requirements Specification: Modular `/sc:git`, Authorized Between-Task Commits in `/sc:implement`, and Submodule Operations (issue 326)

Persona: architect. Priority: maintainability and extension scaffolding. Date: 2026-11-26.
Sources: `seed-brief.md`, `enrichment/codebase-context.md`, `enrichment/research-deep.md` (same brainstorm folder), `.dev/issues/326/issue-summary.md`, `.dev/issues/326/analysis/analyze-git.md`, and a read-only check of the repository in this worktree.

## 1. Overview and scope

### 1.1 Notation

Some real paths contain the package name. This document writes them with the placeholders below. Each placeholder stands for exactly one real location that was checked in this worktree.

| Placeholder | Meaning (verified) |
|---|---|
| `<package>` | The single package directory name under `src/` (`ls src/` lists one entry), and the plugin folder name under `plugins/` |
| `<pkg>` | `src/<package>/`, the source of truth for commands, skills, agents, core files, hooks and the CLI |
| `<plugin>` | `plugins/<package>/`, the plugin mirror. The plugin build script copies from it (`scripts/build_<package>_plugin.py:16`, `PLUGIN_SRC`) |
| `<cli>` | The package's console command (`pyproject.toml:70-71`, `[project.scripts]`). Installed primitives already call it, for example `<cli> review safety-scan` |
| `<home>` | The per-user agent-host configuration directory that `<cli> install` writes to. It holds installed copies such as `<home>/commands/sc/`, `<home>/skills/`, `<home>/WORKER-CONTRACT.md` and `<home>/HOW-WE-WORK.md` |
| `<dev>` | The project-local, gitignored agent-host directory that `make sync-dev` fills (`Makefile:109-163`). Its only tracked file is `settings.json` (`.gitignore:127-128`) |
| `<Product>` | The capitalized product name used as a prefix in one developer-guide file name |

### 1.2 Problem

`/sc:git` (`<pkg>/commands/git.md`, 91 lines) is a prose command. It has no Options table, no STOP rules, no Activation, no submodule text and no backing skill. Its usage line is `/sc:git [operation] [args] [--smart-commit] [--interactive]` (line 22). It still shows a `merge ... --interactive` example (lines 72-77).

`/sc:implement` lists "Auto-commit, open PRs, or release" as a Will Not (`<pkg>/commands/implement.md:100`). Because of that, a long plan lands as one uncommitted change.

### 1.3 In scope

1. A modular `/sc:git`: a command file that follows the developer guide, a protocol skill with one ref per operation group, and a small read-only helper in the package CLI. The plugin mirror and the dev copy are kept in sync, and the legacy root copy is retired.
2. An explicitly authorized local commit between tasks in `/sc:implement`. It never runs inside a task or inside a parallel batch, and it reports a refused hook instead of bypassing it.
3. Defined submodule operations in `/sc:git`: status, update, and a pointer commit, under the same authorization rules.
4. Branch cleanup by reuse only. `/sc:git` routes to `/sc:worktrees`, which runs `scripts/worktree_cleanup.py` from PR 711.

### 1.4 Explicitly out of scope (decided)

- A central relay through which every command calls `/sc:git`. Commands cannot call another session, and `/sc:git` stays on the never-as-worker list (`<pkg>/core/WORKER-CONTRACT.md:23`).
- Push, fetch, pull, merge, rebase, PR creation and PR review. PRs stay with `/sc:pr-submit`, which is also the only push path here (`<pkg>/core/WORKER-CONTRACT.md:245`).
- Remote branch deletion, anywhere.
- A second implementation of local branch cleanup. `_remove_branch` in `scripts/worktree_cleanup.py:2636-2647` stays the only one.
- Any change to the level table in `<pkg>/core/HOW-WE-WORK.md`. That table is copied into the core instructions file, so a change there would spread to every install.
- Fixing `docs/developer-guide/git-standards-protocols.md`. Section 6 explains why it conflicts with the hook this repository enforces.
- Nested submodules (submodules of submodules), `git submodule foreach`, and `update --remote`.
- New project-management workflows. Decision D6 explains why.

### 1.5 Baseline facts (verified in this worktree)

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
| Commit messages are checked by `conventional-pre-commit` at the `commit-msg` stage. `markdownlint --fix` and `ruff-format` can rewrite files during a commit | `.pre-commit-config.yaml:78-84`, `:86-91`, `:130-134` |
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

## 2. Structure of the refactored `/sc:git`

The design has three layers. The command file parses and stops. The protocol skill holds the behavior, with one ref loaded per operation. The package helper is read-only code that computes facts and plans: it decides, and the agent acts. Every write to the repository is a visible shell command run by the agent, never run inside the helper. That way the host's hooks (the launch-level guard, deny rules and pre-commit hooks) always see the real `git add` and `git commit`.

### 2.1 Command file `<pkg>/commands/git.md` (rewritten)

- **FR-001** The front matter has `name: git`, a one-line `description`, `category: version-control` and `complexity: moderate` (the values the developer guide lists in §3.1, `docs/developer-guide/<Product>-Developer-Guide-Commands-Skills-Agents.md:270-284`), `mcp-servers: []`, `personas: []`, and an `argument-hint` that lists exactly the operations in FR-002.
- **FR-002** The Usage block lists exactly these forms, and no others:
  - `/sc:git status`
  - `/sc:git add <path>...`
  - `/sc:git commit [<path>...] (--message "<text>" | --smart-commit)`
  - `/sc:git branch [list | create <name> | switch <name> | cleanup]`
  - `/sc:git submodule [status | update <path> | commit-pointer <path> (--message "<text>" | --smart-commit)]`

  `--message` is new. `--smart-commit` is kept, because routing fixture S23 depends on it. `--interactive` and the `merge` example are removed.
- **FR-003** The body has these sections, in this order: `## Triggers`, `## Usage`, `## Options`, `## STOP rules (checked before Activation)`, `## Behavioral Flow` (parse, STOP, hand off, print), `## Activation` (contains exactly one line `> Skill sc:git-protocol` and names `<home>/skills/sc-git-protocol/SKILL.md`), `## Examples`, `## Outputs`, `## Boundaries` and `## Related Commands`. It has no `## Unattended mode` section.
- **FR-004** STOP rules print the usage block and run nothing in these cases: no operation; an unknown operation; `push`, `pull`, `fetch`, `merge`, `rebase`, `reset`, `clean`, `stash`, `tag` or `pr` as the operation (the message names `/sc:pr-submit` for push and PR, and says merge is not a `/sc:git` operation); `commit` or `commit-pointer` with neither `--message` nor `--smart-commit`, or with both; `create` or `switch` without a name; any token in the forbidden-flag list (FR-030); `--unattended` (the message says `/sc:git` never runs as a worker); and not inside a git work tree.
- **FR-005** Boundaries **Will Not** says, in plain words: push, fetch, pull, merge, rebase, open or edit a PR, delete any branch (local or remote), force anything, stash, rewrite history (`--amend`, reset of a published commit), or stage a `<dev>/` path other than `settings.json`.

### 2.2 Protocol skill `<pkg>/skills/sc-git-protocol/` (new)

- **FR-006** `SKILL.md` has the front matter `name: sc:git-protocol`, a `description`, and `allowed-tools: Read, Write, Bash`. It includes an **operation registry** table. Each row has: operation, class (`read`, `index`, `local-history`, `working-tree`), the authorizing message prefix (FR-020), the ref file, the helper verb, and the STOP and refusal tokens. The registry is the single place that lists what `/sc:git` can do.
- **FR-007** Refs are loaded on demand, one per operation group (developer guide §5.6, the refs pattern):
  - `refs/safety.md`: forbidden operations and flags, path rules, protected branches, hook-refusal handling and the message format. It applies to every write.
  - `refs/status.md`: the `status` and `branch list` reports.
  - `refs/commit.md`: `add` and `commit`.
  - `refs/branch.md`: `create`, `switch` and `cleanup` (routing only).
  - `refs/submodule.md`: `submodule status`, `update` and `commit-pointer`.
- **FR-008 (extension scaffolding)** `SKILL.md` ends with an "Adding an operation" checklist: (1) a registry row; (2) a ref file or a section in an existing ref; (3) a helper verb, only if the operation needs computed facts; (4) a Usage and Options row in `git.md`; (5) tests per §9. A static test asserts that every registry row names an existing ref file and every helper verb it names exists in `<cli> vcs --help`.
- **FR-009** No file in the skill or the command names a `src/<package>/...` path. Cross-primitive references use `<home>/...` with the `<dev>/...` copy as the fallback (project rule "Never Hardcode ... Paths in Installed Primitives"; `tests/skills/test_primitive_dual_surface_lookup.py`).

### 2.3 Read-only helper: `<cli> vcs` (new package code)

Location: `<pkg>/cli/vcs/` (`__init__.py` exporting `vcs_group`, plus `commands.py`, `plan.py`, `submodules.py` and `rules.py`). It is registered in `<pkg>/cli/main.py` the same way as the `review` and `sweep` groups (`main.py:585-592`). The group name `vcs` is unused today (checked against the `add_command` and `@main.command` list). It does not contain the words "git", "commit" or "push", so the launch-level guard's text classifier (`launch-level-guard.sh:135`) does not read a read-only planning call as a commit.

- **FR-010** The verbs, all read-only:
  - `vcs preflight [--cwd <dir>]` prints JSON with `top`, `branch`, `detached`, `protected` (boolean plus a reason), `operation_in_progress` (merge, rebase, cherry-pick, revert or bisect marker), `index_lock`, `hooks_path`, `submodule_recurse`, `push_recurse_submodules`, `dirty` (paths outside `.dev/`, sorted, capped at 200, with `truncated`) and `vcs_contract: "1"`.
  - `vcs stage-plan (--path <p>... | --ledger <file> --run-dir <dir> [--package <dir>]) [--cwd <dir>]` prints JSON with `status` (`ok`, `nothing` or `refused`), `reason`, `tasks` (ledger mode), `add_argv`, `commit_argv`, `commit_paths`, `skipped` (`[{path, why}]`) and `message_path`.
  - `vcs check-message --file <f> [--implement]` prints `ok` or `refused: <rule>`.
  - `vcs submodules [--cwd <dir>]` prints the JSON rows of FR-040.
- **FR-011** The helper calls git only through one runner. That runner adds the prefix `git --no-optional-locks -c core.fsmonitor=false` (the same seam as `probes.py:65`) and allows only read verbs (`rev-parse`, `symbolic-ref`, `status`, `diff`, `ls-files`, `config --get`, `submodule status`, `for-each-ref`, `cat-file`, `merge-base --is-ancestor`, `branch --show-current`, `branch -r --contains`). Any other argv raises an error before it executes.
- **FR-012** Exit codes: 0 when JSON was printed, whatever the `status`; 64 for a usage error; 69 when a lookup failed. These match the codes `/sc:worktrees` uses (`<pkg>/commands/worktrees.md:55`).
- **FR-013** Safety constants are defined once, in `rules.py`:
  - `PROTECTED_BRANCHES = ("master", "main", "integration")`, the same set as `LL-PROTECTED` (`launch-level-guard.sh:59`), plus the target of `refs/remotes/origin/HEAD` when it resolves;
  - `FORBIDDEN_FLAGS` (FR-030);
  - `DEV_MIRROR_ALLOW = ("settings.json",)`;
  - `MIN_GIT = (2, 23)` (`git switch`).

  The refs in §2.2 repeat these lists for the agent, and a parity test asserts the prose and the constants match.

### 2.4 Fate of `commands/sc-git.md`

- **FR-014** Delete `commands/sc-git.md`, and add it to the absence test (the `_RETIRED` list in `tests/docs/test_retired_docs_absent.py:10-34` is the precedent). Leave the other `commands/sc-*.md` files alone (scope). See decision D5.

### 2.5 Plugin mirror and sync steps

- **FR-015** Edit `<pkg>` first. Then copy byte-for-byte:
  - `<pkg>/commands/git.md` to `<plugin>/commands/git.md`;
  - `<pkg>/skills/sc-git-protocol/**` to `<plugin>/skills/sc-git-protocol/**`;
  - `<pkg>/commands/implement.md` to `<plugin>/commands/implement.md`;
  - `<pkg>/skills/sc-implement-protocol/**` to `<plugin>/skills/sc-implement-protocol/**`;
  - `<pkg>/core/HOW-WE-WORK.md` to `<plugin>/skills/sc-recommend/refs/HOW-WE-WORK.md`.

  Add `git.md` to the mirrored list in `<pkg>/commands/README.md:9`, and add `"git"` to the parametrization in `tests/commands/test_routing_plugin_parity.py:41`.
- **FR-016** Run `make sync-dev`, then `make verify-sync`. The verify step must exit 0. `<dev>/` copies are never staged. The only `<dev>/` path that may be staged is `settings.json`, and this work does not change it.
- **FR-017** Update the `/sc:git` row in the Other commands table of `<pkg>/core/HOW-WE-WORK.md:293`. The new row must keep the three phrases that fixture S23 pins: "Status-only stays inspection", "a commit needs authorization" and "Do not append push, merge or PR creation". It removes "merge operations", names `/sc:worktrees` for cleanup, and names only flags that exist in `git.md`, because `tests/core/test_how_we_work_routing_table.py` checks the names the table uses.

## 3. Authorization model

The person's own typed line is the only thing that authorizes a write. No plan field, brief line, other command or agent message can authorize one (`WORKER-CONTRACT.md:57`, "executor-invented approval").

| Operation | Class | Authorized by | Extra guard |
|---|---|---|---|
| `status`, `branch list`, `branch cleanup`, `submodule status` | read | Any `/sc:git` invocation | None |
| `add <path>...` | index | The person's current message starts with `/sc:git add` | Path rules (FR-031) |
| `commit` | local-history | The person's current message starts with `/sc:git commit` | Preflight (FR-032) |
| `branch create`, `branch switch` | working-tree | The person's current message starts with `/sc:git branch` | Clean tree, submodules included (FR-034) |
| `submodule update <path>` | working-tree | The person's current message starts with `/sc:git submodule update` | Submodule state rules (FR-041) |
| `submodule commit-pointer <path>` | local-history | The person's current message starts with `/sc:git submodule commit-pointer` | Submodule state rules plus preflight |
| Between-task commit in `/sc:implement` | local-history | `--commit-tasks` on the `/sc:implement` invocation line | §4 |
| Push, fetch, pull, merge, rebase, reset, clean, stash, tag, any branch deletion, any force | forbidden | Nothing | STOP (FR-004) |

- **FR-020** A write operation runs only when the person's current message starts with the authorizing prefix in the table. This follows the precedent at `WORKER-CONTRACT.md:346`. When `/sc:git` is reached any other way (for example, an agent decides to run it, or another skill suggests it), every write operation is downgraded to a dry run. A dry run prints the plan and the exact commands, writes nothing, and says why.
- **FR-021** One authorizing line authorizes one operation. A follow-up write needs a new typed line.
- **FR-022** No write operation asks for a second confirmation, because none of them is destructive: nothing deletes, overwrites unsaved work, or rewrites history. After every write, `/sc:git` prints the new HEAD and its parent SHA. After a commit it also prints `git reset --soft <parent>` as the way to undo it, with a note that the undo keeps the changes staged.

## 4. Between-task commit behavior in `/sc:implement`

### 4.1 Opt-in switch

- **FR-050** Add a new flag, `--commit-tasks`, to `/sc:implement`: to the Options table, the argument-hint (`implement.md:7`) and the Wave 0 option list (`SKILL.md:57`). It is off by default. It counts only as a standalone token in the option prefix, following the same rule as the other options at `SKILL.md:57-59`. After the source starts, the same text is part of the prompt.
- **FR-051** The flag is per invocation. A resume without the flag makes no commits and writes no `COMMIT:` line.
- **FR-052** No primitive other than `implement.md`, `sc-implement-protocol` and `HOW-WE-WORK.md` may contain the string `--commit-tasks`. Specifically, no `/sc:workflow` handoff, `/sc:issue` launch prompt or `/sc:task` text may contain it. A static test enforces this.
- **FR-053** Replace the Will Not at `implement.md:100` with "Commit without `--commit-tasks` on the invocation line, push, open PRs, or release (a managed archive is not any of these)".

### 4.2 Wave 0 preflight

- **FR-054** When `--commit-tasks` is present, a new Wave 0 step runs after step 5 (resolve the ledger path) and before step 6 (open or create the ledger). It runs `<cli> vcs preflight` and reads any existing ledger without writing to it. It STOPs with `E-COMMIT-PRECONDITION reason=<token>` (no product writes, no ledger writes) on any of these:
  - `unattended`: `--unattended` is present;
  - `helper-missing`: `<cli> vcs` cannot be run, or `vcs_contract` is not `"1"`;
  - `not-a-repo`;
  - `detached-head`;
  - `protected-branch`;
  - `operation-in-progress`;
  - `index-locked`;
  - `dirty`: one or more dirty paths outside `.dev/` that are not named in the `files=` field of any verdict line already in the ledger. The STOP prints up to 20 of them.
- **FR-055** When the preflight passes and the ledger has no `COMMIT: on` line, Wave 0 step 6 appends `COMMIT: on` after the header and before the next `start` line. The line is written once per ledger.

### 4.3 When the commit step runs

- **FR-056** Define these terms over the ledger:
  - A task is **open** when its latest `start` line has no later `complete` verdict line for that task.
  - A task is **pending** when (a) its latest verdict line is `complete`, (b) that line comes after the first `COMMIT: on` line, and (c) no later `COMMIT: sha=` or `COMMIT: none` line lists it.
  - The commit step runs when, and only when, the flag is present, the pending set is not empty, and no task is open.
- **FR-057** Positions in the loop:
  - **Q8a**, after Q7 has flushed a `complete` line and before Q8 starts the next task's Q0;
  - **R0**, at the start of a resume, before task selection (`refs/ledger.md:124-135`);
  - **L0**, after the last task's `complete` line and before the whole-list review or the managed FINAL.

  At every position the "no task is open" condition is rechecked from the ledger on disk.
- **FR-058** Parallel batches: because every member's `start` line is written before any member runs (`SKILL.md:110`, rule (a)), the "no task is open" condition holds only after every member has `complete`. The batch becomes one commit that lists every member. If a member halts, no commit is made. After the resume completes the halted task (it runs alone, rule (c)), the pending set is the completed members plus that task, and they become one commit.
- **FR-059** The commit step never runs while any task has a `halt` or `blocked` record that is its latest record. So HEAD equals `q0-head` for every open or halted task: the retry check 3 (`refs/retry.md:41`) and the Ruling resume condition (6) (`WORKER-CONTRACT.md:280`) still hold.

### 4.4 How the commit is made

- **FR-060** The step runs `<cli> vcs stage-plan --ledger <ledger> --run-dir <run dir> [--package <pkg dir>]`. It acts only on `status` and the printed argv:
  - `nothing`: append `COMMIT: none tasks=<ids> reason=no-changes` and continue;
  - `refused`: append `COMMIT: refused tasks=<ids> reason=<reason>` and STOP `E-COMMIT-REFUSED`;
  - `ok`: continue with FR-061.
- **FR-061** On `ok`, the executor:
  1. Writes the message to `message_path` with the Write tool. For a legacy run that is `<run dir>/commit-msg-<n>.txt`. For a managed run it is `<pkg>/artifacts/commit-msg-<n>.txt`.
  2. Runs `<cli> vcs check-message --file <message_path> --implement`. A refusal is fixed by rewriting the message once; a second refusal ends with `reason=message`.
  3. Runs `add_argv` as one Bash call. Its shape is `git add -- <paths>`, plus `git add -- .dev/tasks` when that directory exists and is not ignored.
  4. Runs `commit_argv` as one Bash call. Its shape is `git commit --only -F <message_path> -- <commit_paths>`.
  5. Reads `git rev-parse HEAD`.
  6. Appends `COMMIT: sha=<40-hex> tasks=<ids>`.

  The executor never edits the argv.
- **FR-062** Path rules inside `stage-plan`:
  - `commit_paths` is the sorted union of the `files=` fields on the pending tasks' latest `complete` lines.
  - For a managed run, it also includes the package directory. It does not include all of `.dev/tasks`, so other packages in flight stay out of the commit. They stay staged by step 3.
  - Excluded, each listed in `skipped` with its reason: paths under `.dev/implement/` (`refs/ledger.md:3`); gitignored paths; paths outside the repository; gitlinks (mode `160000`, matching the revert exclusion at `refs/retry.md:212`); and `<dev>/` paths other than `settings.json`.
  - If nothing remains, the result is `nothing`.
- **FR-063** `add_argv` and `commit_argv` never contain `-A`, `--all`, `.`, `-a`, `--amend`, `--no-verify`, `-n`, `--force`, `-f`, `--allow-empty`, `-c` or `--no-edit`. A test asserts this over every planning case.

### 4.5 Hook refusal

- **FR-064** Refusals are classified with these tokens:
  - `blocked-by-host`: a host PreToolUse hook refused the Bash call. An example is `LL-COMMIT` in a launched session below `full --submit`.
  - `commit-failed`: `git commit` exited non-zero and HEAD did not move. This includes `pre-commit` or `commit-msg` hook failures and formatter hooks that rewrote files.

  Both are written as `COMMIT: refused ... reason=<token>`, with the first 40 lines of output saved to `<run dir>/commit-refused-<n>.log` (managed: `<pkg>/artifacts/`). Both end the run with `E-COMMIT-REFUSED`. The executor never retries with `--no-verify`, never amends, and never edits a hook or `core.hooksPath`.
- **FR-065** On a resume after `E-COMMIT-REFUSED`, R0 plans again from the current tree, so any hook rewrites in the same paths are included. A refusal line does not remove tasks from the pending set.

### 4.6 Message format

- **FR-066** The subject is `<type>[(<scope>)][!]: <summary>`, at most 72 characters. `<type>` is one of `feat`, `fix`, `refactor`, `docs`, `test`, `build`, `ci`, `chore`, `perf` or `style`. The second line is blank. The body has one line per task: `T<id>: <task title>`. The trailer block has one `Implement-Task: T<id> (<verdict>)` line per task and one `Implement-Ledger: <repo-relative ledger path>` line. The helper adds no attribution trailers; those follow the session's own settings. `check-message --implement` enforces all of this.
- **FR-067** A task completed by a Ruling (a non-compliant verdict with operator acceptance) is committed like any other task. Its trailer carries the non-compliant verdict, so the acceptance is visible in history. A Ruling never authorizes a commit (`refs/ledger.md:239`); only `--commit-tasks` does.

### 4.7 Ledger, STOP table and archive helper changes

- **FR-068** `refs/ledger.md` adds a `## Commit records` section with four forms and one regex: `COMMIT: on`; `COMMIT: sha=<40-hex> tasks=<ids>`; `COMMIT: none tasks=<ids> reason=no-changes`; `COMMIT: refused tasks=<ids> reason=<token>`. The reason is the open class `[a-z][a-z-]*`, following the rationale at `refs/ledger.md:116`. The record list at `refs/ledger.md:127` gains `COMMIT`.
- **FR-069** `archive_workspace.py` adds `_COMMIT` to the parser tuple at lines 187-197 and checks every listed id against the plan's tasks, as it already does at line 362. A managed package whose ledger has `COMMIT:` lines archives exactly as it does today.
- **FR-070** The STOP table in `SKILL.md` gains `E-COMMIT-PRECONDITION` (product writes: no; ledger: no) and `E-COMMIT-REFUSED` (product writes: no new task; ledger: the `COMMIT: refused` line). The sentence at `SKILL.md:51` is revised to name both codes.
- **FR-071** The final summary (`SKILL.md`, "Done") prints one line per `COMMIT: sha=` record for this ledger: `<short sha> <tasks> <subject>`.
- **FR-072** The new ref `refs/commit.md` in `sc-implement-protocol` holds §4.3-§4.6. It is loaded only when `--commit-tasks` is present, the same way `refs/retry.md` is loaded only when needed (`SKILL.md:17`). The implement protocol never invokes `/sc:git` or `Skill sc:git-protocol`.

## 5. Submodule operations in `/sc:git`

- **FR-040** `submodule status` reports one row per top-level submodule, built from `git submodule status` and `git status --porcelain=v2 --ignore-submodules=none` (the `S<c><m><u>` field). Each row has: path, recorded SHA, checked-out SHA, branch (or `detached`), and a state from this closed list:
  - `uninitialized` (`-`);
  - `in-sync`;
  - `pointer-moved` (`+`, or `c` = `C`, with no `M` or `U`);
  - `dirty-tracked` (`m` = `M`);
  - `dirty-untracked` (`u` = `U`);
  - `detached-new-commits` (detached, HEAD differs from the recorded SHA, and HEAD is not contained in any local or remote-tracking branch of the submodule);
  - `conflict` (`U` prefix);
  - `nested-not-inspected`.

  The report also prints the values of `submodule.recurse` and `push.recurseSubmodules`. When `submodule.recurse` is true, it warns that a later plain `git push` may push submodules as a side effect.
- **FR-041** `submodule update <path>`:
  - Runs `git submodule update --init -- <path>` only when the state is `uninitialized`, or `pointer-moved` with no `M` or `U`.
  - Refuses with these tokens: `submodule-dirty` (`dirty-tracked`, `dirty-untracked`); `detached-new-commits` (stop and ask, and print `git -C <path> switch -c <name>` as the way to keep the commits); `conflict`; `in-sync` (nothing to do).
  - Never passes `--remote`, `--force`, `--checkout` overrides, `--merge`, `--rebase` or `--recursive`.
- **FR-042** `submodule commit-pointer <path>`:
  - Requires the state `pointer-moved` and a submodule HEAD on a branch.
  - Refuses with `submodule-dirty` ("commit inside the submodule first; run `/sc:git commit` from inside it"), `detached-new-commits`, `uninitialized` and `conflict`.
  - Before committing, warns (read-only, no fetch) when `git -C <path> branch -r --contains <sha>` is empty: "push the submodule before pushing this branch". `/sc:git` never pushes either repository.
  - Commits with the same planned argv shape as FR-061: `git add -- <path>` and then `git commit --only -F <msg> -- <path>`.
- **FR-043** A commit inside a submodule is an ordinary `/sc:git commit` run from inside the submodule's work tree. The detached-HEAD refusal in FR-032 forces a branch first, which is the safe order the research describes.

## 6. Commit rules shared by `/sc:git commit` and the implement step

- **FR-030** The forbidden-flag list: `--no-verify`, `-n` (on commit), `--amend`, `--force`, `-f`, `-D`, `--delete`, `-A`, `--all`, `.` (as a pathspec), `-a`, `--allow-empty`, `--no-edit`, `--remote`, `--recurse-submodules=on-demand`, `--discard-changes`.
- **FR-031** Path rules for `add` and `commit <path>...` are the same as FR-062, without the ledger parts. A `<dev>/` path other than `settings.json` is refused. A gitlink is refused with a pointer to `submodule commit-pointer`.
- **FR-032** Preflight for every local-history write: refuse on `detached-head`, `protected-branch` (FR-013), `operation-in-progress`, `index-locked`, or a git version below `MIN_GIT`.
- **FR-033** `/sc:git commit` with paths commits the working-tree content of exactly those paths (`--only`), so the person's other staged changes stay staged. Without paths, it commits the index as staged. It refuses when the index holds a `<dev>/` path other than `settings.json`. Hook refusal follows FR-064, but without ledger lines. The message comes from `--message`, or from `--smart-commit`, which drafts it from `git diff --cached` in Conventional Commits form. In both cases it is checked by `check-message` (without `--implement`) and passed with `-F`.
- **FR-034** `branch create <name>` runs `git switch -c <name>`, and refuses a name in `PROTECTED_BRANCHES` or a name that already exists. `branch switch <name>` runs `git switch <name>`, and refuses when `git status --porcelain=v2 --ignore-submodules=none` is not empty. Neither ever uses `--force` or `--discard-changes`. If git refuses because the branch is checked out in another worktree, the refusal is shown as is.

**Standards conflict (recorded, not fixed here).** `docs/developer-guide/git-standards-protocols.md:430-439` asks for a `[GFXA-XXX] ...` subject. That file is a template from another project: its front matter id is `GFXAI-GIT-STANDARDS-PROTOCOLS` and its status is "To Do" (lines 1-9). This repository enforces Conventional Commits with `conventional-pre-commit` (`.pre-commit-config.yaml:78-84`). This spec follows the enforced hook.

## 7. Branch cleanup reuse

- **FR-080** `/sc:git branch cleanup` is a read-only routing operation. When the current checkout has `scripts/worktree_cleanup.py` at its top level, it prints the exact lines `/sc:worktrees list` and `/sc:worktrees prune` and stops, running neither. Otherwise it prints the same "runs only inside a checkout of this repository" notice as `worktrees.md:45`.
- **FR-081** No new code anywhere runs `git branch -d`, `git branch -D`, `git branch --delete`, `git push --delete` or `git push <remote> :<branch>`. A repository-wide static test over `<pkg>/cli/vcs/`, `sc-git-protocol` and `git.md` asserts this.
- **FR-082** Local branches without a worktree are not cleaned by any command. That gap is recorded as accepted residual scope. It can be revisited only if the owner names it. It is not built here.

## 8. Interaction with the worker contract and unattended mode

- **FR-090** `/sc:git` stays on the never-as-worker list, unchanged (`WORKER-CONTRACT.md:23`; `NEVER_AS_WORKER` in `tests/skills/test_worker_contract.py:474-485`). `git.md` gets no `## Unattended mode` section, so the brief guard still refuses it under case 3.
- **FR-091** Rewrite the K3 sentence at `WORKER-CONTRACT.md:42`. The new sentence says that per-task commits are delivered as `/sc:implement --commit-tasks`, that they run only in an ordinary person session, that they fall only between a task's `complete` line and the next task's start and never inside a parallel batch, and that `--commit-tasks` is refused under `--unattended` (`E-COMMIT-PRECONDITION reason=unattended`). The worker's end-of-Task commit (lines 42-43) does not change.
- **FR-092** When the P4 conversion adds `## Unattended mode` to `implement.md`, that section lists `--commit-tasks` as refused before any work. It writes `worker_status: failed` with the flag in `reason` (WC-4).
- **FR-093** In launched sessions, the launch-level guard decides. At level `full --submit`, commits are allowed. At other levels, the commit Bash call is refused (`LL-COMMIT`) and maps to `reason=blocked-by-host` (FR-064). Nothing reads the guard's store or probes the launch level, because reading the store would be TAMPER (`launch-level-guard.sh:777`).
- **FR-094** The coordinator's own commit rules (`WORKER-CONTRACT.md:247`) do not change. The pending-set rule agrees with the coordinator's freeze rule: no commit while a plan is halted (§4.3).

## 9. Test obligations

All tests run with `uv run pytest`. The new ones are proposed under `tests/vcs/` unless another file is named.

| ID | Test | What it proves |
|---|---|---|
| T-01 | `tests/vcs/test_stage_plan.py` on temporary git repos | Pending set: sequential tasks; a 3-member batch gives one commit; a halt gives no commit; a resume after a refusal gives a retry; tasks completed before `COMMIT: on` are excluded; open task means no step. Paths: ignored, `.dev/implement/`, gitlink, outside the repo and `<dev>/` are skipped; the managed package directory is included. Result `nothing` when nothing changed |
| T-02 | `tests/vcs/test_argv_shape.py` | `add_argv` and `commit_argv` have the FR-061 shape and never contain an FR-063 token |
| T-03 | `tests/vcs/test_helper_readonly.py` with a recording runner | Every git argv the helper builds is in the FR-011 allow-list, with the `--no-optional-locks -c core.fsmonitor=false` prefix |
| T-04 | `tests/vcs/test_hook_refusal.py` | A failing `pre-commit` hook, and a hook that rewrites a file and exits 1, in a temporary repo: running the planned argv leaves HEAD unchanged; the documented record is `COMMIT: refused ... reason=commit-failed`; re-planning includes the rewritten content; no argv has `--no-verify` |
| T-05 | `tests/vcs/test_only_semantics.py` | After `git add -- .dev/tasks` and `git commit --only -- <paths>`, other staged entries are still staged and not in the commit. This test checks the FR-033 and FR-062 assumption instead of trusting it |
| T-06 | `tests/vcs/test_check_message.py` | Subject regex, 72-character limit, blank line 2, implement trailers. Every allowed type is accepted by the `conventional-pre-commit` default type list (UNVERIFIED until this test runs the pinned hook, `rev: v3.0.0`) |
| T-07 | `tests/vcs/test_submodules.py`, with a local superproject and a `file://` submodule | Each FR-040 state is classified correctly; `update` and `commit-pointer` refuse as in FR-041 and FR-042; the `submodule.recurse` warning appears. Git 2.38.1 and later blocks `file://` submodules unless `protocol.file.allow=always` is set; the test sets it only in its own temporary repos (UNVERIFIED on the CI image) |
| T-08 | `tests/vcs/test_preflight.py` | Detached HEAD, `master`, `main`, `integration` and the `origin/HEAD` target are refused; merge-in-progress and `index.lock` are reported |
| T-09 | `tests/skills/test_implement_commit_rules.py` (static) | `implement.md` Options row and Will Not text (FR-050, FR-053); STOP rows and the revised closed-list sentence (FR-070); `refs/commit.md` exists and is loaded only with the flag; the protocol never invokes `/sc:git` (FR-072) |
| T-10 | Ledger parity test | The ledger regex documented in `refs/ledger.md`, the helper's parser and `archive_workspace.py` `_COMMIT` match the same example lines; `refs/ledger.md:127` lists `COMMIT` |
| T-11 | Archive test (extend `tests/skills/test_workflow_archive.py`) | A managed ledger with `COMMIT:` lines archives. A `COMMIT:` line that names an unknown task gives `E-ARCHIVE-LEDGER` |
| T-12 | `tests/commands/test_git_command.py` (static) | Front matter (FR-001); Usage forms (FR-002); section order and a single Activation `> Skill sc:git-protocol` (FR-003); no `## Unattended mode`; no `merge`, `push` or `pull` operation in Usage; Will Not text (FR-005) |
| T-13 | `tests/skills/test_git_protocol.py` (static) | Registry rows point to existing refs and helper verbs (FR-008); the prose lists equal the `rules.py` constants (FR-013); no `src/<package>/` path (FR-009) |
| T-14 | Fixture and table updates | S23 `activation` becomes `{"sc:git": "sc:git-protocol"}`; `test_worker_contract.py:2953-2960` drops the merge example; parity parametrization gains `git` (FR-015); `commands/sc-git.md` is in the absence list (FR-014) |
| T-15 | `--commit-tasks` scope test (FR-052) | The string appears only in the allowed files |
| T-16 | No-flag regression | A legacy and a managed run without `--commit-tasks` write no `COMMIT:` line, and the existing implement tests pass unchanged |
| T-17 | No-deletion scan (FR-081) | No branch-deletion or remote-deletion argv in the new code or primitives |
| T-18 | Gate | `make verify-sync` exits 0; `uv run pytest tests/core tests/commands tests/skills tests/recommend tests/docs tests/vcs tests/worktree_cleanup` passes |

## 10. Non-functional requirements

- **NFR-001 (no outward action)** No new code or primitive pushes, fetches, pulls, merges, or touches a remote. T-03 and T-17 check this.
- **NFR-002 (visible writes)** Every repository write runs as its own Bash call with argv the helper planned, so every host hook sees it. The helper performs no write. T-03 checks this.
- **NFR-003 (single source for safety rules)** Protected branches, forbidden flags and path rules live once, in `rules.py`. The prose copies are pinned by a parity test (T-13). Changing one rule takes one constant edit plus one prose edit, and the test fails if only one of them changes.
- **NFR-004 (extension cost)** A new `/sc:git` operation needs at most a registry row, one ref section, an optional helper verb, a Usage and Options row, and tests. No existing operation's text or code changes (FR-008).
- **NFR-005 (backward compatibility)** Without `--commit-tasks`, `/sc:implement` writes the same ledger records it writes today, and every existing implement, archive and worker-contract test passes (T-16).
- **NFR-006 (determinism)** The same ledger and tree give byte-identical `stage-plan` JSON: paths sorted, ids in source order.
- **NFR-007 (bounded output)** Helper JSON is at most 64 KiB, path lists hold at most 200 entries with a `truncated` flag, and refusal logs keep at most 40 lines.
- **NFR-008 (latency)** Each helper verb finishes in 5 seconds or less on this repository with a warm file cache. This is a target; no baseline has been measured (UNVERIFIED).
- **NFR-009 (version coupling)** The helper prints `vcs_contract: "1"`, and both skills refuse any other value (`helper-missing`). A breaking change to the helper's JSON raises the number in one release, together with both skills.
- **NFR-010 (installed-path rule)** No new or edited primitive names `src/<package>/...` (FR-009). Checked with the project's grep rule and T-13.
- **NFR-011 (git version)** The helper refuses git versions below 2.23. The environment has 2.47.3.

## 11. Risks and mitigations

| # | Risk | Mitigation | Residual |
|---|---|---|---|
| 1 | Prompt rules are only advice. An agent may run `git commit -a` or `--no-verify` by hand | Exact argv comes from the helper (FR-061); the launch-level guard classes `--no-verify` as TAMPER in launched sessions (`:786`); T-02 and T-04 | In ordinary sessions nothing enforces this mechanically |
| 2 | Formatter hooks (`markdownlint --fix`, `ruff-format`) rewrite files and fail the commit | Classified `commit-failed`; STOP; resume plans again (FR-064, FR-065) | The person must review the rewrite |
| 3 | A ledger grammar change breaks `E-LEDGER-CORRUPT` checks or archiving (`E-ARCHIVE-LEDGER`) | Change `ledger.md:127`, `archive_workspace.py` and the helper in one change; parity test T-10; archive test T-11 | None if they land together |
| 4 | Edits the person made in a touched file get swept into a task commit | Wave 0 `dirty` refusal (FR-054) | Edits made during the run in touched paths (WC-11 notes other writers) |
| 5 | Inspecting submodules loads the submodule's own config, which can run a program (issue 547) | Same `-c core.fsmonitor=false` seam as `probes.py:65`; submodule inspection only runs on a person's `/sc:git submodule` line | Whether `-c` overrides reach every submodule child process and filter is UNVERIFIED |
| 6 | `origin/HEAD` names the wrong default (here `origin/master`, while GitHub's default is `integration`) | `PROTECTED_BRANCHES` always includes `integration` and matches `LL-PROTECTED` | Other projects with differently named shared branches |
| 7 | In launched sessions below `full --submit`, the guard blocks the first commit, so the run stops after the first task | `blocked-by-host` stops cleanly; FR-052 keeps the flag out of launch prompts | Lost time if a person adds the flag at the wrong level |
| 8 | An automated sync may re-create `commands/sc-git.md` (see commit `ff5f73adf`) | Absence test (FR-014) | Whether that automation still runs is UNVERIFIED |
| 9 | The installed skill text and the installed CLI drift apart | `vcs_contract` check (NFR-009) | None beyond a clear refusal |
| 10 | A batch commit covers up to 3 tasks, which is coarser than one task per commit | Trailers list each task; `files=` sets stay separate in the ledger | Accepted |
| 11 | The stash stack is shared across linked worktrees | `/sc:git` never stashes (FR-004) | None |
| 12 | Fixture and table churn (S23, worker-contract scan, routing table) | Updated in the same change (T-14); the three pinned phrases are kept (FR-017) | None |
| 13 | A CI check may require a `## Generator-Constraint Considered` section in the PR body when a gate or validator file changes (user memory note) | Add the section if the check flags `archive_workspace.py` | Which files the check covers is UNVERIFIED |
| 14 | `allowed-tools` in front matter may not restrict tools; it may only pre-approve them | It is not treated as a security boundary; the safety comes from NFR-002 and FR-011 | Its exact semantics in the host are UNVERIFIED |

## 12. Decisions on the seed brief's open questions

- **D1. Structure of `/sc:git`.** Decision: a command file, plus the `sc-git-protocol` skill with one ref per operation group, plus the read-only `<cli> vcs` helper. Why: this is the developer guide's command, skill and refs pattern (§3.1, §5.6) and the house pattern used by implement, issue and closeout. The operation registry (FR-006, FR-008) gives a single extension point. The commit planning that two consumers share needs real code that behavior tests can exercise, not prose. A smaller option was considered and rejected: a command file only, with prose rules and no helper. It is cheaper today, but it can only be tested statically, and the second consumer would have to copy its rules.
- **D2. How `/sc:implement` calls the commit step.** Decision: an inline step in the implement protocol (`refs/commit.md`, positions Q8a, R0 and L0) that calls the shared helper `<cli> vcs stage-plan`. It never calls `/sc:git`. Why: it does not touch the never-as-worker rule, there is one tested planner, and the "no task is open" condition (FR-056, FR-059) keeps HEAD unchanged during every task, so the retry ladder and the Ruling resume checks still hold.
- **D3. Authorization switch.** Decision: the `--commit-tasks` flag on the invocation line, per invocation. It is refused under `--unattended`, and no other primitive may add it (FR-050 to FR-052). Why: a flag can be checked mechanically. A plan field is written by automation, which is the "executor-invented approval" risk (`WORKER-CONTRACT.md:57`). A free-text instruction in the session cannot be tested.
- **D4. Submodule operations and the dirty or detached cases.** Decision: three operations, `status`, `update` and `commit-pointer`. Dirty means every write operation refuses. Detached with commits that no branch contains means stop and ask. Nested submodules are reported but not inspected. There is no push, no `--remote` and no `foreach` (§5). Why: this follows the order in the research (commit inside the submodule on a branch, then the pointer) and avoids the push side effect of `submodule.recurse`.
- **D5. `commands/sc-git.md`.** Decision: remove it, and add it to the absence test (FR-014). Why: nothing reads that folder, the copy is stale with a doubled prefix, and a byte copy could not carry the protocol skill, so it would be a broken half-copy.
- **D6. Residual project-management scope.** Decision: none in this work. Issue and PR status and progress are already covered by `/sc:issue`, `/sc:closeout` and the `issue-pipeline` CLI verbs (`HOW-WE-WORK.md:292`, `:296`; `WORKER-CONTRACT.md:302`). Revisit only if the owner names a specific gap.
- **D7 (added). `merge` in `/sc:git`.** Decision: removed. The seed brief's constraint ("`/sc:git` never pushes, merges or opens PRs") overrides the "merge operations" wording in `HOW-WE-WORK.md:293`, which is rewritten in the same change (FR-017).
- **D8 (added). What a managed commit includes.** Decision: the package directory, not all of `.dev/tasks` (FR-062). Why: this meets the always-staged rule (`git add -- .dev/tasks` still runs), PR 288's evidence rule (the package ledger and artifacts are committed), and it keeps unrelated packages out of the task commit.

## 13. Acceptance criteria

| AC | Criterion | Check |
|---|---|---|
| AC-01 | `git.md` has the FR-001 front matter, the FR-002 usage, the FR-003 sections with one `> Skill sc:git-protocol`, and no `## Unattended mode` | T-12 |
| AC-02 | `sc-git-protocol` exists with `SKILL.md`, the registry, the five refs and the extension checklist; registry rows resolve | T-13; `ls <pkg>/skills/sc-git-protocol/refs` lists `safety.md`, `status.md`, `commit.md`, `branch.md`, `submodule.md` |
| AC-03 | `<cli> vcs --help` lists `preflight`, `stage-plan`, `check-message` and `submodules`; the helper issues only allow-listed read argv | T-03; running `<cli> vcs --help` |
| AC-04 | The source, the plugin mirror and the dev copy are in sync, and `commands/sc-git.md` is gone | `make verify-sync` exits 0; `tests/commands/test_routing_plugin_parity.py` includes `git`; absence test |
| AC-05 | `/sc:implement --commit-tasks` commits between tasks only when no task is open, with exactly the planned paths plus the managed package directory, and writes `COMMIT: sha=` lines | T-01, T-02, T-09 |
| AC-06 | No commit inside a parallel batch; one commit after every member has `complete` | T-01 (batch case) |
| AC-07 | A refused or failed hook gives `COMMIT: refused` and `E-COMMIT-REFUSED`, HEAD does not move, and there is no `--no-verify` or `--amend` | T-04 |
| AC-08 | Without the flag, behavior is unchanged and there are no `COMMIT:` lines | T-16 |
| AC-09 | `--commit-tasks` together with `--unattended` gives `E-COMMIT-PRECONDITION reason=unattended`, and `/sc:git` stays never-as-worker | T-09; `tests/skills/test_worker_contract.py` passes with `NEVER_AS_WORKER` unchanged |
| AC-10 | The submodule `status`, `update` and `commit-pointer` operations classify and refuse as specified | T-07 |
| AC-11 | No local branch deletion outside `scripts/worktree_cleanup.py`, and no remote branch deletion anywhere | T-17; `tests/worktree_cleanup/` passes unchanged |
| AC-12 | Managed archiving accepts ledgers with `COMMIT:` lines | T-10, T-11 |
| AC-13 | The routing guide row, fixture S23 and the worker-contract scan are updated, and their tests pass | T-14; `uv run pytest tests/core tests/recommend tests/skills/test_worker_contract.py` |
| AC-14 | No new or edited primitive names a `src/<package>/` path | T-13; the project's grep rule over commands, skills, agents, core and hooks |
| AC-15 | The full gate passes | T-18 |
