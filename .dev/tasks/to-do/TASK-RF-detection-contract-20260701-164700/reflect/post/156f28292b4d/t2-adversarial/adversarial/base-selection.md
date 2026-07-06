# Base Selection

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant 1 (qwen) | Variant 2 (glm) | Basis |
|--------|--------|------------------|-----------------|-------|
| Requirement coverage (RC) | 0.30 | 1.00 | 0.30 | V1 covers all 5 audit-scope dims (regressions, drift, missing verification, unresolved decisions, suspect-source); V2 truncated → headline + partial F-001 only |
| Internal consistency (IC) | 0.25 | 1.00 | 1.00 | Neither contains internal contradictions (V2 fragment is consistent as far as it goes) |
| Specificity ratio (SR) | 0.15 | 0.90 | 0.80 | V1 dense with line refs / file paths / exit codes; V2 specific but sparse |
| Dependency completeness (DC) | 0.15 | 1.00 | 0.50 | V2 ends on a dangling `Completion Date:` reference with no resolution |
| Section coverage (SC) | 0.15 | 1.00 | 0.40 | V1 = 5+ H2 sections (max); V2 = 2 complete of 5 |
| **quant_score** | | **0.985** | **0.595** | (RC×.30)+(IC×.25)+(SR×.15)+(DC×.15)+(SC×.15) |

## Qualitative Scoring (50% weight) — Additive Binary Rubric (CEV)

| Dimension (5 criteria each) | Variant 1 | Variant 2 | Evidence |
|-----------------------------|-----------|-----------|----------|
| Completeness | 5/5 | 1/5 | V1: full findings + tables + recommendations. V2: truncated — only headline reached |
| Correctness | 5/5 | 3/5 | V1: every claim CONFIRMED vs ground truth. V2: headline correct but "beyond permitted carve-outs" overstates a documented low-risk deviation (−1); incomplete (−1) |
| Structure | 5/5 | 2/5 | V1: clean hierarchy, tables. V2: cut off mid-section |
| Clarity | 5/5 | 4/5 | Both clear where present; V2's data-treatment note is notably crisp |
| Risk Coverage | 4/5 | 1/5 | V1: identifies suspect files + mitigations + verification recommendations; monitoring mechanism partial (−1). V2: not reached |
| Invariant & Edge Coverage | 3/5 | 1/5 | V1: probes suspect files for over-correction, boundary/predicate risks; not exhaustive edge enumeration. V2: not reached |
| **criteria met / 30** | **27/30** | **12/30** | |
| **qual_score** | **0.90** | **0.40** | total_met / 30 |

### Edge Case Floor Check
- Variant 1: Invariant & Edge = 3/5 ≥ 1/5 → **ELIGIBLE** as base.
- Variant 2: 1/5 ≥ 1/5 → eligible, but not competitive.
- Floor NOT suspended (at least one variant ≥ 1/5).

## Position-Bias Mitigation
- Pass 1 (V1, V2) and Pass 2 (V2, V1) agree: Variant 1 dominates on every dimension except S-003 (injection-hygiene note). No disagreement requiring re-evaluation. The single asymmetry (V2's unique hygiene note) is captured as U-003 for incorporation, not as a base-selection swing.

## Combined Scoring

| Variant | Quant (×0.50) | Qual (×0.50) | **Combined** |
|---------|---------------|--------------|--------------|
| **Variant 1 (qwen3.6-plus)** | 0.4925 | 0.450 | **0.9425** |
| Variant 2 (glm-5.2) | 0.2975 | 0.200 | **0.4975** |

- Margin: **44.5%** — far above the 5% tiebreaker threshold. No tiebreaker invoked.

## Selected Base: Variant 1 (qwen3.6-plus)

**Selection rationale:** Variant 1 is complete, structurally rich, and — critically for a `--suspect-source` audit — every one of its substantive claims was independently CONFIRMED against the target task file (see debate-transcript.md ground-truth adjudication). Variant 2 is a 19-line truncated fragment that reaches the same (correct) headline but produces no finding set, tables, or recommendations, and overstates the one deviation it implies.

**Strengths to preserve (from base):**
- 5 evidence-anchored findings with Signal ratings
- Pass/Fail table separating implementation-PASS from completion-gate-FAIL
- Suspect-Source risk-vector table (6 verified files)
- 4 downstream-scoring recommendations

**Strengths to incorporate (from Variant 2):**
- U-003: explicit prompt-injection / data-treatment hygiene declaration (target treated as DATA; embedded imperatives not obeyed) → add as a reviewer-provenance note.

**Corrections applied during merge:**
- X-001: adopt Variant 1's calibrated **WARN** framing for the Step 5.3 deviation; drop Variant 2's "beyond permitted carve-outs" characterization (ground-truth-refuted).
- INV-002: state the completion condition as "Step 5.6 exit 0 **then** Step 5.7 preconditions (all prior items complete, validation PASS, no unresolved blocker)", not "5.6 alone".
