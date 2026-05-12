---
high_severity_count: 1
medium_severity_count: 12
low_severity_count: 4
total_deviations: 17
validation_complete: true
tasklist_ready: false
---

## Deviation Report

### DEV-001 — MEDIUM
- **Severity:** MEDIUM
- **Deviation:** Roadmap adds POST `/auth/logout` endpoint (API-007) and `AuthService.logout()` method not specified anywhere in the TDD. The TDD defines exactly 4 API endpoints in Section 8.1 and 5 functional requirements (FR-AUTH-001 through FR-AUTH-005); none involve logout.
- **Source Quote:** TDD Section 8.1: "POST `/auth/login` [...] POST `/auth/register` [...] GET `/auth/me` [...] POST `/auth/refresh`" (complete API overview — no logout endpoint listed)
- **Roadmap Quote:** "API-007 | Implement POST /auth/logout | Single-device logout. Revokes current refresh token in Redis via TokenManager.revoke(). Returns 200 on success, 401 if unauthenticated."
- **Impact:** Roadmap scope exceeds TDD specification. The addition is justified by the PRD (user story: "As Alex, I want to log out so that I can secure my session on a shared device") but represents a scope decision not traceable to the primary engineering spec.
- **Recommended Correction:** Either update the TDD to add FR-AUTH-006 (Logout) with full API specification and acceptance criteria, or annotate the roadmap task as "PRD-sourced, pending TDD amendment."

### DEV-002 — MEDIUM
- **Severity:** MEDIUM
- **Deviation:** Roadmap adds `consentTimestamp` field to the `UserProfile` schema (DM-001, NFR-COMP-001). The TDD `UserProfile` interface defines exactly 7 fields and does not include `consentTimestamp`.
- **Source Quote:** TDD Section 7.1: `interface UserProfile { id: string; email: string; displayName: string; createdAt: string; updatedAt: string; lastLoginAt: string; roles: string[]; }`
- **Roadmap Quote:** "DM-001 [...] consentTimestamp (NFR-COMP-001). [...] consentTimestamp field present for GDPR (NOT NULL on new registrations)."
- **Impact:** Schema diverges from TDD data model. The addition is sourced from PRD Legal & Compliance Requirements (GDPR consent recording) but has no TDD backing.
- **Recommended Correction:** Amend TDD Section 7.1 `UserProfile` interface and field table to include `consentTimestamp: string` with constraints and description.

### DEV-003 — MEDIUM
- **Severity:** MEDIUM
- **Deviation:** Roadmap introduces four compliance-specific tasks (NFR-COMP-001 through NFR-COMP-004) referencing GDPR, SOC2 Type II, and NIST standards. The TDD mentions "security audit requirements" generally and references NIST/bcrypt but does not define NFR-COMP identifiers or GDPR/SOC2 tasks.
- **Source Quote:** TDD Section 2.3: "Compliance requires authentication audit trails before the Q3 regulatory review." (no GDPR, SOC2, or NFR-COMP-NNN identifiers)
- **Roadmap Quote:** "NFR-COMP-001 | Add GDPR consent recording [...] NFR-COMP-002 | Create audit log table [...] NFR-COMP-003 | Validate NIST password storage compliance [...] NFR-COMP-004 | Validate data minimization"
- **Impact:** Roadmap introduces compliance requirements sourced from PRD Section S17, not from TDD. This broadens scope beyond the engineering specification.
- **Recommended Correction:** Update TDD to incorporate compliance NFRs from the PRD, or document the roadmap's PRD-sourced additions as an explicit scope extension.

### DEV-004 — MEDIUM
- **Severity:** MEDIUM
- **Deviation:** TDD specifies 90-day audit log retention. Roadmap does not implement 90 days; instead it gates Phase 1 on stakeholder resolution of OQ-6, noting a conflict between TDD (90 days) and PRD (12 months).
- **Source Quote:** TDD Section 7.2: "Audit log | PostgreSQL 15 | Login attempts, password resets | 90 days"
- **Roadmap Quote:** "OQ-6 | Audit log retention: 90 days vs 12 months. Requires stakeholder decision — PRD specifies 12 months for SOC2, but implementation implications (partitioning, archival, cold storage) are non-trivial [...] Before Phase 1 start (blocking gate)"
- **Impact:** The roadmap correctly identifies the TDD/PRD conflict but defers rather than implementing the TDD's stated 90-day retention. Phase 1 cannot begin until resolution.
- **Recommended Correction:** Resolve the TDD/PRD conflict in the TDD (amend Section 7.2 to match the PRD's 12-month requirement, or document the 90-day decision with rationale). Then update the roadmap to reference the resolved value.

### DEV-005 — MEDIUM
- **Severity:** MEDIUM
- **Deviation:** TDD Release Checklist (Section 24.2) requires validation of a `UserProfile` data migration script. The roadmap has no corresponding task.
- **Source Quote:** TDD Section 24.2: "UserProfile data migration script validated with production-like dataset"
- **Roadmap Quote:** [MISSING]
- **Impact:** A release gate criterion has no implementation task. Migration validation could be missed, risking data integrity during legacy-to-new-system transition.
- **Recommended Correction:** Add an explicit task in Phase 4 or early Phase 5 for creating and validating the `UserProfile` data migration script against a production-like dataset.

### DEV-006 — MEDIUM
- **Severity:** MEDIUM
- **Deviation:** TDD requires TLS 1.3 enforcement on all endpoints. The roadmap has no explicit task for TLS configuration.
- **Source Quote:** TDD Section 13: "All endpoints enforce TLS 1.3, and sensitive fields (password, tokens) are excluded from application logs."
- **Roadmap Quote:** [MISSING] (Phase 4 security review task #47 mentions "TLS" in passing but no dedicated configuration task)
- **Impact:** A security requirement may be assumed as infrastructure default but is not explicitly verified in any roadmap task's acceptance criteria.
- **Recommended Correction:** Add TLS 1.3 enforcement as an acceptance criterion to the Phase 1 infrastructure setup or the Phase 4 security review task.

### DEV-007 — MEDIUM
- **Severity:** MEDIUM
- **Deviation:** TDD specifies that the JWT `accessToken` payload must contain `user id and roles`. The roadmap's JwtService task (COMP-003) specifies signing/verification but does not define the JWT payload structure.
- **Source Quote:** TDD Section 7.1 AuthToken field table: "accessToken | string (JWT) | NOT NULL | Signed by `JwtService` using RS256; contains user id and roles in payload"
- **Roadmap Quote:** "COMP-003 | Implement JwtService | RS256 signing/verification with 2048-bit RSA keys. 5-second clock skew tolerance. Key rotation support (quarterly)."
- **Impact:** Implementers may not include the required payload fields (user id, roles), leading to downstream integration failures when services depend on token claims.
- **Recommended Correction:** Add to COMP-003 acceptance criteria: "JWT payload includes `sub` (user id) and `roles` claims."

### DEV-008 — MEDIUM
- **Severity:** MEDIUM
- **Deviation:** TDD defines 5 milestones with specific date targets and groupings (M1: AuthService + login/register by 2026-04-14; M2: TokenManager + refresh/me by 2026-04-28). The roadmap restructures into 5 phases with different groupings: Phase 1 is data layer only (1 week), Phase 2 is all backend services (2 weeks), Phase 3 combines API + frontend.
- **Source Quote:** TDD Section 23.1: "M1: Core AuthService | 2026-04-14 | AuthService, PasswordHasher, UserProfile schema, POST /auth/register, POST /auth/login [...] M2: Token Management | 2026-04-28 | TokenManager, JwtService, AuthToken model, POST /auth/refresh, GET /auth/me"
- **Roadmap Quote:** "Phase 1: Data Layer and Infrastructure [...] Duration: 1 week [...] Phase 2: Backend Services and Security [...] Duration: 2 weeks"
- **Impact:** The roadmap's phasing separates data layer from business logic (not how TDD milestones are structured). Milestone-based tracking against TDD dates will not align.
- **Recommended Correction:** Document the phasing divergence rationale (e.g., "data layer isolation reduces integration risk") and provide a TDD-milestone-to-roadmap-phase mapping table.

### DEV-009 — MEDIUM
- **Severity:** MEDIUM
- **Deviation:** TDD expects integration tests to pass at M2 completion (Phase 1 exit criteria). The roadmap defers formal integration testing to Phase 4.
- **Source Quote:** TDD Section 23.2: "Phase 1 (M1-M2): Build AuthService core with PasswordHasher and TokenManager. Exit criteria: all unit tests pass, integration tests against PostgreSQL and Redis pass."
- **Roadmap Quote:** Phase 2 exit criteria: "All 5 backend components pass unit tests. Security constraints verified." (integration tests appear only in Phase 4: TEST-004, TEST-005)
- **Impact:** Integration bugs (e.g., schema mismatches, connection pooling issues) may remain undetected until Phase 4, increasing rework risk late in the project.
- **Recommended Correction:** Add integration test tasks to Phase 2 exit criteria, or explicitly justify the deferral with rationale (e.g., "Phase 4 integration testing on frozen codebase reduces flaky test noise").

### DEV-010 — MEDIUM
- **Severity:** MEDIUM
- **Deviation:** TDD requires both passwords and tokens to be excluded from application logs. The roadmap's NFR-COMP-003 only validates password exclusion.
- **Source Quote:** TDD Section 13: "sensitive fields (password, tokens) are excluded from application logs"
- **Roadmap Quote:** "NFR-COMP-003 [...] grep confirms no password plaintext in logs." (no mention of tokens)
- **Impact:** Token values could appear in application logs, enabling token theft from log aggregation systems.
- **Recommended Correction:** Expand NFR-COMP-003 acceptance criteria to include: "grep confirms no token values (access or refresh) in application logs."

### DEV-011 — LOW
- **Severity:** LOW
- **Deviation:** TDD provides specific milestone target dates (M1: 2026-04-14 through M5: 2026-06-09). The roadmap uses relative durations only (Week 1, Week 3, Week 5, etc.).
- **Source Quote:** TDD Section 23.1: "M1: Core AuthService | 2026-04-14 [...] M5: GA Release | 2026-06-09"
- **Roadmap Quote:** "Phase 1: Data Layer | 1 week | Week 1 [...] Phase 5: Migration Rollout | 4 weeks | Week 11"
- **Impact:** Minor — relative durations are more flexible but lose anchoring to specific calendar dates for cross-team coordination.
- **Recommended Correction:** Add a note mapping roadmap weeks to approximate calendar dates based on Phase 1 start date.

### DEV-012 — LOW
- **Severity:** LOW
- **Deviation:** Roadmap adds `auth_logout_total` to the Prometheus metrics registry. TDD Section 14 specifies exactly 4 metrics and does not include a logout counter.
- **Source Quote:** TDD Section 14: "auth_login_total (counter), auth_login_duration_seconds (histogram), auth_token_refresh_total (counter), auth_registration_total (counter)"
- **Roadmap Quote:** "NFR-PERF-001 [...] Emit auth_login_duration_seconds histogram, auth_login_total counter, auth_token_refresh_total counter, auth_registration_total counter, auth_logout_total counter."
- **Impact:** Minimal — follows logically from the addition of the logout endpoint (DEV-001). No correctness risk.
- **Recommended Correction:** If DEV-001 is resolved by amending the TDD, include `auth_logout_total` in TDD Section 14 as well.

### DEV-013 — LOW
- **Severity:** LOW
- **Deviation:** TDD Release Checklist requires explicit go/no-go sign-off from test-lead and eng-manager. The roadmap has no corresponding task or gate.
- **Source Quote:** TDD Section 24.2: "Go/no-go sign-off from test-lead and eng-manager"
- **Roadmap Quote:** [MISSING] (closest is Phase 5 entry criteria: "Phase 4 complete. All tests pass. Security review signed off.")
- **Impact:** Minor process gap — sign-off is implied by Phase 5 entry criteria but not formalized as a discrete activity.
- **Recommended Correction:** Add an explicit go/no-go sign-off gate between Phase 4 and Phase 5.

### DEV-014 — LOW
- **Severity:** LOW
- **Deviation:** TDD Section 26 provides infrastructure cost estimates ($450/month production). The roadmap does not include cost information.
- **Source Quote:** TDD Section 26: "Infrastructure costs for the AuthService are estimated at $450/month for production: 3 Kubernetes pods ($150), managed PostgreSQL ($200), managed Redis ($100)."
- **Roadmap Quote:** [MISSING]
- **Impact:** Minimal — cost is informational context, not an implementable requirement.
- **Recommended Correction:** No action needed unless cost governance requires roadmap-level tracking.

### DEV-015 — HIGH
- **Severity:** HIGH
- **Deviation:** PRD explicitly requires that password reset invalidates all existing sessions. Neither the TDD FR-AUTH-005 nor the roadmap's password reset tasks (FR-AUTH-005 #20, API-006 #27) include session invalidation.
- **Source Quote:** PRD User Story (AUTH-E3): "AC: Reset email sent within 60 seconds. Link expires after 1 hour. **New password invalidates all existing sessions.**" Also PRD Customer Journey: "Password is updated, **all existing sessions are invalidated**, and user is redirected to login."
- **Roadmap Quote:** "FR-AUTH-005 [...] Valid token → password updated. Expired/used token → 400." and "API-006 [...] Valid token → password updated." (no mention of session invalidation)
- **Impact:** Users who reset their password may have compromised sessions remain active, creating a security vulnerability. This is a functional acceptance criterion stated twice in the PRD with no corresponding implementation in the roadmap.
- **Recommended Correction:** Add to roadmap task FR-AUTH-005 (#20) and API-006 (#27) acceptance criteria: "On successful password reset, all existing refresh tokens for the user are revoked via TokenManager, invalidating all active sessions." Also amend TDD FR-AUTH-005 acceptance criteria to include this requirement.

### DEV-016 — MEDIUM
- **Severity:** MEDIUM
- **Deviation:** PRD defines Jordan (Platform Admin) persona with the acceptance criterion "Logs include user ID, event type, timestamp, IP address, and outcome. **Queryable by date range and user.**" The roadmap defers the audit log query API to v1.1, leaving Jordan's primary need partially unmet.
- **Source Quote:** PRD User Story: "As Jordan (admin), I want to view authentication event logs so that I can investigate incidents and satisfy auditors. AC: Logs include user ID, event type, timestamp, IP address, and outcome. Queryable by date range and user."
- **Roadmap Quote:** "OQ-8 | Admin audit log query API? Deferred to v1.1. Jordan persona needs acknowledged; v1.0 logs events, v1.1 adds query API."
- **Impact:** Jordan persona's primary capability (querying audit logs) is deferred. v1.0 emits events but provides no query interface, requiring direct database access for incident investigation.
- **Recommended Correction:** The roadmap's explicit deferral with rationale is acceptable if stakeholders approve. Document the interim workaround (direct SQL queries) and ensure v1.1 planning includes the query API.

### DEV-017 — MEDIUM
- **Severity:** MEDIUM
- **Deviation:** PRD Legal & Compliance section specifies 12-month audit log retention for SOC2 Type II compliance. The roadmap does not implement this; it gates on OQ-6 stakeholder resolution due to the TDD/PRD conflict (TDD says 90 days, PRD says 12 months).
- **Source Quote:** PRD S17: "Audit logging | SOC2 Type II | All auth events logged with user ID, timestamp, IP, and outcome. **12-month retention.**"
- **Roadmap Quote:** "OQ-6 | Audit log retention: 90 days vs 12 months. Requires stakeholder decision"
- **Impact:** If OQ-6 is not resolved before Phase 1, the compliance requirement remains unimplemented, risking SOC2 audit failure in Q3 2026.
- **Recommended Correction:** Resolve the TDD/PRD conflict definitively. If 12 months is required for SOC2, amend TDD Section 7.2 and unblock OQ-6 with the 12-month decision.

---

## Summary

**Severity Distribution:**

| Severity | Count | Percentage |
|----------|-------|------------|
| HIGH | 1 | 5.9% |
| MEDIUM | 12 | 70.6% |
| LOW | 4 | 23.5% |
| **Total** | **17** | **100%** |

**Key Findings:**

1. **One HIGH severity deviation** (DEV-015): Password reset session invalidation is a PRD functional acceptance criterion stated twice with no implementation in the roadmap. This is a security-relevant omission.

2. **Scope additions from PRD** (DEV-001, DEV-002, DEV-003): The roadmap proactively incorporates PRD requirements (logout, GDPR consent, compliance tasks) that the TDD does not specify. These are well-justified but create TDD/roadmap divergence. The TDD should be amended to maintain document chain integrity.

3. **TDD/PRD conflict** (DEV-004, DEV-017): Audit log retention (90 days vs 12 months) is correctly identified by the roadmap as needing resolution, but the blocking gate on OQ-6 means Phase 1 cannot begin until stakeholders decide. This is a schedule risk.

4. **Missing implementation tasks** (DEV-005, DEV-006, DEV-007): Three TDD-specified items (migration script, TLS 1.3, JWT payload contents) lack explicit roadmap tasks or acceptance criteria.

5. **Phasing restructure** (DEV-008, DEV-009): The roadmap reorganizes TDD milestones into a different phase structure and defers integration testing later than the TDD specifies. The restructure is reasonable but undocumented.

**Verdict:** The roadmap is **not tasklist-ready** due to 1 HIGH severity deviation. Resolving DEV-015 (adding session invalidation to password reset acceptance criteria) is required before proceeding to tasklist generation. The 12 MEDIUM deviations should be reviewed and either accepted with rationale or corrected in the source documents.
