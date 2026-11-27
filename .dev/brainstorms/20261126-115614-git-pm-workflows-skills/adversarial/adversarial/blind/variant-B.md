# Requirements Specification: Modular `/sc:git`, Authorized Between-Task Commits in `/sc:implement`, and Submodule Operations (issue #326)

- Persona: analyzer (root-cause first, evidence for every architectural claim)
- Date: 2026-11-26
- Inputs: `seed-brief.md`, `enrichment/codebase-context.md`, `enrichment/research-deep.md` (all in `.dev/brainstorms/20261126-115614-git-pm-workflows-skills/`), `.dev/issues/326/issue-summary.md`, `.dev/issues/326/analysis/analyze-git.md`, `.dev/issues/326/accuracy-check.md`
- Verification method: every repo citation below was read in this checkout on 2026-11-26 (Read, Grep, read-only git). Anything not checked is marked UNVERIFIED. Flags and files that this spec introduces are marked **(new)**; nothing marked (new) exists today.

## Path notation

The package directory, the dev-copy directory and the per-user install root all carry the package's own name, so this document uses these aliases. Each one can be resolved from the repository.

| Alias | Meaning | How to resolve it |
|---|---|---|
| `<name>` | The Python package name | `pyproject.toml:6` (`name = ...`) |
| `<pkg>` | `src/<name>/`, the source of truth for every installed primitive | `pyproject.toml:79` (`packages = [...]`) |
| `<plugin>` | `plugins/<name>/`, the plugin mirror that `make build-plugin` copies unchanged | `Makefile:65-71`; the build script copies `agents, commands, hooks, rules, scripts, skills` as-is |
| `<dev>` | The hidden, gitignored dev-copy directory at the repository root that `make sync-dev` writes; its only tracked file is `settings.json` | `Makefile:109-163` |
| `<home>` | The per-user install root that `<name> install` writes (`<home>/commands/sc/`, `<home>/skills/`, `<home>/agents/`, core files in `<home>/`) | `<pkg>/cli/install_commands.py:29` |
| root instructions file | The repository's root agent-instructions markdown file that holds the "ABSOLUTE RULE" sections | repository root |
| developer guide | `docs/developer-guide/*-Developer-Guide-Commands-Skills-Agents.md` | glob in `docs/developer-guide/` |

## 1. Overview and scope

### 1.1 Problem in one paragraph

`/sc:git` is a 91-line prose command (`<pkg>/commands/git.md:1-91`). It has no options table, no STOP rules and no backing skill, it says nothing about submodules, and it has never been changed in function (`analyze-git.md` F1). `/sc:implement` makes no commit between tasks (`<pkg>/commands/implement.md:100`: "Auto-commit, open PRs, or release" is a Will Not). So a long plan lands as one uncommitted change, and a lost session or a bad revert can take earlier tasks' uncommitted work with it (`<pkg>/skills/sc-implement-protocol/refs/retry.md:39`). The owner's scope of 2 November narrows the issue to four items: a modular refactor of `/sc:git`, an explicitly authorized commit between tasks in `/sc:implement`, submodule operations in `/sc:git`, and only the branch cleanup that PR 711 did not deliver (`issue-summary.md`, "Decided for this work").

### 1.2 In scope

1. Refactor `/sc:git` into a thin command file plus a protocol skill `sc-git-protocol` **(new)** with `refs/` and one read-only helper script. Mirror it into `<plugin>`, the dev copy and the routing guide.
2. Add an opt-in commit step between tasks to `/sc:implement`, behind a new flag `--commit-tasks` **(new)**. It uses the same read-only helper as `/sc:git`.
3. Add three submodule operations to `/sc:git`: `submodule status`, `submodule update` and `submodule commit-pointer` **(new)**.
4. Decide what happens to `commands/sc-git.md`. The decision is to remove it (section 11, Q5).
5. Update the tests that pin the old behaviour, and add tests for the new behaviour (section 9).

### 1.3 Explicitly out of scope (decided)

| Item | Reason / evidence |
|---|---|
| A central relay where every command calls `/sc:git` | Rejected on 2026-11-02 because commands cannot call another session (`accuracy-check.md` row 10). `/sc:git` is on the never-as-worker list (`<pkg>/core/WORKER-CONTRACT.md:23`) |
| Push, PR creation, PR monitoring, merging into a shared or protected branch | PRs stay with `/sc:pr-submit` (root instructions file, "PR Target" rule). The routing row says "Do not append push, merge or PR creation" (`<pkg>/core/HOW-WE-WORK.md:293`) |
| Remote branch deletion, anywhere | Decided by the owner (`issue-summary.md`). `/sc:worktrees` will not delete a remote branch (`<pkg>/commands/worktrees.md:80`) |
| A second implementation of local branch cleanup | PR 711's `scripts/worktree_cleanup.py` already deletes local branches with `git branch -d` only (`scripts/worktree_cleanup.py:2617`, `:2636-2642`). It is reused, not rebuilt |
| Changes to `scripts/worktree_cleanup.py`, the launch-level guard, the issue-claim launch prompts, or the sweep probes | Not needed by any requirement below. Each change would widen the blast radius |
| Fixing or removing `docs/developer-guide/git-standards-protocols.md` | It is another project's document (section 2, RC-5). This work treats it as non-normative and records a follow-up |
| The other 20 files in the legacy top-level `commands/` directory | Three of them are pinned by `tests/commands/test_help_text_fixes.py:17`, `:41`, `:92`. Only `commands/sc-git.md` is in scope |
| A "project management" extension (status and progress posting) | No residual scope (section 11, Q6) |
| A new hook that denies `--no-verify` in ordinary sessions | Recorded as a risk with a recommended follow-up (section 10, R1); not built here |

## 2. Root causes (why these capabilities are missing today)

Each root cause is stated as a falsifiable claim with its evidence. Section 3 onward is designed to remove these causes, not only to add features.

### RC-1. `/sc:git` predates the three-tier command/skill architecture, and the test suite pins its old shape

- The developer guide makes a command a "thin dispatch stub" of about 80-150 lines with an `## Activation` handoff (developer guide `:53`, `:63-75`). It also says "Every skill MUST have a command in front of it" (`:59`) and lists the required body sections (`:294-306`).
- `git.md` has no `## Activation`, no `## Options`, no STOP rules and no `argument-hint` (`<pkg>/commands/git.md:1-91`). Its history holds only a markdownlint commit and a bulk restore (`analyze-git.md` F1).
- The old shape is locked in by tests:
  - routing case S23 asserts that `/sc:git` is `"self-contained"`, meaning the command has no Activation section (`tests/recommend/fixtures/routing_refresh_cases.json:325`, enforced by `tests/recommend/test_routing_refresh.py:483-496`);
  - its two examples are pinned by exact text in the write-verb classification table (`tests/skills/test_worker_contract.py:2945-2960`).
- So any refactor has a guaranteed test cost, which discourages incremental change.

### RC-2. "A commit needs authorization" was written as prose with no mechanism behind it

- The routing guide says "a commit needs authorization" (`HOW-WE-WORK.md:293`) but never says what counts as authorization.
- `/sc:implement` simply forbids commits (`implement.md:100`). The worker contract parks per-task commits on this issue ("wait for issue #326 (K3)", `WORKER-CONTRACT.md:42`). No such flag exists (`analyze-git.md` F4).
- The only mechanical commit gate in the repo is the launch-level guard. It governs only sessions that the claim script launched ("every other session is ordinary and never blocked", `<pkg>/hooks/scripts/launch-level-guard.sh:5-7`). It allows `COMMIT` only at level `full --submit` (`:806-808`).
- The project settings have no deny rule for `git commit` or `--no-verify` (checked: the git-related permission entries in `<dev>/settings.json` contain none).
- Research shows that prompt-only rules are broken in practice (`research-deep.md` §1, "Rules in the prompt are advisory").
- With nothing to build on, the only safe default was "never commit".

### RC-3. `/sc:implement`'s recovery design depends on HEAD staying still, so a commit point had to be designed around coupled invariants

- The retry ladder needs HEAD unchanged since the task's Q0 (`refs/retry.md:41`; `halt ... reason=head-moved`, `:454`).
- The coordinator's resume check requires HEAD to equal `<retries>/T<id>/q0-head` (`WORKER-CONTRACT.md:280`). A frozen plan forbids any git command that moves HEAD (`:266`).
- Q0 pins each task's start tree as `refs/<name>/implement/<slug>/T<id>` and deletes the pin at `complete` (`<pkg>/skills/sc-implement-protocol/SKILL.md:123-129`).
- The ledger grammar is closed: an unknown last line is `E-LEDGER-CORRUPT` (`refs/ledger.md:127`).
- A commit inside a task would trip `head-moved`, and a new ledger record type would break resume parsing and the archive helper's ordering checks (`refs/managed-workspace.md:93`).
- These coupled constraints, not a lack of interest, are why K3 was parked.

### RC-4. Submodules were only ever handled defensively at the edges, and automation is shut out on purpose

- Every existing consumer refuses or ignores submodules:
  - `/sc:pr-submit` halts on a submodule conflict (`<pkg>/commands/pr-submit.md:71`; `<pkg>/pr_submit/conflicts.py:733`);
  - the sweep passes `--ignore-submodules=all`, because "a submodule's own config could start a program, issue 547" (`<pkg>/cli/sweep/probes.py:64-76`);
  - the implement revert leaves gitlinks out and prints `SUBMODULE <p> <sha>` for a person to fix by hand (`refs/retry.md:212`).
- The launch-level guard's allow-table has no `submodule` subcommand (`launch-level-guard.sh:720`). It falls to `UNKNOWN` (`:724`), which is denied at every launch level (`:816`).
- No command owns the positive operations, so none was ever defined (`analyze-git.md` F5).
- The repository has exactly one submodule, declared in `.gitmodules` under `.vendor/`. In this checkout `git submodule status` prints it with a `-` prefix (not initialized) and gitlink mode `160000`, so the code paths are real but rarely exercised.

### RC-5. The "standards" the issue points to are not this repository's standards

- `docs/developer-guide/git-standards-protocols.md` belongs to another project:
  - its front matter id is `GFXAI-GIT-STANDARDS-PROTOCOLS` (`:2`), its scope line says "for the GFxAI project" (`:54`) and its status is "To Do" (`:6`);
  - it prescribes `main` as the only long-lived branch (`:233`) and the message format `[GFXA-XXX] Brief description` (`:431`);
  - it calls Conventional Commits "encouraged ... non-blocking" (`:461`).
- This repository enforces the opposite:
  - `.pre-commit-config.yaml:78-84` runs `conventional-pre-commit` at the `commit-msg` stage, and a `[GFXA-XXX]` header would fail that hook;
  - the protected branches are `master` and `integration` (`docs/developer-guide/branch-protection.md`, "What is protected"; `.github/rulesets/protect-*.json` each carry `deletion`, `non_fast_forward`, `pull_request`).
- The developer guide's front matter vocabulary (`category` list at `:276-277`, `complexity` list at `:278`) also differs from repo practice (`git.md` and `help.md` use `category: utility`; `worktrees.md` uses `workflow` / `standard`). No code reads `category` (Grep over `<pkg>/cli`, `scripts`, `tests`).
- "Follow the standards" therefore cannot be executed literally. The refactor must follow the enforced gates (pre-commit config, rulesets, routing guide) and say so.

### RC-6. Four copies with no single parity rule make every edit expensive and drift-prone

- `git.md` exists in four places: `<pkg>/commands/git.md`, `<plugin>/commands/git.md` (byte-identical today, `diff -q` silent), the dev copy, and `commands/sc-git.md`.
  - The legacy copy carries the doubled title `/sc:sc:sc:git` and the usage `/sc:sc:git`.
  - Only four commands are parity-tested (`<pkg>/commands/README.md:9`; `tests/commands/test_routing_plugin_parity.py:41-47`).
  - `make sync-dev` never touches `<plugin>` (`Makefile:109-163`).
  - The legacy `commands/` directory is not packaged: the wheel and sdist include only `src/` and `plugins/` (`pyproject.toml:78-97`).
- `/sc:git`'s parity therefore holds by habit, and the legacy copy drifts with nothing to catch it.

### RC-7. Existing tools do not solve this problem, so it has to be designed here

- An official marketplace plugin, `commit-commands`, is a thin prompt with no handling of hooks, protected branches, submodules or parallel work, and its `clean_gone` force-deletes with `-D` (`research-deep.md` §3).
- Session checkpoints are "not a replacement for version control" and miss shell edits (`research-deep.md` §1).
- The tool that commits after every edit (Aider) appears to skip hooks by default (`research-deep.md` §1, UNVERIFIED there).

## 3. Structure of the refactored `/sc:git`

### 3.1 Files

| Path | Status | Content |
|---|---|---|
| `<pkg>/commands/git.md` | rewritten | Interface only: front matter, Triggers, Usage, Options, STOP rules, Behavioral Flow (parse, STOP, activate, print), `## Activation` naming `> Skill sc:git-protocol`, Outputs, Boundaries, Related Commands |
| `<pkg>/skills/sc-git-protocol/SKILL.md` | **(new)** | Authorization classes, the context capture, operation dispatch, the never-list, the report format, and which ref each operation loads |
| `<pkg>/skills/sc-git-protocol/refs/commit.md` | **(new)** | `add`, `commit`, `--smart-commit` message rules, hook outcome handling |
| `<pkg>/skills/sc-git-protocol/refs/branch.md` | **(new)** | Branch list/create, `switch`, `merge` preview and confirmation, deletion pointer to `/sc:worktrees` |
| `<pkg>/skills/sc-git-protocol/refs/submodule.md` | **(new)** | `submodule status`, `update`, `commit-pointer`, dirty and detached rules |
| `<pkg>/skills/sc-git-protocol/scripts/commit_plan.py` | **(new)** | Read-only helper with two subcommands, `preflight` and `verify`, used by `/sc:git` and by `/sc:implement` (section 5) |
| `<plugin>/commands/git.md`, `<plugin>/skills/sc-git-protocol/` | mirrored | Byte copies (FR-007) |
| `commands/sc-git.md` | removed | Section 11, Q5 |

The skill is named `sc-git-protocol`, not `sc-git`. The installer skips a bare `sc-<cmd>` skill whose command exists and does not strip a `-protocol` suffix (`<pkg>/cli/install_skills.py:47-59`; developer guide `:705`).

### 3.2 Requirements

- **FR-001** The command file has front matter with `name: git`, `description`, `category: utility` (kept, section 11), `complexity: standard`, `mcp-servers: []`, `personas: []` and an `argument-hint`.
  - Its body has exactly one `## Activation` section, which contains the line `> Skill sc:git-protocol`, plus `## Options`, a STOP rules section, `## Outputs`, `## Boundaries` and `## Related Commands`.
  - The file is at most 150 lines and contains no protocol logic. This means no git command lines other than in Usage/Examples, and no precondition algorithm.
- **FR-002** `--smart-commit` and `--interactive` stay declared in the command's Usage, `argument-hint` or Options table. The fixture flag check requires this (`tests/recommend/test_routing_refresh.py:307-317`; S23 repeats at `routing_refresh_cases.json:327`).
  - The example lines `/sc:git commit --smart-commit` and `/sc:git merge feature-branch --interactive` are kept verbatim, so their classification rows (`test_worker_contract.py:2945-2960`) stay valid.
- **FR-003** The command has no `## Unattended mode` section and no `--unattended` option. It states that it is on the never-as-worker list of `<home>/WORKER-CONTRACT.md`. A standalone `--unattended` token is a STOP before any git call.
- **FR-004** `SKILL.md` has front matter `name: sc:git-protocol`, `description`, and `allowed-tools: Read, Grep, Glob, Bash, Write`.
  - It has no `Edit`, `Task` or `Skill`: Write is only for the commit message file.
  - It is at most 500 lines (developer guide `:678`). It states, per operation, which single ref it loads, and loads no ref for read-only operations except `submodule status`.
- **FR-005** Before any operation, the skill captures read-only context:
  - current branch or detached state, upstream and ahead/behind;
  - any in-progress operation (merge, rebase, cherry-pick, revert, bisect) and whether `index.lock` is present;
  - `git status --porcelain=v2 --ignore-submodules=none` with its `S<c><m><u>` submodule field (`research-deep.md` §2);
  - the values of `submodule.recurse`, `push.recurseSubmodules` and `diff.submodule`;
  - the last 10 `log --oneline` entries.

  Every git read runs as `git --no-optional-locks -c core.fsmonitor=false ...`, the same seam as `probes.py:64-66`.
- **FR-006** The operation table is closed:

| Operation | Class | Behaviour |
|---|---|---|
| `status` | read | Context from FR-005 as a report, plus the submodule summary |
| `diff [<paths>]` | read | Unstaged and staged diff for the named paths, or all |
| `log [<n>]` | read | Last n commits (default 10) |
| `branch` | read | `git branch -vv` as git prints it, with the note that `[gone]` is not proof of merge (`research-deep.md` §5) |
| `branch <new>` | write | Create from HEAD. Refuses `master`, `main`, `integration` and the resolved default branch |
| `switch <branch>` | write | `git switch <branch>`. Never `--discard-changes`, `-f` or `--force` |
| `add <paths...>` | write | Explicit paths only (FR-014) |
| `commit [<paths...>] [--smart-commit]` | write | refs/commit.md |
| `merge <branch> [--interactive]` | merge | refs/branch.md, FR-013 |
| `submodule status` | read | refs/submodule.md, FR-033 |
| `submodule update [<path>]` | write | FR-034 |
| `submodule commit-pointer <path> [--smart-commit]` | write | FR-035 |

  Any other operation is a STOP that prints "not an /sc:git operation" and a pointer. The other operations include `push`, `pull`, `fetch --prune`, `rebase`, `reset`, `restore`, `clean`, `stash`, `tag`, `cherry-pick`, `revert`, `branch -d`, `branch -D`, `branch --delete` and any other `submodule` subcommand. The pointer says: push and PRs go to `/sc:pr-submit`, worktree and local branch removal goes to `/sc:worktrees`, and everything else should be run by the person.
- **FR-007** Mirror and sync:
  - `<plugin>/commands/git.md` is a byte copy of `<pkg>/commands/git.md`;
  - `<plugin>/skills/sc-git-protocol/` is a byte copy of `<pkg>/skills/sc-git-protocol/`, ignoring `__init__.py` and `__pycache__`;
  - `git.md` is added to the mirrored list in `<pkg>/commands/README.md:9`, and `"git"` is added to the parametrize list of `test_readme_listed_command_mirrors_match_src` (`tests/commands/test_routing_plugin_parity.py:41`);
  - `make sync-dev` then `make verify-sync` exits 0.

  The dev copy is never staged (root instructions file, "Never Stage or Commit" rule). The plugin mirror is required because the plugin build copies `<plugin>` as-is, so a plugin `git.md` that activates a missing skill would be broken in plugin-only installs.
- **FR-008** `commands/sc-git.md` is removed with `git rm`, and no other file under `commands/` is changed.
- **FR-009** The `/sc:git` row in `<pkg>/core/HOW-WE-WORK.md:293` may gain the words "submodule status, update and pointer commit" and "branch removal: /sc:worktrees".
  - It keeps these three phrases verbatim: "Status-only stays inspection", "a commit needs authorization" and "Do not append push, merge or PR creation".
  - Its route steps must not name `sc:pr-submit`, which is S23's competitor (`test_routing_refresh.py:224-243`).
  - The guide is then copied byte-for-byte to `<plugin>/skills/sc-recommend/refs/HOW-WE-WORK.md` (`<pkg>/commands/README.md:11`).
- **FR-010** S23's `"activation": {"sc:git": "self-contained"}` becomes `{"sc:git": "sc:git-protocol"}` (`routing_refresh_cases.json:325`). Every new or changed line under `<pkg>/{skills,commands,agents}` that matches `WRITE_VERB_RE` (`test_worker_contract.py:1894-1897`) gets exactly one row in the classification table:
  - `never-worker` for `sc-git-protocol` lines;
  - `deferred:P4` for the new `/sc:implement` commit-step lines, with the reason "the per-task commit step is off under --unattended (WC-9); /sc:implement is converted in P4".

  Stale rows are removed (`test_worker_contract.py:3227`).

## 4. Authorization model

Root cause addressed: RC-2. The model gives a mechanism that can be tested, defined over operation classes.

- **FR-011 Read class** (`status`, `diff`, `log`, `branch` list, `submodule status`): runs with no authorization. It may run when another command suggests it (for example `/sc:implement`'s Done section, `SKILL.md:193`). A read never writes the index, the working tree, refs or config. `--no-optional-locks` (FR-005) prevents the index refresh write.
- **FR-012 Write class** (`add`, `commit`, `branch <new>`, `switch`, `submodule update`, `submodule commit-pointer`): runs only when the person's own current message starts with `/sc:git <that operation>`.
  - The authorization covers that one operation, once, in that invocation. It never carries over to a later turn.
  - When the skill is reached any other way (through the Skill tool from another command, or on an agent's own initiative), every write operation refuses with `authorization: write operations need a person-typed /sc:git <operation>`, and read operations still run.
  - Precedent for "the person's own message starts with": `/sc:graph init` (`WORKER-CONTRACT.md`, brief table, `/sc:graph` row).
- **FR-013 Merge class**: authorized as in FR-012, plus all of the following:
  1. Refuse when the current branch is in the protected set (FR-015), when HEAD is detached, or when a merge or rebase is in progress.
  2. Show a preview with `git merge-tree --write-tree HEAD <branch>`, which needs git 2.38 or later (`research-deep.md` §5); this checkout runs `git version 2.47.3`. The preview prints the conflicted paths and the files that would change, and touches neither the working tree nor the index.
  3. Ask for a yes/no confirmation in chat, and run `git merge <branch>` only after a yes.
  4. On a conflict, stop and report the conflicted paths. Never resolve them automatically and never run `git merge --abort` automatically; print `git merge --abort` as the person's undo. This matches the coordinator rule "a merge conflict is stopped and reported, never resolved automatically" (`WORKER-CONTRACT.md:237`).
- **FR-014 Never-list** (refused by the command's STOP rules or the skill, whatever the authorization):
  - `push` in any form;
  - PR creation;
  - remote branch deletion;
  - local branch deletion;
  - `--no-verify`, `-n` on `commit`, a `SKIP=` environment prefix (pre-commit's documented skip variable; UNVERIFIED against a specific pre-commit version), `-c core.hooksPath=` and `--amend`;
  - `-f` or `--force` on `add`, `switch`, `checkout` or `branch`;
  - broad pathspecs on `add` or `commit`: `.`, `-A`, `--all`, `-u`, `--update`, `:/`, `*`;
  - staging any path under `<dev>/` except `<dev>/settings.json`;
  - `reset`, `rebase`, `clean`, `stash drop`, `tag`;
  - `submodule update --remote`, `--force` or `--recursive` combined with `--remote`;
  - `git push --recurse-submodules=on-demand`.
- **FR-015 Protected set**: `master`, `main` and `integration` (the names the launch-level guard protects, `launch-level-guard.sh`, `LL-PROTECTED` message, and the rulesets), plus the default branch from `git symbolic-ref --short refs/remotes/origin/HEAD` when that resolves. A write that creates a commit on, or merges into, a branch in the protected set refuses with `branch`. A commit on a detached HEAD refuses with `detached`.
- **FR-016 Commit mechanics** (shared by `/sc:git commit`, `submodule commit-pointer` and the `/sc:implement` step):
  1. Write the message with the Write tool to a temporary file outside the working tree.
  2. Run `commit_plan.py preflight`.
  3. Run `git add -- <paths>`, with `.dev/tasks` appended when it exists, as one literal Bash command.
  4. Run `git commit --only -F <message-file> -- <paths>` as a second literal Bash command.
  5. Run `commit_plan.py verify`.

  The commit is a literal Bash command, never run inside a script: the launch-level guard classifies a command as git only when its text has a `git` word (`launch-level-guard.sh:555-557`, `:595-600`, `:713`), so a script that ran `git commit` would hide the commit from `LL-COMMIT`. `-F <file>` follows the guard's own advice for message text (`launch-level-guard.sh:135`). `.dev/tasks` is added because it is always staged (root instructions file rule 4; `WORKER-CONTRACT.md:247`).
- **FR-017 Hook outcome**: a non-zero `git commit` exit, or a refused tool call, is classified by `verify` (FR-021) and reported. The skill never retries with a bypass and never amends. A new commit after the person fixes the cause needs a new person-typed `/sc:git commit`. This follows the practice "fix, re-stage, make a NEW commit; never --amend" (`research-deep.md` §1).
- **FR-018 Report**: every write operation prints:
  - the preconditions it checked;
  - the exact argv of every git command it ran;
  - the result (new commit hash, refusal token, or conflict list);
  - an undo hint that is printed and never run: `git revert <sha>`, or `git reset --soft <parent>` for an unpushed commit.

### 4.1 Helper script `commit_plan.py` **(new)**

- **FR-019** The script runs as `uv run --no-project python "<skill base>/scripts/commit_plan.py" <subcommand> ...` (precedent: `refs/managed-workspace.md:54`).
  - It uses only the standard library and writes nothing in the repository.
  - Every git call goes through one runner that allows only read verbs: `rev-parse`, `symbolic-ref`, `status`, `ls-files`, `ls-tree`, `cat-file`, `check-ignore`, `diff`, `rev-list`, `log`, `config --get`, `submodule status`, `merge-tree --write-tree`, and `read-tree`/`add`/`write-tree` only under a private `GIT_INDEX_FILE`. Any other verb raises. The allow-list pattern follows `scripts/worktree_cleanup.py:385-392`.
  - Each call has a 10-second timeout. Output is one JSON object on stdout.
- **FR-020** `preflight --top <dir> [--q0-head <file>] [--start-ref <ref>] [--allow-gitlink <path>] --message <file> -- <paths...>` returns `{"status":"ok","pre_tree":"<40-hex>","add":[...],"commit":[...]}` or `{"status":"refuse","reason":"<token>","detail":"..."}`. The reason is one of this closed list:
  - `detached`, `branch`, `in-progress-op`, `index-lock`, `outside-repo`, `ignored-path`, `dev-copy-path`, `broad-pathspec`, `submodule-path`;
  - `submodule-dirty`, `submodule-unpublished`, `foreign-change`, `head-moved`, `no-snapshot`;
  - `message-invalid`, `helper-error`, `git-too-old`.

  `pre_tree` is the private-index tree of the named paths as they stand in the working tree.
- **FR-021** `verify --top <dir> --old-head <40-hex> --pre-tree <40-hex> --exit <code> [--plan <slug> --task <T<id>>...] -- <paths...>` returns one closed token:
  - `committed sha=<40-hex>`: HEAD moved by one commit and its tree for the paths equals `pre_tree`;
  - `empty`: exit non-zero, HEAD unchanged, git reported nothing to commit;
  - `hook-failed`: HEAD unchanged, paths unchanged;
  - `hook-rewrite`: HEAD unchanged, paths changed in the working tree;
  - `hook-rewrite-committed`: HEAD moved, but the committed tree differs from `pre_tree`;
  - `guard`: the tool call was refused before git ran, so HEAD and index are unchanged and no git process left a trace. The format of a host refusal is UNVERIFIED, so the classification rests on "nothing changed and the tool result says blocked";
  - `recovered sha=<40-hex>`: on resume, HEAD's parent equals `--old-head` and HEAD's message carries the trailers `Implement-Plan: <slug>` and `Implement-Task: T<id>`.

  `verify` also lists dirty tracked paths outside `.dev/` that remain after the commit.

## 5. Between-task commit behaviour in `/sc:implement`

Root causes addressed: RC-2 and RC-3. The step is placed where none of the HEAD invariants can see it.

### 5.1 Switch, parse and early refusal

- **FR-022** New flag `--commit-tasks` **(new)**, added to `implement.md`'s `argument-hint` (`implement.md:7`), its Options table and the skill's Wave 0 known options (`SKILL.md:57`).
  - It counts only as a standalone token outside any quoted argument, the same rule as `--unattended` (`WORKER-CONTRACT.md:13`). It is honoured only when the person's own current message starts with `/sc:implement`.
  - When the skill is reached through another command (`implement.md:16-19`, trigger 2) or the token comes from an agent's own invocation, the run stops with `E-COMMIT-REFUSED reason=not-person` before any write.
  - The flag is per invocation and never persisted. A resume without it commits nothing (FR-029).
- **FR-023** When `--commit-tasks` is present, Wave 0 runs `commit_plan.py preflight` once with no paths, after step 6 (ledger) and before the first Q0. It resolves the helper at `<home>/skills/sc-git-protocol/scripts/commit_plan.py`, then at the project dev copy. This is the dual-surface order for skills required by the root instructions file.
  - Before the ledger is created or any product is written, the run stops with `E-COMMIT-REFUSED` and one of the reasons `helper-missing`, `detached`, `branch`, `in-progress-op` or `index-lock`.
  - On a resume the Wave 0 check runs after the ledger is read and before any pending commit (FR-029).

### 5.2 When and where (the commit point)

- **FR-024** A new loop step, `Q7b COMMIT`, sits between `Q7 GATE` (`SKILL.md:149`) and `Q8 NEXT` (`:150`). It runs only when `--commit-tasks` is in force and only for a task whose latest ledger verdict line is `complete`, after that line is flushed and before the next task's Q0 snapshot.
  - Q0 to Q7 is the task body, so HEAD stays still for every check that needs it: retry check 3 (`retry.md:41`) and the coordinator's condition (6) (`WORKER-CONTRACT.md:280`).
  - A `blocked` or `halt` task is never committed. A halted plan stays frozen with HEAD unmoved (`WORKER-CONTRACT.md:263-266`).
- **FR-025 Parallel batches.** Batch rules (a) to (c) stay as they are (`SKILL.md:110`). While any member of the batch has no `complete` or `halt` line, nothing is committed.
  - When every member is `complete`, Q7b runs once and makes one commit for the whole batch, with one `Implement-Task:` trailer per member in source order.
  - When any member halts, no commit is made for the batch. The run stops as rule (b) says, and the batch's commit is made on the resume that completes the halted member.
  - Rationale: every member shares the same `q0-head` (HEAD unchanged during a batch). A commit per member would move HEAD between members and break the `head-moved` invariant for the rest.

### 5.3 Which paths

- **FR-026** The commit set S is built as follows:
  1. Take the union of the `files=` fields of the committed task or tasks (`refs/ledger.md:44-57`).
  2. Remove every path under `.dev/implement/` (legacy ledgers are never added, `refs/ledger.md:3`).
  3. Append `.dev/tasks` when it exists (the managed ledger, its `artifacts/` and the `commits.md` sidecar, `refs/managed-workspace.md:36`; PR 288 preserved).

  `preflight` refuses, and nothing is staged, when:
  - S contains a gitlink (mode `160000` in HEAD, the Q0 tree or the working tree) or `.gitmodules` (`submodule-path`; the person uses `/sc:git submodule commit-pointer`);
  - S contains an ignored path (`ignored-path`), a `<dev>/` path other than `settings.json` (`dev-copy-path`), or a path outside the repository (`outside-repo`).
- **FR-027 Integrity preconditions** (checked by `preflight` with `--q0-head <retries>/T<id>/q0-head --start-ref refs/<name>/implement/<slug>/T<id>`):
  1. HEAD equals the `q0-head` 40-hex, or `head-moved`;
  2. for each product path p in S, the blob of p at `q0-head` equals the blob of p in the Q0 start tree, or `foreign-change`. This means the path carried no uncommitted change from before the task started, which keeps the person's own pending work out of a task's commit (the problem Aider handles by committing it first, `research-deep.md` §1; this spec refuses instead);
  3. the Q0 start is a tree and its pin and `q0-head` file exist, or `no-snapshot`.

### 5.4 Message format

- **FR-028** The message is a Conventional Commits 1.0 message (`research-deep.md` §4), which the repo hook enforces (`.pre-commit-config.yaml:78-84`). Its parts:
  - Header: `<type>: <summary> (T<id>)`, at most 72 characters. `<type>` is one of `feat`, `fix`, `docs`, `test`, `refactor`, `chore`:
    - `docs` when every product path in S ends in `.md` or sits under `docs/`;
    - `test` when every product path sits under `tests/`;
    - otherwise the agent chooses from the task text, using `feat` or `fix` only when they are true and `chore` otherwise.

    `<summary>` is the task title, made imperative and cut at a word boundary. A batch commit uses `(T<a>,T<b>[,T<c>])`.
  - Body: one line `Task T<id> of <ledger source token>` and one line `AC: <ac-list>` for each task.
  - Trailers: `Implement-Plan: <slug>` and one `Implement-Task: T<id>` per task, followed by any trailer the session's own standing instructions require.

  `preflight` validates the header against `^(feat|fix|docs|test|refactor|chore)(\([a-z0-9._-]+\))?!?: \S.{0,70}$` and checks that the trailers are present, else `message-invalid`. The hook's default type list is UNVERIFIED for `conventional-pre-commit` v3.0.0; the six types above are within the commonly accepted set.

### 5.5 Records, pins and resume

- **FR-029** Commit state lives in a sidecar file `commits.md` **(new)** in the ledger directory: `.dev/implement/<slug>/commits.md` for a legacy run, `<pkg-dir>/artifacts/commits.md` for a managed package.
  - It is not the ledger. Precedent: `codegraph.md` "is not the ledger and not a task notes file" (`SKILL.md:79`). The ledger grammar, `E-LEDGER-CORRUPT` and `archive_workspace.py` stay unchanged.
  - Lines: `T<id>: commit sha=<40-hex>`, `T<id>: commit skipped reason=empty`, `T<id>: commit refused reason=<token>`, `T<id>: commit recovered sha=<40-hex>`.
  - Pin lifetime: when `--commit-tasks` is in force, the Q0 pin and checkpoint refs of a committed task are deleted after its `commits.md` line is written, not at `complete` (amending `SKILL.md:129`). Otherwise they are deleted at `complete` as today.
  - Resume row 1 ("Latest verdict is complete → Skip. Delete the Q0 pin ...", `refs/ledger.md:157`) gains one clause. When this invocation carries `--commit-tasks`, the task's pin still exists, and `commits.md` has no `commit sha` or `recovered` line for it:
    1. run `verify` in recover mode first;
    2. if that does not return `recovered`, run Q7b for that task before anything else.
  - Without the flag, row 1 runs as today and prints `T<id>: completed without a commit (no --commit-tasks on this run)`.
  - A task completed in a run without the flag has no pin left, so it is never committed later. Its changes stay in the working tree, and a later task that touches the same paths refuses with `foreign-change`.
- **FR-030 Refusal.** Any `preflight` refusal, or any `verify` result other than `committed`, `empty` or `recovered`, appends `T<id>: commit refused reason=<token>` to `commits.md` and stops the run with `E-COMMIT-REFUSED`.
  - The refusal message prints the reason, the `git diff --stat` of S and the next step.
  - Staged paths stay staged (staging is not committing). The task stays `complete`. `empty` is recorded and the run continues.
  - The STOP table (`SKILL.md:30-49`) gains one row:

  | Code | Trigger | Product writes? | Ledger? |
  |---|---|---|---|
  | `E-COMMIT-REFUSED` | `--commit-tasks` given and: Wave 0 precondition fails (`not-person`, `helper-missing`, `detached`, `branch`, `in-progress-op`, `index-lock`), or Q7b's `preflight` refuses, or `verify` returns `hook-failed`, `hook-rewrite`, `hook-rewrite-committed` or `guard` | Wave 0: No. Q7b: No T{i+1} | Wave 0: No. Q7b: unchanged (task stays `complete`); `commits.md` gets the `refused` line |

  The sentence "No other `E-*` codes besides the rows above" (`SKILL.md:51`) is updated to name this row. A hook refusal is reported, never bypassed: no `--no-verify`, no `-n`, no `SKIP=`, no `--amend`, no `reset`, no `stash`.
- **FR-031** The Boundaries line `Auto-commit, open PRs, or release` (`implement.md:100`) becomes `Commit without the person's --commit-tasks; open PRs; push; or release`. The Completion section's optional `/sc:git` suggestion stays.
  - `implement.md` is copied byte-for-byte to `<plugin>/commands/implement.md` (parity test `test_routing_plugin_parity.py:41-47`).
  - Every changed file under `sc-implement-protocol/` is copied to `<plugin>/skills/sc-implement-protocol/`. Plugin refs are read by `tests/skills/test_implement_saved_prompt_rule.py:19` and `tests/skills/test_model_alias_policy.py:212-213`.
- **FR-032** The step's detail lives in a new ref, `<pkg>/skills/sc-implement-protocol/refs/commit-step.md` **(new)**. `SKILL.md` loads it only when `--commit-tasks` is in force, following the lazy-loading rule (developer guide `:672-687`). `SKILL.md` itself gains only the Q7b line, the Wave 0 option, the STOP row and the load rule.
- **FR-032a Managed archive.** No commit is made for the archive move. After the helper moves a package to `done/`, the new path needs `git add .dev/tasks` (`refs/managed-workspace.md:36`), and committing it is left to the person, for example with `/sc:git commit`.

## 6. Submodule operations in `/sc:git`

Root cause addressed: RC-4. The operations are defined positively and given the same authorization as other writes.

- **FR-033 `submodule status`** (read):
  - prints `git submodule status --recursive`, with the prefixes `-` (not initialized), `+` (checked-out commit differs from the index) and `U` (conflicts), and each entry's `S<c><m><u>` field from FR-005;
  - prints whether HEAD is detached, and whether HEAD is contained in any local or remote-tracking branch (`git -C <path> branch -a --contains HEAD`);
  - prints the recursion config values.

  Any `m=M` or `u=U` entry is labelled "commit inside the submodule first".
- **FR-034 `submodule update [<path>]`** (write, FR-012): runs `git submodule update --init [--recursive] -- <path>` only when the target's state is one of:
  - `-` (not initialized), or
  - `+` where the submodule HEAD is an ancestor of the recorded gitlink (`git -C <path> merge-base --is-ancestor HEAD <gitlink>`).

  In both cases the submodule must have no tracked changes and no untracked files (`m=.` and `u=.`).
  - Otherwise it refuses: `submodule-dirty` when modified; `submodule-ahead` when the recorded gitlink is an ancestor of HEAD (use `commit-pointer`); `submodule-diverged` otherwise.
  - It never passes `--remote`, `--force`, `--merge`, `--rebase` or `--checkout`.
  - It may clone or fetch from the URL in `.gitmodules`; the person's typed `/sc:git submodule update` authorizes that network read.
- **FR-035 `submodule commit-pointer <path> [--smart-commit]`** (write, FR-012) records the submodule's current HEAD as the superproject's gitlink. It requires:
  1. the superproject's preconditions of FR-015 and FR-016;
  2. the submodule has no tracked changes and no untracked files (`submodule-dirty`);
  3. the submodule HEAD is contained in at least one remote-tracking branch of the submodule (`git -C <path> branch -r --contains HEAD` is not empty), else `submodule-unpublished`, with the message "push the submodule yourself first".

     `/sc:git` never pushes. The rule exists because a pointer to an unpublished commit cannot be fetched by anyone else (`research-deep.md` §2, push ordering).

  The commit set is exactly `{<path>}`, passed with `preflight --allow-gitlink <path>`. The message is `chore(submodule): bump <path> to <short-sha>`, with a body from `git diff --submodule=log -- <path>`.
- **FR-036 Dirty or detached.**
  - A dirty submodule is never updated and never pointer-committed (FR-034, FR-035).
  - A detached submodule HEAD that equals the recorded gitlink is the normal state after `update` and needs no action.
  - A detached submodule HEAD with commits that no branch contains (`git -C <path> branch -a --contains HEAD` is empty) is a stop-and-ask case (`research-deep.md` §2). The skill runs nothing and prints the hash and the command the person may run, `git -C <path> switch -c <new-branch>`, so a later `submodule update` cannot lose those commits.
- **FR-037 Not offered**: `submodule foreach`, `sync`, `add`, `deinit`, `set-url`, `set-branch`, `absorbgitdirs` and `update --remote`. They are refused by FR-006.
  - Committing inside a submodule is the ordinary `/sc:git commit` run from the submodule's directory, under the same rules. The protected set then resolves from the submodule's own `origin/HEAD` (FR-015).
- **FR-037a Security trade-off, stated.** `/sc:git status` uses `--ignore-submodules=none`, so a submodule cannot hide its dirt through an `ignore=all` setting (`research-deep.md` §2). This deliberately differs from the sweep's `--ignore-submodules=all` (`probes.py:66`).
  - The sweep reads many worktrees unattended; `/sc:git` reads the person's own checkout at their request.
  - The `-c core.fsmonitor=false --no-optional-locks` seam is kept. Whether `-c` settings reach the child git processes that `status` starts inside submodules is UNVERIFIED, and filter drivers set only in a submodule's own config are not neutralized (risk R8).
- **FR-037b Launched sessions.** The launch-level guard denies every `git submodule` command at every level, because it is `UNKNOWN` (`launch-level-guard.sh:720`, `:724`, `:816`). The skill reports that refusal and never works around it, and the guard is not changed.

## 7. Branch cleanup reuse

- **FR-038** `/sc:git` contains no branch-deletion path. `branch -d`, `-D` and `--delete`, `push --delete`, `push origin :<branch>` and `fetch --prune` are all refused by FR-006, with the pointer to `/sc:worktrees retire|prune`.
  - `/sc:worktrees` runs `scripts/worktree_cleanup.py` (`<pkg>/commands/worktrees.md:47-55`), which deletes a local branch with `git branch -d` only (`scripts/worktree_cleanup.py:2636-2642`) and allows `git branch` only as `--show-current`, `--list <name>` or `-d <name>` (`:385-392`). Its tests forbid `--force`, `-D`, `-f` and `--delete` (`tests/worktree_cleanup/test_removal.py:209-211`).
  - `scripts/worktree_cleanup.py` and `<pkg>/commands/worktrees.md` are unchanged by this work.
- **FR-039** The residual gap is recorded, not built. PR 711 covers branches that have a worktree. It does not cover a local branch with no worktree, and it keeps squash-merged branches because `-d` refuses them, a safe false negative (`research-deep.md` §5). `/sc:git branch` shows `[gone]` upstreams as git prints them, with the note that `[gone]` is not proof of merge. No new code deletes anything.

## 8. Interaction with the worker contract and unattended mode

- **FR-040** `WORKER-CONTRACT.md:42` ("Per-task commits inside `/sc:implement` wait for issue #326 (K3) ...") is replaced by the delivered rule, which says:
  - a per-task commit falls only in Q7b, between a task's `complete` line and the next task's Q0, and never while a parallel batch has a member without `complete` or `halt`;
  - it needs the person's `--commit-tasks`;
  - `/sc:implement --commit-tasks` is refused under `--unattended`, as a stop before any work with `worker_status: failed` and the flag in `reason` (WC-4).

  The refusal binds the P4 conversion of `/sc:implement` (developer guide Archetype 3, "converted in P4"). Until then `/sc:implement` has no `--unattended`. The text keeps WC-9's existing rule "A command's own commit step stays off under `--unattended`" (`WORKER-CONTRACT.md:43`).
- **FR-041** `/sc:git` stays on the never-as-worker line (`WORKER-CONTRACT.md:23`). The brief guard's case 3 refuses it by name, and the test `test_never_as_worker_list_names_every_listed_command` (`test_worker_contract.py:912`) stays green with no change to that line.
- **FR-042** `/sc:implement` reaches the helper script directly. It never invokes `Skill sc:git-protocol` or `/sc:git`. So:
  - no command calls `/sc:git`, and there is no relay;
  - the nested propagation rule (`WORKER-CONTRACT.md:24`) is not triggered;
  - `/sc:git`'s never-as-worker status is untouched.
- **FR-043** The worker's own end-of-Task commit grant (WC-9, `WORKER-CONTRACT.md:42-43`) and the coordinator's commit rules (`:247`) are unchanged. They already use the same shape as FR-016 (`git add -- <paths>` plus `.dev/tasks`, `git commit --only -- <paths>`, never `--no-verify`), so the three paths stay consistent. Moving them onto `commit_plan.py` is a possible follow-up and is not built here.
- **FR-044** Launched sessions: the guard denies `COMMIT` at levels W, WA and F (`launch-level-guard.sh:806-808`).
  - A person who types `--commit-tasks` in such a session gets `E-COMMIT-REFUSED reason=guard` after the first `complete` task. Nothing is lost, because the task's changes stay in the working tree.
  - At level `full --submit`, `COMMIT` is allowed and the step works.
  - The issue-claim launch prompts do not add `--commit-tasks`: per-task commits are authorized only by a person's typed line.
  - `update-ref` on `refs/<name>/implement/...` is not classified as `COMMIT` (`:716` matches only `HEAD`, `--stdin` and `refs/heads/*`), so the deferred pin deletion is unaffected.

## 9. Test obligations

Tests run with `uv run pytest ...`. Static text tests pin the written contract. Script tests exercise real behaviour against temporary git repositories created under pytest's `tmp_path` (allowed by the root instructions file's internal-checkout exception for "test fixtures in a pytest temporary directory").

### 9.1 New tests

| Id | File **(new)** | Asserts | Covers |
|---|---|---|---|
| T-01 | `tests/commands/test_git_command.py` | Front matter fields; `argument-hint` declares `--smart-commit` and `--interactive`; one `## Activation` with `> Skill sc:git-protocol`; Options, STOP and Outputs sections present; no `## Unattended mode`; at most 150 lines; Boundaries name push, PR, remote and local branch deletion, `--no-verify`; no `src/<name>/` path; the two pinned example lines present | FR-001 to FR-003, FR-006 |
| T-02 | same | `<plugin>/commands/git.md` equals `<pkg>/commands/git.md` byte for byte; `commands/sc-git.md` does not exist; every other `commands/sc-*.md` still exists | FR-007, FR-008 |
| T-03 | `tests/skills/test_git_protocol.py` | `SKILL.md` at most 500 lines with the FR-004 front matter; each of the three refs exists and is named in a load rule; the never-list strings of FR-014; the plugin tree equals the src tree | FR-004, FR-007, FR-014 |
| T-04 | `tests/skills/test_git_commit_plan.py` | `preflight` returns each refusal token in FR-020 against a fixture repo built for it (detached HEAD, `master` and `integration` branches, `MERGE_HEAD` present, `index.lock` present, ignored path, `<dev>/` path, `.`/`-A`, gitlink path, `foreign-change`, `head-moved`, missing pin) and `ok` otherwise | FR-020, FR-026, FR-027 |
| T-05 | same | `verify` returns `committed`, `empty`, `hook-failed` (a `pre-commit` hook that exits 1), `hook-rewrite` (a hook that edits a file and exits 1), `hook-rewrite-committed` (a hook that edits and re-adds), and `recovered` (a commit with the trailers and no record) | FR-021, FR-029 |
| T-06 | same | The script's runner refuses any verb outside the FR-019 allow-list, and a monkeypatched call to `commit`, `push`, `reset`, `branch -d` or `update-ref` raises. Pattern from `tests/worktree_cleanup/test_removal.py:209-211` | FR-019, NFR-005 |
| T-07 | `tests/skills/test_implement_commit_step.py` | `SKILL.md` places `Q7b COMMIT` after `Q7 GATE` and before `Q8 NEXT`; the Wave 0 option list contains `--commit-tasks`; the STOP table has the `E-COMMIT-REFUSED` row and the updated "No other" sentence; `refs/commit-step.md` states: one commit per batch only after every member is `complete`, no commit when any member halted, the literal `git add -- ` and `git commit --only -F ` forms, the forbidden `--no-verify`, `-n`, `SKIP=`, `--amend`, `reset`, `stash` tokens, the pin-deferral and resume-row clauses | FR-022 to FR-032 |
| T-08 | same | A two-task scenario with a real temporary repo, driving the script (not the agent): T1's commit succeeds; T2's commit with a failing hook yields `hook-failed`, the `commits.md` line and HEAD unchanged; the person's pre-existing edit to a T2 path yields `foreign-change` | FR-024 to FR-030 |
| T-09 | `tests/skills/test_git_submodule_rules.py` | Fixture superproject with a local submodule (`protocol.file.allow=always` set only inside the fixture): `status` labels `S.M.` as "commit inside the submodule first"; `update` refuses `submodule-dirty`, `submodule-ahead` and `submodule-diverged`; `commit-pointer` refuses `submodule-unpublished` and commits exactly one gitlink path when published | FR-033 to FR-036 |

### 9.2 Existing tests that must be updated and stay green

| File | Change |
|---|---|
| `tests/recommend/fixtures/routing_refresh_cases.json` (S23, line 325) | Activation `self-contained` → `sc:git-protocol` (FR-010) |
| `tests/skills/test_worker_contract.py` (classification table near `:2945`; tests `:3223`, `:3227`) | Add a row for every new `WRITE_VERB_RE` hit; remove stale rows (FR-010) |
| `tests/commands/test_routing_plugin_parity.py:41` and `<pkg>/commands/README.md:9` | Add `git` (FR-007) |
| `tests/skills/` tests that pin the implement STOP table or option list (candidates found by Grep: `test_task_workspace_lifecycle.py`, `test_implement_severity_static.py`, `test_implement_saved_prompt_rule.py`; which assertions are exact is UNVERIFIED) | Accept the new row and option (FR-030) |
| `tests/core/test_how_we_work_routing_table.py:29` and the plugin guide copy tests | Stay green after the FR-009 row edit |
| `tests/skills/test_primitive_dual_surface_lookup.py` | Unchanged and green (NFR-001) |
| `tests/worktree_cleanup/` | Unchanged and green (FR-038) |

## 10. Risks and mitigations

| Id | Risk | Root cause | Mitigation | Residual |
|---|---|---|---|---|
| R1 | An agent in an ordinary session bypasses hooks (`--no-verify`, `-n`, `SKIP=`) despite the text | RC-2: no mechanical gate outside launched sessions (`launch-level-guard.sh:5-7`; no deny rule in `<dev>/settings.json`) | Exact-argv rule (FR-016), never-list (FR-014), static tests (T-07). The guard's `TAMPER` class already covers launched sessions (`launch-level-guard.sh:786`) | Medium. Recommended follow-up: a deny rule for `git commit` with `--no-verify`/`-n` in every session (not built) |
| R2 | A wrapper script hides the commit from the launch-level guard | `LL_GIT` is set only from the command text (`:555-557`) | The script is read-only (FR-019, T-06); the commit is a literal Bash call (FR-016) | Low |
| R3 | A formatting hook rewrites files after QA, so unreviewed content is committed | `markdownlint --fix`, `ruff-format` and `mixed-line-ending --fix=lf` rewrite files (`.pre-commit-config.yaml:34-35`, `:86-91`, `:130-134`) | `verify` compares against `pre_tree` (FR-021); `hook-rewrite*` stops the run (FR-030); a retry needs a fresh `--commit-tasks` | Low |
| R4 | The person's pending edits are swept into a task's commit | Q0 snapshots the dirty tree (`SKILL.md:123-124`) | `foreign-change` (FR-027) | Low |
| R5 | A batch commit moves HEAD under a sibling, causing `head-moved` | Shared `q0-head` | One commit per batch after all members complete; none if any halt (FR-025) | Low |
| R6 | A session dies between the commit and the record, and the commit is repeated or lost | Record written after the commit | Trailers plus `verify` recover mode (FR-021, FR-029) | Low |
| R7 | Test churn from pinned fixtures | RC-1, RC-6 | Enumerated in 9.2; example lines kept verbatim (FR-002) | Low |
| R8 | `status --ignore-submodules=none` runs a program configured inside a submodule | The sweep's issue-547 rationale (`probes.py:66`) | fsmonitor off, `--no-optional-locks`, person-invoked only (FR-037a) | Medium, UNVERIFIED for submodule-local filter drivers |
| R9 | Plugin-only or partial installs lack the helper | Cross-skill dependency | `helper-missing` refusal before any write (FR-023); skill mirrored to `<plugin>` (FR-007) | Low |
| R10 | Future contributors follow the foreign standards document | RC-5 | Declared non-normative here (section 11); follow-up recorded | Medium until that doc is fixed |
| R11 | Commit-message hook not installed locally, so formats go unchecked | The common git dir here has `pre-push` and `pre-push.launch-level` but no `pre-commit` hook (runtime check, 2026-11-26) | `preflight` validates the header itself (FR-028) | Low |
| R12 | `.dev/tasks` brings other packages' changes into a task commit | Repo rule includes the whole directory (`WORKER-CONTRACT.md:247`) | Accepted and consistent with the coordinator rule; the report lists every `.dev/tasks` path committed | Low |
| R13 | A rename lists only the new path, so the deletion of the old path stays uncommitted | `files=` content is agent-written | `verify` prints the dirty paths left behind (FR-021) | Low |

## 11. Decisions on the seed brief's open questions

- **Q1. Structure.** Decision: a command file plus the protocol skill `sc-git-protocol` with three refs (commit, branch, submodule) and one read-only script.
  - Why:
    - the developer guide's three-tier rule (`:53`, `:59`, `:63-75`) and its size limits (command about 80-150 lines; `SKILL.md` up to about 500 lines, `:678`) cannot hold twelve operations with authorization classes, merge preview and submodule rules in one command file;
    - lazy refs keep a read-only `status` cheap (`:672-687`);
    - a command-only layout fits `/sc:worktrees`, which runs one script (`worktrees.md:55`, "No skill is activated"), but `/sc:git` needs per-operation protocol.
  - Cost: S23 changes and the skill must be mirrored to `<plugin>`.
  - Front matter: keep `category: utility`, because no code reads `category` and `help.md` uses the same value; set `complexity: standard`.
- **Q2. How `/sc:implement` calls the commit step.** Decision: a shared read-only script (`commit_plan.py preflight|verify`) inside `sc-git-protocol`, plus the literal `git add` and `git commit` run by the implement protocol in a new `Q7b` step outside the task body.
  - Rejected options:
    - inline duplicated text would make two copies of the safety checks, the drift pattern of RC-6;
    - a script that commits would hide the commit from the guard (R2);
    - a Skill call to `/sc:git` would reintroduce a relay and touch the never-as-worker status.
  - The HEAD-still rule is respected because Q7b runs after `complete` and before the next Q0 (FR-024).
- **Q3. Authorization switch.** Decision: the per-invocation flag `--commit-tasks` on `/sc:implement`, honoured only as a standalone token in the person's own message that starts with `/sc:implement`, and refused under `--unattended`.
  - A plan-level field is rejected for two reasons. It is written by an agent (`/sc:workflow`), which the worker contract calls "executor-invented approval" when no person confirmed it (`WORKER-CONTRACT.md:57`). And a managed plan is hash-pinned after its first `start`, so the field could not be changed later (`refs/managed-workspace.md:44`).
  - A free-form session instruction is rejected because it cannot be tested, does not survive compaction or resume, and is the ambiguity behind the "Do it and let me review" incident (`research-deep.md` §1).
- **Q4. Submodule operations and dirty/detached states.** Decision: `submodule status` (read), `submodule update` (write, only from `-` or a fast-forwardable `+`, clean submodule only) and `submodule commit-pointer` (write, clean and published HEAD only).
  - A dirty submodule refuses. A detached HEAD with commits no branch contains is stop-and-ask, with the branch-create command printed.
  - No `--remote`, no push, no `foreach`/`sync`/`add`/`deinit`. Launched sessions stay denied by the guard (FR-033 to FR-037b).
- **Q5. `commands/sc-git.md`.** Decision: remove that one file.
  - Why: it is never packaged or installed (`pyproject.toml:78-97`), nothing references it (Grep for `commands/sc-[a-z]` finds only `tests/commands/test_help_text_fixes.py`, which names three other legacy files, and one design doc), and its prefix is wrong.
  - Fixing it would keep a fifth copy alive with no parity check. The rest of `commands/` stays, and a follow-up is recorded.
- **Q6. Residual "project management" scope.** Decision: none.
  - Why:
    - `/sc:closeout` settles a merged PR, its issue, the work report entry and the Orca task;
    - `/sc:issue` claims and creates issues;
    - `<name> issue-pipeline complete` posts one result comment per run (`WORKER-CONTRACT.md:302`);
    - progress posts are coordinator-owned outward actions (`WORKER-CONTRACT.md:244`).
  - Adding status posting to `/sc:git` would contradict "Do not append push, merge or PR creation" (`HOW-WE-WORK.md:293`).
- **Additional decision D-7. Standards source.** Decision: `/sc:git` follows the enforced gates, which are `.pre-commit-config.yaml`, `.github/rulesets/`, `docs/developer-guide/branch-protection.md` and the routing guide. `docs/developer-guide/git-standards-protocols.md` is declared non-normative for this work (RC-5).

## 12. Non-functional requirements

- **NFR-001** No installed primitive (command, skill, ref or script text under `<pkg>/{commands,skills,agents,core,hooks}`) tells an agent to read or run another primitive through a `src/<name>/` path.
  - The implement protocol names the helper by its installed path `<home>/skills/sc-git-protocol/scripts/commit_plan.py`, then the project dev copy (root instructions file, "Never Hardcode" rule; developer guide `:98-115`).
  - Check: `grep -rn 'src/<name>' <pkg>/{commands,skills,agents,core,hooks}` gains no new unjustified hit.
- **NFR-002** Size limits:
  - `<pkg>/commands/git.md` at most 150 lines;
  - `sc-git-protocol/SKILL.md` at most 500 lines;
  - each `sc-git-protocol/refs/*.md` and `refs/commit-step.md` at most 250 lines;
  - `sc-implement-protocol/SKILL.md` grows by at most 15 lines.
- **NFR-003** `commit_plan.py`:
  - standard library only, on Python 3.10 or later (`pyproject.toml`);
  - no network, writes nothing in the repository;
  - each git call has a 10-second timeout;
  - exactly one JSON object on stdout; exit 0 for `ok` or a classification, non-zero only for `helper-error`.
- **NFR-004** Determinism: refusal and classification tokens are closed lists (FR-020, FR-021, FR-030), and the same repository state gives the same JSON.
- **NFR-005** No history rewrite: nothing in this work runs `reset`, `rebase`, `--amend`, a force push or `update-ref` on `refs/heads/*`. Each commit point adds at most one commit.
- **NFR-006** `.dev/tasks` is included in every commit set when it exists. `<dev>/` paths other than `settings.json` are never staged, and `-f` is never used on `add`.
- **NFR-007** Fail closed: a missing helper, unparseable helper output, a missing pin or `q0-head`, or an unknown token gives a refusal, never a commit.
- **NFR-008** Sync: `make verify-sync` exits 0, and the parity tests in 9.2 pass.
- **NFR-009** Git floor: `merge` preview needs git 2.38 or later (`git-too-old` refusal otherwise). Status, add and commit work on the version the repository already uses (2.47.3 here).
- **NFR-010** Cost: one commit point adds four Bash calls (preflight, add, commit, verify). A run without `--commit-tasks` adds no call and no file.
- **NFR-011** Context: a `/sc:git` invocation loads at most one ref, and `/sc:implement` loads `refs/commit-step.md` only under `--commit-tasks`.

## 13. Acceptance criteria

Each criterion is a command or an observation with a pass condition.

- **AC-01** `grep -c '^## Activation' <pkg>/commands/git.md` prints `1`, and `grep -c '^> Skill sc:git-protocol$' <pkg>/commands/git.md` prints `1`. `grep -c '^## Unattended mode' <pkg>/commands/git.md` prints `0`. `wc -l < <pkg>/commands/git.md` is 150 or less.
- **AC-02** `test -f <pkg>/skills/sc-git-protocol/SKILL.md` and the three refs and `scripts/commit_plan.py` exist. `wc -l < .../SKILL.md` is 500 or less.
- **AC-03** `cmp <pkg>/commands/git.md <plugin>/commands/git.md` and `diff -r -x __init__.py -x __pycache__ <pkg>/skills/sc-git-protocol <plugin>/skills/sc-git-protocol` both print nothing. `cmp <pkg>/commands/implement.md <plugin>/commands/implement.md` prints nothing.
- **AC-04** `git ls-files commands/sc-git.md` prints nothing, and `git ls-files commands/ | wc -l` prints `20`.
- **AC-05** `make verify-sync` exits 0. `git status --porcelain -- <dev>` shows no staged path other than `settings.json`.
- **AC-06** `uv run pytest tests/commands tests/skills tests/recommend tests/core tests/worktree_cleanup -q` passes, including T-01 to T-09.
- **AC-07** `git diff --quiet origin/integration -- scripts/worktree_cleanup.py <pkg>/commands/worktrees.md <pkg>/hooks/scripts/launch-level-guard.sh` exits 0.
- **AC-08** `grep -rnE 'branch +-D|branch +--delete|push +--delete|push +origin +:' <pkg>/skills/sc-git-protocol <pkg>/skills/sc-implement-protocol` finds hits only on lines that state a refusal (each is classified `read-only` or `never-worker` in the worker-contract table).
- **AC-09** In a fixture repo, two tasks run with `--commit-tasks`, driven through the protocol's documented script calls. The result is exactly two new commits whose headers match FR-028's regex and whose trailers name the plan and task. `commits.md` has two `commit sha=` lines. No `refs/<name>/implement/<slug>/T*` pin remains.
- **AC-10** In the same fixture with a failing `pre-commit` hook, the second commit point leaves HEAD at the first commit, appends `commit refused reason=hook-failed` and stops with `E-COMMIT-REFUSED`. The task's ledger line stays `complete`.
- **AC-11** `/sc:implement` without `--commit-tasks` on any fixture makes zero commits and writes no `commits.md`, which is today's behaviour.
- **AC-12** The never-as-worker line of `<pkg>/core/WORKER-CONTRACT.md` still contains `` `/sc:git` ``. Line 42's K3 sentence is replaced by the delivered rule from FR-040.
- **AC-13** The `/sc:git` row of `<pkg>/core/HOW-WE-WORK.md` contains the three phrases from FR-009, and `cmp <pkg>/core/HOW-WE-WORK.md <plugin>/skills/sc-recommend/refs/HOW-WE-WORK.md` prints nothing.
- **AC-14** `/sc:git submodule commit-pointer` on a fixture submodule whose HEAD is in no remote-tracking branch prints `submodule-unpublished` and makes no commit. On a published HEAD it makes one commit whose only path is the gitlink.
- **AC-15** No new hit under `<pkg>/{commands,skills,agents,core,hooks}` names a `src/<name>/` path, beyond the existing justified ones (NFR-001).
