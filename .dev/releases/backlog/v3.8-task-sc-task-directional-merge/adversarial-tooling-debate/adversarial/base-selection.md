# Base Selection: Hybrid Scoring

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant A (sc:tasklist) | Variant B (task-builder) |
|--------|--------|--------------------------|---------------------------|
| Requirement Coverage (RC) | 0.30 | 0.96 (matches all 8 focus dimensions explicitly) | 0.78 (matches 5/8 explicitly; 3 inferred) |
| Internal Consistency (IC) | 0.25 | 0.94 (no contradictions found; one section explicitly carves CLI vs skill behavior) | 0.91 (no contradictions found; spec is longer + more discursive but consistent) |
| Specificity Ratio (SR) | 0.15 | 0.88 (numerous concrete thresholds, IDs, regex patterns, exact filenames) | 0.82 (concrete file paths and counts; more "depends-on" qualitative guidance) |
| Dependency Completeness (DC) | 0.15 | 0.92 (all cross-references resolved; explicit references to Section N.M) | 0.84 (cross-references to "A.7", "A.8", etc. all resolve) |
| Section Coverage (SC) | 0.15 | 1.00 (more sections normalized to max) | 0.94 |
| **quant_score** | — | **(0.96×0.30)+(0.94×0.25)+(0.88×0.15)+(0.92×0.15)+(1.00×0.15) = 0.937** | **(0.78×0.30)+(0.91×0.25)+(0.82×0.15)+(0.84×0.15)+(0.94×0.15) = 0.842** |

## Qualitative Scoring (50% weight) — 30-Criterion Additive Binary Rubric

### Completeness (5 criteria)
- A: 5/5 (covers all 8 focus dimensions, edge cases, dependencies, success criteria, scope exclusions)
- B: 5/5 (covers all aspects; explicit scope statements throughout)

### Correctness (5 criteria)
- A: 5/5 (no factual errors; technical claims feasible; terminology consistent; no internal contradictions; claims supported by evidence)
- B: 5/5 (same — both skills are internally correct for their intended use)

### Structure (5 criteria)
- A: 5/5 (clear logical ordering; consistent hierarchy; navigation aids; conventions of skill-spec artifact type)
- B: 4/5 (logical ordering, but specification mixes "user-facing prompt examples" with "implementation steps" — single criterion miss: "clear separation of concerns")

### Clarity (5 criteria)
- A: 4/5 (concrete throughout; misses 1 — actionable next step is implicit ("invoke `Skill sc:tasklist-protocol`") but the command file does the dispatching)
- B: 5/5 (very clear input/output contracts; tier selection rules explicit; effective prompt examples)

### Risk Coverage (5 criteria)
- A: 3/5 (identifies "no policy forks", "no clarification = clarification task", "ambiguous-tier confidence threshold"; misses explicit risk register + monitoring mechanism)
- B: 4/5 (zero-trust QA at 3 gates is explicit risk mitigation; failure modes named; monitoring via QA reports; misses external-dependency failure scenario)

### Invariant & Edge Case Coverage (5 criteria)
- A: 4/5 (Phase 8 missing-number rule; tier conflict resolution; clarification-task insertion; checkpoint cadence; misses interaction-effect between compound deliverables and tasklist splitting — caught only post-validation)
- B: 4/5 (multi-track edge cases; resume from various states; F1 loop edge cases; misses scale boundary above 50-item checklist)

### Qualitative Dimension Subtotals
| Dimension | A | B |
|-----------|---|---|
| Completeness | 5 | 5 |
| Correctness | 5 | 5 |
| Structure | 5 | 4 |
| Clarity | 4 | 5 |
| Risk Coverage | 3 | 4 |
| Invariant/Edge | 4 | 4 |
| **Total** | **26/30** | **27/30** |

### Edge Case Floor Check
- A: 4/5 on Invariant/Edge dimension → **PASSES** floor (≥1/5)
- B: 4/5 on Invariant/Edge dimension → **PASSES** floor

### Qualitative Scores
- **qual_score(A) = 26/30 = 0.867**
- **qual_score(B) = 27/30 = 0.900**

## Position-Bias Mitigation

Re-ran rubric in reverse order (B first, then A). Re-evaluation produced identical totals (26 and 27). No disagreements between passes. No re-evaluation required.

## Combined Scoring

- **variant_score(A) = 0.50 × 0.937 + 0.50 × 0.867 = 0.902**
- **variant_score(B) = 0.50 × 0.842 + 0.50 × 0.900 = 0.871**
- **Margin:** 0.031 (3.1%)
- **Tiebreaker check:** Margin <5% → invoke tiebreaker
  - Level 1 (debate performance): A wins 16 points, B wins 6 points → **A wins**
  - Tiebreaker level 1 resolves; no further tiebreakers needed

## Selected Base: Variant A (sc:tasklist)

### Selection Rationale

Variant A wins on **debate performance** (16 vs 6 points), on **quantitative scoring** (0.937 vs 0.842), and on the **invariant probe** (INV-007 specifically identifies B's atomicity-binding violation risk as HIGH-severity UNADDRESSED). B's narrow qualitative-rubric edge (0.900 vs 0.867 — 3.3% margin) reflects B's strengths as a *skill specification document* (clearer prompt examples, explicit risk mitigation framing) — these are skill-prose qualities, not operational fitness for the current artifact.

The combined verdict: **Variant A is operationally fitter for the current 132-task, 5-milestone, atomicity-bound roadmap. Variant B is the right tool for a different scenario (novel-feature MDTM task creation with no validated roadmap upstream).**

### Strengths to Preserve from Base (Variant A)
- Sprint-CLI multi-file bundle output (drives downstream orchestration)
- Tier classification at generation time (load-bearing for `/sc:task` compliance)
- Deterministic algorithm + tie-breaker rules (reproducibility)
- Compound-deliverable preservation for atomicity bindings
- Auto-wired `.roadmap-state.json` (TDD/PRD enrichment without re-passing flags)

### Strengths to Incorporate from Non-Base (Variant B)
For the immediate `/sc:tasklist` invocation: **none directly** — the two skills are not mergeable artifacts, and `/sc:tasklist`'s deterministic-transform contract would be violated by injecting `/task-builder`'s research-subagent pattern.

For a *future* enhancement of `/sc:tasklist`: B's three-gate validation pattern (rf-analyst → rf-qa → rf-qa-qualitative) could supplement `/sc:tasklist`'s post-generation validation. This is a roadmap-for-the-skill-itself improvement, not a current-decision change.
