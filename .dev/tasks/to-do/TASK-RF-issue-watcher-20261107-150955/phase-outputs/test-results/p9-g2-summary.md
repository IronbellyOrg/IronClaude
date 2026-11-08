# Final-tree gate G-2 summary (re-run after the Final-gate fix cycle)
Command: `uv run pytest tests/issue_watch/ tests/skills/test_model_alias_policy.py tests/docs/test_retired_docs_absent.py tests/cli/test_cli_registration.py tests/swarm/test_cli_registration.py tests/recommend/test_cli_registration.py -v -rs` (raw: p9-g2-raw.txt). Result: PASSED. EXIT=0, 2665 passed, 1 skipped, 0 failed, 0 errors.

| Failure | Detail |
|---|---|
| none | |

The one skip is the pre-existing `tests/swarm/test_cli_registration.py:127` ("got empty parameter set for (subcommand)"), outside this change set, recorded and not fixed. No skip in tests/issue_watch/. Summary line: `2665 passed, 1 skipped in 18.12s`
Full suite: CI only (decision DF-05). One reviewer ran it anyway (19575 passed, 4 failed outside issue_watch); see the Phase 9 log for the comparison with a clean master.
