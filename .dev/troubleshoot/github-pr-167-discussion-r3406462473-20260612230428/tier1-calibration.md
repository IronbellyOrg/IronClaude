# Calibration Report

**Card under calibration**: /config/workspace/IronClaude/.dev/troubleshoot/github-pr-167-discussion-r3406462473-20260612230428/tier1-hypothesis.md  
**Rubric**: /config/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md  
**Card tier**: 1  
**Timestamp**: 2026-06-12

## Per-dimension scores

| Dimension | Score | Justification |
|-----------|-------|---------------|
| Evidence grounding | 1.0 | Card cites exact source and observation evidence; spot-check verified `gates.py:47`, `:52`, `:62`, `test_gates.py:140-145`, `tier1-observation.md:13/18`, `doc-context.md:31-32`, and `diagnosability-context.md:29` match the card's claims. |
| Runtime check | 1.0 | Derived from declared `claim_class=static_defect`, `evidence_class=runtime_repro`; rubric cross-tab gives 1.0. Card cites captured UV reproducer output in `tier1-observation.md`. |
| Symptom coverage | 1.0 | Claim explains both reported shapes: `1. Verdict: PASS` and `__Verdict__: PASS` fail because digits/underscores are `\w` and excluded by `[^\w\n:]*`. |
| Reproducibility fit | 1.0 | Card includes deterministic reproducer with captured output showing both false negatives and positive controls. |
| Fix directness | 1.0 | Proposed fix is localized to `_check_verdict_field` regex/comment plus focused tests for missing ordered-list/underscore cases. |
| Domain coherence | 1.0 | Single-domain parser/regex false negative; card explicitly excludes docs-only and JSON-path alternatives. |

## Confidence

- **Self-reported (in card)**: 0.96 — read but not used as input to this score.
- **Calibrated (this report)**: 1.00
- **Formula applied**: `min(mean(all_six), evidence_grounding + 0.30, runtime_check + 0.30)`; verdict-direction cap not applicable.

## Escalation recommendation

- **Verdict**: STOP
- **Reason**: none
- **Rubric rule fired**: confidence ≥ 0.85 AND single-domain AND reproducible → STOP at Tier 1.

## Notes

No cited local evidence failed spot-check. Tier 2 is not required by the rubric.
