# Evidence Validation Report (reflect Wave 5)

**Report under validation**: REPORT.md.draft (mtime 2026-11-02T04:21:09Z)
**Source**: evidence-validator agent, persisted by the parent on receipt
**Total citations**: 72 (71 file:line + 1 command)  **Verified**: 70  **Dropped**: 1  **Passed through**: 1
**Suggested report status**: partial

## Verified
- Deviation register and prose: 26 of 27 file:line citations verified (ccsession:832, 769-770, 782-784, 793-795, 804; tests/unit/test_ccsession_tiers.py:1354-1361, 1404, 595, 1416-1418, 1405; tasklist:70, 21, 82, 69, 29; models.py:772-784; local-gateway-alias-proxy.py:857-872, 490-491, 126-127, 129-133, 862; remediation-source.md:22, 14, 35; orca_close_repro.py:116; orca_close_repro.py file-level).
- Inferred requirements: 44 of 44 quotes found at their cited lines; matcher counts confirmed (31 containment, 13 none, 0.7045).

## Dropped
| location | reason | action taken |
|---|---|---|
| ccsession:785-788 (F14) | the `*)` "owned by another service" branch says nothing about a hand-started shim or setsid | removed from the F14 citation cell; F14 stays supported by local-gateway-alias-proxy.py:490-491, 126-127, 129-133 and ccsession:804 |

## Passed through
`ls -l /proc/2258510/fd` (captured runtime output; recorded in adversarial/merged-output.md:38 and adversarial/invariant-probe.md).

## Structural assertions
sc-reflect-protocol has no refs/agent-assertions.md; the validator used the troubleshoot rule set as a stand-in: A3 evaluated (no fire), A1, A2, A4-A10 skipped (troubleshoot-only or inputs absent).

## Notes
- F5: teardown is at tests/unit/test_ccsession_tiers.py:611-613 (not cited; the cited 595 is correct for its construct).
- F9 verified at file level only.
