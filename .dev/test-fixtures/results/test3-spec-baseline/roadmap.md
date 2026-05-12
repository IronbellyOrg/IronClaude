---
spec_source: "test-spec-user-auth.md"
complexity_score: 0.6
adversarial: true
---

# Final Merged Roadmap: User Authentication Service

## Executive Summary

This roadmap implements a JWT-based authentication service with five core capabilities: login, registration, token refresh with rotation, profile retrieval, and password reset. The system is **medium complexity** (0.6/1.0), driven primarily by cryptographic correctness requirements and the refresh token rotation/replay detection mechanism.

The architecture is a layered TypeScript service using RS256 JWT signing (4096-bit), bcrypt password hashing (cost 12), and stateful refresh token revocation atop stateless access tokens. A feature flag (`AUTH_SERVICE_ENABLED`) provides rollback capability.

**Key architectural decisions are pre-made**: RS256, bcrypt-12, httpOnly cookie transport for refresh tokens, layered DI graph, and no server-side sessions. The roadmap follows a **database-first** approach — the spec precisely defines both schema and API surface, making mock-based iteration unnecessary and eliminating an entire class of integration bugs.

**Testing philosophy**: Embedded testing in every phase for early defect detection, supplemented by explicit coverage targets (90% line, 85% branch) and dedicated security/performance test suites as hardening exit criteria.

**Estimated duration**: 5 phases across 5–6 weeks for a small team (2 engineers + security review).

---

## Open Questions — Resolution Required Before Phase 1

| ID | Question | Recommended Resolution | Blocking Phase |
|----|----------|----------------------|----------------|
| OQ-5 | Refresh token transport: JSON body (FR-AUTH.1) vs httpOnly cookie (Section 2.1) — contradictory | **httpOnly cookie** per security constraint; update FR-AUTH.1 response schema to omit refresh_token from body | Phase 1 |
| OQ-2 | RSA key size not specified | **4096-bit** per current best practice | Phase 1 |
| OQ-1 | "Normal load" undefined for NFR-AUTH.1 | Define as **100 concurrent users, 50 req/s** or reference production baseline | Phase 3 |
| OQ-3 | Per-account rate limiting beyond per-IP | **Defer to v1.1** — per-IP covers MVP; note in risk register | Phase 2 |
| OQ-4 | Password reset link format and frontend integration | Define URL template (e.g., `{FRONTEND_URL}/reset?token={TOKEN}`) and token delivery as URL parameter | Phase 2 |
| OI-1 | Sync vs async email dispatch for password reset | **Synchronous for MVP** (reset traffic is <1% of requests; p95 impact negligible). If queue infrastructure already exists, prefer async. Document trade-off for v1.1 migration. | Phase 2 |
| OI-2 | Max active refresh tokens per user | **Cap at 5**; revoke oldest on overflow | Phase 1 |

---

## Phased Implementation Plan

### Phase 1: Foundation Layer (Week 1–2)

**Goal**: Build zero-dependency base components, database schema, and DI wiring. Everything in later phases depends on this layer.

#### 1.1 Database Schema and Migrations

| Task | Requirements Covered | Details |
|------|---------------------|---------|
| Create `users` table migration | FR-AUTH.2, FR-AUTH.1-IMPL-3, FR-AUTH.1-IMPL-5 | Columns: `id` (UUID v4 PK), `email` (unique index), `display_name`, `password_hash`, `is_locked` (boolean, default false), `created_at`, `updated_at`. Include down-migration. |
| Create `refresh_tokens` table migration | FR-AUTH.3d, FR-AUTH.1-IMPL-3, FR-AUTH.1-IMPL-5 | Columns: `id` (UUID v4 PK), `user_id` (FK → users, cascade delete), `token_hash` (SHA-256, unique), `expires_at`, `revoked_at`, `created_at`. Indexes on `user_id`, `expires_at`. Include down-migration. |
| Verify all migrations are reversible | FR-AUTH.1-IMPL-5 | Automated test: run up then down migration; assert clean state |

#### 1.2 PasswordHasher Service

| Task | Requirements Covered | Details |
|------|---------------------|---------|
| Implement `PasswordHasher` class | FR-AUTH.1, FR-AUTH.2, FR-AUTH.1-IMPL-1 | Methods: `hash(plaintext): Promise<string>`, `verify(plaintext, hash): Promise<boolean>` |
| Password policy validator | FR-AUTH.2c | Separate function: min 8 chars, 1 uppercase, 1 lowercase, 1 digit |
| Configure bcrypt cost factor 12 | NFR-AUTH.3 | Externalize as config; default 12 |
| Unit tests: hash timing ~250ms, verify round-trip, policy validation | NFR-AUTH.3, SC-5 | Benchmark test asserts 200–400ms range |

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
| Configure DI container with injectable services | NFR-AUTH-IMPL-3 | All components independently testable; mock injection supported |
| Register `PasswordHasher` and `JwtService` as singletons | NFR-AUTH-IMPL-3 | No cross-dependencies at this layer |
| Register database connection pool as singleton | NFR-AUTH-IMPL-3 | Available immediately for Phase 2 service integration |

#### 1.5 Crypto Review Gate

| Task | Requirements Covered | Details |
|------|---------------------|---------|
| Security engineer code review of PasswordHasher and JwtService | NFR-AUTH-IMPL-1, NFR-AUTH.3 | Verify: no keys in logs, correct bcrypt usage, RS256 key handling, secrets manager integration design |
| Verify crypto module interfaces are clean for Phase 2 consumption | — | Confirm service contracts before downstream services build on them |

**Exit Criteria**: All units pass. Crypto review signed off. Benchmark confirms ~250ms bcrypt timing and <50ms JWT sign/verify. Migrations run up and down cleanly. DI container wires correctly.

**Integration Points**:
- **DI Container**: Registers `PasswordHasher`, `JwtService`, database connection pool
- **Cross-Reference**: Phase 2 adds `TokenManager`, `AuthService`; Phase 3 adds middleware and routes

---

### Phase 2: Core Auth Logic (Week 2–3)

**Goal**: Implement `TokenManager` and `AuthService` — the stateful and orchestration layers — integrated against real database tables from Phase 1.

#### 2.1 TokenManager Service

| Task | Requirements Covered | Details |
|------|---------------------|---------|
| Implement `TokenManager` class | FR-AUTH.3 | Methods: `issueTokenPair(userId)`, `refreshTokens(refreshToken)`, `revokeAllForUser(userId)` |
| Refresh token rotation with replay detection | FR-AUTH.3a, FR-AUTH.3c | On refresh: issue new pair, revoke old (atomic transaction). On reuse of revoked token: revoke ALL tokens for user |
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
| Implement `AuthService.getProfile()` | FR-AUTH.4 | Return `id`, `email`, `display_name`, `created_at`. Exclude `password_hash`, `refresh_token_hash` (FR-AUTH.4c, SC-8) |
| Implement `AuthService.requestPasswordReset()` | FR-AUTH.5a | Generate reset token (1hr TTL), dispatch email synchronously (OI-1 resolution). Always return 200 (no email enumeration). |
| Implement `AuthService.resetPassword()` | FR-AUTH.5b, FR-AUTH.5c, FR-AUTH.5d | Validate token → update password → invalidate token → revoke all refresh tokens |
| Rate limiter: 5 attempts/min/IP for login | FR-AUTH.1d | Middleware or service-level; in-memory store acceptable for single-instance MVP |
| Unit tests: all 5 flows with happy + error paths | SC-5 | Minimum 15 test cases |

#### 2.3 Feature Flag

| Task | Requirements Covered | Details |
|------|---------------------|---------|
| Implement `AUTH_SERVICE_ENABLED` flag | FR-AUTH.1-IMPL-4 | Read from environment; gate auth route registration |
| Disabled behavior | SC-9 | Recommend 503 with `Retry-After` header for internal consumers; 404 for external/public APIs. Team decides based on operational maturity. |
| Verify rollback: flag=false restores pre-auth behavior | SC-9 | Integration test |

**Exit Criteria**: All unit tests pass for `TokenManager` and `AuthService`. Replay detection works against real database. SC-5 (all 4 services tested).

**Integration Points**:
- **DI Container (updated)**: Adds `TokenManager` (depends on `JwtService`, database), `AuthService` (depends on `TokenManager`, `PasswordHasher`, database)
- **Rate Limiter Middleware**: In-memory store, 5 req/min/IP
- **Feature Flag Gate**: Environment variable reader, route registration conditional
- **Cross-Reference**: Phase 3 routes consume all Phase 2 services

---

### Phase 3: Integration Layer (Week 3–4)

**Goal**: Wire services to HTTP routes and middleware. End-to-end flows work against real database.

#### 3.1 Auth Middleware

| Task | Requirements Covered | Details |
|------|---------------------|---------|
| Implement/modify `src/middleware/auth-middleware.ts` | FR-AUTH.4b | Extract Bearer token from `Authorization` header; verify via `JwtService.verify()`; attach `userId` to request context |
| Cookie extraction for refresh token | FR-AUTH.1-IMPL-2 | Read `refresh_token` from httpOnly cookie; validate via `TokenManager` |
| Reject expired/invalid tokens with 401 | FR-AUTH.4b | Consistent error response format; sanitize error messages to prevent information leakage (FR-AUTH.1b) |
| Unit test: valid token → pass, invalid → 401, missing → 401 | SC-5 | 3 test cases minimum |

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
| Password reset lifecycle: request → reset → login with new password → old tokens invalidated | SC-6 | Validates FR-AUTH.5 end-to-end |
| Sensitive field filtering: verify no `password_hash` or `refresh_token_hash` in any response | SC-8 | Scan all response bodies |
| Rate limiting: 6th login attempt within 1 minute returns 429 | FR-AUTH.1d | Timing-sensitive test |
| E2E lifecycle: register → login → profile → refresh → reset → re-login | SC-7 | Full user journey |

**Exit Criteria**: All integration tests pass. E2E lifecycle completes. SC-6, SC-7, SC-8 validated.

**Integration Points**:
- **Route Table**: 6 route handlers gated by `AUTH_SERVICE_ENABLED`
- **Middleware Chain**: Bearer token verification on protected routes; rate limiter on `/auth/login`

---

### Phase 4: Hardening and Validation (Week 5–6)

**Goal**: Performance validation, security review, rollback verification, production readiness. This phase incorporates comprehensive coverage targets and dedicated security test suites.

#### 4.1 Performance Testing

| Task | Requirements Covered | Details |
|------|---------------------|---------|
| k6 load test: login endpoint | NFR-AUTH.1, SC-2 | Target: p95 < 200ms at defined normal load (OQ-1 resolution) |
| k6 load test: token refresh endpoint | NFR-AUTH.1 | Same latency target |
| k6 load test: registration endpoint | NFR-AUTH.1 | Expect higher latency (bcrypt); document baseline |
| Benchmark bcrypt cost factor 12 timing | NFR-AUTH.3, SC-4 | Assert ~250ms per hash |

#### 4.2 Security Test Suites

| Task | Requirements Covered | Details |
|------|---------------------|---------|
| Replay detection test: reuse revoked token, confirm all tokens invalidated | FR-AUTH.3c, RISK-2 | Adversarial test suite |
| XSS prevention test: verify refresh token only in httpOnly cookie, never in response body | FR-AUTH.1-IMPL-2 | Automated scan |
| Information leakage test: verify generic 401 messages, no email/password differentiation | FR-AUTH.1b | All auth error responses |
| JWT validation test: tampered JWT rejected, expired JWT rejected, invalid signature rejected | SC-5 | Cover all failure modes |
| Sensitive field exclusion: verify no `password_hash` or token hashes in any endpoint response | SC-8 | Automated response schema scan |
| Password policy enforcement: verify FR-AUTH.2c (8+ chars, 1 upper, 1 lower, 1 digit) | FR-AUTH.2c | Boundary value testing |
| Verify no plaintext passwords stored | FR-AUTH.1-IMPL-1 | Database audit |
| Verify RS256 key size (4096-bit) | NFR-AUTH-IMPL-1 | Key inspection |
| Verify httpOnly/Secure/SameSite cookie attributes | FR-AUTH.1-IMPL-2 | Response header verification |

#### 4.3 Coverage Validation

| Task | Requirements Covered | Details |
|------|---------------------|---------|
| Measure and enforce line coverage ≥ 90% | SC-5, SC-6 | Across all unit and integration tests |
| Measure and enforce branch coverage ≥ 85% | SC-5, SC-6 | Identify and fill gaps from Phases 1–3 testing |
| Critical path coverage ≥ 95% | SC-7 | Login, token refresh, password reset flows |

#### 4.4 Rollback Verification

| Task | Requirements Covered | Details |
|------|---------------------|---------|
| Test `AUTH_SERVICE_ENABLED=false` | SC-9 | Auth routes return expected disabled status; existing functionality unaffected |
| Test database down-migrations | FR-AUTH.1-IMPL-5 | Run all migrations down; verify clean state |
| Document rollback procedure | SC-9 | Runbook for on-call |

#### 4.5 Monitoring and Observability

| Task | Requirements Covered | Details |
|------|---------------------|---------|
| Health check endpoint | NFR-AUTH.2 | `/health` returns 200 with service status |
| APM integration for latency tracking | NFR-AUTH.1, SC-2 | p50, p95, p99 latency dashboard |
| Uptime monitoring configuration | NFR-AUTH.2, SC-3 | PagerDuty/alerting integration |

**Exit Criteria**: All success criteria (SC-1 through SC-9) validated. Security test suites pass. Coverage targets met. Production deployment approved.

---

### Phase 5: Production Readiness (Week 6, overlapping with Phase 4)

**Goal**: Deployment pipeline, secrets management, monitoring thresholds, and documentation. This phase incorporates production readiness elements surfaced during debate review.

#### 5.1 Secrets Management

| Task | Requirements Covered | Details |
|------|---------------------|---------|
| Secrets manager integration (Vault, AWS SM, etc.) | NFR-AUTH-IMPL-2, RISK-1 | RSA private key, database credentials, email service API key |
| Key rotation on 90-day schedule | RISK-1 | Grace period for key transitions: old key accepted for verification during rotation window |
| Rotation logging and alerting | RISK-1 | Audit trail for all key access and rotation events |

#### 5.2 Monitoring Thresholds and Alerting

| Task | Requirements Covered | Details |
|------|---------------------|---------|
| Login error rate > 5% → critical alert | NFR-AUTH.2 | Rapid detection of credential stuffing or service issues |
| API p95 latency > 300ms → warning alert | NFR-AUTH.1 | Early warning before SLA breach |
| Refresh token replay detected → security alert | FR-AUTH.3c, RISK-2 | Immediate notification of potential token theft |
| Email service failures → warning alert | RISK-4 | Visibility into password reset degradation |
| Database connection failures → critical alert | NFR-AUTH.2 | Core dependency monitoring |

#### 5.3 Deployment Pipeline

| Task | Requirements Covered | Details |
|------|---------------------|---------|
| CI pipeline: run all test suites, lint, coverage report, build artifact | SC-1–SC-9 | Fail if coverage < 90% |
| Gradual rollout strategy | SC-9, FR-AUTH.1-IMPL-4 | Deploy with flag off → smoke test → 10% traffic (monitor 1hr) → 50% (monitor 1hr) → 100% |
| Rollback procedure: set flag to disabled, redeploy | SC-9 | Target: rollback < 5 minutes |

#### 5.4 Documentation Deliverables

| Task | Requirements Covered | Details |
|------|---------------------|---------|
| OpenAPI/Swagger spec for all `/auth/*` endpoints | — | Request/response examples, error codes (401, 403, 409, 400, 429) |
| Sequence diagrams: login flow, token refresh, password reset, replay detection | — | Architecture documentation |
| Operational runbooks | — | Deployment, rollback, secret rotation, security alert response, metric investigation |
| Security documentation: threat model, controls mapping, incident response for key compromise | RISK-1–RISK-6 | Maps risks to mitigations |

**Exit Criteria**: Secrets configured and rotated. Monitoring dashboards populated. CI/CD pipeline passes end-to-end. Documentation complete and reviewed.

---

## Risk Assessment and Mitigation

| Risk | Severity | Probability | Phase Addressed | Mitigation Strategy | Residual Risk |
|------|----------|-------------|----------------|---------------------|---------------|
| RISK-1: JWT key compromise | HIGH | Low | Phase 1 (key loading), Phase 1.5 (crypto review), Phase 5.1 (rotation) | RS256 4096-bit keys in secrets manager; 90-day rotation with grace period; access audit logging; emergency recovery procedure | Key rotation gap window (max 90 days); compromised secrets manager |
| RISK-2: Refresh token replay | HIGH | Medium | Phase 2 (implementation), Phase 4.2 (adversarial test) | Token rotation on every refresh; full revocation on replay detection (FR-AUTH.3c); atomic database transactions; replay detection metrics | Window between theft and detection (minutes); relies on monitoring |
| RISK-3: bcrypt cost factor obsolescence | MEDIUM | Low | Phase 1 (configurable), Phase 4.1 (benchmark) | Externalized cost factor; annual review documented in runbook; performance benchmarks in CI | Requires proactive annual review |
| RISK-4: Email service dependency | MEDIUM | Medium | Phase 2 (sync MVP) | Synchronous dispatch for MVP; always return 200 to prevent enumeration; queue-based dispatch in v1.1. If queue infrastructure exists, prefer async. | Email delivery failures block password reset; no fallback in spec |
| RISK-5: Account takeover via brute-force | MEDIUM | Medium | Phase 2 (rate limiter) | Rate limiting 5/min/IP; account lockout deferred to v1.1 (GAP-1); progressive backoff for failed attempts | Rate limiting doesn't prevent distributed attacks; per-account lockout not yet implemented |
| RISK-6: Insufficient password entropy | MEDIUM | Low | Phase 1 (policy validator) | Password policy enforcement (8+ chars, 1 upper, 1 lower, 1 digit); configurable via environment | Policy is conservative; stronger policies (zxcvbn, passphrase) recommended for v2.0 |

---

## Resource Requirements and Dependencies

### Team

| Role | Count | Phases | Focus |
|------|-------|--------|-------|
| Backend Engineer | 2 | All | One focused on crypto/token layer (Phases 1.2–1.3, 2.1), one on service/route layer (Phases 1.1, 2.2, 3). Both contribute to Phase 4–5. |
| Security Reviewer | 1 | Phase 1.5 (crypto gate), Phase 4.2 (security suites) | Code review of crypto operations, token handling, sensitive data filtering |

**Responsibility coverage checklist** (ensure these concerns are assigned, not necessarily to separate people): cryptography correctness, database schema design, API/middleware integration, testing/QA, performance validation, deployment/DevOps, monitoring, documentation, security review.

### External Dependencies

| Dependency | Required By | Action | Owner |
|------------|-------------|--------|-------|
| `jsonwebtoken` library | Phase 1 start | `npm install` | Dev team |
| `bcrypt` library | Phase 1 start | `npm install` | Dev team |
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

## Success Criteria and Validation Approach

### Validation Matrix

| Criterion | Description | Phase Validated | Method |
|-----------|-------------|----------------|--------|
| SC-1 | All FR-AUTH.1–5 acceptance criteria pass | Phase 3 | Integration test suite |
| SC-2 | p95 latency < 200ms | Phase 4 | k6 load test |
| SC-3 | 99.9% uptime over 30 days | Post-deploy | Uptime monitoring (Phase 5.2) |
| SC-4 | bcrypt cost 12, ~250ms/hash | Phase 1 + Phase 4 | Unit benchmark + load benchmark |
| SC-5 | All unit tests pass (4 services) | Phase 1–2 | Unit test suite, ≥90% line coverage |
| SC-6 | All integration tests pass | Phase 3 | Integration suite, ≥85% branch coverage |
| SC-7 | E2E lifecycle completes | Phase 3 | Full register→login→profile→refresh→reset→re-login test |
| SC-8 | No sensitive fields in responses | Phase 3 + Phase 4 | Automated response schema scan + security test suite |
| SC-9 | Feature flag rollback works | Phase 4 | Toggle `AUTH_SERVICE_ENABLED`, verify behavior |

### Phase Gates

| Gate | Key Criteria |
|------|-------------|
| **Phase 1 Gate** | Crypto review signed off; all foundations pass unit tests; migrations reversible; DI wires correctly |
| **Phase 2 Gate** | All service unit tests pass; replay detection works against real DB; SC-5 complete |
| **Phase 3 Gate** | Integration and E2E tests pass; SC-6, SC-7, SC-8 validated |
| **Phase 4 Gate** | Security suites pass; performance validated; coverage targets met; SC-1–SC-9 sign-off |
| **Phase 5 Gate** | Secrets configured; monitoring active; CI/CD working; docs complete; production deployment approved |

---

## Timeline Summary

| Phase | Duration | Key Deliverables |
|-------|----------|------------------|
| **Pre-work**: Resolve OQ-5, OQ-2, OI-1, OI-2 | 1–2 days | Decision document |
| **Phase 1**: Foundation | 1.5 weeks | Migrations, PasswordHasher, JwtService, DI wiring, crypto review gate |
| **Phase 2**: Core Auth Logic | 1.5 weeks | TokenManager, AuthService, rate limiter, feature flag |
| **Phase 3**: Integration | 1 week | Routes, middleware, integration + E2E tests |
| **Phase 4**: Hardening | 1 week | Performance validation, security test suites, coverage targets, rollback verification |
| **Phase 5**: Production Readiness | 0.5–1 week (overlaps Phase 4) | Secrets management, monitoring thresholds, deployment pipeline, documentation |
| **Total** | **5–6 weeks** | Production-ready auth service |

**Parallel opportunities**: Phase 1 tasks (schema vs crypto services) split between two engineers. Phase 5 infrastructure setup starts during Phase 4. Load testing and security review run in parallel within Phase 4.

---

## Deferred Items (v1.1)

| Item | Rationale |
|------|-----------|
| **GAP-1**: Progressive account lockout | Complements per-IP rate limiting; requires UX design |
| **GAP-2**: Audit logging for auth events | Compliance/observability; log structure prepared in v1.0 |
| **GAP-3**: Token revocation cascade on user deletion | Data integrity; requires cascade logic |
| **OQ-3**: Per-account rate limiting | Distributed brute-force defense |
| **OI-1**: Async email dispatch via message queue | Retrofit if not already async; resilience improvement |
| OAuth, MFA, RBAC | Excluded by spec |
