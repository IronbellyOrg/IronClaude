# Base Selection: Hybrid Scoring & Winner Determination

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant A (Claude) | Variant B (GPT) |
|--------|--------|-------------------|-----------------|
| Requirement Coverage (RC) | 0.30 | 0.85 — covers FR-1.1-1.18, FR-2.1-2.4, FR-3.x, FR-4.x, FR-5.x, FR-6.x, FR-7.x; misses FR-7.1/7.3 conflicts | 0.82 — covers same FRs; catches FR-7.1/7.3 conflicts but misses NSD-001 |
| Internal Consistency (IC) | 0.25 | 0.78 — D1 100% contradicts later [ADV] MISSING findings; 84-count inflated | 0.90 — no internal contradictions; scores consistent with findings |
| Specificity Ratio (SR) | 0.15 | 0.88 — specific line citations, exact counts, named agents | 0.85 — specific line citations, but fewer agent breakdowns |
| Dependency Completeness (DC) | 0.15 | 0.92 — all cross-references resolve; agent index complete | 0.82 — cross-references present but agent files only listed, not detailed |
| Section Coverage (SC) | 0.15 | 1.00 — 9 sections (max) | 0.78 — 7 sections |

**Quantitative Scores**:
- **Variant A**: (0.85×0.30) + (0.78×0.25) + (0.88×0.15) + (0.92×0.15) + (1.00×0.15) = 0.255 + 0.195 + 0.132 + 0.138 + 0.150 = **0.870**
- **Variant B**: (0.82×0.30) + (0.90×0.25) + (0.85×0.15) + (0.82×0.15) + (0.78×0.15) = 0.246 + 0.225 + 0.128 + 0.123 + 0.117 = **0.839**

---

## Qualitative Scoring (50% weight) — 30-Criterion Binary Rubric

### Completeness (5 criteria)

| # | Criterion | Variant A | Variant B |
|---|-----------|-----------|-----------|
| 1 | Covers all explicit requirements from source input | NOT MET — misses FR-7.1/7.3 conflicts | NOT MET — misses NSD-001 ambiguity |
| 2 | Addresses edge cases and failure scenarios | MET — adversarial pass catches 4 MISSING FRs | MET — catches FR-7.1/7.3 + FR-5.2 positive-case |
| 3 | Includes dependencies and prerequisites | MET — phase dependencies documented | MET — cross-cutting concern dependencies noted |
| 4 | Defines success/completion criteria | MET — verdict criteria table with thresholds | MET — verdict criteria table |
| 5 | Specifies what is explicitly out of scope | NOT MET — no scope section | NOT MET — no scope section |

**A: 3/5, B: 3/5**

### Correctness (5 criteria)

| # | Criterion | Variant A | Variant B |
|---|-----------|-----------|-----------|
| 1 | No factual errors or hallucinated claims | NOT MET — D1 100% contradicts adversarial findings; 84-count inflated | MET — no provably false claims |
| 2 | Technical approaches are feasible | MET — all recommended fixes are actionable | MET — all recommended fixes are actionable |
| 3 | Terminology used consistently | MET — consistent throughout | MET — consistent throughout |
| 4 | No internal contradictions | NOT MET — D1 score vs [ADV] findings | MET — scores consistent with gap registry |
| 5 | Claims supported by evidence | MET — line citations, spec references | MET — line citations, spec references |

**A: 3/5, B: 5/5**

### Structure (5 criteria)

| # | Criterion | Variant A | Variant B |
|---|-----------|-----------|-----------|
| 1 | Logical section ordering | MET — summary → domains → gaps → CC → integration → metrics | MET — summary → domains → gaps → CC → integration |
| 2 | Consistent hierarchy depth | MET — uniform H2/H3 nesting | MET — uniform H2/H3 nesting |
| 3 | Clear separation of concerns | MET — domains, CC agents, integration cleanly separated | NOT MET — Reachability merged with Audit conflates domains |
| 4 | Navigation aids present | MET — agent reports index, domain table | NOT MET — agent files listed without hyperlinks or descriptions |
| 5 | Follows conventions of artifact type | MET — standard validation report structure | MET — standard validation report structure |

**A: 5/5, B: 3/5**

### Clarity (5 criteria)

| # | Criterion | Variant A | Variant B |
|---|-----------|-----------|-----------|
| 1 | Unambiguous language | MET — specific verdicts per requirement | MET — specific verdicts per finding |
| 2 | Concrete rather than abstract | MET — exact line numbers, task IDs | MET — exact line numbers, spec references |
| 3 | Each section has clear purpose | MET | MET |
| 4 | Acronyms and domain terms defined | NOT MET — CC, D1-D7 not defined at first use | NOT MET — FR, SC, NFR not defined |
| 5 | Actionable next steps clearly identified | MET — "Recommended fix" per gap | MET — "Recommended correction" per gap |

**A: 4/5, B: 4/5**

### Risk Coverage (5 criteria)

| # | Criterion | Variant A | Variant B |
|---|-----------|-----------|-----------|
| 1 | Identifies at least 3 risks | MET — 6 HIGH, 5 MEDIUM gaps = risk identification | MET — 7 HIGH, 6 MEDIUM gaps |
| 2 | Provides mitigation for each risk | MET — recommended fix per gap | MET — recommended correction per gap |
| 3 | Addresses failure modes | MET — adversarial pass catches false negatives | NOT MET — no explicit false-negative methodology |
| 4 | Considers external dependencies | NOT MET — no analysis of upstream branch stability | NOT MET — no analysis of upstream dependencies |
| 5 | Includes monitoring/validation mechanism | MET — CC agents provide cross-validation layer | NOT MET — no explicit cross-validation methodology |

**A: 4/5, B: 2/5**

### Invariant & Edge Case Coverage (5 criteria)

| # | Criterion | Variant A | Variant B |
|---|-----------|-----------|-----------|
| 1 | Addresses boundary conditions | MET — FR-3.2 budget exhaustion scenarios verified | MET — budget exhaustion noted |
| 2 | Handles state variable interactions | MET — cross-path coherence (FR-2.4) verified | NOT MET — cross-path not separately analyzed |
| 3 | Identifies guard condition gaps | MET — _run_checkers() registry gap noted | MET — FR-7.3 flush guard gap identified |
| 4 | Covers count divergence | NOT MET — 84-count not validated against ground truth | MET — identifies "13 requirements" count issue (GAP-H007) |
| 5 | Considers interaction effects | MET — CC3 dependency/ordering agent checks interactions | NOT MET — no explicit interaction analysis |

**A: 4/5, B: 3/5**

### Qualitative Summary

| Dimension | Variant A | Variant B |
|-----------|-----------|-----------|
| Completeness | 3/5 | 3/5 |
| Correctness | 3/5 | 5/5 |
| Structure | 5/5 | 3/5 |
| Clarity | 4/5 | 4/5 |
| Risk Coverage | 4/5 | 2/5 |
| Invariant & Edge Case | 4/5 | 3/5 |
| **Total** | **23/30** | **20/30** |

**Qualitative Scores**:
- **Variant A**: 23/30 = **0.767**
- **Variant B**: 20/30 = **0.667**

### Edge Case Floor Check

- Variant A: 4/5 on Invariant & Edge Case → **Eligible**
- Variant B: 3/5 on Invariant & Edge Case → **Eligible**

---

## Position-Bias Mitigation

| Dimension | A (Pass 1) | A (Pass 2) | Agree? | B (Pass 1) | B (Pass 2) | Agree? |
|-----------|-----------|-----------|--------|-----------|-----------|--------|
| Completeness | 3/5 | 3/5 | Yes | 3/5 | 3/5 | Yes |
| Correctness | 3/5 | 3/5 | Yes | 5/5 | 5/5 | Yes |
| Structure | 5/5 | 5/5 | Yes | 3/5 | 3/5 | Yes |
| Clarity | 4/5 | 4/5 | Yes | 4/5 | 4/5 | Yes |
| Risk Coverage | 4/5 | 4/5 | Yes | 2/5 | 2/5 | Yes |
| Invariant | 4/5 | 4/5 | Yes | 3/5 | 3/5 | Yes |

Disagreements found: 0. No re-evaluation needed.

---

## Combined Scoring

| Component | Weight | Variant A | Variant B |
|-----------|--------|-----------|-----------|
| Quantitative | 0.50 | 0.870 | 0.839 |
| Qualitative | 0.50 | 0.767 | 0.667 |
| **Combined** | | **0.819** | **0.753** |

**Margin**: 6.6% (above 5% tiebreaker threshold)

---

## Selected Base: Variant A (Claude Report)

### Selection Rationale

Variant A wins on combined scoring (0.819 vs 0.753) driven by superior structure (5/5 vs 3/5), risk coverage (4/5 vs 2/5), and invariant analysis (4/5 vs 3/5). Its 7-domain decomposition, 11-agent methodology, REJECTED findings section, and adversarial [ADV] tagging provide a stronger foundation for a merged report.

**However**, Variant A has two critical weaknesses that the merge MUST address:
1. Missing FR-7.1/7.3 spec-roadmap conflicts (Variant B's highest-value unique contributions)
2. D1 domain score (100%) contradicts its own adversarial findings
3. Inflated 84-requirement count needs correction

### Strengths to Preserve from Base (Variant A)
- 7-domain + 4 cross-cutting agent decomposition
- [ADV]-tagged adversarial findings with clear discovery provenance
- REJECTED findings section with adjudication rationale
- NEEDS-SPEC-DECISION section
- Integration wiring audit format (9 points)
- Aggregate metrics section with confidence interval

### Strengths to Incorporate from Variant B
1. **GAP-H005**: FR-7.1 schema conflict (`duration_ms` omitted from roadmap) — incorporate as new HIGH gap
2. **GAP-H006**: FR-7.3 flush semantics conflict (session-end vs per-test) — incorporate as new HIGH gap
3. **GAP-H007**: Boundary/count inconsistency ("13 requirements" claim) — incorporate as MEDIUM gap
4. **GAP-M002**: FR-5.2 positive-case testing gap — incorporate as MEDIUM gap
5. **GAP-M003/M004**: FR-6.1/6.2 specificity critique — incorporate as LOW notes
6. **Internal consistency fix**: Correct D1 domain score from 100% to reflect adversarial MISSING findings
7. **Requirement count fix**: Revise from 84 to ~65 (47 FRs + 12 SCs + 6 constraints)
8. **Integration wiring**: Change `_run_checkers()` from FULLY_WIRED to PARTIALLY_WIRED
