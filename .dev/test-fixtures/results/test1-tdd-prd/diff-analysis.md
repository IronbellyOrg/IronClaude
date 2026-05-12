---
total_diff_points: 14
shared_assumptions_count: 18
---

# Roadmap Comparative Diff Analysis

## 1. Shared Assumptions & Agreements

Both variants agree on the following 18 points:

1. **Complexity rating:** MEDIUM (0.55) — security-critical but architecturally well-understood
2. **Business driver:** $2.4M projected revenue from personalization; SOC2 Type II audit in Q3 2026
3. **Facade pattern:** `AuthService` orchestrating `PasswordHasher`, `TokenManager`, `JwtService`, `UserRepo`
4. **Five functional requirements:** FR-AUTH-001 through FR-AUTH-005
5. **Token design:** 15-minute JWT accessToken (RS256, 2048-bit RSA) + 7-day Redis-backed refreshToken
6. **Password hashing:** bcrypt cost factor 12 with `PasswordHasher` abstraction for future argon2id migration
7. **Infrastructure stack:** PostgreSQL 15+, Redis 7+, SendGrid
8. **Rate limiting values:** 10/min login, 5/min register per IP; 60/min profile, 30/min refresh per user
9. **Account lockout:** 5 failed attempts within 15 minutes
10. **Audit log retention:** 12 months (PRD overrides TDD's 90-day)
11. **XSS mitigation:** accessToken in memory only (not localStorage); HttpOnly cookie for refreshToken
12. **Feature flags:** `AUTH_NEW_LOGIN` and `AUTH_TOKEN_REFRESH` with progressive rollout
13. **Rollout strategy:** Alpha (internal) → Beta (10%) → GA (100%)
14. **No user enumeration:** Identical responses for invalid/nonexistent accounts across all endpoints
15. **GDPR consent:** Captured at registration with timestamp
16. **Data minimization:** Only email, hashed password, displayName collected
17. **Team shape:** 2 backend, 1 frontend, 1 QA, 0.5–1 security, 0.5–1 DevOps
18. **Success criteria:** Same 10 metrics with identical targets

---

## 2. Divergence Points

### D-01: Phase Count & Structure
- **Opus:** 6 phases — Foundation, Token Lifecycle, Password Reset, Frontend, Observability/Hardening, Phased Rollout
- **Haiku:** 4 phases (0–3) — Design & Foundation, Core Auth & Registration, Profile/Reset/Audit, Production GA & Stabilization
- **Impact:** Opus's finer granularity provides clearer milestone boundaries but creates more handoff points. Haiku's consolidation reduces ceremony but packs more work per phase, risking milestone ambiguity.

### D-02: Dedicated Design Phase (Phase 0)
- **Opus:** Jumps directly into infrastructure provisioning in Phase 1; no explicit design/planning phase
- **Haiku:** Dedicates Weeks 1–2 to architecture review, threat modeling, OQ resolution, team training, and IaC provisioning
- **Impact:** Haiku's Phase 0 front-loads ambiguity resolution and team alignment. Opus assumes design happens implicitly alongside Phase 1 work, which could surface surprises mid-implementation.

### D-03: Open Question Resolution Strategy
- **Opus:** Lists OQs as blocking specific phases with recommended resolution dates; leaves decisions to stakeholders
- **Haiku:** Resolves all 8 OQs decisively in Phase 0 with specific architectural decisions (e.g., OQ-003: async via background queue; OQ-008: logout endpoint required)
- **Impact:** Haiku's approach eliminates blocking ambiguity before development starts. Opus's deferred approach is more stakeholder-friendly but risks Phase 2–4 delays if decisions slip.

### D-04: Frontend/Backend Parallelization
- **Opus:** Frontend is a distinct Phase 4 (Weeks 7–9) that begins after token lifecycle and password reset are complete
- **Haiku:** Frontend development runs in parallel with backend throughout Phase 1 (Weeks 3–7), with dedicated weekly breakdowns for both tracks
- **Impact:** Haiku's parallel approach is ~2 weeks faster on critical path. Opus's sequential approach is safer (frontend builds on stable APIs) but extends the timeline.

### D-05: Total Duration
- **Opus:** ~15 weeks (13 weeks development + overlap, rollout through Week 15)
- **Haiku:** 12 weeks total (including Phase 0 design)
- **Impact:** 3-week difference. Haiku is more aggressive, leveraging parallel frontend/backend tracks and consolidated phases. Opus has more buffer but risks feature flag fatigue in the extended rollout.

### D-06: Token Lifecycle Phasing
- **Opus:** Dedicates a full phase (Phase 2, Weeks 4–5) to token lifecycle and session management
- **Haiku:** Embeds token lifecycle into Phase 1 alongside login/registration (Week 6 of Phase 1)
- **Impact:** Opus's isolation allows deeper focus on token edge cases. Haiku's integration is more efficient but may compress testing time for a security-critical component.

### D-07: Logout Endpoint Decision
- **Opus:** Lists OQ-008 (logout endpoint) as unresolved; suggests deciding before Phase 4
- **Haiku:** Decides definitively: `POST /auth/logout` required for Alex persona; revokes refreshToken in Redis
- **Impact:** Haiku provides a complete API surface from the start. Opus leaves a gap that could affect frontend `AuthProvider` design if the decision comes late.

### D-08: Observability Timing
- **Opus:** Dedicated Phase 5 (Weeks 9–11) for observability, Prometheus metrics, OpenTelemetry tracing, and alerting
- **Haiku:** Sets up APM instrumentation in Phase 0; metrics defined in operational readiness section; no dedicated observability phase
- **Impact:** Opus's approach gives observability deep attention but delays it until near-rollout. Haiku's early instrumentation means performance baselines are available throughout development, enabling earlier detection of regressions.

### D-09: Audit Logging Placement
- **Opus:** Audit log table created in Phase 1 (schema); hardened and validated in Phase 5
- **Haiku:** Full `AuditLogger` service implementation in Phase 2 (Weeks 8–10), integrated into all AuthService methods
- **Impact:** Similar end result, but Opus splits the concern across two phases (schema early, implementation late), while Haiku consolidates. Haiku's approach means audit logging is validated during beta, which is better for SOC2 readiness.

### D-10: Password Reset Token Storage
- **Opus:** Stores reset tokens implicitly (storage mechanism not specified beyond "1-hour TTL")
- **Haiku:** Explicitly stores reset tokens in PostgreSQL `password_reset_tokens` table with `used` flag for single-use enforcement
- **Impact:** Haiku's specificity provides clearer implementation guidance and prevents the ambiguity of whether reset tokens go to Redis or PostgreSQL.

### D-11: Admin Endpoint for Jordan Persona
- **Opus:** Lists admin API (OQ-007) as potentially Phase 5 or post-v1.0
- **Haiku:** Includes account unlock endpoint (`POST /admin/users/:id/unlock`) in scope; provides interim log query via direct DB access
- **Impact:** Haiku addresses the Jordan admin persona more concretely. Opus risks leaving admin workflows unaddressed at GA.

### D-12: Integration Point Documentation
- **Opus:** Dedicated Section 3 with 5 named integration points (AuthService facade, TokenManager→JwtService, AuthProvider→API, Feature Flags, Rate Limiting) with cross-phase references
- **Haiku:** Uses inline tables per phase showing component wiring
- **Impact:** Opus's centralized integration map is superior for cross-team communication and architectural review. Haiku's inline approach is easier to follow phase-by-phase but harder to trace cross-cutting concerns.

### D-13: Rollback Criteria Specificity
- **Opus:** Explicit rollback triggers: p95 > 1000ms for 5 min, error rate > 5% for 2 min, Redis failures > 10/min, any data loss
- **Haiku:** Rollback criteria mentioned but less precisely defined; references "rollback criteria not triggered" without listing thresholds in one place
- **Impact:** Opus's explicit thresholds are operationally superior — on-call engineers need unambiguous triggers.

### D-14: Risk Table Detail
- **Opus:** 7 risks with severity, phase addressed, mitigation strategy
- **Haiku:** 7 risks with severity, probability, impact, mitigation, contingency, owner, and monitoring columns
- **Impact:** Haiku's risk table is significantly more actionable with ownership, monitoring methods, and contingency plans. Opus's is adequate but lacks operational depth.

---

## 3. Areas Where One Variant Is Clearly Stronger

### Opus Strengths
- **Integration point documentation** (D-12): Centralized dispatch table with cross-phase references is architecturally superior for a team coordination artifact
- **Rollback criteria** (D-13): Explicit, measurable thresholds ready for runbook inclusion
- **Phase granularity** (D-01): Clearer milestone boundaries make progress tracking and gate decisions simpler
- **Compliance gate per phase**: Phase 1 includes an explicit compliance checkpoint before proceeding

### Haiku Strengths
- **Phase 0 design phase** (D-02): Front-loading ambiguity resolution is a best practice that Opus omits entirely
- **OQ resolution** (D-03): Decisive answers to all 8 open questions prevent downstream blocking
- **Parallel development** (D-04): Frontend/backend concurrency saves ~2–3 weeks on critical path
- **Risk table depth** (D-14): Owner, monitoring, contingency columns make risks operationally actionable
- **Implementation detail** (D-10, D-11): More specific on storage mechanisms, admin endpoints, and weekly task breakdowns
- **Observability timing** (D-08): Early APM instrumentation enables data-driven decisions throughout development
- **Weekly cadence** section: Provides concrete ceremony schedule (Mon/Wed/Fri activities) absent from Opus

---

## 4. Areas Requiring Debate to Resolve

1. **Sequential vs. parallel frontend development (D-04):** Opus's sequential approach guarantees stable APIs before frontend builds on them; Haiku's parallel approach is faster but requires API contract discipline (OpenAPI spec finalized in Phase 0). **Debate question:** Is the team mature enough for contract-first parallel development?

2. **Dedicated observability phase vs. early instrumentation (D-08):** Opus's Phase 5 gives observability focused attention; Haiku's Phase 0 setup gives earlier data. **Debate question:** Is it better to instrument early and iterate, or dedicate a hardening phase? (Likely answer: instrument early, validate in a gate.)

3. **Phase 0 design phase necessity (D-02):** Haiku spends 2 weeks on design before coding. Opus starts building in Week 1. **Debate question:** Does this team/org need an explicit design phase, or can architecture be validated in parallel with Phase 1 infrastructure work?

4. **12 weeks vs. 15 weeks (D-05):** Haiku's 12-week timeline is aggressive but achievable with parallel tracks. Opus's 15 weeks includes more buffer. **Debate question:** What is the external deadline? If SOC2 audit is Q3 2026, 15 weeks (ending ~July) may be fine; if personalization features need auth by June, 12 weeks is necessary.

5. **OQ resolution authority (D-03):** Haiku resolves all OQs with architect authority. Opus defers to stakeholders. **Debate question:** Does the architect have mandate to make these decisions, or do OQ-005 ("remember me") and OQ-008 (logout) require product sign-off?

6. **Rollout duration (D-01):** Opus allocates 4 weeks for rollout (Weeks 11–15); Haiku allocates 2 weeks (Weeks 11–12). **Debate question:** For a security-critical auth migration, is 2 weeks of production validation sufficient, or does the 4-week graduated rollout provide necessary safety?
