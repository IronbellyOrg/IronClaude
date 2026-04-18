---
complexity_class: MEDIUM
validation_philosophy: continuous-parallel
validation_milestones: 3
work_milestones: 5
interleave_ratio: "1:2"
major_issue_policy: stop-and-fix
spec_source: test-tdd-user-auth.md
generated: "2026-04-16T00:24:42.329851+00:00"
generator: superclaude-roadmap-executor
---

# Test Strategy — User Authentication Service

## 1. Validation Milestones Mapped to Roadmap Phases

| Validation Milestone | After Phase(s) | Gate Name | Focus |
|---|---|---|---|
| V1 | Phase 1 + Phase 2 | **Contract & Flow Gate** | Schema compliance, crypto configs, all 5 auth flows correct, API contracts honored, audit persistence |
| V2 | Phase 3 | **Performance & SLO Gate** | p95 latency targets, concurrency capacity, uptime monitoring, bcrypt benchmark |
| V3 | Phase 4 | **Release Readiness Gate** | E2E journeys, penetration test, unit coverage >=80%, persona acceptance, zero P0/P1 |

Phase 5 (Rollout) is validated by operational telemetry during staged rollout (alpha/beta/GA), not by a discrete test gate. Rollback triggers (MIG-007) serve as continuous validation during deployment.

**Interleave rationale (1:2):** MEDIUM complexity with 4 compliance obligations (GDPR x2, SOC2, NIST), RS256 key management, and cross-layer FE/BE integration justifies validation every two work phases. This catches schema/contract issues before frontend work begins (V1), confirms performance before exposing UI to users (V2), and blocks rollout on security findings (V3).

## 2. Test Categories

### 2.1 Unit Tests

| ID | Target | Validates | Technique | Phase |
|---|---|---|---|---|
| UT-001 | AuthService.login() | FR-AUTH-001 | Mock PasswordHasher, TokenManager, UserRepo | 2 |
| UT-002 | AuthService.login() — invalid creds | FR-AUTH-001 AC3 | PasswordHasher returns false; assert 401, no token | 2 |
| UT-003 | AuthService.register() | FR-AUTH-002 | Assert bcrypt cost-12 hash, consent_ts stored, displayName validated | 2 |
| UT-004 | AuthService.register() — duplicate email | FR-AUTH-002 AC2 | UserRepo throws conflict; assert 409 | 2 |
| UT-005 | AuthService.register() — weak password | FR-AUTH-002 AC3 | <8 chars / no upper / no digit → 400 | 2 |
| UT-006 | TokenManager.issueTokens() | FR-AUTH-003 | Assert access 15min TTL, refresh 7d TTL, RS256 signed | 2 |
| UT-007 | TokenManager.refresh() — valid | FR-AUTH-003 AC2 | Old token revoked, new pair issued | 2 |
| UT-008 | TokenManager.refresh() — revoked | FR-AUTH-003 AC4 | Assert 401 for revoked refresh token | 2 |
| UT-009 | TokenManager.revoke() | Logout (OQ-006) | Assert Redis DEL on refresh token hash | 2 |
| UT-010 | JwtService.sign() / verify() | NFR-SEC-002 | RS256 2048-bit; tampered token rejected; 5s clock skew | 1 |
| UT-011 | PasswordHasher.hash() / verify() | NFR-SEC-001, NFR-COMP-003 | Cost-12 digest; verify round-trips; no plaintext in logs | 1 |
| UT-012 | PasswordHasher.hash() timing | SC-005 | hash() completes <500ms (bcrypt cost-12 benchmark) | 1 |
| UT-013 | UserRepo.findByEmail() | COMP-005 | Lowercase normalization; returns null for missing | 1 |
| UT-014 | UserRepo.createUser() | COMP-005 | UUID PK generated; default roles=["user"]; timestamps set | 1 |
| UT-015 | Rate limit middleware | API-001/002 | 10/min login, 5/min register → 429 | 2 |
| UT-016 | Error response formatter | All API-xxx | {code, message, status} structure on all error paths | 2 |
| UT-017 | Password reset token generation | FR-AUTH-005 | 1h TTL; single-use; cryptographically random | 2 |
| UT-018 | Account lockout | FR-AUTH-001 AC4 | 5 failures in 15min → 423; resets after window | 2 |
| UT-019 | GDPR consent validation | NFR-COMP-001 | Registration without consent → 400; consent_ts persisted | 2 |
| UT-020 | Data minimization check | NFR-COMP-004 | Assert UserProfile schema has only allowed PII fields | 1 |

**Coverage target:** >=80% on AuthService, TokenManager, PasswordHasher, JwtService, UserRepo.

### 2.2 Integration Tests

| ID | Target | Validates | Infrastructure | Phase |
|---|---|---|---|---|
| IT-001 | Registration → PostgreSQL persist | FR-AUTH-002, TEST-004 | testcontainers (PG) | 2 |
| IT-002 | Login → token issuance → Redis store | FR-AUTH-001 + FR-AUTH-003 | testcontainers (PG + Redis) | 2 |
| IT-003 | Refresh token expiry → 401 | FR-AUTH-003, TEST-005 | testcontainers (Redis with TTL manipulation) | 2 |
| IT-004 | Audit event persistence | NFR-COMP-002 | testcontainers (PG); assert all 5 event types logged | 2 |
| IT-005 | Audit log 12-month partition | DM-003, OQ-008 | testcontainers (PG); verify monthly partitioning works | 2 |
| IT-006 | Password reset email dispatch | FR-AUTH-005, DEP-006 | SendGrid sandbox mode; assert email sent with valid token | 2 |
| IT-007 | Password reset confirm → hash update | FR-AUTH-005 | testcontainers (PG); old hash replaced; token consumed | 2 |
| IT-008 | API Gateway → endpoint routing | INFRA-001 | TLS 1.3 enforcement; CORS restricted; /v1/auth/* routes | 1 |
| IT-009 | Connection pool under load | COMP-005 | pg-pool at 100 connections; conn wait <50ms | 3 |
| IT-010 | Feature flag gating | MIG-004/005 | AUTH_NEW_LOGIN OFF → legacy; ON → new service | 4 |
| IT-011 | Brute-force lockout + audit trail | FR-AUTH-001 AC4 + NFR-COMP-002 | 5 failed logins → lockout + audit events recorded | 2 |
| IT-012 | Token rotation atomicity | FR-AUTH-003 | Refresh issues new pair AND revokes old in single transaction | 2 |

### 2.3 End-to-End Tests (Playwright)

| ID | Journey | Validates | Persona | Phase |
|---|---|---|---|---|
| E2E-001 | Register → Login → Profile | TEST-006, FR-AUTH-001/002/004 | Alex | 4 |
| E2E-002 | Register → Logout → Login | OQ-006, COMP-010 | Alex | 4 |
| E2E-003 | Login → Navigate → Silent refresh → Profile | FR-AUTH-003, COMP-009 | Alex | 4 |
| E2E-004 | Password reset: request → email → confirm → login | FR-AUTH-005, SC-010 | Alex | 4 |
| E2E-005 | Register with weak password → inline validation | FR-AUTH-002 AC3, COMP-007 | Alex | 4 |
| E2E-006 | Register with duplicate email → helpful error | FR-AUTH-002 AC2 | Alex | 4 |
| E2E-007 | 5 failed logins → lockout message | FR-AUTH-001 AC4 | Alex | 4 |
| E2E-008 | Expired refresh token → redirect to login | COMP-009, 7d expiry | Alex | 4 |
| E2E-009 | Registration <60s end-to-end | SC-006, Alex persona target | Alex | 4 |
| E2E-010 | Profile page renders <1s | COMP-008 AC | Alex | 4 |
| E2E-011 | API token refresh (programmatic) | FR-AUTH-003, Sam persona | Sam | 4 |
| E2E-012 | API error codes (401/409/429) clarity | Sam persona | Sam | 4 |

### 2.4 Performance Tests

| ID | Target | Metric | Tool | Phase |
|---|---|---|---|---|
| PERF-001 | POST /auth/login p95 | <200ms (SC-001) | k6 | 3 |
| PERF-002 | POST /auth/register p95 | <200ms | k6 | 3 |
| PERF-003 | POST /auth/refresh p95 | <100ms (SC-003) | k6 | 3 |
| PERF-004 | 500 concurrent logins | No 5xx, p95 <200ms (NFR-PERF-002) | k6 | 3 |
| PERF-005 | bcrypt cost-12 benchmark | <500ms (SC-005) | CI benchmark | 2 |
| PERF-006 | Connection pool stability | pool stable at 500 concurrent | k6 + PG metrics | 3 |
| PERF-007 | Redis latency under load | stable p99 <10ms at 500 concurrent | k6 + Redis metrics | 3 |

### 2.5 Security Tests

| ID | Target | Validates | Technique | Phase |
|---|---|---|---|---|
| SEC-001 | XSS token theft prevention | R-001 | Verify accessToken NOT in localStorage; CSP headers present | 4 |
| SEC-002 | User enumeration prevention | FR-AUTH-001 AC3, FR-AUTH-005 AC | Same response for valid/invalid emails on login and reset | 4 |
| SEC-003 | SQL injection on login/register | OWASP A03 | Parameterized queries; fuzz email/password inputs | 4 |
| SEC-004 | JWT tampering rejection | NFR-SEC-002 | Modify payload → verify() rejects | 1 |
| SEC-005 | No plaintext passwords in logs/DB | NFR-COMP-003, NIST | grep logs + DB for raw password strings; assert none | 2 |
| SEC-006 | TLS 1.3 enforcement | INFRA-001 | TLS downgrade attempt → rejected | 1 |
| SEC-007 | CORS restriction | INFRA-001 | Request from unknown origin → blocked | 1 |
| SEC-008 | Penetration test (full) | R-005 | OWASP Top 10 against all 6 endpoints; zero critical findings | 4 |
| SEC-009 | Reset token entropy | FR-AUTH-005 | Assert cryptographic randomness; not guessable | 2 |
| SEC-010 | HttpOnly cookie for refresh token | R-001 | Browser dev tools confirm flag; JS cannot read | 4 |

### 2.6 Compliance Tests

| ID | Requirement | Standard | Validation | Phase |
|---|---|---|---|---|
| COMP-001 | Consent recorded at registration | GDPR (NFR-COMP-001) | Registration without consent checkbox → 400; consent_ts in DB | 2 |
| COMP-002 | Data minimization — only allowed fields | GDPR (NFR-COMP-004) | Schema inspection: only email, password_hash, display_name as PII | 1 |
| COMP-003 | Audit log captures all 5 event types | SOC2 (NFR-COMP-002) | Trigger each event; assert AuditLog rows with correct fields | 2 |
| COMP-004 | Audit log 12-month retention | SOC2 (NFR-COMP-002) | Verify partition-by-month DDL; retention policy set; old data queryable | 2 |
| COMP-005 | No raw password persisted or logged | NIST (NFR-COMP-003) | Full-text search across DB and log output for test passwords | 2 |
| COMP-006 | bcrypt adaptive hashing with cost 12 | NIST (NFR-COMP-003) | Hash prefix $2b$12$; timing benchmark <500ms | 1 |
| COMP-007 | Consent proof queryable | GDPR | Query consent_ts by user; non-null for all registered users | 2 |

### 2.7 Acceptance Tests (Persona-Based)

| ID | Persona | Scenario | Success Criteria | Phase |
|---|---|---|---|---|
| ACC-001 | Alex (End User) | First-time registration to personalized dashboard | Complete flow <60s; inline validation; immediate session; profile accessible | 4 |
| ACC-002 | Alex (End User) | Return login with silent session persistence | Login <200ms; navigate 5+ pages without re-login; refresh is invisible | 4 |
| ACC-003 | Alex (End User) | Self-service password recovery | Reset email <60s; new password works; old sessions invalidated; >80% completion (SC-010) | 4 |
| ACC-004 | Jordan (Admin) | View failed login audit trail | Query audit logs by user+date; see userId, eventType, timestamp, IP, outcome; admin-only access | 4 |
| ACC-005 | Jordan (Admin) | Account lockout investigation | 5-failure lockout visible in audit; IP recorded; timestamp within 15min window | 4 |
| ACC-006 | Sam (API Consumer) | Programmatic token lifecycle | POST /auth/login → token pair; POST /auth/refresh → new pair; expired → clear 401 JSON error | 4 |
| ACC-007 | Sam (API Consumer) | Error code contract stability | All error responses match {code, message, status}; documented codes match implementation | 4 |

### 2.8 KPI Validation Tests

| KPI | Target | Proxy Test | Measurement Method | Phase |
|---|---|---|---|---|
| SC-001 | Login p95 <200ms | PERF-001 | k6 load test + APM tracing | 3 |
| SC-002 | Registration success >99% | IT-001 + PERF-002 | success/attempts ratio under load | 3 |
| SC-003 | Refresh p95 <100ms | PERF-003 | k6 + APM on TokenManager.refresh() | 3 |
| SC-004 | 99.9% uptime | NFR-REL-001 | Health check monitoring over 7d post-GA | 5 |
| SC-005 | Hash time <500ms | PERF-005 | CI benchmark on PasswordHasher.hash() | 2 |
| SC-006 | Registration conversion >60% | E2E-009 + funnel analytics | landing→register→confirmed funnel | 4-5 |
| SC-007 | >1000 DAU in 30d | Rollout telemetry | Token issuance analytics post-GA | 5 |
| SC-008 | Session duration >30min | E2E-003 (proxy) | Refresh event analytics post-GA | 5 |
| SC-009 | Failed login rate <5% | IT-011 (proxy) | Audit log analysis post-GA | 5 |
| SC-010 | Reset completion >80% | E2E-004 (proxy) | Reset funnel analytics | 4-5 |

### 2.9 Customer Journey E2E Tests (from PRD S22)

| ID | Journey | Steps | Critical Assertions |
|---|---|---|---|
| CJ-001 | First-Time Signup | Land → Sign Up CTA → fill form → submit → dashboard redirect | Redirect <2s; session active; profile populated |
| CJ-002 | Returning User Login | Visit → Log In → credentials → dashboard; navigate pages; return after 7d+ | Silent refresh works; 7d expiry prompts re-login with clear message |
| CJ-003 | Password Reset | Forgot Password → email → confirmation → open email (<60s) → click link → new password → login redirect | Same UX for registered/unregistered; 1h TTL enforced; old sessions killed |
| CJ-004 | Profile Management | Navigate to profile → view data | Renders <1s; data matches registration input |

### 2.10 Edge Case Tests (from PRD S23)

| ID | Scenario | Expected Behavior | Category |
|---|---|---|---|
| EDGE-001 | Duplicate email at registration | 409 with helpful message suggesting login/reset | Unit + E2E |
| EDGE-002 | Wrong password <5 attempts | Generic "Invalid email or password"; no enumeration | Unit + E2E |
| EDGE-003 | Wrong password >=5 attempts | 423 lockout; admin notified; user told to wait or reset | Integration |
| EDGE-004 | Reset for unregistered email | Same success response; no email sent | Unit + E2E |
| EDGE-005 | Expired reset link | Clear error with retry option | E2E |
| EDGE-006 | Concurrent multi-device login | Both sessions valid simultaneously | Integration |
| EDGE-007 | Token expires during editing | Silent refresh if possible; else preserve work + prompt | E2E |
| EDGE-008 | Password fails policy inline | Unmet requirements shown; form blocked | E2E |
| EDGE-009 | Reuse of consumed reset token | Rejected with error; cannot reset again | Unit + Integration |

## 3. Test-Implementation Interleaving Strategy

```
Phase 1 (2.5w)  Phase 2 (2w)     V1 Gate    Phase 3 (1.5w)  V2 Gate    Phase 4 (3w)      V3 Gate    Phase 5 (4w)
┌──────────┐    ┌──────────┐    ┌──────┐    ┌──────────┐   ┌──────┐   ┌──────────────┐   ┌──────┐   ┌──────────┐
│ Infra +  │    │ Auth     │    │Schema│    │ Perf     │   │ SLO  │   │ FE + E2E +   │   │Release│   │ Rollout  │
│ Schema + │ →  │ Flows +  │ →  │+Flow │ →  │ Load +   │ → │ Perf │ → │ Security +   │ → │Readi- │ → │ Alpha →  │
│ Crypto   │    │ API +    │    │Valid.│    │ Monitor  │   │ Gate │   │ Penetration  │   │ness  │   │ Beta →   │
│ Modules  │    │ Audit    │    │      │    │          │   │      │   │              │   │ Gate │   │ GA       │
└──────────┘    └──────────┘    └──────┘    └──────────┘   └──────┘   └──────────────┘   └──────┘   └──────────┘
     │                │                           │                          │
  UT-010/011/012   UT-001→020                  PERF-001→007              E2E-001→012
  SEC-004/006/007  IT-001→012                                           SEC-001→010
  COMP-002/006     COMP-001→007                                         ACC-001→007
                                                                        CJ-001→004
```

**Co-located testing (parallel with implementation):**
- Phase 1: Crypto unit tests (UT-010, UT-011, UT-012), TLS/CORS checks (SEC-006, SEC-007), schema compliance checks (COMP-002, COMP-006)
- Phase 2: All auth flow unit tests (UT-001→UT-020), all integration tests (IT-001→IT-012), compliance tests (COMP-001→007), bcrypt benchmark (PERF-005)
- Phase 4: Frontend E2E (E2E-001→012), security suite (SEC-001→010), acceptance tests (ACC-001→007), customer journey tests (CJ-001→004), edge cases (EDGE-001→009)

**Dedicated validation windows:**
- V1 (0.5 day): Run full unit + integration suite; verify schema freeze; confirm all 6 API contracts return correct codes
- V2 (0.5 day): Run performance suite under load; verify SLO thresholds; confirm monitoring dashboards
- V3 (1 week — budgeted in Phase 4): Dedicated E2E window, penetration testing, persona acceptance, coverage audit

## 4. Risk-Based Test Prioritization

| Priority | Risk | Tests | Rationale |
|---|---|---|---|
| **P0** | R-005: Security breach | SEC-001→010, COMP-005/006 | CRITICAL severity; single breach invalidates entire service |
| **P0** | R-001: Token theft via XSS | SEC-001, SEC-010, E2E-003 | HIGH severity; affects all authenticated users |
| **P0** | R-006: Incomplete audit logging | COMP-003/004/007, IT-004/005 | HIGH severity; SOC2 Q3 deadline is hard |
| **P1** | R-002: Brute-force abuse | UT-018, IT-011, EDGE-003 | MEDIUM severity but HIGH likelihood |
| **P1** | R-004: Low registration adoption | ACC-001, E2E-009, CJ-001 | HIGH severity; gates revenue ($2.4M) |
| **P1** | R-003: Data loss during migration | IT-010, rollback rehearsal | HIGH severity but LOW likelihood |
| **P2** | R-007: Email delivery failures | IT-006, E2E-004 | MEDIUM severity, LOW likelihood |

**Test execution order within each phase follows this priority.** P0 tests must pass before P1 tests begin.

## 5. Acceptance Criteria per Milestone

### V1 — Contract & Flow Gate (after Phase 2)

| Criterion | Measurement | Pass Threshold |
|---|---|---|
| Schema compliance | DM-001/002/003 match extraction spec | 100% field match |
| Crypto baseline | UT-010, UT-011, UT-012 | All green; hash <500ms |
| Auth flow correctness | UT-001→UT-009 | All green |
| API contract compliance | UT-015, UT-016 + manual HTTP | All 6 endpoints return correct status codes per AC |
| Integration flows | IT-001→IT-012 | All green with testcontainers |
| Audit persistence | COMP-003, IT-004 | All 5 event types persisted with required fields |
| Compliance baseline | COMP-001→007 | All green |
| Rate limiting | UT-015 | 429 returned at threshold for all rate-limited endpoints |
| No plaintext passwords | SEC-005 | Zero matches in DB + logs |

### V2 — Performance & SLO Gate (after Phase 3)

| Criterion | Measurement | Pass Threshold |
|---|---|---|
| Login p95 | PERF-001 (k6) | <200ms (SC-001) |
| Register p95 | PERF-002 (k6) | <200ms |
| Refresh p95 | PERF-003 (k6) | <100ms (SC-003) |
| Concurrency | PERF-004 (k6) | 500 concurrent, zero 5xx |
| Pool stability | PERF-006 | No connection exhaustion at 500 concurrent |
| Redis stability | PERF-007 | p99 <10ms at load |
| Uptime monitoring | NFR-REL-001 | Grafana dashboard live; alerts routing |
| Registration success rate | PERF-002 | >99% under load (SC-002) |

### V3 — Release Readiness Gate (after Phase 4)

| Criterion | Measurement | Pass Threshold |
|---|---|---|
| E2E journey | E2E-001 (Playwright) | Register→Login→Profile green |
| Penetration test | SEC-008 | Zero critical findings |
| Unit coverage | Jest --coverage | >=80% on 5 core components |
| Persona acceptance — Alex | ACC-001, ACC-002, ACC-003 | All pass; registration <60s |
| Persona acceptance — Jordan | ACC-004, ACC-005 | Audit queryable by user+date |
| Persona acceptance — Sam | ACC-006, ACC-007 | Token lifecycle + error contract stable |
| Bug count | Defect tracker | Zero P0/P1 open |
| Customer journeys | CJ-001→004 | All critical paths complete |
| Edge cases | EDGE-001→009 | All handled per spec |
| Registration conversion proxy | E2E-009 timing | <60s end-to-end |
| Reset completion proxy | E2E-004 | Full flow completes without error |

## 6. Quality Gates Between Phases

### Gate G1: Phase 1 → Phase 2

| Check | Blocking? | Evidence |
|---|---|---|
| PostgreSQL 15+ reachable, schemas migrated | Yes | DDL applied; DM-001/002/003 tables exist |
| Redis 7+ reachable, TTL working | Yes | SET/GET with TTL verified |
| bcrypt cost-12 hash <500ms | Yes | UT-012 green |
| RS256 sign/verify round-trip | Yes | UT-010 green |
| OQ-004 (token limit) resolved | Yes | Decision documented |
| OQ-008 (12mo retention) resolved | Yes | Resolved per roadmap |
| API Gateway routes /v1/auth/* with TLS 1.3 | Yes | IT-008 green |
| AuthService + TokenManager skeletons compile | Yes | Build green |

### Gate G2: Phase 2 → Phase 3

| Check | Blocking? | Evidence |
|---|---|---|
| **V1 Gate passes** | Yes | All V1 acceptance criteria met |
| All 5 auth flows unit tested | Yes | UT-001→009, UT-017→019 green |
| All 6 endpoints returning correct codes | Yes | IT suite + manual verification |
| SOC2 audit events persisting | Yes | COMP-003 green |
| Rate limiting enforced | Yes | UT-015 green |
| Error format standardized | Yes | UT-016 green |

### Gate G3: Phase 3 → Phase 4

| Check | Blocking? | Evidence |
|---|---|---|
| **V2 Gate passes** | Yes | All V2 acceptance criteria met |
| p95 login <200ms | Yes | PERF-001 report |
| 500 concurrent sustained | Yes | PERF-004 report |
| Monitoring dashboards live | Yes | Grafana screenshot / URL |
| Logout design documented (COMP-010) | Yes | Design doc exists |
| Audit viewer design documented (COMP-011) | Yes | Design doc exists |

### Gate G4: Phase 4 → Phase 5

| Check | Blocking? | Evidence |
|---|---|---|
| **V3 Gate passes** | Yes | All V3 acceptance criteria met |
| Penetration test: zero critical | Yes | Pentest report |
| Unit coverage >=80% | Yes | Jest coverage report |
| E2E Playwright journey green | Yes | TEST-006 / E2E-001 green |
| Zero P0/P1 bugs | Yes | Defect tracker query |
| Runbooks drafted (OPS-001, OPS-002) | Yes | Docs exist |
| Feature flags configured (MIG-004, MIG-005) | Yes | Flag service verified |

### Gate G5: Alpha → Beta (within Phase 5)

| Check | Blocking? | Evidence |
|---|---|---|
| 1 week alpha with zero P0/P1 | Yes | Defect tracker + staging telemetry |
| All FRs pass manual testing | Yes | QA sign-off |
| Rollback procedure tested | Yes | MIG-006 rehearsal log |
| Rollback triggers configured | Yes | MIG-007 alerts firing on threshold breach |

### Gate G6: Beta → GA (within Phase 5)

| Check | Blocking? | Evidence |
|---|---|---|
| 2 weeks at 10% traffic | Yes | Traffic routing confirmed |
| p95 <200ms under real load | Yes | APM dashboard |
| Error rate <0.1% | Yes | Monitoring data |
| Zero Redis connection failures | Yes | Redis metrics |
| AuthProvider refresh validated under load | Yes | E2E-003 equivalent on staging |

## Issue Classification

| Severity | Action | Gate Impact | Examples |
|---|---|---|---|
| CRITICAL | Stop-and-fix immediately | Blocks current phase | Plaintext password in logs; SQL injection; token forgery possible |
| MAJOR | Stop-and-fix before next phase | Blocks next phase | p95 >200ms; audit events not persisting; rate limiting bypassed |
| MINOR | Track and fix in next sprint | No gate impact | Error message wording; non-critical UI alignment; minor log formatting |
| COSMETIC | Backlog | No gate impact | Code style; documentation typos; non-user-facing naming |

## Test Infrastructure Requirements

| Component | Purpose | Used By |
|---|---|---|
| testcontainers (PostgreSQL) | Ephemeral DB for integration tests | IT-001→005, IT-009, IT-011 |
| testcontainers (Redis) | Ephemeral cache for token tests | IT-002, IT-003, IT-012 |
| Jest + ts-jest | Unit test runner + mocking | All UT-xxx |
| Playwright | Browser automation for E2E | All E2E-xxx, CJ-xxx |
| k6 | Load testing | All PERF-xxx |
| SendGrid sandbox | Email integration testing | IT-006 |
| Docker Compose | Local dev environment | Developer testing |
| CI pipeline | Automated test execution | All tests on every PR |

## Test Pyramid Summary

| Level | Count | Coverage Target | Tools |
|---|---|---|---|
| Unit | 20 | 80% on core components | Jest |
| Integration | 12 | 15% | Supertest + testcontainers |
| Performance | 7 | SLO validation | k6 |
| Security | 10 | OWASP Top 10 + compliance | Penetration tools + manual |
| Compliance | 7 | 4 regulatory obligations | Automated + audit review |
| E2E | 12 | Critical user journeys | Playwright |
| Acceptance | 7 | 3 personas covered | Manual + automated |
| Edge Cases | 9 | PRD S23 coverage | Mixed |
| Customer Journeys | 4 | PRD S22 coverage | Playwright |
| **Total** | **88** | | |
