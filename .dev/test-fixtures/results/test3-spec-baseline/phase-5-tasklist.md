# Phase 5 -- Production Readiness

**Goal**: Deployment pipeline, secrets management, monitoring thresholds, and documentation. Overlaps with Phase 4 for infrastructure setup.

**Tasks**: T05.01 -- T05.15
**Roadmap Items**: R-073 -- R-087
**Deliverables**: D-0073 -- D-0087

---

### T05.01 -- Secrets manager integration

| Field | Value |
|---|---|
| Roadmap Item IDs | R-073 |
| Why | NFR-AUTH-IMPL-2 and RISK-1 require RSA keys, database credentials, and email API keys stored in a secrets manager. |
| Effort | L |
| Risk | High |
| Risk Drivers | crypto, security, encryption |
| Tier | STRICT |
| Confidence | [███████---] 80% |
| Critical Path Override | Yes |
| Verification Method | Integration test + security review |
| Deliverable IDs | D-0073 |

**Deliverables:**
- Secrets manager integration (Vault, AWS SM, or equivalent) for: RSA private key, database credentials, email service API key

**Steps:**
1. [PLANNING] Select secrets manager and define access patterns
2. [EXECUTION] Implement secrets retrieval for all 3 secret types
3. [VERIFICATION] Test secret loading in staging environment

**Acceptance Criteria:**
- RSA private key loaded from secrets manager
- Database credentials loaded from secrets manager
- Email API key loaded from secrets manager
- No secrets in environment variables, config files, or code

**Validation:**
- Manual check: Verify no secrets in deployment artifacts
- Evidence: Secrets integration code and test committed

**Dependencies:** T01.09

---

### T05.02 -- Key rotation on 90-day schedule

| Field | Value |
|---|---|
| Roadmap Item IDs | R-074 |
| Why | RISK-1 mitigation requires key rotation with grace period for seamless transitions. |
| Effort | L |
| Risk | High |
| Risk Drivers | crypto, security |
| Tier | STRICT |
| Confidence | [███████---] 75% |
| Critical Path Override | Yes |
| Verification Method | Integration test |
| Deliverable IDs | D-0074 |

**Deliverables:**
- Key rotation mechanism: 90-day schedule, grace period accepting old key for verification during rotation window

**Steps:**
1. [PLANNING] Design rotation protocol with grace period
2. [EXECUTION] Implement dual-key verification (current + previous) during rotation window
3. [VERIFICATION] Test: rotate key, verify tokens signed with old key still validate during grace period

**Acceptance Criteria:**
- New key pair generated on 90-day schedule
- Grace period: old key accepted for verification during rotation window
- New tokens signed with new key only
- Old tokens validated with old key during grace period

**Validation:**
- Manual check: Simulate key rotation, test old and new tokens
- Evidence: Rotation mechanism and test committed

**Dependencies:** T05.01

---

### T05.03 -- Rotation logging and alerting

| Field | Value |
|---|---|
| Roadmap Item IDs | R-075 |
| Why | RISK-1 requires audit trail for all key access and rotation events for security compliance. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | security |
| Tier | STRICT |
| Confidence | [████████--] 85% |
| Critical Path Override | Yes |
| Verification Method | Log inspection |
| Deliverable IDs | D-0075 |

**Deliverables:**
- Audit logging for all key rotation events; alerting on rotation failures

**Steps:**
1. [PLANNING] Define log format and alert conditions
2. [EXECUTION] Add structured logging for key access, rotation start, rotation complete, rotation failure
3. [VERIFICATION] Trigger rotation, verify log entries and alert on failure

**Acceptance Criteria:**
- All key access events logged with timestamp and actor
- Rotation events logged: start, complete, failure
- Alert fires on rotation failure
- Logs do not contain key material

**Validation:**
- Manual check: Review rotation logs after test rotation
- Evidence: Logging configuration and test committed

**Dependencies:** T05.02

---

### T05.04 -- Login error rate alert (>5% critical)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-076 |
| Why | NFR-AUTH.2 requires rapid detection of credential stuffing or service degradation via error rate monitoring. |
| Effort | S |
| Risk | Low |
| Risk Drivers | security |
| Tier | STANDARD |
| Confidence | [████████--] 88% |
| Critical Path Override | No |
| Verification Method | Alert test |
| Deliverable IDs | D-0076 |

**Deliverables:**
- Alert rule: login error rate > 5% triggers critical alert

**Steps:**
1. [PLANNING] Define error rate calculation and threshold
2. [EXECUTION] Configure alert rule in monitoring system
3. [VERIFICATION] Simulate elevated error rate, verify alert fires

**Acceptance Criteria:**
- Alert fires when login error rate exceeds 5%
- Alert classified as critical
- Alert includes error rate percentage and time window

**Validation:**
- Manual check: Trigger alert with simulated failures
- Evidence: Alert configuration committed

**Dependencies:** T04.21

---

### T05.05 -- API p95 latency alert (>300ms warning)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-077 |
| Why | NFR-AUTH.1 requires early warning before SLA breach when latency degrades. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | — |
| Tier | STANDARD |
| Confidence | [█████████-] 90% |
| Critical Path Override | No |
| Verification Method | Alert test |
| Deliverable IDs | D-0077 |

**Deliverables:**
- Alert rule: API p95 latency > 300ms triggers warning alert

**Steps:**
1. [PLANNING] Define latency threshold and measurement window
2. [EXECUTION] Configure warning alert in monitoring system
3. [VERIFICATION] Simulate latency spike, verify alert fires

**Acceptance Criteria:**
- Alert fires when p95 latency exceeds 300ms
- Alert classified as warning
- Alert includes endpoint and latency values

**Validation:**
- Manual check: Verify alert on latency spike
- Evidence: Alert configuration committed

**Dependencies:** T04.21

---

> **CHECKPOINT 14** (after T05.05): Verify T05.01--T05.05 pass. Secrets manager integration complete. Key rotation mechanism functional. Critical alerts configured.

---

### T05.06 -- Refresh token replay security alert

| Field | Value |
|---|---|
| Roadmap Item IDs | R-078 |
| Why | FR-AUTH.3c and RISK-2 require immediate notification of potential token theft via replay detection. |
| Effort | S |
| Risk | Medium |
| Risk Drivers | token, security |
| Tier | STRICT |
| Confidence | [████████--] 88% |
| Critical Path Override | Yes |
| Verification Method | Alert test |
| Deliverable IDs | D-0078 |

**Deliverables:**
- Security alert: refresh token replay detected triggers immediate notification

**Steps:**
1. [PLANNING] Define alert severity and notification channel
2. [EXECUTION] Wire replay detection event to security alert
3. [VERIFICATION] Simulate replay, verify alert fires immediately

**Acceptance Criteria:**
- Alert fires on any refresh token replay event
- Alert classified as security/critical
- Alert includes user ID and timestamp
- Notification reaches security team within 1 minute

**Validation:**
- Manual check: Trigger replay, verify notification received
- Evidence: Alert configuration and test committed

**Dependencies:** T02.02, T04.21

---

### T05.07 -- Email service failure alert

| Field | Value |
|---|---|
| Roadmap Item IDs | R-079 |
| Why | RISK-4 requires visibility into password reset email delivery failures for operational awareness. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | — |
| Tier | STANDARD |
| Confidence | [████████--] 88% |
| Critical Path Override | No |
| Verification Method | Alert test |
| Deliverable IDs | D-0079 |

**Deliverables:**
- Warning alert on email service dispatch failures

**Steps:**
1. [PLANNING] Define failure detection and alert threshold
2. [EXECUTION] Configure alert on email dispatch errors
3. [VERIFICATION] Simulate email failure, verify warning fires

**Acceptance Criteria:**
- Alert fires on email dispatch failure
- Alert classified as warning
- Includes failure count and time window

**Validation:**
- Manual check: Simulate email service down, verify alert
- Evidence: Alert configuration committed

**Dependencies:** T02.11, T04.21

---

### T05.08 -- Database connection failure alert

| Field | Value |
|---|---|
| Roadmap Item IDs | R-080 |
| Why | NFR-AUTH.2 requires core dependency monitoring; database failure is the highest-impact outage scenario. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | database |
| Tier | STANDARD |
| Confidence | [█████████-] 92% |
| Critical Path Override | No |
| Verification Method | Alert test |
| Deliverable IDs | D-0080 |

**Deliverables:**
- Critical alert on database connection failures

**Steps:**
1. [PLANNING] Define failure detection from health check and connection pool
2. [EXECUTION] Configure critical alert on database connectivity loss
3. [VERIFICATION] Simulate database outage, verify critical alert

**Acceptance Criteria:**
- Alert fires on database connection failure
- Alert classified as critical
- Includes connection pool status

**Validation:**
- Manual check: Simulate database outage, verify alert
- Evidence: Alert configuration committed

**Dependencies:** T04.20, T04.21

---

### T05.09 -- CI pipeline configuration

| Field | Value |
|---|---|
| Roadmap Item IDs | R-081 |
| Why | SC-1 through SC-9 require a CI pipeline running all tests, lint, coverage, and producing build artifacts. |
| Effort | L |
| Risk | Medium |
| Risk Drivers | — |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Critical Path Override | No |
| Verification Method | Pipeline execution |
| Deliverable IDs | D-0081 |

**Deliverables:**
- CI pipeline configuration: lint, unit tests, integration tests, security tests, coverage enforcement (>= 90%), build artifact

**Steps:**
1. [PLANNING] Define pipeline stages and failure conditions
2. [EXECUTION] Configure CI pipeline with all stages
3. [VERIFICATION] Run full pipeline end-to-end

**Acceptance Criteria:**
- Pipeline runs lint, all test suites, and coverage check
- Fails if coverage < 90% line or < 85% branch
- Produces build artifact on success
- Runs in < 15 minutes

**Validation:**
- Manual check: Trigger pipeline, verify all stages pass
- Evidence: CI configuration committed; pipeline green

**Dependencies:** T04.14, T04.15

---

### T05.10 -- Gradual rollout strategy

| Field | Value |
|---|---|
| Roadmap Item IDs | R-082 |
| Why | SC-9 and FR-AUTH.1-IMPL-4 require controlled rollout: flag off, smoke test, 10%, 50%, 100% traffic. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | — |
| Tier | STANDARD |
| Confidence | [████████--] 82% |
| Critical Path Override | No |
| Verification Method | Procedure review |
| Deliverable IDs | D-0082 |

**Deliverables:**
- Rollout procedure: deploy with flag off, smoke test, 10% traffic (1hr monitor), 50% (1hr), 100%

**Steps:**
1. [PLANNING] Define rollout stages and monitoring criteria per SC-9
2. [EXECUTION] Document rollout procedure with decision gates at each stage
3. [VERIFICATION] Peer review of procedure

**Acceptance Criteria:**
- Procedure covers: deploy with flag off, smoke test, 10%, 50%, 100%
- Each stage has monitoring criteria and rollback trigger
- 1-hour monitoring window at 10% and 50%

**Validation:**
- Manual check: Peer review sign-off on procedure
- Evidence: Rollout procedure document committed

**Dependencies:** T02.15

---

> **CHECKPOINT 15** (after T05.10): Verify T05.06--T05.10 pass. All alerts configured and tested. CI pipeline green. Rollout procedure documented.

---

### T05.11 -- Rollback procedure (target < 5 minutes)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-083 |
| Why | SC-9 requires rollback achievable in < 5 minutes via feature flag toggle and redeployment. |
| Effort | S |
| Risk | Low |
| Risk Drivers | — |
| Tier | STANDARD |
| Confidence | [█████████-] 90% |
| Critical Path Override | No |
| Verification Method | Timed drill |
| Deliverable IDs | D-0083 |

**Deliverables:**
- Documented rollback procedure with < 5 minute target; verified via timed drill

**Steps:**
1. [PLANNING] Define rollback steps and timing targets
2. [EXECUTION] Document procedure: set flag to disabled, redeploy
3. [VERIFICATION] Execute timed rollback drill; confirm < 5 minutes

**Acceptance Criteria:**
- Rollback procedure documented step-by-step
- Timed drill completes in < 5 minutes
- Procedure includes verification steps

**Validation:**
- Manual check: Execute timed drill
- Evidence: Procedure and drill results committed

**Dependencies:** T04.19, T05.10

---

### T05.12 -- OpenAPI/Swagger spec for auth endpoints

| Field | Value |
|---|---|
| Roadmap Item IDs | R-084 |
| Why | API documentation with request/response examples and error codes enables consumer integration. |
| Effort | M |
| Risk | Low |
| Risk Drivers | — |
| Tier | EXEMPT |
| Confidence | [█████████-] 93% |
| Critical Path Override | No |
| Verification Method | Schema validation |
| Deliverable IDs | D-0084 |

**Deliverables:**
- OpenAPI 3.0 spec for all /auth/* endpoints with request/response examples and error codes (401, 403, 409, 400, 429)

**Steps:**
1. [PLANNING] Define spec structure covering all 6 endpoints
2. [EXECUTION] Write OpenAPI spec with schemas, examples, and error responses
3. [VERIFICATION] Validate spec with openapi-generator or swagger-cli

**Acceptance Criteria:**
- Covers all 6 auth endpoints
- Includes request body schemas with validation rules
- Includes all error response codes with examples
- Spec validates without errors

**Validation:**
- Manual check: Load spec in Swagger UI
- Evidence: OpenAPI spec file committed

**Dependencies:** T03.05, T03.06, T03.07, T03.08, T03.09, T03.10

---

### T05.13 -- Sequence diagrams for auth flows

| Field | Value |
|---|---|
| Roadmap Item IDs | R-085 |
| Why | Architecture documentation aids onboarding and incident response for login, refresh, reset, and replay flows. |
| Effort | M |
| Risk | Low |
| Risk Drivers | — |
| Tier | EXEMPT |
| Confidence | [█████████-] 95% |
| Critical Path Override | No |
| Verification Method | Document review |
| Deliverable IDs | D-0085 |

**Deliverables:**
- Sequence diagrams for: login flow, token refresh, password reset, replay detection

**Steps:**
1. [PLANNING] Identify actors and interactions for each flow
2. [EXECUTION] Create sequence diagrams (PlantUML or Mermaid)
3. [VERIFICATION] Peer review for accuracy

**Acceptance Criteria:**
- Login flow diagram: client, middleware, AuthService, database
- Token refresh diagram: client, middleware, TokenManager, database
- Password reset diagram: client, AuthService, email service, database
- Replay detection diagram: client, TokenManager, database, alert system

**Validation:**
- Manual check: Peer review confirms accuracy
- Evidence: Diagram files committed

**Dependencies:** None

---

### T05.14 -- Operational runbooks

| Field | Value |
|---|---|
| Roadmap Item IDs | R-086 |
| Why | On-call engineers need documented procedures for deployment, rollback, secret rotation, and alert response. |
| Effort | L |
| Risk | Low |
| Risk Drivers | — |
| Tier | EXEMPT |
| Confidence | [█████████-] 90% |
| Critical Path Override | No |
| Verification Method | Document review |
| Deliverable IDs | D-0086 |

**Deliverables:**
- Runbooks for: deployment, rollback, secret rotation, security alert response, metric investigation

**Steps:**
1. [PLANNING] Define runbook structure and audience
2. [EXECUTION] Write 5 runbooks with step-by-step procedures
3. [VERIFICATION] Peer review by operations team

**Acceptance Criteria:**
- Deployment runbook with pre/post checks
- Rollback runbook (references T04.19 procedure)
- Secret rotation runbook with grace period handling
- Security alert response runbook (replay, key compromise)
- Metric investigation runbook (latency, error rate)

**Validation:**
- Manual check: Operations team review sign-off
- Evidence: All runbook documents committed

**Dependencies:** T04.19, T05.02, T05.11

---

### T05.15 -- Security documentation: threat model and controls mapping

| Field | Value |
|---|---|
| Roadmap Item IDs | R-087 |
| Why | RISK-1 through RISK-6 require documented threat model mapping risks to mitigations and incident response. |
| Effort | L |
| Risk | Low |
| Risk Drivers | security |
| Tier | EXEMPT |
| Confidence | [████████--] 88% |
| Critical Path Override | No |
| Verification Method | Security review |
| Deliverable IDs | D-0087 |

**Deliverables:**
- Security documentation: threat model, controls mapping (risks to mitigations), incident response for key compromise

**Steps:**
1. [PLANNING] Define threat model scope from RISK-1 through RISK-6
2. [EXECUTION] Write threat model, map each risk to controls implemented, document incident response
3. [VERIFICATION] Security review sign-off

**Acceptance Criteria:**
- All 6 risks (RISK-1 through RISK-6) mapped to mitigations
- Controls mapping references specific implementations
- Key compromise incident response procedure documented
- Residual risk documented for each threat

**Validation:**
- Manual check: Security engineer review sign-off
- Evidence: Security documentation committed

**Dependencies:** T05.01, T05.02, T05.03

---

> **END-OF-PHASE CHECKPOINT** (Phase 5 Gate): Secrets configured and rotated. Monitoring dashboards populated. CI/CD pipeline passes end-to-end. Documentation complete and reviewed. All deliverables D-0073 through D-0087 produced and verified. Production deployment approved.
