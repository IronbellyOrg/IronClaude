---
spec_source: "test-tdd-user-auth.compressed.md"
complexity_score: 0.65
complexity_class: MEDIUM
primary_persona: architect
base_variant: "none"
variant_scores: "none"
convergence_score: 1.0
debate_rounds: 0
generated: "2026-04-17"
generator: "single"
total_milestones: 4
total_task_rows: 82
risk_count: 7
open_questions: 9
domain_distribution:
  frontend: 22
  backend: 34
  security: 24
  performance: 12
  documentation: 8
consulting_personas: [architect, backend, security, frontend, qa, devops]
milestone_count: 4
milestone_index:
  - id: M1
    title: "Identity Data and Compliance Foundations"
    type: SECURITY
    priority: P0
    dependencies: []
    deliverable_count: 20
    risk_level: High
  - id: M2
    title: "Authentication and Session Core"
    type: SECURITY
    priority: P0
    dependencies: [M1]
    deliverable_count: 18
    risk_level: High
  - id: M3
    title: "User Journeys and Admin Surfaces"
    type: FEATURE
    priority: P0
    dependencies: [M1, M2]
    deliverable_count: 21
    risk_level: High
  - id: M4
    title: "Operational Hardening and Rollout"
    type: MIGRATION
    priority: P0
    dependencies: [M1, M2, M3]
    deliverable_count: 23
    risk_level: High
total_deliverables: 82
total_risks: 7
estimated_milestones: 4
validation_score: 0.96
validation_status: PASS
---

# User Authentication Service — Project Roadmap

## Executive Summary

This roadmap delivers a self-hosted email/password authentication platform that unblocks the Q2-Q3 personalization roadmap, satisfies Q3 SOC2 audit prerequisites, and closes the current gap in self-service account access. The architecture sequences work by technical layer rather than feature bundle: persistent identity and compliance data first, authentication and token security second, user/admin interaction surfaces third, and operational hardening plus phased rollout last.

The plan preserves every extracted requirement and entity as its own deliverable row, then fills PRD-driven gaps the TDD does not yet cover: logout, audit-log queryability for Jordan, compromised-account lock controls, password-reset UI surfaces, public/protected route wiring, health checks, reset-token persistence, consent recording, and audit-event storage.

**Business Impact:** Enables the identity foundation required for personalization revenue, reduces support burden via self-service recovery, and establishes the audit trail required for SOC2 enterprise readiness.

**Complexity:** MEDIUM (0.65) — breadth spans frontend, backend, security, compliance, rollout, and operational guardrails, but the scope remains bounded to email/password auth without OAuth, MFA, or RBAC.

**Critical path:** M1 persistent data/compliance contracts -> M2 secure auth/token core -> M3 user/admin flows and route wiring -> M4 observability, staged migration, rollback readiness, and GA validation.

**Key architectural decisions:**

- Use stateless JWT access tokens with hashed refresh-token records in Redis rather than server-side sessions.
- Treat audit logging, consent capture, and data minimization as foundation-layer deliverables instead of post-launch hardening.
- Keep admin visibility and account-lock actions internal-only in v1.0 to satisfy Jordan’s JTBD without expanding into full RBAC.

**Open risks requiring resolution before M1:**

- OQ-002 leaves the `roles` array bound undefined, which affects the `UserProfile` schema, JWT claim sizing, and profile response contract.
- OQ-PRD-005/OQ-PRD-006 leave internal admin audit/lock surface scope and authorization unresolved, which affects compliance completeness and operational workflow design.

## MLS Summary

|ID|Title|Type|Priority|Effort|Dependencies|Deliverables|Risk|
|---|---|---|---|---|---|---|---|
|M1|Identity Data and Compliance Foundations|SECURITY|P0|4 weeks|—|20|High|
|M2|Authentication and Session Core|SECURITY|P0|4 weeks|M1|18|High|
|M3|User Journeys and Admin Surfaces|FEATURE|P0|4 weeks|M1, M2|21|High|
|M4|Operational Hardening and Rollout|MIGRATION|P0|4 weeks|M1, M2, M3|23|High|

## Dependency Graph

PostgreSQL + Redis + RSA key material -> UserRepo/ConsentStore/AuditLogStore/ResetTokenStore -> PasswordHasher + JwtService -> TokenManager + LockoutPolicy -> AuthService -> `/v1/auth/*` APIs -> AuthProvider + route guards + Login/Register/Profile/Reset/Logout pages -> Admin audit/lock surfaces -> tests + metrics + alerts + runbooks -> feature-flagged alpha -> 10% beta -> GA.

## M1: Identity Data and Compliance Foundations

**M1: Identity Data and Compliance Foundations** | Weeks 1-4 | exit criteria: schemas, cryptographic primitives, compliance storage, foundational APIs, and contract tests are implementation-ready

**Objective:** Establish persistent schemas, security primitives, compliance records, and baseline contracts that all authentication flows depend on. | **Duration:** Weeks 1-4 | **Entry:** Product scope fixed to email/password v1.0; PostgreSQL 15+, Redis 7+, Node.js 20 LTS, and security policy inputs available. | **Exit:** Core data models, persistence adapters, cryptographic primitives, compliance storage, foundational APIs, and baseline contract tests are defined and implementation-ready.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|DM-001|UserProfile schema|Define the canonical PostgreSQL user profile schema used by auth, profile, audit, and token claims.|UserRepo|OQ-002|id:UUIDv4-PK-NN; email:string-UNIQUE-NN-indexed-lowercase-normalized; displayName:string-NN-2..100; createdAt:ISO8601-NN-default-now(); updatedAt:ISO8601-NN-auto-updated; lastLoginAt:ISO8601-nullable; roles:string[]-NN-default-[user]|M|P0|
|2|DM-002|AuthToken envelope|Define the token response envelope and Redis refresh record contract for login and refresh flows.|TokenManager|COMP-006, COMP-007|accessToken:string-JWT-RS256-NN-payload{userId,roles}; refreshToken:string-opaque-UNIQUE-NN-Redis-7d-TTL; expiresIn:number-NN-900; tokenType:string-NN-Bearer|S|P0|
|3|COMP-009|User repository adapter|Implement the PostgreSQL-backed data access layer for user creation, lookup, uniqueness checks, and profile reads.|UserRepo|DM-001|PostgreSQL15+-backed; pg-pool-used; create/find/update supported; email-normalization-applied; uniqueness-enforced; query-latency-observable|M|P0|
|4|COMP-008|Password hashing service|Implement the hashing abstraction with bcrypt cost 12 and no raw-password persistence or logging.|PasswordHasher|NFR-SEC-001, NFR-COMP-003|bcrypt-cost-12; hash+verify-APIs; raw-password-never-persisted; raw-password-never-logged; migration-abstraction-preserved|M|P0|
|5|COMP-007|JWT signing service|Implement RS256 token signing and verification with 2048-bit RSA keys and skew tolerance.|JwtService|NFR-SEC-002|RS256-sign+verify; 2048-bit-RSA-keys; 5s-clock-skew-tolerance; sign/verify-target-<5ms; quarterly-rotation-hook-supported|M|P0|
|6|COMP-010|Consent repository|Add persistent GDPR consent recording so registration stores consent state and timestamp.|ConsentStore|DM-001, NFR-COMP-001|userId-reference; consentGiven:boolean; consentRecordedAt:timestamptz; registration-write-path; queryable-for-audit|S|P0|
|7|COMP-011|Audit event store|Add persistent SOC2 audit event storage for authentication events and retention enforcement.|AuditLogStore|DM-001, NFR-COMP-002|eventId; userId-nullable; eventType; timestamp; ipAddress; outcome; retention>=12-months; queryable-by-user+date|M|P0|
|8|COMP-012|Reset token store|Add password-reset token persistence with one-hour TTL, one-time-use semantics, and session-invalidation linkage.|ResetTokenStore|DM-001|tokenHash; userId; createdAt; expiresAt-1h; usedAt-nullable; one-time-use-enforced; invalidates-sessions-on-confirm|M|P0|
|9|COMP-013|Account lockout policy module|Define reusable failed-attempt tracking and 5-in-15-minute account lockout evaluation logic.|LockoutPolicy|OQ-PRD-003|5-failed-attempts/15-min-window; locked-state-output; reset-on-success; brute-force-counter-source-defined|S|P0|
|10|COMP-014|Error envelope contract|Define the shared error envelope and auth error-code taxonomy used by all v1 endpoints.|APIErrorContract|API-001, API-002, API-003, API-004, API-005, API-006|error.code; error.message; error.status; consistent-401/400/409/423/429-mapping; version-safe-additive-contract|S|P1|
|11|API-002|Registration API contract|Define the versioned registration endpoint contract including request, response, and validation failures.|Auth API|DM-001, COMP-014|path:/v1/auth/register; auth:none; rate-limit:5/min/IP; request:{email,password,displayName}; response:201-UserProfile; errors:400,409|S|P0|
|12|API-005|Reset request API contract|Define the password reset request endpoint with enumeration-safe response semantics.|Auth API|COMP-012, COMP-014|path:/v1/auth/reset-request; auth:none; request:{email}; response:200-generic-confirmation; sends-reset-token; prevents-enumeration|S|P1|
|13|COMP-015|Health check endpoint|Add a health/readiness contract needed for uptime monitoring and rollout gates.|Platform health|COMP-005, COMP-009|service-health-endpoint; PostgreSQL-readiness; Redis-readiness; kube-probe-compatible; uptime-monitorable|S|P1|
|14|FR-AUTH-002|Registration requirement orchestration|Translate registration requirements into a complete backend orchestration contract before endpoint implementation.|AuthService|DM-001, COMP-008, COMP-010, API-002|201-with-UserProfile; duplicate-email-409; weak-password<8/no-uppercase/no-number-400; bcrypt-cost-12; creates-profile-and-consent|M|P0|
|15|NFR-SEC-001|Password hash compliance|Verify and enforce bcrypt cost 12 across all password-hashing call sites and tests.|PasswordHasher|COMP-008|bcrypt-cost-factor-12-enforced; unit-test-asserts-parameter; no-lower-cost-paths|S|P0|
|16|NFR-SEC-002|Token signing compliance|Verify and enforce RS256 with 2048-bit RSA keys for all JWT operations.|JwtService|COMP-007|RS256-only; 2048-bit-key-validation; config-test-present; unsupported-algorithms-rejected|S|P0|
|17|NFR-COMP-001|Registration consent capture|Ensure every registration records explicit GDPR consent and its timestamp before account activation.|ConsentStore|COMP-010, FR-AUTH-002|consent-required-at-registration; timestamp-recorded; persisted-with-user-link; auditable|S|P0|
|18|NFR-COMP-002|Audit logging foundation|Ensure all auth-domain events have a storage contract for user, timestamp, IP, and outcome with retention.|AuditLogStore|COMP-011|userId; timestamp; ipAddress; outcome; eventType; 12-month-retention-minimum; queryable-storage|M|P0|
|19|NFR-COMP-003|Password secrecy guarantee|Ensure passwords never appear in persistence, logs, traces, or error envelopes.|PasswordHasher|COMP-008, COMP-011, COMP-014|raw-password-never-persisted; raw-password-never-logged; raw-password-never-traced; errors-redacted|S|P0|
|20|NFR-COMP-004|Data minimization guardrail|Restrict collected PII to email, hashed password, and display name across storage and API contracts.|UserRepo|DM-001, API-002|no-extra-PII-fields; email+passwordHash+displayName-only; profile-contract-aligned; audit-excludes-extra-PII|S|P0|

### Integration Points — M1

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|UserRepo -> PostgreSQL 15|data access|Schema migrations, pooled queries, uniqueness indexes|M1|AuthService, Profile API, admin audit queries|
|PasswordHasher -> bcryptjs|library adapter|Hash/verify abstraction with cost enforcement|M1|AuthService, reset confirm flow, unit tests|
|JwtService -> RSA key material|crypto service|RS256 sign/verify and rotation hooks|M1|TokenManager, API auth middleware|
|TokenManager -> Redis 7|token persistence|Hashed refresh-token records and revocation store|M1|Login, refresh, logout, reset confirm|
|ConsentStore -> registration flow|compliance persistence|Consent write on account creation|M1|Register API, audit/compliance reviews|
|AuditLogStore -> auth event stream|audit persistence|Structured event write and query contract|M1|Security review, admin audit surface, alerts|
|ResetTokenStore -> SendGrid workflow|email/reset persistence|Token issue, expiry, and one-time-use validation|M1|Reset request API, reset confirm API, reset UI|
|Health endpoint -> Kubernetes probes|platform wiring|Liveness/readiness route published|M1|Uptime monitoring, rollout gates|

### Milestone Dependencies — M1

- Requires PostgreSQL 15+, Redis 7+, Node.js 20 LTS, bcryptjs, jsonwebtoken, SendGrid provisioning, API Gateway policy support, and security policy SEC-POLICY-001.
- Unlocks M2 implementation of TokenManager/AuthService flows and M3 user/admin surfaces by freezing schema and compliance contracts early.

### Open Questions — M1

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-002|Maximum allowed `UserProfile` roles array length?|Affects schema sizing, JWT payload size, and profile contract finalization.|auth-team|2026-04-01|
|2|OQ-PRD-003|Should the 5-attempt/15-minute account lockout policy be confirmed or adjusted before implementation?|Affects lockout semantics, API error behavior, and security acceptance criteria.|Security|2026-04-22|
