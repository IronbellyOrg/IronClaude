---
spec_source: "test-tdd-user-auth.compressed.md"
complexity_score: 0.78
complexity_class: HIGH
primary_persona: architect
adversarial: true
base_variant: "A"
variant_scores: "A:86 B:81"
convergence_score: 0.68
---
<!-- CONV: AuthService=THS, TokenManager=TKN, compliance=CMP, PasswordHasher=PSS, PostgreSQL=PST, JwtService=JWT, UserProfile=SRP, retention=RTN, Integration=NTG, AUTH_NEW_LOGIN=ANL, platform-team=PT, AuthProvider=THP, AUTH_TOKEN_REFRESH=ATR, implementation=MPL, password=PA1, register=RGS, documented=DCM, UserRepo=SRR, AUDIT-001=A0, rejected=RJC, AdminAuthEventService=AES, AccountLockManager=ALM, OBS-ROLLBACK-TRIGGERS=ORT, registration=RE1, endpoints=NDP, resolution=RSL, integration=IN1, Implement=IM1, rollback=RLL, endpoint=EN1, Resolution=RE2, PasswordResetToken=PA2, COMP-006=C0, Compliance=CO1, verified=VRF, rotation=RTT, oldest-eviction=OE, published=PBL, NFR-COMP-002=NC0, FR-AUTH-001=FA0, RegisterPage=RE3, FR-AUTH-003=FRT -->

# User Authentication Service — Project Roadmap

## Executive Summary

Deliver a secure, stateless, JWT-based identity layer (`THS`) for the platform by 2026-06-09, implementing 5 functional and 9 non-functional requirements across backend, frontend, security, data, CMP, testing, and DevOps domains. The roadmap decomposes the TDD's 876-line specification into 5 technically-layered milestones (Foundation → Core Logic → NTG → Hardening → Production Readiness) covering 129 individually tracked deliverables. This plan is the product of an adversarial merge: Variant A (Opus, architect — 86) forms the operational scaffold; Variant B (Haiku, architect — 81) contributes Jordan-persona admin NDP, explicit data-model rows, CONFLICT-2 RSL, and API-deprecation governance (convergence_score 0.68).

**Business Impact:** Unblocks ~$2.4M in projected annual revenue from personalization-dependent features (Q2-Q3 2026), enables SOC2 Type II audit closure (Q3 2026 deadline), and addresses 30% QoQ growth in access-related support tickets. Persona coverage targets Alex (end user <60s RE1), Jordan (admin audit visibility + incident-response lock/unlock via API-009/010), and Sam (API consumer programmatic refresh).

**Complexity:** HIGH (0.78) — Security-critical domain with crypto primitives (bcrypt, RS256), five-component orchestration (`THS`→`TKN`→`JWT`→`PSS`→`SRR`), dual-store persistence (PST+Redis), external SMTP dependency, phased feature-flag rollout, and overlapping regulatory frameworks (SOC2, GDPR, NIST SP 800-63B).

**Critical path:** PST/Redis provisioning (M1) → `PSS` + `SRP` persistence (M2) → `THS.login`/`RGS` (M2) → `TKN` + `JWT` + `/auth/refresh` (M3) → Frontend `THP` wiring (M3) → Audit logging + observability + admin lock/unlock (M4) → Feature-flagged beta ramp (M5) → GA on 2026-06-09.

**Key architectural decisions:**

- Stateless JWT (RS256, 2048-bit RSA, 15-min access / 7-day refresh) over server-side sessions — enables horizontal `THS` scaling without sticky routing.
- bcrypt cost factor 12 via `PSS` abstraction — balances <500ms hash time against offline-crack resistance; interface allows future argon2id migration without API changes.
- Dual-store persistence: PST 15 for `SRP` + `AuthAuditLog` + `PA2` (durable), Redis 7 for hashed refresh tokens (revocable, TTL-enforced) — separation of identity-of-record from session artifacts.
- Feature-flagged phased rollout (`ANL`, `ATR`) with 10% beta gate and human-confirmed RLL triggers for first 30 days post-GA — bounds blast radius during migration.
- Audit log RTN set to 12 months (PRD NC0 / SOC2) overriding TDD §7.2's 90-day default — CMP precedence DCM in OQ-CONFLICT-1.
- Refresh-token cap=5 per user with OE policy (per OQ-PRD-2 RSL) — deterministic Redis sizing, reversible via feature flag if user friction observed.

**Open risks requiring RSL before M1:**

- OQ-CONFLICT-1 (audit RTN TDD 90d vs PRD 12mo) — must be resolved to size PST RTN partition and inform A0 schema.
- OQ-PRD-3 (account lockout policy) — TDD commits to 5 failures/15min; PRD still open; resolve to allow SEC-001 MPL.
- OBS storage budget for 12-month audit log at projected 1M logins/month must be confirmed with PT before M1 exit.

## Milestone Summary

|ID|Title|Type|Priority|Effort|Dependencies|Deliverables|Risk|
|---|---|---|---|---|---|---|---|
|M1|Foundation & Infrastructure|Foundation|P0|2w|PST/Redis/Node20/SendGrid provisioning|27|Medium|
|M2|Core Authentication Logic|Core Logic|P0|2w|M1|23|High|
|M3|NTG, Tokens & Frontend|NTG|P0|3w|M2|34|High|
|M4|Hardening, Observability & CO1|Hardening|P0|2w|M3|31|High|
|M5|Production Readiness & GA|Production|P0|2w|M4|14|Medium|

## Dependency Graph

```
M1 (Foundation)
 ├─> DM-001/DM-002/DM-003/DM-004 schemas ─> M2 (Core Logic) / M3 (reset) / M4 (audit)
 ├─> PostgreSQL provisioning ──> M2.UserRepo
 ├─> Redis provisioning ────────> M3.TokenManager
 ├─> bcryptjs / jsonwebtoken ──> M2.PasswordHasher / M3.JwtService
 ├─> SendGrid setup ────────────> M3.PasswordReset
 └─> AUTH_NEW_LOGIN flag ───────> M2→M3→M5 rollout

M2 (Core Logic: PasswordHasher + AuthService.login/register)
 ├─> FR-AUTH-001, FR-AUTH-002 ─> M3 (API-003/004/005/006)
 └─> UserRepo ───────────────────> M4 (AUDIT-001, AUDIT-002)

M3 (Integration: TokenManager + JwtService + Frontend + Reset)
 ├─> FR-AUTH-003/004/005 ──────> M4 (hardening, observability)
 ├─> COMP-001/002/003/004 ─────> M4 (CAPTCHA, E2E tests)
 └─> API-004 refresh ───────────> M5 (AUTH_TOKEN_REFRESH ramp)

M4 (Hardening: Observability + Compliance + Security + Audit + Admin)
 ├─> OBS-001..009 ──────────────> M5 (alerts in production)
 ├─> AUDIT-001/002 ─────────────> M5 (SOC2 compliance gate)
 ├─> COMP-018 AES + COMP-019 ALM > API-009/010 admin lock/unlock
 ├─> API-011 /health ──────────> M5 (NFR-REL-001 SLO monitoring)
 └─> Pen-test sign-off ─────────> M5 (GA release criteria)

M5 (Production: Phased rollout + runbooks + GA)
 └─> GA 2026-06-09
```

## M1: Foundation & Infrastructure

**Objective:** Provision shared infrastructure, define data contracts (including AuthAuditLog and PA2), scaffold service skeletons, RGS feature flags, and resolve blocking design decisions before any auth logic is written. | **Duration:** 2 weeks (Weeks 1-2, 2026-03-30 → 2026-04-10) | **Entry:** TDD AUTH-001-TDD approved; PRD AUTH-PRD-001 approved; SEC-POLICY-001 reviewed; CONFLICT-1 RSL accepted (12-month RTN chosen). | **Exit:** PST 15 + Redis 7 + Node.js 20 deployed in staging; `SRP`, `AuthToken`, `AuthAuditLog`, `PA2` schemas reviewed; `THS`/`TKN`/`JWT`/`PSS` package skeletons compile; `ANL` and `ATR` flags registered (default OFF); TLS 1.3 + CORS configured at API Gateway; CONFLICT-1 + OQ-PRD-3 resolutions DCM.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|DM-001|SRP entity schema|Define `SRP` PST DDL + TypeScript interface; emit migration script.|SRR|-|id:UUID-PK-NOT-NULL; email:varchar-UNIQUE-NOT-NULL-indexed-lowercase-normalized; displayName:varchar-NOT-NULL-2-100-chars; createdAt:timestamptz-NOT-NULL-DEFAULT-now(); updatedAt:timestamptz-NOT-NULL-auto-updated; lastLoginAt:timestamptz-NULLABLE; roles:text[]-NOT-NULL-DEFAULT-["user"]; password_hash:varchar-NOT-NULL; migration script applies cleanly to empty PST 15|M|P0|
|2|DM-002|AuthToken interface contract|Define `AuthToken` TypeScript interface returned by `THS` and `TKN`.|TKN|-|accessToken:string-JWT-NOT-NULL-RS256-signed-payload-contains-user-id-and-roles; refreshToken:string-NOT-NULL-unique-stored-hashed-in-Redis; expiresIn:number-NOT-NULL-always-900; tokenType:string-NOT-NULL-always-"Bearer"; type exported from shared package|S|P0|
|3|DM-003|AuthAuditLog schema|Define `AuthAuditLog` PST DDL + TypeScript interface; forward-referenced by A0 in M4 but schema frozen in M1 for sizing/budget.|SRR|-|id:UUID-PK-NOT-NULL; user_id:UUID-FK-nullable; event_type:varchar-NOT-NULL-enum(login_success,login_failure,register,refresh,reset_request,reset_confirm,lockout,unlock,logout); ip_address:inet; user_agent:varchar-255; outcome:varchar-NOT-NULL-enum(success,failure); metadata:jsonb; created_at:timestamptz-NOT-NULL-DEFAULT-now(); monthly partitioning contract DCM; 12-month RTN policy declared|M|P0|
|4|DM-004|PA2 schema|Define `PA2` PST DDL + TypeScript interface for reset-token persistence (single-use with 1h TTL).|SRR|-|id:UUID-PK-NOT-NULL; user_id:UUID-FK-NOT-NULL; token_hash:varchar-NOT-NULL-indexed-SHA256; expires_at:timestamptz-NOT-NULL; consumed_at:timestamptz-NULLABLE; created_at:timestamptz-NOT-NULL-DEFAULT-now(); unique constraint on token_hash; AC enforces single-use via UPDATE WHERE consumed_at IS NULL|S|P0|
|5|DEP-001|PST 15+ provisioning|Provision managed PST 15 with connection pool size 100, daily backup, read replica.|Infra|-|version=15+; pool=100; backup RTN 30 days; read replica RPO<5min; staging+prod tenants isolated; pg-pool client integrated|M|P0|
|6|DEP-002|Redis 7+ provisioning|Provision managed Redis 7 cluster with 1GB memory, AOF persistence for refresh-token durability.|Infra|-|version=7+; mem=1GB; AOF=on; SET key TTL=604800s (7d) VRF by smoke; staging+prod tenants isolated|M|P0|
|7|DEP-003|Node.js 20 LTS runtime|Establish Node.js 20 LTS base image and npm/pnpm dependency lockfile.|Infra|-|node=20.x LTS; lockfile committed; Docker base image PBL; build succeeds in CI|S|P0|
|8|DEP-004|bcryptjs library IN1|Add `bcryptjs` dependency wired through `PSS` interface.|PSS|DEP-003|bcryptjs=^2.x; cost-factor parameter wired to env var BCRYPT_COST (default 12); benchmark on target hardware <500ms|S|P0|
|9|DEP-005|jsonwebtoken library IN1|Add `jsonwebtoken` dependency wired through `JWT` interface; load RSA keys from secrets mount.|JWT|DEP-003|jsonwebtoken=^9.x; RS256 algorithm; 2048-bit RSA keys mounted from K8s secret; clock-skew tolerance=5s configured|S|P0|
|10|DEP-006|SendGrid SMTP/API IN1|Provision SendGrid API account, configure DKIM/SPF, integrate transactional template for PA1 reset.|EmailClient|-|API key in vault; DKIM/SPF VRF; reset-email template ID stored in config; sandbox send succeeds|M|P0|
|11|DEP-007|Frontend routing framework|Verify frontend routing framework supports `/login`, `/RGS`, `/profile` routes with auth guards.|Frontend|-|router supports protected routes; redirect-on-401 hook available; route table reviewed|S|P0|
|12|INFRA-001|API Gateway rate limiting|Configure per-IP/per-user rate limits at API Gateway: 10/min login, 5/min RGS, 60/min /me, 30/min refresh.|APIGateway|-|/auth/login=10rpm/IP; /auth/RGS=5rpm/IP; /auth/me=60rpm/user; /auth/refresh=30rpm/user; 429 returned with Retry-After header|M|P0|
|13|INFRA-002|TLS 1.3 enforcement|Enforce TLS 1.3 on all `/auth/*` NDP at load balancer; reject TLS<1.3.|APIGateway|-|TLS-1.3 only; HSTS max-age=31536000; ssllabs.com grade ≥A; older protocols return handshake failure|S|P0|
|14|INFRA-003|CORS allow-list configuration|Restrict CORS to known frontend origins; reject Origin headers outside allow-list.|APIGateway|-|allow-list = staging.platform.com, app.platform.com; preflight returns 403 for other origins; credentials=true wired for cookie refresh|S|P0|
|15|NFR-SEC-002|JWT signing config validation|`JWT` initialization validates RS256 algorithm and 2048-bit RSA key on boot; fails fast otherwise.|JWT|DEP-005|alg=RS256 asserted; key length=2048 asserted; service refuses to start if either invalid; configuration test in CI|S|P0|
|16|NFR-SEC-003|TLS 1.3 + log redaction baseline|Establish global log-redaction middleware that strips `PA1`, `accessToken`, `refreshToken`, `newPassword` fields before sink.|Logging|INFRA-002|redaction list configured; unit test asserts redacted fields never appear in serialized log lines; TLS 1.3 VRF end-to-end|S|P0|
|17|COMP-005-skel|THS skeleton|Create `THS` package with method signatures for `login`, `RGS`, `getProfile`, `resetRequest`, `resetConfirm`; throws NotImplemented.|THS|DM-001,DM-002|src/auth/auth-service exports class; 5 method signatures match TDD §10/§8; package compiles; placeholder unit tests pass|S|P0|
|18|C0-skel|TKN skeleton|Create `TKN` package with method signatures for `issueTokens`, `refresh`, `revoke`; throws NotImplemented.|TKN|DM-002|class exports 3 method signatures; injects `JWT` + Redis client via constructor; package compiles|S|P0|
|19|COMP-007a-skel|JWT skeleton|Create `JWT` package with `sign(payload)` and `verify(token)` signatures; loads keys at boot.|JWT|DEP-005,NFR-SEC-002|class exports sign/verify; key loader injected; package compiles; boot fails if key invalid|S|P0|
|20|COMP-007b-skel|PSS skeleton|Create `PSS` package wrapping bcryptjs with `hash(plain)` and `verify(plain, hash)` signatures.|PSS|DEP-004,DEP-006|class exports hash/verify; cost-factor injected via constructor; package compiles|S|P0|
|21|COMP-009|SRR skeleton|Create `SRR` package abstracting PST CRUD over `SRP`; methods: `findByEmail`, `findById`, `insert`, `updateLastLogin`, `updatePassword`.|SRR|DM-001,DEP-001|5 method signatures; uses pg-pool; transactions supported; package compiles|M|P0|
|22|MIG-004|Feature flag ANL|Register `ANL` feature flag in config service; default OFF; gating wired into `THS.login` entrypoint.|THS|-|flag registered; default=OFF; runtime toggle without redeploy; gating callable from request handler; removal target=Phase 3 GA|S|P0|
|23|MIG-005|Feature flag ATR|Register `ATR` feature flag in config service; default OFF; gating wired into `TKN.refresh`.|TKN|-|flag registered; default=OFF; toggle without redeploy; removal target=Phase 3 + 2 weeks|S|P0|
|24|MIG-001|Phase 1 Internal Alpha plan|Document Phase 1 deployment plan: staging deploy, auth-team + QA test all NDP behind `ANL`.|Release|MIG-004|plan PBL; participants identified; exit=all FA0..005 manual pass + zero P0/P1; duration=1 week|S|P1|
|25|API-VER-001|API URL versioning|Establish `/v1/auth/*` URL-prefix versioning convention with DCM breaking-change policy.|APIGateway|-|all auth NDP mounted under /v1; breaking-change-requires-major-bump DCM; deprecation header support added; deprecation policy doc PBL (resolves TDD §8.4 ambiguity); extended governance in OQ-GOV-001 (M4)|S|P1|
|26|ERR-ENV-001|Standard error envelope|Define and implement uniform error envelope `{ error: { code, message, status } }` across all auth NDP.|THS|-|envelope schema DCM; codes registered: AUTH_INVALID_CREDENTIALS, AUTH_TOKEN_EXPIRED, AUTH_TOKEN_REVOKED, AUTH_ACCOUNT_LOCKED, AUTH_DUPLICATE_EMAIL, AUTH_WEAK_PASSWORD, AUTH_RESET_TOKEN_INVALID; middleware enforces envelope on all 4xx/5xx|S|P0|
|27|RBAC-DECISION|SRP.roles default policy|Document interim policy: roles defaulted to ["user"], not enforced by `THS` (deferred to RBAC PRD).|SRR|DM-001|roles array constrained to default ["user"] in v1.0; enforcement deferred per TDD NG-003; DCM in TDD §3.2 update|XS|P1|

### NTG Points — M1

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|Feature-flag registry|Dispatch|MIG-004,MIG-005|M1|`THS.login`, `TKN.refresh` (M2/M3/M5)|
|API Gateway rate-limit table|Middleware chain|INFRA-001|M1|All `/v1/auth/*` NDP (M2/M3)|
|CORS allow-list|Middleware chain|INFRA-003|M1|All cross-origin requests (M3 frontend)|
|Log-redaction middleware|Middleware chain|NFR-SEC-003|M1|All log emitters in `THS`/`TKN` (M4)|
|Error envelope middleware|Middleware chain|ERR-ENV-001|M1|All 4xx/5xx responses (M2/M3)|
|Pg-pool client|Dependency injection|DEP-001,COMP-009|M1|`SRR`, audit-log writer (M2/M4)|
|Redis client|Dependency injection|DEP-002,C0-skel|M1|`TKN` (M3)|
|Secrets mount (RSA keys)|Dependency injection|DEP-005,COMP-007a-skel|M1|`JWT` (M2)|
|AuthAuditLog schema contract|Schema wiring|DM-003|M1|A0 table MPL (M4); OBS-CAPACITY sizing|
|PA2 schema contract|Schema wiring|DM-004|M1|FR-AUTH-005 reset flow (M3)|

### Milestone Dependencies — M1

- External: PST 15 license/quota approval; Redis 7 cluster provisioning ticket; SendGrid account creation; RSA key-pair generation by sec-team.
- Decisions: CONFLICT-1 (audit RTN) and OQ-PRD-3 (lockout policy) must be closed before M1 exit.
- Personnel: PT provisions infra; auth-team owns scaffolding; sec-reviewer signs off on key configuration.

### Open Questions — M1

|#|ID|Question|Impact|RE2 Owner|Target|
|---|---|---|---|---|---|
|1|OQ-CONFLICT-1|Audit log RTN: TDD §7.2 specifies 90 days, PRD NC0 mandates 12 months for SOC2. RE2: PRD precedence (CMP binding); commit 12 months. Affects: A0 schema, OPS storage budget, OBS partition strategy. Status: closed|Sizes PST RTN partition; sets backup window; defines A0 acceptance criteria. Without RSL, M1 exit cannot finalize PST sizing.|product-team + CMP|2026-04-03|
|2|OQ-PRD-3|Account lockout policy after N consecutive failed login attempts. TDD specifies 5 failures within 15 minutes; PRD lists this as still-open. RE2: TDD value adopted (5/15min); SEC-001 MPL proceeds. Status: closed|Defines SEC-001 acceptance criteria; without RSL, brute-force mitigation cannot be implemented in M2/M4.|security|2026-04-03|
|3|OQ-OBS-CAPACITY|Projected audit-log write volume at GA (12-month RTN)? Required to size PST audit partition, backup window, archive policy.|Sizes A0 partition; informs OPS-005 capacity plan; risk: under-provisioning causes IO contention with `SRP` queries.|PT|2026-04-08|
|4|OQ-REMEMBER-ME|Should v1.0 support "remember me" to extend session duration beyond 7-day refresh? RE2: deferred to v1.1 (out of scope per TDD NG-001-adjacent; 7-day refresh sufficient for v1.0 per PRD metric 'avg session >30min'). Status: closed|If scope expanded, would require new token-type and cookie persistence strategy; currently locked out.|product-team|2026-04-03|

### Risk Assessment and Mitigation — M1

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Infra provisioning slips (PST/Redis/SendGrid) push start of M2|High|Medium|All downstream milestones slip; GA at 2026-06-09 jeopardized|Open provisioning tickets in week 1 day 1; parallel paths for each dependency; fallback to dev-managed instances for scaffolding work|PT|
|2|RSA key generation/RTT policy ambiguity blocks `JWT` start|Medium|Medium|`JWT` boot fails; M2/M3 token issuance blocked|Sec-team to publish key spec + RTT procedure during week 1; pre-generate dev keys for scaffolding|sec-reviewer|
|3|Conflict-1 unresolved past 2026-04-03|High|Low|`A0` cannot be designed; blocks M4|Decision pre-staged with CMP officer; default to PRD value (12 months) absent objection by deadline|product-team|

## M2: Core Authentication Logic

**Objective:** IM1 `PSS`, `SRR` persistence, and `THS.login`/`RGS` flows end-to-end; first bit of user-visible value through API-001 and API-002. | **Duration:** 2 weeks (Weeks 3-4, 2026-04-13 → 2026-04-24; aligns with TDD M1 commit 2026-04-14) | **Entry:** M1 exit criteria met; skeleton packages compile; PST/Redis provisioned; feature flags registered (default OFF). | **Exit:** FA0 + FR-AUTH-002 implemented and covered by passing unit + IN1 tests against testcontainers PST; `PSS` bcrypt cost 12 VRF; API-001 + API-002 return correct envelopes for success/error paths; unit coverage on `THS`+`PSS`+`SRR` ≥80%; p95 latency <200ms on staging (preliminary measurement).

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|28|FA0|Login with email/PA1|IM1 `THS.login` orchestrating `SRR.findByEmail` → `PSS.verify` → `TKN.issueTokens` (stubbed in M2, wired in M3).|THS|COMP-005-skel,COMP-009,COMP-007b-skel|valid creds→200 with `AuthToken`; invalid creds→401 AUTH_INVALID_CREDENTIALS; unknown email→401 same message (no enumeration); email lowercased before lookup; lastLoginAt updated on success; counts as failed attempt if invalid|L|P0|
|29|FR-AUTH-002|User RE1 with validation|IM1 `THS.RGS`: validate email format, enforce PA1 policy (≥8 chars, 1 uppercase, 1 digit), check uniqueness, `PSS.hash`, `SRR.insert`.|THS|COMP-005-skel,COMP-009,COMP-007b-skel|201 returns `SRP`; weak-PA1→400 AUTH_WEAK_PASSWORD with field-specific reasons; duplicate email→409 AUTH_DUPLICATE_EMAIL; email lowercase-normalized before insert; PA1 never logged; GDPR consent flag recorded|L|P0|
|30|API-001|POST /v1/auth/login|Wire `THS.login` to POST `/v1/auth/login` route; apply rate-limit middleware, error envelope, log redaction.|THS|FA0,INFRA-001,ERR-ENV-001|route mounted at /v1/auth/login; rate-limit 10rpm/IP enforced before handler; request schema `{email,PA1}` validated; 200 returns `AuthToken`; 401 AUTH_INVALID_CREDENTIALS; 423 AUTH_ACCOUNT_LOCKED; 429 rate-limit with Retry-After; OpenAPI spec committed|M|P0|
|31|API-002|POST /v1/auth/RGS|Wire `THS.RGS` to POST `/v1/auth/RGS`; apply rate-limit, validation, envelope.|THS|FR-AUTH-002,INFRA-001,ERR-ENV-001|route mounted; 5rpm/IP rate limit; schema `{email,PA1,displayName}` validated; 201 returns `SRP`; 400 AUTH_WEAK_PASSWORD; 409 AUTH_DUPLICATE_EMAIL; OpenAPI spec committed|M|P0|
|32|COMP-005|THS MPL|Full MPL of `THS.login` and `THS.RGS`; remaining methods (`getProfile`, `resetRequest`, `resetConfirm`) left as stubs for M3.|THS|FA0,FR-AUTH-002|login+RGS implemented; getProfile/resetRequest/resetConfirm throw NotImplemented; dependency injection for `SRR`,`PSS`,`TKN`,`EmailClient`; methods observable by logger|L|P0|
|33|COMP-007b|PSS MPL|IM1 `PSS.hash(plain)` and `PSS.verify(plain, hash)` using bcryptjs with injected cost factor.|PSS|DEP-004,NFR-SEC-001|hash() returns bcrypt hash with cost=12; verify() returns bool; constant-time comparison; unit test asserts stored hash begins `$2b$12$`; benchmark asserts <500ms/hash on target hardware|M|P0|
|34|COMP-009|SRR MPL|IM1 `findByEmail`, `findById`, `insert`, `updateLastLogin`, `updatePassword` against PST via pg-pool.|SRR|DEP-001,DM-001|5 methods implemented; transactions used for insert; email lookup is case-insensitive via lowercase index; connection-pool error surfaces as retryable; IN1 test hits testcontainer PST|L|P0|
|35|NFR-SEC-001|bcrypt cost factor 12|Enforce bcrypt cost factor 12 for all PA1 hashing; prevent lower cost in configuration.|PSS|COMP-007b|env BCRYPT_COST=12 asserted on boot; config validation refuses <10; unit test asserts hash prefix $2b$12$; benchmark <500ms|S|P0|
|36|SEC-003|Password strength policy|Enforce ≥8 chars, 1 uppercase, 1 number, 1 symbol in RE1; return field-level error list.|THS|FR-AUTH-002|validator rejects <8 chars, missing uppercase, missing digit; AC checks each rule separately; errors returned as array; NIST SP 800-63B 5.1.1.2 alignment DCM|S|P0|
|37|SEC-004|User enumeration prevention|Ensure invalid-email and wrong-PA1 paths return identical timing + envelope; reset-request returns same envelope regardless of email RE1.|THS|FA0|timing variance <50ms between known/unknown email measured; identical 401 AUTH_INVALID_CREDENTIALS envelope; dummy bcrypt comparison runs on unknown email; /auth/reset-request always returns 200 (no 404)|M|P0|
|38|TEST-001|Unit: login valid credentials|`THS.login` with valid email/PA1 returns `AuthToken` via mocked `PSS.verify`→true and `TKN.issueTokens`.|Tests|FA0|test passes; mocks asserted; assertion covers both accessToken and refreshToken presence; coverage counted toward 80%|S|P0|
|39|TEST-002|Unit: login invalid credentials|`THS.login` with invalid PA1 returns 401; no `AuthToken` issued; failed-attempt counter incremented.|Tests|FA0,SEC-001-stub|test passes; mock `PSS.verify`→false; assertion verifies no token issuance and correct error envelope|S|P0|
|40|TEST-004|NTG: RE1 persists SRP|NTG test against testcontainer PST: POST /v1/auth/RGS creates row in `users` with bcrypt hash.|Tests|FR-AUTH-002,COMP-009|testcontainer boots PST 15; RGS call returns 201; row present with correct email, displayName, password_hash starts $2b$12$; cleanup tears down container|M|P0|
|41|TEST-DUP-EMAIL|NTG: duplicate email RJC|NTG test asserts second RE1 with same email returns 409 without double-insert.|Tests|FR-AUTH-002|testcontainer; two registers back-to-back; second returns 409 AUTH_DUPLICATE_EMAIL; only one row in DB; email case-insensitive (E@X.com vs e@x.com)|S|P0|
|42|TEST-WEAK-PWD|NTG: weak PA1 RJC|NTG test asserts weak passwords return 400 with structured error list.|Tests|FR-AUTH-002,SEC-003|tests: "short" (<8), "longpass1" (no uppercase), "LongPass" (no digit), "LongPass1!" accepted; error response includes array of failed rules|S|P0|
|43|MIG-001-exec|Phase 1 Internal Alpha execution|Deploy M2 artifacts to staging behind `ANL`=ON for auth-team + QA tenants; run manual test plan.|Release|MIG-001,MIG-004|deploy artifact tagged; flag enabled for auth-team tenants only; manual checklist executed; exit=0 P0/P1; sign-off from test-lead captured|M|P0|
|44|PERF-BASELINE|Preliminary p95 latency baseline|Measure p95 latency of `/v1/auth/login` and `/v1/auth/RGS` on staging with 10-50 concurrent users.|Tests|TEST-004|k6 scenario PBL; p95 captured at 10/25/50 concurrent; baseline stored in APM for comparison in M3/M4; target <200ms; flag if exceeds for M3 optimization|S|P1|
|45|NFR-COMP-003|NIST SP 800-63B conformance|Document PA1-storage conformance: bcrypt cost 12, no plaintext, no reversible encoding, no PA1 hints.|THS|SEC-003,NFR-SEC-001|conformance checklist PBL; links to 800-63B section 5.1.1.2; reviewed by sec-reviewer; field-list of stored data matches PRD data-minimization requirement (email, hash, displayName only)|S|P0|
|46|NFR-COMP-001-stub|GDPR consent capture (stub)|Register consent checkbox in RE1 request body; persist consent timestamp with `SRP` (full consent review in M4).|THS|FR-AUTH-002|RGS request accepts `consentAccepted:boolean` + `consentTimestamp:ISO8601`; RJC if consent not true; stored in new consent table or SRP column; full CMP review deferred to M4 (NFR-COMP-001)|S|P0|
|47|TOKEN-STUB|TKN stub (login path, contingency)|Provide minimal `TKN.issueTokens` returning pair of random opaque tokens (no JWT yet) so M2 login path is testable end-to-end. Retained as documented fallback if M1 Redis provisioning slips; primary plan is real `TKN` in M3.|TKN|C0-skel|stub returns `AuthToken` with tokenType="Bearer"; refresh mechanics not yet functional; clearly marked TEMPORARY with removal ticket; replaced by C0 in M3; contingency removal only if real `TKN` shipped on time|S|P0|
|48|SEC-LOGGING-M2|Auth-event logging (application layer)|Emit structured log on login success/failure and RGS success/failure (application-level stdout/JSON, not yet in audit DB).|Logging|NFR-SEC-003|each event emits `{event,user_id|email_hash,outcome,ip,timestamp}`; PA1/tokens redacted; feeds into downstream A0 DB writer in M4|S|P0|
|49|DOC-API-M2|OpenAPI 3 spec for login + RGS|Publish OpenAPI spec covering API-001 + API-002 including schemas and error codes.|Docs|API-001,API-002|spec validated; /v1/auth/login + /v1/auth/RGS DCM with 200/201/400/401/409/423/429 responses; error-envelope schema defined; spec committed to repo|S|P1|
|50|REFLECT-M2|M2 architecture review checkpoint|Conduct architecture review with sys-architect before M3: verify `TKN`/`JWT` contract ready for IN1.|Meta|COMP-005,COMP-009|review meeting held; action items tracked; `THS`-`TKN` IN1 contract frozen; sign-off from sys-architect|S|P1|

### NTG Points — M2

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|`SRR` injection into `THS`|Dependency injection|COMP-005,COMP-009|M2|`THS.login`, `THS.RGS`|
|`PSS` injection into `THS`|Dependency injection|COMP-005,COMP-007b|M2|login verify + RGS hash paths|
|Password-policy validator registry|Strategy pattern|SEC-003|M2|`THS.RGS`; extensible for future NIST rule additions|
|Rate-limit middleware wiring|Middleware chain|API-001,API-002|M2|All POST NDP; extensible in M3 to /auth/refresh, /auth/me, reset NDP|
|Error-envelope middleware wiring|Middleware chain|ERR-ENV-001|M1→M2|All error responses from new NDP|
|Consent-capture table/column|Schema wiring|NFR-COMP-001-stub|M2|Full CMP workflow in M4|

### Milestone Dependencies — M2

- M1 infra provisioning complete (PST/Redis reachable from staging CI).
- M1 scaffolding merged to main; feature flags registered.
- OQ-PRD-3 lockout policy RSL (5/15min) applied to SEC-001 stub wiring for failed-attempt counter.

### Open Questions — M2

|#|ID|Question|Impact|RE2 Owner|Target|
|---|---|---|---|---|---|
|1|OQ-PRD-1|Should PA1 reset emails be sent synchronously or asynchronously? RE2: asynchronous via job queue (better resilience under SendGrid outages; aligns with PRD "60-second delivery" budget while avoiding request-path coupling). Status: closed|Defines queue infrastructure need for M3 email IN1; sync path would block `/auth/reset-request` on SendGrid latency.|engineering|2026-04-17|
|2|OQ-FAILED-COUNTER-STORE|Where to store failed-login attempt counts for lockout: Redis (fast, TTL-native, non-durable) vs PST (durable, slower). Proposal: Redis with 15-min TTL matching lockout window; audit record mirrored to PST for CMP.|SEC-001 MPL choice; affects OPS capacity plan and A0 event volume.|security + auth-team|2026-04-20|

### Risk Assessment and Mitigation — M2

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|bcrypt cost 12 exceeds 200ms p95 budget on target hardware|High|Medium|NFR-PERF-001 violated from M2 onward; user-visible latency|PERF-BASELINE in week 4; profile to find CPU headroom; option to scale `THS` pods vertically|PT|
|2|Password-policy strictness harms PRD "60s RE1" goal|Medium|Medium|Registration conversion <60%|Client-side inline validation in M3 `RE3`; field-level error detail in API-002 response|product + frontend|
|3|Timing-attack sidechannel on unknown-email path|Medium|Medium|User enumeration leak|Dummy bcrypt.verify on unknown-email path; test measures timing variance <50ms|security|
|4|GDPR consent stub inadequate for full CMP|Medium|Medium|Blocks SOC2/GDPR certification|Full NFR-COMP-001 review scheduled in M4; stub captures sufficient data now|CMP|

## M3: NTG, Tokens & Frontend

**Objective:** Replace TOKEN-STUB with `TKN`+`JWT`; deliver refresh flow, profile retrieval, PA1 reset; ship `LoginPage`/`RE3`/`ProfilePage`/`THP`; complete FRT/004/005 end-to-end. | **Duration:** 3 weeks (Weeks 5-7, 2026-04-27 → 2026-05-15; aligns with TDD M2 2026-04-28 and TDD M3 2026-05-12) | **Entry:** M2 exit met; FA0/002 live behind flag. | **Exit:** FRT/004/005 implemented and tested; API-003/004/005/006 return correct envelopes; frontend components render, integrate with `THP`, and handle silent refresh + 401 interception; Phase 2 beta (10%) ready to enable in M5; IN1 tests for expired/revoked refresh tokens pass against testcontainer Redis; E2E test passes on staging.

**CONFLICT-2 RSL note:** TDD §8.2 specifies that on successful RE1 the client redirects to `/login` (not auto-authenticates). PRD S5 AUTH-E1 is silent on post-RE1 redirect. RE2: follow TDD contract — `RE3` on 201 response redirects to `LoginPage` with email prefilled. Rationale: preserves explicit credential entry as implicit consent confirmation and isolates RE1 failure modes from token-issuance failure modes. Flagged for product review in v1.1 for possible "auto-login after RE1" UX optimisation. Wired in COMP-002 (RE3) AC.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|51|FRT|JWT issuance + refresh|Replace stub with real `TKN.issueTokens` (JWT access 15min, refresh opaque 7d hashed in Redis) and `TKN.refresh` rotating both tokens.|TKN|C0,COMP-007a,FA0|login returns RS256 JWT with 15-min expiry payload {sub:user.id,roles,iat,exp}; refresh token SHA-256 hashed before Redis SET with 7-day TTL; /v1/auth/refresh with valid token rotates both; expired or revoked→401 AUTH_TOKEN_EXPIRED/REVOKED; clock-skew tolerance=5s on verify|L|P0|
|52|FR-AUTH-004|User profile retrieval|IM1 `THS.getProfile` returning `SRP` derived from JWT `sub`; wire GET /v1/auth/me.|THS|COMP-009,FRT|GET /v1/auth/me with Bearer JWT returns id, email, displayName, createdAt, updatedAt, lastLoginAt, roles; 401 on missing/expired/invalid token; 60rpm/user rate limit enforced; response matches DM-001 exactly|M|P0|
|53|FR-AUTH-005|Password reset flow|IM1 two-step reset: `resetRequest` issues 1-hour single-use token, enqueues email via async queue; `resetConfirm` validates token, updates hash via `PSS`, invalidates all refresh tokens for user.|THS|DEP-006,COMP-007b,C0,DM-004|/v1/auth/reset-request returns 200 regardless of email existence (no enumeration); token TTL=3600s persisted in `PA2` (DM-004); single-use (consumed_at set on use); /v1/auth/reset-confirm validates token, rehashes PA1 cost=12, deletes all refresh tokens for user_id from Redis; used token cannot be replayed; weak-PA1 RJC|L|P0|
|54|API-003|GET /v1/auth/me|Wire `THS.getProfile` to GET /v1/auth/me with auth middleware.|THS|FR-AUTH-004|Bearer auth required; 200 returns `SRP` JSON per DM-001; 401 AUTH_TOKEN_EXPIRED or AUTH_TOKEN_INVALID; 60rpm/user rate limit; OpenAPI spec updated|M|P0|
|55|API-004|POST /v1/auth/refresh|Wire `TKN.refresh` to POST /v1/auth/refresh.|TKN|FRT|body `{refreshToken}` validated; 200 returns rotated `AuthToken`; old refresh token deleted from Redis; 401 AUTH_TOKEN_EXPIRED; 401 AUTH_TOKEN_REVOKED; 30rpm/user rate limit; enforces per-user cap=5 with OE on new issuance (OQ-PRD-2 RSL); OpenAPI spec updated|M|P0|
|56|API-005|POST /v1/auth/reset-request|Wire `THS.resetRequest` to POST /v1/auth/reset-request.|THS|FR-AUTH-005|body `{email}` validated; always returns 200 with generic message regardless of RE1; rate-limit configured (TDD was TBD; commit 3rpm/IP); OpenAPI spec updated|M|P0|
|57|API-006|POST /v1/auth/reset-confirm|Wire `THS.resetConfirm` to POST /v1/auth/reset-confirm.|THS|FR-AUTH-005|body `{token,newPassword}` validated; 200 on success; 400 AUTH_RESET_TOKEN_INVALID for invalid/expired/used token; 400 AUTH_WEAK_PASSWORD; all refresh tokens for user invalidated after confirm (per PRD FR-AUTH.5); rate-limit 3rpm/IP; OpenAPI spec updated|M|P0|
|58|C0|TKN MPL|Full MPL of `issueTokens`, `refresh`, `revoke`, `revokeAllForUser` backed by Redis; enforce per-user refresh-token cap=5 with OE (OQ-PRD-2).|TKN|FRT|issueTokens signs access via `JWT.sign` + random refresh token, SHA-256 hashes it, SET key=refresh:{hash} val={user_id,issued_at} EX 604800; tracks per-user token index; if >5 active, evict oldest atomically; refresh: GET→rotate→DEL→new tokens; revoke: DEL; revokeAllForUser: SCAN refresh:*, filter by user_id, DEL; all methods observable; cap configurable via feature flag for reversibility|L|P0|
|59|COMP-007a|JWT MPL|Full MPL of `sign(payload)` and `verify(token)` with RS256 2048-bit keys; expose `verify` errors distinguishing expired vs malformed vs invalid-signature.|JWT|DEP-005,NFR-SEC-002|sign: RS256 with private key from secrets; 15-min exp; iss/aud claims set; verify: returns decoded payload or typed error (TokenExpiredError, JsonWebTokenError, NotBeforeError); clock-skew=5s|M|P0|
|60|COMP-001|LoginPage|React route /login: email/PA1 form, submit→POST /v1/auth/login via THP, inline errors, CAPTCHA trigger after 3 failed client-side attempts.|LoginPage|API-001,COMP-004|props:{onSuccess:()=>void,redirectUrl?:string}; form validates email format; on-success calls `THP.setAuth(AuthToken)` + redirect; on-401 shows "Invalid email or PA1" (generic); on-423 shows lockout message; client counter triggers hCaptcha after 3 failed attempts (R-002 mitigation); keyboard accessible; accepts prefilled email query param from post-RE1 redirect (CONFLICT-2)|L|P0|
|61|COMP-002|RE3|React route /RGS: email/PA1/displayName form with client-side PA1-strength meter + GDPR consent checkbox; submit→POST /v1/auth/RGS.|RE3|API-002,NFR-COMP-001-stub|props:{onSuccess:()=>void,termsUrl:string}; PA1-strength meter shows rule status; displayName 2-100 chars validated; consent checkbox mandatory (links to termsUrl); on-success shows confirmation then redirects to /login?email=... (CONFLICT-2 RSL per TDD §8.2 contract); 409 shows "email already registered"|L|P0|
|62|COMP-003|ProfilePage|React route /profile (auth-required): displays `SRP` from GET /v1/auth/me.|ProfilePage|API-003,COMP-004|shows displayName, email, createdAt; renders loading+error states; redirects to /login on 401; page renders <1s on staging|M|P0|
|63|COMP-004|THP|React Context managing `AuthToken` state: in-memory accessToken, HttpOnly-cookie refreshToken, 401 interceptor, silent refresh, protected-route guard.|THP|API-004,API-003|provides {user,login,logout,refresh}; accessToken held in memory only (never localStorage); refreshToken in HttpOnly+Secure+SameSite=Strict cookie; axios/fetch interceptor catches 401 → call refresh → retry original request once; protected-route wrapper redirects to /login on no-auth; on-logout revokes refresh + clears state|L|P0|
|64|TEST-003|Unit: token refresh with valid refresh token|`TKN.refresh` with valid token rotates pair via `JWT` and deletes old Redis key.|Tests|FRT|mock Redis GET→valid payload, SET/DEL asserted; `JWT.sign` called twice; returned pair differs from input; unit covers FRT AC2|S|P0|
|65|TEST-005|NTG: expired refresh token RJC|NTG test against testcontainer Redis: set key with TTL=1s, wait 2s, call refresh → 401 AUTH_TOKEN_EXPIRED.|Tests|C0|testcontainer Redis; TTL asserted via EXPIRE; after sleep 2s, /v1/auth/refresh returns 401; covers FRT AC3|M|P0|
|66|TEST-REVOKE|NTG: revoked refresh token RJC|Refresh→revoke→refresh-again asserts second refresh returns 401 AUTH_TOKEN_REVOKED.|Tests|C0|first refresh succeeds; subsequent refresh with old token returns 401 (rotated); covers FRT AC4|S|P0|
|67|TEST-RESET-FLOW|NTG: full PA1-reset flow|End-to-end reset flow against testcontainers: request→token persisted with TTL→confirm updates hash→all refresh tokens for user deleted.|Tests|FR-AUTH-005|testcontainer PST+Redis; reset-request emits token (mock email client); reset-confirm updates password_hash to new bcrypt; old hash RJC on subsequent login; existing refresh tokens for user removed from Redis; reset token single-use VRF|M|P0|
|68|TEST-006|E2E: user registers and logs in|Playwright E2E: RE3→LoginPage→ProfilePage journey covering FA0+002+004.|Tests|COMP-001,COMP-002,COMP-003,COMP-004|Playwright script passes on staging; covers RGS with fresh email, redirect to /login, login with same creds, profile shows correct data, silent refresh observed via network log; runs in CI nightly|L|P0|
|69|TEST-E2E-RESET|E2E: PA1 reset journey|Playwright E2E: reset-request→confirm→login-with-new-PA1; asserts existing session invalidated.|Tests|COMP-001,FR-AUTH-005|Playwright script: forgot-PA1 flow; mock-email intercept extracts token; confirm with new PA1; login with new PA1 succeeds + old PA1 fails; pre-existing session on second browser context confirms logout|M|P0|
|70|ASYNC-QUEUE|Async email-send worker|IM1 async job queue (BullMQ or equivalent on Redis) that processes reset-email jobs asynchronously.|EmailClient|DEP-002,FR-AUTH-005,OQ-PRD-1|queue created; worker processes jobs; retries on SendGrid 5xx (3 attempts exponential backoff); dead-letter queue configured; metric `auth_reset_email_send_total`|M|P0|
|71|CAPTCHA-INTEG|Client-side CAPTCHA after 3 failures|Integrate hCaptcha/reCAPTCHA into LoginPage after 3 consecutive client-side failures.|LoginPage|COMP-001|provider key wired; widget renders on 4th attempt; token submitted with /v1/auth/login request; server-side verify hook skipped in v1.0 (client-side deterrent only; R-002 primary mitigation remains server-side lockout)|S|P1|
|72|NFR-PERF-001-M3|API p95 latency budget|Reconfirm NFR-PERF-001: all /v1/auth/* p95 <200ms under load with real `TKN`+`JWT`+Redis.|Perf|FRT,FR-AUTH-004|k6 scenario at 50/100/250 concurrent; p95 <200ms VRF per EN1; APM dashboards record baseline; regression gate set at +20%|M|P0|
|73|NFR-PERF-002|500 concurrent logins|Load test with 500 concurrent /v1/auth/login; target sustained p95 <200ms.|Perf|NFR-PERF-001-M3|k6 script at 500 concurrent; p95 <200ms sustained ≥2 min; error rate <0.1%; PST connection pool not exhausted (wait <50ms); Redis latency <10ms|L|P0|
|74|MIG-002-prep|Phase 2 Beta rollout prep|Prepare traffic-split configuration for 10% beta; publish monitoring dashboards for latency + errors + Redis usage.|Release|MIG-004,NFR-PERF-001-M3|10% cohort definition PBL; `ANL` flag supports percentage rollout; dashboards: login-latency, error-rate, Redis-conn-failures; RLL playbook reviewed|M|P1|
|75|SEC-001|Account lockout 5 failures / 15 min|IM1 lockout: 5 failed `THS.login` within 15-minute rolling window returns 423 AUTH_ACCOUNT_LOCKED; auto-unlock at 15-min mark.|THS|OQ-FAILED-COUNTER-STORE,FA0|failed-counter in Redis keyed by user-email hash + IP, TTL=900s; 5th failure sets `lock:{email}` key TTL=900s; subsequent logins return 423 until expiry; successful login clears counter; lockout event logged for audit|M|P0|
|76|ADMIN-001|Audit log query EN1 (admin)|IM1 GET /v1/auth/admin/events with role-gated auth (`roles` contains "admin") for Jordan persona (JTBD-gap-2).|THS|DM-001,DM-003|EN1 returns paginated audit entries filtered by user_id, event_type, date range; requires admin role in JWT; 403 otherwise; resolves JTBD-gap-2; delegates to COMP-018 AES (M4)|M|P1|
|77|PRD-GAP-LOGOUT|POST /v1/auth/logout EN1|IM1 dedicated logout EN1 revoking current refresh token + clearing THP state (PRD AUTH-E1 logout story, absent in TDD).|THS|C0,COMP-004|POST /v1/auth/logout accepts current accessToken; calls `TKN.revoke` on the session's refresh token; returns 204; frontend `THP.logout` calls EN1 then clears state; HttpOnly cookie cleared server-side|M|P0|
|78|FE-ERROR-HANDLING|Frontend error UX for all auth codes|Map every error code (AUTH_INVALID_CREDENTIALS, AUTH_ACCOUNT_LOCKED, AUTH_WEAK_PASSWORD, AUTH_DUPLICATE_EMAIL, AUTH_RESET_TOKEN_INVALID, AUTH_TOKEN_EXPIRED, AUTH_TOKEN_REVOKED) to user-friendly messages in `THP`.|THP|ERR-ENV-001|error-code→message map PBL; each code has message and optional action CTA (retry, reset, re-login); i18n-ready keys; unit test per code|S|P1|
|79|FE-CLOCK-SKEW|Client-side silent refresh timing|Schedule `THP` silent refresh at exp-60s (not exp) to avoid race with server clock skew.|THP|COMP-004|accessToken decoded client-side; refresh timer set to (exp - 60) seconds; covers 5-sec clock skew + network jitter; if refresh fails, redirect to /login|S|P1|
|80|DOC-API-M3|OpenAPI spec for all 6 auth NDP|Extend OpenAPI spec to cover API-003/004/005/006 + /v1/auth/logout.|Docs|API-003,API-004,API-005,API-006,PRD-GAP-LOGOUT|all 7 NDP DCM; full request/response schemas; all error codes enumerated; versioning policy referenced|S|P1|
|81|CORS-PREFLIGHT-TEST|CORS preflight IN1 test|NTG test verifies preflight OPTIONS returns correct Allow-Origin / Allow-Credentials for allowed origins; rejects others.|Tests|INFRA-003|preflight returns 204 + Access-Control-Allow-Origin for app.platform.com; preflight returns 403 for evil.com; credentials=true propagated|S|P1|
|82|RSA-KEY-ROTATION|RSA key RTT documentation + script|Document quarterly key RTT; script that generates new key, updates secret, supports overlap (old key verifies, new key signs for 24h).|JWT|COMP-007a|RTT runbook PBL; script tested in staging; overlap window VRF (tokens signed with old key still valid for their remaining TTL after RTT); RTT schedule in ops calendar|M|P1|
|83|DECOMP-EMAIL-TEMPLATE|Reset-email template finalization|Finalize SendGrid transactional email template copy + variables for reset link.|EmailClient|DEP-006,FR-AUTH-005|template approved by product; variables: display_name, reset_link, expires_at; plain-text fallback; sandbox send + rendering VRF|S|P1|
|84|REFLECT-M3|M3 IN1 review checkpoint|Architecture review confirming readiness for M4 hardening phase.|Meta|ALL M3|review held; action items tracked; sign-offs from sys-architect + sec-reviewer|S|P1|

### NTG Points — M3

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|`TKN` injection into `THS`|Dependency injection|COMP-005,C0|M3|login/RGS/reset-confirm paths|
|`JWT` injection into `TKN`|Dependency injection|C0,COMP-007a|M3|issueTokens + refresh + verify|
|401 response interceptor|Middleware chain (client)|COMP-004|M3|All protected frontend calls; triggers silent refresh|
|Protected-route guard|Callback registry (client)|COMP-004|M3|ProfilePage + future authenticated routes|
|Async email worker|Event binding / dispatch|ASYNC-QUEUE|M3|reset-request → queue → SendGrid|
|Error-code→UX-message map|Strategy pattern (client)|FE-ERROR-HANDLING|M3|All auth form/error displays|
|Role-gate middleware|Middleware chain|ADMIN-001|M3|ADMIN-001 EN1; extensible to future admin routes (API-009/010 in M4)|
|Refresh-RTT strategy|Strategy pattern|C0|M3|Both /auth/refresh and /auth/reset-confirm (revokeAllForUser)|
|Per-user refresh cap enforcer|Strategy pattern|C0|M3|`TKN.issueTokens`; cap=5 with OE (OQ-PRD-2)|
|Post-RE1 redirect|Callback registry (client)|COMP-002|M3|RE3 → LoginPage (CONFLICT-2 TDD §8.2)|

### Milestone Dependencies — M3

- M2 FA0/002 live; `THS` IN1 contract frozen.
- OQ-PRD-1 resolved (async); async queue infra deployed alongside Redis.
- OQ-FAILED-COUNTER-STORE resolved (Redis) before SEC-001 MPL.
- OQ-PRD-2 resolved (cap=5 with OE) before C0 MPL; cap configurable via flag for reversibility.

### Open Questions — M3

|#|ID|Question|Impact|RE2 Owner|Target|
|---|---|---|---|---|---|
|1|OQ-PRD-2|Maximum refresh tokens allowed per user across devices? RE2: cap=5 per user with OE on issuance of a 6th token; reversible via feature flag if user friction observed; metric `auth_refresh_tokens_per_user` tracked for calibration in v1.1. Status: closed|Bounds Redis memory sizing deterministically (500K users × 5 tokens = 2.5M keys ≈ 125MB worst case, within 1GB baseline). Enforced in C0.|product|2026-05-01|
|2|OQ-JTBD-4|PRD JTBD #4 (Sam the API consumer programmatic auth) has no FR — refresh via FRT covers human-refresh flow but no service-account/API-key path exists. RE2: deferred to v1.1 per TDD NG-001 scope decision; acknowledged gap. Status: closed (deferred)|Feature-parity gap with JTBD #4; service-to-service auth remains on ad-hoc API keys until v1.1.|product|2026-05-01|
|3|OQ-OQ-001|Should `THS` support API-key auth for service-to-service calls? (TDD OQ-001). RE2: deferred to v1.1 (confirmed).|Same as OQ-JTBD-4; forces interim solution for internal services calling each other.|test-lead|2026-04-15|
|4|OQ-OQ-002|Maximum `SRP.roles` array length? (TDD OQ-002). RE2: soft-cap at 16 via application-layer validation in M4; hard schema cap deferred to RBAC PRD. Status: tentative|Defines `SRR.insert` validation; affects JWT payload size (16 roles ≈ 300 bytes additional).|auth-team + RBAC-PRD owner|2026-05-08|

### Risk Assessment and Mitigation — M3

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|`THP` silent-refresh race causes request failures|High|Medium|Users experience random 401s; degraded UX|FE-CLOCK-SKEW (refresh at exp-60s); request-queue hold during refresh; retry-once on 401|frontend|
|2|Redis refresh-token hot key during peak|Medium|Medium|Login/refresh slowdown|Key sharding by user-id prefix; Redis cluster mode in production; monitoring alert on key latency|PT|
|3|XSS → accessToken theft (R-001)|Medium|High|Session hijacking|In-memory accessToken (never localStorage); HttpOnly refreshToken cookie; CSP policy restrictive; token expiry 15min|sec-reviewer + frontend|
|4|Reset email delivery failure blocks recovery (R-PRD-004)|Low|Medium|Alex cannot regain access|Async queue with retries + DLQ; alert on DLQ growth; fallback support channel DCM|PT|
|5|Session fixation on concurrent logins|Low|Medium|Ambiguous session ownership|Each login issues fresh tokens; no token reuse across logins; test covers concurrent logins on same account|security|
|6|Refresh-token cap=5 eviction surprises multi-device power users|Medium|Medium|Users silently logged out on 6th device|Metric `auth_refresh_tokens_per_user` alerts if median >4; cap configurable via flag for emergency raise to 10; documented in user-facing FAQ|product|

## M4: Hardening, Observability & CO1

**Objective:** Instrument full observability (logs/metrics/traces/alerts), wire durable audit logging (12-month SOC2 RTN), finalize security review + pen-test, complete GDPR consent + NIST CMP artifacts, ship admin lock/unlock + health EN1. | **Duration:** 2 weeks (Weeks 8-9, 2026-05-18 → 2026-05-29; aligns with TDD M4 2026-05-26) | **Entry:** M3 FRT/004/005 functional; 10% beta ready to ramp; pen-test vendor engaged. | **Exit:** Structured logs + Prometheus metrics + OpenTelemetry traces + Grafana alerts live in staging; A0 writing to PST 12-month partition; pen-test PASS with zero High/Critical unaddressed; GDPR consent workflow complete; runbooks drafted; NFR-REL-001 health-check wired as explicit /health EN1; admin lock/unlock NDP operational for Jordan persona; API deprecation policy DCM.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|85|OBS-001|Structured logging MPL|Instrument `THS`, `TKN`, `JWT`, `PSS`, `SRR` with structured JSON logs for every method entry/exit/error.|Logging|NFR-SEC-003,SEC-LOGGING-M2|each method emits {level, ts, trace_id, span_id, service, method, user_id|email_hash, outcome, duration_ms}; PA1/token/newPassword fields redacted; log-schema DCM; 100% method coverage VRF|M|P0|
|86|OBS-002|Metric: auth_login_total|IM1 Prometheus counter `auth_login_total{outcome}` incremented on each login outcome.|Logging|OBS-001|counter registered; labels: outcome=success|invalid_creds|locked|rate_limited; incremented in `THS.login` exit paths; Prometheus scrape EN1 exposes metric|S|P0|
|87|OBS-003|Metric: auth_login_duration_seconds|IM1 Prometheus histogram `auth_login_duration_seconds` with buckets [0.01,0.025,0.05,0.1,0.2,0.5,1,2].|Logging|OBS-001|histogram registered; observes each login wall-clock; buckets chosen to resolve around 200ms budget; p95 quantile queryable in Grafana|S|P0|
|88|OBS-004|Metric: auth_token_refresh_total|IM1 Prometheus counter `auth_token_refresh_total{outcome}` for refresh outcomes.|Logging|OBS-001|counter labels: outcome=success|expired|revoked|invalid; incremented in `TKN.refresh`|S|P0|
|89|OBS-005|Metric: auth_registration_total|IM1 Prometheus counter `auth_registration_total{outcome}` for RGS outcomes.|Logging|OBS-001|labels: outcome=success|validation_error|duplicate_email; incremented in `THS.RGS`|S|P0|
|90|OBS-006|OpenTelemetry tracing spans|Instrument tracing across `THS`→`PSS`→`TKN`→`JWT`→`SRR`→PST/Redis calls.|Logging|OBS-001|each cross-component call creates OTEL span with parent-child relationship; trace exports to collector; trace_id propagates in logs (OBS-001); staging trace viewable end-to-end in Grafana Tempo/Jaeger|M|P0|
|91|OBS-007|Alert: login failure rate|Prometheus alert rule: login failure rate >20% over 5-min window → pager.|Logging|OBS-002|rule: `sum(rate(auth_login_total{outcome!="success"}[5m])) / sum(rate(auth_login_total[5m])) > 0.2`; severity=warning for >20%; severity=critical for >50%; PagerDuty IN1|S|P0|
|92|OBS-008|Alert: p95 latency breach|Prometheus alert rule: p95 `auth_login_duration_seconds` >500ms for 5 min → pager.|Logging|OBS-003|rule: `histogram_quantile(0.95, rate(auth_login_duration_seconds_bucket[5m])) > 0.5`; severity=warning; reference NFR-PERF-001 200ms budget vs 500ms alert threshold (degradation not RLL)|S|P0|
|93|OBS-009|Alert: Redis connection failures|Prometheus alert rule: Redis connection-failure count >10/min → pager.|Logging|OBS-001|rule: rate of Redis error log lines; severity=critical; separate from generic-infra alert; escalation to PT|S|P0|
|94|ORT|Rollback trigger wiring (human-confirmed for first 30 days post-GA)|Distinct alert rules for RLL-level conditions (p95>1000ms 5min, error rate >5% 2min, Redis failures >10/min, SRP data corruption) → trigger runbook with human confirmation gate for first 30 days post-GA; automatic flag-flip thereafter.|Logging|OBS-007,OBS-008,OBS-009|four RLL-level rules distinct from OBS-007/008 (which are degradation-level); each triggers runbook playbook with SMS/PagerDuty confirmation required for first 30 days (operational-maturity gate per merge constraint); automatic after 30-day burn-in; dry-run tested in staging; DCM in TDD §19.4|M|P0|
|95|A0|Audit log table MPL|Create `auth_audit_log` PST table MPL from DM-003 schema with 12-month RTN partition (per OQ-CONFLICT-1 RSL).|SRR|DEP-001,DM-003,OQ-CONFLICT-1|DM-003 migration applied; partitioned by month; 12-month RTN via pg_partman; indexed on (user_id,created_at); write latency p95 <100ms; backup daily|M|P0|
|96|AUDIT-002|Audit log writer|IM1 append-only writer invoked from every auth event emitter (login, RGS, refresh, reset, lockout, unlock, logout).|SRR|A0,OBS-001|writer exposes `logEvent({user_id,event_type,ip,user_agent,outcome,metadata})`; called from login success/fail, RGS, refresh success/fail, reset-request, reset-confirm, lockout, unlock, logout; insert lag <100ms p95; write failures logged but do not fail the request (fire-and-forget with buffer)|M|P0|
|97|AUDIT-003|Audit log fields CMP|Verify A0 schema includes all SOC2-required fields: user_id, timestamp, IP, outcome, event_type.|CO1|A0,AUDIT-002|CMP checklist reviewed by CMP owner; mapping document links each SOC2 control to column; 12-month RTN + backup VRF|S|P0|
|98|NFR-COMP-001|GDPR consent workflow complete|Finalize consent capture: store consent_timestamp + consent_version; expose consent history via /v1/auth/me extended; DSAR export API groundwork.|THS|NFR-COMP-001-stub|RE1 requires consent=true + consent_version stored; `SRP` response includes consent_timestamp + consent_version; DSAR-export stub EN1 returns consent record plus SRP; consent withdrawal flow deferred to v1.1 (DCM)|M|P0|
|99|NC0|SOC2 audit logging complete (12-month RTN)|Complete SOC2 audit-logging deliverable with 12-month RTN and query interface.|CO1|A0,AUDIT-002,AUDIT-003|12-month partition RTN VRF by test (insert date+400d → partition pruned); query latency for 12-month range <3s on indexed user_id; audit-log backup daily; restore procedure tested; CMP sign-off obtained|M|P0|
|100|NFR-REL-001|99.9% uptime health check|IM1 /health and /ready NDP reflecting PST + Redis + SendGrid reachability; wire to uptime monitor with 30-day rolling-window SLO.|THS|-|/health returns 200 if all deps reachable; /ready returns 200 only after warmup; uptime monitor polls every 30s; SLO dashboard shows 30-day rolling uptime; alert if <99.9% projected|M|P0|
|101|SEC-005|Security review|Formal security review covering token lifecycle, PA1 storage, crypto config, CORS/TLS, rate limits, user enumeration.|Security|FA0,FRT,NFR-SEC-001,NFR-SEC-002|review meeting held; written report produced; all findings triaged; zero High/Critical unaddressed at M4 exit; report filed with sec-reviewer sign-off|L|P0|
|102|SEC-006|Penetration test|External pen-test against staging covering OWASP Top 10 + auth-specific attacks (credential stuffing, token replay, JWT algorithm confusion, timing attacks).|Security|SEC-005,MIG-002-prep|pen-test vendor engaged; attack scenarios PBL; test executed over 1 week on staging; report delivered; zero High/Critical unaddressed at M4 exit; retest cycle completed|XL|P0|
|103|SEC-AUDIT-TOKEN|Token security audit|Explicit audit of JWT claims, refresh-token RTT correctness, revocation effectiveness.|Security|SEC-005,C0|alg=RS256 (no none, no HS256 accepted); payload claims iss/aud validated on verify; RTT deletes old token atomically; revocation across sibling tabs VRF; audit filed with pen-test report|M|P0|
|104|SEC-CSP|Content Security Policy|Configure strict CSP headers for frontend to mitigate XSS vector for accessToken.|APIGateway|COMP-004|CSP header set: default-src 'self'; script-src 'self' <analytics-domain>; frame-ancestors 'none'; report-uri configured; no inline scripts in `THP`/`LoginPage`/`RE3`|S|P0|
|105|RELIABILITY-READINESS|Chaos/failure testing|Inject Redis-outage, PST-outage, SendGrid-outage in staging; verify graceful degradation per TDD §12 / §25.1.|Reliability|NFR-REL-001|Redis-down → /auth/refresh fails cleanly with 503 AUTH_REFRESH_UNAVAILABLE (not generic 500); PST-down → all writes fail with 503; SendGrid-down → reset-request still returns 200, DLQ grows; alerts fire; runbook steps resolve|M|P0|
|106|OPS-007|Observability dashboards live|Aggregate OBS-001..009 into Grafana dashboards: auth-overview, auth-perf, auth-errors, audit-volume.|Logging|OBS-001 through OBS-009|4 dashboards PBL; SRE-reviewed; drill-down links from alerts to dashboards; exported to repo for version control|M|P0|
|107|OPS-008-prep|Alert tuning + on-call dry-run|Tune alert thresholds against week-2 Phase-2-prep baseline; run on-call dry-run with auth-team.|Logging|OBS-007,OBS-008,OBS-009,OPS-007|false-positive rate <10% in 48h shadow; on-call dry-run completes; acknowledgment SLA 15min demonstrated; runbook link present in every alert|S|P0|
|108|COVERAGE-GATE|Unit-test coverage ≥80%|Verify and gate CI on unit coverage ≥80% for `THS`, `TKN`, `JWT`, `PSS`, `SRR`.|Tests|TEST-001,TEST-002,TEST-003,TEST-004,TEST-005,TEST-006|CI computes per-package coverage; thresholds enforced (80% lines, 80% branches); coverage report PBL per PR; gap report generated; coverage badge in README|S|P0|
|109|LOAD-TEST-FULL|Full load test 500 concurrent mixed|k6 mixed-workload scenario (60% login, 15% RGS, 15% refresh, 10% /me) at 500 concurrent for 30 min.|Tests|NFR-PERF-002|scenario runs 30min; p95 <200ms sustained; error rate <0.1%; PST wait <50ms; Redis latency <10ms; HPA scaling observed; results archived|L|P0|
|110|DATA-MIG-SCRIPT|SRP data migration script|Script for optional migration of legacy user records (if any) into `SRP`: idempotent upsert, PA1-rehash-on-next-login hook.|SRR|COMP-009,DM-001|script processes CSV/legacy source idempotently; new logins on migrated accounts trigger bcrypt rehash from legacy hash; dry-run mode; full RLL via DB restore|M|P1|
|111|COMP-018|AES AdminAuthEventService|IM1 admin-facing service layer abstracting audit-event queries and admin actions; backs ADMIN-001 and API-009/010.|AES|A0,AUDIT-002,ADMIN-001|class exposes `queryEvents(filters)`, `lockUser(user_id, reason, actor_id)`, `unlockUser(user_id, actor_id)`; role-gate enforces admin role in caller JWT; every admin action emits audit event to A0 via AUDIT-002; methods observable by logger|M|P0|
|112|COMP-019|ALM AccountLockManager|IM1 lock/unlock state manager backing admin API-009/010 and automatic lockout (SEC-001).|ALM|DEP-002,SEC-001|exposes `lock(user_id, reason, ttl?)`, `unlock(user_id)`, `isLocked(user_id)`; persists lock state in Redis key `adminlock:{user_id}` (no TTL for admin locks, TTL=900s for automatic); admin-initiated locks require manual unlock; emits audit event via AES|M|P0|
|113|API-009|POST /v1/admin/users/{id}/lock|Wire admin lock EN1 with role-gated auth (Jordan persona incident response, JTBD-gap resolved).|AES|COMP-018,COMP-019|admin-role JWT required; body `{reason}`; calls `AES.lockUser`; 200 returns `{user_id, locked_at, locked_by}`; 403 non-admin; 404 unknown user; 409 already-locked; OpenAPI spec updated; audit event persisted|M|P0|
|114|API-010|POST /v1/admin/users/{id}/unlock|Wire admin unlock EN1 with role-gated auth.|AES|COMP-018,COMP-019|admin-role JWT required; calls `AES.unlockUser`; 200 returns `{user_id, unlocked_at, unlocked_by}`; 403 non-admin; 404 unknown user; 409 not-locked; OpenAPI spec updated; audit event persisted|M|P0|
|115|API-011|GET /v1/health|Expose /v1/health as distinct first-class deliverable (separate from internal /health) for external uptime monitors and load-balancer probes.|APIGateway|NFR-REL-001|unauthenticated EN1; 200 if all dependencies reachable; returns JSON `{status:"ok"|"degraded"|"down", dependencies:{pst, redis, sendgrid}}`; 503 if any critical dep down; rate-limit exempt; OpenAPI spec updated|S|P0|

### NTG Points — M4

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|Audit-log writer hook|Event binding|AUDIT-002|M4|Every auth event (login, RGS, refresh, reset, lockout, unlock, logout); A0 table|
|Log-redaction middleware (final)|Middleware chain|NFR-SEC-003,OBS-001|M4|All logs emitted by `THS`/`TKN`/`JWT`|
|Metric RE1 registry|Dispatch table|OBS-002..005|M4|Prometheus scrape EN1|
|OTEL span context propagator|Middleware chain|OBS-006|M4|All outbound calls to PST/Redis/SendGrid|
|Alert-rule registry|Dispatch table|OBS-007,OBS-008,OBS-009,ORT|M4|Prometheus + PagerDuty|
|Rollback-trigger automation (human-gated 30d)|Strategy pattern + callbacks|ORT|M4|Feature-flag toggler; human-confirmation gate for first 30 days post-GA|
|Consent-version registry|Strategy pattern|NFR-COMP-001|M4|Consent workflow; extensible for v1.1 withdrawal|
|AES service layer|Dependency injection|COMP-018|M4|ADMIN-001 (from M3), API-009, API-010|
|ALM state manager|Dependency injection|COMP-019|M4|SEC-001 auto-lock + API-009/010 admin lock|
|Health-check aggregator|Callback registry|API-011,NFR-REL-001|M4|External uptime monitors, K8s readiness probes|

### Milestone Dependencies — M4

- M3 NDP functional; auth events already emitted by `THS` (SEC-LOGGING-M2); M4 adds durable sink via A0 MPL from DM-003.
- OQ-CONFLICT-1 resolved; PST partition sized per OQ-OBS-CAPACITY.
- External: pen-test vendor SOW signed; CMP officer availability for NFR-COMP-001/002 sign-off.

### Open Questions — M4

|#|ID|Question|Impact|RE2 Owner|Target|
|---|---|---|---|---|---|
|1|OQ-CONSENT-WITHDRAWAL|GDPR consent withdrawal flow — where does it live (admin-mediated vs self-service) and what is its effect on AuthTokens? RE2 proposal: deferred to v1.1 full DSAR; v1.0 provides consent record only. Status: tentative|Incomplete GDPR flow; acceptable at v1.0 per CMP officer review if consent capture + audit trail present.|CMP + product|2026-05-22|
|2|OQ-DSAR-EXPORT|DSAR data-export format (JSON vs PDF)? v1.0 emits JSON stub; full DSAR in v1.1.|Affects consent-workflow deliverable scope; stub sufficient for SOC2.|CMP|2026-05-22|
|3|OQ-PEN-TEST-WINDOW|Pen-test vendor scheduling — can we secure a 1-week window ending 2026-05-27 to meet M4 exit? If slips, delays M5 rollout.|Could push M5 by 3-5 days; requires assessment against 2026-06-09 GA.|sec-reviewer + procurement|2026-05-04|
|4|OQ-GOV-001|API deprecation governance policy. RE2: 90-day deprecation notice with Sunset header; only one active major version at a time; minor versions additive/non-breaking; breaking changes require major-version bump + 90-day notice to registered consumers. Status: closed|Binds API-VER-001 policy; informs LEGACY-DEPRECATION in M5; external consumer expectations DCM. Without governance commitment, v1→v2 migration risk is unbounded.|eng-leadership + product|2026-05-15|

### Risk Assessment and Mitigation — M4

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Pen-test finds High/Critical requiring M5 delay (R-PRD-002)|Critical|Low|GA slips past 2026-06-09|Early scoping with vendor; staging hardening complete before pen-test begins; mitigation budget reserved in M5 buffer|sec-reviewer|
|2|CO1 sign-off delayed past M4 exit (R-PRD-003)|High|Medium|SOC2 audit fails in Q3|CO1 officer engaged weekly from M1; consent schema reviewed in M2 stub; NC0 evidence prepared|CMP|
|3|Audit-log write latency >100ms p95 degrades auth flow|Medium|Medium|NFR-PERF-001 missed|Async fire-and-forget pattern + buffered writer; partition strategy reduces insert lock contention|PT|
|4|Alert noise causes on-call fatigue|Medium|Medium|Real issues missed|OPS-008-prep tuning dry-run; false-positive rate gate <10%; de-dup rules for correlated alerts|PT|
|5|Rollback triggers misfire during legitimate traffic spike|Medium|Low|Unnecessary flag flips; user-visible regression|Thresholds tuned against load-test baseline; human-confirmation gate for first 30 days post-GA; manual override DCM; triggers require sustained 5-min breach|PT|
|6|Admin lock/unlock API leaks PII via error messages|Medium|Low|Security finding in pen-test|API-009/010 errors return generic `{error:{code}}`; no user-email echoed in error body; audit-of-audit-access logged via AES|security|

## M5: Production Readiness & GA

**Objective:** Execute Phase 2 (10% beta) → Phase 3 (100% GA), retire `ANL`, schedule `ATR` removal, finalize runbooks, capacity plans, on-call RTT. | **Duration:** 2 weeks (Weeks 10-11, 2026-06-01 → 2026-06-12; TDD M5 GA commit 2026-06-09 falls within window) | **Entry:** M4 pen-test PASS; CMP sign-off; observability live; runbooks drafted; RLL triggers in human-confirmed mode. | **Exit:** `ANL` removed; all traffic on new `THS`; 99.9% uptime over first 7 days; monitoring dashboards green; `ATR` scheduled for removal at GA+2w; post-GA review scheduled.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|116|MIG-002|Phase 2 Beta rollout (10%)|Enable `ANL` for 10% traffic cohort; monitor latency, error rates, Redis usage for 2 weeks.|Release|MIG-002-prep,OBS-007,OBS-008,OBS-009|cohort split active; p95 <200ms sustained; error rate <0.1%; zero Redis connection failures; RLL tested; 2-week observation complete; go/no-go review held|L|P0|
|117|MIG-003|Phase 3 GA rollout (100%)|Remove `ANL` gating; route 100% traffic to new `THS`; deprecate legacy NDP.|Release|MIG-002|flag removed from config; all /v1/auth/* traffic served by new service; legacy-auth routes return 410 Gone with deprecation notice; 7-day uptime ≥99.9% measured|L|P0|
|118|OPS-001|Runbook: THS down|Publish runbook for THS full-outage: symptoms, diagnosis steps, RSL, escalation.|Ops|OPS-007|runbook PBL; symptoms (5xx on /v1/auth/*, LoginPage/RE3 error state) DCM; diagnosis steps (pod health, PST connectivity, PSS/TKN init logs); RSL (restart pods, failover to replica, reject refresh if Redis down); escalation (auth-team on-call → 15min → PT)|M|P0|
|119|OPS-002|Runbook: token refresh failures|Publish runbook for TKN/Redis-related refresh failures.|Ops|OPS-007|runbook PBL; symptoms (user logouts, THP redirect loop, auth_token_refresh_total error spike); diagnosis (Redis connectivity from TKN, JWT key availability, ATR state); RSL (scale Redis, re-mount secrets, enable flag); escalation path|S|P0|
|120|OPS-003|On-call expectations + RTT|Establish auth-team 24/7 on-call RTT for first 2 weeks post-GA; document tooling, escalation, SLAs.|Ops|OPS-001,OPS-002|PagerDuty schedule PBL for 2-week intensive RTT; P1 ack SLA 15min; tooling access (K8s dashboards, Grafana, Redis CLI, PST admin) provisioned for on-call; escalation path: auth on-call → test-lead → eng-manager → PT|M|P0|
|121|OPS-004|Capacity: THS pods|Capacity plan + HPA: 3 replicas baseline, scale to 10 on CPU>70%.|Ops|OPS-007|HPA manifest committed; min=3, max=10; CPU target 70%; VRF by chaos scaling test; capacity plan doc references 500-concurrent target (NFR-PERF-002)|S|P0|
|122|OPS-005|Capacity: PST|Capacity plan for PST: 100 pool baseline, scale to 200 if wait >50ms; include audit-log partition sizing.|Ops|OPS-007,A0|pool size=100 baseline; alert at wait>50ms; scaling procedure DCM; audit-log partition storage 12-month estimate included (per OQ-OBS-CAPACITY); read-replica routing for audit queries|M|P0|
|123|OPS-006|Capacity: Redis memory|Capacity plan for Redis: 1GB baseline for ~100K refresh tokens; scale to 2GB at >70% util.|Ops|OPS-007|memory=1GB baseline; monitoring shows util %; scale playbook to 2GB DCM; worst-case projection (500K tokens ≈ 250MB per OQ-PRD-2 cap=5 analysis) headroom confirmed|S|P0|
|124|OPS-008|Alerts in production|Promote staging alerts (OBS-007/008/009 + ORT) to production; tune against first 24h baseline; RLL triggers remain in human-confirmed mode for first 30 days per M4 operational-maturity gate.|Ops|OBS-007,OBS-008,OBS-009,OPS-008-prep,ORT|alert rules deployed to prod; first-24h false-positive rate <10%; RLL-trigger dry-run in prod-shadow mode; on-call receives test page; human-gate flag set; auto-fire enabled on GA+30d|S|P0|
|125|FLAG-REMOVAL|Feature flag cleanup|Schedule `ANL` removal immediately post-GA; `ATR` at GA+2w per TDD §19.2.|Release|MIG-003|`ANL` PR merged removing flag and all gating checks; `ATR` removal PR drafted with GA+2w merge date; TDD §19.2 updated with actual removal dates|S|P0|
|126|RELEASE-CHECKLIST|Final release checklist|Execute TDD §24.2 release checklist; capture sign-offs from test-lead + eng-manager.|Release|ALL M1..M4|all TDD §24.2 items ticked (staging deploy smoke, LoginPage/RE3 functional, THP refresh VRF with 15-min token, flags configured, runbooks PBL, dashboards VRF, RLL tested, migration script validated, admin lock/unlock NDP exercised, /v1/health returning green); go/no-go sign-off recorded|M|P0|
|127|POST-GA-REVIEW|Post-GA review + metric audit|Week after GA: review PRD success metrics, flag gaps, schedule follow-on work.|Release|MIG-003|review held 2026-06-16 (GA+7d); metrics audited: RE1 conversion (target >60%), login p95 (<200ms), avg session duration (>30min), failed login rate (<5%), PA1 reset completion (>80%); follow-on backlog items created for any miss|S|P1|
|128|LEGACY-DEPRECATION|Legacy auth EN1 deprecation|Return 410 Gone with Sunset header on legacy auth NDP; publish migration notice per OQ-GOV-001 90-day policy.|APIGateway|MIG-003|legacy /auth/* routes return 410 with Sunset: 2026-09-07 (GA+90d per OQ-GOV-001); deprecation notice posted to internal engineering channel; external-API consumer email sent|S|P1|
|129|V1.1-BACKLOG|V1.1 deferred-scope backlog|Capture OQ-001 (API-key auth), OQ-JTBD-4 (service-accounts), OQ-REMEMBER-ME, OQ-CONSENT-WITHDRAWAL, OQ-DSAR-EXPORT, MFA (NG-002), RBAC (NG-003), OAuth (NG-001), refresh-token-cap tuning (OQ-PRD-2 review) as v1.1 tickets.|Meta|ALL OQs|9 v1.1 tickets created with links back to originating OQ/NG IDs; prioritization review scheduled|S|P1|

### NTG Points — M5

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|Traffic-split controller|Dispatch table|MIG-002|M5|`ANL` percentage rollout|
|Deprecation middleware|Middleware chain|LEGACY-DEPRECATION|M5|Legacy /auth/* routes; extensible for future deprecations; binds OQ-GOV-001 90-day policy|
|On-call schedule|Dispatch table|OPS-003|M5|PagerDuty; Grafana annotation; alert routing|
|HPA controller|Strategy pattern|OPS-004|M5|`THS` pod scaling|
|Flag-removal automation|Callback registry|FLAG-REMOVAL|M5|CI/CD post-GA scheduled jobs|
|Rollback human-gate flag|Configuration toggle|OPS-008|M5|ORT auto-fire enablement at GA+30d|

### Milestone Dependencies — M5

- M4 CMP + security sign-offs captured.
- M4 RLL triggers live in human-confirmed mode (auto-fire gated by OPS-008 30-day burn-in).
- M3 `ATR` enablement validated at 10% in MIG-002.
- M4 admin lock/unlock NDP (API-009/010) and /v1/health (API-011) exercised in RELEASE-CHECKLIST.
- External: PagerDuty seat allocation for auth-team; legacy-API consumer list from product; OQ-GOV-001 deprecation policy communicated.

### Risk Assessment and Mitigation — M5

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Phase 2 beta latency regression under 10% real traffic|High|Medium|Rollback + M5 overrun past 2026-06-09 GA|Staged ramp 1%→5%→10% over week 1; automated RLL triggers wired in human-confirmed mode (ORT); mitigation buffer=3 days in M5 schedule|PT|
|2|Migration from legacy auth causes data loss (R-003)|Low|High|User accounts corrupted|Parallel run Phase 1-2; idempotent upsert in DATA-MIG-SCRIPT; full DB backup pre-rollout; RLL restores from backup|PT|
|3|On-call RTT undermanned in post-GA 2-week intensive window|Medium|Medium|P1 SLA breach; incident response degraded|Rotation confirmed week -1 of M5; backup on-call identified; tooling access pre-provisioned|eng-manager|
|4|CO1 audit retrospective finds gap|Medium|Low|Remediation post-GA; SOC2 risk|CO1 sign-off obtained in M4; audit-log sample reviewed; remediation backlog empty at M5 entry|CMP|
|5|Human-confirmed RLL gate causes delayed auto-RLL during week-1 spike|Medium|Low|Incident MTTR extends past 2-min SLO|30-day human gate is per merge constraint; on-call paging SLA 15min ensures human available; OPS-008 dashboard shows RLL-pending state; auto-fire promotion at GA+30d per OPS-008|PT|

## Resource Requirements and Dependencies

### External Dependencies

|Dependency|Version|Purpose|Criticality|Milestone Introduced|Notes|
|---|---|---|---|---|---|
|PST|15+|SRP + audit_log + PA2 storage|Blocker|M1 (DEP-001)|Provisioned via DEP-002; testcontainers pin for CI; DM-003/DM-004 schemas land at M1|
|Redis|7+|Refresh-token store with TTL (cap=5 per user per OQ-PRD-2); rate-limit counters|Blocker|M1 (DEP-003)|EXPIRE-based TTL; AOF persistence for durability; sizing bounded by cap=5 OE policy|
|Node.js|20 LTS|Runtime for backend services|Blocker|M1 (DEP-004)|Pinned in Dockerfile + CI image|
|bcryptjs|^2.4.3|Password hashing (cost=12)|Blocker|M1 (DEP-005)|Wrapped by `PSS` (COMP-005)|
|jsonwebtoken|^9.0.0|JWT sign/verify (RS256)|Blocker|M1 (DEP-006)|Wrapped by `JWT` (COMP-007b)|
|SendGrid|2024 API|Transactional email (reset, verify)|Enhancement|M3 (DEP-007)|Retry/backoff via ASYNC-QUEUE; template-abstracted (DECOMP-EMAIL-TEMPLATE)|
|React Router|^6|Frontend routing for auth pages|Enhancement|M3 (INFRA-003)|THP consumed by LoginPage/RE3/ProfilePage; RE3→LoginPage redirect per CONFLICT-2|
|Prometheus|2.x|Metrics scrape target|Enhancement|M4 (OBS-001)|`/metrics` EN1 on THS; separate from `/v1/health` (API-011)|
|OpenTelemetry Collector|0.x|Trace aggregation|Enhancement|M4 (OBS-002)|OTLP → Jaeger backend|
|PagerDuty|SaaS|Alert routing + on-call; RLL-trigger human-confirmation SMS/page|Enhancement|M4/M5 (OBS-007, ORT, OPS-003)|auth-team escalation policy; human-gate IN1 for first 30 days post-GA|

### Infrastructure Requirements

- **Staging environment**: 2× backend pods, 1× PST primary + 1× replica, 1× Redis; dedicated for M3-M4 IN1/load testing (ref: DEP-002, INFRA-001).
- **Production environment**: 4× backend pods (HPA target CPU 60%), PST primary + standby + PITR backups, Redis Sentinel (3-node), CloudFront/ALB in front of Express app (ref: OPS-004, DEP-002).
- **Observability stack**: Prometheus (15-day RTN), Grafana (dashboards for auth KPIs), Jaeger (7-day trace RTN), centralised logging with 12-month audit-log RTN per OQ-CONFLICT-1 RSL (ref: OBS-001..008, A0, DM-003).
- **Secret management**: RSA signing keys and bcrypt pepper stored in KMS/Vault; RTT runbook in RSA-KEY-ROTATION (M3); SOC2 key-RTT control owned by security-team.
- **CI/CD**: GitHub Actions runners with coverage gate ≥85% (COVERAGE-GATE, M4), testcontainers permissions (privileged runners for Docker-in-Docker), k6 load runners (NFR-PERF-001-M3, LOAD-TEST-FULL).
- **Headcount**: 3 backend engineers, 2 frontend engineers, 1 SRE, 0.5 security-team, 0.25 CMP reviewer, 0.25 tech-writer across 11-week duration (ref: Effort totals per milestone).

## Risk Register

|ID|Risk|Affected Milestones|Category|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|---|---|
|R-001|Load-test tooling not yet procured before M3 NFR-PERF-001-M3 deadline|M1, M3|Operational|High|Medium|Latency budgets unvalidated pre-M4 → LOAD-TEST-FULL slips|Pre-M1 procurement ticket filed in M1; k6-cluster provisioned in DEP-002; fallback: artillery (open-source) pre-validated in M1 spike|sre-team|
|R-002|SSO requirement (Q-6) surfaces during M3-M4 blocking scope lock|M1, M3|Scope|High|Low|Re-plan to add OIDC provider; GA slip 2-4 weeks|ADR-SSO-DEFERRAL DCM in M1; product confirms no SSO for v1 by M1 exit; V1.1-BACKLOG (NG-001) captures deferral|product-eng|
|R-003|Migration from legacy auth causes user-account data loss|M3, M5|Technical|High|Medium|Users locked out; revenue loss ≥$100K/day|DATA-MIG-SCRIPT dry-run in staging (M4); idempotent upsert; full DB backup pre-rollout; MIG-002 phased 10%→50%→100%; RLL restores from backup|PT|
|R-004|CO1 audit discovers 12-month RTN MPL gap|M1, M4, M5|CO1|High|Low|SOC2 certification delayed; remediation post-GA|OQ-CONFLICT-1 closed 12 months in M1; NC0 validates RTN in M4; DM-003/A0 schema enforces non-deletable rows; CMP sign-off gate at M4 exit|CMP|
|R-005|Bcrypt cost=12 latency budget breach under peak load|M2, M4|Performance|Medium|Medium|p95 login > 200ms SLA; WAL for NFR-PERF-001|PERF-BASELINE in M2 measures bcrypt cost; calibration check at M3 load test; cost reduction to 11 is reversible contingency with CMP review|backend-team|
|R-006|RSA key-RTT runbook untested when first RTT due|M3, M5|Operational|Medium|Medium|Key-RTT incident causes unplanned downtime|RSA-KEY-ROTATION drill in M3 on staging; JWKS EN1 supports multi-key verify; runbook reviewed by security-team|security-team|
|R-007|SendGrid outage blocks PA1-reset flow|M3|External|Medium|Medium|Reset emails delayed > SLA; CS tickets surge|ASYNC-QUEUE with retry/backoff (M3); secondary ESP evaluated for V1.1 (not in scope); runbook OPS-002 documents manual-send fallback|PT|
|R-008|CAPTCHA provider IN1 delays M3 login flow|M3|External|Medium|Medium|M3 scope slip; M4 hardening compresses|CAPTCHA-INTEG spike in M3 week 1; feature-flagged so login can ship without CAPTCHA to staging; go/no-go at M3 mid-point|backend-team|
|R-009|Observability capacity planning under-provisioned (OQ-OBS-CAPACITY)|M1, M4|Operational|Medium|Medium|Metrics scrape failures; blind-spot incidents|OQ-OBS-CAPACITY resolved in M1 with SRE input; OBS-001..008 include capacity sizing; monitoring of monitoring in OBS-009|sre-team|
|R-010|Frontend clock skew causes premature token expiry|M3|Technical|Low|High|Users auto-logged-out mid-session; support tickets|FE-CLOCK-SKEW (M3) implements ±30s tolerance and NTP sync detection; E2E covers clock-drift simulation in TEST-E2E-RESET|frontend-team|
|R-011|Legacy `/auth/*` consumer not deprecated by 2026-09-07 cutoff (OQ-GOV-001 90-day Sunset)|M5|Organizational|Medium|Medium|Legacy maintenance burden; CMP scope creep|LEGACY-DEPRECATION ships 410 + Sunset header in M5; POST-GA-REVIEW tracks weekly migration; escalation to eng-leadership if < 50% migrated by GA+8 weeks; OQ-GOV-001 policy bounds exception requests|eng-manager|
|R-012|Pen-test window (OQ-PEN-TEST-WINDOW) not confirmed before M4|M4|CO1|Medium|Low|SOC2 evidence gap; M4 exit gate blocked|OQ-PEN-TEST-WINDOW escalated at M3 mid-point; budget pre-approved; vendor shortlist captured in M1|security-team|
|R-013|Coverage gate (≥85%) blocks M4 exit due to IN1-test flakiness|M4|Quality|Medium|Medium|M4 slip 3-5 days|COVERAGE-GATE introduced in M4 with 1-week burn-in; flaky-test quarantine process; deterministic test-data factories in M2-M3|qa-team|
|R-014|DSAR export (OQ-DSAR-EXPORT) rules unresolved at M4 exit|M4|CO1|Low|Medium|Post-GA remediation for GDPR DSAR|OQ-DSAR-EXPORT targeted to close in M4; default answer: export JSON bundle per SRP + audit_log subset; CMP sign-off|CMP|
|R-015|Consent-withdrawal propagation (OQ-CONSENT-WITHDRAWAL) design gap|M4|CO1|Low|Medium|GDPR right-to-withdraw partially implemented|OQ-CONSENT-WITHDRAWAL closed in M4 with propagation-within-24h SLA; MPL in V1.1 if complexity > 5d|CMP|
|R-016|Post-GA on-call RTT undermanned (2-week intensive window)|M5|Operational|Medium|Medium|P1 SLA breach; incident response degraded|Rotation confirmed week -1 of M5; backup on-call identified; tooling access pre-provisioned; OPS-001/002 runbook library|eng-manager|
|R-017|Admin audit/lock/unlock APIs (ADMIN-001, API-009, API-010) expose PII beyond CMP scope|M3, M4|Security|Medium|Low|Data-leak audit finding|Admin NDP restricted to CMP-team RBAC role; field-level redaction on ip_addr, user_agent when out of RTN window; audit-of-audit-access logged via AES (COMP-018)|security-team|
|R-018|Rate-limit thresholds (login 10/min) too aggressive for legit bursty users|M2, M4|Product|Low|Medium|User friction; CS tickets|Thresholds set per TDD NFR-SEC-003; monitored via OBS-003; adjustment runbook; A/B test planned for V1.1|product-eng|
|R-019|OQ-OQ-002 concurrent-session cap (5 per OQ-PRD-2 OE) insufficient for power users|M3|Product|Low|Medium|Power-user complaints; support tickets|OQ-PRD-2 cap=5 confirmed in M3 as reversible default; telemetry (C0 AC) captures eviction frequency for V1.1 calibration; cap adjustable via config|product-eng|
|R-020|Feature flag (ANL, ATR) removal (M5) leaves dead code paths|M5|Technical|Low|Low|Tech-debt accumulation|FLAG-REMOVAL automates removal via codemod script; tracked in post-GA review; CI check for stale flags|backend-team|

## Success Criteria and Validation Approach

|#|Success Criterion|Source|Metric|Target|Validation Method|Milestone Landing Slot|
|---|---|---|---|---|---|---|
|1|Registration completion rate|PRD goal|Registration start → completion %|≥ 75%|Funnel analytics dashboard; A/B vs legacy|M5 (POST-GA-REVIEW)|
|2|Login success rate (valid creds)|PRD goal|Successful logins / total login attempts with valid creds|≥ 99.5%|OBS-003 metric; NFR-REL-001 SLA|M4 (NFR-REL-001) → M5 telemetry|
|3|Password-reset completion rate|PRD goal|Reset request → successful PA1 change %|≥ 85%|Funnel analytics + SendGrid delivery metric|M5 (POST-GA-REVIEW)|
|4|Authentication latency p95|TDD NFR-PERF-001|p95 `/auth/login` + `/auth/refresh` response time|< 200ms|k6 load test (NFR-PERF-001-M3) + Prom histogram (OBS-003)|M3 (NFR-PERF-001-M3), re-validated M4|
|5|Throughput capacity|TDD NFR-PERF-002|Sustained req/s on `/auth/*`|≥ 1000 RPS|Load test in LOAD-TEST-FULL (M4); Horizontal scaling VRF in OPS-004|M4 (LOAD-TEST-FULL)|
|6|Service availability|TDD NFR-REL-001|Monthly uptime of auth NDP|≥ 99.9%|SLI/SLO dashboard; error budget tracking; `/v1/health` (API-011) liveness probe|M5 (post-GA telemetry) — design validated M4|
|7|Zero PII leakage in logs|TDD NFR-SEC-001|# of PII matches in log grep audit|0|SEC-LOGGING-M2 automated scanner; SEC-AUDIT-TOKEN review|M2 (SEC-LOGGING-M2), re-audited M4|
|8|OWASP Top 10 CMP|TDD NFR-SEC-002|# of High/Critical findings in pen-test + SAST|0|SAST in CI (M1 INFRA-002); pen-test window (M4 OQ-PEN-TEST-WINDOW)|M4 (SEC-005)|
|9|Brute-force resistance|TDD NFR-SEC-003|Rate-limit trigger on 11th login attempt/min|100% blocked|SEC-003 unit tests + SEC-006 burn-in test|M2 (SEC-003), hardened M4 (SEC-006)|
|10|GDPR CMP — consent capture|TDD NFR-COMP-001|Consent flag stored for every RE1|100%|DB constraint NOT NULL on consent column (M1 DM-002); NFR-COMP-001-stub M2; NFR-COMP-001 M4|M4 (NFR-COMP-001)|
|11|SOC2 audit-log completeness|TDD NC0|% of auth events persisted to audit_log (DM-003 schema)|100% (sample audit)|AUDIT-003 replay test; CMP sample review; AES (COMP-018) emits admin events|M4 (NC0)|
|12|Audit-log RTN enforcement|PRD requirement (OQ-CONFLICT-1 closed 12 months)|Retention policy job executes; rows beyond 12 months archived|100% execution ≥ monthly|OPS-005 RTN job; NC0 includes RTN assertion|M4 (NC0), run M5 (OPS-005)|
|13|NIST SP 800-63B PA1 conformance|TDD NFR-COMP-003|Password acceptance matches NIST ruleset|100% (ruleset test suite)|NFR-COMP-003 test vector; TEST-WEAK-PWD|M2 (NFR-COMP-003)|
|14|JWT expiry enforcement|TDD spec|Access token RJC > 15min; refresh > 7d; refresh-cap=5 enforced|100%|TOKEN-STUB unit tests (M2); TEST-REVOKE IN1 (M3); C0 AC asserts cap eviction|M2 (TOKEN-STUB), validated M3|
|15|Rate-limit enforcement — all NDP|TDD NFR-SEC-003|Thresholds configured per EN1 and verifiable|100% NDP covered|SEC-003 config tests + OBS-003 dashboards|M2 (SEC-003), observability M4|
|16|Feature flag RLL works|TDD rollout strategy|Time-to-disable from alarm to zero traffic|< 2 min (auto after GA+30d; human-confirmed during burn-in)|ORT drill in M4; MIG-002 phased rollout; OPS-008 promotion to auto-fire|M4 (ORT) → M5 (MIG-002)|
|17|GA entry gate passed|TDD milestone M4|Load + security + CMP sign-offs collected|3/3 sign-offs|RELIABILITY-READINESS review (M4) + RELEASE-CHECKLIST (M5)|M4 (RELIABILITY-READINESS), formalised M5 (RELEASE-CHECKLIST)|

## Decision Summary

<!-- Every row cites the specific data point that drove the decision — no subjective justifications. -->

|Decision|Chosen|Alternatives Considered|Rationale|
|---|---|---|---|
|ADR-001 Token strategy|JWT RS256 2048-bit + Redis refresh store|Server-side session cookies (RJC: sticky-session hampers HPA in OPS-004); Paseto (RJC: limited Node.js tooling at 2026-04)|NFR-PERF-002 ≥1000 RPS requires stateless auth; public-key verify avoids shared secret; 15-min access TTL + Redis refresh revocation (COMP-007a, SEC-001) mitigates non-trivial revocation. Lands M1 (RBAC-DECISION) → M2 (TOKEN-STUB) → M3 (SEC-001)|
|ADR-002 Password hash cost|bcrypt cost=12|Argon2id (RJC: inconsistent Node.js 20 ecosystem at 2026-04); bcrypt cost=10 (RJC: insufficient margin for GPU attack by 2028); cost=14 (RJC: NFR-PERF-001 p95<200ms budget breach in PERF-BASELINE)|NIST SP 800-63B guidance; PERF-BASELINE (M2) measures ≈250ms/hash within p95 budget; R-005 contingency to cost=11 DCM with CMP review. Lands M1 (COMP-005 skeleton) → M2 (COMP-005 full) + PERF-BASELINE|
|ADR-003 Persistence topology|PST durable (SRP, audit_log, DM-003, DM-004) + Redis ephemeral (refresh cap=5, rate-limit counters, PA1-reset codes)|Single Postgres with partitioned tokens (RJC: TTL cron race-prone); DynamoDB (RJC: multi-cloud outside v1)|NC0 requires 12-mo queryable audit (RDBMS fit); refresh high-throughput + TTL (Redis fit); dual-store consistency mitigated by Redis-SSOT for revocation. Lands M1 (DM-001..004, DEP-001/003) → M3 (SEC-001)|
|ADR-004 Milestone phasing|Technical layers (Foundation → Core → NTG → Hardening → Production) not feature vertical slices|Feature-vertical slices (RJC: 20% observability/audit duplication overhead); agile epic-per-feature (RJC: incompatible with GA 2026-06-09 phased rollout)|complexity_class=HIGH + cross-cutting NFRs benefit from horizontal consolidation (OBS-001..009 single-land M4); TDD M1-M4 already layered. Mitigated by flag-gated dark-launch (`ANL`, `ATR`)|
|ADR-005 Rollout mechanism|Phased `ANL` + `ATR` flags; ramp 10% → 50% → 100% (MIG-002/003)|Big-bang cutover (RJC: no RLL without downtime); blue/green (RJC: 100% duplicate-stack cost unjustified v1)|Success Criterion 16 (<2min RLL) requires ORT; R-001 (load regression) + R-003 (data loss) blast-radius minimised; FLAG-REMOVAL (M5) mitigates flag-debt; human-confirmation gate for first 30d post-GA per merge constraint|
|ADR-006 Audit-log retention|12-month RTN (OQ-CONFLICT-1 RSL; PRD precedence over TDD 90-day draft)|90 days (TDD draft; RJC: CMP conflict); 7 years (RJC: PII residency over-RTN)|SOC2 Type II evidence windows typically require 12 months; DM-001/003 capacity sizing within budget; A0 column compression + archival tier after 6 months. Lands M1 (OQ closed) → M4 (A0, NC0) → M5 (OPS-005 RTN job)|
|ADR-007 Admin response-path scope|Ship ADMIN-001 (query) + API-009/010 (lock/unlock) + AES/ALM (COMP-018/019) in M4|Query-only scope (RJC: Jordan persona incident response gap per debate Round 2 concession); full admin console (RJC: scope explosion, defer to V1.1)|PRD S7 Jordan persona requires incident-response capability; B-variant CONFLICT-2 / C8 scoring (92 vs 80) drove admin-EN1 graft; AES service-layer abstraction (COMP-018) enables lock/unlock without duplicating admin auth wiring. Lands M3 (ADMIN-001) → M4 (COMP-018/019, API-009/010)|
|ADR-008 Refresh-token bound|cap=5 per user with OE (OQ-PRD-2 RSL)|Unlimited + metric (RJC: open-ended Redis sizing per debate); cap=3 (RJC: power-user friction, R-019)|Bounds Redis sizing deterministically (500K tokens ≈ 250MB per OPS-006); reversible default; telemetry via C0 AC enables V1.1 calibration. Lands M3 (C0 AC) + OQ-PRD-2 closed in M3|
|ADR-009 API deprecation policy|90-day Sunset header + one active major (OQ-GOV-001 RSL)|Indefinite maintenance (RJC: unbounded legacy burden, R-011); 30-day Sunset (RJC: insufficient consumer-migration window)|Binds API-VER-001 policy; caps LEGACY-DEPRECATION exception scope; external-consumer-facing commitment per Jordan/Sam persona. Lands M1 (API-VER-001) → M5 (LEGACY-DEPRECATION Sunset: 2026-09-07)|
|ADR-010 CONFLICT-2 post-register UX|RE3 redirects to /login?email=... per TDD §8.2 contract; v1.1 product review for auto-login option|Auto-login after RE1 (RJC: TDD §8.2 contract violation; deferred to v1.1); no redirect (RJC: PRD user-flow gap)|B-variant C9 scoring (95 vs 75) drove explicit conflict-RSL note; COMP-001/002 AC wires redirect; logged for v1.1 product review as reversible UX decision. Lands M3 (COMP-001, COMP-002)|

## Timeline Estimates

|MLS|Duration|Start|End|Key Milestones|
|---|---|---|---|---|
|M1 Foundation|2 weeks (18 pd)|2026-03-30|2026-04-10|DM-001..004 schemas migrated to staging; 3/4 M1 OQs closed; infra procurement confirmed; TDD M1 (Project Setup) by 2026-04-14|
|M2 Core Logic|2 weeks (22 pd)|2026-04-13|2026-04-24|Register + login green on staging; PERF-BASELINE report; zero PII in logs; TOKEN-STUB contingency wired; TDD M1–M2 (Core Auth) by 2026-04-28|
|M3 NTG|3 weeks (27 pd)|2026-04-27|2026-05-15|All FRs green E2E; NFR-PERF-001 p95 < 200ms on staging; rate-limit + CAPTCHA VRF; refresh cap=5 enforced; CONFLICT-2 redirect live; TDD M2–M3 (Password Reset) by 2026-05-12|
|M4 Hardening|2 weeks (21 pd)|2026-05-18|2026-05-29|SOC2 audit sample pass; LOAD-TEST-FULL 1000 RPS pass; pen-test High/Critical = 0; admin lock/unlock + /v1/health live; RLL triggers in human-gated mode; TDD M4 (Security & CO1) by 2026-05-26|
|M5 Production Readiness|2 weeks (11 pd)|2026-06-01|2026-06-12|10%→100% ramp complete; on-call RTT staffed; post-GA review scheduled; RLL auto-fire armed at GA+30d; legacy Sunset 2026-09-07; TDD M5 (Production Deployment) by 2026-06-09|

**Total estimated duration:** 11 calendar weeks (99 person-days) — 2026-03-30 through 2026-06-12

### Timeline Notes

- **GA target**: 2026-06-09 (per TDD milestone commitment). M5 end extends to 2026-06-12 to absorb phased-rollout ramp buffer (R-001 mitigation).
- **Total effort**: 99 person-days across 11 calendar weeks, consistent with Team Size: 3 backend + 2 frontend + 1 SRE + partial security/CMP/tech-writer allocation.
- **Schedule compression**: Milestones overlap at boundary days (M1→M2 kickoff 2026-04-13 while M1 sign-off tails 2026-04-10; M3→M4 kickoff 2026-05-18 while M3 stabilisation tails). No-overlap on M4→M5 boundary (CMP gate must close before rollout).
- **Buffer**: 3 days M5 buffer for rollout abort/resume; no global slack. Any slip > 3 days on M3 critical path (FRT refresh) escalates to replanning GA date.
- **Dependencies on external teams**: pen-test window (M4, R-012 open), CAPTCHA vendor access (M3, R-008), PagerDuty seat provisioning (M4-M5), SendGrid production quota (M3), OQ-GOV-001 external-consumer communication (M5).
- **Week-by-week**: W1-W2 M1, W3-W4 M2, W5-W7 M3, W8-W9 M4, W10-W11 M5.
- **Post-GA auto-fire promotion**: 2026-07-09 (GA+30d) — RLL triggers (ORT) transition from human-confirmed to automated per OPS-008; no new deliverables, configuration flag flip only.
