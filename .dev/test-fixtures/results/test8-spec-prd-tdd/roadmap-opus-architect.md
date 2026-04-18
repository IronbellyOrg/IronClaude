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
total_task_rows: 104
risk_count: 10
open_questions: 10
---

# User Authentication Service — Project Roadmap

## Executive Summary

This roadmap delivers a centralized User Authentication Service replacing ad-hoc credential handling across the platform. The service implements JWT-based stateless sessions (RS256), bcrypt password hashing (cost 12), refresh token rotation with replay detection, and a phased rollout behind feature flags. Five functional requirements (login, registration, token refresh, profile retrieval, password reset) are supported by 12 components spanning backend services, database migrations, frontend pages, and infrastructure. The architecture follows a layered dependency chain: PasswordHasher and JwtService (zero-dependency utilities) → TokenManager → AuthService → auth-middleware → routes, with frontend components (LoginPage, RegisterPage, AuthProvider, ProfilePage) consuming the API surface.

**Business Impact:** Authentication unblocks ~$2.4M ARR from personalization-dependent features planned for Q2-Q3 2026. SOC2 Type II audit readiness (Q3 2026 deadline) requires user-level audit trails that depend on authenticated sessions. 25% of churned users cite absence of user accounts as a reason for leaving.

**Complexity:** MEDIUM (0.6) — Security surface (JWT RS256, bcrypt, token rotation, replay detection, rate limiting) elevates complexity, but bounded scope (5 endpoints, no RBAC/OAuth/MFA) and well-defined layered architecture keep it manageable.

**Critical path:** PasswordHasher + JwtService → TokenManager → AuthService → auth-middleware → route registration → database migration → integration testing → phased rollout. Frontend components (LoginPage, RegisterPage, AuthProvider) run parallel to backend integration but gate E2E validation.

**Key architectural decisions:**

- JWT with RS256 asymmetric signing over opaque tokens or PASETO — enables stateless verification across horizontally scaled service instances
- bcrypt (cost 12) via PasswordHasher abstraction over Argon2id/scrypt — battle-tested, well-audited; abstraction enables future algorithm migration without API changes
- Dual-token strategy (access in memory, refresh in httpOnly cookie with rotation) over server-side sessions — prevents XSS token theft while maintaining horizontal scalability

**Open risks requiring resolution before Phase 1:**

- RSA key pair (2048-bit) must be provisioned in secrets manager before JwtService implementation begins
- PostgreSQL 15+ and Redis 7+ instances must be provisioned and accessible
- SEC-POLICY-001 policy document must be finalized to lock password/token configuration parameters

## Phase 1: Foundation

**Objective:** Provision infrastructure, implement zero-dependency utility modules, create database schema, and establish data model contracts | **Duration:** 1.5 weeks | **Entry:** PostgreSQL 15+, Redis 7+, Node.js 20 LTS provisioned; RSA key pair in secrets manager; SEC-POLICY-001 finalized | **Exit:** PasswordHasher and JwtService pass unit tests; database migrations run cleanly; all data model interfaces compile with type checks

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | COMP-004 | Implement PasswordHasher module | Auth | — | hash(pwd)→bcrypt-string; verify(pwd,hash)→bool; cost-factor:12; hash-time<500ms | M | P0 |
| 2 | NFR-AUTH.3 | Verify bcrypt cost factor 12 config | Auth | COMP-004 | unit-test asserts cost=12; benchmark confirms ~250-300ms/hash | S | P0 |
| 3 | NFR-COMP-003 | Enforce NIST SP 800-63B password storage | Sec | COMP-004 | raw-pwd never persisted; raw-pwd never logged; one-way adaptive hash verified | S | P0 |
| 4 | COMP-003 | Implement JwtService RS256 sign/verify | Auth | — | sign(payload,key)→JWT; verify(jwt,pubkey)→claims; expired→reject; invalid-sig→reject | M | P0 |
| 5 | NFR-SEC-002 | Validate RS256 2048-bit key config | Sec | COMP-003 | config-test asserts RS256 algorithm; key-length≥2048-bit; no HS256 fallback | S | P0 |
| 6 | DM-001 | Define UserRecord database entity | DB | — | id:UUID-PK; email:unique-idx-lowercase; display_name:varchar; password_hash:varchar(bcrypt); is_locked:bool-default-false; created_at:timestamptz; updated_at:timestamptz | M | P0 |
| 7 | DM-002 | Define RefreshTokenRecord entity | DB | DM-001 | id:UUID-PK; user_id:FK→UserRecord.id-cascade; token_hash:varchar(SHA-256); expires_at:timestamptz; revoked:bool-default-false; created_at:timestamptz | M | P0 |
| 8 | DM-003 | Define AuthTokenPair response DTO | Auth | — | access_token:string(JWT,15min-TTL); refresh_token:string(opaque,7d-TTL) | S | P0 |
| 9 | DM-004 | Define UserProfile API response DTO | Auth | — | id:UUID; email:string; displayName:string(2-100ch); createdAt:ISO8601; updatedAt:ISO8601; lastLoginAt:ISO8601-nullable; roles:string[] | S | P0 |
| 10 | DM-005 | Define AuthToken API response DTO | Auth | — | accessToken:string(JWT); refreshToken:string(opaque); expiresIn:number(900); tokenType:string("Bearer") | S | P0 |
| 11 | DM-006 | Define ErrorResponse standard format | Auth | — | error.code:string; error.message:string; error.status:number; consistent across all endpoints | S | P1 |
| 12 | COMP-007 | Create 003-auth-tables migration | DB | DM-001, DM-002 | users-table created with all DM-001 fields; refresh_tokens-table created with all DM-002 fields; down-migration drops both; idempotent | M | P0 |
| 13 | MIG-001 | Provision PostgreSQL 15+ with pooling | Infra | — | pg-pool configured; connection-pool-size:100; connection-wait<50ms; health-check-query passes | M | P0 |
| 14 | MIG-002 | Provision Redis 7+ for token storage | Infra | — | redis-instance running; 1GB memory; TTL-support verified; connectivity from AuthService pods | M | P0 |
| 15 | MIG-003 | Provision RSA key pair in secrets mgr | Infra | — | 2048-bit RSA keypair generated; private-key in secrets-manager; public-key accessible to JwtService; rotation-policy:90d documented | S | P0 |
| 16 | NFR-AUTH.2 | Configure health check endpoint | Infra | MIG-001, MIG-002 | /health returns 200 when PostgreSQL+Redis reachable; returns 503 when either down; uptime monitoring wired | S | P1 |
| 17 | NFR-COMP-004 | Enforce GDPR data minimization schema | DB | DM-001 | schema-review confirms only email,password_hash,display_name collected; no additional PII columns | S | P1 |
| 18 | TEST-UNIT-001 | PasswordHasher unit test suite | Test | COMP-004 | hash-produces-bcrypt-string; verify-matches-correct-pwd; verify-rejects-wrong-pwd; cost-factor-12-asserted; timing-benchmark<500ms | M | P0 |
| 19 | TEST-UNIT-002 | JwtService unit test suite | Test | COMP-003 | sign-produces-valid-JWT; verify-decodes-claims; expired-token-rejected; tampered-token-rejected; RS256-algorithm-verified | M | P0 |

### Integration Points — Phase 1

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| PasswordHasher.hash() | Function export | Phase 1 | Phase 2 | AuthService.register(), AuthService.resetConfirm() |
| PasswordHasher.verify() | Function export | Phase 1 | Phase 2 | AuthService.login() |
| JwtService.sign() | Function export | Phase 1 | Phase 2 | TokenManager.issueTokens() |
| JwtService.verify() | Function export | Phase 1 | Phase 2 | TokenManager.validateAccess(), auth-middleware |
| 003-auth-tables migration | Database schema | Phase 1 | Phase 2 | UserRepo, RefreshTokenRepo |
| pg-pool connection | Dependency injection | Phase 1 | Phase 2 | AuthService, TokenManager |
| Redis client | Dependency injection | Phase 1 | Phase 2 | TokenManager |

## Phase 2: Core Logic

**Objective:** Implement TokenManager, AuthService orchestrator, and all five functional requirement flows (login, registration, token refresh, profile retrieval, password reset) | **Duration:** 2 weeks | **Entry:** Phase 1 exit criteria met; PasswordHasher and JwtService unit tests green | **Exit:** All FR-AUTH.1 through FR-AUTH.5 implemented with passing unit tests; TokenManager refresh rotation and replay detection verified

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 20 | COMP-002 | Implement TokenManager token lifecycle | Auth | COMP-003, MIG-002 | issueTokens(userId)->AuthTokenPair; refresh(token)->new-pair+revoke-old; revokeAll(userId)->all-tokens-invalidated | L | P0 |
| 21 | FR-AUTH.3 | Implement refresh token rotation | Auth | COMP-002 | valid-refresh->new-pair; old-refresh-revoked; rotated-token-stored-in-Redis; SHA-256-hash-before-storage | M | P0 |
| 22 | FR-AUTH.3a | Validate refresh returns new token pair | Auth | FR-AUTH.3 | POST /auth/refresh+valid-token->200+new-accessToken+new-refreshToken | S | P0 |
| 23 | FR-AUTH.3b | Reject expired refresh token | Auth | FR-AUTH.3 | expired-refreshToken->401; requires-re-authentication | S | P0 |
| 24 | FR-AUTH.3c | Detect refresh token replay attack | Auth | FR-AUTH.3 | previously-rotated-token->revoke-ALL-user-tokens; return-401 | M | P0 |
| 25 | FR-AUTH.3d | Store refresh token hashes in DB | Auth | FR-AUTH.3, DM-002 | token-hash:SHA-256; stored-in-Redis-with-7d-TTL; revocation-flag-supported | S | P0 |
| 26 | FR-AUTH.3e | Reject revoked refresh token | Auth | FR-AUTH.3 | revoked-token->401; no-new-pair-issued | S | P0 |
| 27 | FR-AUTH.3f | Session persists across page refresh | Auth | FR-AUTH.3 | active-session-extends-within-7d-window; no-re-login-on-page-reload | S | P1 |
| 28 | COMP-001 | Implement AuthService orchestrator | Auth | COMP-002, COMP-004, DM-001 | login(); register(); refresh(); getProfile(); resetRequest(); resetConfirm(); all-methods-delegate-to-specialized-components | L | P0 |
| 29 | FR-AUTH.1 | Implement login flow in AuthService | Auth | COMP-001 | email+pwd->validate-via-PasswordHasher->issue-tokens-via-TokenManager->return-AuthTokenPair | M | P0 |
| 30 | FR-AUTH.1a | Return 200 with tokens on valid login | Auth | FR-AUTH.1 | valid-creds->200+access_token(15min)+refresh_token(7d) | S | P0 |
| 31 | FR-AUTH.1b | Return 401 on invalid credentials | Auth | FR-AUTH.1 | wrong-pwd->401; wrong-email->401; no-enumeration(same-msg) | S | P0 |
| 32 | FR-AUTH.1c | Return 403 on locked account | Auth | FR-AUTH.1 | is_locked=true->403+suspension-msg | S | P0 |
| 33 | FR-AUTH.1d | Rate-limit login 5/min per IP | Auth | FR-AUTH.1, COMP-012 | 6th-attempt-within-1min->429; counter-resets-after-window | M | P0 |
| 34 | FR-AUTH.1e | Lock account after 5 failed attempts | Auth | FR-AUTH.1 | 5-failures-in-15min->is_locked=true; 423-response; admin-notified | M | P0 |
| 35 | FR-AUTH.1f | No user enumeration on login | Auth | FR-AUTH.1 | nonexistent-email->401+same-error-as-wrong-pwd | S | P0 |
| 36 | FR-AUTH.2 | Implement registration in AuthService | Auth | COMP-001, COMP-004 | validate-input->hash-pwd-via-PasswordHasher->persist-UserRecord->return-UserProfile | M | P0 |
| 37 | FR-AUTH.2a | Return 201 with profile on register | Auth | FR-AUTH.2 | valid-data->201+UserProfile(id,email,displayName,createdAt) | S | P0 |
| 38 | FR-AUTH.2b | Return 409 on duplicate email | Auth | FR-AUTH.2 | existing-email->409-Conflict; DB-unique-constraint-enforced | S | P0 |
| 39 | FR-AUTH.2c | Enforce password policy | Auth | FR-AUTH.2 | min-8ch; >=1-uppercase; >=1-lowercase; >=1-digit; weak-pwd->400 | S | P0 |
| 40 | FR-AUTH.2d | Validate email format | Auth | FR-AUTH.2 | invalid-email-format->400; validated-before-DB-insert | S | P1 |
| 41 | FR-AUTH.2e | Hash with bcrypt cost factor 12 | Auth | FR-AUTH.2, COMP-004 | stored-hash-is-bcrypt; cost-factor-extractable=12 | S | P0 |
| 42 | FR-AUTH.2f | Auto-login after registration | Auth | FR-AUTH.2, FR-AUTH.1 | successful-register->issue-AuthTokenPair->user-logged-in | S | P1 |
| 43 | FR-AUTH.4 | Implement profile retrieval | Auth | COMP-001, COMP-002 | valid-accessToken->fetch-UserProfile-from-DB->return-sanitized-profile | M | P0 |
| 44 | FR-AUTH.4a | Return profile on valid Bearer token | Auth | FR-AUTH.4 | GET /auth/me+valid-token->200+UserProfile | S | P0 |
| 45 | FR-AUTH.4b | Return 401 on expired/invalid token | Auth | FR-AUTH.4 | expired-token->401; invalid-token->401 | S | P0 |
| 46 | FR-AUTH.4c | Exclude sensitive fields from response | Auth | FR-AUTH.4 | no-password_hash; no-refresh_token_hash; no-is_locked in response | S | P0 |
| 47 | FR-AUTH.4d | Include full profile fields in response | Auth | FR-AUTH.4 | id+email+displayName+createdAt+updatedAt+lastLoginAt+roles all present | S | P1 |
| 48 | FR-AUTH.5 | Implement password reset flow | Auth | COMP-001, COMP-004, COMP-002 | two-step: request(email)->send-token; confirm(token,newPwd)->update-hash | L | P0 |
| 49 | FR-AUTH.5a | Generate reset token and send email | Auth | FR-AUTH.5 | registered-email->reset-token(1h-TTL)+email-dispatched-via-SendGrid | M | P0 |
| 50 | FR-AUTH.5b | Reset password with valid token | Auth | FR-AUTH.5 | valid-reset-token+new-pwd->update-password_hash; invalidate-reset-token | M | P0 |
| 51 | FR-AUTH.5c | Reject expired/invalid reset token | Auth | FR-AUTH.5 | expired-token->400; invalid-token->400; descriptive-error-msg | S | P0 |
| 52 | FR-AUTH.5d | Invalidate all sessions on reset | Auth | FR-AUTH.5, COMP-002 | successful-reset->TokenManager.revokeAll(userId); all-refresh-tokens-cleared | S | P0 |
| 53 | FR-AUTH.5e | Prevent reset token reuse | Auth | FR-AUTH.5 | used-token->400; single-use-enforced | S | P0 |
| 54 | FR-AUTH.5f | No enumeration on reset request | Auth | FR-AUTH.5 | unregistered-email->same-200-response; no-email-sent | S | P0 |
| 55 | NFR-COMP-001 | Implement GDPR consent at registration | Auth | FR-AUTH.2 | consent-checkbox-required; consent-timestamp-recorded-in-DB; registration-blocked-without-consent | M | P1 |
| 56 | TEST-UNIT-003 | TokenManager unit test suite | Test | COMP-002 | issue-tokens-returns-AuthTokenPair; refresh-rotates-token; replay-detection-revokes-all; revoked-token-rejected | M | P0 |
| 57 | TEST-UNIT-004 | AuthService.login unit tests | Test | FR-AUTH.1 | valid-creds->tokens; invalid-creds->401; locked-account->403; enumeration-prevention | M | P0 |
| 58 | TEST-UNIT-005 | AuthService.register unit tests | Test | FR-AUTH.2 | valid-data->UserProfile; duplicate-email->409; weak-pwd->400; bcrypt-hash-stored | M | P0 |

### Integration Points -- Phase 2

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| AuthService.login() | Method | Phase 2 | Phase 3 | POST /auth/login route handler |
| AuthService.register() | Method | Phase 2 | Phase 3 | POST /auth/register route handler |
| AuthService.getProfile() | Method | Phase 2 | Phase 3 | GET /auth/me route handler |
| AuthService.refresh() | Method | Phase 2 | Phase 3 | POST /auth/refresh route handler |
| AuthService.resetRequest() | Method | Phase 2 | Phase 3 | POST /auth/reset-request route handler |
| AuthService.resetConfirm() | Method | Phase 2 | Phase 3 | POST /auth/reset-confirm route handler |
| TokenManager -> Redis | Client injection | Phase 2 | Phase 2 | TokenManager stores/retrieves refresh token hashes |
| AuthService -> PasswordHasher | DI registration | Phase 2 | Phase 2 | AuthService.login(), AuthService.register(), AuthService.resetConfirm() |

## Phase 3: Integration

**Objective:** Wire API endpoints, auth middleware, route registration, frontend components, and API Gateway rate limiting; validate end-to-end flows through HTTP layer | **Duration:** 2 weeks | **Entry:** Phase 2 exit criteria met; all AuthService methods pass unit tests | **Exit:** All API endpoints return correct responses; auth-middleware intercepts and validates tokens; frontend components render and submit forms; integration tests pass against real PostgreSQL and Redis

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 59 | COMP-005 | Implement auth-middleware token guard | API | COMP-002 | extract-Bearer-from-Authorization-header; verify-via-TokenManager; 401-if-missing/invalid/expired; attach-decoded-claims-to-request | M | P0 |
| 60 | COMP-006 | Register /auth/* route group | API | COMP-001, COMP-005 | /auth/login; /auth/register; /auth/me; /auth/refresh; /auth/reset-request; /auth/reset-confirm; all-wired-to-AuthService-methods | M | P0 |
| 61 | API-001 | Wire POST /auth/login endpoint | API | COMP-006, FR-AUTH.1 | req-body:{email,password}; delegates-to-AuthService.login(); returns-AuthToken-or-error; content-type:application/json | M | P0 |
| 62 | API-002 | Wire POST /auth/register endpoint | API | COMP-006, FR-AUTH.2 | req-body:{email,password,displayName}; delegates-to-AuthService.register(); returns-UserProfile-or-error | M | P0 |
| 63 | API-003 | Wire GET /auth/me endpoint | API | COMP-006, FR-AUTH.4, COMP-005 | requires-auth-middleware; delegates-to-AuthService.getProfile(); returns-UserProfile | M | P0 |
| 64 | API-004 | Wire POST /auth/refresh endpoint | API | COMP-006, FR-AUTH.3 | req-body:{refreshToken}; delegates-to-AuthService.refresh(); returns-new-AuthToken-pair | M | P0 |
| 65 | API-005 | Wire POST /auth/reset-request endpoint | API | COMP-006, FR-AUTH.5 | req-body:{email}; delegates-to-AuthService.resetRequest(); returns-200-always(no-enum) | M | P0 |
| 66 | API-006 | Wire POST /auth/reset-confirm endpoint | API | COMP-006, FR-AUTH.5 | req-body:{token,newPassword}; delegates-to-AuthService.resetConfirm(); returns-200-or-400 | M | P0 |
| 67 | COMP-012 | Configure API Gateway rate limiting | Infra | API-001, API-002 | login:10req/min/IP; register:5req/min/IP; me:60req/min/user; refresh:30req/min/user; CORS-restricted-to-known-origins | M | P0 |
| 68 | NFR-AUTH.1 | Validate p95 < 200ms under load | Test | API-001, API-002, API-003, API-004 | k6-load-test; all-auth-endpoints-p95<200ms; normal-load-conditions | M | P0 |
| 69 | NFR-PERF-002 | Validate 500 concurrent login support | Test | API-001 | k6-concurrent-test; 500-simultaneous-login-reqs; no-5xx; p95<200ms | M | P0 |
| 70 | COMP-008 | Implement LoginPage component | FE | API-001, COMP-010 | email+password-fields; submit-calls-POST-/auth/login; success->store-AuthToken-via-AuthProvider; failure->generic-error-msg; no-user-enumeration | M | P0 |
| 71 | COMP-009 | Implement RegisterPage component | FE | API-002, COMP-010 | email+password+displayName-fields; client-side-pwd-validation; submit-calls-POST-/auth/register; success->redirect-to-dashboard; 409->suggest-login | M | P0 |
| 72 | COMP-010 | Implement AuthProvider context wrapper | FE | API-004 | wraps-App; manages-AuthToken-state; silent-refresh-on-expiring-accessToken; exposes-UserProfile+auth-methods; clears-tokens-on-tab-close; intercepts-401->trigger-refresh | L | P0 |
| 73 | COMP-011 | Implement ProfilePage component | FE | API-003, COMP-010 | renders-UserProfile-data(displayName,email,createdAt); requires-authenticated-route; loads-via-GET-/auth/me | M | P1 |
| 74 | NFR-COMP-002 | Implement SOC2 audit event logging | Auth | COMP-001 | all-auth-events-logged(login,register,refresh,reset); fields:userId,timestamp,IP,outcome; 12-month-retention; queryable-by-date+user | L | P1 |
| 75 | TEST-INT-001 | Login flow integration test | Test | API-001 | full-HTTP-flow; valid-creds->200+JWT; invalid->401; rate-limit->429 | M | P0 |
| 76 | TEST-INT-002 | Token refresh integration test | Test | API-004 | HTTP-refresh-endpoint; new-pair-issued; old-token-revoked; replay-detection-triggers-revocation | M | P0 |
| 77 | TEST-INT-003 | Registration then login integration | Test | API-001, API-002 | register-user->login-with-same-creds->success; data-persisted-between-operations | M | P0 |
| 78 | TEST-INT-004 | Expired refresh token rejection test | Test | API-004, MIG-002 | Redis-TTL-expiration; expired-refresh->401; integration-with-real-Redis | M | P0 |

### Integration Points — Phase 3

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| auth-middleware -> TokenManager.verify() | Middleware chain | Phase 3 | Phase 3 | GET /auth/me, all protected routes |
| COMP-006 route registry -> AuthService methods | Route dispatch table | Phase 3 | Phase 3 | Express router |
| AuthProvider -> POST /auth/refresh | Silent refresh callback | Phase 3 | Phase 3 | All authenticated frontend pages |
| AuthProvider -> LoginPage redirect | 401 intercept handler | Phase 3 | Phase 3 | ProtectedRoutes wrapper |
| API Gateway rate-limit rules -> /auth/* | Middleware config | Phase 3 | Phase 4 | All auth endpoints |

## Phase 4: Hardening

**Objective:** Security review, penetration testing, performance benchmarking, E2E test coverage, compliance validation, and edge case hardening | **Duration:** 1.5 weeks | **Entry:** Phase 3 exit criteria met; all integration tests pass; frontend components functional | **Exit:** Security review passed; penetration test completed with no P0/P1 findings; E2E tests cover full user lifecycle; all NFRs validated; unit test coverage >80% for core modules

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 79 | NFR-REL-001 | Validate 99.9% availability target | Ops | NFR-AUTH.2 | uptime-monitoring-wired; /health-endpoint-checked-every-30s; PagerDuty-alerting-configured; 30-day-measurement-window-defined | M | P0 |
| 80 | SEC-REVIEW-001 | Conduct security review of auth flow | Sec | COMP-001, COMP-002, COMP-003, COMP-004 | bcrypt-cost-12-verified; RS256-key-rotation-documented(90d); no-plaintext-pwd-in-logs; no-sensitive-fields-in-API-responses; TLS-1.3-enforced | L | P0 |
| 81 | SEC-REVIEW-002 | Penetration testing on auth endpoints | Sec | API-001 through API-006 | brute-force-mitigated; token-theft-mitigated; XSS-vectors-blocked; CSRF-mitigated-by-httpOnly-cookie; no-P0/P1-findings | L | P0 |
| 82 | TEST-E2E-001 | E2E: full user lifecycle test | Test | COMP-008, COMP-009, COMP-010, COMP-011 | register->login->view-profile->refresh-token->reset-password->login-with-new-pwd; all-steps-pass; Playwright-automated | L | P0 |
| 83 | TEST-E2E-002 | E2E: LoginPage login flow | Test | COMP-008 | enter-email+pwd->submit->redirect-to-dashboard; invalid-creds->error-msg; Playwright-automated | M | P0 |
| 84 | TEST-E2E-003 | E2E: RegisterPage registration flow | Test | COMP-009 | enter-email+pwd+name->submit->account-created->redirect; duplicate-email->error-msg; Playwright-automated | M | P0 |
| 85 | TEST-E2E-004 | E2E: AuthProvider token refresh | Test | COMP-010 | accessToken-expires->silent-refresh-triggered->no-user-interruption; expired-refresh->redirect-to-LoginPage | M | P1 |
| 86 | EDGE-001 | Handle concurrent registration race | Auth | FR-AUTH.2, DM-001 | two-simultaneous-register-same-email->one-succeeds+one-gets-409; DB-unique-constraint-prevents-duplicates | S | P1 |
| 87 | EDGE-002 | Handle JWT clock skew tolerance | Auth | COMP-003 | JwtService-allows-5s-clock-skew; tokens-near-expiry-still-valid-within-tolerance | S | P1 |
| 88 | EDGE-003 | Handle Redis unavailability gracefully | Auth | COMP-002 | Redis-down->reject-refresh-requests(401); do-not-serve-stale-tokens; log-connection-failure | M | P1 |
| 89 | NFR-OPS-001 | Configure monitoring dashboards | Ops | COMP-001 | Grafana-dashboards: auth_login_total, auth_login_duration_seconds, auth_token_refresh_total, auth_registration_total; OpenTelemetry-spans-for-AuthService+PasswordHasher+TokenManager+JwtService | M | P0 |
| 90 | OPS-ALERT-001 | Configure alerting thresholds | Ops | NFR-OPS-001 | login-failure-rate>20%/5min->alert; p95-latency>500ms->alert; TokenManager-Redis-failures>10/min->alert | M | P0 |
| 91 | COVERAGE-001 | Verify >80% unit test coverage | Test | TEST-UNIT-001 through TEST-UNIT-005 | Jest-coverage-report; AuthService>=80%; TokenManager>=80%; JwtService>=80%; PasswordHasher>=80% | M | P0 |

### Integration Points -- Phase 4

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| Prometheus metrics -> Grafana | Metrics pipeline | Phase 4 | Phase 5 | On-call dashboards |
| OpenTelemetry spans -> tracing backend | Distributed tracing | Phase 4 | Phase 5 | Incident diagnosis |
| PagerDuty alert rules -> auth-team | Alert routing | Phase 4 | Phase 5 | 24/7 on-call rotation |

## Phase 5: Production Readiness

**Objective:** Phased rollout behind feature flags, operational runbooks, capacity planning validation, data migration, and GA release | **Duration:** 4 weeks (1w internal alpha + 2w beta + 1w GA) | **Entry:** Phase 4 exit criteria met; security review passed; all E2E tests green; monitoring dashboards operational | **Exit:** 99.9% uptime over 7 days in production; feature flags removed; runbooks published; on-call rotation active; all rollback criteria documented and tested

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 92 | FLAG-001 | Configure AUTH_NEW_LOGIN feature flag | Ops | COMP-006 | flag-default:OFF; enables-new-LoginPage+AuthService-login; toggleable-without-deploy | S | P0 |
| 93 | FLAG-002 | Configure AUTH_TOKEN_REFRESH flag | Ops | COMP-002 | flag-default:OFF; enables-refresh-token-flow-in-TokenManager; when-OFF-only-access-tokens-issued | S | P0 |
| 94 | ROLLOUT-001 | Internal alpha deployment to staging | Ops | FLAG-001, FLAG-002 | AuthService-deployed-to-staging; auth-team+QA-test-all-endpoints; LoginPage+RegisterPage-behind-flag; zero-P0/P1-bugs | L | P0 |
| 95 | ROLLOUT-002 | Beta rollout to 10% traffic | Ops | ROLLOUT-001 | AUTH_NEW_LOGIN-enabled-for-10%; monitor-latency+error-rate+Redis-usage; p95<200ms; error-rate<0.1%; no-Redis-connection-failures | XL | P0 |
| 96 | ROLLOUT-003 | GA rollout to 100% traffic | Ops | ROLLOUT-002 | remove-AUTH_NEW_LOGIN-flag; all-users-through-new-AuthService; legacy-auth-deprecated; AUTH_TOKEN_REFRESH-enabled | L | P0 |
| 97 | OPS-RUNBOOK-001 | Publish AuthService down runbook | Ops | NFR-OPS-001 | symptoms; diagnosis-steps; resolution(restart-pods,failover-DB,check-Redis); escalation-path(auth-team->test-lead->eng-manager->platform-team) | M | P0 |
| 98 | OPS-RUNBOOK-002 | Publish token refresh failure runbook | Ops | NFR-OPS-001 | symptoms(unexpected-logout,AuthProvider-redirect-loop); diagnosis(Redis-connectivity,JwtService-key,feature-flag); resolution(scale-Redis,remount-secrets,enable-flag) | M | P0 |
| 99 | OPS-CAPACITY-001 | Validate capacity planning targets | Ops | ROLLOUT-002 | AuthService-HPA:3->10-pods-on-CPU>70%; pg-pool:100-conns(scalable-to-200); Redis:1GB(scalable-to-2GB-at-70%); 500-concurrent-users-sustained | M | P0 |
| 100 | ROLLBACK-001 | Test rollback procedure in staging | Ops | ROLLOUT-001 | disable-AUTH_NEW_LOGIN->legacy-auth-operational; smoke-tests-pass; recovery-time<5min | M | P0 |
| 101 | ROLLBACK-002 | Document rollback criteria | Ops | ROLLBACK-001 | p95>1000ms-for-5min; error-rate>5%-for-2min; Redis-failures>10/min; data-loss-detected->trigger-rollback | S | P0 |
| 102 | MIG-DATA-001 | Validate UserProfile migration script | DB | DM-001, ROLLOUT-001 | idempotent-upsert; tested-with-production-like-dataset; full-backup-before-each-phase; no-data-loss | M | P0 |
| 103 | OPS-ONCALL-001 | Establish 24/7 on-call rotation | Ops | OPS-RUNBOOK-001, OPS-RUNBOOK-002 | P1-ack-within-15min; auth-team-covers-first-2-weeks-post-GA; tooling-access(K8s,Grafana,Redis-CLI,pgAdmin) | S | P0 |
| 104 | SIGNOFF-001 | Obtain go/no-go sign-off | Gate | ROLLOUT-002, SEC-REVIEW-001 | test-lead+eng-manager-approve; all-release-checklist-items-complete; monitoring-dashboards-green | S | P0 |

### Integration Points -- Phase 5

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| AUTH_NEW_LOGIN feature flag -> route dispatch | Feature gate | Phase 5 | Phase 5 | Express router conditionally routes to new vs legacy auth |
| AUTH_TOKEN_REFRESH flag -> TokenManager | Feature gate | Phase 5 | Phase 5 | TokenManager conditionally issues refresh tokens |
| Rollback flag toggle -> legacy auth | Failover switch | Phase 5 | Phase 5 | Emergency rollback procedure |
| UserProfile migration script -> PostgreSQL | Data migration | Phase 5 | Phase 5 | Legacy user records migrated to new schema |

## Risk Assessment and Mitigation

| # | Risk | Severity | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|---|---|
| 1 | JWT private key compromise allows forged tokens | Critical | Low | High | RS256 asymmetric keys; private key in secrets manager; 90-day key rotation; key access audit logging | Security |
| 2 | Refresh token replay after token theft | High | Medium | High | Refresh rotation with replay detection; reuse triggers revocation of ALL user tokens; HttpOnly cookie storage | Auth-team |
| 3 | bcrypt cost factor insufficient for future hardware | Medium | Low | Medium | Configurable cost factor in PasswordHasher; annual review vs OWASP recs; Argon2id migration path via abstraction layer | Security |
| 4 | XSS-based session hijacking via token theft | High | Medium | High | Access token in memory only (never localStorage); HttpOnly cookies for refresh token; 15-min access token TTL; immediate revocation via TokenManager | Auth-team |
| 5 | Brute-force login attacks | Medium | High | Medium | API Gateway rate-limit (10 req/min/IP); account lockout after 5 failed in 15min; bcrypt cost 12 slows offline cracking; WAF IP blocking as escalation | Infra |
| 6 | Data loss during legacy auth migration | High | Low | High | Parallel operation during Phase 1-2; idempotent upsert migration; full DB backup before each rollout phase; tested rollback procedure | Auth-team |
| 7 | Low registration adoption due to poor UX | High | Medium | High | Usability testing before launch; funnel analytics from RegisterPage; iterate based on conversion rate data (target >60%) | Product |
| 8 | Security breach from implementation flaws | Critical | Low | Critical | Dedicated security review; penetration test before production; no P0/P1 findings allowed before GA | Security |
| 9 | Incomplete audit logging fails SOC2 audit | High | Medium | High | Define log schema early (userId, timestamp, IP, outcome); validate against SOC2 controls in QA; 12-month retention verified | Compliance |
| 10 | Email delivery failure blocks password reset | Medium | Low | Medium | SendGrid delivery monitoring and alerting; confirmation shown regardless of email existence; fallback support channel for manual resets | Infra |

## Resource Requirements and Dependencies

### External Dependencies

| Dependency | Required By Phase | Status | Fallback |
|---|---|---|---|
| PostgreSQL 15+ | Phase 1 | Pending provisioning | No fallback; blocking dependency |
| Redis 7+ | Phase 1 | Pending provisioning | No fallback; refresh tokens require Redis |
| Node.js 20 LTS | Phase 1 | Available | None; runtime requirement |
| bcryptjs (npm) | Phase 1 | Available on npm | bcrypt native module as alternative |
| jsonwebtoken (npm) | Phase 1 | Available on npm | jose library as alternative |
| RSA key pair (2048-bit) | Phase 1 | Pending generation | Cannot start JwtService without keys |
| SendGrid API | Phase 2 | Pending account setup | Password reset flow blocked without email delivery |
| pg-pool (npm) | Phase 1 | Available on npm | Direct pg connections (degraded performance) |
| SEC-POLICY-001 policy | Phase 1 | Pending finalization | Use OWASP defaults; update when policy finalizes |
| Frontend routing framework | Phase 3 | Available | Auth pages cannot render without routing |
| Kubernetes cluster | Phase 5 | Available | Manual deployment (slower, no HPA) |
| Prometheus / OpenTelemetry | Phase 4 | Available | No observability; blind to issues |

### Infrastructure Requirements

- PostgreSQL 15+: 100 connection pool, managed instance with failover replica
- Redis 7+: 1 GB memory, TTL support, managed cluster with monitoring
- Kubernetes: 3 initial AuthService pods, HPA scaling to 10 on CPU > 70%
- Secrets manager: RSA private key storage with rotation support (90-day policy)
- API Gateway: Rate limiting rules (10/min login, 5/min register, 60/min profile, 30/min refresh)
- Monitoring stack: Grafana dashboards, Prometheus metric collection, OpenTelemetry tracing
- CI pipeline: testcontainers for ephemeral PostgreSQL+Redis in integration tests
- TLS 1.3: Required on all auth endpoints; certificate provisioning

## Success Criteria and Validation Approach

| Criterion | Metric | Target | Validation Method | Phase |
|---|---|---|---|---|
| Login performance | p95 response time | < 200ms | k6 load test; APM on AuthService.login() | 3, 4 |
| Registration reliability | Success rate | > 99% | Ratio of successful registrations to attempts | 3, 4 |
| Token refresh performance | p95 latency | < 100ms | APM on TokenManager.refresh() | 3, 4 |
| Service availability | Uptime | 99.9% (30-day window) | Health check monitoring | 5 |
| Password hash timing | Hash duration | < 500ms | Benchmark of PasswordHasher.hash() with cost 12 | 1 |
| Registration conversion | Funnel rate | > 60% | Analytics: landing -> register -> confirmed | 5 |
| Active users | DAU (authenticated) | > 1000 within 30d of GA | AuthToken issuance counts | 5 |
| Session duration | Average length | > 30 minutes | Token refresh event analytics | 5 |
| Failed login rate | Failure percentage | < 5% of attempts | Auth event log analysis | 5 |
| Password reset completion | Funnel rate | > 80% | Reset requested -> new password set | 5 |
| Unit test coverage | Code coverage | > 80% for core modules | Jest coverage reports | 4 |

## Timeline Estimates

| Phase | Duration | Start | End | Key Milestones |
|---|---|---|---|---|
| 1: Foundation | 1.5 weeks | Week 1 | Week 2 (mid) | PasswordHasher + JwtService unit-tested; DB migration applied; infra provisioned |
| 2: Core Logic | 2 weeks | Week 2 (mid) | Week 4 (mid) | AuthService + TokenManager complete; FR-AUTH.1-5 implemented; core unit tests green |
| 3: Integration | 2 weeks | Week 4 (mid) | Week 6 (mid) | API endpoints wired; auth-middleware active; frontend components functional; integration tests pass |
| 4: Hardening | 1.5 weeks | Week 6 (mid) | Week 8 | Security review passed; E2E tests green; monitoring configured; >80% coverage |
| 5: Production Readiness | 4 weeks | Week 8 | Week 12 | Alpha (1w) -> Beta 10% (2w) -> GA 100% (1w); runbooks published; on-call active |

**Total estimated duration:** 11 weeks (Weeks 1-12, with Phase 5 overlapping by 1 week with stabilization buffer)

## Open Questions

| # | Question | Impact | Blocking Phase | Resolution Owner |
|---|---|---|---|---|
| 1 | Should password reset emails be sent synchronously or via message queue? | Affects reset endpoint latency and system resilience | Phase 2 (FR-AUTH.5) | Engineering |
| 2 | Maximum number of active refresh tokens per user? | Affects Redis storage requirements and multi-device UX | Phase 2 (FR-AUTH.3) | Product |
| 3 | Should AuthService support API key auth for service-to-service calls? | Deferred to v1.1; affects integration scope | Non-blocking (v1.1) | test-lead |
| 4 | Maximum allowed UserProfile roles array length? | Affects schema validation and future RBAC design | Non-blocking (v1.1) | auth-team |
| 5 | Account lockout: exact threshold and progressive lockout duration? | FR-AUTH.1 rate-limiting partially addresses; full policy undefined | Phase 2 (FR-AUTH.1e) | Security |
| 6 | Should "remember me" extend session beyond 7-day refresh window? | Affects token TTL strategy and UX | Phase 2 (FR-AUTH.3) | Product |
| 7 | Audit logging schema, retention policy, and query interface? | NFR-COMP-002 requires SOC2-compliant logging; implementation details undefined | Phase 3 (NFR-COMP-002) | Backend |
| 8 | Token revocation cascade on user deletion? | Affects data integrity and security posture | Phase 2 (FR-AUTH.3) | Architect |
| 9 | Is FR-AUTH.3 sufficient for Sam (API consumer) or is API-key auth needed? | Gap between persona need and spec coverage | Non-blocking (v1.1) | Product/Engineering |
| 10 | Is logout in scope for v1.0? PRD includes it but no corresponding FR-AUTH.x | Missing functional requirement if in scope | Phase 2 | Product |
