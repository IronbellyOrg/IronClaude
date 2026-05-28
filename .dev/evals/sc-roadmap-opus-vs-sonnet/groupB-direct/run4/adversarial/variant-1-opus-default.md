---
id: "AUTH-ROADMAP-001"
title: "User Authentication Service — Engineering Roadmap"
source: "AUTH-MERGED-PRD-TDD (merged-prd-tdd-user-auth.md)"
target_release: "v1.0"
owning_team: "auth-team"
status: "Draft"
variant: "opus-default"
generated: "2026-05-22"
---

# User Authentication Service — Engineering Roadmap

## 1. Roadmap Overview

**Vision Statement.** Deliver a secure, stateless, standards-compliant identity layer (`AuthService` + `TokenManager` + `JwtService` + `PasswordHasher`) that unblocks the Q2-Q3 2026 personalization roadmap, satisfies SOC2 Type II audit trail requirements, and gives every user a frictionless registration, login, session-persistence, and self-service password-reset experience.

**Target Release.** v1.0 — General Availability (GA) on **2026-06-09** per TDD §23.1 M5.

**Total Estimated Duration.** 11 calendar weeks (2026-03-30 → 2026-06-15), of which 9 weeks are build + integration (M1 → M4) and 2 weeks are phased rollout + stabilization (M5). The TDD anchors M1 at 2026-04-14; this roadmap back-fills a 2-week foundation sprint (M0) starting 2026-03-30 to absorb infrastructure provisioning, schema migrations, and policy resolution before code lands on `AuthService`.

**Phasing Summary.**

| Phase | TDD §19 Anchor | Window | Milestones | Theme |
|-------|----------------|--------|------------|-------|
| Phase 0 | (added) | 2026-03-30 → 2026-04-13 | M0 | Foundation: infra, schemas, contracts, policy decisions |
| Phase 1 | M1-M2 | 2026-04-14 → 2026-04-28 | M1, M2 | Core `AuthService` + `TokenManager`/`JwtService` |
| Phase 2 | M3-M4 | 2026-04-29 → 2026-05-26 | M3, M4 | Password reset + frontend (`LoginPage`, `RegisterPage`, `AuthProvider`) |
| Phase 3 | M5 | 2026-05-27 → 2026-06-15 | M5 | Internal Alpha → Beta 10% → GA 100% |

**Workstream Capacity (engineer-weeks).** Backend Core 14 EW · Token & Crypto 8 EW · Frontend 7 EW · Security & Compliance 5 EW · Observability & SRE 4 EW · QA/Test 6 EW · Tech Lead/PM 4 EW · **Total ≈ 48 EW** across 11 calendar weeks.

---

## 2. Milestones

Six milestones: M0 (added foundation), then M1-M5 from TDD §23.1. Dates anchored to TDD targets; M0 dates are derived back from M1=2026-04-14.

### M0 — Foundation, Contracts, and Policy Resolution

| Field | Value |
|-------|-------|
| **ID** | M0 |
| **Name** | Foundation, Contracts, and Policy Resolution |
| **Target Date** | 2026-04-13 (2-week sprint, starts 2026-03-30) |
| **Scope (FR/NFR)** | Enabling work for FR-AUTH-001..005 and NFR-PERF-001/002, NFR-REL-001, NFR-SEC-001/002. No FR is completed in M0 — this milestone resolves dependencies. |
| **Deliverables** | (1) PostgreSQL 15 instance provisioned + `UserProfile` migration (id UUID PK, email UNIQUE indexed lowercased, displayName 2-100 chars, createdAt/updatedAt/lastLoginAt, roles default `["user"]`) + audit_log table (90-day retention). (2) Redis 7 cluster provisioned with 1 GB memory budget. (3) RS256 RSA 2048-bit keypair generated, stored in secrets manager, rotation runbook drafted. (4) SendGrid account + API key, sandbox templates for password-reset email. (5) OpenAPI 3.1 contract for `/v1/auth/login`, `/v1/auth/register`, `/v1/auth/me`, `/v1/auth/refresh`, `/v1/auth/reset-request`, `/v1/auth/reset-confirm` matching TDD §8. (6) Feature flag scaffolding for `AUTH_NEW_LOGIN` and `AUTH_TOKEN_REFRESH` (default OFF). (7) Decision records for the 4 PRD open questions + OQ-001/OQ-002 (see §9). (8) Threat model draft against OWASP ASVS L2. |
| **Dependencies** | SEC-POLICY-001 sign-off; SendGrid procurement; platform-team to allocate PostgreSQL 15 and Redis 7 capacity. |
| **Exit Criteria** | (1) `make migrate` against staging PostgreSQL applies `UserProfile` and audit_log schemas with zero errors. (2) Redis `PING` returns `PONG` from `AuthService` staging pod. (3) RSA keypair load test: `JwtService` can sign+verify 1000 tokens in < 5s. (4) SendGrid test send: reset email delivered to test inbox in < 60s. (5) OpenAPI spec validated by Spectral linter with zero errors. (6) All 6 open questions either resolved with decision record OR scheduled with explicit owner + decision date. |
| **Estimated Effort** | 8 EW (Backend 3, Platform/SRE 2, Security 1.5, PM/Tech Lead 1.5) |

### M1 — Core `AuthService` (Login + Registration)

| Field | Value |
|-------|-------|
| **ID** | M1 |
| **Name** | Core AuthService — Login and Registration |
| **Target Date** | 2026-04-14 (per TDD §23.1) — 2-week sprint 2026-03-31 → 2026-04-14 (overlaps M0 final week) |
| **Scope (FR/NFR)** | FR-AUTH-001 (login), FR-AUTH-002 (registration), partial NFR-PERF-001 (login p95 < 200ms), NFR-SEC-001 (bcrypt cost 12), GDPR consent capture at registration. |
| **Deliverables** | (1) `AuthService.login(email, password)` orchestrator. (2) `AuthService.register(email, password, displayName, consentTimestamp)` orchestrator. (3) `PasswordHasher.hash()` and `PasswordHasher.verify()` over `bcryptjs` with cost factor 12 (asserted by unit test). (4) `UserRepo` with parameterized queries, email lowercase normalization, unique-constraint violation handling (returns 409 distinct from 500). (5) POST `/v1/auth/login` returning `AuthToken` envelope (stub `accessToken`/`refreshToken` until M2). (6) POST `/v1/auth/register` returning 201 + `UserProfile`. (7) Account-lockout state machine: 5 failed attempts in 15-minute rolling window → 423 Locked + audit log + admin notification. (8) Generic 401 response for unknown email AND wrong password (no user enumeration — proven by response-shape parity test). (9) Password policy validator (≥8 chars, ≥1 uppercase, ≥1 number) per FR-AUTH-002 AC#3. (10) Structured audit log emission on every login attempt (success + failure) with user_id, IP, timestamp, outcome. |
| **Dependencies** | M0 complete (schema, Redis, OpenAPI). |
| **Exit Criteria** | (1) Unit coverage for `AuthService.login`, `AuthService.register`, `PasswordHasher` ≥ 85% lines, ≥ 80% branches (TDD §15.1 target is 80%; this milestone exceeds by 5pp to leave headroom). (2) Integration test: registration → login round-trip against testcontainers PostgreSQL passes in CI. (3) Bcrypt cost-factor unit test asserts cost=12 (NFR-SEC-001 evidence). (4) Enumeration parity test: response shape, status code, and timing variance for unknown-email vs wrong-password indistinguishable (timing within ±15ms). (5) Concurrent registration test: 50 parallel POSTs with same email yield exactly 1 success + 49 × 409. (6) Lockout test: 5 failed attempts within 15 min triggers 423 + audit row; 6th attempt within window blocked; cooldown after 15 min unlocks. (7) Password never appears in any log line — verified by grepping CI log stream for known test password. (8) Login p95 < 200ms in single-pod load test at 100 RPS. |
| **Estimated Effort** | 10 EW (Backend 5, Security 1.5, QA 2, Tech Lead 1.5) |

### M2 — Token Management (`TokenManager` + `JwtService` + `/auth/me` + `/auth/refresh`)

| Field | Value |
|-------|-------|
| **ID** | M2 |
| **Name** | Token Management |
| **Target Date** | 2026-04-28 (per TDD §23.1) — 2-week sprint 2026-04-15 → 2026-04-28 |
| **Scope (FR/NFR)** | FR-AUTH-003 (token issuance + refresh), FR-AUTH-004 (profile retrieval), NFR-PERF-001 (refresh p95 < 100ms per TDD §4.1), NFR-SEC-002 (RS256 2048-bit keys). |
| **Deliverables** | (1) `JwtService.sign(payload)` and `JwtService.verify(token)` using RS256 with 2048-bit RSA keys, 5-second clock-skew tolerance (TDD §12 invariant). (2) `TokenManager.issueTokens(userId)` producing 15-min access token + 7-day opaque refresh token. (3) Refresh tokens stored in Redis as **hashed** values (SHA-256 of opaque token) — TDD §13 invariant. (4) `TokenManager.refresh(refreshToken)` with atomic revoke-and-reissue (rotates refresh token; old token marked revoked). (5) POST `/v1/auth/refresh` returning new `AuthToken` pair. (6) GET `/v1/auth/me` returning `UserProfile` including `lastLoginAt` updated by login flow. (7) Token revocation API (internal): `TokenManager.revokeAllForUser(userId)` used by password reset and admin lock. (8) JWT payload schema: `sub` (user id), `roles`, `iat`, `exp`, `iss`, `aud`. (9) Redis-unavailability fallback: refresh requests return 503 (NOT serve stale tokens) per TDD §12 invariant. (10) Quarterly RSA key rotation runbook. |
| **Dependencies** | M1 complete (login flow produces real tokens). M0 RSA keys + Redis. |
| **Exit Criteria** | (1) Unit coverage for `TokenManager`, `JwtService` ≥ 85%. (2) RS256 key-bit-length unit test asserts 2048 (NFR-SEC-002 evidence). (3) Clock-skew test: token issued at T with `iat=T+4s` and `iat=T-4s` both verify; `iat=T+6s` rejects. (4) Refresh-token hashing test: raw token stored in Redis never matches token returned to client (SHA-256 verified). (5) Refresh rotation test: old refresh token returns 401 after single use; new token works exactly once. (6) Redis-down test (testcontainer Redis paused): `/auth/refresh` returns 503, NOT 200 with stale token. (7) Token-revocation test: password change invalidates all outstanding refresh tokens for that user. (8) `/auth/me` integration test: valid token → `UserProfile` with all 7 fields populated; expired token → 401. (9) Refresh p95 < 100ms at 100 RPS. (10) Login + refresh combined p95 < 200ms at 500 concurrent (NFR-PERF-002 evidence). |
| **Estimated Effort** | 9 EW (Backend 4, Security 2, QA 2, SRE 1) |

### M3 — Password Reset (FR-AUTH-005)

| Field | Value |
|-------|-------|
| **ID** | M3 |
| **Name** | Password Reset with Email Verification |
| **Target Date** | 2026-05-12 (per TDD §23.1) — 2-week sprint 2026-04-29 → 2026-05-12 |
| **Scope (FR/NFR)** | FR-AUTH-005, NFR-SEC (enumeration prevention on reset endpoint), GDPR (reset event audit trail). |
| **Deliverables** | (1) POST `/v1/auth/reset-request` accepting email; always returns 200 within ±10ms timing variance (no enumeration). (2) Reset token generation: 32-byte cryptographically random, stored hashed in Redis with 1-hour TTL, single-use marker. (3) SendGrid integration with templated email (delivered < 60s p95 per PRD success metric). (4) POST `/v1/auth/reset-confirm` accepting reset token + new password; validates token, applies password policy, calls `PasswordHasher.hash()`, persists new hash, **invokes `TokenManager.revokeAllForUser()` to invalidate every existing session** (TDD §15.2 + FR-AUTH-005 AC). (5) Used-token rejection: same token reused returns 401. (6) Expired-token rejection: > 1-hour-old token returns 401 with "Request a new reset link" message. (7) Audit log: `reset_requested`, `reset_completed`, `reset_failed_invalid_token`, `reset_failed_expired_token` events. (8) Rate limit on `/reset-request`: 3 req/min per email (mitigates reset-spam abuse). |
| **Dependencies** | M2 complete (`TokenManager.revokeAllForUser` exists). M0 SendGrid integration verified. |
| **Exit Criteria** | (1) Unit coverage for reset flow ≥ 85%. (2) Enumeration parity test: response for registered vs unregistered email identical in shape, status, AND timing (±10ms). (3) Single-use test: reset token used once → 200; same token used again → 401. (4) TTL test: token 59 min old works, 61 min old fails with explicit "expired" code. (5) Session-invalidation test: complete password reset → ALL outstanding refresh tokens for user return 401 on next `/auth/refresh`. (6) SendGrid delivery test: 95th-percentile delivery latency < 60s across 100-message sample. (7) Rate limit test: 4th `/reset-request` for same email within 1 min returns 429. (8) Password-never-logged grep test passes for reset confirmation path. |
| **Estimated Effort** | 7 EW (Backend 3, Security 1, QA 1.5, SRE 0.5, PM 1) |

### M4 — Frontend Integration (`LoginPage`, `RegisterPage`, `AuthProvider`, `ProfilePage`)

| Field | Value |
|-------|-------|
| **ID** | M4 |
| **Name** | Frontend Integration |
| **Target Date** | 2026-05-26 (per TDD §23.1) — 2-week sprint 2026-05-13 → 2026-05-26 |
| **Scope (FR/NFR)** | Frontend-side coverage of FR-AUTH-001..005 + AC for AUTH-E1, AUTH-E2, AUTH-E3 user stories. NFR: 200ms perceived login latency, no token leakage. |
| **Deliverables** | (1) `LoginPage` component: email + password fields, inline validation, submit calls POST `/v1/auth/login`, on success delegates to `AuthProvider`. (2) `RegisterPage` component: email + password + displayName fields, client-side password-strength validation matching FR-AUTH-002 policy, GDPR consent checkbox with timestamp capture. (3) `AuthProvider` React context: holds `AuthToken` **in memory only** (NOT localStorage per R-001 mitigation); refresh token stored in HttpOnly cookie set by backend; manages silent refresh 60s before access-token expiry; exposes `useAuth()` hook with `user: UserProfile | null`, `login`, `logout`, `isAuthenticated`. (4) `ProfilePage` component calling GET `/v1/auth/me`, rendering displayName/email/createdAt. (5) Forgot-password flow UI: `/forgot-password` page → enter email → confirmation screen → email link → `/reset-password?token=...` page → new password form. (6) `AuthProvider` clears tokens on tab close/visibility change (R-001 mitigation). (7) 401 interceptor: on any 401 from protected API, attempt silent refresh once, on second 401 redirect to `LoginPage`. (8) Generic error UI for "Invalid email or password" (no enumeration leakage in frontend either). |
| **Dependencies** | M2 complete (real `/auth/me` and `/auth/refresh` endpoints). M3 complete (reset endpoints). Backend feature flag `AUTH_NEW_LOGIN` wired. |
| **Exit Criteria** | (1) E2E test (Playwright): registration → logout → login → profile view → logout passes against staging. (2) E2E test: forgot-password → email link → new password → all old sessions invalidated → new login works. (3) E2E test: silent refresh fires within 60s of access-token expiry without user interaction. (4) E2E test: tab close clears in-memory token (verify by reopening tab → must re-authenticate). (5) Token-in-localStorage scan: grep frontend bundle and runtime DOM for `accessToken` in `localStorage`/`sessionStorage` → must return zero matches. (6) Lighthouse performance score for `LoginPage` first-paint < 1s (PRD journey requirement). (7) Accessibility audit: `LoginPage` and `RegisterPage` pass WCAG 2.1 AA via axe-core (deferred per TDD §16 but committed by frontend-team). (8) Frontend unit coverage ≥ 80% on `AuthProvider`. |
| **Estimated Effort** | 7 EW (Frontend 5, QA 1.5, Tech Lead 0.5) |

### M5 — Phased GA Rollout

| Field | Value |
|-------|-------|
| **ID** | M5 |
| **Name** | Phased GA Rollout (Internal Alpha → Beta 10% → GA 100%) |
| **Target Date** | 2026-06-09 (per TDD §23.1) — 3-week window 2026-05-27 → 2026-06-15 (Alpha 1w + Beta 2w; GA flag-flip 2026-06-09) |
| **Scope (FR/NFR)** | All FR-AUTH-001..005 in production; NFR-REL-001 (99.9% uptime); NFR-PERF-001/002 under real load; SOC2 audit-trail validation. |
| **Deliverables** | (1) Internal Alpha (2026-05-27 → 2026-06-02): `AuthService` deployed to staging; auth-team and QA exercise all endpoints; `AUTH_NEW_LOGIN`=ON for staging only. (2) Beta 10% (2026-06-03 → 2026-06-09): `AUTH_NEW_LOGIN`=ON for 10% production traffic via API Gateway header-based routing; `AUTH_TOKEN_REFRESH`=ON. (3) GA 100% (2026-06-09 onward): `AUTH_NEW_LOGIN` removed; all users on new flow. (4) `AUTH_TOKEN_REFRESH` flag removed 2026-06-23 (Phase 3 + 2 weeks per TDD §19.2). (5) Monitoring dashboards (Grafana): `auth_login_total`, `auth_login_duration_seconds`, `auth_token_refresh_total`, `auth_registration_total`, login-failure rate, lockout rate, Redis connection failures, SendGrid delivery latency. (6) Alerting: login failure > 20%/5min; p95 > 500ms; Redis connection failures > 10/min (per TDD §14). (7) Rollback runbook tested in staging once before each phase transition. (8) Post-launch review at 2026-06-23 (T+2w) and 2026-07-09 (T+30d) against success metrics. |
| **Dependencies** | M1-M4 all complete. Operational readiness items from TDD §25.1 (runbook), §25.2 (on-call rotation), §25.3 (capacity planning) signed off. |
| **Exit Criteria** | (1) Internal Alpha: zero P0/P1 bugs across 1-week soak (TDD §19.1 Phase 1). (2) Beta 10%: p95 latency < 200ms, error rate < 0.1%, zero `TokenManager` Redis failures over 2-week window (TDD §19.1 Phase 2). (3) GA 100%: 99.9% uptime over first 7 days post-GA (TDD §19.1 Phase 3, §23.2 Phase 3 exit). (4) All 9 items in TDD §24.2 release checklist marked complete. (5) Security review sign-off from sec-reviewer covering bcrypt cost, RS256 keys, OWASP Auth Cheat Sheet items, refresh-token hashing, TLS 1.3, CORS allow-list. (6) SOC2 audit log spot-check: 100 random events have user_id + timestamp + IP + outcome populated. (7) Rollback drill: dry-run rollback in staging completes in < 5 min per TDD §19.3. |
| **Estimated Effort** | 7 EW (SRE 2, Backend 2, QA 1.5, Security 1, PM 0.5) |

**Milestone Effort Roll-Up:** M0=8 + M1=10 + M2=9 + M3=7 + M4=7 + M5=7 = **48 EW total**, consistent with the §1 capacity estimate.

---

## 3. Workstreams

Five parallel workstreams cross-cut the milestones. Owners are TDD §-aligned (`auth-team`, `frontend-team`, `platform-team`).

| Workstream | Owner | Lead Components | Milestones Touched |
|------------|-------|-----------------|--------------------|
| **WS-1: Backend Core** | auth-team | `AuthService`, `UserRepo`, `UserProfile` schema, password policy, lockout, audit log | M0, M1, M3, M5 |
| **WS-2: Token & Crypto** | auth-team | `TokenManager`, `JwtService`, RS256 keys, refresh hashing, revocation | M0, M2, M5 |
| **WS-3: Frontend** | frontend-team | `LoginPage`, `RegisterPage`, `AuthProvider`, `ProfilePage`, forgot/reset UI | M0 (contracts), M4, M5 |
| **WS-4: Security & Compliance** | auth-team + security reviewer | Threat model, OWASP review, SOC2 audit logging, GDPR consent capture, NIST SP 800-63B alignment, pen test | M0, M1, M2, M3, M5 |
| **WS-5: Observability & SRE** | platform-team | Prometheus metrics, Grafana dashboards, alerts, runbook, capacity plan, rollback drill | M0, M2, M5 |

### Sequencing Within Milestone Timeline

```
Week:        W1   W2  | W3   W4  | W5   W6  | W7   W8  | W9   W10  | W11
Milestone:   M0       | M1       | M2       | M3       | M4        | M5
WS-1 Back:   ██████████████████████        ████████              ████
WS-2 Token:  ████              ██████████████        ██                  ████
WS-3 FE:     ██  (contracts)                          ██████████████  ██
WS-4 Sec:    ████      ██      ██          ██                      ████
WS-5 SRE:    ██████                ██                              ██████
```

### Inter-Workstream Handoff Points

| # | Handoff | From → To | Milestone | Artifact |
|---|---------|-----------|-----------|----------|
| H1 | OpenAPI contract | WS-1 → WS-3 | M0 end | `/v1/auth/*` OpenAPI 3.1 spec |
| H2 | UserProfile schema | WS-1 → WS-4 | M0 end | DDL + GDPR data-minimization review |
| H3 | RSA keypair + rotation runbook | WS-2 → WS-5 | M0 end | Key material in secrets manager + Grafana key-age panel |
| H4 | Login + register endpoints | WS-1 → WS-3 | M1 end | Working `/auth/login` + `/auth/register` against staging |
| H5 | `AuthToken` envelope | WS-2 → WS-3 | M2 end | Real accessToken+refreshToken pairs for `AuthProvider` to consume |
| H6 | `TokenManager.revokeAllForUser` | WS-2 → WS-1 | M2 end | Internal API consumed by password reset flow |
| H7 | Reset email template + delivery SLA | WS-1 → WS-3 | M3 end | SendGrid template ID + reset URL contract for forgot-password UI |
| H8 | Frontend bundle | WS-3 → WS-5 | M4 end | Built artifact deployed to staging with feature-flag gating |
| H9 | Pen test report | WS-4 → WS-5 | Pre-M5 | Sign-off doc gating GA flag flip |
| H10 | Post-launch metrics package | WS-5 → WS-4 + Product | M5 + 30d | Success-metrics dashboard + GDPR/SOC2 audit-log sample |

---

## 4. Requirement Traceability

Every FR-AUTH-XXX and NFR-* from the source mapped to its owning milestone, workstream, and acceptance test reference (TDD §15.2 unit/integration/E2E rows; new acceptance tests labeled AT-NNN).

| Req ID | Requirement (short) | Milestone | Workstream | Acceptance Test |
|--------|---------------------|-----------|------------|-----------------|
| **FR-AUTH-001** | Login with email/password → `AuthToken` | M1 (backend) + M4 (frontend) | WS-1, WS-3 | TDD §15.2 unit "Login with valid credentials returns AuthToken"; AT-001 enumeration parity; AT-002 lockout state machine; E2E "User registers and logs in" |
| **FR-AUTH-002** | Registration with validation + duplicate rejection | M1 (backend) + M4 (frontend) | WS-1, WS-3 | TDD §15.2 integration "Registration persists UserProfile to database"; AT-003 concurrent-registration unique-constraint; AT-004 password-policy validator |
| **FR-AUTH-003** | JWT issuance + refresh (15-min / 7-day) | M2 | WS-2 | TDD §15.2 unit "Token refresh with valid refresh token"; TDD §15.2 integration "Expired refresh token rejected by TokenManager"; AT-005 refresh-rotation single-use; AT-006 Redis-down 503 fallback |
| **FR-AUTH-004** | Profile retrieval via GET `/auth/me` | M2 (backend) + M4 (frontend) | WS-1, WS-3 | AT-007 valid-token returns full `UserProfile` (7 fields); AT-008 expired/invalid token returns 401 |
| **FR-AUTH-005** | Password reset (request + confirm) | M3 (backend) + M4 (frontend) | WS-1, WS-3 | AT-009 enumeration parity on `/reset-request`; AT-010 single-use reset token; AT-011 1-hour TTL boundary; AT-012 reset invalidates all existing sessions |
| **NFR-AUTH.1 / NFR-PERF-001** | All auth endpoints < 200ms p95 | M1, M2, M5 | WS-1, WS-2, WS-5 | k6 load test (TDD §15.1) at 500 concurrent; Beta 10% latency dashboard |
| **NFR-PERF-002** | 500 concurrent login support | M2, M5 | WS-2, WS-5 | k6 sustained-concurrency suite at 500 RPS for 10 min; Beta 10% production p95 < 200ms |
| **NFR-AUTH.2 / NFR-REL-001** | 99.9% uptime rolling 30d | M5 (post-GA) | WS-5 | Uptime monitoring via `/health` endpoint over first 30 days post-GA |
| **NFR-AUTH.3** | Passwords one-way hashed, never plaintext-stored or logged | M1, M3 | WS-1, WS-4 | AT-013 grep CI log stream for known test password (zero hits); AT-014 DB inspection asserts only bcrypt hashes in `users.password_hash` |
| **NFR-SEC-001** | bcrypt cost factor 12 | M1 | WS-1, WS-4 | TDD §24.1 release-criteria assertion; unit test reads bcrypt cost parameter |
| **NFR-SEC-002** | RS256 with 2048-bit RSA keys | M2 | WS-2, WS-4 | Configuration validation test asserting algorithm + key length |
| **Compliance: GDPR consent** | Consent timestamp captured at registration | M1, M4 | WS-1, WS-3, WS-4 | AT-015 registration without consent flag → 400; consent timestamp persisted in audit log |
| **Compliance: SOC2 audit log** | All auth events logged 12-month retention with user_id, IP, ts, outcome | M0 (schema), M1, M2, M3, M5 | WS-1, WS-4, WS-5 | AT-016 100-event spot-check; retention policy validated by ops runbook |
| **Compliance: NIST SP 800-63B** | Password policy + hashing alignment | M0 (policy), M1 | WS-1, WS-4 | Policy review doc signed by security; password-policy validator unit tests |

---

## 5. Critical Path & Dependencies

### Sequenced Dependency Chain

```
M0 (Foundation)
 ├─ PostgreSQL UserProfile schema ──┐
 ├─ Redis 7 cluster ────────────────┤
 ├─ RSA 2048 keypair ───────────────┤
 ├─ SendGrid integration ───────────┤
 └─ OpenAPI contract ───────────────┤
                                    ▼
M1 (AuthService core) ── PasswordHasher ── UserRepo ── lockout ── audit log
                                    │
                                    ▼
M2 (TokenManager + JwtService) ── refresh hashing ── revocation API
                                    │
              ┌─────────────────────┼─────────────────────┐
              ▼                                           ▼
M3 (Password reset) consumes TokenManager.revokeAllForUser
              │                                           │
              ▼                                           ▼
              └────────► M4 (Frontend AuthProvider) ◄─────┘
                                    │
                                    ▼
                          M5 (Alpha → Beta → GA)
```

### Critical Path

`M0 schema + Redis + RSA + SendGrid` → `M1 AuthService.login + AuthService.register + PasswordHasher` → `M2 TokenManager + JwtService` → `M3 reset flow (depends on M2.revokeAllForUser)` → `M4 AuthProvider (depends on M2 endpoints AND M3 reset URLs)` → `M5 GA`.

The dual-tail dependency at M4 (needs both M2 token endpoints and M3 reset URLs) is the **highest-risk handoff**: any 1-day slip in M2 or M3 compresses M4's 2-week window. Mitigation: M3 and M4 backend/frontend leads coordinate in week 5 to lock reset-URL contract early.

### External Dependencies

| External | Required By | Risk if Late | Mitigation |
|----------|-------------|--------------|------------|
| **SendGrid account + templates** | M0 → M3 | M3 password-reset blocked; PRD success metric "Password reset completion > 80%" unmeasurable | Procure in M0 week 1; verify test send in M0 exit criteria; fallback identified: AWS SES |
| **PostgreSQL 15+** | M0 | Entire roadmap blocked at M0 | Coordinate with platform-team Week -2; pre-stage migration scripts locally |
| **Redis 7+** | M0 → M2 → M3 | M2 refresh tokens + M3 reset tokens both blocked | Provisioned in M0; capacity sized at 1 GB (TDD §25.3); HA mode required (no single-node Redis in production) |
| **SEC-POLICY-001 sign-off** | M0 | Password policy thresholds, RS256 key length, token TTLs undefined | Schedule security-policy review in M0 week 1; if blocked, escalate to security lead by 2026-04-03 |

### Internal Component Dependencies

The TDD-prescribed dependency order is **AuthService → PasswordHasher → TokenManager → JwtService** in terms of compositional containment, but the build order surfaces them differently:

| Order | Component | Why this order |
|-------|-----------|----------------|
| 1 | `PasswordHasher` | Smallest dependency surface; isolated unit testable |
| 2 | `UserRepo` + `UserProfile` | Needed before `AuthService.register` can persist |
| 3 | `AuthService` (login + register) | Composes 1 + 2; can stub tokens initially |
| 4 | `JwtService` | RSA-key dependent; independent of `AuthService` |
| 5 | `TokenManager` | Composes 4 + Redis; consumed by `AuthService` |
| 6 | `AuthService` re-wired with real tokens | Replaces M1 token stubs |
| 7 | `AuthProvider` (frontend) | Consumes everything above |

### Risk-Bearing Dependencies

| Dep | Risk Class | Notes |
|-----|-----------|-------|
| Redis → `TokenManager` refresh + revocation | **HIGH** | If Redis is unavailable, TDD §12 invariant says refresh requests must be REJECTED (not serve stale tokens). Single point of failure for session persistence. Mitigation: HA Redis (master + 2 replicas); rollback to legacy auth if Redis is degraded. |
| SendGrid → password reset email | **MEDIUM** | Single external vendor on critical reset path. Mitigation: monitor delivery; identify AWS SES as warm fallback. |
| RS256 key access from secrets manager → `JwtService` cold start | **MEDIUM** | If secrets manager unreachable at boot, `JwtService` cannot sign. Mitigation: pod-level key caching with 5-minute staleness window. |
| `TokenManager.revokeAllForUser` → M3 reset flow | **MEDIUM** | M3 depends on an M2-internal API. If M2 slips, M3 cannot achieve "new password invalidates all sessions" AC. Mitigation: stub `revokeAllForUser` first in M2 week 1 so M3 can wire against it before M2 fully completes. |

---

## 6. Risk Register & Mitigations

Carrying forward R-001, R-002, R-003 from TDD §20; adding R-004 through R-008 for risks introduced by phasing, frontend integration, and rollout.

| ID | Risk | Likelihood | Impact | Mitigation | Owning Milestone | Trigger for Contingency |
|----|------|-----------|--------|------------|------------------|-------------------------|
| **R-001** | Token theft via XSS allows session hijacking | Medium | High | `AuthProvider` keeps `accessToken` in memory only; refresh token in HttpOnly cookie; clears tokens on tab close; 15-min access-token expiry | M4 + M5 | XSS report from pen test (M5 pre-GA) OR `accessToken` found in `localStorage` scan → immediate fix; force `TokenManager.revokeAllForUser` for any flagged accounts |
| **R-002** | Brute-force attacks on `/auth/login` | High | Medium | API Gateway 10 req/min/IP; account lockout after 5 fails in 15 min; bcrypt cost 12 makes offline cracking expensive | M1 + M5 | `auth_login_total{outcome="failure"}` rate > 20%/5min over baseline triggers WAF block + CAPTCHA on `LoginPage` (R-002 contingency from TDD §20) |
| **R-003** | Data loss during migration from legacy auth | Low | High | `AuthService` runs parallel with legacy during Phase 1+2; `UserProfile` upserts are idempotent; full DB backup before each phase | M0, M5 | Any `UserProfile` row count or hash mismatch between legacy and new during Beta 10% → rollback to legacy (TDD §19.4) |
| **R-004** *(new)* | Open-question resolution slip blocks M1 | Medium | Medium | M0 resolves all 6 open questions OR schedules each with hard decision date; explicit decision-blocker register reviewed in M0 weekly check-in | M0 | Any unresolved question by 2026-04-10 (4 days pre-M1) escalates to engineering lead |
| **R-005** *(new)* | Redis unavailability cascades to login (not just refresh) | Low | High | TDD §12 invariant covers refresh; this risk adds: ensure **login does not write to Redis** in any synchronous critical path (audit log can be async-buffered) | M1, M2 | Login p95 latency increases when Redis is throttled → confirms inadvertent Redis dependency; fix architecture before GA |
| **R-006** *(new)* | Enumeration leakage via timing channel | Medium | Medium | AT-001 + AT-009 measure response-time variance ±15ms (login) / ±10ms (reset); CI fails build if exceeded | M1, M3 | Statistical timing test in CI rejects PR → fix before merge |
| **R-007** *(new)* | M3 + M4 simultaneous slip compresses M5 rollout to < 1 week | Medium | High | M3 and M4 share weekly sync from M2 week 2; reset-URL contract locked in M3 week 1 so frontend can stub | M3, M4 | If M3 not feature-complete by 2026-05-08 (4 days pre-M3 close) → de-scope reset-frontend UI to fast-follow post-GA |
| **R-008** *(new)* | RS256 key rotation breaks in-flight tokens | Low | Medium | Quarterly rotation runbook (TDD §13) supports key overlap window: old key kept verifying for 24h after new key starts signing | M2 | First quarterly rotation post-GA (target 2026-09) is dress-rehearsed in staging M5 week 1 |

---

## 7. Rollout & Release Gates

### Phase Gates (per TDD §19.1)

| Gate | Trigger | Owner | Pass Criteria | Fail Action |
|------|---------|-------|--------------|-------------|
| **Gate A: Alpha Entry** | 2026-05-27 | test-lead | M1-M4 all milestone exit criteria met; staging deploy clean; smoke tests green | Defer Alpha start by 1 week; reassess M5 GA date |
| **Gate B: Alpha → Beta 10%** | 2026-06-02 | test-lead + sec-reviewer | Zero P0/P1 bugs in 1-week soak; security review sign-off; pen test report received | Extend Alpha by 1 week; require WS-4 fix-and-retest |
| **Gate C: Beta 10% → GA 100%** | 2026-06-09 | eng-manager + test-lead | p95 < 200ms; error rate < 0.1%; zero `TokenManager` Redis failures over 2-week Beta; SOC2 audit-log spot-check 100/100 | Hold at 10%; investigate per TDD §19.3 rollback procedure |
| **Gate D: AUTH_TOKEN_REFRESH flag removal** | 2026-06-23 | platform-team | 14 days post-GA with refresh latency p95 < 100ms; zero refresh-related incidents | Keep flag for additional 14 days |

### Feature Flag Plan (per TDD §19.2)

| Flag | Default | Enabled In | Removed At | Controls |
|------|---------|-----------|-----------|----------|
| `AUTH_NEW_LOGIN` | OFF | Staging M0 (always ON in staging); 10% prod Beta (2026-06-03); 100% prod GA (2026-06-09) | 2026-06-09 (Phase 3 entry per TDD §19.1) | Routes `/v1/auth/login` + `/v1/auth/register` to new `AuthService` vs legacy |
| `AUTH_TOKEN_REFRESH` | OFF | Beta 10% entry (2026-06-03); persists through GA | 2026-06-23 (Phase 3 + 2 weeks per TDD §19.2) | Enables `TokenManager.refresh()` flow; when OFF, only access tokens are issued (no refresh) |

### Rollback Triggers (per TDD §19.4)

Any of the following triggers a rollback executed per TDD §19.3 procedure:

| # | Trigger | Threshold |
|---|---------|-----------|
| 1 | p95 latency on any `/v1/auth/*` endpoint | > 1000ms for > 5 minutes |
| 2 | Error rate on any `/v1/auth/*` endpoint | > 5% for > 2 minutes |
| 3 | `TokenManager` Redis connection failures | > 10/minute |
| 4 | `UserProfile` data loss or corruption | Any detected occurrence |
| 5 | Active security incident attributable to `AuthService` | Any P0 |

### Rollback Procedure (per TDD §19.3)

1. Disable `AUTH_NEW_LOGIN` → traffic returns to legacy auth path.
2. Verify legacy login operational via 5-request smoke test.
3. Investigate root cause via structured logs + OpenTelemetry traces.
4. If `UserProfile` corruption detected → restore from pre-phase backup.
5. Notify auth-team + platform-team via incident channel within 15 min.
6. Post-mortem within 48 hours (auth-team owns; sec-reviewer + eng-manager required reviewers).

### Release Criteria (mirroring TDD §24)

**Definition of Done (TDD §24.1):**

- [ ] All FR-AUTH-001..005 implemented and verified with passing tests
- [ ] Unit coverage for `AuthService`, `TokenManager`, `JwtService`, `PasswordHasher` ≥ 80% (M1+M2 exit set 85%)
- [ ] Integration tests for all 4 API endpoints pass against real PostgreSQL + Redis
- [ ] Security review complete: bcrypt cost verified, RS256 key rotation documented
- [ ] Performance: < 200ms p95 under 500 concurrent users confirmed via k6

**Release Checklist (TDD §24.2):** 9 items including staging smoke test, frontend functional, `AuthProvider` refresh verified, feature flags configured, runbooks published, dashboards live, rollback tested in staging, migration script validated, go/no-go sign-off.

---

## 8. Quality & Testing Gates

### Per-Milestone Coverage Targets

| Milestone | Unit | Integration | E2E | Performance | Security Reviews |
|-----------|------|-------------|-----|-------------|------------------|
| M0 | — | OpenAPI contract tests pass | — | — | Threat model draft; SEC-POLICY-001 alignment review |
| M1 | ≥ 85% lines on `AuthService.login/register`, `PasswordHasher` | Register → login round-trip vs testcontainer PG | — | Login single-pod 100 RPS p95 < 200ms | bcrypt cost-12 assertion; enumeration parity; password-never-logged grep |
| M2 | ≥ 85% lines on `TokenManager`, `JwtService` | Refresh + revocation + Redis-down vs testcontainer Redis | — | Login+refresh combined 500 concurrent p95 < 200ms | RS256 2048-bit assertion; refresh-hash invariant; clock-skew ±5s |
| M3 | ≥ 85% lines on reset flow | Reset email + token TTL + single-use vs testcontainer Redis + SendGrid sandbox | — | Reset-request rate-limit suite | Reset enumeration parity; session-invalidation invariant |
| M4 | ≥ 80% lines on `AuthProvider` | API contract tests via MSW | Playwright: register → logout → login → profile → forgot/reset | Lighthouse first-paint < 1s on `LoginPage` | localStorage scan = 0; tab-close clears token; WCAG 2.1 AA |
| M5 | (rolled up) ≥ 80% project-wide | All endpoint integration suites green | Full user journeys against staging then 10% production | k6 sustained 500 concurrent for 10 min; p95 < 200ms in Beta | Pen test report received; OWASP Auth Cheat Sheet checklist signed; SOC2 audit-log spot-check 100/100 |

### Security Review Checkpoints

| Checkpoint | When | Owner | Pass Evidence |
|------------|------|-------|--------------|
| SEC-1: Password hashing | M1 close | sec-reviewer | bcrypt cost=12 unit test + `users.password_hash` column inspection shows only `$2[aby]$12$...` patterns |
| SEC-2: Token signing | M2 close | sec-reviewer | RS256 algorithm config + 2048-bit RSA key + key rotation runbook published |
| SEC-3: Refresh-token storage | M2 close | sec-reviewer | Redis contents inspection: refresh tokens stored as SHA-256 hashes, never raw |
| SEC-4: Enumeration prevention | M1 + M3 | sec-reviewer | Timing-parity test passes (±15ms login, ±10ms reset) |
| SEC-5: OWASP Authentication Cheat Sheet review | Pre-M5 | sec-reviewer | All 18 cheat-sheet items checked; non-applicable items documented |
| SEC-6: Pen test | M5 Alpha | external pen tester | Report received; all High/Critical findings resolved before Gate B |
| SEC-7: TLS 1.3 + CORS allow-list | M5 Alpha | platform-team | API Gateway config inspection; `Access-Control-Allow-Origin` lists only known frontend hosts |

### Performance Gate

| Test | Tool | Target | Milestone |
|------|------|--------|-----------|
| Login p95 latency | k6 | < 200ms at 100 RPS single pod | M1 close |
| Refresh p95 latency | k6 | < 100ms (TDD §4.1) | M2 close |
| Sustained concurrency | k6 | 500 concurrent for 10 min, p95 < 200ms, 0 errors | M2 close, repeated M5 Beta |
| Bcrypt hash benchmark | Jest microbench | < 500ms per hash (TDD §4.1) | M1 close |
| Lighthouse first-paint | Lighthouse CI | < 1s on `LoginPage` | M4 close |

### Compliance Gate

| Standard | Evidence | Owner | Milestone |
|----------|----------|-------|-----------|
| **SOC2 Type II audit logging** | All auth events emit user_id + ts + IP + outcome; 12-month retention configured on `audit_log` table; 100-event spot-check passes | WS-4 | M0 schema, M1+M2+M3 emission, M5 spot-check |
| **GDPR consent at registration** | `RegisterPage` requires explicit consent checkbox; consent timestamp persisted in `audit_log` | WS-1 + WS-3 + WS-4 | M1 (backend), M4 (frontend) |
| **GDPR data minimization** | Only email, hashed password, displayName, roles stored — no extra PII fields in `UserProfile` | WS-4 | M0 schema review |
| **NIST SP 800-63B** | Password policy (≥8 chars, complexity), one-way hashing via bcrypt, no password expiration policy (per current 800-63B guidance), credential stuffing protection (lockout + rate limit) | WS-4 | M0 policy review + M1 implementation |

---

## 9. Open Questions & Decisions Needed

Six open questions: 4 from PRD §Open Questions, 2 from TDD §22 (OQ-001, OQ-002). Each must be resolved or scheduled — M0 owns final resolution gates.

| OQ # | Question | Source | Owner | Owning Milestone (Decision Blocks) | Decision Date | Status |
|------|----------|--------|-------|-------------------------------------|---------------|--------|
| **PRD-OQ-1** | Should password reset emails be sent synchronously or asynchronously? | PRD | Engineering | M3 (blocks `/reset-request` implementation choice) | 2026-04-22 (during M2) | **Open** — recommend async via job queue to keep `/reset-request` p95 < 200ms |
| **PRD-OQ-2** | Maximum number of refresh tokens per user across devices? | PRD | Product | M2 (blocks `TokenManager` capacity model) | 2026-04-15 (during M1) | **Open** — recommend cap of 10 active refresh tokens per user; oldest evicted on issuance |
| **PRD-OQ-3** | Account lockout policy after N failed attempts? | PRD | Security | M1 (blocks lockout implementation) | 2026-04-03 (M0) | **Open** — TDD §13 says "5 fails in 15 min"; need security sign-off |
| **PRD-OQ-4** | Should we support "remember me" to extend session duration? | PRD | Product | M2 (blocks refresh-token TTL configuration) | 2026-04-15 (during M1) | **Open** — recommend NO for v1.0; revisit v1.1; keep 7-day refresh TTL fixed |
| **TDD-OQ-001** | Should `AuthService` support API key authentication for service-to-service calls? | TDD | test-lead | M2 (blocks scope decision; could affect `JwtService` claim shape) | 2026-04-15 | Open (TDD: "Deferred to v1.1 scope discussion") — confirm deferral in writing during M0 |
| **TDD-OQ-002** | Maximum allowed `UserProfile.roles` array length? | TDD | auth-team | M0 (blocks `UserProfile` schema constraint) | 2026-04-01 | Open (TDD: "Pending RBAC design review") — for v1.0 set soft cap of 16 with DB-level check constraint; document for downstream RBAC PRD |

**Escalation protocol:** Any open question still Open within 4 calendar days of its Decision Date → escalated to engineering lead (Tech Lead `test-lead` per TDD §Document Information) in next standup. If any Decision Date slips into its owning milestone, that milestone's exit criteria are flagged at risk in the weekly status report.

---

## 10. Success Metrics & Measurement

### PRD Success Metrics (5)

| Metric | Target | Instrumentation Point | Post-Launch Review |
|--------|--------|----------------------|--------------------|
| Registration conversion rate | > 60% | Frontend analytics funnel: landing → `RegisterPage` view → POST `/auth/register` 201 | T+30d (2026-07-09) |
| Login response time (p95) | < 200ms | APM (OpenTelemetry) span on `AuthService.login()`; Prometheus `auth_login_duration_seconds` histogram | T+7d (2026-06-16) — gates GA exit criterion |
| Average session duration | > 30 minutes | `auth_token_refresh_total` event timestamps; compute median time between login and last refresh | T+30d (2026-07-09) |
| Failed login rate | < 5% of attempts | `auth_login_total{outcome="failure"}` / `auth_login_total` ratio over rolling 24h | T+14d (2026-06-23) |
| Password reset completion | > 80% | Funnel: POST `/auth/reset-request` → POST `/auth/reset-confirm` success per email within 1h window | T+30d (2026-07-09) |

### TDD Technical Metrics (5, per §4.1)

| Metric | Target | Instrumentation | Review Milestone |
|--------|--------|-----------------|------------------|
| Login response time (p95) | < 200ms | APM on `AuthService.login()` | M5 Beta exit + T+7d |
| Registration success rate | > 99% | `auth_registration_total{outcome="success"}` / `auth_registration_total` | T+14d |
| Token refresh latency (p95) | < 100ms | APM on `TokenManager.refresh()` | M5 Beta exit + T+7d |
| Service availability | 99.9% over 30d | Health-check uptime monitoring on `/health` | T+30d |
| Password hash time | < 500ms | Benchmark suite of `PasswordHasher.hash()` at cost=12 | M1 close (one-time gate) |

### TDD Business Metrics (2, per §4.2)

| Metric | Target | Instrumentation | Review Milestone |
|--------|--------|-----------------|------------------|
| User registration conversion | > 60% | `RegisterPage` funnel analytics | T+30d |
| Daily active authenticated users | > 1000 within 30 days of GA | Count of unique `userId` claims in `accessToken` issuances per day | T+30d (2026-07-09) |

### Measurement Cadence Summary

| Window | Review | Attendees | Output |
|--------|--------|-----------|--------|
| M5 Beta close (2026-06-09) | Pre-GA latency + error-rate gate | auth-team, platform-team, sec-reviewer | Go/no-go for 100% flag flip |
| T+7d (2026-06-16) | First-week stability review | auth-team, platform-team | Continue monitoring or hold `AUTH_TOKEN_REFRESH` flag removal |
| T+14d (2026-06-23) | `AUTH_TOKEN_REFRESH` removal gate | auth-team | Flag removed or extended |
| T+30d (2026-07-09) | Full success-metric review against PRD + TDD | Product, auth-team, eng-manager | Lessons-learned doc; input to v1.1 PRD (MFA, OAuth) |

---

## Appendix A — TDD Invariants & Edge Cases Carried Into Roadmap

The following invariants from TDD §12 (Error Handling & Edge Cases) and §13 (Security) are explicitly carried as acceptance tests in the milestones above:

| Invariant | Source | Carried In |
|-----------|--------|-----------|
| Account lockout: 5 failed attempts in 15 min → 423 + admin notify | TDD §13 + PRD §Error Handling | M1 AT-002 |
| Clock-skew tolerance: 5-second window in `JwtService` | TDD §12 | M2 clock-skew test |
| Redis unavailability: refresh rejected (NOT stale) | TDD §12 + R-005 | M2 AT-006 (Redis-down test) |
| Concurrent registration with same email: DB unique constraint | TDD §12 | M1 AT-003 |
| Refresh token revocation on password change | TDD §13 + FR-AUTH-005 AC | M3 AT-012 |
| Refresh tokens hashed in Redis (never raw) | TDD §13 | M2 refresh-hash test |
| Password never logged | NFR-AUTH.3 + TDD §13 | M1 AT-013 + M3 grep test |
| Generic 401 for both unknown email and wrong password | PRD §Error Handling + TDD §12 | M1 AT-001 enumeration parity |
| Reset request: same response regardless of registration | PRD §Error Handling + TDD §12 | M3 AT-009 enumeration parity |
| Reset token TTL: 1 hour, single-use | FR-AUTH-005 AC + TDD §13 | M3 AT-010 + AT-011 |
| Multi-device login: both sessions valid | PRD §Error Handling | M2 multi-device test |
| TLS 1.3 enforced on all endpoints | TDD §13 | M5 SEC-7 |
| CORS restricted to known frontend origins | TDD §13 | M5 SEC-7 |

---

## Appendix B — Component → Milestone Matrix

| Component | M0 | M1 | M2 | M3 | M4 | M5 |
|-----------|----|----|----|----|----|----|
| `AuthService` | scaffold | login + register | wire real tokens | reset flow | (consumer only) | GA |
| `PasswordHasher` | — | full impl | — | reused in reset | — | GA |
| `UserRepo` / `UserProfile` schema | DDL | CRUD | `lastLoginAt` update | — | — | GA |
| `TokenManager` | — | (stub) | full impl + revocation | `revokeAllForUser` consumed | (consumer only) | GA |
| `JwtService` | RSA keys | — | full impl | — | — | GA + first rotation drill |
| `LoginPage` | — | — | — | — | full impl | GA |
| `RegisterPage` | — | — | — | — | full impl | GA |
| `AuthProvider` | — | — | — | — | full impl + silent refresh | GA |
| `ProfilePage` | — | — | — | — | full impl | GA |
| Audit log | schema | login events | refresh + revocation events | reset events | — | SOC2 spot-check |
| Feature flags | scaffold | — | — | — | `AUTH_NEW_LOGIN` wired | flag flip + removal |
| Monitoring dashboards | (panel reservations) | login metrics | refresh metrics | reset metrics | frontend RUM | full Grafana dashboard live |

---

**END OF ROADMAP — User Authentication Service v1.0**
