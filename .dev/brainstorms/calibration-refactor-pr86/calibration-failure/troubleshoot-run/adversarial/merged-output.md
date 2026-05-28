# Adversarial Merged Output — Calibration Failure Diagnosis

## Convergence

HYBRID — three layered fixes targeting three distinct mechanisms.

## Chosen Diagnosis (load-bearing)

**H-RCA**: The rubric's flat arithmetic mean treats 5 dimensions as independent, but for runtime-behavior hypotheses they are causally coupled through Evidence-grounding. A 0.5 grounding score should propagate through dependent dimensions, not be averaged against them.

## Layered Fix

### Layer 1 (load-bearing) — Dependency-aware aggregation (H-RCA)

Modify `refs/escalation-rubric.md`:
- When `Evidence grounding < 1.0` AND hypothesis predicts runtime behavior (new `grounding_predicate_type` field), cap calibrated score at `min(mean, 0.84)`.
- Alternative formulation: cap dependent dimensions (symptom, repro, fix) at `Evidence_grounding + 0.3` before averaging.

### Layer 2 (guardrail) — Pin tests (H-QE)

Add 3 eval cases to the calibrator's test suite:
- sha-pinned PR citation without Bash → calibrated ≤ 0.84
- Source-only prediction of runtime behavior → calibrated ≤ 0.84
- Property: `evidence_grounding ≤ 0.5` → calibrated ≤ 0.85 (regardless of other dimensions)

### Layer 3 (defense-in-depth, optional) — Anti-anchoring (H-RefExp)

- Ensemble 2 calibrator instances per card; take minimum.
- Mask card's self-report in calibrator input.
- Probe: "what would have changed your score by 0.1?"

## Why these stack

Layer 1 closes the structural hole. Layer 2 ensures regression-safety. Layer 3 hardens against the residual cognitive failure mode that the prompt-level instruction cannot reliably prevent. Each layer addresses a different root cause; they do not substitute for one another.
