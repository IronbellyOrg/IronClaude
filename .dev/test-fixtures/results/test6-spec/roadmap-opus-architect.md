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
total_task_rows: 52
risk_count: 6
open_questions: 6
---

# User Authentication Service - Project Roadmap

## Executive Summary

This roadmap defines the implementation plan for a JWT-based user authentication service covering login, registration, token refresh, profile retrieval, and password reset. The system uses RS256 asymmetric JWT signing, bcrypt password hashing (cost factor 12), and refresh token rotation with replay detection. The architecture follows a layered pattern (AuthService > TokenManager > JwtService) with strict dependency ordering that constrains parallelization but ensures testability at each layer.

**Business Impact:** Authentication is a gating capability - no user-facing feature can ship without it. Delays here cascade to every downstream service that requires identity verification.

**Complexity:** MEDIUM (0.6) - Well-understood JWT/bcrypt patterns reduce novelty risk, but replay detection, token rotation, and RS256 key management elevate security sensitivity above typical CRUD implementations.

**Critical path:** RSA key provisioning > JwtService > TokenManager > AuthService > AuthMiddleware > Route registration > Integration tests > Feature flag rollout

**Key architectural decisions:**

- RS256 asymmetric signing with secrets-manager-stored private key enables key rotation without service restart and supports multi-service token verification via public key distribution
- Stateless JWT access tokens (no server-side session store) for horizontal scalability; revocation handled through short TTL (15min) plus refresh token DB check
- Refresh token rotation with replay detection: reuse of a rotated token invalidates ALL user sessions, trading single-device UX for security posture

**Open risks requiring resolution before Phase 1:**

- OQ-6: REST paths for registration, refresh, and reset endpoints must be finalized before route implementation
- OQ-1: Email dispatch strategy (sync vs queue) affects password reset endpoint latency budget and error handling design

## Phase 0: Foundation & Infrastructure

**Objective:** Provision database schema, install dependencies, configure secrets management, and establish feature flag gating | **Duration:** 2-3 days | **Entry:** Endpoint paths finalized (OQ-6) | **Exit:** Migration applied; RSA key pair accessible; feature flag toggles auth routes off

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | MIG-001 | Create users table migration | DB | - | id:UUID-PK; email:varchar-unique-idx; display_name:varchar; password_hash:varchar; is_locked:bool-default-false; created_at:timestamptz; updated_at:timestamptz; up+down scripts | M | P0 |
| 2 | MIG-002 | Create refresh_tokens table migration | DB | MIG-001 | id:UUID-PK; user_id:FK>users.id-cascade; token_hash:varchar; expires_at:timestamptz; revoked:bool-default-false; created_at:timestamptz; up+down scripts; idx on user_id | M | P0 |
| 3 | MIG-003 | Write down-migration rollback scripts | DB | MIG-001, MIG-002 | down drops refresh_tokens then users; idempotent; tested in clean DB | S | P0 |
| 4 | DM-001 | Define UserRecord interface | Auth | MIG-001 | id:string(UUID-v4); email:string(unique,indexed); display_name:string; password_hash:string(bcrypt); is_locked:boolean; created_at:Date; updated_at:Date | S | P0 |
| 5 | DM-002 | Define RefreshTokenRecord interface | Auth | MIG-002 | id:string(UUID-v4); user_id:string(FK>UserRecord.id); token_hash:string(SHA-256); expires_at:Date; revoked:boolean; created_at:Date | S | P0 |
| 6 | DM-003 | Define AuthTokenPair response DTO | Auth | - | access_token:string(JWT,15min-TTL); refresh_token:string(opaque,7d-TTL) | S | P0 |
| 7 | DEP-1 | Install jsonwebtoken npm package | Infra | - | package.json updated; lockfile committed; types available | S | P0 |
| 8 | DEP-2 | Install bcrypt npm package | Infra | - | package.json updated; native addon compiles; types available | S | P0 |
| 9 | OPS-001 | Generate RSA key pair for RS256 signing | Sec | - | 2048-bit+ RSA pair; private key PEM; public key PEM; keys not in repo | S | P0 |
| 10 | OPS-002 | Configure secrets manager for RSA key | Sec | OPS-001 | private key stored; access policy scoped to auth service; retrieval <50ms | M | P0 |
| 11 | OPS-003 | Implement feature flag AUTH_SERVICE_ENABLED | Infra | - | flag default:false; routes disabled when false; toggle without redeploy | S | P1 |

### Integration Points - Phase 0

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| 003-auth-tables migration | DB migration | Run via migration runner | Phase 0 | COMP-007, all repositories |
| RSA key pair | Secret | Loaded from secrets manager at startup | Phase 0 | COMP-003 (JwtService) |
| AUTH_SERVICE_ENABLED flag | Feature flag | Checked in route registration | Phase 2 | COMP-006 (AuthRoutes) |

## Phase 1: Core Security Components

**Objective:** Implement foundational security primitives (hashing, JWT, token management) as independently testable modules | **Duration:** 3-4 days | **Entry:** Phase 0 complete; RSA key retrievable | **Exit:** All three core components pass unit tests; token issue/verify/rotate cycle works in isolation

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 12 | COMP-004 | Implement PasswordHasher module | Auth | DEP-2 | hash(password)>bcrypt-string; compare(password,hash)>boolean; cost-factor:12; timing ~250ms; configurable cost | M | P0 |
| 13 | COMP-003 | Implement JwtService module | Auth | DEP-1, OPS-002 | sign(payload,ttl)>JWT-RS256; verify(token)>payload-or-throw; loads private key from secrets mgr; public key exposed for verification | M | P0 |
| 14 | COMP-002 | Implement TokenManager module | Auth | COMP-003, DM-002, DM-003 | issueTokenPair(userId)>AuthTokenPair; access:15min-TTL; refresh:7d-TTL; refresh hash stored in DB; rotateRefresh(token)>new-pair+revoke-old; replayDetect: revoked-token-reuse invalidates all user tokens | L | P0 |
| 15 | COMP-007 | Implement AuthMigration runner | DB | MIG-001, MIG-002, MIG-003 | up creates both tables; down drops both; idempotent; runs in CI pipeline | M | P0 |
| 16 | NFR-AUTH.3 | Verify bcrypt cost factor 12 compliance | Sec | COMP-004 | unit test asserts cost-factor:12; benchmark confirms ~250ms/hash; hash prefix $2b$12$ | S | P0 |
| 17 | TEST-001 | Write PasswordHasher unit tests | Test | COMP-004 | hash produces valid bcrypt; compare matches correct pw; compare rejects wrong pw; cost factor verified; timing within 200-400ms range | M | P0 |
| 18 | TEST-002 | Write JwtService unit tests | Test | COMP-003 | sign produces valid JWT; verify decodes payload; expired token throws; malformed token throws; RS256 algorithm enforced | M | P0 |
| 19 | TEST-003 | Write TokenManager unit tests | Test | COMP-002 | issue returns pair with correct TTLs; refresh rotates token; revoked token triggers full invalidation; expired refresh rejected; hash stored in DB | L | P0 |

### Integration Points - Phase 1

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| PasswordHasher | Injectable service | Constructor injection | Phase 1 | COMP-001 (AuthService) |
| JwtService | Injectable service | Constructor injection | Phase 1 | COMP-002 (TokenManager) |
| TokenManager | Injectable service | Constructor injection | Phase 1 | COMP-001 (AuthService) |
| COMP-007 migration runner | CLI/startup hook | Registered in migration pipeline | Phase 1 | DB startup sequence |

## Phase 2: Auth Service & API Layer

**Objective:** Build AuthService orchestrator, AuthMiddleware, route handlers, and all six API endpoints | **Duration:** 4-5 days | **Entry:** Phase 1 components passing unit tests | **Exit:** All FR acceptance criteria pass against running server; manual smoke test of login > profile > refresh > logout flow

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 20 | COMP-001 | Implement AuthService orchestrator | Auth | COMP-002, COMP-004, DM-001 | login(email,pw)>AuthTokenPair; register(data)>UserRecord; refresh(token)>AuthTokenPair; resetRequest(email)>void; resetConfirm(token,newPw)>void; getProfile(userId)>UserRecord(sanitized) | XL | P0 |
| 21 | COMP-005 | Implement AuthMiddleware | Auth | COMP-002 | extracts Bearer token from Authorization header; verifies via TokenManager; attaches userId to request context; returns 401 on missing/invalid/expired token | M | P0 |
| 22 | COMP-006 | Register AuthRoutes in route index | API | COMP-001, COMP-005, OPS-003 | mounts /auth/* group; gated by AUTH_SERVICE_ENABLED flag; applies rate limiter to login endpoint | M | P0 |
| 23 | API-001 | Implement POST /auth/login handler | API | COMP-001, COMP-006 | delegates to AuthService.login; returns 200+AuthTokenPair; sets refresh_token as httpOnly cookie | M | P0 |
| 24 | API-002 | Implement POST /auth/register handler | API | COMP-001, COMP-006 | delegates to AuthService.register; validates input; returns 201+user profile | M | P0 |
| 25 | API-003 | Implement POST /auth/refresh handler | API | COMP-001, COMP-006 | reads refresh_token from httpOnly cookie; delegates to AuthService.refresh; returns new pair | M | P0 |
| 26 | API-004 | Implement GET /auth/me handler | API | COMP-001, COMP-005, COMP-006 | requires AuthMiddleware; delegates to AuthService.getProfile; returns sanitized profile | S | P0 |
| 27 | API-005 | Implement POST /auth/reset-password handler | API | COMP-001, COMP-006 | accepts email; delegates to AuthService.resetRequest; always returns 200 (no email enumeration) | M | P1 |
| 28 | API-006 | Implement POST /auth/reset-password/confirm | API | COMP-001, COMP-006 | accepts reset token + new password; delegates to AuthService.resetConfirm; returns 200 on success | M | P1 |
| 29 | FR-AUTH.1 | Wire login flow end-to-end | Auth | API-001 | valid-creds>200+AuthToken; invalid>401; locked>403; 5fail/15min/IP>429; no-enum | M | P0 |
| 30 | FR-AUTH.2 | Wire registration flow end-to-end | Auth | API-002 | valid-data>201+profile; dup-email>409; pw-policy:8+chars,upper,lower,digit; email-format-validated | M | P0 |
| 31 | FR-AUTH.3 | Wire token refresh flow end-to-end | Auth | API-003 | valid-refresh>new-pair+rotation; expired>401; revoked>invalidate-all-user-tokens | M | P0 |
| 32 | FR-AUTH.4 | Wire profile retrieval end-to-end | Auth | API-004, COMP-005 | valid-bearer>profile(id,email,display_name,created_at); expired/invalid>401; password_hash+refresh_token_hash excluded | S | P0 |
| 33 | FR-AUTH.5 | Wire password reset flow end-to-end | Auth | API-005, API-006, DEP-3 | registered-email>reset-token(1h-TTL)+email-sent; valid-reset-token>new-pw-set+token-invalidated; expired/invalid>400; success>all-refresh-tokens-revoked | L | P1 |
| 34 | OPS-004 | Configure rate limiter for login endpoint | Sec | COMP-006 | 5 requests/min/IP; returns 429 on exceed; configurable thresholds; no rate limit on other auth endpoints | M | P0 |
| 35 | DEP-3 | Integrate email service for password reset | Infra | FR-AUTH.5 | email dispatched on reset request; template includes reset link with token; delivery confirmed or error logged | L | P1 |

### Integration Points - Phase 2

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| AuthService | Injectable service | Constructor injection with TokenManager + PasswordHasher | Phase 2 | API-001 through API-006 |
| AuthMiddleware | Middleware | Registered in Express/Koa middleware chain | Phase 2 | API-004 (GET /auth/me), future protected routes |
| AuthRoutes | Route registration | Mounted on app via route index | Phase 2 | Express/Koa app |
| Rate limiter | Middleware | Applied to POST /auth/login route specifically | Phase 2 | COMP-006 (AuthRoutes) |
| Email service | External callback | Called by AuthService.resetRequest | Phase 2 | FR-AUTH.5 |
| httpOnly cookie | Cookie config | Set by login/refresh handlers; read by refresh handler | Phase 2 | API-001, API-003 |

## Phase 3: Testing & Hardening

**Objective:** Achieve full test coverage across unit, integration, and E2E layers; validate NFRs; address identified gaps | **Duration:** 3-4 days | **Entry:** All FR flows passing manual smoke tests | **Exit:** All 22 success criteria validated; p95 latency < 200ms under load; security review passed

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 36 | TEST-004 | Write AuthService unit tests | Test | COMP-001 | login/register/refresh/reset paths tested; error cases covered; mocked dependencies; >90% branch coverage | L | P0 |
| 37 | TEST-005 | Write AuthMiddleware unit tests | Test | COMP-005 | valid token passes; missing header>401; malformed token>401; expired token>401; userId attached to req | M | P0 |
| 38 | TEST-006 | Write login integration tests | Test | FR-AUTH.1 | valid-creds>200+tokens; invalid>401-no-enum; locked>403; rate-limit>429-after-5th; tokens valid JWT | L | P0 |
| 39 | TEST-007 | Write registration integration tests | Test | FR-AUTH.2 | valid>201+profile; dup-email>409; weak-pw>400; bad-email>400; user persisted in DB | M | P0 |
| 40 | TEST-008 | Write token refresh integration tests | Test | FR-AUTH.3 | valid-refresh>new-pair; expired>401; replay-detection>all-tokens-revoked; old-refresh-invalidated | L | P0 |
| 41 | TEST-009 | Write E2E auth flow test | Test | FR-AUTH.1, FR-AUTH.2, FR-AUTH.3, FR-AUTH.4 | register>login>get-profile>refresh>get-profile-again; full lifecycle in single test; real DB | L | P0 |
| 42 | TEST-010 | Run k6 load tests for p95 latency | Test | NFR-AUTH.1 | login p95<200ms; register p95<200ms; refresh p95<200ms; profile p95<200ms; 100 concurrent users baseline | L | P0 |
| 43 | NFR-AUTH.1 | Validate auth endpoint response times | Ops | TEST-010 | p95<200ms under normal load; measured via k6; results documented; APM dashboard configured | M | P0 |
| 44 | NFR-AUTH.2 | Configure availability monitoring | Ops | COMP-006 | health check endpoint returns 200; PagerDuty alert on 3 consecutive failures; uptime target 99.9% documented | M | P1 |
| 45 | OPS-005 | Set up health check endpoint | Ops | COMP-006 | GET /health returns 200+status; checks DB connectivity; checks secrets manager access; response <100ms | S | P1 |
| 46 | OPS-006 | Configure audit logging for auth events | Ops | COMP-001 | login-success/fail; register; token-refresh; password-reset; structured JSON format; includes IP, userId, timestamp | M | P1 |
| 47 | OPS-007 | Implement account lockout policy | Sec | COMP-001, FR-AUTH.1 | lock after 10 failed attempts; time-based unlock (30min); admin unlock API; lockout event logged; is_locked flag set on UserRecord | L | P2 |

### Integration Points - Phase 3

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| k6 test scripts | Test harness | CI pipeline stage | Phase 3 | NFR-AUTH.1 validation |
| Health check endpoint | HTTP route | Mounted on /health | Phase 3 | NFR-AUTH.2 monitoring, load balancer |
| PagerDuty integration | Alerting webhook | Configured in monitoring infra | Phase 3 | NFR-AUTH.2 |
| Audit logger | Middleware/decorator | Injected into AuthService methods | Phase 3 | OPS-006, compliance |

## Phase 4: Deployment & Rollout

**Objective:** Enable feature flag, perform canary rollout, validate production success criteria, establish key rotation schedule | **Duration:** 2-3 days | **Entry:** All Phase 3 tests green; security review complete | **Exit:** AUTH_SERVICE_ENABLED=true in production; all 22 success criteria verified; runbook documented

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 48 | OPS-008 | Write deployment runbook | Docs | All prior phases | migration steps; secrets setup; flag toggle; rollback procedure; smoke test checklist | M | P0 |
| 49 | OPS-009 | Execute canary deployment (10% traffic) | Ops | OPS-008 | flag enabled for canary; error rate <0.1%; latency within NFR bounds; no 5xx spike | M | P0 |
| 50 | OPS-010 | Validate all success criteria in prod | Ops | OPS-009 | SC-1 through SC-22 verified; evidence documented; sign-off obtained | L | P0 |
| 51 | OPS-011 | Full rollout (100% traffic) | Ops | OPS-010 | AUTH_SERVICE_ENABLED=true globally; monitoring stable 24h; no rollback triggered | S | P0 |
| 52 | OPS-012 | Schedule RSA key rotation (90-day cycle) | Sec | OPS-002 | rotation runbook; automated reminder; dual-key overlap window; zero-downtime rotation tested | M | P1 |

### Integration Points - Phase 4

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| Feature flag toggle | Config/deployment | Flipped via deployment pipeline | Phase 4 | COMP-006 (AuthRoutes) |
| Canary routing | Infrastructure | Traffic splitting at load balancer | Phase 4 | OPS-009 |
| Key rotation cron | Scheduled job | Secrets manager + key re-signing | Phase 4 | OPS-012, COMP-003 |

## Risk Assessment and Mitigation

| # | Risk | Severity | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|---|---|
| R-1 | JWT private key compromise allows forged tokens | High | Low | High | RS256 asymmetric keys; private key in secrets manager; 90-day rotation; key-pair audit trail | Security lead |
| R-2 | Refresh token replay attack after token theft | High | Medium | High | Token rotation with replay detection; reuse triggers full session invalidation; short access TTL (15min) | Backend lead |
| R-3 | bcrypt cost factor insufficient for future hardware | Medium | Low | Medium | Configurable cost factor; annual OWASP review; migration path to Argon2id documented | Security lead |
| R-4 | Email service outage blocks password reset flow | Medium | Medium | Medium | Async dispatch via queue (pending OQ-1); retry with exponential backoff; user-facing error message on timeout | Backend lead |
| R-5 | Rate limiter bypass via distributed IPs | Medium | Low | Medium | IP-based rate limit as first layer; add user-based rate limit for authenticated endpoints; WAF integration for distributed attack | DevOps lead |
| R-6 | Migration rollback data loss on partial failure | Medium | Low | High | Down-migration tested in CI; migration wrapped in transaction; backup before deploy; canary validates before full rollout | DBA/Backend lead |

## Resource Requirements and Dependencies

### External Dependencies

| Dependency | Required By Phase | Status | Fallback |
|---|---|---|---|
| jsonwebtoken (npm) | Phase 1 | Available; stable | jose library as alternative |
| bcrypt (npm) | Phase 1 | Available; native addon | bcryptjs (pure JS, slower) |
| Email service (SMTP/SES) | Phase 2 | Pending integration | Log-only mode for dev/staging |
| Database (PostgreSQL assumed) | Phase 0 | Required | No fallback; hard dependency |
| Secrets manager (Vault/AWS SM) | Phase 0 | Required | Environment variables (dev only; not for production) |
| k6 (load testing) | Phase 3 | Available | Artillery as alternative |
| PagerDuty (alerting) | Phase 3 | Pending setup | Email alerts as interim |

### Infrastructure Requirements

- PostgreSQL database with migration runner support (existing or new instance)
- Secrets manager with IAM-scoped access policies (Vault, AWS Secrets Manager, or GCP Secret Manager)
- Load balancer supporting canary traffic splitting for phased rollout
- APM integration for p95 latency monitoring (DataDog, New Relic, or Grafana/Prometheus)
- CI pipeline with migration execution, test stages, and k6 load test runner

## Success Criteria and Validation Approach

| Criterion | Metric | Target | Validation Method | Phase |
|---|---|---|---|---|
| SC-1 | Login returns tokens | 200 + access_token(15min) + refresh_token(7d) | Integration test | 2 |
| SC-2 | Invalid creds no enumeration | 401 with generic message | Integration test | 2 |
| SC-3 | Locked account blocked | 403 on locked user login | Integration test | 2 |
| SC-4 | Login rate limited | <=5 attempts/min/IP | Integration test + k6 | 2,3 |
| SC-5 | Registration success | 201 + user profile | Integration test | 2 |
| SC-6 | Duplicate email rejected | 409 on existing email | Integration test | 2 |
| SC-7 | Password policy enforced | 8+ chars, upper, lower, digit | Unit + integration test | 2 |
| SC-8 | Email format validated | Invalid email rejected before DB | Unit test | 2 |
| SC-9 | Token refresh rotates pair | New access + refresh; old revoked | Integration test | 2 |
| SC-10 | Expired refresh rejected | 401 on expired refresh token | Integration test | 2 |
| SC-11 | Replay detection works | Revoked token reuse invalidates all | Integration test | 2,3 |
| SC-12 | Refresh hash persisted | token_hash in refresh_tokens table | Unit test | 1 |
| SC-13 | Profile returns correct fields | id, email, display_name, created_at | Integration test | 2 |
| SC-14 | Expired token on profile | 401 on expired/invalid bearer | Integration test | 2 |
| SC-15 | Sensitive fields excluded | No password_hash or token_hash in response | Integration test | 2 |
| SC-16 | Reset token dispatched | Token generated (1h TTL) + email sent | Integration test (mock email) | 2 |
| SC-17 | Reset token consumed | New password set; token single-use | Integration test | 2 |
| SC-18 | Expired reset rejected | 400 on expired/invalid reset token | Integration test | 2 |
| SC-19 | Reset revokes sessions | All refresh tokens invalidated | Integration test | 2 |
| SC-20 | Auth p95 latency | < 200ms | k6 load test | 3 |
| SC-21 | Service uptime | >= 99.9% | Monitoring + health checks | 4 |
| SC-22 | bcrypt cost factor | Factor 12 (~250ms) | Unit test + benchmark | 1 |

## Timeline Estimates

| Phase | Duration | Start | End | Key Milestones |
|---|---|---|---|---|
| Phase 0 | 2-3 days | Week 1 Day 1 | Week 1 Day 3 | DB migrated; RSA keys provisioned; feature flag ready |
| Phase 1 | 3-4 days | Week 1 Day 3 | Week 2 Day 2 | PasswordHasher + JwtService + TokenManager passing unit tests |
| Phase 2 | 4-5 days | Week 2 Day 2 | Week 3 Day 2 | All 6 endpoints operational; FR acceptance criteria passing |
| Phase 3 | 3-4 days | Week 3 Day 2 | Week 4 Day 1 | Full test suite green; p95 < 200ms; security review signed off |
| Phase 4 | 2-3 days | Week 4 Day 1 | Week 4 Day 3 | Canary validated; full rollout; SC-1 through SC-22 confirmed |

**Total estimated duration:** 14-19 working days (3-4 weeks)

## Open Questions

| # | Question | Impact | Blocking Phase | Resolution Owner |
|---|---|---|---|---|
| OQ-1 | Sync vs queue for password reset emails? | Latency budget for reset endpoint; error handling; resilience under load | Phase 2 (FR-AUTH.5) | Architect + Backend lead |
| OQ-2 | Max active refresh tokens per user? | DB storage; multi-device support; eviction strategy | Phase 1 (COMP-002) | Product + Architect |
| OQ-3 | Progressive lockout policy (threshold, unlock mechanism)? | GAP-1 mitigation; UX vs security tradeoff; admin tooling scope | Phase 3 (OPS-007) | Product + Security lead |
| OQ-4 | Audit logging format and destination? | Compliance readiness; infra requirements; structured logging pipeline | Phase 3 (OPS-006) | Security + DevOps |
| OQ-5 | Revoke tokens on user deletion? | Data integrity; deletion flow complexity; token validation logic | Phase 2 (COMP-002) | Architect + Backend lead |
| OQ-6 | Exact REST paths for register, refresh, reset? | Route implementation; API documentation; client integration | Phase 0 (blocking) | API design lead |
