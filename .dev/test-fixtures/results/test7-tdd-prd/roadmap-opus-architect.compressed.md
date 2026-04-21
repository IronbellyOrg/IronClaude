---
spec_source: "test-tdd-user-auth.compressed.md"
complexity_score: 0.65
complexity_class: MEDIUM
primary_persona: architect
---

# User Authentication Service — Project Roadmap

## Executive Summary

The User Authentication Service delivers the foundational identity layer that unblocks Q2–Q3 2026 personalization features and closes the SOC2 Type II compliance gap. Architecture is a stateless `AuthService` orchestrator delegating to `PasswordHasher` (bcrypt cost 12), `TokenManager` (Redis-backed refresh tokens), and `JwtService` (RS256, 2048-bit RSA, quarterly rotation), fronted by an API Gateway enforcing rate limits, CORS, and TLS 1.3. Frontend consumes the API via `AuthProvider`, `LoginPage`, `RegisterPage`, and `ProfilePage`. Roadmap is organized into five technical-layer milestones delivered over 10 weeks (2026-03-31 → 2026-06-09), aligned to the TDD S23 committed schedule.

**Business Impact:** Unblocks ~$2.4M projected annual revenue from personalization-dependent features, enables SOC2 Type II audit (Q3 2026), and reduces the 30% QoQ growth in access-related support tickets by introducing self-service account recovery.

**Complexity:** MEDIUM (0.65) — Bounded functional scope (5 FR, 6 API endpoints, 2 data models, 3 UI pages) offset by cryptographic correctness requirements, stateless-session design, defense-in-depth security, multi-store persistence (PostgreSQL + Redis + SendGrid), and SOC2/GDPR/NIST compliance envelopes.

**Critical path:** M1 Foundation (schemas, infra, feature-flag plumbing) → M2 Core Authentication (PasswordHasher + registration/login) → M3 Token Management & Session (TokenManager/JwtService + refresh + password reset) → M4 Integration & Hardening (frontend, observability, compliance, security) → M5 Production Readiness & GA (phased rollout, runbooks, capacity, deprecate legacy).

**Key architectural decisions:**

- Stateless JWT with refresh-token rotation (D6.4): server-side sessions rejected to preserve horizontal scalability; `TokenManager` handles dual-token lifecycle with Redis-backed revocation.
- bcrypt cost factor 12 via `PasswordHasher` abstraction: battle-tested with hash time ~300ms, within the <500ms budget; abstraction permits future algorithm migration without API churn.
- RS256 with 2048-bit RSA keys, rotated quarterly: asymmetric signing enables downstream services to verify tokens without sharing the signing secret.
- Audit log retention set to **12 months** (PRD NFR-COMPLIANCE-001 / SOC2 precedence over TDD S7.2's 90-day line — see OQ-CONFLICT-001).
- Scope locked to email/password in v1.0: OAuth, MFA, and RBAC enforcement are Non-Goals (TDD S3.2 NG-001/NG-002/NG-003, PRD S12.2) and are never relitigated inside milestone acceptance criteria.

**Open risks requiring resolution before M1:**

- OQ-CONFLICT-001 (audit log retention 90d vs 12mo) must be resolved before schema/migration authoring in M1 to avoid re-work; resolution committed to 12 months.
- OQ-CONFLICT-002 (TDD feature-milestones vs roadmap technical-layer milestones) mapping must be signed off by test-lead + eng-manager before M1 kickoff so Phase 1/2/3 rollout gates in TDD S19 remain traceable.
- R-PRD-002 (security breach from implementation flaws) — dedicated security review lead must be named and onboarded before cryptographic work begins in M2.

## Milestone Summary

|ID|Title|Type|Priority|Effort|Dependencies|Deliverables|Risk|
|---|---|---|---|---|---|---|---|
|M1|Foundation — Schemas, Infra, Feature-Flag Plumbing|Technical|P0|2w|INFRA-DB-001; SEC-POLICY-001|17|High|
|M2|Core Authentication — Registration, Login, Password Hashing|Technical|P0|2w|M1|18|High|
|M3|Token Management & Session — JWT, Refresh, Password Reset|Technical|P0|2w|M2|24|High|
|M4|Integration & Hardening — Frontend, Observability, Compliance|Technical|P0|2w|M3|27|High|
|M5|Production Readiness & GA — Rollout, Runbooks, Capacity|Operational|P0|2w|M4|16|Medium|

## Dependency Graph

```
INFRA-DB-001 ──┐
SEC-POLICY-001 ┼─> M1 Foundation ─> M2 Core Auth ─> M3 Tokens & Session ─> M4 Integration & Hardening ─> M5 Production Readiness & GA
AUTH-PRD-001 ──┘                     │                    │                       │                           │
                                     └─ FR-AUTH-001/002    ├─ FR-AUTH-003/004/005  ├─ COMP-001..004 frontend   ├─ MIG-001/002/003 phased rollout
                                     └─ API-001/002        ├─ API-003/004/005/006  ├─ OPS-007 observability    ├─ OPS-001..006 runbooks + capacity
                                     └─ COMP-007 PasswordHasher                    ├─ NFR-COMPLIANCE-001..004  └─ Legacy auth deprecation
                                                                                   └─ TEST-001..006
```

## M1: Foundation — Schemas, Infra, Feature-Flag Plumbing

**Objective:** Provision runtime, data stores, and cross-cutting infrastructure (TLS, CORS, rate-limit hooks, feature flags) and author `UserProfile`/`AuthToken` schemas + audit-log schema so M2 can begin coding against a stable foundation. | **Duration:** 2 weeks (2026-03-31 → 2026-04-14) | **Entry:** INFRA-DB-001 provisioned; SEC-POLICY-001 approved; OQ-CONFLICT-001 + OQ-CONFLICT-002 resolved. | **Exit:** PostgreSQL 15 + Redis 7 + Node.js 20 LTS available in staging; `UserProfile`, `AuthToken`, and `audit_log` migrations applied; feature flags `AUTH_NEW_LOGIN` + `AUTH_TOKEN_REFRESH` registered (default OFF); TLS 1.3 + CORS + API-Gateway rate-limit buckets configured.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|DM-001|UserProfile TypeScript interface + PostgreSQL schema|Author `UserProfile` interface and PostgreSQL DDL with every field from TDD S7.1|`UserProfile`, PostgreSQL|INFRA-DB-001|id:UUID-PK-NOT-NULL; email:varchar-UNIQUE-NOT-NULL-lowercase-indexed; displayName:varchar-NOT-NULL-2-to-100-chars; createdAt:timestamptz-NOT-NULL-DEFAULT-now; updatedAt:timestamptz-NOT-NULL-auto-updated; lastLoginAt:timestamptz-NULLABLE; roles:text[]-NOT-NULL-DEFAULT-{user}; 1:N to refresh_tokens; 1:N to audit_log|M|P0|
|2|DM-002|AuthToken TypeScript interface|Author `AuthToken` DTO contract returned by login/refresh endpoints|`TokenManager`, `AuthService`|DM-001|accessToken:JWT-string-NOT-NULL; refreshToken:opaque-string-NOT-NULL-unique; expiresIn:number-NOT-NULL-value-900; tokenType:string-NOT-NULL-value-Bearer; OAuth2-compatible shape|S|P0|
|3|COMP-005|AuthService skeleton|Scaffold `AuthService` facade with method signatures for login/register/me/refresh/resetRequest/resetConfirm; inject `TokenManager`, `PasswordHasher`, `UserRepo`|`AuthService`|DM-001, DM-002|Class exposes 6 methods; dependency-injection wired; handler stubs return 501; unit test harness boots; no business logic yet|M|P0|
|4|COMP-006|TokenManager skeleton|Scaffold `TokenManager` with issueTokens/refresh/revoke signatures; inject `JwtService`; bind Redis client|`TokenManager`|DM-002|Class exposes 3 methods; Redis client connects on boot; signatures typed; handler stubs return 501|S|P0|
|5|COMP-007|PasswordHasher skeleton|Scaffold `PasswordHasher` abstraction with hash/verify signatures; wire `bcryptjs` dependency|`PasswordHasher`|-|hash(plain):Promise<string> and verify(plain,hash):Promise<boolean> signatures; bcryptjs imported; cost-factor config read from env; stubs return deterministic placeholders|S|P0|
|6|INFRA-001|PostgreSQL 15 provisioning|Provision managed PostgreSQL 15 instance for `UserProfile` + audit_log|PostgreSQL|INFRA-DB-001|Cluster reachable from staging; version=15.x; managed backups enabled; connection-pool defaults (pool=100) applied per OPS-005|M|P0|
|7|INFRA-002|Redis 7 provisioning|Provision managed Redis 7 instance for `TokenManager` refresh-token storage|Redis|INFRA-DB-001|Cluster reachable from staging; version=7.x; 1 GB memory per OPS-006; TLS enabled between service and Redis|S|P0|
|8|INFRA-003|Node.js 20 LTS runtime|Standardize Node.js 20 LTS container base image for `AuthService`|Runtime|-|Base image pinned to node:20-lts; image-scan clean; boot smoke test passes|S|P0|
|9|INFRA-004|TLS 1.3 enforcement at API Gateway|Configure gateway to require TLS 1.3 on all `/v1/auth/*` routes|API Gateway|INFRA-003|TLS<1.3 rejected at gateway; valid cert chain; HSTS header emitted|S|P0|
|10|INFRA-005|CORS allow-list|Restrict CORS to known frontend origins per TDD S13|API Gateway|INFRA-004|Preflight OPTIONS returns allow-list only; wildcard rejected; credentials:true gated on matched origin|S|P0|
|11|INFRA-006|API Gateway rate-limit bucket definitions|Define per-endpoint rate-limit buckets at gateway (enforcement in consuming APIs)|API Gateway|INFRA-004|Bucket schemas registered: /login=10/min/IP; /register=5/min/IP; /me=60/min/user; /refresh=30/min/user; 429 envelope emitted on overflow|S|P0|
|12|MIG-DB-001|UserProfile + audit_log migration scripts|Author idempotent migration for `UserProfile` table and `audit_log` table|PostgreSQL|DM-001|Migration applies clean on empty DB and re-runs idempotently; rollback script reverses both tables; audit_log columns: user_id, event_type, timestamp, ip, outcome (per OPS-007)|M|P0|
|13|COMP-AUDIT-001|Audit log persistence schema (12-month retention)|Create audit_log table with retention policy set to 12 months per NFR-COMPLIANCE-001 (resolves OQ-CONFLICT-001)|PostgreSQL, `AuthService`|DM-001, MIG-DB-001|Retention policy = 12 months (committed value, cites OQ-CONFLICT-001); partitioned by month for reclamation; indexed on (user_id, timestamp) and (event_type, timestamp)|M|P0|
|14|MIG-004|Feature flag AUTH_NEW_LOGIN registration|Register feature flag gating new login/register endpoints; default OFF|Feature-flag service|INFRA-003|Flag registered; default OFF; owner=auth-team; cleanup target documented as Phase 3 GA|S|P0|
|15|MIG-005|Feature flag AUTH_TOKEN_REFRESH registration|Register feature flag gating refresh-token flow; default OFF|Feature-flag service|INFRA-003|Flag registered; default OFF; owner=auth-team; cleanup target documented as Phase 3 + 2 weeks|S|P0|
|16|COMP-POLICY-001|Password policy encoding (NIST SP 800-63B)|Encode password-policy validator per NFR-COMPLIANCE-003 + PRD legal/compliance section|`AuthService`|SEC-POLICY-001|Minimum 8 chars; 1 uppercase; 1 number; NIST SP 800-63B compliant; raw password never logged or persisted; unit test asserts each rule|S|P0|
|17|COMP-CONSENT-001|GDPR consent field on registration payload|Add `consent_given_at:timestamptz` capture plumbing to the registration request envelope per NFR-COMPLIANCE-002|`AuthService`, DM-001|DM-001|Registration request accepts consent flag + timestamp; persisted alongside `UserProfile`; absent consent returns 400 with explanation; unit test covers acceptance + rejection|S|P0|

### Integration Points — M1

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|`AuthService` → `TokenManager`|Dependency injection|No (skeleton)|M1|Wired in M2|
|`AuthService` → `PasswordHasher`|Dependency injection|No (skeleton)|M1|Wired in M2|
|`AuthService` → `UserRepo` (PostgreSQL)|Repository binding|No (skeleton)|M1|Wired in M2|
|`TokenManager` → `JwtService`|Dependency injection|No (skeleton)|M1|Wired in M3|
|API Gateway → rate-limit buckets|Config registry|Yes (schema only)|M1|Enforced in M2 onward|
|Feature-flag client → `AUTH_NEW_LOGIN`/`AUTH_TOKEN_REFRESH`|Flag registry|Yes (OFF)|M1|Toggled in M5|
|Audit log writer → `audit_log` table|Structured log sink|No (schema only)|M1|Emitted in M2 onward|

### Milestone Dependencies — M1

- INFRA-DB-001 (shared infrastructure approval for managed PostgreSQL and Redis)
- SEC-POLICY-001 (password + token policy baseline required for NFR-SEC-001, NFR-SEC-002, NFR-COMPLIANCE-003)
- AUTH-PRD-001 (business-context inputs for consent fields and audit scope)

### Open Questions — M1

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-CONFLICT-001|Audit log retention: TDD S7.2 states 90 days; PRD legal/compliance (NFR-COMPLIANCE-001) requires 12 months for SOC2. Which value applies? Status: **closed**. Resolution: **12 months** (PRD/compliance precedence; cited from COMP-AUDIT-001 and all downstream audit-log references).|Schema partitioning, storage sizing, retention automation|Compliance Lead|2026-03-30 (closed)|
|2|OQ-CONFLICT-002|Milestone structure: TDD S23 uses 5 feature-based milestones (M1 Core, M2 Tokens, M3 Reset, M4 Frontend, M5 GA); this roadmap uses 5 technical-layer milestones. A TDD↔roadmap mapping table is included in Timeline Estimates. Status: **closed**. Resolution: retain roadmap technical-layer phasing; TDD feature-milestone names preserved in mapping table.|Cross-team traceability between TDD and roadmap|Eng Manager + Tech Lead|2026-03-30 (closed)|

### Risk Assessment and Mitigation — M1

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|PostgreSQL or Redis provisioning delay blocks all downstream milestones|High|Medium|All M2+ work blocked|Parallelize provisioning with schema authoring; request infra 1 sprint ahead; local Docker-Compose fallback for dev iteration|platform-team|
|2|Audit log retention conflict (OQ-CONFLICT-001) re-litigated mid-implementation, forcing schema change|Medium|Low|Re-work of COMP-AUDIT-001 + MIG-DB-001|Commit to 12-month value at M1 kickoff; cite OQ resolution in schema comments|Compliance Lead|
|3|Feature-flag plumbing not consumed until M5, drift between flag registry and code|Low|Medium|Flag defaults out of sync at rollout|Acceptance test on flag client asserts default=OFF at boot in M1 and re-asserted in M5 runbook smoke test|auth-team|

## M2: Core Authentication — Registration, Login, Password Hashing

**Objective:** Implement registration + login flows end-to-end (request validation → `PasswordHasher` verify/hash → `UserProfile` persistence → audit emission) and wire `AUTH_NEW_LOGIN`-gated endpoints for POST `/v1/auth/login` and POST `/v1/auth/register`. JWT issuance is scaffolded but refresh flow lands in M3. | **Duration:** 2 weeks (2026-04-15 → 2026-04-28) | **Entry:** M1 exit criteria met; dedicated security-review lead onboarded (pre-M1 risk). | **Exit:** FR-AUTH-001 and FR-AUTH-002 pass unit + integration tests against real PostgreSQL; `PasswordHasher` bcrypt cost-12 verified (NFR-SEC-001); account lockout (5/15min) enforced; rate limits active at gateway; audit log rows emitted for every login attempt and registration event; `AUTH_NEW_LOGIN` remains OFF externally — endpoints accessible to internal test users only (feature-bundle gating for partial flow that still lacks refresh + password reset).

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|18|FR-AUTH-001|Login credential validation flow|Wire `AuthService.login()` to validate email/password via `PasswordHasher.verify()` against stored hash|`AuthService`, `PasswordHasher`|M1, COMP-005, COMP-007|Valid creds return 200 with `AuthToken`; invalid creds return 401 generic; non-existent email returns 401 identical to wrong password (no enumeration); unit test for all three paths|L|P0|
|19|FR-AUTH-002|Registration flow|Wire `AuthService.register()` to validate input, hash password, persist `UserProfile`, emit audit event|`AuthService`, `PasswordHasher`, PostgreSQL|M1, COMP-005, COMP-POLICY-001, COMP-CONSENT-001|Valid registration returns 201 with `UserProfile`; duplicate email returns 409; weak password returns 400 citing failed policy rules; bcrypt hash persisted with cost 12; integration test against testcontainer PostgreSQL|L|P0|
|20|COMP-007a|PasswordHasher.hash implementation|Implement `hash(plaintext):Promise<string>` using bcryptjs with cost factor 12 read from config|`PasswordHasher`|COMP-007|Hash output conforms to bcrypt $2b$ format; cost parameter=12 encoded; raw password never logged; benchmark <500ms per NFR-SEC-001 performance budget|S|P0|
|21|COMP-007b|PasswordHasher.verify implementation|Implement `verify(plaintext, hash):Promise<boolean>` using bcryptjs constant-time compare|`PasswordHasher`|COMP-007|Returns true only for matching pair; constant-time compare used (no early exit); does not throw on malformed hash — returns false; unit test covers match, mismatch, and malformed inputs|S|P0|
|22|NFR-SEC-001|Bcrypt cost factor verification test|Unit test that asserts `PasswordHasher` bcrypt cost factor is exactly 12|`PasswordHasher`|COMP-007a|Test parses $2b$ hash, extracts cost byte, asserts ==12; fails build if cost is 10 or 14; cited explicitly as NFR-SEC-001 verification in test name|S|P0|
|23|API-001|POST /v1/auth/login endpoint|Implement login endpoint per TDD S8.2 with full request/response/error envelope|API Gateway, `AuthService`|FR-AUTH-001, INFRA-006|Request: {email, password}; 200 returns AuthToken; 401 invalid creds; 423 account locked; 429 rate limit; error envelope {error:{code,message,status}}; supertest covers each status code|M|P0|
|24|API-002|POST /v1/auth/register endpoint|Implement registration endpoint per TDD S8.2|API Gateway, `AuthService`|FR-AUTH-002, INFRA-006|Request: {email, password, displayName}; 201 returns `UserProfile`; 400 validation errors citing specific failed rule; 409 duplicate email; error envelope consistent; supertest covers each status|M|P0|
|25|COMP-LOCKOUT-001|Account lockout logic (5 attempts / 15 min)|Track failed attempts per-email in a sliding 15-minute window; lock account on 5th failure; 423 Locked thereafter|`AuthService`, Redis|FR-AUTH-001, INFRA-002|Counter resets on successful login; window is sliding (not calendar); lock expires after 15 minutes from latest failure; returns 423 on locked-state login attempt; unit+integration test cover threshold, reset, expiry|M|P0|
|26|NFR-ENUM-001|Enumeration-safe 401 response|Ensure invalid-email and wrong-password return identical 401 envelope and comparable timing|`AuthService`, `PasswordHasher`|FR-AUTH-001|Dummy bcrypt verify runs on unknown-email path to equalize timing; error body identical; test asserts response-body byte-equality between the two paths|S|P0|
|27|API-001-RATE|Rate limit enforcement /v1/auth/login (10 req/min/IP)|Wire gateway bucket INFRA-006 login config to enforcement layer|API Gateway|INFRA-006, API-001|11th request within 60s returns 429 with envelope; tested via k6 burst scenario; rate-limit counter dimensioned per client IP|S|P0|
|28|API-002-RATE|Rate limit enforcement /v1/auth/register (5 req/min/IP)|Wire gateway bucket INFRA-006 register config|API Gateway|INFRA-006, API-002|6th request within 60s returns 429; tested via k6; dimensioned per client IP|S|P0|
|29|OPS-AUDIT-LOGIN|Audit log emission on login attempt|Emit audit-log row on every login attempt (success + failure) per NFR-COMPLIANCE-001|`AuthService`, audit_log|COMP-AUDIT-001, FR-AUTH-001|Row columns: user_id (nullable for unknown email), event_type=AUTH_LOGIN, timestamp, ip, outcome (SUCCESS|FAILURE|LOCKED); 12-month retention honored; password/token fields never in payload|S|P0|
|30|OPS-AUDIT-REG|Audit log emission on registration|Emit audit-log row on every registration attempt|`AuthService`, audit_log|COMP-AUDIT-001, FR-AUTH-002|Row columns: user_id (on success), event_type=AUTH_REGISTER, timestamp, ip, outcome (SUCCESS|DUPLICATE|WEAK_PASSWORD); consent-given-at persisted separately per NFR-COMPLIANCE-002|S|P0|
|31|NFR-COMPLIANCE-003|NIST SP 800-63B password storage verification|Validate password storage pipeline against NIST SP 800-63B controls|`PasswordHasher`, `AuthService`|COMP-POLICY-001, COMP-007a, COMP-007b|One-way adaptive hashing confirmed (bcrypt cost 12); raw password never persisted; raw password never logged; no reversible transformation; security-review sign-off recorded|S|P0|
|32|NFR-COMPLIANCE-004|GDPR data minimization audit|Audit registration payload + `UserProfile` schema against data-minimization principle|`UserProfile`, `AuthService`|DM-001, FR-AUTH-002|Only email + hashed password + displayName + consent timestamp persisted; no additional PII collected; audit signed off by compliance lead; documented in codebase README|S|P0|
|33|COMP-LOGHYG-001|Password + token log hygiene filter|Install logging middleware that strips any field named password, accessToken, refreshToken, resetToken from log payloads|`AuthService`, logging pipeline|-|Middleware registered in M2; unit test asserts no known-secret field appears in emitted log records; scrub list configurable but defaults cover all TDD-named secrets|S|P0|
|34|TEST-001|Unit: login with valid credentials returns AuthToken|Unit test for `AuthService.login()` happy path per TDD S15.2|Test suite|FR-AUTH-001|Mock `PasswordHasher.verify()` returns true; mock `TokenManager.issueTokens()` returns test AuthToken; result contains accessToken + refreshToken; test named TEST-001|S|P0|
|35|TEST-002|Unit: login with invalid credentials returns error|Unit test for `AuthService.login()` failure path|Test suite|FR-AUTH-001, NFR-ENUM-001|Mock `PasswordHasher.verify()` returns false; response is 401 generic envelope; no AuthToken issued; test named TEST-002|S|P0|
|36|TEST-004|Integration: registration persists UserProfile|Supertest + testcontainer integration test per TDD S15.2|Test suite|FR-AUTH-002|Real PostgreSQL via testcontainer; registration produces UserProfile row with bcrypt hash (cost=12); duplicate registration returns 409; test named TEST-004|M|P0|

### Integration Points — M2

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|`AuthService` → `PasswordHasher.hash/verify`|Dependency injection|Yes|M2|Login, Registration flows|
|`AuthService` → `UserRepo` (PostgreSQL pool)|Repository binding|Yes|M2|Registration persistence, login lookup|
|`AuthService` → audit_log writer|Structured log sink|Yes|M2|OPS-AUDIT-LOGIN, OPS-AUDIT-REG|
|`AuthService` → lockout counter (Redis)|Cache binding|Yes|M2|COMP-LOCKOUT-001|
|API Gateway → `/v1/auth/login`, `/v1/auth/register` handlers|Route table|Yes (gated by AUTH_NEW_LOGIN, internal-only)|M2|External exposure unlocks in M5|
|Log middleware → scrubbing filter|Middleware chain|Yes|M2|All log emitters|

### Milestone Dependencies — M2

- M1 exit criteria (schemas, infra, feature flags)
- Dedicated security-review lead named (required for NFR-SEC-001 / NFR-COMPLIANCE-003 sign-off)
- AUTH_NEW_LOGIN feature flag remains gated to internal tenants only — partial feature exposure prevented per feature-bundle integrity (refresh + reset land in M3)

### Open Questions — M2

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-PRD-003|Account lockout threshold: TDD specifies 5 attempts / 15 minutes; PRD does not confirm a specific threshold. Status: **closed**. Resolution: adopt TDD value **5 attempts within a sliding 15-minute window** (per TDD precedence where PRD is silent); referenced by COMP-LOCKOUT-001.|Lockout UX, brute-force resistance|Security Lead|2026-04-12 (closed)|

### Risk Assessment and Mitigation — M2

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-002 Brute-force attacks on login endpoint|Medium|High|Credential-stuffing success|Gateway rate limiting (10/min/IP); account lockout 5/15min (COMP-LOCKOUT-001); bcrypt cost 12; contingency: WAF IP block + CAPTCHA deferred to M4|Security Lead|
|2|Timing side-channel leaks email existence despite 401 parity|Medium|Medium|User enumeration possible|NFR-ENUM-001 dummy bcrypt on unknown-email path; response-body byte-equality test; periodic timing-comparison test in CI|Security Lead|
|3|R-PRD-002 Security breach from implementation flaws|Critical|Low|Reputational + compliance failure|Dedicated security review scheduled end-of-M2 before M3 cryptographic work; penetration testing queued for M4|sec-reviewer|

## M3: Token Management & Session — JWT, Refresh, Password Reset

**Objective:** Complete the authentication feature bundle: `TokenManager` + `JwtService` RS256 signing, refresh-token lifecycle (Redis, 7-day TTL, hashed), silent refresh flow, password-reset request + confirm (SendGrid), and `/v1/auth/me` profile retrieval. `AUTH_TOKEN_REFRESH` flag remains OFF externally — unlocks in M5. | **Duration:** 2 weeks (2026-04-29 → 2026-05-12) | **Entry:** M2 exit criteria met; security review sign-off on cryptographic approach. | **Exit:** FR-AUTH-003, FR-AUTH-004, FR-AUTH-005 pass unit + integration tests; RS256 2048-bit RSA key rotation procedure documented and dry-run passes (NFR-SEC-002); refresh-token flow hashed and TTL-enforced in Redis; password-reset email delivered via SendGrid within 60s and 1-hour TTL enforced; all 6 API endpoints respond with correct envelope.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|37|FR-AUTH-003|JWT access + refresh token issuance and refresh|Implement token issuance (15-min access, 7-day refresh) and refresh flow via `TokenManager` + `JwtService`|`TokenManager`, `JwtService`|COMP-006, COMP-JWT-001|Login returns both tokens with TTLs exactly 900s access / 604800s refresh; POST /refresh with valid refreshToken returns new AuthToken pair; expired refreshToken returns 401; revoked refreshToken returns 401; unit + integration test|L|P0|
|38|COMP-JWT-001|JwtService.sign / verify with RS256|Implement `JwtService` using jsonwebtoken with RS256 and 2048-bit RSA keys|`JwtService`|COMP-006|sign() uses RS256; verify() rejects tokens signed with other algorithms (no alg=none bypass); public key distributable for downstream services; 5-second clock-skew tolerance per TDD S12|M|P0|
|39|NFR-SEC-002|RS256 2048-bit RSA key configuration verification|Automated config-validation test asserts key length = 2048 bits and algorithm = RS256|`JwtService`|COMP-JWT-001|Test parses loaded private key; asserts modulus length = 2048; asserts JWT header alg = RS256; fails build if key is RSA-1024 or HS256|S|P0|
|40|COMP-KEYROT-001|Quarterly RS256 key rotation procedure|Document and implement key-rotation procedure per TDD S13; old key honored during grace window|`JwtService`, config store|COMP-JWT-001|Rotation runbook published; dry-run in staging succeeds; verify() accepts tokens signed by current AND previous key during grace window; alerts fire 14 days before key age exceeds quarter|M|P0|
|41|COMP-006a|TokenManager.issueTokens implementation|Issue access JWT + opaque refresh token; hash refresh token; persist to Redis with 7-day TTL keyed by user id|`TokenManager`, Redis|COMP-006, INFRA-002|Returns `AuthToken`; refresh token stored as SHA-256 hash in Redis (never plain); Redis key pattern documented; TTL exactly 604800s; unit + integration test|M|P0|
|42|COMP-006b|TokenManager.refresh implementation|Validate refresh token (look up hash in Redis), revoke old, issue new pair|`TokenManager`, Redis, `JwtService`|COMP-006a|Unknown refresh token returns 401; expired (Redis TTL elapsed) returns 401; valid token: old Redis entry deleted, new pair issued; distinguishes expired vs revoked in structured logs|M|P0|
|43|COMP-006c|TokenManager.revoke implementation|Explicit refresh-token revocation (used by password reset + logout)|`TokenManager`, Redis|COMP-006a|Delete Redis entry by hashed-token key; idempotent; safe on unknown token; emits audit event AUTH_TOKEN_REVOKE|S|P0|
|44|API-004|POST /v1/auth/refresh endpoint|Implement refresh endpoint per TDD S8.2|API Gateway, `AuthService`, `TokenManager`|FR-AUTH-003, COMP-006b, INFRA-006|Request: {refreshToken}; 200 returns new AuthToken pair with old revoked; 401 on expired or revoked; rate limit 30/min/user; error envelope consistent|M|P0|
|45|API-004-RATE|Rate limit enforcement /v1/auth/refresh (30 req/min/user)|Wire gateway bucket per INFRA-006|API Gateway|INFRA-006, API-004|31st request in 60s returns 429; dimensioned per user id (from resolved refresh token); tested via k6|S|P0|
|46|FR-AUTH-004|User profile retrieval|Implement `AuthService.me()` returning the authenticated user's `UserProfile`|`AuthService`, `UserRepo`|COMP-005, DM-001|Valid accessToken returns id, email, displayName, createdAt, updatedAt, lastLoginAt, roles; expired/invalid returns 401; lastLoginAt updates on each successful /login in parallel path|M|P0|
|47|API-003|GET /v1/auth/me endpoint|Implement profile endpoint per TDD S8.2|API Gateway, `AuthService`|FR-AUTH-004, INFRA-006|Requires Authorization: Bearer <jwt>; 200 returns full `UserProfile`; 401 on missing/expired/invalid token; rate limit 60/min/user|S|P0|
|48|API-003-RATE|Rate limit enforcement /v1/auth/me (60 req/min/user)|Wire gateway bucket per INFRA-006|API Gateway|INFRA-006, API-003|61st request in 60s returns 429; dimensioned per user id; tested via k6|S|P0|
|49|FR-AUTH-005|Password reset flow (request + confirm)|Two-step reset: request sends email with 1-hour TTL token; confirm validates token, updates hash, invalidates all sessions|`AuthService`, `PasswordHasher`, `TokenManager`, SendGrid|COMP-005, COMP-007a, COMP-006c|/reset-request sends reset email via SendGrid; /reset-confirm with valid token updates password hash; token expires after 1 hour; used tokens cannot be reused; all existing refresh tokens revoked on successful reset|L|P0|
|50|API-005|POST /v1/auth/reset-request endpoint|Implement reset-request endpoint per TDD S8|API Gateway, `AuthService`|FR-AUTH-005|Request: {email}; response is enumeration-safe generic confirmation regardless of whether email exists; reset token generated server-side; email dispatched via SendGrid within 60s SLA|M|P0|
|51|API-006|POST /v1/auth/reset-confirm endpoint|Implement reset-confirm endpoint per TDD S8|API Gateway, `AuthService`|FR-AUTH-005|Request: {resetToken, newPassword}; 200 on success; 401 if token expired or already used; 400 if new password fails policy; all refresh tokens for user revoked on success|M|P0|
|52|COMP-RESET-001|Reset-token 1-hour TTL + single-use enforcement|Store reset tokens in Redis with 3600s TTL; mark used atomically on redemption|Redis, `AuthService`|COMP-006, FR-AUTH-005|TTL exactly 3600s; atomic compare-and-delete on redemption prevents replay; second-use attempt returns 401; unit + integration test|S|P0|
|53|COMP-SENDGRID-001|SendGrid integration for password reset emails|Wire SendGrid SDK, template, and delivery monitoring|`AuthService`, SendGrid|FR-AUTH-005|Email template approved by product; delivery attempted via SendGrid API; delivery failure logged with correlation id; retry policy: 3 attempts with exponential backoff; fallback alert fires if >5% failure rate per R-PRD-004|M|P0|
|54|NFR-ENUM-002|Reset-request enumeration safety|Ensure /reset-request returns identical response for registered and unregistered emails|`AuthService`|API-005|Response body byte-identical between the two paths; no email sent for unregistered address but response timing comparable (no short-circuit); test asserts both paths|S|P0|
|55|COMP-RESET-INVALIDATE|Reset invalidates all existing sessions|On successful password reset, revoke every refresh token associated with the user id|`TokenManager`, Redis|COMP-006c, FR-AUTH-005|Integration test: user has 3 active refresh tokens; reset confirmation deletes all 3; subsequent /refresh attempts on those tokens return 401; audit event emitted per revoked token|S|P0|
|56|COMP-ENVELOPE-001|Standard error envelope across all 6 endpoints|Enforce {error:{code,message,status}} envelope on all 4xx/5xx responses across API-001..006|API Gateway, `AuthService`|API-001..006|Contract test runs against all endpoints and asserts error body shape; error codes catalogued (AUTH_INVALID_CREDENTIALS, AUTH_ACCOUNT_LOCKED, AUTH_RATE_LIMITED, AUTH_TOKEN_EXPIRED, AUTH_TOKEN_REVOKED, AUTH_EMAIL_EXISTS, AUTH_WEAK_PASSWORD, AUTH_RESET_TOKEN_INVALID)|S|P0|
|57|COMP-CLOCKSKEW-001|5-second clock-skew tolerance in JwtService|Configure jsonwebtoken verify options with 5s clockTolerance per TDD S12|`JwtService`|COMP-JWT-001|Unit test: token exp=now-3s still verifies; token exp=now-10s fails; test named COMP-CLOCKSKEW-001|S|P0|
|58|COMP-HTTPONLY-001|HttpOnly cookie contract for refreshToken|Define server-side cookie-emission contract: refreshToken Set-Cookie with HttpOnly, Secure, SameSite=Strict|`AuthService`, API Gateway|FR-AUTH-003|/login and /refresh set Set-Cookie with HttpOnly=true, Secure=true, SameSite=Strict, Path=/v1/auth; accessToken NOT in cookie; frontend consumption in M4|S|P0|
|59|TEST-003|Unit: token refresh with valid refresh token|Unit test for `TokenManager.refresh()` happy path per TDD S15.2|Test suite|COMP-006b|Mock Redis returns valid hashed token; new AuthToken pair returned; old Redis entry deleted; new entry added; test named TEST-003|S|P0|
|60|TEST-005|Integration: expired refresh token rejected|testcontainer integration test per TDD S15.2|Test suite, Redis|COMP-006b|Token stored with TTL=1s; wait 2s; /refresh returns 401; test named TEST-005|S|P0|

### Integration Points — M3

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|`TokenManager` → `JwtService`|Dependency injection|Yes|M3|issueTokens, refresh|
|`TokenManager` → Redis refresh-token store|Cache binding|Yes|M3|issueTokens, refresh, revoke|
|`AuthService` → SendGrid|External API client|Yes|M3|Password reset emails|
|`AuthService` → reset-token store (Redis)|Cache binding|Yes|M3|COMP-RESET-001|
|API Gateway → /v1/auth/refresh, /v1/auth/me, /v1/auth/reset-request, /v1/auth/reset-confirm|Route table|Yes (AUTH_TOKEN_REFRESH gated for refresh)|M3|External exposure in M5|
|JWT verifier (downstream services)|Public-key distribution|Yes|M3|Any service validating `AuthService`-issued tokens|

### Milestone Dependencies — M3

- M2 exit criteria
- Security-review sign-off on key-rotation procedure (COMP-KEYROT-001)
- SendGrid account provisioned with verified sender identity (R-PRD-004 mitigation)

### Open Questions — M3

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-002|Maximum allowed `UserProfile.roles` array length? Pending RBAC design review. **Status: open.** Does not block M3 functional code since M3 treats roles as an opaque string[], but the length ceiling must be set before RBAC enforcement lands downstream.|Storage sizing, RBAC downstream design|auth-team|2026-05-10|
|2|OQ-PRD-001|Password reset emails sent synchronously or asynchronously? **Status: open.** Current M3 implementation (COMP-SENDGRID-001) fires asynchronously with 3-attempt retry backoff to absorb SendGrid latency; confirm asynchronous choice is acceptable given the 60s delivery SLA.|Reset UX perceived latency|Engineering Lead|2026-05-08|
|3|OQ-PRD-002|Maximum number of refresh tokens per user across devices? **Status: open.** Current M3 implementation permits unbounded concurrent devices (multi-device concurrent login is expected per PRD edge-case table); a ceiling would add bounded revocation behavior but was not specified.|Redis memory sizing, multi-device UX|Product|2026-05-10|
|4|OQ-001|Should `AuthService` support API key authentication for service-to-service calls? **Status: closed.** Resolution: **deferred to v1.1 scope** per TDD S22 and PRD S12.2 Out-of-Scope. Not relitigated in any M3 deliverable AC per Non-Goals rule.|-|test-lead|2026-04-15 (closed, deferred to v1.1)|
|5|OQ-PRD-004|Support "remember me" to extend session duration? **Status: closed.** Resolution: **out of scope for v1.0** per PRD S12.2 Out-of-Scope (would require session-duration override conflicting with the fixed 7-day refresh TTL). Revisit in v1.1 planning.|-|Product|2026-04-15 (closed, deferred)|

### Risk Assessment and Mitigation — M3

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-001 Token theft via XSS allows session hijacking|Medium|High|Compromised session|accessToken in-memory only (frontend contract in M4); refreshToken via HttpOnly+Secure+SameSite=Strict cookie (COMP-HTTPONLY-001); 15-min access token expiry; hashed refresh tokens in Redis; contingency: `TokenManager.revoke` + force password reset|Security Lead|
|2|Incorrect RS256 configuration (e.g., alg=none bypass, key too short)|Critical|Low|Token forgery|COMP-JWT-001 rejects non-RS256 tokens; NFR-SEC-002 test asserts key length; security review before M3 exit|sec-reviewer|
|3|R-PRD-004 Email delivery failures block password reset|Medium|Medium|User cannot recover account|COMP-SENDGRID-001 delivery monitoring with 3-attempt retry; alert on >5% failure rate; fallback support channel documented in M5 runbook|auth-team|
|4|Replay of reset tokens|Medium|Medium|Account takeover|COMP-RESET-001 atomic compare-and-delete on redemption; 1-hour TTL; single-use enforced at Redis layer (not application-level only)|Security Lead|

## M4: Integration & Hardening — Frontend, Observability, Compliance

**Objective:** Ship frontend consumption surfaces (`AuthProvider`, `LoginPage`, `RegisterPage`, `ProfilePage`), full observability stack (Prometheus metrics, OTel tracing, structured logs, alerts), compliance validation (SOC2 audit queryability, GDPR consent + minimization sign-off), performance + load validation, security hardening (penetration test, CAPTCHA, log-hygiene re-audit), and all test-pyramid layers. | **Duration:** 2 weeks (2026-05-13 → 2026-05-26) | **Entry:** M3 exit criteria met; staging environment provisioned with seeded test accounts. | **Exit:** All 3 frontend pages + `AuthProvider` pass E2E tests (TEST-006); Prometheus metrics + alerts live in staging; OTel traces flow through `AuthService` → `PasswordHasher`/`TokenManager` → `JwtService`; p95 <200ms confirmed under 500 concurrent users (NFR-PERF-002); penetration test findings triaged; SOC2 audit-log query interface signed off by compliance.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|61|COMP-001|LoginPage React component|Implement `/login` page consuming POST /v1/auth/login; store AuthToken via `AuthProvider`|`LoginPage`|API-001, COMP-004|Props: onSuccess:() => void, redirectUrl?:string; renders email + password fields; submits to /login; on 200 stores tokens via AuthProvider; displays generic error on 401; disables submit during pending|M|P0|
|62|COMP-002|RegisterPage React component|Implement `/register` page with client-side password policy validation and GDPR consent checkbox|`RegisterPage`|API-002, COMP-CONSENT-001, COMP-POLICY-001|Props: onSuccess:() => void, termsUrl:string; renders email + password + displayName + consent fields; client-side password-strength check before POST; 409 shows email-exists message; submits consent_given_at with registration|M|P0|
|63|COMP-003|ProfilePage React component|Implement `/profile` page consuming GET /v1/auth/me|`ProfilePage`|API-003, COMP-004|Auth required; renders `UserProfile` (displayName, email, createdAt); on 401 redirects to /login via AuthProvider|S|P0|
|64|COMP-004|AuthProvider React context|Implement context provider wrapping app; manages AuthToken in-memory, orchestrates refresh, intercepts 401s|`AuthProvider`|COMP-HTTPONLY-001, API-004|Props: children:ReactNode; accessToken held in memory (not localStorage) per R-001; refreshToken sent via HttpOnly cookie on /refresh; silent refresh 60s before expiry; 401 interceptor triggers refresh-then-retry once, else redirects to /login|L|P0|
|65|COMP-SILENT-REFRESH|AuthProvider silent refresh scheduler|Schedule refresh attempt 60s before accessToken expiry|`AuthProvider`|COMP-004|Timer fires at exp-60s; calls /refresh; on success updates in-memory accessToken; on 401 clears state and redirects to /login; tested via jest fake timers|S|P0|
|66|COMP-401-INT|AuthProvider 401 response interceptor|Global axios/fetch wrapper intercepts 401, triggers one refresh retry, else logs out|`AuthProvider`|COMP-004, COMP-SILENT-REFRESH|Interceptor wraps all API calls; on 401 calls /refresh; if refresh succeeds, retries original request once; if refresh fails, clears state + redirects /login; infinite-retry-loop guard in place|S|P0|
|67|COMP-CAPTCHA-001|CAPTCHA challenge on LoginPage after 3 failed attempts|Per-IP client-side tracker surfaces CAPTCHA challenge after 3 failures per R-002 contingency|`LoginPage`|COMP-001|After 3 failed /login responses within session, CAPTCHA widget rendered; submit blocked until solved; server-side lockout (COMP-LOCKOUT-001) remains authoritative at 5 failures|S|P1|
|68|OPS-007-LOG|Structured logs for all auth events|Emit structured JSON logs for login (success/failure), registration, refresh, password-reset request/confirm|Logging pipeline, `AuthService`|OPS-AUDIT-LOGIN, OPS-AUDIT-REG|Every endpoint emits 1 structured log line on success + 1 on failure; fields: correlation_id, event_type, user_id (when known), outcome, duration_ms; passwords/tokens scrubbed per COMP-LOGHYG-001|S|P0|
|69|OPS-007-M1|Prometheus metric `auth_login_total`|Counter metric dimensioned by outcome|`AuthService`, Prometheus|OPS-007-LOG|Counter increments on every /login attempt; labels: outcome={success,invalid_creds,locked,rate_limited}; metric name verbatim `auth_login_total`|S|P0|
|70|OPS-007-M2|Prometheus metric `auth_login_duration_seconds`|Histogram metric for login endpoint latency|`AuthService`, Prometheus|OPS-007-LOG|Histogram with standard buckets (5ms..5s); labels: outcome; p95 calculable for NFR-PERF-001 validation; metric name verbatim `auth_login_duration_seconds`|S|P0|
|71|OPS-007-M3|Prometheus metric `auth_token_refresh_total`|Counter metric dimensioned by outcome|`TokenManager`, Prometheus|OPS-007-LOG|Counter labels: outcome={success,expired,revoked,unknown}; metric name verbatim `auth_token_refresh_total`|S|P0|
|72|OPS-007-M4|Prometheus metric `auth_registration_total`|Counter metric dimensioned by outcome|`AuthService`, Prometheus|OPS-007-LOG|Counter labels: outcome={success,duplicate_email,weak_password,validation_error}; metric name verbatim `auth_registration_total`|S|P0|
|73|OPS-007-TRACE|OpenTelemetry distributed tracing|Instrument spans across `AuthService` → `PasswordHasher` / `TokenManager` → `JwtService`|Observability stack|OPS-007-LOG|Parent span per /auth/* request; child spans for PasswordHasher.verify, TokenManager.issueTokens, JwtService.sign; correlation_id propagated; traces visible in staging APM|M|P0|
|74|OPS-007-A1|Alert: login failure rate >20% over 5 min|Configure alert rule on `auth_login_total{outcome="invalid_creds"}` ratio|Alerting system|OPS-007-M1|Alert fires when rate(failure)/rate(total) over 5m >0.2; routes to auth-team on-call; named auth-login-failure-rate-alert|S|P0|
|75|OPS-007-A2|Alert: p95 login latency >500ms|Configure alert on `auth_login_duration_seconds` p95|Alerting system|OPS-007-M2|Alert fires when histogram_quantile(0.95) over 5m >500ms; routes to auth-team on-call; distinct from rollback trigger threshold (1000ms/5m in M5)|S|P0|
|76|OPS-007-A3|Alert: Redis connection failures from TokenManager|Configure alert on Redis client error counter|Alerting system, Redis client|COMP-006|Alert fires when TokenManager Redis error rate >1/min over 5m; routes to auth-team + platform-team; distinct from rollback trigger >10/min in M5|S|P0|
|77|NFR-COMPLIANCE-001|SOC2 audit log queryability (12-month retention)|Provide query interface for audit log by date range + user id per PRD legal/compliance|audit_log, query API|COMP-AUDIT-001, OPS-AUDIT-LOGIN, OPS-AUDIT-REG|12-month retention verified with partition-expiry test; query interface available to Jordan admin persona; SOC2 controls checklist signed off by compliance|M|P0|
|78|NFR-COMPLIANCE-002|GDPR consent recording end-to-end|Validate consent_given_at captured, persisted, and exportable|`AuthService`, `UserProfile`|COMP-CONSENT-001, FR-AUTH-002|E2E test: registration without consent rejected; registration with consent persisted with timestamp; data-export request returns consent record; legal sign-off recorded|S|P0|
|79|NFR-PERF-001|API response time validation (all endpoints p95 <200ms)|APM-instrumented measurement of every /auth/* endpoint under realistic load|Observability stack|OPS-007-M2, OPS-007-TRACE|All 6 endpoints measured p95 <200ms in staging; verbatim target ("<200ms at p95"); results captured in release-report artifact; deviation triggers hold on M5|M|P0|
|80|NFR-PERF-002|500 concurrent login load test (k6)|k6 script sustains 500 concurrent /login requests; validate no errors and latency envelope|k6, staging env|NFR-PERF-001, OPS-004|500 concurrent users sustained for 10 minutes; error rate <0.1%; p95 <200ms; HPA scaling behavior matches OPS-004 plan; results archived|M|P0|
|81|NFR-REL-001|99.9% availability monitoring configuration|Configure uptime monitor over 30-day rolling windows via health check endpoint|Health check, monitoring|OPS-HEALTH-001|SLO dashboard in Grafana; verbatim target ("99.9% uptime over 30-day rolling windows"); error budget computed; burn-rate alerts configured|S|P0|
|82|OPS-HEALTH-001|Health check endpoint|Implement GET /v1/auth/health for liveness + readiness probes|`AuthService`|INFRA-003|/health returns 200 when AuthService + PostgreSQL + Redis reachable; 503 when any dependency unhealthy; probe cadence 10s|S|P0|
|83|SEC-PENTEST-001|External penetration test per R-PRD-002|Engage external security vendor for black-box + grey-box testing|Security vendor|M3 exit, COMP-JWT-001|Scope covers all 6 endpoints + AuthProvider XSS surface; findings triaged within 5 business days; all Critical + High findings remediated before M5 entry; report archived|L|P0|
|84|COMP-LOGHYG-002|Log hygiene re-audit post-integration|Re-verify no password, token, or reset-token leakage after frontend + observability integration|Logging pipeline|COMP-LOGHYG-001, OPS-007-LOG, OPS-007-TRACE|Random sample of 1000 log records + 1000 trace spans scanned; zero secret fields present; test runs in CI against ephemeral staging|S|P0|
|85|TEST-006|E2E: user registers and logs in|Playwright E2E test covering full journey through frontend per TDD S15.2|Test suite, Playwright|COMP-001, COMP-002, COMP-003, COMP-004|Playwright test: Register → redirected to login → login → lands on ProfilePage showing UserProfile; runs against staging; test named TEST-006; runs in CI pipeline|M|P0|
|86|JTBD-GAP-001|Admin audit-log view (PRD JTBD gap fill)|Minimal admin-scoped query surface for Jordan persona "see who attempted access and lock compromised accounts"|Admin UI or CLI, audit_log|NFR-COMPLIANCE-001|Read-only query of audit_log by user id + date range; lock-account call invokes COMP-LOCKOUT-001; scoped to admin role (enforcement downstream — roles tagged but RBAC out of scope per NG-003); interim surface is admin CLI since full admin UI is TDD gap|M|P1|
|87|SUCC-METRIC-001|Funnel telemetry: registration conversion >60%|Emit funnel events from RegisterPage land → submit → confirmed account|`RegisterPage`, analytics pipeline|COMP-002, OPS-007-LOG|Verbatim target: registration conversion >60%; funnel events emitted with correlation_id; dashboard live in staging; reviewed before M5|S|P0|
|88|SUCC-METRIC-002|Funnel telemetry: password reset completion >80%|Emit funnel events from reset-request → email link click → reset-confirm success|`AuthService`, analytics pipeline|FR-AUTH-005, OPS-007-LOG|Verbatim target: password reset completion >80%; funnel events emitted; dashboard live|S|P0|
|89|SUCC-METRIC-003|Session duration telemetry (>30 min average)|Emit token refresh event analytics to compute session duration|`TokenManager`, analytics pipeline|COMP-006b, OPS-007-M3|Verbatim target: average session duration >30 minutes; derived from refresh cadence; dashboard live|S|P0|
|90|SUCC-METRIC-004|Failed-login-rate telemetry (<5% of attempts)|Emit auth-event-log analysis view for failed login rate|audit_log, analytics pipeline|OPS-AUDIT-LOGIN, OPS-007-M1|Verbatim target: failed login rate <5% of attempts; computed from auth_login_total{outcome="invalid_creds"}/total; dashboard live|S|P0|
|91|SUCC-METRIC-005|Daily active authenticated users telemetry|Track `AuthToken` issuance counts per day|`TokenManager`, analytics pipeline|OPS-007-M1, OPS-007-M3|Verbatim target: >1000 DAU within 30 days of GA; dashboard live; baseline captured pre-GA|S|P0|
|92|SUCC-METRIC-006|Password hash time benchmark (<500ms)|CI benchmark of `PasswordHasher.hash()` with cost 12|CI, `PasswordHasher`|COMP-007a|Verbatim target: password hash time <500ms; CI benchmark fails build if regression detected; result captured per commit|S|P0|

### Integration Points — M4

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|React App → `AuthProvider` context|React context provider|Yes|M4|All protected + public routes|
|`AuthProvider` → fetch/axios 401 interceptor|Middleware chain|Yes|M4|All frontend API calls|
|`AuthService` + `TokenManager` → Prometheus scrape|Metrics registry|Yes|M4|Grafana dashboards, alerts|
|`AuthService` + `PasswordHasher` + `TokenManager` + `JwtService` → OTel exporter|Tracing pipeline|Yes|M4|APM/staging tracing|
|audit_log table → admin query CLI (JTBD-GAP-001)|Read API|Yes|M4|Jordan admin persona|
|Funnel analytics events → pipeline|Event emitter|Yes|M4|Success-metric dashboards|
|Penetration-test harness → all endpoints|External vendor engagement|Yes|M4|Security sign-off|

### Milestone Dependencies — M4

- M3 exit criteria (all 6 API endpoints live, AUTH_TOKEN_REFRESH feature flag available)
- External penetration-test vendor engaged 2 weeks prior
- Grafana + Prometheus + OTel collector deployed in staging

### Open Questions — M4

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|JTBD-GAP-001-OQ|PRD JTBD "see who attempted access and lock compromised accounts" (Jordan admin persona) lacks a dedicated FR in the TDD. Interim interface is an admin CLI over audit_log (JTBD-GAP-001 deliverable). Should a full admin UI be added to v1.0 scope or deferred to v1.1? **Status: open.** Resolution: **PRD requires; TDD should be updated** — recommend deferring full UI to v1.1 while shipping CLI in v1.0 to close the behavioral gap.|Admin UX parity with PRD JTBD|Product + Eng Manager|2026-05-20|

### Risk Assessment and Mitigation — M4

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-001 Token theft via XSS on frontend|High|Medium|Session hijacking|accessToken in-memory only in AuthProvider (COMP-004); refreshToken via HttpOnly+Secure+SameSite=Strict (COMP-HTTPONLY-001); CSP headers at gateway; penetration-test surface (SEC-PENTEST-001) covers XSS|Security Lead|
|2|R-PRD-001 Low registration adoption due to poor UX|High|Medium|Under-shoots >60% conversion target|Usability test scheduled on RegisterPage before M5; funnel iteration based on SUCC-METRIC-001; contingency: iterate UX in first post-GA sprint|Product|
|3|R-PRD-003 Compliance failure from incomplete SOC2 audit logging|High|Medium|Q3 SOC2 audit failure|NFR-COMPLIANCE-001 query interface signed off before M5 entry; 12-month retention verified via partition-expiry test; audit events logged for every FR-AUTH-001..005 path|Compliance Lead|
|4|OTel/Prometheus instrumentation adds latency regressing NFR-PERF-001|Medium|Low|p95 slips past 200ms|Before/after benchmark; sampling configured for traces; histogram bucket count bounded; back-out plan: disable tracing in production if regression >10%|auth-team|
|5|Penetration test findings emerge late and block M5 entry|High|Medium|GA delayed|Vendor engaged 2 weeks before M4 start; weekly interim reports; Critical/High findings triaged within 5 business days; buffer within M4 duration|sec-reviewer|

## M5: Production Readiness & GA — Rollout, Runbooks, Capacity

**Objective:** Execute the three-phase rollout (Internal Alpha → Beta 10% → GA 100%), deliver runbooks + on-call rotation + capacity plans, automate rollback triggers, deprecate legacy auth, and retire the gating feature flags. | **Duration:** 2 weeks (2026-05-27 → 2026-06-09) | **Entry:** M4 exit criteria met; SEC-PENTEST-001 Critical + High findings closed; compliance sign-off in hand. | **Exit:** 100% of traffic on new `AuthService`; `AUTH_NEW_LOGIN` removed; `AUTH_TOKEN_REFRESH` scheduled for removal 2 weeks post-GA; 99.9% uptime over first 7 days of GA; all rollback triggers wired with automatic activation; runbooks tested; on-call rotation live; legacy auth deprecated and removal timeline communicated.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|93|MIG-001|Phase 1: Internal Alpha deploy|Deploy `AuthService` to staging; auth-team + QA test all endpoints; LoginPage/RegisterPage behind AUTH_NEW_LOGIN=ON for internal tenants only|`AuthService`, staging|M4 exit, MIG-004|1-week duration; all FR-AUTH-001..005 pass manual testing; zero P0/P1 bugs; exit gate signed off by test-lead before proceeding to MIG-002|M|P0|
|94|MIG-002|Phase 2: Beta 10% traffic|Enable AUTH_NEW_LOGIN for 10% of traffic; monitor latency, error rates, Redis usage|`AuthService`, production|MIG-001|2-week duration; p95 <200ms sustained; error rate <0.1%; no Redis connection failures from TokenManager; exit gate signed off by eng-manager|M|P0|
|95|MIG-003|Phase 3: General Availability (100%)|Remove AUTH_NEW_LOGIN; all users route to new AuthService; enable AUTH_TOKEN_REFRESH; legacy deprecated|`AuthService`, production|MIG-002|1-week duration; 99.9% uptime over 7 days; all dashboards green; AUTH_NEW_LOGIN removed from codebase; AUTH_TOKEN_REFRESH scheduled for removal at GA+14 days|M|P0|
|96|MIG-004-CLEANUP|AUTH_NEW_LOGIN feature flag removal|Remove flag code + usages after Phase 3 GA per TDD S19.2 cleanup target|Feature-flag service, codebase|MIG-003|Flag removed from registry; all conditional code paths simplified to ON behavior; PR reviewed; owner=auth-team per TDD S19.2|S|P0|
|97|MIG-005-CLEANUP|AUTH_TOKEN_REFRESH feature flag removal|Remove flag code + usages 2 weeks after Phase 3 GA per TDD S19.2 cleanup target|Feature-flag service, codebase|MIG-003|Flag removed 2026-06-23 (GA+14d); all conditional code paths simplified; owner=auth-team per TDD S19.2|S|P0|
|98|OPS-ROLLBACK-001|Rollback procedure automation (ordered steps)|Implement rollback runbook as automated/documented procedure with every step from TDD S19.3 in order|Runbook, ops tooling|MIG-004|Ordered checklist encoded verbatim: (1) Disable AUTH_NEW_LOGIN flag; (2) Verify legacy login via smoke tests; (3) Investigate AuthService root cause via logs + traces; (4) If UserProfile data corruption detected, restore from last known-good backup; (5) Notify auth-team + platform-team via incident channel; (6) Post-mortem within 48 hours of rollback; each step has named owner + verification evidence|M|P0|
|99|OPS-ROLLBACK-T1|Automated rollback trigger: p95 latency >1000ms for >5 min|Configure automated trigger to execute OPS-ROLLBACK-001 when threshold breached|Alerting + flag service|OPS-007-M2, OPS-ROLLBACK-001|Trigger wired from day 1 of MIG-001 per TDD S19.4 (source phrasing "Triggered if any of the following occur" → automatic); threshold verbatim ">1000ms for >5 minutes"; dry-run verified in staging; no human-confirmation gate inserted (preserves TDD contract)|M|P0|
|100|OPS-ROLLBACK-T2|Automated rollback trigger: error rate >5% for >2 min|Configure automated trigger per TDD S19.4|Alerting + flag service|OPS-007-M1, OPS-ROLLBACK-001|Automated from day 1; threshold verbatim ">5% for >2 minutes"; dry-run verified in staging|S|P0|
|101|OPS-ROLLBACK-T3|Automated rollback trigger: Redis connection failures >10/min|Configure automated trigger per TDD S19.4|Alerting + flag service|OPS-007-A3, OPS-ROLLBACK-001|Automated from day 1; threshold verbatim ">10 per minute" (distinct from OPS-007-A3 operational alert at >1/min); dry-run verified in staging|S|P0|
|102|OPS-ROLLBACK-T4|Automated rollback trigger: UserProfile data corruption detected|Configure automated trigger on data-integrity probe|Data integrity probe, flag service|MIG-DB-001, OPS-ROLLBACK-001|Data-integrity probe runs hourly in production; on detection of UserProfile record inconsistency, rollback triggered immediately and backup-restore step (step 4) invoked; probe definition and false-positive runbook documented|M|P0|
|103|OPS-001|Runbook: AuthService down|Publish runbook per TDD S25.1|Runbook, on-call|OPS-007-LOG, OPS-HEALTH-001|Symptoms, diagnosis, resolution, escalation documented verbatim from TDD S25.1; escalation: auth-team on-call → 15 min unresolved → platform-team; tested in staging during MIG-001|S|P0|
|104|OPS-002|Runbook: Token refresh failures|Publish runbook per TDD S25.1|Runbook, on-call|OPS-007-A3, MIG-005|Symptoms, diagnosis, resolution, escalation documented verbatim; covers Redis connectivity, JwtService key access, AUTH_TOKEN_REFRESH state; tested in staging|S|P0|
|105|OPS-003|On-call rotation setup (24/7 for first 2 weeks post-GA)|Configure PagerDuty/equivalent; define escalation path|On-call platform|OPS-001, OPS-002|Rotation live before MIG-001; auth-team provides 24/7 for first 2 weeks per TDD S25.2; P1 ack ≤15 min; escalation: on-call → test-lead → eng-manager → platform-team|S|P0|
|106|OPS-004|Capacity plan: AuthService pods (HPA)|Configure Kubernetes HPA per TDD S25.3|K8s, `AuthService`|INFRA-003|3 replicas baseline; HPA scales to 10 replicas at CPU >70%; capacity validated against 500 concurrent users from NFR-PERF-002; config reviewed|S|P0|
|107|OPS-005|Capacity plan: PostgreSQL connection pool|Configure pool sizing per TDD S25.3|PostgreSQL|INFRA-001|100 pool baseline; scale trigger: pool wait time >50ms → increase to 200; monitored via Prometheus pool-wait metric|S|P0|
|108|OPS-006|Capacity plan: Redis memory sizing|Configure Redis memory + scale trigger per TDD S25.3|Redis|INFRA-002|1 GB baseline; expected ~100K refresh tokens (~50 MB); scale trigger: >70% utilization → increase to 2 GB; monitored via Redis INFO memory|S|P0|
|109|OPS-LEGACY-001|Legacy auth endpoint deprecation|Mark legacy endpoints deprecated at GA per TDD S8.4|API Gateway, legacy service|MIG-003|Deprecation headers (Deprecation, Sunset) emitted on legacy responses at GA; 30-day removal communicated to API consumers (Sam persona); removal target 2026-07-09|M|P0|
|110|OPS-SMOKE-001|Production smoke-test suite|Run supertest-based smoke suite against production after each phase transition|CI, production|OPS-HEALTH-001|Smoke suite runs after MIG-001, MIG-002, MIG-003 transitions; covers happy paths for all 6 endpoints; results archived; failure halts phase promotion|S|P0|
|111|OPS-SIGNOFF-001|Go/No-Go sign-off gate|Formal sign-off gate between Beta (MIG-002) and GA (MIG-003) per TDD S24.2|Release management|MIG-002|Checklist includes: NFR-PERF-001 validated, SEC-PENTEST-001 closed, OPS-001/002 runbooks published, OPS-003 rotation live, dashboards green, legal sign-off recorded; signed off by test-lead and eng-manager|S|P0|
|112|OPS-COST-001|Cost + resource tracking baseline|Publish baseline infra cost per TDD S26 ($450/mo target) with monthly tracking|Finance tooling|OPS-004, OPS-005, OPS-006|Baseline $450/mo (3 pods, managed PG, managed Redis); monthly report shared; growth factor ~$50/mo per 10K users captured|S|P1|
|113|OPS-GDPR-EXPORT|GDPR data export capability|Provide mechanism for user to export their personal data per NFR-COMPLIANCE-004|`AuthService`, admin CLI|NFR-COMPLIANCE-002, NFR-COMPLIANCE-004|Export includes email, displayName, createdAt, updatedAt, lastLoginAt, roles, consent_given_at, audit_log entries; format JSON; exportable on demand; tested against EUGDPR Article 15|S|P1|
|114|OPS-RPC-001|Post-GA review window (7 days at 99.9% uptime)|Monitor against exit criterion across first 7 days of GA|Observability|MIG-003, NFR-REL-001|Rolling-window uptime metric exceeds 99.9% for 7 consecutive days post-GA; daily status reports to stakeholders; any breach triggers post-mortem within 48h|S|P0|
|115|OPS-VULN-001|Key-rotation dry-run in production|Execute first quarterly RS256 key rotation in production per COMP-KEYROT-001|`JwtService`, config store|COMP-KEYROT-001, MIG-003|Dry run executed with grace window enabled; downstream services verified tokens signed by both keys during window; post-rotation metrics unchanged; procedure validated against runbook|S|P0|
|116|OPS-AUDIT-QA|Audit log completeness QA|Validate SOC2 control coverage: every FR-AUTH-001..005 path emits exactly one audit row|audit_log, QA|NFR-COMPLIANCE-001|QA harness walks every happy path + error path; asserts exactly one audit_log row emitted per transaction; 12-month retention validated via partition-query; compliance sign-off captured|S|P0|

### Integration Points — M5

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|Automated rollback triggers → flag toggling service|Event → action binding|Yes (automatic from MIG-001)|M5|Phase 1/2/3 rollout protection|
|Data-integrity probe → rollback trigger T4|Scheduled probe|Yes|M5|OPS-ROLLBACK-T4|
|PagerDuty/on-call → auth-team rotation|External platform binding|Yes|M5|OPS-003 escalation|
|API Gateway → Deprecation/Sunset headers on legacy routes|Middleware|Yes|M5|Sam API-consumer persona|
|Release-gate checklist → sign-off workflow|Release management|Yes|M5|OPS-SIGNOFF-001|
|Quarterly key rotation → JwtService verifier|Scheduled job|Yes|M5|All downstream token verifiers|

### Milestone Dependencies — M5

- M4 exit criteria (frontend + observability + compliance + pentest closure)
- Release-management workflow provisioned with OPS-SIGNOFF-001 gate
- On-call rotation platform (PagerDuty or equivalent) provisioned
- Legacy auth endpoint inventory + consumer list compiled for OPS-LEGACY-001

### Risk Assessment and Mitigation — M5

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-003 Data loss during migration from legacy auth|High|Low|User account loss|Parallel run AuthService with legacy in MIG-001 + MIG-002; idempotent upsert migration; full DB backup before each phase; OPS-ROLLBACK-T4 auto-trigger on data corruption; contingency: rollback to legacy + restore from pre-migration backup|platform-team|
|2|Rollback trigger false-positive storm during MIG-002|Medium|Medium|Unnecessary rollbacks disrupt Beta|Thresholds tuned from M4 load-test data; OPS-ROLLBACK-T1..T4 dry-runs in staging before MIG-001; runbook covers false-positive diagnosis; debounce windows sized to trigger semantics (5/2/1 min)|auth-team|
|3|Silent regression in deprecated legacy auth breaks external consumers|Medium|Low|Sam persona integration breakage|Deprecation headers emitted at GA (OPS-LEGACY-001); 30-day sunset period; direct consumer notification; removal tracked in platform-team backlog|platform-team|
|4|99.9% uptime not sustained over first 7 days of GA|High|Low|NFR-REL-001 breached at GA|OPS-004/005/006 capacity plans active; alerts OPS-007-A1/A2/A3 routed to 24/7 rotation; OPS-RPC-001 rolling window monitored daily; post-mortem within 48h of breach|auth-team|
|5|AUTH_TOKEN_REFRESH removal (MIG-005-CLEANUP) regresses refresh flow|Medium|Low|Mass logouts at GA+14d|Pre-removal canary; contract test asserts refresh path works with flag both ON and OFF (i.e., unconditional); rollback plan: re-introduce flag ON if regression|auth-team|

## Resource Requirements and Dependencies

### External Dependencies

|Dependency|Required By Milestone|Status|Fallback|
|---|---|---|---|
|PostgreSQL 15+ (managed)|M1|Provisioning requested|Self-hosted PG 15 in Docker Compose for local dev; delay escalates to platform-team|
|Redis 7+ (managed)|M1|Provisioning requested|Self-hosted Redis 7 in Docker Compose for local dev|
|Node.js 20 LTS runtime|M1|Available|Pin prior 20.x LTS if 20-lts image breaks|
|bcryptjs library|M2|Available (npm)|Native `bcrypt` (compiled) if perf regression|
|jsonwebtoken library|M3|Available (npm)|`jose` library as drop-in alternative|
|SendGrid API|M3|Account pending verification|SES or Postmark as fallback SMTP providers (R-PRD-004)|
|External penetration-test vendor|M4|Scoping in progress|In-house security review with documented coverage gap|
|Prometheus + Grafana + OTel collector|M4|Provisioning requested|Datadog SaaS as alternative with re-instrumentation|
|Kubernetes HPA|M5|Available|Manual scale commands + alerts as interim|
|PagerDuty (on-call)|M5|Account pending|OpsGenie or manual rotation sheet as interim|

### Infrastructure Requirements

- **Compute:** 3 baseline `AuthService` replicas, HPA to 10 at CPU >70% (OPS-004)
- **PostgreSQL:** Managed instance, 100-connection pool (OPS-005), 12-month audit-log partition retention
- **Redis:** Managed cluster, 1 GB baseline scaling to 2 GB, TLS-enabled (OPS-006)
- **API Gateway:** TLS 1.3, CORS allow-list, rate-limit buckets (10/5/60/30 req/min)
- **Observability:** Prometheus scrape, OTel collector, Grafana dashboards, alert routing to PagerDuty
- **Secrets:** 2048-bit RSA key pair for RS256, rotated quarterly; SendGrid API key; DB/Redis credentials (mounted volume)
- **Cost envelope:** ~$450/month production baseline per TDD S26; +$50/mo per 10K users

## Risk Register

|ID|Risk|Affected Milestones|Probability|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|R-001|Token theft via XSS allows session hijacking|M3, M4|Medium|High|accessToken in-memory only (COMP-004); refreshToken via HttpOnly+Secure+SameSite=Strict cookie (COMP-HTTPONLY-001); 15-min access TTL; hashed refresh tokens in Redis; contingency: `TokenManager.revoke` + force password reset|Security Lead|
|R-002|Brute-force attacks on login endpoint|M2|High|Medium|Gateway rate limit 10/min/IP (API-001-RATE); account lockout 5/15min (COMP-LOCKOUT-001); bcrypt cost 12 (COMP-007a); contingency: WAF IP block + CAPTCHA challenge (COMP-CAPTCHA-001)|Security Lead|
|R-003|Data loss during migration from legacy auth|M5|Low|High|Parallel run during MIG-001/MIG-002; idempotent upsert; full backup before each phase; OPS-ROLLBACK-T4 auto-trigger on corruption; contingency: rollback to legacy + restore from backup|platform-team|
|R-PRD-001|Low registration adoption due to poor UX|M4, M5|Medium|High|Usability testing before launch; funnel iteration via SUCC-METRIC-001|Product|
|R-PRD-002|Security breach from implementation flaws|M2, M3, M4|Low|Critical|Dedicated security review across M2/M3; SEC-PENTEST-001 pre-production; contingency: emergency key rotation + coordinated disclosure|sec-reviewer|
|R-PRD-003|Compliance failure from incomplete SOC2 audit logging|M1, M4|Medium|High|Log requirements defined in M1 (COMP-AUDIT-001); SOC2 control validation in M4 (NFR-COMPLIANCE-001); OPS-AUDIT-QA in M5|Compliance Lead|
|R-PRD-004|Email delivery failures blocking password reset|M3|Low|Medium|SendGrid delivery monitoring + 3-attempt retry (COMP-SENDGRID-001); >5% failure-rate alert; fallback support channel documented in OPS-002 runbook|auth-team|
|R-OBS-001|Instrumentation (OTel/Prometheus) regresses NFR-PERF-001 p95 budget|M4|Low|Medium|Before/after benchmarks; trace sampling; contingency: reduce sampling or disable tracing if >10% regression|auth-team|
|R-PENTEST-001|Penetration-test findings block M5 entry|M4, M5|Medium|High|Vendor engaged 2 weeks before M4; weekly interim reports; Critical/High remediated within 5 business days|sec-reviewer|
|R-ROLLBACK-FP|False-positive rollback-trigger storm during MIG-002|M5|Medium|Medium|Thresholds tuned from M4 load test; dry-runs in staging; debounce windows matched to trigger semantics|auth-team|
|R-LEGACY-DEP|Deprecated legacy auth regression breaks API consumers|M5|Low|Medium|Deprecation + Sunset headers; 30-day sunset; direct consumer notification; removal tracked|platform-team|

## Success Criteria and Validation Approach

|Criterion|Metric|Target|Validation Method|Milestone|
|---|---|---|---|---|
|Login response time (p95)|`auth_login_duration_seconds` p95|<200ms|APM histogram quantile over rolling 5m window; NFR-PERF-001 validation in staging|M4|
|Registration success rate|successful registrations / total attempts|>99%|Computed from `auth_registration_total{outcome="success"}` ÷ sum(outcomes)|M4|
|Token refresh p95 latency|APM histogram on `TokenManager.refresh()`|<100ms|APM histogram quantile over rolling 5m window|M4|
|Service availability|Health-check uptime|99.9% over 30-day rolling windows|SLO dashboard + burn-rate alerts; validated over first 30 days post-GA|M5|
|Password hash time|`PasswordHasher.hash()` benchmark|<500ms|CI benchmark per commit; fails build on regression|M4|
|Registration conversion|Funnel: landing → register → confirmed account|>60%|Funnel analytics (SUCC-METRIC-001)|M5 (post-GA)|
|Daily active authenticated users|AuthToken issuance count/day|>1000 within 30 days of GA|`auth_login_total{outcome="success"}` daily rollup (SUCC-METRIC-005)|M5 (post-GA)|
|Average session duration|Derived from token-refresh cadence|>30 minutes|Analytics pipeline (SUCC-METRIC-003)|M5 (post-GA)|
|Failed login rate|Auth event log analysis|<5% of attempts|`auth_login_total{outcome="invalid_creds"}` ÷ total (SUCC-METRIC-004)|M5 (post-GA)|
|Password reset completion|Funnel: reset requested → new password set|>80%|Funnel analytics (SUCC-METRIC-002)|M5 (post-GA)|
|Support 500 concurrent login requests|k6 load test|500 concurrent sustained|NFR-PERF-002 k6 scenario in staging|M4|
|SOC2 audit log coverage|Audit rows per auth event|1 row per FR-AUTH-001..005 transaction|OPS-AUDIT-QA harness + 12-month retention partition test|M5|
|bcrypt cost factor|Persisted hash header|cost=12|NFR-SEC-001 unit test parsing $2b$ hash|M2|
|RS256 key length|JWT header + loaded private key|alg=RS256, 2048-bit|NFR-SEC-002 config-validation test|M3|

## Decision Summary

|Decision|Chosen|Alternatives Considered|Rationale|
|---|---|---|---|
|Session mechanism|JWT (stateless) with refresh-token rotation|Server-side sessions with cookies (rejected)|Stateless verification scales horizontally across services; `TokenManager` handles dual-token lifecycle with Redis-backed revocation (TDD S6.4)|
|Password hashing|bcrypt cost factor 12 via `PasswordHasher`|argon2id (rejected), scrypt (rejected)|bcrypt is battle-tested with well-understood security properties; cost 12 yields hash time ~300ms within <500ms budget; `PasswordHasher` abstraction permits future migration (TDD S6.4)|
|Token signing algorithm|RS256 with 2048-bit RSA keys|HS256 symmetric (rejected)|Asymmetric signing enables downstream verifiers without shared secret; 2048-bit meets NFR-SEC-002 and NIST recommendations|
|Audit log retention|12 months (PRD/SOC2 precedence)|90 days (TDD S7.2 initial value, superseded)|PRD legal/compliance (NFR-COMPLIANCE-001) requires 12 months for SOC2 Type II; resolved via OQ-CONFLICT-001; committed consistently across M1, M4, M5|
|Milestone structure|5 technical-layer milestones (Foundation → Core Auth → Tokens & Session → Integration & Hardening → GA)|5 feature-based milestones per TDD S23|Technical-layer phasing reduces cross-milestone rework; TDD feature-milestone semantics preserved via mapping table; resolved via OQ-CONFLICT-002|
|Token storage|accessToken in-memory; refreshToken HttpOnly+Secure+SameSite=Strict cookie|accessToken in localStorage (rejected)|Defense against XSS token theft (R-001); HttpOnly prevents JS access; SameSite=Strict mitigates CSRF|
|Scope for v1.0|Email/password only|OAuth (deferred v1.1), MFA (deferred v1.1), RBAC enforcement (deferred)|TDD S3.2 Non-Goals NG-001/NG-002/NG-003; PRD S12.2 Out-of-Scope; confirmed never relitigated in milestone ACs|
|Admin JTBD interim UX|CLI over audit_log for Jordan persona|Full admin UI in v1.0 (rejected for scope), no admin interface (rejected for PRD gap)|PRD JTBD requires admin visibility; full UI deferred to v1.1; CLI closes behavioral gap in v1.0 (JTBD-GAP-001)|
|Rollback triggers|Automatic from day 1 of MIG-001|Human-confirmation gate (rejected)|TDD S19.4 phrased as "Triggered if any of the following occur"; automatic semantics preserved; no confirmation layer silently inserted|
|Lockout threshold|5 attempts / 15-minute sliding window (TDD precedence)|PRD silent (no alternative value)|TDD specified concrete threshold; PRD did not conflict; adopted TDD value (OQ-PRD-003 closed)|

## Timeline Estimates

**TDD ↔ Roadmap Milestone Mapping:**

|TDD Milestone (S23.1)|TDD Target Date|Roadmap Milestone|Notes|
|---|---|---|---|
|M1: Core AuthService|2026-04-14|M1 Foundation + M2 Core Authentication|TDD's "core" is split into Foundation (schemas/infra) and Core Authentication (login/register logic)|
|M2: Token Management|2026-04-28|M2 Core Authentication (JWT issuance stub) + M3 Token Management & Session (full)|Token scaffolding begins in M2; full refresh/JWT lifecycle lands in M3|
|M3: Password Reset|2026-05-12|M3 Token Management & Session|Password reset co-packaged with token management (both require Redis + email dependencies)|
|M4: Frontend Integration|2026-05-26|M4 Integration & Hardening|Frontend consolidated with observability, compliance, and perf validation|
|M5: GA Release|2026-06-09|M5 Production Readiness & GA|Phased rollout (MIG-001/002/003), runbooks, capacity, sign-off|

**Roadmap Timeline:**

|Milestone|Duration|Start|End|Key Milestones|
|---|---|---|---|---|
|M1 Foundation|2w (weeks 1–2)|2026-03-31|2026-04-14|Schemas authored (DM-001/DM-002); PostgreSQL + Redis provisioned; audit_log table with 12-month partitioning; feature flags registered (MIG-004/MIG-005); NIST-aligned password-policy validator; GDPR consent field plumbed|
|M2 Core Authentication|2w (weeks 3–4)|2026-04-15|2026-04-28|FR-AUTH-001 + FR-AUTH-002 pass; PasswordHasher bcrypt cost 12 (NFR-SEC-001); account lockout; rate limits live at gateway; audit logging for login/register; TEST-001, TEST-002, TEST-004 pass; AUTH_NEW_LOGIN gated to internal only|
|M3 Token Management & Session|2w (weeks 5–6)|2026-04-29|2026-05-12|FR-AUTH-003/004/005 pass; JwtService RS256 2048-bit (NFR-SEC-002); refresh-token hashed in Redis with 7-day TTL; password reset via SendGrid with 1-hour single-use tokens; quarterly key rotation procedure; TEST-003, TEST-005 pass|
|M4 Integration & Hardening|2w (weeks 7–8)|2026-05-13|2026-05-26|All 3 frontend pages + AuthProvider pass TEST-006; Prometheus metrics + OTel tracing live; alert rules active; NFR-PERF-001 p95 <200ms validated; NFR-PERF-002 500-concurrent load test passes; SOC2 audit log queryable; penetration test completed and Critical/High remediated|
|M5 Production Readiness & GA|2w (weeks 9–10)|2026-05-27|2026-06-09|Phase 1 Internal Alpha (MIG-001); Phase 2 Beta 10% (MIG-002); Phase 3 GA 100% (MIG-003); automated rollback triggers wired; runbooks OPS-001/002 published; on-call rotation live; AUTH_NEW_LOGIN removed; 99.9% uptime over first 7 days post-GA|

**Total estimated duration:** 10 weeks (2026-03-31 → 2026-06-09), aligned verbatim with TDD S23.1 committed schedule end date 2026-06-09. No OQ raised for schedule overshoot because the technically-phased roadmap fits within the TDD-committed window.

