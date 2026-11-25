# Base Selection Report (D10 wake transport)

Scoring caveat, stated first: the two variants are short position papers of equal shape, so the five quantitative metrics barely separate them, and the 30-criterion rubric scores each paper as a document, not each position as a design. The verdict of the debate (OURS, CLAY or HYBRID) is decided by the owner's weighting rule in the common brief, not by this score. The score only picks which paper is the base of the merged position document. All scoring here was done by the orchestrator in one session (two passes), not by independent agents. The quantitative values are estimates from reading the text, not a script count.

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant 1 (OURS) | Variant 2 (CLAY) |
|--------|--------|------------------|------------------|
| requirement_coverage | 0.30 | 1.00 (8/8 items of the topic question touched) | 1.00 (8/8; the launched-session candidate only by contrast, fact 8) |
| internal_consistency | 0.25 | 1.00 (0 self-contradictions; 3 externally wrong or stretched citations are scored under Correctness) | 1.00 (0 self-contradictions) |
| specificity_ratio | 0.15 | 0.96 (paths, lines, numbers throughout) | 0.96 |
| dependency_completeness | 0.15 | 1.00 (internal references resolve; external design lines excluded) | 1.00 |
| section_coverage | 0.15 | 1.00 (6 H2 sections) | 1.00 (6 H2 sections) |
| **quant_score** | | **0.994** | **0.994** |

## Qualitative Scoring (50% weight) - Additive Binary Rubric

Evidence is a section or fact of the variant (CEV protocol); "not met" means no evidence found.

### Completeness (5 criteria)
| Criterion | V1 | Evidence | V2 | Evidence |
|-----------|----|----------|----|----------|
| Covers all explicit requirements | MET | facts 1 to 8 cover 477, wake file, mailbox, typed line, copy, rule | MET | facts 1 to 8; launched session only in fact 8 |
| Edge cases and failures | MET | "What it risks" | MET | "What it risks" (race, mailbox) |
| Dependencies and prerequisites | MET | fact 6 (PR B does not exist) | MET | "Nothing reads the wake until PR B exists" |
| Success or completion criteria | NOT MET | none stated | NOT MET | none stated |
| Out of scope stated | MET | "no listener, no typed wake line..." in the claim | MET | "No listener is built" |
| **Subtotal** | **4/5** | | **4/5** | |

### Correctness (5 criteria)
| Criterion | V1 | Evidence | V2 | Evidence |
|-----------|----|----------|----|----------|
| No factual errors | NOT MET | fact 7 says PR 686 "adds" the parity tests that already exist on master | NOT MET | same parity error in "What it risks"; `orca_term.py` range drifts by 1 to 3 lines |
| Feasible approaches | MET | one Orca verb launch | MET | file, mailbox, typed line, ack |
| Terminology consistent | MET | | MET | |
| No internal contradictions | MET | | MET | |
| Claims supported by evidence | NOT MET | the Q36 citation supports approval latency, not claim latency; `orca_term.py:3` shown as a rule | MET | each fact cites a line; unverified items are labelled |
| **Subtotal** | **3/5** | | **4/5** | |

### Structure (5 criteria)
| Criterion | V1 | V2 |
|-----------|----|----|
| Logical ordering | MET | MET |
| Consistent depth | MET | MET |
| Separation of concerns | MET | MET |
| Navigation aids | NOT MET | NOT MET |
| Follows the position-paper convention of the brief (claim, mechanism, 5 to 10 cited facts, costs, risks, gets right) | MET (8 facts) | MET (8 facts) |
| **Subtotal** | **4/5** | **4/5** |

### Clarity (5 criteria)
| Criterion | V1 | V2 |
|-----------|----|----|
| Unambiguous language | MET | MET |
| Concrete rather than abstract | MET | MET |
| Each section has a clear purpose | MET | MET |
| Acronyms defined on first use | NOT MET (D3, Q3, K11, U5, FU-1 explained only by quotation) | NOT MET (K11, K14, K19, DQ10, U5) |
| Actionable next steps or decision points | NOT MET | NOT MET |
| **Subtotal** | **3/5** | **3/5** |

### Risk Coverage (5 criteria)
| Criterion | V1 | Evidence | V2 | Evidence |
|-----------|----|----------|----|----------|
| At least 3 risks with probability and impact | NOT MET | risks listed, not rated | NOT MET | risks listed, K-ids cited without a rating |
| Mitigation for each risk | NOT MET | none | NOT MET | mitigation for 2 of 5 |
| Failure modes and recovery | MET | pending record, operation-id retry | MET | ack, resend, unread mark |
| External dependencies and their failure | MET | Orca launch reply shapes assumed | MET | mailbox U5 with typed-line fallback |
| Monitoring or validation | NOT MET | only the live test | MET | ack observation, unread mark, exit 7 |
| **Subtotal** | **2/5** | | **3/5** | |

### Invariant and Edge Case Coverage (5 criteria)
| Criterion | V1 | Evidence | V2 | Evidence |
|-----------|----|----------|----|----------|
| Collection boundaries | NOT MET | none | MET | 64 KiB, item counts |
| State interactions across components | NOT MET (pass 2; pass 1 had MET) | the pending record is crash safety, not a cross-component interaction | MET | wake file owned by the poll, ack by the orchestrator |
| Guard condition gaps | MET | names the screen-read race in Clay's guard (fact 8) | MET | names the typing race |
| Count divergence | NOT MET | | NOT MET | attempt 1 to 3 never examined (INV-010) |
| Interaction effects | NOT MET | | MET | mailbox refused falls back to typed line alone |
| **Subtotal** | **1/5** | | **4/5** | |

### Qualitative Summary
| Dimension | V1 | V2 |
|-----------|----|----|
| Completeness | 4/5 | 4/5 |
| Correctness | 3/5 | 4/5 |
| Structure | 4/5 | 4/5 |
| Clarity | 3/5 | 3/5 |
| Risk Coverage | 2/5 | 3/5 |
| Invariant and Edge Case | 1/5 | 4/5 |
| **Total** | **17/30 = 0.567** | **22/30 = 0.733** |

### Edge Case Floor Check
V1 1/5 (meets the floor of 1/5, eligible); V2 4/5 (eligible).

## Position-Bias Mitigation
Pass 1 (input order OURS then CLAY) and pass 2 (reverse order, CLAY then OURS) were both run by the orchestrator. One disagreement: V1 "state interactions across components" was MET in pass 1 and NOT MET in pass 2. Re-evaluation with both pieces of evidence: the pending record protects one component against its own crash and is not an interaction across a boundary, so the final verdict is NOT MET. Disagreements found: 1; verdicts changed: 1 (pass 1 MET to final NOT MET). Not independent agents: the same evaluator ran both passes, so the mitigation is weaker than the protocol intends.

## Combined Scoring
| | V1 (OURS) | V2 (CLAY) |
|---|---|---|
| quant weighted (0.50) | 0.497 | 0.497 |
| qual weighted (0.50) | 0.283 | 0.367 |
| **final score** | **0.780** | **0.864** |

Margin 8.4 percent (above the 5 percent tiebreaker band). No tiebreaker applied.

## Selected Base: Variant 2 (CLAY paper)

**Selection rationale.** The CLAY paper scores higher because it states more failure modes, monitoring and boundary facts, and has fewer unsupported citations. This is a score of the paper as a document. It does not decide the debate verdict: the owner's weighting rule decides that, and the debate converged on a HYBRID (see `refactor-plan.md`).

**Strengths to preserve from the base.** Durable wake file as truth; acknowledgment with resend and unread mark; the id-only rule on every channel; separability from the trigger rules; honest cost and risk list.

**Strengths to incorporate from Variant 1 (OURS).**
1. Owner Q3 narrowing of Coder issue 477 and D1 option A / NG-1: the listener is out by the owner's own decisions (not only Clay's).
2. D3 integer-only prompt as the origin of the id-only rule, built and property-tested (`launch.py:33`, `:84-92`).
3. One fixed-pattern Orca verb for session start, with receipt and operation id, as the preferred start path if a live spike passes (C-004).
4. No copy of `orca_term.py`: one shared terminal helper with a parity test (C-005).
5. The "unproven live" honesty: both paths run behind a live-test gate (K11, U5, FU-1).
