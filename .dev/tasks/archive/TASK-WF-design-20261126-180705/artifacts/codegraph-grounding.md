# Codegraph grounding (TASK-WF-design-20261126-180705)

## Run state

- index_state: fresh (readiness check made once for this run by the first generation, `codegraph_status`: 3773 files, no changes since index; checked 2026-11-26T16:32:04Z). This package is the regenerated plan of the same run; the run does not repeat the check.
- access: mcp; projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-326
- tokens: none. The files this plan changes are Markdown, JSON fixtures and new Python files, so lookups used Grep, Glob and Read (the permanent floor, normal evidence).

## Resolved symbols

Same symbols as the first generation (archived package `TASK-WF-design-20261126-162939`: `archive_workspace.py` line regexes `_HEADER`, `_PLAN`, `_START`, `_VERDICT`, `_RULING`, `_RETRY`, `_HALT`, `_FINAL`, `_ARCH` at lines 44-67, `_parse_ledger` at 181, `_remove_branch` at `scripts/worktree_cleanup.py:2636`, the implement `SKILL.md` anchors, the STOP table, `refs/managed-workspace.md` gate, `HOW-WE-WORK.md` `/sc:git` row, `WORKER-CONTRACT.md` K3 sentence), plus these found by the review of that plan (Read and Grep):

| Named by the review | Where it resolved |
|---|---|
| `_TRANSIENT` pin of four `E-RESUME-NEEDED` reasons | `tests/skills/test_task_workspace_lifecycle.py:611`, `:682-688` |
| halt-line scan and `_ALLOW` list | `tests/skills/test_implement_severity_static.py:296`, `:331-335`, `:420-434` |
| Q0 pin deletion at `complete` | `src/superclaude/skills/sc-implement-protocol/refs/retry.md` (sentence "delete the Q0 pin and the task's checkpoint refs", near line 437) |
| gate step 6 pinned by text | `tests/skills/test_implement_saved_prompt_rule.py:62-70`; `refs/managed-workspace.md` after the code block |
| `wc9-allowed` rows of the edited lines | `tests/skills/test_worker_contract.py` near `:2339-2345` and `:2410-2417` |
| routing test `self-contained` and skill-file checks | `tests/recommend/test_routing_refresh.py:101-107`, `:483-496`; fixture S23 `:325` |

## Dependents

New dependents found by the review, each now named in a task: the byte-parity tests that read the implement plugin twins (`tests/commands/test_workflow_command.py:204-220`, `tests/skills/test_implement_saved_prompt_rule.py:20,91-93`, `tests/skills/test_review_severity_rule.py:382-396`, `tests/skills/test_workflow_remediation.py:607-617`) are run by Tasks 26 to 34, so each of those tasks copies its twin; the halt-line allow-list test is run by Tasks 26, 30, 31, 32; `make lint-architecture` (Makefile) checks the command-to-skill link for `git` and runs in Task 20; CI runs `ruff check` and `ruff format --check` over `src/` and `tests/` (Task 38) and `--strict-markers` (Task 2 registers the `real_framework` marker in `tests/vcs/conftest.py`).

## Pre-check

Advisory, read-only batch of 21 checks run after the plan passed the gate: all 21 hold (the nine-pattern ledger grammar, the `_TRANSIENT` and `_ALLOW` anchors, the `retry.md` Q0 sentence, the saved-prompt gate pin, the `wc9-allowed` rows, the routing test and fixture anchors, the Makefile target, `--strict-markers`, the CI ruff line, `flags.md:141`, `README.md:9`, and the repairs M-02, M-08, M-09, M-11 and the marker present in the new plan). `git merge-base HEAD origin/integration` printed 862384852faebe3255c2876527103696cfd3cf3b, the commit Task 1 records as the base commit for "unchanged" checks. Dependents of the touched anchors that no task names: none found.
