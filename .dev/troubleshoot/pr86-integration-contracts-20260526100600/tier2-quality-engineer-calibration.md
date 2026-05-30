# Calibration Report — quality-engineer (Tier 2)

**Card under calibration**: `/config/workspace/IronClaude/.dev/troubleshoot/pr86-integration-contracts-20260526100600/tier2-quality-engineer-hypothesis.md`
**Rubric**: `/config/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md`
**Card tier**: 2
**Timestamp**: 2026-05-26T10:21:00Z
**Captured from**: confidence-calibrator agent output (disk-write blocked by safety constraint).

## Per-dimension scores

| Dimension | Score | Justification |
|-----------|-------|---------------|
| Evidence grounding | 0.5 | Regex execution reproducer (`FR-S10-02` → `['S10']`) verified analytically. PR-sha-specific citations (TUIBBS_HUB_SPEC, TestHubDispatchRegression, `_signature_subsumed`, PR-line 410-419, 432-433, 355) could not be spot-checked without Bash. Per-card grounding limitation same as the other two Tier 2 calibrations. |
| Symptom coverage | 1.0 | Identifies test_t1, test_t6, test_t7 as silently-green; identifies test_duplicate_lines_deduplicated, test_sequential_id_assignment as at-risk. Mechanism explained per case. |
| Reproducibility fit | 1.0 | Deterministic Python expression for the extractor bug; per-window analysis for downstream Layer 3 behavior. No intermittency. |
| Fix directness | 0.5 | 5 behavior-pin tests + Phase 1 production change + Phase 2 production+test + new conftest.py + snapshot baseline JSON + property-based tests. Total change surface spans 2 files + 1 new file + snapshot artifacts. The diagnosis is tight; the fix is broad. |
| Domain coherence | 1.0 | Single domain: test fidelity + regex extraction logic within one module. |

## Confidence

- **Self-reported**: 0.88
- **Calibrated**: 0.60
- **Delta**: -0.28 — drag from fix-directness (broad change surface) and unverifiable PR-sha citations. The card's reasoning quality is high; the proposed fix specification is broader than rubric prefers.

## Verdict (in the adversarial-debate context)

- **Moderate-to-strong diagnostic strength, broad fix surface.** The phased approach (pin tests first, additive regex second, downstream fixes third) is methodologically sound but adds many moving parts.
- For Wave 4: this card's strongest contribution is the **test-fidelity argument** (test_t1/t6/t7 silently green on wrong invariant) — a finding NEITHER of the other two cards surfaces independently.

## Notes

- If PR-sha citations could be verified, evidence-grounding would rise to 1.0 and calibrated mean to ~0.80 (still below 0.85 due to fix-directness 0.5).
- Phase 0 pin-tests-first IS the safest sequencing — its drag is purely on the calibrated rubric's preference for surgical fix scope, not on the card's correctness.
