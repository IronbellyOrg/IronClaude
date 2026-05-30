# Base Selection — OQ-1 Adversarial Debate

## Note

This debate produced unanimous convergence on Option B. Both opposing advocates (A and C) explicitly conceded the field to B on correctness and scope-discipline grounds. Standard hybrid scoring is performed below for completeness but the outcome is over-determined.

## Quantitative Scoring

| Metric | Weight | V1 (A) | V2 (B) | V3 (C) |
|--------|--------|--------|--------|--------|
| Requirement coverage (covers all 4 pin tests) | 0.30 | 0.75 (3/4) | **1.00 (4/4)** | 0.75 (3/4) |
| Internal consistency | 0.25 | 0.90 (explicit about partial nature) | 1.00 | 0.85 (claims correctness but requires B to actually work) |
| Specificity ratio | 0.15 | 0.85 (concrete trace, concrete failure) | 0.95 (regex literal + 4-test trace) | 0.80 |
| Dependency completeness | 0.15 | 0.95 (self-contained) | 0.95 | 0.70 (depends on B to fully work) |
| Section coverage | 0.15 | 0.85 | 1.00 | 0.85 |
| **Quant score** | — | **0.86** | **0.99** | **0.81** |

## Qualitative Scoring (30-criterion rubric)

| Dimension | V1 (A) | V2 (B) | V3 (C) |
|-----------|--------|--------|--------|
| Completeness (5) | 3 | 5 | 3 |
| Correctness (5) | 3 (test 2 fails) | 5 | 2 (claims that don't hold) |
| Structure (5) | 5 | 5 | 4 |
| Clarity (5) | 5 (very clear about being partial) | 5 | 4 |
| Risk Coverage (5) | 4 | 5 | 3 (under-counts the V1/V2/V3 contract-violation risk) |
| Invariant & Edge Case Coverage (5) | 2 (silently degrades invariant 1) | 5 | 2 (same issue) |
| **Qual subtotal** | **22/30 (0.73)** | **30/30 (1.00)** | **18/30 (0.60)** |

### Edge-case floor (1/5 on Invariant coverage)

All 3 variants pass the floor (V1=2/5, V2=5/5, V3=2/5). No suspension.

## Position-Bias Mitigation

Re-evaluated in reverse order (V3 → V2 → V1). Zero criterion-variant pairs flipped. Final scores unchanged.

## Combined Scoring

| Variant | Quant (×0.50) | Qual (×0.50) | **Final** | Margin |
|---------|---------------|--------------|-----------|--------|
| **V2 (B)** | 0.495 | 0.500 | **0.995** | leader |
| V1 (A) | 0.430 | 0.365 | 0.795 | −0.200 |
| V3 (C) | 0.405 | 0.300 | 0.705 | −0.290 |

**Margin between B and runner-up: 20.0%** — well above the 5% tiebreaker threshold. No tiebreaker needed.

## Selected Base: **Variant 2 — Option B (Helper Uppercases Input)**

### Selection rationale

- **Correctness (decisive)**: The only option where all 4 pin tests pass post-fix. Verified by 3 independent regex traces.
- **Scope-discipline**: Single-word production change (`text.upper()`); preserves `_extract_identifiers` public contract per V1/V2/V3 adversarial-converged decision.
- **Invariant integrity**: Uniquely honors the helper's docstring claim ("All tokens are uppercase") as binding.
- **Unanimous adversarial concession**: Both opposing advocates explicitly chose B as superior on correctness + scope-discipline.

### Strengths to preserve

- The 1-word `.upper()` helper change (Part 1).
- The Test 1 wrapper change to use `_canonicalize_identifiers` (Part 2, shared with Option A).

### Strengths NOT incorporated

- **Option A's "scope discipline at all costs"** framing — overruled because Test 2 failure is non-negotiable correctness, not a style preference.
- **Option C's modification of `_extract_identifiers`** — overruled because (a) C alone doesn't fix Test 2 anyway, (b) violates the V1/V2/V3 adversarial decision, (c) is strictly subsumed by B.

### Strengths NOT preserved from B (the proposal)

- B's "Risks" mention of `.upper()` performance overhead — kept in merged output as a note for reviewers but not flagged as blocker.

## Convergence gate status

- Diff-point agreement: 100% ✅
- All taxonomy levels covered: ✅ (L1 surface diffs S-001/002; L3 state-mechanics diffs C-001 through C-005, X-001, U-001/002, A-003)
- HIGH UNADDRESSED invariants: 0 (Round 2.5 skipped per depth=quick)

**Status: CONVERGED on Option B.**
