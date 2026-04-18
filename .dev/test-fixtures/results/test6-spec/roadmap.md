---
spec_source: "test-spec-user-auth.md"
complexity_score: 0.6
complexity_class: MEDIUM
primary_persona: architect
adversarial: true
base_variant: "roadmap-haiku-architect"
variant_scores: "A:71 B:76"
convergence_score: 0.62
debate_rounds: 2
generated: "2026-04-15"
generator: "adversarial-merge"
total_phases: 4
total_task_rows: 58
risk_count: 6
open_questions: 6
---

# User Authentication Service — Project Roadmap

## Executive Summary

This roadmap defines the implementation plan for a JWT-based user authentication service covering login, registration, token refresh, profile retrieval, and password reset. The system uses RS256 asymmetric JWT signing, bcrypt password hashing (cost factor 12), and refresh token rotation with replay detection. The architecture follows a layered pattern (SecretsProvider > JwtService > TokenManager > AuthService > AuthMiddleware > AuthRoutes) with explicit dependency injection boundaries for each security-sensitive component.

The plan is organized in four phases: security and data foundation, core authentication flows, API exposure and verification, and hardening with production rollout. Crypto primitives are tested in Phase 1 immediately after implementation; auth service unit tests follow in Phase 3 alongside route integration tests. Deployment uses five granular tasks (runbook, 10% canary, SC validation, full rollout, key rotation) to eliminate hand-waving in the rollout sequence.

**Business Impact:** Authentication is a gating capability — no user-facing feature can ship without it. Delays cascade to every downstream service requiring identity verification. Shipping without self-service password recovery creates immediate support burden and user trust risk.

**Complexity:** MEDIUM (0.6) — Security sensitivity is high (replay detection, token rotation, RS256 key management), but the component set is bounded and the implementation order is well constrained by the dependency chain.

**Critical path:** OPS-001/COMP-012/COMP-007 → COMP-003/COMP-004 → TEST-001 → COMP-009/COMP-002 → COMP-001 → COMP-005/COMP-006/API-001..006 → TEST-003 → NFR validation → OPS-008..011

**Key architectural decisions:**

- RS256 asymmetric signing with private key material in secrets manager (SecretsProvider) enables key rotation without service restart and supports multi-service token verification via public key distribution
- Stateless JWT access tokens (15min TTL, no server-side session store) for horizontal scalability; revocation handled through short TTL plus refresh token DB check via RefreshTokenRepository
- Refresh token rotation with replay detection: reuse of a rotated token invalidates ALL user sessions via global revoke, trading single-device UX for security posture
- Explicit components for security-sensitive boundaries (SecretsProvider, AuthCookiePolicy, AuthConfig) to catch common production failure modes at boot rather than at first request

**Open risks requiring resolution before Phase 1:**

- OQ-6: REST paths for registration, refresh, and reset endpoints must be finalized before route contracts are frozen
- OQ-1: Email dispatch strategy (sync vs queue) affects password reset endpoint latency budget and error handling design
- OQ-2: Maximum active refresh tokens per user must be defined before repository eviction and replay-handling policy are finalized

## Phase 1: Security and Data Foundation

**Phase 1** | milestone: schema+crypto ready, primitive tests pass | duration: 4-5d | exit criteria: keys provisioned; migration rollback verified; repositories and crypto primitives implemented and tested

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | OPS-001 | Provision auth secrets and env | Ops | — | RS256-keypair:stored; AUTH_SERVICE_ENABLED:set; cookie+TTL env:set; env-parity:dev+prod | M | P0 |
| 2 | COMP-012 | Define secrets provider | Sec | OPS-001 | name:SecretsProvider; path:src/auth/secrets-provider.ts; role:load RS256 keys+auth env; deps:SecretsMgr+env | M | P0 |
| 3 | DEP-1 | Install jsonwebtoken package | Infra | — | package.json:updated; lockfile:committed; types:available | S | P0 |
| 4 | DEP-2 | Install bcrypt package | Infra | — | package.json:updated; native addon:compiles; types:available | S | P0 |
| 5 | COMP-007 | Build auth table migration | DB | OPS-001 | name:AuthMigration; path:src/database/migrations/003-auth-tables.ts; role:add users+refresh_tokens; deps:Database | M | P0 |
| 6 | MIG-001 | Apply auth schema migration | DB | COMP-007 | users+refresh_tokens:created; idx+FK:valid; up:idempotent; deploy-doc:ready | M | P0 |
| 7 | MIG-002 | Verify migration rollback path | DB | MIG-001 | down-script:present; rollback:clean; reapply:pass; orphan-schema:none | M | P0 |
| 8 | MIG-003 | Write idempotent down-migration | DB | MIG-001,MIG-002 | down drops refresh_tokens then users; idempotent; tested in clean DB | S | P0 |
| 9 | DM-001 | Model user record schema | DB | MIG-001 | id:uuid-v4; email:string+unique+idx; display_name:string; password_hash:bcrypt; is_locked:boolean; created_at:Date; updated_at:Date | M | P0 |
| 10 | DM-002 | Model refresh token schema | DB | MIG-001 | id:uuid-v4; user_id:FK->UserRecord.id; token_hash:SHA-256; expires_at:Date; revoked:boolean; created_at:Date | M | P0 |
| 11 | DM-003 | Define auth token pair DTO | Auth | — | access_token:JWT-RS256-15m-TTL; refresh_token:opaque-7d-TTL | S | P1 |
| 12 | COMP-008 | Implement user repository | DB | DM-001 | name:UserRepository; path:src/auth/user-repository.ts; role:user CRUD+lookup by email/id; deps:DM-001+Database | M | P0 |
| 13 | COMP-009 | Implement refresh token repo | DB | DM-002 | name:RefreshTokenRepository; path:src/auth/refresh-token-repository.ts; role:store+rotate+revoke token hashes; deps:DM-002+Database | M | P0 |
| 14 | COMP-003 | Implement RS256 JWT service | Sec | COMP-012,DEP-1 | name:JwtService; path:src/auth/jwt-service.ts; role:RS256 sign+verify JWT; deps:jsonwebtoken+RSA key pair | M | P0 |
| 15 | COMP-004 | Implement bcrypt hasher | Sec | DEP-2 | name:PasswordHasher; path:src/auth/password-hasher.ts; role:hash+compare with cost config; deps:bcrypt; cost-factor:12 | M | P0 |
| 16 | TEST-001 | Add crypto primitive tests | Test | COMP-003,COMP-004 | rs256 sign/verify:pass; tamper→reject; bcrypt cost12:pass; compare:pass; timing:200-400ms; hash prefix:$2b$12$ | M | P0 |

### Integration Points — Phase 1

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| SecretsProvider | DI/config | secrets manager + env → JwtService | 1 | COMP-003, COMP-013 |
| 003-auth-tables | migration runner | DB migrator → users/refresh_tokens schema | 1 | MIG-001, MIG-002, COMP-008, COMP-009 |
| UserRepository | DI | DB pool → user lookup/write methods | 1 | COMP-001, FR-AUTH.1, FR-AUTH.2, FR-AUTH.4 |
| RefreshTokenRepository | DI | DB pool → token hash persistence | 1 | COMP-002, FR-AUTH.3 |
| JwtService | strategy | RS256 signer/verifier → TokenManager | 1 | COMP-002, COMP-005 |
| PasswordHasher | strategy | bcrypt cost policy → AuthService | 1 | COMP-001, FR-AUTH.1, FR-AUTH.2, FR-AUTH.5 |
| RSA key pair | secret | loaded from secrets manager at startup | 1 | COMP-003 (JwtService) |

## Phase 2: Core Authentication Flows

**Phase 2** | milestone: domain flows implemented | duration: 5-6d | exit criteria: login/register/refresh/reset services pass unit tests; endpoint contracts frozen

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 17 | COMP-002 | Implement token manager | Auth | COMP-003,COMP-009,DM-003 | name:TokenManager; path:src/auth/token-manager.ts; role:issue+refresh+revoke token pairs; deps:JwtService+RefreshTokenRepository; issueTokenPair(userId)→AuthTokenPair; access:15min-TTL; refresh:7d-TTL; refresh hash stored in DB; rotateRefresh(token)→new-pair+revoke-old; replayDetect:revoked-token-reuse invalidates all user tokens | L | P0 |
| 18 | COMP-001 | Implement auth service | Auth | COMP-002,COMP-004,COMP-008 | name:AuthService; path:src/auth/auth-service.ts; role:login+register+refresh+reset orchestration; deps:TokenManager+PasswordHasher+UserRepository; login(email,pw)→AuthTokenPair; register(data)→UserRecord; refresh(token)→AuthTokenPair; resetRequest(email)→void; resetConfirm(token,newPw)→void; getProfile(userId)→UserRecord(sanitized) | L | P0 |
| 19 | COMP-010 | Implement auth rate limiter | Sec | COMP-001 | name:AuthRateLimiter; path:src/auth/auth-rate-limiter.ts; role:cap login attempts per IP; 5req/min/IP; 429 on exceed; configurable thresholds | M | P0 |
| 20 | COMP-011 | Implement reset email adapter | Auth | OPS-001 | name:ResetEmailAdapter; path:src/auth/reset-email-adapter.ts; role:compose+dispatch reset email; deps:Email service+reset URL config | M | P1 |
| 21 | DEP-3 | Integrate email service | Infra | COMP-011 | email dispatched on reset request; template includes reset link with token; delivery confirmed or error logged | L | P1 |
| 22 | FR-AUTH.2 | Deliver user registration flow | Auth | COMP-001,COMP-004,COMP-008 | valid→201+profile; dup-email→409; pwd:min8+upper+lower+digit; email:format-valid | L | P0 |
| 23 | API-002 | Freeze register route contract | API | FR-AUTH.2 | POST:/auth/register; body:email+password+display_name; 201:user-profile; 409:dup-email | S | P0 |
| 24 | FR-AUTH.1 | Deliver user login flow | Auth | COMP-001,COMP-002,COMP-010 | valid→200+access15m+refresh7d; invalid→401+no-enum; locked→403; limit:5/min/IP | L | P0 |
| 25 | API-001 | Freeze login route contract | API | FR-AUTH.1 | POST:/auth/login; body:email+password; 200:access+refresh; 401/403:spec-compliant | S | P0 |
| 26 | FR-AUTH.3 | Deliver token refresh flow | Auth | COMP-002,COMP-009 | valid-refresh→200+rotated pair; expired→401; replay→global revoke; token-hash:persisted | L | P0 |
| 27 | API-003 | Freeze refresh route contract | API | FR-AUTH.3 | POST:/auth/refresh; input:refresh cookie; 200:new pair; 401:expired+revoked | S | P0 |
| 28 | FR-AUTH.5 | Deliver password reset flow | Auth | COMP-001,COMP-004,COMP-011,COMP-009 | registered-email→reset1h+email; valid token→pwd changed+token invalidated; bad token→400; reset→revoke all sessions | XL | P0 |
| 29 | API-005 | Freeze reset request contract | API | FR-AUTH.5 | POST:/auth/reset-password; body:email; always:200(no enumeration); token:1h-TTL; dispatch:email-service | S | P1 |
| 30 | API-006 | Freeze reset confirm contract | API | FR-AUTH.5 | POST:/auth/reset-password/confirm; body:token+password; success:pwd-reset+token-spent; invalid/expired→400 | S | P1 |

### Integration Points — Phase 2

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| TokenManager | strategy chain | JwtService + RefreshTokenRepository + TTL policy | 2 | COMP-001, FR-AUTH.1, FR-AUTH.3, FR-AUTH.5 |
| AuthService | orchestration | UserRepository + PasswordHasher + TokenManager | 2 | API-001 through API-006 |
| AuthRateLimiter | middleware/callback | request IP key → login guard | 2 | FR-AUTH.1, API-001, COMP-006 |
| ResetEmailAdapter | external adapter | reset token payload → Email service | 2 | FR-AUTH.5, API-005 |
| API contracts | route registry | method/path → AuthService handlers | 2 | COMP-006 |
| Email service | external callback | called by ResetEmailAdapter | 2 | FR-AUTH.5 |

## Phase 3: API Exposure and Verification

**Phase 3** | milestone: protected API exposed, test suites pass | duration: 4-5d | exit criteria: middleware/routes live behind flag; profile flow works; unit+integration suites pass; auth config validated at boot

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 31 | COMP-013 | Implement auth config validator | Auth | OPS-001,COMP-012 | name:AuthConfig; path:src/auth/auth-config.ts; role:validate TTLs+cookie flags+key presence at boot; deps:env+SecretsProvider; fail-fast on missing RSA key or invalid TTL | M | P0 |
| 32 | COMP-014 | Implement route feature gate | Gate | OPS-001 | name:AuthFeatureGate; path:src/auth/auth-feature-gate.ts; role:toggle auth routes by AUTH_SERVICE_ENABLED; deps:env+router | S | P0 |
| 33 | COMP-015 | Implement cookie and CORS policy | Sec | COMP-013 | name:AuthCookiePolicy; path:src/auth/auth-cookie-policy.ts; role:httpOnly refresh cookie+CORS config; attrs:httpOnly+Secure+SameSite+Path+Domain; deps:auth env+routes | M | P0 |
| 34 | COMP-005 | Implement auth middleware | API | COMP-002,COMP-013 | name:AuthMiddleware; path:src/middleware/auth-middleware.ts; role:extract+verify Bearer token; attach userId to request context; 401 on missing/invalid/expired | M | P0 |
| 35 | FR-AUTH.4 | Deliver profile retrieval | API | COMP-001,COMP-005,COMP-008 | valid bearer→200+id+email+display_name+created_at; invalid/expired→401; sensitive:excluded(password_hash,token_hash) | M | P0 |
| 36 | API-004 | Freeze profile route contract | API | FR-AUTH.4 | GET:/auth/me; Bearer:required; 200:profile; 401:invalid+expired | S | P0 |
| 37 | COMP-006 | Register auth route group | API | COMP-001,COMP-005,COMP-014,COMP-015,API-001..006 | name:AuthRoutes; path:src/routes/index.ts; role:register /auth/* route group; gated by AUTH_SERVICE_ENABLED; applies rate limiter to login | L | P0 |
| 38 | TEST-002 | Add auth service unit tests | Test | COMP-001,COMP-002,COMP-010,COMP-011 | login/register/refresh/reset:pass; dup-email→409; locked→403; replay→global revoke; >90% branch coverage; mocked dependencies | L | P0 |
| 39 | TEST-003 | Add route integration tests | Test | COMP-006,API-001..006 | status codes:match; cookie+Bearer flows:pass; flag-off→disabled; sensitive fields:excluded; middleware:verified | L | P0 |
| 40 | TEST-006 | Write login integration tests | Test | FR-AUTH.1,COMP-006 | valid-creds→200+tokens; invalid→401-no-enum; locked→403; rate-limit→429-after-5th; tokens valid JWT-RS256 | L | P0 |
| 41 | TEST-007 | Write registration integration tests | Test | FR-AUTH.2,COMP-006 | valid→201+profile; dup-email→409; weak-pw→400; bad-email→400; user persisted in DB | M | P0 |
| 42 | TEST-008 | Write token refresh integration tests | Test | FR-AUTH.3,COMP-006 | valid-refresh→new-pair; expired→401; replay-detection→all-tokens-revoked; old-refresh-invalidated | L | P0 |

### Integration Points — Phase 3

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| AuthConfig | config/DI | env validation → service boot fail-fast | 3 | COMP-001, COMP-002, COMP-003, COMP-015 |
| AuthFeatureGate | feature flag | AUTH_SERVICE_ENABLED → route registry | 3 | COMP-006, OPS-008 |
| AuthCookiePolicy | middleware/config | cookie attrs + CORS headers → auth responses | 3 | API-001, API-003, API-005, API-006 |
| AuthMiddleware | middleware chain | Bearer extraction + TokenManager verify → request context | 3 | FR-AUTH.4, API-004, future protected routes |
| AuthRoutes | route registry | handlers + middleware + gate → /auth/* exposure | 3 | clients, TEST-003, TEST-006..008 |
| Integration suite | test harness | app boot + DB fixtures + HTTP assertions | 3 | TEST-003, TEST-006, TEST-007, TEST-008, NFR-AUTH.1 |

## Phase 4: Hardening, Operations, and Release

**Phase 4** | milestone: production readiness proven | duration: 4-5d | exit criteria: NFRs validated; alerts and rollout controls active; canary+full rollout complete; SC-1..22 verified in prod

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 43 | NFR-AUTH.1 | Validate auth latency budget | Gate | TEST-003,COMP-015 | p95:<200ms; tool:k6; env:prod-like; regressions:none | L | P0 |
| 44 | NFR-AUTH.2 | Validate auth availability | Ops | COMP-006 | uptime:>=99.9%; healthcheck:monitored; PagerDuty:alerting; SLO:published | M | P0 |
| 45 | NFR-AUTH.3 | Validate hashing security target | Sec | COMP-004,TEST-001 | bcrypt-cost:12; hash-time:~250ms; unit-test:pass; benchmark:pass | M | P0 |
| 46 | OPS-002 | Add health and uptime checks | Ops | COMP-006 | health-endpoint:GET /health returns 200+status; checks DB+secrets access; uptime-monitor:on; alert route:PagerDuty; runbook:linked; response:<100ms | M | P0 |
| 47 | OPS-003 | Add auth security observability | Ops | COMP-006,COMP-010 | auth events:logged(login-success/fail,register,refresh,reset); replay alerts:on; failed-login metrics:on; PII:redacted; structured JSON format; includes IP+userId+timestamp | M | P1 |
| 48 | OPS-004 | Define key rotation procedure | Sec | COMP-012,COMP-003 | rotation:90d; dual-key overlap:documented; rollback:defined; ownership:assigned | M | P1 |
| 49 | OPS-007 | Implement account lockout policy | Sec | COMP-001,FR-AUTH.1 | lock after threshold(pending OQ-3); time-based unlock; admin unlock API; lockout event logged; is_locked flag set on UserRecord; requires product+security sign-off | L | P2 |
| 50 | OPS-008 | Write deployment runbook | Docs | All prior phases | migration steps; secrets setup; flag toggle; rollback procedure; smoke test checklist; canary criteria | M | P0 |
| 51 | OPS-009 | Execute canary deployment (10%) | Ops | OPS-008,NFR-AUTH.1,NFR-AUTH.2 | flag enabled for 10% canary; error rate <0.1%; latency within NFR bounds; no 5xx spike; monitor 4h minimum | M | P0 |
| 52 | OPS-010 | Validate all SC in production | Ops | OPS-009 | SC-1 through SC-22 verified in canary; evidence documented; sign-off obtained | L | P0 |
| 53 | OPS-011 | Full rollout (100% traffic) | Ops | OPS-010 | AUTH_SERVICE_ENABLED:true globally; monitoring stable 24h; no rollback triggered | S | P0 |
| 54 | OPS-012 | Schedule RSA key rotation cycle | Sec | OPS-004 | rotation runbook:complete; automated 90d reminder; dual-key overlap window defined; zero-downtime rotation tested | M | P1 |
| 55 | TEST-004 | Run end-to-end auth scenario | Test | COMP-006,OPS-008 | register→login→me→refresh→reset:pass; cookie flow:pass; replay defense:pass; full lifecycle in single test; real DB | L | P0 |
| 56 | TEST-005 | Run migration and recovery drills | Test | MIG-001,MIG-002,MIG-003 | backup-restore:pass; down+up:pass; rollback under flag-off:pass; reapply:clean | M | P1 |
| 57 | TEST-010 | Run k6 load tests | Test | NFR-AUTH.1,COMP-006 | login p95<200ms; register p95<200ms; refresh p95<200ms; profile p95<200ms; 100 concurrent users baseline; results documented | L | P0 |
| 58 | DOC-001 | Publish auth architecture notes | Docs | COMP-006,NFR-AUTH.2,OPS-004 | diagrams:updated; endpoint contracts:frozen; rollback+ops:documented; owners:named; key rotation:documented | M | P1 |

### Integration Points — Phase 4

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| Feature flag toggle | config/deployment | flipped via deployment pipeline | 4 | COMP-006 (AuthRoutes), OPS-009 |
| Canary routing | infrastructure | traffic splitting at load balancer | 4 | OPS-009 |
| Health check endpoint | HTTP route | mounted on /health | 4 | NFR-AUTH.2, load balancer |
| PagerDuty integration | alerting webhook | configured in monitoring infra | 4 | NFR-AUTH.2 |
| Audit logger | middleware/decorator | injected into AuthService methods | 4 | OPS-003, compliance |
| Key rotation cron | scheduled job | secrets manager + key re-signing | 4 | OPS-012, COMP-003 |
| k6 test scripts | test harness | CI pipeline stage | 4 | NFR-AUTH.1, TEST-010 |
| Deployment runbook | documentation | reviewed before rollout execution | 4 | OPS-009, OPS-010, OPS-011 |

## Risk Assessment and Mitigation

| # | Risk | Severity | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|---|---|
| R-1 | Private key exposure for RS256 signer allows forged tokens | High | Low | High | Secrets manager with least-privilege access; SecretsProvider abstraction; 90d rotation via OPS-012; dual-key overlap window; rollout drill in TEST-005 | Security |
| R-2 | Refresh-token replay after theft enables account takeover | High | Medium | High | Token rotation on every refresh; hashed persistence via RefreshTokenRepository; replay-triggered global revoke; short access TTL (15min) | Backend |
| R-3 | bcrypt cost factor insufficient for future hardware | Medium | Low | Medium | Configurable cost factor in PasswordHasher; annual OWASP review; benchmark in NFR-AUTH.3; migration path to Argon2id documented | Security |
| R-4 | Email provider latency stalls password reset flow | Medium | Medium | Medium | Decide sync vs queue before Phase 2 (OQ-1); timeout budget in ResetEmailAdapter; retry with exponential backoff; dead-letter policy | Backend |
| R-5 | Undefined max active refresh tokens causes repo growth | Medium | Medium | Medium | Resolve token cap in OQ-2 before Phase 2; add eviction policy in RefreshTokenRepository; monitor table size | Architect |
| R-6 | Feature flag rollback path untested in production | High | Low | High | Dark launch via AuthFeatureGate; canary rollout (OPS-009); rollback drill in TEST-005; schema retained on flag-off; rollback <5min target | Ops |

## Resource Requirements and Dependencies

### External Dependencies

| Dependency | Required By Phase | Status | Fallback |
|---|---|---|---|
| jsonwebtoken (npm) | 1 | Required; stable | jose library as alternative |
| bcrypt (npm) | 1 | Required; native addon | bcryptjs (pure JS, slower) |
| Database (PostgreSQL) | 1 | Required | No fallback; migration gate blocks rollout |
| Secrets manager (Vault/AWS SM) | 1 | Required | Env-file for local dev only; never prod |
| Email service (SMTP/SES) | 2 | Pending integration | Queue-backed adapter or noop in non-prod |
| k6 (load testing) | 4 | Required | Equivalent load harness if org-standard differs |
| PagerDuty (alerting) | 4 | Pending setup | Temporary alert sink before production cut |

### Infrastructure Requirements

- RSA key-pair generation and secure private-key storage per environment (SecretsProvider)
- PostgreSQL database with migration runner support for `users` and `refresh_tokens` tables, including unique email index and token-hash lookups
- Rate-limit backing store sized for 5/min/IP enforcement on login (AuthRateLimiter)
- HTTPS termination, cookie security flags (httpOnly, Secure, SameSite), and CORS policy aligned to refresh-cookie transport (AuthCookiePolicy)
- Load balancer supporting canary traffic splitting for phased rollout (OPS-009)
- APM integration for p95 latency monitoring (DataDog, New Relic, or Grafana/Prometheus)
- CI pipeline with migration execution, test stages, and k6 load test runner
- Production-like staging environment for latency, replay, rollback, and failover validation

## Success Criteria and Validation Approach

| Criterion | Metric | Target | Validation Method | Phase |
|---|---|---|---|---|
| SC-1 | Login returns tokens | 200 + access_token(15min) + refresh_token(7d) | TEST-003, TEST-006, TEST-004 | 3-4 |
| SC-2 | Invalid creds no enumeration | 401 with generic message | TEST-002, TEST-006 | 3 |
| SC-3 | Locked account blocked | 403 on locked user login | TEST-002, TEST-006 | 3 |
| SC-4 | Login rate limited | <=5 attempts/min/IP | TEST-006, OPS-003 | 3-4 |
| SC-5 | Registration success | 201 + user profile | TEST-002, TEST-007 | 3 |
| SC-6 | Duplicate email rejected | 409 on existing email | TEST-002, TEST-007 | 3 |
| SC-7 | Password policy enforced | 8+ chars, upper, lower, digit | TEST-002, TEST-007 | 3 |
| SC-8 | Email format validated | Invalid email rejected before DB | TEST-002, TEST-007 | 3 |
| SC-9 | Token refresh rotates pair | New access + refresh; old revoked | TEST-002, TEST-008, TEST-004 | 3-4 |
| SC-10 | Expired refresh rejected | 401 on expired refresh token | TEST-002, TEST-008 | 3 |
| SC-11 | Replay detection works | Revoked token reuse invalidates all | TEST-002, TEST-008, TEST-004 | 3-4 |
| SC-12 | Refresh hash persisted | token_hash in refresh_tokens table | TEST-003 (DB assertion) | 3 |
| SC-13 | Profile returns correct fields | id, email, display_name, created_at | TEST-003, TEST-004 | 3-4 |
| SC-14 | Expired token on profile | 401 on expired/invalid bearer | TEST-003 | 3 |
| SC-15 | Sensitive fields excluded | No password_hash or token_hash in response | TEST-003 | 3 |
| SC-16 | Reset token dispatched | Token generated (1h TTL) + email sent | TEST-002 (provider stub) | 3 |
| SC-17 | Reset token consumed | New password set; token single-use | TEST-002, TEST-004 | 3-4 |
| SC-18 | Expired reset rejected | 400 on expired/invalid reset token | TEST-002, TEST-003 | 3 |
| SC-19 | Reset revokes sessions | All refresh tokens invalidated | TEST-002, TEST-004 | 3-4 |
| SC-20 | Auth p95 latency | < 200ms | k6 load test (TEST-010) | 4 |
| SC-21 | Service uptime | >= 99.9% | Health monitoring + PagerDuty (OPS-002) | 4 |
| SC-22 | bcrypt cost factor | Factor 12 (~250ms) | TEST-001 + NFR-AUTH.3 benchmark | 1,4 |

## Timeline Estimates

| Phase | Duration | Start | End | Key Milestones |
|---|---|---|---|---|
| 1 | 4-5d | Day 1 | Day 5 | RSA keys provisioned; migration up/down verified; crypto primitives tested (TEST-001) |
| 2 | 5-6d | Day 6 | Day 11 | AuthService + TokenManager complete; login/register/refresh/reset contracts frozen |
| 3 | 4-5d | Day 12 | Day 16 | Middleware/routes live behind flag; profile endpoint operational; unit+integration suites pass |
| 4 | 4-5d | Day 17 | Day 21 | SLO evidence complete; canary validated; full rollout; SC-1..22 verified; ops docs published |

**Total estimated duration:** 17-21 working days

## Open Questions

| # | Question | Impact | Blocking Phase | Resolution Owner |
|---|---|---|---|---|
| OQ-1 | Should reset email send inline or via queue? | Determines reset latency path, retry design, and ResetEmailAdapter implementation | 2 | Architect + Backend |
| OQ-2 | Maximum active refresh tokens per user? | Shapes RefreshTokenRepository eviction, multi-device support, and replay blast radius | 2 | Architect + Product |
| OQ-3 | Progressive lockout policy after repeated failures? | Needed to close R-5 beyond per-IP rate limit; determines OPS-007 thresholds | 4 | Product + Security |
| OQ-4 | Audit logging schema and sink for auth events? | Required for OPS-003 implementation and compliance maturity | 4 | Ops + Security |
| OQ-5 | Revoke all tokens on user deletion? | Affects deletion semantics, residual access risk, and TokenManager logic | 2 | Architect + Backend |
| OQ-6 | Confirm final REST paths for register/refresh/reset? | Needed before route contracts and client integration are final; blocks API-001..006 | 1 | Backend + API owner |
