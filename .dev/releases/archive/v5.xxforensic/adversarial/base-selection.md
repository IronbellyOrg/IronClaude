# Base Selection: Forensic Refactor Specification

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant A | Variant B | Notes |
|--------|--------|-----------|-----------|-------|
| Requirement Coverage (RC) | 0.30 | 0.85 | 0.90 | B covers more concrete requirements from source spec (phase behavior, thresholds, artifact schema) |
| Internal Consistency (IC) | 0.25 | 0.95 | 0.88 | A has fewer internal tensions; B has `--depth` overload acknowledged as concession |
| Specificity Ratio (SR) | 0.15 | 0.55 | 0.85 | B provides concrete numbers (token budgets, agent counts, line estimates), YAML schemas, tables. A is more narrative. |
| Dependency Completeness (DC) | 0.15 | 0.90 | 0.85 | A explicitly cross-references forensic spec, troubleshoot, brainstorm, adversarial boundaries. B references but assumes reader knows them. |
| Section Coverage (SC) | 0.15 | 1.00 | 0.63 | A has 19 sections; B has 10 sections (normalized: A=1.00, B=10/19=0.53 adjusted to 0.63 for comparable depth) |

**Quant Scores**:
- Variant A: (0.85×0.30) + (0.95×0.25) + (0.55×0.15) + (0.90×0.15) + (1.00×0.15) = 0.255 + 0.2375 + 0.0825 + 0.135 + 0.15 = **0.860**
- Variant B: (0.90×0.30) + (0.88×0.25) + (0.85×0.15) + (0.85×0.15) + (0.63×0.15) = 0.270 + 0.220 + 0.1275 + 0.1275 + 0.0945 = **0.839**

---

## Qualitative Scoring (50% weight) -- Additive Binary Rubric

### Completeness (5 criteria)

| # | Criterion | Variant A | Variant B |
|---|-----------|-----------|-----------|
| 1 | Covers all explicit requirements from source input | MET — covers architectural decision, responsibility split, coupling contract, mode model, escalation, artifacts | MET — covers phase behavior, thresholds, context interface, artifacts, implementation phasing |
| 2 | Addresses edge cases and failure scenarios | NOT MET — no "MAY fix directly" exceptions, no "test is wrong" outcome | MET — S4 MAY-fix-directly exceptions, S9 "test is wrong" valid outcome |
| 3 | Includes dependencies and prerequisites | MET — S3 documents troubleshoot, brainstorm, adversarial prerequisites | MET — S10 cross-references all dependencies |
| 4 | Defines success/completion criteria | NOT MET — no acceptance criteria defined | NOT MET — no formal acceptance criteria |
| 5 | Specifies what is explicitly out of scope | MET — S14 boundaries section | NOT MET — no explicit out-of-scope section |

**Completeness**: A = 3/5, B = 3/5

### Correctness (5 criteria)

| # | Criterion | Variant A | Variant B |
|---|-----------|-----------|-----------|
| 1 | No factual errors or hallucinated claims | MET | MET |
| 2 | Technical approaches feasible with stated constraints | MET | MET |
| 3 | Terminology used consistently | MET | MET |
| 4 | No internal contradictions | MET | NOT MET — `--depth` overloading creates tension with FR-038 (acknowledged as concession) |
| 5 | Claims supported by evidence or rationale | MET | MET — S9 traces decisions to user approvals |

**Correctness**: A = 5/5, B = 4/5

### Structure (5 criteria)

| # | Criterion | Variant A | Variant B |
|---|-----------|-----------|-----------|
| 1 | Logical section ordering | MET — progressive: problem → gaps → recommendation → decision → implications → guidance | MET — progressive: problem → decision → requirements → thresholds → phasing |
| 2 | Consistent hierarchy depth | MET | MET |
| 3 | Clear separation of concerns between sections | MET | MET |
| 4 | Navigation aids present | NOT MET — no TOC or cross-references between sections | NOT MET — no TOC |
| 5 | Follows conventions of the artifact type | MET — handoff document conventions | MET — context brief conventions |

**Structure**: A = 4/5, B = 4/5

### Clarity (5 criteria)

| # | Criterion | Variant A | Variant B |
|---|-----------|-----------|-----------|
| 1 | Unambiguous language | NOT MET — S7 uses "fast failure triage", "scope limited to" without specifics | MET — per-phase table with SKIP/2-agents/abbreviated |
| 2 | Concrete rather than abstract | NOT MET — strategic framing with open questions | MET — tables, YAML schemas, token budgets |
| 3 | Each section has clear purpose | MET | MET |
| 4 | Acronyms and domain terms defined | NOT MET — TFEP not defined (uses "light mode" instead) | MET — S2 defines TFEP explicitly |
| 5 | Actionable next steps identified | MET — S19 clear direction statement | MET — S8 two-phase implementation |

**Clarity**: A = 2/5, B = 5/5

### Risk Coverage (5 criteria)

| # | Criterion | Variant A | Variant B |
|---|-----------|-----------|-----------|
| 1 | Identifies at least 3 risks | MET — S5 Option A cons (bloat, drift, maintenance), S11 naming conflict | MET — S2 regression risk, scope creep, S9 max iterations |
| 2 | Mitigation strategy for each risk | MET — separate command mitigates bloat; naming resolution guidance in S12 | NOT MET — risks identified but mitigations sparse |
| 3 | Addresses failure modes and recovery | NOT MET — no recovery procedures | NOT MET — no recovery procedures for TFEP failure |
| 4 | Considers external dependencies | MET — S3 analyzes troubleshoot, brainstorm, adversarial as dependencies | MET — S10 cross-references |
| 5 | Monitoring or validation mechanism | NOT MET | NOT MET |

**Risk Coverage**: A = 3/5, B = 2/5

### Invariant & Edge Case Coverage (5 criteria)

| # | Criterion | Variant A | Variant B |
|---|-----------|-----------|-----------|
| 1 | Boundary conditions for collections | NOT MET — no empty/single test case handling | NOT MET — no empty test suite handling |
| 2 | State variable interactions across components | MET — S9 coupling contract defines state handoff | NOT MET — INV-001 unaddressed (pre-existing vs new test detection) |
| 3 | Guard condition gaps | NOT MET — no validation for failure context completeness | NOT MET — no validation for context package completeness |
| 4 | Count divergence scenarios | NOT MET | NOT MET — INV-003 parameterized test inflation |
| 5 | Interaction effects when components combine | NOT MET — INV-004 artifact/tasklist compatibility | NOT MET — INV-004 artifact/tasklist compatibility |

**Invariant & Edge Case Coverage**: A = 1/5, B = 0/5

### Edge Case Floor Check
- Variant A: 1/5 — meets minimum floor (>=1/5)
- Variant B: 0/5 — **BELOW FLOOR** (ineligible as base variant)
- **Floor suspension check**: NOT all variants score 0/5 (A scores 1/5), so floor is enforced.

### Qualitative Summary

| Dimension | Variant A | Variant B |
|-----------|-----------|-----------|
| Completeness | 3/5 | 3/5 |
| Correctness | 5/5 | 4/5 |
| Structure | 4/5 | 4/5 |
| Clarity | 2/5 | 5/5 |
| Risk Coverage | 3/5 | 2/5 |
| Invariant & Edge Case | 1/5 | 0/5 |
| **Total** | **18/30** | **18/30** |

**Qual Scores**: A = 18/30 = **0.600**, B = 18/30 = **0.600**

---

## Position-Bias Mitigation

| Dimension | Pass 1 (A→B) | Pass 2 (B→A) | Agreement | Final |
|-----------|-------------|-------------|-----------|-------|
| Completeness | A=3, B=3 | A=3, B=3 | Yes | A=3, B=3 |
| Correctness | A=5, B=4 | A=5, B=4 | Yes | A=5, B=4 |
| Structure | A=4, B=4 | A=4, B=4 | Yes | A=4, B=4 |
| Clarity | A=2, B=5 | A=2, B=5 | Yes | A=2, B=5 |
| Risk Coverage | A=3, B=2 | A=3, B=2 | Yes | A=3, B=2 |
| Invariant | A=1, B=0 | A=1, B=0 | Yes | A=1, B=0 |

Disagreements found: 0. No re-evaluation needed.

---

## Combined Scoring

| Variant | Quant (50%) | Qual (50%) | Combined | Eligible |
|---------|-------------|------------|----------|----------|
| Variant A | 0.860 × 0.50 = 0.430 | 0.600 × 0.50 = 0.300 | **0.730** | Yes |
| Variant B | 0.839 × 0.50 = 0.420 | 0.600 × 0.50 = 0.300 | **0.720** | **No** (edge case floor 0/5) |

**Margin**: 1.0% (within tiebreaker range of 5%)
**Tiebreaker applied**: No — Variant B is ineligible due to edge case floor violation.

---

## Selected Base: Variant A (forensic-refactor-handoff.md)

### Selection Rationale

Variant A is selected as base despite the close scoring for two reasons:

1. **Edge case floor enforcement**: Variant B scores 0/5 on Invariant & Edge Case Coverage, making it ineligible as base per the rubric rules. Variant A scores 1/5 (meeting minimum).

2. **Debate performance on architectural points**: Variant A won the two most architecturally consequential diff points — C-001 (flag model: 3-axis vs overloaded `--depth`) at 65% confidence and X-001 (same topic, contradiction) at 60% confidence. These are L3 (state-mechanics) level decisions that affect the entire system's composability.

### Strengths to Preserve from Base (Variant A)
- Three-axis flag model separation (intent/tier/debate-depth)
- Comprehensive responsibility split between task-unified and forensic
- Coupling contract with explicit inputs/outputs
- Existing command boundary documentation
- `--caller`/`--trigger` concept for extensibility
- Profiles abstraction for composable configurations
- Genericity preservation requirement

### Strengths to Incorporate from Variant B
1. **Per-phase behavior table** (B S3.1) — concrete SKIP/2-agents/abbreviated specs per phase per mode
2. **Binary escalation thresholds** (B S4) — "any pre-existing test fails", "3+ new tests fail", MAY-fix-directly exceptions
3. **Token budget estimates** (B S3.1) — ~5-8K quick, ~15-20K standard
4. **Two-phase implementation strategy** (B S8) — immediate guard now, full integration later
5. **YAML context interface** (B S3.3) — structured failure_context schema with example values
6. **Section-by-section forensic spec change mapping** (B S6) — which sections need what changes
7. **"Test is wrong" as valid outcome** (B S9) — prevents infinite remediation loops
8. **Complete artifact directory tree** (B S3.5) — phase subdirectories and filenames
9. **User-approved decision log** (B S9) — 9 explicit decisions with rationale

### Unresolved Invariants to Address in Merge
- **INV-001**: Test baseline mechanism for pre-existing vs new test detection
- **INV-004**: Artifact-to-tasklist format compatibility specification
