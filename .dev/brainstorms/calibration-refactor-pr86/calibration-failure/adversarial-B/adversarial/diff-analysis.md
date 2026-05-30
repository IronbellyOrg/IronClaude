# Diff Analysis: Calibration-Failure Theory Comparison (Agent B run)

## Metadata
- Generated: 2026-05-26
- Variants compared: 3 (Agent A unmediated, Agent B sc:reflect-degraded, Agent C sc:troubleshoot)
- Total differences found: 9
- Categories: structural (2), content (3), contradictions (0), unique (2), shared assumptions (2)

## Structural Differences

| # | Area | Variant A | Variant B | Variant C | Severity |
|---|---|---|---|---|---|
| S-001 | Document structure | Three theories + cross-theory implications | Reflection invocation evidence + three theories + divergence + appendix | Troubleshoot invocation + three theories + tier-landing narrative | Low |
| S-002 | Theory naming scheme | T1/T2/T3 | B1/B2/B3 | C1/C2/C3 | Low |

## Content Differences

| # | Topic | Variant A | Variant B | Variant C | Severity |
|---|---|---|---|---|---|
| C-001 | Theory 1 (arithmetic mean) | "Arithmetic-mean dilution"; conf 0.85; fix = veto/cap at ≤0.5 → 0.75 ceiling | "Arithmetic-mean dilution"; conf 0.92; fix = min(evidence, mean(other_four)) | "Dimension-orthogonality blind"; conf 0.85; fix = min(mean, evidence+0.3) for runtime claims | Low (same mechanism, different fix formulations) |
| C-002 | Theory 2 (source-vs-runtime) | "OR clause conflates source-citation w/ runtime-verification"; conf 0.80; fix = split into 2 dimensions | "Evidence grounding blind to runtime-behavior claims"; conf 0.88; fix = add 6th dimension "Runtime check" | (Not directly mirrored — folded into C1's "runtime_behavior" predicate) | Medium (A/B explicit, C implicit) |
| C-003 | Theory 3 (third mechanism) | Stripped-context removes doubt signal; conf 0.65 | Verdict-direction asymmetry (REFUTE cost); conf 0.78 | Residual anchoring leak from self-report; conf 0.45 | High (three genuinely different third theories) |

## Contradictions

None detected. All three variants converge on the arithmetic-mean rubric structure as the load-bearing mechanism and agree on the source-vs-runtime evidence gap.

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---|---|---|
| U-001 | C | Theory C2 — calibrator eval suite silent-green coverage; "1.000/1.000" precision/recall claim is doing work it can't carry; recommends pin tests | High (only variant to propose a guardrail-via-test mechanism distinct from rubric-fix mechanisms) |
| U-002 | B | Verdict-direction asymmetry (REFUTE vs AFFIRM cost-of-being-wrong); H3 is canonical REFUTE-closes-door case | High (introduces decision-theoretic framing absent from A and C) |
| U-003 | A | Cross-theory multiplicative-compounding analysis ("T1 and T2 compound, T3 is upstream") | Medium (synthesis distinct from any single theory) |
| U-004 | C | Self-recursive verification framing ("calibration system fails the same way the code it calibrated fails") | Medium (rhetorical/meta-level; not actionable on its own) |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|---|---|---|---|---|
| A-001 | The H3 0.95 REFUTE case is structurally analogous to the pr86 substrate calibration shape (0.90 from 0.5+4×1.0) despite H3 artefacts being absent on disk | All three variants extrapolate from pr86 to H3 without H3 evidence | High — if structural analogy breaks, all three theories' H3 grounding weakens | UNSTATED (promoted) |
| A-002 | The calibrator's `tools: Read` restriction is the root tool-access limit (not policy-removable at the rubric layer alone) | A T2, B B2, C C1 all cite confidence-calibrator.md tool surface | Medium — fixes that depend on Bash being added to calibrator agent are out-of-scope of rubric/scoring fixes | UNSTATED (promoted) |

## Summary
- Total structural differences: 2
- Total content differences: 3
- Total contradictions: 0
- Total unique contributions: 4
- Total shared assumptions surfaced: 2 (UNSTATED: 2, STATED: 0, CONTRADICTED: 0)
- Highest-severity items: C-003 (three different "Theory 3"s requires merge-time selection)
