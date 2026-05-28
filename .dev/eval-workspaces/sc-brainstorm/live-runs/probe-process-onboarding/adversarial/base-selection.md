# Base Selection: Hybrid Scoring

## Quantitative Scoring (50% weight)

Deterministic metrics computed from artifact text.

| Metric | Weight | V1 (opus:scribe) | V2 (sonnet:analyzer) |
|---|---|---|---|
| RC (Requirement Coverage) | 0.30 | **1.00** — addresses all 5 success criteria + all 6 open questions explicitly in §7 | **0.82** — addresses success criteria; covers 4/6 open questions explicitly (missing explicit setup-vs-concepts priority + ceremony tolerance framing) |
| IC (Internal Consistency) | 0.25 | **1.00** — no internal contradictions detected | **1.00** — no internal contradictions detected |
| SR (Specificity Ratio) | 0.15 | **0.85** — heavy concrete numbers (4 files, ≤30 min, 400-line cap, ≤150-line cap, top-3 foot-guns); minimal vague language | **0.82** — concrete numbers (4 root causes, <300s, 95% target); some "should" framing in §6 |
| DC (Dependency Completeness) | 0.15 | **1.00** — all FR/NFR/M references defined in-document | **1.00** — all RC/INT/FR/A references defined in-document |
| SC (Section Coverage) | 0.15 | **1.00** — 7 top-level sections (max across variants) | **1.00** — 7 top-level sections |
| **Quant subtotal** | | **0.978** | **0.919** |

Computation:

- V1 quant_score = (1.00 × 0.30) + (1.00 × 0.25) + (0.85 × 0.15) + (1.00 × 0.15) + (1.00 × 0.15) = **0.978**
- V2 quant_score = (0.82 × 0.30) + (1.00 × 0.25) + (0.82 × 0.15) + (1.00 × 0.15) + (1.00 × 0.15) = **0.919**

## Qualitative Scoring (50% weight) — 30-Criterion Rubric

Claim-Evidence-Verdict (CEV) protocol; binary scoring per criterion.

### Completeness (5 criteria)

| # | Criterion | V1 | V2 |
|---|---|---|---|
| 1 | Covers all explicit requirements from source | 1 (every seed-brief open Q addressed in §7) | 0 (setup-vs-concepts + ceremony-tolerance not explicitly framed) |
| 2 | Addresses edge cases / failure scenarios | 1 (NFR-007 paste edge case, doctor failure modes) | 1 (A2 test flakiness, A1 UV install) |
| 3 | Includes dependencies / prerequisites | 1 (Audience-tag header includes Prereqs) | 1 (FR-003 prereqs listed) |
| 4 | Defines success / completion criteria | 1 (M-001 through M-006) | 1 (§4 falsification per intervention) |
| 5 | Specifies out-of-scope | 1 (§4 explicit "not producing") | 1 (§5 "NOT doing") |
| **Subtotal** | | **5/5** | **4/5** |

### Correctness (5 criteria)

| # | Criterion | V1 | V2 |
|---|---|---|---|
| 1 | No factual errors / hallucinated claims | 1 | 1 |
| 2 | Technical approaches feasible | 1 | 1 |
| 3 | Terminology used consistently | 1 | 1 |
| 4 | No internal contradictions (cross-IC) | 1 | 1 |
| 5 | Claims supported by evidence in document | 1 (cites memory `feedback_no_multiline_paste.md`) | 1 (cites concrete stale-doc content of `docs/developer-guide/`) |
| **Subtotal** | | **5/5** | **5/5** |

### Structure (5 criteria)

| # | Criterion | V1 | V2 |
|---|---|---|---|
| 1 | Logical section ordering | 1 | 1 |
| 2 | Consistent hierarchy depth | 1 | 1 |
| 3 | Clear separation of concerns | 1 (FR / NFR / M distinct) | 0 (no NFR layer; FRs mix functional + quality concerns) |
| 4 | Navigation aids present | 1 | 1 |
| 5 | Follows conventions of artifact type | 1 | 1 |
| **Subtotal** | | **5/5** | **4/5** |

### Clarity (5 criteria)

| # | Criterion | V1 | V2 |
|---|---|---|---|
| 1 | Unambiguous language (no "should consider"/"might"/"as appropriate") | 1 | 0 ("should distinguish" in §6 baseline plan; one "may" in §7) |
| 2 | Concrete rather than abstract | 1 | 1 |
| 3 | Each section purpose clear | 1 | 1 |
| 4 | Acronyms defined on first use | 1 | 1 |
| 5 | Actionable next steps identified | 1 (Adoption Path) | 1 (Falsification Plan is action-shaped) |
| **Subtotal** | | **5/5** | **4/5** |

### Risk Coverage (5 criteria)

| # | Criterion | V1 | V2 |
|---|---|---|---|
| 1 | ≥3 risks identified with prob/impact assessment | 1 (§7 residual risks) | 1 (§7 five open assumptions A1–A5) |
| 2 | Mitigation strategy per risk | 1 | 1 |
| 3 | Failure modes / recovery covered | 0 (doc-rot mentioned but limited recovery story) | 1 (test flakiness, UV install failure, contributor-profile shift) |
| 4 | External-dependency failure scenarios | 0 | 1 (A1 UV install; A5 external link breakage) |
| 5 | Monitoring / validation mechanism | 1 (CI gate) | 1 (baseline + grep checks) |
| **Subtotal** | | **3/5** | **5/5** |

### Invariant & Edge Case Coverage (5 criteria)

| # | Criterion | V1 | V2 |
|---|---|---|---|
| 1 | Boundary conditions for collections | 0 (n/a for this artifact type, neither addresses) | 0 |
| 2 | State variable interactions | 1 (`make onboard-check` exit-code semantics) | 1 (FR-003 step ordering, exit codes) |
| 3 | Guard condition gaps | 1 (FR-010 anti-violation guardrail) | 1 (FR-007 no-claude-skills-commit gate) |
| 4 | Count divergence | 0 (n/a) | 0 (n/a) |
| 5 | Interaction effects | 1 (sync-dev + PR-review interaction) | 1 (A5 cross-impact of stale-doc removal on `superclaude install` references) |
| **Subtotal** | | **3/5** | **3/5** |

### Edge Case Floor Check

| Variant | Invariant subtotal | Floor (1/5) | Eligible? |
|---|---|---|---|
| V1 | 3/5 | ≥ 1/5 | ✓ Eligible |
| V2 | 3/5 | ≥ 1/5 | ✓ Eligible |

### Qualitative Totals

| Variant | Comp. | Corr. | Struct. | Clarity | Risk | Invar. | **Total** |
|---|---|---|---|---|---|---|---|
| V1 | 5 | 5 | 5 | 5 | 3 | 3 | **26/30 = 0.867** |
| V2 | 4 | 5 | 4 | 4 | 5 | 3 | **25/30 = 0.833** |

## Position-Bias Mitigation

A single-orchestrator quick-depth run does not invoke independent dual-pass evaluation. Per-criterion verdicts above were assigned with explicit CEV citations; no Pass-1/Pass-2 disagreement resolution was required. Note this in the telemetry.

## Combined Scoring

| Variant | Quant (×0.50) | Qual (×0.50) | **Combined** |
|---|---|---|---|
| V1 | 0.978 × 0.50 = 0.489 | 0.867 × 0.50 = 0.4335 | **0.9225** |
| V2 | 0.919 × 0.50 = 0.4595 | 0.833 × 0.50 = 0.4165 | **0.8760** |

**Margin:** 0.0465 (4.65%) — **within 5% tiebreaker zone**.

## Tiebreaker Application

| Level | Criterion | V1 | V2 | Winner |
|---|---|---|---|---|
| 1 | Debate performance (diff points won in contested categories) | 3 wins (S-003, C-005, C-006) | 5 wins (S-002, S-004, C-003, C-004, C-007) | **V2** |
| 2 | Higher correctness criteria count | (would be 5/5) | (would be 5/5) | n/a — Level 1 decisive |
| 3 | Input order | (would be first) | — | n/a |

Level 1 (debate performance) is decisive: V2 wins 5 contested diff points to V1's 3 (5 additional points were hybrid resolutions). **V2 is selected as base.**

## Selected Base: Variant 2 (sonnet:analyzer)

**Selection rationale:**

V1 has slightly higher combined raw score (0.9225 vs 0.8760) driven by stronger Completeness, Structure, and Clarity. However, the margin (4.65%) falls within tiebreaker range, and V2 wins debate performance decisively. The debate exposed that V2's core insights — RC-1 stale-doc diagnosis, per-FR falsification discipline, baseline measurement plan, Causes-vs-Symptoms framing — are *structural advantages V1 fully conceded*. V1's higher quant/qual scores reflect its strength as a documentation artifact; V2's debate dominance reflects its strength as a *diagnostic and verifiable* spec. Adopting V2 as base means the merged output starts from causes-before-interventions reasoning (the more honest planning posture) and inherits V1's documentation discipline as enrichment rather than as foundation.

**Strengths to preserve from V2 (base):**

- Root-Cause Diagnosis (§1) with Causes-vs-Symptoms table
- Targeted Interventions framing (each intervention tied to a named root cause)
- Per-FR inline falsification pattern (each FR ends with a verifiable check)
- Falsification Plan (§4) with concrete per-intervention tests
- Explicit baseline measurement plan
- Open Assumptions section (A1–A5)
- "What We Are NOT Doing" with diagnosis-grounded rationale

**Strengths to incorporate from V1 (non-base):**

- Audience-tagged guide structure (FR-006: `**Audience:** X | **Time:** Y | **Prereqs:** Z`)
- Two-click rule (FR-004) for confusion-point discoverability
- Single-line command discipline (NFR-007, grounded in user terminal memory)
- `superclaude doctor` integration as troubleshooting primitive (FR-009)
- Brevity caps as `wc -l`-enforceable check (NFR-001 + M-005)
- DM-as-doc-bug improvement loop (V1 §7 residual)
- Layered guide structure: `docs/contributing/` directory with audience-tagged files (compromise on C-001/X-001)
- Both Makefile targets: `make onboard` (contributor) + `make onboard-check` (CI) (compromise on C-002/X-002)
- NFR layer split from FR layer (compromise on S-003)
- Explicit handling of every seed-brief open question (compromise on C-006)
