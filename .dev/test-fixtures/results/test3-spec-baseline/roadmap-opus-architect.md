---
spec_source: "test-spec-user-auth.md"
complexity_score: 0.6
primary_persona: architect
---

# Project Roadmap: User Authentication Service

## 1. Executive Summary

This roadmap covers implementation of a JWT-based authentication service with five core capabilities: login, registration, token refresh with rotation, profile retrieval, and password reset. The system is **medium complexity** (0.6/1.0), driven primarily by cryptographic correctness requirements and the refresh token rotation/replay detection mechanism.

The architecture is a layered TypeScript service using RS256 JWT signing, bcrypt password hashing (cost 12), and stateful refresh token revocation atop stateless access tokens. A feature flag (`AUTH_SERVICE_ENABLED`) provides rollback capability.

**Key architectural decisions are pre-made**: RS256, bcrypt-12, httpOnly cookie transport for refresh tokens, layered DI graph, and no server-side sessions. The roadmap focuses on correct, secure implementation within these constraints.

**Estimated duration**: 4 phases across 5–6 weeks for a small team (2 engineers + security review).

---

## 2. Open Questions — Resolution Required Before Phase 1

The following must be resolved before implementation begins. Proceeding without resolution introduces rework risk.

| ID | Question | Recommended Resolution | Blocking Phase |
|----|----------|----------------------|----------------|
| OQ-5 | Refresh token transport: JSON body (FR-AUTH.1) vs httpOnly cookie (Section 2.1) — contradictory | **httpOnly cookie** per security constraint; update FR-AUTH.1 response schema to omit refresh_token from body | Phase 1 |
| OQ-2 | RSA key size not specified | **4096-bit** per current best practice | Phase 1 |
| OQ-1 | "Normal load" undefined for NFR-AUTH.1 | Define as **100 concurrent users, 50 req/s** or reference production baseline | Phase 3 |
| OQ-3 | Per-account rate limiting beyond per-IP | **Defer to v1.1** — per-IP covers MVP; note in risk register | Phase 2 |
| OQ-4 | Password reset link format and frontend integration | Define URL template (e.g., `{FRONTEND_URL}/reset?token={TOKEN}`) and token delivery as URL parameter | Phase 2 |
| OI-1 | Sync vs async email dispatch for password reset | **Synchronous for MVP**; queue-based in v1.1 | Phase 2 |
| OI-2 | Max active refresh tokens per user | **Cap at 5**; revoke oldest on overflow | Phase 1 |

---

## 3. Phased Implementation Plan

### Phase 1: Foundation Layer (Week 1–2)

**Goal**: Build zero-dependency base components and database schema. Everything in later phases depends on this layer.

#### 1.1 Database Schema & Migrations

| Task | Requirements Covered | Details |
|------|---------------------|---------|
| Create `users` table migration | FR-AUTH.2, FR-AUTH.1-IMPL-3, FR-AUTH.1-IMPL-5 | Columns: `id` (UUID v4 PK), `email` (unique index), `display_name`, `password_hash`, `is_locked` (boolean), `created_at`, `updated_at`. Include down-migration. |
| Create `refresh_tokens` table migration | FR-AUTH.3d, FR-AUTH.1-IMPL-3, FR-AUTH.1-IMPL-5 | Columns: `id` (UUID v4 PK), `user_id` (FK → users), `token_hash` (SHA-256), `expires_at`, `revoked_at`, `created_at`. Index on `user_id`. Include down-migration. |
| Verify all migrations are reversible | FR-AUTH.1-IMPL-5 | Automated test: run up then down migration; assert clean state |

#### 1.2 PasswordHasher Service

| Task | Requirements Covered | Details |
|------|---------------------|---------|
| Implement `PasswordHasher` class | FR-AUTH.1, FR-AUTH.2, FR-AUTH.1-IMPL-1 | Methods: `hash(plaintext): Promise<string>`, `verify(plaintext, hash): Promise<boolean>` |
| Configure bcrypt cost factor 12 | NFR-AUTH.3 | Externalize as config; default 12 |
| Unit tests: hash timing ~250ms, verify round-trip | NFR-AUTH.3, SC-5 | Benchmark test asserts 200–400ms range |

#### 1.3 JwtService

| Task | Requirements Covered | Details |
|------|---------------------|---------|
| Implement `JwtService` class | FR-AUTH.1, FR-AUTH.3, NFR-AUTH-IMPL-1 | Methods: `sign(payload, ttl): string`, `verify(token): Payload \| null` |
| RS256 key pair loading from secrets manager | NFR-AUTH-IMPL-2 | Load private key for signing, public key for verification; 4096-bit RSA (per OQ-2 resolution) |
| Access token TTL: 15 minutes | FR-AUTH.1a | Configurable via environment variable |
| Unit tests: sign/verify round-trip, expired token rejection, tampered token rejection | SC-5 | Cover happy path + 3 failure modes |

#### 1.4 Dependency Injection Setup

| Task | Requirements Covered | Details |
|------|---------------------|---------|
| Configure DI container with injectable services | NFR-AUTH-IMPL-3 | All components independently testable |
| Register `PasswordHasher` and `JwtService` as singletons | NFR-AUTH-IMPL-3 | No cross-dependencies at this layer |

**Integration Points — Phase 1 Wiring**:

- **Named Artifact**: DI Container / Service Registry
- **Wired Components**: `PasswordHasher`, `JwtService`
- **Owning Phase**: Phase 1
- **Cross-Reference**: Phase 2 adds `TokenManager`, `AuthService`; Phase 3 adds middleware and routes

**Milestone M1**: `PasswordHasher` and `JwtService` pass all unit tests independently. Migrations run up and down cleanly. **Gate**: SC-5 partial (2 of 4 services tested).

---

### Phase 2: Core Auth Logic (Week 2–3)

**Goal**: Implement `TokenManager` and `AuthService` — the stateful and orchestration layers.

#### 2.1 TokenManager Service

| Task | Requirements Covered | Details |
|------|---------------------|---------|
| Implement `TokenManager` class | FR-AUTH.3 | Methods: `issueTokenPair(userId)`, `refreshTokens(refreshToken)`, `revokeAllForUser(userId)` |
| Refresh token rotation with replay detection | FR-AUTH.3a, FR-AUTH.3c | On refresh: issue new pair, revoke old. On reuse of revoked token: revoke ALL tokens for user |
| Refresh token hash storage (SHA-256) | FR-AUTH.3d | Store hash only; never persist raw token |
| Refresh token TTL: 7 days | FR-AUTH.1a | Configurable via environment variable |
| Enforce max 5 active refresh tokens per user | OI-2 resolution | Revoke oldest when cap exceeded |
| Refresh token delivery via httpOnly cookie | FR-AUTH.1-IMPL-2 | Set `Secure`, `SameSite=Strict`, `HttpOnly` attributes; do NOT include in JSON response body (OQ-5 resolution) |
| Unit tests: issue, rotate, replay detection, expiry, cap enforcement | SC-5 | Minimum 6 test cases |

#### 2.2 AuthService

| Task | Requirements Covered | Details |
|------|---------------------|---------|
| Implement `AuthService.login()` | FR-AUTH.1 | Verify credentials → issue token pair. Return 401 generic message on failure (FR-AUTH.1b). Return 403 on locked account (FR-AUTH.1c). |
| Implement `AuthService.register()` | FR-AUTH.2 | Validate email format (FR-AUTH.2d) → check uniqueness (FR-AUTH.2b) → enforce password policy (FR-AUTH.2c) → hash password → create user |
| Password policy enforcement | FR-AUTH.2c | Min 8 chars, 1 uppercase, 1 lowercase, 1 digit |
| Implement `AuthService.getProfile()` | FR-AUTH.4 | Return `id`, `email`, `display_name`, `created_at`. Exclude `password_hash`, `refresh_token_hash` (FR-AUTH.4c, SC-8) |
| Implement `AuthService.requestPasswordReset()` | FR-AUTH.5a | Generate reset token (1hr TTL), dispatch email synchronously (OI-1 resolution) |
| Implement `AuthService.resetPassword()` | FR-AUTH.5b, FR-AUTH.5c, FR-AUTH.5d | Validate token → update password → invalidate token → revoke all refresh tokens |
| Rate limiter: 5 attempts/min/IP for login | FR-AUTH.1d | Middleware or service-level; in-memory store acceptable for single-instance MVP |
| Unit tests: all 5 flows with happy + error paths | SC-5 | Minimum 15 test cases |

#### 2.3 Feature Flag

| Task | Requirements Covered | Details |
|------|---------------------|---------|
| Implement `AUTH_SERVICE_ENABLED` flag | FR-AUTH.1-IMPL-4 | Read from environment; gate auth route registration |
| Verify rollback: flag=false restores pre-auth behavior | SC-9 | Integration test |

**Integration Points — Phase 2 Wiring**:

- **Named Artifact**: DI Container / Service Registry
- **Wired Components (added)**: `TokenManager` (depends on `JwtService`, `RefreshToken` repository), `AuthService` (depends on `TokenManager`, `PasswordHasher`, `User` repository)
- **Owning Phase**: Phase 2
- **Cross-Reference**: Consumed by Phase 3 route handlers and middleware

- **Named Artifact**: Rate Limiter Middleware
- **Wired Components**: In-memory rate limit store keyed by IP, configured for 5 req/min
- **Owning Phase**: Phase 2
- **Cross-Reference**: Wired into login route in Phase 3

- **Named Artifact**: Feature Flag Gate (`AUTH_SERVICE_ENABLED`)
- **Wired Components**: Environment variable reader, route registration conditional
- **Owning Phase**: Phase 2
- **Cross-Reference**: Phase 3 route registration uses this flag; Phase 4 validates rollback via SC-9

**Milestone M2**: All unit tests pass for `TokenManager` and `AuthService`. Replay detection works in isolation. **Gate**: SC-5 (all 4 services tested).

---

### Phase 3: Integration Layer (Week 3–4)

**Goal**: Wire services to HTTP routes and middleware. End-to-end flows work.

#### 3.1 Auth Middleware

| Task | Requirements Covered | Details |
|------|---------------------|---------|
| Modify `src/middleware/auth-middleware.ts` | FR-AUTH.4b | Extract Bearer token from `Authorization` header; verify via `JwtService.verify()`; attach `userId` to request context |
| Reject expired/invalid tokens with 401 | FR-AUTH.4b | Consistent error response format |
| Unit test: valid token → pass, invalid → 401 | SC-5 | 3 test cases minimum |

#### 3.2 Route Registration

| Task | Requirements Covered | Details |
|------|---------------------|---------|
| `POST /auth/login` | FR-AUTH.1 | Rate-limited. Calls `AuthService.login()`. Sets refresh token cookie. Returns access_token in body. |
| `POST /auth/register` | FR-AUTH.2 | Calls `AuthService.register()`. Returns 201 with user profile. |
| `POST /auth/refresh` | FR-AUTH.3 | Reads refresh token from httpOnly cookie. Calls `TokenManager.refreshTokens()`. Sets new cookie. Returns new access_token. |
| `GET /auth/profile` | FR-AUTH.4 | Protected by auth middleware. Calls `AuthService.getProfile()`. |
| `POST /auth/password-reset/request` | FR-AUTH.5a | Calls `AuthService.requestPasswordReset()`. Always returns 200 (no email enumeration). |
| `POST /auth/password-reset/confirm` | FR-AUTH.5b | Calls `AuthService.resetPassword()`. Returns 200 on success. |
| Modify `src/routes/index.ts` for route registration | FR-AUTH.1-IMPL-4 | Conditional on `AUTH_SERVICE_ENABLED` |

#### 3.3 Integration Tests

| Task | Requirements Covered | Details |
|------|---------------------|---------|
| Full login flow: register → login → verify token | SC-6 | Against real database |
| Token refresh with rotation: login → refresh → verify new token, old token rejected | SC-6 | Validates FR-AUTH.3a, FR-AUTH.3c |
| Password reset lifecycle: request → reset → login with new password | SC-6 | Validates FR-AUTH.5 end-to-end |
| Sensitive field filtering: verify no `password_hash` or `refresh_token_hash` in any response | SC-8 | Scan all response bodies |
| Rate limiting: 6th login attempt within 1 minute returns 429 | FR-AUTH.1d | Timing-sensitive test |

**Integration Points — Phase 3 Wiring**:

- **Named Artifact**: Route Table (`src/routes/index.ts`)
- **Wired Components**: 6 route handlers (`/auth/login`, `/auth/register`, `/auth/refresh`, `/auth/profile`, `/auth/password-reset/request`, `/auth/password-reset/confirm`)
- **Owning Phase**: Phase 3
- **Cross-Reference**: Gated by `AUTH_SERVICE_ENABLED` from Phase 2; handlers consume `AuthService` and `TokenManager` from Phase 2

- **Named Artifact**: Middleware Chain
- **Wired Components**: `auth-middleware` (Bearer token verification) applied to protected routes (`/auth/profile`); Rate limiter applied to `/auth/login`
- **Owning Phase**: Phase 3
- **Cross-Reference**: Middleware uses `JwtService` from Phase 1; Rate limiter from Phase 2

**Milestone M3**: All integration tests pass. E2E lifecycle (register → login → profile → refresh → reset → re-login) completes. **Gate**: SC-6, SC-7, SC-8.

---

### Phase 4: Hardening & Validation (Week 5–6)

**Goal**: Performance validation, security review, rollback verification, production readiness.

#### 4.1 Performance Testing

| Task | Requirements Covered | Details |
|------|---------------------|---------|
| k6 load test: login endpoint | NFR-AUTH.1, SC-2 | Target: p95 < 200ms at defined normal load (OQ-1 resolution) |
| k6 load test: token refresh endpoint | NFR-AUTH.1 | Same latency target |
| k6 load test: registration endpoint | NFR-AUTH.1 | Expect higher latency (bcrypt); document baseline |
| Benchmark bcrypt cost factor 12 timing | NFR-AUTH.3, SC-4 | Assert ~250ms per hash |

#### 4.2 Security Review

| Task | Requirements Covered | Details |
|------|---------------------|---------|
| Verify no plaintext passwords stored | FR-AUTH.1-IMPL-1 | Database audit |
| Verify RS256 key size (4096-bit) | NFR-AUTH-IMPL-1 | Key inspection |
| Verify httpOnly/Secure/SameSite cookie attributes | FR-AUTH.1-IMPL-2 | Browser DevTools verification |
| Verify refresh token replay detection | FR-AUTH.3c, RISK-2 | Adversarial test: reuse revoked token, confirm all tokens invalidated |
| Verify generic error messages (no email/password enumeration) | FR-AUTH.1b | Review all 401 response messages |
| Verify sensitive field exclusion in all endpoints | SC-8 | Automated scan of all response schemas |

#### 4.3 Rollback Verification

| Task | Requirements Covered | Details |
|------|---------------------|---------|
| Test `AUTH_SERVICE_ENABLED=false` | SC-9 | Auth routes return 404; existing functionality unaffected |
| Test database down-migrations | FR-AUTH.1-IMPL-5 | Run all migrations down; verify clean state |
| Document rollback procedure | SC-9 | Runbook for on-call |

#### 4.4 Monitoring & Observability

| Task | Requirements Covered | Details |
|------|---------------------|---------|
| Health check endpoint | NFR-AUTH.2 | `/health` returns 200 with service status |
| APM integration for latency tracking | NFR-AUTH.1, SC-2 | p95 latency dashboard |
| Uptime monitoring configuration | NFR-AUTH.2, SC-3 | PagerDuty integration |

**Milestone M4**: All success criteria (SC-1 through SC-9) validated. Security review complete. Production deployment approved. **Gate**: Full SC-1 through SC-9 sign-off.

---

## 4. Risk Assessment & Mitigation

| Risk | Severity | Phase Addressed | Mitigation Strategy | Validation |
|------|----------|----------------|---------------------|------------|
| RISK-1: JWT key compromise | HIGH | Phase 1 (key loading), Phase 4 (review) | RS256 4096-bit keys in secrets manager; 90-day rotation documented | Phase 4 security review verifies key storage and rotation procedure |
| RISK-2: Refresh token replay | HIGH | Phase 2 (implementation), Phase 4 (adversarial test) | Token rotation on every refresh; full revocation on replay detection (FR-AUTH.3c) | Phase 3 integration test + Phase 4 adversarial test |
| RISK-3: bcrypt cost factor obsolescence | MEDIUM | Phase 1 (configurable), Phase 4 (benchmark) | Externalized cost factor; annual review documented in runbook | Phase 4 benchmark confirms ~250ms timing |
| RISK-4: Email service dependency | MEDIUM | Phase 2 (sync MVP) | Synchronous dispatch for MVP; always return 200 to prevent enumeration; queue-based dispatch in v1.1 | Phase 3 integration test covers reset flow |
| **NEW RISK-5**: Cookie/body transport confusion (OQ-5) | MEDIUM | Phase 2 | Resolve before implementation; standardize on httpOnly cookie | Phase 3 integration test verifies cookie transport |

---

## 5. Resource Requirements & Dependencies

### Team

| Role | Count | Phases | Focus |
|------|-------|--------|-------|
| Backend Engineer | 2 | All | Core implementation; one focused on crypto/token layer, one on service/route layer |
| Security Reviewer | 1 | Phase 4 | Code review of crypto operations, token handling, and sensitive data filtering |

### External Dependencies — Acquisition Timeline

| Dependency | Required By | Action | Owner |
|------------|-------------|--------|-------|
| `jsonwebtoken` library | Phase 1 start | `npm install` — no procurement needed | Dev team |
| `bcrypt` library | Phase 1 start | `npm install` — no procurement needed | Dev team |
| RSA 4096-bit key pair | Phase 1 start | Generate and store in secrets manager | DevOps/Security |
| Secrets manager access | Phase 1 start | Provision access for auth service | DevOps |
| Email service credentials | Phase 2 start | Obtain SMTP/API credentials | Dev team + Infra |
| k6 load testing tool | Phase 4 start | Install in CI/staging environment | DevOps |
| APM/monitoring access | Phase 4 start | Configure for auth service | DevOps |

### Infrastructure

| Resource | Purpose | Required By |
|----------|---------|-------------|
| Database (PostgreSQL recommended) | Users + refresh_tokens tables | Phase 1 |
| Secrets manager (Vault, AWS SM, etc.) | RSA private key storage | Phase 1 |
| Email service (SendGrid, SES, etc.) | Password reset emails | Phase 2 |
| Staging environment | Integration and load testing | Phase 3 |

---

## 6. Success Criteria Validation Matrix

| Criterion | Description | Phase Validated | Method |
|-----------|-------------|----------------|--------|
| SC-1 | All FR-AUTH.1–5 acceptance criteria pass | Phase 3 | Integration test suite |
| SC-2 | p95 latency < 200ms | Phase 4 | k6 load test |
| SC-3 | 99.9% uptime over 30 days | Post-deploy | Uptime monitoring |
| SC-4 | bcrypt cost 12, ~250ms/hash | Phase 1 + Phase 4 | Unit benchmark + load benchmark |
| SC-5 | All unit tests pass (4 services) | Phase 1–2 | `uv run pytest` unit suite |
| SC-6 | All integration tests pass | Phase 3 | `uv run pytest` integration suite |
| SC-7 | E2E lifecycle completes | Phase 3 | Full register→login→profile→refresh→reset→re-login test |
| SC-8 | No sensitive fields in responses | Phase 3 + Phase 4 | Automated response schema scan + manual review |
| SC-9 | Feature flag rollback works | Phase 4 | Toggle `AUTH_SERVICE_ENABLED=false`, verify behavior |

---

## 7. Timeline Summary

| Phase | Duration | Parallel? | Key Deliverables |
|-------|----------|-----------|------------------|
| **Pre-work**: Resolve OQ-5, OQ-2, OI-1, OI-2 | 1–2 days | Before Phase 1 | Decision document |
| **Phase 1**: Foundation | 1.5 weeks | Two engineers can split PasswordHasher / JwtService | Migrations, PasswordHasher, JwtService, DI wiring |
| **Phase 2**: Core Auth Logic | 1.5 weeks | TokenManager and AuthService are sequential (AuthService depends on TokenManager) | TokenManager, AuthService, rate limiter, feature flag |
| **Phase 3**: Integration | 1 week | Route wiring + integration tests | Routes, middleware, integration + E2E tests |
| **Phase 4**: Hardening | 1 week | Load testing and security review can run in parallel | Performance validation, security sign-off, rollback verification |
| **Total** | **5–6 weeks** | | Production-ready auth service |

---

## 8. v1.1 Deferred Items

The following are explicitly out of scope for this roadmap but should be planned:

- **GAP-1**: Progressive account lockout policy (complements per-IP rate limiting)
- **GAP-2**: Audit logging for authentication events
- **GAP-3**: Token revocation cascade on user deletion
- **OQ-3**: Per-account rate limiting for distributed brute-force defense
- **OI-1**: Async email dispatch via message queue
- OAuth, MFA, RBAC (excluded by spec)
