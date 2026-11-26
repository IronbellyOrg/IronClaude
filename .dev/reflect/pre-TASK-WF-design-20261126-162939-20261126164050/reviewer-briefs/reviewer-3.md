# Reviewer brief 3 (refactorer)

## T1 card excerpt

## Scope and what was read

The plan has 8 phases and 38 tasks (`TASK-WF-design-20261126-162939.md:32` onward). Lines 1-150 (constitution, Phases 1 to 4 up to Task 11) were read line by line. Tasks 12 to 38 were checked structurally only (plan gate, a dependency-order script, design-term counts), not read line by line. The design (`source.md`, 529 lines) was read by section heading and by targeted Grep.

## Candidate findings

F1 (Medium, may be blocking at implement time). Plan Constraint line 29 says "No code or text uses `--no-verify`, `-n` on commit, `SKIP=`, `commit-tree` or `--amend`" (`TASK-WF-design-20261126-162939.md:29`). Task 3 must write those strings into `FORBIDDEN_FLAGS` (`:60`), and later tasks quote them in acceptance checks (`:172`, `:193`). The implement protocol treats `## Constraints` items as global constraints whose breach, when the reviewer can quote the text, is a blocking `quoted-constraint-breach` (`src/superclaude/skills/sc-implement-protocol/SKILL.md:106`, `refs/qa.md:52`). A strict reviewer can read the deny-list as "text that uses `--no-verify`". Fix: reword line 29 to say no command or argv the code runs, and no recommendation in the primitives, uses them, and that deny-lists and tests of refusals are allowed.

F2 (Note). Declared dependencies are incomplete. Task 6 (`:88-90`) adds a verb to `vcs.py` and uses `vcs_plan.py` but depends only on Task 3; Task 8 (`:110-112`) wires a verb into `vcs.py` and depends on Task 7; Tasks 9 to 12 (`:122-124`, `:132-134`, `:142-144`, `:152`) extend `vcs_plan.py` (created by Task 4, `:66-68`) without depending on Task 4. `vcs.py` is created by Task 5 (`:77-79`). `/sc:implement` ignores `depends-on` and runs source order unless a set is marked `independent` (`SKILL.md:92`, `:110`), and the plan marks none, so execution is unaffected. Script output: `artifacts/dependency-check.txt` (other lines in that file are the ambiguous name `SKILL.md` and forward mentions of files a task only links to, not defects).

F3 (information). Open items O1 to O7 (`source.md:519-529`) stay open by design; the plan does not resolve O1 (DD-11 reading) and says so in the design, so Task 12 and the T-22 test depend on the owner's reading.

## Risk surface

Blast radius the plan names and covers: the pinned STOP-table format test and the "No other `E-*` codes" sentence (implement `SKILL.md` and `tests/skills/test_task_workspace_lifecycle.py`), the write-verb scan and its classification rows, plugin byte parity, the routing row and fixture S23, and the unchanged-file rules for `archive_workspace.py` and `scripts/worktree_cleanup.py` (pre-check: `artifacts/codegraph-grounding.md`, 73 checks, all OK). Untested invariant: real hook-framework behavior (UNVERIFIED, handled by the emulator in Task 2).

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

### .dev/tasks/to-do/TASK-WF-design-20261126-162939/source.md:519-529

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

### .dev/reflect/pre-TASK-WF-design-20261126-162939-20261126164050/artifacts/dependency-check.txt:1-21

`````markdown
tasks 38 created files tracked 13
('NO-DEP-ON-CREATOR', 6, 'vcs_plan.py', 4)  | task line 88 | creator line 66
('NO-DEP-ON-CREATOR', 6, 'vcs.py', 5)  | task line 88 | creator line 77
('NO-DEP-ON-CREATOR', 8, 'vcs.py', 5)  | task line 110 | creator line 77
('NO-DEP-ON-CREATOR', 9, 'vcs_plan.py', 4)  | task line 122 | creator line 66
('NO-DEP-ON-CREATOR', 10, 'vcs_plan.py', 4)  | task line 132 | creator line 66
('FORWARD', 10, 'commit-step.md', 27)  | task line 132 | creator line 310
('NO-DEP-ON-CREATOR', 11, 'vcs_plan.py', 4)  | task line 142 | creator line 66
('NO-DEP-ON-CREATOR', 12, 'vcs_plan.py', 4)  | task line 152 | creator line 66
('FORWARD', 16, 'SKILL.md', 20)  | task line 196 | creator line 238
('FORWARD', 19, 'SKILL.md', 20)  | task line 228 | creator line 238
('NO-DEP-ON-CREATOR', 20, 'vcs.py', 5)  | task line 238 | creator line 77
('FORWARD', 20, 'safety.md', 21)  | task line 238 | creator line 248
('FORWARD', 20, 'commit.md', 21)  | task line 238 | creator line 248
('FORWARD', 20, 'status.md', 22)  | task line 238 | creator line 258
('FORWARD', 20, 'branch.md', 22)  | task line 238 | creator line 258
('FORWARD', 20, 'submodule.md', 23)  | task line 238 | creator line 268
('NO-DEP-ON-CREATOR', 26, 'SKILL.md', 20)  | task line 300 | creator line 238
('FORWARD', 26, 'commit-step.md', 27)  | task line 300 | creator line 310
('NO-DEP-ON-CREATOR', 30, 'SKILL.md', 20)  | task line 340 | creator line 238
('NO-DEP-ON-CREATOR', 34, 'SKILL.md', 20)  | task line 380 | creator line 238
`````


## Coverage slice

| Phase | Title | Plan line | Tasks |
|---|---|---|---|
| P1 | Test scaffolding and hook emulation | 32 | 1-2 (2 tasks) |
| P2 | Helper foundations: rules, runner, entry point, preflight, message check | 54 | 3-6 (4 tasks) |
| P3 | Submodule facts and operations | 98 | 7-8 (2 tasks) |
| P4 | Pure commit-state core | 120 | 9-12 (4 tasks) |
| P5 | Helper planning, verification and recovery verbs | 162 | 13-18 (6 tasks) |
| P6 | /sc:git command and protocol skill | 226 | 19-25 (7 tasks) |
| P7 | Commit step in /sc:implement | 298 | 26-34 (9 tasks) |
| P8 | Routing guide, worker-contract tables, user docs and plugin mirrors | 390 | 35-38 (4 tasks) |
