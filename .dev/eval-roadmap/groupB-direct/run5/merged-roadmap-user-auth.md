<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 1 (opus) -->
<!-- Non-base contributor: Variant 2 (sonnet) -->
<!-- Merge date: 2026-05-22 -->
<!-- Refactor plan: refactor-plan.md (26 changes: 9 HIGH invariant fixes + 12 V2 incorporations + 5 base-weakness fixes subsumed) -->

# User Authentication Service — Implementation Roadmap

> **Source:** `AUTH-PRD-001` (Product Requirements) + `AUTH-001-TDD` (Technical Design), merged at `inputs/merged-prd-tdd-user-auth.md`.
> **Target release:** v1.0 — GA 2026-06-09 (subject to OQ-R7 buffer decision; see §11.2).
> **Owning team:** auth-team (engineering), with product, security, frontend, and platform-team as cross-functional partners.
> **Roadmap horizon:** 11 calendar weeks (2026-03-30 through 2026-06-12), plus a 2-week post-GA stabilization tail.

---

<!-- Source: Base (original) -->
## 1. Vision & Outcome Statement

### 1.1 Business outcome

Ship a self-hosted, NIST SP 800-63B-aligned User Authentication Service that becomes the foundational identity layer for the platform. Success unlocks the Q2-Q3 2026 personalization roadmap (a projected $2.4M ARR), retires the 25% of churn attributable to "no accounts," and clears the Q3 2026 SOC2 Type II audit gate by closing the audit-logging finding.

### 1.2 Technical outcome

A horizontally-scalable, stateless REST service (`AuthService`) that:

- Issues RS256-signed JWT access tokens (15-min TTL) and Redis-backed opaque refresh tokens (7-day TTL) via `TokenManager` / `JwtService`.
- Persists `UserProfile` records in PostgreSQL 15 with bcrypt password hashes via `PasswordHasher` (cost factor determined by M1 benchmark — see D-103, R-104, R-117).
- Exposes four core endpoints (`/auth/login`, `/auth/register`, `/auth/me`, `/auth/refresh`) plus the password-reset pair (`/auth/reset-request`, `/auth/reset-confirm`).
- Integrates with `LoginPage`, `RegisterPage`, `ProfilePage`, and `AuthProvider` on the frontend.
- Meets NFR-PERF-001 (<200ms p95), NFR-PERF-002 (500 concurrent), and NFR-REL-001 (99.9% over 30 days).

### 1.3 What "done" looks like (single sentence)

A new user can register, log in, refresh silently for 7 days, reset a forgotten password, and view their profile — all in under 200ms p95, with every auth event captured in a tamper-evident audit log, and no plaintext credential ever touching storage or logs.

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

<!-- Source: Base (original, modified) — Change #10: three-phase rationale appended -->
## 2. Phasing Strategy

### 2.1 Decomposition rationale

The roadmap is decomposed into **five sequential milestones (M1-M5)** plus **five cross-cutting workstreams (CC1-CC5)** that run in parallel from week 1.

Sequencing was driven by three constraints from the source:

1. **TDD §23.1 anchors dates** — the TDD already proposes M1 (Core AuthService) → M2 (Token Mgmt) → M3 (Password Reset) → M4 (Frontend) → M5 (GA) on a fortnightly cadence. The roadmap honors that cadence and back-fills missing detail (entry/exit criteria, deliverables, dependencies).
2. **Dependency chain from architecture** — `PasswordHasher` and `UserProfile` schema are prerequisites for everything; `TokenManager` requires Redis + `JwtService`; password-reset requires email infra; the frontend cannot integrate until both token issuance and refresh exist. Note: lockout (`LoginAttemptTracker`) also requires Redis from Week 1 (see Change #1 / M1 scope).
3. **Rollout phasing from TDD §19** — Phase 1 (Internal Alpha) and Phase 2 (10% Beta) are folded into M5; both feature flags (`AUTH_NEW_LOGIN`, `AUTH_TOKEN_REFRESH`) gate exposure during M5.

<!-- Source: V2 (sonnet), Section 2.2 "Why Three Phases, Not Two" — merged per Change #10 -->
4. **Three-phase operational clustering** — The PRD prescribes two phases (Core + Integration), but the TDD's five-milestone structure naturally clusters into three operational phases: Core Auth (M1+M2), Self-Service Recovery + User-Facing Integration (M3+M4), and Hardening + GA (M5). Separating M3 (password reset, which has external SendGrid dependency and unique email-delivery failure modes) from M4 (frontend integration, which is purely internal) isolates risk and allows M3/M4 to parallelize partially.

### 2.2 Phase map

| Phase | Milestones | Theme | Calendar window |
|---|---|---|---|
| Foundations | M1 | Schema + core service + bcrypt + register/login + **lockout + defense-in-depth + audit immutability** | Week 1-2 (2026-03-30 → 2026-04-13) |
| Stateful sessions | M2 | JWT + refresh + `/auth/me` + family lineage + token cap + login-transaction ordering | Week 3-4 (2026-04-14 → 2026-04-27) |
| Self-service recovery | M3 | Password reset, email integration (single-attempt + dead-letter), admin audit query | Week 5-6 (2026-04-28 → 2026-05-11) |
| User-facing integration | M4 | `LoginPage`, `RegisterPage`, `ProfilePage`, `AuthProvider`, silent refresh | Week 7-8 (2026-05-12 → 2026-05-25) |
| Hardening + GA | M5 | Internal alpha → 10% beta → 100% GA, runbooks, on-call enablement | Week 9-11 (2026-05-26 → 2026-06-09) |
| Stabilization | Post-GA | Flag removal, post-mortem readiness, capacity tuning | Week 12-13 (2026-06-10 → 2026-06-23) |

### 2.3 Critical path

`Schema (D-101)` → `PasswordHasher (D-103)` → `Register/Login (D-104, D-105)` → `Lockout + global rate limit (D-108, D-109) [M1]` → `JwtService (D-201)` → `TokenManager + family lineage + 10-token cap (D-202, D-209)` → `/auth/refresh + /auth/me (D-203, D-204)` → `AuthProvider silent refresh (D-403)` → `M5 rollout`.

Password reset (M3) and frontend (M4) parallelize partially: `LoginPage` / `RegisterPage` can begin against mocked backends during M2; only `AuthProvider` silent refresh blocks on M2 exit.

---

## 3. Milestones

<!-- Source: Base (original, modified) — Multiple changes applied: Fix #9 (bcrypt), Fix #8 (defense-in-depth), Fix #2 (NULL user_id), Fix #7 (audit immutability), Change #1 (lockout-in-M1) -->
### M1 — Core `AuthService`, schema, register + login, lockout, defense-in-depth, audit immutability

- **Window:** 2026-03-30 → 2026-04-13 (2 weeks)
- **Theme:** Establish the data plane, the two unauthenticated endpoints, and the brute-force defense-in-depth stack.
- **Maps to:** TDD §23.1 M1; PRD FR-AUTH.1, FR-AUTH.2; TDD FR-AUTH-001, FR-AUTH-002; PRD R-002 (brute-force mitigation).

**Scope**

- `UserProfile` table in PostgreSQL 15 (id UUIDv4 PK, email UNIQUE+lowercase, displayName 2-100 chars, createdAt, updatedAt auto, lastLoginAt NULLABLE, roles default `["user"]`).
- `audit_log` table (id, **user_id UUID NULL** — see Fix #2 / INV-005; nullable to permit pre-auth failure events for unknown emails — event_type, ip, user_agent, outcome, email_hash, occurred_at) with the retention policy parameterized (default 90d per TDD §7.2, set to 12 months pending OQ-R1 resolution).
- **Audit-log immutability controls (Fix #7 / INV-022):** Migration creates a DB trigger `prevent_audit_modification BEFORE UPDATE OR DELETE ON audit_log` that raises an error. A dedicated DB role `audit_writer` is created with INSERT-only grants (no UPDATE/DELETE). The application uses this role for all audit writes. SOC2 CC6.1 + CC7.2 controls map to D-110.
- `PasswordHasher` wrapper around `bcryptjs` with **cost factor determined by M1 benchmark on target hardware** (Fix #9 / INV-026). Default cost factor: 11 (~100ms estimated). Target cost factor: 12 (~300ms). Ship at cost 11 unless M1 benchmark demonstrates cost-12 within the 200ms p95 budget inclusive of DB writes and Redis ops. Pluggable interface for future argon2id migration (NG ref to TDD §6.4 rationale).
- `AuthService.register()` and `AuthService.login()` orchestration. Login path follows the transaction ordering defined in §9.5 (per Fix #5 / INV-017): transactional DB writes (lastLoginAt + audit) then Redis SET for refresh token outside the DB transaction.
- `POST /auth/register` (201 / 400 / 409) and `POST /auth/login` (200 / 401 / 423) with the canonical error envelope from TDD §8.3.
- Email normalization (lowercase + trim) at write and read for the unique constraint to hold.
- Password policy validator: ≥8 chars, ≥1 uppercase, ≥1 number (TDD FR-AUTH-002 AC #3); reject before hashing.

- **Account-lockout policy (Change #1, moved from M3 per V2):** 5 failed logins in 15 minutes → `423 Locked` from `/auth/login` (PRD Error Handling table; TDD §13). Lockout state stored in Redis with sliding 15-minute window. Per-account+IP combination (rather than per-account global) to limit DoS surface.

- **Defense-in-depth brute-force stack (Fix #8 / INV-023):** PRD R-002 co-requires lockout AND rate limiting. The roadmap implements four layers (Layer 4 deferred to v1.0 contingency):
  - Layer 1 (M1): Per-account lockout — D-108 LoginAttemptTracker in Redis (sliding window, 5 fails / 15 min, per account+IP).
  - Layer 2 (M1): Gateway IP rate limit — 10 req/min/IP on `/auth/login` (R-102). Already provisioned via API gateway.
  - Layer 3 (M1): Per-account global rate limit — D-109 max 20 login attempts per email-hash per hour across all IPs. Enforced in Redis via sliding window keyed on SHA256(email).
  - Layer 4 (M5 contingency, NOT shipped in v1.0): CAPTCHA after 3 failures (R-112). Documented escalation path if layers 1-3 prove insufficient.

**Deliverables**

| ID | Deliverable | Owner |
|---|---|---|
| D-101 | `migrations/0001_user_profile.sql` (idempotent, includes lowercase-email index) | auth-team |
| D-102 | `migrations/0002_audit_log.sql` with `user_id UUID NULL`, `email_hash` column, retention parameterized (default 90d per TDD, set to 12 months pending OQ-R1) | auth-team |
| D-103 | `PasswordHasher` module with cost factor selected by M1 Week 1 benchmark on target hardware. Default cost-11; cost-12 only if full-path benchmark (bcrypt + DB + Redis) ≤200ms p95. Unit tests cover chosen-cost invariant and 500ms upper-bound timing test. | auth-team |
| D-104 | `AuthService.register()` + `POST /auth/register` handler | auth-team |
| D-105 | `AuthService.login()` + `POST /auth/login` handler (returns placeholder token in M1; real JWT lands in M2) | auth-team |
| D-106 | OpenAPI 3.1 fragment for the two endpoints, committed to `/docs/api/auth.yaml` | auth-team |
| D-107 | Local Docker Compose stack (PostgreSQL 15 + Redis 7) for developer onboarding | devops |
| D-108 | Lockout module (`LoginAttemptTracker`) using Redis sliding window (moved from M3 per Change #1) | auth-team |
| D-109 | Per-account global rate limit module — Redis sliding window keyed on SHA256(email), max 20 attempts/email-hash/hour across all IPs (Fix #8 Layer 3) | auth-team |
| D-110 | Audit-log immutability controls: UPDATE/DELETE trigger + `audit_writer` DB role + integrity verification script (Fix #7 / INV-022) | security + auth-team |

**Entry criteria**

- PostgreSQL 15+ instance provisioned in staging (PRD Dependencies).
- **Redis 7+ instance provisioned in staging** (required for lockout state storage in D-108 and global rate limit in D-109; entry moved from M2 per Change #1).
- Node.js 20 LTS baseline image published.
- Repository scaffolded with linting, formatter, and CI hook for `pnpm test`.

**Exit criteria**

- All D-101 → D-110 merged to main.
- Unit-test coverage for `AuthService` + `PasswordHasher` ≥80%.
- `POST /auth/register` round-trips against staging PostgreSQL, persists `UserProfile`, idempotently rejects duplicate email with 409.
- `POST /auth/login` validates password via `PasswordHasher.verify()` and returns 401 generically (no user enumeration; identical timing within 50ms tolerance between unknown-user and wrong-password paths). The unknown-email path computes a dummy bcrypt hash to match timing (Fix #3 / INV-006).
- **Audit-log INSERT succeeds for `login_failure` events where `user_id` is NULL** (unknown-email path; Fix #2 / INV-005).
- **Audit-log immutability verified:** attempted UPDATE or DELETE on `audit_log` raises a DB trigger error; `audit_writer` role lacks UPDATE/DELETE grants (Fix #7).
- **Account locks after 5 failed logins within 15 minutes; returns 423.** Counter resets after 15-minute sliding window expires (Change #1).
- **Per-account global rate limit enforced:** 20 attempts/email-hash/hour across all IPs verified in integration test (Fix #8 Layer 3).
- `PasswordHasher` benchmark on **target hardware** confirms chosen cost factor (11 or 12) produces total login-path latency within 200ms p95 budget. Benchmark must include bcrypt + DB writes + Redis operations as a full-path measurement (Fix #9 / INV-026).
- OpenAPI fragment validated with `redocly lint`.

**Dependencies & sequencing**

- Blocks: M2 (token issuance can't reuse `AuthService.login()` without M1's contract).
- Blocked by: nothing — this is the start of the critical path. Note that Redis provisioning (CC5 INF-2) must complete in Week 0/1 to unblock D-108.

**Duration estimate:** 10 working days. Risk buffer: +2 days for bcrypt-cost benchmarking surprises on the chosen runtime. The lockout module adds ~20-30 LoC (per V2 estimate); incorporated within the 10-day window.

---

<!-- Source: Base (original, modified) — Fix #1 (family lineage), Fix #4 (eviction guard), Fix #5 (login transaction), Change #6 (10-token FIFO cap) -->
### M2 — Token management (`JwtService`, `TokenManager`, `/auth/refresh`, `/auth/me`)

- **Window:** 2026-04-14 → 2026-04-27 (2 weeks)
- **Theme:** Make sessions persistent and stateless, with durable family-lineage tracking.
- **Maps to:** PRD FR-AUTH.3, FR-AUTH.4; TDD FR-AUTH-003, FR-AUTH-004.

**Scope**

- `JwtService.sign()` / `verify()` using RS256 with 2048-bit RSA keypair (TDD NFR-SEC-002). Keypair loaded from a secret mount; rotation cadence is quarterly with overlap window (TDD §13).
- `JwtService` clock-skew tolerance: 5 seconds (TDD §12).
- `TokenManager.issueTokens()` → returns `AuthToken` (access 15min, refresh 7day, expiresIn=900, tokenType="Bearer").
- `TokenManager` stores **hashed** refresh tokens in Redis 7 with 7-day TTL (TDD §13 — "Refresh tokens are stored as hashed values").
- **Family-lineage storage (Fix #1 / INV-001):** Each refresh-token record stores `family_id` (UUID, set at first issuance) and `parent_id` (hash of previous token in chain, or NULL for root). Stored as a Redis Hash per token with fields `family_id`, `parent_id`, `user_id`, `issued_at`, `status` (issued/rotated/revoked/evicted). A Redis Sorted Set per family `family:{family_id}:members` (score = issued_at, value = token hash) enables efficient family-wide operations. **Redis AOF persistence enabled with `appendfsync everysec`** (TDD §6.3) so family metadata survives cold-start. Family metadata Sorted Set TTL = max refresh-token TTL + 24h buffer (8 days).
- `TokenManager.refresh()` rotates refresh tokens (revoke old, issue new) — refresh-token reuse detection logs a security event and revokes the entire family (subject to evicted-token guard below).
- **Per-user 10-token FIFO cap (Change #6 + Fix #4 / INV-013):** TokenManager enforces a per-user limit of 10 active refresh tokens. When an 11th token is issued, the oldest is evicted via FIFO. **Eviction marks the token's family entry as `evicted=true`** in the family Sorted Set metadata. Reuse-detection consults this flag: if `evicted=true`, the event is logged as a `token_evicted_reuse` audit event at WARNING level and 401 is returned for that token only — the family is NOT revoked (prevents false-positive multi-device logout). If `evicted=false` or absent, normal family-wide revocation proceeds.
- `POST /auth/refresh` and `GET /auth/me` endpoints. `/auth/me` includes id, email, displayName, createdAt, updatedAt, lastLoginAt, roles (TDD FR-AUTH-004 AC #3).
- `lastLoginAt` updated by `AuthService` on each successful login per the transaction ordering in §9.5 (Fix #5 / INV-017).
- Audit-log writes for `login_success`, `login_failure`, `token_refresh_success`, `token_refresh_failure`, `token_reuse_detected`, `token_evicted_reuse`.

**Deliverables**

| ID | Deliverable | Owner |
|---|---|---|
| D-201 | `JwtService` (sign / verify / rotate-aware key resolver) + unit tests | auth-team |
| D-202 | `TokenManager` with hashed-refresh-token storage in Redis + rotation + reuse-detection + **family-lineage storage schema (Fix #1) + eviction-family-guard logic (Fix #4)** + unit tests | auth-team |
| D-203 | `POST /auth/refresh` handler | auth-team |
| D-204 | `GET /auth/me` handler with Bearer-token middleware | auth-team |
| D-205 | Key-rotation runbook stub (quarterly cadence, overlap window) | security |
| D-206 | Audit-log integration for the events listed above | auth-team |
| D-207 | OpenAPI fragments for `/auth/refresh` and `/auth/me` | auth-team |
| D-208 | k6 baseline load script for the four endpoints (used in M5) | qa |
| D-209 | Per-user token-count enforcement with FIFO eviction in TokenManager (Change #6) | auth-team |

**Entry criteria**

- M1 exit criteria met.
- Redis 7 instance available since M1 entry (provisioning per CC5 INF-2); cluster mode + persistence (AOF) verified before M2 kickoff.
- RSA keypair generated and stored in secrets manager; CI has read access to a development keypair.

**Exit criteria**

- Login returns a real `AuthToken` pair; expired access tokens return 401 (TDD FR-AUTH-004 AC #2).
- `/auth/refresh` with valid token returns new pair and old refreshToken is revoked.
- Refresh-token reuse triggers a `token_reuse_detected` audit event AND revokes the entire token family for that user (when the family is NOT marked `evicted=true`).
- **Family-linkage metadata survives simulated Redis restart (FLUSHALL + AOF reload).** Reuse-detection on a pre-restart token still revokes the family (Fix #1 integration test).
- **11-device eviction test (Fix #4):** User with 11 devices: login on device 11 evicts device 1's token. Device 1's stale token triggers reuse-detection. Result: device 1 gets 401 only; devices 2-11 remain active. Family NOT revoked. `token_evicted_reuse` audit event emitted at WARNING.
- **Login-path Redis-failure test (Fix #5):** Login succeeds at DB level but Redis SET fails. Verify: audit_log has `login_success` row, `lastLoginAt` updated, client receives 503, retry succeeds and produces a second `login_success` row (idempotent semantics documented).
- Clock-skew tolerance test: tokens with `iat` within ±5s of server time accepted (TDD §12).
- Redis-unavailable test: `/auth/refresh` returns 503 with explicit error code rather than silently issuing tokens (TDD §12 fallback semantics).
- Coverage for `JwtService` and `TokenManager` ≥80%.

**Dependencies**

- Blocks: M3 (password-reset flow uses `TokenManager` to invalidate all sessions on reset — FR-AUTH.5 AC), M4 (`AuthProvider` silent refresh).
- Blocked by: M1.

**Duration estimate:** 10 working days. Risk buffer: +2 days if key-rotation overlap semantics need a second design pass, +1 day for family-lineage AOF testing.

---

<!-- Source: Base (original, modified) — Change #1 (lockout removed from M3), Change #5 (admin audit query D-309), Fix #6 (SendGrid retry D-303 + D-310) -->
### M3 — Password reset, email integration, enumeration-safe paths, admin audit query

- **Window:** 2026-04-28 → 2026-05-11 (2 weeks)
- **Theme:** Self-service recovery without leaking account existence.
- **Maps to:** PRD FR-AUTH.5; TDD FR-AUTH-005.

**Scope**

- `POST /auth/reset-request` — always returns 200 with a generic confirmation, regardless of whether the email is registered (PRD error-handling row "Reset requested for unregistered email"; TDD §13).
- `POST /auth/reset-confirm` — validates the single-use, 1-hour-TTL token; updates the password hash via `PasswordHasher`; invalidates **all** existing refresh-token families for the user via `TokenManager` (FR-AUTH.5 AC: "new password invalidates all sessions").
- `password_reset_tokens` table or Redis namespace (decision: Redis with 1-hour TTL — simpler revocation; document trade-off in ADR).
- **Email integration with single-attempt + dead-letter pattern (Fix #6 / INV-021):** SendGrid client wrapper performs a single API call with a 5-second timeout. On success, email is sent. On failure (timeout or 5xx), the email payload is logged to a `pending_emails` PostgreSQL table and the handler returns 200 to the client (anti-enumeration always-200 preserved). A cron-based retry sweep (every 5 minutes) processes `pending_emails`, increments retry_count on each attempt, alerts after 10 retries.
- Template includes the reset link, the 1-hour expiry, and an "if you didn't request this, ignore" line.
- Note: account-lockout was moved to M1 per Change #1 (LoginAttemptTracker is D-108 in M1).
- Admin-notification hook on lockout (PRD error-handling row "Wrong password (≥5 attempts): Admin notified"). The structured event is emitted from M1 D-108; the notifier (Slack / pager) is a CC2 deliverable (OBS-5).
- **Admin audit-log query endpoint (Change #5 / V2 D-030):** `GET /admin/audit-logs?from=&to=&user_id=&event_type=` with pagination. Satisfies Jordan persona's "view authentication event logs" user story.

**Deliverables**

| ID | Deliverable | Owner |
|---|---|---|
| D-301 | `AuthService.requestPasswordReset()` + `AuthService.confirmPasswordReset()` | auth-team |
| D-302 | `POST /auth/reset-request` and `POST /auth/reset-confirm` handlers | auth-team |
| D-303 | SendGrid client wrapper with single-attempt 5-second timeout + `pending_emails` dead-letter table integration (Fix #6) | auth-team |
| D-304 | Reset-email template (HTML + plaintext fallback) | auth-team + design |
| D-306 | `password_reset_requested`, `password_reset_completed`, `account_locked`, `account_unlocked` audit events (lockout events emitted from M1 D-108) | auth-team |
| D-307 | Migration to ensure all refresh-token families are revocable by user_id | auth-team |
| D-308 | ADR: synchronous vs asynchronous reset email — recommend single-attempt + dead-letter (Fix #6) | auth-team |
| D-309 | Admin audit-log query endpoint (`GET /admin/audit-logs` with date-range, user-ID, event-type filters + pagination) (Change #5) | auth-team |
| D-310 | `pending_emails` table migration + retry sweep cron job (5-minute interval, 10-retry cap) (Fix #6) | auth-team + devops |

(Note: D-305 was removed in this merge — lockout moved to M1 D-108 per Change #1.)

**Entry criteria**

- M2 exit criteria met.
- SendGrid API credentials provisioned for staging and production (separate keys).
- Email-from domain (`auth@<platform-domain>`) has SPF / DKIM / DMARC records published — verify before M3 starts (CC5 INF-3 / CC2 OBS-7 dependency).

**Exit criteria**

- `/auth/reset-request` returns 200 in <200ms p95 for both registered and unregistered emails; timing variance <30ms between paths (enumeration-safety bar).
- **`/auth/reset-request` returns 200 in <200ms p95 even when SendGrid is unavailable** (email queued for retry per Fix #6).
- `/auth/reset-confirm` with valid token updates password and revokes every active refresh token for the user. Manual verification: log in on two devices, request reset, confirm; both devices receive 401 on next refresh.
- Reset tokens cannot be reused (second submission returns 410 Gone).
- Reset tokens expire at exactly 1 hour (test with frozen clock).
- Email delivery success rate >99% measured against SendGrid status webhook.
- Reset-flow completion rate measurable via `password_reset_requested` → `password_reset_completed` funnel.
- **Admin audit-log query endpoint returns filtered, paginated results** (Change #5 / D-309).

**Dependencies**

- Blocks: M5 (rollout cannot ship without the full FR set).
- Blocked by: M2.

**Duration estimate:** 10 working days. Risk buffer: +3 days if email deliverability requires DNS coordination outside auth-team.

---

<!-- Source: Base (original) -->
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

<!-- Source: Base (original, modified) — Fix #7 (M5 audit immutability verification), Change #9 (beta buffer) -->
### M5 — Rollout: Internal Alpha → 10% Beta → 100% GA

- **Window:** 2026-05-26 → 2026-06-09 (2 weeks; subject to OQ-R7 buffer decision)
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
  - Deprecate any legacy auth endpoints (issue a sunset header for two weeks before removal). [Note: greenfield deployment — legacy endpoints exist only if introduced incidentally during platform development.]
  - Exit gate: 99.9% uptime over the first 7 days post-GA (TDD §19.1 Phase 3).

**M5 Risk Notes (Change #9 — Beta 1-week hidden buffer)**

- **Schedule management:** Embed a 1-week hidden buffer between Beta (5B) completion and GA (5C). This buffer is not reflected in the public timeline.
- **Arithmetic constraint (INV-010 cross-reference):** V1's 11-week active cadence plus V2's +1 week hidden buffer totals 12 active weeks. To preserve the 2026-06-09 GA date, either (a) compress CC2/CC4 activities in Week 9-10, or (b) accept GA slip to 2026-06-16. Decision owner: Product Manager. Resolution deadline: M5 sub-phase 5A entry. Tracked as OQ-R7.

**Deliverables**

| ID | Deliverable | Owner |
|---|---|---|
| D-501 | Production-ready Helm/Kubernetes manifests with 3-pod baseline + HPA to 10 (TDD §25.3) | devops |
| D-502 | Feature-flag wiring (`AUTH_NEW_LOGIN`, `AUTH_TOKEN_REFRESH`) in the production flag service | devops |
| D-503 | Runbook entries for `AuthService` down + token-refresh failures (TDD §25.1) | auth-team |
| D-504 | Grafana dashboard: `auth_login_total`, `auth_login_duration_seconds`, `auth_token_refresh_total`, `auth_registration_total`, `pending_emails_count` (TDD §14) | observability |
| D-505 | Prometheus alert rules: login failure rate >20% / 5min; p95 >500ms; Redis connection-failure alarm; `pending_emails` row count >100 (TDD §14) | observability |
| D-506 | k6 load-test run at 500 concurrent users; report attached to release ticket | qa |
| D-507 | Security review sign-off (PasswordHasher chosen cost verified; JwtService key rotation documented; audit immutability verified) (TDD §24.1) | security |
| D-508 | Rollback dry-run in staging proving the procedure in §12.2 works end-to-end (greenfield-correct per Change #2) | devops + auth-team |
| D-509 | On-call training session + game-day with simulated outage | auth-team |
| D-510 | Go/no-go sign-off captured from test-lead and eng-manager (TDD §24.2) | leadership |

**Entry criteria**

- M1, M2, M3, M4 all complete.
- Security review (CC1) checkpoint passed.
- Observability stack (CC2) green in staging.
- Infrastructure (CC5) all green: prod K8s, Redis cluster, PostgreSQL, feature flag service.
- Runbooks (D-503) reviewed by on-call team.

**Exit criteria**

- 99.9% uptime over 7 consecutive days post-GA.
- Both feature flags `AUTH_NEW_LOGIN` and `AUTH_TOKEN_REFRESH` flipped ON; removal targets per Appendix C.
- Zero P0 incidents in the first 72 hours of GA.
- Headline metrics from §1.4 reported on the dashboard for at least 7 days.
- **Audit-log immutability controls verified in production (Fix #7):** trigger active on `audit_log`, `audit_writer` role enforced, quarterly integrity verification script green.

**Duration estimate:** 10 working days, with the alpha → beta → GA ramp baked in (plus the +1 week hidden buffer per Change #9 / OQ-R7).

---

## 4. Cross-Cutting Workstreams

These tracks run **in parallel** with M1-M5 starting Week 1.

<!-- Source: Base (original, modified) — Fix #7 (CC1 SEC-3 expansion) -->
### CC1 — Security & Compliance

- **Lead:** sec-reviewer
- **Cadence:** Weekly checkpoint review; gate at the end of M2, M4, and M5.
- **Workstream items:**
  - SEC-1: NIST SP 800-63B compliance review of password policy and storage (PRD legal/compliance).
  - SEC-2: GDPR data-minimization audit — confirm only `email`, `hashed password`, `displayName` collected, plus `consent_at` timestamp (PRD legal/compliance).
  - SEC-3: SOC2 Type II audit-log evidence — verify the 12-month retention (PRD) reconciles with the TDD's 90-day retention; **gap resolution: bump audit log retention to 12 months in D-102 to satisfy the SOC2 row**. Expanded per Fix #7 / INV-022: (a) DB trigger preventing audit_log UPDATE/DELETE (in D-110), (b) separate `audit_writer` DB role with INSERT-only grants (in D-110), (c) quarterly log-integrity verification script that checksums row counts and detects gaps in event sequence.
  - SEC-4: Threat-modeling pass before M5 (STRIDE on `AuthService`, `TokenManager`, `JwtService`).
  - SEC-5: Penetration test before GA — explicitly listed in PRD Risk Analysis as a mitigation for "Security breach from implementation flaws." Budget: $5,000-$15,000 (Change #7; see §14 cost table).
  - SEC-6: Quarterly RSA key rotation runbook owned jointly with devops.
  - SEC-7: CORS policy lockdown to known frontend origins (TDD §13).
  - SEC-8: TLS 1.3 enforcement at the API gateway (TDD §13).

<!-- Source: Base (original, modified) — Fix #2 (OBS-1 NULL user_id verification), Change #12 (CC5 cross-references) -->
### CC2 — Observability & Operational Readiness

- **Lead:** auth-team + platform-team
- **Workstream items:**
  - OBS-1: Structured logging — JSON logs with `correlation_id`, `user_id` (nullable for pre-auth), `event_type`, `outcome`. Sensitive fields (`password`, `accessToken`, `refreshToken`) stripped via a logger middleware. **Verification (Fix #2 / INV-005):** NULL `user_id` audit rows are written correctly in M1 integration tests. Test case: login with unregistered email produces an `audit_log` row with `user_id=NULL` and a populated `email_hash`.
  - OBS-2: OpenTelemetry spans across `AuthService` → `PasswordHasher` → `TokenManager` → `JwtService` (TDD §14).
  - OBS-3: Prometheus metrics emission from M2 onward, dashboards from start of M3.
  - OBS-4: Alert rules tested with synthetic failure injection at end of M4.
  - OBS-5: Admin-notification channel (Slack #auth-incidents) wired up before M5 sub-phase 5A; consumes the `account_locked` event from D-306.
  - OBS-6: Capacity planning per TDD §25.3 — confirm Redis 1 GB suffices for ~100K refresh tokens + family-metadata sorted sets + lockout sliding windows + global rate-limit windows; build dashboard alarm at 70% utilization. (Provisioning tracked in CC5 INF-2.)
  - OBS-7: DNS / SPF / DKIM / DMARC for email-from domain (blocks M3 entry). (Provisioning tracked in CC5 INF-3.)
  - OBS-8: `pending_emails` table monitoring (row-count alert >100 — Fix #6 / D-310 retry sweep).

<!-- Source: Base (original, modified) — Fix #3 (QA-6 audit-write timing) -->
### CC3 — Testing & Quality

- **Lead:** qa
- **Workstream items:**
  - QA-1: Unit-test scaffolding from M1; coverage gate (≥80%) enforced in CI by end of M2.
  - QA-2: Integration tests with `testcontainers` for PostgreSQL + Redis from M1.
  - QA-3: Contract tests against the OpenAPI spec (D-106, D-207) by end of M2.
  - QA-4: Playwright E2E suite by end of M4 (D-406).
  - QA-5: k6 load-test framework by end of M2 (D-208); 500-concurrent run before M5 sub-phase 5B (D-506).
  - QA-6: Enumeration-timing test — assert <50ms variance between unknown-user / wrong-password 401 responses, and <30ms variance between reset-request for registered / unregistered email. **Test executes with audit writes ENABLED** (Fix #3 / INV-006). Verifies identical-shape audit INSERTs on both paths (NULL vs UUID `user_id`, populated `email_hash`) and verifies the dummy bcrypt on the unknown-email path produces matching latency.
  - QA-7: Chaos test — Redis down test (including AOF reload for family-lineage durability per Fix #1), PostgreSQL failover test, SendGrid down test (verifies Fix #6 dead-letter behavior).
  - QA-8: Test data: staging seeded with at least 50 test accounts with varied profiles (TDD §15.3).

<!-- Source: Base (original) -->
### CC4 — Documentation & Enablement

- **Lead:** scribe + auth-team
- **Workstream items:**
  - DOC-1: OpenAPI 3.1 spec maintained throughout M1-M3.
  - DOC-2: Tech Reference document (downstream of TDD) populated as endpoints land.
  - DOC-3: Frontend integration guide for `AuthProvider` consumers (other teams).
  - DOC-4: On-call runbook (D-503).
  - DOC-5: API consumer documentation for "Sam the API Consumer" persona — emphasis on refresh-token flow and error codes. Cross-reference Appendix D (API Endpoint Summary).
  - DOC-6: Internal blog post + recorded demo before GA.
  - DOC-7: PRD Open Questions resolved and recorded:
    - OQ-1 (sync vs async reset email) → single-attempt + dead-letter (Fix #6; recorded in D-308 ADR).
    - OQ-2 (max refresh tokens per user) → 10 active refresh tokens per user, oldest evicted on new issuance (FIFO) (Change #6).
    - OQ-3 (lockout policy) → 5 attempts / 15 min sliding window per account+IP (TDD §13; implemented in M1 D-108).
    - OQ-4 ("remember me") → out of scope for v1.0; refresh token already provides 7-day persistence.

<!-- Source: V2 (sonnet), Section 4.5 "Infrastructure Workstream" — merged per Change #12 -->
### CC5 — Infrastructure & Platform

- **Lead:** devops + platform-team
- **Workstream items:**
  - INF-1: PostgreSQL 15+ provisioning + connection pooling (Week -1 to Week 1).
  - INF-2: Redis 7+ provisioning with AOF persistence (`appendfsync everysec`) and cluster mode for prod (Week 1 — moved earlier from M2 entry to support M1 lockout in D-108 per Change #1; AOF requirement per Fix #1).
  - INF-3: API Gateway rate-limit configuration: 10 req/min/IP on `/auth/login` (Layer 2 of defense-in-depth) + DNS/SPF/DKIM/DMARC for email-from domain (Week 2).
  - INF-4: Kubernetes manifests + HPA (3 replicas baseline, scale to 10 on CPU >70%) (Week 3-4).
  - INF-5: CI/CD pipeline: build, test, deploy to staging (Week 1-2).
  - INF-6: Feature flag infrastructure setup (`AUTH_NEW_LOGIN`, `AUTH_TOKEN_REFRESH` registered) (Week 8).
  - INF-7: Production environment provisioning + cutover verification (Week 9).

---

<!-- Source: Base (original, modified) — Fix #1 (R-105 AOF), Fix #9 (R-117 added), Fix #8 (R-102 layered) -->
## 5. Risk Register

Risks are scored as **Probability (Low/Med/High) × Impact (Low/Med/High/Critical)**. Each risk has a mitigation, an owner role, and a monitoring mechanism so it is observable rather than relying on memory.

| ID | Risk | Prob × Impact | Mitigation | Owner | Monitoring |
|---|---|---|---|---|---|
| R-101 | Token theft via XSS allows session hijacking (TDD R-001) | Med × High | Access token in memory only; refresh token in HttpOnly+SameSite=Strict cookie; CSP locked down; `AuthProvider` clears tokens on tab close | security + frontend | Synthetic XSS test in CI; CSP-violation report endpoint |
| R-102 | Brute-force login attacks (TDD R-002) | High × Med | **Defense-in-depth (Fix #8):** Layer 1 per-account lockout 5 fails/15min (D-108); Layer 2 gateway IP rate limit 10/min/IP; Layer 3 per-account global rate limit 20/email-hash/hour (D-109); Layer 4 CAPTCHA after 3 failures (M5 contingency, R-112). bcrypt cost ≥11. | security | `auth_login_total{outcome="failure"}` rate alert; per-email-hash rate alert |
| R-103 | Data loss during cutover (TDD R-003) | Low × High | Idempotent upserts; full DB backup before each rollout sub-phase; parallel run during 5B | auth-team + devops | Backup-verify cron + restore drill in CC1 |
| R-104 | bcrypt cost-12 exceeds 200ms p95 latency budget on target hardware | Med × Med | **Ship at cost 11 unless M1 benchmark demonstrates cost-12 within budget (Fix #9). Document security rationale: cost-11 meets NIST SP 800-63B minimum with substantial margin.** | auth-team | M1 D-103 bench report; APM histogram |
| R-105 | Redis becomes a single point of failure for refresh tokens (TDD §12 fallback "reject refresh requests") | Med × High | Redis cluster mode in production; multi-AZ; read replicas; **AOF persistence with `appendfsync everysec` (Fix #1)** so family-lineage metadata survives cold-start; explicit 503 on outage; client-side prompts re-login | platform-team | Redis-health alert (D-505); refresh-error spike alert; AOF reload integration test |
| R-106 | SendGrid outage blocks password reset (PRD risk) | Low × Med | **Single-attempt + dead-letter (Fix #6):** /auth/reset-request returns 200 within budget; failed sends queued to `pending_emails` for cron retry sweep; alert at >100 pending | auth-team | `pending_emails` row count alert; SendGrid webhook delivery-rate dashboard |
| R-107 | RSA private key compromise | Low × Critical | Keys in secret manager with audit log; quarterly rotation; emergency rotation runbook; refresh-token revocation flushes all sessions | security | Secret-access audit; alerting on out-of-cycle access |
| R-108 | SOC2 audit fails due to insufficient log retention or tampering | Med × High | Bump audit-log retention to 12 months (SEC-3); **audit-log immutability controls via DB trigger + audit_writer role (Fix #7 / D-110)**; quarterly integrity verification; evidence pack assembled before GA | security + compliance | Quarterly evidence review; integrity script CI green |
| R-109 | Clock skew between API nodes invalidates valid tokens | Low × Med | NTP enforcement on all nodes; `JwtService` 5s tolerance window (TDD §12) | platform-team | NTP-drift alert |
| R-110 | Email enumeration via timing side-channel on `/auth/reset-request` or `/auth/login` | Med × Med | Constant-time response; identical-shape audit writes including `email_hash` on both failure paths; dummy bcrypt on unknown-email login path (Fix #3); QA-6 enforces <30ms variance reset / <50ms login WITH audit writes enabled | security + auth-team | QA-6 in CI |
| R-111 | Refresh-token replay after rotation | Low × High | Rotation invalidates old token; reuse-detection revokes entire family (with eviction-flag guard per Fix #4 to prevent false-positive revocation on legitimately evicted tokens) | auth-team | `token_reuse_detected` audit event alert; `token_evicted_reuse` WARNING alert |
| R-112 | Account lockout used as a denial-of-service vector | Med × Med | Lockout is per-account+IP rather than per-account global; admin unlock path; CAPTCHA after 3 failures (PRD R-002 contingency / Defense Layer 4) | security | `account_locked` event-rate alert |
| R-113 | GDPR consent not captured before account creation | Low × High | `RegisterPage` blocks submit until consent box ticked; `consent_at` written in same transaction as `UserProfile` | frontend + auth-team | DB invariant test in CI |
| R-114 | Frontend silent-refresh storm caused by faulty 401 interceptor | Med × Med | Refresh-once-per-access-token-lifecycle guard; mutex around refresh call | frontend | `auth_token_refresh_total` rate ceiling alert |
| R-115 | Long-running migration locks `user_profile` table during M1 cutover | Low × Med | Migrations gated through `pg-online-schema-change`-style tooling; or run in maintenance window | devops | Migration-duration metric |
| R-116 | New `AuthService` deployed without coordinated frontend rollout, causing tokens the client can't refresh | Low × High | Coordinated release with frontend; feature flag `AUTH_NEW_LOGIN` only flips after both backend + frontend bundles deployed | release manager | Deployment-checklist gate |
| R-117 | **Total login-path latency (bcrypt + DB + Redis) exceeds 200ms p95 at cost-11** (Fix #9) | Low × High | Async audit-log write via outbox pattern; Redis pipeline for lockout-check + token-SET. Contingency: accept cost-10 with documented rationale + plan hardware upgrade for cost-12 in v1.1 | auth-team | M1 D-103 full-path benchmark; production APM histogram |

---

## 6. Dependencies & Sequencing

<!-- Source: Base (original, modified) — Change #1 (Redis moved to M1 entry) -->
### 6.1 External dependencies

| Dependency | Needed by | Risk if missing | Mitigation |
|---|---|---|---|
| PostgreSQL 15+ provisioned | M1 entry | Cannot start | DBaaS provisioned in week -1 |
| Redis 7+ provisioned (AOF persistence + cluster mode in prod) | **M1 entry (moved from M2 per Change #1)** | M1 lockout has no backing store; M1 blocked | Provision in Week 0/1 via CC5 INF-2 |
| SendGrid account + API key | M3 entry | Cannot send reset emails | Procurement complete before week 4; verify SPF/DKIM/DMARC |
| Feature-flag service (existing) | M5 entry | Cannot stage rollout | Verify availability in week 8 (CC5 INF-6) |
| Secret manager for RSA keypair | M2 entry | Cannot sign tokens | Generate keypair in week 2 |
| Frontend routing framework | M4 entry | Cannot mount auth pages | Already present per PRD Dependencies |
| API gateway with rate limiting | M1 entry (Layer 2 of defense-in-depth) | Cannot enforce 10/min limits | Existing gateway; configure in CC5 INF-3 |
| Email-from domain DNS access | M3 entry | Email deliverability tanks | Coordinate with IT in week 3 (CC5 INF-3) |

<!-- Source: Base (original, modified) — Change #1 ASCII diagram update -->
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
CC5:     [=========================================]
Redis:   [=========================================] (provisioned Week 1 for M1 lockout per Change #1)
Postgres:[=========================================] (provisioned Week 1)
```

### 6.3 Parallelization opportunities

- **Schema vs hasher (M1):** `migrations/0001_user_profile.sql` and `PasswordHasher` can be built in parallel; they meet at `AuthService.register()`.
- **JWT vs TokenManager (M2):** `JwtService` (sign/verify) is testable in isolation before `TokenManager` exists.
- **Frontend mocking (M4):** `LoginPage` and `RegisterPage` can be built against a mocked backend during M2 if the OpenAPI spec is stable; only `AuthProvider` silent refresh truly blocks on M2.
- **Email template + SendGrid wiring (M3):** Template design (D-304) can start in M2 once strings are agreed.
- **Runbook drafting (CC4 / M5):** D-503 can start during M3 with placeholders that fill in as M4 lands.
- **Lockout + register/login (M1):** D-108 LoginAttemptTracker and D-104/D-105 can be built in parallel; they meet at the `/auth/login` handler.

### 6.4 Blocking-dependency summary

- M1 ⟶ requires Redis 7+ (CC5 INF-2) by Week 1.
- M2 ⟶ blocked by M1.
- M3 ⟶ blocked by M2 (needs `TokenManager` to invalidate sessions on reset).
- M4 ⟶ blocked by M2 (needs `/auth/refresh` for silent refresh) and M3 (needs reset endpoints for `/forgot-password` and `/reset-password` pages).
- M5 ⟶ blocked by M1, M2, M3, M4, CC1 security checkpoint, CC2 dashboards green, CC5 production provisioning complete.

---

<!-- Source: Base (original) -->
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
| Password hash time | <500ms (chosen cost) | Per-build | `PasswordHasher` micro-bench | auth-team | **Hard** — gate in M1 |
| Email delivery rate (including dead-letter retries) | >99% | Rolling 7 days | SendGrid webhook + `pending_emails` reconciliation | auth-team | **Hard** during M3 |
| DAU authenticated users | >1000 | 30 days post-GA | `AuthToken` issuance count | product | Soft |

### 7.3 Per-FR acceptance criteria summary

| FR | Acceptance criteria summary | Test class |
|---|---|---|
| FR-AUTH.1 / FR-AUTH-001 | Valid creds → 200 + `AuthToken`; invalid → 401 generic; non-existent email → 401 (no enumeration, dummy bcrypt + identical-shape audit); 5 fails / 15 min → 423; 20 attempts/email-hash/hour → 429 | Unit + integration + QA-6 |
| FR-AUTH.2 / FR-AUTH-002 | Valid → 201 + `UserProfile`; duplicate email → 409; weak password → 400 with field-level codes; bcrypt cost per M1 benchmark | Unit + integration |
| FR-AUTH.3 / FR-AUTH-003 | Login returns 15-min access + 7-day refresh; `/auth/refresh` rotates; expired or revoked refresh → 401; 10-token FIFO cap per user with evicted-guard | Unit + integration + clock-skew test |
| FR-AUTH.4 / FR-AUTH-004 | `/auth/me` returns full `UserProfile`; expired/invalid token → 401 | Unit + integration |
| FR-AUTH.5 / FR-AUTH-005 | Reset email queued within 5s (cron-delivered after first-attempt failures); 1-hour TTL; single-use; password change invalidates **all** sessions | Integration + E2E + QA-7 chaos |

### 7.4 Definition of Done (rolled up from TDD §24.1)

- All five FRs implemented with passing tests.
- Coverage ≥80% for `AuthService`, `TokenManager`, `JwtService`, `PasswordHasher`.
- Integration tests for all 4 (+ 2 reset + 1 admin audit query) endpoints green.
- Security review signed off (including audit immutability per Fix #7).
- Performance testing confirms 200ms p95 at 500 concurrent users.
- Runbook published, on-call trained.

---

<!-- Source: Base (original, modified) — Fix #3 boundary, Fix #9 latency budget, Change #6 11-device row -->
## 8. Boundary Conditions & Edge Cases

Roadmap-level handling beyond the FR-level table.

| Condition | Handling | Test |
|---|---|---|
| Empty email / password fields | 400 with `code: VALIDATION_REQUIRED_FIELD` | Unit on `AuthService` |
| Email > 254 chars (RFC 5321) | 400 with `code: VALIDATION_EMAIL_TOO_LONG` | Unit |
| displayName outside 2-100 chars | 400 with `code: VALIDATION_DISPLAYNAME_LENGTH` | Unit |
| Unicode in displayName (emoji, RTL) | Accepted; normalized via NFC | Unit |
| Concurrent registration with same email | Second request gets 409 via DB unique constraint; race window <50ms | Integration |
| **User logs in from 11th device while 10 sessions active** (Change #6) | Oldest session's refresh token evicted (FIFO). Evicted-token reuse emits `token_evicted_reuse` WARNING but does NOT revoke family. All remaining 10 sessions stay valid. | Integration (Fix #4) |
| Refresh token used after rotation (non-evicted) | Reuse detection → revoke family, 401 | Unit on `TokenManager` |
| Reset token used twice | First use updates password; second use → 410 Gone | Integration |
| Reset confirm with password identical to current | Allowed (no enumeration); user warned in UI | Unit |
| Lockout reaches 5 then user requests reset | Reset succeeds (different code path); admin notified of unlock-via-reset | Integration |
| User changes password while logged in on Device B | Device B's next API call → 401 → forced re-login | Integration + E2E |
| Server clock drifts +10s | Tokens still accepted within ±5s tolerance; -5s → -10s drift causes premature expiry; alert on NTP drift | Chaos test |
| Redis cold start | `TokenManager` retries 3 times with exponential backoff; falls through to 503. Family-lineage metadata reloaded from AOF (Fix #1) | Chaos test (QA-7) |
| PostgreSQL primary failover | Connection-pool retry; <500ms blip; if >5s, gateway returns 503 | Chaos test |
| Single-element `roles` array (the default `["user"]`) | Treated normally; no special casing needed | Unit |
| Zero refresh tokens for user (never logged in) | `/auth/refresh` returns 401 with `code: AUTH_NO_REFRESH_TOKEN` | Unit |
| Maximum-size payload at `/auth/register` | Body-size limit 10 KB at gateway; 413 Payload Too Large | Integration |
| Slow client (delayed body) | 10-second request-body timeout at gateway | Integration |
| **Login-failure audit-write timing** (Fix #3 / INV-006) | Both unknown-email and wrong-password paths execute identical-shape audit INSERT (1 row, same column set, NULL vs UUID `user_id` only difference). Unknown-email path computes dummy bcrypt to match ~300ms timing. | QA-6 with audit writes enabled |
| **Login-path latency budget breakdown** (Fix #9 / INV-026) | bcrypt target ≤120ms (cost-11), DB writes ≤40ms, Redis ≤20ms, network overhead ≤20ms. Total ≤200ms. | M1 D-103 full-path benchmark |
| **SendGrid first-attempt failure** (Fix #6) | 5-second timeout; payload written to `pending_emails`; client still receives 200 within 5.2s ceiling; cron sweep delivers within 5 min | QA-7 chaos test |
| **Redis FLUSHALL + AOF reload mid-session** (Fix #1) | Family-lineage metadata reloaded from AOF; reuse-detection still revokes family on pre-restart token | QA-7 chaos test |

---

<!-- Source: Base (original, modified) — Change #6 (evicted state), Fix #1 (family-linkage storage), Fix #5 (login transaction) -->
## 9. State Management, Guard Conditions, Concurrency

The TDD marks §9 "Not applicable — backend service," but several real state machines exist and the roadmap calls them out so M2/M3 implementations stay honest.

### 9.1 Refresh-token state machine

States: `issued` → `rotated` (replaced) | `revoked` (manual) | `expired` (TTL hit) | `reused` (security event) | **`evicted`** (FIFO eviction at 11th token per Change #6).

Guards:

- `rotated` is reachable only from `issued`.
- `reused` is reachable from `rotated` or `revoked` (used after replacement).
- `reused` transition revokes the entire token **family** (all descendants of the original issuance) — UNLESS the family metadata has `evicted=true` (Fix #4 guard), in which case only the specific token is rejected (401) and a `token_evicted_reuse` WARNING audit event is emitted.
- `evicted` is reachable from `issued` when an 11th token is issued for the same user; the evicted token's family entry sets `evicted=true`.
- Evicted tokens with `evicted=true` metadata do NOT trigger family revocation on reuse (per Fix #4).

**Family-linkage storage (Fix #1 / INV-001):**

- Each refresh-token record in Redis stores `family_id` (UUID, set at first issuance), `parent_id` (hash of previous token, NULL for root), `user_id`, `issued_at`, `status`.
- A Redis Sorted Set per family `family:{family_id}:members` (score = issued_at, value = token hash) enables efficient family-wide revoke.
- Redis AOF persistence enabled with `appendfsync everysec` ensures family metadata survives cold-start.
- Family metadata Sorted Set TTL = max refresh-token TTL + 24h buffer (8 days).

Concurrency:

- Two simultaneous `/auth/refresh` calls with the same token: serialize via Redis `SET NX` lock keyed on the token hash. Loser of the race gets 401.

### 9.2 Account-lockout state machine

States: `unlocked` ⟶ `locked` (5 failures in window) ⟶ `unlocked` (after window expires or admin/reset action).

Guard: Successful login during the window does NOT reset the failure counter (security choice per M1 D-108 / R-112).

Stored in Redis (keyed by account+IP) per Change #1 (moved from M3 to M1).

### 9.3 Password-reset token state machine

States: `pending` ⟶ `consumed` (single use) | `expired` (1-hour TTL).

Guard: Issuing a new reset request while a `pending` token exists invalidates the prior token (prevents two valid links in two emails).

### 9.4 Audit-log write ordering

Concurrency-safe: each event written as an independent INSERT with `occurred_at = clock_timestamp()`. No cross-row coordination required. Partitioned by month for the 12-month retention.

**Immutability (Fix #7 / INV-022):** The `audit_log` table has a DB trigger preventing UPDATE/DELETE. Inserts are performed via the `audit_writer` role (INSERT-only grant).

<!-- Source: Base (original, modified) — Fix #5 adds login transaction scope -->
### 9.5 Database transactions

- `AuthService.register()`: single transaction inserting `UserProfile` + `audit_log(registration)` + `consent` row. Rolls back atomically on failure.

- **`AuthService.login()` transaction scope (Fix #5 / INV-017):**

  ```
  1. bcrypt verify (~chosen-cost ms, read-only, no transaction needed)
     [Unknown-email path: compute dummy bcrypt to match timing per Fix #3]
  2. BEGIN TRANSACTION:
     a. Validate credentials (read user_profile) — skipped on unknown-email path
     b. UPDATE user_profile SET lastLoginAt = NOW() WHERE id = user_id (skipped on failure paths)
     c. INSERT INTO audit_log (user_id, event_type, ip, user_agent, outcome, email_hash, occurred_at)
        - login_success: user_id=<UUID>, email_hash=SHA256(email)
        - login_failure (wrong password): user_id=<UUID>, email_hash=SHA256(email)
        - login_failure (unknown email): user_id=NULL, email_hash=SHA256(email)
  3. COMMIT TRANSACTION
  4. (success path only) TokenManager.issueTokens() — Redis SET (outside DB transaction)
  5. Return AuthToken (or 401/423) to client
  ```

  **Rollback semantics:** If step 4 (Redis SET) fails, the DB transaction (steps 2-3) is already committed. Audit row shows `login_success`, `lastLoginAt` is updated, but no refresh token is issued. Client receives a 503 error. Client retries → second login attempt succeeds normally, producing a second `login_success` audit row. This is acceptable because (a) the audit trail is accurate (the user did authenticate), (b) the second attempt is idempotent from the user's perspective, (c) `lastLoginAt` converges to the correct value on retry.

- `AuthService.confirmPasswordReset()`: single transaction updating `password_hash` + revoking all refresh-token families for the user + writing `audit_log(password_reset_completed)`.

---

<!-- Source: Base (original) -->
## 10. Out of Scope

Items explicitly excluded from this roadmap and the rationale.

| Item | Rationale | Where it goes |
|---|---|---|
| OAuth / OIDC / social login | PRD non-goal; TDD NG-001; deferred to v1.1+ | Post-GA Considerations §18.5 |
| MFA (TOTP, SMS, WebAuthn) | PRD non-goal; TDD NG-002; v1.2 | Post-GA Considerations §18.5 |
| RBAC enforcement | PRD non-goal; TDD NG-003; `roles` field present but not enforced | Separate authorization PRD |
| API-key authentication for service-to-service | TDD OQ-001 — deferred to v1.1 | Post-GA Considerations §18.5 |
| "Remember me" extended sessions | Refresh token already gives 7-day persistence; resolves PRD OQ #4 | Not needed |
| Admin UI for account management (Jordan persona) | v1.0 ships admin audit query (M3 D-309); rich UI is separate | Admin-tools roadmap |
| Self-service email change | Not in PRD; introduce in v1.1 with verification flow | v1.1 |
| Self-service displayName change | Not in PRD; small addition; punt to v1.1 | v1.1 |
| Account deletion / GDPR right-to-erasure UI | Promoted to v1.1 (hard GDPR deadline) per Change #4 / Post-GA Considerations | v1.1 |
| Hardware-bound or device-trust signals | Out of scope; v2.0+ | v2.0+ |
| Federated SSO (SAML) | Out of scope; v2.0+ | v2.0+ |
| Bot detection / advanced fraud | Defense-in-depth Layers 1-3 in v1.0; CAPTCHA Layer 4 contingency; richer detection later | v1.1+ |

---

<!-- Source: Base (original, modified) — Change #2 (A-11 greenfield), Change #6 (OQ-2 update), Fix #6 (OQ-1 update), Change #9 (OQ-R7) -->
## 11. Open Questions & Assumptions

### 11.1 PRD/TDD open questions and recommended resolutions

| ID | Question | Source | Recommended resolution | Decision owner |
|---|---|---|---|---|
| OQ-1 | Reset emails sync or async? | PRD OQ #1 | **Single-attempt + dead-letter (Fix #6):** 5-second SendGrid timeout; failed sends queued to `pending_emails` for cron retry sweep. Keeps `/auth/reset-request` within budget. Bull/BullMQ deferred to v1.1. (D-308 ADR) | engineering |
| OQ-2 | Max refresh tokens per user? | PRD OQ #2 | **10 active refresh tokens per user. Oldest evicted on new issuance (FIFO).** Covers typical multi-device usage. Eviction-guard per Fix #4 prevents false-positive family revocation. (Change #6) | product |
| OQ-3 | Lockout policy after N failures? | PRD OQ #3 | 5 fails / 15-min sliding window, per-account+IP (TDD §13). Implemented in M1 D-108 per Change #1. | security |
| OQ-4 | Support "remember me"? | PRD OQ #4 | No — 7-day refresh window covers the use case | product |
| OQ-5 | API-key auth for service-to-service? | TDD OQ-001 | Deferred to v1.1 (Post-GA Considerations §18.5) | test-lead |
| OQ-6 | Max `UserProfile.roles` array length? | TDD OQ-002 | Cap at 16 for v1.0 (defensive); revisit with RBAC design | auth-team |

### 11.2 Roadmap-level open questions (newly raised)

| ID | Question | Why it matters | Decision owner | Target |
|---|---|---|---|---|
| OQ-R1 | Audit-log retention: TDD §7.2 says 90 days, PRD legal/compliance row says 12 months. Which wins? | SOC2 evidence horizon | security + compliance | Before M1 D-102 commit |
| OQ-R2 | Refresh-token storage in browser: HttpOnly cookie vs in-memory + sessionStorage hybrid? | XSS surface area (R-101) | security + frontend | Before M4 D-403 |
| OQ-R3 | Where does GDPR right-to-erasure flow live for v1.0? | Hard legal obligation | legal + product | Before GA |
| OQ-R4 | Do we ship a token-revocation endpoint (`POST /auth/logout`) or is client-side discard enough? | M4 logout flow + R-101 | auth-team | Before M4 D-403 |
| OQ-R5 | Do we expose `/auth/me` PATCH for displayName updates in v1.0? | PRD says profile view only; some users will ask | product | Before M2 D-204 |
| OQ-R6 | What is the legacy auth-endpoint deprecation timeline post-GA? | TDD §19.1 Phase 3 mentions deprecation but no date (also see Change #2 — greenfield: legacy endpoints may not exist) | platform-team | Before M5 sub-phase 5C |
| **OQ-R7** | **Does the +1 week hidden buffer push GA to 2026-06-16, or does the team compress Week 9-10 CC activities?** (Change #9 / INV-010) | Schedule integrity vs GA date commitment | Product Manager | Before M5 sub-phase 5A entry |

### 11.3 Assumptions

- **A-1:** SendGrid (or an interchangeable transactional-email provider) is available before M3 starts; if not, M3 slips one sprint.
- **A-2:** PostgreSQL 15+ and Redis 7+ are managed services; no DBA work falls on auth-team.
- **A-3:** API gateway with rate-limiting capability already exists; auth-team configures policies, doesn't build the gateway.
- **A-4:** Frontend routing framework supports protected routes and context providers (React Router or equivalent).
- **A-5:** Secrets manager (Vault / AWS Secrets Manager / equivalent) is in place for RSA keypair distribution.
- **A-6:** Observability stack (Prometheus + Grafana + tracing) is in place; auth-team plugs in metrics, doesn't stand up the stack.
- **A-7:** CI pipeline supports `testcontainers` for ephemeral PostgreSQL + Redis (per TDD §15.3).
- **A-8:** Production CPU class is ≥ comparable to the build agent used for the bcrypt benchmark.
- **A-9:** Personalization features that depend on auth (Q2-Q3 2026) will not begin integration until GA is signaled.
- **A-10:** "auth-team provides 24/7 on-call rotation during first 2 weeks post-GA" (TDD §25.2) is honored.
- **A-11 (Change #2 / greenfield):** There is no existing legacy auth system requiring migration. The PRD describes a greenfield implementation. Rollback strategy must account for this — there is no "flip back to legacy" path. Rollback uses gateway maintenance page (503).

---

<!-- Source: Base (original, modified) — Change #2 (step 2 greenfield correction) -->
## 12. Rollback & Failure-Mode Strategies

### 12.1 Rollback triggers (from TDD §19.4)

- p95 latency > 1000ms for > 5 minutes.
- Error rate > 5% for > 2 minutes.
- Redis connection failures > 10 per minute.
- Any `UserProfile` data loss / corruption.

### 12.2 Rollback procedure (from TDD §19.3, expanded — Change #2 greenfield-correct)

1. Page on-call; declare incident in #auth-incidents.
2. **Flip `AUTH_NEW_LOGIN` OFF. Because this is a greenfield deployment (PRD: "the platform currently operates without any user identity system"), there is no legacy auth to fall back to. Instead, display a maintenance page (503) at the gateway for all `/auth/*` routes until the issue is resolved.** (Per Change #2 + Assumption A-11.)
3. Smoke-test the gateway maintenance page behavior.
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
| SendGrid down | Webhook errors + `pending_emails` row count rises | Single-attempt timeout → `pending_emails` queue → cron retry sweep (Fix #6) | Investigate SendGrid status; manual support workflow if prolonged |
| RSA private key inaccessible | Token signing fails 100% | Service returns 503 | Re-mount secret; emergency rotation if compromised |
| Migration deadlocks `user_profile` | Migration runner timeout | Migration aborts; service stays on old schema | Reschedule in maintenance window |
| Lockout-table runaway growth | Redis memory alert | None — sliding window self-cleans | Investigate brute-force campaign; block at WAF |
| Audit-log write latency | Span duration alert | None — write async via outbox | Investigate DB pressure |
| Redis AOF corruption / cold-start | AOF reload failure alert | Family-lineage metadata rebuilt from audit_log (degraded mode) | Restore Redis from AOF snapshot |
| `pending_emails` backlog >100 | Row-count alert | None | Investigate SendGrid health; rate-limit reset requests if abuse |

---

<!-- Source: Base (original, modified) — Change #5 (Jordan persona D-309) -->
## 13. Personas Coverage Check

The PRD names three personas; this roadmap verifies each is served by v1.0.

| Persona | Need served | Where in roadmap |
|---|---|---|
| Alex (end user) | Register, login, persistent session, reset password, view profile | M1, M2, M3, M4 |
| Jordan (admin) | Audit logs and lockout signals | M1 (audit-log schema D-102), M3 (lockout events D-306, **admin audit query D-309**), CC2 (dashboards) |
| Sam (API consumer) | Programmatic login + refresh with clear error codes | M1 (`/auth/login`), M2 (`/auth/refresh`), DOC-5 (consumer docs), Appendix D (endpoint summary) |

Sam's "stable auth contracts" need is reinforced by the OpenAPI spec maintained throughout M1-M3 (D-106, D-207, CC4), Appendix D (API endpoint summary), and the API governance section in TDD §8.4 (URL-prefix versioning, breaking changes require new major version).

---

<!-- Source: Base (original, modified) — Change #3 (10-row staffing table), Change #7 (pentest row) -->
## 14. Cost & Resource Plan

Anchored on TDD §26 ($450/month production infra) and TDD §25.3 (capacity).

| Resource | M1-M4 (staging) | M5 onward (prod) | Scaling trigger |
|---|---|---|---|
| `AuthService` pods | 1 replica | 3 replicas baseline | HPA → 10 at CPU >70% |
| PostgreSQL | Shared staging instance | Managed instance, 100-conn pool | Bump to 200-conn at wait >50ms |
| Redis | Single-node staging (AOF enabled) | Cluster mode, 1 GB, AOF persistence | Scale to 2 GB at >70% utilization |
| SendGrid | Free tier (dev) | Paid plan with bounce handling | Volume-based plan upgrade |
| **External penetration test (one-time)** | N/A | **$5,000-$15,000** | **N/A — budgeted per engagement** (Change #7 / SEC-5) |
| Monthly run-rate | ~$50 (staging) | ~$450 + scales $50 per 10K users | Linear in user count |

<!-- Source: V2 (sonnet), Section 10.1 "Team Composition" — merged per Change #3, adapted to V1's 11-week cadence -->
### 14.1 Staffing Plan

| Role | Allocation | Weeks Active | Primary Responsibility |
|---|---|---|---|
| Backend Engineer 1 | 100% | Week 1-8 (M1-M4) | `AuthService` + `PasswordHasher` |
| Backend Engineer 2 | 100% | Week 3-8 (M2-M4) | `TokenManager` + `JwtService` |
| Backend Engineer 3 | 100% | Week 5-6 (M3) | Password reset + audit logging integration |
| Frontend Engineer 1 | 100% | Week 7-8 (M4) | `LoginPage` + `RegisterPage` |
| Frontend Engineer 2 | 100% | Week 7-8 (M4) | `AuthProvider` + `ProfilePage` + reset pages |
| QA Engineer | 50% / 100% | 50% Week 1-4; 100% Week 5-11 | Test scaffolding, contract tests, E2E, load tests |
| Security Engineer | 25% | Week 1-2 (policy review) + Week 9-11 (security sign-off) | NIST/SOC2/GDPR review + pentest coordination |
| DevOps Engineer | 25% | Week 1 (CI/CD), Week 3-4 (K8s), Week 9 (prod) | CC5 INF-1 through INF-7 |
| Product Manager | 10% | Week 1-11 | Stakeholder updates + OQ-R1/OQ-R7 decisions |
| SRE (0.5 FTE) | 50% | Week 9-13 (M5 + stabilization) | On-call rotation, runbook validation |

---

<!-- Source: Base (original) -->
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

<!-- Source: Base (original, modified) — added family lineage / evicted / dead-letter terms -->
## 16. Glossary (roadmap additions beyond TDD §28)

| Term | Definition |
|---|---|
| Token family | The lineage of refresh tokens descending from a single login event; reuse detection revokes the entire family (subject to evicted-token guard per Fix #4). |
| Family lineage | `family_id` + `parent_id` pair stored per refresh token in Redis Hash + Sorted Set; AOF-persisted (Fix #1 / INV-001). |
| Evicted token | A refresh token displaced via 10-token FIFO cap (Change #6); marked `evicted=true` in family metadata; reuse does NOT revoke family (Fix #4). |
| Sliding window (lockout) | Counter resets only when the window's worth of time has fully elapsed since the earliest failure, not on each request. |
| Sub-phase | A named step within a milestone, used here for M5 (5A internal alpha / 5B 10% beta / 5C 100% GA). |
| Soft / hard gate | A "hard gate" blocks the GA decision; a "soft gate" is observed and triaged but does not block. |
| Deliverable ID (D-NNN) | Concrete artifact owned by a milestone (e.g., D-103 = `PasswordHasher` module). |
| Dead-letter (email) | `pending_emails` PostgreSQL row holding an email payload that failed first-attempt delivery; processed by cron retry sweep (Fix #6). |
| Defense-in-depth (brute force) | Four-layer stack from R-102: per-account lockout, gateway IP rate limit, per-account global rate limit, CAPTCHA contingency (Fix #8). |
| Audit immutability | DB trigger + `audit_writer` INSERT-only role + integrity verification script preventing audit_log tampering (Fix #7). |

---

<!-- Source: Base (original, modified) — references to D-108, D-109, D-110, D-209, D-309, D-310 added -->
## 17. Appendix A — Milestone-to-Requirement Traceability

| Requirement | Covered by |
|---|---|
| PRD FR-AUTH.1 / TDD FR-AUTH-001 | M1 D-105/D-108/D-109; M2 D-201/D-202; CC3 QA-6 |
| PRD FR-AUTH.2 / TDD FR-AUTH-002 | M1 D-103/D-104 |
| PRD FR-AUTH.3 / TDD FR-AUTH-003 | M2 D-201/D-202/D-203/D-209 |
| PRD FR-AUTH.4 / TDD FR-AUTH-004 | M2 D-204; M4 D-404 |
| PRD FR-AUTH.5 / TDD FR-AUTH-005 | M3 D-301/D-302/D-303/D-304/D-310 |
| PRD NFR-AUTH.1 / TDD NFR-PERF-001 + NFR-PERF-002 | M1 D-103 benchmark; M5 D-506 (k6 load test); CC2 OBS-3; R-117 |
| PRD NFR-AUTH.2 / TDD NFR-REL-001 | M5 D-501 (HPA + replicas); CC2 OBS-4 |
| PRD NFR-AUTH.3 / TDD NFR-SEC-001 | M1 D-103; CC1 SEC-1 |
| TDD NFR-SEC-002 | M2 D-201/D-205; CC1 SEC-6 |
| PRD legal: GDPR consent | M4 D-402; CC1 SEC-2 |
| PRD legal: SOC2 audit logging + immutability | M1 D-102/D-110; CC1 SEC-3; OQ-R1 resolution |
| PRD legal: NIST password storage | M1 D-103; CC1 SEC-1 |
| PRD legal: data minimization | M4 D-402; CC1 SEC-2 |
| PRD R-002 brute-force defense-in-depth | M1 D-108/D-109 + Gateway INF-3; R-102 |
| TDD §13 account lockout | M1 D-108 (moved from M3 per Change #1) |
| TDD §14 observability | CC2 OBS-1 through OBS-8 |
| TDD §19 rollout | M5 sub-phases 5A/5B/5C |
| TDD §24 release criteria | M5 D-507/D-510; §7.4 DoD |
| TDD §25 operational readiness | M5 D-503/D-509; CC2 OBS-5; CC5 INF-1 through INF-7 |
| Jordan persona (admin) | M3 D-309 (admin audit query) |
| Sam persona (API consumer) | DOC-5; Appendix D |

---

<!-- Source: Base (original) -->
## 18. Appendix B — Calendar (one-page view)

```
Week 1  (Mar 30 - Apr  5): M1 kickoff, schema + hasher + lockout + Redis online
Week 2  (Apr  6 - Apr 13): M1 close — register + login + defense-in-depth + audit immutability
Week 3  (Apr 14 - Apr 20): M2 kickoff — JwtService + TokenManager + family lineage
Week 4  (Apr 21 - Apr 27): M2 close — /auth/refresh + /auth/me + 10-token cap
Week 5  (Apr 28 - May  4): M3 kickoff — reset endpoints + email single-attempt + admin audit query
Week 6  (May  5 - May 11): M3 close — pending_emails cron + audit events
Week 7  (May 12 - May 18): M4 kickoff — LoginPage + RegisterPage
Week 8  (May 19 - May 25): M4 close — AuthProvider silent refresh + E2E
Week 9  (May 26 - Jun  1): M5 5A — Internal Alpha in staging
Week 10 (Jun  2 - Jun  8): M5 5B — 10% Beta in production
Week 11 (Jun  9         ): M5 5C — 100% GA (or 2026-06-16 if OQ-R7 buffer applied)
Week 12-13 (Jun 10 - 23) : Stabilization, flag removal, post-mortem readiness
```

---

<!-- Source: V2 (sonnet), Appendix B "Feature Flag Lifecycle" — merged per Change #8 -->
## 18.1 Appendix C — Feature Flag Lifecycle

Operationalizes TDD §19.2. Both flags default to OFF; they are enabled per-phase during rollout and removed only after sustained production stability.

| Flag | Created | Enabled | Disabled (rollback only) | Removed |
|---|---|---|---|---|
| `AUTH_NEW_LOGIN` | Week 8 (M5 prep, INF-6) | Week 9 (5A Internal Alpha) | On rollback trigger per §12.2 | Week 13 (post-stabilization) |
| `AUTH_TOKEN_REFRESH` | Week 8 (M5 prep, INF-6) | Week 10 (5B 10% Beta cohort) | On rollback trigger per §12.2 | Week 15 (post-stabilization + 2 weeks) |

Both flags are tracked in the production feature-flag service per CC5 INF-6. Flag removal targets resolve the "removal targets recorded" note in §10 Out of Scope.

---

<!-- Source: V2 (sonnet), Appendix C "API Endpoint Summary" — merged per Change #11; adapted to V1's milestone+week cadence -->
## 18.2 Appendix D — API Endpoint Summary

Production URLs use `/v1/auth/*` prefix per TDD §8.4 (URL-prefix versioning).

| Endpoint | Method | Auth Required | Rate Limit (Gateway) | Milestone | Week |
|---|---|---|---|---|---|
| `/v1/auth/register` | POST | No | 5 req/min/IP | M1 | Week 1-2 |
| `/v1/auth/login` | POST | No | 10 req/min/IP (Layer 2) + 20/email-hash/hour (Layer 3) | M1 | Week 1-2 |
| `/v1/auth/refresh` | POST | No (uses refresh token) | 30 req/min/IP | M2 | Week 3-4 |
| `/v1/auth/me` | GET | Yes (Bearer access token) | 60 req/min/user | M2 | Week 3-4 |
| `/v1/auth/reset-request` | POST | No | 5 req/min/IP | M3 | Week 5-6 |
| `/v1/auth/reset-confirm` | POST | No (uses reset token) | 10 req/min/IP | M3 | Week 5-6 |
| `/v1/admin/audit-logs` | GET | Yes (admin role) | 60 req/min/user | M3 | Week 5-6 |
| `/v1/auth/logout` | POST | Yes (Bearer) | 30 req/min/user | Conditional — pending OQ-R4 | M4 (if approved) |

---

<!-- Source: V2 (sonnet), Section 13 "Post-GA Considerations" — merged per Change #4; quarter labels marked as targets -->
## 18.5 Post-GA Considerations

Roadmap continuity beyond v1.0. **Quarter labels are targets, not firm commitments.**

### v1.1 Planning (target: Q3 2026)

- MFA (TOTP, SMS, WebAuthn) — TDD NG-002.
- API-key authentication for service-to-service — TDD OQ-001.
- "Remember me" extended sessions (only if telemetry shows demand; current 7-day refresh likely covers).
- Email verification flow (verify ownership of email at registration).
- Password change while logged in (`POST /auth/password-change`).
- Account self-service unlock (post-lockout, email-verified flow).
- **GDPR right-to-erasure flow** (promoted from "Post-v1.0" to named v1.1 item per INV-025 + Change #4 — hard legal obligation).
- Bull/BullMQ Redis-backed job queue for email (upgrade from v1.0 single-attempt + dead-letter, per Fix #6).

### v2.0 Planning (target: Q4 2026)

- OAuth2 / OIDC (NG-001) + social login (Google, Apple, GitHub).
- RBAC enforcement (separate Authorization PRD).
- Admin dashboard UI (beyond the v1.0 audit-log query endpoint).
- Federated SSO (SAML) — TDD scope §10 deferred.

### Ongoing Maintenance

- **Quarterly RS256 key rotation** (per CC1 SEC-6 and TDD §13 schedule).
- **Annual bcrypt cost factor review** — re-benchmark on then-current production hardware; consider upgrade if CPU class advances.
- **SOC2 audit log retention verification** — quarterly integrity script (Fix #7); annual external audit prep.
- **Dependency updates** — monthly Renovate/Dependabot review for `bcryptjs`, `jsonwebtoken`, etc.
- **Capacity review at 10K DAU** — re-evaluate Redis sizing (currently 1 GB sufficient per OBS-6); re-evaluate K8s HPA ceiling (currently 10 pods).

---

<!-- Source: Base (original, modified) — updated to reflect merged content; note residual MEDIUM invariants -->
## 19. Closing Note

This roadmap honors the TDD's existing milestone dates and decomposes them into actionable deliverables, cross-cutting tracks, and a risk register that maps cleanly onto the named architectural components (`AuthService`, `TokenManager`, `JwtService`, `PasswordHasher`, `AuthProvider`). Where the source documents conflicted (90-day vs 12-month audit retention; sync vs async reset email; refresh-token storage strategy), the roadmap flags the conflict as an open question with a recommended resolution rather than silently choosing.

The merge adversarial pipeline (sc:adversarial) integrated 9 HIGH-severity invariant fixes (INV-001, 005, 006, 013, 017, 021, 022, 023, 026), 12 V2 strength incorporations, and resolved 5 base-weakness concessions. Critical fixes include:

- **Lockout in M1 (D-108)** instead of M3, closing PRD R-002 mitigation gap. Co-shipped with per-account global rate limit (D-109) as Layer 3 of the defense-in-depth stack.
- **bcrypt cost factor determined by M1 benchmark** rather than committed at cost-12 — addresses NFR-PERF-001 sum-of-latencies risk (R-104, R-117).
- **Refresh-token family lineage in Redis with AOF persistence** (Fix #1) so reuse detection survives Redis cold-start.
- **10-token FIFO cap with evicted-guard** (Change #6 + Fix #4) prevents false-positive multi-device logout.
- **SendGrid single-attempt + dead-letter** (Fix #6) resolves the 200ms p95 vs retry-guarantee contradiction.
- **Audit-log immutability via DB trigger + `audit_writer` role** (Fix #7) elevates SOC2 readiness.
- **Greenfield-correct rollback** (Change #2) replaces the infeasible "flip back to legacy" step with gateway 503 maintenance page.

The single biggest delivery risk remains the bcrypt-cost-vs-200ms-p95 budget (R-104 + R-117). M1 D-103 makes this measurable on day 1, and the explicit cost-11 default (with cost-12 only on benchmark proof) is the pre-approved escape hatch documented in advance.

The single biggest scope risk is the audit-log retention conflict (OQ-R1): SOC2 evidence horizon must be settled in week 1 because the storage cost and partition strategy depend on it. The new audit-immutability controls (D-110) further strengthen the SOC2 evidence story.

**Schedule risk:** Change #9 introduces a 1-week hidden buffer between Beta and GA. Per OQ-R7 (Section 11.2), the Product Manager must decide before M5 sub-phase 5A entry whether to compress CC2/CC4 activities or slip GA to 2026-06-16.

**Residual MEDIUM UNADDRESSED invariants (10):** INV-002, INV-003, INV-007, INV-008, INV-010, INV-015, INV-019, INV-020, INV-024, INV-025. Per the adversarial protocol, these are tracked in the invariant probe but do not block convergence. Notable items:

- INV-008 is partially addressed by Fix #3's dummy bcrypt on the unknown-email path.
- INV-010 is operationalized as OQ-R7 (the buffer decision).
- INV-025 is operationalized by Change #4's promotion of GDPR right-to-erasure to a named v1.1 item.

These should be re-evaluated during M1 architecture review and again at the M5 go/no-go.
