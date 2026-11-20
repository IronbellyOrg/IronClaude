# Merge Log (Step 5)

## Metadata
- Base: Variant 1 (reviewer-1-card.yaml, analyzer persona, calibrated C=0.75)
- Executor: merge-executor role (this agent, skill-direct Mode A)
- Changes applied: 19 rows written (18 findings + 1 dropped record)
- Status: success
- Timestamp: 2026-11-08T18:36Z
- Output: merged-verdict.yaml

## Changes Applied

| # | Change | Status | Provenance |
|---|--------|--------|------------|
| 1 | 14 R1 rows carried from base with final severities | Applied | Source: Base (original) |
| 2 | QA-1 incorporated, framing narrowed per R2 calibration | Applied | Source: Variant 2, QA-1 |
| 3 | QA-2 incorporated, severity blocking->minor | Applied | Source: Variant 2, QA-2 (modified) — debate X-002 |
| 4 | QA-3 incorporated, citation narrowed to plan:252,257,264 | Applied | Source: Variant 2, QA-3 |
| 5 | QA-4 incorporated unchanged | Applied | Source: Variant 2, QA-4 |
| 6 | R1-F12 severity minor->blocking | Applied | Source: Base (original, modified) — X-003 |
| 7 | R1-F14 dropped (needs-reading list excludes item 5) | Applied | Source: Base (original, modified) — X-004 |
| 8 | Citation corrections written into corrected_citation on R1-F02,F03,F04,F06,F08,F09,F10 | Applied | Source: Base (original, modified) |
| 9 | Citation narrowing on QA-2 (plan:156) and QA-3 (plan:252,257,264) | Applied | Source: Variant 2 (modified) |
| 10 | INV-010 carry-in added to verdict_notes | Applied | Source: invariant-probe.md |

## Post-Merge Validation
- Structural integrity: PASS — merged-verdict.yaml carries merge_method: adversarial, cards: (2 paths), per-finding rows with id / source reviewer / final severity / final category / corrected citation / one-line merge rationale, and a final verdict line.
- Internal references: PASS — every corrected citation was re-verified this merge by Read of the plan (266 lines), runbook ranges, source.md and orca_worktree.py ranges; the vacuous-grep fact re-established by grep (0 matches).
- Contradiction re-scan: PASS — no new contradictions introduced; the two input contradictions (X-001, X-002) are resolved and documented in the merge rationales; both cards' FAIL verdicts align with the merged FAIL.

## Summary
- Planned changes: 10 (per refactor-plan.md)
- Applied: 10
- Failed: 0
- Skipped: 0
