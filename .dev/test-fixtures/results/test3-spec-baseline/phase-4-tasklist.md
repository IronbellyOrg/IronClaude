# Phase 4 -- Hardening and Validation

**Goal**: Performance validation, security review, rollback verification, production readiness. Comprehensive coverage targets and dedicated security test suites.

**Tasks**: T04.01 -- T04.22
**Roadmap Items**: R-051 -- R-072
**Deliverables**: D-0051 -- D-0072

---

### T04.01 -- k6 load test: login endpoint

| Field | Value |
|---|---|
| Roadmap Item IDs | R-051 |
| Why | NFR-AUTH.1 and SC-2 require p95 < 200ms at normal load for the login endpoint. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | security, auth |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Critical Path Override | Yes |
| Verification Method | Load test execution |
| Deliverable IDs | D-0051 |

**Deliverables:**
- k6 test script for POST /auth/login targeting p95 < 200ms at 100 concurrent users / 50 req/s

**Steps:**
1. [PLANNING] Define load profile per NFR-AUTH.1 and OQ-1 resolution
2. [EXECUTION] Write k6 script with ramp-up, sustained load, and p95 threshold
3. [VERIFICATION] Run test; capture and evaluate results

**Acceptance Criteria:**
- p95 latency < 200ms at defined normal load
- No errors during sustained load phase
- Results captured as CI artifact

**Validation:**
- Manual check: Review k6 summary output for p95 value
- Evidence: k6 script and results report committed

**Dependencies:** T03.05

---

### T04.02 -- k6 load test: token refresh endpoint

| Field | Value |
|---|---|
| Roadmap Item IDs | R-052 |
| Why | NFR-AUTH.1 requires same latency target for token refresh as other endpoints. |
| Effort | S |
| Risk | Medium |
| Risk Drivers | token |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Critical Path Override | Yes |
| Verification Method | Load test execution |
| Deliverable IDs | D-0052 |

**Deliverables:**
- k6 test script for POST /auth/refresh targeting p95 < 200ms

**Steps:**
1. [PLANNING] Define load profile matching login test
2. [EXECUTION] Write k6 script for refresh endpoint
3. [VERIFICATION] Run test; capture results

**Acceptance Criteria:**
- p95 latency < 200ms at normal load
- Token rotation completes under load without errors

**Validation:**
- Manual check: Review k6 output
- Evidence: k6 script and results committed

**Dependencies:** T03.07

---

### T04.03 -- k6 load test: registration endpoint

| Field | Value |
|---|---|
| Roadmap Item IDs | R-053 |
| Why | Registration includes bcrypt hashing, so higher latency is expected; baseline must be documented. |
| Effort | S |
| Risk | Low |
| Risk Drivers | — |
| Tier | STANDARD |
| Confidence | [████████--] 88% |
| Critical Path Override | No |
| Verification Method | Load test execution |
| Deliverable IDs | D-0053 |

**Deliverables:**
- k6 test script for POST /auth/register with documented baseline latency

**Steps:**
1. [PLANNING] Define load profile; expect higher latency due to bcrypt
2. [EXECUTION] Write k6 script for registration
3. [VERIFICATION] Run test; document baseline

**Acceptance Criteria:**
- Baseline p95 latency documented (expected ~300-500ms due to bcrypt)
- No errors under load
- Results captured as artifact

**Validation:**
- Manual check: Review k6 output and baseline documentation
- Evidence: k6 script, results, and baseline doc committed

**Dependencies:** T03.06

---

### T04.04 -- Benchmark bcrypt cost factor 12 timing

| Field | Value |
|---|---|
| Roadmap Item IDs | R-054 |
| Why | NFR-AUTH.3 and SC-4 require ~250ms per bcrypt hash; benchmark must confirm this on target hardware. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | crypto |
| Tier | STRICT |
| Confidence | [█████████-] 93% |
| Critical Path Override | Yes |
| Verification Method | Benchmark test |
| Deliverable IDs | D-0054 |

**Deliverables:**
- Standalone benchmark test asserting bcrypt cost factor 12 produces ~250ms hash time (200-400ms range)

**Steps:**
1. [PLANNING] Define benchmark parameters per NFR-AUTH.3
2. [EXECUTION] Write benchmark running 10+ iterations, computing mean/p95
3. [VERIFICATION] Assert mean within 200-400ms range

**Acceptance Criteria:**
- Mean hash time within 200-400ms at cost factor 12
- Benchmark runs on CI hardware
- Results captured in CI output

**Validation:**
- Manual check: Review benchmark output timing values
- Evidence: Benchmark script committed; CI artifact

**Dependencies:** T01.04

---

### T04.05 -- Security test: replay detection

| Field | Value |
|---|---|
| Roadmap Item IDs | R-055 |
| Why | FR-AUTH.3c and RISK-2 require adversarial testing that reused revoked tokens trigger full token invalidation. |
| Effort | M |
| Risk | High |
| Risk Drivers | token, security |
| Tier | STRICT |
| Confidence | [████████--] 85% |
| Critical Path Override | Yes |
| Verification Method | Adversarial test execution |
| Deliverable IDs | D-0055 |

**Deliverables:**
- Adversarial test: reuse revoked refresh token, confirm ALL user tokens invalidated

**Steps:**
1. [PLANNING] Design replay attack scenario
2. [EXECUTION] Write test: login -> refresh (save old token) -> attempt old token -> verify all tokens revoked
3. [VERIFICATION] Confirm user has zero active tokens after replay

**Acceptance Criteria:**
- Replayed revoked token triggers full revocation
- All active refresh tokens for user are invalidated
- Subsequent refresh attempts fail with 401
- Database confirms zero active tokens

**Validation:**
- Manual check: Query refresh_tokens table after replay
- Evidence: Adversarial test committed; CI green

**Dependencies:** T03.07, T02.02

---

> **CHECKPOINT 10** (after T04.05): Verify T04.01--T04.05 pass. Performance baselines established. Replay detection adversarial test passes.

---

### T04.06 -- Security test: XSS prevention (httpOnly cookie)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-056 |
| Why | FR-AUTH.1-IMPL-2 requires refresh tokens only in httpOnly cookies, never in response bodies, preventing XSS theft. |
| Effort | S |
| Risk | High |
| Risk Drivers | token, security |
| Tier | STRICT |
| Confidence | [█████████-] 92% |
| Critical Path Override | Yes |
| Verification Method | Automated scan |
| Deliverable IDs | D-0056 |

**Deliverables:**
- Automated test: scan all endpoint responses, verify refresh token only appears in Set-Cookie header with httpOnly flag

**Steps:**
1. [PLANNING] Define scan scope: all auth endpoints
2. [EXECUTION] Write test: exercise all endpoints, check response bodies and headers
3. [VERIFICATION] Confirm no refresh token in body; cookie has httpOnly

**Acceptance Criteria:**
- No response body contains refresh token value
- Set-Cookie header includes HttpOnly flag
- Set-Cookie header includes Secure flag

**Validation:**
- Manual check: Inspect all Set-Cookie headers
- Evidence: Security test committed; CI green

**Dependencies:** T03.05, T03.07

---

### T04.07 -- Security test: information leakage

| Field | Value |
|---|---|
| Roadmap Item IDs | R-057 |
| Why | FR-AUTH.1b requires generic 401 messages with no email/password differentiation to prevent enumeration. |
| Effort | S |
| Risk | High |
| Risk Drivers | auth, security |
| Tier | STRICT |
| Confidence | [█████████-] 92% |
| Critical Path Override | Yes |
| Verification Method | Automated test |
| Deliverable IDs | D-0057 |

**Deliverables:**
- Test verifying all auth error responses use identical generic messages

**Steps:**
1. [PLANNING] Catalog all error response scenarios
2. [EXECUTION] Write test: wrong email, wrong password, locked account - compare error messages
3. [VERIFICATION] Confirm messages are generic and identical where appropriate

**Acceptance Criteria:**
- Wrong email and wrong password produce identical 401 response body
- No error message reveals whether email exists
- Locked account returns 403 with generic message

**Validation:**
- Manual check: Compare error response bodies byte-for-byte
- Evidence: Information leakage test committed; CI green

**Dependencies:** T03.05

---

### T04.08 -- Security test: JWT validation failure modes

| Field | Value |
|---|---|
| Roadmap Item IDs | R-058 |
| Why | SC-5 requires comprehensive JWT failure mode testing: tampered, expired, and invalid signature. |
| Effort | S |
| Risk | Medium |
| Risk Drivers | token, security, crypto |
| Tier | STRICT |
| Confidence | [█████████-] 92% |
| Critical Path Override | Yes |
| Verification Method | Test execution |
| Deliverable IDs | D-0058 |

**Deliverables:**
- Security test suite covering: tampered JWT rejected, expired JWT rejected, invalid signature rejected

**Steps:**
1. [PLANNING] Define JWT attack vectors
2. [EXECUTION] Write tests: modify payload, use expired token, sign with wrong key
3. [VERIFICATION] All attacks return 401

**Acceptance Criteria:**
- Tampered payload: 401
- Expired token: 401
- Wrong signature: 401
- Algorithm none attack: 401

**Validation:**
- Manual check: Craft attack tokens, verify rejection
- Evidence: JWT security test suite committed; CI green

**Dependencies:** T03.01

---

### T04.09 -- Security test: sensitive field exclusion scan

| Field | Value |
|---|---|
| Roadmap Item IDs | R-059 |
| Why | SC-8 requires automated response schema scanning to ensure no password_hash or token hashes leak. |
| Effort | S |
| Risk | Medium |
| Risk Drivers | security |
| Tier | STRICT |
| Confidence | [█████████-] 92% |
| Critical Path Override | Yes |
| Verification Method | Automated scan |
| Deliverable IDs | D-0059 |

**Deliverables:**
- Automated response schema scanner checking all endpoints for sensitive field leakage

**Steps:**
1. [PLANNING] Define sensitive field list and endpoint scope
2. [EXECUTION] Write scanner: iterate all endpoints, parse responses, search for forbidden fields
3. [VERIFICATION] Run scanner; confirm zero violations

**Acceptance Criteria:**
- No endpoint returns password_hash field
- No endpoint returns token_hash or refresh_token_hash
- Scanner covers all 6 auth endpoints plus error responses

**Validation:**
- Manual check: Review scanner output
- Evidence: Scanner script and results committed

**Dependencies:** T03.15

---

### T04.10 -- Security test: password policy enforcement

| Field | Value |
|---|---|
| Roadmap Item IDs | R-060 |
| Why | FR-AUTH.2c password policy must be enforced at the API level with boundary value testing. |
| Effort | S |
| Risk | Low |
| Risk Drivers | password, security |
| Tier | STRICT |
| Confidence | [█████████-] 93% |
| Critical Path Override | Yes |
| Verification Method | Test execution |
| Deliverable IDs | D-0060 |

**Deliverables:**
- Boundary value test suite for password policy: 7-char, 8-char, missing each character class

**Steps:**
1. [PLANNING] Define boundary test cases per FR-AUTH.2c
2. [EXECUTION] Write tests: 7 chars (fail), 8 chars all classes (pass), missing uppercase/lowercase/digit
3. [VERIFICATION] All boundary cases behave correctly

**Acceptance Criteria:**
- 7-character password rejected
- 8-character password with all classes accepted
- Missing uppercase rejected
- Missing lowercase rejected
- Missing digit rejected

**Validation:**
- Manual check: Attempt registration with boundary passwords
- Evidence: Boundary test suite committed; CI green

**Dependencies:** T03.06

---

> **CHECKPOINT 11** (after T04.10): Verify T04.06--T04.10 pass. All security test suites pass. No information leakage or sensitive field exposure.

---

### T04.11 -- Security test: no plaintext passwords stored

| Field | Value |
|---|---|
| Roadmap Item IDs | R-061 |
| Why | FR-AUTH.1-IMPL-1 mandates no plaintext password storage; database audit confirms compliance. |
| Effort | XS |
| Risk | High |
| Risk Drivers | password, security, database |
| Tier | STRICT |
| Confidence | [█████████-] 95% |
| Critical Path Override | Yes |
| Verification Method | Database audit |
| Deliverable IDs | D-0061 |

**Deliverables:**
- Database audit test: register user, query password_hash column, verify bcrypt format

**Steps:**
1. [PLANNING] Define audit approach
2. [EXECUTION] Write test: register user, query database, assert password_hash starts with $2b$
3. [VERIFICATION] Run audit; confirm no plaintext

**Acceptance Criteria:**
- All password_hash values match bcrypt format ($2b$12$...)
- No plaintext passwords in any database column
- Audit covers users table

**Validation:**
- Manual check: Query users table, inspect password_hash values
- Evidence: Audit test committed; CI green

**Dependencies:** T03.06

---

### T04.12 -- Security test: verify RS256 key size (4096-bit)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-062 |
| Why | NFR-AUTH-IMPL-1 specifies 4096-bit RSA keys; key inspection confirms compliance. |
| Effort | XS |
| Risk | Medium |
| Risk Drivers | crypto, security |
| Tier | STRICT |
| Confidence | [█████████-] 95% |
| Critical Path Override | Yes |
| Verification Method | Key inspection test |
| Deliverable IDs | D-0062 |

**Deliverables:**
- Test that inspects loaded RSA key and asserts 4096-bit key size

**Steps:**
1. [PLANNING] Define key inspection approach
2. [EXECUTION] Write test: load key via JwtService, inspect key size
3. [VERIFICATION] Assert key size is 4096 bits

**Acceptance Criteria:**
- RSA key size is exactly 4096 bits
- Test loads key through same path as production

**Validation:**
- Manual check: openssl rsa -text on key file
- Evidence: Key inspection test committed; CI green

**Dependencies:** T01.09

---

### T04.13 -- Security test: verify cookie attributes

| Field | Value |
|---|---|
| Roadmap Item IDs | R-063 |
| Why | FR-AUTH.1-IMPL-2 requires httpOnly, Secure, and SameSite=Strict attributes on refresh token cookies. |
| Effort | XS |
| Risk | Medium |
| Risk Drivers | token, security |
| Tier | STRICT |
| Confidence | [█████████-] 95% |
| Critical Path Override | Yes |
| Verification Method | Header verification test |
| Deliverable IDs | D-0063 |

**Deliverables:**
- Test verifying Set-Cookie header contains HttpOnly, Secure, and SameSite=Strict

**Steps:**
1. [PLANNING] Define expected cookie attributes
2. [EXECUTION] Write test: login, inspect Set-Cookie header for all 3 attributes
3. [VERIFICATION] Assert all attributes present

**Acceptance Criteria:**
- HttpOnly attribute present
- Secure attribute present
- SameSite=Strict attribute present

**Validation:**
- Manual check: Inspect Set-Cookie header with curl -v
- Evidence: Cookie attribute test committed; CI green

**Dependencies:** T03.05

---

### T04.14 -- Measure and enforce line coverage >= 90%

| Field | Value |
|---|---|
| Roadmap Item IDs | R-064 |
| Why | SC-5 and SC-6 require >= 90% line coverage across all unit and integration tests. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | — |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Critical Path Override | No |
| Verification Method | Coverage report |
| Deliverable IDs | D-0064 |

**Deliverables:**
- Coverage configuration enforcing >= 90% line coverage; coverage report artifact

**Steps:**
1. [PLANNING] Configure coverage tool with 90% threshold
2. [EXECUTION] Run full test suite with coverage; identify and fill gaps
3. [VERIFICATION] CI fails if coverage drops below 90%

**Acceptance Criteria:**
- Line coverage >= 90% across all auth modules
- CI enforces coverage threshold
- Coverage report generated as artifact

**Validation:**
- Manual check: Review coverage report for gaps
- Evidence: Coverage config and report committed

**Dependencies:** T02.14, T03.17

---

### T04.15 -- Measure and enforce branch coverage >= 85%

| Field | Value |
|---|---|
| Roadmap Item IDs | R-065 |
| Why | SC-5 and SC-6 require >= 85% branch coverage; identifies untested conditional paths. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | — |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Critical Path Override | No |
| Verification Method | Coverage report |
| Deliverable IDs | D-0065 |

**Deliverables:**
- Branch coverage measurement and enforcement at >= 85%; gap analysis

**Steps:**
1. [PLANNING] Identify branch coverage gaps from current test suite
2. [EXECUTION] Write additional tests to cover missing branches
3. [VERIFICATION] Branch coverage meets 85% threshold

**Acceptance Criteria:**
- Branch coverage >= 85% across all auth modules
- CI enforces branch coverage threshold
- Gap analysis documented

**Validation:**
- Manual check: Review branch coverage report
- Evidence: Coverage report and gap analysis committed

**Dependencies:** T04.14

---

> **CHECKPOINT 12** (after T04.15): Verify T04.11--T04.15 pass. All security audits pass. Coverage thresholds met (90% line, 85% branch).

---

### T04.16 -- Critical path coverage >= 95%

| Field | Value |
|---|---|
| Roadmap Item IDs | R-066 |
| Why | SC-7 requires >= 95% coverage on critical paths: login, token refresh, and password reset flows. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | auth, security |
| Tier | STRICT |
| Confidence | [████████--] 85% |
| Critical Path Override | Yes |
| Verification Method | Coverage report |
| Deliverable IDs | D-0066 |

**Deliverables:**
- Critical path coverage measurement at >= 95% for login, refresh, and reset flows

**Steps:**
1. [PLANNING] Define critical path modules and coverage scope
2. [EXECUTION] Ensure test coverage for all critical paths reaches 95%
3. [VERIFICATION] Generate targeted coverage report for critical modules

**Acceptance Criteria:**
- Login flow coverage >= 95%
- Token refresh flow coverage >= 95%
- Password reset flow coverage >= 95%

**Validation:**
- Manual check: Review per-module coverage for critical paths
- Evidence: Critical path coverage report committed

**Dependencies:** T04.14, T04.15

---

### T04.17 -- Test AUTH_SERVICE_ENABLED=false behavior

| Field | Value |
|---|---|
| Roadmap Item IDs | R-067 |
| Why | SC-9 requires verification that disabling the flag makes auth routes return expected disabled status. |
| Effort | S |
| Risk | Low |
| Risk Drivers | — |
| Tier | STANDARD |
| Confidence | [█████████-] 92% |
| Critical Path Override | No |
| Verification Method | Integration test |
| Deliverable IDs | D-0067 |

**Deliverables:**
- Integration test: set flag to false, verify auth routes return 503/404, non-auth routes unaffected

**Steps:**
1. [PLANNING] Define disabled behavior expectations per SC-9
2. [EXECUTION] Write test: toggle flag off, request all auth endpoints, verify responses
3. [VERIFICATION] All auth endpoints return disabled response; non-auth endpoints work

**Acceptance Criteria:**
- Auth routes return expected disabled status (503 or 404)
- Non-auth routes are completely unaffected
- No auth middleware intercepts requests when disabled

**Validation:**
- Manual check: Toggle flag and exercise endpoints
- Evidence: Integration test committed; CI green

**Dependencies:** T02.15, T02.16

---

### T04.18 -- Test database down-migrations

| Field | Value |
|---|---|
| Roadmap Item IDs | R-068 |
| Why | FR-AUTH.1-IMPL-5 requires all migrations to be reversible for safe rollback. |
| Effort | S |
| Risk | Medium |
| Risk Drivers | migration, database |
| Tier | STRICT |
| Confidence | [█████████-] 92% |
| Critical Path Override | Yes |
| Verification Method | Migration test |
| Deliverable IDs | D-0068 |

**Deliverables:**
- Test running all migrations down and verifying clean database state

**Steps:**
1. [PLANNING] Define clean state criteria
2. [EXECUTION] Write test: apply all migrations up, then all down, verify no auth tables
3. [VERIFICATION] Database has no auth-related artifacts

**Acceptance Criteria:**
- All migrations run down without error
- No auth-related tables remain after full rollback
- No orphaned indexes or constraints

**Validation:**
- Manual check: Inspect database after full rollback
- Evidence: Migration rollback test committed; CI green

**Dependencies:** T01.03

---

### T04.19 -- Document rollback procedure

| Field | Value |
|---|---|
| Roadmap Item IDs | R-069 |
| Why | SC-9 requires a documented runbook for on-call engineers to perform rollback. |
| Effort | M |
| Risk | Low |
| Risk Drivers | — |
| Tier | EXEMPT |
| Confidence | [█████████-] 93% |
| Critical Path Override | No |
| Verification Method | Document review |
| Deliverable IDs | D-0069 |

**Deliverables:**
- Rollback runbook documenting: feature flag toggle, migration rollback, verification steps

**Steps:**
1. [PLANNING] Define runbook structure and audience (on-call engineers)
2. [EXECUTION] Write step-by-step rollback procedure with verification at each step
3. [VERIFICATION] Peer review of runbook for completeness

**Acceptance Criteria:**
- Covers feature flag toggle procedure
- Covers database migration rollback procedure
- Includes verification steps after each action
- Target: rollback < 5 minutes

**Validation:**
- Manual check: Peer review sign-off
- Evidence: Runbook document committed

**Dependencies:** T04.17, T04.18

---

### T04.20 -- Health check endpoint

| Field | Value |
|---|---|
| Roadmap Item IDs | R-070 |
| Why | NFR-AUTH.2 requires /health endpoint for uptime monitoring and deployment readiness checks. |
| Effort | S |
| Risk | Low |
| Risk Drivers | — |
| Tier | STANDARD |
| Confidence | [█████████-] 95% |
| Critical Path Override | No |
| Verification Method | Automated test |
| Deliverable IDs | D-0070 |

**Deliverables:**
- GET /health endpoint returning 200 with service status (database connectivity, key availability)

**Steps:**
1. [PLANNING] Define health check components
2. [EXECUTION] Implement endpoint checking database and key availability
3. [VERIFICATION] Test: healthy returns 200, unhealthy returns 503

**Acceptance Criteria:**
- Returns 200 with status JSON when healthy
- Returns 503 when database is unreachable
- Includes database connectivity check
- Does not expose sensitive information

**Validation:**
- Manual check: Hit /health endpoint
- Evidence: Health check implementation and test committed

**Dependencies:** T01.14

---

> **CHECKPOINT 13** (after T04.20): Verify T04.16--T04.20 pass. Critical path coverage met. Rollback verified. Health check functional.

---

### T04.21 -- APM integration for latency tracking

| Field | Value |
|---|---|
| Roadmap Item IDs | R-071 |
| Why | NFR-AUTH.1 and SC-2 require p50, p95, p99 latency dashboards for ongoing monitoring. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | — |
| Tier | STANDARD |
| Confidence | [████████--] 82% |
| Critical Path Override | No |
| Verification Method | Dashboard verification |
| Deliverable IDs | D-0071 |

**Deliverables:**
- APM instrumentation on all auth endpoints; dashboard configuration for p50, p95, p99 latency

**Steps:**
1. [PLANNING] Select APM tool and define instrumentation points
2. [EXECUTION] Add instrumentation to all auth route handlers and middleware
3. [VERIFICATION] Verify metrics appear in dashboard

**Acceptance Criteria:**
- All 6 auth endpoints instrumented
- Dashboard shows p50, p95, p99 latency
- Latency broken down by endpoint

**Validation:**
- Manual check: Generate traffic, verify dashboard populates
- Evidence: APM configuration and dashboard screenshot committed

**Dependencies:** T03.05, T03.06, T03.07, T03.08, T03.09, T03.10

---

### T04.22 -- Uptime monitoring configuration

| Field | Value |
|---|---|
| Roadmap Item IDs | R-072 |
| Why | NFR-AUTH.2 and SC-3 require 99.9% uptime monitoring with alerting integration. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | — |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Critical Path Override | No |
| Verification Method | Configuration review |
| Deliverable IDs | D-0072 |

**Deliverables:**
- Uptime monitoring configured for /health endpoint with PagerDuty/alerting integration

**Steps:**
1. [PLANNING] Define monitoring interval and alert thresholds
2. [EXECUTION] Configure uptime monitor targeting /health endpoint
3. [VERIFICATION] Simulate downtime, verify alert fires

**Acceptance Criteria:**
- Health check monitored at configured interval
- Alert fires on consecutive failures
- PagerDuty/alerting integration functional

**Validation:**
- Manual check: Take health endpoint down, verify alert
- Evidence: Monitoring configuration committed

**Dependencies:** T04.20

---

> **END-OF-PHASE CHECKPOINT** (Phase 4 Gate): All success criteria SC-1 through SC-9 validated. Security test suites pass. Coverage targets met (90% line, 85% branch, 95% critical path). Performance validated. Rollback verified. Production deployment approved. All deliverables D-0051 through D-0072 produced and verified.
