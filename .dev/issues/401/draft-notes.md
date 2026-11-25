# Draft notes

Leave a list empty (write "None") when there is nothing to report. The orchestrator asks the user one question only when either list has an item.

## New material

<!-- Facts added to the issue body that the description did not contain, one per line, each with its source (path:line or command). -->

- Production dispatch invokes step functions directly, and repository Python search found calls to the helper only in tests; registered budgets are copied into steps but not enforced through the helper (`src/superclaude/cli/cli_portify/executor.py:107`, `:577`, `:819`; `tests/cli_portify/test_executor.py:518`).
- Current blocker is two seconds, and one timeout test also checks the error message (`tests/cli_portify/test_executor.py:504`, `:558`). Earlier CI measurements supplied by the orchestrator were 10.00 seconds per timeout test with a 10-second blocker; Python 3.10 and the exact reproduction call were also supplied by the orchestrator.
- Medium severity and proposed elapsed-time and production-dispatch coverage are judgments based on the helper and dispatch paths (`src/superclaude/cli/cli_portify/executor.py:191`, `:577`).
- Codegraph and Auggie tools were unavailable; the quick pass used Grep and Read.

## Contradictions

<!-- Each place where the description disagrees with the code, one per line, with path:line evidence. -->

- The description implies SC-001 and SC-002 are enforced through the flawed helper; production dispatch instead calls step functions directly and does not use it (`src/superclaude/cli/cli_portify/executor.py:577`–`:587`). The limits are not enforced through the helper.
- The description says timeout tests only check exception type; one also checks the timeout message (`tests/cli_portify/test_executor.py:558`–`:566`). None of these timeout tests checks elapsed time.
