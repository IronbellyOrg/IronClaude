# Merge Log

Base: variant-3-original.md. Plan: refactor-plan.md (auto-approved). Output: ../merged-verdict.md. Merge date: 2026-11-13.

## Changes applied

| # | Change | Source | Status | Notes |
|---|---|---|---|---|
| 1 | M1 sync-dev gap, medium | V1 F1, V2 F1, V3 confirm | Applied | Evidence plan:19, 82; Makefile:171-178; t5-checks.log:28-35 (re-Read) |
| 2 | M2 baseline-pid gap, medium, Tasks 1-3 argument | V3 round 2 | Applied | plan:70, 20, 29 |
| 3 | M3 setsid reasoning, medium, INFERRED, HEAD guard proxy:1012-1019 | V3 F1 | Applied | Guard re-Read at proxy:1015-1019, comment at 1011-1014 |
| 4 | M4 HC5 off-path review, minor | V2 F2 | Applied | remediation-source.md:35 re-Read |
| 5 | M5 `contains` vs `ends with`, minor | V2 F3 | Applied | plan:32; remediation-source.md:14 |
| 6 | M6 sleep check, M7 teardown/pgrep, M8 dependency chain / pkill vs pid / scope wording, minor | V1 F4/F5, V3 F2-F4 | Applied | M7 fixture lines re-Read: test_ccsession_tiers.py:843-882 |
| 7 | M9 rollout caveat, M10 subreaper (INFERRED), M11 session check on direct start only, non-blocking | INV-001/002/003 | Applied | Recorded as minor with a non-blocking note; M10 citation launch-job-identity.sh:310-312, 483-484 re-Read at src/superclaude/hooks/scripts/ |
| 8 | Correct C-009 citation to test_ccsession_tiers.py:843-882, :855, :863 | V3 concession | Applied | Used in M7 |
| - | Informational section and Rejected/withdrawn section | refactor-plan "Changes NOT being made" | Applied | Stale anchors, vacuous coverage figure; V2 FAIL/Blocking, temp-HOME, anchors as defect |

## Skipped

None. The three items under "Changes NOT being made" are recorded in the Rejected section, not as findings.

## Failed

None.

## Deviations to note

- M9 and M10 were given as "non-blocking" without a severity word; the table vocabulary is blocking|medium|minor, so they carry `minor` and say "Non-blocking" in the claim. Probe rated INV-001/002 MEDIUM, but the brief fixed these as non-blocking items.
- M3 evidence is HEAD code (proxy:1012-1019); the plan-time file may differ. Tagged [INFERRED] per instruction.
- INV-003's test:2019 `getsid` assertion was not re-Read, so it is not cited; plan:32 and plan:40 are used instead.

## Post-merge validation

- Heading hierarchy: OK (three `##` sections in order Verdict, Merged findings, Informational, Rejected; no level skips).
- Internal references: resolved (M1-M11 each appear once; Informational and Rejected sections refer to M4 and to plan lines that exist; cited files exist and were Read).
- Contradictions re-scan: none. Verdict PASS is consistent with 0 blocking rows; V2's FAIL appears only under Rejected; counts (3 medium, 8 minor/non-blocking) match the table.
- Provenance: header comment plus per-section source tags present.
