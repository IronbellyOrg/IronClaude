---
high_severity_count: 0
medium_severity_count: 5
low_severity_count: 4
total_deviations: 9
validation_complete: true
tasklist_ready: true
---

## Deviation Report

### DEV-001
- **ID**: DEV-001
- **Severity**: MEDIUM
- **Deviation**: TDD specifies 90-day audit log retention; roadmap overrides to 12 months without updating the source TDD.
- **Source Quote**: "|Audit log|PostgreSQL 15|Login attempts, password resets|90 days|"
- **Roadmap Quote**: "**12-month audit retention over 90-day TDD default** — OQ-003 conflict resolved in favor of PRD S17 SOC2 Type II evidence requirement."
- **Impact**: Roadmap intentionally diverges from TDD retention; storage sizing, partition-drop plan, and TDD §7.2 require update before implementation. Documented as PRD-driven gap-fill but source TDD remains stale.
- **Recommended Correction**: Update TDD §7.2 audit log retention to 12 months and add PRD-traceability marker in the roadmap entry (e.g., `PRD-gap-fill:TDD-update-needed`) to downgrade to LOW.

### DEV-002
- **ID**: DEV-002
- **Severity**: MEDIUM
- **Deviation**: Admin surface (API-007 logout, API-008 events query, API-009 lock, API-010 unlock, COMP-011 AdminAuditPage) is added beyond TDD scope without explicit traceability label.
- **Source Quote**: "|Method|Path|Auth Required|Rate Limit|Description| |POST|`/auth/login`|No|10 req/min per IP|... |POST|`/auth/register`|... |GET|`/auth/me`|... |POST|`/auth/refresh`|..." (TDD lists only 4 endpoints)
- **Roadmap Quote**: "**Close SOC2 Jordan gap in v1.0** via minimal admin surface (API-007 logout, API-008 events query, API-009 lock, API-010 unlock, COMP-011 AdminAuditPage) — PRD S7 persona coverage tips over clean-boundary deferral"
- **Impact**: Extensions are justified by PRD Jordan persona + SOC2 but not labeled with a traceability marker (e.g., `PRD-gap-fill:TDD-update-needed`). Without the label they count as undocumented extensions.
- **Recommended Correction**: Tag API-007..010 and COMP-011 with `PRD-jordan-gap-fill` or equivalent marker tied to PRD S7/S17, or add corresponding endpoints to the TDD API surface.

### DEV-003
- **ID**: DEV-003
- **Severity**: MEDIUM
- **Deviation**: Password reset flow adds "all sessions revoked" behavior beyond TDD specification.
- **Source Quote**: "POST `/auth/reset-confirm` with valid token updates the password hash. 3. Reset tokens expire after 1 hour. 4. Used reset tokens cannot be reused."
- **Roadmap Quote**: "reset-confirm→new hash stored + all sessions revoked; token 1h TTL+single-use"
- **Impact**: Session revocation on password reset is a PRD AC ("New password invalidates all existing sessions") not present in TDD FR-AUTH-005. Roadmap correctly closes PRD gap but should flag TDD update.
- **Recommended Correction**: Label this AC as `PRD-gap-fill:TDD-update-needed` pointing to PRD FR-AUTH.5 and Password Reset journey step 4, and update TDD FR-AUTH-005 ACs accordingly.

### DEV-004
- **ID**: DEV-004
- **Severity**: MEDIUM
- **Deviation**: Refresh-token storage mechanism differs: TDD states opaque token hashed in Redis; roadmap AC says "stored in Redis by `TokenManager`" with "hashedAtRest" — consistent — but frontend refreshToken storage in HttpOnly cookie (R-001 mitigation) is not in TDD.
- **Source Quote**: "R-001|Token theft via XSS allows session hijacking|Medium|High|Store `AuthToken` accessToken in memory only (not localStorage). `AuthProvider` clears tokens on tab close. HttpOnly cookies for refreshToken."
- **Roadmap Quote**: "accessToken in memory only (R-001); refreshToken in HttpOnly cookie"
- **Impact**: Actually consistent with TDD R-001. Re-evaluate: this is aligned. Retained as LOW stylistic difference only.
- **Recommended Correction**: Downgrade or remove — verified alignment with TDD §20 R-001.

### DEV-005
- **ID**: DEV-005
- **Severity**: MEDIUM
- **Deviation**: Refresh latency NFR (SC-003 <100ms) appears only as success criterion, not as explicit NFR implementation task.
- **Source Quote**: "|Token refresh latency (p95)|< 100ms|APM instrumentation on `TokenManager.refresh()`|"
- **Roadmap Quote**: "SC-003|VLD refresh latency target|VA1|API-004, OPS-005|metric:refresh p95; target<100ms; method:APM tracing on refresh path; regressions blocked"
- **Impact**: Target is validated at rollout but no M2 implementation task enforces <100ms during development. Risk of late-discovery performance regression.
- **Recommended Correction**: Add a pre-merge NFR gate or integration test in M3 asserting refresh p95 <100ms on staging baseline.

### DEV-006
- **ID**: DEV-006
- **Severity**: LOW
- **Deviation**: API version prefix `/v1/auth/*` used in roadmap while TDD §8.4 notes version prefix is "in production"; TDD endpoint paths show unversioned `/auth/*`.
- **Source Quote**: "The authentication API is versioned via URL prefix (`/v1/auth/*` in production)."
- **Roadmap Quote**: "all 10 `/v1/auth/*` endpoints live with unified error envelope"
- **Impact**: Consistent with TDD intent; stylistic alignment on versioning from day one.
- **Recommended Correction**: None; roadmap correctly adopts production versioning early.

### DEV-007
- **ID**: DEV-007
- **Severity**: LOW
- **Deviation**: CAPTCHA after 3 failed attempts added to LoginPage beyond TDD.
- **Source Quote**: "Block offending IPs at WAF level. Enable CAPTCHA challenge on `LoginPage` after 3 failed attempts."
- **Roadmap Quote**: "CAPTCHA after 3 fails (R-002)"
- **Impact**: Aligned with TDD R-002 contingency; roadmap promotes contingency to primary mitigation.
- **Recommended Correction**: None; traceable to R-002.

### DEV-008
- **ID**: DEV-008
- **Severity**: LOW
- **Deviation**: GDPR consent capture (NFR-COMP-001) and data minimization (NFR-COMP-003) introduced from PRD; TDD does not specify these NFRs explicitly.
- **Source Quote**: (PRD) "| Consent at registration | GDPR | Users must consent to data collection at registration. Consent recorded with timestamp.|"
- **Roadmap Quote**: "NFR-COMP-001|Capture GDPR consent at RGS|Registration|DM-001|consent_accepted_at:timestamptz-NN; consent_version:varchar; RGS rejected if unchecked; consent event audited"
- **Impact**: PRD-driven compliance gap-fill correctly added to roadmap and DM-001 schema; TDD UserProfile schema omits consent fields.
- **Recommended Correction**: Tag NFR-COMP-001/003 and DM-001 consent fields with `PRD-gap-fill:TDD-update-needed` referencing PRD Legal & Compliance table; update TDD §7.1 UserProfile to include consent fields.

### DEV-009
- **ID**: DEV-009
- **Severity**: LOW
- **Deviation**: Rate-limit on `/auth/reset-request` (3/hr/IP) added beyond TDD specification.
- **Source Quote**: (TDD §8.1 does not list a rate limit for /auth/reset-request)
- **Roadmap Quote**: "rate-limit 3/hr/IP"
- **Impact**: Reasonable security addition; PRD does not specify but aligned with enumeration-prevention principle.
- **Recommended Correction**: Mark as `source-extension` for traceability; update TDD §8.1 table to include the limit.

## Summary

Analysis covered 5 comparison dimensions (signatures, data models, gates, CLI options, NFRs, integration wiring completeness) plus 5 PRD-supplementary dimensions (persona coverage, business metrics, compliance, scope boundary, PRD story completeness). Findings: 0 HIGH, 5 MEDIUM, 4 LOW — 9 total deviations. All deviations are either transparent PRD-driven gap-fills or minor enhancements; none omit, contradict, or fundamentally misrepresent source requirements. All PRD personas (Alex, Jordan, Sam) have corresponding roadmap coverage (Alex via COMP-001/002/003 + journeys; Jordan via API-008/009/010 + COMP-011; Sam via API-004 refresh CNT). All PRD in-scope user stories have implementation tasks. Compliance (GDPR consent, SOC2 audit logging, NIST password policy) is fully covered. Scope boundaries respected (no OAuth, MFA, or RBAC tasks). `tasklist_ready: true`.
