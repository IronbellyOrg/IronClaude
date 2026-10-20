# Refactor Plan

## Overview
- **Base variant:** V1 (sonnet:analyzer).
- **Incorporated variant:** V2 (haiku:qa).
- **Planned changes:** 5. All are low risk.
- **Target:** adversarial/merged-review-card.yaml, which is a new file. The tasklist and spec are NOT edited.

## Planned Changes

1. **Re-bind the card to the current revision.** Set target_tasklist_sha256 to 954add6c…. Add reviewed_tasklist_sha256 with the value 9d4d00ed…, plus a drift note.
   - Source: diff-analysis integrity finding and A-001; both advocates REJECTED that assumption.
   - Approach: replace.
   - Risk: Low.
2. **Mark A1 as applied.** Keep A1, add `status: applied-in-current`, and cite the evidence T:50.
   - Source: C-001, decided at 90%.
   - Approach: modify.
   - Risk: Low.
3. **Import QA-1, QA-2 and QA-3 from V2** with `status: applied-in-current`, citing the current lines:
   - QA-1: T:60, T:80
   - QA-2: T:61, T:81
   - QA-3: T:59, T:77
   - Source: C-002, C-003 and C-004, all won by V2 and conceded by the V1 advocate.
   - Approach: append.
   - Risk: Low.
4. **Add V2's three coverage gaps to prior_findings_resolved** as resolved, with current-line evidence.
   - Source: X-002.
   - Approach: append.
   - Risk: Low.
5. **Add a test_contract_ceiling note.** Literal tests cannot prove runtime behavior at the quick and standard depths. The spec chose this approach in RF5, so the note is not a tasklist defect.
   - Source: A-002, which both advocates QUALIFIED.
   - Approach: append.
   - Risk: Low.

## Changes NOT Being Made

| Diff point | Non-base approach | Rationale |
|------------|-------------------|-----------|
| X-001 | V2 verdict approve-with-changes | Every change V2 requested is already present in 954add6c, and the V2 advocate conceded this. |
| C-002..C-004 | V2's recommended_change edits to the tasklist | They are already present at T:59-61 and T:77-81. Re-applying them would duplicate text. |
| S-001 | Adopting V2's card shape | This is a style point and is unresolved. Neither shape affects the verdict. |

## Risk Summary
All 5 changes are additive or metadata-only, and they touch only the merged card. Rollback means deleting merged-review-card.yaml.

## Review Status
Auto-approved (non-interactive), 2026-10-20.
