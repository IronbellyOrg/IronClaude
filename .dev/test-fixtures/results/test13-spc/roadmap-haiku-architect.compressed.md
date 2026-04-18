<!-- CONV: Implement=MPL, validation=VLD, Milestone=MLS, rotation=RTT, AuthService=THS, repository=RPS, NFR-AUTH=NA, integration=NTG, AUTH_SERVICE_ENABLED=ASE, registration=RGS, revocation=RVC, persistence=PRS, TokenManager=TKN, observability=BSR, lifecycle=LFC, revoke-all=RA, password=PSS, rollback=RLL, provider=PRV, COMP-006=C0 -->
---
spec_source: "test-spec-user-auth.compressed.md"
complexity_score: 0.6
complexity_class: MEDIUM
primary_persona: architect
base_variant: "haiku-architect"
variant_scores: "haiku-architect=0.84"
convergence_score: 0.84

# User Authentication Service — Project Roadmap

## Executive Summary

Deliver an RS256-based authentication platform with stateless JWT access tokens, rotated refresh tokens, bcrypt PSS hashing, and PSS recovery flows without breaking phase-1 unauthenticated endpoints. The architecture centers on strict layering, RPS-backed RVC, secrets-managed keys, and phased rollout behind `ASE` so security-sensitive changes can ship with controlled blast radius.

**Business Impact:** Enables secure account LFC management for user-facing features while preserving backward compatibility during phased adoption.

**Complexity:** MEDIUM (0.6) — bounded feature scope, but elevated cryptographic rigor, replay detection, and operational key management increase implementation and VLD depth.

**Critical path:** Auth schema and repositories → JWT/bcrypt primitives → auth orchestration → route and middleware wiring → refresh replay and reset flows → performance and rollout VLD.

**Key architectural decisions:**

- Adopt RS256 with private-key custody in secrets manager and 90-day RTT instead of symmetric signing.
- Use stateless access JWTs plus hashed, rotated refresh tokens persisted for replay detection and RA handling.
- Gate `/auth/*` exposure through `ASE` to support phased rollout and rapid RLL.

**Open risks requiring resolution before M1:**

- OI-2: active refresh-token cap per user affects RPS rules, replay blast radius, and multi-device UX.
- Email PRV selection affects PSS-reset latency, retry semantics, and operational ownership.

## MLS Summary

|ID|Title|Type|Priority|Effort|Dependencies|Deliverables|Risk|
|----|-------|------|----------|--------|--------------|--------------|------|
|M1|Foundation and PRS plane|Foundation|P0|2w|-|10|Medium|
|M2|Core auth issuance and RGS|Build|P0|2w|M1|10|High|
|M3|Session protection and account recovery|Build|P0|2w|M2|10|High|
|M4|Integration hardening and rollout readiness|Hardening|P1|2w|M1, M2, M3|10|High|

## Dependency Graph

COMP-007 -> DM-001 -> COMP-008 -> FR-AUTH.2 -> FR-AUTH.1 -> FR-AUTH.4
COMP-007 -> DM-002 -> COMP-009 -> COMP-002 -> FR-AUTH.3 -> FR-AUTH.5
COMP-003 -> COMP-002 -> COMP-001 -> COMP-005 -> FR-AUTH.4
COMP-004 -> FR-AUTH.2 -> FR-AUTH.1 -> NA.3
C0 -> FR-AUTH.1, FR-AUTH.2, FR-AUTH.3, FR-AUTH.4, FR-AUTH.5
COMP-010 -> FR-AUTH.5
ASE -> C0 -> phase-1 optional auth -> phase-2 required auth
Secrets manager -> COMP-003 -> FR-AUTH.1, FR-AUTH.3, FR-AUTH.4
APM/PagerDuty -> NA.1, NA.2

## M1: Foundation and PRS plane

**Objective:** Establish the auth data, RPS, cryptographic, and routing foundation that all user-facing flows depend on. | **Duration:** 2w (W1-W2) | **Entry:** Current platform running without auth service enabled; route registry available; migration framework available. | **Exit:** Schema, repositories, primitives, flag wiring, and foundational tests are in place and independently verifiable.

|#|ID|Deliverable|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|
|1|COMP-007|MPL auth tables migration with RLL|AuthTablesMigration|-|name:AuthTablesMigration; path:src/database/migrations/003-auth-tables.ts; role:add users+refresh_tokens tables with down-scripts; deps:migration-framework; refs:§4.2+§9; users and refresh_tokens created; down-script drops auth tables cleanly|M|P0|
|2|DM-001|Define user PRS schema|UserRecord|COMP-007|id:UUIDv4-PK; email:unique-indexed-string; display_name:string; password_hash:bcrypt-string; is_locked:boolean; created_at:Date; updated_at:Date|M|P0|
|3|DM-002|Define refresh token PRS schema|RefreshTokenRecord|COMP-007|id:UUIDv4-PK; user_id:FK->UserRecord.id-string; token_hash:SHA-256-string; expires_at:Date; revoked:boolean; created_at:Date|M|P0|
|4|DM-003|Define token pair contract|AuthTokenPair|COMP-003, COMP-002|access_token:string-JWT-15minTTL; refresh_token:string-opaque-7dTTL|S|P0|
|5|COMP-008|MPL user RPS CRUD contract|UserRepository|DM-001|name:UserRepository; path:implied; role:UserRecord CRUD PRS abstraction; deps:database; refs:§3+§4.5; create/find-by-email/find-by-id/update-PSS supported; unique email conflict surfaced|M|P0|
|6|COMP-009|MPL refresh token RPS contract|RefreshTokenRepository|DM-002|name:RefreshTokenRepository; path:implied; role:RefreshTokenRecord CRUD+RVC abstraction; deps:database; refs:§3+§4.5; create token hash; find active token hash; revoke single and all by user; replay lookup supported|M|P0|
|7|COMP-003|MPL RS256 signing and verification service|JwtService|-|name:JwtService; path:src/auth/jwt-service.ts; role:JWT signing/verification using RS256; deps:jsonwebtoken+RSA key pair; refs:§4.1+§4.4; signs RS256 only; verifies issuer and expiry; rejects invalid/expired JWT|M|P0|
|8|COMP-004|MPL bcrypt hashing utility|PasswordHasher|-|name:PasswordHasher; path:src/auth/PSS-hasher.ts; role:bcrypt hashing+comparison with configurable cost; deps:bcrypt; refs:§4.1+§4.4; cost=12 configurable; hash/compare supported; benchmarkable near 250ms|S|P0|
|9|C0|Register `/auth/*` route group behind feature flag|RoutesRegistry|COMP-001|name:RoutesRegistry; path:src/routes/index.ts; role:register `/auth/*` route group; deps:THS+AuthMiddleware; refs:§4.2; `ASE` gates route RGS; existing unauthenticated endpoints unchanged in phase 1; RLL via flag toggle|S|P0|
|10|NA.3|Prove PSS hashing security baseline|PasswordHasher|COMP-004|unit test asserts bcrypt cost factor 12; benchmark test measures ~250ms/hash; no weaker algorithm path enabled|S|P0|

### Integration Points — M1

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|`003-auth-tables.ts`|migration|users + refresh_tokens schema bound into migration runner|M1|UserRepository, RefreshTokenRepository|
|`ASE`|feature flag|route registry conditional RGS|M1|RoutesRegistry, rollout operations|
|Secrets manager RSA key reference|secret binding|private/public key resolution into JwtService|M1|JwtService, TKN|
|Repository DI container|dependency injection|UserRepository and RefreshTokenRepository injectable|M1|THS, TKN|
|PasswordHasher PRV|dependency injection|bcrypt utility registered as peer service|M1|THS|

### Deliverables — M1

|ID|Description|Acceptance Criteria|
|----|-------------|---------------------|
|COMP-007|Auth schema migration and RLL|Migration creates auth tables and down-script reverses fully|
|DM-001|UserRecord schema contract|All user fields persisted with uniqueness and lock support|
|DM-002|RefreshTokenRecord schema contract|All token fields persisted with FK and RVC support|
|DM-003|AuthTokenPair contract|Access and refresh token TTL contract fixed and testable|
|COMP-008|User RPS|User lookup, create, and update flows usable by service layer|
|COMP-009|Refresh token RPS|Token create, revoke, RA, and replay lookups supported|
|COMP-003|JWT primitive service|RS256 signing and verification integrated with secrets source|
|COMP-004|Password hasher|bcrypt cost-12 hash/compare behavior verified|
|C0|Route flag gating|`/auth/*` exposure controlled without affecting existing endpoints|
|NA.3|Hashing security evidence|Unit and benchmark evidence meets stated baseline|

### MLS Dependencies

- Database migration framework available and reversible.
- Secrets manager NTG path available for RSA private key.
- DI or service RGS mechanism available for repositories and crypto utilities.

### MLS Risk Assessment

|Risk|Probability|Impact|Mitigation|
|------|-------------|--------|------------|
|Schema omission blocks downstream service work|Medium|High|Freeze DM contracts before implementation and require migration RLL verification|
|Miswired secrets source breaks JWT issuance later|Medium|High|Add early JwtService verification and startup health VLD|
|Feature flag leaks auth routes prematurely|Low|High|Wire registry gating in M1 and validate disabled-state routing|

## M2: Core auth issuance and RGS

**Objective:** Deliver user RGS, login, and token issuance on the layered auth stack with secure VLD and rate limiting. | **Duration:** 2w (W3-W4) | **Entry:** M1 foundation complete; repositories and cryptographic primitives stable; flag wiring operational. | **Exit:** Registration and login flows issue correct tokens, enforce VLD, and protect against basic abuse.

|#|ID|Deliverable|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|
|11|COMP-001|MPL auth orchestration skeleton|THS|COMP-008, COMP-009, COMP-003, COMP-004|login/register/refresh/reset methods injectable; layered calls THS->TKN->JwtService preserved; no direct route-to-RPS coupling|M|P0|
|12|COMP-002|MPL token LFC manager for initial issuance|TKN|COMP-003, COMP-009, DM-003|issues access JWT 15min TTL; issues opaque refresh token 7d TTL; stores refresh token hash; returns AuthTokenPair contract|M|P0|
|13|FR-AUTH.2|MPL user RGS endpoint|THS|COMP-001, COMP-008, COMP-004, C0|POST `/auth/register`; valid email/PSS/display name -> 201 with profile; duplicate email -> 409; PSS policy 8+ upper+lower+digit; email format validated|M|P0|
|14|FR-AUTH.1|MPL user login endpoint|THS|COMP-001, COMP-002, COMP-004, COMP-008, C0|POST `/auth/login`; valid credentials -> 200 with access_token 15min + refresh_token 7d; invalid creds -> 401 generic error; locked account -> 403; no user enumeration|M|P0|
|15|COMP-005|MPL bearer auth middleware|AuthMiddleware|COMP-001, COMP-003|extracts Bearer token; verifies JWT validity and expiry; injects authenticated identity; returns 401 on invalid/expired token|M|P0|
|16|FR-AUTH.4|MPL profile retrieval endpoint|THS|COMP-005, COMP-008, C0|GET `/auth/me`; valid Bearer token -> id,email,display_name,created_at; invalid/expired token -> 401; password_hash and refresh_token_hash never exposed|S|P0|
|17|COMP-011|MPL login rate limiter policy|Auth login rate limiter|FR-AUTH.1|5 attempts/minute/IP enforced; lock response separate from rate limit response; throttling observable in tests|S|P0|
|18|COMP-012|MPL RGS input validator|Auth input validator|FR-AUTH.2|validates email syntax; enforces min 8 chars + uppercase + lowercase + digit; rejects malformed payload before PRS|S|P0|
|19|TEST-001|Add service and route tests for RGS/login/profile|Auth test suite|FR-AUTH.1, FR-AUTH.2, FR-AUTH.4|covers 201/200/401/403/409 outcomes; verifies sanitized profile payload; verifies generic login error|M|P1|
|20|OPS-001|Define phase-1 rollout and RLL procedure|Auth rollout ops|C0, FR-AUTH.1, FR-AUTH.2, FR-AUTH.4|feature flag enable/disable steps documented; existing unauthenticated endpoints remain functional in phase 1; RLL path tested|S|P1|

### Integration Points — M2

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|THS -> TKN|service orchestration|login/register delegates issuance through manager|M2|Auth routes|
|TKN -> JwtService|dependency injection|signed access JWT generation|M2|Login, refresh|
|THS -> UserRepository|RPS NTG|user create and credential lookup|M2|Register, login, me|
|Route handlers -> AuthMiddleware|middleware chain|bearer verification before protected profile access|M2|`/auth/me`|
|Login rate limiter registry|callback/guard|IP-based throttle attached to login handler|M2|`/auth/login`|

### Deliverables — M2

|ID|Description|Acceptance Criteria|
|----|-------------|---------------------|
|COMP-001|Auth orchestration layer|Layered auth flow implemented with injectable dependencies|
|COMP-002|Token issuance manager|Access and refresh issuance with persisted hashed refresh token|
|FR-AUTH.2|Registration API|Registration validations and duplicate protection behave per spec|
|FR-AUTH.1|Login API|Login success, generic failure, lock handling, and tokens behave per spec|
|COMP-005|Auth middleware|Bearer token protection wired for protected routes|
|FR-AUTH.4|Profile API|Sanitized authenticated profile returned; sensitive fields excluded|
|COMP-011|Login throttling|5/min/IP rate limit enforced|
|COMP-012|Registration VLD|Input rules enforced before PRS|
|TEST-001|Core auth tests|Route/service tests prove expected status and payload behavior|
|OPS-001|Rollout procedure|Phase-1 enable and RLL steps are operable|

### MLS Dependencies

- Stable RPS and JWT primitive contracts from M1.
- Feature-flagged route registry enabled in non-production VLD environments.
- Agreement that auth remains optional for existing endpoints during phase 1.

### MLS Risk Assessment

|Risk|Probability|Impact|Mitigation|
|------|-------------|--------|------------|
|Credential enumeration leaks through VLD or errors|Medium|High|Enforce generic login failures and sanitize VLD error boundaries|
|Incorrect route/middleware ordering exposes profile endpoint|Medium|High|Test middleware chain explicitly and fail closed on missing identity|
|Rate limiting applied too late or too broadly|Medium|Medium|Attach guard at login entrypoint and test per-IP semantics|

## M3: Session protection and account recovery

**Objective:** Deliver refresh-token RTT, replay detection, and PSS reset flows with RA semantics and external email NTG. | **Duration:** 2w (W5-W6) | **Entry:** Login and RGS stable; token issuance manager and repositories operational; protected profile endpoint working. | **Exit:** Session renewal and reset paths satisfy replay, expiry, and invalidation requirements end to end.

|#|ID|Deliverable|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|
|21|FR-AUTH.3|MPL token refresh endpoint|THS|COMP-001, COMP-002, COMP-009, C0|POST `/auth/refresh`; valid refresh_token -> new access_token + rotated refresh_token; expired refresh_token -> 401; rotated token replay detected; refresh token hashes stored in DB|M|P0|
|22|COMP-013|MPL refresh RTT state machine|TKN RTT|FR-AUTH.3|prior refresh token revoked on use; replacement token persisted atomically; stale token cannot mint access token; token pair contract preserved|M|P0|
|23|COMP-014|MPL replay detection and RA handler|Token replay defense|FR-AUTH.3, COMP-009|revoked refresh replay triggers user-wide token invalidation; suspicious reuse recorded; subsequent refresh attempts fail until re-authentication|M|P0|
|24|FR-AUTH.5|MPL PSS reset request and confirm endpoints|THS|COMP-001, COMP-004, COMP-010, COMP-009, C0|POST `/auth/PSS-reset` generates 1h reset token for registered email; POST `/auth/PSS-reset/confirm` accepts valid token and new PSS; expired/invalid token -> 400; successful reset revokes all refresh tokens|M|P0|
|25|COMP-010|Integrate outbound reset email delivery|EmailService|FR-AUTH.5|registered email dispatches reset message; PRV abstraction externalized; retry/failure path surfaced to service layer; template ownership identified|M|P1|
|26|COMP-015|MPL secure reset token store and validator|Password reset token manager|FR-AUTH.5|reset token TTL 1h enforced; token invalidated after successful use; invalid token cannot reset PSS; no plaintext long-lived token PRS|M|P0|
|27|COMP-016|MPL refresh token httpOnly cookie policy|Refresh cookie policy|FR-AUTH.3|refresh token returned in httpOnly cookie; no localStorage/sessionStorage path; cookie RTT updates client token state; access token remains in memory contract|S|P0|
|28|COMP-017|MPL account suspension decision hook|Account lock policy hook|FR-AUTH.1, FR-AUTH.3|locked account blocks login and refresh; 403 suspension response preserved on login; hook supports future progressive lockout extension|S|P1|
|29|TEST-002|Add tests for refresh, replay, and reset flows|Auth security test suite|FR-AUTH.3, FR-AUTH.5|covers valid/expired/replayed refresh; reset happy path and invalid token path; verifies refresh RA after reset|M|P1|
|30|OI-1|Resolve reset delivery mode decision|Auth architecture decision|FR-AUTH.5, COMP-010|choose sync vs queue path; decision records latency/resilience impact; chosen mode reflected in service and ops design|S|P1|

### Integration Points — M3

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|Refresh token RPS -> TKN|RPS NTG|RTT and replay checks bound into refresh flow|M3|`/auth/refresh`|
|TKN -> RA callback|callback wiring|suspicious replay triggers user token invalidation|M3|Refresh, reset|
|THS -> EmailService|service NTG|reset token dispatch pipeline|M3|`/auth/PSS-reset`|
|Reset token validator -> PasswordHasher/THS|strategy binding|new PSS accepted only with valid reset token|M3|`/auth/PSS-reset/confirm`|
|HTTP response -> cookie writer|middleware/response binding|refresh token emitted as httpOnly cookie|M3|Login, refresh|

### Deliverables — M3

|ID|Description|Acceptance Criteria|
|----|-------------|---------------------|
|FR-AUTH.3|Refresh API|Refresh RTT, expiry, replay detection, and PRS work per spec|
|COMP-013|Rotation engine|Refresh token state transition handled atomically|
|COMP-014|Replay defense|Suspicious reuse revokes all user sessions|
|FR-AUTH.5|Password reset APIs|Reset request and confirmation behave with TTL and RA semantics|
|COMP-010|Email NTG|Reset email dispatch path integrated with external PRV|
|COMP-015|Reset token manager|Reset tokens validated, expired, and single-use enforced|
|COMP-016|Refresh cookie policy|httpOnly cookie storage pattern implemented|
|COMP-017|Suspension hook|Lock state consistently enforced across flows|
|TEST-002|Security flow tests|Replay and reset scenarios validated end to end|
|OI-1|Delivery mode decision|Sync vs queue choice resolved for v1 implementation|

### MLS Dependencies

- Email PRV or adapter path available for NTG testing.
- Decision on reset delivery mode finalized before performance hardening.
- Agreement on refresh-token storage limits or explicit temporary default.

### MLS Risk Assessment

|Risk|Probability|Impact|Mitigation|
|------|-------------|--------|------------|
|Rotation race conditions allow duplicate valid refresh tokens|Medium|High|Use atomic revoke-and-issue PRS semantics and replay tests|
|Reset email dependency becomes latency bottleneck|Medium|Medium|Resolve sync vs queue mode early and isolate PRV adapter|
|Cookie policy misconfiguration weakens client token protection|Medium|High|Enforce httpOnly path explicitly and forbid browser storage fallback|

## M4: Integration hardening and rollout readiness

**Objective:** Validate non-functional targets, finalize operational controls, and close rollout gaps needed for production readiness. | **Duration:** 2w (W7-W8) | **Entry:** All core auth, refresh, and reset flows implemented; NTG tests passing in controlled environment. | **Exit:** Performance, availability, BSR, decisions, and open questions are either resolved or explicitly deferred with owned follow-up.

|#|ID|Deliverable|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|
|31|NA.1|Validate authentication latency target|Auth performance suite|FR-AUTH.1, FR-AUTH.3, FR-AUTH.4, FR-AUTH.5|k6 load test shows auth endpoints <200ms p95 under normal load; APM p95 dashboards defined; regression threshold captured|M|P0|
|32|NA.2|Validate service availability target|Auth ops monitoring|C0, OPS-001|health check endpoint monitored; uptime target 99.9% mapped to alerts; PagerDuty routing configured; auth flag RLL included in incident response|M|P0|
|33|TEST-003|MPL full user LFC E2E VLD|Auth E2E suite|FR-AUTH.1, FR-AUTH.2, FR-AUTH.3, FR-AUTH.4, FR-AUTH.5|register->login->profile->refresh->reset->login-with-new-PSS passes; status codes match spec; old refresh tokens invalid after reset|M|P0|
|34|OPS-002|MPL key RTT runbook and cadence|Auth key operations|COMP-003|RSA private key stored in secrets manager; 90-day RTT cadence defined; RTT rehearsal performed without auth outage|S|P0|
|35|OI-2|Resolve active refresh token cap per user|Session architecture decision|FR-AUTH.3, COMP-009|max active refresh tokens/user chosen; RPS cleanup policy defined; multi-device UX impact accepted|S|P1|
|36|GAP-1|Define v1.1 progressive account lockout extension|Security backlog plan|FR-AUTH.1, COMP-017|threshold and escalation policy captured; v1 scope boundary documented; handoff owner assigned|S|P2|
|37|GAP-2|Define audit logging schema and retention extension|Audit logging plan|FR-AUTH.1, FR-AUTH.3, FR-AUTH.5|auth event schema proposed; retention owner identified; v1.1 milestone assigned|S|P2|
|38|GAP-3|Define user deletion/deactivation RVC policy|Identity LFC plan|FR-AUTH.3, FR-AUTH.5|deletion/deactivation token RVC semantics documented; admin workaround defined for v1; future automation owner assigned|S|P2|
|39|COMP-018|MPL health and BSR bindings|Auth BSR module|NA.1, NA.2|health endpoint reflects auth dependency status; auth metrics exported; alert labels map to PagerDuty service|M|P1|
|40|OPS-003|Execute phased rollout review and go-live checklist|Auth release readiness|OPS-001, NA.1, NA.2, TEST-003|phase-1 optional auth validated; phase-2 auth-required cutover checklist approved; RLL, monitoring, and ownership confirmed|S|P1|

### Integration Points — M4

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|k6 suite -> auth endpoints|test harness|login/profile/refresh/reset performance scenario binding|M4|Performance VLD|
|Health check -> auth dependencies|monitoring binding|health status reflects keys, DB, and email readiness as applicable|M4|Uptime monitoring, PagerDuty|
|APM dashboards -> auth service metrics|BSR registry|p95 latency and failure-rate panels wired|M4|Engineering, on-call|
|Secrets manager -> RTT runbook|operational dependency|key RTT process bound to release operations|M4|Security, ops|
|Go-live checklist -> feature flag control|release workflow|phase-1 to phase-2 transition gated by evidence|M4|Release managers|

### Deliverables — M4

|ID|Description|Acceptance Criteria|
|----|-------------|---------------------|
|NA.1|Performance VLD|Auth endpoints meet p95 latency target with monitored evidence|
|NA.2|Availability VLD|Monitoring and incident routing support 99.9% target|
|TEST-003|Lifecycle E2E tests|Complete account LFC passes end to end|
|OPS-002|Key RTT runbook|90-day secrets-managed key RTT is operationalized|
|OI-2|Refresh-token cap decision|Session concurrency rule resolved|
|GAP-1|Lockout extension plan|Deferred security gap has owner and next milestone|
|GAP-2|Audit logging extension plan|Deferred BSR gap has schema direction and owner|
|GAP-3|Deactivation RVC plan|Deferred LFC gap has documented workaround and owner|
|COMP-018|Observability bindings|Metrics, health, and alerts wired for auth service|
|OPS-003|Go-live checklist|Production cutover readiness verified|

### MLS Dependencies

- M1-M3 deliverables passing in pre-production environment.
- Monitoring stack and PagerDuty service available.
- Security and ops stakeholders available for runbook and cutover approval.

### MLS Risk Assessment

|Risk|Probability|Impact|Mitigation|
|------|-------------|--------|------------|
|Performance target missed due to bcrypt and external email latency|Medium|High|Isolate synchronous hot path, benchmark bcrypt, and decouple/reset dispatch as needed|
|Incomplete BSR causes slow incident response|Medium|High|Require dashboards, alerts, and health VLD before go-live|
|Deferred gaps are forgotten after release|Medium|Medium|Assign owners and explicit v1.1 follow-up rows in roadmap|

## Risk Assessment and Mitigation

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|JWT private-key compromise enables forged tokens|High|Low|High|RS256 asymmetric keys; secrets manager custody; 90-day RTT; RTT rehearsal|Security/Ops|
|2|Refresh token replay after theft creates session hijack risk|High|Medium|High|Rotation + replay detection + RA semantics + security tests|Backend/Auth|
|3|bcrypt cost factor becomes insufficient over time|Medium|Low|Medium|Configurable cost factor; annual OWASP review; future Argon2id migration path|Security|
|4|No progressive account lockout policy in v1|Medium|Medium|Medium|Enforce 5/min/IP immediately; define v1.1 progressive lockout extension|Product/Security|
|5|User deletion/deactivation RVC undefined in v1|Medium|Medium|Medium|Document admin workaround; define LFC RVC policy in v1.1|Product/Backend|
|6|Email PRV latency or instability degrades reset flow|Medium|Medium|Medium|Resolve sync vs queue mode; isolate PRV adapter; monitor failures|Backend/Ops|
|7|Middleware or feature-flag miswiring exposes routes incorrectly|High|Low|High|Explicit route gating tests; fail-closed middleware ordering; rollout checklist|Backend|

## Resource Requirements and Dependencies

### External Dependencies

|Dependency|Required By MLS|Status|Fallback|
|---|---|---|---|
|`jsonwebtoken`|M1-M4|Required|Block release until RS256 path verified; no HS256 fallback|
|`bcrypt`|M1-M4|Required|Tune cost only within approved policy; no alternate algorithm in v1|
|Email service PRV|M3-M4|TBD|Queue adapter or temporary SMTP bridge with owned SLA|
|Secrets manager|M1-M4|Required|Pre-provision before M1 exit; no filesystem private-key fallback|
|Uptime/APM/PagerDuty stack|M4|Required|Delay go-live until baseline monitoring is in place|

### Infrastructure Requirements

- Non-production environment with migration RLL capability.
- Secrets manager namespace for RSA private/public key material.
- Database indexing support for unique email and refresh token lookups.
- k6-capable load-test environment and APM metric ingestion.
- PagerDuty service or equivalent alert routing for auth incidents.

## Success Criteria and Validation Approach

|Criterion|Metric|Target|Validation Method|MLS|
|---|---|---|---|---|
|FR-AUTH.1 login behavior|Status and payload correctness|200/401/403 with correct token semantics and generic failure|Route/service tests and E2E LFC|M2-M4|
|FR-AUTH.2 RGS behavior|Status and VLD correctness|201/409 with email + PSS policy enforcement|Validation tests and RPS NTG tests|M2|
|FR-AUTH.3 refresh behavior|Rotation/replay outcomes|Valid refresh rotates pair; expired=401; replay revokes all|Security tests and E2E LFC|M3-M4|
|FR-AUTH.4 profile behavior|Sanitized payload correctness|id,email,display_name,created_at only; invalid token=401|Middleware + route tests|M2|
|FR-AUTH.5 reset behavior|Reset token and RVC correctness|1h token issued; invalid=400; success revokes all refresh tokens|Security tests and E2E LFC|M3-M4|
|NA.1 latency|p95 response time|<200ms under normal load|k6 test + APM dashboards|M4|
|NA.2 availability|Uptime budget|99.9% (<8.76h/year downtime)|Health checks + uptime monitoring + PagerDuty|M4|
|NA.3 hash security|bcrypt strength and timing|Cost 12; ~250ms per hash|Unit test + benchmark test|M1|

## Decision Summary

|Decision|Chosen|Alternatives Considered|Rationale|
|----------|--------|------------------------|----------|
|Token signing strategy|RS256 JWT with secrets-managed private key|HS256 JWT (rejected); opaque session tokens (rejected); PASETO (rejected)|Spec mandates RS256, stateless JWT, and secrets-manager custody with 90-day RTT|
|Password hashing algorithm|bcrypt cost factor 12|Argon2id (deferred); scrypt (rejected for v1)|Spec mandates bcrypt cost 12 and NA.3 measures that exact setting|
|Session architecture|Stateless access JWT + persisted hashed rotated refresh tokens|Server-side session store (rejected); non-rotating refresh tokens (rejected)|Constraints require stateless JWT, refresh RTT, DB-backed RVC, and replay detection|
|Refresh token client storage|httpOnly cookie|localStorage (rejected); sessionStorage (rejected)|Constraint explicitly forbids browser storage and requires httpOnly cookie|
|Rollout strategy|Feature-flagged phased enablement|Big-bang auth cutover (rejected); CLI admin controls (rejected)|Constraints require `ASE`, phase-1 backward compatibility, and no CLI surface|
|Reset delivery strategy|Resolve in M3 based on latency/resilience decision|synchronous email; queued email|Open question OI-1 directly affects endpoint latency and resiliency tradeoff|
|Active refresh session policy|Resolve in M4 architecture review|unlimited sessions; fixed cap per user|OI-2 is unresolved and materially affects RPS cleanup and multi-device behavior|

## Timeline Estimates

|MLS|Duration|Start|End|Key Milestones|
|---|---|---|---|---|
|M1|2w|W1|W2|Migration, schemas, repositories, JWT/bcrypt primitives, flag gating|
|M2|2w|W3|W4|THS, TKN, register/login/me, middleware, throttling|
|M3|2w|W5|W6|Refresh RTT, replay defense, reset flows, email NTG, cookie policy|
|M4|2w|W7|W8|Performance/availability VLD, E2E, BSR, runbooks, rollout review|

**Total estimated duration:** 8w

## Open Questions

|#|Question|Impact|Blocking MLS|Resolution Owner|
|---|---|---|---|---|
|1|Should PSS reset emails be sent synchronously or via queue?|Determines reset endpoint latency, retry semantics, and resilience posture|M3|Architect/Backend|
|2|What is the maximum number of active refresh tokens allowed per user?|Shapes RPS policy, RA blast radius, and multi-device UX|M4|Architect/Product|
|3|What progressive account lockout thresholds and escalation rules are required for v1.1?|Affects future security control design beyond basic rate limiting|M4|Security/Product|
|4|What auth audit events, schema, and retention period are required for v1.1?|Affects compliance, BSR, and storage planning|M4|Backend/Ops|
|5|How should token RVC behave on user deletion or deactivation?|Affects identity LFC correctness and admin operations|M4|Architect/Backend|
|6|Are inferred endpoint paths for register, refresh, and reset acceptable as `/auth/register`, `/auth/refresh`, `/auth/PSS-reset`, `/auth/PSS-reset/confirm`?|Path drift would cause API contract mismatch and rework|M2|API Owner|
|7|Which email PRV and template owner will support reset delivery?|Blocks PRV NTG hardening and operational support model|M3|Product/Ops|
