---
base_variant: A
variant_scores: "A:76 B:74"
---

# Scoring Criteria

Derived from the debate's key disputes and convergence points:

1. **Implementation Specificity** — Function names, file paths, constants, field lists ready for direct coding
2. **Phase Structure & Ordering** — Logical dependency ordering, minimal handoff overhead
3. **Risk Treatment** — Explicit risk identification, severity, and actionable mitigation
4. **Requirement Traceability** — Clear FR/NFR/SC mapping per phase
5. **Timeline Realism** — Honest estimation given LLM-dependent phases and ~60% pre-built infrastructure
6. **Architectural Correctness** — Ordering decisions validated by the debate's technical arguments
7. **Operational Overhead** — Ratio of implementation guidance to project management artifacts

# Per-Criterion Scores

| Criterion | Variant A (Opus) | Variant B (Haiku) | Notes |
|---|---|---|---|
| Implementation Specificity | **9/10** | 6/10 | Opus provides function names, cost constants (`CHECKER_COST=10`), byte budgets with allocation percentages, field lists, line references (`convergence.py:50-225`). Haiku describes what to build but rarely names the function or constant. |
| Phase Structure & Ordering | 7/10 | **8/10** | Haiku's separation of registry (Phase 3) from convergence (Phase 5) is validated by the debate — registry serves multiple consumers. Haiku's semantic-before-convergence ordering avoids speculative branching on `source_layer` tags. Opus's bundling is faster but riskier per debate D4/D6. |
| Risk Treatment | **8/10** | 7/10 | Opus surfaces 8 risks with specific mitigations including Risks 7-8 (pre-v3.05 migration, pass credit asymmetry) that Haiku conceded were buried. Haiku adds 5 open-question risks but gives them less visibility. |
| Requirement Traceability | 8/10 | **9/10** | Haiku maps requirements per phase with "Requirements covered" sections and provides explicit SC traceability in Section 5. Opus maps requirements in milestone headers but less systematically. |
| Timeline Realism | 6/10 | **8/10** | Debate consensus: point estimates on LLM-dependent work are aspirational. Haiku's ranges (36-49 days) are more honest. Opus's 32-day estimate assumes zero rework. |
| Architectural Correctness | 7/10 | **8/10** | Debate resolved three disputes in Haiku's favor: FR-10 placement (registry concern), semantic-before-convergence ordering, and registry isolation. Opus wins on data model front-loading if mismatch types are stable, but this is conditional. |
| Operational Overhead | **9/10** | 6/10 | Opus is lean — no Phase 0, no staffing models, no architect emphasis blocks. For a solo developer (likely staffing), this is appropriate. Haiku's gates A-F and emphasis blocks add value for teams but are overhead for solo execution. |

| | A | B |
|---|---|---|
| **Total (weighted)** | **76** | **74** |

Weighting: Implementation Specificity and Architectural Correctness weighted 1.5x; Operational Overhead weighted 0.75x (staffing-dependent).

# Overall Scores & Justification

**Variant A: 76/100** — Superior implementation density makes it immediately actionable. A developer can read Phase 2, Milestone 2.2 and start coding the five checkers without any design interpretation. Risk treatment is more complete. However, three ordering decisions were challenged successfully in the debate.

**Variant B: 74/100** — Architecturally sounder ordering validated by debate. Better timeline honesty and requirement traceability. But implementation sections require a design step before coding begins — "implement FR-1" is an instruction, not a specification. Phase 0 adds 2-3 days of overhead that the debate did not fully resolve in Haiku's favor.

# Base Variant Selection Rationale

**Variant A (Opus) is the base** because:

1. **Implementation density is the harder thing to add.** Haiku's ordering improvements can be applied to Opus's structure by rearranging phases. Adding Opus's level of specificity (function names, constants, field lists, line references) to Haiku's structure would require rewriting every phase.

2. **The merge needs to fix 3 ordering decisions, not rewrite 6 phases of detail.** Moving FR-10 from Phase 4 to Phase 3, reordering semantic-before-convergence, and optionally separating registry from convergence are surgical changes to Opus's structure.

3. **Risk treatment is already stronger.** Risks 7-8 are present; open questions can be added from Haiku.

# Specific Improvements to Incorporate from Variant B

1. **FR-10 placement → Phase 3 (registry phase).** Move run-to-run memory from Phase 4 to Phase 3, per debate consensus that it is a registry concern. Validate end-to-end in Phase 4 when the semantic layer consumes it.

2. **Semantic-before-convergence ordering.** Restructure so the semantic layer (current Phase 4) is validated before the convergence engine consumes its outputs. This avoids building convergence conditional logic (`if source_layer == "semantic"`) against mock semantic findings — directly addressing the project's anti-mock memory.

3. **Timeline ranges.** Replace Opus's 32-day point estimate with range estimates. Use Opus's phase durations as lower bounds and add Haiku-style ranges for LLM-dependent phases (semantic layer, debate calibration, convergence integration).

4. **Named milestone gates (A-F).** Add Haiku's gate structure as lightweight checkpoints mapped to SC criteria. Strip the staffing model and architect emphasis blocks (overhead for solo execution), but keep the gates as go/no-go markers.

5. **Open question risks.** Add Haiku's 5 open-question risks (ParseWarning severity policy, agent failure definition, cross-file coherence scope, TurnLedger constant calibration, FR-4.1 threshold calibration) as explicit items in the risk table rather than burying them in phase exit criteria.

6. **Requirement-ID preservation guidance.** Add Haiku's Section 5 note on preserving exact IDs (FR-4.1, FR-7.1, etc.) in all artifacts — a low-cost addition that prevents requirement drift over a multi-week project.

7. **Collapse Phase 0 into Phase 1.** Per debate: if the team recently worked with TurnLedger and the registry, Phase 0 compresses to hours. Add interface verification as the first milestone of Phase 1 (a 2-hour task, per Opus's rebuttal) rather than a standalone phase.
