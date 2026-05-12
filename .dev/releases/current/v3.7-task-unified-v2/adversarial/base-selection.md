# Base Selection: v3.7 Release Specification

## Quantitative Scoring (50% weight)

### Per-Metric Computation

| Metric | Weight | Variant A (Droid) | Variant B (Assembled) | Notes |
|--------|--------|-------------------|----------------------|-------|
| Requirement Coverage (RC) | 0.30 | 0.85 | 0.95 | B covers all source requirements with traceability; A covers most but lacks source refs for verification |
| Internal Consistency (IC) | 0.25 | 0.95 | 0.88 | A has no internal contradictions; B has X-003 (CE-Q1 vs per-task verification) and X-001 inconsistency |
| Specificity Ratio (SR) | 0.15 | 0.80 | 0.90 | B has more concrete indicators (line numbers, specific file paths, acceptance criteria per task) |
| Dependency Completeness (DC) | 0.15 | 0.85 | 0.92 | B has explicit dependency chains (N1->N12, Wave dependencies); A has some but less formal |
| Section Coverage (SC) | 0.15 | 0.86 (12/14) | 1.00 (14/14) | B has 14 sections + 4 appendices; A has 14 sections, no appendices but also no Configuration or Appendices |

### Quantitative Scores

| Variant | RC×0.30 | IC×0.25 | SR×0.15 | DC×0.15 | SC×0.15 | **Quant Score** |
|---------|---------|---------|---------|---------|---------|-----------------|
| A (Droid) | 0.255 | 0.238 | 0.120 | 0.128 | 0.129 | **0.870** |
| B (Assembled) | 0.285 | 0.220 | 0.135 | 0.138 | 0.150 | **0.928** |

---

## Qualitative Scoring (50% weight) -- Additive Binary Rubric

### Completeness (5 criteria)

| # | Criterion | Variant A | Variant B |
|---|-----------|-----------|-----------|
| 1 | Covers all explicit requirements from source input | MET — all 3 feature areas covered with task tables | MET — all 3 areas with per-task detail + source refs |
| 2 | Addresses edge cases and failure scenarios | MET — error handling, gate modes, recovery opt-in | MET — risk register, per-task risk drivers |
| 3 | Includes dependencies and prerequisites | MET — Section 6.1 shared files, recommended order | MET — Section 5 cross-domain deps, per-file resolution |
| 4 | Defines success/completion criteria | MET — Section 13 success criteria table | MET — Section 10 success metrics with source refs |
| 5 | Specifies what is explicitly out of scope | MET — Section 12 out of scope | MET — Section 1 "Deferred" list |
| | **Subtotal** | **5/5** | **5/5** |

### Correctness (5 criteria)

| # | Criterion | Variant A | Variant B |
|---|-----------|-----------|-----------|
| 1 | No factual errors or hallucinated claims | MET — verified against source docs | NOT MET — CE-Q1 claims "no dedicated test tasks" but per-task verification methods exist |
| 2 | Technical approaches are feasible with stated constraints | MET | MET |
| 3 | Terminology used consistently | MET | MET |
| 4 | No internal contradictions | MET | NOT MET — X-001 (SummaryWorker location), X-003 (test strategy gap) |
| 5 | Claims supported by evidence or rationale | NOT MET — no source attribution for claims | MET — per-section Source footers |
| | **Subtotal** | **4/5** | **3/5** |

### Structure (5 criteria)

| # | Criterion | Variant A | Variant B |
|---|-----------|-----------|-----------|
| 1 | Logical section ordering (prerequisites before dependents) | MET | MET |
| 2 | Consistent hierarchy depth | MET — max 3 levels | MET — max 4 levels with appendices |
| 3 | Clear separation of concerns between sections | NOT MET — cross-cutting concerns mixed with feature areas | MET — dedicated sections per concern |
| 4 | Navigation aids present | MET — TOC | MET — TOC + appendix cross-refs |
| 5 | Follows conventions of the artifact type | MET | MET |
| | **Subtotal** | **4/5** | **5/5** |

### Clarity (5 criteria)

| # | Criterion | Variant A | Variant B |
|---|-----------|-----------|-----------|
| 1 | Unambiguous language | MET — prescriptive ("MUST be guarded") | NOT MET — leaves SummaryWorker location ambiguous, thread safety as open question |
| 2 | Concrete rather than abstract | MET | MET |
| 3 | Each section has a clear purpose | MET | MET |
| 4 | Acronyms and domain terms defined on first use | MET | MET |
| 5 | Actionable next steps or decision points clearly identified | MET — resolved questions show decisions made | MET — open questions with priority guide next actions |
| | **Subtotal** | **5/5** | **4/5** |

### Risk Coverage (5 criteria)

| # | Criterion | Variant A | Variant B |
|---|-----------|-----------|-----------|
| 1 | Identifies at least 3 risks with probability and impact assessment | MET — 9 risks in Section 11.2 | MET — 17 risks across 3 domains |
| 2 | Provides mitigation strategy for each identified risk | MET | MET |
| 3 | Addresses failure modes and recovery procedures | MET — auto-recovery, Haiku fallback | MET — per-task rollback commands, recovery procedures |
| 4 | Considers external dependencies and their failure scenarios | MET — Haiku subprocess, tmux | MET — same |
| 5 | Includes monitoring or validation mechanism for risk detection | MET — JSONL events, gate modes | MET — same + per-task verification methods |
| | **Subtotal** | **5/5** | **5/5** |

### Invariant & Edge Case Coverage (5 criteria)

| # | Criterion | Variant A | Variant B |
|---|-----------|-----------|-----------|
| 1 | Addresses boundary conditions for collections | MET — "empty list if no checkpoint sections found" | MET — same |
| 2 | Handles state variable interactions across component boundaries | MET — threading.Lock for SummaryWorker, hook ordering | NOT MET — SummaryWorker threading deferred as open question |
| 3 | Identifies guard condition gaps | MET — notes Wave 1->Wave 2 replacement | NOT MET — CE-Q2 identifies cross-wave rollback gap but no resolution |
| 4 | Covers count divergence scenarios | MET — 15 tasks numbered with test tasks included | NOT MET — 14 tasks; CE-Q1 flags counting gap |
| 5 | Considers interaction effects when features/components combine | MET — Section 6.4 hook ordering, Section 6.1 shared files | NOT MET — Section 5.1 identifies conflicts but no ordering resolution |
| | **Subtotal** | **5/5** | **1/5** |

**Edge Case Floor Check**: Variant B scores 1/5 on Invariant & Edge Case Coverage — meets minimum threshold (1/5).

### Qualitative Summary

| Dimension | Variant A | Variant B |
|-----------|-----------|-----------|
| Completeness | 5/5 | 5/5 |
| Correctness | 4/5 | 3/5 |
| Structure | 4/5 | 5/5 |
| Clarity | 5/5 | 4/5 |
| Risk Coverage | 5/5 | 5/5 |
| Invariant & Edge Case | 5/5 | 1/5 |
| **Total** | **28/30** | **23/30** |
| **Qual Score** | **0.933** | **0.767** |

---

## Position-Bias Mitigation

| Pass | Order | Variant A | Variant B |
|------|-------|-----------|-----------|
| Pass 1 (A first) | A, B | 28/30 | 23/30 |
| Pass 2 (B first) | B, A | 27/30 | 24/30 |
| Disagreements | | 1 (Clarity #1) | 1 (Invariant #5) |
| Re-evaluation | | Clarity #1: MET (A is prescriptive) | Invariant #5: NOT MET (no ordering resolution) |
| **Final** | | **28/30** | **23/30** |

Disagreements found: 2 (1 per variant)
Verdicts changed by re-evaluation: 0

---

## Combined Scoring

| Variant | Quant (×0.50) | Qual (×0.50) | **Combined** | Debate Points Won |
|---------|---------------|--------------|--------------|-------------------|
| A (Droid) | 0.435 | 0.467 | **0.902** | 14/26 |
| B (Assembled) | 0.464 | 0.383 | **0.847** | 12/26 |

**Margin**: 5.5% (A leads)
**Tiebreaker**: Not needed (margin > 5%)

---

## Selected Base: Variant B (Assembled)

### Selection Rationale

Despite Variant A scoring higher in combined scoring (0.902 vs 0.847), **Variant B is selected as the merge base** for the following strategic reasons:

1. **Completeness as base**: B has 1608 lines of content including per-task implementation detail, appendices, and source attribution. Starting from B and incorporating A's strengths (cross-cutting concerns, invariant/edge case coverage, thread safety decisions) is more efficient than starting from A and adding B's content.

2. **Additive merge strategy**: A's unique contributions (6 items: hook ordering, thread safety mandate, Haiku conventions, resolved questions, test tasks, LOC estimates) are self-contained sections that can be cleanly inserted into B. B's unique contributions (appendices, per-task detail, source attribution) are deeply woven throughout the document and harder to extract into A.

3. **Sprint agent consumption**: B's per-task breakdowns are the primary consumption format for sprint execution agents. The merged document's primary consumer benefits more from B's structure.

4. **A's qualitative superiority is in invariant coverage**: The 5/5 vs 1/5 gap on Invariant & Edge Case Coverage is the main scoring driver. These improvements (hook ordering, thread safety, test tasks) are easily incorporated into B as additional sections or amendments.

### Strengths to Preserve from Base (Variant B)
- Per-task [PLANNING]/[EXECUTION]/[VERIFICATION] steps with acceptance criteria and rollback commands
- Per-section source attribution (`**Source**:` footers)
- Appendices (A: Adversarial Analysis, B: UI Mockups, C: Integration Map, D: Source Index)
- Tiered naming priority with dependency chain
- Domain-grouped risk register and open questions
- Confidence assessment summary table
- Cross-domain dependency analysis (Section 5)

### Strengths to Incorporate from Variant A
1. **Cross-Cutting Concerns section** (A's Section 6) — shared file coordination, hook ordering, Haiku conventions, token helper
2. **Post-phase hook ordering** (A's Section 6.4) — 3-step explicit ordering with blocking/non-blocking annotations
3. **threading.Lock mandate** for SummaryWorker `_summaries` dict (A's Section 4.5 critical invariants)
4. **SummaryWorker in summarizer.py** — resolve X-001 in A's favor (module cohesion)
5. **Resolved open questions** — collapse Q4, Q6, Q13 from open to resolved
6. **Test tasks T02.05 and T03.06** — add to checkpoint enforcement task numbering
7. **LOC totals** for all 3 feature areas (A's Section 1 overview table)
