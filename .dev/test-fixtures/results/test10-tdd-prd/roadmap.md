---
spec_source: "test-tdd-user-auth.md"
complexity_score: 0.65
complexity_class: MEDIUM
primary_persona: architect
adversarial: true
base_variant: "B (Haiku 5-Phase/13-Week)"
variant_scores: "A:68 B:81"
convergence_score: 0.62
debate_rounds: 2
generated: "2026-04-16"
generator: "adversarial_merge"
total_phases: 5
total_task_rows: 110
risk_count: 6
open_questions: 12
---

# User Authentication Service — Project Roadmap

## Executive Summary

This roadmap delivers a security-first User Authentication Service that unblocks the Q2 2026 personalization roadmap, satisfies the Q3 2026 SOC2 Type II audit bar, and preserves architectural headroom for future OAuth2/MFA without breaking the v1 contract. The core shape is a stateless JWT architecture (RS256) fronted by an `AuthService` facade that composes `TokenManager`, `PasswordHasher`, `UserRepo`, `ConsentRecorder`, `ResetTokenStore`, `LockoutPolicy`, and `AuditLogger`. PostgreSQL 15+ holds user, audit, consent, reset, and security-state data; Redis 7+ holds refresh-token revocation state; SendGrid delivers transactional reset email.

The plan is organized into 5 phases plus a formal pre-rollout quality gate, running 13 weeks sequentially or compressing to approximately 10 weeks when parallel frontend and backend streams are available. Each phase has explicit entry/exit criteria, and each module with dispatch, registry, or middleware behavior has an explicit integration-point row naming its consumers.

**Business Impact:** Unblocks approximately $2.4M in projected annual revenue from personalization-dependent features, supports SOC2 Type II audit readiness in Q3 2026, addresses the 25% of churned-user exit surveys citing the absence of accounts, and reduces support burden by replacing manual access resolution with self-service password reset.

**Complexity:** MEDIUM (0.65) — well-scoped single-service feature with moderate complexity driven by security criticality (bcrypt cost 12, RS256 2048-bit, revocation semantics, lockout, rate limiting), dual-store coordination (PostgreSQL + Redis), explicit compliance artifacts (consent, retention, audit), and a three-stage rollout with feature flags.

**Critical path:** `INFRA-001/INFRA-002 → INFRA-003 → INFRA-004 → NFR-SEC-001/NFR-SEC-002 → DM-001/DM-002/DM-003/DM-004/DM-005/DM-006 → COMP-003/COMP-004/COMP-005 → COMP-010/COMP-011/COMP-012/COMP-013/COMP-017 → COMP-001/COMP-002 → FR-AUTH-001/FR-AUTH-002/FR-AUTH-003/FR-AUTH-005 → API-001/API-002/API-004/API-006/API-007 → COMP-006/COMP-007/COMP-008/COMP-009 → TEST-004/TEST-005/TEST-006 → NFR-PERF-001/NFR-PERF-002 → Pre-Rollout Quality Gate → MIG-001 → MIG-002 → MIG-003`.

**Key architectural decisions:**

- Stateless JWT (access in memory, refresh as HttpOnly cookie backed by Redis) with RS256 2048-bit signing, 5s clock-skew tolerance, and quarterly key rotation — enables horizontal scaling without session affinity and supports revocation at logout, refresh, and password-reset events.
- `AuthService` facade is the only orchestration surface; controllers and pages never call `PasswordHasher`, `TokenManager`, or `UserRepo` directly — accommodates future OAuth2/MFA providers without breaking `AuthToken` (DM-002) or endpoint contracts.
- Explicit schemas for consent (DM-004), reset tokens (DM-005), and auth security state (DM-006) are first-class contracts from Phase 1 — auditors read schemas, not module internals, and GDPR Article 7 requires `policyVersion` tied to consent acceptance.
- Testing is hybrid — unit and integration tests land inline with their implementation phase (Phase 2), end-to-end journeys land with the frontend (Phase 3), and compliance/load/resilience tests land with operations (Phase 4); a formal Pre-Rollout Quality Gate aggregates all results into a single pass/fail before MIG-001 alpha.
- Observability (Prometheus metrics, Grafana dashboards, OpenTelemetry tracing) is wired in Phase 4 — not Phase 7 — so alpha and beta phases have trace data during the highest-value debugging window.
- Rollout is three-stage (internal alpha → 10% beta → GA 100%) gated by `AUTH_NEW_LOGIN` and `AUTH_TOKEN_REFRESH` feature flags with a six-step documented rollback chain (MIG-006 through MIG-011).

**Open risks requiring resolution before Phase 1:**

- Audit log retention conflict (TDD says 90 days, PRD says 12 months) — blocks DM-003 schema and NFR-COMP-002 retention policy; OQ-003 must be closed by auth-team + compliance.
- GDPR consent mechanism design (policy versioning, UI surface, storage shape) — blocks DM-004 `policyVersion` field definition and COMP-010 ConsentRecorder implementation; OQ-009 must be closed by compliance + frontend.
- Logout and admin-log-view TDD gaps — PRD requires both (FR-AUTH-006, FR-AUTH-007) but TDD omits endpoints; OQ-004, OQ-005, OQ-011, OQ-012 must be reconciled so TDD absorbs API-007 and API-008 before implementation lock.

## Phase 1: Infrastructure and Security Foundation

**Objective:** Provision infrastructure dependencies, generate cryptographic material, establish the security baseline, freeze data-model contracts, and stand up the shared security and data-plane modules used by all downstream phases. | **Duration:** 2 weeks (Weeks 1–2) | **Entry:** SEC-POLICY-001 draft available; infrastructure access provisioned; audit retention conflict (OQ-003) resolved; GDPR consent policy versioning approach (OQ-009) approved. | **Exit:** PostgreSQL 15+ and Redis 7+ clusters healthy; TLS 1.3 enforced; CORS whitelist live; RS256 2048-bit key pair generated and mounted; `/v1/auth/*` routing active; Docker Compose dev environment starts in <30s; all six data-model schemas (DM-001–DM-006) deployed; `JwtService`, `PasswordHasher`, `UserRepo`, `ConsentRecorder`, `ResetTokenStore`, `LockoutPolicy`, `AuditLogger`, rate-limit middleware, and health endpoint all passing unit/contract tests.

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | INFRA-001 | Provision PostgreSQL 15+ cluster | Infra | — | pg15+running; pool:100; connstring-in-env; backup-configured; read-replica-for-failover | M | P0 |
| 2 | INFRA-002 | Provision Redis 7+ cluster | Infra | — | redis7+running; AUTH-enabled; persistence-on; 1GB-mem-initial; eviction-policy-configured | M | P0 |
| 3 | INFRA-003 | Setup Node.js 20 LTS project scaffold | Infra | — | node20-lts; package.json; tsconfig; eslint; project-structure; entry-points-wired | S | P0 |
| 4 | INFRA-004 | Generate RS256 2048-bit RSA key pair | Sec | — | 2048bit-keypair; mounted-as-k8s-secret; quarterly-rotation-documented; rotation-runbook | S | P0 |
| 5 | INFRA-005 | Enforce TLS 1.3 on all endpoints | Sec | INFRA-003 | tls1.3-only; no-downgrade; cert-valid; HTTP-to-HTTPS-redirect | M | P0 |
| 6 | INFRA-006 | Configure CORS origin whitelist | Sec | INFRA-003 | known-origins->preflight-200; unknown-origin->blocked; no-wildcard | S | P1 |
| 7 | INFRA-007 | Setup /v1/auth/* URL prefix routing | API | INFRA-003 | v1-prefix-active; unversioned-path->404; middleware-chain-ready | S | P0 |
| 8 | INFRA-008 | Define password policy per NIST 800-63B | Sec | — | min8+uppercase+number; no-plaintext-in-logs; policy-doc-approved; communicated-to-FE | S | P0 |
| 9 | INFRA-009 | Configure Docker Compose dev environment | Infra | INFRA-001,INFRA-002 | pg+redis-in-compose; health-checks-pass; dev-startup<30s; testcontainers-compatible | M | P1 |
| 10 | NFR-SEC-002 | Enforce RS256 token signing | Sec | INFRA-004 | alg:RS256; key:RSA2048; verify:strict; skew:5s; config:test-pass | M | P0 |
| 11 | NFR-SEC-001 | Standardize bcrypt cost 12 | Sec | INFRA-003 | algo:bcrypt; cost:12; verify:test-pass; downgrade:none; hash-prefix:$2b$12 | S | P0 |
| 12 | NFR-COMP-001 | Capture GDPR consent at signup | Sec | DM-004,API-002 | consent:req; timestamp:stored; policyVersion:bound; audit:present; register:no-consent→400 | M | P0 |
| 13 | NFR-COMP-002 | Retain audit logs 12 months | Ops | DM-003,COMP-013 | fields:userId|timestamp|ip|outcome; retain:12mo; policy:validated; tiered-storage | M | P0 |
| 14 | NFR-COMP-003 | Block raw password persistence | Sec | COMP-004,COMP-013,INFRA-008 | rawPwd:neverStored; rawPwd:neverLogged; review:pass; sinks:all-checked; error-sanitized | M | P0 |
| 15 | NFR-COMP-004 | Audit data minimization scope | Sec | DM-001,DM-004 | pii:email|displayName|min; roles:justified; timestamps:justified; review:pass; extra-PII:none | M | P1 |
| 16 | DM-001 | Define UserProfile schema | DB | INFRA-001 | id:uuidv4-pk; email:unique+lower+idx; displayName:varchar(2-100); createdAt:timestamptz+defaultNow; updatedAt:timestamptz+auto; lastLoginAt:timestamptz|null; roles:text[]+default[user] | M | P0 |
| 17 | DM-002 | Define AuthToken contract | Sec | COMP-003 | accessToken:jwt-rs256-15min; refreshToken:opaque+unique+hashed-7day; expiresIn:900; tokenType:Bearer | S | P0 |
| 18 | DM-003 | Define AuditLog schema | DB | INFRA-001 | userId:uuid-refUser-NOTNULL; eventType:str-NOTNULL; timestamp:timestamptz-NOTNULL; ipAddress:str-NOTNULL; outcome:str-NOTNULL; retain:12mo-policy | M | P0 |
| 19 | DM-004 | Define ConsentRecord schema | DB | INFRA-001 | userId:uuid-refUser; consentType:str; consentGrantedAt:timestamptz; policyVersion:str-required; sourceIp:str; GDPR-Art7-compliant | M | P0 |
| 20 | DM-005 | Define PasswordResetToken schema | DB | INFRA-001 | tokenHash:str+unique; userId:uuid-refUser; issuedAt:timestamptz; expiresAt:timestamptz-1hr; usedAt:timestamptz|null; single-use | M | P0 |
| 21 | DM-006 | Define AuthSecurityState schema | DB | INFRA-001 | userId:uuid-pk; failedAttempts:int; firstFailedAt:timestamptz|null; lockedUntil:timestamptz|null; passwordChangedAt:timestamptz|null; refreshVersion:int+default0 | M | P0 |
| 22 | COMP-003 | Build JwtService module | Sec | NFR-SEC-002,DM-002,INFRA-004 | type:backendModule; location:withinTokenManager; desc:jwtSignVerify; alg:RS256; key:RSA2048; skew:5s; dep:quarterlyRotatedKeys; implements:NFR-SEC-002 | L | P0 |
| 23 | COMP-004 | Build PasswordHasher module | Sec | NFR-SEC-001,INFRA-008 | type:backendModule; location:withinAuthBoundary; desc:bcryptAbstraction; alg:bcrypt; cost:12; configurable:true; dep:bcryptjs; migReady:true; implements:NFR-SEC-001 | M | P0 |
| 24 | COMP-005 | Build UserRepo data-access layer | DB | DM-001,INFRA-001 | type:dataAccess; location:withinAuthBoundary; desc:userProfilePersistence; store:Postgres15+; ops:findByEmail|findById|create|update; pool:pg-pool; parameterized-queries | L | P0 |
| 25 | COMP-010 | Build ConsentRecorder module | Sec | DM-004,NFR-COMP-001 | type:backendModule; location:withinAuthBoundary; fields:userId|consentType|consentGrantedAt|policyVersion|sourceIp; write:DM-004; trigger:register | M | P0 |
| 26 | COMP-011 | Build ResetTokenStore module | Sec | DM-005,INFRA-001 | type:backendModule; location:withinAuthBoundary; fields:tokenHash|userId|issuedAt|expiresAt|usedAt; store:ttl-backed; dep:DB/Redis; reuse:none | M | P0 |
| 27 | COMP-012 | Build LockoutPolicy module | Sec | DM-006,INFRA-002 | type:backendModule; location:withinAuthBoundary; window:15m; threshold:5; response:423; reset:on-success; dep:AuthSecurityState | M | P0 |
| 28 | COMP-013 | Build AuditLogger module | Ops | DM-003,NFR-COMP-002 | type:backendModule; location:withinAuthBoundary; fields:userId|eventType|timestamp|ipAddress|outcome; retain:12mo; sink:Postgres+otel; async-write; structured-JSON | L | P0 |
| 29 | COMP-017 | Build rate-limit middleware | Gate | INFRA-002,INFRA-003 | type:middleware; location:apiEdge; rules:login10/m/ip|register5/m/ip|refresh30/m/user|me60/m/user; action:429; Redis-backed | M | P0 |
| 30 | COMP-016 | Build auth health endpoint | Ops | COMP-003,COMP-005,INFRA-001,INFRA-002 | type:backendEndpoint; route:/health/auth; checks:postgres|redis|rsaKeys|sendgrid; pgOrRedisFail:unhealthy; rsaKeyMissing:unhealthy; sendgridFail:degraded; slis:uptime|deps | M | P1 |

### Integration Points — Phase 1

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| PostgreSQL connection pool (pg-pool) | Dependency injection | INFRA-001 | 1 | COMP-005 (UserRepo), COMP-013 (AuditLogger), COMP-010 (ConsentRecorder), COMP-011 (ResetTokenStore) |
| Redis client singleton | Dependency injection | INFRA-002 | 1 | COMP-002 (TokenManager), COMP-017 (RateLimiter), COMP-012 (LockoutPolicy) |
| RS256 key pair mount | Secret binding | INFRA-004 | 1 | COMP-003 (JwtService), NFR-SEC-002 enforcement |
| Express middleware chain | Middleware chain | INFRA-003/INFRA-007 | 2 | API-001 through API-008 |
| CORS middleware | Middleware chain | INFRA-006 | 1 | All API endpoints |
| JwtService sign/verify | Strategy pattern | COMP-003 | 2 | COMP-002 (TokenManager), API-001, API-004, API-007 |
| PasswordHasher hash/verify | Strategy pattern | COMP-004 | 2 | COMP-001 (AuthService: login, register, reset-confirm) |
| UserRepo CRUD methods | Dependency injection | COMP-005 | 2 | COMP-001 (AuthService) |
| AuditLogger event sink | Event binding | COMP-013 | 2 | AuthService (all auth events), NFR-COMP-002, API-008, OPS-007 |
| ConsentRecorder register hook | Callback wiring | COMP-010 | 2 | API-002, FR-AUTH-002 |
| LockoutPolicy login guard | Callback/guard | COMP-012 | 2 | API-001, FR-AUTH-001 |
| ResetTokenStore lifecycle | Registry | COMP-011 | 2 | API-005, API-006, FR-AUTH-005 |
| Rate-limit middleware rules | Middleware chain | COMP-017 | 2 | API-001 through API-008 |
| Health endpoint probes | Dependency chain | COMP-016 | 4 | NFR-REL-001, OPS-001, k8s liveness/readiness |

## Phase 2: Core Backend Auth Flows

**Objective:** Implement the `AuthService` facade, `TokenManager`, and all eight REST API endpoints; wire functional requirements FR-AUTH-001 through FR-AUTH-005; integrate SendGrid for password reset; validate all unit and integration tests inline with implementation to catch bugs at introduction, not at Phase 5. | **Duration:** 3 weeks (Weeks 3–5) | **Entry:** Phase 1 exit criteria met; all six schemas deployed; all Phase 1 modules passing contract tests. | **Exit:** All eight API endpoints (login, register, me, refresh, reset-request, reset-confirm, logout, admin/auth-events) return correct responses against acceptance criteria; FR-AUTH-001 through FR-AUTH-005 passing; SOC2 audit logging emits on every auth event; GDPR consent captured and bound to `policyVersion`; TEST-001 through TEST-005, TEST-007, TEST-008 passing in CI with real PostgreSQL/Redis via testcontainers.

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | COMP-001 | Build AuthService facade orchestrator | API | COMP-002,COMP-004,COMP-005,COMP-010,COMP-011,COMP-012,COMP-013 | type:backendFacade; deps:TokenManager|PasswordHasher|UserRepo|ConsentRecorder|ResetTokenStore|LockoutPolicy|AuditLogger|SendGrid; flows:login|register|me|refresh|reset|logout; facade-pattern; interface-extensible-for-OAuth/MFA-per-AC-011 | XL | P0 |
| 2 | COMP-002 | Build TokenManager lifecycle module | Sec | COMP-003,DM-002,DM-006,INFRA-002 | type:backendModule; issue:true; validate:true; refresh:true; revoke:true; store:Redis; 15min-access/7day-refresh-TTL; refreshVersion-bound | XL | P0 |
| 3 | FR-AUTH-001 | Implement email/password login | API | COMP-001,COMP-004,COMP-012,API-001 | valid→200+AuthToken; invalid→401; no-email-enum; 5fail/15m→423-locked; audit:login-success|login-failure | L | P0 |
| 4 | FR-AUTH-002 | Implement validated registration | API | COMP-001,COMP-004,COMP-005,COMP-010,API-002 | valid→201+UserProfile; dup→409; weakPwd→400; bcrypt:cost12-hash-stored; consent:captured; audit:register-event | L | P0 |
| 5 | FR-AUTH-003 | Implement token issue and refresh | API | COMP-002,COMP-003,API-004 | login→access15m+refresh7d; refresh→200+newPair+oldRevoked; expired→401; revoked→401; audit:token-issued|token-refreshed | L | P0 |
| 6 | FR-AUTH-004 | Implement authenticated profile read | API | COMP-001,COMP-005,API-003 | validBearer→200+UserProfile; invalid→401; fields:id|email|displayName|createdAt|updatedAt|lastLoginAt|roles | M | P1 |
| 7 | FR-AUTH-005 | Implement password reset flow | API | COMP-001,COMP-004,COMP-011,API-005,API-006 | request:genericSuccess; confirm:pwdUpdated; ttl:1h; reuse:none; allSessionsInvalidated-per-PRD; audit:reset-request|reset-confirm | L | P0 |
| 8 | API-001 | Implement POST /auth/login endpoint | API | FR-AUTH-001,COMP-017 | req:{email,password}; 200:AuthToken{accessToken,refreshToken,expiresIn,tokenType}; 401:invalid-creds; 423:locked; 429:rate-limit; 10req/min/IP | M | P0 |
| 9 | API-002 | Implement POST /auth/register endpoint | API | FR-AUTH-002,COMP-017,NFR-COMP-001 | req:{email,password,displayName,consent,policyVersion}; 201:UserProfile; 400:validation-errors; 409:email-conflict; 5req/min/IP | M | P0 |
| 10 | API-003 | Implement GET /auth/me endpoint | API | FR-AUTH-004,COMP-017 | hdr:Bearer; 200:UserProfile{id,email,displayName,createdAt,updatedAt,lastLoginAt,roles}; 401:missing|expired|invalid-token; 60req/min/user | S | P1 |
| 11 | API-004 | Implement POST /auth/refresh endpoint | API | FR-AUTH-003,COMP-002,COMP-017 | req:{refreshToken}; 200:new-AuthToken; oldRefresh:revoked; 401:expired|revoked; 30req/min/user | M | P0 |
| 12 | API-005 | Implement POST /auth/reset-request | API | FR-AUTH-005,COMP-011 | req:{email}; resp:genericSuccess-always; no-user-enumeration; email:queuedWithin60s; audit:reset-request | M | P1 |
| 13 | API-006 | Implement POST /auth/reset-confirm | API | FR-AUTH-005,COMP-011,COMP-004 | req:{token,password}; success:confirmed+allSessionsInvalidated; expired→401/400; reused→401/400; audit:reset-confirm | M | P1 |
| 14 | API-007 | Implement POST /auth/logout endpoint | API | COMP-002,COMP-001 | req:{refreshToken}|sessionCtx; success:204/200; refresh:revoked-in-Redis; redirectReady:true; audit:logout-event; PRD-gap-fill:TDD-update-needed | M | P1 |
| 15 | API-008 | Implement GET /admin/auth-events | API | COMP-013,DM-003 | auth:adminOnly; query:{userId,dateRange,eventType}; resp:paginated; fields:userId|eventType|timestamp|ipAddress|outcome; PRD-Jordan-persona-gap-fill | M | P1 |
| 16 | TEST-001 | Verify valid login token issue | Test | FR-AUTH-001,COMP-001 | level:unit; input:validCreds; expect:AuthToken-matches-DM-002; mocks:verify+issue; result:pass | S | P0 |
| 17 | TEST-002 | Verify invalid login rejection | Test | FR-AUTH-001,COMP-001 | level:unit; input:wrongPwd; expect:401+AUTH_INVALID_CREDENTIALS; no-email-enumeration; mocks:verifyFalse | S | P0 |
| 18 | TEST-003 | Verify refresh token rotation | Test | FR-AUTH-003,COMP-002 | level:unit; input:validRefresh; expect:newPair; old:revoked; mocks:redisValid | S | P0 |
| 19 | TEST-004 | Verify registration persistence | Test | FR-AUTH-002,COMP-001,COMP-005 | level:integration; scope:AuthService+Postgres-testcontainer; input:validRegister; expect:userPersisted+pwdHashed+consentRecorded | M | P0 |
| 20 | TEST-005 | Verify expired refresh rejected | Test | FR-AUTH-003,COMP-002 | level:integration; scope:TokenManager+Redis-testcontainer; input:expiredRefresh-past-7day; expect:401 | M | P0 |
| 21 | TEST-007 | Verify logout revokes refresh | Test | API-007,COMP-002 | level:integration; scope:logout+Redis; input:validRefresh; expect:revoked+reuse401 | M | P1 |
| 22 | TEST-008 | Verify admin event log access | Test | API-008,COMP-013 | level:integration; scope:adminAPI+Postgres; auth:adminOnly; filters:userId|dateRange; resp:pageable; non-admin→403 | M | P1 |

### Integration Points — Phase 2

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| AuthService facade dispatch table | Dispatch table | COMP-001 | 2 | login→PasswordHasher+LockoutPolicy+TokenManager+AuditLogger; register→PasswordHasher+UserRepo+ConsentRecorder+AuditLogger; refresh→TokenManager+AuditLogger; reset-request→ResetTokenStore+SendGrid+AuditLogger; reset-confirm→ResetTokenStore+PasswordHasher+TokenManager+AuditLogger; logout→TokenManager+AuditLogger |
| TokenManager Redis revocation registry | Registry | COMP-002 | 2 | refresh hash → user/session/refreshVersion mapping; consumed by API-004, API-007, FR-AUTH-003, FR-AUTH-005 |
| ResetTokenStore confirm callback | Callback wiring | COMP-011 | 2 | token-validate → password-update → token-consume; consumed by API-006, FR-AUTH-005 |
| Admin audit query binding | Route binding | API-008 | 2 | admin endpoint → AuditLogger store filters (userId, dateRange, eventType); consumed by Jordan persona, OPS-007 |
| SendGrid email delivery callback | Callback wiring | API-005 | 2 | FR-AUTH-005 reset-request → SendGrid send → delivery monitoring; fallback path on failure |
| Rate-limit middleware chain | Middleware chain | COMP-017 | 2 | API-001 (10/min/IP), API-002 (5/min/IP), API-003 (60/min/user), API-004 (30/min/user), API-005-008 (configured per endpoint) |
| Request validation middleware | Middleware chain | API-001-008 | 2 | body schema per endpoint → 400 on invalid → sanitize input → prevent XSS/injection |
| AuditLogger event binding | Event binding | COMP-013 | 2 | AuthService emits on login-success, login-failure, register, token-issued, token-refreshed, reset-request, reset-confirm, logout, lockout |

## Phase 3: Frontend Journey and Session UX

**Objective:** Build React frontend components for every auth flow in PRD scope — registration, login, profile, password reset, logout, and admin auth-event viewer — with an `AuthProvider` context managing the token lifecycle, silent refresh, 401 interception, route guards, inline form validation, and session-expiry notification. | **Duration:** 2 weeks (Weeks 6–7, overlaps last week of Phase 2 if parallel streams available). | **Entry:** Phase 2 exit criteria met; API endpoints returning stable contracts; DM-002 AuthToken finalized; GDPR consent UI design approved (OQ-009 closed). | **Exit:** LoginPage, RegisterPage, ProfilePage, PasswordResetPage, LogoutControl, AdminAuthEventsPage all rendering correctly; AuthProvider manages token state with silent refresh and 401 retry dedup; route guards protect `/profile` and `/admin/*`; inline validation blocks weak passwords and missing consent at the client; TEST-006, TEST-009 through TEST-012 E2E journeys green in Playwright.

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | COMP-009 | Build AuthProvider React context | FE | API-004,API-007 | type:reactContext; scope:appRoot; state:AuthToken|UserProfile; 401→refresh-and-retry; unauth→loginRedirect; exposes-user+auth-methods-to-children | XL | P0 |
| 2 | COMP-006 | Build LoginPage route | FE | API-001,COMP-009 | type:page; route:/login; auth:none; props:onSuccess|redirectUrl?; submit:API-001; tokenStore:AuthProvider; generic-error-no-enumeration | L | P0 |
| 3 | COMP-007 | Build RegisterPage route | FE | API-002,COMP-009,COMP-019 | type:page; route:/register; auth:none; props:onSuccess|termsUrl; fields:email|password|displayName|consent-checkbox; policyVersion:bound; clientPwdCheck:true | L | P0 |
| 4 | COMP-008 | Build ProfilePage route | FE | API-003,COMP-009 | type:page; route:/profile; auth:required; source:/auth/me; fields:displayName|email|createdAt|updatedAt|lastLoginAt | M | P1 |
| 5 | COMP-014 | Build LogoutControl component | FE | API-007,COMP-009 | type:frontendComponent; location:appShell; action:logout; refresh:revoked; session:endImmediate; redirect:landing | M | P1 |
| 6 | COMP-015 | Build AdminAuthEventsPage | FE | API-008,COMP-009 | type:frontendPage; route:/admin/auth-events; auth:admin; filters:userId|dateRange|eventType; table:userId|eventType|timestamp|ipAddress|outcome; pagination:server-side | L | P1 |
| 7 | COMP-018 | Configure frontend route guards | FE | COMP-009 | public:/login,/register,/reset; protected:/profile; admin-only:/admin/*; unauth-on-protected→redirect-/login; auth-on-public→redirect-/dashboard | M | P0 |
| 8 | COMP-019 | Build inline form validation module | FE | INFRA-008 | password-strength-meter(min8+upper+number); email-format-check; displayName-length(2-100); consent-required; real-time-feedback | M | P1 |
| 9 | COMP-020 | Wire AuthProvider silent token refresh | FE | COMP-009,API-004 | refresh-triggered-before-accessToken-expiry; retry-queued-401-requests; no-redirect-loop; concurrent-request-dedup; single-inflight-refresh | M | P0 |
| 10 | COMP-021 | Build session expiry notification | FE | COMP-009 | 7day-inactivity→prompt-relogin; preserve-local-state-where-possible; clear-explanation-message | S | P2 |
| 11 | FR-AUTH-006 | Implement user logout journey | FE | API-007,COMP-014,COMP-009 | clickLogout→sessionEnded; refresh:revoked; redirect:landing; sharedDevice:secure; session-invalidated-across-tabs | M | P1 |
| 12 | FR-AUTH-007 | Implement admin auth log view | FE | API-008,COMP-015 | admin→viewLogs; filters:dateRange|user|eventType; data:queryable; auditorUse:true; paginated | M | P1 |
| 13 | TEST-006 | Verify register-login-profile journey | Test | COMP-006,COMP-007,COMP-008,COMP-009 | level:e2e; flow:Register→Login→Profile; expect:accountCreated+login+profileShown; Playwright | L | P0 |
| 14 | TEST-009 | Verify password reset journey | Test | API-005,API-006,COMP-006 | level:e2e; flow:ForgotPwd→Email→Reset→Login; ttl:1h; reuse:none; old-sessions-invalid | L | P1 |
| 15 | TEST-010 | Verify silent refresh behavior | Test | COMP-009,COMP-020,API-004 | level:e2e; accessExpired→refresh-and-retry; user:staysSignedIn; refreshExpired→loginPrompt; dedup-concurrent-requests | L | P1 |
| 16 | TEST-011 | Verify logout journey | Test | FR-AUTH-006,COMP-014 | level:e2e; action:logout; expect:landingRedirect; protectedRoute→login; refreshReuse→401 | M | P1 |
| 17 | TEST-012 | Verify admin log viewer | Test | FR-AUTH-007,COMP-015 | level:e2e; adminOnly:true; filters:work; rows:correct; nonAdmin→403/redirect | M | P1 |

### Integration Points — Phase 3

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| AuthProvider context value | Dependency injection (React context) | COMP-009 | 3 | LoginPage, RegisterPage, ProfilePage, LogoutControl, AdminAuthEventsPage, route guards |
| AuthProvider 401 interceptor | Callback/middleware chain (fetch/Axios) | COMP-009/COMP-020 | 3 | All authenticated API calls → silent refresh → retry or redirect-to-login |
| Route guard registry | Registry (route table) | COMP-018 | 3 | React Router public/protected/admin-only route map |
| Form validation strategies | Strategy pattern | COMP-019 | 3 | RegisterPage, PasswordResetPage confirm form |
| LogoutControl event binding | Event binding | COMP-014 | 3 | onClick → API-007 → AuthProvider state clear → redirect |
| Session-expiry callback | Callback wiring | COMP-021 | 3 | AuthProvider detects refresh-expired → prompts relogin |
| Admin log filter state wiring | State binding | COMP-015 | 3 | Filter controls → query params → API-008 → table rows |
| RegisterPage consent binding | Callback wiring | COMP-007 | 3 | Consent checkbox + policyVersion → API-002 body → ConsentRecorder |

## Phase 4: Performance, Compliance, and Operations

**Objective:** Prove SLO targets under realistic load, validate compliance controls against SOC2/GDPR artifacts, configure autoscaling and capacity, author runbooks and alerts, and wire production-grade observability (Prometheus metrics, Grafana dashboards, OpenTelemetry tracing) before any production traffic. Per debate convergence, observability is placed here — not at GA — so alpha and beta teams have trace data during the highest-value debugging window. | **Duration:** 2 weeks (Weeks 8–9) | **Entry:** Phase 3 exit criteria met; all APIs and UI components functional end-to-end. | **Exit:** p95 < 200ms across all auth endpoints; 500-concurrent k6 load test passes; 99.9% availability path validated; all runbooks written and reviewed; all three alerts configured and paging; OpenTelemetry spans captured end-to-end through AuthService → PasswordHasher → TokenManager → JwtService; security penetration test shows zero critical findings; compliance controls (TEST-013, TEST-014, TEST-015) validated before rollout.

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | NFR-PERF-001 | Validate auth p95 under 200ms | Ops | API-001,API-002,API-003,API-004,OPS-010 | p95:<200ms; apm:enabled; scope:allAuthEndpoints; regressions:none; baseline-established | L | P0 |
| 2 | NFR-PERF-002 | Validate 500 concurrent logins | Ops | API-001,OPS-004,OPS-005 | conc:500; 5xx:0; p95:within-SLA; k6:test-pass; connection-pool-stable; saturation:measured | L | P0 |
| 3 | NFR-REL-001 | Validate 99.9% availability path | Ops | COMP-016,OPS-001,OPS-002 | uptime:99.9%; monitor:30dRolling; health:endpoint; paging:live; staging-validation-complete | M | P0 |
| 4 | MIG-004 | Gate new login with feature flag | Gate | API-001,COMP-006 | flag:AUTH_NEW_LOGIN; default:off; scope:loginPage+loginAPI; %-traffic-targeting; removable:true | S | P0 |
| 5 | MIG-005 | Gate refresh flow with feature flag | Gate | API-004,COMP-009 | flag:AUTH_TOKEN_REFRESH; default:off; whenOff:accessOnly-relogin; removal:phase5+2w | S | P1 |
| 6 | OPS-001 | Author AuthService down runbook | Ops | COMP-016,COMP-005,COMP-002 | symptoms:5xx; diagnosis:k8s|postgres|initLogs; resolution:restart|failover|relogin; escalate:15m; reviewed-by-oncall | M | P1 |
| 7 | OPS-002 | Author refresh failure runbook | Ops | COMP-002,COMP-003,MIG-005 | symptoms:logoutLoop; diagnosis:redis|keys|flag; resolution:scale|remount|enableFlag; escalation-path-defined | M | P1 |
| 8 | OPS-003 | Stand up on-call process | Ops | OPS-001,OPS-002 | p1Ack:15m; coverage:24x7+2wPostGA; path:auth→lead→mgr→platform; tools:k8s,grafana,redis-cli,psql; rotation-scheduled | M | P1 |
| 9 | OPS-004 | Set AuthService pod scaling | Ops | NFR-PERF-002 | replicas:3; hpa:max10; trigger:cpu>70; load:500Concurrent-tested; scale-down-cooldown | M | P1 |
| 10 | OPS-005 | Set PostgreSQL pool scaling | Ops | COMP-005,NFR-PERF-002 | pool:100; expectedQ:50; scaleTo:200@wait>50ms; monitor-alert-on-pool-exhaustion | M | P1 |
| 11 | OPS-006 | Set Redis memory scaling | Ops | COMP-002,NFR-PERF-002 | mem:1GB; expected:100Ktokens~50MB; scaleTo:2GB@>70%; eviction-policy-set | M | P1 |
| 12 | OPS-007 | Alert on login failure spikes | Ops | COMP-013,OPS-010 | metric:auth_login_total; threshold:>20%/5min; action:OPS-001; source:prom; PagerDuty-wired | S | P1 |
| 13 | OPS-008 | Alert on auth latency spikes | Ops | NFR-PERF-001,OPS-010 | metric:auth_login_duration_seconds-histogram; threshold:p95>500ms; source:prom; action:checkPods+db; escalation-defined | S | P1 |
| 14 | OPS-009 | Alert on Redis failures | Ops | COMP-002 | metric:redisConnFailures; threshold:sustainedAny; source:structuredLogs; action:OPS-002; immediate-page | S | P1 |
| 15 | OPS-010 | Deploy Prometheus metrics exporters | Ops | COMP-001 | auth_login_total:counter; auth_login_duration_seconds:histogram; auth_token_refresh_total:counter; auth_registration_total:counter; auth_reset_total:counter; /metrics-endpoint-live | M | P0 |
| 16 | OPS-011 | Build Grafana monitoring dashboards | Ops | OPS-010 | login-rate-panel; latency-p95-panel; refresh-rate-panel; error-rate-panel; registration-funnel-panel; 5-panel-dashboard-live | M | P1 |
| 17 | OPS-012 | Configure OpenTelemetry tracing | Ops | COMP-001 | spans:AuthService→PasswordHasher→TokenManager→JwtService; trace-correlation-id; sampling-rate-configured; traces-available-from-alpha | M | P0 |
| 18 | TEST-013 | Verify consent auditability | Test | NFR-COMP-001,DM-004 | level:integration; consent:recorded; timestamp:present; policyVersion:present; noConsent→400; audit-trail-queryable | M | P1 |
| 19 | TEST-014 | Verify SOC2 log retention policy | Test | NFR-COMP-002,DM-003 | level:integration; retain:12mo; fields:userId|eventType|timestamp|ipAddress|outcome; policy:pass; tiered-storage-verified | M | P1 |
| 20 | TEST-015 | Verify raw password never logged | Test | NFR-COMP-003,COMP-013 | level:securityReview; sinks:app|audit|trace; rawPwd:none; error-messages-sanitized; review:pass | M | P0 |
| 21 | TEST-016 | Verify load and failover readiness | Test | NFR-REL-001,OPS-001,OPS-002 | level:resilience; depLoss:simulated(pg|redis|sendgrid); health:degradesCorrectly-per-COMP-016; runbooks:actionable | L | P1 |
| 22 | TEST-017 | Execute security penetration testing | Test | API-001,API-002,API-003,API-004,API-005,API-006,API-007 | XSS-scan-clean; CSRF-check-pass; JWT-manipulation-rejected; brute-force-blocked; SQLi-blocked; no-critical-findings; report-signed-off | L | P1 |

### Integration Points — Phase 4

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| Feature flag registry (AUTH_NEW_LOGIN, AUTH_TOKEN_REFRESH) | Registry / dispatch gate | MIG-004/MIG-005 | 4 | API router %-traffic targeting (MIG-001, MIG-002, MIG-003); TokenManager.refresh() enable/disable |
| Prometheus scrape targets | Registry | OPS-010 | 4 | Prometheus server scrapes /metrics; consumed by OPS-007, OPS-008, OPS-011, SC-001, SC-003 |
| Prometheus metric bindings | Event binding | OPS-010 | 4 | Counters/histograms wired from AuthService methods; consumed by alerts and dashboards |
| Grafana data source (Prometheus) | Dependency injection | OPS-011 | 4 | Grafana dashboards (login rate, latency, refresh rate, error rate, registration funnel) |
| PagerDuty alert routing | Callback chain | OPS-007/OPS-008/OPS-009 | 4 | On-call rotation (OPS-003) → auth-team → lead → manager → platform |
| OpenTelemetry span context propagation | Middleware chain / trace wiring | OPS-012 | 4 | AuthService → PasswordHasher → TokenManager → JwtService; trace-correlation-id flows through all downstream components |
| Health probe wiring | Middleware / k8s probe | COMP-016 | 4 | k8s liveness/readiness; NFR-REL-001 uptime monitor |
| Autoscaler triggers | Callback wiring | OPS-004 | 4 | HPA CPU>70% → scale AuthService replicas; scale-down cooldown policy |

### Pre-Rollout Quality Gate

**Objective:** Aggregate Phases 2–4 test, compliance, performance, and security results into a single formal pass/fail gate before MIG-001 alpha deployment. This gate exists because distributed inline testing catches bugs early but needs a single sign-off moment before production exposure. | **Duration:** 2–3 days (Week 9 end) | **Entry:** Phase 4 exit criteria met; all Phase 2–4 tests green in CI; observability wired and emitting.

**Gate criteria (all must pass):**

- E2E journeys: TEST-006 (register-login-profile), TEST-009 (password reset), TEST-010 (silent refresh), TEST-011 (logout), TEST-012 (admin log viewer) — all green against staging.
- Performance: NFR-PERF-001 (p95 < 200ms), NFR-PERF-002 (500 concurrent, 0 5xx) — both pass.
- Security: TEST-015 (raw password never logged) — pass; TEST-017 (penetration test) — zero critical findings, all high/medium findings triaged with sign-off.
- Compliance: TEST-013 (consent auditability), TEST-014 (SOC2 log retention, 12-month), NFR-COMP-003 (NIST SP 800-63B password storage), NFR-COMP-004 (GDPR data minimization) — all pass with compliance-team sign-off.
- Resilience: TEST-016 (load and failover readiness), health endpoint degrades correctly per COMP-016 (SendGrid-fail → degraded; pg/redis/rsa-fail → unhealthy).
- Observability: OPS-010 metrics emitting; OPS-011 dashboards live; OPS-012 traces captured; OPS-007/008/009 alerts tested and paging.
- Runbooks: OPS-001, OPS-002 reviewed by on-call; OPS-003 rotation scheduled.

**Exit:** Quality gate sign-off signed by auth-team lead, platform-team lead, security reviewer, compliance reviewer, and product owner; all P0 and P1 issues resolved; go/no-go decision for MIG-001 documented; MIG-006 through MIG-011 rollback runbooks pre-approved.

## Phase 5: Controlled Rollout to GA

**Objective:** Execute the three-stage rollout (internal alpha → 10% beta → 100% GA) with feature flags, rollback readiness, and progressive traffic shifting; validate post-launch success metrics; deprecate legacy auth; complete post-mortem discipline for any rollback event. | **Duration:** 4 weeks (Weeks 10–13) — 1 week alpha + 2 weeks beta + 1 week GA | **Entry:** Pre-Rollout Quality Gate signed off; MIG-004 and MIG-005 flags configured; all rollback runbooks tested in staging. | **Exit:** 100% traffic on new AuthService; AUTH_NEW_LOGIN flag removed; legacy auth deprecated; 99.9% uptime maintained over first 7 days of GA; all dashboards green; all ten success criteria (SC-001 through SC-010) measured with results documented.

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | MIG-001 | Run internal alpha rollout | Gate | MIG-004,OPS-003,TEST-006,TEST-016 | env:staging; users:auth-team+QA; flag:AUTH_NEW_LOGIN=on-internal; success:allFRManualPass+0P0/P1 | L | P0 |
| 2 | MIG-002 | Run 10 percent beta rollout | Gate | MIG-001,NFR-PERF-001,NFR-PERF-002 | traffic:10%; p95:<200ms; errRate:<0.1%; redisFailures:none; 2-week-observation | XL | P0 |
| 3 | MIG-003 | Run GA rollout and cutover | Gate | MIG-002,MIG-005 | traffic:100%; dashboards:green; uptime:99.9%@7d; legacy:deprecated; AUTH_NEW_LOGIN-flag-removed | XL | P0 |
| 4 | MIG-006 | Disable flag for rollback | Gate | MIG-004 | action:AUTH_NEW_LOGIN=off; route:legacy; execution-time:<1min; tested-in-staging | S | P0 |
| 5 | MIG-007 | Verify legacy after rollback | Gate | MIG-006 | smoke-test-suite-for-legacy; automated-execution; pass/fail-in<5min; userImpact:bounded | S | P0 |
| 6 | MIG-008 | Investigate rollback root cause | Ops | MIG-006,COMP-013 | inputs:logs+traces+metrics; cause:identified; evidence:captured; template-followed | M | P1 |
| 7 | MIG-009 | Restore corrupted auth data | DB | MIG-006,DM-001 | backup:lastKnownGood; restore:selective; verify:userProfileIntegrity; RTO<30min; idempotent-upsert | L | P1 |
| 8 | MIG-010 | Notify response teams | Ops | MIG-006 | notify:auth+platform; channel:incident; template-message; status-page-updated | S | P1 |
| 9 | MIG-011 | Complete rollback postmortem | Ops | MIG-008,MIG-009,MIG-010 | blameless-template; deadline:48h; cause:documented; actions:assigned-in-Jira | M | P1 |
| 10 | SC-001 | Validate login latency success metric | Gate | NFR-PERF-001 | metric:loginP95; target:<200ms; source:APM; phase:beta+GA | S | P0 |
| 11 | SC-002 | Validate registration success rate | Gate | API-002,COMP-007 | metric:registrationSuccess; target:>99%; source:funnelRatio; phase:GA | S | P1 |
| 12 | SC-003 | Validate refresh latency metric | Gate | API-004,COMP-009 | metric:refreshP95; target:<100ms; source:APM; phase:beta+GA | S | P1 |
| 13 | SC-004 | Validate uptime success metric | Gate | NFR-REL-001 | metric:uptime; target:99.9%; source:healthMonitoring; phase:GA-30d | S | P0 |
| 14 | SC-005 | Validate password hash timing | Gate | COMP-004 | metric:hashTime; target:<500ms; source:benchmark; phase:preGA | S | P1 |
| 15 | SC-006 | Validate registration conversion | Gate | COMP-007,TEST-006 | metric:registerConversion; target:>60%; source:funnelAnalytics; phase:GA | S | P1 |
| 16 | SC-007 | Validate authenticated DAU growth | Gate | API-001,API-004 | metric:DAU; target:>1000@30d; source:tokenIssueCounts; phase:postGA | S | P2 |
| 17 | SC-008 | Validate session duration metric | Gate | COMP-009,API-004 | metric:avgSession; target:>30m; source:refreshAnalytics; phase:GA | S | P1 |
| 18 | SC-009 | Validate failed login rate | Gate | COMP-013,API-001 | metric:failedLoginRate; target:<5%; source:authEventLogs; phase:GA | S | P1 |
| 19 | SC-010 | Validate reset completion rate | Gate | API-005,API-006 | metric:resetCompletion; target:>80%; source:resetFunnel; phase:GA | S | P1 |

### Integration Points — Phase 5

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| Rollout flag controller | Control plane / dispatch gate | MIG-004/MIG-005 | 5 | Staged traffic (internal → 10% → 100%); MIG-001, MIG-002, MIG-003 |
| Rollback procedure chain | Runbook chain / callback sequence | MIG-006–MIG-011 | 5 | Disable → verify → investigate → restore → notify → postmortem |
| Rollback trigger thresholds | Event binding | OPS-007/OPS-008/OPS-009 | 5 | Alerting (p95>1000ms/5min, error>5%/2min, Redis-fail>10/min) → MIG-006 |
| Success metric dashboard wiring | Dashboard binding | OPS-011 | 5 | SC-001 through SC-010 mapped to prod telemetry panels |
| Incident channel notification hook | Callback wiring | MIG-010 | 5 | Rollback trigger → auth-team + platform-team notification → status page |
| Legacy cutover route mapping | Routing binding | MIG-004 | 5 | API Gateway selects new vs legacy path based on flag state; dual-operation during beta |

## Risk Assessment and Mitigation

| # | Risk | Severity | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|---|---|
| 1 | Token theft via XSS or insecure storage | HIGH | MEDIUM | Session hijack; unauthorized account access; GDPR breach | httpOnly+Secure+SameSite=Strict cookies (COMP-005); CSP hardening (NFR-SEC-001); XSS probe in TEST-017 pen test | security |
| 2 | Brute-force credential stuffing | HIGH | HIGH | Account takeover; reputational loss; GDPR notification obligation | Lockout policy 5/15min (COMP-013); adaptive rate-limits per IP+username (API-001); CAPTCHA on 3rd failure (API-001); attack simulation TEST-008 | security |
| 3 | User migration data loss or corruption | CRITICAL | MEDIUM | Legacy user lockout; trust collapse; GDPR data-integrity violation | Dual-write strategy (MIG-001); golden-dataset integrity checks (MIG-002); full rollback chain MIG-006–MIG-011; pre-migration snapshot | backend |
| 4 | Poor signup/login UX causes <60% conversion | MEDIUM | MEDIUM | Business metric miss (Alex persona goal); churn; failed OKR | Progressive disclosure (COMP-006/007); password-strength meter (COMP-007); persona test personas Alex/Jordan/Sam in TEST-006; funnel analytics OPS-011 | frontend |
| 5 | Audit trail gaps breach SOC2/GDPR compliance | HIGH | MEDIUM | Audit failure; contractual penalties; GDPR fines | 12-month retention COMP-012/NFR-COMP-003; policyVersion binding DM-004/NFR-COMP-001; quarterly access review NFR-COMP-004; SOC2 audit validation TEST-014 | security |
| 6 | SendGrid email delivery failure blocks reset flow | MEDIUM | MEDIUM | Reset completion <80% (Sam persona goal); support escalation | Circuit-breaker fallback (COMP-010); degraded-state health classification (COMP-016); queue-and-retry COMP-010; OPS-001 deliverability alerting; secondary provider in OQ-007 | devops |

## Resource Requirements and Dependencies

### External Dependencies

| Dependency | Required By Phase | Status | Fallback |
|---|---|---|---|
| PostgreSQL 15+ (with pg_partman) | 1 | Provisioned (INFRA-001) | Staging instance; vendor support contract |
| Redis 7+ (cluster mode) | 1 | Provisioned (INFRA-002) | In-memory LRU local cache with degraded rate-limit accuracy |
| SendGrid API (transactional email) | 3 | Account + API key pending | Secondary SES provider (OQ-007 unresolved) |
| RSA 2048-bit key pair (JWT signing) | 1 | Generated in INFRA-003 | HSM-backed key rotation in post-GA |
| OpenTelemetry Collector + Prometheus + Grafana | 4 | Provisioned (OPS-011) | Datadog fallback; manual log-scraping alerts |
| Feature-flag service (AUTH_NEW_LOGIN/AUTH_TOKEN_REFRESH) | 5 | Configuration required (INFRA-009) | Env-var toggle with deploy-time switch |
| Docker Compose test-env stack | 1 | Built in INFRA-009 | Local compose fallback; k8s kind cluster |

### Infrastructure Requirements

- Kubernetes namespace `auth-prod` with HPA (min 3, max 20 pods) for API tier
- PostgreSQL primary + 2 read replicas with automated daily backup + PITR (7-day retention)
- Redis cluster 3-node with sentinel-driven failover and rdb+aof persistence
- TLS 1.3 termination at ingress (managed cert); mutual-TLS from gateway → auth-service
- Secrets vault (HashiCorp Vault or AWS Secrets Manager) for RSA keys + DB creds
- Observability stack: OTel Collector → Prometheus + Grafana + Loki; alert routing to PagerDuty
- CI/CD pipeline with test-fixtures Docker Compose (INFRA-009) + ephemeral staging env
- Log retention storage: encrypted S3 bucket with 12-month lifecycle + legal-hold capability

### Team Resources

- Backend engineer × 2 (senior Node.js/TypeScript + PostgreSQL fluency)
- Frontend engineer × 2 (React + accessibility specialist)
- Security engineer × 1 (penetration testing, NIST SP 800-63B expertise)
- DevOps/SRE × 1 (Kubernetes, OpenTelemetry, incident response)
- QA engineer × 1 (Playwright + k6 + ZAP tooling)
- Compliance/Legal reviewer × 0.25 FTE (GDPR Art 7, SOC2 evidence review)

## Success Criteria and Validation Approach

| Criterion | Metric | Target | Validation Method | Phase |
|---|---|---|---|---|
| Login latency meets SLA | API p95 /auth/login | <200ms | k6 load test against staging 10× expected RPS (NFR-PERF-001, TEST-013) | 4 |
| Token refresh latency | API p95 /auth/refresh | <150ms | k6 load run (NFR-PERF-001) | 4 |
| Service availability | Monthly uptime | 99.9% | Prometheus uptime query; multi-region health probes (NFR-REL-001) | 5 |
| Password hash cost validation | bcrypt hash time | <500ms @ cost=12 | Benchmark in CI (NFR-SEC-002, TEST-007) | 1 |
| Registration conversion | Start-to-verified funnel | >60% | Funnel analytics dashboard vs prior baseline (Alex persona, PRD §6) | 5 |
| Authenticated DAU growth | Unique daily active users | >1000 at 30 days post-GA | Token-issue counters aggregated (PRD §6) | 5 |
| Average session duration | Time between login and logout | >30 minutes | Refresh-token analytics; session-length histogram (Jordan persona, PRD §6) | 5 |
| Failed login rate | failedLogins/totalLogins | <5% | Auth-event log aggregation; lockout-triggered exclusion (PRD §6) | 5 |
| Password reset completion rate | Reset-start-to-success | >80% | Reset funnel analytics (Sam persona, PRD §6) | 5 |
| Security posture | Zero critical vulns | 0 critical, ≤2 high | OWASP ZAP + manual pen test (TEST-017, NFR-SEC-001) | 4 |

## Timeline Estimates

| Phase | Duration | Start | End | Key Milestones |
|---|---|---|---|---|
| Phase 1 | 3 weeks | W01 | W03 | Infra provisioned; DB/Redis/JWT keys ready; schema+audit live; Docker Compose test-env green |
| Phase 2 | 3 weeks | W04 | W06 | AuthService facade + registration/login/refresh/logout/reset endpoints operational; unit+integration tests ≥85% |
| Phase 3 | 3 weeks | W07 | W09 | Signup/login/reset journeys complete; E2E flows (Playwright) passing across Alex/Jordan/Sam personas |
| Phase 4 | 2 weeks | W10 | W11 | Performance, observability, security validated; Pre-Rollout Quality Gate signed-off |
| Phase 5 | 2 weeks | W12 | W13 | Alpha (internal) → 10% beta → 100% GA; legacy migration complete; rollback chain tested |

**Total estimated duration:** 13 weeks sequential (default schedule)

**Compressed alternative (10 weeks):** Phases 2 and 3 may overlap by ~2 weeks if frontend (COMP-006/007/008) is parallelized with backend flows (FR-AUTH-002/003) after AuthService facade stabilizes at W05; contract-first API commitments (API-001–API-008 typed schemas at W04) enable parallel stream. Requires +1 frontend engineer and disciplined contract freeze. Phase 4 overlap with late Phase 3 is not recommended — observability baselines require stable journey flows.

## Open Questions

| # | Question | Impact | Blocking Phase | Resolution Owner |
|---|---|---|---|---|
| 1 | OQ-001: Should social login (Google/GitHub OAuth) be in scope for v1 GA or deferred to v1.1? | Scope +2–3 weeks if in-scope; affects FR-AUTH backlog and COMP-006 UX | 2 | product |
| 2 | OQ-002: MFA strategy — TOTP only, WebAuthn, or both for v1? | Affects NFR-SEC-001 scope and COMP-013 lockout policy interaction | 2 | security |
| 3 | OQ-003: Account deletion + data-export flow (GDPR right-to-erasure + portability) — v1 or v1.1? | NFR-COMP-002 subject rights coverage; legal risk if deferred | 4 | compliance |
| 4 | OQ-004: Email verification requirement — soft (optional) or hard (mandatory for login)? | Affects FR-AUTH-001 registration funnel and SC-006 conversion target | 2 | product |
| 5 | OQ-005: Session concurrency limit — unlimited, N-device cap, or device fingerprint eviction? | Affects COMP-009 refresh-token scheme and OPS-001 session telemetry | 3 | backend |
| 6 | OQ-006: Rate-limit tiers — single global, per-IP only, or per-IP+account composite? | API-001 config; DDoS resilience; UX for shared-NAT users | 2 | security |
| 7 | OQ-007: SendGrid primary provider SLO — or require multi-provider redundancy at v1? | COMP-010 email fallback, SC-010 reset completion risk | 3 | devops |
| 8 | OQ-008: Password complexity rule — NIST SP 800-63B minimum (length+breach-check) or stricter? | NFR-SEC-002, COMP-007 UX friction, SC-006 conversion | 2 | security |
| 9 | OQ-009: Audit log sink — PostgreSQL partitioned only or mirrored to immutable store (S3 Glacier)? | NFR-COMP-003 retention compliance; SOC2 evidence durability | 1 | compliance |
| 10 | OQ-010: Token-refresh rotation — rotate on every refresh or session-long token? | COMP-002/009 refresh scheme; replay-attack surface | 2 | security |
| 11 | OQ-011: Legacy user migration — one-shot cutover or rolling dual-operation through v1.1? | MIG-001–MIG-005 sequencing; Phase 5 duration; rollback complexity | 5 | backend |
| 12 | OQ-012: Feature-flag service choice — LaunchDarkly, Unleash, or bespoke env-var toggle? | INFRA-009 build-out and MIG-004 rollout control plane | 1 | devops |

