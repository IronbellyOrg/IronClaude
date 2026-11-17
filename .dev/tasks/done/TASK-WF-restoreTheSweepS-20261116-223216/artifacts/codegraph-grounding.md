# Codegraph grounding

## Run state

- index_state: fresh (codegraph_status: 0 added, 0 modified, 0 removed; 3370 files)
- checked_at: 2026-11-16T22:32:30Z
- worktree_root / projectPath: /home/coder/workspaces/worktrees/IronClaude/sweep-working-fix
- access: mcp
- tokens: none

## Resolved symbols

- parse_worker_show: src/superclaude/cli/sweep/probes.py (def near line 453)
- _rule_working: src/superclaude/cli/sweep/classify.py (def near line 251), registered in RULES (line 338)
- OrcaObservation fields agent_wait, agent_wait_present, agent_wait_since: src/superclaude/cli/sweep/models.py lines 98-110
- C_WORKING, _classification: src/superclaude/cli/sweep/classify.py

## Dependents

- parse_worker_show callers (codegraph_callers, 9): _run_rows (probes.py:1191) and eight tests in tests/sweep/test_probes_allowlist.py (def-line rows, not call-site verified)
- _rule_working: referenced only through RULES (classify.py)
- agent_wait / agent_wait_present readers (Grep): classify.py rule 4, report.py `_age`, tests in test_classify.py, test_report.py, test_probes_allowlist.py

## Pre-check

All files and symbols named by Tasks 1 to 5 exist; test helpers `_captured`, `_canned`, `_ps` exist in tests/sweep/test_cli_contract.py. Fixtures captured-worker-show-1..5 have no agentWait key (Grep count 0). Dependents no task names: none found.
