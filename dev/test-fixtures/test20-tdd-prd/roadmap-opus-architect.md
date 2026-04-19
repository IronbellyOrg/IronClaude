---
spec_source: "test-tdd-user-auth.compressed.md"
complexity_score: 0.72
complexity_class: HIGH
primary_persona: architect
---

# User Authentication Service — Project Roadmap

## Executive Summary

Deliver a production-grade identity layer (registration, login, logout, JWT-based session persistence, profile retrieval, and self-service password reset) that unblocks the Q2-Q3 2026 personalization roadmap and closes the SOC2 Type II audit gap. The system is implemented as a Node.js 20 LTS service fronted by an API Gateway, backed by PostgreSQL 15 for `UserProfile` persistence and Redis 7 for opaque refresh-token storage with TTL-based revocation, with a React `AuthProvider` context driving frontend integration.

**Business Impact:** Authentication unblocks ~$2.4M in projected annual revenue from personalization-dependent features, closes the Q3 2026 SOC2 audit blocker, and reduces access-issue support ticket volume (up 30% QoQ) via self-service password reset. Target KPIs: registration conversion >60%, login p95 <200ms, session duration >30min, failed-login rate <5%.

**Complexity:** HIGH (0.72) — driven by multi-component orchestration (AuthService + TokenManager + JwtService + PasswordHasher), dual-store persistence (PostgreSQL + Redis), security-critical token lifecycle (RS256 JWT + opaque refresh + revocation), and cross-cutting regulatory compliance (SOC2, GDPR, NIST SP 800-63B).

**Critical path:** DM-001 (UserProfile schema) → COMP-008 (PasswordHasher) → COMP-005 (AuthService) → API-001/API-002 → COMP-007 (JwtService) → COMP-006 (TokenManager) → API-003/API-004 → FR-AUTH-005 (Password reset) → COMP-004 (AuthProvider) → MIG-001/002/003 (phased rollout). Any delay to DM-001, COMP-008, or COMP-007 blocks every downstream deliverable.

**Key architectural decisions:**

- **Stateless JWT access + opaque Redis-backed refresh**: accessToken is RS256-signed (2048-bit RSA, quarterly rotation) and kept in memory only; refreshToken is opaque, hashed at rest in Redis with 7-day TTL — chosen over symmetric HS256 and localStorage-persisted tokens to mitigate R-001 (XSS token theft) at the cost of a Redis dependency.
- **bcrypt cost factor 12 behind a `PasswordHasher` abstraction**: NIST SP 800-63B-compliant adaptive hashing with a pluggable interface to enable algorithm migration (e.g., to argon2) without schema changes; cost 12 chosen to meet <500ms hash-time budget while resisting brute-force.
- **Feature-flag-gated phased rollout (10% → 100%)**: `AUTH_NEW_LOGIN` + `AUTH_TOKEN_REFRESH` flags enable parallel-run with legacy auth, bounded blast radius, and fast rollback — chosen over big-bang cutover to mitigate R-003 (migration data loss).

**Open risks requiring resolution before M1:**

- **PRD/TDD audit-log retention conflict** — PRD NFR-COMPLIANCE-001 requires 12-month SOC2 retention; TDD §7.2 specifies 90-day retention. Must be resolved with compliance before DM-001 schema is finalized.
- **Account lockout notification mechanism** — OQ-PRD-003: PRD requires admin notification after 5 failed attempts; TDD has no notification channel. Blocks FR-AUTH-001 AC #4.
- **Logout endpoint ownership** — PRD user story requires `POST /auth/logout`; TDD API surface omits it. Must be scoped into M2 before TokenManager revocation contract is frozen.

## Milestone Summary

|ID|Title|Type|Priority|Effort|Dependencies|Deliverables|Risk|
|---|---|---|---|---|---|---|---|
|M1|Core AuthService & Registration|Foundation|P0|L (2 weeks)|None|24|High|
|M2|Token Management & Session|Foundation|P0|L (2 weeks)|M1|22|High|
|M3|Password Reset & Audit Logging|Feature|P0|M (2 weeks)|M2|18|Medium|
|M4|Frontend Integration|Feature|P0|M (2 weeks)|M2|14|Medium|
|M5|Phased Rollout & GA|Release|P0|M (2 weeks)|M3, M4|16|High|

## Dependency Graph

```
M1 (Core AuthService)
 ├─ DM-001 UserProfile ──┬─► COMP-005 AuthService ──┬─► API-001 /login
 │                       │                          └─► API-002 /register
 ├─ COMP-008 PasswordHasher ─► (consumed by COMP-005)
 └─ NFR-SEC-001, NFR-COMPLIANCE-002/003/004

M2 (Token Management)         ◄── depends on M1
 ├─ COMP-007 JwtService ──► COMP-006 TokenManager ──┬─► API-003 /me
 ├─ DM-002 AuthToken ───────────────────────────────┴─► API-004 /refresh
 └─ API-LOGOUT (gap fill) ─► COMP-006 revocation

M3 (Reset & Audit)            ◄── depends on M2
 ├─ DM-003 AuditLog ─► API-AUDIT-READ (admin)
 ├─ API-RESET-REQUEST ─► SendGrid
 └─ API-RESET-CONFIRM ─► COMP-008 (re-hash)

M4 (Frontend)                 ◄── depends on M2
 ├─ COMP-004 AuthProvider ──┬─► COMP-001 LoginPage
 │                          ├─► COMP-002 RegisterPage
 │                          └─► COMP-003 ProfilePage
 └─ TEST-006 E2E

M5 (Rollout)                  ◄── depends on M3 + M4
 ├─ MIG-001 Alpha ─► MIG-002 Beta (10%) ─► MIG-003 GA (100%)
 └─ OPS-001..005 runbooks, capacity, observability
```

## M1: Core AuthService & Registration

**Objective:** Establish the canonical `UserProfile` schema, `PasswordHasher` abstraction, and `AuthService` orchestration layer, and ship login + registration endpoints compliant with NIST SP 800-63B password storage and GDPR data-minimization mandates. | **Duration:** 2 weeks (Weeks 1–2) | **Entry:** PostgreSQL 15 + Redis 7 provisioned; RSA keypair generated; audit-log retention decision (TDD 90d vs PRD 12m) resolved with compliance. | **Exit:** FR-AUTH-001 and FR-AUTH-002 pass all acceptance criteria in integration tests against real PostgreSQL; bcrypt cost-factor test passes; zero P0/P1 bugs; all COMPLIANCE-0xx controls implemented.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|DM-001|UserProfile data model|Define and migrate the `UserProfile` PostgreSQL table/TypeScript interface with all fields and constraints.|PostgreSQL|-|id:UUID-PK-NOT-NULL; email:string-UNIQUE-NOT-NULL-lowercase-indexed; displayName:string-NOT-NULL-2to100chars; createdAt:timestamptz-NOT-NULL-DEFAULT-now; updatedAt:timestamptz-NOT-NULL-auto-updated; lastLoginAt:timestamptz-NULLABLE; roles:text[]-NOT-NULL-DEFAULT-{user}; migration-idempotent; rollback-SQL-included|M|P0|
|2|COMP-008|PasswordHasher service|Backend service wrapping bcryptjs with cost factor 12; exposes `hash()` and `verify()`; abstracts algorithm for future migration.|Backend|-|uses-bcryptjs; cost-factor=12; hash-time<500ms; verify-returns-bool; raw-password-never-logged; interface-allows-algorithm-swap; unit-test-asserts-bcrypt-cost-parameter|S|P0|
|3|COMP-005|AuthService orchestration facade|Backend facade class receiving API Gateway requests and delegating to PasswordHasher/TokenManager/JwtService/UserRepo.|Backend|DM-001,COMP-008|dependency-injection-wired; error-envelope-{error:{code,message,status}}; structured-logging-without-sensitive-fields; OpenTelemetry-spans-emitted|M|P0|
|4|FR-AUTH-001|Login with email/password|Implement `AuthService.login()` validating credentials against bcrypt hashes via `PasswordHasher`.|Backend|COMP-005,COMP-008|200+AuthToken-on-valid; 401-on-invalid-password; 401-on-nonexistent-email-no-enumeration; 423-after-5-failed-in-15min; no-timing-side-channels|M|P0|
|5|FR-AUTH-002|User registration with validation|Implement `AuthService.register()` creating `UserProfile` with uniqueness, password-policy, and bcrypt hashing.|Backend|DM-001,COMP-005,COMP-008|201+UserProfile-on-valid; 409-on-duplicate-email; 400-on-weak-password(<8chars,no-upper,no-number); 400-on-invalid-email; bcrypt-hash-persisted-cost-12|M|P0|
|6|API-001|POST /v1/auth/login|Public endpoint validating credentials and issuing tokens; rate-limited at gateway.|API|FR-AUTH-001|request:{email,password}; response-200:{accessToken,refreshToken,expiresIn:900,tokenType:Bearer}; 401-invalid; 423-locked; 429-rate-limit; rate-limit=10req/min/IP|S|P0|
|7|API-002|POST /v1/auth/register|Public endpoint creating new user profile with validation.|API|FR-AUTH-002|request:{email,password,displayName}; response-201:UserProfile; 400-validation; 409-duplicate-email; rate-limit=5req/min/IP|S|P0|
|8|NFR-SEC-001|Password hashing policy enforcement|Verify bcrypt cost factor 12 is mandated via config and tested.|Backend|COMP-008|config-value=12; unit-test-reads-stored-hash-and-asserts-cost-parameter=12; hash-time-benchmark<500ms-documented|S|P0|
|9|NFR-COMPLIANCE-002|GDPR consent at registration|Record explicit consent with timestamp at registration; block account creation without consent.|Backend|FR-AUTH-002,DM-001|consent_accepted_at:timestamptz-column-added; 400-when-consent-missing; consent-record-immutable-post-creation; privacy-notice-link-in-response|S|P0|
|10|NFR-COMPLIANCE-003|Password storage (NIST SP 800-63B)|Verify one-way adaptive hashing; raw passwords never persisted or logged.|Backend|COMP-008|log-scanner-test-confirms-no-raw-password-in-logs; DB-scan-confirms-bcrypt-prefix($2b$); plaintext-never-leaves-AuthService-request-scope|S|P0|
|11|NFR-COMPLIANCE-004|Data minimization (GDPR)|Restrict `UserProfile` collection to email, hashed password, display name.|Backend|DM-001|DM-001-column-audit-shows-no-additional-PII; data-classification-doc-published; schema-change-requires-compliance-sign-off|S|P0|
|12|TEST-001|Unit: login with valid credentials returns AuthToken|Jest unit test on `AuthService.login()` validating positive path.|Test|FR-AUTH-001|mocks-PasswordHasher+TokenManager; asserts-AuthToken-returned; asserts-verify-called-once; asserts-issueTokens-called-once|S|P0|
|13|TEST-002|Unit: login with invalid credentials returns error|Jest unit test validating negative path; `PasswordHasher.verify()` returns false.|Test|FR-AUTH-001|mocks-PasswordHasher-returns-false; asserts-401; asserts-no-AuthToken-issued; asserts-TokenManager-not-called|S|P0|
|14|TEST-004|Integration: registration persists UserProfile to DB|Testcontainers PostgreSQL test for POST `/auth/register` end-to-end persistence.|Test|FR-AUTH-002,DM-001|testcontainers-PostgreSQL-15-started; POST-/auth/register-returns-201; DB-row-inserted-with-bcrypt-hash; email-unique-constraint-enforced|M|P0|
|15|OPS-001|Runbook: AuthService down|Production runbook for AuthService unavailability (5xx on /auth/*).|Docs|COMP-005|diagnosis-steps-enumerated; resolution-pod-restart+DB-failover; escalation=auth-team-on-call→15min→platform-team; prevention-HPA+health-checks-documented|S|P1|
|16|R-002-MIT|Account lockout after 5 failed attempts|Implement lockout counter in Redis keyed by email/IP; 15-minute window.|Backend|COMP-005,FR-AUTH-001|Redis-counter-incr-on-failed-login; TTL=15min; 423-when-count≥5; counter-reset-on-success; integration-test-5-fails-then-423|M|P0|
|17|COMP-UR-001|UserRepo PostgreSQL data access layer|Typed repository encapsulating `UserProfile` CRUD and email lookup via pg-pool.|Backend|DM-001|pg-pool-connection-pooling; parameterized-queries-no-SQL-injection; findByEmail-lowercased-lookup; upsert-idempotent; unit-tests-mock-pool|M|P0|
|18|COMP-RATE-001|Rate-limit wiring (gateway → AuthService)|Register gateway rate-limit policies for /login (10/min/IP) and /register (5/min/IP).|Infra|API-001,API-002|gateway-policy-applied; 429-returned-with-retry-after-header; k6-test-verifies-throttle; metrics-emitted|S|P0|
|19|NFR-JTBD-ALEX-001|<60s registration UX budget|Instrument registration flow to measure Alex's "create account in under 60 seconds" JTBD.|Backend|FR-AUTH-002|registration-p95-latency<60s-end-to-end-measured; funnel-metric-emitted; dashboard-panel-added|S|P1|
|20|COMP-LOG-001|Structured auth event logger (skeleton)|Logger emitting JSON events for login/register outcomes; lays groundwork for SOC2 audit (full retention in M3).|Backend|COMP-005|JSON-schema-defined:{event_type,user_id,timestamp,ip,outcome}; sensitive-fields-excluded; logger-injected-into-AuthService|S|P0|
|21|COMP-MIGRATION-M1|Database migration tooling|Select and wire migration runner (node-pg-migrate or equivalent); initial migration for DM-001.|Infra|DM-001|migration-runner-selected+documented; up/down-scripts-for-DM-001; CI-applies-migrations-before-tests; rollback-validated|S|P0|
|22|COMP-CORS-001|CORS allowlist configuration|Gateway CORS restricted to known frontend origins.|Infra|-|allowlist-config-documented; preflight-OPTIONS-returns-correct-headers; disallowed-origin-returns-403; k6-test-verifies|S|P1|
|23|COMP-TLS-001|TLS 1.3 enforcement|Enforce TLS 1.3 on all public endpoints via gateway/ingress config.|Infra|-|TLS-1.3-only-config; TLS-1.2-downgrade-rejected; cipher-suite-documented; scan-via-testssl.sh-passes|S|P0|
|24|FR-AUTH-001-AC4|Brute-force lockout AC for FR-AUTH-001|Acceptance criterion #4 of FR-AUTH-001 (locked after 5 failed attempts) validated end-to-end via integration test.|Test|R-002-MIT|integration-test-6th-attempt-returns-423; lockout-clears-after-15min; lockout-counter-per-email-not-global|S|P0|

### Integration Points — M1

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|AuthService dispatch|DI container|Registers PasswordHasher, UserRepo, logger at bootstrap|M1|API-001, API-002|
|Gateway rate-limit policy|Middleware chain|Policies attached to `/v1/auth/login`, `/v1/auth/register` at gateway config|M1|API-001, API-002|
|Structured log sink|Middleware/logger|`pino` transport registered; JSON fields per COMP-LOG-001|M1|All M1 backend components|
|DB migration runner|CI step|`npm run migrate:up` hooked into CI before test stage|M1|DM-001, COMP-UR-001|
|CORS policy|Gateway middleware|Origin allowlist injected from env config at gateway init|M1|All /v1/auth/* endpoints|
|Lockout counter|Redis key pattern|`login:fail:{email}` + TTL written by AuthService; read before verify|M1|FR-AUTH-001, R-002-MIT|

### Milestone Dependencies — M1

- **External:** PostgreSQL 15+ provisioned (INFRA-DB-001); Redis 7+ provisioned; Node.js 20 LTS runtime baseline; bcryptjs library; SEC-POLICY-001 ratified.
- **Internal:** None — M1 is the foundation milestone.
- **Decision prerequisites:** Audit-log retention conflict (PRD 12m vs TDD 90d) must be resolved BEFORE DM-001 schema is finalized (blocks any PII-retention column work).

### Open Questions — M1

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-PRD-003|Account lockout policy after N consecutive failed login attempts — TDD says 5/15min, PRD adds admin notification requirement; notification channel undefined.|FR-AUTH-001 AC #4 cannot fully ship without notification mechanism; blocks SOC2 evidence for security-event alerting.|Security + auth-team|Week 1|
|2|OQ-AUDIT-RETENTION|PRD NFR-COMPLIANCE-001 requires 12-month audit-log retention; TDD §7.2 specifies 90 days. Which governs?|Determines DM-AUDIT partitioning strategy, storage cost projection, and SOC2 evidence scope.|Compliance + product-team|Week 1|
|3|OQ-JTBD-JORDAN-LOG-API|PRD JTBD for Jordan (admin) requires queryable audit logs — no TDD FR or API defined. PRD requires; TDD should be updated.|Blocks exit criteria for SOC2 readiness; deferred admin-API scope may push to M3.|Product + auth-team|Week 2|

### Risk Assessment and Mitigation — M1

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Audit-retention decision (OQ-AUDIT-RETENTION) unresolved at schema freeze|High|Medium|Schema rework in M3; SOC2 evidence incomplete at audit|Gate DM-001 finalization on compliance sign-off; default to 12m if unresolved|compliance-lead|
|2|bcrypt cost 12 exceeds p95 latency budget under load|Medium|Low|FR-AUTH-001 fails NFR-PERF-001 (<200ms p95)|Benchmark hash-time on target hardware in week 1; if >400ms, raise HPA floor or revisit cost|auth-team|
|3|Lockout counter race conditions in Redis|Medium|Medium|Wrong users locked / real attackers not locked; FR-AUTH-001 AC #4 fails|Use atomic INCR + EXPIRE; integration test with concurrent requests|auth-team|
|4|GDPR consent record immutability not enforced|High|Low|Regulatory non-compliance; audit finding|Add DB trigger rejecting UPDATE on consent_accepted_at; test migration path|compliance-lead|

## M2: Token Management & Session

**Objective:** Implement the stateful JWT lifecycle — access-token issuance/verification via `JwtService`, opaque refresh-token storage in Redis via `TokenManager`, token refresh and revocation, profile retrieval, and the logout endpoint gap fill from the PRD. | **Duration:** 2 weeks (Weeks 3–4) | **Entry:** M1 exit criteria met; 2048-bit RSA keypair mounted in secrets volume; Redis cluster reachable from AuthService pods. | **Exit:** FR-AUTH-003 and FR-AUTH-004 pass; 500-concurrent-user k6 load test meets NFR-PERF-001/002; refresh-token revocation verified via integration test; logout endpoint shipped.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|DM-002|AuthToken data model|Define the `AuthToken` interface and Redis record schema for opaque refresh tokens.|Backend/Redis|-|accessToken:JWT-string-NOT-NULL-RS256-signed; refreshToken:string-NOT-NULL-unique-opaque-hashed-at-rest; expiresIn:number-NOT-NULL-always-900; tokenType:string-NOT-NULL-always-Bearer; Redis-key=refresh:{hash}-TTL-7d|S|P0|
|2|COMP-007|JwtService|Backend service signing/verifying JWTs with RS256, 2048-bit RSA keys, 5s clock-skew tolerance, quarterly key rotation.|Backend|-|RS256-algorithm; 2048-bit-RSA-key-loaded-from-secrets-volume; sign-emits-valid-JWT; verify-rejects-invalid-signature; 5s-clock-skew-tolerance; kid-header-for-rotation; config-validation-test-passes|M|P0|
|3|COMP-006|TokenManager|Backend service managing JWT lifecycle: issue, refresh, revoke; Redis-backed refresh store with 7-day TTL.|Backend|COMP-007,DM-002|issueTokens-returns-{access,refresh}; refresh-validates-revokes-old-issues-new; revoke-deletes-Redis-key; Redis-TTL=7d; idempotent-refresh-prevents-replay|M|P0|
|4|FR-AUTH-003|JWT token issuance and refresh|Wire TokenManager into login/refresh flows with silent-refresh contract.|Backend|COMP-006,COMP-007|login-returns-access(15m-TTL)+refresh(7d-TTL); POST-/auth/refresh-returns-new-pair; expired-refresh→401; revoked-refresh→401; old-refresh-invalidated-on-rotation|M|P0|
|5|FR-AUTH-004|User profile retrieval|Implement `AuthService.getProfile()` returning authenticated `UserProfile`.|Backend|COMP-005,COMP-006|GET-/auth/me-with-valid-access-returns-UserProfile; expired-access→401; invalid-signature→401; response-includes-id+email+displayName+createdAt+updatedAt+lastLoginAt+roles|S|P0|
|6|API-003|GET /v1/auth/me|Protected endpoint returning the authenticated `UserProfile`.|API|FR-AUTH-004|Authorization:Bearer-header-required; 200+UserProfile-on-valid; 401-on-missing/expired/invalid-token; rate-limit=60req/min/user|S|P0|
|7|API-004|POST /v1/auth/refresh|Exchange valid refresh token for new `AuthToken` pair; old refresh revoked.|API|FR-AUTH-003,COMP-006|request:{refreshToken}; 200+new-AuthToken-pair; 401-on-expired; 401-on-revoked; old-refresh-unusable-post-rotation; rate-limit=30req/min/user|S|P0|
|8|API-LOGOUT|POST /v1/auth/logout (PRD gap fill)|Endpoint revoking refreshToken in Redis and clearing HttpOnly cookie. PRD requires; TDD should be updated.|API|COMP-006|request:{refreshToken}-or-cookie; 204-on-success; 401-when-refresh-missing/invalid; Redis-key-deleted; cookie-cleared-via-Set-Cookie-Max-Age=0|S|P0|
|9|NFR-SEC-002|Token signing policy (RS256/2048-bit)|Verify JwtService signs with RS256 using 2048-bit RSA keys; configuration validation test.|Backend|COMP-007|config-asserts-algorithm=RS256; key-size-validation=2048; quarterly-rotation-runbook-documented; test-rejects-HS256-and-RS128|S|P0|
|10|NFR-PERF-001|API response time (<200ms p95)|APM-tracing validation that all /auth/* endpoints meet latency budget.|Backend|API-001,API-002,API-003,API-004|APM-histogram-shows-p95<200ms-per-endpoint; dashboard-panel-per-endpoint; alert-triggers-if-violated|M|P0|
|11|NFR-PERF-002|500 concurrent auth requests|k6 load test validating concurrent-request capacity.|Test|API-001,API-003,API-004|k6-scenario-500-VUs-sustained-5min; p95<200ms-under-load; error-rate<0.1%; CPU/mem-within-HPA-bounds|M|P0|
|12|TEST-003|Unit: token refresh with valid refresh token|Jest unit test on `TokenManager.refresh()`.|Test|COMP-006|mocks-Redis+JwtService; asserts-old-revoked; asserts-new-pair-returned; asserts-JwtService.sign-called-once|S|P0|
|13|TEST-005|Integration: expired refresh token rejected|Testcontainers Redis test for TTL-based expiration.|Test|COMP-006,DM-002|testcontainers-Redis-7; refresh-token-past-7d-returns-401; Redis-TTL-verified-via-direct-key-read|M|P0|
|14|OPS-002|Runbook: token refresh failures|Production runbook for token-refresh error spikes.|Docs|COMP-006,COMP-007|diagnosis-Redis-connectivity+secrets-mount+flag-state; resolution-scale-Redis+re-mount-secrets; escalation-path-documented; alert-wired-to-pager|S|P1|
|15|COMP-REFRESH-STORE|Redis refresh-token store abstraction|Typed repository for refresh-token hash/TTL operations; injected into TokenManager.|Backend|DM-002|store-interface-with-put/get/revoke; SHA-256-hash-before-persist; TTL-exactly-604800s; unit-tests-mock-ioredis|S|P0|
|16|COMP-JWT-ROTATION|Quarterly RSA key rotation procedure|Scripted key rotation with `kid` header; dual-validation window.|Infra|COMP-007|new-key-generation-script; JwtService-validates-current+previous-kid; rotation-runbook-documented; dry-run-in-staging|M|P1|
|17|NFR-JTBD-SAM-001|Programmatic token refresh for API consumers|Ensure API-004 contract stability for Sam (API consumer) JTBD.|API|API-004|OpenAPI-schema-published; error-envelope-stable; 401-error-code=AUTH_REFRESH_EXPIRED-or-AUTH_REFRESH_REVOKED; backwards-compat-contract-test|S|P1|
|18|COMP-TOKEN-CAP|Per-user refresh-token cap (OQ-PRD-002 resolution dependency)|Implement max-refresh-tokens-per-user limit once product decides cap.|Backend|COMP-REFRESH-STORE,OQ-PRD-002|Redis-set-key=user:refresh:{userId}; cardinality-check-before-insert; oldest-evicted-on-overflow; limit-configurable|S|P1|
|19|COMP-LAST-LOGIN|Update `UserProfile.lastLoginAt` on successful login|Backend hook updating lastLoginAt timestamp after token issuance.|Backend|FR-AUTH-001,DM-001|UPDATE-UserProfile-SET-lastLoginAt=now-WHERE-id=userId; update-async-non-blocking; failure-does-not-fail-login; integration-test-verifies-value-advances|S|P1|
|20|COMP-PWDRESET-INVALIDATE|Hook in TokenManager to invalidate all refresh tokens on password change|Prepares M3 password-reset flow; required by PRD FR-AUTH.5 AC.|Backend|COMP-006|TokenManager.revokeAllForUser(userId)-method; Redis-scan+del-for-user:refresh:{userId}-set; integration-test-verifies-post-reset-refresh-fails|S|P0|
|21|FR-AUTH-003-AC-REVOKE|AC #4: Revoked refreshToken returns 401|End-to-end integration test for manual revocation.|Test|COMP-006|test-revokes-token-then-POST-/refresh-returns-401; revoke-via-logout-path-verified|S|P0|
|22|COMP-TRACE-M2|OpenTelemetry spans across AuthService→TokenManager→JwtService|Instrument token flows with trace context propagation.|Backend|COMP-005,COMP-006,COMP-007|trace-id-in-logs; span-per-component; trace-export-to-collector-verified; dashboards-show-end-to-end-latency-breakdown|S|P1|

### Integration Points — M2

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|TokenManager dispatch|DI container|Injected into AuthService + API-004 handler at bootstrap|M2|FR-AUTH-003, API-004, API-LOGOUT|
|JWT verification middleware|Middleware chain|Express/Fastify middleware on `/v1/auth/me` and protected routes|M2|API-003, future protected APIs|
|RSA keypair mount|Secrets volume → process env|K8s Secret mounted at `/var/run/secrets/jwt-keys`; JwtService reads at init|M2|COMP-007|
|Refresh-store adapter|Strategy pattern|COMP-REFRESH-STORE registers concrete Redis impl; test suites inject memory impl|M2|COMP-006|
|Logout revocation callback|Event hook|COMP-PWDRESET-INVALIDATE registered as handler for password-change event (M3)|M2|M3 FR-AUTH-005|
|JWT kid header dispatcher|Strategy pattern|JwtService resolves current vs previous key by `kid`|M2|COMP-JWT-ROTATION|

### Milestone Dependencies — M2

- **Internal:** M1 complete (DM-001, COMP-005, COMP-008, FR-AUTH-001/002).
- **External:** Redis 7+ cluster reachable; RSA keypair provisioned by platform-team; secrets volume mount configured.
- **Decision prerequisites:** OQ-PRD-002 (per-user refresh-token cap) and OQ-PRD-004 (remember-me) should be resolved before COMP-TOKEN-CAP and refresh TTL policy are frozen; acceptable to ship M2 with unlimited tokens and revisit post-GA.

### Open Questions — M2

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-001|Should `AuthService` support API key authentication for service-to-service calls?|Informs whether COMP-007 must also validate non-JWT credentials; deferred to v1.1.|test-lead|2026-04-15|
|2|OQ-002|What is the maximum allowed `UserProfile` roles array length?|Affects DB column sizing and authorization caching; pending RBAC design review.|auth-team|2026-04-01|
|3|OQ-PRD-002|Maximum number of refresh tokens allowed per user across devices?|Blocks COMP-TOKEN-CAP implementation; if left unlimited, Redis memory growth risk.|Product|Week 3|
|4|OQ-PRD-004|Should we support "remember me" to extend session duration?|Changes refresh TTL policy and possibly introduces second refresh-token class.|Product|Week 4|
|5|OQ-LOGOUT-SCOPE|Does POST /auth/logout revoke only the current refresh token, or all sessions for the user? PRD requires; TDD should be updated.|Determines COMP-PWDRESET-INVALIDATE vs per-token revoke default behavior.|Product + auth-team|Week 3|

### Risk Assessment and Mitigation — M2

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Token theft via XSS (R-001)|High|Medium|Session hijacking; unauthorized access to user data|accessToken in memory only; HttpOnly cookie for refresh; 15m access TTL; AuthProvider clears on tab close|security-lead|
|2|Refresh-token replay via race condition|High|Medium|Old refresh reused after rotation; session-identity confusion|Atomic Lua script for validate→revoke→issue in Redis; idempotency key on refresh request|auth-team|
|3|RS256 key rotation breaks active sessions|Medium|Medium|Mass 401s during rotation; user-visible outage|Dual-validation window (current+previous kid); rotation runbook tested in staging|platform-team|
|4|NFR-PERF-001 violated under 500-concurrent load|Medium|Medium|FR-AUTH-003 exit criteria fail; GA slip|k6 load test in week 3; HPA pre-scaled; connection-pool tuning|auth-team|

## M3: Password Reset & Audit Logging

**Objective:** Ship the two-step self-service password reset (request + confirm) with SendGrid integration, fill the SOC2 audit-log gap with a queryable admin API satisfying NFR-COMPLIANCE-001 (12-month retention), and close the PRD's Jordan-admin JTBD. | **Duration:** 2 weeks (Weeks 5–6) | **Entry:** M2 exit criteria met; SendGrid account + API key provisioned; audit-log retention decision (OQ-AUDIT-RETENTION) resolved. | **Exit:** FR-AUTH-005 passes; reset-token expiry/single-use enforced; audit log meets SOC2 fields (user_id, IP, outcome, timestamp) with 12-month retention; admin audit query API operational.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-AUTH-005|Password reset flow|Two-step reset: request (sends email with token) and confirm (validates token, updates hash via PasswordHasher).|Backend|COMP-008,COMP-005,COMP-PWDRESET-INVALIDATE|POST-/reset-request-with-valid-email-sends-token; POST-/reset-confirm-with-valid-token-updates-hash; reset-token-expires-1h; used-token-cannot-be-reused; new-password-invalidates-all-sessions|M|P0|
|2|API-RESET-REQUEST|POST /v1/auth/reset-request (PRD/TDD gap)|Public endpoint accepting email and queueing reset email; same response regardless of email registration.|API|FR-AUTH-005|request:{email}; 202-Accepted-regardless-of-existence; reset-token-generated-and-stored-with-1h-TTL; SendGrid-job-enqueued; rate-limit=3req/min/IP|S|P0|
|3|API-RESET-CONFIRM|POST /v1/auth/reset-confirm (PRD/TDD gap)|Public endpoint validating reset token and updating password.|API|FR-AUTH-005|request:{token,newPassword}; 200-on-success-204-No-Content; 400-on-weak-password; 401-on-expired-or-used-token; token-marked-used-atomically; all-refresh-tokens-revoked-via-COMP-PWDRESET-INVALIDATE|S|P0|
|4|DM-RESET-TOKEN|ResetToken data model|Persisted reset-token record with expiry and single-use flag.|Backend/PostgreSQL-or-Redis|FR-AUTH-005|id:UUID-PK; user_id:FK-UserProfile; token_hash:string-SHA256-NOT-NULL-unique; expires_at:timestamptz-NOT-NULL; used_at:timestamptz-NULLABLE; created_at:timestamptz-NOT-NULL; index-on-token_hash|S|P0|
|5|COMP-EMAIL-SENDER|SendGrid email integration|Backend service wrapping SendGrid SDK; templated reset email; delivery-failure handling.|Backend|API-RESET-REQUEST|SendGrid-API-key-from-secrets; reset-email-template-rendered; delivery-status-callback-handler; failures-logged-and-metered; retry-with-exponential-backoff(max-3)|M|P0|
|6|DM-AUDIT|AuditLog data model (SOC2-compliant)|PostgreSQL audit log table with mandated SOC2 fields and 12-month retention partitioning.|PostgreSQL|OQ-AUDIT-RETENTION|id:bigint-PK; user_id:UUID-NULLABLE-FK; event_type:varchar-NOT-NULL; ip_address:inet-NOT-NULL; user_agent:text-NULLABLE; outcome:enum(success,failure)-NOT-NULL; metadata:jsonb-NULLABLE; occurred_at:timestamptz-NOT-NULL-indexed; partitioned-by-month-12-months-online|M|P0|
|7|COMP-AUDIT-WRITER|Audit-log writer service|Service consuming auth events from COMP-LOG-001 and persisting AuditLog rows.|Backend|DM-AUDIT,COMP-LOG-001|writes-on-login(success+failure)+register+refresh+revoke+reset-request+reset-confirm; async-non-blocking-via-queue; failure-degrades-to-fallback-log-file; SOC2-required-fields-always-populated|M|P0|
|8|API-AUDIT-READ|GET /v1/admin/audit (PRD/JTBD-Jordan gap fill)|Admin-only endpoint querying audit log by date range and user.|API|DM-AUDIT,COMP-AUDIT-WRITER|admin-role-required-via-RBAC-stub; query-params:userId,from,to,event_type; paginated-response; 200+rows; 403-non-admin; 400-invalid-range; PRD requires; TDD should be updated|M|P0|
|9|NFR-COMPLIANCE-001|Audit logging (SOC2 Type II)|Verify all auth events logged with required fields and 12-month retention.|Backend|DM-AUDIT,COMP-AUDIT-WRITER|fields-user_id+timestamp+ip+outcome-present-on-every-event; retention=12-months-via-monthly-partitions; older-partitions-archived-to-cold-storage; SOC2-evidence-export-script|M|P0|
|10|R-OPS-001-MIT|SendGrid delivery monitoring & alerting|Implement delivery-rate dashboards and alerts for password reset email failures.|Infra|COMP-EMAIL-SENDER|delivery-success-rate-metric; alert-if-rate<95%-over-15min; webhook-for-bounces-handled; fallback-support-channel-documented|S|P1|
|11|FR-AUTH-005-AC4|Used reset tokens cannot be reused|Atomic single-use enforcement test.|Test|FR-AUTH-005,DM-RESET-TOKEN|integration-test-uses-token-twice; second-attempt-returns-401; used_at-set-atomically-via-UPDATE-WHERE-used_at-IS-NULL|S|P0|
|12|FR-AUTH-005-AC3|Reset tokens expire after 1 hour|TTL enforcement test.|Test|FR-AUTH-005,DM-RESET-TOKEN|integration-test-with-expired-token-returns-401; expires_at-validated-server-side-not-trusted-from-client|S|P0|
|13|NFR-COMPLIANCE-001-EVIDENCE|SOC2 audit-evidence export|Script producing CSV/JSON export of audit log for auditors.|Docs|DM-AUDIT|cli-script-with-date-range-flags; output-includes-all-SOC2-fields; runbook-for-auditor-handoff; integration-test-validates-output-schema|S|P1|
|14|COMP-RESET-RATE-LIMIT|Reset-request rate-limit + email-existence-uniform-response|Prevent enumeration via rate limit and uniform 202 response.|Backend|API-RESET-REQUEST|rate-limit=3/min/IP+5/h/email; same-202-response-regardless-of-registration; timing-side-channel-test-shows-no-difference|S|P0|
|15|NFR-JTBD-JORDAN-001|Admin audit-log query JTBD coverage|End-to-end test for Jordan admin journey: investigate failed-login spike → query audit log → identify offending user.|Test|API-AUDIT-READ|test-creates-failed-logins; admin-queries-by-time-range; finds-events; verifies-IP-and-outcome-fields-present|S|P1|
|16|COMP-PWDRESET-LINK|Reset-link generation & URL signing|Generate signed magic-link URL embedded in reset email.|Backend|FR-AUTH-005,COMP-EMAIL-SENDER|URL-format=/reset?token=<opaque>; token-stored-only-as-hash-in-DB; raw-token-never-logged; URL-safe-base64-encoding|S|P0|
|17|COMP-PWDRESET-METRICS|Funnel metrics: reset-request → reset-confirm|Instrument PRD success metric "Password reset completion >80%".|Backend|API-RESET-REQUEST,API-RESET-CONFIRM|counter-auth_reset_request_total; counter-auth_reset_confirm_total; ratio-derived-metric; dashboard-panel-tracks-conversion|S|P1|
|18|R-COMP-001-MIT|SOC2 control validation in QA|QA gate verifying every SOC2-required audit field is present on every event type.|Test|NFR-COMPLIANCE-001|automated-test-asserts-fields-on-each-event-type; manual-walkthrough-with-compliance; sign-off-checkpoint-before-MIG-002|S|P0|

### Integration Points — M3

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|Reset-token store|Strategy pattern|DM-RESET-TOKEN with PostgreSQL adapter; Redis fallback considered|M3|API-RESET-REQUEST, API-RESET-CONFIRM|
|Audit-log queue|Event bus|COMP-AUDIT-WRITER subscribes to internal event bus published by COMP-LOG-001|M3|All M1/M2/M3 backend components|
|SendGrid webhook|HTTP callback|`/v1/internal/sendgrid/webhook` registered with SendGrid for delivery events|M3|R-OPS-001-MIT, COMP-EMAIL-SENDER|
|Password-change hook|Event hook|FR-AUTH-005 publishes `password.changed` event consumed by COMP-PWDRESET-INVALIDATE|M3|M2 COMP-PWDRESET-INVALIDATE|
|Admin RBAC stub|Middleware|API-AUDIT-READ wrapped in `requireRole('admin')` middleware (full RBAC out of v1 scope)|M3|API-AUDIT-READ|
|Audit partition rotator|Cron job|Monthly job creating new partition + archiving partitions >12mo|M3|DM-AUDIT, NFR-COMPLIANCE-001|

### Milestone Dependencies — M3

- **Internal:** M2 complete (COMP-PWDRESET-INVALIDATE, COMP-LOG-001).
- **External:** SendGrid account, API key, sender-domain DNS records (SPF/DKIM/DMARC) configured.
- **Decision prerequisites:** OQ-AUDIT-RETENTION (12m vs 90d) MUST be resolved before DM-AUDIT partition strategy is finalized; OQ-PRD-001 (sync vs async reset email) before COMP-EMAIL-SENDER queue design.

### Open Questions — M3

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-PRD-001|Should password reset emails be sent synchronously or asynchronously?|Determines whether COMP-EMAIL-SENDER blocks the API-RESET-REQUEST response or returns 202 immediately and processes async.|Engineering|Week 5|
|2|OQ-ADMIN-RBAC-SCOPE|Admin RBAC is out of v1 scope but API-AUDIT-READ requires admin gating — do we ship a hardcoded admin email list or block on RBAC PRD? PRD requires; TDD should be updated.|Blocks API-AUDIT-READ; SOC2 requires admin attribution.|product-team + auth-team|Week 5|

### Risk Assessment and Mitigation — M3

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-OPS-001: Email delivery failures block password reset|Medium|Low|Users locked out; support escalation; PRD success-metric "reset completion >80%" missed|R-OPS-001-MIT delivery monitoring + alerting + fallback support channel|ops-team|
|2|R-COMP-001: Compliance failure from incomplete audit logging|High|Medium|SOC2 audit finding; Q3 2026 audit failure|R-COMP-001-MIT QA gate + automated field-presence test + compliance walkthrough|compliance-lead|
|3|Reset-token enumeration via response timing|Medium|Medium|Account-existence leak; GDPR/security finding|COMP-RESET-RATE-LIMIT uniform 202 + rate limits + timing test|security-lead|
|4|Audit-log write failure silently drops events|High|Low|Missing SOC2 evidence; non-repudiation broken|Async queue with durable fallback to local file; alert on queue lag|auth-team|

## M4: Frontend Integration

**Objective:** Build the React `AuthProvider` context, `LoginPage`, `RegisterPage`, and `ProfilePage`, with silent refresh, HttpOnly cookie handling, 401 interception, and the full E2E journey for Alex the end user. | **Duration:** 2 weeks (Weeks 7–8) | **Entry:** M2 endpoints (/login, /register, /me, /refresh, /logout) available in staging; frontend routing framework ready; M3 reset endpoints reachable (not strictly blocking — can run partially in parallel with M3). | **Exit:** TEST-006 E2E passes against staging; AuthProvider silent refresh demonstrated; accessibility scan on login/register passes; registration <60s E2E verified.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|COMP-004|AuthProvider (React context)|Context provider managing `AuthToken` state; silent refresh; 401 interception; redirect to LoginPage.|Frontend|API-001,API-003,API-004|children-wrapped; accessToken-in-memory-only-no-localStorage; HttpOnly-cookie-for-refresh; silent-refresh-before-expiry; 401-interceptor-triggers-logout; exposes-useAuth-hook-with-user+login+logout+register|M|P0|
|2|COMP-001|LoginPage|Route `/login` with email/password form calling POST /auth/login via AuthProvider.|Frontend|COMP-004|props:{onSuccess,redirectUrl?}; form-validation-email+required-password; generic-error-no-user-enumeration; submit-disabled-while-pending; success-redirects-to-redirectUrl-or-dashboard|M|P0|
|3|COMP-002|RegisterPage|Route `/register` with email/password/displayName form and client-side password-strength validation.|Frontend|COMP-004|props:{onSuccess,termsUrl}; inline-validation-strength+email; consent-checkbox-for-NFR-COMPLIANCE-002; 409-duplicate-email-handled; success-logs-user-in-immediately|M|P0|
|4|COMP-003|ProfilePage|Route `/profile` displaying authenticated `UserProfile`.|Frontend|COMP-004,API-003|auth-required-redirects-to-login-if-not; displays-displayName+email+createdAt; loading-state-handled; error-state-handled; <1s-render-p95|S|P1|
|5|TEST-006|E2E: register → login → profile journey|Playwright test validating FR-AUTH-001 and FR-AUTH-002 end-to-end.|Test|COMP-001,COMP-002,COMP-003,COMP-004|headless-and-headed-modes-pass; tests-register-logout-login-profile; token-persistence-across-page-reload-verified; 60s-registration-budget-asserted|M|P0|
|6|COMP-AUTH-ROUTES|Route guards (ProtectedRoutes wrapper)|Route-level guard redirecting unauthenticated users to LoginPage.|Frontend|COMP-004|wraps-protected-routes; preserves-intended-URL-via-redirectUrl-query-param; renders-loading-during-silent-refresh|S|P0|
|7|COMP-RESET-PAGE-REQUEST|ForgotPasswordPage (/forgot)|Route rendering reset-request form calling API-RESET-REQUEST.|Frontend|COMP-004,API-RESET-REQUEST|email-field; submit-shows-confirmation-regardless-of-existence; does-not-enumerate; rate-limit-message-on-429|S|P0|
|8|COMP-RESET-PAGE-CONFIRM|ResetPasswordPage (/reset?token=)|Route rendering new-password form calling API-RESET-CONFIRM.|Frontend|API-RESET-CONFIRM|token-parsed-from-query; new-password-strength-validated-client-side; success-redirects-to-login; expired/used-token-handled|S|P0|
|9|COMP-LOGOUT-UI|Logout action in AuthProvider|UI action calling API-LOGOUT and clearing in-memory state + cookie.|Frontend|COMP-004,API-LOGOUT|logout-button-rendered-when-authenticated; calls-POST-/auth/logout; clears-context-state; redirects-to-login|S|P0|
|10|COMP-SILENT-REFRESH|Silent refresh scheduling|Background scheduler refreshing accessToken 60s before expiry.|Frontend|COMP-004,API-004|setTimeout-based-schedule-at-access-TTL-minus-60s; refresh-call-non-blocking; on-failure-triggers-logout; scheduled-cleared-on-unmount|S|P0|
|11|COMP-401-INTERCEPTOR|401-response interceptor|Axios/fetch interceptor attempting silent refresh on 401 before surfacing error.|Frontend|COMP-SILENT-REFRESH|intercepts-all-auth-required-API-calls; retries-once-after-refresh; if-refresh-fails-propagates-401; does-not-loop|S|P0|
|12|NFR-JTBD-ALEX-002|Alex seamless cross-device session persistence|Verify tokens persist across tabs/devices per PRD customer journey.|Test|COMP-004|Playwright-test-opens-second-tab-and-verifies-session-alive; refresh-token-cookie-domain-configured-correctly|S|P1|
|13|NFR-A11Y-001|Accessibility scan on LoginPage + RegisterPage|axe-core automated accessibility scan.|Test|COMP-001,COMP-002|no-critical-violations; form-labels-present; keyboard-navigation-works; screen-reader-announces-errors|S|P1|
|14|COMP-FE-METRICS|Frontend registration-funnel analytics|Instrument PRD success metric "Registration conversion >60%".|Frontend|COMP-002|analytics-events-emitted:page_view,form_submit,form_success,form_error; funnel-derivable-from-events|S|P1|

### Integration Points — M4

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|AuthProvider context|React Context|App-root wraps children with `<AuthProvider>`; `useAuth()` hook consumed throughout|M4|All frontend components|
|Route guard|Higher-order component|`<ProtectedRoutes>` + `<PublicRoutes>` wrappers in router config|M4|COMP-003 ProfilePage, future protected routes|
|HTTP interceptor|Fetch/Axios middleware|Global interceptor registered at AuthProvider mount; injects Authorization header + handles 401|M4|All API calls from frontend|
|Silent-refresh scheduler|Strategy/timer|Scheduler attached to accessToken expiry; triggers `tokenManager.refresh()` callback|M4|COMP-004|
|Logout event bus|Callback wiring|`onLogout` callbacks registered by features wanting to clear local caches|M4|COMP-004 consumers|

### Milestone Dependencies — M4

- **Internal:** M2 endpoints live in staging; API-LOGOUT shipped; API-RESET-REQUEST / API-RESET-CONFIRM available (can slip into M5 if M3 delayed).
- **External:** Frontend routing framework (PRD dependency); analytics SDK for funnel metrics.
- **Decision prerequisites:** None blocking — M4 may proceed in parallel with M3 for non-reset pages.

### Open Questions — M4

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-COOKIE-SCOPE|Refresh-token HttpOnly cookie scope (domain + SameSite) — site-wide vs subdomain-restricted?|Affects cross-subdomain session sharing for future features; SameSite=Strict blocks some flows.|security-lead + platform-team|Week 7|

### Risk Assessment and Mitigation — M4

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-001: Token theft via XSS (frontend surface)|High|Medium|Session hijacking|accessToken in memory only (no localStorage); HttpOnly+Secure+SameSite=Lax cookie; CSP enforced; AuthProvider clears on tab close|frontend-lead|
|2|Silent refresh race causes logout loop|Medium|Medium|User-visible flicker/kickout|Scheduler cancels on unmount; 401 interceptor single-retry; Playwright test for concurrent requests|frontend-lead|
|3|CAPTCHA missing on login after repeated failures (R-002 contingency)|Medium|Low|Brute-force mitigation gap|COMP-001 adds CAPTCHA after 3 failed attempts per PRD contingency; feature-flag gate|frontend-lead|
|4|Accessibility regressions block compliance/marketing launch|Low|Medium|Launch delay; legal exposure in some jurisdictions|NFR-A11Y-001 automated scan in CI; manual audit before GA|frontend-lead|

## M5: Phased Rollout & GA

**Objective:** Execute feature-flag-gated phased rollout (Internal Alpha → Beta 10% → GA 100%), land operational readiness (runbooks, capacity, observability, SOC2 evidence), and meet NFR-REL-001 99.9% uptime on the first 7-day GA window. | **Duration:** 2 weeks (Weeks 9–10) | **Entry:** M3 + M4 exit criteria met; feature flags deployed in OFF state; rollback runbooks reviewed. | **Exit:** MIG-003 complete; `AUTH_NEW_LOGIN` flag removed; 99.9% uptime maintained over first 7 days; all success criteria validated; SOC2 evidence package delivered.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|MIG-001|Phase 1 — Internal Alpha|Deploy AuthService to staging; auth-team + QA test all endpoints; flags OFF for production; 1-week duration.|Release|M3,M4|all-FR-AUTH-001..005-pass-manual-testing; zero-P0/P1-bugs; runbooks-rehearsed; sign-off-by-auth-team+QA|M|P0|
|2|MIG-002|Phase 2 — Beta (10% traffic)|Enable `AUTH_NEW_LOGIN` for 10%; monitor latency/errors/Redis; 2-week duration.|Release|MIG-001|p95-latency<200ms-under-10%-load; error-rate<0.1%; no-Redis-connection-failures; rollback-triggered-on-breach-criteria|M|P0|
|3|MIG-003|Phase 3 — General Availability (100%)|Remove `AUTH_NEW_LOGIN` flag; route all users through new AuthService; deprecate legacy endpoints.|Release|MIG-002|99.9%-uptime-first-7-days; all-dashboards-green; legacy-endpoints-return-410-Gone-after-grace-window; flag-removal-merged|M|P0|
|4|FF-AUTH-NEW-LOGIN|Feature flag: AUTH_NEW_LOGIN|Flag gating LoginPage + new AuthService login endpoint; ON-off decisions audited.|Infra|MIG-001|flag-registered-in-flag-service; default=OFF; audit-trail-on-state-change; removal-target=after-Phase3; owner=auth-team|S|P0|
|5|FF-AUTH-TOKEN-REFRESH|Feature flag: AUTH_TOKEN_REFRESH|Flag enabling refresh-token flow in TokenManager.|Infra|MIG-001|flag-registered; default=OFF; enables-COMP-006-refresh-path; removal-target=Phase3+2weeks; owner=auth-team|S|P0|
|6|NFR-REL-001|99.9% availability|Health-check monitoring over 30-day rolling window after GA.|Infra|MIG-003,OPS-005|uptime-monitor-on-/health-endpoint; synthetic-probe-every-30s; SLO-dashboard-tracks-30d-rolling; error-budget-tracked|M|P0|
|7|OPS-003|On-call expectations documented|24/7 auth-team on-call rotation for first 2 weeks post-GA; 15-min P1 acknowledgment.|Docs|-|rotation-calendar-published; acknowledgment-SLA-enforced-via-pager; escalation-path=auth-team→test-lead→eng-manager→platform-team; knowledge-prerequisites-documented|S|P1|
|8|OPS-004|Capacity planning documentation|Document AuthService pod count, PostgreSQL pool, Redis memory for 500-concurrent-user target.|Docs|-|AuthService:3-replicas-HPA-to-10-at-CPU>70%; PG-pool=100-scale-to-200-if-wait>50ms; Redis=1GB-scale-to-2GB-at-70%-util; review-cadence=monthly|S|P1|
|9|OPS-005|Observability stack (metrics/logs/tracing/alerts)|Wire Prometheus metrics, structured logs, OpenTelemetry tracing, Grafana dashboards, alert rules.|Infra|COMP-005,COMP-006,COMP-007,COMP-008|metrics:auth_login_total+auth_login_duration_seconds+auth_token_refresh_total+auth_registration_total; structured-JSON-logs-excl-sensitive; OTEL-spans; alerts:login-fail-rate>20%/5m+p95>500ms+Redis-conn-fail; Grafana-dashboards-published|M|P0|
|10|ROLLBACK-PROC|Rollback procedure validated in staging|End-to-end rollback drill per TDD Migration §Rollback Procedure.|Docs|FF-AUTH-NEW-LOGIN|drill-executed-in-staging; time-to-rollback-measured-<5min; smoke-test-verifies-legacy-path-restored; post-mortem-template-ready|S|P0|
|11|ROLLBACK-CRITERIA|Rollback criteria wired to alerts|Alerts on rollback triggers: p95>1000ms/5min, error>5%/2min, Redis-fail>10/min, data corruption.|Infra|OPS-005|each-criterion-has-dedicated-alert; pages-auth-team-on-call; auto-rollback-optional-manual-default|S|P0|
|12|NFR-PERF-VALIDATION|Load test at GA target capacity|k6 scenario hitting 500 concurrent sustained with full auth journey.|Test|NFR-PERF-002,MIG-001|k6-run-in-staging+prod-mirror; p95<200ms-all-endpoints; Redis-latency<5ms; no-HPA-thrashing|M|P0|
|13|SOC2-EVIDENCE-PKG|SOC2 evidence package for Q3 audit|Compile audit-log samples, access-control docs, retention-policy evidence.|Docs|NFR-COMPLIANCE-001,NFR-COMPLIANCE-001-EVIDENCE|audit-log-samples-12mo-demonstrated; retention-policy-signed; access-controls-documented; compliance-handoff-review-passed|M|P0|
|14|POST-GA-METRICS-REVIEW|Week-2 post-GA success-metrics review|Verify PRD and TDD success metrics meet targets; go/no-go on flag removal.|Docs|MIG-003|registration-conversion>60%-measured; login-p95<200ms-measured; session-duration>30min-measured; failed-login-rate<5%-measured; reset-completion>80%-measured; written-review-circulated|S|P0|
|15|DAU-METRIC-WIRING|Instrument DAU metric (1000/30d target)|Emit daily-unique authenticated-user counter from TokenManager.|Backend|COMP-006|daily-job-counts-distinct-users-from-AuthToken-issuance; dashboard-panel; 30-day-goal-tracked|S|P1|
|16|LEGACY-DEPRECATION|Legacy auth endpoints deprecated & removed|Return 410 Gone + retire code paths after GA + grace window.|Backend|MIG-003|deprecation-header-added-during-Phase2; 410-Gone-after-MIG-003+2weeks; legacy-code-removed-in-follow-up-release|S|P1|

### Integration Points — M5

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|Feature-flag dispatcher|Strategy/flag service|FF-AUTH-NEW-LOGIN + FF-AUTH-TOKEN-REFRESH registered with central flag service; gateway reads on each request|M5|API Gateway, AuthService, TokenManager|
|Rollback automation|Runbook + scripts|`scripts/rollback-auth.sh` sets flags to OFF and runs smoke tests|M5|ROLLBACK-PROC|
|Observability pipeline|Exporter + collector|Prometheus scrapes /metrics; OTEL collector ships spans; logs to aggregator|M5|OPS-005|
|SLO monitor|Alerting rules|PromQL rules for uptime, latency, error-rate wired to pager|M5|NFR-REL-001, ROLLBACK-CRITERIA|
|Deprecation header middleware|Middleware chain|Legacy endpoints emit `Deprecation: true` + `Sunset` header during Phase 2|M5|LEGACY-DEPRECATION|

### Milestone Dependencies — M5

- **Internal:** M3 (reset + audit) and M4 (frontend) complete.
- **External:** Prometheus + Grafana + OpenTelemetry collector provisioned; flag service live; pager integration; SOC2 audit calendar confirmed.
- **Decision prerequisites:** None new — all prior OQs must be resolved by M5 start (any unresolved blocks GA go/no-go).

### Risk Assessment and Mitigation — M5

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-003: Data loss during migration from legacy auth|High|Low|UserProfile corruption; customer-visible account loss|MIG-001/002 parallel run; idempotent upsert; full DB backup per phase; documented rollback|auth-team + platform-team|
|2|99.9% uptime missed in first 7 days|High|Medium|GA rolled back; PRD NFR-REL-001 fails|ROLLBACK-CRITERIA alerts; HPA pre-scaled; incident-response rehearsal|platform-team|
|3|SOC2 audit-evidence incomplete at Q3 audit|High|Low|Audit finding; contract/enterprise risk|SOC2-EVIDENCE-PKG reviewed with compliance 2 weeks before audit|compliance-lead|
|4|Success-metrics review reveals missed targets (e.g., conversion <60%)|Medium|Medium|Blocks flag removal; churn risk|POST-GA-METRICS-REVIEW decision point; iterate before removing flags|product + auth-team|
|5|R-BUS-001: Low registration adoption due to poor UX|Medium|Medium|PRD conversion metric missed; business-case justification weakened|Usability testing in MIG-001; funnel iteration in Beta; NFR-JTBD-ALEX-001 budget enforced|product-team|

## Resource Requirements and Dependencies

### External Dependencies

|Dependency|Required By MLS|Status|Fallback|
|---|---|---|---|
|PostgreSQL 15+ (INFRA-DB-001)|M1|Provisioned|Degraded read-only via read-replica; DB migration tooling supports fallback|
|Redis 7+ cluster|M2|Provisioned|Without Redis, refresh flow disabled; users forced to re-login after access expiry|
|Node.js 20 LTS runtime|M1|Available|Downgrade blocked — Node 20 LTS features required|
|bcryptjs library|M1|Available|pnpm-lock pinning; alt: native bcrypt|
|jsonwebtoken library|M2|Available|Pinned version; alt: jose library|
|SendGrid API|M3|Pending provisioning|Fallback to SES or Mailgun; COMP-EMAIL-SENDER interface abstraction enables swap|
|API Gateway (rate limit + CORS)|M1|Provisioned|In-process rate-limit middleware as fallback|
|Prometheus + Grafana|M5|Provisioned|Alternative: Datadog or CloudWatch|
|OpenTelemetry collector|M5|Provisioned|Degraded observability with logs-only|
|SEC-POLICY-001|M1|Ratified|Block — required for config defaults|
|AUTH-PRD-001 (parent)|All|Draft (Week 1)|Approval required before MIG-001|
|Frontend routing framework|M4|Available|Blocks M4 if unavailable|
|RSA keypair + secrets volume|M2|Pending platform-team|Blocks M2 signing; interim self-signed keys in staging|

### Infrastructure Requirements

- **AuthService pods**: 3 replicas baseline, HPA to 10 replicas on CPU >70% (OPS-004).
- **PostgreSQL**: connection pool size 100 baseline, scale to 200 if wait time >50ms; monthly partitioning for `AuditLog` table.
- **Redis**: 1 GB baseline, 2 GB if >70% utilization; HA (sentinel or managed service) to mitigate OPS-002 risk.
- **SendGrid**: verified sender domain with SPF/DKIM/DMARC; webhook endpoint for delivery events (R-OPS-001-MIT).
- **Kubernetes**: HPA configured; pod disruption budget ≥2; network policies restricting AuthService egress to PostgreSQL, Redis, SendGrid, secrets service.
- **Secrets management**: RSA keypair mounted via K8s Secret or secrets manager (Vault/AWS SM); quarterly rotation runbook (COMP-JWT-ROTATION).
- **Observability**: Prometheus scrape targets for AuthService; OpenTelemetry collector reachable from pods; Grafana dashboards provisioned; alert rules wired to pager.
- **CI/CD**: migration runner invoked before test stage; testcontainers for PostgreSQL + Redis in CI; k6 load-test runner for NFR-PERF-002.
- **Team staffing**: auth-team (2 backend eng), 1 frontend eng (M4), 1 QA (M1–M5), compliance-lead (part-time M1–M3, full for M5 SOC2 pkg), platform-team liaison.

## Risk Register

|ID|Risk|Affected Milestones|Probability|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|R-001|Token theft via XSS allows session hijacking|M2, M4|Medium|High|accessToken in memory only; HttpOnly+Secure+SameSite=Lax refresh cookie; 15m access TTL; AuthProvider clears on tab close; TokenManager revocation path|security-lead|
|R-002|Brute-force attacks on login endpoint|M1|High|Medium|Gateway rate limit (10/min/IP); lockout after 5 failed attempts in 15 min (R-002-MIT); bcrypt cost 12; CAPTCHA after 3 fails (M4 contingency)|security-lead + auth-team|
|R-003|Data loss during migration from legacy auth|M5|Low|High|Parallel run in MIG-001/002; idempotent UserProfile upsert; full DB backup per phase; rollback playbook|auth-team + platform-team|
|R-BUS-001|Low registration adoption due to poor UX|M4, M5|Medium|High|Usability testing pre-launch; NFR-JTBD-ALEX-001 60s budget; funnel iteration in Beta|product-team|
|R-COMP-001|Compliance failure from incomplete audit logging|M3, M5|Medium|High|DM-AUDIT SOC2-required fields; NFR-COMPLIANCE-001 automated validation; SOC2-EVIDENCE-PKG; R-COMP-001-MIT QA gate|compliance-lead|
|R-OPS-001|Email delivery failures blocking password reset|M3|Low|Medium|R-OPS-001-MIT delivery monitoring + alerting + fallback support channel; retry with exponential backoff|ops-team|
|R-PERF-001|bcrypt cost 12 breaches p95 latency budget under load|M1, M2, M5|Low|Medium|Benchmark in week 1; HPA floor adjustment; revisit cost only if >400ms hash-time measured|auth-team|
|R-REPLAY-001|Refresh-token replay via race condition|M2|Medium|High|Atomic Lua script for validate→revoke→issue; idempotency-key on refresh request|auth-team|
|R-ROTATE-001|RSA key rotation breaks active sessions|M2, M5|Medium|Medium|Dual-validation window (current+previous kid); rotation runbook tested in staging|platform-team|
|R-AUDIT-RETENTION|PRD/TDD retention conflict not resolved before schema freeze|M1, M3|Medium|High|Gate DM-001 and DM-AUDIT on OQ-AUDIT-RETENTION resolution; default to 12m if unresolved|compliance-lead|
|R-LOCKOUT-001|Lockout counter race conditions in Redis|M1|Medium|Medium|Atomic INCR + EXPIRE; concurrent integration test|auth-team|
|R-RESET-ENUM|Reset-token flow enables account enumeration|M3|Medium|Medium|Uniform 202 response; COMP-RESET-RATE-LIMIT; timing side-channel test|security-lead|
|R-AUDIT-SILENT|Audit-log write failure silently drops events|M3|Low|High|Async queue + durable fallback file; queue-lag alert|auth-team|
|R-UPTIME-001|99.9% uptime missed in first 7 days|M5|Medium|High|ROLLBACK-CRITERIA alerts; HPA pre-scaled; rehearsal drill|platform-team|
|R-METRICS-MISS|Success metrics missed at POST-GA review|M5|Medium|Medium|POST-GA-METRICS-REVIEW decision point; iterate before flag removal|product + auth-team|

## Success Criteria and Validation Approach

|Criterion|Metric|Target|Validation Method|MLS|
|---|---|---|---|---|
|Login latency (technical, TDD)|p95 of AuthService.login()|<200ms|APM histogram on /auth/login|M2, M5|
|Registration success rate|successful_registrations / attempts|>99%|Log aggregation ratio|M1, M5|
|Token refresh latency|p95 of TokenManager.refresh()|<100ms|APM histogram on /auth/refresh|M2, M5|
|Service availability (NFR-REL-001)|uptime over rolling 30 days|99.9%|Synthetic probe on /health|M5|
|Password hash time|bcrypt cost 12 benchmark|<500ms|Unit-test benchmark|M1|
|Unit test coverage|statement coverage for AuthService, TokenManager, JwtService, PasswordHasher|>80%|Jest coverage report in CI|M1, M2|
|FR implementation completeness|FR-AUTH-001..005 passing tests|100%|Test suite execution|M5|
|Integration tests pass|testcontainers PostgreSQL + Redis suites|All green|CI pipeline|M1, M2, M3|
|Concurrent-user load|500 VUs sustained, p95<200ms|Pass|k6 scenario|M2, M5|
|Registration conversion (PRD)|landing → confirmed account|>60%|Frontend funnel analytics|M4, M5|
|Daily active authenticated users|unique users per day|>1000 within 30 days of GA|AuthToken issuance counter|M5|
|Avg session duration (PRD)|seconds between first token and last refresh|>30 minutes|Token refresh event analytics|M5|
|Failed login rate (PRD)|failed / total login attempts|<5%|Auth event log analysis|M5|
|Password reset completion (PRD)|reset-confirm / reset-request|>80%|Funnel metric from COMP-PWDRESET-METRICS|M3, M5|
|SOC2 audit fields completeness|% of events with user_id+timestamp+ip+outcome|100%|Automated field-presence test (R-COMP-001-MIT)|M3, M5|
|Audit-log retention|online retention window|12 months|Partition rotator verifies partitions present|M3|
|Accessibility|axe-core critical violations on LoginPage/RegisterPage|0|CI accessibility scan (NFR-A11Y-001)|M4|
|Alex JTBD: <60s registration|E2E registration duration|<60s|Playwright timing assertion|M1, M4|
|Jordan JTBD: audit queryability|admin can query by userId + date range|Query returns within 2s|API-AUDIT-READ integration test|M3|

## Decision Summary

|Decision|Chosen|Alternatives Considered|Rationale|
|---|---|---|---|
|Token architecture|Stateless JWT access (15m) + opaque Redis refresh (7d)|HS256 symmetric JWT; localStorage-persisted tokens; stateful sessions|R-001 requires refresh revocation and XSS resistance; TDD mandates RS256; in-memory access prevents XSS exfiltration|
|Signing algorithm|RS256 with 2048-bit RSA keys|HS256; RS512; ES256|TDD/NFR-SEC-002 explicit mandate; 2048-bit aligns with NIST baseline; RS256 enables public-key verification at gateway without secret sharing|
|Password hashing|bcrypt cost factor 12|argon2; PBKDF2; scrypt; cost 10/14|NIST SP 800-63B compliance (NFR-COMPLIANCE-003); cost-12 benchmark hash-time <500ms matches NFR-PERF-001; PasswordHasher abstraction allows future migration|
|Primary datastore|PostgreSQL 15+ with pg-pool|MongoDB; MySQL 8; DynamoDB|INFRA-DB-001 provisioned; relational constraints needed for email-uniqueness, audit partitioning, consent immutability|
|Refresh-token store|Redis 7+ with 7-day TTL|In-DB token table; signed stateless refresh|TDD mandate; Redis TTL provides free expiration; revocation is O(1) DEL; refresh tokens never persisted long-term in PG|
|Rollout strategy|Feature-flag phased rollout: Alpha → 10% Beta → 100% GA|Big-bang cutover; canary 5%/25%/50%/100%|R-003 requires bounded blast radius; TDD specifies AUTH_NEW_LOGIN + AUTH_TOKEN_REFRESH flags; rollback <5min|
|Audit-log retention|12 months (resolving OQ-AUDIT-RETENTION in favor of PRD)|90 days (per TDD §7.2)|PRD NFR-COMPLIANCE-001 SOC2 requirement governs; TDD should be updated to align|
|Admin RBAC for audit API|Hardcoded admin list stub for v1|Full RBAC implementation; OAuth-claims-based|Full RBAC out of v1 scope; API-AUDIT-READ still required for Jordan JTBD and SOC2; documented as tech debt|
|Email sync vs async|Async via queue (resolving OQ-PRD-001)|Synchronous inline send|Prevents API-RESET-REQUEST latency spikes; enables retry with backoff; 202-Accepted response pattern|
|Silent-refresh scheduling|Client-side setTimeout at access-TTL minus 60s|Server push; lazy refresh on 401 only|Cache-friendly; bounded clock skew; 401-interceptor is fallback, not primary path|
|Cookie scope|HttpOnly + Secure + SameSite=Lax|SameSite=Strict; SameSite=None|Strict blocks legitimate cross-site flows; None requires Secure and is weaker; Lax balances UX and CSRF resistance|
|API versioning|URL prefix /v1/auth/*|Header-based versioning; no versioning|TDD explicit mandate; well-understood; enables deprecation via HTTP codes (LEGACY-DEPRECATION)|

## Timeline Estimates

|MLS|Duration|Start|End|Key Milestones|
|---|---|---|---|---|
|M1|2 weeks|Week 1|Week 2|DM-001 schema migrated; PasswordHasher tested at cost 12; FR-AUTH-001/002 integration-tested; OPS-001 runbook ready|
|M2|2 weeks|Week 3|Week 4|JwtService+TokenManager shipped; FR-AUTH-003/004 passing; k6 500-concurrent test passes; API-LOGOUT gap filled|
|M3|2 weeks|Week 5|Week 6|FR-AUTH-005 shipped; DM-AUDIT partitioned (12-month); API-AUDIT-READ for Jordan JTBD; SOC2 field-validation test green|
|M4|2 weeks|Week 7|Week 8|AuthProvider + LoginPage/RegisterPage/ProfilePage shipped; TEST-006 E2E green; a11y scan passes|
|M5|2 weeks|Week 9|Week 10|MIG-001→002→003 complete; 99.9% uptime maintained; SOC2 evidence package delivered; post-GA metrics review passed|

**Total estimated duration:** 10 weeks (Week 1 through Week 10)

