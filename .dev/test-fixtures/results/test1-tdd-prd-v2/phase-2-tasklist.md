# Phase 2 -- Password Reset, Compliance, and Beta

Implement password reset flow (FR-AUTH-005). Deploy admin audit log query API (GAP-003) for persona Jordan. Deploy to production at 10% traffic. Validate NFRs under production load. Complete compliance pre-audit preparation. PRD persona Jordan's audit investigation needs are addressed in this phase. Success metric targets: p95 < 200ms, registration conversion > 40% (beta) / > 60% (GA), error rate < 0.1%.

### T02.01 -- Implement POST /auth/reset-request Endpoint

| Field | Value |
|---|---|
| Roadmap Item IDs | R-028 |
| Why | Password reset request per FR-AUTH-005. Sends reset token via SendGrid. Same response regardless of registration (no enumeration). Token: 1-hour TTL, single-use. Serves persona Alex's Password Reset journey (PRD S22). |
| Effort | L |
| Risk | High |
| Risk Drivers | security, authentication, credentials |
| Tier | STRICT |
| Confidence | [██████████] 95% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0030 |

**Artifacts (Intended Paths):**
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0030/spec.md`

**Deliverables:**
1. POST /auth/reset-request: email in body → sends reset token via SendGrid queue; same response for registered/unregistered (no enumeration); token 1-hour TTL, single-use

**Steps:**
1. **[PLANNING]** Review TDD §8 for /auth/reset-request spec and PRD S22 for Password Reset journey (5 steps)
2. **[PLANNING]** Verify SendGrid API key provisioned
3. **[EXECUTION]** Implement endpoint: generate reset token (1-hour TTL, single-use), queue email via SendGrid
4. **[EXECUTION]** Use async queue-based delivery for resilience (OQ-PRD-001 resolution)
5. **[EXECUTION]** Implement email delivery monitoring and alerting (R-007 mitigation)
6. **[VERIFICATION]** Tests: valid email → token sent, unregistered email → same response (no enumeration), token expires after 1 hour, token single-use
7. **[COMPLETION]** Document endpoint and email delivery monitoring

**Acceptance Criteria:**
- FR-AUTH-005 AC #1: Reset request sends email with token link
- No enumeration: same HTTP response for registered and unregistered emails
- Token expires after 1 hour
- Token is single-use (second attempt with same token → 400)

**Validation:**
- Manual check: Request reset for registered email → email received with valid token link
- Evidence: `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0030/evidence.md`

**Dependencies:** T01.10 (AuthService), SendGrid API key
**Rollback:** Disable endpoint

### T02.02 -- Implement POST /auth/reset-confirm Endpoint

| Field | Value |
|---|---|
| Roadmap Item IDs | R-029 |
| Why | Password reset confirmation per FR-AUTH-005. Token + new password → updates hash via PasswordHasher. Invalidates all refresh tokens. |
| Effort | M |
| Risk | High |
| Risk Drivers | security, credentials, authentication |
| Tier | STRICT |
| Confidence | [██████████] 95% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0031 |

**Artifacts (Intended Paths):**
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0031/spec.md`

**Deliverables:**
1. POST /auth/reset-confirm: token + new password → update password hash, invalidate all refresh tokens, audit log entry

**Steps:**
1. **[PLANNING]** Review TDD §8 for /auth/reset-confirm spec
2. **[EXECUTION]** Validate token (exists, not expired, single-use)
3. **[EXECUTION]** Hash new password via PasswordHasher, update in UserRepo
4. **[EXECUTION]** Invalidate ALL refresh tokens for the user in Redis (force re-login everywhere)
5. **[VERIFICATION]** Tests: valid token + password → 200, expired → 400, already used → 400, all refresh tokens revoked
6. **[COMPLETION]** Document endpoint

**Acceptance Criteria:**
- Valid reset token + strong password → password updated, 200 response
- Expired token → 400
- Already-used token → 400
- All refresh tokens for the user revoked (force re-login on all devices)

**Validation:**
- Manual check: Reset password → login with new password → old refresh tokens invalid
- Evidence: `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0031/evidence.md`

**Dependencies:** T02.01 (reset-request), T01.06 (PasswordHasher), T01.08 (TokenManager)
**Rollback:** Revert endpoint

### T02.03 -- Integrate SendGrid Email Service

| Field | Value |
|---|---|
| Roadmap Item IDs | R-030 |
| Why | External email delivery via async queue for password reset. Resilient delivery with monitoring and alerting. R-007 mitigation (email delivery failures). |
| Effort | M |
| Risk | Medium |
| Risk Drivers | depends, requires |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0032 |

**Artifacts (Intended Paths):**
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0032/spec.md`

**Deliverables:**
1. SendGrid API integration via async queue with delivery monitoring, alerting, and fallback support channel documentation

**Steps:**
1. **[PLANNING]** Review Wiring Task 2.1.1 for SendGrid integration pattern
2. **[EXECUTION]** Implement email queue worker with SendGrid API client
3. **[EXECUTION]** Configure SendGrid webhooks for delivery monitoring
4. **[EXECUTION]** Set up delivery failure alerting
5. **[VERIFICATION]** Integration test: queue email → SendGrid delivers → webhook confirms delivery
6. **[COMPLETION]** Document fallback support channel for email delivery failures

**Acceptance Criteria:**
- Emails queued and delivered via SendGrid API
- Delivery monitoring via webhooks operational
- Alerting configured for delivery failures
- Fallback support channel documented

**Validation:**
- Manual check: Trigger password reset → email delivered within 2 seconds → delivery webhook received
- Evidence: `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0032/evidence.md`

**Dependencies:** SendGrid API key, T02.01 (reset-request endpoint)
**Rollback:** Remove SendGrid integration; manual email fallback

### T02.04 -- Implement Admin Audit Log Query API

| Field | Value |
|---|---|
| Roadmap Item IDs | R-031 |
| Why | GET /admin/auth/audit-logs per GAP-003. Queryable by date range, user_id, event type. Admin role authorization. Serves persona Jordan's primary need: view authentication event logs for incident investigation and auditors. |
| Effort | M |
| Risk | High |
| Risk Drivers | security, compliance, audit, permissions |
| Tier | STRICT |
| Confidence | [██████████] 95% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0033 |

**Artifacts (Intended Paths):**
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0033/spec.md`

**Deliverables:**
1. GET /admin/auth/audit-logs: queryable by date range, user_id, event type; protected by admin role; rate limit 10 req/min; query performance < 1 second

**Steps:**
1. **[PLANNING]** Review roadmap 2.2 for audit API spec and PRD persona Jordan's needs
2. **[EXECUTION]** Implement query API with filter parameters (date range, user_id, event type)
3. **[EXECUTION]** Implement admin role authorization (only admin users can access)
4. **[EXECUTION]** Configure rate limiting: 10 req/min
5. **[VERIFICATION]** Tests: valid admin query → results; non-admin → 403; query performance < 1 second; filters work correctly
6. **[COMPLETION]** Document API endpoint for compliance team

**Acceptance Criteria:**
- Admin query returns audit events filtered by date range, user_id, event type
- Non-admin users receive 403 Forbidden
- Query performance < 1 second for typical auditor query
- Validates NFR-COMP-002 (SOC2 audit logging) end-to-end

**Validation:**
- Manual check: Admin user queries audit logs by date range → results returned in < 1 second
- Evidence: `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0033/evidence.md`

**Dependencies:** T01.17 (audit logging foundation), T01.01 (audit log table)
**Rollback:** Disable endpoint

### T02.05 -- Complete Compliance and Audit Readiness

| Field | Value |
|---|---|
| Roadmap Item IDs | R-032 |
| Why | SOC2 pre-audit preparation. Verify audit logging, GDPR consent tracking, admin query API with compliance and legal teams. |
| Effort | M |
| Risk | High |
| Risk Drivers | compliance, audit, gdpr |
| Tier | STRICT |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0034 |

**Artifacts (Intended Paths):**
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0034/spec.md`

**Deliverables:**
1. Compliance validation report: audit log verification (100 entries spot-checked), GDPR consent tracking confirmed, SOC2 control validation complete, admin query validated by compliance team

**Steps:**
1. **[PLANNING]** Coordinate with security-team, legal-team, compliance-team per roadmap 2.3
2. **[EXECUTION]** Spot-check 100 audit log entries: all fields present, correct format
3. **[EXECUTION]** Verify GDPR consent field stored at registration with timestamp
4. **[EXECUTION]** Validate SOC2 controls: audit log queryable, retention enforced, sample report generated
5. **[VERIFICATION]** Compliance team confirms: admin query returns correct data, retention policy verified
6. **[COMPLETION]** File compliance validation report

**Acceptance Criteria:**
- 100 audit log entries spot-checked with all required fields present
- GDPR consent_given + consent_timestamp stored on every registration
- SOC2 audit log queryable, 12-month retention confirmed
- Persona Jordan can query by date range, user_id, event type with < 1s response

**Validation:**
- Manual check: Compliance team signs off on SOC2 pre-audit readiness
- Evidence: `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0034/spec.md`

**Dependencies:** T02.04 (admin audit API), T01.17 (audit logging)
**Rollback:** N/A (validation only)

### Checkpoint: Phase 2 / Tasks 01-05

**Purpose:** Verify password reset and compliance features complete before production deployment.
**Checkpoint Report Path:** `.dev/test-fixtures/results/test1-tdd-prd-v2/checkpoints/CP-P02-T01-T05.md`
**Verification:**
- Password reset flow: request → email → confirm → password updated → all tokens revoked
- Admin audit query returns correct results with < 1s performance
- Compliance team has validated SOC2 readiness
**Exit Criteria:**
- FR-AUTH-005 acceptance criteria pass
- GAP-003 resolved (admin audit API operational)
- SOC2 pre-audit preparation complete

### T02.06 -- Execute Production Deployment and Internal Alpha

| Field | Value |
|---|---|
| Roadmap Item IDs | R-033 |
| Why | Deploy AuthService to production with AUTH_NEW_LOGIN=OFF. Internal testing against production infrastructure before external traffic. |
| Effort | L |
| Risk | High |
| Risk Drivers | deploy, breaking |
| Tier | STRICT |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0035 |

**Artifacts (Intended Paths):**
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0035/spec.md`

**Deliverables:**
1. Production deployment of AuthService with AUTH_NEW_LOGIN=OFF; internal testing verified; observability stack operational in production

**Steps:**
1. **[PLANNING]** Review deployment checklist and rollback procedure from roadmap 2.4
2. **[EXECUTION]** Deploy AuthService and all dependencies to production with AUTH_NEW_LOGIN=OFF
3. **[EXECUTION]** auth-team and QA manually test all endpoints against production PostgreSQL and Redis
4. **[EXECUTION]** Run integration test suite against production infrastructure
5. **[VERIFICATION]** Validate observability: metrics, dashboards, alerts, traces operational in production
6. **[COMPLETION]** Document deployment evidence and production test results

**Acceptance Criteria:**
- AuthService running in production with AUTH_NEW_LOGIN=OFF (no external traffic)
- All endpoints pass manual testing against production databases
- Integration test suite passes against production infrastructure
- Metrics and dashboards operational in production Grafana

**Validation:**
- Manual check: All production smoke tests pass; Grafana shows production metrics
- Evidence: `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0035/evidence.md`

**Dependencies:** All Phase 1 tasks, T02.01-T02.05 (password reset + compliance)
**Rollback:** Disable AUTH_NEW_LOGIN; rollback deployment

### T02.07 -- Execute Beta 10% Traffic Shift and Monitoring

| Field | Value |
|---|---|
| Roadmap Item IDs | R-034 |
| Why | Enable AUTH_NEW_LOGIN for 10% production traffic. 7-day monitoring window validates all NFRs under real load. Success metric targets from PRD S19. |
| Effort | XL |
| Risk | High |
| Risk Drivers | performance, deploy, end-to-end |
| Tier | STRICT |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0036, D-0037 |

**Artifacts (Intended Paths):**
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0036/spec.md`
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0037/spec.md`

**Deliverables:**
1. Beta 10% traffic enabled via AUTH_NEW_LOGIN flag with consistent user-hash routing
2. 7-day monitoring report: p95 < 200ms, error rate < 0.1%, 99.9% uptime, registration conversion funnel, password reset funnel

**Steps:**
1. **[PLANNING]** Review roadmap 2.5 for monitoring thresholds, alert rules, and automatic rollback triggers
2. **[EXECUTION]** Enable AUTH_NEW_LOGIN for 10% of traffic (user ID hash for consistent routing)
3. **[EXECUTION]** Configure alert thresholds per roadmap table (p95 > 500ms, error > 5%, Redis failures, pool exhaustion, brute force)
4. **[EXECUTION]** Configure automatic rollback triggers (p95 > 1s for 5 min, error > 5% for 2 min, Redis > 10 failures/min, data corruption)
5. **[EXECUTION]** Monitor continuously for 7 days: p95, error rate, Redis health, conversion funnel
6. **[VERIFICATION]** After 7 days: all metrics within targets; zero automatic rollback events; zero data corruption
7. **[COMPLETION]** File 7-day monitoring report with metric summaries

**Acceptance Criteria:**
- p95 latency < 200ms sustained (NFR-PERF-001, PRD S19 "login p95 < 200ms")
- Error rate < 0.1% throughout beta window
- Registration conversion rate tracked (target > 40% beta, > 60% GA per PRD S19)
- Password reset completion tracked (target > 70% beta, > 80% GA per PRD S19)

**Validation:**
- Manual check: 7-day metrics show all thresholds met; zero rollback events
- Evidence: Monitoring report at `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0036/evidence.md`

**Dependencies:** T02.06 (production deployment)
**Rollback:** Disable AUTH_NEW_LOGIN → 100% traffic to legacy

**Subtasks (XL decomposition):**
- T02.07a: Enable 10% traffic routing
- T02.07b: Configure alert thresholds and automatic rollback triggers
- T02.07c: Execute 7-day monitoring window
- T02.07d: Compile monitoring report

### T02.08 -- Execute Load Testing and Performance Validation

| Field | Value |
|---|---|
| Roadmap Item IDs | R-035 |
| Why | Validate NFR-PERF-001 (p95 < 200ms) and NFR-PERF-002 (500 concurrent logins) under production-like load. |
| Effort | L |
| Risk | Medium |
| Risk Drivers | performance, latency |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0038 |

**Artifacts (Intended Paths):**
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0038/spec.md`

**Deliverables:**
1. Load test report: 500 concurrent logins (p95 < 200ms, 0% error), sustained 100 req/sec for 10 min, token refresh under load, DB connection limits, password reset flow at 50 concurrent

**Steps:**
1. **[PLANNING]** Review roadmap 2.6 load test table for exact scenarios and success criteria
2. **[EXECUTION]** Run k6: 500 concurrent logins (p95 < 200ms, error < 0.1%)
3. **[EXECUTION]** Run k6: 100 req/sec sustained 10 min (no pool exhaustion)
4. **[EXECUTION]** Run k6: 200 concurrent token refreshes (p95 < 100ms)
5. **[EXECUTION]** Run k6: 500 concurrent login + profile (no connection timeouts)
6. **[VERIFICATION]** All 5 load tests pass their success criteria
7. **[COMPLETION]** File load test report with k6 output

**Acceptance Criteria:**
- NFR-PERF-001: p95 < 200ms for login under 500 concurrent
- NFR-PERF-002: 500 concurrent logins with 0% error rate
- Token refresh p95 < 100ms under 200 concurrent
- No connection pool exhaustion under combined load

**Validation:**
- Manual check: k6 output shows all scenarios pass
- Evidence: k6 reports at `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0038/evidence.md`

**Dependencies:** T02.06 (production deployment), T02.07 (beta traffic)
**Rollback:** N/A (testing only; performance tuning in T02.09)

### T02.09 -- Execute Performance Tuning (If Needed)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-036 |
| Why | Address bottlenecks identified in load testing: PasswordHasher slow (bcrypt cost), TokenManager Redis latency, UserRepo query latency. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | performance, latency, database |
| Tier | STANDARD |
| Confidence | [██████░░--] 65% |
| Requires Confirmation | Yes |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0039 |

**Artifacts (Intended Paths):**
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0039/spec.md`

**Deliverables:**
1. Performance tuning report documenting any bottleneck mitigations applied (or "no tuning needed" if load tests passed clean)

**Steps:**
1. **[PLANNING]** Review load test results (T02.08) for bottleneck identification
2. **[EXECUTION]** If PasswordHasher > 500ms: reduce bcrypt cost to 11, profile CPU, validate timing invariance
3. **[EXECUTION]** If Redis latency high: increase replica count, enable read-from-replica
4. **[EXECUTION]** If UserRepo query slow: add database index on email, profile query plans
5. **[VERIFICATION]** Re-run affected load tests to confirm improvements
6. **[COMPLETION]** Document tuning actions and results

**Acceptance Criteria:**
- All load test targets met after tuning (or already met without tuning)
- Any bcrypt cost reduction documented with security team approval
- Database indexes added if needed
- No regression in other performance metrics

**Validation:**
- Manual check: Re-run k6 tests showing improved metrics (or original tests passing)
- Evidence: `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0039/spec.md`

**Dependencies:** T02.08 (load test results)
**Rollback:** Revert tuning changes
**Notes:** Tier conflict: performance keywords → STANDARD; conditional execution → LIGHT. Resolved to STANDARD by priority (STANDARD > LIGHT when implementation changes possible).

### Checkpoint: End of Phase 2

**Purpose:** Final Phase 2 gate. Verify all exit criteria before GA rollout.
**Checkpoint Report Path:** `.dev/test-fixtures/results/test1-tdd-prd-v2/checkpoints/CP-P02-END.md`
**Verification:**
- FR-AUTH-005 acceptance criteria pass (reset request, confirm, expiry, single-use)
- NFR-PERF-001 and NFR-PERF-002 validated in production
- 7-day beta monitoring: 99.9% uptime, error < 0.1%, zero data corruption
**Exit Criteria:**
- All Phase 2 exit criteria from roadmap met (9 items)
- E2E test passes: register → login → profile → refresh → logout → password reset
- Compliance pre-audit preparation complete
