---
spec_source: "test-tdd-user-auth.compressed.md"
complexity_score: 0.68
complexity_class: MEDIUM
primary_persona: architect
---

# User Authentication Service — Project Roadmap

## Executive Summary

Build a secure, self-service identity layer (email/password, JWT + refresh tokens, self-service reset) as the foundational capability unblocking the Q2–Q3 2026 personalization roadmap and SOC2 Type II audit readiness. Scope is intentionally narrow: no OAuth/MFA/RBAC in v1.0. Architecture separates concerns across eight components (AuthService, TokenManager, JwtService, PasswordHasher, AuthProvider, LoginPage, RegisterPage, ProfilePage) backed by PostgreSQL 15 (UserProfile + audit log) and Redis 7 (refresh tokens). Rollout uses two feature flags and a three-phase traffic ramp (Alpha → Beta 10% → GA 100%) with parallel legacy operation through MIG-002.

**Business Impact:** Unblocks ~$2.4M projected annual revenue from personalization features; satisfies Q3 2026 SOC2 audit gate; targets >60% registration conversion, <200ms p95 login, 99.9% uptime.

**Complexity:** MEDIUM (0.68) — narrow auth-only scope is offset by high security sensitivity (0.85), multi-integration surface (PostgreSQL + Redis + SendGrid + API Gateway = 0.75), and explicit compliance burden (SOC2 + GDPR + NIST).

**Critical path:** DM-001/DM-002 schema → PasswordHasher + JwtService + TokenManager → AuthService orchestration → API endpoints (API-001..006) → AuthProvider + pages → load/security test → MIG-001..003 phased rollout. TokenManager + Redis integration is the highest-risk link; parallel legacy operation through Beta protects rollback.

**Key architectural decisions:**

- Stateless API with JWT-only access tokens (15-min TTL, RS256) and opaque Redis-stored refresh tokens (7-day TTL, hashed); accessToken in browser memory only, refreshToken in HttpOnly cookie — mitigates R-001 (XSS token theft).
- PostgreSQL 15 for UserProfile + audit log (indefinite + 90-day retention respectively); Redis 7 for refresh token store only — cleanly separates durable identity from ephemeral session state.
- URL-prefix API versioning (`/v1/auth/*`) with a canonical error envelope `{ error: { code, message, status } }` across all six endpoints — enables non-breaking additions without client churn.
- Two-flag rollout (`AUTH_NEW_LOGIN`, `AUTH_TOKEN_REFRESH`) with three-phase ramp and parallel legacy operation during Phases 1–2 — mitigates R-003 (migration data loss).

**Open risks requiring resolution before M1:**

- OQ-002 (UserProfile.roles max length) must be resolved before DM-001 schema is frozen; default to VARCHAR[] with application-level cap is the fallback.
- OQ-PRD-003 (lockout threshold) must be confirmed before M2 lockout logic is implemented; default is 5 attempts / 15 min per FR-AUTH-001 AC.
- SendGrid account provisioning and API key must be available before M2 reset-email integration work begins (R-PRD-004).
- RSA key material (2048-bit, quarterly rotation procedure) must be provisioned in the secrets volume before M2 JwtService work begins.

## Milestone Summary

|ID|Title|Type|Priority|Effort|Dependencies|Deliverables|Risk|
|---|---|---|---|---|---|---|---|
|M1|Foundation and Data Layer|Infrastructure|P0|2 weeks|—|12|Medium|
|M2|Core Auth Components|Backend|P0|2 weeks|M1|17|High|
|M3|API Layer and Gateway|Backend|P0|2 weeks|M2|16|Medium|
|M4|Frontend Auth Experience|Frontend|P0|1 week|M3|9|Medium|
|M5|Testing, Security and Compliance|Quality|P0|2 weeks|M4|12|High|
|M6|Rollout and Operations|Ops|P0|3 weeks|M5|22|High|

## Dependency Graph

```
M1 (Foundation + Data)
  └─► M2 (Core Auth Components)
        └─► M3 (API Layer + Gateway)
              └─► M4 (Frontend Auth Experience)
                    └─► M5 (Testing + Security + Compliance)
                          └─► M6 (Rollout + Operations)

External: PostgreSQL 15 → M1 · Redis 7 → M1 · SendGrid → M2 · API Gateway → M3 · Frontend routing → M4 · k6 load tool → M5
Cross-cutting: NFR-COMPLIANCE-002 audit logging surfaces across M1 (schema), M2 (emission), M3 (admin query), M6 (retention).
Critical path: DM-001 → COMP-008 → COMP-007 → COMP-006 → COMP-005 → API-001..006 → COMP-004 → TEST-006 → MIG-003.
```

## M1: Foundation and Data Layer

**Objective:** Provision PostgreSQL + Redis, establish UserProfile and AuthToken schemas, stand up repository abstractions and audit-log infrastructure. | **Duration:** 2 weeks (Week 1–2) | **Entry:** PostgreSQL 15 + Redis 7 provisioned, OQ-002 resolved, primary_persona architect confirms schema. | **Exit:** DM-001 + DM-002 applied to staging DB; repos pass unit tests; audit log table writes confirmed; schema review sign-off.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|DM-001|UserProfile data model|Relational PostgreSQL 15 table representing authenticated users. Indefinite retention.|PostgreSQL|—|id:UUID-PK-NOT-NULL; email:varchar-UNIQUE-NOT-NULL-indexed-lowercase-normalized; displayName:varchar-NOT-NULL-2-to-100-chars; createdAt:timestamptz-NOT-NULL-DEFAULT-now; updatedAt:timestamptz-NOT-NULL-auto-updated; lastLoginAt:timestamptz-NULLABLE; roles:varchar[]-NOT-NULL-DEFAULT-['user']-not-enforced|M|P0|
|2|DM-002|AuthToken data model|Transport struct returned by auth endpoints; refreshToken persisted to Redis with 7-day TTL, accessToken not persisted.|Redis+JwtService|DM-001|accessToken:JWT-NOT-NULL-RS256-signed-payload-userid+roles; refreshToken:opaque-string-NOT-NULL-unique-7day-TTL-redis; expiresIn:number-NOT-NULL-always-900s; tokenType:string-NOT-NULL-always-Bearer-OAuth2-compat|S|P0|
|3|COMP-009|UserRepo module|PostgreSQL-backed repository providing CRUD + upsert against UserProfile; used by AuthService.|UserRepo|DM-001|findByEmail returns single UserProfile or null; insert enforces email uniqueness via DB constraint; upsert idempotent; parameterized queries only (no string concat)|M|P0|
|4|COMP-010|RefreshTokenStore module|Redis-backed store for hashed refresh tokens with 7-day TTL.|RefreshTokenStore|DM-002|store(userId,hash,ttl) sets key with TTL; verify(userId,token) returns bool; revoke(userId,token) deletes key; list(userId) returns active tokens|M|P0|
|5|COMP-011|AuditLogRepo module|PostgreSQL-backed audit log writer; 90-day retention; fields per NFR-COMPLIANCE-002.|AuditLogRepo|DM-001|write(event) persists: user_id:UUID-nullable; event_type:varchar-NOT-NULL; timestamp:timestamptz-NOT-NULL; ip:inet-NOT-NULL; outcome:varchar-NOT-NULL; retention:90-days; queryable by date-range + user_id|M|P0|
|6|MIG-SCHEMA-001|Initial PostgreSQL migration|Flyway/Liquibase migration applying DM-001 + audit log table + indexes to staging then prod.|PostgreSQL|DM-001, COMP-011|migration runs to completion in <30s; rollback script tested; idempotent; version-controlled|S|P0|
|7|INFRA-PG-001|PostgreSQL 15 provisioning|Stand up PG cluster with connection pool (100), TLS in transit, daily backup, 7-day PITR.|PostgreSQL|—|cluster up with 1 primary + 1 read replica; TLS verified; backup+restore tested; pool connects from AuthService namespace|M|P0|
|8|INFRA-REDIS-001|Redis 7 provisioning|Stand up Redis 7 cluster with 1GB memory, TLS in transit, password auth, daily RDB snapshot.|Redis|—|cluster up with persistence; TLS verified; access from AuthService namespace only; snapshot restore tested|M|P0|
|9|NFR-COMPLIANCE-004|Data minimization schema review|Review DM-001 fields against GDPR minimization principle; document rationale for each PII field.|UserRepo|DM-001|only email+password-hash+displayName+roles+timestamps persisted; no phone/address/DOB; written rationale committed to repo|S|P0|
|10|FR-AUTH-002-DB|Email uniqueness + normalization|Enforce lowercase normalization on insert + unique btree index on email.|UserRepo|DM-001|INSERT with mixed-case email is stored lowercase; duplicate insert raises constraint violation; index used by EXPLAIN on findByEmail|S|P0|
|11|OPS-BACKUP-001|Backup + restore procedure|Document and rehearse PG backup + Redis RDB restore; referenced by rollback MIG-009.|PostgreSQL+Redis|INFRA-PG-001, INFRA-REDIS-001|restore drill completes <30 min; document linked from runbooks|S|P1|
|12|COMP-KEYSTORE-001|RSA key material provisioning|Generate 2048-bit RSA key pair; mount into secrets volume; document quarterly rotation.|JwtService|—|key pair generated offline; public key readable by JwtService; rotation runbook drafted; key ID header set|M|P0|

### Integration Points — M1

|Artifact|Type|Wired|M|Consumed By|
|---|---|---|---|---|
|UserRepo DI binding|Dependency injection|Register UserRepo as singleton in service container|M1|AuthService (M2)|
|RefreshTokenStore DI binding|Dependency injection|Register RefreshTokenStore keyed to Redis client|M1|TokenManager (M2)|
|AuditLogRepo DI binding|Dependency injection|Register AuditLogRepo singleton|M1|AuthService, API middleware (M2/M3)|
|PostgreSQL connection pool|Shared resource|Config wiring with 100-connection pool|M1|UserRepo, AuditLogRepo|
|Redis client|Shared resource|Config wiring with TLS + auth|M1|RefreshTokenStore|
|Migration runner|Build step|Hooked into CI deploy pipeline|M1|All future schema changes|
|Secrets volume (RSA keys)|Mount|K8s secret → pod volume at `/secrets/jwt/`|M1|JwtService (M2)|

### Milestone Dependencies — M1

- PostgreSQL 15 infrastructure must be available before INFRA-PG-001 begins.
- Redis 7 infrastructure must be available before INFRA-REDIS-001 begins.
- OQ-002 resolution must precede DM-001 finalization.

### Open Questions — M1

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-002|What is the maximum allowed UserProfile.roles array length?|Blocks DM-001 schema freeze and COMP-011 audit log shape.|auth-team|2026-04-01|

### Risk Assessment and Mitigation — M1

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|UserProfile schema revision after M2 begins|Medium|Medium|Rework of repo + AuthService code paths|Freeze DM-001 at end of M1; gate with architect review|architect|
|2|Redis provisioning delay|Medium|Low|Blocks TokenManager (M2) and refresh flows|Provision Redis in parallel with PG; use managed Redis as fallback|platform-team|
|3|Audit log table growth exceeds capacity|Low|Medium|Storage cost, query slowdown|90-day retention + monthly partition; archive to cold storage|platform-team|

## M2: Core Auth Components

**Objective:** Build the four backend components (PasswordHasher, JwtService, TokenManager, AuthService) that implement FR-AUTH-001..005 and the mandated security NFRs. | **Duration:** 2 weeks (Week 3–4) | **Entry:** M1 exit signed off; SendGrid provisioned; OQ-PRD-003 lockout policy confirmed; RSA keys mounted. | **Exit:** all four components pass unit tests; AuthService orchestrates all five FR flows end-to-end against staging DB; bcrypt cost factor and RS256 signing verified by tests.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|COMP-008|PasswordHasher component|Backend bcrypt abstraction with cost factor 12; abstracts algorithm for future migration.|PasswordHasher|—|hash(password) returns bcrypt hash; verify(password,hash) returns bool; cost factor 12 asserted in unit test; benchmarked ~300ms/hash; no raw password logged|M|P0|
|2|NFR-SEC-001|bcrypt cost factor 12 enforced|Configuration + test enforcing bcrypt cost 12 on all hashes.|PasswordHasher|COMP-008|config value readable at runtime; unit test asserts cost parameter == 12; rejects config with cost <10 at startup|S|P0|
|3|NFR-COMPLIANCE-003|NIST SP 800-63B password hashing compliance|Validate one-way adaptive hashing; audit code paths for raw password exposure.|PasswordHasher|COMP-008|no raw password crosses process boundary except into hash(); logs scrub password fields; code review sign-off from security|S|P0|
|4|COMP-PW-STRENGTH|Password strength validator|Validator enforcing ≥8 chars, ≥1 uppercase, ≥1 number; reused by registration + reset-confirm.|PasswordHasher|—|returns violations for each unmet rule; blocks weak passwords; shared between FR-AUTH-002 and FR-AUTH-005|S|P0|
|5|COMP-007|JwtService component|Backend JWT sign/verify using RS256 with 2048-bit RSA keys; 5-second clock-skew tolerance.|JwtService|COMP-KEYSTORE-001|sign(payload) returns RS256 JWT with kid header; verify(token) validates sig + exp + nbf ± 5s skew; rejects non-RS256 alg; supports key rotation via kid lookup|M|P0|
|6|NFR-SEC-002|RS256 signing with 2048-bit RSA|Enforce RS256 + 2048-bit RSA keys via configuration test.|JwtService|COMP-007|config test rejects keys <2048 bits; only RS256 alg accepted; key ID tracked per issued token|S|P0|
|7|COMP-KEYROT|Quarterly RSA key rotation procedure|Runbook + tooling to rotate RSA keypair without breaking in-flight tokens.|JwtService|COMP-KEYSTORE-001|old key retained for grace period (access token TTL); kid header drives verify key lookup; rotation smoke-tested in staging|M|P1|
|8|COMP-006|TokenManager component|Backend token lifecycle manager — issue, revoke, refresh; stores hashed refresh tokens in Redis 7-day TTL.|TokenManager|COMP-007, COMP-010|issueTokens(userId,roles) returns AuthToken with accessToken+refreshToken; refresh(refreshToken) revokes old + issues new pair; revoke(refreshToken) deletes from Redis; expired tokens return 401; revoked tokens return 401|L|P0|
|9|COMP-005|AuthService orchestrator|Backend orchestrator exposing login/register/profile/refresh/reset flows; delegates to PasswordHasher, TokenManager, UserRepo, AuditLogRepo, SendGrid.|AuthService|COMP-006, COMP-008, COMP-009, COMP-011|login(email,pw) returns AuthToken or raises on invalid; register(email,pw,name) creates UserProfile + logs event; refresh delegates to TokenManager; getProfile(userId) returns UserProfile; reset-request + reset-confirm wire SendGrid|XL|P0|
|10|FR-AUTH-001|Login with email and password|AuthService.login validates bcrypt hash via PasswordHasher + issues AuthToken via TokenManager.|AuthService|COMP-005, COMP-008, COMP-006|valid creds return 200 + AuthToken; invalid creds return 401; non-existent email returns 401 (no enumeration); 5 failures in 15 min triggers lockout; audit event written|M|P0|
|11|FR-AUTH-002|User registration with validation|AuthService.register with email uniqueness, password strength, UserProfile creation.|AuthService|COMP-005, COMP-009, COMP-PW-STRENGTH|valid registration returns 201 + UserProfile; duplicate email returns 409; weak password (<8 chars/no uppercase/no number) returns 400; bcrypt cost 12 used; GDPR consent recorded|M|P0|
|12|FR-AUTH-003|JWT issuance and refresh|TokenManager issues accessToken (15 min) + refreshToken (7 day) via JwtService; supports silent refresh.|TokenManager|COMP-006, COMP-007|login returns both tokens with correct TTLs; POST /auth/refresh with valid refresh returns new pair; expired refresh returns 401; revoked refresh returns 401|L|P0|
|13|FR-AUTH-004|User profile retrieval|AuthService.getProfile returns UserProfile via userId from validated JWT.|AuthService|COMP-005, COMP-007|valid accessToken returns UserProfile with id+email+displayName+createdAt+updatedAt+lastLoginAt+roles; expired/invalid token returns 401|M|P0|
|14|FR-AUTH-005|Password reset flow|Two-step reset: reset-request (SendGrid email with 1-hr token) + reset-confirm (validate + update hash).|AuthService|COMP-005, COMP-008, SendGrid|reset-request with valid email sends email via SendGrid; reset-confirm with valid token updates hash; tokens expire after 1hr; used tokens cannot be reused; all sessions invalidated on confirm (per PRD AC)|L|P0|
|15|COMP-LOCKOUT|Account lockout logic|Track failed login attempts in Redis; lock after 5 failures in 15-min window.|AuthService|COMP-005, Redis|counter increments per failed attempt; window is sliding 15-min; 5th failure returns 423 Locked; lockout TTL configurable; audit event written on lock|M|P0|
|16|NFR-COMPLIANCE-001|GDPR consent at registration|Consent checkbox required at registration; consent record written to audit log with timestamp.|AuthService|COMP-005, COMP-011|register without consent=true returns 400; consent recorded with user_id + timestamp; consent timestamp returned in UserProfile queries for admin|S|P0|
|17|COMP-SENDGRID|SendGrid email integration|SendGrid SDK wired into AuthService for password-reset delivery; template for reset email.|AuthService|SendGrid|reset email delivered within 60s; template includes 1-hr-expiry link; delivery failures retried 3x with exponential backoff; failures trigger alert|M|P0|

### Integration Points — M2

|Artifact|Type|Wired|M|Consumed By|
|---|---|---|---|---|
|AuthService DI binding|Dependency injection|Register AuthService singleton with Password/Jwt/Token/Repo deps|M2|API controllers (M3)|
|TokenManager DI binding|Dependency injection|Register TokenManager keyed to JwtService + RefreshTokenStore|M2|AuthService, refresh endpoint (M3)|
|JwtService DI binding|Dependency injection|Register JwtService reading key material from secrets volume|M2|TokenManager, JWT middleware (M3)|
|PasswordHasher DI binding|Dependency injection|Register PasswordHasher with cost=12 config|M2|AuthService|
|Lockout Redis client|Shared resource|Separate keyspace from refresh tokens (prefix `lockout:`)|M2|AuthService lockout path|
|SendGrid client|External SDK|Init with API key from secret; template ID in config|M2|AuthService reset-request|
|Audit event dispatcher|Event bus|AuthService emits events → AuditLogRepo.write|M2|AuditLogRepo (M1)|

### Milestone Dependencies — M2

- M1 exit (DM-001, DM-002, all repos, infra) must be complete.
- SendGrid API key and sending domain must be provisioned by platform-team before COMP-SENDGRID.
- OQ-PRD-003 (lockout threshold) must be resolved before COMP-LOCKOUT finalizes configuration.

### Open Questions — M2

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-PRD-001|Should password reset emails be sent synchronously or asynchronously?|Determines FR-AUTH-005 latency and COMP-SENDGRID queuing design.|Engineering|2026-04-20|
|2|OQ-PRD-002|Maximum refresh tokens allowed per user across devices?|Determines TokenManager issuance cap and Redis storage sizing.|Product|2026-04-20|
|3|OQ-PRD-003|Account lockout policy — is 5 attempts / 15 min the final number?|Finalizes COMP-LOCKOUT thresholds and FR-AUTH-001 AC.|Security|2026-04-20|

### Risk Assessment and Mitigation — M2

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-PRD-002 Security breach from implementation flaws|Critical|Low|Token forgery, data exposure, compliance failure|Dedicated security review before M3; static analysis on COMP-005..008; pentest in M5|security-team|
|2|R-001 Token theft via XSS|High|Medium|Session hijack, user impersonation|refreshToken in HttpOnly cookie; accessToken in memory only; 15-min access TTL; AuthProvider clears on tab close (M4)|security-team|
|3|R-002 Brute-force attacks on login|Medium|Medium|Account compromise|COMP-LOCKOUT 5/15; bcrypt cost 12 slows attacker; rate limit at gateway (M3); CAPTCHA after 3 failures|security-team|
|4|R-PRD-004 Email delivery failures block password reset|Medium|Medium|Users cannot recover accounts|COMP-SENDGRID retry with backoff; delivery monitoring + alert; fallback support channel documented|platform-team|
|5|bcrypt cost 12 exceeds 500ms on low-tier hardware|Medium|Low|Login latency regression|Benchmark on prod-equivalent hardware; HPA scale-out; ADR for cost factor choice|architect|

## M3: API Layer and Gateway

**Objective:** Expose AuthService via six versioned REST endpoints behind API Gateway with rate limiting, error envelope, and observability; add admin audit log query + explicit logout endpoints to close PRD JTBD gaps. | **Duration:** 2 weeks (Week 5–6) | **Entry:** M2 exit; API Gateway provisioned; TLS 1.3 certs available; CORS whitelist confirmed. | **Exit:** all six contract endpoints pass contract tests; rate limits verified via synthetic traffic; p95 < 200ms on happy path; admin query endpoint returns filtered audit log.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|API-001|POST /v1/auth/login|Authenticates user and returns AuthToken. Rate limit 10/min per IP. No auth required.|API-Gateway+AuthService|COMP-005, FR-AUTH-001|request `{email,password}`; 200 returns AuthToken (accessToken,refreshToken,expiresIn=900,tokenType=Bearer); 401 invalid creds; 423 account locked; 429 rate limit; audit event written|M|P0|
|2|API-002|POST /v1/auth/register|Creates UserProfile and returns it. Rate limit 5/min per IP. No auth required.|API-Gateway+AuthService|COMP-005, FR-AUTH-002|request `{email,password,displayName,consent}`; 201 returns full UserProfile; 400 validation (weak pw/invalid email/missing consent); 409 email conflict; audit event written|M|P0|
|3|API-003|GET /v1/auth/me|Returns authenticated user's UserProfile. Rate limit 60/min per user. Bearer auth.|API-Gateway+AuthService|COMP-005, FR-AUTH-004|header `Authorization: Bearer <jwt>`; 200 returns UserProfile; 401 missing/expired/invalid token|S|P0|
|4|API-004|POST /v1/auth/refresh|Exchanges refresh token for new AuthToken pair; old refresh revoked. Rate limit 30/min per user.|API-Gateway+TokenManager|COMP-006, FR-AUTH-003|request `{refreshToken}`; 200 returns new AuthToken; 401 expired/revoked refresh; old refresh token invalidated atomically|M|P0|
|5|API-005|POST /v1/auth/reset-request|Sends password-reset email with 1-hour token. Response 200 regardless of email existence (no enumeration).|API-Gateway+AuthService|COMP-005, FR-AUTH-005, COMP-SENDGRID|request `{email}`; always 200 in <500ms; email sent only if user exists; audit event written; enumeration test passes|S|P0|
|6|API-006|POST /v1/auth/reset-confirm|Completes password reset; invalidates all sessions on success.|API-Gateway+AuthService|COMP-005, FR-AUTH-005, COMP-006|request `{resetToken,newPassword}`; 200 on success; 400 expired/used token; password strength validated; all refresh tokens for user revoked; audit event written|M|P0|
|7|API-007|POST /v1/auth/logout|Explicit logout endpoint; revokes current refresh token. Covers PRD user story "log out on shared device".|API-Gateway+TokenManager|COMP-006|request with Bearer access + `{refreshToken}` in body; 204 on success; refresh token deleted from Redis; audit event written|S|P0|
|8|API-008|GET /v1/admin/auth/events|Admin-only audit log query endpoint. Closes JTBD gap for Jordan persona.|API-Gateway+AuditLogRepo|COMP-011, NFR-COMPLIANCE-002|Bearer admin role required; filter by user_id + date-range; returns paged event list with user_id+event_type+timestamp+ip+outcome; 403 for non-admin|L|P0|
|9|COMP-ERROR-ENVELOPE|Canonical error envelope middleware|Middleware wrapping all responses into `{error:{code,message,status}}` shape with AUTH_* codes.|API-Gateway|—|all 4xx/5xx responses include code field (AUTH_INVALID_CREDS, AUTH_LOCKED, AUTH_TOKEN_EXPIRED, etc.); documented in API contract; enforced via middleware|M|P0|
|10|COMP-API-VERSION|URL-prefix API versioning|Route prefix `/v1/auth/*` enforced; non-versioned requests return 404.|API-Gateway|—|all six endpoints mounted under /v1/; non-prefixed returns 404; gateway config committed|S|P0|
|11|COMP-RATE-LIMIT|Gateway rate limiting policies|Per-route + per-IP + per-user rate limit rules wired at API Gateway.|API-Gateway|COMP-API-VERSION|login:10/min/IP; register:5/min/IP; refresh:30/min/user; me:60/min/user; returns 429 on breach; tested via synthetic client|M|P0|
|12|COMP-CORS|CORS restriction|CORS middleware allowing only known frontend origins.|API-Gateway|—|whitelist configured; unknown origin blocked with 403; credentials mode supported for HttpOnly cookies|S|P0|
|13|COMP-TLS13|TLS 1.3 enforcement|API Gateway terminates TLS 1.3 only; HSTS header set.|API-Gateway|—|TLS 1.2 and below rejected; HSTS max-age 1yr includeSubDomains; cert chain valid; cipher suite audit passes|S|P0|
|14|COMP-JWT-MW|JWT auth middleware|Middleware validating Bearer token via JwtService on protected routes.|API-Gateway+JwtService|COMP-007|decodes Authorization header; calls JwtService.verify; attaches userId+roles to request context; 401 on failure; 5s skew tolerance|M|P0|
|15|NFR-PERF-001|API response time p95 < 200ms|Instrument and measure p95 on all auth endpoints; optimize hot paths.|API-Gateway+AuthService|API-001..006|APM tracing shows p95 < 200ms on login/register/refresh/me in staging; slow query log empty; histogram metric exposed|M|P0|
|16|COMP-OTEL|OpenTelemetry tracing|Spans across AuthService → PasswordHasher → TokenManager → JwtService; context propagation.|AuthService+OTEL|COMP-005|trace ID returned in X-Trace-Id response header; spans visible in Tempo/Jaeger; errors marked; tested across four components|M|P1|

### Integration Points — M3

|Artifact|Type|Wired|M|Consumed By|
|---|---|---|---|---|
|JWT middleware chain|Middleware|Mounted on /v1/auth/me, /v1/auth/logout, /v1/admin/*|M3|API-003, API-007, API-008|
|Error envelope middleware|Middleware|Mounted globally; overrides default error handler|M3|All API endpoints|
|Rate limit policies|Gateway config|Declarative policy per route|M3|API-001..008|
|CORS middleware|Middleware|Mounted before auth middleware|M3|All API endpoints|
|Route registry|Dispatch table|Maps /v1/auth/<op> → controller method|M3|API-001..008 controllers|
|OpenTelemetry exporter|Observability|Config wiring to OTLP collector|M3|OPS-007 (M6)|
|Admin role check|Authorization strategy|Middleware reading roles claim from JWT|M3|API-008|

### Milestone Dependencies — M3

- M2 exit: AuthService + TokenManager + JwtService operational and covered by unit tests.
- API Gateway product/infra must be available (dependency #7 in extraction).
- CORS whitelist from product/frontend must be confirmed before COMP-CORS.

### Open Questions — M3

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-001|Should AuthService support API key authentication for service-to-service calls?|Deferred to v1.1; could add API-00X row if confirmed in scope.|test-lead|2026-04-15|
|2|GAP-JTBD-ADMIN|PRD Jordan JTBD "view authentication event logs" — gap-fill API-008 added; confirm admin auth model.|Validates coverage of Jordan persona; resolution determines whether RBAC enforcement is needed in v1.0 (TDD says roles stored but not enforced).|product-team|2026-04-25|

### Risk Assessment and Mitigation — M3

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Rate limit too aggressive blocks legitimate users|Medium|Medium|Registration conversion drops below 60% target|Start with documented limits; monitor 429 rate in Beta; tunable via gateway config without code deploy|product-team|
|2|CORS misconfiguration blocks frontend|Medium|Medium|Login flow broken in production|Staging mirror of prod CORS list; smoke test origins before GA; config validated in CI|platform-team|
|3|Admin audit endpoint (API-008) exposes PII without authz|High|Low|GDPR + SOC2 violation|Admin role middleware on route; pentest includes this endpoint; audit of role claim enforcement|security-team|
|4|User enumeration via timing/response differences on API-005|High|Low|Security disclosure|Constant-time response path; 200 always returned; timing audit in M5|security-team|

## M4: Frontend Auth Experience

**Objective:** Deliver the React client surface — AuthProvider context, login/register/profile pages, password-reset flow UI — with silent refresh and HttpOnly-cookie-safe token handling. | **Duration:** 1 week (Week 7) | **Entry:** M3 exit; frontend routing framework available; CORS whitelist includes frontend origin. | **Exit:** all four primary pages render + submit successfully against staging; silent refresh works across tab-switch; logout clears in-memory token and cookie.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|COMP-004|AuthProvider React context|Manages AuthToken state + silent refresh via TokenManager semantics; intercepts 401s; redirects to LoginPage.|AuthProvider|COMP-005,COMP-006,API-001,API-003,API-004|props `{children}`; exposes `{user,login,logout,refresh,isAuthenticated}`; accessToken in memory only; refreshToken in HttpOnly cookie; 401 triggers refresh attempt; silent refresh schedules before exp; unmount clears state|L|P0|
|2|COMP-001|LoginPage|Frontend Route/Page at /login. Email/password form; submits to API-001; stores AuthToken via AuthProvider.|LoginPage|COMP-004,API-001|props `{onSuccess,redirectUrl?}`; renders email+password fields; inline validation; submit calls AuthProvider.login; success redirects to redirectUrl; failure shows generic "Invalid email or password"; no user enumeration|M|P0|
|3|COMP-002|RegisterPage|Frontend Route/Page at /register. Registration form; client-side password strength; GDPR consent checkbox; calls API-002.|RegisterPage|COMP-004,API-002,NFR-COMPLIANCE-001|props `{onSuccess,termsUrl}`; fields email+password+displayName+consent; password strength meter (≥8/1 upper/1 number); consent required to submit; 409 duplicate shows "email already registered"; success logs in immediately|M|P0|
|4|COMP-003|ProfilePage|Frontend Route/Page at /profile. Displays UserProfile via GET /auth/me.|ProfilePage|COMP-004,API-003|auth required; displays displayName+email+createdAt; loading + error states; uses AuthProvider.user; page renders <1s|S|P0|
|5|COMP-FORGOT-PW|ForgotPasswordPage|Page handling password-reset request flow.|ForgotPasswordPage|COMP-004,API-005|route /forgot-password; email input; on submit calls API-005; always shows same confirmation ("If this email is registered, a reset link has been sent."); no enumeration|S|P0|
|6|COMP-RESET-CONFIRM|ResetConfirmPage|Page completing the reset flow from the emailed link.|ResetConfirmPage|COMP-004,API-006|route /reset-confirm?token=...; newPassword + confirm fields with strength meter; calls API-006; success redirects to login with success banner; 400 (expired/used) shows request-new-link CTA|M|P0|
|7|COMP-LOGOUT-UI|Logout control|Button/menu item invoking AuthProvider.logout → API-007.|AuthProvider|COMP-004,API-007|visible when isAuthenticated; click calls API-007; clears in-memory accessToken + HttpOnly cookie; redirects to landing page; confirms on shared-device user story|S|P0|
|8|COMP-SILENT-REFRESH|Silent refresh scheduler|Timer in AuthProvider that refreshes accessToken before exp using refresh cookie.|AuthProvider|COMP-004,API-004|schedules refresh 1 min before accessToken exp; pauses when tab hidden; resumes on visibility; handles race via single-flight; test covers 15-min continuous session|M|P0|
|9|COMP-INLINE-VALIDATION|Inline form validation|Shared validation UI for email + password strength.|shared-ui|COMP-PW-STRENGTH|email regex check on blur; password rules rendered as checklist (≥8/1 upper/1 number); submit disabled until valid; ARIA labels for accessibility|S|P1|

### Integration Points — M4

|Artifact|Type|Wired|M|Consumed By|
|---|---|---|---|---|
|AuthProvider context|React context|Wrapped around App root|M4|All protected routes, LoginPage, RegisterPage|
|401 interceptor|HTTP client middleware|Axios/fetch interceptor chained in AuthProvider|M4|All authenticated API calls|
|Public/protected route guards|React Router|PublicRoutes vs ProtectedRoutes trees|M4|LoginPage, RegisterPage (public); ProfilePage (protected)|
|HttpOnly cookie handling|Browser contract|Fetch with credentials: include|M4|API-004, API-007|
|Silent refresh timer|Event scheduler|setTimeout driven by JWT exp|M4|AuthProvider|

### Milestone Dependencies — M4

- M3 exit: all API endpoints available on staging; CORS includes frontend origin.
- Design system tokens and form primitives must be available (inherited from platform).

### Open Questions — M4

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-PRD-004|Support "remember me" to extend session duration?|Affects AuthProvider + refresh cookie TTL; deferred to v1.1 unless product decides otherwise.|Product|2026-05-10|

### Risk Assessment and Mitigation — M4

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-PRD-001 Low registration adoption from poor UX|Medium|Medium|Below 60% conversion target|Usability testing on RegisterPage before GA; A/B strength-meter variants; inline validation; analytics on funnel|product-team|
|2|Silent refresh race condition|Medium|Medium|Users logged out mid-action|Single-flight refresh; queue pending requests until refresh completes; test covers concurrent 401s|frontend-team|
|3|accessToken leakage via console or dev tools|High|Low|Token theft|Keep in closure scope; no localStorage/sessionStorage; audit via code review; include in security review (M5)|security-team|

## M5: Testing, Security and Compliance

**Objective:** Execute the testing pyramid (unit/integration/E2E), load testing, security review, pentest, and compliance validation (SOC2, GDPR, NIST) before rollout begins. | **Duration:** 2 weeks (Week 8–9) | **Entry:** M4 exit; full auth flow operational in staging; test infrastructure ready (Jest, Supertest, Playwright, testcontainers, k6). | **Exit:** unit 80% / integration 15% / E2E 5% coverage met; load test passes 500 concurrent + p95 < 200ms; pentest report with zero P0/P1 findings; SOC2 + GDPR + NIST sign-off.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|TEST-001|Unit — login with valid credentials returns AuthToken|Validates FR-AUTH-001. AuthService.login calls PasswordHasher.verify → TokenManager.issueTokens → returns AuthToken.|Jest|COMP-005,COMP-008,COMP-006|test passes; asserts accessToken + refreshToken present; expiresIn=900; tokenType=Bearer; mocks of Password/Token collaborators verified|S|P0|
|2|TEST-002|Unit — login with invalid credentials returns error|Validates FR-AUTH-001. AuthService.login returns 401 when PasswordHasher.verify returns false; no AuthToken.|Jest|COMP-005,COMP-008|401 status; no token issued; audit event emitted; no user enumeration in error message|S|P0|
|3|TEST-003|Unit — token refresh with valid refresh token|Validates FR-AUTH-003. TokenManager.refresh validates, revokes old, issues new AuthToken via JwtService.|Jest|COMP-006,COMP-007|new AuthToken returned; old refresh deleted from Redis; new refresh stored; idempotent on replay (second attempt fails)|S|P0|
|4|TEST-004|Integration — registration persists UserProfile to database|Validates FR-AUTH-002. Full flow: API → PasswordHasher → PostgreSQL insert.|Supertest+testcontainers|API-002,COMP-005,DM-001|POST /v1/auth/register with valid body returns 201; DB row exists with lowercase email + bcrypt hash; duplicate email returns 409|M|P0|
|5|TEST-005|Integration — expired refresh token rejected by TokenManager|Validates FR-AUTH-003. Redis TTL expiration correctly invalidates refresh tokens.|Supertest+testcontainers|API-004,COMP-006|fast-forward Redis TTL; POST /v1/auth/refresh returns 401; audit event emitted; no new AuthToken issued|M|P0|
|6|TEST-006|E2E — user registers and logs in|Validates FR-AUTH-001 + FR-AUTH-002. Complete journey: RegisterPage → LoginPage → ProfilePage via AuthProvider.|Playwright|COMP-001,COMP-002,COMP-003,COMP-004|fresh user registers; redirected in to dashboard; logs out; logs back in; ProfilePage shows correct data; all in <5s wall clock|L|P0|
|7|TEST-LOCKOUT|Integration — account lockout after 5 failures|Validates FR-AUTH-001 AC. 5 failed logins in 15 min → 423 Locked.|Supertest+testcontainers|COMP-LOCKOUT,API-001|6th attempt returns 423 within 15-min window; lockout clears after window; audit events for each attempt + lock|M|P0|
|8|TEST-RESET|E2E — password reset flow|Validates FR-AUTH-005. reset-request → email → reset-confirm → new-password login.|Playwright+MailCatcher|API-005,API-006,COMP-FORGOT-PW,COMP-RESET-CONFIRM|reset email arrives <60s; link valid 1hr; new password logs in; old refresh tokens revoked; used token rejected|L|P0|
|9|NFR-PERF-002|Load test 500 concurrent logins|k6 load test validating concurrency target.|k6|API-001,NFR-PERF-001|500 VUs for 5 min; error rate <0.1%; p95 < 200ms; no Redis connection failures; HPA stays <70% CPU|M|P0|
|10|NFR-COMPLIANCE-002|SOC2 audit logging validation|Verify all auth events logged with user_id + timestamp + IP + outcome; 12-month retention plan.|AuditLogRepo|COMP-011,API-001..007|every login/register/refresh/reset/logout emits audit row; 12-month retention policy documented; log scrubbing test confirms no password/token content|M|P0|
|11|SEC-REVIEW|Security review + pentest|Dedicated security review of COMP-005..008; pentest against staging; OWASP Top 10 checklist.|security-team|All M2-M4 deliverables|pentest report issued; zero P0/P1 findings; all P2 findings triaged; sign-off from security lead|XL|P0|
|12|SEC-TIMING|Timing-attack audit|Audit API-001 and API-005 for timing-side-channel leakage (user enumeration).|security-team|API-001,API-005|response-time distribution of known vs unknown email indistinguishable within 10%; tested with 1000-sample comparison|M|P0|

### Integration Points — M5

|Artifact|Type|Wired|M|Consumed By|
|---|---|---|---|---|
|Test DB container|testcontainer|Spawned per test suite|M5|TEST-004, TEST-005, TEST-LOCKOUT|
|Test Redis container|testcontainer|Spawned per test suite|M5|TEST-005, TEST-LOCKOUT|
|k6 load test script|Script|Invoked by CI on M5 gate|M5|NFR-PERF-002|
|Playwright runner|E2E harness|CI browser matrix|M5|TEST-006, TEST-RESET|
|MailCatcher integration|Test email|Captures reset emails for Playwright|M5|TEST-RESET|

### Milestone Dependencies — M5

- M4 exit: full auth surface deployed to staging.
- k6 and Playwright tooling provisioned.
- SendGrid sandbox / MailCatcher configured for reset-flow testing.

### Open Questions — M5

_No open questions._

### Risk Assessment and Mitigation — M5

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-PRD-003 Compliance failure from incomplete audit logging|High|Medium|SOC2 audit fails in Q3|Validate log fields vs SOC2 control catalog in NFR-COMPLIANCE-002; sample audit query by compliance reviewer; fix gaps before GA|compliance-team|
|2|R-PRD-002 Security breach from implementation flaws (late discovery)|Critical|Low|P0 security bug delays GA|Full pentest + threat modeling in M5; remediation buffer week if needed; incident response plan ready|security-team|
|3|Load test reveals p95 regression|Medium|Medium|Misses NFR-PERF-001 target|Profile hot paths; tune bcrypt cost on low-tier hardware; add Redis pipelining; optimize JWT verify caching|architect|
|4|E2E flakiness blocks CI|Medium|High|GA decision delayed|Playwright retry policy; deterministic seed data; MailCatcher instead of real SendGrid in tests|qa-team|

## M6: Rollout and Operations

**Objective:** Execute three-phase rollout (Internal Alpha → Beta 10% → GA 100%) with two feature flags, observability, alerts, runbooks, capacity plans, and rollback procedure. | **Duration:** 3 weeks (Week 10–12) | **Entry:** M5 exit with pentest sign-off, SOC2 audit log validated, k6 target met. | **Exit:** AUTH_NEW_LOGIN removed at GA; 99.9% uptime over first 7 days post-GA; all dashboards green; post-mortem template ready; legacy endpoints deprecated.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|MIG-001|Phase 1: Internal Alpha|1 week. Deploy AuthService to staging; auth-team + QA test all endpoints; LoginPage/RegisterPage behind AUTH_NEW_LOGIN.|Deployment|M5 exit|FR-AUTH-001..005 pass manual test; zero P0/P1 bugs open; traffic from auth-team + QA only; exit gate signed by test-lead|L|P0|
|2|MIG-002|Phase 2: Beta (10% traffic)|2 weeks. Enable AUTH_NEW_LOGIN for 10% of traffic; monitor latency, error rates, Redis usage; AuthProvider refresh under real load.|Deployment|MIG-001|p95 < 200ms sustained; error rate <0.1%; zero Redis connection failures; HPA behavior within projected range; exit gate signed by architect + platform-team|L|P0|
|3|MIG-003|Phase 3: General Availability (100%)|1 week. Remove AUTH_NEW_LOGIN; deprecate legacy endpoints; AUTH_TOKEN_REFRESH enabled.|Deployment|MIG-002|100% traffic on new AuthService; legacy auth endpoints return 410 Gone or redirect; 99.9% uptime over first 7 days; all dashboards green|M|P0|
|4|MIG-004|Feature flag AUTH_NEW_LOGIN|Gates new LoginPage + AuthService login. Default OFF. Owner: auth-team.|FeatureFlag|—|flag created in flag service; default OFF; toggleable per-% or per-cohort; cleanup ticket filed for post-MIG-003 removal|S|P0|
|5|MIG-005|Feature flag AUTH_TOKEN_REFRESH|Enables refresh-token flow in TokenManager; when OFF, access-only. Default OFF. Owner: auth-team.|FeatureFlag|—|flag created in flag service; default OFF; toggleable per-cohort; cleanup ticket filed for MIG-003+2 weeks removal|S|P0|
|6|MIG-006|Rollback step 1 — disable AUTH_NEW_LOGIN|Flip AUTH_NEW_LOGIN off; route traffic to legacy auth.|Deployment|MIG-004|flag toggle completes <30s; traffic shift observed on dashboard; synthetic login against legacy passes|S|P0|
|7|MIG-007|Rollback step 2 — verify legacy login via smoke tests|Run pre-scripted smoke tests against legacy auth endpoints to confirm health.|Deployment|MIG-006|smoke suite passes within 2 min; posted to incident channel; no 5xx on legacy|S|P0|
|8|MIG-008|Rollback step 3 — investigate AuthService root cause|Pull structured logs + OTEL traces; identify failure mode.|Deployment|OPS-007|root-cause hypothesis documented within 30 min of rollback; log + trace IDs captured in incident ticket|M|P0|
|9|MIG-009|Rollback step 4 — restore UserProfile from backup|If UserProfile data corruption detected, restore from last known-good backup.|PostgreSQL|OPS-BACKUP-001|restore completes <30 min; row counts match baseline; data integrity verified via checksum sample|M|P0|
|10|MIG-010|Rollback step 5 — notify auth-team + platform-team|Page on-call channels with incident summary + rollback status.|OnCall|OPS-003|auth-team + platform-team paged within 5 min; incident channel created; stakeholder list notified (product, support)|S|P0|
|11|MIG-011|Rollback step 6 — post-mortem within 48 hours|Author post-mortem doc covering what/why/how/prevent.|Process|MIG-006..010|post-mortem published <48h of rollback; action items assigned; circulated to engineering + product|S|P1|
|12|MIG-ROLLBACK-TRIGGERS|Rollback trigger thresholds|Codify triggers: p95>1000ms for 5 min; error rate >5% for 2 min; Redis connection failures >10/min; any UserProfile data corruption.|Alerts|OPS-008|thresholds encoded as alerting rules; alert test fires below threshold; runbook links from each alert|S|P0|
|13|OPS-001|Runbook: AuthService down|Symptoms: 5xx on /auth/*; LoginPage/RegisterPage error state. Diagnosis + resolution + escalation.|Runbook|—|runbook linked from pager alert; steps cover K8s pod health + PG + Redis checks; escalation auth-team → platform-team at 15 min; rehearsed in game day|S|P0|
|14|OPS-002|Runbook: Token refresh failures|Symptoms: users logged out; AuthProvider redirect loop; auth_token_refresh_total error spike. Diagnosis + resolution + escalation.|Runbook|COMP-006,COMP-010|runbook linked from alert; covers Redis connectivity, JwtService key access, AUTH_TOKEN_REFRESH flag state; rehearsed in game day|S|P0|
|15|OPS-003|On-call expectations|P1 ack ≤15 min; auth-team 24/7 rotation for first 2 weeks post-GA; tooling doc; escalation path.|OnCall|—|rotation schedule published; tools verified (K8s, Grafana, Redis CLI, PG admin); escalation path documented: auth-team → test-lead → eng-manager → platform-team|M|P0|
|16|OPS-004|Capacity: AuthService pods|3 replicas baseline; HPA to 10 at CPU>70%. Expected 500 concurrent users.|Capacity|INFRA-PG-001,INFRA-REDIS-001|HPA configured + tested; 3-replica baseline deployed; scale-out tested to 10 under synthetic load; pod startup <30s|M|P0|
|17|OPS-005|Capacity: PostgreSQL|Current 100 pool; ~50 avg concurrent queries. Scale pool to 200 if wait time >50ms.|Capacity|INFRA-PG-001|pool metric exposed; wait-time alert at 50ms; scale-up runbook documented; connection leak test passes|M|P0|
|18|OPS-006|Capacity: Redis|Current 1 GB; ~100K refresh tokens (~50 MB). Scale to 2 GB at >70% utilization.|Capacity|INFRA-REDIS-001|memory metric exposed; scale-up alert at 70%; eviction policy configured (noeviction for refresh key space); capacity plan documented|S|P0|
|19|OPS-007|Observability: logs + metrics + traces|Structured logs for login/register/refresh/reset; Prometheus metrics (auth_login_total, auth_login_duration_seconds, auth_token_refresh_total, auth_registration_total); OTEL spans.|Observability|COMP-OTEL|Grafana dashboards live; log search includes event types; OTEL spans visible for full AuthService→PasswordHasher→TokenManager→JwtService chain; no PII in logs|L|P0|
|20|OPS-008|Alerts|Login failure rate >20% over 5 min; p95 latency >500ms; TokenManager Redis connection failures. Sensitive fields excluded from logs.|Alerts|OPS-007|alert rules deployed; thresholds verified via synthetic failure; PagerDuty routing to auth-team; log scrubbing test passes for password/token fields|M|P0|
|21|NFR-REL-001|Service availability 99.9% uptime|Measured over 30-day rolling windows via health check endpoint.|Observability|OPS-007,OPS-008|health endpoint returns 200 with DB+Redis status; uptime tracked in SLO dashboard; error budget policy documented; 99.9% target met first 30 days post-GA|M|P0|
|22|OPS-DEPRECATE-LEGACY|Legacy endpoint deprecation|Return 410 Gone or redirect on legacy auth endpoints post-MIG-003.|API-Gateway|MIG-003|legacy /login and /register return 410; redirect added for known clients; deprecation notice shipped to integrators; removed from codebase at MIG-003+30 days|S|P1|

### Integration Points — M6

|Artifact|Type|Wired|M|Consumed By|
|---|---|---|---|---|
|Feature flag service|External dispatch|AUTH_NEW_LOGIN + AUTH_TOKEN_REFRESH registered; gateway + AuthService read|M6|MIG-001..003|
|Prometheus scrape config|Observability|ServiceMonitor for AuthService pods|M6|OPS-007, OPS-008, NFR-REL-001|
|PagerDuty integration|Alerting|Routing key per alert severity → auth-team on-call|M6|OPS-008|
|Grafana dashboards|Observability|Dashboard JSON committed to repo|M6|OPS-007|
|Runbook links|Alert annotation|runbook_url field attached to every alert rule|M6|OPS-001, OPS-002|
|HPA|K8s|HorizontalPodAutoscaler yaml committed|M6|OPS-004|
|SLO/error-budget policy|Process|Published to platform handbook|M6|NFR-REL-001|

### Milestone Dependencies — M6

- M5 exit: pentest clean, SOC2 audit-log validation signed off, k6 load test passes.
- Feature flag service must be operational.
- PagerDuty + Grafana tenants provisioned for auth-team.

### Open Questions — M6

_No open questions._

### Risk Assessment and Mitigation — M6

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-003 Data loss during migration|High|Low|User lockout; support surge; data integrity incident|Parallel legacy + new run MIG-001..002; idempotent upsert; full backup before each phase; rehearsed restore (OPS-BACKUP-001); rollback steps MIG-006..011|platform-team|
|2|Beta 10% traffic reveals p95 regression|Medium|Medium|GA delayed|Rollback to legacy via AUTH_NEW_LOGIN; profile + fix; re-ramp after validation|architect|
|3|Flag lag between gateway + AuthService causes inconsistent routing|Medium|Low|Some users hit new, some legacy|Both layers read same flag source with short TTL; flag toggle monitored with smoke test; rollback procedure unchanged|platform-team|
|4|Legacy deprecation breaks external integrations|Medium|Medium|Customer support tickets; churn|Deprecation notice 30 days before removal; 410 responses include migration doc link; Sam persona integration docs updated|product-team|
|5|On-call fatigue post-GA|Low|Medium|Missed alerts, slow response|24/7 rotation first 2 weeks only; de-escalate to business-hours after stability proven; alert tuning sprint in week 3|auth-team|

## Resource Requirements and Dependencies

### External Dependencies

|Dependency|Required By M|Status|Fallback|
|---|---|---|---|
|PostgreSQL 15+|M1|Provisioned|Managed PG (AWS RDS / Cloud SQL); 7-day PITR restore|
|Redis 7+|M1|Provisioned|Managed Redis (AWS ElastiCache / Memorystore); RDB snapshot restore|
|Node.js 20 LTS runtime|M1|Available|Node 18 LTS acceptable short-term; upgrade path documented|
|bcryptjs library|M2|Available|Native bcrypt (Node binding) as perf fallback; algorithm abstraction in PasswordHasher|
|jsonwebtoken library|M2|Available|jose library as TypeScript-native alternative|
|SendGrid API|M2|To provision|Amazon SES fallback documented; reset flow delivered via support channel if both fail|
|API Gateway|M3|Available|Manual nginx + rate-limit module as interim; roles of TLS/CORS unchanged|
|Frontend routing framework|M4|Available|—|
|Feature flag service|M6|To verify|Env-variable-based toggle as interim; requires restart to flip (degraded)|
|Prometheus + Grafana|M6|Available|—|
|PagerDuty|M6|Available|Opsgenie as fallback routing|
|k6 load testing tool|M5|To provision|Artillery as fallback|
|Playwright|M5|Available|—|
|testcontainers (PG + Redis)|M5|Available|docker-compose fixtures as fallback|
|MailCatcher / SendGrid sandbox|M5|To provision|Filesystem-capture SMTP stub as fallback|
|RSA key material (2048-bit)|M2|Must generate|—|

### Infrastructure Requirements

- PostgreSQL 15 primary + 1 read replica; 100-connection pool (scale to 200 if wait >50ms); daily backup + 7-day PITR; TLS in transit.
- Redis 7 cluster (1 GB baseline → 2 GB at 70% utilization); TLS in transit; password auth; daily RDB snapshot.
- Kubernetes namespace for AuthService with 3 baseline replicas; HPA to 10 at CPU >70%; secrets volume for RSA keys.
- API Gateway with TLS 1.3 termination, HSTS, CORS whitelist, per-route rate limit rules.
- OpenTelemetry collector + Tempo/Jaeger trace storage; Prometheus ServiceMonitor; Grafana dashboards.
- PagerDuty service routing to auth-team on-call; Opsgenie fallback.
- Feature flag service supporting per-% + per-cohort targeting.
- SendGrid account with verified sending domain; API key in K8s secret.

## Risk Register

|ID|Risk|Affected Milestones|Probability|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|R-001|Token theft via XSS|M2, M4|Medium|High|accessToken in memory only; refreshToken in HttpOnly cookie; 15-min access TTL; AuthProvider clears on tab close; force password reset on confirmed theft|security-team|
|R-002|Brute-force attacks on login|M2, M3|Medium|Medium|COMP-LOCKOUT 5/15 min; bcrypt cost 12; gateway rate limit 10/min per IP; CAPTCHA after 3 failures (future); WAF IP block contingency|security-team|
|R-003|Data loss during migration|M6|Low|High|Parallel legacy + new in MIG-001..002; idempotent upsert; full backup before each phase; rehearsed restore; rollback MIG-006..011|platform-team|
|R-PRD-001|Low registration adoption from poor UX|M4, M6|Medium|High|Usability testing pre-launch; funnel analytics on RegisterPage; inline validation; A/B test strength meter; iterate based on conversion|product-team|
|R-PRD-002|Security breach from implementation flaws|M2, M3, M5|Low|Critical|Dedicated security review; SAST + pentest in M5; threat model; remediation buffer; incident response plan|security-team|
|R-PRD-003|Compliance failure from incomplete audit logging|M1, M3, M5, M6|Medium|High|Define log requirements in M1 (COMP-011); validate vs SOC2 controls in NFR-COMPLIANCE-002 (M5); sample audit query signed off by compliance|compliance-team|
|R-PRD-004|Email delivery failures block password reset|M2, M5, M6|Medium|Medium|SendGrid retry with exponential backoff; delivery monitoring + alert; fallback support channel; Amazon SES failover documented|platform-team|
|R-M1-SCHEMA|UserProfile schema revision after M2 begins|M1, M2|Medium|Medium|Freeze DM-001 at end of M1; gate with architect review; OQ-002 must resolve before freeze|architect|
|R-M3-RATELIMIT|Rate limits block legitimate users|M3, M6|Medium|Medium|Monitor 429 rate in Beta; tunable via gateway config without code deploy|product-team|
|R-M3-ADMIN-PII|Admin audit endpoint exposes PII without authz|M3, M5|Low|High|Admin role middleware; pentest scope includes API-008; audit of role claim enforcement|security-team|
|R-M3-ENUM|User enumeration via timing on API-005|M3, M5|Low|High|Constant-time response path; 200 always returned; timing audit SEC-TIMING in M5|security-team|
|R-M4-REFRESH|Silent refresh race condition|M4|Medium|Medium|Single-flight refresh; queued pending requests; concurrent 401 test|frontend-team|
|R-M5-LOAD|Load test reveals p95 regression|M5, M6|Medium|Medium|Profile hot paths; tune bcrypt cost; Redis pipelining; JWT verify caching|architect|
|R-M6-FLAGLAG|Flag lag between gateway + AuthService|M6|Low|Medium|Short TTL + monitored; smoke test on each toggle; rollback unchanged|platform-team|
|R-M6-DEPRECATE|Legacy deprecation breaks external integrations|M6|Medium|Medium|30-day deprecation notice; 410 Gone with migration link; Sam persona integration doc updated|product-team|

## Success Criteria and Validation Approach

|Criterion|Metric|Target|Validation Method|M|
|---|---|---|---|---|
|Login response time p95|HTTP latency on POST /v1/auth/login|< 200ms|APM tracing + k6 load test|M3, M5|
|Registration success rate|Successful POST /v1/auth/register / total attempts|> 99%|Analytics funnel + Grafana dashboard|M4, M6|
|Token refresh latency p95|HTTP latency on POST /v1/auth/refresh|< 100ms|APM tracing|M3, M5|
|Service availability|Uptime over 30-day rolling window|99.9%|Health check endpoint + SLO dashboard|M6|
|Password hash time|bcrypt hash duration|< 500ms (cost 12)|Unit-test benchmark on prod-equivalent hardware|M2, M5|
|User registration conversion|Landing → register → confirmed|> 60%|Product analytics funnel|M4, M6|
|Daily active authenticated users|Unique logged-in users/day|> 1000 within 30 days of GA|AuditLogRepo query aggregated daily|M6|
|Average session duration|Time between first login and last refresh/logout|> 30 min|Token refresh event analytics|M6|
|Failed login rate|Failed logins / total login attempts|< 5%|Auth event log analysis (auth_login_total labels)|M5, M6|
|Password reset completion|reset-request → reset-confirm successful|> 80%|Funnel analytics|M5, M6|
|Pentest findings|P0/P1 security findings at end of M5|0|Security review report|M5|
|SOC2 audit log coverage|Proportion of auth events logged with required fields|100%|Compliance sample query + control catalog|M5, M6|

## Decision Summary

|Decision|Chosen|Alternatives Considered|Rationale|
|---|---|---|---|
|Token architecture|JWT access (15 min, RS256) + opaque Redis refresh (7 day, hashed)|Stateful sessions; JWT-only long-lived|Extraction mandates stateless API (Architectural Constraints); 15-min access + HttpOnly refresh cookie directly mitigates R-001 per NFR-SEC-002|
|Password hashing|bcrypt cost factor 12|argon2; scrypt|NFR-SEC-001 + NFR-COMPLIANCE-003 explicitly mandate bcrypt cost 12; ~300ms benchmark within <500ms target|
|Persistence split|PostgreSQL 15 for UserProfile + audit log; Redis 7 for refresh tokens|All-in-PG; all-in-Redis|Extraction Architectural Constraints mandate both; 90-day audit log retention is relational query workload, refresh tokens are ephemeral with TTL|
|API versioning|URL prefix `/v1/auth/*`|Header-based; query param|Extraction Architectural Constraints specify URL prefix; simpler for gateway routing and CDN caching|
|Rollout strategy|3-phase (Alpha → Beta 10% → GA) with two flags|Big bang; canary on one pod|Extraction Migration Plan specifies this approach; mitigates R-003 by keeping parallel legacy during Phase 1-2|
|Lockout mechanism|5 attempts / 15 min sliding window|IP-based only; CAPTCHA-first|FR-AUTH-001 AC #4 specifies 5/15; extensible to CAPTCHA after 3 failures per R-002 contingency; OQ-PRD-003 may adjust threshold|
|OAuth / MFA / RBAC in v1.0|Deferred|Ship MFA v1.0; ship OAuth v1.0|PRD Scope Definition explicitly lists as Out of Scope; complexity score 0.68 assumes narrow scope|
|Admin audit endpoint|Added API-008 as gap-fill|Defer to v1.1|PRD Jordan JTBD + story AUTH-E3 require "view authentication event logs"; TDD omission flagged as gap-fill in M3|
|Silent refresh implementation|Timer-based pre-emptive refresh (1 min before exp)|Lazy refresh on 401; server-sent event push|Lazy-on-401 introduces UX jank; SSE is over-engineered; timer approach aligns with PRD UX "invisible when it works"|
|Feature flag strategy|Two flags (AUTH_NEW_LOGIN, AUTH_TOKEN_REFRESH)|Single flag; no flags|Extraction Migration Plan specifies both; separates ramp from refresh-flow toggle for independent rollback|
|Admin role enforcement|Middleware read-only check on API-008|Full RBAC engine|PRD Scope excludes RBAC enforcement; middleware is minimum viable to protect API-008 without introducing full role system|

## Timeline Estimates

|M|Duration|Start|End|Key Milestones|
|---|---|---|---|---|
|M1|2 weeks|Week 1|Week 2|DM-001/DM-002 frozen; PG + Redis provisioned; repos tested; RSA keys mounted|
|M2|2 weeks|Week 3|Week 4|PasswordHasher + JwtService + TokenManager + AuthService pass unit tests; SendGrid wired; lockout functional|
|M3|2 weeks|Week 5|Week 6|All six API endpoints (+ API-007 logout + API-008 admin audit) passing contract tests; rate limits verified|
|M4|1 week|Week 7|Week 7|AuthProvider + four pages + reset flow + logout control deployed to staging; silent refresh validated|
|M5|2 weeks|Week 8|Week 9|Unit/integration/E2E coverage met; k6 500-concurrent pass; pentest P0/P1 = 0; SOC2 audit log signed off|
|M6|3 weeks|Week 10|Week 12|MIG-001 Alpha (Week 10) → MIG-002 Beta 10% (Weeks 10–11) → MIG-003 GA 100% (Week 12); 99.9% uptime first 7 days post-GA|

**Total estimated duration:** 12 weeks

