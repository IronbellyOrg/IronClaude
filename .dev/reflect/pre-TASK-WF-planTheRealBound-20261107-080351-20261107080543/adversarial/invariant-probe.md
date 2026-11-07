# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis (opus-class agent, independent of the three sonnet advocates)

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | state_variables | The throwaway HOME (config folder plus launch-level store) lasts across all runs that need it | UNADDRESSED | HIGH | plan:31, :35; live_probe.py:134, :142-143, :160; launch-job-identity.sh:220-225 (missing store reads `ordinary`) |
| INV-002 | interaction_effects | Cleanup copied from live_probe leaves the old child alive until resume and fork run | UNADDRESSED | HIGH | plan:31; live_probe.py:108-123, :279; launch-job-identity.sh:333-337, :343-344 |
| INV-003 | sufficiency_challenge | After the C-001 fix, a PASS means the actors are kept apart | UNADDRESSED | HIGH | plan:119, :48, :70; launch-job-identity.sh:427-428; tests/hooks/test_launch_job_identity.py:473-488; design:504, :506, :559 |
| INV-004 | guard_conditions | Either version of the C-001 fix gives a meaningful binary result | UNADDRESSED | MEDIUM | debate-transcript.md Scoring Matrix C-001 row ("state FAIL is expected or define a per-case evidence class") |
| INV-005 | state_variables | Session id stays the same across --resume, --fork-session and /clear | UNADDRESSED | MEDIUM | launch-job-identity.sh:429-437; design:551, :501; plan:55, :58 |
| INV-006 | collection_boundaries | Resume and fork can test the design's "reused Claude process" case | UNADDRESSED | MEDIUM | design:504; plan:55, :59 |
| INV-007 | interaction_effects | Concurrent human and governed pushes both reach the bare repository | UNADDRESSED | MEDIUM | plan:90, :94; tests/hooks/test_launch_job_identity.py:1306-1331, :1347-1348 |
| INV-008 | interaction_effects | The hook record can supply the selector line for background shapes | UNADDRESSED | MEDIUM | plan:55, :66 (inferred: Claude Code behavior, not in the repo) |
| INV-009 | guard_conditions | A timeout that kills the process group also cleans up governed jobs | ADDRESSED (C-015, rated low; should be medium) | MEDIUM | launch-job-identity.sh:292; live_probe.py:271, :275; tests/hooks/test_launch_job_identity.py:1472-1474 |
| INV-010 | count_divergence | Twelve runs is enough | ADDRESSED (C-006) | LOW | plan:22 |
| INV-011 | guard_conditions | Later tasks stop when preflight reports a refused nested launch or missing authentication | UNADDRESSED | LOW | plan:31, :22; live_probe.py:280-286 |
| INV-012 | count_divergence | 27 of 27 is the right total | ADDRESSED | LOW | diff-analysis.md metadata |
| INV-013 | sufficiency_challenge | 100% agreement means the review is correct | ADDRESSED (recorded as a limit) | LOW | debate-transcript.md Convergence Assessment |

## Summary

- **Total findings**: 13
- **ADDRESSED**: 4 (INV-009, INV-010, INV-012, INV-013)
- **UNADDRESSED**: 9
  - HIGH: 3 (INV-001, INV-002, INV-003)
  - MEDIUM: 5 (INV-004, INV-005, INV-006, INV-007, INV-008)
  - LOW: 1 (INV-011)

Notes: INV-005, INV-006 and INV-008 are inferred from Claude Code behavior that this review did not observe. INV-001 to INV-003 were not debated by the advocates (they arose after Round 2) and are carried into the merged verdict as undebated, probe-sourced findings.
