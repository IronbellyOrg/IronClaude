# 04 -- Task Decomposition Granularity: Baseline vs TDD+PRD Enriched Tasklists

**Status**: Complete
**Investigation type:** Pattern Investigator
**Date:** 2026-04-02
**Analyst:** Claude Opus 4.6

## Methodology

Compared task decomposition across three equivalent functional areas between the spec-baseline (test3, 5 phases, 87 tasks) and the TDD+PRD enriched (test1, 3 phases, 44 tasks). For each area, extracted task titles, summarized content, counted tasks, and measured lines per task. Identified consolidation patterns and assessed completeness at coarser granularity.

**Files analyzed:**
- Baseline: `.dev/test-fixtures/results/test3-spec-baseline/phase-{1..5}-tasklist.md`
- TDD+PRD: `.dev/test-fixtures/results/test1-tdd-prd-v2/phase-{1..3}-tasklist.md`

---

## Area A: Login/Authentication Implementation

### Baseline Decomposition

The baseline splits login/authentication across **12+ tasks** spanning 3 phases:

| Task ID | Title | Phase | Lines (approx) | Content Focus |
|---------|-------|-------|-----------------|---------------|
| T01.04 | Implement PasswordHasher class | 1 | 33 | bcrypt hash/verify methods, configurable cost |
| T01.05 | Implement password policy validator | 1 | 30 | Min 8 chars, 1 upper, 1 lower, 1 digit |
| T01.06 | Configure bcrypt cost factor 12 | 1 | 28 | Config entry with env var override |
| T01.07 | Unit tests for PasswordHasher and policy | 1 | 30 | Hash timing ~250ms, round-trip, policy edge cases |
| T01.08 | Implement JwtService class | 1 | 33 | RS256 sign/verify, algorithm lock |
| T01.09 | RS256 key pair loading from secrets manager | 1 | 33 | Key loading module, 4096-bit, dev fallback |
| T01.10 | Access token TTL configuration (15 minutes) | 1 | 27 | Config entry, env var, default 15m |
| T01.11 | Unit tests for JwtService | 1 | 29 | Round-trip, expired, tampered, wrong algorithm |
| T02.08 | Implement AuthService.login() | 2 | 32 | Verify creds, issue tokens, 401/403, timing side-channel |
| T02.13 | Rate limiter for login endpoint | 2 | 30 | 5 attempts/min/IP, in-memory sliding window |
| T03.05 | POST /auth/login route | 3 | 33 | Route handler, rate-limited, cookie setting |
| T03.12 | Integration test: full login flow | 3 | 28 | Register->login->profile E2E test |

**Total: 12 tasks, ~366 lines**

### TDD+PRD Decomposition

The TDD+PRD version covers the same login functionality in **5 tasks**, all in Phase 1:

| Task ID | Title | Phase | Lines (approx) | Content Focus |
|---------|-------|-------|-----------------|---------------|
| T01.06 | Implement PasswordHasher Component | 1 | 46 | bcrypt cost 12, abstract interface, timing invariance, hash/verify, future argon2id migration path |
| T01.07 | Implement JwtService Component | 1 | 44 | RS256 sign/verify, 2048-bit RSA, 5-second clock skew, config validation |
| T01.10 | Implement AuthService Facade | 1 | 46 | Central orchestrator, login flow, registration flow, constructor DI, audit log callback |
| T01.12 | Implement POST /auth/login Endpoint | 1 | 40 | Endpoint handler + account lockout (Redis counter, 5 failures in 15 min -> 423) + rate limiting (10 req/min/IP) |
| T01.27 | Execute Manual Testing and Bug Fix | 1 | ~40 | 13 test scenarios including login valid/invalid/lockout |

**Total: 5 core tasks, ~216 lines**

### Consolidation Pattern (Area A)

| Baseline Tasks | Consolidated Into (TDD+PRD) | Ratio |
|---|---|---|
| T01.04 + T01.05 + T01.06 + T01.07 (PasswordHasher + policy + config + tests) | T01.06 (PasswordHasher Component) | 4:1 |
| T01.08 + T01.09 + T01.10 + T01.11 (JwtService + keys + TTL + tests) | T01.07 (JwtService Component) | 4:1 |
| T02.08 (AuthService.login) | T01.10 (AuthService Facade -- login is one of several flows) | included |
| T02.13 + T03.05 (rate limiter + login route) | T01.12 (POST /auth/login -- includes lockout + rate limit) | 2:1 |
| T03.12 (Integration test: full login) | T01.27 (Manual Testing -- 13 scenarios) | absorbed |

**Effective ratio: ~12 baseline tasks -> 5 TDD+PRD tasks (2.4:1)**

---

## Area B: Password Reset

### Baseline Decomposition

The baseline splits password reset across **5 tasks** in Phases 2-3:

| Task ID | Title | Phase | Lines (approx) | Content Focus |
|---------|-------|-------|-----------------|---------------|
| T02.11 | Implement AuthService.requestPasswordReset() | 2 | 34 | Generate reset token (1hr TTL), dispatch email synchronously, always return 200 |
| T02.12 | Implement AuthService.resetPassword() | 2 | 33 | Validate token, update hash, invalidate token, revoke all refresh tokens, atomic |
| T03.09 | POST /auth/password-reset/request route | 3 | 26 | Route handler, always 200, anti-enumeration |
| T03.10 | POST /auth/password-reset/confirm route | 3 | 26 | Route handler, 200 success, 400 expired/invalid |
| T03.14 | Integration test: password reset lifecycle | 3 | 30 | E2E: request reset -> confirm -> login new password -> old tokens invalidated |

**Total: 5 tasks, ~149 lines**

### TDD+PRD Decomposition

The TDD+PRD version covers password reset in **3 tasks** in Phase 2:

| Task ID | Title | Phase | Lines (approx) | Content Focus |
|---------|-------|-------|-----------------|---------------|
| T02.01 | Implement POST /auth/reset-request Endpoint | 2 | 48 | Full endpoint: generate token (1hr TTL, single-use), queue email via SendGrid, no enumeration, monitoring + alerting |
| T02.02 | Implement POST /auth/reset-confirm Endpoint | 2 | 36 | Full endpoint: validate token, hash new password, invalidate all refresh tokens, audit log |
| T02.03 | Integrate SendGrid Email Service | 2 | 42 | Async queue, delivery monitoring, alerting, fallback support channel |

**Total: 3 tasks, ~126 lines**

### Consolidation Pattern (Area B)

| Baseline Tasks | Consolidated Into (TDD+PRD) | Ratio |
|---|---|---|
| T02.11 (requestPasswordReset logic) + T03.09 (route handler) | T02.01 (full reset-request endpoint) | 2:1 |
| T02.12 (resetPassword logic) + T03.10 (route handler) | T02.02 (full reset-confirm endpoint) | 2:1 |
| (no equivalent) | T02.03 (SendGrid integration -- net new scope) | 0:1 (new) |
| T03.14 (Integration test lifecycle) | Absorbed into verification steps of T02.01 and T02.02 | absorbed |

**Effective ratio: 5 baseline tasks -> 2 core TDD+PRD tasks (2.5:1)**

The TDD+PRD version merges the service-layer logic and route-handler into a single vertical task, but adds a new task (SendGrid integration) that the baseline does not have at all.

---

## Area C: Testing/QA

### Baseline Decomposition

The baseline has extensive dedicated test tasks across Phases 1-4:

| Task ID | Title | Phase | Lines (approx) | Content Focus |
|---------|-------|-------|-----------------|---------------|
| T01.03 | Verify all migrations are reversible | 1 | 24 | Automated up/down migration cycle test |
| T01.07 | Unit tests for PasswordHasher and policy | 1 | 30 | Hash timing, round-trip, policy boundaries |
| T01.11 | Unit tests for JwtService | 1 | 29 | Sign/verify, expired, tampered, wrong algo |
| T01.15 | Security engineer code review | 1 | 33 | Crypto review sign-off document |
| T02.07 | Unit tests for TokenManager | 2 | 28 | Issue, rotate, replay, expiry, cap, cookie (6 cases) |
| T02.14 | Unit tests for AuthService (all 5 flows) | 2 | 30 | Min 15 test cases across 5 flows |
| T03.04 | Unit tests for auth middleware | 3 | 24 | Valid/invalid/missing token (3 cases) |
| T03.12 | Integration test: full login flow | 3 | 28 | Register->login->profile E2E |
| T03.13 | Integration test: token refresh with rotation | 3 | 29 | Login->refresh->new token->old rejected |
| T03.14 | Integration test: password reset lifecycle | 3 | 30 | Request->confirm->login new pw->old tokens invalid |
| T03.15 | Integration test: sensitive field filtering | 3 | 26 | Scan all responses for password_hash, token_hash |
| T03.16 | Integration test: rate limiting enforcement | 3 | 25 | 6 login attempts, verify 429 on 6th |
| T03.17 | E2E lifecycle test: full user journey | 3 | 30 | Register->login->profile->refresh->reset->re-login |
| T04.04 | Benchmark bcrypt cost factor 12 timing | 4 | 24 | 200-400ms assertion |
| T04.05 | Security test: replay detection | 4 | 28 | Adversarial replay triggers full revocation |
| T04.06 | Security test: XSS prevention (httpOnly) | 4 | 26 | Refresh token only in Set-Cookie with httpOnly |
| T04.07 | Security test: information leakage | 4 | 26 | Generic 401, no email/password differentiation |
| T04.08 | Security test: JWT validation failure modes | 4 | 26 | Tampered, expired, invalid sig, algo none |
| T04.09 | Security test: sensitive field exclusion scan | 4 | 26 | All endpoints scanned for forbidden fields |
| T04.10 | Security test: password policy enforcement | 4 | 26 | 7-char fail, 8-char pass, missing each class |
| T04.11 | Security test: no plaintext passwords stored | 4 | 24 | DB audit confirms bcrypt format |
| T04.12 | Security test: RS256 key size (4096-bit) | 4 | 22 | Key inspection, 4096 bits exactly |
| T04.13 | Security test: cookie attributes | 4 | 22 | HttpOnly, Secure, SameSite=Strict |
| T04.14 | Measure and enforce line coverage >= 90% | 4 | 26 | Coverage config, CI threshold |
| T04.15 | Measure and enforce branch coverage >= 85% | 4 | 26 | Branch coverage, gap analysis |
| T04.16 | Critical path coverage >= 95% | 4 | 24 | Login, refresh, reset path coverage |
| T04.17 | Test AUTH_SERVICE_ENABLED=false behavior | 4 | 24 | Flag disabled -> 503/404, non-auth unaffected |
| T04.18 | Test database down-migrations | 4 | 24 | Repeat migration rollback test |

**Total: 28 dedicated test/QA tasks, ~731 lines**

### TDD+PRD Decomposition

The TDD+PRD version has far fewer standalone test tasks because testing is **embedded within implementation tasks** as verification steps:

| Task ID | Title | Phase | Lines (approx) | Content Focus |
|---------|-------|-------|-----------------|---------------|
| T01.26 | Execute Security Checkpoint Review | 1 | 38 | Security review of crypto components, bcrypt timing, HttpOnly, no plaintext passwords |
| T01.27 | Execute Manual Testing and Bug Fix | 1 | ~40 | 13 test scenarios, 2-day bug fix window, E2E lifecycle |
| T02.05 | Complete Compliance and Audit Readiness | 2 | 36 | SOC2 validation, GDPR consent, audit log spot-check |
| T02.08 | Execute Load Testing and Performance Validation | 2 | 38 | k6: 500 concurrent logins, sustained 100 req/sec, token refresh under load |
| T03.01 | Execute Pre-GA Security Gate and Penetration Testing | 3 | 40 | External pentest, NIST 800-63B, data minimization, HttpOnly cross-browser |

**Total: 5 dedicated test/QA tasks, ~192 lines**

However, each implementation task in TDD+PRD includes a **[VERIFICATION]** step with specific test criteria. For example, T01.12 (POST /auth/login) includes: "API tests: valid login -> 200, invalid -> 401, lockout after 5 -> 423, rate limit -> 429". This embeds testing directly into the implementation task.

### Consolidation Pattern (Area C)

| Baseline Approach | TDD+PRD Approach | Ratio |
|---|---|---|
| 28 standalone test tasks | 5 standalone + embedded verification in ~20 implementation tasks | 28:5 standalone (5.6:1) |
| Separate unit test tasks per component (T01.07, T01.11, T02.07, T02.14) | Tests embedded in component tasks as [VERIFICATION] steps | 4:0 standalone |
| Separate integration test tasks (T03.12-T03.17) | Manual testing task (T01.27) covers 13 scenarios | 6:1 |
| 9 dedicated security test tasks (T04.05-T04.13) | 2 security review tasks (T01.26, T03.01) | 9:2 |
| 3 coverage enforcement tasks (T04.14-T04.16) | No standalone coverage tasks | 3:0 |

---

## Decomposition Projection: If TDD+PRD Were Decomposed to Baseline Granularity

To estimate how many tasks the TDD+PRD version would produce at baseline granularity:

| TDD+PRD Task | Baseline-Equivalent Task Count | Rationale |
|---|---|---|
| T01.01 (Provision PostgreSQL + GDPR + audit) | 3 | Baseline has separate users table, refresh tokens table, and reversibility test |
| T01.02 (Redis cluster) | 1 | No baseline equivalent (baseline uses DB, not Redis) |
| T01.03 (Feature flags) | 3 | Baseline has flag implementation, disabled behavior, rollback test |
| T01.04 (RS256 key pair) | 2 | Key generation + secrets loading |
| T01.06 (PasswordHasher) | 4 | Class + policy + config + unit tests |
| T01.07 (JwtService) | 4 | Class + key loading + TTL config + unit tests |
| T01.08 (TokenManager) | 6 | Class + rotation + hash storage + TTL + max tokens + unit tests |
| T01.10 (AuthService facade) | 5 | Login + register + getProfile + unit tests (5 flows) + feature flag |
| T01.12 (POST /auth/login) | 3 | Route handler + rate limiter + middleware unit test |
| T01.13 (POST /auth/register) | 2 | Route handler + GDPR validation |
| T01.14 (POST /auth/refresh) | 2 | Route handler + cookie extraction |
| T01.17 (Audit logging) | 1 | No baseline equivalent at this scope |
| T01.18-T01.22 (Frontend + routes) | 0 baseline equiv | Baseline has no frontend tasks |
| T01.23 (Gateway rate limiting) | 1 | Baseline rate limiter is per-endpoint already |
| T01.25 (Monitoring) | 2 | APM integration + uptime monitoring |
| T01.26 (Security review) | 1 | Security engineer code review |
| T01.27 (Manual testing) | 7 | Would split into 6 integration tests + E2E test |
| T02.01-T02.02 (Password reset) | 4 | Service logic (2) + route handlers (2) |
| T02.03 (SendGrid) | 0 baseline equiv | Baseline has no email service task |
| T02.06-T02.09 (Deploy + beta + load) | 5 | k6 login + refresh + registration + benchmark + rollout strategy |
| T03.01 (Pentest) | 9 | Would split into 9 individual security tests |
| T03.02-T03.08 (GA + deprecate + docs) | 8 | Rollback, health, docs, runbooks, diagrams, etc. |

**Projected total: ~73 tasks at baseline granularity (vs. 44 actual TDD+PRD tasks)**

This is fewer than the baseline's 87 because:
1. The TDD+PRD version has genuinely different scope (frontend, Redis, GDPR, SendGrid) that creates some tasks the baseline lacks
2. But it also omits scope the baseline has (Phase 5 production readiness, secrets manager integration, key rotation, extensive alerting)

---

## Completeness Assessment: Is Coarser Granularity Genuinely Complete?

### Evidence of Completeness

1. **Embedded verification steps**: Every TDD+PRD implementation task includes explicit [VERIFICATION] steps with specific test scenarios. T01.12 lists 4 test scenarios inline. This is not "testing deferred" -- it is testing co-located with implementation.

2. **Richer acceptance criteria**: TDD+PRD tasks reference specific TDD section numbers (e.g., "TDD S8"), PRD section numbers (e.g., "PRD S22"), persona names (Alex, Sam, Jordan), and gap IDs (GAP-001 through GAP-004). The baseline references spec requirement IDs (FR-AUTH.1, NFR-AUTH.3) but not personas or user journeys.

3. **Subtask decomposition for XL tasks**: T02.07 (Beta 10% Traffic) explicitly lists subtasks T02.07a-T02.07d, showing the TDD+PRD version decomposes XL tasks when needed.

### Evidence of Missing Decomposition

1. **No standalone unit test tasks**: The baseline's explicit unit test tasks (T01.07, T01.11, T02.07, T02.14, T03.04) have no TDD+PRD equivalents. Testing is embedded in verification steps but never called out as independent deliverables. Risk: a developer might skip tests if they complete the "execution" steps and consider the task done.

2. **No coverage enforcement tasks**: The baseline has 3 tasks (T04.14-T04.16) for 90% line, 85% branch, and 95% critical path coverage. The TDD+PRD version has no equivalent. Coverage enforcement could fall through the cracks.

3. **Fewer security-specific tests**: Baseline has 9 individual security test tasks. TDD+PRD has 2 review tasks that cover the same ground at a higher level but with less granular tracking. Items like "verify RS256 key size is exactly 4096 bits" (baseline T04.12) are a checklist item in TDD+PRD T01.26 rather than a trackable task.

4. **Production readiness gap**: The baseline's Phase 5 (15 tasks covering secrets management, key rotation, alerting, CI pipeline, documentation) has only partial coverage in TDD+PRD Phase 3 (8 tasks covering GA rollout, deprecation, docs, stabilization). Monitoring alerts, CI pipeline configuration, and key rotation are either embedded or absent.

---

## Comparison Summary Table

| Dimension | Baseline (test3) | TDD+PRD (test1) | Delta |
|---|---|---|---|
| Total phases | 5 | 3 | -2 |
| Total tasks | 87 | 44 | -43 (-49%) |
| Login/auth tasks | 12 | 5 | -7 (2.4:1 ratio) |
| Password reset tasks | 5 | 3 | -2 (1.7:1 ratio) |
| Testing/QA standalone tasks | 28 | 5 | -23 (5.6:1 ratio) |
| Avg lines per task | ~27 | ~38 | +11 (+41%) |
| Embedded test scenarios | Rarely | Always (every [VERIFICATION] step) | Structural diff |
| Persona references | None | Throughout (Alex, Sam, Jordan) | TDD+PRD advantage |
| Spec traceability style | Requirement IDs (FR-AUTH.1) | TDD sections + PRD sections + Requirement IDs | TDD+PRD richer |
| Frontend scope | None | 5 tasks (LoginPage, RegisterPage, AuthProvider, ProfilePage, routes) | TDD+PRD broader |
| Production readiness | 15 dedicated tasks (Phase 5) | ~3 tasks (embedded in Phase 3) | Baseline more thorough |

---

## Gaps and Questions

1. **Is embedded testing sufficient?** The TDD+PRD version never produces a standalone test suite task. If an executor treats [VERIFICATION] steps as optional, coverage could suffer. The baseline's standalone test tasks make testing an undeniable, separately tracked obligation. Which model leads to better actual test coverage in execution?

2. **Coverage metrics are absent from TDD+PRD.** The baseline explicitly mandates 90% line, 85% branch, and 95% critical path coverage as tracked tasks. The TDD+PRD version has no equivalent. Is this an intentional omission (coverage is assumed) or a gap?

3. **Security test granularity tradeoff.** Baseline's 9 individual security tests (cookie attributes, replay detection, XSS prevention, etc.) make each verifiable independently. TDD+PRD's T01.26 (security checkpoint) and T03.01 (pentest) consolidate them. If a pentest firm covers them, this may be superior. If done internally, the baseline's granularity is more actionable.

4. **Frontend scope disparity.** The TDD+PRD version includes 5 frontend tasks (LoginPage, RegisterPage, AuthProvider, ProfilePage, route protection) that have zero baseline equivalents. This is not a decomposition difference -- it is a scope difference driven by the PRD enrichment. How should we account for this when comparing task counts?

5. **Projected decomposition accuracy.** The 73-task projection for TDD+PRD at baseline granularity is approximate. Some TDD+PRD tasks bundle genuinely distinct work (e.g., T01.01 bundles UserProfile schema + audit log table + GDPR fields + retention policy) that the baseline rightfully separates. Is the TDD+PRD bundling a strength (holistic delivery) or a risk (too much in one task)?

6. **Phase 5 equivalent.** The baseline's Phase 5 (production readiness: secrets manager, key rotation, CI pipeline, rollout strategy, runbooks, OpenAPI spec, sequence diagrams, threat model) is partially covered by TDD+PRD Phase 3 but with significant omissions. Is Phase 5 scope captured elsewhere in the TDD+PRD pipeline (e.g., in the roadmap but not the tasklist)?

---

## Summary

The TDD+PRD enriched tasklist operates at roughly **2-3x coarser granularity** than the baseline for implementation tasks and **5-6x coarser** for testing/QA tasks. This is achieved through two primary consolidation patterns:

1. **Vertical integration**: Where the baseline separates service logic, route handler, and configuration into distinct tasks, TDD+PRD bundles them into a single "implement endpoint" task that spans the full stack vertically. Example: password reset request (baseline 2 tasks -> TDD+PRD 1 task).

2. **Testing absorption**: Where the baseline creates standalone test tasks, TDD+PRD embeds testing as [VERIFICATION] steps within implementation tasks. This eliminates 23 standalone test tasks but shifts testing from a tracked deliverable to an embedded obligation.

The TDD+PRD tasks are individually **41% longer** (averaging ~38 lines vs ~27 lines) because each task contains what the baseline distributes across multiple tasks. This is genuinely more complete at the task level -- each TDD+PRD task includes its own acceptance criteria, verification steps, persona context, and spec traceability -- but it also means each task has a wider blast radius if it fails or stalls.

The key finding is that the consolidation is **not uniform**. Implementation tasks consolidate at 2-3:1, which appears healthy and reduces overhead. Testing tasks consolidate at 5-6:1, which is more aggressive and carries risk that coverage enforcement and security verification may lack the granular tracking the baseline provides.
