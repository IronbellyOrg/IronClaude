# Diff Analysis: Eval Spec Change Proposals

## Metadata
- Generated: 2026-03-19
- Variants compared: 3
- Total proposals found: 13 (12 after dedup)
- Categories: content (12), contradictions (0), duplicates (1), unique per-variant (V1: 5, V2: 5, V3: 3)

## Proposal Inventory

| ID | Source | Proposal | Spec Sections Affected | Overlap |
|----|--------|----------|----------------------|---------|
| A | V1 | Code-level evidence tier | Section 2, Section 5.2, FR-EVAL.14 | — |
| B | V1 | Correct failure classification | Section 5.2, FR-EVAL.13, FR-EVAL.14 | Partial w/ K |
| C | V1 | CONDITIONAL_PASS verdict | FR-EVAL.5, FR-EVAL.7, Section 4.5 | **Duplicate of L** |
| D | V1 | Regression-guard scoring mode | FR-EVAL.14, FR-EVAL.5 | — |
| E | V1 | Duration variance thresholds | FR-EVAL.5, NFR table | — |
| F | V2 | Partial run scoring | FR-EVAL.1, FR-EVAL.4, FR-EVAL.13 | — |
| G | V2 | Gate rejection vs functional failure | Section 2, Section 5.2, FR-EVAL.13 | Partial w/ K |
| H | V2 | Per-step variance tracking | FR-EVAL.1, FR-EVAL.5, NFR-EVAL.3 | — |
| I | V2 | Minimum completeness thresholds | FR-EVAL.4, FR-EVAL.5, NFR-EVAL.12 | — |
| J | V2 | Worktree reuse policy | FR-EVAL.6, FR-EVAL.4 | — |
| K | V3 | --eval-mode / --continue-on-fail | FR-EVAL.4, FR-EVAL.13, Section 5.2 | Partial w/ B, G |
| L | V3 | Ternary verdict model | FR-EVAL.5, FR-EVAL.7, FR-EVAL.13, Section 4.5 | **Duplicate of C** |
| M | V3 | Auto-detect LLM fabrication | FR-EVAL.9, Section 7, Appendix C | — |

## Duplicate Resolution

**C + L → C+L (merged)**: Both propose replacing `EvalReport.overall_passed: bool` with `verdict: str` {PASS, CONDITIONAL_PASS, FAIL} + `blocked_layers: list[str]`. V1-C focuses on data model; V3-L adds the `conditions: list[str]` field for upgrade requirements. Merged version incorporates both.

## Unique Contributions Per Variant

- **V1 unique**: A (evidence tier), D (regression-guard mode), E (duration variance)
- **V2 unique**: F (partial run scoring), G (gate rejection), H (per-step variance), I (min completeness), J (worktree reuse)
- **V3 unique**: K (eval-mode), M (auto-detect fabrication)

## Summary
- Total unique proposals after dedup: 12
- High-overlap clusters: {B, K, G} (gate failure handling), {C, L} (verdict model)
- All proposals cite evidence from the same v3.0 eval run (4 runs: 2 local, 2 global)
