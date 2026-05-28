# Base Selection — Hybrid via Adversarial Convergence

## Note on selection methodology

Standard `sc:adversarial` base-selection picks ONE variant as the merged base, then incorporates others' strengths. In this run, the Round 2 rebuttals and Round 2.5 invariant probe converged on a **HYBRID** that cherry-picks load-bearing elements from all 3 variants. The scoring below records each variant's contribution, the hybrid's composition, and explicit acknowledgment that no single variant's strategy survives unmodified.

## Quantitative Scoring

| Metric | Weight | V1 (RCA) | V2 (RefExp) | V3 (QE) |
|--------|--------|----------|-------------|---------|
| Requirement coverage (RC) — covers 5/5 PR findings | 0.30 | 1.00 (defers F2, F4 to follow-up PRs but covers all 5) | 1.00 | 1.00 |
| Internal consistency (IC) | 0.25 | 0.95 | 0.88 (F2 policy ambiguity self-acknowledged) | 0.92 |
| Specificity ratio (SR) | 0.15 | 0.85 (specific line cites + regex literal) | 0.80 | 0.95 (regex literal + IC-### renumbering risk named) |
| Dependency completeness (DC) | 0.15 | 0.90 | 0.85 | 0.95 (test_t1 filter change explicit) |
| Section coverage (SC) | 0.15 | 0.86 (6/7) | 0.86 (6/7) | 1.00 (7/7) |
| **Quant score** | — | **0.92** | **0.88** | **0.95** |

## Qualitative Scoring (30-criterion rubric)

| Dimension | V1 (RCA) | V2 (RefExp) | V3 (QE) |
|-----------|----------|-------------|---------|
| Completeness (5) | 4 (defers F2/F4) | 5 | 5 |
| Correctness (5) | 5 | 4 (F2 single-line flip under-specified; INV-002 false) | 4 (INV-007 latent path; one false-claim on additive-only sufficiency) |
| Structure (5) | 5 (3-PR shape disciplines review) | 4 | 4 (Phase 0 sequencing strong; total surface broad) |
| Clarity (5) | 5 | 5 (named invariants) | 4 |
| Risk Coverage (5) | 4 (acknowledges F2 latency risk explicitly) | 3 (F4 renumbering risk under-addressed) | 5 (5 named risks, including IC-### shifts) |
| Invariant & Edge Case Coverage (5) | 3 (implicit) | 2 (helper invariants named but Layer 3 window-upper missed → INV-002) | 5 (explicit, but missed INV-003 PascalCase) |
| **Qual subtotal** | **26/30 (0.87)** | **23/30 (0.77)** | **27/30 (0.90)** |

### Edge-case floor check

Threshold: 1/5 on Invariant & Edge Case Coverage. All 3 variants pass (V2=2/5, V1=3/5, V3=5/5). No suspension required.

## Position-Bias Mitigation

Re-evaluated in reverse order (V3 → V2 → V1) with same rubric. Two criterion-variant pairs flipped:

- Pass 1 V1 Structure = 4 → Pass 2 V1 Structure = 5 (reverse order made the PR-shape discipline more visible). Re-evaluation verdict: 5.
- Pass 1 V3 Risk Coverage = 4 → Pass 2 V3 Risk Coverage = 5 (re-evaluation noted the IC-### renumbering callout was a specific, falsifiable risk). Re-evaluation verdict: 5.

Both adjustments applied to scores above. No other disagreements.

## Combined Scoring

| Variant | Quant (×0.50) | Qual (×0.50) | **Final** | Margin to next |
|---------|---------------|--------------|-----------|----------------|
| V3 (QE) | 0.475 | 0.450 | **0.925** | leader |
| V1 (RCA) | 0.460 | 0.435 | **0.895** | −0.030 |
| V2 (RefExp) | 0.440 | 0.385 | **0.825** | −0.100 |

**Tiebreaker triggered**: V3 and V1 are 3.0% apart (within 5% threshold).

- Level 1 (debate performance): V1 won 8 diff points; V3 won 6. → **V1 takes Level 1**.
- Final Level 1 winner: V1.

## Selected Base: **HYBRID** (V1 structure + V3 sequencing + V2 helper + INV-002 amendment)

The pure-tiebreaker result (V1) is overridden by the explicit hybrid convergence from Round 2 rebuttals and the Round 2.5 fault-finder remediation. The rationale:

- **From V1 (PR shape)**: 3-PR split — PR A = F1+F3+F5, PR B = F2 (separate), PR C = F4 (separate). PR A inherits all subsequent V3/V2 strengths.
- **From V3 (sequencing + additive)**: Pin tests land FIRST in PR A; F1 is additive-only (preserve `S10` AND add `FR-S10-02`).
- **From V2 (abstraction)**: Introduce `_canonicalize_identifiers(text) -> frozenset[str]` helper in PR A with the 3 named invariants in its docstring.
- **From Round 2.5 (INV-002/003/012 amendment)**: Mandate Layer 3 `window_text.upper()` at PR-line 355 alongside the helper. Without this, F3 is NOT closed — verified empirically by fault-finder.

### Strengths to preserve

- V1's PR-scope discipline and per-PR revertibility.
- V3's pin-tests-first sequencing and additive-only F1.
- V3's `test_t1` filter change (substring → `c.mechanism_signature[1]`).
- V2's named-invariant helper as the locus of canonicalization.

### Strengths NOT incorporated (and why)

- V3's property-based hypothesis tests + JSON snapshot guard + new conftest.py — deferred to a follow-up "test infrastructure" PR (V3 conceded this in Round 2).
- V2's "single PR" framing — overruled in favor of V1's 3-PR split, but V2's helper IS preserved inside V1's PR A.
- V1's "F4 splits because of counter renumbering risk" — preserved as PR C separation.

## Convergence gate status

- Diff-point agreement: 81% ≥ 0.80 ✅
- All 3 taxonomy levels covered: ✅ (L1 in S-003 abstraction; L2 in S-001 PR shape; L3 in INV-001 through INV-015 state/guard probes)
- HIGH UNADDRESSED invariants: **3 → resolved by the explicit amendment** (mandate window-upper alongside helper). Post-amendment count = 0.

**Status: CONVERGED on hybrid.**
