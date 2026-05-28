# Round 1 — Variant 2 Advocate (sonnet)

## Position Summary

Variant 2 produces the more operationally honest and actionably detailed roadmap. It correctly identifies the project as greenfield (eliminating an infeasible legacy-rollback assumption), provides a concrete staffing plan that a hiring manager can act on immediately, quantifies costs for procurement (including pentest budget), includes post-GA product continuity planning that prevents v1.0 from becoming an orphan release, and places account lockout in M1 where it eliminates a brute-force vulnerability window that Variant 1 leaves open for four weeks. While Variant 1 is stronger on security formalization (state machines, token families, chaos testing), these are design-level artifacts that belong in the TDD, not the roadmap. Variant 2 focuses the roadmap on what roadmaps are for: sequencing, staffing, risk management, and delivery commitments.

---

## Steelman of Variant 1

Before critiquing Variant 1, I acknowledge what it genuinely gets right.

**State machine formalization (U-001, S-007).** Variant 1 Section 9 defines explicit state machines for refresh tokens (`issued -> rotated | revoked | expired | reused`), account lockout (`unlocked <-> locked`), and password reset tokens (`pending -> consumed | expired`). These prevent ambiguous implementation. This is genuinely valuable -- a developer reading V1's Section 9.1 knows exactly what transitions are legal and what guards enforce them. Variant 2 lacks this entirely.

**Token family concept (U-002).** Variant 1's "reuse detection revokes entire lineage of refresh tokens descending from a single login event" (Section 9.1, risk R-111) is a security-relevant design decision that prevents token replay attacks across a token chain. Variant 2 mentions "token rotation and revocation" but never defines what happens when a rotated token is reused. This is a meaningful gap.

**Audit retention conflict identification (X-008, C-005).** Variant 1 flags the TDD/PRD conflict explicitly: "TDD Section 7.2 says 90 days, PRD says 12 months" and creates OQ-R1 for resolution before D-102 commit. Variant 2 silently states "12-month audit log retention policy enforcement" (D-033) without acknowledging TDD's 90-day specification. Flagging conflicts is better than silently resolving them.

**Chaos testing (U-005, C-014).** Variant 1 QA-7 explicitly tests Redis down, PostgreSQL failover, and SendGrid down. Variant 2 mentions integration tests but has no chaos engineering track. These tests catch failure modes before production.

**Enumeration timing targets (U-004, C-015).** Variant 1 QA-6 enforces <50ms variance (login) and <30ms variance (reset-request). Variant 2 mentions "identical response" but provides no measurable timing gate. Measurable gates are better than informal aspirations.

**Communication and governance (S-009).** Variant 1 Section 15 defines a meeting cadence table (weekly status, weekly burndown, bi-weekly risk review, go/no-go review). This operationalizes the roadmap into a review rhythm. Variant 2 has no governance section.

**Multi-tab coordination (U-003).** Variant 1 specifies BroadcastChannel API for cross-tab token sync. Variant 2 is silent on this. In a real SPA, logging out in tab A while tab B remains active creates confusing UX without this.

**GDPR right-to-erasure urgency flag (U-008).** Variant 1 flags this as "a hard legal obligation" with urgency, while Variant 2 lists it as "Post-v1.0" without urgency. The legal obligation is real regardless of scope phase.

These are substantive contributions. Variant 1 is a more thorough security and design document. The question is whether those strengths belong in a roadmap or in the TDD that the roadmap references.

---

## Strengths Claimed (with evidence)

### Strength 1: Greenfield assumption correctly stated -- eliminates infeasible rollback path

**Variant 2 evidence:** Assumption 6 (Section 9.2) states explicitly: "There is no existing legacy auth system requiring migration. The PRD describes a greenfield implementation ('the platform currently operates without any user identity system'). If a legacy system exists, M5 must include migration scripts and the rollback procedure changes."

**Why this is superior:** The source PRD Executive Summary states: "The platform currently operates without any user identity system." The Problem Statement confirms: "Every visitor is anonymous." There is no legacy auth. Variant 1's rollback procedure (Section 12.2 step 2) says: "Flip AUTH_NEW_LOGIN OFF -- traffic routes back to legacy auth." This rollback path is architecturally infeasible on a greenfield deployment. Variant 2's rollback (Section 12.1) correctly shows a maintenance-page fallback for greenfield: "Disable AUTH_NEW_LOGIN feature flag. All traffic routes back to legacy behavior (or, for greenfield, displays a maintenance page)."

**Diff point:** U-025, X-004.

### Strength 2: Detailed team composition enables immediate staffing action

**Variant 2 evidence:** Section 10.1 provides a 10-row table with role, allocation percentage, and active sprint window:

| Role | Allocation | Sprints Active |
|------|-----------|----------------|
| Backend Engineer 1 | 100% | Sprint 1-8 |
| Backend Engineer 2 | 100% | Sprint 3-8 |
| Backend Engineer 3 | 100% | Sprint 5-8 |
| Frontend Engineer 1 | 100% | Sprint 7-8 |
| Frontend Engineer 2 | 100% | Sprint 7-8 |
| QA Engineer | 50% Sprint 1-4, 100% Sprint 5-11 | -- |
| Security Engineer | 25% | Sprint 1-2, Sprint 9-10 |
| DevOps Engineer | 25% | Sprint 1, Sprint 4, Sprint 9 |
| Product Manager | 10% | Sprint 1-11 |

**Why this is superior:** Variant 1's team composition (Section 14) is a single row: "2 backend + 1 frontend FTE + 0.5 SRE + 0.25 security review." This tells a manager nothing about when each person is needed. Variant 2's table shows that Backend Engineer 3 is only needed from Sprint 5 (password reset), Frontend Engineers are only needed for Sprints 7-8, and Security is only needed in Sprints 1-2 and 9-10. This enables staggered onboarding and accurate cost forecasting.

**Diff point:** U-022, S-012.

### Strength 3: Account lockout placed in M1 eliminates brute-force vulnerability window

**Variant 2 evidence:** D-006 (M1): "Account lockout after 5 failed attempts within 15 minutes" (Section 3.1, line 79). Exit criteria: "Account locks after 5 failed logins within 15 minutes, returns 423" (Section 3.1, line 97).

**Why this is superior:** The login endpoint (`POST /auth/login`) is public-facing from the moment it ships. If lockout is deferred to M3 (Variant 1, D-305), the login endpoint is vulnerable to brute-force attacks for the entire M1 and M2 window -- 4 weeks in Opus's timeline, 8 weeks in Sonnet's sprint labeling. The PRD's Risk Analysis explicitly rates brute-force attacks as High probability, Medium impact. Deferring protection against a High-probability risk for 4-8 weeks on a public endpoint is a security gap. The TDD Section 13 states: "Account lockout after 5 failed login attempts within 15 minutes mitigates brute-force attacks." There is no "mitigates brute-force attacks... starting in week 5" qualifier.

**Counter to Variant 1's scope concern:** Variant 1 argues lockout adds scope to M1's tight 2-week window. But lockout is a counter on failed login attempts with a threshold check -- approximately 20-30 lines of code (a `LoginAttemptTracker` that increments a counter and checks against a threshold). This is not architecturally complex. The risk of NOT including it (4 weeks of unmitigated brute-force exposure on a public endpoint) far outweighs the schedule risk of adding 20-30 lines to M1.

**Diff point:** C-003, X-002.

### Strength 4: Post-GA planning prevents v1.0 from becoming an orphan release

**Variant 2 evidence:** Section 13 "Post-GA Considerations" with three subsections:

- Section 13.1: v1.1 planning (Q3 2026) -- MFA, API keys, remember me, email verification, password change, self-service unlock
- Section 13.2: v2.0 planning (Q4 2026) -- OAuth, social login, RBAC, admin dashboard
- Section 13.3: Ongoing maintenance -- key rotation, bcrypt review, retention verification, dependency updates, capacity review

**Why this is superior:** Variant 1 has no post-GA section. Its Out of Scope section (Section 10) lists items like MFA, OAuth, and RBAC as deferred but provides no timeline or sequencing. Product teams need visibility into what comes next to plan their own roadmaps. The PRD's Non-Goals explicitly defer MFA to "v1.1" and OAuth to "v2.0" -- a roadmap should honor that versioning by showing when those phases land. Without post-GA planning, stakeholders have no answer to "what happens after June 9?"

**Diff point:** U-023, S-013.

### Strength 5: Feature flag lifecycle table operationalizes flag management

**Variant 2 evidence:** Appendix B provides per-flag lifecycle dates:

| Flag | Created | Enabled | Disabled | Removed |
|------|---------|---------|----------|---------|
| `AUTH_NEW_LOGIN` | Sprint 8 | Sprint 9 | On rollback only | Sprint 11 + 2 weeks |
| `AUTH_TOKEN_REFRESH` | Sprint 8 | Sprint 9 | On rollback only | Sprint 11 + 4 weeks |

**Why this is superior:** Feature flags that are never removed become permanent configuration debt. Variant 1 mentions "removal targets recorded" in Section 10 but provides no concrete dates. Variant 2 specifies exactly when each flag is created, enabled, and removed. This prevents the common failure mode where feature flags persist indefinitely because "nobody remembers what they do." The TDD Section 19.2 specifies a removal target ("Remove after Phase 3 GA" and "Remove after Phase 3 + 2 weeks"), and Variant 2 operationalizes this with concrete sprint deadlines.

**Diff point:** U-024, C-021.

### Strength 6: Admin audit log query deliverable serves Jordan persona

**Variant 2 evidence:** D-030 (M3): "Audit log query interface for admin (filter by date range, user, event type)" (Section 3.3, line 190). Exit criteria: "Audit logs queryable by date range and user ID" (Section 3.3, line 208).

**Why this is superior:** The PRD defines Jordan the Platform Admin as a named persona whose JTBD is: "When a security incident occurs, I want to see who attempted access and lock compromised accounts." The PRD User Story for Jordan states: "Logs include user ID, event type, timestamp, IP address, and outcome. Queryable by date range and user." Variant 1 mentions audit logs in the personas coverage check (Section 13) but has no dedicated deliverable for the query interface. Audit logs that cannot be queried are audit logs that cannot be used for incident investigation. D-030 is the deliverable that makes the audit log actually useful to Jordan.

**Diff point:** U-027, C-018.

### Strength 7: Pentest cost quantified for procurement

**Variant 2 evidence:** Section 10.3 cost projection table: "External pentest (one-time): $5,000-$15,000" (line 700).

**Why this is superior:** External penetration testing is a PRD requirement ("Security breach from implementation flaws... mitigation: Dedicated security review; penetration testing before production"). It requires procurement. Variant 1 lists "External penetration test" (CC1 SEC-5) but provides no budget. A procurement team cannot start a vendor engagement without a budget estimate. Variant 2's $5K-$15K range enables the product manager to request budget approval in parallel with development, preventing M5 from being blocked by procurement lead time.

**Diff point:** U-026, C-023.

### Strength 8: Three-phase decomposition rationale justifies structure against PRD

**Variant 2 evidence:** Section 2.2 "Why Three Phases, Not Two" explicitly argues: "The PRD's two-phase split places password reset (a security-sensitive email integration) in the same phase as frontend integration. Separating them isolates risk: the email-dependent password reset flow has external dependencies (SendGrid) and unique failure modes (delivery latency, token expiry), while frontend integration is purely internal."

**Why this is superior:** The PRD prescribes two phases (Section "Phasing"): Phase 1 (Sprint 1-3) and Phase 2 (Sprint 4-6). The TDD prescribes five milestones (M1-M5). A roadmap that blindly follows either source without reconciling them creates confusion. Variant 2 explicitly acknowledges both prescriptions and provides an engineering rationale for its three-phase decomposition. Variant 1 adopts the TDD's five-milestone structure without discussing why it diverges from the PRD's two-phase prescription.

**Diff point:** U-021.

### Strength 9: Hidden beta buffer provides schedule risk management

**Variant 2 evidence:** M5 risk notes (Section 3.5): "build a 1-week buffer into the schedule (hidden from the public timeline) between Beta and GA" (line 364).

**Why this is superior:** Beta phases regularly surface issues that need remediation time. A roadmap that schedules Beta end directly against GA commit date with zero buffer is setting up a forced choice between shipping known issues or slipping the GA date publicly. Variant 2's hidden buffer is a standard project management technique that absorbs discovery without external date slips. Variant 1 has no buffer.

**Diff point:** U-028, C-029.

### Strength 10: M3 and M4 parallelization reduces critical path

**Variant 2 evidence:** Section 6.1 critical path diagram shows M3 and M4 running in parallel: "Sprint 5-6: M3 (Password Reset)" and "Sprint 7-8: M4 (Frontend)" with a note: "M4 frontend development can begin in Sprint 5-6 in parallel with M3, using M2's completed API endpoints for LoginPage, RegisterPage, and AuthProvider. Only the password reset page depends on M3's reset-request endpoint." Dependency matrix confirms: "M3 reset-request endpoint" is a SOFT dependency on M4, not hard.

**Why this is superior:** Variant 1 Section 6.4 states M4 is blocked by both M2 AND M3 ("M4 blocked by M2, M3"). This forces fully sequential execution: M1 -> M2 -> M3 -> M4 -> M5. But LoginPage, RegisterPage, and AuthProvider only need M2's endpoints (`/auth/login`, `/auth/register`, `/auth/refresh`, `/auth/me`). Only the password reset page (`/forgot-password`, `/reset-password`) needs M3. By identifying M3's dependency on M4 as soft (partial), Variant 2 enables frontend development to start 4 weeks earlier, shortening the overall critical path.

**Diff point:** S-017, Section 6.3 of V2 vs Section 6.4 of V1.

---

## Weaknesses Identified in Variant 1 (with evidence)

### Weakness 1: Infeasible legacy auth rollback path on a greenfield project

**Variant 1 evidence:** Section 12.2 rollback procedure, step 2: "Flip AUTH_NEW_LOGIN OFF -- traffic routes back to legacy auth" (line 664). Step 3: "Smoke-test legacy login flow."

**Why this is a problem:** The source PRD Executive Summary (line 49) states: "The platform currently operates without any user identity system." The Problem Statement (line 68): "Every visitor is anonymous, creating three critical business problems." There is no legacy auth. Rolling back to a system that does not exist is impossible. If the team follows V1's rollback procedure during an actual incident, step 2 will fail because there is no legacy auth to route to, and the team will be left without a working rollback plan during an active incident. This is not a theoretical concern -- the TDD Section 19.3 rollback procedure references "legacy auth" as a fallback, and the PRD explicitly rules it out.

**Diff point:** X-004, C-022.

### Weakness 2: No measurable buffer in an 11-week plan with 2-week milestones

**Variant 1 evidence:** Section 2.2 phase map shows 11 weeks of milestones with zero buffer weeks. Each milestone is exactly 10 working days. The "2-week stabilization tail" (Week 12-13) occurs after GA, not before.

**Why this is a problem:** The TDD Section 17 benchmarks bcrypt cost-12 at ~300ms. The PRD NFR-PERF-001 requires <200ms p95. Variant 1's own risk R-104 rates this as Medium probability, Medium impact. If the bcrypt benchmark in M1 Week 1 shows that cost-12 cannot meet the latency budget, the mitigation is "drop to cost 11 with documented rationale." But dropping cost factors, re-benchmarking, and getting security sign-off takes time that is not budgeted in the 10-day M1 window. Any single milestone slipping by even 2-3 days cascades through the entire chain (M1 -> M2 -> M3 -> M4 -> M5) because V1's milestones are fully sequential with no float. The TDD's milestone dates (Section 23.1) are targets, not commitments -- a roadmap should add schedule risk management, not just transcribe dates.

**Diff point:** C-001, C-002, X-001.

### Weakness 3: No post-GA planning leaves product roadmap continuity undefined

**Variant 1 evidence:** Variant 1 has no section equivalent to V2's Section 13 "Post-GA Considerations." Out of Scope items (Section 10) reference "v1.1 roadmap" and "v1.2 roadmap" but provide no dates, sequencing, or feature prioritization.

**Why this is a problem:** The PRD Non-Goals explicitly version future work: "OAuth/OIDC... planned for v2.0" and "MFA... planned for v1.1." A roadmap that names these versions without providing any timeline fails to support downstream planning. The engineering team needs to know whether to architect for MFA in 3 months or 12 months. The product team needs to know when to schedule the OAuth dependency. The compliance team needs to know when GDPR right-to-erasure will be addressed (a "hard legal obligation" per V1's own OQ-R3). Without post-GA dates, every stakeholder is planning in a vacuum.

**Diff point:** S-013.

### Weakness 4: No dedicated admin audit log query deliverable

**Variant 1 evidence:** Section 13 personas coverage check lists "Jordan (admin): Audit logs and lockout signals" but no deliverable in any milestone provides a query interface. The audit log schema (D-102) creates the table. The audit events (D-206, D-306) populate it. But no deliverable provides a way to query it.

**Why this is a problem:** The PRD User Story for Jordan states: "Logs include user ID, event type, timestamp, IP address, and outcome. Queryable by date range and user." Without a query interface deliverable, Jordan cannot fulfill the JTBD: "When a security incident occurs, I want to see who attempted access and lock compromised accounts." An audit log table that exists in the database but has no query endpoint is not usable by Jordan. This is a gap in persona coverage -- V1's own Section 13 claims Jordan is served but omits the deliverable that would serve him.

**Diff point:** C-018, U-027.

### Weakness 5: Missing concrete staffing plan prevents resource planning

**Variant 1 evidence:** Section 14: "Engineering: 2 backend + 1 frontend FTE + 0.5 SRE + 0.25 security review" (line 709).

**Why this is a problem:** This single-row staffing estimate does not specify when each person is needed. The frontend engineers are needed for M4 (weeks 7-8) but not M1-M3. The SRE is needed for infrastructure provisioning in M1, K8s manifests in M2, and production deployment in M5. Without sprint-level allocation, a manager cannot:

1. Request headcount for the right time window
2. Stagger contractor start dates to minimize cost
3. Identify when the team is under- or over-staffed

This is a roadmap, not an architecture document. Its primary purpose is to coordinate people and time. A staffing plan that does not specify when people are needed fails at that primary purpose.

**Diff point:** S-012.

### Weakness 6: Audit log placement in M1 creates a TDD/PRD conflict that is handled inconsistently

**Variant 1 evidence:** D-102 places the audit log table in M1 with "90-day retention job spec." CC1 SEC-3 then says: "verify the 12-month retention (PRD) reconciles with the TDD's 90-day retention; gap resolution: bump audit log retention to 12 months in D-102 to satisfy the SOC2 row."

**Why this is a problem:** While I acknowledge V1's strength in flagging the conflict (OQ-R1), the resolution is internally inconsistent. D-102 is specified as having "90-day retention" in the deliverable text, but SEC-3 says to "bump" it to 12 months. The deliverable and the workstream item contradict each other. Which does the developer implement? Additionally, the 12-month retention creates a storage cost that is not reflected in the cost plan (Section 14: $450/month). At a conservative 100 auth events per user per month and 10,000 users, 12 months of audit logs is ~12M rows, which at ~500 bytes per row is ~6 GB of storage -- not free, and not accounted for.

**Diff point:** C-005, X-008.

---

## Concessions

I acknowledge the following genuine weaknesses in Variant 2:

### Concession 1: Duration labeling is internally inconsistent

Variant 2 Section 11 states "Total Duration: 22 weeks (~5.5 months), Sprint 1 through Sprint 11" and labels milestones as "Sprint 1-2, weeks 1-4" (M1), "Sprint 3-4, weeks 5-8" (M2), etc. However, the actual target dates -- M1: 2026-04-14, M2: 2026-04-28, M3: 2026-05-12, M4: 2026-05-26, M5: 2026-06-09 -- are identical to the TDD Section 23.1 dates and imply approximately 11 weeks of calendar time, not 22. The "22 weeks" label is misleading. If the roadmap is read naively (22 weeks starting from Sprint 1), the GA date would land in November 2026, not June 2026. This labeling error undermines confidence in the document and should be corrected to align the sprint counts with the actual calendar dates.

### Concession 2: Audit log deferred to M3 creates a SOC2 coverage gap

Variant 2 places the audit log table in M3 (D-028), meaning login, registration, and token refresh events in M1 and M2 are not captured in a structured audit log for approximately 8-12 weeks. The PRD Constraints section states: "All auth events must be logged for SOC2 audit trail requirements." Deferring audit infrastructure to M3 means this constraint is violated during M1 and M2. While structured logging (M2 deliverables D-022, observability workstream Sprint 2) captures events in application logs, application logs are not a substitute for a dedicated audit log table with enforced retention. This is a genuine compliance gap that should be addressed, potentially by creating a minimal audit table in M1 and enriching it in M3.

### Concession 3: No state machine formalization

Variant 2 does not include formal state machine definitions for refresh tokens, account lockout, or password reset tokens. Variant 1's Section 9 provides explicit states, transitions, guards, and concurrency rules. Without these, a developer implementing `TokenManager.refresh()` in M2 might not know that a rotated-then-reused token should revoke the entire family lineage. The absence of state machines in the roadmap shifts the burden of defining these transitions to the implementer at coding time, which increases the risk of inconsistent implementations across the team.

### Concession 4: Missing enumeration timing variance targets

Variant 2's edge case table (Section 7.3) states "identical response" for enumeration scenarios but provides no timing variance target. Variant 1 QA-6 enforces <50ms variance (login) and <30ms variance (reset-request). Without a measurable target, "identical" is an aspiration, not a test gate. An implementation that returns 401 in 5ms for wrong-email and 310ms for wrong-password technically returns "identical" responses but is trivially distinguishable via timing side-channel.

### Concession 5: No chaos testing track

Variant 2 mentions integration tests against real PostgreSQL and Redis but does not include a chaos engineering track equivalent to V1's QA-7 (Redis down, PostgreSQL failover, SendGrid down). The rollback procedure (Section 12.1) describes what to do when Redis is unavailable, but without a chaos test that simulates the failure, the team cannot verify the fallback behavior works before production.

---

## Shared Assumption Responses (MANDATORY)

**A-005**: NTP synchronization on all AuthService nodes is operational. Without it, JWT validation fails unpredictably.

- VERDICT: ACCEPT
- RATIONALE: Both variants depend on 5-second clock skew tolerance (TDD Section 12). This requires NTP. Without NTP, tokens issued by one node may be rejected by another, causing intermittent 401s that are extremely difficult to diagnose. The assumption is valid and necessary.

**A-008**: Frontend is a React SPA with React Router (or equivalent) supporting context providers and protected routes. If the frontend is a different framework, the M4 deliverables change entirely.

- VERDICT: ACCEPT
- RATIONALE: Both variants describe `AuthProvider` context, `LoginPage`, `RegisterPage`, and `ProfilePage` as React component patterns. The TDD Section 10 defines `AuthProvider` with `children: ReactNode`. This is React-specific. If the frontend is Angular or Vue, M4 deliverables are fundamentally different. The assumption is well-grounded in the source TDD.

**A-009**: No server-side session affinity is required. If session affinity is needed for any reason, the HPA scaling model breaks.

- VERDICT: ACCEPT
- RATIONALE: JWT-based stateless authentication is the explicit architectural choice (TDD Section 6.4: "JWT enables stateless verification across services"). Redis-backed refresh tokens do not require sticky sessions. The HPA scaling model (3 replicas baseline, scale to 10 at CPU > 70%) assumes any pod can serve any request. Session affinity would break this.

**A-010**: A named security reviewer (sec-reviewer) is allocated at >= 25% capacity during review gates. If unavailable, the gate cannot pass and M5 GA is blocked.

- VERDICT: ACCEPT
- RATIONALE: Both variants have security review gates. Variant 2 places security review in Sprint 9-10. Variant 1 places it at M2, M4, and M5 gates. Both require a named reviewer with sufficient allocation. If the security reviewer is shared across multiple projects and unavailable, the gate blocks. This is a valid dependency that should be surfaced. Variant 2's team composition table (Section 10.1) already accounts for this: Security Engineer at 25% for Sprint 1-2 and Sprint 9-10.

**A-011**: bcryptjs (JavaScript) is the password hashing library. If the team evaluates argon2id (mentioned in V1 as future migration target), that is a v1.1+ concern.

- VERDICT: ACCEPT
- RATIONALE: TDD Section 6.4 explicitly selects "bcrypt via PasswordHasher" with "bcryptjs" as the library. Both variants use cost factor 12. argon2id is mentioned in Variant 1 as a future migration target (consistent with the TDD's "pluggable interface for future argon2id migration"). v1.0 ships with bcryptjs. This is not contested.

**A-012**: Redis memory is provisioned for auth-specific workloads only (~100K tokens at 1 GB). If other services share the Redis instance, capacity planning is invalid.

- VERDICT: QUALIFY
- RATIONALE: Variant 2 adds Bull/BullMQ (a Redis-backed job queue) for async email delivery (OQ-A recommendation, Section 9.1). Bull/BullMQ stores job metadata in Redis, consuming additional memory beyond refresh tokens. If the job queue is co-located on the same Redis instance, the 1 GB capacity estimate (TDD Section 25.3: "~100K refresh tokens, ~50 MB") does not account for queue overhead. The capacity planning should be updated to include both refresh token storage and job queue storage, or the job queue should be provisioned on a separate Redis namespace/instance. This qualification does not invalidate the assumption but requires a capacity adjustment if Variant 2's async email recommendation is adopted.

---

## Per-Diff-Point Position Tally

| Point | Topic | Winner (V2 advocate position) | One-sentence rationale |
|-------|-------|-------------------------------|----------------------|
| C-001 | Total roadmap duration | Tie (with V2 labeling concession) | Both variants hit the same TDD-mandated GA date; V2's "22 weeks" label is a documentation error, not a schedule difference. |
| C-002 | Per-milestone duration | V1 | V1's 2-week milestones match the TDD's fortnightly cadence; V2's 4-week-per-milestone claim contradicts its own target dates. |
| C-003 | Lockout placement | V2 | Public-facing login endpoint without lockout for 4-8 weeks is an unmitigated brute-force risk that contradicts the TDD's explicit security consideration. |
| C-004 | Audit log placement | V1 | SOC2 audit trail from day 1 (V1) is more compliant than deferring to M3 (V2), though V2's structured logging partially mitigates. |
| C-005 | Audit retention conflict | V1 | V1 flags the TDD/PRD conflict explicitly; V2 silently overrides TDD's 90-day figure. |
| C-006 | Reset token storage | Tie | Redis TTL auto-expiry (V1) vs database hashed storage (V2) are both valid; trade-offs are architectural, not roadmap-level. |
| C-007 | Max refresh tokens | V2 | V2's 10-token cap with eviction (OQ-B) provides a concrete v1.0 policy; V1's "no cap, observe" defers a decision that affects storage sizing. |
| C-009 | Token family concept | V1 | V1's formal token family lineage with reuse detection is a security enhancement that V2 omits entirely. |
| C-014 | Chaos testing | V1 | V1's QA-7 chaos track tests failure modes before production; V2 has no equivalent. |
| C-015 | Enumeration timing | V1 | V1's <50ms/<30ms variance targets are measurable gates; V2's "identical response" is untestable as specified. |
| C-018 | Admin audit query | V2 | V2 D-030 provides a concrete deliverable for Jordan; V1 mentions the need but has no dedicated deliverable. |
| C-022 | Legacy auth assumption | V2 | V2 correctly identifies greenfield per PRD; V1's legacy rollback path is infeasible. |
| C-029 | Beta buffer | V2 | V2's hidden 1-week buffer is standard schedule risk management absent in V1. |
| S-007 | State machines | V1 | V1's formal state machines prevent ambiguous implementation; V2 lacks them entirely. |
| S-009 | Governance cadence | V1 | V1's communication cadence table operationalizes the roadmap; V2 has no equivalent. |
| S-012 | Team composition | V2 | V2's 10-row sprint-window staffing plan is actionable; V1's single-row estimate is not. |
| S-013 | Post-GA planning | V2 | V2's v1.1/v2.0 planning provides product continuity; V1 has none. |
| U-001 | State machine formalization | V1 | Significant value -- prevents ambiguous token lifecycle implementation. |
| U-002 | Token family concept | V1 | Security-relevant design decision absent from V2. |
| U-005 | Chaos testing | V1 | Validates failure-mode handling before production. |
| U-022 | Team composition detail | V2 | Actionable staffing plan that a manager can use for hiring and allocation. |
| U-023 | Post-GA v1.1/v2.0 planning | V2 | Prevents orphan release; provides product roadmap continuity. |
| U-025 | Greenfield assumption | V2 | Correctly eliminates infeasible legacy rollback path. |
| U-027 | Admin audit log query | V2 | Serves Jordan persona with a concrete deliverable. |
| X-001 | Duration contradiction | V1 wins on clarity | V2's "22 weeks" label contradicts its own target dates; V1 is internally consistent. |
| X-003 | Audit log milestone gap | V1 | SOC2 coverage from day 1 is correct; V2's M1/M2 gap violates PRD constraint. |
| X-004 | Legacy auth contradiction | V2 | V1's rollback procedure references a non-existent legacy system; V2's greenfield assumption is correct per PRD. |
