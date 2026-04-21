---
convergence_score: 0.62
rounds_completed: 2
---

# Adversarial Debate: Opus Architect (Variant A) vs. Haiku Architect (Variant B)

## Round 1: Initial Positions

### D1: Phase Structure and Timeline

**Variant A (Opus — 4 phases, 10 weeks):**
Four phases provide natural go/no-go gates between Foundation, Core Auth, Profile/Reset, and Hardening. Each phase has a clean scope boundary. The 4-week difference buys us three additional milestone checkpoints where stakeholders can inspect progress and course-correct. For a security-critical service feeding into a SOC2 audit, rushing is the wrong optimization. The overlap between phases (Sprints 2, 4, 6) already compresses the calendar — this isn't waterfall, it's staged delivery with parallel tracks.

**Variant B (Haiku — 2 phases, 6 weeks):**
Six weeks is not "rushing" — it's respecting the Q3 SOC2 deadline and the personalization roadmap dependency. Collapsing into two phases eliminates artificial handoff ceremonies. The security checkpoint at end of Phase 1 (day 19) is a hard gate that provides the same risk mitigation as Opus's Phase 4, but four weeks earlier. Every week of delay is a week the personalization team can't integrate. The 10-week timeline assumes a luxury we don't have.

---

### D2: Logout Endpoint

**Variant A (Opus — no explicit logout):**
The spec's FR-AUTH requirements don't mandate a logout endpoint. Token revocation through refresh token lifecycle already handles session termination — a refresh token in an httpOnly cookie can be cleared client-side, and server-side the token simply expires or is revoked during password reset. Adding endpoints not in the spec is scope creep. If logout is needed, it belongs in v1.1 alongside admin UI and other session management features.

**Variant B (Haiku — explicit POST /auth/logout):**
Logout is a derived requirement from any reasonable reading of the Alex persona. "Session persists across page refreshes" implies a user can also *end* a session intentionally. The implementation cost is 1 day — `LogoutHandler` marks the refresh token as revoked and clears the cookie. Omitting logout creates a security gap: if a user suspects their session is compromised, they have no way to terminate it. This isn't scope creep; it's completing the session lifecycle.

---

### D3: Refresh Token Hashing Algorithm

**Variant A (Opus — unspecified hash for refresh tokens):**
We specify storing refresh token *hashes* in the database (FR-AUTH.3d) without mandating bcrypt specifically for this purpose. Refresh tokens are randomly generated 32-byte strings — they aren't vulnerable to dictionary attacks. The appropriate hash is SHA-256, which is effectively instant. Bcrypt's 250ms latency on every token refresh would degrade the p95 for a core hot-path operation that fires on every page load after access token expiry.

**Variant B (Haiku — bcrypt for refresh tokens):**
We use bcrypt for refresh tokens to maintain a single hashing strategy across the codebase. Consistency reduces implementation complexity and the cognitive load of "which hash do I use where?" The 250ms per refresh is within our p95 budget of 200ms when you account for the fact that bcrypt isn't the only operation — but the total budget is tight. We acknowledge this is a debatable point.

---

### D5: Rate Limiting — IP-only vs. IP+Email

**Variant A (Opus — per-IP, 5/min):**
Per-IP rate limiting is the standard approach and avoids leaking information about which email accounts exist. If you rate-limit on `{ip}:{email}`, an attacker can probe email existence by testing different emails from the same IP — rate-limited emails are registered, non-rate-limited ones aren't. The simplicity of IP-only also avoids a Redis dependency in Phase 1.

**Variant B (Haiku — dual key IP+email via Redis):**
IP-only rate limiting is trivially evaded by distributed botnets. The dual key `{ip}:{email}` prevents both distributed credential stuffing (same email, many IPs) and single-IP brute force (same IP, many emails). The email enumeration concern is mitigated by applying the rate limit response (429) identically regardless of email existence — you rate-limit the *attempt count*, not the *account state*. Redis is standard infrastructure for any production service at this scale.

---

### D6: Admin Audit API

**Variant A (Opus — deferred to v1.1):**
The spec explicitly states admin UI is out of scope. An API endpoint for querying audit logs is a stepping stone to an admin panel — it implies a consumer that doesn't exist yet. SOC2 auditors can query the database directly or via standard BI tooling. Adding an API endpoint invites questions about authentication for that endpoint (separate admin auth?), pagination, filtering — each "simple" feature spawns more work.

**Variant B (Haiku — AuditLogQueryHandler, 2 days):**
SOC2 auditors won't query raw PostgreSQL. They need a reproducible, documented interface. The `AuditLogQueryHandler` is a read-only paginated endpoint with date/user/event filters — 2 days of work that directly serves the Jordan persona. Authentication can be scoped to internal network or basic auth initially. The alternative is scrambling during the Q3 audit to provide log access, which is worse than building it now.

---

### D7: Security Review Cadence

**Variant A (Opus — single review in Phase 4):**
A comprehensive security review at the end, when all code is complete, is more efficient than multiple partial reviews. Phase 4 is dedicated exclusively to hardening — no competing feature work. The security engineer can review the complete attack surface holistically rather than in fragments. PR-level security reviews during Phases 1-3 catch the obvious issues; the formal review catches architectural flaws.

**Variant B (Haiku — two checkpoints, mid-project + pre-launch):**
Finding a structural security flaw at week 9 of a 10-week project is catastrophically expensive. Our Phase 1 checkpoint (day 19) reviews the cryptographic primitives, token lifecycle, and replay detection *before* building password reset on top of them. If the foundation is flawed, we catch it with 3 weeks of feature work invested, not 8. This is standard security engineering practice — shift left.

---

### D8: Silent Token Refresh (Frontend)

**Variant A (Opus — not explicitly planned):**
Token storage strategy is documented (access in memory, refresh in httpOnly cookie). The frontend implementation of silent refresh is an implementation detail of the frontend auth pages listed in Phase 3. It doesn't need a separate line item — any competent frontend engineer implementing auth pages will build the refresh flow.

**Variant B (Haiku — explicit 3-day deliverable in Phase 1):**
"Any competent engineer will figure it out" is not a plan. Silent refresh involves intercepting 401 responses, queuing pending requests, refreshing the token, and replaying queued requests — it's non-trivial. Without explicit planning, it becomes a last-minute scramble that introduces bugs. The 3-day estimate in Phase 1 ensures session persistence works end-to-end before Phase 2 builds on it.

---

### D13: Email Dispatch Architecture

**Variant A (Opus — deferred decision, OQ-1):**
Email dispatch architecture (sync vs. async) is an open question for the team to resolve before Phase 3. Committing to async via message queue now adds infrastructure complexity (Bull/Celery, Redis, dead letter queues, monitoring) that may be premature. The team might prefer a simpler synchronous implementation with a timeout, especially if SendGrid's p95 is under 500ms.

**Variant B (Haiku — committed async with retry strategy):**
Synchronous email dispatch on a security-critical endpoint is an availability risk. If SendGrid has a 30-second outage, every password reset request blocks for 30 seconds, possibly timing out and returning a 500 — leaving users uncertain whether their reset was sent. Async with exponential backoff (max 5 retries) and SendGrid webhook monitoring is the production-ready choice. The infrastructure cost of a message queue is minimal compared to the operational risk.

---

## Round 2: Rebuttals

### D1 Rebuttal

**Variant A rebuts B:**
"Respecting the Q3 deadline" assumes 6 weeks is sufficient with zero schedule slip. A 6-week plan with no buffer means any delay — a security review finding, an email integration issue, a load test failure — directly threatens the launch date. Our 10-week plan has overlap and buffer. The personalization team needs a *stable* auth service, not a rushed one. Shipping a security-critical service with no margin is the actual risk.

**Variant B rebuts A:**
The 10-week plan *also* has zero explicit buffer — you've just spread the same work thinner with more ceremony between phases. Our Phase 1 security checkpoint is a hard gate; if it fails, we know at week 3, not week 9. The personalization team's Q2 dependency means every week of delay has a dollar cost. We can add a 1-week buffer to our plan (7 weeks total) and still beat Opus by 3 weeks.

---

### D3 Rebuttal

**Variant B rebuts A:**
We concede the point on bcrypt for refresh tokens. SHA-256 is the correct choice for randomly-generated tokens — bcrypt's dictionary-attack resistance is irrelevant here, and 250ms per refresh is a real cost on a hot path. We would adopt SHA-256 for refresh token hashing while keeping bcrypt exclusively for passwords.

**Variant A rebuts B:**
We appreciate the concession. This is exactly the kind of design decision that a specification should not over-prescribe — the implementer should choose the right tool for each hashing context.

---

### D5 Rebuttal

**Variant A rebuts B:**
The email enumeration vector via rate limiting is real. Applying 429 identically regardless of email existence doesn't fully mitigate it — timing differences between "email exists, rate limit applies" and "email doesn't exist, rate limit applies" can leak information. IP-only avoids this class of side-channel entirely. However, we acknowledge that distributed attacks are a legitimate threat. A compromise: IP-only in Phase 1, with the dual-key approach as a documented Phase 2 hardening item.

**Variant B rebuts A:**
Timing-based enumeration via rate limiting is a stretch — the rate limit check itself is a cache lookup, not a database query, so timing is uniform. But the compromise of IP-only in Phase 1 with dual-key in Phase 2 is acceptable *only if* the Phase 2 hardening is a blocking requirement, not a "nice to have" that gets cut.

---

### D6 Rebuttal

**Variant A rebuts B:**
"SOC2 auditors won't query raw PostgreSQL" — actually, they often do, via their own tooling or exported CSV/JSON. The audit *trail* is the requirement, not the *query interface*. However, we acknowledge that a simple read-only API with basic auth is low-cost and reduces audit friction. If the compliance team confirms they need a programmatic interface for Q3, we would include it.

**Variant B rebuts A:**
Agreed — this should be a compliance team decision. We'd accept deferring it if compliance explicitly signs off that database-level access meets their needs for the Q3 audit. The 2-day estimate stands as the cost if they want an API.

---

### D7 Rebuttal

**Variant A rebuts B:**
"Finding a structural flaw at week 9" assumes PR-level reviews are ineffective. In a well-run team, security-relevant PRs get security engineer review before merge. The formal Phase 4 review catches *systemic* issues (interaction between components, deployment configuration, holistic threat modeling) that PR-level reviews miss. However, we concede that a brief mid-project checkpoint (1 day, not 2) focused on cryptographic primitives specifically would be valuable.

**Variant B rebuts A:**
We accept the reduced scope — a 1-day mid-project review focused on cryptographic implementation and token lifecycle is sufficient for Phase 1, with the comprehensive pentest in Phase 2 as planned. The key principle is that foundational security code gets reviewed before being built upon.

---

### D2 Rebuttal

**Variant A rebuts B:**
The 1-day implementation cost is accurate for the endpoint itself, but omits testing (logout E2E, logout + refresh interaction, logout all devices), documentation, and the scope precedent it sets. However, we acknowledge that session termination is a basic user expectation. We would accept including a minimal `POST /auth/logout` (revoke refresh token, clear cookie) without the `LogoutAllDevices` variant.

**Variant B rebuts A:**
Accepted. `LogoutAllDevices` can be deferred to v1.1 alongside account lockout. The basic logout endpoint is the non-negotiable minimum.

---

## Convergence Assessment

### Areas of Agreement Reached

1. **Refresh token hashing**: SHA-256, not bcrypt — both variants converge (Haiku conceded)
2. **Logout endpoint**: Minimal `POST /auth/logout` included in v1.0 — both converge (Opus conceded with scope limit)
3. **Mid-project security checkpoint**: 1-day focused review of cryptographic primitives after Phase 1 core implementation — both converge (Opus conceded reduced version; Haiku accepted reduced scope)
4. **Admin audit API**: Decision deferred to compliance team input — both converge on making it conditional
5. **Silent token refresh**: Should be explicitly planned, not assumed — Opus implicitly conceded by not countering strongly

### Remaining Disputes (Unresolved)

1. **Phase structure (2 vs. 4)**: Fundamental disagreement on timeline. Opus argues for safety margin; Haiku argues for speed-to-value. Resolution depends on team capacity and Q3 deadline firmness — this is a stakeholder decision, not a technical one.

2. **Rate limiting approach (IP-only vs. dual-key)**: Partial convergence on phased approach (IP-only first, dual-key as hardening), but disagreement on whether dual-key is a hard gate for launch.

3. **Email dispatch (sync vs. async)**: Haiku's position is technically stronger but adds infrastructure. Opus preserves optionality. Resolution should be an engineering team decision based on existing infrastructure (does a message queue already exist?).

4. **Resource estimation specificity**: Haiku provides person-week estimates; Opus lists roles only. This is a presentation preference, not a technical dispute — both approaches are valid for different audiences.

5. **Schema design (locked_at vs. deleted_at, revoked_at vs. is_revoked)**: Both have genuine merits. The merged roadmap should include both `locked_at` (future lockout), `deleted_at` (future GDPR deletion), `revoked_at` (audit-friendly timestamp over boolean), and `rotated_from_id` (explicit rotation chain).

6. **Post-launch monitoring thresholds**: Haiku includes explicit alert thresholds; Opus does not. This is an additive improvement — no reason to exclude it.

### Recommendation for Merge

The merged roadmap should adopt Haiku's operational completeness (logout, silent refresh, monitoring thresholds, email retry strategy, `rotated_from_id` schema) layered onto Opus's structural discipline (requirement traceability, per-phase wiring tables, open question resolution deadlines, scope guardrails). Phase count and timeline should be escalated to stakeholders with both options presented.
