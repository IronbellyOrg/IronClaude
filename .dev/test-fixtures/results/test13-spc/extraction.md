---
spec_source: test-spec-user-auth.compressed.md
generated: 2026-04-17T00:00:00Z
generator: requirements-extraction-agent
functional_requirements: 5
nonfunctional_requirements: 3
total_requirements: 8
complexity_score: 0.6
complexity_class: MEDIUM
domains_detected: [backend, security, database]
risks_identified: 3
dependencies_identified: 5
success_criteria_count: 8
extraction_mode: standard
pipeline_diagnostics: {elapsed_seconds: 69.0, started_at: "2026-04-17T01:17:28.392154+00:00", finished_at: "2026-04-17T01:18:37.401016+00:00"}
---

## Functional Requirements

### FR-AUTH.1: User Login
**Description**: Authenticate users via email and password, returning JWT access token and refresh token upon successful credential verification.
**Endpoint**: `POST /auth/login`
**Acceptance Criteria**:
- Valid credentials → 200 with access_token (15min TTL) + refresh_token (7d TTL)
- Invalid credentials → 401 with generic error (no enumeration of email vs password)
- Locked account → 403 indicating suspension
- Rate-limit: 5 attempts/minute per IP
**Dependencies**: PasswordHasher, TokenManager, User database table

### FR-AUTH.2: User Registration
**Description**: Register new users with input validation, hashed password storage, and confirmation response.
**Endpoint**: (implied) `POST /auth/register` under `/auth/*` route group
**Acceptance Criteria**:
- Valid data (email, password, display name) → 201 with user profile
- Duplicate email → 409 conflict
- Password policy: min 8 chars, ≥1 uppercase, ≥1 lowercase, ≥1 digit
- Email format validation before registration
**Dependencies**: PasswordHasher, User database table

### FR-AUTH.3: Token Refresh
**Description**: Issue and refresh JWT tokens, allowing new access_token via valid refresh_token without re-authentication.
**Endpoint**: (implied) `POST /auth/refresh` under `/auth/*` route group
**Acceptance Criteria**:
- Valid refresh_token → new access_token + rotated refresh_token
- Expired refresh_token → 401, force re-authentication
- Rotated (revoked) refresh_token replay → invalidate all user tokens (replay detection)
- Refresh token hashes stored in DB for revocation
**Dependencies**: TokenManager, JwtService, RefreshToken database table

### FR-AUTH.4: Profile Retrieval
**Description**: Return authenticated user's profile data for valid access token.
**Endpoint**: `GET /auth/me`
**Acceptance Criteria**:
- Valid Bearer access_token → profile (id, email, display_name, created_at)
- Expired/invalid token → 401
- Never expose password_hash or refresh_token_hash
**Dependencies**: TokenManager, User database table

### FR-AUTH.5: Password Reset
**Description**: Secure password reset flow via time-limited token dispatched over email.
**Endpoint**: (implied) `POST /auth/password-reset` and `POST /auth/password-reset/confirm` under `/auth/*` route group
**Acceptance Criteria**:
- Registered email → generate reset token (1h TTL) + dispatch email
- Valid reset token → allow new password + invalidate reset token
- Expired/invalid reset token → 400 with error
- Successful reset → invalidate all existing refresh tokens
**Dependencies**: TokenManager, PasswordHasher, Email service (external)

## Non-Functional Requirements

### NFR-AUTH.1: Authentication Latency
**Target**: < 200ms p95 under normal load
**Measurement**: k6 load testing; p95 latency monitored in production APM
**Domain**: Performance

### NFR-AUTH.2: Service Availability
**Target**: 99.9% uptime (< 8.76h downtime/year)
**Measurement**: Health check endpoint + uptime monitoring; PagerDuty alerting
**Domain**: Reliability

### NFR-AUTH.3: Password Hashing Security
**Target**: bcrypt cost factor 12 (~250ms per hash)
**Measurement**: Unit test verifying cost factor; benchmark test for hash timing
**Domain**: Security

## Complexity Assessment

**Complexity Score**: 0.6 (MEDIUM)

**Scoring Rationale**:
| Factor | Weight | Score | Notes |
|---|---|---|---|
| Functional breadth | 0.20 | 0.6 | 5 FRs covering login, register, refresh, profile, reset |
| Security sensitivity | 0.25 | 0.8 | Crypto operations (JWT RS256, bcrypt), replay detection, rate limiting |
| Integration surface | 0.15 | 0.4 | 2 DB tables, 1 external email service, middleware wiring |
| Data model complexity | 0.15 | 0.4 | 3 interfaces, FK relationships, hashing fields |
| Cryptographic rigor | 0.15 | 0.8 | RS256 asymmetric signing, bcrypt cost 12, SHA-256 hashing, token rotation |
| Operational concerns | 0.10 | 0.5 | Feature flag rollout, migrations with down-scripts, key rotation |

**Net Assessment**: MEDIUM complexity — bounded scope with 5 FRs but elevated security rigor drives the score above typical CRUD features. Scope explicitly excludes OAuth, MFA, and RBAC, keeping surface manageable.

## Architectural Constraints

1. **Token format mandated**: JWT with RS256 asymmetric signing (no HS256, no opaque tokens, no PASETO)
2. **Password hashing mandated**: bcrypt with cost factor 12 (no Argon2id, no scrypt in v1)
3. **Token storage pattern**: Access token in memory; refresh token in httpOnly cookie (no localStorage/sessionStorage)
4. **Session strategy**: Stateless JWT — no server-side session store permitted
5. **Refresh rotation required**: Every refresh MUST invalidate prior refresh_token and detect replay
6. **Key management**: Private RSA key must reside in secrets manager; 90-day rotation cadence
7. **Layered architecture**: AuthService → TokenManager → JwtService; PasswordHasher as peer utility; all components injectable and independently testable
8. **Feature-flag rollout**: `AUTH_SERVICE_ENABLED` flag gates routing; rollback via flag toggle
9. **Backwards compatibility**: Existing unauthenticated endpoints remain functional during phase 1; auth becomes required in phase 2
10. **Out of scope (v1)**: OAuth2/OIDC federation, MFA, RBAC, social login — deferred to v2.0
11. **No CLI surface**: Administrative operations handled via existing admin dashboard
12. **Database migration convention**: Migration `003-auth-tables.ts` must include down-migration scripts

## Component Inventory

### Services / Modules

| ID | Name | Source Path | Role | Dependencies | Source Reference |
|---|---|---|---|---|---|
| COMP-001 | AuthService | `src/auth/auth-service.ts` | Core orchestrator coordinating login, register, refresh, reset flows | TokenManager, PasswordHasher, User repository | §4.1, §4.4 |
| COMP-002 | TokenManager | `src/auth/token-manager.ts` | JWT lifecycle management — issues, refreshes, revokes token pairs | JwtService, RefreshToken repository | §4.1, §4.4 |
| COMP-003 | JwtService | `src/auth/jwt-service.ts` | Low-level JWT signing/verification using RS256 | `jsonwebtoken` library, RSA key pair | §4.1, §4.4 |
| COMP-004 | PasswordHasher | `src/auth/password-hasher.ts` | bcrypt password hashing and comparison with configurable cost factor | `bcrypt` library | §4.1, §4.4 |
| COMP-005 | AuthMiddleware | `src/middleware/auth-middleware.ts` | Bearer token extraction and verification for request pipeline | TokenManager (via AuthService) | §4.2, §4.4 |
| COMP-006 | RoutesRegistry | `src/routes/index.ts` | Registers `/auth/*` route group | AuthService, AuthMiddleware | §4.2 |
| COMP-007 | AuthTablesMigration | `src/database/migrations/003-auth-tables.ts` | DB migration adding users + refresh_tokens tables with down-scripts | Migration framework | §4.2, §9 |
| COMP-008 | UserRepository | (implied) | Persistence abstraction for UserRecord CRUD | Database | §3 (DPN), §4.5 |
| COMP-009 | RefreshTokenRepository | (implied) | Persistence abstraction for RefreshTokenRecord CRUD and revocation | Database | §3 (FR-AUTH.3 DPN), §4.5 |
| COMP-010 | EmailService | (external) | Dispatches password reset emails | External SMTP/email provider | §3 (FR-AUTH.5 DPN) |

### Data Models

| ID | Name | Source Reference | Fields |
|---|---|---|---|
| DM-001 | UserRecord | §4.5 | `id: string (UUID v4)`, `email: string (unique, indexed)`, `display_name: string`, `password_hash: string (bcrypt)`, `is_locked: boolean`, `created_at: Date`, `updated_at: Date` |
| DM-002 | RefreshTokenRecord | §4.5 | `id: string (UUID v4)`, `user_id: string (FK → UserRecord.id)`, `token_hash: string (SHA-256)`, `expires_at: Date`, `revoked: boolean`, `created_at: Date` |
| DM-003 | AuthTokenPair | §4.5 | `access_token: string (JWT, 15min TTL)`, `refresh_token: string (opaque, 7d TTL)` |

## Risk Inventory

1. **JWT secret key compromise allows forged tokens** — Severity: HIGH (probability low, impact high)
   - *Mitigation*: RS256 asymmetric keys; private key in secrets manager; 90-day key rotation
2. **Refresh token replay attack after token theft** — Severity: HIGH (probability medium, impact high)
   - *Mitigation*: Refresh token rotation with replay detection; revoke all user tokens on suspicious reuse
3. **bcrypt cost factor too low for future hardware** — Severity: MEDIUM (probability low, impact medium)
   - *Mitigation*: Configurable cost factor; annual OWASP review; migration path to Argon2id
4. **(GAP-1) No progressive account lockout policy** — Severity: MEDIUM (from §12)
   - *Mitigation*: Rate-limit addresses partial risk; expand to progressive lockout in v1.1
5. **(GAP-3) Token revocation on user deletion not addressed** — Severity: MEDIUM (from §12)
   - *Mitigation*: Deferred to v1.1; document operational workaround

## Dependency Inventory

### External Libraries
1. **jsonwebtoken** — JWT signing/verification (RS256) — used by JwtService
2. **bcrypt** — password hashing — used by PasswordHasher

### External Services
3. **Email service** — password reset email dispatch (FR-AUTH.5) — provider TBD
4. **Secrets manager** — storage for RSA private key (risk mitigation)
5. **Uptime/APM monitoring + PagerDuty** — NFR-AUTH.2 availability alerting

### Internal Integration Points
- User database table (via UserRepository)
- RefreshToken database table (via RefreshTokenRepository)
- Request pipeline middleware layer
- Existing `/routes/index.ts` route registry
- Admin dashboard (for account locking / token revocation operations)

### Cryptographic Assets
- RSA key pair for RS256 signing (rotated every 90 days)

## Success Criteria

1. **FR-AUTH.1**: Login endpoint returns 200 with token pair for valid credentials, 401 for invalid, 403 for locked accounts; rate limit of 5/min/IP enforced
2. **FR-AUTH.2**: Registration returns 201 with user profile, 409 on duplicate email; password policy (8+ chars, upper/lower/digit) and email format enforced
3. **FR-AUTH.3**: Refresh rotates token pair; expired refresh returns 401; replay of revoked refresh triggers full user-token invalidation; refresh hashes persisted
4. **FR-AUTH.4**: Profile endpoint returns sanitized user record for valid Bearer token; 401 otherwise; no sensitive fields leaked
5. **FR-AUTH.5**: Reset token (1h TTL) emailed; valid reset allows password change + invalidates reset token; successful reset invalidates all refresh tokens
6. **NFR-AUTH.1**: Authentication endpoints ≤ 200ms p95 under normal load (k6 validated, APM monitored)
7. **NFR-AUTH.2**: 99.9% availability achieved (< 8.76h/year downtime) via health check + PagerDuty
8. **NFR-AUTH.3**: bcrypt cost factor 12 verified in unit test; hash latency ≈ 250ms benchmarked

### E2E Acceptance
Complete user lifecycle (register → login → profile → refresh → reset → login-with-new-password) executes end-to-end with correct status codes and credential invalidation after reset.

## Open Questions

1. **OI-1**: Should password reset emails be sent synchronously or via message queue? — Impacts reset endpoint latency and resilience — Target: v1.0 sprint planning
2. **OI-2**: Maximum number of active refresh tokens per user? — Impacts storage + multi-device UX — Target: architecture review
3. **GAP-1**: Account lockout threshold / progressive lockout policy after N failed attempts (security domain) — deferred to v1.1
4. **GAP-2**: Audit logging schema and retention for authentication events (backend domain) — deferred to v1.1
5. **GAP-3**: Token revocation behavior on user deletion / deactivation (architect domain) — deferred to v1.1
6. **Implicit**: Endpoint paths for registration, refresh, and password-reset flows are not explicitly enumerated in the spec — only `/auth/login` and `/auth/me` are verbatim; remaining paths inferred from `/auth/*` route group
7. **Implicit**: Email provider selection (SendGrid/SES/SMTP) and template ownership for reset email
