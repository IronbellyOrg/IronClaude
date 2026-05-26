---
id: "AUTH-ROADMAP-MERGED-001"
title: "User Authentication Service — Implementation Roadmap (Merged)"
source: ".dev/eval-roadmap/inputs/merged-prd-tdd-user-auth.md"
generated_by: "sc:adversarial (V2 base + V1 strengths + invariant probe fixes)"
generated_at: "2026-05-22"
version: "1.0"
target_release: "v1.0 / Q2 2026"
soc2_audit_deadline: "Q3 2026"
---

<!--
Provenance:
- Base structure: variant-2-sonnet-architect.md (6-milestone scaffold M1-M6)
- Strengths merged from: variant-1-opus-architect.md (constant-time mechanisms, atomic-UPDATE, OQ-7 retention conflict, key-rotation runbook, sequencing rationale)
- Invariant fixes applied: invariant-probe.md INV-001, INV-002, INV-004, INV-005, INV-007, INV-009, INV-011, INV-012, INV-013, INV-014
- Refactor plan: refactor-plan.md (18 planned changes, auto-approved)
-->

# User Authentication Service — Implementation Roadmap

---

## Executive Summary

<!-- Source: Base (V2 Sonnet) -->
This roadmap sequences the delivery of the User Authentication Service (v1.0) across six milestones spanning approximately 12 weeks, targeting general availability by early June 2026 in alignment with the Q2 2026 release window and the Q3 2026 SOC2 Type II audit deadline. The service covers user registration, login, logout, session persistence via JWT access/refresh tokens, profile retrieval, and self-service password reset. Success is measured against concrete targets drawn from the PRD and TDD: registration conversion above 60%, login p95 latency below 200ms, session duration above 30 minutes, failed login rate below 5%, and password reset completion above 80% (PRD Success Metrics table). SOC2 audit logging is embedded from the first milestone rather than bolted on later, and the phased rollout strategy uses feature flags (AUTH_NEW_LOGIN, AUTH_TOKEN_REFRESH) to de-risk the production cut-over.

Constant-time anti-enumeration defenses (dummy-hash verify on unknown-email and lockout-rejected paths; always-enqueue reset jobs with audit-row parity) are designed in M1/M2/M4 — not retrofitted — because timing-oracle defects discovered under pen-test are the highest-impact GA blocker (R-010).

---

## Milestones

---

### M1: Infrastructure, Schema, and Security Foundations

<!-- Source: Base (V2 Sonnet, modified) — Changes #4, #9, #11, #15: schema additions for SOC2 retention split, admin RBAC seed, Redis isolation, multi-AZ -->

**Objective:** Provision all infrastructure dependencies (multi-AZ), define and deploy the database schema (including minimal admin flag and SOC2-relevance flag), implement PasswordHasher, and establish the audit logging pipeline that SOC2 requires from day one.

**Scope:**

- In: PostgreSQL 15+ (multi-AZ) and Redis 7+ (multi-AZ, isolated namespaces) provisioning; users and audit_log table creation (including `isAdmin` column and `soc2_relevant` flag); PasswordHasher module with bcrypt cost 12; structured audit log emitter; CI pipeline with testcontainers; Prometheus metrics scaffolding for auth_login_total, auth_login_duration_seconds, auth_registration_total, auth_token_refresh_total (TDD Section 14); build-time dummy-hash constant provisioned in deploy artifacts.
- Out: AuthService orchestration; token issuance; API endpoints; frontend components; email integration.

**Deliverables:**

| ID | Deliverable | Traceability |
|----|-------------|--------------|
| D1.1 | PostgreSQL schema migration: users table (id UUID PK, email UNIQUE NOT NULL, password_hash, display_name 2-100 chars, created_at, updated_at, last_login_at, roles TEXT[] DEFAULT '{user}', locked_until TIMESTAMP, failed_login_count INT DEFAULT 0, **isAdmin BOOLEAN DEFAULT FALSE**) <!-- Change #9: minimal admin enforcement (INV-004) --> | TDD Section 7.1 UserProfile fields; PRD FR-AUTH.2 duplicate rejection |
| D1.2 | PostgreSQL schema migration: audit_log table (id, user_id, event_type, ip_address, user_agent, outcome, timestamp, **soc2_relevant BOOLEAN DEFAULT TRUE**); indexes on (user_id, timestamp) and (event_type, timestamp); **partitioned by month for purge efficiency**; 12-month retention default with derived view for 90-day operational subset (resolves OQ-PRD-TDD-1 without destructive migration) <!-- Change #4: OQ-7 retention conflict resolution + schema flag (INV-002) --> | PRD Legal/Compliance — SOC2 Type II 12-month retention; TDD §7.2 90-day; PRD FR-AUTH.5 audit logging AC |
| D1.3 | PasswordHasher module: hash(plaintext, cost=12) and verify(plaintext, hash) functions with bcrypt; benchmark asserting hash time under 500ms (TDD Section 17) | TDD NFR-SEC-001; TDD Section 6.4 design decisions |
| D1.4 | Audit log emitter: emits structured JSON events for all auth state transitions (registration_attempt, login_attempt, login_success, login_failure, account_locked, password_reset_requested, password_reset_completed, token_revoked) | PRD Legal/Compliance — SOC2 user ID, timestamp, IP, outcome |
| D1.5 | Redis 7+ provisioning (**multi-AZ**) with TLS — **two logically-isolated namespaces**: `redis-session` (refresh tokens + lockout counters) and `redis-queue` (BullMQ reset-email queue). Implementation may be two Redis instances OR single instance with explicit `maxmemory-policy` per key-prefix + monitoring alert when queue keys exceed 30% of allocation. Memory-budget documented per namespace. <!-- Change #11: Redis isolation (INV-012); Change #15: multi-AZ --> | TDD Section 25.3 capacity planning; INV-012 fix |
| D1.6 | CI pipeline: Docker Compose for local dev (PostgreSQL, Redis); testcontainers for CI ephemeral databases; Jest + ts-jest configured for 80% unit coverage gate | TDD Section 15.3 test environments |
| D1.7 | Prometheus exporters registered for auth_login_total, auth_login_duration_seconds, auth_registration_total, auth_token_refresh_total; Grafana dashboard skeleton | TDD Section 14 — Observability |
| D1.8 | **PostgreSQL multi-AZ deployment with synchronous standby for SOC2 fault-tolerance evidence**; documented failover RTO/RPO targets <!-- Change #15: Multi-AZ Postgres --> | A-001 resolution; SOC2 fault-tolerance |
| D1.9 | **Dummy-hash constant provisioned at build/deploy time** as a stable cross-pod config artifact (NOT per-pod boot-time hash); identical across all pods to maintain constant-time invariant. Stored in secret store alongside RSA keys; rotated only deliberately. <!-- Change #12: dummy hash provisioning (INV-001) --> | INV-001 fix |
| D1.10 | **Admin bootstrap seed**: explicit admin emails set `isAdmin=TRUE` at M1 deploy via migration; admin list maintained in deploy config (not editable via API in v1.0) <!-- Change #9: minimal admin RBAC (INV-004) --> | INV-004 fix |

**Acceptance Criteria:**

1. Schema migrations run idempotently on empty PostgreSQL instance; rollback tested. <!-- Source: Base (V2 Sonnet) -->
2. PasswordHasher.hash() produces bcrypt output with cost 12; verify() correctly matches and rejects; benchmark under 500ms on CI hardware (TDD Section 17).
3. Audit log emitter writes a valid JSON record to audit_log table containing user_id, event_type, timestamp, ip_address, outcome, soc2_relevant for each emitted event.
4. Redis reachable from service network (both namespaces); TLS enforced; ping latency under 5ms; multi-AZ failover validated in staging.
5. CI pipeline runs on every PR; testcontainers spin up PostgreSQL and Redis; tests pass.
6. **Dummy-hash constant is identical across all pods (verify by hashing the constant string in each pod and comparing); not regenerated on pod restart.** <!-- Change #12: INV-001 -->
7. **PostgreSQL synchronous standby promoted within 60s during simulated primary failure (multi-AZ drill).** <!-- Change #15 -->

**Dependencies:**

- External: PostgreSQL 15+ multi-AZ cluster provisioned by platform team; Redis 7+ multi-AZ provisioned; SendGrid account credentials available for later milestone.
- Internal: None (this is the first milestone).

**Estimated Duration:** 2 weeks.

**Risks and Mitigations:**

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| PostgreSQL provisioning delayed by infra team | Medium | High | Begin schema design in parallel using Docker Compose local environment; trigger provisioning request on day one. |
| bcrypt cost 12 exceeds 500ms on CI hardware | Low | Medium | Profile on CI runners first; if over budget, propose cost 11 with security team sign-off per SEC-POLICY-001. |
| Audit log schema too narrow for future SOC2 control mapping | Medium | Medium | `soc2_relevant` flag + JSONB metadata column allows M5 to derive operational-vs-SOC2 view without destructive migration (Change #4). |
| Multi-AZ infra cost exceeds budget | Medium | Medium | SOC2-defensible cost; document risk acceptance path (single-AZ + manual DR) if cost-blocked. |

---

### M2: Authentication Core — Registration, Login, Logout

<!-- Source: Base (V2 Sonnet, modified) — Changes #2, #5, #8, #12, #13: constant-time mechanisms, atomic-UPDATE lockout, per-email rate limit, sliding-window/boundary parity -->

**Objective:** Implement AuthService orchestration for user registration and login/logout flows, wiring PasswordHasher to the database with **atomic lockout semantics and constant-time anti-enumeration defenses**, and issuing initial JWT access tokens (refresh tokens deferred to M3 for clean separation).

**Scope:**

- In: AuthService.login(), AuthService.register(), AuthService.logout(); POST /auth/login, POST /auth/register endpoints; input validation (email format, password policy: minimum 8 chars, uppercase, number); duplicate email handling (409 Conflict); **atomic lockout (single-statement UPDATE) keyed by email** after 5 failed attempts within 15 minutes (423 Locked); **constant-time defenses on all failure paths**; generic error responses preventing user enumeration; API Gateway rate limiting configuration (**10 req/min per IP AND 5 req/min per email for login; per-email is authoritative anti-brute-force control**, 5 req/min per IP for register).
- Out: Token refresh flow (M3); password reset (M4); profile retrieval (M3); frontend pages (M5).

**Deliverables:**

| ID | Deliverable | Traceability |
|----|-------------|--------------|
| D2.1 | AuthService.login(email, password): normalizes email to lowercase; **executes atomic counter-update SQL**: `UPDATE users SET failed_login_count = failed_login_count + 1, locked_until = CASE WHEN failed_login_count + 1 >= 5 THEN NOW() + INTERVAL '15 minutes' ELSE locked_until END WHERE email = $1 RETURNING failed_login_count, locked_until` — no SELECT FOR UPDATE needed; calls PasswordHasher.verify(); on success issues access token via JwtService (15-min TTL) and resets `failed_login_count = 0`; emits `account_locked` audit event at 5th failure; **returns generic 401 for wrong password, unknown email, AND locked accounts**. <!-- Change #5: atomic-UPDATE lockout (INV-009, INV-013) --> | PRD FR-AUTH.1 AC; TDD FR-AUTH-001 AC items 1-4; PRD Error Handling table |
| D2.2 | **Constant-time defense module** (covers INV-001, INV-005, INV-014): (a) on unknown-email branch, execute `PasswordHasher.verify(submittedPassword, DUMMY_HASH_CONSTANT)` before returning generic 401; (b) on lockout-rejected path, ALSO execute `PasswordHasher.verify` against the dummy hash before returning 401 (so locked-account latency matches unknown-email-with-dummy-verify path — fixes INV-014); (c) DUMMY_HASH_CONSTANT loaded from D1.9 build-time config; (d) lockout-key is the submitted email (atomic UPDATE returns no-op for unknown email — no information leak); (e) Option B for v1.0: fixed-window lockout with explicit AC that lockout-rejected response time MUST match dummy-verify duration regardless of window state (sliding-window upgrade deferred to v1.1). <!-- Changes #2, #12, #13: constant-time + dummy-hash + boundary parity (INV-001, INV-005, INV-014) --> | INV-001/005/014 fixes; PRD anti-enumeration |
| D2.3 | AuthService.register(email, password, displayName): validates email format, password policy (>=8 chars, uppercase, number), displayName (2-100 chars); normalizes email to lowercase; checks uniqueness via DB unique constraint (not application-level check, to handle concurrent registration race); hashes password via PasswordHasher; inserts UserProfile; emits registration_attempt and login_success audit events; **also emits `registration_attempt` audit row on race-loser (409) path so SOC2 logs see both attempts** <!-- INV-003 partial mitigation -->; auto-logs user in (returns access token) | PRD FR-AUTH.2 AC; TDD FR-AUTH-002 AC items 1-4; PRD Signup Flow |
| D2.4 | AuthService.logout(userId): revokes all refresh tokens for user in Redis (TokenManager integration placeholder); emits token_revoked audit event; returns 200 | PRD "Log Out ends session immediately" AC |
| D2.5 | POST /auth/login endpoint: accepts {email, password}; returns 200 with {accessToken, expiresIn: 900, tokenType: "Bearer"} or error; **rate limited at 10 req/min per IP AND 5 req/min per email at API Gateway (per-email is primary; per-IP guards against credential-stuffing across accounts; per-email lockout is the primary defense and acknowledges A-004 NAT false-positive concern).** <!-- Change #8 --> | TDD Section 8.2 POST /auth/login |
| D2.6 | POST /auth/register endpoint: accepts {email, password, displayName}; returns 201 with UserProfile or error (400 validation, 409 duplicate); rate limited at 5 req/min per IP | TDD Section 8.2 POST /auth/register |
| D2.7 | JwtService: sign(payload, RS256, 15-min TTL) and verify(token, RS256) with 2048-bit RSA key loaded from secrets mount (in-memory tmpfs, never on disk); 5-second clock skew tolerance; key rotation documented in M3 D3.x runbook | TDD Section 6.4 key decisions; TDD NFR-SEC-002 |
| D2.8 | Unit tests: valid login returns token; invalid credentials return 401; locked account returns 423; duplicate email returns 409; weak password returns 400 with field-level errors; password never appears in logs; **timing-parity test: 1000 samples of unknown-email-401 vs locked-account-401 vs wrong-password-401 latencies; p95 deltas within 20ms** <!-- Change #2/#13 verification --> | TDD Section 15.2 unit test table |
| D2.9 | Integration tests: full registration flow through PasswordHasher to database insert; concurrent duplicate email race handled by unique constraint; **concurrent failed logins for same email across 3 pods correctly trigger lockout at 5th attempt (10 parallel POST /auth/login from 3 pods using testcontainers)** <!-- Change #5: atomic lockout proof --> | TDD Section 15.2; INV-009 fix |

**Acceptance Criteria:**

1. POST /auth/login with valid credentials returns 200 with accessToken (JWT, RS256-signed, 15-min TTL) within 200ms p95 (TDD NFR-PERF-001).
2. POST /auth/login with wrong password returns 401 with body `{error: {code: "AUTH_INVALID_CREDENTIALS", message: "The provided email or password is incorrect.", status: 401}}` — **identical response and identical p95 latency (±20ms) for non-existent email, wrong-password, AND lockout-rejected paths** (PRD Error Handling — no user enumeration; INV-014 fix).
3. POST /auth/login after 5 failures within 15 minutes returns 423 Locked; **6th attempt response time matches dummy-verify duration (NOT faster — INV-014 fix)**.
4. **Concurrent failed logins for the same email across multiple pods correctly trigger lockout at exactly the 5th attempt (atomic-UPDATE guarantees no double-decrement or skip).** <!-- Change #5 -->
5. POST /auth/register with valid input returns 201 with UserProfile including id (UUID v4), email (lowercase), displayName, createdAt, roles=["user"], lastLoginAt=null, isAdmin=false (TDD FR-AUTH-002 AC item 1).
6. POST /auth/register with duplicate email returns 409 Conflict; **both registration_attempt audit rows present (winner + loser)**.
7. POST /auth/register with password "short" returns 400 with field-level validation errors.
8. All auth events emitted to audit_log with user_id, timestamp, IP, outcome (PRD SOC2 requirement).
9. Unit test coverage for AuthService and PasswordHasher exceeds 80%.
10. Concurrent registration with identical email handled gracefully (first wins, second gets 409; no duplicate rows).
11. **Per-email rate limit (5 req/min) enforced and returns 429 on 6th attempt within 60 seconds regardless of source IP** <!-- Change #8 -->.

**Dependencies:**

- M1 (schema with isAdmin + soc2_relevant columns, PasswordHasher, audit logger, Redis multi-AZ provisioned, dummy-hash constant deployed).

**Estimated Duration:** 2 weeks.

**Risks and Mitigations:**

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Account lockout threshold (5/15min) too aggressive for typo-prone users | Medium | Medium | Threshold + window configurable via env vars; monitor locked-account rate in beta; adjust if >2% of users hit lockout. |
| Atomic-UPDATE SQL pattern misimplemented (race condition reintroduced) | Low | High | Integration test with 10 parallel pods enforced as CI gate (D2.9); SQL pattern reviewed by DB lead. |
| Constant-time defense regression in future refactor | Medium | High | Timing-parity test (D2.8) runs in CI on every PR; alert if p95 delta exceeds 20ms. |
| API Gateway rate limiting per-email key unsupported | Low | Medium | Validate gateway supports per-email key dimension early; fallback: implement at AuthService layer with Redis counter. |

---

### M3: Token Lifecycle, Session Persistence, and Profile Retrieval

<!-- Source: Base (V2 Sonnet, modified) — Changes #6, #9: quarterly RS256 key-rotation runbook, isAdmin JWT claim -->

**Objective:** Implement TokenManager for the full JWT access/refresh token lifecycle, add the GET /auth/me profile endpoint, enable multi-device session support with revocation, and freeze the API contract for parallel frontend work.

**Scope:**

- In: TokenManager (issue, refresh, revoke); POST /auth/refresh endpoint; GET /auth/me endpoint; refresh token storage in Redis (`redis-session` namespace) with 7-day TTL; opaque refresh tokens (not JWT); rotation-on-refresh (old token revoked, new pair issued, MULTI/EXEC atomic); silent token refresh in AuthProvider (placeholder contract for M5); multi-device concurrent sessions; **JWT payload includes `isAdmin` claim from users table**; Redis unavailability graceful degradation (reject refresh, force re-login); **quarterly RS256 key-rotation runbook**.
- Out: Password reset flow (M4); frontend components (M5).

**Deliverables:**

| ID | Deliverable | Traceability |
|----|-------------|--------------|
| D3.1 | TokenManager.issueTokens(userId, roles, **isAdmin**): generates access token (JwtService, 15-min TTL, payload includes `userId, roles, isAdmin`) and opaque refresh token (crypto-random, 256-bit); stores hashed refresh token in `redis-session` keyed by userId with 7-day TTL; returns AuthToken | TDD §7.1; INV-004 fix |
| D3.2 | TokenManager.refresh(oldRefreshToken): validates old token against Redis; **atomic MULTI/EXEC revoke-old + issue-new** to prevent replay during rotation; emits token_refresh_success / token_refresh_failure audit events; returns 401 with AUTH_TOKEN_EXPIRED or AUTH_TOKEN_REVOKED on mismatch <!-- INV-010 promoted to AC --> | TDD FR-AUTH-003 AC items 2-4; INV-010 |
| D3.3 | TokenManager.revokeAllForUser(userId): deletes all refresh tokens for a user from Redis; used by logout and password reset flows | PRD FR-AUTH.5 AC |
| D3.4 | POST /auth/refresh endpoint: accepts {refreshToken}; returns 200 with new AuthToken pair or 401; rate limited at 30 req/min per user | TDD Section 8.2; TDD Section 8.1 |
| D3.5 | GET /auth/me endpoint: validates Bearer accessToken; returns UserProfile with id, email, displayName, createdAt, updatedAt, lastLoginAt, roles, **isAdmin**; returns 401 for missing/expired/invalid token | TDD Section 8.2; TDD FR-AUTH-004 |
| D3.6 | AuthService.logout wiring: calls TokenManager.revokeAllForUser(userId); invalidates all sessions; redirects to landing page | PRD "Log Out" AC |
| D3.7 | Redis unavailability handling: if `redis-session` unreachable during refresh, return 401 AUTH_SERVICE_UNAVAILABLE with retry-after header; do not serve stale tokens; alert fires | TDD Section 12 |
| D3.8 | **RS256 key-rotation runbook with quarterly cadence**: documented rotation procedure; key-access audit log; in-memory tmpfs mount for private key; rotation drill scheduled in M6 Phase 1 Alpha <!-- Change #6 --> | V1 D2.7 contribution; SOC2 audit value |
| D3.9 | **Frozen OpenAPI contract published to frontend team to unblock M5 in parallel** <!-- Source: V1 Opus, L127 D2.9 — merged per Change #1 sequencing rationale --> | Parallel-work enablement |
| D3.10 | Unit tests: token refresh with valid token returns new pair; expired/revoked refresh token returns 401; rotation-on-refresh prevents reuse | TDD Section 15.2 |
| D3.11 | Integration tests: full token lifecycle against real Redis; expired Redis TTL correctly invalidates refresh tokens; **concurrent two-tab refresh race: first wins, second gets 401 (MULTI/EXEC atomicity proof)** | TDD Section 15.2; INV-010 |
| D3.12 | Load test script (k6): simulate 500 concurrent token refresh operations; validate p95 < 100ms for refresh | TDD NFR-PERF-002 |

**Acceptance Criteria:**

1. POST /auth/refresh with valid refresh token returns 200 with new AuthToken pair; old refresh token is revoked.
2. POST /auth/refresh with expired refresh token returns 401 with AUTH_TOKEN_EXPIRED error code.
3. GET /auth/me with valid accessToken returns UserProfile with all fields **including `isAdmin`** matching TDD Section 7.1 schema.
4. GET /auth/me with expired token returns 401.
5. Token refresh latency p95 < 100ms under 500 concurrent requests.
6. Redis failure during refresh returns 401 (not stale data) and triggers alert.
7. Logout revokes all refresh tokens for the user; subsequent refresh attempts return 401.
8. All token lifecycle events emitted to audit_log.
9. JWT access token payload includes userId, roles, **isAdmin**; signed RS256; expires in exactly 900 seconds.
10. 7-day refresh token TTL enforced by Redis TTL.
11. **Key-rotation runbook reviewed and signed off by sec-reviewer; first drill scheduled for M6 Phase 1 Alpha.** <!-- Change #6 -->
12. **Concurrent two-tab refresh: first succeeds, second returns 401 (MULTI/EXEC atomicity verified).** <!-- INV-010 -->

**Dependencies:**

- M1 (Redis namespaces provisioned, JwtService keys, isAdmin column).
- M2 (AuthService login/register emitting initial access tokens; constant-time defenses).

**Estimated Duration:** 2 weeks.

**Risks and Mitigations:**

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Refresh token rotation creates race condition when two tabs refresh simultaneously | Medium | High | Redis MULTI/EXEC atomic revoke-and-issue; integration test for concurrent refresh race; documented as expected behavior. |
| Redis single point of failure for all sessions | Medium | High | Multi-AZ Redis from M1 (Change #15); test failover in staging. |
| 7-day refresh TTL too long for security posture | Low | Medium | TTL configurable via env var; monitor average session duration; adjust in Phase 2 beta. |

---

### M4: Password Reset, Email Integration, Admin Audit Views, and Backend Pen-Test

<!-- Source: Base (V2 Sonnet, modified) — Changes #3, #7, #9, #10, #18: always-enqueue email with audit-row parity, backend pen-test split into M4, minimal admin RBAC, keyset pagination -->

**Objective:** Complete the self-service password reset flow with **constant-time email-job enqueuing**, implement admin-facing audit log querying **with minimal admin-role enforcement**, harden the reset flow against enumeration and replay attacks, and execute the **backend penetration test as M4 completion gate**.

**Scope:**

- In: POST /auth/reset-request; POST /auth/reset-confirm; reset token generation (single-use, 1-hour TTL); SendGrid email integration; reset email template; **always-enqueue mechanism (worker silently drops unregistered-email jobs + emits audit row for all requests)**; session invalidation on password change; **admin audit log query endpoint with `isAdmin=true` JWT-claim gating and keyset pagination**; GDPR consent recording at registration; **backend penetration test (RS256 verification, refresh rotation, lockout bypass, timing oracles, password storage, rate limit)**.
- Out: Frontend pages (M5); frontend pen-test (M5); rollout and feature flags (M6).

**Deliverables:**

| ID | Deliverable | Traceability |
|----|-------------|--------------|
| D4.1 | AuthService.requestPasswordReset(email): **always enqueues email job in `redis-queue` BullMQ regardless of registration status**; for registered emails: worker generates crypto-random reset token (256-bit), stores hashed token in `redis-session` with 1-hour TTL keyed by user_id, sends email via SendGrid; for unregistered emails: **worker silently drops the email-send step but ALSO emits a `password_reset_requested` audit row** so audit-log absence ≠ unregistered (fixes INV-007); returns identical 200 success response for all emails. <!-- Change #3 + Change #10: always-enqueue + audit-row parity (INV-007) --> | PRD FR-AUTH.5 AC; TDD FR-AUTH-005 AC items 1, 3; PRD anti-enumeration; INV-007 |
| D4.2 | AuthService.confirmPasswordReset(token, newPassword): validates token against Redis; on match, hashes new password via PasswordHasher; updates users table; deletes reset token (single-use enforcement); calls TokenManager.revokeAllForUser(userId); emits password_reset_completed audit event; returns success | TDD FR-AUTH-005 AC items 2, 4 |
| D4.3 | POST /auth/reset-request endpoint: accepts {email}; returns 200 with confirmation (identical for all emails); rate limited at 3 req/min per IP AND 1 req/min per email | PRD Password Reset Flow |
| D4.4 | POST /auth/reset-confirm endpoint: accepts {token, password}; returns 200 on success or 400/401 on failure; expired tokens return clear error | PRD Error Handling |
| D4.5 | SendGrid integration module: transactional email template; **BullMQ worker on `redis-queue` namespace with retry on transient failure, dead-letter on permanent failure**; **worker emits `password_reset_requested` audit row for ALL incoming requests (including unregistered-email drops)** with non-user-correlatable `request_id` payload; delivery monitoring with alerting on bounce rate >5%; **SPF, DKIM, DMARC configured; Gmail/Outlook deliverability tested in staging** | PRD Dependencies; INV-007 fix |
| D4.6 | GDPR consent recording: registration endpoint records consent timestamp in audit_log alongside registration event; consent text version stored in event metadata | PRD Legal/Compliance |
| D4.7 | Admin audit query API: `GET /admin/audit-logs?user_id=&event_type=&from=&to=&cursor=&limit=` — **requires `isAdmin=true` JWT claim (enforced at endpoint guard, populated by D1.10 seed + D3.5 me payload)**; **keyset cursor pagination on `(timestamp DESC, id DESC)` with explicit LIMIT default 100, max 500; no OFFSET pagination on large tables**; results include user ID, event type, timestamp, IP, outcome; **respects `soc2_relevant` filter parameter for SOC2-evidence pulls**. <!-- Change #9: admin RBAC (INV-004); Change #18: keyset pagination (INV-011); Change #4: soc2_relevant flag --> | PRD FR-AUTH.5 admin story; INV-004, INV-011 |
| D4.8 | Integration tests: full reset flow (request → email mock → confirm → password changed → sessions revoked); expired token rejection; reused token rejection; concurrent reset request handling; **unregistered-email reset emits audit row but no email sent (INV-007 verification)**; **admin endpoint returns 403 without isAdmin claim**; **admin endpoint keyset pagination returns deterministic ordering under concurrent inserts** | TDD Section 15.2 |
| D4.9 | Load test for reset flow: 100 concurrent reset requests; email delivery pipeline does not block API response (async dispatch); p95 for POST /auth/reset-request under 200ms regardless of queue saturation | PRD Open Question 1 |
| D4.10 | **Backend penetration test report**: focused on backend surface (RS256 verification, refresh rotation, lockout bypass, timing oracles for unknown-email vs locked vs wrong-password, password storage, rate limit, admin endpoint RBAC, atomic-UPDATE race). **M4 completion gate — no P0/P1 findings unresolved.** <!-- Change #7: pen-test split --> | PRD Risk Analysis; V1 R-010 |

**Acceptance Criteria:**

1. POST /auth/reset-request for registered email enqueues email job; email arrives within 60 seconds; returns 200 with generic confirmation; **response p95 ≤ 200ms regardless of registration status**.
2. POST /auth/reset-request for unregistered email returns identical 200 response; **NO email sent BUT audit-log row IS written with `password_reset_requested` outcome** (INV-007 fix; audit absence ≠ unregistered).
3. POST /auth/reset-confirm with valid token and strong password updates password hash; all existing refresh tokens revoked; all active sessions terminated.
4. POST /auth/reset-confirm with expired token (TTL > 1 hour) returns error with AUTH_RESET_TOKEN_EXPIRED code.
5. POST /auth/reset-confirm with already-used token returns 401; single-use enforcement verified.
6. Admin audit query (`/admin/audit-logs`): **without `isAdmin=true` JWT claim returns 403 Forbidden**; with claim returns paginated results filtered by user_id, event_type, soc2_relevant, and date range using keyset cursor `(timestamp DESC, id DESC)`; results stable under concurrent inserts.
7. GDPR consent recorded at registration with timestamp and consent text version in audit_log metadata.
8. SendGrid delivery monitoring alert fires if bounce rate exceeds 5% over 1-hour window.
9. **Backend penetration test report shows zero P0/P1 findings unresolved before M5 entry** <!-- Change #7 -->.

**Dependencies:**

- M1 (audit_log schema with soc2_relevant; Redis namespaces; isAdmin column; admin seed).
- M2 (AuthService, PasswordHasher, atomic lockout).
- M3 (TokenManager.revokeAllForUser; isAdmin JWT claim).
- External: SendGrid API credentials and approved sender domain configured; sec-reviewer booked for pen-test.

**Estimated Duration:** 2 weeks (backend pen-test runs in final 3 days of milestone).

**Risks and Mitigations:**

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| SendGrid downtime blocks password reset flow entirely | Low | High | Async queue (does not block API response); queue depth monitoring; alert on backlog >100; documented fallback support channel. |
| Reset token race: user clicks link in two emails, both reset tokens valid | Low | Medium | Single-use enforcement at Redis level; new request invalidates previous tokens. |
| Admin audit query performance degrades with 12-month data volume | Medium | Medium | Index on (user_id, timestamp), (event_type, timestamp); keyset pagination; query timeout at 5 seconds; partition by month. |
| Password reset email lands in spam | Medium | High | Pre-warm SendGrid domain; SPF, DKIM, DMARC before beta; test against Gmail/Outlook in staging. |
| Backend pen-test finds P0 close to M5 entry | Medium | High | Pen-test scheduled in M4 final 3 days; 1-week buffer in M5 absorbs cure time; if P0 found, extend M4 by 1 week before blocking M5 (Change #7). |
| Audit-row-on-drop creates registration oracle if request_id is correlatable | Low | High | `request_id` is opaque UUID, NOT email-derived; admin query never joins to email-lookup for dropped requests. |

---

### M5: Frontend Integration, E2E Validation, and Frontend Security Hardening

<!-- Source: Base (V2 Sonnet, modified) — Change #7: pen-test scope narrowed to frontend; buffer extended -->

**Objective:** Build and integrate LoginPage, RegisterPage, AuthProvider, and ProfilePage; validate all user journeys end-to-end; conduct **frontend-focused security review and penetration testing** (XSS, CSRF, AuthProvider redirect loop, token-in-memory enforcement) against OWASP ASVS L2.

**Scope:**

- In: LoginPage component (email/password form, generic errors, rate limit UX, lockout messaging); RegisterPage component (email/password/displayName form, inline validation, GDPR consent checkbox, password strength meter); AuthProvider context (token storage in memory — not localStorage — per TDD R-001 mitigation, silent refresh on 401 interception, redirect to LoginPage on refresh failure, **one-refresh-attempt cap + circuit breaker after 3 consecutive failures**); ProfilePage component; E2E test suite (Playwright); **frontend security review + frontend penetration testing (XSS token exfiltration, CSRF on cookie-based refresh, AuthProvider redirect loop, token storage verification, inline-password-policy drift)**.
- Out: Production rollout (M6); backend pen-test (completed in M4).

**Deliverables:**

| ID | Deliverable | Traceability |
|----|-------------|--------------|
| D5.1 | LoginPage: email/password fields; submit calls POST /auth/login; stores AuthToken in memory via AuthProvider (not localStorage — TDD R-001); displays generic "Invalid email or password" on 401; displays lockout message on 423; redirects to dashboard on success; loads in <1 second | TDD Section 10.2; PRD Login Flow |
| D5.2 | RegisterPage: email, password, displayName fields with inline validation; GDPR consent checkbox; submit calls POST /auth/register; auto-login on success; redirect to dashboard within 2 seconds | TDD Section 10.2; PRD Signup Flow |
| D5.3 | AuthProvider: React context managing AuthToken state in memory; **refresh token via HttpOnly cookie**; transparent token refresh; **one-refresh-attempt cap per request; circuit breaker disables refresh for 30s after 3 consecutive failures**; clears tokens on tab/window close; exposes userProfile, isAdmin, isAuthenticated to children | TDD Section 10.2/10.3; PRD FR-AUTH.3; INV redirect-loop |
| D5.4 | ProfilePage: fetches GET /auth/me; displays displayName, email, createdAt; renders in under 1 second | TDD Section 10.1; PRD FR-AUTH.4 |
| D5.5 | E2E test suite (Playwright): (1) Full registration → auto-login → profile view; (2) Login with valid credentials → session persists on refresh; (3) Login with invalid credentials → generic error; (4) Token expires during active session → silent refresh → no data loss; (5) Password reset flow end-to-end; (6) Logout → session terminated; (7) **AuthProvider redirect-loop prevention test (3 consecutive 401s triggers circuit breaker)**; (8) **CSRF defense on cookie-based refresh** | TDD Section 15.2 |
| D5.6 | Security review report: bcrypt cost 12 verified; RS256 key-rotation schedule signed off; no passwords/tokens in logs; CORS whitelisted; TLS 1.3 enforced; OWASP ASVS L2 checklist addressed | TDD Section 13; PRD NFR-AUTH.3 |
| D5.7 | **Frontend penetration test report** (scope: XSS token exfiltration, CSRF on cookie refresh, token storage in memory verification, AuthProvider redirect loop, inline-password-policy drift between UI and server). **1-week buffer reserved for remediation** before M6 gate. <!-- Change #7: pen-test scope narrowed --> | PRD Risk Analysis |

**Acceptance Criteria:**

1. LoginPage submits credentials to POST /auth/login; success redirects to dashboard; failure shows generic error with no timing-based user enumeration (response time variance <50ms; backend already enforces <20ms in D2.8).
2. RegisterPage validates all fields client-side; GDPR consent mandatory; duplicate email shows user-friendly message.
3. AuthProvider stores accessToken in memory only (not localStorage, not sessionStorage); silent refresh triggers when accessToken within 60 seconds of expiry; tab close clears tokens.
4. ProfilePage displays all UserProfile fields including isAdmin if applicable; redirects to LoginPage when unauthenticated.
5. E2E test suite covers all 8 scenarios listed in D5.5; all pass against staging.
6. Security review report confirms: bcrypt cost 12 enforced, RS256 signing active, no secrets in logs, CORS whitelisted, TLS 1.3 only.
7. **Frontend pen-test report shows zero critical findings; high findings have documented remediation plan before M6 gate** (Change #7).
8. Registration form submission to dashboard redirect completes in under 2 seconds.
9. Registration conversion funnel tracking instrumented.

**Dependencies:**

- M2 (login/register endpoints with constant-time defenses).
- M3 (token refresh, GET /auth/me, isAdmin claim, frozen OpenAPI contract from D3.9).
- M4 (password reset endpoints, backend pen-test cleared).
- External: Frontend build pipeline; staging environment with backend deployed.

**Estimated Duration:** 2 weeks (can partially overlap with M4 backend work via frozen OpenAPI contract).

**Risks and Mitigations:**

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Frontend pen-test reveals critical vulnerability blocking GA | Low | Critical | Schedule pen test at start of M5 Week 2; 1-week buffer for remediation (Change #7); if critical finding, extend M5 by up to 1 week before blocking M6 gate. |
| AuthProvider silent refresh causes redirect loop on stale tokens | Medium | High | Circuit breaker: after 3 consecutive refresh failures, redirect to LoginPage with expired_session message (D5.3, D5.5 test). |
| Frontend build pipeline incompatible with token-in-memory pattern | Low | Medium | Validate AuthProvider pattern in isolated POC during M3; ensure SSR/hydration compatibility. |
| Inline password-strength meter drifts from server policy | Medium | Medium | Single shared policy module (JSON schema); contract test against /register drives both UI and server. |

---

### M6: Phased Rollout, Monitoring Validation, and General Availability

<!-- Source: Base (V2 Sonnet, modified) — Change #6: first key-rotation drill in Phase 1; Change #14: legacy-vs-greenfield rollback branch -->

**Objective:** Execute the three-phase rollout strategy (Internal Alpha, 10% Beta, 100% GA), validate all monitoring and runbooks, **execute first quarterly RS256 key-rotation drill**, **branch rollback procedure based on legacy-vs-greenfield deployment topology**, remove feature flags, and achieve 99.9% uptime over 7 days in production.

**Scope:**

- In: Feature flag deployment (AUTH_NEW_LOGIN, AUTH_TOKEN_REFRESH); Phase 1 Internal Alpha (1 week — auth-team + QA + **first RS256 key-rotation drill** + **deployment-topology check**); Phase 2 Beta at 10% traffic (2 weeks); Phase 3 GA at 100% (1 week); rollback procedure validation (**branched: legacy-flag-off vs greenfield-503-blast-radius**); runbook review; on-call rotation setup; feature flag removal; capacity validation; success metrics baseline measurement.
- Out: New feature development (post-GA backlog).

**Deliverables:**

| ID | Deliverable | Traceability |
|----|-------------|--------------|
| D6.1 | Feature flags AUTH_NEW_LOGIN and AUTH_TOKEN_REFRESH deployed to production (default OFF); flag toggle documented in runbook | TDD Section 19.2 |
| D6.2 | Phase 1 Internal Alpha: AUTH_NEW_LOGIN ON for auth-team and QA; all FR-AUTH-001..005 pass manual testing against staging; zero P0/P1 bugs; **first RS256 key-rotation drill executed and audit-logged**; **deployment-topology verified (legacy-present vs greenfield)** <!-- Change #6 + Change #14 --> | TDD Section 19.1 |
| D6.3 | Phase 2 Beta (10%): AUTH_NEW_LOGIN ON for 10% of traffic; monitor p95 latency <200ms, error rate <0.1%, zero TokenManager Redis connection failures over 2 weeks | TDD Section 19.1 |
| D6.4 | Phase 3 GA (100%): AUTH_NEW_LOGIN ON for all traffic; legacy auth endpoints deprecated (or 503 in greenfield); AUTH_TOKEN_REFRESH enabled; validate 99.9% uptime over first 7 days | TDD Section 19.1 |
| D6.5 | **Branched rollback procedure tested in staging**: <!-- Change #14 (A-007) --> **(a) Legacy-present branch**: disable AUTH_NEW_LOGIN → verify legacy auth handles `/auth/*` traffic → smoke test → document elapsed time. **(b) Greenfield branch (no legacy)**: feature-flag-off blast-radius test → confirm auth-disabled state returns 503 cleanly for all `/auth/*` endpoints → document blast radius. Topology determined at Phase 1 kickoff. | TDD Section 19.3; A-007 |
| D6.6 | Runbook published and reviewed: AuthService down; PostgreSQL multi-AZ failover; Redis (both namespaces) graceful degradation; token refresh failure; **RS256 key rotation procedure with quarterly cadence; first drill executed during M6 Phase 1 Alpha** <!-- Change #6 -->; escalation path | TDD Section 25.1/25.2 |
| D6.7 | Success metrics dashboard live: registration conversion (>60%), login p95 (<200ms), session duration (>30 min), failed login rate (<5%), password reset completion (>80%) | PRD Success Metrics |
| D6.8 | Capacity validation report: 3 AuthService replicas handling 500 concurrent users; PostgreSQL connection pool at 100 with <50ms wait; Redis (both namespaces) under utilization caps; HPA scales to 10 replicas at CPU >70% | TDD Section 25.3 |
| D6.9 | SOC2 audit evidence package: audit log sample covering all event types; retention policy documentation (12-month SOC2-relevant + 90-day operational view via D1.2 flag); access control documentation; incident response runbook; consent recording evidence | PRD Legal/Compliance; OQ-PRD-TDD-1 resolution |

**Acceptance Criteria:**

1. Phase 1 Internal Alpha: all FR-AUTH-001..005 pass; zero P0/P1 bugs; **first key-rotation drill completes without service disruption; deployment topology declared (legacy vs greenfield)**.
2. Phase 2 Beta: p95 latency <200ms sustained; error rate <0.1%; no Redis connection failures; rollback not triggered.
3. Phase 3 GA: 99.9% uptime over first 7 days; all monitoring dashboards green; feature flags removed from configuration.
4. **Rollback procedure tested end-to-end in staging via appropriate branch** (legacy or greenfield); completed in under 15 minutes from flag toggle to confirmation.
5. Runbook reviewed and signed off by auth-team on-call engineer; escalation path validated; **key-rotation runbook signed off**.
6. Success metrics baselined.
7. SOC2 audit evidence package compiled and reviewed by compliance team before Q3 audit.
8. On-call rotation active 24/7 for first 2 weeks post-GA; acknowledgment time <15 minutes for P1 alerts.
9. Feature flags removed from codebase; legacy auth endpoints marked deprecated with removal timeline (or N/A in greenfield).

**Dependencies:**

- M1-M5 all complete.
- External: Production Kubernetes cluster; monitoring infrastructure deployed; compliance team available.

**Estimated Duration:** 4 weeks (1 week Alpha + 2 weeks Beta + 1 week GA stabilization).

**Risks and Mitigations:**

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Beta reveals performance regression not caught in load testing | Medium | High | Maintain legacy auth (or 503-stub in greenfield) as fallback; rollback criteria defined; extend beta by 1 week if p95 exceeds 200ms. |
| Legacy auth system already deprecated, leaving no rollback path | Low | Critical | **Greenfield rollback branch (D6.5b) replaces legacy-restore with 503 blast-radius test** (Change #14). |
| SOC2 evidence package incomplete at audit time | Medium | Critical | Begin evidence collection from M1; review at each milestone gate; engage compliance team at M4 for pre-review. |
| 10% beta traffic insufficient to surface concurrency issues | Medium | Medium | Supplement with synthetic load; push to 25% if first week clean. |
| Key-rotation drill triggers session loss | Low | High | Rotation uses dual-key window (old + new accepted for 1 hour); verified in staging before Phase 1 (Change #6). |

---

## Cross-Cutting Concerns

### Security

<!-- Source: Base (V2 Sonnet) + Changes #2, #6, #9, #10, #13: constant-time defenses, key rotation, admin RBAC, atomic lockout -->

- **Password storage:** bcrypt cost 12 via PasswordHasher; raw passwords never persisted or logged. Verified in M1, enforced in M2.
- **Token signing:** RS256 with 2048-bit RSA keys; private key on in-memory tmpfs mount, never on disk; **quarterly rotation schedule with runbook (M3 D3.8); first drill in M6 Phase 1 Alpha** (Change #6).
- **User enumeration prevention:** ALL authentication failure paths (wrong email, wrong password, locked account, password-reset unregistered email) return identical response bodies AND identical p95 latency (±20ms). Constant-time module (D2.2) enforces dummy-hash verify on all login failure branches including lockout; reset endpoint always-enqueues email job with audit-row parity (D4.1, D4.5). Validated in M2 unit tests (timing-parity test) and M4/M5 pen-tests.
- **Account lockout:** 5 failed attempts within 15 minutes triggers 423 Locked via **atomic UPDATE keyed by email** (Change #5); response timing matches dummy-verify path (Change #2/#13 — INV-014). Lockout key = email; per-email rate limit (5 req/min) is primary brute-force defense; per-IP (10 req/min) is secondary (Change #8).
- **Admin endpoint RBAC (minimal v1.0):** `isAdmin BOOLEAN` column in users (D1.1); seeded at deploy via D1.10; JWT claim populated by D3.1; admin endpoint guard enforces `isAdmin=true` (D4.7). Full RBAC framework remains v1.1+ (Change #9 — INV-004 fix).
- **Token storage in frontend:** AuthToken stored in memory only; refresh token via HttpOnly cookie; cleared on tab close (TDD R-001).
- **CORS:** Restricted to known frontend origins.
- **TLS 1.3:** Enforced on all endpoints.
- **Penetration testing:** **Backend pen-test in M4 (RS256, lockout, timing oracles, atomic-UPDATE); frontend pen-test in M5 (XSS, CSRF, AuthProvider redirect loop)** (Change #7).
- **Redis namespace isolation:** `redis-session` (refresh tokens + lockout counters) vs `redis-queue` (BullMQ reset emails) to prevent reset-spam OOM cascading into lockout bypass (Change #11 — INV-012).

### Observability

<!-- Source: Base (V2 Sonnet) + Change #16: NTP/clock-drift monitoring -->

- **Metrics (Prometheus):** auth_login_total, auth_login_duration_seconds (histogram), auth_token_refresh_total, auth_registration_total, auth_password_reset_total{outcome}.
- **Structured logging:** All auth events as JSON with user_id, event_type, timestamp, ip_address, outcome, soc2_relevant.
- **Distributed tracing:** OpenTelemetry spans through AuthService → PasswordHasher → TokenManager → JwtService.
- **Alerting:** Login failure rate >20% over 5 min; p95 latency >500ms; TokenManager Redis connection failures; email bounce rate >5%; **pod-clock-drift alert: warn when pod-to-pod drift exceeds 2 seconds (early warning before JWT 5s skew tolerance is breached)** (Change #16 — A-002).
- **Dashboards:** Grafana dashboards for auth health; success metrics funnel dashboard.

### Testing

- **Unit (80% coverage target):** AuthService methods, PasswordHasher, JwtService sign/verify, TokenManager lifecycle, UserProfile validation, **timing-parity tests**.
- **Integration (15%):** API endpoint cycles; database operations (including atomic-UPDATE lockout under 10-parallel-pod concurrency); Redis token storage; **end-to-end always-enqueue audit-parity test**.
- **E2E (5%):** Full user journeys through LoginPage, RegisterPage, AuthProvider including redirect-loop and CSRF tests.
- **Load testing:** k6 scripts; 500 concurrent users; p95 <200ms login, <100ms refresh.

### Compliance (SOC2 Type II)

<!-- Source: Base (V2 Sonnet, modified) — Change #4: split-table resolution -->

- **Audit logging:** All auth events recorded from M1 with user_id, event_type, timestamp, IP, outcome, soc2_relevant flag.
- **Retention (resolves OQ-PRD-TDD-1):** Single audit_log table with `soc2_relevant BOOLEAN` flag. 12-month retention default; derived view exposes 90-day operational subset (TDD §7.2 alignment) without destructive migration (Change #4 — INV-002).
- **Evidence collection:** Begin from M1; compile at M6; compliance team pre-review at M4.
- **Consent recording:** GDPR consent at registration with timestamp and consent text version.
- **Data minimization:** Only email, hashed password, display name (plus isAdmin flag for minimal RBAC).
- **Password policy:** NIST SP 800-63B compliance; bcrypt cost 12; no plaintext.

### Performance Budgets

| Endpoint | p95 Target | Load Condition | Measurement |
|----------|-----------|----------------|-------------|
| POST /auth/login | <200ms | 500 concurrent | APM + k6 (timing-parity within 20ms across success/failure paths) |
| POST /auth/register | <200ms | 500 concurrent | APM + k6 |
| GET /auth/me | <200ms | 500 concurrent | APM + k6 |
| POST /auth/refresh | <100ms | 500 concurrent | APM + k6 |
| POST /auth/reset-request | <200ms | 100 concurrent | k6 (queue-saturation parity) |
| PasswordHasher.hash() | <500ms | Single operation | Benchmark in CI |
| JwtService sign/verify | <5ms | Single operation | Unit benchmark |
| TokenManager Redis ops | <10ms | Single operation | Redis latency monitoring |

---

## Risk Register

| ID | Risk | Probability | Impact | Mitigation | Owner | Traceability |
|----|------|-------------|--------|------------|-------|--------------|
| RR-1 | Low registration adoption; conversion <60% target | Medium | High | Usability testing M5; iterate on funnel analytics; A/B test form messaging. | Product + Frontend | PRD Risk Analysis |
| RR-2 | Security breach (token theft, XSS, injection) | Low | Critical | Memory-only token storage, 15-min access TTL, bcrypt cost 12, RS256 signing, CORS restrictions, backend pen-test M4, frontend pen-test M5; no P0 findings allowed for GA gate. | Security + Auth-team | PRD Risk Analysis; TDD R-001 |
| RR-3 | SOC2 compliance failure from incomplete audit logging | Medium | High | Audit logging from M1; soc2_relevant flag for retention split; 12-month retention; compliance pre-review at M4. | Compliance + Auth-team | PRD Risk Analysis |
| RR-4 | Email delivery failures block password reset | Low | Medium | Async dispatch; >5% bounce alert; documented fallback support channel. | Auth-team + Infra | PRD Risk; SendGrid dependency |
| RR-5 | Redis unavailability causes session invalidation or refresh failures | Medium | High | Multi-AZ Redis from M1 (Change #15); namespace isolation (Change #11); graceful degradation; runbook for failover. | Platform + Auth-team | TDD R-003; INV-012 |
| RR-6 | Concurrent token refresh race | Medium | Medium | Redis MULTI/EXEC atomicity; first refresh wins; documented as expected behavior. | Auth-team | TDD Section 12; INV-010 |
| RR-7 | bcrypt cost 12 exceeds 500ms budget | Low | Medium | Profile on CI + staging in M1; negotiate cost 11 with security if needed. | Auth-team | TDD Section 17 |
| RR-8 | Rollback to legacy auth fails during beta emergency | Low | Critical | **Branched rollback (D6.5): legacy-restore OR greenfield 503-blast-radius drill** (Change #14); validate topology in Phase 1. | Auth-team + Platform | TDD Section 19.3; A-007 |
| RR-9 | Timing oracle from lockout-rejected path responding faster than dummy-verify path | Medium | High | D2.2 enforces dummy-verify on lockout path (INV-014); D2.8 timing-parity test in CI; pen-test in M4 verifies. | Sec-reviewer + Auth-team | INV-014; Change #2/#13 |
| RR-10 | Admin endpoint privilege-escalation via missing RBAC | Low | Critical | Minimal admin RBAC via isAdmin column + JWT claim (Change #9); D4.7 enforces 403 without claim; integration test in D4.8. | Auth-team + Security | INV-004 |
| RR-11 | Admin audit query becomes enumeration oracle via row-absence | Low | High | Worker emits audit row for ALL requests (including drops) with opaque request_id (Change #10); D4.8 integration test verifies. | Auth-team | INV-007 |
| RR-12 | Atomic-lockout SQL pattern misimplemented under multi-pod scale | Low | High | 10-parallel-pod CI test enforced (D2.9); SQL pattern reviewed by DB lead (Change #5). | Auth-team + DB lead | INV-009, INV-013 |
| RR-13 | Pen-test discovers high-severity finding close to GA | Medium | High | Backend pen-test in M4 with 1-week M5 buffer; frontend pen-test in M5 Week 2 with 1-week remediation buffer (Change #7); SOC2 deadline is Q3 — room exists to delay 1 sprint. | Sec-reviewer | V1 R-010 |

---

## Definition of Done

### Per Milestone

1. All deliverables for the milestone are implemented and code-reviewed.
2. All acceptance criteria for the milestone pass with automated test evidence.
3. Unit test coverage for new code exceeds 80%.
4. Integration tests pass against real PostgreSQL and Redis.
5. Audit log events for all new state transitions are emitted and verified.
6. No P0 or P1 bugs open against the milestone scope.
7. Performance targets validated (p95 <200ms under load; timing-parity ±20ms where applicable).
8. Security review checkpoint signed off by sec-reviewer (lightweight at M1/M2/M3, backend-pen-test gate at M4, frontend-pen-test gate at M5).

### Overall (Release Gate)

1. All FR-AUTH-001 through FR-AUTH-005 implemented and verified.
2. Unit test coverage for AuthService, TokenManager, JwtService, PasswordHasher exceeds 80%.
3. Integration tests for all API endpoints pass against real PostgreSQL and Redis.
4. Security review complete: bcrypt cost verified, RS256 key-rotation runbook signed off + first drill executed, **backend pen-test (M4) and frontend pen-test (M5) both zero-P0**.
5. Performance testing confirms all endpoints meet <200ms p95 latency under 500 concurrent users; timing-parity within 20ms across login failure paths.
6. E2E tests cover all 8 user journey scenarios.
7. Runbooks (including key-rotation, branched-rollback) reviewed and published.
8. Monitoring dashboards verified, including NTP/clock-drift alert.
9. Rollback procedure tested in staging via topology-appropriate branch.
10. 99.9% uptime sustained over 7 days in production.
11. SOC2 audit evidence package compiled and reviewed by compliance (Q3 2026 readiness).

---

## Open Questions and Assumptions

### Open Questions (from PRD and TDD)

<!-- Source: Base (V2 Sonnet) + Change #4: OQ-PRD-TDD-1 added -->

| ID | Question | Owner | Target Resolution | Impact on Roadmap |
|----|----------|-------|-------------------|-------------------|
| OQ-PRD-1 | Should password reset emails be sent synchronously or asynchronously? | Engineering | Before M4 | Resolved: async via BullMQ on `redis-queue` namespace (D4.5). |
| OQ-PRD-2 | Maximum number of refresh tokens per user across devices? | Product | Before M3 | Assumed unlimited within 7-day TTL window in v1.0; revisit if Redis memory exceeds plan. |
| OQ-PRD-3 | Account lockout policy: auto-unlock after window, or admin-only? | Security | Before M2 | Resolved: auto-unlock after 15-minute window via atomic-UPDATE SQL (D2.1). |
| OQ-PRD-4 | Should "remember me" extend session beyond 7 days? | Product | Before M5 | Deferred to v1.1. |
| OQ-TDD-1 | Should AuthService support API key authentication for service-to-service calls? | test-lead | Deferred to v1.1 | No v1.0 impact. |
| OQ-TDD-2 | Maximum allowed UserProfile roles array length? | auth-team | Before M2 | Assumed 16 entries with DB CHECK constraint. |
| **OQ-PRD-TDD-1** | **Audit-log retention conflict: PRD requires 12-month SOC2 retention; TDD §7.2 specifies 90-day on `auth_audit_log` table** <!-- Change #4 (INV-002) --> | **compliance-lead** | **M1 schema design (resolved)** | **Resolved via D1.2: single table with `soc2_relevant BOOLEAN` flag; 12-month physical retention; 90-day operational view derived in M6 evidence pack. No destructive migration required.** |

### Assumptions

1. PostgreSQL 15+ multi-AZ provisioned before M1 begins (PRD Assumptions; Change #15).
2. Redis 7+ multi-AZ provisioned with two namespaces (`redis-session`, `redis-queue`) before M1 begins (Change #11, #15).
3. SendGrid API credentials and approved sender domain configured before M4.
4. Frontend routing framework supports client-side token-based authentication.
5. Security policy SEC-POLICY-001 defines password and token parameters before M2.
6. Node.js 20 LTS is the runtime environment.
7. Greenfield-vs-legacy deployment topology determined at M6 Phase 1 kickoff (Change #14).
8. Email/password only in v1.0; no OAuth, social login, or MFA.
9. The API Gateway supports per-IP and per-email rate limiting (Change #8).
10. Production Kubernetes cluster supports HPA for AuthService.
11. NTP synchronization in place; pod-to-pod clock drift <2s under normal conditions (Change #16).

---

## Sequencing Rationale (architect's note)

<!-- Source: V1 Opus, L476-484 — merged per Change #1, with V1→V2 milestone-number translation -->

The dependency chain is **data → service → tokens → reset → frontend → rollout**, not a parallelizable matrix. Key non-obvious sequencing decisions:

1. **Audit log lands in M1, not M6.** SOC2 controls are not features; retrofitting audit emission across six endpoints under audit pressure is the textbook failure mode. Cost in M1 is ~2 days; cost in M6 would be a rollout slip. The `soc2_relevant` flag (Change #4) is added at M1 schema time, not M6, to avoid destructive migration.

2. **Lockout counter atomicity on Postgres from M2 (not Redis), but Redis multi-AZ + namespace isolation provisioned at M1.** Atomic counter accuracy is a SOC2 control: V2's PG-column approach with single-statement UPDATE (Change #5) is equally valid to V1's Redis-INCR and avoids M1 Redis-dependency for lockout. Redis is still provisioned at M1 because refresh tokens and BullMQ depend on it, but lockout lives in the users table.

3. **M3 freezes the API contract (D3.9) before M5 starts.** Frontend (M5) and backend (M4) can run in parallel after M3 if the OpenAPI spec is locked at M3 close. This recovers ~1 sprint from a naive serial plan and is why the M4 backend-pen-test gate doesn't block M5 scaffolding.

4. **Backend pen-test in M4, frontend pen-test in M5 (not a single M5 pen-test).** A late security finding that blocks GA is the single highest-impact schedule risk (RR-13). Splitting pen-tests by surface (Change #7) gives backend findings 2 weeks of cure time before GA and ensures frontend has a complete UI to test against. Booking pen-test in M5-only (V1 original) gave insufficient cure time; booking entirely in M4 (V1's R-010 single-test plan) had no frontend to test.

5. **Constant-time anti-enumeration in M2 (login) and M4 (reset).** Both endpoints (login on unknown email, login on locked account, reset on unregistered email) must execute the same code paths regardless of registration/state, or the timing side-channel re-introduces the enumeration vulnerability the PRD explicitly prohibits. M2 D2.2 covers login paths (constant dummy-verify on unknown email AND lockout-rejected — INV-014 fix); M4 D4.1/D4.5 cover reset (always-enqueue with audit-row parity — INV-007 fix). The dummy-hash constant is provisioned at build time (M1 D1.9) so it's identical across pods (INV-001 fix).

6. **Minimal admin RBAC at M1 (isAdmin column + seed), JWT claim at M3, endpoint guard at M4.** Without minimal admin enforcement (Change #9), the M4 admin endpoint is a privilege-escalation surface (INV-004). Full RBAC framework remains v1.1+; v1.0 ships single-bit gating sufficient for SOC2 admin audit query access.

---

<!--
=== MERGE STATUS ===
All 18 planned changes from refactor-plan.md applied.
Invariant fixes: INV-001, INV-002, INV-004, INV-005, INV-007, INV-009, INV-011, INV-012, INV-013, INV-014 addressed.
INV-010 promoted to acceptance criterion (D3.11, M3 AC #12).
INV-003 partial mitigation in D2.3 (race-loser audit row).
MEDIUM-severity unaddressed: INV-006 (DKIM rotation coordination), INV-008 (90-day retention boundary), INV-015 (queue-saturation timing variance), INV-016 (table-split admin-endpoint retrofit risk — partially mitigated by Change #4's view-based split).
-->
