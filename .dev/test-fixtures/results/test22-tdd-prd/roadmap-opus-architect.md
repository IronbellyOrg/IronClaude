---
spec_source: "test-tdd-user-auth.compressed.md"
complexity_score: 0.75
complexity_class: HIGH
primary_persona: architect
adversarial: false
base_variant: "none"
variant_scores: "none"
convergence_score: none
---

# User Authentication Service — Project Roadmap

## Executive Summary

The User Authentication Service (AUTH-001) delivers a stateless, JWT-based identity layer composed of `AuthService` orchestrator fronting `TokenManager` + `JwtService` + `PasswordHasher` + `UserRepo`, backed by PostgreSQL 15 for `UserProfile` persistence and Redis 7 for refresh-token lifecycle. Implementation is phased technically (Foundation → Core Logic → Integration → Hardening → Production Readiness) across 11 calendar weeks ending 2026-06-09, aligned to the TDD §23 milestones. Scope covers FR-AUTH-001 through FR-AUTH-005, 9 NFRs spanning performance, reliability, security, and compliance (GDPR, SOC2 Type II, NIST SP 800-63B), 6 REST endpoints under `/v1/auth/*`, and 9 named components with frontend surfaces `LoginPage`, `RegisterPage`, `ProfilePage`, `AuthProvider`.

**Business Impact:** Unblocks the Q2-Q3 2026 personalization roadmap (~$2.4M ARR), satisfies SOC2 Type II audit deadline in Q3 2026, and resolves the 25% of churn-exit feedback citing missing accounts. Directly enables JTBD for Alex (end user), Jordan (admin audit), and Sam (API consumer programmatic auth).

**Complexity:** HIGH (0.75) — security-critical domain (+0.20); multi-component orchestration across 5 services (+0.15); cross-stack API+frontend+email integration (+0.15); phased rollout with feature flags + rollback (+0.10); compliance obligations SOC2+GDPR+NIST (+0.10); multi-datastore coordination PostgreSQL+Redis (+0.05).

**Critical path:** Infra provisioning (PG15 + Redis7 + RS256 keys) → `PasswordHasher` + `JwtService` primitives → `TokenManager` refresh lifecycle → `AuthService` orchestration → API endpoints → frontend `AuthProvider` context → compliance audit logging → Phase 1 alpha → Phase 2 beta (10%) → Phase 3 GA.

**Key architectural decisions:**

- Stateless JWT with dual-token lifecycle (15-min access + 7-day refresh) over server-side sessions — enables horizontal scaling of `AuthService` across Kubernetes HPA-managed pods.
- bcrypt cost-factor 12 via `PasswordHasher` abstraction — ~300ms hash time fits within 200ms p95 SLO after pool tuning; algorithm-swap contract preserved for NIST roadmap evolution.
- RS256 2048-bit asymmetric signing with quarterly rotation — enables verify-without-secret propagation to downstream services; avoids HS256 shared-secret blast radius.
- Refresh-token hashed-at-rest in Redis 7 (7-day TTL) with `TokenManager`-owned revocation — decouples session life from access token and enables per-device/per-user revocation under compromise.
- Feature-flag-gated rollout (`AUTH_NEW_LOGIN`, `AUTH_TOKEN_REFRESH`) + parallel legacy operation during Phase 1-2 — enables rollback without data migration reversal.
- Audit retention inherited from PRD SOC2 (12 months), overriding TDD §7.2's 90-day default — see OQ-CONF-001 in M4.

**Open risks requiring resolution before M1:**

- OQ-CONF-001 (audit retention 90d vs 12mo) must be committed before PG schema is finalized; roadmap commits to 12 months per PRD SOC2 precedence.
- OQ-PRD-002 (max refresh tokens per user) must be resolved before `TokenManager` Redis key schema is frozen in M1.
- OQ-PRD-003 lockout policy already committed to TDD value (5 attempts / 15 min per §13) — documented in M2.
- SEC-POLICY-001 sign-off required before RS256 key provisioning in M1 (key rotation procedure).

## Milestone Summary

|ID|Title|Type|Priority|Effort|Dependencies|Deliverables|Risk|
|---|---|---|---|---|---|---|---|
|M1|Foundation: Infra, Data Models, Skeletons|infrastructure|P0|L|PG15 provisioned; Redis7 provisioned; SEC-POLICY-001 approved; OQ-PRD-002, OQ-CONF-001 resolved|14|High|
|M2|Core Logic: Password, JWT, Token, Orchestration|implementation|P0|XL|M1|18|High|
|M3|Integration: REST API + Frontend|implementation|P0|L|M2|19|Medium|
|M4|Hardening: Security, Compliance, Observability|quality|P0|L|M3|17|High|
|M5|Production Readiness: Migration, Rollout, Runbooks|release|P0|M|M4|22|Medium|

## Dependency Graph

```
[External Deps]
  PG15 ─┐
  Redis7 ─┤
  Node20 ─┼──▶ M1 Foundation ──▶ M2 Core Logic ──▶ M3 Integration ──▶ M4 Hardening ──▶ M5 Prod Readiness
  SendGrid ─┤          │              │                 │                 │                 │
  SEC-POL ─┘          │              │                 │                 │                 │
                       ▼              ▼                 ▼                 ▼                 ▼
                   DM-001/002     COMP-005/6/7/8    API-001..006      NFR-COMP-001..004   MIG-001..011
                   UserRepo       FR-AUTH-001/2/3   COMP-001..004     OPS-007 metrics     OPS-001..010
                   Feature flags  Lockout mech.     FR-AUTH-004/5     OPS-008/9/10 alerts Rollback drills

Intra-component wiring:
  AuthService ──▶ PasswordHasher ──▶ bcryptjs
  AuthService ──▶ TokenManager  ──▶ JwtService ──▶ jsonwebtoken
                   │                  │
                   └─▶ Redis (refresh store)
  AuthService ──▶ UserRepo ──▶ PostgreSQL (users + audit log)
  AuthService ──▶ EmailAdapter ──▶ SendGrid
  AuthProvider (FE) ──▶ API Gateway ──▶ AuthService
  API Gateway: rate limit + CORS + TLS1.3 ──▶ AuthService
```

## M1: Foundation — Infrastructure, Data Models, Skeletons

**Objective:** Provision datastores, finalize `UserProfile` and `AuthToken` schemas, stand up `UserRepo`, feature-flag infrastructure, RS256 key material, API gateway skeleton, and CI test harness before core logic begins. | **Duration:** Weeks 1-2 (2026-03-26 → 2026-04-09) | **Entry:** SEC-POLICY-001 approved; PG15 + Redis7 + K8s namespace provisioned; Node.js 20 LTS baseline image published; OQ-PRD-002 resolved | **Exit:** DM-001/DM-002 schemas migrated; UserRepo passes unit tests; RS256 keypair in secrets; AUTH_NEW_LOGIN + AUTH_TOKEN_REFRESH flags defined (default OFF); rate-limit + CORS + TLS 1.3 validated in staging

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|INFRA-PG|PostgreSQL 15 provisioning|Provision managed PG15 with connection pool, read replica, and backup policy supporting `UserProfile` storage and audit log table|Infrastructure|—|PG15 reachable from `AuthService` namespace; TLS required; pg-pool max 100; daily backup + PITR enabled; restore drill documented|M|P0|
|2|INFRA-REDIS|Redis 7 provisioning|Provision managed Redis 7 cluster with TLS, persistence, and 1GB initial memory for refresh-token storage|Infrastructure|—|Redis 7.x cluster reachable; TLS enforced; AOF persistence; keyspace notifications enabled for TTL events; memory alarm at 70%|M|P0|
|3|INFRA-K8S|Kubernetes namespace + HPA baseline|Create `auth-service` namespace, baseline Deployment (3 replicas), HPA targeting CPU>70% scaling to 10, PodDisruptionBudget|Infrastructure|—|3-replica Deployment healthy; HPA YAML applied; readiness+liveness probes hitting health endpoint; PDB minAvailable=2|M|P0|
|4|INFRA-KEYS|RS256 keypair + secret mount|Generate 2048-bit RSA keypair, store private key in KMS-backed secret, mount read-only to `JwtService` pods, document quarterly rotation|Infrastructure|SEC-POLICY-001|Keypair generated offline; private key in K8s Secret with KMS envelope; public key published to JWKS endpoint; rotation runbook signed by security|S|P0|
|5|INFRA-TLS|API gateway TLS 1.3 + CORS|Configure API gateway with TLS 1.3 minimum, HSTS, and CORS restricted to known frontend origins allowlist|Infrastructure|—|TLS 1.3 enforced (no fallback to <1.2); HSTS max-age 31536000; CORS allowlist loaded from config; cross-origin preflight tested|S|P0|
|6|INFRA-RATE|API gateway rate limits|Configure per-IP and per-user rate limits per TDD §8.1: /login 10/min/IP, /register 5/min/IP, /me 60/min/user, /refresh 30/min/user|Infrastructure|INFRA-TLS|Each endpoint enforces documented rate; 429 returned on breach; rate decisions logged for auditability|S|P0|
|7|INFRA-DEPS|Runtime dependency pinning|Install and pin `bcryptjs`, `jsonwebtoken`, `pg`, `ioredis`, `@sendgrid/mail` at audited versions with lockfile|Backend|—|Lockfile committed; SBOM generated; vulnerability scan clean (no High/Critical CVEs at pin time)|S|P0|
|8|DM-001|UserProfile PG schema + migration|Create `users` table implementing DM-001 fields with indexes, constraints, and default values|UserRepo|INFRA-PG|id:UUID-PK-NOT-NULL; email:varchar-UNIQUE-NOT-NULL-lowercase-idx; display_name:varchar(2..100)-NOT-NULL; created_at:timestamptz-NOT-NULL-DEFAULT-now(); updated_at:timestamptz-NOT-NULL-auto; last_login_at:timestamptz-NULLABLE; roles:text[]-NOT-NULL-DEFAULT-['user']; migration reversible|M|P0|
|9|DM-002|AuthToken Redis key schema|Define Redis key layout for refresh tokens (`authtok:refresh:{hash}`) implementing DM-002 fields; accessToken stays ephemeral in JWT payload|TokenManager|INFRA-REDIS|accessToken:JWT-RS256-NOT-NULL; refreshToken:string-opaque-stored-as-sha256-hash-in-Redis-NOT-NULL-unique; expiresIn:number-NOT-NULL=900; tokenType:string-NOT-NULL="Bearer"; TTL=7d|S|P0|
|10|DM-AUDIT|Audit log PG table|Create append-only `auth_audit_log` table capturing user_id, event_type, timestamp, ip, outcome; partitioned monthly for 12-month retention (per OQ-CONF-001 resolution)|UserRepo|INFRA-PG|Schema: event_id:UUID-PK; user_id:UUID-FK-nullable; event_type:varchar-NOT-NULL; ts:timestamptz-NOT-NULL; ip:inet; outcome:varchar; monthly partitions; 12-month retention job scheduled|M|P0|
|11|COMP-009|UserRepo data access layer|Implement pg-pool-backed CRUD for `UserProfile` with prepared statements and transaction support|UserRepo|DM-001, INFRA-DEPS|findByEmail(), insert(), update(), updateLastLogin() methods; unit tests ≥80% coverage; query time <20ms on indexed lookups|M|P0|
|12|FLAG-NEW-LOGIN|Feature flag AUTH_NEW_LOGIN|Register `AUTH_NEW_LOGIN` flag in feature-flag system with default OFF, owner auth-team, cleanup target Phase 3 GA|Infrastructure|—|Flag visible in flag UI; default OFF; targeted rollout supported by user-id bucket; audit trail on flag changes; MIG-004 ID reserved|S|P0|
|13|FLAG-REFRESH|Feature flag AUTH_TOKEN_REFRESH|Register `AUTH_TOKEN_REFRESH` flag, default OFF; when OFF, only access tokens are issued; MIG-005 ID reserved; cleanup target Phase 3 + 2 weeks|Infrastructure|—|Flag visible; default OFF; `TokenManager` reads flag at request time; toggling takes effect without redeploy|S|P0|
|14|OQ-CONF-001|Commit audit retention to 12 months|Resolve TDD 90d vs PRD 12mo retention conflict; commit to PRD precedence; cite in DM-AUDIT migration and NFR-COMP-002|UserRepo|—|12-month retention hardcoded in partition-drop job; cross-reference in README; OQ-CONF-001 closed with rationale|S|P0|

### Integration Points — M1

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|FeatureFlagClient|DI registration|M1|auth-team|AuthService, TokenManager (for AUTH_NEW_LOGIN / AUTH_TOKEN_REFRESH gates)|
|UserRepo ← pg-pool|DI registration|M1|auth-team|AuthService M2, audit writer M4|
|RedisClient ← ioredis|DI registration|M1|auth-team|TokenManager M2|
|JWKS endpoint|HTTP route|M1|auth-team|Downstream verifiers, JwtService M2|
|Rate-limit policy map|Config dispatch|M1|platform-team|API gateway M3 endpoints|

### Milestone Dependencies — M1

- External: PostgreSQL 15 managed service, Redis 7 managed service, Kubernetes cluster, SendGrid API account (late-provisioning acceptable until M3), SEC-POLICY-001 sign-off.
- Internal: INFRA-DB-001 parent dependency from TDD frontmatter.

### Open Questions — M1

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-PRD-002|Maximum number of refresh tokens allowed per user across devices?|Blocks DM-002 Redis key schema freeze — if capped, `TokenManager` needs LRU/FIFO eviction; if unlimited, memory budget must expand beyond OPS-006's 1GB projection|Product|2026-04-02|
|2|OQ-002|Maximum allowed `UserProfile.roles` array length?|Affects DM-001 roles column type constraint and input validation; default roadmap assumption is ≤16 until RBAC design completes|auth-team|2026-04-01|
|3|OQ-CONF-001|TDD §7.2 says 90-day audit retention; PRD SOC2 §Legal says 12 months — which wins?|HIGH severity conflict affecting DM-AUDIT partitioning, storage sizing, cost model, and compliance posture. Committed resolution: 12 months (PRD wins on regulatory intent). Status: closed — all downstream rows reference 12mo|Security|2026-03-30 (closed)|

### Risk Assessment and Mitigation — M1

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|RS256 private key compromise before MI1 exit|Critical|Low|Full token forgery capability; forces global rotation + session invalidation|Offline keygen; KMS envelope encryption; RBAC on Secret; rotation runbook; quarterly rotation cadence documented|Security|
|2|PG schema churn after migration|Medium|Medium|Blocks M2 AuthService development; requires downtime or multi-deploy migrations|Finalize OQ-CONF-001 + OQ-PRD-002 before first migration; use reversible migrations; stage in staging first|auth-team|
|3|Feature-flag system unavailable at M1 exit|Medium|Low|Blocks rollout; forces code-based toggle fallback|Use existing platform flag service; validate read-path with canary flag in M1 week 1|platform-team|

## M2: Core Logic — Password, JWT, Token, Orchestration

**Objective:** Implement the four backend service components (`PasswordHasher`, `JwtService`, `TokenManager`, `AuthService`) with their full business logic and unit/integration test coverage; deliver login/register/refresh request handlers behind feature flags. | **Duration:** Weeks 3-4 (2026-04-09 → 2026-04-23) | **Entry:** M1 exit criteria met; DM schemas stable; keys provisioned | **Exit:** `AuthService.login()`, `AuthService.register()`, `TokenManager.refresh()` pass unit tests at ≥80% coverage per NFR-PERF-001 target methods; lockout mechanism blocks after 5 attempts/15min; bcrypt cost 12 verified in assertion test; RS256 signing verified via config test; integration tests against real PG+Redis pass

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|15|COMP-008|PasswordHasher implementation|bcryptjs-backed hash/verify with cost factor 12, algorithm abstraction interface for future NIST migration; raw passwords never logged|PasswordHasher|INFRA-DEPS|hash(pw)→string with $2b$12$ prefix; verify(pw,hash)→bool; cost=12 asserted in unit test; <500ms per op benchmark; no password appears in log capture in test|M|P0|
|16|NFR-SEC-001|Enforce bcrypt cost 12|Configuration validator + unit test asserting `PasswordHasher` cost parameter is exactly 12; fails build if drifted|PasswordHasher|COMP-008|Test parses hash prefix and asserts cost byte = 12; CI blocks merge if assertion fails|S|P0|
|17|NFR-COMP-003|NIST SP 800-63B adaptive hashing|Confirm one-way adaptive hash via `PasswordHasher`; add password storage compliance doc referencing bcrypt cost and no-plaintext-persist invariant|PasswordHasher|NFR-SEC-001|Compliance doc committed; code review checklist includes "no password log/return/persist" inspection; static analysis rule for password field names|S|P0|
|18|COMP-007|JwtService implementation|RS256 sign/verify over JWT claims (sub=user_id, roles, iat, exp); 5-second clock skew tolerance; public-key verify path|JwtService|INFRA-KEYS, INFRA-DEPS|sign() produces RS256 JWT; verify() accepts ±5s skew; invalid signature throws; <5ms per op; unit tests cover expired/tampered/wrong-issuer cases|M|P0|
|19|NFR-SEC-002|RS256 2048-bit key configuration test|Boot-time config test asserts signing key is 2048-bit RSA and algorithm is RS256; refuse to start otherwise|JwtService|COMP-007, INFRA-KEYS|Service refuses to start with HS256 or <2048-bit key; test asserts RSA modulus length ≥2048|S|P0|
|20|COMP-006|TokenManager implementation|Dual-token lifecycle: issue access+refresh pair, store refresh as sha256 hash in Redis with 7d TTL, revoke on refresh, revoke-all on password reset|TokenManager|COMP-007, DM-002|issueTokens(userId,roles)→AuthToken; refresh(refreshToken)→new AuthToken + old revoked; revokeAll(userId) clears all user refresh entries; <10ms Redis ops; unit tests cover reuse-after-revoke|M|P0|
|21|FR-AUTH-003|JWT token issuance and refresh|Wire `TokenManager` + `JwtService` to support login issuance and POST /auth/refresh semantics; expired refresh returns 401; revoked refresh returns 401|TokenManager|COMP-006, COMP-007|Login returns accessToken(TTL=900) + refreshToken(TTL=604800); /auth/refresh with valid token returns new pair and old is unusable; expired returns 401; revoked returns 401|M|P0|
|22|COMP-005|AuthService orchestrator|Backend facade orchestrating login/register/profile/reset via `PasswordHasher`, `TokenManager`, `UserRepo`; central error-code mapping|AuthService|COMP-006, COMP-008, COMP-009|login(), register(), getProfile(), resetRequest(), resetConfirm() methods; error codes mapped to AUTH_* constants; unit tests ≥80% cover all branches|L|P0|
|23|FR-AUTH-001|Login with email + password|`AuthService.login()` lowercases email, loads user via UserRepo, verifies via PasswordHasher, issues tokens via TokenManager, updates last_login_at|AuthService|COMP-005|Valid creds→200+AuthToken; invalid creds→401 generic (no enumeration); unknown email→401 identical shape; last_login_at updated on success; timing side-channel test within 10ms variance|M|P0|
|24|FR-AUTH-002|Registration with validation|`AuthService.register()` validates email format, enforces password policy (≥8 chars, uppercase, number), checks uniqueness, stores bcrypt hash, creates UserProfile|AuthService|COMP-005|Valid→201+UserProfile; duplicate email→409; weak password→400 with field error; roles defaults to ['user']; bcrypt cost=12 hash persisted|M|P0|
|25|SEC-LOCKOUT|Account lockout mechanism|Implement 5-failed-attempts-in-15-min lockout using Redis sliding window keyed by user_id+email; returns 423 Locked; lockout auto-expires after 15min|AuthService|COMP-005, INFRA-REDIS|6th attempt within 15min returns 423; successful login clears counter; TTL-driven auto-unlock verified; per OQ-PRD-003 resolution using TDD §13 values|S|P0|
|26|OQ-PRD-003|Commit lockout policy|Resolve PRD-flagged OQ using TDD §13 values (5 attempts / 15 min); document in SEC-LOCKOUT and compliance doc|AuthService|SEC-LOCKOUT|OQ-PRD-003 marked closed with rationale "TDD wins on implementation detail per conflict resolution rule"; values cited identically in code, test, runbook|S|P1|
|27|VAL-EMAIL|Email normalization + format validation|Lowercase and trim email on every input; RFC 5321 length + basic format validation in `AuthService`; reject control chars|AuthService|COMP-005|Uppercase input normalized; whitespace trimmed; malformed rejected 400; PG unique constraint never fires for case-only duplicates|S|P0|
|28|VAL-PWD|Password strength policy|Client-side + server-side enforcement of ≥8 chars, ≥1 uppercase, ≥1 digit; server authoritative|AuthService|COMP-005|Rule set hardcoded + documented; server rejects weak password with specific field errors; matches FR-AUTH-002 AC3|S|P0|
|29|TEST-001|Login with valid credentials returns AuthToken|Unit test validating FR-AUTH-001 happy path: PasswordHasher.verify() then TokenManager.issueTokens() invocation order|AuthService test|FR-AUTH-001|Mocks for UserRepo + PasswordHasher + TokenManager; asserts verify() called before issueTokens(); returned AuthToken shape validated; runs in CI|S|P0|
|30|TEST-002|Login with invalid credentials returns error|Unit test validating FR-AUTH-001 negative path: returns 401, no AuthToken issued|AuthService test|FR-AUTH-001|PasswordHasher.verify() returns false → 401 error code AUTH_INVALID_CREDENTIALS; TokenManager.issueTokens() NOT called; same timing as valid path within 10ms|S|P0|
|31|TEST-003|Token refresh with valid refresh token|Unit test validating FR-AUTH-003 refresh flow: old token revoked, new pair issued|TokenManager test|FR-AUTH-003|TokenManager.refresh(valid) → new AuthToken; Redis key for old token removed; reuse-after-refresh returns 401; covers revocation idempotency|S|P0|
|32|TEST-004|Registration persists UserProfile to database|Integration test: AuthService + real PostgreSQL via testcontainers validating FR-AUTH-002 end-to-end persistence|AuthService+PG test|FR-AUTH-002, COMP-009|Testcontainer PG started; register() call persists row; bcrypt hash present; unique constraint triggers 409 on duplicate; transaction rolled back on failure|M|P0|

### Integration Points — M2

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|PasswordHasher|DI registration|M2|auth-team|AuthService login/register/reset|
|JwtService|DI registration|M2|auth-team|TokenManager issue/verify; downstream service verifiers|
|TokenManager|DI registration|M2|auth-team|AuthService login/refresh; AuthProvider silent refresh M3|
|AuthService|DI registration|M2|auth-team|API Gateway handlers M3|
|ErrorCodeMap|dispatch table|M2|auth-team|API error renderer M3 (AUTH_INVALID_CREDENTIALS, AUTH_ACCOUNT_LOCKED, AUTH_TOKEN_EXPIRED, ...)|

### Milestone Dependencies — M2

- Depends on M1 (DM-001, DM-002, INFRA-KEYS, INFRA-REDIS, UserRepo, feature flags).
- External: no new external deps; relies on M1-installed bcryptjs + jsonwebtoken.

### Risk Assessment and Mitigation — M2

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|bcrypt cost 12 exceeds 200ms p95 SLO under load (NFR-PERF-001 breach)|High|Medium|Login latency SLO miss; GA gate fails|Benchmark on production-class CPU in M2; tune PG pool + connection settings; profile worker pool; if breach persists, escalate to performance engineer and re-evaluate cost factor with security sign-off|auth-team|
|2|JWT clock skew causes valid tokens rejected|Medium|Low|Intermittent 401s in production|Implement ±5s skew tolerance per TDD §12; enforce NTP on all pods; alert on clock drift|auth-team|
|3|Timing side-channel enables user enumeration (R-001 related)|High|Medium|Allows attacker to distinguish known vs unknown emails|Constant-time compare; always hash on unknown email; timing-parity test in CI within 10ms variance|Security|

## M3: Integration — REST API Endpoints, Frontend, Email

**Objective:** Expose all 6 API endpoints under `/v1/auth/*`, deliver `LoginPage`, `RegisterPage`, `ProfilePage`, and `AuthProvider` context, integrate SendGrid for password reset, and add the PRD-derived logout endpoint. | **Duration:** Weeks 5-6 (2026-04-23 → 2026-05-07) | **Entry:** M2 services wired and unit-tested | **Exit:** All 6 endpoints + logout return correct shapes per TDD §8; E2E test from RegisterPage → LoginPage → ProfilePage passes; AuthProvider performs silent refresh transparently; password reset email delivered within 60s

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|33|API-001|POST /v1/auth/login|HTTP handler mapping `{email,password}` to AuthService.login(); rate-limited 10/min/IP; returns AuthToken|API Gateway|FR-AUTH-001, INFRA-RATE|200→AuthToken; 401 invalid; 429 rate; 423 locked; error shape {error:{code,message,status}}; OpenAPI schema published; response under 200ms p95|M|P0|
|34|API-002|POST /v1/auth/register|HTTP handler mapping `{email,password,displayName}` to AuthService.register(); rate-limited 5/min/IP; returns UserProfile|API Gateway|FR-AUTH-002, INFRA-RATE|201→UserProfile with id,email,displayName,createdAt,updatedAt,lastLoginAt=null,roles=['user']; 400 validation; 409 duplicate; OpenAPI published|M|P0|
|35|API-003|GET /v1/auth/me|HTTP handler validating Bearer token via JwtService, fetching UserProfile via UserRepo; rate-limited 60/min/user|API Gateway|FR-AUTH-004, COMP-007, COMP-009|200→UserProfile(id,email,displayName,createdAt,updatedAt,lastLoginAt,roles); 401 missing/expired/invalid token; identical 401 for all failure subtypes|S|P0|
|36|FR-AUTH-004|User profile retrieval|AuthService.getProfile() returning authenticated user's UserProfile including all DM-001 fields|AuthService|COMP-005, API-003|Response includes id,email,displayName,createdAt,updatedAt,lastLoginAt,roles; tokens older than 15min rejected; lastLoginAt never mutated by /auth/me|S|P0|
|37|API-004|POST /v1/auth/refresh|HTTP handler mapping `{refreshToken}` to TokenManager.refresh(); rate-limited 30/min/user|API Gateway|FR-AUTH-003, INFRA-RATE|200→new AuthToken pair; 401 expired/revoked; old refresh token unusable after call; p95 <100ms per NFR-PERF|S|P0|
|38|API-005|POST /v1/auth/reset-request|HTTP handler triggering reset-token email via SendGrid; returns uniform 200 regardless of email existence (anti-enumeration per PRD)|API Gateway|FR-AUTH-005, INT-EMAIL|Uniform 200 response; token generated with 1h TTL stored in PG; email dispatched within 60s; timing-identical for known/unknown emails within 50ms|S|P0|
|39|API-006|POST /v1/auth/reset-confirm|HTTP handler validating reset token, updating bcrypt hash via PasswordHasher, revoking all sessions via TokenManager.revokeAll()|API Gateway|FR-AUTH-005, COMP-006|200 on success; 400 on invalid/expired/used token; new password replaces hash; TokenManager.revokeAll(userId) called (PRD AC5: new password invalidates existing sessions)|S|P0|
|40|FR-AUTH-005|Password reset flow|Two-step flow wiring /reset-request → email → /reset-confirm with PasswordHasher update and full session revocation|AuthService|API-005, API-006, COMP-006|Reset token TTL=3600s; single-use (marked used row); 1 hour expiry; new hash persisted; TokenManager.revokeAll() invalidates all refresh tokens per PRD|M|P0|
|41|INT-EMAIL|SendGrid email adapter|Backend adapter encapsulating SendGrid API for password reset emails with retry/backoff and delivery status webhook ingestion|AuthService|INFRA-DEPS|sendResetEmail(email,token,link) method; exponential backoff on 5xx; webhook endpoint records delivery status; template id pinned; test-env uses sandbox mode|M|P0|
|42|API-LOGOUT|POST /v1/auth/logout (PRD gap fill)|Endpoint revoking the caller's current refresh token; implements PRD AUTH-E1 "user can log out" user story not present in TDD|API Gateway|COMP-006|200 on success; 401 without valid access token; refresh token removed from Redis; idempotent (second call returns 200 no-op); OpenAPI published|S|P1|
|43|ERR-FORMAT|Unified error response format|Implement error envelope `{error:{code,message,status}}` across all endpoints with stable code catalog (AUTH_INVALID_CREDENTIALS, AUTH_ACCOUNT_LOCKED, AUTH_TOKEN_EXPIRED, AUTH_TOKEN_REVOKED, AUTH_WEAK_PASSWORD, AUTH_EMAIL_TAKEN, AUTH_RESET_TOKEN_INVALID)|API Gateway|COMP-005|Every 4xx/5xx returns envelope; code catalog documented; 500s never leak stack traces; correlation_id present on 5xx|S|P0|
|44|API-VERS|API versioning prefix|All endpoints mounted under `/v1/auth/*`; unversioned /auth/* returns 404 or redirect per policy|API Gateway|API-001..006|All routes live under /v1/auth/; unversioned paths not accessible in prod; OpenAPI bundled under servers.url=/v1/auth|S|P0|
|45|COMP-001|LoginPage component|React route `/login` rendering email+password form, submitting to /v1/auth/login, persisting AuthToken via AuthProvider|Frontend|API-001, COMP-004|Props: onSuccess,redirectUrl?; inline validation on submit; 401 shows generic error without enumerating user; 423 shows lockout message; a11y labels on inputs|M|P0|
|46|COMP-002|RegisterPage component|React route `/register` rendering email+password+displayName form with client-side strength validation before /v1/auth/register|Frontend|API-002, COMP-004|Props: onSuccess,termsUrl; real-time password strength meter; submits only if policy met; 409 shows "email exists, try login" with link|M|P0|
|47|COMP-003|ProfilePage component|React route `/profile` (protected) calling /v1/auth/me and rendering UserProfile data|Frontend|API-003, COMP-004|Renders id,email,displayName,createdAt,updatedAt,lastLoginAt,roles; 401 triggers AuthProvider redirect to LoginPage; loading + error states present|S|P0|
|48|COMP-004|AuthProvider context|React context provider managing AuthToken state, silent refresh via TokenManager client, 401 interceptor, protected-route redirects|Frontend|API-004, COMP-001, COMP-002, COMP-003|Props: children; accessToken in memory (not localStorage); refreshToken in HttpOnly cookie (R-001 mitigation); silent refresh at t-60s before expiry; 401 triggers refresh attempt once then redirect to /login|L|P0|
|49|FE-RESET|Password reset UI flow|Frontend pages for /forgot-password (request) and /reset-password?token=... (confirm) integrating with API-005/API-006|Frontend|API-005, API-006|Forgot page shows uniform confirmation; confirm page validates token presence and expiry; success redirects to /login with toast; AuthProvider clears stale tokens|M|P0|
|50|FE-LOGOUT|Logout button wiring|UI logout control calling API-LOGOUT and clearing AuthProvider state; handles backend failure gracefully (local-only clear)|Frontend|COMP-004, API-LOGOUT|Logout button visible in authed layouts; clears in-memory token + HttpOnly cookie; redirects to /; handles 5xx by still clearing local state|S|P1|
|51|TEST-005|Expired refresh token rejected by TokenManager|Integration test: TokenManager + real Redis validating FR-AUTH-003 TTL expiration enforcement|TokenManager+Redis test|FR-AUTH-003, COMP-006|Testcontainer Redis; issue token then advance time past TTL; refresh() returns 401; Redis key auto-removed by TTL|S|P0|

### Integration Points — M3

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|Express/Fastify routes /v1/auth/*|HTTP dispatch|M3|auth-team|External clients, LoginPage/RegisterPage/ProfilePage|
|Error renderer middleware|middleware chain|M3|auth-team|All API handlers (AUTH_* code catalog)|
|JWT verify middleware|middleware chain|M3|auth-team|GET /v1/auth/me, logout, protected routes|
|SendGrid webhook handler|HTTP route|M3|auth-team|Delivery status ingestion for OPS monitoring|
|AuthProvider React context|DI (FE)|M3|frontend-team|LoginPage, RegisterPage, ProfilePage, protected routes|
|Silent-refresh scheduler|callback wiring|M3|frontend-team|AuthProvider background refresh before expiry|

### Milestone Dependencies — M3

- Depends on M2 core services (`AuthService`, `TokenManager`, `JwtService`, `PasswordHasher`).
- External: SendGrid production API key + domain authentication (SPF/DKIM/DMARC); frontend routing framework availability (PRD Dependencies).

### Open Questions — M3

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-PRD-001|Should password reset emails be sent synchronously or asynchronously?|Affects API-005 latency SLO and reliability posture; synchronous ties response time to SendGrid; async requires background worker + job store. Default: async via in-memory queue, upgrade to durable queue if loss rate >0.1%|Engineering|2026-04-30|
|2|OQ-PRD-004|Should we support "remember me" to extend session duration?|Impacts COMP-004 AuthProvider storage strategy and NFR-SEC-001 R-001 mitigation (longer-lived tokens are higher-value XSS targets). Default: NOT supported in v1.0 per TDD Non-Goal NG-001-like scope; revisit v1.1|Product|2026-04-30|

### Risk Assessment and Mitigation — M3

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|XSS in frontend exfiltrates accessToken (R-001)|High|Medium|Session hijacking; GDPR + SOC2 incident|In-memory-only accessToken storage; HttpOnly+Secure+SameSite=Strict for refreshToken cookie; CSP with nonce; automated XSS scan in CI; 15-min access TTL bounds window|Security|
|2|SendGrid delivery outage blocks password reset (R-PRD-004)|Medium|Medium|Users locked out of recovery; support-ticket surge|Delivery webhook monitoring; alert on 5-min delivery success rate <95%; documented fallback: manual reset via admin tool + support channel|auth-team|
|3|AuthProvider silent-refresh race condition under concurrent tabs|Medium|High|Multiple simultaneous /refresh calls cause unnecessary token rotation and race on old-token revocation|Tab-leader election via BroadcastChannel; mutex lock on refresh; idempotent refresh handler in TokenManager (revocation tolerant of already-revoked)|frontend-team|

## M4: Hardening — Security, Compliance, Observability

**Objective:** Drive NFRs (performance, reliability) to SLO, implement compliance deliverables (SOC2 audit log emission, GDPR consent capture, NIST policy doc, data minimization), wire instrumentation (structured logs, Prometheus metrics, OpenTelemetry spans, alert rules), and pass dedicated security review + pen test per R-PRD-002 mitigation. | **Duration:** Weeks 7-8 (2026-05-07 → 2026-05-21) | **Entry:** M3 endpoints functional in staging | **Exit:** NFR-PERF-001 (<200ms p95) and NFR-PERF-002 (500 concurrent) proven via k6; audit log emits on every auth event with SOC2 fields; GDPR consent checkbox blocks registration without it; all Prometheus counters/histograms observable; all 3 alert rules fire in staging; pen test sign-off received

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|52|NFR-PERF-001|API response time p95 <200ms|Establish k6 scenarios for every endpoint, tune PG connection pool, optimize bcrypt worker pool, cache JWKS|AuthService|M3 endpoints|k6 run of 10-minute steady load reports p95<200ms for /login, /register, /me, /refresh, /reset-*; APM dashboard published|M|P0|
|53|NFR-PERF-002|500 concurrent authentication capacity|k6 load test at 500 concurrent virtual users sustaining login-refresh cycle without error-rate breach|AuthService|NFR-PERF-001|500 VUs for 10 min with error rate <0.1%, p95<200ms, no Redis or PG connection errors; HPA scales within limits|M|P0|
|54|NFR-REL-001|99.9% availability measurement|Health check endpoint + uptime monitor + 30-day rolling SLO dashboard|AuthService|INFRA-K8S|`/healthz` returns 200 when PG+Redis reachable; uptime monitor records 30-day rolling; alerting on <99.9% trend; SLO dashboard published|S|P0|
|55|NFR-COMP-001|GDPR consent at registration|Add `consent_given_at:timestamptz` column to users; require explicit boolean in /register request body; reject registration without consent|AuthService|DM-001|DB column added in reversible migration; API-002 schema requires consent=true; rejection returns 400 with AUTH_CONSENT_REQUIRED; RegisterPage shows checkbox + link to termsUrl|S|P0|
|56|NFR-COMP-002|SOC2 audit logging implementation|Emit audit log entries for login success/failure, registration, logout, token refresh, password reset request/confirm, account lock with user_id, timestamp, IP, outcome; 12-month retention (per OQ-CONF-001)|AuthService|DM-AUDIT|Every auth event produces audit row; fields: user_id,event_type,ts,ip,outcome match SOC2 requirements; 12-month retention enforced by partition-drop job; integration test verifies row presence for each event path|M|P0|
|57|NFR-COMP-003|NIST SP 800-63B compliance doc|Formal compliance document stating `PasswordHasher` algorithm, cost factor, plaintext-exclusion invariants, rotation posture; sign-off from security|Compliance|NFR-SEC-001|Doc committed to repo; references bcrypt cost 12, no plaintext storage, no plaintext log, password-reset token invariants; security sign-off recorded|S|P0|
|58|NFR-COMP-004|GDPR data minimization confirmation|Schema + API audit confirming only email, bcrypt password hash, display name, timestamps, and consent record are collected; no additional PII|Compliance|DM-001, NFR-COMP-001|Data inventory document enumerates every stored field with lawful basis; review sign-off from DPO/privacy; no additional columns admitted without privacy review|S|P0|
|59|OBS-LOG|Structured logging implementation|Emit JSON logs to stdout from AuthService for every auth event with correlation_id, user_id, event_type, outcome, ip, ua, duration_ms|AuthService|COMP-005|Logs pass schema validation in CI; never contain password, refreshToken, or resetToken; correlation_id propagated from request header; log level configurable|S|P0|
|60|OBS-METRICS|Prometheus metrics instrumentation|Instrument `auth_login_total` (counter, labels: outcome), `auth_login_duration_seconds` (histogram), `auth_token_refresh_total` (counter, labels: outcome), `auth_registration_total` (counter, labels: outcome)|AuthService|COMP-005|All four metrics scraped at /metrics; histograms use standard bucket set covering 5ms..2s; dashboards published in Grafana|M|P0|
|61|OPS-007|Prometheus metrics catalog publication|Document every emitted metric with name, type, labels, units, and purpose; link from runbook|Observability|OBS-METRICS|Catalog doc lists auth_login_total, auth_login_duration_seconds, auth_token_refresh_total, auth_registration_total with full metadata|S|P0|
|62|OBS-TRACE|OpenTelemetry distributed tracing|Instrument span creation across AuthService → PasswordHasher → TokenManager → JwtService with context propagation over HTTP|AuthService|COMP-005|Traces visible in tracing backend; each service emits spans with standard attributes; sampling rate configurable (default 10%); 401 error spans record exception|M|P0|
|63|OBS-ALERT-LOGIN|Alert rule login failure rate (OPS-008)|Alert rule firing when login failure rate >20% over 5 minutes; routes to auth-team on-call; P2 severity|Observability|OBS-METRICS|Rule deployed in Prometheus/Alertmanager; fires in staging during induced failure; routes to correct on-call channel|S|P0|
|64|OBS-ALERT-LAT|Alert rule p95 latency breach (OPS-009)|Alert rule firing when p95 latency >500ms sustained 5 minutes; routes to auth-team on-call; P2 severity|Observability|OBS-METRICS|Rule deployed; fires under induced latency test; distinguishes per-endpoint p95|S|P0|
|65|OBS-ALERT-REDIS|Alert rule TokenManager Redis failures (OPS-010)|Alert rule firing when Redis connection failure rate from TokenManager exceeds 0 sustained 1 minute; routes to auth-team; P1 severity|Observability|OBS-METRICS|Rule deployed; fires under induced Redis outage in staging; P1 paging path verified|S|P0|
|66|SEC-REVIEW|Dedicated security review|Formal security review of AuthService attack surface, token handling, password pipeline, and rate-limit effectiveness per R-PRD-002|Security|M3 endpoints|Review checklist signed by security team covering OWASP auth cheat-sheet items; findings tracked to resolution before M5 entry|M|P0|
|67|SEC-PENTEST|Pre-GA penetration test|Engage internal or contracted pen test targeting credential stuffing, token theft, timing side-channels, enumeration, lockout bypass|Security|SEC-REVIEW|Report delivered; P0/P1 findings remediated or accepted by executive sponsor; re-test for P0 fixes passes|L|P0|
|68|TEST-006|E2E register → login → profile|Playwright E2E validating FR-AUTH-001+FR-AUTH-002 full journey through AuthProvider, including silent refresh after 15-min simulated TTL|E2E test|COMP-001, COMP-002, COMP-003, COMP-004|Playwright suite covers register form → email verification skip → login → /profile render → wait 15min (time-advance) → silent refresh → still authenticated; runs in CI|M|P0|

### Integration Points — M4

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|AuditLogWriter|DI registration|M4|auth-team|AuthService event hooks (login/register/refresh/reset/lock)|
|Prometheus /metrics endpoint|HTTP route|M4|auth-team|Prometheus scraper, Grafana dashboards|
|OpenTelemetry SDK|middleware chain|M4|auth-team|Tracing backend, all AuthService methods|
|Alertmanager rules|config dispatch|M4|platform-team|On-call rotation, OPS-008/9/10|
|GDPR consent validator|middleware chain|M4|auth-team|API-002 /register request pipeline|

### Milestone Dependencies — M4

- Depends on M3 endpoints to instrument.
- External: APM/tracing backend (Grafana Tempo or equivalent); Alertmanager configured with auth-team routing; pen test vendor or internal security red-team availability.

### Open Questions — M4

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-CONF-001-AUDIT|Reaffirm 12-month audit retention operationalized via partition-drop job|Closes the TDD/PRD conflict operationally: impacts OPS-005 PG capacity projection (larger audit table) and DM-AUDIT partition count. Status: closed at M1 with 12mo commit; M4 verifies operationalization|Security|2026-05-21 (closed-verify)|

### Risk Assessment and Mitigation — M4

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Pen test surfaces P0 finding requiring architectural rework (R-PRD-002)|Critical|Low|GA slip; potential NFR-SEC revision|Schedule pen test early in M4 (week 7); reserve M4 week 8 buffer for remediation; executive escalation path documented|Security|
|2|SOC2 audit logging gaps found in QA (R-PRD-003)|High|Medium|Compliance failure; Q3 audit blocker|Build compliance-driven test suite validating audit row presence for every event path before M4 exit; cross-check with SOC2 control matrix|Compliance|
|3|NFR-PERF-001 p95 breach under load attributable to bcrypt or PG pool|High|Medium|GA gate fails|Profile bottlenecks during M4 week 7 load tests; apply connection-pool tuning, dedicated bcrypt worker pool, or increase pod count; contingency: cost factor review with security approval|auth-team|

## M5: Production Readiness — Migration, Rollout, Runbooks

**Objective:** Execute phased rollout (internal alpha → 10% beta → 100% GA), publish runbooks and on-call procedures, validate capacity plans, drill rollback, and retire feature flags on schedule. | **Duration:** Weeks 9-11 (2026-05-21 → 2026-06-09) | **Entry:** M4 hardening + pen test sign-off + compliance sign-off; all SLOs met in staging | **Exit:** `AUTH_NEW_LOGIN` 100% for ≥7 days with 99.9% uptime; `AUTH_TOKEN_REFRESH` enabled with stable refresh success rate; feature flags cleaned up per MIG-004 / MIG-005 schedule; post-GA retrospective held

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|69|MIG-001|Phase 1 - Internal Alpha|Deploy AuthService to staging; auth-team + QA verify all endpoints; enable AUTH_NEW_LOGIN for internal users only; week 9|Rollout|M4 exit|FR-AUTH-001..005 manual pass; zero P0/P1 bugs; ≤1 week duration; sign-off from QA+auth-team|M|P0|
|70|MIG-002|Phase 2 - Beta (10%)|Enable AUTH_NEW_LOGIN for 10% of production traffic; monitor latency, error rate, Redis usage; weeks 10-11|Rollout|MIG-001|p95<200ms sustained 14 days; error rate <0.1%; no Redis connection failures; canary dashboard green|M|P0|
|71|MIG-003|Phase 3 - General Availability|Enable for 100% traffic; deprecate legacy endpoints; enable AUTH_TOKEN_REFRESH; week 11 tail|Rollout|MIG-002|99.9% uptime over first 7 days post-100%; all dashboards green; runbook referenced in operational review|S|P0|
|72|MIG-004|Retire AUTH_NEW_LOGIN flag|Remove flag after Phase 3 completes; delete legacy code paths and flag-gated branches|Rollout|MIG-003|Flag removed from code + config; legacy code paths deleted; no references remain in prod; PR merged 1 week after MIG-003 entry|S|P1|
|73|MIG-005|Retire AUTH_TOKEN_REFRESH flag|Remove flag after Phase 3 + 2 weeks of stable refresh operation|Rollout|MIG-003|Flag removed; TokenManager always-on refresh; PR merged 2 weeks after MIG-003 entry|S|P1|
|74|MIG-006|Rollback step 1 - Disable AUTH_NEW_LOGIN|Runbook step: flip flag OFF to route traffic to legacy auth if rollback trigger fires|Rollout|FLAG-NEW-LOGIN, MIG-001|Runbook published; flag-flip command in runbook; tested in staging rollback drill|S|P0|
|75|MIG-007|Rollback step 2 - Verify legacy smoke tests|Runbook step: verify legacy login flow operational via smoke test suite|Rollout|MIG-006|Smoke suite script exists; runbook cites exact invocation; drill verifies smoke passes on legacy path|S|P0|
|76|MIG-008|Rollback step 3 - Root-cause AuthService failure|Runbook step: triage AuthService logs + traces to identify failure cause before re-enabling|Rollout|OBS-LOG, OBS-TRACE|Runbook cites log queries + trace filters; diagnosis playbook linked; target RCA within 4h of incident|S|P0|
|77|MIG-009|Rollback step 4 - Restore UserProfile backup|Runbook step: if data corruption detected, restore from last known-good PG backup; documented PITR window and checksum procedure|Rollout|INFRA-PG|Runbook cites PITR restore command; test restore executed in staging; checksum verification step documented|S|P0|
|78|MIG-010|Rollback step 5 - Incident notification|Runbook step: notify auth-team + platform-team via incident channel; create incident ticket|Rollout|MIG-006|Runbook cites channel + ticket template; auto-notification hook tested in staging|S|P0|
|79|MIG-011|Rollback step 6 - Post-mortem within 48h|Runbook step: schedule post-mortem meeting within 48h; publish RCA document|Rollout|MIG-010|Post-mortem template linked in runbook; calendar invite automation tested; RCA published within 48h of rollback drill|S|P0|
|80|OPS-001|Runbook - AuthService down|Publish runbook covering symptoms (5xx on all /auth/*, LoginPage/RegisterPage error state), diagnosis (K8s pod health, PG connectivity, PasswordHasher/TokenManager init logs), resolution (restart pods, PG failover, Redis-down force-re-login), escalation auth-team→platform-team|Operational|OBS-LOG|Runbook published in wiki; linked from OPS-001 alert payloads; reviewed in on-call handoff; drill executed in staging|M|P0|
|81|OPS-002|Runbook - Token refresh failures|Publish runbook covering symptoms (user logouts, AuthProvider redirect loop, auth_token_refresh_total error spike), diagnosis (Redis connectivity, JwtService key access, AUTH_TOKEN_REFRESH state), resolution (scale Redis, remount secrets, enable flag), escalation auth-team→platform-team|Operational|OBS-METRICS|Runbook published; drill executed during AUTH_TOKEN_REFRESH toggle test|S|P0|
|82|OPS-003|On-call expectations doc|Document P1 acknowledgment SLA (15 min), 24/7 auth-team rotation during first 2 weeks post-GA, tooling access (K8s dashboards, Grafana, Redis CLI, PG admin), escalation path auth-team→test-lead→eng-manager→platform-team|Operational|OPS-001, OPS-002|Doc published; rotation schedule in PagerDuty; all team members have verified access to listed tools|S|P0|
|83|OPS-004|Capacity - AuthService pods|Validate HPA: 3 replicas baseline, scale to 10 at CPU>70%, sustain 500 concurrent users|Operational|INFRA-K8S, NFR-PERF-002|HPA YAML applied; load test triggers scale-up within 2 min; capacity dashboard published|S|P0|
|84|OPS-005|Capacity - PostgreSQL connections|Validate 100 pool size; scale to 200 if wait time >50ms; connection budget across pods documented|Operational|INFRA-PG|Connection-wait dashboard published; budget matches pod × pool formula; alert at 80% utilization|S|P0|
|85|OPS-006|Capacity - Redis memory|Validate 1GB baseline supports ~100K refresh tokens (~50MB projected); scale to 2GB at >70% utilization|Operational|INFRA-REDIS|Memory-utilization dashboard published; projection uses OQ-PRD-002 resolved value; scale-up runbook referenced|S|P0|
|86|OPS-008|Alert - login failure rate|Alert rule deployed and routed per OBS-ALERT-LOGIN; documented in OPS-003 on-call doc|Operational|OBS-ALERT-LOGIN|Alert tested in production dry-run; routes to auth-team channel; doc link present in alert payload|S|P0|
|87|OPS-009|Alert - p95 latency breach|Alert rule deployed and routed per OBS-ALERT-LAT|Operational|OBS-ALERT-LAT|Alert tested in production dry-run; per-endpoint breakdown in alert payload|S|P0|
|88|OPS-010|Alert - TokenManager Redis failures|Alert rule deployed and routed per OBS-ALERT-REDIS|Operational|OBS-ALERT-REDIS|Alert tested; P1 pager fires; runbook OPS-002 linked from alert payload|S|P0|
|89|ROLL-TRIG|Rollback trigger automation|Wire automated guardrails that trigger rollback prompts when any of: p95>1000ms for 5 min, error rate>5% for 2 min, Redis failure rate>10/min, UserProfile data-integrity check fails|Operational|OBS-METRICS, OBS-ALERT-LAT|Automation creates incident ticket + pages on-call on trigger; staging drill validates trigger fires on induced failure; distinguished from operational alerts in OPS-008/9/10|M|P0|
|90|POST-GA|Post-GA retrospective|Facilitated retro within 2 weeks post-100% rollout covering SLO compliance, incident count, feature-flag cleanup, compliance posture, open tech debt|Operational|MIG-003|Retro scheduled; action items tracked; follow-up issues filed; summary published to stakeholders|S|P1|

### Integration Points — M5

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|Feature-flag rollout targeting|dispatch registry|M5|auth-team|AUTH_NEW_LOGIN 0%→10%→100% progression|
|Rollback trigger evaluator|callback wiring|M5|platform-team|Prometheus rules → incident automation|
|Runbook link catalog|reference registry|M5|auth-team|Alert payloads, on-call handoff docs|
|PagerDuty routing|config dispatch|M5|platform-team|P1/P2 page-outs from OPS-008/9/10|

### Milestone Dependencies — M5

- Depends on M4 observability, compliance, and security sign-off.
- External: PagerDuty or equivalent on-call tool; incident management tooling; legacy-auth parallel operation during Phase 1-2.

### Open Questions — M5

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-001|Should AuthService support API key authentication for service-to-service calls?|Scope boundary only — per TDD §3.2 NG-001-class Non-Goal: OAuth/social is out; API-key auth is explicitly deferred to v1.1 per extraction. Status: closed-deferred to v1.1. Status: closed|test-lead|2026-04-15 (closed-deferred)|
|2|OQ-JTBD-SAM|PRD JTBD #4 (Sam the API Consumer) gap — programmatic auth with refresh is covered by FR-AUTH-003; machine-token use case is NOT covered in v1.0|Documents that Sam's JTBD is partially served (refresh flow works for human-initiated tokens) but true service-to-service auth awaits v1.1. Resolution: "PRD requires v1.1 — TDD should be updated to reflect". No v1.0 scope change|Product|2026-05-28|

### Risk Assessment and Mitigation — M5

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Phase 2 10% rollout surfaces latency regression under real load (R-001 / R-PRD-002 relate)|High|Medium|Phase 3 delayed; potential rollback to legacy|Shadow-traffic test during MIG-001; auto-rollback trigger via ROLL-TRIG; dedicated eng on-call during 10% window|auth-team|
|2|Data loss during legacy→new migration (R-003)|High|Low|Account corruption; customer impact; regulatory exposure|Parallel operation through Phase 1-2 with idempotent upsert; pre-phase PG backup; documented restore test (MIG-009); schema changes only forward-compatible|auth-team|
|3|SendGrid delivery failure blocks password reset at scale (R-PRD-004)|Medium|Medium|Support load spike; user recovery blocked|OPS-002 runbook covers detection; fallback admin-reset path documented; delivery-rate alert from M4 OBS-METRICS|auth-team|
|4|Runbook drift between staging drills and production reality|Medium|Medium|Ineffective incident response; prolonged MTTR|Execute at least one full-path drill against staging for each runbook in M5 week 9; update runbook from drill findings before MIG-002|auth-team|

## Resource Requirements and Dependencies

### External Dependencies

|Dependency|Required By MLS|Status|Fallback|
|---|---|---|---|
|PostgreSQL 15+ (managed)|M1|Assumed provisioned per PRD Dependencies|Self-hosted on platform-team; INFRA-DB-001 parent dependency|
|Redis 7+ (managed)|M1|To provision|Self-hosted Redis cluster; in-memory Map for staging-only emergency fallback (NOT prod-safe)|
|Node.js 20 LTS runtime|M1|Baseline available|Containerized base image under platform-team control|
|bcryptjs library|M2|NPM|Fork + pin; argon2id alternative documented per PasswordHasher abstraction|
|jsonwebtoken library|M2|NPM|Fork + pin; jose library documented as alternative|
|SendGrid API|M3|To contract|Amazon SES fallback documented; delay API-005 until alternative provisioned if SendGrid unavailable|
|Frontend routing framework|M3|Assumed per PRD|Block COMP-001/2/3 until available; backend API-only delivery possible as phase split|
|SEC-POLICY-001 sign-off|M1 (INFRA-KEYS)|Pending|Block RS256 key issuance; temporary dev-only key with non-prod guardrails|
|APM/tracing backend|M4|Assumed available|OpenTelemetry OTLP to console exporter; limits observability but unblocks code|
|PagerDuty or equivalent|M5|Assumed available|Manual on-call rotation via Slack channel; degrades MTTA|
|Kubernetes cluster|M1|Available|Self-managed; existing platform-team infra|
|Pen test vendor|M4 (SEC-PENTEST)|To engage|Internal red-team; schedule risk|

### Infrastructure Requirements

- Kubernetes namespace `auth-service` with HPA (3→10 pods, CPU>70%) and PodDisruptionBudget minAvailable=2.
- PostgreSQL 15 primary + read replica, pg-pool max 100 (scale to 200 per OPS-005), daily backup + PITR, monthly partition management for `auth_audit_log` (12-month retention per OQ-CONF-001).
- Redis 7 cluster, 1GB baseline (scale to 2GB per OPS-006), AOF persistence, TLS enforced, keyspace notifications for TTL expiry events.
- KMS-backed secret store for RS256 private key with quarterly rotation procedure.
- API gateway with TLS 1.3, HSTS, CORS allowlist, per-endpoint rate limits per TDD §8.1.
- Prometheus scrape + Grafana dashboards + Alertmanager routing to auth-team on-call.
- OpenTelemetry trace collector routing to tracing backend (sampling 10%).
- SendGrid production sender with SPF/DKIM/DMARC verified on sending domain.

## Risk Register

|ID|Risk|Affected Milestones|Probability|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|R-001|Token theft via XSS allows session hijacking|M2, M3, M4|Medium|High|In-memory accessToken; HttpOnly+Secure+SameSite=Strict cookie for refreshToken; 15-min access TTL; CSP with nonce; automated XSS scan in CI; TokenManager revocation + forced password reset as contingency|Security|
|R-002|Brute-force attacks on login endpoint|M2, M3, M5|High|Medium|API-gateway 10/min/IP + 5-attempt lockout (SEC-LOCKOUT); bcrypt cost 12 makes offline cracking expensive; WAF IP block + CAPTCHA after 3 failures as contingency|Security|
|R-003|Data loss during legacy→new migration|M5|Low|High|Parallel operation in Phase 1-2; idempotent upsert for UserProfile migration; pre-phase PG backup; MIG-009 restore runbook; forward-compatible schema only|auth-team|
|R-PRD-001|Low registration adoption due to poor UX|M3, M5|Medium|High|Pre-launch usability testing on RegisterPage; funnel-data iteration; LoginPage strength meter; OPS-007 registration-rate metric|Product|
|R-PRD-002|Security breach from implementation flaws|M2, M3, M4, M5|Low|Critical|SEC-REVIEW checklist signed off; SEC-PENTEST before GA; OWASP auth cheat-sheet adherence; SOC2 control mapping in NFR-COMP-002|Security|
|R-PRD-003|Compliance failure from incomplete audit logging|M1, M4, M5|Medium|High|DM-AUDIT schema defined early; NFR-COMP-002 audit-row integration tests for every event; 12-month retention operationalized via partition job; SOC2 control matrix cross-check|Compliance|
|R-PRD-004|Email delivery failures blocking password reset|M3, M5|Medium|Medium|SendGrid webhook monitoring; alert on 5-min delivery rate <95%; fallback admin-reset path in OPS-002 runbook; documented SES alternative|auth-team|
|R-PERF-001|bcrypt cost 12 + pool contention breaches NFR-PERF-001 p95<200ms|M2, M4, M5|Medium|High|M4 NFR-PERF-001 load tests with early signal at M2 benchmark; PG pool tuning; dedicated bcrypt worker pool; HPA to 10 pods; cost-factor review with security as last resort|auth-team|
|R-AUDIT-RET|TDD vs PRD audit retention conflict|M1, M4|Low|High|OQ-CONF-001 resolved at M1 committing to PRD 12-month precedence; DM-AUDIT partition-drop job implements 12mo; operationalization verified at M4|Security|
|R-RACE-REFRESH|Silent-refresh race across multiple tabs|M3|High|Medium|BroadcastChannel tab-leader election; mutex on refresh; idempotent TokenManager.refresh() tolerant of already-revoked tokens|frontend-team|

## Success Criteria and Validation Approach

|Criterion|Metric|Target|Validation Method|MLS|
|---|---|---|---|---|
|Login latency SLO|p95 of /v1/auth/login|<200ms|APM histogram auth_login_duration_seconds; k6 load test at 500 VU|M4|
|Registration success rate|registrations_ok / registrations_attempted|>99%|auth_registration_total by outcome over 30-day window|M4, M5|
|Token refresh latency|p95 of /v1/auth/refresh|<100ms|APM histogram scoped to TokenManager.refresh span|M4|
|Service availability|uptime over 30-day rolling window|99.9%|Synthetic /healthz monitor + SLO dashboard|M4, M5|
|Password hash time|bcrypt cost-12 hash duration|<500ms|Unit benchmark in CI + production histogram|M2|
|Registration conversion rate|RegisterPage landing→confirmed account|>60%|Funnel analytics via OPS-007 metrics + product analytics|M5|
|Daily active authenticated users|distinct user_ids with AuthToken issued per day|>1000 within 30 days of GA|TokenManager issuance count aggregated daily|M5|
|Average session duration|mean time between issue and revoke|>30 minutes|auth_token_refresh_total derived metric|M5|
|Failed login rate|failed_logins / total_login_attempts|<5%|auth_login_total by outcome over 30-day window|M4, M5|
|Password reset completion|reset_confirmed / reset_requested|>80%|Funnel via API-005/API-006 audit events|M5|
|Unit test coverage|line coverage for AuthService, TokenManager, JwtService, PasswordHasher|>80%|Jest coverage report in CI|M2|
|Integration tests pass|all 4 API endpoints against real PG+Redis|100% pass|testcontainers CI workflow|M3|
|Security review complete|SEC-REVIEW checklist|sign-off|SEC-REVIEW artifact committed; SEC-PENTEST report with no unaddressed P0|M4|
|Load test at 500 concurrent|k6 scenario; p95 + error rate|p95<200ms, errors<0.1%|M4 k6 run archived|M4|

## Decision Summary

|Decision|Chosen|Alternatives Considered|Rationale|
|---|---|---|---|
|Session mechanism|JWT (stateless) + refresh token|Server-side sessions with HttpOnly cookies|TDD §6.4 cites horizontal-scaling benefit across `AuthService` pods via Kubernetes HPA; server-side sessions require sticky routing or shared session store which adds an additional failure domain beyond PG+Redis|
|Password hashing|bcrypt cost 12 via PasswordHasher|argon2id, scrypt|TDD §6.4 cites battle-tested security properties; cost 12 benchmarked at ~300ms leaving headroom under NFR-PERF-001 200ms p95 once pooling is tuned; abstraction layer permits future algorithm swap|
|Token signing algorithm|RS256 with 2048-bit RSA keys|HS256 shared secret|Asymmetric verify enables downstream services to validate without access to signing key; blast radius of leaked signing key contained via quarterly rotation; NFR-SEC-002 verbatim|
|Refresh token storage|Hashed in Redis 7|Plaintext in DB, JWE encrypted|Redis TTL automates expiry per NFR-REL design; hashing-at-rest prevents DB-dump replay; decoupled from PG reduces AuthService latency on refresh|
|Audit retention period|12 months|TDD §7.2 90 days; PRD §Legal 12 months|PRD §Legal SOC2 Type II requires 12 months; PRD precedence on business/regulatory intent per Document Conflict Resolution rule; OQ-CONF-001 closed with 12mo commit; operationalized via DM-AUDIT partition-drop job|
|Rollout mechanism|Feature flags AUTH_NEW_LOGIN + AUTH_TOKEN_REFRESH with 3-phase cutover|Big-bang deploy, blue/green|TDD §19.1 phased mitigates R-003 data-loss risk; parallel legacy operation enables flag-flip rollback without data reversal (MIG-006); matches R-003 mitigation evidence|
|Milestone paradigm|Technical layers (Foundation → Core Logic → Integration → Hardening → Production Readiness)|TDD §23 product milestones M1..M5|Technical-layer phasing preserves dependency-driven execution; TDD product milestones remain the calendar anchor via Timeline Estimates table|
|Account lockout policy|5 attempts / 15 min (TDD §13)|PRD OQ-PRD-003 "open"|TDD wins on implementation detail per conflict resolution rule; committed via SEC-LOCKOUT; OQ-PRD-003 closed|
|Password reset email delivery|Asynchronous|Synchronous inline with API-005|OQ-PRD-001 default resolution: async preserves API-005 latency budget; upgrade to durable queue if loss rate >0.1% observed; revisit per OQ-PRD-001|
|"Remember me" support|Not supported in v1.0|Longer-lived token or sliding session|OQ-PRD-004 default resolution: excluded per R-001 XSS blast-radius containment; revisit v1.1|
|Social/OAuth + MFA + RBAC enforcement|Out of scope v1.0|In-scope|PRD §Scope Definition + TDD §3.2 NG-001/002/003 explicit Non-Goals; hard scope decision (not OQ)|

## Timeline Estimates

|MLS|Duration|Start|End|Key Milestones|
|---|---|---|---|---|
|M1|2 weeks (weeks 1-2)|2026-03-26|2026-04-09|Maps to TDD pre-M1 prep; DM-001/DM-002 schemas; RS256 keys; feature flags; INFRA-* complete|
|M2|2 weeks (weeks 3-4)|2026-04-09|2026-04-23|Maps to TDD M1 (2026-04-14) and partial M2; AuthService + PasswordHasher + TokenManager + JwtService; FR-AUTH-001/002/003 backend; TEST-001..005|
|M3|2 weeks (weeks 5-6)|2026-04-23|2026-05-07|Maps to TDD M2 (2026-04-28) and M3 (2026-05-12); 6 API endpoints + logout; LoginPage/RegisterPage/ProfilePage/AuthProvider; password reset; TEST-005; SendGrid integration|
|M4|2 weeks (weeks 7-8)|2026-05-07|2026-05-21|Maps to TDD M4 (2026-05-26) minus 1 week; NFR-PERF load tests; NFR-COMP-001..004 compliance; OBS-LOG/METRICS/TRACE/ALERT; SEC-REVIEW + SEC-PENTEST; TEST-006 E2E|
|M5|3 weeks (weeks 9-11)|2026-05-21|2026-06-09|Maps to TDD M5 GA (2026-06-09) exactly; MIG-001 Phase 1 alpha → MIG-002 Phase 2 10% beta → MIG-003 Phase 3 100% GA; runbooks; capacity validation; POST-GA retro|

**TDD Milestone Mapping (per Timeline Anchoring Rule):**

|Roadmap MLS|TDD §23 Milestone|TDD Target Date|Alignment|
|---|---|---|---|
|M1|(TDD pre-M1 prep)|—|Foundation precedes TDD M1 scope|
|M2|TDD M1 Core AuthService|2026-04-14|M2 week-3 includes TDD M1 scope completion; M2 exit at 2026-04-23 exceeds TDD M1 target — FR-AUTH-003 refresh/JWT in M2 overlaps TDD M2|
|M3|TDD M2 Token Management + M3 Password Reset|2026-04-28 / 2026-05-12|M3 window 2026-04-23→2026-05-07 spans TDD M2; TDD M3 password reset completes by M3 end 2026-05-07|
|M4|TDD M4 Frontend Integration|2026-05-26|Frontend components were delivered in M3; M4 focuses on hardening around them; M4 exit 2026-05-21 is earlier than TDD M4 date, preserving buffer|
|M5|TDD M5 GA Release|2026-06-09|M5 exit 2026-06-09 matches TDD GA date exactly|

**Total estimated duration:** 11 weeks (2026-03-26 → 2026-06-09), anchored to TDD §23 committed GA date 2026-06-09. No overshoot flagged. If Phase 2 beta reveals SLO breach requiring remediation beyond M5 week-11 buffer, the GA date slip must be escalated as a new blocking OQ in M5 rather than silently accepted.


