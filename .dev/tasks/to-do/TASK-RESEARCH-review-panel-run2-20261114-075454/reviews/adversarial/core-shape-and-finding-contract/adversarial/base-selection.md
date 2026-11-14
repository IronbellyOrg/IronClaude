# Base Selection Report

Variants: Variant A = `variant-1-original.md` (Proposal A, one core schema and engine, findings-v2 superset, v1 loop as `spec-loop` profile); Variant B = `variant-2-original.md` (Proposal B, thin shared contract, per-module engines, convergence on a trigger). Both were scored as written. The full Claim-Evidence-Verdict text for every criterion is in `scorer-pass1.md` (input order A, B) and `scorer-pass2.md` (reverse order B, A), written by two independent scorer agents that did not see each other's output.

## Quantitative Scoring (50% weight)

Computed by a script (stdlib regex over the two variant files, no LLM judgment), except where the table says "orchestrator count".

| Metric | Weight | Variant A | Variant B |
|--------|--------|-----------|-----------|
| requirement_coverage (8 source requirements: C-S1, CO-1, CO-2, CO-3, CO-4, CL-X11, FX-1, FX-2; matched by ID or keyword in the body) | 0.30 | 1.000 (8 of 8; by ID alone 7 of 8) | 1.000 (8 of 8; by ID alone 3 of 8) |
| internal_consistency (1 - contradictions / tagged claims) | 0.25 | 0.941 (2 contradictions, orchestrator count, over 34 tagged claims) | 0.949 (2 contradictions, orchestrator count, over 39 tagged claims) |
| specificity_ratio (concrete lines / (concrete + vague)) | 0.15 | 1.000 (74 concrete, 0 vague) | 1.000 (69 concrete, 0 vague) |
| dependency_completeness (resolved internal references / all) | 0.15 | 1.000 (67 of 67) | 0.884 (38 of 43) |
| section_coverage (H2 sections / max) | 0.15 | 1.000 (9 of 9) | 0.778 (7 of 9) |
| **quant_score** | | **0.985** | **0.936** |

Notes: the two orchestrator-counted internal contradictions per variant are (A) a clustering plan (`cluster_v2` for new ledgers) that conflicts with the anchor-required `spec-loop` profile and with T2's expectation of an equal ledger, (B) the guarded input described both as reached from `merge_round` (E-3, 2.3) and as an input that "cannot occur today in the shipped flow" (INV-D), plus the projection view against B's own build-only-for-a-consumer rule. The specificity metric does not separate the variants (both 1.000). The metric set rewards section count and ID matches, which favour the longer Variant A; the margin below is small for that reason.

## Qualitative Scoring (50% weight) - Additive Binary Rubric

Per-criterion final verdicts (A / B). "P1" and "P2" are the two passes; "agree" means both passes gave the same verdict; "re-eval" means the passes disagreed and the orchestrator's re-evaluation (see Position-Bias Mitigation) is final. Full CEV evidence is in the two scorer files.

### Completeness (5 criteria)

| Criterion | Variant A | Variant B | Basis |
|-----------|-----------|-----------|-------|
| 1 Covers all explicit requirements | MET | NOT MET | agree. B gives no answer to FX-2 (exact-substring anchors) and no CL-X11 placement decision (scorer-pass1 Completeness 1; scorer-pass2 Completeness 1; B advocate conceded the FX-2 gap in Round 1) |
| 2 Edge cases and failure scenarios | MET | MET | agree |
| 3 Dependencies and prerequisites | MET | MET | agree |
| 4 Success or completion criteria | MET | MET | agree |
| 5 Out-of-scope items | MET | MET | agree |
| **Subtotal** | **5/5** | **4/5** | |

### Correctness (5 criteria)

| Criterion | Variant A | Variant B | Basis |
|-----------|-----------|-----------|-------|
| 1 No factual errors or hallucinated claims | NOT MET | NOT MET | agree. Both rest on a `KeyError` reached through `merge_round`; `findings.py:104` rejects a line with no anchor before `ledger.py:135-136` calls `annotate` (re-read by the orchestrator, both advocates and both scorers) |
| 2 Technical approaches feasible with stated constraints | NOT MET | MET | agree. A's `cluster_v2` for new ledgers cannot cluster anchor-only findings (`cluster.py:128-181`, `test_review_cluster.py:279-293`) |
| 3 Terminology consistent and accurate | NOT MET | MET | re-eval (P1 NOT MET for A, P2 MET for A). "findings-v2 as the superset" is inaccurate by A's own E7 and E9 (v2 rejects `calibrated_confidence` and `prior` lines that v1 accepts) and by `findings_v2.py:109-110`; A's advocate conceded this in Round 2 |
| 4 No internal contradictions | NOT MET | NOT MET | agree (different reasons, see Quantitative notes) |
| 5 Claims supported by evidence or rationale | MET | MET | agree |
| **Subtotal** | **1/5** | **3/5** | |

### Structure (5 criteria)

| Criterion | Variant A | Variant B | Basis |
|-----------|-----------|-----------|-------|
| 1 Logical section ordering | MET | MET | agree |
| 2 Consistent hierarchy depth | MET | MET | agree |
| 3 Clear separation of concerns | MET | MET | agree |
| 4 Navigation aids | MET | MET | agree |
| 5 Follows artifact-type conventions | MET | MET | agree |
| **Subtotal** | **5/5** | **5/5** | |

### Clarity (5 criteria)

| Criterion | Variant A | Variant B | Basis |
|-----------|-----------|-----------|-------|
| 1 Unambiguous language | NOT MET | NOT MET | re-eval for both (P1 NOT MET, P2 MET for each). A's T3 uses "materially worse" and "reliably enough" with no number; B's 5.1 fail rule uses "a small fixed number of engine-specific fields" and 5.4 says "The numbers are a proposal for the debate, not findings" |
| 2 Concrete rather than abstract | MET | MET | agree |
| 3 Each section has a clear purpose | MET | MET | agree |
| 4 Acronyms and terms defined on first use | NOT MET | NOT MET | agree (INV-A.., C-06, D-1.., M-items undefined in both) |
| 5 Actionable next steps or decision points | MET | MET | agree |
| **Subtotal** | **3/5** | **3/5** | |

### Risk Coverage (5 criteria)

| Criterion | Variant A | Variant B | Basis |
|-----------|-----------|-----------|-------|
| 1 At least 3 risks with probability and impact | NOT MET | NOT MET | agree (impact levels only, no probability) |
| 2 Mitigation for each identified risk | MET | NOT MET | agree. B's INV-I item ("B does not improve it") and engine-count cost have no control |
| 3 Failure modes and recovery | MET | MET | agree |
| 4 External dependencies and failure scenarios | MET | MET | agree |
| 5 Monitoring or validation mechanism | MET | MET | agree |
| **Subtotal** | **4/5** | **3/5** | |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | Variant A | Variant B | Basis |
|-----------|-----------|-----------|-------|
| 1 Collection boundaries (empty, single, maximum) | MET | MET | re-eval for A (P1 MET, P2 NOT MET); B agree. A: INV-I zero valid blocks (`ledger.py:150-157`), the single-valid-block pass, FX-1 over-limit lines |
| 2 State variable interactions across components | MET | MET | agree |
| 3 Guard condition gaps | MET | MET | re-eval for B (P1 MET, P2 NOT MET); A agree. B names more than its 2.3 guard: E-8 "no chain guard" in v1 union-find, E-10 clearing by silence and one valid block of N passing |
| 4 Count divergence | MET | MET | agree |
| 5 Interaction effects | MET | MET | agree |
| **Subtotal** | **5/5** | **5/5** | |

### Qualitative Summary

| Dimension | Variant A | Variant B |
|-----------|-----------|-----------|
| Completeness | 5/5 | 4/5 |
| Correctness | 1/5 | 3/5 |
| Structure | 5/5 | 5/5 |
| Clarity | 3/5 | 3/5 |
| Risk Coverage | 4/5 | 3/5 |
| Invariant & Edge Case Coverage | 5/5 | 5/5 |
| **qual_score** | **23/30 = 0.767** | **23/30 = 0.767** |

### Edge Case Floor Check

Both variants score 5/5 on Invariant & Edge Case Coverage (floor: at least 1/5). Both eligible as base; the floor is not suspended.

## Position-Bias Mitigation

Pass 1 (input order A, B): A 23/30, B 23/30. Pass 2 (reverse order B, A): A 24/30, B 23/30. 60 criterion-variant pairs were compared (30 criteria x 2 variants); 5 pairs disagreed.

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| Correctness 3 (terminology) | A | NOT MET | MET | DISAGREE | NOT MET |
| Clarity 1 (unambiguous language) | A | NOT MET | MET | DISAGREE | NOT MET |
| Clarity 1 (unambiguous language) | B | NOT MET | MET | DISAGREE | NOT MET |
| Invariant 1 (collection boundaries) | A | MET | NOT MET | DISAGREE | MET |
| Invariant 3 (guard condition gaps) | B | MET | NOT MET | DISAGREE | MET |

Disagreements re-evaluated: 5 (by the orchestrator against the cited evidence of both passes, with the CEV rule that a MET needs a specific citation). Final verdicts changed from Pass 1: 0; from Pass 2: 5. The re-evaluation reasons are in the Basis column above. Because all five re-evaluations landed on the Pass 1 verdict, a sensitivity check was run with the opposite resolution (every disagreement resolved to the Pass 2 verdict): A would be 24/30 and B 23/30 (the Clarity 1 pair and Correctness 3 move A and B up, Invariant 1 moves A down, Invariant 3 moves B down). The base selection below is unchanged under that check (see Combined Scoring).

Note on the re-evaluation: the orchestrator performed it directly rather than dispatching a third agent; it used only evidence already cited in the two scorer files and the debate transcript.

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate Tiebreaker |
|---------|---------------|--------------|-----------------|-------------------|
| A (opus:architect+qa, `variant-1-original.md`) | 0.4926 | 0.3833 | **0.8760** | 2 of 23 points won (8.7%) |
| B (opus:architect+qa, `variant-2-original.md`) | 0.4682 | 0.3833 | **0.8515** | 10 of 23 points won (43.5%) |

Sensitivity (all disagreements resolved to Pass 2): A 0.8926 (quant 0.4926 + qual 0.4000), B 0.8515; margin 4.1 percent, still below 5 percent.

**Margin**: 2.45 percent (below the 5 percent threshold)
**Tiebreaker applied**: Yes, level 1 (debate performance, points won in Step 2). Of the 23 points: Variant B 10 (S-002, C-001, C-002, C-003, C-004, C-007, X-001, X-002, X-003, A-003), Variant A 2 (S-001, S-004), HYBRID 7, NEITHER 4. B wins by 8 points; the gap is not within 5 percent, so levels 2 and 3 are not reached. For reference, level 2 (correctness criteria met) would also favour B (3 versus 1).

## Selected Base: Variant B (opus:architect+qa, `variant-2-original.md`)

### Selection Rationale

The two variants tie on the qualitative layer (23 of 30 each) and Variant A leads the quantitative layer by 0.049, mostly through section count and internal-reference completeness (section_coverage 1.000 versus 0.778, dependency_completeness 1.000 versus 0.884). The combined margin is 2.45 percent, below the 5 percent tiebreaker threshold, so the protocol's level-1 tiebreaker (debate performance) decides: Variant B won 10 of the 23 debated points, Variant A won 2, and 11 ended as HYBRID (7) or NEITHER (4). The debate itself moved toward B's shape: the Variant A advocate withdrew locator-agnostic `annotate`, `citations` in ledger rows, the clustering marker, the typed re-review line kind and `cluster_v2` for new ledgers, after both advocates verified in code that a citation-only line is rejected by `findings.py:104` before it can reach `annotate`, and that `cluster_v2` cannot cluster anchor-only findings (`cluster.py:128-181`, `test_review_cluster.py:279-293`). Variant A's Correctness score (1 of 5) reflects those two points. Variant B's lower Completeness (no FX-2 answer, no CL-X11 placement) and Risk Coverage (no control for the engine-count cost) are carried into the refactoring plan as items to take from Variant A.

### Strengths to Preserve from Base (Variant B)

1. Thin shared contract with per-module engines: id grammar `_ID`, one limits-constants module, one repair step, the shared `refs_norm` token list with `T<PP>.<TT>`, hash and identity helpers (B 2.1).
2. Defect-locality table showing which defects are shared helpers and which are engine-local (B 3.2).
3. Pre-registered location-reliability decision rule (B 5.3) and the named convergence trigger (B 5.4, with item 2 replaced by A's T-c).
4. Conformance golden set of about 20 lines (B 5.1).
5. Git-history evidence that duplicate cost is a projection (B E-5) and the module-by-module engine table (B 2.2).

### Strengths to Incorporate from Non-Base Variants

1. From Variant A, E11 and T5: the verified stuck-row defect (a row with `span None` never reaches `resolved_check`); take it as a surfacing change in `render_merged_report` (per-row `### Lx` block, not the reviser-brief id line) with no configuration knobs, clearing routed to C-02 (agreed by both advocates in Round 2; B's Round 2 table records DISAGREE on A's `on_missing`/`on_ambiguous` knobs).
2. From Variant A, T1 and T2: the pin-parity gate and the differential replay over committed fixtures, with `test_review_cluster.py:279-293` and `test_rendered_merged_report` added to the named pins.
3. From Variant A, section 4: the per-row answer table for C-S1, CO-1, CO-2, CO-3, CO-4, CL-X11, FX-1, FX-2 (fills B's missing FX-2 and CL-X11 answers) and section 9, open points.
4. From Variant A, the observation that the clustering section resolver and the ledger passthrough keys are deferred until a consumer needs them (recorded as deferred with the trigger, not built now).
5. From Variant A, the convergence precondition: before any loop moves to the v2 kernel, give `same_defect_v2` an anchor-span branch or derive a `spec`-role citation from the located span (A Round 2).
