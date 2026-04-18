---
base_variant: "A (Opus-Architect)"
variant_scores: "A:78 B:72"
---

# Evaluation: Opus-Architect vs Haiku-Architect Roadmaps

## 1. Scoring Criteria (Derived from Debate)

The debate surfaced 18 divergence points across 6 clusters. I distilled these into 10 evaluation criteria, weighted by their impact on roadmap utility as a planning and execution artifact.

| # | Criterion | Weight | Rationale |
|---|-----------|--------|-----------|
| 1 | Spec Fidelity & Extraction Coverage | 10% | All FR/AC/SC/RISK/GAP/OQ IDs must appear as traceable tasks |
| 2 | Phase Structure & Gate Quality | 12% | Debate Cluster 1 (D-1): milestone clarity, single-purpose phases |
| 3 | Test Timing & Defect Discovery | 12% | Debate Cluster 1 (D-3, D-8): early detection vs. settled interfaces |
| 4 | Security Placement & Completeness | 10% | Debate Cluster 4 (D-14): distributed validation vs. holistic review |
| 5 | Integration Documentation | 8% | Debate Cluster 4 (D-7): global map vs. per-phase notes |
| 6 | Operational Readiness | 10% | Debate Cluster 6 (D-9, D-10): rollback, runbooks, ownership |
| 7 | Task Granularity & Trackability | 10% | Debate Cluster 2 (D-4, D-11-13): component count, OQ tracking |
| 8 | Timeline & Planning Utility | 10% | Debate Cluster 5 (D-15): critical path, multi-dev estimates |
| 9 | Risk Management | 8% | Both agreed on risk priorities; evaluation focuses on actionability |
| 10 | Architectural Pragmatism | 10% | Debate Cluster 3 (D-5, D-6): YAGNI vs. operational pragmatism |

## 2. Per-Criterion Scores

### C1: Spec Fidelity & Extraction Coverage (weight 10%)

| Aspect | A (Opus) | B (Haiku) |
|--------|----------|-----------|
| FR coverage | All FR-AUTH.1 through FR-AUTH.5 with sub-items (1a-1d, 2a-2d, 3a-3d, 4a-4c, 5a-5d) | All FRs covered but sub-items less granular — FR-AUTH.2 is one task, not 4 |
| AC coverage | AC-1 through AC-10, each a distinct task | AC-1 through AC-10 present, same coverage |
| SC validation | Single TEST-017 covering all 22 SC | Distributed: SC-1, SC-11, SC-20, SC-21, SC-22 as Phase 4; SC-2, SC-4, SC-5, SC-9, SC-12, SC-16, SC-19 in Phase 5 |
| GAP/OQ | Mentioned in prose with phase assignments | GAP-1/2/3 and OQ-1 through OQ-7 as trackable tasks with resolution tasks (OQ-1A, OQ-2A) |

**Score**: A: 8 / B: 8. Both achieve full extraction coverage. A has finer FR sub-task decomposition; B has better OQ/SC traceability. These offset.

---

### C2: Phase Structure & Gate Quality (weight 12%)

**Variant A**: 7 phases with single-purpose objectives (infra → crypto → tokens → auth service → HTTP → security → release). Each phase gate is unambiguous — "Phase 2 complete" means crypto primitives work, nothing more. Milestones are concrete and verifiable.

**Variant B**: 5 broader phases. Phase 1 bundles schema, crypto components, AND repository abstractions. Phase 2 bundles token lifecycle, AuthService, AND API contracts. Broader phases mean fewer ceremonies but less precise "done" definitions.

The debate convergence did not resolve this dispute (marked as "team process decision"), but Opus's 7-phase structure was explicitly recommended in the synthesis as providing "finer gates." For a security-sensitive system, more frequent verification points reduce risk accumulation.

**Score**: A: 9 / B: 7

---

### C3: Test Timing & Defect Discovery (weight 12%)

**Variant A**: Tests co-located with implementation. TEST-001 through TEST-004 ship in Phase 2 alongside PasswordHasher/JwtService. Defects in crypto primitives found in Week 1. However, SC validation is monolithic (TEST-017) — a "black box that passes or fails with no granular visibility" (Haiku's rebuttal).

**Variant B**: Tests concentrated in Phase 4. Developer testing is implicit during Phases 1-3; formalized tests arrive against settled interfaces. SC validation is distributed across 12+ tasks with per-criterion evidence. However, the debate acknowledged this creates late-discovery risk for fundamental design issues.

The convergence assessment explicitly states: "hybrid test timing is optimal — unit tests co-located with implementation, integration and security tests concentrated in a validation phase." A's co-located approach is closer to this hybrid; B requires more structural change to adopt it.

**Score**: A: 8 / B: 6

---

### C4: Security Placement & Completeness (weight 10%)

**Variant A**: Dedicated Phase 6 (Security Hardening & Performance) with RISK-1/2/3 validation, TEST-015 security suite, and holistic review. Provides a clean milestone for security engineering review. Weakness: security defects found in Phase 6 require changes to Phases 1-5 code.

**Variant B**: Distributed validation — AC-6 in Phase 1, RISK-1/AC-7 in Phase 3, replay validation in Phase 2. Catches issues at point of construction. Weakness: no explicit holistic review milestone.

The convergence explicitly states both are needed: "validate individual security controls when built (Haiku's approach), then conduct a formal security review milestone before release (Opus's Phase 6 reframed as a review)." A has the review milestone that B lacks; B's distributed approach is easier to add to A than adding a review milestone to B.

**Score**: A: 7 / B: 7

---

### C5: Integration Documentation (weight 8%)

**Variant A**: Global Section 2 with 5 named integration artifacts (DI container, route registration, middleware chain, feature flag, migration registry). Provides an architectural map of the entire system in one place.

**Variant B**: Per-phase integration points (3-4 per phase) with named artifacts, wired components, owning phase, and cross-references. More actionable for developers working within a phase.

The convergence states "the optimal approach is both — a brief global wiring overview plus per-phase integration notes." A has the global overview; B has the per-phase notes. Both are incomplete. A's Section 2 is a stronger architectural artifact; B's per-phase notes are more operationally useful.

**Score**: A: 8 / B: 8

---

### C6: Operational Readiness (weight 10%)

**Variant A**: Single comprehensive runbook (OPS-005 in Phase 7), health check in Phase 1 with concrete criteria (GET /health, <50ms), key rotation automation (OPS-002). No explicit rollback rehearsal task — buried in TEST-018.

**Variant B**: Separate runbooks (OPS-003 deployment, OPS-004 key rotation, OPS-005 alerting, OPS-006 staged rollout), explicit rollback rehearsal (MIG-003) with staging criteria, ownership map (COMP-017). Email interface defined in Phase 1 (DEP-3).

The convergence favored B on rollback rehearsal ("the validation deserves its own task") and early email interface ("surfacing procurement lead time"). A's health check placement and concrete criteria are strengths B lacks. But B's operational artifact set is significantly more complete and parallelizable.

**Score**: A: 6 / B: 9

---

### C7: Task Granularity & Trackability (weight 10%)

**Variant A**: 94 tasks, 11 components. FR sub-items decomposed (e.g., FR-AUTH.1a through 1d as separate tasks). OQ resolution mentioned in prose ("resolve before Phase N"). SC validation monolithic.

**Variant B**: ~100 tasks, 17 components. OQ resolution as explicit tasks with assignment (OQ-3, OQ-7 in Phase 1; OQ-1, OQ-2 in Phase 2) and resolution recording tasks (OQ-1A, OQ-2A). SC validation distributed with evidence linking. But COMP-013/014/015/016 may be thin wrappers inflating count.

The debate convergence explicitly favored B's OQ tracking approach: "prose directives are not tracked in sprint boards, not assignable, and not verifiable." A's FR sub-task decomposition is a counterbalancing strength. The 17-component question remains unresolved, but OQ trackability is a clear B advantage.

**Score**: A: 7 / B: 8

---

### C8: Timeline & Planning Utility (weight 10%)

**Variant A**: 4-5 weeks (1 dev), 2.5-3.5 weeks (2 dev). ASCII critical path diagram showing exact task dependencies. Per-phase duration estimates with parallelism notes. Tighter range enables sprint commitment.

**Variant B**: 5.0-7.5 engineering weeks (50% range). Per-phase textual breakdown. No critical path diagram. No multi-developer estimate.

A is clearly superior here. The debate's convergence stated "both estimates should be presented with the critical path diagram from Opus and the uncertainty acknowledgment from Haiku," but the structural planning artifacts (critical path, dual estimates) are firmly A's contribution.

**Score**: A: 9 / B: 5

---

### C9: Risk Management (weight 8%)

**Variant A**: Structured risk table with severity, mitigation strategy, phase addressed, and validation task cross-references. Gap-derived risks with timeline. Architectural risk section on OQ schedule impact.

**Variant B**: Narrative risk assessment with "why it matters," mitigation strategy, and release gate per risk. Gap-derived risks with recommended architect actions. Similar coverage, slightly more operational in tone.

Both are solid. A's tabular format is more scannable; B's narrative format provides more context. A's OQ schedule risk analysis is a unique strength.

**Score**: A: 8 / B: 7

---

### C10: Architectural Pragmatism (weight 10%)

**Variant A**: 11 components, minimal refresh token schema (boolean revoked flag), 3 separate migrations, cross-cutting concerns inline. YAGNI-aligned. Appropriate for 2-3 person team.

**Variant B**: 17 components, rich refresh token schema (revoked_at timestamp, replaced_by_token_id, created_ip, user_agent), 2 atomic migrations, every concern a named artifact. Pattern-consistent. Appropriate for 5+ person team.

The convergence noted `revoked_at` as a "zero-cost improvement" over boolean — I agree. But `replaced_by_token_id` and client metadata columns are genuinely debatable, and the 6 extra components add indirection. For the stated medium complexity (0.6), A's pragmatism is better calibrated while B risks over-engineering.

**Score**: A: 8 / B: 7

---

## 3. Overall Scores with Justification

| Criterion | Weight | A Score | B Score | A Weighted | B Weighted |
|-----------|--------|---------|---------|------------|------------|
| Spec Fidelity | 10% | 8 | 8 | 8.0 | 8.0 |
| Phase Structure | 12% | 9 | 7 | 10.8 | 8.4 |
| Test Timing | 12% | 8 | 6 | 9.6 | 7.2 |
| Security Placement | 10% | 7 | 7 | 7.0 | 7.0 |
| Integration Docs | 8% | 8 | 8 | 6.4 | 6.4 |
| Operational Readiness | 10% | 6 | 9 | 6.0 | 9.0 |
| Task Trackability | 10% | 7 | 8 | 7.0 | 8.0 |
| Timeline & Planning | 10% | 9 | 5 | 9.0 | 5.0 |
| Risk Management | 8% | 8 | 7 | 6.4 | 5.6 |
| Architectural Pragmatism | 10% | 8 | 7 | 8.0 | 7.0 |
| **Totals** | **100%** | | | **78.2** | **71.6** |

**Variant A (Opus): 78** | **Variant B (Haiku): 72**

A leads by 6 points. The margin is driven by three structural advantages: phase granularity (+2.4), test timing alignment with convergence recommendation (+2.4), and timeline/planning utility (+4.0). B's operational readiness advantage (+3.0) and task trackability edge (+1.0) partially offset but do not close the gap.

## 4. Base Variant Selection Rationale

**Selected base: Variant A (Opus-Architect)**

The selection is driven by structural considerations — A's foundational architecture is harder to retrofit into B than B's improvements are to graft onto A:

1. **Phase skeleton**: A's 7-phase structure provides finer gates that the convergence assessment recommended. Converting B's 5 phases into 7 would require splitting Phase 1 (foundations+crypto+repositories becomes infra+crypto) and Phase 2 (token lifecycle+auth+contracts becomes tokens+auth service), fundamentally reorganizing the document. Adding B's improvements to A's existing phases is additive, not restructuring.

2. **Test placement**: Moving from co-located (A) to hybrid requires adding a concentrated validation phase — achievable by augmenting A's Phase 7. Moving from concentrated (B) to hybrid requires distributing tests backward into Phases 1-3, which contradicts B's structural premise.

3. **Planning artifacts**: A's critical path diagram and dual-developer estimates are structural elements that B completely lacks. Adding these to B would require re-analyzing all of B's dependencies.

4. **Frontmatter completeness**: A includes `total_task_rows: 94`, `granularity_floor_target: 80`, and `extraction_ids_preserved: true` — metadata that supports toolchain integration.

## 5. Specific Improvements from Variant B to Incorporate in Merge

The following B elements should be integrated into the A base, ordered by priority:

### Must Incorporate (convergence-agreed)

1. **Contract-first API definitions** (B's Phase 2, API-001 through API-006): Move API contract definition tasks from A's Phase 5 to A's Phase 3 or early Phase 4. The debate convergence explicitly states "contracts-as-test-targets provide value even on a single team." Define contracts before route implementation so integration tests have targets.

2. **Explicit rollback rehearsal task** (B's MIG-003): Add a standalone rollback rehearsal task in A's Phase 7 (or late Phase 6) with B's staging criteria: "feature flag disablement plus down migration restore pre-auth state without orphaned data structures." Do not leave this buried inside TEST-018.

3. **OQ tracking as explicit tasks** (B's OQ-3/OQ-7 in Phase 1, OQ-1/OQ-2 in Phase 2, OQ-1A/OQ-2A in Phase 5): Replace A's prose-based OQ references with assignable, trackable tasks at the phases where decisions must be made. Add resolution-recording tasks (OQ-1A, OQ-2A) to make decision debt visible to project managers.

4. **Early email interface definition** (B's DEP-3 in Phase 1): Move A's DEP-3 from Phase 4 to Phase 1. Define the EmailDispatcher interface early to surface procurement lead time. Implementation remains deferred to Phase 4.

5. **Distributed SC validation with evidence linking**: Replace A's monolithic TEST-017 with individual SC verification tasks (following B's pattern of SC-1, SC-11, SC-20, etc.) spread across Phases 6-7. Each task links to specific test evidence. Retain a final SC-ALL coherence check but make individual criteria independently auditable.

6. **`revoked_at` timestamp over boolean**: In A's DM-002 (RefreshTokens schema), replace `revoked (boolean, default false)` with `revoked_at (timestamptz, nullable)`. Zero-cost improvement that provides incident timeline data. Check `IS NOT NULL` replaces `= true`.

### Should Incorporate (strong value-add)

7. **Per-phase integration notes** (B's "Integration points for Phase N" sections): Supplement A's global Section 2 with per-phase integration summaries. Each phase gets a brief subsection listing named artifacts created/consumed in that phase with cross-references. This provides both the architectural map (A's Section 2) and the developer-actionable notes (B's per-phase approach).

8. **PasswordResetRepository** (B's COMP-010 as a repository): Add a PasswordResetRepository to A's Phase 2 alongside COMP-008/009. The debate did not converge on this, but pattern consistency across all three token-related tables reduces cognitive load and is a low-cost addition (4 methods, one test suite).

9. **Ownership map** (B's COMP-017): Add a task in A's Phase 7 to publish a component ownership matrix. The debate rebuttal about "organizational process vs. architecture" has merit, but making it a deliverable ensures operational responsibility is explicit at launch.

### Defer to Team Decision (unresolved in debate)

10. **Additional components COMP-013/014/015/016**: Do not add B's auth context model, route-handler adapter, error mapping strategy, or cookie transport handler as separate components. The debate did not resolve this, and A's inline approach is more pragmatic at the stated complexity. If the team is >3 developers, reconsider.

11. **`replaced_by_token_id` and client metadata columns**: Do not add to base merge. The YAGNI argument holds for strict v1.0. Include a decision note referencing the trade-off for the team to resolve based on whether security incident investigation is an organizational priority.

12. **Migration granularity (3 vs 2)**: Retain A's 3 separate migrations. The debate showed Opus's surgical rollback benefit is real, and Haiku's rebuttal ("future changes get new migrations anyway") does not negate the value of independent initial table lifecycle.
