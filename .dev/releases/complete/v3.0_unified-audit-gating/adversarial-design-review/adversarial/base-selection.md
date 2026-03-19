# Base Selection: Resume Pipeline Fix

## Quantitative Scoring (50% weight)

### Per-Metric Breakdown

| Metric | Weight | Variant A | Variant B | Variant C |
|--------|--------|-----------|-----------|-----------|
| Requirement Coverage (RC) | 0.30 | 0.85 (covers 4/4 bugs, no --depth) | 0.95 (covers 4/4 bugs + depth + option audit) | 0.90 (covers 4/4 bugs + depth) |
| Internal Consistency (IC) | 0.25 | 0.92 (no internal contradictions found) | 0.88 (Fix 1 vs Fix 1b creates two paths; interaction matrix addresses but adds complexity) | 0.85 (guard-then-sometimes-restore creates mixed signals in §3.1 vs §4.2) |
| Specificity Ratio (SR) | 0.15 | 0.90 (full code blocks, line references, concrete assertions) | 0.82 (mix of code and table-form tests; some pseudocode) | 0.75 (fewer code blocks; guard comparison uses hardcoded values) |
| Dependency Completeness (DC) | 0.15 | 0.88 (cross-references Bug 1→4 ordering; internal refs resolve) | 0.92 (cross-refs between §§2-7; interaction matrix §5 refs all fixes) | 0.82 (forward refs to §6 Click note from §3.1; some dangling) |
| Section Coverage (SC) | 0.15 | 0.80 (8/10 sections vs B's max) | 1.00 (10/10: problem, RCA, fixes, depth audit, interaction, tests, migration, files) | 0.70 (7/10: no dedicated migration, no option audit, no interaction matrix) |

### Quantitative Scores

| Variant | RC×0.30 | IC×0.25 | SR×0.15 | DC×0.15 | SC×0.15 | **Quant Total** |
|---------|---------|---------|---------|---------|---------|-----------------|
| A | 0.255 | 0.230 | 0.135 | 0.132 | 0.120 | **0.872** |
| B | 0.285 | 0.220 | 0.123 | 0.138 | 0.150 | **0.916** |
| C | 0.270 | 0.213 | 0.113 | 0.123 | 0.105 | **0.823** |

---

## Qualitative Scoring (50% weight) -- Additive Binary Rubric

### Completeness (5 criteria)

| # | Criterion | A | B | C |
|---|-----------|---|---|---|
| 1 | Covers all 4 bugs from source input | MET (Bugs 1-4 each have dedicated section) | MET (Fixes 1-4 mapped to bugs) | MET (§3.1-3.4 map to bugs) |
| 2 | Addresses edge cases and failure scenarios | MET (5-row edge case table for Bug 1) | MET (§6.3 lists 5 edge cases) | NOT MET (edge cases scattered, no systematic list) |
| 3 | Includes dependencies and prerequisites | MET (implementation order with rationale) | MET (§5 interaction matrix) | MET (§7 implementation order) |
| 4 | Defines success/completion criteria | NOT MET (no explicit success criteria) | NOT MET (no explicit success criteria) | NOT MET (no explicit success criteria) |
| 5 | Specifies what is out of scope | MET (race condition noted as out-of-scope) | NOT MET (scope boundaries implicit) | NOT MET (scope boundaries implicit) |
| | **Subtotal** | **4/5** | **3/5** | **2/5** |

### Correctness (5 criteria)

| # | Criterion | A | B | C |
|---|-----------|---|---|---|
| 1 | No factual errors | MET | MET | MET |
| 2 | Technical approaches feasible | MET (get_parameter_source is real API) | MET (None defaults work in Click) | MET (guard approach is sound) |
| 3 | Terminology consistent | MET | MET | MET |
| 4 | No internal contradictions | MET | NOT MET (Fix 1 vs Fix 1b presents two approaches without choosing) | NOT MET (§2 argues against restore, §4.2 restores depth) |
| 5 | Claims supported by evidence | MET (line numbers, code references) | MET (line numbers, code references) | MET (failure chain diagram, code references) |
| | **Subtotal** | **5/5** | **4/5** | **4/5** |

### Structure (5 criteria)

| # | Criterion | A | B | C |
|---|-----------|---|---|---|
| 1 | Logical section ordering | MET (bugs ordered by root cause) | MET (problem→RCA→fix→test→migration) | MET (problem→philosophy→fix→test) |
| 2 | Consistent hierarchy depth | MET | NOT MET (Fix 3 goes to H4 §3.1/3.2; others stay at H3) | MET |
| 3 | Clear separation of concerns | MET | MET | NOT MET (§3.3 argues both for and against cascade removal) |
| 4 | Navigation aids | NOT MET (no TOC or index) | NOT MET (no TOC or index) | NOT MET (no TOC or index) |
| 5 | Follows artifact type conventions | MET (standard design doc format) | MET (standard design doc format) | MET (standard design doc format) |
| | **Subtotal** | **4/5** | **3/5** | **3/5** |

### Clarity (5 criteria)

| # | Criterion | A | B | C |
|---|-----------|---|---|---|
| 1 | Unambiguous language | MET | NOT MET ("simpler and safer approach" without criteria for simpler/safer) | MET |
| 2 | Concrete rather than abstract | MET (full code for all fixes) | MET (full code for fixes, though Fix 1 has two variants) | NOT MET (§3.3 cascade discussion is abstract; no concrete recommendation) |
| 3 | Each section has clear purpose | MET | MET | MET |
| 4 | Terms defined on first use | MET | MET | MET |
| 5 | Actionable next steps identified | MET (implementation order explicit) | MET (§8 files to modify) | MET (§7 implementation order) |
| | **Subtotal** | **5/5** | **4/5** | **4/5** |

### Risk Coverage (5 criteria)

| # | Criterion | A | B | C |
|---|-----------|---|---|---|
| 1 | Identifies ≥3 risks with assessment | MET (5-row risk table with likelihood) | NOT MET (risks mentioned inline but no structured assessment) | NOT MET (no structured risk assessment) |
| 2 | Mitigation strategy per risk | MET (mitigations in table column) | NOT MET (mitigations implied but not structured) | NOT MET (layers serve as implicit mitigation) |
| 3 | Addresses failure modes and recovery | MET (edge case table per bug) | MET (§6.3 edge cases) | MET (§5 layered defense) |
| 4 | Considers external dependencies | MET (Click version check noted) | MET (Click None handling, schema version) | MET (Click eager problem noted) |
| 5 | Monitoring/validation mechanism | NOT MET (no logging/alerting spec) | NOT MET (no monitoring spec) | MET (cascade logging, conditional write logging) |
| | **Subtotal** | **4/5** | **2/5** | **3/5** |

### Invariant & Edge Case Coverage (5 criteria)

| # | Criterion | A | B | C |
|---|-----------|---|---|---|
| 1 | Boundary conditions for collections | MET (empty/missing state file, malformed agents) | MET (empty agents, missing state) | MET (empty state, no-progress condition) |
| 2 | State variable interactions | NOT MET (doesn't address depth/agents coupling) | MET (interaction matrix covers cross-fix state) | MET (differential depth/agents treatment) |
| 3 | Guard condition gaps | MET (Step.inputs or [] handles None) | MET (None check at boundary) | MET (conditional writes as guard) |
| 4 | Count divergence scenarios | NOT MET (no parallel group discussion) | NOT MET (no parallel group discussion) | NOT MET (no parallel group discussion) |
| 5 | Interaction effects when features combine | NOT MET (no cross-fix interaction analysis) | MET (§5 interaction matrix) | MET (§5 layered defense model) |
| | **Subtotal** | **2/5** | **3/5** | **3/5** |

### Edge Case Floor Check

| Variant | Invariant & Edge Case Score | Eligible? |
|---------|---------------------------|-----------|
| A | 2/5 | YES (≥1/5 threshold) |
| B | 3/5 | YES |
| C | 3/5 | YES |

### Qualitative Summary

| Dimension | A | B | C |
|-----------|---|---|---|
| Completeness | 4/5 | 3/5 | 2/5 |
| Correctness | 5/5 | 4/5 | 4/5 |
| Structure | 4/5 | 3/5 | 3/5 |
| Clarity | 5/5 | 4/5 | 4/5 |
| Risk Coverage | 4/5 | 2/5 | 3/5 |
| Invariant/Edge | 2/5 | 3/5 | 3/5 |
| **Total** | **24/30** | **19/30** | **19/30** |
| **Qual Score** | **0.800** | **0.633** | **0.633** |

---

## Position-Bias Mitigation

| Dimension | Variant | Pass 1 (A,B,C) | Pass 2 (C,B,A) | Agreement | Final |
|-----------|---------|-----------------|-----------------|-----------|-------|
| Risk Coverage | B | 2/5 | 2/5 | Agree | 2/5 |
| Risk Coverage | C | 3/5 | 3/5 | Agree | 3/5 |
| Completeness | C | 2/5 | 3/5 | Disagree | 2/5 (re-evaluated: missing systematic edge cases confirmed) |
| Invariant/Edge | A | 2/5 | 2/5 | Agree | 2/5 |

Disagreements found: 1
Verdicts changed: 0

---

## Combined Scoring

| Variant | Quant (×0.50) | Qual (×0.50) | **Combined** | Rank |
|---------|---------------|--------------|--------------|------|
| A | 0.436 | 0.400 | **0.836** | 1 |
| B | 0.458 | 0.317 | **0.775** | 2 |
| C | 0.412 | 0.317 | **0.728** | 3 |

**Margin A vs B**: 6.1% (above 5% tiebreaker threshold -- no tiebreaker needed)

---

## Selected Base: Variant A (brainstorm-resume-fix-A.md)

### Selection Rationale

Variant A scores highest on the combined metric, driven by strong qualitative performance: highest correctness (5/5), clarity (5/5), completeness (4/5), and risk coverage (4/5). While B leads quantitatively (broader requirement coverage, better section coverage), A's implementation specificity (full pytest code blocks, concrete line references, dedicated risk table) makes it the most actionable base for merge execution.

### Strengths to Preserve from Base (A)
1. `ctx.get_parameter_source("agents")` detection mechanism (to be wrapped in `ResumableConfig` per Round 3 consensus)
2. Silent restore via `_restore_agents_from_state()` helper
3. Full `_apply_resume` rewrite with `regenerated_outputs` set
4. Defense-in-depth `_save_state` with generate-step check
5. Full pytest code blocks for all tests
6. Risk assessment table with likelihood ratings
7. Backward compatibility analysis

### Strengths to Incorporate from Non-Base Variants

**From B:**
1. Full CLI option audit table (§4) -- systematic review of all `--` options
2. Fix interaction matrix (§5) -- partial-application risk analysis
3. Schema version / migration analysis (§7.3)
4. `_step_needs_rerun()` helper extraction for modularity
5. `--depth` coverage with same detection pattern
6. Integration and edge case test specifications (expand A's 6 tests)
7. Estimated diff size annotation

**From C:**
1. Differential `--depth` vs `--agents` treatment rationale
2. State-driven path resolution concept for `_apply_resume` gate checks
3. Conditional state writes: no-progress guard for `_save_state`
4. 5-layer defense summary as documentation
5. `--on-conflict` flag design for non-interactive contexts
6. Cascade logging for observability (complement dependency-aware tracking)

**From Round 3 Consensus (all variants):**
1. `ResumableConfig` dataclass with `source` tag (replaces raw `get_parameter_source`)
2. `-1` high-water mark initialization with atomic group completion
3. `group_progress` dict for smart per-step rerun within parallel groups
4. State file schema versioning
5. WARNING for orphaned agent assignments under quick depth
