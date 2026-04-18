---
spec_source: "test-spec-user-auth.md"
complexity_score: 0.6
complexity_class: MEDIUM
primary_persona: architect
adversarial: false
base_variant: "none"
variant_scores: "none"
convergence_score: none
debate_rounds: none
generated: "2026-04-15"
generator: "single"
total_phases: 5
total_task_rows: 82
risk_count: 9
open_questions: 11
---

# User Authentication Service — Project Roadmap

## Executive Summary

This roadmap delivers a centralized User Authentication Service replacing ad-hoc credential handling across the platform. The service implements JWT-based stateless sessions via `AuthService` orchestrating `TokenManager`, `JwtService`, and `PasswordHasher`, backed by PostgreSQL for user persistence and Redis for refresh token management. Five REST endpoints (`/auth/login`, `/auth/register`, `/auth/me`, `/auth/refresh`, `/auth/reset-*`) serve three personas: Alex (end user), Sam (API consumer), and Jordan (platform admin). Frontend integration delivers `LoginPage`, `RegisterPage`, `ProfilePage`, and `AuthProvider` context wrapper.

**Business Impact:** Authentication unblocks ~$2.4M in projected annual revenue from personalization-dependent features. Compliance prerequisite for SOC2 Type II audit (Q3 2026 deadline). Addresses 25% churn attributed to missing user accounts.

**Complexity:** MEDIUM (0.6) — Elevated security sensitivity (password hashing, JWT signing, token rotation, replay detection) offset by bounded scope (5 FRs), standard architectural patterns, and well-defined data models.

**Critical path:** PasswordHasher + JwtService (parallel) → TokenManager → AuthService → AuthMiddleware → Routes/Migrations → Frontend Integration → Phased Rollout

**Key architectural decisions:**

- JWT with RS256 asymmetric signing for stateless cross-service verification; access tokens in memory, refresh tokens in httpOnly cookies
- bcrypt cost factor 12 via `PasswordHasher` abstraction for future algorithm migration (Argon2id path documented)
- Refresh token rotation with replay detection in Redis; suspicious reuse triggers full user token revocation
- Layered architecture with dependency injection: AuthService → TokenManager/PasswordHasher → JwtService, all independently testable

**Open risks requiring resolution before Phase 1:**

- Rate limit conflict: spec defines 5 req/min/IP for login vs. TDD defines 10 req/min/IP (Open Question #7 — must reconcile)
- Data model divergence: spec `UserRecord` (snake_case) vs. TDD `UserProfile` (camelCase) with additional fields (Open Question #8 — schema must be finalized)
- Refresh token storage: spec specifies PostgreSQL vs. TDD specifies Redis (Open Question #11 — architectural decision required)

## Phase 1: Foundation (Infrastructure & Data Layer)

**Objective:** Provision database schemas, crypto infrastructure, repository layer, and dev environment | **Duration:** 1.5 weeks | **Entry:** Rate limit conflict and data model divergence resolved (OQ #7, #8, #11) | **Exit:** Migration scripts pass up/down; UserRepo CRUD operational; RSA keys provisioned; Docker Compose dev env healthy

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | COMP-012 | Create auth database migration script | DB | — | users+refresh_tokens tables created; up/down scripts pass; idempotent execution | M | P0 |
| 2 | DM-001 | Implement UserRecord/UserProfile schema | DB | COMP-012 | id:UUID-PK; email:unique-idx-lowercase; displayName:varchar(2-100); password_hash:varchar; is_locked:bool-default-false; created_at:timestamptz; updated_at:timestamptz; lastLoginAt:timestamptz-nullable; roles:text[]-default-["user"] | M | P0 |
| 3 | DM-002 | Implement RefreshTokenRecord schema | DB | COMP-012 | id:UUID-PK; user_id:FK→users.id-cascade; token_hash:varchar(SHA-256); expires_at:timestamptz; revoked:bool-default-false; created_at:timestamptz | M | P0 |
| 4 | DM-003 | Define AuthToken response interface | Auth | — | accessToken:JWT-string; refreshToken:opaque-string; expiresIn:number(900); tokenType:string("Bearer") | S | P0 |
| 5 | COMP-010 | Implement UserRepo CRUD layer | DB | DM-001 | create/findByEmail/findById/updateLastLogin/lockAccount methods; pg-pool connection pooling; parameterized queries | M | P0 |
| 6 | NFR-SEC-002 | Generate RS256 2048-bit RSA key pair | Sec | — | private key in secrets manager; public key for verification; rotation procedure documented; no plaintext export | S | P0 |
| 7 | COMP-015 | Configure Docker Compose dev env | Infra | — | PostgreSQL 15+, Redis 7+, Node.js 20 LTS containers; healthy on `docker-compose up`; ports mapped | M | P1 |
| 8 | COMP-016 | Configure CI pipeline with testcontainers | Infra | COMP-015 | ephemeral PostgreSQL+Redis per run; Jest executes; coverage report generated; <5min pipeline | M | P1 |
| 9 | SEC-001 | Enforce TLS 1.3 on all endpoints | Sec | — | HTTP connections reject TLS<1.3; cert validation passes; HSTS header present | S | P0 |
| 10 | SEC-002 | Configure CORS origin whitelist | Sec | — | known frontend origins only; preflight 200; unknown origins→403; config externalized | S | P1 |
| 11 | COMP-017 | Set up API versioning prefix /v1/auth | API | — | all auth routes under `/v1/auth/*`; versioning middleware active; non-versioned→404 | S | P1 |
| 12 | NFR-004 | Enforce GDPR data minimization in schema | DB | DM-001 | only email, password_hash, displayName collected; no additional PII columns; schema audit passes | S | P1 |
| 13 | COMP-013 | Configure API Gateway rate limiting | Infra | — | per-IP rate limits enforced; 429 on threshold breach; config externalized; bypass for health checks | M | P0 |

### Integration Points — Phase 1

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| UserRepo → PostgreSQL connection pool | DI/Config | Phase 1 | Phase 1 | COMP-001 (AuthService), COMP-005 (AuthMiddleware) |
| RSA key pair → secrets manager mount | Config | Phase 1 | Phase 2 | COMP-003 (JwtService) |
| Docker Compose → CI pipeline | Config | Phase 1 | Phase 4 | TEST-001 through TEST-009 |
| API Gateway rate limiter → route middleware | Middleware chain | Phase 1 | Phase 3 | API-001 through API-006 |

## Phase 2: Core Logic (Service Implementation)

**Objective:** Implement PasswordHasher, JwtService, TokenManager, and AuthService with all FR flows | **Duration:** 2 weeks | **Entry:** Phase 1 exit criteria met; database schemas deployed; RSA keys available | **Exit:** All AuthService methods pass unit tests; login/register/refresh/reset flows operational in isolation

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 14 | COMP-004 | Implement PasswordHasher module | Auth | — | hash()/verify() methods; bcrypt cost-12; configurable; <500ms/hash; pure utility | M | P0 |
| 15 | NFR-AUTH.3 | Validate bcrypt cost factor 12 | Auth | COMP-004 | unit test asserts cost=12; benchmark <500ms; hash verifiable by bcrypt.compare | S | P0 |
| 16 | NFR-003 | Verify NIST SP 800-63B compliance | Sec | COMP-004 | one-way adaptive hash; no plaintext storage/logging; cost meets OWASP minimum | S | P0 |
| 17 | FR-AUTH.2b | Store bcrypt hash with cost factor 12 | Auth | COMP-004 | PasswordHasher.hash() outputs bcrypt; cost-12 in prefix; NIST-compliant | S | P0 |
| 18 | COMP-003 | Implement JwtService module | Auth | NFR-SEC-002 | sign/verify RS256; 2048-bit RSA; expired→rejected; 5s clock skew tolerance | M | P0 |
| 19 | FR-AUTH.1b | Reconcile login rate limit conflict | API | — | 5-vs-10 req/min/IP decision documented; single limit implemented consistently | S | P0 |
| 20 | COMP-002 | Implement TokenManager module | Auth | COMP-003 | issueTokens/refresh/revoke; access 15min TTL; refresh 7d TTL; hashes in Redis | L | P0 |
| 21 | FR-AUTH.3a | Store refresh tokens in Redis with TTL | Auth | COMP-002 | Redis stores SHA-256 hashed tokens; 7d TTL auto-expires; revocation supported | M | P0 |
| 22 | FR-AUTH.3 | Implement token refresh with rotation | Auth | COMP-002 | valid-refresh→new-pair+revoke-old; expired→401; revoked→invalidate-all-user | M | P0 |
| 23 | FR-AUTH.3b | Enforce 30 req/min refresh rate limit | API | COMP-002 | rate limiter on POST /auth/refresh; 429 on breach; per-user via token claims | S | P1 |
| 24 | COMP-001 | Implement AuthService orchestrator | Auth | COMP-002, COMP-004, COMP-010 | login/register/refresh/reset methods; DI for all deps; no direct DB access | L | P0 |
| 25 | FR-AUTH.1 | Implement login flow in AuthService | Auth | COMP-001 | valid-creds→200+AuthToken; invalid→401; locked→403/423; no enumeration | M | P0 |
| 26 | FR-AUTH.1a | Implement account lockout after 5 fails | Auth | COMP-001 | 5 failed/15min→is_locked=true; 423 response; counter reset on success | M | P0 |
| 27 | FR-AUTH.1c | Return 423 Locked for locked accounts | Auth | FR-AUTH.1a | locked-login→423; suspension msg; no token issued; no enumeration | S | P0 |
| 28 | FR-AUTH.2 | Implement registration in AuthService | Auth | COMP-001 | valid-data→201+UserProfile; dup-email→409; weak-pw→400; email validated | M | P0 |
| 29 | FR-AUTH.2a | Normalize email to lowercase on register | Auth | FR-AUTH.2 | emails stored lowercase; case-insensitive lookup; idempotent; indexed | S | P1 |
| 30 | FR-AUTH.2c | Return full UserProfile on registration | Auth | FR-AUTH.2 | id, email, displayName, createdAt, updatedAt, lastLoginAt(null), roles | S | P1 |
| 31 | FR-AUTH.4 | Implement profile retrieval | Auth | COMP-001 | valid-Bearer→UserProfile; expired/invalid→401; sensitive fields excluded | M | P0 |
| 32 | FR-AUTH.4a | Include extended profile fields | Auth | FR-AUTH.4 | response adds updatedAt, lastLoginAt, roles beyond spec minimum | S | P1 |
| 33 | FR-AUTH.4b | Enforce 60 req/min profile rate limit | API | FR-AUTH.4 | rate limiter on GET /auth/me; 429 on breach; per-user tracking | S | P1 |
| 34 | FR-AUTH.5 | Implement password reset flow | Auth | COMP-001 | reset-request→email-1h-token; reset-confirm→new-pw; sessions invalidated | L | P0 |
| 35 | FR-AUTH.5a | Ensure reset tokens are single-use | Auth | FR-AUTH.5 | used-token→400; consumed after use; replay→error | S | P0 |
| 36 | FR-AUTH.5b | Prevent email enumeration on reset | Auth | FR-AUTH.5 | same 200 regardless of registration; no timing side-channel | S | P1 |
| 37 | COMP-014 | Implement standard error response format | API | — | {error:{code,message,status}} JSON; AUTH_* codes; all endpoints consistent | M | P1 |

### Integration Points — Phase 2

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| PasswordHasher → AuthService DI binding | DI | Phase 2 | Phase 2 | COMP-001 (login, register) |
| JwtService → TokenManager DI binding | DI | Phase 2 | Phase 2 | COMP-002 (issueTokens, refresh) |
| TokenManager → AuthService DI binding | DI | Phase 2 | Phase 2 | COMP-001 (login, refresh) |
| UserRepo → AuthService DI binding | DI | Phase 2 | Phase 2 | COMP-001 (register, getProfile) |
| TokenManager → Redis client connection | Config | Phase 2 | Phase 2 | COMP-002 (refresh token CRUD) |
| Error response format → API handlers | Middleware | Phase 2 | Phase 3 | API-001 through API-006 |

## Phase 3: Integration (API, Middleware, Frontend)

**Objective:** Wire API endpoints, auth middleware, frontend components, and validate end-to-end flows | **Duration:** 2 weeks | **Entry:** All AuthService methods operational; unit tests passing | **Exit:** All API endpoints return correct responses; LoginPage/RegisterPage functional; AuthProvider handles silent refresh; p95 latency validated

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 38 | COMP-005 | Implement AuthMiddleware | Auth | COMP-002 | Bearer extraction; JwtService verify; decoded claims on req; 401 on invalid/expired | M | P0 |
| 39 | COMP-011 | Register /auth/* route group | API | COMP-001 | all auth endpoints routed; middleware on protected; 404 on unknown paths | M | P0 |
| 40 | API-001 | Wire POST /auth/login endpoint | API | COMP-011, FR-AUTH.1 | req-validation>AuthService.login>AuthToken; 200/401/423/429 correct | M | P0 |
| 41 | API-002 | Wire POST /auth/register endpoint | API | COMP-011, FR-AUTH.2 | req-validation>AuthService.register>UserProfile; 201/400/409 correct | M | P0 |
| 42 | API-003 | Wire GET /auth/me endpoint | API | COMP-011, COMP-005 | middleware-auth>AuthService.getProfile>UserProfile; 200/401 correct | M | P0 |
| 43 | API-004 | Wire POST /auth/refresh endpoint | API | COMP-011, FR-AUTH.3 | refreshToken>TokenManager.refresh>new AuthToken; 200/401 correct | M | P0 |
| 44 | API-005 | Wire POST /auth/reset-request | API | COMP-011, FR-AUTH.5 | email>AuthService.resetRequest>confirmation; email dispatched; same response | M | P0 |
| 45 | API-006 | Wire POST /auth/reset-confirm | API | COMP-011, FR-AUTH.5 | token+pw>AuthService.resetConfirm>success; sessions invalidated; 200/400 | M | P0 |
| 46 | COMP-006 | Build LoginPage component | FE | COMP-008 | email+pw fields; POST /auth/login; AuthToken via AuthProvider; error display | L | P0 |
| 47 | COMP-007 | Build RegisterPage component | FE | COMP-008 | email+pw+displayName; client-side pw validation; POST /auth/register; redirect | L | P0 |
| 48 | COMP-008 | Build AuthProvider context wrapper | FE | COMP-002 | AuthToken state; silent refresh; UserProfile exposed; tab-close clears; 401 intercept | L | P0 |
| 49 | COMP-009 | Build ProfilePage component | FE | COMP-008 | displays displayName, email, createdAt; GET /auth/me; auth required; loading state | M | P1 |
| 50 | NFR-001 | Add GDPR consent capture at registration | FE | COMP-007 | consent checkbox; timestamp recorded; register blocked without consent | M | P1 |
| 51 | NFR-AUTH.1 | Validate <200ms p95 login latency | API | API-001 | k6 confirms p95<200ms; APM baseline established; dashboard metric visible | M | P0 |
| 52 | NFR-PERF-002 | Validate 500 concurrent login capacity | API | API-001 | k6 sustains 500 concurrent; no 5xx; p95<200ms under load; pool stable | M | P0 |

### Integration Points — Phase 3

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| AuthMiddleware → route middleware chain | Middleware chain | Phase 3 | Phase 3 | API-003 (GET /auth/me), protected routes |
| AuthService → route handler dispatch | Dispatch table | Phase 3 | Phase 3 | API-001 through API-006 |
| AuthProvider → LoginPage/RegisterPage context | React context | Phase 3 | Phase 3 | COMP-006, COMP-007, COMP-009 |
| AuthProvider → TokenManager silent refresh | Event callback | Phase 3 | Phase 3 | COMP-008 (access token expiry handler) |
| CORS config → API Gateway | Config | Phase 1 | Phase 3 | All /auth/* endpoints |
| Rate limiter per-endpoint config | Registry | Phase 1 | Phase 3 | API-001, API-002, API-004 |

## Phase 4: Hardening (Security, Testing, Compliance)

**Objective:** Achieve test coverage targets, validate security posture, implement compliance logging, and complete performance benchmarks | **Duration:** 1.5 weeks | **Entry:** All API endpoints functional; frontend components rendering; basic happy-path flows working | **Exit:** Unit coverage >80% for core modules; integration tests pass against real PostgreSQL+Redis; security review complete; SOC2 audit logging operational

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 53 | TEST-001 | Write PasswordHasher unit tests | Test | COMP-004 | hash produces bcrypt; verify matches; cost-12 asserted; timing <500ms | M | P0 |
| 54 | TEST-002 | Write JwtService unit tests | Test | COMP-003 | sign produces valid JWT; verify rejects expired; RS256 confirmed; clock skew | M | P0 |
| 55 | TEST-003 | Write TokenManager unit tests | Test | COMP-002 | issueTokens returns pair; refresh rotates; revoked rejected; replay detected | M | P0 |
| 56 | TEST-004 | Write AuthService unit tests | Test | COMP-001 | login valid/invalid; register valid/dup; profile; reset request/confirm; lockout | L | P0 |
| 57 | TEST-005 | Integration: registration persists to DB | Test | API-002 | full HTTP>DB insert; UserProfile retrievable; password hashed; 201 returned | M | P0 |
| 58 | TEST-006 | Integration: expired refresh rejected | Test | API-004 | Redis TTL expires; 401 returned; user must re-authenticate; no stale token | M | P0 |
| 59 | TEST-007 | E2E: register>login>profile flow | Test | COMP-006, COMP-007 | Playwright: RegisterPage>LoginPage>ProfilePage; tokens valid; data consistent | L | P0 |
| 60 | TEST-008 | Execute k6 load test suite | Test | API-001 | 500 concurrent; p95<200ms; no 5xx; auth_login_duration_seconds metric ok | M | P1 |
| 61 | SEC-003 | Document RSA key rotation procedure | Sec | NFR-SEC-002 | 90-day rotation; runbook written; zero-downtime rotation verified in staging | M | P1 |
| 62 | SEC-004 | Validate sensitive field log exclusion | Sec | — | password, tokens excluded from all log output; grep verification passes | S | P0 |
| 63 | NFR-AUTH.2 | Validate 99.9% uptime target | Ops | — | health check endpoint responds; uptime monitor configured; PagerDuty wired | M | P0 |
| 64 | NFR-002 | Implement SOC2 audit event logging | Auth | COMP-001 | login/register/refresh/reset logged with userId, timestamp, IP, outcome; 12mo retention | L | P0 |
| 65 | TEST-009 | Configure test Docker Compose env | Test | COMP-015 | PostgreSQL+Redis testcontainers; ephemeral per-run; CI-compatible; <3min startup | M | P1 |
| 66 | TEST-010 | Seed staging test accounts | Test | — | pre-created accounts; known credentials; automated smoke tests pass | S | P1 |
| 67 | TEST-011 | Execute security penetration test | Sec | Phase 3 | OWASP top-10 verified; no injection; no enumeration; token handling secure | L | P1 |
| 68 | TEST-012 | Validate password policy compliance | Test | FR-AUTH.2 | NIST 800-63B: 8+ chars, upper+lower+digit; weak passwords rejected; edge cases | S | P0 |

### Integration Points — Phase 4

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| Audit logger → AuthService event hooks | Event binding | Phase 4 | Phase 4 | NFR-002 (all auth events) |
| Audit logger → PostgreSQL audit table | Config | Phase 4 | Phase 4 | NFR-002 (90-day retention) |
| k6 test scripts → CI pipeline | Config | Phase 4 | Phase 5 | MIG-001, MIG-002 (load validation) |
| Penetration test results → security review | Report | Phase 4 | Phase 5 | MIG-001 (alpha gate) |

## Phase 5: Production Readiness (Rollout & Operations)

**Objective:** Execute phased rollout from alpha through GA; establish monitoring, alerting, runbooks, and on-call rotation | **Duration:** 4 weeks (1 alpha + 2 beta + 1 GA) | **Entry:** Phase 4 exit criteria met; zero P0/P1 bugs; security review passed; audit logging operational | **Exit:** 99.9% uptime over 7 days in production; feature flags removed; monitoring dashboards green; on-call rotation active

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 69 | MIG-004 | Configure AUTH_NEW_LOGIN feature flag | Ops | — | flag defaults OFF; toggleable without deploy; routes gated; rollback-safe | S | P0 |
| 70 | MIG-005 | Configure AUTH_TOKEN_REFRESH flag | Ops | — | flag defaults OFF; refresh gated; access-only mode when OFF; independent toggle | S | P0 |
| 71 | MIG-001 | Execute Internal Alpha deployment | Ops | Phase 4 | AuthService on staging; auth-team+QA test all endpoints; zero P0/P1; 1-week | L | P0 |
| 72 | MIG-002 | Execute Beta 10% traffic rollout | Ops | MIG-001 | AUTH_NEW_LOGIN at 10%; p95<200ms; error<0.1%; Redis stable; 2-week soak | XL | P0 |
| 73 | MIG-003 | Execute GA 100% rollout | Ops | MIG-002 | flag removed; all traffic via AuthService; 99.9% uptime over 7 days | L | P0 |
| 74 | MIG-006 | Validate rollback procedure in staging | Ops | MIG-001 | disable flag>legacy active; smoke tests pass; rollback <5min; tested twice | M | P0 |
| 75 | MIG-007 | Create down-migration scripts | DB | COMP-012 | users+refresh_tokens droppable; idempotent down-migration; tested in staging | M | P1 |
| 76 | OPS-001 | Write AuthService-down runbook | Ops | — | diagnosis steps; pod restart; PostgreSQL failover; Redis fallback; escalation | M | P0 |
| 77 | OPS-002 | Write token-refresh-failure runbook | Ops | — | Redis check; JwtService key check; feature flag verify; escalation path | M | P0 |
| 78 | OPS-003 | Configure Grafana monitoring dashboards | Ops | NFR-002 | auth_login_total; auth_login_duration_seconds; auth_token_refresh_total; auth_registration_total | M | P0 |
| 79 | OPS-004 | Configure alerting rules in PagerDuty | Ops | OPS-003 | login-fail>20%/5min; p95>500ms; Redis-fail>10/min; auto-page on-call | M | P0 |
| 80 | OPS-005 | Establish on-call rotation | Ops | — | 24/7 for 2 weeks post-GA; auth-team rotation; 15-min acknowledge SLA | S | P1 |
| 81 | OPS-006 | Complete capacity planning review | Ops | — | 3>10 pods HPA; 100>200 pg-pool; Redis 1>2GB threshold; scaling triggers doc | M | P1 |
| 82 | OPS-007 | Automate rollback criteria monitoring | Ops | MIG-006 | p95>1000ms/5min; error>5%/2min; Redis-fail>10/min triggers alert; manual decision | M | P1 |

### Integration Points — Phase 5

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| AUTH_NEW_LOGIN flag → route middleware | Feature flag | Phase 5 | Phase 5 | API-001, API-002 (traffic gating) |
| AUTH_TOKEN_REFRESH flag → TokenManager | Feature flag | Phase 5 | Phase 5 | COMP-002 (refresh flow gating) |
| Grafana dashboards → PagerDuty alerts | Callback | Phase 5 | Phase 5 | OPS-004 (alert triggers) |
| Rollback criteria → monitoring automation | Strategy pattern | Phase 5 | Phase 5 | OPS-007 (threshold checks) |
| Down-migration → rollback procedure | Dependency | Phase 5 | Phase 5 | MIG-006 (data layer rollback) |

## Risk Assessment and Mitigation

| # | Risk | Severity | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|---|---|
| 1 | JWT private key compromise allows forged tokens | Critical | Low | High | RS256 asymmetric keys; private key in secrets manager; 90-day rotation; key never in logs/env | sec-reviewer |
| 2 | Refresh token replay attack after theft | Critical | Medium | High | Token rotation with replay detection; suspicious reuse revokes all user tokens; Redis hash storage | auth-team |
| 3 | bcrypt cost factor insufficient for future hardware | Medium | Low | Medium | Configurable cost in PasswordHasher; annual OWASP review; Argon2id migration path documented | auth-team |
| 4 | XSS-based token theft enables session hijack | Critical | Medium | High | Access token in memory only (not localStorage); httpOnly cookie for refresh; 15-min expiry; AuthProvider clears on tab close | sec-reviewer |
| 5 | Brute-force attacks on login endpoint | High | High | Medium | API Gateway rate limit (resolved per OQ #7); account lockout 5-fail/15min; bcrypt cost-12 slows offline cracking | auth-team |
| 6 | Data loss during legacy auth migration | High | Low | High | Parallel run Phase 1-2; idempotent upsert; full DB backup before each phase; rollback procedure validated | platform-team |
| 7 | Low registration adoption due to poor UX | High | Medium | High | Usability testing before launch; funnel analytics on RegisterPage; iterate based on >60% conversion target | product-team |
| 8 | Incomplete audit logging fails SOC2 compliance | High | Medium | High | Define log schema in Phase 4 (NFR-002); validate against SOC2 controls in QA; 12-month retention verified | auth-team |
| 9 | Email delivery failures block password reset | Medium | Low | Medium | SendGrid delivery monitoring; alerting on failure rate; fallback support channel for manual resets | platform-team |

## Resource Requirements and Dependencies

### External Dependencies

| Dependency | Required By Phase | Status | Fallback |
|---|---|---|---|
| PostgreSQL 15+ | Phase 1 | Available | None — critical path; service non-functional without it |
| Redis 7+ | Phase 1 | Available | Reject refresh requests; users re-login on access expiry |
| Node.js 20 LTS | Phase 1 | Available | None — runtime requirement |
| bcryptjs library | Phase 2 | Available (npm) | bcrypt native module (requires build tools) |
| jsonwebtoken library | Phase 2 | Available (npm) | jose library (standards-compliant alternative) |
| SendGrid API | Phase 2 | Requires provisioning | Manual password reset via support channel |
| Frontend routing framework | Phase 3 | Available | None — auth pages cannot render without routing |
| SEC-POLICY-001 policy document | Phase 1 | Pending review | Use OWASP defaults for password/token policies |

### Infrastructure Requirements

- 3 Kubernetes pods for AuthService (HPA to 10 based on CPU >70%) — est. $150/month
- Managed PostgreSQL with 100-connection pool (scale to 200 if wait >50ms) — est. $200/month
- Managed Redis 1GB (scale to 2GB if >70% utilized; ~100K refresh tokens = ~50MB) — est. $100/month
- RSA 2048-bit key pair stored in cloud secrets manager with quarterly rotation
- Docker Compose for local dev; testcontainers for CI ephemeral environments
- k6 load testing infrastructure for 500 concurrent user simulation
- Grafana + Prometheus for monitoring; PagerDuty for alerting
- Total estimated infrastructure: $450/month production; scales ~$50/month per 10K users

## Success Criteria and Validation Approach

| Criterion | Metric | Target | Validation Method | Phase |
|---|---|---|---|---|
| Login performance | p95 response time | < 200ms | k6 load test + APM on AuthService.login() | Phase 3 |
| Registration reliability | Success rate | > 99% | Ratio of successful registrations to attempts | Phase 3 |
| Token refresh speed | p95 refresh latency | < 100ms | APM on TokenManager.refresh() | Phase 3 |
| Service uptime | Availability | 99.9% (30-day rolling) | Health check monitoring + PagerDuty | Phase 5 |
| Password hash timing | PasswordHasher.hash() | < 500ms | Benchmark test with bcrypt cost-12 | Phase 2 |
| Registration conversion | Funnel completion | > 60% | Analytics: landing > register > confirmed | Phase 5 |
| Active users | Daily authenticated users | > 1000 within 30d of GA | AuthToken issuance count | Phase 5 |
| Session engagement | Average session duration | > 30 minutes | Token refresh event analytics | Phase 5 |
| Login failure rate | Failed login ratio | < 5% of attempts | Auth event log analysis | Phase 5 |
| Password reset completion | Reset funnel | > 80% | Funnel: reset requested > new password set | Phase 5 |
| Test coverage | Unit test coverage | > 80% for core modules | Jest coverage report for AuthService, TokenManager, JwtService, PasswordHasher | Phase 4 |

## Timeline Estimates

| Phase | Duration | Start | End | Key Milestones |
|---|---|---|---|---|
| Phase 1: Foundation | 1.5 weeks | 2026-04-21 | 2026-05-02 | DB migration, UserRepo, RSA keys, Docker Compose, CI pipeline |
| Phase 2: Core Logic | 2 weeks | 2026-05-05 | 2026-05-16 | PasswordHasher, JwtService, TokenManager, AuthService, all FR flows |
| Phase 3: Integration | 2 weeks | 2026-05-19 | 2026-05-30 | API endpoints, AuthMiddleware, LoginPage, RegisterPage, AuthProvider |
| Phase 4: Hardening | 1.5 weeks | 2026-06-02 | 2026-06-11 | Unit/integration/E2E tests, security review, SOC2 logging, load tests |
| Phase 5: Production Readiness | 4 weeks | 2026-06-12 | 2026-07-10 | Alpha (1w), Beta 10% (2w), GA 100% (1w), monitoring, runbooks |

**Total estimated duration:** 11 weeks (2026-04-21 to 2026-07-10)

Note: Phase 5 duration is dominated by the phased rollout soak periods (1w alpha + 2w beta + 1w GA stabilization). Phases 1-4 represent 7 weeks of active development. Timeline assumes OQ #7 (rate limit), OQ #8 (data model), and OQ #11 (refresh storage) are resolved before Phase 1 entry.

## Open Questions

| # | Question | Impact | Blocking Phase | Resolution Owner |
|---|---|---|---|---|
| 1 | Should password reset emails be synchronous or via message queue? | Affects reset endpoint latency and resilience | Phase 2 | Engineering |
| 2 | Maximum active refresh tokens per user? | Storage requirements; multi-device support | Phase 2 | Product |
| 3 | Should AuthService support API key auth for service-to-service? | AuthMiddleware interface design; deferred to v1.1 | None (v1.1) | test-lead |
| 4 | Maximum UserProfile roles array length? | Schema constraint; pending RBAC design | None (v1.1) | auth-team |
| 5 | Account lockout policy: progressive or fixed threshold? | Spec rate-limits 5/min/IP but lacks progressive lockout | Phase 2 | Security |
| 6 | Should "remember me" extend session duration? | Refresh token TTL; UX impact | Phase 2 | Product |
| 7 | Rate limit conflict: spec 5 req/min/IP vs TDD 10 req/min/IP for login | Single value must be chosen before implementation | Phase 1 (blocking) | Engineering |
| 8 | Data model: spec UserRecord (snake_case) vs TDD UserProfile (camelCase); TDD adds lastLoginAt, roles | Schema must be finalized before migration | Phase 1 (blocking) | Engineering |
| 9 | Logout FR missing: PRD scope includes logout but spec has no FR | JTBD #2 and persona Alex expect logout; missing requirement | Phase 2 | Product/Engineering |
| 10 | Admin audit log querying: PRD persona Jordan requires it; no spec FR | SOC2 compliance (NFR-002) depends on queryable logs | Phase 4 | Product/Engineering |
| 11 | Refresh token storage: spec says PostgreSQL vs TDD says Redis | Architectural decision affects revocation strategy and performance | Phase 1 (blocking) | Engineering |
