# Base Selection Report

Slot X-13 (process-redesign-modules). Variant A = Proposal A (`variant-1-original.md`, Sweep-Sheet-shaped). Variant B = Proposal B (`variant-2-original.md`, Recipe-Ledger-shaped). The variants are scored as written, not the hybrid the advocates later converged on. Detailed evidence: `score-pass1.md` (forward order, with the quantitative layer), `score-pass2.md` (reverse order), `score-reeval.md` (re-evaluation of the 7 disagreements), `quant-score.py` and `quant-score-output.json` (deterministic; run with `uv run python quant-score.py`).

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant A (Proposal A) | Variant B (Proposal B) |
|--------|--------|------------------------|------------------------|
| requirement_coverage | 0.30 | 1.0000 (12 of 12 source requirements matched by keyword groups) | 1.0000 (12 of 12) |
| internal_consistency | 0.25 | 0.8148 (5 debate-verified contradictions / 27 scorable claims) | 0.8065 (6 / 31) |
| specificity_ratio | 0.15 | 1.0000 (72 concrete lines, 0 vague indicator hits) | 1.0000 (65 concrete lines, 0 vague hits) |
| dependency_completeness | 0.15 | 1.0000 (7 of 7 internal references resolve) | 1.0000 (23 of 23) |
| section_coverage | 0.15 | 0.8889 (8 H2 / max 9) | 1.0000 (9 H2 / max 9) |
| **quant_score** | | **0.9370** | **0.9516** |

The scorer's deviations from the generic definitions (stated in `quant-score.py` header): the 12 source requirements are the slot's own design questions (core shape, advisory vs demotion/promotion, read-only recipes, CB-2, slot keys, gates, core and modules, invariants, measurement, consistency with C-01..C-03, PR review and rf-qa, objection and answer); IC counts only contradictions the debate verified against code or text (each is listed with its evidence in `quant-score-output.json`); the same script run twice gives identical JSON.

## Qualitative Scoring (50% weight) — Additive Binary Rubric

Final verdicts per criterion after the two passes and the re-evaluation (full CEV text for every criterion is in `score-pass1.md`, `score-pass2.md` and, for the 7 disputed pairs, `score-reeval.md`).

| Dimension / criterion | Variant A | Variant B |
|-----------------------|-----------|-----------|
| **Completeness** 1 covers all explicit requirements | MET | MET |
| 2 edge cases and failure scenarios | MET | MET |
| 3 dependencies and prerequisites | MET | MET |
| 4 success and completion criteria | MET | MET |
| 5 out-of-scope items | MET | MET |
| **Subtotal** | **5/5** | **5/5** |
| **Correctness** 1 no factual errors or hallucinated claims | NOT MET | NOT MET |
| 2 technical approaches feasible with stated constraints | NOT MET | NOT MET |
| 3 terminology consistent and accurate | MET | NOT MET (re-eval: "reviewer id" used for two id spaces, conceded and re-verified) |
| 4 no internal contradictions | MET (re-eval: A's verified errors are against code, not between two A statements, already counted in 1, 2 and 5) | NOT MET |
| 5 claims supported by evidence | NOT MET | NOT MET |
| **Subtotal** | **2/5** | **0/5** |
| **Structure** 1 logical section ordering | MET | MET |
| 2 consistent hierarchy depth | MET | MET |
| 3 separation of concerns | NOT MET | MET |
| 4 navigation aids | MET | MET |
| 5 follows conventions of the artifact type | MET | MET |
| **Subtotal** | **4/5** | **5/5** |
| **Clarity** 1 unambiguous language | MET | MET |
| 2 concrete rather than abstract | MET | MET |
| 3 each section has a clear purpose | MET | MET |
| 4 acronyms and terms defined on first use | NOT MET (re-eval: G0, D1-D7, E1/E2/E5/E7 never defined in A) | NOT MET (re-eval: G0, D1-D7, E1-E7, X-14, H1-H4 never defined in B) |
| 5 actionable next steps | MET | MET |
| **Subtotal** | **4/5** | **4/5** |
| **Risk Coverage** 1 at least 3 risks with probability and impact | MET | MET |
| 2 mitigation for each identified risk | NOT MET (re-eval: the false-positive risk has only a measurement) | NOT MET (re-eval: v1 weaker check and `ran` accepted or deferred) |
| 3 failure modes and recovery | MET | MET |
| 4 external dependencies | MET | MET |
| 5 monitoring or validation mechanism | MET | MET |
| **Subtotal** | **4/5** | **4/5** |
| **Invariant & Edge Case** 1 collection boundaries | MET | MET |
| 2 state variable interactions across boundaries | MET | MET |
| 3 guard condition gaps | MET | MET |
| 4 count divergence scenarios | MET (re-eval: A:33 and A:98 give the same class of evidence both passes accepted for B) | MET |
| 5 interaction effects | MET | MET |
| **Subtotal** | **5/5** | **5/5** |

### Qualitative Summary

| Dimension | Variant A | Variant B |
|-----------|-----------|-----------|
| Completeness | 5/5 | 5/5 |
| Correctness | 2/5 | 0/5 |
| Structure | 4/5 | 5/5 |
| Clarity | 4/5 | 4/5 |
| Risk Coverage | 4/5 | 4/5 |
| Invariant & Edge Case | 5/5 | 5/5 |
| **qual_score** | **24/30 = 0.8000** | **23/30 = 0.7667** |

### Edge Case Floor Check
Invariant & Edge Case Coverage: Variant A 5/5, Variant B 5/5. Both meet the floor (>= 1/5); both are eligible as base.

## Position-Bias Mitigation

Pass 1 evaluated A then B (totals A 23, B 23). Pass 2 evaluated B then A (totals A 25, B 26). They disagreed on 7 of 60 criterion-variant pairs; each was re-evaluated with an explicit comparison and the re-evaluation verdict is final.

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| Correctness 3 (terminology) | B | NOT MET | MET | DISAGREE | NOT MET |
| Correctness 4 (no contradictions) | A | NOT MET | MET | DISAGREE | MET |
| Clarity 4 (terms defined) | A | NOT MET | MET | DISAGREE | NOT MET |
| Clarity 4 (terms defined) | B | NOT MET | MET | DISAGREE | NOT MET |
| Risk Coverage 2 (mitigation for each risk) | A | NOT MET | MET | DISAGREE | NOT MET |
| Risk Coverage 2 (mitigation for each risk) | B | NOT MET | MET | DISAGREE | NOT MET |
| Invariant & Edge Case 4 (count divergence) | A | MET | NOT MET | DISAGREE | MET |

Disagreements re-evaluated: 7 of 60. Final verdicts that differ from Pass 1: 1 (Correctness 4, A). Final verdicts that differ from Pass 2: 6. The other 53 pairs were agreed.

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate Tiebreaker |
|---------|---------------|--------------|-----------------|-------------------|
| A (Proposal A) | 0.4685 | 0.4000 | **0.8685** | 5 points won of 29 (17.2%); Correctness 2/5 |
| B (Proposal B) | 0.4758 | 0.3833 | **0.8591** | 4 points won of 29 (13.8%); Correctness 0/5 |

**Margin**: 0.94 percentage points (0.8685 vs 0.8591), below the 5% threshold.
**Tiebreaker applied**: Yes.
- Level 1, debate performance (points won in Step 2 scoring matrix): Variant A 5 (C-010, X-002, X-003, X-006, X-008), Variant B 4 (S-002, S-003, C-004, C-012). 13 points went to the hybrid the advocates built, 6 to "Neither", 1 (S-004) is unresolved. The difference of 3.4 percentage points of the 29 points is within 5%, so Level 2 was also applied.
- Level 2, correctness criteria count: Variant A 2, Variant B 0. Variant A wins.
- Both levels point to Variant A; Level 3 (input order, A first) would also select A.
The layers disagreed: the quantitative layer favoured B (0.9516 vs 0.9370, driven by section coverage, 9 vs 8 H2 sections; internal consistency was marginally higher for A, 0.8148 vs 0.8065, and requirement coverage, specificity and dependency completeness were equal), the qualitative layer favoured A (24 vs 23, driven by Correctness 2/5 vs 0/5, partly offset by Structure 4/5 vs 5/5).

## Selected Base: Variant A (Proposal A, Sweep-Sheet-shaped; `variant-1-original.md`)

### Selection Rationale
Variant A is selected by the tiebreaker, not by a clear score margin (margin 0.94%). It leads on the qualitative Correctness dimension, where the debate verified fewer wrong statements about code in A than in B (B's own advocate conceded no brief renderer exists in `cli/review`, the `ledger.py:468` route lists the wrong set, the `recipes` name collides with `cli/swarm/recipes/`, and the sidecar key is the card stem not `<slot_id>-<i>`). A won the points that decide the core of the conflict: no demotion or promotion in the core (X-002, X-003), CB-2 outside the core (C-010, X-006), and the model-free per-class gate (X-008, conditional). B won the carrier-side points: separate rowcheck file (C-004), rf-qa mark mapping (C-012), evidence table and non-claims section (S-002, S-003). The advocates converged on a hybrid for 13 of 29 points; the merge therefore starts from A and incorporates B's strengths. The conditions of A's lead are listed in `refactor-plan.md`.

### Strengths to Preserve from Base
1. Advisory-only checks and no demotion or promotion in the core, with the grounds the debate verified: `ledger.py:210-213` (typed flag authority), `_brief_ids` at `ledger.py:99-104` (a demoted row never reaches the Reviser brief), no merge hook at `merge_cmd.py:71`, `SKILL.md:343`.
2. Classes as module data, no class constants in the core; extractors per class behind an offline gate (M1), now reserved.
3. Keeping the shell out of the reviewer (`reflect-reviewer.md:5, 8, 59`), with C4 and C8 as the first extractor candidates.
4. Snapshot-boundary rule for script-attached evidence; reporting found-at-any-severity and found-at-blocking separately.
5. A's consistency with C-01, C-02 and C-03, and the effect statements on PR review and rf-qa.

### Strengths to Incorporate from Non-Base Variant (Variant B)
1. The reviewer-side record-only row block `rows-v1` as the source of `observed` (B section 3 item 4; E7), placed before the findings block in v1 and after it in v2 (as agreed in Round 2).
2. A separate `review-rowcheck/1` output so `review-precheck/1` and `reread_set` stay byte-identical (B U-010); A's part (c) flags in `precheck.json` withdrawn.
3. `requires_tools` and tool-keyed `search_forms` on the card and the card-to-tool lint test (B U-012); no `extractor` field until an extractor exists.
4. The code-level tests T-B1..T-B7 as corrected in the debate, and gates G-2, G-3 (arms Z0, K, RL, SS) from B's section 6.
5. B's evidence table form and "What this proposal does not claim" section (S-002, S-003); the rf-qa mark mapping as a design inference (C-012).
6. The C-02 and C-03 containment analysis (CRITICAL floor, union) as the reason demotion stays reserved behind G-4.
