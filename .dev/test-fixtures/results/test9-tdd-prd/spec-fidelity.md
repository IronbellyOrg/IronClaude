---
high_severity_count: 2
medium_severity_count: 7
low_severity_count: 3
total_deviations: 12
validation_complete: true
tasklist_ready: false
---

## Deviation Report

### DEV-001 | HIGH | Prometheus metrics instrumentation has no wiring task

- **Deviation**: TDD Section 14 specifies four Prometheus metrics requiring code instrumentation across service components. The roadmap references these metrics as validation acceptance criteria in OPS-004 (Phase 5) but contains no task to implement the metric instrumentation wiring in the service code. Metrics cannot be validated if never instrumented.
- **Source Quote**: "Metrics are exposed via Prometheus: `auth_login_total` (counter), `auth_login_duration_seconds` (histogram), `auth_token_refresh_total` (counter), `auth_registration_total` (counter)." (TDD S14)
- **Roadmap Quote**: OPS-004 AC: "Prometheus-metrics:auth_login_total+auth_login_duration_seconds+auth_token_refresh_total+auth_registration_total" (Phase 5, validation only)
- **Impact**: The team has no implementation task to add metric instrumentation to AuthService, TokenManager, or registration flows. OPS-004 validates the existence of metrics in Phase 5 but no Phase 1-2 task creates them. This callback-binding pattern (metrics library -> service methods -> Prometheus endpoint) has no wiring task.
- **Recommended Correction**: Add a Phase 2 task (e.g., OBS-001) to instrument the four Prometheus metrics into AuthService.login(), AuthService.register(), and TokenManager.refresh() methods, with AC requiring counters and histograms to emit on each call.

### DEV-002 | HIGH | OpenTelemetry distributed tracing instrumentation has no wiring task

- **Deviation**: TDD Section 14 specifies OpenTelemetry span instrumentation across four named components. The roadmap mentions OpenTelemetry in OPS-004 as part of capacity validation but has no task to implement tracing instrumentation in service code.
- **Source Quote**: "Distributed tracing via OpenTelemetry spans covers the full request lifecycle through `AuthService`, `PasswordHasher`, `TokenManager`, and `JwtService`." (TDD S14)
- **Roadmap Quote**: OPS-004 AC: "OpenTelemetry:tracing" (Phase 5, validation only)
- **Impact**: Without a dedicated instrumentation task, span creation and context propagation across AuthService, PasswordHasher, TokenManager, and JwtService may not be implemented. Phase 3 performance validation (NFR-PERF-001) references "APM-tracing:on-AuthService-methods" but this is APM measurement, not OpenTelemetry span instrumentation. The callback-binding pattern for tracing across 4 components has no wiring task.
- **Recommended Correction**: Add a Phase 2 task (e.g., OBS-002) to instrument OpenTelemetry spans across the four named components, with AC requiring spans to propagate through the full AuthService -> PasswordHasher/TokenManager -> JwtService call chain.

### DEV-003 | MEDIUM | Observability alert thresholds from TDD S14 not tasked

- **Deviation**: TDD Section 14 specifies three operational alert thresholds for day-to-day monitoring. The roadmap has rollback triggers (MIG-007) with different thresholds and different purpose, and uptime alerting (NFR-REL-001), but no task configures the S14 operational alerts.
- **Source Quote**: "Alerts are configured for: login failure rate exceeding 20% over 5 minutes, p95 latency exceeding 500ms, and `TokenManager` Redis connection failures." (TDD S14)
- **Roadmap Quote**: MIG-007: "p95>1000ms/5min->rollback; err>5%/2min->rollback; Redis-fail>10/min->rollback" (different thresholds, rollback triggers not operational alerts)
- **Impact**: Post-GA operational monitoring will lack the TDD-specified alert thresholds. The rollback triggers (MIG-007) fire at crisis-level thresholds (p95 >1000ms) while the TDD operational alerts fire at degradation-level thresholds (p95 >500ms). Without the operational alerts, gradual performance degradation may go undetected until it triggers a rollback.
- **Recommended Correction**: Add a Phase 3 task to configure Grafana alert rules for the three TDD S14 thresholds, distinct from the MIG-007 rollback triggers.

### DEV-004 | MEDIUM | Audit log retention changed from 90 days to 12 months

- **Deviation**: The roadmap changes the audit log retention period from the TDD-specified 90 days to 12 months based on PRD compliance requirements. The roadmap documents this as an intentional override (OQ-008) but the TDD text has not been updated.
- **Source Quote**: "Audit log | PostgreSQL 15 | Login attempts, password resets | 90 days" (TDD S7.2)
- **Roadmap Quote**: OQ-008: "Resolved: PRD wins; 12-month retention required per SOC2; TDD Section 7.2 must be updated; affects storage sizing and compliance signoff"
- **Impact**: The TDD and roadmap are in documented conflict. Storage sizing, partitioning strategy (DM-003: "partitioned:by-month"), and cost estimates differ between 90-day and 12-month retention. Teams referencing the TDD will see conflicting retention requirements.
- **Recommended Correction**: Update TDD Section 7.2 to reflect 12-month retention as stated in OQ-008 resolution. Verify cost estimates in TDD S26 account for 12-month audit data growth.

### DEV-005 | MEDIUM | GA timeline extends 31 days beyond TDD milestone target

- **Deviation**: The TDD targets GA release at 2026-06-09 (M5). The roadmap extends GA completion to 2026-07-10, a 31-day extension. The roadmap provides justification (adversarial debate synthesis, dedicated E2E window, SOC2 margin) but diverges from the TDD's committed timeline.
- **Source Quote**: "M5: GA Release | 2026-06-09 | Phase 3 rollout complete, feature flags removed" (TDD S23.1)
- **Roadmap Quote**: "Phase 5: Rollout & Operations | 4 weeks | 2026-06-13 | 2026-07-10" (Timeline Estimates)
- **Impact**: Stakeholders relying on the TDD's June 9 GA date will face a month-long delay. The PRD states "Not shipping in Q2 means a full-quarter delay to the personalization roadmap." The roadmap's July 10 date is technically Q3, though it provides margin for the Q3 SOC2 audit.
- **Recommended Correction**: Either update TDD S23 milestones to match the 13-week roadmap timeline, or compress the roadmap to fit the TDD's ~8-week window. Document the timeline decision rationale in the TDD.

### DEV-006 | MEDIUM | Five-phase roadmap diverges from TDD's three-phase structure

- **Deviation**: The TDD defines a 3-phase implementation plan with specific milestone groupings. The roadmap restructures into 5 phases with different task groupings and adds two new phases (Security/Contracts Baseline and API Hardening).
- **Source Quote**: "Phase 1 (M1-M2): Build AuthService core with PasswordHasher and TokenManager. [...] Phase 2 (M3-M4): Add password reset flow and frontend components. [...] Phase 3 (M5): Rollout and stabilization." (TDD S23.2)
- **Roadmap Quote**: "Phase 1: Security, Contracts & Persistence Baseline | Phase 2: Core Backend & API Contracts | Phase 3: API Hardening & Performance | Phase 4: Frontend, Testing & E2E | Phase 5: Rollout & Operations" (Roadmap phase headers)
- **Impact**: Teams referencing the TDD's phasing for sprint planning will find different phase definitions in the roadmap. The TDD's Phase 1 combines what the roadmap splits across Phases 1-2. The TDD's Phase 2 maps to roadmap Phase 4 with Phase 3 inserted between. Milestone tracking against TDD dates will not align.
- **Recommended Correction**: Add a phase-mapping table to the roadmap showing how TDD milestones M1-M5 map to the 5-phase structure. Alternatively, update TDD S23 to reflect the expanded phasing.

### DEV-007 | MEDIUM | Logout implementation lacks API endpoint task despite PRD in-scope status

- **Deviation**: The PRD explicitly includes logout as an in-scope user story (AUTH-E1). The roadmap identifies the TDD gap (OQ-006) and provides a design task (COMP-010), but contains no API endpoint implementation task (e.g., POST /auth/logout) and no frontend logout action implementation beyond AuthProvider's implied logout() method.
- **Source Quote (PRD)**: "As Alex (end user), I want to log out so that I can secure my session on a shared device. AC: 'Log Out' ends session immediately and redirects to landing page." (PRD AUTH-E1)
- **Roadmap Quote**: OQ-006: "Logout functionality missing from TDD [...] affects session revocation and shared-device safety" | COMP-010: "type:session-component; loc:cross-layer; action:end-session; revoke:refresh-token; redirect:landing; shared-device-risk:reduced" (Phase 1, design only)
- **Impact**: The roadmap's COMP-010 designs logout but no Phase 2 API-xxx task implements the endpoint. AuthProvider integration points reference "Logout action -> token revoker" (Phase 4) but the backend endpoint to accept the revocation request is absent. Implementation teams may omit the logout endpoint entirely.
- **Recommended Correction**: Add a Phase 2 API task (e.g., API-007: POST /auth/logout) with AC: valid-refresh-token->revoked; session-cleared; 200-response. Add a corresponding COMP-009 integration for the frontend logout action.

### DEV-008 | MEDIUM | Password reset does not specify session invalidation per PRD

- **Deviation**: The PRD specifies that setting a new password invalidates all existing sessions. Neither the TDD's FR-AUTH-005 nor the roadmap's corresponding tasks include session invalidation as an acceptance criterion.
- **Source Quote (PRD)**: "New password invalidates all sessions." (PRD FR-AUTH.5 AC); "User enters a new password and submits. Password is updated, all existing sessions are invalidated, and user is redirected to login." (PRD Customer Journey)
- **Roadmap Quote**: FR-AUTH-005 AC: "request(valid-email)->sends-token-email; confirm(valid-token)->updates-hash; token-1h-TTL; single-use; same-response-for-unknown-email" | API-006 AC: "valid-token+strong-pwd->password-updated; expired-token->error; used-token->error; weak-pwd->400"
- **Impact**: After a password reset, existing refresh tokens in Redis remain valid. A compromised session persists even after the password is changed, negating the security purpose of password reset. This directly contradicts the PRD's security intent.
- **Recommended Correction**: Add AC to FR-AUTH-005 and API-006: "on-password-update->all-user-refresh-tokens-revoked-via-TokenManager". Update TEST-005 scope to validate that password reset triggers full token revocation.

### DEV-009 | MEDIUM | Structured application logging not explicitly tasked

- **Deviation**: TDD Section 14 specifies structured application logging for all authentication events as a distinct deliverable from audit database persistence. The roadmap has NFR-COMP-002 for audit event persistence to PostgreSQL but no task for configuring structured application log emissions (stdout/JSON).
- **Source Quote**: "The `AuthService` emits structured logs for all authentication events (login success/failure, registration, token refresh, password reset)." (TDD S14)
- **Roadmap Quote**: NFR-COMP-002: "events:login_success+login_failure+registration+password_reset+token_refresh; fields:userId+timestamp+ip+outcome; retention:12mo; storage:queryable; partitioned" (audit DB persistence only)
- **Impact**: NFR-COMP-002 covers compliance audit records in PostgreSQL. The TDD additionally requires structured application logs emitted to stdout for operational debugging and log aggregation. Without explicit tasking, the team may rely solely on database audit records without implementing streaming application logs, limiting real-time observability and incident debugging.
- **Recommended Correction**: Add a Phase 2 task for structured log configuration (e.g., OBS-003) with AC: JSON-format logs emitted for all auth events; sensitive fields (password, tokens) excluded; log level and format configurable per environment.

### DEV-010 | LOW | Password reset endpoints lack formal API specifications in TDD Section 8

- **Deviation**: TDD Section 8.1 API Overview and Section 8.2 Endpoint Details only formally specify four endpoints. The password reset endpoints (POST /auth/reset-request, POST /auth/reset-confirm) are named in FR-AUTH-005 but lack request/response schema definitions in Section 8.2. The roadmap correctly adds API-005 and API-006 tasks to fill this gap.
- **Source Quote**: TDD S8.1 table lists only: POST /auth/login, POST /auth/register, GET /auth/me, POST /auth/refresh. FR-AUTH-005 references "POST `/auth/reset-request`" and "POST `/auth/reset-confirm`" without full API specs.
- **Roadmap Quote**: API-005: "any-email->same-success-response; registered-email-triggers-SendGrid; no-enumeration; token-1h-TTL" | API-006: "valid-token+strong-pwd->password-updated; expired-token->error; used-token->error; weak-pwd->400"
- **Impact**: Minor inconsistency in the TDD. The roadmap correctly infers and tasks the endpoints. No risk to implementation correctness.
- **Recommended Correction**: Update TDD S8.1 to add the two reset endpoints with rate limits. Add S8.2 endpoint detail blocks for POST /auth/reset-request and POST /auth/reset-confirm with request/response schemas.

### DEV-011 | LOW | PasswordResetPage component added beyond TDD component inventory

- **Deviation**: The TDD Section 10.1 route table lists three pages (LoginPage, RegisterPage, ProfilePage) with no /reset-password route. The roadmap adds COMP-012 (PasswordResetPage at /reset-password), which is implied by FR-AUTH-005 but not listed in the TDD's component inventory.
- **Source Quote**: TDD S10.1 routes: "/login | LoginPage | No", "/register | RegisterPage | No", "/profile | ProfilePage | Yes" (3 routes total)
- **Roadmap Quote**: COMP-012: "route:/reset-password; two-step:request-form(email)+confirm-form(token+new-password); inline-password-validation; same-UX-for-registered/unregistered; expired-link-error-with-retry"
- **Impact**: Minimal. The component is clearly required by FR-AUTH-005's user-facing password reset flow. The roadmap correctly identifies the gap and fills it.
- **Recommended Correction**: Add /reset-password route and PasswordResetPage to TDD S10.1 route table. Add PasswordResetPage to S10.2 shared components with props.

### DEV-012 | LOW | Success criteria SC-008, SC-009, SC-010 sourced from PRD without TDD basis

- **Deviation**: The roadmap includes three success criteria (SC-008: session duration >30min, SC-009: failed login rate <5%, SC-010: password reset completion >80%) that originate from the PRD's Success Metrics section but have no corresponding metrics in TDD Section 4.
- **Source Quote**: TDD S4.1-4.2 defines 7 metrics: login p95 <200ms, registration success >99%, refresh p95 <100ms, 99.9% uptime, hash time <500ms, registration conversion >60%, DAU >1000.
- **Roadmap Quote**: "SC-008 | Average session duration | >30 minutes | Refresh event analytics and cohort review | Phase 5 exit" | "SC-009 | Failed login rate | <5% of attempts | Audit log analysis with alert thresholds | Phase 5 exit" | "SC-010 | Password reset completion | >80% | Reset-requested->password-updated funnel | Phase 4 exit"
- **Impact**: Minimal. Adding PRD-sourced metrics strengthens validation coverage. The metrics don't conflict with TDD specifications.
- **Recommended Correction**: Add SC-008, SC-009, and SC-010 metrics to TDD Section 4.2 Business Metrics table to maintain single-source-of-truth alignment.

## PRD Supplementary Validation

**Persona Coverage**: All three personas (Alex, Jordan, Sam) have roadmap phases addressing their primary needs. Alex's end-to-end journey (register/login/reset/profile) is fully covered across Phases 2-4. Jordan's audit visibility is addressed via DM-003, NFR-COMP-002, and COMP-011. Sam's programmatic token management is covered by FR-AUTH-003 and API-004. One gap: Jordan's "account lock/unlock" need is partially addressed (automated lockout via FR-AUTH-001) but admin unlock is absent — deferred per TDD NG-003 (RBAC out of scope).

**Business Metric Traceability**: All five PRD success metrics have corresponding SC-xxx entries with validation methods and phase assignments. Fully traced.

**Compliance & Legal Coverage**: All four PRD legal requirements (GDPR consent, SOC2 audit logging, NIST password storage, GDPR data minimization) have dedicated roadmap tasks with Phase 1 ratification. No gaps.

**Scope Boundary Enforcement**: No roadmap items fall outside the PRD's scope definition. OAuth, MFA, RBAC enforcement, and social login are correctly excluded.

## Summary

The roadmap is a thorough and well-structured translation of the TDD, covering all 5 functional requirements, all 5 non-functional requirements, all 6 API endpoints (including 2 inferred from FR-AUTH-005), all 9 named components, both data models, the 3-phase rollout plan, rollback procedures, and operational readiness requirements. Integration wiring is exceptionally well-documented with per-phase tables.

**Two HIGH severity findings** concern the observability instrumentation gap: Prometheus metrics (4 counters/histograms) and OpenTelemetry tracing (4-component span chain) are specified as TDD S14 deliverables requiring code-level wiring but have no implementation tasks in the roadmap. They appear only as Phase 5 validation ACs, creating a "validate what was never built" risk.

**Seven MEDIUM findings** span: operational alert thresholds not tasked (S14), audit log retention conflict (90d→12mo), timeline extension (+31 days), phasing restructure (3→5 phases), logout implementation gap (PRD), password reset session invalidation omission (PRD), and structured application logging not tasked (S14).

**Three LOW findings** are additive improvements: password reset endpoint specs, PasswordResetPage component, and PRD-sourced success criteria — all cases where the roadmap correctly fills TDD gaps.

| Severity | Count | Pattern |
|---|---|---|
| HIGH | 2 | Observability instrumentation wiring (S14) |
| MEDIUM | 7 | Timeline/phasing divergence (3), PRD coverage gaps (2), observability tasking (2) |
| LOW | 3 | Correct gap-filling additions |
| **Total** | **12** | |

The roadmap cannot proceed to tasklist conversion until the 2 HIGH deviations are resolved by adding explicit instrumentation tasks for Prometheus metrics and OpenTelemetry tracing, ideally in Phase 2 alongside the service implementations they instrument.
