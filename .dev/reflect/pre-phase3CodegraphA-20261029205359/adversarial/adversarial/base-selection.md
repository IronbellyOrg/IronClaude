# Base Selection: reviewer-card merge

"Requirements" for requirement coverage (RC) are the 17 actionable, non-refuted merged findings that a reviewer raised: M-01..M-16 and M-18, from `consensus-draft.md`. M-17 is excluded because a calibrator surfaced it, not a reviewer. Scores come from the card text, after the debate's refutations.

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant 1 | Variant 2 | Computation |
|---|---|---|---|---|
| Requirement coverage (RC) | 0.30 | 0.824 | 0.294 | V1 raised 14 of 17 (M-01..M-14). V2 raised 5 of 17 (M-04 as an advisory note, M-08 via R2-05, M-15, M-16, M-18). |
| Internal consistency (IC) | 0.25 | 0.933 | 0.750 | V1: 1 refuted claim of 15 (R1-13). V2: 2 false claims of 8 (the "no Regression" verdict; R2-02's troubleshoot half). |
| Specificity ratio (SR) | 0.15 | 0.95 | 0.90 | Both cite lines throughout. V2 has two fixes reading "No plan change" / "None". |
| Dependency completeness (DC) | 0.15 | 0.95 | 0.95 | V1 cited R1-12 at :262/:277 where the conflicting text is at :255. V2 cites INF-* ids that the calibrator could not verify. |
| Section coverage (SC) | 0.15 | 0.80 | 1.00 | Top-level keys: V1 has 8, V2 has 10 (adds `verdict` and `advisory_notes`). |
| **quant_score** | | **0.884** | **0.702** | |

## Qualitative Scoring (50% weight): Additive Binary Rubric (CEV)

| Dimension / criterion | V1 | V2 | Evidence |
|---|---|---|---|
| Completeness 1: all explicit requirements | NOT MET | NOT MET | Each card missed findings the other raised (V1 missed R2-01, R2-02 and U-012; V2 missed R1-01, R1-02, R1-03, R1-06 and others) |
| Completeness 2: edge and failure scenarios | MET | MET | V1: R1-04 (false new failure), R1-07. V2: the advisory note on the superset |
| Completeness 3: dependencies and prerequisites | MET | NOT MET | V1: R1-06 (untracked inputs). V2: none |
| Completeness 4: success criteria | MET | MET | Both give fixes |
| Completeness 5: out of scope stated | MET | NOT MET | V1 self_audit: "DES and E-1..E-7 inputs not read" |
| Correctness 1: no factual errors | NOT MET | NOT MET | V1: R1-13 refuted by DES:535-536. V2: verdict refuted by test:294 |
| Correctness 2: feasible fixes | NOT MET | MET | V1: R1-01's `$(cat …)` fix is unproven (corrected in Round 2) |
| Correctness 3: terminology accurate | NOT MET | NOT MET | Both cards misapply the deviation classes (Round 1 concessions) |
| Correctness 4: no internal contradictions | MET | MET | Neither card contradicts itself |
| Correctness 5: claims backed by evidence | MET | MET | Line citations throughout |
| Structure 1-5 | 5/5 | 5/5 | Ordered ids, consistent schema, separate calibration blocks, follows the reviewer-card convention |
| Clarity 1: unambiguous | MET | MET | |
| Clarity 2: concrete | MET | MET | |
| Clarity 3: clear purpose per section | MET | MET | |
| Clarity 4: terms defined | NOT MET | NOT MET | V1 uses G6, H5 and "T1 D-2" undefined. V2 uses INF-022 etc. undefined |
| Clarity 5: actionable next steps | MET | MET | |
| Risk 1: at least 3 risks with probability and impact | NOT MET | NOT MET | Severity is given, probability is not |
| Risk 2: mitigation per risk | MET | NOT MET | V2: R2-03 and R2-04 have no fix |
| Risk 3: failure modes and recovery | MET | NOT MET | V1: R1-06 escalate, R1-07 H5 |
| Risk 4: external dependencies | MET | NOT MET | V1: pr-submit flags, `gh`, live session |
| Risk 5: validation mechanism | MET | MET | V1: R1-03 names the test. V2: R2-01 adds an assertion |
| Invariant 1: empty or boundary collections | MET | NOT MET | V1: R1-04 pipefail-safe empty-failure pipeline |
| Invariant 2: state across components | MET | MET | V1: R1-08 tracked state after the commit. V2: R2-05 |
| Invariant 3: guard gaps | MET | NOT MET | V1: R1-11 ineffective guard |
| Invariant 4: count divergence | MET | MET | V1: R1-15 count equality. V2: superset count |
| Invariant 5: interaction effects | MET | MET | V1: R1-10 (Task 7 vs Task 12). V2: R2-02 (Tasks 6/7/10) |

### Qualitative Summary

| Dimension | V1 | V2 |
|---|---|---|
| Completeness | 4 | 2 |
| Correctness | 2 | 3 |
| Structure | 5 | 5 |
| Clarity | 4 | 4 |
| Risk Coverage | 4 | 1 |
| Invariant & Edge Case | 5 | 3 |
| **Total** | **24/30 = 0.80** | **18/30 = 0.60** |

### Edge Case Floor Check
V1 scores 5/5 and V2 scores 3/5. Both are eligible.

## Position-Bias Mitigation
- Pass 1 evaluated V1 then V2; pass 2 evaluated V2 then V1. One evaluator (the orchestrator) ran both passes.
- Disagreements: 1. V2 Correctness 3 was MET in pass 1 because the labels are consistent, and NOT MET in pass 2 because R2-05 and R2-06 are not Drift. Re-evaluation with both pieces of evidence gave NOT MET as the final verdict.
- Verdicts changed: 1.

## Combined Scoring

| Variant | Quant × 0.5 | Qual × 0.5 | Final |
|---|---|---|---|
| Variant 1 (reviewer-1, sonnet/analyzer) | 0.442 | 0.400 | **0.842** |
| Variant 2 (reviewer-2, glm-5.3/qa) | 0.351 | 0.300 | **0.651** |

Margin: 19.1 points, so no tiebreaker applies. V1 also won 9 of the 15 diff points outright; the rest were shared or both.

## Selected Base: Variant 1 (reviewer-1 card)

**Why it wins.** V1 carries the three verified defects that make the plan fail when run (M-01, M-03, M-08), plus the untracked-input blocker (M-06). It covers 14 of the 17 reviewer-raised findings.

**Strengths to keep.** V1's findings and its exact fixes, as corrected in Round 2 (M-01 inline `--body`; M-07 narrowed to loading the new commands).

**Strengths to take from V2:**
- R2-01, with its fix corrected per DES:478.
- R2-02, narrowed to `reflect.md:6` in both the src file and the plugin twin.
- R2-05's commit-point divergence, merged into M-08.
- R2-06, plus its calibrator's Task 8 message item (M-18).
- The advisory note's spec-origin label for M-04.
- The origin field (plan-only or inherited-from-spec), which V1 lacked.

**Taken from V1's calibrator:** the G3 continue rule (M-17).

**Base weaknesses to fix:**
- About eight class labels (corrected per the transcript).
- R1-13 (refuted).
- R1-06 over-breadth (narrowed).
