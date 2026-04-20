---
spec_source: "test-tdd-user-auth.compressed.md"
complexity_score: 0.72
complexity_class: HIGH
primary_persona: architect
---

# User Authentication Service — Project Roadmap

## Executive Summary

A standards-compliant identity layer (AuthService + TokenManager + JwtService + PasswordHasher) delivered in five technically-phased milestones preserving the TDD's 10-week calendar commitment ending 2026-06-09. The architecture is stateless JWT with opaque refresh tokens (Redis-backed), PostgreSQL-persisted UserProfile, bcrypt cost 12 hashing, RS256 2048-bit signing, and a staged rollout gated by AUTH_NEW_LOGIN and AUTH_TOKEN_REFRESH feature flags. Layering is Foundation → Token Management → Compliance & Reset → Frontend Integration → Production Readiness, with gating flags preventing external exposure of partial features at every seam.

**Business Impact:** Unblocks ~$2.4M projected annual revenue from Q2–Q3 2026 personalization features, closes the SOC2 Type II audit gap before Q3 2026, and addresses the 25% churn-survey signal citing absence of accounts. Targets: >60% registration conversion, >1000 DAU within 30 days of GA, <5% failed-login rate, >30-minute average session duration, >80% password-reset completion.

**Complexity:** HIGH (0.72) — multi-component backend (AuthService/TokenManager/JwtService/PasswordHasher) with dual persistence (PostgreSQL + Redis), cross-cutting security (bcrypt 12, RS256 2048-bit, TLS 1.3, lockout, CORS), frontend integration surface (LoginPage/RegisterPage/AuthProvider), staged rollout with feature flags, and compliance obligations (SOC2 Type II, GDPR, NIST SP 800-63B).

**Critical path:** DM-001 UserProfile schema → PasswordHasher → AuthService.register/login → TokenManager+JwtService → /auth/me + /auth/refresh → Password Reset + Audit Logging → AuthProvider silent refresh → Phased rollout (Alpha → 10% Beta → GA). Any slip on DM-001 or JwtService key provisioning blocks every downstream milestone.

**Key architectural decisions:**

- Stateless JWT (RS256, 2048-bit RSA, quarterly rotation) with 15-min access tokens + opaque refresh tokens (Redis, 7-day TTL, hashed-at-rest); rejected server-side sessions because horizontal scale across future services requires stateless verification.
- bcrypt cost factor 12 via PasswordHasher abstraction; rejected argon2id/scrypt for battle-tested security properties and fit within <500ms hash target at cost 12.
- URL-versioned REST API (`/v1/auth/*`) with unified error envelope `{error:{code,message,status}}`; rejected third-party (Auth0/Firebase) to retain UserProfile/TokenManager control and avoid vendor lock-in.

**Open risks requiring resolution before M1:**

- OQ-M1-001 (TDD schedule overshoot): M1 TDD target 2026-04-14 has already passed (today 2026-04-20); committed default now runs 2026-04-20 → 2026-05-04 with compressed Phase 2/3 windows to preserve TDD end date 2026-06-09.
- OQ-M1-002 (audit-log retention conflict): TDD §7.2 states 90-day retention; PRD S17 (derived NFR-COMP-001) and SOC2 require 12 months. Precedence rule: compliance authority > TDD design default → committed 12-month retention applied consistently across DM-AUDIT, OPS-004, Timeline, Success Criteria. TDD §7.2 must be updated.
- OQ-M1-003 (JwtService RSA key custody): 2048-bit RS256 key provisioning and quarterly-rotation procedure must be signed off by sec-reviewer before any token is issued.

## Milestone Summary

|ID|Title|Type|Priority|Effort|Dependencies|Deliverables|Risk|
|---|---|---|---|---|---|---|---|
|M1|Foundation: Data Layer, AuthService, Registration, Login|Backend|P0|L|INFRA-DB-001, SEC-POLICY-001|22|HIGH|
|M2|Token Management: Refresh, Profile, JWT|Backend|P0|L|M1|18|HIGH|
|M3|Password Reset, Compliance & Audit Logging|Backend|P0|M|M1, M2|14|MEDIUM|
|M4|Frontend Integration: LoginPage, RegisterPage, AuthProvider|Frontend|P0|M|M1, M2, M3|16|MEDIUM|
|M5|Production Readiness: Rollout, Observability, Operations|DevOps|P0|M|M1, M2, M3, M4|20|HIGH|

## Dependency Graph

```
INFRA-DB-001 (PostgreSQL 15) ─┐
SEC-POLICY-001 ───────────────┤
Redis 7+ ─────────────────────┤
                              ▼
                             M1 (Foundation)
                              │  DM-001, PasswordHasher, AuthService,
                              │  /auth/login, /auth/register, lockout
                              ▼
                             M2 (Token Management)
                              │  TokenManager, JwtService, DM-002,
                              │  /auth/refresh, /auth/me, Redis
                              ▼
                             M3 (Password Reset + Compliance)
                              │  FR-AUTH-005, SendGrid, audit log,
                              │  GDPR consent, data minimization
                              ▼
                             M4 (Frontend Integration)
                              │  LoginPage, RegisterPage, AuthProvider,
                              │  silent refresh, XSS mitigation
                              ▼
                             M5 (Production Readiness)
                                 MIG-001/002/003, feature flags,
                                 observability, alerts, runbooks, GA
```

**TDD ↔ Roadmap milestone mapping:** Roadmap M1↔TDD M1 (2026-04-14 target, overdue — see OQ-M1-001), M2↔TDD M2 (2026-04-28), M3↔TDD M3 (2026-05-12), M4↔TDD M4 (2026-05-26), M5↔TDD M5 (2026-06-09 GA).

## M1: Foundation — Data Layer, AuthService, Registration, Login

**Objective:** Stand up PostgreSQL-backed UserProfile persistence, PasswordHasher (bcrypt cost 12), AuthService orchestrator, and the two unauthenticated endpoints (/auth/login, /auth/register) with account-lockout protection. | **Duration:** 2 weeks (2026-04-20 → 2026-05-04, compressed to respect TDD M1 2026-04-14 original target) | **Entry:** INFRA-DB-001 PostgreSQL 15 provisioned; SEC-POLICY-001 approved; Node.js 20 LTS runtime available. | **Exit:** FR-AUTH-001 and FR-AUTH-002 pass unit + integration tests against real PostgreSQL; `PasswordHasher.hash()` benchmark <500ms at cost 12; /auth/login and /auth/register endpoints behind `AUTH_NEW_LOGIN=OFF` flag (disabled-by-default gating prevents external exposure until M4/M5).

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|DM-001|UserProfile PostgreSQL schema|Create `user_profiles` table with all source fields and indexes per TDD §7.1|PostgreSQL|INFRA-DB-001|id:UUID-PK-NOT-NULL; email:varchar-UNIQUE-NOT-NULL-indexed-lowercased; display_name:varchar-NOT-NULL-2-to-100-chars; password_hash:varchar-NOT-NULL-bcrypt; created_at:timestamptz-NOT-NULL-DEFAULT-now(); updated_at:timestamptz-NOT-NULL-auto-updated-trigger; last_login_at:timestamptz-NULLABLE; roles:text[]-NOT-NULL-DEFAULT-{user}; migration file committed; indices verified via \d+|M|P0|
|2|DM-AUDIT|Audit log PostgreSQL schema|Create `auth_audit_log` table for SOC2 Type II event trail per NFR-COMP-001|PostgreSQL|DM-001|id:UUID-PK; user_id:UUID-NULLABLE-FK-user_profiles; event_type:varchar-NOT-NULL-enum(login_success,login_failure,register,reset_request,reset_confirm,token_refresh,lockout); occurred_at:timestamptz-NOT-NULL-DEFAULT-now(); ip_address:inet; outcome:varchar-NOT-NULL; retention policy documented as 12 months per OQ-M1-002|S|P0|
|3|COMP-AUTHSVC|AuthService orchestrator class|Implement facade class delegating to PasswordHasher/TokenManager/UserRepo per TDD §6.2|AuthService|DM-001|class AuthService exported from src/services/auth-service.ts; constructor-injects PasswordHasher, UserRepo, TokenManager; methods login(), register(), getProfile() signatures stubbed; TypeScript strict mode clean|M|P0|
|4|COMP-PWDHASH|PasswordHasher component|Bcrypt abstraction with cost factor 12 per NFR-SEC-001|PasswordHasher|—|class PasswordHasher with hash(password) and verify(password, hash) methods; uses bcryptjs with saltRounds=12; unit test asserts cost parameter==12; benchmark <500ms at cost 12 on target hardware|S|P0|
|5|COMP-USERREPO|UserRepo data-access component|PostgreSQL data access layer for UserProfile|UserRepo|DM-001|class UserRepo with findByEmail(), findById(), insert(profile), updateLastLogin(id, ts); pg-pool-based with 100-connection pool; parameterized queries only (no string concat); covered by integration tests against testcontainer|M|P0|
|6|FR-AUTH-001|Login authentication logic|AuthService.login() validates credentials via PasswordHasher against stored hashes per TDD §5.1|AuthService|COMP-AUTHSVC,COMP-PWDHASH,COMP-USERREPO|valid creds return 200 with AuthToken; invalid creds return 401 generic error; non-existent email returns 401 (no user enumeration); last_login_at updated on success; email normalized to lowercase before lookup|M|P0|
|7|FR-AUTH-002|Registration with validation|AuthService.register() creates UserProfile with email uniqueness + password policy per TDD §5.1|AuthService|COMP-AUTHSVC,COMP-PWDHASH,COMP-USERREPO|valid registration returns 201 with UserProfile body; duplicate email returns 409 Conflict; weak password (<8 chars OR no uppercase OR no number) returns 400 with field errors; password stored as bcrypt hash cost 12; audit event inserted|M|P0|
|8|API-001|POST /auth/login endpoint|REST endpoint binding per TDD §8.2|API|FR-AUTH-001|route registered at POST /v1/auth/login; request schema {email,password}; response 200 AuthToken; error envelope {error:{code,message,status}}; codes AUTH_INVALID_CREDENTIALS, AUTH_ACCOUNT_LOCKED, AUTH_RATE_LIMITED|S|P0|
|9|API-002|POST /auth/register endpoint|REST endpoint binding per TDD §8.2|API|FR-AUTH-002|route registered at POST /v1/auth/register; request schema {email,password,displayName}; response 201 UserProfile; error envelope for VALIDATION, DUPLICATE_EMAIL|S|P0|
|10|FEAT-LOCK|Account lockout enforcement|Lockout after 5 failed attempts within 15 minutes per FR-AUTH-001 AC4|AuthService|FR-AUTH-001,DM-AUDIT|failed-attempt counter persisted (Redis key `lockout:{email}` with 15-min sliding window); 5th failure sets lock flag for 15 min; subsequent login attempts return 423 Locked; audit event emitted; unit + integration tests|M|P0|
|11|API-ERR|Unified error envelope middleware|`{error:{code,message,status}}` response shape across all /auth/* endpoints per TDD §8.3|API|—|Express/Fastify error middleware emits envelope; codes enumerated (AUTH_INVALID_CREDENTIALS, AUTH_DUPLICATE_EMAIL, AUTH_RATE_LIMITED, AUTH_ACCOUNT_LOCKED, AUTH_WEAK_PASSWORD); no stack traces in response body|S|P0|
|12|API-RATE|Rate limiting configuration|API Gateway limits per TDD §8.1: 10/min login per IP, 5/min register per IP|API Gateway|API-001,API-002|gateway config file committed; 429 Too Many Requests returned; Retry-After header set; integration test verifies limits trigger correctly|S|P0|
|13|NFR-SEC-001|bcrypt cost 12 validation test|Unit test enforcing PasswordHasher uses bcrypt with cost factor 12|Testing|COMP-PWDHASH|test asserts bcrypt.getRounds(hash)==12; CI fails if cost factor changes without review|XS|P0|
|14|NFR-PERF-001|Login endpoint latency instrumentation (p95 <200ms)|Histogram + p95 alert rule wired for AuthService.login per TDD §17 and NFR-PERF-001|Observability|API-001|prometheus histogram `auth_login_duration_seconds` (buckets 0.025,0.05,0.1,0.2,0.5,1,2); OpenTelemetry span `AuthService.login` emitted; alert rule `histogram_quantile(0.95, auth_login_duration_seconds) > 0.200 for 5m` committed|S|P0|
|15|NFR-PERF-002|Concurrent 500-user load profile (k6)|k6 script validating 500 concurrent logins sustain <200ms p95 per NFR-PERF-002|Testing|API-001,NFR-PERF-001|k6 script in tests/load/login.js; VU=500 sustained for 5min; p95<200ms assertion; result artifact published to CI|S|P0|
|16|TEST-001|Unit — login with valid credentials returns AuthToken|Per TDD §15.2|Testing|FR-AUTH-001|jest test mocks PasswordHasher.verify→true, TokenManager.issueTokens; asserts AuthToken shape and call order; covers FR-AUTH-001 AC1|XS|P0|
|17|TEST-002|Unit — login with invalid credentials returns 401|Per TDD §15.2|Testing|FR-AUTH-001|jest test mocks PasswordHasher.verify→false; asserts 401 and no tokens issued; covers FR-AUTH-001 AC2, AC3|XS|P0|
|18|TEST-004|Integration — registration persists UserProfile to database|Per TDD §15.2 using testcontainers|Testing|FR-AUTH-002,DM-001|supertest + testcontainer PostgreSQL; POST /auth/register returns 201; SELECT from user_profiles WHERE email=X returns 1 row with bcrypt hash|S|P0|
|19|OPS-LOG-M1|Structured login/registration logging|stdout JSON logs for login_success/failure and register per OPS-004 (exclude password/tokens)|Observability|FR-AUTH-001,FR-AUTH-002|pino/winston logger; fields user_id, event, timestamp, ip, outcome; password and accessToken/refreshToken fields redacted; log sampled for load tests|S|P0|
|20|METRIC-REG|Registration counter metric|`auth_registration_total` counter per OPS-004|Observability|FR-AUTH-002|prometheus counter with labels {outcome=success\|duplicate\|validation}; emitted on every register attempt|XS|P1|
|21|METRIC-LOGIN|Login counter metric|`auth_login_total` counter per OPS-004|Observability|FR-AUTH-001|prometheus counter with labels {outcome=success\|invalid\|locked\|rate_limited}; emitted on every login attempt|XS|P1|
|22|TLS-CORS|TLS 1.3 + CORS restriction|TLS 1.3 termination at gateway; CORS allowlist for known frontend origins per TDD §13|DevOps|API-001,API-002|ingress config enforces TLSv1.3; CORS allowlist committed to config/cors-origins.json; integration test verifies 403 on disallowed origin|S|P0|

### Integration Points — M1

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|PasswordHasher|Dependency injection|M1 (COMP-AUTHSVC constructor-injects)|M1|AuthService.login, AuthService.register|
|UserRepo|Dependency injection|M1 (COMP-AUTHSVC constructor-injects)|M1|AuthService.login, AuthService.register, future AuthService.getProfile|
|API error middleware|Middleware chain|M1 (registered after routes)|M1|all /auth/* endpoints|
|API Gateway rate-limit policy|Gateway config binding|M1 (deployed before routes)|M1|POST /auth/login, POST /auth/register|

### Milestone Dependencies — M1

- INFRA-DB-001 PostgreSQL 15 provisioned and reachable from service network.
- SEC-POLICY-001 approved (password policy, key custody, lockout policy).
- Node.js 20 LTS runtime images built and published.
- Redis 7 reachable (used by lockout counter; full refresh-token use lands in M2).

### Open Questions — M1

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-M1-001|TDD M1 target 2026-04-14 has passed (today 2026-04-20). Commit to compressed 2026-04-20→2026-05-04 schedule to preserve TDD GA 2026-06-09, or reschedule all downstream milestones? Committed default: compressed schedule.|Blocks every downstream milestone date|test-lead, eng-manager|2026-04-22|
|2|OQ-M1-002|Audit-log retention: TDD §7.2 says 90 days; NFR-COMP-001 / PRD / SOC2 require 12 months. Precedence rule: compliance > design default → committed value 12 months applied to DM-AUDIT, OPS-004, Timeline, Success Criteria. TDD §7.2 must be updated.|Committed value: 12 months. Determines storage sizing, backup retention, audit coverage.|sec-reviewer, test-lead|2026-04-22|
|3|OQ-M1-003|JwtService RSA key custody and quarterly rotation procedure — where are 2048-bit private keys stored and who authorizes rotation?|Blocks M2 token issuance; security audit gate|sec-reviewer|2026-04-28|
|4|OQ-M1-004 (from TDD OQ-002)|Maximum allowed UserProfile.roles array length?|Affects DM-001 schema constraint and future RBAC enforcement|auth-team|2026-04-01 (overdue — pending RBAC design review)|
|5|OQ-M1-005 (from PRD OQ-PRD-3)|Exact lockout policy after N failed attempts (threshold/window/unlock mechanism)? TDD specifies 5 attempts / 15 min / 15-min lock — committed to TDD value for M1 unless Security overrides.|Committed value: 5/15min/15-min auto-unlock. Affects FEAT-LOCK acceptance.|sec-reviewer|2026-04-25|

### Risk Assessment and Mitigation — M1

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-002 Brute-force attacks on login endpoint|MEDIUM|HIGH|Credential stuffing at scale|API Gateway rate limit 10/min per IP; FEAT-LOCK after 5 failures/15min; bcrypt cost 12 deters offline cracking; WAF + CAPTCHA planned in M5 as contingency|sec-reviewer|
|2|R-003 Data loss during legacy-auth migration|HIGH|LOW|UserProfile corruption or orphaned accounts|Pre-phase PostgreSQL backup; idempotent upsert on migration script; parallel run with legacy until M5 Phase 2|auth-team|
|3|R-M1-SCHED M1 start slipped past TDD target 2026-04-14|HIGH|CERTAIN (already occurred)|Downstream cascade risk to GA 2026-06-09|Compressed M1 to 2 weeks starting 2026-04-20; OQ-M1-001 tracks decision; weekly burn-down review with eng-manager|test-lead|
|4|R-PRD-002 Compliance failure from incomplete audit logging|HIGH|MEDIUM|SOC2 audit finding; legal exposure|DM-AUDIT schema lands in M1 before any event generation; 12-month retention per OQ-M1-002; log schema reviewed by sec-reviewer before M3 expansion|sec-reviewer|

## M2: Token Management — Refresh, Profile, JWT

**Objective:** Implement `TokenManager` + `JwtService` lifecycle (RS256 2048-bit, 15-min access TTL, 7-day opaque refresh hashed-at-rest in Redis), expose GET /auth/me and POST /auth/refresh, and instrument refresh-latency budget (<100ms p95). | **Duration:** 2 weeks (2026-05-04 → 2026-05-18) | **Entry:** M1 exit complete; OQ-M1-003 resolved (RSA key custody signed off); Redis 7 reachable. | **Exit:** FR-AUTH-003 + FR-AUTH-004 pass unit + integration tests; `TokenManager.refresh` p95 <100ms verified; all four endpoints (`/auth/login`, `/auth/register`, `/auth/me`, `/auth/refresh`) pass integration tests against real PostgreSQL + Redis; `AUTH_TOKEN_REFRESH=OFF` flag keeps refresh disabled externally until M5.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|DM-002|AuthToken response model|Response shape + Redis schema for refresh token storage per TDD §7.1|TokenManager|COMP-TOKMGR|accessToken:JWT-NOT-NULL-RS256-signed-15min-TTL; refreshToken:string-NOT-NULL-unique-opaque-hashed-at-rest; expiresIn:number-NOT-NULL-always-900; tokenType:string-NOT-NULL-always-"Bearer"; Redis key schema `refresh:{hash}` value JSON {user_id,issued_at,expires_at}; TTL=604800 (7 days)|S|P0|
|2|COMP-JWTSVC|JwtService component|RS256 sign/verify wrapper around jsonwebtoken per NFR-SEC-002|JwtService|OQ-M1-003|class JwtService.sign(payload)/verify(token); algorithm="RS256"; 2048-bit RSA key loaded from secrets mount; 5-second clock-skew tolerance; quarterly-rotation procedure documented; unit tests cover valid/expired/tampered tokens|M|P0|
|3|COMP-TOKMGR|TokenManager component|Token lifecycle orchestrator per TDD §6.2|TokenManager|COMP-JWTSVC,DM-002|class TokenManager.issueTokens(userId, roles)/refresh(oldRefresh)/revoke(refresh); persists hashed refresh to Redis; revokes old token on refresh; emits audit events; covered by unit + integration tests|M|P0|
|4|NFR-SEC-002|RS256 2048-bit key validation test|Configuration test asserting JwtService uses RS256 + 2048-bit RSA|Testing|COMP-JWTSVC|test decodes JWT header alg=="RS256"; reads key metadata and asserts bitLength===2048; CI fails on algorithm downgrade|XS|P0|
|5|FR-AUTH-003|JWT token issuance and refresh logic|TokenManager.refresh exchanges valid refresh for new AuthToken pair per TDD §5.1|AuthService|COMP-TOKMGR,COMP-JWTSVC|login returns both accessToken (15 min TTL) and refreshToken (7 day TTL); POST /auth/refresh with valid refreshToken returns new AuthToken pair with old refresh revoked; expired refreshToken returns 401; revoked refreshToken returns 401|M|P0|
|6|FR-AUTH-004|Profile retrieval logic|AuthService.getProfile returns full UserProfile per TDD §5.1|AuthService|COMP-AUTHSVC,COMP-USERREPO|GET /auth/me with valid accessToken returns UserProfile; expired/invalid token returns 401; response includes id,email,displayName,createdAt,updatedAt,lastLoginAt,roles|S|P0|
|7|API-003|GET /auth/me endpoint|REST binding per TDD §8.2|API|FR-AUTH-004,COMP-JWTSVC|route GET /v1/auth/me; Bearer auth middleware verifies accessToken via JwtService; rate limit 60/min per user; returns full UserProfile; error envelope on 401|S|P0|
|8|API-004|POST /auth/refresh endpoint|REST binding per TDD §8.2|API|FR-AUTH-003|route POST /v1/auth/refresh; request {refreshToken}; response 200 new AuthToken pair; rate limit 30/min per user; old token revoked in Redis before new issued (atomic); 401 on expired/revoked|S|P0|
|9|COMP-AUTHMW|Bearer authentication middleware|Token extraction + verification middleware for protected routes|API|COMP-JWTSVC|middleware reads Authorization header; calls JwtService.verify; attaches {user_id, roles} to request; returns 401 with AUTH_TOKEN_INVALID on failure; 5-sec clock skew tolerance honored|S|P0|
|10|FEAT-REFRESH-FLAG|AUTH_TOKEN_REFRESH feature flag wiring|Flag-gated refresh flow per TDD §19.2|Infrastructure|API-004|flag default OFF; when OFF, /auth/refresh returns 404; when ON, full refresh flow active; flag state readable at request time (no restart needed); removal target documented (Phase 3 GA + 2 weeks)|S|P0|
|11|NFR-PERF-003|Token refresh latency instrumentation (p95 <100ms)|Histogram + p95 alert rule wired per TDD §4.1 success metric|Observability|API-004|prometheus histogram `auth_token_refresh_duration_seconds` (buckets 0.01,0.025,0.05,0.1,0.25,0.5); alert rule `histogram_quantile(0.95, auth_token_refresh_duration_seconds) > 0.100 for 5m` committed|S|P0|
|12|METRIC-REFRESH|Token refresh counter metric|`auth_token_refresh_total` counter per OPS-004|Observability|API-004|prometheus counter with labels {outcome=success\|expired\|revoked\|invalid}; emitted on every refresh attempt|XS|P1|
|13|TEST-003|Unit — token refresh with valid refresh token|Per TDD §15.2|Testing|FR-AUTH-003|jest test asserts old token revoked in Redis mock and new AuthToken pair issued via JwtService; covers refresh rotation invariant|XS|P0|
|14|TEST-005|Integration — expired refresh token rejected by TokenManager|Per TDD §15.2 using testcontainer Redis|Testing|FR-AUTH-003,COMP-TOKMGR|integration test sets Redis TTL to 1s; waits 2s; asserts /auth/refresh returns 401 and audit event emitted|S|P0|
|15|TEST-ME|Integration — /auth/me returns authenticated UserProfile|Covers FR-AUTH-004 end-to-end|Testing|API-003|supertest obtains access token via login; GETs /auth/me; asserts 200 with UserProfile shape; asserts 401 for expired token|S|P0|
|16|OPS-LOG-M2|Structured token-event logging|Logs for refresh success/failure (exclude token values) per OPS-004|Observability|API-004|log fields event=token_refresh, user_id, timestamp, outcome, old_token_hash_prefix; token values themselves redacted|XS|P1|
|17|SEC-RT-HASH|Refresh token hashed-at-rest in Redis|Storage hardening per TDD §13 threat model|Infrastructure|DM-002|only SHA-256 hash stored in Redis; raw refreshToken returned to client only once; unit test verifies Redis never contains raw token|S|P0|
|18|SEC-CLOCK-SKEW|JWT clock-skew tolerance configuration|5-second tolerance in JwtService.verify per TDD §12|JwtService|COMP-JWTSVC|config option `clockTolerance: 5`; unit test generates token iat+4s future — verify accepts; iat+6s future — verify rejects|XS|P1|

### Integration Points — M2

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|JwtService|Dependency injection|M2 (TokenManager constructor-injects)|M2|TokenManager, COMP-AUTHMW|
|TokenManager|Dependency injection|M2 (AuthService constructor-injects)|M2|AuthService.login, POST /auth/refresh|
|Bearer auth middleware|Middleware chain|M2 (registered on protected routes)|M2|GET /auth/me, future protected endpoints|
|AUTH_TOKEN_REFRESH flag|Feature-flag client|M2 (runtime-evaluated)|M2|POST /auth/refresh route handler|
|Redis refresh-token store|TCP/RESP client pool|M2 (initialized at boot)|M2|TokenManager.issueTokens, TokenManager.refresh, TokenManager.revoke|

### Milestone Dependencies — M2

- M1 complete: AuthService, PasswordHasher, UserRepo, /auth/login, /auth/register, audit-log schema operational.
- OQ-M1-003 resolved: RSA 2048-bit private/public key pair provisioned in secrets store; rotation schedule signed off.
- Redis 7+ cluster deployed and reachable with hashed refresh-token persistence capability.

### Open Questions — M2

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-M2-001 (from PRD OQ-PRD-2)|Max refresh tokens per user across devices? TDD is silent; PRD leaves open. Impacts Redis sizing and multi-device UX.|Storage sizing; "remember-me" design downstream|product-manager, auth-team|2026-05-11|
|2|OQ-M2-002 (from PRD OQ-PRD-4)|"Remember me" to extend session duration beyond 7-day refresh TTL?|Affects TokenManager TTL logic and UserProfile schema (possible preferences column)|product-manager|2026-05-11|
|3|OQ-M2-003 (JTBD coverage from extraction)|PRD JTBD #2 "pick up where I left off across devices" — confirm cross-device session continuity is in scope or defer. Current implementation supports multi-device via independent refresh tokens per device; explicit sync features are out of scope unless confirmed.|Impacts M4 AuthProvider design and M5 rollout comms|product-manager|2026-05-07|

### Risk Assessment and Mitigation — M2

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-001 Token theft via XSS enables session hijacking|HIGH|MEDIUM|Unauthorized session takeover|SEC-RT-HASH ensures Redis-at-rest hash; accessToken memory-only + refreshToken HttpOnly cookie lands in M4; 15-min access TTL; TokenManager.revoke() available for incident response|sec-reviewer|
|2|R-M2-KEY JwtService signing-key rotation breaks existing tokens|MEDIUM|MEDIUM|Session invalidation wave during rotation|Dual-key verification window (accept N-1 kid during rotation); rotation runbook in OPS-002; unit test covers kid-based verification|auth-team|
|3|R-M2-REDIS Redis unavailability blocks refresh and lockout|HIGH|LOW|User sessions forced to re-login; lockout counter lost|TokenManager fails closed (reject refresh); AuthProvider surfaces clear "session expired" UX (M4); Redis HA replica; alert on Redis connection failures >10/min|platform-team|

## M3: Password Reset, Compliance & Audit Logging

**Objective:** Deliver FR-AUTH-005 password-reset flow (request/confirm) with SendGrid email integration, expand audit logging to full SOC2 Type II coverage (12-month retention per OQ-M1-002), and add GDPR consent capture + data minimization at registration. | **Duration:** 2 weeks (2026-05-18 → 2026-06-01) | **Entry:** M2 exit complete; SendGrid account provisioned; legal sign-off on consent text. | **Exit:** FR-AUTH-005 passes unit, integration, and E2E-precursor tests; audit log covers login/register/refresh/reset events with 12-month retention configured; GDPR consent stored with timestamp per NFR-COMP-001; data minimization enforced (only email, hashed password, display name collected).

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|DM-RESET|PasswordResetToken schema|PostgreSQL table for reset-token lifecycle per FR-AUTH-005|PostgreSQL|DM-001|id:UUID-PK; user_id:UUID-NOT-NULL-FK-user_profiles; token_hash:varchar-NOT-NULL-UNIQUE-SHA256; expires_at:timestamptz-NOT-NULL-1hour-after-creation; used_at:timestamptz-NULLABLE-ensures-single-use; created_at:timestamptz-NOT-NULL-DEFAULT-now(); migration committed|S|P0|
|2|COMP-MAILSVC|EmailService / SendGrid adapter|SendGrid API wrapper for password-reset delivery|EmailService|—|class EmailService.sendResetEmail(email, token, displayName); SendGrid API key from secrets mount; retry with exponential backoff on 5xx; delivery monitored; integration test uses SendGrid sandbox|S|P0|
|3|FR-AUTH-005|Password reset request + confirm logic|Two-step reset flow per TDD §5.1|AuthService|COMP-AUTHSVC,DM-RESET,COMP-MAILSVC,COMP-PWDHASH|POST /auth/reset-request with valid email sends reset token via email (always returns 200 to prevent enumeration); POST /auth/reset-confirm with valid token updates password hash; reset tokens expire after 1 hour; used reset tokens cannot be reused (used_at enforced); all existing refresh tokens revoked on password change|M|P0|
|4|API-RESET-REQ|POST /auth/reset-request endpoint|REST binding per FR-AUTH-005|API|FR-AUTH-005|route POST /v1/auth/reset-request; request {email}; response 200 always (enumeration-safe); rate limit 5/min per IP; audit event emitted regardless of whether email is registered|S|P0|
|5|API-RESET-CONF|POST /auth/reset-confirm endpoint|REST binding per FR-AUTH-005|API|FR-AUTH-005|route POST /v1/auth/reset-confirm; request {token,newPassword}; response 200 on success; 400 on weak password; 401 on expired/used/invalid token; invalidates all existing refresh tokens for user; audit event emitted|S|P0|
|6|SEC-RESET-HASH|Reset token hashed-at-rest|Only SHA-256 hash stored in DM-RESET per TDD §13|Infrastructure|DM-RESET|raw token returned only in email link; token_hash column stores SHA256; integration test verifies DB never contains raw token|S|P0|
|7|NFR-COMP-001|SOC2 audit logging full coverage|All auth events (login, register, refresh, reset-request, reset-confirm, lockout) emit to DM-AUDIT with user_id + event + timestamp + IP + outcome, 12-month retention|AuditLogger|DM-AUDIT,OPS-LOG-M1,OPS-LOG-M2|every FR event produces DM-AUDIT row; IP extracted from X-Forwarded-For with trust-proxy config; partitioning strategy documented (monthly partitions); 12-month retention enforced via partition drop job; compliance test asserts SOC2 event catalog coverage|M|P0|
|8|NFR-GDPR-CONSENT|GDPR consent capture at registration|Consent flag + timestamp persisted at /auth/register per NFR-COMP-001|AuthService|DM-001,FR-AUTH-002|registration request includes consent_accepted:bool and consent_version:string; UserProfile extended with consent_accepted_at:timestamptz + consent_version:varchar columns; request fails 400 if consent_accepted!=true; consent text versioned under legal/ with version tag referenced|S|P0|
|9|NFR-GDPR-MIN|Data minimization enforcement|Only email, password_hash, display_name, consent fields collected at registration per NFR-COMP-001|AuthService|FR-AUTH-002|registration request schema strictly validates allowed fields; additional properties rejected with 400; documentation enumerates collected PII fields for legal review|XS|P0|
|10|OPS-RETENTION|12-month audit retention job|Scheduled PostgreSQL partition-drop for audit log older than 12 months per OQ-M1-002|DevOps|DM-AUDIT|cron job (monthly) drops partitions aged >12 months; backup retention policy documented; runbook entry added; retention window configurable via env var AUDIT_RETENTION_MONTHS (default 12)|S|P0|
|11|METRIC-RESET|Password-reset counters|`auth_reset_request_total` and `auth_reset_confirm_total` counters|Observability|API-RESET-REQ,API-RESET-CONF|prometheus counters with outcome labels; emitted on every request/confirm attempt|XS|P1|
|12|TEST-RESET-UNIT|Unit — password reset request generates single-use token|Covers FR-AUTH-005 AC1-4|Testing|FR-AUTH-005|jest test mocks EmailService and DM-RESET; asserts token expiry 1 hour; asserts used_at set on confirm; asserts re-use returns 401|S|P0|
|13|TEST-RESET-INT|Integration — reset flow end-to-end against real Postgres|Supertest + testcontainer Postgres|Testing|FR-AUTH-005,API-RESET-REQ,API-RESET-CONF|POST /reset-request → read token from DM-RESET (bypassing email) → POST /reset-confirm → login with new password succeeds; refresh tokens previously issued are rejected|S|P0|
|14|TEST-COMPLIANCE|Compliance test — SOC2 event catalog coverage|Automated check that every FR event class emits a DM-AUDIT row|Testing|NFR-COMP-001|test driver exercises login (success/fail), register, refresh (success/fail), reset (request/confirm), lockout; asserts corresponding DM-AUDIT rows exist with required fields|S|P0|

### Integration Points — M3

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|EmailService|Dependency injection|M3 (AuthService constructor-injects for reset flow)|M3|AuthService reset-request handler|
|AuditLogger|Event emitter (pub-sub style)|M3 (subscribed to AuthService events)|M3|DM-AUDIT persistence|
|ResetTokenRepo|Dependency injection|M3 (AuthService constructor-injects)|M3|AuthService reset-request, reset-confirm|
|Audit retention cron|Scheduled job binding|M3 (cron entry installed)|M3|DM-AUDIT partition maintenance|

### Milestone Dependencies — M3

- M2 complete: TokenManager and audit-event emission available so reset-confirm can revoke all active refresh tokens for a user.
- SendGrid account provisioned with API key in secrets mount.
- Legal/compliance review of GDPR consent text complete with version tag.

### Open Questions — M3

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-M3-001 (from PRD OQ-PRD-1)|Password reset emails sent synchronously (block response until delivered) vs asynchronously (queue + retry)?|Affects p95 latency of POST /reset-request and user-perceived delivery reliability|eng-manager, auth-team|2026-05-21|
|2|OQ-M3-002 (closed — TDD vs PRD retention conflict)|TDD §7.2 states 90-day audit retention; PRD / SOC2 / NFR-COMP-001 require 12 months. STATUS: closed. RESOLUTION: compliance authority > TDD design default → committed 12-month retention across DM-AUDIT, OPS-RETENTION, Timeline, Success Criteria. TDD §7.2 must be updated.|Committed to 12 months; no schedule impact; TDD doc update follow-up tracked separately|sec-reviewer|2026-04-22 (closed)|

### Risk Assessment and Mitigation — M3

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-PRD-003 Email delivery failure blocks password reset|MEDIUM|MEDIUM|Users cannot recover accounts without support ticket|SendGrid delivery monitoring + alert on bounce rate >2%; fallback documented in OPS-003 runbook; retry with exponential backoff on 5xx responses|auth-team|
|2|R-PRD-002 Compliance failure from incomplete audit logging|HIGH|MEDIUM|SOC2 audit finding|NFR-COMP-001 covers all FR events; TEST-COMPLIANCE enforces catalog in CI; sec-reviewer sign-off before M5 GA|sec-reviewer|
|3|R-M3-ENUM User enumeration via reset-request timing or response|MEDIUM|LOW|Attacker determines which emails are registered|/reset-request always returns 200 with constant-time response; do not branch on email existence until after async token generation step; test asserts timing ±20ms between registered and unregistered email paths|sec-reviewer|

## M4: Frontend Integration — LoginPage, RegisterPage, AuthProvider

**Objective:** Build the React routes and components (`LoginPage`, `RegisterPage`, `ProfilePage`) plus the `AuthProvider` context that manages `AuthToken` state, silent refresh, 401 interception, and XSS-mitigation token storage (access in memory, refresh in HttpOnly cookie). | **Duration:** 2 weeks (2026-06-01 → 2026-06-15, overlapping M5 setup) | **Entry:** M1, M2, M3 endpoints live behind flags and passing integration tests. | **Exit:** E2E test TEST-006 passes (register → login → profile); silent refresh verified with 15-minute access TTL; no accessToken persisted to localStorage; refreshToken delivered exclusively via HttpOnly cookie; AUTH_NEW_LOGIN flag still OFF in production.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|COMP-001|Route `/login` → LoginPage binding|Route registration per TDD §10.1|Frontend|COMP-004|react-router route `/login` mapped to LoginPage; no auth required; redirect to `/profile` if already authenticated via AuthProvider|XS|P0|
|2|COMP-002|Route `/register` → RegisterPage binding|Route registration per TDD §10.1|Frontend|COMP-005|react-router route `/register` mapped to RegisterPage; no auth required; redirect to `/profile` if already authenticated|XS|P0|
|3|COMP-003|Route `/profile` → ProfilePage binding|Route registration per TDD §10.1; auth required|Frontend|COMP-006,API-003|react-router protected route `/profile` mapped to ProfilePage; unauthenticated access redirects to `/login` via AuthProvider guard|S|P0|
|4|COMP-004|LoginPage component|Email/password login form per TDD §10.2|Frontend|API-001,COMP-006|props: onSuccess: ()=>void, redirectUrl?: string; renders email + password fields with inline validation; submits to POST /auth/login via AuthService client; stores returned AuthToken via AuthProvider; shows generic error on 401 (no enumeration); a11y labels on all inputs|M|P0|
|5|COMP-005|RegisterPage component|Registration form per TDD §10.2|Frontend|API-002,COMP-006,NFR-GDPR-CONSENT|props: onSuccess: ()=>void, termsUrl: string; renders email + password + displayName + GDPR consent checkbox; client-side password strength validation (<8 chars / no uppercase / no number rejected pre-submit); submits to /auth/register; shows 409 duplicate-email error; links to termsUrl|M|P0|
|6|COMP-006|AuthProvider context provider|Token state + silent refresh + 401 interception per TDD §10.2|Frontend|API-004|React Context provider exposing {userProfile, isAuthenticated, login(), logout(), register()}; stores accessToken in memory only (React state, NEVER localStorage/sessionStorage); reads refreshToken via HttpOnly cookie only; axios/fetch interceptor catches 401 and attempts silent refresh once; on refresh failure redirects to /login; clears tokens on tab close (beforeunload)|L|P0|
|7|SEC-HTTPONLY|RefreshToken HttpOnly cookie delivery|Backend cookie flags per TDD §13 (R-001 mitigation)|Backend|API-001,API-004|POST /auth/login response sets refreshToken as HttpOnly; Secure; SameSite=Strict cookie; response body returns only accessToken + expiresIn + tokenType (NOT refreshToken); /auth/refresh reads cookie instead of body in production (body accepted only when feature-flagged OFF for legacy migration)|M|P0|
|8|SEC-MEMSTORE|AccessToken in-memory storage enforcement|AuthProvider never persists accessToken to storage|Frontend|COMP-006|code review checklist item; automated lint rule rejects localStorage/sessionStorage set of "accessToken" key; unit test asserts AuthProvider state cleared on unmount and on beforeunload event|S|P0|
|9|FEAT-SILENTREF|Silent refresh scheduler|Refresh accessToken ~1 min before 15-min expiry|Frontend|COMP-006,API-004|AuthProvider schedules refresh at expiresIn-60 seconds after each token issuance; cancels on logout; deduplicates concurrent refresh attempts; verified via E2E test waiting 14 min and observing refresh call in network log|M|P0|
|10|FEAT-401INT|401 response interceptor|HTTP client interceptor triggers silent refresh then retries|Frontend|COMP-006|single retry attempt per 401; on retry failure propagates to caller as AuthError; logs-out user and redirects to /login via router|S|P0|
|11|UI-ERR|Client-side error UX|Generic login error, specific registration errors, clear lockout message|Frontend|COMP-004,COMP-005|LoginPage renders "Invalid email or password" on 401 (no user enumeration); 423 Locked renders "Account temporarily locked — try again in 15 minutes"; RegisterPage renders field-specific errors from 400 response|S|P1|
|12|UI-A11Y|Accessibility baseline for auth pages|Keyboard navigation + ARIA labels + visible focus|Frontend|COMP-004,COMP-005,COMP-003|axe-core scan passes with zero serious/critical violations; tab order tested; visible focus ring; form field labels programmatically associated|S|P1|
|13|TEST-006|E2E — user registers and logs in|Playwright flow RegisterPage → LoginPage → ProfilePage per TDD §15.2|Testing|COMP-004,COMP-005,COMP-006,API-003|playwright test navigates /register, fills form, submits, redirects to /login, logs in, reaches /profile with user details displayed; validates FR-AUTH-001, FR-AUTH-002, FR-AUTH-004|M|P0|
|14|TEST-E2E-REFRESH|E2E — silent refresh maintains session|Playwright fast-forward or 16-min wait|Testing|FEAT-SILENTREF|playwright test with clock-override extension advances 14 min; asserts network log shows /auth/refresh call and new access token used; session not interrupted|S|P0|
|15|TEST-E2E-LOGOUT|E2E — logout clears tokens and redirects|Playwright|Testing|COMP-006|test asserts logout() call clears AuthProvider state; navigates to /login; protected /profile redirects to /login; no accessToken in memory per devtools inspection|S|P1|
|16|FUNNEL-REG|Registration-conversion funnel instrumentation|Analytics events at landing→form→submitted→confirmed per PRD success metric target >60%|Frontend|COMP-005|analytics events registration_viewed, registration_started, registration_submitted, registration_confirmed emitted with user_id + session_id; target tracked in product dashboard as part of SUCC-PRD-REG|S|P1|

### Integration Points — M4

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|AuthProvider (React Context)|Context injection|M4 (wraps <App/>)|M4|LoginPage, RegisterPage, ProfilePage, any protected route|
|Axios/Fetch 401 interceptor|HTTP client middleware|M4 (installed at AuthProvider boot)|M4|all authenticated HTTP calls|
|React Router protected-route guard|Router middleware|M4 (wraps <ProtectedRoute/>)|M4|/profile and future authenticated routes|
|Silent-refresh scheduler|Timer binding|M4 (setTimeout lifecycle in AuthProvider)|M4|implicit for every token-issuance event|
|HttpOnly refresh-cookie server config|Backend cookie-setter|M4 (modifies M1 login response)|M4|browser cookie jar; /auth/refresh cookie read|

### Milestone Dependencies — M4

- M1/M2/M3 endpoints live behind flags and passing integration tests.
- Frontend routing framework (e.g., React Router) provisioned per PRD Assumptions.
- Design system components (Input, Button, Form) available in the shared UI library.

### Open Questions — M4

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-M4-001 (JTBD gap-fill from PRD)|PRD AUTH-E1 user story "logout" implies POST /auth/logout endpoint that invalidates the active refresh token. TDD does not specify a dedicated logout endpoint — logout today is client-side clear of state only. STATUS: open. PROPOSAL: add POST /auth/logout calling TokenManager.revoke(currentRefresh); RESOLUTION: PRD requires; TDD should be updated. Do NOT add OQ as deliverable row; if approved, a new deliverable will be added in M4 or M5.|Without server-side revocation, a stolen refresh token remains valid until TTL expires|product-manager, auth-team|2026-05-28|
|2|OQ-M4-002|"Remember-me" extension (from OQ-M2-002) — if approved, affects AuthProvider session-persistence UX and adds a checkbox to LoginPage.|Frontend scope expansion; affects COMP-004 and COMP-006|product-manager|2026-05-28|

### Risk Assessment and Mitigation — M4

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-001 Token theft via XSS allows session hijacking|HIGH|MEDIUM|Attacker steals accessToken and impersonates user|SEC-MEMSTORE enforces accessToken in memory only; SEC-HTTPONLY sets HttpOnly+Secure+SameSite=Strict on refreshToken cookie; SEC-RT-HASH (M2) ensures Redis-at-rest is hashed; TokenManager.revoke available for incident response; frontend CSP header restricts inline scripts|sec-reviewer|
|2|R-PRD-001 Low registration adoption due to poor UX|MEDIUM-HIGH|MEDIUM|PRD conversion target >60% missed|FUNNEL-REG instruments the funnel before GA; usability test with 5+ end users before Phase 1 Alpha; iterate on inline validation copy|product-manager|
|3|R-M4-ROUTER Protected-route redirect loop under token expiry|MEDIUM|LOW|AuthProvider interceptor loops /auth/refresh → 401 → refresh → 401|FEAT-401INT limits retry to 1 per 401; TEST-E2E-REFRESH covers happy path; runbook OPS-002 (from M5) covers the failure mode|auth-team|

## M5: Production Readiness — Rollout, Observability, Operations

**Objective:** Execute the three-phase rollout (MIG-001 Alpha → MIG-002 10% Beta → MIG-003 GA 100%), close the observability surface (metrics, tracing, alerts, runbooks), lock in capacity plan, and deliver the automated rollback triggers defined in the TDD as automatic conditions. | **Duration:** 2 weeks (2026-06-01 → 2026-06-16; MIG-003 GA checkpoint on 2026-06-09 per TDD) | **Entry:** M1–M4 complete; staging smoke-tests green; monitoring dashboards provisioned. | **Exit:** 99.9% uptime sustained over first 7 days post-GA; all alerts firing to correct channels; feature flags `AUTH_NEW_LOGIN` removed; `AUTH_TOKEN_REFRESH` scheduled for removal 2 weeks post-GA; post-mortem template ready; on-call rotation active.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|MIG-001|Phase 1 Internal Alpha (1 week)|Deploy AuthService to staging; auth-team + QA validate all endpoints; AUTH_NEW_LOGIN behind flag|DevOps|M1,M2,M3,M4|service deployed to staging namespace; all FR-AUTH-001..005 pass manual test pass; zero P0/P1 bugs open; sign-off from test-lead + sec-reviewer; duration 1 week|M|P0|
|2|MIG-002|Phase 2 Beta 10% traffic (2 weeks)|Enable AUTH_NEW_LOGIN for 10% traffic; monitor latency, error rate, Redis usage|DevOps|MIG-001|10% weighted routing at API Gateway; monitoring p95 <200ms sustained; error rate <0.1% sustained; zero TokenManager Redis connection failures over 2 weeks; AuthProvider silent refresh verified under real load|M|P0|
|3|MIG-003|Phase 3 GA 100% (1 week)|Remove AUTH_NEW_LOGIN flag; all traffic on new service; legacy endpoints deprecated; AUTH_TOKEN_REFRESH enabled|DevOps|MIG-002|100% routing to new AuthService; legacy /auth routes return 410 Gone; AUTH_TOKEN_REFRESH=ON for all traffic; 99.9% uptime over first 7 days; all monitoring dashboards green|M|P0|
|4|FEAT-FLAG-NEWLOGIN|AUTH_NEW_LOGIN feature flag lifecycle|Flag gating new login stack per TDD §19.2|Infrastructure|M1|default OFF; removable from code 7 days after MIG-003 GA (removal target 2026-06-16); flag documented in feature-flag registry with owner + removal date|S|P0|
|5|FEAT-FLAG-REFRESH|AUTH_TOKEN_REFRESH flag lifecycle|Flag gating refresh flow per TDD §19.2|Infrastructure|M2|default OFF until MIG-003; ON at GA; removable 14 days after Phase 3 GA (removal target 2026-06-23); registry-tracked|S|P0|
|6|OPS-001|Runbook — AuthService down|Symptoms/diagnosis/resolution per TDD §25.1|DevOps|M1,M2|runbook in docs/runbooks/auth-service-down.md; covers 5xx on /auth/*; pod health + Postgres + PasswordHasher/TokenManager init log diagnosis; restart pods, failover Postgres replica, Redis-down handling; escalation auth-team on-call → platform-team after 15min; ack within 15 min for P1|S|P0|
|7|OPS-002|Runbook — token refresh failures|Symptoms/diagnosis/resolution per TDD §25.1|DevOps|M2,M4|runbook covers AuthProvider redirect loops + auth_token_refresh_total error spikes; Redis connectivity + JwtService key + AUTH_TOKEN_REFRESH flag diagnosis; scale Redis, remount secrets, enable flag; escalation path documented|S|P0|
|8|OPS-003|On-call rotation and expectations|24/7 auth-team rotation for first 2 weeks post-GA per TDD §25.2|DevOps|MIG-003|PagerDuty schedule committed; P1 ack <15 min; tooling access (k8s dashboard, Grafana, Redis CLI, Postgres admin); escalation: on-call → test-lead → eng-manager → platform-team|S|P0|
|9|OPS-004|Observability baseline|Structured logs + prometheus metrics + OTEL spans + alerts per TDD §14 and §25.4|Observability|M1,M2,M3,M4|structured JSON logs for login/register/refresh/reset (password+tokens redacted); prometheus metrics auth_login_total, auth_login_duration_seconds, auth_token_refresh_total, auth_registration_total (all wired via METRIC-* deliverables); OTEL spans AuthService→PasswordHasher→TokenManager→JwtService; Grafana dashboard published|M|P0|
|10|OPS-005|Capacity plan provisioning|3 replicas baseline with HPA to 10 per TDD §25.3|DevOps|M1|Kubernetes Deployment replicas=3; HPA minReplicas=3, maxReplicas=10, targetCPUUtilizationPercentage=70; PostgreSQL pool=100 with 200-ceiling runbook trigger at connection wait >50ms; Redis baseline 1GB with 2GB scale trigger at >70% utilization|S|P0|
|11|ALERT-LOGIN-FAIL|Alert — login failure rate >20% over 5 min|Per TDD §14 alert list|Observability|OPS-004,METRIC-LOGIN|prometheus alert rule `rate(auth_login_total{outcome="invalid"}[5m]) / rate(auth_login_total[5m]) > 0.2` for 5m; routes to auth-team on-call|XS|P0|
|12|ALERT-LATENCY|Alert — p95 latency >500ms|Per TDD §14|Observability|NFR-PERF-001|alert rule `histogram_quantile(0.95, auth_login_duration_seconds) > 0.500 for 5m`; pages auth-team|XS|P0|
|13|ALERT-REDIS|Alert — TokenManager Redis connection failures|Per TDD §14|Observability|COMP-TOKMGR|alert rule on metric `auth_redis_connection_failures_total` rate >0 for 5m; pages platform-team|XS|P0|
|14|ROLLBACK-AUTO-LATENCY|Automated rollback trigger — p95 >1000ms for >5 min|Per TDD §19.4 rollback criterion|DevOps|MIG-002,ALERT-LATENCY|automation watches `histogram_quantile(0.95, auth_login_duration_seconds) > 1.0 for 5m`; triggers AUTH_NEW_LOGIN=OFF automatically; PagerDuty incident created; runbook step 1 (flag disable) automated; remaining steps human-gated|M|P0|
|15|ROLLBACK-AUTO-ERR|Automated rollback trigger — error rate >5% for >2 min|Per TDD §19.4|DevOps|MIG-002|automation watches 5xx rate; triggers flag-off + incident; independent from ROLLBACK-AUTO-LATENCY so either can fire alone|S|P0|
|16|ROLLBACK-AUTO-REDIS|Automated rollback trigger — TokenManager Redis failures >10/min|Per TDD §19.4|DevOps|MIG-002,ALERT-REDIS|automation watches auth_redis_connection_failures_total rate >10/min; triggers flag-off + incident|S|P0|
|17|ROLLBACK-AUTO-DATA|Automated rollback trigger — UserProfile data loss/corruption detected|Per TDD §19.4|DevOps|MIG-002|integrity check job compares row counts + checksum against pre-phase snapshot at 5-min interval; any delta triggers automated flag-off + escalation to sec-reviewer + platform-team; restore-from-backup step human-gated|M|P0|
|18|ROLLBACK-STEPS|Rollback procedure checklist (6 ordered steps)|Per TDD §19.3 ordered sequence|DevOps|MIG-001,MIG-002,MIG-003|runbook checklist executes in source order: (1) disable AUTH_NEW_LOGIN flag; (2) verify legacy login via smoke tests; (3) investigate root cause via structured logs/traces; (4) if UserProfile corruption, restore from last known-good backup; (5) notify auth-team + platform-team via incident channel; (6) post-mortem within 48 hours; every step has an owner field; SLA: post-mortem within 48h|M|P0|
|19|NFR-REL-001|99.9% uptime SLO instrumentation|Uptime monitored over 30-day rolling windows per NFR-REL-001|Observability|OPS-004|blackbox-exporter probes `/health` every 30s from 3 regions; error budget tracked in Grafana; alert at 99.5% availability (budget burn-rate); SLO doc published|S|P0|
|20|SUCC-SLO-BOARD|Success-criteria dashboard|Grafana dashboard binding every numeric success target to a panel|Observability|OPS-004,NFR-PERF-001,NFR-PERF-003,NFR-REL-001|dashboard panels: login p95 <200ms, refresh p95 <100ms, registration success >99%, availability 99.9%, PasswordHasher.hash <500ms, concurrent 500 users sustained, registration conversion >60%, DAU >1000 within 30d, unit coverage ≥80%, session duration >30 min, failed login <5%, reset completion >80%; each panel has source metric and threshold line|M|P0|

### Integration Points — M5

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|AUTH_NEW_LOGIN flag|Gateway routing config|M5 (traffic split 10% then 100%)|M5|API Gateway weighted routing|
|AUTH_TOKEN_REFRESH flag|Runtime feature flag|M5 (toggled during MIG-003)|M5|/auth/refresh route handler|
|Prometheus scrape targets|Discovery binding|M5 (ServiceMonitor CRD)|M5|Prometheus, Grafana, alertmanager|
|Automated rollback watchers|Event binding (alert → webhook)|M5 (alertmanager → rollback-controller)|M5|feature-flag service, PagerDuty|
|Audit-log retention cron|Scheduled job|M3 (installed) / M5 (verified in prod)|M5|DM-AUDIT partition maintenance|
|HPA policy|Kubernetes controller|M5 (HPA CRD applied)|M5|AuthService Deployment|

### Milestone Dependencies — M5

- M1–M4 complete with integration + E2E tests green.
- Staging environment mirrors production topology (PostgreSQL replica + Redis cluster + API Gateway).
- PagerDuty / alerting provider configured with auth-team + platform-team routing.
- Backup and restore procedures tested in staging with production-like dataset.

### Open Questions — M5

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-M5-001 (from TDD OQ-001)|Should AuthService support API key authentication for service-to-service calls? STATUS: closed. RESOLUTION: deferred to v1.1 per TDD Non-Goal NG — out of scope for v1.0; do not relitigate; v1.1 roadmap slot reserved.|Locked — no impact on v1.0 GA|test-lead|2026-04-15 (closed, deferred to v1.1)|
|2|OQ-M5-002 (from PRD Jordan persona + JTBD admin)|Admin-visible auth event log UI / query tool — PRD Jordan persona expects queryable audit logs. For v1.0 GA, raw SQL access to auth_audit_log is sufficient; a dedicated admin UI is deferred. STATUS: open. PROPOSAL: mark admin UI as v1.1 scope; document raw-SQL query guide in OPS-003 runbook appendix.|Without a UI, admins depend on DB access; acceptable for internal admin use at GA|product-manager, auth-team|2026-06-02|

### Risk Assessment and Mitigation — M5

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-003 Data loss during migration from legacy auth|HIGH|LOW|UserProfile corruption or orphaned accounts|Parallel run through MIG-001/002; idempotent upsert on migration script; pre-phase PostgreSQL backups; ROLLBACK-AUTO-DATA integrity check; rollback step 4 restores from backup|auth-team|
|2|R-M5-ROLLOUT Rollout beyond 10% destabilizes under real traffic|HIGH|MEDIUM|Latency/error spikes visible to real users|MIG-002 holds 10% for 2 weeks with p95 + error + Redis watch; automated rollback triggers (ROLLBACK-AUTO-*) disable AUTH_NEW_LOGIN within minutes; runbook ROLLBACK-STEPS executed|platform-team|
|3|R-M5-ALERT Alerts mis-route or swallow incidents|MEDIUM|LOW|Delayed response to P1s; SLO breach|Alert-routing tests before MIG-001; on-call drills during MIG-001; OPS-003 rotation verified|platform-team|
|4|R-PRD-003 Email delivery failure blocks password reset|MEDIUM|MEDIUM|Users cannot self-recover at GA|SendGrid delivery-rate alert (>2% bounce); OPS-003 escalation includes SendGrid ticket path; fallback support channel documented|auth-team|

## Resource Requirements and Dependencies

### External Dependencies

|Dependency|Required By Milestone|Status|Fallback|
|---|---|---|---|
|PostgreSQL 15+ (INFRA-DB-001)|M1|Assumed provisioned per PRD Assumptions|Managed PostgreSQL (AWS RDS / GCP Cloud SQL) fallback; local Docker Compose for dev|
|Redis 7+|M1 (lockout), M2 (refresh tokens)|Provisioning tracked|Fall back to in-process cache for lockout (lossy); refresh flow cannot fall back and must block until Redis healthy|
|Node.js 20 LTS runtime|M1|Official images available|Pin to 20.x LTS line; 22.x not certified|
|bcryptjs library|M1|npm public|None; core security dependency|
|jsonwebtoken library|M2|npm public|jose as alternate; requires JwtService rewrite|
|SendGrid API|M3|Account provisioned per PRD Assumptions|AWS SES as fallback email provider; EmailService adapter covers swap|
|API Gateway (rate limiting, CORS, routing)|M1, M5|Platform-team owned|Nginx ingress as fallback with Lua rate-limit module|
|SEC-POLICY-001 (password + token policy)|M1|Drafted; approval tracked via OQ-M1-003|Cannot start M1 without; blocking|
|Kubernetes + HPA + Prometheus + Grafana + alertmanager|M5|Platform-provided|No fallback — platform standard|
|PagerDuty (on-call rotation)|M5|Org standard|OpsGenie alternative per org policy|

### Infrastructure Requirements

- AuthService: 3 Kubernetes pod replicas baseline, HPA to 10 replicas at CPU >70% (per OPS-005 / TDD §25.3). Target: 500 concurrent login requests sustained under <200ms p95.
- PostgreSQL 15+: 100-connection pool, raise to 200 if connection wait >50ms. Storage plan includes audit-log monthly partitions with 12-month retention and pre-phase backups before each rollout phase.
- Redis 7+: 1 GB baseline (~100K refresh tokens ≈ 50 MB); scale to 2 GB at >70% utilization. HA replica required to survive single-node failure without forcing mass re-login.
- Secrets management: RSA 2048-bit private key (RS256) and SendGrid API key delivered via Kubernetes Secrets (or equivalent KMS-backed mount).
- Observability stack: Prometheus scrape configured for AuthService pods, Grafana dashboards published, alertmanager wired to PagerDuty with auth-team and platform-team routing keys.
- Cost envelope ~$450/month at initial GA (per TDD §26): ~$150 compute (3 pods), ~$200 managed PostgreSQL, ~$100 managed Redis; scales linearly with user growth (~$50/month per 10K additional users).

## Risk Register

|ID|Risk|Affected Milestones|Probability|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|R-001|Token theft via XSS enables session hijacking|M2, M4|Medium|High|accessToken in memory only (SEC-MEMSTORE); refreshToken HttpOnly+Secure+SameSite=Strict cookie (SEC-HTTPONLY); Redis-at-rest refresh hash (SEC-RT-HASH); 15-min access TTL; TokenManager.revoke for incident response; frontend CSP|sec-reviewer|
|R-002|Brute-force attacks on login endpoint|M1, M5|High|Medium|API Gateway rate limit 10/min per IP; FEAT-LOCK 5-failure/15-min lockout; bcrypt cost 12; WAF + CAPTCHA planned as M5 contingency|sec-reviewer|
|R-003|Data loss during migration from legacy auth|M1, M5|Low|High|Pre-phase PostgreSQL backups; idempotent upsert migration; parallel legacy run during MIG-001/002; ROLLBACK-AUTO-DATA integrity check; restore-from-backup in ROLLBACK-STEPS|auth-team|
|R-PRD-001|Low registration adoption due to poor UX|M4, M5|Medium|Medium-High|FUNNEL-REG instruments conversion funnel; usability testing before MIG-001; iterate inline validation copy; monitor >60% conversion target post-GA|product-manager|
|R-PRD-002|Compliance failure from incomplete audit logging|M1, M3, M5|Medium|High|DM-AUDIT lands M1; NFR-COMP-001 covers all FR events in M3; TEST-COMPLIANCE CI check; 12-month retention via OPS-RETENTION; sec-reviewer sign-off gate before GA|sec-reviewer|
|R-PRD-003|Email delivery failure blocking password reset|M3, M5|Medium|Medium|SendGrid delivery monitoring with >2% bounce alert; retry with backoff; fallback support channel; SES as backup provider|auth-team|
|R-M1-SCHED|M1 start slipped past TDD target 2026-04-14|M1, M2, M3, M4, M5|Certain (occurred)|High|Compressed M1 to 2 weeks from 2026-04-20; OQ-M1-001 tracks decision; weekly burn-down review with eng-manager|test-lead|
|R-M2-KEY|JwtService signing-key rotation breaks existing tokens|M2, M5|Medium|Medium|Dual-key verification window during rotation; kid-based lookup; rotation runbook; quarterly rotation scheduled|auth-team|
|R-M2-REDIS|Redis unavailability blocks refresh and lockout|M2, M5|Low|High|TokenManager fails closed on Redis loss; AuthProvider surfaces clear UX (M4); Redis HA replica; alert on connection failures >10/min; ROLLBACK-AUTO-REDIS automated trigger|platform-team|
|R-M3-ENUM|User enumeration via /reset-request timing or response|M3|Low|Medium|Constant-time response; /reset-request always 200; timing test ±20ms between registered/unregistered paths|sec-reviewer|
|R-M4-ROUTER|Protected-route redirect loop under token expiry|M4|Low|Medium|FEAT-401INT single-retry limit; TEST-E2E-REFRESH covers happy path; OPS-002 runbook covers failure mode|auth-team|
|R-M5-ROLLOUT|Rollout beyond 10% destabilizes under real traffic|M5|Medium|High|MIG-002 holds 10% for 2 weeks with p95 + error + Redis watch; automated rollback triggers disable flag within minutes; ROLLBACK-STEPS executed|platform-team|
|R-M5-ALERT|Alerts mis-route or swallow incidents|M5|Low|Medium|Alert-routing tests before MIG-001; on-call drills during MIG-001; OPS-003 rotation verified|platform-team|

## Success Criteria and Validation Approach

|Criterion|Metric|Target|Validation Method|MLS|
|---|---|---|---|---|
|Login response latency|auth_login_duration_seconds p95|< 200ms|APM tracing on AuthService.login; SUCC-SLO-BOARD panel|M1, M5|
|Registration success rate|auth_registration_total{outcome=success} / total|> 99%|Ratio of successful to attempted registrations in prometheus|M1, M5|
|Token refresh latency|auth_token_refresh_duration_seconds p95|< 100ms|APM tracing on TokenManager.refresh; SUCC-SLO-BOARD panel|M2, M5|
|Service availability|Blackbox-probe success rate (30-day rolling)|99.9%|NFR-REL-001 blackbox exporter + SLO error budget|M5|
|Password hash time|PasswordHasher.hash() benchmark|< 500ms (bcrypt cost 12)|Benchmark in CI against target hardware|M1|
|Registration conversion|Funnel landing → confirmed|> 60%|FUNNEL-REG analytics events|M4, M5|
|Daily active authenticated users|Distinct user_id in auth_login_total{outcome=success} / day|> 1000 within 30 days of GA|Prometheus + product analytics|M5|
|Unit test coverage|AuthService + TokenManager + JwtService + PasswordHasher|≥ 80%|Jest coverage report in CI gate|M1–M5|
|Concurrent-user sustained load|500 concurrent login users under <200ms p95|Pass k6 load profile|NFR-PERF-002 k6 script|M1|
|Failed login rate|auth_login_total{outcome=invalid} / total|< 5%|Prometheus + SUCC-SLO-BOARD|M5|
|Average session duration|Token-refresh event analytics|> 30 minutes|Refresh cadence analysis|M5|
|Password reset completion|/reset-confirm success / /reset-request success|> 80%|Funnel analytics|M3, M5|
|SOC2 audit-event catalog coverage|DM-AUDIT row per FR event class|100% coverage|TEST-COMPLIANCE|M3, M5|
|Integration-test pass rate — all 4 endpoints|/auth/login, /auth/register, /auth/me, /auth/refresh|100% pass against real PostgreSQL + Redis|CI integration suite|M2, M3|

## Decision Summary

|Decision|Chosen|Alternatives Considered|Rationale|
|---|---|---|---|
|Session mechanism|JWT access (15-min) + opaque refresh (7-day, Redis)|Server-side cookie sessions|TDD §6.4 cites horizontal-scale requirement; stateless verification enables future service replication without session replication|
|Password hashing algorithm|bcrypt cost 12 via PasswordHasher|argon2id, scrypt|TDD §6.4 + NFR-SEC-001; bcrypt cost 12 fits <500ms hash budget with well-understood security properties and abstraction allows future migration|
|JWT signing algorithm|RS256 with 2048-bit RSA|HS256, ES256|NFR-SEC-002 mandates RS256 2048-bit; enables public-key verification by downstream services without sharing private key|
|Auth system ownership|Self-hosted AuthService|Auth0, Firebase Auth|TDD §21; full control over UserProfile schema, TokenManager behavior, avoids vendor lock-in and SaaS cost|
|API versioning|URL-prefix /v1/auth/*|Header-based (Accept)|TDD §8.4; simpler for clients, cacheable, explicit in logs|
|Audit-log retention|12 months|TDD §7.2 proposed 90 days|PRD NFR-COMP-001 + SOC2 Type II require 12-month retention; precedence rule resolves in favor of compliance authority (OQ-M1-002)|
|Milestone layering|Technical layers (Foundation → Token → Compliance → Frontend → Production)|TDD delivery-theme milestones (flat 5-phase)|Technical layering aligns with dependency graph (DM-001 blocks everything); overlaps with TDD dates via mapping table; preserves TDD GA date 2026-06-09|
|Access-token storage (client)|In-memory only|localStorage, sessionStorage|R-001 mitigation; XSS cannot exfiltrate in-memory React state; paired with HttpOnly refresh cookie|
|Refresh-token client delivery|HttpOnly + Secure + SameSite=Strict cookie|Response body, localStorage|R-001 mitigation; SEC-HTTPONLY makes cookie unreadable from JS, Secure forces TLS, SameSite=Strict eliminates CSRF|
|Rollback-trigger implementation|Automated (watchers fire on metric thresholds)|Human-gated confirmation|TDD §19.4 phrases triggers as automatic conditions; ROLLBACK-AUTO-* match source contract; any human gate would be OQ rather than silent change|

## Timeline Estimates

|Milestone|Duration|Start|End|Key Deliverables|
|---|---|---|---|---|
|M1 Foundation|2 weeks|Week 1 / 2026-04-20|Week 2 / 2026-05-04|DM-001, COMP-AUTHSVC, COMP-PWDHASH, FR-AUTH-001/002, API-001/002, FEAT-LOCK, NFR-SEC-001 / PERF-001/002, DM-AUDIT — aligns with TDD M1 (original target 2026-04-14, compressed per OQ-M1-001)|
|M2 Token Management|2 weeks|Week 3 / 2026-05-04|Week 4 / 2026-05-18|COMP-JWTSVC, COMP-TOKMGR, DM-002, FR-AUTH-003/004, API-003/004, NFR-SEC-002, NFR-PERF-003 (refresh p95 <100ms), SEC-RT-HASH — aligns with TDD M2 (2026-04-28); actual 2026-05-18 reflects compressed M1 carry|
|M3 Password Reset + Compliance|2 weeks|Week 5 / 2026-05-18|Week 6 / 2026-06-01|DM-RESET, COMP-MAILSVC, FR-AUTH-005, API-RESET-REQ / CONF, NFR-COMP-001 (12-month retention), NFR-GDPR-CONSENT / MIN — aligns with TDD M3 (2026-05-12); compressed to preserve GA|
|M4 Frontend Integration|2 weeks|Week 7 / 2026-06-01|Week 8 / 2026-06-15|COMP-001/002/003/004/005/006, SEC-HTTPONLY, SEC-MEMSTORE, FEAT-SILENTREF, FEAT-401INT, TEST-006 — aligns with TDD M4 (2026-05-26)|
|M5 Production Readiness|2 weeks (overlapping M4 final week)|Week 7 / 2026-06-01|Week 9 / 2026-06-16|MIG-001 (Alpha) → MIG-002 (10% Beta) → MIG-003 (GA 100% on 2026-06-09); OPS-001..005, ROLLBACK-AUTO-*, NFR-REL-001, SUCC-SLO-BOARD — GA date 2026-06-09 matches TDD M5|

**Total estimated duration:** 9 calendar weeks from 2026-04-20 through GA on 2026-06-09 (TDD committed date preserved via M4/M5 overlap); rollout stabilization extends to 2026-06-16; feature-flag cleanup (AUTH_TOKEN_REFRESH removal) completes 2026-06-23. Any slip in M1 or M2 that cannot be absorbed in the M4/M5 overlap becomes a new Open Question (rescheduled GA vs further compression) rather than a silent schedule change.






