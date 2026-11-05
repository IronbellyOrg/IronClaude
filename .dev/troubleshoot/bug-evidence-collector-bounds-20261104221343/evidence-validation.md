# Evidence Validation Report

**Report under validation**: .dev/troubleshoot/bug-evidence-collector-bounds-20261104221343/REPORT.md.draft
**Validator**: evidence-validator (persisted by the parent on receipt; condensed)
**Total citations**: 16 (5 Evidence, 11 Proposed Fix symbol claims)
**Verified**: 16
**Dropped**: 0
**Passed through (command, no reexec)**: 0
**Suggested report status**: success

## Verified citations
| # | Location | Verdict |
|---|---|---|
| E1 | scripts/collect-conflict-evidence.sh:68-70 check_deadline | verified (compares SECONDS only when called) |
| E2 | probe-evidence.out:8 `elapsed=65s` | verified |
| E3 | probe-evidence.out:5 `EVIDENCE_FAIL out_not_empty` | verified |
| E4 | refs/conflict-mechanical.md:253 row 5 restart under the same cycle_id | verified (line now also carries the fix) |
| E5 | probe-evidence.out:11 post-fix `elapsed=61s` | verified |
| F1-F4 | collect-conflict-evidence.sh:79-80 budget guard; :88 background job with fds 3/4 closed; :90, :100 kill -0 / sleep 0.2; :91-98 TERM, 1 s, KILL, wait, fail timeout | verified |
| F5 | conflicts.py:1219-1239 conflict_attempt; exported __init__.py:42, :131 | verified |
| F6-F7 | conflict-mechanical.md:71 cycle_dir; conflict-intent.md:16, :95, :99 | verified |
| F8-F13 | test_conflict_scripts.py:1526, :1540, :1551; test_conflict_e2e.py:1039; test_conflicts_core.py:2517, :2541; test_conflict_sync_protocol.py:143 | verified |

## Dropped citations
None.

## Notes
- E1 cites the deadline check; the pre-fix foreground branch is evidenced by the unfixed probe (E2).
- The post-fix probe discarded stdout; only exit and elapsed are evidence.
- Front matter `status: success` with `escalation_reason: low_confidence` reflects the Tier 1 -> Tier 2 escalation, not a failure.
- Line numbers are as of validation (before fix cycle 1 of the off-path review, which did not touch these lines' content).
