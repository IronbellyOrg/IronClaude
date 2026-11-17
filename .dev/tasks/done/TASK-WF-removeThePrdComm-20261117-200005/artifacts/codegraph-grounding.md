# Codegraph grounding: TASK-WF-removeThePrdComm-20261117-200005

## Run state

- index_state: fresh by CLI `codegraph status` (3,822 files, 58,424 nodes, no pending-change list); not usable for lookups
- checked_at: 2026-11-17T20:00:01Z
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/v6-prd-cli
- projectPath: the same path
- access: none (the codegraph MCP server disconnected earlier in the session, so no lookup tool is listed; the CLI read verbs are not in this primitive's allowlist)
- tokens: graph:absent
- Floor used for every lookup below: Grep, `git grep` and Read.

## Resolved symbols

| Symbol or file the source names | Found at |
|---|---|
| `superclaude prd` group (`prd_group`) | `src/superclaude/cli/prd/commands.py`; registered at `src/superclaude/cli/main.py:539-541` |
| removed package | `src/superclaude/cli/prd/` (15 files); tests `tests/cli/prd/` (17 files, 229 passing tests at baseline) |
| interactive prd skill (stays) | `src/superclaude/skills/prd/` |

## Dependents

Dependents of the removed package, from `git grep` for `superclaude.cli.prd`, `from .prd`, `prd_group`, quoted `"prd"` and CLI-roster lists. The full table with line numbers is `.dev/cleanup/prd-cli/dependency-map.md` (section B).

- `src/superclaude/cli/main.py:539-541`: the only import of the package.
- `tests/cli/test_cli_registration.py:41`: expects `prd` in the top-level roster and runs `prd --help`.
- `tests/troubleshoot/backtest/test_replay_executor.py:81`: the only live import in tests (`from superclaude.cli.prd import gates`). The `from superclaude.cli.prd import ...` lines in `test_backtest_e1.py`, `_e2.py` and `_e4.py` are inside snippet strings run against an old commit and are not live imports.
- `tests/skills/test_review_severity_rule.py`: reads the files of rows C-152, S-107 and S-108 from the two fixtures, and compares the fixtures byte for byte with `.dev/review-severity-rule/cap-edits.yaml` and `sweep-edits.yaml`.
- Text-only references: hook script, `eval/orchestrator.py` docstring, `reuse-auditor.md`, `tests/cli/reflect/test_cli_smoke.py` docstring, four docs, `PROJECT_INDEX.json` and `.md`.

## Pre-check

Floor (Grep, Read, `test -e`), 2026-11-17: all 19 files the tasks name exist; the lines the tasks quote (main.py 539-541, test_cli_registration.py 41, severity test 281 and 288, guide 135/147, review-severity doc 69, technical-architecture 315, PROJECT_INDEX.json 46/94/110, PROJECT_INDEX.md 36) match. `gate_passed` resolves in `src/superclaude/cli/pipeline/gates.py`. Dependents of the removed package that no task names: none found by `git grep` (the only other hits are tracked `.dev/` records and the backtest snippet strings, both deliberately left). Result: 14 tasks checked, 0 unresolved.
