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
generated: "2026-04-15"
generator: "single"
total_phases: 7
total_task_rows: 52
risk_count: 7
open_questions: 8
---

# User Authentication Service — Project Roadmap

## Executive Summary

This roadmap defines a seven-phase implementation plan for a stateless JWT-based authentication service covering registration, login, token lifecycle, profile retrieval, and self-service password reset. The system comprises 9 backend/frontend components orchestrated by `AuthService`, backed by PostgreSQL (user persistence, audit logs) and Redis (refresh token revocation), with a React frontend delivering login, registration, profile, and password-reset pages through an `AuthProvider` context.

The architecture enforces RS256-signed JWTs with 15-minute access tokens and 7-day refresh tokens, bcrypt cost-12 password hashing, and a three-phase feature-flagged rollout (alpha → 10% beta → GA). Four compliance obligations (GDPR consent, GDPR data minimization, SOC2 12-month audit logging, NIST SP 800-63B password storage) are addressed in a dedicated compliance phase before testing begins.

**Business Impact:** Authentication unblocks ~$2.4M projected annual revenue from personalization-dependent features. Delay past Q2 2026 risks SOC2 audit failure in Q3 and a full-quarter slip to the personalization roadmap. Three personas drive design: Alex (end user — fast registration, seamless sessions), Jordan (admin — audit visibility, account management), Sam (API consumer — programmatic token management).

**Complexity:** MEDIUM (0.65) — Well-scoped single-service domain with clear component boundaries. Elevated by security criticality (token theft, brute-force), compliance obligations (GDPR, SOC2, NIST), and multi-store data topology (PostgreSQL + Redis + SendGrid).

**Critical path:** DM-001 → COMP-005 → COMP-001 → FR-AUTH-001 → API-001 → COMP-006 → TEST-004 → MIG-001 → MIG-003. Infrastructure provisioning and `UserRepo` implementation gate all downstream work.

**Key architectural decisions:**

- Stateless REST with JWT — no server-side session store; all session state in RS256-signed tokens with Redis-backed refresh token revocation
- Layered component hierarchy — `AuthService` orchestrates `PasswordHasher`, `TokenManager`, `UserRepo`; `TokenManager` delegates to `JwtService` and Redis
- Feature-flagged rollout — `AUTH_NEW_LOGIN` and `AUTH_TOKEN_REFRESH` flags enable incremental traffic migration with instant rollback

**Open risks requiring resolution before Phase 1:**

- R-001 (Token theft via XSS): accessToken storage strategy must be finalized — memory-only vs. HttpOnly cookie tradeoffs affect `AuthProvider` implementation
- OQ-004 (Max refresh tokens per user): Unbounded tokens per user could exhaust Redis memory; must define limit before `TokenManager` implementation

## Phase 1: Infrastructure & Data Foundation

**Objective:** Provision all data stores, define schemas, configure cryptographic primitives, and establish the API gateway — the foundation every subsequent phase depends on | **Duration:** 1.5 weeks | **Entry:** PostgreSQL 15+, Redis 7+, Node.js 20 LTS provisioned; RS256 key generation tooling available | **Exit:** All three database schemas migrated and verified; bcrypt and RS256 configs pass validation tests; API gateway routes `/v1/auth/*` with TLS 1.3 and CORS; SendGrid integration returns 200 on test email

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | DM-001 | Create UserProfile PostgreSQL schema | DB | — | id:UUID-PK; email:unique-idx-lower; display_name:varchar(2-100); password_hash:varchar-not-null; created_at:timestamptz-default-now; updated_at:timestamptz-auto; last_login_at:timestamptz-nullable; roles:text[]-default-user | M | P0 |
| 2 | DM-002 | Define AuthToken JWT+Redis structure | DB | DM-001 | access_token:JWT-RS256-signed; refresh_token:opaque-unique; expires_in:int-900; token_type:Bearer; refresh stored hashed in Redis; 7d TTL | M | P0 |
| 3 | DM-003 | Create AuditLog PostgreSQL schema | DB | DM-001 | user_id:varchar-not-null; event_type:varchar-not-null; timestamp:timestamptz-not-null; ip_address:varchar-not-null; outcome:varchar-not-null; 12-month retention policy; partitioned by month | M | P0 |
| 4 | NFR-SEC-001 | Configure bcrypt cost factor 12 | Sec | — | bcrypt-cost:12; hash-time<500ms; unit test asserts cost param; no plaintext passwords persisted or logged | S | P0 |
| 5 | NFR-SEC-002 | Generate RS256 2048-bit key pair | Sec | — | RS256-2048bit; key pair generated; private key in secrets store; public key accessible to JwtService; quarterly rotation documented | M | P0 |
| 6 | COMP-010 | Provision API Gateway with TLS/CORS | Infra | — | TLS-1.3-enforced; CORS restricted to known origins; `/v1/auth/*` prefix routed; rate-limit headers present; health-check endpoint returns 200 | L | P0 |
| 7 | COMP-011 | Implement EmailService SendGrid wrapper | Infra | — | SendGrid API integration; send-email method; delivery status callback; test email returns 200; error handling for delivery failures; R-007 mitigation | M | P1 |

### Integration Points — Phase 1

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| UserProfile schema (DM-001) | DDL migration | Phase 1 | Phase 1 | COMP-005 (UserRepo), DM-003 (AuditLog FK) |
| AuditLog schema (DM-003) | DDL migration | Phase 1 | Phase 1 | NFR-COMP-002 (SOC2 logging) |
| RS256 key pair (NFR-SEC-002) | Secret mount | Phase 1 | Phase 2 | COMP-003 (JwtService) |
| bcrypt config (NFR-SEC-001) | Environment config | Phase 1 | Phase 2 | COMP-004 (PasswordHasher) |
| API Gateway (COMP-010) | Reverse proxy | Phase 1 | Phase 3 | API-001 through API-006 |
| EmailService (COMP-011) | Service module | Phase 1 | Phase 2 | FR-AUTH-005 (password reset) |

## Phase 2: Core Backend Components

**Objective:** Implement all backend service modules and wire the AuthService orchestrator to its dependencies — producing a fully functional auth backend ready for API exposure | **Duration:** 2 weeks | **Entry:** Phase 1 schemas migrated; bcrypt and RS256 configs validated | **Exit:** All five backend components pass unit tests; AuthService handles login, registration, token refresh, profile retrieval, and password reset flows end-to-end in integration tests

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | COMP-004 | Implement PasswordHasher module | Auth | NFR-SEC-001 | hash() returns bcrypt-cost-12 digest; verify() validates against stored hash; hash-time<500ms; no plaintext logged; future-algorithm-migration hook | M | P0 |
| 2 | COMP-003 | Implement JwtService sign/verify | Auth | NFR-SEC-002 | sign() produces RS256 JWT with user-id+roles payload; verify() validates signature+expiry; 5s clock-skew tolerance; rejects tampered tokens | M | P0 |
| 3 | COMP-005 | Implement UserRepo data access layer | DB | DM-001 | findByEmail(); createUser(); updateLastLogin(); connection-pool via pg-pool size:100 scalable-to-200; conn-wait<50ms | L | P0 |
| 4 | COMP-002 | Implement TokenManager lifecycle | Auth | COMP-003 | issueTokens() returns AuthToken pair; refresh() rotates tokens; revoke() invalidates in Redis; stores refresh-hash in Redis with 7d TTL; old token revoked on refresh | L | P0 |
| 5 | COMP-001 | Implement AuthService orchestrator | Auth | COMP-002, COMP-004, COMP-005 | delegates login to PasswordHasher+TokenManager; delegates register to PasswordHasher+UserRepo; delegates refresh to TokenManager; delegates reset to EmailService+PasswordHasher; emits audit events | XL | P0 |
| 6 | FR-AUTH-001 | Implement login flow in AuthService | Auth | COMP-001 | valid-creds→200+AuthToken; invalid→401; non-existent-email→401; 5fail/15min→423; no-enum | L | P0 |
| 7 | FR-AUTH-002 | Implement registration with validation | Auth | COMP-001 | valid-reg→201+UserProfile; dup-email→409; weak-pwd(<8,no-upper,no-num)→400; bcrypt-cost-12 hash stored | L | P0 |
| 8 | FR-AUTH-003 | Implement JWT issuance and refresh | Auth | COMP-002 | login→accessToken(15min)+refreshToken(7d); POST-refresh→new-pair; expired-refresh→401; revoked-refresh→401 | L | P0 |
| 9 | FR-AUTH-004 | Implement profile retrieval | Auth | COMP-001, COMP-005 | valid-token→UserProfile(id,email,displayName,createdAt,updatedAt,lastLoginAt,roles); expired/invalid-token→401 | M | P0 |
| 10 | FR-AUTH-005 | Implement password reset flow | Auth | COMP-001, COMP-011 | reset-request+valid-email→sends-token-email; reset-confirm+valid-token→updates-hash; token-1h-TTL; single-use; same-response-for-unknown-email | L | P0 |

### Integration Points — Phase 2

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| PasswordHasher.hash()/verify() | Method dispatch | Phase 2 | Phase 2 | COMP-001 (AuthService) login + registration |
| TokenManager.issueTokens()/refresh()/revoke() | Method dispatch | Phase 2 | Phase 2 | COMP-001 (AuthService) login + refresh |
| JwtService.sign()/verify() | Method dispatch | Phase 2 | Phase 2 | COMP-002 (TokenManager) |
| UserRepo.findByEmail()/createUser() | Data access dispatch | Phase 2 | Phase 2 | COMP-001 (AuthService) |
| Redis client | Connection pool | Phase 2 | Phase 2 | COMP-002 (TokenManager) refresh token store |
| EmailService.sendResetEmail() | Service call | Phase 2 | Phase 2 | COMP-001 (AuthService) password reset |
| AuthService audit event emitter | Event binding | Phase 2 | Phase 5 | NFR-COMP-002 (SOC2 logging) |

## Phase 3: API Layer & Security Hardening

**Objective:** Expose all six REST endpoints through the API gateway with rate limiting, input validation, and error standardization; verify performance targets under load | **Duration:** 1.5 weeks | **Entry:** All Phase 2 backend components passing unit tests; API gateway routing confirmed | **Exit:** All endpoints return correct status codes per AC; rate limiting enforced; p95 <200ms on login; 500 concurrent logins sustained; error response format standardized

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | API-001 | Implement POST /auth/login endpoint | API | FR-AUTH-001, COMP-010 | valid-creds→200+AuthToken; invalid→401; locked→423; rate:10req/min/IP→429; error format:{code,message,status} | L | P0 |
| 2 | API-002 | Implement POST /auth/register endpoint | API | FR-AUTH-002, COMP-010 | valid→201+UserProfile; dup-email→409; weak-pwd→400; invalid-email→400; rate:5req/min/IP; displayName:2-100chars | L | P0 |
| 3 | API-003 | Implement GET /auth/me endpoint | API | FR-AUTH-004, COMP-010 | Bearer-token→200+UserProfile(id,email,displayName,createdAt,updatedAt,lastLoginAt,roles); missing/expired/invalid-token→401; rate:60req/min/user | M | P0 |
| 4 | API-004 | Implement POST /auth/refresh endpoint | API | FR-AUTH-003, COMP-010 | valid-refresh→200+new-AuthToken; expired→401; revoked→401; old-token-invalidated; rate:30req/min/user | M | P0 |
| 5 | API-005 | Implement POST /auth/reset-request | API | FR-AUTH-005, COMP-010 | any-email→same-success-response; registered-email-triggers-SendGrid; no-enumeration; token-1h-TTL | M | P0 |
| 6 | API-006 | Implement POST /auth/reset-confirm | API | FR-AUTH-005, COMP-010 | valid-token+strong-pwd→password-updated; expired-token→error; used-token→error; weak-pwd→400 | M | P0 |
| 7 | NFR-PERF-001 | Validate API p95 response <200ms | API | API-001 | p95-login<200ms; p95-register<200ms; p95-refresh<100ms; APM tracing on AuthService methods; regression threshold set | L | P0 |
| 8 | NFR-PERF-002 | Load test 500 concurrent logins | API | API-001, NFR-PERF-001 | k6-load-test; 500-concurrent-login-requests; no-5xx; p95<200ms; connection-pool-stable; Redis-latency-stable | L | P1 |

### Integration Points — Phase 3

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| API Gateway rate-limit rules | Middleware chain | Phase 3 | Phase 3 | API-001 (10/min), API-002 (5/min), API-003 (60/min), API-004 (30/min) |
| Bearer token validation middleware | Middleware chain | Phase 3 | Phase 3 | API-003 (auth-required) |
| Error response formatter | Middleware chain | Phase 3 | Phase 3 | All API-xxx endpoints |
| URL prefix `/v1/auth/*` router | Reverse proxy | Phase 1 | Phase 3 | All API-xxx endpoints |
| APM tracing instrumentation | Callback wiring | Phase 3 | Phase 5 | NFR-PERF-001, OPS-004 |

## Phase 4: Frontend Components & UX

**Objective:** Build all frontend page components and the AuthProvider context, delivering the complete user-facing auth experience for Alex (registration <60s, seamless sessions) and the password reset self-service flow | **Duration:** 1.5 weeks | **Entry:** All API endpoints returning correct responses; Bearer token validation working | **Exit:** LoginPage, RegisterPage, ProfilePage, PasswordResetPage render correctly; AuthProvider handles silent refresh and 401 interception; inline validation on all forms; no user enumeration in error messages

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | COMP-009 | Implement AuthProvider context | FE | API-003, API-004 | wraps App root; manages AuthToken state; silent refresh via TokenManager; 401 interception+redirect; exposes UserProfile+auth methods to children; handles 7d refresh expiry gracefully | L | P0 |
| 2 | COMP-006 | Build LoginPage component | FE | COMP-009, API-001 | route:/login; email+password form; onSuccess callback; redirectUrl prop; submits to API-001; generic error on failure; no user enumeration; stores AuthToken via AuthProvider | L | P0 |
| 3 | COMP-007 | Build RegisterPage component | FE | COMP-009, API-002 | route:/register; email+password+displayName form; termsUrl prop; inline password-strength validation; submits to API-002; dup-email shows helpful message; registration<60s (Alex persona) | L | P0 |
| 4 | COMP-008 | Build ProfilePage component | FE | COMP-009, API-003 | route:/profile; auth-required; displays UserProfile(id,email,displayName,createdAt,updatedAt,lastLoginAt,roles); loads via GET /auth/me; renders<1s | M | P0 |
| 5 | COMP-012 | Build PasswordResetPage component | FE | API-005, API-006 | route:/reset-password; two-step: request form (email) + confirm form (token+new password); inline password validation; same UX for registered/unregistered emails; expired-link error with retry option | L | P1 |

### Integration Points — Phase 4

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| AuthProvider.login()/logout()/refresh() | Context dispatch | Phase 4 | Phase 4 | COMP-006 (LoginPage), COMP-007 (RegisterPage) |
| AuthProvider.user (UserProfile state) | Context subscription | Phase 4 | Phase 4 | COMP-008 (ProfilePage) |
| AuthProvider 401 interceptor | Callback wiring | Phase 4 | Phase 4 | All authenticated routes |
| AuthProvider silent refresh timer | Event binding | Phase 4 | Phase 4 | Token expiry cycle (every <15min) |
| Frontend routing framework (DEP-007) | Route registry | Phase 4 | Phase 4 | /login, /register, /profile, /reset-password |

## Phase 5: Compliance, Observability & Operations

**Objective:** Implement all compliance controls (GDPR consent, data minimization, SOC2 audit logging, NIST password storage), establish operational readiness (runbooks, on-call, capacity planning), and configure uptime monitoring | **Duration:** 1.5 weeks | **Entry:** All functional flows working end-to-end through frontend; API endpoints stable | **Exit:** GDPR consent captured at registration; audit logs persisting with 12-month retention; NIST compliance validated; all four runbooks reviewed by auth-team; monitoring dashboards live; HPA autoscaling configured

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | NFR-COMP-001 | Implement GDPR consent at registration | Sec | API-002 | consent checkbox on RegisterPage; consent recorded with timestamp in UserProfile; registration blocked without consent; consent audit trail queryable | M | P0 |
| 2 | NFR-COMP-002 | Implement SOC2 audit log persistence | Sec | DM-003, COMP-001 | all auth events logged: login_success, login_failure, registration, password_reset, token_refresh; fields: userId, eventType, timestamp, ipAddress, outcome; 12-month retention; partitioned storage | L | P0 |
| 3 | NFR-COMP-003 | Validate NIST SP 800-63B compliance | Sec | COMP-004, NFR-SEC-001 | one-way adaptive hashing (bcrypt-12); raw passwords never persisted or logged; password policy enforced at registration+reset; compliance documented | M | P0 |
| 4 | NFR-COMP-004 | Enforce GDPR data minimization | Sec | DM-001 | only email, password_hash, display_name collected; no additional PII fields in UserProfile; privacy audit confirms minimal data; documented | S | P1 |
| 5 | NFR-REL-001 | Configure 99.9% uptime monitoring | Ops | COMP-010, API-001 | health-check endpoint monitored; 30-day rolling window SLA calculation; alerting on downtime >4.3min/month; Grafana dashboard for uptime | L | P0 |
| 6 | OPS-001 | Create AuthService-down runbook | Ops | COMP-001, NFR-REL-001 | symptoms, diagnosis, resolution steps documented; PostgreSQL failover procedure; Redis fallback behavior; escalation path: auth-team->test-lead->eng-manager->platform-team; 15-min ack target | M | P1 |
| 7 | OPS-002 | Create token-refresh-failure runbook | Ops | COMP-002 | symptoms: unexpected logouts, AuthProvider redirect loop; diagnosis: Redis connectivity, JwtService key, feature flag; resolution steps; escalation documented | M | P1 |
| 8 | OPS-003 | Establish on-call rotation | Ops | OPS-001, OPS-002 | 24/7 rotation for first 2 weeks post-GA; P1 ack within 15min; tooling: K8s dashboards, Grafana, Redis CLI, PostgreSQL admin; knowledge prerequisites documented | M | P1 |
| 9 | OPS-004 | Configure capacity planning and HPA | Ops | NFR-PERF-002 | AuthService: 3 replicas, HPA to 10 at CPU>70%; PostgreSQL: pool 100, scale to 200 at wait>50ms; Redis: 1GB, scale to 2GB at mem>70%; Prometheus metrics: auth_login_total, auth_login_duration_seconds, auth_token_refresh_total, auth_registration_total; OpenTelemetry tracing; cost: $450/mo base | L | P1 |

### Integration Points — Phase 5

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| Audit event logger | Event binding | Phase 5 | Phase 5 | AuthService emits → AuditLog PostgreSQL table |
| GDPR consent field | Schema extension | Phase 5 | Phase 4 | COMP-007 (RegisterPage) consent checkbox |
| Prometheus metrics exporter | Callback wiring | Phase 5 | Phase 5 | OPS-004 capacity planning, Grafana |
| OpenTelemetry spans | Callback wiring | Phase 5 | Phase 5 | AuthService → PasswordHasher → TokenManager → JwtService |
| Health check endpoint | HTTP probe | Phase 5 | Phase 7 | MIG-002 monitoring, NFR-REL-001 uptime |

## Phase 6: Testing & Quality Assurance

**Objective:** Execute the full test pyramid — unit tests for isolated component logic, integration tests with real PostgreSQL/Redis via testcontainers, and E2E tests through the complete user journey — achieving 80% unit coverage target | **Duration:** 1.5 weeks | **Entry:** All functional flows, compliance controls, and observability instrumented | **Exit:** All TEST-xxx pass green; unit coverage ≥80%; integration tests confirm real DB persistence and token expiry; E2E Playwright test completes register→login→profile journey; zero P0/P1 bugs

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | TEST-001 | Unit test login valid credentials | Test | FR-AUTH-001, COMP-001 | AuthService.login() calls PasswordHasher.verify() + TokenManager.issueTokens(); returns valid AuthToken with accessToken+refreshToken; mocks: PasswordHasher, TokenManager, UserRepo | M | P0 |
| 2 | TEST-002 | Unit test login invalid credentials | Test | FR-AUTH-001, COMP-001 | 401 when PasswordHasher.verify() returns false; no AuthToken issued; mocks: PasswordHasher(false), UserRepo | M | P0 |
| 3 | TEST-003 | Unit test token refresh valid token | Test | FR-AUTH-003, COMP-002 | old token revoked; new AuthToken pair issued via JwtService; mocks: Redis client, JwtService | M | P0 |
| 4 | TEST-004 | Integration test registration persists | Test | FR-AUTH-002, COMP-005 | full flow: API request → PasswordHasher → PostgreSQL insert; UserProfile retrievable from real PostgreSQL; testcontainers; no mocks | L | P0 |
| 5 | TEST-005 | Integration test expired refresh rejected | Test | FR-AUTH-003, COMP-002 | expired Redis TTL → 401; real Redis via testcontainers; confirms TTL-based invalidation | L | P0 |
| 6 | TEST-006 | E2E register-login-profile flow | Test | COMP-006, COMP-007, COMP-008 | Playwright: RegisterPage → LoginPage → ProfilePage; user sees profile data; AuthProvider handles token lifecycle; full stack; no mocks | XL | P0 |

### Integration Points — Phase 6

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| testcontainers PostgreSQL | Test fixture | Phase 6 | Phase 6 | TEST-004 (registration persistence) |
| testcontainers Redis | Test fixture | Phase 6 | Phase 6 | TEST-005 (token expiry) |
| Jest mock factories | Dependency injection | Phase 6 | Phase 6 | TEST-001, TEST-002, TEST-003 |
| Playwright test harness | E2E framework | Phase 6 | Phase 6 | TEST-006 (full journey) |
| Docker Compose test env | Infrastructure | Phase 6 | Phase 6 | Local developer testing |

## Phase 7: Migration & General Availability

**Objective:** Execute the three-phase rollout (internal alpha, 10% beta, 100% GA) with feature flags, monitoring, and documented rollback procedures; remove feature flags post-GA | **Duration:** 4 weeks (1 alpha + 2 beta + 1 GA) | **Entry:** All TEST-xxx green; zero P0/P1 bugs; monitoring dashboards live; runbooks reviewed | **Exit:** AUTH_NEW_LOGIN flag removed; 100% traffic on new AuthService; 99.9% uptime over first 7 days; all rollback criteria monitored; post-mortem template ready

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | MIG-004 | Configure AUTH_NEW_LOGIN feature flag | Ops | TEST-006 | flag gates LoginPage+AuthService login endpoint; default OFF; toggleable per-environment; flag state logged for audit | S | P0 |
| 2 | MIG-005 | Configure AUTH_TOKEN_REFRESH flag | Ops | TEST-006 | flag gates refresh token flow in TokenManager; default OFF; when OFF only access tokens issued; flag state logged | S | P0 |
| 3 | MIG-001 | Deploy internal alpha to staging | Ops | MIG-004, MIG-005 | AuthService deployed to staging; auth-team+QA test all endpoints; LoginPage+RegisterPage behind AUTH_NEW_LOGIN; 1 week duration; all FRs pass manual testing; zero P0/P1 bugs; rollback: disable flag | L | P0 |
| 4 | MIG-002 | Execute beta rollout at 10% traffic | Ops | MIG-001 | AUTH_NEW_LOGIN enabled for 10% traffic; 2 weeks duration; monitor: p95<200ms, error-rate<0.1%, no Redis connection failures; AuthProvider handles refresh under real load; rollback: disable flag | L | P0 |
| 5 | MIG-003 | Promote to general availability 100% | Ops | MIG-002 | remove AUTH_NEW_LOGIN flag; all users on new AuthService; legacy auth deprecated; AUTH_TOKEN_REFRESH enabled; 99.9% uptime over first 7 days; all monitoring dashboards green; rollback: re-enable flag | L | P0 |
| 6 | MIG-006 | Document rollback procedure | Docs | MIG-001 | 6-step procedure documented: disable flag, verify legacy, investigate, restore backup if corruption, notify teams, post-mortem within 48h | M | P0 |
| 7 | MIG-007 | Configure rollback trigger criteria | Ops | MIG-001 | automated alerts: p95>1000ms for >5min, error-rate>5% for >2min, Redis failures>10/min, any data corruption; any trigger initiates rollback | M | P0 |

### Integration Points — Phase 7

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| AUTH_NEW_LOGIN flag (MIG-004) | Feature flag | Phase 7 | Phase 7 | LoginPage, RegisterPage, AuthService login endpoint |
| AUTH_TOKEN_REFRESH flag (MIG-005) | Feature flag | Phase 7 | Phase 7 | TokenManager refresh flow |
| Legacy auth routing | Reverse proxy strategy | Phase 7 | Phase 7 | API Gateway fallback during rollout |
| Monitoring dashboards (OPS-004) | Callback wiring | Phase 5 | Phase 7 | MIG-002 beta monitoring, MIG-003 GA monitoring |
| Rollback trigger alerts (MIG-007) | Event binding | Phase 7 | Phase 7 | PagerDuty/Opsgenie -> auth-team on-call |

## Risk Assessment and Mitigation

| # | Risk | Severity | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|---|---|
| 1 | R-001: Token theft via XSS | HIGH | Medium | Session hijacking; unauthorized access to user accounts | Store accessToken in memory only (not localStorage); HttpOnly cookies for refreshToken; 15-min access token expiry limits exposure window; CSP headers restrict script sources | auth-team |
| 2 | R-002: Brute-force attacks on login | MEDIUM | High | Account compromise; credential stuffing | Rate limiting at API Gateway (10 req/min/IP); account lockout after 5 failed attempts in 15 min; bcrypt cost-12 makes offline cracking infeasible; CAPTCHA after 3 failures on LoginPage | auth-team |
| 3 | R-003: Data loss during migration | HIGH | Low | User accounts inaccessible; service rollback required | Parallel operation during MIG-001/MIG-002; idempotent upsert operations; full backup before each phase; tested rollback procedure (MIG-006) | platform-team |
| 4 | R-004: Low registration adoption | HIGH | Medium | Business KPIs missed; personalization roadmap impact | Usability testing before launch (Alex persona validation); registration<60s target; funnel analytics on RegisterPage; iterate based on SC-006 conversion data | product-team |
| 5 | R-005: Security breach from flaws | CRITICAL | Low | Data exposure; regulatory consequences; trust damage | Dedicated security review before Phase 7; penetration testing on all API endpoints; OWASP Top 10 checklist; NFR-COMP-003 NIST validation | security-team |
| 6 | R-006: Incomplete audit logging | HIGH | Medium | SOC2 audit failure in Q3 2026; compliance gap | Define log requirements in Phase 1 (DM-003); validate against SOC2 controls in Phase 5 (NFR-COMP-002); 12-month retention confirmed; Jordan persona validates queryability | compliance-team |
| 7 | R-007: Email delivery failures | MEDIUM | Low | Password reset flow blocked; support ticket volume increases | SendGrid delivery monitoring and alerting (COMP-011); fallback support channel documented; same-response pattern prevents user enumeration regardless of delivery | auth-team |

## Resource Requirements and Dependencies

### External Dependencies

| Dependency | Required By Phase | Status | Fallback |
|---|---|---|---|
| DEP-001: PostgreSQL 15+ | Phase 1 | Required before start | No fallback; blocks all user persistence |
| DEP-002: Redis 7+ | Phase 1 | Required before start | Degrade to access-only tokens (no refresh); users must re-login on expiry |
| DEP-003: Node.js 20 LTS | Phase 1 | Required before start | No fallback; runtime dependency |
| DEP-004: bcryptjs | Phase 2 | Install at COMP-004 | No fallback; required for password hashing |
| DEP-005: jsonwebtoken | Phase 2 | Install at COMP-003 | No fallback; required for JWT sign/verify |
| DEP-006: SendGrid API | Phase 2 | Account provisioned | Password reset flow blocked (FR-AUTH-005); fallback: support ticket channel |
| DEP-007: Frontend routing framework | Phase 4 | Available in codebase | Auth pages cannot render; blocks all frontend work |

### Infrastructure Requirements

- **Compute:** 3 Kubernetes pods for AuthService (HPA to 10 at CPU >70%); estimated $150/month
- **PostgreSQL:** Managed instance with 100 connection pool (scalable to 200); partitioned audit_log table for 12-month retention; estimated $200/month
- **Redis:** 1 GB instance for refresh token storage (~100K tokens at ~50 MB); scale to 2 GB at 70% utilization; estimated $100/month
- **SendGrid:** API account for transactional email (password reset); delivery monitoring dashboard
- **Secrets management:** RSA key pair storage for JwtService; environment-based bcrypt config; feature flag service for AUTH_NEW_LOGIN and AUTH_TOKEN_REFRESH
- **Monitoring:** Prometheus for metrics collection; Grafana for dashboards; OpenTelemetry for distributed tracing; PagerDuty/Opsgenie for alerting
- **CI/CD:** testcontainers for PostgreSQL and Redis in CI pipeline; Docker Compose for local development
- **Total estimated cost:** $450/month base production; ~$50/month per additional 10K users

## Success Criteria and Validation Approach

| Criterion | Metric | Target | Validation Method | Phase |
|---|---|---|---|---|
| SC-001: Login response time | p95 latency on AuthService.login() | <200ms | APM tracing + k6 load test | Phase 3 (NFR-PERF-001) |
| SC-002: Registration success rate | Successful registrations / total attempts | >99% | Application metrics + error log analysis | Phase 3 (API-002) |
| SC-003: Token refresh latency | p95 latency on TokenManager.refresh() | <100ms | APM tracing on refresh endpoint | Phase 3 (NFR-PERF-001) |
| SC-004: Service availability | Uptime over 30-day rolling window | 99.9% | Health check monitoring (NFR-REL-001) | Phase 7 (MIG-003) |
| SC-005: Password hash time | PasswordHasher.hash() execution time | <500ms | Benchmark test with bcrypt cost 12 | Phase 2 (COMP-004) |
| SC-006: Registration conversion | Funnel: RegisterPage visit -> confirmed account | >60% | Frontend analytics on RegisterPage | Phase 7 (MIG-002) |
| SC-007: Daily active authenticated users | AuthToken issuance count per day | >1000 within 30 days of GA | Token issuance counter metrics | Phase 7 (MIG-003 + 30d) |
| SC-008: Average session duration | Time between first token issuance and last refresh | >30 minutes | Token refresh event analytics | Phase 7 (MIG-003 + 30d) |
| SC-009: Failed login rate | Failed login attempts / total attempts | <5% | Auth event log analysis (AuditLog) | Phase 7 (MIG-002) |
| SC-010: Password reset completion | Funnel: reset requested -> new password set | >80% | Email delivery + reset-confirm event tracking | Phase 7 (MIG-002) |

## Timeline Estimates

| Phase | Duration | Start | End | Key Milestones |
|---|---|---|---|---|
| Phase 1: Infrastructure & Data Foundation | 1.5 weeks | Week 1 | Week 2 | All schemas migrated; RS256+bcrypt configs validated; API gateway routing live |
| Phase 2: Core Backend Components | 2 weeks | Week 2 | Week 4 | All 5 backend components implemented; AuthService orchestrator wired; all FR flows passing unit tests |
| Phase 3: API Layer & Security Hardening | 1.5 weeks | Week 4 | Week 5 | All 6 endpoints live; rate limiting enforced; p95 <200ms validated; 500 concurrent logins sustained |
| Phase 4: Frontend Components & UX | 1.5 weeks | Week 5 | Week 7 | LoginPage, RegisterPage, ProfilePage, PasswordResetPage rendered; AuthProvider silent refresh working |
| Phase 5: Compliance, Observability & Operations | 1.5 weeks | Week 7 | Week 8 | GDPR consent captured; SOC2 audit logging live (12-month retention); all runbooks reviewed; HPA configured |
| Phase 6: Testing & Quality Assurance | 1.5 weeks | Week 8 | Week 10 | All TEST-xxx green; unit coverage >=80%; E2E journey passing; zero P0/P1 bugs |
| Phase 7: Migration & General Availability | 4 weeks | Week 10 | Week 14 | Alpha (week 10-11), Beta 10% (week 11-13), GA 100% (week 13-14); feature flags removed |

**Total estimated duration:** 14 weeks (3.5 months)

**Compliance gate:** SOC2 audit logging (NFR-COMP-002) must be validated before Phase 7 beta to ensure audit trail coverage during rollout. GDPR consent (NFR-COMP-001) must be live before any real user registration in Phase 7.

**Persona-driven sequencing rationale:**
- Alex (end user): Phases 1-4 deliver the core registration/login experience; Phase 7 beta validates <60s registration and seamless sessions
- Jordan (admin): Phase 5 delivers audit visibility; OQ-007 (admin log viewing UI) deferred pending TDD update
- Sam (API consumer): Phase 3 delivers stable auth contracts with clear error codes; Phase 7 beta validates programmatic token refresh

## Open Questions

| # | Question | Impact | Blocking Phase | Resolution Owner |
|---|---|---|---|---|
| 1 | OQ-001: Should AuthService support API key auth for service-to-service calls? | Affects API design; may require additional endpoint or auth middleware | Phase 3 | test-lead |
| 2 | OQ-002: Maximum allowed UserProfile roles array length? | Affects DM-001 schema constraints and validation logic | Phase 1 | auth-team |
| 3 | OQ-003: Password reset emails sent sync or async? | Affects API-005 response time and EmailService architecture | Phase 2 | Engineering |
| 4 | OQ-004: Max refresh tokens per user across devices? | Affects Redis memory planning (OPS-004) and TokenManager revocation logic | Phase 2 | Product |
| 5 | OQ-005: Support "remember me" extended session duration? | Affects AuthProvider and TokenManager TTL configuration | Phase 4 | Product |
| 6 | OQ-006: Logout functionality missing from TDD | PRD includes logout user story (Epic AUTH-E1); no FR, API endpoint, or component exists | Phase 2 | auth-team |
| 7 | OQ-007: Admin audit log viewing missing from TDD | PRD includes admin log viewing story (Epic AUTH-E3); no API endpoint for log querying | Phase 5 | auth-team |
| 8 | OQ-008: Audit log retention conflict (TDD: 90d vs PRD: 12mo) | Resolved: PRD wins; 12-month retention required; TDD Section 7.2 must be updated | Resolved | auth-team |
