# Tier 2 — root-cause-analyst hypothesis (H-RCA)

**Author**: root-cause-analyst (inline)
**Tier**: 2
**Type**: bug

## Claim

**Root cause: dimension-orthogonality fallacy in the rubric.** The 5 dimensions (Evidence grounding, Symptom coverage, Reproducibility fit, Fix directness, Domain coherence) are treated as *independent* — but for runtime-behavior hypotheses they are *causally coupled to grounding*. If grounding is incomplete (calibrator can't run the predicted behavior), then symptom-coverage, reproducibility-fit, and fix-directness scores are all *conditional on the unverified grounding*. Treating them as independent and averaging them is a category error analogous to averaging a 0.5 probability with four 1.0 probabilities of *consequences-of-that-probability* — the dependency structure is lost.

In pr86: all 5 reviewer findings were structurally coherent (high symptom/repro/fix/domain scores), but every one of them rested on PR-sha citations the calibrator couldn't verify. The 0.5 should have **propagated** through the dependent dimensions, not been averaged against them.

## Evidence

- `escalation-rubric.md:11-17` — dimension table presents 5 dimensions as a flat axis-aligned grid; no dependency annotation.
- `confidence-calibrator.md:53` — "Score each dimension 0.0 / 0.5 / 1.0 per the rubric's anchor language" — explicit per-dimension independence.
- `tier2-root-cause-analyst-calibration.md:13`: even though the agent flagged "0.5 — calibrator lacked Bash", the downstream dimensions ALL stayed at 1.0 because they were graded on the card's *internal coherence*, not against the unverifiable grounding.
- H3 fingerprint: a refute verdict whose mechanism-coverage and reproducer-fit are high *only if* the source-only reading correctly predicts runtime — which is exactly what was unverified.

## Proposed Fix

**Dependency-aware aggregation**. When `Evidence grounding < 1.0`:
- Cap `Symptom coverage`, `Reproducibility fit`, and `Fix directness` at `min(self, Evidence grounding + 0.3)`. (Allows some independence buffer but propagates the grounding hole.)
- Domain-coherence stays orthogonal (it's a meta-property, not a content-property).
- Then average. For the H3/pr86 fingerprint: 0.5, 0.8 (capped), 0.8, 0.8, 1.0 → 0.78. Escalation triggers.

## Confidence

**Self-reported: 0.85**. Dependency-coupling explanation is mechanistically sound; the cap-formula is one of several reasonable choices.

## Risks

- Cap factor (0.3 buffer) is heuristic; needs eval data.
- May trip on legitimate cases where source-only reading is perfectly conclusive (e.g., syntax-level bugs).

## If I'm wrong...

...the bug is upstream — calibrator agent ignoring the spec instruction "treat self-reported confidence as signal, not number." Then the rubric arithmetic is innocent and the agent prompt is guilty.
