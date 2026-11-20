d3850ca238d5d8c52d155e17cfc813c3983d05f7
# T22 review 1

Earlier blocking findings: none (first review).

## Acceptance criteria

- T22.AC1 met. T22.AC1@src/superclaude/cli/issue_watch/cli.py:133-136 prints `launched: <n>` only when `launched_issue` is set and `attempted: <n>` only when `attempted_issue` is set, once each, after `cycle:` and `exit:` (cli.py:130-131), before the dry-run lines (cli.py:137-141). Tests: tests/issue_watch/test_cli.py:589 (`launched: 12` once, no `attempted:`), :597 (`attempted: 12` once, no `launched:`, exit 7), :606 (neither line, live and dry-run outputs unchanged), :571-572 (real confirmed launch prints `launched: 42`). The changed pins in test_cli_e2e.py (confirmed launch only) are the task's intended new line, not a regression.
- T22.AC2 met. T22.AC2@src/superclaude/cli/issue_watch/cycle.py:1216 sets `attempted_issue` only in the `unknown` branch (the only `launch_unknown` return, cycle.py:1217-1218); the launched branch (cycle.py:1212) and the spawn_error branch (cycle.py:1219-1221) leave it None; the field is declared at cycle.py:484 and passed at cycle.py:1320. Tests: tests/issue_watch/test_cycle.py:5408 (set to 9 for each unknown outcome, launched_issue None), :5421 (None on a confirmed launch), :5428 (None for spawn_error and for no launch).
- T22.AC3 met. T22.AC3@tests/issue_watch/test_no_text.py:553 and :564 still pass; the new lines are integers only (cli.py:134, cli.py:136). `uv run pytest tests/issue_watch -q`: 2971 passed.

## Findings

None.
