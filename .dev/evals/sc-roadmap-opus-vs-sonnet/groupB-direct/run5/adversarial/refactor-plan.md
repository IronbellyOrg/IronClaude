# Refactoring Plan: Roadmap Merge

## Overview

- **Base variant:** Variant 1 (opus) — `variant-1-opus-default.md` (790 lines, 19 H2 sections)
- **Non-base variant:** Variant 2 (sonnet) — `variant-2-sonnet-default.md` (854 lines, 16 H2 sections)
- **Planned changes:** 12 V2-strength incorporations + 9 HIGH invariant fixes + 5 base-weakness fixes = **26 total changes**
- **Risk profile:** **Medium overall** — most incorporations are additive/low-risk; the 9 invariant fixes include 4 that restructure existing sections (High risk)
- **Status:** BLOCKED_BY_INVARIANTS at convergence — merge MUST address all 9 HIGH UNADDRESSED items before the result can be considered converged

---

## Section 1: V2 Strengths to Incorporate

### Change #1: Move Account Lockout from M3 to M1

- **Source:** V2 Section 3.1, deliverable D-006 (Sprint 1-2); V2 Section 4.1 Security Workstream row "Implement account lockout" Sprint 2
- **Target Location in V1 base:** V1 Section 3, Milestone M1 (currently no lockout deliverable) and Milestone M3 (D-305 `LoginAttemptTracker`)
- **Integration Approach:** restructure
  1. Move `LoginAttemptTracker` deliverable from M3 (D-305) to M1. Assign new D-ID within M1's numbering block (e.g., D-108). Preserve V1's Redis-sliding-window storage choice and V1's naming convention.
  2. Add Redis provisioning to M1 entry criteria (currently M1 entry has no Redis dependency; lockout-in-M1 requires Redis available from Week 1).
  3. Remove D-305 from M3 deliverables and M3 scope text. M3 scope text "Account-lockout policy" paragraph moves to M1 scope.
  4. Update M1 exit criteria to add: "Account locks after 5 failed logins within 15 minutes (423 response)."
  5. Update M3 exit criteria to remove the lockout-specific criteria (the "Lockout: 5 wrong-password attempts in 15 min returns 423" bullet).
  6. Update the internal-sequencing ASCII diagram (V1 Section 6.2) to show Redis dependency at M1 entry instead of M2 entry.
  7. Update V1 Section 6.1 External Dependencies table: add "Redis 7+ provisioned" to M1 entry row (currently M2 entry only).
- **Rationale:** C-003 won by V2 at 95% confidence (debate-transcript scoring matrix). V1 conceded in R1 and reaffirmed in R2. PRD R-002 co-requires lockout AND rate limiting, making M1 lockout a PRD compliance requirement, not a nice-to-have. V2's "20-30 LoC" argument makes the scope objection untenable. Leaving login unprotected for 4 weeks (M1-M2-M3) contradicts PRD R-002 mitigation.
- **Risk Level:** Medium — moves a Redis dependency into M1, tightening M1's entry criteria and adding ~20-30 LoC to the tightest milestone
- **Specific Edit Instructions:**
  - In V1 M1 scope block, after the password-policy-validator paragraph, insert: "Account-lockout policy: 5 failed logins in 15 minutes -> 423 Locked from /auth/login (PRD Error Handling table; TDD Section 13). Lockout state stored in Redis with sliding 15-minute window."
  - In V1 M1 deliverables table, add row: `| D-108 | Lockout module (LoginAttemptTracker) using Redis sliding window | auth-team |`
  - In V1 M1 entry criteria, add: "Redis 7+ instance provisioned in staging (required for lockout state storage)."
  - In V1 M1 exit criteria, add: "Account locks after 5 failed logins within 15 minutes; returns 423. Counter resets after 15-minute sliding window expires."
  - In V1 M3 scope, remove the "Account-lockout policy" paragraph entirely.
  - In V1 M3 deliverables, remove D-305 row.
  - In V1 M3 exit criteria, remove the lockout bullet.
  - In V1 Section 6.1 External Dependencies, change the Redis row from "M2 entry" to "M1 entry" and update the "Risk if missing" to "M1 lockout has no backing store; M1 blocked."
  - In V1 Section 6.2 ASCII diagram, add a Redis bracket starting at Week 1 instead of Week 3.

### Change #2: Greenfield-Correct Rollback Procedure

- **Source:** V2 Assumption 6 (Section 9.2, line 656); V2 Section 12.1 rollback steps (line 749: "All traffic routes back to legacy behavior (or, for greenfield, displays a maintenance page)")
- **Target Location in V1 base:** V1 Section 12.2 Rollback Procedure, step 2 (currently reads: "Flip AUTH_NEW_LOGIN OFF -- traffic routes back to legacy auth")
- **Integration Approach:** replace
  1. Replace V1 Section 12.2 step 2 with: "Flip `AUTH_NEW_LOGIN` OFF. Because this is a greenfield deployment (PRD: 'the platform currently operates without any user identity system'), there is no legacy auth to fall back to. Instead, display a maintenance page (503) at the gateway for all `/auth/*` routes until the issue is resolved."
  2. In V1 Section 11.3 Assumptions, add Assumption A-11: "There is no existing legacy auth system requiring migration. The PRD describes a greenfield implementation. Rollback strategy must account for this — there is no 'flip back to legacy' path."
- **Rationale:** C-022 won by V2 at 95% confidence. X-004 (contradiction) won by V2 at 95% confidence. V1 conceded in R1 (Concession 2) and R2 (P1-incident failure mode). PRD Executive Summary confirms greenfield. V1's rollback step 2 is infeasible in production — it would route traffic to a nonexistent legacy system, causing a P1 incident.
- **Risk Level:** Low — text replacement only, no structural changes
- **Specific Edit Instructions:**
  - In V1 Section 12.2, replace step 2 text "Flip `AUTH_NEW_LOGIN` OFF -- traffic routes back to legacy auth." with the greenfield-correct text above.
  - Add Assumption A-11 to V1 Section 11.3.

### Change #3: 10-Row Staffing Table

- **Source:** V2 Section 10.1 "Team Composition" (lines 670-683), 10-row table with Role / Allocation / Sprints Active columns
- **Target Location in V1 base:** V1 Section 14 "Cost & Resource Plan" (currently has a single row: "2 backend + 1 frontend FTE + 0.5 SRE + 0.25 security review")
- **Integration Approach:** replace
  1. Replace the single staffing row in V1 Section 14 with V2's 10-row table, adapted to V1's fortnightly milestone cadence (Sprint 1-6 instead of Sprint 1-11). Map V2's sprint windows to V1's weeks:
     - Backend Engineer 1 (AuthService + PasswordHasher): 100%, Week 1-8 (M1-M4)
     - Backend Engineer 2 (TokenManager + JwtService): 100%, Week 3-8 (M2-M4)
     - Backend Engineer 3 (Password reset + audit logging): 100%, Week 5-6 (M3 only — V1's 2-week M3 vs V2's 4-week M3)
     - Frontend Engineer 1 (LoginPage + RegisterPage): 100%, Week 7-8 (M4)
     - Frontend Engineer 2 (AuthProvider + ProfilePage + reset page): 100%, Week 7-8 (M4)
     - QA Engineer: 50% Week 1-4, 100% Week 5-11
     - Security Engineer: 25% Week 1-2 (policy) + Week 9-11 (review)
     - DevOps Engineer: 25% Week 1 (CI/CD), Week 3-4 (K8s), Week 9 (prod)
     - Product Manager: 10% Week 1-11
     - SRE (0.5 FTE): Week 9-13 (M5 + stabilization)
- **Rationale:** S-012 won by V2 at 95% confidence. V1 conceded in R1 (Concession 3) and R2. V1's single-row staffing is unactionable for staffing requests.
- **Risk Level:** Low — additive content, replaces a single summary line with a detailed table
- **Specific Edit Instructions:**
  - In V1 Section 14, after the cost/resource table, replace the single staffing row with the 10-row table above. Keep the cost rows (pods, PostgreSQL, Redis, SendGrid, monthly run-rate) unchanged.

### Change #4: Post-GA Planning Section

- **Source:** V2 Section 13 "Post-GA Considerations" (lines 776-801) with three subsections: v1.1 Planning (Q3 2026), v2.0 Planning (Q4 2026), Ongoing Maintenance
- **Target Location in V1 base:** New section to insert after current V1 Section 18 (Appendix B — Calendar) and before Section 19 (Closing Note). Alternatively, insert as Section 18.5 or renumber V1's closing sections.
- **Integration Approach:** insert
  1. Add a new section "Post-GA Considerations" between V1's Appendix B and Closing Note. Use V2's three-subsection structure.
  2. Tag quarter labels as "target" rather than firm commitments (per V1 R2 refinement).
  3. v1.1 list: MFA (NG-002), API key auth (OQ-001), "Remember me" (OQ-D), email verification, password change while logged in, account self-service unlock, GDPR right-to-erasure (promoted from "Post-v1.0" to named v1.1 item per INV-025).
  4. v2.0 list: OAuth2/OIDC (NG-001), social login, RBAC enforcement (separate PRD), admin dashboard.
  5. Ongoing Maintenance: quarterly RS256 key rotation, bcrypt cost review, SOC2 audit log retention verification, dependency updates, capacity review at 10K DAU.
- **Rationale:** S-013 won by V2 at 85% confidence. V1 conceded in R1 and R2 (adopt V2 structure, mark quarters as "target"). Provides product roadmap continuity beyond v1.0.
- **Risk Level:** Low — new section, does not modify existing content
- **Specific Edit Instructions:**
  - Insert a new H2 section "Post-GA Considerations" after Appendix B (Section 18). Renumber Closing Note from 19 to 20 (or adjust as needed to maintain V1's section numbering scheme).
  - Copy V2 Section 13 content, adapting sprint references to V1's week-based cadence.

### Change #5: Admin Audit Log Query Deliverable

- **Source:** V2 Section 3.3 deliverable D-030 (line 190): "Audit log query interface for admin (filter by date range, user, event type)"
- **Target Location in V1 base:** V1 Section 3, Milestone M3 deliverables table (add new row after D-306)
- **Integration Approach:** append
  1. Add new deliverable D-309 to M3: "Admin audit-log query endpoint (`GET /admin/audit-logs?from=&to=&user_id=&event_type=`) with pagination. Satisfies Jordan persona's 'view authentication event logs' user story."
  2. Update M3 exit criteria to add: "Audit logs queryable by date range, user ID, and event type via admin endpoint."
  3. Update V1 Section 13 Personas Coverage Check: Jordan row gains "M3 D-309 (admin audit query)" reference.
- **Rationale:** C-018 won by V2 at 90% confidence. V1 conceded in R1 (Concession 4) and R2. V2 D-030 is the correct Jordan-persona deliverable. V1 mentions Jordan needing audit logs in the personas check but has no corresponding deliverable.
- **Risk Level:** Low — additive deliverable to M3, ~1 day of additional scope
- **Specific Edit Instructions:**
  - In V1 M3 deliverables table, add row: `| D-309 | Admin audit-log query endpoint (GET /admin/audit-logs with date-range, user-ID, event-type filters + pagination) | auth-team |`
  - In V1 M3 exit criteria, add: "Admin audit-log query endpoint returns filtered, paginated results."
  - In V1 Section 13 Personas table, update Jordan row "Where in roadmap" column to: "M1 (audit-log schema D-102), M3 (lockout events D-306, admin audit query D-309), CC2 (dashboards)."

### Change #6: 10-Token FIFO Refresh Cap

- **Source:** V2 Section 9.1 OQ-B (line 639): "10 active refresh tokens per user. Oldest evicted on new issuance."
- **Target Location in V1 base:** V1 Section 3 Milestone M2 scope and deliverables; V1 Section 11.1 OQ-2 resolution; V1 Section 9.1 refresh-token state machine
- **Integration Approach:** restructure
  1. Update V1 OQ-2 resolution (Section 11.1) from "No cap in v1.0; emit metric and revisit in v1.1" to: "10 active refresh tokens per user. Oldest evicted on new issuance (FIFO). Covers typical multi-device usage."
  2. Add to M2 scope: "TokenManager enforces a per-user limit of 10 active refresh tokens. When an 11th token is issued, the oldest is evicted via FIFO. Eviction marks the token's family metadata as `evicted=true` to prevent false-positive family revocation (see INV-013 fix)."
  3. Add deliverable D-209 to M2: "Per-user token-count enforcement with FIFO eviction in TokenManager."
  4. Update V1 Section 9.1 refresh-token state machine: add `evicted` as a terminal state reachable from `issued`. Add guard: "evicted tokens with `evicted=true` metadata do NOT trigger family revocation on reuse — they emit a warning-level audit event instead."
  5. Update V1 Section 8 Boundary Conditions table: change "User logs in from 6th device while 5 sessions active" row to: "User logs in from 11th device: oldest session's refresh token evicted (FIFO). Evicted token reuse emits warning but does NOT revoke family. All remaining 10 sessions stay valid."
- **Rationale:** C-007 / X-006 won by V2 at 85% confidence. Both advocates agree. V1's "no cap, observe" defers a sizing decision. INV-013 flags eviction-vs-family interaction as HIGH UNADDRESSED — this change is paired with Fix #4 (INV-013) to ensure eviction does not cause false-positive family revocation.
- **Risk Level:** Medium — modifies TokenManager behavior in M2, adds eviction logic and family-metadata interaction
- **Specific Edit Instructions:**
  - In V1 Section 11.1 OQ-2 row, replace the "Recommended resolution" cell with: "10 active refresh tokens per user. Oldest evicted on new issuance (FIFO)."
  - In V1 M2 scope, add the token-cap paragraph.
  - In V1 M2 deliverables, add D-209.
  - In V1 Section 9.1, add `evicted` state and the guard text.
  - In V1 Section 8, update the 6th-device boundary row to the 11th-device version.

### Change #7: Pentest Cost Quantification

- **Source:** V2 Section 10.3 Cost Projection table (line 701): "External pentest (one-time) | $5,000-$15,000 | N/A"
- **Target Location in V1 base:** V1 Section 14 Cost & Resource Plan table
- **Integration Approach:** append
  1. Add a row to V1's cost table: "External penetration test (one-time)" with cost "$5,000-$15,000" and scaling factor "N/A — budgeted per engagement".
- **Rationale:** C-023 won by V2 at 85% confidence. Budget enables procurement; V1 is silent on pentest cost despite listing it as a PRD mitigation (SEC-5).
- **Risk Level:** Low — single table row addition
- **Specific Edit Instructions:**
  - In V1 Section 14 cost table, after the SendGrid row and before the total row, insert: `| External penetration test (one-time) | $5,000-$15,000 | N/A — budgeted per engagement |`

### Change #8: Feature Flag Lifecycle Table

- **Source:** V2 Appendix B (lines 834-839): Feature Flag Lifecycle table with Created / Enabled / Disabled / Removed columns per flag
- **Target Location in V1 base:** V1 Appendix B (Calendar view) — insert as a new appendix after current Appendix B, or expand Appendix B to include the lifecycle table
- **Integration Approach:** append
  1. Add a new Appendix C: "Feature Flag Lifecycle" with the following table adapted to V1's week-based cadence:
     - `AUTH_NEW_LOGIN`: Created Week 8 (M5 prep), Enabled Week 9 (Alpha), Disabled on rollback only, Removed Week 13 (post-stabilization)
     - `AUTH_TOKEN_REFRESH`: Created Week 8 (M5 prep), Enabled Week 10 (Beta), Disabled on rollback only, Removed Week 15 (post-stabilization + 2 weeks)
  2. Both flags default to OFF. They are enabled per-phase during rollout and removed only after sustained production stability.
- **Rationale:** C-021 won by V2 at 90% confidence. V1 conceded in R1 and R2. Appendix B operationalizes TDD Section 19.2 with concrete sprint deadlines. V1's Section 10 Out of Scope says "removal targets recorded" but does not provide dates.
- **Risk Level:** Low — new appendix, does not modify existing sections
- **Specific Edit Instructions:**
  - Insert a new H2 "Appendix C — Feature Flag Lifecycle" after current Appendix B.
  - Copy V2's Appendix B table structure, adapting Sprint references to V1's Week references.

### Change #9: Beta 1-Week Hidden Buffer

- **Source:** V2 Section 3.5 M5 Risk Notes (line 364): "build a 1-week buffer into the schedule (hidden from the public timeline) between Beta and GA"
- **Target Location in V1 base:** V1 Section 3, Milestone M5 scope and risk notes; V1 Section 2.2 Phase Map
- **Integration Approach:** append with arithmetic note
  1. Add to M5 risk notes: "Schedule management: embed a 1-week hidden buffer between Beta (5B) completion and GA (5C). This buffer is not reflected in the public timeline."
  2. Add a cross-reference note to INV-010: "Arithmetic constraint: V1's 11-week active cadence plus V2's +1 week hidden buffer totals 12 active weeks. To preserve the 2026-06-09 GA date, either (a) compress CC2/CC4 activities in Week 9-10, or (b) accept GA slip to 2026-06-16. Decision owner: Product Manager. Resolution deadline: M5 sub-phase 5A entry."
- **Rationale:** C-029 won by V2 at 90% confidence. V1 conceded in R1 and R2 ("standard PM practice"). INV-010 flags arithmetic incompatibility — the buffer is adopted but the GA-date tension is documented as a decision point.
- **Risk Level:** Medium — introduces a schedule constraint that may force a GA date slip; INV-010 remains MEDIUM UNADDRESSED as a scheduling decision rather than a spec defect
- **Specific Edit Instructions:**
  - In V1 M5 risk notes, add the buffer paragraph and the INV-010 arithmetic note.
  - Add to V1 Section 11.2 (roadmap-level open questions): "OQ-R7: Does the +1 week hidden buffer push GA to 2026-06-16, or does the team compress Week 9-10 CC activities? Decision owner: Product Manager. Target: Before M5 sub-phase 5A entry."

### Change #10: Three-Phase Decomposition Rationale

- **Source:** V2 Section 2.2 "Why Three Phases, Not Two" (lines 46-48): explains why password reset and frontend integration are separated
- **Target Location in V1 base:** V1 Section 2.1 "Decomposition rationale" — append a short paragraph
- **Integration Approach:** append
  1. After V1's existing three constraints in Section 2.1, add a fourth paragraph: "The PRD prescribes two phases (Core + Integration), but the TDD's five-milestone structure naturally clusters into three operational phases: Core Auth (M1+M2), Self-Service Recovery + User-Facing Integration (M3+M4), and Hardening + GA (M5). Separating M3 (password reset, which has external SendGrid dependency and unique email-delivery failure modes) from M4 (frontend integration, which is purely internal) isolates risk and allows M3/M4 to parallelize partially."
- **Rationale:** U-021 cited by V2 in R1 as a unique contribution. V1 did not oppose. Not directly scored in debate matrix but noted as a "valuable rationale" in R2 V1 rebuttal. Low-conflict addition.
- **Risk Level:** Low — text addition only, no structural changes
- **Specific Edit Instructions:**
  - In V1 Section 2.1, after the third numbered constraint, insert the three-phase rationale paragraph.

### Change #11: API Endpoint Summary Appendix

- **Source:** V2 Appendix C (lines 845-854): 6-row table with Endpoint / Method / Auth / Rate Limit / Milestone / Sprint columns
- **Target Location in V1 base:** New appendix to insert after the Feature Flag Lifecycle appendix (or as Appendix D if Change #8 is also applied)
- **Integration Approach:** append
  1. Add a new appendix "API Endpoint Summary" with a 6-row table covering all endpoints: `/auth/login`, `/auth/register`, `/auth/refresh`, `/auth/me`, `/auth/reset-request`, `/auth/reset-confirm`.
  2. Adapt Sprint columns to V1's Milestone+Week cadence. Add `POST /auth/logout` as a conditional row (pending OQ-R4 resolution).
  3. Note: "Production URLs use `/v1/auth/*` prefix per TDD Section 8.4."
- **Rationale:** U-027 cited as unique V2 contribution. V1 Section 13 Personas Check identifies Sam (API consumer) as needing "stable auth contracts" — the endpoint summary directly serves this persona. Not directly scored in debate matrix but uncontroversial.
- **Risk Level:** Low — new appendix, does not modify existing content
- **Specific Edit Instructions:**
  - Insert new H2 "Appendix D — API Endpoint Summary" after the Feature Flag Lifecycle appendix.
  - Copy V2 Appendix C table, replacing Sprint references with Week/Milestone references matching V1's cadence.

### Change #12: Infrastructure Workstream Split

- **Source:** V2 Section 4.5 "Infrastructure Workstream" (lines 434-447): explicit sprint-level table for PostgreSQL, Redis, API Gateway, K8s, CI/CD, feature flag, and prod provisioning activities
- **Target Location in V1 base:** V1 Section 4 Cross-Cutting Workstreams — either split V1 CC2 (Observability & Operational Readiness) into CC2 (Observability) + CC5 (Infrastructure), or annotate CC2 to make infrastructure items explicit
- **Integration Approach:** restructure
  1. Add a new CC5 "Infrastructure & Platform" workstream to V1 Section 4, with the following items adapted to V1's week-based cadence:
     - INF-1: PostgreSQL 15+ provisioning and connection pooling (Week -1 to Week 1)
     - INF-2: Redis 7+ provisioning (Week 1 — moved from M2 entry due to lockout-in-M1)
     - INF-3: API Gateway rate-limit configuration (Week 2)
     - INF-4: Kubernetes manifests + HPA (3 replicas, scale to 10 on CPU > 70%) (Week 3-4)
     - INF-5: CI/CD pipeline: build, test, deploy to staging (Week 1-2)
     - INF-6: Feature flag infrastructure setup (Week 8)
     - INF-7: Production environment provisioning (Week 9)
  2. Remove infrastructure items currently embedded in V1 CC2 (OBS items that are really infrastructure: OBS-6 capacity planning dashboard, OBS-7 DNS/SPF/DKIM/DMARC). Keep these in CC2 as observability-driven but add cross-references to CC5 for the provisioning action.
- **Rationale:** V2 separates infrastructure from observability, making provisioning dependencies visible. V1 embeds infra in CC2 and M5 deliverables. Splitting makes the "Redis by M1 entry" requirement (from Change #1) trackable as a dedicated workstream item. Not directly scored in debate but noted as a structural improvement in R2.
- **Risk Level:** Medium — restructures the cross-cutting workstream section; does not change deliverables, only tracking
- **Specific Edit Instructions:**
  - In V1 Section 4, after CC4, add a new H3 "CC5 — Infrastructure & Platform" with the seven-item list above.
  - In V1 CC2, keep OBS-1 through OBS-7 but add parenthetical cross-references to CC5 items where provisioning is the underlying dependency (e.g., OBS-7 DNS/SPF/DKIM/DMARC: "(provisioning tracked in CC5 INF-3)").

---

## Section 2: HIGH-Severity Invariant Fixes (MANDATORY)

### Fix #1: INV-001 — Refresh-Token Family Lineage Durability

- **Invariant:** Refresh-token "family" lineage state is persisted in Redis and survives Redis restarts so that reuse-detection can revoke descendants discovered after a Redis cold-start.
- **Risk:** If Redis loses persistence between rotation N and reuse detection at N+1, the family is unreachable. A reused token goes undetected, and the attacker retains access. This directly undermines V1's core security contribution (token-family semantics, Section 9.1).
- **Fix Approach:**
  1. Define family-linkage storage schema in D-202 (TokenManager): each refresh-token record in Redis stores `family_id` (UUID, set at first issuance) and `parent_id` (hash of the previous token in the chain, or null for root). Store as a Redis Hash per token with fields: `family_id`, `parent_id`, `user_id`, `issued_at`, `status` (issued/rotated/revoked/evicted).
  2. Add a Redis Sorted Set per family: key = `family:{family_id}:members`, score = issued_at timestamp, value = token hash. This enables efficient "revoke all descendants" by scanning the sorted set.
  3. Specify durability: Redis AOF persistence enabled with `appendfsync everysec` (per TDD Section 6.3 Redis requirements). Document that AOF ensures family metadata survives cold-start.
  4. Document family-metadata TTL: family metadata Sorted Set TTL = max refresh-token TTL + 24-hour buffer (8 days). This ensures the family tracking outlives the longest-lived token in the family.
  5. Add integration test: "After Redis restart (simulated via FLUSHALL + AOF reload), reuse-detection on a pre-restart token still revokes the family."
- **Target Location:**
  - V1 Section 9.1 (refresh-token state machine): add family-linkage storage subsection
  - V1 M2 deliverable D-202: expand description to include family-linkage storage schema
  - V1 M2 exit criteria: add "Family-linkage metadata survives simulated Redis restart (AOF persistence test)."
  - V1 Section 5 Risk Register: update R-105 to note AOF persistence requirement
- **Owner / Acceptance Test:** auth-team; integration test in M2 CI pipeline

### Fix #2: INV-005 — Audit Log NULL user_id

- **Invariant:** M1 audit_log table accepts NULL `user_id` for pre-authentication failure events (e.g., failed login for unknown email).
- **Risk:** If `user_id NOT NULL`, every `login_failure` for an unknown-email address cannot be audited. This directly contradicts the audit-day-1 consensus and the PRD's "all auth events must be logged" requirement. The SOC2 audit trail is incomplete from day 1.
- **Fix Approach:**
  1. Update V1 D-102 (`migrations/0002_audit_log.sql`) schema definition to explicitly specify: `user_id UUID NULL` (not NOT NULL). Add a comment in the migration: "-- Nullable to allow pre-auth failure events (login for unknown email, reset-request for unregistered email)."
  2. Add to V1 CC2 OBS-1 workstream item: add explicit verification: "Verify NULL user_id audit rows are written correctly in M1 integration tests. Test case: login with unregistered email produces an audit_log row with user_id=NULL."
  3. Add to V1 M1 exit criteria: "Audit-log INSERT succeeds for login_failure events where user_id is NULL (unknown email path)."
- **Target Location:**
  - V1 Section 3 M1 scope: update audit_log schema description to note `user_id NULL`
  - V1 D-102 deliverable: update description
  - V1 M1 exit criteria: add NULL user_id test
  - V1 CC2 OBS-1: add verification item
- **Owner / Acceptance Test:** auth-team; M1 integration test verifies NULL user_id row

### Fix #3: INV-006 — Enumeration-Timing + Audit-Write Interaction

- **Invariant:** The `unknown-email vs wrong-password` enumeration-timing constraint (<50ms variance, V1 QA-6) holds when audit-log INSERT happens on the failure path.
- **Risk:** Unknown-email path has no `user_id` to insert; wrong-password path has one. The two paths have asymmetric DB write costs. Without identical-shape writes, the timing variance blows past the 50ms QA-6 budget, creating a timing side-channel that leaks whether an email is registered.
- **Fix Approach:**
  1. Mandate identical-shape audit writes on both failure paths:
     - Unknown-email path: write audit_log with `user_id=NULL, email_hash=SHA256(email)`.
     - Wrong-password path: write audit_log with `user_id=<UUID>, email_hash=SHA256(email)`.
     - Both paths execute the same number of DB operations (1 audit INSERT) with the same row shape. The only difference is NULL vs UUID in one column.
  2. For unknown-email path, also compute a dummy bcrypt hash (to match the ~300ms timing of the wrong-password path's bcrypt verify). This addresses INV-008 (MEDIUM UNADDRESSED but directly interacts with INV-006).
  3. Update V1 QA-6 test to verify timing variance <50ms WITH audit writes enabled (not just without).
  4. Update V1 Section 8 Boundary Conditions: add a row for "Login failure audit-write timing" stating the identical-shape requirement.
- **Target Location:**
  - V1 Section 9.5 Database Transactions: add login-failure-path transaction description
  - V1 CC3 QA-6: update test to include audit writes
  - V1 Section 8: add boundary condition row
- **Owner / Acceptance Test:** auth-team + security; QA-6 CI gate

### Fix #4: INV-013 — Token Eviction vs Family-Revocation Race

- **Invariant:** Maximum refresh tokens per user (consensus: V2's 10-token FIFO cap). Eviction at the 11th token does not race with reuse-detection on the 10th token. If an evicted token is later "used" by the legitimate device, reuse-detection must NOT revoke the entire family (false-positive user logout across all devices).
- **Risk:** Without this fix, a legitimate user with 10+ devices who logs in on an 11th device will be logged out everywhere when the evicted device's stale token triggers reuse-detection. This is a severe UX regression masquerading as a security feature.
- **Fix Approach:**
  1. When evicting the oldest token (FIFO), mark that token's family entry as `evicted=true` in the family Sorted Set metadata. This is the sentinel that distinguishes "legitimate eviction" from "malicious reuse."
  2. In the reuse-detection handler: if the presented token's family metadata has `evicted=true`, log a `token_evicted_reuse` audit event at WARNING level (not security-critical) and return 401 for that specific token only. Do NOT revoke the entire family.
  3. If the presented token's family metadata has `evicted=false` (or no eviction flag), proceed with normal reuse-detection: revoke the entire family (security event).
  4. Add integration test: "User with 11 devices: login on device 11 evicts device 1's token. Device 1's stale token triggers reuse-detection. Result: device 1 gets 401 only; devices 2-11 remain active. Family NOT revoked."
- **Target Location:**
  - V1 Section 9.1 refresh-token state machine: add `evicted` state and guard (this is also covered by Change #6)
  - V1 M2 deliverable D-202: expand to include eviction-family-guard logic
  - V1 M2 exit criteria: add the 11-device integration test
- **Owner / Acceptance Test:** auth-team; M2 integration test

### Fix #5: INV-017 — Login-Path Transaction Ordering

- **Invariant:** M1 audit-log writes for `login_success` + M2 `lastLoginAt` UPDATE + M2 TokenManager Redis SET are correctly ordered to avoid "audit says success, lastLoginAt unchanged" partial-state.
- **Risk:** If login flow is: (1) bcrypt verify -> (2) audit INSERT -> (3) UPDATE lastLoginAt -> (4) Redis SET refresh token, a Redis failure between step 3 and 4 leaves user with "logged in" audit + updated lastLoginAt + NO token. SOC2 audit trail becomes non-deterministic relative to system state. User retries -> second `login_success` audit row, double-increment lastLoginAt.
- **Fix Approach:**
  1. Define login-path transaction scope in V1 Section 9.5 (equivalent to the existing `register()` transaction scope):

     ```
     AuthService.login() transaction scope:
     1. bcrypt verify (~300ms, read-only, no transaction needed)
     2. BEGIN TRANSACTION:
        a. Validate credentials (read user_profile)
        b. UPDATE user_profile SET lastLoginAt = NOW() WHERE id = user_id
        c. INSERT INTO audit_log (user_id, event_type='login_success', ...)
     3. COMMIT TRANSACTION
     4. TokenManager.issueTokens() — Redis SET (outside DB transaction)
     5. Return AuthToken to client
     ```

  2. Document rollback semantics: if step 4 (Redis SET) fails, the DB transaction (steps 2-3) is already committed. Audit row shows `login_success`, lastLoginAt is updated, but no refresh token is issued. Client receives a 503 error. Client retries -> second login attempt succeeds normally, producing a second `login_success` audit row. This is acceptable because: (a) the audit trail is accurate (the user did authenticate), (b) the second attempt is idempotent from the user's perspective, (c) `lastLoginAt` converges to the correct value on retry.
  3. Add integration test: "Login succeeds at DB level but Redis SET fails. Verify: audit_log has login_success row, lastLoginAt updated, client receives 503, retry succeeds."
- **Target Location:**
  - V1 Section 9.5: add `AuthService.login()` transaction scope after existing `register()` and `confirmPasswordReset()` scopes
  - V1 M2 exit criteria: add Redis-failure-during-login test
- **Owner / Acceptance Test:** auth-team; M2 integration test

### Fix #6: INV-021 — In-Process SendGrid Retry vs 200ms p95

- **Invariant:** The "in-process SendGrid retry" consensus (C-020 V1 wins for v1.0) does not block the request thread long enough to violate NFR-PERF-001 200ms p95.
- **Risk:** In-process retry with exponential backoff on SendGrid 5xx could take >60s, blocking the HTTP response. Either fire-and-forget (loses retry guarantee on process restart) or synchronous-with-retry (violates 200ms p95). Cannot be both.
- **Fix Approach:** Adopt option (c) from the invariant probe's recommendation — "single in-process attempt + dead-letter log for manual retry":
  1. `/auth/reset-request` sends email via a single SendGrid API call with a 5-second timeout. If the call succeeds, email is sent. If it fails (timeout or 5xx), log the email payload to a `pending_emails` PostgreSQL table and return 200 to the client (the anti-enumeration always-200 response is preserved regardless).
  2. Add a cron-based retry sweep (runs every 5 minutes): query `pending_emails` for unsent rows, attempt SendGrid delivery, mark as sent or increment retry_count. Cap at 10 retries before alerting.
  3. This resolves the contradiction: the HTTP response returns in <5 seconds (well within 200ms p95 for the API call itself, since the email send is offloaded to the retry sweep after the first attempt fails). The first-attempt 5-second timeout is the ceiling.
  4. Update V1 D-303 (SendGrid client wrapper) description to: "SendGrid client wrapper with single-attempt 5-second timeout + `pending_emails` dead-letter table for retry sweep."
  5. Add new deliverable D-310 to M3: "`pending_emails` table + retry sweep cron job (5-minute interval, 10-retry cap)."
  6. Update V1 M3 exit criteria: "/auth/reset-request returns 200 in <200ms p95 even when SendGrid is unavailable (email queued for retry)."
  7. Document decision owner: auth-team lead.
- **Target Location:**
  - V1 Section 3 M3 scope: update async-email description
  - V1 D-303 deliverable: update description
  - V1 M3 deliverables: add D-310
  - V1 M3 exit criteria: update reset-request latency criterion
  - V1 Section 11.1 OQ-1 resolution: update to reflect single-attempt + dead-letter approach
- **Owner / Acceptance Test:** auth-team; M3 integration test (SendGrid down scenario)

### Fix #7: INV-022 — SOC2 Audit-Log Immutability Sufficiency

- **Invariant:** Consensus audit-log in M1 is sufficient to pass SOC2 Type II audit gate without immutability guarantees.
- **Risk:** SOC2 CC7.2 (system monitoring) and CC6.1 (logical access) require tamper-evident logs, segregation of duties on log access, and log integrity verification. Without these, the audit log is necessary but not sufficient for SOC2 Type II sign-off.
- **Fix Approach:**
  1. Add to M1 D-102 scope: "Migration includes a DB trigger preventing UPDATE and DELETE on the `audit_log` table: `CREATE TRIGGER prevent_audit_modification BEFORE UPDATE OR DELETE ON audit_log FOR EACH ROW EXECUTE FUNCTION raise_error('audit_log is immutable');`"
  2. Add to M1 scope: "Separate DB role `audit_writer` with INSERT-only grants on `audit_log`. No grant for UPDATE or DELETE. Application uses this role for audit writes."
  3. Add to CC1 SEC-3 workstream item: expand to include: "(a) DB trigger preventing audit_log modification, (b) separate audit_writer DB role, (c) quarterly log-integrity verification script that checksums row counts and detects gaps in the event sequence."
  4. Add deliverable D-110 to M1: "Audit-log immutability controls: UPDATE/DELETE trigger + audit_writer role + integrity verification script."
  5. Map SOC2 controls to deliverables:
     - CC6.1 (logical access): D-110 (audit_writer role, no UPDATE/DELETE grants)
     - CC7.2 (system monitoring): D-102 (audit_log schema) + D-110 (immutability trigger) + SEC-3 (integrity verification)
  6. Add to M5 pre-GA checklist: "Verify audit-log immutability controls in production (trigger active, audit_writer role enforced, integrity script green)."
- **Target Location:**
  - V1 M1 scope: add immutability controls
  - V1 M1 deliverables: add D-110
  - V1 CC1 SEC-3: expand description
  - V1 M5 exit criteria: add immutability verification
- **Owner / Acceptance Test:** security + auth-team; M1 integration test (attempt UPDATE/DELETE on audit_log -> trigger raises error); M5 pre-GA verification

### Fix #8: INV-023 — Lockout-Only Brute-Force Sufficiency

- **Invariant:** Consensus M1 lockout (5 attempts / 15 min) alone is sufficient against PRD R-002 "High probability" brute-force risk.
- **Risk:** Lockout is bypassed trivially: distributed attack across 1M IPs hitting 4 attempts each. PRD R-002 mitigation co-requires both lockout AND rate limiting.
- **Fix Approach:**
  1. Explicitly document the defense-in-depth stack as a new subsection in V1 Section 3 M1 scope or as a dedicated paragraph in V1 Section 5 Risk Register R-102:
     - Layer 1 (M1): Per-account lockout — 5 failures in 15 min per account+IP combination. LoginAttemptTracker in Redis.
     - Layer 2 (M1): Gateway IP rate limit — 10 req/min/IP on `/auth/login` (V1 R-102). Already provisioned via API gateway.
     - Layer 3 (M1, NEW): Per-account global rate limit — rate-limit login attempts by email-hash regardless of source IP. New deliverable D-109: "Per-account global rate limit: max 20 login attempts per email-hash per hour, across all IPs. Enforced in Redis via sliding window keyed on SHA256(email)."
     - Layer 4 (M5 contingency): CAPTCHA after 3 failures (V1 R-112 contingency). Not shipped in v1.0 but documented as the escalation path if layers 1-3 prove insufficient.
  2. Add D-109 to M1 deliverables table.
  3. Update R-102 mitigation column to list all four layers.
  4. Add M1 exit criterion: "Per-account global rate limit enforced: 20 attempts/email-hash/hour across all IPs verified in integration test."
- **Target Location:**
  - V1 M1 scope: add defense-in-depth paragraph
  - V1 M1 deliverables: add D-109
  - V1 Section 5 R-102: update mitigation
  - V1 M1 exit criteria: add global rate limit test
- **Owner / Acceptance Test:** auth-team + security; M1 integration test (simulate 20 attempts from different IPs against same email -> 429 after 20th)

### Fix #9: INV-026 — bcrypt cost-12 vs NFR-PERF-001

- **Invariant:** Consensus bcrypt cost-12 (~300ms hash time) achieves NFR-PERF-001 (<200ms p95 login).
- **Risk:** Sum-of-latencies at cost-12: bcrypt 300ms + DB writes 20-50ms + Redis 5-10ms = 325-360ms. NFR-PERF-001 cannot be hit at cost-12 with the current architecture. The roadmap names cost-11 as a fallback but does not commit to it.
- **Fix Approach:**
  1. Update V1 D-103 description to: "PasswordHasher module with cost factor determined by benchmark in M1 Week 1 on target hardware. Default cost factor: 11 (estimated ~100ms). Target cost factor: 12 (~300ms). Ship at cost 11 unless M1 benchmark demonstrates cost-12 within the 200ms p95 budget inclusive of DB writes and Redis operations."
  2. Update V1 M1 exit criteria: replace "PasswordHasher benchmark on the build agent confirms cost-12 hash time is in the 250-500ms band" with: "PasswordHasher benchmark on target hardware confirms chosen cost factor (11 or 12) produces total login-path latency within 200ms p95 budget. Benchmark must include bcrypt + DB writes + Redis operations as a full-path measurement."
  3. Update V1 R-104 mitigation from "drop to cost 11 if latency budget exceeded" to: "Ship at cost 11 unless benchmark demonstrates cost-12 within budget. Document security rationale: cost-11 meets NIST SP 800-63B minimum (>=10ms hash time is satisfied at cost-11 with substantial margin)."
  4. Add a new entry to V1 Section 5 Risk Register: "R-117: Total login-path latency (bcrypt + DB + Redis) exceeds 200ms p95 at cost-11. Prob: Low, Impact: High (blocks NFR-PERF-001). Mitigation: async audit-log write via outbox pattern; Redis pipeline for lockout-check + token-SET. Contingency: accept cost-10 with documented rationale and plan to upgrade hardware for cost-12 in v1.1."
  5. Add to V1 Section 8 Boundary Conditions: "Login-path latency budget breakdown: bcrypt target <=120ms (cost-11), DB writes <=40ms, Redis <=20ms, network overhead <=20ms. Total <=200ms."
- **Target Location:**
  - V1 D-103 deliverable: update description
  - V1 M1 exit criteria: update benchmark criterion
  - V1 R-104: update mitigation
  - V1 Section 5: add R-117
  - V1 Section 8: add latency-budget row
- **Owner / Acceptance Test:** auth-team; M1 D-103 benchmark report reviewed by security + eng-manager

---

## Section 3: Base Weaknesses Being Fixed

These are weaknesses in V1 that the V1 advocate conceded (per round-2-rebuttal-1.md) and that are addressed by the changes above. Listed briefly to avoid redundancy with Section 1.

| Weakness | V1 Advocate Concession | Fix Applied |
|---|---|---|
| Lockout deferred to M3 leaves M1/M2 unprotected | R1 Concession 1, R2 reaffirmed | Change #1 (lockout-in-M1) + Fix #8 (defense-in-depth stack) |
| Rollback assumes legacy auth that doesn't exist (greenfield) | R1 Concession 2, R2 sharpened as P1-incident failure mode | Change #2 (greenfield rollback) |
| Single-row staffing unactionable | R1 Concession 3, R2 reaffirmed | Change #3 (10-row staffing table) |
| No admin audit query deliverable for Jordan persona | R1 Concession 4, R2 reaffirmed | Change #5 (D-309 admin audit query) |
| Audit retention conflict (90d vs 12m) silently unresolved in deliverable text | R2 wording fix: "retention parameterized, default 90d per TDD, set to 12 months pending OQ-R1" | Implicitly addressed by V1's existing OQ-R1 mechanism; Fix #7 (SOC2 immutability) strengthens the audit-story overall |

---

## Section 4: Changes NOT Being Made

### Rejection #1: V2's 22-Week Timeline

- **V2 position:** Section 11 "Total Duration: 22 weeks (~5.5 months)" with Sprint 1-11 numbering.
- **Rejected because:** V2 conceded in R1 and R2. PRD Phasing section explicitly states "Phase 1 (Sprint 1-3) + Phase 2 (Sprint 4-6) = 6 sprints." V1's 11-week active + 2-week tail matches. The 22-week label is a self-contradiction (X-001, 100% confidence V1 win) since V2's own milestone dates align with an 11-week plan.
- **Evidence:** Debate-transcript scoring matrix: C-001 (V1, 100%), C-002 (V1, 95%), X-001 (V1, 100%). Both advocates agree.

### Rejection #2: V2's M3 Audit Log Placement

- **V2 position:** Audit log table ships in M3 (D-028), leaving M1 and M2 events unlogged for 8-12 weeks.
- **Rejected because:** V2 conceded in R1 and R2. PRD constraint is unconditional ("All auth events must be logged for SOC2 audit trail requirements"). Application logs are not audit logs. SOC2 audit trail must exist from day 1.
- **Evidence:** C-004 (V1, 95%), X-003 (V1, 95%). V2's R2 strengthened concession: "audit-day-1 is a PRD compliance requirement."

### Rejection #3: Bull/BullMQ Async Queue for v1.0 Email

- **V2 position:** Use Bull/BullMQ Redis-backed job queue for async email delivery (D-026, Section 9.1 OQ-A recommendation).
- **Rejected for v1.0 because:** V2 conceded in R2 that Bull is v1.1 not v1.0 scope. V1's in-process approach is simpler for single-template v1.0. V1 R2 raised undisclosed monitoring, runbook, and queue-poisoning surface. INV-021 exposed the in-process contradiction, but Fix #6 resolves it via single-attempt + dead-letter table (not Bull). Bull is the recommended v1.1 upgrade path.
- **Evidence:** C-020 (V1 v1.0 / V2 v1.1, 85%). Both advocates converge in R2.

### Rejection #4: V2's 30-Minute Lockout Auto-Unlock

- **V2 position:** Auto-unlock after 30 minutes (OQ-C recommendation, Section 9.1).
- **Rejected because:** TDD Section 13 grounds the 15-minute window. V2's 30-minute recommendation doubles the window without source support and is more punitive for legitimate users who mistype passwords.
- **Evidence:** C-008 (V1, 85%). X-005 (V1, 85%). V1 R2 cites TDD Section 13 explicitly.

### Rejection #5: V2's Absence of State Machines, Token Families, Chaos Testing, Enumeration Timing

- **V2 position:** State machines, token families, chaos testing (QA-7), and enumeration-timing gates (QA-6) belong in the TDD, not the roadmap.
- **Rejected because:** V2 conceded all of these in R1 and R2. TDD lacks token-family semantics and formal state machines; roadmap must supply them for M2/M3 implementers. QA-6 and QA-7 are testable, CI-enforceable gates that are roadmap-appropriate.
- **Evidence:** C-009 (V1, 90%), S-007 (V1, 95%), C-014 (V1, 95%), C-015 (V1, 95%). All conceded by V2.

### Rejection #6: V2's DB-Hashed Reset Token Storage

- **V2 position:** Reset tokens stored hashed in database (D-025).
- **Rejected as a tie:** Both advocates rate as Tie in R1 and R2. Redis TTL (V1) and DB-hashed (V2) are both architecturally valid. V1 ADR D-308 documents the trade-off. Base (V1) approach prevails: Redis with 1-hour TTL.
- **Evidence:** C-006 (Tie, 80%), X-007 (Tie, 80%). Neither advocate argues for a change.

---

## Section 5: Risk Summary

| Change # | Description | Risk Level | Impact if Wrong | Rollback Strategy |
|---|---|---|---|---|
| #1 | Lockout-in-M1 | Medium | M1 scope creep; Redis dependency moved to Week 1 may delay M1 start if infra not ready | Revert lockout to M3 if M1 Week 1 Redis not provisioned; ship M1 without lockout as interim |
| #2 | Greenfield rollback | Low | None — text-only change reflecting PRD reality | N/A |
| #3 | 10-row staffing table | Low | Staffing numbers may be aspirational; no structural impact | Revert to single-row summary if detailed table proves inaccurate |
| #4 | Post-GA section | Low | Quarter targets may slip; noted as "targets" not commitments | Remove section if post-GA planning changes |
| #5 | Admin audit query (D-309) | Low | ~1 day additional M3 scope | Defer D-309 to v1.1 if M3 is tight |
| #6 | 10-token FIFO cap | Medium | Eviction logic may have edge cases; family-metadata interaction adds M2 complexity | Revert to V1's "no cap, observe" policy if implementation proves too complex for M2 |
| #7 | Pentest cost row | Low | Cost estimate may be inaccurate | Update estimate when vendor selected |
| #8 | Feature flag lifecycle | Low | Timeline may shift | Update appendix as dates change |
| #9 | Beta buffer | Medium | Forces GA-date decision (slip to 2026-06-16 or compress CC activities) | Accept GA slip if team cannot compress |
| #10 | Three-phase rationale | Low | Rationale paragraph only | Remove paragraph if phasing changes |
| #11 | API endpoint summary | Low | Reference only; may drift if endpoints change | Update appendix as API evolves |
| #12 | Infrastructure workstream | Medium | Restructures CC section; tracking overhead if not maintained | Revert to single CC2 if split adds confusion |
| Fix #1 | INV-001 family lineage | High | If family-metadata storage design is wrong, reuse-detection fails silently | AOF persistence is Redis-standard; worst case, family tracking is rebuilt from audit_log |
| Fix #2 | INV-005 NULL user_id | Low | Schema change only | Migration is additive (relaxing NOT NULL) |
| Fix #3 | INV-006 enumeration timing | Medium | Identical-shape writes must be verified in CI; dummy bcrypt adds ~300ms to unknown-email path (intentional) | QA-6 gate catches regression |
| Fix #4 | INV-013 eviction guard | High | If evicted=true flag is not set correctly, false-positive family revocations occur | Disable 10-token cap (revert to V1's no-cap policy) until fix is verified |
| Fix #5 | INV-017 login transaction | Medium | Login-path transaction scope must be implemented correctly; Redis-outside-transaction is acceptable per analysis | Document as known limitation if Redis-failure-during-login path proves problematic |
| Fix #6 | INV-021 SendGrid retry | High | Dead-letter table adds operational surface (cron job, retry monitoring); if cron fails, emails silently queue | Alert on pending_emails table row count > 100; manual retry via admin action |
| Fix #7 | INV-022 SOC2 immutability | Medium | Trigger and role-based access are standard DB patterns; integrity script must be maintained quarterly | SOC2 auditor may accept compensating controls if trigger is temporarily disabled during migration |
| Fix #8 | INV-023 defense-in-depth | Medium | Per-account global rate limit adds Redis key-per-email-hash; memory impact estimated at ~1MB per 100K users | Disable Layer 3 if Redis memory pressure exceeds OBS-6 thresholds; rely on Layers 1+2 |
| Fix #9 | INV-026 bcrypt cost | High | If cost-11 also exceeds budget (unlikely per TDD Section 17 benchmark), NFR-PERF-001 is unachievable without async audit writes | R-117 contingency: async audit-log write via outbox pattern or accept cost-10 |

---

## Section 6: Execution Order for Merge

The merge-executor should apply changes in the following order. Grouping: invariant fixes first (unblock convergence), then V2 strength incorporations (add value), then base-weakness fixes (correct identified issues — most are covered by earlier changes).

### Phase A: HIGH-Severity Invariant Fixes (mandatory, highest priority)

1. **Fix #9 (INV-026): bcrypt cost-12 vs NFR-PERF-001** — Apply first because it affects M1 scope (D-103), M1 exit criteria, risk register (R-104 + new R-117), and boundary conditions table. Other changes reference the bcrypt cost factor.

2. **Fix #8 (INV-023): Defense-in-depth brute-force stack** — Apply second because it adds D-109 to M1 deliverables and modifies M1 scope. Must be applied before Change #1 (lockout-in-M1) because both modify M1 deliverables and the defense-in-depth stack includes lockout as Layer 1.

3. **Fix #2 (INV-005): Audit log NULL user_id** — Apply third because it modifies D-102 schema (M1 deliverable) and M1 exit criteria. Independent of Fix #9 and Fix #8 but also targets M1.

4. **Fix #3 (INV-006): Enumeration timing + audit writes** — Apply fourth because it depends on Fix #2 (NULL user_id) and modifies the login-failure path, QA-6 test, and Section 8 boundary conditions.

5. **Fix #7 (INV-022): SOC2 audit-log immutability** — Apply fifth because it adds D-110 to M1 deliverables, expands CC1 SEC-3, and adds M5 exit criteria. Independent of the login-path fixes but also targets M1 scope.

6. **Fix #1 (INV-001): Family lineage durability** — Apply sixth because it modifies M2 deliverables (D-202), M2 exit criteria, and Section 9.1 state machine. Must be applied before Fix #4 (eviction guard) because the family metadata schema is the foundation for the eviction flag.

7. **Fix #4 (INV-013): Eviction vs family-revocation race** — Apply seventh because it depends on Fix #1 (family metadata schema) and modifies Section 9.1 state machine (adds `evicted` state). Must be applied before Change #6 (10-token FIFO cap) because the cap is what triggers eviction.

8. **Fix #5 (INV-017): Login-path transaction ordering** — Apply eighth because it adds a new transaction scope to Section 9.5 and modifies M2 exit criteria. Independent of family-lineage fixes but references the login flow.

9. **Fix #6 (INV-021): In-process SendGrid retry** — Apply ninth because it modifies M3 scope (D-303 + new D-310), M3 exit criteria, and OQ-1 resolution. Independent of M1/M2 fixes.

### Phase B: V2 Strength Incorporations (add value)

10. **Change #1: Lockout-in-M1** — Must be applied after Fix #8 (defense-in-depth stack, which includes lockout as Layer 1) and Fix #9 (bcrypt cost, which affects M1 scope). Moves D-305 to M1, adds Redis to M1 entry criteria, updates sequencing diagrams.

11. **Change #6: 10-token FIFO cap** — Must be applied after Fix #4 (eviction guard) because the cap triggers eviction and the guard prevents false-positive family revocation.

12. **Change #2: Greenfield rollback** — Independent. Can be applied at any point in Phase B.

13. **Change #3: 10-row staffing table** — Independent. Replaces single row in Section 14.

14. **Change #4: Post-GA section** — Independent. New section insertion.

15. **Change #5: Admin audit query (D-309)** — Independent. Adds deliverable to M3.

16. **Change #7: Pentest cost** — Independent. Single table row.

17. **Change #8: Feature flag lifecycle** — Independent. New appendix.

18. **Change #9: Beta buffer** — Independent but references M5 schedule. Apply after Change #1 (which modifies M1/M5 sequencing).

19. **Change #10: Three-phase rationale** — Independent. Paragraph addition.

20. **Change #11: API endpoint summary** — Independent. New appendix.

21. **Change #12: Infrastructure workstream** — Independent. New CC5 section.

### Phase C: Base Weakness Fixes (correct identified issues)

22. **Base weakness: Rollback assumes legacy auth** — Already covered by Change #2. No separate action needed.

23. **Base weakness: Single-row staffing** — Already covered by Change #3. No separate action needed.

24. **Base weakness: No admin audit query** — Already covered by Change #5. No separate action needed.

25. **Base weakness: Audit retention conflict** — V1's existing OQ-R1 mechanism handles this. Fix #7 (SOC2 immutability) strengthens the overall audit story. No separate action needed beyond ensuring D-102 wording reflects: "retention parameterized, default 90d per TDD, set to 12 months pending OQ-R1 resolution."

26. **Base weakness: Lockout deferred to M3** — Already covered by Change #1. No separate action needed.

---

## Section 7: Review Status

- **Approval:** auto-approved (non-interactive mode)
- **Timestamp:** 2026-05-22T12:30:00Z
- **Total changes:** 26 (12 V2 incorporations + 9 invariant fixes + 5 base-weakness fixes, where 5 base-weakness fixes are subsumed by earlier changes)
- **Distinct edit operations:** 21 (Phase A: 9 invariant fixes + Phase B: 12 V2 incorporations; Phase C base-weakness fixes are already covered)
- **HIGH-risk changes:** 4 (Fix #1 family lineage, Fix #4 eviction guard, Fix #6 SendGrid retry, Fix #9 bcrypt cost)
- **HIGH invariant fixes:** 9 (all 9 HIGH UNADDRESSED items addressed)
- **Residual MEDIUM UNADDRESSED invariants:** 10 (INV-002, INV-003, INV-007, INV-008, INV-010, INV-015, INV-019, INV-020, INV-024, INV-025) — these are tracked in the invariant probe but do not block convergence per the protocol; merge-executor should note them as known limitations in the merged output's closing section.

---

*Plan assembled from: base-selection.md (scoring + V2 strengths I-1 through I-12 + 9 HIGH UNADDRESSED invariants), debate-transcript.md (per-point scoring matrix + convergence assessment), invariant-probe.md (26 findings with refactor actions), diff-analysis.md (98 diff points), variant-1-opus-default.md (790-line base), variant-2-sonnet-default.md (854-line non-base).*
