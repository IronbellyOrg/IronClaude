# Base Selection: Canonical UC-2 Reachability Design

## Quantitative Scoring (50% weight)

Metrics adapted to design-decision artifacts (precision-for-gate-role, safety, completeness, blast-radius, decision-reversibility).

| Metric | Weight | C-canonical | B-canonical | Coexist-now |
|---|---:|---:|---:|---:|
| Gate-role precision (false-Regression resistance) | 0.30 | 0.95 | 0.55 | 0.60 |
| Safety / false-PASS resistance | 0.25 | 0.90 | 0.70 | 0.55 |
| Completeness shipped today | 0.15 | 0.95 | 0.55 | 0.50 |
| Blast radius / merge risk (higher = safer) | 0.15 | 0.80 | 0.75 | 0.30 |
| Reversibility (can add the other later) | 0.15 | 0.85 | 0.70 | 0.40 |
| **quant_score** | | **0.892** | **0.633** | **0.503** |

## Qualitative Scoring (50% weight) — additive binary across 6 dimensions (CEV)

| Dimension (5 criteria each) | C | B | Coexist |
|---|---:|---:|---:|
| Completeness | 5/5 | 3/5 | 3/5 |
| Correctness | 5/5 | 4/5 | 3/5 |
| Structure (ownership clarity) | 4/5 | 3/5 | 2/5 |
| Clarity (operator signal) | 4/5 | 3/5 | 2/5 |
| Risk coverage | 4/5 | 4/5 | 2/5 |
| Invariant & edge-case coverage | 4/5 | 3/5 | 2/5 |
| **qual_score (/30)** | **26/30 = 0.867** | **20/30 = 0.667** | **14/30 = 0.467** |

Edge-case floor (≥1/5 on invariant dimension): C 4/5 ✓, B 3/5 ✓, Coexist 2/5 ✓ — all eligible.

## Combined Scoring

| Variant | quant×0.5 | qual×0.5 | **combined** |
|---|---:|---:|---:|
| **C-canonical** | 0.446 | 0.434 | **0.880** |
| B-canonical | 0.317 | 0.334 | 0.650 |
| Coexist-now | 0.252 | 0.234 | 0.485 |

Margin C over B = 0.230 (>0.05) → **no tiebreaker needed.**

## Selected Base: Variant 1 — C-canonical (FR-RH1 contracted-sink gate)

**Rationale:** C wins decisively on the two dimensions that matter most for a *gate* — precision and false-PASS resistance — and is the most complete artifact today. B's genuine strength (recall) is preserved by demoting it to the complementary advisory lane, not by discarding it.

**Strengths to preserve (from C):** real-boot-only Regression bar; telemetry-only skips; additive 1.6.0 R7 schema; full wrapper/docs/bounded-cost surface.

**Strengths to incorporate (from B):** broad unwired-surface recall as an additive, advisory, *later* capability; B's fail-open-on-uncertainty discipline; UNREACHED as a finding modifier that never downgrades a C Regression.

**Edge-case floor:** satisfied.
