# Diff Analysis: Calibration-Failure Theory Comparison (Agent C run)

## Metadata
- Generated: 2026-05-26
- Variants compared: 3 (A=unmediated, B=sc:reflect-degraded, C=sc:troubleshoot)
- Total differences found: 11
- Categories: structural (2), content (3), contradictions (1), unique (3), shared assumptions (2)

## Structural Differences

| #     | Area              | Variant A           | Variant B                       | Variant C                          | Severity |
|-------|-------------------|---------------------|---------------------------------|------------------------------------|----------|
| S-001 | Front-matter      | Mechanism files list | Skill-failure disclosure block | Skill-call evidence + Wave summary | Low      |
| S-002 | Cross-theory section | "Cross-theory implications" (compounding analysis) | Divergence table only | "Where the troubleshoot tiers landed" + meta-observation | Medium |

## Content Differences

| #     | Topic                          | Variant A Approach                                       | Variant B Approach                                | Variant C Approach                            | Severity |
|-------|--------------------------------|----------------------------------------------------------|---------------------------------------------------|-----------------------------------------------|----------|
| C-001 | Theory 1 (arithmetic mean)     | Veto/cap: dim ≤0.5 caps composite at 0.75                | Gated min: `min(evidence_grounding, mean(other_four))` | Conditional cap: ≤0.84 when grounding<1.0 AND runtime-behavior predicate | Low |
| C-002 | Theory 2 (evidence dimension)  | SPLIT into Source-citation + Runtime-verification        | ADD sixth Runtime check dimension                 | Subsumed under C1 + addressed via pin tests (C2) | Medium |
| C-003 | Theory 3 (third mechanism)     | Stripped-context removes doubt signal (information-channel) | Verdict-direction asymmetry (REFUTE cost ≠ AFFIRM cost) | Residual anchoring leak from card's self-report | High |

## Contradictions

| #     | Point of Conflict              | A Position                                      | B Position                                      | C Position                                  | Impact |
|-------|--------------------------------|-------------------------------------------------|-------------------------------------------------|---------------------------------------------|--------|
| X-001 | Nature of third mechanism      | Information loss in calibrator's input channel  | Asymmetric cost-of-being-wrong by verdict direction | Anchoring leak from self-report number      | Medium — different fixes |

## Unique Contributions

| #     | Variant | Contribution                                              | Value Assessment |
|-------|---------|-----------------------------------------------------------|------------------|
| U-001 | A       | Theory 3: stripped-context removes doubt signal; fix = mandatory "Falsification standard" field that survives the strip | High |
| U-002 | B       | Theory B3: verdict-direction asymmetry (REFUTE has higher cost-of-being-wrong than AFFIRM); fix = `verdict=REFUTE AND claim_class=runtime-behavior → cap at 0.70` | High |
| U-003 | C       | Theory C2: calibrator eval suite (8/8, P=1.0 R=1.0) has silent-green coverage of structurally-unverifiable predicates; fix = 3 pin tests | High |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|------------|------------------|--------|--------|
| A-001 | Arithmetic-mean rubric structure is the load-bearing mechanism (all three rank it first) | All 3 Theory-1 confidences: A=0.85, B=0.92, C=0.85 | If wrong, all three primary fixes miss the real cause | UNSTATED — none of the three test whether removing the average alone would have caught H3 |
| A-002 | The pr86 substrate is structurally analogous to H3 (substrate-fidelity inference) | All three explicitly invoke pr86 as proxy for missing H3 substrate | If H3 differs (e.g., all five dims self-scored 1.0), the dilution math is the wrong target | STATED in A (caveat at end), implicit in B and C |

## Summary
- Total structural differences: 2
- Total content differences: 3
- Total contradictions: 1
- Total unique contributions: 3
- Total shared assumptions surfaced: 2 (UNSTATED: 1, STATED-with-caveat: 1)
- Highest-severity items: C-003 (third-mechanism divergence), X-001 (same)
- Convergence baseline: HIGH on Theory 1 (arithmetic mean), HIGH on Theory 2 (evidence-grounding OR-clause + Read-only tool), LOW on Theory 3 (three distinct mechanisms)
