---
total_diff_points: 12
shared_assumptions_count: 14
---

## Shared Assumptions and Agreements

Both variants converge on the following:

1. **Same spec source and complexity:** Both derive from TDD_TASK_BUILDER_CONVERGENCE.compressed.md with complexity_score 0.7 (HIGH) and primary_persona "architect".
2. **Same FR landing order:** PR-06 → PR-01 → PR-04 → PR-07 → PR-02 → PR-03, mapping to FR-CONV.1 → .2 → .3 → .4 → .5 → .6.
3. **Same critical blocker:** Q-DM-1 (per-item schema PRD-vs-source contradiction) must be resolved by Engineering Lead before FR-CONV.1.
4. **Strictly-additive governance (A-002):** No existing item renamed, renumbered, removed, or weakened.
5. **No new external dependencies (NFR-CONV.5):** Only Read/Grep/Glob/Bash; no MCP servers, no synchronous network calls.
6. **Token-cost ceiling NFR-CONV.4 ≤1.10** measured on 5 representative BUILD_REQUESTs.
7. **Determinism scope split:** Structural fields byte-deterministic (NFR-CONV.1); research-prose nondeterminism acceptable (NFR-CONV.2).
8. **Anti-inflation preservation:** rf-qa-qualitative.md:766-775 byte-stable; FR-CONV.3 is reliance-only with mandatory Self-Audit (INV-019).
9. **All-agents-fail guard precedence:** Zero partitions succeeded → no synthetic-dnsp; rf-team-lead.md:417 escalation activates.
10. **Same 8 TB-Add checks and 5 adversarial axes (AX-1..5 + none + drift-axis-inactive).**
11. **Same retry halt precedence:** regression > monotonicity > 3-cycle hard cap > proceed.
12. **Same DM-003 7-field DNSP schema** with dedup_key 2-tuple and found_n_times.
13. **K-003 audit window:** First 5 rf-qa-qualitative runs post-FR-CONV.3 audited by QA Lead.
14. **Total duration ~14 weeks** within 2026-Q3 GA target.

## Divergence Points

### 1. Milestone Decomposition Strategy

- **Opus variant:** 7 milestones, one per FR-CONV.X (M1=FR-CONV.1, M2=FR-CONV.2, ..., M6=FR-CONV.6, M7=audit/GA). Each milestone is 2 weeks.
- **Haiku variant:** 5 milestones grouping by technical layer (M1=Contracts/Foundations, M2=FR-CONV.1+.2, M3=FR-CONV.3+.4, M4=FR-CONV.5+.6, M5=Validation/Rollout).
- **Impact:** Opus offers finer per-FR rollback granularity and clearer 1:1 mapping to PRs; Haiku offers cleaner thematic layering and a dedicated upfront contract-freeze phase but couples sibling FRs into a single milestone gate.

### 2. Contract Definition Timing

- **Opus variant:** DM/API contracts defined inline within their consuming FR milestone (e.g., DM-001 inside M2/FR-CONV.2).
- **Haiku variant:** Dedicated M1 "Decision and Contract Foundation" front-loads all DM-001..005, API-001..004, COMP-001..006, and NFR contracts before any FR implementation.
- **Impact:** Haiku's front-loaded approach establishes a stable contract surface and may catch contract conflicts early; Opus's just-in-time approach keeps contracts colocated with their first consumer, which may better match how iterative implementation reveals contract needs.

### 3. Item Count Per Milestone

- **Opus variant:** M1=23, M2=17, M3=21, M4=20, M5=21, M6=29, M7=20 (total ~151 items).
- **Haiku variant:** M1=26, M2=18, M3=17, M4=12, M5=23 (total ~96 items).
- **Impact:** Opus is more granular with explicit feature-flag, mitigation, and integration sub-items per milestone; Haiku is more compact, treating some adjacent concerns as implicit. Opus offers more checkpointing; Haiku reduces tracking overhead.

### 4. Timeline Anchoring

- **Opus variant:** Concrete dates per milestone (2026-05-15 → 2026-08-21) with explicit start/end for each.
- **Haiku variant:** Week-relative scheduling (Week 1-14) anchored to "TDD Design Complete 2026-05-21" and Q-DM-1 resolution, without committing to specific calendar dates.
- **Impact:** Opus commits to a concrete schedule useful for stakeholder commitments; Haiku preserves flexibility against the Q-DM-1 unblock date.

### 5. Operations Runbook Treatment

- **Opus variant:** OPS-001..007 land in M7 (final milestone) alongside observability counters.
- **Haiku variant:** OPS-001..007 land in M5 along with MET-001..006 measurement items as numbered deliverables, plus dedicated FLAG-* logical-flag governance entries.
- **Impact:** Functionally equivalent; Haiku makes metrics and flag governance more visible as named line items; Opus folds them into narrative integration-point tables.

### 6. Open Questions Placement

- **Opus variant:** Q-DM-1 in M1; OPEN-INV-006 in M5; OPEN-X-002 in M3; OPEN-TOKEN in M7. Each question lives where it's relevant.
- **Haiku variant:** Q-DM-1 and OPEN-INV-018 in M1 (front-loaded); OPEN-INV-006 in M2; OPEN-X-002 in M3; OPEN-PR05, OPEN-INV-017, OPEN-TOKEN all in M5.
- **Impact:** Haiku consolidates more open questions to early and final milestones; Opus distributes them to point-of-impact. Haiku increases M5 open-question pressure; Opus risks late surfacing of OPEN-INV-018.

### 7. OPEN-INV-018 Treatment

- **Opus variant:** Listed in M1 Open Questions but flagged as pre-M1 entry gate alongside Q-DM-1.
- **Haiku variant:** Listed in M1 with target "Before M2 implementation starts" — treated as gate to M2.
- **Impact:** Both protect against `.dev/tasks/` layout drift, but Haiku makes the dependency more procedurally explicit.

### 8. Component (COMP-*) Surface Definition

- **Opus variant:** COMP-001..006 referenced inline as the "Comp" column on each row but not separately enumerated as distinct deliverables.
- **Haiku variant:** COMP-001..006 explicitly enumerated as M1 deliverables (Orchestrator, rf-task-builder, rf-qa, rf-qa-qualitative, rf-analyst, rf-team-lead-preservation) with type/location/modifies/anchors metadata.
- **Impact:** Haiku gives clearer architectural surface map upfront; Opus assumes the reader infers component scope from FR-anchored edits.

### 9. NFR Treatment

- **Opus variant:** NFR-CONV.1, .5 land in M1; NFR-CONV.7 in M2; NFR-CONV.10 in M6; NFR-CONV.2..4, .8, .9 in M7. NFRs are distributed by enforcement point.
- **Haiku variant:** All NFR-CONV.1..10 + NFR-CONV-R1 land as numbered M1 deliverables (rows 16-26), measured/validated in M5.
- **Impact:** Haiku front-loads NFR definitions for a consolidated NFR contract; Opus places NFRs at their natural enforcement point, which may better reflect when they actually become testable.

### 10. Feature Flag Governance Visibility

- **Opus variant:** Feature flags appear as final row(s) within each FR-CONV.X milestone (FF_TB_ADD_1_THROUGH_8, FF_EXECUTION_CONTEXT_HEADER, etc.).
- **Haiku variant:** Logical flags consolidated in M5 as FLAG-TB-ADD-1-8, FLAG-EXECUTION-CONTEXT, FLAG-INHERITED-VERDICT, FLAG-FIVE-AXES, FLAG-RETRY-GUARDS, FLAG-DNSP-EMISSION.
- **Impact:** Opus ties each flag to its FR for lifecycle co-location; Haiku centralizes flag governance in the rollout milestone — easier to audit collectively but disconnected from FR landing.

### 11. Test Fixture Distribution

- **Opus variant:** Tests numbered TEST-001..025 are distributed to their corresponding FR milestone (TEST-001..003 in M1; TEST-004..006 in M2; etc.); TEST-023..025 in M7.
- **Haiku variant:** Tests largely follow the same distribution but TEST-024 (sequencing fixture) appears in M5 rather than M5 of Opus's mapping where it appears in M5/FR-CONV.5; TEST-022 (synthetic-dedup-not-regression) explicitly placed in M4.
- **Impact:** Minor difference; both variants validate the same 25-fixture suite.

### 12. Dependency Graph Presentation

- **Opus variant:** Detailed ASCII dependency graph with mutual-coupling annotations (e.g., "M5/M6 mutual-shape coupling").
- **Haiku variant:** Simple linear arrow graph: Q-DM-1 → M1 → M2 → M3 → M4 → M5.
- **Impact:** Opus surfaces critical coupling (FR-CONV.5 ↔ FR-CONV.6 dedup-key shape) explicitly; Haiku's flatter graph hides intra-milestone coupling because adjacent FRs are bundled.

## Areas Where One Variant Is Clearly Stronger

**Opus is stronger at:**
- **Rollback granularity:** Per-FR milestones make per-FR rollback first-class; matches the release-spec's stated SP-10 per-FR rollback goal.
- **Mutual-coupling visibility:** Explicit dependency-graph annotations call out FR-CONV.5 ↔ FR-CONV.6 dedup-key coupling and FR-CONV.3 ↔ FR-CONV.1 INV-010 enumeration.
- **Concrete scheduling:** Calendar-anchored dates and per-milestone calendar windows aid stakeholder commitments.
- **Per-FR feature-flag colocation:** Feature flags tied to their FR's lifecycle.

**Haiku is stronger at:**
- **Contract-first architecture:** Dedicated M1 freezes all DM/API/COMP/NFR surfaces before implementation, reducing mid-implementation contract churn.
- **Architectural surface map:** Explicit COMP-001..006 enumeration provides a clearer mental model of the modification surface.
- **Reduced tracking overhead:** 5 milestones vs 7 reduces context-switching and ceremony.
- **Centralized governance:** FLAG-* and MET-* numbered items make release-readiness collectively auditable in M5.

## Areas Requiring Debate to Resolve

1. **Milestone granularity (Divergence 1, 3):** Should the roadmap optimize for per-FR rollback granularity (Opus) or thematic layering with reduced overhead (Haiku)? The release-spec §9 SP-10 per-FR rollback requirement may favor Opus, but Haiku does not foreclose per-FR rollback — it just doesn't make milestone boundaries align with FR boundaries.
2. **Contract definition timing (Divergence 2):** Is upfront contract freeze worth the risk of premature commitment, or does just-in-time definition better match iterative implementation discovery?
3. **NFR placement (Divergence 9):** Should NFRs be defined as one consolidated contract surface (Haiku) or distributed to their enforcement point (Opus)?
4. **Feature-flag governance (Divergence 10):** Co-locate flags with FR lifecycle (Opus) or centralize in rollout milestone (Haiku)?
5. **Schedule commitment (Divergence 4):** Calendar-anchored dates (Opus) or week-relative flexibility (Haiku) — which better matches Q-DM-1 unblock-date uncertainty?
6. **OPS/MET visibility (Divergence 5):** Should operations runbooks and metrics be numbered M5 deliverables (Haiku) or M7 narrative integration points (Opus)?
