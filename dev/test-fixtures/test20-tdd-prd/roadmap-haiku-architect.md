---
spec_source: "test-tdd-user-auth.compressed.md"
complexity_score: 0.72
complexity_class: HIGH
primary_persona: architect
base_variant: "none"
variant_scores: "single-pass"
convergence_score: 1.0
generated: "2026-04-19"
generator: "gpt-5.4 incremental roadmap"
milestone_count: 5
total_deliverable_rows: 54
risk_count: 6
open_questions: 10
---
# User Authentication Service — Project Roadmap

## Executive Summary

The User Authentication Service roadmap delivers the platform’s foundational identity layer in 5 technical-layer milestones across 10 weeks. The plan sequences 50 deliverables from identity data contracts and cryptographic primitives through backend auth orchestration, versioned APIs, React integration, compliance validation, and phased production rollout. This sequencing matches the architecture’s hard dependencies: PostgreSQL and Redis plus RS256 key custody first, `AuthService` and `TokenManager` next, then API and UI integration, then cross-cutting validation, then migration and operations.

**Business Impact:** Unblocks the Q2-Q3 2026 personalization roadmap, supports the projected $2.4M annual revenue tied to authenticated experiences, reduces access-related support burden, and closes the SOC2 Type II audit gap around user-level accountability.

**Complexity:** HIGH (0.72) — driven by dual-store state management (PostgreSQL + Redis), security-critical token lifecycle design, frontend/backend coordination, phased migration, and overlapping compliance requirements (SOC2, GDPR, NIST).

**Critical path:** M1 identity data and crypto baseline -> M2 auth orchestration plus reset/logout workflows -> M3 API contracts and route/auth-state wiring -> M4 compliance, performance, and test validation -> M5 phased rollout and operational readiness.

**Key architectural decisions:**
- Use short-lived RS256 JWT access tokens with opaque Redis-backed refresh tokens instead of server-side sessions to preserve horizontal scalability and meet the stateless-service constraint.
- Keep the access token in memory and the refresh token in an HttpOnly cookie to mitigate R-001 token theft while still supporting silent refresh and cross-page continuity.
- Close PRD/TDD gaps explicitly in the roadmap by adding logout and audit-log query deliverables rather than assuming downstream teams will infer them.

**Open risks requiring resolution before M1:**
- Resolve the 90-day vs 12-month audit-log retention conflict before finalizing storage and compliance controls.
- Confirm the maximum `roles` array length for `UserProfile` before freezing the PostgreSQL schema.
- Confirm SendGrid delivery mode and operational ownership for password-reset traffic before locking the reset-flow architecture.

## Milestone Summary

|ID|Title|Type|Priority|Effort|Dependencies|Deliverables|Risk|
|---|---|---|---|---|---|---|---|
|M1|Identity Data and Security Foundation|FOUNDATION|P0|2w|—|10|High|
|M2|Auth Domain Services and Session Lifecycle|FEATURE|P0|2w|M1|10|High|
|M3|API Surface and Frontend Integration|FEATURE|P0|2w|M2|11|Medium|
|M4|Compliance, Validation, and Quality Gates|VALIDATION|P0|2w|M3|15|High|
|M5|Release Rollout and Operational Readiness|RELEASE|P0|2w|M4|8|High|

## Dependency Graph

M1 -> M2 -> M3 -> M4 -> M5
M1: DM-001, DM-002, COMP-007, COMP-008, base infra, gateway, observability bootstrap
M2: COMP-005, COMP-006, FR-AUTH-001..005, logout/session invalidation, reset token store
M3: API-001..007, COMP-001..004
M4: TEST-001..006, NFR-PERF-001, NFR-PERF-002, NFR-REL-001, NFR-SEC-001, NFR-SEC-002, compliance gap closure
M5: MIG-001..003, OPS-001..005

## M1: Identity Data and Security Foundation

**M1: Identity Data and Security Foundation** | Weeks 1-2 | exit criteria: persistence, cryptography, gateway baseline, and audit schema are ready for service implementation

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|DM-001|UserProfile persistence model|Implement the canonical user entity in PostgreSQL with normalization, timestamps, and downstream role linkage.|UserRepo|—|id:UUIDv4-PK-NOTNULL; email:unique-indexed-lowercase-NOTNULL; displayName:varchar(2-100)-NOTNULL; createdAt:timestamptz-default-now-NOTNULL; updatedAt:timestamptz-auto-updated-NOTNULL; lastLoginAt:timestamptz-nullable; roles:text[]-default-["user"]-NOTNULL|M|P0|
|2|DM-002|AuthToken contract and refresh record|Define the external token response contract and the internal Redis-backed refresh-token record semantics.|TokenManager|DM-001|accessToken:JWT-string-NOTNULL-15min-TTL; refreshToken:opaque-string-NOTNULL-7day-TTL-hashed-at-rest; expiresIn:int-900-NOTNULL; tokenType:string-"Bearer"-NOTNULL|S|P0|
|3|COMP-007|JwtService|Implement RS256 signing and verification with 2048-bit keys, skew tolerance, and rotation compatibility.|JwtService|DM-002|sign(payload,expiresIn,issuer,audience):RS256-only; verify(token,issuer,audience):RS256-only; keySize:2048bit-RSA; clockSkewTolerance:5s; keyRotation:quarterly-compatible|M|P0|
|4|COMP-008|PasswordHasher|Implement bcrypt hashing and verification behind an abstraction suitable for future migration.|PasswordHasher|—|hash(plain):bcrypt-cost12; verify(plain,hash):boolean; algorithm:bcrypt; costFactor:12; rawPassword:not-persisted; rawPassword:not-logged|S|P0|
|5|COMP-012|AuditLog entity|Define the audit-log storage model needed for compliance, queryability, and retention controls.|AuditLogStore|DM-001|id:UUID-PK; userId:UUID-nullable-indexed; eventType:string-indexed; timestamp:timestamptz-indexed; ip:string-NOTNULL; outcome:string-NOTNULL; metadata:jsonb-optional; retentionPolicy:12months-configurable|M|P0|
|6|INF-001|PostgreSQL 15 baseline|Provision and validate PostgreSQL 15+ with pooling for user and audit data.|PostgreSQL|DM-001, COMP-012|version:15+; pooling:pg-pool-enabled; backups:enabled; connectivity:from-auth-pods; migrations:automated|M|P0|
|7|INF-002|Redis 7 token store baseline|Provision and validate Redis 7+ for refresh-token storage, revocation, and TTL workflows.|Redis|DM-002|version:7+; TTL-support:enabled; persistence:configured; connectivity:from-auth-pods; eviction-policy:compatible-with-token-store|M|P0|
|8|INF-003|API Gateway auth edge baseline|Configure gateway pathing, TLS, and CORS prerequisites for `/v1/auth/*`.|API Gateway|—|routePrefix:/v1/auth/*; TLS:1.3-enforced; CORS:known-origins-only; rateLimitHooks:available; authHeaders:forwarded-correctly|M|P0|
|9|INF-004|SendGrid delivery baseline|Provision password-reset email delivery integration and secret distribution path.|SendGrid|—|provider:SendGrid; auth:API-or-SMTP-configured; secrets:mounted-securely; deliveryHealth:observable; senderIdentity:verified|S|P0|
|10|INF-005|Observability bootstrap|Create the base metrics, traces, and structured logging channels required by later milestones.|Observability|INF-001, INF-002, INF-003|metrics:Prometheus-scrape-enabled; tracing:OpenTelemetry-enabled; logs:structured; sensitiveFields:passwords-and-tokens-excluded; dashboards:bootstrap-created|M|P0|

### Integration Points — M1

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|RS256 key registry|registry|COMP-007 secret mount + verifier config|M1|COMP-006, API auth middleware|
|Password hasher abstraction|strategy|COMP-008 interface bound in service container|M1|COMP-005, FR-AUTH-001, FR-AUTH-002, FR-AUTH-005|
|Gateway auth route map|dispatch table|INF-003 `/v1/auth/*` mapping|M1|API-001, API-002, API-003, API-004, API-005, API-006, API-007|
|Audit event sink|callback wiring|COMP-012 structured event writer|M1|FR-AUTH-001, FR-AUTH-002, FR-AUTH-003, FR-AUTH-004, FR-AUTH-005, OPS-005|

### Milestone Dependencies — M1

- External dependencies: PostgreSQL 15+, Redis 7+, Node.js 20 LTS, SendGrid, API Gateway, SEC-POLICY-001.
- Architectural dependencies: PRD retention requirement must supersede the conflicting 90-day TDD statement before storage policy is frozen.

### Open Questions — M1

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-002|What is the maximum allowed `UserProfile` roles array length?|Blocks final `DM-001` schema bounds and validation behavior.|auth-team|2026-04-01|
|2|OQ-PRD-002|What is the maximum number of refresh tokens allowed per user across devices?|Affects Redis sizing, revocation policy, and multi-device semantics in `DM-002` and `COMP-006`.|Product|2026-04-24|
|3|OQ-COMP-001|Which retention value is authoritative for audit logs: 90 days in TDD or 12 months in PRD/NFR-COMPLIANCE-001?|Blocks final `COMP-012` storage policy and compliance sign-off.|Compliance|2026-04-22|

### Risk Assessment and Mitigation — M1

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Schema rework from unresolved role cardinality and retention conflicts|High|Medium|Schedule slip and migration churn|Resolve OQs before migration freeze; treat PRD compliance requirements as gating constraints.|architect|
|2|Weak crypto/key custody setup undermines token integrity|High|Low|System-wide auth compromise|Use RS256 2048-bit keys, restricted secret mounts, and quarterly rotation from day one.|security|

## M2: Auth Domain Services and Session Lifecycle

**M2: Auth Domain Services and Session Lifecycle** | Weeks 3-4 | exit criteria: all core auth behaviors, reset flows, logout, and audit emission are implemented behind stable services

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|COMP-005|AuthService|Implement the orchestration service that owns registration, login, profile lookup, reset flows, and logout/session invalidation.|AuthService|COMP-007, COMP-008, DM-001, DM-002, COMP-012|login(email,password):delegates-to-PasswordHasher-and-TokenManager; register(email,password,displayName,consent):creates-user-and-profile; me(userId):returns-UserProfile; resetRequest(email):generic-response-no-enumeration; resetConfirm(token,newPassword):updates-hash-invalidates-sessions; logout(session):revokes-refresh-token|L|P0|
|2|COMP-006|TokenManager|Implement token issuance, refresh, revocation, cookie coordination, and session invalidation semantics.|TokenManager|COMP-007, DM-002, INF-002|issue(userId,roles):returns-AuthToken; refresh(refreshToken):rotates-token-pair; revoke(refreshToken):marks-unusable; invalidateAll(userId):used-after-password-reset; cookieMode:HttpOnly-refresh-token-supported|L|P0|
|3|FR-AUTH-001|Login flow|Implement secure email/password authentication with brute-force protections and non-enumerating errors.|AuthService|COMP-005, COMP-006, COMP-008|validCredentials:200-AuthToken; invalidCredentials:401-generic-error; nonExistentEmail:401-generic-error; failedAttempts:5-in-15min-lockout|M|P0|
|4|FR-AUTH-002|Registration flow|Implement account creation with uniqueness, password strength checks, consent capture, and profile creation.|AuthService|COMP-005, COMP-008, DM-001|validRegistration:201-UserProfile; duplicateEmail:409; weakPassword(<8,noUppercase,noNumber):400; passwordHash:bcrypt-cost12; consent:recorded-with-timestamp|M|P0|
|5|FR-AUTH-003|Token issuance and refresh|Implement short-lived access tokens plus refresh rotation and revocation logic.|TokenManager|COMP-006|loginReturns:accessToken+refreshToken; accessTTL:15min; refreshTTL:7days; refreshEndpoint:valid-token-returns-new-pair; expiredRefresh:401; revokedRefresh:401|M|P0|
|6|FR-AUTH-004|Profile retrieval behavior|Implement authenticated profile retrieval with full contract coverage.|AuthService|COMP-005, DM-001|validAccessToken:returns-UserProfile; invalidOrExpiredToken:401; fields:id,email,displayName,createdAt,updatedAt,lastLoginAt,roles|S|P0|
|7|FR-AUTH-005|Password reset flow|Implement reset request and confirmation including token expiry and single-use guarantees.|AuthService|COMP-005, INF-004|resetRequest:email-sent-for-valid-address; resetConfirm:valid-token-updates-password; resetTokenTTL:1hour; usedResetToken:rejected-on-reuse|M|P0|
|8|COMP-013|ResetTokenManager|Implement generation, persistence, hashing, and one-time consumption of password-reset tokens.|ResetTokenManager|INF-002, INF-004|tokenFormat:opaque-random; storage:hashed-at-rest; TTL:1hour; consume(token):single-use; resendFlow:supported|M|P0|
|9|API-007|Logout endpoint behavior|Add the missing logout capability implied by the PRD so users can end sessions on shared devices.|AuthService, TokenManager|COMP-005, COMP-006|endpoint:POST-/auth/logout; authenticatedCall:204-or-200; refreshToken:revoked; subsequentRefresh:401; redirectHint:frontend-supported|S|P0|
|10|COMP-014|Auth audit emission|Emit structured auth events for login, registration, refresh, reset, logout, and failures.|AuthService, TokenManager|COMP-012, INF-005|events:login,login_failed,register,refresh,logout,reset_request,reset_confirm; fields:userId,timestamp,ip,outcome; retention:12months-target; sensitiveData:excluded|M|P0|

### Integration Points — M2

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|AuthService method registry|dispatch table|COMP-005 maps login/register/me/reset/logout handlers|M2|API-001, API-002, API-003, API-005, API-006, API-007|
|Token lifecycle callbacks|callback wiring|COMP-006 issues refresh rotation + invalidation callbacks|M2|FR-AUTH-003, FR-AUTH-005, API-004, API-007|
|Reset token pipeline|middleware chain|COMP-013 validate -> consume -> update hash|M2|FR-AUTH-005, API-006|
|Audit event publisher|event binding|COMP-014 bound to AuthService and TokenManager outcomes|M2|NFR-COMPLIANCE-001, OPS-005, admin log access|

### Milestone Dependencies — M2

- M1 foundation complete and deployed to a usable staging environment.
- Product and compliance sign-off on consent capture and audit retention semantics.

### Open Questions — M2

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-PRD-001|Should password reset emails be sent synchronously or asynchronously?|Changes `FR-AUTH-005` request-path latency and failure-handling model.|Engineering|2026-04-23|
|2|OQ-PRD-003|Should the lockout policy also trigger admin notification after the fifth failed attempt?|Affects `FR-AUTH-001`, `COMP-014`, and future admin tooling scope.|Security|2026-04-23|
|3|OQ-GAP-001|Should logout revoke only the presented refresh token or all active refresh tokens for the user?|Affects `API-007` semantics and user expectations on shared devices.|Product|2026-04-24|

### Risk Assessment and Mitigation — M2

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-001 token theft via XSS or token persistence mistakes|High|Medium|Session hijacking|Keep access token in memory only, use HttpOnly cookie for refresh token, short access TTL, and invalidate sessions on reset.|security|
|2|R-002 brute-force pressure on login flow|Medium|High|Unauthorized access attempts and service degradation|Combine gateway rate limits, 5-in-15 lockout, bcrypt cost 12, and audit alerts for repeated failures.|backend|

## M3: API Surface and Frontend Integration

**M3: API Surface and Frontend Integration** | Weeks 5-6 | exit criteria: all user- and integration-facing routes and React auth components are wired against stable service contracts

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|API-001|Login API|Expose login over REST with generic failures, lockout handling, and rate-limit behavior.|Auth API|FR-AUTH-001, COMP-005, INF-003|method:POST; path:/v1/auth/login; auth:none; request:email,password; response200:accessToken,refreshToken,expiresIn,tokenType; errors:401,423,429|M|P0|
|2|API-002|Registration API|Expose registration with validation, uniqueness, and profile-return behavior.|Auth API|FR-AUTH-002, COMP-005, INF-003|method:POST; path:/v1/auth/register; auth:none; request:email,password,displayName,consent; response201:id,email,displayName,createdAt,updatedAt,lastLoginAt,roles; errors:400,409|M|P0|
|3|API-003|Profile API|Expose authenticated profile retrieval for the current user.|Auth API|FR-AUTH-004, COMP-005, INF-003|method:GET; path:/v1/auth/me; auth:Bearer-accessToken; response200:id,email,displayName,createdAt,updatedAt,lastLoginAt,roles; errors:401|S|P0|
|4|API-004|Refresh API|Expose refresh-token rotation and renewal behavior for browser and API consumers.|Auth API|FR-AUTH-003, COMP-006, INF-003|method:POST; path:/v1/auth/refresh; auth:refresh-token; request:refreshToken-or-HttpOnly-cookie; response200:accessToken,refreshToken,expiresIn,tokenType; errors:401|M|P0|
|5|API-005|Reset-request API|Expose password-reset initiation with generic success semantics.|Auth API|FR-AUTH-005, COMP-005, INF-003|method:POST; path:/v1/auth/reset-request; auth:none; request:email; response200:generic-confirmation; enumeration:prevented; delivery:SendGrid-triggered|S|P0|
|6|API-006|Reset-confirm API|Expose password-reset completion with token validation and password update behavior.|Auth API|FR-AUTH-005, COMP-013, INF-003|method:POST; path:/v1/auth/reset-confirm; auth:none; request:token,newPassword; response200:password-updated; errors:400,401; usedOrExpiredToken:rejected|S|P0|
|7|COMP-001|LoginPage|Build the login route with generic error handling, lockout messaging, and successful redirect.|Frontend|API-001|route:/login; props:onSuccess,redirectUrl?; fields:email,password; errors:generic-no-enumeration; success:stores-auth-state-via-AuthProvider|M|P0|
|8|COMP-002|RegisterPage|Build the registration route with inline validation, consent capture, and successful session establishment.|Frontend|API-002|route:/register; props:onSuccess,termsUrl; fields:email,password,displayName,consent; clientValidation:password-policy; success:creates-session-and-redirects|M|P0|
|9|COMP-003|ProfilePage|Build the authenticated profile route that renders current user data from `/auth/me`.|Frontend|API-003|route:/profile; auth:required; fieldsRendered:id,email,displayName,createdAt,lastLoginAt,roles; unauthorized:redirect-to-login|S|P0|
|10|COMP-004|AuthProvider|Build the React auth context that stores access tokens in memory, manages refresh, intercepts 401s, and exposes auth actions.|Frontend|API-001, API-003, API-004, API-007|props:children; accessToken:memory-only; refreshToken:HttpOnly-cookie-aware; silentRefresh:supported; methods:login,logout,register,loadProfile; 401Interceptor:redirects-unauthenticated-users|L|P0|
|11|API-008|Admin audit-log query API|Add the missing admin query surface required by Jordan’s PRD JTBD for incident investigation and auditors.|Admin API|COMP-012, COMP-014|method:GET; path:/v1/auth/audit-logs; auth:admin; filters:userId,dateRange,eventType,outcome; response:paginated-log-rows; retention:12months-visible|M|P1|

### Integration Points — M3

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|Frontend route registry|registry|`/login`, `/register`, `/profile` route bindings|M3|COMP-001, COMP-002, COMP-003|
|Auth context provider tree|dependency injection|COMP-004 wraps app and injects auth state/actions|M3|COMP-001, COMP-002, COMP-003|
|401 response interceptor|middleware chain|COMP-004 handler refreshes or redirects on unauthorized|M3|All authenticated frontend requests|
|Admin audit query binding|dispatch table|API-008 filter-to-query mapping|M3|Jordan admin workflows, compliance review|

### Milestone Dependencies — M3

- M2 services and contracts complete.
- Frontend routing framework available and compatible with protected-route behavior.

### Open Questions — M3

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-001|Should `AuthService` support API key authentication for service-to-service calls beyond refresh-token flows?|May expand API scope beyond the current Sam persona coverage path.|test-lead|2026-04-15|
|2|OQ-PRD-004|Should we support a "remember me" option to extend session duration?|Affects `API-004`, `COMP-001`, and session-policy UX/cookie semantics.|Product|2026-04-26|
|3|OQ-GAP-002|Does admin audit-log access require a dedicated UI in v1.0 or is API-only sufficient?|Changes whether a frontend admin component must be added before M3 exit.|Product|2026-04-26|

### Risk Assessment and Mitigation — M3

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Frontend token handling drifts from the in-memory/HttpOnly security model|High|Medium|Regresses XSS/session-hijack posture|Treat client storage rules as non-negotiable ACs for `COMP-004` and verify via E2E and code review.|frontend|
|2|PRD-critical admin visibility remains unimplemented|High|Medium|Jordan persona and SOC2 use cases remain blocked|Ship API-008 as an explicit gap-fill deliverable and surface remaining UI uncertainty as an OQ.|architect|

## M4: Compliance, Validation, and Quality Gates

**M4: Compliance, Validation, and Quality Gates** | Weeks 7-8 | exit criteria: technical and compliance success criteria are measurable, tested, and passing against staging-like environments

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|TEST-001|Valid login unit test|Verify valid credentials drive password verification and token issuance.|QA|FR-AUTH-001, COMP-005, COMP-006, COMP-008|level:unit; component:AuthService; input:valid-email-password; expected:verify-called,issueTokens-called,AuthToken-returned|S|P0|
|2|TEST-002|Invalid login unit test|Verify invalid credentials return errors without issuing tokens.|QA|FR-AUTH-001, COMP-005, COMP-008|level:unit; component:AuthService; input:invalid-password; expected:401; tokenIssued:false|S|P0|
|3|TEST-003|Refresh rotation unit test|Verify valid refresh tokens rotate and old tokens are revoked.|QA|FR-AUTH-003, COMP-006|level:unit; component:TokenManager; input:valid-refresh-token; expected:new-pair-issued,old-token-revoked|S|P0|
|4|TEST-004|Registration integration test|Verify registration persists `UserProfile` and hashed password in PostgreSQL.|QA|FR-AUTH-002, DM-001, INF-001|level:integration; scope:AuthService+PostgreSQL; input:valid-register-payload; expected:201,profile-row-inserted,password-stored-as-bcrypt-hash|M|P0|
|5|TEST-005|Expired refresh integration test|Verify expired Redis refresh tokens are rejected with 401.|QA|FR-AUTH-003, INF-002|level:integration; scope:TokenManager+Redis; input:expired-refresh-token; expected:401|S|P0|
|6|TEST-006|Register-login-profile E2E test|Verify the end-to-end user journey through RegisterPage, LoginPage, AuthProvider, and ProfilePage.|QA|COMP-001, COMP-002, COMP-003, COMP-004|level:E2E; flow:register->login->profile; expected:session-established,profile-rendered,silent-refresh-compatible|M|P0|
|7|NFR-PERF-001|API response-time validation|Validate auth endpoints stay below 200ms p95 with tracing-backed measurement.|Performance|API-001, API-002, API-003, API-004|metric:p95-response-time; target:<200ms; measurement:APM-tracing-on-AuthService-methods|M|P0|
|8|NFR-PERF-002|Concurrent authentication validation|Validate support for 500 concurrent login requests using load testing.|Performance|API-001, INF-001, INF-002|metric:concurrent-logins; target:500; measurement:k6-load-test; latency:within-target-band|M|P0|
|9|NFR-REL-001|Availability validation|Validate 99.9% uptime measurement path over rolling windows using health checks and monitors.|Reliability|INF-003, OPS-005|metric:availability; target:99.9%-30day-window; measurement:uptime-monitoring-on-health-endpoint|S|P0|
|10|NFR-SEC-001|Password-hashing compliance validation|Verify bcrypt cost factor 12 and raw-password handling constraints.|Security QA|COMP-008|metric:bcrypt-cost-parameter; target:12; validation:unit-test-plus-log-scrub-for-no-plaintext|S|P0|
|11|NFR-SEC-002|Token-signing compliance validation|Verify RS256 signing with 2048-bit RSA keys and configuration enforcement.|Security QA|COMP-007|metric:JWT-algorithm-and-key-size; target:RS256-and-2048bit; validation:config-validation-test-and-token-inspection|S|P0|
|12|NFR-COMPLIANCE-001|SOC2 audit logging validation|Validate that all auth events are logged with required fields and retained for the compliant period.|Compliance QA|COMP-012, COMP-014|metric:audit-log-completeness; target:userId+timestamp+ip+outcome-on-all-auth-events-and-12month-retention; validation:log-schema-audit-plus-retention-policy-check|M|P0|
|13|NFR-COMPLIANCE-002|GDPR consent validation|Validate that registration requires consent and records it with timestamp.|Compliance QA|FR-AUTH-002|metric:consent-capture; target:required-at-registration-with-timestamp; validation:integration-test-plus-db-verification|S|P0|
|14|NFR-COMPLIANCE-003|NIST password-storage validation|Validate one-way adaptive hashing and guarantee raw passwords are never persisted or logged.|Compliance QA|COMP-008, FR-AUTH-002, FR-AUTH-005|metric:plaintext-password-exposure; target:none; validation:storage-inspection-plus-log-scrub-plus-security-test|S|P0|
|15|NFR-COMPLIANCE-004|GDPR data-minimization validation|Validate only email, hashed password, and display name are collected as required user data.|Compliance QA|DM-001, FR-AUTH-002|metric:collected-PII-surface; target:email+hashedPassword+displayName-only; validation:schema-review-plus-request-payload-audit|S|P0|

### Integration Points — M4

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|Test environment matrix|registry|local/CI/staging environment mapping|M4|TEST-004, TEST-005, TEST-006|
|Auth metrics exporter|middleware chain|INF-005 metrics hooks attached to auth handlers|M4|NFR-PERF-001, NFR-REL-001, OPS-005|
|Load-test target manifest|dispatch table|endpoint and concurrency targets mapped for k6|M4|NFR-PERF-002|
|Compliance validation checklist|callback wiring|security/compliance assertions linked to release gate|M4|NFR-SEC-001, NFR-SEC-002, M5 go-live review|

### Milestone Dependencies — M4

- M3 endpoints and frontend flows complete.
- Real PostgreSQL and Redis test environments available; no mock-only acceptance for integration gates.

### Open Questions — M4

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-GAP-003|What alert threshold should define SendGrid delivery failure for production gating?|Affects whether email reliability is strong enough to release password reset.|Platform|2026-04-28|
|2|OQ-GAP-004|How should hashed password storage be represented in the technical data model when `DM-001` currently enumerates profile fields only?|Needed to reconcile PRD data-minimization and NIST storage requirements with implementation ownership and schema traceability.|architect|2026-04-28|

### Risk Assessment and Mitigation — M4

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Compliance validation passes technically but misses PRD-required audit details|High|Medium|SOC2 readiness remains false-positive|Cross-check validation against PRD fields user ID, timestamp, IP, outcome, and 12-month retention explicitly.|compliance|
|2|Performance targets degrade under real concurrency despite passing unit/integration tests|High|Medium|Launch blocked or unstable|Run k6 against staging with real PostgreSQL/Redis and trace bottlenecks before rollout approval.|qa|

## M5: Release Rollout and Operational Readiness

**M5: Release Rollout and Operational Readiness** | Weeks 9-10 | exit criteria: phased release, rollback, monitoring, and on-call readiness are complete for GA

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|MIG-001|Phase 1 internal alpha|Deploy to staging/internal users behind feature flags and validate all critical flows manually and automatically.|Release|M4|duration:1week; audience:auth-team+QA; flags:AUTH_NEW_LOGIN-enabled-internal; success:FR-AUTH-001..005-pass; bugs:P0/P1-zero-open|M|P0|
|2|MIG-002|Phase 2 beta 10% rollout|Expose the new auth path to 10% of traffic and observe latency, errors, and refresh behavior.|Release|MIG-001|duration:2weeks-planned-within-rollout-window; traffic:10%; p95:<200ms; errorRate:<0.1%; RedisFailures:none-material|M|P0|
|3|MIG-003|Phase 3 general availability|Promote the new stack to 100% of traffic and retire legacy auth routing.|Release|MIG-002|duration:1week-planned-within-rollout-window; traffic:100%; uptime:99.9%-first-7-days; dashboards:green; legacyEndpoints:deprecated|M|P0|
|4|OPS-001|Runbook for AuthService outage|Prepare response guidance for total auth-service failure and dependency outages.|Operations|MIG-001|symptoms:/auth/*-5xx; diagnosis:pods,postgres,passwordhasher,tokenmanager; resolution:restart/failover/relogin; escalation:auth-team->platform-team|S|P0|
|5|OPS-002|Runbook for token refresh failures|Prepare response guidance for silent-refresh breakage, redirect loops, and Redis/key failures.|Operations|MIG-001|symptoms:unexpected-logouts,redirect-loop,refresh-errors; diagnosis:Redis,JwtService,flags; resolution:scale-redis,remount-keys,flag-check|S|P0|
|6|OPS-003|On-call and escalation plan|Define 24/7 ownership, acknowledgement targets, and escalation ladder for post-GA support.|Operations|MIG-002|responseTime:P1-within-15min; coverage:24/7-first-2-weeks-post-GA; escalation:auth-team->test-lead->eng-manager->platform-team|S|P0|
|7|OPS-004|Capacity plan|Validate pod, PostgreSQL, and Redis headroom against the target traffic envelope.|Operations|NFR-PERF-002, MIG-002|pods:3-base-to-10-HPA; postgresPool:100-with-200-upscale-threshold; redisMemory:1GB-with-2GB-upscale-threshold|S|P0|
|8|OPS-005|Production observability and alerting|Finalize dashboards, alerts, and log scrubbing for auth operations and compliance evidence.|Operations|INF-005, COMP-014|logs:structured-auth-events; metrics:auth_login_total,auth_login_duration_seconds,auth_token_refresh_total,auth_registration_total; alerts:login-failure-rate,p95-latency,redis-failures; dashboards:Grafana-ready|M|P0|

### Integration Points — M5

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|Feature-flag registry|registry|`AUTH_NEW_LOGIN` and `AUTH_TOKEN_REFRESH` rollout states|M5|MIG-001, MIG-002, MIG-003|
|Rollback procedure chain|middleware chain|flag disable -> smoke test -> incident diagnostics -> backup restore path|M5|OPS-001, release managers|
|Alert routing bindings|event binding|Prometheus/Grafana alerts wired to on-call escalation targets|M5|OPS-003|
|Operational dashboard catalog|dispatch table|dashboard ownership and use-case mapping|M5|OPS-001, OPS-002, OPS-005|

### Milestone Dependencies — M5

- M4 validation complete and passing.
- Feature flags, dashboards, and runbooks must exist before production traffic is shifted.

### Risk Assessment and Mitigation — M5

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-003 data loss or inconsistency during legacy-auth migration|High|Low|User-impacting auth regression and rollback|Use phased rollout, parallel validation, idempotent upserts, and pre-phase backups with tested rollback.|devops|
|2|R-OPS-001 email delivery failure blocks password resets in production|Medium|Low|Recovery flow unavailable|Add delivery monitoring, alert thresholds, and fallback support channel before GA.|operations|

## Resource Requirements and Dependencies

### External Dependencies

|Dependency|Required By MLS|Status|Fallback|
|---|---|---|---|
|PostgreSQL 15+|M1, M2, M4, M5|Required|Block rollout until provisioned; no acceptable in-memory fallback|
|Redis 7+|M1, M2, M4, M5|Required|Disable refresh flow and force re-login temporarily only during incident response|
|Node.js 20 LTS|M1, M2, M3|Required|No fallback; runtime mandate|
|SendGrid API|M1, M2, M4, M5|Required|Support-channel fallback for password reset while delivery incident is mitigated|
|API Gateway|M1, M3, M5|Required|Do not expose auth service directly to the internet|
|OpenTelemetry + Prometheus|M1, M4, M5|Required|Manual log inspection only as temporary emergency fallback|
|SEC-POLICY-001|M1, M4|Required|Security approval gate remains closed until clarified|
|AUTH-PRD-001|M1, M2, M3, M4|Required|PRD scope remains the authoritative business-context input|

### Infrastructure Requirements

- Kubernetes deployment with 3 baseline replicas and HPA scaling to 10 replicas.
- Secrets distribution for RSA private keys, SendGrid credentials, and database/Redis credentials.
- CI environments with testcontainers-backed PostgreSQL and Redis.
- Staging environment isolated enough to run realistic k6 and Playwright validation.

## Risk Register

|ID|Risk|Affected Milestones|Probability|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|R-001|Token theft via XSS or insecure token persistence|M2, M3|Medium|High|Keep access token in memory only, refresh token in HttpOnly cookie, short TTLs, and session invalidation on reset.|security|
|R-002|Brute-force attacks on login endpoint|M2, M3|High|Medium|Rate limits, lockout after 5 failed attempts in 15 minutes, bcrypt cost 12, and audit alerting.|backend|
|R-003|Data loss during migration from legacy auth|M5|Low|High|Parallel run, idempotent upserts, per-phase backups, and rollback readiness.|devops|
|R-BUS-001|Low registration adoption due to poor UX|M3, M4|Medium|High|Inline validation, friction reduction, and funnel validation before GA.|frontend|
|R-COMP-001|Compliance failure from incomplete audit logging|M1, M2, M4|Medium|High|Define audit schema early and validate PRD-required fields and retention at release gate.|compliance|
|R-OPS-001|Email delivery failures block password reset|M1, M2, M5|Low|Medium|Provision monitored SendGrid integration and operational fallback path.|operations|

## Success Criteria and Validation Approach

|Criterion|Metric|Target|Validation Method|MLS|
|---|---|---|---|---|
|Login latency|API p95 response time|< 200ms|APM tracing on login path plus k6 verification|M4|
|Registration success|Successful registrations / attempts|> 99%|Integration telemetry and funnel checks|M4|
|Refresh latency|Refresh p95 response time|< 100ms|APM tracing on refresh path|M4|
|Availability|Rolling 30-day uptime|99.9%|Health-check monitoring and uptime alerts|M4, M5|
|Password hash time|Hash duration at cost 12|< 500ms|Benchmark in CI/staging|M4|
|Unit coverage|Coverage on auth core services|> 80%|Coverage report on AuthService/TokenManager/JwtService/PasswordHasher|M4|
|Functional completeness|All 5 FRs implemented with passing tests|100%|Traceability from FR rows to test rows|M4|
|Integration realism|PostgreSQL and Redis backed tests|Pass|testcontainers-based integration suite|M4|
|Concurrent auth support|Concurrent login requests|500 users|k6 load test|M4|
|Registration conversion|Landing -> confirmed account funnel|> 60%|Product analytics in beta/GA|M5|
|Authenticated user adoption|Daily active authenticated users|> 1000 within 30 days|Token issuance analytics|M5|
|Average session duration|Session duration|> 30 minutes|Refresh event analytics|M5|
|Failed login rate|Failed logins / attempts|< 5%|Audit log analysis|M5|
|Password reset completion|Reset requested -> password changed|> 80%|Reset-flow funnel analysis|M5|

## Decision Summary

|Decision|Chosen|Alternatives Considered|Rationale|
|---|---|---|---|
|Session architecture|JWT access + Redis-backed refresh tokens|Server-side sessions; long-lived JWT only|Chosen because the constraints require stateless service behavior, 15-minute access TTL, 7-day refresh support, and horizontal scaling behind Kubernetes/API Gateway.|
|Token storage on client|Access token in memory, refresh token in HttpOnly cookie|Both tokens in localStorage; both tokens in cookies|Chosen because R-001 explicitly cites XSS risk and the architectural constraints require in-memory access tokens.|
|Password hashing|bcrypt cost factor 12 via PasswordHasher abstraction|Lower bcrypt cost; direct library calls without abstraction|Chosen because FR/NFR require bcrypt cost 12 and future algorithm migration should not force auth-service rewrites.|
|Audit-log scope|Explicit audit entity and admin query API added to roadmap|Assume logs remain internal only|Chosen because PRD Jordan persona and SOC2 logging requirements demand queryable logs with user ID, timestamp, IP, and outcome.|
|Release strategy|3-phase flag-based rollout with rollback gates|Big-bang cutover|Chosen because migration risk R-003 and success criteria require observable, reversible production progression.|

## Timeline Estimates

|MLS|Duration|Start|End|Key Milestones|
|---|---|---|---|---|
|M1|2 weeks|Week 1|Week 2|Schema, crypto, infra, gateway, observability baseline|
|M2|2 weeks|Week 3|Week 4|AuthService, TokenManager, login/register/reset/logout, audit emission|
|M3|2 weeks|Week 5|Week 6|APIs, LoginPage, RegisterPage, ProfilePage, AuthProvider, admin audit query API|
|M4|2 weeks|Week 7|Week 8|Tests, performance, reliability, security, compliance validation|
|M5|2 weeks|Week 9|Week 10|Alpha, beta, GA rollout; runbooks; on-call; dashboards|

**Total estimated duration:** 10 weeks
