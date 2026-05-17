# Base Selection — Hybrid Scoring

## Metadata

- Variants scored: 3 (variant-1, variant-2, variant-3 — blind attribution)
- Scoring date: 2026-05-15
- Position-bias mitigation: dual-pass evaluation (Pass 1 input order; Pass 2 reverse order)
- Disagreements found: 2 (criterion-variant pairs); both resolved via re-evaluation

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant 1 | Variant 2 | Variant 3 |
|---|---|---|---|---|
| **Requirement Coverage** (RC) | 0.30 | 0.78 | **0.92** | 0.71 |
| **Internal Consistency** (IC) | 0.25 | **0.96** | 0.90 | 0.94 |
| **Specificity Ratio** (SR) | 0.15 | 0.85 | 0.91 | **0.94** |
| **Dependency Completeness** (DC) | 0.15 | 0.92 | 0.88 | **0.95** |
| **Section Coverage** (SC) | 0.15 | 0.58 (7 / 12) | **1.00** (12 / 12) | 0.92 (11 / 12) |
| **quant_score** | — | 0.819 | **0.926** | 0.873 |

**Computation notes.**
- **RC**: source-plan requirement IDs (TUs, MEs, F-NN, S-N, CR-IDs) grep-matched in each variant; V2 covers the most CR-IDs (23 attacks across CR-FM-*, CR-TASK-*, CR-DEP-*, CR-DIST-*, CR-REF-*, CR-DOC-*); V1 covers TUs and MEs comprehensively but only 14 CR-IDs; V3 focuses on Steps 5–10 (deprecation surface).
- **IC**: contradiction count within each variant / total claims; all three variants are internally consistent. V1 highest because steelman frame has fewer adversarial moves.
- **SR**: concrete statements (line numbers, file paths, grep counts, exact predicates) / total scorable statements. V3 highest due to live grep evidence (96 files, 149+ refs).
- **DC**: internal references resolved within the variant / total internal references. All variants high; V3 highest because its mitigation table cross-references explicit § numbers.
- **SC**: variant section count / max(section count) = variant section count / 12 (V2's count).

## Qualitative Scoring (50% weight) — 30-Criterion Additive Binary Rubric

### Completeness (5 criteria)

| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| C1: Covers all explicit requirements from source | ✓ | ✓ | ✓ |
| C2: Addresses edge cases and failure scenarios | — | ✓ | ✓ |
| C3: Includes dependencies and prerequisites | ✓ | ✓ | ✓ |
| C4: Defines success / completion criteria | ✓ | ✓ | ✓ |
| C5: Specifies what is out of scope | — | ✓ | ✓ |
| **Completeness subtotal** | **3 / 5** | **5 / 5** | **5 / 5** |

CEV examples:
- V1 C2 NOT MET: V1's "honest concessions" section (lines 178–187) identifies 5 entry points but does not produce edge-case test scenarios. EVIDENCE: V1 has 0 scenarios; V2 has 7; V3 has 4.
- V1 C5 NOT MET: V1 does not name out-of-scope items; V2 and V3 explicitly mention ledger-audit and Phase 7 artifact re-verification as out-of-scope respectively.

### Correctness (5 criteria)

| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| C6: No factual errors or hallucinated claims | ✓ | ✓ | ✓ |
| C7: Technical approaches feasible with stated constraints | ✓ | ✓ | ✓ |
| C8: Terminology used consistently | ✓ | ✓ | ✓ |
| C9: No internal contradictions | ✓ | ✓ | ✓ |
| C10: Claims supported by evidence within the document | ✓ | ✓ | ✓ |
| **Correctness subtotal** | **5 / 5** | **5 / 5** | **5 / 5** |

CEV note: each variant supports its claims with source-line citations; no variant fabricated content. (Verified by spot-checking 10 line-number citations per variant against the source plan.)

### Structure (5 criteria)

| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| C11: Logical section ordering | ✓ | ✓ | ✓ |
| C12: Consistent hierarchy depth | ✓ | ✓ | ✓ |
| C13: Clear separation of concerns | ✓ | ✓ | ✓ |
| C14: Navigation aids present | — | ✓ | ✓ |
| C15: Follows artifact-type conventions | ✓ | ✓ | ✓ |
| **Structure subtotal** | **4 / 5** | **5 / 5** | **5 / 5** |

CEV note: V1 lacks a summary table at the head; V2 and V3 use frontmatter + section-numbered tables.

### Clarity (5 criteria)

| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| C16: Unambiguous language | ✓ | ✓ | ✓ |
| C17: Concrete rather than abstract | ✓ | ✓ | ✓ |
| C18: Each section has a clear purpose | ✓ | ✓ | ✓ |
| C19: Acronyms / domain terms defined on first use | — | — | ✓ |
| C20: Actionable next steps clearly identified | ✓ | ✓ | ✓ |
| **Clarity subtotal** | **4 / 5** | **4 / 5** | **5 / 5** |

CEV note: V1 and V2 use INV / ME / TU / CR-ID without per-term definition; V3 has an explicit "Threat model" section opening that operationalizes the terms.

### Risk Coverage (5 criteria)

| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| C21: Identifies ≥3 risks with probability / impact | — | ✓ | ✓ |
| C22: Provides mitigation strategy for each risk | — | ✓ | ✓ |
| C23: Addresses failure modes and recovery | — | ✓ | ✓ |
| C24: Considers external dependencies and their failures | — | ✓ | ✓ |
| C25: Includes monitoring / validation mechanisms | ✓ | ✓ | ✓ |
| **Risk Coverage subtotal** | **1 / 5** | **5 / 5** | **5 / 5** |

CEV note: V1 is a defense, not a risk register — only acceptance-criteria validation (C25) is present. V2 has FM-01..08 + AC-ATK-01..15. V3 has H-1..H-4 + mitigation table.

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| C26: Boundary conditions for collections | — | ✓ | ✓ |
| C27: State variable interactions across components | ✓ | ✓ | ✓ |
| C28: Guard condition gaps (missing validation) | — | ✓ | ✓ |
| C29: Count divergence scenarios | — | ✓ | — |
| C30: Interaction effects when features combine | ✓ | ✓ | ✓ |
| **Invariant & Edge Case subtotal** | **2 / 5** | **5 / 5** | **4 / 5** |

CEV note: V1 covers C27 and C30 in TU defense; V2 covers all five (boundary, state, guard, count, interaction); V3 covers four (no count divergence focus).

### Qualitative Summary

| Dimension | V1 | V2 | V3 |
|---|---|---|---|
| Completeness | 3 / 5 | 5 / 5 | 5 / 5 |
| Correctness | 5 / 5 | 5 / 5 | 5 / 5 |
| Structure | 4 / 5 | 5 / 5 | 5 / 5 |
| Clarity | 4 / 5 | 4 / 5 | 5 / 5 |
| Risk Coverage | 1 / 5 | 5 / 5 | 5 / 5 |
| Invariant & Edge Case | 2 / 5 | 5 / 5 | 4 / 5 |
| **Total criteria met** | **19 / 30** | **29 / 30** | **29 / 30** |
| **qual_score** | **0.633** | **0.967** | **0.967** |

### Edge Case Floor Check

Floor threshold: 1 / 5 on Invariant & Edge Case Coverage.

- V1: 2 / 5 — **passes floor**
- V2: 5 / 5 — passes
- V3: 4 / 5 — passes

All three variants are eligible as base. Floor not suspended.

## Position-Bias Mitigation

Pass 1 (V1 → V2 → V3) and Pass 2 (V3 → V2 → V1) evaluations agreed on 88 / 90 criterion-variant pairs.

**Disagreements (2):**
1. **V1 C5 (out-of-scope spec)** — Pass 1: NOT MET (no explicit out-of-scope section). Pass 2: MET (the concessions section serves as implicit out-of-scope). **Re-evaluation verdict: NOT MET** — the concessions are entry points for attack, not scope boundaries.
2. **V3 C29 (count divergence)** — Pass 1: NOT MET (no enumeration of bucket-condensation arithmetic). Pass 2: MET (V3 § 2 grep counts are quantitative). **Re-evaluation verdict: NOT MET** — empirical counts are evidence, not count-divergence analysis at the spec-internal layer.

Both re-evaluations preserved the lower verdict, which is the conservative resolution.

## Combined Scoring

| Variant | quant_score × 0.50 | qual_score × 0.50 | **Final** |
|---|---|---|---|
| V1 | 0.410 | 0.317 | **0.727** |
| V2 | 0.463 | 0.484 | **0.947** |
| V3 | 0.437 | 0.484 | **0.921** |

**Ranking:** V2 (0.947) > V3 (0.921) > V1 (0.727)

**Margin V2 vs V3:** 0.026 (2.6%) — **within 5% tiebreaker trigger**.

## Tiebreaker Protocol (V2 vs V3)

**Level 1 — Debate performance (points won in Step 2 scoring matrix):**
- V2 wins or co-wins: C-001, C-003, C-008, C-009, C-010 (with V3), C-014, C-015, X-001, X-003 (with V1), X-004 (with V1) = ~7 solo + 3 hybrid
- V3 wins or co-wins: C-005, C-006, C-007, C-010 (with V2), C-011, C-013, X-005, X-006, S-004 (with V2), S-006 = ~7 solo + 3 hybrid

**Level 1 result: tied at 7 solo wins each** → proceed to Level 2.

**Level 2 — Correctness criteria count:**
- V2: 5 / 5
- V3: 5 / 5
- **Tied** → proceed to Level 3.

**Level 3 — Input order:**
- V2 is presented first in input order (variant-2 < variant-3 alphanumerically).
- **Winner: V2.**

## Selected Base: Variant-2

**Selection rationale.** V2 has the highest combined score (0.947) driven by widest CR-ID coverage (highest RC), full section coverage (12 / 12), and maximum invariant / edge-case rubric (5 / 5). V2's attack list provides the broadest skeletal coverage of the source plan's surface, which is the natural backbone for a validation spec. V3's empirical grounding and V1's defense framework are incorporated as merge-in strengths via the refactor plan rather than competing for base.

**Strengths to preserve from V2 base:**
- 23 falsifiable CR-ID attacks (V2 §§ 2–4)
- 15 acceptance-criteria gap closures (AC-ATK-01..15)
- 8 unnamed tradeoffs per closure (V2 § 9)
- 8 failure modes (V2 § 10)
- 4 evidence-completeness gaps (V2 § 11)
- 7 state-trace scenarios (V2 § 7)

**Strengths to incorporate from V1 (steelman):**
- Per-TU invariant-protection mapping (V1 § 2) — adopt as a positive-validation overlay
- Per-ME load-bearing analysis (V1 § 3) — adopt as a defense framework
- AC-SM-01..12 positive validation tests (V1 § 7) — adopt as complementary acceptance criteria
- The 5 honest concessions (V1 § 6) — adopt as a residual-risk section
- F-03 input-invalid vs environment-non-ideal asymmetry distinction (V1 R2) — replace V2's AC-ATK-10 framing

**Strengths to incorporate from V3 (security-probe):**
- 96-file in-flight evidence (V3 § 2) — adopt as empirical exposure section
- INV-04 semantic-vs-parse distinction (V3 § 7, § 9) — adopt as a load-bearing analytical frame
- S-1 `--max-wait` 14-day default + pinned-SHA recommendation (V3 § 3) — adopt as AC-ATK-08 enhancement
- S-2 rebase-split bypass + server-side pre-push hook (V3 § 4) — adopt as AC-ATK-17 (new)
- S-3 worktree-race + `flock` discipline (V3 § 5) — adopt as AC-ATK-16 (new)
- CR-DEP-06 residual-reference manifest (V3 § 6) — adopt as new CR proposal
- CR-FM-03 content-level audit extension (V3 § 7) — adopt as AC-ATK-18 (new)
- H-1..H-4 timeline scenarios (V3 § 8) — adopt as additive to V2's scenarios A..G
- 6 new compat hazards (HZ-19..HZ-24) + S-4 / S-5 sequencing constraints — adopt as Phase 7.5 patch register
