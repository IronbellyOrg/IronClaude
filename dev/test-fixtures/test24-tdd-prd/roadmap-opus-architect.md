---
spec_source: "test-tdd-user-auth.compressed.md"
complexity_score: 0.78
complexity_class: HIGH
primary_persona: architect
adversarial: false
base_variant: none
variant_scores: none
convergence_score: none
---

# User Authentication Service — Project Roadmap

## Executive Summary

Deliver a secure, stateless, JWT-based identity layer (`AuthService`) for the platform by 2026-06-09, implementing 5 functional and 9 non-functional requirements across backend, frontend, security, data, compliance, testing, and DevOps domains. The roadmap decomposes the TDD's 876-line specification into 5 technically-layered milestones (Foundation → Core Logic → Integration → Hardening → Production Readiness) covering 120 individually tracked deliverables.

**Business Impact:** Unblocks ~$2.4M in projected annual revenue from personalization-dependent features (Q2-Q3 2026), enables SOC2 Type II audit closure (Q3 2026 deadline), and addresses 30% QoQ growth in access-related support tickets. Persona coverage targets Alex (end user <60s registration), Jordan (admin audit visibility), and Sam (API consumer programmatic refresh).

**Complexity:** HIGH (0.78) — Security-critical domain with crypto primitives (bcrypt, RS256), five-component orchestration (`AuthService`→`TokenManager`→`JwtService`→`PasswordHasher`→`UserRepo`), dual-store persistence (PostgreSQL+Redis), external SMTP dependency, phased feature-flag rollout, and overlapping regulatory frameworks (SOC2, GDPR, NIST SP 800-63B).

**Critical path:** PostgreSQL/Redis provisioning (M1) → `PasswordHasher` + `UserProfile` persistence (M2) → `AuthService.login`/`register` (M2) → `TokenManager` + `JwtService` + `/auth/refresh` (M3) → Frontend `AuthProvider` wiring (M3) → Audit logging + observability (M4) → Feature-flagged beta ramp (M5) → GA on 2026-06-09.

**Key architectural decisions:**

- Stateless JWT (RS256, 2048-bit RSA, 15-min access / 7-day refresh) over server-side sessions — enables horizontal `AuthService` scaling without sticky routing.
- bcrypt cost factor 12 via `PasswordHasher` abstraction — balances <500ms hash time against offline-crack resistance; interface allows future argon2id migration without API changes.
- Dual-store persistence: PostgreSQL 15 for `UserProfile` + audit log (durable), Redis 7 for hashed refresh tokens (revocable, TTL-enforced) — separation of identity-of-record from session artifacts.
- Feature-flagged phased rollout (`AUTH_NEW_LOGIN`, `AUTH_TOKEN_REFRESH`) with 10% beta gate and automatic rollback triggers — bounds blast radius during migration.
- Audit log retention set to 12 months (PRD NFR-COMP-002 / SOC2) overriding TDD §7.2's 90-day default — compliance precedence documented in OQ-CONFLICT-1.

**Open risks requiring resolution before M1:**

- OQ-CONFLICT-1 (audit retention TDD 90d vs PRD 12mo) — must be resolved to size PostgreSQL retention partition and inform AUDIT-001 schema.
- OQ-PRD-3 (account lockout policy) — TDD commits to 5 failures/15min; PRD still open; resolve to allow SEC-001 implementation.
- OBS storage budget for 12-month audit log at projected 1M logins/month must be confirmed with platform-team before M1 exit.

## Milestone Summary

|ID|Title|Type|Priority|Effort|Dependencies|Deliverables|Risk|
|---|---|---|---|---|---|---|---|
|M1|Foundation & Infrastructure|Foundation|P0|2w|PostgreSQL/Redis/Node20/SendGrid provisioning|25|Medium|
|M2|Core Authentication Logic|Core Logic|P0|2w|M1|23|High|
|M3|Integration, Tokens & Frontend|Integration|P0|3w|M2|34|High|
|M4|Hardening, Observability & Compliance|Hardening|P0|2w|M3|26|High|
|M5|Production Readiness & GA|Production|P0|2w|M4|14|Medium|

## Dependency Graph

```
M1 (Foundation)
 ├─> DM-001/DM-002 schemas ─────> M2 (Core Logic)
 ├─> PostgreSQL provisioning ──> M2.UserRepo
 ├─> Redis provisioning ────────> M3.TokenManager
 ├─> bcryptjs / jsonwebtoken ──> M2.PasswordHasher / M3.JwtService
 ├─> SendGrid setup ────────────> M3.PasswordReset
 └─> AUTH_NEW_LOGIN flag ───────> M2→M3→M5 rollout

M2 (Core Logic: PasswordHasher + AuthService.login/register)
 ├─> FR-AUTH-001, FR-AUTH-002 ─> M3 (API-003/004/005/006)
 └─> UserRepo ───────────────────> M4 (AUDIT-001)

M3 (Integration: TokenManager + JwtService + Frontend + Reset)
 ├─> FR-AUTH-003/004/005 ──────> M4 (hardening, observability)
 ├─> COMP-001/002/003/004 ─────> M4 (CAPTCHA, E2E tests)
 └─> API-004 refresh ───────────> M5 (AUTH_TOKEN_REFRESH ramp)

M4 (Hardening: Observability + Compliance + Security + Audit)
 ├─> OBS-001..009 ──────────────> M5 (alerts in production)
 ├─> AUDIT-001/002 ─────────────> M5 (SOC2 compliance gate)
 └─> Pen-test sign-off ─────────> M5 (GA release criteria)

M5 (Production: Phased rollout + runbooks + GA)
 └─> GA 2026-06-09
```

## M1: Foundation & Infrastructure

**Objective:** Provision shared infrastructure, define data contracts, scaffold service skeletons, register feature flags, and resolve blocking design decisions before any auth logic is written. | **Duration:** 2 weeks (Weeks 1-2, 2026-03-30 → 2026-04-10) | **Entry:** TDD AUTH-001-TDD approved; PRD AUTH-PRD-001 approved; SEC-POLICY-001 reviewed; CONFLICT-1 resolution accepted (12-month retention chosen). | **Exit:** PostgreSQL 15 + Redis 7 + Node.js 20 deployed in staging; `UserProfile` and `AuthToken` schemas reviewed; `AuthService`/`TokenManager`/`JwtService`/`PasswordHasher` package skeletons compile; `AUTH_NEW_LOGIN` and `AUTH_TOKEN_REFRESH` flags registered (default OFF); TLS 1.3 + CORS configured at API Gateway; CONFLICT-1 + OQ-PRD-3 resolutions documented.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|DM-001|UserProfile entity schema|Define `UserProfile` PostgreSQL DDL + TypeScript interface; emit migration script.|UserRepo|-|id:UUID-PK-NOT-NULL; email:varchar-UNIQUE-NOT-NULL-indexed-lowercase-normalized; displayName:varchar-NOT-NULL-2-100-chars; createdAt:timestamptz-NOT-NULL-DEFAULT-now(); updatedAt:timestamptz-NOT-NULL-auto-updated; lastLoginAt:timestamptz-NULLABLE; roles:text[]-NOT-NULL-DEFAULT-["user"]; password_hash:varchar-NOT-NULL; migration script applies cleanly to empty PostgreSQL 15|M|P0|
|2|DM-002|AuthToken interface contract|Define `AuthToken` TypeScript interface returned by `AuthService` and `TokenManager`.|TokenManager|-|accessToken:string-JWT-NOT-NULL-RS256-signed-payload-contains-user-id-and-roles; refreshToken:string-NOT-NULL-unique-stored-hashed-in-Redis; expiresIn:number-NOT-NULL-always-900; tokenType:string-NOT-NULL-always-"Bearer"; type exported from shared package|S|P0|
|3|DEP-001|PostgreSQL 15+ provisioning|Provision managed PostgreSQL 15 with connection pool size 100, daily backup, read replica.|Infra|-|version=15+; pool=100; backup retention 30 days; read replica RPO<5min; staging+prod tenants isolated; pg-pool client integrated|M|P0|
|4|DEP-002|Redis 7+ provisioning|Provision managed Redis 7 cluster with 1GB memory, AOF persistence for refresh-token durability.|Infra|-|version=7+; mem=1GB; AOF=on; SET key TTL=604800s (7d) verified by smoke; staging+prod tenants isolated|M|P0|
|5|DEP-003|Node.js 20 LTS runtime|Establish Node.js 20 LTS base image and npm/pnpm dependency lockfile.|Infra|-|node=20.x LTS; lockfile committed; Docker base image published; build succeeds in CI|S|P0|
|6|DEP-004|bcryptjs library integration|Add `bcryptjs` dependency wired through `PasswordHasher` interface.|PasswordHasher|DEP-003|bcryptjs=^2.x; cost-factor parameter wired to env var BCRYPT_COST (default 12); benchmark on target hardware <500ms|S|P0|
|7|DEP-005|jsonwebtoken library integration|Add `jsonwebtoken` dependency wired through `JwtService` interface; load RSA keys from secrets mount.|JwtService|DEP-003|jsonwebtoken=^9.x; RS256 algorithm; 2048-bit RSA keys mounted from K8s secret; clock-skew tolerance=5s configured|S|P0|
|8|DEP-006|SendGrid SMTP/API integration|Provision SendGrid API account, configure DKIM/SPF, integrate transactional template for password reset.|EmailClient|-|API key in vault; DKIM/SPF verified; reset-email template ID stored in config; sandbox send succeeds|M|P0|
|9|DEP-007|Frontend routing framework|Verify frontend routing framework supports `/login`, `/register`, `/profile` routes with auth guards.|Frontend|-|router supports protected routes; redirect-on-401 hook available; route table reviewed|S|P0|
|10|INFRA-001|API Gateway rate limiting|Configure per-IP/per-user rate limits at API Gateway: 10/min login, 5/min register, 60/min /me, 30/min refresh.|APIGateway|-|/auth/login=10rpm/IP; /auth/register=5rpm/IP; /auth/me=60rpm/user; /auth/refresh=30rpm/user; 429 returned with Retry-After header|M|P0|
|11|INFRA-002|TLS 1.3 enforcement|Enforce TLS 1.3 on all `/auth/*` endpoints at load balancer; reject TLS<1.3.|APIGateway|-|TLS-1.3 only; HSTS max-age=31536000; ssllabs.com grade ≥A; older protocols return handshake failure|S|P0|
|12|INFRA-003|CORS allow-list configuration|Restrict CORS to known frontend origins; reject Origin headers outside allow-list.|APIGateway|-|allow-list = staging.platform.com, app.platform.com; preflight returns 403 for other origins; credentials=true wired for cookie refresh|S|P0|
|13|NFR-SEC-002|JWT signing config validation|`JwtService` initialization validates RS256 algorithm and 2048-bit RSA key on boot; fails fast otherwise.|JwtService|DEP-005|alg=RS256 asserted; key length=2048 asserted; service refuses to start if either invalid; configuration test in CI|S|P0|
|14|NFR-SEC-003|TLS 1.3 + log redaction baseline|Establish global log-redaction middleware that strips `password`, `accessToken`, `refreshToken`, `newPassword` fields before sink.|Logging|INFRA-002|redaction list configured; unit test asserts redacted fields never appear in serialized log lines; TLS 1.3 verified end-to-end|S|P0|
|15|COMP-005-skel|AuthService skeleton|Create `AuthService` package with method signatures for `login`, `register`, `getProfile`, `resetRequest`, `resetConfirm`; throws NotImplemented.|AuthService|DM-001,DM-002|src/auth/auth-service exports class; 5 method signatures match TDD §10/§8; package compiles; placeholder unit tests pass|S|P0|
|16|COMP-006-skel|TokenManager skeleton|Create `TokenManager` package with method signatures for `issueTokens`, `refresh`, `revoke`; throws NotImplemented.|TokenManager|DM-002|class exports 3 method signatures; injects `JwtService` + Redis client via constructor; package compiles|S|P0|
|17|COMP-007a-skel|JwtService skeleton|Create `JwtService` package with `sign(payload)` and `verify(token)` signatures; loads keys at boot.|JwtService|DEP-005,NFR-SEC-002|class exports sign/verify; key loader injected; package compiles; boot fails if key invalid|S|P0|
|18|COMP-007b-skel|PasswordHasher skeleton|Create `PasswordHasher` package wrapping bcryptjs with `hash(plain)` and `verify(plain, hash)` signatures.|PasswordHasher|DEP-004,DEP-006|class exports hash/verify; cost-factor injected via constructor; package compiles|S|P0|
|19|COMP-009|UserRepo skeleton|Create `UserRepo` package abstracting PostgreSQL CRUD over `UserProfile`; methods: `findByEmail`, `findById`, `insert`, `updateLastLogin`, `updatePassword`.|UserRepo|DM-001,DEP-001|5 method signatures; uses pg-pool; transactions supported; package compiles|M|P0|
|20|MIG-004|Feature flag AUTH_NEW_LOGIN|Register `AUTH_NEW_LOGIN` feature flag in config service; default OFF; gating wired into `AuthService.login` entrypoint.|AuthService|-|flag registered; default=OFF; runtime toggle without redeploy; gating callable from request handler; removal target=Phase 3 GA|S|P0|
|21|MIG-005|Feature flag AUTH_TOKEN_REFRESH|Register `AUTH_TOKEN_REFRESH` feature flag in config service; default OFF; gating wired into `TokenManager.refresh`.|TokenManager|-|flag registered; default=OFF; toggle without redeploy; removal target=Phase 3 + 2 weeks|S|P0|
|22|MIG-001|Phase 1 Internal Alpha plan|Document Phase 1 deployment plan: staging deploy, auth-team + QA test all endpoints behind `AUTH_NEW_LOGIN`.|Release|MIG-004|plan published; participants identified; exit=all FR-AUTH-001..005 manual pass + zero P0/P1; duration=1 week|S|P1|
|23|API-VER-001|API URL versioning|Establish `/v1/auth/*` URL-prefix versioning convention with documented breaking-change policy.|APIGateway|-|all auth endpoints mounted under /v1; breaking-change-requires-major-bump documented; deprecation header support added; deprecation policy doc published (resolves TDD §8.4 ambiguity)|S|P1|
|24|ERR-ENV-001|Standard error envelope|Define and implement uniform error envelope `{ error: { code, message, status } }` across all auth endpoints.|AuthService|-|envelope schema documented; codes registered: AUTH_INVALID_CREDENTIALS, AUTH_TOKEN_EXPIRED, AUTH_TOKEN_REVOKED, AUTH_ACCOUNT_LOCKED, AUTH_DUPLICATE_EMAIL, AUTH_WEAK_PASSWORD, AUTH_RESET_TOKEN_INVALID; middleware enforces envelope on all 4xx/5xx|S|P0|
|25|RBAC-DECISION|UserProfile.roles default policy|Document interim policy: roles defaulted to ["user"], not enforced by `AuthService` (deferred to RBAC PRD).|UserRepo|DM-001|roles array constrained to default ["user"] in v1.0; enforcement deferred per TDD NG-003; documented in TDD §3.2 update|XS|P1|

### Integration Points — M1

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|Feature-flag registry|Dispatch|MIG-004,MIG-005|M1|`AuthService.login`, `TokenManager.refresh` (M2/M3/M5)|
|API Gateway rate-limit table|Middleware chain|INFRA-001|M1|All `/v1/auth/*` endpoints (M2/M3)|
|CORS allow-list|Middleware chain|INFRA-003|M1|All cross-origin requests (M3 frontend)|
|Log-redaction middleware|Middleware chain|NFR-SEC-003|M1|All log emitters in `AuthService`/`TokenManager` (M4)|
|Error envelope middleware|Middleware chain|ERR-ENV-001|M1|All 4xx/5xx responses (M2/M3)|
|Pg-pool client|Dependency injection|DEP-001,COMP-009|M1|`UserRepo`, audit-log writer (M2/M4)|
|Redis client|Dependency injection|DEP-002,COMP-006-skel|M1|`TokenManager` (M3)|
|Secrets mount (RSA keys)|Dependency injection|DEP-005,COMP-007a-skel|M1|`JwtService` (M2)|

### Milestone Dependencies — M1

- External: PostgreSQL 15 license/quota approval; Redis 7 cluster provisioning ticket; SendGrid account creation; RSA key-pair generation by sec-team.
- Decisions: CONFLICT-1 (audit retention) and OQ-PRD-3 (lockout policy) must be closed before M1 exit.
- Personnel: platform-team provisions infra; auth-team owns scaffolding; sec-reviewer signs off on key configuration.

### Open Questions — M1

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-CONFLICT-1|Audit log retention: TDD §7.2 specifies 90 days, PRD NFR-COMP-002 mandates 12 months for SOC2. Resolution: PRD precedence (compliance binding); commit 12 months. Affects: AUDIT-001 schema, OPS storage budget, OBS partition strategy. Status: closed|Sizes PostgreSQL retention partition; sets backup window; defines AUDIT-001 acceptance criteria. Without resolution, M1 exit cannot finalize PostgreSQL sizing.|product-team + compliance|2026-04-03|
|2|OQ-PRD-3|Account lockout policy after N consecutive failed login attempts. TDD specifies 5 failures within 15 minutes; PRD lists this as still-open. Resolution: TDD value adopted (5/15min); SEC-001 implementation proceeds. Status: closed|Defines SEC-001 acceptance criteria; without resolution, brute-force mitigation cannot be implemented in M2/M4.|security|2026-04-03|
|3|OQ-OBS-CAPACITY|Projected audit-log write volume at GA (12-month retention)? Required to size PostgreSQL audit partition, backup window, archive policy.|Sizes AUDIT-001 partition; informs OPS-005 capacity plan; risk: under-provisioning causes IO contention with `UserProfile` queries.|platform-team|2026-04-08|
|4|OQ-REMEMBER-ME|Should v1.0 support "remember me" to extend session duration beyond 7-day refresh? Resolution: deferred to v1.1 (out of scope per TDD NG-001-adjacent; 7-day refresh sufficient for v1.0 per PRD metric 'avg session >30min'). Status: closed|If scope expanded, would require new token-type and cookie persistence strategy; currently locked out.|product-team|2026-04-03|

### Risk Assessment and Mitigation — M1

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Infra provisioning slips (PostgreSQL/Redis/SendGrid) push start of M2|High|Medium|All downstream milestones slip; GA at 2026-06-09 jeopardized|Open provisioning tickets in week 1 day 1; parallel paths for each dependency; fallback to dev-managed instances for scaffolding work|platform-team|
|2|RSA key generation/rotation policy ambiguity blocks `JwtService` start|Medium|Medium|`JwtService` boot fails; M2/M3 token issuance blocked|Sec-team to publish key spec + rotation procedure during week 1; pre-generate dev keys for scaffolding|sec-reviewer|
|3|Conflict-1 unresolved past 2026-04-03|High|Low|`AUDIT-001` cannot be designed; blocks M4|Decision pre-staged with compliance officer; default to PRD value (12 months) absent objection by deadline|product-team|

## M2: Core Authentication Logic

**Objective:** Implement `PasswordHasher`, `UserRepo` persistence, and `AuthService.login`/`register` flows end-to-end; first bit of user-visible value through API-001 and API-002. | **Duration:** 2 weeks (Weeks 3-4, 2026-04-13 → 2026-04-24; aligns with TDD M1 commit 2026-04-14) | **Entry:** M1 exit criteria met; skeleton packages compile; PostgreSQL/Redis provisioned; feature flags registered (default OFF). | **Exit:** FR-AUTH-001 + FR-AUTH-002 implemented and covered by passing unit + integration tests against testcontainers PostgreSQL; `PasswordHasher` bcrypt cost 12 verified; API-001 + API-002 return correct envelopes for success/error paths; unit coverage on `AuthService`+`PasswordHasher`+`UserRepo` ≥80%; p95 latency <200ms on staging (preliminary measurement).

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|26|FR-AUTH-001|Login with email/password|Implement `AuthService.login` orchestrating `UserRepo.findByEmail` → `PasswordHasher.verify` → `TokenManager.issueTokens` (stubbed in M2, wired in M3).|AuthService|COMP-005-skel,COMP-009,COMP-007b-skel|valid creds→200 with `AuthToken`; invalid creds→401 AUTH_INVALID_CREDENTIALS; unknown email→401 same message (no enumeration); email lowercased before lookup; lastLoginAt updated on success; counts as failed attempt if invalid|L|P0|
|27|FR-AUTH-002|User registration with validation|Implement `AuthService.register`: validate email format, enforce password policy (≥8 chars, 1 uppercase, 1 digit), check uniqueness, `PasswordHasher.hash`, `UserRepo.insert`.|AuthService|COMP-005-skel,COMP-009,COMP-007b-skel|201 returns `UserProfile`; weak-password→400 AUTH_WEAK_PASSWORD with field-specific reasons; duplicate email→409 AUTH_DUPLICATE_EMAIL; email lowercase-normalized before insert; password never logged; GDPR consent flag recorded|L|P0|
|28|API-001|POST /v1/auth/login|Wire `AuthService.login` to POST `/v1/auth/login` route; apply rate-limit middleware, error envelope, log redaction.|AuthService|FR-AUTH-001,INFRA-001,ERR-ENV-001|route mounted at /v1/auth/login; rate-limit 10rpm/IP enforced before handler; request schema `{email,password}` validated; 200 returns `AuthToken`; 401 AUTH_INVALID_CREDENTIALS; 423 AUTH_ACCOUNT_LOCKED; 429 rate-limit with Retry-After; OpenAPI spec committed|M|P0|
|29|API-002|POST /v1/auth/register|Wire `AuthService.register` to POST `/v1/auth/register`; apply rate-limit, validation, envelope.|AuthService|FR-AUTH-002,INFRA-001,ERR-ENV-001|route mounted; 5rpm/IP rate limit; schema `{email,password,displayName}` validated; 201 returns `UserProfile`; 400 AUTH_WEAK_PASSWORD; 409 AUTH_DUPLICATE_EMAIL; OpenAPI spec committed|M|P0|
|30|COMP-005|AuthService implementation|Full implementation of `AuthService.login` and `AuthService.register`; remaining methods (`getProfile`, `resetRequest`, `resetConfirm`) left as stubs for M3.|AuthService|FR-AUTH-001,FR-AUTH-002|login+register implemented; getProfile/resetRequest/resetConfirm throw NotImplemented; dependency injection for `UserRepo`,`PasswordHasher`,`TokenManager`,`EmailClient`; methods observable by logger|L|P0|
|31|COMP-007b|PasswordHasher implementation|Implement `PasswordHasher.hash(plain)` and `PasswordHasher.verify(plain, hash)` using bcryptjs with injected cost factor.|PasswordHasher|DEP-004,NFR-SEC-001|hash() returns bcrypt hash with cost=12; verify() returns bool; constant-time comparison; unit test asserts stored hash begins `$2b$12$`; benchmark asserts <500ms/hash on target hardware|M|P0|
|32|COMP-009|UserRepo implementation|Implement `findByEmail`, `findById`, `insert`, `updateLastLogin`, `updatePassword` against PostgreSQL via pg-pool.|UserRepo|DEP-001,DM-001|5 methods implemented; transactions used for insert; email lookup is case-insensitive via lowercase index; connection-pool error surfaces as retryable; integration test hits testcontainer PostgreSQL|L|P0|
|33|NFR-SEC-001|bcrypt cost factor 12|Enforce bcrypt cost factor 12 for all password hashing; prevent lower cost in configuration.|PasswordHasher|COMP-007b|env BCRYPT_COST=12 asserted on boot; config validation refuses <10; unit test asserts hash prefix $2b$12$; benchmark <500ms|S|P0|
|34|SEC-003|Password strength policy|Enforce ≥8 chars, 1 uppercase, 1 number, 1 symbol in registration; return field-level error list.|AuthService|FR-AUTH-002|validator rejects <8 chars, missing uppercase, missing digit; AC checks each rule separately; errors returned as array; NIST SP 800-63B 5.1.1.2 alignment documented|S|P0|
|35|SEC-004|User enumeration prevention|Ensure invalid-email and wrong-password paths return identical timing + envelope; reset-request returns same envelope regardless of email registration.|AuthService|FR-AUTH-001|timing variance <50ms between known/unknown email measured; identical 401 AUTH_INVALID_CREDENTIALS envelope; dummy bcrypt comparison runs on unknown email; /auth/reset-request always returns 200 (no 404)|M|P0|
|36|TEST-001|Unit: login valid credentials|`AuthService.login` with valid email/password returns `AuthToken` via mocked `PasswordHasher.verify`→true and `TokenManager.issueTokens`.|Tests|FR-AUTH-001|test passes; mocks asserted; assertion covers both accessToken and refreshToken presence; coverage counted toward 80%|S|P0|
|37|TEST-002|Unit: login invalid credentials|`AuthService.login` with invalid password returns 401; no `AuthToken` issued; failed-attempt counter incremented.|Tests|FR-AUTH-001,SEC-001-stub|test passes; mock `PasswordHasher.verify`→false; assertion verifies no token issuance and correct error envelope|S|P0|
|38|TEST-004|Integration: registration persists UserProfile|Integration test against testcontainer PostgreSQL: POST /v1/auth/register creates row in `users` with bcrypt hash.|Tests|FR-AUTH-002,COMP-009|testcontainer boots PostgreSQL 15; register call returns 201; row present with correct email, displayName, password_hash starts $2b$12$; cleanup tears down container|M|P0|
|39|TEST-DUP-EMAIL|Integration: duplicate email rejected|Integration test asserts second registration with same email returns 409 without double-insert.|Tests|FR-AUTH-002|testcontainer; two registers back-to-back; second returns 409 AUTH_DUPLICATE_EMAIL; only one row in DB; email case-insensitive (E@X.com vs e@x.com)|S|P0|
|40|TEST-WEAK-PWD|Integration: weak password rejected|Integration test asserts weak passwords return 400 with structured error list.|Tests|FR-AUTH-002,SEC-003|tests: "short" (<8), "longpass1" (no uppercase), "LongPass" (no digit), "LongPass1!" accepted; error response includes array of failed rules|S|P0|
|41|MIG-001-exec|Phase 1 Internal Alpha execution|Deploy M2 artifacts to staging behind `AUTH_NEW_LOGIN`=ON for auth-team + QA tenants; run manual test plan.|Release|MIG-001,MIG-004|deploy artifact tagged; flag enabled for auth-team tenants only; manual checklist executed; exit=0 P0/P1; sign-off from test-lead captured|M|P0|
|42|PERF-BASELINE|Preliminary p95 latency baseline|Measure p95 latency of `/v1/auth/login` and `/v1/auth/register` on staging with 10-50 concurrent users.|Tests|TEST-004|k6 scenario published; p95 captured at 10/25/50 concurrent; baseline stored in APM for comparison in M3/M4; target <200ms; flag if exceeds for M3 optimization|S|P1|
|43|NFR-COMP-003|NIST SP 800-63B conformance|Document password-storage conformance: bcrypt cost 12, no plaintext, no reversible encoding, no password hints.|AuthService|SEC-003,NFR-SEC-001|conformance checklist published; links to 800-63B section 5.1.1.2; reviewed by sec-reviewer; field-list of stored data matches PRD data-minimization requirement (email, hash, displayName only)|S|P0|
|44|NFR-COMP-001-stub|GDPR consent capture (stub)|Register consent checkbox in registration request body; persist consent timestamp with `UserProfile` (full consent review in M4).|AuthService|FR-AUTH-002|register request accepts `consentAccepted:boolean` + `consentTimestamp:ISO8601`; rejected if consent not true; stored in new consent table or UserProfile column; full compliance review deferred to M4 (NFR-COMP-001)|S|P0|
|45|TOKEN-STUB|TokenManager stub (login path)|Provide minimal `TokenManager.issueTokens` returning pair of random opaque tokens (no JWT yet) so M2 login path is testable end-to-end.|TokenManager|COMP-006-skel|stub returns `AuthToken` with tokenType="Bearer"; refresh mechanics not yet functional; clearly marked TEMPORARY with removal ticket; replaced by COMP-006 in M3|S|P0|
|46|SEC-LOGGING-M2|Auth-event logging (application layer)|Emit structured log on login success/failure and register success/failure (application-level stdout/JSON, not yet in audit DB).|Logging|NFR-SEC-003|each event emits `{event,user_id|email_hash,outcome,ip,timestamp}`; password/tokens redacted; feeds into downstream AUDIT-001 DB writer in M4|S|P0|
|47|DOC-API-M2|OpenAPI 3 spec for login + register|Publish OpenAPI spec covering API-001 + API-002 including schemas and error codes.|Docs|API-001,API-002|spec validated; /v1/auth/login + /v1/auth/register documented with 200/201/400/401/409/423/429 responses; error-envelope schema defined; spec committed to repo|S|P1|
|48|REFLECT-M2|M2 architecture review checkpoint|Conduct architecture review with sys-architect before M3: verify `TokenManager`/`JwtService` contract ready for integration.|Meta|COMP-005,COMP-009|review meeting held; action items tracked; `AuthService`-`TokenManager` integration contract frozen; sign-off from sys-architect|S|P1|

### Integration Points — M2

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|`UserRepo` injection into `AuthService`|Dependency injection|COMP-005,COMP-009|M2|`AuthService.login`, `AuthService.register`|
|`PasswordHasher` injection into `AuthService`|Dependency injection|COMP-005,COMP-007b|M2|login verify + register hash paths|
|Password-policy validator registry|Strategy pattern|SEC-003|M2|`AuthService.register`; extensible for future NIST rule additions|
|Rate-limit middleware wiring|Middleware chain|API-001,API-002|M2|All POST endpoints; extensible in M3 to /auth/refresh, /auth/me, reset endpoints|
|Error-envelope middleware wiring|Middleware chain|ERR-ENV-001|M1→M2|All error responses from new endpoints|
|Consent-capture table/column|Schema wiring|NFR-COMP-001-stub|M2|Full compliance workflow in M4|

### Milestone Dependencies — M2

- M1 infra provisioning complete (PostgreSQL/Redis reachable from staging CI).
- M1 scaffolding merged to main; feature flags registered.
- OQ-PRD-3 lockout policy resolution (5/15min) applied to SEC-001 stub wiring for failed-attempt counter.

### Open Questions — M2

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-PRD-1|Should password reset emails be sent synchronously or asynchronously? Resolution: asynchronous via job queue (better resilience under SendGrid outages; aligns with PRD "60-second delivery" budget while avoiding request-path coupling). Status: closed|Defines queue infrastructure need for M3 email integration; sync path would block `/auth/reset-request` on SendGrid latency.|engineering|2026-04-17|
|2|OQ-FAILED-COUNTER-STORE|Where to store failed-login attempt counts for lockout: Redis (fast, TTL-native, non-durable) vs PostgreSQL (durable, slower). Proposal: Redis with 15-min TTL matching lockout window; audit record mirrored to PostgreSQL for compliance.|SEC-001 implementation choice; affects OPS capacity plan and AUDIT-001 event volume.|security + auth-team|2026-04-20|

### Risk Assessment and Mitigation — M2

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|bcrypt cost 12 exceeds 200ms p95 budget on target hardware|High|Medium|NFR-PERF-001 violated from M2 onward; user-visible latency|PERF-BASELINE in week 4; profile to find CPU headroom; option to scale `AuthService` pods vertically|platform-team|
|2|Password-policy strictness harms PRD "60s registration" goal|Medium|Medium|Registration conversion <60%|Client-side inline validation in M3 `RegisterPage`; field-level error detail in API-002 response|product + frontend|
|3|Timing-attack sidechannel on unknown-email path|Medium|Medium|User enumeration leak|Dummy bcrypt.verify on unknown-email path; test measures timing variance <50ms|security|
|4|GDPR consent stub inadequate for full compliance|Medium|Medium|Blocks SOC2/GDPR certification|Full NFR-COMP-001 review scheduled in M4; stub captures sufficient data now|compliance|

## M3: Integration, Tokens & Frontend

**Objective:** Replace TOKEN-STUB with `TokenManager`+`JwtService`; deliver refresh flow, profile retrieval, password reset; ship `LoginPage`/`RegisterPage`/`ProfilePage`/`AuthProvider`; complete FR-AUTH-003/004/005 end-to-end. | **Duration:** 3 weeks (Weeks 5-7, 2026-04-27 → 2026-05-15; aligns with TDD M2 2026-04-28 and TDD M3 2026-05-12) | **Entry:** M2 exit met; FR-AUTH-001/002 live behind flag. | **Exit:** FR-AUTH-003/004/005 implemented and tested; API-003/004/005/006 return correct envelopes; frontend components render, integrate with `AuthProvider`, and handle silent refresh + 401 interception; Phase 2 beta (10%) ready to enable in M5; integration tests for expired/revoked refresh tokens pass against testcontainer Redis; E2E test passes on staging.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|49|FR-AUTH-003|JWT issuance + refresh|Replace stub with real `TokenManager.issueTokens` (JWT access 15min, refresh opaque 7d hashed in Redis) and `TokenManager.refresh` rotating both tokens.|TokenManager|COMP-006,COMP-007a,FR-AUTH-001|login returns RS256 JWT with 15-min expiry payload {sub:user.id,roles,iat,exp}; refresh token SHA-256 hashed before Redis SET with 7-day TTL; /v1/auth/refresh with valid token rotates both; expired or revoked→401 AUTH_TOKEN_EXPIRED/REVOKED; clock-skew tolerance=5s on verify|L|P0|
|50|FR-AUTH-004|User profile retrieval|Implement `AuthService.getProfile` returning `UserProfile` derived from JWT `sub`; wire GET /v1/auth/me.|AuthService|COMP-009,FR-AUTH-003|GET /v1/auth/me with Bearer JWT returns id, email, displayName, createdAt, updatedAt, lastLoginAt, roles; 401 on missing/expired/invalid token; 60rpm/user rate limit enforced; response matches DM-001 exactly|M|P0|
|51|FR-AUTH-005|Password reset flow|Implement two-step reset: `resetRequest` issues 1-hour single-use token, enqueues email via async queue; `resetConfirm` validates token, updates hash via `PasswordHasher`, invalidates all refresh tokens for user.|AuthService|DEP-006,COMP-007b,COMP-006|/v1/auth/reset-request returns 200 regardless of email existence (no enumeration); token TTL=3600s; single-use (deleted on consume); /v1/auth/reset-confirm validates token, rehashes password cost=12, deletes all refresh tokens for user_id from Redis; used token cannot be replayed; weak-password rejected|L|P0|
|52|API-003|GET /v1/auth/me|Wire `AuthService.getProfile` to GET /v1/auth/me with auth middleware.|AuthService|FR-AUTH-004|Bearer auth required; 200 returns `UserProfile` JSON per DM-001; 401 AUTH_TOKEN_EXPIRED or AUTH_TOKEN_INVALID; 60rpm/user rate limit; OpenAPI spec updated|M|P0|
|53|API-004|POST /v1/auth/refresh|Wire `TokenManager.refresh` to POST /v1/auth/refresh.|TokenManager|FR-AUTH-003|body `{refreshToken}` validated; 200 returns rotated `AuthToken`; old refresh token deleted from Redis; 401 AUTH_TOKEN_EXPIRED; 401 AUTH_TOKEN_REVOKED; 30rpm/user rate limit; OpenAPI spec updated|M|P0|
|54|API-005|POST /v1/auth/reset-request|Wire `AuthService.resetRequest` to POST /v1/auth/reset-request.|AuthService|FR-AUTH-005|body `{email}` validated; always returns 200 with generic message regardless of registration; rate-limit configured (TDD was TBD; commit 3rpm/IP); OpenAPI spec updated|M|P0|
|55|API-006|POST /v1/auth/reset-confirm|Wire `AuthService.resetConfirm` to POST /v1/auth/reset-confirm.|AuthService|FR-AUTH-005|body `{token,newPassword}` validated; 200 on success; 400 AUTH_RESET_TOKEN_INVALID for invalid/expired/used token; 400 AUTH_WEAK_PASSWORD; all refresh tokens for user invalidated after confirm (per PRD FR-AUTH.5); rate-limit 3rpm/IP; OpenAPI spec updated|M|P0|
|56|COMP-006|TokenManager implementation|Full implementation of `issueTokens`, `refresh`, `revoke`, `revokeAllForUser` backed by Redis.|TokenManager|FR-AUTH-003|issueTokens signs access via `JwtService.sign` + random refresh token, SHA-256 hashes it, SET key=refresh:{hash} val={user_id,issued_at} EX 604800; refresh: GET→rotate→DEL→new tokens; revoke: DEL; revokeAllForUser: SCAN refresh:*, filter by user_id, DEL; all methods observable|L|P0|
|57|COMP-007a|JwtService implementation|Full implementation of `sign(payload)` and `verify(token)` with RS256 2048-bit keys; expose `verify` errors distinguishing expired vs malformed vs invalid-signature.|JwtService|DEP-005,NFR-SEC-002|sign: RS256 with private key from secrets; 15-min exp; iss/aud claims set; verify: returns decoded payload or typed error (TokenExpiredError, JsonWebTokenError, NotBeforeError); clock-skew=5s|M|P0|
|58|COMP-001|LoginPage|React route /login: email/password form, submit→POST /v1/auth/login via AuthProvider, inline errors, CAPTCHA trigger after 3 failed client-side attempts.|LoginPage|API-001,COMP-004|props:{onSuccess:()=>void,redirectUrl?:string}; form validates email format; on-success calls `AuthProvider.setAuth(AuthToken)` + redirect; on-401 shows "Invalid email or password" (generic); on-423 shows lockout message; client counter triggers hCaptcha after 3 failed attempts (R-002 mitigation); keyboard accessible|L|P0|
|59|COMP-002|RegisterPage|React route /register: email/password/displayName form with client-side password-strength meter + GDPR consent checkbox; submit→POST /v1/auth/register.|RegisterPage|API-002,NFR-COMP-001-stub|props:{onSuccess:()=>void,termsUrl:string}; password-strength meter shows rule status; displayName 2-100 chars validated; consent checkbox mandatory (links to termsUrl); on-success shows confirmation + redirects to /login; 409 shows "email already registered"|L|P0|
|60|COMP-003|ProfilePage|React route /profile (auth-required): displays `UserProfile` from GET /v1/auth/me.|ProfilePage|API-003,COMP-004|shows displayName, email, createdAt; renders loading+error states; redirects to /login on 401; page renders <1s on staging|M|P0|
|61|COMP-004|AuthProvider|React Context managing `AuthToken` state: in-memory accessToken, HttpOnly-cookie refreshToken, 401 interceptor, silent refresh, protected-route guard.|AuthProvider|API-004,API-003|provides {user,login,logout,refresh}; accessToken held in memory only (never localStorage); refreshToken in HttpOnly+Secure+SameSite=Strict cookie; axios/fetch interceptor catches 401 → call refresh → retry original request once; protected-route wrapper redirects to /login on no-auth; on-logout revokes refresh + clears state|L|P0|
|62|TEST-003|Unit: token refresh with valid refresh token|`TokenManager.refresh` with valid token rotates pair via `JwtService` and deletes old Redis key.|Tests|FR-AUTH-003|mock Redis GET→valid payload, SET/DEL asserted; `JwtService.sign` called twice; returned pair differs from input; unit covers FR-AUTH-003 AC2|S|P0|
|63|TEST-005|Integration: expired refresh token rejected|Integration test against testcontainer Redis: set key with TTL=1s, wait 2s, call refresh → 401 AUTH_TOKEN_EXPIRED.|Tests|COMP-006|testcontainer Redis; TTL asserted via EXPIRE; after sleep 2s, /v1/auth/refresh returns 401; covers FR-AUTH-003 AC3|M|P0|
|64|TEST-REVOKE|Integration: revoked refresh token rejected|Refresh→revoke→refresh-again asserts second refresh returns 401 AUTH_TOKEN_REVOKED.|Tests|COMP-006|first refresh succeeds; subsequent refresh with old token returns 401 (rotated); covers FR-AUTH-003 AC4|S|P0|
|65|TEST-RESET-FLOW|Integration: full password-reset flow|End-to-end reset flow against testcontainers: request→token persisted with TTL→confirm updates hash→all refresh tokens for user deleted.|Tests|FR-AUTH-005|testcontainer PostgreSQL+Redis; reset-request emits token (mock email client); reset-confirm updates password_hash to new bcrypt; old hash rejected on subsequent login; existing refresh tokens for user removed from Redis; reset token single-use verified|M|P0|
|66|TEST-006|E2E: user registers and logs in|Playwright E2E: RegisterPage→LoginPage→ProfilePage journey covering FR-AUTH-001+002+004.|Tests|COMP-001,COMP-002,COMP-003,COMP-004|Playwright script passes on staging; covers register with fresh email, login with same creds, profile shows correct data, silent refresh observed via network log; runs in CI nightly|L|P0|
|67|TEST-E2E-RESET|E2E: password reset journey|Playwright E2E: reset-request→confirm→login-with-new-password; asserts existing session invalidated.|Tests|COMP-001,FR-AUTH-005|Playwright script: forgot-password flow; mock-email intercept extracts token; confirm with new password; login with new password succeeds + old password fails; pre-existing session on second browser context confirms logout|M|P0|
|68|ASYNC-QUEUE|Async email-send worker|Implement async job queue (BullMQ or equivalent on Redis) that processes reset-email jobs asynchronously.|EmailClient|DEP-002,FR-AUTH-005,OQ-PRD-1|queue created; worker processes jobs; retries on SendGrid 5xx (3 attempts exponential backoff); dead-letter queue configured; metric `auth_reset_email_send_total`|M|P0|
|69|CAPTCHA-INTEG|Client-side CAPTCHA after 3 failures|Integrate hCaptcha/reCAPTCHA into LoginPage after 3 consecutive client-side failures.|LoginPage|COMP-001|provider key wired; widget renders on 4th attempt; token submitted with /v1/auth/login request; server-side verify hook skipped in v1.0 (client-side deterrent only; R-002 primary mitigation remains server-side lockout)|S|P1|
|70|NFR-PERF-001-M3|API p95 latency budget|Reconfirm NFR-PERF-001: all /v1/auth/* p95 <200ms under load with real `TokenManager`+`JwtService`+Redis.|Perf|FR-AUTH-003,FR-AUTH-004|k6 scenario at 50/100/250 concurrent; p95 <200ms verified per endpoint; APM dashboards record baseline; regression gate set at +20%|M|P0|
|71|NFR-PERF-002|500 concurrent logins|Load test with 500 concurrent /v1/auth/login; target sustained p95 <200ms.|Perf|NFR-PERF-001-M3|k6 script at 500 concurrent; p95 <200ms sustained ≥2 min; error rate <0.1%; PostgreSQL connection pool not exhausted (wait <50ms); Redis latency <10ms|L|P0|
|72|MIG-002-prep|Phase 2 Beta rollout prep|Prepare traffic-split configuration for 10% beta; publish monitoring dashboards for latency + errors + Redis usage.|Release|MIG-004,NFR-PERF-001-M3|10% cohort definition published; `AUTH_NEW_LOGIN` flag supports percentage rollout; dashboards: login-latency, error-rate, Redis-conn-failures; rollback playbook reviewed|M|P1|
|73|SEC-001|Account lockout 5 failures / 15 min|Implement lockout: 5 failed `AuthService.login` within 15-minute rolling window returns 423 AUTH_ACCOUNT_LOCKED; auto-unlock at 15-min mark.|AuthService|OQ-FAILED-COUNTER-STORE,FR-AUTH-001|failed-counter in Redis keyed by user-email hash + IP, TTL=900s; 5th failure sets `lock:{email}` key TTL=900s; subsequent logins return 423 until expiry; successful login clears counter; lockout event logged for audit|M|P0|
|74|ADMIN-001|Audit log query endpoint (admin)|Implement GET /v1/auth/admin/events with role-gated auth (`roles` contains "admin") for Jordan persona (JTBD-gap-2).|AuthService|DM-001|endpoint returns paginated audit entries filtered by user_id, event_type, date range; requires admin role in JWT; 403 otherwise; resolves JTBD-gap-2|M|P1|
|75|PRD-GAP-LOGOUT|POST /v1/auth/logout endpoint|Implement dedicated logout endpoint revoking current refresh token + clearing AuthProvider state (PRD AUTH-E1 logout story, absent in TDD).|AuthService|COMP-006,COMP-004|POST /v1/auth/logout accepts current accessToken; calls `TokenManager.revoke` on the session's refresh token; returns 204; frontend `AuthProvider.logout` calls endpoint then clears state; HttpOnly cookie cleared server-side|M|P0|
|76|FE-ERROR-HANDLING|Frontend error UX for all auth codes|Map every error code (AUTH_INVALID_CREDENTIALS, AUTH_ACCOUNT_LOCKED, AUTH_WEAK_PASSWORD, AUTH_DUPLICATE_EMAIL, AUTH_RESET_TOKEN_INVALID, AUTH_TOKEN_EXPIRED, AUTH_TOKEN_REVOKED) to user-friendly messages in `AuthProvider`.|AuthProvider|ERR-ENV-001|error-code→message map published; each code has message and optional action CTA (retry, reset, re-login); i18n-ready keys; unit test per code|S|P1|
|77|FE-CLOCK-SKEW|Client-side silent refresh timing|Schedule `AuthProvider` silent refresh at exp-60s (not exp) to avoid race with server clock skew.|AuthProvider|COMP-004|accessToken decoded client-side; refresh timer set to (exp - 60) seconds; covers 5-sec clock skew + network jitter; if refresh fails, redirect to /login|S|P1|
|78|DOC-API-M3|OpenAPI spec for all 6 auth endpoints|Extend OpenAPI spec to cover API-003/004/005/006 + /v1/auth/logout.|Docs|API-003,API-004,API-005,API-006,PRD-GAP-LOGOUT|all 7 endpoints documented; full request/response schemas; all error codes enumerated; versioning policy referenced|S|P1|
|79|CORS-PREFLIGHT-TEST|CORS preflight integration test|Integration test verifies preflight OPTIONS returns correct Allow-Origin / Allow-Credentials for allowed origins; rejects others.|Tests|INFRA-003|preflight returns 204 + Access-Control-Allow-Origin for app.platform.com; preflight returns 403 for evil.com; credentials=true propagated|S|P1|
|80|RSA-KEY-ROTATION|RSA key rotation documentation + script|Document quarterly key rotation; script that generates new key, updates secret, supports overlap (old key verifies, new key signs for 24h).|JwtService|COMP-007a|rotation runbook published; script tested in staging; overlap window verified (tokens signed with old key still valid for their remaining TTL after rotation); rotation schedule in ops calendar|M|P1|
|81|DECOMP-EMAIL-TEMPLATE|Reset-email template finalization|Finalize SendGrid transactional email template copy + variables for reset link.|EmailClient|DEP-006,FR-AUTH-005|template approved by product; variables: display_name, reset_link, expires_at; plain-text fallback; sandbox send + rendering verified|S|P1|
|82|REFLECT-M3|M3 integration review checkpoint|Architecture review confirming readiness for M4 hardening phase.|Meta|ALL M3|review held; action items tracked; sign-offs from sys-architect + sec-reviewer|S|P1|

### Integration Points — M3

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|`TokenManager` injection into `AuthService`|Dependency injection|COMP-005,COMP-006|M3|login/register/reset-confirm paths|
|`JwtService` injection into `TokenManager`|Dependency injection|COMP-006,COMP-007a|M3|issueTokens + refresh + verify|
|401 response interceptor|Middleware chain (client)|COMP-004|M3|All protected frontend calls; triggers silent refresh|
|Protected-route guard|Callback registry (client)|COMP-004|M3|ProfilePage + future authenticated routes|
|Async email worker|Event binding / dispatch|ASYNC-QUEUE|M3|reset-request → queue → SendGrid|
|Error-code→UX-message map|Strategy pattern (client)|FE-ERROR-HANDLING|M3|All auth form/error displays|
|Role-gate middleware|Middleware chain|ADMIN-001|M3|ADMIN-001 endpoint; extensible to future admin routes|
|Refresh-rotation strategy|Strategy pattern|COMP-006|M3|Both /auth/refresh and /auth/reset-confirm (revokeAllForUser)|

### Milestone Dependencies — M3

- M2 FR-AUTH-001/002 live; `AuthService` integration contract frozen.
- OQ-PRD-1 resolved (async); async queue infra deployed alongside Redis.
- OQ-FAILED-COUNTER-STORE resolved (Redis) before SEC-001 implementation.

### Open Questions — M3

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-PRD-2|Maximum refresh tokens allowed per user across devices? Options: unlimited (current TDD implicit) vs device-cap N. Resolution proposal: unlimited in v1.0 + metric `auth_refresh_tokens_per_user` for observation; revisit in v1.1 if median >10. Status: tentative|Without cap, token theft on one device persists across others; with cap, multi-device users may churn tokens. Affects Redis memory sizing.|product|2026-05-01|
|2|OQ-JTBD-4|PRD JTBD #4 (Sam the API consumer programmatic auth) has no FR — refresh via FR-AUTH-003 covers human-refresh flow but no service-account/API-key path exists. Resolution: deferred to v1.1 per TDD NG-001 scope decision; acknowledged gap. Status: closed (deferred)|Feature-parity gap with JTBD #4; service-to-service auth remains on ad-hoc API keys until v1.1.|product|2026-05-01|
|3|OQ-OQ-001|Should `AuthService` support API-key auth for service-to-service calls? (TDD OQ-001). Resolution: deferred to v1.1 (confirmed).|Same as OQ-JTBD-4; forces interim solution for internal services calling each other.|test-lead|2026-04-15|
|4|OQ-OQ-002|Maximum `UserProfile.roles` array length? (TDD OQ-002). Resolution: soft-cap at 16 via application-layer validation in M4; hard schema cap deferred to RBAC PRD. Status: tentative|Defines `UserRepo.insert` validation; affects JWT payload size (16 roles ≈ 300 bytes additional).|auth-team + RBAC-PRD owner|2026-05-08|

### Risk Assessment and Mitigation — M3

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|`AuthProvider` silent-refresh race causes request failures|High|Medium|Users experience random 401s; degraded UX|FE-CLOCK-SKEW (refresh at exp-60s); request-queue hold during refresh; retry-once on 401|frontend|
|2|Redis refresh-token hot key during peak|Medium|Medium|Login/refresh slowdown|Key sharding by user-id prefix; Redis cluster mode in production; monitoring alert on key latency|platform-team|
|3|XSS → accessToken theft (R-001)|Medium|High|Session hijacking|In-memory accessToken (never localStorage); HttpOnly refreshToken cookie; CSP policy restrictive; token expiry 15min|sec-reviewer + frontend|
|4|Reset email delivery failure blocks recovery (R-PRD-004)|Low|Medium|Alex cannot regain access|Async queue with retries + DLQ; alert on DLQ growth; fallback support channel documented|platform-team|
|5|Session fixation on concurrent logins|Low|Medium|Ambiguous session ownership|Each login issues fresh tokens; no token reuse across logins; test covers concurrent logins on same account|security|

## M4: Hardening, Observability & Compliance

**Objective:** Instrument full observability (logs/metrics/traces/alerts), wire durable audit logging (12-month SOC2 retention), finalize security review + pen-test, complete GDPR consent + NIST compliance artifacts. | **Duration:** 2 weeks (Weeks 8-9, 2026-05-18 → 2026-05-29; aligns with TDD M4 2026-05-26) | **Entry:** M3 FR-AUTH-003/004/005 functional; 10% beta ready to ramp; pen-test vendor engaged. | **Exit:** Structured logs + Prometheus metrics + OpenTelemetry traces + Grafana alerts live in staging; AUDIT-001 writing to PostgreSQL 12-month partition; pen-test PASS with zero High/Critical unaddressed; GDPR consent workflow complete; runbooks drafted; NFR-REL-001 health-check wired.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|83|OBS-001|Structured logging implementation|Instrument `AuthService`, `TokenManager`, `JwtService`, `PasswordHasher`, `UserRepo` with structured JSON logs for every method entry/exit/error.|Logging|NFR-SEC-003,SEC-LOGGING-M2|each method emits {level, ts, trace_id, span_id, service, method, user_id|email_hash, outcome, duration_ms}; password/token/newPassword fields redacted; log-schema documented; 100% method coverage verified|M|P0|
|84|OBS-002|Metric: auth_login_total|Implement Prometheus counter `auth_login_total{outcome}` incremented on each login outcome.|Logging|OBS-001|counter registered; labels: outcome=success|invalid_creds|locked|rate_limited; incremented in `AuthService.login` exit paths; Prometheus scrape endpoint exposes metric|S|P0|
|85|OBS-003|Metric: auth_login_duration_seconds|Implement Prometheus histogram `auth_login_duration_seconds` with buckets [0.01,0.025,0.05,0.1,0.2,0.5,1,2].|Logging|OBS-001|histogram registered; observes each login wall-clock; buckets chosen to resolve around 200ms budget; p95 quantile queryable in Grafana|S|P0|
|86|OBS-004|Metric: auth_token_refresh_total|Implement Prometheus counter `auth_token_refresh_total{outcome}` for refresh outcomes.|Logging|OBS-001|counter labels: outcome=success|expired|revoked|invalid; incremented in `TokenManager.refresh`|S|P0|
|87|OBS-005|Metric: auth_registration_total|Implement Prometheus counter `auth_registration_total{outcome}` for register outcomes.|Logging|OBS-001|labels: outcome=success|validation_error|duplicate_email; incremented in `AuthService.register`|S|P0|
|88|OBS-006|OpenTelemetry tracing spans|Instrument tracing across `AuthService`→`PasswordHasher`→`TokenManager`→`JwtService`→`UserRepo`→PostgreSQL/Redis calls.|Logging|OBS-001|each cross-component call creates OTEL span with parent-child relationship; trace exports to collector; trace_id propagates in logs (OBS-001); staging trace viewable end-to-end in Grafana Tempo/Jaeger|M|P0|
|89|OBS-007|Alert: login failure rate|Prometheus alert rule: login failure rate >20% over 5-min window → pager.|Logging|OBS-002|rule: `sum(rate(auth_login_total{outcome!="success"}[5m])) / sum(rate(auth_login_total[5m])) > 0.2`; severity=warning for >20%; severity=critical for >50%; PagerDuty integration|S|P0|
|90|OBS-008|Alert: p95 latency breach|Prometheus alert rule: p95 `auth_login_duration_seconds` >500ms for 5 min → pager.|Logging|OBS-003|rule: `histogram_quantile(0.95, rate(auth_login_duration_seconds_bucket[5m])) > 0.5`; severity=warning; reference NFR-PERF-001 200ms budget vs 500ms alert threshold (degradation not rollback)|S|P0|
|91|OBS-009|Alert: Redis connection failures|Prometheus alert rule: Redis connection-failure count >10/min → pager.|Logging|OBS-001|rule: rate of Redis error log lines; severity=critical; separate from generic-infra alert; escalation to platform-team|S|P0|
|92|OBS-ROLLBACK-TRIGGERS|Automated rollback trigger wiring|Distinct alert rules for rollback-level conditions (p95>1000ms 5min, error rate >5% 2min, Redis failures >10/min, UserProfile data corruption) → trigger automated feature-flag flip via runbook automation.|Logging|OBS-007,OBS-008,OBS-009|four rollback-level rules distinct from OBS-007/008 (which are degradation-level); each triggers runbook playbook (not manual page); dry-run tested in staging; documented in TDD §19.4|M|P0|
|93|AUDIT-001|Audit log table schema|Create `auth_audit_log` PostgreSQL table with 12-month retention partition (per OQ-CONFLICT-1 resolution).|UserRepo|DEP-001,OQ-CONFLICT-1|columns: id:UUID-PK; user_id:UUID-FK-nullable; event_type:varchar; ip_address:inet; user_agent:varchar; outcome:varchar; metadata:jsonb; created_at:timestamptz-NOT-NULL; partitioned by month; 12-month retention via pg_partman; indexed on (user_id,created_at)|M|P0|
|94|AUDIT-002|Audit log writer|Implement append-only writer invoked from every auth event emitter (login, register, refresh, reset, lockout, logout).|UserRepo|AUDIT-001,OBS-001|writer exposes `logEvent({user_id,event_type,ip,user_agent,outcome,metadata})`; called from login success/fail, register, refresh success/fail, reset-request, reset-confirm, lockout, logout; insert lag <100ms p95; write failures logged but do not fail the request (fire-and-forget with buffer)|M|P0|
|95|AUDIT-003|Audit log fields compliance|Verify AUDIT-001 schema includes all SOC2-required fields: user_id, timestamp, IP, outcome, event_type.|Compliance|AUDIT-001,AUDIT-002|compliance checklist reviewed by compliance owner; mapping document links each SOC2 control to column; 12-month retention + backup verified|S|P0|
|96|NFR-COMP-001|GDPR consent workflow complete|Finalize consent capture: store consent_timestamp + consent_version; expose consent history via /v1/auth/me extended; DSAR export API groundwork.|AuthService|NFR-COMP-001-stub|registration requires consent=true + consent_version stored; `UserProfile` response includes consent_timestamp + consent_version; DSAR-export stub endpoint returns consent record plus UserProfile; consent withdrawal flow deferred to v1.1 (documented)|M|P0|
|97|NFR-COMP-002|SOC2 audit logging complete (12-month retention)|Complete SOC2 audit-logging deliverable with 12-month retention and query interface.|Compliance|AUDIT-001,AUDIT-002,AUDIT-003|12-month partition retention verified by test (insert date+400d → partition pruned); query latency for 12-month range <3s on indexed user_id; audit-log backup daily; restore procedure tested; compliance sign-off obtained|M|P0|
|98|NFR-REL-001|99.9% uptime health check|Implement /health and /ready endpoints reflecting PostgreSQL + Redis + SendGrid reachability; wire to uptime monitor with 30-day rolling-window SLO.|AuthService|-|/health returns 200 if all deps reachable; /ready returns 200 only after warmup; uptime monitor polls every 30s; SLO dashboard shows 30-day rolling uptime; alert if <99.9% projected|M|P0|
|99|SEC-005|Security review|Formal security review covering token lifecycle, password storage, crypto config, CORS/TLS, rate limits, user enumeration.|Security|FR-AUTH-001,FR-AUTH-003,NFR-SEC-001,NFR-SEC-002|review meeting held; written report produced; all findings triaged; zero High/Critical unaddressed at M4 exit; report filed with sec-reviewer sign-off|L|P0|
|100|SEC-006|Penetration test|External pen-test against staging covering OWASP Top 10 + auth-specific attacks (credential stuffing, token replay, JWT algorithm confusion, timing attacks).|Security|SEC-005,MIG-002-prep|pen-test vendor engaged; attack scenarios published; test executed over 1 week on staging; report delivered; zero High/Critical unaddressed at M4 exit; retest cycle completed|XL|P0|
|101|SEC-AUDIT-TOKEN|Token security audit|Explicit audit of JWT claims, refresh-token rotation correctness, revocation effectiveness.|Security|SEC-005,COMP-006|alg=RS256 (no none, no HS256 accepted); payload claims iss/aud validated on verify; rotation deletes old token atomically; revocation across sibling tabs verified; audit filed with pen-test report|M|P0|
|102|SEC-CSP|Content Security Policy|Configure strict CSP headers for frontend to mitigate XSS vector for accessToken.|APIGateway|COMP-004|CSP header set: default-src 'self'; script-src 'self' <analytics-domain>; frame-ancestors 'none'; report-uri configured; no inline scripts in `AuthProvider`/`LoginPage`/`RegisterPage`|S|P0|
|103|RELIABILITY-READINESS|Chaos/failure testing|Inject Redis-outage, PostgreSQL-outage, SendGrid-outage in staging; verify graceful degradation per TDD §12 / §25.1.|Reliability|NFR-REL-001|Redis-down → /auth/refresh fails cleanly with 503 AUTH_REFRESH_UNAVAILABLE (not generic 500); PostgreSQL-down → all writes fail with 503; SendGrid-down → reset-request still returns 200, DLQ grows; alerts fire; runbook steps resolve|M|P0|
|104|OPS-007|Observability dashboards live|Aggregate OBS-001..009 into Grafana dashboards: auth-overview, auth-perf, auth-errors, audit-volume.|Logging|OBS-001 through OBS-009|4 dashboards published; SRE-reviewed; drill-down links from alerts to dashboards; exported to repo for version control|M|P0|
|105|OPS-008-prep|Alert tuning + on-call dry-run|Tune alert thresholds against week-2 Phase-2-prep baseline; run on-call dry-run with auth-team.|Logging|OBS-007,OBS-008,OBS-009,OPS-007|false-positive rate <10% in 48h shadow; on-call dry-run completes; acknowledgment SLA 15min demonstrated; runbook link present in every alert|S|P0|
|106|COVERAGE-GATE|Unit-test coverage ≥80%|Verify and gate CI on unit coverage ≥80% for `AuthService`, `TokenManager`, `JwtService`, `PasswordHasher`, `UserRepo`.|Tests|TEST-001,TEST-002,TEST-003,TEST-004,TEST-005,TEST-006|CI computes per-package coverage; thresholds enforced (80% lines, 80% branches); coverage report published per PR; gap report generated; coverage badge in README|S|P0|
|107|LOAD-TEST-FULL|Full load test 500 concurrent mixed|k6 mixed-workload scenario (60% login, 15% register, 15% refresh, 10% /me) at 500 concurrent for 30 min.|Tests|NFR-PERF-002|scenario runs 30min; p95 <200ms sustained; error rate <0.1%; PostgreSQL wait <50ms; Redis latency <10ms; HPA scaling observed; results archived|L|P0|
|108|DATA-MIG-SCRIPT|UserProfile data migration script|Script for optional migration of legacy user records (if any) into `UserProfile`: idempotent upsert, password-rehash-on-next-login hook.|UserRepo|COMP-009,DM-001|script processes CSV/legacy source idempotently; new logins on migrated accounts trigger bcrypt rehash from legacy hash; dry-run mode; full rollback via DB restore|M|P1|

### Integration Points — M4

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|Audit-log writer hook|Event binding|AUDIT-002|M4|Every auth event (login, register, refresh, reset, lockout, logout); AUDIT-001 table|
|Log-redaction middleware (final)|Middleware chain|NFR-SEC-003,OBS-001|M4|All logs emitted by `AuthService`/`TokenManager`/`JwtService`|
|Metric registration registry|Dispatch table|OBS-002..005|M4|Prometheus scrape endpoint|
|OTEL span context propagator|Middleware chain|OBS-006|M4|All outbound calls to PostgreSQL/Redis/SendGrid|
|Alert-rule registry|Dispatch table|OBS-007,OBS-008,OBS-009,OBS-ROLLBACK-TRIGGERS|M4|Prometheus + PagerDuty|
|Rollback-trigger automation|Strategy pattern + callbacks|OBS-ROLLBACK-TRIGGERS|M4|Feature-flag toggler; distinct from degradation alerts|
|Consent-version registry|Strategy pattern|NFR-COMP-001|M4|Consent workflow; extensible for v1.1 withdrawal|

### Milestone Dependencies — M4

- M3 endpoints functional; auth events already emitted by `AuthService` (SEC-LOGGING-M2); M4 adds durable sink.
- OQ-CONFLICT-1 resolved; PostgreSQL partition sized per OQ-OBS-CAPACITY.
- External: pen-test vendor SOW signed; compliance officer availability for NFR-COMP-001/002 sign-off.

### Open Questions — M4

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-CONSENT-WITHDRAWAL|GDPR consent withdrawal flow — where does it live (admin-mediated vs self-service) and what is its effect on AuthTokens? Resolution proposal: deferred to v1.1 full DSAR; v1.0 provides consent record only. Status: tentative|Incomplete GDPR flow; acceptable at v1.0 per compliance officer review if consent capture + audit trail present.|compliance + product|2026-05-22|
|2|OQ-DSAR-EXPORT|DSAR data-export format (JSON vs PDF)? v1.0 emits JSON stub; full DSAR in v1.1.|Affects consent-workflow deliverable scope; stub sufficient for SOC2.|compliance|2026-05-22|
|3|OQ-PEN-TEST-WINDOW|Pen-test vendor scheduling — can we secure a 1-week window ending 2026-05-27 to meet M4 exit? If slips, delays M5 rollout.|Could push M5 by 3-5 days; requires assessment against 2026-06-09 GA.|sec-reviewer + procurement|2026-05-04|

### Risk Assessment and Mitigation — M4

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Pen-test finds High/Critical requiring M5 delay (R-PRD-002)|Critical|Low|GA slips past 2026-06-09|Early scoping with vendor; staging hardening complete before pen-test begins; mitigation budget reserved in M5 buffer|sec-reviewer|
|2|Compliance sign-off delayed past M4 exit (R-PRD-003)|High|Medium|SOC2 audit fails in Q3|Compliance officer engaged weekly from M1; consent schema reviewed in M2 stub; NFR-COMP-002 evidence prepared|compliance|
|3|Audit-log write latency >100ms p95 degrades auth flow|Medium|Medium|NFR-PERF-001 missed|Async fire-and-forget pattern + buffered writer; partition strategy reduces insert lock contention|platform-team|
|4|Alert noise causes on-call fatigue|Medium|Medium|Real issues missed|OPS-008-prep tuning dry-run; false-positive rate gate <10%; de-dup rules for correlated alerts|platform-team|
|5|Rollback triggers misfire during legitimate traffic spike|Medium|Low|Unnecessary flag flips; user-visible regression|Thresholds tuned against load-test baseline; manual override documented; triggers require sustained 5-min breach|platform-team|

## M5: Production Readiness & GA

**Objective:** Execute Phase 2 (10% beta) → Phase 3 (100% GA), retire `AUTH_NEW_LOGIN`, schedule `AUTH_TOKEN_REFRESH` removal, finalize runbooks, capacity plans, on-call rotation. | **Duration:** 2 weeks (Weeks 10-11, 2026-06-01 → 2026-06-12; TDD M5 GA commit 2026-06-09 falls within window) | **Entry:** M4 pen-test PASS; compliance sign-off; observability live; runbooks drafted. | **Exit:** `AUTH_NEW_LOGIN` removed; all traffic on new `AuthService`; 99.9% uptime over first 7 days; monitoring dashboards green; `AUTH_TOKEN_REFRESH` scheduled for removal at GA+2w; post-GA review scheduled.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|109|MIG-002|Phase 2 Beta rollout (10%)|Enable `AUTH_NEW_LOGIN` for 10% traffic cohort; monitor latency, error rates, Redis usage for 2 weeks.|Release|MIG-002-prep,OBS-007,OBS-008,OBS-009|cohort split active; p95 <200ms sustained; error rate <0.1%; zero Redis connection failures; rollback tested; 2-week observation complete; go/no-go review held|L|P0|
|110|MIG-003|Phase 3 GA rollout (100%)|Remove `AUTH_NEW_LOGIN` gating; route 100% traffic to new `AuthService`; deprecate legacy endpoints.|Release|MIG-002|flag removed from config; all /v1/auth/* traffic served by new service; legacy-auth routes return 410 Gone with deprecation notice; 7-day uptime ≥99.9% measured|L|P0|
|111|OPS-001|Runbook: AuthService down|Publish runbook for AuthService full-outage: symptoms, diagnosis steps, resolution, escalation.|Ops|OPS-007|runbook published; symptoms (5xx on /v1/auth/*, LoginPage/RegisterPage error state) documented; diagnosis steps (pod health, PostgreSQL connectivity, PasswordHasher/TokenManager init logs); resolution (restart pods, failover to replica, reject refresh if Redis down); escalation (auth-team on-call → 15min → platform-team)|M|P0|
|112|OPS-002|Runbook: token refresh failures|Publish runbook for TokenManager/Redis-related refresh failures.|Ops|OPS-007|runbook published; symptoms (user logouts, AuthProvider redirect loop, auth_token_refresh_total error spike); diagnosis (Redis connectivity from TokenManager, JwtService key availability, AUTH_TOKEN_REFRESH state); resolution (scale Redis, re-mount secrets, enable flag); escalation path|S|P0|
|113|OPS-003|On-call expectations + rotation|Establish auth-team 24/7 on-call rotation for first 2 weeks post-GA; document tooling, escalation, SLAs.|Ops|OPS-001,OPS-002|PagerDuty schedule published for 2-week intensive rotation; P1 ack SLA 15min; tooling access (K8s dashboards, Grafana, Redis CLI, PostgreSQL admin) provisioned for on-call; escalation path: auth on-call → test-lead → eng-manager → platform-team|M|P0|
|114|OPS-004|Capacity: AuthService pods|Capacity plan + HPA: 3 replicas baseline, scale to 10 on CPU>70%.|Ops|OPS-007|HPA manifest committed; min=3, max=10; CPU target 70%; verified by chaos scaling test; capacity plan doc references 500-concurrent target (NFR-PERF-002)|S|P0|
|115|OPS-005|Capacity: PostgreSQL|Capacity plan for PostgreSQL: 100 pool baseline, scale to 200 if wait >50ms; include audit-log partition sizing.|Ops|OPS-007,AUDIT-001|pool size=100 baseline; alert at wait>50ms; scaling procedure documented; audit-log partition storage 12-month estimate included (per OQ-OBS-CAPACITY); read-replica routing for audit queries|M|P0|
|116|OPS-006|Capacity: Redis memory|Capacity plan for Redis: 1GB baseline for ~100K refresh tokens; scale to 2GB at >70% util.|Ops|OPS-007|memory=1GB baseline; monitoring shows util %; scale playbook to 2GB documented; worst-case projection (500K tokens ≈ 250MB per OQ-PRD-2 analysis) headroom confirmed|S|P0|
|117|OPS-008|Alerts in production|Promote staging alerts (OBS-007/008/009 + OBS-ROLLBACK-TRIGGERS) to production; tune against first 24h baseline.|Ops|OBS-007,OBS-008,OBS-009,OPS-008-prep|alert rules deployed to prod; first-24h false-positive rate <10%; rollback-trigger dry-run in prod-shadow mode; on-call receives test page|S|P0|
|118|FLAG-REMOVAL|Feature flag cleanup|Schedule `AUTH_NEW_LOGIN` removal immediately post-GA; `AUTH_TOKEN_REFRESH` at GA+2w per TDD §19.2.|Release|MIG-003|`AUTH_NEW_LOGIN` PR merged removing flag and all gating checks; `AUTH_TOKEN_REFRESH` removal PR drafted with GA+2w merge date; TDD §19.2 updated with actual removal dates|S|P0|
|119|RELEASE-CHECKLIST|Final release checklist|Execute TDD §24.2 release checklist; capture sign-offs from test-lead + eng-manager.|Release|ALL M1..M4|all TDD §24.2 items ticked (staging deploy smoke, LoginPage/RegisterPage functional, AuthProvider refresh verified with 15-min token, flags configured, runbooks published, dashboards verified, rollback tested, migration script validated); go/no-go sign-off recorded|M|P0|
|120|POST-GA-REVIEW|Post-GA review + metric audit|Week after GA: review PRD success metrics, flag gaps, schedule follow-on work.|Release|MIG-003|review held 2026-06-16 (GA+7d); metrics audited: registration conversion (target >60%), login p95 (<200ms), avg session duration (>30min), failed login rate (<5%), password reset completion (>80%); follow-on backlog items created for any miss|S|P1|
|121|LEGACY-DEPRECATION|Legacy auth endpoint deprecation|Return 410 Gone with Sunset header on legacy auth endpoints; publish migration notice.|APIGateway|MIG-003|legacy /auth/* routes return 410 with Sunset: 2026-07-01; deprecation notice posted to internal engineering channel; external-API consumer email sent|S|P1|
|122|V1.1-BACKLOG|V1.1 deferred-scope backlog|Capture OQ-001 (API-key auth), OQ-JTBD-4 (service-accounts), OQ-REMEMBER-ME, OQ-CONSENT-WITHDRAWAL, OQ-DSAR-EXPORT, MFA (NG-002), RBAC (NG-003), OAuth (NG-001) as v1.1 tickets.|Meta|ALL OQs|8 v1.1 tickets created with links back to originating OQ/NG IDs; prioritization review scheduled|S|P1|

### Integration Points — M5

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|Traffic-split controller|Dispatch table|MIG-002|M5|`AUTH_NEW_LOGIN` percentage rollout|
|Deprecation middleware|Middleware chain|LEGACY-DEPRECATION|M5|Legacy /auth/* routes; extensible for future deprecations|
|On-call schedule|Dispatch table|OPS-003|M5|PagerDuty; Grafana annotation; alert routing|
|HPA controller|Strategy pattern|OPS-004|M5|`AuthService` pod scaling|
|Flag-removal automation|Callback registry|FLAG-REMOVAL|M5|CI/CD post-GA scheduled jobs|

### Milestone Dependencies — M5

- M4 compliance + security sign-offs captured.
- M3 `AUTH_TOKEN_REFRESH` enablement validated at 10% in MIG-002.
- External: PagerDuty seat allocation for auth-team; legacy-API consumer list from product.

### Risk Assessment and Mitigation — M5

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Phase 2 beta latency regression under 10% real traffic|High|Medium|Rollback + M5 overrun past 2026-06-09 GA|Staged ramp 1%→5%→10% over week 1; automated rollback triggers wired (OBS-ROLLBACK-TRIGGERS); mitigation buffer=3 days in M5 schedule|platform-team|
|2|Migration from legacy auth causes data loss (R-003)|Low|High|User accounts corrupted|Parallel run Phase 1-2; idempotent upsert in DATA-MIG-SCRIPT; full DB backup pre-rollout; rollback restores from backup|platform-team|
|3|On-call rotation undermanned in post-GA 2-week intensive window|Medium|Medium|P1 SLA breach; incident response degraded|Rotation confirmed week -1 of M5; backup on-call identified; tooling access pre-provisioned|eng-manager|
|4|Compliance audit retrospective finds gap|Medium|Low|Remediation post-GA; SOC2 risk|Compliance sign-off obtained in M4; audit-log sample reviewed; remediation backlog empty at M5 entry|compliance|

## Resource Requirements and Dependencies

### External Dependencies

|Dependency|Version|Purpose|Criticality|Milestone Introduced|Notes|
|---|---|---|---|---|---|
|PostgreSQL|15+|UserProfile + audit_log storage|Blocker|M1 (DEP-001)|Provisioned via DEP-002; testcontainers pin for CI|
|Redis|7+|Refresh-token store with TTL|Blocker|M1 (DEP-003)|EXPIRE-based TTL; AOF persistence for durability|
|Node.js|20 LTS|Runtime for backend services|Blocker|M1 (DEP-004)|Pinned in Dockerfile + CI image|
|bcryptjs|^2.4.3|Password hashing (cost=12)|Blocker|M1 (DEP-005)|Wrapped by `PasswordHasher` (COMP-005)|
|jsonwebtoken|^9.0.0|JWT sign/verify (RS256)|Blocker|M1 (DEP-006)|Wrapped by `JwtService` (COMP-007b)|
|SendGrid|2024 API|Transactional email (reset, verify)|Enhancement|M3 (DEP-007)|Retry/backoff via ASYNC-QUEUE; template-abstracted (DECOMP-EMAIL-TEMPLATE)|
|React Router|^6|Frontend routing for auth pages|Enhancement|M3 (INFRA-003)|AuthProvider consumed by LoginPage/RegisterPage/ProfilePage|
|Prometheus|2.x|Metrics scrape target|Enhancement|M4 (OBS-001)|`/metrics` endpoint on AuthService|
|OpenTelemetry Collector|0.x|Trace aggregation|Enhancement|M4 (OBS-002)|OTLP → Jaeger backend|
|PagerDuty|SaaS|Alert routing + on-call|Enhancement|M4/M5 (OBS-007, OPS-003)|auth-team escalation policy|

### Infrastructure Requirements

- **Staging environment**: 2× backend pods, 1× PostgreSQL primary + 1× replica, 1× Redis; dedicated for M3-M4 integration/load testing (ref: DEP-002, INFRA-001).
- **Production environment**: 4× backend pods (HPA target CPU 60%), PostgreSQL primary + standby + PITR backups, Redis Sentinel (3-node), CloudFront/ALB in front of Express app (ref: OPS-004, DEP-002).
- **Observability stack**: Prometheus (15-day retention), Grafana (dashboards for auth KPIs), Jaeger (7-day trace retention), centralised logging with 12-month audit-log retention per OQ-CONFLICT-1 resolution (ref: OBS-001..008, AUDIT-001).
- **Secret management**: RSA signing keys and bcrypt pepper stored in KMS/Vault; rotation runbook in RSA-KEY-ROTATION (M3); SOC2 key-rotation control owned by security-team.
- **CI/CD**: GitHub Actions runners with coverage gate ≥85% (COVERAGE-GATE, M4), testcontainers permissions (privileged runners for Docker-in-Docker), k6 load runners (NFR-PERF-001-M3, LOAD-TEST-FULL).
- **Headcount**: 3 backend engineers, 2 frontend engineers, 1 SRE, 0.5 security-team, 0.25 compliance reviewer, 0.25 tech-writer across 11-week duration (ref: Effort totals per milestone).

## Risk Register

|ID|Risk|Affected Milestones|Category|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|---|---|
|R-001|Load-test tooling not yet procured before M3 NFR-PERF-001-M3 deadline|M1, M3|Operational|High|Medium|Latency budgets unvalidated pre-M4 → LOAD-TEST-FULL slips|Pre-M1 procurement ticket filed in M1; k6-cluster provisioned in DEP-002; fallback: artillery (open-source) pre-validated in M1 spike|sre-team|
|R-002|SSO requirement (Q-6) surfaces during M3-M4 blocking scope lock|M1, M3|Scope|High|Low|Re-plan to add OIDC provider; GA slip 2-4 weeks|ADR-SSO-DEFERRAL documented in M1; product confirms no SSO for v1 by M1 exit; V1.1-BACKLOG (NG-001) captures deferral|product-eng|
|R-003|Migration from legacy auth causes user-account data loss|M3, M5|Technical|High|Medium|Users locked out; revenue loss ≥$100K/day|DATA-MIG-SCRIPT dry-run in staging (M4); idempotent upsert; full DB backup pre-rollout; MIG-002 phased 10%→50%→100%; rollback restores from backup|platform-team|
|R-004|Compliance audit discovers 12-month retention implementation gap|M1, M4, M5|Compliance|High|Low|SOC2 certification delayed; remediation post-GA|OQ-CONFLICT-1 closed 12 months in M1; NFR-COMP-002 validates retention in M4; AUDIT-001 schema enforces non-deletable rows; compliance sign-off gate at M4 exit|compliance|
|R-005|Bcrypt cost=12 latency budget breach under peak load|M2, M4|Performance|Medium|Medium|p95 login > 200ms SLA; WAL for NFR-PERF-001|PERF-BASELINE in M2 measures bcrypt cost; calibration check at M3 load test; cost reduction to 11 is reversible contingency with compliance review|backend-team|
|R-006|RSA key-rotation runbook untested when first rotation due|M3, M5|Operational|Medium|Medium|Key-rotation incident causes unplanned downtime|RSA-KEY-ROTATION drill in M3 on staging; JWKS endpoint supports multi-key verify; runbook reviewed by security-team|security-team|
|R-007|SendGrid outage blocks password-reset flow|M3|External|Medium|Medium|Reset emails delayed > SLA; CS tickets surge|ASYNC-QUEUE with retry/backoff (M3); secondary ESP evaluated for V1.1 (not in scope); runbook OPS-006 documents manual-send fallback|platform-team|
|R-008|CAPTCHA provider integration delays M3 login flow|M3|External|Medium|Medium|M3 scope slip; M4 hardening compresses|CAPTCHA-INTEG spike in M3 week 1; feature-flagged so login can ship without CAPTCHA to staging; go/no-go at M3 mid-point|backend-team|
|R-009|Observability capacity planning under-provisioned (OQ-OBS-CAPACITY)|M1, M4|Operational|Medium|Medium|Metrics scrape failures; blind-spot incidents|OQ-OBS-CAPACITY resolved in M1 with SRE input; OBS-001..008 include capacity sizing; monitoring of monitoring in OBS-009|sre-team|
|R-010|Frontend clock skew causes premature token expiry|M3|Technical|Low|High|Users auto-logged-out mid-session; support tickets|FE-CLOCK-SKEW (M3) implements ±30s tolerance and NTP sync detection; E2E covers clock-drift simulation in TEST-E2E-RESET|frontend-team|
|R-011|Legacy `/auth/*` consumer not deprecated by 2026-09-09 cutoff|M5|Organizational|Medium|Medium|Legacy maintenance burden; compliance scope creep|LEGACY-DEPRECATION ships deprecation headers + consumer list in M5; POST-GA-REVIEW tracks weekly migration; escalation to eng-leadership if < 50% migrated by GA+8 weeks|eng-manager|
|R-012|Pen-test window (OQ-PEN-TEST-WINDOW) not confirmed before M4|M4|Compliance|Medium|Low|SOC2 evidence gap; M4 exit gate blocked|OQ-PEN-TEST-WINDOW escalated at M3 mid-point; budget pre-approved; vendor shortlist captured in M1 |security-team|
|R-013|Coverage gate (≥85%) blocks M4 exit due to integration-test flakiness|M4|Quality|Medium|Medium|M4 slip 3-5 days|COVERAGE-GATE introduced in M4 with 1-week burn-in; flaky-test quarantine process; deterministic test-data factories in M2-M3|qa-team|
|R-014|DSAR export (OQ-DSAR-EXPORT) rules unresolved at M4 exit|M4|Compliance|Low|Medium|Post-GA remediation for GDPR DSAR|OQ-DSAR-EXPORT targeted to close in M4; default answer: export JSON bundle per UserProfile + audit_log subset; compliance sign-off|compliance|
|R-015|Consent-withdrawal propagation (OQ-CONSENT-WITHDRAWAL) design gap|M4|Compliance|Low|Medium|GDPR right-to-withdraw partially implemented|OQ-CONSENT-WITHDRAWAL closed in M4 with propagation-within-24h SLA; implementation in V1.1 if complexity > 5d|compliance|
|R-016|Post-GA on-call rotation undermanned (2-week intensive window)|M5|Operational|Medium|Medium|P1 SLA breach; incident response degraded|Rotation confirmed week -1 of M5; backup on-call identified; tooling access pre-provisioned; OPS-007 runbook library|eng-manager|
|R-017|Admin audit query (ADMIN-001) exposes PII beyond compliance scope|M3|Security|Medium|Low|Data-leak audit finding|ADMIN-001 restricted to compliance-team RBAC role; field-level redaction on ip_addr, user_agent when out of retention window; audit-of-audit-access logged|security-team|
|R-018|Rate-limit thresholds (login 10/min) too aggressive for legit bursty users|M2, M4|Product|Low|Medium|User friction; CS tickets|Thresholds set per TDD NFR-SEC-003; monitored via OBS-003; adjustment runbook; A/B test planned for V1.1|product-eng|
|R-019|OQ-OQ-002 concurrent-session cap (16) insufficient for power users|M3|Product|Low|Medium|Power-user complaints; support tickets|OQ-OQ-002 tentative cap=16 confirmed in M3; telemetry captures session count distribution for V1.1 calibration|product-eng|
|R-020|Feature flag (AUTH_NEW_LOGIN) removal (M5) leaves dead code paths|M5|Technical|Low|Low|Tech-debt accumulation|FLAG-REMOVAL automates removal via codemod script; tracked in post-GA review; CI check for stale flags|backend-team|

## Success Criteria and Validation Approach

|#|Success Criterion|Source|Metric|Target|Validation Method|Milestone Landing Slot|
|---|---|---|---|---|---|---|
|1|Registration completion rate|PRD goal|Registration start → completion %|≥ 75%|Funnel analytics dashboard; A/B vs legacy|M5 (POST-GA-REVIEW)|
|2|Login success rate (valid creds)|PRD goal|Successful logins / total login attempts with valid creds|≥ 99.5%|OBS-003 metric; NFR-REL-001 SLA|M4 (NFR-REL-001) → M5 telemetry|
|3|Password-reset completion rate|PRD goal|Reset request → successful password change %|≥ 85%|Funnel analytics + SendGrid delivery metric|M5 (POST-GA-REVIEW)|
|4|Authentication latency p95|TDD NFR-PERF-001|p95 `/auth/login` + `/auth/refresh` response time|< 200ms|k6 load test (NFR-PERF-001-M3) + Prom histogram (OBS-003)|M3 (NFR-PERF-001-M3), re-validated M4|
|5|Throughput capacity|TDD NFR-PERF-002|Sustained req/s on `/auth/*`|≥ 1000 RPS|Load test in LOAD-TEST-FULL (M4); Horizontal scaling verified in OPS-004|M4 (LOAD-TEST-FULL)|
|6|Service availability|TDD NFR-REL-001|Monthly uptime of auth endpoints|≥ 99.9%|SLI/SLO dashboard; error budget tracking|M5 (post-GA telemetry) — design validated M4|
|7|Zero PII leakage in logs|TDD NFR-SEC-001|# of PII matches in log grep audit|0|SEC-LOGGING-M2 automated scanner; SEC-AUDIT-TOKEN review|M2 (SEC-LOGGING-M2), re-audited M4|
|8|OWASP Top 10 compliance|TDD NFR-SEC-002|# of High/Critical findings in pen-test + SAST|0|SAST in CI (M1 INFRA-002); pen-test window (M4 OQ-PEN-TEST-WINDOW)|M4 (SEC-005) |
|9|Brute-force resistance|TDD NFR-SEC-003|Rate-limit trigger on 11th login attempt/min|100% blocked|SEC-003 unit tests + SEC-006 burn-in test|M2 (SEC-003), hardened M4 (SEC-006)|
|10|GDPR compliance — consent capture|TDD NFR-COMP-001|Consent flag stored for every registration|100%|DB constraint NOT NULL on consent column (M1 DM-002); NFR-COMP-001-stub M2; NFR-COMP-001 M4|M4 (NFR-COMP-001)|
|11|SOC2 audit-log completeness|TDD NFR-COMP-002|% of auth events persisted to audit_log|100% (sample audit)|AUDIT-003 replay test; compliance sample review|M4 (NFR-COMP-002)|
|12|Audit-log retention enforcement|PRD requirement (OQ-CONFLICT-1 closed 12 months)|Retention policy job executes; rows beyond 12 months archived|100% execution ≥ monthly|OPS-005 retention job; NFR-COMP-002 includes retention assertion|M4 (NFR-COMP-002), run M5 (OPS-005)|
|13|NIST SP 800-63B password conformance|TDD NFR-COMP-003|Password acceptance matches NIST ruleset|100% (ruleset test suite)|NFR-COMP-003 test vector; TEST-WEAK-PWD|M2 (NFR-COMP-003)|
|14|JWT expiry enforcement|TDD spec|Access token rejected > 15min; refresh > 7d|100%|TOKEN-STUB unit tests (M2); TEST-REVOKE integration (M3)|M2 (TOKEN-STUB), validated M3|
|15|Rate-limit enforcement — all endpoints|TDD NFR-SEC-003|Thresholds configured per endpoint and verifiable|100% endpoints covered|SEC-003 config tests + OBS-003 dashboards|M2 (SEC-003), observability M4|
|16|Feature flag rollback works|TDD rollout strategy|Time-to-disable from alarm to zero traffic|< 2 min|OBS-ROLLBACK-TRIGGERS drill in M4; MIG-002 phased rollout|M4 (OBS-ROLLBACK-TRIGGERS) → M5 (MIG-002)|
|17|GA entry gate passed|TDD milestone M4|Load + security + compliance sign-offs collected|3/3 sign-offs|RELIABILITY-READINESS review (M4) + RELEASE-CHECKLIST (M5)|M4 (RELIABILITY-READINESS), formalised M5 (RELEASE-CHECKLIST)|

## Decision Summary

### ADR-001 — JWT (RS256) over server-side sessions

- **Decision**: Use JWT RS256 2048-bit RSA key pair for access tokens; Redis-backed refresh tokens for revocation.
- **Rationale**: TDD requires horizontal scalability (NFR-PERF-002 ≥1000 RPS) — stateless auth avoids session affinity. Public-key verification permits downstream services to validate without shared secret. RS256 (asymmetric) preferred over HS256 to avoid key distribution risk.
- **Alternatives considered**: Server-side session cookies (rejected: sticky-session requirement hampers HPA scaling in OPS-004); Paseto (rejected: limited tooling in Node.js ecosystem 2026-04).
- **Trade-off**: Revocation is non-trivial — mitigated via short-lived access token (15 min) + Redis refresh-token store (COMP-007a, SEC-001 revocation endpoint).
- **Landing**: M1 (RBAC-DECISION + COMP-007b skeleton) → M2 (TOKEN-STUB) → M3 (SEC-001 revocation).

### ADR-002 — bcrypt cost factor 12

- **Decision**: bcrypt cost=12 for password hashing.
- **Rationale**: NIST SP 800-63B hash-strength guidance; measured ≈250ms/hash on production hardware (spike in M2 PERF-BASELINE). Balances brute-force resistance against login-latency budget (NFR-PERF-001 p95 < 200ms on login endpoint excluding password check if pre-auth fast-path; inside budget with 1 bcrypt eval + network).
- **Alternatives considered**: Argon2id (rejected: additional dep vetting, inconsistent ecosystem support in our Node.js 20 runtime at 2026-04); bcrypt cost=10 (rejected: insufficient margin for GPU attack by 2028 horizon); cost=14 (rejected: latency budget breach in PERF-BASELINE).
- **Trade-off**: R-005 latency risk; contingency to lower to cost=11 documented in NFR-PERF-001-M3 review.
- **Landing**: M1 (COMP-005 skeleton) → M2 (COMP-005 full) → M2 (PERF-BASELINE validates).

### ADR-003 — PostgreSQL + Redis dual-store persistence

- **Decision**: PostgreSQL for durable state (UserProfile, audit_log); Redis for ephemeral/high-churn state (refresh tokens, rate-limit counters, password-reset codes).
- **Rationale**: Audit log requires durable, queryable, retained-12-months storage (NFR-COMP-002) — RDBMS fit. Refresh tokens have high write-throughput + TTL-based expiry — Redis fit. Colocating both in Postgres rejected due to I/O pressure projected at 1000 RPS (DEP-002 capacity planning).
- **Alternatives considered**: Single Postgres with partitioned tokens table (rejected: TTL enforcement via cron is race-prone); DynamoDB (rejected: multi-cloud scope outside v1).
- **Trade-off**: Dual-store consistency — mitigated by keeping refresh-token revocation as single-source-of-truth in Redis; Postgres only references token IDs.
- **Landing**: M1 (DM-001, DEP-001, DEP-003) → M3 (SEC-001 revocation wires both stores).

### ADR-004 — Technical-layer milestone phasing (not vertical slices)

- **Decision**: Milestones map to technical layers (Foundation → Core Logic → Integration → Hardening → Production Readiness) rather than per-feature vertical slices.
- **Rationale**: TDD complexity_class=HIGH with cross-cutting NFRs (security, compliance, observability) benefits from horizontal consolidation — e.g., OBS-001..009 in M4 lands one observability stack rather than fragmenting across each feature. TDD milestone structure (M1-M4) already maps to this layering.
- **Alternatives considered**: Feature-vertical slices (rejected: would duplicate observability/audit infrastructure across M2-M4; 20% effort overhead per audit); agile epic-per-feature (rejected: incompatible with GA commit 2026-06-09 and phased rollout).
- **Trade-off**: Later visibility on end-to-end feature completion; mitigated by feature-flag-gated enablement (AUTH_NEW_LOGIN, AUTH_TOKEN_REFRESH) keeping features dark until milestone exit.
- **Landing**: structural — governs M1-M5 definitions.

### ADR-005 — Phased rollout with feature flags

- **Decision**: Roll out via `AUTH_NEW_LOGIN` + `AUTH_TOKEN_REFRESH` flags; ramp 10% → 50% → 100% in MIG-002 (M5).
- **Rationale**: Minimises blast radius of R-001 (load regression) and R-003 (migration data loss); supports < 2min rollback (Success Criterion 16) via OBS-ROLLBACK-TRIGGERS.
- **Alternatives considered**: Big-bang cutover (rejected: no rollback path without downtime); blue/green deploy (deferred: infrastructure cost for 100% duplicate stack not justified for v1).
- **Trade-off**: Flag complexity; mitigated via FLAG-REMOVAL automation in M5 post-GA.
- **Landing**: M1 (RBAC-DECISION + feature-flag infra in INFRA-002) → M3 (FE flag gating) → M5 (MIG-002, FLAG-REMOVAL).

### ADR-006 — Audit-log retention: 12 months (OQ-CONFLICT-1 resolution)

- **Decision**: 12-month retention for audit_log per PRD NFR-COMP-002; overrides TDD's 90-day draft.
- **Rationale**: SOC2 Type II evidence windows typically require 12 months of auth activity; PRD carries compliance precedence. Storage cost projection (DM-001 capacity planning) within budget at projected user growth.
- **Alternatives considered**: 90 days (TDD draft; rejected due to compliance conflict); 7 years (rejected: over-retention; PII residency risk).
- **Trade-off**: Storage cost; mitigated by AUDIT-001 column compression and archival tier after 6 months.
- **Landing**: M1 (OQ-CONFLICT-1 closed) → M4 (AUDIT-001, NFR-COMP-002) → M5 (OPS-005 retention job).

## Timeline Estimates

|Milestone|Focus|Effort (pd)|Start|End|TDD Milestone Mapping|Exit Gate|
|---|---|---|---|---|---|---|
|M1 Foundation|Data model, dependencies, observability capacity plan, OQ resolution|18|2026-03-30|2026-04-10|TDD M1 (Project Setup, by 2026-04-14)|DM schemas migrated to staging; 3/4 M1 OQs closed; infra procurement confirmed|
|M2 Core Logic|Register/login flows, password hashing, JWT stub, rate limiting|22|2026-04-13|2026-04-24|TDD M1–M2 (Core Auth, by 2026-04-28)|Register + login green on staging; PERF-BASELINE report; zero PII in logs|
|M3 Integration|Session refresh/logout, password reset, frontend wiring, CAPTCHA, load-baseline|27|2026-04-27|2026-05-15|TDD M2–M3 (Password Reset, by 2026-05-12)|All FRs green E2E; NFR-PERF-001 p95 < 200ms on staging; rate-limit + CAPTCHA verified|
|M4 Hardening|Observability, audit pipeline, compliance validation, pen-test, full load|21|2026-05-18|2026-05-29|TDD M4 (Security & Compliance, by 2026-05-26)|SOC2 audit sample pass; LOAD-TEST-FULL 1000 RPS pass; pen-test High/Critical = 0|
|M5 Production Readiness|Phased rollout, ops runbooks, GA, legacy deprecation|11|2026-06-01|2026-06-12|TDD M5 (Production Deployment, by 2026-06-09)|10%→100% ramp complete; on-call rotation staffed; post-GA review scheduled|

### Timeline Notes

- **GA target**: 2026-06-09 (per TDD milestone commitment). M5 end extends to 2026-06-12 to absorb phased-rollout ramp buffer (R-001 mitigation).
- **Total effort**: 99 person-days across 11 calendar weeks, consistent with Team Size: 3 backend + 2 frontend + 1 SRE + partial security/compliance/tech-writer allocation.
- **Schedule compression**: Milestones overlap at boundary days (M1→M2 kickoff 2026-04-13 while M1 sign-off tails 2026-04-10; M3→M4 kickoff 2026-05-18 while M3 stabilisation tails). No-overlap on M4→M5 boundary (compliance gate must close before rollout).
- **Buffer**: 3 days M5 buffer for rollout abort/resume; no global slack. Any slip > 3 days on M3 critical path (FR-AUTH-003 refresh) escalates to replanning GA date.
- **Dependencies on external teams**: pen-test window (M4, R-012 open), CAPTCHA vendor access (M3, R-008), PagerDuty seat provisioning (M4-M5), SendGrid production quota (M3).
- **Week-by-week**: W1-W2 M1, W3-W4 M2, W5-W7 M3, W8-W9 M4, W10-W11 M5.



