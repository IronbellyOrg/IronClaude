---
spec_source: "test-tdd-user-auth.compressed.md"
complexity_score: 0.72
complexity_class: HIGH
primary_persona: architect
adversarial: false
base_variant: "none"
variant_scores: "none"
convergence_score: none
debate_rounds: none
generated: "2026-04-19"
generator: "single"
total_milestones: 7
total_task_rows: 93
risk_count: 7
open_questions: 9
domain_distribution:
  frontend: 12
  backend: 38
  security: 18
  performance: 10
  documentation: 22
consulting_personas: [architect, security, backend, frontend, qa, devops]
milestone_count: 7
milestone_index:
  - id: M1
    title: "Foundation and Infrastructure"
    type: FEATURE
    priority: P0
    dependencies: []
    deliverable_count: 13
    risk_level: Medium
  - id: M2
    title: "Core Authentication Backend"
    type: FEATURE
    priority: P0
    dependencies: [M1]
    deliverable_count: 17
    risk_level: High
  - id: M3
    title: "Extended Auth Flows (Refresh, Profile, Reset, Logout)"
    type: FEATURE
    priority: P0
    dependencies: [M2]
    deliverable_count: 14
    risk_level: Medium
  - id: M4
    title: "Frontend Integration"
    type: FEATURE
    priority: P1
    dependencies: [M2, M3]
    deliverable_count: 11
    risk_level: Medium
  - id: M5
    title: "Testing and Hardening"
    type: TEST
    priority: P0
    dependencies: [M2, M3, M4]
    deliverable_count: 12
    risk_level: Medium
  - id: M6
    title: "Observability and Compliance"
    type: SECURITY
    priority: P0
    dependencies: [M2, M3]
    deliverable_count: 13
    risk_level: High
  - id: M7
    title: "Migration and Phased Rollout"
    type: MIGRATION
    priority: P0
    dependencies: [M5, M6]
    deliverable_count: 13
    risk_level: High
total_deliverables: 93
total_risks: 7
estimated_milestones: 7
validation_score: 0.88
validation_status: PASS
---

# User Authentication Service — Project Roadmap

## Executive Summary

The User Authentication Service introduces a stateless JWT-based identity layer to unblock the Q2–Q3 2026 personalization roadmap and satisfy the Q3 2026 SOC2 Type II audit. The architecture separates concerns across four backend components (`AuthService`, `TokenManager`, `JwtService`, `PasswordHasher`) fronted by an API Gateway that enforces rate limits and TLS 1.3, with PostgreSQL 15 for `UserProfile` persistence and Redis 7 for refresh-token storage. The frontend adds three routes (`LoginPage`, `RegisterPage`, `ProfilePage`) wrapped by a single `AuthProvider` that handles silent token refresh. Rollout is gated by two feature flags (`AUTH_NEW_LOGIN`, `AUTH_TOKEN_REFRESH`) and a three-phase migration (internal alpha → 10% beta → 100% GA).

**Business Impact:** Unlocks ~$2.4M in personalization-dependent annual revenue, closes a SOC2 audit blocker scheduled for Q3 2026, and stems a 30% QoQ growth in access-related support tickets. Addresses primary personas Alex (end user), Jordan (admin), and Sam (API consumer).

**Complexity:** HIGH (0.72) — driven by security-critical surface (bcrypt cost 12, RS256 JWT, account lockout, GDPR consent, SOC2 audit logging), multi-team coordination (auth-team, platform-team, frontend-team), phased rollout with two flags and a documented rollback path, and compliance windows that force observability and retention decisions early.

**Critical path:** M1 Foundation (DB + Redis + service skeleton + key management) → M2 Core Auth Backend (AuthService + PasswordHasher + JwtService + TokenManager + login/register APIs) → M3 Extended Flows (refresh, profile, reset, logout) → M5 Testing/Hardening and M6 Observability/Compliance in parallel → M7 Phased Rollout with feature-flag gating. M4 Frontend runs parallel to M3 once API contracts are frozen.

**Key architectural decisions:**

- Stateless JWT access tokens (RS256, 2048-bit, 15-min TTL) with opaque refresh tokens in Redis (7-day TTL) — rationale: meets NFR-PERF-001 p95 < 200ms without hot-path DB reads while retaining revocation via `TokenManager`.
- bcrypt cost factor 12 for `PasswordHasher` — rationale: NIST SP 800-63B adaptive hashing requirement (NFR-COMP-003, NFR-SEC-001); benchmarked ~300ms per hash, within NFR-PERF-001 envelope because hashing is off the token-refresh hot path.
- API Gateway enforces rate limiting and CORS before requests reach `AuthService` — rationale: mitigates R-002 (brute force) without coupling business logic to gateway concerns, and keeps per-endpoint rate limits (10/min login, 5/min register, 60/min profile, 30/min refresh) centrally governed.
- Parallel-run legacy + new auth across Phase 1–2 with feature-flag cutover — rationale: mitigates R-003 (data loss during migration) and provides instant rollback via `AUTH_NEW_LOGIN=OFF`.

**Open risks requiring resolution before M1:**

- OQ-007 (audit log retention conflict: TDD 90 days vs PRD SOC2 12 months) must be resolved before M1 exits because the retention target dictates PostgreSQL sizing and archival tier choice.
- OQ-005 (account lockout policy) must be resolved before M2 login endpoint is finalized; Security sign-off required to freeze the 5-failures-in-15-minutes rule.
- SEC-POLICY-001 authority must be confirmed available before M1 kick-off — password and token policy flows down from it.

## Milestone Summary

|ID|Title|Type|Priority|Effort|Dependencies|Deliverables|Risk|
|---|---|---|---|---|---|---|---|
|M1|Foundation and Infrastructure|FEATURE|P0|M|—|13|Medium|
|M2|Core Authentication Backend|FEATURE|P0|L|M1|17|High|
|M3|Extended Auth Flows|FEATURE|P0|M|M2|14|Medium|
|M4|Frontend Integration|FEATURE|P1|M|M2, M3|11|Medium|
|M5|Testing and Hardening|TEST|P0|M|M2, M3, M4|12|Medium|
|M6|Observability and Compliance|SECURITY|P0|M|M2, M3|13|High|
|M7|Migration and Phased Rollout|MIGRATION|P0|L|M5, M6|13|High|

## Dependency Graph

```
M1 (Foundation) → M2 (Core Backend) → M3 (Extended Flows) ─┐
                                   ↘                        ├→ M5 (Testing) ─┐
                                     M4 (Frontend) ─────────┘                 ├→ M7 (Rollout)
                                   ↘                                          │
                                     M6 (Observability/Compliance) ───────────┘

Entity flow: DM-001/DM-002 → COMP-005..008 → API-001..006 → COMP-001..004
             TEST-001..006 validate COMP-*; MIG-001..007 gate production cutover
External: PostgreSQL 15+, Redis 7+, Node.js 20 LTS, SendGrid, API Gateway, SEC-POLICY-001, INFRA-DB-001
```

## M1: Foundation and Infrastructure

**Objective:** Provision runtime, storage, and cross-cutting infrastructure so the auth service can be implemented on top. | **Duration:** Weeks 1–2 | **Entry:** OQ-007 retention decision resolved, SEC-POLICY-001 available, cloud accounts/secrets ready. | **Exit:** PostgreSQL + Redis reachable from service skeleton; JWT key pair generated and mounted; CI pipeline green on empty service; data model migrations land `UserProfile` schema in staging.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|INFRA-DB-001|PostgreSQL 15 provisioning|Provision PostgreSQL 15+ cluster in staging and prod with read replica for failover.|PostgreSQL|—|cluster reachable via pg-pool; read replica lag < 5s; automated backups enabled|M|P0|
|2|DM-001|`UserProfile` schema and migration|Create `users` table matching UserProfile interface; indexes and constraints.|PostgreSQL|INFRA-DB-001|id:UUID-PK; email:unique-idx-lowercase-NOT-NULL; display_name:varchar-2-100-NOT-NULL; password_hash:varchar-NOT-NULL; created_at:timestamptz-default-now; updated_at:timestamptz-auto-updated; last_login_at:timestamptz-nullable; roles:text[]-NOT-NULL-default-{user}|M|P0|
|3|DM-002|`AuthToken` contract and Redis schema|Define AuthToken TypeScript interface; design Redis keyspace for refresh tokens.|Redis, Shared types|INFRA-REDIS-001|access_token:JWT-string-NOT-NULL; refresh_token:opaque-string-NOT-NULL-unique; expires_in:number-NOT-NULL-900; token_type:string-NOT-NULL-Bearer; redis-key:rt:{token_hash}; ttl:604800s; value:{user_id,issued_at}|S|P0|
|4|INFRA-REDIS-001|Redis 7 provisioning|Deploy Redis 7+ cluster with persistence (AOF) and 1GB baseline memory.|Redis|—|RESP reachable from service; 1GB memory; AOF persistence on; connection pool sized for 500 concurrent|M|P0|
|5|INFRA-NODE-001|Node.js 20 LTS service skeleton|Bootstrap `auth-service` Node.js 20 project with TypeScript, ESLint, structured logger.|AuthService|—|pnpm/npm install succeeds; `npm run build` green; health endpoint returns 200|S|P0|
|6|INFRA-GATEWAY-001|API Gateway routes and CORS|Configure gateway to front `/v1/auth/*`, enforce TLS 1.3, CORS allowlist.|API Gateway|INFRA-NODE-001|routes registered; CORS origins match known frontend list; TLS 1.3 only; pre-flight OPTIONS handled|M|P0|
|7|INFRA-RATELIMIT-001|API Gateway rate-limit config|Enforce per-endpoint rate limits at gateway before AuthService.|API Gateway|INFRA-GATEWAY-001|login:10/min/IP; register:5/min/IP; me:60/min/user; refresh:30/min/user; reset-request:5/min/IP; 429 error envelope consistent|M|P0|
|8|INFRA-SECRETS-001|JWT RSA keypair and secret mount|Generate 2048-bit RSA keypair; mount via secrets volume; document quarterly rotation.|JwtService, Secrets|INFRA-NODE-001|private+public keys 2048-bit RSA; mounted at /run/secrets/jwt; rotation runbook drafted|S|P0|
|9|INFRA-CI-001|CI pipeline for auth-service|Configure lint/build/test/coverage/security-scan pipeline.|CI/CD|INFRA-NODE-001|lint, build, unit test, coverage, npm audit, container scan all blocking; PR checks required|M|P0|
|10|INFRA-EMAIL-001|SendGrid integration wiring|Provision SendGrid account, API key, sender domain; stub transactional template for reset email.|Email|—|API key in secret store; sender domain SPF/DKIM verified; test email delivers in staging|S|P0|
|11|INFRA-PGPOOL-001|PostgreSQL connection pool config|Configure pg-pool with size 100, idle 30s, query timeout 10s.|AuthService, PostgreSQL|INFRA-DB-001|pool size 100; max wait 5s; leak detection logs; metrics emitted for active/idle|S|P1|
|12|NFR-COMP-004|GDPR data minimization baseline|Enforce schema-level that only email+password_hash+display_name+roles are collected; no extra PII columns.|PostgreSQL schema|DM-001|schema review sign-off; lint rule blocking PII columns without review; documented in data map|S|P0|
|13|INFRA-ENV-001|Environment configuration model|Define config keys for TTLs, bcrypt cost, rate limits, flag defaults; schema-validated at boot.|AuthService|INFRA-NODE-001|boot fails fast on invalid config; cost_factor, access_ttl_sec, refresh_ttl_sec, reset_ttl_sec, AUTH_NEW_LOGIN, AUTH_TOKEN_REFRESH present|S|P1|

### Integration Points — M1

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|pg-pool connection|Dependency injection|at service bootstrap|M1|COMP-005 AuthService, COMP-006 TokenManager|
|Redis client|Dependency injection|at service bootstrap|M1|COMP-006 TokenManager|
|JWT keypair loader|Secrets mount + DI|at service bootstrap|M1|COMP-007 JwtService|
|SendGrid transport|Strategy provider (SMTP vs API)|at service bootstrap|M1|COMP-005 AuthService (reset flow)|
|Config schema validator|Middleware (boot-time)|at service bootstrap|M1|All COMP-00x backend|

### Milestone Dependencies — M1

- External: SEC-POLICY-001 (password/token policy), INFRA-DB-001 (DB provisioning authority).
- Prior: none.

### Open Questions — M1

|#|ID|Question|Impact|Owner|Target|
|---|---|---|---|---|---|
|1|OQ-007|Audit log retention: TDD 90 days vs PRD SOC2 12 months. PRD wins on business intent; TDD update required.|High — drives PostgreSQL sizing, backup tier, archival strategy, and COMP-005 audit-log schema|Compliance + auth-team|End of M1 week 1|

### Risk Assessment and Mitigation — M1

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-003 data loss during infrastructure bring-up|High|Low|Corrupt or empty `UserProfile` schema blocks M2|Migration scripts idempotent; full backup before each apply; dry-run in staging|platform-team|
|2|INFRA-BLOCKER dependencies not ready (SEC-POLICY-001 absent, SendGrid blocked)|Medium|Medium|Schedule slip for M2 by full milestone|Pre-kickoff readiness checklist; named accountable owner per dependency|architect|

## M2: Core Authentication Backend

**Objective:** Implement the four backend components and the two public endpoints that cover login and registration end-to-end, enforcing security/compliance NFRs. | **Duration:** Weeks 3–5 | **Entry:** M1 exit criteria met; OQ-005 lockout policy signed off by Security. | **Exit:** API-001 and API-002 pass integration tests against PostgreSQL+Redis; bcrypt cost and RS256 configuration validated; account lockout enforced; login p95 < 200ms in staging.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|COMP-008|`PasswordHasher` component|Bcrypt-based hasher with configurable cost; `hash(plain)` and `verify(plain,hash)`.|PasswordHasher|INFRA-NODE-001, INFRA-ENV-001|hash cost 12; hash returns in < 500ms; verify constant-time against stored hash; module unit-tested|M|P0|
|2|NFR-SEC-001|Bcrypt cost factor 12 enforcement|Config-validated default cost=12 with unit test asserting parameter at runtime.|PasswordHasher|COMP-008|unit test fails if cost != 12; cost surfaces in metrics; config override forbidden in prod|S|P0|
|3|NFR-COMP-003|NIST SP 800-63B password storage|Plaintext password never logged, never persisted; redaction middleware in logger.|PasswordHasher, Logger|COMP-008|log redaction rule for password/password_hash/token; static analysis rule blocks console.log of sensitive fields|S|P0|
|4|COMP-007|`JwtService` component|RS256 signer/verifier with 5s clock skew; sign/verify p95 < 5ms.|JwtService|INFRA-SECRETS-001|RS256 only; 2048-bit keys; iss/sub/exp/iat claims present; verify rejects tampered signature|M|P0|
|5|NFR-SEC-002|RS256 2048-bit key configuration test|Config validator asserts algorithm=RS256 and key length=2048 at boot.|JwtService|COMP-007, INFRA-SECRETS-001|boot fails on HS256 or keys < 2048; test suite asserts config|S|P0|
|6|COMP-006|`TokenManager` component|Issue/revoke/rotate refresh tokens; hashed storage in Redis; delegates signing to JwtService.|TokenManager|COMP-007, INFRA-REDIS-001, DM-002|issueTokens returns AuthToken; refresh TTL 7d; revoke removes key; hashed refresh-token storage; user→token index for device listing|L|P0|
|7|COMP-005|`AuthService` orchestrator|Backend facade exposing API-001..006; delegates to UserRepo, PasswordHasher, TokenManager.|AuthService|COMP-008, COMP-006, INFRA-PGPOOL-001|orchestrates login/register/refresh/profile/reset; no business logic in controllers; transactional boundaries documented|L|P0|
|8|API-001|POST `/v1/auth/login` endpoint|Authenticate via AuthService; return AuthToken.|AuthService|COMP-005, COMP-008, COMP-006|200 with AuthToken on valid creds; 401 on invalid (no enumeration); 423 on locked account; 429 on rate limit; URL versioned|M|P0|
|9|API-002|POST `/v1/auth/register` endpoint|Create UserProfile; bcrypt hash; return profile.|AuthService|COMP-005, COMP-008, DM-001|201 with UserProfile; 400 on weak password (< 8 chars, no uppercase, no number); 409 on duplicate email; 201 response omits password_hash|M|P0|
|10|FR-AUTH-001|Login with email and password|End-to-end login flow behind API-001; integrates lockout and rate limits.|AuthService|API-001, FR-LOCKOUT|valid creds:200+AuthToken; invalid:401; unknown-email:401 (same as wrong pw); locked:423; 5 failures in 15min triggers lockout|M|P0|
|11|FR-AUTH-002|User registration with validation|End-to-end registration behind API-002 with password strength and uniqueness.|AuthService|API-002|valid:201+UserProfile; duplicate email:409; weak pw:400; bcrypt cost 12 verified; displayName 2-100 chars enforced|M|P0|
|12|FR-LOCKOUT|Account lockout after 5 failures (per OQ-005)|Track failures per-account in 15-min sliding window; lock account and refuse login.|AuthService, PostgreSQL|OQ-005, COMP-005|5 failures in 15min locks account; lockout duration per Security sign-off; is_locked surfaced in profile; unlock path defined|M|P0|
|13|FR-PW-POLICY|Password strength policy|Reject passwords < 8 chars, missing uppercase, or missing digit per NIST-aligned derivative policy.|AuthService|COMP-005, NFR-COMP-003|weak password rejected with structured 400; policy config documented; compatible with SEC-POLICY-001|S|P0|
|14|API-ERR-001|Standardized error envelope|Return `{ error: { code: "AUTH_*", message, status } }` for all auth endpoints.|AuthService|COMP-005|envelope schema contract-tested; no stack traces in prod responses; codes namespaced AUTH_*|S|P0|
|15|API-VERSION-001|URL-prefix versioning `/v1/auth/*`|Register all endpoints under `/v1` with additive-change governance policy.|AuthService|INFRA-GATEWAY-001|all endpoints under /v1/auth; breaking change requires new major; documented in ADR|S|P1|
|16|NFR-PERF-001|Login p95 < 200ms|Instrument AuthService.login and verify against APM baseline.|AuthService, APM|API-001, COMP-008|p95 < 200ms in staging at 100 RPS; bcrypt budget off hot path; alert on regression|M|P0|
|17|NFR-REL-001|Service availability SLO wiring|Define 99.9% SLO, health endpoint, readiness probe.|AuthService, APM|COMP-005|/_health returns 200 with DB+Redis probe; SLO recorded in SLO doc; burn-rate alert configured|S|P0|

### Integration Points — M2

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|AuthService router|Dispatch table (HTTP route → handler)|M2|M2|API Gateway|
|PasswordHasher→AuthService|Constructor DI|M2|M2|COMP-005 AuthService|
|TokenManager→AuthService|Constructor DI|M2|M2|COMP-005 AuthService|
|JwtService→TokenManager|Constructor DI|M2|M2|COMP-006 TokenManager|
|Error envelope middleware|Middleware chain (post-handler)|M2|M2|All API-001..006|
|Lockout interceptor|Middleware chain (pre-handler on login)|M2|M2|API-001|
|Config validator|Boot-time hook|M1→M2|M2|COMP-005..008|

### Milestone Dependencies — M2

- Prior: M1 (all infrastructure + DM-001/DM-002).
- External: OQ-005 Security sign-off on lockout policy.

### Open Questions — M2

|#|ID|Question|Impact|Owner|Target|
|---|---|---|---|---|---|
|1|OQ-005|Account-lockout policy after N consecutive failures — aligned with TDD's 5/15-min rule but needs Security sign-off.|High — blocks FR-LOCKOUT and API-001 finalization|Security|Before M2 week 2|
|2|OQ-002|Maximum allowed `UserProfile.roles` array length.|Medium — shapes DM-001 index size and JWT claim size|auth-team|Immediately (past 2026-04-01 target; escalate)|

### Risk Assessment and Mitigation — M2

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-002 brute-force attacks on login|Medium|High|Credential stuffing, enumeration, support load|Gateway rate limit 10/min/IP; account lockout 5/15min; bcrypt cost 12; CAPTCHA post-3 failures (M4)|Security|
|2|R-007 Redis unavailability impairs TokenManager|Low|Medium|Refresh impossible; users forced to re-login|Fail-closed on refresh; DI boundary supports circuit breaker; alert wired in M6|auth-team|
|3|Misconfigured RS256 keys (wrong alg or too short)|High|Low|Tokens forgeable or service refuses to boot|Boot-time validator (NFR-SEC-002); two-key (active+standby) pattern for rotation|Security|

## M3: Extended Auth Flows (Refresh, Profile, Reset, Logout)

**Objective:** Complete the remaining auth surfaces — token refresh, profile retrieval, password reset (two-step), and PRD-required logout/revocation — with rate limits and session invalidation semantics correct. | **Duration:** Weeks 6–7 | **Entry:** M2 exit criteria met; API-001/002 stable; OQ-003 (sync vs async reset email) decided; OQ-004 (max refresh tokens per user) decided. | **Exit:** API-003..006 and new logout endpoint pass integration tests; silent refresh works; reset tokens expire at 1 hour and are single-use; logout revokes all refresh tokens for the caller.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|API-004|POST `/v1/auth/refresh` endpoint|Exchange refresh token for new AuthToken pair; revoke old refresh token.|TokenManager, AuthService|COMP-005, COMP-006|200 with new pair; 401 on expired/revoked; old refresh revoked atomically; new refresh replaces prior entry; rate limit 30/min/user|M|P0|
|2|FR-AUTH-003|JWT token issuance and refresh|Access 15-min TTL and refresh 7-day TTL behind API-004 via TokenManager.|TokenManager|API-004, COMP-007|access exp = now+900s; refresh exp = now+604800s; refresh rotation on every use; revoked refresh:401|M|P0|
|3|API-003|GET `/v1/auth/me` endpoint|Return caller UserProfile for valid accessToken.|AuthService|COMP-005, DM-001|200 with full UserProfile (id,email,displayName,createdAt,updatedAt,lastLoginAt,roles); 401 on expired/invalid; rate limit 60/min/user|S|P0|
|4|FR-AUTH-004|User profile retrieval|End-to-end profile retrieval behind API-003.|AuthService|API-003|valid token returns full UserProfile; expired/invalid:401; response matches DM-001 shape exactly; no password_hash leaked|S|P0|
|5|API-005|POST `/v1/auth/reset-request` endpoint|Generate 1h single-use reset token; send email via SendGrid; enumeration-safe response.|AuthService, Email|COMP-005, INFRA-EMAIL-001|identical 200/202 for registered and unregistered emails; reset token ttl=3600s, single-use; rate limit 5/min/IP|M|P0|
|6|API-006|POST `/v1/auth/reset-confirm` endpoint|Validate reset token; update password; invalidate all existing sessions for the user.|AuthService, PasswordHasher, TokenManager|COMP-005, COMP-008, COMP-006|200 on success; 401 on invalid/expired/used token; 400 on weak new pw; all refresh tokens for user revoked; used reset token cannot be reused|M|P0|
|7|FR-AUTH-005|Password reset flow end-to-end|Two-step reset binding API-005 and API-006 with 1-hour expiry and single-use semantics.|AuthService|API-005, API-006|reset email within 60s; link expires at 1h; used token rejected; new password invalidates all sessions|M|P0|
|8|FR-AUTH-006|Logout / refresh-token revocation (PRD gap; see OQ-008)|Add POST `/v1/auth/logout` to revoke caller's refresh token(s). Required by PRD user story "log out on shared device".|AuthService, TokenManager|COMP-005, COMP-006, OQ-008|200 on success; caller's refresh token revoked; optional `all_devices=true` revokes every refresh token for user; no-op idempotent on already-revoked token|S|P0|
|9|MIG-RESETFLOW|Reset email sync vs async decision (OQ-003)|Implement per OQ-003 resolution — SendGrid delivery with retry/backoff; queue if async.|AuthService, Queue (optional)|OQ-003|Decision recorded in ADR; chosen path tested under 500-email burst; reset delivery observed < 60s p95|S|P1|
|10|CAP-REFRESH-LIMIT|Per-user refresh token cap (OQ-004)|Enforce max refresh tokens per user across devices per OQ-004 resolution.|TokenManager, Redis|OQ-004, COMP-006|Cap applied; oldest token evicted on overflow; device list API considered for M4; test asserts cap enforced|S|P1|
|11|NFR-PERF-003|Refresh p95 < 100ms|Instrument TokenManager.refresh; verify APM baseline and Redis read latency.|TokenManager, APM|API-004|refresh p95 < 100ms in staging; Redis GET+SETEX budget < 20ms; alert on regression|S|P0|
|12|SESSION-INVAL-001|Session invalidation on password change|Invalidate all refresh tokens on password change / reset-confirm / forced revocation.|TokenManager|API-006, FR-AUTH-006|integration test: after reset-confirm, any prior refresh token returns 401; invariant also applies to admin-forced reset|S|P0|
|13|FR-RESET-RATE|Reset-request rate limit hardening|Add gateway rate limit for API-005 and per-account throttle.|API Gateway, AuthService|API-005, INFRA-RATELIMIT-001|5 req/min/IP; 3 req/hour per email account; violations:429; metrics exposed|S|P1|
|14|NFR-COMP-001|GDPR consent at registration|Capture consent_at timestamp + consent_version at register; expose on profile admin endpoint.|AuthService, PostgreSQL|DM-001, API-002|consent_at NOT NULL on register; consent_version persisted; consent withdrawal runbook defined|M|P0|

### Integration Points — M3

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|Reset token store|Registry (token_hash → user_id, exp, used)|M3|M3|API-005, API-006|
|SendGrid transactional template|Strategy (SMTP/API)|M1→M3|M3|API-005|
|Logout handler|Dispatch route|M3|M3|FR-AUTH-006|
|Session invalidation hook|Event binding (on password change)|M3|M3|TokenManager|
|Refresh cap enforcer|Middleware in TokenManager.issue|M3|M3|COMP-006|

### Milestone Dependencies — M3

- Prior: M2 (AuthService, TokenManager, JwtService, PasswordHasher, API-001/002).
- Decisions required: OQ-003, OQ-004, OQ-008.

### Open Questions — M3

|#|ID|Question|Impact|Owner|Target|
|---|---|---|---|---|---|
|1|OQ-003|Password-reset emails sent synchronously or asynchronously?|Medium — affects reset latency and failure handling|Engineering|Before M3 kickoff|
|2|OQ-004|Maximum refresh tokens per user across devices?|Medium — drives Redis capacity planning and CAP-REFRESH-LIMIT|Product|Before M3 week 2|
|3|OQ-006|Support "remember me" to extend session duration?|Low — only if in-scope for v1; otherwise deferred|Product|Before M3 exit|
|4|OQ-008|FR-AUTH-006 logout/revocation endpoint — PRD requires; TDD should be updated to include it.|High — PRD JTBD gap; must exist for shared-device use case|Product + auth-team|Before M3 week 1|
|5|OQ-001|Should AuthService support API key authentication for service-to-service calls?|Low — out-of-scope for v1 per Sam persona's stated refresh-token flow; confirm deferral|test-lead|Before M3 exit|

### Risk Assessment and Mitigation — M3

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-001 token theft via XSS|High|Low|Session hijacking, account takeover|Access token in memory only; refresh in HttpOnly cookie enforced in M4; short TTL; revoke+force reset on detection|Security|
|2|R-006 email delivery failures|Low|Medium|Password reset blocked for affected users|SendGrid delivery monitoring; alerting in M6; support fallback channel documented|auth-team|
|3|Reset token leak or replay|High|Low|Account takeover via reset link|Single-use enforcement; 1h TTL; token stored as hash in DB; log all reset events|Security|

## M4: Frontend Integration

**Objective:** Ship the three end-user surfaces and the `AuthProvider` that wires tokens, silent refresh, 401 interception, and redirect logic to the backend APIs. | **Duration:** Weeks 8–9 | **Entry:** M2 API-001/002 stable; M3 API-003/004 contract-frozen (M4 can start once contracts are frozen, does not need M3 exit). | **Exit:** Alex happy-path journeys (signup → dashboard, login → dashboard, logout, password reset) pass E2E on staging; silent refresh verified across a 16-minute tab session; client-side validation mirrors backend rules.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|COMP-004|`AuthProvider` React context|Wraps app; manages AuthToken state; intercepts 401; triggers silent refresh; redirects unauthenticated users.|AuthProvider|API-003, API-004|exposes user+token; refreshes silently 60s before expiry; queues inflight requests during refresh; redirect to /login on terminal 401|M|P0|
|2|COMP-001|`LoginPage` route|Email/password form; calls API-001; stores tokens via AuthProvider; optional redirectUrl prop.|LoginPage|COMP-004, API-001|valid creds redirect to onSuccess target; invalid shows generic error; 423 shows locked-account message; respects redirectUrl query|M|P0|
|3|COMP-002|`RegisterPage` route|Email/password/displayName form; client-side strength validation; GDPR consent checkbox; termsUrl prop.|RegisterPage|COMP-004, API-002, NFR-COMP-001|client validates pw strength identically to backend; consent checkbox required and submitted; 409 shown as "try login or reset"; happy path redirects to dashboard|M|P0|
|4|COMP-003|`ProfilePage` route|Authenticated route showing UserProfile per API-003.|ProfilePage|COMP-004, API-003|shows email, displayName, createdAt; protected by AuthProvider; 401 triggers refresh then redirect|S|P1|
|5|FE-LOGOUT-001|Logout control + flow|Global logout control calls FR-AUTH-006 endpoint and clears AuthProvider state.|AuthProvider|FR-AUTH-006|click ends session; refresh token revoked server-side; redirect to landing; second-tab also logged out via storage event|S|P0|
|6|FE-SILENTREFRESH|Silent refresh loop|AuthProvider timer refreshes access token transparently before expiry.|AuthProvider|API-004, FR-AUTH-003|refresh 60s pre-expiry; retries once on transient error; terminal failure triggers redirect to /login|S|P0|
|7|FE-RESETUI|Reset-request and reset-confirm UI|Two forms wired to API-005 and API-006 with consistent enumeration-safe messaging.|AuthPages|API-005, API-006|reset-request shows same success regardless of registration; reset-confirm enforces same policy as register; success redirects to /login|M|P0|
|8|FE-CAPTCHA|CAPTCHA after 3 failed logins (mitigates R-002)|Integrate CAPTCHA challenge on LoginPage after 3 consecutive client-observed failures.|LoginPage, CAPTCHA provider|COMP-001|after 3 failures, form requires CAPTCHA token; backend verifies at gateway; failure to pass CAPTCHA:400|M|P1|
|9|FE-TOKENSTORAGE|Token storage strategy|Access token in memory only; refresh token in HttpOnly cookie (set by backend); clear on tab close.|AuthProvider|R-001|access token never persisted to localStorage; refresh cookie Secure+HttpOnly+SameSite=Strict; unload handler clears state|S|P0|
|10|FE-ROUTING|Protected vs public route guard|Route-level guard for ProfilePage and any future authenticated route.|AuthProvider|COMP-004|unauth user redirected to /login with returnUrl; after login, returnUrl honored; public routes bypass guard|S|P1|
|11|FE-A11Y-001|Accessibility baseline for auth pages|Ensure WCAG 2.1 AA for Login/Register/Profile forms (labels, contrast, keyboard nav).|LoginPage, RegisterPage, ProfilePage|COMP-001, COMP-002, COMP-003|axe-core scan 0 critical; keyboard-only flow completes; screen-reader announces inline errors|S|P1|

### Integration Points — M4

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|AuthProvider context|React DI (context provider)|M4|M4|App, all routes|
|401 interceptor|Fetch middleware chain|M4|M4|Every authenticated fetch|
|Storage event listener|Event binding (cross-tab logout)|M4|M4|AuthProvider|
|CAPTCHA provider|Strategy (provider-specific)|M4|M4|LoginPage|
|Silent-refresh timer|Dispatch (setTimeout registry keyed on expiry)|M4|M4|AuthProvider|

### Milestone Dependencies — M4

- Prior: M2 (API-001/002), M3 contract-freeze on API-003/004/005/006 and FR-AUTH-006.

### Risk Assessment and Mitigation — M4

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-001 XSS-mediated token theft|High|Low|Session hijack|Access token in memory only; HttpOnly refresh cookie; CSP enforced at gateway|frontend-team|
|2|R-004 low registration adoption (PRD business risk)|Medium|Medium|Personalization revenue delayed|Usability testing pre-launch; funnel instrumentation; iterate based on data|product-team|
|3|Refresh race condition (concurrent tabs)|Medium|Medium|Two tabs race to refresh, one gets 401|Single-flight refresh via AuthProvider; storage-event coordination|frontend-team|

## M5: Testing and Hardening

**Objective:** Execute the test pyramid and security hardening so release criteria (unit coverage > 80%, load p95 < 200ms at 500 concurrent, pen test passed) are met. | **Duration:** Weeks 10–11 | **Entry:** M2–M4 feature-complete in staging. | **Exit:** All TEST-001..006 green in CI; 500-concurrent k6 run passes NFR-PERF-002; pen test shows zero P0/P1; contract tests green for error envelope and API versioning.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|TEST-001|Unit: login valid credentials returns AuthToken|Jest test on AuthService.login with mocked dependencies.|AuthService (unit)|COMP-005, COMP-008|returns AuthToken with non-empty accessToken + refreshToken; PasswordHasher.verify mocked true; TokenManager.issueTokens called once|S|P0|
|2|TEST-002|Unit: invalid credentials returns 401|Jest test asserting 401 without AuthToken and without TokenManager call.|AuthService (unit)|COMP-005|returns 401; no issueTokens call; no enumeration in message|S|P0|
|3|TEST-003|Unit: token refresh with valid refresh token|Jest test on TokenManager.refresh with Redis and JwtService mocked.|TokenManager (unit)|COMP-006, COMP-007|old token revoked; new AuthToken pair issued; Redis keys updated atomically|S|P0|
|4|TEST-004|Integration: registration persists UserProfile|Supertest + testcontainers Postgres; register, then re-fetch row.|AuthService + Postgres|API-002, DM-001|row persisted with bcrypt hash; returned payload matches persisted fields; password_hash never returned|M|P0|
|5|TEST-005|Integration: expired refresh rejected|Supertest + testcontainers Redis with accelerated TTL.|TokenManager + Redis|API-004|expired refresh:401; no new pair issued; Redis entry absent|M|P0|
|6|TEST-006|E2E: user registers then logs in|Playwright: RegisterPage → LoginPage → ProfilePage under AuthProvider.|Frontend + Backend|COMP-001..004|full journey passes; profile page shows correct UserProfile; silent refresh fires during session|M|P0|
|7|NFR-PERF-002|Concurrent authentication SLO|Define, measure, and document the 500-concurrent-login SLO for AuthService.|AuthService|NFR-PERF-001|SLO documented; measurement harness recorded; TEST-LOAD-001 is the validation method|S|P0|
|8|TEST-LOAD-001|Load test: 500 concurrent logins|k6 script against staging; record p95 login latency, error rate, Redis usage.|AuthService|NFR-PERF-001, NFR-PERF-002, API-001|sustain 500 concurrent; login p95 < 200ms; error rate < 0.1%; no Redis connection failures|M|P0|
|9|TEST-SEC-001|Penetration test on auth endpoints|External or internal sec team pen test covering OWASP Top 10 for auth.|AuthService|API-001..006, FR-AUTH-006|zero P0/P1 findings; P2 findings triaged and dispositioned; report archived|L|P0|
|10|TEST-CONTRACT-001|Contract test for error envelope|Schema-validated tests asserting AUTH_* error codes and response shape.|AuthService|API-ERR-001|every 4xx/5xx response matches envelope schema; stack traces never present in prod profile|S|P0|
|11|TEST-ENUM-001|Enumeration-safety regression tests|Automated tests asserting identical responses for unknown-email vs wrong-password and registered vs unregistered reset-request.|AuthService|API-001, API-005|response bodies/status identical across enumeration vectors; timing variance within threshold|S|P0|
|12|TEST-COV-001|Unit coverage > 80% for COMP-005..008|Coverage gates on CI enforcing threshold for auth components.|AuthService, TokenManager, JwtService, PasswordHasher|INFRA-CI-001|coverage ≥ 80% per file on COMP-005..008; gate blocks PRs below threshold|S|P0|

### Integration Points — M5

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|Test container fixtures|Registry (pg+redis test containers)|M5|M5|TEST-004, TEST-005|
|k6 load profile|Strategy (scenario/script)|M5|M5|TEST-LOAD-001|
|Playwright CI runners|Dispatch (parallel workers)|M5|M5|TEST-006|
|Coverage gate|CI hook (post-test)|M5|M5|TEST-COV-001|
|Pen test remediation tracker|Registry (findings → owners)|M5|M5|TEST-SEC-001|

### Milestone Dependencies — M5

- Prior: M2, M3, M4 feature complete in staging.

### Risk Assessment and Mitigation — M5

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Load test reveals p95 > 200ms at 500 concurrent|High|Medium|NFR-PERF-001/002 miss; rollout blocked|Profile bottleneck; tune pg-pool, Redis ops, bcrypt cost off hot path; scale HPA earlier|performance|
|2|Pen test P0 finding late in M5|High|Low|M7 cutover slips|Schedule pen test in M5 week 1, not week 2; remediation sprint reserved in M5|Security|
|3|Flaky Playwright E2E suite|Medium|Medium|CI noise delays releases|Quarantine + retries; data seeding stabilized; dedicated flake triage owner|qa|

## M6: Observability and Compliance

**Objective:** Land the structured logs, metrics, traces, alerts, runbooks, and compliance artefacts required for GA and the Q3 2026 SOC2 audit. | **Duration:** Weeks 12–13 | **Entry:** M2–M3 feature-complete; OQ-007 retention resolved; audit-log schema finalized. | **Exit:** Dashboards live, alerts routed, 12-month retention configured, runbooks exercised in a game-day, admin audit-log query endpoint available for Jordan persona.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|OPS-007|Structured logs with sensitive-field redaction|Emit JSON logs for login, registration, refresh, reset, logout; redact passwords/tokens.|AuthService|COMP-005|logs include user_id, event, ts, ip, outcome; redaction confirmed by log-pipeline test; sampling documented|M|P0|
|2|OPS-008|Prometheus metrics exposition|Expose counters and histograms: auth_login_total, auth_login_duration_seconds, auth_token_refresh_total, auth_registration_total.|AuthService|COMP-005|/metrics endpoint scraped; histogram buckets 10/25/50/100/200/500/1000ms; labels: outcome, endpoint|S|P0|
|3|OPS-009|Alerting rules|Alerts for login failure rate > 20%/5min, p95 > 500ms, Redis connection failures.|AuthService, Alertmanager|OPS-008|alerts fire in synthetic test; routed to auth-team on-call; runbook links attached|M|P0|
|4|OPS-010|Distributed tracing via OpenTelemetry|Instrument AuthService → PasswordHasher → TokenManager → JwtService spans end-to-end.|AuthService, OTel|COMP-005..008|trace spans cover full request lifecycle; sampling rate configurable; latency attribution works in staging trace|M|P0|
|5|OPS-001|Runbook: AuthService down|Documented diagnosis + resolution for 5xx cascade.|Runbook|OPS-009|runbook lists symptoms, checks, fixes, escalation; exercised in game-day; link attached to alert|S|P0|
|6|OPS-002|Runbook: token refresh failures|Runbook covering Redis, JwtService key availability, flag state.|Runbook|OPS-009|steps tested in staging; escalation path validated; includes AUTH_TOKEN_REFRESH flag check|S|P0|
|7|OPS-003|On-call expectations document|P1 ack in 15 min; auth-team 24/7 first 2 weeks post-GA; tooling inventory; escalation path.|Runbook|—|document approved; PagerDuty rotations configured; escalation path documented|S|P0|
|8|OPS-004|AuthService capacity plan (pods + HPA)|3 baseline pods; HPA to 10 on CPU > 70%; validate against NFR-PERF-002.|K8s HPA|TEST-LOAD-001|HPA manifest applied; load test triggers scale-out; cool-down tuned; metric recorded in capacity doc|S|P0|
|9|OPS-005|Postgres connection capacity plan|Pool size 100; expand to 200 if wait time > 50ms.|PostgreSQL|INFRA-PGPOOL-001|runbook sets threshold; alerts on wait_time > 50ms; scale procedure documented|S|P1|
|10|OPS-006|Redis memory capacity plan|1GB baseline (~100K refresh tokens ≈ 50MB); scale to 2GB at >70% utilization.|Redis|INFRA-REDIS-001|threshold alert in place; scale procedure documented; backfill/hot-add procedure exercised|S|P1|
|11|NFR-COMP-002|SOC2 Type II audit logging (12-month retention per OQ-007)|Persist auth events in PostgreSQL audit table with 12-month retention + cold archival.|PostgreSQL, AuthService|OQ-007, OPS-007|audit_events table with user_id, event_type, ts, ip, outcome, request_id; 12-month retention policy applied; archival job scheduled|L|P0|
|12|FR-AUDIT-QUERY|Admin audit-log query endpoint (PRD Jordan gap; see OQ-009)|Add admin endpoint/UI to query audit logs by user and date range for incident investigation.|AuthService (admin API)|NFR-COMP-002, OQ-009|filter by user_id and date range; pagination supported; admin-only (role check); access itself audited|M|P0|
|13|COMP-DASH|Compliance dashboard wiring|Grafana/other dashboards for SOC2 evidence gathering: auth events, locks, resets.|Dashboards|OPS-007, NFR-COMP-002|dashboard link shared with compliance; evidence exportable; screenshots archived for audit|S|P1|

### Integration Points — M6

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|Log redaction rules|Middleware chain (logger pipeline)|M6|M6|All COMP-00x backend|
|Prometheus scrape target|Registry (service discovery)|M6|M6|Prometheus|
|OTel exporter|Strategy (OTLP endpoint)|M6|M6|Tracing backend|
|Audit-event writer|Dispatch (AuthService event → audit table)|M6|M6|NFR-COMP-002|
|Alert → runbook binding|Event binding (alert payload includes runbook URL)|M6|M6|On-call pager|

### Milestone Dependencies — M6

- Prior: M2, M3 feature-complete.
- Decisions required: OQ-007 (retention), OQ-009 (admin audit query scope).

### Open Questions — M6

|#|ID|Question|Impact|Owner|Target|
|---|---|---|---|---|---|
|1|OQ-009|PRD Jordan persona JTBD "view auth event logs to investigate incidents" — no corresponding FR in TDD; audit-log query capability unspecified. PRD requires; TDD should be updated to cover FR-AUDIT-QUERY.|High — gap fill required for Jordan persona; drives FR-AUDIT-QUERY scope and admin role model|auth-team + Product|Before M6 week 1|

### Risk Assessment and Mitigation — M6

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-005 compliance failure from incomplete audit logging|Medium|Medium|SOC2 audit finding; go-live slip|Define log schema early (M6 week 1); validate against SOC2 controls; archive retention runbook tested|Compliance|
|2|Audit retention mis-sized (OQ-007 not resolved in time)|High|Low|12-month retention missed; rework needed|Block M6 start on OQ-007 resolution; size Postgres with 12-month headroom by default|platform-team|
|3|Admin audit query exposes excessive PII|Medium|Low|Secondary data exposure|Role-gated; response fields whitelisted; admin access itself audited|Security|

## M7: Migration and Phased Rollout

**Objective:** Execute the three-phase migration (internal alpha → 10% beta → 100% GA) with feature-flag gating, documented rollback, and legacy deprecation. | **Duration:** Weeks 14–16 | **Entry:** M5 green; M6 dashboards/alerts live; release criteria signed off. | **Exit:** 100% traffic on new AuthService for 7 consecutive days; legacy auth endpoints deprecated; flags cleaned up on their stated schedule; post-launch review completed.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|MIG-001|Phase 1 Internal Alpha|1-week deploy to staging; auth-team + QA; AUTH_NEW_LOGIN=OFF except internal.|Rollout|M5, M6|FR-AUTH-001..005 pass manual testing; zero P0/P1 bugs; rollback rehearsed|M|P0|
|2|MIG-002|Phase 2 Beta at 10%|2-week rollout at 10% traffic; monitor latency, error rate, Redis usage, AuthProvider refresh under real load.|Rollout|MIG-001|p95 < 200ms; error rate < 0.1%; zero Redis connection failures across the window|M|P0|
|3|MIG-003|Phase 3 GA at 100%|1-week ramp to 100%; remove AUTH_NEW_LOGIN; enable AUTH_TOKEN_REFRESH globally; deprecate legacy.|Rollout|MIG-002|99.9% uptime across first 7 days; dashboards green; legacy endpoints return 410 after deprecation window|L|P0|
|4|MIG-004|Feature flag `AUTH_NEW_LOGIN`|Gate new LoginPage and API-001; default OFF; cleanup after Phase 3 GA.|Flag|COMP-001, API-001|flag toggles per-percentage; audit trail for changes; removal PR merged after GA|S|P0|
|5|MIG-005|Feature flag `AUTH_TOKEN_REFRESH`|Enable refresh flow in TokenManager; when OFF, only access tokens issued; cleanup 2 weeks after GA.|Flag|COMP-006, API-004|OFF disables refresh path; ON issues refresh tokens; cleanup PR scheduled and tracked|S|P0|
|6|MIG-006|Rollback procedure|Stepwise rollback: disable flag → smoke legacy → investigate → restore backup if needed → comms → post-mortem.|Rollback|MIG-001..005|runbook exists; rehearsed in MIG-001 game-day; 48h post-mortem SLA defined; incident channel named|M|P0|
|7|MIG-007|Rollback triggers|Objective triggers: p95 > 1000ms for > 5min; error > 5% for > 2min; Redis failures > 10/min; any UserProfile corruption.|Rollback|OPS-009|triggers codified in alert rules; on-call trained; dashboard shows trigger status|S|P0|
|8|MIG-LEGACY-DEP|Legacy auth deprecation plan|Communicate, deprecate, then remove legacy auth endpoints.|Rollout, Comms|MIG-003|deprecation header emitted in Phase 2; removal PR after 2-week window; downstream integrators notified|M|P1|
|9|MIG-KEY-ROT|JWT key rotation first-run|Execute RS256 key rotation procedure in staging and prod during Phase 2 or after GA.|JwtService|INFRA-SECRETS-001, NFR-SEC-002|rotation completes without auth outage; old key retained for 1 refresh cycle; runbook updated|M|P1|
|10|RELEASE-CRIT-001|Release criteria gate|Formal gate against §24: unit coverage > 80% on COMP-005..008; SLOs green; pen test clean; compliance sign-off.|Release|TEST-COV-001, TEST-SEC-001, NFR-COMP-002|checklist signed by auth-team + test-lead + Compliance + platform-team; release doc archived|S|P0|
|11|GA-SMOKE-001|GA post-cutover smoke suite|30-minute post-cutover smoke tests over all 6 auth endpoints in prod.|Production|MIG-003|all 6 endpoints return expected status; token round-trip verified; no anomalous alerts|S|P0|
|12|GAMEDAY-001|Pre-GA game day|Simulate AuthService pod loss, Redis outage, SendGrid failure; validate OPS-001/002 runbooks.|All|OPS-001, OPS-002|3 scenarios executed; each runbook performed within documented time; gaps logged and closed before GA|M|P1|
|13|POST-LAUNCH-REVIEW|30-day post-launch review|Review against PRD success metrics (registration > 60%, p95 < 200ms, DAU > 1000, reset completion > 80%, failed login < 5%).|Product, auth-team|MIG-003|metrics vs targets reported; corrective actions owned; insights feed v1.1 planning|S|P1|

### Integration Points — M7

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|Feature flag service|Registry (flag → targeting rule)|M7|M7|MIG-004, MIG-005|
|Rollback switch|Dispatch (flag OFF → legacy path)|M7|M7|MIG-006|
|Deprecation header|Middleware (add `Deprecation` + `Sunset`)|M7|M7|Legacy endpoints|
|Smoke runner|Strategy (post-deploy hook)|M7|M7|GA-SMOKE-001|
|Game-day scenario runner|Dispatch (scenario id → chaos action)|M7|M7|GAMEDAY-001|

### Milestone Dependencies — M7

- Prior: M5 (testing pass), M6 (observability live).
- External: SendGrid production credentials; Legal/Compliance sign-off on NFR-COMP-002.

### Risk Assessment and Mitigation — M7

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-003 data loss during cutover|High|Low|User profile corruption; outage|Parallel run through Phase 1–2; pre-phase full DB backup; idempotent upserts; MIG-006 rehearsed|platform-team|
|2|R-006 SendGrid outage during Phase 2|Low|Medium|Reset flow broken for affected users|Delivery monitoring + alerting; fallback support channel; queue-based retry if chosen in OQ-003|auth-team|
|3|Rollback invoked but legacy path regressed|High|Low|No safe fallback|Legacy smoke in MIG-001; canary on legacy during beta; deprecation only after GA stability|platform-team|
|4|Feature flag misconfiguration at scale|Medium|Medium|Partial outages or leaked exposure|Staged percentage rollout; flag-change audit log; two-person approval for >10% steps|auth-team|

## Resource Requirements and Dependencies

### External Dependencies

|Dependency|Required By MLS|Status|Fallback|
|---|---|---|---|
|PostgreSQL 15+|M1|Provision via INFRA-DB-001|Managed DB fallback (RDS/Cloud SQL) if in-house cluster slips|
|Redis 7+|M1|To be provisioned|Managed Redis (Elasticache/MemoryStore) if self-hosted slips|
|Node.js 20 LTS|M1|Standard|Node 22 LTS upgrade path reserved but not in scope|
|bcryptjs (NPM)|M2|Stable|Replaceable with node-argon2 if perf regression; re-score `PasswordHasher`|
|jsonwebtoken (NPM)|M2|Stable|`jose` library fallback if maintenance issues arise|
|SendGrid (SMTP/API)|M3, M7|To be contracted|Alternative ESP (Mailgun, SES) behind strategy interface INFRA-EMAIL-001|
|API Gateway|M1|Existing platform asset|Dedicated per-service limiter if gateway cannot meet rate-limit contract|
|SEC-POLICY-001|M1|Authority must be confirmed|Block M1 kickoff until policy is available|
|INFRA-DB-001 (provisioning authority)|M1|Upstream platform team|Escalate via platform-team on-call if deadline slips|

### Infrastructure Requirements

- PostgreSQL 15 cluster with read replica, automated backups, and 12-month audit-table retention (post OQ-007 resolution) plus cold archival tier.
- Redis 7 cluster with AOF persistence, 1GB baseline memory (scale trigger at >70% utilization to 2GB), observable connection pool.
- Kubernetes namespace for `auth-service` with HPA (3→10 pods, CPU > 70%), readiness/liveness probes, and secrets volume for RSA keypair.
- API Gateway configuration supporting per-endpoint rate limits, CORS allowlist, TLS 1.3, and the 410-deprecation responses for legacy routes post-GA.
- Observability stack: Prometheus scraping `/metrics`, Grafana dashboards, Alertmanager routes to auth-team PagerDuty, OpenTelemetry collector for distributed traces, log pipeline with redaction middleware.
- CI/CD pipeline with coverage gates, security scanning, container image signing, and staged deploys with automated rollback on SLO burn.

## Risk Register

|ID|Risk|Affected Milestones|Probability|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|R-001|Token theft via XSS allows session hijacking|M3, M4|Low|High|Access token in memory; refresh token in HttpOnly cookie; 15-min access TTL; AuthProvider clears on tab close; revocation + forced password reset if detected|Security|
|R-002|Brute-force attacks on login endpoint|M2, M4, M6|High|Medium|Gateway rate limit 10/min/IP; account lockout 5/15min; bcrypt cost 12; CAPTCHA after 3 failures; WAF IP blocks as contingency|Security|
|R-003|Data loss during migration from legacy auth|M1, M7|Low|High|Parallel run through Phase 1–2; idempotent upserts; full DB backup pre-phase; rehearsed rollback in MIG-006|platform-team|
|R-004|Low registration adoption due to poor UX (PRD business)|M4, M7|Medium|Medium|Usability testing pre-launch; funnel instrumentation; iterate based on data|product-team|
|R-005|Compliance failure from incomplete audit logging|M6, M7|Medium|High|Define log requirements in M6 week 1; validate against SOC2 controls in M5 QA; retention runbook tested|Compliance|
|R-006|Email delivery failures block password reset (PRD operational)|M3, M7|Medium|Low|SendGrid delivery monitoring and alerting; fallback support channel; async queue with retry per OQ-003|auth-team|
|R-007|Redis unavailability impairing TokenManager|M2, M6, M7|Medium|Low|Fail-closed on refresh; users re-login via LoginPage; Redis capacity and alerting in OPS-006/009|auth-team|

## Success Criteria and Validation Approach

|Criterion|Metric|Target|Validation Method|MLS|
|---|---|---|---|---|
|Login performance|APM p95 on AuthService.login()|< 200ms|TEST-LOAD-001 k6 run + prod APM|M2, M5, M7|
|Registration success rate|successful_registrations / attempts|> 99%|Analytics funnel + AuthService metrics|M2, M7|
|Token refresh performance|APM p95 on TokenManager.refresh()|< 100ms|APM instrumentation (NFR-PERF-003)|M3, M5|
|Service availability|Uptime over 30-day rolling window|99.9%|SLO burn-rate alert + status page|M2, M7|
|Password hashing SLA|PasswordHasher.hash() latency|< 500ms at cost 12|Unit benchmark + prod metric|M2|
|Concurrent authentication|Sustained concurrent login requests|500|k6 load test (NFR-PERF-002)|M5|
|Registration conversion|landing→register→confirmed account funnel|> 60%|Analytics funnel on RegisterPage|M4, M7|
|DAU within 30 days GA|AuthToken issuance counts|> 1000|Metric aggregation (PRD)|M7|
|Average session duration|Refresh-event analytics|> 30 minutes|PRD analytics|M7|
|Failed login rate|auth_login_total{outcome="failure"} / total|< 5%|Prometheus + PRD analytics|M5, M7|
|Password reset completion|reset-requested→new-password-set funnel|> 80%|Analytics funnel (PRD)|M7|
|Unit test coverage on core auth components|Coverage on COMP-005..008|> 80%|CI coverage gate (TEST-COV-001)|M5|

## Decision Summary

|Decision|Chosen|Alternatives Considered|Rationale|
|---|---|---|---|
|Session model|Stateless JWT access + Redis-backed refresh|Sticky server-side sessions; database-backed sessions|NFR-PERF-001 requires p95 < 200ms at 500 concurrent (NFR-PERF-002); stateless JWT avoids DB hot-path reads on every request while refresh tokens in Redis preserve revocation (R-001)|
|Password hashing algorithm|bcrypt cost 12|argon2id; scrypt; PBKDF2|TDD §5.2 mandates bcrypt cost 12 and NIST SP 800-63B adaptive hashing (NFR-COMP-003); existing library maturity and ~300ms benchmark inside NFR-PERF-001 budget|
|JWT signing algorithm|RS256 2048-bit|HS256 (shared secret); ES256|NFR-SEC-002 mandates RS256 with 2048-bit keys and quarterly rotation; asymmetric signing supports key rotation without re-distributing shared secrets|
|Rate limiting placement|API Gateway (pre-service)|In-process middleware; WAF-only|R-002 requires uniform enforcement before hitting AuthService; gateway centralizes per-endpoint limits (login 10/min, register 5/min, me 60/min, refresh 30/min)|
|Refresh token storage|Opaque token hashed in Redis (7d TTL)|Self-contained JWT refresh; stateless refresh|Opaque token enables revocation (logout FR-AUTH-006, reset FR-AUTH-005) and device cap (CAP-REFRESH-LIMIT per OQ-004); Redis TTL matches 7-day policy|
|Rollout strategy|3 phases with 2 feature flags + rollback|Big-bang cutover; canary-only|R-003 mitigation requires parallel run; flags allow instant rollback via AUTH_NEW_LOGIN=OFF; matches TDD §5.3 migration plan|
|Audit retention|12 months (PRD SOC2) overriding TDD 90 days|90-day TDD default|OQ-007 resolution: PRD business intent wins; SOC2 Type II audit in Q3 2026 requires 12-month retention (NFR-COMP-002)|
|Logout endpoint (FR-AUTH-006)|Add explicit POST /v1/auth/logout|Rely on implicit token expiry|PRD user story "log out on shared device" (AUTH-E1) cannot be served by expiry alone; OQ-008 requires TDD update; revocation also required for reset-confirm cascade|
|Admin audit-log query (FR-AUDIT-QUERY)|Add admin endpoint for date-range + user-id queries|Direct DB access; external log tool|PRD Jordan JTBD "investigate incidents" has no FR coverage (OQ-009); schema-level filter + role gate required for SOC2 evidence handling|
|Deferred scope (v1.0)|No OAuth/social, no MFA, no RBAC enforcement|Include MFA or OAuth in v1|PRD S12.2 Out-of-Scope explicit; dedicated PRDs planned for MFA (v1.1) and OAuth (v2.0); unblock Q2 2026 personalization window first|

## Timeline Estimates

|MLS|Duration|Start|End|Key Milestones|
|---|---|---|---|---|
|M1|2 weeks|Week 1|Week 2|DB + Redis provisioned; DM-001/002 migrated; RSA keypair mounted; CI green|
|M2|3 weeks|Week 3|Week 5|COMP-005..008 implemented; API-001/002 live in staging; login p95 < 200ms|
|M3|2 weeks|Week 6|Week 7|API-003..006 + FR-AUTH-006; silent refresh verified; reset flow end-to-end|
|M4|2 weeks|Week 8|Week 9|COMP-001..004 shipped; AuthProvider silent refresh; E2E happy path in staging|
|M5|2 weeks|Week 10|Week 11|Unit/integration/E2E green; 500-concurrent load pass; pen test clean|
|M6|2 weeks|Week 12|Week 13|Logs/metrics/traces/alerts live; 12-month audit retention; FR-AUDIT-QUERY available|
|M7|3 weeks|Week 14|Week 16|Phase 1 → Phase 2 (10%) → Phase 3 (100% GA); flag cleanup scheduled|

**Total estimated duration:** 16 weeks (4 months), aligning with Q2 2026 target release and preserving an 8-week buffer before the Q3 2026 SOC2 audit window.

