---
spec_source: "test-tdd-user-auth.compressed.md"
complexity_score: 0.72
complexity_class: HIGH
primary_persona: architect
adversarial: true
base_variant: "A"
variant_scores: "A:78 B:72"
convergence_score: 0.62
---

# User Authentication Service — Project Roadmap

## Executive Summary

A standards-compliant identity layer (AuthService + TokenManager + JwtService + PasswordHasher) delivered in five technically-phased milestones preserving the TDD's 10-week calendar commitment ending 2026-06-09. Architecture is stateless JWT with opaque refresh tokens (Redis-backed, capped at 5 per user), PostgreSQL-persisted UserProfile, bcrypt cost 12 hashing, RS256 2048-bit signing, and staged rollout gated by AUTH_NEW_LOGIN and AUTH_TOKEN_REFRESH feature flags. Layering is Foundation → Token Management → Compliance & Reset → Frontend + Hardening + Admin + Observability → Production Readiness, with gating flags preventing external exposure of partial features at every seam. This plan is the product of an adversarial merge: Variant A (Opus, architect — 78) forms the operational scaffold with compressed-schedule honesty, automated rollback triggers, and distributed hardening; Variant B (Haiku, architect — 72) contributes Jordan-persona admin APIs, logout endpoint, explicit observability block, consent-at-M1 placement, /health endpoint, go/no-go release gate, and CONFLICT-2 surfacing (convergence_score 0.62).

**Business Impact:** Unblocks ~$2.4M projected annual revenue from Q2–Q3 2026 personalization features, closes the SOC2 Type II audit gap before Q3 2026, and addresses the 25% churn-survey signal citing absence of accounts. Targets: >60% registration conversion, >1000 DAU within 30 days of GA, <5% failed-login rate, >30-minute average session duration, >80% password-reset completion. Admin operational readiness (Jordan persona) satisfied at GA via API-008/009/010 + COMP-018/019 rather than raw-SQL access.

**Complexity:** HIGH (0.72) — multi-component backend (AuthService/TokenManager/JwtService/PasswordHasher) with dual persistence (PostgreSQL + Redis), cross-cutting security (bcrypt 12, RS256 2048-bit, TLS 1.3, lockout, CORS), frontend integration surface (LoginPage/RegisterPage/AuthProvider), staged rollout with feature flags, and compliance obligations (SOC2 Type II, GDPR, NIST SP 800-63B).

**Critical path:** DM-001 UserProfile schema → PasswordHasher → AuthService.register/login → TokenManager+JwtService → /auth/me + /auth/refresh → Password Reset + NFR-COMP-001 expansion → AuthProvider silent refresh + logout + admin ops + OBS-001..007 → Phased rollout (Alpha → 10% Beta → GA) gated by OPS-011. Any slip on DM-001 or JWT key provisioning blocks every downstream milestone.

**Key architectural decisions:**

- Stateless JWT (RS256, 2048-bit RSA, quarterly rotation) with 15-min access tokens + opaque refresh tokens (Redis, 7-day TTL, hashed-at-rest, capped at 5 per user per OQ-PRD-2 closure); rejected server-side sessions because horizontal scale across future services requires stateless verification.
- bcrypt cost factor 12 via PasswordHasher abstraction; rejected argon2id/scrypt for battle-tested security properties and fit within <500ms hash target at cost 12.
- URL-versioned REST API (`/v1/auth/*`) with unified error envelope `{error:{code,message,status}}`; rejected third-party (Auth0/Firebase) to retain UserProfile/TokenManager control and avoid vendor lock-in.
- Registration success behavior (CONFLICT-2): return `201 UserProfile` and redirect to login; rejected PRD auto-login because TDD §8.2 defines the endpoint contract and silent forking would break API stability — conversion impact tracked in M4 funnel metrics.
- Password-reset email dispatch: asynchronous with immediate generic confirmation (OQ-PRD-1 closure); rejected synchronous because it would breach NFR-PERF-001 latency budget and expose enumeration via timing.
- Admin operational surface (API-008/009/010 + COMP-018/019) and logout (API-007 + COMP-016) ship at GA, not v1.1; Jordan persona and SOC2 incident-response readiness are GA-blocking per PRD S7/S17.
- Rollback triggers implemented as automated conditions (ROLLBACK-AUTO-LATENCY/ERR/REDIS/DATA) per TDD §19.4; rejected human-gated drills because TDD phrases the triggers as automatic conditions and any human gate would silently weaken the contract.

**Open risks requiring resolution before M1:**

- OQ-M1-001 (TDD schedule overshoot): M1 TDD target 2026-04-14 has already passed (today 2026-04-20); committed default now runs 2026-04-20 → 2026-05-04 with compressed Phase 2/3 windows to preserve TDD end date 2026-06-09.
- OQ-M1-002 (audit-log retention conflict): TDD §7.2 states 90-day retention; PRD S17 (derived NFR-COMP-001) and SOC2 require 12 months. Precedence rule: compliance authority > TDD design default → committed 12-month retention applied consistently across DM-AUDIT, OPS-RETENTION, Timeline, Success Criteria. TDD §7.2 must be updated.
- OQ-M1-003 (JWT RSA key custody): 2048-bit RS256 key provisioning and quarterly-rotation procedure must be signed off by sec-reviewer before any token is issued.

## Milestone Summary

|ID|Title|Type|Priority|Effort|Dependencies|Deliverables|Risk|
|---|---|---|---|---|---|---|---|
|M1|Foundation: Data Layer, AuthService, Registration, Login, Consent|Backend|P0|L|INFRA-DB-001, SEC-POLICY-001, COMPLIANCE-001|24|HIGH|
|M2|Token Management: Refresh, Profile, JWT|Backend|P0|L|M1|18|HIGH|
|M3|Password Reset, Compliance Expansion & Audit Logging|Backend|P0|M|M1, M2|13|MEDIUM|
|M4|Frontend + Hardening + Admin Ops + Observability|Frontend/Hardening|P0|L|M1, M2, M3|31|HIGH|
|M5|Production Readiness: Rollout, Rollback Automation, Release Gate|DevOps|P0|M|M1, M2, M3, M4|21|HIGH|

## Dependency Graph

```
INFRA-DB-001 (PostgreSQL 15) ─┐
SEC-POLICY-001 ───────────────┤
COMPLIANCE-001 ───────────────┤
Redis 7+ ─────────────────────┤
                              ▼
                             M1 (Foundation + Consent)
                              │  DM-001, DM-AUDIT, PasswordHasher, AuthService,
                              │  /auth/login, /auth/register, lockout,
                              │  NFR-GDPR-CONSENT, COMP-CONSENT-REC
                              ▼
                             M2 (Token Management)
                              │  TokenManager, JwtService, DM-002 (5-token cap),
                              │  /auth/refresh, /auth/me, Redis
                              ▼
                             M3 (Password Reset + Compliance Expansion)
                              │  FR-AUTH-005, SendGrid (async), NFR-COMP-001 coverage,
                              │  data minimization, retention job
                              ▼
                             M4 (Frontend + Hardening + Admin + Observability)
                              │  LoginPage, RegisterPage, AuthProvider, silent refresh,
                              │  XSS mitigation, API-007 logout, COMP-016 LogoutControl,
                              │  API-008/009/010 admin, COMP-018/019, API-011 /health,
                              │  OBS-001..007 observability block
                              ▼
                             M5 (Production Readiness)
                                 MIG-001/002/003, feature flags, ROLLBACK-AUTO-*,
                                 alerts, runbooks, OPS-011 go/no-go gate, GA
```

**TDD ↔ Roadmap milestone mapping:** Roadmap M1↔TDD M1 (2026-04-14 target, overdue — see OQ-M1-001), M2↔TDD M2 (2026-04-28), M3↔TDD M3 (2026-05-12), M4↔TDD M4 + hardening (2026-05-26), M5↔TDD M5 (2026-06-09 GA).

## M1: Foundation — Data Layer, AuthService, Registration, Login, Consent

**Objective:** Stand up PostgreSQL-backed UserProfile persistence, PasswordHasher (bcrypt cost 12), AuthService orchestrator, the two unauthenticated endpoints (/auth/login, /auth/register) with account-lockout protection, DM-AUDIT schema, and GDPR consent capture wiring (moved forward from M3 to avoid late schema migration). | **Duration:** 2 weeks (2026-04-20 → 2026-05-04, compressed to respect TDD M1 2026-04-14 original target) | **Entry:** INFRA-DB-001 PostgreSQL 15 provisioned; SEC-POLICY-001 approved; COMPLIANCE-001 legal consent text versioned; Node.js 20 LTS runtime available. | **Exit:** FR-AUTH-001 and FR-AUTH-002 pass unit + integration tests against real PostgreSQL; `PasswordHasher.hash()` benchmark <500ms at cost 12; /auth/login and /auth/register endpoints behind `AUTH_NEW_LOGIN=OFF` flag; GDPR consent persisted at registration with versioned text; audit schema ready for NFR-COMP-001 expansion in M3.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|DM-001|UserProfile PostgreSQL schema|Create `user_profiles` table with all source fields and indexes per TDD §7.1|PostgreSQL|INFRA-DB-001|id:UUID-PK-NOT-NULL; email:varchar-UNIQUE-NOT-NULL-indexed-lowercased; display_name:varchar-NOT-NULL-2-to-100-chars; password_hash:varchar-NOT-NULL-bcrypt; created_at:timestamptz-NOT-NULL-DEFAULT-now(); updated_at:timestamptz-NOT-NULL-auto-updated-trigger; last_login_at:timestamptz-NULLABLE; roles:text[]-NOT-NULL-DEFAULT-{user}; consent_accepted_at:timestamptz-NULLABLE; consent_version:varchar-NULLABLE; migration file committed; indices verified via \d+|M|P0|
|2|DM-AUDIT|Audit log PostgreSQL schema|Create `auth_audit_log` table for SOC2 Type II event trail per NFR-COMP-001|PostgreSQL|DM-001|id:UUID-PK; user_id:UUID-NULLABLE-FK-user_profiles; event_type:varchar-NOT-NULL-enum(login_success,login_failure,register,reset_request,reset_confirm,token_refresh,logout,lockout,admin_lock,admin_unlock,admin_query); occurred_at:timestamptz-NOT-NULL-DEFAULT-now()-indexed; ip_address:inet; outcome:varchar-NOT-NULL; actor_type:varchar-NOT-NULL-enum(user,admin,system); metadata:jsonb-minimized; retention policy documented as 12 months per OQ-M1-002|S|P0|
|3|COMP-AUTHSVC|AuthService orchestrator class|Implement facade class delegating to PasswordHasher/TokenManager/UserRepo/ConsentRecorder per TDD §6.2|AuthService|DM-001|class AuthService exported from src/services/auth-service.ts; constructor-injects PasswordHasher, UserRepo, TokenManager, ConsentRecorder; methods login(), register(), getProfile() signatures stubbed; TypeScript strict mode clean|M|P0|
|4|COMP-PWDHASH|PasswordHasher component|Bcrypt abstraction with cost factor 12 per NFR-SEC-001|PasswordHasher|—|class PasswordHasher with hash(password) and verify(password, hash) methods; uses bcryptjs with saltRounds=12; unit test asserts cost parameter==12; benchmark <500ms at cost 12 on target hardware|S|P0|
|5|COMP-USERREPO|UserRepo data-access component|PostgreSQL data access layer for UserProfile|UserRepo|DM-001|class UserRepo with findByEmail(), findById(), insert(profile), updateLastLogin(id, ts); pg-pool-based with 100-connection pool; parameterized queries only (no string concat); covered by integration tests against testcontainer|M|P0|
|6|COMP-CONSENT-REC|ConsentRecorder component|Component that records consent evidence during registration and links it to the user + audit trail (pulled forward from M3)|ConsentRecorder|NFR-COMP-001,DM-AUDIT,DM-001|class ConsentRecorder.record(userId, consentVersion, ip, timestamp); writes consent_accepted_at + consent_version to user_profiles; emits DM-AUDIT event_type=register with consent metadata; failure path audited; PII minimization preserved|S|P0|
|7|FR-AUTH-001|Login authentication logic|AuthService.login() validates credentials via PasswordHasher against stored hashes per TDD §5.1|AuthService|COMP-AUTHSVC,COMP-PWDHASH,COMP-USERREPO|valid creds return 200 with AuthToken; invalid creds return 401 generic error; non-existent email returns 401 (no user enumeration); last_login_at updated on success; email normalized to lowercase before lookup|M|P0|
|8|FR-AUTH-002|Registration with validation|AuthService.register() creates UserProfile with email uniqueness + password policy per TDD §5.1 and CONFLICT-2 contract|AuthService|COMP-AUTHSVC,COMP-PWDHASH,COMP-USERREPO,COMP-CONSENT-REC|valid registration returns 201 with UserProfile body (per CONFLICT-2, no auto-login); duplicate email returns 409 Conflict; weak password (<8 chars OR no uppercase OR no number) returns 400 with field errors; password stored as bcrypt hash cost 12; audit event inserted; consent recorded via ConsentRecorder|M|P0|
|9|API-001|POST /auth/login endpoint|REST endpoint binding per TDD §8.2|API|FR-AUTH-001|route registered at POST /v1/auth/login; request schema {email,password}; response 200 AuthToken; error envelope {error:{code,message,status}}; codes AUTH_INVALID_CREDENTIALS, AUTH_ACCOUNT_LOCKED, AUTH_RATE_LIMITED|S|P0|
|10|API-002|POST /auth/register endpoint|REST endpoint binding per TDD §8.2 (CONFLICT-2: 201 redirect-to-login contract)|API|FR-AUTH-002|route registered at POST /v1/auth/register; request schema {email,password,displayName,consentAccepted:bool,consentVersion:string}; response 201 UserProfile (NO tokens issued per CONFLICT-2); error envelope for VALIDATION, DUPLICATE_EMAIL, CONSENT_REQUIRED|S|P0|
|11|FEAT-LOCK|Account lockout enforcement|Lockout after 5 failed attempts within 15 minutes per FR-AUTH-001 AC4 and OQ-PRD-3 closure|AuthService|FR-AUTH-001,DM-AUDIT|failed-attempt counter persisted (Redis key `lockout:{email}` with 15-min sliding window); 5th failure sets lock flag for 15 min auto-unlock; subsequent login attempts return 423 Locked; audit event emitted; unit + integration tests|M|P0|
|12|API-ERR|Unified error envelope middleware|`{error:{code,message,status}}` response shape across all /auth/* endpoints per TDD §8.3|API|—|Express/Fastify error middleware emits envelope; codes enumerated (AUTH_INVALID_CREDENTIALS, AUTH_DUPLICATE_EMAIL, AUTH_RATE_LIMITED, AUTH_ACCOUNT_LOCKED, AUTH_WEAK_PASSWORD, CONSENT_REQUIRED); no stack traces in response body|S|P0|
|13|API-RATE|Rate limiting configuration|API Gateway limits per TDD §8.1: 10/min login per IP, 5/min register per IP|API Gateway|API-001,API-002|gateway config file committed; 429 Too Many Requests returned; Retry-After header set; integration test verifies limits trigger correctly|S|P0|
|14|NFR-SEC-001|bcrypt cost 12 validation test|Unit test enforcing PasswordHasher uses bcrypt with cost factor 12|Testing|COMP-PWDHASH|test asserts bcrypt.getRounds(hash)==12; CI fails if cost factor changes without review|XS|P0|
|15|NFR-SEC-003|Transport and log redaction baseline|Enforce TLS 1.3 at gateway and redact password/token fields at logger layer per TDD §13|DevOps/Logging|API-001,API-002|ingress config enforces TLSv1.3; logger middleware strips fields password,accessToken,refreshToken,resetToken from any structured log record; unit test asserts redacted output|S|P0|
|16|NFR-GDPR-CONSENT|GDPR consent capture at registration|Consent flag + timestamp persisted at /auth/register per NFR-COMP-001 (moved from M3 to M1 per Haiku delta)|AuthService|DM-001,FR-AUTH-002,COMP-CONSENT-REC|registration request includes consent_accepted:bool and consent_version:string; UserProfile consent_accepted_at and consent_version columns populated via ConsentRecorder; request fails 400 CONSENT_REQUIRED if consent_accepted!=true; consent text versioned under legal/ with version tag referenced|S|P0|
|17|NFR-PERF-001|Login endpoint latency instrumentation (p95 <200ms)|Histogram + p95 alert rule wired for AuthService.login per TDD §17 and NFR-PERF-001|Observability|API-001|prometheus histogram `auth_login_duration_seconds` (buckets 0.025,0.05,0.1,0.2,0.5,1,2); OpenTelemetry span `AuthService.login` emitted; alert rule `histogram_quantile(0.95, auth_login_duration_seconds) > 0.200 for 5m` committed|S|P0|
|18|NFR-PERF-002|Concurrent 500-user load profile (k6)|k6 script validating 500 concurrent logins sustain <200ms p95 per NFR-PERF-002 (kept in M1 for early bug-catching per base-selection)|Testing|API-001,NFR-PERF-001|k6 script in tests/load/login.js; VU=500 sustained for 5min; p95<200ms assertion; result artifact published to CI|S|P0|
|19|TEST-001|Unit — login with valid credentials returns AuthToken|Per TDD §15.2|Testing|FR-AUTH-001|jest test mocks PasswordHasher.verify→true, TokenManager.issueTokens; asserts AuthToken shape and call order; covers FR-AUTH-001 AC1|XS|P0|
|20|TEST-002|Unit — login with invalid credentials returns 401|Per TDD §15.2|Testing|FR-AUTH-001|jest test mocks PasswordHasher.verify→false; asserts 401 and no tokens issued; covers FR-AUTH-001 AC2, AC3|XS|P0|
|21|TEST-004|Integration — registration persists UserProfile to database|Per TDD §15.2 using testcontainers|Testing|FR-AUTH-002,DM-001|supertest + testcontainer PostgreSQL; POST /auth/register returns 201 UserProfile (no tokens per CONFLICT-2); SELECT from user_profiles WHERE email=X returns 1 row with bcrypt hash, consent_accepted_at, consent_version populated|S|P0|
|22|OPS-LOG-M1|Structured login/registration logging|stdout JSON logs for login_success/failure and register per OPS-004 (exclude password/tokens)|Observability|FR-AUTH-001,FR-AUTH-002,NFR-SEC-003|pino/winston logger; fields user_id, event, timestamp, ip, outcome; password and accessToken/refreshToken fields redacted; log sampled for load tests|S|P0|
|23|METRIC-REG|Registration counter metric|`auth_registration_total` counter per OPS-004|Observability|FR-AUTH-002|prometheus counter with labels {outcome=success\|duplicate\|validation\|consent_missing}; emitted on every register attempt|XS|P1|
|24|METRIC-LOGIN|Login counter metric|`auth_login_total` counter per OPS-004|Observability|FR-AUTH-001|prometheus counter with labels {outcome=success\|invalid\|locked\|rate_limited}; emitted on every login attempt|XS|P1|

### Integration Points — M1

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|PasswordHasher|Dependency injection|M1 (COMP-AUTHSVC constructor-injects)|M1|AuthService.login, AuthService.register|
|UserRepo|Dependency injection|M1 (COMP-AUTHSVC constructor-injects)|M1|AuthService.login, AuthService.register, future AuthService.getProfile|
|ConsentRecorder|Dependency injection|M1 (COMP-AUTHSVC constructor-injects for register flow)|M1|AuthService.register, NFR-COMP-001 expansion in M3|
|API error middleware|Middleware chain|M1 (registered after routes)|M1|all /auth/* endpoints|
|API Gateway rate-limit policy|Gateway config binding|M1 (deployed before routes)|M1|POST /auth/login, POST /auth/register|
|AuditLog event emitter|Event emitter (pub-sub)|M1 (initial event set: login_success/failure, register, lockout)|M1|DM-AUDIT persistence|

### Milestone Dependencies — M1

- INFRA-DB-001 PostgreSQL 15 provisioned and reachable from service network.
- SEC-POLICY-001 approved (password policy, key custody, lockout policy).
- COMPLIANCE-001 legal/compliance review of GDPR consent text with version tag.
- Node.js 20 LTS runtime images built and published.
- Redis 7 reachable (used by lockout counter; full refresh-token use lands in M2).

### Open Questions — M1

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-M1-001|TDD M1 target 2026-04-14 has passed (today 2026-04-20). Commit to compressed 2026-04-20→2026-05-04 schedule to preserve TDD GA 2026-06-09, or reschedule all downstream milestones? Committed default: compressed schedule.|Blocks every downstream milestone date|test-lead, eng-manager|2026-04-22|
|2|OQ-M1-002|Audit-log retention: TDD §7.2 says 90 days; NFR-COMP-001 / PRD / SOC2 require 12 months. Precedence rule: compliance > design default → committed value 12 months applied to DM-AUDIT, OPS-RETENTION, Timeline, Success Criteria. TDD §7.2 must be updated.|Committed value: 12 months. Determines storage sizing, backup retention, audit coverage.|sec-reviewer, test-lead|2026-04-22|
|3|OQ-M1-003|JWT RSA key custody and quarterly rotation procedure — where are 2048-bit private keys stored and who authorizes rotation?|Blocks M2 token issuance; security audit gate|sec-reviewer|2026-04-28|
|4|OQ-M1-004 (from TDD OQ-002)|Maximum allowed UserProfile.roles array length? STATUS: closed. RESOLUTION: no v1.0 service-level cap; roles:string[] remains contract-only until RBAC design review.|Keeps DM-001 stable without inventing RBAC enforcement in v1.0.|auth-team|2026-04-22 (closed)|
|5|OQ-M1-005 (from PRD OQ-PRD-3)|Exact lockout policy after N failed attempts? STATUS: closed. RESOLUTION: committed to TDD value 5 attempts / 15 min / 15-min auto-unlock.|Committed value: 5/15min/15-min auto-unlock. Affects FEAT-LOCK acceptance.|sec-reviewer|2026-04-25 (closed)|

### Risk Assessment and Mitigation — M1

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-002 Brute-force attacks on login endpoint|MEDIUM|HIGH|Credential stuffing at scale|API Gateway rate limit 10/min per IP; FEAT-LOCK after 5 failures/15min; bcrypt cost 12 deters offline cracking; WAF + CAPTCHA planned in M5 as contingency|sec-reviewer|
|2|R-003 Data loss during legacy-auth migration|HIGH|LOW|UserProfile corruption or orphaned accounts|Pre-phase PostgreSQL backup; idempotent upsert on migration script; parallel run with legacy until M5 Phase 2|auth-team|
|3|R-M1-SCHED M1 start slipped past TDD target 2026-04-14|HIGH|CERTAIN (already occurred)|Downstream cascade risk to GA 2026-06-09|Compressed M1 to 2 weeks starting 2026-04-20; OQ-M1-001 tracks decision; weekly burn-down review with eng-manager|test-lead|
|4|R-PRD-002 Compliance failure from incomplete audit logging|HIGH|MEDIUM|SOC2 audit finding; legal exposure|DM-AUDIT schema lands in M1 before any event generation; 12-month retention per OQ-M1-002; log schema reviewed by sec-reviewer before M3 expansion; consent recorded at M1 not M3|sec-reviewer|
|5|R-M1-CONSENT Over-collection of user data violates GDPR/NIST minimization|HIGH|MEDIUM|Regulatory exposure; PRD S17 non-compliance|Limit persisted user fields to email, hashed password, display_name, consent metadata; route consent evidence to audit records rather than profile expansion; legal sign-off on DM-001 columns|architect|

## Milestone M2: Token Management (Week 3–4, 2026-05-04 → 2026-05-18)

**Objective**: Issue JWT access + refresh tokens, protect routes via auth middleware, enforce rotation and revocation with Redis-backed storage (≤5 active refresh tokens per user, oldest eviction).
**Duration**: 2 weeks (14 days). Overlaps with M3 by ~5 days for parallelisation.
**Entry Criteria**: M1 exit satisfied; AUTH_NEW_LOGIN flag deployed (0% rollout); Redis 7 reachable; JWT RSA key custody documented (OQ-M1-003 closed).
**Exit Criteria**: Token issuance p95 <100ms; refresh rotation working end-to-end; authMiddleware protects GET /profile; TEST-003 + TEST-005 + TEST-ME green.

### Deliverables — M2

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|DM-002|RefreshToken data model|Entity `RefreshToken` persisted in Redis (hash set keyed by user_id). Fields: token_id:uuid \| user_id:uuid→UserProfile \| token_hash:sha256 \| issued_at:ts \| expires_at:ts \| device_id:string \| revoked:bool. TTL 7 days. Max 5 active tokens/user — oldest evicted on 6th issuance.|DM-002|DM-001|Redis schema migration applied; per-user set capped at 5; automatic eviction verified with integration test|M|P0|
|2|COMP-JWTSVC|JwtService|RS256 signer/verifier using 2048-bit RSA keys. Operations: `sign(payload,ttl)`, `verify(token)`, `getPublicKey()`, `rotateKeys()` (quarterly). Access token TTL 15min; refresh token TTL 7d. Key material loaded from secure key vault referenced by OQ-M1-003 resolution.|COMP-JWTSVC|OQ-M1-003 closed|Valid tokens verify; expired tokens rejected; key rotation preserves existing tokens until TTL expiry|L|P0|
|3|COMP-TOKMGR|TokenManager service|Issues, rotates, and revokes refresh tokens via Redis. Enforces 5-token cap with oldest-eviction. Exposes `issue(user)`, `rotate(old_token)`, `revoke(token)`, `revokeAllForUser(user_id)`. Rotation invalidates old refresh token atomically.|COMP-TOKMGR|COMP-JWTSVC, DM-002|Cap enforced under concurrent issuance (race-safe); rotation prevents replay of old refresh token; all operations idempotent|L|P0|
|4|NFR-SEC-002|Token security requirements|Access tokens: RS256 only, aud+iss claims enforced, no symmetric fallback. Refresh tokens: stored as SHA-256 hash in Redis (never plaintext). Tokens are httpOnly cookies (set in M4). Clock-skew tolerance ±30s.|NFR-SEC-002|COMP-JWTSVC, COMP-TOKMGR|Static analysis confirms no HS256 path; Redis inspection shows hashed tokens; clock-skew negative test passes|M|P0|
|5|FR-AUTH-003|User Login (token issuance path)|TDD §4 / PRD FR-003. Endpoint validates credentials (delegated to AuthService from M1), then issues access+refresh token pair. Success returns `{accessToken, refreshToken, expiresIn}`. Lockout path from FEAT-LOCK still applies.|FR-AUTH-003|COMP-AUTHSVC (M1), COMP-JWTSVC, COMP-TOKMGR|Valid login returns token pair; invalid credentials return 401; locked account returns 423; p95 <200ms|L|P0|
|6|FR-AUTH-004|Token Refresh|TDD §4 / PRD FR-004. POST /auth/refresh accepts refresh token, validates (exists in Redis, not revoked, not expired), issues new access+refresh pair, revokes old refresh token atomically. Replay of old refresh token returns 401 and revokes the entire user's token set (security trigger).|FR-AUTH-004|COMP-TOKMGR|Normal refresh issues new pair; replay of rotated token triggers 401 and family revocation; expired refresh returns 401|M|P0|
|7|API-003|POST /auth/login endpoint|HTTP contract: 200 `{accessToken, refreshToken, expiresIn:900}`, 401 invalid credentials, 423 account locked. Content-Type application/json. Rate-limit 10 req/min per IP (inherited M1).|API-003|FR-AUTH-003|OpenAPI spec published; contract tests green against 200/401/423 cases|M|P0|
|8|API-004|POST /auth/refresh endpoint|HTTP contract: 200 new token pair, 401 invalid/expired/replayed, 429 rate-limited. Rate-limit 30 req/min per token.|API-004|FR-AUTH-004|OpenAPI spec published; replay test returns 401; rate-limit integration test green|M|P0|
|9|COMP-AUTHMW|AuthMiddleware|Express middleware `authMiddleware(req,res,next)`. Extracts bearer token from `Authorization: Bearer` header; validates via JwtService; attaches `req.user`. Applied to GET /profile (TEST-ME fixture) and all protected M3–M4 routes. Returns 401 on invalid/expired token.|COMP-AUTHMW|COMP-JWTSVC|Middleware rejects missing/invalid/expired tokens with 401; valid token populates req.user with sub+roles|M|P0|
|10|FEAT-REFRESH-FLAG|Feature flag AUTH_TOKEN_REFRESH|LaunchDarkly (or equivalent) flag gating new refresh flow in production. Default 0%. Rollout plan lands in M5 OPS-* tasks.|FEAT-REFRESH-FLAG|COMP-AUTHSVC|Flag wired; refresh endpoint short-circuits to legacy path when flag off; override per-user for QA cohort|S|P0|
|11|NFR-PERF-003|Token issuance performance|Token issuance (login path) p95 <100ms measured at service boundary under 100 RPS sustained for 5 minutes. Validated in load-test harness re-used from M1.|NFR-PERF-003|FR-AUTH-003|k6 run records p95 <100ms; report attached to milestone exit review|M|P0|
|12|METRIC-REFRESH|Metrics for refresh flow|Prometheus counters `auth_refresh_success_total`, `auth_refresh_fail_total{reason}`, histogram `auth_refresh_duration_ms`; Grafana panel added to Auth dashboard seeded in M1.|METRIC-REFRESH|COMP-TOKMGR|Panel shows live data from staging; alert threshold placeholder set for M5 ALERT-* tasks|S|P1|
|13|TEST-003|JWT validation test suite|Unit tests for JwtService: valid token verify, expired token, tampered payload, wrong algorithm (HS256 attempt rejection), clock-skew ±30s boundary. Coverage ≥90% on JwtService.|TEST-003|COMP-JWTSVC|Jest suite green; coverage report ≥90%; HS256 attempt yields rejection, not verification|M|P0|
|14|TEST-005|Refresh rotation integration test|Integration test: login → refresh → replay old token → expect 401 + family revocation. Runs against real Redis in test container. Also covers 5-token cap eviction.|TEST-005|FR-AUTH-004, DM-002|Scenario passes end-to-end in CI; Redis hash set shrinks to 5 entries on 6th issue|M|P0|
|15|TEST-ME|GET /profile protected route fixture|Introduces GET /profile gated by authMiddleware. Serves as standing integration test for middleware behaviour before M3 profile feature work.|TEST-ME|COMP-AUTHMW|Valid token returns 200 with profile stub; missing/invalid token returns 401|S|P1|
|16|OPS-LOG-M2|Token-lifecycle audit logs|Extend DM-AUDIT event_type enum with `token_issued`, `token_refreshed`, `token_revoked`, `refresh_replay_detected` (security). Event emitter wired in COMP-TOKMGR paths.|OPS-LOG-M2|DM-AUDIT (M1), COMP-TOKMGR|All four events visible in audit table during integration run; PII-free payload verified|S|P0|
|17|SEC-RT-HASH|Refresh token hashing at rest|SHA-256 of refresh token stored in Redis; plaintext never persisted. Covered under NFR-SEC-002 but tracked as explicit deliverable for audit trail.|SEC-RT-HASH|COMP-TOKMGR|Redis dump inspection in test env: no plaintext tokens; unit test asserts hashing path|S|P0|
|18|SEC-CLOCK-SKEW|Clock-skew tolerance ±30s|JwtService configured with 30-second leeway on `exp` and `nbf` claims to survive NTP drift between service and gateway nodes.|SEC-CLOCK-SKEW|COMP-JWTSVC|Boundary tests at -30s, +30s, -31s, +31s behave as spec'd|S|P1|

### Integration Points — M2

|Component|Interface|Exposed In|Consumed By|Contract|
|---|---|---|---|---|
|JwtService|`sign(payload,ttl)` / `verify(token)` / `rotateKeys()`|M2|COMP-TOKMGR, COMP-AUTHMW, all protected M3–M4 routes|RS256 2048-bit RSA; aud+iss enforced|
|TokenManager|`issue(user)` / `rotate(old)` / `revoke(token)` / `revokeAllForUser(user_id)`|M2|FR-AUTH-003, FR-AUTH-004, M3 password-change flow (session invalidation)|Redis-backed; 5-token cap; oldest-eviction; family revocation on replay|
|AuthMiddleware|Express middleware binding `req.user`|M2|GET /profile, all M3–M4 protected routes|Returns 401 on failure; never 500 for token issues|
|Refresh-replay detector|Internal event hook in TokenManager|M2|OPS-LOG-M2 audit emission; M5 ALERT-LOGIN-FAIL alerting|Emits `refresh_replay_detected` audit event|
|Feature flag AUTH_TOKEN_REFRESH|LaunchDarkly boolean|M2|FR-AUTH-004 handler branch|Default off; M5 rollout owns flip|

### Milestone Dependencies — M2

- OQ-M1-003 closed (RSA key custody + rotation procedure approved by sec-reviewer).
- Redis 7 production-equivalent instance available in staging (existed for M1 lockout — upgraded capacity confirmed for token storage).
- M1 AuthService + UserRepo stable (no breaking schema changes on DM-001).
- Load-test harness from NFR-PERF-002 reusable for NFR-PERF-003.

### Open Questions — M2

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-M2-001 (from PRD OQ-PRD-2)|Maximum number of concurrent refresh tokens per user? STATUS: closed. RESOLUTION: committed to 5-token cap with oldest-eviction on the 6th issuance. Rationale: matches TDD §5.2 implicit device limit; prevents unbounded Redis growth; aligns with multi-device UX research.|Committed value: 5 active tokens/user, FIFO eviction. Shapes DM-002, COMP-TOKMGR, TEST-005.|auth-team, sec-reviewer|2026-05-02 (closed)|
|2|OQ-M2-002 (from PRD OQ-PRD-4)|Should "remember me" extend refresh-token TTL from 7d to 30d? STATUS: closed. RESOLUTION: deferred to v1.1. v1.0 ships with single 7-day refresh TTL regardless of UI checkbox. Rationale: variable TTLs complicate family-revocation logic and 7d is sufficient per TDD.|Removes one variant from v1.0 scope; UI checkbox becomes visual-only or hidden until v1.1.|product, auth-team|2026-05-02 (closed)|
|3|OQ-M2-003|Should refresh-replay detection revoke only the replayed family or ALL tokens for the user? Committed default: replayed family only (matches TDD §5.3); full-user revoke kept as manual admin action via API-009.|Affects blast radius of security incidents vs. user-experience disruption.|sec-reviewer|2026-05-10|

### Risk Assessment and Mitigation — M2

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-M2-KEY RSA private key compromise or mis-custody|CRITICAL|LOW|All issued tokens trusted by attacker; mass revocation required|Key vault with HSM backing (OQ-M1-003 resolution); quarterly rotation; alert on vault access anomalies; key never leaves vault process|sec-reviewer|
|2|R-M2-REDIS Redis outage halts token issuance and refresh|HIGH|MEDIUM|Users cannot authenticate or refresh; cascading login failures|Redis Sentinel or managed Redis with failover <30s; NFR-REL-001 circuit-breaker (M5) falls through to read-only mode; ROLLBACK-AUTO-REDIS triggers automated rollback|auth-team|
|3|R-M2-REPLAY Refresh-token replay attack|HIGH|LOW|Account takeover if undetected|Rotation + family revocation on replay (FR-AUTH-004); SEC-RT-HASH prevents disk exposure; refresh_replay_detected audit event triggers sec review|sec-reviewer|
|4|R-M2-PERF Token issuance p95 exceeds 100ms under load|MEDIUM|MEDIUM|NFR-PERF-003 breach; user-visible login latency|k6 perf gate in CI; RS256 pre-warmed key cache in JwtService; Redis pipelined writes in COMP-TOKMGR|auth-team|

## Milestone M3: Profile & Password Management (Week 5–6, 2026-05-11 → 2026-05-25)

**Objective**: Deliver authenticated profile read/update, password change with session invalidation, and password-reset flow (email-token based). Overlaps M2 exit by ~1 week.
**Duration**: 2 weeks (14 days).
**Entry Criteria**: M2 AuthMiddleware stable; TokenManager exposes `revokeAllForUser`; email provider credentials provisioned; rate-limit policy on /auth/reset-* agreed.
**Exit Criteria**: GET/PUT /profile live; POST /auth/password/change invalidates refresh-token family; POST /auth/password/reset-request + /auth/password/reset-confirm work end-to-end with async email dispatch; TEST-PROFILE + TEST-RESET green.

### Deliverables — M3

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-PROF-001|Profile Retrieval|TDD §6 / PRD FR-005. GET /profile returns `{user_id, email, display_name, created_at, last_login}` for the authenticated caller. Fields hidden: hashed_password, consent_accepted_at (admin API only).|FR-PROF-001|COMP-AUTHMW (M2)|Valid token → 200 + profile JSON; invalid token → 401; response excludes sensitive columns|M|P0|
|2|FR-PROF-002|Profile Update|TDD §6 / PRD FR-006. PUT /profile accepts `{display_name?}` (v1.0 scope limited to display_name; email change deferred to v1.1 per scope discipline). Persists via COMP-USERREPO.|FR-PROF-002|FR-PROF-001|Update succeeds with valid body; email field rejected with 400 (out of scope); change audited|S|P1|
|3|FR-AUTH-005|Password Change (authenticated)|TDD §4 / PRD FR-007. POST /auth/password/change accepts `{currentPassword, newPassword}`. Validates current via bcrypt.compare, hashes new via bcrypt cost 12, invokes `TokenManager.revokeAllForUser(user_id)` to invalidate all refresh tokens. User must re-login.|FR-AUTH-005|COMP-AUTHSVC (M1), COMP-TOKMGR (M2)|Correct current password succeeds; incorrect returns 401; all refresh tokens revoked post-change; audit event `password_changed` emitted|M|P0|
|4|FR-AUTH-006|Password Reset Request|TDD §4 / PRD FR-008. POST /auth/password/reset-request accepts `{email}`. Always returns 200 (prevents enumeration — R-M3-ENUM). If email matches, generates one-time reset token (32-byte random, SHA-256 hashed in DB, 15min TTL) and dispatches reset email via async queue.|FR-AUTH-006|DM-001, COMP-EMAILQ|Known email → email dispatched + token persisted; unknown email → same 200 response, no DB write; rate-limit 3/hour per email|M|P0|
|5|FR-AUTH-007|Password Reset Confirm|TDD §4 / PRD FR-009. POST /auth/password/reset-confirm accepts `{resetToken, newPassword}`. Validates token hash+TTL+not-used, rehashes password, marks token used, revokes all refresh tokens, emits `password_reset_completed` audit event.|FR-AUTH-007|FR-AUTH-006, COMP-TOKMGR|Valid token → password rotated; expired/used token → 400; password changes and all sessions invalidated|M|P0|
|6|DM-RESET|PasswordResetToken data model|Entity persisted in PostgreSQL. Fields: token_id:uuid \| user_id:uuid→UserProfile \| token_hash:sha256 \| expires_at:ts \| used_at:ts?. Index on token_hash. TTL enforcement via scheduled job.|DM-RESET|DM-001|Schema migration applied; index present; cleanup job purges expired tokens daily|S|P0|
|7|COMP-EMAILQ|EmailDispatcher (async queue)|Queue-backed email dispatcher (BullMQ on Redis 7). Non-blocking — /auth/password/reset-request returns before email actually sends. Templates: `password_reset`, `password_changed_notice`. Retries 3x with exponential backoff.|COMP-EMAILQ|Redis 7|reset-request p95 <300ms (not waiting on SMTP); failed email enqueue does NOT fail the HTTP request; dead-letter queue monitored|M|P0|
|8|API-005|GET/PUT /profile endpoints|Protected by authMiddleware. GET 200 profile JSON / 401 unauth. PUT 200 updated profile / 400 invalid field / 401 unauth.|API-005|FR-PROF-001, FR-PROF-002|OpenAPI contract tests green|S|P0|
|9|API-006|POST /auth/password/change|Protected. 200 ok / 401 wrong current password / 400 weak new password (NIST policy).|API-006|FR-AUTH-005|Contract tests cover all branches|S|P0|
|10|API-RESET-REQ|POST /auth/password/reset-request|Public. Always 200 (to prevent enumeration). Rate-limit 3/hour/email + 10/hour/IP.|API-RESET-REQ|FR-AUTH-006|Enumeration negative test: unknown emails indistinguishable from known at response level|S|P0|
|11|API-RESET-CONF|POST /auth/password/reset-confirm|Public (token-bearer auth). 200 ok / 400 invalid-or-expired token / 400 weak password.|API-RESET-CONF|FR-AUTH-007|Contract tests green; token reuse yields 400|S|P0|
|12|TEST-PROFILE|Profile integration tests|End-to-end tests: login → GET /profile → PUT display_name → GET /profile confirms update. Negative: unauthenticated, invalid body.|TEST-PROFILE|API-005|All scenarios green in CI|S|P0|
|13|TEST-RESET|Password reset integration test|E2E: register → reset-request (assert 200 + token in DB) → reset-confirm (assert 200 + tokens revoked) → login with new password. Negative: unknown email, expired token, reused token.|TEST-RESET|API-RESET-REQ, API-RESET-CONF|All scenarios green; includes enumeration negative test|M|P0|

### Integration Points — M3

|Component|Interface|Exposed In|Consumed By|Contract|
|---|---|---|---|---|
|EmailDispatcher|`enqueue(template, to, payload)` (async)|M3|FR-AUTH-006, FR-AUTH-007 (password_changed_notice)|BullMQ job; 3 retries; DLQ on final failure|
|TokenManager.revokeAllForUser|Invoked from password change + reset|M2→M3|FR-AUTH-005, FR-AUTH-007|Atomic revocation of entire user refresh-token set|
|DM-RESET cleanup job|Cron (daily 03:00 UTC)|M3|Ops / DB maintenance|Purges rows where expires_at < now - 7d|
|Rate-limit policy on /auth/reset-*|Gateway config|M3|API-RESET-REQ|3/hour/email, 10/hour/IP|

### Milestone Dependencies — M3

- M2 TokenManager stable with `revokeAllForUser` publicly supported.
- Email provider SMTP credentials provisioned in staging vault.
- DM-001 unchanged (columns from M1 sufficient for profile reads).
- Redis 7 capacity reviewed — adds BullMQ workload on top of token storage.

### Open Questions — M3

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-M3-001 (from PRD OQ-PRD-1)|Are password-reset emails sent synchronously (block HTTP request) or asynchronously (queue)? STATUS: closed. RESOLUTION: async via BullMQ (COMP-EMAILQ). Rationale: TDD §4.3 implies async via "dispatched"; NFR-PERF on reset-request requires p95 <300ms which SMTP cannot guarantee; enumeration-resistance does not depend on sync delivery.|Committed design: async queue. Drives COMP-EMAILQ deliverable and NFR-PERF target.|backend-architect, product|2026-05-06 (closed)|
|2|OQ-M3-002|Email provider selection (SES vs. SendGrid vs. Mailgun) — affects throughput limits and DLQ integration.|Throughput caps for reset emails; incident response path when provider degrades.|devops, product|2026-05-14|
|3|OQ-M3-003|Should password_changed_notice email include device/IP metadata (security-positive but privacy-sensitive)? Default: include city-level geoIP + user-agent family, omit raw IP.|User security visibility vs. PII minimization (aligns with R-M1-CONSENT).|sec-reviewer, product|2026-05-16|

### Risk Assessment and Mitigation — M3

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-M3-ENUM Email enumeration via reset-request response differential|HIGH|MEDIUM|Attacker maps valid email accounts|Always return 200 regardless of email existence; constant-time response; rate-limit 3/hr/email + 10/hr/IP; enumeration negative test in TEST-RESET|sec-reviewer|
|2|R-M3-EMAIL Email provider outage blocks password reset|HIGH|MEDIUM|Users locked out of account recovery|Async queue with DLQ; fallback provider runbook; incident alert on DLQ depth >50 (wired in M5 ALERT-*); reset-request still returns 200 so UX continues|devops|
|3|R-M3-TOKEN Reset token leakage via email interception or referer header|HIGH|LOW|Account takeover via stolen reset link|15-min TTL; single-use; SHA-256 hashing at rest; token in request body not URL path; password_changed_notice email alerts user to unexpected changes|sec-reviewer|
|4|R-M3-SESSION Stale sessions persist after password change|MEDIUM|LOW|Compromised credentials remain valid via existing refresh tokens|`TokenManager.revokeAllForUser` invoked on password change and reset-confirm; audit event logged; TEST-RESET asserts revocation|auth-team|

## Milestone M4: Frontend, Admin APIs & Observability (Week 7–8, 2026-05-18 → 2026-06-01)

**Objective**: Ship React frontend for all M1–M3 flows; deliver admin-facing APIs for account management; wire up full observability stack (metrics, structured logs, traces, SLO dashboards); deliver logout + health endpoints needed for rollout.
**Duration**: 2 weeks. Overlaps M3 exit by ~1 week.
**Entry Criteria**: M2 token middleware + M3 password flows complete; Grafana + Prometheus instances provisioned; admin role policy approved; frontend build pipeline reachable.
**Exit Criteria**: All UI flows pass E2E tests; admin APIs gated by admin role claim; /health returns JSON per contract; Prometheus scrape target live; SLO dashboards populated with real staging traffic.

### Deliverables — M4

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|COMP-001|LoginPage component|React component at /login. Renders email+password form, calls POST /auth/login, stores accessToken in memory (SEC-MEMSTORE), sets httpOnly refresh cookie via response (SEC-HTTPONLY). Handles 401/423/429 error paths with UI feedback.|COMP-001|API-003 (M2)|Form submits; error states rendered; React Testing Library suite green|M|P0|
|2|COMP-002|RegisterPage component|React component at /register. Form with email, password, display_name, consent checkbox (required). Wires consent_accepted_at + consent_version to POST /auth/register body. Per CONFLICT-2 contract: on success, NOT auto-logged-in — redirects to /login with "Check your email" banner.|COMP-002|API-002 (M1)|Form submits; consent blocks submission when unchecked; post-register redirect lands on /login; no token stored|M|P0|
|3|COMP-003|ProfilePage component|React component at /profile. Reads GET /profile, renders editable display_name, submits PUT /profile on save. Password change and reset-initiate links present.|COMP-003|API-005 (M3), COMP-006|Renders for authenticated user; unauth redirects to /login|M|P1|
|4|COMP-004|PasswordChangeForm|Embedded in ProfilePage. Fields: current, new, confirm. Calls POST /auth/password/change. On success shows "Password changed — please log in again" (session revoked).|COMP-004|API-006 (M3)|Success path triggers logout UX; error paths (weak password, wrong current) rendered inline|S|P1|
|5|COMP-005|PasswordResetForm|Two-step flow: (a) /auth/reset page requests email → POST /auth/password/reset-request, (b) /auth/reset/confirm?token=… accepts new password → POST /auth/password/reset-confirm.|COMP-005|API-RESET-REQ, API-RESET-CONF (M3)|Both steps land correct 200 UX regardless of email existence; confirm page rejects expired/used tokens|M|P0|
|6|COMP-006|AuthGuard router component|React Router guard. Wraps protected routes (/profile, /settings, /admin/*). Checks presence of valid in-memory access token; if absent/expired attempts silent refresh (FEAT-SILENTREF) before redirecting to /login.|COMP-006|COMP-001, FEAT-SILENTREF|Protected route renders only with valid session; silent refresh transparent to user|M|P0|
|7|SEC-HTTPONLY|HttpOnly refresh-token cookie|Backend sets `refreshToken` cookie with `HttpOnly; Secure; SameSite=Strict; Path=/auth/refresh`. Frontend never reads refresh token directly; only POST /auth/refresh sends it automatically.|SEC-HTTPONLY|API-003, API-004 (M2)|Browser devtools show cookie is httpOnly; document.cookie excludes refreshToken; CSRF-safe via SameSite|S|P0|
|8|SEC-MEMSTORE|Access token in memory only|Frontend stores access token in a module-scoped variable (React context). Never in localStorage/sessionStorage. Lost on tab refresh → silent refresh rehydrates.|SEC-MEMSTORE|COMP-001|Static analysis confirms no localStorage.setItem('accessToken') calls; OWASP ZAP pass clean|S|P0|
|9|FEAT-SILENTREF|Silent refresh on expiry|Interceptor fires POST /auth/refresh when access token expires (401) or preemptively within 30s of exp. New access token rehydrates in-memory store; original request is retried once.|FEAT-SILENTREF|API-004 (M2), SEC-HTTPONLY|Expired access token transparently refreshed; failed refresh redirects to /login|M|P0|
|10|FEAT-401INT|401 response interceptor|Axios (or fetch wrapper) interceptor catches 401 on any API call, triggers silent refresh, retries original request once, falls through to /login on second 401.|FEAT-401INT|FEAT-SILENTREF|Single retry verified; infinite-loop guard in place|S|P0|
|11|UI-ERR|Error boundaries + toast system|React ErrorBoundary wraps each page; network/API errors surface via toast (react-hot-toast or equivalent). Rate-limit 429 shows cooldown UX.|UI-ERR|COMP-001..005|Forced-error tests render fallback UI instead of blank screen|S|P1|
|12|UI-A11Y|Accessibility audit pass|WCAG 2.1 AA compliance across auth screens: keyboard navigation, ARIA labels, color contrast ≥4.5:1, focus management on modal open/close.|UI-A11Y|COMP-001..005|axe-core CI check reports 0 critical/serious; manual keyboard walkthrough documented|M|P1|
|13|TEST-006|Frontend component test suite|React Testing Library + Jest unit tests for COMP-001..006. Coverage ≥80% on auth module. Mocks API layer.|TEST-006|COMP-001..006|Coverage gate passes in CI|M|P0|
|14|E2E-REFRESH|Playwright E2E — silent refresh|Playwright scenario: login → wait for access token expiry (TTL compressed in test env) → make protected request → assert seamless refresh → request succeeds.|E2E-REFRESH|FEAT-SILENTREF, COMP-006|Scenario green against staging; recorded in CI pipeline|M|P0|
|15|E2E-LOGOUT|Playwright E2E — logout|Scenario: login → click LogoutControl → assert POST /auth/logout called → assert refresh-cookie cleared → assert subsequent protected request returns 401 → redirected to /login.|E2E-LOGOUT|COMP-016, API-007|Scenario green; cookie clear verified via response headers|S|P0|
|16|FUNNEL-REG|Registration funnel instrumentation|Frontend events `register_form_viewed`, `register_submitted`, `register_success`, `register_failed{reason}` emitted to analytics (Segment or self-hosted). Feeds PRD NFR-001 conversion KPIs.|FUNNEL-REG|COMP-002|Events visible in analytics sink within 60s of emission|S|P1|
|17|API-007|POST /auth/logout|Server endpoint revoking the refresh token presented (or all user tokens if `?all=true` query). Clears httpOnly refresh cookie via `Set-Cookie: refreshToken=; Max-Age=0`. Returns 204.|API-007|COMP-TOKMGR (M2)|Logout revokes refresh token; cookie cleared; audit event `logout` emitted; 204 on success regardless of token validity|S|P0|
|18|COMP-016|LogoutControl component|React component (button in header) calling POST /auth/logout then clearing in-memory access token and routing to /login. Shows toast "Signed out".|COMP-016|API-007|Click invokes endpoint; local state cleared; route changes to /login|S|P0|
|19|API-008|GET /admin/auth/users|Admin-only endpoint. Paginated list of UserProfile rows (sensitive columns redacted — hashed_password never returned). Supports `?email=` substring search. Protected by admin role claim.|API-008|COMP-AUTHMW (M2), DM-001|Non-admin returns 403; admin returns paginated JSON; hashed_password absent from response|M|P0|
|20|API-009|POST /admin/auth/users/:id/revoke-sessions|Admin endpoint calling `TokenManager.revokeAllForUser(id)`. Emits audit event `admin_revoke_sessions` with admin_user_id actor.|API-009|COMP-TOKMGR (M2), DM-AUDIT|Admin can force logout any user; audit event recorded; non-admin returns 403|S|P0|
|21|API-010|POST /admin/auth/users/:id/unlock|Admin endpoint clearing lockout counter for user (FEAT-LOCK M1 state). Emits audit event `admin_unlock` with actor.|API-010|FEAT-LOCK (M1), DM-AUDIT|Locked user becomes unlocked; audit event recorded; non-admin returns 403|S|P0|
|22|COMP-018|AdminAuthEventService|Server-side service encapsulating admin-originated mutations (revoke, unlock, user listing). Enforces admin role check, adds actor metadata to audit events, rate-limits admin bulk operations.|COMP-018|API-008, API-009, API-010|Single enforcement point for admin auth mutations; integration tests cover role-gating|M|P0|
|23|COMP-019|AccountLockManager|Server-side service centralising lockout logic already scattered in M1 FEAT-LOCK. Exposes `isLocked(user)`, `recordFailure(user)`, `unlock(user)`. Used by AuthService (login path) and API-010 (admin unlock).|COMP-019|FEAT-LOCK (M1)|Unit tests cover lockout count thresholds; admin unlock path uses same service|M|P0|
|24|API-011|GET /health|Liveness + readiness endpoint. Returns `{status:"ok", db:"ok", redis:"ok", version:<sha>, uptime_s:<int>}`. Public (no auth). Used by load balancer, Kubernetes probes, synthetic monitors (OBS-006).|API-011|DM-001, Redis|Endpoint returns 200 when dependencies healthy; returns 503 when db or redis unreachable; documented in runbook|S|P0|
|25|OBS-001|Prometheus metrics endpoint|GET /metrics exposes Prometheus scrape format: counters from METRIC-REG, METRIC-LOGIN, METRIC-REFRESH plus `http_requests_total{route,status}`, `http_request_duration_ms` histogram. Scrape interval 15s.|OBS-001|METRIC-REG, METRIC-LOGIN, METRIC-REFRESH|Prometheus target UP in staging; all counters visible; histogram has sensible buckets 10/50/100/250/500/1000ms|M|P0|
|26|OBS-002|Structured JSON logging|Logger (pino) emits JSON with fields `timestamp, level, service, trace_id, span_id, user_id?, route?, msg, ...`. stdout only (container runtime collects). No PII (email, password hashes) in logs.|OBS-002|OPS-LOG-M1 (M1)|Log sample review: JSON parseable; PII scan clean; trace_id present on request-scoped lines|S|P0|
|27|OBS-003|Distributed trace IDs|OpenTelemetry SDK integrated. Incoming requests generate trace_id; outbound calls (Redis, DB, email queue) propagate context. Exporter writes to OTLP endpoint (Tempo or Jaeger).|OBS-003|OBS-002|Traces visible in Tempo for sampled requests; span tree shows login → DB → Redis|M|P0|
|28|OBS-004|Audit-log dashboard|Grafana dashboard reading from DM-AUDIT (Loki or direct DB panel). Panels: logins/min, failed-login rate, lockouts, password changes, admin actions (from API-008..010 events). Linked from oncall runbook.|OBS-004|DM-AUDIT (M1), OBS-003|Dashboard loads against staging data; panels refresh at 30s; alertable panels feed ALERT-* in M5|M|P0|
|29|OBS-005|SLI/SLO definitions|Service-level indicators codified: login-success-rate ≥99.5%, refresh-success-rate ≥99.9%, p95 login latency <200ms, p95 refresh <100ms, availability ≥99.9%. Recorded as Prometheus recording rules; feed SUCC-SLO-BOARD (M5).|OBS-005|OBS-001|SLIs computed in staging; error-budget panel populated; reviewed with SRE|M|P0|
|30|OBS-006|Synthetic monitors|Checkly (or equivalent) probe suite: /health every 1min, full register → login → refresh → logout flow every 5min. Alerts wired into M5 oncall.|OBS-006|API-011|Monitors green in staging; alerts deliver to oncall channel in <60s of failure|S|P0|
|31|OBS-007|Alerting runbook|Markdown runbook in repo `docs/runbooks/auth.md` covering: Redis down, refresh-replay spike, login-failure spike, /health 503, synthetic failure. Each entry: symptom → diagnosis steps → mitigation → escalation.|OBS-007|OBS-004, OBS-006|Runbook reviewed by SRE; linked from all Grafana alert panels; dry-run of Redis-down scenario walked through|S|P0|

### Integration Points — M4

|Component|Interface|Exposed In|Consumed By|Contract|
|---|---|---|---|---|
|LogoutControl→/auth/logout|POST with httpOnly cookie|M4|COMP-016, E2E-LOGOUT|Returns 204; clears cookie; revokes refresh|
|AuthGuard|React Router v6 `<Outlet/>`|M4|All protected routes|Silent refresh on mount; redirect on unrecoverable 401|
|Admin APIs|Gated by `roles` claim includes "admin"|M4|Admin SPA (out of scope v1.0) or direct API callers|403 on non-admin; audit event per mutation|
|/health|Liveness+readiness JSON|M4|K8s probes, LB, OBS-006 synthetics|200 healthy / 503 degraded; never 500|
|Prometheus /metrics|Pull scrape|M4|Prometheus server|15s scrape; cardinality <10k labels|
|OTLP exporter|gRPC OTLP push|M4|Tempo / Jaeger|Trace per request; sampled 10% prod, 100% staging|
|Alert runbook|Markdown in repo|M4|Oncall engineers, linked from Grafana|Every alert has a matching runbook section|

### Milestone Dependencies — M4

- M2 token pair + middleware stable.
- M3 password-change/reset flows reachable from frontend.
- Grafana + Prometheus + Loki + Tempo provisioned (or managed equivalents).
- Admin role claim issuance mechanism decided (static config file for v1.0; dynamic admin console deferred).
- AUTH_NEW_LOGIN flag still at 0% — M4 lands behind flag, ready for M5 rollout.

### Open Questions — M4

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-M4-001|Admin role assignment mechanism for v1.0: static config (YAML env var) vs. DB-backed admin_users table. Committed default: static YAML for v1.0, DB-backed in v1.1.|Admin API access control; audit posture|sec-reviewer, product|2026-05-22|
|2|OQ-M4-002|OpenTelemetry exporter target — Tempo (self-hosted) vs. Jaeger (legacy) vs. managed SaaS. Committed default: Tempo to match existing Grafana stack.|Trace retention cost; integration effort|devops|2026-05-20|
|3|OQ-M4-003|Synthetic monitor credentials — dedicated test user account per environment; rotation schedule. Committed: dedicated `synthetics@internal` user created in staging + prod, password rotated quarterly.|Credential hygiene for OBS-006|sec-reviewer|2026-05-24|

### Risk Assessment and Mitigation — M4

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-M4-ROUTER Router-guard race condition during silent refresh|MEDIUM|MEDIUM|Flicker to /login then back to protected route, or duplicate refresh calls|Single-flight refresh promise in FEAT-SILENTREF; guard awaits refresh result before redirect; E2E-REFRESH asserts no flicker|frontend-lead|
|2|R-M4-ADMIN Admin API privilege escalation via forged role claim|CRITICAL|LOW|Unauthorised revoke/unlock of any account|Admin role asserted from signed JWT claim (RS256); server never trusts client-supplied role hints; unit test proves tampered token rejected; COMP-018 single enforcement point|sec-reviewer|
|3|R-M4-OBS-CARD Prometheus metric cardinality explosion from per-user labels|MEDIUM|MEDIUM|Prometheus OOM; dashboard latency|Explicit allowlist on label values; user_id NEVER used as label; CI check on metrics exposition output|devops|
|4|R-M4-HEALTH /health endpoint leaks internal component versions/hostnames|LOW|MEDIUM|Information disclosure for attackers|Version field limited to short git sha; hostnames omitted; /health is public but contains no secrets|sec-reviewer|
|5|R-M4-CSRF CSRF on refresh-cookie endpoint|HIGH|LOW|Attacker forces refresh from third-party origin|SameSite=Strict cookie; CORS allowlist; POST-only endpoint; audit event on refresh from unexpected origin|sec-reviewer|

## Milestone M5: Migration, Rollout & Rollback Hardening (Week 9–10, 2026-05-26 → 2026-06-09)

**Objective**: Migrate legacy users, execute phased production rollout via feature flags, deliver automated rollback triggers, alerting, SLO dashboards, and signed-off go/no-go gate for GA.
**Duration**: 2 weeks. Overlaps M4 exit by ~4 days.
**Entry Criteria**: M4 exit satisfied; AUTH_NEW_LOGIN and AUTH_TOKEN_REFRESH flags deployed (0%); OBS dashboards populated in staging; migration dry-run passed in staging.
**Exit Criteria**: Legacy auth retired; new system at 100% traffic; NFR-REL-001 met in prod; all automated rollback triggers proven in chaos-test; GA go/no-go gate signed off; SUCC-SLO-BOARD live in production Grafana.

### Deliverables — M5

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|MIG-001|Legacy user data migration script|One-time job reading legacy_users table, upserting into new UserProfile via COMP-USERREPO. Preserves created_at, email (validated), last_login. Hashed passwords rehashed lazily on next login (legacy SHA-1 → bcrypt on first successful login).|MIG-001|DM-001 (M1)|Dry-run on staging copy: 0 row loss; idempotent re-run produces 0 changes|L|P0|
|2|MIG-002|Parallel-run reconciliation|During Phase 1 rollout, every login hits legacy AND new systems; discrepancies logged to `auth_migration_mismatch` table for review. Runs until flag reaches 50%.|MIG-002|MIG-001, FEAT-FLAG-NEWLOGIN|Mismatch rate <0.1% before advancing flag; dashboard panel visible|M|P0|
|3|MIG-003|Legacy auth retirement|After 100% traffic on new system stable for 48h, legacy auth routes return 410 Gone; legacy_users table archived to cold storage; retirement noted in CHANGELOG.|MIG-003|MIG-002, NFR-REL-001|Legacy endpoint returns 410; smoke test confirms no traffic on legacy code path for 24h|S|P0|
|4|FEAT-FLAG-NEWLOGIN|Rollout of AUTH_NEW_LOGIN|Phased rollout: 0% → 1% → 5% → 25% → 50% → 100%. Advance only if SLO panel green for ≥60min and error-rate delta vs. legacy <0.5%.|FEAT-FLAG-NEWLOGIN|FEAT-LOCK, OBS-005, MIG-002|Each stage held minimum duration; documented advance decisions in rollout log|M|P0|
|5|FEAT-FLAG-REFRESH|Rollout of AUTH_TOKEN_REFRESH|Same phased approach as NEWLOGIN but tied to token-refresh flow. Dependent on NEWLOGIN ≥25% before starting.|FEAT-FLAG-REFRESH|FEAT-REFRESH-FLAG (M2), FEAT-FLAG-NEWLOGIN|Dependency ordering enforced; advancement criteria logged|M|P0|
|6|OPS-001|Production Prometheus + Grafana provisioned|Prod instances of metrics + dashboards stack, separate from staging. Retention 30d metrics, 90d dashboards. Auth for Grafana via SSO.|OPS-001|OBS-001 (M4)|Prod scrape targets up; SSO login works; retention settings verified|M|P0|
|7|OPS-002|Production Tempo/Jaeger trace backend|Prod trace backend with 7-day retention; sampling 10% of requests + 100% of 5xx + 100% of refresh-replay events.|OPS-002|OBS-003 (M4)|Prod traces visible; sampling rules active|S|P1|
|8|OPS-003|Production Loki log aggregation|Prod Loki cluster ingesting structured JSON from OBS-002. Retention 14d hot + 90d cold.|OPS-003|OBS-002 (M4)|Queryable in Grafana; PII scanner cron flags violators daily|M|P0|
|9|OPS-004|Audit-log retention 12 months|DM-AUDIT rows older than 12 months archived to S3 Glacier (per OQ-M1-002 committed value). Nightly job; signed manifest for SOC2.|OPS-004|DM-AUDIT (M1)|First archive run completes; manifest stored; restore drill documented|M|P0|
|10|OPS-005|SMTP / email provider prod rollout|Prod email provider credentials injected; DKIM+SPF+DMARC configured for sender domain. Monitoring on bounce + complaint rates.|OPS-005|COMP-EMAILQ (M3)|Deliverability test: 99%+ inbox rate to major providers; complaint rate <0.1%|S|P0|
|11|ALERT-LOGIN-FAIL|Alert: login failure spike|Prometheus alert on `rate(auth_login_fail_total[5m]) / rate(auth_login_total[5m]) > 0.30` sustained 10min. Pages oncall.|ALERT-LOGIN-FAIL|METRIC-LOGIN (M1), OPS-001|Firing alert reaches pager in staging test; runbook linked|S|P0|
|12|ALERT-LATENCY|Alert: login p95 latency|Alert on `histogram_quantile(0.95, rate(auth_login_duration_ms_bucket[5m])) > 300` sustained 10min.|ALERT-LATENCY|OBS-001, OBS-005|Synthetic spike triggers alert; page delivery <60s|S|P0|
|13|ALERT-REDIS|Alert: Redis unavailable|Alert on Redis exporter `redis_up == 0` for >1min. Pages oncall immediately.|ALERT-REDIS|OPS-001|Redis-kill chaos drill fires alert; runbook resolves drill|S|P0|
|14|ROLLBACK-AUTO-LATENCY|Automated rollback on latency breach|If login p95 >500ms for 15min during rollout, flag auto-reverts to previous stage (LaunchDarkly scheduled segment). Manual override requires 2 approvers.|ROLLBACK-AUTO-LATENCY|FEAT-FLAG-NEWLOGIN, ALERT-LATENCY|Chaos test with induced latency demonstrates auto-revert within 15min window|M|P0|
|15|ROLLBACK-AUTO-ERR|Automated rollback on error rate|If 5xx-rate on /auth/* >1% for 10min during rollout, flag auto-reverts.|ROLLBACK-AUTO-ERR|FEAT-FLAG-NEWLOGIN|Chaos test injects 5xx spike; auto-revert verified|M|P0|
|16|ROLLBACK-AUTO-REDIS|Automated rollback on Redis unavailability|If Redis unreachable for >3min, auth service enters read-only mode (existing sessions honored, no new issuance) and flag auto-reverts new-login traffic to 0%.|ROLLBACK-AUTO-REDIS|ALERT-REDIS, FEAT-FLAG-NEWLOGIN|Redis chaos drill triggers read-only mode + flag flip; drill report filed|M|P0|
|17|ROLLBACK-AUTO-DATA|Automated rollback on DB write-failure spike|If DM-001 write error rate >5% for 5min, halt registration (return 503) and revert FEAT-FLAG-NEWLOGIN to last stable stage.|ROLLBACK-AUTO-DATA|DM-001, FEAT-FLAG-NEWLOGIN|DB-fault chaos drill triggers halt + revert; no data corruption observed|M|P0|
|18|ROLLBACK-STEPS|Manual rollback runbook|docs/runbooks/auth-rollback.md. Step-by-step manual procedure for full stack revert if automated triggers fail. Includes DB restore from backup, flag reset, incident-comms template.|ROLLBACK-STEPS|OBS-007 (M4), ROLLBACK-AUTO-*|SRE walkthrough performed; runbook version-controlled|S|P0|
|19|NFR-REL-001|Reliability: 99.9% availability|Prod service meets 99.9% monthly availability SLO after rollout. Measured via /health synthetic monitor + Prometheus up metric.|NFR-REL-001|OBS-005, OBS-006 (M4), OPS-001|First full post-GA calendar month: availability ≥99.9%; error-budget panel confirms|M|P0|
|20|SUCC-SLO-BOARD|Production SLO dashboard|Grafana board surfacing login-success-rate, refresh-success-rate, p95 latencies, error budget burn-down, rollout-stage indicator. Embedded link in exec status updates.|SUCC-SLO-BOARD|OBS-004, OBS-005 (M4)|Board linked from README ops section; exec review signs off|S|P0|
|21|OPS-011|GA go/no-go gate|Formal signed-off gate before advancing flag to 100%. Checklist: all ROLLBACK-AUTO-* chaos-tested; SUCC-SLO-BOARD green ≥48h; ALERT-* verified; MIG-002 mismatch rate <0.1%; OBS-007 runbook dry-run complete; sec-reviewer + eng-manager + product sign off in ticket.|OPS-011|ROLLBACK-AUTO-LATENCY, ROLLBACK-AUTO-ERR, ROLLBACK-AUTO-REDIS, ROLLBACK-AUTO-DATA, SUCC-SLO-BOARD, MIG-002|Checklist fully ticked; signed-off ticket attached to release; GA announced only after gate passes|M|P0|

### Integration Points — M5

|Component|Interface|Exposed In|Consumed By|Contract|
|---|---|---|---|---|
|FEAT-FLAG-NEWLOGIN|LaunchDarkly segment|M5|Auth service login branch|0→1→5→25→50→100%; reversible in <60s|
|ROLLBACK-AUTO-*|Alertmanager webhook → LaunchDarkly API|M5|Feature flag service|Auto-revert within SLA per trigger|
|Go/no-go gate|Signed checklist (Jira / GH issue template)|M5|Release manager, exec|All boxes checked before 100% rollout|
|Legacy-to-new reconciliation|auth_migration_mismatch table + dashboard|M5|MIG-002 during rollout|Mismatch <0.1% gate|
|Prod SSO for Grafana|Okta/Azure AD OIDC|M5|OPS-001|MFA required; group-based admin|

### Milestone Dependencies — M5

- M4 observability + admin + logout + health deliverables all green.
- LaunchDarkly (or equivalent) prod environment provisioned + API tokens in vault.
- Chaos-testing harness (Gremlin / Chaos Mesh / bespoke) reachable from staging.
- S3 Glacier bucket provisioned for audit log archival (OPS-004).
- 48h stability window budget in schedule (MIG-003 requirement) before 2026-06-09 GA.

### Open Questions — M5

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-M5-001|Automated rollback 2-approver manual override — who are the two named approvers? Committed default: on-call SRE + engineering manager (named in docs/runbooks/auth.md).|Rollback authority clarity; compliance|eng-manager, devops|2026-05-28|
|2|OQ-M5-002|Go-live communication plan: email all existing users about new login flow? Committed default: yes, 48h prior, plus in-app banner during rollout.|User support volume; UX expectation-setting|product, support|2026-05-30|
|3|OQ-M5-003|Chaos-testing budget: can we run prod-equivalent chaos drills in a lower environment, or do we need a prod canary? Committed default: staging-only; canary deferred to v1.1.|Confidence in ROLLBACK-AUTO-* triggers|devops, sec-reviewer|2026-06-02|

### Risk Assessment and Mitigation — M5

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-M5-ROLLOUT Silent regression during phased rollout bypasses SLO gates|HIGH|MEDIUM|Degraded UX for % of users before detection|MIG-002 parallel-run catches functional delta; ROLLBACK-AUTO-LATENCY + -ERR catch perf/reliability delta; 60min hold per stage; dashboards reviewed before advance|eng-manager|
|2|R-M5-ALERT Alert fatigue from noisy thresholds|MEDIUM|MEDIUM|Oncall ignores real incident|ALERT-* thresholds tuned in staging chaos drills first; each alert requires matching OBS-007 runbook entry; alert review monthly|devops|
|3|R-M5-MIGRATION Data loss during legacy→new migration|HIGH|LOW|User accounts missing or duplicated|Pre-migration PostgreSQL snapshot; idempotent MIG-001 script; MIG-002 reconciliation surfaces mismatches; dry-run on staging copy mandatory|auth-team|
|4|R-M5-LEGACY Legacy auth still receives traffic after cutover|MEDIUM|LOW|Split-brain session state|410 Gone on legacy routes post-MIG-003; router rules audited; 24h traffic observation before retirement|devops|
|5|R-M5-AUDIT-ARCHIVE Audit-log archival job fails silently, breaching SOC2|HIGH|LOW|Compliance finding; retention gap|OPS-004 job emits signed manifest; alert on missing manifest for 25h; quarterly restore drill|sec-reviewer|

## Resource Requirements

### External Dependencies

|Dependency|Required By|Availability Needed|Owner|
|---|---|---|---|
|PostgreSQL 15|DM-001, DM-AUDIT, DM-RESET (M1/M3)|M1 start (2026-04-20)|devops|
|Redis 7|FEAT-LOCK (M1), DM-002 (M2), COMP-EMAILQ (M3)|M1 start — capacity review for M2/M3 additions|devops|
|Node.js 20 LTS runtime|All server deliverables|M1 start|devops|
|React 18 + Vite build chain|COMP-001..006 + UI-* (M4)|M4 start (2026-05-18)|frontend-lead|
|OpenTelemetry SDK + OTLP backend (Tempo)|OBS-003 (M4)|M4 start|devops|
|Prometheus + Grafana + Loki|OBS-001..007 (M4), OPS-001..003 (M5)|Staging: M4 start; Prod: M5 start|devops|
|LaunchDarkly (or equivalent) prod env|FEAT-FLAG-NEWLOGIN, FEAT-FLAG-REFRESH, ROLLBACK-AUTO-* (M5)|M5 start (2026-05-26)|devops|
|Email provider (SES/SendGrid — per OQ-M3-002)|COMP-EMAILQ (M3), OPS-005 (M5)|M3 start (2026-05-11); prod-credentialled by M5|devops, product|
|Key management vault with HSM|COMP-JWTSVC (M2)|OQ-M1-003 closure (target 2026-04-28) → M2 start|sec-reviewer|
|S3 Glacier (audit archival)|OPS-004 (M5)|M5 start|devops|
|SSO provider (Okta/Azure AD) for Grafana|OPS-001 (M5)|M5 start|devops|
|Chaos-testing harness|ROLLBACK-AUTO-* chaos drills (M5)|M5 week 1|devops|
|Synthetics service (Checkly/equivalent)|OBS-006 (M4), OBS-006 prod binding (M5)|M4 start|devops|

### Infrastructure Requirements

- **Service network** sized for 100 RPS sustained on auth endpoints (load test target NFR-PERF-002 / NFR-PERF-003); autoscale headroom 3x.
- **PostgreSQL**: primary + 1 read replica; backup RPO ≤1h, RTO ≤4h. Storage sized for 12-month audit retention (estimate ~50GB/year at projected user growth — reviewed in OPS-004).
- **Redis**: 2-node Sentinel (or managed equivalent) with automatic failover <30s. Separate logical DBs for token storage (DM-002) and email queue (COMP-EMAILQ).
- **Secrets**: RSA private key material in HSM-backed vault (per OQ-M1-003); quarterly rotation; access audit emitted to SIEM.
- **Feature-flag service**: reachable from prod auth service with ≤50ms p95 eval latency; flag-eval cache with 10s TTL to absorb vendor outages.
- **Observability storage**: Prometheus 30d retention; Loki 14d hot + 90d cold; Tempo 7d retention; aggregate storage ~2TB for initial scale.
- **Email deliverability**: sender domain with DKIM+SPF+DMARC; bounce/complaint webhook endpoints consuming into OBS-004 dashboard.
- **CDN / edge**: frontend static assets fronted by CDN with immutable-asset caching; auth endpoints remain origin-only (no edge caching on /auth/*).
- **Logging PII scanner**: daily cron over Loki querying for email/password patterns; flags to sec-reviewer channel.

## Global Risk Register

|ID|Risk|Severity|Likelihood|Impact|Affected Milestones|Mitigation|
|---|---|---|---|---|---|---|
|R-001|JWT secret/key compromise (system-wide)|CRITICAL|LOW|Mass token forgery; full auth bypass|M2, M5|HSM-backed key custody (OQ-M1-003); quarterly rotation; SIEM alerting on vault access anomalies; emergency rotation runbook|
|R-002|Brute-force attacks on login endpoint|MEDIUM|HIGH|Credential stuffing at scale|M1, M5|Gateway rate-limit 10/min/IP; FEAT-LOCK 5/15min; bcrypt cost 12; WAF+CAPTCHA contingency in M5|
|R-003|Data loss during legacy-auth migration|HIGH|LOW|UserProfile corruption, orphaned accounts|M5|Pre-migration PG snapshot; idempotent MIG-001; MIG-002 parallel reconciliation; staging dry-run|
|R-PRD-001|PRD compliance (GDPR consent) drift from TDD|HIGH|MEDIUM|Regulatory exposure; launch blocker|M1, M3|Consent fields in DM-001 at M1 (moved earlier from M3); NFR-GDPR-CONSENT in M1; legal sign-off before rollout; CONFLICT-2 registration contract enforces consent capture|
|R-PRD-002|Compliance failure from incomplete audit logging|HIGH|MEDIUM|SOC2 finding; legal exposure|M1, M5|DM-AUDIT in M1 before any event generation; 12-month retention (OQ-M1-002); OPS-004 archival job; audit of event schema before M3|
|R-PRD-003|12-month audit retention storage cost overrun|MEDIUM|MEDIUM|Budget surprise; possible retention cut under pressure|M1, M5|Early sizing review in OPS-004; S3 Glacier tiering reduces steady-state cost; monthly budget review|
|R-M1-SCHED|M1 start slipped past TDD target 2026-04-14|HIGH|CERTAIN|Downstream cascade risk to GA 2026-06-09|M1|Compressed 2-week M1 starting 2026-04-20; OQ-M1-001 decision ticket; weekly burn-down|
|R-M2-KEY|RSA private key compromise or mis-custody|CRITICAL|LOW|All issued tokens trusted by attacker|M2|HSM vault; quarterly rotation; never-export policy; vault-access alerts|
|R-M2-REDIS|Redis outage halts token issuance / refresh|HIGH|MEDIUM|Cascading login failures|M2, M5|Sentinel/managed failover <30s; NFR-REL-001; ROLLBACK-AUTO-REDIS; read-only fallback mode|
|R-M3-ENUM|Email enumeration via reset-request response|HIGH|MEDIUM|Attacker maps valid accounts|M3|Always-200 response; rate-limit 3/hr/email + 10/hr/IP; enumeration negative test|
|R-M4-ROUTER|Router-guard race condition during silent refresh|MEDIUM|MEDIUM|UI flicker; duplicate refresh calls|M4|Single-flight refresh promise; E2E-REFRESH asserts no flicker|
|R-M5-ROLLOUT|Silent regression during phased rollout|HIGH|MEDIUM|Degraded UX before detection|M5|MIG-002 parallel-run; ROLLBACK-AUTO-LATENCY/ERR; 60min hold per stage; dashboard review before advance|
|R-M5-ALERT|Alert fatigue from noisy thresholds|MEDIUM|MEDIUM|Oncall ignores real incident|M5|Thresholds tuned in staging chaos; every alert has OBS-007 runbook entry; monthly alert review|

## Success Criteria

|#|Criterion|Measurement|Target|Owner|
|---|---|---|---|---|
|1|All 107 deliverables in exit state by GA|JIRA ticket closure + CI green|100%|eng-manager|
|2|NFR-PERF-001: registration p95 <200ms|k6 load test at 100 RPS|p95 <200ms|auth-team|
|3|NFR-PERF-002: login p95 <200ms under 100 RPS sustained|k6 load test|p95 <200ms|auth-team|
|4|NFR-PERF-003: token issuance p95 <100ms|k6 load test|p95 <100ms|auth-team|
|5|NFR-REL-001: 99.9% monthly availability post-GA|Prometheus up + synthetic uptime|≥99.9% first full month|devops|
|6|SLO: login success rate ≥99.5%|Prometheus recording rule|sustained ≥99.5% over 7d|devops|
|7|SLO: refresh success rate ≥99.9%|Prometheus recording rule|sustained ≥99.9% over 7d|devops|
|8|Audit-log coverage: every auth event logged|Schema review + integration tests|100% event-type coverage|sec-reviewer|
|9|Audit-log retention: 12 months|OPS-004 archival manifest|first archive run signed|sec-reviewer|
|10|GDPR consent captured at registration|DM-001 consent fields populated for 100% of new users|100% non-null|legal|
|11|Zero P0 security findings pre-GA|Pentest report + SAST CI|0 P0, ≤2 P1 accepted with mitigation|sec-reviewer|
|12|Migration data integrity: 0 row loss|MIG-001 dry-run + post-cutover reconciliation|0 row loss, <0.1% mismatch cleared|auth-team|
|13|Rollback triggers proven in chaos drills|Drill reports for LATENCY/ERR/REDIS/DATA|4/4 drills pass|devops|
|14|Go/no-go gate (OPS-011) signed off|Checklist fully ticked + 3 sign-offs|Signed 2026-06-07 or earlier|eng-manager|

## Decision Summary

|#|Decision|Rationale|Source|
|---|---|---|---|
|1|JWT RS256 with 2048-bit RSA, not HS256|Asymmetric signing allows public-key verification at edge without secret distribution; industry standard for multi-service auth|TDD §5.1|
|2|bcrypt cost factor 12|Balance of security (~250ms hash time) vs. login latency budget; aligns with OWASP 2024 guidance|TDD §4.1|
|3|Redis-backed refresh tokens with 5-token cap (oldest-eviction)|Caps Redis growth; matches typical multi-device UX; family-revocation on replay simpler than variable TTL|TDD §5.2 + OQ-PRD-2 resolution|
|4|Refresh-token TTL 7 days (no remember-me variant in v1.0)|Removes TTL variance from family-revocation logic; remember-me deferred to v1.1|OQ-PRD-4 resolution|
|5|12-month audit log retention (not 90d)|PRD NFR-COMP-001 + SOC2 requirement overrides TDD §7.2 default of 90d; compliance > design default|OQ-M1-002 resolution / CONFLICT-1|
|6|Registration returns 201 UserProfile, NOT auto-login token pair|Reduces attack surface on unverified email; forces email-verification loop in v1.1; PRD FR-002 contract|CONFLICT-2 resolution|
|7|GDPR consent captured in M1 at registration, not M3|Cannot persist user data before consent is recorded; R-PRD-001/NIST-minimization requires it upfront|Variant B delta / NFR-GDPR-CONSENT relocation|
|8|Password reset email dispatch is async (BullMQ)|SMTP latency incompatible with <300ms p95; enumeration-resistance independent of sync|OQ-PRD-1 resolution|
|9|Lockout policy: 5 attempts / 15-min window / 15-min auto-unlock|Committed to TDD-specified values; admin-override via API-010|OQ-PRD-3 resolution|
|10|Silent refresh with in-memory access token + httpOnly refresh cookie|XSS-resistant (no localStorage exposure); CSRF-resistant (SameSite=Strict); proven pattern|TDD §6.2|
|11|Automated rollback on 4 signals: latency, 5xx rate, Redis down, DB write-error spike|Covers the four observed failure-mode families; manual override requires 2 approvers to limit abuse|M5 ROLLBACK-AUTO-* design|
|12|Admin role via signed JWT claim (static YAML assignment v1.0)|Simple for v1.0; DB-backed admin_users + console deferred to v1.1|OQ-M4-001 resolution|
|13|GA gated on OPS-011 formal go/no-go with 3 sign-offs|Forces explicit decision rather than drift-to-GA; adds accountability trail|Variant B delta|

## Timeline Estimates

|Milestone|Start|End|Duration|Overlap With Next|
|---|---|---|---|---|
|M1 Foundations + Consent|2026-04-20|2026-05-04|2 weeks|~0 days|
|M2 Token Management|2026-05-04|2026-05-18|2 weeks|~5 days with M3|
|M3 Profile & Password|2026-05-11|2026-05-25|2 weeks|~5 days with M4|
|M4 Frontend + Admin + Observability|2026-05-18|2026-06-01|2 weeks|~4 days with M5|
|M5 Migration + Rollout + Rollback|2026-05-26|2026-06-09|2 weeks|— (GA)|

**Critical path**: M1.DM-001 → M2.COMP-TOKMGR → M3.FR-AUTH-005 → M4.FEAT-SILENTREF → M5.OPS-011 → GA 2026-06-09.
**Compression risk**: R-M1-SCHED already triggered; parallel M3↔M4 overlap saves ~10 days vs. sequential. Any M1 slip cascades; M1 exit 2026-05-04 is the hardest internal deadline.
**Buffer**: 48h stability window before GA (MIG-003 requirement); no additional slack. Any mid-milestone slip consumes this buffer before impacting GA.

INCREMENTAL_WRITE_COMPLETE: /config/workspace/SuperClaude_Framework/dev/test-fixtures/test24-tdd-prd/roadmap.md
