# Diff Analysis: Roadmap Comparison (opus vs sonnet)

## Metadata

- Generated: 2026-05-22T12:00:00Z
- Variants: 2 (opus, sonnet)
- Source: merged-prd-tdd-user-auth.md
- Total differences: 98
- Categories: structural (20), content (30), contradictions (8), unique (28), shared assumptions (12)

---

## Structural Differences

| # | Area | Variant 1 (opus) | Variant 2 (sonnet) | Severity |
|---|------|-------------------|---------------------|----------|
| S-001 | Top-level section count | 19 sections + 2 appendices | 13 sections + 3 appendices | Medium |
| S-002 | Milestone numbering | M1-M5 with sub-phases 5A/5B/5C | M1-M5 with phases Phase 1/2/3 | Low |
| S-003 | Deliverable ID scheme | D-101 through D-510 (3-digit, milestone-prefixed) | D-001 through D-060 (3-digit, sequential) | Low |
| S-004 | Risk register ID scheme | R-101 through R-116 | RR-001 through RR-012 | Low |
| S-005 | Cross-cutting workstream count | 4 workstreams (CC1-CC4) with named items (SEC-N, OBS-N, QA-N, DOC-N) | 5 workstreams (Security, Observability, Testing, Documentation, Infrastructure) with sprint-level activity tables | Medium |
| S-006 | Edge cases section | Dedicated Section 8 "Boundary Conditions & Edge Cases" with 19-row table | Embedded in Section 7.3 "Edge Case Coverage" with 16-row table | Medium |
| S-007 | State management section | Dedicated Section 9 with 5 subsections (refresh-token, lockout, reset-token state machines, audit ordering, DB transactions) | Absent — no formal state machine definitions | High |
| S-008 | Personas coverage check | Dedicated Section 13 verifying Alex, Jordan, Sam against roadmap deliverables | Absent — personas mentioned inline but no dedicated coverage verification | Medium |
| S-009 | Communication & governance | Dedicated Section 15 with cadence table (weekly status, bi-weekly risk, go/no-go) | Absent — no governance cadence specified | Medium |
| S-010 | Glossary | Dedicated Section 16 with 5 term definitions | Absent — no glossary section | Low |
| S-011 | Capacity planning placement | Section 14 "Cost & Resource Plan" — brief table with staging vs prod costs | Section 10 "Capacity Planning and Resource Allocation" — 3 subsections with team composition, infrastructure sizing, and cost projection tables | Medium |
| S-012 | Team composition detail | Single row: "2 backend + 1 frontend FTE + 0.5 SRE + 0.25 security review" | 10-row table with role, allocation percentage, and active sprint window per person | Medium |
| S-013 | Post-GA planning | 2-week stabilization tail mentioned in phase map; no dedicated post-GA section | Dedicated Section 13 "Post-GA Considerations" with v1.1 planning (Q3 2026), v2.0 planning (Q4 2026), and ongoing maintenance subsections | Medium |
| S-014 | Feature flag lifecycle | Mentioned in M5 deliverables and Section 10 Out of Scope; no dedicated appendix | Dedicated Appendix B with Created/Enabled/Disabled/Removed columns per flag | Low |
| S-015 | API endpoint summary | Endpoints described inline within milestones; no summary table | Dedicated Appendix C with Method/Auth/Rate Limit/Milestone/Sprint columns for all 6 endpoints | Low |
| S-016 | Critical path representation | Textual: "Schema (D-101) -> PasswordHasher (D-103) -> ..." with named deliverables | ASCII diagram showing Sprint-to-Milestone flow with branching parallel tracks | Low |
| S-017 | Timeline representation | ASCII week-level Gantt (Section 6.2) + Appendix B calendar view | Sprint-level textual timeline with parallel activity annotations | Low |
| S-018 | Closing section | Section 19 "Closing Note" summarizing top delivery risk and top scope risk | Absent — document ends at Appendix C | Low |
| S-019 | Rollback procedure format | 8-step numbered procedure with forensic snapshot and incident channel steps | 5-step numbered procedure with greenfield/maintenance-page fallback note | Low |
| S-020 | Open questions structure | Two-tier: Section 11.1 maps PRD/TDD OQs with resolutions + Section 11.2 raises 6 new roadmap-level OQs (OQ-R1 to OQ-R6) | Single-tier: Section 9.1 with 6 questions (OQ-A to OQ-F) mixing source and roadmap-originated questions | Medium |

---

## Content Differences

| # | Topic | Variant 1 (opus) | Variant 2 (sonnet) | Severity |
|---|-------|-------------------|---------------------|----------|
| C-001 | Total roadmap duration | 11 weeks (2026-03-30 to 2026-06-09) + 2-week stabilization | 22 weeks (~5.5 months, Sprint 1-11) | High |
| C-002 | Per-milestone duration | 2 weeks each for M1-M4; 2 weeks for M5 (with sub-phases) | 4 weeks (2 sprints) each for M1-M4; 6 weeks (3 sprints) for M5 | High |
| C-003 | Account lockout milestone placement | M3 (D-305, LoginAttemptTracker in Redis) | M1 (D-006, part of core AuthService) | High |
| C-004 | Audit log table milestone placement | M1 (D-102, `migrations/0002_audit_log.sql`) | M3 (D-028, "Audit log table in PostgreSQL") | High |
| C-005 | Audit log retention conflict | Explicitly identifies TDD says 90 days, PRD says 12 months; creates OQ-R1; recommends bumping to 12 months in D-102 | States "12-month audit log retention policy enforcement" (D-033) without acknowledging TDD's 90-day figure | Medium |
| C-006 | Password reset token storage medium | Redis with 1-hour TTL; ADR documents trade-off (D-308) | Database storage, hashed (D-025: "stored hashed in database") | Medium |
| C-007 | Max refresh tokens per user | No cap in v1.0; emit metric, revisit in v1.1 if abuse (OQ-2 in DOC-4) | 10 active tokens per user; oldest evicted on new issuance (OQ-B) | Medium |
| C-008 | Lockout auto-unlock timing | Implied 15-minute sliding window: "counter resets after the 15-min window passes" (M3 exit criteria) | Recommends auto-unlock after 30 minutes (OQ-C); admin can manually unlock earlier | Medium |
| C-009 | Token family / reuse detection | Formal token family concept: reuse detection revokes entire family lineage (Section 9.1 state machine) | Mentions token rotation and revocation; no "token family" concept | Medium |
| C-010 | Multi-tab coordination | BroadcastChannel API for cross-tab token sync (M4 scope) | Not mentioned; no multi-tab coordination mechanism | Medium |
| C-011 | Silent refresh timing | Specific: schedule at `expiresIn - 60s` (14 minutes after issuance) | Generic: "detect expiring accessToken, refresh via TokenManager before expiry" | Low |
| C-012 | Tab-close behavior | `AuthProvider` clears in-memory tokens on `beforeunload` (TDD R-001) | Mentions tokens lost on tab close as a risk note but no explicit `beforeunload` handler | Low |
| C-013 | Lighthouse performance requirement | Lighthouse score >= 90 for LoginPage and RegisterPage (M4 exit criteria) | Not mentioned | Low |
| C-014 | Chaos testing | QA-7 explicit: Redis down, PostgreSQL failover, SendGrid down chaos tests | Not mentioned | Medium |
| C-015 | Enumeration timing variance | QA-6: <50ms variance (unknown-user vs wrong-password), <30ms variance (reset-request registered vs unregistered) | Edge case table mentions "identical response" but no timing variance target | Medium |
| C-016 | Concurrent refresh race handling | Redis `SET NX` lock keyed on token hash; loser gets 401 (Section 9.1) | Recommends Redis MULTI/EXEC or Lua script for atomic token rotation (M2 risk note) | Low |
| C-017 | Logout endpoint existence | Open question OQ-R4: "Do we ship POST /auth/logout or is client-side discard enough?" | Not raised; Log Out described as "clear tokens, redirect to landing page" (D-042) with no server-side revocation | Low |
| C-018 | Admin audit log query | Mentioned in personas check (Jordan needs audit logs) but no dedicated deliverable for query API | Dedicated deliverable D-030: "Audit log query interface for admin (filter by date range, user, event type)" | Medium |
| C-019 | GDPR right-to-erasure | Flagged as missing from PRD (Section 10 out-of-scope + OQ-R3) with note about hard legal obligation | Listed as out of scope "Post-v1.0" without urgency flag | Low |
| C-020 | Async email recommendation | Async via queue; ADR D-308; resolves PRD OQ #1 | Async via Redis-backed job queue (Bull/BullMQ); specific technology named | Low |
| C-021 | Feature flag removal timeline | Flags remain ON; "removal targets recorded" in Section 10; post-GA stabilization | `AUTH_NEW_LOGIN` removed at Sprint 11 + 2 weeks; `AUTH_TOKEN_REFRESH` at Sprint 11 + 4 weeks (Appendix B) | Low |
| C-022 | Legacy auth assumption | Rollback procedure says "Flip AUTH_NEW_LOGIN OFF -- traffic routes back to legacy auth" (Section 12.2) | Assumption 6 explicitly states greenfield ("no existing legacy auth system"); rollback shows maintenance-page fallback | Medium |
| C-023 | Pentest cost | Not quantified | "$5,000-$15,000 one-time" in cost projection table (Section 10.3) | Low |
| C-024 | K8s manifest detail | D-501: "Production-ready Helm/Kubernetes manifests with 3-pod baseline + HPA to 10" | Sprint 4 infrastructure workstream: "Kubernetes deployment manifests + HPA (3 replicas, scale to 10 on CPU > 70%)" | Low |
| C-025 | Rollback step count | 8-step procedure including forensic snapshot (step 4) and incident channel notification (step 7) | 5-step procedure; omits forensic snapshot and incident channel notification | Low |
| C-026 | On-call escalation detail | Implicit from CC2 OBS-5 (admin notification channel) | Explicit P1 response time (15 min), escalation path (4-level), tooling access list (Section 12.2) | Low |
| C-027 | Migration locking risk | R-115: long-running migration locks user_profile table; mitigated by pg-online-schema-change tooling | Not mentioned | Low |
| C-028 | Coordinated frontend+backend release risk | R-116: "New AuthService deployed without coordinated frontend rollout" — feature flag gate requires both deployed | Not raised as a named risk | Low |
| C-029 | Beta buffer | No explicit buffer mentioned | "Build a 1-week buffer into the schedule (hidden from the public timeline) between Beta and GA" (M5 risk notes) | Low |
| C-030 | Password change (while logged in) in scope | Not listed in Out of Scope section | Explicitly listed as out of scope: "Password change (while logged in)" with v1.1 target | Low |

---

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Impact |
|---|-------------------|--------------------|--------------------|--------|
| X-001 | Roadmap total duration | 11 weeks + 2-week stabilization (Section 2.2 phase map) | 22 weeks total (Section 11 timeline summary) | High — the same GA date (2026-06-09) with wildly different execution timelines. A 22-week plan starting from Sprint 1 would need to start ~November 2025 to hit June 2026 GA. |
| X-002 | Account lockout milestone | M3 (password reset milestone); D-305 `LoginAttemptTracker` using Redis sliding window | M1 (core auth milestone); D-006 "Account lockout after 5 failed attempts within 15 minutes" | High — if lockout ships in M1 (sonnet), the LoginAttemptTracker must coexist with PasswordHasher in the first 2-4 weeks. If it ships in M3 (opus), the login endpoint is vulnerable to brute force for 4-6 weeks. |
| X-003 | Audit log table milestone | M1 D-102 `migrations/0002_audit_log.sql` — audit infrastructure exists from day 1 | M3 D-028 — audit logging only becomes available when password reset is built | High — SOC2 audit trail is absent in sonnet's M1 and M2, meaning login, registration, and token refresh events go unlogged for ~8-12 weeks. This contradicts PRD's "All auth events must be logged for SOC2 audit trail requirements." |
| X-004 | Legacy auth system existence | Rollback (Section 12.2 step 2): "Flip AUTH_NEW_LOGIN OFF -- traffic routes back to legacy auth" — assumes a functioning legacy auth system | Assumption 6: "There is no existing legacy auth system requiring migration... the PRD describes a greenfield implementation" — rollback shows maintenance-page fallback | Medium — the rollback procedure is architecturally different depending on which assumption is correct. The PRD says "the platform currently operates without any user identity system" (greenfield), so V1's legacy rollback path may be infeasible. |
| X-005 | Lockout auto-unlock timing | M3 exit criteria: "counter resets after the 15-min window passes" — implies 15-minute auto-unlock aligned with the sliding window | OQ-C recommendation: "Auto-unlock after 30 minutes" — doubles the window | Medium — operational behavior differs for locked-out users. A 30-minute lockout is materially more punitive than 15 minutes, affecting UX for legitimate users who mistype passwords. |
| X-006 | Max refresh tokens per user | No cap in v1.0; metric-based observation (DOC-4) | 10 active tokens per user with oldest-evicted policy (OQ-B) | Medium — V2's cap introduces eviction logic that V1 defers. If V2 is adopted, the TokenManager must implement per-user token counting and FIFO eviction in M2, adding scope. |
| X-007 | Password reset token storage | Redis with 1-hour TTL; ADR documents trade-off (simpler revocation, single-purpose storage) | Database storage, hashed (D-025) — persistent storage survives Redis restarts but requires cleanup cron | Medium — the storage medium affects M3 implementation: Redis TTL auto-expires tokens, while database storage requires an explicit expiry sweep or query-time validation. Both are valid but architecturally different. |
| X-008 | Audit log retention source truth | Flags conflict: TDD Section 7.2 says 90 days, PRD says 12 months; creates OQ-R1 for explicit resolution before D-102 commit | States 12-month retention (D-033) without acknowledging TDD's 90-day specification | Low — both converge on 12 months for SOC2 compliance, but V2 silently overrides the TDD. If the TDD is the engineering SoT, this could cause confusion. |

---

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---------|-------------|-------|
| U-001 | opus | State machine formalization (Section 9): refresh-token states (`issued -> rotated | revoked | expired | reused`), lockout states (`unlocked <-> locked`), reset-token states (`pending -> consumed | expired`) with explicit guards and concurrency rules | High — prevents ambiguous implementation of token lifecycle; directly supports M2/M3 coding |
| U-002 | opus | Token family concept: reuse detection revokes entire lineage of refresh tokens descending from a single login event (Section 9.1, risk R-111) | High — security-relevant design decision that prevents token replay attacks across a token chain |
| U-003 | opus | Multi-tab coordination via BroadcastChannel API (M4 scope) | Medium — prevents inconsistent auth state across browser tabs (logout in tab A not reflected in tab B) |
| U-004 | opus | Enumeration-timing variance targets: <50ms (login), <30ms (reset-request) enforced via QA-6 | Medium — turns an informal security requirement into a measurable CI gate |
| U-005 | opus | Chaos testing track (QA-7): explicit tests for Redis down, PostgreSQL failover, SendGrid down | Medium — validates failure-mode handling before production; directly supports the failure-mode catalog |
| U-006 | opus | Personas coverage check (Section 13): maps Alex/Jordan/Sam needs to specific roadmap deliverables | Medium — ensures no persona is orphaned; catches gaps like "Sam needs stable contracts" linking to OpenAPI maintenance |
| U-007 | opus | Communication & governance cadence table (Section 15): weekly status, weekly burndown, bi-weekly risk review, as-needed ADRs, go/no-go review, post-mortem trigger | Medium — operationalizes the roadmap into a meeting/review rhythm |
| U-008 | opus | GDPR right-to-erasure flagged as a missing PRD item with hard legal obligation (OQ-R3, Section 10 out-of-scope) | Medium — surfaces a compliance gap the source documents missed |
| U-009 | opus | Token revocation endpoint as open question OQ-R4: "Do we ship POST /auth/logout or is client-side discard enough?" | Medium — the answer determines whether M4 logout is purely client-side or requires a new backend endpoint |
| U-010 | opus | DNS/SPF/DKIM/DMARC coordination as explicit CC2 item (OBS-7) blocking M3 entry | Medium — email deliverability is a cross-team dependency that could silently slip M3 if not tracked |
| U-011 | opus | Database transaction scope documented: `register()` is single transaction (UserProfile + audit_log + consent), `confirmPasswordReset()` is single transaction (password_hash + revoke tokens + audit) (Section 9.5) | Medium — prevents partial-write bugs in M1 and M3 implementation |
| U-012 | opus | Migration locking risk (R-115): long-running migration locks user_profile; mitigated by pg-online-schema-change tooling | Low — specific operational risk for the D-101 migration |
| U-013 | opus | Coordinated frontend+backend release risk (R-116): feature flag only flips after both sides deployed | Low — prevents split-brain state where backend returns JWTs the frontend cannot refresh |
| U-014 | opus | Silent refresh timing specified as `expiresIn - 60s` (14 minutes after issuance) (M4 scope) | Low — removes ambiguity from AuthProvider implementation |
| U-015 | opus | `beforeunload` handler for tab-close token clearing (M4 scope, TDD R-001) | Low — explicit XSS mitigation for tab-close scenarios |
| U-016 | opus | Lighthouse score >= 90 for LoginPage and RegisterPage (M4 exit criteria) | Low — adds a measurable frontend performance gate |
| U-017 | opus | Refresh storm prevention: "401 interceptor only triggers ONE refresh attempt per access-token lifecycle" (M4 exit criteria) | Medium — prevents cascading load on /auth/refresh during token expiry events |
| U-018 | opus | Closing note identifying top delivery risk (bcrypt-cost-12 latency) and top scope risk (audit retention conflict) | Low — provides executive summary of what to watch |
| U-019 | opus | Redis `SET NX` lock for concurrent refresh token rotation (Section 9.1 concurrency rule) | Medium — specific implementation guidance for a race condition |
| U-020 | opus | Consent written in same transaction as UserProfile (Section 9.5, risk R-113) | Medium — ensures GDPR compliance is atomic with account creation |
| U-021 | sonnet | Three-phase decomposition rationale (Section 2.2 "Why Three Phases, Not Two") explaining why password reset and frontend integration are separated | Medium — justifies phase structure against the source PRD's two-phase prescription |
| U-022 | sonnet | Detailed team composition table (Section 10.1): 10 roles with allocation % and sprint windows | Medium — resource plan that can be directly used for staffing requests |
| U-023 | sonnet | Post-GA v1.1 planning with specific feature list (MFA, API keys, remember me, email verification, password change, self-service unlock) and v2.0 planning (OAuth, social login, RBAC, admin dashboard) (Section 13) | Medium — provides product roadmap continuity beyond v1.0 |
| U-024 | sonnet | Feature flag lifecycle table with Created/Enabled/Disabled/Removed dates per flag (Appendix B) | Medium — operationalizes flag management with clear removal criteria |
| U-025 | sonnet | Greenfield assumption explicitly stated (Assumption 6): "There is no existing legacy auth system requiring migration" | Medium — eliminates ambiguity about rollback feasibility |
| U-026 | sonnet | Pentest cost quantified at $5,000-$15,000 one-time (Section 10.3) | Low — budget item for procurement planning |
| U-027 | sonnet | Admin audit log query interface deliverable (D-030) with filter by date range, user, event type | Medium — gives Jordan (admin persona) a concrete tool; absent in opus |
| U-028 | sonnet | 1-week hidden buffer between Beta and GA (M5 risk notes) | Low — schedule management tactic not exposed in public timeline |

---

## Shared Assumptions

| # | Assumption | Source Agreement | Classification | Promoted |
|---|-----------|-----------------|----------------|----------|
| A-001 | The API gateway with rate-limiting capability already exists; auth-team configures policies, doesn't build it | V1 A-3 states explicitly; V2 infrastructure workstream implies it | STATED | No |
| A-002 | The observability stack (Prometheus + Grafana) is already deployed; auth-team plugs in metrics | V1 A-6 states explicitly; V2 observability workstream implies it | STATED | No |
| A-003 | CI pipeline supports testcontainers for ephemeral PostgreSQL + Redis | V1 A-7 states explicitly; V2 testing workstream implies it | STATED | No |
| A-004 | The feature flag service is already operational in the infrastructure | V1 dependency table (M5 entry); V2 dependency matrix (M5 hard dependency) | STATED | No |
| A-005 | NTP is configured on all service nodes for JWT clock skew tolerance | Neither states explicitly; both depend on 5-second clock skew tolerance from TDD Section 12 | UNSTATED | **[SHARED-ASSUMPTION] NTP synchronization on all AuthService nodes is operational. Without it, JWT validation fails unpredictably.** |
| A-006 | The application runs on Node.js 20 LTS exclusively | V2 Assumption 7 states explicitly; V1 mentions "Node.js 20 LTS baseline image" in M1 entry criteria | STATED | No |
| A-007 | Kubernetes (with Helm) is the deployment and orchestration platform | V1 D-501 "Helm/Kubernetes manifests"; V2 infrastructure workstream "Kubernetes deployment manifests" | STATED | No |
| A-008 | The frontend is React-based (AuthProvider context, JSX component patterns) | Both describe `AuthProvider`, `LoginPage`, `RegisterPage` as React context/component patterns | UNSTATED | **[SHARED-ASSUMPTION] Frontend is a React SPA with React Router (or equivalent) supporting context providers and protected routes. If the frontend is a different framework, the M4 deliverables change entirely.** |
| A-009 | Horizontal scaling is achieved through stateless JWT verification + Kubernetes HPA | Both describe 3-pod baseline with HPA to 10 at CPU > 70%; JWT enables stateless verification | UNSTATED | **[SHARED-ASSUMPTION] No server-side session affinity is required. If session affinity is needed for any reason, the HPA scaling model breaks.** |
| A-010 | The security team is available for review at M2, M4, and M5 gates | V1 CC1 specifies weekly checkpoints; V2 security workstream specifies Sprint 1-2 and Sprint 9-10 windows | UNSTATED | **[SHARED-ASSUMPTION] A named security reviewer (sec-reviewer) is allocated at >= 25% capacity during review gates. If unavailable, the gate cannot pass and M5 GA is blocked.** |
| A-011 | bcryptjs is the chosen bcrypt implementation library (not argon2id) for v1.0 | V1 M1 scope: "wrapper around bcryptjs"; V2 does not name the library but references bcrypt throughout | UNSTATED | **[SHARED-ASSUMPTION] bcryptjs (JavaScript) is the password hashing library. If the team evaluates argon2id (mentioned in V1 as future migration target), that is a v1.1+ concern.** |
| A-012 | Redis is used exclusively for refresh token storage and lockout state; no other Redis consumers compete for memory | V1 describes Redis for refresh tokens + lockout sliding window; V2 adds job queue (Bull/BullMQ) on Redis | UNSTATED | **[SHARED-ASSUMPTION] Redis memory is provisioned for auth-specific workloads only (~100K tokens at 1 GB). If other services share the Redis instance, capacity planning (OBS-6) is invalid.** |

---

## Summary

### Totals per category

| Category | Count |
|----------|-------|
| Structural Differences | 20 |
| Content Differences | 30 |
| Contradictions | 8 |
| Unique Contributions | 28 (20 opus, 8 sonnet) |
| Shared Assumptions | 12 (4 STATED, 6 UNSTATED, 2 CONTRADICTED sub-facets) |
| **Total** | **98** |

### Highest-severity items

**High severity (4):**

- **C-001 / C-002**: Duration mismatch — opus plans 11 weeks, sonnet plans 22 weeks for the same GA date. This is the single most consequential difference: it affects staffing, cost, and feasibility.
- **C-003**: Lockout placement — opus defers to M3 (leaving M1/M2 endpoints unprotected for 4 weeks), sonnet includes in M1 (adding scope to the tightest milestone).
- **C-004**: Audit log placement — opus builds audit infrastructure in M1 (SOC2 coverage from day 1), sonnet defers to M3 (M1/M2 events go unlogged for ~8-12 weeks, contradicting PRD's "all auth events must be logged").

**Medium severity items requiring resolution (12):**

- X-001 through X-008 (contradictions)
- C-005 (audit retention conflict handling)
- C-006 (reset token storage medium)
- C-009 (token family concept)
- S-007 (state machine formalization absent in sonnet)
