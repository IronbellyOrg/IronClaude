<!-- CONV: AuthService=THS, TokenManager=TKN, JwtService=JWT, Milestone=MLS, PasswordHasher=PSS, revokeAllForUser=RVK, rotation=RTT, RoutesRegistry=RTS, constraint=CNS, AUTH_SERVICE_ENABLED=ASE, AuthMiddleware=THM, integration=NTG, Implement=MPL, Integration=IN1, NFR-AUTH=NA, RefreshTokenRepository=RFR, detection=DTC, Dependencies=DPN, COMP-002=C0, password=PA1 -->
---
spec_source: "test-spec-user-auth.compressed.md"
complexity_score: 0.6
complexity_class: MEDIUM
primary_persona: architect
adversarial: false

# User Authentication Service — Project Roadmap

## Executive Summary

Deliver a layered, stateless JWT authentication service (login, registration, refresh, profile, PA1 reset) with bounded v1 scope that explicitly excludes OAuth, MFA, and RBAC. The architecture enforces strict separation between orchestration (THS), token lifecycle (TKN), low-level crypto (JWT), and PA1 hashing (PSS) so each layer is independently testable and replaceable. Rollout is gated by the `ASE` feature flag with coexistence of unauthenticated endpoints in phase 1; auth becomes mandatory in phase 2.

**Business Impact:** Unblocks authenticated user surfaces across the product, establishes a reusable crypto foundation (RS256 signing, bcrypt-12 hashing, refresh RTT with replay DTC) for all downstream services, and retires ad-hoc auth patterns. Meets 99.9% availability and <200ms p95 latency SLOs required by the broader platform reliability targets.

**Complexity:** MEDIUM (0.6) — 5 FRs with bounded surface, but elevated cryptographic rigor (RS256 asymmetric signing, bcrypt cost 12, SHA-256 refresh hashing, RTT + replay DTC) and 6 API endpoints drive the score above typical CRUD work. 10 components and 3 data models with FK relationships require disciplined dependency sequencing.

**Critical path:** RSA key pair + secrets manager (OPS-001, OPS-004) → DB migration (COMP-007) → JWT + PSS (COMP-003, COMP-004) → TKN (C0) → THS (COMP-001) → flow endpoints (FR-AUTH.1–5) → routing + middleware wiring (COMP-005, COMP-006) → rollout behind ASE flag (OPS-002).

**Key architectural decisions:**

- Stateless RS256 JWT over opaque tokens/PASETO/HS256 — mandated by CNS §1; asymmetric keys enable future verification offloading without distributing secrets.
- Layered service decomposition (THS → TKN → JWT, PSS peer) — mandated by CNS §7; each layer injectable and independently testable, matching the dependency graph.
- Refresh token RTT with replay DTC stored as SHA-256 hashes in DB — required by FR-AUTH.3 acceptance criteria; enables full-user-token invalidation on suspicious reuse (risk mitigation for HIGH-severity theft scenario).
- Feature-flag gated rollout with backward-compatible phase 1 (unauthenticated endpoints remain functional) and mandatory-auth phase 2 — mandated by constraints §8–§9; allows non-destructive rollback via flag toggle.
- bcrypt cost factor 12 with configurable parameter and documented migration path to Argon2id — mandated by CNS §2 with risk mitigation for future hardware (risk #3).

**Open risks requiring resolution before M1:**

- OI-1: Password reset email delivery mode (synchronous vs queued) must be decided before API-005/API-006 contract lock; affects reset endpoint latency SLO and resilience posture.
- OI-7: Email provider selection (SendGrid/SES/SMTP) must be confirmed before M5; secrets manager NTG (OPS-004) and Email service contract (COMP-010) depend on the choice.
- Implicit: Endpoint paths for register/refresh/PA1-reset (only `/auth/login` and `/auth/me` are verbatim in spec) — assumed under `/auth/*` route group; product owner must confirm before API contract lock at end of M2.

## MLS Summary

|ID|Title|Type|Priority|Effort|DPN|Deliverables|Risk|
|---|---|---|---|---|---|---|---|
|M1|Foundation, Data Layer & Secrets|Foundation|P0|2w|none|12|MEDIUM|
|M2|Cryptographic Services & Token Manager|Core|P0|2w|M1|8|HIGH|
|M3|Login, Registration & Middleware|Feature|P0|2w|M2|14|MEDIUM|
|M4|Token Refresh & Profile|Feature|P0|2w|M3|9|HIGH|
|M5|Password Reset Flow|Feature|P1|2w|M3, M4|10|MEDIUM|
|M6|Wiring, Rollout & Validation|IN1|P0|2w|M3, M4, M5|10|MEDIUM|

## Dependency Graph

```
M1 (Foundation)
 ├─ DM-001 UserRecord ──┐
 ├─ DM-002 RefreshTokenRecord ──┤
 ├─ DM-003 AuthTokenPair ──┐    │
 ├─ COMP-007 Migration ────┴────┘
 ├─ COMP-008 UserRepository ──┐
 ├─ COMP-009 RefreshTokenRepository ──┐
 ├─ OPS-001 RSA key pair ──────────┐  │
 └─ OPS-004 Secrets manager ───────┤  │
                                   │  │
M2 (Crypto Services) ──────────────┘  │
 ├─ COMP-003 JwtService ──┐           │
 ├─ COMP-004 PasswordHasher ──┐       │
 └─ COMP-002 TokenManager ←───┴───────┘
        │                     │
M3 (Auth Flows) ←─────────────┘
 ├─ COMP-001 AuthService ──┐
 ├─ COMP-005 AuthMiddleware ──┐
 ├─ FR-AUTH.1 Login (API-001) ──┤
 └─ FR-AUTH.2 Register (API-002) ──┘
        │
M4 (Token Lifecycle) ←─┘
 ├─ FR-AUTH.3 Refresh (API-003)
 └─ FR-AUTH.4 Profile (API-004)
        │
M5 (Reset) ←─┘
 ├─ FR-AUTH.5 Reset (API-005, API-006)
 └─ COMP-010 EmailService
        │
M6 (Rollout) ←─┘
 ├─ COMP-006 RoutesRegistry
 ├─ OPS-002 Feature flag
 └─ OPS-005 APM + PagerDuty
```

## M1: Foundation, Data Layer & Secrets

**M1: Foundation, Data Layer & Secrets** | Weeks 1–2 (2w) | Entry: spec frozen, RSA key-management policy signed off | Exit: all DB tables created with reversible migration; repositories unit-tested; RSA key pair in secrets manager; libraries pinned.

**Objective:** Establish the persistent data substrate, cryptographic key storage, and library dependencies required for every subsequent milestone. No business logic in this milestone — pure foundation.

|#|ID|Deliverable|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|
|1|DM-001|Define UserRecord schema|UserRepository|—|id:UUID-v4-PK; email:varchar-unique-idx; display_name:varchar; password_hash:varchar-bcrypt; is_locked:bool; created_at:timestamptz; updated_at:timestamptz|S|P0|
|2|DM-002|Define RefreshTokenRecord schema|RFR|DM-001|id:UUID-v4-PK; user_id:UUID-FK→UserRecord.id; token_hash:varchar-SHA256; expires_at:timestamptz; revoked:bool; created_at:timestamptz|S|P0|
|3|DM-003|Define AuthTokenPair DTO type|TKN|—|access_token:string-JWT-15min-TTL; refresh_token:string-opaque-7d-TTL; no persistence — in-memory DTO only|S|P0|
|4|COMP-007|MPL `003-auth-tables.ts` migration|Database|DM-001, DM-002|up creates users+refresh_tokens tables with FK+unique-idx; down drops both tables; idempotent; tested in CI|M|P0|
|5|COMP-008|MPL UserRepository|THS|DM-001, COMP-007|CRUD by id/email; lock-state update; never exposes password_hash in query projections; injectable interface|M|P0|
|6|COMP-009|MPL RFR|TKN|DM-002, COMP-007|create/find-by-hash/revoke/revoke-all-for-user; hash-based lookup only; injectable interface|M|P0|
|7|OPS-001|Generate RSA key pair for RS256|JWT|—|2048-bit min; private key PEM stored in secrets manager; public key distributed to verifier pods; 90-day RTT runbook drafted|M|P0|
|8|OPS-004|Secrets manager NTG|JWT|OPS-001|AWS Secrets Manager (or equiv) client wired; key fetch cached in-memory; IAM policy scoped read-only to auth service identity|M|P0|
|9|DEP-001|Pin `jsonwebtoken` library|JWT|—|version pinned in package.json; licence reviewed; SCA scan clean; used only by JWT|S|P0|
|10|DEP-002|Pin `bcrypt` library|PSS|—|version pinned; native-module build verified in CI for Linux targets; licence reviewed|S|P0|
|11|TEST-M1-001|Migration up/down NTG test|Database|COMP-007|up creates expected schema; down removes all auth tables; no residual constraints; tested against Postgres container|S|P0|
|12|TEST-M1-002|Repository CRUD NTG tests|UserRepository, RFR|COMP-008, COMP-009|unique-email CNS fires; FK cascade on user delete; revoke-all affects only target user|M|P0|

### IN1 Points — M1

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|UserRepository|DI interface|Registered in container at service boot|M1|COMP-001 THS (M3)|
|RFR|DI interface|Registered in container at service boot|M1|C0 TKN (M2)|
|RSA private key|Secrets manager secret|Fetched on JWT init, cached|M1|COMP-003 JWT (M2)|
|RSA public key|Config asset|Distributed via config/env at deploy|M1|COMP-003 JWT verify path (M2)|

### MLS DPN

- None (foundation milestone).

### MLS Risk Assessment

|Risk|Probability|Impact|Mitigation|
|---|---|---|---|
|Migration lacks down-script → irreversible rollout|Low|High|Mandated in CNS §12; PR gate requires down-migration test green|
|Secrets manager misconfiguration blocks JWT init|Low|High|Dry-run key fetch in CI; alerting on fetch failure; documented break-glass read path|
|bcrypt native build fails on target OS image|Medium|Medium|Pin to distribution with pre-built binaries; CI matrix covers target image|

## M2: Cryptographic Services & Token Manager

**M2: Cryptographic Services & Token Manager** | Weeks 3–4 (2w) | Entry: M1 exit; RSA keys available; bcrypt library operational | Exit: JWT signs/verifies RS256; PSS meets ~250ms target; TKN issues/rotates/revokes token pairs; all layers unit-tested in isolation.

**Objective:** Deliver the cryptographic primitives and the token-lifecycle orchestrator. This milestone locks the contracts (`TKN.issue`, `TKN.refresh`, `TKN.revoke*`) consumed by every flow in M3–M5.

|#|ID|Deliverable|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|
|13|COMP-003|MPL JWT (RS256 sign/verify)|JWT|OPS-001, OPS-004, DEP-001|signs with private key; verifies with public key; 15min access-token TTL enforced; rejects HS256 tokens; kid header supports RTT|M|P0|
|14|COMP-004|MPL PSS|PSS|DEP-002|bcrypt.hash with cost=12; bcrypt.compare in constant-time; cost factor exposed via config; hash/verify interface injectable|M|P0|
|15|NA.3|Verify bcrypt cost factor & hash timing|PSS|COMP-004|unit test asserts cost=12 embedded in hash prefix; benchmark test records ≈250ms wall time on reference hardware and fails if <100ms or >500ms|S|P0|
|16|C0|MPL TKN|TKN|COMP-003, COMP-009, DM-003|issue(userId) returns AuthTokenPair; refresh(token) rotates and returns new pair; revoke(tokenHash); RVK(userId); replay-DTC path invokes RVK|L|P0|
|17|OPS-006|Document RSA key RTT policy (90-day)|JWT|OPS-001|runbook covers kid advertising; grace window for overlapping keys; rollback procedure; audit-log requirement|S|P1|
|18|TEST-M2-001|JWT sign/verify unit tests|JWT|COMP-003|valid token verifies; tampered token rejected; expired token rejected; wrong-key token rejected; HS256 token rejected|S|P0|
|19|TEST-M2-002|bcrypt timing benchmark|PSS|COMP-004, NA.3|runs in CI on reference runner; median 200–300ms; fails build if out of band|S|P0|
|20|TEST-M2-003|Token RTT & replay-DTC unit tests|TKN|C0|rotate returns new pair; original refresh hash revoked; replay of revoked hash triggers RVK; race between two refreshes yields at most one live pair|M|P0|

### IN1 Points — M2

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|JWT|DI service|Registered at service boot with keys injected from secrets manager|M2|C0 TKN, COMP-005 THM|
|PSS|DI service|Registered at service boot, peer utility|M2|COMP-001 THS (login, register, reset-confirm)|
|TKN|DI service|Registered at service boot|M2|COMP-001 THS, COMP-005 THM|

### MLS DPN

- M1 (DM-001, DM-002, DM-003, COMP-007, COMP-008, COMP-009, OPS-001, OPS-004, DEP-001, DEP-002).

### MLS Risk Assessment

|Risk|Probability|Impact|Mitigation|
|---|---|---|---|
|JWT secret key compromise allows forged tokens|Low|High|RS256 asymmetric keys; private key in secrets manager; 90-day RTT (OPS-006); kid-based verification supports overlap RTT|
|Refresh-token replay attack after theft|Medium|High|Rotation on every refresh + replay DTC (C0); RVK on suspicious reuse; SHA-256 hash storage (never plaintext)|
|bcrypt cost too low for future hardware|Low|Medium|Configurable cost factor; annual OWASP review documented; migration path to Argon2id in tech-debt backlog|

## M3: Login, Registration & Middleware

**M3: Login, Registration & Middleware** | Weeks 5–6 (2w) | Entry: M2 exit; TKN + PSS locked | Exit: POST /auth/login, POST /auth/register operational end-to-end against real DB; THM verifies Bearer tokens; rate limiter enforces 5/min/IP on login.

**Objective:** Deliver the first user-visible endpoints and the request-pipeline middleware. THS becomes the orchestration seam — no flow logic lives inside endpoint handlers.

|#|ID|Deliverable|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|
|21|COMP-001|MPL THS orchestrator|THS|C0, COMP-004, COMP-008|login/register/refresh/reset methods delegate to peers; returns domain DTOs only (never raw records); transactional where needed|L|P0|
|22|FR-AUTH.1|MPL login flow|THS|COMP-001, C0, COMP-004|valid creds→AuthTokenPair; invalid→AuthError(generic, no enum leak); locked→AuthError(suspended); last_login timestamp updated|M|P0|
|23|API-001|Expose `POST /auth/login`|RTS|FR-AUTH.1, OPS-003|200 with token pair; 401 generic; 403 locked; 429 on rate-limit breach; request/response schema validated|M|P0|
|24|FR-AUTH.2|MPL registration flow|THS|COMP-001, COMP-004, COMP-008|valid data→UserRecord created + 201 profile; duplicate email→AuthError(conflict); policy + email-format validated pre-hash|M|P0|
|25|API-002|Expose `POST /auth/register`|RTS|FR-AUTH.2|201 with sanitized profile (no password_hash); 409 on duplicate email; 400 on policy/format violation; JSON schema locked|M|P0|
|26|SEC-001|Password policy validator|THS|—|enforces min 8 chars, ≥1 upper, ≥1 lower, ≥1 digit; returns structured error codes per rule; unit-tested boundary cases|S|P0|
|27|SEC-002|Email format validator|THS|—|RFC-5322 subset regex or library; rejects empty/TLD-less/control-char inputs; unit-tested against canonical valid/invalid corpora|S|P0|
|28|COMP-005|MPL THM|THM|C0, COMP-003|extracts Bearer token; invokes verify; attaches `req.user`; on invalid/expired→401; skipped for `/auth/*` public subset|M|P0|
|29|OPS-003|Rate limiter (5/min/IP on login)|THM|—|sliding-window or token-bucket; storage backend configurable; emits 429 with Retry-After; bypasses only for allowlisted internal IPs|M|P0|
|30|TEST-M3-001|Login happy-path NTG test|THS|API-001, FR-AUTH.1|returns 200 with valid JWT pair; access token decodes to correct sub; refresh token hash persisted|S|P0|
|31|TEST-M3-002|Login invalid-credentials test|THS|API-001|401 for wrong PA1 and unknown email; identical response body (no enumeration); same latency within 10% band|S|P0|
|32|TEST-M3-003|Login locked-account test|THS|API-001, COMP-008|is_locked=true user receives 403; access/refresh never issued; audit-log entry emitted|S|P0|
|33|TEST-M3-004|Registration duplicate-email test|THS|API-002|second register with same email→409; UserRecord count unchanged; no partial insert|S|P0|
|34|TEST-M3-005|Rate-limit enforcement test|THM|OPS-003|6th attempt within 60s→429 with Retry-After; counter resets per IP after window|S|P0|

### IN1 Points — M3

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|THS|DI service|Registered at boot; consumed by route handlers|M3|API-001, API-002 (M3); API-003–API-006 (M4/M5)|
|THM|Middleware chain entry|Registered in request pipeline ahead of protected routes|M3|All protected routes including API-004 (M4)|
|Rate limiter|Middleware|Wrapped around `POST /auth/login` route|M3|API-001|
|Password policy validator|THS-internal strategy|Injected into register & reset-confirm paths|M3|FR-AUTH.2 (M3), FR-AUTH.5 (M5)|
|Email format validator|THS-internal strategy|Injected into register & reset-request paths|M3|FR-AUTH.2 (M3), FR-AUTH.5 (M5)|

### MLS DPN

- M2 (C0, COMP-003, COMP-004, NA.3).

### MLS Risk Assessment

|Risk|Probability|Impact|Mitigation|
|---|---|---|---|
|User enumeration via timing or error-message differences|Medium|Medium|Identical response body for all 401 cases; constant-time compare via bcrypt; TEST-M3-002 asserts latency band|
|Rate limiter storage SPOF|Low|Medium|Use shared Redis or equivalent with failover; fail-open policy documented with audit-logging on degraded mode|
|Middleware ordering mistakes expose protected routes|Low|High|IN1 test for each protected route verifies 401 without token; route-registry contract test enforces middleware order|

## M4: Token Refresh & Profile

**M4: Token Refresh & Profile** | Weeks 7–8 (2w) | Entry: M3 exit; THM verifying Bearer tokens; TKN RTT path unit-tested | Exit: `/auth/refresh` rotates tokens with replay DTC; `/auth/me` returns sanitized profile; replay attempts invalidate all user tokens.

**Objective:** Complete the access-token lifecycle by adding refresh and profile. Replay DTC is the single HIGH-severity security deliverable of this milestone.

|#|ID|Deliverable|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|
|35|FR-AUTH.3|MPL token refresh flow|THS|C0, COMP-009|valid refresh→rotated AuthTokenPair; expired→401 force re-auth; replay of revoked→RVK + 401; refresh hashes always SHA-256|M|P0|
|36|API-003|Expose `POST /auth/refresh`|RTS|FR-AUTH.3|200 with new pair; 401 for expired/replayed; refresh sourced from httpOnly cookie per CNS §3; new refresh set via Set-Cookie httpOnly+secure+sameSite|M|P0|
|37|FR-AUTH.4|MPL profile retrieval|THS|COMP-001, COMP-005, COMP-008|valid Bearer→sanitized profile(id, email, display_name, created_at); expired/invalid→401; no password_hash, no refresh_token_hash ever returned|S|P0|
|38|API-004|Expose `GET /auth/me`|RTS|FR-AUTH.4, COMP-005|200 with ProfileDTO; 401 without/invalid token; schema excludes sensitive fields by design; JSON schema contract-tested|S|P0|
|39|SEC-003|Refresh RTT + replay DTC|TKN|C0, COMP-009|every refresh revokes old hash and issues new; replayed revoked hash→RVK(userId)+audit event; race-safe via DB-row lock on token_hash|M|P0|
|40|SEC-004|Profile field sanitization contract|THS|FR-AUTH.4|ProfileDTO mapper defined; serializer has allowlist not denylist; sensitive-field regression test over response JSON|S|P0|
|41|TEST-M4-001|Refresh RTT NTG test|TKN|FR-AUTH.3, API-003|refresh issues new pair; old refresh cannot be reused; audit entry on RTT|S|P0|
|42|TEST-M4-002|Replay-DTC NTG test|TKN|SEC-003|replay of revoked refresh triggers RVK; all active refresh tokens for user marked revoked; subsequent refreshes/API calls→401|M|P0|
|43|TEST-M4-003|Profile no-leak regression test|THS|FR-AUTH.4, SEC-004|response JSON keys match ProfileDTO allowlist exactly; `password_hash`, `token_hash`, `is_locked` never serialized|S|P0|

### IN1 Points — M4

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|TKN.refresh|Callback from THS|Injected|M4|API-003|
|ProfileDTO mapper|Serializer strategy|Registered on THS|M4|API-004|
|Replay-DTC audit event|Event binding|TKN emits event; logger subscribes|M4|Admin dashboard, audit log (future GAP-2)|

### MLS DPN

- M3 (COMP-001, COMP-005).

### MLS Risk Assessment

|Risk|Probability|Impact|Mitigation|
|---|---|---|---|
|Race condition allows two valid refresh pairs from one parent|Medium|High|DB-row lock on refresh_tokens.token_hash; TEST-M4-002 includes concurrent refresh scenario|
|Profile endpoint leaks sensitive fields after schema evolution|Medium|High|ProfileDTO allowlist serializer; TEST-M4-003 regression guard; PR gate enforces DTO review|
|httpOnly cookie misconfiguration on refresh exposes token to JS|Low|High|IN1 test asserts Set-Cookie attributes include HttpOnly+Secure+SameSite; OWASP header lint in CI|

## M5: Password Reset Flow

**M5: Password Reset Flow** | Weeks 9–10 (2w) | Entry: M4 exit; email provider decided (OI-7); synchronous-vs-queued dispatch decision (OI-1) | Exit: reset request generates email; confirmation endpoint accepts valid token and invalidates all refresh tokens.

**Objective:** Close the last FR by delivering the reset flow with correct email dispatch, 1h token TTL, single-use enforcement, and post-reset token invalidation.

|#|ID|Deliverable|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|
|44|FR-AUTH.5|MPL PA1 reset flow|THS|COMP-001, C0, COMP-004, COMP-010|registered email→reset token(1h)+email dispatched; valid token→new PA1 stored + reset token invalidated; expired/invalid→400; successful reset→RVK|L|P0|
|45|API-005|Expose `POST /auth/PA1-reset`|RTS|FR-AUTH.5|always 202 whether email known or not (no enumeration); rate-limited per IP; reset token hash stored, plaintext emailed once|M|P0|
|46|API-006|Expose `POST /auth/PA1-reset/confirm`|RTS|FR-AUTH.5|valid reset-token+new PA1 meeting SEC-001→200; invalid/expired→400; token single-use (revoked after success); refresh tokens for user revoked|M|P0|
|47|COMP-010|EmailService adapter|EmailService|DEP-003|send(reset-email-template, recipient, token-link); retries on transient failure; failures do not leak recipient existence in response|M|P0|
|48|DEP-003|Select & integrate email provider|EmailService|OI-7|provider decision documented (SendGrid/SES/SMTP); API key in secrets manager; sandbox creds for non-prod; SPF/DKIM/DMARC configured|M|P0|
|49|SEC-005|Reset token TTL + single-use enforcement|THS|FR-AUTH.5|token stored as SHA-256 hash; `expires_at` = now+1h; consumed-flag set atomically with PA1 update; replay after success→400|M|P0|
|50|SEC-006|Invalidate-all refresh on reset|THS|SEC-005, COMP-009|after successful PA1 update, RVK invoked in same transaction; TEST-M5-003 verifies active sessions terminated|S|P0|
|51|TEST-M5-001|Reset email dispatch NTG test|EmailService|API-005, COMP-010|request for known email→email provider mock invoked with correct template+link; request for unknown email→202 with no provider call|S|P0|
|52|TEST-M5-002|Reset token expiry test|THS|SEC-005|token used at 59m→accepted; at 61m→400; invalid random token→400; reused after success→400|S|P0|
|53|TEST-M5-003|Reset invalidates all refresh tokens|THS|SEC-006|prior refresh tokens issued; reset succeeds; attempt to refresh with old refresh→401; new login required|S|P0|

### IN1 Points — M5

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|EmailService|DI service|Registered at boot; env decides sandbox vs prod credentials|M5|THS reset flow|
|Reset token store|Repository extension|RFR OR dedicated reset_tokens table (decision in M5 kickoff)|M5|THS reset flow|
|Reset email template|Config asset|Owned by product + ops; version-controlled|M5|EmailService|

### MLS DPN

- M3 (COMP-001 THS, SEC-001 PA1 policy).
- M4 (SEC-003 replay DTC — reset flow relies on RVK path).

### MLS Risk Assessment

|Risk|Probability|Impact|Mitigation|
|---|---|---|---|
|Email dispatch latency breaks <200ms p95 SLO for reset endpoint|Medium|Medium|OI-1 decision: queue dispatch asynchronously so API-005 returns 202 immediately; NA.1 measured only on sync path|
|Account enumeration via differential responses on reset request|Medium|Medium|API-005 always returns 202 and identical body; timing parity enforced via TEST fixture|
|Reset token leaks in logs (token in URL querystring logged)|Medium|High|Token delivered in URL path fragment or POST body; logging middleware redacts auth-related query params; review log sinks|

## M6: Wiring, Rollout & Validation

**M6: Wiring, Rollout & Validation** | Weeks 11–12 (2w) | Entry: M5 exit; all flows implemented and unit-tested | Exit: `ASE` flag toggles `/auth/*` routing; APM+PagerDuty in place; k6 confirms <200ms p95; E2E lifecycle test green; rollback rehearsed.

**Objective:** Wire the finished components into the request pipeline, ship behind a flag, and close both NFRs with real measurement. No new business logic — this milestone is NTG, observability, and validation only.

|#|ID|Deliverable|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|
|54|COMP-006|Register `/auth/*` routes in RTS|RTS|API-001, API-002, API-003, API-004, API-005, API-006|route group added to `src/routes/index.ts`; gated by ASE; route inventory doc updated|S|P0|
|55|OPS-002|MPL `ASE` feature flag|RTS|COMP-006|flag backed by config system supporting runtime toggle; false→/auth/* routes return 404 (or pass-through); true→routes active|S|P0|
|56|OPS-005|Wire APM + PagerDuty for auth service|Observability|—|health-check endpoint exposed; APM instruments THS latency per flow; PagerDuty escalation policy binds to health-check failure; SLO dashboard published|M|P0|
|57|DEP-004|Secrets manager operational readiness|JWT, EmailService|OPS-001, OPS-004, DEP-003|prod secrets provisioned and rotated once in staging; IAM policies audited; break-glass recovery doc written|S|P0|
|58|DEP-005|APM + Uptime + PagerDuty operational|Observability|OPS-005|synthetic probes hitting `/auth/login` (canary user) and `/auth/me`; uptime calculated from probe success; alert routes verified in drill|S|P0|
|59|NA.1|Validate latency <200ms p95 under load|THS|All auth endpoints, OPS-005|k6 load test sustained 50 rps for 10 min across /login and /refresh; p95<200ms; results archived; APM dashboard confirms in prod shadow window|M|P0|
|60|NA.2|Validate 99.9% availability SLO|Observability|OPS-005, DEP-005|30-day rolling uptime≥99.9% in staging soak; incident runbook reviewed; PagerDuty on-call rota activated|M|P0|
|61|TEST-M6-001|E2E user lifecycle test|THS|All API endpoints|register→login→GET /me→refresh→PA1-reset→login-with-new-PA1 passes with expected status codes; old refresh tokens invalid after reset|M|P0|
|62|TEST-M6-002|Feature-flag rollback test|RTS|OPS-002|toggle flag off during active traffic; new requests return expected fallback; in-flight requests complete without error; toggle back on restores service|S|P0|
|63|OPS-007|Publish rollout runbook + rollback procedure|Operations|OPS-002, OPS-005|runbook covers phase-1 coexistence, phase-2 mandatory-auth cutover, flag rollback, key-RTT break-glass; signed off by SRE|S|P1|

### IN1 Points — M6

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|RTS|Route table dispatch|Registers handler per API-00x inside `/auth/*` group at boot|M6|Request pipeline|
|ASE flag|Config flag (strategy pattern)|Read at route registration; recheck per-request on hot-reload|M6|RTS, tests|
|APM latency instrumentation|Middleware + in-service timers|Wrapped around each THS method and route handler|M6|Observability dashboards|
|PagerDuty escalation|Event binding|Health-check failure → PagerDuty REST API event-create|M6|On-call rota|
|Admin dashboard NTG|Operational callback|Revoke-token / lock-account actions call THS admin methods|M6|Ops team (per CNS §11: no CLI)|

### MLS DPN

- M3 (API-001, API-002).
- M4 (API-003, API-004).
- M5 (API-005, API-006).

### MLS Risk Assessment

|Risk|Probability|Impact|Mitigation|
|---|---|---|---|
|Flag rollback leaves orphaned sessions|Low|Medium|Rollback runbook (OPS-007) covers session handling; flag off only serves 404, never invalid tokens; clients handle 404 as re-auth|
|Latency SLO fails under production load despite k6 pass|Medium|Medium|Canary deploy with 5% traffic first; APM watches p95 for 24h; rollback via OPS-002 flag if SLO breach detected|
|Availability SLO missed due to secrets manager outage|Low|High|Cache RSA keys in-memory on JWT init; fail-open with cached keys during secrets outage; incident runbook documents the break-glass|

## Risk Assessment and Mitigation

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|R1|JWT private key compromise allows forged tokens|HIGH|Low|High|RS256 asymmetric keys; secrets manager storage (OPS-004); 90-day RTT (OPS-006); kid-based overlap RTT|Architect / Security|
|R2|Refresh token replay after theft|HIGH|Medium|High|Rotation on every refresh + replay DTC (SEC-003); SHA-256 hash storage; RVK on suspicious reuse|Architect|
|R3|bcrypt cost factor too low for future hardware|MEDIUM|Low|Medium|Configurable cost; annual OWASP review; Argon2id migration path on backlog|Security|
|R4|GAP-1 — No progressive account lockout|MEDIUM|Medium|Medium|Rate-limit (OPS-003) addresses short-window attack; progressive lockout deferred to v1.1 with ADR|Product / Security|
|R5|GAP-3 — Token revocation on user deletion not addressed|MEDIUM|Low|Medium|Operational workaround via admin dashboard (RVK manual trigger); fully automated in v1.1|Architect|
|R6|User enumeration via differential responses|MEDIUM|Medium|Medium|Identical 401 response body for login; 202 response for reset-request; timing parity assertions in tests|Security|
|R7|httpOnly cookie misconfiguration exposes refresh to JS|HIGH|Low|High|Contract tests on Set-Cookie flags (HttpOnly, Secure, SameSite=Strict); OWASP header lint in CI|Backend|
|R8|Migration lacks reversible down-script|HIGH|Low|High|Constraint §12 mandates down-migration; CI job asserts down-then-up idempotence|DevOps|
|R9|Reset token leaks via logs|HIGH|Medium|High|Token in POST body only; log-redaction middleware; log-sink review before rollout|Security|
|R10|Latency SLO breach under production load|MEDIUM|Medium|Medium|k6 pre-validation (NA.1); canary 5% deploy with APM watch; flag rollback path|SRE|
|R11|Email dispatch outage blocks PA1 reset|MEDIUM|Medium|Medium|Async queue dispatch (OI-1); provider fallback documented; user self-service rollback via login if email delayed|Backend|
|R12|GAP-2 — No audit logging schema defined|MEDIUM|High|Medium|Emit audit events from SEC-003, SEC-005, SEC-006 to a structured log sink now; formalize schema in v1.1|Architect|
|R13|Scope creep pulling OAuth/MFA/RBAC into v1|MEDIUM|Medium|Medium|Constraint §10 explicitly out-of-scope; ADR records deferral; change-control gate on scope additions|PM|

## Resource Requirements and DPN

### External DPN

|Dependency|Required By MLS|Status|Fallback|
|---|---|---|---|
|`jsonwebtoken` library (DEP-001)|M1 (pin), M2 (use)|Stable upstream|Pin to last-known-good; internal fork if licence change|
|`bcrypt` library (DEP-002)|M1 (pin), M2 (use)|Stable upstream; native build|`bcryptjs` as pure-JS fallback (document perf delta)|
|Email service provider (DEP-003)|M5|Selection pending (OI-7)|SMTP fallback via internal relay; document delivery SLA trade-off|
|Secrets manager (OPS-004, DEP-004)|M1 (integrate), M6 (operational)|Assumed available (AWS Secrets Manager or equiv)|Encrypted file-based secret with strict IAM (non-prod only)|
|APM + Uptime + PagerDuty (OPS-005, DEP-005)|M6|Platform-level dependency|Stack-local Prometheus + Alertmanager as interim|

### Infrastructure Requirements

- Postgres (or equivalent) with FK + unique-index support for the new `users` and `refresh_tokens` tables (COMP-007).
- Secrets manager with per-identity IAM policies scoped to the auth service (OPS-004).
- Redis or equivalent shared store for the rate limiter (OPS-003).
- APM agent runtime installed in service container (OPS-005).
- CI runner with Postgres container for migration and repository NTG tests (TEST-M1-001, TEST-M1-002).
- Load-testing environment capable of 50 rps sustained (NA.1 validation via k6).
- Email provider sandbox credentials for non-prod environments (DEP-003).

## Success Criteria and Validation Approach

|Criterion|Metric|Target|Validation Method|MLS|
|---|---|---|---|---|
|FR-AUTH.1 login correctness|Status code + token pair validity|200/401/403/429 per matrix|IN1 tests TEST-M3-001/002/003/005 + manual smoke|M3|
|FR-AUTH.2 registration correctness|Status code + DB record + PA1 policy|201/400/409 per matrix|IN1 tests TEST-M3-004 + policy unit tests (SEC-001/002)|M3|
|FR-AUTH.3 refresh + replay DTC|Token RTT + replay→revokeAll|New pair issued; replay→full invalidation|TEST-M4-001, TEST-M4-002|M4|
|FR-AUTH.4 profile no-leak|Response schema|Allowlist-only fields returned|TEST-M4-003 contract test + static DTO review|M4|
|FR-AUTH.5 reset correctness|Token TTL + single-use + invalidation|1h TTL; single-use; refresh revoked post-reset|TEST-M5-001/002/003|M5|
|NA.1 latency|p95 latency across auth endpoints|<200ms under sustained 50 rps|k6 report + APM 24h production shadow|M6|
|NA.2 availability|Uptime (monthly)|≥99.9%|Uptime-probe aggregation + PagerDuty incident log review|M6|
|NA.3 PA1 hashing|bcrypt cost factor + hash latency|cost=12; 200–300ms p50|Unit test (cost prefix) + benchmark test (TEST-M2-002)|M2|
|E2E user lifecycle|Register→login→me→refresh→reset→login-new-pwd|All steps green; old credentials invalidated|TEST-M6-001|M6|

## Decision Summary

|Decision|Chosen|Alternatives Considered|Rationale|
|---|---|---|---|
|Token format|RS256 JWT|HS256 JWT; opaque tokens with server store; PASETO|Mandated by CNS §1; RS256 supports verifier distribution without sharing private key|
|Password hashing|bcrypt cost 12|Argon2id; scrypt|Mandated by CNS §2; bcrypt has mature ecosystem and known ~250ms target on reference hardware|
|Refresh token storage|httpOnly cookie + SHA-256 hash in DB|localStorage; sessionStorage; opaque server session|Mandated by CNS §3; CNS §4 forbids server-side session store; hash prevents DB-leak-enables-replay|
|Session strategy|Stateless JWT|Server-side session store|Mandated by CNS §4; enables horizontal scaling without session stickiness|
|Refresh RTT policy|Rotate on every refresh + replay DTC|Long-lived refresh; no RTT|Mandated by CNS §5; mitigates HIGH-severity risk R2 (refresh theft / replay)|
|Key storage|Secrets manager with 90-day RTT|Environment variables; config files; KMS-only|Mandated by CNS §6; mitigates HIGH-severity risk R1; supports auditability|
|Component layering|THS → TKN → JWT + PSS peer|Monolithic AuthController; flat services|Mandated by CNS §7; each layer testable in isolation and swappable (e.g., Argon2id migration path only touches PSS)|
|Rollout strategy|Feature-flag gated with phase-1 coexistence|Big-bang cutover; blue/green only|Mandated by constraints §8–§9; rollback via flag toggle is lowest-blast-radius|
|v1 scope exclusions|OAuth/MFA/RBAC deferred to v2.0|Include minimal MFA now|Constraint §10 fixes scope; MEDIUM complexity (0.6) already near upper bound for target duration|
|Admin surface|Admin dashboard only (no CLI)|CLI scripts; runbook-only|Mandated by CNS §11; dashboard already exists as operational surface|
|Email delivery mode|Async queue (pending OI-1 confirmation)|Synchronous dispatch|Keeps API-005 under NA.1 p95 SLO; isolates email provider outages from auth uptime (mitigates R11)|
|Reset token store|Dedicated reset_tokens table (recommended)|Reuse refresh_tokens table|Separation prevents accidental replay-DTC entanglement; revocation semantics differ (single-use vs rotate)|

## Timeline Estimates

|MLS|Duration|Start|End|Key Milestones|
|---|---|---|---|---|
|M1|2 weeks|Week 1|Week 2|DB migration green; repositories tested; RSA keys in secrets manager|
|M2|2 weeks|Week 3|Week 4|JWT + PSS unit-tested; TKN RTT verified; bcrypt benchmark banded|
|M3|2 weeks|Week 5|Week 6|Login + Register endpoints live against real DB; THM verifies Bearer; rate limiter enforced|
|M4|2 weeks|Week 7|Week 8|Refresh RTT + replay DTC operational; GET /auth/me returns sanitized profile|
|M5|2 weeks|Week 9|Week 10|Reset request + confirm endpoints; reset token TTL + single-use enforced; refresh tokens invalidated on reset|
|M6|2 weeks|Week 11|Week 12|Routes wired behind ASE flag; APM+PagerDuty live; NA.1 & NA.2 validated; E2E lifecycle green|

**Total estimated duration:** 12 weeks (3 calendar months), sequential with gated handoffs; no parallel milestone tracks assumed for v1.

## Open Questions

|#|Question|Impact|Blocking MLS|Resolution Owner|
|---|---|---|---|---|
|OI-1|Password reset emails: synchronous dispatch vs message queue?|Reset endpoint latency SLO (NA.1) + resilience to email-provider outages (R11)|M5|Architect + Backend lead|
|OI-2|Maximum concurrent active refresh tokens per user?|Storage growth; multi-device UX; revoke-all semantics|M4 (contract); enforceable change in v1.1 if deferred|Architect + Product|
|GAP-1|Progressive account lockout threshold after N failed attempts?|Partial coverage of brute-force attack (R4); v1 ships rate-limit only|Not blocking v1; scheduled for v1.1|Security|
|GAP-2|Audit logging schema and retention policy for auth events?|Forensic readiness (R12); compliance|Not blocking v1 but emit events now per R12 mitigation|Architect + Compliance|
|GAP-3|Token revocation behavior on user deletion / deactivation?|Ghost sessions after account removal (R5)|Not blocking v1; manual workaround via admin dashboard in v1|Architect|
|OI-6|Endpoint paths for register/refresh/PA1-reset (only /auth/login and /auth/me verbatim in spec)|API contract stability; consumer NTG|M2 (contract lock before M3 implementation)|Product + Architect|
|OI-7|Email provider selection (SendGrid/SES/SMTP) and template ownership|Blocks DEP-003 and COMP-010|M5 (must resolve before sprint kickoff)|Product + DevOps|
