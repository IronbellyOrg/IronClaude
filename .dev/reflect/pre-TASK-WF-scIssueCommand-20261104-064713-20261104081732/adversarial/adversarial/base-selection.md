# Base Selection Report

Regenerated on resume (replacement worker, dispatch ctx_f4fb98ca009d, after 12:41 UTC 2026-11-04). The copy written at 12:40:48 by the old worker session, which ran in parallel after the outage, is kept unchanged as `base-selection.partial-1240.md` and was not used as an input. Every number below was recomputed from its sources: the quantitative layer by the script `.work/quant_score.py` (output in `.work/quant-score.out`), the qualitative layer from the two independent evaluator passes `.work/qual-pass1.md` (order V1, V2, V3) and `.work/qual-pass2.md` (order V3, V2, V1), both finished at 09:03 UTC before the outage, and the six pass disagreements re-evaluated by the orchestrator (debate-orchestrator role) in this run. The regenerated result agrees with the partial copy on every score and on the selected base; that agreement was checked after the recomputation, not used to produce it.

Variants: V1 = reviewer-1 card (sonnet:analyzer); V2 = reviewer-2 card (haiku, served by glm-5.3:qa); V3 = reviewer-3 card (opus:refactorer). The inputs are YAML reviewer cards: a "section" is a top-level YAML key and a "claim" is a finding claim, the verdict or the self-audit.

## Quantitative Scoring (50% weight)

| Metric | Weight | V1 | V2 | V3 |
|--------|--------|----|----|----|
| requirement_coverage (RC) | 0.30 | 0.200 (spec sections 7, 12, 13, 19 = 4/20) | 0.500 (sections 4, 7, 8, 12, 13, 14, 15, 16, 17, 20 = 10/20) | 0.150 (sections 13, 14, 20 = 3/20) |
| internal_consistency (IC) | 0.25 | 1.000 (0 claim-vs-claim contradictions / 8 claims) | 1.000 (0 / 6) | 1.000 (0 / 14) |
| specificity_ratio (SR) | 0.15 | 1.000 (22 citations, 0 vague-term hits) | 1.000 (14, 0) | 1.000 (41, 0) |
| dependency_completeness (DC) | 0.15 | 1.000 (self-audit reference A-1 resolves) | 1.000 (no internal references) | 1.000 (S-1 and S-2 resolve) |
| section_coverage (SC) | 0.15 | 0.889 (8/9 keys) | 1.000 (9/9) | 0.778 (7/9) |
| **quant_score** | | **0.7433** | **0.8500** | **0.7117** |

Method: RC maps each `source.md:N[-M]` citation to the H2 section holding those lines (the spec has 20 H2 sections, starting at lines 11, 20, 42, 57, 81, 112, 137, 182, 221, 240, 272, 284, 316, 323, 344, 384, 402, 410, 444, 465) and adds explicit "section N" mentions. IC counts claim-vs-claim contradictions only; V3's S-2, whose own evidence (`refs/ledger.md:161`) refutes it, is a claim-vs-evidence error and is scored under qualitative Correctness 1 and 4, not here. SR uses the protocol's vague-term list. Running the script twice gives the same output.

## Qualitative Scoring (50% weight) - Additive Binary Rubric

Final verdicts after position-bias resolution. CEV evidence for every cell is in `.work/qual-pass1.md` and `.work/qual-pass2.md`; cells settled by re-evaluation are marked (R).

### Completeness
| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| 1 Covers all explicit requirements | NOT MET (missed A-002..A-007) | NOT MET (missed C-001 and all eight A-points) | NOT MET (missed C-001 and A-002..A-007) |
| 2 Edge cases / failure scenarios | MET (A-1 guard failure; A-6 invalid page cap) | NOT MET | MET (S-8 `__pycache__`; S-5 `permissionMode`) |
| 3 Dependencies / prerequisites | MET (A-2; A-1 read-SKILL.md-first prerequisite) | NOT MET | MET (S-3; S-9) |
| 4 Success / completion criteria | MET | MET | MET |
| 5 Out-of-scope items | NOT MET | MET (Q-1 deferred PR step) | NOT MET |
| **Subtotal** | **3/5** | **2/5** | **3/5** |

### Correctness
| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| 1 No factual errors | NOT MET (A-2 second half and A-1 third-party harm path conceded, round2-v1.md:13, :25) | NOT MET (self-audit "ACs observable" conceded false, round2-v2.md:13) | NOT MET ("resume cannot work" conceded false, round2-v3.md:25) |
| 2 Feasible recommendations | MET | MET | MET |
| 3 Terminology / categories accurate | NOT MET (A-1 blocking/safety-risk conceded minor) | NOT MET (R) | NOT MET (S-1 category and S-1/S-2 severities conceded) |
| 4 No internal contradictions | MET | MET | NOT MET (S-2 cites ledger.md:161, which supports resume) |
| 5 Claims cited | MET | MET | MET |
| **Subtotal** | **3/5** | **3/5** | **2/5** |

### Structure
| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| 1 Logical ordering | MET (blocking first) | MET (R) | MET (blocking first) |
| 2 Consistent schema | MET | MET | NOT MET (block and flow styles mixed) |
| 3 One topic per finding | NOT MET (A-3 bundles four claims) | MET | NOT MET (S-6 two topics; S-2 two branches) |
| 4 Navigation aids | MET | MET | MET |
| 5 Card conventions | MET | MET | MET |
| **Subtotal** | **4/5** | **5/5** | **3/5** |

### Clarity
| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| 1 Unambiguous language | MET | MET | NOT MET (S-2 alternative outcomes) |
| 2 Concrete | MET | MET | MET |
| 3 One-sentence summary per finding | NOT MET (A-3) | MET | MET (R) |
| 4 Terms defined on first use | NOT MET | NOT MET | NOT MET |
| 5 Actionable next steps | MET | MET | MET |
| **Subtotal** | **3/5** | **4/5** | **3/5** |

### Risk Coverage
| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| 1 At least 3 risks with impact | MET | NOT MET | MET |
| 2 Mitigation for each | MET | MET | MET |
| 3 Failure modes and recovery | MET | NOT MET | MET |
| 4 External dependencies and failures | MET (R) | NOT MET | MET |
| 5 Validation mechanism | MET | MET | MET |
| **Subtotal** | **5/5** | **2/5** | **5/5** |

### Invariant & Edge Case Coverage
| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| 1 Collection boundaries | MET (A-6 page cap) | NOT MET | NOT MET |
| 2 State interactions across components | MET (A-4 shell state into tests) | NOT MET | MET (S-1, S-5) |
| 3 Guard-condition gaps | MET (A-1 Wave 0 guard) | NOT MET | MET (S-6 presence check) |
| 4 Count divergence | MET (A-4 two of four variables cleared) | NOT MET (R) | NOT MET (R) |
| 5 Interaction effects | MET (A-5 scan vs copied prose) | NOT MET | MET (S-1 table vs scan) |
| **Subtotal** | **5/5** | **0/5** | **3/5** |

### Qualitative Summary
| Dimension | V1 | V2 | V3 |
|---|---|---|---|
| Completeness | 3/5 | 2/5 | 3/5 |
| Correctness | 3/5 | 3/5 | 2/5 |
| Structure | 4/5 | 5/5 | 3/5 |
| Clarity | 3/5 | 4/5 | 3/5 |
| Risk Coverage | 5/5 | 2/5 | 5/5 |
| Invariant & Edge Case | 5/5 | 0/5 | 3/5 |
| **qual_score** | **23/30 = 0.7667** | **16/30 = 0.5333** | **19/30 = 0.6333** |

### Edge Case Floor Check
| Variant | Invariant & Edge Case | Eligible as base |
|---|---|---|
| V1 | 5/5 | Yes |
| V2 | 0/5 | No (below the 1/5 floor) |
| V3 | 3/5 | Yes |

## Position-Bias Mitigation

The two passes were compared cell by cell (30 criteria x 3 variants = 90 pairs). Six pairs disagreed; each was re-evaluated with both passes' evidence side by side, and the re-evaluation verdict is final.

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final and reason |
|---|---|---|---|---|---|
| Correctness 3 | V2 | MET | NOT MET | DISAGREE | NOT MET: V2 conceded its Q-2/Q-3 labels ("Conceded on the label", round2-v2.md:17); both items are round-1-sanctioned authorized expansions, so `spec-command-deviation` and `weakened-test-scope` misdescribe them |
| Structure 1 | V2 | MET | NOT MET | DISAGREE | MET: Q-1..Q-4 follow the plan's line order of their primary anchors (plan:25, :92, :129, :254); pass 2 judged only spec and severity order |
| Clarity 3 | V3 | NOT MET | MET | DISAGREE | MET: the criterion asks whether each finding can be summarised in one sentence; S-2 reduces to "Task 15's stop-and-resume does not fit /sc:implement's semantics" (its wrongness is scored under Correctness) |
| Risk 4 | V1 | MET | NOT MET | DISAGREE | MET: V1 analyses failures of GitHub (A-1), ClickUp (A-3, A-4, A-6) and the executor (A-2); the criterion asks for external dependencies and their failures, not all four the evaluators listed |
| Invariant 4 | V2 | NOT MET | MET | DISAGREE | NOT MET: the self-audit asserts that counts match ("all nine STOP codes"); it examines no divergence scenario |
| Invariant 4 | V3 | MET | NOT MET | DISAGREE | NOT MET: S-3 is a dependency-set mismatch and S-8 a membership issue; neither is a count, off-by-one or range divergence |

Disagreements: 6 of 90 pairs. Final verdicts that differ from pass 1: 3 (V2 Correctness 3, V3 Clarity 3, V3 Invariant 4). Final verdicts that differ from pass 2: 3 (V2 Structure 1, V1 Risk 4, V2 Invariant 4).
Totals: pass 1 V1 23, V2 17, V3 19; pass 2 V1 22, V2 16, V3 19; final V1 23, V2 16, V3 19.

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Eligible |
|---|---|---|---|---|
| V1 (sonnet:analyzer) | 0.3717 | 0.3833 | **0.7550** | yes |
| V2 (haiku->glm-5.3:qa) | 0.4250 | 0.2667 | **0.6917** | no (edge-case floor) |
| V3 (opus:refactorer) | 0.3558 | 0.3167 | **0.6725** | yes |

**Margin**: V1 leads V2 by 6.3 points and the next eligible variant, V3, by 8.3 points; both exceed the 5% tiebreaker threshold.
**Tiebreaker applied**: No.
Debate points won (scoring matrix in debate-transcript.md, for reference): V1 5 (C-001, C-002, C-004, C-005, X-002), V2 3 (C-006, X-001, A-006), V3 2 (C-003, C-007); points no card raised 5 (A-002, A-003, A-004, A-005, A-007); rejected 4 (S-001, S-002, A-001, A-008).

## Selected Base: Variant 1 (reviewer-1, sonnet:analyzer)

### Selection Rationale
V1 has the highest combined score and is the only variant with full Risk Coverage and full Invariant & Edge Case Coverage. It raised C-001, which every advocate ranked first in Round 2 (round2-v1.md:31, round2-v2.md:44, round2-v3.md:38). It is also the only card that checked the round-1 fixes (`round1_fix_check`). Its weaknesses are the over-graded A-1 (conceded to minor) and the bundled A-3; the merge corrects both.

### Strengths to Preserve from Base
1. A-1 as the lead finding, regraded minor and top priority, with the Round 2 fix (foreign URL whose repo and issue number cannot exist, an origin_repo.py URL check that Wave 0 calls, real-output evidence, plan:26 rewritten by target, else approval).
2. A-2 (Task 15 two exits), A-3/A-4/A-6 ClickUp hygiene, A-5 scan scoping.
3. `round1_fix_check: {F-01: fixed, F-02: fixed}`.

### Strengths to Incorporate from Non-Base Variants
1. V3 S-1 (C-003 winner): the section 14 table rows that Task 6 copies lack `--repo`; merged with V1 A-5.
2. V3 S-3 (C-007 winner), S-4 (into C-005), S-5, S-6 (into C-004), S-7, S-8, S-10 as minor; S-9 and S-12 as notes; S-11 dropped (withdrawn by V3).
3. V2 Q-4 (C-006 winner): the executor prompts only on its closed list, so "approval at that moment" needs an explicit ask step; Q-2 and Q-3 recorded as authorized expansions; Q-1 dropped as a duplicate of plan:25.
4. V2's X-001 verdict: PASS with notes.
5. Shared-assumption findings A-002..A-007 (no card raised them; minor).
