# Phase 4 -- Non-Functional Requirements and Observability

**Goal:** Instrument the service for latency, availability, and security NFRs; ship the monitoring, alerting, and load-testing rigging that gates GA.

### T04.01 -- APM instrumentation across /auth/* (OPS-001)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-063 |
| Why | Distributed tracing + p95/p99 metrics for every /auth/* route. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | performance, infra |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0019 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0019/spec.md`
- `TASKLIST_ROOT/artifacts/D-0019/evidence.md`

**Deliverables:**
- `src/infra/observability/apm.ts` and per-handler spans

**Steps:**
1. **[PLANNING]** Identify APM SDK + sampling policy
2. **[PLANNING]** Map spans to handler→service→repository
3. **[EXECUTION]** Wire APM middleware
4. **[EXECUTION]** Export latency histograms
5. **[VERIFICATION]** Verify traces show full call chain in staging APM
6. **[COMPLETION]** Append evidence path

**Acceptance Criteria:**
- Spans cover handler→AuthService→TokenManager→repository for /auth/login
- Latency histograms exported per route
- p95/p99 percentiles visible in APM UI
- Evidence file `D-0019/evidence.md` recorded

**Validation:**
- Manual check: APM dashboard shows /auth/login span chain
- Evidence: linkable artifact produced

**Dependencies:** T03.03
**Rollback:** Disable APM SDK
**Notes:** -

### T04.02 -- Health check endpoint (OPS-002)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-064 |
| Why | GET /healthz returns 200 with DB, secrets, and key cache validated. |
| Effort | S |
| Risk | Medium |
| Risk Drivers | infra |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0020 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0020/spec.md`
- `TASKLIST_ROOT/artifacts/D-0020/evidence.md`

**Deliverables:**
- `src/routes/healthz.ts` handler

**Steps:**
1. **[PLANNING]** Read OPS-002 spec
2. **[PLANNING]** Identify components to ping (DB, secrets, key cache)
3. **[EXECUTION]** Implement handler with parallel checks
4. **[EXECUTION]** Bypass rate-limit for /healthz
5. **[VERIFICATION]** Run k6 baseline; assert <50ms p95
6. **[COMPLETION]** Append evidence path

**Acceptance Criteria:**
- DB ping, secrets fetch, and key cache validated in single response
- Response p95 < 50ms (under normal load)
- Bypasses RATE-001
- Evidence file `D-0020/evidence.md` recorded

**Validation:**
- Manual check: curl /healthz returns 200 with subsystem statuses
- Evidence: linkable artifact produced

**Dependencies:** T01.05
**Rollback:** Revert PR
**Notes:** -

### T04.03 -- k6 load test for NFR-AUTH.1 (OPS-004)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-065 |
| Why | Repeatable load profile against staging hitting all 5 endpoints; gates p95<200ms target. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | performance |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0021 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0021/spec.md`
- `TASKLIST_ROOT/artifacts/D-0021/evidence.md`

**Deliverables:**
- `tests/load/k6/auth-load.js` + CI nightly job

**Steps:**
1. **[PLANNING]** Read OPS-004 acceptance criteria
2. **[PLANNING]** Identify baseline traffic shape
3. **[EXECUTION]** Author k6 script for all five /auth endpoints
4. **[EXECUTION]** Wire CI nightly run
5. **[VERIFICATION]** Compare report to baseline
6. **[COMPLETION]** Append evidence path

**Acceptance Criteria:**
- Script `tests/load/k6/auth-load.js` exercises all five endpoints
- CI nightly job runs and produces report
- p95 < 200ms target verified or remediation issue filed
- Evidence file `D-0021/evidence.md` recorded

**Validation:**
- Manual check: latest CI run report attached
- Evidence: linkable artifact produced

**Dependencies:** T04.01
**Rollback:** Disable nightly schedule
**Notes:** -

### T04.04 -- bcrypt cost benchmark (SEC-001)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-066 |
| Why | CI benchmark proving cost=12 hashes within documented timing band. |
| Effort | S |
| Risk | Medium |
| Risk Drivers | security, performance |
| Tier | STRICT |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0022 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0022/spec.md`
- `TASKLIST_ROOT/artifacts/D-0022/evidence.md`

**Deliverables:**
- `tests/security/bcrypt-bench.ts`

**Steps:**
1. **[PLANNING]** Read CRYPTO-003 + SEC-001 spec
2. **[PLANNING]** Identify CI runner CPU baseline
3. **[EXECUTION]** Implement benchmark generating cost=12 hashes
4. **[EXECUTION]** Make timing band env-var configurable
5. **[VERIFICATION]** Run benchmark; assert p95 within 200-350ms
6. **[COMPLETION]** Append evidence path

**Acceptance Criteria:**
- Bench prints actual ms p95 on failure
- Timing band 200-350ms enforced (env-var override allowed)
- SC-3 evidenced via CI artifact
- Evidence file `D-0022/evidence.md` recorded

**Validation:**
- Manual check: CI bench artifact attached
- Evidence: linkable artifact produced

**Dependencies:** T02.01
**Rollback:** Mark bench as informational (skip)
**Notes:** -

### T04.05 -- Checkpoint: M4 NFR Instrumentation Verified

**Purpose:** Verify NFR instrumentation (APM, health, k6, bcrypt bench) is live in staging and gates SC-1/2/3 before release.
**Checkpoint Report Path:** `checkpoints/CP-P04-END.md`

**Verification:**
- APM dashboards show /auth span chain
- /healthz responds in <50ms p95
- k6 nightly produces report; bcrypt bench passes timing band

**Exit Criteria:**
- NFR-AUTH.1 (p95<200ms) measurable in CI
- NFR-AUTH.2 (99.9% availability) instrumented
- NFR-AUTH.3 (bcrypt cost=12) benchmarked
