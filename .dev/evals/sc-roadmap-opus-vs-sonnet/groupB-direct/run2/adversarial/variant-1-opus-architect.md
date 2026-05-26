---
id: "AUTH-ROADMAP-001"
title: "User Authentication Service — Implementation Roadmap (v1.0)"
source: ".dev/eval-roadmap/inputs/merged-prd-tdd-user-auth.md (AUTH-PRD-001 + AUTH-001-TDD)"
generated_by: "system-architect (variant-1-opus-architect, groupB-direct/run2/adversarial)"
generated_at: "2026-05-22"
version: "1.0"
target_release: "v1.0 / Q2 2026"
target_ga_date: "2026-06-09"
soc2_audit_deadline: "Q3 2026"
---

# User Authentication Service — Implementation Roadmap

## Executive Summary

This roadmap sequences delivery of the User Authentication Service (registration, login, logout, JWT session persistence, profile retrieval, password reset) to hit v1.0 GA on **2026-06-09** (TDD §23.1) and meet the **SOC2 Type II audit window in Q3 2026** (PRD Business Context). Five milestones move from foundation (DB schema + audit log infrastructure) → core `AuthService` (login/register) → token lifecycle (`TokenManager`/`JwtService`) → password reset + frontend integration → phased rollout (10% beta → 100% GA).

Success is measured against PRD/TDD targets: registration conversion **>60%**, login **p95 <200ms** at 500 concurrent users (NFR-PERF-001/002), service **99.9% uptime** (NFR-REL-001), failed login rate **<5%**, password reset completion **>80%**, and zero P0/P1 security findings before GA. SOC2 audit-log emission (user ID, timestamp, IP, outcome; 12-month retention for auth events, 90-day for the audit table per TDD §7.2) is built into M1 — not bolted on at the end — because every endpoint shipped without logging is a compliance defect that must be retrofitted under audit pressure.

Critical sequencing: PostgreSQL/Redis schema and audit-log scaffolding land first (M1) so every subsequent endpoint emits compliant events from its first commit; token lifecycle (M2) lands before the frontend (M4) so `AuthProvider` can be built against a stable contract; password reset (M3) is gated on email delivery + reset-token storage being production-ready, not just functional.

---

## Milestones

### M1 — Foundation: Data Layer, Audit Log, and Core `AuthService` (Register + Login)

**Target completion:** 2026-04-14 (TDD §23.1)
**Estimated duration:** 3 weeks (Sprint 1 + half of Sprint 2)

**Objective:** Stand up the persistence layer, SOC2-grade audit logging, and the `AuthService` register/login surface with bcrypt password hashing so that the platform has a working — but not yet token-managed — identity primitive.

**Scope (in):**

- PostgreSQL 15 schema for `UserProfile` (id UUID v4 PK, email UNIQUE+indexed lowercase-normalized, displayName 2–100 chars, createdAt, updatedAt, lastLoginAt nullable, roles default `["user"]`) — TDD §7.1
- Audit log table in PostgreSQL with **90-day retention** (TDD §7.2) capturing user_id, event_type, timestamp, IP address, outcome — PRD Legal §Audit logging, SOC2 Type II
- `AuthService` orchestrator skeleton + `PasswordHasher` (bcrypt cost factor **12**, NFR-SEC-001)
- `POST /auth/register` (FR-AUTH-002 / FR-AUTH.2): unique email enforcement, password policy (≥8 chars, uppercase, number per TDD §5.1), 201 with `UserProfile`, 409 on duplicate, 400 on weak password
- `POST /auth/login` (FR-AUTH-001 / FR-AUTH.1): credential validation, generic 401 (no user enumeration per PRD §Error Handling, TDD §12), **account lockout after 5 failed attempts in 15-minute window** (FR-AUTH-001 AC #4)
- Rate limiting at API Gateway: login **10 req/min/IP**, register **5 req/min/IP** (TDD §8.1)
- Structured logging emitter (`auth_login_total`, `auth_registration_total` counters per TDD §14) wired into Prometheus

**Scope (out):**

- JWT issuance — tokens deferred to M2; M1 login responds with `userId` + ephemeral session reference only (or returns 202 behind `AUTH_NEW_LOGIN=OFF` feature flag if dual-stack with legacy is required)
- Refresh tokens, `/auth/refresh`, `/auth/me` — M2
- Password reset — M3
- Frontend pages — M4

**Deliverables:**

- **D1.1** PostgreSQL migration scripts: `users` table + indexes, `auth_audit_log` table with 90-day retention policy (partitioned by month for purge efficiency)
- **D1.2** `AuthService` class with `register()` and `login()` methods; `PasswordHasher` with bcrypt cost 12 (benchmarked ≤500ms per NFR-SEC-001 / §17)
- **D1.3** REST endpoints `POST /v1/auth/register` and `POST /v1/auth/login` with error contract per TDD §8.3 (`{error: {code, message, status}}`)
- **D1.4** Account lockout state machine: counter+window per email, lock event written to audit log, 423 Locked response (TDD §8.2 login error responses)
- **D1.5** Audit log emitter middleware that fires on every `/auth/*` request — success and failure both logged with user_id (or null for unknown email), IP, outcome
- **D1.6** Unit test suite (Jest) covering `PasswordHasher` hash/verify, `AuthService.register/login`, lockout counter — target **≥80% coverage on M1 surface** (TDD §15.1, §24.1)
- **D1.7** Integration tests via Supertest + testcontainers: register persists to PostgreSQL, login enforces lockout, audit rows appear (TDD §15.1, §15.2)
- **D1.8** Runbook stub for `AuthService` down + PostgreSQL unreachable (TDD §25.1 scenario 1)

**Acceptance criteria:**

- Registering a new user persists a `UserProfile` row with bcrypt-hashed password (verified by `bcrypt.compare` test, never plaintext in DB or logs — NFR-AUTH.3, NFR-SEC-001)
- Duplicate-email registration returns **409**; weak password returns **400** with field-level error code (TDD §8.2)
- 5 failed logins in 15 minutes against the same email returns **423 Locked**; 6th attempt is rejected without invoking `PasswordHasher.verify` (defense against timing oracle)
- Audit log contains exactly one row per `/auth/*` request, with non-null timestamp + IP + outcome; SOC2 spot-check passes for 100 synthetic events
- Unit test coverage on `AuthService` + `PasswordHasher` ≥ 80% (TDD §24.1)
- p95 of `/auth/register` and `/auth/login` ≤ 200ms under 100-RPS local load (provisional toward NFR-PERF-001)
- Rate limit returns **429** at 11th login attempt in a minute from a single IP (TDD §8.1)

**Dependencies:**

- PostgreSQL 15+ provisioned (PRD Assumptions, TDD §18)
- API Gateway with configurable per-IP rate limits available
- Bcryptjs / equivalent library vetted by security review

**Estimated duration:** 3 weeks

**Risks + mitigations (M1-specific):**

| Risk | Mitigation |
|---|---|
| Audit-log table grows unbounded under attack-scale traffic | Partition by month from day 1; cron-based drop of partitions older than 90 days (TDD §7.2). Lock-event rate ceiling alarmed at 1k/min. |
| Bcrypt cost 12 exceeds 200ms p95 budget on shared CPU pods | Benchmark in CI; if hash time pushes login p95 over budget, isolate `PasswordHasher` to a worker pool or accept M1-only 300ms p95 with M5 tuning ticket. Per TDD §17 the 300ms hash fits the 200ms p95 only with connection-pool optimizations — verify both. |
| Lockout state stored in-process makes horizontal scale unreliable | Back lockout counters with Redis from M1 even though Redis is "M2 territory" — counter accuracy is a SOC2 control, not a performance optimization |
| User-enumeration leakage via response timing | Ensure 401 response time for unknown email matches valid-email-wrong-password (run `PasswordHasher.verify` against a constant dummy hash on miss) |

---

### M2 — Token Lifecycle: `TokenManager`, `JwtService`, Refresh + `/auth/me`

**Target completion:** 2026-04-28 (TDD §23.1)
**Estimated duration:** 2 weeks (Sprint 2 second half + Sprint 3)

**Objective:** Replace M1's interim session reference with the production JWT access/refresh model so sessions persist across page refreshes (FR-AUTH-003 / FR-AUTH.3) and API consumers (Sam persona) can refresh tokens without user interaction.

**Scope (in):**

- `JwtService` signing JWT access tokens with **RS256, 2048-bit RSA keys** (NFR-SEC-002), **15-minute TTL** (FR-AUTH-003)
- `TokenManager` issuing/storing opaque refresh tokens in **Redis 7** with **7-day TTL** (FR-AUTH-003, TDD §7.2)
- Refresh tokens stored as **hashed values** in Redis to prevent token theft from compromising sessions (TDD §13)
- `POST /v1/auth/refresh`: validates refresh token, **revokes old token, issues new pair** (rotation — TDD §8.2 `/auth/refresh`)
- `GET /v1/auth/me` (FR-AUTH-004 / FR-AUTH.4): Bearer-token-protected, returns full `UserProfile` (id, email, displayName, createdAt, updatedAt, lastLoginAt, roles)
- M1's login endpoint upgraded to return full `AuthToken` (`accessToken`, `refreshToken`, `expiresIn: 900`, `tokenType: "Bearer"`)
- Clock-skew tolerance of **5 seconds** in `JwtService` verification (TDD §12)
- Key-rotation runbook + quarterly rotation schedule (TDD §13)
- New Prometheus metrics: `auth_login_duration_seconds` histogram, `auth_token_refresh_total` counter (TDD §14)
- Alert rules: login failure rate > 20% over 5 min, p95 latency > 500ms, `TokenManager` Redis connection failures (TDD §14)

**Scope (out):**

- Password reset (M3)
- Frontend `AuthProvider` (M4) — though contract is frozen here for parallel frontend work
- HttpOnly-cookie refresh-token transport — design decided in M2 but UI wiring lands in M4

**Deliverables:**

- **D2.1** `JwtService` with RS256 sign/verify, key loading from secret store, 5-second skew tolerance, unit-tested against forged/expired/wrong-key tokens
- **D2.2** `TokenManager.issueTokens()`, `refresh()`, `revoke()` operating against Redis 7
- **D2.3** Redis key schema: `refresh:<hash(token)>` → `{userId, issuedAt, deviceFingerprint?}` with 7-day TTL
- **D2.4** Endpoints `POST /v1/auth/refresh`, `GET /v1/auth/me` with full TDD §8.2 contracts
- **D2.5** Refresh-token rotation: each `/auth/refresh` invalidates the presented token; replay attack returns 401 (FR-AUTH-003 AC #4)
- **D2.6** Redis-unavailability behavior: refresh requests rejected (not served stale tokens) per TDD §12; circuit breaker + alert
- **D2.7** Integration tests: expired refresh token → 401, revoked refresh token → 401, full `/login → /me → /refresh → /me` flow against testcontainers Postgres+Redis
- **D2.8** Load test (k6) confirming **p95 login < 200ms at 500 concurrent users** (NFR-PERF-001/002), **p95 refresh < 100ms** (TDD §4.1)
- **D2.9** Frozen OpenAPI contract published to frontend team to unblock M4 in parallel

**Acceptance criteria:**

- Login response includes valid JWT (decodes to user id + roles), refreshToken, `expiresIn: 900`, `tokenType: "Bearer"` (TDD §7.1 `AuthToken`)
- `GET /auth/me` with valid Bearer returns full `UserProfile`; with expired/missing/invalid token returns 401 (FR-AUTH-004 ACs)
- `/auth/refresh` with a previously-rotated token returns 401 (rotation enforced)
- Access token modified by one byte fails `JwtService.verify` (signature integrity)
- Clock-skew test: token issued at T+3s validated at T passes; at T+6s fails
- Redis killed mid-test: `/auth/refresh` returns 401/503 (never 200 with stale tokens)
- k6 load test: 500 concurrent login RPS, p95 < 200ms (NFR-PERF-001/002), error rate < 0.1%
- All four endpoints from M1+M2 emit audit log rows with token-event types (`token.issued`, `token.refreshed`, `token.revoked`)

**Dependencies:**

- M1 (PostgreSQL `users`, audit log, `AuthService` skeleton)
- Redis 7+ provisioned with persistence (AOF) and replica
- Secret store (HashiCorp Vault or equivalent) holding RSA keypair

**Estimated duration:** 2 weeks

**Risks + mitigations (M2-specific):**

| Risk | Mitigation |
|---|---|
| Refresh-token replay if rotation is non-atomic | Use Redis `MULTI/EXEC` (or `SET NX` + delete) to make revoke-and-issue atomic; integration test for race |
| RSA private key leak | Mount as in-memory tmpfs, never write to disk; key-access audit log; quarterly rotation runbook (TDD §13) |
| Refresh-token storm at deploy (mass re-login) overwhelms Redis | Pre-warm Redis cluster; HPA on `AuthService` (TDD §25.3: 3→10 replicas at 70% CPU); rate-limit refresh at 30 req/min/user (TDD §8.1) |
| Stateless JWT means revoke can't be instant for access token | Document the 15-minute residual exposure window; for high-severity revoke, add denylist of user IDs in Redis checked at `/me` (deferred to v1.1 if not needed for SOC2) |

---

### M3 — Password Reset Flow + Email Integration

**Target completion:** 2026-05-12 (TDD §23.1)
**Estimated duration:** 2 weeks (Sprint 4)

**Objective:** Deliver self-service password recovery (FR-AUTH-005 / FR-AUTH.5) — request + confirm endpoints, SendGrid integration, single-use 1-hour reset tokens, full session invalidation on password change.

**Scope (in):**

- `POST /v1/auth/reset-request`: accepts email, **always returns 200** regardless of registration status (anti-enumeration per PRD §Error Handling, TDD §12)
- `POST /v1/auth/reset-confirm`: validates reset token, applies password policy, hashes new password via `PasswordHasher`, **invalidates all refresh tokens for the user** (FR-AUTH.5 AC, TDD §13)
- Reset-token storage: opaque token, **1-hour TTL** (FR-AUTH-005 AC #3, TDD §13), single-use (used-token store or status field)
- Email delivery via SendGrid (PRD Dependencies, TDD §18): reset email **sent within 60 seconds** of request (PRD User Journey §Password Reset)
- Async email send via job queue so reset-request endpoint stays under 200ms even under email-provider slowness
- New metric `auth_password_reset_total{outcome=requested|completed|expired|invalid}`
- Audit log events for reset-requested, reset-completed, reset-token-expired, reset-token-reused

**Scope (out):**

- Frontend password-reset pages (M4)
- MFA-gated reset (non-goal NG-002, deferred to v1.2)

**Deliverables:**

- **D3.1** Reset-token data model: hashed token, user_id FK, expires_at, used_at nullable
- **D3.2** `POST /v1/auth/reset-request` and `POST /v1/auth/reset-confirm` endpoints
- **D3.3** SendGrid integration with templated reset email, retry on transient failure, dead-letter on permanent failure
- **D3.4** Job queue (e.g., BullMQ on Redis) for async email send
- **D3.5** Session-invalidation logic: on successful reset-confirm, delete all refresh tokens matching `userId` in Redis (TDD §13 — "new password invalidates all sessions" per PRD FR-AUTH.5)
- **D3.6** Unit tests: token expiry, single-use enforcement, all-sessions-invalidation
- **D3.7** Integration test: end-to-end request → email captured by mock provider → confirm → old refresh tokens rejected
- **D3.8** SendGrid delivery monitoring + alert at <95% delivery rate over 1 hour (PRD Risk §Email delivery)
- **D3.9** Runbook entry for "reset emails not delivering" with SendGrid status check + manual override path

**Acceptance criteria:**

- Reset request for registered email returns 200 within 200ms; email arrives within 60 seconds (PRD User Journey)
- Reset request for unregistered email returns identical 200 response (timing within ±20ms of registered case to prevent timing-oracle enumeration)
- Reset link works exactly once: second use returns 400 with `AUTH_RESET_TOKEN_USED` (TDD §8.3 error format)
- Reset link older than 1 hour returns 400 with `AUTH_RESET_TOKEN_EXPIRED`
- After successful reset-confirm, all existing refresh tokens for that user return 401 on `/auth/refresh` (FR-AUTH.5 AC)
- Audit log shows full reset chain: requested → email-sent → confirmed (or expired/reused)
- Load test: 100 RPS reset requests with email delivery still queued does not push login p95 above budget

**Dependencies:**

- M1 (`UserProfile`, `PasswordHasher`, audit log)
- M2 (`TokenManager` — needs `revokeAllForUser()` method)
- SendGrid account, API key, verified sender domain (PRD Dependencies)
- Redis queue capacity (small additive to M2 capacity plan)

**Estimated duration:** 2 weeks

**Risks + mitigations (M3-specific):**

| Risk | Mitigation |
|---|---|
| SendGrid outage blocks password reset entirely | Dead-letter queue + alert; documented fallback support channel (PRD Risk Analysis); reset-token validity not tied to email delivery — user can retry request once SendGrid recovers |
| Reset endpoint becomes spam vector (mass enumeration probe or email-bomb) | Per-email rate limit (1 reset request / 60 sec / email) at gateway; per-IP rate limit (3/min); CAPTCHA on UI in M4 if abuse observed |
| Timing-side-channel leaks "is this email registered?" | Constant-time path: always enqueue email job (drop in worker if unregistered) so request-side latency is identical |
| Concurrent reset requests for the same user create token races | Invalidate prior unconsumed reset tokens on new request; or accept N concurrent tokens but mark all consumed on first use |

---

### M4 — Frontend Integration: `LoginPage`, `RegisterPage`, `AuthProvider`, ProfilePage

**Target completion:** 2026-05-26 (TDD §23.1)
**Estimated duration:** 2 weeks (Sprint 5)

**Objective:** Wire user-facing React components against the frozen M2 contract, deliver Alex's end-to-end signup → login → profile → reset journey (PRD Customer Journey Map), and ship behind `AUTH_NEW_LOGIN` feature flag for staged rollout.

**Scope (in):**

- `LoginPage` route `/login`: email/password form, inline validation, generic error message (no enumeration), calls `POST /v1/auth/login`
- `RegisterPage` route `/register`: email + password + displayName, client-side password-strength meter (mirrors server policy), calls `POST /v1/auth/register`
- ProfilePage route `/profile`: protected, displays `UserProfile` from `GET /v1/auth/me` (PRD User Journey §Profile)
- `AuthProvider` React context: stores accessToken **in memory only** (not localStorage — XSS mitigation per R-001 / TDD §13), refresh token via **HttpOnly cookie**, silent refresh on accessToken expiry, intercepts 401 to retry once after refresh then redirect to `/login`
- Forgot-password UI: request page + confirm page consuming M3 endpoints
- Logout: clears in-memory accessToken, clears refresh cookie, server-side refresh-token revoke
- Inline validation for password policy with helpful messaging (PRD §UX Requirements)
- Page-load budget: `/login` renders in < 1 second (PRD User Journey §Returning User Login)

**Scope (out):**

- Social login, MFA, "remember me" (PRD Open Questions OQ-4 deferred)
- Admin tools for Jordan persona (admin event-log viewer — M5 or v1.1 depending on capacity; SOC2 audit access can be DB-direct for v1.0)

**Deliverables:**

- **D4.1** `LoginPage`, `RegisterPage`, ProfilePage React components with TDD §10.2 prop contracts
- **D4.2** `AuthProvider` with in-memory accessToken + HttpOnly-cookie refreshToken + silent-refresh interceptor
- **D4.3** Forgot-password request/confirm pages
- **D4.4** Component hierarchy per TDD §10.3 (`App → AuthProvider → {PublicRoutes, ProtectedRoutes}`)
- **D4.5** Playwright E2E tests (TDD §15.1): register → login → view profile → logout; forgot password → email link → reset → login with new password; refresh-token silent rotation across 16-minute timespan (verifies 15-min TTL boundary)
- **D4.6** Frontend telemetry: registration funnel events for >60% conversion measurement (PRD Success Metrics)
- **D4.7** Feature flag `AUTH_NEW_LOGIN` wiring (default OFF in prod)
- **D4.8** Accessibility pass on auth pages (deferred to frontend TDD per TDD §16, but at minimum: keyboard-navigable forms, labeled inputs, error-message `aria-live`)

**Acceptance criteria:**

- Playwright suite covers all PRD §User Journey flows; all green
- Login p95 measured from browser-Submit to dashboard-render < 1 second (PRD User Journey "login completes in < 200ms p95" for API + render budget)
- Silent refresh occurs without user-visible interruption when accessToken expires mid-session
- Browser tab close clears in-memory token (R-001 mitigation)
- Logout immediately renders the user logged-out on a second open tab within 1 refresh cycle
- 401 from `/auth/me` triggers exactly one refresh attempt; second 401 redirects to `/login` with no infinite loop (R-002-adjacent: TDD §25.1 runbook scenario "AuthProvider enters redirect loop")
- Registration funnel telemetry feeds the >60% conversion metric (PRD Success Metrics)

**Dependencies:**

- M2 frozen API contract (D2.9)
- M3 password-reset endpoints
- Frontend routing framework (PRD Dependencies)
- Backend deployed to staging with feature flags wired

**Estimated duration:** 2 weeks

**Risks + mitigations (M4-specific):**

| Risk | Mitigation |
|---|---|
| Token storage choice (memory vs localStorage) causes auto-logout on tab refresh | Use refresh-cookie path: page reload → silent refresh → restore session; covered by Playwright reload-mid-session test |
| 401 + refresh + 401 redirect loop (per TDD §25.1) | Hard-cap one refresh attempt per request; circuit-breaker disables refresh for 30s after 3 consecutive failures |
| CSRF on cookie-based refresh | Refresh endpoint requires same-origin + custom header (`X-CSRF-Token` double-submit or SameSite=Strict cookie); add CSRF test to Playwright |
| Inline password-strength meter drifts from server policy | Single shared policy module (JSON schema or pure-function); contract test that hits server `/register` with N test cases drives both UI and server |

---

### M5 — Phased Rollout, Hardening, and GA

**Target completion:** 2026-06-09 (TDD §23.1 — GA)
**Estimated duration:** 4 weeks (Sprint 6 + 2 weeks rollout overlap)

**Objective:** Execute the three-phase rollout (Internal Alpha → 10% Beta → 100% GA) per TDD §19.1, complete security/penetration review, validate SOC2 audit-log fitness, and remove feature flags.

**Scope (in):**

- **Phase 1: Internal Alpha** (Week 1) — all endpoints deployed to staging, auth-team + QA execute full FR-AUTH-001..005 manual test plan, **zero P0/P1 bugs** exit criterion (TDD §19.1)
- **Phase 2: Beta @ 10%** (Weeks 2–3) — `AUTH_NEW_LOGIN=ON` for 10% of traffic, monitor latency, error rates, Redis usage; exit criteria: **p95 latency < 200ms, error rate < 0.1%, no TokenManager Redis connection failures** (TDD §19.1)
- **Phase 3: GA @ 100%** (Week 4) — remove `AUTH_NEW_LOGIN`, enable `AUTH_TOKEN_REFRESH`, deprecate legacy auth; exit criteria: **99.9% uptime over first 7 days** (TDD §19.1, §23.2)
- Security review + penetration test (PRD Risk Analysis): bcrypt cost verified, RS256 key-rotation runbook signed off, OWASP Authentication Cheat Sheet checklist passed (TDD §27.2)
- SOC2 audit-log validation: 12-month retention policy enforced (PRD Legal), spot-check on synthetic incident playback
- Production observability: Grafana dashboards verified for `auth_login_total`, `auth_login_duration_seconds`, `auth_token_refresh_total`, `auth_registration_total` (TDD §24.2)
- Rollback drill in staging (TDD §19.3)
- On-call rotation: **24/7 auth-team coverage for first 2 weeks post-GA**, P1 ack within 15 minutes (TDD §25.2)
- Capacity validation: HPA 3→10 pods on CPU > 70%, PostgreSQL pool 100→200 if wait > 50ms, Redis 1GB → 2GB if > 70% utilized (TDD §25.3)

**Scope (out):**

- MFA, OAuth, RBAC enforcement (non-goals, v1.1+)
- Admin event-log UI (deferred unless SOC2 auditor requires UI access — DB-direct view acceptable for initial audit)

**Deliverables:**

- **D5.1** Staging deployment + Alpha sign-off document (auth-team + QA)
- **D5.2** Penetration test report with zero unresolved Critical/High findings before Phase 3
- **D5.3** Beta 10% rollout dashboard + 2-week observation log
- **D5.4** GA rollout executed, feature flags removed within 2 weeks post-GA (TDD §19.2 removal targets)
- **D5.5** SOC2 audit-log evidence package: 30-day sample of audit events with full required fields (user ID, timestamp, IP, outcome — PRD Legal)
- **D5.6** Rollback drill executed in staging with documented timing (target: < 5 min from flag flip to legacy traffic)
- **D5.7** Final runbooks for both TDD §25.1 scenarios (AuthService down, token refresh failures), reviewed by on-call team
- **D5.8** Post-GA metrics report at 30 days vs PRD success targets

**Acceptance criteria:**

- All five FR-AUTH-001..005 pass production smoke tests post-flag-flip
- Beta phase: zero rollback triggers fired (no p95 > 1000ms for 5+ min, no error rate > 5% for 2+ min, no Redis failures > 10/min, no `UserProfile` corruption per TDD §19.4)
- 99.9% uptime measured over the first 7 GA days (TDD §19.1 Phase 3 success criterion)
- Penetration test sign-off: no unresolved P0/P1 (PRD Risk §Security breach)
- SOC2 evidence pack accepted by compliance lead
- Both feature flags (`AUTH_NEW_LOGIN`, `AUTH_TOKEN_REFRESH`) removed per TDD §19.2 removal targets
- 30-day post-GA metrics: registration conversion > 60%, login p95 < 200ms, failed login rate < 5%, reset completion > 80% (PRD Success Metrics)

**Dependencies:**

- M1–M4 deliverables all green
- Staging environment fidelity with production (TDD §15.3)
- Security review window booked (lead time ≥ 2 weeks)
- Compliance lead availability for SOC2 evidence walkthrough

**Estimated duration:** 4 weeks

**Risks + mitigations (M5-specific):**

| Risk | Mitigation |
|---|---|
| Pen-test surfaces a P0 that blocks Phase 3 | Security review starts in M4 (parallel) not M5; budget 1 sprint slack between pen-test and GA |
| 10% Beta traffic insufficient to detect rare bug before 100% | Hold Beta minimum 2 weeks per TDD §19.1; expand to 25% for 48 hours before 100% if no signals |
| Flag-removal causes regression because dead-code paths weren't exercised | Pre-removal: run E2E suite with flags forced ON and forced OFF; remove flags only after both paths green for 1 week |
| SOC2 auditor rejects audit-log schema late in Q3 | Schedule mock-audit in M5 Week 1 with internal compliance using sampled events; iterate schema in M5 not under audit pressure |

---

## Cross-Cutting Concerns

### Security (woven through M1–M5; explicit ownership: sec-reviewer + auth-team)

- **OWASP Authentication Cheat Sheet checklist** referenced in TDD §27.2 — track item-by-item from M1, sign off in M5
- **TLS 1.3 enforced** on all endpoints (TDD §13)
- **No user enumeration** — generic 401 on login (FR-AUTH-001 AC #3), identical 200 on reset-request regardless of registration (PRD Error Handling, TDD §12)
- **Sensitive-field redaction** in logs — password, accessToken, refreshToken, reset tokens never in application logs (NFR-AUTH.3, TDD §13)
- **Key rotation** — RS256 keys rotated quarterly (TDD §13), runbook delivered M2, first rotation drill in M5
- **CORS** — restricted to known frontend origins from M2 onward (TDD §13)
- **Brute-force defense layered**: API Gateway rate limit + bcrypt cost 12 + 5-attempt lockout (R-002 mitigation, TDD §13)

### Observability (M1 baseline, expanded each milestone)

- **Structured logs** for every auth event (TDD §14): JSON, schema-versioned, correlation ID per request
- **Prometheus metrics**: `auth_login_total`, `auth_login_duration_seconds` (histogram), `auth_token_refresh_total`, `auth_registration_total` (TDD §14, §24.2)
- **OpenTelemetry distributed tracing** through `AuthService → PasswordHasher → TokenManager → JwtService` (TDD §14)
- **Alerts** (TDD §14): login failure rate > 20% over 5 min, p95 > 500ms, `TokenManager` Redis failures
- **Funnel telemetry**: registration landing → submit → confirmed (PRD Success Metrics), reset requested → completed (>80% target)

### Testing (per TDD §15)

- **Test pyramid**: Unit 80% / Integration 15% / E2E 5%
- **Tools**: Jest + ts-jest (unit), Supertest + testcontainers (integration), Playwright (E2E)
- **Coverage gate**: ≥80% on `AuthService`, `TokenManager`, `JwtService`, `PasswordHasher` (TDD §24.1) — enforced in CI from M1
- **Performance test** (k6): 500 concurrent logins, p95 < 200ms (NFR-PERF-002) — executed at M2 close and M5 entry
- **Security test**: signature-tamper, expired-token, replay, timing-oracle for unknown email, lockout-bypass attempts — added M1→M3 incrementally

### Compliance (SOC2, GDPR, NIST)

- **SOC2 Type II audit logging**: enabled from M1 (not bolted on) — user_id, event_type, timestamp, IP, outcome, **12-month retention for auth events** per PRD Legal (note: TDD §7.2 says 90-day on the audit table — reconcile in M5 evidence-pack review; default to PRD's 12-month for SOC2-relevant events)
- **NIST SP 800-63B password storage**: bcrypt cost 12, one-way, never plaintext (PRD Legal, NFR-AUTH.3)
- **GDPR data minimization**: only email, hashed password, displayName collected (PRD Legal)
- **GDPR consent**: registration form captures consent with timestamp (PRD Legal) — wired in M4 (`RegisterPage`) with backend `consents` row written by `AuthService.register()` in M1
- **Right-to-erasure**: out of v1.0 scope but `UserProfile` schema designed to support soft-delete + cascade (note: confirm via Open Question)

### Performance Budgets (TDD §17, §4.1)

| Operation | Budget |
|---|---|
| `/auth/login` p95 | < 200ms (NFR-PERF-001, NFR-AUTH.1) |
| `/auth/register` p95 | < 200ms |
| `/auth/refresh` p95 | < 100ms (TDD §4.1) |
| `/auth/me` p95 | < 100ms (implied by <200ms aggregate, mostly token verify + DB read) |
| Bcrypt hash time | ~300ms, budgeted ≤500ms (NFR-SEC-001, TDD §17) |
| JWT sign/verify | < 5ms (TDD §17) |
| Redis op | < 10ms (TDD §17) |
| Concurrent login capacity | 500 RPS (NFR-PERF-002) |

---

## Risk Register

| ID | Risk | Probability | Impact | Mitigation | Contingency | Owner |
|---|---|---|---|---|---|---|
| R-001 | Token theft via XSS allows session hijacking (TDD R-001) | Medium | High | Access token in memory only; refresh token in HttpOnly+SameSite cookie; 15-min access TTL; `AuthProvider` clears on tab close | `TokenManager.revokeAllForUser()`; force password reset for affected users | sec-reviewer |
| R-002 | Brute-force attacks on login (TDD R-002) | High | Medium | Rate limit 10 req/min/IP at gateway; 5-attempt lockout in 15-min window; bcrypt cost 12 raises offline-crack cost | WAF IP block; CAPTCHA on `LoginPage` after 3 failures | sec-reviewer |
| R-003 | Data loss during migration from legacy auth (TDD R-003) | Low | High | Parallel-run M1+M2 with legacy; idempotent upserts; full DB backup pre-phase | Rollback to legacy + restore `UserProfile` from backup | platform-team |
| R-004 | SOC2 audit fails due to incomplete audit logging (PRD Risk) | Medium | High | Audit table + emitter delivered in M1, not retrofitted; mock audit in M5 Week 1; 12-month retention enforced | 1-sprint buffer in M5 for schema iteration; compliance lead reviews schema in M2 not M5 | compliance-lead |
| R-005 | Email delivery (SendGrid) failures block password reset (PRD Risk) | Low | Medium | Delivery monitoring + alert at < 95% over 1 hour; retry queue with dead-letter; fallback support channel documented | Failover to secondary SES-style provider (provisioned but cold in v1.0); manual support-driven reset via runbook | auth-team |
| R-006 | Bcrypt cost 12 plus DB round-trip pushes `/auth/login` over 200ms p95 (NFR-PERF-001) | Medium | Medium | Connection pooling tuned in M1; bcrypt cost benchmarked in CI on prod-equivalent CPU; consider isolating hash to worker pool if needed | Reduce cost to 11 with security sign-off, or scale `AuthService` horizontally; trade-off documented | auth-team |
| R-007 | Refresh-token replay during non-atomic rotation | Low | High | Atomic Redis `MULTI/EXEC` on revoke-then-issue; integration test for concurrent refresh race | If replay detected, invalidate full token family for that user; alert security | auth-team |
| R-008 | Lockout state in process memory miscounts under multi-pod scale | Medium | Medium | Back lockout counters with Redis from M1 (not deferred to M2) | If Redis down, fail-closed: reject login with 503 rather than allow unbounded attempts | auth-team |
| R-009 | Frontend `AuthProvider` redirect loop on refresh failure (TDD §25.1) | Medium | Medium | One-refresh-attempt cap per request; circuit breaker after 3 consecutive failures; Playwright test for loop scenario | Hot-fix to disable refresh interceptor via remote config flag; users re-login | frontend-team |
| R-010 | Pen-test discovers high-severity finding < 2 weeks before GA | Medium | High | Pen-test scheduled in M4 (parallel with frontend), not in M5; bug-bash in M5 Week 1; 1-week slack between pen-test and Phase 3 | Delay GA by 1 sprint; SOC2 deadline is Q3 not Q2, so room exists | sec-reviewer |

---

## Definition of Done

### Per-milestone DoD

- All listed deliverables (D*.X) merged to main and deployed to staging
- Unit + integration tests for the milestone's surface area pass in CI
- Test coverage on touched code ≥ 80% (TDD §24.1)
- Audit log emits expected events for every new endpoint (SOC2 control)
- Runbook entries added or updated for new failure modes
- Performance budgets met (see Performance Budgets table) in load test or load-test-projection
- Security review checkpoint signed off by sec-reviewer (lightweight at M1/M2, full at M5)
- Acceptance criteria for the milestone all green

### Overall v1.0 DoD (TDD §24.1)

- [ ] All FR-AUTH-001 through FR-AUTH-005 implemented and verified with passing tests
- [ ] Unit test coverage for `AuthService`, `TokenManager`, `JwtService`, `PasswordHasher` exceeds 80%
- [ ] Integration tests for all four (now six with `/reset-request`, `/reset-confirm`) API endpoints pass against real PostgreSQL + Redis
- [ ] Security review complete: bcrypt cost 12 verified, RS256 key rotation documented, OWASP checklist passed
- [ ] Performance testing confirms < 200ms p95 under 500 concurrent users
- [ ] Both feature flags removed per TDD §19.2 timing
- [ ] Rollback drill executed successfully in staging
- [ ] SOC2 audit-log evidence pack accepted by compliance
- [ ] On-call runbooks published and reviewed (TDD §25.1)
- [ ] 99.9% uptime over first 7 GA days (TDD §19.1)
- [ ] 30-day post-GA metrics meet PRD Success Metrics targets
- [ ] Go/no-go sign-off from test-lead and eng-manager (TDD §24.2)

---

## Open Questions and Assumptions

### Carried forward from PRD/TDD (must resolve before milestone listed)

| ID | Question | Source | Owner | Needed by |
|---|---|---|---|---|
| OQ-1 | Password reset email sync vs async | PRD Open Q1 | Engineering | M3 start — **proposed resolution: async via job queue (D3.4)** so reset-request endpoint stays under 200ms |
| OQ-2 | Maximum refresh tokens per user across devices | PRD Open Q2 | Product | M2 start — **proposed default: unlimited within 7-day TTL window; revisit if Redis memory exceeds capacity plan** (TDD §25.3) |
| OQ-3 | Account lockout policy (N attempts, duration) | PRD Open Q3 | Security | M1 start — **proposed resolution from TDD FR-AUTH-001 AC #4: 5 attempts in 15-minute window, lock until manual unlock or 1-hour auto-unlock** (confirm auto-unlock duration) |
| OQ-4 | "Remember me" to extend session duration | PRD Open Q4 | Product | M2 start — **proposed v1.0 decision: defer; 7-day refresh TTL covers most usage; revisit post-GA** |
| OQ-5 | Should `AuthService` support API key auth for service-to-service? | TDD OQ-001 | test-lead | M2 — **deferred to v1.1 per TDD note** |
| OQ-6 | Max `UserProfile.roles` array length | TDD OQ-002 | auth-team | M1 — **proposed: 16 entries, enforced as DB CHECK constraint** |
| OQ-7 | Reset-table retention conflict (PRD says 12-month for auth logs; TDD §7.2 says 90-day on `auth_audit_log`) | PRD vs TDD | compliance-lead | M5 SOC2 evidence pack — **proposed: split tables, 90-day operational log + 12-month SOC2-relevant subset** |

### Working assumptions (validate at milestone entry)

- A1 — Email delivery infra (SendGrid) provisioned before M3 start (PRD Assumption)
- A2 — PostgreSQL 15 + Redis 7 available before M1 (PRD Assumption, TDD §18)
- A3 — Frontend routing framework supports protected routes + redirect interceptors (PRD Assumption)
- A4 — Security policy SEC-POLICY-001 finalized before M2 (PRD Dependencies)
- A5 — Legacy auth system (if any) exposes a shim that `AUTH_NEW_LOGIN` flag can switch against; if no legacy exists, Phase 1 alpha can be skipped and Beta runs against new-only traffic
- A6 — Frontend TDD (FE-AUTH-001-TDD) covers accessibility for `LoginPage`/`RegisterPage` (TDD §16) — coordinate ownership before M4
- A7 — Staging environment has production-fidelity Redis + Postgres (TDD §15.3) for load and rollback drills

---

## Sequencing Rationale (architect's note)

The dependency chain is **data → service → tokens → reset → frontend → rollout**, not a parallelizable matrix. Key non-obvious sequencing decisions:

1. **Audit log lands in M1, not M5.** SOC2 controls are not features; retrofitting audit emission across six endpoints under audit pressure is the textbook failure mode. Cost in M1 is ~2 days; cost in M5 would be a rollout slip.
2. **Lockout counter on Redis from M1, even though "Redis is M2."** Counter accuracy is a SOC2 control. In-process counters break on horizontal scale. Provision Redis at M1 even if only `TokenManager` "owns" it in M2.
3. **M2 freezes the API contract before M4 starts.** Frontend (M4) and backend (M3) can run in parallel after M2 if the OpenAPI spec is locked at M2 close (D2.9). This recovers 1 sprint from a naive serial plan.
4. **Pen-test in M4 (parallel), not M5.** A late security finding that blocks GA is the single highest-impact schedule risk (R-010). Booking the pen-test in M4 with the frontend gives 2 weeks of cure time before GA.
5. **Constant-time anti-enumeration in M1 and M3.** Both endpoints (login on unknown email, reset on unregistered email) must execute the same code paths regardless of registration, or the timing side-channel re-introduces the enumeration vulnerability PRD §UX explicitly prohibits.
