# Cluster sprint-cli-core, review 2026-11-17

| Issue | Title | Verdict | Comment | Evidence |
|---|---|---|---|---|
| 29 | cleanup_audit/executor.py calls undefined process.is_running()/stop() | NEEDS-OWNER-DECISION | https://github.com/IronbellyOrg/IronClaude/issues/29#issuecomment-6941362682 | executor.py:89-107 still calls the undefined methods; #571 PR 2 removes the runner |
| 143 | sprint executor: 3 e2e harness nits | NEEDS-OWNER-DECISION | https://github.com/IronbellyOrg/IronClaude/issues/143#issuecomment-6941363180 | config.py:156, monitor.py:30, executor checkpoint gate all unchanged; #571 PR 11 removes sprint |
| 401 | cli_portify run_with_timeout | NEEDS-OWNER-DECISION | https://github.com/IronbellyOrg/IronClaude/issues/401#issuecomment-6941363614 | executor.py:191-216 and 577-587 unchanged; #571 PR 4 removes cli-portify |
| 465 | Verifier report delivery failure | STALE-VALID | https://github.com/IronbellyOrg/IronClaude/issues/465#issuecomment-6941364036 | rf-qa-qualitative.md:826-828 unchanged by #582; #572 may rework agent |
| 470 | Research pipeline blocks before research | STALE-VALID | https://github.com/IronbellyOrg/IronClaude/issues/470#issuecomment-6941364698 | rf-qa.md:316 vs template created_date still mismatched; #463 closed; #571 Part B pending |
| 476 | sprint status/logs placeholders | BLOCKED | https://github.com/IronbellyOrg/IronClaude/issues/476#issuecomment-6941365297 | logging_.py:367-378 still stubs; Clay backlog 11-16 |
| 496 | sprint run CI=0 treated as yes | BLOCKED | https://github.com/IronbellyOrg/IronClaude/issues/496#issuecomment-6941365902 | commands.py:325-326 unchanged; Clay backlog |
| 554 | cli-portify ignores max review iterations | BLOCKED | https://github.com/IronbellyOrg/IronClaude/issues/554#issuecomment-6941366443 | panel_review.py ConvergenceEngine(max_iterations=1) unchanged; Clay backlog |
| 535 | sprint tmux child drops resume, parallelism, handoff | BLOCKED | https://github.com/IronbellyOrg/IronClaude/issues/535#issuecomment-6941366996 | tmux.py:176-217 still omits the three flags; Clay backlog |

## Close candidates
None marked READY-TO-CLOSE. Strong candidates for close as not planned, if the owner confirms #571 PRs 2, 4 and 11 (remove cli/cleanup_audit, cli/cli_portify, cli/sprint): 29, 143, 401, 476, 496, 535, 554. Precedent: the owner closed #495, #558 and #559 (same Clay backlog comment) as not planned on 2026-11-17.

## Owner questions
- #29: Close as not planned because the cleanup-audit runner is being removed (#571 PR 2), or keep until it merges?
- #143: Close as not planned because sprint is being removed (#571 PR 11), or fix the three nits first?
- #401: Close as not planned, matching #495, #558 and #559?
