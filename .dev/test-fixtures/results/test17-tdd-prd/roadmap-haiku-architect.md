---
spec_source: "test-tdd-user-auth.compressed.md"
complexity_score: 0.65
complexity_class: MEDIUM
primary_persona: architect
generated: "2026-04-18"
generator: "single"
total_milestones: 5
total_task_rows: 95
risk_count: 7
open_questions: 8
domain_distribution:
  frontend: 18
  backend: 36
  security: 20
  performance: 10
  documentation: 16
consulting_personas: [architect, backend, security, frontend, qa, devops]
milestone_count: 5
milestone_index:
  - id: M1
    title: "Core Security and Data Foundations"
    type: SECURITY
    priority: P0
    dependencies: []
    deliverable_count: 24
    risk_level: High
  - id: M2
    title: "Registration and Login Experience"
    type: FEATURE
    priority: P0
    dependencies: [M1]
    deliverable_count: 15
    risk_level: High
  - id: M3
    title: "Session Lifecycle and Protected Access"
    type: FEATURE
    priority: P0
    dependencies: [M1, M2]
    deliverable_count: 20
    risk_level: High
  - id: M4
    title: "Password Reset, Audit, and Admin Visibility"
    type: FEATURE
    priority: P0
    dependencies: [M1, M3]
    deliverable_count: 19
    risk_level: High
  - id: M5
    title: "Rollout, Reliability, and GA Operations"
    type: MIGRATION
    priority: P1
    dependencies: [M2, M3, M4]
    deliverable_count: 17
    risk_level: Medium
total_deliverables: 95
total_risks: 7
estimated_milestones: 5
validation_score: 0.94
validation_status: PASS_WITH_WARNINGS
---

# User Authentication Service — Project Roadmap

## Executive Summary

This roadmap sequences the authentication program as a technical-layer rollout: establish cryptographic and data foundations first, ship registration/login next to unlock business value early, then harden session management, password recovery, auditability, and staged production rollout. The plan preserves every extracted requirement and entity as an explicit deliverable while adding PRD-driven gap fills for logout and admin audit-log investigation so v1.0 satisfies both user and compliance outcomes.

**Business Impact:** Unlocks the Q2 2026 personalization roadmap, protects the projected $2.4M annual revenue tied to authenticated experiences, and closes the largest SOC2 audit blocker before Q3 2026.

**Complexity:** MEDIUM (0.65) — moderate functional surface, but elevated by RS256 key management, Redis-backed refresh-token revocation, staged rollout, GDPR/SOC2 obligations, and anti-abuse controls.

**Critical path:** M1 crypto/data/runtime baseline → M2 registration/login → M3 token refresh/profile/logout → M4 password reset/audit/admin visibility → M5 staged rollout and SLO validation.

**Key architectural decisions:**

- Use RS256 access tokens with opaque Redis-backed refresh tokens so revocation, rotation, and Sam’s programmatic refresh use case can coexist.
- Keep access tokens in memory and refresh handling non-script-readable for browser flows while preserving clear refresh contracts for API consumers.
- Add an explicit admin audit-log query surface and UI because Jordan’s JTBD and SOC2 evidence requirements are not fully covered by the extracted FR set alone.

**Open risks requiring resolution before M1:**

- Lock in RSA key provisioning and quarterly rotation ownership before implementation begins.
- Confirm whether API-key authentication stays out of v1.0 so the auth boundary does not widen mid-foundation.

## MLS Summary

|ID|Title|Type|Priority|Effort|Dependencies|Deliverables|Risk|
|---|---|---|---|---|---|---|---|
|M1|Core Security and Data Foundations|SECURITY|P0|XL|—|24|High|
|M2|Registration and Login Experience|FEATURE|P0|L|M1|15|High|
|M3|Session Lifecycle and Protected Access|FEATURE|P0|XL|M1,M2|20|High|
|M4|Password Reset, Audit, and Admin Visibility|FEATURE|P0|XL|M1,M3|19|High|
|M5|Rollout, Reliability, and GA Operations|MIGRATION|P1|L|M2,M3,M4|17|Medium|

## Dependency Graph

M1(core schemas, crypto, controllers, health) -> M2(registration, login, consent)
M1(core schemas, crypto, controllers, health) -> M3(refresh, profile, logout, protected access)
M1(core schemas, crypto, controllers, health) -> M4(reset, audit, admin visibility)
M2(registration, login, consent) -> M3(refresh, profile, logout, protected access)
M3(refresh, profile, logout, protected access) -> M4(reset, audit, admin visibility)
M2,M3,M4 -> M5(alpha, beta, GA, rollback, reliability)

## M1: Core Security and Data Foundations

**Objective:** Establish the runtime, schema, cryptographic, API-shell, and policy baseline that every auth flow depends on. | **Duration:** 3 weeks | **Entry:** PRD scope fixed to email/password v1.0; PostgreSQL, Redis, and Node.js 20 environments available. | **Exit:** Core data contracts, token/signing services, audit schema, controller skeletons, and observability baseline are deployable in staging with policy conformance verified.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|DM-001|UserProfile schema|Define PostgreSQL schema and TypeScript contract for the canonical user record used by registration, login, and profile retrieval.|AuthService,PostgreSQL|INFRA-DB-001|id:uuid-pk-notnull; email:unique-indexed-lowercase-notnull; displayName:2-100-notnull; createdAt:iso8601-default-now-notnull; updatedAt:iso8601-auto-updated-notnull; lastLoginAt:iso8601-nullable; roles:string[]-default-user-notnull|M|P0|
|2|DM-002|AuthToken contract|Define token response contract returned by login and refresh and align it with frontend and API consumers.|TokenManager,JwtService|NFR-SEC-002|accessToken:jwt-rs256-notnull; refreshToken:opaque-unique-notnull; expiresIn:number-900-notnull; tokenType:Bearer-notnull|S|P0|
|3|COMP-007|AuthService core module|Create the orchestration service that owns registration, login, profile, and reset use cases and delegates hashing, tokening, and persistence.|AuthService|DM-001,DM-002|service boundaries documented; methods for register/login/me/reset flows defined; persistence/token/hash dependencies injected; no caller bypasses service boundary|M|P0|
|4|COMP-008|PasswordHasher module|Implement dedicated password hashing and verification component using bcrypt cost 12 and no raw-password persistence.|PasswordHasher|NFR-SEC-001,SEC-POLICY-001|hash uses bcrypt-cost12; verify compares bcrypt hashes; raw passwords never persisted; raw passwords never logged|S|P0|
|5|COMP-009|JwtService module|Implement RS256 signing and verification component with 2048-bit RSA keys, 15-minute access-token TTL, and ±5-second clock skew tolerance.|JwtService|NFR-SEC-002,SEC-POLICY-001|signs-rs256; rsa-keysize-2048; access-ttl-900s; verify honors-5s-skew; key identifiers supported for rotation|M|P0|
|6|COMP-010|TokenManager module|Implement refresh-token issuance, hashing, storage, revocation, and rotation orchestration against Redis 7+.|TokenManager,Redis|DM-002,COMP-009|issues access+refresh pair; stores hashed refresh token in redis; ttl-7d; supports revoke+rotate; lookup by user/session metadata|M|P0|
|7|COMP-011|AuditLog repository|Create audit-log persistence component for compliance evidence and incident investigation support.|AuditLog,PostgreSQL|NFR-COMPLIANCE-002,INFRA-DB-001|stores userId; eventType; timestamp; ipAddress; outcome; retention-configurable-to-12m; query paths support date+user filters|M|P0|
|8|COMP-012|ResetToken store|Create reset-token persistence and validation component with one-hour TTL and single-use semantics.|ResetTokenStore,PostgreSQL|FR-AUTH-005|token persisted hashed; ttl-1h; used flag enforced; lookup invalid after consume; user linkage preserved|M|P0|
|9|COMP-013|Consent recorder|Create registration-consent component to capture GDPR consent state and timestamp at account creation.|ConsentRecorder,PostgreSQL|NFR-COMPLIANCE-001,DM-001|consent-required-at-registration; consentTimestamp-recorded; linked-to-userId; no extra-PII captured|S|P0|
|10|COMP-014|AuthController shell|Create REST controller shell for `/v1/auth/*` endpoints with unified error envelope and versioned routing.|AuthController|COMP-007|routes mounted under-v1-auth; errors use error.code+message+status; JSON-only responses; additive-field policy documented|M|P0|
|11|API-001|Login endpoint contract|Define and scaffold POST `/auth/login` request, response, and error semantics before business logic wiring.|AuthController|COMP-014,DM-002|method POST; path /v1/auth/login; auth none; request email+password; 200 returns AuthToken; 401 generic-invalid; 423 locked; 429 rate-limited|S|P0|
|12|API-002|Register endpoint contract|Define and scaffold POST `/auth/register` contract for validated account creation.|AuthController|COMP-014,DM-001|method POST; path /v1/auth/register; auth none; request email+password+displayName; 201 returns UserProfile; 400 validation; 409 duplicate|S|P0|
|13|API-003|Profile endpoint contract|Define and scaffold GET `/auth/me` contract for authenticated profile retrieval.|AuthController|COMP-014,DM-001|method GET; path /v1/auth/me; auth bearer-accessToken; header Authorization:Bearer<JWT>; 200 returns id+email+displayName+createdAt+updatedAt+lastLoginAt+roles; 401 invalid-expired-missing|S|P0|
|14|API-004|Refresh endpoint contract|Define and scaffold POST `/auth/refresh` contract for silent and programmatic refresh.|AuthController|COMP-014,DM-002|method POST; path /v1/auth/refresh; auth refreshToken-in-body; request refreshToken; 200 returns new AuthToken pair; old refresh revoked; 401 expired-or-revoked|S|P0|
|15|API-005|Reset-request endpoint contract|Define and scaffold POST `/auth/reset-request` anti-enumeration contract.|AuthController|COMP-014|method POST; path /v1/auth/reset-request; auth none; request email; 200 regardless-of-registration; side-effect reset email token with-1h-ttl|S|P0|
|16|API-006|Reset-confirm endpoint contract|Define and scaffold POST `/auth/reset-confirm` contract with session invalidation behavior.|AuthController|COMP-014,COMP-012|method POST; path /v1/auth/reset-confirm; auth none; request token+newPassword; updates password hash; invalidates all sessions; 400 expired-used-token; 400 weak-password|S|P0|
|17|API-007|Logout endpoint gap fill|Add explicit logout endpoint required by the PRD user story so shared-device session termination is first-class.|AuthController,TokenManager|COMP-014,OQ-PRD-002|method POST; path /v1/auth/logout; auth bearer-or-refresh context; revokes current session immediately; returns clear success code; redirects supported by frontend flow|S|P0|
|18|API-008|Admin audit query endpoint gap fill|Add admin audit-log query API to satisfy Jordan’s PRD JTBD and SOC2 investigation workflow.|AuditController,AuditLog|COMP-011|method GET; path /v1/auth/audit-events; auth admin-only; filters userId+dateRange+outcome; paginated JSON; auditable access to audit logs|M|P1|
|19|NFR-SEC-001|Password hashing policy enforcement|Validate bcrypt cost-factor and hashing policy as a release-blocking platform capability.|PasswordHasher|COMP-008|bcrypt cost factor 12 enforced; unit assertion covers configured cost; no plain-text persistence; no plain-text logging|S|P0|
|20|NFR-SEC-002|Token signing policy enforcement|Validate JWT signing configuration meets RS256 and RSA key-size requirements with rotation support.|JwtService|COMP-009|rs256-only; rsa2048-minimum; config validation test exists; quarterly rotation path defined; invalid config fails fast|S|P0|
|21|NFR-COMPLIANCE-002|Audit logging foundation|Define compliant audit-event schema, retention policy, and event taxonomy before feature flows emit logs.|AuditLog|COMP-011|captures userId+timestamp+ipAddress+outcome; auth event taxonomy defined; retention configurable to-12-months; SOC2 evidence queries supported|M|P0|
|22|NFR-COMPLIANCE-003|Password-storage compliance|Map NIST SP 800-63B storage requirements directly into implementation and validation controls.|PasswordHasher|NFR-SEC-001|adaptive one-way hashing only; raw passwords never persisted; raw passwords never logged; compliance mapping documented in tests|S|P0|
|23|NFR-COMPLIANCE-004|Data-minimization boundary|Enforce collection boundary so auth data stores only email, hashed password, and display name collected. No additional PII.|AuthService,PostgreSQL|DM-001,NFR-COMPLIANCE-001|collects email+hashedPassword+displayName only; no additional PII fields added; audit data separate from profile; schema review completed|S|P0|
|24|OPS-010|Tracing baseline|Establish OpenTelemetry trace propagation across auth components before business flows are load-tested.|AuthService,PasswordHasher,TokenManager,JwtService|COMP-007,COMP-008,COMP-009,COMP-010|traces span AuthService->PasswordHasher->TokenManager->JwtService; correlation ids propagate; staging export works; missing sampling policy flagged|M|P1|

### Integration Points — M1

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|AuthService -> PasswordHasher|dependency injection|Constructor injection with verify/hash interface|M1|FR-AUTH-001,FR-AUTH-002,FR-AUTH-005|
|AuthService -> TokenManager|dependency injection|Constructor injection with issue/refresh/revoke interface|M1|FR-AUTH-001,FR-AUTH-003,API-007|
|TokenManager -> JwtService|service call|issueTokens/refreshTokens invoke sign+verify|M1|API-001,API-004|
|AuthController route registry|dispatch table|`/v1/auth/*` mapped to handlers in versioned router|M1|API-001,API-002,API-003,API-004,API-005,API-006,API-007|
|Audit event emitter -> AuditLog repository|event binding|auth events emit structured records to repository|M1|NFR-COMPLIANCE-002,API-008|
|Auth middleware -> trace context|middleware chain|request context injects trace/span ids before handler execution|M1|NFR-PERF-001,OPS-010|

### Risk Assessment and Mitigation — M1

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-001 Token theft via XSS|High|Medium|Session compromise and unauthorized access|Keep access tokens in memory, use non-script-readable refresh handling, limit access TTL to 15 minutes, and support fast revocation.|security|
|2|R-002 Brute-force on login|High|Medium|Credential stuffing, account lockouts, and operational noise|Define gateway rate limits, enforce lockout state, and validate bcrypt cost and anti-enumeration behavior in M1.|security|
|3|R-PRD-003 Compliance failure from incomplete audit logging|High|Medium|SOC2 evidence gap and release delay|Lock schema, required fields, and retention direction in M1 before downstream feature work proceeds.|compliance|

### Milestone Dependencies — M1

- PostgreSQL 15+, Redis 7+, Node.js 20 LTS, SEC-POLICY-001, and SendGrid integration design must be available before exiting M1.
- API-key authentication is explicitly deferred unless OQ-001 is reopened and approved for v1.0.

### Open Questions — M1

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-001|Should `AuthService` support API key authentication for service-to-service calls?|Changes the auth boundary, route contracts, and token model; defer keeps v1.0 scope stable.|test-lead|2026-04-15|
|2|OQ-002|Maximum allowed `UserProfile` roles array length?|Affects DM-001 validation, storage sizing, and admin-query assumptions.|auth-team|2026-04-01|
|3|OQ-PRD-003|Should the 5-failures-in-15-min lockout policy remain fixed or be adjusted?|Changing threshold affects brute-force mitigation, UX, and alert tuning.|Security|2026-04-22|
|4|OQ-RET-001|Who owns the audit retention decision between 90 days and 12 months?|Blocks final schema/index sizing and compliance evidence design; PRD intent currently wins.|Compliance + Engineering|2026-04-22|
