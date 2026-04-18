---
base_variant: "opus-architect"
variant_scores: "A:81 B:79"
---

# Roadmap Variant Evaluation

## 1. Scoring Criteria (Derived from Debate)

Ten criteria distilled from the eight debated divergence points and the convergence assessment:

| # | Criterion | Weight | Debate Source |
|---|-----------|--------|---------------|
| 1 | Spec Traceability | 10% | D-3 (task decomposition), frontmatter completeness |
| 2 | Architectural Rigor | 12% | D-2 (contract-first vs implementation-first) |
| 3 | Task Actionability | 12% | D-3 (wiring visibility), D-1 (phase granularity) |
| 4 | Integration Visibility | 10% | D-3/D-4 (wiring tasks, DI tracking) |
| 5 | Risk Management | 10% | Both variants' risk tables, R-1 through R-6 |
| 6 | Testing Strategy | 12% | D-6 (co-located vs consolidated) |
| 7 | Operational Readiness | 12% | D-13 (deployment scope), D-8 (feature flag timing) |
| 8 | Timeline Realism | 8% | D-10 (single-point vs range) |
| 9 | Team Fit | 7% | D-1 (phase granularity vs fractional resources) |
| 10 | Governance & Gates | 7% | D-1 (gates vs checkpoints), OQ closure model |

---

## 2. Per-Criterion Scores

### 2.1 Spec Traceability (weight: 10%)

| | Opus (A) | Haiku (B) |
|---|----------|-----------|
| Score | **85** | 75 |

**Justification**: Opus frontmatter tracks `extraction_ids_preserved: 55` and `derived_entity_ids: 37`, providing auditable provenance. SC-1 through SC-14 map directly to spec success criteria with explicit test references. Haiku maps FRs and NFRs thoroughly but lacks extraction-count metadata in frontmatter (`generated` and `generator` fields absent). Both trace every FR/NFR to tasks, but Opus's traceability table in Section 6 is more immediately auditable.

### 2.2 Architectural Rigor (weight: 12%)

| | Opus (A) | Haiku (B) |
|---|----------|-----------|
| Score | 78 | **85** |

**Justification**: Haiku's contract-first approach (COMP-005 through COMP-008) forces interface decisions to surface before implementation. As Haiku argued in Round 1, Topic 1: "the contract review is the cheapest possible moment to catch a misaligned abstraction boundary." The security engineer reviewing 200 lines of contracts vs. 2000 lines of implementation is a legitimate efficiency argument for security-sensitive code. However, this advantage applies primarily to the security-critical interfaces (JWT, TokenManager), not to all 9 contract tasks. Opus's architectural rigor is sound but implicit — the Phase 0 architecture decisions function as informal contracts.

### 2.3 Task Actionability (weight: 12%)

| | Opus (A) | Haiku (B) |
|---|----------|-----------|
| Score | **88** | 78 |

**Justification**: Opus's 92 tasks each represent a single working deliverable with concrete acceptance criteria. A developer picking up `FR-AUTH.2a` knows exactly what to build and how to verify it. Haiku's 130 tasks include many at S effort that are design/contract artifacts rather than working code (e.g., COMP-001 "Define auth module boundaries and package layout" — acceptance criteria: "Module boundaries documented; ownership agreed"). These are valuable design steps but less actionable as tracked work items for a 1-FTE backend team. The 12 explicit wiring tasks (DI-001 through DI-005, API-*.W1) are individually clear but, as Opus argued, the information they contain already exists in Opus's acceptance criteria.

### 2.4 Integration Visibility (weight: 10%)

| | Opus (A) | Haiku (B) |
|---|----------|-----------|
| Score | 72 | **88** |

**Justification**: Haiku's strongest structural contribution. `SecurityServiceContainer`, `AuthRouteRegistry`, and `AuthMiddlewareChain` are named artifacts with explicit ownership per phase and cross-references to consuming phases. As Haiku argued: "When someone asks 'what services does the auth module depend on?' in six months, `SecurityServiceContainer` answers that question." Opus tracks integration in Section 2 (Integration Points) and through acceptance criteria, but has no single artifact equivalent. The ~6 hours of overhead for explicit wiring tasks is negligible against the documentation value.

### 2.5 Risk Management (weight: 10%)

| | Opus (A) | Haiku (B) |
|---|----------|-----------|
| Score | **82** | 80 |

**Justification**: Both identify the same six risks and provide similar mitigations. Opus adds probability/severity ratings and a residual risk analysis (R-2 replay race condition). Haiku adds architect recommendations per risk ("Release should be blocked if key versioning is not operationally defined") and secondary delivery risks. These are roughly equivalent, with Opus's quantified ratings slightly more useful for prioritization.

### 2.6 Testing Strategy (weight: 12%)

| | Opus (A) | Haiku (B) |
|---|----------|-----------|
| Score | **80** | 78 |

**Justification**: This is close. Opus's co-located testing provides faster feedback — a bug in `PasswordHasher` surfaces in Phase 1, not Phase 3. Opus also includes cross-cutting tests (TEST-007 schema validation in Phase 2, TEST-009/010 security tests in Phase 4), contrary to Haiku's claim that co-located testing "naturally misses" cross-cutting concerns. However, Haiku's TEST-ARCH-001 (test strategy matrix) and TEST-ARCH-002 (test fixtures) are valuable planning artifacts that prevent ad-hoc test coverage. The debate converged on this: "a test strategy matrix should be defined early; individual tests should be written when their prerequisites are complete." Opus's distribution is closer to this consensus.

### 2.7 Operational Readiness (weight: 12%)

| | Opus (A) | Haiku (B) |
|---|----------|-----------|
| Score | **88** | 65 |

**Justification**: The largest gap between variants. Opus's Phase 5 includes 18 tasks covering staging deployment (OPS-007), production deployment (OPS-008), feature flag (OPS-006), and all SC validations. As Opus argued: "The roadmap's job is to deliver a working feature to production, not to hand off a validated codebase and hope someone else deploys it." With 0.25 FTE DevOps allocated in the spec, deployment is clearly in scope. Haiku's `OperationalReadinessChecklist` is a checklist without tasks — necessary but insufficient. Haiku's early feature flag (OPS-003 in Phase 1) is a legitimate advantage the debate converged on, but it doesn't compensate for the missing deployment plan.

### 2.8 Timeline Realism (weight: 8%)

| | Opus (A) | Haiku (B) |
|---|----------|-----------|
| Score | **80** | 76 |

**Justification**: Opus's 7.5 weeks includes deployment; Haiku's 5.5-7 weeks excludes it. As Opus rebutted: "If you add deployment to Haiku's estimate (~0.5–1 week), the range becomes 6–8 weeks." Haiku's range-based estimate is more honest about uncertainty (8 open questions), but the lower bound of 5.5 weeks is optimistic for 130 tasks with a fractional team. Opus's parallelization note (Phase 2+3 concurrent = 6.5 weeks) provides a concrete compression lever. Both are reasonable; Opus's is more complete.

### 2.9 Team Fit (weight: 7%)

| | Opus (A) | Haiku (B) |
|---|----------|-----------|
| Score | **80** | 78 |

**Justification**: Opus provides explicit FTE allocations per phase (1 backend, 0.5 security, 0.5 QA, 0.25 DevOps). Haiku raises a valid concern about 6-phase reviews for fractional resources ("scheduling 6 reviews across 7.5 weeks means a review almost every week — constant context-switching for part-time contributors"). However, Opus's argument that gates are safer than checkpoints for security-sensitive code is compelling. The fractional resource scheduling concern is real but manageable — 1-hour reviews weekly is not unreasonable.

### 2.10 Governance & Gates (weight: 7%)

| | Opus (A) | Haiku (B) |
|---|----------|-----------|
| Score | 78 | **84** |

**Justification**: Haiku's explicit release gate recommendation (Section 5.4) is cleaner than Opus's implicit "all SC pass in Phase 5" approach. Haiku requires: SC-1 through SC-14 green, OQ-1/3/7/8 closed, R-1/2/4 reviews complete, feature flag and migration rollback proven, security leakage tests green. This is a binary go/no-go checklist. Haiku's evidence-based OQ closure (decisions validated by test results, not just stakeholder sign-off) is the stronger model, as the debate converged: "a decision validated by a load test" provides higher confidence than "a decision documented with stakeholder sign-off."

---

## 3. Overall Scores

| Criterion | Weight | Opus (A) | Haiku (B) | A Weighted | B Weighted |
|-----------|--------|----------|-----------|------------|------------|
| Spec Traceability | 10% | 85 | 75 | 8.5 | 7.5 |
| Architectural Rigor | 12% | 78 | 85 | 9.4 | 10.2 |
| Task Actionability | 12% | 88 | 78 | 10.6 | 9.4 |
| Integration Visibility | 10% | 72 | 88 | 7.2 | 8.8 |
| Risk Management | 10% | 82 | 80 | 8.2 | 8.0 |
| Testing Strategy | 12% | 80 | 78 | 9.6 | 9.4 |
| Operational Readiness | 12% | 88 | 65 | 10.6 | 7.8 |
| Timeline Realism | 8% | 80 | 76 | 6.4 | 6.1 |
| Team Fit | 7% | 80 | 78 | 5.6 | 5.5 |
| Governance & Gates | 7% | 78 | 84 | 5.5 | 5.9 |
| **Total** | **100%** | | | **81.6** | **78.6** |

**Opus (Variant A): 81.6 | Haiku (Variant B): 78.6**

The 3-point gap is modest, reflecting genuinely different strengths. Opus wins on actionability, operational completeness, and spec traceability. Haiku wins on architectural rigor, integration visibility, and governance. Neither variant is clearly superior across all dimensions — this is a merge scenario, not a replacement.

---

## 4. Base Variant Selection Rationale

**Selected base: Opus (Variant A)**

Three factors drive this selection:

1. **Operational completeness is harder to retrofit than architectural rigor.** Adding contracts, named artifacts, and a release gate to Opus requires inserting ~15 tasks into existing phases. Removing Haiku's deployment gap requires designing an entire new phase with staging/production tasks, feature flag wiring, and deployment sequencing — work Opus has already done.

2. **Task structure favors the merge direction.** Opus's 92-task, one-deliverable-per-task structure is a cleaner merge target. Adding Haiku's named artifacts and contract tasks to Opus is additive. Restructuring Haiku's 3-phase model to accommodate Opus's deployment phase would require redistributing 50+ tasks across phase boundaries.

3. **Frontmatter and traceability metadata.** Opus's frontmatter (`total_phases`, `total_task_rows`, `extraction_ids_preserved`, `derived_entity_ids`) provides the structural metadata needed for downstream tooling (tasklist generation, validation). Adding this to Haiku would require re-counting after restructuring.

---

## 5. Specific Improvements from Haiku (Variant B) to Incorporate in Merge

### 5.1 Must Incorporate (Debate Convergence Points)

| # | Improvement | Source | Target Location | Rationale |
|---|-------------|--------|-----------------|-----------|
| 1 | **Early feature flag** — move `AUTH_SERVICE_ENABLED` from Phase 5 to Phase 0 | OPS-003 (Haiku Phase 1) | Opus Phase 0, after COMP-006 | Debate converged: "low cost and moderate testing benefit; net positive." Enables regression testing with flag on/off across all phases. |
| 2 | **Test strategy matrix** — add `TEST-ARCH-001` to Phase 0 | TEST-ARCH-001 (Haiku Phase 1) | Opus Phase 0, after OQ resolution block | Debate converged: "a test strategy matrix should be defined early." Maps every FR/NFR to verification type before implementation begins. |
| 3 | **Evidence-based OQ closure** — add validation tasks for OQ-1, OQ-3, OQ-7, OQ-8 in Phase 5 | OQ-1 through OQ-8 (Haiku Phase 3) | Opus Phase 5, alongside SC validations | Debate converged: "early decision + later validation is the strongest combined approach." Adds ~8 S-effort tasks linking OQ decisions to measured evidence. |
| 4 | **Mid-phase checkpoint** — add Checkpoint B between Phase 2 and Phase 3 | Checkpoint B (Haiku mid-Phase 2) | Opus between Phase 2 milestone and Phase 3 start | Debate converged: "some form of mid-implementation checkpoint is warranted for the largest implementation block." Advisory, not blocking. |

### 5.2 Should Incorporate (Strong Haiku Advantages)

| # | Improvement | Source | Target Location | Rationale |
|---|-------------|--------|-----------------|-----------|
| 5 | **Named integration artifacts** — introduce `SecurityServiceContainer` and `AuthRouteRegistry` as named artifacts in Integration Points section | Haiku Phase 1 artifacts | Opus Section 2 (Integration Points) | Haiku scored 88 vs Opus 72 on integration visibility. Named artifacts provide long-term documentation value at zero task overhead — they're labels, not tasks. |
| 6 | **Security-interface contracts** — add contract definitions for JWT service (COMP-005) and TokenManager (COMP-007) interfaces only | COMP-005, COMP-007 (Haiku Phase 1) | Opus Phase 0, before COMP-002 and COMP-003 | Per debate synthesis: "contract definitions for security-sensitive interfaces only." The 0.5 FTE security engineer reviews 2 interface specs (~50 lines) in Phase 0 instead of reviewing full implementation in Phase 4. Not all 9 Haiku contracts — only JWT and TokenManager where interface misalignment has the highest downstream cost. |
| 7 | **Explicit release gate criteria** — add Section 5.4-style release gate checklist | Haiku Section 5.4 | Opus Section 6 (after validation strategy) | Haiku's binary go/no-go checklist ("Release only when all are true: SC-1 through SC-14 green, OQ-1/3/7/8 closed, R-1/2/4 complete, rollback proven") is cleaner than Opus's implicit "all Phase 5 tasks pass." |
| 8 | **Test fixture planning** — add `TEST-ARCH-002` for shared test fixture definitions | TEST-ARCH-002 (Haiku Phase 1) | Opus Phase 0, after TEST-ARCH-001 | Shared fixtures (locked accounts, expired tokens, revoked sessions) prevent duplication across Phases 1-4 test tasks. |

### 5.3 Do Not Incorporate

| # | Haiku Element | Reason to Exclude |
|---|---------------|-------------------|
| 1 | Explicit DI binding tasks (DI-001 through DI-005) | Acceptance criteria in Opus's COMP tasks already cover runtime resolution. Adding separate DI tasks doubles tracking for a 1-FTE team. |
| 2 | Route wiring tasks (API-*.W1) | Opus's API-001 through API-006 already include "route registered" in acceptance criteria. Splitting registration from wiring creates two tasks where one suffices. |
| 3 | Consolidated Phase 3 testing | Opus's co-located testing provides faster feedback. The test strategy matrix (incorporated above) addresses completeness without consolidation. |
| 4 | 3-phase structure | 6 phases with gates are safer for security-sensitive code, per Opus's rebuttal. The mid-phase checkpoint (incorporated above) addresses Haiku's scheduling concern. |
| 5 | All 9 contract definitions | Contracts for non-security interfaces (auth module boundaries, user domain model, route skeletons) add overhead without proportional value for 1 FTE. Only JWT and TokenManager contracts are worth the interface-stability guarantee. |
| 6 | Deployment-excluded scope | The spec allocates 0.25 FTE DevOps. Deployment belongs in the roadmap. |

### 5.4 Estimated Merge Impact

Adding the 4 must-incorporate and 4 should-incorporate items adds approximately **12-14 tasks** to Opus's 92, bringing the total to ~104-106 tasks. Phase 0 grows by ~1 day (contracts + test strategy + feature flag). Phase 5 grows by ~0.5 days (OQ closure evidence). Total timeline impact: negligible (< 0.5 weeks), as most additions are S-effort.
