---
total_diff_points: 14
shared_assumptions_count: 18
---

## Shared Assumptions

1. **Facade pattern**: Both use `AuthService` as single orchestration facade over `TokenManager`, `PasswordHasher`, `UserRepo`
2. **Stateless JWT + RS256 2048-bit** signing with server-managed refresh tokens in Redis
3. **bcrypt cost 12** as password hashing baseline
4. **PostgreSQL 15+ / Redis 7+** as persistence layer
5. **SendGrid** for password reset emails
6. **Business case**: ~$2.4M personalization revenue unlock, SOC2 Q3 2026 readiness
7. **Complexity**: MEDIUM (0.65) -- both agree on classification and drivers
8. **Three-phase rollout**: alpha -> 10% beta -> GA with feature flags `AUTH_NEW_LOGIN` and `AUTH_TOKEN_REFRESH`
9. **PRD gap fills**: Both identify and include logout (API-007) and admin log access (API-008) missing from TDD
10. **GDPR consent** required at registration with no design in TDD
11. **Audit log retention**: Both resolve TDD/PRD conflict toward 12-month retention
12. **Rate limiting**: 10 req/min/IP login, 5 req/min/IP register, 30 req/min/user refresh, 60 req/min/user profile
13. **Account lockout**: 5 failures in 15 minutes -> 423 response
14. **Same 10 success criteria** with identical targets (p95<200ms, 99.9% uptime, >60% conversion, etc.)
15. **Same 6 risks** with substantially identical mitigations
16. **Rollback chain**: disable flag -> verify legacy -> root cause -> data restore -> notify -> postmortem
17. **Token TTLs**: 15-minute access, 7-day refresh
18. **Node.js 20 LTS** runtime

## Divergence Points

### 1. Phase Structure: 7 Phases vs 5 Phases
- **Opus**: 7 phases -- separates infrastructure (P1), data/security (P2), backend (P3), frontend (P4), testing (P5), migration (P6), operations (P7)
- **Haiku**: 5 phases -- merges infrastructure+data+security into P1, merges backend+unit/integration tests into P2, frontend+E2E into P3, operations+compliance into P4, rollout+success metrics into P5
- **Impact**: Opus offers finer-grained exit gates and clearer handoff boundaries. Haiku reduces coordination overhead but creates larger, harder-to-fail-fast phases.

### 2. Timeline: 9 Weeks vs 13 Weeks
- **Opus**: 9 weeks with aggressive phase overlap (P4 overlaps P3; P7 overlaps P6)
- **Haiku**: 13 weeks fully sequential, no overlap
- **Impact**: Opus is 44% faster but assumes parallel frontend/backend teams and concurrent ops work during rollout. Haiku is more conservative and realistic for a single team. The 4-week difference is significant for the Q2/Q3 SOC2 deadline.

### 3. Infrastructure as Separate Phase vs Embedded
- **Opus**: Dedicates Phase 1 (1 week) purely to provisioning PostgreSQL, Redis, TLS, CORS, project scaffold, Docker Compose
- **Haiku**: Folds infrastructure provisioning into Phase 1 alongside schema definitions, security modules, and component builds (2 weeks)
- **Impact**: Opus's isolation ensures infra is validated before any code depends on it. Haiku's bundling risks blocked developers if provisioning slips but reduces phase transition overhead.

### 4. Additional Schemas: ConsentRecord, PasswordResetToken, AuthSecurityState
- **Opus**: Defines 3 schemas (UserProfile, AuthToken, AuditLog) -- consent, reset tokens, and lockout state are implicit in component implementations
- **Haiku**: Defines 6 explicit schemas (DM-001 through DM-006) including `ConsentRecord`, `PasswordResetToken`, and `AuthSecurityState` as first-class data models
- **Impact**: Haiku's explicit schemas force early design decisions on consent storage, reset token lifecycle, and lockout state -- reducing ambiguity in Phase 2/3 implementations. Opus leaves these as implementation details, risking inconsistent designs across components.

### 5. Test Placement: Dedicated Phase vs Inline
- **Opus**: Concentrates all testing in Phase 5 (1.5 weeks) -- unit, integration, E2E, load, security, compliance
- **Haiku**: Distributes tests across Phases 2 (unit+integration), 3 (E2E), and 4 (compliance+load+resilience)
- **Impact**: Haiku's approach catches failures closer to implementation and avoids a late-stage testing bottleneck. Opus's batched testing is more efficient to schedule but risks discovering integration issues 3-4 weeks after the code was written.

### 6. Frontend Admin Page
- **Opus**: Includes API-008 (admin log query endpoint) but no frontend admin page component
- **Haiku**: Includes both API-008 and `COMP-015 AdminAuthEventsPage` with filters, plus `FR-AUTH-007` for the admin log viewing journey and `TEST-012` for E2E validation
- **Impact**: Haiku fully closes the Jordan persona gap from the PRD. Opus leaves the admin experience as API-only, requiring separate frontend work.

### 7. Logout Journey Completeness
- **Opus**: API-007 endpoint + COMP-017 LogoutButton (simple click->clear->redirect)
- **Haiku**: API-007 + COMP-014 LogoutControl + FR-AUTH-006 (full journey spec) + TEST-011 (E2E verification) + explicit shared-device security consideration
- **Impact**: Haiku treats logout as a first-class user journey with E2E coverage. Opus treats it as a UI widget with less verification rigor.

### 8. Success Metrics as Explicit Tasks
- **Opus**: Success criteria defined in a summary table; validation happens implicitly during testing/rollout phases
- **Haiku**: Each success criterion (SC-001 through SC-010) is an explicit task row in Phase 5 with defined source, phase, and gate behavior
- **Impact**: Haiku makes metric validation a blocking gate in the rollout -- metrics must pass before GA proceeds. Opus relies on team discipline to check the summary table.

### 9. Phase 1 Duration and Security Foundation Depth
- **Opus**: 1 week for infrastructure only; security modules (PasswordHasher, JwtService) in Phase 2
- **Haiku**: 2 weeks covering infrastructure + schemas + security modules + consent/audit/lockout/reset stores + rate limiter + health endpoint
- **Impact**: Haiku front-loads all security-critical components before any API work begins, ensuring the security foundation is complete and tested. Opus spreads security work across P1-P2, which is faster but means APIs in P3 may begin before all security modules are validated.

### 10. Health Endpoint Scope
- **Opus**: NFR-REL-001 checks PostgreSQL + Redis connectivity only
- **Haiku**: COMP-016 checks PostgreSQL + Redis + RSA keys + SendGrid, with SLI definitions for uptime and dependency health
- **Impact**: Haiku's broader health check catches more failure modes (key rotation issues, email delivery degradation) before they impact users.

### 11. Total Task Rows: 88 vs 93
- **Opus**: 88 rows with no inline tests before Phase 5
- **Haiku**: 93 rows with tests distributed across phases and explicit success metric validation tasks
- **Impact**: Haiku's 5 additional rows come from explicit schema definitions (DM-004/5/6), admin frontend (COMP-015), and success metric gates (SC-001-010). These add traceability but increase tracking overhead.

### 12. Open Questions: 12 vs 10
- **Opus**: 12 open questions, including 2 explicit PRD gap annotations (OQ-011, OQ-012) as separate items
- **Haiku**: 10 open questions, folding PRD gaps into a closing note rather than numbered OQs
- **Impact**: Opus's explicit PRD gap OQs create clearer tracking and assignment. Haiku's closing note is informational but less actionable.

### 13. Docker Compose / Dev Environment
- **Opus**: Explicit INFRA-009 task for Docker Compose dev environment with testcontainers compatibility
- **Haiku**: No explicit dev environment setup task; testcontainers mentioned only in infrastructure requirements prose
- **Impact**: Opus ensures developer onboarding and local testing are first-class concerns. Haiku assumes this will happen organically.

### 14. OpenTelemetry Tracing Placement
- **Opus**: OPS-012 in Phase 7 (operations), after GA rollout begins
- **Haiku**: Wired into Phase 4 integration points alongside Prometheus metrics, before rollout
- **Impact**: Haiku ensures distributed tracing is available during alpha/beta for debugging rollout issues. Opus may lack tracing during the most critical rollout phases.

## Areas Where Each Variant Is Clearly Stronger

### Opus Strengths
- **Faster timeline** (9 vs 13 weeks) with explicit phase overlap planning
- **Integration point tables per phase** are more detailed with explicit wiring phases and consumer lists
- **Docker Compose dev environment** as explicit task
- **Executive summary** includes quantified critical path and architectural decision rationale
- **Resource requirements** section is more detailed (specific team responsibilities per phase)

### Haiku Strengths
- **Explicit data models** for consent, reset tokens, and security state -- forces early schema design
- **Tests distributed inline** with implementation -- catches issues sooner
- **Success metrics as gated tasks** -- enforceable rather than advisory
- **Admin frontend** fully specified (COMP-015, FR-AUTH-007, TEST-012)
- **Logout as complete journey** with E2E coverage and shared-device security
- **Health endpoint** checks all four dependencies, not just two
- **OpenTelemetry before rollout** -- available when most needed
- **Front-loaded security foundation** -- all security modules validated before API work begins

## Areas Requiring Debate

1. **9 weeks vs 13 weeks**: Is parallel execution realistic given team size? The SOC2 Q3 deadline may force Opus's timeline, but Haiku's is safer for a single team.
2. **Test batching vs inline**: Opus's dedicated testing phase is more schedulable; Haiku's inline approach catches bugs earlier. Team testing maturity should decide.
3. **Schema explicitness**: Should `ConsentRecord`, `PasswordResetToken`, and `AuthSecurityState` be first-class schemas (Haiku) or implementation details (Opus)? Compliance reviewers likely prefer Haiku's approach.
4. **Admin frontend in v1 scope**: Opus defers it; Haiku includes it. Product/compliance must decide if Jordan persona is v1 or v1.1.
5. **Phase granularity**: 7 smaller phases (Opus) vs 5 larger phases (Haiku). More phases = more exit gates but more coordination cost. Team size and cadence should determine this.
