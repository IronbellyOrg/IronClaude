---
high_severity_count: 1
medium_severity_count: 9
low_severity_count: 3
total_deviations: 13
validation_complete: true
tasklist_ready: false
---

## Deviation Report

### 1. DEV-001
- **Severity**: HIGH
- **Deviation**: Roadmap implements role-based enforcement (admin role checks) that TDD NG-003 and PRD S12 explicitly mark as out-of-scope.
- **Source Quote (TDD §3.2)**: "NG-003 | Role-based access control (RBAC) | `UserProfile` includes a roles field but enforcement is out of scope"
- **Source Quote (PRD S12)**: "Role-based access control | Authorization is a separate concern; dedicated PRD"
- **Roadmap Quote**: "API-009 ... admin-role JWT required; body `{reason}` ... 403 non-admin ... API-010 ... admin-role JWT required ... 403 non-admin ... ADMIN-001 ... requires admin role in JWT; 403 otherwise"
- **Impact**: Scope creep into authorization domain that both source documents intentionally defer. Creates partial/ad-hoc RBAC that will collide with the planned dedicated RBAC PRD, risks inconsistent role semantics across the platform, and extends v1.0 surface area (and attack surface) beyond what stakeholders approved.
- **Recommended Correction**: Either (a) defer ADMIN-001/API-009/API-010 to v1.1 and raise a scope-change request jointly amending TDD NG-003 + PRD S12; or (b) retain the endpoints but gate them via an IP allow-list or pre-shared admin API key at the gateway rather than role-in-JWT enforcement, keeping the TDD "enforcement out of scope" promise intact.

### 2. DEV-002
- **Severity**: MEDIUM
- **Deviation**: Roadmap success criterion for registration conversion sets a stricter target than the PRD.
- **Source Quote (PRD S19)**: "Registration conversion rate | > 60% | Funnel: landing -> register -> confirmed account"
- **Roadmap Quote**: "Registration completion rate | PRD goal | Registration start → completion % | ≥ 75%"
- **Impact**: Validation gate may fail GA entry on a threshold the PRD did not commit to. Also changes the metric subject ("conversion" vs "completion"), so measurement method may not align.
- **Recommended Correction**: Align roadmap Success Criterion #1 to "> 60%" with source citation to PRD S19; if the team wants a stretch goal, annotate ≥75% as an aspirational target rather than the validation threshold.

### 3. DEV-003
- **Severity**: MEDIUM
- **Deviation**: Password reset completion target tightened above PRD commitment.
- **Source Quote (PRD S19)**: "Password reset completion | > 80% | Funnel: reset requested -> new password set"
- **Roadmap Quote**: "Password-reset completion rate | PRD goal | Reset request → successful password change % | ≥ 85%"
- **Impact**: Same risk as DEV-002 — GA/ready gate may block on a threshold the business did not approve.
- **Recommended Correction**: Reset target to "> 80%" to match PRD S19.

### 4. DEV-004
- **Severity**: MEDIUM
- **Deviation**: NFR-PERF-002 target has been unit-converted in the roadmap success criteria from "500 concurrent login requests" to "≥ 1000 RPS", which is a different load dimension.
- **Source Quote (TDD §5.2)**: "NFR-PERF-002 | Concurrent authentication | Support 500 concurrent login requests | Load testing with k6"
- **Roadmap Quote**: "Throughput capacity | TDD NFR-PERF-002 | Sustained req/s on `/auth/*` | ≥ 1000 RPS"
- **Impact**: The Success Criteria gate is not the same as the TDD NFR. The roadmap tasks (NFR-PERF-002 task #73, LOAD-TEST-FULL task #109) correctly reference 500 concurrent users, but the Success Criteria row cannot be consistently satisfied against the TDD definition. Audit/review gates may disagree with load-test evidence.
- **Recommended Correction**: Change Success Criterion #5 to "≥ 500 concurrent `/auth/login` requests sustained at p95 < 200ms, error rate < 0.1%", matching TDD §5.2 wording exactly.

### 5. DEV-005
- **Severity**: MEDIUM
- **Deviation**: TDD §4.2 business metric for daily active authenticated users is not represented in the roadmap's Success Criteria or any validation milestone.
- **Source Quote (TDD §4.2)**: "Daily active authenticated users | > 1000 within 30 days of GA | `AuthToken` issuance counts"
- **Roadmap Quote**: [MISSING]
- **Impact**: Untraced business metric; GA success review (POST-GA-REVIEW) has no validation hook for DAU, so the TDD's 30-day post-GA adoption commitment will not be measured.
- **Recommended Correction**: Add a POST-GA-REVIEW acceptance criterion measuring DAU from `AuthToken` issuance counts with target >1000 by GA+30d, and add a corresponding Success Criteria row.

### 6. DEV-006
- **Severity**: MEDIUM
- **Deviation**: Roadmap inserts a 30-day human-confirmation gate in front of the rollback triggers, which TDD §19.4 phrases as automatic conditions.
- **Source Quote (TDD §19.4)**: "Rollback is triggered if any of the following occur during rollout: - p95 latency exceeds 1000ms for more than 5 minutes - Error rate exceeds 5% for more than 2 minutes - `TokenManager` Redis connection failures exceed 10 per minute - Any data loss or corruption detected in `UserProfile` records"
- **Roadmap Quote**: "OBS-ROLLBACK-TRIGGERS ... each triggers runbook playbook with SMS/PagerDuty confirmation required for first 30 days (operational-maturity gate per merge constraint); automatic after 30-day burn-in"
- **Impact**: During the 30-day window the "Error rate >5% for 2 min" TDD trigger will not fire automatically — a human must acknowledge first, potentially extending MTTR past the TDD's 2-minute impact threshold on error-rate breaches and violating the implicit "triggered if occur" contract.
- **Recommended Correction**: Either (a) remove the human-gate and honor TDD §19.4 auto-trigger semantics from day 1, or (b) amend TDD §19.4 with an ADR documenting the 30-day burn-in and update R-PRD-002 rollback commitments.

### 7. DEV-007
- **Severity**: MEDIUM
- **Deviation**: Account lockout (FR-AUTH-001 AC4) is not delivered in the milestone where login ships; it slips to M3 while login ships in M2.
- **Source Quote (TDD §5.1)**: "FR-AUTH-001 ... 4. Account locked after 5 failed attempts within 15 minutes."
- **Source Quote (TDD §23)**: "M1: Core `AuthService` | 2026-04-14 | `AuthService`, `PasswordHasher`, `UserProfile` schema, POST `/auth/register`, POST `/auth/login`"
- **Roadmap Quote**: "FA0 (Login with email/password) ... Eff:L Pri:P0" appears in M2 (2026-04-13 → 2026-04-24), while SEC-001 ("Account lockout 5 failures / 15 min ... Implement lockout") appears in M3 (2026-04-27 → 2026-05-15)
- **Impact**: Login becomes available to alpha users without brute-force protection for ~3 weeks. Also, FR-AUTH-001 cannot be marked feature-complete at the "Core Authentication" milestone exit, contradicting TDD's M1 deliverable packaging.
- **Recommended Correction**: Move SEC-001 into M2 as a blocker for FA0 exit, or add an explicit FA0 acceptance note that login endpoint is firewall-restricted to internal tenants until SEC-001 lands.

### 8. DEV-008
- **Severity**: MEDIUM
- **Deviation**: TDD's explicit 6-step rollback procedure is not enumerated in the roadmap's runbook acceptance criteria.
- **Source Quote (TDD §19.3)**: "1. Disable `AUTH_NEW_LOGIN` feature flag ... 2. Verify legacy login flow is operational via smoke tests 3. Investigate `AuthService` failure root cause ... 4. If data corruption is detected ... restore from last known-good backup 5. Notify auth-team and platform-team via incident channel 6. Post-mortem within 48 hours of rollback"
- **Roadmap Quote**: "OPS-001 Runbook: AuthService down ... resolution (restart pods, failover to replica, reject refresh if Redis down) ..."
- **Impact**: On-call runbooks don't verifiably contain the 6 TDD-mandated steps (especially items 4 = backup restore decision and 6 = 48-hour post-mortem SLA). Post-incident audit may find the SOC2-relevant post-mortem commitment uncaptured.
- **Recommended Correction**: Add an explicit acceptance criterion to OPS-001/OPS-002 that the published runbook contains all 6 steps verbatim from TDD §19.3, and that the 48-hour post-mortem SLA is registered in the incident-response calendar.

### 9. DEV-009
- **Severity**: MEDIUM
- **Deviation**: TDD §17 sub-component performance budgets are not individually instrumented or validated; only the aggregate 200ms envelope is.
- **Source Quote (TDD §17)**: "The `JwtService` sign and verify operations complete in under 5ms. `TokenManager` Redis operations target < 10ms latency."
- **Roadmap Quote**: OBS-003 measures "auth_login_duration_seconds" histogram; NFR-PERF-001-M3 validates aggregate p95 < 200ms; no per-component latency histogram defined for `JwtService.sign/verify` or `TokenManager` Redis operations.
- **Impact**: Regression in one sub-budget (e.g., Redis latency drift to 50ms) may be masked by overall envelope until it consumes the whole budget. Loss of observability signal at the component granularity TDD specified.
- **Recommended Correction**: Add two Prometheus histograms in M4: `auth_jwt_operation_duration_seconds{op}` and `auth_redis_operation_duration_seconds{op}`, with alerts on 5ms and 10ms p95 breaches respectively.

### 10. DEV-010
- **Severity**: MEDIUM
- **Deviation**: PRD's "reset email delivered within 60 seconds" SLA from the customer journey and PRD acceptance is not reflected in the ASYNC-QUEUE acceptance criteria.
- **Source Quote (PRD S14, Password Reset Journey, step 3)**: "User opens the reset email (delivered within 60 seconds) and clicks the link (1-hour TTL)."
- **Source Quote (PRD S5, FR-AUTH.5 AC)**: "Reset email sent within 60 seconds"
- **Roadmap Quote**: "ASYNC-QUEUE ... queue created; worker processes jobs; retries on SendGrid 5xx (3 attempts exponential backoff); dead-letter queue configured; metric `auth_reset_email_send_total`"
- **Impact**: No instrumentation or SLO exists against the PRD's explicit delivery time guarantee; user-visible recovery experience could drift without triggering any alert.
- **Recommended Correction**: Add an SLO to ASYNC-QUEUE: p95 email-send latency (queue submission → SendGrid 2xx) < 60s, with a Prometheus histogram `auth_reset_email_latency_seconds` and an alert rule on p95 > 60s.

### 11. DEV-011
- **Severity**: LOW
- **Deviation**: Milestone organization diverges from TDD §23 (feature-sliced M1–M5) in favor of a technically-layered structure, and M5 end-date extends past TDD GA.
- **Source Quote (TDD §23)**: "M1: Core `AuthService` | 2026-04-14 ... M2: Token Management | 2026-04-28 ... M3: Password Reset | 2026-05-12 ... M4: Frontend Integration | 2026-05-26 ... M5: GA Release | 2026-06-09"
- **Roadmap Quote**: "M1 Foundation ... M2 Core Logic ... M3 Integration, Tokens & Frontend ... M4 Hardening, Observability & Compliance ... M5 Production Readiness & GA ... GA target: 2026-06-09 ... M5 end extends to 2026-06-12 to absorb phased-rollout ramp buffer"
- **Impact**: Reporting and progress-tracking against TDD milestones requires a translation table (roadmap provides one in the Timeline Estimates). GA date itself is preserved.
- **Recommended Correction**: Add an explicit TDD→roadmap milestone mapping table in the Executive Summary, or annotate each roadmap milestone with the covered TDD milestone(s) to preserve traceability.

### 12. DEV-012
- **Severity**: LOW
- **Deviation**: TDD goal G-004 uses "CRUD operations" language that exceeds the read-only capability actually specified in TDD §8 and delivered by the roadmap.
- **Source Quote (TDD §3.1)**: "G-004 | Profile management | `UserProfile` CRUD operations available via `/auth/me`"
- **Roadmap Quote**: "API-003 GET /v1/auth/me ... Bearer auth required; 200 returns `UserProfile` JSON per DM-001 ..."
- **Impact**: TDD is self-inconsistent (G-004 says CRUD; §8 specifies only GET). Roadmap aligns with §8 and with PRD FR-AUTH.4 (read-only). Minor traceability noise, no functional gap against PRD.
- **Recommended Correction**: Flag in the roadmap Open Questions that TDD G-004 should be corrected to "Profile retrieval" to match §8, or confirm that PUT/PATCH /auth/me is genuinely v1.1 scope.

### 13. DEV-013
- **Severity**: LOW
- **Deviation**: PRD's "Login success rate ≥ 99.5%" target in the roadmap is not sourced from any explicit PRD or TDD line — it is inferred from NFR-REL-001 availability.
- **Source Quote (TDD §5.2)**: "NFR-REL-001 | Service availability | 99.9% uptime measured over 30-day rolling windows"
- **Source Quote (PRD S19)**: "Failed login rate | < 5% of attempts"
- **Roadmap Quote**: "Login success rate (valid creds) | PRD goal | Successful logins / total login attempts with valid creds | ≥ 99.5%"
- **Impact**: Success criterion label claims "PRD goal" but has no PRD citation. The inverse (PRD's <5% failed rate) is a different metric (includes invalid credentials). Potential confusion between availability SLO and login success rate.
- **Recommended Correction**: Either (a) rename to "Service availability ≥ 99.9%" and cite NFR-REL-001, or (b) derive directly from PRD S19 failed-login-rate and restate as "Failed login rate < 5% of attempts".

## Summary

13 deviations identified: 1 HIGH, 9 MEDIUM, 3 LOW. The lone HIGH is a genuine scope-boundary violation — the roadmap ships admin role-gating (ADMIN-001, API-009, API-010) that both TDD NG-003 and PRD S12 explicitly park for a dedicated RBAC effort. MEDIUM findings cluster around (a) success-metric drift from PRD/TDD targets, (b) sub-NFR targets and SLAs that appear in the source documents but have no instrumentation task, and (c) rollout-procedure divergences (lockout timing, rollback human-gate, 6-step procedure). LOW findings concern organizational/labeling differences that don't affect correctness. **`tasklist_ready: false`** — the RBAC-scope violation (DEV-001) must be resolved (scope amendment or implementation change) before the roadmap is safe to hand to task generation.
