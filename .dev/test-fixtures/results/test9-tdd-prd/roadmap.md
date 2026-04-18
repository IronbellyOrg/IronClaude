---
spec_source: "test-tdd-user-auth.md"
complexity_score: 0.65
complexity_class: MEDIUM
primary_persona: architect
adversarial: true
base_variant: "B (Haiku)"
variant_scores: "A:66 B:74"
convergence_score: 0.62
debate_rounds: 2
generated: "2026-04-15"
generator: "adversarial_merge"
total_phases: 5
total_task_rows: 68
risk_count: 7
open_questions: 8
---

# User Authentication Service — Project Roadmap

## Executive Summary

This roadmap defines a five-phase, 13-week implementation plan for a stateless JWT-based authentication service covering registration, login, logout, token lifecycle, profile retrieval, and self-service password reset. The system comprises 9 backend/frontend components orchestrated by `AuthService`, backed by PostgreSQL (user persistence, audit logs) and Redis (refresh token revocation), with a React frontend delivering login, registration, profile, and password-reset pages through an `AuthProvider` context.

The architecture delivers in compliance-first technical layers: ratify security and compliance constraints before schema freeze, implement backend auth flows and API contracts second, harden performance and validate SLOs third, wire user-facing and admin-facing surfaces with co-located testing fourth, and only then expand traffic under explicit rollout gates. This phasing — synthesized from adversarial debate between a 7-phase and 4-phase variant — balances compliance-first constraint ratification (debate convergence point) with dedicated E2E testing time (rebuttal concession) and realistic timeline buffering.

Four compliance obligations (GDPR consent at registration, GDPR data minimization, SOC2 12-month audit logging, NIST SP 800-63B password storage) are ratified as Phase 1 gate constraints on schemas, not deferred to post-functional validation. This prevents the late-stage schema rework pattern identified in the debate.

**Business Impact:** Authentication unblocks ~$2.4M projected annual revenue from personalization-dependent features. Delay past Q2 2026 risks SOC2 audit failure in Q3 and a full-quarter slip to the personalization roadmap. Three personas drive design: Alex (end user — registration <60s, seamless sessions), Jordan (admin — audit visibility, account management), Sam (API consumer — programmatic token management, clear error codes).

**Complexity:** MEDIUM (0.65) — Single-service scope with clear component boundaries, materially elevated by RS256 key management, brute-force defenses, Redis-backed refresh revocation, GDPR/SOC2/NIST constraints, and cross-layer FE/BE integration.

**Critical path:** NFR-SEC-001/002 + NFR-COMP-001/003/004 → DM-001 → COMP-005 → COMP-001 → FR-AUTH-001 → API-001 → NFR-PERF-001 → COMP-009 → COMP-006 → TEST-006 → MIG-001 → MIG-003. Compliance constraint ratification and infrastructure provisioning gate all downstream work.

**Key architectural decisions:**

- Stateless REST with JWT — no server-side session store; all session state in RS256-signed tokens with Redis-backed refresh token revocation; 15-minute access tokens and 7-day hashed refresh tokens
- Compliance-first constraint ratification — GDPR consent, data minimization, NIST password storage, and SOC2 audit schema validated as Phase 1 gate constraints before schema freeze, not as Phase 5 instrumentation
- Contract-first rollout — API Gateway rate limits, `AUTH_NEW_LOGIN` and `AUTH_TOKEN_REFRESH` feature flags, staged activation (alpha → 10% beta → GA), and hard rollback triggers

**Open risks requiring resolution before Phase 1:**

- OQ-008 must be resolved in favor of 12-month audit retention before schema, storage, and cost baselines are locked
- OQ-004 (max refresh tokens per user) affects Redis memory planning and TokenManager revocation logic; must define limit before `TokenManager` implementation
- OQ-001 (service-to-service auth) affects future API design; v1 scope decision must be recorded
- Logout (OQ-006) and admin audit viewing (OQ-007) are PRD-scope gaps; their component designs must be finalized before FE route structure hardens

## Phase 1: Security, Contracts & Persistence Baseline

**Objective:** Provision all data stores, ratify compliance constraints on schemas, configure cryptographic primitives, establish the API gateway, scaffold orchestrator interfaces, and resolve blocking open questions — the foundation every subsequent phase depends on | **Duration:** 2.5 weeks | **Entry:** PostgreSQL 15+, Redis 7+, Node.js 20 LTS provisioning initiated; RS256 key generation tooling available; PRD and TDD finalized | **Exit:** All schemas frozen with compliance constraints ratified; bcrypt and RS256 configs pass validation tests; API gateway routes `/v1/auth/*` with TLS 1.3 and CORS; OQ-004, OQ-008 resolved; AuthService and TokenManager skeleton interfaces compilable; logout and audit viewer designs documented

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | DEP-001 | Provision PostgreSQL 15+ primary | Infra | — | version:15+; pool:100-ready; backup:pre-phase; user+audit-store:reachable | L | P0 |
| 2 | DEP-002 | Provision Redis 7+ refresh store | Infra | — | version:7+; ttl:7d-ready; hash-store:on; failover:documented | M | P0 |
| 3 | DEP-003 | Pin Node.js 20 LTS runtime | Infra | — | runtime:20LTS; build:green; start:ok; drift:blocked-in-CI | S | P0 |
| 4 | DEP-004 | Lock bcryptjs dependency | Sec | DEP-003 | lib:bcryptjs; hash+verify:ok; cost12:supported; vuln:0-critical | S | P0 |
| 5 | DEP-005 | Lock jsonwebtoken dependency | Sec | DEP-003 | lib:jsonwebtoken; RS256:ok; verify:ok; vuln:0-critical | S | P0 |
| 6 | DEP-006 | Baseline SendGrid integration | Ops | — | api-key:provisioned; sandbox:ok; template-path:defined; fallback:support; test-email:200 | M | P1 |
| 7 | DEP-007 | Confirm frontend routing base | FE | — | routes:/login+/register+/profile+/reset-password; guards:supported; redirects:ok | S | P0 |
| 8 | OQ-008 | Resolve 12-month log retention | Gate | DEP-001 | retention:12mo; TDD-conflict:closed; storage-cost:accepted; schema:unblocked | S | P0 |
| 9 | OQ-001 | Decide service auth boundary | Gate | — | api-key-scope:decided; v1-impact:documented; defer/accept:recorded | S | P1 |
| 10 | OQ-004 | Set refresh token device limit | Gate | DEP-002 | per-user-limit:decided; eviction-policy:defined; UX-impact:documented | S | P0 |
| 11 | NFR-SEC-001 | Enforce bcrypt cost factor 12 | Sec | DEP-004 | algo:bcrypt; cost:12; hash-time<500ms; unit-test:pass; no-plaintext-persisted-or-logged | M | P0 |
| 12 | NFR-SEC-002 | Generate RS256 2048-bit key pair | Sec | DEP-005 | alg:RS256; key:2048b; private-key:secrets-store; public-key:JwtService-accessible; quarterly-rotation:documented; verify:pass; clock-skew:5s | M | P0 |
| 13 | NFR-COMP-001 | Ratify GDPR consent constraint | Sec | DM-001 | consent:required-at-registration; timestamp:stored; no-consent->400; proof:queryable; constrains:DM-001+COMP-007 | M | P0 |
| 14 | NFR-COMP-003 | Ban raw password persistence | Sec | NFR-SEC-001 | adaptive-hash:on; raw-store:none; raw-log:none; review:pass; constrains:COMP-004+FR-AUTH-002 | M | P0 |
| 15 | NFR-COMP-004 | Enforce GDPR data minimization | Sec | DM-001 | allow:email+password_hash+display_name; extra-PII:none; forms:trimmed; constrains:DM-001+COMP-007 | M | P0 |
| 16 | DM-001 | Create UserProfile PostgreSQL schema | DB | DEP-001, OQ-008, NFR-COMP-001, NFR-COMP-004 | id:UUID-PK; email:unique-idx-lower; display_name:varchar(2-100); password_hash:varchar-not-null; created_at:timestamptz-default-now; updated_at:timestamptz-auto; last_login_at:timestamptz-nullable; roles:text[]-default-user; consent_ts:timestamptz-nullable | L | P0 |
| 17 | DM-002 | Define AuthToken JWT+Redis structure | API | DEP-002, NFR-SEC-002 | access_token:JWT-RS256-signed; refresh_token:opaque-unique; expires_in:int-900; token_type:Bearer; refresh:stored-hashed-in-Redis; ttl:7d | M | P0 |
| 18 | DM-003 | Create AuditLog PostgreSQL schema | DB | DEP-001, OQ-008 | user_id:varchar-not-null; event_type:varchar-not-null; timestamp:timestamptz-not-null; ip_address:varchar-not-null; outcome:varchar-not-null; retention:12-month; partitioned:by-month | M | P0 |
| 19 | COMP-003 | Build JwtService module | Sec | NFR-SEC-002, DM-002 | sign():RS256-JWT-with-user-id+roles-payload; verify():validates-signature+expiry; clock-skew:5s; rejects:tampered-tokens | L | P0 |
| 20 | COMP-004 | Build PasswordHasher module | Sec | NFR-SEC-001 | hash():bcrypt-cost-12-digest; verify():validates-against-stored; hash-time<500ms; no-plaintext-logged; future-algorithm-migration:hooked | M | P0 |
| 21 | COMP-005 | Build UserRepo data access layer | DB | DM-001, DEP-001 | findByEmail(); createUser(); updateLastLogin(); connection-pool:pg-pool-size-100-scalable-to-200; conn-wait<50ms | L | P0 |
| 22 | COMP-001 | Scaffold AuthService orchestrator | API | COMP-003, COMP-004, COMP-005 | login(email,password):AuthToken; register(email,password,displayName):UserProfile; refresh(refreshToken):AuthToken; resetRequest(email):void; resetConfirm(token,password):void; delegates:PasswordHasher+TokenManager+UserRepo; emits:audit-events | M | P0 |
| 23 | COMP-002 | Scaffold TokenManager module | API | COMP-003, DEP-002, OQ-004 | issueTokens():AuthToken-pair; refresh():rotates-tokens; revoke():invalidates-in-Redis; stores:refresh-hash-with-7d-TTL; old-token-revoked-on-refresh | M | P0 |
| 24 | COMP-010 | Design logout coordination | API | COMP-001, COMP-002 | type:session-component; loc:cross-layer; action:end-session; revoke:refresh-token; redirect:landing; shared-device-risk:reduced | S | P1 |
| 25 | COMP-011 | Design audit log viewer | Ops | DM-003 | type:admin-component; loc:ops/admin; query:user+date; fields:userId+eventType+timestamp+ipAddress+outcome; access:admin-only; retention-view:12mo | M | P1 |
| 26 | OQ-002 | Bound roles array length | Gate | DM-001 | roles-max:decided; token-size:reviewed; validation:defined | S | P1 |
| 27 | INFRA-001 | Provision API Gateway with TLS/CORS | Infra | — | TLS-1.3-enforced; CORS:known-origins; route:/v1/auth/*; rate-limit-headers:present; health-check:200 | L | P0 |

### Integration Points — Phase 1

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| UserProfile schema (DM-001) | DDL migration | Phase 1 | Phase 1 | COMP-005 (UserRepo), DM-003 (AuditLog FK) |
| AuditLog schema (DM-003) | DDL migration | Phase 1 | Phase 1 | NFR-COMP-002 (SOC2 logging), COMP-011 (audit viewer) |
| AuthToken contract (DM-002) | Interface contract | Phase 1 | Phase 2 | COMP-002 (TokenManager), FR-AUTH-003 |
| RS256 key pair (NFR-SEC-002) | Secret mount | Phase 1 | Phase 1 | COMP-003 (JwtService) |
| bcrypt config (NFR-SEC-001) | Environment config | Phase 1 | Phase 1 | COMP-004 (PasswordHasher) |
| API Gateway (INFRA-001) | Reverse proxy | Phase 1 | Phase 2 | API-001 through API-006 |
| AuthService skeleton (COMP-001) | Interface contract | Phase 1 | Phase 2 | FR-AUTH-001 through FR-AUTH-005 |
| TokenManager skeleton (COMP-002) | Interface contract | Phase 1 | Phase 2 | FR-AUTH-003, API-004 |
| AuthService -> PasswordHasher | Service delegation | Phase 1 | Phase 2 | FR-AUTH-001, FR-AUTH-002, FR-AUTH-005 |
| AuthService -> UserRepo | Repository binding | Phase 1 | Phase 2 | FR-AUTH-001, FR-AUTH-002, FR-AUTH-004 |
| TokenManager -> JwtService | Service delegation | Phase 1 | Phase 2 | FR-AUTH-003, API-004 |
| TokenManager -> Redis | Cache/store binding | Phase 1 | Phase 2 | DM-002, FR-AUTH-003 |
| EmailService (DEP-006) | Service integration | Phase 1 | Phase 2 | FR-AUTH-005 (password reset) |
| Logout design (COMP-010) | Interface contract | Phase 1 | Phase 4 | COMP-009 (AuthProvider), FE logout action |
| Audit viewer design (COMP-011) | Interface contract | Phase 1 | Phase 4 | OQ-007 (admin scope) |

## Phase 2: Core Backend & API Contracts

**Objective:** Implement all backend auth flows through the scaffolded orchestrators and expose all six REST endpoints with rate limiting, input validation, and error standardization; wire SOC2 audit event persistence alongside the flows that emit audit events | **Duration:** 2 weeks | **Entry:** Phase 1 schemas frozen; compliance constraints ratified; bcrypt and RS256 configs validated; COMP-001/002 skeletons compilable; API Gateway routing confirmed | **Exit:** All five auth flows pass unit tests; all six API endpoints return correct status codes per AC; rate limiting enforced; SOC2 audit events persisting to AuditLog; error response format standardized

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | FR-AUTH-001 | Implement email/password login | Auth | COMP-001, COMP-004, COMP-005, API-001 | valid-creds->200+AuthToken; invalid->401+generic; unknown-email->401+no-enum; 5fail/15min->423; audit-event:emitted | L | P0 |
| 2 | FR-AUTH-002 | Implement registration with validation | Auth | COMP-001, COMP-004, COMP-005, API-002, NFR-COMP-001, NFR-COMP-004 | valid-reg->201+UserProfile; dup-email->409; weak-pwd(<8,no-upper,no-num)->400; bcrypt-cost-12-hash-stored; consent-ts:recorded | L | P0 |
| 3 | FR-AUTH-003 | Implement JWT issuance and refresh | Auth | COMP-002, COMP-003, DEP-002, API-004 | login->access15min+refresh7d; valid-refresh->200+new-pair; expired->401; revoked->401; old-token-revoked-on-refresh | L | P0 |
| 4 | FR-AUTH-004 | Implement profile retrieval | Auth | COMP-001, COMP-005, API-003 | valid-bearer->200+UserProfile(id,email,displayName,createdAt,updatedAt,lastLoginAt,roles); invalid/expired-token->401 | M | P0 |
| 5 | FR-AUTH-005 | Implement password reset flow | Auth | COMP-001, COMP-004, DEP-006, API-005, API-006 | request(valid-email)->sends-token-email; confirm(valid-token)->updates-hash; token-1h-TTL; single-use; same-response-for-unknown-email | L | P0 |
| 6 | NFR-COMP-002 | Persist SOC2 audit events | Sec | DM-003, COMP-001, OQ-008 | events:login_success+login_failure+registration+password_reset+token_refresh; fields:userId+timestamp+ip+outcome; retention:12mo; storage:queryable; partitioned | L | P0 |
| 7 | API-001 | Implement POST /auth/login endpoint | API | FR-AUTH-001, INFRA-001 | valid-creds->200+AuthToken; invalid->401; locked->423; rate:10req/min/IP->429; error-format:{code,message,status} | M | P0 |
| 8 | API-002 | Implement POST /auth/register endpoint | API | FR-AUTH-002, INFRA-001 | valid->201+UserProfile; dup-email->409; weak-pwd->400; invalid-email->400; rate:5req/min/IP; displayName:2-100chars; consent:required | M | P0 |
| 9 | API-003 | Implement GET /auth/me endpoint | API | FR-AUTH-004, INFRA-001 | Bearer-token->200+UserProfile(id,email,displayName,createdAt,updatedAt,lastLoginAt,roles); missing/expired/invalid-token->401; rate:60req/min/user | M | P0 |
| 10 | API-004 | Implement POST /auth/refresh endpoint | API | FR-AUTH-003, INFRA-001 | valid-refresh->200+new-AuthToken; expired->401; revoked->401; old-token-invalidated; rate:30req/min/user | M | P0 |
| 11 | API-005 | Implement POST /auth/reset-request | API | FR-AUTH-005, INFRA-001 | any-email->same-success-response; registered-email-triggers-SendGrid; no-enumeration; token-1h-TTL | M | P1 |
| 12 | API-006 | Implement POST /auth/reset-confirm | API | FR-AUTH-005, INFRA-001 | valid-token+strong-pwd->password-updated; expired-token->error; used-token->error; weak-pwd->400 | M | P1 |

### Integration Points — Phase 2

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| /v1/auth router -> handlers | Dispatch table | Phase 2 | Phase 2 | API-001, API-002, API-003, API-004, API-005, API-006 |
| Rate-limit middleware -> endpoints | Middleware chain | Phase 2 | Phase 2 | API-001 (10/min), API-002 (5/min), API-003 (60/min), API-004 (30/min) |
| Bearer token validation middleware | Middleware chain | Phase 2 | Phase 2 | API-003 (auth-required) |
| Error response formatter | Middleware chain | Phase 2 | Phase 2 | All API-xxx endpoints |
| PasswordHasher.hash()/verify() | Method dispatch | Phase 1 | Phase 2 | COMP-001 (AuthService) login + registration |
| TokenManager.issueTokens()/refresh()/revoke() | Method dispatch | Phase 1 | Phase 2 | COMP-001 (AuthService) login + refresh |
| JwtService.sign()/verify() | Method dispatch | Phase 1 | Phase 2 | COMP-002 (TokenManager) |
| UserRepo.findByEmail()/createUser() | Data access dispatch | Phase 1 | Phase 2 | COMP-001 (AuthService) |
| Redis client | Connection pool | Phase 1 | Phase 2 | COMP-002 (TokenManager) refresh token store |
| Password reset request -> SendGrid | Service callback | Phase 2 | Phase 2 | FR-AUTH-005, API-005 |
| Auth events -> AuditLog writer | Event binding | Phase 2 | Phase 2 | NFR-COMP-002, Jordan persona |

**Phase 2 Exit Checklist — Success Criteria:**
- SC-005: Password hash time <500ms (bcrypt cost-12 benchmark in CI)

## Phase 3: API Hardening & Performance

**Objective:** Validate API response time targets under load, prove concurrency capacity, and establish uptime monitoring — the quality gate that separates implementation from user-facing work | **Duration:** 1.5 weeks | **Entry:** All Phase 2 endpoints returning correct responses; rate limiting enforced; audit events persisting | **Exit:** p95 login <200ms; 500 concurrent logins sustained with no 5xx; 99.9% uptime monitoring live with alert routing; all Phase 3 exit criteria pass

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | NFR-PERF-001 | Validate API p95 response <200ms | API | API-001, FR-AUTH-001 | p95-login<200ms; p95-register<200ms; p95-refresh<100ms; APM-tracing:on-AuthService-methods; regression-threshold:set | L | P0 |
| 2 | NFR-PERF-002 | Load test 500 concurrent logins | API | API-001, NFR-PERF-001 | k6-load-test; 500-concurrent-login-requests; no-5xx; p95<200ms; connection-pool:stable; Redis-latency:stable | L | P1 |
| 3 | NFR-REL-001 | Establish 99.9% uptime monitoring | Ops | API-001, INFRA-001 | health-check:monitored; 30d-rolling-SLA; alert:downtime>4.3min/month; Grafana-dashboard:live; alert-route:auth-team | M | P0 |

### Integration Points — Phase 3

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| APM tracing instrumentation | Callback wiring | Phase 3 | Phase 3 | NFR-PERF-001, OPS-004 (capacity planning) |
| k6 load test scripts | Test fixture | Phase 3 | Phase 5 | MIG-002 (beta load validation) |
| Health check endpoint | HTTP probe | Phase 3 | Phase 5 | MIG-002 monitoring, NFR-REL-001 uptime |
| Grafana uptime dashboard | Callback wiring | Phase 3 | Phase 5 | OPS-003 (on-call), MIG-007 (rollback triggers) |
| Prometheus metrics exporter | Callback wiring | Phase 3 | Phase 5 | OPS-004 (capacity planning) |

**Phase 3 Exit Checklist — Success Criteria:**
- SC-001: Login p95 <200ms (APM tracing + k6 load test)
- SC-002: Registration success rate >99% (success/attempts ratio on API-002)
- SC-003: Token refresh p95 <100ms (APM tracing on TokenManager.refresh())
- SC-005: Password hash time <500ms (bcrypt cost-12 benchmark)

## Phase 4: Frontend, Testing & E2E

**Objective:** Build all frontend page components and the AuthProvider context, resolve remaining open questions for logout and admin scope, execute co-located unit/integration tests, and run a dedicated E2E testing window with penetration testing before rollout | **Duration:** 3 weeks (2 weeks frontend + co-located testing, 1 week dedicated E2E + security review) | **Entry:** All API endpoints returning correct responses; performance targets met; Bearer token validation working; logout and audit viewer designs documented | **Exit:** All pages render correctly; AuthProvider handles silent refresh and 401 interception; all TEST-xxx pass green; unit coverage >=80%; E2E Playwright test completes register->login->profile journey; penetration test passes with zero critical findings; zero P0/P1 bugs

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | OQ-003 | Choose reset email dispatch | Gate | DEP-006, API-005 | mode:sync/async-decided; email-SLA:<60s; retry:defined; failure-UX:set | S | P1 |
| 2 | OQ-005 | Decide remember-me scope | Gate | FR-AUTH-003, COMP-009 | support:yes/no; session-impact:documented; v1/v1.1:assigned | S | P1 |
| 3 | OQ-006 | Specify logout v1 scope | Gate | COMP-010, COMP-009 | logout-story:covered; revoke-path:defined; redirect:landing; shared-device-risk:reduced | S | P0 |
| 4 | OQ-007 | Specify audit viewer scope | Gate | COMP-011, DM-003 | filters:user+date; access:admin-only; retention-view:12mo; incident-use:covered | S | P0 |
| 5 | COMP-009 | Build AuthProvider context | FE | API-004, API-003, OQ-005 | wraps-App-root; manages-AuthToken-state; silent-refresh-via-TokenManager; 401-interception+redirect; exposes-UserProfile+auth-methods; handles-7d-refresh-expiry; props:children:ReactNode | L | P0 |
| 6 | COMP-006 | Build LoginPage component | FE | COMP-009, API-001 | route:/login; email+password-form; onSuccess-callback; redirectUrl-prop; submits-to-API-001; generic-error-on-failure; no-user-enumeration; stores-AuthToken-via-AuthProvider | L | P0 |
| 7 | COMP-007 | Build RegisterPage component | FE | COMP-009, API-002, NFR-COMP-001 | route:/register; email+password+displayName-form; termsUrl-prop; inline-password-strength-validation; consent-checkbox-required; submits-to-API-002; dup-email-shows-helpful-message; registration<60s | L | P0 |
| 8 | COMP-008 | Build ProfilePage component | FE | COMP-009, API-003 | route:/profile; auth-required; displays-UserProfile(id,email,displayName,createdAt,updatedAt,lastLoginAt,roles); loads-via-GET-/auth/me; renders<1s | M | P0 |
| 9 | COMP-012 | Build PasswordResetPage component | FE | API-005, API-006 | route:/reset-password; two-step:request-form(email)+confirm-form(token+new-password); inline-password-validation; same-UX-for-registered/unregistered; expired-link-error-with-retry | L | P1 |
| 10 | TEST-001 | Unit test login valid credentials | Test | FR-AUTH-001, COMP-001 | AuthService.login()-calls-PasswordHasher.verify()+TokenManager.issueTokens(); returns-valid-AuthToken; mocks:PasswordHasher,TokenManager,UserRepo | M | P0 |
| 11 | TEST-002 | Unit test login invalid credentials | Test | FR-AUTH-001, COMP-001 | 401-when-PasswordHasher.verify()-returns-false; no-AuthToken-issued; mocks:PasswordHasher(false),UserRepo | M | P0 |
| 12 | TEST-003 | Unit test token refresh valid | Test | FR-AUTH-003, COMP-002 | old-token-revoked; new-AuthToken-pair-issued-via-JwtService; mocks:Redis-client,JwtService | M | P0 |
| 13 | TEST-004 | Integration test registration DB | Test | FR-AUTH-002, COMP-005 | full-flow:API-request->PasswordHasher->PostgreSQL-insert; UserProfile-retrievable; testcontainers; no-mocks | L | P0 |
| 14 | TEST-005 | Integration test expired refresh | Test | FR-AUTH-003, COMP-002 | expired-Redis-TTL->401; real-Redis-via-testcontainers; TTL-based-invalidation:confirmed | L | P0 |
| 15 | TEST-006 | E2E register-login-profile flow | Test | COMP-006, COMP-007, COMP-008, COMP-009 | Playwright:RegisterPage->LoginPage->ProfilePage; user-sees-profile-data; AuthProvider-handles-token-lifecycle; full-stack; no-mocks | XL | P0 |

### Integration Points — Phase 4

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| AuthProvider.login()/logout()/refresh() | Context dispatch | Phase 4 | Phase 4 | COMP-006 (LoginPage), COMP-007 (RegisterPage) |
| AuthProvider.user (UserProfile state) | Context subscription | Phase 4 | Phase 4 | COMP-008 (ProfilePage) |
| AuthProvider 401 interceptor | Callback wiring | Phase 4 | Phase 4 | All authenticated routes |
| AuthProvider silent refresh timer | Event binding | Phase 4 | Phase 4 | Token expiry cycle (every <15min) |
| Frontend routing framework (DEP-007) | Route registry | Phase 1 | Phase 4 | /login, /register, /profile, /reset-password |
| Logout action -> token revoker | Event binding | Phase 4 | Phase 4 | OQ-006, COMP-010 |
| GDPR consent checkbox (NFR-COMP-001) | Schema constraint | Phase 1 | Phase 4 | COMP-007 (RegisterPage) |
| testcontainers PostgreSQL | Test fixture | Phase 4 | Phase 4 | TEST-004 (registration persistence) |
| testcontainers Redis | Test fixture | Phase 4 | Phase 4 | TEST-005 (token expiry) |
| Jest mock factories | Dependency injection | Phase 4 | Phase 4 | TEST-001, TEST-002, TEST-003 |
| Playwright test harness | E2E framework | Phase 4 | Phase 4 | TEST-006 (full journey) |

**Phase 4 Exit Checklist — Success Criteria:**
- SC-006: Registration conversion >60% (landing->register->confirmed funnel analytics)
- SC-010: Password reset completion >80% (reset-requested->new-password-set funnel)
- Unit coverage >=80% on AuthService, TokenManager, PasswordHasher, JwtService, UserRepo
- Zero P0/P1 bugs; penetration test: zero critical findings

## Phase 5: Rollout & Operations

**Objective:** Execute the three-phase rollout (internal alpha, 10% beta, 100% GA) with feature flags, monitoring, and documented rollback procedures; establish operational readiness with runbooks, on-call, and capacity planning; remove feature flags post-GA | **Duration:** 4 weeks (1 week alpha + 2 weeks beta + 1 week GA) | **Entry:** All TEST-xxx green; zero P0/P1 bugs; penetration test passed; monitoring dashboards live; runbooks drafted | **Exit:** AUTH_NEW_LOGIN flag removed; 100% traffic on new AuthService; 99.9% uptime over first 7 days; all rollback criteria monitored; on-call rotation staffed; post-mortem template ready

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | MIG-004 | Configure AUTH_NEW_LOGIN flag | Ops | TEST-006 | flag-gates:LoginPage+AuthService-login; default:OFF; toggleable-per-env; flag-state:logged-for-audit | S | P0 |
| 2 | MIG-005 | Configure AUTH_TOKEN_REFRESH flag | Ops | TEST-006 | flag-gates:refresh-token-flow-in-TokenManager; default:OFF; when-OFF:only-access-tokens; flag-state:logged | S | P0 |
| 3 | MIG-001 | Deploy internal alpha to staging | Ops | MIG-004, MIG-005 | env:staging; users:auth-team+QA; flag:AUTH_NEW_LOGIN-on; 1-week-duration; all-FRs-pass-manual-testing; P0/P1:0; rollback:disable-flag | L | P0 |
| 4 | MIG-002 | Execute beta rollout at 10% traffic | Ops | MIG-001 | AUTH_NEW_LOGIN:10%-traffic; 2-weeks-duration; p95<200ms; error-rate<0.1%; Redis-failures:0; AuthProvider-refresh-under-load:validated; rollback:disable-flag | L | P0 |
| 5 | MIG-003 | Promote to general availability | Ops | MIG-002 | remove:AUTH_NEW_LOGIN-flag; all-users-on-new-AuthService; legacy:deprecated; AUTH_TOKEN_REFRESH:enabled; 99.9%-uptime-over-7d; dashboards:green; rollback:re-enable-flag | L | P0 |
| 6 | MIG-006 | Document rollback procedure | Docs | MIG-001 | 6-step:disable-flag->verify-legacy->investigate->restore-backup->notify-teams->postmortem<48h | M | P0 |
| 7 | MIG-007 | Configure rollback trigger criteria | Ops | MIG-001, NFR-PERF-001, NFR-REL-001 | p95>1000ms/5min->rollback; err>5%/2min->rollback; Redis-fail>10/min->rollback; data-corruption->rollback; automated-alerts:configured | M | P0 |
| 8 | OPS-001 | Publish AuthService-down runbook | Ops | COMP-001, DEP-001, DEP-002 | symptoms:5xx+/auth/*; diag:k8s+PG+Redis+logs; resolve:restart/failover; escalate:auth-team->test-lead->eng-manager->platform-team; ack<15min | M | P0 |
| 9 | OPS-002 | Publish refresh-failure runbook | Ops | COMP-002, COMP-003, MIG-005 | symptoms:logout-loop+counter-spike; diag:Redis-conn+JwtService-key+feature-flag; resolve:scale/remount/enable-flag; page:on-call | M | P0 |
| 10 | OPS-003 | Staff 24/7 launch on-call rotation | Ops | MIG-003, OPS-001, OPS-002 | 24/7-rotation:first-2-weeks-post-GA; P1-ack<15min; tools:K8s-dashboards+Grafana+RedisCLI+PGadmin; knowledge-prereqs:documented | M | P1 |
| 11 | OPS-004 | Validate capacity scaling plan | Infra | NFR-PERF-002, DEP-001, DEP-002 | AuthService:3-pods-HPA-to-10@CPU>70%; PostgreSQL:pool-100-scale-to-200@wait>50ms; Redis:1GB-scale-to-2GB@mem>70%; Prometheus-metrics:auth_login_total+auth_login_duration_seconds+auth_token_refresh_total+auth_registration_total; OpenTelemetry:tracing | L | P0 |

### Integration Points — Phase 5

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| AUTH_NEW_LOGIN flag (MIG-004) | Feature flag | Phase 5 | Phase 5 | LoginPage, RegisterPage, AuthService login endpoint |
| AUTH_TOKEN_REFRESH flag (MIG-005) | Feature flag | Phase 5 | Phase 5 | TokenManager refresh flow |
| Legacy auth routing | Reverse proxy strategy | Phase 5 | Phase 5 | API Gateway fallback during rollout |
| Monitoring dashboards (OPS-004) | Callback wiring | Phase 3 | Phase 5 | MIG-002 beta monitoring, MIG-003 GA monitoring |
| Rollback trigger alerts (MIG-007) | Event binding | Phase 5 | Phase 5 | PagerDuty/Opsgenie -> auth-team on-call |
| Feature flag service -> login routes | Registry/gating | Phase 5 | Phase 5 | MIG-001, MIG-002, MIG-003, MIG-004 |
| Feature flag service -> refresh flow | Registry/gating | Phase 5 | Phase 5 | MIG-003, MIG-005, OPS-002 |
| Analytics funnel -> product reviews | Reporting pipeline | Phase 5 | Phase 5 | SC-006, SC-007, SC-008, SC-009, SC-010 |

**Phase 5 Exit Checklist — Success Criteria:**
- SC-004: Service availability 99.9% over 30-day rolling window (health-check monitoring)
- SC-007: >1000 daily active authenticated users within 30 days of GA (token issuance analytics)
- SC-008: Average session duration >30 minutes (refresh event analytics)
- SC-009: Failed login rate <5% of attempts (audit log analysis)

## Risk Assessment and Mitigation

Prioritize security and compliance gates before broad traffic exposure. Treat Redis, PostgreSQL, and email delivery as independent failure domains with rehearsed fallbacks. Do not remove feature flags until GA telemetry is stable and rollback drills have passed.

| # | Risk | Severity | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|---|---|
| 1 | R-001: Token theft via XSS | HIGH | Medium | Session hijacking; unauthorized access to user accounts; forced resets | accessToken in memory only (not localStorage); HttpOnly cookies for refreshToken; 15-min access token expiry limits exposure; CSP headers restrict script sources; revoke workflow ready | security + FE |
| 2 | R-002: Brute-force login abuse | MEDIUM | High | Account compromise; credential stuffing; attack traffic; support load | Rate limiting at API Gateway (10 req/min/IP); account lockout after 5 failed attempts in 15 min; bcrypt cost-12 makes offline cracking infeasible; CAPTCHA after 3 failures on LoginPage; WAF blocks ready | security + platform |
| 3 | R-003: Data loss during migration | HIGH | Low | User accounts inaccessible; service rollback required; launch delay | Parallel operation during MIG-001/MIG-002; idempotent upsert operations; full backup before each phase; tested rollback procedure (MIG-006); legacy parallel path | platform + DB |
| 4 | R-004: Low registration adoption | HIGH | Medium | Business KPIs missed (SC-006 <60%); personalization roadmap impact; revenue delay | Usability testing before launch (Alex persona validation); registration <60s target; funnel analytics on RegisterPage; iterate based on SC-006 conversion data | product + FE |
| 5 | R-005: Security breach from flaws | CRITICAL | Low | Data exposure; regulatory consequences; trust damage; incident response | Dedicated security review before Phase 5; penetration testing on all API endpoints; OWASP Top 10 checklist; NFR-COMP-003 NIST validation; prod gate blocked until zero critical findings | security |
| 6 | R-006: Incomplete audit logging | HIGH | Medium | SOC2 audit failure in Q3 2026; compliance gap; incident blind spots | Define log requirements in Phase 1 (DM-003); validate against SOC2 controls in Phase 2 (NFR-COMP-002); 12-month retention confirmed; Jordan persona validates queryability via COMP-011 | compliance + ops |
| 7 | R-007: Email delivery failures | MEDIUM | Low | Password reset flow blocked; support ticket volume increases | SendGrid delivery monitoring and alerting (DEP-006); retry policy defined; fallback support channel documented; same-response pattern prevents user enumeration regardless of delivery | ops |

## Resource Requirements and Dependencies

### External Dependencies

| Dependency | Required By Phase | Status | Fallback |
|---|---|---|---|
| DEP-001: PostgreSQL 15+ | Phase 1 | Must provision before schema freeze | No fallback; blocks all user persistence |
| DEP-002: Redis 7+ | Phase 1 | Must provision before refresh design | Degrade to access-only tokens (no refresh); users must re-login on expiry |
| DEP-003: Node.js 20 LTS | Phase 1 | Standardize in CI and runtime images | No fallback; runtime dependency |
| DEP-004: bcryptjs | Phase 1 | Pin and security-scan before implementation | No fallback in v1.0 |
| DEP-005: jsonwebtoken | Phase 1 | Pin and validate RS256 support | No fallback in v1.0 |
| DEP-006: SendGrid API | Phase 1 (baseline), Phase 2 (integration) | Account provisioned, sandbox validated | Password reset flow blocked (FR-AUTH-005); fallback: support ticket channel |
| DEP-007: Frontend routing framework | Phase 1 | Confirm guard and redirect support | Auth pages cannot render; blocks all frontend work |
| SEC-POLICY-001: Security policy | Phase 1 | Product/security signoff required | Freeze security-sensitive scope until clarified |

### Infrastructure Requirements

- **Compute:** 3 Kubernetes pods for AuthService (HPA to 10 at CPU >70%); estimated $150/month
- **PostgreSQL:** Managed instance with 100 connection pool (scalable to 200 at wait >50ms); partitioned audit_log table for 12-month retention; estimated $200/month
- **Redis:** 1 GB instance for refresh token storage (~100K tokens at ~50 MB); scale to 2 GB at 70% utilization; estimated $100/month
- **SendGrid:** API account for transactional email (password reset); delivery monitoring dashboard
- **Secrets management:** RSA key pair storage for JwtService; environment-based bcrypt config; feature flag service for AUTH_NEW_LOGIN and AUTH_TOKEN_REFRESH
- **Monitoring:** Prometheus for metrics collection; Grafana for dashboards; OpenTelemetry for distributed tracing; PagerDuty/Opsgenie for alerting
- **CI/CD:** testcontainers for PostgreSQL and Redis in CI pipeline; Docker Compose for local development
- **Total estimated cost:** $450/month base production; ~$50/month per additional 10K users

### Teaming and Ownership

- **auth-team:** Backend service implementation, token lifecycle, AuthService orchestrator, test ownership, on-call rotation
- **frontend team:** AuthProvider, LoginPage, RegisterPage, ProfilePage, PasswordResetPage, funnel UX, consent checkbox
- **security/compliance:** RS256 key management, NIST/GDPR/SOC2 validation, penetration testing, audit coverage review
- **platform/ops:** Infrastructure provisioning, feature flag service, monitoring dashboards, on-call tooling, rollback rehearsals, capacity planning

## Success Criteria and Validation Approach

Success criteria are validated as phase exit checklists (see each phase above), not as individual task rows. This follows Opus's separation-of-concerns argument accepted in the debate synthesis: metric checks are governance artifacts validated at phase boundaries, not M-effort deliverables competing for tracker space.

| Criterion | Metric | Target | Validation Method | Phase |
|---|---|---|---|---|
| SC-001 | Login response time (p95) | <200ms | APM tracing on AuthService.login() + k6 load test | Phase 3 exit |
| SC-002 | Registration success rate | >99% | Registration attempt/success ratio on API-002 | Phase 3 exit |
| SC-003 | Token refresh latency (p95) | <100ms | APM tracing on TokenManager.refresh() | Phase 3 exit |
| SC-004 | Service availability | 99.9% uptime | 30-day health-check monitoring and alert audit | Phase 5 exit |
| SC-005 | Password hash time | <500ms | bcrypt cost-12 benchmark in CI and pre-GA | Phase 2 exit |
| SC-006 | Registration conversion | >60% | Landing->register->confirmed funnel analytics | Phase 4 exit |
| SC-007 | Daily active authenticated users | >1000 in 30 days | Token issuance and active-user analytics | Phase 5 exit (GA+30d) |
| SC-008 | Average session duration | >30 minutes | Refresh event analytics and cohort review | Phase 5 exit (GA+30d) |
| SC-009 | Failed login rate | <5% of attempts | Audit log analysis with alert thresholds | Phase 5 exit |
| SC-010 | Password reset completion | >80% | Reset-requested->password-updated funnel | Phase 4 exit |

**Validation sequence:**
- Phase 1: Contract and schema validation, security baseline checks, dependency readiness
- Phase 2: Unit tests alongside implementation, API contract validation, audit event persistence checks
- Phase 3: Performance benchmarks (SC-001, SC-002, SC-003, SC-005), load test, uptime monitoring activation
- Phase 4: Co-located unit/integration tests, Playwright E2E journeys (TEST-006), UX checks against Alex/Jordan/Sam personas, penetration testing, SC-006 and SC-010 funnel baselines
- Phase 5: Staged rollout telemetry, rollback rehearsal (MIG-006), security/compliance signoff, GA metric review (SC-004, SC-007, SC-008, SC-009)

## Timeline Estimates

| Phase | Duration | Start | End | Key Milestones |
|---|---|---|---|---|
| Phase 1: Security, Contracts & Persistence Baseline | 2.5 weeks | 2026-04-15 | 2026-04-29 | Infra provisioned; OQ-008+OQ-004 resolved; schemas frozen with compliance constraints; core modules built; orchestrator skeletons compilable |
| Phase 2: Core Backend & API Contracts | 2 weeks | 2026-04-30 | 2026-05-13 | All 5 auth flows implemented; 6 API endpoints live with rate limiting; SOC2 audit events persisting; SC-005 validated |
| Phase 3: API Hardening & Performance | 1.5 weeks | 2026-05-14 | 2026-05-22 | p95 <200ms validated; 500 concurrent logins sustained; 99.9% uptime monitoring live; SC-001/002/003 pass |
| Phase 4: Frontend, Testing & E2E | 3 weeks | 2026-05-23 | 2026-06-12 | All FE pages rendered; AuthProvider stable; E2E Playwright journey green; unit coverage >=80%; penetration test passed; zero P0/P1 |
| Phase 5: Rollout & Operations | 4 weeks | 2026-06-13 | 2026-07-10 | Alpha (week 1), Beta 10% (weeks 2-3), GA 100% (week 4); feature flags removed; runbooks published; on-call staffed; SC-004/007/008/009 tracked |

**Total estimated duration:** 13 weeks (2026-04-15 to 2026-07-10)

**Timeline rationale:** The 13-week timeline splits the difference between Opus's 14-week estimate (realistic but sequentially structured) and Haiku's 11-week estimate (aggressive but compliance-first). The 0.5-week buffer on Phase 1 accounts for the front-loaded 27-task baseline. The 1-week dedicated E2E window in Phase 4 (debate concession from Opus) prevents QA squeeze when frontend runs long. Absolute dates anchor to the SOC2 Q3 2026 deadline; GA on July 10 provides margin for the Q3 audit preparation.

**Compliance gate:** GDPR consent (NFR-COMP-001) ratified as Phase 1 constraint, captured at registration from Phase 2 onward. SOC2 audit logging (NFR-COMP-002) wired in Phase 2 alongside the flows that emit events. Both are live before any real-user traffic in Phase 5.

**Persona-driven sequencing:**
- Alex (end user): Phases 1-4 deliver the core registration/login/reset experience; Phase 5 beta validates <60s registration and seamless sessions
- Jordan (admin): Phase 1 designs audit viewer (COMP-011); Phase 2 wires audit persistence (NFR-COMP-002); Phase 4 specifies admin scope (OQ-007)
- Sam (API consumer): Phase 2 delivers stable auth API contracts with clear error codes; Phase 3 validates p95 targets; Phase 5 beta validates programmatic token refresh

## Open Questions

| # | Question | Impact | Blocking Phase | Resolution Owner |
|---|---|---|---|---|
| 1 | OQ-001: Should AuthService support API key auth for service-to-service calls? | Affects API design; may require additional endpoint or auth middleware | Phase 1 | test-lead |
| 2 | OQ-002: Maximum allowed UserProfile roles array length? | Affects DM-001 schema constraints, JWT size, and downstream auth payloads | Phase 1 | auth-team |
| 3 | OQ-003: Password reset emails sent synchronously or asynchronously? | Changes UX latency, queueing design, and delivery retry model | Phase 4 | Engineering |
| 4 | OQ-004: Max refresh tokens per user across devices? | Affects Redis memory planning (OPS-004), TokenManager revocation logic, and device UX | Phase 1 | Product |
| 5 | OQ-005: Support "remember me" extended session duration? | Changes FE session UX, AuthProvider config, and token lifetime expectations | Phase 4 | Product |
| 6 | OQ-006: Logout functionality missing from TDD | PRD includes logout user story (Epic AUTH-E1); no FR, API endpoint, or component in TDD; affects session revocation and shared-device safety | Phase 4 | Product + Engineering |
| 7 | OQ-007: Admin audit log viewing missing from TDD | PRD includes admin log viewing story (Epic AUTH-E3); no API endpoint for log querying in TDD; affects Jordan persona and incident workflows | Phase 4 | Product + Engineering |
| 8 | OQ-008: Audit log retention conflict (TDD: 90d vs PRD: 12mo) | Resolved: PRD wins; 12-month retention required per SOC2; TDD Section 7.2 must be updated; affects storage sizing and compliance signoff | Resolved (Phase 1 gate) | auth-team |
