# Base Selection Report

Slot C-08 (run-record-and-served-model-capture). Variant 1 = Proposal A (`variant-1-original.md`); Variant 2 = Proposal B (`variant-2-original.md`). Both variants were scored as written, not as the hybrid the debate produced. Scorers: Pass 1 (input order, also the deterministic quantitative layer) and Pass 2 (reverse order) ran as separate agents; a third agent re-evaluated the 8 disagreements. Detail: `score-pass1.md`, `score-pass2.md`, `score-reeval.md`, `quant-score.py`, `quant-score-output.json`.

## Quantitative Scoring (50% weight)

Computed by `quant-score.py` (stdlib only, deterministic, content sha256 `b9e9e6ce...`). There are no formal requirement IDs, so requirement coverage uses the protocol's topic-matching edge case over 30 topics drawn from the C-08 row and the decided requirements it names.

| Metric | Weight | Variant 1 (Proposal A) | Variant 2 (Proposal B) |
|--------|--------|------------------------|------------------------|
| requirement_coverage | 0.30 | 0.9667 (29 of 30 topics; misses "two labelled cost bases") | 0.9667 (29 of 30; misses OQ-19) |
| internal_consistency | 0.25 | 0.9487 (2 INTRA contradictions X-004, X-010 over 39 tagged claims) | 0.8718 (5 INTRA contradictions X-002, X-003, X-007, X-008, X-009 over 39 tagged claims) |
| specificity_ratio | 0.15 | 1.0000 (130 concrete, 0 vague) | 1.0000 (117 concrete, 0 vague) |
| dependency_completeness | 0.15 | 1.0000 (14 of 14 internal references resolve) | 1.0000 (16 of 16) |
| section_coverage | 0.15 | 0.8889 (8 H2 of max 9) | 1.0000 (9 H2) |
| **quant_score** | | **0.9605** | **0.9579** |

## Qualitative Scoring (50% weight) — Additive Binary Rubric

Final verdicts per criterion (after position-bias resolution). The Claim-Evidence-Verdict text for every criterion and both passes is in `score-pass1.md`, `score-pass2.md` and, for the 8 disputed pairs, `score-reeval.md`.

### Completeness (5 criteria)

| Criterion | Variant 1 | Variant 2 |
|-----------|-----------|-----------|
| 1. Covers all explicit requirements from source input | NOT MET | NOT MET |
| 2. Addresses edge cases and failure scenarios | MET | MET |
| 3. Includes dependencies and prerequisites | MET | MET |
| 4. Defines success/completion criteria | MET | MET |
| 5. Specifies what is explicitly out of scope | MET | MET |
| **Subtotal** | **4/5** | **4/5** |

### Correctness (5 criteria)

| Criterion | Variant 1 | Variant 2 |
|-----------|-----------|-----------|
| 1. No factual errors or hallucinated claims | NOT MET | NOT MET |
| 2. Technical approaches are feasible with stated constraints | NOT MET | NOT MET |
| 3. Terminology used consistently and accurately throughout | MET | NOT MET |
| 4. No internal contradictions (cross-validated with IC) | NOT MET | NOT MET |
| 5. Claims supported by evidence or rationale within the document | MET | MET |
| **Subtotal** | **2/5** | **1/5** |

### Structure (5 criteria)

| Criterion | Variant 1 | Variant 2 |
|-----------|-----------|-----------|
| 1. Logical section ordering (prerequisites before dependents) | MET | MET |
| 2. Consistent hierarchy depth (no orphaned subsections) | MET | MET |
| 3. Clear separation of concerns between sections | MET | MET |
| 4. Navigation aids present | MET | MET |
| 5. Follows conventions of the artifact type | MET | MET |
| **Subtotal** | **5/5** | **5/5** |

### Clarity (5 criteria)

| Criterion | Variant 1 | Variant 2 |
|-----------|-----------|-----------|
| 1. Unambiguous language | MET | MET |
| 2. Concrete rather than abstract | MET | MET |
| 3. Each section has a clear purpose | MET | MET |
| 4. Acronyms and domain terms defined on first use | NOT MET | MET |
| 5. Actionable next steps or decision points identified | MET | MET |
| **Subtotal** | **4/5** | **5/5** |

### Risk Coverage (5 criteria)

| Criterion | Variant 1 | Variant 2 |
|-----------|-----------|-----------|
| 1. Identifies at least 3 risks with probability and impact | MET | MET |
| 2. Provides mitigation strategy for each identified risk | MET | MET |
| 3. Addresses failure modes and recovery procedures | MET | MET |
| 4. Considers external dependencies and their failure scenarios | MET | MET |
| 5. Includes monitoring or validation mechanism for risk detection | MET | MET |
| **Subtotal** | **5/5** | **5/5** |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | Variant 1 | Variant 2 |
|-----------|-----------|-----------|
| 1. Boundary conditions for collections (empty, single, maximum) | MET | MET |
| 2. State variable interactions across component boundaries | MET | MET |
| 3. Guard condition gaps (missing validation, unguarded assumptions) | MET | MET |
| 4. Count divergence scenarios (off-by-one, inclusive/exclusive) | MET | MET |
| 5. Interaction effects when features or components combine | MET | MET |
| **Subtotal** | **5/5** | **5/5** |

### Qualitative Summary

| Dimension | Variant 1 | Variant 2 |
|-----------|-----------|-----------|
| Completeness | 4/5 | 4/5 |
| Correctness | 2/5 | 1/5 |
| Structure | 5/5 | 5/5 |
| Clarity | 4/5 | 5/5 |
| Risk Coverage | 5/5 | 5/5 |
| Invariant & Edge Case Coverage | 5/5 | 5/5 |
| **qual_score** | **25/30 = 0.8333** | **25/30 = 0.8333** |

Correctness is the one dimension where the variants differ (V1 2/5, V2 1/5), and both scorers agreed on every Correctness verdict. Variant 1 is MET on criteria 3 and 5 and NOT MET on 1, 2 and 4; Variant 2 is MET on criterion 5 only. The debate verified defects of both papers against the code: Variant 1's claim that refusal rows close C-03 INV-001 has no writer in its own module table (X-004), it names no location for the loop's events (X-010) and lists `cycle.py` as a lock user on a docstring hit (X-012); Variant 2's `agents[]` on `published`/`failed` has no code path (X-002), its producer is placed after the call that raises (X-003), its append-time type check has no mechanism in `load` (X-007) and its Tier 2 `reviewer_run` producer names no component (X-008). The per-criterion evidence is in `score-pass1.md` and `score-pass2.md`. Completeness criterion 1 is NOT MET for Variant 2 because OQ-19 (the reviewer-model header line, `spec-panel.md:258`) is answered nowhere in it (re-evaluation, disagreement 4); Variant 1 is NOT MET on the same criterion for the missing second labelled cost basis.

### Edge Case Floor Check

| Variant | Invariant & Edge Case score | Eligible as base (>= 1/5) |
|---------|-----------------------------|---------------------------|
| Variant 1 (Proposal A) | 5/5 | Eligible |
| Variant 2 (Proposal B) | 5/5 | Eligible |

## Position-Bias Mitigation

Pass 1 evaluated Variant 1 then Variant 2; Pass 2 evaluated Variant 2 then Variant 1, independently (Pass 2 did not read Pass 1). 60 criterion-variant pairs; 52 agreed; 8 disagreed and were re-evaluated with an explicit comparison prompt (`score-reeval.md`); the re-evaluation verdict is final.

Pass-level subtotals before resolution: Pass 1 V1 23/30, V2 22/30; Pass 2 V1 25/30, V2 24/30.

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| Completeness 1: Covers all explicit requirements from source input | V2 | NOT MET | MET | DISAGREE | NOT MET |
| Structure 1: Logical section ordering (prerequisites before dependents) | V2 | MET | NOT MET | DISAGREE | MET |
| Clarity 4: Acronyms and domain terms defined on first use | V2 | NOT MET | MET | DISAGREE | MET |
| Risk Coverage 1: Identifies at least 3 risks with probability and impact | V1 | NOT MET | MET | DISAGREE | MET |
| Risk Coverage 1: Identifies at least 3 risks with probability and impact | V2 | NOT MET | MET | DISAGREE | MET |
| Risk Coverage 2: Provides mitigation strategy for each identified risk | V2 | MET | NOT MET | DISAGREE | MET |
| Invariant & Edge Case Coverage 1: Boundary conditions for collections (empty, single, maximum) | V1 | NOT MET | MET | DISAGREE | MET |
| Invariant & Edge Case Coverage 1: Boundary conditions for collections (empty, single, maximum) | V2 | NOT MET | MET | DISAGREE | MET |

The 52 agreed pairs are listed in the VERDICTS blocks of `score-pass1.md` and `score-pass2.md`.

Disagreements re-evaluated: 8
Final verdicts changed from Pass 1: 5 (V1 invariant_edge_case 1, V1 risk_coverage 1, V2 clarity 4, V2 invariant_edge_case 1, V2 risk_coverage 1)
Final verdicts changed from Pass 2: 3 (V2 completeness 1, V2 risk_coverage 2, V2 structure 1)

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate Tiebreaker |
|---------|---------------|--------------|-----------------|-------------------|
| 1 (Proposal A) | 0.4803 | 0.4167 | **0.8969** | 8 points won (Step 2 scoring matrix) |
| 2 (Proposal B) | 0.4789 | 0.4167 | **0.8956** | 4 points won |

**Margin**: 0.0013 (0.13% , below the 5% threshold)
**Tiebreaker applied**: Yes, level 1 (debate performance). Points won in the Step 2 scoring matrix over the 31 diff points: Variant 1 won 8 (S-002, C-002, C-007, X-002, X-008, X-009, A-004, A-007), Variant 2 won 4 (C-005, X-001, X-007, X-011); 13 points went to the hybrid (C-001, C-003, C-004, C-006, C-008, X-003, X-004, X-006, X-010, A-003, A-005, A-006, A-008), 5 to neither (S-001, X-005, X-012, A-001, A-002) and 1 is unresolved (A-009). Variant 1 leads 8 to 4 (66.7% against 33.3% of decided points), which is not within 5%, so level 1 decides. Level 2 (correctness criteria MET: Variant 1 has 2, Variant 2 has 1) points the same way and was not needed.
**Evidence**: the quantitative layer is a near tie (0.9605 against 0.9579, Variant 1 ahead by IC 0.9487 against 0.8718; Variant 2 ahead on section coverage); the qualitative layer is an exact tie at 25/30; Variant 1 has the higher correctness count.

## Selected Base: Variant 1 (Proposal A; default model, default persona)

### Selection Rationale

The combined scores are 0.8969 (Variant 1) and 0.8956 (Variant 2), a margin of 0.13%, below the 5% threshold, so the tiebreaker protocol applied. Level 1 (debate performance) selects Variant 1: it won 8 diff points to Variant 2's 4. The two debate advocates reached the same ordering in substance: both named Proposal A's per-run events file as the right observation store (Advocate B: "A is the right base for the observation store, the refusal rows and the loop path") while Proposal B contributes the telemetry `strict` keyword, the fence analysis, the in-process merge writer restricted by cause, the A3 identity-gate replay and the shadow fallback text. After Round 2 the advocates agreed on 28 of 31 points (90.3%); the three non-agreed points are C-001 and X-006 (label splits with converged substance) and A-009 (the telemetry-append lock). Convergence is blocked by the invariant probe: 13 HIGH-severity UNADDRESSED invariants (see `invariant-probe.md`).

### Strengths to Preserve from Base (Variant 1)

1. One append-only per-run `events.jsonl` for per-agent observation, refused actions and the orchestrator, written only by code; the manifest stays a pure stage state machine (no `usage`, `model` or `agents[]` added). A committed manifest takes no second write (`manifest.py:293-296`, `manifest_cmd.py:204`), so a manifest carrier cannot hold the orchestrator tail or a killed run.
2. The null rule: where the adapter cannot read a value the field is null and `identity_source` stays `requested-pinned`; nothing is estimated.
3. The self-falsifying measurements: M1 adapter replay, M2 real-process concurrency test with an unlocked control, M3 cost-basis check that would remove the cost reason, and the list of existing tests that must pass unmodified.
4. Contract 1.8.0, `derive_verdict` and the verdict matrix untouched; events are write-only observation (INV-L).
5. The loop path through the same format and an idempotent `ingest` with no ordering precondition on the orchestrator.

### Strengths to Incorporate from Non-Base Variant (Variant 2) and from the debate's Round 2 hybrid

1. `validate_record(strict=...)` at append on the two call sites (`telemetry.py:289, 411`) in place of `review-telemetry/2` (X-007; B Round 2 corrected the label rule so tier aliases and fixtures validate).
2. The SKILL edit-fence analysis: no memory writer move (C-005, X-011); edits only inside `### 4.3a`; one deliberate edit to the assertion at `test_shadow_skill_contract.py:228`.
3. A code-owned writer in `review merge` for refusals, action rows only, reason from a `LedgerError.reason` attribute, never cost rows (X-003, X-004; A's local derivation hits `UnboundLocalError` when `led.load` raises).
4. The identity gate in `scripts/reflect_shadow_exit.py`, read-only, with an A3 replay as the acceptance test; the shadow fallback text (`panel_fallback_reason`); a committed synthetic transcript fixture for unit tests.
5. A blocking, timed, lazily imported lock helper at CLI level for the manifest (`manifest_cmd.py`) and the events file; `rev` deferred behind M2.
6. One producer `review record export` with deterministic record ids, a required telemetry directory and a visible `record_absent`.

