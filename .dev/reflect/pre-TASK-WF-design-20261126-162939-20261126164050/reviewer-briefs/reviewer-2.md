# Reviewer brief 2 (qa)

## T1 card excerpt

## Scope and what was read

The plan has 8 phases and 38 tasks (`TASK-WF-design-20261126-162939.md:32` onward). Lines 1-150 (constitution, Phases 1 to 4 up to Task 11) were read line by line. Tasks 12 to 38 were checked structurally only (plan gate, a dependency-order script, design-term counts), not read line by line. The design (`source.md`, 529 lines) was read by section heading and by targeted Grep.

## Coverage map (Step 1B.0)

- Pass 1 (`ID_REGEX`, parsed): the only family it matches in the design is `T-nn` (the design's test ids): 27 distinct, 25 named somewhere in the plan, 2 not named (`T-14` at `source.md:407`, `T-18` at `source.md:458`). `coverage_pct` = 25/27 = 0.9259.
- Pass 2 (inferred rows): the design's own label families that `ID_REGEX` does not match: FR (122 distinct), NFR (18), DD (11), AC (21). Each row quotes the first design line that carries the id (`artifacts/coverage-pass1.json`). Ranges such as `FR-060..FR-063` were expanded. DD: 11 of 11 named in the plan. FR: 79 of 122. NFR: 10 of 18. AC: 7 of 21.
- Union: 132 of 199 ids are named in the plan text, `coverage_pct_union` = 0.6633, 67 unmapped. `inferred_count` (172) is larger than `parsed_count` (27), so the parse-density guard fires: `coverage_degraded: parsed-sparse`.
- Reading of the gap: most unmapped ids are cited only inside the design's summary rows (`source.md:15-19`, one row per component C1 to C5), the P7 row (`source.md:473`) and the traceability table (`source.md:517`). A term check of the design's mechanisms against the plan found every major mechanism named in the plan (Q8a, R0, L0, commits.md, stage-plan, check-message, resolve-check, reconcile, snapshot, abandon, adopt, vcs_contract, E-RESUME-NEEDED, S23, sync-dev, DD-9, DD-10, DD-11). So the id gap is mostly "the plan does not cite the id", and only a semantic read of each design section can say whether any requirement has no task. That read is left to Tier 2.

## Recommendations

1. Edit `TASK-WF-design-20261126-162939.md:29` as in F1; success check: no sentence in the plan forbids text that Tasks 3, 14 and 16 must write.
2. Add `Task 4` to the `Depends on:` lines of Tasks 9 to 12 and `Task 4`, `Task 5` to Tasks 6 and 8; success check: `artifacts/dependency-check.txt` rerun shows no `NO-DEP-ON-CREATOR` row for `vcs_plan.py` or `vcs.py`.
3. Tier 2 should read each design section against the tasks (the qa reviewer has the whole design in its brief).

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-26T16:32:04Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-326 projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-326

### .dev/tasks/to-do/TASK-WF-design-20261126-162939/TASK-WF-design-20261126-162939.md:1-30

`````markdown
---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: deep
slug: TASK-WF-design-20261126-162939
version: "1"
priority: Medium
created_date: "2026-11-26"
---

# Implement the modular /sc:git, authorized between-task commits in /sc:implement, and submodule operations (issue 326)

Source: ./source.md
Goal: Deliver the design in ./source.md: a refactored `/sc:git` (command file, protocol skill, read-only `vcs` helper script) with defined submodule operations, and an opt-in `--commit-tasks` commit step in `/sc:implement` with crash recovery, protection of work outside the commit set and owner resolution, plus the routing, worker-contract, plugin-mirror, documentation and test changes around them.

## Constraints

- Requirement ids (FR-xxx, NFR-xxx, AC-xx, T-xx, D1-D11) and the decisions DD-1 to DD-11 are defined in ./source.md (the design) and, in full wording, in the merged requirements at .dev/brainstorms/20261126-115614-git-pm-workflows-skills/merged-requirements.md. A task that needs exact wording (a regex, a refusal text, a line form) reads the cited FR in that file. Where the design adds a decision (DD-n), the design wins.
- Decided scope: the narrowed scope of 2 November is confirmed; the local branch cleanup that PR 711 delivered (`scripts/worktree_cleanup.py`, `_remove_branch` at line 2636, and the `/sc:worktrees` command) is reused and stays unchanged; nothing in this work deletes a remote branch or any local branch.
- Out of scope: a relay through which every command calls `/sc:git`; push, pull, merge, rebase or PR creation in `/sc:git`; nested submodules; new project-management workflows; any change to the level table in `src/superclaude/core/HOW-WE-WORK.md`; any change to `src/superclaude/skills/sc-implement-protocol/scripts/archive_workspace.py` or to the task-ledger grammar.
- `/sc:git` never pushes, merges, fetches on its own or opens a PR. The one exception is `submodule update`, which may clone or fetch from the `.gitmodules` URL on the person's typed, disclosed line (FR-044, NFR-001). PRs stay with `/sc:pr-submit`.
- The `vcs` helper is read-only: it writes no ref, user index, work-tree file or config, and runs git only through one runner with an allow-list. Every repository write is a visible call the agent makes (FR-011, NFR-002).
- Installed primitives (files under `src/superclaude/commands`, `skills`, `agents`, `core`, `hooks`, `templates` and their `plugins/superclaude/` copies) never name a `src/superclaude/...` path: they use `~/.claude/...` with the project copy made by `make sync-dev` as the fallback (FR-009, NFR-010). Edit `src/superclaude/` first, run `make sync-dev`, and keep the `plugins/superclaude/` copies byte-identical. Never stage any file under the project agent-host folder `.claude/` other than its `settings.json`.
- Python runs through UV: `uv run pytest ...` and `uv run --no-project python <script>`. The helper uses the Python standard library only (Python 3.10 or later).
- The write-verb scan in `tests/skills/test_worker_contract.py` (`WRITE_VERB_RE` at line 1894, `_scan_write_verbs` at line 1927, `WRITE_VERB_CLASSIFICATION` keyed by file, verb and exact stripped line) covers every file under `src/superclaude/skills`, `commands` and `agents`, scripts included, and also fails on stale rows. Any task that adds or edits a line containing `git add`, `git commit`, `git update-ref`, `git push`, `git merge` or `git stash` updates the classification rows in the same task (category `never-worker` for `/sc:git` files, `deferred:P4` for the implement commit-step lines). Helper Python builds argv lists, so it avoids those literal phrases.
- Behavior changes ship with tests. New behavior and helper tests live under `tests/vcs/` (real temporary repositories); static text pins live under `tests/skills/` and `tests/commands/`; real-framework hook tests are marked and skipped when `pre-commit` is not installed (DD-7).
- UNVERIFIED items stay marked UNVERIFIED in the code, docs and tests that depend on them (git version floor for `--pathspec-from-file`, real hook-framework behavior, `file://` submodule tests on CI, `-c core.fsmonitor=false` coverage, the 5-second latency target of NFR-008 which has no baseline); a task never turns one into a stated fact without a passing test.
- Nothing in this work runs `reset`, `rebase`, `--amend`, a force push, or `update-ref` on `refs/heads/*`; each boundary adds at most one commit (NFR-017). No code or text uses `--no-verify`, `-n` on commit, `SKIP=`, `commit-tree` or `--amend`.
- The minor wording and placement notes the merge left open (M3-2, M3-3, M3-7, M3-9 and parts of M3-4 and M3-6) are listed in `.dev/brainstorms/20261126-115614-git-pm-workflows-skills/adversarial/adversarial/merge-log.md`; a task that writes a ref re-reads them first. If the pull request touches a gate or validator file, its body needs a `## Generator-Constraint Considered` section (a CI check; which files it covers is UNVERIFIED).
`````

### .dev/tasks/to-do/TASK-WF-design-20261126-162939/source.md:1-8

`````markdown
# Design: Modular `/sc:git`, Authorized Between-Task Commits in `/sc:implement`, and Submodule Operations (issue 326)

- Command: `/sc:design .dev/brainstorms/20261126-115614-git-pm-workflows-skills/merged-requirements.md --type component --format spec --output .dev/brainstorms/20261126-115614-git-pm-workflows-skills/design.md`
- Date: 2026-11-26. Issue: https://github.com/IronbellyOrg/IronClaude/issues/326. Base branch: `integration`.
- Input: `merged-requirements.md` (the adversarially merged requirements; convergence 1.0, 3 debate rounds, 39 planned merge changes applied). Its ids (FR-xxx, NFR-xxx, AC-xx, T-xx, D1-D11) are used here unchanged, so every design element traces to a requirement.
- Decided scope (from `.dev/issues/326/issue-summary.md`, "Decided for this work (iteration 3)"): confirm the narrowed scope of 2 November; reuse the local branch cleanup that PR 711 delivered (do not rebuild it); no remote branch deletion.
- Grounding: index_state: fresh (tools used: `codegraph_status`, `codegraph_search`, `codegraph_node` with `symbolsOnly:true`); checked_at=2026-11-26T16:22:17Z; worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-326. Graph rows only located code; every file:line cited below was read with Read or Grep in this run (section 11 lists them). Nothing was run or built: this document designs, it does not implement.

`````

### .dev/tasks/to-do/TASK-WF-design-20261126-162939/source.md:9-41

`````markdown
## 1. Design summary

Four deliverables, built as five components (C1 to C5):

| # | Component | What it is | Requirements |
|---|---|---|---|
| C1 | `/sc:git` command + `sc-git-protocol` skill | A thin command file, a protocol skill with an operation registry and five refs loaded on demand | §2 and §3, §4, §5 (FR-001..FR-046) |
| C2 | `vcs` helper (skill script) | Read-only Python that computes facts and plans (seven verbs, JSON out). It never writes the repository | FR-010..FR-013, FR-060..FR-063, FR-106, FR-123, FR-130, NFR-006..NFR-009 |
| C3 | Commit step in `sc-implement-protocol` | New flag `--commit-tasks`, a new ref `refs/commit-step.md`, three commit positions (Q8a, R0, L0), a sidecar `commits.md` and a boundary state machine | §6, §7.1, §7.2, §7.5 (FR-050..FR-079, FR-100..FR-109, FR-130..FR-133) |
| C4 | Worktree protection and owner resolution | Snapshot before and compare after every commit attempt; `abandon` / `adopt` answers that settle a boundary that cannot be proven | §7.3, §7.4 (FR-110..FR-126) |
| C5 | Surrounding surfaces | Routing row, fixture S23, worker contract, plugin mirror, retired legacy copy, tests, sync steps | §2.4, §2.5, §8, §9, §10 (FR-014..FR-017, FR-080..FR-094) |

What this design does **not** build (decided): a relay through which every command calls `/sc:git`; push, pull, merge, rebase or PR creation in `/sc:git`; remote branch deletion; a second implementation of local branch cleanup; nested submodules; new project-management workflows (D6).

### 1.1 Notation: spec placeholders and their real values

The requirements avoid some words by using placeholders. This design is a development document, so it uses the real values. Each value was checked in this worktree (see §11).

| Spec placeholder | Real value in this repository |
|---|---|
| `<package>` | `superclaude` |
| `<pkg>` | `src/superclaude/` |
| `<plugin>` | `plugins/superclaude/` |
| `<cli>` | `superclaude` (console command, `pyproject.toml` `[project.scripts]`) |
| `<home>` | `~/.claude/` (installed copies: `~/.claude/commands/sc/`, `~/.claude/skills/`) |
| `<dev>` | `.claude/` (gitignored sync-dev copies; only `settings.json` may be staged) |
| `<skill-dir>` | `~/.claude/skills/sc-git-protocol/`, then `.claude/skills/sc-git-protocol/` |
| `<pkg-dir>`, `<run-dir>` | the managed task package `.dev/tasks/to-do/<slug>/` (later `done/<slug>/`); the legacy run folder `.dev/implement/<slug>/` |
| pin refs `refs/<package>/implement/<slug>/...` | `refs/superclaude/implement/<slug>/...` (the existing Q0 pin is `refs/superclaude/implement/<slug>/T<id>`, `SKILL.md:126`) |
| pin refs `refs/<package>/git/...` | `refs/superclaude/git/...` |

Rule that still holds for every installed primitive: no file under `src/superclaude/{commands,skills,agents,core,hooks,templates}` or its `plugins/superclaude/` mirror may name a `src/superclaude/...` path (project rule; FR-009, NFR-010). Primitives name `~/.claude/...` with `.claude/...` as the project fallback. This document is not a primitive, so it may name `src/` paths.

`````

### .dev/tasks/to-do/TASK-WF-design-20261126-162939/source.md:42-105

`````markdown
## 2. Architecture

### 2.1 Components and data flow

```
                          person types a line
                                  |
              +-------------------+--------------------+
              |                                        |
     /sc:git <operation>                     /sc:implement <src> --commit-tasks
              |                                        |
   commands/git.md  (parse, STOP, activate)    commands/implement.md (option, STOP)
              |                                        |
   skills/sc-git-protocol/SKILL.md             skills/sc-implement-protocol/SKILL.md
     registry -> one ref + safety.md                    |  Wave 0: preflight(5b) -> ledger(6) -> run line -> reconcile
              |                                         |  Loop:   Q0..Q7 -> Q8a COMMIT STEP -> Q8
              |                                         |  also:   R0 (resume), L0 (before FINAL)
              |                                  refs/commit-step.md  (commit procedure + reconcile/settle)
              |                                         |
              +----------------+------------------------+
                               |  both call, never invoke each other
                               v
              skills/sc-git-protocol/scripts/vcs.py   (READ-ONLY helper, JSON in/out)
                 vcs_rules.py  vcs_plan.py  vcs_submodules.py
                               |
                               v   one runner: git --no-optional-locks -c core.fsmonitor=false <allow-listed verb>
                             git (repository)

   Every WRITE (git add, git commit, git switch, git update-ref, git submodule update, file writes
   to commits.md / the ledger) is a visible Bash or Write call made by the AGENT, so the host's
   hooks (launch-level guard, deny rules, pre-commit) always see it.
```

### 2.2 Invariants the design must keep (each is tested)

| # | Invariant | Held by |
|---|---|---|
| I1 | HEAD equals `q0-head` for every open or halted task (retry check 3, `refs/retry.md:41`; coordinator resume check, `WORKER-CONTRACT.md:280`) | FR-056, FR-059, FR-077 (commit only when no task is open) |
| I2 | The task-ledger grammar, `E-LEDGER-CORRUPT` and `archive_workspace.py` do not change | State lives in a sidecar `commits.md` (FR-100, D9) |
| I3 | The helper writes no ref, user index, work-tree file or config; the agent runs every write visibly | FR-011, NFR-002, T-03 |
| I4 | A commit happens only on the person's own typed line | FR-020, FR-050, FR-122 |
| I5 | Settle before advance: no new task, all-complete return, FINAL or archive while a boundary is unsettled | FR-077, FR-107, FR-070 (archive gate) |
| I6 | Fail closed: a missing helper, pin, `q0-head`, or an unknown token refuses, never commits | NFR-016 |
| I7 | One writer per ledger and `commits.md` | FR-133 (stated residual, no lock) |
| I8 | At most one commit per boundary key, across crashes and resumes | FR-108, FR-130, T-22 |
| I9 | `/sc:git` never pushes, merges, fetches on its own or opens a PR; the one clone/fetch exception is `submodule update` on a typed, disclosed line | FR-004, FR-005, FR-044, NFR-001 |

### 2.3 Decisions this design adds to the requirements

The requirements leave these open. Each is a design decision (DD) that the plan and tests must follow.

| DD | Decision | Why |
|---|---|---|
| DD-1 | The boundary key's "ledger identity" is the token `managed:<slug>` or `legacy:<slug>` (the pin-id slug), never a file path | A managed package moves from `to-do/` to `done/` at archive; a path-based key would change after archive and break recovery of an archived package. `refs/managed-workspace.md:32` already says "No lookup hashes a plan path (the package moves)" |
| DD-2 | The helper is one entry script plus three sibling modules, run as `uv run --no-project python <skill-dir>/scripts/vcs.py <verb>`. Tests load modules with `sys.path.insert` of the scripts folder; the byte-parity test compares the source and plugin folders | The precedent `tests/skills/test_workflow_archive.py` loads a script by path and asserts byte parity with `plugins/superclaude/` |
| DD-3 | All helper JSON goes through one `emit(obj)` function that sorts keys, drops no field, caps lists at 200 with `truncated`, and refuses output above 64 KiB (NFR-006, NFR-007) | One place enforces determinism and the cap; S is never capped, so the full path list goes to the pathspec file, not the JSON |
| DD-4 | Commit message text is written by the agent to a temporary file outside the work tree (`message_path` from `stage-plan`); the helper validates it with `check-message` and never writes it | Keeps I3 and lets the guard see a normal `git commit -F` |
| DD-5 | The reconcile result is a JSON list of boundaries with a fixed state vocabulary (`due`, `pending`, `refused`, `uncertain`, `settled`, `out-of-protocol`) and one `action` per boundary from a closed list; the agent only performs the named action | Makes the FR-107 table testable as a pure function: `(ledger, commits.md, flag, git facts) -> actions` |
| DD-6 | The `run` line field `args=` records the option prefix only, never source text, and `source=` is a path or `inline:<hash8>` (FR-101) | Keeps secrets in inline prompts out of `commits.md` |
| DD-7 | New tests live under `tests/vcs/` (helper and git behavior, real temporary repositories) and `tests/skills/`, `tests/commands/` (static text checks). Real-framework hook tests are marked and skipped when `pre-commit` is not installed | Matches the existing split between behavior tests and static text pins |
| DD-8 | The helper's ledger reader reuses the exact line regexes of `archive_workspace.py` (`_START`, `_VERDICT`, `_RULING`, `_RETRY`, `_HALT`, `_PLAN`, `_FINAL`), copied into `vcs_plan.py`, and a parity test loads both files and asserts the patterns are equal | Two readers of one closed grammar must not drift; the archive helper is deliberately unchanged (I2) |
| DD-9 | The runner allow-list is a table `verb -> permitted option tokens` in `vcs_rules.py`, not a list of verbs; an option outside the table is rejected before execution. Containment uses `for-each-ref --contains <sha> <refs...>` (a permitted verb) instead of `branch --contains`, so one code path covers local and remote-tracking refs | FR-011 names verbs; a verb alone does not stop `branch -D` or `config --unset`, and `branch -r --contains` cannot see local branches |
| DD-10 | Reading git config uses `config --get` and `config --get-regexp` only (same read-only family). `--get-regexp '^filter\.'` is the lossless-snapshot check input (FR-112, `snapshot-unsupported`) | FR-011 lists `config --get`; the snapshot check needs the regexp form. The plan must add it to the allow-list test (T-03) |

`````

### .dev/tasks/to-do/TASK-WF-design-20261126-162939/source.md:106-168

`````markdown
## 3. Component C1: `/sc:git` command and `sc-git-protocol` skill

### 3.1 Files

```
src/superclaude/commands/git.md                          rewritten (<= 150 lines, NFR-012)
src/superclaude/skills/sc-git-protocol/SKILL.md          new (<= 500 lines)
src/superclaude/skills/sc-git-protocol/refs/safety.md    forbidden ops/flags, path rules, protected branches, hook refusal, message format, FR-110..FR-117 (git side)
src/superclaude/skills/sc-git-protocol/refs/status.md    status, branch list reports
src/superclaude/skills/sc-git-protocol/refs/commit.md    add, commit (FR-031..FR-039)
src/superclaude/skills/sc-git-protocol/refs/branch.md    branch create, switch, cleanup (routing only)
src/superclaude/skills/sc-git-protocol/refs/submodule.md submodule status, update, commit-pointer (FR-040..FR-046)
src/superclaude/skills/sc-git-protocol/scripts/          vcs.py, vcs_rules.py, vcs_plan.py, vcs_submodules.py (C2)
plugins/superclaude/commands/git.md                      byte copy of the source
plugins/superclaude/skills/sc-git-protocol/**            byte copy of the source folder
commands/sc-git.md                                       deleted (D5, FR-014)
```

The skill name ends in `-protocol`, which is the rule `install_skills` uses to install a skill standalone (`src/superclaude/cli/install_skills.py:47-59`; to be re-read when the plan reaches the install step).

### 3.2 Command file shape (`git.md`)

Front matter: `name: git`, a one-line `description`, `category: version-control`, `complexity: moderate`, `mcp-servers: []`, `personas: []`, `argument-hint` listing exactly the FR-002 operations (FR-001). Sections in this order (FR-003): Triggers, Usage, Options, STOP rules (checked before Activation), Behavioral Flow (parse, STOP, hand off, print), Activation (one line `> Skill sc:git-protocol` and the installed path `~/.claude/skills/sc-git-protocol/SKILL.md`), Examples, Outputs, Boundaries, Related Commands. No `## Unattended mode` (FR-090: the brief guard then refuses it under case 3, `WORKER-CONTRACT.md:23`).

STOP rules table (FR-004), all print the usage block and run nothing: unknown operation; `push`, `pull`, `fetch`, `merge`, `rebase`, `reset`, `clean`, `stash`, `tag`, `pr` as the operation (the message names `/sc:pr-submit` for push and PR); `commit` or `commit-pointer` with neither or both of `--message` and `--smart-commit`; `create` or `switch` without a name; any token in `FORBIDDEN_FLAGS`; `--unattended`; not inside a git work tree. A bare `/sc:git` runs `status`.

### 3.3 Protocol skill (`SKILL.md`)

Front matter `name: sc:git-protocol`, `description`, `allowed-tools: Read, Write, Bash` (not treated as a security boundary: risk 14). Body order: purpose; the person-line authorization rule; the **operation registry**; the per-invocation flow; the report format; the refusal and STOP token catalog; the "Adding an operation" checklist (FR-008).

Operation registry (single list of what `/sc:git` can do; FR-006):

| Operation | Class | Authorizing prefix of the person's current message (FR-020) | Refs loaded (FR-018) | Helper verbs |
|---|---|---|---|---|
| `status` | read | any `/sc:git` line | `status.md` | `preflight`, `submodules` |
| `branch list` | read | any `/sc:git` line | `status.md` | `preflight` |
| `branch cleanup` | read (route only) | any `/sc:git` line | `branch.md` | none |
| `submodule status` | read | any `/sc:git` line | `submodule.md` | `submodules` |
| `add <path>...` | index | `/sc:git add` | `commit.md`, `safety.md` | `preflight`, `stage-plan` |
| `commit [<path>...]` | local-history | `/sc:git commit` | `commit.md`, `safety.md` | `preflight`, `stage-plan`, `check-message`, `verify` |
| `branch create <name>` | working-tree | `/sc:git branch` | `branch.md`, `safety.md` | `preflight` |
| `branch switch <name>` | working-tree | `/sc:git branch` | `branch.md`, `safety.md` | `preflight` |
| `submodule update <path>...` | working-tree | `/sc:git submodule update` | `submodule.md`, `safety.md` | `preflight`, `submodules` |
| `submodule commit-pointer <path>` | local-history | `/sc:git submodule commit-pointer` | `submodule.md`, `safety.md` | `preflight`, `submodules`, `check-message`, `verify` |

At most two refs load per invocation: the operation's group ref plus `safety.md` for a write; a read loads only its group ref (FR-018, T-13).

### 3.4 Per-invocation flow (write operations)

1. **Authorize.** The person's current message must start with the operation's prefix, else refuse `authorization: write operations need a person-typed /sc:git <operation>` and print no command lines; reads still run (FR-020). One line authorizes one operation and only the repository, paths, branch name or submodule target it names (FR-021, FR-023).
2. **Preflight.** `vcs preflight` returns `top`, `branch`, `symbolic_ref`, `detached`, `protected`, `operation_in_progress`, `index_lock`, `hooks_path`, `submodule_recurse`, `push_recurse_submodules`. The agent refuses on `detached-head`, `protected-branch`, `operation-in-progress`, `index-locked`, `git-too-old` (FR-032).
3. **Plan.** `vcs stage-plan --path ...` (or no paths for a pathless commit) returns `add_argv`, `commit_argv`, `commit_paths`, `skipped`, `message_path`; for an `add` only `add_argv`.
4. **Message** (commit): `--message` or `--smart-commit` (drafted from `git diff --cached` in Conventional Commits form), written with Write to `message_path`, checked by `vcs check-message` (FR-039, FR-066 without `--implement`).
5. **Protect work outside the commit set** (commit and pointer commit, FR-117): visible `git update-ref` pins of the worktree snapshot, taken just before the commit with the Q0 private-index method (`SKILL.md:124`).
6. **Write.** The agent runs the planned `git` command with its own Bash call (the FR-035 argv; for a pathless commit `git commit -F <message file>` without `--only`). It never edits the argv.
7. **Verify and report.** `vcs verify` reads back the parent, changed paths and contents; the agent prints the FR-022 report (preconditions checked, exact argv, result, HEAD before and after, whether index and work tree changed) and, as advice it never runs, `git reset --soft <parent>` or `git revert <sha>`. A `/sc:git` pin is deleted with a visible `git update-ref -d` after a clean comparison and kept while an outside-change report is outstanding (FR-117).

Branch `create` runs `git switch -c <name>` and refuses a protected or existing name; `switch` runs `git switch <name>` and refuses a non-empty `git status --porcelain=v2 --ignore-submodules=none` (FR-034). `branch cleanup` prints the `/sc:worktrees` route (`list`, `archive` writes even without `--apply`, `retire`/`prune` need `--apply`) and runs nothing; without `scripts/worktree_cleanup.py` it prints the notice of `worktrees.md:45` (FR-080). No code anywhere runs a branch delete (FR-081, T-17).

### 3.5 Safety content owned once

`refs/safety.md` repeats the lists that live as constants in `vcs_rules.py` (`PROTECTED_BRANCHES`, `FORBIDDEN_FLAGS`, `DEV_MIRROR_ALLOW`, `MIN_GIT`); a parity test asserts prose equals constants (NFR-003, T-13). Changing one rule is one constant edit plus one prose edit, and the test fails if only one changes.

`````

### .dev/tasks/to-do/TASK-WF-design-20261126-162939/source.md:169-240

`````markdown
## 4. Component C2: the `vcs` helper

### 4.1 Layout and calling convention

```
scripts/vcs.py             entry point: argparse, verb dispatch, emit(), exit codes 0 / 64 / 69
scripts/vcs_rules.py       constants and the runner allow-list table (single source for safety rules)
scripts/vcs_plan.py        GitRunner, ledger reader, sidecar parser, boundary and key logic, stage-plan, candidate, reconcile, verify, resolve-check
scripts/vcs_submodules.py  submodule facts and the derived-state precedence
```

Python 3.10 or later, standard library only. Run as `uv run --no-project python "<skill-dir>/scripts/vcs.py" <verb> ...` (the precedent is the archive helper call at `refs/managed-workspace.md:54`). Exit codes: 0 when JSON was printed whatever the `status`; 64 usage error; 69 lookup failure (FR-012). Every JSON object carries `vcs_contract: "1"`, `verb`, `status`, `reason`, and `head_before` / `head_after` where relevant (FR-010). A reader that sees another `vcs_contract` value refuses with `helper-missing` (NFR-009).

### 4.2 The runner seam (FR-011, DD-9)

`GitRunner(top, timeout=10)` builds every call as `git --no-optional-locks -c core.fsmonitor=false [-C <dir>] <verb> <options>` and checks it against `ALLOWED`, a table from verb to permitted option tokens, before it runs. Verbs: `rev-parse`, `symbolic-ref`, `status`, `diff`, `ls-files`, `ls-tree`, `cat-file`, `check-ignore`, `config --get/--get-regexp`, `submodule status`, `for-each-ref`, `rev-list`, `log`, `merge-base --is-ancestor`, `branch --show-current`, `hash-object` without `-w`, and `read-tree`, `add`, `write-tree` only when `GIT_INDEX_FILE` names a private temporary index. A violation raises `ForbiddenArgv` before the process starts (T-03 uses a recording runner). Implement-side reads add `--ignore-submodules=all`; only the person-invoked `/sc:git status` and `submodule status` use `--ignore-submodules=none`. The runner returns `(rc, stdout)` and callers must distinguish `rc 1` from `rc 128` (an `--is-ancestor` exit of 128 is "unknown", never "diverged"; FR-041).

The private-index calls write loose objects, as the Q0 snapshot does; the helper writes no ref, no user index, no work-tree file and no config (FR-011).

### 4.3 Verbs

| Verb | Arguments | Result fields (beyond the envelope) | `status` values |
|---|---|---|---|
| `preflight` | `[--cwd <dir>]` | `top`, `branch`, `symbolic_ref`, `detached`, `protected {value, reason}`, `operation_in_progress`, `index_lock`, `hooks_path`, `submodule_recurse`, `push_recurse_submodules`, `git_version`, `min_git_ok`, `default_branch_known` | `ok`, `refused` |
| `stage-plan` | `(--path <p>... \| --ledger <file> --run-dir <dir> [--package <dir>]) [--candidate] [--cwd <dir>]` | `tasks`, `commit_paths`, `skipped [{path, why}]`, `add_argv`, `commit_argv`, `message_path`, `pathspec_file`, `s_count`, `truncated`; with `--candidate`: `candidate_tree` | `ok`, `nothing`, `refused` |
| `check-message` | `--file <f> [--implement]` | `header_len`, `rule` when refused | `ok`, `refused` |
| `verify` | `--key <64hex> --attempt <n> --parent <40hex> --candidate-ref <ref> --worktree-ref <ref> --exit <int> [--ledger <f> --sidecar <f>] [--cwd]` | `class`, `sha`, `outside_changed`, `outside_paths` (capped), `changed_paths` | `committed`, `pending`, an FR-036 class, `uncertain` |
| `reconcile` | `--ledger <f> --sidecar <f> --run-dir <d> [--package <d>] --flag on\|off [--cwd]` | `boundaries [{key, members, state, action, parent, head, reason}]`, `runs`, `segments` | `ok`, `refused` (`sidecar-mismatch`, `sidecar-corrupt`, `plan-changed`) |
| `resolve-check` | `--key <hex or unique prefix> --ledger <f> --sidecar <f> [--run-dir <d> --package <d>] [--cwd]` | `key`, `state`, `choices [abandon, adopt?]`, `basis`, `differs`, `head`, `parent`, `quiescent` | `ok`, `refused` (`unknown-boundary`, `ambiguous-key`, `already-settled`, `adopt-not-descendant`, `adopt-unverifiable`) |
| `submodules` | `[--cwd <dir>]` | `superproject {branch, head}`, `config {submodule_recurse, push_recurse_submodules}`, `rows [...]` (section 4.6) | `ok` |

Ledger-mode `stage-plan` finds the single due boundary itself: settle before advance means at most one boundary is due at a time (FR-077). With no due boundary it refuses `no-due-boundary`. The sidecar path is always `<ledger dir>/commits.md`.

### 4.4 Core types and pure functions (interfaces only)

```
LedgerView   tasks[id] -> TaskGen[]      TaskGen(start_ordinal, start_sha, start_line_no, anchor_line_no|None, verdict, files[])
RunLine      run, flag(on|off), revoked, ledger_lines, branch, at, args, source, worktree
Sidecar      runs[RunLine], attempts[key -> Attempt[]], terminal[key] -> Terminal|None, resolved[key] -> Resolved|None
Boundary     members[task ids], key(64 hex), anchors[line_no], eligible(bool), state(due|pending|refused|uncertain|settled|out-of-protocol)

parse_ledger(text)            -> LedgerView        # DD-8 regexes; unknown last line -> LedgerCorrupt
parse_sidecar(text)           -> Sidecar           # strict per-line regexes; unknown form, malformed line, truncated tail -> SidecarCorrupt (never repaired)
ledger_k(text)                -> int               # newline count (+1 when the last line is unterminated), FR-102
segment_of(line_no, runs)     -> RunLine|None      # last run line with k < line_no; equal offsets resolved by sidecar order
boundary_key(ident, ledger_id, source_id, members) -> str   # SHA-256, ident = managed:<slug>|legacy:<slug> (DD-1)
derive_state(boundary, sidecar, git_facts, flag)  -> (state, action)   # DD-5, FR-107 as a table
plan_stage(...)               -> StagePlan
build_candidate(...)          -> tree sha          # private index: read-tree parent, add S, include the frozen sidecar bytes
verify_commit(...)            -> VerifyResult      # FR-108 predicate
resolve_check(...)            -> ResolveResult
```

All functions are pure over their inputs plus read-only git facts. Determinism (NFR-006): paths sorted, ids in source order, keys sorted, no timestamps in results except those copied from the sidecar.

### 4.5 `stage-plan` algorithm (FR-060..FR-063, FR-073..FR-076)

1. Parse mode. Path mode (for `/sc:git`) skips steps 2 and 6 to 8. Ledger mode reads the ledger and `commits.md` and finds the due boundary (refuse `no-due-boundary`, `out-of-protocol`, `unsettled` as FR-105 and FR-107 define).
2. `commit_paths` = sorted union of the `files=` of the members' anchor `complete` lines (FR-062); a later re-review `complete` never changes it.
3. Apply path rules, each to `skipped` with its `why`: under `.dev/implement/`; ignored (`check-ignore`); outside the repository or resolving through a symlink outside (`outside-repo`); gitlink or under a mode-160000 entry of HEAD, index or the retained Q0 tree (`gitlink`); `.claude/` path other than `settings.json` (`dev-copy-path`, also for a tracked file); not representable in the ledger (`path-unrepresentable`); a directory entry (`directory-entry`); absent from the work tree, index and HEAD (`absent`); a path absent from the work tree but present in the index or HEAD is a deletion and is staged.
4. Managed run: add the literal expansion of `<pkg-dir>` from `git ls-files -z --cached --others --exclude-standard -- <pkg-dir>` (FR-076); S = `commit_paths` plus that expansion. `git add -- .dev/tasks` is a separate argv; it does not widen S (FR-062).
5. Checks, each a refusal token: `branch-changed` / `branch-unproven` (current symbolic ref against `<retries>/T<id>/q0-branch` of the first member, FR-054); `head-moved` (HEAD against `q0-head`); `foreign-change` (blob at `q0-head` against the blob in the Q0 start tree, per product path, FR-075); `changed-after-review` (product path against the accepted tree, FR-074); `no-accepted-tree`, `no-snapshot` (FR-073); `truncated` (S larger than the 200-entry JSON cap is still written in full to the pathspec file; only the JSON list is capped).
6. Write nothing to the repository. The pathspec file is written to a temporary location outside the work tree by the helper's caller (the agent), using the list in `pathspec_file`; `stage-plan` prints the path to use and the NUL-delimited content hash (`paths=`).
7. `add_argv` and `commit_argv` have exactly the FR-035 shape and never contain a token of FR-063 (T-02).
8. `--candidate` (run after the prepared line is appended): build the candidate tree from the parent plus S, including the managed sidecar's frozen prepared bytes, in a private temporary index, and print its tree sha. The agent pins it with a literal `git update-ref` (FR-108). The tree hash is never written inside the sidecar it covers.

### 4.6 Submodule facts (FR-040..FR-042)

One row per top-level registered submodule, sorted by path. Facts and their git source (all through the runner): `gitlink` from `ls-tree HEAD -- <path>`; `initialized` and `conflicted` from `submodule status` prefixes; `head` from `-C <path> rev-parse HEAD`; `branch` from `-C <path> branch --show-current` (null when detached); `commit_changed`, `tracked_dirty`, `untracked_dirty` from the `S<c><m><u>` field of `status --porcelain=v2 --ignore-submodules=none`; `target_local` from `-C <path> cat-file -e <gitlink>^{commit}`; `contained` from `for-each-ref --contains <head> refs/heads refs/remotes` (DD-9; null when unknown); `nested` when the submodule has its own `.gitmodules`. A missing value is null, never a fabricated clean state.

Derived `state`, first match wins: `conflict`, `dirty-tracked`, `dirty-untracked`, `detached-new-commits` (detached, HEAD differs from gitlink, not contained), `uninitialized`, `target-not-local`, `submodule-ahead` (gitlink is an ancestor of HEAD), `submodule-diverged`, `pointer-moved`, `in-sync`. Eligibility for `update` and `commit-pointer` is a table over `state` (FR-041, FR-042); the published-target check for `commit-pointer` reads only remote-tracking refs of the remote whose `remote.<r>.url` equals the `.gitmodules` URL, and the report labels the result a local observation with the last fetch time (FR-042).

`````

### .dev/tasks/to-do/TASK-WF-design-20261126-162939/source.md:241-366

`````markdown
## 5. Component C3: the commit step in `sc-implement-protocol`

### 5.1 Change manifest inside the implement protocol

| File | Change | Requirements |
|---|---|---|
| `src/superclaude/commands/implement.md` | Options row and `argument-hint` (line 7) gain `--commit-tasks`; the Will Not at line 100 becomes "Commit without `--commit-tasks` on the invocation line, push, open PRs, or release (a managed archive is not any of these)" | FR-050, FR-053 |
| `skills/sc-implement-protocol/SKILL.md` | Wave 0 step 1 known-options list (line 57) gains the flag; new step **5b** (commit preflight, flag only) after step 5 and before step 6; new step **6b** (outside-S observation, `run` line, reconcile) after step 6; Q0 records `<retries>/T<id>/q0-branch` beside `q0-head` (flag only); the Q0 cleanup sentence (line 129) is amended; one loop line **Q8a** between Q7 and Q8; STOP table gains `E-COMMIT-PRECONDITION` and `E-COMMIT-REFUSED`, and the closed-list sentence (line 51) names both; the "Done" summary prints commit lines; one load-rule line; **net growth at most 15 lines** | FR-054, FR-057, FR-070, FR-071, FR-072, FR-131, NFR-012 |
| `skills/sc-implement-protocol/refs/commit-step.md` (new) | Two parts. **Reconcile and settle** (applies to every run that has the flag or an existing `commits.md`): `off` run line, settle before advance, FR-100..FR-108 as read-and-record rules, outside-S comparison of a resumed attempt, FR-114..FR-116, owner resolution FR-120..FR-125, pin lifetime FR-131, no-lock rule FR-133, helper check FR-019, final summary FR-071. **Commit procedure** (flag only): trigger and positions, the nine-step procedure, hook classes, message format, capture and snapshot FR-110..FR-112, `verify`, retry inputs FR-132, Ruling text FR-078 | FR-072 |
| `refs/ledger.md` | Resume Row 1 and the pin-deletion sentence stop deleting `accepted/`, `boundary/`, `boundary-wt/`, `rewritten/` pins and the Q0 pin of an unsettled boundary's members; the legacy all-complete stop (line 139) and the FINAL dispatch honour settle before advance | FR-077, FR-131 |
| `refs/retry.md` | Line 504 "(no commit follows it)" becomes the FR-078 text; "Halts and transient stops" gains `commit-interrupted` and `index-locked`; Q0 file list gains `q0-branch` | FR-078, FR-116, FR-054 |
| `refs/qa.md` | Ruling cost-if-wrong (line 254) says the accepted task is committed at the next boundary when the current `run` line is `on` | FR-078 |
| `refs/managed-workspace.md` | Archive gate step 1 (line 52) refuses `E-ARCHIVE-BLOCKED reason=unsettled-boundary` before any move while a due, pending, refused or uncertain boundary exists; reads the ledger and `commits.md` through `vcs reconcile` | FR-070 |
| `scripts/archive_workspace.py` | **No change** (verified by a byte-equality assertion against the integration base in T-11) | I2, FR-070 |
| `core/WORKER-CONTRACT.md` | K3 sentence at line 42 rewritten to the delivered rule; WC-9 end-of-Task commit grant unchanged | FR-091 |
| `plugins/superclaude/**` | Byte copies of every changed file above | FR-015 |

### 5.2 Wave 0 order (flagged and unflagged)

| Step | Action | When |
|---|---|---|
| 1 | Tokenize arguments; `--commit-tasks` counts only as a standalone token in the option prefix of a message the person typed that starts with `/sc:implement` | always |
| 3 to 5 | Resolve source, enumerate tasks, resolve the ledger path (managed: `<pkg>/progress.md`) | always |
| **5b** | `vcs preflight`; read any existing ledger and `commits.md` without writing; STOP `E-COMMIT-PRECONDITION reason=<token>` on `not-person`, `unattended`, `helper-missing`, `not-a-repo`, `detached-head`, `protected-branch`, `operation-in-progress`, `index-locked`, `git-too-old` | flag present |
| 6 | Open or create the ledger; managed identity and `PLAN:` pin verification (`E-PLAN-CHANGED` stops here, before anything is committed) | always |
| **6b** | (a) take any outstanding outside-S comparison (FR-113); (b) append the `run` line; (c) `vcs reconcile`; (d) perform the actions it names | flag present, or `commits.md` exists |
| 7 to 9 | Task-count notice, auggie, the single codegraph readiness check and its `codegraph.md` append | always (after 6b, FR-106) |
| Q-loop | Task selection, Q0..Q8, with Q8a, R0, L0 | always |

The "outside-S comparison before the new `run` line" order exists so the executor's own new `run` line never looks like damage (FR-106, FR-113). The managed `codegraph.md` append moves after reconcile for the same reason (FR-132).

### 5.3 Commit positions (FR-057)

| Position | Where | Runs when |
|---|---|---|
| **Q8a** | After Q7 has flushed a `complete` line and every task writer has finished and been joined; before Q8 writes the next `start` or takes the next Q0 | flag present, no task open, a boundary is due |
| **R0** | At the start of a resume, inside step 6b (reconcile), before task selection | flag present and a boundary is due or pending, or any run that must settle |
| **L0** | After the last task's `complete` and before the whole-list review, the legacy all-complete stop, or the managed FINAL | flag present, a boundary is due |

"No task is open" is rechecked from the ledger on disk at every position. A batch (up to 3 tasks, every `start` written before any member runs, `SKILL.md:108-110`) becomes one boundary and one commit after every member is `complete`; if a member halts, no commit is made until a resume completes it (FR-058). The commit step never runs while any task's latest record is `halt` or `blocked` (FR-059).

### 5.4 Boundary state machine

Event-driven; the table is the single source for `derive_state` (DD-5). `Terminal` lines live in `commits.md`.

| From | Event | To | Line appended |
|---|---|---|---|
| (none) | Last member's anchor `complete` flushed, anchor in an `on` segment | `due` | none |
| `due` | Run with flag, no task open, checks pass, S non-empty | `pending` | `commit prepared key=... attempt=1 ...` |
| `due` | S empty | settled | `commit skipped key=... reason=empty` |
| `due` | batch members not all eligible | settled | `commit skipped key=... reason=mixed-authorization` |
| `due` | another task's `start` follows a member's anchor | `out-of-protocol` | none (STOP with owner choices) |
| `pending` | `verify` returns `committed` | settled | `commit sha=<40hex> key=... attempt=<n>` |
| `pending` | `verify` returns `pending` (HEAD = parent) after a hook class | `refused` (HEAD = parent) | `commit refused key=... attempt=<n> reason=<class>` |
| `pending` | `verify` returns `hook-rewrite-committed` or other history | `refused` (HEAD != parent) or `uncertain` | `commit refused ...` or `commit uncertain ...` |
| `pending` | timeout, signal, exit > 128 | `pending` (open) | none; STOP `E-RESUME-NEEDED reason=commit-interrupted` |
| `pending` / `refused` (HEAD = parent) | flagged run, FR-107 conditions hold | `pending` (attempt n+1) | new `prepared` line |
| `pending` | unflagged or later run proves the commit exists | settled | `commit recovered=<40hex> key=... attempt=<n>` |
| any unsettled | owner answers `abandon` or `adopt` | settled | `commit resolved key=... as=abandoned\|adopted ...` |

Unsettled = `due`, `pending`, `refused`, `uncertain`, `out-of-protocol`. Settle before advance (I5): while any exists, no run writes a `start`, takes a Q0, returns "all complete", runs FINAL, or enters the archive gate (FR-077). A late preparation or a retry happens only inside reconcile and only while no task is open, so HEAD never moves under an open task.

### 5.5 The commit procedure (FR-061)

Each step is one visible call unless marked "helper".

| # | Step | Who | Writes |
|---|---|---|---|
| 1 | `vcs stage-plan --ledger ... --run-dir ... [--package ...]` computes S and runs the FR-073..075 and branch checks | helper | nothing |
| 2 | Write the message to `message_path` (outside the work tree); `vcs check-message --implement` (one rewrite allowed, a second refusal is `reason=message`) | agent, helper | temp file |
| 3 | Write `commit-paths-<key>-a<n>.txt` (NUL-delimited S) beside the sidecar; append the `prepared` line (flushed before the side effect) | agent | `commits.md`, path file |
| 4 | `vcs stage-plan --candidate` prints the frozen candidate tree; pin `refs/superclaude/implement/<slug>/boundary/<key>-a<n>` with `git update-ref` | helper, agent | ref |
| 5 | `git --literal-pathspecs add --pathspec-from-file=<f> --pathspec-file-nul` for S, then `git add -- .dev/tasks` when it exists and is not ignored | agent | index |
| 6 | Worktree snapshot with the Q0 private-index method; pin `.../boundary-wt/<key>-a<n>` | agent | ref |
| 7 | `git --literal-pathspecs commit --only -F <msg> --pathspec-from-file=<f> --pathspec-file-nul`, Bash timeout 600000 ms | agent | commit |
| 8 | `vcs verify ...` applies the FR-108 predicate and the FR-113 outside-S comparison | helper | nothing |
| 9 | Append the terminal line (not part of the commit it records; in a managed run it is staged with `.dev/tasks` and enters the next boundary commit; in a legacy run the sidecar is never staged) | agent | `commits.md` |

The executor never edits an argv the helper printed (FR-061). It never runs `--no-verify`, `-n`, `SKIP=`, `commit-tree` or `--amend`, and never edits a hook or `core.hooksPath` (FR-064).

### 5.6 Crash points and what the next run finds (FR-108, FR-130, T-22)

| Crash after | On disk | Next run (flagged) |
|---|---|---|
| `complete` flushed, before `prepared` | boundary `due`, no line | crash-explained if no later `start` and no task open: prepare now (FR-105); otherwise `out-of-protocol` |
| `prepared` appended, before pins exist | `prepared` line, HEAD = parent, a pin missing | DD-11: HEAD = parent, so nothing was committed: `pending`, new attempt n+1 with fresh pins; the incomplete attempt is never treated as prepared |
| staged and pinned, before the commit call | index holds S, HEAD = parent | `pending`: new attempt allowed only as FR-107 says |
| commit made, before the terminal line | HEAD has one parent = prepared parent, tree equals the pinned candidate, trailer carries the key | `verify` proves it: append `commit recovered=<sha>`; nothing is committed twice |
| terminal line written | settled | nothing |
| commit killed by timeout, orphan hook still running | attempt open, possibly rewritten files | STOP `E-RESUME-NEEDED reason=commit-interrupted` until the person confirms git and hook processes stopped (FR-116) |
| person committed by hand on top | HEAD history differs | `uncertain`; owner chooses `abandon` or `adopt` (FR-120) |

DD-11 (added by this design): a `prepared` line without its pins whose HEAD still equals the prepared parent is `pending` and may be retried as attempt n+1. FR-108 calls incomplete proof `uncertain`, which this design reads as the case where history has also moved. The plan should confirm this reading with the owner in review; both readings fail closed.

### 5.7 Pin families

| Ref (under `refs/superclaude/implement/<slug>/`) | Created | Kept until |
|---|---|---|
| `T<id>` (Q0 start tree, existing) | Q0 | the boundary of which the task is a member settles (FR-131) |
| `accepted/T<id>-s<start ordinal>` | before the first eligible `complete` is flushed (FR-073) | the boundary settles |
| `boundary/<key>-a<n>` (frozen candidate tree) | step 4 | the boundary settles |
| `boundary-wt/<key>-a<n>` (worktree snapshot) | step 6 | the boundary settles, and while an `outside-changed` report is outstanding, even through archive (FR-114, FR-125) |
| `rewritten/<key>-a<n>` (tree rewritten by a hook) | after a rewrite class | the boundary settles |
| `retry/T<rid>/r<k>-<j>` (reviewed trees, existing) | review | deleted at `complete` once the accepted pin holds the tree |

Pins are create-once: an existing pin with a different target refuses `pin-conflict` and a retry never overwrites an earlier recovery pin (FR-110). `boundary/` and `boundary-wt/` are siblings because git cannot create a ref under an existing ref. After settlement the executor deletes ordinary proof with literal `git update-ref -d` calls, and the final summary lists every leftover pin with its delete line (FR-131). `/sc:git` uses `refs/superclaude/git/boundary-wt/<timestamp>` (FR-117).

### 5.8 Sidecar `commits.md` (FR-100..FR-103)

Location: legacy `.dev/implement/<slug>/commits.md` (never staged, like the legacy ledger); managed `<pkg-dir>/artifacts/commits.md` (staged with `.dev/tasks`). Six line forms, one regex each, documented once in `refs/commit-step.md` and parsed by `vcs_plan.py`, pinned by parity test T-10:

- `run <n>: commit-tasks=(on|off)[ reason=revoked] ledger-lines=<k> branch=(<ref>|-) at=<ISO-8601> args="<prefix>" source=<path|inline:<hash8>> worktree=<id>`
- `T<ids>: commit prepared key=<64hex> attempt=<n> parent=<40hex> branch=<ref> paths=<sha256> accepted=<ref>[,<ref>...] plan=<hash|-> source=<hash|->`
- `T<ids>: commit (sha|recovered)=<40hex> key=<64hex> attempt=<n>[ outside-changed=<n> wt=<ref>]`
- `T<ids>: commit skipped key=<64hex> reason=(empty|mixed-authorization)`
- `T<ids>: commit (refused|uncertain) key=<64hex> attempt=<n> reason=<token>[ rewritten=<ref>]`
- the two `resolved` forms (section 6.2).

Rules: a record is appended and flushed before the side effect it announces; the parser rejects unknown forms, malformed lines and a truncated tail and never repairs (`sidecar-corrupt` is, like `E-LEDGER-CORRUPT`, the one state a person repairs by hand); `k` counts newline bytes plus one for an unterminated last line; a ledger line at position `p` belongs to the last `run` line with `k < p`; only the executor appends `run` lines. Eligibility anchors on the **first** `complete` after a task's `start`; later re-review lines never create, revive or re-authorize a generation (FR-103). The boundary key is SHA-256 over the canonical tuple (repository/worktree identity, `managed:<slug>` or `legacy:<slug>` per DD-1, source identity, ordered task ids, each start ordinal and full start sha); stored keys are always 64 hex, a 12-hex prefix is for display only.

### 5.9 Flag lifecycle and the unflagged run

`--commit-tasks` is per invocation, off by default, and a resume needs it again. The grant covers later turns of the same active run (including the in-chat Ruling that continues to the next task, and context compaction, because the executor re-reads the ledger and `commits.md` from disk). Plain words from the person can revoke it (a revocation `run` line precedes the next attempt) but never widen it (FR-050). A Ruling never authorizes a commit (`refs/ledger.md:239`). Under `--unattended` the run refuses before any commit-feature write (`E-COMMIT-PRECONDITION reason=unattended`; FR-092 keeps this when P4 adds the section). At launch levels below `full --submit` the guard refuses the commit call, reported as `blocked-by-host` (FR-093); nothing reads the guard's store.

A run without the flag and with no `commits.md` adds no Bash call and no file (NFR-018). With an existing `commits.md` it loads only the "Reconcile and settle" part, appends one `off` run line, reconciles, may record a proved existing commit as `recovered`, STOPs `reason=unsettled` on an unsettled boundary before task selection, and never makes a commit (FR-051, FR-107, T-16).

`````

### .dev/tasks/to-do/TASK-WF-design-20261126-162939/source.md:367-394

`````markdown
## 6. Component C4: protecting work outside the commit set, and owner resolution

### 6.1 Worktree snapshot and compare (FR-110..FR-118)

Why it exists: under `git commit --only`, every change outside S counts as unstaged, and a hook framework that stashes unstaged changes can lose them if it is killed; edits to assume-unchanged files can be overwritten even without a kill (research and probe findings, risk 15).

1. **Two independent proofs** per attempt: the candidate tree (what the commit may contain, step 4) and the worktree tree (content outside S, step 6). One never substitutes for the other.
2. **Capture before commit:** after the visible `git add` calls and immediately before the visible commit, build the worktree snapshot with the Q0 private-index method (`SKILL.md:124`), starting from HEAD, and pin it with a literal `git update-ref`. A failed or incomplete snapshot appends `refused reason=snapshot-failed` and makes no commit. A configuration whose snapshot would not be lossless (for example a clean/smudge filter found by `config --get-regexp '^filter\.'`, DD-10) refuses `snapshot-unsupported` before the commit.
3. **Compare every attempt:** after any normally finished attempt take a second snapshot before appending the result line or any log, and compare every path outside S with the before tree, including additions, deletions, modes and symlinks. A failed comparison stops `reason=outside-unverified` and keeps the before pin.
4. **Detected damage:** the result line records `outside-changed=<n> wt=<ref>`; the invocation stops `E-COMMIT-REFUSED reason=outside-changed` even if the commit itself verifies; the proved commit is not relabelled and no second commit is made; the before pin is kept through resolution and archive until the owner releases it. Recovery is explicit: the STOP prints `git restore --source=<saved-ref> -- <literal-paths>` for saved paths only, with "compare first: this overwrites any newer edit". The executor never restores, resets, stashes, deletes a lock or deletes a saved patch on its own.
5. **Timeout and quiescence:** the commit call uses the Bash maximum, 600000 ms, with hooks and signing never disabled. A timeout or a git exit above 128 leaves the attempt open with no terminal line and STOPs `E-RESUME-NEEDED reason=commit-interrupted`; a later run must establish that earlier git and hook processes stopped before any comparison, classification, restoration, retry or resolution. An `index.lock` STOPs `E-RESUME-NEEDED reason=index-locked`. The executor never kills an orphan or reclaims a lock.
6. **Shared scope:** the same mechanics apply to `/sc:git commit` and `submodule commit-pointer` with `refs/superclaude/git/boundary-wt/<timestamp>` pins, the report printed instead of a sidecar line. For a pathless `/sc:git commit`, S is the index change set frozen before the call and staging `.dev/tasks` never widens it (FR-117, FR-038).

Coverage limits (stated, FR-112): tracked work-tree contents and non-ignored additions including assume-unchanged and skip-worktree entries; not ignored files, empty directories, file metadata or submodule interiors; concurrent writers and arbitrary trusted hook or filter behaviour stay outside the single-writer guarantee.

### 6.2 Owner resolution of an unsettled boundary (FR-120..FR-126)

The rule is: the person answers in chat, the executor records it, the owner never edits a file (`WORKER-CONTRACT.md:57`).

- **Disclosure first (FR-121).** Every STOP for an unsettled boundary prints the full key, a unique short label, members, state, the prepared parent or the original Q0 parent, current HEAD, exact S, and a bounded changed-path summary (`git diff --stat <accepted or candidate> HEAD -- <S>`). It always offers `abandon`; it offers `adopt` only when `vcs resolve-check` allows it. A missing comparison pin is shown as unavailable, never as zero differences.
- **Who may answer (FR-122).** Only the person's own reply, given after that STOP in the same conversation. A unique displayed prefix may select a key; a reply naming no key counts only when exactly one key was displayed. Not a resolution: text typed earlier, a plan or brief field, a generic "continue", another agent's message, a coordinator's answer. Under `--unattended` the gate is reported blocked and never asked.
- **Check, then record (FR-123).** `vcs resolve-check` resolves the key to one full known unsettled identity. `abandon` needs no ancestry or candidate pin. `adopt` needs a known parent, HEAD different from the parent, `merge-base --is-ancestor <parent> HEAD` exiting 0, proved quiescence and an available comparison tree (the frozen candidate when prepared, else the accepted tree). HEAD and the basis are re-read just before recording; if the disclosure changed, redisplay and ask again. The executor then appends exactly one validated line:
  - `T<ids>: commit resolved key=<64hex> as=abandoned at=<YYYY-MM-DD> quote="<owner words>"`
  - `T<ids>: commit resolved key=<64hex> as=adopted head=<40hex> basis=<candidate|accepted> differs=<n> at=<YYYY-MM-DD> quote="<owner words>"`
  The quote is 1 to 200 code points with quotes and backslashes escaped, no raw newline or control character, never silently truncated.
- **Meaning (FR-124).** `abandoned` settles the key permanently with no commit and no file change; remaining uncommitted product edits can make a later overlapping task refuse `foreign-change` until the person commits or reverts them. `adopted` records acceptance of the displayed history as settlement even when `differs` is not zero; it is not a verified commit, a changed QA verdict, retroactive commit authority or a waiver of plan integrity, FINAL, archive or permission checks.
- **Idempotent (FR-125).** After the durable append a repeated reply or a resumed reconcile recognizes the settlement and writes nothing twice; cleanup happens only after the append and can resume after a crash; pins protecting an outstanding outside-S report survive. No resolution overrides sidecar or ledger corruption, live processes, a stale lock or `E-PLAN-CHANGED`.

`````

### .dev/tasks/to-do/TASK-WF-design-20261126-162939/source.md:395-414

`````markdown
## 7. Component C5: surrounding surfaces

| File | Change | Requirements |
|---|---|---|
| `src/superclaude/commands/git.md` | Rewritten per §3.2 | FR-001..FR-005 |
| `plugins/superclaude/commands/git.md`, `plugins/superclaude/skills/sc-git-protocol/**` | Byte copies of the source (the plugin build copies `plugins/superclaude/` unchanged, `scripts/build_superclaude_plugin.py:16`, `:77`) | FR-015 |
| `commands/sc-git.md` | Deleted; add to the `_RETIRED` absence list in `tests/docs/test_retired_docs_absent.py` (precedent). The other `commands/sc-*.md` files are left alone | FR-014, D5 |
| `src/superclaude/commands/README.md` (line 9) | Add `git` to the list of plugin-mirrored commands | FR-015 |
| `tests/commands/test_routing_plugin_parity.py` (line 41) | `@pytest.mark.parametrize("name", [...])` gains `"git"` | FR-015, AC-04 |
| `src/superclaude/core/HOW-WE-WORK.md` (the `/sc:git` row, around line 293) | Rewritten: drops "merge operations", names `/sc:worktrees` for cleanup, names only flags that exist in `git.md`, keeps the three phrases fixture S23 pins ("Status-only stays inspection", "a commit needs authorization", "Do not append push, merge or PR creation"), route steps do not name `/sc:pr-submit`. The level table is not touched, so the copy into `src/superclaude/core/CLAUDE.md` is not needed | FR-017 |
| `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` | Byte copy of the edited guide | FR-015, AC-13 |
| `src/superclaude/core/WORKER-CONTRACT.md` (line 42) | K3 sentence rewritten (section 5.1). Verified: the plugin tree holds no copy of this file | FR-091 |
| `tests/recommend/fixtures/routing_refresh_cases.json` (S23, lines 312-331) | `activation` becomes `{"sc:git": "sc:git-protocol"}`; top-level `mode_flags` stay `[]`; the repeat's `mode_flags` stay `["--smart-commit"]` | T-14 |
| `tests/skills/test_worker_contract.py` (lines 2945-2960 and the classification table) | Drop the `merge feature-branch --interactive` row; every new or changed line under `src/superclaude/{skills,commands,agents}` that matches `WRITE_VERB_RE` gets exactly one classification row (`never-worker` for `sc-git-protocol`; `deferred:P4` for the implement commit-step lines); stale rows removed | T-14 |
| `docs/user-guide/commands.md` (lines 98, 1258-1273) and `docs/user-guide/flags.md` (lines 136-140) | **Added by this design, not in the requirements:** they document `[--smart-commit] [--interactive]` and a `merge ... --interactive` example, which the refactor removes. Update them to the FR-002 usage so the user guide is not left stale | FR-002, FR-004 |
| `make sync-dev`, `make verify-sync` | Run after every `src/` edit; `<dev>` copies are never staged except `.claude/settings.json`. `verify-sync` is not proof of plugin parity (it never touches `plugins/`), so the explicit `cmp` / `diff -r` checks of AC-04 are required | FR-016, RC-6 |
| Tests that pin the implement STOP table or option list | Candidates: `tests/skills/test_task_workspace_lifecycle.py`, `test_implement_severity_static.py`, `test_implement_saved_prompt_rule.py`; which assertions are exact is UNVERIFIED and must be read when the plan reaches them (`tests/skills/test_implement_*.py` exist: retry_citation, adviser_family, launch_alias, retry_revert, saved_prompt_rule, severity_static, severity_replay) | T-14 |

Unchanged and asserted unchanged: `scripts/worktree_cleanup.py` (`_remove_branch` at line 2636), `src/superclaude/commands/worktrees.md`, `src/superclaude/hooks/scripts/launch-level-guard.sh`, `src/superclaude/skills/sc-implement-protocol/scripts/archive_workspace.py` (AC-11, FR-081). Mentions of `/sc:git` that only suggest it as an optional next step (`implement.md:107`, `sc-implement-protocol/SKILL.md:213`, the cleanup-audit command, protocol and report template) stay as they are; the implement protocol never invokes `/sc:git` or `Skill sc:git-protocol` (FR-072).

`````

### .dev/tasks/to-do/TASK-WF-design-20261126-162939/source.md:415-432

`````markdown
## 8. Interface catalog

### 8.1 STOP codes and reason tokens

| Code | Where | Reasons (open class `[a-z][a-z-]*`) |
|---|---|---|
| `E-COMMIT-PRECONDITION` | implement Wave 0 step 5b | `not-person`, `unattended`, `helper-missing`, `not-a-repo`, `detached-head`, `protected-branch`, `operation-in-progress`, `index-locked`, `git-too-old` |
| `E-COMMIT-REFUSED` | implement, reconcile or any commit position | the FR-036 classes (`blocked-by-host`, `hook-failed`, `hook-rewrite`, `hook-rewrite-evidence`, `hook-rewrite-committed`, `hook-rewrite-pinned`, `commit-error`) and `unsettled`, `out-of-protocol`, `uncertain`, `candidate-changed`, `sidecar-mismatch`, `sidecar-corrupt`, `branch-changed`, `branch-unproven`, `head-moved`, `foreign-change`, `changed-after-review`, `no-accepted-tree`, `no-snapshot`, `snapshot-failed`, `snapshot-unsupported`, `outside-changed`, `outside-unverified`, `pin-conflict`, `path-unrepresentable`, `outside-repo`, `directory-entry`, `message`, `helper-missing` |
| `E-RESUME-NEEDED` (existing code, two new transient reasons) | after a timeout or when a lock exists | `commit-interrupted`, `index-locked`; neither writes a terminal line |
| `E-ARCHIVE-BLOCKED` (existing code, new reason) | managed archive gate step 1 | `unsettled-boundary` |
| `/sc:git` refusal tokens | `/sc:git` write operations | `authorization`, `helper-missing`, `detached-head`, `protected-branch`, `operation-in-progress`, `index-locked`, `git-too-old`, `dev-copy-path`, `outside-repo`, `directory-entry`, `path-unrepresentable`, `gitlink`, `blocked-by-host`, plus the submodule tokens of §4.6 (`submodule-dirty`, `conflict`, `detached-new-commits`, `submodule-ahead`, `submodule-diverged`, `submodule-unpublished`, `remote-mismatch`, `target-not-local`) |

The implement STOP table stays closed apart from the two new codes and the two new reasons; the sentence at `SKILL.md:51` names both and says `E-RESUME-NEEDED` is the only code the retry ladder and the commit step's transient stops add (FR-070).

### 8.2 Helper JSON contract

`vcs_contract: "1"`; both protocols refuse any other value (`helper-missing`). A breaking JSON change raises the number in one release together with both protocols (NFR-009). Output at most 64 KiB; path lists at most 200 entries with `truncated`; refusal logs keep at most 40 lines; the cap never applies to S, the pathspec file or the `paths=` hash (NFR-007). Each helper git call has a 10-second timeout; the commit call uses 600000 ms (NFR-014).

`````

### .dev/tasks/to-do/TASK-WF-design-20261126-162939/source.md:433-459

`````markdown
## 9. Test design

All tests run with `uv run pytest`. Helper and git behavior tests use real temporary repositories (the existing `tests/worktree_cleanup/conftest.py` already builds throwaway repositories and local bare remotes and has a `git_in` helper to reuse); static text tests pin the prose.

| Module | Covers | Notes |
|---|---|---|
| `tests/vcs/conftest.py` | fixtures: `repo` (temp repo + local bare remote), `ledger_builder` (writes ledger lines from the closed grammar), `sidecar_builder`, `hook_emulator`, `submodule_repo`; adds the scripts folder to `sys.path` and loads `archive_workspace.py` by path (as `test_workflow_archive.py` does) | the `hook_emulator` runs the framework's exact command sequence and names the source revision it copies (FR-118) |
| `tests/vcs/test_stage_plan.py` | T-01, T-23 | path rules, deletions, gitlinks, literal names such as `:(glob)*`, `-n`, spaces, `d/how to merge.md` |
| `tests/vcs/test_argv_shape.py` | T-02 | FR-035 shape; no FR-063 token over every planning case |
| `tests/vcs/test_helper_readonly.py` | T-03 | recording runner; every argv is in the allow-list table with the prefix; `ForbiddenArgv` raised for `branch -D`, `config --unset`, `update-ref` |
| `tests/vcs/test_hook_refusal.py` | T-04 | each FR-036 class and its `commits.md` line; no same-run retry; no `--no-verify` in any argv |
| `tests/vcs/test_only_semantics.py` | T-05 | `git commit --only` leaves other staged entries staged and out of the commit (checks the assumption rather than trusting it) |
| `tests/vcs/test_check_message.py` | T-06 | 72-code-point rule, trailers, type list; the `conventional-pre-commit` type list is UNVERIFIED until a test runs the pinned hook |
| `tests/vcs/test_submodules.py` | T-07 | local superproject with a `file://` submodule; sets `protocol.file.allow=always` only in its own repos (UNVERIFIED on the CI image) |
| `tests/vcs/test_preflight.py` | T-08 | detached HEAD, protected names, merge in progress, `index.lock`, `origin/HEAD` notice, `git-too-old` (also checks the 2.25 claim of NFR-011) |
| `tests/vcs/test_eligibility.py` | T-19, T-22 (pure part), T-10 | segments, anchors, keys, mixed batches, `derive_state` table, sidecar regex parity |
| `tests/vcs/test_crash_points.py` | T-22, AC-16 | interrupt before `prepared`, after it, after staging, after the commit, after the terminal line; resume twice; at most one commit per key |
| `tests/vcs/test_worktree_protection.py` | T-20, AC-17 | emulated SIGTERM to the process group, to git alone with an orphan hook, SIGKILL, timeout, stale lock; assume-unchanged and skip-worktree edits; second attempt cannot overwrite the first pin; `git gc` cannot prune it |
| `tests/vcs/test_resolution.py` | T-21, AC-18 | every unsettled state offers `abandon`; rejection cases; crash after the resolution append |
| `tests/skills/test_git_protocol.py` | T-13, T-17 | registry rows resolve to refs; helper verbs appear in `vcs.py --help`; prose lists equal `vcs_rules.py`; no `src/superclaude/` path; no branch-deletion argv; helper and protocol byte parity with `plugins/` |
| `tests/skills/test_implement_commit_rules.py` | T-09, T-15, T-16, T-24, T-25 | option row and Will Not text; STOP rows; the load rule; `--commit-tasks` string appears only in the FR-052 files; unflagged run behavior; FINAL reads current files; grant provenance |
| `tests/commands/test_git_command.py` | T-12 | front matter, usage forms, section order, one Activation line, no Unattended section, Will Not text |
| extend `tests/skills/test_workflow_archive.py` | T-11 | a package with `commits.md` archives unchanged; an unsettled boundary blocks; `archive_workspace.py` unchanged |
| extend `tests/commands/test_routing_plugin_parity.py`, `tests/recommend/test_routing_refresh.py` fixtures, `tests/skills/test_worker_contract.py`, `tests/docs/test_retired_docs_absent.py` | T-14, AC-04, AC-13 | updates listed in §7 |

Real-framework hook tests (FR-118) skip when `pre-commit` is not installed (DD-7). Test-first order inside each phase: write the failing test from the requirement, then the code or text. T-18 is the final gate: `make verify-sync` exits 0 and `uv run pytest tests/core tests/commands tests/skills tests/recommend tests/docs tests/vcs tests/worktree_cleanup` passes.

`````

### .dev/tasks/to-do/TASK-WF-design-20261126-162939/source.md:460-477

`````markdown
## 10. Build sequence for the plan

Ordered so the riskiest, least certain work is proven first and each phase has a gate. Sizes are relative (S, M, L); the issue estimate is about 40 hours in total.

| Phase | Scope | Depends on | Gate | Size |
|---|---|---|---|---|
| P0 | Baseline and scaffolding: record a green baseline of the T-18 test set; create `tests/vcs/` and its fixtures; build the hook emulator; optional spike that checks the emulator against the real framework with `uv run --with pre-commit` in a temporary directory (answers the UNVERIFIED items of FR-118 early) | none | baseline recorded; fixtures import | M |
| P1 | `vcs_rules.py`, `GitRunner`, `emit`, verbs `preflight` and `check-message`, safety constants | P0 | T-02, T-03, T-06, T-08 | M |
| P2 | `vcs_submodules.py` and verb `submodules` | P1 | T-07 | M |
| P3 | Pure core in `vcs_plan.py`: ledger reader (DD-8), sidecar parser, segments, keys (DD-1), `derive_state` (DD-5, DD-11) | P0 | T-10, pure part of T-19, ledger-regex parity | M |
| P4 | `stage-plan` (incl. `--candidate`), `verify`, `reconcile`, `resolve-check` | P1, P3 | T-01, T-04, T-05, T-19, T-22, T-23 | L |
| P5 | `/sc:git` command and protocol skill (registry, five refs), delete `commands/sc-git.md`, plugin mirror, README, parity parametrization, `sync-dev` | P1, P2 | T-12, T-13, T-17, T-26, T-27 | M |
| P6 | Implement integration: `--commit-tasks`, Wave 0 steps 5b and 6b, Q8a, R0, L0, `refs/commit-step.md`, STOP rows, archive-gate text, Row 1 and pin-lifetime amendments, Ruling text, K3 sentence | P4 | T-09, T-11, T-15, T-16, T-20, T-21, T-24, T-25 | L |
| P7 | Routing guide row, fixture S23, worker-contract scan, user docs, plugin copies, `make sync-dev` and `verify-sync` | P5, P6 | T-14, T-18, AC-01..AC-21 | M |
| P8 | Final check: run every acceptance observation of §14 of the requirements; PR text (see open item O5) | P7 | all AC pass | S |

Parallelism: P1, P2 and P3 can run in parallel after P0. P5 needs only P1 and P2, so it can run in parallel with P3 and P4. P6 is the critical path (P3 then P4 then P6). If the owner prefers two reviews, P0 to P5 (the `/sc:git` side and the helper) and P6 to P8 (the implement side) form a natural split at the P5/P6 boundary.

`````

### .dev/tasks/to-do/TASK-WF-design-20261126-162939/source.md:478-500

`````markdown
## 11. Validation against the existing code

Each item was read in this run (Read, Grep, Glob or codegraph), after the single readiness check at the top.

| Claim | Evidence |
|---|---|
| Wave 0 step 5 resolves the ledger path and step 6 opens or creates the ledger; step 9 is the single codegraph check and writes `codegraph.md` | `skills/sc-implement-protocol/SKILL.md:71`, `:72`, `:75`, `:79` |
| Q0 snapshots with a private index and pins `refs/superclaude/implement/<slug>/T<id>`; the cleanup sentence is at line 129; Q8 is at line 150 | `SKILL.md:121-129`, `:149-150` |
| Known options are listed at `SKILL.md:57`; the closed STOP sentence is at `:51`; the STOP table includes `E-LEDGER-CORRUPT` at `:42` | `SKILL.md:42`, `:51`, `:57` |
| The legacy all-complete stop sentence is in `refs/ledger.md`; the unknown-last-line rule is at line 127 | `refs/ledger.md:127`, `:139` |
| The archive gate is agent-run protocol text (steps 1 to 5); the helper checks ledger records only | `refs/managed-workspace.md:50-56` |
| `archive_workspace.py` exposes `_parse_ledger`, `validate`, `archive`, `print_state`, `main` and the line regexes `_START`, `_VERDICT`, `_RULING`, `_RETRY`, `_HALT`, `_PLAN`, `_FINAL` | codegraph file outline of `skills/sc-implement-protocol/scripts/archive_workspace.py` (lines 44-67, 181, 278, 477, 557, 579) |
| `_remove_branch` is the only local branch deletion and sits at line 2636 | codegraph search; `scripts/worktree_cleanup.py:2636` |
| Existing test precedent loads a skill script by path, runs it with `subprocess`, and asserts byte parity with `plugins/` | `tests/skills/test_workflow_archive.py:22-27`, `:671-678`, `:1033-1035` |
| Plugin parity test parametrization is at line 41; the plugin build copies `plugins/superclaude/` unchanged (`PLUGIN_SRC` at line 16, `copytree` at line 47) | `tests/commands/test_routing_plugin_parity.py:41`; `scripts/build_superclaude_plugin.py:16`, `:47`, `:77` |
| `make sync-dev` copies commands into `.claude/commands/sc/`; `make verify-sync` diffs them | `Makefile:109`, `:131-135`, `:166`, `:232-236` |
| The guard classes a command as git only from its text (`LL_GIT`), and classes `--no-verify` as TAMPER | `hooks/scripts/launch-level-guard.sh:556-557`, `:786` |
| `WORKER-CONTRACT.md` has no plugin mirror | Glob of `plugins/superclaude/**/WORKER-CONTRACT.md` found nothing |
| Today the user guide documents the old usage and a `merge ... --interactive` example | `docs/user-guide/commands.md:1265`, `:1273`; `docs/user-guide/flags.md:136-140` |
| `/sc:git` is on the never-as-worker list in the developer guide and the worker contract | `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:982`; `src/superclaude/core/WORKER-CONTRACT.md:23` (cited by the requirements, read by the debate agents) |

Carried forward as UNVERIFIED (the requirements mark them too; none blocks the design, each has a test or a spike): the git version that first supports `--pathspec-from-file` for both `add` and `commit` (believed 2.25, checked by T-08); whether `-c core.fsmonitor=false` protects against every program a submodule's config could start (risk 5); the real `pre-commit` framework's behavior under `--only` (spike in P0, T-20); whether `file://` submodule tests work on the CI image (T-07); which implement tests pin the STOP table exactly (§7); whether the old automated sync could re-create `commands/sc-git.md` (risk 8, guarded by the absence test); whether `allowed-tools` in skill front matter restricts tools (risk 14, not relied on); the helper latency target (NFR-008, no baseline).

`````

### .dev/tasks/to-do/TASK-WF-design-20261126-162939/source.md:501-518

`````markdown
## 12. Traceability

| Requirement range | Component | Section | Tests |
|---|---|---|---|
| FR-001..FR-009, FR-018, FR-019 | C1 | §3 | T-12, T-13 |
| FR-010..FR-013, NFR-006..NFR-009, NFR-011, NFR-014 | C2 | §4 | T-02, T-03, T-06, T-08, T-13 |
| FR-014..FR-017, FR-080..FR-082, FR-090..FR-094 | C5 | §7 | T-14, T-17, AC-04, AC-11, AC-13 |
| FR-020..FR-023 | C1 | §3.4 | T-13 |
| FR-030..FR-039 | C1 + C2 | §3.4, §4.5 | T-01, T-02, T-04, T-05, T-23, T-26, T-27 |
| FR-040..FR-046 | C1 + C2 | §4.6 | T-07 |
| FR-050..FR-053, FR-054, FR-056..FR-059, FR-077, FR-079 | C3 | §5.2, §5.3, §5.9 | T-09, T-15, T-16, T-24, T-25 |
| FR-060..FR-067, FR-073..FR-076, FR-078 | C3 + C2 | §5.5, §4.5 | T-01, T-04, T-06, T-19 |
| FR-070..FR-072 | C3 | §5.1, §8 | T-09, T-11 |
| FR-100..FR-109, FR-130..FR-133 | C3 + C2 | §5.4 to §5.8 | T-10, T-19, T-22 |
| FR-110..FR-118 | C4 + C2 | §6.1 | T-20 |
| FR-120..FR-126 | C4 + C2 | §6.2 | T-21 |
| NFR-001..NFR-005, NFR-010, NFR-012..NFR-018 | all | §2.2, §8 | T-03, T-13, T-16, T-17 |

`````

### .dev/tasks/to-do/TASK-WF-design-20261126-162939/source.md:519-530

`````markdown
## 13. Open items for the plan review

| # | Item | Why it matters | Suggested handling |
|---|---|---|---|
| O1 | DD-11: a `prepared` line without its pins and HEAD still equal to the parent is `pending` (retry as attempt n+1), not `uncertain` | FR-108 and FR-111 can be read two ways; both fail closed | Confirm in plan review; the `derive_state` table and T-22 need one reading |
| O2 | DD-10: `config --get-regexp` in the helper allow-list | FR-011 names `config --get` only | Add to the allow-list parity test (T-03) when P1 lands |
| O3 | User guide updates (`commands.md`, `flags.md`) are added by this design | They would be stale after the refactor; they are outside the requirement list | Keep as small tasks in P7; the owner can strike them at plan approval |
| O4 | `HOW-WE-WORK.md` may need to mention `--commit-tasks` | FR-052 allows the string there but no requirement says it must appear | Decide when editing the routing row in P7; if it does not appear, the static list in T-15 still holds |
| O5 | The pull request may need a `## Generator-Constraint Considered` body section if a gate or validator file changes (user memory note; which files the check covers is UNVERIFIED) | Without it CI can fail | Check the touched files at P8 and add the section if needed |
| O6 | Review load: one large pull request versus two | Size L, about 40 hours | The P5/P6 boundary is the natural split; the owner decides at plan approval |
| O7 | The minor review notes left open by the merge (M3-2, M3-3, M3-7, M3-9 and parts of M3-4 and M3-6) are listed in `adversarial/adversarial/merge-log.md` | They are wording and placement points that do not change a requirement | Re-read them when writing the refs in P5 and P6 |

`````

### .dev/tasks/to-do/TASK-WF-design-20261126-162939/TASK-WF-design-20261126-162939.md:32-53

`````markdown
## Phase 1: Test scaffolding and hook emulation

## Task 1: Create the shared test fixtures for the vcs helper and record the test baseline

Create `tests/vcs/conftest.py` and `tests/vcs/test_fixtures.py`, following the layout of `tests/worktree_cleanup/conftest.py` (reuse or mirror its `git_in` helper and its throwaway-repository and local bare-remote builders). Fixtures: `repo` (temporary git repository with a local bare remote), `ledger_builder` (writes an implement ledger from the closed grammar: header line, `PLAN:` line, `T<id>: start sha=...`, `T<id>: complete verdict=... files=...`, `Ruling`, `halt`, `FINAL` lines; the grammar is the one in `src/superclaude/skills/sc-implement-protocol/refs/ledger.md` and the regexes in `archive_workspace.py` lines 44-67), `sidecar_builder` (writes `commits.md` lines from the forms in section 5.8 of ./source.md), `submodule_repo` (superproject plus a `file://` submodule, setting `protocol.file.allow=always` only inside its own temporary repositories), and `scripts_dir` (adds `src/superclaude/skills/sc-git-protocol/scripts` to `sys.path` lazily, so tests skip cleanly until that folder exists). Load `archive_workspace.py` by path with `importlib.util.spec_from_file_location`, as `tests/skills/test_workflow_archive.py` lines 22-27 does. Then run the existing final-gate test set without `tests/vcs` (`uv run pytest tests/core tests/commands tests/skills tests/recommend tests/docs tests/worktree_cleanup -q`) and save the summary to `./artifacts/baseline-tests.log`, listing any test that already fails before this work.

Acceptance criteria:
- `uv run pytest tests/vcs/test_fixtures.py -q` passes: a ledger written by `ledger_builder` is accepted by `archive_workspace._parse_ledger`, `sidecar_builder` writes every line form of FR-100 and FR-120, and `submodule_repo` yields a superproject whose submodule status line can be read.
- `./artifacts/baseline-tests.log` exists, states the command, the pass and fail counts and the names of pre-existing failures (or "none").
- `tests/worktree_cleanup/` and `src/superclaude/skills/sc-implement-protocol/scripts/archive_workspace.py` are unchanged.

## Task 2: Build the hook-manager emulator fixture and the optional real-framework spike

Depends on: Task 1

Add the `hook_emulator` fixture to `tests/vcs/conftest.py` and tests in `tests/vcs/test_hook_emulator.py` (FR-118, risk 15 in ./source.md section 6.1). The emulator installs a `pre-commit` hook script in the temporary repository that replays the hook framework's command sequence under `git commit --only`: save unstaged tracked changes as a patch file in a temporary cache folder, check out the tree, run a configurable hook action (pass, exit 1, rewrite a file and exit 1, rewrite a file and `git add` it, block until killed), then re-apply the patch. The module docstring names the framework source revision the sequence was copied from, or says UNVERIFIED when the revision could not be confirmed. Add `tests/vcs/test_precommit_spike.py`, which compares the emulator with the real framework and skips when `pre-commit` is not on `PATH`; try the spike once with `uv run --with pre-commit` inside a temporary directory and record the outcome (it ran, or why it could not) in `./artifacts/precommit-spike.md`.

Acceptance criteria:
- `tests/vcs/test_hook_emulator.py` shows: on success the person's unstaged edit outside the commit set is restored; after SIGKILL during the hook the edit exists only in the saved patch; an edit to an assume-unchanged file is overwritten even without a kill; a hook that exits 1 leaves HEAD unchanged.
- `tests/vcs/test_precommit_spike.py` is skipped (not failed) when the framework is absent, and `./artifacts/precommit-spike.md` records the real outcome.
- No file outside `tests/vcs/` and `./artifacts/` is changed.

`````


## Coverage slice

| Requirement id | Card ID | Status | Grounding |
|---|---|---|---|
| FR-003: / C1 / `/sc:git` command + `sc-git-protocol` skill / A thin command fi | - | NOT named in plan text | source.md:15 |
| FR-004: / C1 / `/sc:git` command + `sc-git-protocol` skill / A thin command fi | - | NOT named in plan text | source.md:15 |
| FR-007: / C1 / `/sc:git` command + `sc-git-protocol` skill / A thin command fi | - | NOT named in plan text | source.md:15 |
| FR-015: / C1 / `/sc:git` command + `sc-git-protocol` skill / A thin command fi | - | NOT named in plan text | source.md:15 |
| FR-016: / C1 / `/sc:git` command + `sc-git-protocol` skill / A thin command fi | - | NOT named in plan text | source.md:15 |
| FR-020: / C1 / `/sc:git` command + `sc-git-protocol` skill / A thin command fi | - | NOT named in plan text | source.md:15 |
| FR-021: / C1 / `/sc:git` command + `sc-git-protocol` skill / A thin command fi | - | NOT named in plan text | source.md:15 |
| FR-024: / C1 / `/sc:git` command + `sc-git-protocol` skill / A thin command fi | - | NOT named in plan text | source.md:15 |
| FR-025: / C1 / `/sc:git` command + `sc-git-protocol` skill / A thin command fi | - | NOT named in plan text | source.md:15 |
| FR-026: / C1 / `/sc:git` command + `sc-git-protocol` skill / A thin command fi | - | NOT named in plan text | source.md:15 |
| FR-027: / C1 / `/sc:git` command + `sc-git-protocol` skill / A thin command fi | - | NOT named in plan text | source.md:15 |
| FR-028: / C1 / `/sc:git` command + `sc-git-protocol` skill / A thin command fi | - | NOT named in plan text | source.md:15 |
| FR-029: / C1 / `/sc:git` command + `sc-git-protocol` skill / A thin command fi | - | NOT named in plan text | source.md:15 |
| FR-037: / C1 / `/sc:git` command + `sc-git-protocol` skill / A thin command fi | - | NOT named in plan text | source.md:15 |
| FR-061: / C2 / `vcs` helper (skill script) / Read-only Python that computes fa | - | NOT named in plan text | source.md:16 |
| FR-106: / C2 / `vcs` helper (skill script) / Read-only Python that computes fa | - | NOT named in plan text | source.md:16 |
| FR-123: / C2 / `vcs` helper (skill script) / Read-only Python that computes fa | - | NOT named in plan text | source.md:16 |
| NFR-007: / C2 / `vcs` helper (skill script) / Read-only Python that computes fa | - | NOT named in plan text | source.md:16 |
| FR-055: / C3 / Commit step in `sc-implement-protocol` / New flag `--commit-tas | - | NOT named in plan text | source.md:17 |
| FR-056: / C3 / Commit step in `sc-implement-protocol` / New flag `--commit-tas | - | NOT named in plan text | source.md:17 |
| FR-057: / C3 / Commit step in `sc-implement-protocol` / New flag `--commit-tas | - | NOT named in plan text | source.md:17 |
| FR-059: / C3 / Commit step in `sc-implement-protocol` / New flag `--commit-tas | - | NOT named in plan text | source.md:17 |
| FR-068: / C3 / Commit step in `sc-implement-protocol` / New flag `--commit-tas | - | NOT named in plan text | source.md:17 |
| FR-069: / C3 / Commit step in `sc-implement-protocol` / New flag `--commit-tas | - | NOT named in plan text | source.md:17 |
| FR-074: / C3 / Commit step in `sc-implement-protocol` / New flag `--commit-tas | - | NOT named in plan text | source.md:17 |
| FR-075: / C3 / Commit step in `sc-implement-protocol` / New flag `--commit-tas | - | NOT named in plan text | source.md:17 |
| FR-104: / C3 / Commit step in `sc-implement-protocol` / New flag `--commit-tas | - | NOT named in plan text | source.md:17 |
| FR-105: / C3 / Commit step in `sc-implement-protocol` / New flag `--commit-tas | - | NOT named in plan text | source.md:17 |
| FR-109: / C3 / Commit step in `sc-implement-protocol` / New flag `--commit-tas | - | NOT named in plan text | source.md:17 |
| FR-111: / C4 / Worktree protection and owner resolution / Snapshot before and  | - | NOT named in plan text | source.md:18 |
| FR-114: / C4 / Worktree protection and owner resolution / Snapshot before and  | - | NOT named in plan text | source.md:18 |
| FR-115: / C4 / Worktree protection and owner resolution / Snapshot before and  | - | NOT named in plan text | source.md:18 |
| FR-119: / C4 / Worktree protection and owner resolution / Snapshot before and  | - | NOT named in plan text | source.md:18 |
| FR-121: / C4 / Worktree protection and owner resolution / Snapshot before and  | - | NOT named in plan text | source.md:18 |
| FR-122: / C4 / Worktree protection and owner resolution / Snapshot before and  | - | NOT named in plan text | source.md:18 |
| FR-124: / C4 / Worktree protection and owner resolution / Snapshot before and  | - | NOT named in plan text | source.md:18 |
| FR-125: / C4 / Worktree protection and owner resolution / Snapshot before and  | - | NOT named in plan text | source.md:18 |
| FR-083: / C5 / Surrounding surfaces / Routing row, fixture S23, worker contrac | - | NOT named in plan text | source.md:19 |
| FR-084: / C5 / Surrounding surfaces / Routing row, fixture S23, worker contrac | - | NOT named in plan text | source.md:19 |
| FR-085: / C5 / Surrounding surfaces / Routing row, fixture S23, worker contrac | - | NOT named in plan text | source.md:19 |
| FR-086: / C5 / Surrounding surfaces / Routing row, fixture S23, worker contrac | - | NOT named in plan text | source.md:19 |
| FR-087: / C5 / Surrounding surfaces / Routing row, fixture S23, worker contrac | - | NOT named in plan text | source.md:19 |
| FR-088: / C5 / Surrounding surfaces / Routing row, fixture S23, worker contrac | - | NOT named in plan text | source.md:19 |
| FR-089: / C5 / Surrounding surfaces / Routing row, fixture S23, worker contrac | - | NOT named in plan text | source.md:19 |
| NFR-016: / I6 / Fail closed: a missing helper, pin, `q0-head`, or an unknown to | - | NOT named in plan text | source.md:84 |
| AC-04: / `tests/commands/test_routing_plugin_parity.py` (line 41) / `@pytest. | - | NOT named in plan text | source.md:403 |
| AC-13: / `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` / Byte | - | NOT named in plan text | source.md:405 |
| T-14: / `tests/recommend/fixtures/routing_refresh_cases.json` (S23, lines 31 | - | NOT named in plan text | source.md:407 |
| AC-11: Unchanged and asserted unchanged: `scripts/worktree_cleanup.py` (`_rem | - | NOT named in plan text | source.md:413 |
| NFR-014: `vcs_contract: "1"`; both protocols refuse any other value (`helper-mi | - | NOT named in plan text | source.md:431 |
| NFR-011: / `tests/vcs/test_preflight.py` / T-08 / detached HEAD, protected name | - | NOT named in plan text | source.md:447 |
| T-18: Real-framework hook tests (FR-118) skip when `pre-commit` is not insta | - | NOT named in plan text | source.md:458 |
| AC-02: / P7 / Routing guide row, fixture S23, worker-contract scan, user docs | - | NOT named in plan text | source.md:473 |
| AC-03: / P7 / Routing guide row, fixture S23, worker-contract scan, user docs | - | NOT named in plan text | source.md:473 |
| AC-05: / P7 / Routing guide row, fixture S23, worker-contract scan, user docs | - | NOT named in plan text | source.md:473 |
| AC-06: / P7 / Routing guide row, fixture S23, worker-contract scan, user docs | - | NOT named in plan text | source.md:473 |
| AC-07: / P7 / Routing guide row, fixture S23, worker-contract scan, user docs | - | NOT named in plan text | source.md:473 |
| AC-08: / P7 / Routing guide row, fixture S23, worker-contract scan, user docs | - | NOT named in plan text | source.md:473 |
| AC-09: / P7 / Routing guide row, fixture S23, worker-contract scan, user docs | - | NOT named in plan text | source.md:473 |
| AC-10: / P7 / Routing guide row, fixture S23, worker-contract scan, user docs | - | NOT named in plan text | source.md:473 |
| AC-12: / P7 / Routing guide row, fixture S23, worker-contract scan, user docs | - | NOT named in plan text | source.md:473 |
| AC-14: / P7 / Routing guide row, fixture S23, worker-contract scan, user docs | - | NOT named in plan text | source.md:473 |
| AC-15: / P7 / Routing guide row, fixture S23, worker-contract scan, user docs | - | NOT named in plan text | source.md:473 |
| NFR-004: / NFR-001..NFR-005, NFR-010, NFR-012..NFR-018 / all / §2.2, §8 / T-03, | - | NOT named in plan text | source.md:517 |
| NFR-005: / NFR-001..NFR-005, NFR-010, NFR-012..NFR-018 / all / §2.2, §8 / T-03, | - | NOT named in plan text | source.md:517 |
| NFR-013: / NFR-001..NFR-005, NFR-010, NFR-012..NFR-018 / all / §2.2, §8 / T-03, | - | NOT named in plan text | source.md:517 |
| NFR-015: / NFR-001..NFR-005, NFR-010, NFR-012..NFR-018 / all / §2.2, §8 / T-03, | - | NOT named in plan text | source.md:517 |
