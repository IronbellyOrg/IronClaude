# Refactoring Plan — Merge V1 (Base) + V2 Incorporations + R2.5 Required Additions

## Overview

| Field                       | Value                                                                     |
|-----------------------------|---------------------------------------------------------------------------|
| Base variant                | Variant 1 (opus:architect) — selected per base-selection.md               |
| Incorporated variants       | Variant 2 (sonnet:analyzer) — format/traceability strengths only          |
| Total changes planned       | 14 (7 V2 incorporations + 7 R2.5 HIGH-severity required additions)        |
| Rejected alternatives       | 5 (documented in §Changes NOT Being Made)                                 |
| Overall risk                | Low-Medium (additive changes dominant; one structural resequence in M5)   |
| Review status               | Auto-approved (no `--interactive` flag)                                   |
| Plan timestamp              | 2026-05-22T17:05:00+00:00                                                 |

---

## Planned Changes

### Change #1 — Insert Success Metrics Table

- **Title**: Insert Success Metrics table immediately after Executive Summary
- **Source variant**: V2 §Success Metrics (lines 21-34)
- **Target location**: V1 base, between Executive Summary and Strategic Objectives
- **Integration approach**: INSERT (additive)
- **Rationale**: V1 advocate fully conceded this in R2. V2's 12-metric tabular format with target/baseline/measurement/source columns is structurally superior for SOC2 audit and operational tracking. V1's Strategic Objectives prose can survive as a "Why these metrics" rationale section beneath the table. Debate scoring matrix S-008 confidence 90% (V2 winner).
- **Risk level**: Low (purely additive; no V1 content removed)

### Change #2 — Insert Sprint-Level Breakdown Table

- **Title**: Insert Sprint-Level Breakdown table after Milestones section
- **Source variant**: V2 §Sprint-Level Breakdown (lines 180-188)
- **Target location**: V1 base, after the M1-M5 detailed milestone sections, before Workstreams
- **Integration approach**: INSERT (additive)
- **Rationale**: V1 advocate fully conceded. V2's S1-S6 table with explicit date windows and owner team is required for sprint planning. Modification needed: owner cells reconciled with V1's 5-workstream model (each sprint may have multiple owning streams).
- **Risk level**: Low

### Change #3 — Replace Per-Milestone Exit Criteria with Performance & Reliability Gates Table

- **Title**: Replace Acceptance & Release Gates section with V2's Performance & Reliability Gates table format
- **Source variant**: V2 §Performance & Reliability Gates (lines 225-235)
- **Target location**: V1 base §Acceptance & Release Gates
- **Integration approach**: RESTRUCTURE (replace V1 prose-gate list with V2 table; keep V1's GA criteria as the M5-exit row)
- **Rationale**: V1 advocate conceded. V2's table format with Gate/Threshold/Phase Boundary/Source columns is more traceable than V1's per-milestone prose. V1's "Final GA criteria" 7-item list becomes the M5-exit cluster.
- **Risk level**: Low

### Change #4 — Insert Per-FR Validation Strategy Table

- **Title**: Insert Validation Strategy section with per-FR Unit/Integration/E2E matrix
- **Source variant**: V2 §Validation Strategy (lines 193-199)
- **Target location**: V1 base, after Cross-Cutting Concerns, before Risk Register
- **Integration approach**: INSERT (additive)
- **Rationale**: V1 advocate fully conceded. V2's FR-AUTH-001..005 × Unit/Integration/E2E matrix operationalizes TDD §15.1's 80/15/5 pyramid. Required for audit traceability.
- **Risk level**: Low

### Change #5 — Insert Out-of-Scope Explicit Table

- **Title**: Insert Out-of-Scope explicit deferral table
- **Source variant**: V2 §Out-of-Scope (lines 264-277)
- **Target location**: V1 base, after Risk Register, before Open Questions
- **Integration approach**: INSERT (additive)
- **Rationale**: V1 advocate conceded. Maps each TDD §3.2 NG-001/002/003 + deferred capabilities to their target release. V1 only mentioned non-goals in Objective 4 prose.
- **Risk level**: Low

### Change #6 — Augment Open Questions with Target Resolution Dates

- **Title**: Add Owner + Target Resolution Date columns to V1's Open Questions
- **Source variant**: V2 §Open Questions (lines 282-288) — table format with Owner/Target columns
- **Target location**: V1 base §Open Questions
- **Integration approach**: REPLACE (V1's narrative format → V2's table format; V1's "Recommended position" prose preserved beneath each row)
- **Rationale**: V1 has 8 well-reasoned OQs with recommended positions; V2 has 6 OQs with owners and dates. Merge keeps V1's 8 questions AND V1's recommended positions, but adds V2's Owner + Target Resolution Date columns. Net upgrade for both.
- **Risk level**: Low

### Change #7 — Quote TDD §19.4 Rollback Triggers Verbatim

- **Title**: Quote TDD §19.4 rollback trigger thresholds in M5 Architectural Risks section
- **Source variant**: V2 §Performance & Reliability Gates closing paragraph (lines 237)
- **Target location**: V1 base §M5 Architectural Risks
- **Integration approach**: APPEND
- **Rationale**: V2 quotes "p95 > 1000ms for > 5 min; error rate > 5% for > 2 min; Redis connection failures > 10/min" verbatim from TDD §19.4. V1 mentions rollback but does not enumerate these numbers. Operational runbook requires verbatim quotes.
- **Risk level**: Low

### Change #8 — Add Frontend-Team Capacity Confirmation as M1 Precondition (INV-001)

- **Title**: Add explicit frontend-team capacity confirmation as a M1 precondition
- **Source variant**: NONE — required by R2.5 invariant probe INV-001 (HIGH UNADDRESSED)
- **Target location**: V1 base §M1 Dependencies (line 68) AND V1 §Open Questions
- **Integration approach**: APPEND (new deliverable D1.7 + new OQ)
- **Rationale**: Both variants assume frontend team is available; neither names a contact or commits headcount. INV-001 promotes diff-analysis A-003 (UNSTATED) to a required precondition. Concrete addition: "D1.7 — frontend-team representative committed to M3 workstream with named POC and capacity allocation by M1 exit."
- **Risk level**: Low (organizational confirmation, not technical work)

### Change #9 — Book SOC2 Compliance Reviewer for M4 Sign-off (INV-002)

- **Title**: Name SOC2 compliance reviewer and book M4 sign-off calendar hold
- **Source variant**: NONE — required by INV-002 (HIGH UNADDRESSED)
- **Target location**: V1 base §M4 Deliverables D4.5
- **Integration approach**: MODIFY (D4.5 description gains: "Compliance reviewer named in M1 D1.5 ADR; sign-off calendar hold confirmed by M3 exit")
- **Rationale**: V1 line 146 requires SOC2 control-mapping sign-off but does not name the reviewer. With Q3 2026 audit prep absorbing compliance time, this reviewer must be booked in advance.
- **Risk level**: Low (organizational)

### Change #10 — Add Per-Email Backstop Counter to Lockout (INV-004)

- **Title**: Add per-email backstop counter to account lockout (in addition to email+IP composite)
- **Source variant**: NONE — required by INV-004 (HIGH UNADDRESSED); corrects a V1 strength
- **Target location**: V1 base §M4 Deliverables D4.4
- **Integration approach**: MODIFY (D4.4 acquires dual-key: email+IP composite for distributed-DoS mitigation AND per-email aggregate for IP-rotation attack mitigation; aggregate threshold higher, e.g., 50 attempts/15min/email)
- **Rationale**: V1's email+IP composite (line 153) was identified as a strength but R2.5 fault-finder showed it violates FR-AUTH-001 AC4 against IP-rotating attackers. The fix: dual-counter design (composite for DoS prevention + aggregate for spec compliance).
- **Risk level**: Medium (changes core lockout semantics; requires explicit test in D2.6 / D4.4 acceptance criteria)

### Change #11 — Promote Atomic Refresh-Token Rotation to Deliverable Test (INV-005)

- **Title**: Promote atomic Redis rotation from risk note to D3.2 acceptance test
- **Source variant**: NONE — required by INV-005 (HIGH UNADDRESSED)
- **Target location**: V1 base §M3 D3.2 Exit Criteria
- **Integration approach**: APPEND to D3.2 Exit Criteria: "Atomic rotation verified by integration test simulating concurrent refresh requests; LUA script or MULTI/EXEC transaction confirmed by code review."
- **Rationale**: V1 line 121 flagged atomic rotation as a risk note but did not gate it via test. Without a test, a non-atomic implementation passes M3 gate undetected and creates a replay window in production.
- **Risk level**: Medium (adds test obligation; implementation requires LUA or pipelining)

### Change #12 — Resequence M5: Pen-Test Moves to End-M4 / Start-M5 (INV-007)

- **Title**: Move pen-test (D5.1) from M5-internal to end-M4 / start-M5 boundary
- **Source variant**: NONE — required by INV-007 (HIGH UNADDRESSED)
- **Target location**: V1 base §M4 and §M5 milestone scopes
- **Integration approach**: RESTRUCTURE — D5.1 (external pen-test) becomes the M4 exit gate AND the M5 entry artifact. M5 11-day window now contains D5.2 remediation (7 days) + D5.3-D5.5 runbooks/dashboards (parallel, 5 days) + D5.6 rollout (4 days) + D5.7 readiness review (1 day). Total 11 days, no buffer compression. Critical pen-test findings have 7 days remediation (was 2 days in V1).
- **Rationale**: INV-007 showed V1's M5 arithmetic was infeasible with 2-day buffer. This restructure makes pen-test the M4→M5 boundary gate, freeing M5 for remediation and rollout. Also resolves V1's self-contradiction between "2-day buffer" and "2-week remediation window" (V1 lines 183, 214).
- **Risk level**: Medium (changes milestone boundary semantics; M4 exit gate becomes more demanding)

### Change #13 — Reconcile pg-pool Sizing with PostgreSQL Max Connections (INV-011)

- **Title**: Add PgBouncer (or read replica) as M1 deliverable; reconcile pg-pool numbers
- **Source variant**: NONE — required by INV-011 (HIGH UNADDRESSED)
- **Target location**: V1 base §M1 D1.1 + new D1.8
- **Integration approach**: MODIFY D1.1 (pool sized to source spec line 1212's "200 max" with HPA awareness) + ADD D1.8 (PgBouncer connection pooler deployed alongside PostgreSQL to absorb horizontal-scaling client multiplication)
- **Rationale**: V1 line 49 sized pg-pool for 500 concurrent — source spec line 1212 caps PG at 200 (scale to 200 only when wait > 50ms). Horizontal scaling (V1 bcrypt contingency) multiplies clients per pod against this cap. PgBouncer or read replica is required infrastructure, not optional.
- **Risk level**: Medium (adds infrastructure dependency; affects M1 scope)

### Change #14 — Reconcile Rollback with revokeAll Semantics (INV-013)

- **Title**: Make rollback forward-only after revokeAll events; remove "honor refresh tokens" rollback clause
- **Source variant**: NONE — required by INV-013 (HIGH UNADDRESSED)
- **Target location**: V1 base §M5 Architectural Risks (lines 184) + §Rollback Procedure
- **Integration approach**: MODIFY — replace V1's "rollback honors refresh tokens issued during stages" with: "Rollback after a revokeAll event (password reset, security incident) is forward-only; affected users re-login on the legacy or new service. Pre-revokeAll tokens are flushed in both services upon rollback to prevent stale-token validation drift."
- **Rationale**: V1's "honor refresh tokens" contract directly contradicted V1's `TokenManager.revokeAll()` semantics in password reset. Cannot both honor and revoke. Forward-only rollback is the cleaner contract.
- **Risk level**: Medium (changes rollback contract; requires legacy-service coordination)

---

## Changes NOT Being Made

| # | V2 Approach Considered                                              | Why V1 Approach Preserved                                                                                          |
|---|----------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------|
| 1 | V2's M1 = Core AuthService (ships login/register endpoints)         | V1's M1 = Foundations (no feature code; ADRs + infra). Debate confirmed V1's M1 is SHORTER calendar-wise (~2.5 wks vs V2's 4 wks); V2 advocate withdrew the "25% wasted" critique. V1's M1 design also gives frontend a 5-week parallel runway. |
| 2 | V2's frontend ships in single M4 sprint                              | V1's frontend ramps from mid-M2 (against frozen OpenAPI) through M3. V2 advocate explicitly conceded: "V1 wins this exchange. Merge should adopt V1's sequencing." |
| 3 | V2 has no external pen-test deliverable                              | V1's D5.1 pen-test is non-negotiable per PRD §Risk Analysis row 2 ("Dedicated security review; penetration testing before production"). V2 advocate full concession on C-007. |
| 4 | V2 has no ADRs                                                       | V1's M1 D1.5 ADRs are required for SOC2 decision provenance. V2 advocate partial concession; merged plan keeps all 4 ADRs (token storage, bcrypt vs argon2, refresh-storage hashing, MFA/OAuth seams). |
| 5 | V2's 3-phase rollout (Alpha → 10% Beta → 100%)                       | V1's 4-stage rollout (1% → 10% → 50% → 100%, 24h per stage) gives finer-grained anomaly detection at production scale. INV-007 restructure preserves 4-stage rollout with realistic remediation window. |

---

## Risk Summary

| Change | Risk Level | Impact if Wrong                                                                              | Rollback Plan                                                                |
|--------|------------|----------------------------------------------------------------------------------------------|------------------------------------------------------------------------------|
| 1-7    | Low        | Cosmetic / format only; no semantic change                                                   | Revert to V1 prose if table proves harder to maintain                        |
| 8      | Low        | Frontend team unavailable → M3 slips                                                          | Re-source from contractor pool or compress D3.4-D3.5 (Playwright pre-built)  |
| 9      | Low        | Compliance reviewer unavailable → M4 SOC2 gate slips                                          | Escalate to compliance VP; back-pressure on Q3 audit prep                    |
| 10     | Medium     | Dual-counter implementation bug locks legitimate users                                        | Per-email aggregate threshold tunable via config; revert to single composite if false positive rate > 1% |
| 11     | Medium     | Atomic rotation test infrastructure complex                                                   | Use simpler `WATCH/MULTI/EXEC` if LUA proves debug-hostile; document and gate |
| 12     | Medium     | Pen-test slip past M4 exit blocks M5 entry                                                    | Build M4 exit buffer (2-3 days); if slip, GA shifts right not gates compressed |
| 13     | Medium     | PgBouncer learning curve / config errors                                                      | Fallback to per-pod connection limits; use proxy-mode rather than session-mode |
| 14     | Medium     | Legacy-service token-flush coordination requires legacy code change                           | Document forward-only rollback contract in runbook; manual support flow for affected users |

**Overall risk envelope**: Low-to-Medium. No HIGH-risk changes. All Medium-risk changes have documented rollback plans.

---

## Review Status

**Auto-approved** — `--interactive` flag not provided. All changes proceed to merge execution per protocol default.

If reviewer wishes to inspect: every change cites a specific source (V1 line numbers, V2 line numbers, or INV-NNN finding ID). The 7 R2.5 HIGH-severity items are documented as mandatory additions, not optional.
