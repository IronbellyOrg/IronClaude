# Base Selection Report

Variants scored: Variant A = `variant-1-original.md` (proposal-a.md), Variant B = `variant-2-original.md` (proposal-b.md). The scored text is the ORIGINAL variant text, not the converged hybrid. Full per-criterion CEV (claim, evidence, verdict) for both passes is in `scorer-pass1.md` (order A then B) and `scorer-pass2.md` (order B then A) in this folder.

## Quantitative Scoring (50% weight)

Source requirements for RC: the C-02 row (clearing, blocking authority, verdict derivation, defer owner and expiry, counted-as-open, unanswered-means-open, invariant statements) plus the six required sections; no formal requirement IDs exist, so section-level topic matching was used. Computation by the orchestrator from the variant text (grep counts for vague indicators, section headings and internal references); claim counts for IC are estimates (about 55 scorable claims in A, about 65 in B).

| Metric | Weight | Variant A | Variant B | 
|--------|--------|-----------------------------------------|-----------|
| requirement_coverage | 0.30 | 1.000 (10 of 10 requirement topics matched) | 1.000 (10 of 10; B's optional expiry counted as matched) |
| internal_consistency | 0.25 | 1.000 (0 contradictions after pass-2 and re-evaluation, see Position-Bias section) | 0.985 (1 contradiction: B1 `prior open|regressed` sets any row vs B7 terminal deferred row; about 1 of 65 claims) |
| specificity_ratio | 0.15 | 1.000 (concrete 54 lines with digit or code token, vague indicators 0; supplementary line share 0.79) | 1.000 (concrete 78 lines, vague 0; supplementary line share 0.92) |
| dependency_completeness | 0.15 | 1.000 (internal section references 2, 3.1, 5 and 7 all resolve; "section N.M" mentions that cite research files are external and excluded) | 1.000 (sections 2, 2.1, 2.2, 3, 4, 5, 6 resolve; "research 13 7.2, section 8" is external) |
| section_coverage | 0.15 | 1.000 (7 H2 sections) | 1.000 (7 H2 sections) |
| **quant_score** | | **1.000** | **0.996** |

## Qualitative Scoring (50% weight) - Additive Binary Rubric

Rules applied by both scorers: CEV for every criterion; no evidence means NOT MET; a Correctness criterion is NOT MET where the debate (debate-transcript.md) established a factual or design error that bears on it. Debate-established defects used: A: `--resolution` claim overstated (counting is new code), "recorded completion state is complete" has no merge-path counterpart (only `block_ok`), dissent held at `resolved_check` is skipped by `apply_revision` (`ledger.py:328`), `expires_round` inert, Q above the one-reviewer re-review deadlocks. B: quote gate cannot clear a deletion fix (`document_review_loop_prompts.md:53`) and spans are lossy (`findings.py:431`), B6 category predicate misgrades `document_review_loop_prompts.md:31`, B1 vs B7 contradiction, B5 can yield REVISE with an empty brief, pin list omitted `test_prior_lines_never_change_a_status`.

Per-criterion verdicts (M = MET, N = NOT MET). Columns: pass 1 / pass 2 / final. Final equals the agreed verdict, or the re-evaluation verdict where the passes disagreed.

### Completeness (5 criteria)

| # | Criterion | A (p1/p2/final) | B (p1/p2/final) |
|---|-----------|-----------------|-----------------|
| 1 | Covers all explicit requirements | M/M/M | M/M/M |
| 2 | Edge cases and failure scenarios | M/M/M | M/M/M |
| 3 | Dependencies and prerequisites | M/M/M | M/M/M |
| 4 | Success or completion criteria | M/M/M | M/M/M |
| 5 | Explicit out of scope | M/M/M | M/M/M |
| **Subtotal** | | **5/5** | **5/5** |

### Correctness (5 criteria)

| # | Criterion | A (p1/p2/final) | B (p1/p2/final) | Key evidence |
|---|-----------|-----------------|-----------------|--------------|
| 1 | No factual errors or hallucinated claims | N/N/N | M/M/M | A section 1 and 2: "recorded completion state is `complete`" and "`--resolution` carries requested ids the guard counts" (`merge_cmd.py:73-83` builds only a model map); B's citations re-read by both advocates, no factual error established |
| 2 | Technical approaches feasible | N/N/N | N/N/N | A: dissent hold swallowed by `ledger.py:328`, quorum deadlock; B: quote gate on deletions, B6 predicate |
| 3 | Terminology consistent and accurate | N/N/N | M/M/M | A: "complete reviewer" names a state the merge path lacks |
| 4 | No internal contradictions | N/M/**M** | N/N/N | A re-evaluated (below); B: B1 vs B7 conceded in Round 2 |
| 5 | Claims supported by evidence | M/M/M | M/M/M | Both carry file:line tags |
| **Subtotal** | | **2/5** | **3/5** | |

### Structure (5 criteria)

| # | Criterion | A (p1/p2/final) | B (p1/p2/final) |
|---|-----------|-----------------|-----------------|
| 1 | Logical section ordering | M/M/M | M/M/M |
| 2 | Consistent hierarchy depth | M/M/M | M/M/M |
| 3 | Separation of concerns | M/M/M | M/M/M |
| 4 | Navigation aids | M/M/M | M/M/M |
| 5 | Artifact-type conventions | M/M/M | M/M/M |
| **Subtotal** | | **5/5** | **5/5** |

### Clarity (5 criteria)

| # | Criterion | A (p1/p2/final) | B (p1/p2/final) |
|---|-----------|-----------------|-----------------|
| 1 | Unambiguous language | M/M/M | N/M/**M** |
| 2 | Concrete rather than abstract | M/M/M | M/M/M |
| 3 | Section purpose clear | M/M/M | M/M/M |
| 4 | Terms defined on first use | N/N/N | N/N/N |
| 5 | Actionable next steps | M/M/M | M/M/M |
| **Subtotal** | | **4/5** | **4/5** |

### Risk Coverage (5 criteria)

| # | Criterion | A (p1/p2/final) | B (p1/p2/final) |
|---|-----------|-----------------|-----------------|
| 1 | At least 3 risks with probability and impact | N/N/N (severity only, no probability) | N/N/N (severity only) |
| 2 | Mitigation for each risk | N/N/N | N/N/N |
| 3 | Failure modes and recovery | M/M/M | M/M/M |
| 4 | External dependencies | M/M/M | M/M/M |
| 5 | Monitoring or validation | M/M/M | M/M/M |
| **Subtotal** | | **3/5** | **3/5** |

### Invariant & Edge Case Coverage (5 criteria)

| # | Criterion | A (p1/p2/final) | B (p1/p2/final) |
|---|-----------|-----------------|-----------------|
| 1 | Collection boundaries | M/M/M | M/M/M |
| 2 | State variable interactions across boundaries | M/M/M | M/M/M |
| 3 | Guard condition gaps | M/M/M | M/M/M |
| 4 | Count divergence | M/M/M | M/M/M |
| 5 | Interaction effects | M/M/M | M/M/M |
| **Subtotal** | | **5/5** | **5/5** |

### Qualitative Summary

| Dimension | Variant A | Variant B |
|-----------|-----------|-----------|
| Completeness | 5/5 | 5/5 |
| Correctness | 2/5 | 3/5 |
| Structure | 5/5 | 5/5 |
| Clarity | 4/5 | 4/5 |
| Risk Coverage | 3/5 | 3/5 |
| Invariant & Edge Case Coverage | 5/5 | 5/5 |
| **qual_score** | **24/30 = 0.800** | **25/30 = 0.833** |

### Edge Case Floor Check
- Variant A: Invariant & Edge Case Coverage 5/5 (floor is 1/5): eligible as base.
- Variant B: 5/5: eligible as base.
- Floor suspension not needed.

## Position-Bias Mitigation

Pass 1 evaluated A then B (`scorer-pass1.md`: A 23/30, B 24/30). Pass 2 evaluated B then A (`scorer-pass2.md`: B 25/30, A 24/30). Two criterion-variant pairs disagreed; each was re-evaluated by the orchestrator with both passes' evidence side by side, and the re-evaluation verdict is final.

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| Correctness 4 (no internal contradictions) | A | NOT MET | MET | DISAGREE | MET |
| Clarity 1 (unambiguous language) | B | NOT MET | MET | DISAGREE | MET |

Re-evaluation of A Correctness 4: Pass 1 cited `expires_round` return-to-open (section 2 `defer` row) against VM-6 plus "ESCALATE when every remaining row is deferred" (section 2 Verdict and Round order rows). The two statements are not contradictory: the expiry can fire whenever another blocking row keeps the loop in REVISE, and is inert only in the held-only state; that inertness is a feasibility defect already scored under Correctness 2 (NOT MET) and counting it again as a contradiction double-penalises. No other opposing claim exists inside A ("prior lines never a status writer" is consistent with a veto-only role). Final: MET.

Re-evaluation of B Clarity 1: Pass 1 cited three open points (B7 "An expiry may be recorded", B6 "optional per-lens stage that may overwrite", B3 "exact normalisation is module work"). A grep of both variants for the criterion's listed phrases ("should consider", "might", "as appropriate", "as needed", "properly", "adequate", "various", "etc.") finds none in either. Variant A carries equivalent declared open points (Q parameter, `review-ledger/2` unsettled) and was MET in both passes; consistency requires the same standard. Final: MET.

Disagreements re-evaluated: 2
Final verdicts changed: 2 (each from the pass that scored it NOT MET; no final verdict differs from at least one pass)

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate Tiebreaker |
|---------|---------------|--------------|-----------------|-------------------|
| A | 0.5000 | 0.4000 | **0.9000** | 5 points won |
| B | 0.4981 | 0.4167 | **0.9148** | 5 points won |

**Margin**: 1.48 percentage points (below the 5% threshold, tiebreaker applies)
**Tiebreaker applied**: Yes
- Level 1, debate performance: points won in the Step 2 scoring matrix: A 5 (C-002, C-004, X-001, X-002, X-004), B 5 (C-003, C-006, C-007, C-009, A-002 resolved), 6 hybrids, 1 tie, 4 qualified or independent, 1 unresolved. Tied, so not decisive.
- Level 2, correctness criteria count: B 3 of 5 MET, A 2 of 5 MET. B wins.
- The raw combined score also ranks B first (0.9148 against 0.9000).

## Selected Base: Variant B (explicit per-row verification; `proposal-b.md`)

### Selection Rationale
B is the base: it leads on combined score by 0.015, and, because that margin is inside the 5% band, the Level 2 tiebreaker (correctness count 3 against 2) also selects B. The correctness gap is the only dimension where the variants differ: A carries a terminology and factual error in its guard ("recorded completion state is `complete`", `--resolution` counting) and two feasibility defects (dissent hold swallowed at `ledger.py:328`, quorum above panel size deadlocks), B carries the B1/B7 contradiction and two feasibility defects (quote gate, B6 predicate). The debate itself converged on a hybrid that adopts more of B's mechanics (text-hash binding, dissent routed to `regressed`, terminal deferral, `refound_deferred`, drop of stored verdict keys, `verify_ids` and `held_ids`) and more of A's guard (quorum gate with the `block_ok` filter, record-only evidence key, CRITICAL floor with no predicate). The margin is narrow and the selection is by tiebreaker, so the merged result must be read as the hybrid the debate produced, not as B unmodified.

### Strengths to Preserve from Base (Variant B)
1. Text-hash binding at `revise` and `merge` (`pending_new_sha256`; B4).
2. Dissent routes a `resolved_check` row back to a status `apply_revision` accepts (B's `open|regressed` move, narrowed to `resolved_check` rows).
3. Terminal, counted-open `defer` with required owner and reason, no expiry in the core, `refound_deferred` surfaced.
4. Derived verdict with `brief_ids`, `verify_ids`, `held_ids`; stored round keys dropped (VM-3 wording, `synth-06-conflict-log.md:178`).
5. Fail-closed principle: the answer check gates, it does not warn; the M2 free pre-measurement and M3 flip-count measurement; the asymmetry argument.

### Strengths to Incorporate from Non-Base Variant (Variant A)
1. The quorum gate (`need = min(Q, requested)`, `block_ok` filter, same-round re-find wins, prior map built before the clearing loop) replacing B's quote-gated clearing: A section 2 Clearing rule and the debate's C-001 and X-003 outcome.
2. Record-only optional `evidence` key with `quote_in_doc` instead of a gate (C-002 outcome; keeps B's key, adopts A's no-gate position).
3. Typed `blocking` stays authority plus a CRITICAL floor in `merge_round` with `blocking_typed` kept and a flip warning; no category predicate (C-004, X-004).
4. Narrowed pin rule and docstring edit (C-005, X-001): a prior moves only a `resolved_check` row; test renamed.
5. `held` events with reason codes and `unverified_ids` in the merge output; the empty-brief REVISE handling (`next` field, report wording); A's D-11 A/B/C reproductions as the test list; A's three-arm replay as the measurement design.
6. Items the debate dropped from A: `expires_round` and reopen-on-refind (C-006, C-007), A's schema-snapshot form of C-009.
