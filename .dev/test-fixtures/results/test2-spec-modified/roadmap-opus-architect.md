---
spec_source: test-spec-user-auth.md
complexity_score: 0.62
primary_persona: architect
generated: "2026-03-27T00:00:00Z"
generator: roadmap-architect-v1
total_phases: 4
total_milestones: 8
total_requirements_mapped: 8
risks_addressed: 5
open_questions: 8
---

# Project Roadmap: User Authentication Service v1.0

## 1. Executive Summary

This roadmap delivers a JWT-based authentication service comprising 5 functional endpoints (login, registration, token refresh, profile retrieval, password reset) with 3 non-functional targets (latency, availability, hashing security). The system uses RS256 asymmetric signing, bcrypt password hashing, and stateful refresh token rotation with replay detection.

**Complexity**: MEDIUM (0.62) — driven primarily by security correctness requirements and stateful token rotation logic, not breadth.

**Critical Path**: Password Hasher + JWT Service → Token Manager → Auth Service → Middleware + Routes → Integration Testing → Load Testing → Deploy behind feature flag.

**Key Constraints**:
- RS256 asymmetric signing (not HS256) — requires secrets manager integration before any JWT work
- bcrypt cost factor 12 (~250ms/hash) consumes most of the 200ms p95 latency budget for login
- 8 open questions, 3 of which block implementation (OQ-1, OQ-6, OQ-7)

**Blocking Decisions Required Before Phase 2**:
1. Secrets manager platform selection (OQ-7) — blocks `jwt-service.ts`
2. Email service provider and interface contract (OQ-1, OQ-6) — blocks FR-AUTH.5
3. Maximum active refresh tokens per user (OQ-2) — blocks FR-AUTH.3 table design

---

## 2. Phased Implementation Plan

### Phase 0: Foundation & Decision Resolution
**Duration**: 3–5 days  
**Goal**: Resolve blocking open questions, establish infrastructure prerequisites, finalize database schema.

#### Milestone 0.1: Blocking Decisions Resolved
- [ ] **OQ-7**: Select secrets manager platform (AWS Secrets Manager / HashiCorp Vault / GCP Secret Manager)
  - Decision determines key injection mechanism for `jwt-service.ts` and deployment pipeline
- [ ] **OQ-1 / OQ-6**: Select email service provider; define interface contract, retry policy, SLA, and failure behavior for FR-AUTH.5
  - Synchronous vs. async dispatch decision directly impacts endpoint latency and infrastructure requirements
- [ ] **OQ-2**: Define maximum concurrent refresh tokens per user
  - Impacts RefreshToken table schema, indexing strategy, and revocation blast radius
- [ ] **OQ-3**: Confirm account lockout policy scope (v1.0 or v1.1)
  - If v1.0: extends FR-AUTH.1 scope; adds RISK-4 mitigation work to Phase 2
- [ ] **OQ-8**: Document accepted behavior for concurrent refresh token rotation race condition
  - Decide: idempotency window vs. accepted false-positive invalidation vs. deferred to v1.1

#### Milestone 0.2: Infrastructure Prerequisites
- [ ] Generate RS256 key pair; store private key in selected secrets manager
- [ ] Configure key rotation automation (90-day period per deployment constraint)
- [ ] Provision or configure email service credentials
- [ ] Set up feature flag `AUTH_SERVICE_ENABLED` in configuration system
- [ ] Create database migration `003-auth-tables.ts` with User and RefreshToken table schemas (including down-migration for rollback)
- [ ] Validate k6 and APM tooling are available for NFR validation in Phase 3

**Exit Criteria**: All blocking OQs resolved with documented decisions. Infrastructure provisioned. Migration script reviewed and tested against dev database.

---

### Phase 1: Core Components (No External Dependencies)
**Duration**: 5–7 days  
**Goal**: Implement and unit-test the foundational components that have no inter-component dependencies.

**Implementation order follows the spec's hard dependency chain (items 1–2).**

#### Milestone 1.1: Password Hasher — `password-hasher.ts`
**Covers**: Component dependency for FR-AUTH.1, FR-AUTH.2, FR-AUTH.5; NFR-AUTH.3

- [ ] Implement `PasswordHasher` with bcrypt, cost factor 12
- [ ] Make cost factor configurable (RISK-3 mitigation: future Argon2id migration path)
- [ ] Unit tests:
  - Verify cost factor 12 is applied (NFR-AUTH.3)
  - Benchmark: hash timing ≈ 250ms (SC-3)
  - Correct hash verification for valid/invalid passwords
  - Password policy enforcement: min 8 chars, ≥1 uppercase, ≥1 lowercase, ≥1 digit (FR-AUTH.2 AC-3)

#### Milestone 1.2: JWT Service — `jwt-service.ts` (parallel with 1.3)
**Covers**: Component dependency for FR-AUTH.3, FR-AUTH.4; NFR-AUTH.1

- [ ] Implement `JwtService` with RS256 signing using key from secrets manager (decision from OQ-7)
- [ ] Access token generation with 15-minute TTL (FR-AUTH.1 AC-1, SC-5)
- [ ] Token verification and expiry validation
- [ ] Unit tests:
  - Token generation and decode round-trip
  - TTL assertions: access token 15min (SC-5)
  - Expired token rejection
  - Invalid/tampered token rejection
  - RS256 signature verification with public key

#### Milestone 1.3: Token Manager — `token-manager.ts` (parallel with 1.2)
**Covers**: FR-AUTH.3 (refresh token lifecycle); component dependency for FR-AUTH.1, FR-AUTH.4, FR-AUTH.5

- [ ] Implement `TokenManager` for refresh token issuance, rotation, and revocation
- [ ] Refresh token generation with 7-day TTL (FR-AUTH.1 AC-1, SC-5)
- [ ] Store refresh token hashes in database (FR-AUTH.3 AC-4)
- [ ] Refresh token rotation: invalidate previous, issue new (FR-AUTH.3 AC-1)
- [ ] Replay detection: reuse of revoked token → invalidate all user tokens (FR-AUTH.3 AC-3, SC-8)
- [ ] Enforce max active refresh tokens per user (decision from OQ-2)
- [ ] Unit tests:
  - Token issuance and hash storage
  - Rotation produces new token and invalidates old
  - Replay detection triggers full revocation (SC-8)
  - Expired refresh token rejection (FR-AUTH.3 AC-2)
  - Concurrent rotation behavior (per OQ-8 decision)

**Exit Criteria**: All three components pass unit tests independently. Cost factor benchmark meets SC-3. Token TTLs verified against SC-5.

---

### Phase 2: Service Layer & API Surface
**Duration**: 7–10 days  
**Goal**: Compose core components into `AuthService`, implement middleware, wire routes, and pass integration tests for all 5 functional requirements.

**Implementation order follows spec dependency chain (items 3–5).**

#### Milestone 2.1: Auth Service — `auth-service.ts`
**Covers**: FR-AUTH.1, FR-AUTH.2, FR-AUTH.3, FR-AUTH.5

- [ ] Implement `AuthService` as the sole external-facing orchestrator
  - Internal components (`TokenManager`, `JwtService`, `PasswordHasher`) are NOT exposed directly via HTTP
- [ ] **Login flow** (FR-AUTH.1):
  - Credential verification via `PasswordHasher`
  - Token issuance via `TokenManager` + `JwtService`
  - Rate limiting: 5 attempts/minute/IP (FR-AUTH.1 AC-4, SC-4)
  - Locked account handling → 403 (FR-AUTH.1 AC-3)
  - Generic error on invalid credentials — must not reveal which field was wrong (FR-AUTH.1 AC-2)
  - If OQ-3 resolved as v1.0: progressive account lockout (RISK-4 mitigation)
- [ ] **Registration flow** (FR-AUTH.2):
  - Email format validation (FR-AUTH.2 AC-4)
  - Password policy enforcement (FR-AUTH.2 AC-3)
  - Duplicate email detection → 409 (FR-AUTH.2 AC-2)
  - User record creation with hashed password → 201 (FR-AUTH.2 AC-1)
- [ ] **Token refresh flow** (FR-AUTH.3):
  - Valid refresh token → new access + rotated refresh token (FR-AUTH.3 AC-1)
  - Expired refresh token → 401 (FR-AUTH.3 AC-2)
  - Replayed revoked token → full user token invalidation (FR-AUTH.3 AC-3)
- [ ] **Password reset flow** (FR-AUTH.5):
  - Reset token generation, 1-hour TTL (FR-AUTH.5 AC-1, SC-7)
  - Email dispatch via selected email service (decision from OQ-1/OQ-6)
  - Reset token consumption and password update (FR-AUTH.5 AC-2)
  - Expired/invalid reset token → 400 (FR-AUTH.5 AC-3)
  - Session invalidation on successful reset (FR-AUTH.5 AC-4)

#### Milestone 2.2: Auth Middleware — `auth-middleware.ts`
**Covers**: FR-AUTH.4; integration into existing middleware chain

- [ ] Implement Bearer token extraction and verification via `TokenManager`
- [ ] Valid token → attach user context to request; proceed
- [ ] Invalid/expired token → 401 response (FR-AUTH.4 AC-2)
- [ ] Integrate into existing `src/middleware/auth-middleware.ts` — no new middleware framework

#### Milestone 2.3: Routes & Database Migration
**Covers**: All FR-AUTH requirements; deployment infrastructure

- [ ] Register routes under `/auth/*` group in `src/routes/index.ts`:
  - `POST /auth/login` (FR-AUTH.1)
  - `POST /auth/register` (FR-AUTH.2)
  - `POST /auth/refresh` (FR-AUTH.3)
  - `GET /auth/profile` (FR-AUTH.4) — protected by auth middleware
  - `POST /auth/forgot-password` + `POST /auth/reset-password` (FR-AUTH.5)
- [ ] Ensure refresh token delivered via httpOnly cookie (architectural constraint: XSS/CSRF mitigation)
- [ ] Sensitive fields (`password_hash`, `refresh_token_hash`) excluded from profile response (FR-AUTH.4 AC-3)
- [ ] Apply migration `003-auth-tables.ts`; verify down-migration rollback works
- [ ] Feature flag `AUTH_SERVICE_ENABLED` gates all new routes; existing unauthenticated endpoints unaffected

#### Integration Points — Dispatch & Wiring

| Named Artifact | Wired Components | Owning Phase | Consumed By |
|---|---|---|---|
| **Route registry** (`src/routes/index.ts`) | `/auth/*` route group wired to `AuthService` methods | Phase 2.3 | Phase 2.3 (HTTP surface), Phase 3 (E2E tests) |
| **Middleware chain** (`src/middleware/auth-middleware.ts`) | `TokenManager.verify()` injected into existing middleware pipeline | Phase 2.2 | Phase 2.3 (profile route), any future protected routes |
| **AuthService dependency injection** | `PasswordHasher`, `JwtService`, `TokenManager` composed into `AuthService` constructor | Phase 2.1 | Phase 2.1 (all auth flows), Phase 2.3 (route handlers) |
| **Feature flag** (`AUTH_SERVICE_ENABLED`) | Route-level conditional registration | Phase 0.2 (created), Phase 2.3 (consumed) | Phase 4 (deployment rollout) |
| **Database migration** (`003-auth-tables.ts`) | User table, RefreshToken table schemas | Phase 0.2 (authored), Phase 2.3 (applied) | Phase 1.3, Phase 2.1 (data access) |
| **Secrets manager integration** | RSA private key injected into `JwtService` at startup | Phase 0.2 (provisioned), Phase 1.2 (consumed) | Phase 2.1 (token signing), Phase 4 (key rotation) |
| **Email service adapter** | Email provider client wired into `AuthService` for FR-AUTH.5 | Phase 2.1 | Phase 2.1 (password reset dispatch) |

#### Integration Tests (Phase 2 exit gate)
- [ ] Login: valid credentials → 200 + tokens (FR-AUTH.1 AC-1)
- [ ] Login: invalid credentials → 401 generic error (FR-AUTH.1 AC-2)
- [ ] Login: locked account → 403 (FR-AUTH.1 AC-3)
- [ ] Login: rate limit → 429 on 6th attempt within 60s (SC-4)
- [ ] Registration: valid data → 201 + user profile (FR-AUTH.2 AC-1)
- [ ] Registration: duplicate email → 409 (FR-AUTH.2 AC-2)
- [ ] Registration: weak password → 400 with policy details (FR-AUTH.2 AC-3, SC-6)
- [ ] Registration: invalid email format → 400 (FR-AUTH.2 AC-4)
- [ ] Refresh: valid token → new tokens (FR-AUTH.3 AC-1)
- [ ] Refresh: expired token → 401 (FR-AUTH.3 AC-2)
- [ ] Refresh: replayed revoked token → full invalidation (FR-AUTH.3 AC-3, SC-8)
- [ ] Profile: valid token → user data without sensitive fields (FR-AUTH.4 AC-1, AC-3)
- [ ] Profile: expired/invalid token → 401 (FR-AUTH.4 AC-2)
- [ ] Password reset: registered email → reset email dispatched (FR-AUTH.5 AC-1)
- [ ] Password reset: valid reset token → password changed, sessions invalidated (FR-AUTH.5 AC-2, AC-4)
- [ ] Password reset: expired reset token → 400 (FR-AUTH.5 AC-3, SC-7)

**Exit Criteria**: All integration tests pass. All 5 functional requirements verified against acceptance criteria. Feature flag toggle verified (on/off).

---

### Phase 3: Non-Functional Validation & Hardening
**Duration**: 4–6 days  
**Goal**: Validate NFR targets, execute security review, and confirm all success criteria.

#### Milestone 3.1: Performance Validation
- [ ] k6 load test: login endpoint p95 < 200ms under normal load (NFR-AUTH.1, SC-1)
  - Profile the full login code path: bcrypt (~250ms) is the dominant contributor — the 200ms p95 target is tight
  - If target not met: evaluate bcrypt cost factor tuning, connection pooling, or async optimizations
- [ ] k6 load test: registration, refresh, profile endpoints under load
- [ ] Verify bcrypt hash timing benchmark (SC-3)
- [ ] Set up APM dashboard for production latency monitoring

#### Milestone 3.2: Security Hardening
- [ ] Verify RS256 key is loaded only from secrets manager, never from env vars or source (RISK-1 mitigation)
- [ ] Verify 90-day key rotation automation is functional
- [ ] Pen test: attempt to extract sensitive fields from profile endpoint (FR-AUTH.4 AC-3)
- [ ] Pen test: attempt credential enumeration via login/registration error messages
- [ ] Verify rate limiting cannot be bypassed via header manipulation
- [ ] If account lockout in scope (OQ-3): verify progressive lockout behavior (RISK-4)
- [ ] Confirm refresh token replay detection under concurrent load (RISK-2, SC-8)

#### Milestone 3.3: Availability & Observability
- [ ] Health check endpoint operational for uptime monitoring (NFR-AUTH.2, SC-2)
- [ ] PagerDuty alerting configured for auth service degradation
- [ ] Confirm OQ-4 decision: if audit logging deferred to v1.1, document the gap explicitly

**Exit Criteria**: All 8 success criteria (SC-1 through SC-8) validated. Security review complete with no critical findings. APM and alerting operational.

---

### Phase 4: Deployment & Rollout
**Duration**: 2–3 days  
**Goal**: Deploy behind feature flag, execute phased rollout, confirm production behavior.

#### Milestone 4.1: Staged Deployment
- [ ] Deploy with `AUTH_SERVICE_ENABLED=false` — verify existing endpoints unaffected
- [ ] Enable for internal/canary traffic; monitor APM for latency regression
- [ ] Enable for 10% → 50% → 100% of production traffic
- [ ] Verify 99.9% uptime target during rollout window (NFR-AUTH.2)

#### Milestone 4.2: Post-Deployment Verification
- [ ] Confirm production p95 latency matches load test results (SC-1)
- [ ] Verify key rotation schedule is active (90-day period)
- [ ] Confirm down-migration rollback procedure is documented and tested
- [ ] Remove or archive feature flag after full rollout is stable

**Exit Criteria**: Service running at 100% traffic. All success criteria confirmed in production. Rollback procedure validated.

---

## 3. Risk Assessment & Mitigation

| Risk | Severity | Phase Addressed | Mitigation | Residual Gap |
|------|----------|-----------------|------------|--------------|
| **RISK-1**: JWT private key compromise | High | Phase 0 (provisioning), Phase 1.2 (implementation), Phase 3.2 (verification) | RS256 + secrets manager + 90-day rotation | No emergency rotation procedure for active breach |
| **RISK-2**: Refresh token replay attack | High | Phase 1.3 (rotation logic), Phase 2 (integration test SC-8), Phase 3.2 (load verification) | Token rotation + replay detection + full revocation | Window between theft and first legitimate use; no anomaly alerting on rapid rotation |
| **RISK-3**: bcrypt cost factor insufficient | Medium | Phase 1.1 (configurable cost factor), Phase 3.1 (benchmark) | Configurable cost factor; Argon2id migration path documented | No automated review schedule or alerting |
| **RISK-4**: No progressive lockout | Medium | Phase 0 (scope decision OQ-3), Phase 2.1 (if in scope) | If v1.0: progressive lockout in `AuthService`; if v1.1: document gap | Distributed brute-force remains possible if deferred |
| **RISK-5**: Token state on user deletion | Medium | Phase 0 (scope decision OQ-5) | If v1.0: deletion hook with cascade revocation; if v1.1: document 7-day TTL gap | Depends on whether user deletion is a v1.0 use case |

**Architect's Risk Prioritization**:
1. RISK-1 and RISK-2 are the highest-priority items because they enable session hijacking. Both are addressed in the critical path.
2. The NFR-AUTH.1 latency target (< 200ms p95) is at tension with the bcrypt cost factor 12 (~250ms). This is a **known constraint conflict** — Phase 3.1 must profile the full code path early enough to course-correct if needed.
3. The email service dependency (OQ-6) is a **schedule risk** — if provider selection slips, FR-AUTH.5 cannot begin.

---

## 4. Resource Requirements & Dependencies

### External Dependencies (from Dependency Inventory)

| # | Dependency | Status | Blocking | Action Required |
|---|-----------|--------|----------|-----------------|
| 1 | `jsonwebtoken` library | Available | Phase 1.2 | Validate maintenance status and CVE history before adoption |
| 2 | `bcrypt` library | Available | Phase 1.1 | Standard; no concerns |
| 3 | RSA key pair (secrets manager) | **Requires OQ-7 resolution** | Phase 0.2 | Select platform; provision keys |
| 4 | Email service | **Requires OQ-1/OQ-6 resolution** | Phase 2.1 (FR-AUTH.5) | Select provider; define interface contract |
| 5 | User database table | Created in Phase 0.2 | Phase 1.3+ | Migration `003-auth-tables.ts` |
| 6 | RefreshToken database table | Created in Phase 0.2 | Phase 1.3+ | Migration `003-auth-tables.ts`; schema depends on OQ-2 |
| 7 | k6 + APM tooling | Available | Phase 3.1 | Confirm k6 installed; APM dashboard provisioned |

### Staffing Estimate
- **1 backend engineer** (primary): 3–4 weeks for Phases 1–3
- **1 security reviewer** (part-time): 2–3 days in Phase 3.2
- **1 DevOps engineer** (part-time): 2–3 days for secrets manager, key rotation, feature flag, deployment pipeline (Phases 0, 4)

### Parallel Work Opportunities
- Phase 1.2 (`jwt-service.ts`) and Phase 1.3 (`token-manager.ts`) can be developed in parallel once interfaces are defined
- Phase 3.1 (performance) and Phase 3.2 (security) can overlap
- Phase 0 decision resolution and infrastructure provisioning can proceed concurrently

---

## 5. Success Criteria & Validation

All 8 success criteria map to specific phases and test types:

| Criterion | Requirement Source | Phase Validated | Test Type |
|-----------|-------------------|-----------------|-----------|
| **SC-1**: Auth endpoint p95 < 200ms | NFR-AUTH.1 | Phase 3.1 | k6 load test + APM |
| **SC-2**: ≥ 99.9% uptime | NFR-AUTH.2 | Phase 3.3, Phase 4 | Health check monitoring |
| **SC-3**: Hash timing ≈ 250ms | NFR-AUTH.3 | Phase 1.1 | Unit benchmark |
| **SC-4**: Rate limiting 5/min/IP | FR-AUTH.1 AC-4 | Phase 2 integration tests | Integration: 6th attempt → 429 |
| **SC-5**: Token TTLs correct | FR-AUTH.1 AC-1, FR-AUTH.3 AC-1 | Phase 1.2, Phase 1.3 | Unit: JWT decode + expiry assertion |
| **SC-6**: Password policy enforced | FR-AUTH.2 AC-3 | Phase 1.1, Phase 2 | Unit + integration: boundary inputs |
| **SC-7**: Reset token 1-hour TTL | FR-AUTH.5 AC-1 | Phase 2 integration tests | Integration: use after 1 hour → 400 |
| **SC-8**: Replay detection → full revocation | FR-AUTH.3 AC-3 | Phase 1.3, Phase 2, Phase 3.2 | Unit + integration + load test |

**Definition of Done (v1.0)**: All SC-1 through SC-8 pass in both test and production environments. Feature flag removed. Rollback procedure documented and tested.

---

## 6. Timeline Summary

| Phase | Duration | Key Deliverables | Dependencies |
|-------|----------|------------------|--------------|
| **Phase 0**: Foundation | 3–5 days | OQ decisions resolved, infrastructure provisioned, migration ready | Stakeholder availability for OQ decisions |
| **Phase 1**: Core Components | 5–7 days | `PasswordHasher`, `JwtService`, `TokenManager` — unit tested | Phase 0 complete (secrets manager for jwt-service) |
| **Phase 2**: Service & API | 7–10 days | `AuthService`, middleware, routes — integration tested | Phase 1 complete; email service available (OQ-6) |
| **Phase 3**: NFR Validation | 4–6 days | Performance, security, availability validated against SC-1–SC-8 | Phase 2 complete; k6 + APM tooling ready |
| **Phase 4**: Deployment | 2–3 days | Phased rollout, production verification | Phase 3 complete |
| **Total** | **21–31 days** | | |

**Critical Path**: OQ-7 decision → Phase 0 infra → Phase 1.1 + 1.2/1.3 parallel → Phase 2.1 → Phase 2.2/2.3 → Phase 3 → Phase 4

**Schedule Risk**: The tightest constraint is the 200ms p95 latency target (SC-1) vs. the ~250ms bcrypt budget. If Phase 3.1 reveals this is infeasible, options include reducing bcrypt cost factor (security tradeoff), optimizing the surrounding code path, or renegotiating the latency SLO. Identify this early — run a quick benchmark in Phase 1.1 of the full expected code path, not just the hash operation in isolation.

---

## 7. Items Deferred to v1.1 (Confirmed Out of Scope)

Per spec and gap analysis:
- OAuth2/OIDC federation
- Multi-factor authentication
- Role-based access control (RBAC)
- Social login providers
- Authentication audit logging (OQ-4 — confirm deferral)
- Token revocation on user deletion (OQ-5 / RISK-5 — confirm deferral)
- Anomaly alerting on rapid token rotation (RISK-2 residual gap)
- Emergency key rotation procedure (RISK-1 residual gap)
