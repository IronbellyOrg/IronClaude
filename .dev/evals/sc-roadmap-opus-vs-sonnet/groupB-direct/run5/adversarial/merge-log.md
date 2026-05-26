# Merge Log

## Metadata

- Base: Variant 1 (opus) — `variant-1-opus-default.md` (790 lines, 19 H2 sections)
- Non-base contributor: Variant 2 (sonnet) — `variant-2-sonnet-default.md`
- Executor: merge-executor agent (Step 5 of sc:adversarial protocol)
- Refactor plan: `refactor-plan.md` (26 changes: 9 invariant fixes + 12 V2 incorporations + 5 base-weakness fixes)
- Output: `/config/workspace/IronClaude/.dev/eval-roadmap/groupB-direct/run5/merged-roadmap-user-auth.md` (1034 lines, 19 H2 sections + 3 sub-numbered appendices)
- Changes applied: 26 planned / 26 applied / 0 failed / 0 skipped
- Merge timestamp: 2026-05-22T15:42:00Z
- Status: success

---

## Changes Applied

### Phase A — HIGH-Severity Invariant Fixes

### Change Fix #9: INV-026 bcrypt cost-12 vs NFR-PERF-001

- Status: applied
- Target: M1 D-103, M1 exit criteria, R-104, new R-117, §8 boundary conditions
- Before: D-103 description hard-committed to "cost factor 12" with 250-500ms band benchmark; R-104 mitigation said "drop to cost 11 if budget exceeded"
- After: D-103 description now says "cost factor selected by M1 Week 1 benchmark on target hardware. Default cost-11; cost-12 only if full-path benchmark ≤200ms p95"; M1 exit criterion replaced with full-path latency budget; R-104 updated to "Ship at cost 11 unless benchmark demonstrates cost-12"; new R-117 added covering total login-path latency; §8 has new "Login-path latency budget breakdown" row
- Provenance tag: `<!-- Source: Base (original, modified) — Fix #9 (bcrypt) ... -->`
- Validation: pass — all five touchpoints (D-103, M1 exit, R-104, R-117, §8) modified consistently

### Change Fix #8: INV-023 Defense-in-depth brute-force stack

- Status: applied
- Target: M1 scope, M1 deliverables (new D-109), R-102, M1 exit criteria
- Before: M1 scope had no defense-in-depth stack; R-102 mitigation listed lockout + gateway rate limit only
- After: M1 scope now has a 4-layer defense-in-depth paragraph; D-109 added (per-account global rate limit 20/email-hash/hour); R-102 mitigation enumerates all 4 layers; M1 exit criterion added for D-109 enforcement
- Provenance tag: `<!-- Source: Base (original, modified) — Fix #8 ... -->`
- Validation: pass — 4-layer stack documented; D-109 has deliverable row; R-102 updated

### Change Fix #2: INV-005 Audit log NULL user_id

- Status: applied
- Target: M1 scope (audit_log description), D-102, M1 exit criteria, CC2 OBS-1
- Before: D-102 description did not specify nullable user_id
- After: M1 scope explicitly states `user_id UUID NULL`; D-102 description includes nullability; M1 exit criterion added for NULL user_id audit INSERT; OBS-1 has explicit verification item
- Provenance tag: `<!-- Source: Base (original, modified) — Fix #2 (NULL user_id) ... -->`
- Validation: pass — schema, deliverable, exit criterion, and OBS workstream item all updated consistently

### Change Fix #3: INV-006 Enumeration timing + audit-write interaction

- Status: applied
- Target: §9.5 login transaction scope, CC3 QA-6, §8 boundary conditions
- Before: QA-6 test described variance bounds but did not specify "with audit writes enabled"; no boundary row for audit-write timing
- After: §9.5 login transaction scope includes both unknown-email and wrong-password paths with identical-shape audit writes and dummy bcrypt on unknown-email path; QA-6 description updated to "Test executes with audit writes ENABLED"; new §8 boundary row "Login-failure audit-write timing"
- Provenance tag: `<!-- Source: Base (original, modified) — Fix #3 (QA-6 audit-write timing) ... -->`
- Validation: pass — three touchpoints aligned; dummy-bcrypt requirement propagates to M1 exit criteria and §8 latency budget

### Change Fix #7: INV-022 SOC2 audit-log immutability

- Status: applied
- Target: M1 scope, M1 deliverables (new D-110), CC1 SEC-3, M5 exit criteria
- Before: SEC-3 covered retention only; no immutability controls
- After: M1 scope has "Audit-log immutability controls" subsection; D-110 added; SEC-3 expanded with (a) DB trigger, (b) audit_writer role, (c) quarterly integrity verification; M5 exit criterion added; §9.4 notes immutability mechanism
- Provenance tag: `<!-- Source: Base (original, modified) — Fix #7 (audit immutability) ... -->`
- Validation: pass — control surface explicit; SOC2 CC6.1+CC7.2 controls mapped to D-110

### Change Fix #1: INV-001 Refresh-token family lineage durability

- Status: applied
- Target: M2 D-202, M2 exit criteria, §9.1, R-105
- Before: §9.1 mentioned "token family" concept but no storage schema; D-202 description did not specify family-linkage storage; R-105 had no AOF requirement
- After: M2 scope has explicit family-lineage storage paragraph (Redis Hash + Sorted Set + AOF `appendfsync everysec`); D-202 description updated; M2 exit criterion added for AOF-reload integration test; §9.1 has dedicated "Family-linkage storage" subsection; R-105 mitigation notes AOF persistence
- Provenance tag: `<!-- Source: Base (original, modified) — Fix #1 (family lineage) ... -->`
- Validation: pass — durability mechanism specified end-to-end with concrete schema and integration test

### Change Fix #4: INV-013 Token eviction vs family-revocation race

- Status: applied
- Target: §9.1 state machine, M2 D-202, M2 exit criteria
- Before: §9.1 had no `evicted` state
- After: §9.1 adds `evicted` state with guard "evicted tokens with `evicted=true` do NOT trigger family revocation"; M2 scope includes paired eviction + guard logic; D-202 description includes eviction-family-guard logic; M2 exit criterion added for 11-device integration test
- Provenance tag: `<!-- Source: Base (original, modified) — Fix #4 (eviction guard) ... -->`
- Validation: pass — guard logic consistent with Change #6 (10-token cap)

### Change Fix #5: INV-017 Login-path transaction ordering

- Status: applied
- Target: §9.5 (new transaction scope), M1 scope, M2 exit criteria
- Before: §9.5 had only `register()` and `confirmPasswordReset()` scopes; no login scope
- After: §9.5 has full `AuthService.login()` transaction scope with ordering: bcrypt → BEGIN TX (read, UPDATE lastLoginAt, INSERT audit_log) → COMMIT → Redis SET (outside TX) → return; rollback semantics documented; M1 scope cross-references §9.5; M2 exit criterion added for Redis-failure-during-login test
- Provenance tag: `<!-- Source: Base (original, modified) — Fix #5 (login transaction) ... -->`
- Validation: pass — transaction boundary explicit; degenerate retry case (double audit row) documented as acceptable

### Change Fix #6: INV-021 In-process SendGrid retry vs 200ms p95

- Status: applied
- Target: M3 scope, D-303, new D-310, M3 exit criteria, §11.1 OQ-1, §12.3 failure-mode catalog
- Before: M3 used "Asynchronous email send via a queue"; D-303 was "SendGrid client wrapper with retry + bounce-handling hook"; OQ-1 resolution was "async via queue"
- After: M3 scope describes single-attempt 5-sec timeout + `pending_emails` dead-letter table + cron retry sweep; D-303 description updated; new D-310 added (pending_emails table + cron); M3 exit criterion added "returns 200 in <200ms p95 even when SendGrid unavailable"; OQ-1 resolution updated; §12.3 SendGrid-down row updated; OBS-8 monitoring added
- Provenance tag: `<!-- Source: Base (original, modified) — Fix #6 (SendGrid retry) ... -->`
- Validation: pass — first-attempt timeout ceiling (5s) reconciled with handler latency target; cron sweep + alert at >100 rows specified

### Phase B — V2 Strength Incorporations

### Change #1: Move Account Lockout from M3 to M1

- Status: applied
- Target: M1 scope/deliverables/entry/exit criteria, M3 (D-305 removed), §6.1 external dependencies, §6.2 ASCII diagram, §6.4 blocking-dependency summary
- Before: V1 had D-305 LoginAttemptTracker in M3; M1 had no lockout deliverable; Redis was M2 entry dependency
- After: D-108 LoginAttemptTracker now in M1; M1 entry criteria require Redis 7+; M1 exit adds "Account locks after 5 failed logins within 15 minutes"; M3 D-305 removed (note inserted); §6.1 Redis row updated to "M1 entry (moved from M2 per Change #1)"; §6.2 diagram now shows Redis at Week 1
- Provenance tag: `<!-- Source: V2 (sonnet), Section 3.1 D-006 — merged per Change #1 -->`
- Validation: pass — Redis moved to Week 1, lockout integrated with defense-in-depth Layer 1, all six required modifications executed

### Change #6: 10-Token FIFO Refresh Cap

- Status: applied
- Target: M2 scope, M2 deliverables (new D-209), §11.1 OQ-2, §9.1, §8 boundary conditions
- Before: OQ-2 resolution was "No cap in v1.0"; §9.1 had no `evicted` state; §8 had "User logs in from 6th device while 5 sessions active"
- After: OQ-2 resolution updated to "10 active refresh tokens; oldest evicted FIFO"; M2 scope includes per-user 10-token FIFO cap with eviction-guard paragraph; D-209 added; §9.1 includes `evicted` state and guard; §8 row updated to "User logs in from 11th device while 10 sessions active"; coordinated with Fix #4
- Provenance tag: `<!-- Source: V2 (sonnet), OQ-B — merged per Change #6, paired with Fix #4 -->`
- Validation: pass — cap + guard work together; eviction does not cause false-positive family revoke

### Change #2: Greenfield-Correct Rollback Procedure

- Status: applied
- Target: §12.2 step 2, §11.3 Assumptions (new A-11)
- Before: §12.2 step 2 said "traffic routes back to legacy auth"
- After: §12.2 step 2 replaced with "display a maintenance page (503) at the gateway for all `/auth/*` routes"; A-11 added stating greenfield assumption; §10 Out of Scope footnote updated to reflect greenfield context
- Provenance tag: `<!-- Source: V2 (sonnet), Section 12.1 — merged per Change #2 -->`
- Validation: pass — replaces an infeasible rollback step with a feasible one; PRD greenfield context now explicit

### Change #3: 10-Row Staffing Table

- Status: applied
- Target: §14 Cost & Resource Plan (new §14.1)
- Before: §14 had single row "2 backend + 1 frontend FTE + 0.5 SRE + 0.25 security review"
- After: §14.1 Staffing Plan added with 10 rows (Backend 1/2/3, Frontend 1/2, QA, Security, DevOps, PM, SRE) adapted to V1's 11-week cadence
- Provenance tag: `<!-- Source: V2 (sonnet), Section 10.1 "Team Composition" — merged per Change #3 -->`
- Validation: pass — staffing now actionable for org/HR requests; weeks align with V1 milestone windows

### Change #4: Post-GA Planning Section

- Status: applied
- Target: New §18.5 after §18.2 (Appendix D), before §19 Closing Note
- Before: V1 had no post-GA planning section
- After: §18.5 Post-GA Considerations added with three subsections (v1.1 Planning Q3 2026 target, v2.0 Planning Q4 2026 target, Ongoing Maintenance); GDPR right-to-erasure promoted to named v1.1 item per INV-025
- Provenance tag: `<!-- Source: V2 (sonnet), Section 13 — merged per Change #4 -->`
- Validation: pass — quarters labeled as "target"; ongoing maintenance items cross-reference Fix #7 SOC2 verification

### Change #5: Admin Audit Log Query Deliverable

- Status: applied
- Target: M3 deliverables (new D-309), M3 exit criteria, §13 Personas Coverage Check
- Before: No admin query deliverable; Jordan persona row referenced only "M1 (audit-log schema), M3 (lockout events), CC2 (dashboards)"
- After: D-309 `GET /admin/audit-logs?from=&to=&user_id=&event_type=` added with pagination; M3 exit criterion added; Jordan row updated to "M1 (D-102), M3 (D-306, **D-309**), CC2"; §18.2 Appendix D includes `/v1/admin/audit-logs` row; §17 Appendix A updated
- Provenance tag: `<!-- Source: V2 (sonnet), D-030 — merged per Change #5 -->`
- Validation: pass — Jordan persona now has explicit deliverable serving the user story

### Change #7: Pentest Cost Quantification

- Status: applied
- Target: §14 Cost & Resource Plan table
- Before: V1 listed SEC-5 pentest but no cost
- After: Cost table includes "External penetration test (one-time) | $5,000-$15,000 | N/A — budgeted per engagement"
- Provenance tag: `<!-- Source: V2 (sonnet), Section 10.3 — merged per Change #7 -->`
- Validation: pass — single row added, SEC-5 cross-reference updated

### Change #8: Feature Flag Lifecycle Table

- Status: applied
- Target: New §18.1 Appendix C
- Before: V1 §10 mentioned "removal targets recorded" but no dates
- After: §18.1 Appendix C added with `AUTH_NEW_LOGIN` (Created W8, Enabled W9, Removed W13) and `AUTH_TOKEN_REFRESH` (Created W8, Enabled W10, Removed W15)
- Provenance tag: `<!-- Source: V2 (sonnet), Appendix B "Feature Flag Lifecycle" — merged per Change #8 -->`
- Validation: pass — concrete removal dates now exist for both flags; CC5 INF-6 referenced

### Change #9: Beta 1-Week Hidden Buffer

- Status: applied
- Target: M5 Risk Notes, §11.2 (new OQ-R7)
- Before: V1 had no hidden buffer; INV-010 arithmetic unaddressed
- After: M5 Risk Notes paragraph added describing 1-week hidden buffer + arithmetic constraint cross-referencing INV-010; OQ-R7 added to §11.2 (PM decision: compress or slip to 2026-06-16)
- Provenance tag: `<!-- Source: V2 (sonnet), Section 3.5 M5 Risk Notes — merged per Change #9 -->`
- Validation: pass — INV-010 now operationalized as a tracked decision; GA-date subject to OQ-R7

### Change #10: Three-Phase Decomposition Rationale

- Status: applied
- Target: §2.1 Decomposition rationale (4th constraint paragraph)
- Before: §2.1 had three numbered constraints
- After: §2.1 has four numbered constraints; new paragraph explains three-phase operational clustering and why M3 separates from M4
- Provenance tag: `<!-- Source: V2 (sonnet), Section 2.2 "Why Three Phases, Not Two" — merged per Change #10 -->`
- Validation: pass — paragraph integrated without altering numbering of subsequent constraints

### Change #11: API Endpoint Summary Appendix

- Status: applied
- Target: New §18.2 Appendix D
- Before: V1 had no consolidated endpoint summary
- After: §18.2 Appendix D added with 8 rows (register, login, refresh, me, reset-request, reset-confirm, admin audit-logs, conditional logout pending OQ-R4); `/v1/*` prefix noted per TDD §8.4
- Provenance tag: `<!-- Source: V2 (sonnet), Appendix C — merged per Change #11 -->`
- Validation: pass — Sam persona served; rate-limit columns reflect defense-in-depth layers

### Change #12: Infrastructure Workstream Split

- Status: applied
- Target: New §4 CC5 workstream; CC2 OBS-6/OBS-7 cross-references
- Before: V1 had CC1-CC4 only; infra embedded in CC2 OBS-6/OBS-7 and M5 deliverables
- After: CC5 Infrastructure & Platform workstream added with INF-1 through INF-7; CC2 OBS-6/OBS-7 now have "(Provisioning tracked in CC5 INF-N)" cross-references; §6.2 ASCII diagram extended with CC5 row
- Provenance tag: `<!-- Source: V2 (sonnet), Section 4.5 — merged per Change #12 -->`
- Validation: pass — infrastructure tracked explicitly; Redis-Week-1 dependency (from Change #1) visible in CC5 INF-2

### Phase C — Base Weakness Fixes (subsumed by Phase A/B changes)

### Change #B1: Lockout deferred to M3 (subsumed)

- Status: applied (subsumed)
- Subsumed by: Change #1 (lockout-in-M1) + Fix #8 (defense-in-depth)
- No separate edit required

### Change #B2: Rollback assumes legacy auth (subsumed)

- Status: applied (subsumed)
- Subsumed by: Change #2 (greenfield rollback)
- No separate edit required

### Change #B3: Single-row staffing (subsumed)

- Status: applied (subsumed)
- Subsumed by: Change #3 (10-row staffing table)
- No separate edit required

### Change #B4: No admin audit query (subsumed)

- Status: applied (subsumed)
- Subsumed by: Change #5 (D-309 admin audit query)
- No separate edit required

### Change #B5: Audit retention conflict text (subsumed + reinforced)

- Status: applied (subsumed)
- Subsumed by: V1's existing OQ-R1 mechanism (retained) + Fix #7 (SOC2 immutability strengthens audit story)
- D-102 description updated to: "retention parameterized, default 90d per TDD, set to 12 months pending OQ-R1"
- No separate structural edit required

---

## Post-Merge Validation Results

### Structural Integrity

- Status: PASS
- Heading-level gaps: none (all H2 → H3 transitions are clean; sub-numbered appendices §18.1, §18.2, §18.5 use H2 consistently with §18 as the calendar appendix)
- Orphaned subsections: none
- Heading audit: 1 H1 + 19 numbered H2 (sections 1-19) + 3 sub-numbered H2 appendices (18.1, 18.2, 18.5) + 36 H3 (subsections, milestones, cross-cutting tracks, Appendix D body)
- M1-M5 progression intact and dependency-ordered
- CC1-CC5 workstreams parallel-tracked from Week 1
- Section ordering preserved: Vision → Phasing → Milestones → Workstreams → Risks → Dependencies → Metrics → Boundaries → State → OOS → Open Q → Rollback → Personas → Cost → Comms → Glossary → Traceability → Calendar → Flag Lifecycle → API Summary → Post-GA → Closing

### Internal References

- Total unique IDs scanned: 160
- Internal IDs (defined in merged doc): 125 — RESOLVED
- External / cross-document IDs: 35 — these reference source artifacts (PRD, TDD, invariant-probe.md) and are correctly NOT internally defined
  - TDD risk IDs: R-001, R-002, R-003 (referenced inside R-101/R-102/R-103 "TDD R-NNN" labels — external)
  - TDD open question: OQ-002 (TDD OQ-002 max roles array length — external)
  - Invariant probe IDs: INV-001, 002, 003, 005, 006, 007, 008, 010, 013, 015, 017, 019, 020, 021, 022, 023, 024, 025, 026 (refs to sibling artifact `invariant-probe.md` — external by design)
  - PRD/TDD FR IDs: FR-AUTH.1–.5 and FR-AUTH-001–005 (external)
  - V2 source deliverable: D-030 (referenced in provenance comment only — pointer to source variant, not an internal definition)
  - Removed-deliverable note: D-305 (intentionally referenced as removed; M3 deliverable table includes a note explaining the removal)
  - OQ-R7: defined in §11.2 (verified present at line 758)
- Broken internal references: 0
- Broken external references: 0 (all external IDs are correctly external)

### Contradiction Rescan

- New contradictions introduced: 0
- Audited cross-cuts:
  - Lockout-in-M1 (Change #1) is consistent with M1 entry-criteria Redis requirement; consistent with §6.1 dependency table; consistent with §6.2 ASCII diagram; consistent with Fix #8 defense-in-depth Layer 1.
  - 10-token FIFO cap (Change #6) is consistent with Fix #4 evicted-guard; both modify §9.1 in compatible ways; §8 boundary row updated coherently.
  - bcrypt cost decision (Fix #9) — D-103 default cost-11 is consistent with R-104 mitigation; R-117 contingency does not contradict R-104; §8 latency budget row sums to ≤200ms at cost-11.
  - SendGrid single-attempt + dead-letter (Fix #6) — M3 scope, D-303, D-310, OQ-1 resolution, §12.3 failure-mode row all describe the same mechanism; no contradiction between "always 200" anti-enumeration response and 5-second timeout.
  - Greenfield rollback (Change #2) — §12.2 step 2 (gateway 503) is consistent with A-11 (no legacy auth); §10 Out of Scope footnote on legacy endpoints is consistent.
  - Audit immutability (Fix #7) — D-110, SEC-3 expansion, §9.4 note, M5 exit criterion all describe the same trigger + role + integrity-script mechanism.
  - Three-phase rationale (Change #10) added as an additive 4th constraint in §2.1 without contradicting the existing five-milestone decomposition.
- Verdict: zero new contradictions introduced by the merge.

---

## Summary

- Planned: 26
- Applied: 26 (21 distinct edit operations + 5 subsumed)
- Failed: 0
- Skipped: 0
- HIGH-severity invariant fixes addressed: 9 / 9 (INV-001, 005, 006, 013, 017, 021, 022, 023, 026)
- V2 strength incorporations applied: 12 / 12 (Changes #1-#12)
- Base-weakness fixes resolved: 5 / 5 (subsumed by Phase A/B changes)
- Residual MEDIUM UNADDRESSED invariants (per plan §7): 10 (INV-002, 003, 007, 008, 010, 015, 019, 020, 024, 025) — INV-008 partially mitigated by Fix #3 dummy bcrypt; INV-010 operationalized as OQ-R7; INV-025 operationalized by Change #4 GDPR-RtE promotion.
- Merged output: 1034 lines (within plan target ~900-1300)
- Provenance annotations: every H2/H3 section carries an HTML-comment provenance tag (Base / V2 / Invariant Fix / combinations)
- Overall status: **success**
