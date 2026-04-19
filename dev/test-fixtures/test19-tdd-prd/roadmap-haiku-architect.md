---
spec_source: "test-tdd-user-auth.compressed.md"
complexity_score: 0.68
complexity_class: MEDIUM
primary_persona: architect
adversarial: false
base_variant: "none"
variant_scores: "none"
convergence_score: none
---

# User Authentication Service — Project Roadmap

## Executive Summary

This roadmap delivers a security-first authentication foundation that unblocks the Q2 2026 personalization roadmap, closes the SOC2 Type II auditability gap before the Q3 2026 audit window, and covers the full v1.0 identity lifecycle: registration, login, logout, session refresh, profile retrieval, password reset, audit visibility, staged rollout, and operational readiness. The sequencing is intentionally architectural: data contracts, cryptographic controls, compliance capture, and routing policy land before lifecycle APIs; APIs land before UX surfaces; rollout controls and runbooks land only after test and compliance evidence exist.

The plan also gap-fills PRD-required capabilities omitted or underspecified in the extraction/TDD layer: logout, admin-facing authentication event visibility, forgot-password/reset UI, and health verification. Those additions are treated as first-class roadmap deliverables rather than implicit follow-on work so that Sam’s programmatic token use case and Jordan’s incident-investigation JTBD are both covered within v1.0 scope.

**Business Impact:** Enables the identity layer required for personalized features, protects the projected $2.4M annual revenue unlock tied to authentication-dependent roadmap items, reduces access-related support load, and establishes the audit trail required for enterprise compliance.

**Complexity:** MEDIUM (0.68) — narrow product scope (email/password only; no OAuth, MFA, or RBAC enforcement) but high security sensitivity, multiple infrastructure dependencies, and explicit GDPR/SOC2/NIST obligations.

**Critical path:** M1 identity data plane and cryptographic controls → M2 lifecycle APIs and PRD gap-fill endpoints → M3 frontend experience, validation, and compliance evidence → M4 feature-flagged rollout, rollback readiness, and 99.9% uptime operations.

**Key architectural decisions:**

- Use stateless RS256 access tokens plus Redis-backed opaque refresh tokens instead of server-side sessions to preserve horizontal scale and controlled revocation.
- Keep access tokens ephemeral on the client and use HttpOnly refresh-token handling, audit logging, and forced session revocation to mitigate token theft and password-reset fallout.
- Treat logout, admin audit visibility, and health verification as v1.0 deliverables because the PRD requires them even where the extracted TDD artifacts are incomplete.

**Open risks requiring resolution before M1:**

- `OQ-PRD-003` must finalize the lockout threshold so backend lockout state, UI messaging, and gateway rate-limit posture do not diverge.
- `OQ-002` must clarify the `roles` array bound so `UserProfile` schema validation is not retrofitted after rollout.
- The TDD should be updated to acknowledge PRD-derived gap fills for logout and admin audit visibility before implementation evidence is reviewed.

## Milestone Summary

|ID|Title|Type|Priority|Effort|Dependencies|Deliverables|Risk|
|---|---|---|---|---|---|---|---|
|M1|Identity Data, Crypto, and Control Plane|Foundation|P0|XL|—|21|High|
|M2|Account Lifecycle and Service APIs|Platform|P0|XL|M1|21|High|
|M3|Frontend Experience, Validation, and Compliance Evidence|Experience|P0|XL|M1, M2|21|High|
|M4|Rollout, Operations, and Reliability|Launch|P0|XL|M1, M2, M3|20|High|

## Dependency Graph

PostgreSQL 15+ → `DM-001` + `COMP-009` + `COMP-011` → `COMP-005` → `API-001`,`API-002`,`API-003`,`API-005`,`API-006`,`API-008`

Redis 7+ → `DM-002` + `COMP-012` + `COMP-013` + `COMP-015` → `COMP-006` → `API-004`,`API-007`,`COMP-019`,`COMP-020`

RSA key material → `COMP-016` → `COMP-007` → `COMP-006` + `COMP-032` → `API-003`,`API-009`

Gateway policies → `COMP-017` + `COMP-030` + `COMP-018` → all `/v1/auth/*` routes

`COMP-005` + `COMP-006` + `COMP-007` + `COMP-008` → FR-AUTH-001..005 → API-001..007

API surface → `COMP-004` → `COMP-001`,`COMP-002`,`COMP-003`,`COMP-022`,`COMP-023`,`COMP-024`,`COMP-025`

Metrics and traces → `COMP-028` + `COMP-029` → `TEST-004`,`TEST-005`,`NFR-PERF-001`,`OPS-007`,`OPS-008`

Feature flags `MIG-004`,`MIG-005` → `MIG-001` → `MIG-002` → `MIG-003`

## M1: Identity Data, Crypto, and Control Plane

**Objective:** Establish the identity data plane, cryptographic configuration, compliance capture, and request-control infrastructure required for safe auth implementation. | **Duration:** 2 weeks (weeks 1-2) | **Entry:** Product and engineering confirm v1.0 remains email/password only; PostgreSQL 15+, Redis 7+, Node.js 20 LTS, and API Gateway are available; security team provides RSA key issuance path. | **Exit:** Identity schemas, stores, repos, control-plane components, and security policies are implemented in staging; compliance and crypto configuration is verifiable; request ingress is constrained before public auth flows are enabled.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|DM-001|UserProfile schema and contract|Define and migrate the canonical `UserProfile` model and storage contract.|PostgreSQL|—|id:UUID-PK-NOTNULL; email:string-UNIQUE-NOTNULL-indexed-lowercase-normalized; displayName:string-NOTNULL-2..100; createdAt:ISO8601-NOTNULL-default-now; updatedAt:ISO8601-NOTNULL-auto-updated; lastLoginAt:ISO8601-NULLABLE-set-on-login; roles:string[]-NOTNULL-default['user']-not-enforced; relationships:1:N-refresh-tokens,1:N-audit-log|M|P0|
|2|DM-002|AuthToken contract and token storage model|Define the token pair contract and persistence rules for access vs refresh state.|Redis|DM-001|accessToken:JWT-NOTNULL-RS256-signed-payload-user-id+roles; refreshToken:opaque-string-NOTNULL-unique-7d-TTL-Redis; expiresIn:number-NOTNULL-always-900; tokenType:string-NOTNULL-always-Bearer; accessToken:not-persisted; refreshToken:stored-hashed|S|P0|
|3|NFR-SEC-001|bcrypt cost-12 baseline|Lock password hashing configuration before service flows are built.|PasswordHasher|—|bcrypt-only; cost-factor=12; config-tested; startup-fails-if-weaker; no alternate algorithm in-v1.0|S|P0|
|4|NFR-SEC-002|RS256 signing baseline|Lock JWT signing algorithm and key strength before token issuance exists.|JwtService|—|alg=RS256; RSA-key-size>=2048; rotation-window=quarterly; config-tested; no weaker algorithm accepted|S|P0|
|5|NFR-COMPLIANCE-001|Consent capture persistence|Add GDPR consent capture needed at registration time.|ConsentRepo|DM-001|registration-consent-required; consent-recorded-with-timestamp; consent-version-stored; linked-to-user-id; queryable-for-audit|S|P0|
|6|NFR-COMPLIANCE-003|One-way adaptive password storage|Enforce NIST-aligned storage rules at the boundary of the auth domain.|PasswordHasher|NFR-SEC-001|one-way-adaptive-hashing; raw-password-never-persisted; raw-password-never-logged; verification-only-via-hash-compare|S|P0|
|7|NFR-COMPLIANCE-004|Data minimization guardrails|Constrain persisted profile data to GDPR-minimum scope.|ConfigValidator|DM-001|allowed-user-fields=email,password_hash,display_name,consent,timestamps,roles; no-extra-PII-required; schema-review-required-for-new-fields|S|P0|
|8|COMP-005|AuthService component skeleton|Create the backend orchestration boundary for all auth flows.|AuthService|COMP-009,COMP-011,COMP-006,COMP-008|location:backend-service; flows:login,register,profile,refresh,reset-request,reset-confirm; delegates:PasswordHasher,TokenManager,UserRepo; deps:PostgreSQL,PasswordHasher,TokenManager,SendGrid-reset; emits-audit-and-metrics-hooks|M|P0|
|9|COMP-006|TokenManager component skeleton|Create the token lifecycle manager and revocation contract.|TokenManager|COMP-012,COMP-007|functions:issue,revoke,refresh,revoke-all; refresh-token-storage:hashed-in-Redis; refresh-token-TTL=7d; deps:Redis,JwtService|M|P0|
|10|COMP-007|JwtService component skeleton|Create the JWT signing and verification boundary.|JwtService|COMP-016|functions:sign,verify; alg:RS256; RSA:2048-bit; rotation:quarterly; clock-skew:5s; deps:key-material-secrets-volume|M|P0|
|11|COMP-008|PasswordHasher component skeleton|Create the password hashing abstraction for current and future algorithm control.|PasswordHasher|NFR-SEC-001|algorithm:bcrypt; cost:12; abstraction:future-migration-ready; benchmark-target≈300ms/hash; deps:bcryptjs|M|P0|
|12|COMP-009|UserRepo|Repository for `UserProfile` reads/writes and uniqueness checks.|AuthService|DM-001|operations:get-by-id,get-by-email,create,update-last-login,update-password; email-normalization-enforced; unique-email-conflict-surfaced|M|P0|
|13|COMP-010|ConsentRepo|Repository for consent event writes and retrieval.|AuthService|NFR-COMPLIANCE-001,DM-001|operations:record-consent,get-latest-consent; fields:user_id,consent_version,accepted_at; append-only|S|P1|
|14|COMP-011|AuditLogRepo|Repository for auth event persistence and query support.|AuthService|DM-001|operations:write-event,query-by-user,query-by-range; fields:user_id,timestamp,ip,outcome,event_type; retention-ready|M|P0|
|15|COMP-012|RefreshTokenStore|Redis-backed store for hashed refresh tokens and session revocation state.|TokenManager|DM-002|operations:put,get,delete,delete-all-for-user; hash-refresh-token-before-store; TTL=7d; user-index-for-multi-device-revoke|M|P0|
|16|COMP-013|ResetTokenStore|Redis-backed store for password-reset tokens with one-time-use semantics.|AuthService|DM-001|operations:put,get,mark-used,delete; token-TTL=1h; one-time-use-enforced; user-id-linked|S|P0|
|17|COMP-014|PasswordPolicyValidator|Central password validation module reused by registration and reset flows.|AuthService|NFR-COMPLIANCE-003|rules:min-length-8,requires-uppercase,requires-number; returns-machine-readable-reasons; reusable-from-frontend-and-backend|S|P0|
|18|COMP-015|LoginAttemptTracker|Track failed login attempts and account lockout windows.|AuthService|Redis|window=15m; threshold=5-failures-pending-final-decision; keyed-by-normalized-email-or-user; clear-on-success-or-expiry|M|P0|
|19|COMP-016|ConfigValidator|Boot-time validator for crypto, CORS, TLS, retention, and service limits.|AuthService|NFR-SEC-001,NFR-SEC-002|validates:bcrypt-cost,JWT-alg,key-size,TTL,CORS-origin-list,TLS-mode,retention-window; fail-fast-on-invalid-config|S|P0|
|20|COMP-017|RateLimitPolicyRegistry|Registry for per-endpoint gateway policy and lockout coordination.|API Gateway|—|entries:login-10/min/IP,register-5/min/IP,me-60/min/user,refresh-30/min/user,reset-request-5/min/IP,logout-30/min/user; queryable-by-route-id|S|P0|
|21|COMP-030|SecurityHeadersMiddleware|Apply request/response hardening needed before auth pages and APIs go live.|API Gateway|COMP-017|enforces:TLS1.3-only,CORS-allowlist,secure-cookie-policy,baseline-CSP-hooks,X-Frame-Options-deny,referrer-policy,cache-control-no-store-for-auth|M|P0|

### Integration Points — M1

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|PostgreSQL connection pool|DI|Yes|M1|COMP-009, COMP-010, COMP-011, COMP-005|
|Redis client|DI|Yes|M1|COMP-012, COMP-013, COMP-015, COMP-006|
|RSA key secrets mount|Secret wiring|Yes|M1|COMP-016, COMP-007|
|Rate-limit policy registry|Registry|Yes|M1|COMP-018, API-001..007|
|Security headers middleware|Middleware chain|Yes|M1|All auth API routes and frontend auth responses|

### Risk Assessment and Mitigation — M1

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-PRD-002 Security breach from implementation flaws|Critical|Medium|Weak crypto or ingress config compromises every later milestone.|Lock crypto and ingress posture before lifecycle APIs; enforce boot-time config validation; security review M1 outputs.|security-team|
|2|R-PRD-003 Compliance failure from incomplete audit logging|High|Medium|Missing consent or audit persistence causes rework and audit failure later.|Implement consent and audit repositories in foundation milestone; validate required fields early.|compliance-team|
|3|R-002 Brute-force attacks on login|Medium|Medium|Control-plane gaps make later lockout and rate-limit work ineffective.|Define gateway rate-limit registry and login-attempt tracker before API exposure.|platform-team|

### Milestone Dependencies — M1

- No prior milestone dependencies.
- External prerequisites: PostgreSQL 15+, Redis 7+, Node.js 20 LTS, API Gateway, key-management path, frontend routing framework.

### Open Questions — M1

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-PRD-003|Is 5 failed attempts in 15 minutes the final lockout policy, or should the threshold/window change?|Affects `COMP-015`, gateway messaging, alert thresholds, and FR-AUTH-001 behavior.|Security|Week 1|
|2|OQ-002|What is the maximum allowed `UserProfile.roles` array length?|Affects `DM-001` validation, storage constraints, and token payload sizing.|auth-team|Week 2|

## M2: Account Lifecycle and Service APIs

**Objective:** Implement the complete backend lifecycle for login, registration, refresh, profile retrieval, reset, logout, audit visibility, and health checks on top of the M1 control plane. | **Duration:** 3 weeks (weeks 3-5) | **Entry:** M1 exit criteria met; lockout policy resolved; secrets and dependencies available in staging. | **Exit:** All auth lifecycle APIs are implemented and contract-complete; PRD gap-fill APIs exist; service wiring is end-to-end functional in staging; health and admin audit surfaces are queryable.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-AUTH-001|Login flow|Implement credential authentication and lockout behavior.|AuthService|COMP-005,COMP-008,COMP-015,COMP-006|valid-credentials→200+AuthToken; invalid-credentials→401; non-existent-email→401-no-enumeration; locked-after-5-failed-attempts/15m→423|M|P0|
|2|FR-AUTH-002|Registration flow|Implement account creation with uniqueness, password policy, and profile creation.|AuthService|COMP-005,COMP-009,COMP-010,COMP-014|valid-registration→201+UserProfile; duplicate-email→409; weak-password(<8/no-uppercase/no-number)→400; stores-bcrypt-cost12-hash|M|P0|
|3|FR-AUTH-003|Token issuance and refresh|Implement token pair issuance and silent-refresh-compatible exchange.|TokenManager|COMP-006,COMP-007,COMP-012|login-returns-accessToken(15m)+refreshToken(7d); valid-refresh→new-AuthToken-pair; expired-refresh→401; revoked-refresh→401|M|P0|
|4|FR-AUTH-004|Profile retrieval|Implement authenticated retrieval of the current user profile.|AuthService|COMP-005,COMP-009,COMP-032|valid-access-token→UserProfile; expired-or-invalid-token→401; response-includes:id,email,displayName,createdAt,updatedAt,lastLoginAt,roles|S|P0|
|5|FR-AUTH-005|Password reset flow|Implement request and confirm reset lifecycle with one-time reset tokens.|AuthService|COMP-005,COMP-013,COMP-014,COMP-006,COMP-027|reset-request-sends-token-email; reset-confirm-updates-password-hash; reset-token-expires-1h; used-reset-token-non-reusable; all-sessions-invalidated-on-confirm|M|P0|
|6|API-001|POST /v1/auth/login|Expose login as a public endpoint with rate limiting and error mapping.|COMP-018|FR-AUTH-001,COMP-017|method:POST; path:/v1/auth/login; auth:none; rate-limit:10/min/IP; request:{email,password}; response-200:AuthToken; errors:401,423,429|M|P0|
|7|API-002|POST /v1/auth/register|Expose registration as a public endpoint with validation handling.|COMP-018|FR-AUTH-002,COMP-017|method:POST; path:/v1/auth/register; auth:none; rate-limit:5/min/IP; request:{email,password,displayName}; response-201:UserProfile; errors:400,409|M|P0|
|8|API-003|GET /v1/auth/me|Expose current-user retrieval behind access-token verification.|COMP-018|FR-AUTH-004,COMP-032|method:GET; path:/v1/auth/me; auth:Bearer-accessToken; rate-limit:60/min/user; header:Authorization:Bearer<jwt>; response-200:UserProfile; errors:401|S|P0|
|9|API-004|POST /v1/auth/refresh|Expose refresh-token exchange and old-token revocation.|COMP-018|FR-AUTH-003,COMP-012|method:POST; path:/v1/auth/refresh; auth:refreshToken-in-body; rate-limit:30/min/user; request:{refreshToken}; response-200:new-AuthToken-pair; errors:401-expired/revoked|M|P0|
|10|API-005|POST /v1/auth/reset-request|Expose reset-token request without account enumeration.|COMP-018|FR-AUTH-005,COMP-027|method:POST; path:/v1/auth/reset-request; auth:none; request:{email}; response-200-regardless-of-email-existence; no-enumeration; email-dispatched-for-known-account|M|P0|
|11|API-006|POST /v1/auth/reset-confirm|Expose reset confirmation and session invalidation.|COMP-018|FR-AUTH-005,COMP-013,COMP-006|method:POST; path:/v1/auth/reset-confirm; auth:resetToken-in-body; request:{resetToken,newPassword}; response-200-on-success; errors:400-expired/used-token; revoke-all-sessions|M|P0|
|12|API-007|POST /v1/auth/logout|PRD-derived logout endpoint to terminate the current session.|COMP-018|COMP-006,COMP-021|method:POST; path:/v1/auth/logout; auth:Bearer-accessToken+refresh-context; response-200; current-refresh-token-revoked; audit-event-written|S|P0|
|13|API-008|GET /v1/admin/auth/audit-log|PRD-derived admin query surface for Jordan’s incident-investigation JTBD.|COMP-018|COMP-026,COMP-032,COMP-011|method:GET; path:/v1/admin/auth/audit-log; auth:admin-context; query:date-range,user-id,event-type,outcome; response:paged-audit-events; internal-only-until-RBAC|M|P1|
|14|API-009|GET /v1/auth/health|Health endpoint for uptime, probes, and operational diagnosis.|COMP-033|COMP-016|method:GET; path:/v1/auth/health; auth:none-internal; response:dependency-status-for-PG,Redis,key-material; used-by-readiness-and-uptime-checks|S|P1|
|15|COMP-018|AuthRoutesController|Controller/router that binds service methods to versioned HTTP routes and error envelopes.|API layer|COMP-005|routes:login,register,me,refresh,reset-request,reset-confirm,logout,admin-audit,health; version-prefix:/v1/auth/*; error-envelope:{error:{code,message,status}}|M|P0|
|16|COMP-021|AuthCookieWriter|Central writer for secure refresh-token cookie behavior and clearing on logout/reset.|API layer|COMP-030|cookie:httpOnly,secure,sameSite=strict; used-on-login,refresh,logout,reset-confirm; clears-cookie-on-session-termination|S|P0|
|17|COMP-026|AuditLogQueryService|Service layer for filtered audit-log reads and export-safe views.|AdminAPI|COMP-011|filters:user-id,date-range,event-type,outcome; supports-pagination; omits-sensitive-fields; optimized-for-incident-investigation|S|P1|
|18|COMP-027|EmailDispatchAdapter|Adapter for SendGrid reset-email delivery and delivery-failure handling.|AuthService|SendGrid API|provider:SendGrid; operation:send-reset-email; includes-template-id,recipient,reset-link; emits-delivery-status; failure-visible-for-alerting|S|P0|
|19|COMP-028|AuthMetricsEmitter|Emit counters and histograms for auth lifecycle events at the service boundary.|Observability|COMP-005|metrics:auth_login_total,auth_login_duration_seconds,auth_token_refresh_total,auth_registration_total; tags:outcome,route; no-secret-values|S|P1|
|20|COMP-032|AccessTokenGuard|Middleware for JWT verification and request user-context hydration.|API layer|COMP-007|verifies:Bearer-JWT; rejects:missing/expired/invalid; hydrates:user-id,roles,token-exp; used-by:/me,/logout,/admin/auth/audit-log|S|P0|
|21|COMP-033|HealthCheckController|Controller for readiness/liveness and dependency diagnosis.|Ops API|COMP-016,API-009|checks:PG,Redis,key-material,config-validity; statuses:ready,degraded,down; machine-readable-response; probe-safe|S|P1|

### Integration Points — M2

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|AuthRoutesController route map|Registry|Yes|M2|All auth API clients and tests|
|AccessTokenGuard|Middleware chain|Yes|M2|API-003, API-007, API-008|
|AuthCookieWriter|Response middleware|Yes|M2|API-001, API-004, API-007, API-006|
|EmailDispatchAdapter|Adapter|Yes|M2|API-005, FR-AUTH-005|
|AuditLogQueryService|Service wiring|Yes|M2|API-008, COMP-025|

### Risk Assessment and Mitigation — M2

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-001 Token theft via XSS|High|Medium|Stolen tokens can impersonate users until expiry or revocation.|Use in-memory access tokens, HttpOnly refresh cookies, short access TTL, revoke-all on reset, secure headers.|security-team|
|2|R-002 Brute-force attacks on login|Medium|High|Automated credential attacks may cause takeover or service pressure.|Combine gateway rate limits, lockout tracker, bcrypt cost 12, and alerting for failure spikes.|security-team|
|3|R-PRD-004 Email delivery failures block password reset|Medium|Medium|Users cannot recover access without working reset email delivery.|Add delivery adapter status, monitoring, fallback support path, and visible failure telemetry.|platform-team|

### Milestone Dependencies — M2

- Depends on M1 schemas, stores, crypto, and ingress controls.
- External dependencies: SendGrid API availability, API Gateway route publication, secrets volume mounted in staging.

### Open Questions — M2

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-001|Should `AuthService` support API key authentication for service-to-service calls in v1.1 planning?|Affects whether current API contracts need explicit future extension points; not in v1.0 scope.|test-lead|Week 4|
|2|OQ-PRD-001|Should password-reset emails be sent synchronously or asynchronously?|Changes API-005 latency, failure semantics, queueing architecture, and user messaging.|Engineering|Week 3|
|3|OQ-PRD-002|What is the maximum allowed number of refresh tokens per user across devices?|Affects `COMP-012` user-token indexing, revocation behavior, and multi-device session policy.|Product|Week 5|

## M3: Frontend Experience, Validation, and Compliance Evidence

**Objective:** Deliver the end-user and admin-facing auth experience, validate performance and correctness across unit/integration/E2E layers, and produce the compliance evidence required to trust the new auth surface. | **Duration:** 3 weeks (weeks 6-8) | **Entry:** M2 APIs stable in staging and available under the versioned contract; design inputs and routing framework are available. | **Exit:** Core auth UI flows, admin audit visibility, test suite, and compliance/performance evidence pass in staging; feature-flagged auth can be exercised end-to-end by QA.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|COMP-001|LoginPage|Implement the login route and form behavior for end users.|Frontend|API-001,COMP-004|route:/login; auth:none; props:onSuccess:()=>void,redirectUrl?:string; form:email,password; submits:/v1/auth/login; stores-AuthToken-via-AuthProvider; deps:AuthProvider,AuthService-API|M|P0|
|2|COMP-002|RegisterPage|Implement the registration route with client-side validation and consent.|Frontend|API-002,COMP-004,NFR-COMPLIANCE-001|route:/register; auth:none; props:onSuccess:()=>void,termsUrl:string; form:email,password,displayName; client-side-password-strength-validation; calls:/v1/auth/register; deps:AuthProvider,AuthService-API|M|P0|
|3|COMP-003|ProfilePage|Implement the authenticated profile page backed by `/auth/me`.|Frontend|API-003,COMP-004|route:/profile; auth:yes; displays:UserProfile; source:GET-/v1/auth/me; deps:AuthProvider|S|P0|
|4|COMP-004|AuthProvider|Implement auth state management, silent refresh, and unauthenticated redirects.|Frontend|API-001,API-003,API-004,API-007|props:children:ReactNode; manages:AuthToken-state; silent-refresh-via-TokenManager-semantics; intercepts-401s; redirects-unauthenticated-users-to-LoginPage; deps:AuthService-API,TokenManager-semantics|L|P0|
|5|TEST-001|Unit login success test|Verify valid login issues a token pair through service orchestration.|Testing|FR-AUTH-001|scope:unit; validates:AuthService.login→PasswordHasher.verify→TokenManager.issueTokens; expects:valid-AuthToken-with-access+refresh|S|P0|
|6|TEST-002|Unit login failure test|Verify invalid login returns an error and issues no tokens.|Testing|FR-AUTH-001|scope:unit; validates:AuthService.login invalid-password-path; expects:401-style-error; no-AuthToken-issued|S|P0|
|7|TEST-003|Unit refresh success test|Verify refresh revokes old tokens and issues a new pair.|Testing|FR-AUTH-003|scope:unit; validates:TokenManager.refresh; expects:old-refresh-revoked,new-AuthToken-issued-via-JwtService|S|P0|
|8|TEST-004|Integration registration persistence test|Verify registration persists the full user profile path to PostgreSQL.|Testing|FR-AUTH-002,DM-001|scope:integration; path:API→PasswordHasher→PostgreSQL-insert; expects:UserProfile-persisted-and-returned|M|P0|
|9|TEST-005|Integration expired refresh rejection test|Verify Redis TTL expiry invalidates refresh tokens correctly.|Testing|FR-AUTH-003,DM-002|scope:integration; path:Redis-TTL→TokenManager; expects:expired-refresh-token-rejected|M|P0|
|10|TEST-006|E2E register-login-profile journey test|Verify the golden path across registration, login, auth state, and profile rendering.|Testing|COMP-001,COMP-002,COMP-003,COMP-004|scope:E2E; journey:RegisterPage→LoginPage→ProfilePage-via-AuthProvider; expects:end-to-end-success|M|P0|
|11|NFR-PERF-001|p95 auth latency evidence|Measure and validate auth endpoint latency against the p95 target.|Observability|COMP-028,COMP-029|all-auth-endpoints-p95<200ms; measurement-via-APM/OTel-on-AuthService-methods; evidence-captured-for-staging|M|P0|
|12|NFR-PERF-002|500 concurrent login evidence|Load-test concurrent authentication behavior against the scale target.|Testing|API-001,COMP-028|supports-500-concurrent-login-requests; measured-via-k6; no-unbounded-error-spike-or-redis-failure|M|P0|
|13|NFR-COMPLIANCE-002|SOC2 audit logging evidence|Validate all auth events are captured with the required fields and retention assumptions.|Compliance|COMP-011,COMP-026|all-auth-events-logged; fields:user-id,timestamp,IP,outcome; retention=12-months; evidence-queryable-for-audit|M|P0|
|14|COMP-019|RefreshScheduler|Client-side scheduler that triggers silent refresh before access-token expiry.|Frontend|COMP-004,API-004|runs-before-access-expiry; requests-new-token-pair; avoids-visible-session-drop; cancellable-on-logout/tab-close|S|P1|
|15|COMP-020|AuthHttpClientInterceptor|HTTP client wrapper for auth headers, single-refresh retry, and 401 handling.|Frontend|COMP-004,API-004|adds-Authorization-Bearer-header; retries-once-after-refresh; queues-concurrent-401s-during-refresh; redirects-on-refresh-failure|M|P0|
|16|COMP-022|ForgotPasswordPage|PRD-derived page for starting self-service reset without account enumeration.|Frontend|API-005|route:/forgot-password; auth:none; form:email; submits:/v1/auth/reset-request; identical-success-message-regardless-of-registration|S|P0|
|17|COMP-023|ResetPasswordPage|PRD-derived page for completing password reset via emailed token.|Frontend|API-006|route:/reset-password; auth:none; form:resetToken,newPassword,confirmPassword; validates-password-policy; submits:/v1/auth/reset-confirm; handles-expired/used-token-state|S|P0|
|18|COMP-024|LogoutControl|PRD-derived UI control that terminates the current session and redirects out of protected space.|Frontend|API-007,COMP-004|visible-to-authenticated-user; action:POST-/v1/auth/logout; clears-client-auth-state; redirects-to-landing-or-login|S|P0|
|19|COMP-025|AdminAuditLogPage|PRD-derived admin UI for viewing auth events during incidents and audit review.|Frontend|API-008|route:/admin/auth-audit; auth:admin-context; filters:user,date-range,event-type,outcome; paged-results; no-secret-data-rendered|M|P1|
|20|COMP-029|AuthTracingMiddleware|Client/server trace correlation for auth requests, UI actions, and backend spans.|Observability|COMP-028|propagates-trace-id-from-frontend-to-backend; correlates-UI-journey-with-API-spans; visible-in-OTel-tools|S|P1|
|21|COMP-031|FeatureFlagAdapter|Frontend/back-end adapter for `AUTH_NEW_LOGIN` and `AUTH_TOKEN_REFRESH` checks during staged rollout.|Feature flags|MIG-004,MIG-005|reads:AUTH_NEW_LOGIN,AUTH_TOKEN_REFRESH; gates-new-pages-and-refresh-behavior; safe-default=OFF; runtime-observable|S|P0|

### Integration Points — M3

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|AuthProvider context|React context|Yes|M3|LoginPage, RegisterPage, ProfilePage, ForgotPasswordPage, ResetPasswordPage, LogoutControl|
|Auth HTTP interceptor|Middleware chain|Yes|M3|All frontend auth API calls|
|Refresh scheduler|Event/timer|Yes|M3|AuthProvider and token refresh flow|
|Feature flag adapter|Flag registry|Yes|M3|Frontend route and refresh gating during rollout|
|Trace correlation headers|Middleware chain|Yes|M3|Performance validation and operational diagnostics|

### Risk Assessment and Mitigation — M3

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-PRD-001 Low registration adoption from poor UX|Medium|Medium|Friction undermines the business case for shipping auth in Q2.|Add inline validation, clear error states, consent UX, and funnel instrumentation before rollout.|product-team|
|2|R-001 Token theft via XSS|High|Medium|Client-side auth state becomes the most exposed attack surface.|Use in-memory access tokens, secure cookies, no localStorage persistence, CSP/security headers, and 401/logout cleanup.|frontend-team|
|3|R-PRD-003 Compliance failure from incomplete audit logging|High|Medium|UI/admin evidence may not match SOC2 review expectations.|Validate audit-log queryability, required fields, and retention evidence before rollout begins.|compliance-team|

### Milestone Dependencies — M3

- Depends on M2 auth lifecycle APIs, health endpoint, and audit query service.
- Requires frontend routing framework and staging environment with feature flags enabled for QA.

### Open Questions — M3

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-PRD-004|Should v1.0 support a “remember me” option to extend session duration or behavior?|Affects `COMP-019`, session messaging, token TTL policy, and UX scope; current roadmap assumes no extension beyond 7-day refresh window.|Product|Week 7|
|2|OQ-GAP-001|Logout is required by the PRD but not explicit in the extracted TDD — should the TDD be updated to include it formally?|Needed so validation and downstream docs treat logout as in-scope, not a roadmap-only addition.|Engineering|Week 6|
|3|OQ-GAP-002|Admin auth-event visibility is required by Jordan’s JTBD but missing from the extracted functional requirements — should the TDD be updated to include API/UI coverage?|Needed so audit evidence, QA, and release review measure the same scope baseline.|Product + Compliance|Week 8|

## M4: Rollout, Operations, and Reliability

**Objective:** Execute the staged launch plan, prove rollback readiness, operationalize on-call and observability, and meet reliability targets under real traffic. | **Duration:** 4 weeks (weeks 9-12) | **Entry:** M3 end-to-end evidence complete in staging; security/compliance review completed; feature flags available in production control plane. | **Exit:** Internal alpha, 10% beta, and GA are completed or launch-ready; rollback playbook is rehearsed; runbooks, alerts, capacity baselines, and uptime checks are active; the service can sustain production support expectations.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|MIG-001|Phase 1 internal alpha|Deploy auth to staging/internal alpha behind `AUTH_NEW_LOGIN` and validate all core flows manually.|Rollout|M1,M2,M3|phase:internal-alpha; duration:1-week; target:staging+auth-team+QA; flag:AUTH_NEW_LOGIN; exit:FR-AUTH-001..005-pass-manual-test,zero-P0/P1|M|P0|
|2|MIG-002|Phase 2 beta 10% traffic|Enable the new login flow for 10% of traffic and monitor latency/error behavior.|Rollout|MIG-001|phase:beta; duration:2-weeks; exposure:10%-traffic; monitor:latency,error-rate,Redis-usage,AuthProvider-refresh; exit:p95<200ms,error<0.1%,zero-Redis-connection-failures|L|P0|
|3|MIG-003|Phase 3 general availability|Promote the new auth stack to 100% traffic and remove the main login flag.|Rollout|MIG-002|phase:GA; duration:1-week; exposure:100%-traffic; remove:AUTH_NEW_LOGIN; enable:AUTH_TOKEN_REFRESH; exit:99.9%-uptime-first-7-days,all-dashboards-green|M|P0|
|4|MIG-004|Feature flag AUTH_NEW_LOGIN|Define, wire, and govern the main auth-surface rollout flag.|Feature flags|COMP-031|name:AUTH_NEW_LOGIN; purpose:gate-new-LoginPage/AuthService-login; default:OFF; owner:auth-team; cleanup:remove-after-MIG-003|S|P0|
|5|MIG-005|Feature flag AUTH_TOKEN_REFRESH|Define, wire, and govern the refresh-flow rollout flag.|Feature flags|COMP-031|name:AUTH_TOKEN_REFRESH; purpose:gate-refresh-token-flow; default:OFF; owner:auth-team; cleanup:remove-2-weeks-after-MIG-003|S|P0|
|6|MIG-006|Rollback step 1 disable new login|First rollback action disables the main auth feature flag and returns traffic to legacy auth.|Rollback|MIG-004|action:disable-AUTH_NEW_LOGIN; effect:route-traffic-to-legacy-auth; executable-without-code-change|S|P0|
|7|MIG-007|Rollback step 2 verify legacy login|Second rollback action validates the fallback path after disabling the new flow.|Rollback|MIG-006|action:run-legacy-login-smoke-tests; verifies:login-still-works-after-flag-disable; exit:legacy-auth-healthy|S|P0|
|8|MIG-008|Rollback step 3 investigate root cause|Third rollback action collects traces and logs to diagnose the failing auth subsystem.|Rollback|MIG-006,OPS-007|action:inspect-structured-logs+traces; focus:AuthService,Redis,JwtService,PostgreSQL; produces:incident-diagnosis-artifact|S|P0|
|9|MIG-009|Rollback step 4 restore data if needed|Fourth rollback action restores the last known-good backup if corruption is detected.|Rollback|DM-001|action:restore-from-last-known-good-backup; trigger:UserProfile-data-corruption; verification:data-integrity-checks-pass|S|P0|
|10|MIG-010|Rollback step 5 notify teams|Fifth rollback action notifies the auth and platform teams via incident path.|Rollback|OPS-003|action:notify-auth-team+platform-team; channel:incident-channel; timing:immediate-on-rollback-decision|S|P1|
|11|MIG-011|Rollback step 6 post-mortem|Final rollback action creates a post-mortem within 48 hours.|Rollback|MIG-010|action:post-mortem; SLA:within-48-hours; includes:timeline,root-cause,corrective-actions|S|P1|
|12|OPS-001|Runbook AuthService down|Operational guide for 5xx/auth unavailability incidents.|Operations|API-009,OPS-007|symptoms:5xx-on-/auth/*,LoginPage/RegisterPage-error; diagnosis:pod-health,PG-connectivity,PasswordHasher/TokenManager-init-logs; resolution:restart-pods,PG-failover,re-login-if-Redis-down; escalation:auth-oncall→platform@15m|M|P0|
|13|OPS-002|Runbook token refresh failures|Operational guide for session-refresh incident handling.|Operations|API-004,OPS-007|symptoms:unexpected-logouts,redirect-loop,auth_token_refresh_total-spike; diagnosis:Redis,JwtService-key-access,AUTH_TOKEN_REFRESH-flag; resolution:scale-Redis,re-mount-secrets,enable-flag-if-OFF; escalation:auth-team→platform-team|M|P0|
|14|OPS-003|On-call expectations|Define ownership, tooling, and escalation path for the first post-GA period.|Operations|OPS-001,OPS-002|P1-ack≤15m; auth-team-24/7-first-2-weeks-post-GA; tooling:K8s-dashboards,Grafana,Redis-CLI,PG-admin; path:auth-team→test-lead→eng-manager→platform-team|S|P0|
|15|OPS-004|Capacity AuthService pods|Baseline and scaling posture for the service deployment tier.|Operations|API-009|current:3-replicas; expected:500-concurrent-users; scaling-trigger:HPA-to-10-replicas-at-CPU>70%|S|P0|
|16|OPS-005|Capacity PostgreSQL|Baseline and scaling posture for the database tier.|Operations|DM-001|current:pool-100; expected:~50-avg-concurrent-queries; scaling-trigger:increase-pool-to-200-if-wait>50ms|S|P0|
|17|OPS-006|Capacity Redis|Baseline and scaling posture for the token/session cache tier.|Operations|DM-002|current:1GB; expected:~100K-refresh-tokens(~50MB); scaling-trigger:2GB-at->70%-utilization|S|P0|
|18|OPS-007|Observability stack|Activate logs, metrics, and traces for production support and launch monitoring.|Operations|COMP-028,COMP-029|structured-logs:login/register/refresh/reset; metrics:auth_login_total,auth_login_duration_seconds,auth_token_refresh_total,auth_registration_total; spans:AuthService→PasswordHasher→TokenManager→JwtService|M|P0|
|19|OPS-008|Alerting policy|Launch alerts for failure rate, latency, Redis issues, and secret-safe logging posture.|Operations|OPS-007|alerts:login-failure-rate>20%/5m,p95>500ms,Redis-connection-failures-threshold; sensitive-fields-excluded-from-logs|M|P0|
|20|NFR-REL-001|99.9% uptime target|Operationalize and measure availability via health checks and launch monitoring.|Operations|API-009,OPS-007,OPS-008|service-availability=99.9%-over-30-day-rolling-window; measured-via-health-check-endpoint-and-monitoring; SLO-dashboards-live|M|P0|

### Integration Points — M4

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|Feature flag adapter|Flag registry|Yes|M4|MIG-001, MIG-002, MIG-003, frontend gating|
|Health endpoint|Ops endpoint|Yes|M4|Readiness checks, uptime monitors, runbooks|
|Metrics/alerts pipeline|Observability chain|Yes|M4|Beta monitoring, GA monitoring, on-call response|
|Rollback playbook|Operational workflow|Yes|M4|Incident handling and release management|
|Capacity thresholds|Operational config|Yes|M4|HPA, database pool tuning, Redis scaling|

### Risk Assessment and Mitigation — M4

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-003 Data loss during migration|High|Medium|Rollout or rollback can corrupt or lose user-profile state.|Use phased rollout, backups before phases, idempotent restore path, and rehearsed rollback steps.|platform-team|
|2|R-PRD-002 Security breach from implementation flaws|Critical|Low|Uncaught flaws under real traffic become customer-visible incidents.|Require security review and staged traffic exposure before GA; keep rollback path live through beta.|security-team|
|3|R-PRD-004 Email delivery failures block password reset|Medium|Medium|Production recovery experience fails even if core auth is healthy.|Alert on delivery failures, keep fallback support path, and monitor completion-rate criterion.|support-team|

### Milestone Dependencies — M4

- Depends on M3 test, performance, and compliance evidence.
- Requires incident channel, monitoring stack, feature-flag control plane, and on-call rota to be active before beta.

## Resource Requirements and Dependencies

### External Dependencies

|Dependency|Required By Milestone|Status|Fallback|
|---|---|---|---|
|PostgreSQL 15+|M1|Required|Delay rollout until persistent user storage is available; no safe fallback|
|Redis 7+|M1|Required|Disable refresh-based persistence and require re-login; not acceptable for target UX|
|Node.js 20 LTS|M1|Required|No fallback; runtime is mandated|
|bcryptjs|M1|Required|No algorithm fallback in v1.0|
|jsonwebtoken|M1|Required|No signing fallback in v1.0|
|SendGrid API|M2|Required|Manual support-assisted password reset until provider restored|
|API Gateway|M1|Required|No public rollout without TLS/CORS/rate-limit enforcement|
|Frontend routing framework|M3|Required|Auth APIs can ship, but user-facing flow cannot|

### Infrastructure Requirements

- Staging and production environments must both expose PostgreSQL, Redis, secret mounts, and the API Gateway before beta begins.
- RSA signing keys must be issued and rotated through a controlled secret-management workflow with quarterly cadence.
- Observability must include structured logs, Prometheus metrics, OpenTelemetry traces, and alert delivery before any external traffic percentage is enabled.
- Backup and restore validation for `UserProfile` and audit-log data must be completed before `MIG-001`.
- Feature-flag control for `AUTH_NEW_LOGIN` and `AUTH_TOKEN_REFRESH` must support fast disable without redeploy.

## Risk Register

|ID|Risk|Affected Milestones|Probability|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|R-001|Token theft via XSS|M2, M3|Medium|High|Use in-memory access tokens, HttpOnly refresh cookies, secure headers, short TTLs, logout/reset revocation, and frontend hardening.|security-team|
|R-002|Brute-force attacks on login|M1, M2|Medium|Medium|Combine gateway rate limits, lockout tracking, bcrypt cost 12, and failure-rate alerting.|security-team|
|R-003|Data loss during migration|M4|Medium|High|Phase rollout, back up before phases, keep rollback playbook live, restore from last known-good backup when needed.|platform-team|
|R-PRD-001|Low registration adoption from poor UX|M3|Medium|Medium|Use inline validation, clear errors, funnel instrumentation, and pre-launch usability review.|product-team|
|R-PRD-002|Security breach from implementation flaws|M1, M4|Low|Critical|Lock security controls early, require review before rollout, and use staged exposure with rollback capability.|security-team|
|R-PRD-003|Compliance failure from incomplete audit logging|M1, M3|Medium|High|Implement consent/audit persistence early and validate field completeness and retention evidence before launch.|compliance-team|
|R-PRD-004|Email delivery failures block password reset|M2, M4|Medium|Medium|Instrument SendGrid delivery, alert on failures, and provide a fallback support channel.|support-team|

## Success Criteria and Validation Approach

|Criterion|Metric|Target|Validation Method|Milestone|
|---|---|---|---|---|
|Fast login|Login response time p95|< 200ms|APM/OTel traces over API-001 in staging and beta|M3, M4|
|Registration correctness|Registration success rate|> 99%|Integration tests plus rollout funnel monitoring|M3, M4|
|Fast token refresh|Token refresh latency p95|< 100ms|APM/OTel traces over API-004|M3, M4|
|Availability|Service uptime|99.9% over 30-day rolling window|Health checks, SLO dashboard, and uptime monitors|M4|
|Hashing performance|Password hash time|< 500ms at cost 12|Benchmark + config test around PasswordHasher|M1, M3|
|Onboarding value|User registration conversion|> 60%|Product funnel instrumentation during beta and GA|M3, M4|
|Adoption|Daily active authenticated users|> 1000 within 30 days of GA|Analytics on successful authenticated sessions|M4|
|Engagement|Average session duration|> 30 minutes|Token refresh and session analytics|M3, M4|
|Login usability/security balance|Failed login rate|< 5% of attempts|Auth event log analysis|M3, M4|
|Recovery effectiveness|Password reset completion rate|> 80%|Reset funnel from request to successful confirm|M3, M4|

## Decision Summary

|Decision|Chosen|Alternatives Considered|Rationale|
|---|---|---|---|
|Session architecture|RS256 access token + Redis-backed opaque refresh token|Server-side sessions; access-token-only; API keys for all clients|Matches stateless API constraint, supports silent refresh, and aligns with extracted `DM-002`, `FR-AUTH-003`, and Redis dependency.|
|Password storage|bcrypt cost factor 12 via `PasswordHasher`|Lower bcrypt cost; alternate algorithm in v1.0|Required by `FR-AUTH-002`, `NFR-SEC-001`, and `NFR-COMPLIANCE-003`; extraction explicitly forbids alternative algorithms in v1.0.|
|Rollout approach|Three phases with two feature flags and six-step rollback|Big-bang release; no flag gating|Backed by `MIG-001..011`, risk `R-003`, and the extracted phased rollout/rollback plan.|
|Client token handling|Access token in memory, refresh token in HttpOnly cookie|localStorage/sessionStorage persistence; long-lived access token|Direct mitigation for `R-001` and consistent with PRD session-persistence UX without increasing XSS exposure.|
|Admin audit visibility|Ship API/UI gap-fill in v1.0 roadmap|Defer entirely to future RBAC effort|Jordan’s PRD JTBD and `NFR-COMPLIANCE-002` require queryable auth-event visibility even though the extracted FR list omits it.|

## Timeline Estimates

|Milestone|Duration|Start|End|Key Milestones|
|---|---|---|---|---|
|M1|2 weeks|Week 1|Week 2|Schemas, repos, stores, crypto/config validators, request-control plane|
|M2|3 weeks|Week 3|Week 5|Lifecycle service methods, versioned APIs, logout/admin audit/health gap fills|
|M3|3 weeks|Week 6|Week 8|Frontend auth flows, test pyramid, performance and compliance evidence|
|M4|4 weeks|Week 9|Week 12|Alpha, beta, GA, rollback rehearsal, on-call and reliability operations|

**Total estimated duration:** 12 weeks
