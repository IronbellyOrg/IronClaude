# Phase 3 -- GA Rollout and Stabilization

Ramp to 100% production traffic. Execute pre-GA penetration testing (dual security gate with Phase 1 checkpoint). Remove feature flags. Deprecate legacy auth. Establish on-call rotation. Validate all PRD success metrics (S19) baselines. Post-GA stabilization per debate convergence recommendation.

### T03.01 -- Execute Pre-GA Security Gate and Penetration Testing

| Field | Value |
|---|---|
| Roadmap Item IDs | R-037 |
| Why | Dual security gate: Phase 3 pentest complements Phase 1 checkpoint. External firm tests XSS token theft (R-001), brute force (R-002), enumeration, reset token security. Per PRD S17 (Legal & Compliance). |
| Effort | L |
| Risk | High |
| Risk Drivers | security, vulnerability, audit, compliance |
| Tier | STRICT |
| Confidence | [██████████] 95% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0040 |

**Artifacts (Intended Paths):**
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0040/spec.md`

**Deliverables:**
1. Penetration test report: XSS token theft, brute force, user enumeration, password reset token security, NIST SP 800-63B compliance, HttpOnly cookie verification. Zero unresolved critical/high findings.

**Steps:**
1. **[PLANNING]** Scope pentest: focus areas per roadmap 3.1 (R-001, R-002, enumeration, reset tokens)
2. **[EXECUTION]** Engage external firm for penetration testing
3. **[EXECUTION]** Security review of code changed since Phase 1 checkpoint (token refresh production, password reset, admin API)
4. **[EXECUTION]** Validate NIST SP 800-63B password policy compliance
5. **[EXECUTION]** Verify data minimization (NFR-COMP-003): only email, hashed password, displayName collected
6. **[VERIFICATION]** All critical/high findings remediated (remediation window Days 3-4)
7. **[COMPLETION]** File pentest report with security sign-off

**Acceptance Criteria:**
- Penetration test complete with zero unresolved critical or high findings
- NIST SP 800-63B compliance confirmed
- NFR-COMP-003 validated: only email, hashed password, displayName collected
- HttpOnly cookie confirmed across all supported browsers

**Validation:**
- Manual check: Pentest report shows zero critical/high findings after remediation
- Evidence: `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0040/spec.md`

**Dependencies:** All Phase 2 tasks complete
**Rollback:** N/A (testing only; remediation is separate)

### T03.02 -- Execute Traffic Ramp to GA (50% → 100%)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-038 |
| Why | Gradual ramp from 10% → 50% → 100%. Enable AUTH_TOKEN_REFRESH for all users. Validates system stability at full load. |
| Effort | M |
| Risk | High |
| Risk Drivers | deploy, end-to-end |
| Tier | STRICT |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0041 |

**Artifacts (Intended Paths):**
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0041/spec.md`

**Deliverables:**
1. GA traffic ramp: 50% stable for 8 hours → 100% stable for 1 hour → AUTH_TOKEN_REFRESH enabled → smoke tests pass

**Steps:**
1. **[PLANNING]** Review roadmap 3.2 for ramp schedule and acceptance criteria
2. **[EXECUTION]** Increase AUTH_NEW_LOGIN to 50%; monitor for 8 hours
3. **[EXECUTION]** Increase AUTH_NEW_LOGIN to 100%; smoke test passes, zero errors for 1 hour
4. **[EXECUTION]** Enable AUTH_TOKEN_REFRESH; verify refresh success rate > 99%
5. **[VERIFICATION]** All three stages stable: 50% for 8h, 100% for 1h, refresh > 99% success
6. **[COMPLETION]** Document ramp results

**Acceptance Criteria:**
- 50% traffic stable for 8 hours (no alerts triggered)
- 100% traffic stable for 1 hour (smoke test passes, zero errors)
- AUTH_TOKEN_REFRESH enabled, POST /auth/refresh success rate > 99%
- All success metrics from PRD S19 tracked during ramp

**Validation:**
- Manual check: Grafana dashboards show stable metrics throughout ramp
- Evidence: `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0041/evidence.md`

**Dependencies:** T03.01 (pentest clear)
**Rollback:** Disable AUTH_NEW_LOGIN → 100% traffic to legacy per roadmap rollback procedure

### T03.03 -- Deprecate Legacy Authentication

| Field | Value |
|---|---|
| Roadmap Item IDs | R-039 |
| Why | Legacy auth system deprecated and removed after GA. Redirect legacy traffic, announce deprecation, remove legacy code. |
| Effort | M |
| Risk | High |
| Risk Drivers | migration, breaking, rollback |
| Tier | STRICT |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0042 |

**Artifacts (Intended Paths):**
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0042/spec.md`

**Deliverables:**
1. Legacy auth deprecated: public announcement, 301 redirect from /v0/auth/login → /v1/auth/login, legacy code removed (code review approved)

**Steps:**
1. **[PLANNING]** Review roadmap 3.3 for deprecation steps and timeline
2. **[EXECUTION]** Announce deprecation: legacy endpoints deprecated after 30 days
3. **[EXECUTION]** Configure 301 redirect from legacy /v0/auth/login → /v1/auth/login
4. **[EXECUTION]** Remove legacy AuthService and related components (code review approved)
5. **[VERIFICATION]** Verify: legacy endpoint returns 301; no remaining code references to legacy auth
6. **[COMPLETION]** Document deprecation and removal

**Acceptance Criteria:**
- Public deprecation announcement issued with 30-day notice
- Legacy endpoints return 301 redirect to new endpoints
- Legacy code fully removed from codebase
- Code review approved for removal

**Validation:**
- Manual check: GET /v0/auth/login → 301 redirect to /v1/auth/login
- Evidence: `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0042/evidence.md`

**Dependencies:** T03.02 (100% traffic on new system)
**Rollback:** Re-enable legacy code and routing (30-day window)

### T03.04 -- Clean Up Feature Flags

| Field | Value |
|---|---|
| Roadmap Item IDs | R-040 |
| Why | Remove AUTH_NEW_LOGIN at GA. Schedule AUTH_TOKEN_REFRESH removal at GA + 2 weeks. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | EXEMPT |
| Confidence | [██████████] 95% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0043 |

**Artifacts (Intended Paths):**
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0043/spec.md`

**Deliverables:**
1. AUTH_NEW_LOGIN flag removed; AUTH_TOKEN_REFRESH removal scheduled for GA + 2 weeks

**Steps:**
1. **[PLANNING]** Review roadmap 3.4 for cleanup schedule
2. **[EXECUTION]** Remove AUTH_NEW_LOGIN flag and all code references
3. **[EXECUTION]** Schedule AUTH_TOKEN_REFRESH removal for GA + 2 weeks
4. **[COMPLETION]** Document flag removal

**Acceptance Criteria:**
- AUTH_NEW_LOGIN fully removed from codebase
- AUTH_TOKEN_REFRESH removal scheduled
- No dead code referencing removed flags
- Tests still pass after flag removal

**Validation:**
- Evidence: `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0043/spec.md`

**Dependencies:** T03.02 (GA traffic ramp complete)
**Rollback:** Re-add flags if needed

### T03.05 -- Validate Runbooks and Establish On-Call Rotation

| Field | Value |
|---|---|
| Roadmap Item IDs | R-041 |
| Why | Operational readiness: validate runbooks via dry-run scenarios, establish 24/7 on-call rotation for first 2 weeks post-GA. Per TDD §25 Operational Readiness. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | end-to-end |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0044, D-0045 |

**Artifacts (Intended Paths):**
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0044/spec.md`
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0045/spec.md`

**Deliverables:**
1. Runbook validation report: dry-run AuthService down, token refresh failures, Redis down — all completed < 15 min
2. On-call rotation schedule: 24/7 for first 2 weeks post-GA, auth-team confirmed, escalation paths clear

**Steps:**
1. **[PLANNING]** Review roadmap 3.5 for runbook scenarios and on-call requirements
2. **[EXECUTION]** Dry-run: AuthService down scenario → runbook executable, completion < 15 min
3. **[EXECUTION]** Dry-run: token refresh failure → runbook executable, completion < 15 min
4. **[EXECUTION]** Dry-run: Redis down → runbook executable, completion < 15 min
5. **[EXECUTION]** Establish on-call rotation: auth-team acknowledged, escalation paths documented
6. **[VERIFICATION]** All 3 runbooks executable in < 15 min; on-call confirmed
7. **[COMPLETION]** File validation report and on-call schedule

**Acceptance Criteria:**
- All 3 runbook dry-runs completed in < 15 minutes each
- On-call rotation confirmed by auth-team for first 2 weeks post-GA
- Escalation paths clear and documented
- Capacity planning verified: pod count, pool sizes, Redis memory handle peak projections

**Validation:**
- Manual check: Runbook completion times documented; on-call schedule published
- Evidence: `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0044/evidence.md`

**Dependencies:** T03.02 (GA active)
**Rollback:** N/A

### Checkpoint: Phase 3 / Tasks 01-05

**Purpose:** Verify security, GA traffic, legacy deprecation, flag cleanup, and operational readiness before success metrics and documentation.
**Checkpoint Report Path:** `.dev/test-fixtures/results/test1-tdd-prd-v2/checkpoints/CP-P03-T01-T05.md`
**Verification:**
- Pentest complete with zero critical/high findings
- 100% traffic on new AuthService for at least 24 hours
- Legacy auth deprecated with 301 redirect active
**Exit Criteria:**
- All security findings remediated
- On-call rotation established
- Feature flag cleanup in progress

### T03.06 -- Establish Success Metrics Baselines

| Field | Value |
|---|---|
| Roadmap Item IDs | R-042 |
| Why | Establish Day 1 baselines for all PRD S19 success metrics: DAU, registration conversion, login p95, service availability, failed login rate, password reset completion, session duration. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | EXEMPT |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0046 |

**Artifacts (Intended Paths):**
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0046/spec.md`

**Deliverables:**
1. Success metrics baseline report: DAU target > 1000 (30 days), registration conversion > 60% (30 days), login p95 < 200ms (sustained), availability 99.9% (30-day rolling), failed login < 5% (14 days), reset completion > 80% (14 days), session > 30 min (7 days)

**Steps:**
1. **[PLANNING]** Review roadmap 3.6 for metric definitions and targets from PRD S19
2. **[EXECUTION]** Record Day 1 baselines from production dashboards for all 7 metrics
3. **[EXECUTION]** Configure dashboards with target overlays for tracking over time
4. **[COMPLETION]** File baseline report

**Acceptance Criteria:**
- All 7 PRD S19 success metrics have recorded Day 1 baselines
- Dashboard target overlays configured for each metric
- Targets match PRD: DAU > 1000, conversion > 60%, p95 < 200ms, 99.9% availability, failed login < 5%, reset > 80%, session > 30 min
- Measurement methods per roadmap (APM, funnel analysis, event logs, Prometheus)

**Validation:**
- Evidence: Baseline report at `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0046/spec.md`

**Dependencies:** T03.02 (GA traffic)
**Rollback:** N/A

### T03.07 -- Publish Documentation and Knowledge Transfer

| Field | Value |
|---|---|
| Roadmap Item IDs | R-043 |
| Why | Operations runbook, API documentation (OpenAPI spec for persona Sam), troubleshooting guide, and architecture decision record for future maintainers. |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0047, D-0048, D-0049, D-0050 |

**Artifacts (Intended Paths):**
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0047/spec.md`
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0048/spec.md`
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0049/spec.md`
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0050/spec.md`

**Deliverables:**
1. Operations runbook for on-call engineers
2. API documentation (OpenAPI spec) for developers and persona Sam (API consumers)
3. Troubleshooting guide for support team
4. Architecture decision record (ADR) for future maintainers

**Steps:**
1. **[PLANNING]** Review roadmap 3.7 for deliverable specifications and audiences
2. **[EXECUTION]** Write operations runbook covering all incident scenarios
3. **[EXECUTION]** Generate OpenAPI spec from API endpoint definitions
4. **[EXECUTION]** Write troubleshooting guide with common issues and solutions
5. **[EXECUTION]** Write ADR documenting key architectural decisions (stateless AuthService, RS256 JWT, bcrypt cost 12, feature flag gating)
6. **[VERIFICATION]** All 4 documents reviewed and published
7. **[COMPLETION]** Knowledge transfer sessions scheduled

**Acceptance Criteria:**
- Operations runbook covers all incident scenarios from T03.05 dry-runs
- OpenAPI spec covers all 8 API endpoints (7 auth + 1 admin audit) — serves persona Sam
- Troubleshooting guide addresses common issues from Phase 2 beta
- ADR documents all key architectural decisions

**Validation:**
- Manual check: All 4 documents exist and have been reviewed by target audiences
- Evidence: Documents at `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0047/` through `D-0050/`

**Dependencies:** T03.05 (runbook validation)
**Rollback:** N/A

### T03.08 -- Execute Post-GA Stabilization

| Field | Value |
|---|---|
| Roadmap Item IDs | R-044 |
| Why | Explicit stabilization period per Opus recommendation. 24/7 on-call, continuous metric validation, AUTH_TOKEN_REFRESH flag removal, post-mortem if incidents occurred, 99.9% uptime validation over 7 consecutive days. |
| Effort | L |
| Risk | Medium |
| Risk Drivers | performance, end-to-end |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0051, D-0052 |

**Artifacts (Intended Paths):**
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0051/spec.md`
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0052/spec.md`

**Deliverables:**
1. Stabilization report: 99.9% uptime over 7 consecutive days (NFR-REL-001), all dashboard and alert thresholds finalized
2. Post-mortem document (if P0/P1 incidents occurred) or "no incidents" confirmation

**Steps:**
1. **[PLANNING]** Review roadmap 3.8 for stabilization requirements
2. **[EXECUTION]** Maintain 24/7 on-call rotation for auth-team
3. **[EXECUTION]** Continuously validate metrics against success criteria from PRD S19
4. **[EXECUTION]** Remove AUTH_TOKEN_REFRESH flag at GA + 2 weeks
5. **[EXECUTION]** Finalize all dashboards and alerting thresholds based on production data
6. **[VERIFICATION]** Validate 99.9% uptime over 7 consecutive days (NFR-REL-001); 48-hour post-GA window: zero P0 incidents
7. **[COMPLETION]** File stabilization report and post-mortem (if applicable)

**Acceptance Criteria:**
- 99.9% uptime over 7 consecutive days confirmed
- AUTH_TOKEN_REFRESH removed at GA + 2 weeks
- Post-mortem filed if any P0/P1 incidents occurred
- All dashboards and alert thresholds finalized for ongoing operations
- 48-hour post-GA window: zero P0 incidents

**Validation:**
- Manual check: Prometheus uptime metric shows 99.9% for 7 consecutive days
- Evidence: Stabilization report at `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0051/spec.md`

**Dependencies:** T03.02 (GA traffic), T03.06 (metrics baselines)
**Rollback:** N/A (monitoring only)

### Checkpoint: End of Phase 3

**Purpose:** Final gate. All roadmap exit criteria met. Project complete.
**Checkpoint Report Path:** `.dev/test-fixtures/results/test1-tdd-prd-v2/checkpoints/CP-P03-END.md`
**Verification:**
- Penetration test complete with no unresolved critical/high findings
- 100% traffic on new AuthService for 7+ days
- 99.9% uptime validated over 7 consecutive days
**Exit Criteria:**
- All Phase 3 exit criteria from roadmap met (10 items)
- Legacy auth fully deprecated and removed
- All documentation published
- Success metrics baselines established
- Zero P0 incidents in 48-hour post-GA window
