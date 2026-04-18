---
spec_source: "test-tdd-user-auth.md"
complexity_score: 0.65
complexity_class: MEDIUM
primary_persona: architect
adversarial: false
base_variant: "none"
variant_scores: "none"
convergence_score: null
debate_rounds: null
generated: "2026-04-16"
generator: "single"
total_phases: 7
total_task_rows: 88
risk_count: 6
open_questions: 12
---

# User Authentication Service -- Project Roadmap

## Executive Summary

This roadmap delivers a secure, production-grade user authentication service spanning registration, login, logout, JWT-based session persistence, profile retrieval, and self-service password reset. The system is built on a stateless JWT architecture (RS256) with PostgreSQL for user persistence, Redis for refresh token management, and SendGrid for transactional email. The implementation follows a facade pattern with `AuthService` orchestrating `TokenManager`, `PasswordHasher`, and `UserRepo` -- designed for future extensibility toward OAuth2 and MFA without breaking changes.

The roadmap is structured across 7 phases over approximately 9 weeks: infrastructure foundation, data layer and security modules, backend service and API layer, frontend implementation, testing and quality assurance, staged migration and rollout, and operations and observability. Each phase has explicit entry/exit criteria and rollback procedures.

**Business Impact:** Authentication unblocks ~$2.4M in projected annual revenue from personalization-dependent features (Q2-Q3 2026 roadmap). It is also a prerequisite for SOC2 Type II audit compliance scheduled for Q3 2026. 25% of churned users cite the absence of user accounts as a reason for leaving.

**Complexity:** MEDIUM (0.65) -- Well-scoped single-service feature with moderate complexity driven by security criticality (bcrypt, RS256, token revocation, account lockout), dual-store architecture (PostgreSQL + Redis), and three-phase rollout with feature flags.

**Critical path:** INFRA-001/002 -> DM-001 -> COMP-005 -> COMP-004 -> COMP-003 -> COMP-001/002 -> FR-AUTH-001/002/003 -> API-001/002/004 -> TEST-004/005 -> MIG-001 -> MIG-002 -> MIG-003

**Key architectural decisions:**

- Stateless JWT with RS256 signing (no server-side sessions) -- access tokens in memory only, refresh tokens as HttpOnly cookies backed by Redis, enabling horizontal scaling without session affinity
- Facade pattern for `AuthService` with explicit interface boundaries to `TokenManager`, `PasswordHasher`, and `UserRepo` -- accommodates future OAuth2/MFA providers without breaking the API contract (AC-011)
- Three-phase rollout (alpha -> 10% beta -> GA) with feature flags `AUTH_NEW_LOGIN` and `AUTH_TOKEN_REFRESH` providing instant rollback capability at each stage

**Open risks requiring resolution before Phase 1:**

- OQ-003: Audit log retention discrepancy (TDD: 90 days vs PRD: 12 months) must be resolved with compliance team -- affects DM-003 schema and storage planning
- OQ-004: Logout endpoint omitted from TDD but in PRD scope -- this roadmap includes API-007 as a gap fill; TDD should be updated
- OQ-009: GDPR consent mechanism at registration has no implementation design -- must be designed before Phase 3 NFR-COMP-001 task

## Phase 1: Infrastructure Foundation

**Objective:** Provision all infrastructure dependencies, generate cryptographic material, and establish the project scaffold with security baselines. | **Duration:** 1 week | **Entry:** SEC-POLICY-001 draft available; infrastructure access provisioned | **Exit:** PostgreSQL 15+ and Redis 7+ clusters healthy; TLS 1.3 enforced; RS256 key pair generated and mounted; /v1/auth/* routing active; Docker Compose dev environment operational

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | INFRA-001 | Provision PostgreSQL 15+ cluster | Infra | -- | pg15+running; pool:100; connstring-in-env; backup-configured | M | P0 |
| 2 | INFRA-002 | Provision Redis 7+ cluster | Infra | -- | redis7+running; AUTH-enabled; persistence-off; 1GB-mem | M | P0 |
| 3 | INFRA-003 | Setup Node.js 20 LTS project scaffold | Infra | -- | node20-lts; package.json; tsconfig; eslint; project-structure | S | P0 |
| 4 | INFRA-004 | Generate RS256 2048-bit RSA key pair | Sec | -- | 2048bit-keypair; mounted-as-k8s-secret; quarterly-rotation-documented | S | P0 |
| 5 | INFRA-005 | Enforce TLS 1.3 on all endpoints | Sec | INFRA-003 | tls1.3-only; no-downgrade; cert-valid; HTTP-to-HTTPS-redirect | M | P0 |
| 6 | INFRA-006 | Configure CORS origin whitelist | Sec | INFRA-003 | known-origins->preflight-200; unknown-origin->blocked; no-wildcard | S | P1 |
| 7 | INFRA-007 | Setup /v1/auth/* URL prefix routing | API | INFRA-003 | v1-prefix-active; unversioned-path->404; middleware-chain-ready | S | P0 |
| 8 | INFRA-008 | Define password policy per NIST 800-63B | Sec | -- | min8+uppercase+number; no-plaintext-in-logs; policy-doc-approved | S | P0 |
| 9 | INFRA-009 | Configure Docker Compose dev environment | Infra | INFRA-001,INFRA-002 | pg+redis-in-compose; health-checks-pass; dev-startup<30s; testcontainers-compatible | M | P1 |

### Integration Points -- Phase 1

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| PostgreSQL connection pool (pg-pool) | Dependency injection | Phase 2 | COMP-005 | UserRepo, AuditLogger |
| Redis client singleton | Dependency injection | Phase 2 | COMP-002 | TokenManager, RateLimiter |
| RS256 key pair mount | Secret binding | Phase 2 | COMP-003 | JwtService |
| Express middleware chain | Middleware chain | Phase 3 | API-001 to API-008 | All API endpoints |
| CORS middleware | Middleware chain | Phase 1 | INFRA-007 | All API endpoints |

## Phase 2: Data Layer & Security Modules

**Objective:** Implement database schemas, data access layer, and cryptographic security modules. Validate all security invariants with unit tests. | **Duration:** 1.5 weeks | **Entry:** Phase 1 exit criteria met; PostgreSQL and Redis healthy | **Exit:** UserProfile, AuthToken, and AuditLog schemas deployed; UserRepo CRUD operational; PasswordHasher and JwtService passing all security validation tests; bcrypt cost 12 and RS256 2048-bit verified

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | DM-001 | Create UserProfile table in PostgreSQL | DB | INFRA-001 | id:UUID-PK; email:unique-idx-lowercase; display_name:varchar(100); created_at:timestamptz; updated_at:timestamptz; last_login_at:timestamptz-nullable; roles:text[]-default-["user"] | M | P0 |
| 2 | DM-002 | Define AuthToken response structure | API | -- | accessToken:JWT-string; refreshToken:string-unique; expiresIn:number-900; tokenType:string-"Bearer" | S | P0 |
| 3 | DM-003 | Create Audit Log table in PostgreSQL | DB | INFRA-001 | userId:UUID-NOT-NULL; eventType:varchar-NOT-NULL; timestamp:timestamptz-NOT-NULL; ipAddress:varchar-NOT-NULL; outcome:varchar-NOT-NULL; 12-month-retention-policy | M | P0 |
| 4 | COMP-005 | Build UserRepo data access layer | DB | DM-001 | findByEmail(); findById(); create(); update(); pg-pool-connection; parameterized-queries; no-SQL-injection | M | P0 |
| 5 | COMP-004 | Build PasswordHasher abstraction | Sec | INFRA-003 | hash(password)->bcrypt-string; verify(password,hash)->bool; cost-configurable; algorithm-swappable-interface | M | P0 |
| 6 | COMP-003 | Build JwtService sign/verify module | Sec | INFRA-004 | sign(payload)->JWT-RS256; verify(token)->payload-or-error; 5s-clock-skew-tolerance; key-rotation-support | M | P0 |
| 7 | NFR-SEC-001 | Validate bcrypt cost factor 12 | Sec | COMP-004 | config:cost=12; hash-prefix=$2b$12; unit-test-asserts-cost-parameter | S | P0 |
| 8 | NFR-SEC-002 | Validate RS256 2048-bit token signing | Sec | COMP-003 | JWT-header:alg=RS256; key>=2048bit; sign-then-verify-round-trip-passes | S | P0 |
| 9 | NFR-COMP-003 | Verify NIST SP 800-63B password storage | Sec | COMP-004 | one-way-hash-only; grep-all-log-sinks-no-raw-pwd; sanitize-error-messages | S | P0 |
| 10 | NFR-COMP-004 | Audit UserProfile schema data minimization | Sec | DM-001 | only:email+hash+displayName+roles+timestamps; roles[]-justification-documented; no-extra-PII | S | P1 |
| 11 | COMP-010 | Build AuditLogger service module | DB | DM-003 | log(event)->insert-audit-row; async-write; structured-JSON; covers-all-auth-event-types | M | P1 |
| 12 | COMP-011 | Build rate limiter middleware | API | INFRA-002 | per-IP-tracking; configurable-limits; 429-on-exceed; Redis-backed-counters | M | P0 |
| 13 | COMP-012 | Build account lockout manager | Sec | INFRA-002,COMP-005 | track-failed-attempts; lock-after-5-in-15min; unlock-after-cooldown; 423-response | M | P0 |
| 14 | COMP-013 | Build error response formatter | API | INFRA-003 | {error:{code,message,status}}-shape; consistent-across-endpoints; no-stack-traces-in-prod | S | P1 |

### Integration Points -- Phase 2

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| PasswordHasher.hash() / verify() | Strategy pattern | Phase 3 | COMP-001 | AuthService (login, register, reset-confirm) |
| JwtService.sign() / verify() | Strategy pattern | Phase 3 | COMP-002 | TokenManager |
| UserRepo CRUD methods | Dependency injection | Phase 3 | COMP-001 | AuthService |
| AuditLogger.log() | Event binding | Phase 3 | COMP-001 | AuthService (all auth events) |
| Rate limiter middleware | Middleware chain | Phase 3 | API-001 to API-008 | All API endpoints |
| Error response formatter | Middleware chain | Phase 3 | API-001 to API-008 | All API endpoints |
| Account lockout manager | Callback wiring | Phase 3 | FR-AUTH-001 | AuthService login flow |

## Phase 3: Backend Service & API Layer

**Objective:** Implement AuthService facade, TokenManager, all REST API endpoints, and wire functional/non-functional requirements. Integrate SendGrid for password reset. | **Duration:** 2 weeks | **Entry:** Phase 2 exit criteria met; all data models deployed; PasswordHasher, JwtService, UserRepo operational | **Exit:** All 8 API endpoints returning correct responses; FR-AUTH-001 through FR-AUTH-005 passing acceptance criteria; GDPR consent and SOC2 audit logging active; health check endpoint returning 200

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | COMP-001 | Build AuthService facade orchestrator | Auth | COMP-002,COMP-004,COMP-005 | delegates-to-TokenManager+PasswordHasher+UserRepo; facade-pattern; interface-extensible-for-OAuth/MFA-per-AC-011 | L | P0 |
| 2 | COMP-002 | Build TokenManager module | Auth | COMP-003,INFRA-002 | issueTokens()->AuthToken; refresh()->AuthToken; revoke(); Redis-storage; 15min-access/7day-refresh-TTL | L | P0 |
| 3 | FR-AUTH-001 | Implement login credential validation | Auth | COMP-001,COMP-004,COMP-012 | valid-creds->200+AuthToken; invalid->401; no-email-enum; 5fail/15min->423-locked | L | P0 |
| 4 | FR-AUTH-002 | Implement registration with validation | Auth | COMP-001,COMP-005 | valid-reg->201+UserProfile; dup-email->409; weak-pwd->400; bcrypt-cost-12-hash-stored | L | P0 |
| 5 | FR-AUTH-003 | Implement JWT issuance and refresh | Auth | COMP-002 | login->accessToken(15min)+refreshToken(7day); valid-refresh->new-pair+old-revoked; expired->401; revoked->401 | L | P0 |
| 6 | FR-AUTH-004 | Implement user profile retrieval | Auth | COMP-001,COMP-005 | valid-token->UserProfile{id,email,displayName,createdAt,updatedAt,lastLoginAt,roles}; invalid-token->401 | M | P0 |
| 7 | FR-AUTH-005 | Implement password reset flow | Auth | COMP-001,COMP-004,COMP-014 | request->email-sent; confirm->hash-updated; token-1hr-TTL; no-reuse; invalidate-all-sessions-per-PRD | L | P0 |
| 8 | API-001 | Implement POST /auth/login endpoint | API | FR-AUTH-001,COMP-011 | 200+AuthToken; 401-AUTH_INVALID_CREDENTIALS; 423-locked; 429-rate-limit; 10req/min/IP | M | P0 |
| 9 | API-002 | Implement POST /auth/register endpoint | API | FR-AUTH-002,COMP-011 | 201+UserProfile; 400-validation-errors; 409-email-conflict; 5req/min/IP | M | P0 |
| 10 | API-003 | Implement GET /auth/me endpoint | API | FR-AUTH-004,COMP-011 | 200+UserProfile; 401-missing/expired/invalid-token; Bearer-header; 60req/min/user | M | P0 |
| 11 | API-004 | Implement POST /auth/refresh endpoint | API | FR-AUTH-003,COMP-011 | 200+new-AuthToken; 401-expired/revoked; old-token-revoked-on-success; 30req/min/user | M | P0 |
| 12 | API-005 | Implement POST /auth/reset-request | API | FR-AUTH-005 | 200-always-regardless-of-email-existence; email-sent-if-registered; no-user-enumeration | M | P0 |
| 13 | API-006 | Implement POST /auth/reset-confirm | API | FR-AUTH-005 | valid-token->pwd-updated; expired-token->error; used-token->error; all-sessions-invalidated | M | P0 |
| 14 | API-007 | Implement POST /auth/logout endpoint | API | COMP-002 | revoke-refreshToken-in-Redis; clear-session; 200-on-success; PRD-gap-fill:TDD-update-needed | M | P1 |
| 15 | API-008 | Implement GET /admin/auth/logs query | API | COMP-010 | admin-role-required; filter-by-date+user+eventType; paginated-response; PRD-Jordan-persona-gap-fill | L | P1 |
| 16 | NFR-PERF-001 | Validate <200ms p95 API response time | Auth | API-001 | p95<200ms-all-auth-endpoints; APM-instrumented-on-AuthService-methods; baseline-established | M | P0 |
| 17 | NFR-PERF-002 | Validate 500 concurrent login support | Auth | API-001 | k6-load-test-500-concurrent; no-5xx-errors; latency-within-p95-SLA; connection-pool-stable | M | P0 |
| 18 | NFR-REL-001 | Implement health check for 99.9% SLA | Auth | COMP-001 | GET-/health->200; pg-connectivity-check; redis-connectivity-check; uptime-monitor-wired | S | P0 |
| 19 | NFR-COMP-001 | Implement GDPR consent at registration | Auth | API-002 | consent-field-required-on-register; timestamp-stored-with-consent; no-201-without-consent; audit-trail | M | P1 |
| 20 | NFR-COMP-002 | Implement SOC2 audit logging | Auth | COMP-010 | all-auth-events-logged; userId+timestamp+IP+outcome-per-event; 12-month-retention; structured-format | M | P0 |
| 21 | COMP-014 | Wire SendGrid email integration | Auth | -- | send-reset-email(to,token); delivery-monitoring; template-configured; rate-limit-aware; fallback-alert | M | P1 |
| 22 | COMP-015 | Build request validation middleware | API | INFRA-003 | validate-body-schema-per-endpoint; 400-on-invalid; sanitize-input; prevent-XSS-injection | M | P1 |

### Integration Points -- Phase 3

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| AuthService facade delegation table | Dispatch table | Phase 3 | COMP-001 | login->PasswordHasher+TokenManager; register->PasswordHasher+UserRepo; reset->PasswordHasher+SendGrid |
| TokenManager Redis token store | Registry | Phase 3 | COMP-002 | issueTokens writes; refresh reads+writes; revoke deletes |
| Feature flag AUTH_NEW_LOGIN | Dispatch/gate | Phase 6 | MIG-004 | API router (routes traffic to new vs legacy auth) |
| Feature flag AUTH_TOKEN_REFRESH | Dispatch/gate | Phase 6 | MIG-005 | TokenManager (enables/disables refresh flow) |
| SendGrid email callback | Callback wiring | Phase 3 | COMP-014 | FR-AUTH-005 password reset request |
| Request validation middleware | Middleware chain | Phase 3 | COMP-015 | All API endpoints |
| AuditLogger event binding | Event binding | Phase 3 | COMP-010 | AuthService emits on every auth event |

## Phase 4: Frontend Implementation

**Objective:** Build React frontend components for all auth flows: login, registration, profile, password reset, and logout. Implement AuthProvider context with silent token refresh and route guards. | **Duration:** 1.5 weeks | **Entry:** Phase 3 API endpoints returning correct responses; DM-002 AuthToken structure finalized | **Exit:** LoginPage, RegisterPage, ProfilePage, PasswordResetPage rendering correctly; AuthProvider managing token lifecycle; route guards protecting authenticated routes; inline form validation active

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | COMP-009 | Build AuthProvider React context | FE | API-004 | token-state-management; silent-refresh-before-expiry; 401-intercept->retry; redirect-unauth-to-login; expose-user+auth-methods-to-children | L | P0 |
| 2 | COMP-006 | Build LoginPage component | FE | COMP-009,API-001 | email+password-form; onSuccess-callback; redirectUrl-prop; generic-error-display; no-user-enumeration-in-UI | M | P0 |
| 3 | COMP-007 | Build RegisterPage component | FE | COMP-009,API-002 | email+password+displayName-form; inline-validation; termsUrl-prop; GDPR-consent-checkbox-per-NFR-COMP-001 | M | P0 |
| 4 | COMP-008 | Build ProfilePage component | FE | COMP-009,API-003 | displays:displayName+email+createdAt; auth-required; loading-state; error-state; data-matches-registration | M | P0 |
| 5 | COMP-016 | Build PasswordResetPage component | FE | API-005,API-006 | request-form(email); confirm-form(token+newPassword); token-from-URL-param; success-redirect-to-login; PRD-reset-flow | M | P1 |
| 6 | COMP-017 | Build LogoutButton component | FE | COMP-009,API-007 | click->clear-tokens+revoke-refresh+redirect-to-landing; session-ends-immediately; PRD-logout-story | S | P1 |
| 7 | COMP-018 | Configure frontend route guards | FE | COMP-009 | public:/login,/register,/reset; protected:/profile; unauth-on-protected->redirect-/login; auth-on-public->redirect-/dashboard | M | P0 |
| 8 | COMP-019 | Build inline form validation module | FE | -- | password-strength-meter(min8+upper+number); email-format-check; displayName-length(2-100); real-time-feedback | M | P1 |
| 9 | COMP-020 | Wire AuthProvider silent token refresh | FE | COMP-009,API-004 | refresh-triggered-before-accessToken-expiry; retry-queued-401-requests; no-redirect-loop; concurrent-request-dedup | M | P0 |
| 10 | COMP-021 | Build session expiry notification | FE | COMP-009 | 7day-inactivity->prompt-relogin; preserve-local-state-where-possible; clear-explanation-message | S | P2 |

### Integration Points -- Phase 4

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| AuthProvider context value | Dependency injection (React context) | Phase 4 | COMP-009 | LoginPage, RegisterPage, ProfilePage, LogoutButton, route guards |
| AuthProvider 401 interceptor | Callback wiring | Phase 4 | COMP-009 | All authenticated API calls (Axios/fetch interceptor) |
| Route guard configuration | Registry (route table) | Phase 4 | COMP-018 | React Router (public vs protected routes) |
| Form validation rules | Strategy pattern | Phase 4 | COMP-019 | RegisterPage, PasswordResetPage (confirm form) |

## Phase 5: Testing & Quality Assurance

**Objective:** Execute the full test pyramid (unit, integration, E2E), perform load testing and security review, and validate compliance controls. | **Duration:** 1.5 weeks | **Entry:** Phase 3 and Phase 4 complete; all endpoints and UI components functional | **Exit:** 80% unit coverage; integration tests passing with real PostgreSQL/Redis via testcontainers; E2E register-login-profile journey green; k6 500-concurrent passes p95<200ms; no critical security findings; GDPR/SOC2 controls validated

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | TEST-001 | Test login valid credentials returns AuthToken | Test | FR-AUTH-001 | unit; mock-PasswordHasher.verify->true; mock-TokenManager.issue; assert-AuthToken-shape-matches-DM-002 | S | P0 |
| 2 | TEST-002 | Test login invalid credentials returns 401 | Test | FR-AUTH-001 | unit; mock-PasswordHasher.verify->false; assert-401+AUTH_INVALID_CREDENTIALS; assert-no-email-enumeration | S | P0 |
| 3 | TEST-003 | Test token refresh with valid refresh token | Test | FR-AUTH-003 | unit; mock-Redis-valid-record; assert-new-AuthToken-pair; assert-old-refreshToken-revoked | S | P0 |
| 4 | TEST-004 | Test registration persists UserProfile to DB | Test | FR-AUTH-002 | integration; real-PostgreSQL-via-testcontainer; assert-row-inserted; bcrypt-hash-verified; no-plaintext-pwd | M | P0 |
| 5 | TEST-005 | Test expired refresh token rejected | Test | FR-AUTH-003 | integration; real-Redis-via-testcontainer; token-past-7day-TTL; assert-401-rejection | M | P0 |
| 6 | TEST-006 | Test register->login->profile E2E journey | Test | COMP-006,COMP-007,COMP-008 | e2e; Playwright; register-new-user->login-same-creds->profile-page-shows-correct-data | L | P0 |
| 7 | TEST-007 | Test password reset E2E flow | Test | COMP-016,API-005,API-006 | e2e; request-reset->verify-email-sent->confirm-with-token->login-new-pwd; old-sessions-invalid | L | P1 |
| 8 | TEST-008 | Run k6 load test 500 concurrent logins | Test | API-001 | load-test; 500-concurrent; p95<200ms; 0-5xx-errors; connection-pool-stable; report-generated | M | P0 |
| 9 | TEST-009 | Execute security penetration testing | Test | API-001,API-002,API-003,API-004,API-005,API-006,API-007 | XSS-scan-clean; CSRF-check-pass; JWT-manipulation-rejected; brute-force-blocked; no-critical-findings | L | P1 |
| 10 | TEST-010 | Validate GDPR/SOC2 compliance controls | Test | NFR-COMP-001,NFR-COMP-002 | consent-captured-at-registration; audit-log-12-month-retention; no-plaintext-pwd-in-any-log-sink; data-minimization-confirmed | M | P1 |

### Integration Points -- Phase 5

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| testcontainers PostgreSQL instance | Dependency injection (test) | Phase 5 | TEST-004 | Integration tests (replaces mock DB) |
| testcontainers Redis instance | Dependency injection (test) | Phase 5 | TEST-005 | Integration tests (replaces mock Redis) |
| Playwright browser context | E2E test harness | Phase 5 | TEST-006,TEST-007 | Full user journey tests |
| k6 load test script | Test artifact | Phase 5 | TEST-008 | CI pipeline, capacity validation |

## Phase 6: Migration & Staged Rollout

**Objective:** Execute three-phase rollout (alpha -> 10% beta -> GA) with feature flags, rollback procedures, and progressive traffic shifting. | **Duration:** 4 weeks (1 week alpha + 2 weeks beta + 1 week GA) | **Entry:** Phase 5 exit criteria met; all tests green; security review signed off | **Exit:** 100% traffic on new AuthService; AUTH_NEW_LOGIN flag removed; legacy auth deprecated; 99.9% uptime over first 7 days of GA; all rollback procedures documented and tested

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | MIG-004 | Configure AUTH_NEW_LOGIN feature flag | Gate | -- | flag-in-config-system; default:OFF; toggle-without-deploy; %-traffic-targeting-capable | S | P0 |
| 2 | MIG-005 | Configure AUTH_TOKEN_REFRESH feature flag | Gate | -- | flag-in-config-system; default:OFF; gates-refresh-flow-in-TokenManager; removal-target:GA+2wk | S | P0 |
| 3 | MIG-001 | Deploy internal alpha to staging | Ops | TEST-006,MIG-004 | all-FRs-pass-manual-test; 0-P0/P1-bugs; auth-team+QA-sign-off; AUTH_NEW_LOGIN-ON-for-internal | L | P0 |
| 4 | MIG-002 | Execute 10% beta traffic rollout | Ops | MIG-001 | p95<200ms; error-rate<0.1%; Redis-stable; TokenManager-healthy; 2-week-observation-period | XL | P0 |
| 5 | MIG-003 | Execute 100% GA rollout | Ops | MIG-002 | remove-AUTH_NEW_LOGIN-flag; 99.9%-uptime-7days; all-dashboards-green; legacy-deprecated | L | P0 |
| 6 | MIG-006 | Document rollback step 1: disable flag | Ops | MIG-004 | runbook-written; AUTH_NEW_LOGIN-OFF->legacy-route; execution-time<1min; tested-in-staging | S | P0 |
| 7 | MIG-007 | Document rollback step 2: verify legacy | Ops | MIG-006 | smoke-test-suite-for-legacy-auth; automated-execution; pass/fail-in<5min | S | P0 |
| 8 | MIG-008 | Document rollback step 3: root cause | Ops | MIG-007 | structured-log-query-templates; trace-correlation-guide; root-cause-analysis-template | S | P1 |
| 9 | MIG-009 | Document rollback step 4: data restore | Ops | MIG-008 | backup-restore-runbook; idempotent-upsert-for-UserProfile; tested-restore-procedure; RTO<30min | M | P0 |
| 10 | MIG-010 | Document rollback step 5: notify teams | Ops | MIG-009 | incident-channel-configured; template-message; auth-team+platform-team-notified; status-page-updated | S | P1 |
| 11 | MIG-011 | Document rollback step 6: post-mortem | Ops | MIG-010 | blameless-template-created; 48hr-deadline-documented; action-items-tracking-in-Jira | S | P1 |

### Integration Points -- Phase 6

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| AUTH_NEW_LOGIN flag -> API router | Dispatch/gate | Phase 6 | MIG-004 | API Gateway (routes %-traffic to new vs legacy) |
| AUTH_TOKEN_REFRESH flag -> TokenManager | Dispatch/gate | Phase 6 | MIG-005 | TokenManager.refresh() (enabled/disabled) |
| Rollback trigger thresholds | Event binding | Phase 6 | MIG-006 | Alerting system (p95>1000ms/5min, error>5%/2min, Redis-fail>10/min) |
| Legacy auth parallel operation | Dual-write/read | Phase 6 | MIG-001,MIG-002 | API Gateway (A/B routing during beta) |

## Phase 7: Operations & Observability

**Objective:** Establish production-grade observability, alerting, runbooks, capacity planning, and on-call procedures. | **Duration:** 2 weeks (overlaps with Phase 6 beta/GA) | **Entry:** MIG-001 deployed to staging; monitoring infrastructure available | **Exit:** All runbooks written and reviewed; Prometheus metrics exporting; Grafana dashboards live; all 3 alerts configured and tested; on-call rotation scheduled; OpenTelemetry tracing active across AuthService call chain

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | OPS-001 | Write runbook: AuthService down | Ops | MIG-001 | symptoms+diagnosis+resolution+escalation-documented; covers-pod-health+pg-failover+redis-fallback; reviewed-by-oncall | M | P0 |
| 2 | OPS-002 | Write runbook: token refresh failures | Ops | MIG-001 | symptoms:redirect-loop+error-counter-spike; diagnosis:Redis+JwtService+flag-check; escalation-path-defined | M | P0 |
| 3 | OPS-003 | Define on-call expectations and rotation | Ops | MIG-003 | 15min-ack-P1; 24/7-rotation-first-2wks-post-GA; tooling-list(k8s,grafana,redis-cli,psql); escalation:oncall->lead->manager->platform | S | P0 |
| 4 | OPS-004 | Configure AuthService pod autoscaling | Infra | MIG-001 | base:3-replicas; HPA-CPU>70%->scale-to-10; tested-under-500-concurrent-load; scale-down-cooldown | M | P0 |
| 5 | OPS-005 | Configure PostgreSQL connection scaling | Infra | INFRA-001 | pool:100-default; scale-to-200-if-conn-wait>50ms; monitoring-alert-on-pool-exhaustion | S | P1 |
| 6 | OPS-006 | Configure Redis memory scaling | Infra | INFRA-002 | base:1GB; scale-to-2GB-if->70%-utilized; ~100K-refresh-tokens-capacity(~50MB); eviction-policy-set | S | P1 |
| 7 | OPS-007 | Configure login failure rate alert | Ops | OPS-010 | threshold:>20%-over-5min; source:auth_login_total-Prometheus; action->OPS-001-runbook; PagerDuty-wired | S | P0 |
| 8 | OPS-008 | Configure p95 latency alert | Ops | OPS-010 | threshold:>500ms; source:auth_login_duration_seconds-histogram; action->check-pods+DB-perf; escalation-defined | S | P0 |
| 9 | OPS-009 | Configure Redis connection failure alert | Ops | OPS-010 | any-sustained-failures; source:TokenManager-structured-logs; action->OPS-002-runbook; immediate-page | S | P0 |
| 10 | OPS-010 | Deploy Prometheus metrics exporters | Ops | MIG-001 | auth_login_total:counter; auth_login_duration_seconds:histogram; auth_token_refresh_total:counter; auth_registration_total:counter | M | P0 |
| 11 | OPS-011 | Build Grafana monitoring dashboards | Ops | OPS-010 | login-rate-panel; latency-p95-panel; refresh-rate-panel; error-rate-panel; 4-panel-dashboard-live | M | P1 |
| 12 | OPS-012 | Configure OpenTelemetry tracing | Ops | COMP-001 | spans:AuthService->PasswordHasher->TokenManager->JwtService; trace-correlation-id; sampling-rate-configured | M | P1 |

### Integration Points -- Phase 7

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| Prometheus scrape targets | Registry | Phase 7 | OPS-010 | Prometheus server (scrapes /metrics endpoint) |
| Grafana data source (Prometheus) | Dependency injection | Phase 7 | OPS-011 | Grafana dashboards |
| PagerDuty alert routing | Callback wiring | Phase 7 | OPS-007,OPS-008,OPS-009 | On-call rotation |
| OpenTelemetry span context propagation | Middleware chain | Phase 7 | OPS-012 | AuthService -> all downstream components |

## Risk Assessment and Mitigation

| # | Risk | Severity | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|---|---|
| 1 | R-001: Token theft via XSS enables session hijacking | High | Medium | Unauthorized access to user accounts; data breach | Store accessToken in memory only (never localStorage). HttpOnly cookies for refreshToken. 15-minute access token expiry limits blast radius. Implement CSP headers. Wire immediate revocation in TokenManager if theft detected. | auth-team |
| 2 | R-002: Brute-force attacks on login endpoint | Medium | High | Account compromise; service degradation under attack volume | Rate limiting 10 req/min per IP via COMP-011. Account lockout after 5 failed attempts via COMP-012. bcrypt cost 12 makes offline cracking expensive (~250ms/attempt). WAF IP blocking. CAPTCHA escalation for repeat offenders. | auth-team |
| 3 | R-003: Data loss during migration from legacy auth | High | Low | Users locked out; data integrity failure; rollback required | Parallel legacy operation during Phase 6 MIG-001/002. Idempotent upsert for UserProfile migration. Full PostgreSQL backup before each rollout phase. Tested restore procedure (MIG-009) with RTO<30min. | platform-team |
| 4 | R-004: Low registration adoption due to poor UX | High | Medium | Conversion rate below 60% target; feature adoption blocked | Usability testing before launch (Phase 5). Inline form validation (COMP-019). Registration completes in <2s. Iterate based on funnel analytics. A/B test registration flow if initial conversion below target. | product-team |
| 5 | R-005: Compliance failure from incomplete audit logging | High | Medium | SOC2 audit failure in Q3 2026; regulatory exposure | Define log schema early (DM-003 in Phase 2). Validate against SOC2 controls in Phase 5 (TEST-010). Enforce 12-month retention per PRD. Review all log sinks for plaintext password leakage. | compliance |
| 6 | R-006: Email delivery failures blocking password reset | Medium | Low | Users unable to reset passwords; increased support ticket volume | Delivery monitoring via SendGrid dashboard (COMP-014). Alert on delivery failure rate >5%. Fallback support channel for manual password recovery. Monitor email bounce and spam rates. | auth-team |

## Resource Requirements and Dependencies

### External Dependencies

| Dependency | Required By Phase | Status | Fallback |
|---|---|---|---|
| PostgreSQL 15+ (DEP-001) | Phase 1 | Provisioning needed | No fallback -- critical path; service non-functional without it |
| Redis 7+ (DEP-002) | Phase 1 | Provisioning needed | Degrade to access-token-only auth (no refresh); users re-login on every expiry |
| Node.js 20 LTS (DEP-003) | Phase 1 | Available | None -- runtime requirement |
| bcryptjs library (DEP-004) | Phase 2 | npm registry | argon2 as alternative hashing library (requires PasswordHasher interface change) |
| jsonwebtoken library (DEP-005) | Phase 2 | npm registry | jose library as alternative JWT implementation |
| SendGrid API (DEP-006) | Phase 3 | Account needed | Defer FR-AUTH-005 password reset; manual reset via support channel |
| Frontend routing framework (DEP-007) | Phase 4 | Assumed available | Auth pages cannot render without client-side routing |
| SEC-POLICY-001 document (DEP-008) | Phase 1 | Draft needed | Define interim password/token policies inline; formalize later |

### Infrastructure Requirements

- PostgreSQL 15+ cluster: 100 connection pool, automated backups, read replica for failover (INFRA-001)
- Redis 7+ cluster: 1GB initial memory, AUTH enabled, TTL support for 7-day refresh tokens (INFRA-002)
- Kubernetes cluster: 3-10 AuthService pods with HPA on CPU>70% (OPS-004)
- TLS 1.3 certificates: valid, auto-renewed, no protocol downgrade (INFRA-005)
- RSA 2048-bit key pair: mounted as Kubernetes secret, quarterly rotation (INFRA-004)
- Docker Compose: local dev environment with PostgreSQL + Redis for developer testing (INFRA-009)
- testcontainers: ephemeral PostgreSQL + Redis for CI integration tests (TEST-004, TEST-005)
- Prometheus + Grafana: metrics collection and dashboarding (OPS-010, OPS-011)
- OpenTelemetry: distributed tracing across AuthService call chain (OPS-012)
- SendGrid account: transactional email for password reset with delivery monitoring (COMP-014)
- Feature flag system: supports %-based traffic targeting and instant toggle (MIG-004, MIG-005)
- k6: load testing tool for 500-concurrent validation (TEST-008)
- Playwright: E2E browser automation for user journey tests (TEST-006, TEST-007)

### Team Resources

- **auth-team:** Primary development and on-call ownership. Responsible for Phases 1-5 implementation and Phase 7 runbooks.
- **platform-team:** Infrastructure provisioning (Phase 1), Kubernetes/HPA configuration (Phase 7), escalation point for data and infrastructure issues.
- **frontend-team:** Phase 4 implementation of LoginPage, RegisterPage, ProfilePage, AuthProvider, and route guards.
- **QA:** E2E test development (TEST-006, TEST-007), manual testing during MIG-001 alpha, load testing (TEST-008).
- **compliance:** Review of NFR-COMP-001 through NFR-COMP-004, audit log validation (TEST-010), SOC2 control sign-off.
- **security:** Penetration testing (TEST-009), review of PasswordHasher and JwtService implementations, CSP header review.

## Success Criteria and Validation Approach

| Criterion | Metric | Target | Validation Method | Phase |
|---|---|---|---|---|
| SC-001: Login response time | p95 latency on AuthService.login() | < 200ms | APM instrumentation + k6 load test (TEST-008) | Phase 5 |
| SC-002: Registration success rate | Successful registrations / total attempts | > 99% | Application metrics (auth_registration_total counter) | Phase 6 (beta) |
| SC-003: Token refresh latency | p95 latency on TokenManager.refresh() | < 100ms | APM instrumentation on refresh endpoint | Phase 5 |
| SC-004: Service availability | Uptime over 30-day rolling window | 99.9% | Health check monitoring via OPS-001 + uptime service | Phase 7 (post-GA) |
| SC-005: Password hash time | Benchmark PasswordHasher.hash() with bcrypt cost 12 | < 500ms | Unit benchmark in CI (Phase 2 NFR-SEC-001 validation) | Phase 2 |
| SC-006: Registration conversion | Funnel: RegisterPage -> confirmed account | > 60% | Frontend analytics on RegisterPage + backend registration events | Phase 6 (beta) |
| SC-007: Daily active authenticated users | Unique AuthToken issuances per day | > 1000 within 30 days of GA | auth_login_total counter + unique user dedup | Phase 7 (post-GA) |
| SC-008: Average session duration | Time between first token and last refresh | > 30 minutes | Token refresh event analytics (auth_token_refresh_total) | Phase 7 (post-GA) |
| SC-009: Failed login rate | Failed logins / total login attempts | < 5% | Auth event log analysis (OPS-007 alert threshold is 20%) | Phase 6 (GA) |
| SC-010: Password reset completion | Funnel: reset requested -> new password set | > 80% | Auth event log: reset-request -> reset-confirm events | Phase 6 (GA) |

## Timeline Estimates

| Phase | Duration | Start | End | Key Milestones |
|---|---|---|---|---|
| Phase 1: Infrastructure Foundation | 1 week | Week 1 | Week 1 | PostgreSQL+Redis healthy; TLS+CORS active; project scaffold ready |
| Phase 2: Data Layer & Security Modules | 1.5 weeks | Week 2 | Week 3 | Schemas deployed; UserRepo+PasswordHasher+JwtService operational; security validations passing |
| Phase 3: Backend Service & API Layer | 2 weeks | Week 3 | Week 5 | All 8 API endpoints live; FR-AUTH-001-005 passing; GDPR+SOC2 logging active |
| Phase 4: Frontend Implementation | 1.5 weeks | Week 4 | Week 5 | All UI components rendering; AuthProvider token lifecycle working; route guards active |
| Phase 5: Testing & Quality Assurance | 1.5 weeks | Week 5 | Week 6 | 80% unit coverage; integration+E2E green; k6 500-concurrent passes; security review clean |
| Phase 6: Migration & Staged Rollout | 4 weeks | Week 6 | Week 9 | Alpha (W6-7) -> Beta 10% (W7-8) -> GA 100% (W9); feature flags configured+removed |
| Phase 7: Operations & Observability | 2 weeks | Week 7 | Week 9 | Runbooks+alerts+dashboards+tracing live; on-call rotation active |

**Total estimated duration:** 9 weeks (Phases 4-5 overlap with Phase 3; Phase 7 overlaps with Phase 6 beta/GA)

**Key milestone dates (assuming Q2 2026 start):**

1. **Week 1:** Infrastructure provisioned and validated
2. **Week 3:** Data layer complete, security modules validated
3. **Week 5:** All backend APIs and frontend components functional
4. **Week 6:** Testing complete, security review signed off, alpha deployment
5. **Week 8:** Beta at 10% traffic, 2-week observation window cleared
6. **Week 9:** GA at 100%, legacy deprecated, operations fully staffed

## Open Questions

| # | Question | Impact | Blocking Phase | Resolution Owner |
|---|---|---|---|---|
| 1 | OQ-001: Should AuthService support API key authentication for service-to-service calls? | May require additional API endpoint and key management infrastructure | Phase 3 (if yes) | test-lead (OVERDUE: 2026-04-15) |
| 2 | OQ-002: Maximum allowed UserProfile roles array length? | Affects DM-001 schema constraint and validation logic | Phase 2 | auth-team (OVERDUE: 2026-04-01) |
| 3 | OQ-003: Audit log retention: TDD 90 days vs PRD 12 months? | Affects DM-003 storage planning and compliance validation (TEST-010) | Phase 2 | auth-team / compliance |
| 4 | OQ-004: Logout endpoint -- client-side token clear or server-side refresh revocation? | Affects API-007 implementation scope; this roadmap assumes server-side revocation | Phase 3 | auth-team |
| 5 | OQ-005: Admin audit log access -- deferred or missing from TDD? | Affects API-008 implementation; this roadmap includes it as PRD gap fill | Phase 3 | test-lead |
| 6 | OQ-006: Password reset email -- synchronous or asynchronous? | Sync blocks API response; async requires queue infrastructure but better UX | Phase 3 | Engineering |
| 7 | OQ-007: Max refresh tokens per user across devices? | Affects TokenManager Redis storage strategy and COMP-002 logic | Phase 3 | Product |
| 8 | OQ-008: "Remember me" extending session beyond 7 days? | Affects COMP-002 refresh token TTL configuration | Phase 3 | Product |
| 9 | OQ-009: GDPR consent mechanism design at registration? | Affects NFR-COMP-001 implementation; no design in TDD | Phase 3 | auth-team |
| 10 | OQ-010: UserProfile roles[]+timestamps -- GDPR data minimization compliant? | Affects NFR-COMP-004 assessment; may require schema change | Phase 2 | compliance |
| 11 | OQ-011 (PRD gap): Logout capability requires API-007 -- TDD should be updated | PRD lists logout as in-scope but TDD has no endpoint | Phase 3 | auth-team |
| 12 | OQ-012 (PRD gap): Jordan admin log viewing requires API-008 -- TDD should be updated | PRD Epic AUTH-E3 user story for admin has no corresponding FR/API | Phase 3 | test-lead |
