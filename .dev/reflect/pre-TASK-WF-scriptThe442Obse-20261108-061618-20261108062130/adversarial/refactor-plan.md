# Refactor Plan (Step 4) — base: Variant 1 (reviewer-1-card.yaml)

## Overview
- Base: Variant 1 (14 finding rows, differentiated severity)
- Incorporated from Variant 2: 4 finding rows (QA-1, QA-2, QA-3, QA-4) with QA-2 severity adjusted blocking -> minor
- Changes: 19 merged rows (18 finding rows + 1 dropped-row record), 2 severity changes, 7 citation corrections, 1 probe carry-in (INV-010)
- Overall risk: Low (additive row merge into a YAML verdict; no content rewritten)

## Planned Changes
1. Incorporate QA-1 as merged row 15 (complements R1-F01 in the same plan:70-75 wait block; keep both).
2. Incorporate QA-2 as merged row 16, severity minor (plan:156 + plan:240 ordering evidence; R1 self-audit point 7 corroborates the stop-rule match).
3. Incorporate QA-3 as merged row 17, blocking (verified conflict: plan:252/257/264 vs runbook:726).
4. Incorporate QA-4 as merged row 18, blocking (plan:187-191 verified: no FAIL-classification assertion).
5. Raise R1-F12 severity minor -> blocking (calibration + Round 2 concession).
6. Drop R1-F14 (plan:183 list excludes item 5; cited plan lines unrelated).
7. Correct citations on R1-F02, F03, F04, F06, F08, F09, F10 per the calibration map and fresh reads (corrected_plan_citation fields).
8. Add citation corrections to QA-2 (narrow 134-161 -> plan:156) and QA-3 (narrow 240-264 -> plan:252,257,264).
9. Carry INV-010 into verdict_notes as a pre-execution review item (destructive cleanup paths at plan:205-206, runbook:823, neither card's finding).

## Changes NOT Being Made
- C-002 (verdict derivation): both cards independently FAIL; no change needed.
- S-002 (self-audit style): both self-audits preserved verbatim in the merged verdict appendix references; style not normalized.
- V2's severity normalization to all-blocking: rejected — Round 1 unanimous + both calibrations favor the differentiated scale.
- R1-F13 severity raise: rejected — kept minor per Round 2 agreement (runbook:172-182 lists the writes; ambiguity is documentary, recommendation to state authorization stands).

## Risk Summary
All changes additive to a new YAML artifact; source cards untouched (copies at variant-1-original.yaml / variant-2-original.yaml). Rollback: delete merged-verdict.yaml.

## Review Status
Auto-approved (non-interactive), 2026-11-08T18:36Z.
