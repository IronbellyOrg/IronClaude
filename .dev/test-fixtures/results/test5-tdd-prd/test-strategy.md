---
complexity_class: HIGH
validation_philosophy: continuous-parallel
validation_milestones: 5
work_milestones: 5
interleave_ratio: 1:1
major_issue_policy: stop-and-fix
spec_source: test-tdd-user-auth.md
generated: "2026-04-20T19:20:15.126663+00:00"
generator: superclaude-roadmap-executor
---

# Test Strategy — User Authentication Service (AUTH-001)

## 1. Validation Philosophy and Interleave Ratio

**Ratio justification (1:1):** Roadmap complexity_class=HIGH (0.78) with five technically-layered work milestones (M1–M5) each carrying P0 deliverables and regulated exit criteria (SOC2 audit log, NIST SP 800-63B password storage, bcrypt cost 12, RS256 2048-bit, pen-test PASS). Security-critical crypto primitives, dual-store persistence, and phased flag-gated rollout cannot tolerate validation debt. Every work milestone is paired with a validation milestone (V1–V5) that **runs continuously in parallel** with work and **gates its exit**.

**Major issue policy (stop-and-fix):** MAJOR or CRITICAL issues halt milestone exit; MINOR tracked; COSMETIC backlogged.

## 2. Validation Milestones Mapped to Roadmap

**V1: Foundation Validation** | parallel with M1 (2026-03-30→2026-04-10) | gates M1 exit
**V2: Core Logic Validation** | parallel with M2 (2026-04-13→2026-04-24) | gates M2 exit
**V3: Integration & Tokens Validation** | parallel with M3 (2026-04-27→2026-05-15) | gates M3 exit
**V4: Security, Compliance & Load Validation** | parallel with M4 (2026-05-18→2026-05-29) | gates M4 exit
**V5: Production Readiness Validation** | parallel with M5 (2026-06-01→2026-06-12) | gates GA 2026-06-09

## 3. Test Categories

| Category | Tooling (from TDD §15) | Coverage Target | Primary Scope |
|---|---|---|---|
| Unit | Jest, ts-jest | 80% lines + 80% branches (COVERAGE-GATE, M4) | AuthService, TokenManager, JwtService, PasswordHasher, UserRepo |
| Integration | Supertest, testcontainers (PostgreSQL 15, Redis 7) | 15% of pyramid | API endpoints, DB ops, Redis TTL, cross-component flow |
| E2E | Playwright | 5% of pyramid | LoginPage→RegisterPage→ProfilePage journey, reset flow, silent refresh |
| Contract | OpenAPI validator + Schemathesis | 100% of /v1/auth/* endpoints | Request/response schemas, error envelope, status codes, rate limits |
| Data-model | SQL migration tests + Zod/TS-type assertions | 100% of DM-001..004 | Field constraints, indexes, FK, partitioning |
| Performance | k6 | NFR-PERF-001 (<200ms p95), NFR-PERF-002 (500 concurrent, 1000 RPS) | /auth/login, /auth/register, /auth/refresh, /auth/me, mixed workload |
| Security | SAST (Semgrep), DAST (OWASP ZAP), external pen-test | Zero High/Critical at M4 exit | OWASP Top 10, JWT algorithm confusion, timing attacks, credential stuffing, token replay |
| Compliance | Custom audit-log replay + retention assertions | 100% SOC2 event coverage | NFR-COMP-001 (GDPR consent), NFR-COMP-002 (SOC2 12-month), NFR-COMP-003 (NIST SP 800-63B) |
| Chaos/Reliability | Toxiproxy + manual outage injection | 3 failure modes (Redis, Postgres, SendGrid) | Graceful degradation, runbook validation, rollback triggers |
| Acceptance (persona) | Playwright + manual scripts | 3 personas × ≥1 primary workflow | Alex (E2E signup <60s), Jordan (admin audit/lock), Sam (programmatic refresh) |
| KPI validation | Funnel analytics + Grafana + synthetic probes | 5 PRD metrics | Registration conversion, login p95, session >30min, failed-login rate <5%, reset completion >80% |
| Migration rollback | DB snapshot + flag-flip drill | 3 phases (MIG-001/002/003) | Legacy→new parity, idempotent upsert, full-backup restore |
| Operational readiness | Runbook dry-run + alert shadow | 2 runbooks (OPS-001/002) + 5 alert rules | OBS-007/008/009, ORT, on-call response <15min |

## 4. Test-Implementation Interleaving Strategy

Continuous-parallel execution inside every milestone:

- **Day 0–2:** Validation team authors acceptance criteria review, derives contract tests from OpenAPI + DM schemas, writes test skeletons alongside scaffolding.
- **Mid-milestone:** Unit + integration tests land with each deliverable PR; CI gates every PR on coverage floor and contract check.
- **Final 20%:** E2E, performance, security, compliance scans run nightly; on-call dry-runs and runbook reviews executed.
- **Exit gate:** All validation milestone criteria green → work milestone closes. Any MAJOR/CRITICAL issue triggers stop-and-fix.

## 5. Risk-Based Test Prioritization

| Priority | Risks (from Risk Register) | Test Emphasis |
|---|---|---|
| P0 — Critical | R-001 XSS/token theft, R-003 data loss in migration, R-004 compliance gap, R-PRD-002 security breach | SEC-AUDIT-TOKEN, DATA-MIG-SCRIPT dry-run, NFR-COMP-001/002 assertions, full pen-test (SEC-006), CSP+HttpOnly cookie verification |
| P1 — High | R-005 bcrypt latency, R-006 RSA rotation, R-009 observability capacity, R-010 frontend clock skew | PERF-BASELINE (M2), RSA-KEY-ROTATION drill (M3 staging), FE-CLOCK-SKEW unit + E2E with clock-drift simulation, load test at 500/1000 concurrent |
| P2 — Medium | R-002 brute-force, R-007 SendGrid outage, R-008 CAPTCHA integration, R-018 rate-limit calibration, R-019 refresh cap friction | SEC-001 lockout test, CAPTCHA-INTEG spike test, async queue DLQ drill, rate-limit boundary tests, refresh-cap-5 eviction E2E |
| P3 — Low | R-020 flag-removal debt, R-011 legacy consumer deprecation, R-017 admin PII leak | Static analysis for stale flags, 410+Sunset header assertion, admin error-envelope PII scan |

## 6. Milestone-by-Milestone Validation Detail

### V1: Foundation Validation (gates M1 exit)

**What to test:**
- **Schema validation (DM-001..004):** Apply migrations to empty Postgres 15 testcontainer; assert column types, UNIQUE on email (lowercased), partitioning declared on auth_audit_log, unique token_hash on password_reset_tokens, FK integrity.
- **Infra smoke (DEP-001..007):** pg-pool connects with 100-size pool; Redis SET/EXPIRE=604800 verified; SendGrid sandbox send succeeds; Node 20 LTS boot; bcryptjs benchmark <500ms at cost=12 on target hardware.
- **Security baseline (NFR-SEC-002, NFR-SEC-003):** JwtService init fails fast if alg≠RS256 or key<2048 bits; log-redaction middleware unit test asserts `password`, `accessToken`, `refreshToken`, `newPassword` never serialized; TLS 1.3 handshake via ssllabs.com grade ≥A.
- **Feature-flag registration:** AUTH_NEW_LOGIN and AUTH_TOKEN_REFRESH default OFF, runtime toggle without redeploy.
- **Error envelope (ERR-ENV-001):** Middleware unit test asserts envelope shape on all 4xx/5xx; error-code registry complete.
- **Decision gates:** OQ-CONFLICT-1 (12-month retention) documented; OQ-PRD-3 (lockout 5/15min) documented.

**Acceptance criteria:** 100% of M1 deliverable IDs have ≥1 automated test; CI green; 3/4 blocking OQs closed; infra smoke passes in staging; sec-reviewer signs off on key config.

**Exit gate:** Zero CRITICAL/MAJOR; OQ-CONFLICT-1 + OQ-PRD-3 closed.

### V2: Core Logic Validation (gates M2 exit)

**Named test cases (from TDD §15):**
- **TEST-001** Unit — Login with valid credentials returns AuthToken (AuthService + mocked PasswordHasher + TokenManager).
- **TEST-002** Unit — Login with invalid credentials returns 401, no AuthToken issued, failed-attempt counter incremented.
- **TEST-004** Integration — Registration persists UserProfile to testcontainer Postgres with bcrypt hash starting `$2b$12$`.
- **TEST-DUP-EMAIL** Integration — Second register with same email returns 409, only one row; case-insensitive (E@X.com vs e@x.com).
- **TEST-WEAK-PWD** Integration — Passwords "short", "longpass1", "LongPass" rejected with structured error list; "LongPass1!" accepted.

**What to test:**
- **FR-AUTH-001/002 contract:** API-001 (/v1/auth/login) and API-002 (/v1/auth/register) Schemathesis run against OpenAPI spec; 200/201/400/401/409/423/429 all produced.
- **SEC-003 password policy:** ≥8 chars, uppercase, digit, symbol; NIST SP 800-63B section 5.1.1.2 conformance.
- **SEC-004 user enumeration:** Timing variance <50ms between known/unknown email paths; identical 401 envelope; dummy bcrypt.verify on unknown email.
- **NFR-SEC-001:** Config validation refuses BCRYPT_COST<10; hash prefix asserted.
- **PERF-BASELINE:** k6 at 10/25/50 concurrent login; capture p95 baseline for M3 comparison.
- **NFR-COMP-001-stub:** Registration rejects missing consent; consent_timestamp persisted.
- **SEC-LOGGING-M2:** Structured log emitted on each auth event; automated PII scanner asserts zero password/token in logs.
- **OpenAPI spec (DOC-API-M2):** Published spec validated; all error codes enumerated.

**Acceptance criteria:** Unit coverage on AuthService+PasswordHasher+UserRepo ≥80% lines+branches; TEST-001/002/004/DUP-EMAIL/WEAK-PWD green; preliminary p95<200ms; zero PII matches in log grep audit.

**Exit gate:** All P0 unit+integration green; PERF-BASELINE report filed; architecture review (REFLECT-M2) signed off by sys-architect.

### V3: Integration & Tokens Validation (gates M3 exit)

**Named test cases:**
- **TEST-003** Unit — TokenManager.refresh rotates pair; Redis GET→SET/DEL asserted; JwtService.sign called twice.
- **TEST-005** Integration — Expired refresh token: testcontainer Redis SET TTL=1s, sleep 2s, /v1/auth/refresh returns 401 AUTH_TOKEN_EXPIRED.
- **TEST-REVOKE** Integration — Refresh→revoke→refresh-again returns 401 AUTH_TOKEN_REVOKED.
- **TEST-RESET-FLOW** Integration — Full reset flow: request→token persisted with 1h TTL→confirm updates bcrypt hash→all refresh tokens for user deleted; reset token single-use.
- **TEST-006** E2E — RegisterPage→LoginPage→ProfilePage Playwright journey; silent refresh observed in network log.
- **TEST-E2E-RESET** E2E — Forgot-password flow; mock-email intercept extracts token; confirm; old password rejected; pre-existing session on 2nd browser context logs out.
- **CORS-PREFLIGHT-TEST** Integration — OPTIONS returns 204 + Allow-Origin for app.platform.com, 403 for evil.com.

**What to test:**
- **FR-AUTH-003/004/005:** API-003/004/005/006 contract-tested; refresh-token cap=5 with oldest-eviction verified (OQ-PRD-2); per-user cap telemetry emitted.
- **JwtService correctness:** RS256 asserted; alg=none/HS256 token rejected; clock-skew=5s tolerance; iss/aud claims validated.
- **NFR-PERF-001-M3:** k6 at 50/100/250 concurrent; p95<200ms for login, refresh, me, reset-request.
- **NFR-PERF-002:** k6 at 500 concurrent login for ≥2 min; p95<200ms; error rate <0.1%; pg-pool wait<50ms; Redis latency<10ms.
- **SEC-001 lockout:** 5 failures/15min → 423; 6th attempt within window returns 423; successful login clears counter.
- **CONFLICT-2 redirect:** RegisterPage 201 → /login?email=... prefilled (TDD §8.2).
- **ADMIN-001 role-gate:** GET /v1/auth/admin/events returns 403 for non-admin JWT; 200 for admin.
- **PRD-GAP-LOGOUT:** POST /v1/auth/logout revokes current refresh; subsequent refresh returns 401.
- **FE-CLOCK-SKEW:** AuthProvider refresh timer = exp−60s; clock-drift simulation E2E.
- **FE-ERROR-HANDLING:** Each of 7 error codes maps to UX message; unit test per code.
- **RSA-KEY-ROTATION:** Staging drill with overlap window verified.

**Acceptance criteria:** Coverage ≥80% on TokenManager+JwtService; all 7 integration tests green; TEST-006 + TEST-E2E-RESET green in CI nightly; NFR-PERF-001-M3 + NFR-PERF-002 p95<200ms at 500 concurrent; OpenAPI spec (DOC-API-M3) complete for 7 endpoints.

**Exit gate:** 10% beta dashboards published and reviewed; rollback playbook reviewed; REFLECT-M3 sign-off from sys-architect + sec-reviewer.

### V4: Security, Compliance & Load Validation (gates M4 exit)

**Named test cases (new for M4):**
- **LOAD-TEST-FULL** — k6 mixed workload 60% login / 15% register / 15% refresh / 10% me at 500 concurrent for 30 min; 1000 RPS sustained; p95<200ms; error rate<0.1%; HPA scaling observed.
- **NFR-COMP-002-RETENTION** — Insert audit record with created_at = now−400d; trigger pg_partman; assert partition pruned; 12-month retention enforced.
- **NFR-COMP-001-CONSENT** — 100% registration records have consent=true + consent_version stored; DSAR export stub returns consent record + UserProfile.
- **SEC-AUDIT-TOKEN** — JWT alg=none rejected; HS256 rejected when RS256 expected; iss/aud mismatch rejected; revocation effective across sibling tabs.
- **RELIABILITY-READINESS** — Toxiproxy: Redis-down → /auth/refresh 503 AUTH_REFRESH_UNAVAILABLE (not 500); Postgres-down → writes 503; SendGrid-down → reset-request still 200, DLQ grows, alert fires.
- **AUDIT-002-COVERAGE** — Synthetic replay: login_success/login_failure/register/refresh/reset_request/reset_confirm/lockout/unlock/logout all produce audit_log rows with required SOC2 fields.
- **API-009/010 admin lock/unlock** — Admin JWT locks user, user login returns 423, unlock restores access, every action logged to audit via AdminAuthEventService.
- **API-011 /v1/health** — Returns 200 with `{status, dependencies:{pst,redis,sendgrid}}`; 503 if any critical dep down; unauthenticated.

**What to test:**
- **OBS-001..009:** Every method emits structured log with trace_id; metrics registered; OpenTelemetry spans traceable end-to-end in Tempo/Jaeger; alert rules fire against synthetic load.
- **OBS-ROLLBACK-TRIGGERS:** Four rollback alert rules distinct from degradation alerts; dry-run in staging; human-confirmation gate verified.
- **SEC-005 security review:** Written report; zero High/Critical unaddressed.
- **SEC-006 pen-test:** External vendor, 1-week window, OWASP Top 10 + credential stuffing + token replay + JWT algorithm confusion + timing attacks; zero High/Critical at exit.
- **SEC-CSP:** CSP header set; no inline scripts in LoginPage/RegisterPage/AuthProvider; report-uri captures violations.
- **NFR-COMP-003:** Conformance checklist linked to NIST SP 800-63B §5.1.1.2; reviewed by sec-reviewer.
- **COVERAGE-GATE:** CI enforces ≥80% lines+branches on AuthService/TokenManager/JwtService/PasswordHasher/UserRepo.
- **OPS-008-prep:** 48h alert shadow; false-positive rate <10%; on-call dry-run 15min ack SLA.

**Compliance test category (PRD S17-derived):**
- GDPR consent capture: 100% of registration rows have consent_timestamp + consent_version; DSAR stub export verified.
- SOC2 Type II audit-log: 12-month retention enforced; all 9 event types persisted; sample review by compliance officer.
- NIST SP 800-63B: bcrypt cost 12; no plaintext; no reversible encoding; no password hints; validated via test vectors.
- Data minimization: schema contains only email, password_hash, displayName, consent metadata; no additional PII.

**Acceptance criteria:** Pen-test PASS (zero High/Critical); LOAD-TEST-FULL achieves 1000 RPS for 30min within latency budget; compliance sign-off captured; all 4 Grafana dashboards live; rollback triggers dry-run passed.

**Exit gate:** SOC2 sample review pass; CSP + HttpOnly cookie + TLS 1.3 + log redaction + CORS verified end-to-end; admin lock/unlock + /v1/health exercised.

### V5: Production Readiness Validation (gates GA 2026-06-09)

**What to test:**
- **MIG-002 10% ramp:** 1%→5%→10% staged; SLO dashboards green; rollback playbook drilled in prod-shadow mode.
- **MIG-003 100% GA:** Legacy /auth/* returns 410 Gone with Sunset header; new service serves 100% traffic; 7-day uptime ≥99.9%.
- **OPS-001/002 runbook dry-run:** AuthService down + token refresh failures scenarios executed in staging; on-call 15min ack SLA demonstrated.
- **OPS-004/005/006 capacity:** HPA scales 3→10 under load; pg-pool stays below 50ms wait; Redis memory <70% at projected 500K tokens × cap=5.
- **FLAG-REMOVAL:** CI check for stale AUTH_NEW_LOGIN references post-GA; AUTH_TOKEN_REFRESH removal PR ready for GA+2w.
- **LEGACY-DEPRECATION:** 410 + Sunset: 2026-09-07 header asserted on all legacy routes.
- **KPI validation (PRD S19 metrics):** Registration conversion >60% (funnel), login p95 <200ms (APM), avg session >30min (refresh event analytics), failed-login rate <5% (audit log analysis), reset completion >80% (funnel).
- **Persona acceptance tests:** Alex — signup in <60s E2E; Jordan — query audit events + lock/unlock user via admin API; Sam — programmatic refresh with 15-min access token and clear error codes.
- **Customer journey E2E (PRD S22):** First-Time Signup, Returning User Login with silent refresh, Password Reset, Profile Management — all four journeys Playwright-covered.
- **ROLLBACK-AUTOMATION readiness:** Human-confirmed mode verified for first 30 days; auto-fire promotion scheduled for 2026-07-09.

**Acceptance criteria:** All 17 Success Criteria (roadmap §"Success Criteria and Validation Approach") with M5 landing slot green; TDD §24.2 release checklist ticked; POST-GA-REVIEW scheduled for 2026-06-16.

**Exit gate:** GA sign-off from test-lead + eng-manager; on-call rotation staffed; V1.1-BACKLOG captured for 9 deferred OQs.

## 7. Quality Gates Between Milestones

| Gate | Blocks | Criteria (stop-and-fix applies to all) |
|---|---|---|
| G1: M1→M2 | Start of core logic | All schemas migrated; infra smoke green; OQ-CONFLICT-1 + OQ-PRD-3 closed; error envelope + redaction middleware active |
| G2: M2→M3 | Start of token integration | TEST-001/002/004/DUP-EMAIL/WEAK-PWD green; unit coverage ≥80% on AuthService+PasswordHasher+UserRepo; PERF-BASELINE report filed; zero PII in logs |
| G3: M3→M4 | Start of hardening | TEST-003/005/REVOKE/RESET-FLOW/006/E2E-RESET green; NFR-PERF-002 at 500 concurrent passing; refresh cap=5 with eviction verified; CONFLICT-2 redirect live |
| G4: M4→M5 | Start of rollout | Pen-test PASS (zero High/Critical); SOC2 compliance sign-off; LOAD-TEST-FULL 1000 RPS pass; coverage gate enforced; rollback triggers dry-run passed |
| G5: M5→GA | Production traffic | 10% beta stable 2 weeks; uptime ≥99.9% over 7 days; runbook dry-run successful; legacy deprecation live with Sunset 2026-09-07; all 5 PRD KPIs measurable |

## 8. Issue Classification and Actions

| Severity | Examples | Action |
|---|---|---|
| CRITICAL | Plaintext password in logs; JWT alg=none accepted; data loss in migration; pen-test High finding | Stop-and-fix immediately; milestone halted; incident channel opened |
| MAJOR | p95 breach of NFR-PERF-001; audit-log event missing; refresh-token replay possible; CSP bypass | Stop-and-fix before next milestone exit; blocks G-gate |
| MINOR | Flaky E2E test; dashboard label typo; rate-limit threshold off-by-one; runbook paragraph out-of-date | Tracked in V1.1-BACKLOG; no gate impact |
| COSMETIC | Log message formatting; OpenAPI description wording; test-fixture naming | Backlog; no gate impact |

## 9. Tooling Summary (from TDD §15 + inferred)

Jest + ts-jest (unit), Supertest + testcontainers (integration, Postgres 15 + Redis 7), Playwright (E2E), k6 (load), Semgrep (SAST), OWASP ZAP (DAST), external pen-test vendor (M4), Prometheus + Grafana + Tempo/Jaeger (observability), Toxiproxy (chaos), Schemathesis (OpenAPI contract), pg_partman (retention).
