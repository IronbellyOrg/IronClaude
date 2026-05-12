# 03 -- Roadmap Phase Structure Comparison

**Status**: Complete
**Investigation Type:** Pattern Investigator
**Date:** 2026-04-03
**Question:** Why does the TDD+PRD roadmap have 3 phases (66 sections) while the baseline has 5 phases (38 sections)? Does the tasklist generator follow the roadmap's phase structure or create its own?

---

## 1. Phase Count and Naming

### Baseline Roadmap (test3-spec-baseline/roadmap.md) -- 5 Phases

| Phase | Name | Weeks | Lines (approx) |
|-------|------|-------|-----------------|
| Phase 1 | Foundation Layer | 1-2 | 39-84 |
| Phase 2 | Core Auth Logic | 2-3 | 92-135 |
| Phase 3 | Integration Layer | 3-4 | 138-178 |
| Phase 4 | Hardening and Validation | 5-6 | 182-234 |
| Phase 5 | Production Readiness | 6 (overlap w/ P4) | 237-277 |

### TDD+PRD Roadmap (test1-tdd-prd-v2/roadmap.md) -- 3 Phases

| Phase | Name | Weeks | Lines (approx) |
|-------|------|-------|-----------------|
| Phase 1 | Core Authentication -- Internal Alpha | 1-2 | 46-217 |
| Phase 2 | Password Reset, Compliance, and Beta | 3-4 | 220-336 |
| Phase 3 | GA Rollout and Stabilization | 5-6 | 339-432 |

**Key Finding:** The TDD+PRD roadmap uses a **delivery-milestone** phasing model (Alpha/Beta/GA), while the baseline uses a **technical-layer** phasing model (Foundation/Logic/Integration/Hardening/Production). Same 6-week timeline, radically different decomposition philosophy.

---

## 2. Subsection Count per Phase

### Baseline Roadmap -- Subsections within Phases

| Phase | Subsections (####) | Table Rows (discrete work items) |
|-------|-------------------|----------------------------------|
| Phase 1 | 1.1, 1.2, 1.3, 1.4, 1.5 | 3 + 4 + 4 + 3 + 2 = 16 |
| Phase 2 | 2.1, 2.2, 2.3 | 7 + 7 + 3 = 17 |
| Phase 3 | 3.1, 3.2, 3.3 | 4 + 7 + 6 = 17 |
| Phase 4 | 4.1, 4.2, 4.3, 4.4, 4.5 | 4 + 9 + 3 + 3 + 3 = 22 |
| Phase 5 | 5.1, 5.2, 5.3, 5.4 | 3 + 5 + 3 + 4 = 15 |
| **Total** | **20 subsections** | **87 work items** |

### TDD+PRD Roadmap -- Subsections within Phases

| Phase | Subsections (####) | Discrete Work Items (table rows + numbered lists + wiring tasks) |
|-------|-------------------|----------------------------------------------------------------|
| Phase 1 | 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9 | 5 + 6(+4 wiring) + 5 + 4(+1 wiring) + 5(+2 wiring) + 2 + 4 + 6 + 14 = ~53 items |
| Phase 2 | 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7 | 2(+1 wiring) + 1 + 4 + 4 + 5(alerts) + 5 + 3 = ~25 items |
| Phase 3 | 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8 | 6 + 3 + 3 + 2 + 3 + 7 + 4 + 6 = ~34 items |
| **Total** | **24 subsections** | **~112 work items** |

**Key Finding:** The TDD+PRD roadmap has MORE subsections (24 vs 20) and significantly MORE work items (~112 vs 87) despite having FEWER phases. The 3-phase model is not a reduction in scope -- it is a consolidation into delivery milestones with much denser per-phase content.

---

## 3. Why 3 Phases vs 5 Phases?

The difference is explained by the input documents and the architectural debate:

### Baseline (5 phases): Spec-only input
- Input: A single technical specification (`test-spec-user-auth.md`)
- No PRD, no personas, no business metrics
- Roadmap follows a **build-up-the-stack** pattern: schema first, then services, then routes, then hardening, then production ops
- Phases map to technical dependency layers (DB -> Services -> HTTP -> Tests -> Deploy)
- Phase 4 (Hardening) and Phase 5 (Production) are separated because the spec has no rollout strategy

### TDD+PRD (3 phases): TDD + PRD dual input
- Input: TDD (`test-tdd-user-auth.md`) + PRD (`test-prd-user-auth.md`)
- PRD provides personas, business metrics, rollout strategy, compliance requirements
- The adversarial debate (convergence 0.72) explicitly chose a **progressive delivery** model: Alpha -> Beta 10% -> GA 100%
- Each phase delivers a **shippable increment**, not just a technical layer
- Phase 1 includes foundation, services, routes, frontend, AND testing -- everything needed for internal alpha
- Phase 4/5 concerns (hardening, monitoring, deployment) are distributed across all 3 phases because the PRD demands production-readiness at each milestone

**Root cause:** The PRD's rollout strategy (Internal Alpha -> Beta 10% -> GA 100%) dictated the phase structure. The adversarial debate explicitly noted: "Password reset (FR-AUTH-005) moved to Phase 2 per Opus's progressive delivery argument -- reduces Phase 1 blast radius."

---

## 4. Tasklist Generator Phase Fidelity

### Baseline: Roadmap -> Tasklist Mapping

| Roadmap Phase | Tasklist Phase | Phase Name Match? | Task Count |
|---------------|---------------|-------------------|------------|
| Phase 1: Foundation Layer | Phase 1 | Yes (exact) | 16 |
| Phase 2: Core Auth Logic | Phase 2 | Yes (exact) | 17 |
| Phase 3: Integration Layer | Phase 3 | Yes (exact) | 17 |
| Phase 4: Hardening and Validation | Phase 4 | Yes (exact) | 22 |
| Phase 5: Production Readiness | Phase 5 | Yes (exact) | 15 |
| **Total** | **5 phases** | **5/5 match** | **87 tasks** |

The baseline tasklist-index.md explicitly states `total_phases: 5` and maps 1:1 to roadmap phases.

### TDD+PRD: Roadmap -> Tasklist Mapping

| Roadmap Phase | Tasklist Phase | Phase Name Match? | Task Count |
|---------------|---------------|-------------------|------------|
| Phase 1: Core Authentication -- Internal Alpha | Phase 1: Core Authentication -- Internal Alpha | Yes (exact) | 27 |
| Phase 2: Password Reset, Compliance, and Beta | Phase 2: Password Reset, Compliance, and Beta | Yes (exact) | 9 |
| Phase 3: GA Rollout and Stabilization | Phase 3: GA Rollout and Stabilization | Yes (exact) | 8 |
| **Total** | **3 phases** | **3/3 match** | **44 tasks** |

The TDD+PRD tasklist-index.md states `Total Phases: 3` and maps 1:1 to roadmap phases.

**Finding: The tasklist generator preserves roadmap phase structure with 1:1 fidelity.** It does not create its own phases, reinterpret phases, split, or merge them. Phase names are passed through verbatim.

---

## 5. Roadmap Work Items to Tasklist Tasks Ratio

### Baseline

| Phase | Roadmap Work Items | Tasklist Tasks | Ratio |
|-------|-------------------|----------------|-------|
| Phase 1 | 16 | 16 | 1.00:1 |
| Phase 2 | 17 | 17 | 1.00:1 |
| Phase 3 | 17 | 17 | 1.00:1 |
| Phase 4 | 22 | 22 | 1.00:1 |
| Phase 5 | 15 | 15 | 1.00:1 |
| **Total** | **87** | **87** | **1.00:1** |

The baseline index states `roadmap_item_range: "R-001 -- R-087"` and `total_tasks: 87`. This is a perfect 1:1 mapping.

### TDD+PRD

| Phase | Roadmap Items (R-###) | Tasklist Tasks | Deliverables | R-to-T Ratio | R-to-D Ratio |
|-------|----------------------|----------------|-------------- |-------------- |-------------- |
| Phase 1 | R-001 to R-027 (27) | 27 (T01.01-T01.27) | 29 | 1.00:1 | 1.07:1 |
| Phase 2 | R-028 to R-036 (9) | 9 (T02.01-T02.09) | 10 | 1.00:1 | 1.11:1 |
| Phase 3 | R-037 to R-044 (8) | 8 (T03.01-T03.08) | 13 | 1.00:1 | 1.63:1 |
| **Total** | **44** | **44** | **52** | **1.00:1** | **1.18:1** |

The TDD+PRD tasklist-index.md states the generator rule: "1 task per roadmap item by default; splits only when item contains independently deliverable outputs."

**Finding: Both runs show a perfect 1:1 ratio of roadmap items to tasks.** The TDD+PRD run has MORE deliverables than tasks (52 vs 44) because some roadmap items produce multiple independently-verifiable deliverables (e.g., R-001 produces both D-0001 UserProfile table and D-0002 Audit log table; R-043 produces 4 documentation deliverables).

---

## 6. Comparative Summary Table

| Dimension | Baseline (spec-only) | TDD+PRD (enriched) | Delta |
|-----------|---------------------|---------------------|-------|
| Input documents | 1 (spec) | 2 (TDD + PRD) | +1 doc |
| Adversarial debate | Yes | Yes | Same |
| Roadmap phases | 5 | 3 | -2 phases |
| Phase model | Technical layers | Delivery milestones | Different paradigm |
| Roadmap subsections (####) | 20 | 24 | +4 subsections |
| Roadmap work items (table rows) | ~87 | ~112 | +25 items |
| Roadmap lines | 380 | 746 | +366 lines (1.96x) |
| Tasklist phases | 5 | 3 | Matches roadmap |
| Tasklist tasks | 87 | 44 | -43 tasks |
| Tasklist deliverables | 87 | 52 | -35 deliverables |
| Roadmap item registry (R-###) | 87 (R-001--R-087) | 44 (R-001--R-044) | -43 items |
| R-item to task ratio | 1:1 | 1:1 | Same |
| Task to deliverable ratio | 1:1 | 1:1.18 | TDD+PRD splits deliverables |
| Phase name fidelity | Exact match | Exact match | Same |
| Largest phase (tasks) | Phase 4 (22) | Phase 1 (27) | Different distribution |
| Tier: STRICT % | 55% | 45% (20/44) | -10pp |
| Tier: EXEMPT % | 14% | 14% (6/44) | Same |
| Complexity class | Not stated | HIGH | -- |

---

## 7. The Paradox: Fewer Tasks but More Content

The TDD+PRD roadmap is nearly 2x longer (746 vs 380 lines) yet produces fewer roadmap items (44 vs 87) and fewer tasks. This is because:

1. **Granularity difference at the roadmap level.** The baseline roadmap defines work at a fine-grained table-row level (e.g., separate rows for "Create users table migration" and "Create refresh_tokens table migration"). The TDD+PRD roadmap bundles related items into coarser roadmap items (e.g., "Provision PostgreSQL 15+ with UserProfile table schema including GDPR consent fields, audit log table, password hash column" is ONE item that covers what the baseline splits across 2-3).

2. **Wiring tasks and integration documentation.** The TDD+PRD roadmap contains extensive "Wiring Task" blocks (1.2.1 through 1.5.2, 2.1.1) that describe integration patterns, dependency injection configuration, dispatch tables, and callback chains. These add substantial line count but are not counted as separate roadmap items -- they are implementation guidance attached to parent items.

3. **PRD enrichment adds non-task content.** The PRD brings personas, business metrics, alert thresholds, rollback procedures, compliance checklists, risk mitigation roadmaps, success criteria measurement methods, cost estimates, and team composition. This adds ~200 lines of content that does not map to discrete tasks.

4. **The roadmap item registry is the true conversion unit.** The tasklist generator counts R-### items (explicitly enumerated in the Roadmap Item Registry table), not subsections or table rows. The TDD+PRD roadmap has 44 R-items; the baseline has 87. The generator converts each R-item to exactly one task.

---

## Gaps and Questions

1. **Why does the baseline have 2x more roadmap items despite a simpler input?** The baseline's technical-layer phasing creates many small, single-concern items (e.g., "Unit tests: hash timing ~250ms" is a standalone item). The TDD+PRD model bundles implementation + tests into single items. This suggests the roadmap generator produces different granularity depending on the phasing model, OR the adversarial debate resolution drives different decomposition strategies.

2. **Is the 1:1 R-item-to-task ratio a hardcoded rule or emergent?** The TDD+PRD tasklist-index.md explicitly states the rule: "1 task per roadmap item by default; splits only when item contains independently deliverable outputs." The baseline does not state this rule explicitly but exhibits the same behavior. Likely a deterministic rule in the tasklist generator.

3. **Phase 1 task concentration risk.** The TDD+PRD Phase 1 has 27 tasks (61% of all tasks) while the baseline distributes more evenly (16, 17, 17, 22, 15). This front-loading could create sprint execution bottlenecks. Is this a quality concern?

4. **Deliverable multiplication.** The TDD+PRD run produces 52 deliverables from 44 tasks (1.18:1 ratio) while the baseline has a strict 1:1 ratio. The TDD+PRD generator splits deliverables when a roadmap item "contains independently deliverable outputs." This suggests enriched inputs produce more granular verification artifacts even if task count is lower.

5. **Missing: How does the roadmap generator decide phase count?** The data shows the generator follows whatever phase structure the adversarial debate produces. The real question is: what in the debate prompt or input documents drives 3 vs 5 phases? The TDD+PRD metadata says `base_variant: "B (Haiku Architect)"` with `variant_scores: "A:71 B:79"` and the Haiku variant used progressive delivery phasing. The baseline does not include this metadata.

---

## Summary

The TDD+PRD roadmap has 3 phases because the PRD provides a rollout strategy (Alpha -> Beta -> GA) that the adversarial debate adopted as the phasing model. The baseline has 5 phases because, without a PRD, the debate defaulted to a technical-layer decomposition. The difference is not about more or fewer work items -- it is a fundamentally different organizational paradigm.

The tasklist generator exhibits **strict phase fidelity**: it preserves roadmap phase count, names, and ordering without reinterpretation. It applies a **1:1 roadmap-item-to-task** rule in both runs. The apparent paradox of "more content, fewer tasks" is explained by the TDD+PRD roadmap bundling more implementation detail per roadmap item and adding substantial non-task content (wiring docs, metrics, rollback procedures, compliance checklists).

The core insight is that **input document richness determines phase structure**, while the **tasklist generator is phase-structure-agnostic** -- it mechanically converts whatever R-items it finds into tasks, preserving the roadmap's organizational decisions.
