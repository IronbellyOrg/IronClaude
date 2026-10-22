# Task 6 independent compliance and post-review checks

Verdict: **compliant**. Independent reviewer inspected the actual added test fixture/functions, incremental patch, required execution artifact and relevant existing four-file coverage. No missing, extra-scope or misunderstood requirement was verified. The reviewer did not run commands/tests or edit files.

| AC | Status | Reviewer evidence |
|---|---|---|
| T6.AC1 | met | `tests/cli/test_install_codebase_memory.py:1412-1449`, `:1489-1506`, existing `:95-105`, `:191-317`; `tests/cli/test_update_command.py:251-277` |
| T6.AC2 | met | `tests/cli/test_install_codebase_memory.py:1277-1323`, `:1365-1379`, `:1414-1427`, `:1483-1488`; existing `tests/cli/test_install_mcp_tavily.py:517-627`, `:678-809` |
| T6.AC3 | met | `tests/cli/test_install_codebase_memory.py:840-1274`, `:1452-1477` |
| T6.AC4 | met | `tests/cli/test_install_codebase_memory.py:1354-1363`, `:1479-1488`, `:1509-1528`, existing `:544-726`; `tests/cli/test_install_mcp_tavily.py:920-995` |
| T6.AC5 | met | `tests/cli/test_install_codebase_memory.py:15-24`, `:1277-1408`, `:206-246`, `:1428-1432`; `tests/cli/test_update_command.py:96-146` |
| T6.AC6 | met | `artifacts/t6-cli-regressions.txt:33-39`, `:49-59` relative to this package; required exact four-file UV execution and result are recorded. |

Four genuine cross-entry cases result from two test functions parameterized across default/custom configuration locations. Actual CLI/lifecycle coordinators, discovery, registration reconciliation, native acquisition decisions and product receipt creation remain active. Mocks intercept external process effects, not shared lifecycle outcomes or ownership proof. New flows cover initial/repeat/repair, dry-run/list invariance, confirmed removal with retained sentinels/updater, update exclusion, explicit restoration and failed-removal preservation. Existing failure-matrix tests are reused rather than duplicated.

## Coordinator post-review extras

Existing environment, worktree imports, PYTHONDONTWRITEBYTECODE=1, disabled pytest cache provider:

- Required four-file suite: exit 0, **242 passed, 1 skipped in 11.32s**. Existing API-key-gated live Tavily skip remains; no real upstream/Claude/network lifecycle was executed.
- Ruff on the changed test file: exit 0, all checks passed.
- Scoped mypy on the changed test file: exit 0, no issues in one source file. A private temporary cache outside the checkout was cleaned through its exact-directory exit trap. This green test-file check does not erase the two previously documented legacy MCP-module diagnostics.

No product files or other test files changed in Task 6. The separately authorized released-binary/companion-file live smoke remains pending and is not proven by these mocked integration cases.
