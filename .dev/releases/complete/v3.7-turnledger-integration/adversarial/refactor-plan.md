# Refactoring Plan: Merged Validation Report

## Overview
- **Base variant**: Variant B (Sonnet Validation Report)
- **Incorporated variants**: Variant A (GPT Validation Report)
- **Planned changes**: 4
- **Rejected changes**: 2
- **Overall risk**: Low (all changes are additive or reclassification)

---

## Planned Changes

### Change #1: Reclassify FR-7.1 from MEDIUM to HIGH
- **Source variant**: Variant A, GAP-H005
- **Target location**: Variant B, GAP-M004 (currently MEDIUM)
- **Integration approach**: Reclassify — move from MEDIUM section to HIGH section, update severity, update finding count in frontmatter
- **Rationale**: Debate point X-002, won by Variant A (68% confidence). The roadmap explicitly states "9-field schema" while the spec requires 10 fields. This is a textual contradiction regardless of whether duration_ms is auto-computed. The auto-computation detail affects *implementation* but not the fact that the roadmap's field list is wrong.
- **Risk level**: Low — severity reclassification only, no content change

### Change #2: Add standalone boundary/count finding
- **Source variant**: Variant A, GAP-H007
- **Target location**: Variant B, after GAP-H009 (add as new GAP-H010)
- **Integration approach**: Insert — add new HIGH finding based on Variant A's analysis
- **Rationale**: Debate point C-008, won by Variant A (62% confidence). The roadmap's claim of "13 requirements" at `roadmap.md:271` vs the actual 62+ atomic requirement surface is an independently valuable observation about planning metadata accuracy. Variant B addresses the consequence (via cascade) but not the root cause (misleading count).
- **Risk level**: Low — additive change, no modification of existing content

### Change #3: Add adversarial pass status header
- **Source variant**: Variant A, line 26
- **Target location**: Variant B, between frontmatter and H1 heading
- **Integration approach**: Insert — add single line confirming adversarial re-read
- **Rationale**: Unique contribution U-003 from Variant A. Low value but zero cost, provides process accountability.
- **Risk level**: Low — single line addition

### Change #4: Update frontmatter metrics for reclassification
- **Source variant**: Derived from Change #1 and #2
- **Target location**: Variant B, frontmatter YAML
- **Integration approach**: Modify — update valid_high from 9 to 11, valid_medium from 5 to 4, total_findings from 21 to 22 (adding boundary/count finding)
- **Rationale**: Frontmatter must reflect actual finding counts after reclassification and addition.
- **Risk level**: Low — arithmetic update

---

## Changes NOT Being Made

### Rejected #1: Adopt Variant A's 62-requirement universe
- **Diff point**: X-001
- **Variant A approach**: 62 requirements, excludes cascading success criteria
- **Rationale**: Unresolved in debate (50% confidence). Variant B's 71-requirement count includes SC criteria as separate tracked items, which is methodologically valid for a validation report. The specific count matters less than the gap identification, which is consistent across both variants. Adopting the lower count would reduce coverage granularity without improving accuracy.

### Rejected #2: Remove cascade findings (H008, H009) in favor of standalone approach
- **Diff point**: C-007
- **Variant A approach**: Treat FR-6.1/6.2 as standalone MEDIUM findings
- **Rationale**: Debate point C-007, won by Variant B (85% confidence). The cascade analysis is a strength — it shows that weak gap closure language has second-order effects on SC-1 and SC-8. Removing cascading findings would lose analytical depth.

---

## Risk Summary

| Change | Risk | Impact | Rollback |
|--------|------|--------|----------|
| #1 Reclassify FR-7.1 | Low | Severity label change only | Revert to MEDIUM |
| #2 Add boundary/count | Low | New finding, no existing content modified | Remove finding |
| #3 Add adversarial status | Low | Single line, no semantic impact | Remove line |
| #4 Update frontmatter | Low | Arithmetic, no semantic impact | Revert counts |

---

## Review Status
- **Approval**: Auto-approved (non-interactive mode)
- **Timestamp**: 2026-03-23T00:00:00Z
