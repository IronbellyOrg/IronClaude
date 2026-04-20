<!-- CONV: AuthService=THS, PasswordHasher=PSS, TokenManager=TKN, password=PA1, UserProfile=SRP, AuthProvider=THP, PostgreSQL=PST, security=SCR, Integration=NTG, JwtService=JWT, Mitigation=MTG, registration=RGS, SendGrid=SND, Frontend=FRN, rotation=RTT, compliance=CMP, validation=VLD, AUTH_NEW_LOGIN=ANL, FR-AUTH-001=FA0, Dependencies=DPN -->
---
spec_source: "test-tdd-user-auth.compressed.md"
complexity_score: 0.68
complexity_class: MEDIUM
primary_persona: architect
adversarial: false
base_variant: "none"
variant_scores: "none"
convergence_score: none
---

# User Authentication Service — Project Roadmap

## Executive Summary

The User Authentication Service establishes the platform's identity layer, unblocking the entire Q2–Q3 2026 personalization roadmap and satisfying the Q3 2026 SOC2 Type II audit requirement. Scope is narrow (email/PA1 auth, JWT + Redis refresh, self-service PA1 reset) with explicit exclusions for OAuth, MFA, and RBAC enforcement. Architecture mandates a stateless REST service (Node.js 20 LTS) fronted by an API Gateway, backed by PST 15 for `SRP` persistence and Redis 7 for refresh tokens, with RS256-signed JWTs produced by a dedicated `JWT` and bcrypt (cost 12) PA1 hashing via `PSS`. Rollout follows a three-phase feature-flag gated path (internal alpha → 10% beta → GA) with parallel-legacy safety net. This roadmap sequences milestones by architectural layer — foundations first (data and crypto primitives), then core services, then user-facing flows and CMP — to keep the blast radius of each integration small and each milestone independently shippable.

**Business Impact:** Unblocks ≈$2.4M projected annual personalization revenue; enables Q3 2026 SOC2 Type II audit pass; targets >60% RGS conversion, <200ms p95 login, 99.9% availability, >30-minute avg session, >80% PA1-reset completion.

**Complexity:** MEDIUM (0.68) — 14 requirements across 7 domains, 8 components, 4 external integrations (PST, Redis, SND, API Gateway); inherently SCR-sensitive (auth-critical surface with XSS, brute-force, and token-theft risk), but deliberately narrow scope (no OAuth/MFA in v1.0) keeps integration surface bounded.

**Critical path:** DM-001/DM-002 schemas → `PSS` + `JWT` primitives → `TKN` + `THS` orchestrator → API surface (API-001..006) → `THP` + frontend pages → CMP/audit logging → phased rollout (MIG-001..003) → GA.

**Key architectural decisions:**

- **Stateless JWT with Redis-backed refresh (RS256, 15-min access / 7-day refresh):** avoids server-side session affinity, supports horizontal scaling of `THS` pods, and enables silent refresh for Sam the API consumer. Alternative (server sessions) rejected on scalability and API-consumer ergonomics.
- **bcrypt cost 12 in a dedicated `PSS` abstraction:** NIST SP 800-63B compliant; ≈300ms hash time (inside the 500ms target). Abstraction keeps a future algorithm migration (e.g., argon2id) localized to one component.
- **Three-phase, feature-flag-gated rollout with parallel legacy (`ANL`, `AUTH_TOKEN_REFRESH`):** bounds blast radius of the auth cutover; enables rollback in minutes rather than redeploys.
- **URL-prefix API versioning (`/v1/auth/*`):** deterministic contract for Sam; breaking changes require a major bump so client SDKs do not silently break.
- **No OAuth, MFA, or RBAC enforcement in v1.0:** roles stored on `SRP` but not enforced; scope boundary explicitly guarded so the SOC2 deadline is not jeopardized by scope creep.

**Open risks requiring resolution before M1:**

- OQ-PRD-003 — final account-lockout threshold must be frozen before `THS` login logic is implemented (current assumption: 5 attempts / 15 min).
- OQ-PRD-001 — synchronous vs asynchronous PA1-reset email delivery must be decided before MIG-001 rollout so OPS-008 alert thresholds are correct.
- R-PRD-002 — SCR review scope and pentest vendor must be booked at M1 kickoff to avoid blocking M5 exit.

## Milestone Summary

|ID|Title|Type|Priority|Effort|DPN|Deliverables|Risk|
|---|---|---|---|---|---|---|---|
|M1|Foundations — Data Models, Infra, Crypto Primitives|Foundation|P0|M|—|14|Medium|
|M2|Core Auth Service — Login, Registration, Token Lifecycle|Core|P0|L|M1|17|High|
|M3|Password Reset and Email NTG|Core|P0|M|M2|10|Medium|
|M4|FRN NTG — Auth UI and Provider|UI|P0|M|M2, M3|11|Medium|
|M5|Testing, Performance, and Security Validation|Quality|P0|L|M2, M3, M4|16|High|
|M6|Compliance, Audit Logging, and Observability|Compliance|P0|M|M2, M3|14|High|
|M7|Phased Rollout and Operational Readiness|Release|P0|M|M5, M6|18|High|

## Dependency Graph

```
M1 (Foundations: DM-001, DM-002, COMP-007 JwtService, COMP-008 PasswordHasher, PG/Redis/Gateway)
  ↓
M2 (Core Auth: COMP-005 AuthService, COMP-006 TokenManager, FR-AUTH-001..003, API-001..004)
  ↓                    ↓
M3 (Reset: FR-AUTH-004, FR-AUTH-005, API-005, API-006, SendGrid)
                       ↓
M4 (Frontend: COMP-001..004 LoginPage/RegisterPage/ProfilePage/AuthProvider)
                       ↓                 ↓
M5 (Validation: TEST-001..006, NFR-SEC-001/002, NFR-PERF-001/002, security review, pentest)
                                         ↓
M6 (Compliance: NFR-COMPLIANCE-001..004, OPS-007/008, audit log schema, admin read-API)
                                         ↓
M7 (Rollout: MIG-001..011, OPS-001..006, GA signoff)

External integrations wired across M1→M7:
  PostgreSQL 15 ── M1 schema ── M2 UserRepo ── M6 audit log ── M7 capacity (OPS-005)
  Redis 7 ─────── M1 cluster ── M2 TokenManager ── M7 capacity (OPS-006)
  SendGrid ────── M3 provider integration ── M7 delivery monitoring (R-PRD-004)
  API Gateway ─── M1 TLS/CORS ── M2 rate limits ── M7 prod cutover
```

## M1: Foundations — Data Models, Infra, Crypto Primitives

**Objective:** Stand up the data, infrastructure, and cryptographic primitives on which every auth flow depends | **Duration:** Weeks 1–2 | **Entry:** Node.js 20 LTS, PG 15, Redis 7 provisioned; SEC-POLICY-001 reviewed; OQ-PRD-003 resolved | **Exit:** DM-001/DM-002 migrations applied in staging; `PSS` and `JWT` pass unit tests; API Gateway terminates TLS 1.3 with CORS allowlist

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|DM-001|`SRP` schema + PST migration|Create `user_profiles` table with all fields and constraints from extraction; enforce email uniqueness via index; default roles|PST|—|id:UUID-PK-NOT-NULL; email:string-UNIQUE-NOT-NULL-indexed-lowercase-normalized; displayName:string-NOT-NULL-2-to-100-chars; createdAt:ISO8601-NOT-NULL-DEFAULT-now(); updatedAt:ISO8601-NOT-NULL-auto-updated; lastLoginAt:ISO8601-NULLABLE; roles:string[]-NOT-NULL-DEFAULT-["user"]-not-enforced; migration idempotent; relationships: 1:N refresh-tokens(Redis), 1:N audit-log(PG-90day)|M|P0|
|2|DM-002|`AuthToken` storage model (Redis + JWT payload)|Define Redis key schema for refresh tokens with 7-day TTL; document JWT claim schema; hashed refresh-token storage|Redis, JWT|DM-001|accessToken:JWT-NOT-NULL-RS256-signed-payload-user-id-plus-roles; refreshToken:opaque-string-NOT-NULL-unique-7day-TTL-in-Redis-stored-hashed; expiresIn:number-NOT-NULL-always-900-seconds; tokenType:string-NOT-NULL-always-"Bearer"-OAuth2-compat; Redis key pattern `rt:{userId}:{tokenId}`; audit-log PG 90-day retention|S|P0|
|3|COMP-008|`PSS` component|Implement bcrypt abstraction with cost factor 12; interface hides algorithm choice for future migration|bcryptjs|—|hash() and verify() methods; cost=12; benchmark < 500ms/hash; algorithm abstracted behind interface; no plaintext logging|S|P0|
|4|COMP-007|`JWT` component|Implement RS256 sign/verify with 2048-bit RSA keys; 5s clock-skew tolerance; secret-volume mounting|jsonwebtoken|—|sign() produces RS256 JWT; verify() accepts 5s skew; keys loaded from mounted secrets volume; quarterly RTT hook documented; invalid signature returns explicit error|M|P0|
|5|NFR-SEC-001|bcrypt cost factor 12 mandate|Codify cost factor 12 as configuration with unit-test assertion; block deploy if cost < 12|COMP-008|3|unit test asserts bcrypt cost parameter == 12; config VLD on service boot; deploy script fails if value overridden below 12|S|P0|
|6|NFR-SEC-002|RS256 + 2048-bit RSA key mandate|Codify RS256 + 2048-bit RSA; config test asserts key size and algorithm|COMP-007|4|configuration test asserts algorithm == RS256 and key length ≥ 2048 bits; key files restricted to service principal; keys committed via secrets manager, never in repo|S|P0|
|7|INFRA-PG|PST 15 cluster provision|Provision PG 15 primary + read replica; enable point-in-time recovery; baseline backup|PST|—|PG 15.x running; replica lag < 1s; nightly backup + PITR 7-day retention; connection pool limit 100 (baseline per OPS-005)|M|P0|
|8|INFRA-REDIS|Redis 7 cluster provision|Provision Redis 7 with 1 GB baseline capacity and persistence enabled|Redis|—|Redis 7.x running; AOF persistence on; RDB snapshot every 15 min; 1 GB allocated; TLS in transit|S|P0|
|9|INFRA-NODE|Node.js 20 LTS service runtime baseline|Standardize runtime, package manager, and service boot scaffolding|Node.js|—|Node 20.x LTS pinned via `.nvmrc`; service boots with structured logging; health endpoint at `/healthz`|S|P0|
|10|INFRA-GW|API Gateway TLS and CORS baseline|Configure TLS 1.3 termination and CORS allowlist at gateway for `/v1/auth/*`|API Gateway|—|TLS 1.3 enforced; weak ciphers disabled; CORS allowlist restricted to known frontend origins; HTTP → HTTPS redirect|S|P0|
|11|INFRA-SECRETS|Secrets management and RSA key generation|Generate and store initial RSA-2048 keypair in secrets manager; document quarterly RTT|Secrets mgr|4|keypair generated; stored in secrets manager with restricted IAM; RTT runbook references quarterly cadence; no key material in repo or logs|S|P0|
|12|INFRA-AUDIT|Audit log table schema (foundation)|Create `auth_audit_log` table for per-event records with 90-day retention policy stub; details populated in M6|PST|1|columns: id, user_id, event_type, timestamp, ip, outcome; indexed by user_id and timestamp; retention job scaffold|S|P1|
|13|COMP-REPO|`UserRepo` data-access component|Encapsulate `SRP` CRUD and email-uniqueness enforcement; used by `THS`|PST|1|findByEmail(); insert() throws on email conflict; updateLastLoginAt(); unit tests cover unique-constraint path|S|P0|
|14|DECISION-HASH|Decision record: bcrypt v argon2id|Document chosen algorithm, cost 12 rationale, and future-migration plan behind `PSS`|ADR|3|ADR committed; lists NIST SP 800-63B reference; enumerates rollforward path to argon2id via same interface|S|P1|

### NTG Points — M1

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|`PSS`|DI component|Registered in DI container at service boot (M1)|M1|`THS` (M2), `PasswordReset` (M3)|
|`JWT`|DI component|Registered in DI container; RSA key loaded from secrets volume|M1|`TKN` (M2), middleware auth-verify (M2)|
|`UserRepo`|DI component|Registered with PG connection-pool dependency|M1|`THS` (M2), profile handlers (M2), audit writer (M6)|
|API Gateway|Middleware chain|TLS/CORS rules deployed as gateway config|M1|All API-001..006 (M2, M3)|
|Secrets volume|K8s mount|`JWT` reads from `/var/run/secrets/jwt/*`|M1|`JWT` (M1→M7)|

### Milestone DPN — M1

- External: PST 15, Redis 7, Node.js 20 LTS runtimes available.
- Policy: SEC-POLICY-001 (PA1 + token SCR) reviewed and signed off.
- Decisions: OQ-PRD-003 (account lockout threshold) resolved so FA0 lockout AC is stable before M2.

### Open Questions — M1

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-PRD-003|Account lockout policy after N consecutive failed attempts — is 5 the final number?|Blocks DM-001 constraint wording and THS login logic; drives lockout duration and alerting thresholds|Security|End of Week 1|
|2|OQ-002|What is the maximum allowed `SRP` roles array length?|Shapes DM-001 constraint and JWT payload size; affects NFR-SEC-002 token bloat risk|auth-team|2026-04-01|

### Risk Assessment and MTG — M1

|#|Risk|Severity|Likelihood|Impact|MTG|Owner|
|---|---|---|---|---|---|---|
|1|RSA key material leak or weak generation|Critical|Low|Full token forgery; forces emergency RTT|Generate in HSM-backed secrets manager; restrict IAM; RTT runbook; no keys in repo|SCR|
|2|Bcrypt cost chosen too high → login latency bust|High|Low|p95 > 200ms NFR-PERF-001 miss|Benchmark cost 12 on target pod size pre-M2; unit test asserts cost=12 not ≥12|backend|
|3|DM-001 migration applied incorrectly to prod-like env|High|Medium|Blocks all downstream milestones|Migration idempotency tests; apply to staging first; backup before run|platform|
|4|Redis provisioned with insufficient persistence|Medium|Low|Refresh tokens vanish on node restart; mass logouts|AOF + RDB both enabled; staging restart drill|platform|

## M2: Core Auth Service — Login, Registration, Token Lifecycle

**Objective:** Implement the backend authentication orchestrator, token lifecycle, and first four API endpoints | **Duration:** Weeks 3–4 | **Entry:** M1 foundations complete; OQ-PRD-003 and OQ-PRD-002 resolved | **Exit:** FA0, FR-AUTH-002, FR-AUTH-003 pass unit + integration tests; API-001..004 return documented status codes; account lockout enforced

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|COMP-005|`THS` orchestrator|Backend orchestrator exposing login/register/profile/refresh; delegates to `PSS`, `TKN`, `UserRepo`|THS|COMP-008, COMP-007, COMP-REPO|exposes login(), register(), getProfile(), refresh(); dependencies injected; unit tests cover success + failure paths; no direct DB access outside `UserRepo`|L|P0|
|2|COMP-006|`TKN` lifecycle component|Issue/revoke/refresh; store hashed refresh tokens in Redis with 7-day TTL|TKN|COMP-007, INFRA-REDIS|issueTokens(userId) → AuthToken pair; revoke(refreshToken) removes from Redis; refresh() validates → revokes old → issues new; refresh token hashed before Redis write|L|P0|
|3|FA0|Login with email/PA1|`THS.login()` validates credentials via `PSS.verify()`; returns `AuthToken`; enforces lockout|THS|1, 2, COMP-008|valid → 200 + AuthToken(access+refresh); invalid → 401 generic; non-existent email → 401 (no enumeration); 5 failed attempts within 15 min → account locked; lastLoginAt updated on success|L|P0|
|4|FR-AUTH-002|User RGS with VLD|`THS.register()` enforces email uniqueness, PA1 strength, creates `SRP`; writes via `UserRepo`; hashes via `PSS`|THS|1, COMP-REPO, COMP-008|valid → 201 + SRP; duplicate email → 409; weak PA1 (<8 chars, no uppercase, no number) → 400; bcrypt cost 12 used; roles default ["user"]|M|P0|
|5|FR-AUTH-003|JWT issuance + silent refresh|`TKN` issues 15-min access + 7-day refresh; refresh endpoint returns new pair with RTT|TKN|2, COMP-007|login returns both tokens; POST /auth/refresh with valid refresh → new AuthToken pair; expired refresh → 401; revoked refresh → 401; old refresh invalidated on RTT|M|P0|
|6|API-001|POST `/auth/login`|HTTP handler: request VLD, rate limit (10/min/IP), call `THS.login()`, envelope errors|API Gateway, THS|3|auth none; rate 10/min/IP; request `{email, PA1}`; 200 AuthToken(expiresIn=900, tokenType="Bearer"); 401 invalid; 423 account locked; 429 rate limit; error envelope `{error:{code:"AUTH_*",message,status}}`|M|P0|
|7|API-002|POST `/auth/register`|HTTP handler: request VLD, rate limit (5/min/IP), call `THS.register()`|API Gateway, THS|4|auth none; rate 5/min/IP; request `{email, PA1, displayName}`; 201 full SRP; 400 weak PA1/invalid email; 409 email conflict|M|P0|
|8|API-003|GET `/auth/me`|HTTP handler: JWT middleware verify, return authenticated `SRP`|API Gateway, THS|COMP-007, COMP-REPO|auth Bearer access; rate 60/min/user; 200 SRP(id, email, displayName, createdAt, updatedAt, lastLoginAt, roles); 401 missing/expired/invalid|S|P0|
|9|API-004|POST `/auth/refresh`|HTTP handler for token RTT; rate-limited per user|API Gateway, TKN|5|auth refresh in body; rate 30/min/user; request `{refreshToken}`; 200 new AuthToken; 401 expired/revoked; old refresh token revoked before new issued|M|P0|
|10|FR-AUTH-004|Authenticated profile retrieval|Return `SRP` including id, email, displayName, timestamps, roles for authenticated user|THS|8|GET /auth/me with valid access → SRP; expired/invalid → 401; response includes id, email, displayName, createdAt, updatedAt, lastLoginAt, roles|S|P0|
|11|COMP-MW-AUTH|JWT-verify middleware|Request-scoped middleware that verifies Bearer tokens via `JWT` and injects user context|Express middleware|COMP-007|rejects missing/expired/invalid with 401; injects userId + roles into request context; exempts public routes (login, register, reset-*)|S|P0|
|12|COMP-MW-RATELIMIT|Rate limit wiring at API Gateway|Apply endpoint-specific rate limits per extraction|API Gateway|INFRA-GW|login 10/min/IP; register 5/min/IP; refresh 30/min/user; me 60/min/user; 429 with envelope error|S|P0|
|13|COMP-LOCKOUT|Account-lockout tracker|Track failed attempts in Redis with sliding 15-min window; lock for cooldown period|Redis|INFRA-REDIS, 3|5 failures within 15 min → account locked; lock expires after policy-defined window; counter resets on successful login; lock surfaced as 423 by API-001|S|P0|
|14|R-002-MIT|Brute-force mitigation wiring|Combine rate limit + lockout + bcrypt cost; add WAF/CAPTCHA hooks described as contingency|API Gateway, THS|6, 12, 13|API Gateway 10/min/IP; 5-attempt lockout active; bcrypt cost 12; WAF rule + CAPTCHA hook documented as contingency playbook|S|P0|
|15|COMP-ERR-ENV|Shared error envelope helper|Centralize `{error:{code,message,status}}` envelope; enforce AUTH_* error codes|THS|—|all AUTH endpoints return envelope on non-2xx; codes: AUTH_INVALID_CREDENTIALS, AUTH_RATE_LIMITED, AUTH_LOCKED, AUTH_TOKEN_EXPIRED, AUTH_TOKEN_INVALID; tested via contract tests|S|P1|
|16|COMP-VERSION|URL-prefix versioning `/v1/auth/*`|Mount all endpoints under `/v1/auth/*`; document breaking-change policy|API Gateway|INFRA-GW|all auth endpoints served at `/v1/auth/*`; non-versioned aliases return 404; policy doc committed requiring major bump on breaking change|S|P1|
|17|DECISION-SESSION|Decision record: stateless JWT vs server session|Document rationale for stateless JWT + Redis refresh over server-side sessions|ADR|—|ADR committed; lists scalability, Sam-persona ergonomics, horizontal-scaling rationale; alternatives (server sessions, DB-backed sessions) scored|S|P1|

### NTG Points — M2

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|`THS`|DI orchestrator|Registered in DI container; injected into HTTP handlers|M2|API-001..004 handlers, M3 reset handlers, M4 frontend|
|`TKN`|DI service|Injected into `THS`; uses `JWT` + Redis client|M2|`THS` (M2), `THP` refresh loop (M4)|
|JWT-verify middleware|Express middleware chain|Mounted on protected `/v1/auth/*` routes|M2|API-003, M3 reset-confirm, M6 admin routes|
|Rate-limit rules|Gateway config|Deployed per-endpoint|M2|API-001..004 (M2), API-005..006 (M3)|
|Error-envelope helper|DI utility|Injected into all handlers|M2|All auth endpoints M2→M7|
|Account-lockout counter|Redis strategy|Called from `THS.login()` failure path|M2|API-001 (M2), admin unlock (M6)|

### Milestone DPN — M2

- M1 complete: `PSS`, `JWT`, `UserRepo`, PG/Redis/Gateway baselines.
- OQ-PRD-003 resolved (lockout threshold) before COMP-LOCKOUT is implemented.
- OQ-PRD-002 decision informs refresh-token-per-user cap configured in `TKN`.

### Open Questions — M2

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-PRD-002|Maximum refresh tokens allowed per user across devices?|Shapes `TKN` storage strategy, Redis key layout, and revocation-on-cap policy|Product|End of Week 3|
|2|OQ-PRD-004|Support "remember me" to extend session duration?|Affects AuthToken schema and refresh-TTL logic in `TKN`; defer to v1.1 if negative|Product|End of Week 3|

### Risk Assessment and MTG — M2

|#|Risk|Severity|Likelihood|Impact|MTG|Owner|
|---|---|---|---|---|---|---|
|1|User enumeration via differential 401 behavior|High|Medium|Attacker can confirm account existence, enables targeted phishing|Identical 401 response for non-existent email and wrong PA1; identical response-time profile; contract test enforces|backend|
|2|Refresh token replay|High|Medium|Stolen refresh grants persistent access|Rotation on every refresh; old refresh revoked before new issued; hashed storage in Redis; tie token to user+deviceId where possible|backend|
|3|Brute-force on login|Medium|High|Credential stuffing success|Gateway rate limit 10/min/IP + 5-attempt lockout + bcrypt cost 12; WAF/CAPTCHA contingency documented|SCR|
|4|Lockout misconfig locks all legit users|High|Low|Service unavailable for real users|Staged rollout of lockout policy; admin-unlock tooling in M6; alert when lockout-rate spikes|backend|

## M3: Password Reset and Email NTG

**Objective:** Implement the two-step self-service PA1 reset flow and integrate SND delivery | **Duration:** Weeks 5–6 | **Entry:** M2 complete; SND API key provisioned; OQ-PRD-001 resolved | **Exit:** FR-AUTH-005 passes integration tests end-to-end; API-005/API-006 return non-enumerating responses; reset tokens expire at 1 hour; used tokens cannot be reused; sessions invalidated on PA1 change

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-AUTH-005|Password reset flow (two-step)|`THS` supports request (email + token) and confirm (token VLD + PA1 update via `PSS`)|THS|COMP-005, COMP-008|POST /auth/reset-request with valid email → token emailed; POST /auth/reset-confirm with valid token → PA1 updated via PSS; reset tokens expire after 1 hour; used tokens cannot be reused; all existing sessions invalidated on confirm|L|P0|
|2|API-005|POST `/auth/reset-request`|HTTP handler; sends PA1-reset email with 1-hour token; always returns 200 to prevent enumeration|API Gateway, THS|1|auth none; request `{email}`; 200 regardless of email existence (no enumeration); identical latency on existent vs non-existent email; rate-limited to prevent abuse|M|P0|
|3|API-006|POST `/auth/reset-confirm`|HTTP handler; validates token, updates PA1, invalidates all sessions|API Gateway, THS|1|auth reset token in body; request `{resetToken, newPassword}`; 200 on success; 400 on expired/used token; newPassword runs through strength validator; all refresh tokens for user revoked|M|P0|
|4|COMP-RESET-STORE|Reset-token store|Store reset tokens (hashed) in Redis with 1-hour TTL; single-use semantics|Redis|INFRA-REDIS|token hashed before Redis write; TTL 3600s; delete-on-use via atomic GET+DEL pattern; key pattern `pwdreset:{tokenId}`|S|P0|
|5|COMP-EMAIL|SND email provider integration|Wrap SND SDK with retry + structured error handling; typed templates for reset email|SND|—|sendResetEmail(to, resetLink) returns success/error; retries transient failures (3 attempts, exp backoff); template id pinned in config; HTML + text variants; from-address pinned|M|P0|
|6|COMP-RESET-TMPL|Reset email template|HTML + text template containing 1-hour reset link with explicit expiry note|SND|5|template versioned in repo; contains reset link, 1-hour expiry message, support contact; renders correctly in major email clients|S|P1|
|7|NFR-COMPLIANCE-003-RESET|NIST SP 800-63B PA1 update via reset|Reset confirm runs new PA1 through bcrypt cost 12; never logs plaintext|THS|1, COMP-008|new PA1 hashed via PSS before DB write; plaintext never logged; token deletion confirmed before hash write; failure path does not leak existence|S|P0|
|8|COMP-SESSION-INVAL|Session invalidation on PA1 change|`TKN` purges all refresh tokens for user on successful reset-confirm|TKN|COMP-006, 3|all `rt:{userId}:*` keys deleted atomically on PA1 change; next login required for all devices; unit test asserts revocation|S|P0|
|9|R-PRD-004-MIT|Email delivery monitoring hook|Instrument SND send success/failure + alert threshold stub|SND|5|`email_send_success_total` and `email_send_failure_total` counters; alert spec documented for M6 wiring; support-channel fallback noted in runbook|S|P1|
|10|DECISION-RESET-ASYNC|Decision record: sync vs async reset email|Document chosen delivery mode based on OQ-PRD-001 resolution; capture retry/SLA implications|ADR|OQ-PRD-001|ADR committed; cites OQ-PRD-001 resolution; documents latency SLA, queue (if async), and alerting thresholds|S|P1|

### NTG Points — M3

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|Reset-token store|Redis strategy|Called from `THS.resetRequest()` and `resetConfirm()`|M3|API-005, API-006|
|SND client|DI provider|Registered with API key from secrets manager; used by reset flow|M3|API-005 (M3), future notification hooks|
|Session-invalidation hook|`TKN` method|Invoked from reset-confirm success path|M3|API-006 (M3), admin force-logout (M6)|
|Reset email template|Config-driven asset|Template id referenced from reset handler|M3|API-005 (M3)|

### Milestone DPN — M3

- M2 complete: `THS`, `TKN`, `PSS` wired.
- SND API key provisioned in secrets manager.
- OQ-PRD-001 resolved so sync-vs-async delivery decision is locked before API-005 implementation.

### Open Questions — M3

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-PRD-001|Password reset emails: synchronous or asynchronous delivery?|Blocks API-005 implementation, queue infra decision, and OPS-008 alert thresholds|Engineering|Start of Week 5|

### Risk Assessment and MTG — M3

|#|Risk|Severity|Likelihood|Impact|MTG|Owner|
|---|---|---|---|---|---|---|
|1|R-PRD-004|Email delivery failures block PA1 reset|Medium|Delivery monitoring + alerting (OPS-008); fallback support channel documented; 3-attempt retry in `COMP-EMAIL`|ops|
|2|Reset token enumeration via timing|High|Low|Attacker probes valid emails|Constant-time response on reset-request; identical 200 payload/latency for existent vs non-existent; rate-limited|backend|
|3|Reset token reuse|High|Low|Password reset hijack|Hashed storage; atomic GET+DEL in Redis; all sessions invalidated on confirm|backend|
|4|SND outage blocks reset flow|Medium|Low|User stuck, support tickets spike|Retries + alerting; support-channel fallback; dependency status page monitoring|ops|

## M4: FRN NTG — Auth UI and Provider

**Objective:** Ship login, RGS, profile, and context provider for Alex (end user) with silent refresh wired through `THP` | **Duration:** Weeks 7–8 | **Entry:** M2/M3 API contracts stable; frontend routing framework available | **Exit:** COMP-001..004 pass component tests; Customer Journey Map flows (signup, login, reset, profile) demonstrable end-to-end in staging

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|COMP-004|`THP` React context|Manages `AuthToken` state, silent refresh, 401 interception, redirect-to-login|FRN|API-001, API-003, API-004|props: `children: ReactNode`; stores accessToken in memory only; refresh scheduled before 15-min expiry; intercepts 401 and triggers refresh then retry; clears state on tab close; exposes login()/logout()/isAuthenticated|L|P0|
|2|COMP-001|`LoginPage` route|Renders email/PA1 form; submits to `/auth/login`; handles error, lockout, rate limit|FRN|1, API-001|route `/login`; props `{onSuccess, redirectUrl?}`; inline VLD for email format; generic error on 401 (no enumeration); 423 locked shows reset guidance; 429 shows retry-after message; success → redirectUrl|M|P0|
|3|COMP-002|`RegisterPage` route|Renders email/PA1/displayName form with client-side strength VLD; calls `/auth/register`|FRN|1, API-002|route `/register`; props `{onSuccess, termsUrl}`; client-side: min 8 chars, uppercase, number; displays terms link; 409 shows login/reset hint; 400 highlights failed rule; success auto-logs-in via THP|M|P0|
|4|COMP-003|`ProfilePage` route|Displays `SRP` fetched via GET `/auth/me`|FRN|1, API-003|route `/profile`; auth required (THP); shows displayName, email, createdAt; 401 triggers refresh then retry; render < 1s on staging|S|P0|
|5|COMP-RESET-REQ|Password reset request UI|Form at `/forgot-PA1` that calls `/auth/reset-request`; always shows success message|FRN|API-005|route `/forgot-PA1`; email input; on submit shows confirmation regardless of email existence; link to login|S|P0|
|6|COMP-RESET-CONFIRM|Password reset confirm UI|Form at `/reset-PA1?token=...` that calls `/auth/reset-confirm`|FRN|API-006|route parses token from URL; newPassword field with strength validator; on 400 shows "link expired, request new"; on success redirects to login|S|P0|
|7|COMP-LOGOUT|Logout action|Clears in-memory token, revokes refresh token via API, redirects to `/`|FRN|1, API-004|logout() clears THP state; calls backend revoke endpoint; cookie (HttpOnly refresh) cleared; redirects to landing|S|P0|
|8|NFR-COMPLIANCE-001|GDPR consent at RGS|Consent checkbox on `RegisterPage` with timestamp recorded server-side|FRN, THS|3, DM-001|checkbox must be checked to submit; RGS payload includes `consentAt` timestamp; stored in audit log; privacy policy link provided|S|P0|
|9|NFR-COMPLIANCE-004|GDPR data minimization (UI)|RegisterPage collects only email, PA1, displayName|FRN|3|no additional PII fields on form; no optional phone/address; field list matches DM-001 exactly; design review signoff|S|P0|
|10|R-001-MIT|Token theft XSS mitigations|THP stores accessToken in memory only; refreshToken via HttpOnly cookie; clears on tab close|FRN|1|accessToken never written to localStorage/sessionStorage; refreshToken transported via HttpOnly+Secure+SameSite cookie; window.beforeunload clears state; CSP header verified at gateway|M|P0|
|11|COMP-401-INTERCEPT|Global 401 interceptor|Axios/fetch interceptor triggers silent refresh then retry; if refresh fails, redirects to login|FRN|1|intercepts 401 once, attempts refresh, re-fires original request; on refresh-fail clears state and redirects to /login; prevents refresh-loop via per-request flag|S|P0|

### NTG Points — M4

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|`THP`|React context|Wraps app root; public and protected routes consume via `useAuth()`|M4|`LoginPage`, `RegisterPage`, `ProfilePage`, 401 interceptor|
|HTTP client interceptor|Middleware chain|Registered during THP mount; applies to every auth-sensitive request|M4|All authenticated fetches (M4→M7)|
|Protected-route guard|Route wrapper|Wraps `/profile` and future protected routes|M4|`ProfilePage` (M4), future personalized routes|
|HttpOnly refresh cookie|Cookie policy|Set by `/auth/login` response; read by backend refresh endpoint|M4|API-001, API-004 (M2); THP refresh loop (M4)|

### Milestone DPN — M4

- M2 API-001..004 stable.
- M3 API-005..006 stable for reset UI.
- FRN routing framework dependency ready (from Dependency Inventory #8).

### Open Questions — M4

*(none — all UI-side questions either resolved by M2/M3 decisions or deferred to v1.1 by product scope)*

### Risk Assessment and MTG — M4

|#|Risk|Severity|Likelihood|Impact|MTG|Owner|
|---|---|---|---|---|---|---|
|1|R-001|Token theft via XSS|High|Medium|Full account takeover|accessToken memory-only; HttpOnly cookie for refresh; 15-min access TTL; THP clears on tab close; CSP enforced; dependency audit (`npm audit`) in CI|SCR|
|2|R-PRD-001|Low RGS adoption from poor UX|Medium|Medium|Revenue impact, adoption miss|Usability testing pre-launch; funnel analytics from Day 1; iterate on error copy; >60% target tracked via success criteria|product|
|3|Silent-refresh loop bug|Medium|Medium|Users see flash or logout storms|Per-request refresh flag; unit tests for 401-during-refresh; staging soak test|frontend|
|4|CSP misconfiguration allows inline scripts|High|Low|XSS surface widens|CSP nonce-based; `unsafe-inline` forbidden; report-only mode in staging before enforcement|SCR|

## M5: Testing, Performance, and Security Validation

**Objective:** Prove FR/NFR CMP with the testing pyramid (80/15/5), pass performance + SCR bars, complete penetration testing | **Duration:** Weeks 9–10 | **Entry:** M2/M3/M4 feature-complete; staging environment ready with seeded accounts | **Exit:** All TEST-001..006 green; unit coverage ≥80%; integration 15%; E2E 5%; k6 run sustains 500 concurrent login RPS at <200ms p95; pentest findings at High or above resolved

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|TEST-001|Unit — login with valid credentials returns `AuthToken`|Validates FA0: `THS.login()` calls `PSS.verify()` → `TKN.issueTokens()`|THS|FA0|Jest+ts-jest; mocks PSS and TKN; asserts returned AuthToken has access + refresh; asserts lastLoginAt updated|S|P0|
|2|TEST-002|Unit — login with invalid credentials returns error|Validates FA0: `PSS.verify()` false → 401, no token|THS|FA0|Jest; asserts 401 envelope with AUTH_INVALID_CREDENTIALS; asserts no token issued; identical response for non-existent email|S|P0|
|3|TEST-003|Unit — token refresh with valid refresh token|Validates FR-AUTH-003: `TKN.refresh()` rotates and re-issues|TKN|FR-AUTH-003|Jest; asserts old refresh revoked before new issued; asserts new AuthToken pair returned; asserts JWT signs with RS256|S|P0|
|4|TEST-004|NTG — RGS persists `SRP` to PG|Validates FR-AUTH-002: API → `PSS` → PST insert|THS, PST|FR-AUTH-002|Supertest + testcontainers; spins up PG; asserts row inserted with hashed PA1; asserts email uniqueness constraint fires on duplicate|M|P0|
|5|TEST-005|NTG — expired refresh token rejected|Validates FR-AUTH-003: Redis TTL correctly invalidates|TKN, Redis|FR-AUTH-003|testcontainers Redis; fast-forward via TTL; assert 401 on expired refresh; assert no new token issued|M|P0|
|6|TEST-006|E2E — user registers and logs in|Validates FA0 + FR-AUTH-002; Customer Journey signup + login|FRN, All APIs|COMP-001, COMP-002, COMP-004|Playwright; RegisterPage → LoginPage → ProfilePage; asserts SRP data displayed; asserts silent refresh fires before access expiry|M|P0|
|7|NFR-PERF-001|API response time (p95 < 200ms)|Load test auth endpoints via k6|THS|M4 complete|k6 scenario on /auth/login, /auth/refresh, /auth/me; p95 < 200ms on each; report committed to perf folder|M|P0|
|8|NFR-PERF-002|500 concurrent login load test|k6 ramp to 500 concurrent login RPS on staging|THS, PST, Redis|NFR-PERF-001|k6 sustains 500 concurrent for 10 min; error rate < 0.1%; p95 < 200ms; Redis/PG pool metrics captured|M|P0|
|9|NFR-REL-001|Reliability — health-check endpoint and SLO wiring|Deploy `/healthz` readiness/liveness; configure SLO dashboard for 99.9% over 30-day window|THS|INFRA-NODE|`/healthz` checks PG + Redis connectivity; K8s probes wired; SLO dashboard (Grafana) computed over 30-day rolling; error-budget policy documented|S|P0|
|10|TEST-LOCKOUT|NTG — account lockout after 5 failures|Validate lockout enforcement and recovery|THS, Redis|COMP-LOCKOUT|testcontainers; 5 failed logins within 15 min → 423 on 6th; after policy window → login succeeds; counter reset on successful login|M|P0|
|11|TEST-ENUM|Security — no user enumeration|Contract test: identical response + latency for non-existent vs wrong-PA1|THS|FA0|latency delta < 10ms between paths over 1000 samples; identical status + body; identical for /auth/reset-request|S|P0|
|12|TEST-RESET-LIFECYCLE|NTG — reset token single-use + 1h TTL|Full flow reset-request → reset-confirm; second-use rejected; post-1h rejected|THS, Redis|FR-AUTH-005|first confirm succeeds; second attempt → 400 token-used; after 1h → 400 token-expired; all refresh tokens revoked for user|M|P0|
|13|R-PRD-002-REV|Dedicated SCR review|Architecture + code review with SCR team; threat model committed|Security team|M2, M3, M4|STRIDE-style threat model; review of DM-001/DM-002, API surface, token lifecycle, reset flow; findings logged with remediation owners|M|P0|
|14|R-PRD-002-PEN|Penetration test|External pentest vendor engages staging; covers OWASP ASVS L2 auth controls|External vendor|M2, M3, M4|pentest scope covers auth surface; findings report delivered; High/Critical findings resolved before M7 exit|L|P0|
|15|TEST-COV|Coverage gate enforcement|CI gate enforces unit 80% / integration 15% structure|CI|1, 2, 3, 4, 5|CI fails if unit line coverage < 80% on `THS`, `TKN`, `PSS`, `JWT`; integration/E2E counts audited|S|P1|
|16|TEST-CI-ENV|Ephemeral CI test environment|testcontainers-based CI run with ephemeral PG + Redis|CI|INFRA-PG, INFRA-REDIS|CI spins PG 15 + Redis 7 containers per run; teardown automatic; parallel-safe; documented in README|S|P1|

### NTG Points — M5

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|k6 load scenarios|Test harness|Executed on staging against public gateway|M5|NFR-PERF-001, NFR-PERF-002 VLD; M7 pre-GA re-run|
|testcontainers setup|Test harness|Invoked per integration test run (local + CI)|M5|TEST-004, TEST-005, TEST-LOCKOUT, TEST-RESET-LIFECYCLE|
|Playwright E2E suite|Test harness|Runs against staging env with seeded accounts|M5|TEST-006; M7 pre-GA smoke|
|Pentest findings tracker|Review process|Findings logged with severity + owner; blocked on remediation before M7|M5|R-PRD-002 closure|

### Milestone DPN — M5

- M2, M3, M4 feature-complete.
- Staging environment with seeded test accounts isolated from prod.
- Pentest vendor contract signed (must be booked at M1 kickoff per pre-M1 risk).

### Open Questions — M5

*(none — resolution of scope-related OQs rolled forward from earlier milestones)*

### Risk Assessment and MTG — M5

|#|Risk|Severity|Likelihood|Impact|MTG|Owner|
|---|---|---|---|---|---|---|
|1|R-PRD-002|Security breach from implementation flaws|Critical|Low|Identity compromise, CMP failure|Dedicated SCR review (TEST-13); external pentest (TEST-14); STRIDE threat model; High/Critical findings block M7|SCR|
|2|Load test surfaces p95 > 200ms|High|Medium|NFR-PERF-001 miss blocks MIG-002|Profile bcrypt cost, PG pool, Redis cluster; scale pods per OPS-004; re-test|backend|
|3|E2E flakiness delays sign-off|Medium|Medium|False positives erode trust in CI|Playwright retries + seed reset between tests; deterministic test users; quarantine flaky tests with root-cause logging|qa|
|4|Coverage gate blocks release on trivial gaps|Medium|Low|Delivery delay|Grant temporary waivers with justification PRs; backfill coverage post-merge|qa|

## M6: Compliance, Audit Logging, and Observability

**Objective:** Satisfy SOC2/GDPR/NIST CMP requirements, ship audit logging with admin visibility, instrument full observability stack | **Duration:** Weeks 11–12 | **Entry:** M2/M3/M4 complete; SOC2 control mapping document available | **Exit:** NFR-COMPLIANCE-001..004 validated against controls; audit-log queryable by admin (Jordan); Prometheus metrics + OpenTelemetry traces live; alerts firing on staging thresholds

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|NFR-COMPLIANCE-002|SOC2 Type II audit logging|All auth events logged with user ID, timestamp, IP, outcome; 12-month retention|THS, PST|INFRA-AUDIT|events logged: login-success, login-failure, RGS, PA1-reset-request, PA1-reset-confirm, refresh, lockout, logout; each row has userId, timestamp, ip, outcome; 12-month retention policy applied; SOC2 control mapping doc attached|M|P0|
|2|NFR-COMPLIANCE-003|NIST SP 800-63B PA1 storage VLD|Audit confirms bcrypt cost 12 in prod config; plaintext never logged|THS|NFR-SEC-001|NIST control mapping checked; config audit shows bcrypt cost 12; log scrubbers confirm no plaintext in any log stream; test asserts scrubber|S|P0|
|3|COMP-AUDIT-WRITER|Audit-log writer component|Centralized async writer for audit events; decouples from request path|THS|INFRA-AUDIT|writer batches + flushes every N events or T seconds; failure does not block request; dead-letter queue for persistence failures|M|P0|
|4|COMP-AUDIT-READER|Admin audit-read API (JTBD gap fill)|GET `/v1/admin/auth-events` for Jordan persona to investigate incidents|THS|1, 3|admin role required; query by userId, date range, eventType; paginated; returns list of audit rows; SOC2 audit trail exposed|M|P1|
|5|OPS-007|Observability — metrics and traces|Prometheus metrics + OpenTelemetry spans across `THS` → `PSS` → `TKN` → `JWT`|THS|M2 complete|counters: `auth_login_total`, `auth_registration_total`, `auth_token_refresh_total`; histogram: `auth_login_duration_seconds`; OTel spans cover full request path; dashboards in Grafana|M|P0|
|6|OPS-008|Observability — alerts|Alert rules for login failure rate, p95 latency, Redis connection failures|Prometheus|5|alert: login_failure_rate > 20% over 5 min; alert: p95_latency > 500ms; alert: TKN Redis connection failures above threshold; sensitive fields (PA1, tokens) excluded from logs|S|P0|
|7|NFR-COMPLIANCE-001-VALIDATE|GDPR consent audit|Validate consent timestamp recorded for every new RGS|THS|NFR-COMPLIANCE-001|every RGS row links to audit event with `consent_at` timestamp; query demonstrates 100% coverage on staging; privacy policy version referenced|S|P0|
|8|NFR-COMPLIANCE-004-VALIDATE|GDPR data minimization audit|Audit DB schema for fields beyond email/hashed-PA1/displayName|DM-001|DM-001|data-classification doc lists every field with justification; no additional PII present; data-flow diagram signed off by privacy lead|S|P0|
|9|R-PRD-003-MIT|SOC2 control mapping|Map auth events to SOC2 CC7.2/CC6.1 controls; QA validates in staging|Compliance|1|every SOC2 control relevant to auth mapped to a log event or technical control; VLD test asserts events visible for each control; CMP sign-off recorded|M|P0|
|10|COMP-LOG-SCRUB|Log scrubber middleware|Redact PA1, tokens, PII from all structured log statements|Logging|INFRA-NODE|scrubber regex + field list; CI test asserts no matches in log fixtures; applied at logger level so application code cannot bypass|S|P0|
|11|COMP-ADMIN-UNLOCK|Admin account-unlock tool|Allow Jordan to unlock locked accounts; tool records actor in audit log|THS|COMP-LOCKOUT, 1|admin endpoint or CLI; actor, target user, reason logged; unlocks immediately; rate-limited to avoid misuse|S|P1|
|12|OPS-DASH|Grafana dashboards|Service dashboard: RPS, error rate, p95 latency, lockout rate, refresh rate, Redis/PG saturation|Grafana|5|dashboard JSON in repo; referenced from OPS-001/002 runbooks; auto-provisioned in staging + prod|S|P1|
|13|OPS-SLO|SLO + error-budget policy|Define 99.9% availability and p95 < 200ms SLOs; wire burn-rate alerts|Grafana|5, NFR-REL-001|SLOs defined; fast and slow burn-rate alerts configured; monthly error-budget reviewed; doc attached to runbook|S|P1|
|14|DECISION-VERSIONING|Decision record: URL-prefix versioning|Document `/v1/auth/*` policy and breaking-change rules for Sam persona|ADR|COMP-VERSION|ADR committed; lists Sam-persona rationale; enumerates what counts as breaking; references URL-prefix choice over header-based|S|P2|

### NTG Points — M6

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|Audit-log writer|DI async pipeline|Injected into `THS` and reset flow handlers|M6|All auth events (M6→M7); admin read API|
|Prometheus registry|Metrics instrumentation|Counters/histograms registered on service boot|M6|Grafana dashboards; OPS-008 alerts|
|OpenTelemetry tracer|Tracing pipeline|SDK initialized at service boot; spans auto-instrumented across components|M6|Traces exported to collector; Grafana Tempo or equivalent|
|Log scrubber|Logger middleware|Mounted at logger level, not application code|M6|All log lines across service|
|Admin role guard|Middleware|Wraps `/v1/admin/*` routes; validates role claim|M6|COMP-ADMIN-UNLOCK, COMP-AUDIT-READER|

### Milestone DPN — M6

- M2/M3/M4 feature-complete.
- SOC2 control mapping from CMP team.
- Observability stack (Prometheus + OTel collector + Grafana) available per platform standard.

### Open Questions — M6

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|JTBD-GAP-01|Admin persona (Jordan) JTBD "view authentication event logs for incident investigation" — PRD requires admin-facing API/UI; TDD omits|Drives COMP-AUDIT-READER scope and admin UI plan; PRD requires; TDD should be updated|product-team + auth-team|Start of Week 11|

### Risk Assessment and MTG — M6

|#|Risk|Severity|Likelihood|Impact|MTG|Owner|
|---|---|---|---|---|---|---|
|1|R-PRD-003|Compliance failure from incomplete audit logging|High|Medium|SOC2 Type II audit failure, enterprise deal blockers|Define log requirements early (done M1 foundation); validate against SOC2 controls in QA (R-PRD-003-MIT); CMP sign-off pre-GA|CMP|
|2|Audit writer drops events under load|High|Low|Compliance gap|Async writer with DLQ + retry; alert on DLQ depth; integration test at k6 load levels|backend|
|3|Log scrubber bypass leaks secrets|Critical|Low|Token/PA1 leak in logs|Scrubber at logger level; CI fixture tests; RTT + revocation runbook if breach detected|SCR|
|4|Admin-role claim spoofing|High|Low|Unauthorized audit log access|Role claim signed in JWT via RS256; admin middleware validates role + issuer; audit log read itself logged|SCR|

## M7: Phased Rollout and Operational Readiness

**Objective:** Execute the three-phase rollout with feature flags and parallel legacy safety net; complete runbooks, capacity planning, on-call RTT; cut over to GA | **Duration:** Weeks 13–15 | **Entry:** M5 SCR/pentest sign-off; M6 CMP sign-off; feature flags in config service | **Exit:** `ANL` fully enabled at 100%; legacy endpoints deprecated; 99.9% uptime over first 7 days of GA; all P0/P1 dashboards green; runbooks rehearsed

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|MIG-001|Phase 1: Internal Alpha (1 week)|Deploy `THS` to staging; auth-team + QA test all endpoints; `LoginPage`/`RegisterPage` behind `ANL`|THS, FRN|M5, M6|FA0..005 pass manual test plan; zero P0/P1 bugs open at end of week; auth-team + QA sign-off|M|P0|
|2|MIG-002|Phase 2: Beta 10% traffic (2 weeks)|Enable `ANL` for 10% of traffic; monitor latency, error rates, Redis usage|API Gateway, THS|MIG-001|p95 < 200ms over rolling 24h; error rate < 0.1%; zero Redis connection failures; `THP` silent refresh succeeds under real load|L|P0|
|3|MIG-003|Phase 3: General Availability 100%|Remove `ANL`; deprecate legacy endpoints; enable `AUTH_TOKEN_REFRESH`|API Gateway, THS|MIG-002|99.9% uptime over first 7 days post-GA; legacy endpoints return deprecation header then 410 Gone per plan; all dashboards green|M|P0|
|4|MIG-004|Feature flag `ANL`|Gates new `LoginPage`/`THS` login paths; default OFF|Config service|—|flag registered in config service; default OFF; targeting by traffic % and tenant; ownership auth-team; cleanup after MIG-003 GA|S|P0|
|5|MIG-005|Feature flag `AUTH_TOKEN_REFRESH`|Enables refresh-token flow in `TKN`; when OFF, access-only|Config service|—|flag registered; default OFF; cleanup scheduled MIG-003 + 2 weeks; ownership auth-team|S|P0|
|6|MIG-006|Rollback step 1 — disable `ANL`|Flip flag to OFF; route traffic to legacy auth|Config service|MIG-004|runbook action: flip flag; verify traffic routed to legacy endpoints within 60s; logged as incident step|S|P0|
|7|MIG-007|Rollback step 2 — verify legacy login via smoke tests|Automated smoke-test suite hits legacy endpoints post-rollback|CI, API Gateway|MIG-006|smoke test pass rate == 100%; captures representative user flows; evidence attached to incident ticket|S|P0|
|8|MIG-008|Rollback step 3 — investigate root cause|Engineer investigates `THS` root cause via structured logs + traces|THS|OPS-007|on-call opens investigation within 15 min; traces + logs collected; hypothesis recorded; ties to R-### or new risk entry|S|P0|
|9|MIG-009|Rollback step 4 — restore `SRP` from backup if corrupted|PITR restore of last known-good backup if data corruption detected|PST|INFRA-PG|backup freshness < 24h; restore runbook rehearsed; data diff report generated; communication plan activated|M|P0|
|10|MIG-010|Rollback step 5 — notify auth-team + platform-team|Incident channel notification on rollback; incident commander designated|IncidentOps|—|notification fired in incident channel within 5 min of rollback; roster of on-call + escalations included|S|P0|
|11|MIG-011|Rollback step 6 — post-mortem within 48h|Blameless post-mortem with action items feeding back into roadmap|Process|MIG-008|post-mortem doc committed within 48h; action items assigned with owners and dates; tracked to closure|S|P0|
|12|OPS-001|Runbook: `THS` down|Diagnosis and resolution steps for 5xx on `/auth/*`; `LoginPage`/`RegisterPage` error state|Runbook|OPS-007|runbook covers pod health check (K8s), PG connectivity, `PSS`/`TKN` init logs; resolution: restart pods, PG failover to read replica, Redis-down degraded-mode behavior; escalation to auth-team on-call → platform-team at 15 min|S|P0|
|13|OPS-002|Runbook: Token refresh failures|Diagnosis for mass `THP` redirect loops and `auth_token_refresh_total` spike|Runbook|OPS-007|runbook covers Redis connectivity from `TKN`, `JWT` key access, `AUTH_TOKEN_REFRESH` flag state; resolution: scale Redis cluster, re-mount secrets volume, enable flag if OFF; escalation auth-team → platform-team|S|P0|
|14|OPS-003|On-call expectations and RTT|Define on-call RTT, ack SLA, tooling|Process|—|P1 ack ≤ 15 min; auth-team 24/7 RTT for first 2 weeks post-GA; tooling: K8s dashboards, Grafana, Redis CLI, PG admin; path: auth-team on-call → test-lead → eng-manager → platform-team|S|P0|
|15|OPS-004|Capacity: `THS` pods|Baseline 3 replicas; HPA to 10 at CPU > 70%|THS, K8s|—|HPA config: min 3, max 10, target CPU 70%; load test (NFR-PERF-002) verifies scaling triggers; runbook references capacity thresholds|S|P0|
|16|OPS-005|Capacity: PST connection pool|Baseline 100 pool; scale to 200 if wait > 50ms|PST|INFRA-PG|pool configured at 100; wait-time metric exported; alert when > 50ms sustained 5 min; runbook step to increase pool + restart|S|P0|
|17|OPS-006|Capacity: Redis|1 GB baseline; scale to 2 GB at > 70% utilization|Redis|INFRA-REDIS|utilization metric exported; alert at 70%; runbook step for capacity increase; eviction policy reviewed|S|P0|
|18|GA-SIGNOFF|Cross-functional GA sign-off|Product + Engineering + Security + Compliance sign off on GA release|Cross-functional|MIG-003, R-PRD-002-PEN, R-PRD-003-MIT|signed ADR/release-readiness checklist: success-criteria baselines met, SCR findings closed, SOC2 controls validated, runbooks rehearsed; recorded in release tracker|S|P0|

### NTG Points — M7

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|`ANL` flag|Feature flag|Registered in config service; evaluated at API Gateway and frontend|M7|API-001/002, `LoginPage`, `RegisterPage` during MIG-001..003|
|`AUTH_TOKEN_REFRESH` flag|Feature flag|Registered in config service; evaluated in `TKN`|M7|API-004, `THP` refresh loop|
|HPA policy|K8s controller|Deployed per-service; tied to CPU metric|M7|`THS` pods (OPS-004)|
|Rollback automation|Incident runbook|Script runs MIG-006..010 with human approval gate|M7|Incident response; drills in pre-MIG-001 week|
|Release-readiness checklist|Process gate|Required signatures in release tracker|M7|GA-SIGNOFF|

### Milestone DPN — M7

- M5 sign-off: pentest findings High/Critical closed; NFR-PERF-001/002 validated.
- M6 sign-off: SOC2 control mapping complete; observability live.
- Rollback triggers agreed: p95 > 1000ms for 5 min · error rate > 5% for 2 min · Redis connection failures > 10/min · any `SRP` data corruption.

### Open Questions — M7

*(none — all release-blocking questions resolved in M1–M6; remaining OQs deferred to v1.1 per product scope)*

### Risk Assessment and MTG — M7

|#|Risk|Severity|Likelihood|Impact|MTG|Owner|
|---|---|---|---|---|---|---|
|1|R-003|Data loss during migration|High|Low|Corrupted `SRP` data, customer impact|Parallel legacy+new run Phases 1-2; idempotent upserts; PITR backup before each phase; MIG-009 restore rehearsed|platform|
|2|Feature flag misfire routes 100% traffic prematurely|High|Low|Unplanned rollout, blast radius not contained|Flag change requires two-person approval in config service; automated canary check aborts if error-rate threshold exceeded|platform|
|3|On-call gap during 24/7 window|High|Medium|P1 ack SLA missed|OPS-003 explicit 24/7 auth-team RTT for 2 weeks post-GA; platform-team backup; paging test pre-MIG-002|ops|
|4|SND throttling during Phase 2 load|Medium|Medium|Reset emails delayed; R-PRD-004 materializes|Coordinate SND quotas pre-MIG-002; monitor `email_send_failure_total`; fallback support channel per OPS runbook|ops|

## Resource Requirements and DPN

### External DPN

|Dependency|Required By MLS|Status|Fallback|
|---|---|---|---|
|PST 15+|M1|To provision|Managed cloud PG if self-hosted unavailable; delay M1 exit|
|Redis 7+|M1|To provision|Managed cloud Redis; switch to ElastiCache if cluster unavailable|
|Node.js 20 LTS|M1|Standard runtime|Pin to 20.x; block upgrade to 22 until post-GA|
|bcryptjs|M1|npm dependency|No realistic fallback; abstraction behind `PSS` allows future swap to argon2id|
|jsonwebtoken|M1|npm dependency|Alternative `jose` library available with same RS256 semantics|
|SND API|M3|Needs API key + domain verification|AWS SES or Postmark; swap via `COMP-EMAIL` interface|
|API Gateway|M1|Shared platform dependency|Fall back to service-side rate limiting + CORS if gateway delayed (reduced defense-in-depth)|
|FRN routing framework|M4|Internal dependency|Must be ready by M4 start; escalate to platform if not|

### Infrastructure Requirements

- Kubernetes cluster with HPA enabled for `THS` (min 3, max 10 replicas).
- Prometheus + Grafana + OpenTelemetry collector for observability stack (OPS-007/008).
- Secrets manager with IAM-scoped access for RSA keypair and SND API key.
- CI runners capable of hosting testcontainers (PG 15 + Redis 7) in parallel.
- Staging environment isolated from production, with seeded test accounts and representative data volumes.
- Backup + PITR infrastructure for PST (nightly full + continuous WAL, 7-day retention).
- Config service for feature flags (`ANL`, `AUTH_TOKEN_REFRESH`).
- Incident management tooling (paging, runbook hosting, status page).

## Risk Register

|ID|Risk|Affected Milestones|Probability|Impact|MTG|Owner|
|---|---|---|---|---|---|---|
|R-001|Token theft via XSS|M4|Medium|High — full account takeover|accessToken in memory only; HttpOnly cookies for refreshToken; 15-min access TTL; `THP` clears on tab close; CSP enforced; contingency: immediate `TKN` revocation + force PA1 reset|SCR|
|R-002|Brute-force attacks on login|M2|High|Medium — credential stuffing success|API Gateway rate limit 10/min/IP; 5-attempt account lockout; bcrypt cost 12; contingency: WAF IP block + CAPTCHA after 3 failed attempts|SCR|
|R-003|Data loss during migration|M7|Low|High — `SRP` corruption|Parallel legacy+new during MIG-001..002; idempotent upsert; full PITR backup before each phase; contingency: rollback to legacy + restore (MIG-009)|platform|
|R-004|RSA key material leak or weak generation|M1|Low|Critical — token forgery|HSM-backed secrets manager; restricted IAM; quarterly RTT; no keys in repo|SCR|
|R-005|User enumeration via differential 401 behavior|M2, M3|Medium|High — targeted phishing enablement|Identical 401 for non-existent email vs wrong PA1; constant-time path; identical reset-request response; TEST-ENUM contract test|backend|
|R-006|Refresh token replay|M2|Medium|High — persistent unauthorized access|Rotation on every refresh; old revoked before new issued; hashed Redis storage|backend|
|R-007|Log scrubber bypass leaks secrets|M6|Low|Critical — token/PA1 leak|Logger-level scrubber; CI fixture tests; RTT runbook on breach|SCR|
|R-PRD-001|Low RGS adoption from poor UX|M4|Medium|High — revenue miss vs >60% target|Usability testing pre-launch; funnel iteration; analytics from Day 1|product|
|R-PRD-002|Security breach from implementation flaws|M5|Low|Critical — identity compromise|Dedicated SCR review (TEST-13); external pentest (TEST-14); High/Critical findings block M7|SCR|
|R-PRD-003|Compliance failure from incomplete audit logging|M6|Medium|High — SOC2 audit failure|Define log requirements early; validate against SOC2 controls in QA; CMP sign-off pre-GA|CMP|
|R-PRD-004|Email delivery failures block PA1 reset|M3, M7|Low|Medium — user stuck + support spike|Delivery monitoring + alerting; fallback support channel; retries with backoff|ops|
|R-008|Load test surfaces p95 > 200ms|M5|Medium|High — blocks MIG-002 rollout|Profile bcrypt cost, PG pool, Redis cluster; scale pods per OPS-004; re-run k6|backend|
|R-009|Feature flag misfire routes 100% traffic prematurely|M7|Low|High — unplanned full rollout|Two-person approval on flag changes; automated canary abort on error-rate breach|platform|
|R-010|Admin-role claim spoofing|M6|Low|High — audit log exfiltration|Role claim signed via RS256; admin middleware validates; admin-read logged|SCR|

## Success Criteria and Validation Approach

|Criterion|Metric|Target|Validation Method|MLS|
|---|---|---|---|---|
|Login response time|p95 latency on `/auth/login`|< 200ms|k6 load test on staging; APM in prod|M5, M7|
|Registration success rate|successful registrations / attempts|> 99%|analytics funnel on `/auth/register`|M7|
|Token refresh latency|p95 on `/auth/refresh`|< 100ms|k6 load test on staging; APM in prod|M5, M7|
|Service availability|uptime / 30-day window|99.9%|SLO dashboard; health-check uptime checks|M7|
|Password hash time|per-hash wall time|< 500ms|bcrypt benchmark in CI + NFR-PERF-001 VLD|M1, M5|
|User RGS conversion|landing → confirmed-account funnel|> 60%|product analytics (post-GA)|M7|
|Daily active authenticated users|DAU after GA|> 1000 within 30 days|product analytics|M7|
|Average session duration|token-refresh event analytics|> 30 minutes|OPS-007 metrics + product analytics|M7|
|Failed login rate|failures / attempts|< 5%|auth event log analysis (NFR-COMPLIANCE-002)|M7|
|Password reset completion rate|confirmed resets / requests|> 80%|reset-flow funnel analytics|M7|
|Unit test coverage|line coverage on core components|≥ 80%|CI coverage gate (TEST-COV)|M5|
|Security review + pentest|High/Critical findings resolved|100% closed|R-PRD-002-REV + R-PRD-002-PEN|M5|
|SOC2 audit trail completeness|coverage of SOC2 CC7.2/CC6.1 auth events|100%|R-PRD-003-MIT mapping VLD|M6|

## Decision Summary

|Decision|Chosen|Alternatives Considered|Rationale|
|---|---|---|---|
|Session strategy|Stateless JWT (RS256) + Redis-backed refresh (7-day)|(a) Server-side sessions in PG; (b) Stateless JWT only (no refresh)|(a) rejected: horizontal scaling of `THS` requires session affinity; (b) rejected: forces re-login every 15 min, violates FR-AUTH.3 session persistence + silent refresh for Sam persona|
|Password hashing algorithm|bcrypt cost 12 via `PSS` abstraction|(a) argon2id; (b) PBKDF2|chosen per NIST SP 800-63B CMP + ≈300ms benchmark (inside 500ms target); abstraction preserves future argon2id migration path (DECISION-HASH ADR)|
|Token signing algorithm|RS256 with 2048-bit RSA|(a) HS256 symmetric; (b) EdDSA|HS256 rejected: shared secret leaks to any verifier; EdDSA deferred: library support less mature across client SDKs; RS256 matches NFR-SEC-002|
|API versioning|URL-prefix `/v1/auth/*`|(a) Accept-version header; (b) query param|URL-prefix chosen for Sam-persona ergonomics (cacheable, debuggable); breaking changes require explicit major bump (DECISION-VERSIONING ADR)|
|Rollout strategy|3-phase feature-flag gated with parallel legacy|(a) Big-bang cutover; (b) Blue-green without flag|(a) rejected: MIG R-003 data-loss blast radius too large; (b) partial mitigation only: flag granularity enables 10% canary with instant rollback (MIG-006)|
|Refresh token storage|Hashed refresh tokens in Redis 7 with 7-day TTL|(a) JWT refresh tokens (stateless); (b) PG-persisted refresh tokens|(a) rejected: cannot revoke before expiry; (b) rejected: PG write load + slower token VLD; Redis chosen per NFR-PERF-001 (<100ms refresh p95)|
|FRN token storage|accessToken in memory + refreshToken in HttpOnly cookie|(a) Both in localStorage; (b) Both in sessionStorage|(a)/(b) rejected: R-001 XSS exfiltration; memory+HttpOnly limits blast radius and matches R-001 mitigation|
|v1.0 scope|Email/PA1 only; roles stored but not enforced|(a) Include OAuth; (b) Include MFA|(a) + (b) rejected: Q3 2026 SOC2 deadline constraints scope; deferred per PRD S12 (Out of Scope); prevents missing CMP window|
|Email provider|SND with typed wrapper (`COMP-EMAIL`)|(a) AWS SES; (b) Postmark|SND chosen per Dependency Inventory #6; wrapper abstraction enables swap via single component (R-PRD-004 contingency)|
|Account lockout (pre-OQ-PRD-003)|5 attempts / 15 min window|(a) 3 attempts; (b) 10 attempts|working assumption tracked in OQ-PRD-003; 5 balances usability (Alex persona) vs brute-force mitigation (R-002); to be confirmed before M2 lockout implementation|

## Timeline Estimates

|MLS|Duration|Start|End|Key Milestones|
|---|---|---|---|---|
|M1|2 weeks|Week 1|Week 2|DM-001/DM-002 migrations applied; `PSS` + `JWT` pass unit tests; TLS 1.3 + CORS live; OQ-PRD-003 resolved|
|M2|2 weeks|Week 3|Week 4|FA0..003 integration-green; API-001..004 contract-frozen; account lockout active; OQ-PRD-002 resolved|
|M3|2 weeks|Week 5|Week 6|FR-AUTH-005 end-to-end in staging; API-005/006 non-enumerating; sessions invalidated on reset; OQ-PRD-001 resolved|
|M4|2 weeks|Week 7|Week 8|COMP-001..004 + reset UIs pass component tests; Customer Journey flows demonstrable in staging|
|M5|2 weeks|Week 9|Week 10|TEST-001..006 green; NFR-PERF-001/002 validated; pentest report delivered; High/Critical findings resolved|
|M6|2 weeks|Week 11|Week 12|NFR-COMPLIANCE-001..004 validated; audit-log admin API live; Prometheus metrics + OTel traces firing|
|M7|3 weeks|Week 13|Week 15|MIG-001 alpha → MIG-002 10% beta → MIG-003 GA; OPS-001..006 runbooks rehearsed; GA-SIGNOFF executed|

**Total estimated duration:** 15 weeks (≈3.5 months) from Week 1 kickoff to GA sign-off, with a further 2-week post-GA 24/7 on-call window (OPS-003) before steady-state RTT.

