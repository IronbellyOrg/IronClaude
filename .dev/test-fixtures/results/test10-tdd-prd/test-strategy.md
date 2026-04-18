---
complexity_class: MEDIUM
validation_philosophy: continuous-parallel
validation_milestones: 5
work_milestones: 5
interleave_ratio: 1:2
major_issue_policy: stop-and-fix
spec_source: test-tdd-user-auth.md
generated: "2026-04-16T17:02:00.620865+00:00"
generator: superclaude-roadmap-executor
---

# User Authentication Service — Test Strategy

## Validation Milestones (Mapped to Roadmap Phases)

**V1 (Phase 1 exit)** | Infrastructure & Schema Contract Validation | 2 days | Exit: all 6 schemas (DM-001–DM-006) pass contract tests; RS256 key signing verified; PostgreSQL/Redis health probes green; bcrypt cost=12 benchmark <500ms
**V2 (Phase 2 exit)** | Backend Flow & API Contract Validation | 3 days | Exit: TEST-001–TEST-005, TEST-007, TEST-008 green; all 8 endpoints return spec-compliant responses; audit events emitted for every auth action; consent captured with policyVersion
**V3 (Phase 3 exit)** | E2E Journey & Persona UX Validation | 3 days | Exit: TEST-006, TEST-009–TEST-012 green across Alex/Jordan/Sam persona flows; silent refresh dedup verified; route guards enforce correctly
**V4 (Phase 4 exit / Pre-Rollout Quality Gate)** | Performance, Compliance, Security, Observability | 1 week | Exit: p95<200ms; 500-concurrent k6 pass; TEST-013–TEST-017 green; OTel traces captured end-to-end; zero critical pen-test findings
**V5 (Phase 5 exit / Post-GA)** | Rollout Safety & KPI Validation | ongoing through W13 | Exit: SC-001–SC-010 measured; 99.9% uptime at 7d; rollback chain tested in staging; all flags removed per schedule

## Test Categories

| Category | Scope | Tools | Owner | Phase |
|---|---|---|---|---|
| Unit | AuthService methods, TokenManager, PasswordHasher, JwtService, LockoutPolicy, validation logic | Jest, ts-jest | auth-team | 2 |
| Integration | AuthService+Postgres, TokenManager+Redis, ConsentRecorder+DB, ResetTokenStore lifecycle, admin audit query | Supertest, testcontainers | auth-team | 2 |
| E2E | Register→Login→Profile, password reset, silent refresh, logout, admin log viewer | Playwright | QA | 3 |
| Acceptance (persona) | Alex signup<60s, Jordan admin audit query, Sam programmatic token refresh | Playwright + k6 API harness | QA+product | 3–4 |
| Performance/Load | Login p95, refresh p95, 500 concurrent, hash benchmark | k6, APM | DevOps/QA | 4 |
| Resilience | Dep-loss simulation (pg/redis/sendgrid), failover, health degradation | Chaos scripts, testcontainers | DevOps | 4 |
| Security | XSS, CSRF, JWT tampering, brute-force, SQLi, raw-password sink scan | OWASP ZAP, manual pen test | security | 4 |
| Compliance | GDPR consent auditability, SOC2 12-month retention, NIST SP 800-63B storage, data minimization | Evidence review + integration tests | compliance | 4 |
| Rollout/Canary | Flag toggling, %-traffic routing, rollback runbook execution | Staging drills | DevOps/auth | 5 |
| KPI Validation | SC-001–SC-010 metric emission and target achievement | Prometheus/Grafana, funnel analytics | product/DevOps | 5 |

## Interleaving Strategy & Ratio Justification

**Ratio: 1:2 (one validation milestone per two work milestones, MEDIUM complexity baseline).** This roadmap actually runs **5:5 (1:1 continuous-parallel)** because each phase carries a dedicated validation exit. The 1:2 baseline is satisfied by V1+V2 gating the two backend work phases (P1 work → P2 work), V3 gating the frontend phase, and V4+V5 gating operations+rollout. Tests land **inline with implementation**, not after: unit+integration tests ship in Phase 2 alongside the endpoint they cover; E2E journeys ship in Phase 3 alongside the UI they drive; compliance/load/security tests ship in Phase 4 alongside the observability they instrument. The formal Pre-Rollout Quality Gate (end of Phase 4) is the aggregate sign-off before MIG-001.

**Justification for MEDIUM ratio (not HIGH 1:1):** complexity_score=0.65, single-service scope, standard REST patterns, no novel algorithms. The security criticality is elevated by continuous-parallel placement of security tests in every phase rather than collapsing to 1:1 cadence.

## Risk-Based Test Prioritization

| Priority | Risk | Tests (first to run, last to skip) |
|---|---|---|
| P0 | R-003 Migration data loss (CRITICAL) | TEST-004, rollback drills MIG-006–MIG-011 in staging, pre-cutover dual-read verification |
| P0 | R-001 Token theft via XSS | TEST-017 (pen), NFR-SEC-002 config test, httpOnly/Secure/SameSite cookie integration test |
| P0 | R-005 Audit/compliance gap | TEST-013, TEST-014, TEST-015, NFR-COMP-003 log-sink scan |
| P0 | NFR-SEC-001/002 crypto baseline | TEST-007 hash-time benchmark, RS256 config validation |
| P1 | R-002 Brute-force | TEST-002, lockout integration (5/15min), API-001 rate-limit test, CAPTCHA-on-3rd-failure (per mitigation) |
| P1 | R-004 Low conversion UX | TEST-006 persona flow, funnel tracking on RegisterPage, inline-validation unit tests (COMP-019) |
| P1 | R-006 SendGrid failure | TEST-009 reset flow with circuit-breaker sim, health endpoint degraded-state assertion (COMP-016) |
| P2 | Session-concurrency OQ-005 | Session duration SC-008, multi-device refresh-token test |

## Acceptance Criteria Per Milestone

**V1 — Infrastructure & Schema**
- All 6 schemas deployed; pg_partman ready for audit partitioning
- RS256 2048-bit key pair mounted; JwtService sign/verify round-trip passes
- bcrypt cost=12 benchmark <500ms on target pod spec
- Docker Compose dev stack starts <30s; testcontainers boot in CI
- OQ-003 (retention) and OQ-009 (consent design) closed before exit

**V2 — Backend Flows & API**
- TEST-001 through TEST-005, TEST-007, TEST-008 green in CI
- 8 endpoints return spec-compliant bodies; error envelope uniform per contract
- Every auth event emits to AuditLogger with {userId,eventType,timestamp,ipAddress,outcome}
- ConsentRecorder writes policyVersion on every register (GDPR Art 7)
- Coverage: ≥80% unit, ≥15% integration

**V3 — Frontend Journeys**
- TEST-006, TEST-009–TEST-012 green in Playwright
- AuthProvider silent-refresh dedup: single in-flight refresh across ≥3 concurrent 401s
- Route guards: unauth→/login, auth→/dashboard, non-admin→/admin/*→403
- Inline validation blocks weak password, missing consent, invalid email client-side
- Persona acceptance (PRD S7): Alex completes signup→login→profile <60s; Jordan queries audit log with 3 filter dimensions; Sam refresh cycle stable across 7-day token life

**V4 — Performance, Compliance, Security (Pre-Rollout Gate)**
- NFR-PERF-001 p95<200ms across all 8 endpoints; NFR-PERF-002 500 concurrent, 0 5xx, pool stable
- TEST-013/014/015 pass; compliance reviewer sign-off
- TEST-017 zero critical, ≤2 high (triaged); XSS/CSRF/JWT-tamper/SQLi clean
- OPS-010 metrics live, OPS-011 dashboards rendering, OPS-012 traces span AuthService→PasswordHasher→TokenManager→JwtService
- OPS-007/008/009 alerts tested via synthetic trigger, page reaches on-call
- OPS-001/002 runbooks reviewed and signed by on-call

**V5 — Rollout & KPI**
- MIG-001 alpha: zero P0/P1 in 1 week
- MIG-002 beta: p95<200ms, error<0.1%, zero Redis conn failures over 2 weeks at 10%
- MIG-003 GA: 99.9% uptime over first 7 days; AUTH_NEW_LOGIN flag removed
- SC-001–SC-010 measured and reported; SC-006>60% conversion, SC-010>80% reset completion, SC-009<5% failed login rate

## Quality Gates

| Gate | From → To | Blocking Criteria | Severity Policy |
|---|---|---|---|
| G1 | P1 → P2 | Schema contract tests, key mount, dep health all green; OQ-003/OQ-009 resolved | MAJOR blocks; MINOR tracked |
| G2 | P2 → P3 | TEST-001–005,007,008 green; audit emission verified on all events; 80/15 coverage floor | MAJOR blocks; CRITICAL stop-and-fix |
| G3 | P3 → P4 | All E2E + persona tests green; silent refresh dedup proven; guards enforced | MAJOR blocks |
| G4 | P4 → P5 (Pre-Rollout Quality Gate) | Perf SLO, pen-test zero-critical, compliance sign-off, observability emitting, runbooks reviewed; signed by auth-lead + platform-lead + security + compliance + product | ANY CRITICAL/MAJOR = stop-and-fix; no conditional pass |
| G5 | Beta → GA | MIG-002 14-day window: p95<200ms, err<0.1%, zero Redis failures; rollback drill executed in staging | Rollback triggers (p95>1000ms/5min, err>5%/2min, Redis>10fail/min) = immediate stop-and-fix |

**Issue handling:** CRITICAL = block current phase, fix before any further work; MAJOR = block next phase gate; MINOR = ticket for next sprint, no gate impact; COSMETIC = backlog. All rollback-trigger events are CRITICAL by definition.

## PRD-Derived Additions

**Persona acceptance tests (PRD S7):**
- Alex: full signup→login→profile journey <60s end-to-end (TEST-006 extended with timing assertion)
- Jordan: admin audit log query by userId+dateRange+eventType returns paginated results <1s (TEST-012 extended)
- Sam: programmatic token refresh across 7-day refresh TTL, no interactive prompts, stable error codes (API-harness test under k6)

**Customer journey E2E coverage (PRD S22):**
- First-Time Signup → TEST-006 + consent checkbox assertion
- Returning User Login → TEST-010 silent refresh + 7-day expiry prompt
- Password Reset → TEST-009 incl. 1hr TTL, single-use, all-sessions-invalidated
- Profile Management → TEST-006 profile render <1s

**KPI validation tests (PRD S19 → SC-001–SC-010):** each success criterion mapped 1:1 to a Prometheus/Grafana panel wired in OPS-011; funnel analytics instrumented on RegisterPage (SC-006), reset flow (SC-010), login endpoint (SC-001, SC-009).

**Compliance test category (PRD S17):**
- GDPR Art 7 consent: TEST-013 verifies policyVersion binding, timestamp, sourceIp
- SOC2 12-month retention: TEST-014 verifies partition lifecycle and tiered-storage policy (resolves OQ-003 in PRD's favor)
- NIST SP 800-63B: TEST-015 grep/scan across app+audit+trace sinks for raw password; error message sanitization
- GDPR data minimization: NFR-COMP-004 schema audit of UserProfile fields (roles[], timestamps)

**Edge case coverage (PRD S23):** negative tests added to V2/V3 —
- Duplicate email → 409 with login/reset hint
- Lockout at 5 fails/15min → 423 + admin notification
- Reset for unregistered email → generic success, no email sent, no enumeration
- Expired reset link → clear error + new-link CTA
- Multi-device concurrent login → both sessions valid, refresh versions independent
- Token-expired-during-edit → silent refresh attempt, local preserve on failure
- Password policy failure → inline block, form un-submittable
