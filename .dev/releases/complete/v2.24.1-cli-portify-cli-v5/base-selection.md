---
base_variant: B
variant_scores: "A:71 B:79"
---

# Scoring Criteria

Derived from the debate's key dispute areas and convergence assessment:

1. **Phase Structure Efficiency** (15%) — Minimal ceremony, no redundant phases
2. **Model/Resolution Coupling** (15%) — Appropriate grouping of tightly coupled work
3. **CLI Integration Design** (15%) — Ownership clarity for user-facing argument changes
4. **Timeline Realism** (15%) — Honest estimates that support planning
5. **Test Specificity** (10%) — Trackable, countable validation commitments
6. **Risk Communication** (10%) — Actionable risk information without process overhead
7. **Validation Traceability** (10%) — Clear mapping from criteria to verification method
8. **Readability & Navigability** (10%) — How quickly an implementer can extract what they need

# Per-Criterion Scores

| Criterion | Weight | A (Haiku) | B (Opus) | Notes |
|-----------|--------|-----------|----------|-------|
| Phase Structure Efficiency | 15% | 6/10 | 9/10 | A's Phase 0 and Phase 6 are overhead. Debate confirmed Phase 0 restates the roadmap; Phase 6 belongs in issue tracking. B's 5 phases have no dead weight. |
| Model/Resolution Coupling | 15% | 6/10 | 8/10 | A separates models (Phase 2) from resolution (Phase 1), but the debate showed models can't be reviewed meaningfully without resolution context. B combines them in Phase 1, enabling holistic review of the contract+algorithm together. |
| CLI Integration Design | 15% | 6/10 | 8/10 | A distributes CLI changes across phases. B isolates the high-risk `WORKFLOW_PATH → TARGET` change in a dedicated Phase 3. The debate's tiebreaker favored isolation for the single highest-risk CLI change. |
| Timeline Realism | 15% | 7/10 | 8/10 | A's 6.5 days is plausible but presents false precision given 7 open questions and 6 risks. B's 7-9 day range with per-phase ranges is more honest. Both converge around 7-8 days in practice, but B communicates uncertainty better. |
| Test Specificity | 10% | 5/10 | 8/10 | A says "targeted new test suite across 5 files" with no count. B specifies ~37 tests with per-phase breakdown (~15+~12+~5+~5). B is trackable against SC-8. |
| Risk Communication | 10% | 8/10 | 7/10 | A's three-tier governance (blocking/gating/managed) is clearer than B's severity column alone. Low cost, high clarity. A wins here. |
| Validation Traceability | 10% | 6/10 | 9/10 | B's tabular validation matrix (criterion → phase → method) is immediately scannable. A's narrative format requires reading through paragraphs to extract the same information. |
| Readability & Navigability | 10% | 6/10 | 8/10 | B uses tables for risks, timeline, validation, and dependency graphs. A is prose-heavy. For an implementer scanning for "what do I do in Phase 2," B is faster. |

# Overall Scores

| Variant | Weighted Score | Justification |
|---------|---------------|---------------|
| **A (Haiku)** | **71** | Stronger risk governance framework and thorough per-phase exit criteria, but carries dead-weight phases (0, 6), artificially splits coupled work, lacks test counts, and buries traceability in prose. |
| **B (Opus)** | **79** | Tighter phase structure, better coupling decisions, honest timelines, trackable test targets, and tabular formats that an implementer can action quickly. Weaker on risk governance labeling. |

# Base Variant Selection Rationale

**Variant B (Opus)** is the base because:

1. Its phase structure requires no subtraction — all 5 phases carry real work. A requires removing Phase 0 and Phase 6 (per debate convergence).
2. The model+resolution coupling in Phase 1 is architecturally sound — the debate confirmed these can't be reviewed independently.
3. The dedicated CLI phase (Phase 3) won the debate's tiebreaker on the highest-risk user-facing change.
4. Its tabular formats (risk table, validation matrix, timeline summary) are merge-ready scaffolding that A's content can be injected into.

# Improvements to Incorporate from Variant A

1. **Risk governance tiers** — Add A's three-tier classification (release-blocking / release-gating / managed resilience) as a column in B's risk table. Low cost, unambiguous go/no-go semantics.

2. **Per-phase exit criteria** — A explicitly states exit criteria for each phase. B implies them but doesn't formalize. Add a 2-3 line exit criteria block to each of B's phases.

3. **Lettered milestones** — A's Milestone A/B/C/D scheme provides status-tracking anchors. Add these to B's phase descriptions for progress reporting.

4. **Resolution log as first-class asset** — A's architectural priorities section explicitly calls out `resolution_log` as an observability asset. Add this emphasis to B's Phase 1 and Phase 4 descriptions.

5. **Contingency actions per risk** — A provides specific contingency plans (e.g., "narrow new resolution logic to explicit new input forms only"). B's mitigations are good but lack fallback actions. Merge A's contingency lines into B's risk table.
