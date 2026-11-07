# Reviewer brief 2 (qa lens, haiku slot; pre-execution plan audit, read-only)

Repository root: `/home/coder/workspaces/worktrees/IronClaude/WorkerContractFollowups` (all relative paths resolve against it).

You audit the plan `.dev/tasks/to-do/TASK-WF-workerContractFo-20261106-214402/TASK-WF-workerContractFo-20261106-214402.md` against its brief `.dev/tasks/to-do/TASK-WF-workerContractFo-20261106-214402/source.md` (mode pre, UC-1). You are read-only: no edits, no shell, no git. Audit the hunks below and anything you Read, Grep or Glob in the repository.

Persona focus: testability. For every acceptance criterion, is there a command or an assertion that would fail if the work were wrong? Check: (a) the brief's verification command list (source.md:36) against the plan's Task 5 final criterion; (b) whether the plan's new assertions (WC-4 "git ignores" and "outside the repository"; workflow and build "WC-4"; test clause "WC-4" and `[]`; init-lite "exited 0") would pass on today's text (a check that already passes proves nothing); (c) whether any existing assertion in `tests/skills/test_worker_contract.py` (for example the `test_unattended_artifacts_list_only_files_the_run_wrote` asserts at :799 and :808, or the init-lite `_artifacts_clause` checks) would break on the planned wording and is not named in the plan.

Return findings as YAML: a list of items with id, priority (P1 blocks /sc:implement or makes a planned test pass on wrong text; P2 a defect a reviewer or test would catch; P3 cosmetic or an owner note), claim, evidence (file:line for every claim, or tag the claim [INFERRED]), exact_change and verifier; then self_reported_confidence (0-1) and a short list of what you checked and found clean. A zero-finding answer needs a self-audit naming what you checked.

## T1 card excerpt

The orchestrator's Tier 1 card is `.dev/reflect/pre-TASK-WF-workerContractFo-20261106-214402-20261106214804/reflection-card.yaml` (read it). It reports full coverage (15/15 inferred requirements matched) and three P3 findings: RF-1 (Task 1's search for WC-4 copies omits docs/, and the developer guide restates WC-4 `artifacts` at docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:1002), RF-2 (plugin test.md has no Unattended section and is left unchanged, unstated), RF-3 (Task 5 `./artifacts/` base directory unnamed). Do not just confirm these; look for what the card missed.

## Grounding hunks

- Codegraph run-state: index_state: unchecked (inputs are Markdown and test text); checked_at: 2026-11-06T21:48:04Z; worktree_root and projectPath: /home/coder/workspaces/worktrees/IronClaude/WorkerContractFollowups. Do not call codegraph; use Read and Grep.
- `src/superclaude/core/WORKER-CONTRACT.md:31-32`: WC-4 header and the worker-fields sub-bullet containing the pinned phrase "`artifacts` (every other file written), `blocked_question` when blocked, and `reason` when failed".
- `src/superclaude/core/WORKER-CONTRACT.md:39-41`: WC-9; line 41 stages with `git add -- <paths>` plus `.dev/tasks`.
- `tests/skills/test_worker_contract.py:19` CONTRACT_PATH; `:107` WC-4 phrase pin; `:324`, `:329`, `:339`, `:349-353` UNATTENDED_EXPECT rows for init-lite, workflow, build, test; `:769` `_artifacts_clause`; `:777` `test_unattended_artifacts_list_only_files_the_run_wrote` (asserts at `:799` and `:808`); `:1062` WRITE_VERB_RE.
- `src/superclaude/commands/workflow.md:72` and `src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md:52`: current per-command restatement of the ignored-path reason (plugin copies byte-identical at the same lines).
- `src/superclaude/commands/build.md:104`: build `artifacts` clause with `git check-ignore`, typical `build/`, `dist/`, `*.egg-info/`.
- `src/superclaude/commands/test.md:97-107`: test Unattended section; Contract bullet at `:103` has no `artifacts` rule.
- `src/superclaude/skills/sc-init-lite-protocol/SKILL.md:61` and `src/superclaude/commands/init-lite.md:92`: "succeeded when the audit finished".
- Parity tests: `tests/commands/test_workflow_command.py:94-102` (plugin skill folder and plugin workflow.md), `tests/skills/test_task_workspace_smoke.py:41`.

## Coverage matrix slice

All 15 rows in `.dev/reflect/pre-TASK-WF-workerContractFo-20261106-214402-20261106214804/artifacts/coverage-matrix.yaml`. Rows you own: INF-004, INF-006, INF-008, INF-009, INF-010, INF-013, INF-014.
