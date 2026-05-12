# Phase 5 -- Admin APIs and Observability

**Phase Goal:** Expose operator-facing admin auth endpoints (user lookup, session revocation, unlock) backed by a dedicated AdminAuthEventService and AccountLockManager, then stand up full observability -- health, Prometheus metrics, structured logs, OTel traces, dashboards, SLO rules, synthetic monitors, and alerting runbook -- so the service is operable and measurable before rollout.

**Task Count:** 13 (T05.01 - T05.13)

---

## T05.01 -- API-008 GET /admin/auth/users endpoint

- **Roadmap Item IDs:** R-074
- **Why:** Support desk needs filtered user lookup; must be admin-scoped and audited.
- **Effort:** M
- **Risk:** Medium
- **Risk Drivers:** auth, permissions, rbac
- **Tier:** STRICT
- **Confidence:** [█████████-] 90%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `auth/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0075
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0075/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0075 `backend/src/routes/admin/users.ts` returning paginated UserProfile summary with filters (status, email, created_at range).

**Steps:**
1. **[PLANNING]** Define admin RBAC scope (role=admin JWT claim) and pagination contract.
2. **[PLANNING]** Confirm filter fields with support stakeholders.
3. **[EXECUTION]** Implement repository query + handler with Zod request validation.
4. **[EXECUTION]** Enforce admin scope middleware and emit AuthEvent `ADMIN_USER_QUERY` via AdminAuthEventService.
5. **[VERIFICATION]** Contract test: non-admin -> 403; admin -> 200 with schema.
6. **[COMPLETION]** Update OpenAPI + admin runbook.

**Acceptance Criteria:**
- Non-admin caller receives 403.
- Response schema matches OpenAPI spec and supports pagination cursors.
- Every call emits AuthEvent with actor and filters.
- Query is index-backed; EXPLAIN plan attached to evidence.

**Validation:**
- Manual check: contract + auth tests pass.
- Evidence: linkable artifact produced (pytest log + EXPLAIN output).

**Dependencies:** T01.01, T02.15
**Rollback:** Unregister route.
**Notes:** Response PII minimized (no password hash, token hashes).

---

## T05.02 -- API-009 POST /admin/auth/users/:id/revoke-sessions endpoint

- **Roadmap Item IDs:** R-075
- **Why:** Incident response needs ability to kill active sessions for a user.
- **Effort:** S
- **Risk:** Medium
- **Risk Drivers:** auth, security
- **Tier:** STRICT
- **Confidence:** [█████████-] 95%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `auth/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0076
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0076/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0076 `backend/src/routes/admin/revoke-sessions.ts` invoking TokenManager.revokeFamily for all families of user.

**Steps:**
1. **[PLANNING]** Confirm side-effects: logout everywhere + audit event.
2. **[EXECUTION]** Iterate family IDs for user and call revokeFamily.
3. **[EXECUTION]** Emit `ADMIN_SESSION_REVOKE` AuthEvent with reason parameter.
4. **[VERIFICATION]** Integration test: active refresh tokens become invalid after call.
5. **[COMPLETION]** Update runbook with operator instructions.

**Acceptance Criteria:**
- All active refresh families for user revoked atomically.
- AuthEvent captures admin, target user, and reason.
- Operation is idempotent (second call returns 204).
- Endpoint restricted to admin scope.

**Validation:**
- Manual check: integration test uses real Redis to confirm revocation.
- Evidence: linkable artifact produced (test log).

**Dependencies:** T02.06, T05.04
**Rollback:** Disable route via feature flag `admin.revoke`.
**Notes:** Required by CONFLICT-2-related incident playbook.

---

## T05.03 -- API-010 POST /admin/auth/users/:id/unlock endpoint

- **Roadmap Item IDs:** R-076
- **Why:** Support needs to clear lockouts without waiting 15 min window.
- **Effort:** S
- **Risk:** Medium
- **Risk Drivers:** auth
- **Tier:** STRICT
- **Confidence:** [█████████-] 90%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `auth/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0077
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0077/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0077 `backend/src/routes/admin/unlock.ts` resetting AccountLockManager counters + UserProfile.locked_until.

**Steps:**
1. **[PLANNING]** Decide unlock side effects (reset counter vs. expire lock).
2. **[EXECUTION]** Implement handler calling AccountLockManager.adminUnlock.
3. **[EXECUTION]** Emit `ADMIN_ACCOUNT_UNLOCK` AuthEvent with reason.
4. **[VERIFICATION]** Test that subsequent login succeeds after unlock.
5. **[COMPLETION]** Update runbook with SLA expectations.

**Acceptance Criteria:**
- Unlock clears lock state immediately.
- AuthEvent records admin + reason.
- Only admin scope may invoke.
- Endpoint idempotent for already-unlocked user.

**Validation:**
- Manual check: integration test unlocks account and logs in.
- Evidence: linkable artifact produced (test log).

**Dependencies:** T01.16, T05.05
**Rollback:** Disable via feature flag `admin.unlock`.
**Notes:** Required by FEAT-LOCK runbook.

---

## T05.04 -- COMP-018 AdminAuthEventService

- **Roadmap Item IDs:** R-077
- **Why:** Centralizes admin action auditing to ensure SOC2 traceability.
- **Effort:** M
- **Risk:** Medium
- **Risk Drivers:** compliance, audit
- **Tier:** STRICT
- **Confidence:** [█████████-] 90%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `auth/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0078
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0078/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0078 `backend/src/services/admin/AdminAuthEventService.ts` emitting structured AuthEvents with 12-month retention label.

**Steps:**
1. **[PLANNING]** Confirm schema union with DM-AUDIT.
2. **[EXECUTION]** Implement service methods for each admin action type.
3. **[EXECUTION]** Tag events with `retention=12mo` and `actor_kind=admin`.
4. **[VERIFICATION]** Unit tests cover each admin event shape.
5. **[COMPLETION]** Document SOC2 mapping in audit plan.

**Acceptance Criteria:**
- All admin endpoints (T05.01-T05.03) route through this service.
- Events are queryable by actor and target.
- 12-month retention label applied for OPS-004 archival.
- No PII beyond user id in events.

**Validation:**
- Manual check: unit tests verify service emissions.
- Evidence: linkable artifact produced (jest log).

**Dependencies:** T01.02
**Rollback:** Revert admin endpoints to emit directly into AuditService.
**Notes:** Shared with FR-PROF-002 profile update audits.

---

## T05.05 -- COMP-019 AccountLockManager

- **Roadmap Item IDs:** R-078
- **Why:** Encapsulates lockout state (Redis + UserProfile.locked_until) used by FEAT-LOCK and admin unlock.
- **Effort:** M
- **Risk:** Medium
- **Risk Drivers:** auth, security
- **Tier:** STRICT
- **Confidence:** [████████--] 85%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `auth/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0079
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0079/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0079 `backend/src/services/auth/AccountLockManager.ts` with increment/clear/adminUnlock + 15-min TTL.

**Steps:**
1. **[PLANNING]** Confirm lockout threshold (5 failures / 15 min) per FEAT-LOCK.
2. **[EXECUTION]** Implement Redis-counter increments with sliding TTL.
3. **[EXECUTION]** Provide adminUnlock path clearing counter + locked_until.
4. **[VERIFICATION]** Unit tests cover threshold crossing + reset semantics.
5. **[COMPLETION]** Wire into AuthService login flow (already scaffolded in Phase 1).

**Acceptance Criteria:**
- 5th failed login within 15 min locks account.
- Successful login clears counter.
- adminUnlock resets both Redis counter and DB field.
- All transitions emit AuthEvent.

**Validation:**
- Manual check: unit tests with fakeredis.
- Evidence: linkable artifact produced (jest log).

**Dependencies:** T01.16
**Rollback:** Disable feature flag `auth.lockout.enabled`.
**Notes:** Reused by T05.03 and incident response.

---

### Checkpoint: Phase 5 / Tasks 1-5

- **Purpose:** Confirm all admin auth endpoints and supporting services are complete and audited end-to-end.
- **Verification:**
  - All 5 tasks marked complete with evidence artifacts.
  - Admin endpoints emit `ADMIN_*` AuthEvents with required fields.
  - AccountLockManager unit tests pass and integration harness confirms lock/unlock cycle.
- **Exit Criteria:**
  - No admin action bypasses AdminAuthEventService.
  - RBAC tests (non-admin -> 403) green for all three endpoints.
  - Open questions logged for T05.06 observability stack bring-up.

---

## T05.06 -- API-011 GET /health liveness and readiness

- **Roadmap Item IDs:** R-079
- **Why:** Platform requires health probes for deploy orchestration.
- **Effort:** S
- **Risk:** Low
- **Risk Drivers:** (none matched)
- **Tier:** STANDARD
- **Confidence:** [███████---] 75%
- **Requires Confirmation:** No
- **Critical Path Override:** No
- **Verification Method:** Direct test execution (30s)
- **MCP Required:** (none)
- **MCP Preferred:** Sequential, Context7
- **Fallback Allowed:** Yes
- **Sub-Agent Delegation:** None
- **Deliverable IDs:** D-0080
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0080/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0080 `backend/src/routes/health.ts` exposing liveness + readiness with DB + Redis checks.

**Steps:**
1. **[PLANNING]** Define liveness = process ok; readiness = DB + Redis + email queue ok.
2. **[EXECUTION]** Implement two endpoints returning JSON status + dependency table.
3. **[VERIFICATION]** Integration test verifies readiness fails when DB down.
4. **[COMPLETION]** Update deploy manifest probes.

**Acceptance Criteria:**
- Liveness returns 200 while process up.
- Readiness returns 503 when dependency unavailable.
- Response includes per-dependency status.
- No auth required (probe endpoints).

**Validation:**
- Manual check: integration test simulating dependency failure.
- Evidence: linkable artifact produced (jest log).

**Dependencies:** T01.05, T02.02
**Rollback:** Revert deploy probes to TCP check.
**Notes:** Informs ALERT-* thresholds.

---

## T05.07 -- OBS-001 GET /metrics Prometheus exposition

- **Roadmap Item IDs:** R-080
- **Why:** Required metrics surface for SLOs and alerts.
- **Effort:** M
- **Risk:** Low
- **Risk Drivers:** (none matched)
- **Tier:** STANDARD
- **Confidence:** [███████---] 75%
- **Requires Confirmation:** No
- **Critical Path Override:** No
- **Verification Method:** Direct test execution (30s)
- **MCP Required:** (none)
- **MCP Preferred:** Sequential, Context7
- **Fallback Allowed:** Yes
- **Sub-Agent Delegation:** None
- **Deliverable IDs:** D-0081
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0081/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0081 `backend/src/telemetry/metrics.ts` + `/metrics` endpoint exposing auth + HTTP counters/histograms.

**Steps:**
1. **[PLANNING]** Inventory required metrics (login attempts, success, failures, refresh, latency histograms).
2. **[EXECUTION]** Instrument routes with prom-client counters/histograms.
3. **[EXECUTION]** Expose `/metrics` endpoint guarded by internal network.
4. **[VERIFICATION]** Hit endpoint in test and assert metric names + label cardinality bounded.
5. **[COMPLETION]** Document metric catalog in observability plan.

**Acceptance Criteria:**
- All required SLI metrics present.
- Label cardinality stays below platform limits.
- Endpoint not exposed publicly.
- Histogram buckets align with SLO targets.

**Validation:**
- Manual check: curl /metrics in integration test.
- Evidence: linkable artifact produced (test log).

**Dependencies:** T01.21, T02.13
**Rollback:** Disable /metrics endpoint; keep prom-client internal.
**Notes:** Feeds OBS-005 recording rules.

---

## T05.08 -- OBS-002 pino structured JSON logger

- **Roadmap Item IDs:** R-081
- **Why:** Centralized structured logging baseline for Loki ingestion.
- **Effort:** S
- **Risk:** Low
- **Risk Drivers:** (none matched)
- **Tier:** STANDARD
- **Confidence:** [███████---] 75%
- **Requires Confirmation:** No
- **Critical Path Override:** No
- **Verification Method:** Direct test execution (30s)
- **MCP Required:** (none)
- **MCP Preferred:** Sequential, Context7
- **Fallback Allowed:** Yes
- **Sub-Agent Delegation:** None
- **Deliverable IDs:** D-0082
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0082/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0082 `backend/src/telemetry/logger.ts` pino instance with redaction rules + request id middleware.

**Steps:**
1. **[PLANNING]** Confirm redaction list (password, tokens, cookies).
2. **[EXECUTION]** Configure pino with JSON output, ISO-8601 timestamps, level env.
3. **[EXECUTION]** Add request-id middleware propagating x-request-id.
4. **[VERIFICATION]** Unit test verifies redaction + required fields.
5. **[COMPLETION]** Wire into route handlers.

**Acceptance Criteria:**
- All logs emitted as JSON with required fields.
- No secret appears in log output across fuzz tests.
- Request id flows through downstream service calls.
- Log level configurable via env.

**Validation:**
- Manual check: unit test asserts redacted fields.
- Evidence: linkable artifact produced (jest log).

**Dependencies:** (none)
**Rollback:** Fallback to console.log with warning header.
**Notes:** Required by OBS-003 trace-id injection.

---

## T05.09 -- OBS-003 OpenTelemetry SDK + OTLP exporter

- **Roadmap Item IDs:** R-082
- **Why:** Traces auth flows end-to-end for latency debugging.
- **Effort:** M
- **Risk:** Low
- **Risk Drivers:** (none matched)
- **Tier:** STANDARD
- **Confidence:** [███████---] 75%
- **Requires Confirmation:** No
- **Critical Path Override:** No
- **Verification Method:** Direct test execution (30s)
- **MCP Required:** (none)
- **MCP Preferred:** Sequential, Context7
- **Fallback Allowed:** Yes
- **Sub-Agent Delegation:** None
- **Deliverable IDs:** D-0083
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0083/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0083 `backend/src/telemetry/tracing.ts` initializing OTel SDK + OTLP HTTP exporter to Tempo dev.

**Steps:**
1. **[PLANNING]** Choose auto-instrumentation set (HTTP, pg, ioredis, pino).
2. **[EXECUTION]** Initialize SDK in bootstrap before HTTP server.
3. **[EXECUTION]** Add manual spans around password hash, token mint, rotation.
4. **[VERIFICATION]** Run integration test; confirm spans visible in dev Tempo.
5. **[COMPLETION]** Document span naming conventions.

**Acceptance Criteria:**
- Login flow produces continuous trace across HTTP -> DB -> Redis.
- Trace ids flow into pino logs.
- Sampling policy documented (1.0 dev, 0.1 prod).
- SDK shutdown flushes spans on process exit.

**Validation:**
- Manual check: run smoke test with OTLP collector listening.
- Evidence: linkable artifact produced (tempo query or trace json).

**Dependencies:** T05.08
**Rollback:** Disable exporter via env flag; keep SDK no-op.
**Notes:** Feeds OPS-002 prod Tempo stack.

---

## T05.10 -- OBS-004 Grafana audit-log + auth events dashboard

- **Roadmap Item IDs:** R-083
- **Why:** Single pane of glass for security ops monitoring authentication activity.
- **Effort:** M
- **Risk:** Low
- **Risk Drivers:** (none matched)
- **Tier:** STANDARD
- **Confidence:** [███████---] 75%
- **Requires Confirmation:** No
- **Critical Path Override:** No
- **Verification Method:** Direct test execution (30s)
- **MCP Required:** (none)
- **MCP Preferred:** Sequential, Context7
- **Fallback Allowed:** Yes
- **Sub-Agent Delegation:** None
- **Deliverable IDs:** D-0084
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0084/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0084 `observability/grafana/dashboards/auth-events.json` provisioned dashboard.

**Steps:**
1. **[PLANNING]** Enumerate required panels (login rate, failure rate, lockouts, refresh mint).
2. **[EXECUTION]** Build dashboard JSON and template variables.
3. **[EXECUTION]** Commit dashboard to provisioning folder.
4. **[VERIFICATION]** Load dashboard against dev Prometheus and confirm panels render.
5. **[COMPLETION]** Attach screenshot to evidence.

**Acceptance Criteria:**
- All required panels populated.
- Dashboard imported via GitOps provisioning.
- Links to runbook per alert.
- Version stamped in dashboard JSON.

**Validation:**
- Manual check: dashboard renders in dev Grafana.
- Evidence: linkable artifact produced (screenshot + JSON file path).

**Dependencies:** T05.07
**Rollback:** Delete dashboard JSON; Grafana reload.
**Notes:** Referenced by SUCC-SLO-BOARD.

---

### Checkpoint: Phase 5 / Tasks 6-10

- **Purpose:** Confirm observability baseline (health, metrics, logs, traces, dashboard) is functional.
- **Verification:**
  - /health and /metrics endpoints integration tests pass.
  - Traces flow to dev Tempo; logs appear in dev Loki.
  - Grafana dashboard loads with populated panels.
- **Exit Criteria:**
  - No secret appears in logs, metrics, or traces.
  - Dependency probes reflect accurate health state.
  - Dashboard referenced by runbook draft.

---

## T05.11 -- OBS-005 SLI/SLO Prometheus recording rules

- **Roadmap Item IDs:** R-084
- **Why:** Defines login success, latency, availability SLIs feeding 99.9% SLO.
- **Effort:** M
- **Risk:** Low
- **Risk Drivers:** (none matched)
- **Tier:** STANDARD
- **Confidence:** [███████---] 75%
- **Requires Confirmation:** No
- **Critical Path Override:** No
- **Verification Method:** Direct test execution (30s)
- **MCP Required:** (none)
- **MCP Preferred:** Sequential, Context7
- **Fallback Allowed:** Yes
- **Sub-Agent Delegation:** None
- **Deliverable IDs:** D-0085
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0085/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0085 `observability/prometheus/rules/auth-slo.yaml` recording + alerting rule definitions.

**Steps:**
1. **[PLANNING]** Define SLIs: login_success_rate, p95_login_latency, availability.
2. **[EXECUTION]** Author recording rules for 5m + 30m windows.
3. **[EXECUTION]** Author SLO-burn alert rules (fast + slow window).
4. **[VERIFICATION]** promtool test rules with sample data.
5. **[COMPLETION]** Commit rules + doc referencing SLO targets.

**Acceptance Criteria:**
- Recording rules cover required SLIs.
- promtool test suite passes.
- Burn-rate alerts align with 99.9% SLO.
- Rules imported via GitOps.

**Validation:**
- Manual check: promtool test rules output.
- Evidence: linkable artifact produced (promtool log).

**Dependencies:** T05.07
**Rollback:** Remove rule file from provisioning path.
**Notes:** Required by ALERT-LOGIN-FAIL and ALERT-LATENCY.

---

## T05.12 -- OBS-006 Checkly synthetic monitor suite

- **Roadmap Item IDs:** R-085
- **Why:** Synthetic end-to-end canary for login/register against staging + prod.
- **Effort:** S
- **Risk:** Low
- **Risk Drivers:** (none matched)
- **Tier:** STANDARD
- **Confidence:** [███████---] 75%
- **Requires Confirmation:** No
- **Critical Path Override:** No
- **Verification Method:** Direct test execution (30s)
- **MCP Required:** (none)
- **MCP Preferred:** Sequential, Context7
- **Fallback Allowed:** Yes
- **Sub-Agent Delegation:** None
- **Deliverable IDs:** D-0086
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0086/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0086 `monitors/checkly/auth.check.js` login + register synthetic check set.

**Steps:**
1. **[PLANNING]** Pick regions + cadence (every 5 min from 3 regions).
2. **[EXECUTION]** Author Checkly API checks with canary account.
3. **[EXECUTION]** Wire alert routing to PagerDuty low-severity.
4. **[VERIFICATION]** Dry-run in staging; confirm alerts fire on fault injection.
5. **[COMPLETION]** Document monitor ownership.

**Acceptance Criteria:**
- Monitors active in staging.
- Alerting routed to on-call.
- Canary credentials rotated quarterly via job.
- Monitor code source-controlled.

**Validation:**
- Manual check: Checkly dashboard shows green history after deploy.
- Evidence: linkable artifact produced (Checkly run link or JSON).

**Dependencies:** T05.06
**Rollback:** Disable monitor in Checkly UI.
**Notes:** Production enablement at T06.07.

---

## T05.13 -- OBS-007 docs/runbooks/auth.md alerting runbook

- **Roadmap Item IDs:** R-086
- **Why:** Operational runbook mapping each alert to mitigation, escalation, rollback.
- **Effort:** S
- **Risk:** Low
- **Risk Drivers:** (none matched)
- **Tier:** STANDARD
- **Confidence:** [███████---] 75%
- **Requires Confirmation:** No
- **Critical Path Override:** No
- **Verification Method:** Direct test execution (30s)
- **MCP Required:** (none)
- **MCP Preferred:** Sequential, Context7
- **Fallback Allowed:** Yes
- **Sub-Agent Delegation:** None
- **Deliverable IDs:** D-0087
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0087/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0087 `docs/runbooks/auth.md` including alert matrix, rollback triggers, contacts.

**Steps:**
1. **[PLANNING]** Inventory all alert names from OBS-005 + ALERT-* (Phase 6).
2. **[EXECUTION]** Document detection, triage, mitigation, rollback for each.
3. **[EXECUTION]** Add escalation tree and PagerDuty schedules.
4. **[VERIFICATION]** Runbook review with SRE lead.
5. **[COMPLETION]** Link runbook from dashboard and alert annotations.

**Acceptance Criteria:**
- Every alert maps to an entry.
- Rollback triggers from Phase 6 represented.
- Contacts reviewed and current.
- Document version stamped.

**Validation:**
- Manual check: reviewed and accepted by SRE stakeholder.
- Evidence: linkable artifact produced (doc file + review note).

**Dependencies:** T05.11
**Rollback:** Restore prior revision.
**Notes:** Updated again at T06.18 rollback runbook consolidation.

---

### Checkpoint: End of Phase 5

- **Purpose:** Confirm observability and admin tooling are production-ready and referenced by runbook.
- **Verification:**
  - All 13 tasks marked complete with evidence.
  - SLO recording rules deployed to staging Prometheus.
  - Runbook reviewed; PagerDuty wired to alerts.
- **Exit Criteria:**
  - Admin APIs fully audited and RBAC-tested.
  - Dashboards + alerts verifiable against synthetic checks.
  - Phase 6 rollout prerequisites satisfied.

---
