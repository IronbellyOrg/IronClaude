---
id: "AUTH-ROADMAP-V1"
title: "User Authentication Service - Roadmap"
source: "merged-prd-tdd-user-auth.md"
target_release: "v1.0 (2026-06-09)"
variant: "sonnet:analyzer"
---

# User Authentication Service — Roadmap

## Executive Summary

The User Authentication Service is the critical-path identity layer that unblocks ~$2.4M in projected annual revenue tied to Q2-Q3 2026 personalization features and is a hard prerequisite for the Q3 2026 SOC2 Type II audit. This roadmap delivers the v1.0 scope defined in AUTH-PRD-001 and AUTH-001-TDD — email/password authentication, JWT access + refresh tokens, profile retrieval, and self-service password reset — across five milestones (M1-M5) terminating in GA on 2026-06-09.

Delivery is structured as three phases mapped to six two-week sprints (12 weeks total, 2026-03-17 through 2026-06-09). Phase 1 (M1-M2) ships the backend `AuthService` with `PasswordHasher` and `TokenManager`; Phase 2 (M3-M4) adds password reset and frontend `LoginPage` / `RegisterPage` / `AuthProvider`; Phase 3 (M5) executes the three-stage feature-flag rollout (Internal Alpha → 10% Beta → 100% GA). Every milestone has a measurable exit gate tied to a specific FR/NFR ID, and every NFR has a benchmark or load test as its acceptance criterion.

Scope discipline is explicit: v1.0 ships email/password only. OAuth/social login (NG-001), MFA (NG-002), and RBAC enforcement (NG-003) are out of scope and deferred to v1.1, v1.2, and v2.0 respectively. The roles field exists on `UserProfile` but enforcement is downstream.

## Success Metrics

| Metric | Target | Baseline | Measurement Method | Source |
|--------|--------|----------|--------------------|--------|
| Login response time (p95) | < 200ms | N/A (greenfield) | APM on `AuthService.login()` | NFR-PERF-001 |
| Concurrent login capacity | 500 RPS | N/A | k6 load test | NFR-PERF-002 |
| Service availability | 99.9% / 30d rolling | N/A | Health-check uptime monitor | NFR-REL-001 |
| Token refresh latency (p95) | < 100ms | N/A | APM on `TokenManager.refresh()` | TDD §4.1 |
| Password hash time | < 500ms | N/A | Benchmark `PasswordHasher.hash()` at bcrypt cost 12 | NFR-SEC-001, TDD §4.1 |
| `JwtService` sign/verify | < 5ms | N/A | Unit benchmark | TDD §17 |
| Registration conversion | > 60% | N/A | Funnel landing → confirmed account | PRD §Success Metrics |
| Failed login rate | < 5% of attempts | N/A | Auth event log analysis | PRD §Success Metrics |
| Password reset completion | > 80% | N/A | Funnel: reset requested → new password set | PRD §Success Metrics |
| Avg session duration | > 30 minutes | N/A | Token refresh event analytics | PRD §Success Metrics |
| Unit test coverage | ≥ 80% | 0% | Jest coverage report on `AuthService`/`TokenManager`/`JwtService`/`PasswordHasher` | TDD §15.1, §24.1 |
| DAU (authenticated) | > 1000 within 30d of GA | 0 | `AuthToken` issuance counts | TDD §4.2 |

## Milestones

| ID | Name | Target Date | FR Coverage | Validation Gate |
|----|------|-------------|-------------|-----------------|
| M1 | Core AuthService | 2026-04-14 | FR-AUTH-001, FR-AUTH-002 | Unit + integration tests pass; bcrypt cost 12 verified |
| M2 | Token Management | 2026-04-28 | FR-AUTH-003, FR-AUTH-004 | Token lifecycle integration tests pass against Redis |
| M3 | Password Reset | 2026-05-12 | FR-AUTH-005 | Email delivery integration test; reset token TTL/single-use verified |
| M4 | Frontend Integration | 2026-05-26 | UX coverage for E1, E2, E3 | Playwright E2E suite green; `AuthProvider` silent-refresh verified |
| M5 | GA Release | 2026-06-09 | All FR + all NFR | 99.9% uptime over 7 days in production; flags removed |

### M1: Core AuthService — 2026-04-14

**Goal**: Deliver the registration and login backend such that a new user can be created and authenticated end-to-end against PostgreSQL with bcrypt-hashed credentials.

**Deliverables**:

- D1.1 `AuthService` skeleton with `login()` and `register()` orchestration methods (TDD §6.1, §10)
- D1.2 `PasswordHasher` module wrapping `bcryptjs` with cost factor 12 (NFR-SEC-001)
- D1.3 `UserProfile` PostgreSQL schema + migration (TDD §7.1): UUID PK, unique lowercased email index, 2-100 char displayName constraint, timestamps, default `roles=["user"]`
- D1.4 `POST /auth/login` endpoint with rate limit 10 req/min/IP and 401 generic error (TDD §8.2)
- D1.5 `POST /auth/register` endpoint with rate limit 5 req/min/IP, 409 on duplicate email, 400 on weak password (< 8 chars / no uppercase / no number)
- D1.6 Account lockout: 5 failed attempts within 15 minutes → 423 Locked (FR-AUTH-001 AC4)
- D1.7 Standard error envelope (`{ error: { code, message, status } }`) per TDD §8.3

**Validation**:

- Unit tests for `AuthService.login()` happy path, invalid-credentials path, lockout threshold
- Unit tests for `PasswordHasher.hash()` and `verify()` asserting cost factor == 12 (NFR-SEC-001 verification)
- Integration test: registration persists `UserProfile` to PostgreSQL via testcontainers (TDD §15.2)
- Integration test: duplicate email returns 409
- Benchmark: `PasswordHasher.hash()` median < 500ms on reference hardware

**Metrics**: Unit coverage ≥ 80% on `AuthService` + `PasswordHasher`; bcrypt cost asserted via unit test; 0 P0/P1 defects on FR-AUTH-001/002 acceptance criteria.

**Sprint Allocation**: Sprint 1-2 (2026-03-17 → 2026-04-14, 4 weeks).

### M2: Token Management — 2026-04-28

**Goal**: Stateless JWT-based session lifecycle is fully operational including refresh-token rotation and revocation, and `GET /auth/me` returns the authenticated profile.

**Deliverables**:

- D2.1 `JwtService` signing access tokens with RS256 + 2048-bit RSA keys (NFR-SEC-002), 15-minute TTL (`expiresIn: 900`)
- D2.2 `TokenManager` issuing refresh tokens (7-day TTL) stored as hashed values in Redis (TDD §13)
- D2.3 `AuthToken` response model: `accessToken`, `refreshToken`, `expiresIn`, `tokenType: "Bearer"` (TDD §7.1)
- D2.4 `POST /auth/refresh` endpoint with rotation (old token revoked, new pair issued) and rate limit 30 req/min/user
- D2.5 `GET /auth/me` endpoint (Bearer auth, 60 req/min/user) returning full `UserProfile` (FR-AUTH-004)
- D2.6 5-second clock-skew tolerance in `JwtService` verification (TDD §12)
- D2.7 Redis-unavailable fallback: reject refresh, force re-login (no stale tokens)
- D2.8 Audit log table + emitter for login success/failure, token issuance, refresh (SOC2 prerequisite)

**Validation**:

- Unit test: `TokenManager.refresh()` revokes old refresh token, issues new pair via `JwtService` (FR-AUTH-003)
- Unit test: expired refresh token returns 401
- Unit test: revoked refresh token returns 401
- Integration test: Redis TTL expiration correctly invalidates refresh tokens (TDD §15.2)
- Integration test: `GET /auth/me` with valid Bearer returns full `UserProfile` including `lastLoginAt`
- Benchmark: `JwtService.sign()` and `verify()` < 5ms each; `TokenManager` Redis ops < 10ms (TDD §17)

**Metrics**: Token refresh latency p95 < 100ms in integration env; unit coverage ≥ 80% on `TokenManager` + `JwtService`; zero token-leak findings in security review.

**Sprint Allocation**: Sprint 3 (2026-04-15 → 2026-04-28, 2 weeks).

### M3: Password Reset — 2026-05-12

**Goal**: Self-service password recovery via email is operational end-to-end with enumeration-resistant responses and single-use, time-limited reset tokens.

**Deliverables**:

- D3.1 `POST /auth/reset-request` endpoint accepting email; returns 200 regardless of registration status (enumeration prevention, PRD §Error Handling)
- D3.2 `POST /auth/reset-confirm` endpoint validating reset token and updating password hash via `PasswordHasher`
- D3.3 Reset token storage (Redis, 1-hour TTL, single-use flag) — used tokens cannot be reused (FR-AUTH-005 AC4)
- D3.4 SendGrid integration for password reset email delivery; template with 1-hour TTL link
- D3.5 Password update invalidates all existing refresh tokens for that user via `TokenManager` (PRD AC for FR-AUTH.5)
- D3.6 Delivery monitoring + alerting on SendGrid failures (R-Email mitigation)

**Validation**:

- Integration test: reset for unregistered email returns 200, no email sent
- Integration test: reset token used twice → second use returns 401
- Integration test: expired reset token (> 1 hour) returns 401
- Integration test: successful password reset invalidates all prior refresh tokens
- E2E test (initial): full request → email → confirm flow against staging SendGrid sandbox
- Email delivery latency: 95% of reset emails delivered within 60 seconds (PRD AC)

**Metrics**: Reset token expiry asserted; email delivery success rate > 99% in staging; zero enumeration leaks confirmed by security review of response timing.

**Sprint Allocation**: Sprint 4 (2026-04-29 → 2026-05-12, 2 weeks).

### M4: Frontend Integration — 2026-05-26

**Goal**: Frontend components consume the `AuthService` API end-to-end and silent token refresh works under realistic browser behavior.

**Deliverables**:

- D4.1 `LoginPage` component (TDD §10.2): email/password form, calls `POST /auth/login`, stores `AuthToken` via `AuthProvider`, no user enumeration in error messages
- D4.2 `RegisterPage` component: client-side password strength validation, calls `POST /auth/register`, redirects to login on success
- D4.3 `AuthProvider` context: in-memory `accessToken` (R-001 mitigation), HttpOnly cookie for refreshToken, silent refresh on 401, clears tokens on tab close
- D4.4 `ProfilePage` route consuming `GET /auth/me`
- D4.5 Protected-route wrapper redirecting unauthenticated users to `/login`
- D4.6 Feature flag wiring for `AUTH_NEW_LOGIN` and `AUTH_TOKEN_REFRESH` (TDD §19.2)

**Validation**:

- Playwright E2E: register → login → view profile (full journey, FR-AUTH-001/002/004)
- Playwright E2E: `AuthProvider` silent refresh after 15-min access token expiry (simulated via clock advance)
- Playwright E2E: password reset flow from `LoginPage` → email → set new password → re-login
- Playwright E2E: protected route redirects unauthenticated user to `LoginPage`
- Manual: token cleared on tab close (R-001 verification)

**Metrics**: E2E suite green (5% of test pyramid per TDD §15.1); zero P0/P1 bugs on Phase 1 exit checklist; staging passes all release-checklist items in TDD §24.2.

**Sprint Allocation**: Sprint 5 (2026-05-13 → 2026-05-26, 2 weeks).

### M5: GA Release — 2026-06-09

**Goal**: Authentication service is live for 100% of traffic with all feature flags removed and 7 days of stable production operation.

**Deliverables**:

- D5.1 Internal Alpha deploy to staging behind `AUTH_NEW_LOGIN=ON` for auth-team + QA (1 week per TDD §19.1)
- D5.2 Beta rollout: `AUTH_NEW_LOGIN=ON` for 10% of traffic (2 weeks)
- D5.3 GA: 100% traffic on new `AuthService`, legacy endpoints deprecated
- D5.4 Feature flags `AUTH_NEW_LOGIN` and `AUTH_TOKEN_REFRESH` removed post-GA
- D5.5 Monitoring dashboards live: `auth_login_total`, `auth_login_duration_seconds`, `auth_token_refresh_total`, `auth_registration_total` (TDD §14)
- D5.6 Alerts configured: login failure rate > 20% over 5min, p95 latency > 500ms, Redis connection failures
- D5.7 Runbook published (TDD §25.1); on-call rotation in place for first 2 weeks post-GA
- D5.8 Rollback procedure tested in staging (TDD §19.3)

**Validation**:

- Load test (k6): 500 concurrent login RPS sustained, p95 < 200ms (NFR-PERF-001, NFR-PERF-002)
- Beta phase gate: p95 < 200ms, error rate < 0.1%, zero Redis connection failures over 2 weeks
- GA phase gate: 99.9% uptime over first 7 days (NFR-REL-001)
- Security review: bcrypt cost 12 verified in prod config; RS256 key rotation documented; CORS restricted to known origins (TDD §13, §24.1)
- All TDD §24.2 release checklist items signed off by test-lead and eng-manager

**Metrics**: 99.9% uptime (rolling 30d goal, 7d at GA); login p95 < 200ms in production; zero rollback triggers fired during Beta or GA (TDD §19.4 thresholds: p95 > 1000ms / 5min, error > 5% / 2min, Redis failures > 10/min).

**Sprint Allocation**: Sprint 6 (2026-05-27 → 2026-06-09, 2 weeks).

## Sprint-Level Breakdown

| Sprint | Window | Milestones | Owner | Primary Deliverables |
|--------|--------|------------|-------|----------------------|
| S1 | 2026-03-17 → 2026-03-31 | M1 (part 1) | auth-team backend | D1.1 `AuthService` skeleton; D1.2 `PasswordHasher`; D1.3 `UserProfile` schema |
| S2 | 2026-04-01 → 2026-04-14 | M1 (part 2) | auth-team backend | D1.4-D1.7 login/register endpoints + lockout + error envelope |
| S3 | 2026-04-15 → 2026-04-28 | M2 | auth-team backend | D2.1-D2.8 `TokenManager` + `JwtService` + `/auth/me` + `/auth/refresh` + audit log |
| S4 | 2026-04-29 → 2026-05-12 | M3 | auth-team backend + platform-team (SendGrid) | D3.1-D3.6 password reset flow + email integration |
| S5 | 2026-05-13 → 2026-05-26 | M4 | frontend-team + auth-team | D4.1-D4.6 `LoginPage`, `RegisterPage`, `AuthProvider`, `ProfilePage` |
| S6 | 2026-05-27 → 2026-06-09 | M5 | auth-team + platform-team | D5.1-D5.8 phased rollout, monitoring, runbook, GA cutover |

## Validation Strategy

Validation follows the test pyramid in TDD §15.1: 80% unit / 15% integration / 5% E2E. Every FR-AUTH-NNN has at least one unit test and one integration test; high-traffic flows additionally have E2E coverage.

| FR | Unit Validation | Integration Validation | E2E Validation |
|----|-----------------|------------------------|----------------|
| FR-AUTH-001 (login) | `AuthService.login()` happy + invalid-credentials + lockout (TDD §15.2) | `POST /auth/login` against PostgreSQL with bcrypt-hashed seed user | Playwright login flow via `LoginPage` |
| FR-AUTH-002 (register) | `AuthService.register()` validation: duplicate email, weak password | Registration persists `UserProfile` to PostgreSQL (TDD §15.2) | Playwright register → first login |
| FR-AUTH-003 (tokens) | `TokenManager.refresh()` rotation; `JwtService.sign()`/`verify()` | Expired refresh token rejected by Redis TTL (TDD §15.2) | `AuthProvider` silent refresh in Playwright |
| FR-AUTH-004 (profile) | `AuthService.getMe()` returns full `UserProfile` shape | `GET /auth/me` with Bearer returns 200 + all fields | `ProfilePage` renders post-login |
| FR-AUTH-005 (reset) | Reset-token single-use + 1h expiry logic | Full request → confirm flow against staging SendGrid | Playwright full reset journey |

NFR validation is gated at M5 entry:

- NFR-PERF-001 (p95 < 200ms): k6 load test in staging before Beta
- NFR-PERF-002 (500 concurrent): k6 sustained-load test before Beta
- NFR-REL-001 (99.9% uptime): measured over 7 days post-GA via health-check monitor
- NFR-SEC-001 (bcrypt cost 12): unit test asserts `PasswordHasher` cost parameter (TDD §15.2)
- NFR-SEC-002 (RS256 / 2048-bit): configuration validation test in CI

## Risk Matrix

| ID | Risk | Probability | Impact | Inherent Risk | Mitigation | Residual Risk | Source |
|----|------|-------------|--------|---------------|------------|---------------|--------|
| R-001 | Token theft via XSS hijacks session | Medium | High | High | In-memory accessToken only; HttpOnly cookie for refresh; 15-min access TTL; `TokenManager` revocation | Low | TDD §20 R-001 |
| R-002 | Brute-force on `/auth/login` | High | Medium | High | API Gateway 10 req/min/IP rate limit; 5-attempt lockout in `AuthService`; bcrypt cost 12; CAPTCHA fallback after 3 failures | Low | TDD §20 R-002 |
| R-003 | Data loss during legacy auth migration | Low | High | Medium | Parallel run during Phase 1+2; idempotent `UserProfile` upserts; full DB backup before each phase | Low | TDD §20 R-003 |
| R-EMAIL | SendGrid delivery failure blocks password reset | Low | Medium | Low | Delivery monitoring + alerting; fallback support channel; queue retries | Low | PRD §Risk Analysis |
| R-COMPLIANCE | Incomplete audit logging fails SOC2 | Medium | High | High | Audit log table specified in M2 (D2.8); SOC2 control mapping validated in QA before GA | Low | PRD §Risk Analysis |
| R-LATENCY | bcrypt cost 12 (~300ms hash) + DB I/O breaches 200ms p95 | Medium | Medium | Medium | Connection pooling (TDD §17); `JwtService` < 5ms; Redis < 10ms; k6 gate at M5 entry | Low | TDD §17, NFR-PERF-001 |
| R-REDIS | Redis outage prevents refresh, mass re-login | Low | Medium | Low | TDD §12 fallback rejects refresh (safer than stale); HPA-scaled Redis cluster (TDD §25.3); 2GB scale trigger at 70% util | Low | TDD §12, §25.3 |

## Performance & Reliability Gates

Hard gates blocking promotion from one phase to the next:

| Gate | Threshold | Phase Boundary | Source |
|------|-----------|----------------|--------|
| Login p95 latency | < 200ms | Alpha → Beta | NFR-PERF-001 |
| Concurrent login capacity | 500 RPS sustained | Alpha → Beta | NFR-PERF-002 |
| Error rate | < 0.1% | Beta → GA | TDD §19.1 |
| Redis connection failures | 0 over 2-week Beta | Beta → GA | TDD §19.1 |
| Uptime | 99.9% over first 7 days | GA exit | NFR-REL-001 |
| Unit test coverage | ≥ 80% on core components | M1, M2 exit | TDD §24.1 |
| bcrypt cost factor | == 12 (asserted) | M1 exit | NFR-SEC-001 |
| JWT signing algorithm | == RS256 + 2048-bit RSA | M2 exit | NFR-SEC-002 |
| Rollback trigger thresholds | Not breached | Every phase | TDD §19.4 |

Rollback is triggered immediately and automatically if any of the following fire during Beta or GA (TDD §19.4): p95 > 1000ms for > 5 min; error rate > 5% for > 2 min; Redis connection failures > 10/min; any `UserProfile` data corruption.

## Rollout Plan

**Phase 1 — Internal Alpha (2026-05-27 → 2026-06-02, 1 week)**

- Audience: auth-team + QA only, behind `AUTH_NEW_LOGIN` feature flag
- Entry gate: M4 complete; all E2E tests green; release checklist (TDD §24.2) signed by test-lead
- Exit gate: All FR-AUTH-001 through FR-AUTH-005 pass manual testing; zero P0/P1 bugs
- Measurement: Manual test matrix + automated regression suite; staging dashboards green

**Phase 2 — Beta 10% (2026-06-03 → 2026-06-09, ~1 week compressed; TDD §19.1 nominal 2w if schedule permits)**

- Audience: 10% production traffic via flag-based traffic splitter
- Entry gate: Alpha exit gate met
- Exit gate: p95 < 200ms; error rate < 0.1%; zero Redis connection failures
- Measurement: Prometheus dashboards (`auth_login_duration_seconds`, `auth_login_total`); APM traces; on-call alerts silent

**Phase 3 — GA 100% (2026-06-09 onward)**

- Audience: 100% of users
- Entry gate: Beta exit gate met
- Exit gate: 99.9% uptime over first 7 days; flags removed; runbook validated against at least one real incident drill
- Measurement: NFR-REL-001 uptime monitor; rollback triggers from TDD §19.4 not fired

Note: Per PRD timeline (target Q2 2026 / 2026-06-09) the TDD's nominal 4-week rollout window (1w Alpha + 2w Beta + 1w GA) is compressed; if Alpha or Beta gates slip, GA shifts right rather than compressing further — quality gates are non-negotiable.

## Out-of-Scope (explicit)

v1.0 explicitly excludes the following per TDD §3.2 and PRD §Scope Definition. These appear in this section solely to prevent scope creep — they are not roadmap items:

| Capability | Deferred To | Rationale |
|------------|-------------|-----------|
| OAuth / OIDC / social login (Google, GitHub) | v1.1 (NG-001) | Requires third-party integration infrastructure |
| Multi-factor authentication (SMS/TOTP) | v1.2 (NG-002) | Separate feature; requires SMS/TOTP vendor selection |
| Role-based access control enforcement | v2.0 (NG-003) | Authorization is a distinct PRD; `roles` field exists but is not enforced by `AuthService` |
| API-key authentication for service-to-service | v1.1 (OQ-001) | Open question pending v1.1 scope discussion |
| "Remember me" extended session duration | TBD (PRD OQ-4) | Open question, owner: Product |
| Account lockout policy beyond 5/15min | v1.1 candidate (PRD OQ-3) | Owner: Security |

Anything not on the in-scope list is out-of-scope by construction. New asks during the build must be triaged to a future release and added to the deferred-list, not absorbed into v1.0.

## Open Questions

| ID | Question | Owner | Target Resolution | Source |
|----|----------|-------|-------------------|--------|
| OQ-001 | Should `AuthService` support API-key auth for service-to-service? | test-lead | 2026-04-15 (before M2 exit) | TDD §22 |
| OQ-002 | Maximum allowed `UserProfile.roles` array length? | auth-team | 2026-04-01 (before M2) | TDD §22 |
| OQ-003 | Password reset emails: sync vs async delivery? | Engineering | 2026-04-22 (before M3 start) | PRD §Open Questions |
| OQ-004 | Maximum refresh tokens per user across devices? | Product | 2026-04-22 (before M3 start) | PRD §Open Questions |
| OQ-005 | Account lockout policy after N failed attempts (confirm 5/15min default)? | Security | 2026-04-08 (before M1 exit) | PRD §Open Questions |
| OQ-006 | "Remember me" support to extend session duration? | Product | 2026-05-06 (before M4) | PRD §Open Questions |

Open questions that miss their target resolution date escalate to the eng-manager for explicit defer-or-decide; none may remain open at M5 entry.
