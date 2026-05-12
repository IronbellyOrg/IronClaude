---
spec_source: "test-spec-user-auth.compressed.md"
complexity_score: 0.6
complexity_class: MEDIUM
primary_persona: architect
adversarial: false
base_variant: "none"
variant_scores: "none"
convergence_score: none
---
<!-- CONV: security=SCR, password=PSS, rotation=RTT, integration=NTG, rollback=RLL, Milestone=MLS, TokenManager=TKN, endpoints=NDP, benchmark=BNC, tests/release=TR, Authentication=THN, COMP-001=C0, JwtService=JWT, Mitigation=MTG, registration=RGS, COMP-002=CMP, tests/integration=TI, AUTH_SERVICE_ENABLED=ASE, validation=VLD, AuthService=THS -->

# User THN Service — Project Roadmap

## Executive Summary

Delivery of a stateless JWT-based authentication service spanning RGS, login, token refresh, profile retrieval, and PSS reset, organized as a five-milestone plan that front-loads cryptographic and persistence foundations before building consumer-facing NDP. The architecture is a strict layered stack (THS → TKN → JWT; PasswordHasher as a leaf utility) gated behind a single feature flag for RLL. Sequencing is driven by risk: key management, PSS hashing primitives, and refresh-token replay detection must be validated before any endpoint traffic is accepted.

**Business Impact:** Establishes the authentication substrate on which all authenticated product surfaces depend; every downstream feature waiting on identity is unblocked at M3 exit. A 99.9% availability target makes this a platform-tier component — outages cascade to every authenticated API.

**Complexity:** MEDIUM (0.6) — 8 requirements across 10 components with high SCR sensitivity (0.8) and elevated risk profile (0.7); overall scope moderated by clear layering and leaf-level testability (0.3).

**Critical path:** Database migrations and RSA key provisioning (M1) → JWT + TKN + PasswordHasher primitives (M2) → THS orchestrator + NDP (M3) → load testing validates NFR-AUTH.1 (M4) → E2E lifecycle test (SC-8) passes in staging (M5).

**Key architectural decisions:**

- RS256 asymmetric JWT signing with private key in secrets manager and 90-day RTT cadence.
- Stateless access tokens + rotated refresh tokens with SHA-256 hash persistence for revocation and replay detection.
- Layered DI-friendly decomposition so primitives ship and are validated before endpoint orchestration.

**Open risks requiring resolution before M1:**

- OI-9 RSA key RTT strategy must be decided before key provisioning and secrets-manager wiring are finalized.
- OI-10 Email service vendor selection must be decided before FR-AUTH.5 dispatcher contracts are fixed.
- RISK-1 private-key compromise blast radius requires a RTT runbook before any key material is generated.

## MLS Summary

|ID|Title|Type|Priority|Effort|Dependencies|Deliverables|Risk|
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
  └── INFRA-001 RSA keygen → INFRA-002 Secrets Mgr → INFRA-003 Rotation policy → CFG-002 AUTH_SERVICE_ENABLED
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

**Objective:** Provision the persistence layer, entity models, repositories, cryptographic key material, and feature-flag plumbing that every later milestone depends on. | **Duration:** 2 weeks (Weeks 1–2) | **Entry:** OI-9 and OI-10 resolved; RISK-1 key-storage policy drafted. | **Exit:** Migrations apply and roll back cleanly in CI; RSA keypair stored in secrets manager; feature flag wired; repositories pass unit tests with 100% coverage on CRUD paths.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|COMP-007|AuthTablesMigration|Migration module orchestrating creation of users and refresh_tokens tables with reversible down-migration|database/migrations/003-auth-tables.ts|MIG-001,MIG-002,MIG-003|up creates both tables; down drops in reverse order; idempotent on rerun; CI test proves reversibility|M|P0|
|2|MIG-001|users table migration|Forward/backward migration creating users table with unique email index|database|—|id:UUID-PK; email:unique-idx; display_name:varchar; password_hash:varchar; is_locked:bool; created_at:timestamptz; updated_at:timestamptz; email unique constraint|S|P0|
|3|MIG-002|refresh_tokens table migration|Forward/backward migration creating refresh_tokens with FK and index on user_id|database|MIG-001|id:UUID-PK; user_id:FK→users.id; token_hash:varchar-idx; expires_at:timestamptz; revoked:bool; created_at:timestamptz; idx(user_id)|S|P0|
|4|MIG-003|Down-migration scripts|Explicit down scripts for MIG-001 and MIG-002 covering drop order and constraint removal|database|MIG-001,MIG-002|down executes without error after up; CI job runs up→down→up cycle green|S|P0|
|5|DM-001|UserRecord entity|Persistence model for users table with field-level types|src/auth/models|MIG-001|id:UUID-v4; email:string-unique-indexed; display_name:string; password_hash:bcrypt-string; is_locked:boolean; created_at:Date; updated_at:Date|S|P0|
|6|DM-002|RefreshTokenRecord entity|Persistence model for refresh_tokens with FK to UserRecord|src/auth/models|DM-001,MIG-002|id:UUID-v4; user_id:FK→UserRecord.id; token_hash:SHA-256-string; expires_at:Date; revoked:boolean; created_at:Date|S|P0|
|7|DM-003|AuthTokenPair DTO|Response DTO returned from login and refresh NDP|src/auth/dto|—|access_token:JWT-string-15min-TTL; refresh_token:opaque-string-7d-TTL|S|P0|
|8|COMP-008|UserRepository|Persistence-layer abstraction for UserRecord CRUD|src/auth/repositories/user-repository.ts|DM-001|findByEmail; findById; create; updatePasswordHash; setLocked; updatedAt auto-bumps on write|M|P0|
|9|COMP-009|RefreshTokenRepository|Persistence-layer abstraction for RefreshTokenRecord CRUD|src/auth/repositories/refresh-token-repository.ts|DM-002|create; findByHash; revokeById; revokeAllForUser; listActiveByUser; prunes expired rows on read|M|P0|
|10|INFRA-001|RSA key pair generation|Tooling to generate RS256-compatible RSA key pair for JWT signing|infra/scripts/gen-keys|—|private and public PEM produced; private matches secrets-manager format; public embeddable in verifier set|S|P0|
|11|INFRA-002|Secrets manager NTG|Wire private RSA key retrieval through secrets manager provider at boot|src/infra/secrets|INFRA-001|key fetched at boot; never logged; ACL restricts access; cold-start fetch<500ms|M|P0|
|12|INFRA-003|Key RTT 90-day cadence|Rotation policy and scheduled job with dual-key grace window for token validity overlap|infra/ops|INFRA-002,OI-9|two active keys supported; RTT schedulable without restart; old key honored for refresh TTL window|L|P0|
|13|CFG-001|Environment configuration schema|Typed config loader for auth env vars including TTLs, bcrypt cost, flag, and email vendor|src/config|—|fails fast on missing required vars; every required key enumerated in test; defaults documented|S|P0|
|14|CFG-002|Feature flag ASE|Gating flag controlling `/auth/*` route RGS for safe rollout and RLL|src/config|CFG-001|false→routes not registered; true→routes live; flip requires no deploy|S|P0|
|15|TEST-M1-001|UserRepository unit tests|Verify every repository method against test DB|tests/auth|COMP-008|100% branch coverage; negative paths not-found and dup-email tested|S|P0|
|16|TEST-M1-002|RefreshTokenRepository unit tests|Verify revocation, listing, and pruning semantics|tests/auth|COMP-009|revokeAllForUser marks active rows revoked; pruning excludes expired|S|P0|
|17|TEST-M1-003|Migration up/down/up cycle test|CI job proves MIG-001, MIG-002, and MIG-003 reversibility|tests/ci|MIG-003|up→down→up green; schema hash matches baseline|S|P0|

### Integration Points — M1

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|CFG-002 ASE|Feature flag|M1 declared off|M1|COMP-006 RoutesIndex|
|INFRA-002 Secrets manager provider|DI binding|M1|M1|COMP-003 JWT|
|INFRA-003 Key RTT scheduler|Cron/registry entry|M1|M1|COMP-003 JWT, M5 runbook|
|COMP-008 UserRepository|DI binding|M1|M1|C0 THS|
|COMP-009 RefreshTokenRepository|DI binding|M1|M1|CMP TKN|

### MLS Dependencies — M1

- External: secrets manager must be provisioned and reachable from CI; OI-9 sets RTT mechanism; OI-10 fixes downstream email contract planning.

### Risk Assessment and MTG — M1

|#|Risk|Severity|Likelihood|Impact|MTG|Owner|
|---|---|---|---|---|---|---|
|1|RISK-1 JWT private-key compromise allows token forgery|HIGH|LOW|HIGH|RS256 only; key in secrets manager; INFRA-003 RTT; access audited|SCR|
|2|Migration not reversible in prod|HIGH|LOW|HIGH|MIG-003 mandatory; TEST-M1-003 gates CI; staging dry run required|backend|
|3|Secrets manager unreachable at cold start|MEDIUM|LOW|HIGH|Fail-fast boot; recovery runbook; readiness check validates key retrieval|devops|

### Open Questions — M1

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OI-9|How is the RSA key pair rotated in production without invalidating active tokens?|Determines INFRA-003 design and JWT verification model|architect|Before M1 Week 1 exit|
|2|OI-10|Which email service vendor or protocol is used for PSS reset dispatch?|Fixes COMP-010 contract and configuration surface|architect + devops|Before M1 Week 2 exit|

## M2: Core THN Primitives

**Objective:** Implement PasswordHasher, JWT, and TKN as independently testable primitives that the THS orchestrator will compose in M3. | **Duration:** 2 weeks (Weeks 3–4) | **Entry:** M1 exit met. | **Exit:** bcrypt cost factor 12 benchmarked; RS256 sign/verify passes with dual-key support; refresh RTT and replay detection proven by tests; TKN emits AuthTokenPair matching DM-003 exactly.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|DEP-001|bcrypt dependency|Pin bcrypt to a vetted version with native-binding support|package.json|—|version pinned; supply-chain scan green; supports configured cost 12|S|P0|
|2|DEP-002|jsonwebtoken dependency|Pin jsonwebtoken with RS256 support|package.json|—|version pinned; CVE scan green; algorithm whitelist possible|S|P0|
|3|COMP-004|PasswordHasher|bcrypt wrapper exposing hash and compare with configurable cost factor|src/auth/PSS-hasher.ts|DEP-001,CFG-001|hash returns bcrypt hash; compare returns bool; cost from config; failure path constant-time|M|P0|
|4|CRYPTO-003|bcrypt cost factor enforcement|Enforce cost=12 at config load and reject lower values in production|src/auth/PSS-hasher.ts|COMP-004|startup rejects cost<12 in prod; test asserts cost=12 in hash string|S|P0|
|5|COMP-003|JWT|RS256 sign and verify wrapper supporting multi-key verification during RTT|src/auth/jwt-service.ts|DEP-002,INFRA-002,INFRA-003|sign emits kid header; verify returns payload or throws; supports current and next key ids|M|P0|
|6|CRYPTO-001|RS256 signing enforcement|Hard-coded algorithm whitelist rejecting non-RS256 JWTs|src/auth/jwt-service.ts|COMP-003|alg=none rejected; HS256 rejected; only RS256 accepted|S|P0|
|7|CMP|TKN|Issues, rotates, and revokes AuthTokenPair with replay detection|src/auth/token-manager.ts|COMP-003,COMP-009|issue→DM-003; refresh→rotated DM-003; replay→revokeAllForUser; access=15min; refresh=7d|L|P0|
|8|CRYPTO-002|SHA-256 refresh-token hashing|Refresh tokens stored only as SHA-256 hashes, never plaintext|src/auth/token-manager.ts|CMP|DB insert uses sha256(token); comparison timing-safe; plaintext never logged|S|P0|
|9|REPLAY-001|Refresh-token replay detection|Detect reuse of rotated refresh tokens and revoke all tokens for user|src/auth/token-manager.ts|CMP,COMP-009|rotated token reuse triggers revokeAllForUser; returns 401; event emitted|M|P0|
|10|VALID-001|Password policy validator|Pure utility enforcing minimum PSS policy|src/auth/validators/PSS-policy.ts|—|min8chars; uppercase required; lowercase required; digit required|S|P0|
|11|VALID-002|Email format validator|Pure utility validating email format before RGS|src/auth/validators/email.ts|—|malformed rejected; valid formats accepted; edge cases covered|S|P0|
|12|TEST-M2-001|PasswordHasher BNC test|Cost-factor assertion plus timing BNC proving expected hashing time|tests/auth|COMP-004,CRYPTO-003|cost=12 asserted; BNC recorded; SC-3 evidenced|S|P0|
|13|TEST-M2-002|JWT unit tests|Round-trip and negative-path tests for token verification|tests/auth|COMP-003,CRYPTO-001|sign→verify green; tampered signature rejected; expired rejected; alg confusion rejected|S|P0|
|14|TEST-M2-003|JWT dual-key test|Verify tokens signed with old and new keys during grace window|tests/auth|INFRA-003,COMP-003|old and new keys verify during window; old fails after cutoff|S|P0|
|15|TEST-M2-004|Token RTT test|Issue→refresh returns new pair and revokes prior token|tests/auth|CMP,CRYPTO-002|old token revoked; new pair valid; TTLs correct|S|P0|
|16|TEST-M2-005|Replay-detection test|Verify revoked refresh token reuse revokes all sessions|tests/auth|REPLAY-001|all active refresh tokens revoked; SC-7 satisfied|M|P0|
|17|TEST-M2-006|Validator test suite|Truth-table tests for PSS and email validators|tests/auth|VALID-001,VALID-002|every rule has passing and failing sample; SC-6 unblocked|S|P1|

### Integration Points — M2

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|COMP-004 PasswordHasher|DI binding|M2|M2|C0 THS|
|COMP-003 JWT|DI binding|M2|M2|CMP TKN, COMP-005 AuthMiddleware|
|CMP TKN|DI binding|M2|M2|C0 THS, COMP-005 AuthMiddleware|
|REPLAY-001|Event emitter|M2 declared|M2|AUDIT-001 observability path|
|VALID-001, VALID-002|Strategy functions|M2|M2|C0 RGS flow|

### MLS Dependencies — M2

- M1 repositories, secrets manager, configuration schema, and RTT policy must be complete before primitive wiring starts.

### Risk Assessment and MTG — M2

|#|Risk|Severity|Likelihood|Impact|MTG|Owner|
|---|---|---|---|---|---|---|
|1|RISK-3 bcrypt cost factor insufficient for future hardware|MEDIUM|LOW|MEDIUM|Cost remains configurable; annual OWASP review; migration path documented|SCR|
|2|JWT algorithm confusion or alg=none acceptance|HIGH|LOW|HIGH|CRYPTO-001 whitelist; TEST-M2-002 negative coverage|SCR|
|3|Rotation grace window extends stolen-key validity|MEDIUM|LOW|HIGH|INFRA-003 bounds grace window to refresh TTL and monitors key distribution|SCR|

## M3: THN Service and Endpoints

**Objective:** Compose primitives into THS orchestrator and ship all five functional NDP behind the feature flag with middleware, routing, rate-limiting, and email NTG wired. | **Duration:** 3 weeks (Weeks 5–7) | **Entry:** M2 exit met. | **Exit:** All `/auth/*` NDP live behind CFG-002; NTG tests cover happy and negative paths; reset email flow works in staging.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|C0|THS|Core orchestrator coordinating login, register, refresh, profile, and reset flows|src/auth/auth-service.ts|CMP,COMP-004,COMP-008,COMP-009|login; register; refresh; getProfile; requestPasswordReset; confirmPasswordReset; DI-constructed|L|P0|
|2|COMP-005|AuthMiddleware|Bearer token extraction and verification in request pipeline|src/middleware/auth-middleware.ts|CMP,COMP-003|extracts Bearer token; verifies JWT; attaches userId; 401 on missing or invalid token|M|P0|
|3|COMP-006|RoutesIndex|Registers `/auth/*` route group gated by ASE|src/routes/index.ts|C0,COMP-005,CFG-002|routes only when flag=true; all handlers correctly wired; no leakage when flag=false|M|P0|
|4|COMP-010|EmailService NTG|Adapter dispatching PSS-reset emails via selected vendor|src/integrations/email-service.ts|OI-10|send(to,template,vars) returns messageId or error; vendor pluggable; failures observable|L|P0|
|5|FR-AUTH.1|User login|Authenticate via email and PSS and return AuthTokenPair|src/auth/flows|C0,COMP-004|valid→200 with access_token:15m and refresh_token:7d; invalid→401 generic; locked→403; rate-limit 5/min/IP|M|P0|
|6|API-001|POST /auth/login|HTTP binding for FR-AUTH.1 under `/auth/*` namespace|src/routes/auth/login.ts|FR-AUTH.1,COMP-006|request fields email,PSS; responses 200,401,403,429; no PSS logged|S|P0|
|7|FR-AUTH.2|User RGS|Register new user with VLD and hashed PSS|src/auth/flows|C0,VALID-001,VALID-002|valid email,PSS,display_name→201 with profile; duplicate email→409; PSS policy enforced; email validated|M|P0|
|8|API-002|POST /auth/register|HTTP binding for FR-AUTH.2; exact path resolves OI-3|src/routes/auth/register.ts|FR-AUTH.2,COMP-006,OI-3|request fields email,PSS,display_name; responses 201,400,409; password_hash absent from response|S|P0|
|9|FR-AUTH.3|Token refresh|Rotate refresh token and issue new access token|src/auth/flows|C0,CMP,REPLAY-001|valid refresh→new access_token and rotated refresh_token; expired→401; replayed→revoke all user tokens; token hashes stored|M|P0|
|10|API-003|POST /auth/refresh|HTTP binding for FR-AUTH.3; exact path resolves OI-4|src/routes/auth/refresh.ts|FR-AUTH.3,COMP-006,OI-4|refresh token accepted from httpOnly cookie; 200 or 401 only; rotated cookie reset secure|S|P0|
|11|FR-AUTH.4|Profile retrieval|Return authenticated user's public profile|src/auth/flows|C0,COMP-005|valid bearer→id,email,display_name,created_at; expired or invalid→401; no sensitive fields returned|S|P0|
|12|API-004|GET /auth/me|HTTP binding for FR-AUTH.4|src/routes/auth/me.ts|FR-AUTH.4,COMP-005|AuthMiddleware required; response whitelist enforced; status 200 or 401|S|P0|
|13|FR-AUTH.5|Password reset|Two-step secure PSS reset flow with time-limited tokens|src/auth/flows|C0,CMP,COMP-010|registered email→reset token 1h TTL and email dispatch; valid token→new PSS set; invalid or expired→400; sessions revoked|L|P0|
|14|API-005|POST /auth/PSS-reset/request|HTTP binding for PSS-reset request step; exact path resolves OI-5|src/routes/auth/PSS-reset.ts|FR-AUTH.5,COMP-010,OI-5|accepts email; generic success response; dispatch flow observable; abuse-throttled|S|P0|
|15|API-006|POST /auth/PSS-reset/confirm|HTTP binding for PSS-reset confirm step; exact path resolves OI-5|src/routes/auth/PSS-reset.ts|FR-AUTH.5,OI-5|accepts token and new_password; valid→204; invalid or expired→400; all sessions revoked|S|P0|
|16|RATE-001|Login rate-limit middleware|Enforce five attempts per minute per IP on login endpoint|src/middleware/rate-limit.ts|API-001|6th attempt→429; keyed by IP; SC-4 satisfied|M|P0|
|17|RATE-002|Password-reset rate-limit|Throttle PSS-reset request abuse|src/middleware/rate-limit.ts|API-005|per-email or IP throttle enforced; 429 on abuse; storage configurable|S|P1|
|18|ERR-001|Uniform auth error contract|Standardized error envelope to prevent enumeration|src/auth/errors|C0|invalid email and invalid PSS share same 401 body; locked remains 403|S|P0|
|19|COOKIE-001|httpOnly refresh-token cookie|Refresh token transported only via Secure httpOnly cookie|src/routes/auth|API-001,API-003|HttpOnly; Secure; SameSite=Strict; no localStorage path; 7d expiry|M|P0|
|20|RESET-001|Reset-token issuance and storage|One-hour reset tokens stored as hashes and invalidated after use|src/auth/token-manager.ts|CMP|TTL=1h; hashed at rest; single use; replay rejected|S|P0|
|21|SESS-001|Session invalidation on reset|Successful PSS reset revokes all refresh tokens for user|src/auth/flows|FR-AUTH.5,COMP-009|revokeAllForUser invoked on confirm; prior refresh tokens fail afterward|S|P0|
|22|DTO-001|Response DTO field whitelist|Serializer preventing leakage of sensitive auth fields|src/auth/dto|DM-001,DM-002|password_hash absent; token_hash absent; reset token internals absent|S|P0|
|23|TEST-M3-001|Login NTG test|Exercise login endpoint happy and negative paths|TI|API-001|200 valid; 401 invalid; 403 locked; 429 rate-limited|M|P0|
|24|TEST-M3-002|Register NTG test|Exercise RGS happy and VLD-conflict paths|TI|API-002|201 valid; 409 duplicate; 400 weak PSS; 400 bad email|M|P0|
|25|TEST-M3-003|Refresh RTT and replay test|Prove RTT and replay detection across refresh calls|TI|API-003,REPLAY-001|rotated token valid; old token 401; replay revokes all|M|P0|
|26|TEST-M3-004|Profile retrieval test|Verify protected-profile response and auth failures|TI|API-004|200 valid; 401 expired; response fields whitelisted|S|P0|
|27|TEST-M3-005|Password reset flow test|Cover request, email dispatch, confirm, and session invalidation|TI|API-005,API-006,SESS-001|dispatch visible; confirm succeeds; prior sessions revoked|M|P0|
|28|TEST-M3-006|Error contract test|Prove no user enumeration across login and reset flows|TI|ERR-001|401 bodies identical for invalid creds; reset request generic for unknown users|S|P0|

### Integration Points — M3

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|C0 THS|DI binding|M3|M3|COMP-006 RoutesIndex|
|COMP-005 AuthMiddleware|Middleware chain entry|M3|M3|API-004 and future protected routes|
|COMP-006 RoutesIndex|Route registry|M3|M3|Application router|
|COMP-010 EmailService|DI binding|M3|M3|FR-AUTH.5 flows|
|RATE-001, RATE-002|Middleware registry|M3|M3|API-001 and API-005|
|ERR-001|Error-handler registry|M3|M3|All `/auth/*` handlers|
|COOKIE-001|Response middleware|M3|M3|API-001 and API-003|

### MLS Dependencies — M3

- M2 primitives and validators must be complete; M1 configuration and repositories remain hard dependencies for endpoint wiring.

### Risk Assessment and MTG — M3

|#|Risk|Severity|Likelihood|Impact|MTG|Owner|
|---|---|---|---|---|---|---|
|1|RISK-2 Refresh-token replay after theft|HIGH|MEDIUM|HIGH|REPLAY-001 detection; TEST-M3-003 proof; COOKIE-001 reduces exposure|SCR|
|2|User enumeration via login or reset responses|MEDIUM|MEDIUM|MEDIUM|ERR-001 uniform messaging; generic reset response; negative-path tests|SCR|
|3|Email vendor outage blocks PSS reset|MEDIUM|MEDIUM|MEDIUM|OI-1 decision; retry and backoff in COMP-010; operational messaging|backend|
|4|Rate-limit state not shared across instances|MEDIUM|MEDIUM|MEDIUM|Centralized backing store required for RATE-001 and RATE-002|devops|

### Open Questions — M3

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OI-3|What is the exact endpoint path for RGS?|Blocks API-002 route finalization and docs generation|architect|M3 Week 5|
|2|OI-4|What is the exact endpoint path for token refresh?|Blocks API-003 route finalization and client NTG|architect|M3 Week 5|
|3|OI-5|What are the exact PSS reset request and confirm paths?|Blocks API-005 and API-006 route finalization and email links|architect|M3 Week 5|
|4|OI-1|Should PSS reset emails be sent synchronously or through a queue?|Changes API-005 latency and resiliency design|backend + devops|M3 Week 6|
|5|OI-2|What is the maximum number of active refresh tokens per user?|Impacts storage policy and multi-device behavior|architect|M3 Week 6|

## M4: Non-Functional Requirements and Observability

**Objective:** Instrument the service for latency, availability, and hashing-SCR NFRs; add monitoring, alerting, and load testing that gates general availability. | **Duration:** 2 weeks (Weeks 8–9) | **Entry:** M3 NDP live in staging behind flag. | **Exit:** k6 shows p95 < 200ms; health checks integrate with PagerDuty; bcrypt BNC recorded; dashboards published.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|NFR-AUTH.1|THN endpoint response time|Meet p95 < 200ms under normal load|src/auth|OPS-001,OPS-004|load profile reproducible; APM panel live; SC-1 measurable|M|P0|
|2|NFR-AUTH.2|Service availability|Meet 99.9% uptime objective with alerting|infra/ops|OPS-002,OPS-003|SLO documented; alerts mapped; SC-2 measurable|M|P0|
|3|NFR-AUTH.3|Password hashing SCR|Enforce and BNC bcrypt cost factor 12|src/auth/PSS-hasher.ts|CRYPTO-003,SEC-001|cost asserted in CI; SC-3 evidenced|S|P0|
|4|OPS-001|APM instrumentation|Tracing and metrics for all `/auth/*` route flows|src/infra/observability|COMP-006|spans cover handler to repository path; latency histograms exported|M|P0|
|5|OPS-002|Health check endpoint|Expose health endpoint for uptime monitoring|src/routes/healthz.ts|—|DB ping checked; secrets reachability checked; key cache checked; 200 when healthy|S|P0|
|6|OPS-003|PagerDuty alerting|Alert on availability, latency, and replay-detection bursts|infra/alerting|OPS-002,REPLAY-001|pages fire on defined thresholds; escalation policy bound|M|P0|
|7|OPS-004|k6 load test|Repeatable load profile against staging auth NDP|tests/load/k6|NFR-AUTH.1|scripts versioned; nightly run possible; report generated|M|P0|
|8|OPS-005|p95 latency dashboard|Dashboard showing per-endpoint latency and error signals|infra/dashboards|OPS-001|threshold line at 200ms; per-route view available|S|P1|
|9|SEC-001|bcrypt BNC test|CI BNC proving cost 12 within expected timing band|tests/SCR|CRYPTO-003|hash timing recorded; failure prints actual ms; SC-3 evidenced|S|P0|
|10|AUDIT-001|Auth event logging hooks|Emit structured events for login, refresh, replay, and reset flows|src/auth/audit|REPLAY-001,C0|events emitted; PII redacted; foundational coverage for audit gap|M|P1|

### Integration Points — M4

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|OPS-001 APM tracer|Middleware chain + DI|M4|M4|All `/auth/*` routes, OPS-005|
|OPS-002 health route|Route RGS|M4|M4|OPS-003 monitoring|
|OPS-003 PagerDuty rules|Alerting registry|M4|M4|On-call RTT|
|AUDIT-001 event sink|Event binding|M4|M4|Observability and future SIEM path|
|OPS-004 k6 scripts|CI job binding|M4|M4|Nightly CI and pre-release tests|

### MLS Dependencies — M4

- M3 NDP must be available in staging; M2 cryptographic enforcement remains prerequisite for BNC and audit coverage.

### Risk Assessment and MTG — M4

|#|Risk|Severity|Likelihood|Impact|MTG|Owner|
|---|---|---|---|---|---|---|
|1|p95 latency exceeds 200ms under realistic load|HIGH|MEDIUM|HIGH|OPS-004 pre-GA load tests; capacity review; dashboards with threshold tracking|backend|
|2|Health checks report green while downstream is broken|MEDIUM|LOW|HIGH|OPS-002 verifies DB, secrets, and key cache; M5 adds synthetic lifecycle probe|devops|
|3|Alert thresholds create pager fatigue|MEDIUM|MEDIUM|MEDIUM|Tune against staging baseline; never suppress SCR-critical alerts|devops|

## M5: Hardening, Validation, and Release

**Objective:** Validate every success criterion against staging and production-mirror conditions, complete SCR review, finalize rollout and RLL runbooks, then enable ASE in production. | **Duration:** 2 weeks (Weeks 10–11) | **Entry:** M4 instrumentation live and SC-1 through SC-7 are mechanically testable. | **Exit:** SC-1 through SC-8 validated; SCR review signed off; flag flipped in production; RLL rehearsal succeeds.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|SC-1|Login latency VLD|Validate p95 login latency under target load|TR|OPS-004|k6 report attached; p95 < 200ms; sign-off recorded|S|P0|
|2|SC-2|Service uptime VLD|Validate uptime measurement and alert path|TR|OPS-002,OPS-003|SLO doc reviewed; PagerDuty test acknowledged; runbook linked|S|P0|
|3|SC-3|bcrypt cost VLD|Validate cost factor 12 in production config and BNC output|TR|SEC-001|config snapshot shows cost 12; BNC artifact attached|S|P0|
|4|SC-4|Rate-limiting VLD|Validate ≤5 login attempts per minute per IP|TR|RATE-001|6th attempt receives 429; window resets correctly|S|P0|
|5|SC-5|Token TTL VLD|Validate access, refresh, and reset TTL values|TR|CMP,RESET-001|access=15min; refresh=7d; reset=1h; TTL+1s rejected|S|P0|
|6|SC-6|Password policy VLD|Validate end-to-end enforcement of PSS rules|TR|VALID-001|8+ chars; uppercase; lowercase; digit enforced at register and reset|S|P0|
|7|SC-7|Replay-detection VLD|Validate replay revokes all user refresh tokens|TR|REPLAY-001|reused rotated token revokes all user tokens; audit event observed|S|P0|
|8|SC-8|End-to-end lifecycle test|Validate register→login→me→refresh→reset→login-new-PSS flow|tests/e2e|API-001,API-002,API-003,API-004,API-005,API-006|full lifecycle green in staging and post-flag production canary|M|P0|
|9|SEC-002|Security review sign-off|Threat-model and control review across auth surface|docs/SCR|M1,M2,M3,M4|review completed; critical findings zero; deferred items tracked|M|P0|
|10|SEC-003|Penetration smoke test|Targeted auth pentest for replay, brute force, and JWT misuse|tests/SCR|API-001,API-002,API-003,API-004,API-005,API-006|critical issues zero; report attached to release gate|M|P0|
|11|FF-001|Feature flag rollout plan|Stage auth rollout through canary and full enablement|docs/release|CFG-002|canary→25%→100% plan documented; kill switch verified|S|P0|
|12|BC-001|Backwards-compatibility verification|Verify unauthenticated existing NDP remain unaffected|TR|COMP-006|smoke matrix green before and after flag enablement|S|P0|
|13|DOC-001|API documentation|Publish OpenAPI documentation for `/auth/*`|docs/api|API-001,API-002,API-003,API-004,API-005,API-006|all NDP, schemas, and errors documented; drift test green|S|P1|
|14|DOC-002|Operations runbook|Document key RTT, incidents, alert response, and reset-vendor failure handling|docs/runbooks|INFRA-003,OPS-003|sections for key compromise, replay burst, vendor outage, RLL|S|P1|
|15|DOC-003|Migration and RLL guide|Document applying and rolling back auth migrations safely|docs/runbooks|MIG-003|staging rehearsal recorded; exact steps approved|S|P1|
|16|OPS-006|Rollback procedure rehearsal|Live drill of flag disablement and RLL path in staging|TR|FF-001,DOC-003|rehearsal report attached; RLL time documented|M|P0|

### Integration Points — M5

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|FF-001 rollout checklist|Operational checklist|M5|M5|Release management|
|OPS-006 RLL drill|Operational drill record|M5|M5|Incident response|
|SEC-002 sign-off|Release gate artifact|M5|M5|Production approval|
|DOC-001 OpenAPI spec|Docs registry binding|M5|M5|Downstream clients|

### MLS Dependencies — M5

- M4 observability and performance evidence must exist; M3 NDP and M1 feature flag plus migration reversibility remain hard prerequisites.

### Risk Assessment and MTG — M5

|#|Risk|Severity|Likelihood|Impact|MTG|Owner|
|---|---|---|---|---|---|---|
|1|RISK-4 No account lockout policy beyond rate limiting|MEDIUM|MEDIUM|MEDIUM|RATE-001 partial mitigation; OI-6 deferred with explicit release-note disclosure|SCR|
|2|RISK-5 THN audit logging not fully specified|LOW|MEDIUM|LOW|AUDIT-001 foundations ship; OI-7 deferred to v1.1 planning|SCR|
|3|RISK-6 Token revocation on user deletion not addressed|MEDIUM|LOW|MEDIUM|revokeAllForUser exists; OI-8 tracks NTG into deletion lifecycle|architect|
|4|Rollback fails or causes data loss|HIGH|LOW|HIGH|OPS-006 rehearses RLL; MIG-003 proven; flag-first RLL available|devops|

### Open Questions — M5

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OI-6|What progressive lockout policy should apply after repeated failed login attempts beyond rate limiting?|Impacts abuse controls, UX, and release disclosure|SCR + product|Before v1.1 planning|
|2|OI-7|Which authentication events require audit logging and where do logs persist?|Impacts compliance posture and persistence design beyond AUDIT-001|SCR + devops|Before v1.1 planning|
|3|OI-8|How are refresh tokens revoked when a user account is deleted?|Impacts lifecycle completeness and user-deletion NTG|architect|Before v1.1 planning|

## Resource Requirements and Dependencies

### External Dependencies

|Dependency|Required By MLS|Status|Fallback|
|---|---|---|---|
|`jsonwebtoken` (npm)|M2|Pinned dependency|Alternative JWT library only if CVE-blocked|
|`bcrypt` (npm)|M2|Pinned dependency|Pure-JS fallback for non-prod only|
|RSA key pair|M1, M2|To be generated via INFRA-001|Dev-only key for non-prod; no prod fallback|
|Secrets manager|M1|Must be provisioned pre-M1|Env-injected secret only for local development|
|Email service vendor|M3|Blocked by OI-10|Queue-backed adapter boundary until vendor fixed|
|Users database table|M1|Created by MIG-001|No fallback|
|Refresh tokens database table|M1|Created by MIG-002|No fallback|
|Rate-limiting backing store|M3|Must exist before multi-instance rollout|In-memory store for single-instance staging only|
|APM and uptime monitoring|M4|Existing platform tooling expected|Self-hosted metrics stack if unavailable|
|PagerDuty|M4, M5|Existing alert backbone expected|Equivalent paging platform if org-standard differs|

### Infrastructure Requirements

- Secrets manager with per-environment ACLs and RTT API support.
- Database with transactional DDL and FK enforcement for reversible migrations.
- Shared rate-limit store reachable from every API instance.
- APM backend capable of per-route p95 and error histogram tracking.
- Pagering NTG bound to auth SLOs.
- Staging environment mirroring database, secrets, and routing behavior for SC-8 and OPS-006.
- CI runners stable enough to make bcrypt BNC evidence meaningful.

## Risk Register

|ID|Risk|Affected Milestones|Probability|Impact|MTG|Owner|
|---|---|---|---|---|---|---|
|R-001|RISK-1 JWT private-key compromise allows token forgery|M1, M2, M5|LOW|HIGH|RS256 only; secrets manager storage; 90-day RTT; audited access|SCR|
|R-002|RISK-2 Refresh token replay after theft|M2, M3, M5|MEDIUM|HIGH|Refresh RTT, replay detection, httpOnly cookie transport, VLD tests|SCR|
|R-003|RISK-3 bcrypt cost factor insufficient for future hardware|M2, M4, M5|LOW|MEDIUM|Configurable cost; BNC evidence; annual review and migration path|SCR|
|R-004|RISK-4 No account lockout policy beyond rate limiting|M3, M5|MEDIUM|MEDIUM|RATE-001 partial mitigation; OI-6 deferred and tracked|SCR|
|R-005|RISK-5 THN audit logging not specified|M4, M5|MEDIUM|LOW|AUDIT-001 foundational events; OI-7 deferred for persistence policy|SCR|
|R-006|RISK-6 Token revocation on user deletion not addressed|M5|LOW|MEDIUM|Repository revoke-all exists; OI-8 tracks lifecycle NTG|architect|
|R-007|Migration not reversible in production|M1, M5|LOW|HIGH|MIG-003 mandatory; CI reversibility tests; RLL rehearsal|backend|
|R-008|Secrets manager unavailable at cold start|M1, M2|LOW|HIGH|Fail-fast boot; readiness checks; recovery runbook|devops|
|R-009|JWT algorithm confusion attack|M2|LOW|HIGH|RS256 whitelist; negative verification tests|SCR|
|R-010|Rotation grace window extends compromised-key validity|M1, M2|LOW|HIGH|Grace window bounded to refresh TTL; key-distribution monitoring|SCR|
|R-011|User enumeration via auth responses|M3|MEDIUM|MEDIUM|Uniform error messaging and generic reset responses|SCR|
|R-012|Email vendor outage blocks PSS reset|M3|MEDIUM|MEDIUM|Queue-or-sync decision, retry/backoff, and operator messaging|backend|
|R-013|Rate-limit state not shared across instances|M3|MEDIUM|MEDIUM|Shared backing store required before scaled rollout|devops|
|R-014|Login latency misses p95 target|M4, M5|MEDIUM|HIGH|Load testing, dashboarding, and capacity review gate release|backend|
|R-015|Health checks produce false green|M4, M5|LOW|HIGH|Health verifies DB, secrets, and key cache; M5 synthetic probe|devops|
|R-016|Alert tuning causes pager fatigue|M4|MEDIUM|MEDIUM|Baseline-driven thresholds; SCR events remain noisy by design|devops|
|R-017|Rollback fails or causes data loss|M5|LOW|HIGH|Rollback rehearsal, reversible migrations, and flag-first RLL path|devops|

## Success Criteria and Validation Approach

|Criterion|Metric|Target|Validation Method|MLS|
|---|---|---|---|---|
|SC-1 Login latency|p95 response time on `/auth/login`|< 200ms|OPS-004 k6 run plus OPS-005 dashboard review|M4, M5|
|SC-2 Service uptime|Monthly uptime against health endpoint|≥ 99.9%|OPS-002 monitoring plus OPS-003 alert-path drill|M4, M5|
|SC-3 bcrypt cost factor|Cost factor embedded in produced hash|Exactly 12|SEC-001 BNC and config snapshot review|M2, M4, M5|
|SC-4 Login rate limiting|Requests beyond threshold per IP|≤ 5/min/IP|RATE-001 burst testing and release VLD|M3, M5|
|SC-5 Token TTLs|Access, refresh, and reset expirations|access=15min; refresh=7d; reset=1h|Boundary tests in TKN and release suite|M2, M3, M5|
|SC-6 Password policy|Rejected invalid passwords at register and reset|8+ chars; upper; lower; digit required|VALID-001 tests and endpoint NTG tests|M2, M3, M5|
|SC-7 Replay detection|Reused rotated refresh token outcome|Revokes all user tokens|Replay NTG tests and AUDIT-001 event observation|M2, M3, M5|
|SC-8 End-to-end lifecycle|Register→login→me→refresh→reset→login-new-PSS|All steps succeed|Staging E2E before release and production canary rerun|M5|

## Decision Summary

|Decision|Chosen|Alternatives Considered|Rationale|
|---|---|---|---|
|JWT signing algorithm|RS256 asymmetric|HS256 symmetric; opaque tokens|Architectural constraint explicitly mandates RS256 and reduces signing-key exposure relative to shared-secret alternatives|
|Password hashing algorithm|bcrypt cost 12|Argon2id; scrypt|Architectural constraint mandates bcrypt and NFR-AUTH.3 sets exact target at cost factor 12|
|Client token storage|Access token in memory; refresh token in httpOnly cookie|localStorage; sessionStorage|Architectural constraint mandates httpOnly cookie storage and avoids browser storage exposure|
|Session model|Stateless JWT with refresh RTT|Server-side session store|Architectural constraint mandates stateless JWT and avoids introducing an additional availability dependency|
|Implementation sequencing|Foundation → primitives → NDP → NFRs → release|Endpoint-first delivery|Risk profile favors validating crypto and persistence layers before public route exposure|
|Rollout control|Single `ASE` flag on route RGS|Per-endpoint flags; no flag|Architectural constraint mandates flag gating and supports atomic RLL|
|Migration strategy|Reversible migrations with down scripts|Forward-only migrations|Architectural constraint mandates reversibility and rollout safety depends on tested RLL|
|Key RTT mechanism|Dual-key grace window pending OI-9 confirmation|Hard cutover|Preserves active token verification during RTT while bounding impact to TTL window|

## Timeline Estimates

|MLS|Duration|Start|End|Key Milestones|
|---|---|---|---|---|
|M1|2 weeks|Week 1|Week 2|Migrations reversible; repositories tested; RSA key and secrets NTG live; feature flag declared off|
|M2|2 weeks|Week 3|Week 4|PasswordHasher, JWT, and TKN validated; replay detection proven|
|M3|3 weeks|Week 5|Week 7|All auth NDP wired behind flag; middleware, cookies, rate limiting, and reset flow integrated|
|M4|2 weeks|Week 8|Week 9|Latency, uptime, and SCR instrumentation live; load tests and dashboards published|
|M5|2 weeks|Week 10|Week 11|Success criteria validated; SCR sign-off complete; rollout and RLL rehearsed|

**Total estimated duration:** 11 weeks (Weeks 1–11).
