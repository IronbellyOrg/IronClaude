---
spec_source: "test-tdd-user-auth.compressed.md"
complexity_score: 0.65
complexity_class: MEDIUM
primary_persona: architect
adversarial: false
generated: "2026-04-18"
generator: "single"
total_milestones: 5
total_task_rows: 86
risk_count: 11
open_questions: 8
domain_distribution:
  frontend: 15
  backend: 45
  security: 20
  performance: 8
  documentation: 12
consulting_personas: [architect, security, backend, frontend, qa, devops]
milestone_count: 5
milestone_index:
  - id: M1
    title: "Foundation, Data Layer & Security Primitives"
    type: FEATURE
    priority: P0
    dependencies: []
    deliverable_count: 19
    risk_level: Medium
  - id: M2
    title: "Authentication Core Services & Token Lifecycle"
    type: FEATURE
    priority: P0
    dependencies: [M1]
    deliverable_count: 22
    risk_level: High
  - id: M3
    title: "Password Reset, Compliance & Admin Audit"
    type: FEATURE
    priority: P0
    dependencies: [M2]
    deliverable_count: 14
    risk_level: Medium
  - id: M4
    title: "Frontend Integration & End-to-End Flows"
    type: FEATURE
    priority: P1
    dependencies: [M2]
    deliverable_count: 13
    risk_level: Medium
  - id: M5
    title: "Migration, Observability & GA Rollout"
    type: MIGRATION
    priority: P0
    dependencies: [M3, M4]
    deliverable_count: 18
    risk_level: High
total_deliverables: 86
total_risks: 11
estimated_milestones: 5
validation_score: 0.0
validation_status: SKIPPED
---

# User Authentication Service — Project Roadmap

## Executive Summary

The User Authentication Service delivers the platform's foundational identity layer: self-service registration, email/password login, persistent sessions with silent refresh, profile access, and self-service password reset. It unblocks the Q2–Q3 2026 personalization roadmap (~$2.4M ARR) and closes the SOC2 Type II compliance gap scheduled for Q3 2026 audit.

**Business Impact:** Unblocks personalized dashboards, saved preferences, and activity history; removes 30% QoQ growth in access-related support tickets; satisfies SOC2 user-level audit logging; addresses the 25% of churn surveys citing absence of accounts. Target KPIs: registration conversion >60%, login p95 <200ms, avg session >30 min, failed login <5%, password reset completion >80%.

**Complexity:** MEDIUM (0.65) — 5 FRs across 4 external integration points (PostgreSQL, Redis, SendGrid, API Gateway), high security burden (bcrypt cost 12, RS256 rotation, refresh revocation, lockout, anti-enumeration, GDPR+SOC2+NIST), moderate frontend surface with silent refresh, staged 3-phase rollout with dual feature flags. Not HIGH: no MFA, no OAuth, no RBAC enforcement, single service boundary.

**Critical path:** INFRA-DB-001 provisioning → data-model migrations → `PasswordHasher` + `JwtService` primitives → `AuthService` login/register → `TokenManager` refresh → audit logging → `AuthProvider` silent refresh → MIG-001 alpha → MIG-002 10% beta → MIG-003 GA.

**Key architectural decisions:**

- Stateless JWT access tokens (RS256, 15-min TTL) with opaque refresh tokens stored hashed in Redis (7-day TTL) — decouples authentication from session state and enables horizontal scaling of `AuthService` pods behind HPA (CPU >70%).
- PostgreSQL 15 for durable `UserProfile` + audit log persistence; Redis 7 for refresh-token revocation and rate-limit counters — isolates ephemeral and durable concerns.
- Three-phase staged rollout gated by feature flags `AUTH_NEW_LOGIN` and `AUTH_TOKEN_REFRESH` with explicit quantitative rollback triggers (p95 >1000ms, error >5%, Redis failures >10/min).

**Open risks requiring resolution before M1:**

- Audit retention conflict (TDD 90d vs PRD 12m) must be resolved before schema migration — locks in partition/retention strategy on the audit table.
- OQ-PRD-003 lockout threshold (5/15min in TDD vs pending Security refinement) should be fixed before gateway rate-limit wiring lands in M2.
- SendGrid account, sender domain, and SPF/DKIM must be provisioned before M3 password-reset work starts.

## Milestone Summary

|ID|Title|Type|Priority|Effort|Dependencies|Deliverables|Risk|
|---|---|---|---|---|---|---|---|
|M1|Foundation, Data Layer & Security Primitives|FEATURE|P0|2 weeks|—|19|Medium|
|M2|Authentication Core Services & Token Lifecycle|FEATURE|P0|3 weeks|M1|22|High|
|M3|Password Reset, Compliance & Admin Audit|FEATURE|P0|2 weeks|M2|14|Medium|
|M4|Frontend Integration & End-to-End Flows|FEATURE|P1|2 weeks|M2|13|Medium|
|M5|Migration, Observability & GA Rollout|MIGRATION|P0|3 weeks|M3, M4|18|High|

## Dependency Graph

```
M1 (Foundation & Data) ──► M2 (Auth Core & Tokens) ──┬──► M3 (Reset, Compliance, Admin Audit) ──┐
                                                     │                                           │
                                                     └──► M4 (Frontend Integration)  ────────────┼──► M5 (Migration, Observability, GA)
                                                                                                 │
External: INFRA-DB-001, SEC-POLICY-001, SendGrid, k8s/API-Gateway ────────────────► feeds M1..M5
```

## M1: Foundation, Data Layer & Security Primitives

**Objective:** Provision infrastructure, land data models, and implement cryptographic primitives so downstream auth flows compose against stable, secure building blocks. | **Duration:** 2 weeks (Weeks 1–2) | **Entry:** INFRA-DB-001 capacity approved; SEC-POLICY-001 reviewed; audit retention conflict resolved. | **Exit:** PostgreSQL + Redis schemas live in staging; `PasswordHasher` and `JwtService` unit-tested at cost 12 / RS256-2048; /v1/auth skeleton boots; API versioning middleware in place.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|INFRA-DB-001|Provision PostgreSQL 15 + Redis 7|Stand up managed PG 15 primary+replica and Redis 7 cluster with TLS; wire k8s secrets and connection pooling.|Infra|—|PG 15 reachable via pgbouncer (pool=100); Redis 7 with maxmemory=1GB, AOF on; TLS 1.3 enforced; credentials in k8s secret|M|P0|
|2|DM-001|UserProfile table schema + migration|Create `users` table for `UserProfile` with all fields, indexes, and constraints per extraction.|Backend|INFRA-DB-001|id:UUID-PK-NOTNULL; email:varchar-UNIQUE-NOTNULL-lowercase-indexed; display_name:varchar-NOTNULL-2to100; created_at:timestamptz-NOTNULL-default-now(); updated_at:timestamptz-NOTNULL-auto-trigger; last_login_at:timestamptz-NULLABLE; roles:text[]-NOTNULL-default-{user}; migration idempotent|M|P0|
|3|DM-002|AuthToken DTO + Redis refresh-token schema|Define `AuthToken` TypeScript interface and Redis key layout for hashed refresh tokens with per-user index.|Backend|INFRA-DB-001|access_token:string-JWT-RS256; refresh_token:string-NOTNULL-unique; expires_in:number-NOTNULL-eq-900; token_type:string-NOTNULL-eq-Bearer; Redis key `rt:{userId}:{tokenId}` stores SHA-256 hash with TTL=7d|S|P0|
|4|DM-003|Audit log table schema + migration|Create `auth_audit_log` table with partitioning strategy driven by retention resolution.|Backend|INFRA-DB-001, OQ-PRD-AUDIT-RETENTION|id:UUID-PK; user_id:UUID-FK-NULLABLE; event_type:enum-NOTNULL; timestamp:timestamptz-NOTNULL-indexed; ip_address:inet-NOTNULL; outcome:enum-NOTNULL; metadata:jsonb; monthly-range-partitioned; retention honors resolved policy (12m per PRD wins over 90d TDD)|M|P0|
|5|DM-004|PasswordResetToken schema|Table/row for one-time reset tokens with hashed value, expiry, and usage flag.|Backend|INFRA-DB-001|id:UUID-PK; user_id:UUID-FK-NOTNULL; token_hash:varchar-NOTNULL-indexed; expires_at:timestamptz-NOTNULL; used_at:timestamptz-NULLABLE; created_at:timestamptz-NOTNULL; unique(token_hash); cleanup job drops rows where used_at OR expires_at<now()-7d|S|P0|
|6|COMP-007|AuthService skeleton (Node.js 20 LTS)|Scaffold `AuthService` class in Node 20 with DI container, config loader, and error mapping.|Backend|INFRA-DB-001|Class exposed at `src/services/AuthService.ts`; DI wires `PasswordHasher`, `TokenManager`, `UserRepo`; Node 20.x engines pinned in package.json; error→HTTP mapping via `ErrorEnvelope`|M|P0|
|7|COMP-008|PasswordHasher component|bcryptjs wrapper enforcing cost 12 with `hash()` and `verify()` methods plus perf guard.|Backend|COMP-007|cost=12 enforced via config; hash returns bcrypt $2b$ string; verify constant-time; perf <500ms p95 on target pod; unit test asserts cost param=12 (NFR-SEC-001)|S|P0|
|8|COMP-009|JwtService component|RS256 signer/verifier with 2048-bit RSA keys, kid header, and ±5s clock skew tolerance.|Backend|COMP-007|alg=RS256; 2048-bit RSA key pair loaded from k8s secret; kid in header; iss/aud/exp/iat claims set; verify honors ±5s skew (NFR-SEC-002); unit test fails if HS256 used|M|P0|
|9|COMP-010|TokenManager component|Issue/rotate/revoke pair composed of JWT access + opaque refresh stored in Redis.|Backend|COMP-009, DM-002|`issueTokens(userId,roles)` returns `AuthToken`; `rotate(refreshToken)` revokes old, issues new pair atomically; `revokeAll(userId)` deletes all user rt:* keys; access-token TTL=900s, refresh TTL=7d|M|P0|
|10|COMP-011|AuditLogger component|Structured-log emitter that writes to `auth_audit_log` and JSON stdout with PII redaction.|Backend|DM-003|Emits {user_id,event,timestamp,ip,outcome}; never logs password/tokens; writes synchronously to PG on auth-critical events; async batch for non-critical; SOC2 fields present|M|P0|
|11|COMP-012|API Gateway routing + rate-limit wiring|Configure gateway to terminate TLS, apply per-route rate limits, and forward to `AuthService` pods.|Infra|COMP-007|TLS 1.3 terminated at gateway; `/v1/auth/login`=10rpm/IP, `/v1/auth/register`=5rpm/IP, `/v1/auth/refresh`=30rpm/user, `/v1/auth/me`=60rpm/user; 429 envelope returned; HSTS enabled|M|P0|
|12|COMP-013|SendGrid email client wrapper|Thin client for transactional email used by password reset; retries + dead-letter on failure.|Backend|COMP-007|POST SendGrid v3 API with bearer key from secret; exponential backoff 3 retries; DLQ to Redis list `email:dlq`; templates referenced by ID; sandbox mode gated by env|S|P1|
|13|NFR-SEC-001|Bcrypt cost-factor policy test + key in config|Enforce bcrypt cost=12 via configuration guard and CI test that fails on deviation.|Security|COMP-008|Unit test `expect(hash.$2b$12$)`; CI lint rejects cost<12; SEC-POLICY-001 referenced in PR template|S|P0|
|14|NFR-SEC-002|RS256 key management + rotation runbook|Generate 2048-bit RSA pair, mount via k8s secret, document quarterly rotation.|Security|COMP-009|2048-bit keys generated with ssh-keygen/openssl; kid rolled on rotation; verifier accepts N and N-1 kid for overlap window; rotation runbook in `/runbooks/auth-key-rotation.md`|M|P0|
|15|NFR-COMPLIANCE-003|NIST SP 800-63B hashing conformance|Assert bcrypt+cost12 satisfies NIST 800-63B §5.1.1.2 adaptive hashing.|Security|NFR-SEC-001|Compliance memo attached to PR citing NIST control; raw passwords never persisted or logged; CI grep rejects `password:` log patterns|S|P0|
|16|NFR-COMPLIANCE-004|GDPR data minimization review|Verify schema collects only email, hashed password, display_name; no additional PII.|Compliance|DM-001|DM-001 schema matches; DPIA memo filed; removal of any extra fields gated by privacy review|S|P1|
|17|API-VERSION-MW|URL versioning middleware (/v1/auth/*)|Express middleware enforcing `/v1/auth` prefix and rejecting unknown versions with 404.|Backend|COMP-007|All auth routes mount under `/v1/auth`; unknown `/v2/..` returns 404 envelope; additive fields allowed within v1; CORS middleware restricts to known frontend origins|S|P0|
|18|ERROR-ENVELOPE|Unified JSON error envelope|Shared error serializer producing `{error:{code,message,status}}` across endpoints.|Backend|COMP-007|All 4xx/5xx responses conform to envelope; codes stable and documented; no stack traces leaked to clients; integration test enforces shape|S|P0|
|19|CORS-CONFIG|CORS origin allow-list|Whitelist known frontend origins; reject others.|Security|API-VERSION-MW|`Access-Control-Allow-Origin` set from ALLOWED_ORIGINS env; preflight OPTIONS supported; credentials mode compatible with HttpOnly cookies|S|P0|

### Integration Points — M1

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|DI container|Dependency injection|`AuthService`→`PasswordHasher`,`JwtService`,`TokenManager`,`AuditLogger`,`UserRepo`|M1|M2 handlers|
|Gateway rate-limit table|Dispatch table|Per-route limits keyed on `(route,identity_scope)`|M1|M2 APIs|
|JWT `kid` registry|Registry|Active + previous key IDs for verification overlap|M1|M2 token verify, M5 rotation|
|Error envelope serializer|Middleware chain|Wraps all controller errors into `{error:{code,message,status}}`|M1|M2/M3/M4 endpoints|
|CORS middleware|Middleware chain|Allow-list from `ALLOWED_ORIGINS` env|M1|M4 frontend calls|
|SendGrid template ID map|Registry|`reset_request`→template_id|M1|M3 password reset|

### Milestone Dependencies — M1

- INFRA-DB-001 provisioning ticket must be closed before DM-001..004 migrations apply.
- SEC-POLICY-001 sign-off required for NFR-SEC-001/002 acceptance.

### Risk Assessment and Mitigation — M1

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Audit retention conflict unresolved at schema-freeze time forces costly re-partitioning|Medium|Medium|Rework of DM-003 migration; possible data backfill|Drive resolution in Week 1; design partition scheme to support both 90d and 12m with config switch|compliance-lead|
|2|RS256 key rotation procedure untested, risks mass-logout at first rotation|High|Low|All users force-logged-out; SLA breach|Implement kid overlap window (N + N-1); dry-run rotation in staging end of M1|security-lead|
|3|Bcrypt cost=12 exceeds 500ms budget on smaller pod SKU|Medium|Medium|Login latency breach of NFR-PERF-001|Benchmark during M1; reserve CPU limits; fallback plan to vertical-scale pod class|auth-team|

### Open Questions — M1

|#|ID|Question|Impact|Owner|Target|
|---|---|---|---|---|---|
|1|OQ-PRD-AUDIT-RETENTION|Resolve audit retention: PRD 12 months vs TDD 90 days. DM-003 partition/retention policy blocks until resolved. PRD requires; TDD should be updated.|Blocks DM-003 migration design and storage sizing|compliance-lead, product-manager|Before end of Week 1|
|2|OQ-001|Should `AuthService` support API key authentication for service-to-service calls?|Affects gateway routing and `AuthService` scope boundary; currently deferred to v1.1|test-lead|2026-04-15 (deferred to v1.1)|

## M2: Authentication Core Services & Token Lifecycle

**Objective:** Implement the four core auth endpoints (login, register, profile, refresh) with unit/integration test coverage, wiring rate limits, lockout, anti-enumeration, and token rotation against the M1 primitives. | **Duration:** 3 weeks (Weeks 3–5) | **Entry:** M1 exit criteria met; OQ-PRD-003 lockout threshold confirmed. | **Exit:** FR-AUTH-001..004 pass with ≥80% unit coverage on `AuthService`/`TokenManager`/`JwtService`/`PasswordHasher`; k6 shows p95 <200ms at 500 concurrent; integration suite green on testcontainers.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-AUTH-001|Login with email and password|`AuthService.login(email,password)` validates against bcrypt hash via `PasswordHasher`, issues `AuthToken` via `TokenManager`.|Backend|COMP-007, COMP-008, COMP-010|Valid creds→200 + `AuthToken`(access+refresh); invalid→401 generic; non-existent email→401 (no enumeration); lockout after 5 failures in 15 min→423|M|P0|
|2|API-001|POST /v1/auth/login endpoint|Express handler wrapping `AuthService.login`; rate-limit 10rpm/IP at gateway; response shape `AuthToken`.|Backend|FR-AUTH-001, COMP-012|Route mounted; request `{email,password}`; 200 returns `AuthToken`; 401 invalid; 423 locked; 429 rate-limited; error envelope used|S|P0|
|3|FR-AUTH-002|User registration with validation|`AuthService.register(email,password,displayName)` validates uniqueness, password strength, creates `UserProfile`, hashes via `PasswordHasher`.|Backend|COMP-007, COMP-008, DM-001|Valid→201 + `UserProfile`; duplicate email→409; weak pwd (<8 chars / no upper / no digit)→400; bcrypt hash written with cost=12|M|P0|
|4|API-002|POST /v1/auth/register endpoint|Express handler wrapping `AuthService.register`; rate-limit 5rpm/IP; GDPR consent capture.|Backend|FR-AUTH-002, COMP-012, NFR-COMPLIANCE-001|Route mounted; request `{email,password,displayName,consent}`; 201 returns `UserProfile`; 409 dup; 400 validation; consent_at timestamp persisted|S|P0|
|5|FR-AUTH-003|JWT token issuance and refresh|`TokenManager.issueTokens()` and `TokenManager.rotate()` implement 15-min access + 7-day refresh with Redis-backed revocation.|Backend|COMP-009, COMP-010|Login issues pair; `/v1/auth/refresh` swaps tokens; expired refresh→401; revoked refresh→401; old refresh revoked atomically on rotation|M|P0|
|6|API-004|POST /v1/auth/refresh endpoint|Handler consuming `{refreshToken}` and returning new `AuthToken` pair; old token single-use.|Backend|FR-AUTH-003, COMP-012|Route mounted; rate-limit 30rpm/user; valid→200 pair; reuse-detection→401 + revoke all user tokens; error envelope used|S|P0|
|7|FR-AUTH-004|User profile retrieval|`AuthService.me(accessToken)` returns `UserProfile` fields.|Backend|COMP-007, DM-001, COMP-009|GET `/v1/auth/me` with valid AT→200 `UserProfile`; includes id,email,displayName,createdAt,updatedAt,lastLoginAt,roles; expired/invalid→401|S|P0|
|8|API-003|GET /v1/auth/me endpoint|Handler verifying Bearer token via `JwtService` and delegating to `AuthService.me`.|Backend|FR-AUTH-004, COMP-012|Route mounted; rate-limit 60rpm/user; Authorization header required; 401 missing/expired/invalid|S|P0|
|9|COMP-LOGIN-ATTEMPT-TRACKER|Failed-login attempt tracker (Redis)|Redis counter per email/IP with 15-min sliding window used to enforce lockout after 5 failures.|Backend|INFRA-DB-001, FR-AUTH-001|Key `loginfail:{email}` incr on 401; EXPIRE=900s; reaches 5→return 423 and lock flag; reset on successful login; OQ-PRD-003 threshold honored|M|P0|
|10|COMP-ANTIENUM|Anti-enumeration response normalizer|Shared helper ensuring login + reset-request return identical timing and messages regardless of email existence.|Security|FR-AUTH-001|Constant-time compare on hash verify even when user missing; 401 message identical in both cases; p95 delta <20ms between hit and miss|M|P0|
|11|NFR-PERF-001|Auth endpoint latency <200ms p95|Instrument APM on `AuthService` methods; profile and tune.|Performance|API-001..API-004|APM histograms report p95 <200ms across all four endpoints in staging under nominal load|M|P0|
|12|NFR-PERF-002|500 concurrent login capacity|k6 load test script exercising login at 500 VU sustained.|Performance|API-001, COMP-012|k6 scenario `login-500vu` passes with error rate <0.1%, p95 <200ms; report archived to /perf-results/|M|P0|
|13|TEST-001|Unit: login valid creds returns AuthToken|Jest unit test mocking `PasswordHasher.verify=true` and `TokenManager.issueTokens`.|Testing|FR-AUTH-001|Test asserts 200 + access + refresh; mocks verified; FR-AUTH-001 traced|S|P0|
|14|TEST-002|Unit: login invalid creds returns 401|Jest unit test mocking `PasswordHasher.verify=false`.|Testing|FR-AUTH-001|Test asserts 401 generic; no AuthToken; no TokenManager call; FR-AUTH-001 traced|S|P0|
|15|TEST-003|Unit: TokenManager refresh rotates pair|Jest unit test with Redis mock hit and `JwtService.sign`.|Testing|FR-AUTH-003|Old token marked revoked; new pair issued; FR-AUTH-003 traced|S|P0|
|16|TEST-004|Integration: register persists UserProfile|Supertest + testcontainers PG; POST /register; assert row + bcrypt hash column.|Testing|FR-AUTH-002, DM-001|201 returned; users row exists; password column matches $2b$12$ prefix|M|P0|
|17|TEST-005|Integration: expired refresh rejected|Supertest + testcontainers Redis; seed expired token; POST /refresh.|Testing|FR-AUTH-003|401 returned; revocation log entry written|S|P0|
|18|COMP-AUDIT-HOOKS|Wire AuditLogger into login/register/refresh|Inject `AuditLogger` into each handler to emit success/failure events.|Backend|COMP-011, API-001..API-004|Events `login.success`, `login.failure`, `register.success`, `token.refresh.success`, `token.refresh.failure` written to `auth_audit_log` with user_id,ip,outcome|S|P0|
|19|NFR-COMPLIANCE-001|GDPR consent capture at registration|Persist consent boolean + timestamp on `UserProfile` creation.|Compliance|FR-AUTH-002, DM-001|Consent column added via migration; API-002 requires `consent=true`; false→400; timestamp stored; audit event emitted|S|P0|
|20|HEALTHCHECK|Health check endpoint for AuthService|`/v1/auth/healthz` reports PG + Redis + JWT-key status.|Backend|COMP-007, INFRA-DB-001|GET returns 200 with `{pg:ok,redis:ok,jwtKey:ok}`; 503 if any component fails; used by k8s readiness probe|S|P1|
|21|OPENAPI-DOC|OpenAPI 3.1 spec for /v1/auth|Publish OpenAPI document covering login/register/me/refresh.|Documentation|API-001..API-004|`/v1/auth/openapi.json` served; all request/response schemas defined; error envelope documented; Sam-persona clarity review passes|S|P1|
|22|GATEWAY-LOCKOUT-WIRING|Dispatch lockout and rate-limit state into gateway|Strategy wiring ensuring 423 and 429 responses originate correctly and consistently.|Security|COMP-012, COMP-LOGIN-ATTEMPT-TRACKER|423 on lockout; 429 on rate; headers `Retry-After` set; integration test covers both|S|P0|

### Integration Points — M2

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|Express route registry|Dispatch table|`/v1/auth/{login,register,me,refresh}`→handlers|M2|M4 frontend|
|Rate-limit strategy|Strategy pattern|Per-route policy keyed on (route, identity)|M2|M3 reset endpoints|
|Lockout counter|Redis registry|`loginfail:{email}` keys with sliding TTL|M2|M3 reset flow interaction|
|AuditLogger callback chain|Callback wiring|Handlers→`AuditLogger.record(event,ctx)`|M2|M3 reset audit, M5 SOC2 pack|
|APM middleware|Middleware chain|Wraps auth handlers with trace spans|M2|M5 observability|

### Milestone Dependencies — M2

- Depends on all M1 primitives (`PasswordHasher`, `JwtService`, `TokenManager`, `AuditLogger`, gateway, schemas).
- OQ-PRD-003 (lockout threshold) must be resolved before COMP-LOGIN-ATTEMPT-TRACKER is implemented.

### Risk Assessment and Mitigation — M2

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-001: Token theft via XSS|High|Medium|Session hijack; user impersonation|In-memory AT storage; HttpOnly+Secure cookie for RT; 15-min AT TTL; CSP headers; `TokenManager.revokeAll` on suspicion|security-lead|
|2|R-002: Brute-force on login|Medium|High|Account takeover; reputational harm|Gateway rate-limit 10rpm/IP; lockout after 5 failures/15min; bcrypt cost=12; WAF IP block + CAPTCHA after 3 failures as contingency|auth-team|
|3|User enumeration via timing on login or register|Medium|Medium|Reconnaissance enabling targeted brute force|`COMP-ANTIENUM` constant-time path; identical error strings; p95 delta test gate in CI|security-lead|
|4|Refresh-token reuse (replay)|High|Low|Stale RT reaccepted after rotation|Single-use RT; reuse-detection revokes all user tokens; log + alert `token.refresh.reuse_detected`|auth-team|
|5|R-PRD-002 implementation flaws surface in prod|Critical|Low|Breach; SOC2 finding|Security review + pentest gate before MIG-002; threat model signoff end of M2|security-lead|

### Open Questions — M2

|#|ID|Question|Impact|Owner|Target|
|---|---|---|---|---|---|
|1|OQ-PRD-003|Account lockout policy after N consecutive failed login attempts (TDD=5/15min; Security may refine)|Locks in `COMP-LOGIN-ATTEMPT-TRACKER` threshold and UX messaging|Security|Before Week 3 start|
|2|OQ-002|Maximum allowed `UserProfile.roles` array length|Affects DM-001 validator and JWT claim size budget; pending RBAC design review|auth-team|2026-04-01|
|3|OQ-PRD-002|Maximum refresh tokens per user across devices (Sam persona JTBD lacks concrete FR); PRD requires; TDD should be updated|Determines Redis keyspace sizing and rotation semantics for multi-device|Product|Before Week 5|

## M3: Password Reset, Compliance & Admin Audit

**Objective:** Deliver the two-step password reset flow, complete SOC2 audit-log coverage, and close the admin JTBD gap by exposing an admin-scoped audit-log query API. | **Duration:** 2 weeks (Weeks 6–7) | **Entry:** M2 exit criteria met; SendGrid account + SPF/DKIM live. | **Exit:** FR-AUTH-005 pass; reset-completion funnel measurable; `auth_audit_log` satisfies SOC2 field requirements; admin audit API queryable by date/user.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-AUTH-005|Password reset flow (request + confirm)|`AuthService.requestReset(email)` and `AuthService.confirmReset(token,newPassword)` implementing two-step reset with token email.|Backend|COMP-007, COMP-008, DM-004, COMP-013|Request→email sent with 1h TTL token; confirm→password updated via `PasswordHasher`; used tokens cannot be reused; new password invalidates all existing sessions (PRD FR-AUTH.5)|M|P0|
|2|API-005|POST /v1/auth/reset-request endpoint|Handler that accepts `{email}` and returns 200 regardless of registration to prevent enumeration; side-effect emails reset token.|Backend|FR-AUTH-005, COMP-013, COMP-ANTIENUM|Route mounted; rate-limit 3rpm/IP; 200 constant response; token persisted hashed in DM-004; email enqueued to SendGrid; audit event `password.reset_requested`|S|P0|
|3|API-006|POST /v1/auth/reset-confirm endpoint|Handler that accepts `{token,newPassword}`, validates + updates password, revokes all user tokens.|Backend|FR-AUTH-005, COMP-010, COMP-008|Route mounted; 400 expired/used/invalid token; 400 weak password; 200 on success; `TokenManager.revokeAll(userId)` invoked; audit event `password.reset_completed`|S|P0|
|4|EMAIL-TEMPLATE-RESET|SendGrid reset-request email template|Localized template with 1-hour TTL link; clear CTA; security footer.|Documentation|COMP-013|Template ID referenced in SendGrid registry; renders token URL with HTTPS; under 60s delivery target; alt-text and text fallback included|S|P1|
|5|COMP-SESSION-INVALIDATOR|Session-wide revocation on password change|Method on `TokenManager` that deletes all `rt:{userId}:*` keys and records audit event.|Backend|COMP-010, COMP-011|All user refresh tokens purged; audit `session.invalidated_all` written; integration test confirms subsequent refresh returns 401|S|P0|
|6|TEST-006|E2E: register → login → profile happy path|Playwright flow exercising RegisterPage → LoginPage → ProfilePage through `AuthProvider`.|Testing|FR-AUTH-001, FR-AUTH-002|Playwright scenario passes in CI; Validates FR-AUTH-001 + FR-AUTH-002 + `AuthProvider`; artifact uploaded|M|P1|
|7|NFR-COMPLIANCE-002|SOC2 audit log completeness|Validate every auth event produces log row with user_id, timestamp, ip, outcome; retention honors resolved OQ-PRD-AUDIT-RETENTION.|Compliance|COMP-011, COMP-AUDIT-HOOKS, DM-003|SOC2 control matrix mapped; QA checklist green; retention job verified; 12-month retention applied (PRD); test asserts required fields on every event|M|P0|
|8|COMP-ADMIN-AUDIT-API|Admin audit query API (gap fill)|Admin-scoped read API `/v1/admin/audit?user=&from=&to=` — fills PRD admin JTBD gap not covered by TDD.|Backend|DM-003, COMP-011|Requires admin role claim; filters by user, date range, event type; paginated (limit 100); returns audit log rows; audit event `admin.audit.queried` written; PRD requires; TDD should be updated|M|P0|
|9|ADMIN-AUTHZ-MIDDLEWARE|Admin role guard middleware|Middleware that verifies `roles` JWT claim contains `admin` before allowing `/v1/admin/*`.|Security|COMP-009, COMP-ADMIN-AUDIT-API|Non-admin→403; admin→next; audit event `admin.access.denied` on 403; unit + integration tests|S|P0|
|10|RESET-CLEANUP-JOB|Expired reset-token cleanup job|Scheduled job deleting rows where used_at OR expires_at<now()-7d from DM-004.|Backend|DM-004|Cron runs hourly; metric `reset_tokens_purged_total` emitted; test confirms rows removed|S|P2|
|11|RESET-FUNNEL-METRICS|Prometheus metrics for reset funnel|Counters for `password_reset_requested_total`, `password_reset_completed_total` to compute PRD completion rate ≥80%.|Performance|API-005, API-006|Metrics emitted; Grafana panel shows completion rate; target >80%|S|P1|
|12|PRD-LOGIN-FAILURE-METRICS|Failed-login-rate metric|Counter `auth_login_failure_total` and ratio panel enabling <5% failed-login PRD KPI.|Performance|COMP-AUDIT-HOOKS|Metric emitted; Grafana ratio `failures/(successes+failures)` panel; alert if >20% over 5 min (OPS-009)|S|P1|
|13|PRD-SESSION-DURATION|Session-duration analytics|Track refresh events to compute avg session duration >30 min.|Performance|FR-AUTH-003|Metric `auth_session_duration_seconds` histogram; analytics dashboard; target avg >30 min|S|P2|
|14|PRIVACY-DPIA-SIGNOFF|GDPR DPIA sign-off for reset flow|Complete Data Protection Impact Assessment memo for reset flow and email processor (SendGrid).|Compliance|NFR-COMPLIANCE-004|DPIA memo filed; SendGrid data-processing agreement stored; sign-off recorded|S|P0|

### Integration Points — M3

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|Admin role guard|Middleware chain|`/v1/admin/*`→`ADMIN-AUTHZ-MIDDLEWARE`→handler|M3|M5 operational tooling|
|Reset-token store|DI injection|`AuthService`→DM-004 repository|M3|OPS runbooks|
|Session invalidator hook|Event binding|`auth.password.changed`→`COMP-SESSION-INVALIDATOR`|M3|Security incident response|
|SendGrid template registry|Registry|`reset_request`→template_id; future events extend|M3|Future email workflows|
|Audit-query result formatter|Strategy|JSON vs CSV export selector|M3|Jordan admin persona tooling|

### Milestone Dependencies — M3

- Depends on M2 for `AuthService`, `TokenManager`, `AuditLogger`, handler scaffolding, and APM.
- SendGrid credentials + sender-domain verification must be complete by Week 6 start.

### Risk Assessment and Mitigation — M3

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-PRD-004: Email delivery failures block reset|Medium|Low|Users locked out; support escalation|SendGrid delivery monitoring; DLQ + retry; fallback support channel; alert on delivery failure rate >1%|devops|
|2|R-PRD-003: Incomplete audit logging causes SOC2 failure|High|Medium|Compliance audit finding|QA checklist against SOC2 controls; required-fields test in CI; DPIA filed|compliance-lead|
|3|Reset token enumeration via timing or response divergence|Medium|Low|Leak of which emails are registered|Constant-time response via `COMP-ANTIENUM`; 200 returned regardless; tokens hashed at rest|security-lead|
|4|Admin audit API leaks PII beyond need|Medium|Low|GDPR violation|Admin-role gate; field-level redaction; access-audited|compliance-lead|

### Open Questions — M3

|#|ID|Question|Impact|Owner|Target|
|---|---|---|---|---|---|
|1|OQ-PRD-001|Should password reset emails be sent synchronously or asynchronously?|Drives `API-005` threading model and user-visible latency|Engineering|Before Week 6|
|2|OQ-PRD-004|Should "remember me" be supported to extend session duration?|Affects `TokenManager` TTL policy and FR-AUTH-003 scope|Product|Deferred to v1.1 (non-blocking)|

## M4: Frontend Integration & End-to-End Flows

**Objective:** Deliver the three user-facing routes and the `AuthProvider` context with silent refresh, protected routing, and validated end-to-end journeys aligned with the Alex persona's <60-second registration target. | **Duration:** 2 weeks (Weeks 8–9) | **Entry:** M2 auth APIs stable in staging; CORS + HTTPS configured. | **Exit:** All frontend components render under auth; silent refresh works without user interaction; E2E Playwright passes; accessibility and PRD UX criteria met.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|COMP-001|/login route → LoginPage|Public page hosting email/password form, calling API-001; stores `AuthToken` via `AuthProvider`.|Frontend|API-001, COMP-004|Route `/login`; props `onSuccess:()=>void, redirectUrl?:string`; generic error on 401; lockout banner on 423; rate-limit banner on 429; submit disabled during request|M|P0|
|2|COMP-002|/register route → RegisterPage|Public page with email/password/displayName form; client-side password strength validation; GDPR consent checkbox.|Frontend|API-002, COMP-004, NFR-COMPLIANCE-001|Route `/register`; props `onSuccess:()=>void, termsUrl:string`; min 8 chars, 1 upper, 1 digit validated client-side; 409 surfaces inline; consent checkbox required; registration completes <60s median (Alex persona)|M|P0|
|3|COMP-003|/profile route → ProfilePage|Protected page showing `UserProfile` from API-003.|Frontend|API-003, COMP-006|Route `/profile`; renders displayName, email, createdAt; redirects to /login if unauthenticated; last-login visible|S|P1|
|4|COMP-004|AuthProvider context|React context managing `AuthToken` state, 401 interception, silent refresh, and `UserProfile` exposure.|Frontend|API-004, FR-AUTH-003|Wraps `App`; props `children:ReactNode`; `useAuth()` exposes `{user,login,logout,isAuthenticated}`; silent refresh triggered before AT expiry; 401 on AT triggers rotate then retry original request once; redirect to /login on refresh failure|L|P0|
|5|COMP-005|PublicRoutes group|Route group for unauthenticated routes (LoginPage, RegisterPage).|Frontend|COMP-001, COMP-002|Children render without auth; authenticated users redirected to /profile when visiting /login or /register|S|P1|
|6|COMP-006|ProtectedRoutes group|Route group enforcing authentication via `AuthProvider` redirect.|Frontend|COMP-004, COMP-003|Unauthenticated visits redirect to /login with `redirectUrl` preserved; loading state shown while `AuthProvider` checks session|S|P0|
|7|FE-TOKEN-STORAGE|In-memory access-token storage + HttpOnly cookie refresh|Client-side strategy per R-001 mitigation: AT never in localStorage; RT in HttpOnly+Secure+SameSite=strict cookie.|Frontend|COMP-004|AT held in JS memory within `AuthProvider`; RT never accessible to JS; page reload triggers silent refresh from RT cookie; CSP header forbids inline scripts|M|P0|
|8|FE-ERROR-BOUNDARY|Auth error boundary|React error boundary catching auth exceptions and surfacing generic UX.|Frontend|COMP-004|Unhandled errors render fallback UI; telemetry emitted; no secrets leaked to screen|S|P1|
|9|FE-A11Y-AUDIT|Accessibility audit of auth pages|Axe-core audit on LoginPage, RegisterPage, ProfilePage.|Frontend|COMP-001, COMP-002, COMP-003|Zero critical violations; keyboard nav works; ARIA labels present; color-contrast passes WCAG AA|S|P1|
|10|FE-LOCALIZATION-KEYS|i18n keys for auth UX|Extract all user-facing strings to i18n catalog for future localization.|Frontend|COMP-001, COMP-002, COMP-003|Catalog produced; en-US baseline in place; lint forbids raw strings in auth components|S|P2|
|11|FE-REMEMBER-REDIRECT|Post-login redirect preservation|`redirectUrl` query param honored on /login success.|Frontend|COMP-001, COMP-004|Deep-link visit→redirected to /login?redirectUrl=X→after login navigates to X; XSS-safe URL validation (same-origin only)|S|P1|
|12|E2E-FORGOT-PASSWORD|E2E: forgot password happy path|Playwright scenario covering /login → reset-request → email capture → reset-confirm.|Testing|FR-AUTH-005, COMP-001|Scenario passes in CI using SendGrid sandbox/webhook; includes session-invalidation check post-reset|M|P1|
|13|TEST-PROVIDER-INTEGRATION|Integration: AuthProvider silent refresh|Vitest + MSW test forcing AT expiry and asserting silent refresh + request retry.|Testing|COMP-004|401 handler rotates tokens once; retries original request; second 401 triggers logout; no infinite loop|M|P0|

### Integration Points — M4

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|Axios/fetch interceptor|Middleware chain|401→rotate→retry; logout on second 401|M4|All authenticated page requests|
|React context|Dependency injection|`AuthProvider` exposed via `useAuth` hook|M4|All downstream UI components|
|Route guard|Strategy pattern|`ProtectedRoutes` vs `PublicRoutes`|M4|Future protected pages|
|CSP + HttpOnly cookie policy|Config registry|Strict CSP; RT cookie flags|M4|All browser sessions|

### Milestone Dependencies — M4

- Depends on M2 APIs being stable.
- CORS allow-list (M1) must include production frontend origin before GA.
- Can run in parallel with M3 where frontend does not consume reset-specific endpoints.

### Risk Assessment and Mitigation — M4

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Silent-refresh loop on persistent 401|High|Medium|Browser-pinned CPU; support escalation|Single-retry guard in interceptor; exponential backoff on successive failures; circuit breaker pattern|frontend|
|2|R-PRD-001: Low registration adoption due to UX friction|High|Medium|Missed 60% conversion KPI|Usability tests with Alex persona; funnel instrumentation; iterate quickly post-launch|product-manager, frontend|
|3|Token leakage via localStorage misuse by future devs|High|Low|R-001 realized|Lint rule forbidding `localStorage.setItem('*token*')`; CI gate; documentation in `/docs/auth-frontend.md`|security-lead|
|4|Accessibility regressions breaking Alex persona inclusivity|Medium|Medium|User exclusion; potential legal risk|Axe-core CI gate; manual keyboard + screen-reader testing|frontend|

### Open Questions — M4

|#|ID|Question|Impact|Owner|Target|
|---|---|---|---|---|---|
|1|OQ-FE-STORAGE|Confirm HttpOnly+Secure+SameSite=strict cookie works with all supported deployment topologies (subdomains, CDN). If not, fallback storage strategy required.|Determines `FE-TOKEN-STORAGE` final form|security-lead, frontend|Before Week 8 start|

## M5: Migration, Observability & GA Rollout

**Objective:** Execute the 3-phase staged rollout (Alpha → 10% Beta → GA) with full observability stack, runbooks, capacity plans, rollback procedures, and final compliance sign-off. | **Duration:** 3 weeks (Weeks 10–12) | **Entry:** M3 + M4 exit criteria met; security review + pentest complete; feature flags `AUTH_NEW_LOGIN` and `AUTH_TOKEN_REFRESH` deployed OFF. | **Exit:** 99.9% uptime over 7-day GA window; all dashboards green; legacy endpoints deprecated; `AUTH_NEW_LOGIN` flag removed; OPS-001..010 in force.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|MIG-001|Phase 1: Internal Alpha|Deploy `AuthService` to staging; auth-team + QA exercise all endpoints; `LoginPage`/`RegisterPage` behind `AUTH_NEW_LOGIN=ON` for internal tenants only.|Devops|M3, M4, MIG-004|Duration 1 week; FR-AUTH-001..005 regression pass; zero P0/P1 bugs; APM dashboards green; exit gate signed by auth-team + QA|M|P0|
|2|MIG-002|Phase 2: Beta (10% traffic)|Enable `AUTH_NEW_LOGIN` at 10% via gateway weighted routing; monitor latency, error rate, Redis; validate silent refresh under load.|Devops|MIG-001, MIG-005|Duration 2 weeks; p95 <200ms; error rate <0.1%; no Redis failures; `AuthProvider` refresh validated at volume; k6 run archived|L|P0|
|3|MIG-003|Phase 3: GA (100%)|Remove `AUTH_NEW_LOGIN` flag; route 100%; deprecate legacy; enable `AUTH_TOKEN_REFRESH`.|Devops|MIG-002|Duration 1 week; 99.9% uptime over 7 days; all dashboards green; legacy endpoints return 410; documentation updated|M|P0|
|4|MIG-004|Feature flag AUTH_NEW_LOGIN|Gate new login path; default OFF; remove after MIG-003.|Devops|COMP-012|Flag registered; default OFF; dispatch switches between new and legacy login endpoints; removal ticket filed at GA|S|P0|
|5|MIG-005|Feature flag AUTH_TOKEN_REFRESH|Gate refresh-token flow; default OFF; when OFF only access tokens issued; cleanup MIG-003 + 2 weeks.|Devops|COMP-010|Flag registered; default OFF; `TokenManager` reads flag; cleanup ticket filed|S|P0|
|6|MIG-006|Rollback procedure|Documented ordered rollback steps: disable flag → smoke legacy → investigate → restore if corruption → notify → post-mortem.|Documentation|MIG-001..MIG-005|Runbook at `/runbooks/auth-rollback.md`; dry-run performed end of MIG-001; steps numbered; RACI clear|M|P0|
|7|MIG-007|Rollback criteria|Quantitative triggers: p95 >1000ms >5min; error >5% >2min; Redis failures >10/min; any `UserProfile` data corruption.|Devops|OPS-009|Thresholds encoded in Grafana alert rules; auto-notify auth-team + platform-team on-call; triggers linked to MIG-006 steps|S|P0|
|8|OPS-001|Runbook: AuthService down|Symptoms/diagnosis/resolution/escalation flow for full-service outage.|Documentation|COMP-007|Runbook at `/runbooks/auth-service-down.md`; covers pod restart, PG failover, Redis degraded, legacy fallback; escalation auth-team→platform-team (15 min)|S|P0|
|9|OPS-002|Runbook: Token refresh failures|Symptoms/diagnosis/resolution for refresh outages causing unexpected logouts.|Documentation|COMP-010|Runbook at `/runbooks/auth-refresh-failures.md`; covers Redis conn, JWT key mount, flag state; links to key-rotation runbook|S|P0|
|10|OPS-003|On-call expectations documented|P1 ack 15 min; auth-team 24/7 for first 2 weeks post-GA; tooling and escalation chain.|Documentation|MIG-003|Doc at `/runbooks/auth-oncall.md`; rotation scheduled in PagerDuty; tool access verified; knowledge prereqs listed|S|P1|
|11|OPS-004|Capacity: AuthService pods + HPA|3 replicas baseline; HPA to 10 replicas at CPU >70%.|Devops|MIG-002|HPA manifest applied; load test confirms scale at 500 concurrent; CPU reserve headroom verified|S|P0|
|12|OPS-005|Capacity: PostgreSQL connections|Pool 100 baseline; grow to 200 if wait >50ms.|Devops|INFRA-DB-001|pgbouncer config tuned; monitor panel shows wait time; runbook includes growth trigger|S|P1|
|13|OPS-006|Capacity: Redis memory|1 GB baseline; alert at 70% utilization; grow to 2 GB.|Devops|INFRA-DB-001|Alert rule; used_memory panel; runbook step to resize cluster; eviction policy confirmed `allkeys-lru`|S|P1|
|14|OPS-007|Structured logging configured|Auth events with user_id, IP, timestamp, outcome; retention 12 months (PRD wins).|Devops|COMP-011|Log schema documented; retention policy applied in log store; sensitive fields scrubbed; SOC2 sign-off attached|M|P0|
|15|OPS-008|Prometheus metrics published|`auth_login_total`, `auth_login_duration_seconds`, `auth_token_refresh_total`, `auth_registration_total` + FR-AUTH-005 counters.|Devops|API-001..API-006|Metrics emitted on `/metrics`; Grafana auth dashboard published; SLO panels for NFR-PERF-001/NFR-REL-001|M|P0|
|16|OPS-009|Alerts for auth SLOs and rollback gates|Alert rules: login failure rate >20% / 5min; p95 >500ms; Redis conn failures; rollback gates (MIG-007).|Devops|OPS-008, MIG-007|Alert rules applied; routed to PagerDuty; tested via synthetic failure; severity mapped; NFR-REL-001 SLO alarms live|M|P0|
|17|OPS-010|OpenTelemetry tracing end-to-end|Distributed tracing across `AuthService`→`PasswordHasher`→`TokenManager`→`JwtService`; sampling strategy resolved.|Devops|COMP-007|OTel SDK wired; spans named consistently; sampling policy defined (candidate: 10% plus always-sample on error); traces visible in backend|M|P1|
|18|NFR-REL-001|99.9% availability SLO validation|Validate availability via synthetic health checks over 30-day rolling windows.|Performance|OPS-008, OPS-009|Health probe runs every 60s; uptime dashboard shows 99.9% target; error budget burn alerts configured|S|P0|

### Integration Points — M5

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|Feature-flag dispatch|Dispatch table|`AUTH_NEW_LOGIN`, `AUTH_TOKEN_REFRESH` keys read by router and `TokenManager`|M5|Rollout phases|
|Alert routing|Dispatch/registry|Severity→PagerDuty policy map|M5|On-call rotations|
|OTel exporter|Middleware chain|Service→Collector→Backend|M5|Performance debugging|
|Grafana dashboard registry|Registry|`auth-overview`, `auth-slos`, `auth-audit`|M5|Jordan admin persona, auth-team|
|Log-retention policy|Config registry|12-month retention applied per-index|M5|SOC2 audit|

### Milestone Dependencies — M5

- Depends on M3 (compliance + reset) and M4 (frontend) complete; cannot start MIG-001 until both green.
- OPS-010 tracing sampling strategy must be decided before MIG-002 beta to avoid cost spike at 10% traffic.

### Risk Assessment and Mitigation — M5

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-003: Data loss during migration|High|Low|User lockout; trust damage|Parallel run with legacy; idempotent upserts; pre-phase PG backups; MIG-006 rollback restore step|devops, auth-team|
|2|Feature-flag drift between services causing split-brain auth|High|Low|Users served inconsistent auth|Centralized flag source; flag-check middleware; health probe asserts flag visibility|devops|
|3|Tracing sampling too aggressive at 10% beta spikes cost|Medium|Medium|Budget overrun|Start with head-based 10% sample + tail sampling on errors; cost alarms; downshift if budget exceeded|devops|
|4|Post-GA alert fatigue masking real incidents|Medium|Medium|Missed SLO breach|Alert thresholds reviewed weekly first month; silence→tune workflow|auth-team|

### Open Questions — M5

|#|ID|Question|Impact|Owner|Target|
|---|---|---|---|---|---|
|1|OQ-OPS-010-SAMPLING|OpenTelemetry sampling strategy unspecified in TDD (OPS-010). Decide between head-based, tail-based, or hybrid sampling before MIG-002 beta.|Affects observability cost and debug depth at 10% traffic|devops, observability-lead|Before MIG-002 start (Week 11)|

## Resource Requirements and Dependencies

### External Dependencies

|Dependency|Required By Milestone|Status|Fallback|
|---|---|---|---|
|PostgreSQL 15+ (INFRA-DB-001)|M1|Provisioning in progress|Self-hosted PG 15 on existing k8s cluster (adds 1 week)|
|Redis 7+|M1|Provisioning in progress|Self-hosted Redis 7 sentinel (adds 1 week)|
|Node.js 20 LTS runtime|M1|Available|Pin Node 18 LTS with documented technical debt|
|`bcryptjs` npm library|M1|Available on npm|`argon2` with updated cost-factor policy (pending SEC-POLICY-001 re-approval)|
|`jsonwebtoken` npm library|M1|Available on npm|`jose` library as drop-in|
|SendGrid API|M3|Account provisioning pending|AWS SES or Mailgun fallback (contract required)|
|AUTH-PRD-001|M1..M5|Signed-off|N/A — roadmap aborts|
|SEC-POLICY-001|M1|Pending legal/security sign-off|N/A — blocks M1 exit|
|INFRA-DB-001 ticket|M1|Scheduled|Use shared staging cluster; re-provision pre-GA|
|Frontend routing framework (React Router)|M4|Available|Existing project already uses framework|
|k8s + API Gateway|M1|Available|Existing platform|
|PagerDuty|M5|Available|OpsGenie fallback|

### Infrastructure Requirements

- PostgreSQL 15 primary + 1 replica; pgbouncer connection pooler (pool 100; grows to 200).
- Redis 7 cluster with persistence (AOF); 1 GB baseline, scale to 2 GB; TLS enforced.
- k8s namespace for `AuthService`; HPA on CPU >70% (3→10 replicas); PodDisruptionBudget min=2.
- API Gateway rate-limit policies per endpoint; TLS 1.3 termination; CORS allow-list env.
- Secrets management (k8s secret or equivalent) for RS256 keys, SendGrid token, DB credentials.
- Observability stack: Prometheus + Grafana + Loki + OTel Collector; PagerDuty integration.
- Backup: daily full + hourly WAL for PostgreSQL; 30-day retention.
- CI/CD: GitHub Actions (or current system) with UV, Jest, Playwright, k6 runners.

## Risk Register

|ID|Risk|Affected Milestones|Probability|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|R-001|Token theft via XSS|M2, M4|Medium|High|In-memory AT + HttpOnly RT cookie; CSP headers; 15-min AT; `revokeAll` on suspicion; CI lint against localStorage token|security-lead|
|R-002|Brute-force on login|M1, M2|High|Medium|Gateway 10rpm/IP; lockout 5/15min; bcrypt cost=12; WAF + CAPTCHA contingency|auth-team|
|R-003|Data loss during migration|M5|Low|High|Parallel-run with legacy; idempotent upserts; pre-phase backups; MIG-006 rollback+restore|devops|
|R-PRD-001|Low registration adoption from poor UX|M4, M5|Medium|High|Usability testing with Alex persona; funnel data; iterate post-launch|product-manager|
|R-PRD-002|Security breach from implementation flaws|M2, M5|Low|Critical|Security review + pentest before MIG-002; threat model sign-off end of M2|security-lead|
|R-PRD-003|Compliance failure from incomplete audit logging|M1, M3|Medium|High|SOC2 control mapping; required-fields test in CI; DPIA; retention 12m|compliance-lead|
|R-PRD-004|Email delivery failures blocking password reset|M3|Low|Medium|SendGrid delivery monitoring; DLQ + retry; fallback support channel|devops|
|R-AUDIT-RETENTION|Unresolved 90d vs 12m audit retention forces rework|M1, M3|Medium|Medium|Drive resolution Week 1; partition scheme supports both with config switch|compliance-lead|
|R-KEY-ROTATION|RS256 key rotation mass-logout|M1, M5|Low|High|kid overlap window N + N-1; dry-run in staging; documented runbook|security-lead|
|R-SILENT-REFRESH-LOOP|Silent-refresh loop on persistent 401|M4|Medium|High|Single-retry guard; backoff; circuit breaker|frontend|
|R-FLAG-DRIFT|Feature-flag drift causing split-brain auth|M5|Low|High|Centralized source; flag-check middleware; health-probe assertion|devops|

## Success Criteria and Validation Approach

|Criterion|Metric|Target|Validation Method|Milestone|
|---|---|---|---|---|
|Login latency|Login endpoint p95|<200ms|APM histogram on `/v1/auth/login` in staging and prod|M2, M5|
|Registration success|Registration success rate|>99%|`auth_registration_total{outcome=success}` / total|M2, M5|
|Token refresh latency|Refresh endpoint p95|<100ms|APM on `/v1/auth/refresh`|M2, M5|
|Service availability|30-day rolling uptime|99.9%|Synthetic health probes + Grafana SLO|M5|
|Password-hash performance|Bcrypt hash time|<500ms at cost 12|Unit perf test + staging benchmark|M1|
|Registration conversion|Funnel: landing→register→confirmed|>60%|Product analytics funnel (PRD KPI)|M4, M5|
|Daily active authenticated users|DAU (auth)|>1000 within 30d of GA|Analytics event stream|M5 (post-GA)|
|Unit test coverage|Coverage on AuthService/TokenManager/JwtService/PasswordHasher|>80%|Jest coverage report in CI|M2, M3|
|Concurrent capacity|500 concurrent p95|<200ms @ 500 VU|k6 load test|M2, M5|
|Avg session duration|Duration histogram avg|>30 min|OPS-008 metric panel (PRD KPI)|M5 (post-GA)|
|Failed login rate|Failures / attempts|<5%|OPS-008 panel (PRD KPI)|M5 (post-GA)|
|Password reset completion|Reset-completed / reset-requested|>80%|`RESET-FUNNEL-METRICS` panel (PRD KPI)|M5 (post-GA)|

## Decision Summary

|Decision|Chosen|Alternatives Considered|Rationale|
|---|---|---|---|
|Token model|Stateless JWT AT (RS256, 15-min) + opaque RT in Redis (7-day)|Opaque AT in DB; JWT AT with session table|TDD architectural mandate; enables horizontal scale; 15-min AT limits blast radius; Redis enables revocation (FR-AUTH-003, R-001)|
|Password hashing|bcrypt cost 12|Argon2id; scrypt; PBKDF2|NFR-SEC-001 mandate; bcryptjs available; cost 12 balances <500ms perf budget with NIST SP 800-63B adaptive requirement (NFR-COMPLIANCE-003)|
|Signing algorithm|RS256 with 2048-bit RSA|HS256 (symmetric); ES256|NFR-SEC-002 mandate; asymmetric enables key distribution; 2048-bit meets NIST baseline through 2030|
|Refresh-token storage|Redis with SHA-256 hash and TTL|PostgreSQL table; encrypted cookie only|Redis TTL matches 7-day lifetime; O(1) revocation; Redis 7 capacity plan 1 GB handles ~100K tokens with 90% headroom|
|Rollout strategy|3-phase staged (Alpha→10% Beta→GA) with 2 feature flags|Big-bang cutover; blue/green|Extraction mandate (MIG-001..003); lower risk given R-PRD-002 criticality; explicit rollback criteria (MIG-007)|
|Audit retention|12 months (PRD wins over TDD 90d)|90d TDD-only|PRD NFR-COMPLIANCE-002 mandates 12 months for SOC2 Type II; resolved via conflict rule "PRD wins on business intent"|
|Admin audit API|Introduce gap-fill endpoint (`COMP-ADMIN-AUDIT-API`)|Defer to admin PRD|PRD Jordan-persona JTBD "view auth event logs to investigate incidents" has no FR in TDD — gap must be filled to satisfy AUTH-E3 admin user story|
|Token frontend storage|AT in memory + RT in HttpOnly+Secure+SameSite cookie|AT in localStorage; both in cookies|R-001 mitigation; Alex persona silent-refresh requires durable RT; SameSite+HttpOnly removes JS access|
|Rate-limit strategy|Per-endpoint policies at API Gateway|Application-layer middleware; none|R-002 mitigation; gateway is the single ingress; WAF + CAPTCHA contingency layered|
|Observability sampling|Hybrid head-based (10%) + tail-based on errors|Always-sample; fixed 1%|OQ-OPS-010-SAMPLING resolution candidate; balances cost at 10% beta traffic with debug depth on failures|

## Timeline Estimates

|Milestone|Duration|Start|End|Key Milestones|
|---|---|---|---|---|
|M1|2 weeks|Week 1|Week 2|INFRA-DB-001 live; DM-001..004 migrations applied; `PasswordHasher` + `JwtService` unit-tested; audit-retention conflict resolved|
|M2|3 weeks|Week 3|Week 5|API-001..004 in staging; FR-AUTH-001..004 green; k6 500-VU p95 <200ms; pentest scheduled|
|M3|2 weeks|Week 6|Week 7|FR-AUTH-005 complete; admin audit API shipped; DPIA filed; SOC2 field checklist green|
|M4|2 weeks|Week 8|Week 9|COMP-001..006 live; silent refresh validated; axe-core zero critical; E2E passes|
|M5|3 weeks|Week 10|Week 12|MIG-001 alpha (W10); MIG-002 10% beta (W11); MIG-003 GA (W12); dashboards + runbooks live|

**Total estimated duration:** 12 weeks (Week 1 → Week 12).

