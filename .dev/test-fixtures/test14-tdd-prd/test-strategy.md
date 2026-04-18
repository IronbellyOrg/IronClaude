---
complexity_class: HIGH
validation_philosophy: continuous-parallel
validation_milestones: 5
work_milestones: 5
interleave_ratio: 1:1
major_issue_policy: stop-and-fix
spec_source: test-tdd-user-auth.md
generated: "2026-04-17T15:41:14.999215+00:00"
generator: superclaude-roadmap-executor
---

# Test Strategy — User Authentication Service

## 1. Validation Milestones (1:1 mapped to work milestones)

**V1: Contract & Infrastructure Validation** | paired with M1 | duration 2w (parallel) | exit: all schemas/DI wiring verified; TLS1.3 A+; secret-scrub tests green
**V2: API & Compliance Validation** | paired with M2 | duration 2w (parallel) | exit: 10 endpoints meet contracts; SOC2 audit coverage 20/20; pen-test booking confirmed
**V3: Client Integration & QA Gate Validation** | paired with M3 | duration 2w (parallel) | exit: 80/15/5 coverage gate green; security + journey tests green; pre-merge NFR gates enforced
**V4: Rollout Safety & Success Criteria Validation** | paired with M4 | duration 3w (parallel) | exit: SC-001..012 measured green; pen-test Critical/High=0; divergence <0.1%
**V5: Operational Readiness Validation** | paired with M5 | duration 1w (parallel) | exit: runbooks rehearsed; rotation + retention jobs VA2; SOC2 dry-run pass

## 2. Test Categories

| Category | Tooling | Coverage Target | Scope |
|---|---|---|---|
| Unit | Jest, ts-jest | 80% | AuthService, PasswordHasher, JwtService, TokenManager, validators |
| Integration | Supertest, testcontainers | 15% | API→DB→Redis flows, audit write paths, email dispatch |
| E2E | Playwright (Chromium/Firefox/WebKit) | 5% | Login/Register/Profile/Reset/Admin journeys |
| Load | k6 (nightly + pre-release) | 500 concurrent | NFR-PERF-001/002 regression gate |
| Security | testssl.sh, timing-parity harness, OWASP ZAP, external pen-test | Critical/High=0 | TLS, XSS/CSP, enumeration, lockout, RSA/bcrypt config |
| Compliance | SOC2 evidence harness, GDPR consent checks | 100% flows audited | NFR-COMP-001/002/003, 12mo retention, NC0 |
| Acceptance (persona) | Playwright + manual usability | ≥1 per persona | Alex, Jordan, Sam JTBD |
| Contract | OpenAPI 3.1 linter + handler-spec parity CI | 100% endpoints | COMP-OPENAPI |

## 3. Interleaving Strategy

HIGH complexity (0.72) + auth security-criticality + phased rollout + SOC2 evidence requirement justify 1:1 interleave: every work milestone is shadowed by a validation milestone running in parallel on the same timeline. Rationale: (a) security primitives (bcrypt/RS256/TLS/CSP) must be validated at the moment they are wired, not after; (b) SOC2 audit evidence is milestone-cumulative and cannot be back-filled; (c) rollback triggers in M4 demand pre-validated baselines; (d) single-shot pen-test needs validated contracts by W4. Lower ratios (1:2 / 1:3) would defer discovery of enumeration leaks, RSA/bcrypt misconfig, and audit-event gaps past the point of cheap fix.

## 4. Risk-Based Prioritization

| Rank | Risk | Severity | Test Focus | Milestone |
|---|---|---|---|---|
| 1 | R-PRD-004 security breach | CRITICAL | Pen-test, TEST-SEC-*, CSP/HSTS, RS256/bcrypt gates | V1→V4 |
| 2 | R-003 migration data loss | HIGH | Divergence monitor tests, restore rehearsal, idempotent upsert tests | V4 |
| 3 | R-001 XSS token theft | HIGH | THP memory-only token tests, ESLint localStorage ban, CSP Report-Only | V3 |
| 4 | R-PRD-002 compliance audit gap | HIGH | NC0 20-scenario audit integration, 12mo retention, SOC2 dry-run | V2, V4 |
| 5 | R-002 brute force | MEDIUM | Lockout test, rate-limit, CAPTCHA | V2, V3 |
| 6 | R-PRD-001 RGS UX | HIGH | Usability testing 5 users, funnel analytics | V3 |
| 7 | R-PRD-003 email delivery | MEDIUM | SendGrid webhook + retry + SLA alert tests | V2, V4 |

## 5. Acceptance Criteria per Milestone

**M1/V1:** OQ-003/005/007/008 closed; DM-001/002/003 migrations reversible; TLS1.3 testssl.sh A+; CSP Report-Only deployed; DLP secret-scrub passes leak test; DI containers boot-validate crypto config fail-fast.
**M2/V2:** 10 `/v1/auth/*` endpoints pass contract tests (OpenAPI parity CI); FA0 constant-time (±10ms); 423 lockout after 5/15m; reset email <60s; NC0 logs 20/20 scenarios with required fields; pen-test vendor contract signed by end W4.
**M3/V3:** 80% unit / 15% integration / 5% E2E coverage enforced in CI; TEST-SEC-ENUMERATION/LOCKOUT green; TEST-IMPLICIT-BCRYPT/RS256 boot fail-fast; Playwright matrix green across 3 browsers; PRD-JOURNEY-FIRSTSIGNUP usability n≥5; a11y WCAG 2.1 AA pass.
**M4/V4:** SC-001..012 targets met with APM evidence; pen-test Critical/High=0 open; MIG-DUAL-RUN drift <0.1%; rollback tabletop executed; Alertmanager P1 routes verified; 99.9% uptime first 7d GA.
**M5/V5:** OPS-001..005 runbooks rehearsed; RSA rotation job + retention partition-drop job automated and dry-run; post-mortem template committed; SOC2 auditor preview pass.

## 6. Quality Gates

| Gate | Between | Blocks If |
|---|---|---|
| G1 Contract-freeze | M1→M2 | OQ-003/007/008 open; TLS A+ fail; DI boot-validate fail |
| G2 API-ready | M2→M3 | Any of 10 endpoints missing OpenAPI parity; NC0 20/20 not green; pen-test not booked |
| G3 Pre-merge (every PR in M3+) | PR→main | Coverage <80/15/5; bcrypt/RS256 config test fail; TEST-SEC-ENUMERATION/LOCKOUT regression |
| G4 Beta-exit (SC-011) | MIG-002→MIG-003 | p95≥200ms OR err≥0.1% OR Redis failures >0 over 2w OR divergence >0.1% |
| G5 GA | MIG-003→M5 | Pen-test Critical/High open; SC-001..012 red; rollback runbook not tabletop-exercised |
| G6 Ops-handover | M5→close | Retention job not automated; RSA rotation not automated; SOC2 dry-run fail |

## 7. Persona Acceptance Tests (PRD S7)

| Persona | Test | Milestone |
|---|---|---|
| Alex (end user) | PRD-JOURNEY-FIRSTSIGNUP: land→signup→dashboard ≤2s with inline validation + funnel analytics | V3 |
| Alex (returning) | PRD-JOURNEY-SESSIONPERSIST: silent refresh across pageloads; >7d idle prompts re-login | V3 |
| Jordan (admin) | COMP-011 AdminAuditPage E2E: filter by user+date; lock/unlock round-trip visible in audit | V3 |
| Sam (API consumer) | Programmatic login→refresh→me cycle via curl/Supertest; stable error envelope | V2 |

## 8. Customer Journey E2E Tests (PRD S22)

| Journey | E2E Coverage | Milestone |
|---|---|---|
| First-Time Signup | TEST-006 + PRD-JOURNEY-FIRSTSIGNUP | V3 |
| Returning User Login | PRD-JOURNEY-SESSIONPERSIST + silent-refresh interceptor test | V3 |
| Password Reset | COMP-FE-RESET-REQ + COMP-FE-RESET-CONF E2E, email delivery <60s assertion | V3, V4 |
| Profile Management | COMP-003 E2E reads full UserProfile; 401→refresh→re-fetch | V3 |

## 9. KPI Validation Tests (PRD S19)

| KPI | Target | Validation Test | Owner Milestone |
|---|---|---|---|
| Registration conversion | >60% | SC-006 funnel analytics landing→register→confirmed | V4 |
| Login p95 | <200ms | SC-001 APM + TEST-IMPLICIT-LOAD k6 nightly | V3, V4 |
| Avg session duration | >30m | SC-008 token-refresh analytics | V4 |
| Failed login rate | <5% | SC-009 audit event aggregation | V4 |
| Password reset completion | >80% | SC-010 reset funnel analytics | V4 |

## 10. Compliance Test Category (PRD S17)

| Control | Test | Milestone |
|---|---|---|
| GDPR consent | NFR-COMP-001 schema + API-002 rejection test when consent=false | V2 |
| GDPR data minimization | NFR-COMP-003 negative-field rejection test | V2 |
| SOC2 audit logging | TEST-IMPLICIT-AUDIT 20 scenarios + queryable-by-user+date + SOC2 dry-run export | V2, V4 |
| 12mo retention | Monthly-partition test + partition-drop dry-run + auditor preview | V1, V5 |
| NIST SP 800-63B | TEST-IMPLICIT-BCRYPT cost==12 + COMP-VALIDATOR password-strength unit tests | V3 |
| Raw-password never logged | COMP-DLP leak test with known secrets in log stream | V1 |

## 11. Edge Case Coverage (PRD S23)

| Scenario | Test Artifact | Severity Mapping |
|---|---|---|
| Duplicate email at registration | API-002 409 test + FE inline hint | MAJOR if missing |
| ≥5 failed logins | TEST-SEC-LOCKOUT + 423 assertion + audit row | CRITICAL if missing |
| Reset requested for unregistered email | TEST-SEC-ENUMERATION constant-time + identical body/headers | CRITICAL if leak |
| Expired reset link | COMP-RESETTOKEN TTL test + FE clear-error | MAJOR |
| Concurrent multi-device login | TEST-005 multi-session + OQ-005 cap enforcement test | MINOR→MAJOR if cap violated |
| Token expires during edit | THP single-flight silent-refresh race test | MAJOR |
| Password policy failure | COMP-VALIDATOR unit + FE inline validation | MAJOR |
