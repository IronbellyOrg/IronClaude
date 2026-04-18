---
spec_source: "test-spec-user-auth.md"
complexity_score: 0.6
complexity_class: MEDIUM
primary_persona: architect
adversarial: false
base_variant: "none"
variant_scores: "none"
convergence_score: 1.0
debate_rounds: 0
generated: "2026-04-15"
generator: "roadmap-single-haiku-architect"
total_phases: 4
total_task_rows: 45
risk_count: 6
open_questions: 6
---

# User Authentication Service — Project Roadmap

## Executive Summary

1. Deliver a rollback-safe auth subsystem in four phases: security/data foundation, domain services, API exposure, then hardening and release validation.
2. Keep the critical path narrow: config/keys and migration first, then crypto primitives, then token manager and auth orchestration, then middleware/routes, then SLO validation and rollout drill.
3. Treat token rotation, replay detection, and secrets handling as the main architecture drivers; they define schema, dependency injection boundaries, and launch gates.

**Business Impact:** Unlocks protected-user capabilities with production-grade auth while preserving rollback control via `AUTH_SERVICE_ENABLED` and migration down-scripts.

**Complexity:** MEDIUM (0.6) — Security sensitivity is high, but the component set is bounded and the implementation order is well constrained.

**Critical path:** COMP-012/OPS-001/COMP-007 → COMP-003/COMP-004 → COMP-009/COMP-002 → COMP-001 → COMP-005/COMP-006/API-001..006 → NFR validation + MIG-002.

**Key architectural decisions:**
- Use RS256 with private-key material in secrets manager and public verification keys distributed per environment.
- Keep access tokens stateless and short-lived; enforce revocation through hashed refresh tokens, rotation, and replay-triggered global user invalidation.
- Roll out routes behind `AUTH_SERVICE_ENABLED` so schema and code can ship dark before exposure.

**Open risks requiring resolution before Phase 1:**
- Exact paths for register, refresh, and reset endpoints must be fixed before route contracts are frozen.
- Reset email dispatch mode (sync vs queue) must be chosen before FR-AUTH.5 latency expectations are locked.
- Maximum active refresh tokens per user must be defined before repository eviction and replay-handling policy are finalized.

## Phase 1: Security and Data Foundation

**Phase 1** | milestone: schema+crypto ready | duration: 4-5d | exit criteria: keys provisioned; migration rollback verified; repositories and crypto primitives ready

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | OPS-001 | Provision auth secrets and env | Ops | — | RS256-keypair:stored; AUTH_SERVICE_ENABLED:set; cookie+TTL env:set; env-parity:dev+prod | M | P0 |
| 2 | COMP-012 | Define secrets provider | Sec | OPS-001 | name:SecretsProvider; path:src/auth/secrets-provider.ts; role:load RS256 keys+auth env; deps:SecretsMgr+env; source:2.1+9 | M | P0 |
| 3 | COMP-007 | Build auth table migration | DB | OPS-001 | name:AuthMigration; path:src/database/migrations/003-auth-tables.ts; role:add users+refresh_tokens tables; deps:Database; source:4.2 | M | P0 |
| 4 | MIG-001 | Apply auth schema migration | DB | COMP-007 | users+refresh_tokens:created; idx+FK:valid; up:idempotent; deploy-doc:ready | M | P0 |
| 5 | MIG-002 | Verify migration rollback path | DB | MIG-001 | down-script:present; rollback:clean; reapply:pass; orphan-schema:none | M | P0 |
| 6 | DM-001 | Model user record schema | DB | MIG-001 | id:uuid-v4; email:string+unique+idx; display_name:string; password_hash:bcrypt; is_locked:boolean; created_at:Date; updated_at:Date | M | P0 |
| 7 | DM-002 | Model refresh token schema | DB | MIG-001 | id:uuid-v4; user_id:FK->UserRecord.id; token_hash:SHA-256; expires_at:Date; revoked:boolean; created_at:Date | M | P0 |
| 8 | DM-003 | Define auth token pair DTO | Auth | — | access_token:JWT-15m; refresh_token:opaque-7d | S | P1 |
| 9 | COMP-008 | Implement user repository | DB | DM-001 | name:UserRepository; path:src/auth/user-repository.ts; role:user CRUD+lookup by email/id; deps:DM-001+Database; source:FR-AUTH.1+2+4 | M | P0 |
| 10 | COMP-009 | Implement refresh token repo | DB | DM-002 | name:RefreshTokenRepository; path:src/auth/refresh-token-repository.ts; role:store+rotate+revoke token hashes; deps:DM-002+Database; source:FR-AUTH.3 | M | P0 |
| 11 | COMP-003 | Implement RS256 JWT service | Sec | COMP-012 | name:JwtService; path:src/auth/jwt-service.ts; role:RS256 sign+verify JWT; deps:jsonwebtoken+RSA key pair; source:4.1 | M | P0 |
| 12 | COMP-004 | Implement bcrypt hasher | Sec | OPS-001 | name:PasswordHasher; path:src/auth/password-hasher.ts; role:hash+compare with cost config; deps:bcrypt; source:4.1 | M | P0 |

### Integration Points — Phase 1

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| SecretsProvider | DI/config | secrets manager + env → JwtService | 1 | COMP-003 |
| 003-auth-tables | migration runner | DB migrator → users/refresh_tokens schema | 1 | MIG-001,MIG-002 |
| UserRepository | DI | DB pool → user lookup/write methods | 1 | COMP-001,FR-AUTH.1,FR-AUTH.2,FR-AUTH.4 |
| RefreshTokenRepository | DI | DB pool → token hash persistence | 1 | COMP-002,FR-AUTH.3 |
| JwtService | strategy | RS256 signer/verifier → TokenManager | 1 | COMP-002,COMP-005 |
| PasswordHasher | strategy | bcrypt cost policy → AuthService | 1 | COMP-001,FR-AUTH.1,FR-AUTH.2,FR-AUTH.5 |

## Phase 2: Core Authentication Flows

**Phase 2** | milestone: domain flows implemented | duration: 5-6d | exit criteria: login/register/refresh/reset services pass unit tests and endpoint contracts are frozen

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | COMP-002 | Implement token manager | Auth | COMP-003,COMP-009,DM-003 | name:TokenManager; path:src/auth/token-manager.ts; role:issue+refresh+revoke token pairs; deps:COMP-003+RefreshToken repository; source:4.1 | L | P0 |
| 2 | COMP-001 | Implement auth service | Auth | COMP-002,COMP-004,COMP-008 | name:AuthService; path:src/auth/auth-service.ts; role:login+register+refresh+reset orchestration; deps:COMP-002+COMP-004+User repository; source:4.1 | L | P0 |
| 3 | COMP-010 | Implement auth rate limiter | Sec | COMP-001 | name:AuthRateLimiter; path:src/auth/auth-rate-limiter.ts; role:cap login attempts per IP; deps:req IP+rate store; source:FR-AUTH.1d | M | P0 |
| 4 | COMP-011 | Implement reset email adapter | Auth | OPS-001 | name:ResetEmailAdapter; path:src/auth/reset-email-adapter.ts; role:compose+dispatch reset email; deps:Email service+reset URL config; source:FR-AUTH.5a+OQ-1 | M | P1 |
| 5 | FR-AUTH.2 | Deliver user registration flow | Auth | COMP-001,COMP-004,COMP-008 | valid→201+profile; dup-email→409; pwd:min8+upper+lower+digit; email:format-valid | L | P0 |
| 6 | API-002 | Freeze register route contract | API | FR-AUTH.2 | POST:/auth/register; body:email+password+display_name; 201:user-profile; 409:dup-email | S | P0 |
| 7 | FR-AUTH.1 | Deliver user login flow | Auth | COMP-001,COMP-002,COMP-010 | valid→200+access15m+refresh7d; invalid→401+no-enum; locked→403; limit:5/min/IP | L | P0 |
| 8 | API-001 | Freeze login route contract | API | FR-AUTH.1 | POST:/auth/login; body:email+password; 200:access+refresh; 401/403:spec | S | P0 |
| 9 | FR-AUTH.3 | Deliver token refresh flow | Auth | COMP-002,COMP-009 | valid-refresh→200+rotated pair; expired→401; replay→global revoke; token-hash:persisted | L | P0 |
| 10 | API-003 | Freeze refresh route contract | API | FR-AUTH.3 | POST:/auth/refresh; input:refresh cookie; 200:new pair; 401:expired+revoked | S | P0 |
| 11 | FR-AUTH.5 | Deliver password reset flow | Auth | COMP-001,COMP-004,COMP-011,COMP-009 | registered-email→reset1h+email; valid token→pwd changed+token invalidated; bad token→400; reset→revoke all sessions | XL | P0 |
| 12 | API-005 | Freeze reset request contract | API | FR-AUTH.5 | POST:/auth/reset-password; body:email; token:1h; dispatch:email-service | S | P1 |
| 13 | API-006 | Freeze reset confirm contract | API | FR-AUTH.5 | POST:/auth/reset-password/confirm; body:token+password; success:pwd-reset; invalid/expired→400 | S | P1 |

### Integration Points — Phase 2

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| TokenManager | strategy chain | JwtService + RefreshTokenRepository + TTL policy | 2 | COMP-001,FR-AUTH.1,FR-AUTH.3,FR-AUTH.5 |
| AuthService | orchestration | UserRepository + PasswordHasher + TokenManager | 2 | API-001,API-002,API-003,API-005,API-006 |
| AuthRateLimiter | middleware/callback | request IP key → login guard | 2 | FR-AUTH.1,API-001 |
| ResetEmailAdapter | external adapter | reset token payload → Email service | 2 | FR-AUTH.5,API-005 |
| API contracts | route registry | method/path → AuthService handlers | 2 | COMP-006 |

## Phase 3: API Exposure and Verification

**Phase 3** | milestone: protected API exposed | duration: 4-5d | exit criteria: middleware/routes live behind flag; profile flow works; unit and integration suites pass

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | COMP-013 | Implement auth config validator | Auth | OPS-001,COMP-012 | name:AuthConfig; path:src/auth/auth-config.ts; role:validate TTLs+cookie flags+key presence; deps:env+SecretsProvider; source:2.1+9 | M | P0 |
| 2 | COMP-014 | Implement route feature gate | Gate | OPS-001 | name:AuthFeatureGate; path:src/auth/auth-feature-gate.ts; role:toggle auth routes by AUTH_SERVICE_ENABLED; deps:env+router; source:9 | S | P0 |
| 3 | COMP-015 | Implement cookie and CORS policy | Sec | COMP-013 | name:AuthCookiePolicy; path:src/auth/auth-cookie-policy.ts; role:httpOnly refresh cookie+CORS config; deps:auth env+routes; source:2.1 | M | P0 |
| 4 | COMP-005 | Implement auth middleware | API | COMP-002,COMP-013 | name:AuthMiddleware; path:src/middleware/auth-middleware.ts; role:extract+verify Bearer token; deps:COMP-002; source:4.2 | M | P0 |
| 5 | FR-AUTH.4 | Deliver profile retrieval | API | COMP-001,COMP-005,COMP-008 | valid bearer→200+id+email+display_name+created_at; invalid/expired→401; sensitive:excluded | M | P0 |
| 6 | API-004 | Freeze profile route contract | API | FR-AUTH.4 | GET:/auth/me; Bearer:required; 200:profile; 401:invalid+expired | S | P0 |
| 7 | COMP-006 | Register auth route group | API | COMP-001,COMP-005,COMP-014,COMP-015,API-001,API-002,API-003,API-004,API-005,API-006 | name:AuthRoutes; path:src/routes/index.ts; role:register /auth/* route group; deps:COMP-001; source:4.2 | L | P0 |
| 8 | TEST-001 | Add crypto primitive tests | Test | COMP-003,COMP-004 | rs256 sign/verify:pass; tamper→reject; bcrypt cost12:pass; compare:pass | M | P1 |
| 9 | TEST-002 | Add auth service unit tests | Test | COMP-001,COMP-002,COMP-010,COMP-011 | login/register/refresh/reset:pass; dup-email→409; locked→403; replay→global revoke | L | P0 |
| 10 | TEST-003 | Add route integration tests | Test | COMP-006,API-001,API-002,API-003,API-004,API-005,API-006 | status codes:match; cookie+Bearer flows:pass; flag-off→disabled; sensitive fields:excluded | L | P0 |

### Integration Points — Phase 3

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| AuthConfig | config/DI | env validation → service boot | 3 | COMP-001,COMP-002,COMP-003,COMP-015 |
| AuthFeatureGate | feature flag | AUTH_SERVICE_ENABLED → route registry | 3 | COMP-006,OPS-005 |
| AuthCookiePolicy | middleware/config | cookie attrs + CORS headers → auth responses | 3 | API-001,API-003,API-005,API-006 |
| AuthMiddleware | middleware chain | Bearer extraction + TokenManager verify → request context | 3 | FR-AUTH.4,API-004 |
| AuthRoutes | route registry | handlers + middleware + gate → `/auth/*` exposure | 3 | clients,TEST-003 |
| Integration suite | test harness | app boot + DB fixtures + HTTP assertions | 3 | TEST-003,NFR-AUTH.1 |

## Phase 4: Hardening, Operations, and Release

**Phase 4** | milestone: production readiness proven | duration: 4-5d | exit criteria: NFRs validated; alerts and rollout controls active; open questions reduced to post-v1 items

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | NFR-AUTH.1 | Validate auth latency budget | Gate | TEST-003,COMP-015 | p95:<200ms; tool:k6; env:prod-like; regressions:none | L | P0 |
| 2 | NFR-AUTH.2 | Validate auth availability | Ops | COMP-006 | uptime:>=99.9%; healthcheck:monitored; PagerDuty:alerting; SLO:published | M | P0 |
| 3 | NFR-AUTH.3 | Validate hashing security target | Sec | COMP-004,TEST-001 | bcrypt-cost:12; hash-time:~250ms; unit-test:pass; benchmark:pass | M | P0 |
| 4 | OPS-002 | Add health and uptime checks | Ops | COMP-006 | health-endpoint:covered; uptime-monitor:on; alert route:PagerDuty; runbook:linked | M | P0 |
| 5 | OPS-003 | Add auth security observability | Ops | COMP-006,COMP-010 | auth events:logged; replay alerts:on; failed-login metrics:on; PII:redacted | M | P1 |
| 6 | OPS-004 | Define key rotation procedure | Sec | COMP-012,COMP-003 | rotation:90d; dual-key overlap:documented; rollback:defined; ownership:assigned | M | P1 |
| 7 | OPS-005 | Execute feature-flag rollout plan | Gate | COMP-014,TEST-003,NFR-AUTH.1,NFR-AUTH.2 | dark-launch:pass; canary:pass; rollback<5m; flag-state:audited | M | P0 |
| 8 | TEST-004 | Run end-to-end auth scenario | Test | COMP-006,OPS-005 | register→login→me→refresh→reset:pass; cookie flow:pass; replay defense:pass | L | P0 |
| 9 | TEST-005 | Run migration and recovery drills | Test | MIG-001,MIG-002,OPS-005 | backup-restore:pass; down+up:pass; rollback under flag-off:pass | M | P1 |
| 10 | DOC-001 | Publish auth architecture notes | Docs | COMP-006,NFR-AUTH.2,OPS-004 | diagrams:updated; endpoint contracts:frozen; rollback+ops:documented; owners:named | M | P2 |

## Risk Assessment and Mitigation

| # | Risk | Severity | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|---|---|
| 1 | Private key exposure for RS256 signer | High | Low | Forged access tokens | Secrets manager, least-privilege access, 90d rotation, rollout drill | Security |
| 2 | Refresh-token replay after theft | High | Medium | Account takeover across sessions | Rotation on every refresh, hashed persistence, replay-triggered global revoke | Backend |
| 3 | bcrypt cost causes latency breach | Medium | Medium | Login/register p95 > 200ms | Benchmark cost 12 early, isolate hashing path, tune infrastructure headroom | Backend |
| 4 | Email provider latency stalls reset flow | Medium | Medium | Reset endpoint timeout or user-facing delays | Decide sync vs queue before build, timeout budget, retry/dead-letter policy | Backend |
| 5 | Undefined max active refresh tokens | Medium | Medium | Repo growth and unclear multi-device behavior | Resolve token cap in architecture review, add eviction policy before GA | Architect |
| 6 | Feature flag rollback path untested | High | Low | Slow incident containment | Dark launch, canary rollout, rollback drill with schema retained | Ops |

## Resource Requirements and Dependencies

### External Dependencies

| Dependency | Required By Phase | Status | Fallback |
|---|---|---|---|
| jsonwebtoken | 1-4 | Required | Delay COMP-003 until approved library present |
| bcrypt | 1-4 | Required | Block launch; no weaker hash substitute |
| Email service | 2-4 | Required | Queue-backed adapter or temporary noop in non-prod only |
| Database | 1-4 | Required | No fallback; migration gate blocks rollout |
| Secrets manager | 1-4 | Required | Env-file only for local dev; never prod |
| k6 | 4 | Required | Equivalent load harness if org-standard tool differs |
| PagerDuty | 4 | Required | Temporary alert sink only before production cut |

### Infrastructure Requirements

- RSA key-pair generation and secure private-key storage per environment.
- Database capacity for `users` and `refresh_tokens`, including unique email index and token-hash lookups.
- Rate-limit backing store sized for 5/min/IP enforcement on login.
- HTTPS, cookie security flags, and CORS policy aligned to refresh-cookie transport.
- Production-like staging environment for latency, replay, rollback, and failover validation.

## Success Criteria and Validation Approach

| Criterion | Metric | Target | Validation Method | Phase |
|---|---|---|---|---|
| SC-1 login success | HTTP status + payload | 200 + access15m + refresh7d | TEST-003 + TEST-004 | 3-4 |
| SC-2 login failure privacy | Error contract | 401 + no credential enumeration | TEST-002 + TEST-003 | 2-3 |
| SC-3 locked account handling | HTTP status | 403 | TEST-002 + TEST-003 | 2-3 |
| SC-4 login throttling | Per-IP attempt cap | 5/min/IP | TEST-002 + observability check | 2-4 |
| SC-5 registration success | HTTP status + profile | 201 + user profile | TEST-002 + TEST-003 | 2-3 |
| SC-6 duplicate email rejection | Conflict response | 409 | TEST-002 + TEST-003 | 2-3 |
| SC-7 password policy | Validation rules | min8 + upper + lower + digit | TEST-002 | 2 |
| SC-8 email validation | Input validation | RFC-style format gate | TEST-002 | 2 |
| SC-9 refresh rotation | Token lifecycle | new pair every refresh | TEST-002 + TEST-004 | 2-4 |
| SC-10 expired refresh denial | HTTP status | 401 | TEST-002 + TEST-003 | 2-3 |
| SC-11 replay defense | Security control | revoked replay → global revoke | TEST-002 + TEST-004 | 2-4 |
| SC-12 token-hash persistence | Storage check | refresh hashes stored | DB assertion in TEST-003 | 3 |
| SC-13 profile success | Response contract | 200 + id,email,display_name,created_at | TEST-003 + TEST-004 | 3-4 |
| SC-14 invalid bearer denial | HTTP status | 401 | TEST-003 | 3 |
| SC-15 sensitive field exclusion | Response hygiene | no password_hash/token_hash | TEST-003 | 3 |
| SC-16 reset request dispatch | Token/email workflow | reset token 1h + email sent | TEST-002 + provider stub/integration | 2-3 |
| SC-17 reset confirm success | Password update | new password accepted; token spent | TEST-002 + TEST-004 | 2-4 |
| SC-18 invalid reset denial | HTTP status | 400 | TEST-002 + TEST-003 | 2-3 |
| SC-19 session invalidation on reset | Revocation coverage | all refresh tokens invalidated | TEST-002 + TEST-004 | 2-4 |
| SC-20 auth latency | p95 latency | <200ms | k6 + APM review | 4 |
| SC-21 availability | Uptime SLO | >=99.9% | health monitoring + PagerDuty evidence | 4 |
| SC-22 hashing posture | bcrypt config | cost factor 12 | unit + benchmark tests | 4 |

## Timeline Estimates

| Phase | Duration | Start | End | Key Milestones |
|---|---|---|---|---|
| 1 | 4-5d | Day 1 | Day 5 | keys ready; migration up/down verified; crypto services complete |
| 2 | 5-6d | Day 6 | Day 11 | AuthService + TokenManager complete; login/register/refresh/reset contracts frozen |
| 3 | 4-5d | Day 12 | Day 16 | middleware/routes live behind flag; profile endpoint and integration suite pass |
| 4 | 4-5d | Day 17 | Day 21 | SLO evidence complete; rollout drill pass; ops docs published |

**Total estimated duration:** 17-21 working days

## Open Questions

| # | Question | Impact | Blocking Phase | Resolution Owner |
|---|---|---|---|---|
| 1 | Should reset email send inline or via queue? | Determines reset latency path and retry design | 2 | Architect + Backend |
| 2 | Maximum active refresh tokens per user? | Shapes repo eviction, multi-device support, and replay blast radius | 2 | Architect |
| 3 | Progressive lockout policy after repeated failures? | Needed to close GAP-1 beyond simple per-IP rate limit | 4 | Product + Security |
| 4 | Audit logging schema and sink for auth events? | Required for incident response and compliance maturity | 4 | Ops + Security |
| 5 | Revoke all tokens on user deletion? | Affects deletion semantics and residual access risk | 4 | Architect + Backend |
| 6 | Confirm final REST paths for register/refresh/reset? | Needed before route contracts and client integration are final | 2 | Backend + API owner |