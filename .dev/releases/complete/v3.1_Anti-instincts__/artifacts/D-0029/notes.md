# D-0029: Structural Audit Threshold (0.5) Analysis

## Threshold Under Test

`extraction_total_requirements / total_structural_indicators >= 0.5` (defined in `spec_structural_audit.py:107`)

## Shadow Data Analysis

4 calibration scenarios tested against the structural audit threshold:

| Test Case | Indicators | Req Count | Ratio | Passed | Expected | Correct |
|---|---|---|---|---|---|---|
| rich-spec-good | 7 | 8 | 1.14 | PASS | PASS | YES |
| rich-spec-bad | 7 | 2 | 0.29 | FAIL | FAIL | YES |
| minimal-spec-ok | 0 | 0 | 1.00 | PASS | PASS | YES (passthrough) |
| medium-spec | 3 | 2 | 0.67 | PASS | PASS | YES |

## Indicator Breakdown (Rich Spec)

| Indicator | Count |
|---|---|
| code_blocks | 1 |
| must_shall | 2 |
| function_signatures | 1 |
| class_definitions | 1 |
| test_names | 1 |
| registry_patterns | 1 |
| pseudocode_blocks | 0 |
| **total** | **7** |

## Rates

- **Accuracy**: 4/4 (100%)
- **False positive rate**: 0/4 (0%)
- **False negative rate**: 0/4 (0%)

## Threshold Rationale

The 0.5 threshold is deliberately conservative because structural indicators overcount:
- Code examples that aren't requirements inflate the indicator count
- Alternative approaches mentioned in specs add indicators without adding requirements
- Non-requirement prose (explanatory code blocks) contributes to indicator total

A ratio below 0.5 strongly suggests the extraction dropped content — it means the extraction captured fewer than half the structural indicators in the spec.

## Recommendation

**KEEP threshold at 0.5**. Rationale:
- Perfect accuracy across all test cases (100%)
- Zero false positives and zero false negatives
- Conservative design accommodates the inherent overcount in structural indicators
- Warning-only enforcement (FR-MOD4.3) means even occasional false positives won't block the pipeline
