# Phase 5 -- Hardening, Validation, and Release

**Goal:** Validate every success criterion against staging and production-mirror, complete security and architecture reviews, finalize rollout/rollback runbook, then enable AUTH_SERVICE_ENABLED in production.

### T05.01 -- SC-1..SC-7 validation suite (release gate)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-073 |
| Why | Validate every mechanically-verifiable success criterion against staging before flag flip. |
| Effort | M |
| Risk | High |
| Risk Drivers | security, auth, performance |
| Tier | STRICT |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0023 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0023/spec.md`
- `TASKLIST_ROOT/artifacts/D-0023/evidence.md`

**Deliverables:**
- `tests/release/sc-1-7-validation.md` evidence pack

**Steps:**
1. **[PLANNING]** Identify each SC's owner
2. **[PLANNING]** Confirm artifact attachment requirements
3. **[EXECUTION]** Run k6 + bench + integration suites
4. **[EXECUTION]** Collect signed-off evidence per SC
5. **[VERIFICATION]** Cross-check against release ticket
6. **[COMPLETION]** Append evidence path

**Acceptance Criteria:**
- All SC-1..SC-7 evidence attached to release ticket
- Each SC signed off by named owner
- Replay event observed in AUDIT-001 sink (SC-7 evidence)
- Evidence file `D-0023/evidence.md` recorded

**Validation:**
- Manual check: release ticket has 7 evidence attachments
- Evidence: linkable artifact produced

**Dependencies:** T04.05
**Rollback:** N/A (validation, not implementation)
**Notes:** -

### T05.02 -- Penetration smoke test (SEC-003)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-074 |
| Why | Targeted pentest of /auth/* covering enumeration, brute force, replay, JWT attacks. |
| Effort | M |
| Risk | High |
| Risk Drivers | security, vulnerability |
| Tier | STRICT |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0024 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0024/spec.md`
- `TASKLIST_ROOT/artifacts/D-0024/evidence.md`

**Deliverables:**
- `tests/security/pentest-report.md`

**Steps:**
1. **[PLANNING]** Identify attack matrix (enumeration, brute, replay, JWT)
2. **[PLANNING]** Confirm test environment isolation
3. **[EXECUTION]** Run pentest scripts
4. **[EXECUTION]** Triage findings into severity buckets
5. **[VERIFICATION]** Confirm zero critical findings
6. **[COMPLETION]** Append evidence path

**Acceptance Criteria:**
- Pentest report file `tests/security/pentest-report.md` exists with findings
- Critical findings = 0 (release blocker if any)
- Each finding has remediation assignee or accepted-risk note
- Evidence file `D-0024/evidence.md` recorded

**Validation:**
- Manual check: report attached to release ticket
- Evidence: linkable artifact produced

**Dependencies:** T05.01
**Rollback:** N/A
**Notes:** -

### T05.03 -- Feature flag rollout plan (FF-001)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-075 |
| Why | Staged rollout (canary→25%→100%) with kill-switch verified. |
| Effort | S |
| Risk | Medium |
| Risk Drivers | infra, deploy |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0025 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0025/spec.md`
- `TASKLIST_ROOT/artifacts/D-0025/evidence.md`

**Deliverables:**
- `docs/release/ff-001-rollout.md`

**Steps:**
1. **[PLANNING]** Identify rollout stages
2. **[PLANNING]** Identify on-call briefing artifacts
3. **[EXECUTION]** Author rollout doc
4. **[EXECUTION]** Rehearse kill-switch in staging
5. **[VERIFICATION]** Confirm doc approval signatures
6. **[COMPLETION]** Append evidence path

**Acceptance Criteria:**
- Doc `docs/release/ff-001-rollout.md` exists with three rollout stages
- Kill-switch rehearsal recorded
- On-call briefed (sign-off captured)
- Evidence file `D-0025/evidence.md` recorded

**Validation:**
- Manual check: rollout doc approved in PR
- Evidence: linkable artifact produced

**Dependencies:** T05.01
**Rollback:** N/A (planning artifact)
**Notes:** -

### T05.04 -- Rollback procedure rehearsal (OPS-006)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-076 |
| Why | Live drill of CFG-002=false plus migration rollback in staging. |
| Effort | M |
| Risk | High |
| Risk Drivers | migration, rollback, infra |
| Tier | STRICT |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0026 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0026/spec.md`
- `TASKLIST_ROOT/artifacts/D-0026/evidence.md`

**Deliverables:**
- `tests/release/rollback-rehearsal.md`

**Steps:**
1. **[PLANNING]** Confirm staging environment mirrors prod
2. **[PLANNING]** Confirm rollback runbook draft
3. **[EXECUTION]** Flip CFG-002 to false; observe routes disappear
4. **[EXECUTION]** Apply MIG-003 down scripts; verify schema reverts
5. **[VERIFICATION]** Measure mean rollback time
6. **[COMPLETION]** Append evidence path

**Acceptance Criteria:**
- Rehearsal report recorded with mean rollback time
- CFG-002 flag-flip rollback completes without restart
- MIG-003 down completes cleanly with no data loss
- Evidence file `D-0026/evidence.md` recorded

**Validation:**
- Manual check: rehearsal report attached
- Evidence: linkable artifact produced

**Dependencies:** T05.03, T01.01
**Rollback:** N/A (rehearsal IS the rollback)
**Notes:** Critical path override (migration rollback).

### T05.05 -- Checkpoint: M5 Release Gate Verified

**Purpose:** Verify all SC-1..SC-8 are green and rollback rehearsal recorded before flipping CFG-002 in production.
**Checkpoint Report Path:** `checkpoints/CP-P05-END.md`

**Verification:**
- SC-1..SC-7 evidence attached
- Pentest report has zero criticals
- Rollback rehearsal recorded with mean time

**Exit Criteria:**
- Security review sign-off filed
- Feature flag rollout plan approved
- On-call briefed and acknowledged
