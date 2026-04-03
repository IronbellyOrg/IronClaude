---
spec_source: "test-tdd-user-auth.md"
prd_source: "test-prd-user-auth.md"
complexity_score: 0.55
complexity_class: "MEDIUM"
primary_persona: architect
roadmap_version: "1.0"
generated: "2026-04-03T00:00:00Z"
---

# User Authentication Service — Project Roadmap (v1.0)

**Scope:** Stateless REST API for user registration, login, session management, and password reset.
**Complexity:** MEDIUM (0.55) — well-bounded scope with elevated security concerns and phased rollout strategy.
**Timeline:** 4 weeks (Alpha 1 week + Beta 2 weeks + GA 1 week)
**Risk Level:** MEDIUM — token theft, brute-force attacks, audit log compliance gaps.

---

## Executive Summary

The User Authentication Service is a prerequisite for all Q2–Q3 2026 personalization features and SOC2 Type II compliance. This roadmap phases the implementation across three stages:

1. **Phase 1 (Internal Alpha):** Deploy all core components (`AuthService`, `TokenManager`, `JwtService`, `PasswordHasher`, `UserRepo`) to staging. Manual testing of FR-AUTH-001 through FR-AUTH-005. Feature-flagged behind `AUTH_NEW_LOGIN`.

2. **Phase 2 (Beta):** Release to 10% of production traffic. Monitor latency, error rates, Redis usage against success criteria. Validate NFR-PERF-001 (< 200ms p95) and NFR-REL-001 (99.9% uptime).

3. **Phase 3 (GA):** Remove feature flags, deprecate legacy auth, enable `AUTH_TOKEN_REFRESH` for full token refresh flow.

**Business Value:** Unblocks ~$2.4M in annual revenue from personalization features. Enables SOC2 audit trail and compliance with GDPR consent and audit logging requirements (NFR-COMP-001, NFR-COMP-002, NFR-COMP-003).

**Key Deliverables:**
- 5 API endpoints (POST `/auth/login`, `/auth/register`, `/auth/refresh`, GET `/auth/me`, POST `/auth/reset-request`, `/auth/reset-confirm`)
- Stateless token-based session management with dual-token lifecycle (15-min access, 7-day refresh)
- Password reset flow with email delivery
- 12-month audit log (PRD requirement overrides TDD's 90-day retention)
- Production-ready monitoring, runbooks, and on-call support

**Architecture Persona Priorities:**
- Stateless API: no server-side session storage (constraint from extraction)
- Security-first token handling: XSS mitigation via memory-only access tokens + HttpOnly refresh cookies
- Phased rollout with automatic rollback triggers
- Integration point enumeration to avoid wiring gaps

---

## Phased Implementation Plan

### Phase 1: Internal Alpha (Week 1)

**Goal:** Deploy all backend and frontend components to staging. Pass manual QA. Zero P0/P1 bugs.

#### 1.1 Component Implementation (3–4 days)

| Component | Owner | Deliverable | Acceptance |
|-----------|-------|-------------|-----------|
| `PasswordHasher` | auth-team | bcryptjs abstraction with cost factor 12 | Unit tests: hash/verify operations, timing invariance |
| `JwtService` | auth-team | RS256 signing service with 2048-bit keys | Unit tests: sign/verify, token structure, clock skew tolerance |
| `TokenManager` | auth-team | Refresh token issuance, validation, revocation via Redis | Unit tests: token lifecycle, Redis TTL, revocation queries |
| `UserRepo` | auth-team | `UserProfile` CRUD to PostgreSQL | Integration tests: insert, query, unique email constraint |
| `AuthService` | auth-team | Facade orchestrating login, registration, profile, password reset | Integration tests: full flows, error handling, feature flag gates |

**Wiring Task 1.1.1: Password Hashing Strategy Registry**
- **Named Artifact:** `PasswordHasher` abstraction
- **Wired Components:** bcryptjs implementation (cost 12); future argon2id slot reserved
- **Owning Phase:** Phase 1
- **Cross-Reference:** FR-AUTH-001 (login), FR-AUTH-002 (registration), FR-AUTH-005 (password reset)
- **Implementation Detail:** Abstraction layer in `PasswordHasher` delegates to pluggable strategy. Default: bcryptjs. Migration path to argon2id does not require API changes.

**Wiring Task 1.1.2: Token Dispatch Table**
- **Named Artifact:** `TokenManager` internal dispatch for token type handling
- **Wired Components:** Access token flow → `JwtService.sign()`, refresh token flow → Redis storage
- **Owning Phase:** Phase 1
- **Cross-Reference:** FR-AUTH-003 (token issuance and refresh)
- **Implementation Detail:** Internal routing logic determines whether to issue new tokens or validate refresh tokens. No explicit registry; determined by request parameter inspection.

**Wiring Task 1.1.3: Account Lockout Strategy**
- **Named Artifact:** Lockout enforcement in `AuthService.login()`
- **Wired Components:** Failed attempt counter (in-memory or Redis), 15-minute TTL per IP/email combination
- **Owning Phase:** Phase 1
- **Cross-Reference:** FR-AUTH-001 AC #4 (lockout after 5 failures)
- **Implementation Detail:** Each failed login attempt increments counter; 6th attempt within 15 minutes triggers 423 Locked response. Counter expires via Redis TTL.

#### 1.2 Frontend Implementation (2–3 days)

| Component | Owner | Deliverable | Acceptance |
|-----------|-------|-------------|-----------|
| `LoginPage` | frontend-team | Email/password form; calls POST `/auth/login`; token storage via `AuthProvider` | Component test: form submission, error display, redirect on success |
| `RegisterPage` | frontend-team | Registration form with client-side validation; calls POST `/auth/register` | Component test: email/password/displayName validation, duplicate email handling |
| `AuthProvider` | frontend-team | Context provider managing `AuthToken` state, silent refresh, 401 interception | Unit test: token refresh logic, 401 handling, user context exposure |
| Route protection | frontend-team | Protected routes redirecting unauthenticated users to `LoginPage` | Routing test: protected access denied without auth, redirects to login |

**Wiring Task 1.2.1: Silent Token Refresh Middleware Chain**
- **Named Artifact:** `AuthProvider` refresh interceptor
- **Wired Components:** HTTP client interceptor → detects 401 → calls POST `/auth/refresh` → retries original request → updates context
- **Owning Phase:** Phase 1
- **Cross-Reference:** FR-AUTH-003 (token refresh), JTBD-2 (session persistence)
- **Implementation Detail:** Middleware chain triggers on any 401 response. Refresh logic is idempotent (retried request with new token). Expired refresh token triggers logout.

#### 1.3 API Gateway & Rate Limiting Setup (1 day)

| Task | Owner | Deliverable | Acceptance |
|------|-------|-------------|-----------|
| Configure rate limiting | devops-team | POST `/auth/login`: 10 req/min per IP; POST `/auth/register`: 5 req/min per IP; GET `/auth/me`: 60 req/min per user | Staging test: verify limits enforced, 429 returned |
| Configure CORS | devops-team | Allow frontend origin (staging domain); disallow cross-origin token access | Staging test: CORS headers present, preflight passes |

**Wiring Task 1.3.1: Rate Limiting Middleware**
- **Named Artifact:** API Gateway rate limiting configuration
- **Wired Components:** Per-endpoint limits wired to IP/user-based buckets
- **Owning Phase:** Phase 1
- **Cross-Reference:** R-002 (brute-force mitigation), NFR-PERF-002 (concurrent request support)
- **Implementation Detail:** API Gateway enforces limits before requests reach `AuthService`. Limits differ by endpoint (login more restrictive than refresh). 429 responses trigger client-side backoff.

#### 1.4 Feature Flag Wiring (1 day)

| Flag | Behavior | Owner | Acceptance |
|------|----------|-------|-----------|
| `AUTH_NEW_LOGIN` | OFF by default. When ON, routes login/register traffic to `AuthService`; when OFF, uses legacy auth. | devops-team | Staging test: traffic routed correctly, seamless toggle without restart |
| `AUTH_TOKEN_REFRESH` | OFF by default. When ON, enables POST `/auth/refresh` endpoint. When OFF, only access tokens issued. | devops-team | Staging test: refresh endpoint accessible/unavailable based on flag |

**Wiring Task 1.4.1: Feature Flag Registry**
- **Named Artifact:** `AUTH_NEW_LOGIN` and `AUTH_TOKEN_REFRESH` flags in feature flag service
- **Wired Components:** `AuthService` checks `AUTH_NEW_LOGIN` at login entry point; `TokenManager` checks `AUTH_TOKEN_REFRESH` at refresh endpoint
- **Owning Phase:** Phase 1
- **Cross-Reference:** Rollout phasing (Phase 1 Alpha, Phase 2 Beta, Phase 3 GA)
- **Implementation Detail:** Flags loaded from environment or feature flag store on service startup. Changes do not require restart if using polling store. Default OFF for both flags.

#### 1.5 Monitoring & Observability Setup (1 day)

| Artifact | Owner | Details | Acceptance |
|----------|-------|---------|-----------|
| Prometheus metrics | devops-team | `auth_login_total`, `auth_login_duration_seconds`, `auth_registration_total`, `auth_token_refresh_total` | Staging test: metrics scraped, dashboards render |
| OpenTelemetry traces | devops-team | Trace spans from API entry through `PasswordHasher` → `TokenManager` → `JwtService` | Staging test: traces visible in Jaeger, latency measured |
| Structured logging | devops-team | All auth events logged: login success/failure, registration, token refresh, password reset | Staging test: logs parseable, searchable by user ID and event type |
| Grafana dashboards | devops-team | Login latency p95, error rate, concurrent requests, Redis memory usage | Staging test: dashboards load, reflect real traffic |

**Wiring Task 1.5.1: Audit Log Callback Chain**
- **Named Artifact:** Post-login/registration/refresh callback that writes to audit log table
- **Wired Components:** Each `AuthService` flow end-point triggers audit log write: user_id, event_type, timestamp, IP, outcome
- **Owning Phase:** Phase 1
- **Cross-Reference:** NFR-COMP-002 (SOC2 audit logging), GAP-002 (admin audit log query API, addressed in Phase 2)
- **Implementation Detail:** Synchronous callback at end of each auth operation. Audit log retention: 12 months (PRD requirement, overrides TDD 90-day). Schema: user_id, event_type, timestamp, ip_address, outcome, details (JSON).

#### 1.6 Manual Testing & Bug Fix (2 days)

| Test Scenario | Owner | Success Criteria | Status |
|---------------|-------|------------------|--------|
| User registration (valid data) | QA | Account created, user logged in, redirected to dashboard | Pending |
| User registration (duplicate email) | QA | 409 error, user NOT created, helpful message | Pending |
| User registration (weak password) | QA | 400 error, inline validation feedback | Pending |
| User login (valid credentials) | QA | 200 OK, `AuthToken` returned, token stored via `AuthProvider` | Pending |
| User login (invalid credentials) | QA | 401 error, no user enumeration | Pending |
| User login (5 failed attempts) | QA | Account locked, 423 response, error message | Pending |
| Token refresh (valid refresh token) | QA | 200 OK, new `AuthToken` pair, old token revoked | Pending |
| Token refresh (expired refresh token) | QA | 401 error, user prompted to re-login | Pending |
| User profile retrieval (authenticated) | QA | GET `/auth/me` returns `UserProfile` with email, displayName, timestamps | Pending |
| User profile retrieval (unauthenticated) | QA | 401 error | Pending |
| Session persistence (page refresh) | QA | `AuthProvider` silently refreshes token; no re-login prompt | Pending |
| Audit logging (login success) | QA | Audit log entry written with user_id, timestamp, IP, outcome | Pending |

**Exit Criteria for Phase 1:**
- All 5 FR-AUTH requirements pass functional tests
- Zero P0/P1 bugs (P2 bugs allowed with mitigation)
- Audit log retention set to 12 months (override TDD 90-day default)
- Feature flags `AUTH_NEW_LOGIN` and `AUTH_TOKEN_REFRESH` both OFF by default
- Metrics and tracing validated in staging

---

### Phase 2: Beta (Weeks 2–3)

**Goal:** Validate NFR-PERF-001 (< 200ms p95), NFR-REL-001 (99.9% uptime), and R-002 (brute-force mitigation) under production load.

#### 2.1 Production Deployment & Traffic Shift (Day 1 of Week 2)

| Task | Owner | Deliverable | Acceptance |
|------|-------|-------------|-----------|
| Deploy to production | devops-team | `AuthService` and dependencies (PostgreSQL, Redis, SendGrid) deployed with `AUTH_NEW_LOGIN` OFF | Prod smoke test: service healthy, metrics flowing |
| Enable feature flag for 10% cohort | devops-team | `AUTH_NEW_LOGIN` enabled for 10% of traffic via feature flag store (user ID hash) | Prod validation: 10% of requests route to new service, 90% to legacy |

**Wiring Task 2.1.1: Production Feature Flag Routing**
- **Named Artifact:** Feature flag cohort distribution (10% sampling)
- **Wired Components:** Request router checks user ID hash against 10% threshold, routes to `AuthService` or legacy auth
- **Owning Phase:** Phase 2
- **Cross-Reference:** Rollout phasing, zero-downtime deployment
- **Implementation Detail:** Consistent hashing ensures same user always routes to same service across requests. Flag changes propagate within 30 seconds (polling interval).

#### 2.2 Production Monitoring & Alert Tuning (Days 1–3 of Week 2)

| Metric | Alert Threshold | Action | Owner |
|--------|-----------------|--------|-------|
| `auth_login_duration_seconds` p95 | > 500ms | Page on-call, investigate latency root cause | devops-team |
| `auth_login_total` error rate | > 5% for 2 minutes | Page on-call, check `AuthService` and Redis health | devops-team |
| Redis connection failures | > 10/minute | Page on-call, check Redis cluster, scale if needed | devops-team |
| PostgreSQL connection pool exhaustion | > 80% utilized | Page on-call, check for connection leaks, scale if needed | devops-team |
| Brute-force attack detected (rate limit hit > 1000x per endpoint) | True | Page security-team, enable IP-level blocking at WAF | security-team |

#### 2.3 Load Testing & Performance Validation (Days 2–5 of Week 2)

| Test Scenario | Load | Success Criteria | Tool | Owner |
|---------------|------|------------------|------|-------|
| Concurrent login requests | 500 concurrent | p95 latency < 200ms; error rate < 0.1% | k6 | QA |
| Sustained login traffic | 100 req/sec for 10 min | p95 latency < 200ms; no Redis connection pool exhaustion | k6 | QA |
| Token refresh under load | 200 concurrent refresh requests | p95 latency < 100ms; refresh token TTL respected | k6 | QA |
| Database connection pool limits | 500 concurrent login + profile requests | Connection pool not exhausted; no connection timeouts | k6 + Postgres monitoring | QA |

**Success Criteria:**
- NFR-PERF-001: All endpoints meet < 200ms p95 (target met)
- NFR-PERF-002: 500 concurrent logins handled without errors
- Error rate < 0.1% under sustained load

#### 2.4 Beta Monitoring Window (Full Week 3)

| Metric | Target | Measurement | Owner |
|--------|--------|-------------|-------|
| Service availability | 99.9% uptime | Health check monitoring, 7-day rolling window | devops-team |
| Login success rate | > 99% | Ratio of successful logins to attempts | auth-team |
| Token refresh success rate | > 99% | Ratio of successful refreshes to attempts | auth-team |
| Failed login rate (end-user legitimate attempts) | < 5% | Auth event log analysis | product-team |
| Average session duration | > 30 minutes | Token refresh event analytics | product-team |

**Rollback Trigger Conditions:**
- p95 latency exceeds 1000ms for > 5 minutes → Trigger Phase 2 rollback
- Error rate exceeds 5% for > 2 minutes → Trigger Phase 2 rollback
- Redis connection failures > 10/minute → Trigger Phase 2 rollback
- Any data corruption detected → Trigger Phase 2 rollback + restore from backup

**Rollback Procedure:**
1. Disable `AUTH_NEW_LOGIN` feature flag → 100% traffic routes to legacy auth
2. Verify legacy login flow operational via smoke tests
3. Investigate root cause in logs/traces
4. If data corruption, restore PostgreSQL and Redis from pre-Phase-2 backup
5. Post-mortem within 48 hours

#### 2.5 Compliance & Audit Readiness (Day 5 of Week 2)

| Task | Owner | Acceptance |
|------|-------|-----------|
| Audit log verification | security-team | Spot-check 100 audit log entries: all fields present (user_id, timestamp, IP, outcome), 12-month retention configured |
| GDPR consent tracking | legal-team | Verify consent field present on registration, consent timestamp recorded | GAP-004 resolution |
| SOC2 control validation | security-team | Audit log queryable, retention policy enforced, sample report generated |

#### 2.6 Performance Tuning & Hot Spot Fixes (Ongoing Week 3)

If load tests or beta monitoring identify bottlenecks:

| Bottleneck | Mitigation | Phase | Owner |
|-----------|-----------|-------|-------|
| `PasswordHasher` slow (if bcrypt cost 12 > 500ms) | Reduce cost to 11 (or profile CPU); validate timing-invariant implementation | 2 | auth-team |
| `TokenManager` Redis latency | Increase Redis replica count; enable read-from-replica for validation | 2 | devops-team |
| `UserRepo` query latency | Add database index on email column (if not present); profile query plans | 2 | devops-team |

**Exit Criteria for Phase 2:**
- 7-day uptime 99.9% or better
- p95 latency < 200ms on all endpoints
- Error rate < 0.1% under sustained load
- Brute-force mitigation (account lockout) validated
- Audit log 12-month retention configured and tested
- Zero data corruption incidents

---

### Phase 3: GA — Full Rollout (Week 4)

**Goal:** Remove feature flags, deprecate legacy auth, enable full token refresh capability.

#### 3.1 Feature Flag Cleanup & Traffic Migration (Day 1–2 of Week 4)

| Task | Owner | Details | Acceptance |
|------|-------|---------|-----------|
| Increase `AUTH_NEW_LOGIN` to 50% | devops-team | Gradual ramp to ensure stability | Monitor error rate, latency |
| Increase `AUTH_NEW_LOGIN` to 100% | devops-team | All traffic to `AuthService`; legacy auth no longer used | Smoke test passes, zero errors for 1 hour |
| Enable `AUTH_TOKEN_REFRESH` | devops-team | Refresh tokens fully functional | Verify POST `/auth/refresh` accessible, success rate > 99% |
| Remove feature flags | devops-team | Delete `AUTH_NEW_LOGIN` and `AUTH_TOKEN_REFRESH` conditional logic; code now assumes new auth only | All tests pass, no references to flags remain |

#### 3.2 Legacy Auth Deprecation (Days 2–3 of Week 4)

| Task | Owner | Details | Acceptance |
|------|-------|---------|-----------|
| Announce deprecation | product-team | Public communication: legacy auth endpoint deprecated after 30 days | Users notified via email and in-app banner |
| Redirect legacy endpoint traffic | devops-team | Legacy `/v0/auth/login` endpoint returns 301 redirect to `/v1/auth/login` | 301 responses logged, redirect verified |
| Remove legacy code | auth-team | Delete legacy `AuthService` and related components from codebase | Code review approved, no breaking references |

#### 3.3 Production Hardening & Runbook Validation (Days 3–4 of Week 4)

| Task | Owner | Details | Acceptance |
|------|-------|---------|-----------|
| Validate runbooks | devops-team | Dry-run all on-call scenarios: `AuthService` down, token refresh failures, Redis down | All runbooks executable, completion time < 15 min |
| On-call handoff | devops-team | Assign 24/7 on-call rotation for first 2 weeks post-GA | auth-team on-call confirmed, escalation paths clear |
| Capacity planning review | devops-team | Verify `AuthService` pod count, PostgreSQL pool size, Redis memory handle peak load projections | Scaling triggers defined and tested |

#### 3.4 Success Metrics Baseline & Dashboard Setup (Day 4 of Week 4)

| Metric | Baseline (Day 1 of GA) | Target | Dashboard | Owner |
|--------|----------------------|--------|-----------|-------|
| Daily active authenticated users | (establish baseline) | > 1000 within 30 days | Product dashboard | product-team |
| Registration conversion rate | (establish baseline) | > 60% | Funnel analytics | product-team |
| Login response time (p95) | (record from Phase 2) | < 200ms sustained | Ops dashboard | devops-team |
| Service availability | (record from Phase 2) | 99.9% rolling 30-day | Ops dashboard | devops-team |
| Failed login rate | (record from Phase 2) | < 5% | Ops dashboard | devops-team |
| Password reset completion rate | (establish baseline) | > 80% | Product dashboard | product-team |

#### 3.5 Documentation & Knowledge Transfer (Days 3–5 of Week 4)

| Deliverable | Owner | Audience | Acceptance |
|-------------|-------|----------|-----------|
| Operations runbook | devops-team | On-call engineers | Comprehensive, tested, linked from README |
| API documentation | auth-team | Developers, API consumers | Swagger/OpenAPI spec, endpoint docs, error codes, rate limits |
| Troubleshooting guide | auth-team | Support team, auth-team | Common issues, diagnosis steps, escalation paths |
| Architecture decision record (ADR) | auth-team | Future maintainers | Rationale for JWT vs session storage, RS256 vs HS256, bcrypt cost 12 |

**Exit Criteria for Phase 3:**
- 100% traffic on new `AuthService`
- Legacy auth fully deprecated and removed
- On-call rotation established
- All runbooks validated
- Success metrics baseline established
- Zero P0 production incidents for 48 hours

---

## Integration Points & Wiring Summary

### Dispatch Tables & Registries

| Artifact | Components | Owning Phase | Validation |
|----------|-----------|--------------|-----------|
| **Password Hashing Strategy** | `PasswordHasher` (bcryptjs) + future argon2id slot | Phase 1 | Unit test: hash/verify operations pass |
| **Token Dispatch** | `TokenManager` routes to JWT vs Redis based on request type | Phase 1 | Integration test: both paths exercise correctly |
| **Feature Flag Registry** | `AUTH_NEW_LOGIN`, `AUTH_TOKEN_REFRESH` flags + router | Phase 1 | Staging test: traffic splits correctly between old/new |
| **Rate Limiting Rules** | Per-endpoint limits (login 10/min, register 5/min, refresh 30/min) | Phase 1 | Load test: limits enforced, 429 returned |
| **Account Lockout Strategy** | Failed attempt counter with 15-min TTL | Phase 1 | Unit test: counter increments, lockout triggered after 5 failures |
| **Audit Log Callback Chain** | Post-operation callbacks writing user_id, timestamp, IP, outcome | Phase 1 | Integration test: all auth events logged |
| **Silent Refresh Middleware** | HTTP interceptor → 401 → refresh → retry | Phase 1 | Component test: middleware chain executes end-to-end |
| **Error Response Dispatch** | Error codes mapped to HTTP status (401, 409, 429, etc.) | Phase 1 | API test: all endpoints return correct status codes |
| **CORS Middleware** | Allowed origins configuration | Phase 1 | Staging test: CORS headers present, preflight passes |

### Dependency Injection & Configuration

| Component | Injected Dependencies | Configuration Source | Phase |
|-----------|----------------------|----------------------|-------|
| `AuthService` | `PasswordHasher`, `TokenManager`, `UserRepo` | Constructor injection | Phase 1 |
| `TokenManager` | `JwtService`, Redis client | Constructor injection | Phase 1 |
| `UserRepo` | PostgreSQL connection pool | Constructor injection | Phase 1 |
| `JwtService` | RS256 private/public key pair, key rotation schedule | Environment variables + secret store | Phase 1 |
| `PasswordHasher` | bcryptjs cost factor (12) | Configuration file or environment | Phase 1 |
| `AuthProvider` (frontend) | API base URL, token storage mechanism | Context props | Phase 1 |

### Feature Flagging Integration

| Flag | Service Boundary | Check Location | Behavior | Phase |
|------|-----------------|-----------------|----------|-------|
| `AUTH_NEW_LOGIN` | Router → `AuthService` vs legacy | API Gateway or middleware | Route to new service if ON; legacy if OFF | Phases 1, 2, 3 |
| `AUTH_TOKEN_REFRESH` | `TokenManager` refresh endpoint | TokenManager initialization | Expose POST `/auth/refresh` if ON; 404 if OFF | Phases 1, 2, 3 |

### Callback Chain: Audit Logging

**Flow:**
1. User calls POST `/auth/login`
2. `AuthService.login()` invokes `PasswordHasher.verify()`
3. On success/failure, `AuditLogger.log()` callback fires
4. Log entry written to PostgreSQL: `{ user_id, event_type: "login", timestamp, ip_address, outcome, details }`
5. Log retention policy enforced: 12 months (overrides TDD 90-day)

**Implementation Detail:**
- Synchronous callback; no async delay (logging should not block response)
- One callback per auth operation: login, registration, token refresh, password reset request, password reset confirmation
- Callback wired in `AuthService` constructor initialization

---

## Risk Assessment & Mitigation

### Risk Register

| # | ID | Risk | Probability | Impact | Severity | Mitigation | Contingency | Owner |
|---|-----|------|------------|--------|----------|-----------|-------------|-------|
| 1 | R-001 | Token theft via XSS allows session hijacking | Medium | High | HIGH | Store accessToken in memory only. HttpOnly cookies for refreshToken. 15-minute access token expiry limits window. CSP headers enforced. | Immediate token revocation via `TokenManager`. Force password reset for affected accounts. | security-team |
| 2 | R-002 | Brute-force attacks on login endpoint | High | Medium | HIGH | Rate limiting (10 req/min per IP). Account lockout after 5 failures within 15 minutes. CAPTCHA on `LoginPage` after 3 failures. | Block IPs at WAF. Enable SMS alert for admin on lockout spike. | security-team |
| 3 | R-003 | Data loss during migration from legacy auth | Low | High | MEDIUM | Parallel run during Phase 1–2. Idempotent upsert operations. Full DB backup before each phase. | Rollback to legacy. Restore from pre-migration backup within 30 minutes. | devops-team |
| 4 | R-004 | Low registration adoption due to poor UX | Medium | High | MEDIUM | Usability testing before Phase 1 launch. A/B test registration form (email-first vs all-fields). Iterate based on funnel data. | Extend Phase 1 timeline by 1 week for UX fixes if conversion < 40% in beta. | product-team |
| 5 | R-005 | Security breach from implementation flaws | Low | Critical | HIGH | Dedicated security review of `PasswordHasher`, `JwtService`, token storage logic before Phase 2. Penetration testing by external firm before Phase 3. | Immediate incident response; public disclosure within 48 hours; offer password resets. | security-team |
| 6 | R-006 | Compliance failure from incomplete audit logging | Medium | High | HIGH | Define audit log schema early (Phase 1). Validate against SOC2 controls in Phase 2 QA. Ensure 12-month retention configured. | Delay Phase 3 GA by 1 week; backfill missing audit logs from service logs if possible. | compliance-team |
| 7 | R-007 | Email delivery failures blocking password reset | Low | Medium | MEDIUM | SendGrid delivery monitoring and alerting. Fallback support channel for users. Test password reset flow weekly. | Manual password reset via admin console. Public communication of email delay. | devops-team |

### Risk Mitigation Roadmap

**Immediate (Phase 1):**
- R-001: CSP headers configured in API Gateway; accessToken memory storage + HttpOnly refresh cookies implemented in frontend
- R-002: Rate limiting wired at API Gateway; account lockout logic in `AuthService`
- R-003: Full DB backup automation set up; backup tested before Phase 1 cutover
- R-005: Security code review scheduled for end of Phase 1
- R-006: Audit log schema finalized; 12-month retention configured

**Pre-Beta (End of Phase 1):**
- R-002: CAPTCHA service integration tested (Recaptcha or equivalent)
- R-004: Usability testing of `RegisterPage` with 10 users; iteration on weak spots
- R-005: Penetration testing engagement scoped (external firm); Phase 3 timeline dependent on findings

**Pre-GA (Phase 2–3):**
- R-004: A/B testing results analyzed; conversion rate decision gate for Phase 3 go/no-go
- R-005: Pentest findings remediated; security sign-off obtained
- R-006: SOC2 auditor pre-audit review completed; any gaps addressed
- R-007: SendGrid alerting configured; fallback support documentation published

---

## Resource Requirements & Dependencies

### Team Composition

| Role | Count | Responsibilities | Allocation |
|------|-------|------------------|-----------|
| **Backend Engineer (auth-team)** | 2 | `AuthService`, `TokenManager`, `JwtService`, `PasswordHasher`, `UserRepo`, API endpoints | 100% (Phases 1–3) |
| **Frontend Engineer** | 1 | `LoginPage`, `RegisterPage`, `AuthProvider`, protected routes, token storage | 100% (Phases 1–2) |
| **DevOps Engineer** | 1 | Feature flags, deployment, monitoring, on-call rotation setup | 50% (Phases 1–3) |
| **QA Engineer** | 1 | Manual testing, load testing, runbook validation, regression testing | 100% (Phases 1–3) |
| **Security Engineer** | 0.5 | Code review, pentesting coordination, audit logging validation | 50% (Phases 1, 2) |
| **Product Manager** | 0.25 | Metrics definition, business value tracking, UX iteration decisions | 25% (Phases 1–3) |
| **Compliance Officer** | 0.25 | Audit logging verification, SOC2 alignment, GDPR consent tracking | 25% (Phases 1–3) |

**Peak Staffing:** 6 FTE during Phase 1 (full implementation); 5 FTE during Phase 2 (beta monitoring + tuning); 3 FTE during Phase 3 (GA + runbook validation).

### Infrastructure Dependencies

| Dependency | Version | Purpose | Impact if Unavailable | Procurement Timeline |
|-----------|---------|---------|----------------------|----------------------|
| PostgreSQL | 15+ | `UserProfile` persistence, audit log | No user storage; service non-functional | Pre-Phase 1 (already provisioned) |
| Redis | 7+ | Refresh token storage, revocation, account lockout counter | Token refresh disabled; account lockout bypassed | Pre-Phase 1 (already provisioned) |
| Node.js LTS | 20 | `AuthService` runtime | Service cannot run | Pre-Phase 1 |
| SendGrid API | — | Password reset emails | FR-AUTH-005 blocked | Pre-Phase 1 (API key provisioned) |
| Kubernetes (optional) | 1.28+ | Pod orchestration, auto-scaling | Manual instance management required | Pre-Phase 1 (if cloud-native deployment) |

### Third-Party Service Dependencies

| Service | Provider | Purpose | Cost | SLA | Fallback |
|---------|----------|---------|------|-----|----------|
| Email delivery | SendGrid | Password reset, email validation | ~$100/month at scale | 99.9% uptime | Support ticket for manual reset |
| Feature flag store | LaunchDarkly or in-house | Feature flag management | $0 (in-house) or $200+/month | — | Hardcoded flags in code |
| Error tracking | Sentry (optional) | Error monitoring and alerting | $100+/month | — | CloudWatch logs only |
| APM | DataDog or New Relic (optional) | Performance monitoring | $200+/month | — | Prometheus + Grafana |

### External Document Dependencies

| Document | Type | Purpose | Ownership | Status |
|----------|------|---------|-----------|--------|
| AUTH-PRD-001 | Upstream | Product requirements this roadmap implements | product-team | Draft |
| INFRA-DB-001 | Infrastructure | Database provisioning and sizing | devops-team | Done |
| SEC-POLICY-001 | Policy | Password and token security requirements | security-team | Pending review |
| COMPLIANCE-001 | Policy | SOC2 audit logging and GDPR requirements | compliance-team | Pending review |

---

## Success Criteria & Validation Approach

### Technical Validation

#### NFR-PERF-001: API Response Time (< 200ms p95)

**Measurement Method:**
- APM instrument: `AuthService.login()`, `TokenManager.refresh()`, `UserRepo.getById()` methods
- Trace all HTTP requests end-to-end (API Gateway → `AuthService` → database)
- Percentile capture: p50, p95, p99 latencies

**Validation Gates:**
| Phase | Target | Validation | Owner |
|-------|--------|-----------|-------|
| Alpha (Staging) | < 200ms p95 | APM dashboard; manual load test with 100 concurrent requests | QA |
| Beta (10% prod) | < 200ms p95 sustained | APM dashboard; k6 load test (500 concurrent logins) | QA |
| GA | < 200ms p95 sustained | APM dashboard; ongoing monitoring; alert if > 500ms for 5 min | devops-team |

**Success Definition:** p95 latency remains < 200ms throughout Phase 2 Beta monitoring window (full week 3) under production load.

#### NFR-PERF-002: Concurrent Authentication (500 concurrent login requests)

**Measurement Method:**
- k6 load test: 500 concurrent login requests, sustained for 10 minutes
- Measure: successful authentication rate, latency distribution, error rate, database connection pool utilization

**Validation Gate:**
- All 500 requests succeed (0% error rate)
- p95 latency < 200ms
- No database connection pool exhaustion

**Success Definition:** Phase 2 load testing passes 500 concurrent concurrent login test without errors.

#### NFR-REL-001: Service Availability (99.9% uptime over 30-day rolling windows)

**Measurement Method:**
- Health check endpoint: GET `/auth/health` returning 200 OK if `AuthService`, PostgreSQL, and Redis all healthy
- Monitoring: Prometheus scrapes every 30 seconds; cumulative uptime tracked

**Validation Gate:**
| Phase | Target | Measurement | Owner |
|-------|--------|-------------|-------|
| Alpha (Staging) | N/A | Not production; uptime not measured | — |
| Beta (Week 3) | 99.9% over 7 days | Monitoring dashboard; alert if < 99.9% | devops-team |
| GA | 99.9% over 30-day rolling windows | Ongoing monitoring; on-call escalation if breached | devops-team |

**Success Definition:** Phase 2 Beta achieves 99.9% uptime for full 7-day monitoring window.

#### NFR-SEC-001: Password Hashing (bcrypt cost factor 12)

**Measurement Method:**
- Unit test: `PasswordHasher.hash()` with test password; verify bcrypt cost parameter in resulting hash
- Benchmark test: Measure hash time with cost 12; target ~300ms per hash

**Validation Gate:**
- Hash function returns bcrypt hash with cost parameter = 12
- Hash time < 500ms (tolerance for slower CI environments)
- No plaintext passwords in logs or database

**Success Definition:** Unit tests pass; hash time benchmarked at < 500ms.

#### NFR-SEC-002: Token Signing (RS256 with 2048-bit RSA keys)

**Measurement Method:**
- Unit test: `JwtService.sign()` and `JwtService.verify()` with sample payload
- Configuration validation test: Verify 2048-bit key length via keysize property

**Validation Gate:**
- JWT payload signed with RS256 (header.alg = "RS256")
- Key size verification passes (2048 bits or greater)
- Token verification succeeds with matching public key
- Token verification fails with mismatched key

**Success Definition:** Unit tests pass; configuration validates RSA key size.

#### NFR-COMP-001: GDPR Consent at Registration

**Measurement Method:**
- Data schema: `UserProfile` includes `consent_given` (boolean) and `consent_timestamp` (ISO 8601)
- API test: POST `/auth/register` request includes `consent` field; response confirms consent recorded

**Validation Gate:**
- `UserProfile` schema includes consent fields
- Registration form displays consent checkbox
- Consent field required (cannot register without consent)
- Consent timestamp persisted in database

**Success Definition:** User can register only with consent checkbox; consent timestamp recorded.

#### NFR-COMP-002: SOC2 Audit Logging (12-month retention)

**Measurement Method:**
- Audit log schema: `audit_logs` table with columns: user_id, event_type, timestamp, ip_address, outcome, details (JSON)
- Retention policy: PostgreSQL policy deletes records > 12 months old
- Query validation: Auditor can query logs by user_id, date range, event type

**Validation Gate:**
- Audit log table created with all required columns
- Retention policy configured (12-month TTL)
- Sample audit logs present for all auth events (login, registration, token refresh, password reset)
- Query performance validated (< 1 second for typical auditor query)

**Success Definition:** SOC2 auditor pre-audit review confirms audit logs meet control requirements.

#### NFR-COMP-003: GDPR Data Minimization

**Measurement Method:**
- Data schema review: `UserProfile` contains only email, hashed_password, displayName, timestamps
- Privacy audit: No additional PII fields (phone, address, etc.)

**Validation Gate:**
- `UserProfile` schema review approved by compliance team
- No additional PII collected at registration
- Data minimization documented in privacy policy

**Success Definition:** Compliance team approves data minimization scope.

### Business Validation

#### Registration Conversion Rate (> 60%)

**Measurement Method:**
- Product analytics: Track funnel from landing page → "Sign Up" click → registration form → email confirmation → first login
- Measurement: Conversion = (confirmed accounts / landing page visits) × 100

**Validation Gate:**
| Phase | Target | Measurement | Owner |
|-------|--------|-------------|-------|
| Alpha | N/A | Not released to users | — |
| Beta | > 40% (relaxed target for 10% cohort) | Funnel analytics; daily dashboards | product-team |
| GA | > 60% (full target) | Funnel analytics; daily dashboards | product-team |

**Success Definition:** GA conversion rate exceeds 60% within 30 days of Phase 3 GA.

#### Daily Active Authenticated Users (> 1000 within 30 days of GA)

**Measurement Method:**
- Product analytics: Count unique users who issue at least one auth token (login or token refresh) per day
- Measurement: DAU = count of users with ≥ 1 auth event per calendar day

**Validation Gate:**
| Metric | Target | Timeline | Owner |
|--------|--------|----------|-------|
| Day 1 of GA | Establish baseline | Day 1 | product-team |
| Day 7 of GA | Upward trend visible | Day 7 | product-team |
| Day 30 of GA | > 1000 DAU | Day 30 | product-team |

**Success Definition:** 1000+ DAU achieved by end of Phase 3 first month.

#### Failed Login Rate (< 5% of attempts)

**Measurement Method:**
- Auth event log analysis: Count login attempts by outcome (success, invalid credentials, account locked, etc.)
- Measurement: Failed login rate = (failed attempts / total attempts) × 100

**Validation Gate:**
| Phase | Target | Measurement | Owner |
|-------|--------|-------------|-------|
| Beta | < 10% (relaxed for testing) | Daily dashboard | QA |
| GA | < 5% (full target) | Daily dashboard | product-team |

**Success Definition:** Failed login rate consistently < 5% in GA phase (after user education period).

#### Average Session Duration (> 30 minutes)

**Measurement Method:**
- Product analytics: Token refresh event timestamps; calculate time between login and last refresh (or logout)
- Measurement: Average session duration = mean(logout_time - login_time) for all sessions

**Validation Gate:**
| Phase | Target | Measurement | Owner |
|-------|--------|-------------|-------|
| Beta | > 20 minutes (relaxed for testing) | Daily dashboard | product-team |
| GA | > 30 minutes (full target) | Daily dashboard | product-team |

**Success Definition:** Average session duration > 30 minutes within 7 days of GA.

#### Password Reset Completion Rate (> 80%)

**Measurement Method:**
- Product analytics: Funnel tracking from reset request → email opened → link clicked → new password submitted → success
- Measurement: Completion rate = (password resets completed / reset emails sent) × 100

**Validation Gate:**
| Phase | Target | Measurement | Owner |
|-------|--------|-------------|-------|
| Beta | > 70% (relaxed for testing) | Daily dashboard | product-team |
| GA | > 80% (full target) | Daily dashboard | product-team |

**Success Definition:** Reset completion rate > 80% within 14 days of GA.

### Requirement Coverage Validation

All 13 requirements (5 functional, 8 non-functional) must pass acceptance criteria by end of Phase 1 Alpha:

| Requirement | Acceptance Criteria | Phase 1 Exit Gate | Status |
|-------------|-------------------|-----------------|--------|
| FR-AUTH-001 | Login returns 200 with `AuthToken` on valid credentials; 401 on invalid; 423 on lockout | Unit test + integration test pass | Pending |
| FR-AUTH-002 | Registration returns 201 with `UserProfile` on success; 409 on duplicate email; 400 on weak password | Unit test + integration test pass | Pending |
| FR-AUTH-003 | Token refresh returns new `AuthToken` pair; refresh token 7-day TTL; access token 15-min TTL | Unit test + integration test pass | Pending |
| FR-AUTH-004 | GET `/auth/me` returns authenticated user's `UserProfile` | Unit test + integration test pass | Pending |
| FR-AUTH-005 | Password reset request sends email with 1-hour token; confirmation updates password; token single-use | Unit test + integration test pass; email delivery tested | Pending |
| NFR-PERF-001 | < 200ms p95 latency | Load test passes | Pending |
| NFR-PERF-002 | 500 concurrent logins supported | Load test passes | Pending |
| NFR-REL-001 | 99.9% uptime over rolling 30-day windows | Phase 2 validation gate | Pending |
| NFR-SEC-001 | bcrypt cost factor 12 | Unit test validates cost parameter | Pending |
| NFR-SEC-002 | RS256 with 2048-bit RSA keys | Configuration test validates key size | Pending |
| NFR-COMP-001 | GDPR consent at registration | Data schema + form validation | Pending |
| NFR-COMP-002 | 12-month audit log retention | Retention policy configured | Pending |
| NFR-COMP-003 | Data minimization (email, hashed password, display name only) | Data schema review | Pending |

---

## Gap Resolution Plan

The extraction identified 5 gaps. Resolution approach per gap:

| Gap ID | Gap | Severity | Resolution | Phase | Owner |
|--------|-----|----------|-----------|-------|-------|
| GAP-001 | **Audit log retention conflict:** TDD specifies 90-day; PRD requires 12-month for SOC2 | High | **Action:** Override TDD with PRD 12-month requirement. Configure PostgreSQL retention policy for 12 months. Validate in Phase 1. | Phase 1 | devops-team |
| GAP-002 | **Logout endpoint missing:** PRD includes logout as in-scope (Epic AUTH-E1). TDD missing logout endpoint. | Medium | **Action:** Add POST `/auth/logout` endpoint wired to `TokenManager.revoke()`. Revokes current refresh token. Acceptance: Unit test + integration test. | Phase 1 Phase 1.2 | auth-team |
| GAP-003 | **Admin audit log query API missing:** PRD persona Jordan requires queryable audit logs (AUTH-E3 story). TDD has no admin endpoint. | Medium | **Action:** Add GET `/admin/auth/audit-logs` endpoint (requires admin role). Query by date range, user_id, event type. Acceptance: Integration test with sample auditor queries. | Phase 2 | auth-team |
| GAP-004 | **GDPR consent mechanism unspecified:** NFR-COMP-001 requires consent at registration. `UserProfile` schema and `/auth/register` request/response do not include consent. | Medium | **Action:** Add `consent_given` (boolean) and `consent_timestamp` (ISO 8601) to `UserProfile`. Add `consent` checkbox to `RegisterPage`. Require consent (return 400 if false). Acceptance: Integration test verifies consent recorded. | Phase 1 | auth-team + frontend-team |
| GAP-005 | **Password reset endpoints not fully specified:** FR-AUTH-005 references `/auth/reset-request` and `/auth/reset-confirm` but TDD Section 8 omits detailed request/response schemas. | Medium | **Action:** Finalize schemas: POST `/auth/reset-request` (email) → 200 OK regardless of registration status. POST `/auth/reset-confirm` (token, newPassword) → 200 OK on success or 401 on expired/invalid token. Acceptance: API tests validate schemas and error cases. | Phase 1 | auth-team |

**Gap Resolution Schedule:**
- GAP-001 (audit retention): Configured in Phase 1; validated in Phase 2
- GAP-002 (logout endpoint): Implemented in Phase 1.2; tested in Phase 1.6 manual testing
- GAP-003 (admin audit API): Implemented in Phase 2; validated by auditor
- GAP-004 (GDPR consent): Implemented in Phase 1; tested in Phase 1.6
- GAP-005 (reset schemas): Finalized in Phase 1.1; tested in Phase 1.6

All gaps must be resolved before Phase 2 Beta to avoid compliance/contractual issues.

---

## Timeline Estimates & Critical Path

### High-Level Timeline

```
Week 1 (Phase 1):   Internal Alpha — Component implementation, manual testing, feature flag setup
Week 2–3 (Phase 2): Beta — 10% traffic, load testing, performance tuning, compliance validation
Week 4 (Phase 3):   GA — Traffic migration, runbook validation, legacy deprecation, on-call handoff
```

### Detailed Phase 1 Breakdown (Week 1)

| Task | Duration | Dependencies | Owner | Slack |
|------|----------|-------------|-------|-------|
| `PasswordHasher` implementation | 0.5 days | None | auth-team | — |
| `JwtService` implementation | 0.75 days | None | auth-team | — |
| `TokenManager` implementation | 1 day | `JwtService` | auth-team | — |
| `UserRepo` implementation | 0.5 days | None | auth-team | — |
| `AuthService` implementation | 1.5 days | All above + gap fixes | auth-team | — |
| `LoginPage` + `RegisterPage` | 1 day | None (parallel) | frontend-team | — |
| `AuthProvider` implementation | 1 day | `LoginPage` + `RegisterPage` | frontend-team | — |
| Feature flag wiring | 0.5 days | `AuthService`, frontend | devops-team | — |
| Monitoring setup | 0.5 days | None (parallel) | devops-team | 0.5 days |
| Manual testing (QA) | 2 days | All components ready | QA | 1 day |
| **Critical Path Total** | **5 days** | Sequential: `PasswordHasher` → `JwtService` → `TokenManager` → `AuthService` → Test | — | — |

**Critical Path Analysis:**
- Critical path: `PasswordHasher` → `JwtService` → `TokenManager` → `AuthService` → gap fixes → manual testing
- Parallel streams: Frontend (`LoginPage` → `RegisterPage` → `AuthProvider`), DevOps (monitoring setup), both can start on Day 1
- Risk: If `PasswordHasher` or `JwtService` implementation discovers bugs, timeline extends by 1+ days
- Mitigation: Pair programming on crypto-critical components; prototype hash/sign operations on Day 0

### Detailed Phase 2 Breakdown (Weeks 2–3)

| Task | Duration | Dependencies | Async/Sync | Owner |
|------|----------|-------------|-----------|-------|
| Production deployment + feature flag enable | 0.5 days | Phase 1 exit gate | Sync | devops-team |
| Monitoring + alert tuning (Day 1–3) | 3 days | Deployment | Parallel to load testing | devops-team |
| Load testing (k6, Days 2–5) | 4 days | Deployment | Parallel | QA |
| Performance tuning + hot-spot fixes | 3 days | Load test results | Sync (depends on findings) | auth-team + devops-team |
| Compliance validation (audit log, consent) | 2 days | Deployment + monitoring | Parallel | compliance-team + security-team |
| 7-day stability window (Week 3) | 7 days | All above | Monitor | devops-team |
| **Total Duration** | **14 days** | — | — | — |

**Timeline Risk:**
- If load testing identifies p95 > 500ms, 2–3 day tuning cycle required (serial)
- If compliance gaps found (e.g., audit log missing columns), 1–2 day fix cycle required
- Stability window is non-negotiable; cannot accelerate GA without 7-day clean monitoring

### Detailed Phase 3 Breakdown (Week 4)

| Task | Duration | Dependencies | Owner |
|------|----------|-------------|-------|
| Traffic ramp to 50% (Day 1) | 0.5 days | Phase 2 exit gate | devops-team |
| Traffic ramp to 100% (Day 2) | 0.5 days | 50% stability for 8 hours | devops-team |
| Enable `AUTH_TOKEN_REFRESH` (Day 2) | 0.25 days | 100% traffic stable | devops-team |
| Legacy auth deprecation (Days 2–3) | 1 day | 100% traffic validation | auth-team |
| Runbook dry-run (Day 3) | 1 day | Feature flag cleanup | devops-team |
| On-call handoff + rotation setup (Day 4) | 0.5 days | Runbook validation | devops-team |
| Success metrics baseline (Day 4) | 0.5 days | 24-hour production data | product-team |
| **Total Duration** | **7 days** | — | — |

**Critical Path:** Sequential ramp (50% → 100%) + legacy deprecation + runbook validation. Cannot compress timeline without violating safety gates (e.g., 8-hour stability check before 100% ramp).

### Overall Critical Path & Slack Analysis

**Sequence:**
```
Phase 1 (5 critical days)
  → Gap fixes (2 days)
  → Manual testing (2 days)
  → Phase 1 exit gate
  ↓
Phase 2 (14 days: 3 monitoring + 4 load test + 7 stability)
  → Phase 2 exit gate
  ↓
Phase 3 (7 days: 0.5 ramp + 0.5 ramp + 6 cleanup)
  → GA complete
```

**Total Timeline:** 4 weeks (28 calendar days) from start of Phase 1 to GA completion.

**Slack & Risk Mitigation:**
- Slack in Phase 1: 0.5 days (if monitoring setup completes before manual testing)
- Slack in Phase 2: 0 days (7-day stability window is absolute; load testing runs in parallel to monitoring)
- Slack in Phase 3: 0 days (sequential ramp; cannot compress)

**Risk Scenarios & Time Impact:**
| Scenario | Impact | Mitigation | Time Added |
|----------|--------|------------|-----------|
| `PasswordHasher` bugs found in Phase 1 testing | Blocks auth-team | Pair programming; prototype on Day 0 | 1–2 days |
| Load test identifies p95 > 500ms | Blocks Phase 2 exit gate | Parallel performance tuning; possible algorithm change (bcrypt cost 11) | 2–3 days |
| Compliance gaps (audit log, consent) found in Phase 2 | Blocks Phase 3 GA | Fix + re-validate in Phase 2 monitoring window | 1–2 days |
| 7-day stability window fails (e.g., 99.5% uptime, not 99.9%) | Blocks Phase 3 GA | Investigate root cause, fix, repeat 7-day window | 7+ days |

**Conservative Estimate:** 4 weeks best-case; 5–6 weeks if any P1 bugs surface.

---

## Success Definition & Go/No-Go Criteria

### Phase 1 Exit Gate (End of Week 1)

**Go Criteria:**
- [ ] All 5 FR-AUTH requirements pass unit + integration tests
- [ ] All 8 NFR requirements validated (performance, security, compliance)
- [ ] Zero P0/P1 bugs; P2 bugs documented with mitigations
- [ ] Audit log 12-month retention configured (GAP-001 resolved)
- [ ] GDPR consent field added to `UserProfile` (GAP-004 resolved)
- [ ] Logout endpoint implemented (GAP-002 resolved)
- [ ] Password reset schemas finalized (GAP-005 resolved)
- [ ] Feature flags `AUTH_NEW_LOGIN` and `AUTH_TOKEN_REFRESH` both OFF by default
- [ ] Staging environment passes smoke tests; metrics flowing

**No-Go Triggers:**
- P0 bug unfixed
- Core requirement failing acceptance criteria
- Compliance gap unresolved (audit retention, consent)

---

### Phase 2 Exit Gate (End of Week 3)

**Go Criteria:**
- [ ] 7-day uptime 99.9% or better
- [ ] p95 latency < 200ms sustained
- [ ] Error rate < 0.1% under load
- [ ] 500 concurrent login load test passes
- [ ] Brute-force mitigation (account lockout) validated
- [ ] Audit log compliance validated by security team
- [ ] No data corruption incidents
- [ ] Admin audit log query API implemented (GAP-003 resolved)
- [ ] Runbook scenarios validated (not dry-run; in-staging)
- [ ] On-call team trained and ready

**No-Go Triggers:**
- Uptime < 99.9% for any 24-hour window
- p95 latency > 500ms sustained
- Any data corruption or security incident
- Load test fails (error rate > 1%)
- Compliance validation fails

---

### Phase 3 Exit Gate (End of Week 4)

**Go Criteria:**
- [ ] 100% traffic successfully migrated from legacy auth
- [ ] Legacy auth fully deprecated and code removed
- [ ] On-call rotation established and acknowledged
- [ ] 48-hour post-GA zero P0 incidents
- [ ] Success metrics baseline established

**No-Go Triggers:**
- Any P0 incidents after traffic ramp
- Data loss or corruption
- On-call escalation failures

---

## Appendix: Component Details

### Components Summary

| Component | Responsibility | Status | Owner | Phase |
|-----------|---------------|--------|-------|-------|
| `AuthService` | Facade for all auth flows: login, registration, profile, password reset | Not Started | auth-team | Phase 1 |
| `TokenManager` | Token issuance, refresh, revocation via Redis | Not Started | auth-team | Phase 1 |
| `JwtService` | JWT sign/verify using RS256 | Not Started | auth-team | Phase 1 |
| `PasswordHasher` | bcrypt abstraction for password hashing/verification | Not Started | auth-team | Phase 1 |
| `UserRepo` | `UserProfile` CRUD to PostgreSQL | Not Started | auth-team | Phase 1 |
| `LoginPage` | Email/password login UI | Not Started | frontend-team | Phase 1 |
| `RegisterPage` | Registration form with validation | Not Started | frontend-team | Phase 1 |
| `AuthProvider` | React context for auth state and silent refresh | Not Started | frontend-team | Phase 1 |
| ProfilePage | User profile display | Not Started | frontend-team | Phase 1 |

### API Endpoint Inventory

| # | Method | Path | Auth | Rate Limit | Status | Phase |
|---|--------|------|------|------------|--------|-------|
| 1 | POST | `/auth/login` | No | 10 req/min per IP | Pending | Phase 1 |
| 2 | POST | `/auth/register` | No | 5 req/min per IP | Pending | Phase 1 |
| 3 | GET | `/auth/me` | Yes (Bearer) | 60 req/min per user | Pending | Phase 1 |
| 4 | POST | `/auth/refresh` | No (refresh token body) | 30 req/min per user | Pending | Phase 1 |
| 5 | POST | `/auth/logout` | Yes (Bearer) | 60 req/min per user | **New (GAP-002)** | Phase 1 |
| 6 | POST | `/auth/reset-request` | No | 2 req/min per email | Pending | Phase 1 |
| 7 | POST | `/auth/reset-confirm` | No | Not specified | Pending | Phase 1 |
| 8 | GET | `/admin/auth/audit-logs` | Yes (Admin) | 10 req/min | **New (GAP-003)** | Phase 2 |

---

## Conclusion

This roadmap phases the User Authentication Service across 4 weeks: 1 week internal alpha, 2 weeks beta validation, 1 week GA. Implementation focuses on security-first token handling, phased rollout with automatic rollback triggers, and comprehensive compliance validation. All identified gaps are addressed; all 13 requirements are traceable to phases and validation gates. Resource requirements and success criteria are explicit.

**Recommended Go Date for Phase 1:** Immediate (Week of 2026-04-07)
**Estimated GA Date:** Week of 2026-04-28
