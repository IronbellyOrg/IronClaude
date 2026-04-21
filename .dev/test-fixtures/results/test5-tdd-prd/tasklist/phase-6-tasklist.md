# Phase 6 -- Production Readiness and Rollout

**Phase Goal:** Migrate legacy_users to UserProfile, retire legacy auth, gate new login/refresh behind feature flags, stand up production observability stack (Prometheus/Tempo/Loki/SMTP), wire SLO + auto-rollback automation, and clear OPS-011 GA go/no-go gate to reach 99.9% SLO availability.

**Task Count:** 21 (T06.01 - T06.21)

---

## T06.01 -- MIG-001 legacy_users -> UserProfile migration script

- **Roadmap Item IDs:** R-087
- **Why:** Data migration is single-shot, irreversible path to new schema and bcrypt hashes.
- **Effort:** L
- **Risk:** High
- **Risk Drivers:** migration, data, schema, rollback
- **Tier:** STRICT
- **Confidence:** [█████████-] 95%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `migrations/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0088
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0088/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0088 `backend/migrations/mig-001-legacy-to-userprofile.ts` idempotent batch migration with progress + checksum reporting.

**Steps:**
1. **[PLANNING]** Confirm source/target column mapping and bcrypt upgrade policy (re-hash on first login).
2. **[PLANNING]** Define batch size (1000 rows) and resume token.
3. **[EXECUTION]** Implement read-only dry-run mode.
4. **[EXECUTION]** Implement commit mode with per-batch transaction + progress log.
5. **[EXECUTION]** Emit `MIG_BATCH_COMPLETE` AuthEvent with counts and checksum.
6. **[VERIFICATION]** Run against staging dump; compare row counts and spot-check 100 records.
7. **[VERIFICATION]** Execute sub-agent verification with quality-engineer.
8. **[COMPLETION]** Publish migration report.

**Acceptance Criteria:**
- Dry-run reports exact row counts and mismatches.
- Commit mode resumes from last token on retry.
- All rows land with consent_flag captured (null where unknown + audit).
- No password plaintext persisted; legacy hash carried as opaque blob for rehash.

**Validation:**
- Manual check: staging run with dump; row count parity verified.
- Evidence: linkable artifact produced (migration report + checksum file).

**Dependencies:** T01.01, T01.02
**Rollback:** Restore database snapshot taken pre-migration.
**Notes:** OPS-004 archival must be online before commit mode runs.

---

## T06.02 -- MIG-002 parallel-run reconciliation + mismatch table

- **Roadmap Item IDs:** R-088
- **Why:** Detect divergence between legacy_users and UserProfile during cut-over.
- **Effort:** M
- **Risk:** High
- **Risk Drivers:** data, migration
- **Tier:** STRICT
- **Confidence:** [█████████-] 90%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `migrations/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0089
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0089/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0089 `backend/jobs/mig-002-reconcile.ts` scheduled reconciliation writing to `auth_migration_mismatch` table.

**Steps:**
1. **[PLANNING]** Define comparison columns and tolerances.
2. **[EXECUTION]** Implement job diffing legacy vs. new tables.
3. **[EXECUTION]** Create mismatch schema + indexes.
4. **[EXECUTION]** Expose Grafana panel with open mismatch count.
5. **[VERIFICATION]** Inject synthetic drift and confirm detection.
6. **[COMPLETION]** Document triage procedure.

**Acceptance Criteria:**
- Job completes within 30 min for full dataset.
- Mismatches persisted with reason codes.
- Panel shows trend and breakdown by reason.
- Alert routes to data-eng on backlog > threshold.

**Validation:**
- Manual check: synthetic drift test reports mismatches.
- Evidence: linkable artifact produced (job log + panel screenshot).

**Dependencies:** T06.01
**Rollback:** Disable scheduled job; preserve mismatch table read-only.
**Notes:** Must be clean before MIG-003.

---

## T06.03 -- MIG-003 legacy auth retirement 410 Gone

- **Roadmap Item IDs:** R-089
- **Why:** Closes migration by returning 410 Gone on legacy endpoints after cut-over.
- **Effort:** S
- **Risk:** Medium
- **Risk Drivers:** breaking, migration
- **Tier:** STRICT
- **Confidence:** [████████--] 85%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `auth/`, `migrations/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0090
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0090/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0090 `backend/src/legacy/retire.ts` returning 410 with migration pointer body on `/v0/auth/*`.

**Steps:**
1. **[PLANNING]** Verify traffic to legacy endpoints is 0 for 48h.
2. **[EXECUTION]** Replace legacy handlers with 410 Gone response.
3. **[EXECUTION]** Emit AuthEvent `LEGACY_AUTH_CALL` with source IP for audit.
4. **[VERIFICATION]** Contract test: GET/POST legacy -> 410.
5. **[COMPLETION]** Update API gateway docs.

**Acceptance Criteria:**
- All legacy paths return 410 with JSON pointer.
- No data-path code remains behind 410 branch.
- AuthEvent captures any continued calls.
- Change gated behind FEAT-FLAG-NEWLOGIN at 100%.

**Validation:**
- Manual check: contract tests; gateway logs verified.
- Evidence: linkable artifact produced (test log + gateway snippet).

**Dependencies:** T06.01, T06.02, T06.04
**Rollback:** Revert retire module to legacy handlers (code only; data already migrated).
**Notes:** Hard cut-over requires approval from OPS-011 gate.

---

## T06.04 -- FEAT-FLAG-NEWLOGIN phased rollout segment

- **Roadmap Item IDs:** R-090
- **Why:** Controls gradual rollout of new login flow (0% -> 1% -> 5% -> 25% -> 50% -> 100%) with SLO-green >=60min + error-rate delta <0.5% advancement criteria.
- **Effort:** M
- **Risk:** High
- **Risk Drivers:** rollout, auth
- **Tier:** STRICT
- **Confidence:** [█████████-] 90%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `auth/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0091
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0091/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0091 feature flag segment `auth.newlogin` + rollout plan document + dashboard filter.

**Steps:**
1. **[PLANNING]** Define segment criteria (tenant + random bucket) with LaunchDarkly/Unleash.
2. **[EXECUTION]** Implement segment registration + percentage increments.
3. **[EXECUTION]** Wire flag into AuthService login path.
4. **[VERIFICATION]** Simulate each rollout step in staging.
5. **[COMPLETION]** Capture rollout log with timestamps + approvers.

**Acceptance Criteria:**
- Flag controls 100% of new login traffic across 0%->1%->5%->25%->50%->100% stages.
- Each stage advances only after SLO-green >=60min and error-rate delta <0.5% vs prior stage.
- Rollback returns legacy path on flag off within 60s; rollout steps logged with approver.
- Flag respects auto-rollback triggers.

**Validation:**
- Manual check: staged rollout verification run.
- Evidence: linkable artifact produced (flag history export).

**Dependencies:** T01.10
**Rollback:** Set flag to 0%; legacy endpoints remain live until T06.03.
**Notes:** Tied to ROLLBACK-AUTO-* triggers.

---

## T06.05 -- FEAT-FLAG-REFRESH phased rollout segment

- **Roadmap Item IDs:** R-091
- **Why:** Separate flag for refresh-token flow to allow independent rollback of token rotation.
- **Effort:** M
- **Risk:** Medium
- **Risk Drivers:** rollout, auth
- **Tier:** STRICT
- **Confidence:** [█████████-] 90%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `auth/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0092
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0092/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0092 feature flag segment `auth.refresh` + rollout document.

**Steps:**
1. **[PLANNING]** Confirm dependency on FEAT-FLAG-NEWLOGIN ordering.
2. **[EXECUTION]** Register segment and wire into TokenManager refresh path.
3. **[EXECUTION]** Add guard so flag-off falls back to session cookie behavior.
4. **[VERIFICATION]** Staging rollout to 10% tenant segment with canary.
5. **[COMPLETION]** Record decision log.

**Acceptance Criteria:**
- Flag controls 100% of refresh traffic.
- Flag off rejects refresh calls gracefully (401 with guidance).
- Rollback independent of FEAT-FLAG-NEWLOGIN.
- Auto-rollback triggers honored.

**Validation:**
- Manual check: canary tenant verifies flag on/off behavior.
- Evidence: linkable artifact produced (flag history + synthetic monitor).

**Dependencies:** T02.08, T06.04
**Rollback:** Set flag to 0%; refresh path returns 401.
**Notes:** Required for ROLLBACK-AUTO-REDIS read-only mode.

---

### Checkpoint: Phase 6 / Tasks 1-5

- **Purpose:** Confirm migration and feature-flag segmentation are production-ready.
- **Verification:**
  - MIG-001/002 execute successfully against staging snapshot.
  - MIG-003 cut-over plan approved and gated by flags.
  - Feature flag segments active with rollout/rollback tested.
- **Exit Criteria:**
  - Reconciliation backlog = 0 on staging.
  - Rollback paths verified (<=60s flag flip).
  - All admin approvals captured.

---

## T06.06 -- OPS-001 production Prometheus + Grafana stack

- **Roadmap Item IDs:** R-092
- **Why:** Required production telemetry backbone for SLO observability.
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
- **Deliverable IDs:** D-0093
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0093/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0093 `infra/prod/observability/prometheus-grafana/` Helm + values manifest for prod stack.

**Steps:**
1. **[PLANNING]** Size Prometheus retention (30 days metrics per OPS-001, remote_write for long-term).
2. **[EXECUTION]** Deploy Prometheus + Grafana + alertmanager via Helm.
3. **[EXECUTION]** Apply OBS-005 recording rules and dashboards.
4. **[VERIFICATION]** Confirm scrape of /metrics from prod pods.
5. **[COMPLETION]** Document DNS + access URLs.

**Acceptance Criteria:**
- Prometheus scrapes all auth-service targets.
- Grafana auth via SSO.
- Alertmanager routes to PagerDuty.
- Disaster-recovery snapshot schedule configured.

**Validation:**
- Manual check: prod dashboard loads live metrics.
- Evidence: linkable artifact produced (screenshot + manifest diff).

**Dependencies:** T05.07, T05.10
**Rollback:** Helm rollback to previous values.
**Notes:** Remote-write target defined in OPS-004.

---

## T06.07 -- OPS-002 production Tempo trace backend

- **Roadmap Item IDs:** R-093
- **Why:** Production tracing sink for OTLP exporter (OBS-003).
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
- **Deliverable IDs:** D-0094
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0094/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0094 `infra/prod/observability/tempo/` Helm install + retention config.

**Steps:**
1. **[PLANNING]** Size storage (7 days retention per OPS-002) and ingest rate; configure sampling rules (10% default + 100% 5xx + 100% refresh-replay).
2. **[EXECUTION]** Deploy Tempo with S3 backend.
3. **[EXECUTION]** Wire OTLP HTTP ingress.
4. **[VERIFICATION]** Submit test span from staging and query by trace id.
5. **[COMPLETION]** Link Grafana datasource.

**Acceptance Criteria:**
- Tempo ingests OTLP at expected rate.
- Traces queryable in Grafana Explore.
- Retention policy aligned with SLO review window.
- Datasource configured with auth.

**Validation:**
- Manual check: query staging trace in prod Tempo.
- Evidence: linkable artifact produced (Grafana trace screenshot).

**Dependencies:** T05.09, T06.06
**Rollback:** Helm rollback; OTLP endpoint reverts to dev.
**Notes:** Required before enabling production sampling 0.1.

---

## T06.08 -- OPS-003 production Loki log aggregation

- **Roadmap Item IDs:** R-094
- **Why:** Ingests pino logs for audit retrieval + alert context.
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
- **Deliverable IDs:** D-0095
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0095/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0095 `infra/prod/observability/loki/` Helm install + retention.

**Steps:**
1. **[PLANNING]** Determine retention (14 days hot + 90 days cold per OPS-003, 12 months archive via OPS-004).
2. **[EXECUTION]** Deploy Loki with object storage backend.
3. **[EXECUTION]** Configure promtail/agents scraping prod pods.
4. **[VERIFICATION]** Confirm log search returns structured fields.
5. **[COMPLETION]** Document query cheatsheet.

**Acceptance Criteria:**
- Logs ingested with 2m p95 latency.
- Labels minimized to bounded cardinality.
- Retention configured.
- PII redaction audited via sample logs.

**Validation:**
- Manual check: LogQL query returns auth events.
- Evidence: linkable artifact produced (query log).

**Dependencies:** T05.08, T06.06
**Rollback:** Helm rollback; agents send to dev Loki.
**Notes:** Feeds OPS-004 archival manifest.

---

## T06.09 -- OPS-004 12-month audit archival job + manifest

- **Roadmap Item IDs:** R-095
- **Why:** Satisfies SOC2 12-month retention (CONFLICT-1 resolved at 12 months).
- **Effort:** M
- **Risk:** Medium
- **Risk Drivers:** compliance, audit, data
- **Tier:** STRICT
- **Confidence:** [█████████-] 90%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `auth/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0096
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0096/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0096 `backend/jobs/audit-archive.ts` + `infra/prod/observability/archival/` bucket manifest + legal hold config.

**Steps:**
1. **[PLANNING]** Confirm CONFLICT-1 decision (12 months hot, legal hold override).
2. **[EXECUTION]** Implement archival job rotating audit logs to object storage monthly.
3. **[EXECUTION]** Apply object-lock + immutability policy for 12 months.
4. **[EXECUTION]** Emit manifest (`auth_audit_manifest.json`) signed with KMS.
5. **[VERIFICATION]** Inject test event; verify appears in archive after rotation.
6. **[COMPLETION]** Document legal hold exception workflow.

**Acceptance Criteria:**
- All audit log entries survive 12 months minimum.
- Manifest signature verifiable.
- Legal hold process documented and tested.
- No mutation of archived objects possible.

**Validation:**
- Manual check: archival job dry-run + integrity verification.
- Evidence: linkable artifact produced (manifest + verify log).

**Dependencies:** T01.02, T06.08
**Rollback:** Fallback to manual export (keeps data but breaks SLA); ticket to refit.
**Notes:** Gate for MIG-001 cut-over.

---

## T06.10 -- OPS-005 production SMTP + DKIM/SPF/DMARC

- **Roadmap Item IDs:** R-096
- **Why:** Password-reset emails require authenticated SMTP stack to prevent spoofing and land in inboxes.
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
- **Deliverable IDs:** D-0097
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0097/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0097 `infra/prod/email/` DKIM/SPF/DMARC records + SMTP provider credentials (stored in secret manager).

**Steps:**
1. **[PLANNING]** Choose sender domain + envelope policies.
2. **[EXECUTION]** Configure DKIM + SPF + DMARC records via DNS.
3. **[EXECUTION]** Provision SMTP credentials in secret manager.
4. **[VERIFICATION]** Send test email from production BullMQ worker and verify headers.
5. **[COMPLETION]** Update runbook.

**Acceptance Criteria:**
- DMARC set to `p=reject` after monitoring period; complaint rate <0.1% verified via provider telemetry.
- SPF/DKIM pass mail-tester inspection.
- Secrets rotated quarterly per policy.
- Queue logs capture provider message id.

**Validation:**
- Manual check: mail-tester score >= 9/10.
- Evidence: linkable artifact produced (score screenshot + DNS audit).

**Dependencies:** T03.07
**Rollback:** Switch provider to backup SMTP; update DNS to staging config.
**Notes:** Passwords never emailed; only reset links.

---

### Checkpoint: Phase 6 / Tasks 6-10

- **Purpose:** Confirm production observability + email infrastructure are live and verified.
- **Verification:**
  - Prometheus, Tempo, Loki scraping + ingesting prod signals.
  - OPS-004 archival job completes dry-run with signed manifest.
  - DMARC policy enforced; password-reset email landing in inboxes.
- **Exit Criteria:**
  - SRE lead sign-off on stack.
  - Archival integrity test passes.
  - SMTP deliverability >= 99% in canary.

---

## T06.11 -- ALERT-LOGIN-FAIL Prometheus alert rule

- **Roadmap Item IDs:** R-097
- **Why:** Detects sustained login failure rate anomalies.
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
- **Deliverable IDs:** D-0098
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0098/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0098 `observability/prometheus/rules/alert-login-fail.yaml` alerting rule firing on login failure rate >30% sustained 10min.

**Steps:**
1. **[PLANNING]** Confirm threshold (failure rate >30% sustained 10min per ALERT-LOGIN-FAIL).
2. **[EXECUTION]** Author rule + annotations with runbook link.
3. **[VERIFICATION]** promtool test with synthetic data.
4. **[COMPLETION]** Commit and deploy via GitOps.

**Acceptance Criteria:**
- Alert fires when login failure rate >30% sustained 10min.
- Annotations include runbook URL + severity.
- Labels support routing to on-call.
- Version-controlled.

**Validation:**
- Manual check: promtool pass.
- Evidence: linkable artifact produced (test output).

**Dependencies:** T05.11
**Rollback:** Remove rule via GitOps revert.
**Notes:** Linked from OBS-007 runbook.

---

## T06.12 -- ALERT-LATENCY login p95 latency alert

- **Roadmap Item IDs:** R-098
- **Why:** Detects latency regressions against SLO target (p95 < 300ms).
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
- **Deliverable IDs:** D-0099
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0099/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0099 `observability/prometheus/rules/alert-latency.yaml` rule for p95 breach sustained 10m.

**Steps:**
1. **[PLANNING]** Align threshold with NFR-PERF-001.
2. **[EXECUTION]** Author rule referencing histogram_quantile.
3. **[VERIFICATION]** promtool test.
4. **[COMPLETION]** Commit via GitOps.

**Acceptance Criteria:**
- Alert fires at p95 > 300ms for 10m.
- Linked to runbook entry.
- Severity = high.
- Version-controlled.

**Validation:**
- Manual check: promtool pass.
- Evidence: linkable artifact produced (test output).

**Dependencies:** T05.11
**Rollback:** Revert rule.
**Notes:** Feeds ROLLBACK-AUTO-LATENCY input.

---

## T06.13 -- ALERT-REDIS Redis unavailable alert

- **Roadmap Item IDs:** R-099
- **Why:** Refresh tokens depend on Redis; detection required for rollback automation.
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
- **Deliverable IDs:** D-0100
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0100/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0100 `observability/prometheus/rules/alert-redis.yaml` covering redis_up == 0 for >1min.

**Steps:**
1. **[PLANNING]** Confirm scrape target and timeout.
2. **[EXECUTION]** Author rule + critical severity label.
3. **[VERIFICATION]** promtool test.
4. **[COMPLETION]** Commit.

**Acceptance Criteria:**
- Alert fires on Redis scrape failure >1min.
- Annotations reference rollback runbook.
- Paging severity set to P1.
- Version-controlled.

**Validation:**
- Manual check: promtool pass.
- Evidence: linkable artifact produced (test output).

**Dependencies:** T05.11
**Rollback:** Revert rule.
**Notes:** Input to ROLLBACK-AUTO-REDIS.

---

## T06.14 -- ROLLBACK-AUTO-LATENCY automated latency trigger

- **Roadmap Item IDs:** R-100
- **Why:** Auto-flip FEAT-FLAG-NEWLOGIN to 0% on sustained latency breach (trigger 1 of 4).
- **Effort:** M
- **Risk:** High
- **Risk Drivers:** rollback, performance, auth
- **Tier:** STRICT
- **Confidence:** [█████████-] 90%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `auth/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0101
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0101/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0101 `ops/rollback/auto-latency.yaml` alertmanager -> rollback-actor integration + chaos-test harness.

**Steps:**
1. **[PLANNING]** Define trigger condition (p95 >500ms for 15min per ROLLBACK-AUTO-LATENCY).
2. **[EXECUTION]** Implement webhook receiver that flips FEAT-FLAG-NEWLOGIN to 0%.
3. **[EXECUTION]** Add per-action audit event + Slack/PagerDuty notice.
4. **[VERIFICATION]** Execute chaos drill injecting latency and verify flag flip <= 60s.
5. **[COMPLETION]** Capture drill report.

**Acceptance Criteria:**
- Drill passes with rollback < 60s.
- Manual override path documented.
- Audit event captured with cause.
- Trigger requires two consecutive alert firings to avoid flapping.

**Validation:**
- Manual check: drill report reviewed.
- Evidence: linkable artifact produced (chaos test log).

**Dependencies:** T06.04, T06.12
**Rollback:** Disable webhook; manual rollback via runbook.
**Notes:** Trigger 1 of 4.

---

## T06.15 -- ROLLBACK-AUTO-ERR automated error-rate trigger

- **Roadmap Item IDs:** R-101
- **Why:** Auto-rollback on 5xx surge >1% for 10min (trigger 2 of 4).
- **Effort:** M
- **Risk:** High
- **Risk Drivers:** rollback, auth
- **Tier:** STRICT
- **Confidence:** [█████████-] 90%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `auth/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0102
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0102/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0102 `ops/rollback/auto-err.yaml` alertmanager rule + chaos-test harness.

**Steps:**
1. **[PLANNING]** Confirm 5xx + timeout error thresholds.
2. **[EXECUTION]** Add recording rule + webhook to rollback actor.
3. **[VERIFICATION]** Chaos drill injecting 5xx verifies flag flip.
4. **[COMPLETION]** Drill report archived.

**Acceptance Criteria:**
- Error-rate threshold (>1% sustained 10min) triggers rollback.
- Rollback completes < 60s.
- Post-rollback dashboard highlights incident.
- Manual override documented.

**Validation:**
- Manual check: drill report reviewed.
- Evidence: linkable artifact produced (chaos log).

**Dependencies:** T06.04, T05.11
**Rollback:** Disable webhook; rely on manual rollback.
**Notes:** Trigger 2 of 4.

---

### Checkpoint: Phase 6 / Tasks 11-15

- **Purpose:** Confirm alerting and first two rollback triggers are production-verified.
- **Verification:**
  - All three ALERT-* rules deployed and tested.
  - Two auto-rollback triggers pass chaos drills.
  - Manual override procedure validated in runbook.
- **Exit Criteria:**
  - promtool tests all green.
  - Chaos drill reports archived.
  - Runbook updated with drill links.

---

## T06.16 -- ROLLBACK-AUTO-REDIS Redis-down read-only mode

- **Roadmap Item IDs:** R-102
- **Why:** Degrade gracefully when Redis unreachable >3min (trigger 3 of 4) by blocking refresh + logins while allowing admin.
- **Effort:** M
- **Risk:** High
- **Risk Drivers:** rollback, auth
- **Tier:** STRICT
- **Confidence:** [█████████-] 90%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `auth/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0103
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0103/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0103 `ops/rollback/auto-redis.yaml` + `backend/src/middleware/read-only.ts` read-only mode gate.

**Steps:**
1. **[PLANNING]** Confirm read-only semantics (allow GET, block mint, allow admin unlock).
2. **[EXECUTION]** Implement middleware tied to ALERT-REDIS via config reload.
3. **[EXECUTION]** Wire webhook to flip FEAT-FLAG-REFRESH off + enable middleware.
4. **[VERIFICATION]** Chaos drill blocks Redis; verify behavior and time-to-rollback.
5. **[COMPLETION]** Update runbook with operator steps.

**Acceptance Criteria:**
- Read-only mode active within 60s once Redis unreachable >3min.
- Admin endpoints remain operational.
- State is fully reversible on Redis recovery.
- Drill captures user impact metrics.

**Validation:**
- Manual check: chaos drill log.
- Evidence: linkable artifact produced (drill log).

**Dependencies:** T02.03, T06.05, T06.13
**Rollback:** Disable middleware + webhook; restore flag state.
**Notes:** Trigger 3 of 4.

---

## T06.17 -- ROLLBACK-AUTO-DATA DB write-error rollback

- **Roadmap Item IDs:** R-103
- **Why:** Rolls back on DB write error rate >5% sustained 5 minutes (trigger 4 of 4).
- **Effort:** M
- **Risk:** High
- **Risk Drivers:** rollback, data
- **Tier:** STRICT
- **Confidence:** [█████████-] 90%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `auth/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0104
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0104/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0104 `ops/rollback/auto-data.yaml` alert + rollback webhook + data integrity check script.

**Steps:**
1. **[PLANNING]** Confirm write-error classification (timeouts, unique violations, connection pool exhaustion).
2. **[EXECUTION]** Author recording rule + alertmanager route.
3. **[EXECUTION]** Wire rollback actor to set FEAT-FLAG-NEWLOGIN + FEAT-FLAG-REFRESH to 0%.
4. **[VERIFICATION]** Chaos drill saturating DB writes; observe rollback + recovery.
5. **[COMPLETION]** Update runbook with data-integrity check.

**Acceptance Criteria:**
- Rollback completes < 60s.
- Data integrity report auto-generated post-incident.
- False-positive rate tracked.
- Runbook cross-links MIG-002 reconciliation job.

**Validation:**
- Manual check: chaos drill log.
- Evidence: linkable artifact produced (drill log + integrity report).

**Dependencies:** T06.04, T06.05, T06.14
**Rollback:** Disable webhook; run manual integrity check and rollback.
**Notes:** Trigger 4 of 4; completes ROLLBACK-AUTO suite.

---

## T06.18 -- ROLLBACK-STEPS manual rollback runbook

- **Roadmap Item IDs:** R-104
- **Why:** Documents operator steps for manual rollback when auto triggers fail.
- **Effort:** S
- **Risk:** Medium
- **Risk Drivers:** rollback
- **Tier:** STANDARD
- **Confidence:** [███████---] 75%
- **Requires Confirmation:** No
- **Critical Path Override:** No
- **Verification Method:** Direct test execution (30s)
- **MCP Required:** (none)
- **MCP Preferred:** Sequential, Context7
- **Fallback Allowed:** Yes
- **Sub-Agent Delegation:** None
- **Deliverable IDs:** D-0105
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0105/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0105 `docs/runbooks/rollback.md` step-by-step manual rollback procedure.

**Steps:**
1. **[PLANNING]** Enumerate scenarios each auto trigger covers and manual overlaps.
2. **[EXECUTION]** Document commands for flag flip, middleware enable, DB snapshot restore.
3. **[EXECUTION]** Add decision tree for when to escalate to legacy cut-in.
4. **[VERIFICATION]** Tabletop exercise with SRE team.
5. **[COMPLETION]** Publish and link from OBS-007.

**Acceptance Criteria:**
- Every auto trigger has manual fallback.
- Commands are copy-paste ready.
- Approvals chain documented.
- Version stamped.

**Validation:**
- Manual check: tabletop exercise sign-off.
- Evidence: linkable artifact produced (exercise notes).

**Dependencies:** T06.14, T06.15, T06.16, T06.17
**Rollback:** Revert document to prior revision.
**Notes:** Consolidates OBS-007 rollback references.

---

## T06.19 -- NFR-REL-001 99.9% availability SLO

- **Roadmap Item IDs:** R-105
- **Why:** Formal SLO contract driving alerting thresholds and GA gate.
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
- **Deliverable IDs:** D-0106
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0106/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0106 `docs/slo/auth-availability.md` 99.9% SLO definition + error budget policy.

**Steps:**
1. **[PLANNING]** Define SLI (successful 200 responses to /auth/login + /auth/refresh).
2. **[EXECUTION]** Author SLO doc + error budget policy.
3. **[EXECUTION]** Confirm burn-rate alerts align with SLO.
4. **[VERIFICATION]** Review with product + SRE.
5. **[COMPLETION]** Publish in docs.

**Acceptance Criteria:**
- SLI + SLO + window documented.
- Error budget policy includes freeze rules.
- Referenced by runbook and GA gate.
- Approved by product owner.

**Validation:**
- Manual check: review sign-off recorded.
- Evidence: linkable artifact produced (doc + review note).

**Dependencies:** T05.11, T06.06
**Rollback:** Restore prior doc revision.
**Notes:** Drives OPS-011 approval.

---

## T06.20 -- SUCC-SLO-BOARD production SLO dashboard

- **Roadmap Item IDs:** R-106
- **Why:** Production Grafana view showing SLO status + error budget burn.
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
- **Deliverable IDs:** D-0107
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0107/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0107 `observability/grafana/dashboards/auth-slo.json` SLO + error budget dashboard.

**Steps:**
1. **[PLANNING]** Define panel set (SLO status, burn rate, top errors, latency heatmap).
2. **[EXECUTION]** Build dashboard JSON referencing OBS-005 recording rules.
3. **[VERIFICATION]** Import into prod Grafana and verify panels.
4. **[COMPLETION]** Attach to runbook.

**Acceptance Criteria:**
- Error-budget burn panel live.
- Links from panels to runbook entries.
- Version stamped.
- Provisioned via GitOps.

**Validation:**
- Manual check: dashboard renders in prod Grafana.
- Evidence: linkable artifact produced (screenshot + JSON path).

**Dependencies:** T06.06, T06.19
**Rollback:** Remove dashboard JSON.
**Notes:** Referenced by OPS-011 gate.

---

### Checkpoint: Phase 6 / Tasks 16-20

- **Purpose:** Confirm remaining rollback triggers, SLO doc, and dashboard complete.
- **Verification:**
  - All four ROLLBACK-AUTO triggers drill-verified.
  - Manual rollback runbook tabletop complete.
  - SLO doc approved; dashboard live in prod.
- **Exit Criteria:**
  - 4/4 auto triggers evidenced.
  - SLO + error-budget policy approved.
  - Dashboard linked from runbook + OPS-011 checklist.

---

## T06.21 -- OPS-011 GA go/no-go gate signed checklist

- **Roadmap Item IDs:** R-107
- **Why:** Final gate ensuring SLO, rollback, audit, and rollout readiness; GA launch cannot proceed otherwise.
- **Effort:** M
- **Risk:** High
- **Risk Drivers:** rollback, compliance, auth
- **Tier:** STRICT
- **Confidence:** [█████████-] 90%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `auth/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0108
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0108/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0108 `docs/launch/ga-checklist.md` signed GA go/no-go checklist with evidence links for every prerequisite.

**Steps:**
1. **[PLANNING]** Enumerate prerequisites (migration success, SLO doc, rollback drills x4, audit archival, runbook review, admin approvals).
2. **[EXECUTION]** Gather evidence artifacts from prior tasks (D-0088 -> D-0107).
3. **[EXECUTION]** Execute final staging end-to-end validation run.
4. **[EXECUTION]** Obtain sign-off from the 3 required approvers per OPS-011: sec-reviewer, eng-manager, product.
5. **[VERIFICATION]** Sub-agent verifies all prerequisites have artifacts + sign-offs.
6. **[COMPLETION]** Publish checklist + release GA feature-flag to 100%.

**Acceptance Criteria:**
- Every prerequisite row has linked evidence + approver + timestamp.
- All 3 required sign-offs collected (sec-reviewer + eng-manager + product).
- No open rollback-drill findings.
- GA flag set to 100% only after checklist signed.

**Validation:**
- Manual check: gate meeting minutes + signatures.
- Evidence: linkable artifact produced (signed checklist file).

**Dependencies:** T06.01, T06.02, T06.03, T06.04, T06.05, T06.09, T06.14, T06.15, T06.16, T06.17, T06.18, T06.19, T06.20
**Rollback:** Revoke GA flag; reconvene gate meeting.
**Notes:** Only task gating full 100% launch of new auth stack.

---

### Checkpoint: End of Phase 6

- **Purpose:** Confirm production rollout is complete and all compliance/SLO gates satisfied.
- **Verification:**
  - GA checklist signed by all stakeholders.
  - 99.9% SLO panel green for trailing 7 days on staging.
  - All ROLLBACK-AUTO drills archived; manual rollback runbook validated.
- **Exit Criteria:**
  - No open P1/P2 issues from rollout.
  - Legacy auth returning 410 with 0 traffic.
  - Post-launch review scheduled 14 days out.

---
