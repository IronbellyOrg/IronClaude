---
spec_source: "test-tdd-user-auth.compressed.md"
complexity_score: 0.72
complexity_class: HIGH
primary_persona: architect
---
# User Authentication Service — Project Roadmap

## Executive Summary

The roadmap delivers the identity foundation needed for Q2 2026 personalization and Q3 2026 SOC2 readiness by sequencing work in technical layers: security and data contracts first, core auth APIs second, client integration and admin gaps third, and rollout/operations last. Priority is given to flows that unblock Alex and Sam immediately while closing Jordan's auditability gap before GA.

**Business Impact:** Enables self-service signup, login, profile access, password recovery, and programmatic session refresh while protecting the projected $2.4M personalization upside and audit readiness.

**Complexity:** HIGH (0.72) — bounded endpoint count, but materially elevated by RS256 key lifecycle, bcrypt cost 12, Redis refresh revocation, phased migration, frontend/backend coupling, and GDPR/SOC2/NIST obligations.

**Critical path:** Security and compliance decisions → canonical data/token contracts → core persistence and auth modules → `/v1/auth/*` endpoints → client/session wiring → staged migration with observability and rollback gates.

**Key architectural decisions:**

- Keep `AuthService` stateless and store only hashed refresh-token state in Redis; access tokens remain short-lived JWTs.
- Treat compliance as design-time scope: consent capture, data minimization, audit-event completeness, and 12-month retention land before beta.
- Close PRD/TDD gaps explicitly by adding logout and admin-audit deliverables without expanding into OAuth, MFA, or RBAC.

**Open risks requiring resolution before M1:**

- OQ-003 must resolve to 12-month audit retention before audit schema, storage sizing, and compliance signoff are locked.
- OQ-005 and OQ-007 affect refresh-token cardinality, logout semantics, and route/session behavior; settle them before frontend state contracts freeze.
- OQ-008 is a PRD scope gap for admin audit visibility and account lock workflows; either add it to v1.0 delivery or formally defer it.

## Milestone Summary

| ID | Title | Type | Priority | Effort | Dependencies | Deliverables | Risk |
|---|---|---|---|---|---|---|---|
| M1 | Security, contracts, and persistence baseline | Foundation | P0 | XL | PostgreSQL, Redis, Node.js, SEC-POLICY-001 | 18 | High |
| M2 | Core auth APIs and compliance flows | Backend | P0 | XL | M1, SendGrid, API Gateway | 21 | High |
| M3 | Client integration, admin gaps, and QA | Application | P0 | L | M2, routing framework | 14 | Medium |
| M4 | Rollout, operations, and validation | Release | P0 | XL | M2, M3, feature flags, observability stack | 26 | High |

## Dependency Graph

`SEC-POLICY-001, PostgreSQL, Redis, Node.js, bcryptjs, jsonwebtoken, frontend routing` → `M1` → `M2` → `M3` → `M4`

`M1` → `{DM-001, DM-002, DM-003, COMP-005, COMP-006, COMP-007, COMP-008}` → `M2`

`M2` → `{API-001, API-002, API-003, API-004, API-005, API-006, FR-AUTH-001..005, NFR-COMP-002}` → `M3`

`M2, M3` → `{MIG-001, MIG-002, MIG-003, OPS-001..005, success criteria validation}` → `M4`

## M1: Security, contracts, and persistence baseline

**Objective:** Freeze security, compliance, token, and persistence contracts before feature implementation. | **Duration:** 1 week (W1) | **Entry:** extraction and PRD approved for roadmaping | **Exit:** schemas, module boundaries, and policy decisions are implementation-ready

| # | ID | Deliverable | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | OQ-003 | Resolve audit-retention conflict | Compliance | - | retention:12mo decided; PRD/TDD delta recorded; storage sizing updated; schema unblocked | S | P0 |
| 2 | OQ-002 | Bound roles cardinality | UserProfile | DM-001 | roles max decided; token payload bounded; validation rule documented; schema impact closed | S | P1 |
| 3 | OQ-005 | Cap concurrent refresh tokens | TokenManager | DM-002 | per-user token cap decided; multi-device policy documented; eviction rule defined; Redis sizing updated | S | P0 |
| 4 | OQ-006 | Confirm lockout policy | AuthService | FR-AUTH-001 | threshold:5/15m confirmed or revised; 423 behavior approved; admin visibility captured; gateway policy aligned | S | P0 |
| 5 | DM-001 | Define UserProfile schema | PostgreSQL | OQ-002 | id:UUIDv4-PK; email:unique+idx+lowercase+notnull; displayName:2-100+notnull; createdAt:ISO8601+defaultnow+notnull; updatedAt:ISO8601+autoupdated+notnull; lastLoginAt:ISO8601+nullable; roles:string[]+default[user]+notnull | M | P0 |
| 6 | DM-002 | Define AuthToken contract | Token contract | FR-AUTH-003 | accessToken:JWT+notnull; refreshToken:opaque+unique+hashed-in-Redis+TTL7d+notnull; expiresIn:number+900+notnull; tokenType:string+Bearer+notnull | M | P0 |
| 7 | DM-003 | Define AuditLog schema | PostgreSQL | OQ-003 | userId:notnull; eventType:login_success|login_failure|registration|token_refresh|password_reset|logout|lock|unlock; timestamp:ISO8601+notnull; ipAddress:notnull; outcome:notnull; retention:12mo | M | P0 |
| 8 | NFR-SEC-001 | Standardize bcrypt cost 12 | PasswordHasher | DM-001 | algorithm:bcrypt; cost:12; raw-password:none; raw-password-logs:none; unit-check defined | M | P0 |
| 9 | NFR-SEC-002 | Standardize RS256 key policy | JwtService | DM-002 | alg:RS256; key:2048-bit RSA; rotation:quarterly; config-validation defined | M | P0 |
| 10 | NFR-COMP-001 | Capture GDPR consent at registration | Registration | DM-001 | consent required at register; consentTimestamp persisted; no-consent→400; proof queryable | M | P0 |
| 11 | NFR-COMP-003 | Enforce data minimization | Data boundary | DM-001 | collect only:email+password_hash+displayName; extra PII rejected; forms aligned; API aligned | M | P0 |
| 12 | COMP-005 | Establish AuthService facade | AuthService | DM-001,DM-002,DM-003 | type:backend-service; loc:Node.js20 service; deps:PasswordHasher+TokenManager+JwtService+PostgreSQL/UserRepo+SendGrid; flows:login+registration+profile+refresh+password-reset | L | P0 |
| 13 | COMP-006 | Baseline backend security module package | Security modules | DM-002,NFR-SEC-001,NFR-SEC-002 | type:backend-internal-modules; TokenManager:issue+refresh+revoke AuthToken pairs+Redis hashed refresh TTL7d; JwtService:sign+verify JWT RS256 2048-bit RSA skew5s; PasswordHasher:bcrypt cost12+migration abstraction | L | P0 |
| 14 | COMP-007 | Isolate TokenManager subcomponent | TokenManager | COMP-006,DM-002 | type:backend-module; actions:issue+refresh+revoke; store:Redis hashed refreshToken TTL7d; rotation:on-use; multi-device policy applied | M | P0 |
| 15 | COMP-008 | Isolate JwtService subcomponent | JwtService | COMP-006,NFR-SEC-002 | type:backend-module; actions:sign+verify accessToken; alg:RS256; key:2048-bit RSA; skew:5s | M | P0 |
| 16 | COMP-009 | Isolate PasswordHasher subcomponent | PasswordHasher | COMP-006,NFR-SEC-001 | type:backend-module; actions:hash+verify; alg:bcrypt; cost:12; future algorithm migration abstraction preserved | M | P0 |
| 17 | COMP-012 | Implement UserRepo adapter | UserRepo | DM-001 | type:repository; store:PostgreSQL15+; ops:create+findByEmail+findById+updateLastLogin; uniqueness:email enforced | M | P0 |
| 18 | COMP-013 | Implement AuditLogWriter adapter | AuditLogWriter | DM-003,OQ-003 | type:repository; store:PostgreSQL15+; writes:userId+eventType+timestamp+ipAddress+outcome; retention:12mo; query support:date+user | M | P0 |

### Integration Points — M1

| Artifact | Type | Wired | Milestone | Consumed By |
|---|---|---|---|---|
| API Gateway → AuthService | Edge routing | TLS1.3, CORS allowlist, `/v1/auth/*` route prefix, upstream rate-limit hooks | M1 | API-001, API-002, API-003, API-004, API-005, API-006, API-007 |
| AuthService → UserRepo | Dependency injection | repository interface for create/find/update profile flows | M1 | FR-AUTH-001, FR-AUTH-002, FR-AUTH-004 |
| AuthService → AuditLogWriter | Event binding | auth event persistence contract | M1 | NFR-COMP-002, API-007, API-008, API-009, API-010 |
| TokenManager → Redis | Store binding | hashed refresh token storage, revocation, TTL | M1 | FR-AUTH-003, API-004, API-007 |
| TokenManager → JwtService | Service delegation | sign/verify access tokens with RS256 policy | M1 | FR-AUTH-003, API-001, API-004 |

### Deliverables — M1

| ID | Description | Acceptance Criteria |
|---|---|---|
| DM-001 | Canonical user profile schema | Every persisted field, constraint, and default is frozen and referenced by API and frontend contracts |
| DM-002 | Canonical auth token contract | Access/refresh token pair contract is stable, TTLs are fixed, and storage semantics are documented |
| COMP-005 | Backend orchestration boundary | `AuthService` owns orchestration only and delegates hashing, tokening, persistence, and email concerns |
| COMP-006 | Security module decomposition | Token, JWT, and password modules are isolated and independently testable |
| DM-003 | Audit event persistence model | Audit fields satisfy SOC2 evidence needs and support user/date queries |

### Milestone Dependencies — M1

- PostgreSQL 15+, Redis 7+, Node.js 20 LTS, bcryptjs, jsonwebtoken, SendGrid, and API Gateway availability must be confirmed.
- SEC-POLICY-001 and PRD legal/compliance requirements must be treated as authoritative for password and token policy.
- OQ-003, OQ-005, and OQ-006 should be closed before API contract code begins.

### Milestone Risk Assessment — M1

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Retention conflict remains unresolved | Medium | High | Make PRD 12-month rule authoritative and freeze storage/partition plan before implementation |
| Refresh-token cardinality remains ambiguous | Medium | Medium | Decide per-user cap early and carry it into Redis key design and AuthProvider behavior |
| Roles field grows without bound | Low | Medium | Fix array limit before JWT payload and profile schema are locked |

## M2: Core auth APIs and compliance flows

**Objective:** Implement the server-side contracts that deliver login, registration, profile, refresh, reset, logout, and admin audit capabilities. | **Duration:** 2 weeks (W2-W3) | **Entry:** M1 contracts and policy decisions complete | **Exit:** all `/v1/auth/*` server flows are implemented and contract-testable

| # | ID | Deliverable | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | OQ-001 | Decide API-key auth deferment | Auth boundary | COMP-005 | service-to-service auth yes/no decided; v1.0 deferment documented; non-user path excluded from current APIs; backlog owner assigned | S | P1 |
| 2 | OQ-004 | Decide synchronous vs asynchronous reset delivery | Password reset | FR-AUTH-005 | delivery mode decided; <60s delivery target preserved; retry semantics defined; SendGrid integration shape fixed | S | P1 |
| 3 | FR-AUTH-001 | Implement login with email and password | AuthService | COMP-005,COMP-009,COMP-007,COMP-012 | valid credentials→200+AuthToken; invalid credentials→401; nonexistent email→401 no enumeration; 5 failed attempts/15m→423 lockout | L | P0 |
| 4 | FR-AUTH-002 | Implement validated registration | AuthService | COMP-005,COMP-009,COMP-012,NFR-COMP-001,NFR-COMP-003 | valid registration→201+UserProfile; duplicate email→409; weak password(<8,no uppercase,no number)→400; bcrypt hash cost12 stored | L | P0 |
| 5 | FR-AUTH-003 | Implement JWT issuance and refresh | TokenManager | COMP-007,COMP-008,DM-002 | login returns accessToken15m+refreshToken7d; POST refresh valid token→new AuthToken pair; expired refresh→401; revoked refresh→401 | L | P0 |
| 6 | FR-AUTH-004 | Implement authenticated profile retrieval | AuthService | COMP-005,COMP-012,DM-001 | GET /auth/me valid accessToken→UserProfile; expired or invalid token→401; response includes id+email+displayName+createdAt+updatedAt+lastLoginAt+roles | M | P0 |
| 7 | FR-AUTH-005 | Implement two-step password reset | AuthService | COMP-005,COMP-009,OQ-004 | POST reset-request valid email sends reset token; POST reset-confirm valid token updates password hash; token expires in 1h; used token cannot be reused; existing sessions invalidated | L | P0 |
| 8 | NFR-PERF-001 | Meet p95 latency target | AuthService | FR-AUTH-001,FR-AUTH-002,FR-AUTH-003,FR-AUTH-004,FR-AUTH-005 | all auth endpoints p95<200ms; APM tracing on AuthService methods; hot paths measured; regressions blocked | M | P0 |
| 9 | NFR-PERF-002 | Support 500 concurrent logins | AuthService | FR-AUTH-001,NFR-PERF-001 | 500 concurrent login requests sustained; k6 scenario defined; saturation within capacity plan; failures within SLO | M | P0 |
| 10 | NFR-REL-001 | Establish availability controls | Health/ops | COMP-005 | uptime target 99.9%/30d instrumented; health check endpoint live; monitoring wired; alert thresholds defined | M | P0 |
| 11 | NFR-COMP-002 | Implement SOC2 audit logging | AuditLogWriter | COMP-013,DM-003 | log login success/failure+registration+token refresh+password reset+logout; fields userId+timestamp+ipAddress+outcome; retention 12mo; queryable by date range and user | L | P0 |
| 12 | API-001 | Deliver POST /auth/login contract | Login API | FR-AUTH-001 | auth:none; rate-limit:10 req/min/IP; request email+password; 200 response AuthToken(accessToken+refreshToken+expiresIn900+tokenTypeBearer); errors 401+423+429 | M | P0 |
| 13 | API-002 | Deliver POST /auth/register contract | Register API | FR-AUTH-002,NFR-COMP-001 | auth:none; rate-limit:5 req/min/IP; request email+password+displayName+consent; 201 response UserProfile(id+email+displayName+createdAt+updatedAt+lastLoginAt null+roles[user]); errors 400+409 | M | P0 |
| 14 | API-003 | Deliver GET /auth/me contract | Profile API | FR-AUTH-004 | auth:Bearer accessToken; rate-limit:60 req/min/user; request header Authorization:Bearer <accessToken>; 200 response full UserProfile; errors 401 | M | P0 |
| 15 | API-004 | Deliver POST /auth/refresh contract | Refresh API | FR-AUTH-003 | auth:none at HTTP layer; rate-limit:30 req/min/user; request refreshToken; 200 response new AuthToken pair; expired/revoked refresh→401 | M | P0 |
| 16 | API-005 | Deliver POST /auth/reset-request contract | Reset request API | FR-AUTH-005,OQ-004 | auth:none; request email; generic success prevents enumeration; email dispatch path fixed; rate-limit defined | M | P1 |
| 17 | API-006 | Deliver POST /auth/reset-confirm contract | Reset confirm API | FR-AUTH-005 | auth:none; request token+password; valid token updates bcrypt hash; expired/used token rejected; sessions revoked | M | P1 |
| 18 | API-007 | Deliver POST /auth/logout contract | Logout API | FR-AUTH-003 | auth:Bearer or refresh-bound session identity; session ends immediately; refresh token revoked; user redirected or client instructed to clear state | M | P1 |
| 19 | API-008 | Deliver GET /auth/events contract | Admin audit API | NFR-COMP-002,OQ-008 | admin-only; filters user+dateRange; response fields userId+eventType+timestamp+ipAddress+outcome; pagination and auth errors defined | M | P1 |
| 20 | API-009 | Deliver POST /auth/users/{id}/lock contract | Admin lock API | OQ-008,FR-AUTH-001 | admin-only; target account lock persisted; lock reason captured; subsequent login blocked with 423 | M | P1 |
| 21 | API-010 | Deliver POST /auth/users/{id}/unlock contract | Admin unlock API | OQ-008,API-009 | admin-only; lock cleared; unlock visible in audit log; subsequent valid login allowed | M | P1 |

### Integration Points — M2

| Artifact | Type | Wired | Milestone | Consumed By |
|---|---|---|---|---|
| `/v1/auth/*` router | Dispatch table | login, register, me, refresh, reset-request, reset-confirm, logout, events, lock, unlock handlers mapped to AuthService/admin services | M2 | API-001, API-002, API-003, API-004, API-005, API-006, API-007, API-008, API-009, API-010 |
| Gateway middleware chain | Middleware | TLS1.3, CORS allowlist, route-level rate limits, auth header parsing, admin guard binding | M2 | API-001, API-002, API-003, API-004, API-008, API-009, API-010 |
| AuthService → SendGrid | Callback wiring | reset token generation, template render, delivery dispatch, failure surfacing | M2 | FR-AUTH-005, API-005 |
| AuthService → TokenManager → JwtService | Service chain | verify password, issue pair, rotate refresh, sign/verify JWT | M2 | FR-AUTH-001, FR-AUTH-003, API-001, API-004, API-007 |
| AuthService/admin handlers → AuditLogWriter | Event binding | success/failure/logout/lock/unlock events persisted with IP and outcome | M2 | NFR-COMP-002, API-007, API-008, API-009, API-010 |

### Deliverables — M2

| ID | Description | Acceptance Criteria |
|---|---|---|
| FR-AUTH-001 | Login flow implementation | Login is generic on failure, resistant to enumeration, and produces the canonical token pair on success |
| FR-AUTH-005 | Reset flow implementation | Reset request and confirm endpoints preserve privacy, TTL rules, and session invalidation semantics |
| API-008 | Admin event-query API | Jordan can query audit records by user and date range with stable response fields |
| API-009 | Administrative lock control | Admin-triggered lockout prevents future logins and creates a visible audit trail |
| NFR-COMP-002 | Compliance-grade event logging | Every security-relevant auth event is retained for 12 months with mandatory fields |

### Milestone Dependencies — M2

- SendGrid must be provisioned before reset-request implementation is finalized.
- API Gateway is responsible for CORS and rate limiting; service code should not duplicate gateway concerns.
- Admin APIs should stay within v1.0 only if OQ-008 resolves as in-scope; otherwise they move to deferred follow-up with explicit issue ownership.

### Milestone Risk Assessment — M2

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Reset delivery mode chosen too late | Medium | Medium | Freeze sync/async decision before email integration and API error contract stabilize |
| Admin-control scope expands uncontrolled | Medium | High | Limit v1.0 admin surface to audit, lock, and unlock only; exclude RBAC and broader user management |
| Performance target missed after compliance logging | Medium | High | Instrument logging path early and benchmark p95 before beta admission |

## M3: Client integration, admin gaps, and QA

**Objective:** Wire the frontend session model, deliver core user journeys, and prove correctness across unit, integration, and E2E layers. | **Duration:** 1 week (W4) | **Entry:** M2 APIs are stable and testable | **Exit:** golden-path user journeys and admin-visible behaviors are verified end-to-end

| # | ID | Deliverable | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | OQ-007 | Decide remember-me scope | Product/session UX | API-004,COMP-004 | remember-me yes/no decided; session-duration impact documented; v1.0 or deferment recorded; frontend state contract aligned | S | P1 |
| 2 | OQ-008 | Resolve admin audit and lock scope | Admin surface | API-008,API-009,API-010 | admin event view and lock/unlock confirmed in-scope or formally deferred; owner assigned; roadmap variance closed | S | P0 |
| 3 | COMP-001 | Implement LoginPage | LoginPage | API-001,COMP-004 | type:frontend page route; loc:/login; auth:none; props:onSuccess()+redirectUrl?; form email+password; submit POST /auth/login; stores AuthToken via AuthProvider | M | P0 |
| 4 | COMP-002 | Implement RegisterPage | RegisterPage | API-002,COMP-004,NFR-COMP-001 | type:frontend page route; loc:/register; auth:none; props:onSuccess()+termsUrl; form email+password+displayName+consent; client-side password validation enforced; submit POST /auth/register | M | P0 |
| 5 | COMP-003 | Implement ProfilePage | ProfilePage | API-003,COMP-004 | type:frontend page route; loc:/profile; auth:required; pulls full UserProfile; renders id/email/displayName/createdAt/updatedAt/lastLoginAt/roles | M | P1 |
| 6 | COMP-004 | Implement AuthProvider | AuthProvider | API-001,API-003,API-004,API-007,OQ-007 | type:React context provider; props:children ReactNode; manages AuthToken state; intercepts 401; triggers silent refresh; redirects unauthenticated protected routes to LoginPage; clears state on logout/tab-close policy | L | P0 |
| 7 | COMP-010 | Implement LogoutControl | Logout UX | API-007,COMP-004 | visible logout action exists; triggers immediate session termination; clears client auth state; redirects to landing/login | M | P1 |
| 8 | COMP-011 | Implement AdminAuditPage | Admin audit UI | API-008,OQ-008 | admin view lists auth events; filters by user/date range; shows userId+eventType+timestamp+ipAddress+outcome; access restricted to admins | M | P1 |
| 9 | TEST-001 | Add valid-login unit test | AuthService test | FR-AUTH-001 | AuthService.login() calls PasswordHasher.verify then TokenManager.issueTokens; valid AuthToken returned; success path audited | M | P0 |
| 10 | TEST-002 | Add invalid-login unit test | AuthService test | FR-AUTH-001 | PasswordHasher.verify false→401; no AuthToken issued; generic error preserved; no user enumeration leak | M | P0 |
| 11 | TEST-003 | Add refresh unit test | TokenManager test | FR-AUTH-003 | TokenManager.refresh validates token; revokes old refresh token; issues new pair via JwtService; revoked/expired handled | M | P0 |
| 12 | TEST-004 | Add registration integration test | Auth+PostgreSQL test | FR-AUTH-002,DM-001 | API request flows through PasswordHasher to DB insert; UserProfile persisted with canonical fields; duplicate email blocked | L | P0 |
| 13 | TEST-005 | Add expired-refresh integration test | Token+Redis test | FR-AUTH-003,DM-002 | Redis TTL expiration invalidates refresh token; expired refresh returns 401; no replacement pair issued | L | P0 |
| 14 | TEST-006 | Add registration-login-profile E2E | Playwright journey | COMP-001,COMP-002,COMP-003,COMP-004 | user registers, logs in, profile renders; silent session handling works; protected-route redirect works | L | P0 |

### Integration Points — M3

| Artifact | Type | Wired | Milestone | Consumed By |
|---|---|---|---|---|
| App root → AuthProvider | Context/provider wiring | global auth state, refresh lifecycle, protected-route redirect behavior | M3 | COMP-001, COMP-002, COMP-003, COMP-010 |
| Public/Protected route registry | Route binding | `/login`, `/register` public; `/profile`, admin routes protected | M3 | COMP-001, COMP-002, COMP-003, COMP-011 |
| Form submit handlers | Event binding | page forms map to login/register/reset/logout endpoints with inline validation and generic error rendering | M3 | API-001, API-002, API-005, API-006, API-007 |
| 401 interceptor → refresh strategy | Callback chain | expired access token triggers refresh flow or redirect on failure | M3 | API-003, API-004, COMP-004 |
| AdminAuditPage → audit query API | Data binding | date-range and user filters map to admin event endpoint response | M3 | API-008, API-009, API-010 |

### Deliverables — M3

| ID | Description | Acceptance Criteria |
|---|---|---|
| COMP-004 | Shared authentication provider | Client state, refresh, redirect, and logout behavior are centralized and deterministic |
| COMP-001 | Login user journey | Alex can authenticate quickly with safe failure UX and post-login redirect behavior |
| TEST-006 | End-to-end auth journey coverage | Registration, login, session persistence, and profile retrieval succeed in a browser-driven flow |
| COMP-011 | Admin incident visibility UI | Jordan can inspect audit activity without direct database access |
| TEST-004 | Persistence integration coverage | Registration writes the canonical user schema and respects validation/uniqueness rules |

### Milestone Dependencies — M3

- Frontend routing framework must support protected-route redirects and shared context providers.
- Browser E2E coverage depends on stable reset, login, and profile APIs from M2.
- Remember-me behavior must not expand refresh TTL beyond the approved product/security decision.

### Milestone Risk Assessment — M3

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Session UX diverges from backend refresh policy | Medium | High | Bind AuthProvider behavior to API-004 contract and finalize remember-me decision before FE freeze |
| Admin views leak excessive auth data | Low | High | Limit fields to userId, eventType, timestamp, IP, and outcome; enforce admin-only access |
| E2E tests miss edge behavior | Medium | Medium | Cover protected-route redirects, silent refresh failure, and logout clearing in browser tests |

## M4: Rollout, operations, and validation

**Objective:** De-risk cutover through staged migration, operational readiness, and measurable validation against technical and business targets. | **Duration:** 4 weeks (W5-W8) | **Entry:** M2 APIs and M3 journeys are validated | **Exit:** GA is complete, rollback is rehearsed, and success criteria are observable in production

| # | ID | Deliverable | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | MIG-001 | Execute internal alpha rollout | Rollout | M2,M3 | duration:1w; staging deploy complete; auth-team+QA enabled via AUTH_NEW_LOGIN; FR-AUTH-001..005 manual pass; zero P0/P1 bugs | M | P0 |
| 2 | MIG-002 | Execute 10% beta rollout | Rollout | MIG-001,NFR-PERF-001,NFR-PERF-002 | duration:2w; AUTH_NEW_LOGIN enabled for 10% traffic; p95<200ms; error rate<0.1%; zero TokenManager Redis connection failures | L | P0 |
| 3 | MIG-003 | Execute 100% GA rollout | Rollout | MIG-002 | duration:1w; all users routed to new AuthService; AUTH_NEW_LOGIN removed; AUTH_TOKEN_REFRESH enabled then removed after +2w; 99.9% uptime first 7d | L | P0 |
| 4 | OPS-001 | Publish AuthService-down runbook | Operations | MIG-001 | symptoms 5xx `/auth/*`; diagnose pods+PostgreSQL+module init; resolve restart/failover/relogin; escalation auth-team then platform-team; prevention HPA+multi-AZ Redis+pool tuning | M | P0 |
| 5 | OPS-002 | Publish token-refresh-failure runbook | Operations | MIG-001,MIG-002 | symptoms logout loops+counter spike; diagnose Redis+keys+flag; resolve scale Redis/remount secrets/enable AUTH_TOKEN_REFRESH; escalation path defined | M | P0 |
| 6 | OPS-003 | Stand up launch on-call model | Operations | MIG-003 | P1 acknowledge<15m; auth-team 24/7 for first 2 weeks post-GA; tooling k8s+Grafana+Redis CLI+PostgreSQL admin; escalation chain documented | M | P1 |
| 7 | OPS-004 | Validate capacity plan | Capacity | NFR-PERF-002 | AuthService replicas 3 baseline scale to 10 on CPU>70%; PostgreSQL pool 100 increase to 200 if wait>50ms; Redis 1GB baseline scale to 2GB at >70% utilization | M | P0 |
| 8 | OPS-005 | Deliver observability stack | Observability | NFR-PERF-001,NFR-REL-001,NFR-COMP-002 | structured logs exclude passwords/tokens; metrics auth_login_total+auth_login_duration_seconds+auth_token_refresh_total+auth_registration_total; OTel traces across AuthService→PasswordHasher→TokenManager→JwtService; alerts on failure/latency/Redis issues | L | P0 |
| 9 | R-001 | Mitigate token theft via XSS | Security | COMP-004,FR-AUTH-003 | accessToken stored in memory only; refreshToken HttpOnly cookie or equivalent secure storage; AuthProvider clears tokens on tab close per policy; immediate revocation path available | L | P0 |
| 10 | R-002 | Mitigate brute-force attacks | Security | API-001,FR-AUTH-001 | gateway rate limit 10 req/min/IP; account lockout after 5 failed attempts/15m; bcrypt cost12 active; WAF block and CAPTCHA contingency documented | L | P0 |
| 11 | R-003 | Protect legacy-auth migration data | Migration safety | MIG-001,MIG-002 | parallel run in phases 1-2; idempotent UserProfile upserts; full DB backup before each phase; restore procedure tested | M | P0 |
| 12 | R-PRD-001 | Counter poor registration UX adoption | Product risk | COMP-002,MIG-002 | usability testing pre-launch complete; funnel instrumentation enabled; iterate on drop-off findings; conversion target ownership assigned | M | P1 |
| 13 | R-PRD-002 | Prevent compliance failure from incomplete logs | Compliance risk | NFR-COMP-002,OPS-005 | log field set mapped to SOC2 controls; QA validation complete; 12-month retention confirmed; missing-event audit passes | M | P0 |
| 14 | R-PRD-003 | Detect email delivery failures | Operational risk | API-005,OPS-005 | SendGrid delivery monitoring and alerts live; reset email SLA tracked; fallback support channel documented | M | P1 |
| 15 | R-PRD-004 | Run dedicated security review gate | Security review | M2,M3 | dedicated security review complete; pen-test before production complete; critical findings resolved or rollout blocked | L | P0 |
| 16 | SC-001 | Validate login latency target | Validation | API-001,OPS-005 | metric login p95; target<200ms; method APM tracing; milestone admission beta+GA | M | P0 |
| 17 | SC-002 | Validate registration success rate | Validation | API-002,OPS-005 | metric registration success; target>99%; method API analytics; failures triaged | M | P1 |
| 18 | SC-003 | Validate refresh latency target | Validation | API-004,OPS-005 | metric refresh p95; target<100ms; method APM tracing on refresh path; regressions blocked | M | P0 |
| 19 | SC-004 | Validate availability target | Validation | NFR-REL-001,OPS-005 | metric uptime; target≥99.9% over 30d; method health check monitoring; alert route tested | M | P0 |
| 20 | SC-005 | Validate hash-time target | Validation | NFR-SEC-001 | metric PasswordHasher.hash(); target<500ms cost12; method benchmark test; drift blocked | S | P0 |
| 21 | SC-006 | Validate registration conversion | Validation | R-PRD-001 | metric funnel conversion; target>60%; method landing→register→confirmed funnel; review cadence defined | M | P1 |
| 22 | SC-007 | Validate authenticated DAU growth | Validation | MIG-003 | metric daily active authenticated users; target>1000 within 30d GA; method AuthToken issuance analytics; trend review scheduled | M | P1 |
| 23 | SC-008 | Validate average session duration | Validation | API-004,COMP-004 | metric average session duration; target>30m; method token-refresh analytics; UX regressions investigated | M | P1 |
| 24 | SC-009 | Validate failed-login rate | Validation | API-001,NFR-COMP-002 | metric failed login rate; target<5% attempts; method auth event log analysis; spikes alert | M | P1 |
| 25 | SC-010 | Validate password reset completion | Validation | API-005,API-006,R-PRD-003 | metric reset completion; target>80%; method reset funnel analysis; delivery failures correlated | M | P1 |
| 26 | SC-011 | Validate phase-2 beta exit gate | Validation | MIG-002 | metric p95<200ms+error<0.1%+zero Redis failures over 2 weeks at 10% traffic; method staged rollout telemetry; exit signoff recorded | M | P0 |

### Integration Points — M4

| Artifact | Type | Wired | Milestone | Consumed By |
|---|---|---|---|---|
| Feature flag registry | Registry | AUTH_NEW_LOGIN and AUTH_TOKEN_REFRESH staged enablement, disablement, and removal | M4 | MIG-001, MIG-002, MIG-003, OPS-002 |
| Monitoring stack → alert routes | Event binding | latency, failure-rate, Redis, uptime, and delivery alerts routed to on-call | M4 | OPS-001, OPS-002, OPS-003, SC-001, SC-004, SC-011 |
| Rollout controller → rollback procedure | Decision gate | rollback triggers on p95, error rate, Redis failures, or data corruption | M4 | MIG-002, MIG-003, R-003 |
| Analytics pipeline | Reporting pipeline | registration, session, failed-login, and reset funnels recorded for business validation | M4 | SC-002, SC-006, SC-007, SC-008, SC-009, SC-010 |
| Backup/restore automation | Operational wiring | pre-phase backup, restore rehearsal, and corruption contingency path | M4 | R-003, MIG-001, MIG-002, MIG-003 |

### Deliverables — M4

| ID | Description | Acceptance Criteria |
|---|---|---|
| MIG-002 | Beta rollout gate | Beta traffic can run for two weeks at 10% with no Redis instability and acceptable latency/error rates |
| OPS-005 | Production observability | Metrics, traces, logs, and alerts make auth health and audit coverage visible before GA |
| R-PRD-004 | Security-release gate | Production launch is blocked until security review and pen-test complete with no unresolved critical findings |
| SC-011 | Phase-exit validation | Phase 2 exit criteria are measured directly from rollout telemetry and signed off |
| MIG-003 | GA cutover | Legacy auth can be retired behind stable metrics and tested rollback controls |

### Milestone Dependencies — M4

- Feature flags `AUTH_NEW_LOGIN` and `AUTH_TOKEN_REFRESH` must exist before rollout begins.
- Rollback triggers must be measured from live telemetry rather than manual observation.
- Compliance and security signoff are release blockers, not post-GA follow-ups.

### Milestone Risk Assessment — M4

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Cutover proceeds without rollback confidence | Low | Critical | Rehearse rollback before 100% traffic and keep flags removable until stability period ends |
| Observability misses compliance-critical events | Medium | High | Validate event coverage against SOC2-required fields before beta signoff |
| Beta metrics look healthy but UX adoption lags | Medium | Medium | Combine technical telemetry with funnel analytics before declaring GA success |

## Risk Assessment and Mitigation

| # | Risk | Severity | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|---|---|
| 1 | R-001 Token theft via XSS allows session hijacking | High | Medium | Session hijack, forced resets, customer trust loss | memory-only access token, secure refresh storage, short TTL, revocation path | security + frontend |
| 2 | R-002 Brute-force attacks on login endpoint | Medium | High | Account abuse, support load, noisy incidents | gateway rate limits, lockout policy, bcrypt cost12, WAF/CAPTCHA contingency | security + platform |
| 3 | R-003 Data loss during migration from legacy auth | High | Medium | Account corruption, rollback, launch delay | parallel run, idempotent upserts, pre-phase backups, restore rehearsal | auth-team + platform |
| 4 | R-PRD-001 Low registration adoption due to poor UX | High | Medium | Lost revenue, slower personalization activation | usability testing, funnel instrumentation, iterative UX tuning | product + frontend |
| 5 | R-PRD-002 Compliance failure from incomplete audit logging | High | Medium | SOC2 failure, incident blind spots | define log fields early, QA validation, 12-month retention, audit queries | compliance + auth-team |
| 6 | R-PRD-003 Email delivery failures blocking password reset | Medium | Low | Recovery failures, support ticket growth | SendGrid monitoring, alerting, fallback support process | ops |
| 7 | R-PRD-004 Security breach from implementation flaws | Critical | Low | Incident response, reputational damage, launch block | dedicated security review, pen-test, production gate on zero critical findings | security |

## Resource Requirements and Dependencies

### External Dependencies

| Dependency | Required By Milestone | Status | Fallback |
|---|---|---|---|
| PostgreSQL 15+ | M1 | Required before schema freeze | Block implementation until provisioned |
| Redis 7+ | M1 | Required before token design closes | Disable refresh and force re-login only as contingency during incidents |
| Node.js 20 LTS | M1 | Required for runtime baseline | No viable fallback in v1.0 |
| bcryptjs | M1 | Required for PasswordHasher | No viable fallback without security re-approval |
| jsonwebtoken | M1 | Required for JwtService | No viable fallback without token redesign |
| SendGrid | M2 | Required for password reset delivery | Support-assisted reset while delivery incident is active |
| API Gateway | M2 | Required for upstream rate limiting and CORS | Do not duplicate policy in service code; block release if unavailable |
| SEC-POLICY-001 | M1 | Required for password/token policy authority | Freeze security-sensitive implementation until clarified |
| Frontend routing framework | M3 | Required for Login/Register/Profile/Admin routes | Defer frontend rollout while backend remains API-only |

### Infrastructure Requirements

- Kubernetes or equivalent runtime with baseline 3 `AuthService` replicas and HPA to 10.
- PostgreSQL backup/restore automation before each rollout phase.
- Redis HA and memory scaling from 1 GB to 2 GB at utilization thresholds.
- TLS 1.3 termination, CORS allowlist enforcement, and `/v1/auth/*` versioned routing.
- APM, OpenTelemetry, Prometheus, structured logging, and alert routing before beta.

## Success Criteria and Validation Approach

| Criterion | Metric | Target | Validation Method | Milestone |
|---|---|---|---|---|
| SC-001 | Login response time p95 | < 200ms | APM tracing on login path during beta and GA | M4 |
| SC-002 | Registration success rate | > 99% | API analytics on registration attempts vs successful creates | M4 |
| SC-003 | Token refresh response time p95 | < 100ms | APM tracing on refresh path | M4 |
| SC-004 | Availability | ≥ 99.9% over 30 days | health-check monitoring and alert audit | M4 |
| SC-005 | PasswordHasher.hash runtime | < 500ms at cost 12 | benchmark/unit validation in CI and pre-GA | M4 |
| SC-006 | Registration conversion | > 60% | landing→register→confirmed funnel review | M4 |
| SC-007 | Daily active authenticated users | > 1,000 within 30 days of GA | token issuance and active-user analytics | M4 |
| SC-008 | Average session duration | > 30 minutes | token refresh event analytics | M4 |
| SC-009 | Failed login rate | < 5% of attempts | auth event log analysis | M4 |
| SC-010 | Password reset completion | > 80% | reset funnel analysis | M4 |
| SC-011 | Phase 2 beta exit gate | p95<200ms; error<0.1%; zero Redis failures for 2 weeks at 10% traffic | staged rollout telemetry and release signoff | M4 |
| SC-012 | 500 concurrent logins | 500 sustained concurrent requests | k6 load testing against login path | M4 |

## Decision Summary

| Decision | Chosen | Alternatives Considered | Rationale |
|----------|--------|------------------------|----------|
| Session architecture | Stateless access JWT + Redis-backed hashed refresh tokens | server-side sessions; opaque-only tokens | TDD requires stateless AuthService, 15-minute access tokens, and Redis-managed refresh revocation |
| Signing algorithm | RS256 with 2048-bit RSA keys | HS256; longer-lived access tokens | NFR-SEC-002 and architectural constraints explicitly mandate RS256, 2048-bit keys, and quarterly rotation |
| Compliance retention | 12-month audit retention | 90-day TDD retention | PRD legal/compliance explicitly requires 12-month SOC2 retention and supersedes lower TDD retention |
| v1.0 scope guardrail | Include logout and minimal admin audit/lock surface only | expand to RBAC/OAuth/MFA; omit PRD-derived gaps | PRD scope is auth foundation; logout is in-scope, admin visibility is a JTBD gap, while OAuth/MFA/RBAC are explicitly out-of-scope |
| Rollout strategy | Alpha → 10% beta → 100% GA behind feature flags | big-bang cutover; permanent dual-run | migration plan already defines phased rollout, rollback triggers, and feature flags as the safer path |

## Timeline Estimates

| Milestone | Duration | Start | End | Key Milestones |
|---|---|---|---|---|
| M1 | 1 week | W1 | W1 | Retention conflict resolved, schemas frozen, core service boundaries established |
| M2 | 2 weeks | W2 | W3 | Auth APIs implemented, compliance logging wired, admin/API scope stabilized |
| M3 | 1 week | W4 | W4 | Frontend auth journeys working, admin visibility delivered, tests green |
| M4 | 4 weeks | W5 | W8 | Alpha/beta/GA rollout complete, observability active, success metrics validated |

**Total estimated duration:** 8 weeks

## Open Questions

| # | Question | Impact | Blocking Milestone | Resolution Owner |
|---|---|---|---|---|
| 1 | OQ-001: Should `AuthService` support API key authentication for service-to-service calls? | Affects future auth boundary and whether non-user callers are in v1.0 | M2 | test-lead |
| 2 | OQ-002: What is the maximum allowed `UserProfile.roles` array length? | Affects schema validation and JWT payload sizing | M1 | auth-team |
| 3 | OQ-003: TDD says 90-day audit retention while PRD requires 12 months; which policy is authoritative in implementation artifacts? | Blocks audit schema, storage planning, and compliance acceptance | M1 | compliance + auth-team |
| 4 | OQ-004: Should password reset email delivery be synchronous or asynchronous? | Changes API latency and email integration design | M2 | Engineering |
| 5 | OQ-005: Maximum number of refresh tokens allowed per user across devices? | Affects Redis keying, revocation rules, and AuthProvider UX | M1 | Product |
| 6 | OQ-006: Confirm final account lockout policy beyond the current 5 attempts / 15 minutes default? | Impacts security UX, gateway policy, and admin visibility | M1 | Security |
| 7 | OQ-007: Support a remember-me option to extend session duration? | Affects frontend session UX and token lifecycle expectations | M3 | Product |
| 8 | OQ-008: Are admin event-log viewing and lock/unlock controls part of v1.0 scope? | Determines whether Jordan's PRD JTBD is delivered or formally deferred | M3 | Product + auth-team |
| 9 | PRD gap fill: Should logout remain implemented even though it was omitted from the extracted API inventory? | PRD in-scope capability requires explicit backend and frontend coverage | M2 | product-team |
| 10 | PRD gap fill: If admin APIs are deferred, where is the follow-up TDD update tracked? | Prevents silent scope drift and missing Jordan persona coverage | M3 | product-team + auth-team |
