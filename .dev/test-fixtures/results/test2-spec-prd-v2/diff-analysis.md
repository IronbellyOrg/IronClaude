---
total_diff_points: 14
shared_assumptions_count: 12
---

# Diff Analysis: Opus Architect vs. Haiku Architect Roadmaps

## 1. Shared Assumptions and Agreements

1. **Complexity rating**: Both assign 0.6 (MEDIUM) complexity score
2. **RS256 JWT signing**: Both specify asymmetric RS256 with secrets-managed key pairs and 90-day rotation
3. **bcrypt cost factor 12**: Both agree on NIST SP 800-63B compliance with bcrypt at cost factor 12 (~250ms target)
4. **Token TTLs**: Both specify 15-minute access tokens and 7-day refresh tokens
5. **Refresh token rotation with replay detection**: Both implement single-use rotation where replay triggers full user token revocation
6. **Password policy**: Both enforce min 8 chars, uppercase, lowercase, digit (identical NIST SP 800-63B interpretation)
7. **Email enumeration prevention**: Both require generic error messages on login failure and identical responses for password reset regardless of email existence
8. **Audit logging as foundational**: Both elevate SOC2 audit logging to Phase 1 rather than deferring it
9. **Feature flag**: Both include `AUTH_SERVICE_ENABLED` as a routing gate for rollback capability
10. **Token storage strategy**: Both specify access token in memory, refresh token in httpOnly cookie
11. **Scope exclusions**: Both exclude OAuth2/OIDC, MFA, RBAC, social login, admin UI from v1.0
12. **Success criteria alignment**: Both target p95 < 200ms at 500 concurrent, 99.9% availability, >60% registration conversion, E2E lifecycle test suite as launch gate

---

## 2. Divergence Points

### D1: Phase Structure and Timeline

- **Opus**: 4 phases across 7 sprints (~10 weeks). Separates Foundation/Infrastructure, Core Auth, Profile/Password Reset, and Hardening/Launch into distinct phases.
- **Haiku**: 2 phases across 6 weeks. Collapses foundation + core auth + logout into Phase 1; profile + password reset + compliance hardening into Phase 2.
- **Impact**: Opus provides more granular milestone checkpoints but extends timeline by ~4 weeks. Haiku is more aggressive but compresses hardening into Phase 2 alongside feature work, risking quality shortcuts under time pressure.

### D2: Logout Endpoint

- **Opus**: Does not include an explicit logout endpoint. Token revocation is implied through refresh token lifecycle.
- **Haiku**: Includes explicit `POST /auth/logout` with `LogoutHandler` that revokes the refresh token and clears the httpOnly cookie. Also proposes optional `LogoutAllDevices` endpoint.
- **Impact**: Haiku's approach is more complete — logout is a standard user expectation (Alex persona). Opus's omission is a gap; the spec's FR-AUTH requirements don't explicitly mandate logout, but it's a reasonable derived requirement.

### D3: Refresh Token Storage Mechanism

- **Opus**: Stores refresh token hashes in database (FR-AUTH.3d). Does not specify the hashing algorithm for refresh tokens.
- **Haiku**: Explicitly specifies hashing refresh tokens with bcrypt before storage, plus a `rotated_from_id` self-referential column for tracking rotation chains.
- **Impact**: Haiku's `rotated_from_id` design is architecturally superior for replay detection — it creates an explicit chain rather than requiring inference. However, bcrypt for refresh token hashing adds latency on every refresh; a faster hash (SHA-256) may be more appropriate since refresh tokens are random (not user-chosen passwords).

### D4: Password Reset Token Storage

- **Opus**: Stores password reset tokens "alongside or parallel to refresh tokens" — vague on exact mechanism.
- **Haiku**: Creates a dedicated `password_reset_tokens` table with explicit schema (id, user_id, token_hash, expires_at, is_used) plus a scheduled cleanup job for expired tokens.
- **Impact**: Haiku's dedicated table with cleanup job is more operationally sound. Opus's ambiguity risks ad-hoc implementation.

### D5: Rate Limiting Implementation

- **Opus**: Specifies "5 attempts per minute per IP" with per-IP rate limiting middleware. No mention of technology choice.
- **Haiku**: Specifies Redis-based `RedisKeyRateLimiter` keyed on `{ip}:{email}` (dual key), with explicit escalation path (10+ failures in 5 min → flag for review). Also addresses distributed IP spoofing as Risk R10.
- **Impact**: Haiku's dual-key approach (IP + email) is more resistant to distributed attacks. The Redis dependency adds infrastructure complexity but is standard practice. Opus's IP-only approach is simpler but more easily evaded.

### D6: Admin Audit Interface

- **Opus**: No admin audit query endpoint. Notes Jordan persona is "partial coverage via logs only" and admin UI deferred to v1.1.
- **Haiku**: Includes `AuditLogQueryHandler` with pagination, date range filtering, and user_id filtering. Positions this as API-level support for Jordan persona even without a UI.
- **Impact**: Haiku provides better Jordan persona coverage within v1.0 scope. Opus's position is defensible (spec says admin UI is out of scope) but an API endpoint is low-cost and high-value for SOC2 auditors.

### D7: Security Review Cadence

- **Opus**: Single security review + penetration testing in Phase 4 (end of project).
- **Haiku**: Two explicit security checkpoints — end of Phase 1 (code review, SAST, threat model) and end of Phase 2 (pentest, penetration testing). Phase 1 checkpoint is a hard gate before proceeding.
- **Impact**: Haiku's approach is significantly stronger. Finding security issues at the end (Opus Phase 4) is expensive to remediate. Haiku's mid-project checkpoint catches structural flaws early.

### D8: Silent Token Refresh (Frontend)

- **Opus**: Mentions token storage strategy (access in memory, refresh in httpOnly cookie) but does not detail client-side silent refresh behavior.
- **Haiku**: Explicitly includes "Silent Token Refresh on Frontend" as a Phase 1 deliverable with 3-day estimate — background refresh when access token expires without page redirect.
- **Impact**: Haiku addresses a critical UX requirement (Alex persona: session persists across page refreshes). Opus assumes this but doesn't plan the work.

### D9: Database Schema Design

- **Opus**: `users` table includes `locked_at` column. `refresh_tokens` table includes `token_hash`, `expires_at`, `revoked_at`.
- **Haiku**: `users` table includes `updated_at` and `deleted_at` (soft delete). `refresh_tokens` table adds `rotated_from_id` (self-referential) and uses `is_revoked` boolean instead of `revoked_at` timestamp.
- **Impact**: Haiku's `deleted_at` supports future account deletion (GDPR right to erasure) without architectural changes. Opus's `locked_at` supports account lockout directly. Opus's `revoked_at` timestamp preserves when revocation occurred (useful for audit). Both have merits — ideally combine both approaches.

### D10: Resource Estimation

- **Opus**: Lists 5 roles (backend TS, security, frontend, DevOps, QA) without effort estimates.
- **Haiku**: Detailed person-week allocation per phase per role, totaling ~24-26 person-weeks. Includes Product Manager time.
- **Impact**: Haiku's resource planning is more actionable for project management. Opus leaves staffing as an exercise for the reader.

### D11: Post-Launch Monitoring

- **Opus**: Defines success criteria targets but no explicit alerting thresholds.
- **Haiku**: Includes explicit post-launch monitoring section with alert thresholds (p95 > 250ms, availability < 99.8%, failed login > 10%, email delivery < 95%).
- **Impact**: Haiku's operational readiness is stronger. Alert thresholds at ~20% above targets give early warning before SLA breach.

### D12: Open Questions Handling

- **Opus**: 8 open questions with recommendations and clear resolution deadlines tied to phases.
- **Haiku**: 6 architectural decisions with detailed rationale, trade-offs, and implementation phase references. Frames some as "architect decisions" (already decided) vs. "stakeholder input needed."
- **Impact**: Opus preserves more optionality for stakeholder input. Haiku is more opinionated, which accelerates execution but may not reflect the team's preferred decision-making style.

### D13: Email Dispatch Architecture

- **Opus**: Lists async email as a recommendation in open questions (OQ-1) but doesn't commit.
- **Haiku**: Commits to async via message queue (Bull/Celery) with explicit retry strategy (exponential backoff, max 5 attempts) and delivery monitoring via SendGrid webhooks.
- **Impact**: Haiku's commitment and detailed retry/monitoring design is production-ready. Opus's deferral creates risk of synchronous implementation by default.

### D14: Wiring Documentation Style

- **Opus**: Integration points documented per-phase in tables with Named Artifact, Type, Wired Components, Owning Phase, Consumed By.
- **Haiku**: Dedicated "Architectural Integration Points" section at the end with cross-references across phases, plus inline wiring context per task.
- **Impact**: Opus's per-phase tables are easier to follow during sprint execution. Haiku's centralized section is better for architectural review. Both approaches have merit; Opus's is more practical for developers.

---

## 3. Areas Where One Variant Is Clearly Stronger

### Opus is stronger in:

- **Requirement traceability**: Every deliverable explicitly maps to FR/NFR identifiers (e.g., "FR-AUTH.1a", "NFR-AUTH.3")
- **Phase granularity**: 4-phase structure provides clearer milestones and go/no-go gates
- **Open question discipline**: Explicitly ties each OQ to blocking phase with resolution deadline
- **Per-phase wiring tables**: Integration points documented where developers need them
- **Scope guardrails section**: Explicit out-of-scope list with escalation guidance ("route to v1.1+ planning cycle")

### Haiku is stronger in:

- **Operational completeness**: Logout endpoint, silent refresh, admin audit API, post-launch monitoring thresholds
- **Security posture**: Dual security checkpoints (mid-project + pre-launch) vs. single end-of-project review
- **Implementation specificity**: Named artifacts with concrete patterns (dispatch table, callback chain, composite pattern), day-level task estimates, technology choices (Redis, Bull, SonarQube)
- **Resource planning**: Person-week estimates per role per phase
- **Schema design**: `rotated_from_id` for rotation chains, `deleted_at` for soft delete, dedicated `password_reset_tokens` table
- **Resilience planning**: Email retry strategy, connection pooling, rate limiter evasion mitigation

---

## 4. Areas Requiring Debate to Resolve

1. **Phase count (2 vs. 4)**: Is the 4-week timeline difference justified by Opus's additional granularity, or does Haiku's compression better serve the Q3 SOC2 deadline? The answer depends on team maturity and risk tolerance.

2. **Refresh token hashing algorithm**: Haiku uses bcrypt for refresh tokens — is the ~250ms latency per refresh acceptable, or should a faster hash (SHA-256) be used since tokens are randomly generated (not vulnerable to dictionary attacks)?

3. **Logout as in-scope**: Both specs don't explicitly require logout. Should it be included in v1.0? The UX argument (Haiku) is compelling, but scope discipline (Opus) has value.

4. **Admin audit API in v1.0**: Low implementation cost (~2 days per Haiku) vs. scope creep risk. SOC2 auditors may need this for the Q3 audit — check with compliance before deciding.

5. **Security checkpoint cadence**: Haiku's mid-project security gate is best practice but adds 2 days of elapsed time. If the team has embedded security review culture (PR-level reviews), the formal checkpoint may be redundant.

6. **Account lockout in v1.0**: Opus includes `locked_at` in schema and defers logic to open question. Haiku explicitly defers to v1.1. Should the schema include the column now (future-proofing) even if logic is deferred?
