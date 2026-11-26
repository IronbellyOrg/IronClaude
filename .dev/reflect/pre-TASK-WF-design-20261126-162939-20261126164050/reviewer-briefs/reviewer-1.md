# Reviewer brief 1 (analyzer)

## T1 card excerpt

## Scope and what was read

The plan has 8 phases and 38 tasks (`TASK-WF-design-20261126-162939.md:32` onward). Lines 1-150 (constitution, Phases 1 to 4 up to Task 11) were read line by line. Tasks 12 to 38 were checked structurally only (plan gate, a dependency-order script, design-term counts), not read line by line. The design (`source.md`, 529 lines) was read by section heading and by targeted Grep.

## Candidate findings

F1 (Medium, may be blocking at implement time). Plan Constraint line 29 says "No code or text uses `--no-verify`, `-n` on commit, `SKIP=`, `commit-tree` or `--amend`" (`TASK-WF-design-20261126-162939.md:29`). Task 3 must write those strings into `FORBIDDEN_FLAGS` (`:60`), and later tasks quote them in acceptance checks (`:172`, `:193`). The implement protocol treats `## Constraints` items as global constraints whose breach, when the reviewer can quote the text, is a blocking `quoted-constraint-breach` (`src/superclaude/skills/sc-implement-protocol/SKILL.md:106`, `refs/qa.md:52`). A strict reviewer can read the deny-list as "text that uses `--no-verify`". Fix: reword line 29 to say no command or argv the code runs, and no recommendation in the primitives, uses them, and that deny-lists and tests of refusals are allowed.

F2 (Note). Declared dependencies are incomplete. Task 6 (`:88-90`) adds a verb to `vcs.py` and uses `vcs_plan.py` but depends only on Task 3; Task 8 (`:110-112`) wires a verb into `vcs.py` and depends on Task 7; Tasks 9 to 12 (`:122-124`, `:132-134`, `:142-144`, `:152`) extend `vcs_plan.py` (created by Task 4, `:66-68`) without depending on Task 4. `vcs.py` is created by Task 5 (`:77-79`). `/sc:implement` ignores `depends-on` and runs source order unless a set is marked `independent` (`SKILL.md:92`, `:110`), and the plan marks none, so execution is unaffected. Script output: `artifacts/dependency-check.txt` (other lines in that file are the ambiguous name `SKILL.md` and forward mentions of files a task only links to, not defects).

F3 (information). Open items O1 to O7 (`source.md:519-529`) stay open by design; the plan does not resolve O1 (DD-11 reading) and says so in the design, so Task 12 and the T-22 test depend on the owner's reading.

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

### .dev/tasks/to-do/TASK-WF-design-20261126-162939/source.md:75-104

`````markdown
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

### .dev/tasks/to-do/TASK-WF-design-20261126-162939/source.md:316-334

`````markdown
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

`````


## Coverage slice

| Requirement id | Card ID | Status | Grounding |
|---|---|---|---|
| T-03: / I3 / The helper writes no ref, user index, work-tree file or config; | - | named in plan | source.md:81 |
| T-22: / I8 / At most one commit per boundary key, across crashes and resumes | - | named in plan | source.md:86 |
| DD-1: / DD-1 / The boundary key's "ledger identity" is the token `managed:<s | - | named in plan | source.md:95 |
| DD-2: / DD-2 / The helper is one entry script plus three sibling modules, ru | - | named in plan | source.md:96 |
| DD-3: / DD-3 / All helper JSON goes through one `emit(obj)` function that so | - | named in plan | source.md:97 |
| DD-4: / DD-4 / Commit message text is written by the agent to a temporary fi | - | named in plan | source.md:98 |
| DD-5: / DD-5 / The reconcile result is a JSON list of boundaries with a fixe | - | named in plan | source.md:99 |
| DD-6: / DD-6 / The `run` line field `args=` records the option prefix only,  | - | named in plan | source.md:100 |
| DD-7: / DD-7 / New tests live under `tests/vcs/` (helper and git behavior, r | - | named in plan | source.md:101 |
| DD-8: / DD-8 / The helper's ledger reader reuses the exact line regexes of ` | - | named in plan | source.md:102 |
| DD-9: / DD-9 / The runner allow-list is a table `verb -> permitted option to | - | named in plan | source.md:103 |
| DD-10: / DD-10 / Reading git config uses `config --get` and `config --get-reg | - | named in plan | source.md:104 |
| T-13: At most two refs load per invocation: the operation's group ref plus ` | - | named in plan | source.md:151 |
| T-17: Branch `create` runs `git switch -c <name>` and refuses a protected or | - | named in plan | source.md:163 |
| T-02: 7. `add_argv` and `commit_argv` have exactly the FR-035 shape and neve | - | named in plan | source.md:232 |
| T-11: / `scripts/archive_workspace.py` / **No change** (verified by a byte-e | - | named in plan | source.md:254 |
| DD-11: / `prepared` appended, before pins exist / `prepared` line, HEAD = par | - | named in plan | source.md:326 |
| T-10: Location: legacy `.dev/implement/<slug>/commits.md` (never staged, lik | - | named in plan | source.md:350 |
| T-16: A run without the flag and with no `commits.md` adds no Bash call and  | - | named in plan | source.md:365 |
| T-14: / `tests/recommend/fixtures/routing_refresh_cases.json` (S23, lines 31 | - | NOT named in plan text | source.md:407 |
| T-01: / `tests/vcs/test_stage_plan.py` / T-01, T-23 / path rules, deletions, | - | named in plan | source.md:440 |
| T-23: / `tests/vcs/test_stage_plan.py` / T-01, T-23 / path rules, deletions, | - | named in plan | source.md:440 |
| T-04: / `tests/vcs/test_hook_refusal.py` / T-04 / each FR-036 class and its  | - | named in plan | source.md:443 |
| T-05: / `tests/vcs/test_only_semantics.py` / T-05 / `git commit --only` leav | - | named in plan | source.md:444 |
| T-06: / `tests/vcs/test_check_message.py` / T-06 / 72-code-point rule, trail | - | named in plan | source.md:445 |
| T-07: / `tests/vcs/test_submodules.py` / T-07 / local superproject with a `f | - | named in plan | source.md:446 |
| T-08: / `tests/vcs/test_preflight.py` / T-08 / detached HEAD, protected name | - | named in plan | source.md:447 |
| T-19: / `tests/vcs/test_eligibility.py` / T-19, T-22 (pure part), T-10 / seg | - | named in plan | source.md:448 |
| T-20: / `tests/vcs/test_worktree_protection.py` / T-20, AC-17 / emulated SIG | - | named in plan | source.md:450 |
| T-21: / `tests/vcs/test_resolution.py` / T-21, AC-18 / every unsettled state | - | named in plan | source.md:451 |
| T-09: / `tests/skills/test_implement_commit_rules.py` / T-09, T-15, T-16, T- | - | named in plan | source.md:453 |
| T-15: / `tests/skills/test_implement_commit_rules.py` / T-09, T-15, T-16, T- | - | named in plan | source.md:453 |
| T-24: / `tests/skills/test_implement_commit_rules.py` / T-09, T-15, T-16, T- | - | named in plan | source.md:453 |
| T-25: / `tests/skills/test_implement_commit_rules.py` / T-09, T-15, T-16, T- | - | named in plan | source.md:453 |
| T-12: / `tests/commands/test_git_command.py` / T-12 / front matter, usage fo | - | named in plan | source.md:454 |
| T-18: Real-framework hook tests (FR-118) skip when `pre-commit` is not insta | - | NOT named in plan text | source.md:458 |
| T-26: / P5 / `/sc:git` command and protocol skill (registry, five refs), del | - | named in plan | source.md:471 |
| T-27: / P5 / `/sc:git` command and protocol skill (registry, five refs), del | - | named in plan | source.md:471 |
