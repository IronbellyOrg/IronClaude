---
total_diff_points: 18
shared_assumptions_count: 16
---

# Comparative Diff Analysis: Opus-Architect vs Haiku-Architect Roadmaps

## 1. Shared Assumptions and Agreements

Both variants agree on these 16 foundational positions:

1. **RS256 asymmetric JWT signing** (AC-1) with secrets-manager-stored private keys (AC-6)
2. **bcrypt cost factor 12** as password hashing baseline (AC-2)
3. **Refresh token rotation** with SHA-256 hash persistence and replay detection (FR-AUTH.3a-d)
4. **Stateless access tokens** (15min TTL) with stateful refresh tracking (7d TTL)
5. **Feature flag gated rollout** via `AUTH_SERVICE_ENABLED` (AC-8, AC-10)
6. **Dependency injection** for all core components (AC-5)
7. **Same 6 API endpoints**: register, login, refresh, profile, reset-request, reset-confirm
8. **Same 5 external dependencies**: jsonwebtoken, bcrypt, email service, relational DB, secrets manager
9. **Same 3 risks prioritized**: key compromise (RISK-1), replay attack (RISK-2), bcrypt obsolescence (RISK-3)
10. **Same 3 gaps identified**: progressive lockout (GAP-1), audit logging (GAP-2), deletion revocation (GAP-3)
11. **Same 7 open questions** (OQ-1 through OQ-7) with similar blocking analysis
12. **Down-migration support** as a hard requirement (AC-9)
13. **OAuth/OIDC/MFA/RBAC** deferred to v2.0; GAP-2/GAP-3 deferred to v1.1
14. **Same NFR targets**: p95 < 200ms (NFR-AUTH.1), 99.9% uptime (NFR-AUTH.2), bcrypt benchmark (NFR-AUTH.3)
15. **Same component decomposition** for core services: PasswordHasher, JwtService, TokenManager, AuthService, AuthMiddleware, AuthRoutes, AuthMigration
16. **Same team skill requirements**: backend TS, security, database, QA, DevOps

---

## 2. Divergence Points

### D-1: Phase Count and Granularity

| Aspect | Opus | Haiku |
|--------|------|-------|
| Total phases | 7 | 5 |
| Total task rows | 94 | ~100 (20 per phase) |

- **Opus** separates infrastructure, crypto/repos, token management, auth service, middleware/routes, security hardening, and validation into distinct phases.
- **Haiku** consolidates into broader phases: foundations+crypto+repos (Phase 1), token+auth orchestration (Phase 2), request-path integration (Phase 3), validation (Phase 4), operationalization (Phase 5).
- **Impact**: Opus offers finer-grained phase gates and clearer dependency isolation. Haiku reduces coordination overhead and milestone ceremonies but risks less precise progress tracking.

---

### D-2: Integration Point Placement

| Aspect | Opus | Haiku |
|--------|------|-------|
| Placement | Dedicated Section 2, upfront before phases | Embedded at the end of each phase |

- **Opus** enumerates all 5 integration artifacts (DI container, route registry, middleware chain, feature flag gate, migration registry) in a single pre-plan section with cross-phase references.
- **Haiku** documents 3-4 integration artifacts per phase with explicit "Owning Phase" and "Cross-Reference" annotations.
- **Impact**: Opus gives a global wiring overview useful for architects reviewing the full plan. Haiku localizes integration context closer to where it's actionable, reducing the need to cross-reference sections.

---

### D-3: Test Placement Strategy

| Aspect | Opus | Haiku |
|--------|------|-------|
| Approach | Tests co-located with implementation phases | Tests concentrated in Phase 4 |

- **Opus** places TEST tasks alongside their feature phases (e.g., TEST-001 through TEST-004 in Phase 2 with crypto components, TEST-005-006 in Phase 3 with token management).
- **Haiku** defers all TEST tasks to Phase 4 "Validation and hardening."
- **Impact**: Opus encourages TDD or at least concurrent test authoring, catching defects earlier. Haiku risks a late-phase testing bottleneck where defects discovered in Phase 4 require changes across Phases 1-3. However, Haiku's approach simplifies parallel developer assignment per phase.

---

### D-4: Component Inventory Breadth

| Aspect | Opus | Haiku |
|--------|------|-------|
| Core components | COMP-001 through COMP-011 (11 total) | COMP-001 through COMP-017 (17 total) |

- **Haiku** introduces 6 additional explicit components:
  - `COMP-010` PasswordResetRepository (separate abstraction)
  - `COMP-013` Auth context attachment model
  - `COMP-014` Route-handler adapter layer
  - `COMP-015` Error mapping strategy
  - `COMP-016` Cookie/header transport handling
  - `COMP-017` Auth module ownership map
- **Opus** folds reset token persistence into existing repository patterns and treats context propagation, error mapping, and transport as implementation details of existing components.
- **Impact**: Haiku produces more testable, named artifacts for cross-cutting concerns. Opus keeps the component count manageable but may leave error mapping and transport handling underspecified.

---

### D-5: Migration Structure

| Aspect | Opus | Haiku |
|--------|------|-------|
| Migration files | 3 separate migrations (MIG-001, MIG-002, MIG-003) | 2 migrations (MIG-001 up, MIG-002 down) bundling all tables |

- **Opus** creates one migration per table (users, refresh_tokens, password_reset_tokens), executed in sequence by COMP-007.
- **Haiku** creates a single up migration for all auth tables and a single down migration, treating the auth schema as an atomic unit.
- **Impact**: Opus allows partial rollback at table granularity. Haiku treats auth as all-or-nothing, which is simpler to reason about but inflexible if only one table needs modification.

---

### D-6: Refresh Token Schema Design

| Aspect | Opus | Haiku |
|--------|------|-------|
| DM-002 fields | Standard: id, user_id, token_hash, expires_at, revoked, created_at | Extended: adds replaced_by_token_id, created_ip, user_agent, revoked_at (nullable timestamptz) |

- **Haiku** adds `replaced_by_token_id` (self-referencing UUID) for rotation chain lineage tracking, plus client metadata fields (`created_ip`, `user_agent`).
- **Opus** uses a simpler boolean `revoked` flag without lineage tracking.
- **Impact**: Haiku's schema enables forensic analysis of replay attack chains and per-device session visibility. Opus's schema is leaner but requires scanning by user_id to detect replay patterns rather than walking a token chain.

---

### D-7: API Contract Definition Timing

| Aspect | Opus | Haiku |
|--------|------|-------|
| When contracts are defined | Phase 5 (alongside route implementation) | Phase 2 (before route implementation) |

- **Haiku** defines API-001 through API-006 as contract definition tasks in Phase 2, separate from route implementation in Phase 3.
- **Opus** merges contract definition with endpoint implementation in Phase 5.
- **Impact**: Haiku enables contract-first development and parallel frontend/backend work. Opus couples contracts to implementation, which is pragmatic for a single team but delays frontend integration planning.

---

### D-8: Success Criteria Validation Strategy

| Aspect | Opus | Haiku |
|--------|------|-------|
| Approach | Single TEST-017 validates all 22 SC criteria in Phase 7 | Distributes critical SC checks across Phases 4-5 (SC-1, SC-2, SC-4, SC-5, SC-9, SC-11, SC-12, SC-16, SC-19, SC-20, SC-21, SC-22) |

- **Opus** treats SC validation as a single comprehensive gate before release.
- **Haiku** selectively validates critical SCs as individual tasks with explicit evidence linkage.
- **Impact**: Opus's monolithic validation task is clean but opaque — it's hard to tell which SC failed. Haiku's distributed approach provides traceable evidence per criterion but adds task overhead.

---

### D-9: Rollback Rehearsal Explicitness

| Aspect | Opus | Haiku |
|--------|------|-------|
| Rollback testing | Implicit in Phase 7 regression (TEST-018) | Explicit MIG-003 task in Phase 4 with staging rehearsal criteria |

- **Haiku** creates a dedicated `MIG-003: Execute rollback rehearsal` task requiring staging environment proof.
- **Opus** subsumes rollback verification into the broader TEST-018 regression suite.
- **Impact**: Haiku makes rollback readiness a first-class gate that's independently trackable. Opus risks rollback verification being deprioritized within a large regression task.

---

### D-10: Email Dispatcher Definition Timing

| Aspect | Opus | Haiku |
|--------|------|-------|
| When defined | Phase 4 (COMP-010, DEP-3) | Phase 1 (DEP-3 interface), Phase 2 (FR-AUTH.5 integration) |

- **Haiku** defines the email service integration contract in Phase 1 as an interface, allowing other teams to begin provider selection early.
- **Opus** defers both the integration and the adapter to Phase 4.
- **Impact**: Haiku's early interface definition reduces integration risk if the email provider requires procurement or configuration lead time.

---

### D-11: PasswordResetRepository as Separate Abstraction

| Aspect | Opus | Haiku |
|--------|------|-------|
| Reset token persistence | Handled by AuthService and inline logic | Dedicated COMP-010 PasswordResetRepository with full contract |

- **Haiku** gives password reset token persistence its own repository abstraction with explicit methods (createResetToken, findValidResetToken, consumeResetToken, invalidateUserResetTokens).
- **Opus** manages reset tokens through the AuthService and migration layer without a named repository component.
- **Impact**: Haiku's approach is more testable and follows the same pattern used for UserRepository and RefreshTokenRepository. Opus's approach is less consistent but avoids a thin wrapper.

---

### D-12: Request Validation Layer

| Aspect | Opus | Haiku |
|--------|------|-------|
| Approach | Inline within endpoint handlers | Dedicated COMP-011 request validation component |

- **Haiku** creates an explicit validation layer component that enforces email format, password policy, required fields, and schema consistency before service execution.
- **Opus** handles input validation within individual FR-AUTH tasks (e.g., FR-AUTH.2c for password policy, FR-AUTH.2d for email format).
- **Impact**: Haiku centralizes validation logic for reuse and consistency. Opus distributes it across feature tasks, which may lead to inconsistent validation patterns across endpoints.

---

### D-13: Error Mapping Strategy

| Aspect | Opus | Haiku |
|--------|------|-------|
| Approach | Implicit in endpoint implementation | Explicit COMP-015 component |

- **Haiku** creates a named error mapping strategy component that translates domain errors to HTTP status codes (400/401/403/409/429) while preventing credential leakage.
- **Opus** handles error responses within individual API tasks and AuthService methods.
- **Impact**: Haiku makes error response consistency a testable, owned artifact. Opus risks inconsistent error formatting across endpoints.

---

### D-14: Operational Artifacts

| Aspect | Opus | Haiku |
|--------|------|-------|
| Runbooks | Single OPS-005 in Phase 7 | OPS-003 (deployment), OPS-004 (key rotation), OPS-005 (alerting), OPS-006 (staged rollout) in Phase 5 |
| Ownership | Not addressed | Explicit COMP-017 ownership map |

- **Haiku** breaks operational readiness into 4 distinct tasks with a dedicated ownership map.
- **Opus** consolidates into a single comprehensive runbook task.
- **Impact**: Haiku's granularity makes operations handoff more actionable and assignable. Opus's single task may produce a better-integrated document but is harder to parallelize.

---

### D-15: Timeline Estimation Approach

| Aspect | Opus | Haiku |
|--------|------|-------|
| Total estimate | 4-5 weeks (1 dev), 2.5-3.5 weeks (2 devs) | 5.0-7.5 engineering weeks |
| Critical path | ASCII diagram with explicit node chain | Textual per-phase description |

- **Opus** provides both single-developer and parallel-developer estimates with a visual critical path.
- **Haiku** provides a wider range without multi-developer optimization analysis.
- **Impact**: Opus's timeline is more actionable for sprint planning. Haiku's wider range is more conservative and perhaps more honest about uncertainty.

---

### D-16: Health Check Implementation

| Aspect | Opus | Haiku |
|--------|------|-------|
| Approach | Concrete OPS-001 endpoint in Phase 1 with spec (GET /health, <50ms) | Strategy-level OPS-002 in Phase 3, OPS-001 as feature flag semantics in Phase 1 |

- **Opus** implements a working health check endpoint early with specific performance criteria.
- **Haiku** defers the health check to a "strategy definition" task without concrete implementation details.
- **Impact**: Opus delivers observable infrastructure earlier. Haiku delays observability, which could slow debugging during Phases 2-3 development.

---

### D-17: Security Hardening Placement

| Aspect | Opus | Haiku |
|--------|------|-------|
| Security tasks | Concentrated Phase 6 with dedicated RISK validation tasks | Distributed across Phases 1 (AC-6), 3 (RISK-1, AC-7), 4 (TEST-008, TEST-011) |

- **Opus** groups all security validation into a dedicated Phase 6 with penetration testing references.
- **Haiku** distributes security controls across phases, validating them closer to their implementation.
- **Impact**: Opus risks discovering security issues late in a dedicated phase. Haiku validates security properties incrementally but lacks a cohesive security review milestone.

---

### D-18: Open Question Resolution Tracking

| Aspect | Opus | Haiku |
|--------|------|-------|
| Approach | Prose in risk section; "resolve before Phase N" directives | Explicit OQ tasks in phase tables (OQ-3, OQ-7 in Phase 1; OQ-1, OQ-2 in Phase 2; OQ-4 in Phase 3) plus resolution tracking tasks (OQ-1A, OQ-2A in Phase 5) |

- **Haiku** creates trackable task rows for each open question resolution AND follow-up "record final decision" tasks.
- **Opus** mentions OQ resolution requirements in phase preambles but doesn't create discrete tasks.
- **Impact**: Haiku makes decision debt visible in task tracking. Opus's approach is lighter but OQ resolution could fall through the cracks.

---

## 3. Areas Where One Variant Is Clearly Stronger

### Opus is stronger in:

| Area | Why |
|------|-----|
| **Test co-location** | Tests alongside implementation catches defects earlier and enforces TDD discipline |
| **Critical path visualization** | ASCII dependency diagram makes scheduling concrete and reviewable |
| **Multi-developer timeline** | Explicit parallel-developer estimate enables practical sprint planning |
| **Health check early delivery** | Working observability in Phase 1 aids all subsequent development |
| **Task ID traceability** | 94 tasks with consistent ID scheme (FR-AUTH.Xx, SC-N) map cleanly to extraction IDs |
| **Concise phase structure** | 7 narrow phases with clear single-purpose objectives |

### Haiku is stronger in:

| Area | Why |
|------|-----|
| **Component decomposition** | 17 named components vs 11 — error mapping, validation, transport, and context are first-class testable artifacts |
| **API contract-first** | Defining contracts in Phase 2 enables parallel frontend work and earlier integration testing |
| **Schema richness** | `replaced_by_token_id` and client metadata fields enable forensic replay chain analysis |
| **Open question tracking** | OQ tasks + resolution recording tasks prevent decision debt from being invisible |
| **Rollback rehearsal** | Explicit staging rehearsal task with concrete criteria vs buried in regression suite |
| **Per-phase integration docs** | Localized integration artifacts are more actionable than a global upfront section |
| **Operational granularity** | 4 distinct ops tasks + ownership map vs 1 monolithic runbook |
| **PasswordResetRepository** | Consistent repository pattern for all 3 entity types improves testability |

---

## 4. Areas Requiring Debate to Resolve

### Debate 1: Test Timing — Co-located vs Concentrated

- **Opus position**: Write tests in the same phase as implementation (TDD-adjacent).
- **Haiku position**: Concentrate tests in a validation phase after implementation stabilizes.
- **Key question**: Does the team practice TDD? If yes, Opus's approach is natural. If not, Haiku's approach avoids test churn during active design iteration. A hybrid (unit tests co-located, integration tests concentrated) may be optimal.

### Debate 2: Migration Granularity — Per-Table vs Atomic

- **Opus position**: 3 separate migrations for independent table lifecycle.
- **Haiku position**: 1 atomic up + 1 atomic down treating auth schema as a unit.
- **Key question**: Will auth tables ever need independent schema evolution? If yes, Opus's granularity pays off. If auth is always deployed atomically, Haiku's simplicity is preferable.

### Debate 3: Component Count — Lean vs Explicit

- **Opus position**: 11 components; cross-cutting concerns handled inline.
- **Haiku position**: 17 components; every concern gets a named, testable artifact.
- **Key question**: Is the team large enough to benefit from fine-grained ownership? Small teams may find 17 components over-engineered. Larger teams benefit from clear boundaries and independent testability.

### Debate 4: Security Validation — Concentrated Phase vs Distributed

- **Opus position**: Dedicated security hardening phase (Phase 6) with penetration testing.
- **Haiku position**: Security controls validated alongside implementation.
- **Key question**: Is there a security engineer who reviews at a specific milestone, or does the team self-validate continuously? If the former, Opus's concentrated phase provides a clean review point. If the latter, Haiku's distribution avoids late-stage security rework.

### Debate 5: Timeline Realism

- **Opus position**: 4-5 weeks (1 dev), with explicit parallelism for 2-dev acceleration.
- **Haiku position**: 5.0-7.5 engineering weeks, wider range.
- **Key question**: Haiku's conservative estimate may reflect realistic overhead (OQ resolution, procurement, integration debugging). Opus's optimistic estimate assumes OQ decisions are made promptly. The truth likely depends on organizational decision-making speed.

### Debate 6: Refresh Token Schema Richness

- **Opus position**: Minimal schema with boolean `revoked` flag.
- **Haiku position**: Rich schema with `replaced_by_token_id` lineage and client metadata.
- **Key question**: Is forensic replay chain analysis a v1.0 requirement or a nice-to-have? The additional schema complexity has a maintenance cost. If security incident investigation is important, Haiku's richer schema is worth it. If not, Opus's lean schema reduces migration complexity.
