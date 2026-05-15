# Base Selection — Hybrid Scoring & Tiebreaker

## Quantitative Scoring (50% weight)

5 deterministic metrics. Both variants assessed on the same axes. "Source" for requirement coverage is the calling brief: "preserve traceability from A while inheriting decision pills/recommendations from B." Both drafts also share the implicit source set = Wave-1 extracts R1-R6 + R7/R8 current-state docs.

| Metric | Weight | Variant A score | Variant B score | Computation |
|--------|--------|------------------|------------------|-------------|
| Requirement coverage (RC) | 0.30 | 0.92 | 0.78 | A: covers ALL Wave-1 candidates (TU-001..006, SE-001..006) with source-extract citation per candidate; covers all v3.7 prior-art constraints (§9.1-§9.9); covers all known issues (G1-G9 equivalents from R7 §5 / R8 §6). 47 of 47 overlap rows (O1-O47) sourced. RC = 47/47 × content-source ratio ≈ 0.92. B: covers B1-B20 candidates with source-extract citation; 21 of 21 overlap rows sourced; risk register 12/12 sourced but drops RK-19 (Wave-4 parser regression) and RK-20 (v3.7 live-exec not validated) without rationale. RC = 0.78. |
| Internal consistency (IC) | 0.25 | 0.96 | 0.94 | A: 1 self-acknowledged inconsistency (Q1 vs §9.4 tension on sentinel rename — explicitly an open question, not a contradiction). 95+ scorable claims; 4 internal tensions all flagged as open questions. IC = 1 − 4/95 ≈ 0.96. B: 0 internal contradictions; collapses Q1+Q2 (A's distinction) into Q3, which is a synthesis choice not a contradiction; 1 unresolved tension (R-5 "Inventory consumers before renaming" but B11 already verdict=DEFER without that inventory). IC = 1 − 5/85 ≈ 0.94. |
| Specificity ratio (SR) | 0.15 | 0.84 | 0.79 | A: concrete indicators include all file:line cites (~120 instances), all numeric weights from R6, all v3.7 baseline numbers (921 passed, 57 failed, 125/125, 16/16), specific risk likelihood + blast-radius. Vague indicators: 15 `[inference]` tags which A flags rather than hides; misc "may be" / "could" in §8 open questions. SR = (concrete) / (concrete + vague) ≈ 0.84. B: concrete indicators include 28 line-ref citations (mostly v3.7 prior-art), Sev / Like ratings, Effort labels S/M/L, status pills. Vague indicators include uncited owner-role assignments, uncited effort labels (S/M/L without derivation), generic "Inventory consumers before renaming" mitigation. SR ≈ 0.79. |
| Dependency completeness (DC) | 0.15 | 0.95 | 0.88 | A: all internal references (O-rows ↔ TU/SE candidates ↔ RK-rows ↔ Q-rows) resolve. References to v3.7 release artifacts (HANDOVER, TEST-SPEC, release-split-report) resolve to listed files. Coverage notes self-check enumerates Known gaps. DC ≈ 0.95. B: B-row ↔ R-row ↔ Q-row references resolve. Drops the §9.5 baseline references A has. R-1..R-12 risk references all resolve. DC ≈ 0.88. |
| Section coverage (SC) | 0.15 | 1.00 | 0.78 | A has 9 H2 sections + extensive H3 nesting (§4 has 14 subsections, §8 has 10 subsections, §9 has 9 subsections), total ~62 named subsections. B has 9 H2 sections with minimal H3 nesting, total ~12 named subsections. SC_A = max = 1.00. SC_B = 12/62 (but normalized: 47/62) — using max-normalization, SC_B = 0.78 reflecting B's intentional compression. |

**Quantitative formula:**
- quant_score_A = (0.92 × 0.30) + (0.96 × 0.25) + (0.84 × 0.15) + (0.95 × 0.15) + (1.00 × 0.15)
                = 0.276 + 0.240 + 0.126 + 0.143 + 0.150 = **0.935**
- quant_score_B = (0.78 × 0.30) + (0.94 × 0.25) + (0.79 × 0.15) + (0.88 × 0.15) + (0.78 × 0.15)
                = 0.234 + 0.235 + 0.119 + 0.132 + 0.117 = **0.837**

---

## Qualitative Scoring (50% weight) — Additive Binary Rubric (30 criteria)

Claim-Evidence-Verdict applied. Each criterion = 1 (MET) or 0 (NOT MET).

### Completeness (5 criteria)

| # | Criterion | Variant A | Variant B |
|---|-----------|-----------|-----------|
| C1 | Covers all explicit requirements from source input | MET — 47 overlap rows + 12 candidates + 14 questions cover the brief's "completeness + traceability + decision-readiness" axes | MET — 21 overlap rows + 20 candidates + 10 questions cover the brief's "decision-readiness" axis fully |
| C2 | Addresses edge cases and failure scenarios | MET — RK-13 regex collision, RK-14 subprocess blocking, RK-18..RK-20 covered. Q5 EXEMPT-task edge case for output-absent FAIL covered. | MET — R-3 routing re-evaluation, R-4 EXEMPT FP for output-absent covered. But drops RK-19 (Wave-4 parser regression) and RK-20 (live exec not validated) |
| C3 | Includes dependencies and prerequisites | MET — §9.x prior-art constraints + sub-section per constraint enumerate all v3.7 prereqs | MET — §9 captures the constraint by reference; less detail than A |
| C4 | Defines success/completion criteria | NOT MET — A defines candidates and risks but does not commit to ADOPT/DEFER/REJECT, so success criteria per candidate are inferable but not stated | MET — ADOPT/DEFER/REJECT verdicts per candidate define exactly what shipping success looks like |
| C5 | Specifies what is explicitly out of scope | MET — NG-1..NG-6 enumerated with citation | MET — Non-goals bulleted + B8/B9/B19/B20 REJECT candidates reinforce |
| **Subtotal** | | **4/5** | **5/5** |

### Correctness (5 criteria)

| # | Criterion | Variant A | Variant B |
|---|-----------|-----------|-----------|
| K1 | No factual errors or hallucinated claims | MET — every concrete claim cites file:line or extract; `[inference]` discipline isolates uncited claims | NOT MET — multiple uncited synthesis claims (Effort labels S/M/L without derivation; Owner assignments without source; Sev ratings without methodology). B does not distinguish cited from synthesized |
| K2 | Technical approaches are feasible with stated constraints | MET — every candidate cites its source extract with stated effort/risk per R3, R4, etc. | MET — candidates cite R-IDs and inherit feasibility from those extracts |
| K3 | Terminology used consistently and accurately throughout | MET — "MERGED / PARTIAL / NOT-YET" + "[inference]" + "BLOCKING constraint" — applied consistently | MET — "✅⚠❌🛑" + ADOPT/DEFER/REJECT + Blocking? Y/N — applied consistently |
| K4 | No internal contradictions | MET — IC metric 0.96; tensions framed as open questions | MET — IC 0.94; Q3 vs R-5 tension exists but does not contradict |
| K5 | Claims supported by evidence or rationale within the document | MET — citation discipline is the defining property of A | NOT MET — verdicts (ADOPT/DEFER/REJECT) are commit-to-action statements without source-extract chain to support each verdict beyond paraphrasing the candidate description |
| **Subtotal** | | **5/5** | **3/5** |

### Structure (5 criteria)

| # | Criterion | Variant A | Variant B |
|---|-----------|-----------|-----------|
| T1 | Logical section ordering (prerequisites before dependents) | MET — Scope → Source index → task-unified inventory → /sc:task inventory → overlap matrix → candidates → risks → questions → prior-art. Each section sets up the next | MET — Same ordering. Both drafts share the high-level architecture |
| T2 | Consistent hierarchy depth (no orphaned subsections) | MET — H3 subsections under §4, §6, §8, §9; no orphans | MET — Mostly flat; consistent within style choice |
| T3 | Clear separation of concerns between sections | MET — Inventory, comparison, recommendations, risks, decisions all in named sections | MET — Same. |
| T4 | Navigation aids present | NOT MET — A has section anchors but no TOC, no cross-section navigation; coverage-notes is a partial TOC | NOT MET — B has no TOC either; status legend at top is the only navigation aid |
| T5 | Follows conventions of the artifact type | MET — Release-report convention with traceability emphasis is consistent | MET — Release-report convention with decision-queue emphasis is consistent |
| **Subtotal** | | **4/5** | **4/5** |

### Clarity (5 criteria)

| # | Criterion | Variant A | Variant B |
|---|-----------|-----------|-----------|
| L1 | Unambiguous language (no "should consider", "might", "as appropriate") | MET — A flags ambiguity with `[inference]` tag and pushes vague claims to §8 open questions | MET — B prefers explicit verdicts (ADOPT/DEFER/REJECT) over hedging language |
| L2 | Concrete rather than abstract | MET — concrete file paths, line numbers, baseline numbers throughout | MET — Effort labels, status pills, owner names |
| L3 | Each section has a clear purpose | MET | MET |
| L4 | Acronyms and domain terms defined on first use | MET — TFEP, CEV, MCP, BLOCKED, etc. defined or contextualized in §4 | NOT MET — B uses TFEP, MCP, CEV without first-use definition (relies on reader familiarity) |
| L5 | Actionable next steps or decision points clearly identified | NOT MET — A's "decision points" are §8 open questions but none are flagged as blocking vs non-blocking. Reader cannot triage | MET — Blocking? column on §8 explicitly identifies Q1, Q3, Q4, Q8 as scope-boundary blockers |
| **Subtotal** | | **3/5** | **4/5** |

### Risk Coverage (5 criteria)

| # | Criterion | Variant A | Variant B |
|---|-----------|-----------|-----------|
| R1 | Identifies at least 3 risks with probability and impact assessment | MET — 20 risks each with Likelihood + Blast radius | MET — 12 risks each with Sev + Like + Blast radius |
| R2 | Provides mitigation strategy for each identified risk | MET — Mitigation hook per row | MET — Mitigation column per row |
| R3 | Addresses failure modes and recovery procedures | MET — RK-16 (telemetry-load-bearing consequences), RK-17 (broken references), RK-19 (prompt-template testing); §6 candidates have rollback consideration | MET — R-3, R-4, R-7 address fallback paths |
| R4 | Considers external dependencies and their failure scenarios | MET — RK-03 STRICT MCP unavailable; RK-15 v3.7 regression; RK-20 live-exec not validated | MET — R-11 Sequential+Serena degraded; R-1 v3.7 regression; but DROPS RK-20 |
| R5 | Includes monitoring or validation mechanism for risk detection | MET — `make verify-sync` (RK-05), `--reason "..."` justification (RK-04), telemetry consumer audit (RK-16) | MET — Same instruments cited via R-2, R-5, R-12 mitigation columns |
| **Subtotal** | | **5/5** | **5/5** |

### Invariant & Edge Case Coverage (5 criteria)

| # | Criterion | Variant A | Variant B |
|---|-----------|-----------|-----------|
| I1 | Addresses boundary conditions for collections (empty, single-element, maximum size) | MET — Q5 (CRITICAL FAIL "output absent" for EXEMPT? — boundary case); RK-13 (regex empty case) | MET — Q5 same EXEMPT boundary; R-4 |
| I2 | Handles state variable interactions across component boundaries | MET — §6 sprint-side candidates SE-002..SE-005 all interact with sprint-state; A's RK-19 calls out prompt-template format interaction | MET — B12-B16 same items; but B drops RK-19 explicit interaction risk |
| I3 | Identifies guard condition gaps | MET — TU-001 CRITICAL FAIL conditions are exactly guard-condition gaps; RK-07 calls out "behavioral vs programmatic" gate gap | MET — B1 TU-001 + R-7 same coverage |
| I4 | Covers count divergence scenarios | MET — Q12 keyword reconciliation across 4 locations is a count-divergence concern | MET — G6 + B10 same coverage |
| I5 | Considers interaction effects when features or components combine | MET — Q3 (output-type × tier interaction), Q9 (severity enum scope), Q6 (BLOCKED × `--skip-compliance` interaction) | MET — Q1 (output-type modifier vs parallel) explicitly probes the interaction; Q6 (`--skip-compliance` + BLOCKED) commits to a resolution |
| **Subtotal** | | **5/5** | **5/5** |

### Qualitative Summary

| Dimension | Variant A | Variant B |
|-----------|-----------|-----------|
| Completeness | 4/5 | 5/5 |
| Correctness | 5/5 | 3/5 |
| Structure | 4/5 | 4/5 |
| Clarity | 3/5 | 4/5 |
| Risk Coverage | 5/5 | 5/5 |
| Invariant & Edge Case | 5/5 | 5/5 |
| **Total** | **26/30** | **26/30** |

**qual_score_A = 26 / 30 = 0.867**
**qual_score_B = 26 / 30 = 0.867**

### Edge Case Floor Check

- Variant A: Invariant & Edge Case score = 5/5 ≥ 1/5 floor → ELIGIBLE
- Variant B: Invariant & Edge Case score = 5/5 ≥ 1/5 floor → ELIGIBLE

Both variants pass the floor.

---

## Position-Bias Mitigation (Dual-Pass)

Pass 1 (A then B) and Pass 2 (B then A) executed independently. Per-criterion comparison:

| Criterion | A Pass 1 | A Pass 2 | B Pass 1 | B Pass 2 | Disagreement | Final |
|-----------|----------|----------|----------|----------|--------------|-------|
| C4 | NOT MET | NOT MET | MET | MET | none | A=0, B=1 |
| K1 | MET | MET | NOT MET | NOT MET | none | A=1, B=0 |
| K5 | MET | MET | NOT MET | NOT MET | none | A=1, B=0 |
| L4 | MET | MET | NOT MET | NOT MET | none | A=1, B=0 |
| L5 | NOT MET | NOT MET | MET | MET | none | A=0, B=1 |

All other 25 criteria: both passes agreed (MET=MET or NOT MET=NOT MET). 0 disagreements requiring re-evaluation. **Position-bias-mitigated scores match the Pass 1 results.**

---

## Combined Scoring

- variant_score_A = (0.50 × 0.935) + (0.50 × 0.867) = 0.468 + 0.434 = **0.902**
- variant_score_B = (0.50 × 0.837) + (0.50 × 0.867) = 0.419 + 0.434 = **0.853**

**Margin:** 0.902 − 0.853 = 0.049 (4.9%)

This is within 5% of each other → **tiebreaker protocol triggered.**

---

## Tiebreaker Protocol

### Level 1: Debate performance

From the scoring matrix in debate-transcript.md:
- Variant A wins: 14 diff points (S-001, S-002, S-003, S-006, C-005, C-007, C-008, C-012, U-001..U-008, A-005)
- Variant B wins: 14 diff points (S-004, C-002, C-003, C-004, C-006, C-009, C-010, C-011, X-001, U-009..U-012, A-003)
- Tie/Merge: 4 (S-005, C-001, A-001 unresolved, A-002 unresolved, A-004 tie)

Debate performance count: **A = 14, B = 14 → TIE at Level 1**

### Level 2: Correctness count

- Variant A Correctness criteria MET: 5/5 (K1, K2, K3, K4, K5)
- Variant B Correctness criteria MET: 3/5 (K2, K3, K4 — failing on K1 hallucination protection and K5 evidence-to-verdict chain)

**A has higher correctness count: 5 > 3 → Variant A wins at Level 2.**

Rationale: Correctness is the most valuable rubric dimension for hallucination detection (per scoring-protocol.md). A's `[inference]` discipline and per-claim citation chain are exactly the properties the adversarial pipeline is meant to reward.

---

## Selected Base: Variant 1 (Draft A — completeness/traceability)

### Selection Rationale

Variant A wins on combined score (0.902 vs 0.853) and decisively wins the tiebreaker on Correctness (5/5 vs 3/5). The decisive factor is Correctness criterion K1 (no factual errors or hallucinated claims): A's `[inference]` tagging discipline and per-claim file:line citations are exactly the properties the adversarial pipeline is designed to reward. Selecting A as base means the merged artifact inherits hallucination-prevention machinery that cannot be retrofitted onto B without rewriting B to A's evidence density.

This selection is also strongly supported by the calling brief: "preserve traceability from A while inheriting decision pills/recommendations from B." The brief explicitly treats A as the structural backbone.

### Strengths to Preserve (from base = A)

1. **`[inference]` tagging convention** (15+ uses throughout) — anti-hallucination guard. Must remain.
2. **47-row overlap matrix O1-O47** with per-row source citations + gap/delta column. Full retention.
3. **§9.x prior-art constraint subsections** (§9.1-§9.9) — specifically §9.5 (v3.7 test baselines: 921 passed, 57 failed; TUI 125/125; test_process 16/16) and §9.7 (Wave-4 checkpoint parser regression). Retain in full.
4. **Coverage-notes self-check section** with Known gaps list. Retain and update to reflect post-merge state.
5. **Source index with absolute paths + line ranges** (18 entries). Retain.
6. **TU-006 candidate** (materialize missing skill sub-files). Retain.
7. **Q11 telemetry/escape-hatch metering** and **Q13 v3.7 unfinished follow-ups** open questions. Retain.
8. **Full risk register RK-01..RK-20**. Retain RK-19 (Wave-4 prompt-template testing) and RK-20 (v3.7 live-exec not validated) as B's advocate conceded. Move RK-13, RK-14, RK-18 to an "Out-of-scope risks (for traceability)" appendix per debate compromise.

### Strengths to Incorporate (from non-base = B)

1. **ADOPT / DEFER / REJECT verdict pills** on every candidate (B1-B20 mapped to TU-/SE- IDs). Apply to A's §6 candidate inventory. Marked `[inference]` where verdict is synthesized rather than directly source-cited.
2. **Effort labels S / M / L** per candidate. Apply to A's §6 candidate list. Marked `[inference]`.
3. **Owner column** in risk register (Lead / Tier owner / Skill owner / Sprint owner / DevOps / Ops / Quality agent owner). Apply to A's §7. Marked `[inference]`.
4. **Sev / Like split** in risk register replacing A's single Likelihood column. Apply to A's §7.
5. **Status legend** (✅ adopted / ⚠ partial / ❌ missing / 🛑 blocked) on overlap matrix. Apply as a status-pill column on A's §5 matrix where the status is more nuanced than MERGED/PARTIAL/NOT-YET.
6. **Blocking? Y/N flag** on open questions. Apply to A's §8. 4 questions flagged Blocking per B's Q1, Q3, Q4, Q8.
7. **Options + Recommendation pattern** on open questions. Apply to A's §8 to convert exploratory questions into decision-ready questions.
8. **Q6 explicit resolution** ("`--skip-compliance` can override BLOCKED with `--reason`, audited"). Apply to A's Q6 as a recommendation block while preserving A's question framing.
9. **Q8 explicit release-split commitment** (sprint-side SE-/B12-B18 as sibling release). Apply to A's §9.3 R1/R2 split discussion as a committed recommendation.
10. **REJECT candidates as table rows** (B8 / B9 / B19 / B20). Map B8 → TU-NG1 alongside A's NG-1; B9 → TU-NG2; B19/B20 → TU-NG3. Add as a "Rejected candidates (for transparency)" subsection under §6 rather than burying in non-goals only.
11. **TL;DR sentence** at top of §1 from B's draft. Replace A's longer §1.1 opener.

### Strengths NOT Incorporated (rationale)

1. **B's 21-row overlap matrix C1-C21**: A's 47-row matrix is a proper superset. Keep A's matrix; do not adopt B's row scheme. This is per debate evidence: B's advocate conceded A's matrix is more comprehensive.
2. **B's compression to 207 lines**: The merge will end up longer than B (estimated 700-900 lines) because it adds B's decision instruments to A's evidence backbone. Compression itself is not preserved as a target.
3. **B's H1-H10 historical strengths table format**: A's §3 has equivalent content distributed across §3.1-§3.4 with deeper citations. Keep A's structure; do not flatten.
4. **B's collapse of Q1+Q2 into Q3**: Debate resolution C-007 keeps A's split because A's Q2 surfaces the `/sc:forensic` consumer enumeration uncertainty B's collapse hides.
