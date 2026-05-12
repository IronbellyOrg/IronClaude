---
spec_source: test-tdd-user-auth.md
complexity_score: 0.65
primary_persona: architect
---

# User Authentication Service — Project Roadmap

## Executive Summary

This roadmap delivers a secure, stateless user authentication system spanning backend services, frontend components, compliance infrastructure, and operational readiness. The system unblocks the Q2 2026 personalization roadmap ($2.4M revenue impact) and satisfies Q3 2026 SOC2 audit requirements.

**Complexity:** MEDIUM (0.65). Five functional requirements, nine non-functional requirements, nine backend/frontend components, six API endpoints, and three-phase rollout with 500 concurrent user load.

**Critical Constraint:** Ten open questions must be resolved before Phase 2 begins. Highest priority: audit log retention conflict (TDD specifies 90 days; PRD requires 12 months for SOC2), logout endpoint missing from TDD, and GDPR consent field not in UserProfile schema.

**Success Targets:**
- Registration conversion > 60%
- Login response time (p95) < 200ms
- Service availability 99.9% uptime
- Password reset completion > 80%
- Failed login rate < 5%

---

## Phased Implementation Plan

### Phase 1: Backend Foundation & Core Services (Weeks 1–3)

**Goal:** Establish secure authentication backbone. Deliver login, registration, and token infrastructure with full test coverage.

**Personas & Value:** Alex (end user) gets frictionless registration and login. Sam (API consumer) gains token refresh capability. Platform unblocks personalization features pending frontend integration.

**Milestones:**
- End Week 1: Data models and repositories complete; tests green for DM-001, DM-002
- End Week 2: All core services implemented (COMP-001–005); unit tests pass (TEST-001–003)
- End Week 3: All backend APIs operational (API-001–004); feature flag deployed to staging; internal alpha launch (MIG-001)

**Task Rows:**

| ID | Task | Component | Type | Owner | Dependencies | Acceptance Criteria |
|----|------|-----------|------|-------|--------------|-------------------|
| DM-001 | Design UserProfile schema and PostgreSQL migrations | Data Layer | Schema | auth-team | PostgreSQL 15+, SEC-POLICY-001 | id (UUID PK), email (UNIQUE), displayName, timestamps, roles array; indexed on email; supports audit log foreign keys |
| DM-002 | Design AuthToken structure and Redis storage patterns | Data Layer | Schema | auth-team | Redis 7+ | accessToken (JWT), refreshToken (opaque, hashed in Redis), expiresIn, tokenType; refresh tokens with 7-day TTL; revocation support |
| COMP-001 | Implement AuthService orchestrator | Backend Service | Core | auth-team | COMP-002, COMP-004, COMP-005, FR-AUTH-001–005 | Receives login/register/profile/reset requests; coordinates PasswordHasher, TokenManager, UserRepo; all methods covered by unit tests |
| COMP-002 | Implement TokenManager (token lifecycle) | Backend Service | Core | auth-team | COMP-003, Redis, FR-AUTH-003 | Issues and validates JWT pairs; revokes refresh tokens; stores hashed tokens in Redis; silent refresh logic |
| COMP-003 | Implement JwtService (RS256 signing) | Backend Service | Core | auth-team | RSA keys, FR-AUTH-003 | Signs/verifies JWTs with RS256 and 2048-bit keys; 5-second clock skew tolerance; quarterly key rotation capability |
| COMP-004 | Implement PasswordHasher (bcrypt abstraction) | Backend Service | Core | auth-team | bcryptjs, NFR-SEC-001 | Hash/verify methods; bcrypt cost factor 12; designed for future algorithm swaps; supports password policy validation |
| COMP-005 | Implement UserRepo (PostgreSQL access layer) | Backend Repository | Data Layer | auth-team | PostgreSQL 15+, pg-pool, DM-001 | Insert, retrieve, update UserProfile; connection pooling; transaction support; audit log inserts |
| API-001 | Implement POST /auth/login endpoint | API | Backend | auth-team | COMP-001, COMP-002, COMP-004, FR-AUTH-001, NFR-PERF-001 | Validates email/password; calls PasswordHasher; issues AuthToken via TokenManager; 200 success, 401/423/429 errors; < 200ms p95 |
| API-002 | Implement POST /auth/register endpoint | API | Backend | auth-team | COMP-001, COMP-005, COMP-004, FR-AUTH-002, NFR-SEC-001 | Creates UserProfile; hashes password via PasswordHasher; validates email uniqueness, password strength; 201 success, 400/409 errors |
| API-003 | Implement GET /auth/me endpoint | API | Backend | auth-team | COMP-001, COMP-005, FR-AUTH-004 | Returns authenticated UserProfile; validates Bearer token; 200 success, 401 error; includes id, email, displayName, roles, timestamps |
| API-004 | Implement POST /auth/refresh endpoint | API | Backend | auth-team | COMP-002, COMP-003, FR-AUTH-003 | Exchanges valid refresh token for new AuthToken pair; revokes old token; 200 success, 401 error; < 100ms p95 |
| FR-AUTH-001 | Login with email and password (functional req) | Feature | Requirement | product-team | COMP-001, API-001, TEST-001 | Valid credentials → 200 + AuthToken; invalid → 401 (no enumeration); account locked after 5 failed attempts in 15 min |
| FR-AUTH-002 | User registration with validation (functional req) | Feature | Requirement | product-team | COMP-001, API-002, TEST-004 | Email uniqueness enforced; password policy enforced (8+ chars, uppercase, number); bcrypt cost 12; 201 + UserProfile on success |
| FR-AUTH-003 | JWT token issuance and refresh (functional req) | Feature | Requirement | product-team | COMP-002, API-003, API-004, TEST-003 | accessToken 15-min TTL, refreshToken 7-day TTL; refresh returns new pair; revoked tokens return 401 |
| FR-AUTH-004 | User profile retrieval (functional req) | Feature | Requirement | product-team | COMP-001, API-003 | GET /auth/me returns id, email, displayName, createdAt, updatedAt, lastLoginAt, roles; expires tokens return 401 |
| NFR-SEC-001 | Password hashing with bcrypt cost 12 | Non-Functional | Security | auth-team | COMP-004, DM-001 | Unit test asserting bcrypt cost parameter; no plaintext passwords stored or logged; bcryptjs integration confirmed |
| NFR-SEC-002 | Token signing with RS256 2048-bit keys | Non-Functional | Security | auth-team | COMP-003, DM-002 | Configuration validation test; key generation and storage verified; RS256 signature validation in tests |
| TEST-001 | Unit test: Login with valid credentials returns AuthToken | Test | Unit | qa-team | COMP-001, COMP-002, COMP-004 | Mocks PasswordHasher.verify() → true; TokenManager.issueTokens() returns token pair; AuthService.login() returns valid AuthToken |
| TEST-002 | Unit test: Login with invalid credentials returns 401 | Test | Unit | qa-team | COMP-001, COMP-004 | Mocks PasswordHasher.verify() → false; AuthService.login() returns 401 error; no AuthToken issued |
| TEST-003 | Unit test: Token refresh with valid refresh token | Test | Unit | qa-team | COMP-002, COMP-003 | Mocks Redis lookup; TokenManager.refresh() validates token, revokes old, issues new pair; old refresh token marked revoked |
| MIG-001 | Phase 1 – Internal Alpha: Staging deployment with feature flag | Migration | Rollout | platform-team | All Phase 1 tasks | AuthService deployed to staging; AUTH_NEW_LOGIN feature flag OFF by default; auth-team + QA test all endpoints; zero P0/P1 bugs before Phase 2 start |

**Risk Mitigations (Phase 1):**
- **R-001 (Token theft via XSS):** Enforce in-memory-only accessToken storage during Phase 1 design; document HttpOnly cookie strategy for Phase 2 frontend.
- **R-003 (Data loss during migration):** Establish PostgreSQL backup procedures before Phase 1 migrations run; test restore process.

**Open Questions Blocking Phase 2:**
1. **OQ-6 — Audit log retention conflict:** TDD §7.2 specifies 90-day retention; PRD §S17 requires 12 months for SOC2. **Decision required:** Which retention policy governs implementation?
2. **OQ-9 — GDPR consent field missing:** NFR-COMP-001 requires consent timestamp at registration. **Decision required:** Add `consentTimestamp` field to DM-001 UserProfile schema before Phase 1 ends?
3. **OQ-10 — Password reset endpoints unspecified:** FR-AUTH-005 references `/auth/reset-request` and `/auth/reset-confirm` but TDD §8 lacks endpoint details. **Decision required:** Finalize endpoint specs (request/response schemas, token TTL, email delay) before Phase 2.

**Phase 1 Success Criteria:**
- All DM, COMP, API, FR, NFR, TEST-001–003, and MIG-001 tasks completed
- Zero critical (P0/P1) bugs in staging
- Performance baseline established: login < 200ms p95, registration < 300ms p95
- Feature flag AUTH_NEW_LOGIN controls login routing; can be disabled without code changes

---

### Phase 2: Frontend Integration & Advanced Flows (Weeks 4–6)

**Goal:** Deliver user-facing authentication, password reset flow, and compliance audit logging. Roll out to 10% of users (beta) and validate under load.

**Personas & Value:** Alex completes signup in < 60 seconds and experiences seamless session persistence. Jordan (admin) gains audit trail visibility for compliance. Platform achieves 60% registration conversion.

**Milestones:**
- End Week 4: All frontend components deployed (COMP-006–009); LoginPage and RegisterPage render in < 1s; AuthProvider handles token refresh.
- End Week 5: Password reset flow integrated (API-005, API-006, FR-AUTH-005); email integration tested; integration tests pass (TEST-004–005); beta rollout initiates (MIG-002).
- End Week 6: Beta runs at 10% load; monitoring confirms < 200ms p95 login latency; refresh token revocation working; funnel analytics show > 50% registration conversion.

**Task Rows:**

| ID | Task | Component | Type | Owner | Dependencies | Acceptance Criteria |
|----|------|-----------|------|-------|--------------|-------------------|
| COMP-006 | Implement LoginPage frontend component | Frontend | UI | frontend-team | COMP-009, API-001, API-004 | Renders email/password form; submits to POST /auth/login; stores AuthToken via AuthProvider; redirects to dashboard on success; shows error on 401/423/429; < 1s load time |
| COMP-007 | Implement RegisterPage frontend component | Frontend | UI | frontend-team | COMP-009, API-002, NFR-SEC-001 | Renders email/password/displayName form; client-side password validation; submits to POST /auth/register; handles 400/409 errors; auto-login on success; < 1s load time |
| COMP-008 | Implement ProfilePage frontend component | Frontend | UI | frontend-team | COMP-009, API-003, FR-AUTH-004 | Displays UserProfile (id, email, displayName, createdAt, timestamps, roles); protected by AuthProvider; < 1s load time |
| COMP-009 | Implement AuthProvider context provider | Frontend | Context | frontend-team | API-001, API-003, API-004, COMP-006–008 | Manages AuthToken state; silent refresh on token expiry; intercepts 401 responses and retries; redirects unauthenticated users to login; clears tokens on logout |
| API-005 | Implement POST /auth/reset-request endpoint | API | Backend | auth-team | COMP-001, Email Service, FR-AUTH-005 | Accepts email; generates reset token (1-hour TTL); sends email via SendGrid; returns success regardless of email existence (prevents enumeration) |
| API-006 | Implement POST /auth/reset-confirm endpoint | API | Backend | auth-team | COMP-001, COMP-004, FR-AUTH-005 | Validates reset token; hashes new password via PasswordHasher; updates UserProfile; revokes all refresh tokens; single-use token enforcement |
| FR-AUTH-005 | Password reset flow (functional req) | Feature | Requirement | product-team | API-005, API-006, TEST-004, NFR-COMP-002 | POST /auth/reset-request sends email with reset token; POST /auth/reset-confirm validates token (1-hour TTL), updates password hash, invalidates all sessions; > 80% completion rate in funnel |
| NFR-PERF-001 | API response time < 200ms p95 (non-functional req) | Non-Functional | Performance | qa-team | API-001–006, COMP-001–005 | APM instrumentation on AuthService methods; load test validates p95 latency; accepted during Phase 2 beta with 10% traffic |
| NFR-PERF-002 | Concurrent authentication 500 requests (non-functional req) | Non-Functional | Performance | qa-team | API-001, API-004, COMP-001–002 | k6 load test confirms 500 concurrent login requests; service scales horizontally without connection pool exhaustion |
| NFR-REL-001 | Service availability 99.9% uptime (non-functional req) | Non-Functional | Reliability | qa-team | API-001–006, MIG-002 | Uptime monitoring via health check endpoint; rolling 30-day window; acceptable during Phase 2 beta |
| NFR-COMP-001 | GDPR consent at registration (non-functional req) | Non-Functional | Compliance | compliance-team | DM-001 (with consentTimestamp field), COMP-007, API-002 | Users consent to data collection at registration; consent timestamp recorded in UserProfile; field retained for audit |
| NFR-COMP-002 | SOC2 audit logging 12-month retention (non-functional req) | Non-Functional | Compliance | compliance-team | COMP-001, DM-001, OPS systems | All auth events logged (login attempt, success/failure, password reset, token refresh); user ID, timestamp, IP, outcome recorded; 12-month retention in PostgreSQL |
| TEST-004 | Integration test: Registration persists UserProfile to database | Test | Integration | qa-team | COMP-007, API-002, DM-001, COMP-005 | Full flow: API request → PasswordHasher → PostgreSQL insert; 201 response; UserProfile persisted with correct hash and metadata |
| TEST-005 | Integration test: Expired refresh token rejected | Test | Integration | qa-team | COMP-002, API-004, Redis | testcontainers Redis; TokenManager validates TTL expiry; 401 response on expired token; token cleanup on expiry |
| TEST-006 | E2E test: User registers and logs in (Playwright) | Test | E2E | qa-team | COMP-006–009, API-001–004 | Complete journey: RegisterPage form → POST /auth/register → LoginPage form → POST /auth/login → ProfilePage display; AuthToken persists across page refresh |
| MIG-002 | Phase 2 – Beta 10% traffic rollout | Migration | Rollout | platform-team | All Phase 2 tasks, MIG-001 complete | Enable AUTH_NEW_LOGIN for 10% of traffic; monitor latency, error rates, Redis usage; rollback if p95 > 500ms or error rate > 0.1%; run for 2 weeks |
| MIG-004 | Feature flag AUTH_NEW_LOGIN | Migration | Feature Flag | platform-team | MIG-001 | Controls access to new LoginPage, RegisterPage, AuthService endpoints; default OFF; gates all new auth traffic; removable post-GA |
| MIG-005 | Feature flag AUTH_TOKEN_REFRESH | Migration | Feature Flag | platform-team | COMP-002, API-004 | Enables refresh token flow; when OFF, only access tokens issued; default OFF; removable after Phase 3 + 2 weeks |

**Risk Mitigations (Phase 2):**
- **R-002 (Brute-force attacks):** API Gateway rate limiting 10 req/min per IP; account lockout after 5 failed attempts; CAPTCHA added to LoginPage after 3 failures if needed.
- **R-004 (Low registration adoption):** Usability testing on RegisterPage; iterate based on funnel metrics (target > 60% conversion).
- **R-007 (Email delivery failures):** SendGrid delivery monitoring and alerting; fallback support channel for stuck password resets.

**Dependency Wiring (Phase 2):**
- **AuthProvider context** wires API interceptors: intercepts 401 responses, triggers token refresh via API-004, retries original request.
- **LoginPage and RegisterPage** dispatch requests through AuthProvider context methods, not directly to APIs.
- **Email service integration** wired into COMP-001 (AuthService) for FR-AUTH-005; uses SendGrid as external dependency.

**Critical Resolution Before Phase 2 Start:**
- **Confirm OQ-6 resolution:** If PRD wins (12-month retention), ensure DM-001 audit log schema supports 12-month lifecycle; update retention policy in OPS systems.
- **Confirm OQ-9 resolution:** Add `consentTimestamp` field to DM-001 UserProfile; update API-002 response schema to include consent; add GDPR consent checkbox to COMP-007 RegisterPage.
- **Finalize API-005 and API-006 specs:** Document request/response schemas, token TTL (1 hour), email send delay (immediate or async), rate limit (TBD).

**Phase 2 Success Criteria:**
- All COMP, API, FR, NFR (except NFR-SEC-001/002 validation), TEST-004–006, and MIG tasks completed
- Beta (MIG-002) runs for 2 weeks with < 200ms p95 login latency, < 0.1% error rate
- Registration conversion funnel > 50% (target > 60% by GA)
- Audit logging emits events for all auth operations; 12-month retention pipeline operational
- Zero P0/P1 bugs in beta; rollback capability tested

---

### Phase 3: Hardening, Operations & General Availability (Weeks 7–9)

**Goal:** Security hardening, operational readiness, and full deployment to 100% of traffic. Platform is production-ready, SOC2-compliant, and supportable by on-call teams.

**Personas & Value:** Jordan (admin) has runbooks and alerts for incident response. Platform achieves 99.9% uptime SLA. Compliance team passes SOC2 Type II audit Q3 2026.

**Milestones:**
- End Week 7: Security review complete; penetration testing performed; operational runbooks drafted (OPS-001–003); capacity plans finalized (OPS-004–006).
- End Week 8: All operational tasks complete; runbooks tested; alerts configured; on-call training delivered; rollback procedure validated (MIG-006).
- End Week 9: GA deployment (MIG-003); 100% of traffic routed through AuthService; monitoring dashboards green; support handoff complete.

**Task Rows:**

| ID | Task | Component | Type | Owner | Dependencies | Acceptance Criteria |
|----|------|-----------|------|-------|--------------|-------------------|
| NFR-SEC-001 | Penetration testing and security hardening (validation) | Non-Functional | Security | security-team | COMP-001–009, API-001–006 | Third-party pentest report filed; no P0/P1 findings; all P2+ mitigated before GA; token storage validation (HttpOnly, in-memory); CORS policy verified |
| NFR-SEC-002 | RSA key rotation capability and validation (validation) | Non-Functional | Security | auth-team | COMP-003, OPS systems | Key rotation procedure documented; quarterly rotation schedule confirmed; JwtService handles key version in token header; validation test passes |
| NFR-COMP-003 | NIST SP 800-63B password storage compliance (validation) | Non-Functional | Compliance | compliance-team | COMP-004, NFR-SEC-001 | Audit report confirms bcrypt cost 12 meets NIST adaptive hashing requirement; no plaintext password logging; compliance validation test passes |
| NFR-COMP-004 | GDPR data minimization validation | Non-Functional | Compliance | compliance-team | DM-001, COMP-007, API-002 | UserProfile schema contains only email, hashed password, displayName, consent timestamp; no extra PII; data collection policy signed off by legal |
| MIG-003 | Phase 3 – General Availability 100% traffic | Migration | Rollout | platform-team | All Phase 2 tasks, MIG-002 complete, OPS-001–006 ready | Remove AUTH_NEW_LOGIN feature flag; route all login/register traffic through AuthService; legacy auth endpoints deprecated; 99.9% uptime SLA monitored; rollback procedure ready |
| MIG-006 | Rollback Procedure (documentation and testing) | Migration | Operations | platform-team | MIG-001, MIG-002, MIG-003 | Steps documented: disable AUTH_NEW_LOGIN, verify legacy auth operational, investigate failure, restore backups if needed; procedure tested with > 95% confidence in 15-min restoration time |
| OPS-001 | Runbook – AuthService Down (documentation and testing) | Operational | Runbook | ops-team | COMP-001, Kubernetes, PostgreSQL | Symptoms, diagnosis steps, resolution procedure documented; tested with simulated pod failure; on-call responder can execute in < 15 minutes |
| OPS-002 | Runbook – Token Refresh Failures (documentation and testing) | Operational | Runbook | ops-team | COMP-002, Redis, JwtService | Symptoms (user logouts, 401 spikes), diagnosis (Redis connectivity, signing key access), resolution steps (Redis scaling, secrets re-mount); tested with Redis failure scenario |
| OPS-003 | On-Call Expectations (training and handoff) | Operational | Training | ops-team | OPS-001, OPS-002, OPS-004–006 | Auth-team provides 24/7 rotation first 2 weeks post-GA; P1 acknowledgment within 15 minutes; escalation path documented; on-call engineer trained on architecture, JWT lifecycle, Redis ops, PostgreSQL admin |
| OPS-004 | Capacity Planning – AuthService Pods (sizing and HPA) | Operational | Capacity | devops-team | COMP-001, Kubernetes | 3 replicas baseline; HPA scales to 10 replicas at CPU > 70%; resource requests/limits set; load test confirms 500 concurrent users supported |
| OPS-005 | Capacity Planning – PostgreSQL Connections (pool sizing) | Operational | Capacity | devops-team | COMP-005, pg-pool | 100-connection pool baseline; scaling trigger at wait time > 50ms; monitoring for connection exhaustion; backup strategy for high load |
| OPS-006 | Capacity Planning – Redis Memory (memory planning) | Operational | Capacity | devops-team | COMP-002, Redis | 1 GB baseline; 100K refresh tokens (~50 MB expected); scaling trigger at > 70% utilization; eviction policy set to allkeys-lru |

**Risk Mitigations (Phase 3):**
- **R-005 (Security breach from implementation flaws):** Penetration testing by third party; security review checklist; all findings remediated before GA.
- **R-006 (Compliance failure from audit logging):** Define log requirements early (Phase 1); validate against SOC2 controls in QA; audit log retention set to 12 months (resolves OQ-6).

**Dependency Verification (Phase 3):**
- All external dependencies confirmed operational: PostgreSQL 15+, Redis 7+, SendGrid API, Node.js 20 LTS, bcryptjs, jsonwebtoken.
- Observability infrastructure in place: APM tracing, Prometheus metrics, structured logging, alerts.
- Runbooks and incident response validated with simulated failures.

**Phase 3 Success Criteria:**
- All OPS tasks and migration tasks complete
- Security pentest clean (no P0/P1 findings)
- Operational readiness: runbooks tested, alerts configured, on-call rotation active
- Monitoring dashboards green: login p95 < 200ms, availability > 99.9%, error rate < 0.1%
- Rollback procedure validated and < 15-min restoration time achievable
- GA deployment (MIG-003) executed with zero customer impact

---

## Risk Assessment and Mitigation Strategies

**Summary of Risks from Extraction:**

| Risk ID | Risk | Severity | Probability | Mitigation | Contingency | Phase Addressed |
|---------|------|----------|------------|-----------|------------|-----------------|
| R-001 | Token theft via XSS | HIGH | Medium | In-memory accessToken; HttpOnly refresh token cookies; 15-min expiry; token clears on tab close | Immediate token revocation; force password reset | Phase 1 (design), Phase 2 (frontend) |
| R-002 | Brute-force attacks on login | MEDIUM | High | Rate limiting (10 req/min per IP); account lockout (5 failures in 15 min); bcrypt cost 12; CAPTCHA after 3 failures | WAF IP blocking; incident response | Phase 1 & 2 |
| R-003 | Data loss during migration | HIGH | Low | Parallel operation with legacy auth; idempotent migrations; full database backup before each phase | Rollback to legacy auth; restore from backup | Phase 1 & 2 (MIG-001, MIG-002) |
| R-004 | Low registration adoption due to poor UX | HIGH | Medium | Usability testing on RegisterPage; iterate based on funnel data; target > 60% conversion | Re-design RegisterPage flow; extend Phase 2 timeline | Phase 2 |
| R-005 | Security breach from implementation flaws | CRITICAL | Low | Security review; third-party pentest; no P0/P1 findings before GA | Full service rollback; force password resets | Phase 3 |
| R-006 | Compliance failure from audit logging | HIGH | Medium | Define log requirements early; validate against SOC2 controls; 12-month retention pipeline | Re-audit system; remediate log gaps | Phase 2 & 3 |
| R-007 | Email delivery failures blocking password reset | MEDIUM | Low | SendGrid delivery monitoring; alerting on failures; fallback support channel | Manual password resets via support | Phase 2 |

**Critical Resolution Gate:** OQ-6 (audit log retention conflict) must be resolved before Phase 2 begins. If PRD's 12-month retention requirement is adopted, Phase 2 PostgreSQL and archival strategy must account for 12-month lifecycle.

---

## Resource Requirements and Dependencies

**Team Structure:**
- **auth-team (5 FTE):** Backend engineers; implement COMP-001–005, API-001–006, migrations, operability
- **frontend-team (3 FTE):** Frontend engineers; implement COMP-006–009, integration with AuthProvider
- **qa-team (2 FTE):** QA engineers; test strategy, coverage, load testing, E2E automation
- **security-team (1 FTE, shared):** Security review, penetration testing, compliance validation
- **ops-team (1 FTE, shared):** Operational readiness, runbooks, capacity planning, on-call training
- **product-team (1 FTE):** Requirements ownership, success metrics tracking, stakeholder communication

**External Dependencies:**

| Dependency | Type | Provider | Availability Required | Risk Mitigation |
|-----------|------|----------|----------------------|-----------------|
| PostgreSQL 15+ | Infrastructure | Ops team | Before Phase 1 Week 1 | Backup/restore procedure; failover to read replica if needed |
| Redis 7+ | Infrastructure | Ops team | Before Phase 1 Week 1 | Cluster scaling; redundancy |
| Node.js 20 LTS | Runtime | Public | Before Phase 1 Week 1 | Version pinning; security patches applied immediately |
| SendGrid API | External service | SendGrid | Before Phase 2 Week 4 | Delivery monitoring; fallback support channel for reset flow |
| bcryptjs | npm package | npm | Before Phase 1 Week 1 | Version pinning; security audit; fallback to scryptjs if needed |
| jsonwebtoken | npm package | npm | Before Phase 1 Week 1 | Version pinning; security audit |
| Frontend routing framework | Internal | Frontend platform | Before Phase 2 Week 4 | Component acceptance criteria specify routing interfaces |
| SEC-POLICY-001 | Policy document | Compliance team | Before Phase 1 Week 1 | Password and token policies must be finalized; undefined policies block Phase 1 start |

**Budget/Capacity Impact:**
- **Phase 1:** 5 FTE auth-team + 1 FTE QA = 6 FTE (weeks 1–3)
- **Phase 2:** 5 FTE auth-team + 3 FTE frontend-team + 2 FTE QA + 1 FTE security (pentest) = 11 FTE (weeks 4–6)
- **Phase 3:** 5 FTE auth-team + 1 FTE ops + 1 FTE security (validation) = 7 FTE (weeks 7–9)
- **Ongoing post-GA:** 2 FTE auth-team (on-call) + 1 FTE ops

---

## Success Criteria and Validation Approach

**Quantitative Success Metrics (from PRD S19 and Extraction):**

| Metric | Target | Measurement Method | Owner | Validation Frequency |
|--------|--------|--------------------|-------|----------------------|
| SC-001: Login response time (p95) | < 200ms | APM instrumentation on AuthService.login(); sampled over first 7 days of GA | qa-team + ops-team | Real-time dashboard; weekly review |
| SC-002: Registration success rate | > 99% | (successful registrations / attempts); monitored during Phase 2 beta and GA | product-team | Daily funnel dashboard |
| SC-003: Token refresh latency (p95) | < 100ms | APM instrumentation on TokenManager.refresh(); sampled under load | qa-team | Real-time dashboard |
| SC-004: Service availability | 99.9% uptime | Health check monitoring via continuous ping; rolling 30-day window; SLA tracked post-GA | ops-team | Weekly SLA report |
| SC-005: Password hash time | < 500ms | Benchmark of PasswordHasher.hash() with bcrypt cost 12; unit test validates | qa-team | Per-release benchmark |
| SC-006: Registration conversion (funnel) | > 60% | (confirmed accounts / landing page visits); tracked from GA onward | product-team | Weekly metrics review |
| SC-007: Daily active authenticated users | > 1000 within 30 days of GA | AuthToken issuance count; cumulative new users | product-team | Daily dashboard |
| SC-008: Average session duration | > 30 minutes | Token refresh event analytics; time between login and logout/expiry | product-team | Weekly metrics review |
| SC-009: Failed login rate | < 5% of attempts | (failed login attempts / total attempts); monitored via auth event logs | ops-team | Daily monitoring; alert > 5% |
| SC-010: Password reset completion (funnel) | > 80% | (new passwords set / reset emails sent); tracked post-launch | product-team | Weekly funnel review |

**Qualitative Validation (Phase 3):**

| Gate | Validation | Owner | Approval |
|------|-----------|-------|----------|
| Security posture | Penetration test report; zero P0/P1 findings; security review checklist signed off | security-team | CISO or security lead |
| Operational readiness | Runbooks tested with simulated failures; on-call engineer can execute > 95% within 15 min | ops-team | Ops manager |
| Compliance | SOC2 audit logging validated; 12-month retention pipeline operational; GDPR consent collected; NIST password hashing confirmed | compliance-team | Compliance officer |
| Product quality | Usability testing shows > 60% registration conversion; zero P0 bugs in beta; NPS > 6.5 from beta users | product-team | Product manager |

**Post-Launch Monitoring (Phase 3+):**
- Daily SLO dashboard: login latency, availability, error rates, registration conversion
- Weekly metrics review: user growth, session duration, reset completion rate, failed login trends
- Monthly post-incident reviews: incident frequency, MTTR, customer impact
- Quarterly compliance audit: log retention, consent tracking, NIST compliance

---

## Timeline Estimates per Phase

**Phase 1: Backend Foundation & Core Services — 3 weeks**

| Week | Deliverables | Confidence |
|------|--------------|-----------|
| Week 1 | DM-001, DM-002, COMP-001–002 designed; PostgreSQL schema deployed; feature flag infra ready | High (90%) |
| Week 2 | COMP-003–005, API-001–004 implemented; TEST-001–003 passing; unit test coverage > 80% | High (85%) |
| Week 3 | MIG-001 staged deployment; internal alpha launch with auth-team + QA; bug fixes; readiness gate for Phase 2 | High (80%) |

**Phase 2: Frontend Integration & Advanced Flows — 3 weeks**

| Week | Deliverables | Confidence |
|------|--------------|-----------|
| Week 4 | COMP-006–009 implemented; PASSWORD reset endpoints (API-005, API-006) designed; frontend tests drafted | Medium (75%) |
| Week 5 | All frontend components integrated with AuthProvider; TEST-004–005 passing; SendGrid integration live; MIG-002 beta rollout (10% traffic) | Medium (70%) |
| Week 6 | Beta stable for 2 weeks; registration conversion > 50%; password reset flow working; funnel analytics established; readiness gate for Phase 3 | Medium (65%) |

**Phase 3: Hardening, Operations & GA — 3 weeks**

| Week | Deliverables | Confidence |
|------|--------------|-----------|
| Week 7 | Security pentest complete; OPS-001–003 runbooks drafted; capacity plans finalized (OPS-004–006); on-call training scheduled | Medium (70%) |
| Week 8 | Runbooks tested; alerts configured; security findings remediated; rollback procedure validated; go/no-go decision | High (80%) |
| Week 9 | MIG-003 GA deployment; 100% traffic routed to AuthService; monitoring stable; support handoff; retrospective on Phase 1–3 | Medium (70%) |

**Total Timeline: 9 weeks (approximately 2 calendar months for a well-coordinated team)**

**Confidence Notes:**
- High confidence (85%+): Backend services, APIs, data models, basic testing — well-scoped, proven technologies.
- Medium confidence (70–80%): Frontend integration, E2E testing, operational readiness — some unknowns around load test results and issue discovery.
- Lower confidence (< 70%): Security pentest findings, scalability under production load, on-call team ramp-up — dependent on external factors and people.

**Buffer Recommendations:**
- Add 1–2 weeks contingency for P1 bug fixes discovered during Phase 1 or 2.
- Phase 3 security pentest may uncover issues requiring rework; add 1 week if findings are significant.
- Post-GA on-call ramp-up should extend 2 weeks past Phase 3 to stabilize and respond to production issues.

---

## Architecture Integration Points

**Primary Dispatch Mechanisms:**

1. **AuthService Orchestrator (COMP-001)**
   - **Named Artifact:** AuthService class with methods: `login()`, `register()`, `getProfile()`, `initiatePasswordReset()`, `confirmPasswordReset()`
   - **Wired Components:** PasswordHasher (COMP-004), TokenManager (COMP-002), UserRepo (COMP-005)
   - **Owning Phase:** Phase 1 (implementation in weeks 1–3)
   - **Consuming Phases:** Phase 2 (frontend API calls to AuthService endpoints), Phase 3 (observability and operational support)

2. **TokenManager Lifecycle (COMP-002)**
   - **Named Artifact:** TokenManager class with methods: `issueTokens()`, `refreshTokens()`, `revokeRefreshToken()`, `validateAccessToken()`
   - **Wired Components:** JwtService (COMP-003), Redis (external storage), DM-002 (AuthToken structure)
   - **Owning Phase:** Phase 1 (weeks 1–3)
   - **Consuming Phases:** Phase 2 (frontend AuthProvider calls refresh), Phase 3 (operational monitoring of token lifecycle)

3. **AuthProvider Context (COMP-009)**
   - **Named Artifact:** AuthProvider context with interceptors for API calls and 401 response handling
   - **Wired Components:** LoginPage (COMP-006), RegisterPage (COMP-007), ProfilePage (COMP-008); API-001, API-003, API-004
   - **Owning Phase:** Phase 2 (weeks 4–6)
   - **Consuming Phases:** Phase 3 (operational support for frontend session handling)

**Dependency Injection Strategy:**
- AuthService constructor receives instances of PasswordHasher, TokenManager, UserRepo.
- TokenManager constructor receives instance of JwtService.
- No global singletons; enables testing with mocks.

**Error Propagation:**
- All backend services return structured error responses: `{ error: { code, message, status } }`
- AuthProvider catches 401 responses and triggers token refresh via TokenManager.refresh(); retries original request.
- All error codes enumerated in Phase 1 API design.

---

## Appendix: Open Questions Requiring Stakeholder Resolution

**BLOCKING Phase 2 Start:**

| OQ # | Question | Source | Owner | Impact if Unresolved |
|------|----------|--------|-------|----------------------|
| OQ-6 | **Audit log retention conflict:** TDD §7.2 specifies 90 days; PRD §S17 requires 12 months for SOC2. Which governs? | Extraction gap | auth-team + compliance | If TDD (90 days) implemented, SOC2 audit fails Q3 2026. If PRD (12 months), archival infrastructure must scale. |
| OQ-9 | **GDPR consent field missing:** NFR-COMP-001 requires consent timestamp at registration. `UserProfile` schema lacks field. | Extraction gap | Engineering | GDPR compliance gap. Feature cannot ship without consent tracking. |
| OQ-10 | **Password reset endpoints unspecified:** FR-AUTH-005 references `/auth/reset-request` and `/auth/reset-confirm` but TDD §8 lacks detailed specs. | TDD gap | Engineering | Phase 2 implementation blocked without endpoint request/response schemas, token TTL, email send behavior. |

**DEFERRED to Phase 2+ (Non-Blocking):**

| OQ # | Question | Source | Owner | Impact |
|------|----------|--------|-------|--------|
| OQ-1 | Should `AuthService` support API key authentication for service-to-service calls? | TDD | test-lead | Deferred to v1.1; not in scope for v1.0 GA |
| OQ-2 | Max allowed `UserProfile` roles array length? | TDD | auth-team | Design: assume 10 for now; revisit if RBAC grows beyond this |
| OQ-3 | Password reset email sent synchronously or asynchronously? | PRD | Engineering | Recommend async with queue; sync acceptable if latency < 500ms |
| OQ-4 | Max refresh tokens per user across devices? | PRD | Product | Design: no limit for v1.0; rate limit refresh calls instead |
| OQ-5 | "Remember me" to extend session duration? | PRD | Product | Deferred to v1.1; v1.0 uses fixed 7-day refresh window |
| OQ-7 | **Logout endpoint missing:** PRD Epic AUTH-E1 includes logout user story; TDD defines no logout endpoint. | PRD/TDD gap | Engineering | Implement `POST /auth/logout` in Phase 2 to support "log out to secure on shared device" JTBD. |
| OQ-8 | **Admin audit log query missing:** Jordan (admin) persona requires queryable auth logs (by date/user). TDD §14 defines log emission but no query API. | PRD/TDD gap | Product + Engineering | Defer to v1.1; v1.0 logs events; v1.1 adds admin query API. Document in roadmap. |

---

## Phased Resource Allocation Summary

**Total Project Capacity: ~22 FTE-weeks**

- **Phase 1:** 6 FTE × 3 weeks = 18 FTE-weeks
- **Phase 2:** 11 FTE × 3 weeks = 33 FTE-weeks
- **Phase 3:** 7 FTE × 3 weeks = 21 FTE-weeks
- **Post-GA on-call:** 3 FTE × 2 weeks = 6 FTE-weeks

**Critical Path:**
1. Database schema (DM-001, DM-002) — required before any service implementation
2. AuthService, PasswordHasher, TokenManager (COMP-001–003) — required before API endpoints
3. Frontend components (COMP-006–009) — required before Phase 2 completion
4. Security review and pentest — required before Phase 3 completion

**Sequencing Constraint:** Phase 2 cannot start until Phase 1 is 100% complete; Phase 3 cannot start until Phase 2 is 100% complete. No overlap due to tight frontend-backend coupling via API contracts.

---

## Recommendation to Architect Stakeholders

**Go/No-Go Readiness:**

- **Start Phase 1 immediately** if SEC-POLICY-001 (security policy) is finalized. Non-blocking prerequisites (PostgreSQL, Redis, SendGrid configs) should be provisioned in parallel.
- **Resolve OQ-6, OQ-9, OQ-10 before Phase 2 kickoff** (end of Week 3). A 1-week delay to finalize these gates is preferable to rework at Phase 2 midpoint.
- **Expect Phase 2 scope creep** around password reset and email deliverability. Budget 1–2 additional days for edge cases (email bounce handling, retry logic).
- **Staffing risk:** Frontend-team availability is critical path. If frontend capacity is unavailable Week 4–6, phase Phase 2 into Phase 2a (backend polish) and Phase 2b (frontend push), extending timeline by 1–2 weeks.

**Strategic Value Realization:**
- **Week 3 (Phase 1 complete):** Platform gains ability to track users in log data. Internal team testing begins. Compliance team can validate audit logging infrastructure.
- **Week 6 (Phase 2 complete, beta stable):** First 10% of users onboard on new authentication. Product metrics (registration conversion, login latency) measurable. Personalization feature development can begin (decoupled from auth completion).
- **Week 9 (Phase 3 complete, GA):** Platform achieves user identity layer. SOC2 audit path clearer (Q3 deadline achievable if compliance work stays on track). Personalization roadmap unblocks.

**Architectural Debt Incurred:**
- v1.0 does **not** include logout endpoint (OQ-7) — frontend must manually clear AuthToken on logout intent; no backend session termination mechanism.
- v1.0 does **not** include admin audit log query API (OQ-8) — compliance team must query PostgreSQL directly until v1.1.
- v1.0 does **not** support social login or MFA — both deferred to v1.1+.

**Recommended Monitoring Posture:**
- Real-time SLO dashboard during Phase 2 beta and Phase 3 GA.
- Weekly metrics reviews (product metrics, operational SLIs, error logs).
- Incident response training for on-call team before Phase 3 GA.
- Post-launch retrospective scheduled for 2 weeks after Phase 3 completion.
