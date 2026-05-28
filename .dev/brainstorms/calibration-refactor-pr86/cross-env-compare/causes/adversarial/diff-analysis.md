# Diff Analysis: Cross-Environment Calibration-Failure Cause Merge

## Metadata

- Generated: 2026-05-27T00:30Z
- Variants compared: 2
- Variant 1: pr86-substrate run (this environment) — `calibration-failure/FINAL-MERGED-CAUSES.md` (33.7 KB, 2026-05-26T19:38)
- Variant 2: T4-substrate run (other environment) — `Calibration-Refactor-pr86-B/FINAL-MERGED-CAUSES.md` (13.2 KB, 2026-05-27T00:19)
- Total differences found: 14
- Categories: structural (4), content (5), contradictions (1), unique (3), shared assumptions (1)

## Structural Differences

| #     | Area                  | Variant 1 (pr86-substrate)                                                         | Variant 2 (T4-substrate)                                                  | Severity |
|-------|-----------------------|------------------------------------------------------------------------------------|---------------------------------------------------------------------------|----------|
| S-001 | Top-line organization | Mechanism-tagged (M1/M2/M3a/M3b/M3c/M4) with cross-mechanism implications          | Ranked list (#1-#5) with layer tagging (audit/generation/design/assignment) | Medium   |
| S-002 | Depth/length          | 269 lines, deep mechanism-decomposition + synthesis addendum                       | 139 lines, terse ranked-list + convergence stats                          | Medium   |
| S-003 | Provenance scaffolding| Heavy HTML-comment provenance per section (Source: Variant N, line N)              | Single header-block provenance; per-cause evidence only                   | Low      |
| S-004 | Section taxonomy      | Mechanism→Evidence→Confidence→Fix per M; cross-mechanism; synthesis addendum 1-5  | Top causes → Unresolved contradictions → Excluded → Stats → Shared assumptions | Medium |

## Content Differences

| #     | Topic                                | Variant 1 Approach                                                                                                      | Variant 2 Approach                                                                                                       | Severity |
|-------|--------------------------------------|-------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------|----------|
| C-001 | Arithmetic-mean dilution             | M1 — primary mechanism, 0.89 confidence, cites `(0.5+4×1.0)/5=0.90` arithmetic verbatim from `tier2-RCA-calibration.md:11-17` | A-δ (shared assumption #4) — confirmed correct as-written from `escalation-rubric.md:19`; not promoted to a top cause | High     |
| C-002 | Source-vs-runtime evidence conflation| M2 — primary mechanism, 0.85 confidence; "OR clause" trap; recommends 6th Runtime-check dimension                       | #2 — "rubric evidence-class disjunction"; identical mechanism, 0.80 likelihood; layer = generation                       | Low      |
| C-003 | Verdict-direction asymmetry          | M3a — 0.78 confidence; cites the H3 0.95-REFUTE explicitly; recommends verdict-direction modifier capping ≤0.70         | #3 — refute-vs-confirm asymmetry; 0.70 likelihood; same rubric symmetry critique; same H3 example                       | Low      |
| C-004 | Calibrator non-execution             | Not addressed as a primary cause — assumes calibrator ran (`tier2-*-calibration.md` files exist on the pr86 substrate) | #1 — TOP cause, 0.85 likelihood; empirically verified by `ls` returning "no such file or directory"                     | High     |
| C-005 | Eval-suite silent-green / pin tests  | M4 — 0.68 confidence; recursion-of-anti-pattern framing; recommends 3 pin tests                                          | Not addressed                                                                                                            | High     |

## Contradictions

| #     | Point of Conflict             | Variant 1 Position                                                                                            | Variant 2 Position                                                                                                            | Impact |
|-------|-------------------------------|---------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------|--------|
| X-001 | Did the calibrator execute?   | Implicitly assumes YES — entire mechanism stack (M1/M2/M3a/M3b/M3c) reasons about the calibrator's *output* on pr86 substrate, citing `tier2-root-cause-analyst-calibration.md:11-19` evidence-grounding=0.5 + four 1.0s = 0.90 | EMPIRICALLY VERIFIED NO on T4 substrate — `ls .../tier2-*-calibration.md` returns "No such file or directory"; the H3 0.95 is agent self-report passed through unchecked | High — different substrates have *different* failure modes. pr86 = "calibrator ran but the math is broken"; T4 = "calibrator never ran at all" |

## Unique Contributions

| #     | Variant | Contribution                                                                                                                                       | Value Assessment |
|-------|---------|----------------------------------------------------------------------------------------------------------------------------------------------------|------------------|
| U-001 | V1 (pr86) | M4 (eval-suite silent-green pin tests) + Cross-mechanism compounding analysis (M1×M2 multiplicative; M2→M3a sequential; M4 as prevention-layer)    | High             |
| U-002 | V1 (pr86) | M3b (Falsification-standard card field) + M3c (dual-instance-minimum) sub-mechanisms with independent fixes                                        | Medium-High      |
| U-003 | V2 (T4) | Calibrator-non-execution as the empirically-verifiable #1 cause; layer taxonomy (audit/generation/design/assignment); INV-002 partial-calibration; agent-domain mismatch (#5) | High             |

## Shared Assumptions

| A-NNN | Assumption                                                                                                                                                                 | Source Agreement                                                                                                                                                              | Impact                                                                                                                                                                                                                                                                                            | Status                                                       |
|-------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------|
| A-001 | The rubric/calibrator IS the right layer to fix the calibration-failure pathology                                                                                          | Both variants prescribe fixes at the rubric (M1/M2 dimension changes) and calibrator-agent layers; neither considers an upstream verification-gate that requires runtime output before confidence is assignable | High — if the right fix is an upstream "runtime-check-required-before-confidence-eligible" gate, both merges are recommending the wrong layer. V2 explicitly names this as A-α in §5.                                                                                          | UNSTATED in V1; STATED in V2 (A-α); flagged for Step 4       |

## Summary

- Total structural differences: 4 (1 Medium, 2 Medium, 1 Low)
- Total content differences: 5 (3 High, 2 Low)
- Total contradictions: 1 (High — X-001 substrate-divergent failure mode)
- Total unique contributions: 3 (2 High, 1 Medium-High)
- Total shared assumptions surfaced: 1 (UNSTATED → STATED hybrid; A-001 promoted to debate attention)
- Highest-severity items: C-001, C-004, C-005, X-001

**Convergence baseline (pre-debate)**: 4 of 5 top mechanisms appear in both variants in some form (M2/C-002, M3a/C-003, A-001/A-δ, and at least partial overlap on M1/A-δ). 2 mechanisms are unique to one side (M4 to V1; calibrator-non-execution to V2). The substrate divergence in X-001 is the load-bearing diagnostic finding.
