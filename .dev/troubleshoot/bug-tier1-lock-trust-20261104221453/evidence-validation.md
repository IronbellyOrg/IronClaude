# Evidence Validation Report

**Report under validation**: .dev/troubleshoot/bug-tier1-lock-trust-20261104221453/REPORT.md.draft
**Validator**: evidence-validator (persisted by the parent on receipt; condensed)
**Total citations**: 16 (5 Evidence, 11 Proposed Fix claims)
**Verified**: 16
**Dropped**: 0
**Passed through (command, no reexec)**: 0
**Suggested report status**: success

## Verified citations
| # | Location | Verdict |
|---|---|---|
| 1 | tier1-observation.md:2 | verified (the HEAD hash is an inference from git log, not quoted in that line; red-run.out:6 corroborates) |
| 2 | probe-lock-trust.out:6 `in-tree backend executed: yes` | verified |
| 3 | conflicts.py:208-216 MECHANICAL_RULES | verified |
| 4 | pyproject.toml:16 `requires-python = ">=3.10"` | verified |
| 5 | red-run.out:1 | verified |
| 6-9 | conflicts.py:226-272 lock_trust_findings (pure); :29-32 guarded import; :223, :238-267 fail-closed paths; :254-271 order and shapes; exports __init__.py:51, :140 | verified |
| 10-11 | conflict-mechanical.md:82-95 (gate at :88), halt row :302 | verified |
| 12-14 | conflict-mechanical.md:131 trust limit; SKILL.md:321; commands/pr-submit.md:54 | verified |
| 15-16 | test_conflicts_core.py:2482-2509, 2561, 2567, 2585, 2604, 2627-2633, 2686, 2691, 2695, 2701; test_conflict_sync_protocol.py:119-135, :138-140 | verified |

## Dropped citations
None.

## Notes
- "CI (3.10) skips the trigger tests" verified (.github/workflows/test.yml:22, the _needs_tomllib marker).
- The out-of-scope residual list has no citations; it is a stated limitation, not evidence.
- The path/editable triggers rest on the owner's list, not on probe evidence (tier1-observation.md:14-15).
- Line numbers are as of validation; fix cycle 1 of the off-path review then rewrote the step 5 invocation sentence (see REPORT.md Proposed Fix).
