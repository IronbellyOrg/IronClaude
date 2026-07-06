# Base Selection

These are competing framework-policy positions on one proposition. The qualitative rubric (Correctness, Risk Coverage, Invariant/Edge-case) plus the Round 2.5 probe carry the selection.

## Quantitative (informational)
| Metric (weight) | V1 | V2 | V3 |
|---|---|---|---|
| IC (0.25) | 0.82 | 0.92 | 0.90 |
| SR (0.15) | 0.88 | 0.85 | 0.88 |
| DC (0.15) | 0.85 | 0.88 | 0.92 |
| SC (0.15) | 1.00 | 1.00 | 1.00 |
| RC (0.30) | 0.85 | 0.90 | 0.92 |
| **quant** | **0.87** | **0.91** | **0.92** |

## Qualitative (additive binary, decisive dimensions)
| Dimension (/5) | V1 | V2 | V3 |
|---|---|---|---|
| Completeness | 4 | 5 | 5 |
| **Correctness** | 2 | 5 | 4 |
| Structure | 5 | 5 | 5 |
| Clarity | 5 | 4 | 5 |
| Risk Coverage | 3 | 5 | 4 |
| **Invariant & Edge-Case** | 2 | 4 | 3 |
| **/30** | **21** | **28** | **26** |
| **qual** | **0.70** | **0.93** | **0.87** |

**Correctness CEV:**
- **V1 — NOT MET ×3.** Blanket delegation refuted by its own concessions (A-002 freeze-first, A-003 reflexive exception, monoculture irreducible); mechanism-superset claim false on the recall≠precision axis (`context.md` §5).
- **V2 — MET ×5.** Every core claim survived and was *amplified* by the probe: monoculture (INV-001/003), watcher-never-watches (INV-002), already-violated-at-Phase-E (INV-004) are all V2's framework-monoculture thesis made structural.
- **V3 — NOT MET ×1.** The rubric is correct *locally* (derives the right per-target verdict) but the probe showed it is necessary-not-sufficient: it cannot see the aggregate property (INV-001) and its success condition is the monoculture trigger (INV-003).

## Combined
| Variant | quant×.5 | qual×.5 | **score** |
|---|---|---|---|
| V1 | 0.435 | 0.350 | **0.785** |
| V2 | 0.455 | 0.465 | **0.920** |
| V3 | 0.460 | 0.435 | **0.895** |

V2 (0.920) and V3 (0.895) are within 5% → **tiebreaker**.
- **Level 1 (debate performance):** V2 won the HIGH invariant points (INV-001/002/003/004 are V2's thesis); V3 won by parameterizing the contradictions. Split.
- **Level 2 (correctness count):** V2 > V3 (28 vs 26; V2's claims survived, V3's rubric shown insufficient). **V2 edges it.**

## Selected Base: **V3 (rubric) as structural scaffold, with V2 as the decisive transfer**

**Rationale — why not simply V2:** The proposition is explicitly *"a pattern for these two AND all future protocols."* A bare stance ("never delegate") cannot answer "all future protocols" — V2 itself concedes a future auto-apply protocol genuinely fits reflect (`variant-2:25`), which a blanket "never" cannot encode. Only a *procedure* generalizes. So the framework answer must be structured as V3's rubric.

**But V3 alone fails the probe.** The 4 HIGH invariants prove the per-protocol rubric is necessary-not-sufficient. The merge therefore takes V3's rubric as scaffold and grafts in **V2's framework-level guards** as mandatory additions — without them the rubric green-lights its own monoculture. This is a genuine V3-base + critical-V2-transfer merge, not a V3 win.

**Strengths to preserve (V3):** the 4-gate per-protocol decision procedure; derives "keep both" for the targets; permits the narrow applied-work case; auditable per-protocol verdict.

**Strengths to incorporate (V2 — decisive):** the aggregate monoculture invariant (a framework-level verifier-heterogeneity guard the per-protocol gates structurally lack — INV-001/003); the requirement that reflect's own output be independently cross-checked (INV-002); fail-closed-to-bespoke on ambiguity.

**Kernel to incorporate (V1):** for genuine applied-work / auto-apply protocols, delegation is right (G1+G4) — but never as sole validator, and only after an enforceable contract freeze.

**Edge-case floor:** all three ≥1/5; floor satisfied.
