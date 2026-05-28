# Round 2 — Variant 2 Rebuttal (sonnet)

## Response to Criticisms

- **Criticism**: V2's "22 weeks" duration label contradicts its own target dates (M5 GA 2026-06-09), making the document internally inconsistent (C-001, C-002, X-001).
- **Response**: **CONCEDE (reaffirmed).** I conceded this in R1 and V1's R2 new evidence clinches it. The PRD Phasing section explicitly says "Phase 1 (Sprint 1-3)" + "Phase 2 (Sprint 4-6)" = 6 sprints. At 2-week sprint cadence, that is 12 calendar weeks. V2's "22 weeks, Sprint 1-11" label is a documentation error that must be corrected. The merged roadmap should adopt V1's 11-week active window with 2-week stabilization tail, augmented by V2's 1-week hidden beta buffer.
- **Diff IDs**: C-001, C-002, X-001.

- **Criticism**: V2 defers audit logging to M3 (D-028), leaving 8-12 weeks of M1/M2 events unstructured, violating the PRD's "all auth events must be logged for SOC2 audit trail requirements" (C-004, X-003).
- **Response**: **CONCEDE.** V1 is correct that application logs are not audit logs -- they lack enforced retention, immutable append-only semantics, and queryable schema. My R1 concession 2 caveat ("structured logging partially mitigates") understated the gap. The PRD constraint is unconditional ("All auth events"), not "all auth events from M3 onward." The merged roadmap must place the audit table in M1 (adopt V1's D-102) and add query events progressively through M2 and M3.
- **Diff IDs**: C-004, X-003.

- **Criticism**: V2 silently overrides the TDD's 90-day audit retention with 12-month retention without acknowledging the conflict (C-005, X-008).
- **Response**: **CONCEDE.** V1's OQ-R1 mechanism -- flag the conflict, name the decision owner, set a resolution deadline before D-102 commit -- is the correct process. Silent overrides are exactly what causes downstream confusion. The merged roadmap should adopt V1's conflict-flagging discipline AND V1's R2 refined wording: "retention parameterized, default 90d per TDD, set to 12 months pending OQ-R1 resolution before M1 commit."
- **Diff IDs**: C-005, X-008.

- **Criticism**: V2 lacks state machine formalization (S-007, U-001), leaving token lifecycle transitions undefined for implementers.
- **Response**: **CONCEDE (with qualification).** V1 is correct that the TDD does not contain these state machines and that the roadmap is the natural place to surface them. I no longer argue "state machines belong in the TDD" -- that position fails because the TDD lacks them. The merged roadmap should adopt V1's Section 9 state machines (refresh-token, lockout, reset-token) and V1's Section 9.4-9.5 (audit ordering, DB transaction scope). **Qualification**: these state machines should be labeled as "roadmap-level acceptance criteria for M2/M3 deliverables" rather than as a standalone section, so they are tied to specific deliverable IDs and exit criteria rather than floating as architectural prose.
- **Diff IDs**: S-007, U-001, U-002, C-009.

- **Criticism**: V2 lacks chaos testing (U-005, C-014), leaving rollback triggers unverified until production.
- **Response**: **CONCEDE.** Already conceded in R1. V1's QA-7 track (Redis down, PostgreSQL failover, SendGrid down) is a concrete, testable deliverable. The merged roadmap should adopt it.
- **Diff IDs**: U-005, C-014.

- **Criticism**: V2 lacks enumeration timing variance targets (U-004, C-015), making the anti-enumeration requirement untestable.
- **Response**: **CONCEDE.** Already conceded in R1. V1's <50ms (login) and <30ms (reset-request) gates are CI-enforceable. "Identical response" without a timing target is an aspiration. Adopt V1's QA-6.
- **Diff IDs**: U-004, C-015.

- **Criticism**: V2's Bull/BullMQ recommendation creates undisclosed infrastructure dependency -- queue monitoring, runbook, stuck-job recovery, queue-poisoning surface -- not budgeted in the cost table (C-020, new V1 R2 criticism).
- **Response**: **PARTIAL REBUTTAL.** V1 overstates the complexity. Bull is the most widely deployed job queue in the Node.js ecosystem (>14M weekly npm downloads). Its monitoring is standard (Bull Board UI ships with the library), its retry semantics are declarative (configurable attempts + backoff), and its dead-letter handling is built-in (the `failed` queue). These are not "undisclosed" -- they are standard Bull operational patterns any Node.js team knows. The runbook concern is valid but modest: a drain procedure is `queue.pause(); queue.clean(0, 'completed'); queue.close()` -- three commands, not an operational epic. **However**, V1 is correct that V2's cost table does not account for the additional Redis memory. The merged roadmap should either (a) add a line item for queue Redis (~$30-50/month for a dedicated small instance) or (b) re-size the existing Redis allocation. On the question of in-process retry (V1) vs. queue (V2): for v1.0 with a single email template (password reset), in-process retry with exponential backoff is genuinely simpler and sufficient. The queue approach becomes necessary when email volume grows (welcome emails, MFA codes, etc. in v1.1+). The merged roadmap should adopt V1's in-process approach for v1.0 and note Bull/BullMQ as the v1.1 recommendation when email templates multiply.
- **Diff IDs**: C-020.

- **Criticism**: V2's "soft M3-to-M4 dependency" parallelization claim is illusory because M2 is the binding constraint for M4 frontend work -- LoginPage/RegisterPage depend on M2 endpoints, not M3 (S-017, new V1 R2 criticism).
- **Response**: **PARTIAL CONCESSION.** V1 is correct that M2 is the binding constraint for LoginPage, RegisterPage, and AuthProvider. M4 cannot start meaningful frontend work until M2's `/auth/login`, `/auth/register`, `/auth/refresh`, `/auth/me` endpoints are stable. However, V1 overstates by calling the parallelization gain "mostly illusory." The password-reset pages (`/forgot-password`, `/reset-password`) genuinely depend on M3's `/auth/reset-request` endpoint. Under V1's model, these pages cannot even begin until M3 closes. Under V2's model, M4 starts frontend scaffolding (AuthProvider shell, routing, shared components) in parallel with M3, building the M2-dependent pages first and the M3-dependent pages when M3 closes. This is a real -- if modest -- parallelization gain of approximately 1 week. The merged roadmap should use V2's soft-dependency model but with the honest acknowledgment that M2 is the primary constraint.
- **Diff IDs**: S-017.

---

## Response to V1's Round 2 Concessions & Position Flips

### Accepted Concessions

1. **Lockout-in-M1 (C-003/X-002).** V1 concedes outright and sharpens: "the fix is small (V2-advocate is correct that a counter+threshold is approximately 20-30 lines of code)." V1 also cites PRD R-002 mitigation column listing both lockout AND rate limiting as required mitigations, making M1 lockout a PRD compliance requirement, not just good practice. This strengthens the merged outcome: lockout in M1 is now grounded in both security rationale AND PRD compliance.

2. **Greenfield rollback (C-022/X-004).** V1 concedes and sharpens to "P1-incident failure mode" -- acknowledging that following V1's procedure during an actual incident would fail at step 2. This is the correct severity assessment. The merged roadmap adopts V2's maintenance-page fallback and eliminates the infeasible legacy path.

3. **Beta-to-GA buffer (C-029, U-028).** V1 concedes and calls it "standard PM practice." V1 also notes that its own "2-week stabilization tail" is post-GA, not pre-GA, so no pre-GA float exists in V1. The merged roadmap adopts V2's 1-week hidden buffer between Beta and GA.

4. **Post-GA Section 13 structure (S-013).** V1 concedes on structure (adopt V2's three-subsection layout) but notes that V2's quarter assignments (Q3 2026, Q4 2026) are not source-grounded -- the PRD says "planned for v1.1" without dates. **This is a fair point.** V2's quarter targets are estimates, not commitments. The merged roadmap should adopt V2's structure but label quarters as "target, subject to PM confirmation." V1 also flags the ongoing-maintenance subsection (key rotation, bcrypt review, retention verification, dependency updates, capacity review) as particularly valuable for SOC2 auditors. Agreed -- this is a strong contribution.

5. **Staffing table (S-012).** V1 concedes. The merged roadmap adopts V2's 10-row per-sprint allocation table.

6. **Admin audit query (C-018).** V1 concedes. D-030 is adopted into the merged roadmap.

7. **Three-phase rationale (U-021).** V1 calls this "a documentation-completeness issue, not a structural defect" and proposes a one-paragraph "phase-to-milestone mapping" note. **Partially accepted.** A mapping note is the minimum; the merged roadmap should include it. But V2's explicit "Why Three Phases, Not Two" section is more than a mapping note -- it is an engineering rationale that prevents a reader from questioning the divergence. Include the rationale, not just the mapping.

8. **Audit retention wording (C-005).** V1 proposes: "retention parameterized, default 90d per TDD, set to 12 months pending OQ-R1 resolution before M1 commit." This is good wording. Adopt it. V1 also concedes the storage cost is unmodeled (~6 GB at 12-month retention) and should be line-itemed. Agreed.

### Challenged Concessions

1. **V1's partial concession on post-GA quarter commitments is directionally correct but undercuts the roadmap's purpose.** A roadmap that says "v1.1 at some point, v2.0 at some point" provides no coordination value. The merged roadmap should include V2's quarter targets as "planning assumptions" (not commitments) and note that PM confirmation is a pre-GA action item. This preserves coordination value without over-committing.

### Counter-Rebuttal: C-020 Flip (Async Email)

V1 flips C-020 from Tie to V1, arguing Bull/BullMQ creates "undisclosed complexity." I counter:

**Bull is standard Node.js tooling.** With >14M weekly downloads, Bull is to Node.js what Sidekiq is to Ruby or Celery is to Python. It is not a niche dependency. A Node.js engineering team that cannot operate Bull cannot operate a production application of any complexity.

**The monitoring concern is overstated.** Bull Board (the standard monitoring UI) ships as a companion package and provides queue depth, retry rate, and failed-job inspection out of the box. This is not custom monitoring -- it is a one-line middleware addition.

**The queue-poisoning concern is generic.** Any system that accepts input and processes it asynchronously has this surface. It is not unique to Bull. Input validation at the HTTP layer (which both variants include) mitigates it.

**The runbook concern is real but bounded.** A drain procedure during deploys and stuck-job recovery are standard operational patterns documented in Bull's README. They are not "undisclosed."

**However**, I concede V1's core point on v1.0 scope: with a single email template (password reset), in-process retry with exponential backoff is simpler and sufficient. Bull becomes valuable when v1.1 adds welcome emails, MFA codes, email verification, and password-change notifications. **The merged roadmap should adopt V1's in-process approach for v1.0 and name Bull/BullMQ as the v1.1 async recommendation.** This is the honest resolution: V1 wins v1.0, V2 wins the forward-looking recommendation.

---

## Updated Assessment of Variant 1

### V1 arguments now MORE persuasive

1. **Duration arithmetic (C-001/C-002).** V1's R2 new evidence -- PRD Phasing section explicitly says "Phase 1 (Sprint 1-3)" + "Phase 2 (Sprint 4-6)" = 6 sprints -- is decisive. I conceded this in R1 but V1's source citation makes it irrefutable. The PRD itself prescribes 12 weeks, not 22.

2. **Audit-day-1 as PRD compliance, not just best practice (C-004).** V1's framing that the PRD constraint ("All auth events must be logged") is unconditional -- not "all auth events from M3 onward" -- is correct. My R1 "structured logging partially mitigates" caveat was too generous to V2. Application logs are not audit logs.

3. **Token family omission as a security gap (C-009).** V1's R2 point is correct: the TDD does not contain token-family semantics, so "belongs in the TDD" is not a valid rebuttal. The roadmap must specify reuse-detection consequences or the implementer invents them.

4. **V1's M2-is-binding-constraint point on M4 parallelization (S-017).** V1 correctly identifies that LoginPage/RegisterPage depend on M2 endpoints, making M2 -- not M3 -- the binding constraint for M4. My "soft M3-to-M4 dependency" framing was technically correct but operationally misleading. The parallelization gain is real but modest (~1 week).

### V1 arguments still UNPERSUASIVE

1. **V1's 30-minute lockout critique (X-005).** V1 argues V2's 30-minute auto-unlock is "more punitive without source support." This is correct -- TDD Section 13 grounds 15 minutes. But V1's R2 new evidence that the 15-minute window is a sliding-window counter reset (not an auto-unlock timer) introduces ambiguity that neither variant fully resolves. The merged roadmap should adopt 15-minute auto-unlock aligned with the TDD and make the sliding-window reset behavior explicit in the state machine.

2. **V1's claim that its single-row staffing is "operational" (S-012).** V1 conceded this but the original argument was never persuasive. A staffing row without timing tells a hiring manager nothing about when to request headcount.

3. **V1's governance cadence as a differentiator (S-009).** V1's Section 15 is valuable, but it is standard PM practice that any competent team would establish. Its absence from V2 is a gap, but not a structural deficiency. The merged roadmap should adopt it.

### Strongest remaining V1 weaknesses

1. **No pre-GA buffer.** An 11-week plan with zero float and sequential milestones is brittle. Even with V2's 1-week buffer adopted, V1's original structure has no internal milestone float.

2. **No post-GA planning.** Without V2's Section 13, stakeholders have no answer to "what happens after GA?" This is a coordination failure in a document whose purpose is coordination.

3. **Infeasible rollback path (now conceded).** This was V1's most dangerous weakness and V1 correctly conceded it.

---

## New Evidence

1. **PRD R-002 mitigation column lists lockout AND rate limiting as co-required mitigations.** V1 cited this in R2. This is significant because it means M1 lockout is not just "good practice" but PRD-mandated. A roadmap that defers one of the PRD's two named brute-force mitigations for 4 weeks is non-compliant with the PRD's own risk treatment. This strengthens the lockout-in-M1 argument from "security best practice" to "PRD compliance requirement." (Affects: C-003, X-002.)

2. **TDD Section 25.3 Redis sizing is ~50 MB, not 1 GB.** V1's R2 new evidence clarifies that the TDD sizes Redis at ~50 MB for ~100K refresh tokens. V2's cost table shows Redis at $100/month, which is for a 1 GB instance (standard managed Redis minimum). This means there IS headroom for a small Bull queue on the same instance -- but the capacity plan should explicitly account for it rather than leaving it implicit. The 50 MB sizing also means the merged roadmap's capacity section should use the TDD's figure, not an assumed 1 GB. (Affects: A-012, C-020.)

3. **TDD Section 19.2 specifies feature flag removal targets.** The TDD says: "Remove AUTH_NEW_LOGIN after Phase 3 GA" and "Remove AUTH_TOKEN_REFRESH after Phase 3 + 2 weeks." V2's Appendix B operationalizes these with concrete sprint deadlines (Sprint 11 + 2 weeks, Sprint 11 + 4 weeks). This is direct TDD-to-roadmap traceability -- V2's flag lifecycle table is not an invention but a faithful rendering of TDD Section 19.2 into sprint-level dates. (Affects: C-021, U-024.)

4. **PRD Non-Goals explicitly version future work.** The PRD Non-Goals section says: "OAuth/OIDC... planned for v2.0" and "MFA... planned for v1.1." V2's Section 13 is not inventing versioning -- it is operationalizing versioning that the PRD already specifies. V1's R2 criticism that V2's quarter assignments are "not source-grounded" is partially correct (the PRD does not give dates), but the versioning itself is PRD-grounded. The merged roadmap should preserve the version-to-feature mapping and add "target quarter, subject to PM confirmation" as the date qualifier. (Affects: S-013, U-023.)

5. **V1 risk R-113: consent must be written in the same transaction as UserProfile.** V1 Section 9.5 documents this as a DB transaction scope requirement. This is a GDPR compliance detail that V2 does not address. The merged roadmap should adopt this transaction-scope specification. (Affects: U-020.)

---

## Per-Diff-Point Position Update

| Diff ID | R1 Position | R2 Position | Changed? | Why |
|---------|-------------|-------------|----------|-----|
| C-001 | Tie (with V2 labeling concession) | V1 | Yes | V1's PRD sprint-count evidence is decisive. |
| C-002 | V1 | V1 | No | TDD fortnightly cadence is explicit. |
| C-003 | V2 | V2 (stronger) | Sharpened | V1 concedes; PRD R-002 co-requires lockout. |
| C-004 | V1 | V1 | No | Audit-day-1 is PRD compliance, not best practice. |
| C-005 | V1 | V1 | No | V1's conflict-flagging is correct; adopt refined wording. |
| C-006 | Tie | Tie | No | Both architecturally valid. |
| C-007 | V2 | V2 | No | 10-token cap is concrete. |
| C-008 | V1 | V1 | No | TDD Section 13 grounds 15-min window. |
| C-009 | V1 | V1 | No | V2 concedes; TDD lacks state machines. |
| C-010 | V1 | V1 | No | V2 has no equivalent. |
| C-011 | V1 | V1 | No | Specificity wins. |
| C-012 | V1 | V1 | No | Explicit handler. |
| C-013 | V1 | V1 | No | Measurable gate. |
| C-014 | V1 | V1 | No | V2 concedes. |
| C-015 | V1 | V1 | No | V2 concedes. |
| C-016 | Tie | Tie | No | Both valid. |
| C-017 | V1 | V1 | No | V1 raises the OQ. |
| C-018 | V2 | V2 | No | D-030 is the right deliverable; V1 concedes. |
| C-019 | V1 | V1 | No | Legal urgency is correct. |
| C-020 | Tie (V2 specific, V1 cleaner) | V1 (v1.0); V2 (v1.1 recommendation) | Changed | V1's in-process approach is simpler for single-template v1.0. Bull is standard but unnecessary overhead for one email type. |
| C-021 | V2 | V2 | No | Appendix B operationalizes TDD Section 19.2. |
| C-022 | V2 | V2 (stronger) | Sharpened | V1 concedes; P1-incident failure mode. |
| C-023 | V2 | V2 | No | Budget enables procurement. |
| C-027 | V1 | V1 | No | V2 silent on migration locking. |
| C-028 | V1 | V1 | No | V2 silent on coordinated release risk. |
| C-029 | V2 | V2 (stronger) | Sharpened | V1 concedes; standard PM practice. |
| S-007 | V1 | V1 | No | V2 concedes; TDD lacks state machines. |
| S-008 | V1 | V1 | No | V2 has no personas check. |
| S-009 | V1 | V1 | No | V2 has no governance section. |
| S-012 | V2 | V2 | No | V1 concedes. |
| S-013 | V2 | V2 (with quarter caveat) | Refined | Adopt structure, mark quarters as "target." |
| S-017 | (not tallied) | V1 (primary), V2 (modest gain) | New | M2 is the binding constraint; parallelization gain is real but ~1 week. |
| X-001 | V1 wins on clarity | V1 | No | V2 conceded. |
| X-002 | V2 | V2 | No | Lockout in M1. |
| X-003 | V1 | V1 | No | SOC2 day-1 required. |
| X-004 | V2 | V2 (sharpened) | Sharpened | P1-incident failure mode. |
| X-005 | V1 | V1 | No | TDD Section 13 grounds 15-min. |
| X-006 | V2 | V2 | No | 10-token cap concrete. |
| X-007 | Tie | Tie | No | Both valid. |
| X-008 | V1 | V1 | No | V1's conflict flagging is correct. |

**Net updated tally:**

- **V1 outright wins:** C-001, C-002, C-004, C-005, C-008, C-009, C-010, C-011, C-012, C-013, C-014, C-015, C-017, C-019, C-020 (v1.0), C-027, C-028, S-007, S-008, S-009, S-017, X-001, X-003, X-005, X-008 = **25 points**
- **V2 outright wins:** C-003, C-007, C-018, C-021, C-022, C-023, C-029, S-012, S-013, X-002, X-004, X-006 = **12 points**
- **Ties:** C-006, C-016, X-007 = **3 points**
- **Split:** C-020 (V1 for v1.0, V2 for v1.1 recommendation)

---

## Final Concessions in This Round

1. **Timeline (C-001, C-002, X-001).** V1 wins. The PRD's explicit sprint count makes V2's 22-week label indefensible. The merged roadmap uses 11-week active + 2-week stabilization + 1-week hidden beta buffer.

2. **Audit log placement (C-004, X-003).** V1 wins. Audit-day-1 is a PRD compliance requirement, not a best practice. The merged roadmap places the audit table in M1.

3. **Audit retention handling (C-005, X-008).** V1 wins. Conflict-flagging via OQ-R1 is the correct process. Silent overrides are a failure mode.

4. **State machines (S-007, C-009).** V1 wins. The TDD lacks these; the roadmap must supply them. My "belongs in the TDD" rebuttal was wrong.

5. **Chaos testing (C-014) and enumeration timing (C-015).** V1 wins. Measurable gates and failure-mode validation are engineering discipline that V2 should have included.

6. **Async email for v1.0 (C-020).** V1 wins. In-process retry is simpler and sufficient for a single email template. Bull is the right call for v1.1+ when templates multiply.

7. **M4 parallelization (S-017).** V1 wins on the primary constraint (M2 binds M4). The parallelization gain is real but modest.

**V2 retains wins on:** lockout placement (C-003), greenfield rollback (C-022), staffing detail (S-012), post-GA planning (S-013), feature flag lifecycle (C-021), admin audit query (C-018), pentest budget (C-023), beta buffer (C-029), refresh token cap (C-007/X-006).

**Synthesis position unchanged from V1's R2 closing:** V1 contributes the security-discipline and engineering-formalization backbone. V2 contributes the operational-polish and procurement-readiness layer. Neither dominates standalone. The merged artifact -- adopting V1's milestone cadence, state machines, audit-day-1, OQ conflict discipline, chaos track, enumeration gates, and governance cadence, plus V2's staffing table, post-GA section, feature-flag lifecycle, admin audit query, greenfield rollback, lockout-in-M1, pentest budget, beta buffer, and refresh-token cap -- dominates both.
