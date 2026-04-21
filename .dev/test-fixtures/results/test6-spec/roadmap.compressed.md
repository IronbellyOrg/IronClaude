---
spec_source: "test-spec-user-auth.compressed.md"
complexity_score: 0.6
complexity_class: MEDIUM
primary_persona: architect
adversarial: true
base_variant: "A"
variant_scores: "A:86 B:78"
convergence_score: 0.82
---
<!-- CONV: security=SCR, rotation=RTT, TokenManager=TKN, revokeAllForUser=RVK, Milestone=MLS, AuthService=THS, JwtService=JWT, rollback=RLL, COMP-001=C0, REPLAY-001=R0, tests/release=TR, password=PSS, COMP-002=CMP, RefreshTokenRepository=RFR, integration=NTG, Mitigation=MTG, tests/integration=TI, AUTH_SERVICE_ENABLED=ASE, endpoints=NDP, INFRA-003=I0, Authentication=THN, benchmark=BNC, registration=RGS, validation=VLD, Integration=IN1, PasswordHasher=PA1, Dependencies=DPN, architect=RCH, validation=VA1, documented=DCM, PagerDuty=PGR, endpoint=EN1, AuthMiddleware=THM, src/auth/flows=SAF, detection=DTC, whitelist=WHT, COMP-009=CO1, enforced=NFR, tests/auth=TA, COMP-006=CO2, COMP-003=CO3, password_hash=PH, orchestrator=OR1, NFR-AUTH=NA -->

# User THN Service — Project Roadmap

## Executive Summary

Delivery of a stateless JWT-based authentication service spanning RGS, login, token refresh, profile retrieval, and PSS reset, organized as a five-milestone plan that front-loads cryptographic and persistence foundations before building consumer-facing NDP. The architecture is a strict layered stack (THS → TKN → JWT; PA1 as a leaf utility) gated behind a single feature flag for RLL. Sequencing is driven by risk: key management, PSS hashing primitives, and refresh-token replay DTC must be validated before any EN1 traffic is accepted.

**Business Impact:** Establishes the authentication substrate on which all authenticated product surfaces depend; every downstream feature waiting on identity is unblocked at M3 exit. A 99.9% availability target makes this a platform-tier component — outages cascade to every authenticated API.

**Complexity:** MEDIUM (0.6) — 8 requirements across 10 components with high SCR sensitivity (0.8) and elevated risk profile (0.7); overall scope moderated by clear layering and leaf-level testability (0.3).

**Critical path:** Database migrations and RSA key provisioning (M1) → JWT + TKN + PA1 primitives (M2) → THS OR1 + NDP (M3) → load testing validates NA.1 (M4) → E2E lifecycle test (SC-8) passes in staging (M5).

**Key architectural decisions:**

- RS256 asymmetric JWT signing with a 2048-bit RSA floor, private key held in the secrets manager, and a 90-day RTT cadence with a dual-key grace window (drives the key-RTT workstream in M1 and resolution of OI-9 before rollout).
- Stateless access tokens + rotated refresh tokens transported only in an httpOnly cookie scoped `path=/auth/refresh`, with SHA-256 hash persistence for revocation and replay DTC.
- Layered DI-friendly decomposition — every component is injectable, so primitives ship and are validated in M2 before THS orchestration lands in M3.

**Open risks requiring resolution before M1:**

- OI-9 RSA key RTT strategy (dual-key grace period vs. flag-cutover) must be decided before keys are provisioned and secrets-manager wiring is finalized.
- OI-10 Email service vendor selection (SMTP vs. SendGrid vs. SES) must be decided before FR-AUTH.5 dispatcher contract is fixed and M3 sequencing is safe.
- RISK-1 private-key compromise blast radius — key-storage policy and RTT runbook must be drafted before any key material is generated.

## MLS Summary

|ID|Title|Type|Priority|Effort|DPN|Deliverables|Risk|
|---|---|---|---|---|---|---|---|
|M1|Foundation, Data Layer, Key Management|Infrastructure|P0|2w|—|17|HIGH|
|M2|Core THN Primitives|Core|P0|2w|M1|17|HIGH|
|M3|THN Service and Endpoints|Feature|P0|3w|M2|28|MEDIUM|
|M4|Non-Functional Requirements and Observability|Platform|P0|2w|M3|10|MEDIUM|
|M5|Hardening, Validation, and Release|Release|P0|2w|M4|16|MEDIUM|

## Dependency Graph

```
M1 (Foundation + Keys)
  ├── MIG-001 users → MIG-002 refresh_tokens → MIG-003 down-migrations
  ├── DM-001, DM-002, DM-003 → COMP-008 UserRepo, COMP-009 RefreshTokenRepo
  └── INFRA-001 RSA keygen (2048-bit min) → INFRA-002 Secrets Mgr → INFRA-003 Rotation policy → CFG-002 AUTH_SERVICE_ENABLED
           ↓
M2 (Primitives)
  ├── DEP-001 bcrypt → COMP-004 PasswordHasher → CRYPTO-003 cost=12
  ├── DEP-002 jsonwebtoken → COMP-003 JwtService (RS256) → CRYPTO-001
  └── COMP-003 + COMP-009 → COMP-002 TokenManager → CRYPTO-002 SHA-256 → REPLAY-001
           ↓
M3 (Service + Endpoints)
  ├── COMP-002 + COMP-004 + COMP-008 → COMP-001 AuthService
  ├── COMP-001 → FR-AUTH.1 (API-001), FR-AUTH.2 (API-002), FR-AUTH.3 (API-003)
  ├── COMP-002 → COMP-005 AuthMiddleware → FR-AUTH.4 (API-004)
  ├── COMP-010 EmailService → FR-AUTH.5 (API-005, API-006)
  └── COMP-001 + COMP-005 → COMP-006 RoutesIndex
           ↓
M4 (NFRs)
  ├── COMP-006 → OPS-001 APM → NFR-AUTH.1 (p95<200ms)
  ├── OPS-002 Health → OPS-003 PagerDuty → NFR-AUTH.2 (99.9%)
  └── COMP-004 → SEC-001 bcrypt benchmark → NFR-AUTH.3
           ↓
M5 (Release)
  └── SC-1..SC-8 validation → SEC-002 review → FF-001 rollout → GA
```

## M1: Foundation, Data Layer, Key Management

**Objective:** Provision the persistence layer, entity models, repositories, cryptographic key material, and feature-flag plumbing that every later milestone depends on. | **Duration:** 2 weeks (Weeks 1–2) | **Entry:** OI-9 and OI-10 resolved; RISK-1 key-storage policy drafted. | **Exit:** Migrations apply and roll back cleanly in CI; RSA keypair (2048-bit min) stored in secrets manager; feature flag wired; repositories pass unit tests with 100% coverage on CRUD paths.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|COMP-007|AuthTablesMigration|Migration module orchestrating creation of users and refresh_tokens tables with reversible down-migration|database/migrations/003-auth-tables.ts|MIG-001,MIG-002,MIG-003|up creates both tables; down drops in reverse order; idempotent on rerun; CI test proves reversibility|M|P0|
|2|MIG-001|users table migration|Forward/backward migration creating users table with unique email index|database|—|columns: id:UUID-PK, email:unique-idx, display_name:varchar, PH:varchar, is_locked:bool, created_at:timestamptz, updated_at:timestamptz; email unique constraint|S|P0|
|3|MIG-002|refresh_tokens table migration|Forward/backward migration creating refresh_tokens with FK and indexes|database|MIG-001|columns: id:UUID-PK, user_id:FK→users.id, token_hash:varchar, expires_at:timestamptz, revoked:bool, created_at:timestamptz; idx(user_id); idx(token_hash)|S|P0|
|4|MIG-003|Down-migration scripts|Explicit down scripts for MIG-001 and MIG-002 covering drop order and constraint removal|database|MIG-001,MIG-002|down executes without error after up; CI job runs up→down→up cycle green|S|P0|
|5|DM-001|UserRecord entity|Persistence model for users table with app-layer field types|src/auth/models|MIG-001|id:UUID-v4; email:string-unique-indexed; display_name:string; PH:bcrypt-string; is_locked:boolean; created_at:Date; updated_at:Date|S|P0|
|6|DM-002|RefreshTokenRecord entity|Persistence model for refresh_tokens with FK to UserRecord|src/auth/models|DM-001,MIG-002|id:UUID-v4; user_id:FK→UserRecord.id; token_hash:SHA-256-string; expires_at:Date; revoked:boolean; created_at:Date|S|P0|
|7|DM-003|AuthTokenPair DTO|Response DTO returned from login/refresh NDP|src/auth/dto|—|access_token:JWT-string-15min-TTL; refresh_token:opaque-string-7d-TTL; no PH; no token_hash; DTO-001 WHT applies|S|P0|
|8|COMP-008|UserRepository|Persistence-layer abstraction for UserRecord CRUD|src/auth/repositories/user-repository.ts|DM-001|findByEmail; findById; create; updatePasswordHash; setLocked; updatedAt auto-bumps on write|M|P0|
|9|CO1|RFR|Persistence-layer abstraction for RefreshTokenRecord CRUD|src/auth/repositories/refresh-token-repository.ts|DM-002|create; findByHash; revokeById; RVK; listActiveByUser; prunes expired rows on read|M|P0|
|10|INFRA-001|RSA key pair generation|Tooling to generate RS256-compatible RSA key pair (2048-bit min) for JWT signing|infra/scripts/gen-keys|—|2048-bit RSA minimum NFR; private and public PEM produced; private matches secrets-manager format; public embeddable in JWKS|S|P0|
|11|INFRA-002|Secrets manager NTG|Wire private RSA key retrieval through secrets manager provider at boot|src/infra/secrets|INFRA-001|key fetched at boot; never logged; kms-level ACL restricts access; cold-start fetch<500ms|M|P0|
|12|I0|Key RTT 90-day cadence|Rotation policy and scheduled job with dual-key grace window for token validity overlap|infra/ops|INFRA-002,OI-9|two active keys supported (n, n+1); RTT schedulable without restart; old key honored for refresh TTL window|L|P0|
|13|CFG-001|Environment configuration schema|Typed config loader for all auth-related env vars (TTLs, bcrypt cost, flag, email vendor, bcrypt timing band override)|src/config|—|fails fast on missing required vars; unit test enumerates every required key; defaults DCM|S|P0|
|14|CFG-002|Feature flag ASE|Gating flag controlling `/auth/*` route registration for safe rollout/RLL|src/config|CFG-001|false → routes not registered; true → routes live; flip requires no deploy|S|P0|
|15|TEST-M1-001|UserRepository unit tests|Verify every repository method against in-memory/test DB|TA|COMP-008|100% branch coverage; negative paths (not-found, dup email) tested|S|P0|
|16|TEST-M1-002|RFR unit tests|Verify revocation, listing, and pruning semantics|TA|CO1|RVK marks every active row revoked; pruning excludes expired|S|P0|
|17|TEST-M1-003|Migration up/down/up cycle test|CI job proves MIG-001/002/003 reversibility|tests/ci|MIG-003|up→down→up green; schema hash matches baseline|S|P0|

### IN1 Points — M1

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|CFG-002 ASE|Feature flag|M1 (declared, off)|M1|CO2 RoutesIndex (M3)|
|INFRA-002 Secrets manager provider|DI binding|M1|M1|CO3 JWT (M2)|
|I0 Key RTT scheduler|Cron/registry entry|M1|M1|CO3 JWT (M2), M5 ops runbook|
|COMP-008 UserRepository|DI binding (IUserRepository)|M1|M1|C0 THS (M3)|
|CO1 RFR|DI binding (IRefreshTokenRepository)|M1|M1|CMP TKN (M2)|

### MLS DPN — M1

- External: Secrets manager must be provisioned and reachable from CI (OI-9 resolution sets RTT mechanism). No intra-roadmap prerequisites.

### Open Questions — M1

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OI-9|How is the RSA key pair rotated in production without invalidating active tokens (dual-key grace period vs. cutover)?|Determines I0 design; dual-key requires JWT multi-key verification path|RCH|Before M1 Week 1 exit|
|2|OI-10|Which email service vendor/protocol is used (SMTP, SendGrid, SES)?|Fixes COMP-010 contract and M3 sequencing; client library choice affects CFG-001|RCH + devops|Before M1 Week 2 exit|

### Risk Assessment and MTG — M1

|#|Risk|Severity|Likelihood|Impact|MTG|Owner|
|---|---|---|---|---|---|---|
|1|RISK-1 JWT private-key compromise allows token forgery|HIGH|LOW|HIGH|RS256 asymmetric with 2048-bit RSA floor; private key only in secrets manager; I0 RTT; audit access logs|SCR|
|2|Migration not reversible in prod (data loss on RLL)|HIGH|LOW|HIGH|MIG-003 mandatory; TEST-M1-003 gates CI; dry-run on staging|backend|
|3|Secrets manager unreachable at cold start blocks boot|MEDIUM|LOW|HIGH|Fail-fast + runbook fallback to cached key for read-only auth (INFRA-002)|devops|

## M2: Core THN Primitives

**Objective:** Implement PA1, JWT, and TKN as independently testable primitives that the THS OR1 will compose in M3. | **Duration:** 2 weeks (Weeks 3–4) | **Entry:** M1 exit met (repositories, keys, flag). | **Exit:** bcrypt cost factor 12 benchmarked within DCM timing band; RS256 sign/verify round-trip passes with dual-key; refresh RTT with replay DTC proven by unit tests; TKN emits AuthTokenPair matching DM-003 exactly.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|DEP-001|bcrypt npm dependency|Pin bcrypt to a vetted version with native-binding support|package.json|—|version pinned; license compatible; supply-chain scan green|S|P0|
|2|DEP-002|jsonwebtoken npm dependency|Pin jsonwebtoken library with RS256 support|package.json|—|version pinned; CVE scan green; algorithm WHT supports RS256|S|P0|
|3|COMP-004|PA1|bcrypt wrapper exposing hash and compare with configurable cost factor|src/auth/PSS-hasher.ts|DEP-001,CFG-001|hash(plain)→bcrypt-hash; compare(plain,hash)→bool; cost read from config; constant-time failure path|M|P0|
|4|CRYPTO-003|bcrypt cost factor enforcement|Enforce cost=12 at config load and reject lower values in production|src/auth/PSS-hasher.ts|COMP-004|startup rejects cost<12 when NODE_ENV=production; unit test asserts cost=12 in produced hash string|S|P0|
|5|CO3|JWT|RS256 sign and verify wrapper supporting multi-key verification during RTT|src/auth/jwt-service.ts|DEP-002,INFRA-002,I0|sign→JWT with kid header; verify→payload or throws; supports n and n+1 key ids; clock skew tolerance configurable|M|P0|
|6|CRYPTO-001|RS256 asymmetric signing enforcement|Hard-coded algorithm WHT rejecting any non-RS256 JWT on verify|src/auth/jwt-service.ts|CO3|alg=none rejected; alg=HS256 rejected; only alg=RS256 accepted; negative tests present|S|P0|
|7|CMP|TKN|Issues, rotates, and revokes AuthTokenPair with refresh-token replay DTC|src/auth/token-manager.ts|CO3,CO1|issue(userId)→DM-003; refresh(token)→rotated DM-003; detectReplay(usedHash)→RVK; TTLs access=15min, refresh=7d|L|P0|
|8|CRYPTO-002|SHA-256 refresh-token hash|Refresh tokens stored only as SHA-256 hashes, never in plaintext|src/auth/token-manager.ts|CMP|DB insert uses sha256(token); comparison uses timing-safe equal; plaintext never logged|S|P0|
|9|R0|Refresh-token replay DTC|Detect reuse of a previously-rotated refresh token and revoke all tokens for that user|src/auth/token-manager.ts|CMP,CO1|rotated token reused → RFR.RVK; event emitted; returns 401|M|P0|
|10|VALID-001|Password policy validator|Pure utility enforcing 8+ chars, uppercase, lowercase, digit|src/auth/validators/PSS-policy.ts|—|rejects<8 chars; rejects missing class; unit tests enumerate all four failure modes|S|P0|
|11|VALID-002|Email format validator|Pure utility validating RFC-5322 compliant email|src/auth/validators/email.ts|—|rejects malformed; accepts unicode local-part; unit tests cover edge cases|S|P0|
|12|TEST-M2-001|PA1 unit + BNC|Cost-factor assertion plus timing BNC proving ~250ms/hash on CI hardware|TA|COMP-004,CRYPTO-003|cost=12 asserted from hash string; BNC p95 within DCM range; SC-3 satisfied|S|P0|
|13|TEST-M2-002|JWT unit tests|Sign→verify round-trip; tampered signature rejected; expired token rejected; alg=none rejected|TA|CO3,CRYPTO-001|round-trip green; 4 negative paths proven|S|P0|
|14|TEST-M2-003|JWT dual-key RTT test|Token signed with old key verifies during grace window; signed with new key verifies always|TA|I0,CO3|both key ids verify during window; old rejected after window expiry|S|P0|
|15|TEST-M2-004|TKN RTT test|Issue→refresh returns new pair; old refresh token marked revoked|TA|CMP,CRYPTO-002|SHA-256 hash mismatch raises error; revoked flag set on rotated row|S|P0|
|16|TEST-M2-005|Replay-DTC test|Reusing a revoked refresh token triggers RVK|TA|R0|all active refresh tokens for user revoked; SC-7 satisfied|M|P0|
|17|TEST-M2-006|Password policy + email validator tests|Exhaustive truth table for VALID-001 and VALID-002|TA|VALID-001,VALID-002|every rule has passing and failing sample; SC-6 unblocked|S|P1|

### IN1 Points — M2

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|COMP-004 PA1|DI binding (IPasswordHasher)|M2|M2|C0 THS (M3)|
|CO3 JWT|DI binding (IJwtService)|M2|M2|CMP TKN (M2), COMP-005 THM (M3)|
|CMP TKN|DI binding (ITokenManager)|M2|M2|C0 THS (M3), COMP-005 THM (M3)|
|R0|Event emitter → audit sink|M2 (declared), wired in M4 (OPS-001)|M2|M4 observability|
|VALID-001, VALID-002|Strategy functions|M2|M2|C0 THS (M3) register flow|

### MLS DPN — M2

- M1 (repositories, secrets manager, CFG-001 config, I0 RTT policy).

### Risk Assessment and MTG — M2

|#|Risk|Severity|Likelihood|Impact|MTG|Owner|
|---|---|---|---|---|---|---|
|1|RISK-3 bcrypt cost=12 insufficient for future hardware|MEDIUM|LOW|MEDIUM|Cost read from config (CRYPTO-003); annual OWASP review scheduled; Argon2id migration path DCM|SCR|
|2|JWT algorithm confusion / alg=none acceptance|HIGH|LOW|HIGH|CRYPTO-001 algorithm WHT; negative tests in TEST-M2-002|SCR|
|3|Rotation grace window allows extended acceptance of stolen key|MEDIUM|LOW|HIGH|I0 bounds grace window to refresh TTL (7d); monitoring of kid distribution|SCR|

## M3: THN Service and Endpoints

**Objective:** Compose primitives into THS OR1 and ship all five functional NDP behind the feature flag with middleware, routing, rate-limiting, and email NTG wired. | **Duration:** 3 weeks (Weeks 5–7) | **Entry:** M2 exit met (primitives green). | **Exit:** All five `/auth/*` NDP live behind CFG-002; NTG tests cover happy + negative paths; email service dispatches reset emails end-to-end in staging.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|C0|THS|Core OR1 coordinating login, register, refresh, profile, and reset flows|src/auth/auth-service.ts|CMP,COMP-004,COMP-008,CO1|exposes login, register, refresh, getProfile, requestPasswordReset, confirmPasswordReset; each maps to exactly one FR; DI-constructed|L|P0|
|2|COMP-005|THM|Bearer token extraction and verification in request pipeline|src/middleware/auth-middleware.ts|CMP,CO3|extracts Authorization: Bearer; verifies via JWT; attaches userId to request; 401 on missing/invalid|M|P0|
|3|CO2|RoutesIndex|Registers `/auth/*` route group, gated by ASE|src/routes/index.ts|C0,COMP-005,CFG-002|routes registered only when flag=true; handler wiring matches each FR EN1; no routes leak when flag=false|M|P0|
|4|COMP-010|EmailService NTG|Adapter dispatching PSS-reset emails via selected vendor (resolution of OI-10)|src/integrations/email-service.ts|OI-10|send(to,template,vars) returns messageId or retries; failures logged with correlation id; vendor pluggable|L|P0|
|5|FR-AUTH.1|User login|Authenticate via email/PSS, return AuthTokenPair|SAF|C0,COMP-004|valid→200 DM-003; invalid→401 generic; locked→403; rate-limit 5/min/IP NFR|M|P0|
|6|API-001|POST /auth/login|HTTP binding for FR-AUTH.1 under `/auth/*` namespace|src/routes/auth/login.ts|FR-AUTH.1,CO2|request schema: email,PSS; responses 200/401/403/429; no PSS in logs|S|P0|
|7|FR-AUTH.2|User RGS|Register new user with VA1 and bcrypt hash|SAF|C0,VALID-001,VALID-002|valid→201 profile; dup email→409; PSS policy NFR via VALID-001; email format NFR via VALID-002|M|P0|
|8|API-002|POST /auth/register|HTTP binding for FR-AUTH.2; exact path resolves OI-3|src/routes/auth/register.ts|FR-AUTH.2,CO2,OI-3|request: email,PSS,display_name; responses 201/400/409; PH never returned|S|P0|
|9|FR-AUTH.3|Token refresh|Rotate refresh token and issue new access token|SAF|C0,CMP,R0|valid→new DM-003 and revoke prior; expired→401; replayed→revoke-all-user-tokens; SC-7 satisfied|M|P0|
|10|API-003|POST /auth/refresh|HTTP binding for FR-AUTH.3; exact path resolves OI-4|src/routes/auth/refresh.ts|FR-AUTH.3,CO2,OI-4|request: refresh_token in httpOnly cookie; responses 200/401; rotated cookie set with Secure,HttpOnly,SameSite=Strict|S|P0|
|11|FR-AUTH.4|Profile retrieval|Return authenticated user's public profile|SAF|C0,COMP-005|valid Bearer→200 {id,email,display_name,created_at}; expired/invalid→401; no PH or token_hash in body|S|P0|
|12|API-004|GET /auth/me|HTTP binding for FR-AUTH.4|src/routes/auth/me.ts|FR-AUTH.4,COMP-005|THM required; response schema matches AC exactly; field WHT NFR at DTO layer|S|P0|
|13|FR-AUTH.5|Password reset|Two-step flow: request reset email, confirm new PSS|SAF|C0,CMP,COMP-010|registered email→reset token 1h TTL + email dispatched; valid token→PSS updated; expired/invalid→400; all refresh tokens revoked on success|L|P0|
|14|API-005|POST /auth/PSS-reset/request|HTTP binding for FR-AUTH.5 request step; exact path resolves OI-5|src/routes/auth/PSS-reset.ts|FR-AUTH.5,COMP-010,OI-5|accepts email; always 202 regardless of existence (user enumeration guard); rate-limited|S|P0|
|15|API-006|POST /auth/PSS-reset/confirm|HTTP binding for FR-AUTH.5 confirm step; exact path resolves OI-5|src/routes/auth/PSS-reset.ts|FR-AUTH.5,OI-5|accepts token+new_password; valid→204 + revoke-all-sessions; invalid/expired→400|S|P0|
|16|RATE-001|Login rate-limit middleware|Enforce 5-attempts-per-minute-per-IP on API-001|src/middleware/rate-limit.ts|API-001|6th attempt→429; counter keyed by client IP; bypass for known health-check paths; SC-4 satisfied|M|P0|
|17|RATE-002|Password-reset rate-limit|Throttle API-005 per email to mitigate abuse|src/middleware/rate-limit.ts|API-005|per-email throttle DCM; exceeding returns 429; shared Redis/in-memory store configurable|S|P1|
|18|ERR-001|Uniform auth error contract|Standardized error envelope with generic messaging to prevent enumeration|src/auth/errors|C0|401 body identical for invalid email vs invalid PSS; 403 distinguishes locked account; error codes defined|S|P0|
|19|COOKIE-001|httpOnly refresh-token cookie|Refresh token transported only in httpOnly, Secure, SameSite=Strict cookie scoped to refresh path|src/routes/auth|API-001,API-003|no localStorage path; CORS explicitly configured; cookie path=/auth/refresh; expiration=7d|M|P0|
|20|RESET-001|Reset-token issuance and storage|Time-limited reset tokens (1h TTL) stored as SHA-256 hashes|src/auth/token-manager.ts|CMP|TTL=1h; single-use; stored hashed; reused→400; SC-5 partial|S|P0|
|21|SESS-001|Session invalidation on reset|Successful PSS reset revokes all refresh tokens for user|SAF|FR-AUTH.5,CO1|RFR.RVK called in confirm path; NTG test asserts prior refresh tokens 401|S|P0|
|22|DTO-001|Response DTO field WHT|Serializer enforcing no PH, token_hash, reset_hash leakage (single source of truth)|src/auth/dto|DM-001,DM-002|unit test introspects every auth response; forbidden fields absent; FR-AUTH.4 AC NFR|S|P0|
|23|TEST-M3-001|Login NTG test|End-to-end test of API-001 happy + all negative paths|TI|API-001|200 on valid; 401 on invalid; 403 on locked; 429 on rate-limit exceeded|M|P0|
|24|TEST-M3-002|Register NTG test|End-to-end test of API-002 including dup + PSS policy|TI|API-002|201 valid; 409 dup; 400 bad PSS; 400 bad email|M|P0|
|25|TEST-M3-003|Refresh RTT + replay test|IN1 test proving RTT and replay DTC across calls|TI|API-003,R0|rotated token valid; old token→401; replay→revoke-all|M|P0|
|26|TEST-M3-004|Profile retrieval test|IN1 test of API-004 with THM|TI|API-004|valid bearer→200; expired→401; field WHT NFR|S|P0|
|27|TEST-M3-005|Password reset flow test|IN1 test covering request→email-dispatched→confirm→all sessions revoked|TI|API-005,API-006,SESS-001|dispatch observable (mocked COMP-010); confirm revokes all refresh tokens|M|P0|
|28|TEST-M3-006|Error contract test|Negative tests proving no user enumeration and locked distinction|TI|ERR-001|401 bodies identical across invalid-email vs invalid-PSS; 403 only on locked|S|P0|

### IN1 Points — M3

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|C0 THS|DI binding (IAuthService)|M3|M3|CO2 RoutesIndex|
|COMP-005 THM|Middleware chain entry|M3|M3|API-004, all downstream authenticated routes (post-v1.0)|
|CO2 RoutesIndex|Route registry (gated by CFG-002)|M3|M3|App router (consumer of `/auth/*`)|
|COMP-010 EmailService|DI binding (IEmailService)|M3|M3|FR-AUTH.5 via C0|
|RATE-001, RATE-002|Middleware registry (dispatch table)|M3|M3|API-001 and API-005 respectively|
|ERR-001 Error contract|Error-handler registry|M3|M3|All `/auth/*` handlers|
|COOKIE-001|Response middleware|M3|M3|API-001, API-003|

### MLS DPN — M3

- M2 (CMP, CO3, COMP-004, VALID-001, VALID-002, R0); M1 (CO2 prerequisite CFG-002 and repositories).

### Open Questions — M3

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OI-3|Exact EN1 path for registration under `/auth/*`?|Blocks API-002 route wiring and API documentation|RCH|M3 Week 5|
|2|OI-4|Exact EN1 path for token refresh?|Blocks API-003 route wiring and client SDK|RCH|M3 Week 5|
|3|OI-5|Exact EN1 paths for PSS reset request vs. confirm (two-step flow)?|Blocks API-005/006 wiring and email template deep-links|RCH|M3 Week 5|
|4|OI-1|Should PSS reset emails be dispatched synchronously or via a message queue?|Determines API-005 latency and COMP-010 resilience strategy|backend + devops|M3 Week 6|
|5|OI-2|Maximum number of active refresh tokens per user?|Drives CO1 pruning semantics and multi-device UX|RCH|M3 Week 6|

### Risk Assessment and MTG — M3

|#|Risk|Severity|Likelihood|Impact|MTG|Owner|
|---|---|---|---|---|---|---|
|1|RISK-2 Refresh-token replay after theft|HIGH|MEDIUM|HIGH|R0 enforces DTC; TEST-M3-003 proves; COOKIE-001 reduces exposure surface|SCR|
|2|User enumeration via login/reset error responses|MEDIUM|MEDIUM|MEDIUM|ERR-001 uniform 401; API-005 always 202; TEST-M3-006 negative tests|SCR|
|3|Email vendor outage blocks FR-AUTH.5|MEDIUM|MEDIUM|MEDIUM|OI-1 resolution (queue preferred); retry with backoff in COMP-010; status-page fallback messaging|backend|
|4|Rate-limit state not shared across instances|MEDIUM|MEDIUM|MEDIUM|RATE-001 uses central store (Redis) configurable via CFG-001|devops|

## M4: Non-Functional Requirements and Observability

**Objective:** Instrument the service for the latency, availability, and SCR NFRs; ship the monitoring, alerting, and load-testing rigging that gates GA. | **Duration:** 2 weeks (Weeks 8–9) | **Entry:** M3 NDP live in staging behind flag. | **Exit:** k6 run shows p95 < 200ms; health EN1 integrated with PGR; bcrypt BNC recorded as CI artifact; APM dashboards published.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|NA.1|Authentication EN1 response time|p95 < 200ms under normal load across `/auth/*`|src/auth|OPS-001,OPS-004|k6 scenario reproducible in CI; APM panel live; SC-1 satisfied|M|P0|
|2|NA.2|Service availability|99.9% uptime objective with alerting|infra/ops|OPS-002,OPS-003|SLO doc published; PGR escalation policy mapped; SC-2 measurable|M|P0|
|3|NA.3|Password hashing SCR|bcrypt cost factor 12 NFR and benchmarked|src/auth/PSS-hasher.ts|CRYPTO-003,SEC-001|cost asserted in CI; SC-3 satisfied|S|P0|
|4|OPS-001|APM instrumentation|Distributed tracing + p95/p99 metrics for every `/auth/*` route|src/infra/observability|CO2|spans cover handler→THS→TKN→repository; latency histograms exported|M|P0|
|5|OPS-002|Health check EN1|`GET /healthz` returns 200 with DB, secrets, and key cache validated in the response|src/routes/healthz.ts|—|DB ping, secrets, and key cache validated in response; <50ms p95; bypasses RATE-001|S|P0|
|6|OPS-003|PGR alerting|Pager rules on availability, latency, and replay-DTC burst|infra/alerting|OPS-002,R0|alert fires on 5xx > threshold; on p95 > 200ms 5min; on replay events > N/min|M|P0|
|7|OPS-004|k6 load test for NA.1|Repeatable load profile against staging hitting all 5 NDP|tests/load/k6|NA.1|scripts versioned; CI nightly; report compares to baseline|M|P0|
|8|OPS-005|p95 latency dashboard|Grafana panel showing per-EN1 p95 latency and rate-limit hits|infra/dashboards|OPS-001|published with link in runbook; threshold lines drawn at 200ms|S|P1|
|9|SEC-001|bcrypt cost BNC test|CI BNC proving cost=12 hashes within DCM timing band; CI env-var configurable|tests/SCR|CRYPTO-003|p95 between 200ms and 350ms on reference hardware (CI env-var override); failure prints actual ms; SC-3 evidenced|S|P0|
|10|AUDIT-001|Auth event logging hooks|Emit structured events for login success/fail, refresh RTT, replay, reset (foundational for v1.1)|src/auth/audit|R0,C0|events emitted to observability sink; PII redacted; addresses RISK-5/OI-7 partially|M|P1|

### IN1 Points — M4

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|OPS-001 APM tracer|Middleware chain + DI|M4|M4|All `/auth/*` routes; OPS-005|
|OPS-002 /healthz route|Route registration|M4|M4|OPS-003 PGR checks|
|OPS-003 PGR rules|Alerting registry|M4|M4|On-call RTT|
|AUDIT-001 event sink|Event emitter binding|M4|M4|R0 producers; downstream SIEM|
|OPS-004 k6 scripts|CI job binding|M4|M4|Nightly CI + manual pre-release runs|

### MLS DPN — M4

- M3 (NDP live behind flag); M2 (CRYPTO-003 for SEC-001).

### Risk Assessment and MTG — M4

|#|Risk|Severity|Likelihood|Impact|MTG|Owner|
|---|---|---|---|---|---|---|
|1|p95 latency exceeds 200ms under realistic load|HIGH|MEDIUM|HIGH|Pre-GA k6 (OPS-004) + capacity headroom plan; dashboards (OPS-005); cache repository reads where safe|backend|
|2|Health check passes while downstream broken (false green)|MEDIUM|LOW|HIGH|OPS-002 also pings secrets manager and DB; synthetic login probe added in M5|devops|
|3|Alerting noise causes pager fatigue|MEDIUM|MEDIUM|MEDIUM|OPS-003 thresholds tuned against staging baseline; quiet-hours not allowed for SCR events|devops|

## M5: Hardening, Validation, and Release

**Objective:** Validate every success criterion against staging and production-mirror, complete SCR and architecture reviews, finalize rollout/RLL runbook, then enable ASE in production. | **Duration:** 2 weeks (Weeks 10–11) | **Entry:** M4 instrumentation live; SC-1..SC-7 mechanically verifiable. | **Exit:** SC-1..SC-8 all green; SCR review sign-off; flag flipped in production; RLL rehearsal succeeded.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|SC-1|Login EN1 latency VA1|Validate p95<200ms under normal load profile|TR|OPS-004|k6 report attached to release ticket; signed off by perf|S|P0|
|2|SC-2|Service uptime VA1|Validate 99.9% uptime methodology and alert paths|TR|OPS-002,OPS-003|SLO doc reviewed; PGR test page acknowledged; chaos drill executed|S|P0|
|3|SC-3|bcrypt cost factor VA1|Validate cost=12 in production config and BNC|TR|SEC-001|prod config snapshot shows cost=12; SEC-001 CI run attached|S|P0|
|4|SC-4|Login rate-limiting VA1|Validate ≤5/min/IP under attack scenario|TR|RATE-001|burst test triggers 429 at 6th attempt; counter resets per minute|S|P0|
|5|SC-5|Token TTL VA1|Validate access=15min, refresh=7d, reset=1h|TR|CMP,RESET-001|NTG tests assert each TTL boundary; token at TTL+1s rejected|S|P0|
|6|SC-6|Password policy enforcement VA1|Validate 8+ chars, upper, lower, digit NFR end-to-end|TR|VALID-001|TEST-M2-006 + TEST-M3-002 evidenced; reset confirm path also enforces|S|P0|
|7|SC-7|Refresh-token replay-DTC VA1|Validate replay revokes all user tokens|TR|R0|TEST-M3-003 evidence + manual chaos check; AUDIT-001 event observed|S|P0|
|8|SC-8|End-to-end lifecycle test|Register→login→/auth/me→refresh→reset→login-with-new-PSS all succeed|tests/e2e|API-001,API-002,API-003,API-004,API-005,API-006|scripted E2E green in staging; rerun green post-flag-flip in prod|M|P0|
|9|SEC-002|Security review and threat model sign-off|Architect-led review covering RISK-1..RISK-6 mitigations and OWASP ASVS L2 alignment|docs/SCR|all M1–M4 deliverables|review doc filed; outstanding gaps tracked to v1.1; sign-off in PR|M|P0|
|10|SEC-003|Penetration smoke test|Targeted pentest of `/auth/*` covering enumeration, brute force, replay, JWT attacks|tests/SCR|API-001,API-002,API-003,API-004,API-005,API-006|report attached; criticals = 0 to release|M|P0|
|11|FF-001|Feature flag rollout plan|Staged rollout (canary→25%→100%) with kill-switch verified|docs/release|CFG-002|rollout doc approved; RLL drill rehearsed; on-call briefed|S|P0|
|12|BC-001|Backwards-compatibility verification|Existing unauthenticated NDP unaffected during and after rollout|TR|CO2|smoke matrix runs against existing routes pre/post flag|S|P0|
|13|DOC-001|API documentation|OpenAPI 3 spec for `/auth/*` published to docs portal|docs/api|API-001,API-002,API-003,API-004,API-005,API-006|every EN1, error code, schema DCM; drift test in CI|S|P1|
|14|DOC-002|Operations runbook|Runbook covering on-call procedures, key RTT, incident playbooks|docs/runbooks|I0,OPS-003|sections: RTT, replay-burst, key-compromise, email-outage|S|P1|
|15|DOC-003|Migration and RLL guide|Step-by-step for applying MIG-001..003 and rolling back|docs/runbooks|MIG-003|rehearsed in staging; sign-off recorded|S|P1|
|16|OPS-006|Rollback procedure rehearsal|Live drill of CFG-002=false plus migration RLL in staging|TR|FF-001,DOC-003|rehearsal report attached; mean RLL time DCM|M|P0|

### IN1 Points — M5

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|FF-001 rollout plan|Operational checklist|M5|M5|Release management|
|OPS-006 RLL rehearsal|Drill record|M5|M5|Incident response|
|SEC-002 review sign-off|Gate artifact|M5|M5|Release gate|
|DOC-001 OpenAPI spec|Docs registry binding|M5|M5|Downstream client teams|

### MLS DPN — M5

- M4 (NFR instrumentation); M3 (all NDP); M1 (RTT policy + flag).

### Open Questions — M5

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OI-6|Progressive lockout policy after N failed login attempts (beyond rate-limiting)?|Determines whether SC-4 alone is sufficient; influences UX + abuse signals|SCR + product|Decision before v1.1; must be acknowledged in release notes|
|2|OI-7|Which authentication events require audit logging and where do logs persist?|AUDIT-001 emits foundational events but persistence policy missing; affects compliance posture|SCR + devops|Decision before v1.1; partial mitigation in M4|
|3|OI-8|How are refresh tokens revoked when a user account is deleted?|Lifecycle gap (RISK-6); ad-hoc revoke-all-for-user available; needs hook in user-deletion flow|RCH|Decision before v1.1|

### Risk Assessment and MTG — M5

|#|Risk|Severity|Likelihood|Impact|MTG|Owner|
|---|---|---|---|---|---|---|
|1|RISK-4 No account lockout policy after N failed attempts|MEDIUM|MEDIUM|MEDIUM|RATE-001 partial mitigation; OI-6 deferred to v1.1; decision logged in release notes|SCR|
|2|RISK-5 Authentication audit logging not specified|LOW|MEDIUM|LOW|AUDIT-001 ships foundational events; OI-7 deferred; SIEM hook stub left in place|SCR|
|3|RISK-6 Token revocation on user deletion not addressed|MEDIUM|LOW|MEDIUM|RVK exists in CO1; OI-8 will wire it into user-deletion flow in v1.1|RCH|
|4|Rollback fails or causes data loss|HIGH|LOW|HIGH|OPS-006 rehearses; MIG-003 tested in M1; FF-001 enables non-DB RLL first|devops|

## Resource Requirements and DPN

### External DPN

|Dependency|Required By MLS|Status|Fallback|
|---|---|---|---|
|`jsonwebtoken` (npm)|M2|Commodity — pinned in DEP-002|node-jose as drop-in if CVE-blocked (verify currency at incident time)|
|`bcrypt` (npm)|M2|Commodity — pinned in DEP-001|`bcryptjs` (pure JS) as temporary fallback (verify currency at incident time)|
|RSA key pair (RS256, 2048-bit min)|M1, M2|To generate via INFRA-001|Dev-only key for non-prod; no prod fallback|
|Secrets manager|M1|Must be provisioned pre-M1|Boot-time env injection gated to non-prod only|
|Email service (vendor TBD via OI-10)|M3|Blocked by OI-10|Queue + dead-letter queue to decouple API-005|
|Users database table|M1|Created by MIG-001|n/a (hard dependency)|
|Refresh_tokens database table|M1|Created by MIG-002|n/a (hard dependency)|
|Rate-limiting store (Redis or equivalent)|M3|Provisioned by devops|In-memory fallback for single-instance staging only|
|APM (tracing + metrics)|M4|Existing platform tooling|Self-hosted Prometheus if APM unavailable|
|PGR (alerting)|M4, M5|Existing NTG|Opsgenie as tooling equivalent|

### Infrastructure Requirements

- Secrets manager with per-environment ACLs and RTT API support (covers INFRA-002/003).
- Database with transactional DDL for migrations (MIG-001..003) and FK enforcement.
- Central rate-limit store reachable from every API instance (Redis or equivalent).
- APM backend capable of ingesting traces and p95/p99 histograms per route (OPS-001, OPS-005).
- PGR service + escalation policy bound to the auth SLO (OPS-003).
- Email service access (SMTP relay or vendor API per OI-10) with outbound connectivity from the app tier.
- CI runner with stable compute profile for SEC-001 bcrypt BNC (cost=12 timing band depends on CPU; env-var override available).
- Staging environment that mirrors production database and secrets manager for SC-8 E2E and OPS-006 RLL rehearsal.

## Risk Register

|ID|Risk|Affected Milestones|Probability|Impact|MTG|Owner|
|---|---|---|---|---|---|---|
|R-001|RISK-1 JWT private-key compromise allows token forgery|M1, M2, M5|LOW|HIGH|RS256 with 2048-bit floor; key in secrets manager; I0 90-day RTT; access audited (AUDIT-001)|SCR|
|R-002|RISK-2 Refresh-token replay attack after theft|M2, M3, M5|MEDIUM|HIGH|R0 + TEST-M3-003 + COOKIE-001 httpOnly transport with path=/auth/refresh|SCR|
|R-003|RISK-3 bcrypt cost=12 insufficient for future hardware|M2, M4, M5|LOW|MEDIUM|Cost read from config (CRYPTO-003); SEC-001 BNC; annual OWASP review; Argon2id migration path DCM|SCR|
|R-004|RISK-4 No account lockout policy beyond rate-limit|M3, M5|MEDIUM|MEDIUM|RATE-001 partial mitigation; OI-6 deferred to v1.1 with release-notes disclosure|SCR|
|R-005|RISK-5 Auth audit logging policy not specified|M4, M5|MEDIUM|LOW|AUDIT-001 foundational events emitted; OI-7 deferred to v1.1|SCR|
|R-006|RISK-6 Refresh-token revocation on user deletion not wired|M5|LOW|MEDIUM|RVK available (CO1); OI-8 wires into user-deletion flow in v1.1|RCH|
|R-007|Migration not reversible in prod (data loss on RLL)|M1, M5|LOW|HIGH|MIG-003 mandatory; TEST-M1-003 gates CI; OPS-006 rehearsal|backend|
|R-008|Secrets manager unreachable at cold start|M1, M2|LOW|HIGH|Fail-fast boot; runbook fallback; health check (OPS-002) validates|devops|
|R-009|JWT algorithm confusion (alg=none acceptance)|M2|LOW|HIGH|CRYPTO-001 WHT; negative tests in TEST-M2-002|SCR|
|R-010|Rotation grace window extends stolen-key validity|M1, M2|LOW|HIGH|I0 bounds grace to refresh TTL (7d); kid distribution monitored|SCR|
|R-011|User enumeration via login/reset error responses|M3|MEDIUM|MEDIUM|ERR-001 uniform 401; API-005 always 202; TEST-M3-006|SCR|
|R-012|Email vendor outage blocks FR-AUTH.5|M3|MEDIUM|MEDIUM|OI-1 queue-based dispatch; retry+backoff in COMP-010; status-page messaging|backend|
|R-013|Rate-limit state not shared across instances|M3|MEDIUM|MEDIUM|RATE-001 uses central store (Redis) via CFG-001|devops|
|R-014|p95 latency exceeds 200ms under realistic load|M4, M5|MEDIUM|HIGH|OPS-004 k6 pre-GA; capacity headroom plan; repository read caching where safe|backend|
|R-015|Health check reports green while downstream broken|M4, M5|LOW|HIGH|OPS-002 verifies DB + secrets + key cache; synthetic login probe in M5|devops|
|R-016|Alerting thresholds cause pager fatigue|M4|MEDIUM|MEDIUM|OPS-003 thresholds tuned against staging baseline; SCR alerts never silenced|devops|
|R-017|Rollback fails or causes data loss|M5|LOW|HIGH|OPS-006 rehearsal; MIG-003; FF-001 flag-first RLL before DB RLL|devops|

## Success Criteria and Validation Approach

|Criterion|Metric|Target|Validation Method|MLS|
|---|---|---|---|---|
|SC-1 Login latency|p95 response time on `/auth/login` under normal load|< 200ms|k6 load script (OPS-004) + APM panel (OPS-005); release gate in M5|M4, M5|
|SC-2 Service uptime|Monthly uptime against /healthz|≥ 99.9%|Uptime monitor + PGR SLO (OPS-002, OPS-003); chaos drill in M5|M4, M5|
|SC-3 bcrypt cost factor|Cost factor embedded in produced hash|Exactly 12|SEC-001 CI BNC (200–350ms band, env-var override) + config snapshot diff|M2, M4, M5|
|SC-4 Login rate limiting|Requests beyond threshold per IP|≤ 5/min/IP|IN1 test TEST-M3-001 + burst script in M5|M3, M5|
|SC-5 Token TTLs|Access/refresh/reset token expirations|access=15min; refresh=7d; reset=1h|TEST-M2-004, TEST-M3-005; boundary tests in M5|M2, M3, M5|
|SC-6 Password policy|Register + reset reject non-compliant passwords|8+ chars, upper, lower, digit NFR|TEST-M2-006 + TEST-M3-002 + reset-confirm test|M2, M3, M5|
|SC-7 Replay DTC|Reused rotated refresh token|Revokes all refresh tokens for user|TEST-M3-003 + AUDIT-001 event observation|M3, M5|
|SC-8 E2E lifecycle|Register→login→/auth/me→refresh→reset→login-new-PSS|All steps succeed|Scripted E2E in staging; rerun post-flag-flip in prod|M5|

## Decision Summary

|Decision|Chosen|Alternatives Considered|Rationale|
|---|---|---|---|
|JWT signing algorithm|RS256 asymmetric with 2048-bit RSA floor|HS256 symmetric; opaque tokens|Architectural-Constraint-RS256 mandates RS256; RISK-1 blast radius favors asymmetric so verifiers never hold the signing key; 2048-bit floor closes SEC-002 ambiguity|
|Password hash|bcrypt cost=12|Argon2id; scrypt|Architectural-Constraint-BcryptCost12 mandates bcrypt; NA.3 targets ~250ms per hash which aligns with cost=12 per SEC-001 BNC (200–350ms band, CI env-var override)|
|Token storage location (client)|access in memory; refresh in httpOnly cookie scoped `path=/auth/refresh`|localStorage; sessionStorage; broad cookie path|Architectural-Constraint-HttpOnlyCookie mandates httpOnly cookie; `path=/auth/refresh` narrows XSS blast radius so refresh cookie is invisible to every other route|
|Session strategy|Stateless JWT with refresh RTT|Server-side session store; sliding cookies|Architectural-Constraint-StatelessJWT mandates stateless JWT; avoids introducing a session store for a 99.9% availability service (NA.2)|
|Sequencing of primitives vs OR1|Primitives first (M2), OR1 after (M3)|Top-down OR1-first|Risk profile 0.7 + testability 0.3 make leaf-first safer; enables TEST-M2-* gates before any EN1 ships|
|Feature-flag rollout vector|Single flag CFG-002 ASE gating route registration|Per-EN1 flags; percentage rollout via LB|Architectural-Constraint-FeatureFlag mandates single flag; keeps RLL atomic and auditable; FF-001 adds canary staging on top|
|Migrations reversibility|Mandatory down scripts with CI up/down/up test|Forward-only migrations|Architectural-Constraint-ReversibleMigrations; R-007 HIGH-impact without reversibility|
|Key RTT mechanism|Dual-key grace window (pending OI-9 confirmation)|Hard cutover; JWKS with key list|Dual-key bounds R-010 to refresh TTL (7d) and preserves NA.2 during RTT|
|DM entity type convention|App-layer types in DM (string, Date, boolean, UUID-v4); DDL types confined to MIG-001/002|DDL types in DM entities|Base selection recommendation #3 — DM readers are backend engineers writing repository code; migration artifacts own the DDL contract|
|DTO field-exclusion enforcement|DTO-001 single source of truth with DM-003 AC referencing "DTO-001 WHT applies"|Duplicate blacklist in DM-003|Base selection recommendation #4 — one checkpoint avoids bypass by new developers while preserving traceability in DM-003 AC|

## Timeline Estimates

|MLS|Duration|Start|End|Key Milestones|
|---|---|---|---|---|
|M1|2 weeks|Week 1|Week 2|Migrations reversible in CI; 2048-bit RSA key + secrets manager live; feature flag declared off; repositories unit-tested|
|M2|2 weeks|Week 3|Week 4|PA1 cost=12 benchmarked within 200–350ms band; JWT RS256 with dual-key verification; TKN RTT + replay DTC green|
|M3|3 weeks|Week 5|Week 7|All five `/auth/*` NDP live behind flag; OI-3/4/5 path decisions landed; NTG tests + error contract proven|
|M4|2 weeks|Week 8|Week 9|NA.1/2/3 instrumented; APM, health (with DB/secrets/key-cache checks), PGR, k6, SEC-001 BNC all in place|
|M5|2 weeks|Week 10|Week 11|SC-1..SC-8 validated; SCR sign-off; staged flag-flip in prod; RLL rehearsed|

**Total estimated duration:** 11 weeks (Weeks 1–11).

