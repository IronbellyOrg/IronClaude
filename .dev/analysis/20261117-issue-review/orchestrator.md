# Cluster: orchestrator (2026-11-17)

| Issue | Title | Verdict | Comment | Evidence |
|---|---|---|---|---|
| 339 | Orchestrator to run and manage all sessions | ACTIVE | https://github.com/IronbellyOrg/IronClaude/issues/339#issuecomment-6941329369 | Sweep merged (#539, #579); sc:close and actions not built |
| 409 | TUI dashboard / observer | ACTIVE | https://github.com/IronbellyOrg/IronClaude/issues/409#issuecomment-6941329702 | #577 turned questions panel on (commands.py:67), #586 live and load test; body banner stale |
| 423 | Orchestrator v2 proactive holistic | STALE-VALID | https://github.com/IronbellyOrg/IronClaude/issues/423#issuecomment-6941330131 | Not started; Q14 answered; rewrite awaits owner grant |
| 431 | Orchestrator alive check weak signals | STALE-VALID | https://github.com/IronbellyOrg/IronClaude/issues/431#issuecomment-6941330464 | Rules merged in #434 (11-08); live behavior untested |
| 444 | Sub-orchestrator evaluation | STALE-VALID | https://github.com/IronbellyOrg/IronClaude/issues/444#issuecomment-6941330720 | WC-13 unchanged (WORKER-CONTRACT.md:62); Phase 2 not started |
| 446 | WC-9 retry index.lock 10 s | STALE-VALID | https://github.com/IronbellyOrg/IronClaude/issues/446#issuecomment-6941331008 | WORKER-CONTRACT.md:45 still has no retry |
| 468 | orchestration check spam | STALE-VALID | https://github.com/IronbellyOrg/IronClaude/issues/468#issuecomment-6941331282 | No producer or fix found on master |
| 534 | Phase 1 follow-ups | NEEDS-OWNER-DECISION | https://github.com/IronbellyOrg/IronClaude/issues/534#issuecomment-6941331617 | #539 merged, #579 fixed working class; 50-read cap remains (probes.py:129) |

## Close candidates

None. Possible owner call: #431 could close as "rules merged in #434, monitor work under #423" (asked in its comment, not recommended as READY-TO-CLOSE because live behavior is untested).

## Owner questions

- #534: After a restart, should the sweep get one change that raises or pages the 50-read cap and adds wording for settled or asleep sessions, or stay as is with both recorded as stated limits?
