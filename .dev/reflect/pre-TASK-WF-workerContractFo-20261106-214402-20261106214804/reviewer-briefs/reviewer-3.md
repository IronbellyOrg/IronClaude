# Reviewer brief 3 (refactorer lens, opus slot; pre-execution plan audit, read-only)

Repository root: `/home/coder/workspaces/worktrees/IronClaude/WorkerContractFollowups` (all relative paths resolve against it).

You audit the plan `.dev/tasks/to-do/TASK-WF-workerContractFo-20261106-214402/TASK-WF-workerContractFo-20261106-214402.md` against its brief `.dev/tasks/to-do/TASK-WF-workerContractFo-20261106-214402/source.md` (mode pre, UC-1). You are read-only: no edits, no shell, no git. Audit the hunks below and anything you Read, Grep or Glob in the repository.

Persona focus: single source of truth and scope. Follow-up 1's whole point is that the ignored-path rule is written once (WC-4) and the command texts only point at it. Check: (a) does the plan leave any restatement of the reason behind (search src/, plugins/, docs/ and tests/ for "git refuses" and "stages every"); (b) does the plan add text beyond what the brief asks (scope creep), or miss a place the brief names; (c) does the planned WC-4 sentence fit the WC-4 sub-bullet structure and the installed-primitive rule (no `src/superclaude/` paths in installed files, CLAUDE.md "Never Hardcode src/superclaude/ Paths"); (d) are the Depends-on links (Tasks 2, 3, 4 on Task 1) and phase order sound.

Return findings as YAML: a list of items with id, priority (P1 blocks /sc:implement or makes a planned test pass on wrong text; P2 a defect a reviewer or test would catch; P3 cosmetic or an owner note), claim, evidence (file:line for every claim, or tag the claim [INFERRED]), exact_change and verifier; then self_reported_confidence (0-1) and a short list of what you checked and found clean. A zero-finding answer needs a self-audit naming what you checked.

## T1 card excerpt

The orchestrator's Tier 1 card is `.dev/reflect/pre-TASK-WF-workerContractFo-20261106-214402-20261106214804/reflection-card.yaml` (read it). It reports full coverage (15/15 inferred requirements matched) and three P3 findings: RF-1 (Task 1's search for WC-4 copies omits docs/, and the developer guide restates WC-4 `artifacts` at docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:1002), RF-2 (plugin test.md has no Unattended section and is left unchanged, unstated), RF-3 (Task 5 `./artifacts/` base directory unnamed). Do not just confirm these; look for what the card missed.

## Grounding hunks

- Codegraph run-state: index_state: unchecked (inputs are Markdown and test text); checked_at: 2026-11-06T21:48:04Z; worktree_root and projectPath: /home/coder/workspaces/worktrees/IronClaude/WorkerContractFollowups. Do not call codegraph; use Read and Grep.
- `src/superclaude/core/WORKER-CONTRACT.md:31-32`: WC-4 header and the worker-fields sub-bullet; `:39-41` WC-9 (line 41: `git add -- <paths>` plus `.dev/tasks`).
- `src/superclaude/commands/workflow.md:72`, `src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md:52` (plugin copies byte-identical), `src/superclaude/commands/build.md:104`: the three per-command restatements the brief names (source.md:11).
- `src/superclaude/commands/test.md:103`: test Contract bullet, no `artifacts` rule.
- `src/superclaude/skills/sc-init-lite-protocol/SKILL.md:61`, `src/superclaude/commands/init-lite.md:92`: init-lite status wording.
- `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:1002`: developer-guide summary of the WC-4 worker contract.
- `tests/skills/test_worker_contract.py:107` WC-4 phrase pin; `:777` artifacts test; `:1062` WRITE_VERB_RE.

## Coverage matrix slice

All 15 rows in `.dev/reflect/pre-TASK-WF-workerContractFo-20261106-214402-20261106214804/artifacts/coverage-matrix.yaml`. Rows you own: INF-001, INF-002, INF-006, INF-007, INF-008, INF-015.
