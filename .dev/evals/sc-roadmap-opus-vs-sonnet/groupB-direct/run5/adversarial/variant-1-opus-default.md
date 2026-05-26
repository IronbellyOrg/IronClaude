# User Authentication Service — Implementation Roadmap

> **Source:** `AUTH-PRD-001` (Product Requirements) + `AUTH-001-TDD` (Technical Design), merged at `inputs/merged-prd-tdd-user-auth.md`.
> **Target release:** v1.0 — GA 2026-06-09.
> **Owning team:** auth-team (engineering), with product, security, frontend, and platform-team as cross-functional partners.
> **Roadmap horizon:** 11 calendar weeks (2026-03-30 through 2026-06-12), plus a 2-week post-GA stabilization tail.

---

## 1. Vision & Outcome Statement

### 1.1 Business outcome

Ship a self-hosted, NIST SP 800-63B-aligned User Authentication Service that becomes the foundational identity layer for the platform. Success unlocks the Q2-Q3 2026 personalization roadmap (a projected $2.4M ARR), retires the 25% of churn attributable to "no accounts," and clears the Q3 2026 SOC2 Type II audit gate by closing the audit-logging finding.

### 1.2 Technical outcome

A horizontally-scalable, stateless REST service (`AuthService`) that:

- Issues RS256-signed JWT access tokens (15-min TTL) and Redis-backed opaque refresh tokens (7-day TTL) via `TokenManager` / `JwtService`.
- Persists `UserProfile` records in PostgreSQL 15 with bcrypt-12 password hashes via `PasswordHasher`.
- Exposes four core endpoints (`/auth/login`, `/auth/register`, `/auth/me`, `/auth/refresh`) plus the password-reset pair (`/auth/reset-request`, `/auth/reset-confirm`).
- Integrates with `LoginPage`, `RegisterPage`, `ProfilePage`, and `AuthProvider` on the frontend.
- Meets NFR-PERF-001 (<200ms p95), NFR-PERF-002 (500 concurrent), and NFR-REL-001 (99.9% over 30 days).

### 1.3 What "done" looks like (single sentence)

A new user can register, log in, refresh silently for 7 days, reset a forgotten password, and view their profile — all in under 200ms p95, with every auth event captured in a 90-day audit log, and no plaintext credential ever touching storage or logs.

### 1.4 Headline metrics (tie to PRD §Success Metrics and TDD §4)

| Metric | Target | Source |
|---|---|---|
| Registration conversion | >60% | PRD success metrics |
| Login p95 latency | <200ms | NFR-PERF-001 / TDD §4.1 |
| Token-refresh p95 latency | <100ms | TDD §4.1 |
| Avg session duration | >30 min | PRD success metrics |
| Failed-login rate | <5% of attempts | PRD success metrics |
| Password-reset completion | >80% | PRD success metrics |
| Service availability | 99.9% / 30-day rolling | NFR-REL-001 |
| Unit-test coverage (`AuthService`, `TokenManager`, `JwtService`, `PasswordHasher`) | >80% | TDD §24.1 |
| DAU (30 days post-GA) | >1000 | TDD §4.2 |

---

## 2. Phasing Strategy

### 2.1 Decomposition rationale

The roadmap is decomposed into **five sequential milestones (M1-M5)** plus **four cross-cutting workstreams (CC1-CC4)** that run in parallel from week 1.

Sequencing was driven by three constraints from the source:

1. **TDD §23.1 anchors dates** — the TDD already proposes M1 (Core AuthService) → M2 (Token Mgmt) → M3 (Password Reset) → M4 (Frontend) → M5 (GA) on a fortnightly cadence. The roadmap honors that cadence and back-fills missing detail (entry/exit criteria, deliverables, dependencies).
2. **Dependency chain from architecture** — `PasswordHasher` and `UserProfile` schema are prerequisites for everything; `TokenManager` requires Redis + `JwtService`; password-reset requires email infra; the frontend cannot integrate until both token issuance and refresh exist.
3. **Rollout phasing from TDD §19** — Phase 1 (Internal Alpha) and Phase 2 (10% Beta) are folded into M5; both feature flags (`AUTH_NEW_LOGIN`, `AUTH_TOKEN_REFRESH`) gate exposure during M5.

### 2.2 Phase map

| Phase | Milestones | Theme | Calendar window |
|---|---|---|---|
| Foundations | M1 | Schema + core service + bcrypt + register/login endpoints | Week 1-2 (2026-03-30 → 2026-04-13) |
| Stateful sessions | M2 | JWT + refresh + `/auth/me` + audit-log skeleton | Week 3-4 (2026-04-14 → 2026-04-27) |
| Self-service recovery | M3 | Password reset, email integration, lockout | Week 5-6 (2026-04-28 → 2026-05-11) |
| User-facing integration | M4 | `LoginPage`, `RegisterPage`, `ProfilePage`, `AuthProvider`, silent refresh | Week 7-8 (2026-05-12 → 2026-05-25) |
| Hardening + GA | M5 | Internal alpha → 10% beta → 100% GA, runbooks, on-call enablement | Week 9-11 (2026-05-26 → 2026-06-09) |
| Stabilization | Post-GA | Flag removal, post-mortem readiness, capacity tuning | Week 12-13 (2026-06-10 → 2026-06-23) |

### 2.3 Critical path

`Schema (D-101)` → `PasswordHasher (D-103)` → `Register/Login (D-104, D-105)` → `JwtService (D-201)` → `TokenManager (D-202)` → `/auth/refresh + /auth/me (D-203, D-204)` → `AuthProvider silent refresh (D-403)` → `M5 rollout`.

Password reset (M3) and frontend (M4) parallelize partially: `LoginPage` / `RegisterPage` can begin against mocked backends during M2; only `AuthProvider` silent refresh blocks on M2 exit.

---

## 3. Milestones

### M1 — Core `AuthService`, schema, register + login

- **Window:** 2026-03-30 → 2026-04-13 (2 weeks)
- **Theme:** Establish the data plane and the two unauthenticated endpoints.
- **Maps to:** TDD §23.1 M1; PRD FR-AUTH.1, FR-AUTH.2; TDD FR-AUTH-001, FR-AUTH-002.

**Scope**

- `UserProfile` table in PostgreSQL 15 (id UUIDv4 PK, email UNIQUE+lowercase, displayName 2-100 chars, createdAt, updatedAt auto, lastLoginAt NULLABLE, roles default `["user"]`).
- `audit_log` table (id, user_id, event_type, ip, user_agent, outcome, occurred_at) with the 90-day retention policy from TDD §7.2.
- `PasswordHasher` wrapper around `bcryptjs` with cost factor 12 and pluggable interface for future argon2id migration (NG ref to TDD §6.4 rationale).
- `AuthService.register()` and `AuthService.login()` orchestration.
- `POST /auth/register` (201 / 400 / 409) and `POST /auth/login` (200 / 401) with the canonical error envelope from TDD §8.3.
- Email normalization (lowercase + trim) at write and read for the unique constraint to hold.
- Password policy validator: ≥8 chars, ≥1 uppercase, ≥1 number (TDD FR-AUTH-002 AC #3); reject before hashing.

**Deliverables**

| ID | Deliverable | Owner |
|---|---|---|
| D-101 | `migrations/0001_user_profile.sql` (idempotent, includes lowercase-email index) | auth-team |
| D-102 | `migrations/0002_audit_log.sql` with 90-day retention job spec | auth-team |
| D-103 | `PasswordHasher` module + unit tests covering cost-12 invariant and 500ms upper-bound timing test | auth-team |
| D-104 | `AuthService.register()` + `POST /auth/register` handler | auth-team |
| D-105 | `AuthService.login()` + `POST /auth/login` handler (returns placeholder token in M1; real JWT lands in M2) | auth-team |
| D-106 | OpenAPI 3.1 fragment for the two endpoints, committed to `/docs/api/auth.yaml` | auth-team |
| D-107 | Local Docker Compose stack (PostgreSQL 15 + Redis 7 placeholder) for developer onboarding | devops |

**Entry criteria**

- PostgreSQL 15+ instance provisioned in staging (PRD Dependencies).
- Node.js 20 LTS baseline image published.
- Repository scaffolded with linting, formatter, and CI hook for `pnpm test`.

**Exit criteria**

- All D-101 → D-107 merged to main.
- Unit-test coverage for `AuthService` + `PasswordHasher` ≥80%.
- `POST /auth/register` round-trips against staging PostgreSQL, persists `UserProfile`, idempotently rejects duplicate email with 409.
- `POST /auth/login` validates password via `PasswordHasher.verify()` and returns 401 generically (no user enumeration; identical timing within 50ms tolerance between unknown-user and wrong-password paths).
- `PasswordHasher` benchmark on the build agent confirms cost-12 hash time is in the 250-500ms band (TDD §17).
- OpenAPI fragment validated with `redocly lint`.

**Dependencies & sequencing**

- Blocks: M2 (token issuance can't reuse `AuthService.login()` without M1's contract).
- Blocked by: nothing — this is the start of the critical path.

**Duration estimate:** 10 working days. Risk buffer: +2 days for bcrypt-cost benchmarking surprises on the chosen runtime.

---

### M2 — Token management (`JwtService`, `TokenManager`, `/auth/refresh`, `/auth/me`)

- **Window:** 2026-04-14 → 2026-04-27 (2 weeks)
- **Theme:** Make sessions persistent and stateless.
- **Maps to:** PRD FR-AUTH.3, FR-AUTH.4; TDD FR-AUTH-003, FR-AUTH-004.

**Scope**

- `JwtService.sign()` / `verify()` using RS256 with 2048-bit RSA keypair (TDD NFR-SEC-002). Keypair loaded from a secret mount; rotation cadence is quarterly with overlap window (TDD §13).
- `JwtService` clock-skew tolerance: 5 seconds (TDD §12).
- `TokenManager.issueTokens()` → returns `AuthToken` (access 15min, refresh 7day, expiresIn=900, tokenType="Bearer").
- `TokenManager` stores **hashed** refresh tokens in Redis 7 with 7-day TTL (TDD §13 — "Refresh tokens are stored as hashed values").
- `TokenManager.refresh()` rotates refresh tokens (revoke old, issue new) — refresh-token reuse detection logs a security event.
- `POST /auth/refresh` and `GET /auth/me` endpoints. `/auth/me` includes id, email, displayName, createdAt, updatedAt, lastLoginAt, roles (TDD FR-AUTH-004 AC #3).
- `lastLoginAt` updated by `AuthService` on each successful login (TDD §7.1).
- Audit-log writes for `login_success`, `login_failure`, `token_refresh_success`, `token_refresh_failure`.

**Deliverables**

| ID | Deliverable | Owner |
|---|---|---|
| D-201 | `JwtService` (sign / verify / rotate-aware key resolver) + unit tests | auth-team |
| D-202 | `TokenManager` with hashed-refresh-token storage in Redis + rotation + reuse-detection unit tests | auth-team |
| D-203 | `POST /auth/refresh` handler | auth-team |
| D-204 | `GET /auth/me` handler with Bearer-token middleware | auth-team |
| D-205 | Key-rotation runbook stub (quarterly cadence, overlap window) | security |
| D-206 | Audit-log integration for the four events listed above | auth-team |
| D-207 | OpenAPI fragments for `/auth/refresh` and `/auth/me` | auth-team |
| D-208 | k6 baseline load script for the four endpoints (used in M5) | qa |

**Entry criteria**

- M1 exit criteria met.
- Redis 7 instance provisioned in staging with persistence enabled (TDD §6.3).
- RSA keypair generated and stored in secrets manager; CI has read access to a development keypair.

**Exit criteria**

- Login returns a real `AuthToken` pair; expired access tokens return 401 (TDD FR-AUTH-004 AC #2).
- `/auth/refresh` with valid token returns new pair and old refreshToken is revoked.
- Refresh-token reuse triggers a `token_reuse_detected` audit event AND revokes the entire token family for that user.
- Clock-skew tolerance test: tokens with `iat` within ±5s of server time accepted (TDD §12).
- Redis-unavailable test: `/auth/refresh` returns 503 with explicit error code rather than silently issuing tokens (TDD §12 fallback semantics).
- Coverage for `JwtService` and `TokenManager` ≥80%.

**Dependencies**

- Blocks: M3 (password-reset flow uses `TokenManager` to invalidate all sessions on reset — FR-AUTH.5 AC), M4 (`AuthProvider` silent refresh).
- Blocked by: M1.

**Duration estimate:** 10 working days. Risk buffer: +2 days if key-rotation overlap semantics need a second design pass.

---

### M3 — Password reset, email integration, lockout, enumeration-safe paths

- **Window:** 2026-04-28 → 2026-05-11 (2 weeks)
- **Theme:** Self-service recovery without leaking account existence.
- **Maps to:** PRD FR-AUTH.5; TDD FR-AUTH-005.

**Scope**

- `POST /auth/reset-request` — always returns 200 with a generic confirmation, regardless of whether the email is registered (PRD error-handling row "Reset requested for unregistered email"; TDD §13).
- `POST /auth/reset-confirm` — validates the single-use, 1-hour-TTL token; updates the password hash via `PasswordHasher`; invalidates **all** existing refresh-token families for the user via `TokenManager` (FR-AUTH.5 AC: "new password invalidates all sessions").
- `password_reset_tokens` table or Redis namespace (decision: Redis with 1-hour TTL — simpler revocation; document trade-off in ADR).
- Email integration with SendGrid (PRD Dependencies). Template includes the reset link, the 1-hour expiry, and an "if you didn't request this, ignore" line.
- Account-lockout policy: 5 failed logins in 15 minutes → `423 Locked` from `/auth/login` (PRD Error Handling table; TDD §13). Lockout state stored in Redis with sliding 15-minute window.
- Admin-notification hook on lockout (PRD error-handling row "Wrong password (≥5 attempts): Admin notified"). M3 emits a structured event; the actual notifier (Slack / pager) is a CC2 deliverable.
- Asynchronous email send via a queue (resolves PRD Open Question #1 — recommend async to keep request latency under NFR-PERF-001).

**Deliverables**

| ID | Deliverable | Owner |
|---|---|---|
| D-301 | `AuthService.requestPasswordReset()` + `AuthService.confirmPasswordReset()` | auth-team |
| D-302 | `POST /auth/reset-request` and `POST /auth/reset-confirm` handlers | auth-team |
| D-303 | SendGrid client wrapper with retry + bounce-handling hook | auth-team |
| D-304 | Reset-email template (HTML + plaintext fallback) | auth-team + design |
| D-305 | Lockout module (`LoginAttemptTracker`) using Redis sliding window | auth-team |
| D-306 | `password_reset_requested`, `password_reset_completed`, `account_locked`, `account_unlocked` audit events | auth-team |
| D-307 | Migration to ensure all refresh-token families are revocable by user_id | auth-team |
| D-308 | ADR: synchronous vs asynchronous reset email — recommend async | auth-team |

**Entry criteria**

- M2 exit criteria met.
- SendGrid API credentials provisioned for staging and production (separate keys).
- Email-from domain (`auth@<platform-domain>`) has SPF / DKIM / DMARC records published — verify before M3 starts (CC2 dependency).

**Exit criteria**

- `/auth/reset-request` returns 200 in <200ms p95 for both registered and unregistered emails; timing variance <30ms between paths (enumeration-safety bar).
- `/auth/reset-confirm` with valid token updates password and revokes every active refresh token for the user. Manual verification: log in on two devices, request reset, confirm; both devices receive 401 on next refresh.
- Reset tokens cannot be reused (second submission returns 410 Gone).
- Reset tokens expire at exactly 1 hour (test with frozen clock).
- Lockout: 5 wrong-password attempts in 15 min returns 423; correct credentials before threshold do NOT reset the counter (security choice — document in ADR); counter resets after the 15-min window passes.
- Email delivery success rate >99% measured against SendGrid status webhook.
- Reset-flow completion rate measurable via `password_reset_requested` → `password_reset_completed` funnel.

**Dependencies**

- Blocks: M5 (rollout cannot ship without the full FR set).
- Blocked by: M2.

**Duration estimate:** 10 working days. Risk buffer: +3 days if email deliverability requires DNS coordination outside auth-team.

---

### M4 — Frontend integration (`LoginPage`, `RegisterPage`, `ProfilePage`, `AuthProvider`)

- **Window:** 2026-05-12 → 2026-05-25 (2 weeks)
- **Theme:** Make the service usable by humans.
- **Maps to:** PRD UX requirements; TDD §10.

**Scope**

- `LoginPage` (route `/login`) — email + password, inline validation, generic-error display, "Forgot password?" link.
- `RegisterPage` (route `/register`) — email + password + displayName, client-side password-strength meter mirroring server policy, terms-of-service link, GDPR consent checkbox with recorded timestamp (PRD legal/compliance row "Consent at registration").
- `ProfilePage` (route `/profile`) — auth-required, calls `GET /auth/me`, shows displayName / email / createdAt.
- `AuthProvider` context — holds `AuthToken` in memory (NOT localStorage; TDD R-001 mitigation), exposes `login`, `logout`, `refresh`, `user` to children, intercepts 401 to trigger silent refresh, redirects to `/login` after refresh failure.
- `AuthProvider` token-expiry strategy: schedule silent refresh at `expiresIn - 60s` (i.e., 14 minutes after issuance) to avoid races.
- Password-reset UI: `/forgot-password` (request) and `/reset-password?token=…` (confirm) pages.
- Tab-close behavior: `AuthProvider` clears in-memory tokens on `beforeunload` (TDD R-001).
- Multi-tab coordination: BroadcastChannel API to keep tokens consistent when the user logs out in one tab.
- Logout flow: clears tokens, calls a token-revocation endpoint hint (or just discards client-side — if no revocation endpoint, document it in ADR and add to M5 risk list).

**Deliverables**

| ID | Deliverable | Owner |
|---|---|---|
| D-401 | `LoginPage` component + unit tests | frontend |
| D-402 | `RegisterPage` component + password-strength meter + GDPR consent | frontend |
| D-403 | `AuthProvider` with silent-refresh + 401 interceptor + tab-close handler + multi-tab sync | frontend |
| D-404 | `ProfilePage` with loading / error states | frontend |
| D-405 | `/forgot-password` and `/reset-password` pages | frontend |
| D-406 | E2E test suite covering register → login → silent refresh → profile → logout (Playwright; TDD §15.1 E2E tier) | qa |
| D-407 | Frontend ADR: refresh-token storage (memory + HttpOnly cookie hybrid per TDD R-001) | frontend |
| D-408 | Accessibility audit: WCAG 2.1 AA for `LoginPage`, `RegisterPage`, `ProfilePage` (forward-looking even though TDD §16 marks N/A backend-side) | design + frontend |

**Entry criteria**

- M2 exit criteria met (silent refresh requires real `/auth/refresh`).
- M3 exit criteria met (reset pages need both endpoints).
- Frontend routing framework available (PRD Dependencies).

**Exit criteria**

- Full Playwright E2E run green: new user can register, log in, navigate, get silently refreshed at 14 min mark, log out, log back in.
- Multi-tab logout works: logging out in tab A clears auth in tab B within 1 second.
- Tab-close drops the in-memory access token (verified by inspecting JS heap snapshot).
- Lighthouse score ≥90 for `LoginPage` and `RegisterPage`.
- Password-strength meter on `RegisterPage` rejects passwords the server would reject (no double-roundtrip for trivially-weak inputs).
- 401 interceptor only triggers ONE refresh attempt per access-token lifecycle (no refresh storms).

**Dependencies**

- Blocks: M5.
- Blocked by: M2, M3.

**Duration estimate:** 10 working days. Risk buffer: +2 days for silent-refresh race-condition debugging.

---

### M5 — Rollout: Internal Alpha → 10% Beta → 100% GA

- **Window:** 2026-05-26 → 2026-06-09 (2 weeks)
- **Theme:** Ship safely.
- **Maps to:** TDD §19 (Migration & Rollout Plan); TDD §24 (Release Criteria); TDD §25 (Operational Readiness).

**Scope**

- **Sub-phase 5A — Internal Alpha (Week 9, 2026-05-26 → 2026-06-01)**:
  - Deploy to staging behind `AUTH_NEW_LOGIN=ON` for auth-team + QA only.
  - Run the full TDD §15 test pyramid against staging.
  - Manual verification of all FR-AUTH.1 → FR-AUTH.5.
  - Exit gate: zero P0/P1 bugs (TDD §19.1 Phase 1 criterion).
- **Sub-phase 5B — 10% Beta (Week 10, 2026-06-02 → 2026-06-08)**:
  - Enable `AUTH_NEW_LOGIN` for 10% of production traffic via the feature-flag service.
  - `AUTH_TOKEN_REFRESH=ON` for the beta cohort.
  - 24/7 on-call rotation from auth-team begins (TDD §25.2).
  - Exit gate: p95 latency <200ms, error rate <0.1%, zero `TokenManager` Redis connection failures over a 48-hour observation window.
- **Sub-phase 5C — 100% GA (Day 11 → 2026-06-09)**:
  - Remove the cohort filter from `AUTH_NEW_LOGIN`; flag remains ON globally.
  - Deprecate any legacy auth endpoints (issue a sunset header for two weeks before removal).
  - Exit gate: 99.9% uptime over the first 7 days post-GA (TDD §19.1 Phase 3).

**Deliverables**

| ID | Deliverable | Owner |
|---|---|---|
| D-501 | Production-ready Helm/Kubernetes manifests with 3-pod baseline + HPA to 10 (TDD §25.3) | devops |
| D-502 | Feature-flag wiring (`AUTH_NEW_LOGIN`, `AUTH_TOKEN_REFRESH`) in the production flag service | devops |
| D-503 | Runbook entries for `AuthService` down + token-refresh failures (TDD §25.1) | auth-team |
| D-504 | Grafana dashboard: `auth_login_total`, `auth_login_duration_seconds`, `auth_token_refresh_total`, `auth_registration_total` (TDD §14) | observability |
| D-505 | Prometheus alert rules: login failure rate >20% / 5min; p95 >500ms; Redis connection-failure alarm (TDD §14) | observability |
| D-506 | k6 load-test run at 500 concurrent users; report attached to release ticket | qa |
| D-507 | Security review sign-off (PasswordHasher cost-12 verified; JwtService key rotation documented) (TDD §24.1) | security |
| D-508 | Rollback dry-run in staging proving the procedure in TDD §19.3 works end-to-end | devops + auth-team |
| D-509 | On-call training session + game-day with simulated outage | auth-team |
| D-510 | Go/no-go sign-off captured from test-lead and eng-manager (TDD §24.2) | leadership |

**Entry criteria**

- M1, M2, M3, M4 all complete.
- Security review (CC1) checkpoint passed.
- Observability stack (CC3) green in staging.
- Runbooks (D-503) reviewed by on-call team.

**Exit criteria**

- 99.9% uptime over 7 consecutive days post-GA.
- Both feature flags `AUTH_NEW_LOGIN` and `AUTH_TOKEN_REFRESH` flipped ON and pending removal (removal targets recorded — see §10 Out of Scope).
- Zero P0 incidents in the first 72 hours of GA.
- Headline metrics from §1.4 reported on the dashboard for at least 7 days.

**Duration estimate:** 10 working days, with the alpha → beta → GA ramp baked in.

---

## 4. Cross-Cutting Workstreams

These tracks run **in parallel** with M1-M5 starting Week 1.

### CC1 — Security & Compliance

- **Lead:** sec-reviewer
- **Cadence:** Weekly checkpoint review; gate at the end of M2, M4, and M5.
- **Workstream items:**
  - SEC-1: NIST SP 800-63B compliance review of password policy and storage (PRD legal/compliance).
  - SEC-2: GDPR data-minimization audit — confirm only `email`, `hashed password`, `displayName` collected, plus `consent_at` timestamp (PRD legal/compliance).
  - SEC-3: SOC2 Type II audit-log evidence — verify the 12-month retention (PRD) reconciles with the TDD's 90-day retention; **gap resolution: bump audit log retention to 12 months in D-102 to satisfy the SOC2 row**.
  - SEC-4: Threat-modeling pass before M5 (STRIDE on `AuthService`, `TokenManager`, `JwtService`).
  - SEC-5: Penetration test before GA — explicitly listed in PRD Risk Analysis as a mitigation for "Security breach from implementation flaws."
  - SEC-6: Quarterly RSA key rotation runbook owned jointly with devops.
  - SEC-7: CORS policy lockdown to known frontend origins (TDD §13).
  - SEC-8: TLS 1.3 enforcement at the API gateway (TDD §13).

### CC2 — Observability & Operational Readiness

- **Lead:** auth-team + platform-team
- **Workstream items:**
  - OBS-1: Structured logging — JSON logs with `correlation_id`, `user_id` (nullable for pre-auth), `event_type`, `outcome`. Sensitive fields (`password`, `accessToken`, `refreshToken`) stripped via a logger middleware.
  - OBS-2: OpenTelemetry spans across `AuthService` → `PasswordHasher` → `TokenManager` → `JwtService` (TDD §14).
  - OBS-3: Prometheus metrics emission from M2 onward, dashboards from start of M3.
  - OBS-4: Alert rules tested with synthetic failure injection at end of M4.
  - OBS-5: Admin-notification channel (Slack #auth-incidents) wired up before M5 sub-phase 5A; consumes the `account_locked` event from D-306.
  - OBS-6: Capacity planning per TDD §25.3 — confirm Redis 1 GB suffices for ~100K refresh tokens; build dashboard alarm at 70% utilization.
  - OBS-7: DNS / SPF / DKIM / DMARC for email-from domain (blocks M3 entry).

### CC3 — Testing & Quality

- **Lead:** qa
- **Workstream items:**
  - QA-1: Unit-test scaffolding from M1; coverage gate (≥80%) enforced in CI by end of M2.
  - QA-2: Integration tests with `testcontainers` for PostgreSQL + Redis from M1.
  - QA-3: Contract tests against the OpenAPI spec (D-106, D-207) by end of M2.
  - QA-4: Playwright E2E suite by end of M4 (D-406).
  - QA-5: k6 load-test framework by end of M2 (D-208); 500-concurrent run before M5 sub-phase 5B (D-506).
  - QA-6: Enumeration-timing test — assert <50ms variance between unknown-user / wrong-password 401 responses, and <30ms variance between reset-request for registered / unregistered email.
  - QA-7: Chaos test — Redis down test, PostgreSQL failover test, SendGrid down test.
  - QA-8: Test data: staging seeded with at least 50 test accounts with varied profiles (TDD §15.3).

### CC4 — Documentation & Enablement

- **Lead:** scribe + auth-team
- **Workstream items:**
  - DOC-1: OpenAPI 3.1 spec maintained throughout M1-M3.
  - DOC-2: Tech Reference document (downstream of TDD) populated as endpoints land.
  - DOC-3: Frontend integration guide for `AuthProvider` consumers (other teams).
  - DOC-4: On-call runbook (D-503).
  - DOC-5: API consumer documentation for "Sam the API Consumer" persona — emphasis on refresh-token flow and error codes.
  - DOC-6: Internal blog post + recorded demo before GA.
  - DOC-7: PRD Open Questions resolved and recorded:
    - OQ-1 (sync vs async reset email) → async (recorded in D-308 ADR).
    - OQ-2 (max refresh tokens per user) → no hard cap in v1.0; add metric and revisit in v1.1.
    - OQ-3 (lockout policy) → 5 attempts / 15 min sliding window (TDD §13).
    - OQ-4 ("remember me") → out of scope for v1.0; refresh token already provides 7-day persistence.

---

## 5. Risk Register

Risks are scored as **Probability (Low/Med/High) × Impact (Low/Med/High/Critical)**. Each risk has a mitigation, an owner role, and a monitoring mechanism so it is observable rather than relying on memory.

| ID | Risk | Prob × Impact | Mitigation | Owner | Monitoring |
|---|---|---|---|---|---|
| R-101 | Token theft via XSS allows session hijacking (TDD R-001) | Med × High | Access token in memory only; refresh token in HttpOnly+SameSite=Strict cookie; CSP locked down; `AuthProvider` clears tokens on tab close | security + frontend | Synthetic XSS test in CI; CSP-violation report endpoint |
| R-102 | Brute-force login attacks (TDD R-002) | High × Med | Rate limiting 10/min/IP at gateway; lockout 5 fails / 15 min in `AuthService`; bcrypt cost 12 | security | `auth_login_total{outcome="failure"}` rate alert |
| R-103 | Data loss during cutover (TDD R-003) | Low × High | Idempotent upserts; full DB backup before each rollout sub-phase; parallel run during 5B | auth-team + devops | Backup-verify cron + restore drill in CC1 |
| R-104 | bcrypt cost-12 exceeds 200ms p95 latency budget on target hardware | Med × Med | Bench on actual production CPU class in M1; if >500ms, drop to cost 11 with documented rationale | auth-team | M1 D-103 bench report; APM histogram |
| R-105 | Redis becomes a single point of failure for refresh tokens (TDD §12 fallback "reject refresh requests") | Med × High | Redis cluster mode in production; multi-AZ; read replicas; explicit 503 on outage; client-side prompts re-login | platform-team | Redis-health alert (D-505); refresh-error spike alert |
| R-106 | SendGrid outage blocks password reset (PRD risk) | Low × Med | Async queue with retry + backoff; on prolonged outage, fall back to manual support workflow per PRD risk row | auth-team | SendGrid webhook delivery-rate dashboard |
| R-107 | RSA private key compromise | Low × Critical | Keys in secret manager with audit log; quarterly rotation; emergency rotation runbook; refresh-token revocation flushes all sessions | security | Secret-access audit; alerting on out-of-cycle access |
| R-108 | SOC2 audit fails due to insufficient log retention | Med × High | Bump audit-log retention to 12 months (SEC-3); evidence pack assembled before GA | security + compliance | Quarterly evidence review |
| R-109 | Clock skew between API nodes invalidates valid tokens | Low × Med | NTP enforcement on all nodes; `JwtService` 5s tolerance window (TDD §12) | platform-team | NTP-drift alert |
| R-110 | Email enumeration via timing side-channel on `/auth/reset-request` | Med × Med | Constant-time response: always do the same DB lookup + (no-op for unregistered) queue-publish; QA-6 enforces <30ms variance | security + auth-team | QA-6 in CI |
| R-111 | Refresh-token replay after rotation | Low × High | Rotation invalidates old token; reuse-detection revokes entire family (TDD §12 implicitly + best practice) | auth-team | `token_reuse_detected` audit event alert |
| R-112 | Account lockout used as a denial-of-service vector | Med × Med | Lockout is per-account+IP rather than per-account global; admin unlock path; CAPTCHA after 3 failures (PRD R-002 contingency) | security | `account_locked` event-rate alert |
| R-113 | GDPR consent not captured before account creation | Low × High | `RegisterPage` blocks submit until consent box ticked; `consent_at` written in same transaction as `UserProfile` | frontend + auth-team | DB invariant test in CI |
| R-114 | Frontend silent-refresh storm caused by faulty 401 interceptor | Med × Med | Refresh-once-per-access-token-lifecycle guard; mutex around refresh call | frontend | `auth_token_refresh_total` rate ceiling alert |
| R-115 | Long-running migration locks `user_profile` table during M1 cutover | Low × Med | Migrations gated through `pg-online-schema-change`-style tooling; or run in maintenance window | devops | Migration-duration metric |
| R-116 | New `AuthService` deployed without coordinated frontend rollout, causing tokens the client can't refresh | Low × High | Coordinated release with frontend; feature flag `AUTH_NEW_LOGIN` only flips after both backend + frontend bundles deployed | release manager | Deployment-checklist gate |

---

## 6. Dependencies & Sequencing

### 6.1 External dependencies

| Dependency | Needed by | Risk if missing | Mitigation |
|---|---|---|---|
| PostgreSQL 15+ provisioned | M1 entry | Cannot start | DBaaS provisioned in week -1 |
| Redis 7+ provisioned (cluster mode in prod) | M2 entry | Cannot issue refresh tokens | Provision in week 2 |
| SendGrid account + API key | M3 entry | Cannot send reset emails | Procurement complete before week 4; verify SPF/DKIM/DMARC |
| Feature-flag service (existing) | M5 entry | Cannot stage rollout | Verify availability in week 8 |
| Secret manager for RSA keypair | M2 entry | Cannot sign tokens | Generate keypair in week 2 |
| Frontend routing framework | M4 entry | Cannot mount auth pages | Already present per PRD Dependencies |
| API gateway with rate limiting | M5 entry | Cannot enforce 10/min limits | Existing gateway; just add policy |
| Email-from domain DNS access | M3 entry | Email deliverability tanks | Coordinate with IT in week 3 |

### 6.2 Internal sequencing

```
Week:    1   2   3   4   5   6   7   8   9   10  11
M1:      [=======]
M2:              [=======]
M3:                      [=======]
M4:                              [=======]
M5:                                      [===========]
CC1:     [=========================================]
CC2:     [=========================================]
CC3:     [=========================================]
CC4:     [=========================================]
```

### 6.3 Parallelization opportunities

- **Schema vs hasher (M1):** `migrations/0001_user_profile.sql` and `PasswordHasher` can be built in parallel; they meet at `AuthService.register()`.
- **JWT vs TokenManager (M2):** `JwtService` (sign/verify) is testable in isolation before `TokenManager` exists.
- **Frontend mocking (M4):** `LoginPage` and `RegisterPage` can be built against a mocked backend during M2 if the OpenAPI spec is stable; only `AuthProvider` silent refresh truly blocks on M2.
- **Email template + SendGrid wiring (M3):** Template design (D-304) can start in M2 once strings are agreed.
- **Runbook drafting (CC4 / M5):** D-503 can start during M3 with placeholders that fill in as M4 lands.

### 6.4 Blocking-dependency summary

- M2 ⟶ blocked by M1.
- M3 ⟶ blocked by M2 (needs `TokenManager` to invalidate sessions on reset).
- M4 ⟶ blocked by M2 (needs `/auth/refresh` for silent refresh) and M3 (needs reset endpoints for `/forgot-password` and `/reset-password` pages).
- M5 ⟶ blocked by M1, M2, M3, M4, CC1 security checkpoint, CC2 dashboards green.

---

## 7. Success Metrics & Acceptance Criteria

### 7.1 Metric scoring rubric

A metric is "green" when measured on at least the time window listed. Anything else is yellow (investigate) or red (blocks GA decision).

### 7.2 Detailed metric table

| Metric | Target | Window | Source telemetry | Owner | Gate? |
|---|---|---|---|---|---|
| Registration conversion | >60% | 30 days post-GA | Funnel: `/register` view → `registration_success` | product | Soft gate |
| Login p95 latency | <200ms | Rolling 7 days | `auth_login_duration_seconds` histogram | auth-team | **Hard** — blocks GA |
| Token refresh p95 latency | <100ms | Rolling 7 days | `auth_token_refresh_duration_seconds` | auth-team | **Hard** — blocks GA |
| Avg session duration | >30 min | 30 days post-GA | refresh-event analytics | product | Soft |
| Failed login rate | <5% | Rolling 7 days | `auth_login_total{outcome="failure"}` ratio | security + product | Yellow if >5, red if >10 |
| Password reset completion | >80% | 30 days post-GA | `password_reset_requested` → `password_reset_completed` | product | Soft |
| Service availability | 99.9% | 30-day rolling | uptime monitor | platform-team | **Hard** |
| Password hash time | <500ms | Per-build | `PasswordHasher` micro-bench | auth-team | **Hard** — gate in M1 |
| Email delivery rate | >99% | Rolling 7 days | SendGrid webhook | auth-team | **Hard** during M3 |
| DAU authenticated users | >1000 | 30 days post-GA | `AuthToken` issuance count | product | Soft |

### 7.3 Per-FR acceptance criteria summary

| FR | Acceptance criteria summary | Test class |
|---|---|---|
| FR-AUTH.1 / FR-AUTH-001 | Valid creds → 200 + `AuthToken`; invalid → 401 generic; non-existent email → 401 (no enumeration); 5 fails / 15 min → 423 | Unit + integration + QA-6 |
| FR-AUTH.2 / FR-AUTH-002 | Valid → 201 + `UserProfile`; duplicate email → 409; weak password → 400 with field-level codes; bcrypt cost 12 | Unit + integration |
| FR-AUTH.3 / FR-AUTH-003 | Login returns 15-min access + 7-day refresh; `/auth/refresh` rotates; expired or revoked refresh → 401 | Unit + integration + clock-skew test |
| FR-AUTH.4 / FR-AUTH-004 | `/auth/me` returns full `UserProfile`; expired/invalid token → 401 | Unit + integration |
| FR-AUTH.5 / FR-AUTH-005 | Reset email within 60s; 1-hour TTL; single-use; password change invalidates **all** sessions | Integration + E2E + QA-7 chaos |

### 7.4 Definition of Done (rolled up from TDD §24.1)

- All five FRs implemented with passing tests.
- Coverage ≥80% for `AuthService`, `TokenManager`, `JwtService`, `PasswordHasher`.
- Integration tests for all 4 (+ 2 reset) endpoints green.
- Security review signed off.
- Performance testing confirms 200ms p95 at 500 concurrent users.
- Runbook published, on-call trained.

---

## 8. Boundary Conditions & Edge Cases

Roadmap-level handling beyond the FR-level table.

| Condition | Handling | Test |
|---|---|---|
| Empty email / password fields | 400 with `code: VALIDATION_REQUIRED_FIELD` | Unit on `AuthService` |
| Email > 254 chars (RFC 5321) | 400 with `code: VALIDATION_EMAIL_TOO_LONG` | Unit |
| displayName outside 2-100 chars | 400 with `code: VALIDATION_DISPLAYNAME_LENGTH` | Unit |
| Unicode in displayName (emoji, RTL) | Accepted; normalized via NFC | Unit |
| Concurrent registration with same email | Second request gets 409 via DB unique constraint; race window <50ms | Integration |
| User logs in from 6th device while 5 sessions active | All sessions valid (multi-device explicitly OK per PRD); add metric to revisit cap in v1.1 | Integration |
| Refresh token used after rotation | Reuse detection → revoke family, 401 | Unit on `TokenManager` |
| Reset token used twice | First use updates password; second use → 410 Gone | Integration |
| Reset confirm with password identical to current | Allowed (no enumeration); user warned in UI | Unit |
| Lockout reaches 5 then user requests reset | Reset succeeds (different code path); admin notified of unlock-via-reset | Integration |
| User changes password while logged in on Device B | Device B's next API call → 401 → forced re-login | Integration + E2E |
| Server clock drifts +10s | Tokens still accepted within ±5s tolerance; -5s → -10s drift causes premature expiry; alert on NTP drift | Chaos test |
| Redis cold start | `TokenManager` retries 3 times with exponential backoff; falls through to 503 | Chaos test |
| PostgreSQL primary failover | Connection-pool retry; <500ms blip; if >5s, gateway returns 503 | Chaos test |
| Single-element `roles` array (the default `["user"]`) | Treated normally; no special casing needed | Unit |
| Zero refresh tokens for user (never logged in) | `/auth/refresh` returns 401 with `code: AUTH_NO_REFRESH_TOKEN` | Unit |
| Maximum-size payload at `/auth/register` | Body-size limit 10 KB at gateway; 413 Payload Too Large | Integration |
| Slow client (delayed body) | 10-second request-body timeout at gateway | Integration |

---

## 9. State Management, Guard Conditions, Concurrency

The TDD marks §9 "Not applicable — backend service," but several real state machines exist and the roadmap calls them out so M2/M3 implementations stay honest.

### 9.1 Refresh-token state machine

States: `issued` → `rotated` (replaced) | `revoked` (manual) | `expired` (TTL hit) | `reused` (security event).

Guards:

- `rotated` is reachable only from `issued`.
- `reused` is reachable from `rotated` or `revoked` (used after replacement).
- `reused` transition revokes the entire token **family** (all descendants of the original issuance).

Concurrency:

- Two simultaneous `/auth/refresh` calls with the same token: serialize via Redis `SET NX` lock keyed on the token hash. Loser of the race gets 401.

### 9.2 Account-lockout state machine

States: `unlocked` ⟶ `locked` (5 failures in window) ⟶ `unlocked` (after window expires or admin/reset action).

Guard: Successful login during the window does NOT reset the failure counter (security choice per M3 §3 exit criteria).

### 9.3 Password-reset token state machine

States: `pending` ⟶ `consumed` (single use) | `expired` (1-hour TTL).

Guard: Issuing a new reset request while a `pending` token exists invalidates the prior token (prevents two valid links in two emails).

### 9.4 Audit-log write ordering

Concurrency-safe: each event written as an independent INSERT with `occurred_at = clock_timestamp()`. No cross-row coordination required. Partitioned by month for the 12-month retention.

### 9.5 Database transactions

- `AuthService.register()`: single transaction inserting `UserProfile` + `audit_log(registration)` + `consent` row. Rolls back atomically on failure.
- `AuthService.confirmPasswordReset()`: single transaction updating `password_hash` + revoking all refresh-token families + writing `audit_log(password_reset_completed)`.

---

## 10. Out of Scope

Items explicitly excluded from this roadmap and the rationale.

| Item | Rationale | Where it goes |
|---|---|---|
| OAuth / OIDC / social login | PRD non-goal; TDD NG-001; deferred to v1.1 | v1.1 roadmap |
| MFA (TOTP, SMS, WebAuthn) | PRD non-goal; TDD NG-002; v1.2 | v1.2 roadmap |
| RBAC enforcement | PRD non-goal; TDD NG-003; `roles` field present but not enforced | Separate authorization PRD |
| API-key authentication for service-to-service | TDD OQ-001 — deferred to v1.1 | v1.1 scope discussion |
| "Remember me" extended sessions | Refresh token already gives 7-day persistence; resolves PRD OQ #4 | Not needed |
| Admin UI for account management (Jordan persona) | Beyond v1.0 — audit-log query API ships; UI is separate | Admin-tools roadmap |
| Self-service email change | Not in PRD; introduce in v1.1 with verification flow | v1.1 |
| Self-service displayName change | Not in PRD; small addition; punt to v1.1 | v1.1 |
| Account deletion / GDPR right-to-erasure UI | Not in PRD MVP, but a real GDPR obligation — flag in §11 open question | v1.1 (hard deadline driven by GDPR) |
| Hardware-bound or device-trust signals | Out of scope; v2.0+ | v2.0+ |
| Federated SSO (SAML) | Out of scope; v2.0+ | v2.0+ |
| Bot detection / advanced fraud | Use gateway rate limiting + lockout in v1.0; richer detection later | v1.1+ |

---

## 11. Open Questions & Assumptions

### 11.1 PRD/TDD open questions and recommended resolutions

| ID | Question | Source | Recommended resolution | Decision owner |
|---|---|---|---|---|
| OQ-1 | Reset emails sync or async? | PRD OQ #1 | Async via queue (D-308 ADR) — keeps `/auth/reset-request` under NFR-PERF-001 | engineering |
| OQ-2 | Max refresh tokens per user? | PRD OQ #2 | No cap in v1.0; emit `refresh_tokens_per_user` metric and revisit in v1.1 if abuse detected | product |
| OQ-3 | Lockout policy after N failures? | PRD OQ #3 | 5 fails / 15-min sliding window, per-account+IP (TDD §13) | security |
| OQ-4 | Support "remember me"? | PRD OQ #4 | No — 7-day refresh window covers the use case | product |
| OQ-5 | API-key auth for service-to-service? | TDD OQ-001 | Deferred to v1.1 | test-lead |
| OQ-6 | Max `UserProfile.roles` array length? | TDD OQ-002 | Cap at 16 for v1.0 (defensive); revisit with RBAC design | auth-team |

### 11.2 Roadmap-level open questions (newly raised)

| ID | Question | Why it matters | Decision owner | Target |
|---|---|---|---|---|
| OQ-R1 | Audit-log retention: TDD §7.2 says 90 days, PRD legal/compliance row says 12 months. Which wins? | SOC2 evidence horizon | security + compliance | Before M1 D-102 commit |
| OQ-R2 | Refresh-token storage in browser: HttpOnly cookie vs in-memory + sessionStorage hybrid? | XSS surface area (R-101) | security + frontend | Before M4 D-403 |
| OQ-R3 | Where does GDPR right-to-erasure flow live for v1.0? | Hard legal obligation | legal + product | Before GA |
| OQ-R4 | Do we ship a token-revocation endpoint (`POST /auth/logout`) or is client-side discard enough? | M4 logout flow + R-101 | auth-team | Before M4 D-403 |
| OQ-R5 | Do we expose `/auth/me` PATCH for displayName updates in v1.0? | PRD says profile view only; some users will ask | product | Before M2 D-204 |
| OQ-R6 | What is the legacy auth-endpoint deprecation timeline post-GA? | TDD §19.1 Phase 3 mentions deprecation but no date | platform-team | Before M5 sub-phase 5C |

### 11.3 Assumptions

- **A-1:** SendGrid (or an interchangeable transactional-email provider) is available before M3 starts; if not, M3 slips one sprint.
- **A-2:** PostgreSQL 15+ and Redis 7+ are managed services; no DBA work falls on auth-team.
- **A-3:** API gateway with rate-limiting capability already exists; auth-team configures policies, doesn't build the gateway.
- **A-4:** Frontend routing framework supports protected routes and context providers (React Router or equivalent).
- **A-5:** Secrets manager (Vault / AWS Secrets Manager / equivalent) is in place for RSA keypair distribution.
- **A-6:** Observability stack (Prometheus + Grafana + tracing) is in place; auth-team plugs in metrics, doesn't stand up the stack.
- **A-7:** CI pipeline supports `testcontainers` for ephemeral PostgreSQL + Redis (per TDD §15.3).
- **A-8:** Production CPU class is ≥ comparable to the build agent used for the bcrypt-12 benchmark.
- **A-9:** Personalization features that depend on auth (Q2-Q3 2026) will not begin integration until GA is signaled.
- **A-10:** "auth-team provides 24/7 on-call rotation during first 2 weeks post-GA" (TDD §25.2) is honored.

---

## 12. Rollback & Failure-Mode Strategies

### 12.1 Rollback triggers (from TDD §19.4)

- p95 latency > 1000ms for > 5 minutes.
- Error rate > 5% for > 2 minutes.
- Redis connection failures > 10 per minute.
- Any `UserProfile` data loss / corruption.

### 12.2 Rollback procedure (from TDD §19.3, expanded)

1. Page on-call; declare incident in #auth-incidents.
2. Flip `AUTH_NEW_LOGIN` OFF — traffic routes back to legacy auth.
3. Smoke-test legacy login flow.
4. Snapshot Redis + PostgreSQL state for forensic analysis.
5. Investigate root cause via structured logs + traces.
6. If `UserProfile` corruption detected, restore from last known-good backup (RPO target: ≤15 min).
7. Notify auth-team + platform-team via incident channel.
8. Post-mortem within 48 hours.

### 12.3 Failure-mode catalog

| Failure | Detection | Auto-response | Manual response |
|---|---|---|---|
| PostgreSQL primary down | Health-check fail | Failover to replica (managed service) | Verify writes resumed |
| Redis cluster down | Health-check fail | `/auth/refresh` returns 503 | Scale Redis; force users to re-login on `LoginPage` |
| SendGrid down | Webhook errors | Email queue retries with backoff | Manual support workflow for reset requests |
| RSA private key inaccessible | Token signing fails 100% | Service returns 503 | Re-mount secret; emergency rotation if compromised |
| Migration deadlocks `user_profile` | Migration runner timeout | Migration aborts; service stays on old schema | Reschedule in maintenance window |
| Lockout-table runaway growth | Redis memory alert | None — sliding window self-cleans | Investigate brute-force campaign; block at WAF |
| Audit-log write latency | Span duration alert | None — write async via outbox | Investigate DB pressure |

---

## 13. Personas Coverage Check

The PRD names three personas; this roadmap verifies each is served by v1.0.

| Persona | Need served | Where in roadmap |
|---|---|---|
| Alex (end user) | Register, login, persistent session, reset password, view profile | M1, M2, M3, M4 |
| Jordan (admin) | Audit logs and lockout signals | M1 (audit-log schema), M3 (lockout events), CC2 (dashboards) |
| Sam (API consumer) | Programmatic login + refresh with clear error codes | M1 (`/auth/login`), M2 (`/auth/refresh`), DOC-5 (consumer docs) |

Sam's "stable auth contracts" need is reinforced by the OpenAPI spec maintained throughout M1-M3 (D-106, D-207, CC4) and the API governance section in TDD §8.4 (URL-prefix versioning, breaking changes require new major version).

---

## 14. Cost & Resource Plan

Anchored on TDD §26 ($450/month production infra) and TDD §25.3 (capacity).

| Resource | M1-M4 (staging) | M5 onward (prod) | Scaling trigger |
|---|---|---|---|
| `AuthService` pods | 1 replica | 3 replicas baseline | HPA → 10 at CPU >70% |
| PostgreSQL | Shared staging instance | Managed instance, 100-conn pool | Bump to 200-conn at wait >50ms |
| Redis | Single-node staging | Cluster mode, 1 GB | Scale to 2 GB at >70% utilization |
| SendGrid | Free tier (dev) | Paid plan with bounce handling | Volume-based plan upgrade |
| Engineering | 2 backend + 1 frontend FTE | + 0.5 SRE + 0.25 security review | — |
| Monthly run-rate | ~$50 (staging) | ~$450 + scales $50 per 10K users | Linear in user count |

---

## 15. Communication & Governance

| Artifact | Cadence | Audience |
|---|---|---|
| Roadmap status update | Weekly | Product, eng-manager, stakeholders |
| Burn-down per milestone | Weekly | auth-team |
| Risk register review | Bi-weekly | auth-team + security |
| Architecture decisions (ADRs) | As needed | All approvers in TDD §Approvers |
| GA go/no-go review | End of M5 sub-phase 5B | test-lead + eng-manager + sec-reviewer |
| Post-launch metrics review | Weekly for 4 weeks post-GA | Product + auth-team |
| Post-mortem | Within 48 hours of any rollback or P1 | All hands |

---

## 16. Glossary (roadmap additions beyond TDD §28)

| Term | Definition |
|---|---|
| Token family | The lineage of refresh tokens descending from a single login event; reuse detection revokes the entire family. |
| Sliding window (lockout) | Counter resets only when the window's worth of time has fully elapsed since the earliest failure, not on each request. |
| Sub-phase | A named step within a milestone, used here for M5 (5A internal alpha / 5B 10% beta / 5C 100% GA). |
| Soft / hard gate | A "hard gate" blocks the GA decision; a "soft gate" is observed and triaged but does not block. |
| Deliverable ID (D-NNN) | Concrete artifact owned by a milestone (e.g., D-103 = `PasswordHasher` module). |

---

## 17. Appendix A — Milestone-to-Requirement Traceability

| Requirement | Covered by |
|---|---|
| PRD FR-AUTH.1 / TDD FR-AUTH-001 | M1 D-105; M2 D-201/D-202; CC3 QA-6 |
| PRD FR-AUTH.2 / TDD FR-AUTH-002 | M1 D-103/D-104 |
| PRD FR-AUTH.3 / TDD FR-AUTH-003 | M2 D-201/D-202/D-203 |
| PRD FR-AUTH.4 / TDD FR-AUTH-004 | M2 D-204; M4 D-404 |
| PRD FR-AUTH.5 / TDD FR-AUTH-005 | M3 D-301/D-302/D-303/D-304 |
| PRD NFR-AUTH.1 / TDD NFR-PERF-001 + NFR-PERF-002 | M5 D-506 (k6 load test); CC2 OBS-3 |
| PRD NFR-AUTH.2 / TDD NFR-REL-001 | M5 D-501 (HPA + replicas); CC2 OBS-4 |
| PRD NFR-AUTH.3 / TDD NFR-SEC-001 | M1 D-103; CC1 SEC-1 |
| TDD NFR-SEC-002 | M2 D-201/D-205; CC1 SEC-6 |
| PRD legal: GDPR consent | M4 D-402; CC1 SEC-2 |
| PRD legal: SOC2 audit logging | M1 D-102; CC1 SEC-3; OQ-R1 resolution |
| PRD legal: NIST password storage | M1 D-103; CC1 SEC-1 |
| PRD legal: data minimization | M4 D-402; CC1 SEC-2 |
| TDD §13 account lockout | M3 D-305 |
| TDD §14 observability | CC2 OBS-1 through OBS-6 |
| TDD §19 rollout | M5 sub-phases 5A/5B/5C |
| TDD §24 release criteria | M5 D-507/D-510; §7.4 DoD |
| TDD §25 operational readiness | M5 D-503/D-509; CC2 OBS-5 |

---

## 18. Appendix B — Calendar (one-page view)

```
Week 1  (Mar 30 - Apr  5): M1 kickoff, schema + hasher
Week 2  (Apr  6 - Apr 13): M1 close — register + login endpoints
Week 3  (Apr 14 - Apr 20): M2 kickoff — JwtService + TokenManager
Week 4  (Apr 21 - Apr 27): M2 close — /auth/refresh + /auth/me
Week 5  (Apr 28 - May  4): M3 kickoff — reset endpoints + email + lockout
Week 6  (May  5 - May 11): M3 close — async email + audit events
Week 7  (May 12 - May 18): M4 kickoff — LoginPage + RegisterPage
Week 8  (May 19 - May 25): M4 close — AuthProvider silent refresh + E2E
Week 9  (May 26 - Jun  1): M5 5A — Internal Alpha in staging
Week 10 (Jun  2 - Jun  8): M5 5B — 10% Beta in production
Week 11 (Jun  9         ): M5 5C — 100% GA
Week 12-13 (Jun 10 - 23) : Stabilization, flag removal, post-mortem readiness
```

---

## 19. Closing Note

This roadmap honors the TDD's existing milestone dates and decomposes them into actionable deliverables, cross-cutting tracks, and a risk register that maps cleanly onto the named architectural components (`AuthService`, `TokenManager`, `JwtService`, `PasswordHasher`, `AuthProvider`). Where the source documents conflicted (90-day vs 12-month audit retention; sync vs async reset email; refresh-token storage strategy), the roadmap flags the conflict as an open question with a recommended resolution rather than silently choosing.

The single biggest delivery risk is the bcrypt-cost-12 latency budget (R-104): the TDD acknowledges ~300ms hash time against a 200ms p95 endpoint budget, and that math only works with aggressive connection pooling. M1 D-103 makes this measurable on day 1, and the rollback to cost 11 (with a documented security trade-off) is the pre-approved escape hatch.

The single biggest scope risk is the audit-log retention conflict (OQ-R1): SOC2 evidence horizon must be settled in week 1 because the storage cost and partition strategy depend on it.
