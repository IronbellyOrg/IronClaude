---
spec_source: "test-spec-user-auth.compressed.md"
complexity_score: 0.6
complexity_class: MEDIUM
primary_persona: architect
adversarial: true
base_variant: "opus-architect"
variant_scores: "A(opus):78 B(haiku):70"
convergence_score: 0.72
---

# User Authentication Service — Project Roadmap

## Executive Summary

Deliver a layered, stateless JWT authentication service (login, registration, refresh, profile, password reset) with bounded v1 scope that explicitly excludes OAuth, MFA, and RBAC. The architecture enforces strict separation between orchestration (AuthService), token lifecycle (TokenManager), low-level crypto (JwtService), and password hashing (PasswordHasher) so each layer is independently testable and replaceable. Rollout is gated by the `AUTH_SERVICE_ENABLED` feature flag with coexistence of unauthenticated endpoints in phase 1; auth becomes mandatory in phase 2.

**Business Impact:** Unblocks authenticated user surfaces across the product, establishes a reusable crypto foundation (RS256 signing, bcrypt-12 hashing, refresh rotation with replay detection) for all downstream services, and retires ad-hoc auth patterns. Meets 99.9% availability and <200ms p95 latency SLOs required by the broader platform reliability targets.

**Complexity:** MEDIUM (0.6) — 5 FRs with bounded surface, but elevated cryptographic rigor (RS256 asymmetric signing, bcrypt cost 12, SHA-256 refresh hashing, rotation + replay detection) and 6 API endpoints drive the score above typical CRUD work. 10 components and 3 data models with FK relationships require disciplined dependency sequencing.

**Critical path:** RSA key pair + secrets manager (OPS-001, OPS-004) → DB migration (COMP-007) → JwtService + PasswordHasher (COMP-003, COMP-004) → TokenManager (COMP-002) → AuthService (COMP-001) → flow endpoints (FR-AUTH.1–5) → routing + middleware wiring (COMP-005, COMP-006) → rollout behind AUTH_SERVICE_ENABLED flag (OPS-002).

**Key architectural decisions:**

- Stateless RS256 JWT over opaque tokens/PASETO/HS256 — mandated by constraints §1; asymmetric keys enable future verification offloading without distributing secrets.
- Layered service decomposition (AuthService → TokenManager → JwtService, PasswordHasher peer) — mandated by constraints §7; each layer injectable and independently testable, matching the dependency graph.
- Refresh token rotation with replay detection stored as SHA-256 hashes in DB — required by FR-AUTH.3 acceptance criteria; enables full-user-token invalidation on suspicious reuse (mitigation for HIGH-severity theft scenario).
- Feature-flag gated rollout with backward-compatible phase 1 (unauthenticated endpoints remain functional) and mandatory-auth phase 2 — mandated by constraints §8–§9; allows non-destructive rollback via flag toggle.
- bcrypt cost factor 12 with configurable parameter and documented migration path to Argon2id — mandated by constraints §2 with forward-hardware mitigation (risk R3).
- Refresh token delivered and stored only in httpOnly+Secure+SameSite cookies with an explicit cookie-policy deliverable (SEC-007) — mandated by constraints §3; browser storage paths explicitly forbidden.
- Explicit v1.1 handoff ownership for deferred gaps (progressive lockout, audit logging schema, deletion/deactivation revocation) via GAP-1/GAP-2/GAP-3 planning deliverables with named owners rather than risk-register-only discipline.

**Open risks requiring resolution before M1:**

- OI-7: Email provider selection (SendGrid/SES/SMTP) must be confirmed before M5; secrets manager integration (OPS-004) and EmailService contract (COMP-010) depend on the choice.
- OI-6: Endpoint paths for register/refresh/password-reset (only `/auth/login` and `/auth/me` are verbatim in spec) — assumed under `/auth/*` route group; product owner must confirm before API contract lock at end of M2.
- OI-1: Password reset email delivery mode (synchronous vs queued) must be decided at M5 kickoff (scheduled as an M5 planning deliverable, not a pre-M1 blocker) because it affects reset endpoint latency SLO and resilience posture.

## Milestone Summary

| ID | Title | Type | Priority | Effort | Dependencies | Deliverables | Risk |
|---|---|---|---|---|---|---|---|
| M1 | Foundation, Data Layer & Secrets | Foundation | P0 | 2w | none | 12 | MEDIUM |
| M2 | Cryptographic Services & Token Manager | Core | P0 | 2w | M1 | 8 | HIGH |
| M3 | Login, Registration & Middleware | Feature | P0 | 2w | M2 | 15 | MEDIUM |
| M4 | Token Refresh & Profile | Feature | P0 | 2w | M3 | 10 | HIGH |
| M5 | Password Reset Flow | Feature | P1 | 2w | M3, M4 | 11 | MEDIUM |
| M6 | Wiring, Rollout & Validation | Integration | P0 | 2w | M3, M4, M5 | 15 | MEDIUM |

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
        │
M3 (Auth Flows + Middleware) ←─┘
 ├─ COMP-001 AuthService ──┐
 ├─ COMP-005 AuthMiddleware ──┐
 ├─ COMP-017 Account suspension hook ──┤
 ├─ FR-AUTH.1 Login (API-001) ─────────┤
 └─ FR-AUTH.2 Register (API-002) ──────┘
        │
M4 (Token Lifecycle + Profile) ←─┘
 ├─ FR-AUTH.3 Refresh (API-003)
 ├─ FR-AUTH.4 Profile (API-004)
 └─ SEC-007 Refresh cookie policy
        │
M5 (Reset) ←─┘
 ├─ FR-AUTH.5 Reset (API-005, API-006)
 ├─ OI-1-DEC Reset dispatch mode decision
 └─ COMP-010 EmailService
        │
M6 (Rollout + v1.1 Handoff) ←─┘
 ├─ COMP-006 RoutesRegistry
 ├─ OPS-002 Feature flag
 ├─ OPS-005/009 APM + health endpoint
 ├─ OPS-007/008 Runbook + go-live checklist
 └─ GAP-1/GAP-2/GAP-3 v1.1 handoff plans
```

## M1: Foundation, Data Layer & Secrets

**Objective:** Establish the persistent data substrate, cryptographic key storage, and library dependencies required for every subsequent milestone. No business logic in this milestone — pure foundation. | **Duration:** 2w (W1–W2) | **Entry:** spec frozen; RSA key-management policy signed off | **Exit:** all DB tables created with reversible migration; repositories unit-tested; RSA key pair in secrets manager; libraries pinned.

| # | ID | Deliverable | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | DM-001 | Define UserRecord schema | UserRepository | — | id:UUIDv4-PK; email:varchar-unique-idx; display_name:varchar; password_hash:varchar-bcrypt; is_locked:bool; created_at:timestamptz; updated_at:timestamptz | S | P0 |
| 2 | DM-002 | Define RefreshTokenRecord schema | RefreshTokenRepository | DM-001 | id:UUIDv4-PK; user_id:UUID-FK→UserRecord.id; token_hash:varchar-SHA256; expires_at:timestamptz; revoked:bool; created_at:timestamptz | S | P0 |
| 3 | DM-003 | Define AuthTokenPair DTO type | TokenManager | — | access_token:string-JWT-15min-TTL; refresh_token:string-opaque-7d-TTL; no persistence — in-memory DTO only | S | P0 |
| 4 | COMP-007 | Implement `003-auth-tables.ts` migration | Database | DM-001, DM-002 | up creates users+refresh_tokens tables with FK+unique-idx; down drops both tables; idempotent; tested in CI | M | P0 |
| 5 | COMP-008 | Implement UserRepository | AuthService | DM-001, COMP-007 | CRUD by id/email; lock-state update; update-password; never exposes password_hash in query projections; injectable interface | M | P0 |
| 6 | COMP-009 | Implement RefreshTokenRepository | TokenManager | DM-002, COMP-007 | create/find-by-hash/revoke/revoke-all-for-user; hash-based lookup only; injectable interface | M | P0 |
| 7 | OPS-001 | Generate RSA key pair for RS256 | JwtService | — | 2048-bit min; private key PEM stored in secrets manager; public key distributed to verifier pods; 90-day rotation runbook drafted | M | P0 |
| 8 | OPS-004 | Secrets manager integration | JwtService | OPS-001 | AWS Secrets Manager (or equiv) client wired; key fetch cached in-memory; IAM policy scoped read-only to auth service identity | M | P0 |
| 9 | DEP-001 | Pin `jsonwebtoken` library | JwtService | — | version pinned in package.json; licence reviewed; SCA scan clean; used only by JwtService | S | P0 |
| 10 | DEP-002 | Pin `bcrypt` library | PasswordHasher | — | version pinned; native-module build verified in CI for Linux targets; licence reviewed | S | P0 |
| 11 | TEST-M1-001 | Migration up/down integration test | Database | COMP-007 | up creates expected schema; down removes all auth tables; no residual constraints; tested against Postgres container | S | P0 |
| 12 | TEST-M1-002 | Repository CRUD integration tests | UserRepository, RefreshTokenRepository | COMP-008, COMP-009 | unique-email constraint fires; FK cascade on user delete; revoke-all affects only target user | M | P0 |

### Integration Points — M1

| Artifact | Type | Wired | Milestone | Consumed By |
|---|---|---|---|---|
| UserRepository | DI interface | Registered in container at service boot | M1 | COMP-001 AuthService (M3) |
| RefreshTokenRepository | DI interface | Registered in container at service boot | M1 | COMP-002 TokenManager (M2) |
| RSA private key | Secrets manager secret | Fetched on JwtService init, cached in-memory | M1 | COMP-003 JwtService (M2) |
| RSA public key | Config asset | Distributed via config/env at deploy | M1 | COMP-003 JwtService verify path (M2) |
| `003-auth-tables.ts` | Migration | Bound into migration runner; reversible | M1 | UserRepository, RefreshTokenRepository |

### Milestone Dependencies — M1

- None (foundation milestone).

### Milestone Risk Assessment — M1

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Migration lacks down-script → irreversible rollout | Low | High | Mandated in constraints §12; PR gate requires down-migration test green |
| Secrets manager misconfiguration blocks JwtService init | Low | High | Dry-run key fetch in CI; alerting on fetch failure; documented break-glass read path |
| bcrypt native build fails on target OS image | Medium | Medium | Pin to distribution with pre-built binaries; CI matrix covers target image |

## M2: Cryptographic Services & Token Manager

**Objective:** Deliver the cryptographic primitives and the token-lifecycle orchestrator. This milestone locks the contracts (`TokenManager.issue`, `TokenManager.refresh`, `TokenManager.revoke*`) consumed by every flow in M3–M5. | **Duration:** 2w (W3–W4) | **Entry:** M1 exit; RSA keys available; bcrypt library operational | **Exit:** JwtService signs/verifies RS256; PasswordHasher meets ~250ms target; TokenManager issues/rotates/revokes token pairs; all layers unit-tested in isolation.

| # | ID | Deliverable | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 13 | COMP-003 | Implement JwtService (RS256 sign/verify) | JwtService | OPS-001, OPS-004, DEP-001 | signs with private key; verifies with public key; 15min access-token TTL enforced; rejects HS256 tokens; kid header supports rotation | M | P0 |
| 14 | COMP-004 | Implement PasswordHasher | PasswordHasher | DEP-002 | bcrypt.hash with cost=12; bcrypt.compare in constant-time; cost factor exposed via config; hash/verify interface injectable | M | P0 |
| 15 | NFR-AUTH.3 | Verify bcrypt cost factor & hash timing | PasswordHasher | COMP-004 | unit test asserts cost=12 embedded in hash prefix; benchmark test records ≈250ms wall time on reference hardware and fails if <100ms or >500ms | S | P0 |
| 16 | COMP-002 | Implement TokenManager | TokenManager | COMP-003, COMP-009, DM-003 | issue(userId) returns AuthTokenPair; refresh(token) rotates and returns new pair; revoke(tokenHash); revokeAllForUser(userId); replay-detection path invokes revokeAllForUser | L | P0 |
| 17 | OPS-006 | Document RSA key rotation policy (90-day) | JwtService | OPS-001 | runbook covers kid advertising; grace window for overlapping keys; rollback procedure; audit-log requirement | S | P1 |
| 18 | TEST-M2-001 | JwtService sign/verify unit tests | JwtService | COMP-003 | valid token verifies; tampered token rejected; expired token rejected; wrong-key token rejected; HS256 token rejected | S | P0 |
| 19 | TEST-M2-002 | bcrypt timing benchmark | PasswordHasher | COMP-004, NFR-AUTH.3 | runs in CI on reference runner; median 200–300ms; fails build if out of band | S | P0 |
| 20 | TEST-M2-003 | Token rotation & replay-detection unit tests | TokenManager | COMP-002 | rotate returns new pair; original refresh hash revoked; replay of revoked hash triggers revokeAllForUser; race between two refreshes yields at most one live pair | M | P0 |

### Integration Points — M2

| Artifact | Type | Wired | Milestone | Consumed By |
|---|---|---|---|---|
| JwtService | DI service | Registered at service boot with keys injected from secrets manager | M2 | COMP-002 TokenManager, COMP-005 AuthMiddleware |
| PasswordHasher | DI service | Registered at service boot; peer utility | M2 | COMP-001 AuthService (login, register, reset-confirm) |
| TokenManager | DI service | Registered at service boot | M2 | COMP-001 AuthService, COMP-005 AuthMiddleware |
| kid-aware verify | Strategy binding | JwtService selects public key by kid for overlapping-key rotation | M2 | JwtService verify path |

### Milestone Dependencies — M2

- M1 (DM-001, DM-002, DM-003, COMP-007, COMP-008, COMP-009, OPS-001, OPS-004, DEP-001, DEP-002).

### Milestone Risk Assessment — M2

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| JWT private key compromise allows forged tokens | Low | High | RS256 asymmetric keys; private key in secrets manager; 90-day rotation (OPS-006); kid-based verification supports overlap rotation |
| Refresh-token replay attack after theft | Medium | High | Rotation on every refresh + replay detection (COMP-002); revokeAllForUser on suspicious reuse; SHA-256 hash storage (never plaintext) |
| bcrypt cost too low for future hardware | Low | Medium | Configurable cost factor; annual OWASP review documented; migration path to Argon2id in tech-debt backlog |

## M3: Login, Registration & Middleware

**Objective:** Deliver the first user-visible endpoints and the request-pipeline middleware. AuthService becomes the orchestration seam — no flow logic lives inside endpoint handlers. | **Duration:** 2w (W5–W6) | **Entry:** M2 exit; TokenManager + PasswordHasher locked | **Exit:** POST /auth/login, POST /auth/register operational end-to-end against real DB; AuthMiddleware verifies Bearer tokens; rate limiter enforces 5/min/IP on login; account-suspension hook consistently enforced.

| # | ID | Deliverable | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 21 | COMP-001 | Implement AuthService orchestrator | AuthService | COMP-002, COMP-004, COMP-008 | login/register/refresh/reset methods delegate to peers; returns domain DTOs only (never raw records); transactional where needed | L | P0 |
| 22 | FR-AUTH.1 | Implement login flow | AuthService | COMP-001, COMP-002, COMP-004 | valid creds→AuthTokenPair; invalid→AuthError(generic, no enum leak); locked→AuthError(suspended); last_login timestamp updated | M | P0 |
| 23 | API-001 | Expose `POST /auth/login` | RoutesRegistry | FR-AUTH.1, OPS-003 | 200 with token pair; 401 generic; 403 locked; 429 on rate-limit breach; request/response schema validated | M | P0 |
| 24 | FR-AUTH.2 | Implement registration flow | AuthService | COMP-001, COMP-004, COMP-008 | valid data→UserRecord created + 201 profile; duplicate email→AuthError(conflict); policy + email-format validated pre-hash | M | P0 |
| 25 | API-002 | Expose `POST /auth/register` | RoutesRegistry | FR-AUTH.2 | 201 with sanitized profile (no password_hash); 409 on duplicate email; 400 on policy/format violation; JSON schema locked | M | P0 |
| 26 | SEC-001 | Password policy validator | AuthService | — | enforces min 8 chars, ≥1 upper, ≥1 lower, ≥1 digit; returns structured error codes per rule; unit-tested boundary cases | S | P0 |
| 27 | SEC-002 | Email format validator | AuthService | — | RFC-5322 subset regex or library; rejects empty/TLD-less/control-char inputs; unit-tested against canonical valid/invalid corpora | S | P0 |
| 28 | COMP-005 | Implement AuthMiddleware | AuthMiddleware | COMP-002, COMP-003 | extracts Bearer token; invokes verify; attaches `req.user`; on invalid/expired→401; skipped for `/auth/*` public subset | M | P0 |
| 29 | OPS-003 | Rate limiter (5/min/IP on login) | AuthMiddleware | — | sliding-window or token-bucket; storage backend configurable; emits 429 with Retry-After; bypasses only for allowlisted internal IPs | M | P0 |
| 30 | COMP-017 | Implement account suspension hook | AccountLockPolicy | FR-AUTH.1, COMP-008 | locked account blocks login (403) and refresh (401); hook is forward-compatible with progressive lockout extension (GAP-1); centralized check invoked from login + refresh paths | S | P1 |
| 31 | TEST-M3-001 | Login happy-path integration test | AuthService | API-001, FR-AUTH.1 | returns 200 with valid JWT pair; access token decodes to correct sub; refresh token hash persisted | S | P0 |
| 32 | TEST-M3-002 | Login invalid-credentials test | AuthService | API-001 | 401 for wrong password and unknown email; identical response body (no enumeration); same latency within 10% band | S | P0 |
| 33 | TEST-M3-003 | Login locked-account test | AuthService | API-001, COMP-008, COMP-017 | is_locked=true user receives 403; access/refresh never issued; audit-log entry emitted | S | P0 |
| 34 | TEST-M3-004 | Registration duplicate-email test | AuthService | API-002 | second register with same email→409; UserRecord count unchanged; no partial insert | S | P0 |
| 35 | TEST-M3-005 | Rate-limit enforcement test | AuthMiddleware | OPS-003 | 6th attempt within 60s→429 with Retry-After; counter resets per IP after window | S | P0 |

### Integration Points — M3

| Artifact | Type | Wired | Milestone | Consumed By |
|---|---|---|---|---|
| AuthService | DI service | Registered at boot; consumed by route handlers | M3 | API-001, API-002 (M3); API-003–API-006 (M4/M5) |
| AuthMiddleware | Middleware chain entry | Registered in request pipeline ahead of protected routes | M3 | All protected routes including API-004 (M4) |
| Rate limiter | Middleware | Wrapped around `POST /auth/login` route | M3 | API-001 |
| Password policy validator | Strategy | Injected into register & reset-confirm paths | M3 | FR-AUTH.2 (M3), FR-AUTH.5 (M5) |
| Email format validator | Strategy | Injected into register & reset-request paths | M3 | FR-AUTH.2 (M3), FR-AUTH.5 (M5) |
| Account suspension hook | Strategy | Centralized check invoked from login + refresh | M3 | FR-AUTH.1, FR-AUTH.3 (M4); GAP-1 extension surface |

### Milestone Dependencies — M3

- M2 (COMP-002, COMP-003, COMP-004, NFR-AUTH.3).

### Milestone Risk Assessment — M3

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| User enumeration via timing or error-message differences | Medium | Medium | Identical response body for all 401 cases; constant-time compare via bcrypt; TEST-M3-002 asserts latency band |
| Rate limiter storage SPOF | Low | Medium | Use shared Redis or equivalent with failover; fail-open policy documented with audit-logging on degraded mode |
| Middleware ordering mistakes expose protected routes | Low | High | Integration test for each protected route verifies 401 without token; route-registry contract test enforces middleware order |
| Account-lock check missing on refresh path | Medium | High | COMP-017 centralizes check; TEST-M3-003 covers login; M4 includes refresh-path lock-state assertion |

## M4: Token Refresh & Profile

**Objective:** Complete the access-token lifecycle by adding refresh and profile. Replay detection is the single HIGH-severity security deliverable of this milestone. Refresh-cookie policy is promoted to an explicit SEC deliverable. | **Duration:** 2w (W7–W8) | **Entry:** M3 exit; AuthMiddleware verifying Bearer tokens; TokenManager rotation path unit-tested | **Exit:** `/auth/refresh` rotates tokens with replay detection; `/auth/me` returns sanitized profile; replay attempts invalidate all user tokens; refresh cookie contract asserted.

| # | ID | Deliverable | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 36 | FR-AUTH.3 | Implement token refresh flow | AuthService | COMP-002, COMP-009, COMP-017 | valid refresh→rotated AuthTokenPair; expired→401 force re-auth; replay of revoked→revokeAllForUser + 401; refresh hashes always SHA-256; locked-account refresh→401 | M | P0 |
| 37 | API-003 | Expose `POST /auth/refresh` | RoutesRegistry | FR-AUTH.3, SEC-007 | 200 with new pair; 401 for expired/replayed; refresh sourced from httpOnly cookie per constraints §3; new refresh set via Set-Cookie httpOnly+secure+sameSite | M | P0 |
| 38 | FR-AUTH.4 | Implement profile retrieval | AuthService | COMP-001, COMP-005, COMP-008 | valid Bearer→sanitized profile(id, email, display_name, created_at); expired/invalid→401; no password_hash, no refresh_token_hash ever returned | S | P0 |
| 39 | API-004 | Expose `GET /auth/me` | RoutesRegistry | FR-AUTH.4, COMP-005 | 200 with ProfileDTO; 401 without/invalid token; schema excludes sensitive fields by design; JSON schema contract-tested | S | P0 |
| 40 | SEC-003 | Refresh rotation + replay detection | TokenManager | COMP-002, COMP-009 | every refresh revokes old hash and issues new; replayed revoked hash→revokeAllForUser(userId)+audit event; race-safe via DB-row lock on token_hash | M | P0 |
| 41 | SEC-004 | Profile field sanitization contract | AuthService | FR-AUTH.4 | ProfileDTO mapper defined; serializer has allowlist not denylist; sensitive-field regression test over response JSON | S | P0 |
| 42 | SEC-007 | Refresh token httpOnly cookie policy | RefreshCookiePolicy | API-003 | refresh token returned only in Set-Cookie with HttpOnly+Secure+SameSite=Strict; Path=/auth; Max-Age=7d; no localStorage/sessionStorage emission path; browser-storage fallback explicitly forbidden in code + lint rule | S | P0 |
| 43 | TEST-M4-001 | Refresh rotation integration test | TokenManager | FR-AUTH.3, API-003 | refresh issues new pair; old refresh cannot be reused; audit entry on rotation | S | P0 |
| 44 | TEST-M4-002 | Replay-detection integration test | TokenManager | SEC-003 | replay of revoked refresh triggers revokeAllForUser; all active refresh tokens for user marked revoked; subsequent refreshes/API calls→401 | M | P0 |
| 45 | TEST-M4-003 | Profile no-leak regression test | AuthService | FR-AUTH.4, SEC-004 | response JSON keys match ProfileDTO allowlist exactly; `password_hash`, `token_hash`, `is_locked` never serialized | S | P0 |

### Integration Points — M4

| Artifact | Type | Wired | Milestone | Consumed By |
|---|---|---|---|---|
| TokenManager.refresh | Callback from AuthService | Injected into AuthService refresh method | M4 | API-003 |
| ProfileDTO mapper | Serializer strategy | Registered on AuthService; allowlist-only | M4 | API-004 |
| Replay-detection audit event | Event binding | TokenManager emits event; logger subscribes | M4 | Admin dashboard, audit log (GAP-2 handoff) |
| Refresh cookie writer | Middleware/response binding | AuthService returns SetCookieIntent; writer applies HttpOnly+Secure+SameSite | M4 | API-001 login (first issuance), API-003 refresh |
| DB row-lock on token_hash | Concurrency control | Acquired inside TokenManager.refresh transaction | M4 | SEC-003 race-safe rotation |

### Milestone Dependencies — M4

- M3 (COMP-001, COMP-005, COMP-017).

### Milestone Risk Assessment — M4

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Race condition allows two valid refresh pairs from one parent | Medium | High | DB-row lock on refresh_tokens.token_hash; TEST-M4-002 includes concurrent refresh scenario |
| Profile endpoint leaks sensitive fields after schema evolution | Medium | High | ProfileDTO allowlist serializer; TEST-M4-003 regression guard; PR gate enforces DTO review |
| httpOnly cookie misconfiguration on refresh exposes token to JS | Low | High | SEC-007 explicit contract; integration test asserts Set-Cookie attributes include HttpOnly+Secure+SameSite; OWASP header lint in CI |

## M5: Password Reset Flow

**Objective:** Close the last FR by delivering the reset flow with correct email dispatch, 1h token TTL, single-use enforcement, and post-reset token invalidation. OI-1 reset-dispatch mode is resolved as the first scheduled deliverable of this milestone. | **Duration:** 2w (W9–W10) | **Entry:** M4 exit; email provider decided (OI-7); kickoff day reserved for OI-1 decision | **Exit:** reset request generates email; confirmation endpoint accepts valid token and invalidates all refresh tokens; dispatch mode documented in an ADR.

| # | ID | Deliverable | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 46 | OI-1-DEC | Resolve reset-email dispatch mode (sync vs queue) | Architecture ADR | — | decision scheduled at M5 day 1; ADR records latency trade-off vs NFR-AUTH.1 and resilience vs email-provider outage (R11); decision binds COMP-010 and API-005 design | S | P0 |
| 47 | FR-AUTH.5 | Implement password reset flow | AuthService | COMP-001, COMP-002, COMP-004, COMP-010, OI-1-DEC | registered email→reset token(1h)+email dispatched; valid token→new password stored + reset token invalidated; expired/invalid→400; successful reset→revokeAllForUser | L | P0 |
| 48 | API-005 | Expose `POST /auth/password-reset` | RoutesRegistry | FR-AUTH.5 | always 202 whether email known or not (no enumeration); rate-limited per IP; reset token hash stored, plaintext emailed once | M | P0 |
| 49 | API-006 | Expose `POST /auth/password-reset/confirm` | RoutesRegistry | FR-AUTH.5 | valid reset-token+new password meeting SEC-001→200; invalid/expired→400; token single-use (revoked after success); refresh tokens for user revoked | M | P0 |
| 50 | COMP-010 | EmailService adapter | EmailService | DEP-003, OI-1-DEC | send(reset-email-template, recipient, token-link); retries on transient failure; failures do not leak recipient existence in response; dispatch mode per OI-1-DEC (sync call or queue publish) | M | P0 |
| 51 | DEP-003 | Select & integrate email provider | EmailService | OI-7 | provider decision documented (SendGrid/SES/SMTP); API key in secrets manager; sandbox creds for non-prod; SPF/DKIM/DMARC configured | M | P0 |
| 52 | SEC-005 | Reset token TTL + single-use enforcement | AuthService | FR-AUTH.5 | token stored as SHA-256 hash; `expires_at` = now+1h; consumed-flag set atomically with password update; replay after success→400 | M | P0 |
| 53 | SEC-006 | Invalidate-all refresh on reset | AuthService | SEC-005, COMP-009 | after successful password update, revokeAllForUser invoked in same transaction; TEST-M5-003 verifies active sessions terminated | S | P0 |
| 54 | TEST-M5-001 | Reset email dispatch integration test | EmailService | API-005, COMP-010 | request for known email→email provider mock invoked with correct template+link; request for unknown email→202 with no provider call; timing parity assertion | S | P0 |
| 55 | TEST-M5-002 | Reset token expiry test | AuthService | SEC-005 | token used at 59m→accepted; at 61m→400; invalid random token→400; reused after success→400 | S | P0 |
| 56 | TEST-M5-003 | Reset invalidates all refresh tokens | AuthService | SEC-006 | prior refresh tokens issued; reset succeeds; attempt to refresh with old refresh→401; new login required | S | P0 |

### Integration Points — M5

| Artifact | Type | Wired | Milestone | Consumed By |
|---|---|---|---|---|
| EmailService | DI service | Registered at boot; env decides sandbox vs prod credentials | M5 | AuthService reset flow |
| Reset token store | Repository extension | Dedicated `reset_tokens` table (chosen to separate single-use semantics from refresh rotation) | M5 | AuthService reset flow |
| Reset email template | Config asset | Owned by product + ops; version-controlled | M5 | EmailService |
| Dispatch-mode strategy | Strategy pattern | Sync-call vs queue-publish selected per OI-1-DEC | M5 | COMP-010 EmailService |

### Milestone Dependencies — M5

- M3 (COMP-001 AuthService, SEC-001 password policy).
- M4 (SEC-003 replay detection — reset flow relies on revokeAllForUser path).

### Milestone Risk Assessment — M5

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Email dispatch latency breaks <200ms p95 SLO for reset endpoint | Medium | Medium | OI-1-DEC: queue dispatch asynchronously so API-005 returns 202 immediately; NFR-AUTH.1 measured only on sync path |
| Account enumeration via differential responses on reset request | Medium | Medium | API-005 always returns 202 and identical body; timing parity enforced via TEST-M5-001 fixture |
| Reset token leaks in logs (token in URL querystring logged) | Medium | High | Token delivered in URL path fragment or POST body; logging middleware redacts auth-related query params; review log sinks |

## M6: Wiring, Rollout & Validation

**Objective:** Wire the finished components into the request pipeline, ship behind a flag, close both NFRs with real measurement, and hand off deferred scope with named owners. No new business logic — this milestone is integration, observability, validation, and v1.1 handoff only. | **Duration:** 2w (W11–W12) | **Entry:** M5 exit; all flows implemented and unit-tested | **Exit:** `AUTH_SERVICE_ENABLED` flag toggles `/auth/*` routing; APM+PagerDuty in place; k6 confirms <200ms p95; E2E lifecycle test green; rollback rehearsed; GAP-1/2/3 v1.1 plans owned; go-live checklist signed off.

| # | ID | Deliverable | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 57 | COMP-006 | Register `/auth/*` routes in RoutesRegistry | RoutesRegistry | API-001, API-002, API-003, API-004, API-005, API-006 | route group added to `src/routes/index.ts`; gated by AUTH_SERVICE_ENABLED; route inventory doc updated | S | P0 |
| 58 | OPS-002 | Implement `AUTH_SERVICE_ENABLED` feature flag | RoutesRegistry | COMP-006 | flag backed by config system supporting runtime toggle; false→/auth/* routes return 404 (or pass-through); true→routes active | S | P0 |
| 59 | OPS-005 | Wire APM + PagerDuty for auth service | Observability | — | APM instruments AuthService latency per flow; PagerDuty escalation policy binds to health-check failure; SLO dashboard published | M | P0 |
| 60 | OPS-009 | Health endpoint with dependency status | Observability | OPS-005, DEP-004, DEP-003 | `GET /health/auth` returns 200 when secrets-manager reachable, DB reachable, email-provider reachable (or degraded-mode); 503 otherwise; JSON body lists per-dependency status keys:{keys,db,email}; probed every 30s | S | P0 |
| 61 | DEP-004 | Secrets manager operational readiness | JwtService, EmailService | OPS-001, OPS-004, DEP-003 | prod secrets provisioned and rotated once in staging; IAM policies audited; break-glass recovery doc written | S | P0 |
| 62 | DEP-005 | APM + Uptime + PagerDuty operational | Observability | OPS-005 | synthetic probes hitting `/auth/login` (canary user) and `/auth/me`; uptime calculated from probe success; alert routes verified in drill | S | P0 |
| 63 | NFR-AUTH.1 | Validate latency <200ms p95 under load | AuthService | All auth endpoints, OPS-005 | k6 load test sustained 50 rps for 10 min across /login and /refresh; p95<200ms; results archived; APM dashboard confirms in prod shadow window | M | P0 |
| 64 | NFR-AUTH.2 | Validate 99.9% availability SLO | Observability | OPS-005, DEP-005, OPS-009 | 30-day rolling uptime≥99.9% in staging soak; incident runbook reviewed; PagerDuty on-call rota activated | M | P0 |
| 65 | TEST-M6-001 | E2E user lifecycle test | AuthService | All API endpoints | register→login→GET /me→refresh→password-reset→login-with-new-password passes with expected status codes; old refresh tokens invalid after reset | M | P0 |
| 66 | TEST-M6-002 | Feature-flag rollback test | RoutesRegistry | OPS-002 | toggle flag off during active traffic; new requests return expected fallback; in-flight requests complete without error; toggle back on restores service | S | P0 |
| 67 | OPS-007 | Publish rollout runbook + rollback procedure | Operations | OPS-002, OPS-005 | runbook covers phase-1 coexistence, phase-2 mandatory-auth cutover, flag rollback, key-rotation break-glass; signed off by SRE | S | P1 |
| 68 | OPS-008 | Go-live checklist (phase-1→phase-2 cutover) | Operations | OPS-007, NFR-AUTH.1, NFR-AUTH.2, TEST-M6-001 | explicit checklist deliverable (not just a runbook section); entries for monitoring green, synthetic probes green, rollback rehearsed, stakeholder sign-offs captured; phase-1 validation evidence linked; phase-2 cutover date captured | S | P0 |
| 69 | GAP-1 | v1.1 progressive account lockout plan | Security backlog | COMP-017, OPS-003 | plan document enumerates threshold schedule, escalation (temporary→permanent lock), integration points with COMP-017; owner: Security Lead; target: v1.1 sprint 1; ADR filed | S | P1 |
| 70 | GAP-2 | v1.1 audit logging schema + retention plan | Audit/Architecture | SEC-003, SEC-005, SEC-006 | plan document enumerates event types, JSON schema, sink (e.g., structured log + append-only store), retention window, compliance sign-off path; owner: Architect; target: v1.1 sprint 1; ADR filed | S | P1 |
| 71 | GAP-3 | v1.1 deletion/deactivation token revocation plan | Identity lifecycle | COMP-001, COMP-009 | plan document specifies admin-dashboard manual workaround for v1, automated revocation hook for v1.1, integration with user deletion/deactivation workflow; owner: Product + Architect; target: v1.1 sprint 2 | S | P1 |

### Integration Points — M6

| Artifact | Type | Wired | Milestone | Consumed By |
|---|---|---|---|---|
| RoutesRegistry | Route table dispatch | Registers handler per API-00x inside `/auth/*` group at boot | M6 | Request pipeline |
| AUTH_SERVICE_ENABLED flag | Config flag (strategy pattern) | Read at route registration; recheck per-request on hot-reload | M6 | RoutesRegistry, tests |
| APM latency instrumentation | Middleware + in-service timers | Wrapped around each AuthService method and route handler | M6 | Observability dashboards |
| PagerDuty escalation | Event binding | Health-check failure → PagerDuty REST API event-create | M6 | On-call rota |
| Health endpoint | Monitoring binding | `/health/auth` reflects secrets/DB/email dependency status | M6 | Uptime probes, PagerDuty |
| Admin dashboard integration | Operational callback | Revoke-token / lock-account actions call AuthService admin methods | M6 | Ops team (per constraints §11: no CLI); GAP-3 manual workaround |
| Go-live checklist | Release workflow gate | Phase-1→phase-2 transition gated by checklist evidence | M6 | Release manager, SRE |

### Milestone Dependencies — M6

- M3 (API-001, API-002).
- M4 (API-003, API-004, SEC-007).
- M5 (API-005, API-006).

### Milestone Risk Assessment — M6

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Flag rollback leaves orphaned sessions | Low | Medium | Rollback runbook (OPS-007) + go-live checklist (OPS-008) cover session handling; flag off only serves 404, never invalid tokens; clients handle 404 as re-auth |
| Latency SLO fails under production load despite k6 pass | Medium | Medium | Canary deploy with 5% traffic first; APM watches p95 for 24h; rollback via OPS-002 flag if SLO breach detected |
| Availability SLO missed due to secrets manager outage | Low | High | Cache RSA keys in-memory on JwtService init; OPS-009 reports degraded mode; incident runbook documents break-glass |
| Deferred gaps forgotten after release | Medium | Medium | GAP-1/2/3 are owned deliverables with named owners + target sprints; ADRs filed; roadmap re-review at v1.1 kickoff |

## Risk Assessment and Mitigation

| # | Risk | Severity | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|---|---|
| R1 | JWT private key compromise allows forged tokens | HIGH | Low | High | RS256 asymmetric keys; secrets manager storage (OPS-004); 90-day rotation (OPS-006); kid-based overlap rotation | Architect / Security |
| R2 | Refresh token replay after theft | HIGH | Medium | High | Rotation on every refresh + replay detection (SEC-003); SHA-256 hash storage; revokeAllForUser on suspicious reuse | Architect |
| R3 | bcrypt cost factor too low for future hardware | MEDIUM | Low | Medium | Configurable cost; annual OWASP review; Argon2id migration path on backlog | Security |
| R4 | No progressive account lockout in v1 (deferred) | MEDIUM | Medium | Medium | Rate-limit (OPS-003) + COMP-017 suspension hook cover short-window attack; GAP-1 owns v1.1 progressive lockout with ADR | Security Lead |
| R5 | Token revocation on user deletion not fully automated in v1 | MEDIUM | Low | Medium | Admin dashboard manual workaround (GAP-3); automated hook in v1.1 with named owner | Product + Architect |
| R6 | User enumeration via differential responses | MEDIUM | Medium | Medium | Identical 401 response body for login; 202 response for reset-request; timing parity assertions in tests | Security |
| R7 | httpOnly cookie misconfiguration exposes refresh to JS | HIGH | Low | High | SEC-007 explicit cookie-policy deliverable; contract tests on Set-Cookie flags; OWASP header lint in CI | Backend |
| R8 | Migration lacks reversible down-script | HIGH | Low | High | Constraint §12 mandates down-migration; CI job asserts down-then-up idempotence | DevOps |
| R9 | Reset token leaks via logs | HIGH | Medium | High | Token in POST body only; log-redaction middleware; log-sink review before rollout | Security |
| R10 | Latency SLO breach under production load | MEDIUM | Medium | Medium | k6 pre-validation (NFR-AUTH.1); canary 5% deploy with APM watch; flag rollback path | SRE |
| R11 | Email dispatch outage blocks password reset | MEDIUM | Medium | Medium | OI-1-DEC resolves sync vs queue dispatch at M5 kickoff; async queue default; provider fallback documented | Backend |
| R12 | Audit logging schema not defined in v1 | MEDIUM | High | Medium | Emit audit events from SEC-003, SEC-005, SEC-006 to structured log sink now; GAP-2 formalizes schema + retention with named owner for v1.1 | Architect + Compliance |
| R13 | Scope creep pulling OAuth/MFA/RBAC into v1 | MEDIUM | Medium | Medium | Constraint §10 explicitly out-of-scope; ADR records deferral; change-control gate on scope additions | PM |

## Resource Requirements and Dependencies

### External Dependencies

| Dependency | Required By Milestone | Status | Fallback |
|---|---|---|---|
| `jsonwebtoken` library (DEP-001) | M1 (pin), M2 (use) | Stable upstream | Pin to last-known-good; internal fork if licence change |
| `bcrypt` library (DEP-002) | M1 (pin), M2 (use) | Stable upstream; native build | `bcryptjs` as pure-JS fallback (document perf delta) |
| Email service provider (DEP-003) | M5 | Selection pending (OI-7) | SMTP fallback via internal relay; document delivery SLA trade-off |
| Secrets manager (OPS-004, DEP-004) | M1 (integrate), M6 (operational) | Assumed available (AWS Secrets Manager or equiv) | Encrypted file-based secret with strict IAM (non-prod only) |
| APM + Uptime + PagerDuty (OPS-005, DEP-005) | M6 | Platform-level dependency | Stack-local Prometheus + Alertmanager as interim |
| Redis or equivalent rate-limit store (OPS-003) | M3 | Platform-level dependency | Process-local counter (non-prod only; document SPOF) |

### Infrastructure Requirements

- Postgres (or equivalent) with FK + unique-index support for the new `users`, `refresh_tokens`, and `reset_tokens` tables (COMP-007).
- Secrets manager with per-identity IAM policies scoped to the auth service (OPS-004).
- Redis or equivalent shared store for the rate limiter (OPS-003).
- APM agent runtime installed in service container (OPS-005).
- CI runner with Postgres container for migration and repository integration tests (TEST-M1-001, TEST-M1-002).
- Load-testing environment capable of 50 rps sustained (NFR-AUTH.1 validation via k6).
- Email provider sandbox credentials for non-prod environments (DEP-003).
- PagerDuty service or equivalent alert routing for auth incidents (DEP-005).

## Success Criteria and Validation Approach

| Criterion | Metric | Target | Validation Method | Milestone |
|---|---|---|---|---|
| FR-AUTH.1 login correctness | Status code + token pair validity | 200/401/403/429 per matrix | Integration tests TEST-M3-001/002/003/005 + manual smoke | M3 |
| FR-AUTH.2 registration correctness | Status code + DB record + password policy | 201/400/409 per matrix | Integration tests TEST-M3-004 + policy unit tests (SEC-001/002) | M3 |
| FR-AUTH.3 refresh + replay detection | Token rotation + replay→revokeAll | New pair issued; replay→full invalidation | TEST-M4-001, TEST-M4-002 | M4 |
| FR-AUTH.4 profile no-leak | Response schema | Allowlist-only fields returned | TEST-M4-003 contract test + static DTO review | M4 |
| FR-AUTH.5 reset correctness | Token TTL + single-use + invalidation | 1h TTL; single-use; refresh revoked post-reset | TEST-M5-001/002/003 | M5 |
| Refresh cookie policy (SEC-007) | Set-Cookie attributes | HttpOnly+Secure+SameSite=Strict on every refresh emission | Integration assertion + header lint | M4 |
| Account lock enforcement (COMP-017) | Status code on login + refresh with locked user | 403 login, 401 refresh; no token issuance | TEST-M3-003 + M4 refresh-lock assertion | M3, M4 |
| NFR-AUTH.1 latency | p95 latency across auth endpoints | <200ms under sustained 50 rps | k6 report + APM 24h production shadow | M6 |
| NFR-AUTH.2 availability | Uptime (monthly) | ≥99.9% | Uptime-probe aggregation + PagerDuty incident log review | M6 |
| NFR-AUTH.3 password hashing | bcrypt cost factor + hash latency | cost=12; 200–300ms p50 | Unit test (cost prefix) + benchmark test (TEST-M2-002) | M2 |
| Health endpoint (OPS-009) | Dependency status accuracy | 200 when keys+DB+email OK; 503 otherwise | Dependency-failure integration tests | M6 |
| E2E user lifecycle | Register→login→me→refresh→reset→login-new-pwd | All steps green; old credentials invalidated | TEST-M6-001 | M6 |
| v1.1 handoff quality (GAP-1/2/3) | Owned plan + ADR + target sprint | Each GAP has named owner and v1.1 sprint target | Roadmap review at release + ADR repository check | M6 |

## Decision Summary

| Decision | Chosen | Alternatives Considered | Rationale |
|----------|--------|------------------------|----------|
| Token format | RS256 JWT | HS256 JWT; opaque tokens with server store; PASETO | Mandated by constraints §1; RS256 supports verifier distribution without sharing private key |
| Password hashing | bcrypt cost 12 | Argon2id; scrypt | Mandated by constraints §2; bcrypt has mature ecosystem and known ~250ms target on reference hardware |
| Refresh token client storage | httpOnly+Secure+SameSite cookie | localStorage; sessionStorage; opaque server session | Mandated by constraints §3; SEC-007 promotes cookie policy to explicit deliverable; constraints §4 forbids server-side session store |
| Refresh token server storage | SHA-256 hash in `refresh_tokens` table | Plaintext; encrypted-at-rest plaintext | Spec acceptance criteria on FR-AUTH.3; hash prevents DB-leak-enables-replay |
| Session strategy | Stateless JWT | Server-side session store | Mandated by constraints §4; enables horizontal scaling without session stickiness |
| Refresh rotation policy | Rotate on every refresh + replay detection | Long-lived refresh; no rotation | Mandated by constraints §5; mitigates HIGH-severity risk R2 |
| Key storage | Secrets manager with 90-day rotation | Environment variables; config files; KMS-only | Mandated by constraints §6; mitigates HIGH-severity risk R1; supports auditability |
| Component layering | AuthService → TokenManager → JwtService + PasswordHasher peer | Monolithic AuthController; flat services | Mandated by constraints §7; each layer testable in isolation and swappable |
| Rollout strategy | Feature-flag gated with phase-1 coexistence | Big-bang cutover; blue/green only | Mandated by constraints §8–§9; rollback via flag toggle is lowest-blast-radius |
| Milestone count & duration | 6 milestones, 12 weeks | 4 milestones / 8 weeks (Haiku variant, scored 70 vs Opus 78); 5 milestones / 10 weeks (debate synthesis suggestion) | Base-selection scored Opus 78 vs Haiku 70; debate LEANS OPUS on refresh/reset decoupling (C4) and OI-7 gating (C6); 12w preserves P0/P1 isolation and dedicated rollout milestone |
| Refresh + reset milestone isolation | Reset in M5, independent of Refresh in M4 | Bundle refresh + reset in one milestone (Haiku) | Debate LEANS OPUS on C4; if P1 reset slips, P0 refresh still ships; revoke-all contract is exercised first in M4 replay path and consumed in M5 reset |
| GAP handling (lockout, audit, deletion) | Owned deliverables GAP-1/2/3 in M6 with named owners + ADRs | Risk-register entries only (Opus original) | Debate LEANS HAIKU on C5; Haiku's owned deliverables reduce forget-risk at negligible capacity cost |
| OI-1 resolution timing | Scheduled as M5 kickoff deliverable (OI-1-DEC) | Pre-M1 blocker (Opus original); in-flight during M3 (Haiku) | Hybrid: earlier than Haiku (prevents COMP-010 rework), later than Opus (unblocks earlier milestones); OI-1-DEC ADR is first M5 deliverable |
| OI-7 resolution timing | Hard gate before M5 | Accept in-flight (Haiku) | Debate LEANS OPUS on C6; email-provider choice binds DEP-003 + COMP-010 contracts |
| v1 scope exclusions | OAuth/MFA/RBAC deferred to v2.0 | Include minimal MFA now | Constraint §10 fixes scope |
| Admin surface | Admin dashboard only (no CLI) | CLI scripts; runbook-only | Mandated by constraints §11; dashboard already exists as operational surface |
| Email delivery mode | Decision deferred to OI-1-DEC (default: async queue) | Synchronous dispatch | Keeps API-005 under NFR-AUTH.1 p95 SLO; isolates email provider outages from auth uptime (mitigates R11) |
| Reset token store | Dedicated `reset_tokens` table | Reuse `refresh_tokens` table | Separation prevents accidental replay-detection entanglement; revocation semantics differ (single-use vs rotate) |
| Security ID scheme | SEC-001…SEC-007 | COMP-011…COMP-018 (Haiku rename) | Debate marks as cosmetic; SEC-xxx scheme preserved for 1:1 compliance traceability |

## Timeline Estimates

| Milestone | Duration | Start | End | Key Milestones |
|---|---|---|---|---|
| M1 | 2 weeks | Week 1 | Week 2 | DB migration green; repositories tested; RSA keys in secrets manager |
| M2 | 2 weeks | Week 3 | Week 4 | JwtService + PasswordHasher unit-tested; TokenManager rotation verified; bcrypt benchmark banded |
| M3 | 2 weeks | Week 5 | Week 6 | Login + Register endpoints live against real DB; AuthMiddleware verifies Bearer; rate limiter enforced; account-lock hook centralized |
| M4 | 2 weeks | Week 7 | Week 8 | Refresh rotation + replay detection operational; GET /auth/me returns sanitized profile; SEC-007 cookie policy asserted |
| M5 | 2 weeks | Week 9 | Week 10 | OI-1-DEC ADR filed; reset request + confirm endpoints; reset token TTL + single-use enforced; refresh tokens invalidated on reset |
| M6 | 2 weeks | Week 11 | Week 12 | Routes wired behind AUTH_SERVICE_ENABLED; APM+PagerDuty live; NFR-AUTH.1 & NFR-AUTH.2 validated; go-live checklist signed; GAP-1/2/3 v1.1 plans owned |

**Total estimated duration:** 12 weeks (3 calendar months), sequential with gated handoffs; no parallel milestone tracks assumed for v1.

## Open Questions

| # | Question | Impact | Blocking Milestone | Resolution Owner |
|---|---|---|---|---|
| OI-1 | Password reset emails: synchronous dispatch vs message queue? | Reset endpoint latency SLO (NFR-AUTH.1) + resilience to email-provider outages (R11) | M5 (scheduled as OI-1-DEC deliverable at M5 kickoff) | Architect + Backend lead |
| OI-2 | Maximum concurrent active refresh tokens per user? | Storage growth; multi-device UX; revoke-all semantics | Not blocking v1 (accepted as in-flight decision at M4 kickoff per Haiku improvement); enforceable change in v1.1 if deferred | Architect + Product |
| OI-6 | Endpoint paths for register/refresh/password-reset (only /auth/login and /auth/me verbatim in spec) | API contract stability; consumer integration | M2 (contract lock before M3 implementation) | Product + Architect |
| OI-7 | Email provider selection (SendGrid/SES/SMTP) and template ownership | Blocks DEP-003 and COMP-010 | M5 (hard gate — must resolve before sprint kickoff) | Product + DevOps |
| GAP-1 | Progressive account lockout threshold after N failed attempts (v1.1 scope)? | Partial coverage of brute-force attack (R4); v1 ships rate-limit + COMP-017 hook only | Not blocking v1; owned deliverable in M6; target v1.1 sprint 1 | Security Lead |
| GAP-2 | Audit logging schema and retention policy for auth events (v1.1 scope)? | Forensic readiness (R12); compliance | Not blocking v1; owned deliverable in M6; target v1.1 sprint 1 | Architect + Compliance |
| GAP-3 | Token revocation behavior on user deletion / deactivation (v1.1 scope)? | Ghost sessions after account removal (R5) | Not blocking v1; owned deliverable in M6; manual workaround via admin dashboard in v1; target v1.1 sprint 2 | Architect + Product |

