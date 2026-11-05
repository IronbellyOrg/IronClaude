# Calibration Report (Tier 1 card, blind, confidence-calibrator on opus)

Persisted by the orchestrator from the agent's returned report (the agent has no Write tool).

**Card under calibration**: `.dev/reflect/pre-TASK-WF-writeTheP1Static-20261105-033458-20261105034258/t1-card.md`
**Rubric**: `~/.claude/skills/sc-reflect-protocol/refs/reflection-rubric.md` (five dimensions, C = arithmetic mean)
**Card tier**: 1 | **Timestamp**: 2026-11-05T03:50:00Z

## Per-dimension scores

| Dimension | Score | Justification |
|---|---|---|
| Citation grounding | 0.88 | All 19 citations match their sources. Gaps: F-001 cites no `git status` evidence for "unrelated paths"; F-002 cites `spec:221` for a phrase that lives in the section 3.1 brainstorm row; the coverage-matrix path is relative to the reflect folder, not the plan package. |
| Coverage completeness | 0.65 | `coverage_pct_union 0.50`, parsed 0, parsed-sparse; raised into the 0.60-0.84 band because F-005 lists the 7 unmapped rows by ID, but backs them with two plan lines rather than one mapping per row. |
| Deviation-classification clarity | 0.35 | The card labels findings by severity and grounding tag, not by Aligned / Refinement / Drift / Regression. F-002 hedges between disclosed and scope creep. |
| Risk surface coverage | 0.65 | Real risks listed; no blast-radius reasoning. Not surfaced: which of the 16 pinned test files could break, unverified business-panel frontmatter loading, drift between plugin mirrors. |
| Recommendation actionability | 0.75 | Recommendation 1 names the target, the replacement command and the timing. Recommendation 2 names a recipient but no artifact or success test. |

## Stage-2 trace

| Step | Value |
|---|---|
| arithmetic_mean(all_five) | 0.656 |
| verdict_cap | none (`claim_class: static_defect`, no Runtime check dimension) |
| **calibrated** | **0.66** |
| structural_flags | skipped (no assertions_path) |

## Confidence

- Self-reported 0.80 (not used). Calibrated 0.66. Delta -0.14.

## Escalation recommendation

- Verdict `ESCALATE`, reason `low_confidence` (0.66 < 0.85). No execution restriction.

## Notes

- Spot-check: 19 of 19 citations match. F-002's phrase "automatic research enrichment ... is off" is not at `spec:221`; the nearest text is the P2 row (line 222) and the section 3.1 brainstorm row.
- INF-006 wording drift in the matrix ("the small fixes to the ready commands" vs `source.md:5` "the small fixes to ready commands").
- Six of the seven unmapped rows have plausible Constraint-level coverage in `plan:19-24`; INF-003 (flag parse rule) is covered only partly by `plan:24`'s switch sentence.
- `assertion_skipped: C1-C8 (assertions_path)`. No file was modified by the agent.
