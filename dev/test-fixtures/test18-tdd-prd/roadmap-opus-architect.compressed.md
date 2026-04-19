---
spec_source: "test-tdd-user-auth.compressed.md"
complexity_score: 0.72
complexity_class: HIGH
primary_persona: architect
adversarial: false
base_variant: "none"
variant_scores: "none"
convergence_score: none
---

# User Authentication Service — Project Roadmap

## Executive Summary

The User Authentication Service is the foundational identity layer for the platform, unblocking Q2-Q3 2026 personalization (projected $2.4M ARR impact), SOC2 Type II audit readiness by Q3 2026, and self-service account recovery. The roadmap phases delivery across six architecturally layered milestones: foundation and data layer, core authentication flows, token management, profile and password reset, security/compliance/observability, and migration/rollout/GA.

**Business Impact:** Enables entire personalization roadmap (FR-AUTH.1-5), satisfies SOC2 audit logging gate, reduces 30% QoQ growth in access-issue support tickets via self-service password reset, and ships competitive table-stakes (25% of churn cites lack of accounts).

**Complexity:** HIGH (0.72) — multi-component orchestration across AuthService/TokenManager/JwtService/PasswordHasher, dual feature-flagged phased rollout, cross-team frontend/backend/platform dependencies, SOC2/GDPR/NIST compliance obligations, and high-blast-radius migration with legacy parallel run.

**Critical path:** DM-001/DM-002 data contracts → COMP-007 PasswordHasher + COMP-008 JwtService primitives → COMP-005 AuthService orchestrator → FR-AUTH-001/002 login+registration → FR-AUTH-003 token refresh + COMP-004 AuthProvider silent refresh → FR-AUTH-004/005 profile+reset → NFR-COMPLIANCE-001/002/003 gates → MIG-001/002/003 phased rollout to GA.

**Key architectural decisions:**

- JWT stateless sessions with RS256 2048-bit RSA (AC-001) over HS256 or server-side sessions — chosen for scale (NFR-PERF-002 500 concurrent), quarterly key rotation (AC-009), and OAuth2 Bearer compatibility (AC-P-003 Sam).
- bcrypt cost 12 via `PasswordHasher` abstraction (AC-002, NFR-SEC-001) over argon2id — chosen for NIST SP 800-63B compliance, mature Node.js library support, and < 500ms hash target (SC-005).
- Redis 7+ opaque refresh token storage with 7-day TTL (AC-004) over JWT refresh tokens — chosen to enable revocation on logout/rotation (R-001 mitigation) and bound Redis working set (OPS-004: 1 GB for ~100K tokens).

**Open risks requiring resolution before M1:**

- OQ-002 maximum `UserProfile.roles` array length blocks DM-001 schema finalization (auth-team, target 2026-04-01).
- OQ-005 account lockout thresholds (N attempts/window) blocks FR-AUTH-001 AC.4 implementation; TDD proposes 5/15min but PRD requires security sign-off (Security, target pre-M2).
- OQ-007 Jordan admin audit log UI scope (PRD JTBD without FR coverage) — must be resolved before M5 to size audit log schema (product-team, target pre-M5).

## Milestone Summary

|ID|Title|Type|Priority|Effort|Dependencies|Deliverables|Risk|
|----|-------|------|----------|--------|--------------|--------------|------|
|M1|Foundation & Data Layer|Infrastructure|P0|2w|INFRA-DB-001, SEC-POLICY-001|17|Medium|
|M2|Core Authentication Flows|Feature|P0|3w|M1|18|High|
|M3|Token Management & Session|Feature|P0|2w|M2|14|High|
|M4|Profile & Password Reset|Feature|P0|2w|M2, M3, SendGrid|14|Medium|
|M5|Security, Compliance & Observability|Cross-cutting|P0|2w|M2, M3, M4|16|High|
|M6|Migration, Rollout & GA|Release|P0|3w|M1-M5|16|High|

## Dependency Graph

```
INFRA-DB-001 ──┐
SEC-POLICY-001 ├──> M1 (Foundation) ──> M2 (Core Auth) ──┬──> M3 (Tokens) ──┐
AUTH-PRD-001 ──┘                                          │                  ├──> M5 (Security/Compliance) ──> M6 (Rollout/GA)
                                                          └──> M4 (Profile/Reset) ┘
                                                                   │
                                                              SendGrid (external)

Cross-cutting:
- R-001..R-006 risks span M2-M6
- NFR-PERF-001/002 validated in M6 load tests
- NFR-COMPLIANCE-001/002/003 implemented in M5, audited in M6
- AC-010 feature flags wired in M2-M3, retired in M6
```

## M1: Foundation & Data Layer (Weeks 1-2)

**Objective:** Provision Postgres/Redis/K8s infrastructure, define DM-001/DM-002 data contracts, scaffold COMP-005 AuthService + COMP-006 TokenManager with primitive modules (PasswordHasher, JwtService, UserRepo), and anchor cross-cutting architectural constraints (AC-001..008, AC-P-001/003). | **Duration:** 2 weeks | **Entry:** INFRA-DB-001 provisioned, SEC-POLICY-001 published, OQ-002 resolved. | **Exit:** Postgres schema deployed to staging; Redis cluster reachable; AuthService container builds green; DM-001 + DM-002 contracts reviewed and frozen; all primitives unit-tested.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|AC-003|Provision PostgreSQL 15+|Deploy managed Postgres instance with 100-conn pool, backup policy, read replica.|Infra|INFRA-DB-001|PG15+ reachable from staging AuthService; conn pool=100; backup every 6h; replica lag<5s|M|P0|
|2|AC-004|Provision Redis 7+|Deploy Redis 7 with 1 GB memory, persistence disabled (ephemeral), TLS auth.|Infra|INFRA-DB-001|Redis7 reachable; 1GB mem; TLS required; auth token present; P99 GET<5ms|M|P0|
|3|AC-005|Node.js 20 LTS runtime container|Build base container image pinned to Node 20 LTS with security patches.|Infra|-|Image built; node-v20.x.x; no high-sev CVEs; passes trivy scan|S|P0|
|4|AC-007|TLS 1.3 termination|Configure ingress with TLS 1.3 minimum, HSTS, modern cipher suite.|Infra|AC-005|TLS1.3 enforced; HSTS 6mo; A+ on SSLLabs; no TLS1.1/1.0 accepted|S|P0|
|5|AC-008|CORS allowlist configuration|Restrict CORS to known frontend origins via env-driven allowlist.|Infra|AC-005|CORS_ALLOWED_ORIGINS env var; wildcard rejected; preflight 204; unknown origin 403|S|P0|
|6|AC-006|URL-prefix API versioning|Wire `/v1/auth/*` route prefix into router; enforce version header passthrough.|COMP-005|AC-005|All auth routes under /v1; unversioned requests 404; additive fields permitted in-version|S|P0|
|7|DM-001|UserProfile schema & migration|Define Postgres table users with fields id:UUID-PK; email:varchar unique-idx lowercase-normalized; display_name:varchar(2-100) not-null; password_hash:varchar not-null; created_at:timestamptz not-null default-now; updated_at:timestamptz not-null auto; last_login_at:timestamptz nullable; roles:text[] not-null default-'{user}'.|DB|AC-003, OQ-002|Fields id:UUID-PK; email:unique-idx; display_name:varchar; password_hash:varchar; created_at:timestamptz; updated_at:timestamptz; last_login_at:timestamptz-nullable; roles:text[]; migration applies forward+backward; unique index on email enforced|M|P0|
|8|DM-002|AuthToken TypeScript interface|Define return-shape contract fields accessToken:JWT-string not-null RS256-signed; refreshToken:opaque-string not-null unique Redis-hashed 7d-TTL; expiresIn:number not-null 900; tokenType:string not-null "Bearer".|COMP-005|-|Fields accessToken:JWT-string; refreshToken:opaque-string; expiresIn:number=900; tokenType:string="Bearer"; TS interface exported; json-schema generated|S|P0|
|9|COMP-005|AuthService skeleton|Scaffold backend orchestrator/facade with route bindings, DI container, error envelope, audit hooks (no business logic yet).|COMP-005|AC-005, AC-006|/v1/auth/* routes return 501 stub; DI container resolves PasswordHasher+TokenManager+UserRepo; error envelope {error:{code,message,status}}; trace context propagated|M|P0|
|10|COMP-006|TokenManager skeleton|Scaffold token issuance/validation module with Redis client injection, metric hooks.|COMP-005|AC-004, COMP-008|TokenManager.issueTokens/validateRefresh/revoke signatures; Redis client injected; auth_token_* metrics registered; 100% null impl unit tests|S|P0|
|11|COMP-007|PasswordHasher primitive|Implement bcrypt wrapper with cost factor 12, timing-safe verify, error taxonomy.|COMP-005|AC-002|PasswordHasher.hash()/verify() impl; bcrypt cost=12 constant; timing-safe verify; unit test asserts cost param; hash<500ms (SC-005)|S|P0|
|12|COMP-008|JwtService primitive|Implement RS256 sign/verify with 2048-bit RSA key loading, kid claim, clock skew tolerance.|COMP-005|AC-001|JwtService.sign()/verify() impl; RS256 enforced; 2048-bit key validated at startup; kid claim present; 60s clock skew|S|P0|
|13|COMP-009|UserRepo data access|Implement Postgres repository for UserProfile CRUD with parameterized queries, tx support.|COMP-005|DM-001|UserRepo.findByEmail/create/update/touchLastLogin impl; parameterized only; tx wrapper; unique-violation mapped to domain error|M|P0|
|14|AC-001|JWT RS256 2048-bit key config|Load RSA keypair from secret store; validate modulus size; expose kid.|COMP-008|-|keypair loaded from secrets; modulus=2048; startup fails on<2048; kid rotatable via config|S|P0|
|15|AC-002|bcrypt cost 12 config enforcement|Pin bcrypt cost constant; unit test asserts; reject runtime override.|COMP-007|-|BCRYPT_COST=12 constant (no env override); unit test asserts cost param in hash; PR fails if constant changed|S|P0|
|16|AC-P-001|Alex (End User) design requirements|Document persona-driven constraints into frontend ADR: registration <60s; session persistence; self-service reset.|Docs|-|ADR doc created; <60s flow enumerated; session-persistence requirement cited in COMP-004 spec; reset flow cited in FR-AUTH-005|S|P1|
|17|AC-P-003|Sam (API Consumer) OAuth2 compat ADR|Document programmatic token refresh + Bearer tokenType + stable error codes contract.|Docs|DM-002|ADR doc created; Bearer tokenType enforced in DM-002; error codes table (AUTH_*); refresh flow specified|S|P1|

### Integration Points — M1

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|DI container (AuthService)|Registry|COMP-005 bootstrap wires PasswordHasher/TokenManager/JwtService/UserRepo|M1|COMP-005 and all M2-M5 handlers|
|Route registry (/v1/auth/*)|Dispatch table|COMP-005 router binds verb+path→handler|M1|API-001..007 in M2-M4|
|Middleware chain|Pipeline|AuthService bootstrap registers cors→tls→tracing→error-envelope|M1|all auth routes|
|Secret loader|Callback|JwtService startup hook loads RSA keypair|M1|COMP-008|
|Metric registry (Prometheus)|Registry|TokenManager/PasswordHasher register counters+histograms on bootstrap|M1|OPS-005 scraping|

### Milestone Dependencies — M1

- INFRA-DB-001 database infrastructure (hard block on AC-003, AC-004).
- SEC-POLICY-001 organizational password/token policy (hard block on AC-001, AC-002).
- AUTH-PRD-001 parent product requirements (defines scope for AC-P-001/003).
- OQ-002 resolution (blocks DM-001 schema freeze).

### Open Questions — M1

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-002|Maximum allowed `UserProfile.roles` array length?|Blocks DM-001 schema freeze and Postgres text[] constraint sizing; affects payload size in API-003|auth-team|2026-04-01|

### Risk Assessment and Mitigation — M1

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-003 Data loss during legacy→new migration|High|Low|High|Pre-phase backup automated; idempotent upsert tested in M1; rollback runbook drafted|platform-team|
|2|RSA key compromise at bootstrap|High|Low|High|Secrets manager integration; startup validation; monthly rotation dry-run in staging|security-team|
|3|Postgres schema change downtime|Medium|Medium|Medium|Migrations reviewed by DBA; zero-downtime patterns (add-nullable-then-backfill); tested on staging snapshot|auth-team|

## M2: Core Authentication Flows (Weeks 3-5)

**Objective:** Deliver FR-AUTH-001 (login) and FR-AUTH-002 (registration) end-to-end from `LoginPage`/`RegisterPage` through AuthService to Postgres, with bcrypt hashing, password policy enforcement, account lockout, per-IP rate limiting, and standardized error envelope. | **Duration:** 3 weeks | **Entry:** M1 exit criteria met; COMP-005..009 primitives green. | **Exit:** FR-AUTH-001 + FR-AUTH-002 integration tests pass against real Postgres; NFR-SEC-001 bcrypt-cost-12 asserted; TEST-001/002/004 ≥80% coverage on AuthService; LoginPage/RegisterPage render behind `AUTH_NEW_LOGIN=false` flag.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-AUTH-001|Login with email+password|Implement AuthService.login() invoking PasswordHasher.verify then TokenManager.issueTokens, returning AuthToken.|COMP-005|COMP-007, COMP-006, COMP-009|valid-creds→200+AuthToken; invalid-creds→401; nonexistent-email→401 (no enumeration); 5 fails/15min→423 locked|L|P0|
|2|FR-AUTH-002|Registration with validation|Implement AuthService.register() with email uniqueness check, password policy, PasswordHasher.hash, UserProfile insert.|COMP-005|COMP-007, COMP-009|valid-reg→201+UserProfile; duplicate-email→409; weak-password→400; bcrypt-cost-12 stored|L|P0|
|3|API-001|POST /auth/login endpoint|Wire login route with request schema validation, rate limit, error envelope.|COMP-005|FR-AUTH-001, AC-006, COMP-010|POST /v1/auth/login; body{email,password}; 200→AuthToken; 401/423/429 per spec; auth=none; rate=10/min/IP|M|P0|
|4|API-002|POST /auth/register endpoint|Wire register route with schema validation, rate limit.|COMP-005|FR-AUTH-002, AC-006, COMP-010|POST /v1/auth/register; body{email,password,displayName}; 201→UserProfile; 400/409 per spec; rate=5/min/IP|M|P0|
|5|API-007|POST /auth/logout endpoint|New endpoint to terminate session; revokes refresh token via TokenManager.revoke.|COMP-005|COMP-006|POST /v1/auth/logout; auth=Bearer; 204 on success; refresh-token revoked in Redis; idempotent|S|P0|
|6|NFR-SEC-001|bcrypt cost 12 enforcement|Unit+property test asserts bcrypt cost parameter inside stored hash; CI gate.|COMP-007|AC-002|unit-test asserts cost=12 parsed from hash; property test on 100 random pwds; CI fails if any hash has cost≠12|S|P0|
|7|COMP-001|LoginPage (frontend)|React route /login with email/password form; calls API-001; stores AuthToken via AuthProvider.|Frontend|COMP-004, API-001|props{onSuccess,redirectUrl?}; form fields email+password; success→AuthProvider.setToken→onSuccess; 401→inline error "Invalid email or password"; a11y keyboard/screen-reader|M|P0|
|8|COMP-002|RegisterPage (frontend)|React route /register with email/password/displayName form; client-side password-strength preview.|Frontend|COMP-004, API-002|props{onSuccess,termsUrl}; fields email+password+displayName; client strength meter (8+ chars, upper, number); 409→inline duplicate hint; 400→per-field errors|M|P0|
|9|COMP-004|AuthProvider (initial)|React context provider holding AuthToken in memory; 401 interceptor stub.|Frontend|DM-002|provides {token,setToken,clearToken}; token in memory (not localStorage); 401 interceptor registered; logout clears|M|P0|
|10|COMP-010|RateLimiter middleware|Token-bucket middleware keyed by IP or user; configurable thresholds per route.|Middleware|COMP-005|middleware wraps /login (10/min/IP), /register (5/min/IP); exceeded→429+Retry-After; metrics auth_ratelimit_total|M|P0|
|11|TEST-001|Unit: login valid credentials|AuthService.login happy path with mocked PasswordHasher+TokenManager.|Tests|FR-AUTH-001|PasswordHasher.verify called with email-derived user; TokenManager.issueTokens called; returns AuthToken with both tokens; coverage line+branch|S|P0|
|12|TEST-002|Unit: login invalid credentials|AuthService.login error path returns 401 without leaking enumeration.|Tests|FR-AUTH-001|PasswordHasher.verify→false→401; user-not-found→401 (same latency as verify-false ±10ms); TokenManager not called|S|P0|
|13|TEST-004|Integration: registration persists to DB|AuthService.register end-to-end against testcontainers Postgres.|Tests|FR-AUTH-002, DM-001|real PG via testcontainers; register→users row exists; password_hash stored as bcrypt cost-12; duplicate→409; cleanup after test|M|P0|
|14|Lockout-001|Account lockout (5/15min)|Track failed attempts in Redis keyed by user; lock after 5 in 15-min window.|COMP-005|AC-004, COMP-006, OQ-005|sliding-window counter in Redis; 5 fails/15min→locked=true; 423 returned; auto-unlock after 15min; admin-reset path (stub for Jordan)|M|P0|
|15|PolicyCheck-001|Password policy validator|Enforce 8+ chars, uppercase, number; return field-level errors for RegisterPage.|COMP-005|FR-AUTH-002|len>=8; [A-Z]; [0-9]; returns 400 with {field:"password",violations:[...]}; matches NIST SP 800-63B adaptive guidance|S|P0|
|16|UniqCheck-001|Email uniqueness check|Case-insensitive unique check against UserRepo; lowercase-normalize at ingress.|COMP-005|FR-AUTH-002, DM-001|email lowercased before lookup+store; UserRepo.findByEmail uses unique index; race handled via PG unique-violation→409|S|P0|
|17|ErrEnv-001|Error envelope standardization|Wrap all auth errors in {error:{code,message,status}} with stable code taxonomy.|COMP-005|AC-006|AUTH_INVALID_CREDENTIALS/AUTH_ACCOUNT_LOCKED/AUTH_DUPLICATE_EMAIL/AUTH_WEAK_PASSWORD/AUTH_RATE_LIMITED codes; message safe for i18n; status mirrors HTTP|S|P0|
|18|AC-011|v1.0 scope guardrail (no MFA/OAuth/RBAC)|Document + linter rule rejecting MFA/OAuth imports; roles[] present but not enforced.|Docs|-|ADR documents exclusions; import-lint rule blocks passport-oauth/speakeasy; roles array stored but no authZ middleware consumes it|S|P1|

### Integration Points — M2

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|Route dispatcher|Dispatch table|COMP-005 binds POST /login→handleLogin, POST /register→handleRegister, POST /logout→handleLogout|M2|API-001, API-002, API-007|
|RateLimiter middleware chain|Middleware|COMP-010 inserted before login/register handlers with per-route config|M2|API-001, API-002|
|Error envelope formatter|Callback|global error boundary maps thrown AuthError→{error:{code,message,status}}|M2|all /v1/auth/* routes|
|Feature flag AUTH_NEW_LOGIN (default OFF)|Strategy|COMP-001/002 check flag via config provider before rendering new flow|M2|COMP-001, COMP-002|
|Lockout counter strategy|Registry|Redis-backed sliding window registered in AuthService bootstrap|M2|FR-AUTH-001 login path|

### Milestone Dependencies — M2

- M1 exit criteria (all primitives green, routes scaffolded).
- SendGrid sandbox credentials for later email use (not blocking M2).
- OQ-005 lockout thresholds resolution before merging Lockout-001.

### Open Questions — M2

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-005|Account lockout policy thresholds (N attempts/window)?|TDD proposes 5/15min but PRD requires security sign-off; affects Lockout-001 implementation and NFR-SEC user-safety claim|Security|2026-05-01|

### Risk Assessment and Mitigation — M2

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-002 Brute-force on login|Medium|High|Medium|10/min IP rate limit + 5-fails/15min lockout + bcrypt cost 12; WAF IP block as contingency; CAPTCHA after 3 failures (deferred)|security-team|
|2|User enumeration via timing side-channel|High|Medium|High|Timing-safe PasswordHasher.verify; 401 returned at identical latency for user-not-found vs wrong-password (verified in TEST-002)|auth-team|
|3|Password policy too weak for NIST compliance|Medium|Low|High|PolicyCheck-001 validated against NIST SP 800-63B; legal review before GA|auth-team|
|4|Redis lockout counter drift on failover|Medium|Low|Medium|Redis persistence off but lockout counters ephemeral is acceptable; document + monitor Redis restarts|platform-team|

## M3: Token Management & Session (Weeks 6-7)

**Objective:** Deliver FR-AUTH-003 token lifecycle — JWT access token (15min) + Redis-stored refresh token (7d) issuance, validation, rotation, and revocation — with AuthProvider silent refresh and AC-P-002 admin audit visibility contract. | **Duration:** 2 weeks | **Entry:** M2 exit; Redis token schema design approved. | **Exit:** FR-AUTH-003 integration tests pass; TEST-003/005 green; refresh rotation invalidates old token; AuthProvider silent-refresh passes E2E smoke; quarterly key rotation dry-run successful on staging.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-AUTH-003|JWT token issuance and refresh|Complete TokenManager.issueTokens + validateRefresh + rotate; 15min access, 7d refresh TTL.|COMP-006|COMP-008, AC-004|login→access(15min)+refresh(7d); POST /refresh with valid token→new pair; expired→401; revoked→401; rotation invalidates prior refresh|L|P0|
|2|API-004|POST /auth/refresh endpoint|Wire refresh route with body-carried refreshToken, rotation semantics.|COMP-005|FR-AUTH-003, COMP-006|POST /v1/auth/refresh; body{refreshToken}; 200→new AuthToken pair; 401 expired/revoked; rate=30/min/user; old token revoked atomically|M|P0|
|3|NFR-SEC-002|RS256 signing validation|Runtime test asserts all issued JWTs use RS256 and 2048-bit key.|COMP-008|AC-001|config validation test asserts alg=RS256; kid present; 2048-bit key; startup fails on HS*; smoke test parses real-issued token|S|P0|
|4|AC-009|Quarterly JWT key rotation|Key rotation procedure with kid overlap (accept old+new for 24h window).|COMP-008|NFR-SEC-002|rotation script issues new kid; JwtService accepts both kids for 24h overlap; rotation runbook documented; staging dry-run executed|M|P0|
|5|COMP-006|TokenManager full implementation|Complete issuance/validation/revocation with hashed refresh storage in Redis.|COMP-006|AC-004, COMP-008|issueTokens hashes refresh (SHA-256) before Redis SET; validateRefresh fetches+compares; revoke DELs; tokens keyed by userId:jti|M|P0|
|6|COMP-008|JwtService full implementation|Complete sign/verify with kid resolution, clock-skew tolerance, claim validation.|COMP-008|AC-001|sign adds iss/aud/exp/iat/sub/jti/kid; verify validates all claims; rejects alg=none; 60s clock skew; kid lookup from keystore|S|P0|
|7|COMP-004|AuthProvider silent refresh|Enhance context to schedule refresh at T-60s to expiry; 401 interceptor auto-refresh-then-retry; clear on tab close.|Frontend|COMP-004 skeleton, API-004|refresh scheduled at 14min; 401 interceptor triggers refresh-then-retry once; failed-refresh→redirect /login; beforeunload→clearToken|M|P0|
|8|RefreshHash-001|Refresh token hashing strategy|Store SHA-256 of refresh token in Redis; never store plaintext.|COMP-006|COMP-006|Redis SET stores sha256(refreshToken); validateRefresh hashes input before GET; token rotation revokes old hash; security review signed off|S|P0|
|9|Revoke-001|Refresh revocation on rotation|On refresh, atomically delete old token + store new; reject replay.|COMP-006|FR-AUTH-003|Redis MULTI/EXEC or Lua for atomic DEL+SET; replay of rotated token→401; unit test exercises rotation race|S|P0|
|10|AC-012|Stateless service validation|CI test runs two AuthService pods, asserts login on pod-A + refresh on pod-B works.|Tests|COMP-005|k8s test spawns 2 replicas; login on pod-A, refresh on pod-B; succeeds; no in-memory session state leaked|S|P0|
|11|AC-P-002|Jordan (Admin) visibility contract|Publish structured auth-event log schema + topic contract for downstream admin UI.|Docs|COMP-005|JSON schema published; fields {userId,event,ts,ip,outcome,reason}; contract versioned; consumer channel documented|S|P1|
|12|TEST-003|Unit: token refresh with valid refresh|TokenManager.validateRefresh + rotate with mocked Redis.|Tests|FR-AUTH-003|valid refresh→revokes old→issues new pair via JwtService; mocks assert Redis DEL+SET called in MULTI; returns AuthToken|S|P0|
|13|TEST-005|Integration: expired refresh rejected|testcontainers Redis with 7d TTL; fast-forward clock; refresh returns 401.|Tests|FR-AUTH-003|real Redis with short TTL in test; fake timers advance past TTL; POST /refresh→401 AUTH_REFRESH_EXPIRED; revoked token→401|M|P0|
|14|TestHook-001|Clock injection for token tests|Inject ClockProvider into JwtService + TokenManager for deterministic expiry tests.|Tests|COMP-008, COMP-006|ClockProvider interface; real=Date.now, test=fake; unit tests advance fake clock without real sleeps; zero flakiness over 100 CI runs|S|P1|

### Integration Points — M3

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|Refresh token store (Redis)|Registry|TokenManager writes sha256(refresh)→{userId,issuedAt,expiresAt} keyed by jti|M3|FR-AUTH-003, Revoke-001|
|Key resolver (kid→pubkey)|Dispatch table|JwtService.verify dispatches on `kid` claim to matching key|M3|COMP-008, AC-009|
|AuthProvider 401 interceptor|Middleware|axios/fetch wrapper auto-invokes refresh-then-retry once|M3|all authenticated frontend calls|
|Silent-refresh scheduler|Callback|AuthProvider registers setTimeout at T-60s to token expiry|M3|COMP-004|
|Auth event publisher|Event bus|AuthService emits {login/refresh/logout/fail} events to log bus|M3|AC-P-002, M5 audit logger|
|Feature flag AUTH_TOKEN_REFRESH (default OFF)|Strategy|TokenManager.refresh gated on flag; when off, refresh endpoint returns 503 and legacy short sessions used|M3|API-004|

### Milestone Dependencies — M3

- M2 exit (login flow operational, AuthProvider skeleton live).
- Redis cluster confirmed at target capacity (~100K tokens ≈ 50MB).

### Open Questions — M3

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-001|Should AuthService support API key auth for service-to-service calls?|Affects whether TokenManager adds a second credential type; impacts Sam (AC-P-003) integration DX|test-lead|2026-04-15|
|2|OQ-004|Max refresh tokens per user across devices?|Bounds Redis working-set growth (OPS-004 sizing); affects multi-device UX|Product|2026-05-15|
|3|OQ-006|Support "remember me" for extended sessions?|May require distinct refresh TTLs; changes DM-002 shape and TokenManager API|Product|2026-05-15|

### Risk Assessment and Mitigation — M3

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-001 Token theft via XSS|High|Medium|High|accessToken memory-only in AuthProvider; refreshToken HttpOnly+Secure+SameSite=Strict cookie; 15-min access expiry; quarterly key rotation; contingency: TokenManager.revoke + force reset|security-team|
|2|Refresh token replay after rotation|High|Low|High|Atomic DEL+SET in Redis (MULTI/EXEC or Lua); Revoke-001 rejects replays; TEST-005 asserts|auth-team|
|3|Clock skew invalidating valid tokens|Medium|Low|Medium|60s skew tolerance in JwtService.verify; NTP on all pods; monitoring for drift>1s|platform-team|
|4|Silent-refresh race on multi-tab|Medium|Medium|Medium|AuthProvider uses BroadcastChannel or singleton refresh-in-flight promise; only one tab refreshes per rotation|frontend-team|

## M4: Profile & Password Reset (Weeks 8-9)

**Objective:** Deliver FR-AUTH-004 (profile retrieval) and FR-AUTH-005 (two-step password reset) end-to-end, including SendGrid email integration, reset-token lifecycle (1h TTL, single-use), and session-invalidation-on-password-change. | **Duration:** 2 weeks | **Entry:** M2 + M3 exits; SendGrid sandbox + production accounts approved; OQ-003 sync/async resolution. | **Exit:** FR-AUTH-004/005 integration tests pass; ProfilePage renders against API-003; reset email delivered <60s in staging; TEST-006 E2E green.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-AUTH-004|User profile retrieval|Implement AuthService.getProfile returning UserProfile for authenticated user.|COMP-005|COMP-009, COMP-006|GET /me with valid access→UserProfile (id,email,displayName,createdAt,updatedAt,lastLoginAt,roles); expired/invalid→401; touchLastLogin on retrieval option|S|P0|
|2|FR-AUTH-005|Password reset flow (two-step)|Implement reset-request (email send) + reset-confirm (token validate + hash update); session invalidation.|COMP-005|COMP-007, COMP-012, COMP-009, OQ-003|POST /reset-request→email sent within 60s (success same response regardless of email-known); POST /reset-confirm with valid token→password updated→all sessions revoked; 1h TTL; single-use|L|P0|
|3|API-003|GET /auth/me endpoint|Wire profile route with Bearer auth and rate limit.|COMP-005|FR-AUTH-004|GET /v1/auth/me; auth=Bearer; 200→UserProfile; 401 missing/invalid; rate=60/min/user|S|P0|
|4|API-005|POST /auth/reset-request endpoint|New endpoint to initiate password reset (referenced FR-AUTH-005 but not in TDD S8.1).|COMP-005|FR-AUTH-005, OQ-003|POST /v1/auth/reset-request; body{email}; 202 (always, no enumeration); rate=3/min/IP, 5/hour/email; emits ResetRequested event|M|P0|
|5|API-006|POST /auth/reset-confirm endpoint|New endpoint to validate reset token + set new password.|COMP-005|FR-AUTH-005, COMP-007|POST /v1/auth/reset-confirm; body{token,newPassword}; valid+unused token→200; expired/used→400 AUTH_RESET_TOKEN_INVALID; password policy enforced; all refresh tokens revoked|M|P0|
|6|COMP-003|ProfilePage (frontend)|React route /profile rendering UserProfile fields; protected by AuthProvider.|Frontend|COMP-004, API-003|protected route; renders displayName, email, createdAt; loading + error states; <1s render (PRD journey)|S|P0|
|7|COMP-012|EmailService client|SendGrid wrapper with template registry, retry+circuit-breaker, deliverability metrics.|Backend|-|SendGrid API key from secrets; retry 3x exp-backoff; circuit-breaker open after 10 failures/min; emits email_sent/failed metrics; sandbox vs prod env|M|P0|
|8|ResetTok-001|Reset token generation + TTL|Cryptographic random 32-byte token; SHA-256 hash stored in Redis with 1h TTL keyed by hash.|COMP-005|AC-004|crypto.randomBytes(32); base64url; sha256 hashed in Redis; TTL=3600s; key=reset:sha256(token)→userId; entropy>=256 bits|S|P0|
|9|ResetSingleUse-001|Single-use reset token|Atomic Redis GET+DEL on confirm; second confirm with same token→400.|COMP-005|ResetTok-001|Lua script atomic GET+DEL; second use→400 AUTH_RESET_TOKEN_INVALID; metric reset_token_reused_total|S|P0|
|10|SessionRevoke-001|Invalidate sessions on password change|On reset-confirm success, delete all refresh tokens for userId.|COMP-006|FR-AUTH-005, COMP-006|Redis SCAN+DEL pattern user:{id}:refresh:*; user must re-login on all devices; PRD AC.5 satisfied|S|P0|
|11|EmailTpl-001|Reset email template|HTML+plaintext template with reset link, expiry notice, support contact.|Templates|COMP-012|template versioned in repo; reset link uses 1-time token; expiry shown ("expires 1h"); plaintext fallback; passes Spam-Assassin <3.0|S|P1|
|12|TEST-006|E2E: register → login → profile|Playwright flow exercising RegisterPage→LoginPage→ProfilePage through AuthProvider.|Tests|COMP-001,COMP-002,COMP-003,COMP-004|Playwright spec; new user registers; logs out; logs in; navigates to /profile; sees own data; runs in CI staging env|M|P0|
|13|TEST-RESET-001|Integration: reset confirm invalidates sessions|testcontainers Redis + Postgres; complete reset flow; verify prior refresh tokens rejected.|Tests|FR-AUTH-005, SessionRevoke-001|user has 3 active refresh tokens; reset-confirm succeeds; all 3 refresh→401; new login works|M|P0|
|14|EmailDel-001|Email deliverability monitoring|SendGrid event webhook → metrics; alert on delivery rate <95% over 15min.|Backend|COMP-012|webhook endpoint receives delivered/bounced/dropped; emits email_delivery_status_total; alert on success<95%/15min; dashboard panel|S|P1|

### Integration Points — M4

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|EmailService template registry|Registry|COMP-012 loads templates from /templates dir keyed by name|M4|EmailTpl-001, future verification emails|
|Reset token store (Redis)|Registry|reset:sha256(token)→userId with 1h TTL|M4|ResetTok-001, ResetSingleUse-001|
|Session revocation strategy|Strategy|user-id-prefix SCAN+DEL pattern registered with TokenManager|M4|SessionRevoke-001|
|SendGrid event webhook|Callback|inbound webhook→EmailDel-001 metric publisher|M4|EmailDel-001|
|ResetRequested event|Event binding|API-005 emits to event bus; future consumers (audit, analytics)|M4|M5 AuditLogger|
|Profile route guard|Middleware|AuthProvider HOC redirects unauthenticated users to /login with returnUrl|M4|COMP-003|

### Milestone Dependencies — M4

- M2 (login/registration), M3 (token mgmt) exits.
- SendGrid (external) — production API key + DKIM/SPF configured.
- OQ-003 sync vs async email decision (blocks API-005 implementation pattern).

### Open Questions — M4

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-003|Should password reset emails be sent sync or async?|Affects API-005 latency budget (sync=>500ms+SendGrid SLA risk; async=>queue infra needed)|Engineering|2026-06-01|

### Risk Assessment and Mitigation — M4

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-006 Email delivery failures block password reset|Medium|Low|Medium|SendGrid delivery monitoring + alerting (EmailDel-001); fallback support channel; retry with exponential backoff; circuit-breaker prevents cascading|platform-team|
|2|Reset token enumeration via timing|High|Low|High|Constant-time hash compare; identical 202 response regardless of email known|security-team|
|3|Reset link leaked via referer/logs|High|Low|High|Reset URL uses POST-only landing page (no GET token in URL after first click); referer-policy:no-referrer; access logs redact token query param|security-team|
|4|Race: same token used twice concurrently|Medium|Low|Medium|ResetSingleUse-001 atomic Lua script; only one wins; loser→400|auth-team|

## M5: Security, Compliance & Observability (Weeks 10-11)

**Objective:** Land cross-cutting NFRs — GDPR consent capture (NFR-COMPLIANCE-001), SOC2 audit logging (NFR-COMPLIANCE-002), data minimization (NFR-COMPLIANCE-003), Prometheus metrics + OpenTelemetry traces + alerts (OPS-005), plus security validations (brute-force, token theft, pen-test). | **Duration:** 2 weeks | **Entry:** M2 + M3 + M4 exits; audit log schema approved by compliance. | **Exit:** audit log covers all 7 auth event types with 12-month retention policy; consent record persisted at registration; dashboards green; pen-test report with zero critical findings; SOC2 control mapping validated.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|NFR-COMPLIANCE-001|GDPR consent at registration|Capture consent record at registration with timestamp, version, IP.|COMP-005|FR-AUTH-002, DM-001|RegisterPage adds consent checkbox (required); register API stores consent{version,ts,ip} row; rejection→400 AUTH_CONSENT_REQUIRED; historical versions retained|M|P0|
|2|NFR-COMPLIANCE-002|SOC2 audit logging|Log every auth event with userId, ts, ip, outcome, event-type; 12-month retention.|COMP-011|COMP-005|events: login_success/login_fail/register/refresh/logout/reset_request/reset_confirm; fields userId,ts,ip,ua,outcome,reason; 12mo retention; immutable (append-only); queryable by userId+date range|L|P0|
|3|NFR-COMPLIANCE-003|Data minimization|Audit data collection — only email, password_hash, displayName collected.|Docs|DM-001|DPIA doc attesting collected fields; PR-lint blocks new user columns without compliance review; logs redact PII beyond email+userId|S|P0|
|4|COMP-011|AuditLogger component|Structured audit log writer with Postgres append-only table + retention job.|Backend|AC-003|AuditLogger.log(event) writes to audit_events table; table partitioned monthly; cron deletes partitions >12mo; JSON schema enforced at write|M|P0|
|5|OPS-005|Observability stack|Prometheus metrics, OpenTelemetry tracing, alert rules, structured logging.|Infra|COMP-005, COMP-006, COMP-007, COMP-008|auth_login_total/auth_login_duration_seconds/auth_token_refresh_total/auth_registration_total registered; OTel spans span AuthService→PasswordHasher→TokenManager→JwtService; alerts login-failure>20%/5min, p95>500ms, Redis-conn-fail; JSON logs with redaction|L|P0|
|6|ConsentCapture-001|Consent UI + schema|Add consent checkbox to RegisterPage; data model for consent records.|Frontend,DB|NFR-COMPLIANCE-001|RegisterPage adds required checkbox with link to policy; consent_records table(userId,policyVersion,ts,ip); FK from users; migration idempotent|S|P0|
|7|AuditSchema-001|Audit log JSON schema|Publish + enforce JSON schema for audit events; versioned.|Docs|NFR-COMPLIANCE-002|schema file in repo /schemas/audit-event-v1.json; AuditLogger validates writes; breaking change requires new version; consumers pinned to version|S|P0|
|8|AuditRetention-001|12-month retention job|Cron job deletes audit partitions older than 12 months; logs deletion counts.|Infra|COMP-011|k8s CronJob runs monthly; DROPs partitions where month<(now-12mo); emits metric audit_retention_deleted_total; 90-day operational PG copy preserved|S|P0|
|9|MetricsInstr-001|Prometheus metric instrumentation|Instrument AuthService/TokenManager/PasswordHasher/JwtService with counters+histograms.|Backend|OPS-005|counters auth_*_total{status=success|fail}; histogram auth_login_duration_seconds buckets[0.05,0.1,0.2,0.5,1]; labels scrubbed of PII; /metrics endpoint scraped|M|P0|
|10|OTelTracing-001|OpenTelemetry tracing|Wire OTel SDK; propagate traceparent; ensure span hierarchy.|Backend|OPS-005|OTel auto-instr for HTTP+PG+Redis; manual spans for PasswordHasher.hash/verify; traceparent header ingress→egress; exported to collector|M|P0|
|11|AlertRules-001|Alert rule definitions|Prometheus alert rules for login failure rate, p95 latency, Redis conn failures.|Infra|OPS-005, MetricsInstr-001|alert login_failure_rate_high (>20%/5min) → severity=warning; p95_latency_high (>500ms/5min) → warning; p95_latency_critical (>1000ms/5min) → page; redis_conn_fail (>10/min) → page|S|P0|
|12|StructLog-001|Structured JSON logging + redaction|JSON logger with automatic PII redaction (passwords, tokens, raw email in some contexts).|Backend|OPS-005|pino JSON output; redactor masks password/newPassword/refreshToken/accessToken; unit test asserts no plaintext secret in log stream|S|P0|
|13|SecTestBrute-001|Security test: brute-force protection|Automated test exercises 6 rapid failed logins, asserts 423 and rate-limit engagement.|Tests|Lockout-001, COMP-010|test runs 10 failed attempts in 1min; after attempt 5 → 423; after 10 → 429; metrics incremented; auto-unlock after 15min verified|S|P0|
|14|SecTestXSS-001|Security test: token theft mitigation|Pen-test that XSS cannot exfil accessToken (memory-only) or refreshToken (HttpOnly).|Tests|R-001, COMP-004|simulated XSS payload attempts document.cookie + window.fetch; refreshToken HttpOnly (unreachable from JS); accessToken not in storage; failure modes documented|M|P0|
|15|PenTest-001|External penetration test|Third-party pen-test of all /v1/auth/* endpoints against OWASP Top 10.|Tests|M4 exit|pen-test report delivered; zero critical, zero high findings; medium findings triaged with remediation SLA; retest passes|L|P0|
|16|CORSTest-001|CORS + TLS config validation|Automated test asserts CORS rejects unknown origins; TLS1.3 enforced; no TLS1.1/1.0.|Tests|AC-007, AC-008|test hits endpoint from whitelisted origin→200; from unknown→403; curl --tls-max 1.2 refused; SSLLabs scan A+|S|P0|

### Integration Points — M5

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|AuditLogger event bus subscriber|Event binding|COMP-011 subscribes to auth-event bus emitted by M2 AuthService|M5|NFR-COMPLIANCE-002|
|Metric registry (Prometheus)|Registry|all backend components register counters/histograms via shared registry|M5|OPS-005, AlertRules-001|
|OTel span decorator|Middleware|HTTP middleware wraps each handler with span; auto-propagation|M5|OTelTracing-001|
|Alert handler dispatch|Dispatch table|alertmanager routes: warning→slack, critical→pagerduty|M5|AlertRules-001, on-call|
|Log redaction transformer|Middleware|pino serializer pipeline redacts known sensitive keys|M5|StructLog-001|
|Retention cron|Scheduler|k8s CronJob registered for monthly audit partition drop|M5|AuditRetention-001|
|Consent version registry|Registry|policyVersion keyed strings; app reads current; historical preserved|M5|ConsentCapture-001|

### Milestone Dependencies — M5

- M2/M3/M4 exits (core flows emit events to wire up).
- Compliance team sign-off on audit schema (AuditSchema-001).
- OQ-007 admin tooling scope decision (affects whether audit query UI is in v1.0).

### Open Questions — M5

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-007|PRD JTBD for Jordan (admin audit log UI) has no corresponding FR in TDD — is admin tooling in scope v1.0?|If in-scope, adds significant FR + UI work; if out-of-scope, only AC-P-002 contract emitted. PRD requires; TDD should be updated.|product-team|2026-06-15|

### Risk Assessment and Mitigation — M5

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-005 Compliance failure from incomplete audit logging|High|Medium|High|Validate SOC2 controls in QA; define log schema early (AuditSchema-001); legal/compliance sign-off gate before GA; retention job tested|compliance-team|
|2|PII leak in logs or metrics|High|Medium|High|StructLog-001 redactor + unit tests asserting no plaintext token/password in log stream; metric labels audited for cardinality + PII|security-team|
|3|Alert fatigue from noisy rules|Medium|Medium|Low|Thresholds tuned against staging baseline; warning vs critical split; on-call feedback loop post-GA|sre-team|
|4|GDPR DPIA gap blocks launch|High|Low|High|NFR-COMPLIANCE-003 DPIA doc produced + legal-reviewed in M5 week 1|compliance-team|

## M6: Migration, Rollout & GA (Weeks 12-14)

**Objective:** Execute three-phase feature-flagged rollout (MIG-001 Alpha → MIG-002 Beta 10% → MIG-003 GA), validate NFR performance + reliability targets under load, publish runbooks (OPS-001/002), capacity-size infrastructure (OPS-004), and deprecate legacy auth. | **Duration:** 3 weeks | **Entry:** M5 exits + pen-test clean + compliance sign-off. | **Exit:** MIG-003 GA reached; 99.9% uptime over 7 days post-GA; legacy endpoints deprecated; all runbooks exercised via game-day; SC-001..SC-012 targets met.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|AC-010|Feature flag wiring (AUTH_NEW_LOGIN, AUTH_TOKEN_REFRESH)|Integrate feature flag service; gate LoginPage/login handler and refresh endpoint.|COMP-005,Frontend|M2, M3|flag provider injected; AUTH_NEW_LOGIN default OFF (Phase 1) → 10% (Phase 2) → 100% (Phase 3); AUTH_TOKEN_REFRESH default OFF → ON at Phase 3; flag removal scheduled Phase 3+2w|M|P0|
|2|MIG-001|Phase 1 — Internal Alpha (1 week)|Deploy AuthService to staging; auth-team + QA test all endpoints; flags OFF for prod.|Release|M5 exit|AuthService on staging with all endpoints live; auth-team executes test plan covering FR-AUTH-001..005; zero P0/P1 defects; manual sign-off|L|P0|
|3|MIG-002|Phase 2 — Beta 10% (2 weeks)|Enable AUTH_NEW_LOGIN for 10% traffic; monitor p95, error rate, Redis.|Release|MIG-001|10% traffic via feature-flag targeting; p95<200ms sustained 72h; error<0.1% 72h; zero Redis failures; rollback tested once|L|P0|
|4|MIG-003|Phase 3 — General Availability|Ramp to 100%; deprecate legacy endpoints; enable AUTH_TOKEN_REFRESH.|Release|MIG-002|100% traffic on new; legacy /auth/* marked deprecated with 301 to /v1/auth/*; AUTH_TOKEN_REFRESH on; 99.9% uptime 7d post-ramp; flag removal scheduled|L|P0|
|5|OPS-001|Runbook — AuthService down|Document symptoms, diagnosis, resolution, escalation for total outage.|Docs|OPS-005|runbook in repo /runbooks/authservice-down.md; covers pod health/PG conn/init logs/restart/PG failover/Redis-down contingency; escalation auth-team→15min→platform-team; game-day exercised|S|P0|
|6|OPS-002|Runbook — Token refresh failures|Document diagnosis + resolution for refresh failures / AuthProvider loops.|Docs|OPS-005|runbook /runbooks/token-refresh.md; covers Redis conn/key access/flag state; resolutions Redis scale/secret remount/flag toggle; escalation path|S|P0|
|7|OPS-003|On-call expectations + rotation|24/7 auth-team rotation first 2 weeks post-GA; P1 ack<15min; access to dashboards.|Docs|OPS-001, OPS-002|PagerDuty schedule configured; P1 ack SLA=15min; runbook access for auth-team→test-lead→eng-manager→platform-team; access to k8s/Grafana/Redis CLI/PG admin verified|S|P0|
|8|OPS-004|Capacity planning + HPA|3 replicas min, HPA to 10 at CPU>70%; PG pool 100→200; Redis 1GB→2GB at >70%.|Infra|M1|HPA manifest min=3 max=10 target-cpu=70; PG pool alert at wait>50ms; Redis alert at util>70% with auto-scale runbook; capacity model documented|M|P0|
|9|NFR-PERF-001|Validate p95<200ms at load|k6 load test at production traffic profile.|Tests|MIG-002|k6 script simulating login:60%, refresh:30%, register:10%; 500 RPS sustained 30min; p95<200ms; passed on staging before Phase 3|M|P0|
|10|NFR-PERF-002|Validate 500 concurrent logins|k6 ramp test.|Tests|NFR-PERF-001|k6 ramp to 500 concurrent virtual users; error rate<0.5%; p99<500ms; HPA observed scaling; passes CI gate|S|P0|
|11|NFR-REL-001|Validate 99.9% availability|Uptime monitoring via synthetic health-check probes over 30-day window.|Tests|MIG-003|health-check probe every 1min from 3 regions; uptime dashboard; 30-day rolling 99.9% achieved; downtime tracked with postmortem|M|P0|
|12|Rollback-001|Rollback procedure validation|Game-day exercise disabling AUTH_NEW_LOGIN and routing to legacy.|Tests|AC-010, MIG-002|ordered steps (disable flag→smoke legacy→RCA→data restore if needed→notify→post-mortem); exercise executed in staging; MTTR<10min for flag-based rollback|M|P0|
|13|LegacyDeprec-001|Legacy endpoint deprecation|Mark legacy /auth/* as deprecated with sunset header + 301 redirect.|Backend|MIG-003|Sunset header + Deprecation header per RFC8594; 301 to /v1/auth/*; legacy traffic <1%/7d before removal; removal ticketed for +4 weeks|S|P1|
|14|GAExit-001|GA exit gate checklist|Formal go/no-go checklist covering SC-001..012, dashboards green, compliance signed off.|Release|SC-001..012|checklist doc enumerated; green across: SC-001 p95<200ms, SC-002 reg>99%, SC-003 refresh<100ms, SC-004 99.9%, SC-005 hash<500ms, SC-011 coverage≥80%, SC-012 FR tests green; stakeholder signatures|S|P0|
|15|Backup-001|Pre-phase backup automation|Automated PG snapshot before each phase gate; retained 30d.|Infra|AC-003|pre-Phase1/2/3 PG snapshot via managed service; retention 30d; restore-to-staging drill executed once|S|P0|
|16|Postmortem-001|Post-mortem template + SLA|Template + 48h SLA for incident post-mortem per TDD rollback procedure.|Docs|OPS-001|template in /runbooks/postmortem-template.md; Jira/Linear auto-ticket on P0/P1; 48h SLA tracked|S|P1|

### Integration Points — M6

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|Feature flag registry|Registry|AUTH_NEW_LOGIN + AUTH_TOKEN_REFRESH registered in flag service with targeting rules|M6|AC-010, MIG-001/002/003|
|Rollback hook|Callback|one-click flag revert in control plane; emits rollback_event|M6|Rollback-001|
|Load test harness|Strategy|k6 scripts pinned to traffic profile; run via CI on staging + ad-hoc in prod (read-only paths)|M6|NFR-PERF-001/002|
|HPA controller|Dispatch|k8s HPA evaluates CPU target every 15s, scales replicas|M6|OPS-004|
|Uptime probe scheduler|Scheduler|synthetic monitor (Pingdom/Datadog) runs /healthz every 60s from 3 regions|M6|NFR-REL-001|
|Game-day runbook dispatcher|Playbook|on-call drills scheduled weekly for first month post-GA|M6|OPS-001, OPS-002, Rollback-001|

### Milestone Dependencies — M6

- M1-M5 all exit criteria.
- Pen-test report (PenTest-001) with zero critical/high.
- Compliance sign-off (NFR-COMPLIANCE-001/002/003 DPIA + SOC2 control mapping).
- Legacy auth decommission timeline approved by product.

### Risk Assessment and Mitigation — M6

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-003 Data loss during migration|High|Low|High|Parallel legacy run Phases 1-2; idempotent upsert; Backup-001 pre-phase snapshots; rollback runbook exercised; restore drill completed|platform-team|
|2|R-004 Low registration adoption|High|Medium|High|Usability testing in MIG-001 Alpha; funnel analytics dashboards pre-GA; iterate RegisterPage between Phase 2 and Phase 3 based on data|product-team|
|3|Phase 2 10% traffic masks tail-latency regression|Medium|Medium|Medium|MIG-002 requires p95<200ms sustained 72h before Phase 3; tail-latency alert at p99>500ms; NFR-PERF-001 validated at full-load BEFORE phase ramps|sre-team|
|4|HPA thrash under burst traffic|Medium|Low|Medium|HPA cooldown tuned; burst capacity reserved; load test NFR-PERF-002 exercises ramp; on-call playbook includes manual scale override|platform-team|
|5|Legacy endpoint removal breaks unknown clients|Medium|Medium|Medium|Sunset+Deprecation headers for 4 weeks before removal; access logs analyzed for unknown User-Agents; customer comms for Sam (API consumers)|auth-team|

## Resource Requirements and Dependencies

### External Dependencies

|Dependency|Required By Milestone|Status|Fallback|
|---|---|---|---|
|PostgreSQL 15+ (INFRA-DB-001)|M1|Provisioned|None — hard block; escalate to platform-team|
|Redis 7+|M1|Provisioned|In-memory fallback for dev only; no prod fallback (refresh unavailable)|
|Node.js 20 LTS|M1|Available|Node 18 LTS until Oct 2026 (non-preferred)|
|bcryptjs|M1|Available (npm)|argon2 if bcrypt maintenance stalls (requires AC-002 revision)|
|jsonwebtoken (RS256)|M1|Available (npm)|jose library (drop-in replacement if needed)|
|SendGrid|M4|Production account approval pending|AWS SES as fallback (requires EmailService adapter)|
|API Gateway (upstream)|M2|Shared infra|Direct ingress with in-app rate limit (degraded)|
|Kubernetes + HPA|M6|Shared infra|Static 5-replica deployment (loses elasticity)|
|Prometheus|M5|Shared infra|Datadog metrics (cost impact)|
|OpenTelemetry collector|M5|Shared infra|Honeycomb direct export|
|AUTH-PRD-001|M1-M6|Active (this doc)|N/A|
|SEC-POLICY-001|M1|Published|N/A — hard block|

### Infrastructure Requirements

- Postgres 15: 100-conn pool, multi-AZ, automated backups every 6h, 30-day retention, read replica with <5s lag.
- Redis 7: 1 GB initial, scale to 2 GB when utilization >70%, TLS-auth, no persistence needed (ephemeral refresh tokens acceptable).
- Kubernetes: min 3 / max 10 AuthService replicas with HPA target CPU 70%; PDB=1; rolling-update maxUnavailable=1.
- Secrets manager: RSA keypair storage with quarterly rotation support; SendGrid API key; Redis/Postgres credentials.
- Observability: Prometheus scrape targets, OTel collector, Loki/CloudWatch for logs, Grafana dashboards (login-ops, token-ops, reset-ops, SOC2-audit).
- CI/CD: testcontainers for PG+Redis integration tests; Playwright for E2E; k6 for load; trivy for container scanning.
- PagerDuty schedule for auth-team rotation post-GA.
- Network: TLS 1.3 at ingress; CORS allowlist; WAF (IP-based rate limiting + bot protection).

## Risk Register

|ID|Risk|Affected Milestones|Probability|Impact|Mitigation|Owner|
|----|------|---------------------|-------------|--------|------------|-------|
|R-001|Token theft via XSS|M3, M5|Medium|High|accessToken memory-only in AuthProvider; HttpOnly Secure SameSite=Strict cookie for refreshToken; 15-min access expiry; quarterly key rotation (AC-009); revoke via TokenManager + force reset as contingency|security-team|
|R-002|Brute-force on login|M2, M5|High|Medium|10 req/min IP rate limit (COMP-010); 5-fails/15min lockout (Lockout-001); bcrypt cost 12; WAF IP block as contingency; CAPTCHA after 3 failures (deferred to v1.1)|security-team|
|R-003|Data loss during migration|M1, M6|Low|High|Pre-phase backups (Backup-001); idempotent upsert; parallel legacy run Phases 1-2; documented rollback runbook; restore drill executed|platform-team|
|R-004|Low registration adoption|M4, M6|Medium|High|Usability testing in Alpha phase; funnel analytics dashboards; iterate RegisterPage between Phase 2 and Phase 3 based on data (PRD SC-006 >60% target)|product-team|
|R-005|Compliance failure from incomplete audit logging|M5, M6|Medium|High|Validate SOC2 controls in QA; define audit log schema (AuditSchema-001) early; compliance sign-off gate before GA; 12-month retention job (AuditRetention-001) tested|compliance-team|
|R-006|Email delivery failures block password reset|M4, M6|Low|Medium|SendGrid delivery monitoring (EmailDel-001); alerting; retry with exponential backoff; circuit-breaker; fallback support channel|platform-team|
|R-007|PII leak in logs or metrics|M5, M6|Medium|High|StructLog-001 redactor with unit tests asserting no plaintext token/password in log stream; metric label cardinality audit|security-team|
|R-008|User enumeration via timing side-channel|M2, M5|Medium|High|Timing-safe PasswordHasher.verify; 401 returned at identical latency for user-not-found vs wrong-password (TEST-002 asserts)|auth-team|
|R-009|Refresh token replay after rotation|M3|Low|High|Atomic DEL+SET in Redis via Lua script; Revoke-001 rejects replays; TEST-005 asserts|auth-team|
|R-010|Phase 2 10% traffic masks tail-latency regression|M6|Medium|Medium|MIG-002 requires p95<200ms sustained 72h before Phase 3; p99>500ms alert; NFR-PERF-001 full-load validation before ramp|sre-team|

## Success Criteria and Validation Approach

|Criterion|Metric|Target|Validation Method|Milestone|
|---|---|---|---|---|
|SC-001|Login p95 latency|<200ms|k6 load test (NFR-PERF-001) + APM p95 dashboard|M6|
|SC-002|Registration success rate|>99%|Funnel analytics on POST /register 2xx/total|M6|
|SC-003|Token refresh p95 latency|<100ms|APM p95 on /auth/refresh over 7-day window|M6|
|SC-004|Service availability|99.9% over 30d|Synthetic uptime probe (NFR-REL-001) from 3 regions|M6|
|SC-005|PasswordHasher.hash() duration|<500ms|Unit benchmark + production histogram p95|M2|
|SC-006|Registration conversion|>60%|Funnel landing→register→confirmed|M6|
|SC-007|Authenticated DAU within 30d of GA|≥1000|Analytics count of unique userIds with login event|M6|
|SC-008|Avg session duration|>30min|Refresh-event interval analytics|M6|
|SC-009|Failed login rate|<5% of attempts|auth_login_total{status="fail"}/total|M6|
|SC-010|Password reset completion|>80%|Funnel reset-requested → reset-confirmed|M6|
|SC-011|Unit test coverage|≥80% AuthService/TokenManager/JwtService/PasswordHasher|Jest coverage report in CI|M2-M4|
|SC-012|FR integration tests|All 5 FRs pass|testcontainers PG+Redis integration suite green|M2-M4|

## Decision Summary

|Decision|Chosen|Alternatives Considered|Rationale|
|----------|--------|------------------------|----------|
|Session model|JWT stateless + Redis refresh (AC-001, AC-004)|Server-side sessions; JWT-only refresh|NFR-PERF-002 requires 500 concurrent; stateless AuthService enables HPA (OPS-004); Redis refresh enables revocation (R-001 mitigation)|
|Password hashing|bcrypt cost 12 (AC-002, NFR-SEC-001)|argon2id; scrypt|NIST SP 800-63B compliant; mature node support; hash<500ms (SC-005) with cost 12; matches SEC-POLICY-001|
|Token signing algorithm|RS256 2048-bit (AC-001, NFR-SEC-002)|HS256 shared secret; ES256|RS256 enables public-key verification without shared secret; quarterly rotation (AC-009) easier; aligns with OAuth2 best practice|
|API versioning|URL-prefix `/v1/auth/*` (AC-006)|Header-based; accept-based|URL-prefix trivially cacheable and client-readable; breaking changes require v2 route; additive safe in-version|
|Rollout strategy|Dual feature flag phased 10%→100% (AC-010, MIG-001-003)|Big-bang cutover; blue-green only|Feature flags enable fast rollback (R-003); 10% beta bounds blast radius; TDD S19.2 prescribes; NFR-REL-001 99.9% requires gradual validation|
|Frontend token storage|AuthProvider memory + HttpOnly cookie refresh (COMP-004)|localStorage access token; sessionStorage|Mitigates R-001 XSS token theft; HttpOnly refresh resists JS exfil; memory-only access clears on tab close|
|Refresh token storage|Redis hashed, 7-day TTL (COMP-006, RefreshHash-001)|Postgres table; JWT refresh|Redis O(1) lookup <5ms supports SC-003 <100ms; TTL enforces expiry automatically; hashing prevents plaintext theft on Redis compromise|
|Email provider|SendGrid (COMP-012)|AWS SES; Mailgun|Assumption in PRD dependencies table; templates + webhook events already integrated at org; AWS SES fallback documented|
|Rate limiting|App-level COMP-010 + API Gateway|Gateway only; WAF only|Defense-in-depth; app-level needed per-user (not IP) limits; gateway provides IP floor|
|Audit log storage|Postgres partitioned append-only (COMP-011)|Immutable log service; S3+Athena|SOC2 requires queryable by userId+date; partitioning supports retention job (AuditRetention-001); uses existing PG infra|
|Password reset UX|202 Accepted always, no enumeration|Return 404 if email unknown|OWASP + PRD AC: prevents email enumeration; SC-010 >80% completion does not require early failure|
|Lockout threshold|5 attempts / 15 min sliding (Lockout-001)|3/10min; 10/1h|TDD S6 baseline; OQ-005 security review pending; balance R-002 vs usability|

## Timeline Estimates

|Milestone|Duration|Start|End|Key Milestones|
|---|---|---|---|---|
|M1|2 weeks|W1|W2|Postgres/Redis provisioned; DM-001/002 frozen; AuthService+TokenManager scaffolds green; OQ-002 resolved|
|M2|3 weeks|W3|W5|FR-AUTH-001/002 integration tests green; LoginPage/RegisterPage behind AUTH_NEW_LOGIN=false; TEST-001/002/004 ≥80% coverage|
|M3|2 weeks|W6|W7|FR-AUTH-003 + API-004 live; AuthProvider silent-refresh operational; TEST-003/005 green; key rotation dry-run passed|
|M4|2 weeks|W8|W9|FR-AUTH-004/005 + API-003/005/006 live; ProfilePage rendered; SendGrid reset-email <60s; TEST-006 E2E green|
|M5|2 weeks|W10|W11|NFR-COMPLIANCE-001/002/003 landed; OPS-005 dashboards + alerts live; pen-test clean; audit log 12mo retention enforced|
|M6|3 weeks|W12|W14|MIG-001 Alpha (W12) → MIG-002 Beta 10% (W13-W14 start) → MIG-003 GA (W14); NFR-PERF/REL validated; runbooks game-dayed; SC-001..012 met|

**Total estimated duration:** 14 weeks (approximately 3.5 months). Critical path runs M1→M2→M3→M4→M5→M6 with M3 and M4 partially parallelizable (M4 can begin once M3 token scaffolding is complete, week 7).
