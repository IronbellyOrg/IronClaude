# Base Selection Report

## Quantitative Scoring (50% weight)
Mode A compares reviewer cards, not implementation specs. Requirement-coverage proxy: the eight distinct review concerns U-001 to U-008 in diff-analysis.md; each card covers four. This measures breadth, not defect validity. Claims counted are the four finding claims per card. Dependencies counted are evidence-list entries (A eight, B ten); all named files resolve, irrespective of whether a cited claim is convincing. Sections counted are twelve top-level YAML fields per card. A bounded YAML count confirmed these cardinalities.

| Metric | Weight | Variant A (sonnet analyzer) | Variant B (haiku QA) |
|---|---|---|---|
| requirement_coverage | .30 | 4/8 = .50 | 4/8 = .50 |
| internal_consistency | .25 | 1 - 0/4 = 1 | 1 - 0/4 = 1 |
| specificity_ratio | .15 | 4/4 = 1 | 4/4 = 1 |
| dependency_completeness | .15 | 8/8 = 1 | 10/10 = 1 |
| section_coverage | .15 | 12/12 = 1 | 12/12 = 1 |
| **quant_score** | | **.8500** | **.8500** |

No internal contradiction means no opposing claims within one card. It does not mean all claims are true; correctness is assessed below.

## Qualitative Scoring (50% weight)
Each row states the criterion (claim), the binary verdict, and evidence. A/B refer to variant-1-original.md / variant-2-original.md. Absence verdicts follow inspection of all findings, recommendations and card metadata. Criteria follow scoring-protocol.md exactly; no partial credit.

### Completeness (5 criteria)
| Criterion | A | Evidence | B | Evidence |
|---|---|---|---|---|
| All explicit requirements | NOT MET | No Task 5 review in findings/self_audit | NOT MET | No Task 3 review in findings/note |
| Edge cases/failures | MET | F1 invalid backtick tokens | MET | QA-02 missing captures; QA-04 changed Date |
| Dependencies/prerequisites | MET | F1 ties acceptance to REASON_TABLE | MET | QA-02 capture precondition |
| Completion criteria | MET | F1 zero unexplained misses | MET | QA-02 all fixtures or revised gate |
| Explicit out-of-scope | NOT MET | No review scope exclusion field | NOT MET | No review scope exclusion field |
| Subtotal | 3/5 | | 3/5 | |

### Correctness (5 criteria)
| Criterion | A | Evidence | B | Evidence |
|---|---|---|---|---|
| No factual errors | NOT MET | F3/F5 withdrawn in Round 2 | NOT MET | QA-02 coverage-matrix allegation not verified in Round 2 |
| Feasible with constraints | MET | F1 and F4 require bounded plan clarifications | MET | F2/QA-03/04 keep parser changes out of scope |
| Consistent terminology | MET | F-series IDs and plan-gap class | MET | Distinct IDs, consistent plan-gap class |
| No internal contradictions | MET | No opposed claims among four findings | MET | QA-02 describes a plan contradiction, not a contradiction within the card |
| Evidence/rationale | MET | Eight evidence entries for four findings | MET | Ten entries plus fixture consumer evidence |
| Subtotal | 4/5 | | 4/5 | |

### Structure (5 criteria)
| Criterion | A | Evidence | B | Evidence |
|---|---|---|---|---|
| Logical ordering | MET | Metadata, findings, calibration | MET | Same card order |
| Consistent hierarchy | MET | Each finding has claim/evidence/recommendation | MET | Same finding hierarchy |
| Separation of concerns | MET | Findings separate from self_audit | MET | Findings separate from note/calibration |
| Navigation aids | MET | IDs, source anchors, calibration_ref | MET | IDs, source anchors, calibration_ref |
| Artifact conventions | MET | Reviewer YAML schema fields present | MET | Reviewer YAML schema fields present; self_audit is useful, not schema-mandatory |
| Subtotal | 5/5 | | 5/5 | |

### Clarity (5 criteria)
| Criterion | A | Evidence | B | Evidence |
|---|---|---|---|---|
| Unambiguous language | MET | F1 specifies three misses plus fourth | MET | QA-03 names payload/raw mismatch |
| Concrete statements | MET | F4 names map line and section 16 | MET | QA-04 names Date and consuming test |
| Clear section purposes | MET | claim/evidence/recommendation labels | MET | Same labels |
| Terms defined first use | NOT MET | T1/AC not expanded within card | NOT MET | T1/FU-1 not expanded within card |
| Actionable next steps | MET | Each of four findings has recommendation | MET | Each of four findings has recommendation |
| Subtotal | 4/5 | | 4/5 | |

### Risk Coverage (5 criteria)
| Criterion | A | Evidence | B | Evidence |
|---|---|---|---|---|
| Three risks with probability/impact | NOT MET | Severity only; no probability assessment | NOT MET | Severity only; no probability assessment |
| Mitigation for each risk | MET | Four recommendations | MET | Four recommendations |
| Failure/recovery procedures | NOT MET | F1 check correction, no recovery workflow | MET | QA-04 separates expected-value repair from parser follow-up |
| External dependency failures | NOT MET | Findings focus on design/runbook | MET | QA-02 missing owner captures; QA-03 real gh envelope |
| Validation mechanism | MET | F1 zero unexplained misses | MET | F2 secret check; QA-03 consumed field verification |
| Subtotal | 2/5 | | 4/5 | |

### Invariant & Edge Case Coverage (5 criteria)
| Criterion | A | Evidence | B | Evidence |
|---|---|---|---|---|
| Collection boundaries | NOT MET | No absent-capture collection assessment | MET | QA-02 missing captures versus all-fixture gate |
| State across components | NOT MET | No fixture-to-test state transition | MET | QA-03 changed marker with unchanged consumed raw |
| Guard condition gaps | MET | F1 token-membership guard rejects non-reasons | MET | QA-02 precondition conflicts with body |
| Count divergence | NOT MET | F3 count objection withdrawn; no valid count finding | MET | QA-02 all-fixture goal versus subset completion |
| Interaction effects | MET | F4 new section 16 versus existing map | MET | QA-04 capture Date versus test expectation |
| Subtotal | 2/5 | Eligible (at least 1/5) | 5/5 | Eligible (at least 1/5) |

### Qualitative Summary
| Dimension | A | B |
|---|---|---|
| Completeness | 3/5 | 3/5 |
| Correctness | 4/5 | 4/5 |
| Structure | 5/5 | 5/5 |
| Clarity | 4/5 | 4/5 |
| Risk Coverage | 2/5 | 4/5 |
| Invariant & Edge Case Coverage | 2/5 | 5/5 |
| **qual_score** | **20/30 = .6667** | **25/30 = .8333** |

## Position-Bias Mitigation
Pass 1 evaluated A then B. Pass 2 evaluated B then A against the same source cards, checking especially whether recovery/count concerns were valid evidence rather than rewarding length. Each cell below is A/B (1=MET, 0=NOT MET), independent of evaluation order; evidence is in the corresponding criterion row above.

| Criterion (ordinal within dimension) | Pass 1 A then B | Pass 2 B then A | Agreement | Final A/B |
|---|---|---|---|---|
| Completeness 1 | 0/0 | 0/0 | yes | 0/0 |
| Completeness 2 | 1/1 | 1/1 | yes | 1/1 |
| Completeness 3 | 1/1 | 1/1 | yes | 1/1 |
| Completeness 4 | 1/1 | 1/1 | yes | 1/1 |
| Completeness 5 | 0/0 | 0/0 | yes | 0/0 |
| Correctness 1 | 0/0 | 0/0 | yes | 0/0 |
| Correctness 2 | 1/1 | 1/1 | yes | 1/1 |
| Correctness 3 | 1/1 | 1/1 | yes | 1/1 |
| Correctness 4 | 1/1 | 1/1 | yes | 1/1 |
| Correctness 5 | 1/1 | 1/1 | yes | 1/1 |
| Structure 1 | 1/1 | 1/1 | yes | 1/1 |
| Structure 2 | 1/1 | 1/1 | yes | 1/1 |
| Structure 3 | 1/1 | 1/1 | yes | 1/1 |
| Structure 4 | 1/1 | 1/1 | yes | 1/1 |
| Structure 5 | 1/1 | 1/1 | yes | 1/1 |
| Clarity 1 | 1/1 | 1/1 | yes | 1/1 |
| Clarity 2 | 1/1 | 1/1 | yes | 1/1 |
| Clarity 3 | 1/1 | 1/1 | yes | 1/1 |
| Clarity 4 | 0/0 | 0/0 | yes | 0/0 |
| Clarity 5 | 1/1 | 1/1 | yes | 1/1 |
| Risk 1 | 0/0 | 0/0 | yes | 0/0 |
| Risk 2 | 1/1 | 1/1 | yes | 1/1 |
| Risk 3 | 0/1 | 0/1 | yes | 0/1 |
| Risk 4 | 0/1 | 0/1 | yes | 0/1 |
| Risk 5 | 1/1 | 1/1 | yes | 1/1 |
| Invariant 1 | 0/1 | 0/1 | yes | 0/1 |
| Invariant 2 | 0/1 | 0/1 | yes | 0/1 |
| Invariant 3 | 1/1 | 1/1 | yes | 1/1 |
| Invariant 4 | 0/1 | 0/1 | yes | 0/1 |
| Invariant 5 | 1/1 | 1/1 | yes | 1/1 |

Disagreements re-evaluated: 0. Final verdicts changed: 0. This is order reversal within one judging context, not a claim of independent blind grading.

## Combined Scoring
| Variant | Quant x .50 | Qual x .50 | Final score | Debate wins |
|---|---|---|---|---|
| A | .4250 | .3333 | .7583 | 4/11 |
| B | .4250 | .4167 | .8417 | 3/11 |

Margin: .0833 (8.33 percentage points), above the 5% tiebreaker threshold. Tiebreaker not applied. Both variants exceed the invariant floor. Arithmetic verified with a tolerance-based numeric check; an initial exact-float equality assertion failed on representation and was corrected with isclose, not by changing any score.

## Selected Base: Variant B (haiku:qa)
### Selection Rationale
B wins by calibrated substantive risk coverage, not by its inflated self-confidence or its original high QA-02 severity. The underlying card remains imperfect; both Round 2 rebuttals and the invariant probe narrow its claims. A wins more individual comparison points, but the score margin makes that tiebreaker irrelevant. No selection implies plan approval.
### Strengths to Preserve from Base
1. Capture-verification surface gap, F2, without alleging an observed leak.
2. Task 5 every-fixture gate contradiction, raw consumer field, and capture-dependent expected values, with Round 2 qualifications.
### Strengths to Incorporate from Non-Base Variants
1. A's impossible reason-token acceptance check, F1, and low section-map omission, F4.
2. A's self-audit discipline and the explicit withdrawal of F3/F5 as defects.
3. Probe limitations: unreviewed Task 3 fidelity and conditional CRLF test-adapter interaction. Preserve them as warnings; no new runtime defect is established.
