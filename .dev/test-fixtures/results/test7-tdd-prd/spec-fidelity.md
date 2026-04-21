---
high_severity_count: 0
medium_severity_count: 4
low_severity_count: 3
total_deviations: 7
validation_complete: true
tasklist_ready: true
---

## Deviation Report

### DEV-001
- **ID**: DEV-001
- **Severity**: MEDIUM
- **Deviation**: Audit log retention conflict between TDD (90 days) and PRD (12 months) resolved in favor of PRD value, but the TDD's explicit 90-day commitment is silently overridden rather than flagged as a TDD source change request.
- **Source Quote (TDD)**: "|Audit log|PostgreSQL 15|Login attempts, password resets|90 days|"
- **Source Quote (PRD)**: "Audit logging|SOC2 Type II|All auth events logged with user ID, timestamp, IP, and outcome. 12-month retention."
- **Roadmap Quote**: "Retention policy = 12 months (committed value, cites OQ-CONFLICT-001); partitioned by month for reclamation"
- **Impact**: The roadmap correctly applies PRD precedence but the TDD source remains contradictory. Engineers reading only the TDD would implement to 90 days. The OQ-CONFLICT-001 closure cites "PRD/compliance precedence" but no roadmap task targets updating TDD S7.2 to match.
- **Recommended Correction**: Add an explicit task or note in M1 deliverables to update TDD S7.2 audit-log retention from 90 days to 12 months for documentation consistency, or flag TDD update as part of OPS-AUDIT-QA in M5.

### DEV-002
- **ID**: DEV-002
- **Severity**: MEDIUM
- **Deviation**: Logout endpoint and `LogoutHandler` are added to roadmap (API-007 / COMP-015) based solely on PRD scope, but TDD S8 explicitly enumerates only 4 endpoints (`/auth/login`, `/auth/register`, `/auth/me`, `/auth/refresh`) and does not include logout.
- **Source Quote (TDD)**: "RESTful API endpoints: `/auth/login`, `/auth/register`, `/auth/me`, `/auth/refresh`"
- **Source Quote (PRD)**: "**As Alex (end user), I want to** log out **so that** I can secure my session on a shared device. *AC:* 'Log Out' ends session immediately and redirects to landing page."
- **Roadmap Quote**: "API-007|POST /v1/auth/logout endpoint|Implement logout endpoint required by PRD in-scope definition and user story coverage"
- **Impact**: The roadmap correctly closes a PRD user story gap that the TDD omitted, but the TDD source still does not document the logout endpoint contract (request/response, error codes, rate limit). Without TDD update, downstream Tech Reference and engineers may miss the contract.
- **Recommended Correction**: Add a roadmap task to update TDD S8 to include the logout endpoint specification, or document this as a known TDD gap in OQ-CONFLICT registry.

### DEV-003
- **ID**: DEV-003
- **Severity**: MEDIUM
- **Deviation**: Reset request rate limit (5 req/min/IP) is introduced in roadmap as OQ-RESET-RL-001 with no source basis in either TDD S8 (which lists only 4 endpoints with rate limits) or PRD (which is silent on rate limits).
- **Source Quote (TDD)**: "|POST|`/auth/login`|No|10 req/min per IP|...|POST|`/auth/register`|No|5 req/min per IP|...|GET|`/auth/me`|Yes (Bearer)|60 req/min per user|...|POST|`/auth/refresh`|No (refresh token in body)|30 req/min per user|"
- **Roadmap Quote**: "/reset-request=5/min/IP (per OQ-RESET-RL-001)"
- **Impact**: The roadmap proposes a value not in the source documents. While reasonable, this creates a roadmap-introduced specification that requires backfill into the TDD before downstream consumers can use it as source of truth.
- **Recommended Correction**: Either explicitly mark the 5 req/min/IP value as roadmap-proposed pending TDD update, or add a task to update TDD S8.1 with the reset endpoint rate limits.

### DEV-004
- **ID**: DEV-004
- **Severity**: MEDIUM
- **Deviation**: TDD S8.2 specifies refresh token transport in request body (`{"refreshToken": "..."}`), but roadmap commits to HttpOnly cookie-only transport via COMP-HTTPONLY-001 and treats request-body transport as deferred (OQ-REFRESH-TRANSPORT-001).
- **Source Quote (TDD)**: "POST `/auth/refresh` ... **Request:** ```json { \"refreshToken\": \"dGhpcyBpcyBhIHJlZnJlc2g...\" } ```"
- **Roadmap Quote**: "Request: {refreshToken} from HttpOnly cookie (per COMP-HTTPONLY-001) ... dual-mode request-body refresh not shipped in v1.0 pending OQ-REFRESH-TRANSPORT-001"
- **Impact**: The roadmap unilaterally narrows the TDD's stated contract for security reasons (R-001 XSS), which is defensible but contradicts the documented TDD API spec. Sam (API consumer persona) explicitly cannot use cookies, and the PRD JTBD #4 names programmatic refresh as a requirement.
- **Recommended Correction**: Resolve OQ-REFRESH-TRANSPORT-001 before M3 with explicit product/security sign-off; if cookie-only is the final answer, add a task to update TDD S8.2 to reflect the HttpOnly cookie contract and document Sam persona's required path (e.g., separate API consumer flow).

### DEV-005
- **ID**: DEV-005
- **Severity**: LOW
- **Deviation**: Roadmap adds a 5th and 6th frontend page (`ResetRequestPage`, `ResetConfirmPage`) not enumerated in TDD S10.1 page/route table, derived from PRD recovery journey.
- **Source Quote (TDD)**: "|`/login`|`LoginPage`|No|Email/password login form...|`/register`|`RegisterPage`|No|Registration form...|`/profile`|ProfilePage|Yes|Displays `UserProfile` data..."
- **Source Quote (PRD)**: "**Password Reset Flow:** Click 'Forgot Password' -> enter email -> confirmation shown ... -> email with 1-hour reset link -> set new password -> redirected to login."
- **Roadmap Quote**: "COMP-016|ResetRequestPage React component|Implement `/forgot-password` page... COMP-017|ResetConfirmPage React component|Implement `/reset-password` page..."
- **Impact**: Roadmap correctly derives frontend pages needed for FR-AUTH-005 reset flow. TDD frontend page table is incomplete relative to its own stated reset capability.
- **Recommended Correction**: Add task to backfill TDD S10.1 with the two reset pages; minor doc correction.

### DEV-006
- **ID**: DEV-006
- **Severity**: LOW
- **Deviation**: Roadmap milestone structure (5 technical-layer milestones) differs from TDD S23.1 milestone structure (5 feature-based milestones), acknowledged via OQ-CONFLICT-002 with mapping table.
- **Source Quote (TDD)**: "|M1: Core `AuthService`|2026-04-14|...|M2: Token Management|2026-04-28|...|M3: Password Reset|2026-05-12|...|M4: Frontend Integration|2026-05-26|...|M5: GA Release|2026-06-09|"
- **Roadmap Quote**: "M1 Foundation — Schemas, Infra, Feature-Flag Plumbing ... M2 Core Authentication ... M3 Token Management & Session ... M4 Integration & Hardening ... M5 Production Readiness & GA"
- **Impact**: Same end date and total duration; mapping table preserves traceability. No correctness impact.
- **Recommended Correction**: None; mapping table is sufficient.

### DEV-007
- **ID**: DEV-007
- **Severity**: LOW
- **Deviation**: Admin audit-log view (JTBD-GAP-001) is shipped as CLI in v1.0 to address Jordan persona, but neither TDD nor PRD specifies an admin interface form factor.
- **Source Quote (PRD)**: "**As Jordan (admin), I want to** view authentication event logs **so that** I can investigate incidents and satisfy auditors. *AC:* Logs include user ID, event type, timestamp, IP address, and outcome. Queryable by date range and user."
- **Source Quote (TDD)**: [No corresponding admin UI/CLI deliverable specified]
- **Roadmap Quote**: "JTBD-GAP-001|Admin audit-log view (PRD JTBD gap fill)|Minimal admin-scoped query surface for Jordan persona ... interim surface is admin CLI since full admin UI is TDD gap"
- **Impact**: Roadmap acknowledges PRD JTBD coverage with interim CLI; resolution defers full UI to v1.1. Acceptable interim approach.
- **Recommended Correction**: Confirm Jordan persona and product accept CLI as v1.0 deliverable; backfill TDD with admin CLI specification.

## Summary

The roadmap demonstrates strong fidelity to both the TDD and PRD source documents. All 5 functional requirements (FR-AUTH-001 through FR-AUTH-005), 4 API endpoints from TDD S8, all 2 data models, all 5 NFRs, all 3 risks (R-001/R-002/R-003), and all phased rollout commitments are addressed with concrete implementation tasks. Integration wiring is comprehensively tracked via per-milestone Integration Points tables. Observability instrumentation (4 named Prometheus metrics, OTel tracing, all 3 alert thresholds, and 4 distinct rollback triggers) is implemented in M2/M3/M4 — not deferred to validation-only ACs.

The 7 deviations found are dominated by legitimate **roadmap-led source corrections** rather than fidelity failures: the roadmap correctly closes PRD-required gaps that the TDD silently omitted (logout endpoint, reset UI pages, audit retention, admin JTBD). Severity distribution: **0 HIGH, 4 MEDIUM, 3 LOW**. The 4 MEDIUM deviations all stem from contradictions or silences in source documents that the roadmap resolves with explicit OQs and justifications, not from roadmap omissions.

**tasklist_ready: true** — no HIGH severity deviations block tasklist generation. The MEDIUM deviations should be tracked as follow-up TDD doc updates but do not require roadmap rework.
