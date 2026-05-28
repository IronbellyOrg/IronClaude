# Round 1 — Variant 1 Advocate (opus)

## Position Summary

Variant 1 is the stronger roadmap because it (a) honors the source documents' actual schedule arithmetic — six 2-week sprints = 12 calendar weeks, not 22 — (b) builds SOC2-grade audit infrastructure from day 1 instead of deferring it through M1/M2, and (c) supplies the formal state machines, token-family semantics, enumeration-timing gates, and chaos-test track that turn a TDD-aligned plan into something an implementer can execute without inventing security-critical transitions at coding time. Variant 2's operational additions (team table, post-GA section, pentest budget) are genuinely useful but are bolted onto a roadmap whose own duration label (22 weeks) contradicts its own target dates (Mar 30 → Jun 9 ≈ 11 weeks), and whose deferral of audit logging and brute-force lockout opens compliance and security gaps that no amount of staffing detail can close.

---

## Steelman of Variant 2

Variant 2 is not a weak document. The strongest version of its case is this:

1. **Operational honesty about people.** A roadmap is a coordination artifact for humans. V2's 10-row staffing table (Section 10.1) names exactly who is needed and when. V1's single line ("2 backend + 1 frontend FTE + 0.5 SRE + 0.25 security review") is unactionable for hiring. (U-022, S-012.)
2. **Greenfield discipline.** V2's Assumption 6 ("There is no existing legacy auth system requiring migration") is correct per the PRD Executive Summary ("the platform currently operates without any user identity system"). V1's rollback procedure step 2 — "Flip `AUTH_NEW_LOGIN` OFF — traffic routes back to legacy auth" — references a system that does not exist. (U-025, X-004.)
3. **Lockout in M1 closes a real brute-force window.** A public `/auth/login` endpoint without lockout is exposed to the PRD's own "High probability, Medium impact" R-002 risk for as long as lockout is deferred. (C-003, X-002.)
4. **Post-GA continuity.** V2 Section 13 names v1.1 (MFA, API keys, remember me, email verification, password change, self-service unlock) and v2.0 (OAuth, social login, RBAC, admin dashboard) with quarters attached. V1 lists deferred items in Out of Scope but supplies no sequencing. (U-023, S-013.)
5. **Feature-flag lifecycle.** V2 Appendix B specifies Created/Enabled/Disabled/Removed per flag. V1 says "removal targets recorded" without dates. (U-024, C-021.)
6. **Admin audit query.** V2 D-030 explicitly delivers a query interface for Jordan persona; V1 lists the audit table and the events but no query deliverable. (U-027, C-018.)
7. **Pentest budget.** V2 quantifies $5K-$15K. V1 lists the pentest as a deliverable but assigns no budget, which can stall procurement. (U-026, C-023.)
8. **M3/M4 parallelization.** V2's dependency matrix marks M3 → M4 as a SOFT dependency for the reset pages only, enabling earlier frontend start.

These are real strengths and I will concede several below.

---

## Strengths Claimed (with evidence)

### Strength 1: Duration arithmetic matches the source documents

**V1 evidence:** Section 1 line 6 — "11 calendar weeks (2026-03-30 through 2026-06-12), plus a 2-week post-GA stabilization tail." Section 2.2 phase map: M1 (week 1-2), M2 (week 3-4), M3 (week 5-6), M4 (week 7-8), M5 (week 9-11). Section 18 calendar (lines 768-779) lists every week explicitly.

**Source grounding:** PRD prescribes "Phase 1 (Sprint 1-3)" + "Phase 2 (Sprint 4-6)" = 6 sprints × 2 weeks = **12 calendar weeks**. TDD Section 23.1 anchors M1 → M5 on a fortnightly cadence with the same total. V1's 11-week active window + 2-week stabilization tail = 13 weeks total, which rounds to the source intent.

**Why this matters:** V2 Section 11 labels the plan "Total Duration: 22 weeks (~5.5 months), Sprint 1 through Sprint 11" while simultaneously hitting the TDD's target dates (M1: 2026-04-14, M5: 2026-06-09). 22 weeks starting Sprint 1 would land GA in early September 2026 if sprints are 2 weeks each, or November 2026 if sprints are 1 week. Either way, V2's own duration label contradicts its own dates.

**Diff points:** C-001, C-002, X-001.

### Strength 2: SOC2 audit infrastructure exists from day 1

**V1 evidence:** D-102 (M1): `migrations/0002_audit_log.sql` with 90-day retention job spec, bumped to 12 months via SEC-3 (CC1). M2 D-206: "Audit-log integration for `login_success`, `login_failure`, `token_refresh_success`, `token_refresh_failure`." M3 D-306 adds reset and lockout events.

**Source grounding:** PRD Constraints: "All auth events must be logged for SOC2 audit trail requirements." PRD Legal/Compliance row references SOC2 audit-logging finding. The PRD's executive summary calls SOC2 readiness one of three business outcomes ($2.4M ARR, churn, **SOC2 audit gate**).

**Why this matters:** V2 places the audit log table in M3 (D-028). That means login (M1), registration (M1), and token refresh (M2) events have no structured audit row for 8-12 weeks of V2's own schedule. Application logs are not audit logs — they have no enforced retention, no immutable append-only semantics, and no queryable schema. V2 is in violation of the PRD constraint during M1 and M2.

**Diff points:** C-004, X-003.

### Strength 3: Audit retention conflict flagged, not silently resolved

**V1 evidence:** OQ-R1 (Section 11.2): "Audit-log retention: TDD §7.2 says 90 days, PRD legal/compliance row says 12 months. Which wins?" with explicit decision owner (security + compliance) and target (before M1 D-102 commit). CC1 SEC-3 documents the gap-resolution path: "bump audit log retention to 12 months in D-102 to satisfy the SOC2 row."

**Source grounding:** TDD Section 7.2 explicitly says 90-day retention; PRD legal/compliance row explicitly says 12 months. Both are in the source.

**Why this matters:** V2 D-033 states "12-month audit log retention policy enforcement" without acknowledging the TDD's 90-day specification. Silent overrides of the TDD are exactly what creates downstream confusion when an engineer reads the TDD for implementation guidance and finds it disagrees with the roadmap. V1's OQ-R1 forces an explicit reconciliation event before D-102 commits.

**Diff points:** C-005, X-008.

### Strength 4: Formal state machines remove implementation ambiguity

**V1 evidence:** Section 9 defines three state machines:

- 9.1 Refresh-token: `issued → rotated | revoked | expired | reused` with explicit guard "reused is reachable from rotated or revoked" and explicit consequence "revokes the entire token family"
- 9.2 Account lockout: `unlocked ⟶ locked ⟶ unlocked` with the security choice "successful login during the window does NOT reset the failure counter"
- 9.3 Password-reset token: `pending ⟶ consumed | expired` with guard "issuing a new reset request while a pending token exists invalidates the prior token"
- 9.4-9.5 audit-write ordering + DB transaction scope for `register()` and `confirmPasswordReset()`

**Why this matters:** V2 has nothing equivalent. A developer implementing `TokenManager.refresh()` from V2 alone does not know that reuse-after-rotation must revoke the family lineage, not just the reused token. This is the entire OWASP refresh-token-rotation pattern. Silence here means each implementer invents their own answer.

**Diff points:** U-001, U-002, S-007, C-009.

### Strength 5: Token family concept prevents replay-across-chain attacks

**V1 evidence:** Section 9.1 — "reused transition revokes the entire token family (all descendants of the original issuance)." Risk R-111 ties this to "Refresh-token replay after rotation" with mitigation "rotation invalidates old token; reuse-detection revokes entire family."

**Source grounding:** TDD Section 12 explicitly references refresh-token rotation. The "family" concept is the canonical OWASP/IETF interpretation of rotation-with-reuse-detection.

**Why this matters:** V2 mentions "atomic Redis operations" for rotation but never defines what happens when a rotated token is reused. Under V2's design, reuse-detection logic is undefined. Under V1's design, reuse triggers revocation of every refresh token descended from the original login event — which is the only safe interpretation.

**Diff points:** U-002, C-009.

### Strength 6: Measurable enumeration-timing gate

**V1 evidence:** QA-6 (CC3): "Enumeration-timing test — assert <50ms variance between unknown-user / wrong-password 401 responses, and <30ms variance between reset-request for registered / unregistered email." M1 exit criteria: "identical timing within 50ms tolerance between unknown-user and wrong-password paths."

**Why this matters:** V2 edge case table says "identical response" but provides no timing target. A 401 that takes 5ms for unknown-user and 310ms for wrong-password is technically "identical" in body but trivially distinguishable via timing side-channel. V1's <50ms / <30ms turns the anti-enumeration requirement into a CI gate.

**Diff points:** U-004, C-015.

### Strength 7: Chaos-testing track validates failure modes before production

**V1 evidence:** QA-7 (CC3): "Chaos test — Redis down test, PostgreSQL failover test, SendGrid down test." TDD Section 12 fallback semantics (`/auth/refresh` returns 503 on Redis outage) are exit-criterion items in M2.

**Why this matters:** V2 has integration tests but no chaos track. The rollback procedure in V2 Section 12.1 describes what to do when Redis is unavailable, but without a chaos test that simulates the failure, the team cannot verify the 503 fallback works until production.

**Diff points:** U-005, C-014.

### Strength 8: Multi-tab and tab-close behavior specified

**V1 evidence:** M4 scope (lines 253-254): "`AuthProvider` clears in-memory tokens on `beforeunload`" and "Multi-tab coordination: BroadcastChannel API to keep tokens consistent when the user logs out in one tab." M4 exit criterion: "Multi-tab logout works: logging out in tab A clears auth in tab B within 1 second."

**Why this matters:** V2 mentions tab-close risk but has no `beforeunload` deliverable and no multi-tab coordination at all. In a real SPA, logout-in-tab-A while tab-B remains authenticated is a visible UX defect that creates customer-support tickets. V1 closes it.

**Diff points:** U-003, U-015, C-010, C-012.

### Strength 9: Governance cadence operationalizes the roadmap

**V1 evidence:** Section 15 communication & governance table — weekly status, weekly burndown, bi-weekly risk register review, as-needed ADRs, go/no-go at end of M5-5B, post-mortem within 48 hours.

**Why this matters:** V2 has no governance cadence. Roadmaps without review rhythms drift. V1's table maps directly onto SoC2 evidence requirements (regular risk reviews are auditable artifacts).

**Diff points:** U-007, S-009.

### Strength 10: Personas coverage check verifies no orphaned user

**V1 evidence:** Section 13 explicitly maps Alex, Jordan, Sam to milestones with deliverable IDs.

**Why this matters:** V2 names personas inline but never verifies coverage. (I concede V2's D-030 is a stronger Jordan deliverable than V1's CC2 OBS dashboards — see Concession 4.)

**Diff points:** U-006, S-008.

---

## Weaknesses Identified in Variant 2

### Weakness 1: Internally contradictory duration

**V2 evidence:** Section 11 line 739 — "Total Duration: 22 weeks (~5.5 months), Sprint 1 through Sprint 11." But milestone target dates are M1: 2026-04-14, M2: 2026-04-28, M3: 2026-05-12, M4: 2026-05-26, M5: 2026-06-09 — exactly the TDD's fortnightly cadence. From M1 kickoff (Sprint 1) to M5 GA (Sprint 11) is ~22 weeks only if every sprint is 1 week long, which V2 never claims and which contradicts every standard 2-week sprint convention.

**Why this matters:** A reader following V2's sprint labels in good faith would plan staffing, contractor procurement, and dependent teams' integrations for a 22-week schedule. The actual schedule per V2's own dates is half that. This is not a minor labeling issue — it's the document's primary structural defect. (V2's advocate concedes this; I am citing it because it materially undermines V2's claim to "operational honesty.")

**Diff points:** C-001, C-002, X-001.

### Weakness 2: 8-12 week SOC2 audit-logging gap

**V2 evidence:** D-028 (M3): "Audit log table in PostgreSQL." Until M3 completes, no audit log table exists. M1-M2 events (login success/failure, registration, token refresh) have no structured audit row.

**Source grounding:** PRD Constraints: "All auth events must be logged for SOC2 audit trail requirements." The PRD does not say "auth events from M3 onward."

**Why this matters:** SOC2 evidence is retrospective. An auditor in Q3 2026 asking "show me every login event from launch" gets an answer of "we have application logs from M1 and audit-table rows from M3 onward" — which is not the same as a single queryable audit log. V2's concession 2 acknowledges this gap but does not close it.

**Diff points:** C-004, X-003.

### Weakness 3: Silent override of TDD audit-retention figure

**V2 evidence:** D-033: "12-month audit log retention policy enforcement" with no acknowledgment of TDD Section 7.2's 90-day figure.

**Why this matters:** When the engineering team reads the TDD for storage sizing (90 days = ~1.5 GB at conservative volume) and the roadmap for compliance (12 months = ~6 GB), they get conflicting answers. V1's OQ-R1 forces a resolution event; V2 silently picks one side. This is exactly the failure mode the PRD/TDD conflict resolution process is supposed to prevent.

**Diff points:** C-005, X-008.

### Weakness 4: No token family concept

**V2 evidence:** D-012 mentions "refresh token rotation" and risk RR-011 mentions atomic operations, but no deliverable defines reuse-detection-revokes-family.

**Why this matters:** Under V2's design, what happens when an attacker exfiltrates a refresh token and uses it after the legitimate client has rotated to a new one? V2's spec says "single-use refresh tokens" but doesn't define the consequence of detecting a reuse. The OWASP/IETF-canonical answer (revoke the entire family) is not in V2's deliverables. An implementer would either invent this or, worse, only revoke the reused token — leaving the attacker's other descendants valid.

**Diff points:** U-002, C-009.

### Weakness 5: No state machine formalization

**V2 evidence:** No section equivalent to V1 Section 9.

**Why this matters:** V2 concedes this. The roadmap consequence is that M2 and M3 implementations are at higher risk of inconsistent state-handling across the team. The TDD does not provide these state machines either — the roadmap is the natural place to surface them as deliverable-level requirements.

**Diff points:** S-007, U-001.

### Weakness 6: No enumeration-timing variance gate

**V2 evidence:** Section 7.3 edge case table — "identical response" with no timing variance target.

**Why this matters:** "Identical response" is uncheckable. A test that compares response bodies will pass even if the timing channel leaks. V1's <50ms / <30ms gates are CI-enforceable.

**Diff points:** U-004, C-015.

### Weakness 7: No chaos engineering track

**V2 evidence:** Testing workstream (Section 4.3) lists unit, integration, E2E, and k6 load testing. No chaos tests.

**Why this matters:** V2's own rollback triggers (Section 12.3) list Redis cluster failure as a failure mode requiring rollback. Without a chaos test that simulates Redis failure, the rollback procedure is unverified until production.

**Diff points:** U-005, C-014.

### Weakness 8: Open-ended async-email infrastructure expands the M3 scope without budget update

**V2 evidence:** OQ-A recommendation (Section 9.1): "Asynchronous via Redis-backed job queue (Bull/BullMQ). Avoids blocking HTTP response. Provides retry semantics. Adds ~50 lines of code + Redis queue infrastructure." But the cost projection (Section 10.3) still shows Redis at $100/month with no upgrade for the job queue workload.

**Why this matters:** Bull/BullMQ adds per-job memory (job data, retry metadata, completed-job retention). The 1 GB Redis sized for ~100K refresh tokens does not have headroom for a job queue. V2's capacity plan is internally inconsistent with its own async-email recommendation. (See my QUALIFY on A-012 below.)

**Diff point:** C-020 + capacity-vs-OQ-A interaction.

---

## Concessions

I concede the following genuine weaknesses in Variant 1:

### Concession 1: V1's lockout placement in M3 leaves a brute-force window

V1 places `LoginAttemptTracker` (D-305) in M3. From M1 close (week 2) through M3 close (week 6), the public `/auth/login` endpoint relies only on gateway-level rate limiting (10/min/IP per R-102) and bcrypt cost-12 latency for brute-force defense. The PRD risk analysis rates brute-force at High probability. Four weeks of unmitigated exposure on a public endpoint is a real gap.

**Partial defense (not full):** R-102 mitigation lists "rate limiting 10/min/IP at gateway" as the M1-day-1 defense, and bcrypt cost-12 adds ~300ms per attempt, making large-scale brute-force computationally expensive even without lockout. The CC1 SEC-1 NIST review starts in week 1 and would flag the gap. But these are mitigations, not equivalents. V2's M1 placement is correct on this point. The right fix is to move D-305 into M1 as a minimal counter-and-threshold (per V2 advocate's correct observation that this is ~20-30 lines of code) and refine the sliding-window semantics in M3.

### Concession 2: V1's legacy-auth rollback path is infeasible on greenfield

V1 Section 12.2 step 2 references "traffic routes back to legacy auth." The PRD explicitly says "the platform currently operates without any user identity system." There is no legacy auth. V1's rollback procedure cannot work as written. The correct fallback for greenfield is V2's "maintenance page or unauthenticated read-only mode," and V1's rollback section needs to be rewritten accordingly. This is a real defect.

### Concession 3: V1's staffing detail is too thin to be operational

V1 Section 14 single-row staffing ("2 backend + 1 frontend FTE + 0.5 SRE + 0.25 security review") tells a hiring manager nothing actionable about timing. V2's per-sprint allocation table is materially better. A future revision of V1 should adopt V2's table format.

### Concession 4: V1 lacks a dedicated admin audit-log query deliverable

V1 has the audit table (D-102) and the audit events (D-206, D-306) but no D-NNN that delivers the query interface. Jordan persona's JTBD ("see who attempted access") needs a queryable surface. V2's D-030 is the right pattern.

---

## Shared Assumption Responses (MANDATORY)

The diff analysis promotes **A-005, A-008, A-009, A-010, A-011, A-012** to [SHARED-ASSUMPTION] status. Verdicts below.

### A-005 — NTP synchronization on all AuthService nodes is operational

- **VERDICT: ACCEPT**
- **RATIONALE:** Both variants depend on the TDD §12 5-second clock-skew tolerance. NTP is the standard mechanism. Without NTP, JWT validation fails non-deterministically across pods. V1 risk R-109 ("Clock skew between API nodes invalidates valid tokens") names NTP enforcement explicitly. V2 RR-012 mentions NTP synchronization as a mitigation. Both variants converge — assumption is valid and necessary.

### A-008 — Frontend is a React SPA with React Router (or equivalent)

- **VERDICT: ACCEPT**
- **RATIONALE:** TDD Section 10 specifies `AuthProvider` with `children: ReactNode` — a React-specific signature. Both variants describe `AuthProvider` as a React context. If the frontend were Angular/Vue/Svelte, M4 deliverables are different artifacts entirely. The assumption is well-grounded in the source TDD; V1's BroadcastChannel and `beforeunload` choices in particular presume browser-SPA semantics consistent with React.

### A-009 — No server-side session affinity is required

- **VERDICT: ACCEPT**
- **RATIONALE:** TDD Section 6.4 explicitly chooses stateless JWT verification. Both variants describe a 3-pod baseline with HPA to 10 — a model that breaks under sticky sessions. Redis is the only stateful component, and it is accessed by token-hash key rather than by user/session affinity. The assumption holds.

### A-010 — Named security reviewer at ≥25% capacity during gates

- **VERDICT: ACCEPT (with elaboration)**
- **RATIONALE:** Both variants have security gates that block GA. V1 CC1 specifies "Weekly checkpoint review; gate at the end of M2, M4, and M5." V2 Section 10.1 allocates Security Engineer at 25% for Sprint 1-2 and Sprint 9-10. The assumption that this person exists and is allocated is load-bearing — without them, the security review at M5 (D-507) cannot complete and GA is blocked. V1's failure to make this allocation explicit in a staffing table is a related weakness (see Concession 3).

### A-011 — bcryptjs is the v1.0 hashing library; argon2id is v1.1+

- **VERDICT: ACCEPT**
- **RATIONALE:** TDD Section 6.4 names bcrypt as the choice with "via PasswordHasher." V1 M1 scope explicitly says "wrapper around `bcryptjs` with cost factor 12 and pluggable interface for future argon2id migration." V2 references bcrypt throughout. The pluggable interface in V1 D-103 keeps the door open for argon2id without making it a v1.0 commitment. Assumption holds for v1.0.

### A-012 — Redis is provisioned for auth workloads only (~100K tokens at 1 GB)

- **VERDICT: QUALIFY**
- **RATIONALE:** V1's design uses Redis for refresh tokens + lockout sliding window + (optionally per ADR D-308) password-reset tokens. V2 adds Bull/BullMQ as the async-email queue, which co-locates a job queue on the same Redis instance. The TDD §25.3 sizing of "~100K refresh tokens, ~50 MB" was computed assuming token-only usage. If V2's async-email recommendation is adopted, the 1 GB Redis must be re-sized to include queue overhead (job payloads, retry metadata, completed-job retention) OR the job queue must run on a separate Redis instance/namespace. V1 keeps the assumption clean by not adding a queue dependency (the SendGrid client wrapper in D-303 handles retries directly). The assumption is broadly correct but needs a capacity adjustment if Bull/BullMQ is adopted.

---

## Per-Diff-Point Position Tally

| Point | Topic | Winner | One-sentence rationale |
|---|---|---|---|
| C-001 | Total roadmap duration | **V1** | PRD's 6 sprints × 2 weeks = 12 weeks; V1's 11-week active + 2-week tail matches; V2's "22 weeks" label contradicts its own target dates. |
| C-002 | Per-milestone duration | **V1** | TDD §23.1 specifies fortnightly cadence; V1 honors it; V2's "4 weeks per milestone" claim cannot reach Jun-9 GA from Sprint 1 starting on schedule. |
| C-003 | Lockout placement | **V2 (concede)** | Public login endpoint without lockout for 4+ weeks is unacceptable; V1 should move D-305 into M1. |
| C-004 | Audit log placement | **V1** | SOC2 requires all auth events logged from day 1; V2's M3 deferral leaves 8-12 weeks of M1/M2 events unstructured. |
| C-005 | Audit retention conflict handling | **V1** | V1 explicitly flags TDD-90d vs PRD-12m via OQ-R1; V2 silently picks 12 months. |
| C-006 | Reset token storage medium | **Tie** | Redis-TTL (V1) and DB-hashed (V2) are both valid; trade-off documented in V1 ADR D-308. |
| C-007 | Max refresh tokens per user | **V2** | V2's 10-token cap with FIFO eviction is a concrete v1.0 policy; V1's "no cap, observe" defers a sizing-relevant decision. |
| C-008 | Lockout auto-unlock timing | **V1** | 15-min sliding window aligns with TDD §13; V2's 30-min recommendation is more punitive without source support. |
| C-009 | Token family concept | **V1** | Reuse-detection-revokes-family is the OWASP-canonical pattern; V2 omits it. |
| C-010 | Multi-tab coordination | **V1** | BroadcastChannel API closes a visible SPA UX defect; V2 silent. |
| C-011 | Silent refresh timing | **V1** | `expiresIn - 60s` is implementable; V2's "before expiry" is ambiguous. |
| C-012 | Tab-close behavior | **V1** | Explicit `beforeunload` handler; V2 mentions risk only. |
| C-013 | Lighthouse score | **V1** | Measurable frontend gate; V2 silent. |
| C-014 | Chaos testing | **V1** | QA-7 validates failure modes before production; V2 has none. |
| C-015 | Enumeration timing variance | **V1** | <50ms / <30ms gates are CI-enforceable; V2's "identical" is not. |
| C-016 | Concurrent refresh race | **Tie** | SET-NX (V1) and MULTI/EXEC (V2) are both valid serialization mechanisms. |
| C-017 | Logout endpoint | **V1** | V1 raises OQ-R4 forcing a decision; V2 silently picks client-side discard. |
| C-018 | Admin audit query | **V2 (concede)** | V2 D-030 is a concrete Jordan-persona deliverable absent in V1. |
| C-019 | GDPR right-to-erasure | **V1** | V1 flags as hard legal obligation; V2 lists as "Post-v1.0" without urgency. |
| C-020 | Async email recommendation | **Tie (V2 more specific, V1 cleaner)** | V2 names Bull/BullMQ but creates A-012 capacity issue; V1 keeps SendGrid retries in-process. |
| C-021 | Feature flag removal timeline | **V2 (concede)** | Appendix B's per-flag lifecycle is operationally tighter. |
| C-022 | Legacy auth assumption | **V2 (concede)** | Greenfield per PRD; V1's rollback path is infeasible as written. |
| C-023 | Pentest cost | **V2** | Budget enables procurement; V1 silent. |
| C-027 | Migration locking | **V1** | R-115 names pg-online-schema-change; V2 silent. |
| C-028 | Frontend+backend coordinated release | **V1** | R-116 names the split-brain risk; V2 silent. |
| C-029 | Beta buffer | **V2** | 1-week hidden buffer is standard PM practice; V1 has none. |
| S-007 | State machine formalization | **V1** | Section 9 prevents ambiguous token/lockout/reset transitions. |
| S-008 | Personas coverage check | **V1** | Section 13 verifies no orphaned persona. |
| S-009 | Governance cadence | **V1** | Section 15 operationalizes review rhythm. |
| S-012 | Team composition | **V2 (concede)** | Per-sprint allocation table is actionable. |
| S-013 | Post-GA planning | **V2** | v1.1/v2.0 sequencing prevents orphan release. |
| X-001 | Duration contradiction | **V1** | V1 internally consistent; V2's 22wk label contradicts its dates. |
| X-002 | Lockout milestone | **V2** | M1 placement closes brute-force window. |
| X-003 | Audit log milestone | **V1** | SOC2 day-1 coverage required by PRD constraint. |
| X-004 | Legacy auth existence | **V2** | Greenfield per PRD. |
| X-005 | Lockout auto-unlock timing | **V1** | 15-min aligns with TDD §13. |
| X-006 | Max refresh tokens | **V2** | 10-token cap is a concrete v1.0 policy. |
| X-007 | Reset token storage | **Tie** | Both architecturally valid. |
| X-008 | Audit retention source truth | **V1** | Explicit conflict flag beats silent override. |

**Net tally:** V1 wins on the security and engineering-discipline axes (state machines, token family, audit-day-1, enumeration timing, chaos testing, OQ-conflict flagging, multi-tab UX, governance, personas, NTP/migration/coordination risks). V2 wins on the operational axes (staffing detail, post-GA continuity, feature-flag lifecycle, admin audit query, pentest budget, greenfield rollback path, lockout placement, beta buffer, refresh-token cap).

**Synthesis position for round 2:** Adopt V1's milestone cadence (11 weeks), state machines, audit-day-1, OQ-R1 conflict-flagging discipline, token-family semantics, enumeration-timing gates, chaos track, BroadcastChannel/`beforeunload`, governance section. Adopt V2's per-sprint staffing table, post-GA Section 13, feature-flag lifecycle appendix, admin audit query D-030, greenfield rollback path, lockout-in-M1, pentest budget, beta buffer, refresh-token cap. The merged artifact dominates both.
