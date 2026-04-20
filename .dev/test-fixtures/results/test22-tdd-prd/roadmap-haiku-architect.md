---
spec_source: "test-tdd-user-auth.compressed.md"
complexity_score: 0.75
complexity_class: HIGH
primary_persona: architect
base_variant: "none"
variant_scores: "none"
convergence_score: null
---

# User Authentication Service — Project Roadmap

## Executive Summary

This roadmap translates the authentication extraction, TDD, and PRD into a technically phased plan that preserves every extracted ID, closes spec gaps, and keeps the default schedule inside the committed TDD end date of 2026-06-09. The plan prioritizes security primitives and compliance data contracts first, then layers token lifecycle and APIs, then frontend and email integrations, then hardening, and finally phased rollout with explicit rollback and on-call readiness.

**Business Impact:** Unblocks the 2026 personalization roadmap, supports the Q3 SOC2 audit path, reduces access-related support burden, and establishes the identity foundation required for persistent user sessions and programmatic integrations.

**Complexity:** HIGH (0.75) — security-critical auth flows, PostgreSQL+Redis coordination, frontend/backend/email integration, phased rollout, and GDPR/SOC2/NIST obligations all land in the same release.

**Critical path:** M1 compliant data/security foundation -> M2 token lifecycle and core auth APIs -> M3 frontend, reset, and audit-query integrations -> M4 performance/observability hardening -> M5 rollout, rollback, and production readiness.

**Key architectural decisions:**

- Use stateless JWT access tokens plus revocable refresh tokens, with RS256 signing and Redis-backed refresh-token control.
- Keep user profiles and audit records in PostgreSQL, enforce bcrypt cost 12 via `PasswordHasher`, and never persist or log raw secrets.
- Resolve document conflicts in favor of committed compliance or implementation detail: 12-month audit retention over the TDD’s 90-day note, and 5 failed attempts in 15 minutes for lockout.

**Open risks requiring resolution before M1:**

- `OQ-002` leaves `UserProfile.roles` maximum length undefined; schema work must carry `TBD-pending-OQ-002` until auth-team closes the RBAC review.
- The TDD/PRD retention mismatch for audit logs must not leak into implementation; this roadmap commits to 12-month retention everywhere compliance storage is specified.

## MLS Summary

|ID|Title|Type|Priority|Effort|Dependencies|Deliverables|Risk|
|----|-------|------|----------|--------|--------------|--------------|------|
|M1|Foundation & Compliance Contracts|Foundation|P0|XL|PRD/TDD baseline, PostgreSQL 15+, Node.js 20, SEC-POLICY-001|19|High|
|M2|Core Auth & Session Control|Core Logic|P0|XL|M1, Redis 7+, RSA key material|21|High|
|M3|UX, Recovery & Audit Access|Integration|P0|XL|M2, SendGrid, frontend router|21|High|
|M4|Hardening, SLOs & Validation|Hardening|P1|L|M3, Prometheus, OpenTelemetry, k6|14|Medium|
|M5|Production Readiness & Rollout|Production Readiness|P0|XL|M4, Kubernetes, feature flag service, incident tooling|21|High|

## Dependency Graph

SEC-POLICY-001 -> {NFR-SEC-001, NFR-SEC-002, NFR-COMP-003, SEC-001, SEC-002, SEC-003}

Node.js 20 + PostgreSQL 15+ -> {DM-001, API-002, API-008, COMP-009, COMP-014, API-009, OPS-005}

Redis 7+ -> {DM-002, API-004, API-007, COMP-006, OPS-006, OPS-010}

SendGrid -> {API-005, COMP-011, COMP-016, COMP-017, R-PRD-004}

Prometheus + OpenTelemetry -> {OBS-005, OBS-006, OBS-007, OBS-008, OBS-009, OBS-010, OBS-011, NFR-PERF-001, NFR-REL-001}

M1 -> M2 -> M3 -> M4 -> M5

API-002 -> FR-AUTH-002 -> COMP-004 -> M3 user onboarding flow

API-001 + API-004 + API-007 -> COMP-004 -> session persistence, silent refresh, logout

API-008 + OBS-009 + OPS-007 -> NFR-REL-001 + MIG-002 + MIG-003

## M1: Foundation & Compliance Contracts

**Objective:** establish compliant schema, registration, baseline gateway controls, audit storage, and security invariants before tokenized auth expands surface area | **Duration:** W1-W2 (2026-03-30 to 2026-04-12, 2 weeks) | **Entry:** PRD/TDD baselined; PostgreSQL 15+ provisioned; SEC-POLICY-001 available | **Exit:** `UserProfile` and audit storage finalized except `roles` cap pending `OQ-002`; registration path and `/v1/auth/health` work end-to-end; baseline security/compliance tests pass

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-AUTH-002|Registration capability|Implement registration orchestration with validation, uniqueness, hashing, consent capture, and profile persistence.|AuthService|DM-001, API-002, COMP-005, COMP-008, COMP-009|201 returns `UserProfile`; duplicate email->409; weak password->400; bcrypt cost=12; consent recorded.|L|P0|
|2|NFR-SEC-001|Password hash standard|Enforce bcrypt cost factor 12 for registration and reset operations.|PasswordHasher|COMP-008|bcrypt cost=12 everywhere; unit assertion proves configured cost; no alternate algorithm enabled in v1.0.|M|P0|
|3|NFR-COMP-001|Registration consent capture|Record GDPR consent at registration without expanding stored profile PII.|AuthService|API-002, COMP-014|consent required before create; consent_timestamp recorded; consent event auditable; profile data remains minimal.|M|P0|
|4|NFR-COMP-003|Secret handling compliance|Guarantee one-way adaptive hashing and ban raw password persistence or logging.|AuthService|COMP-008, COMP-014|raw_password:not persisted; raw_password:not logged; stored_secret:bcrypt_hash_only; reset path uses same rule.|M|P0|
|5|NFR-COMP-004|Data minimization guardrail|Restrict collected identity data to the approved minimal set.|UserRepo|DM-001, API-002|allowed_profile_fields=email,displayName; stored_secret=hashed_password; extra PII rejected; logs redact secrets.|M|P0|
|6|DM-001|UserProfile schema|Define the PostgreSQL schema and interface for authenticated users.|UserRepo|OQ-002|id:UUIDv4+PK+notnull; email:lowercase+unique+indexed+notnull; displayName:2-100chars+notnull; createdAt:ISO8601+default_now+notnull; updatedAt:ISO8601+auto_updated+notnull; lastLoginAt:ISO8601+nullable; roles:string[]+default[user]+max:TBD-pending-OQ-002.|L|P0|
|7|API-002|POST `/v1/auth/register`|Implement the versioned registration endpoint contract.|Auth API|FR-AUTH-002, DM-001|method:POST; path:/v1/auth/register; auth:none; rate_limit:5/min/IP; req:email,password,displayName,consent; 201:id,email,displayName,createdAt,updatedAt,lastLoginAt=null,roles["user"]; 400 validation; 409 duplicate.|L|P0|
|8|API-008|GET `/v1/auth/health`|Add health endpoint for uptime checks, rollout gates, and SLO measurement.|Auth API|COMP-005|method:GET; path:/v1/auth/health; auth:none; 200:status=ok; checks:service,postgres,redis,key_readiness.|S|P1|
|9|COMP-005|AuthService facade|Build the backend orchestration facade for all auth flows.|AuthService|COMP-008, COMP-009, COMP-006, COMP-011|deps:TokenManager,PasswordHasher,UserRepo,EmailServiceAdapter; flows:login,register,getProfile,resetRequest,resetConfirm,logout; errors:uniform_JSON; no raw-secret logging.|L|P0|
|10|COMP-008|PasswordHasher|Build the password hashing abstraction over bcrypt.|PasswordHasher|-|alg:bcrypt; cost:12; ops:hash,verify; abstraction:future_migration_ready; plaintext:not persisted.|M|P0|
|11|COMP-009|UserRepo|Implement PostgreSQL data access for user records.|UserRepo|DM-001|deps:pg-pool; ops:create,findByEmail,findById,updateLastLogin,updatePassword,storeConsent; model:`UserProfile` CRUD.|L|P0|
|12|COMP-010|API Gateway policy layer|Configure route policies for auth ingress.|API Gateway|API-002, API-008|policies:rate_limit,CORS,TLS1.3,origin_allowlist; routes:/v1/auth/register,/v1/auth/health; lockout signals propagated.|M|P0|
|13|COMP-014|AuditLogStore|Define the PostgreSQL-backed audit event store with compliance retention.|AuditLogStore|OQ-CONFLICT-001|store:PostgreSQL15; events:login,registration,refresh,password_reset,lockout,logout; fields:userId,timestamp,ip,outcome,eventType; retention:12_months.|L|P0|
|14|SEC-002|Transport and CORS policy|Enforce transport and origin restrictions at the edge.|API Gateway|COMP-010|tls:1.3_only; cors:known_frontend_origins_only; insecure_origins rejected; policy errors observable.|M|P0|
|15|SEC-004|Reset token persistence contract|Define single-use reset token storage and invalidation semantics before flow implementation.|AuthService|COMP-014|token:single_use; ttl:1h; consume_once invalidates; lookup never reveals account existence.|M|P0|
|16|OBS-001|Login and lockout log schema|Implement structured log fields for login and lockout events.|AuthService|COMP-014|events:login_success,login_failure,account_locked; fields:userId|anon,timestamp,ip,outcome,reason,requestId; JSON stdout emitted.|M|P1|
|17|OBS-002|Registration and consent log schema|Implement structured log fields for registration and consent events.|AuthService|COMP-014|events:registration_attempt,registration_success,consent_recorded; fields:userId,timestamp,ip,outcome,consent_timestamp,requestId; JSON stdout emitted.|M|P1|
|18|TEST-004|Registration integration test|Validate register flow against real PostgreSQL storage.|Integration Tests|API-002, DM-001|scope:`AuthService`+PostgreSQL; request->hash->insert passes; duplicate email blocked; returned `UserProfile` matches schema.|M|P0|
|19|TEST-011|Security configuration validation|Verify baseline security defaults are encoded in configuration and code.|Security Tests|NFR-SEC-001, SEC-002, NFR-COMP-003|bcrypt cost=12 asserted; TLS1.3 enforced; CORS allowlist present; raw-password logging forbidden by test fixtures.|M|P0|

### Integration Points — M1

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|`AuthService` constructor injection|Dependency injection|`PasswordHasher`, `UserRepo`, `TokenManager`, `EmailServiceAdapter` interfaces frozen|M1|API handlers, tests|
|Gateway route registry|Route/policy binding|`/v1/auth/register` and `/v1/auth/health` bound to rate-limit, CORS, TLS policy|M1|External clients, uptime monitors|
|Audit event writer|Persistence wiring|`AuthService` event emission wired to `AuditLogStore` schema|M1|Compliance reporting, future alerts|
|Schema migration chain|Migration sequencing|`UserProfile` and audit tables migrate before service boot|M1|`UserRepo`, staging deploys|

### Risk Assessment and Mitigation — M1

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Implementation flaw in foundational auth code weakens all later milestones (`R-PRD-002`).|Critical|Low|System-wide security breach.|Front-load security invariants, config tests, and explicit secret-handling rules before token issuance work.|auth-team + sec-reviewer|
|2|Incomplete audit schema or short retention causes compliance rework (`R-PRD-003`).|High|Medium|SOC2 evidence gap and redesign later.|Commit to 12-month retention in M1 and make audit fields queryable from day one.|auth-team + compliance|
|3|Brute-force protections arrive too late for exposed registration/login paths (`R-002`).|Medium|High|Credential attack surface opens during rollout.|Bind rate limits and lockout semantics at gateway/service contracts in M1, not as late hardening.|auth-team + platform-team|

### Milestone Dependencies — M1

- PostgreSQL 15+ schema migration capability and backup policy must exist before `DM-001` and `COMP-014` are marked done.
- SEC-POLICY-001 must be available to finalize bcrypt, TLS, CORS, and secret-handling controls.
- `OQ-002` remains open; every artifact carrying `roles` must use `TBD-pending-OQ-002` until auth-team resolves the cap.
- Compliance sign-off on 12-month audit retention is required before M1 exits.

### Open Questions — M1

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-002|What is the maximum allowed `UserProfile.roles` array length? Source: TDD §22 and extraction Open Questions. Status: open; resolution: none yet, so roadmap uses `TBD-pending-OQ-002` in schema and token-related artifacts.|Schema validation and token-payload sizing remain provisional; M1 cannot claim final RBAC-ready contract.|auth-team|2026-04-01|
|2|OQ-PRD-003|Account lockout policy after N consecutive failed login attempts? Source: PRD Open Questions. Status: closed; resolution: adopt TDD §13 + FR-AUTH-001 value of 5 failed attempts within 15 minutes because the implementation detail is explicit there.|Prevents drift across gateway rate-limit messaging, service logic, and automated tests.|Security|TBD|
|3|OQ-CONFLICT-001|Audit log retention conflict: TDD §7.2/Operational Readiness notes 90 days while PRD Legal & Compliance requires 12-month retention. Status: closed; resolution: 12 months, with PRD compliance requirement taking precedence over the draft TDD note.|Storage sizing, purge jobs, and compliance validation use one retention value everywhere.|auth-team + compliance|TBD|

## M2: Core Auth & Session Control

**Objective:** implement credential login, token issuance, refresh, logout, profile retrieval, and core session-governance controls on top of the M1 schema and compliance baseline | **Duration:** W3-W4 (2026-04-13 to 2026-04-26, 2 weeks) | **Entry:** M1 complete; Redis 7+ available; RS256 key material provisioned | **Exit:** login, refresh, logout, and profile APIs work against PostgreSQL+Redis; session and token controls are wired; core auth unit/integration tests pass

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-AUTH-001|Login capability|Implement credential authentication with generic failure handling and lockout enforcement.|AuthService|API-001, COMP-005, COMP-008, COMP-013, COMP-006|200 returns `AuthToken`; invalid credentials->401; unknown email->401; lockout after 5 failures/15min; no user enumeration.|L|P0|
|2|FR-AUTH-003|Access and refresh token lifecycle|Implement token issuance and silent refresh flow with revocation support.|TokenManager|DM-002, API-004, COMP-006, COMP-007|login returns access(15m)+refresh(7d); refresh returns new pair; expired refresh->401; revoked refresh->401.|L|P0|
|3|FR-AUTH-004|Authenticated profile retrieval|Implement authenticated profile lookup for the current user.|AuthService|API-003, DM-001, COMP-012|GET `/v1/auth/me` with valid bearer token returns `UserProfile`; expired or invalid token->401; response includes id,email,displayName,createdAt,updatedAt,lastLoginAt,roles.|M|P0|
|4|NFR-SEC-002|RS256 token signing|Enforce RS256 signing with 2048-bit RSA keys and verification controls.|JwtService|COMP-007, SEC-POLICY-001|alg:RS256; key_size:2048bit_RSA; ops:sign,verify; clock_skew_tolerance:5s; rotation:quarterly documented.|M|P0|
|5|DM-002|AuthToken contract|Define the token payload and refresh-token record model.|TokenManager|OQ-002, OQ-PRD-002|accessToken:JWT+notnull+RS256+carries{id,roles}; refreshToken:opaque+unique+notnull+hashed_in_Redis; expiresIn:number+900+notnull; tokenType:string+Bearer+notnull.|L|P0|
|6|API-001|POST `/v1/auth/login`|Implement the login endpoint with lockout and rate-limit semantics.|Auth API|FR-AUTH-001, COMP-013|method:POST; path:/v1/auth/login; auth:none; rate_limit:10/min/IP; req:email,password; 200:accessToken,refreshToken,expiresIn=900,tokenType=Bearer; errors:401,429,423.|L|P0|
|7|API-003|GET `/v1/auth/me`|Implement bearer-authenticated profile retrieval.|Auth API|FR-AUTH-004, COMP-012|method:GET; path:/v1/auth/me; auth:Bearer accessToken; rate_limit:60/min/user; req_header:Authorization; 200:`UserProfile`; error:401 missing/expired/invalid token.|M|P0|
|8|API-004|POST `/v1/auth/refresh`|Implement refresh-token exchange and revocation of prior token.|Auth API|FR-AUTH-003, COMP-006|method:POST; path:/v1/auth/refresh; auth:none; rate_limit:30/min/user; req:refreshToken; 200:new `AuthToken` pair; error:401 expired_or_revoked.|L|P0|
|9|API-007|POST `/v1/auth/logout`|Add logout endpoint to satisfy the PRD end-session user story and revoke active refresh tokens.|Auth API|COMP-006, OQ-GAP-001|method:POST; path:/v1/auth/logout; auth:Bearer or refresh token; req:refreshToken?; 204:session ended; effects:revoke active refresh tokens and clear client session contract.|M|P0|
|10|COMP-006|TokenManager|Build the dual-token lifecycle service backed by Redis.|TokenManager|COMP-007, Redis 7+|deps:`JwtService`,Redis; ops:issueTokens,refresh,revoke,revokeAllForUser,hashRefreshToken; storage:hashed refresh tokens; lifecycle:dual token.|L|P0|
|11|COMP-007|JwtService|Build token signing and verification logic.|JwtService|SEC-POLICY-001|alg:RS256; key_size:2048; ops:sign,verify; skew_tolerance:5s; payload carries user id and roles.|M|P0|
|12|COMP-012|AuthGuard middleware|Implement bearer-token parsing and current-user context wiring for protected routes.|AuthGuard|COMP-007, API-003|ops:parse Authorization header,verify JWT,attach current user id/roles,return 401 on invalid token; consumes `/v1/auth/me` and internal protected handlers.|M|P0|
|13|COMP-013|LoginAttemptTracker|Implement failed-attempt counting and lockout windows.|LoginAttemptTracker|FR-AUTH-001|window:15min; threshold:5 failures; outcomes:increment,lock,reset_on_success; no user enumeration leakage.|M|P0|
|14|SEC-001|Client token storage policy|Codify XSS-resistant session handling for browser and API clients.|AuthProvider contract|FR-AUTH-003, R-001|accessToken:memory_only; refreshToken:HttpOnly_cookie_or_secure client vault; clear_on_tab_close for browser; revoke on security event.|M|P0|
|15|SEC-003|Lockout and brute-force control|Implement service-side lockout behavior aligned with gateway rate limits.|AuthService|COMP-013, API-001|lockout:5 failures/15min; 423 on locked account; login failure path generic; WAF/CAPTCHA escalation hooks exposed.|M|P0|
|16|OBS-003|Token lifecycle logging|Instrument token issuance, refresh, revocation, and logout events.|TokenManager|COMP-014, API-004, API-007|events:token_issued,token_refreshed,token_revoked,logout; fields:userId,timestamp,ip,outcome,requestId; JSON stdout emitted.|M|P1|
|17|OBS-004|Auth access tracing|Add tracing and structured access logs for login, me, and refresh flows.|AuthService|COMP-005, COMP-006, COMP-007|spans:AuthService.login,getProfile; TokenManager.issueTokens,refresh; JwtService.sign,verify; trace context propagated end-to-end.|M|P1|
|18|TEST-001|Valid-login unit test|Verify successful login orchestration returns a valid token pair.|Unit Tests|FR-AUTH-001, COMP-005|`AuthService.login()` calls `PasswordHasher.verify()` then `TokenManager.issueTokens()` and returns valid `AuthToken`.|S|P0|
|19|TEST-002|Invalid-login unit test|Verify invalid credentials do not issue tokens and preserve generic failures.|Unit Tests|FR-AUTH-001, COMP-005|verify false -> 401; no `AuthToken`; no user enumeration-specific branch leaks.|S|P0|
|20|TEST-003|Refresh unit test|Verify refresh revokes the old token and issues a new pair.|Unit Tests|FR-AUTH-003, COMP-006|valid refresh token -> revoke old + issue new `AuthToken` via `JwtService`.|S|P0|
|21|TEST-005|Expired-refresh integration test|Verify Redis TTL expiration rejects expired refresh tokens.|Integration Tests|API-004, COMP-006|Redis TTL expiry invalidates token; refresh returns 401; old token cannot be reused.|M|P0|

### Integration Points — M2

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|Bearer middleware chain|Middleware binding|`AuthGuard` wired before `/v1/auth/me` and logout handlers|M2|Protected API routes|
|Token service registry|Dependency injection|`AuthService` wired to `TokenManager`; `TokenManager` wired to `JwtService` + Redis|M2|Login, refresh, logout flows|
|Lockout state adapter|Callback/state binding|login failures update `LoginAttemptTracker`; success resets counters|M2|`/v1/auth/login`, alerting|
|Refresh-token revocation hook|Strategy wiring|logout and reset-confirm use shared revoke-all strategy|M2|Logout, password reset, incident response|

### Risk Assessment and Mitigation — M2

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Token theft through insecure client storage enables hijacking (`R-001`).|High|Medium|Account takeover and session abuse.|Enforce in-memory access tokens, revocable refresh tokens, short TTLs, and explicit logout/revoke flows.|frontend-team + auth-team|
|2|Brute-force attempts overwhelm login path or bypass lockout (`R-002`).|Medium|High|Credential stuffing and user lock fatigue.|Combine API rate limits, attempt tracking, lockout windows, and clear monitoring hooks.|auth-team + platform-team|
|3|Session-governance ambiguity around multi-device refresh tokens causes security or UX churn.|Medium|Medium|Late behavior changes in token storage and logout semantics.|Implement revocation strategy hooks now and keep per-user token cap configurable behind `OQ-PRD-002`.|auth-team|

### Milestone Dependencies — M2

- Redis 7+ with stable connectivity and TTL behavior is required for `DM-002`, `API-004`, `API-007`, and `TEST-005`.
- RS256 signing keys must be provisioned and mountable before `COMP-007` and `NFR-SEC-002` can exit.
- `DM-001` remains source of truth for `roles`; token payload work inherits `TBD-pending-OQ-002` until the cap is decided.
- Logout and revoke-all semantics must stay aligned with later password-reset invalidation work in M3.

### Open Questions — M2

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-001|Should `AuthService` support API key authentication for service-to-service calls? Source: TDD §22 and extraction Open Questions. Status: closed; resolution: defer to v1.1 because v1.0 scope is email/password + refresh-token auth, and programmatic refresh already covers the committed v1.0 Sam persona path.|Prevents scope creep into a second auth mechanism during the critical-path token milestone.|test-lead|2026-04-15|
|2|OQ-PRD-002|Maximum number of refresh tokens allowed per user across devices? Source: PRD Open Questions. Status: open; resolution: none yet, so `TokenManager` must keep per-user token-cap enforcement configurable as `TBD-pending-OQ-PRD-002` while preserving multi-device sessions.|Affects Redis sizing, logout semantics, and session-revocation UX for multi-device users.|Product|TBD|
|3|OQ-GAP-001|PRD user story requires logout, but the TDD omits a logout endpoint. Status: closed; resolution: add `API-007 POST /v1/auth/logout` in v1.0 because PRD requires end-session behavior; TDD should be updated.|Keeps roadmap coverage aligned with PRD AUTH-E1 without forcing hidden client-only logout behavior.|Product + auth-team|TBD|

## M3: UX, Recovery & Audit Access

**Objective:** integrate frontend routes, silent-session UX, password reset, compliance-grade audit visibility, and PRD-implied recovery flows on top of the M2 APIs | **Duration:** W5-W6 (2026-04-27 to 2026-05-10, 2 weeks) | **Entry:** M2 complete; SendGrid available; frontend routing foundation ready | **Exit:** login/register/profile/reset journeys work end-to-end; audit events are queryable for admins/internal tooling; password reset invalidates active sessions and remains anti-enumeration safe

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-AUTH-005|Password reset capability|Implement request/confirm reset flow with anti-enumeration, expiry, single use, and session invalidation.|AuthService|API-005, API-006, COMP-011, SEC-004, API-007|reset-request sends token; reset-confirm updates hash; token TTL=1h; token single-use; password change invalidates all existing sessions.|L|P0|
|2|NFR-COMP-002|SOC2 audit logging|Implement complete auth-event logging with 12-month retention and query support.|AuditLogStore|COMP-014, API-009|events include userId,timestamp,ip,outcome,eventType; retention=12 months; queryable by user and date range.|L|P0|
|3|API-005|POST `/v1/auth/reset-request`|Implement anti-enumeration reset-request endpoint with email dispatch contract.|Auth API|FR-AUTH-005, COMP-011|method:POST; path:/v1/auth/reset-request; auth:none; req:email; behavior:uniform response regardless of account existence; token TTL=1h; delivery via SendGrid; anti-enumeration preserved.|L|P0|
|4|API-006|POST `/v1/auth/reset-confirm`|Implement reset confirmation endpoint with single-use token validation and session revocation.|Auth API|FR-AUTH-005, SEC-004, API-007|method:POST; path:/v1/auth/reset-confirm; auth:none; req:token,newPassword; behavior:validate token,update hash,revoke all sessions; errors:400/401 on invalid_or_expired_or_used token.|L|P0|
|5|API-009|GET `/v1/auth/audit-events`|Add internal audit-query endpoint required by the PRD admin persona and compliance workflows.|Audit API|COMP-014, OQ-GAP-002|method:GET; path:/v1/auth/audit-events; auth:internal_admin_only; query:userId?,dateFrom?,dateTo?,eventType?,outcome?; resp:paginated audit events with userId,timestamp,ip,outcome,eventType; errors:400,401,403.|M|P1|
|6|COMP-001|LoginPage|Implement the public login route using the new login API.|LoginPage|API-001, COMP-004|route:/login; auth:public; props:onSuccess(),redirectUrl?; fields:email,password; submit:POST `/v1/auth/login`; success stores `AuthToken` via `AuthProvider`.|M|P0|
|7|COMP-002|RegisterPage|Implement the public registration route with inline validation and consent UX.|RegisterPage|API-002, COMP-004|route:/register; auth:public; props:onSuccess(),termsUrl; fields:email,password,displayName,consent; client_validation:password>=8+uppercase+number; submit:POST `/v1/auth/register`; success:auto-login then redirect to dashboard.|M|P0|
|8|COMP-003|ProfilePage|Implement the protected profile route backed by `/v1/auth/me`.|ProfilePage|API-003, COMP-019|route:/profile; auth:required; renders:id,email,displayName,createdAt,lastLoginAt,roles; source:GET `/v1/auth/me`.|M|P0|
|9|COMP-004|AuthProvider|Implement shared auth state, silent refresh, 401 interception, and auth method exposure.|AuthProvider|API-001, API-004, API-007, API-003|props:children:ReactNode; state:`AuthToken`,`UserProfile`; ops:silent_refresh,intercept_401,redirect_unauthenticated,logout; hierarchy:App->AuthProvider->PublicRoutes/ProtectedRoutes.|L|P0|
|10|COMP-011|EmailServiceAdapter|Implement SendGrid-backed reset email dispatch with async delivery and monitoring hooks.|EmailServiceAdapter|SendGrid, OQ-PRD-001|provider:SendGrid; ops:sendResetEmail; mode:async; payload:email,token,expiresAt; retries/monitoring hooks exposed.|M|P0|
|11|COMP-016|ForgotPasswordPage|Add the PRD-implied reset-request page invoked from the login journey.|ForgotPasswordPage|API-005, OQ-GAP-003|route:/forgot-password; auth:public; fields:email; submit:POST `/v1/auth/reset-request`; confirmation uniform for registered and unregistered email.|M|P1|
|12|COMP-017|ResetPasswordPage|Add the PRD-implied reset-confirm page for token-based password updates.|ResetPasswordPage|API-006, OQ-GAP-003|route:/reset-password; auth:public; fields:token,newPassword,confirmPassword; submit:POST `/v1/auth/reset-confirm`; expired/used token shows recovery action.|M|P1|
|13|COMP-018|PublicRoutes|Implement public-route grouping under the shared provider hierarchy.|PublicRoutes|COMP-001, COMP-002, COMP-016, COMP-017|children:LoginPage,RegisterPage,ForgotPasswordPage,ResetPasswordPage; auth:public; wired under `AuthProvider`.|S|P2|
|14|COMP-019|ProtectedRoutes|Implement protected-route wrapper for authenticated navigation.|ProtectedRoutes|COMP-003, COMP-004|children:ProfilePage; auth:required; redirects unauthenticated users to `LoginPage`; preserves intended destination when possible.|S|P1|
|15|OBS-005|Password reset event logs|Instrument reset-request and reset-confirm logging with compliance fields.|AuthService|API-005, API-006, COMP-014|events:password_reset_requested,password_reset_completed,password_reset_rejected; fields:userId|anon,timestamp,ip,outcome,requestId.|M|P1|
|16|OBS-006|Audit query access logs|Instrument access logs for internal audit-log queries.|Audit API|API-009|events:audit_query_requested,audit_query_completed; fields:actorId,timestamp,filters,outcome,requestId; sensitive payloads redacted.|S|P2|
|17|TEST-006|Registration-to-profile E2E|Validate full onboarding and authenticated profile journey through the UI.|E2E Tests|COMP-001, COMP-002, COMP-003, COMP-004|flow:`RegisterPage`->`LoginPage`->`ProfilePage`; `AuthProvider` stores tokens; profile data renders correctly.|M|P0|
|18|TEST-007|Reset-request anti-enumeration test|Verify reset requests return uniform responses regardless of email existence.|Integration Tests|API-005|registered and unregistered emails return same outward response; email send only for existing account; no enumeration leak.|M|P0|
|19|TEST-008|Reset-confirm revocation test|Verify password reset invalidates active sessions across devices.|Integration Tests|API-006, API-007|successful reset changes hash; all refresh tokens revoked; subsequent refresh/logout on old sessions fail.|M|P0|
|20|TEST-009|Logout flow test|Verify logout revokes the current session and redirects users appropriately.|E2E Tests|API-007, COMP-004|logout ends session immediately; redirect to landing/login; revoked token cannot refresh afterward.|S|P1|
|21|TEST-010|Audit query contract test|Verify audit-event query returns compliant fields and filters correctly.|Integration Tests|API-009, NFR-COMP-002|response items include userId,timestamp,ip,outcome,eventType; filters by user/date range work; unauthorized access rejected.|M|P1|

### Integration Points — M3

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|App route tree|Route binding|`AuthProvider` wraps `PublicRoutes` and `ProtectedRoutes` with `/login`, `/register`, `/profile`, `/forgot-password`, `/reset-password`|M3|Frontend users|
|401 interceptor|Callback wiring|HTTP client interceptor triggers silent refresh or redirect via `AuthProvider`|M3|Protected frontend flows|
|Reset email dispatch pipeline|Async callback/queue wiring|`AuthService.resetRequest()` emits work to `EmailServiceAdapter` with monitoring hooks|M3|Password recovery flow|
|Audit query service|Internal API binding|`AuditLogStore` read path exposed through internal-only `GET /v1/auth/audit-events`|M3|Jordan admin workflows, compliance tooling|

### Risk Assessment and Mitigation — M3

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Poor onboarding UX suppresses registration conversion (`R-PRD-001`).|High|Medium|Business-value delay despite functional auth service.|Ship inline validation, consent UX, and full E2E path before hardening and rollout.|frontend-team + product-team|
|2|Email delivery failure blocks password recovery (`R-PRD-004`).|Medium|Low|Users cannot regain access and support load spikes.|Use async SendGrid adapter, monitor delivery, preserve fallback support path, and test anti-enumeration behavior.|auth-team + platform-team|
|3|Incomplete admin/audit access leaves Jordan persona unmet and weakens compliance readiness (`R-PRD-003`).|High|Medium|Incident investigation remains manual and audit evidence incomplete.|Add audit query path plus access logs in the same milestone as reset and profile UX.|auth-team + compliance|

### Milestone Dependencies — M3

- SendGrid availability is required for `COMP-011`, `API-005`, and password-reset E2E validation.
- Frontend routing and shared provider composition must be stable before `PublicRoutes`, `ProtectedRoutes`, and page-level components can exit.
- Audit-query access depends on `COMP-014` retaining 12-month event data from earlier milestones.
- Logout revocation semantics from M2 are prerequisites for the PRD-required reset invalidates-all-sessions behavior.

### Open Questions — M3

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-PRD-001|Should password reset emails be sent synchronously or asynchronously? Source: PRD Open Questions. Status: closed; resolution: asynchronous delivery via `EmailServiceAdapter`, because it preserves anti-enumeration, isolates external latency, and still supports the PRD/TDD delivery SLA expectations.|Keeps reset-request latency predictable and prevents SendGrid slowness from directly degrading auth API p95.|Engineering|TBD|
|2|OQ-PRD-004|Should we support "remember me" to extend session duration? Source: PRD Open Questions. Status: closed; resolution: defer beyond v1.0 because the committed session model is 15-minute access token + 7-day refresh window and the TDD/PRD scope does not require a second persistence mode.|Avoids introducing a second session policy that would complicate security review and rollout inside the fixed v1.0 schedule.|Product|TBD|
|3|OQ-GAP-002|PRD requires Jordan to query auth events by user and date range, but the TDD omits an admin-facing audit query contract. Status: closed; resolution: add `API-009 GET /v1/auth/audit-events` in v1.0 for internal admin/compliance use; TDD should be updated.|Closes the Jordan persona gap without expanding RBAC enforcement scope for end users.|Product + auth-team|TBD|
|4|OQ-GAP-003|PRD password-reset journey requires dedicated forgot/reset pages, but the TDD component list omits them. Status: closed; resolution: add `COMP-016 ForgotPasswordPage` and `COMP-017 ResetPasswordPage`; TDD should be updated.|Ensures end-to-end recovery is implementable in the UI rather than implied only by backend endpoints.|Product + frontend-team|TBD|

## M4: Hardening, SLOs & Validation

**Objective:** wire production-grade observability, alerts, tracing, and non-functional validation so the service can prove its latency, concurrency, and availability promises before live rollout | **Duration:** W7-W8 (2026-05-11 to 2026-05-24, 2 weeks) | **Entry:** M3 complete; Prometheus, OpenTelemetry, and k6 available in staging | **Exit:** metrics, traces, and alerts are emitting; performance and reliability evidence confirms readiness for phased rollout; security review package is complete

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|NFR-PERF-001|Endpoint latency target|Validate and optimize all auth endpoints to remain below the required p95 latency budget.|AuthService|OPS-007, OBS-008, TEST-012|all auth endpoints p95 <200ms; measured via APM/tracing; regressions surfaced before rollout.|L|P0|
|2|NFR-PERF-002|Concurrent login capacity|Demonstrate support for 500 concurrent login requests under load.|AuthService|TEST-012|500 concurrent login requests sustained; no unacceptable error amplification; results captured for go/no-go.|M|P0|
|3|NFR-REL-001|Availability objective|Implement monitoring and evidence collection for 99.9% rolling availability.|Platform SRE|API-008, OPS-008, OPS-009, OPS-010|health checks monitored; availability target 99.9% over 30-day windows; alert paths verified.|M|P0|
|4|OPS-007|Prometheus auth metrics|Expose the required auth Prometheus metrics set for service monitoring.|Observability|OBS-007, OBS-008, OBS-009, OBS-010|metrics:`auth_login_total`,`auth_login_duration_seconds`,`auth_token_refresh_total`,`auth_registration_total`; labels documented; scrape target live.|M|P0|
|5|OPS-008|Login failure alert|Configure and verify alerting for elevated login failure rates.|Alerting|OBS-007|trigger:login failure rate >20% over 5m; route:on-call; noise tested against expected lockout traffic.|S|P1|
|6|OPS-009|Latency breach alert|Configure and verify alerting for p95 latency breaches.|Alerting|OBS-008|trigger:p95 latency >500ms; route:on-call; dashboard links point to traces and logs.|S|P1|
|7|OPS-010|Redis failure alert|Configure and verify alerting for `TokenManager` Redis failures.|Alerting|OBS-009|trigger:`TokenManager` Redis connection failures; route:on-call; runbook linked.|S|P1|
|8|OBS-007|`auth_login_total` instrumentation|Instrument login success/failure counters in service code.|AuthService|API-001|counter:`auth_login_total`; labels:outcome,reason?; increments on success,failure,lockout paths.|S|P1|
|9|OBS-008|`auth_login_duration_seconds` instrumentation|Instrument login latency histogram in service code.|AuthService|API-001|histogram:`auth_login_duration_seconds`; spans full login path; p95 derivable from exported buckets.|S|P1|
|10|OBS-009|`auth_token_refresh_total` instrumentation|Instrument refresh counters in `TokenManager` and refresh endpoint path.|TokenManager|API-004|counter:`auth_token_refresh_total`; labels:outcome; increments on success,expired,revoked,redis_error paths.|S|P1|
|11|OBS-010|`auth_registration_total` instrumentation|Instrument registration counters in service code.|AuthService|API-002|counter:`auth_registration_total`; labels:outcome; increments on success,validation_error,duplicate_email paths.|S|P1|
|12|OBS-011|Distributed tracing chain|Implement end-to-end tracing across auth components and external calls.|AuthService|COMP-005, COMP-008, COMP-006, COMP-007, COMP-011|spans:`AuthService`->`PasswordHasher`->`TokenManager`->`JwtService` plus SendGrid call; trace context propagated; errors annotated.|M|P1|
|13|TEST-012|Performance and load suite|Run k6/APM performance suite covering login, register, refresh, and reset traffic profiles.|Performance Tests|NFR-PERF-001, NFR-PERF-002|load tests capture p95 latency, throughput, error rate; 500-concurrent login scenario included; artifacts saved for release review.|M|P0|
|14|TEST-013|Security and reliability evidence pack|Assemble validation evidence for security review and uptime readiness.|QA + Security Review|NFR-REL-001, NFR-SEC-002, OPS-008, OPS-009, OPS-010|bcrypt cost verified; RS256 rotation documented; alert routes exercised; health monitoring and failure drills recorded.|M|P0|

### Integration Points — M4

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|Prometheus exporter registry|Metrics binding|service metrics registered and scraped from auth pods|M4|Grafana dashboards, alert rules|
|OpenTelemetry middleware|Middleware/trace binding|request spans wrap auth handlers and propagate into hashing, token, and email services|M4|APM, debugging, rollout gates|
|Alert rule set|Alert configuration|login, latency, and Redis alerts bound to paging channels and runbooks|M4|auth-team on-call, platform-team|
|Load-test harness|Validation binding|k6 scenarios target staging routes and compare against SLO thresholds|M4|release review, go/no-go meeting|

### Risk Assessment and Mitigation — M4

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Security defects remain latent without hard evidence (`R-PRD-002`).|Critical|Low|Production breach risk survives feature completion.|Require explicit security evidence pack, key-rotation docs, and observability coverage before rollout starts.|sec-reviewer + auth-team|
|2|Incomplete monitoring misses audit or performance regressions (`R-PRD-003`).|High|Medium|Rollout proceeds without actionable detection.|Instrument metrics in code and verify alert/routing behavior before any traffic shift.|auth-team + platform-team|
|3|Concurrency or latency ceilings fail only under live load.|Medium|Medium|Beta rollout instability and emergency rollback.|Run k6/APM tests with the exact 500-concurrent and p95 thresholds from the TDD/PRD before M5.|qa-team + auth-team|

### Milestone Dependencies — M4

- Prometheus scrape targets and OpenTelemetry collectors must be available in staging before `OPS-007` and `OBS-011` can be completed.
- Load tests must run against M3-complete flows, including reset and logout, to avoid false confidence on partial routes.
- Alert destinations must be wired to the on-call chain defined for M5 operational readiness.
- Release review cannot treat M4 complete until the evidence pack covers latency, concurrency, security configuration, and alert verification.

## M5: Production Readiness & Rollout

**Objective:** execute phased rollout, operationalize runbooks and capacity controls, verify rollback readiness, and complete the production handoff without exceeding the committed v1.0 date | **Duration:** W9-W10+2d (2026-05-25 to 2026-06-09, 16 days) | **Entry:** M4 evidence approved; Kubernetes/HPA and incident tooling ready; feature flags configured | **Exit:** internal alpha, beta, and GA are executed or ready for execution with rollback proven, on-call staffed, and production dashboards green through the TDD end date

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|MIG-001|Phase 1 internal alpha|Run internal alpha deployment and validation behind the new-login flag.|Release Management|COMP-020, TEST-018|duration:1_week; audience:auth-team+QA; deploy staging/internal; enable `AUTH_NEW_LOGIN` internal-only; exit:FR-AUTH-001..005 manual pass, zero P0/P1 bugs.|M|P0|
|2|MIG-002|Phase 2 beta 10%|Roll out to 10% production traffic with focused telemetry review.|Release Management|MIG-001, TEST-012|duration:2_weeks; audience:10% traffic; monitor latency,error_rate,Redis_usage; exit:p95<200ms,error_rate<0.1%,no Redis connection failures.|L|P0|
|3|MIG-003|Phase 3 GA 100%|Promote to full production traffic and retire legacy traffic path.|Release Management|MIG-002, COMP-020|duration:1_week; audience:100%; remove `AUTH_NEW_LOGIN`; deprecate legacy endpoints; enable `AUTH_TOKEN_REFRESH`; exit:99.9% uptime first 7 days, dashboards green.|L|P0|
|4|MIG-004|Feature flag `AUTH_NEW_LOGIN`|Define, own, and clean up the primary new-login rollout flag.|Feature Flags|COMP-020|default:OFF; owner:auth-team; purpose:gates `LoginPage` + `AuthService` login endpoint; cleanup:after Phase 3 GA.|S|P0|
|5|MIG-005|Feature flag `AUTH_TOKEN_REFRESH`|Define, own, and clean up the refresh-flow rollout flag.|Feature Flags|COMP-020|default:OFF; owner:auth-team; purpose:enables refresh token flow; when OFF only access tokens issued; cleanup:after Phase 3 + 2 weeks.|S|P0|
|6|MIG-006|Rollback step 1|Implement and verify the immediate flag-based traffic fallback step.|Rollback Playbook|MIG-004|action:disable `AUTH_NEW_LOGIN`; effect:route traffic back to legacy auth; execution time meets incident expectations.|S|P0|
|7|MIG-007|Rollback step 2|Implement and verify legacy-login smoke validation after fallback.|Rollback Playbook|MIG-006, TEST-017|action:verify legacy login flow operational via smoke tests; pass/fail surfaced to incident channel.|S|P0|
|8|MIG-008|Rollback step 3|Operationalize root-cause investigation using logs and traces.|Rollback Playbook|OBS-011|action:investigate `AuthService` failure via structured logs + traces; owners and evidence sources documented.|S|P1|
|9|MIG-009|Rollback step 4|Operationalize backup restore for `UserProfile` corruption scenarios.|Rollback Playbook|OPS-005|action:restore from last known-good backup if `UserProfile` corruption detected; restore drill documented.|M|P0|
|10|MIG-010|Rollback step 5|Operationalize incident communication for auth rollback events.|Incident Response|OPS-003|action:notify auth-team + platform-team via incident channel; templates and contact paths preloaded.|S|P1|
|11|MIG-011|Rollback step 6|Operationalize postmortem completion after rollback events.|Incident Response|MIG-010|action:postmortem within 48h of rollback; owners, template, and evidence inputs defined.|S|P1|
|12|OPS-001|Runbook: AuthService down|Publish and verify the runbook for full auth service outage handling.|Runbooks|OBS-011, API-008|scenario:`AuthService` down; symptoms:5xx on `/auth/*`, UI error state; diagnosis:K8s health,PG connectivity,init logs; resolution:restart pods/failover/re-login; escalation:auth-team->platform-team after 15m.|M|P0|
|13|OPS-002|Runbook: token refresh failures|Publish and verify the runbook for refresh-path instability.|Runbooks|OPS-010, OBS-009|scenario:token refresh failures; symptoms:unexpected logout,redirect loop,error spike; diagnosis:Redis,key access,flag state; resolution:scale Redis,re-mount secrets,enable flag; escalation documented.|M|P0|
|14|OPS-003|On-call expectations|Staff and document the production support model for launch.|On-call|MIG-001, MIG-002, MIG-003|P1 ack within 15m; 24/7 auth-team rotation first 2 weeks post-GA; tooling:K8s dashboards,Grafana,Redis CLI,PG admin; escalation path:auth-team->test-lead->eng-manager->platform-team.|M|P0|
|15|OPS-004|AuthService pod capacity plan|Operationalize HPA-backed pod scaling for expected concurrency.|Capacity Planning|NFR-PERF-002|current:3 replicas; expected:500 concurrent users; scale:HPA to 10 replicas at CPU >70%.|S|P1|
|16|OPS-005|PostgreSQL capacity plan|Operationalize database-connection scaling and restore readiness.|Capacity Planning|DM-001|current_pool:100; avg_queries:50 concurrent; scale_to:200 if wait_time>50ms; backup/restore path verified.|S|P1|
|17|OPS-006|Redis memory plan|Operationalize Redis sizing for refresh-token storage.|Capacity Planning|DM-002, OQ-PRD-002|current:1GB; expected:~100K refresh tokens (~50MB); scale_to:2GB at >70% utilization.|S|P1|
|18|COMP-020|FeatureFlagController|Implement rollout-flag wiring used by alpha/beta/GA and rollback flows.|FeatureFlagController|MIG-004, MIG-005|flags:`AUTH_NEW_LOGIN`,`AUTH_TOKEN_REFRESH`; ops:read,evaluate,flip,audit; consumed by login,refresh,rollout tooling.|M|P0|
|19|COMP-021|Rollout dashboard|Assemble the release dashboard linking metrics, traces, alerts, and rollback triggers.|Rollout Dashboard|OPS-007, OPS-008, OPS-009, OPS-010|views:latency,error_rate,Redis_failures,traffic_split,availability; links to runbooks and incident channel.|M|P1|
|20|TEST-017|Rollback drill|Exercise the rollback sequence in staging before production traffic shifts.|Release Validation|MIG-006, MIG-007, MIG-008, MIG-009|flag fallback works; legacy smoke suite passes; restore path rehearsed; communication and postmortem templates validated.|M|P0|
|21|TEST-018|GA smoke suite|Run the final smoke suite across login, register, me, refresh, logout, and reset during each rollout phase.|Release Validation|MIG-001, MIG-002, MIG-003|flows:register,login,me,refresh,logout,reset-request,reset-confirm; results recorded per phase; blockers page owners immediately.|M|P0|

### Integration Points — M5

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|Feature flag service|Strategy/flag binding|`AUTH_NEW_LOGIN` and `AUTH_TOKEN_REFRESH` bound to auth routes and rollout control panel|M5|Release managers, `AuthService`, `AuthProvider`|
|Incident channel automation|Notification binding|rollback and alert events route to auth-team/platform-team channel templates|M5|On-call responders|
|Runbook-to-dashboard links|Operational binding|dashboard panels deep-link to `OPS-001` and `OPS-002` procedures|M5|Auth-team, platform-team|
|Rollback validation suite|Test harness binding|staging rollback drill reuses smoke tests and restore checks before production shifts|M5|Release managers, QA|

### Risk Assessment and Mitigation — M5

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Migration rollout causes user-impacting regressions or data loss (`R-003`).|High|Low|Rollback, restore, and trust erosion.|Use phased rollout, pre-phase backups, idempotent data handling, and staged rollback drills before GA.|auth-team + platform-team|
|2|Email or Redis instability during rollout degrades recovery or session persistence (`R-PRD-004`).|Medium|Low|Unexpected logout and blocked resets during beta/GA.|Track dedicated alerts, runbooks, and dashboard visibility before and during traffic increases.|platform-team + auth-team|
|3|Operational readiness gaps leave incidents uncontained in the first GA week.|High|Medium|Longer outages and slower customer recovery.|Require staffed on-call rotation, verified runbooks, and explicit rollback triggers before GA.|eng-manager + auth-team|

### Milestone Dependencies — M5

- Kubernetes deployment controls, HPA, and incident tooling must be live before alpha starts.
- Feature flags must be independently switchable and auditable before beta and GA.
- Rollback drill completion is a gate for external traffic shifts.
- Beta and GA decisions depend on M4 evidence plus live dashboard confirmation during each phase.

## Resource Requirements and Dependencies

### External Dependencies

|Dependency|Required By MLS|Status|Fallback|
|---|---|---|---|
|PostgreSQL 15+|M1, M2, M3, M5|Required|Restore from last known-good backup; hold rollout if migration health is unclear.|
|Redis 7+|M2, M4, M5|Required|Reject refresh requests and force re-login while incident response restores cache health.|
|Node.js 20 LTS|M1-M5|Required|No supported fallback; release blocked until runtime compliance is restored.|
|`bcryptjs`|M1, M2, M4|Required|No algorithm substitution in v1.0; release blocked if bcrypt cost-12 support is unavailable.|
|`jsonwebtoken`|M2, M4|Required|No supported fallback; token issuance blocked until RS256-compatible library path is healthy.|
|SendGrid API|M3, M5|Required|Fallback to support-assisted recovery channel; reset-request endpoint remains anti-enumeration safe.|
|Frontend routing framework|M3|Required|Minimal route wiring without advanced navigation state if framework features slip.|
|SEC-POLICY-001|M1, M2, M4|Required|Security review cannot complete without it; rollout blocked.|
|Feature flag service|M5|Required|Manual config toggles only as emergency fallback during rollback drill, not as default rollout control.|
|Prometheus + OpenTelemetry|M4, M5|Required|Reduced log-only visibility; beta/GA should not proceed without restored telemetry.|

### Infrastructure Requirements

- PostgreSQL storage sized for `UserProfile`, audit logs with 12-month retention, and backup/restore rehearsal.
- Redis capacity sized for at least ~100K refresh tokens with room for `OQ-PRD-002` growth once the device cap is resolved.
- Kubernetes HPA support for auth pods scaling from 3 to 10 replicas at CPU >70%.
- Secret-management support for quarterly RS256 key rotation and runtime key mounts.
- Staging environment with production-like PostgreSQL, Redis, telemetry, and feature-flag behavior.

## Risk Register

|ID|Risk|Affected Milestones|Probability|Impact|Mitigation|Owner|
|----|------|---------------------|-------------|--------|------------|-------|
|R-001|Token theft via XSS allows session hijacking.|M2, M3, M4, M5|Medium|High|In-memory access tokens, revocable refresh tokens, short TTLs, explicit logout/reset invalidation, and alert-backed investigation paths.|frontend-team + auth-team|
|R-002|Brute-force attacks on login endpoint.|M1, M2, M4|High|Medium|Gateway rate limiting, login-attempt tracking, 5-failures/15-min lockout, monitoring hooks, and WAF/CAPTCHA escalation path.|auth-team + platform-team|
|R-003|Data loss during migration from legacy auth.|M5|Low|High|Phased rollout, backups before phases, idempotent data handling, rollback drills, and restore procedure validation.|auth-team + platform-team|
|R-PRD-001|Low registration adoption due to poor UX.|M3, M5|Medium|High|Inline validation, complete onboarding journey testing, funnel instrumentation, and fast post-beta iteration path.|frontend-team + product-team|
|R-PRD-002|Security breach from implementation flaws.|M1, M2, M4|Low|Critical|Front-load security controls, maintain evidence-backed validation, and require security review before rollout.|sec-reviewer + auth-team|
|R-PRD-003|Compliance failure from incomplete audit logging.|M1, M3, M4|Medium|High|Define audit schema early, retain 12 months, expose compliant query paths, and validate against SOC2 requirements.|auth-team + compliance|
|R-PRD-004|Email delivery failures blocking password reset.|M3, M5|Low|Medium|Async email adapter, delivery monitoring, fallback support channel, and reset-specific smoke tests.|platform-team + auth-team|

## Success Criteria and Validation Approach

|Criterion|Metric|Target|Validation Method|MLS|
|---|---|---|---|---|
|Login latency target|Login response time p95|< 200ms|APM traces + k6 results against `/v1/auth/login`.|M4|
|Registration success rate|Successful registrations / attempts|> 99%|Registration funnel analytics and integration-test trend checks.|M3, M4|
|Refresh latency target|Token refresh latency p95|< 100ms|APM traces on `TokenManager.refresh()` under staged load.|M4|
|Availability objective|Rolling service availability|99.9% uptime|Health-check monitoring and release dashboard evidence.|M4, M5|
|Hashing budget|`PasswordHasher.hash()` time|< 500ms|Benchmark suite at bcrypt cost 12 in staging hardware profile.|M4|
|Onboarding conversion|User registration conversion|> 60%|`RegisterPage` funnel from landing -> register -> confirmed account.|M3, M5|
|Authenticated adoption|Daily active authenticated users|> 1000 within 30 days of GA|Token issuance and session analytics after GA.|M5|
|Functional completeness|FR-AUTH-001 through FR-AUTH-005|Implemented with passing tests|Traceability review against deliverable rows and automated suites.|M1-M4|
|Unit coverage gate|Coverage for `AuthService`,`TokenManager`,`JwtService`,`PasswordHasher`|>80%|Coverage report in CI and release evidence pack.|M4|
|Integration API gate|Integration tests for all four core API endpoints|Pass against real PostgreSQL + Redis|Supertest/testcontainers suite plus staging validation.|M2-M4|
|Security review gate|bcrypt cost verified; RS256 key rotation documented|Complete|Security-review checklist and evidence pack.|M4|
|Performance gate|Auth endpoints under load|<200ms p95 under 500 concurrent users|k6 load suite and trace review.|M4|
|Engagement proxy|Average session duration|> 30 minutes|Refresh-token analytics and session telemetry after beta/GA.|M5|
|Recovery usability|Password reset completion|> 80%|Reset funnel: requested -> completed, plus support-ticket trend.|M3, M5|

## Decision Summary

|Decision|Chosen|Alternatives Considered|Rationale|
|----------|--------|------------------------|----------|
|Session architecture|JWT access tokens + refresh tokens with revocation|JWT+refresh (fit 5/5), server sessions (fit 3/5), third-party auth provider (fit 2/5)|Chosen because the TDD requires stateless auth, the PRD requires persistent sessions/programmatic refresh, and horizontal scaling is easier without server-held session state.|
|Password hashing standard|bcrypt cost 12 via `PasswordHasher`|bcrypt-12 (fit 5/5), argon2id (fit 2/5 for v1.0 due to constraint conflict), scrypt (fit 2/5)|Chosen because architectural constraints explicitly mandate bcrypt cost 12 and NFR-SEC-001 verifies that exact configuration.|
|Token signing algorithm|RS256 with 2048-bit RSA keys|RS256-2048 (fit 5/5), HS256 (fit 1/5), ES256 (fit 2/5)|Chosen because NFR-SEC-002 and architectural constraints explicitly require RS256 with 2048-bit RSA keys and quarterly rotation.|
|Audit retention policy|12-month audit-log retention|12 months (fit 5/5), 90 days (fit 1/5)|Chosen because PRD Legal & Compliance requires 12-month SOC2 retention, while the 90-day TDD note is a draft conflict that would fail compliance intent.|
|Reset email dispatch mode|Asynchronous SendGrid dispatch|async dispatch (fit 5/5), synchronous API call (fit 2/5)|Chosen because PRD requires anti-enumeration and good UX, and async delivery isolates external-email latency from auth endpoint p95 budgets.|
|Scope boundary for programmatic auth|Refresh-token support in v1.0; API keys deferred to v1.1|refresh-only v1.0 (fit 5/5), add API keys now (fit 2/5)|Chosen because JTBD #4 is adequately served by programmatic refresh in v1.0, while API keys introduce a second auth mechanism on the critical path.|
|Rollout strategy|Three-phase alpha -> 10% beta -> 100% GA|phased rollout (fit 5/5), big-bang GA (fit 1/5)|Chosen because the TDD already commits to 1-week alpha, 2-week beta, and 1-week GA, and the risk inventory explicitly calls for rollback-friendly traffic ramps.|

## Timeline Estimates

|MLS|Duration|Start|End|Key Milestones|
|---|---|---|---|---|
|M1|W1-W2 (2 weeks)|2026-03-30|2026-04-12|Maps to TDD M1 `Core AuthService` foundation work: schema, registration, health, audit baseline.|
|M2|W3-W4 (2 weeks)|2026-04-13|2026-04-26|Maps to late TDD M1 + most of TDD M2 `Token Management`: login, refresh, me, logout, token controls.|
|M3|W5-W6 (2 weeks)|2026-04-27|2026-05-10|Maps to TDD M3 `Password Reset` + TDD M4 `Frontend Integration` + PRD Jordan audit-access gap closure.|
|M4|W7-W8 (2 weeks)|2026-05-11|2026-05-24|Maps to hardening slice before TDD M5: metrics, tracing, alerts, performance, security evidence.|
|M5|W9-W10+2d (16 days)|2026-05-25|2026-06-09|Maps to TDD M5 `GA Release`: phased rollout, rollback validation, on-call readiness, production handoff.|

**Total estimated duration:** 10 weeks + 2 days (2026-03-30 to 2026-06-09)
