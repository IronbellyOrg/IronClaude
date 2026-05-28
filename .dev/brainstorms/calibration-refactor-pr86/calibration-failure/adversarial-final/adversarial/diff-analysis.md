# Diff Analysis: Calibration-Failure Root-Cause Merge Comparison

## Metadata

- Generated: 2026-05-26T19:35Z
- Variants compared: 3 (A-merged, B-merged, C-merged — each itself a sc:adversarial merge of the same 3 underlying theory files)
- Total differences found: 14
- Categories: structural (3), content (5), contradictions (1), unique (3), shared assumptions (2)

## Structural Differences

| #     | Area                          | Variant 1 (A)                                                       | Variant 2 (B)                                          | Variant 3 (C)                                                                       | Severity |
|-------|-------------------------------|---------------------------------------------------------------------|--------------------------------------------------------|-------------------------------------------------------------------------------------|----------|
| S-001 | Top-level section count       | 7 H2 sections (methodology, T1–T4, secondary, cross-theory, top-causes) | 5 H2 sections (top-line, theories, cross-theory, caveat, methodology) | 6 H2 sections (M1, M2, M3-composite, M4, cross-mechanism, caveats, top-causes) | Low      |
| S-002 | M3 hierarchy depth            | Flat T3 + Secondary §S1/S2 (depth 2)                                | Flat M3 only (depth 1)                                 | M3 with M3a/M3b/M3c subsections (depth 2)                                           | Medium   |
| S-003 | Provenance annotation style   | HTML comment per section: `<!-- provenance: ... -->`                | Bottom-of-doc provenance map table                     | Inline italic per section: `*Provenance: ...*`                                      | Low      |

## Content Differences

| #     | Topic                                  | Variant 1 (A)                                                                                              | Variant 2 (B)                                                                          | Variant 3 (C)                                                                                                       | Severity |
|-------|----------------------------------------|------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|----------|
| C-001 | M1 confidence value                    | 0.90                                                                                                       | 0.90                                                                                   | 0.88                                                                                                                | Low      |
| C-002 | M3 framing                             | Verdict-direction is primary T3; stripped-context and anchoring demoted to Secondary §S1/§S2                | Verdict-direction is M3, only; other two not represented                               | M3 explicitly composite (M3a verdict-direction 0.78 + M3b stripped-context 0.65 + M3c anchoring 0.45)               | High     |
| C-003 | Channel-B-degradation disclosure       | Full §Methodology & Channel Disclosure table at top (load-bearing limit on certainty)                       | Abbreviated §5 methodology note (1 paragraph)                                          | Not explicitly disclosed (referenced obliquely in protocol header only)                                              | Medium   |
| C-004 | M1 fix formula                         | Gated minimum primary (V2's), with V1 veto-or-cap and V3 runtime-aware clamp as alternatives               | Gated minimum primary, runtime-aware clamp as alternate                                | Gated minimum + veto rule + runtime predicate-type cap (lists all three as composite fix)                            | Medium   |
| C-005 | Top-causes count and inclusion         | Top 4 ranked (M1, M2, M3-verdict, M4), explicit "compositional not exchangeable"                            | Top 4 implied (M1/M2/M3/M4), framed as multiplicative+orthogonal+meta                  | Top 3 + M3a flagged as "strong alternative third pick" (treats M4 vs M3a as tied for #3)                            | Medium   |

## Contradictions

| #     | Point of Conflict                      | Variant 1 (A) Position                                                                              | Variant 2 (B) Position                                                              | Variant 3 (C) Position                                                                                | Impact |
|-------|----------------------------------------|-----------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|--------|
| X-001 | Is M3 one mechanism or three?          | One primary (verdict-direction) + two demoted secondaries                                            | One mechanism (verdict-direction) — other two not surfaced                          | Composite of three orthogonal sub-mechanisms, each with distinct fix and distinct confidence          | Medium |

## Unique Contributions

| #     | Variant        | Contribution                                                                                                                                                              | Value Assessment |
|-------|----------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------|
| U-001 | Variant 1 (A)  | Cross-theory implications §5 paragraph: "T3 is upstream of T1 and T2" ordering analysis with explicit fix-sequence (apply T2 first, then T3 atop it)                       | High             |
| U-002 | Variant 2 (B)  | Top-line findings §1 — single-paragraph synthesis of multiplicative+modulated+propagated structure suitable for an executive summary                                       | Medium           |
| U-003 | Variant 3 (C)  | M3 composite structure preserving M3b's Falsification-standard card-field fix and M3c's dual-instance-minimum fix — two structurally independent improvements absent from A/B | High             |

## Shared Assumptions

| A-NNN | Assumption                                                                                                                            | Source Agreement                                              | Impact | Status    |
|-------|---------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------|--------|-----------|
| A-001 | The pr86 substrate (0.90 calibrated, evidence-grounding=0.5 plus four 1.0s) is structurally analogous to the H3 0.95-REFUTE case      | All three converge on substrate-vs-H3 framing                  | High   | UNSTATED  |
| A-002 | The four "prose-readable" dimensions (symptom coverage, reproducibility fit, fix directness, domain coherence) are independent enough of evidence-grounding that they can honestly score 1.0 when evidence-grounding is 0.5 | All three use the (0.5 + 1 + 1 + 1 + 1) / 5 = 0.90 demonstration | High   | UNSTATED  |

## Summary

- Total structural differences: 3 (none High-severity)
- Total content differences: 5 (1 High-severity: C-002)
- Total contradictions: 1 (Medium-severity: X-001)
- Total unique contributions: 3 (U-001 High, U-002 Medium, U-003 High)
- Total shared assumptions surfaced: 2 (both UNSTATED, both High-impact)
- Highest-severity items: C-002 (M3 framing), U-001 and U-003 (compositional value)
- Variants substantially similar threshold check: 14 differences out of ~40 comparable items ≈ 35% — above 10% similarity floor, debate proceeds.
