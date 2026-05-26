# Merge Log — V1 (opus:architect) + V2 (sonnet:analyzer) + R2.5 Invariant Probe

## Metadata

| Field                       | Value                                                                     |
|-----------------------------|---------------------------------------------------------------------------|
| Base variant                | Variant 1 (opus:architect)                                                |
| Incorporated variant        | Variant 2 (sonnet:analyzer) — format/traceability tables only             |
| R2.5 additions              | INV-001, INV-002, INV-004, INV-005, INV-007, INV-011, INV-013             |
| Executor                    | merge-executor (per /sc:adversarial Step 5)                               |
| Plan source                 | /config/workspace/IronClaude/.dev/eval-roadmap/groupB-direct/run1/adversarial/refactor-plan.md |
| Output artifact             | /config/workspace/IronClaude/.dev/eval-roadmap/groupB-direct/run1/merged-output.md |
| Changes planned             | 14                                                                        |
| Changes applied             | 14                                                                        |
| Changes skipped             | 0                                                                         |
| Changes failed              | 0                                                                         |
| Provenance tags inserted    | 45 (5 header + 40 per-section)                                            |
| Merged document word count  | 8083                                                                      |
| Status                      | COMPLETE — all 14 planned changes applied; post-merge validation green     |
| Merge timestamp             | 2026-05-22T17:10:00+00:00                                                 |

---

## Per-Change Application Log

### Change #1 — Insert Success Metrics Table — APPLIED

- **Status**: APPLIED
- **Source**: V2 §Success Metrics (lines 21-34)
- **Target location**: After Executive Summary, before V1's Strategic Objectives
- **Before**: V1 had Executive Summary → Strategic Objectives (6 prose objectives).
- **After**: Executive Summary → Success Metrics table (12 metrics × 5 columns) → "Why These Metrics — Strategic Objectives" subsection retaining all 6 V1 objectives verbatim as table rationale.
- **Provenance tag**: `<!-- Source: Variant 2 (sonnet:analyzer), §Success Metrics — merged per Change #1 -->` and `<!-- Source: Base (V1 opus:architect, modified) — repositioned under Success Metrics table as rationale per Change #1 -->`
- **Validation**: Table renders with 12 rows; 6 V1 objectives preserved verbatim beneath table.

### Change #2 — Insert Sprint-Level Breakdown Table — APPLIED

- **Status**: APPLIED
- **Source**: V2 §Sprint-Level Breakdown (lines 180-188)
- **Target location**: After M1-M5 milestone detail sections, before Workstreams
- **Before**: V1 jumped directly from M5 to Workstreams with no sprint-level calendar.
- **After**: New `## Sprint-Level Breakdown` section with S1-S6 × Window × Milestones × Owner Workstreams × Primary Deliverables table. Owner column reconciled with V1's 5-workstream model (sprints carry multiple workstreams). Sprint windows shifted from V2's original calendar to fit V1's M1-M5 dates (e.g., S4 absorbs M3 work; S5 absorbs M4 + D5.1 pen-test boundary).
- **Provenance tag**: `<!-- Source: Variant 2 (sonnet:analyzer), §Sprint-Level Breakdown — merged per Change #2; owner cells reconciled with V1's 5-workstream model -->`
- **Validation**: 6 sprint rows present; reconciliation note included.

### Change #3 — Replace Acceptance & Release Gates with Performance & Reliability Gates Table — APPLIED

- **Status**: APPLIED
- **Source**: V2 §Performance & Reliability Gates (lines 225-235)
- **Target location**: Replaces V1's prose §Acceptance & Release Gates
- **Before**: V1 had prose-list of per-milestone gates + a 7-item GA criteria list.
- **After**: Tabular gate format (Gate / Threshold / Phase Boundary / Source) extended to include every V1 milestone gate AND all R2.5 additions (atomic rotation per Change #11, dual-key lockout per Change #10, named SOC2 reviewer per Change #9, frontend-team commitment per Change #8, pen-test at M4→M5 boundary per Change #12). V1's final 7-item GA criteria preserved as a single "Final GA criteria (cluster row for M5 exit)" row. TDD §19.4 verbatim threshold quote appended (per Change #7 cross-reference).
- **Provenance tag**: `<!-- Source: Variant 2 (sonnet:analyzer), §Performance & Reliability Gates — merged per Change #3; V1's final GA criteria preserved as M5-exit row -->`
- **Validation**: Table has 30+ gate rows; V1 GA criteria all 7 enumerated in cluster row; TDD §19.4 quote present verbatim.

### Change #4 — Insert Per-FR Validation Strategy Table — APPLIED

- **Status**: APPLIED
- **Source**: V2 §Validation Strategy (lines 193-199)
- **Target location**: After Cross-Cutting Concerns, before Risk Register
- **Before**: V1 had no per-FR validation matrix.
- **After**: New `## Validation Strategy` section with FR-AUTH-001..005 × Unit/Integration/E2E matrix, plus NFR validation gate list. Integration cells for FR-AUTH-001 augmented with dual-counter lockout (per Change #10) and FR-AUTH-003 augmented with atomic rotation (per Change #11). NFR gates relocated from M5 entry to M4 exit (k6) and M5 entry (pen-test, per Change #12) to align with restructured milestone boundaries.
- **Provenance tag**: `<!-- Source: Variant 2 (sonnet:analyzer), §Validation Strategy — merged per Change #4 -->`
- **Validation**: 5 FR rows present; 5 NFR gates listed; cross-references to Changes #10/#11/#12 included.

### Change #5 — Insert Out-of-Scope Explicit Table — APPLIED

- **Status**: APPLIED
- **Source**: V2 §Out-of-Scope (lines 264-277)
- **Target location**: After Performance & Reliability Gates, before Open Questions
- **Before**: V1 mentioned non-goals only in prose under Objective 4.
- **After**: New `## Out-of-Scope (explicit)` section with 6-row Capability × Deferred To × Rationale table. Account-lockout row updated to reference current dual-key design per Change #10.
- **Provenance tag**: `<!-- Source: Variant 2 (sonnet:analyzer), §Out-of-Scope — merged per Change #5 -->`
- **Validation**: 6 rows present; NG-001/NG-002/NG-003 + OQ-001/OQ-3/OQ-4 all mapped.

### Change #6 — Augment Open Questions with Owner + Target Resolution Date Columns — APPLIED

- **Status**: APPLIED
- **Source**: V2 §Open Questions (lines 282-288) — table format
- **Target location**: V1 base §Open Questions
- **Before**: V1 had 8 numbered narrative OQs with "Recommended position" prose.
- **After**: V2 table format applied (ID / Question / Owner / Target Resolution / Source). All 8 V1 OQs preserved + new OQ-9 added per Change #8 (frontend-team capacity). V1's "Recommended position" prose preserved beneath table as numbered list (OQ-1 through OQ-9).
- **Provenance tag**: `<!-- Source: Base (V1 opus:architect, modified) — V2's Owner + Target Resolution Date columns added per Change #6; V1's 8 OQs and recommended positions preserved; new INV-001 OQ appended per Change #8 -->`
- **Validation**: 9 OQ rows in table; 9 recommended-position items below; OQ-9 cross-references Change #8.

### Change #7 — Quote TDD §19.4 Rollback Triggers Verbatim — APPLIED

- **Status**: APPLIED
- **Source**: V2 §Performance & Reliability Gates closing paragraph (line 237)
- **Target location**: M5 Architectural Risks section + Performance & Reliability Gates closing paragraph
- **Before**: V1 mentioned rollback but did not enumerate TDD §19.4 thresholds.
- **After**: M5 risks now contains: **"p95 > 1000ms for > 5 min; error rate > 5% for > 2 min; Redis connection failures > 10/min"** (TDD §19.4) verbatim. The Performance & Reliability Gates section closing paragraph repeats the verbatim quote.
- **Provenance tag**: `<!-- Source: Variant 2 (sonnet:analyzer), §Performance & Reliability Gates closing paragraph — merged per Change #7 -->`
- **Validation**: Verbatim quote present in 2 locations; TDD §19.4 attribution included.

### Change #8 — Add Frontend-Team Capacity Confirmation as M1 Precondition (INV-001) — APPLIED

- **Status**: APPLIED
- **Source**: R2.5 invariant probe INV-001 (HIGH UNADDRESSED)
- **Target location**: M1 §Deliverables (new D1.7); Workstreams §Frontend Integration; Open Questions (new OQ-9); Dependency Graph
- **Before**: Both V1 and V2 assumed frontend team availability without commitment.
- **After**: New D1.7 deliverable — "Frontend-team representative committed to M3 workstream with named POC and capacity allocation by M1 exit; ≥1.0 FTE for D3.4/D3.5/D3.6 across mid-M2 through M3." Workstreams §Frontend Integration cross-references D1.7. Open Questions adds OQ-9. Dependency graph adds D1.7 sequencing constraint. M1 Exit Criteria adds "Frontend-team POC named and committed in writing."
- **Provenance tag**: `<!-- Source: R2.5 invariant probe INV-001 — added per Change #8 -->` (4 locations)
- **Validation**: D1.7 present in M1; OQ-9 present in Open Questions; risk-register row added; sequencing constraint listed.

### Change #9 — Book SOC2 Compliance Reviewer for M4 Sign-off (INV-002) — APPLIED

- **Status**: APPLIED
- **Source**: R2.5 invariant probe INV-002 (HIGH UNADDRESSED)
- **Target location**: M1 D1.5 (ADR includes reviewer name); M4 D4.5 (description gains reviewer-named + sign-off-hold language)
- **Before**: V1 line 146 required SOC2 sign-off but did not name a reviewer.
- **After**: D1.5 ADR list extended to include "(e) named SOC2 compliance reviewer for M4 sign-off". D4.5 description extended with: "SOC2 control-mapping reviewer named in M1 D1.5 ADR; sign-off calendar hold confirmed by M3 exit so the reviewer's M4 slot is locked in ahead of Q3 2026 audit-prep contention." M4 Exit Criteria updated. Workstreams §Security & Compliance and Risk Register row updated.
- **Provenance tag**: `<!-- Source: R2.5 invariant probe INV-002 — modified per Change #9 -->` (2 locations)
- **Validation**: D1.5 lists reviewer-naming as ADR item (e); D4.5 contains sign-off-hold language; risk-register row updated.

### Change #10 — Add Per-Email Backstop Counter to Lockout (INV-004) — APPLIED

- **Status**: APPLIED
- **Source**: R2.5 invariant probe INV-004 (HIGH UNADDRESSED)
- **Target location**: M4 D4.4
- **Before**: V1 D4.4 specified email+IP composite lockout only.
- **After**: D4.4 redesigned as "dual-key counter design": (a) email+IP composite (5/15min) for distributed-DoS mitigation, (b) per-email aggregate (50/15min) for IP-rotation attack mitigation per FR-AUTH-001 AC4. Aggregate threshold tunable; fallback to composite-only if false-positive rate > 1%. M4 Architectural Risks updated to reference dual-key design. Risk register gains new "IP-rotating attacker bypasses email+IP composite lockout" row. Cross-cutting Concerns §Security item (6) updated. Out-of-Scope row updated to reference current dual-key design.
- **Provenance tag**: `<!-- Source: R2.5 invariant probe INV-004 — modified per Change #10 -->` (2 locations)
- **Validation**: D4.4 contains both counter thresholds; Security item (6) lists both keys; risk-register row added.

### Change #11 — Promote Atomic Refresh-Token Rotation to Deliverable Test (INV-005) — APPLIED

- **Status**: APPLIED
- **Source**: R2.5 invariant probe INV-005 (HIGH UNADDRESSED)
- **Target location**: M3 D3.2 Exit Criteria + M3 Architectural Risks
- **Before**: V1 line 121 mentioned atomic rotation as a risk note but did not gate it via test.
- **After**: M3 Exit Criteria gains bullet: "D3.2 atomic rotation verified by integration test simulating concurrent refresh requests; LUA script or MULTI/EXEC transaction confirmed by code review." M3 Architectural Risk bullet updated: "This atomicity is now gated by D3.2 integration test (per Change #11)." Validation Strategy FR-AUTH-003 row references atomic rotation. Dependency Graph adds: "D3.2 atomic-rotation integration test gates M3 exit." Risk Register gains new row. Cross-cutting Concerns §Security item (4) updated.
- **Provenance tag**: `<!-- Source: R2.5 invariant probe INV-005 — added per Change #11 -->` and `<!-- Source: R2.5 invariant probe INV-005 — modified per Change #11 -->` (2 locations)
- **Validation**: D3.2 exit criterion added; risk-register row added; FR-AUTH-003 validation row mentions atomic rotation.

### Change #12 — Resequence M5: Pen-Test Moves to End-M4 / Start-M5 (INV-007) — APPLIED

- **Status**: APPLIED
- **Source**: R2.5 invariant probe INV-007 (HIGH UNADDRESSED); also resolves V1 self-contradiction (lines 183 vs 214)
- **Target location**: M4 (scope, dependencies, exit criteria) + M5 (scope, D5.1, D5.2, architectural risks)
- **Before**: V1 placed D5.1 pen-test internal to M5 with 2-day buffer; D5.2 had 2-day remediation window. This contradicted V1 line 214 which said "pen-test scheduled with 2-week remediation window".
- **After**: D5.1 is now the M4→M5 boundary artifact (M4 exit gate AND M5 entry artifact). D5.2 remediation window expanded to 7 days. M5 11-day window: D5.2 (7d) + D5.3-D5.5 parallel (5d) + D5.6 rollout (4d) + D5.7 readiness (1d) — no buffer compression. M5 scope rewritten to remove pen-test execution. M4 exit criteria gain "pen-test report delivered." Dependency graph updated. Validation Strategy NFR gates updated to gate pen-test at M5 entry. Risk Register row updated to reflect M4→M5 boundary timing. Contradiction between V1 lines 183 and 214 resolved by the 7-day window explicitly replacing the 2-day buffer.
- **Provenance tag**: `<!-- Source: R2.5 invariant probe INV-007 — modified per Change #12 -->` (3 locations) and `<!-- Source: R2.5 invariant probe INV-007 — added per Change #12 -->` (1 location)
- **Validation**: D5.1 description includes "M4 exit gate AND M5 entry artifact"; D5.2 window says 7 days; M4 exit criteria mention pen-test; risk-register row updated.

### Change #13 — Reconcile pg-pool Sizing with PostgreSQL Max Connections (INV-011) — APPLIED

- **Status**: APPLIED
- **Source**: R2.5 invariant probe INV-011 (HIGH UNADDRESSED)
- **Target location**: M1 D1.1 (modified) + M1 D1.8 (new)
- **Before**: V1 D1.1 sized pg-pool for 500 concurrent — exceeded source spec line 1212 "200 max" cap.
- **After**: D1.1 now reads: "configure pg-pool connection pooling sized per source spec line 1212 ('200 max' with HPA awareness; scale to 200 only when wait > 50ms), with explicit awareness that horizontal pod replication multiplies clients per pod against this cap." New D1.8: "Deploy PgBouncer (or read replica) connection pooler alongside PostgreSQL to absorb horizontal-scaling client multiplication." M1 Exit Criteria adds PgBouncer smoke test. M1 Architectural Risks adds PgBouncer-required item. M4 Architectural Risks updated (PgBouncer absorbs horizontal-scaling). Dependency Graph adds D1.8 blocking constraint on D4.7 k6 load test. Risk Register gains "PostgreSQL 200-max connection cap" row. Cross-cutting Concerns §Performance Budgets updated.
- **Provenance tag**: `<!-- Source: R2.5 invariant probe INV-011 — modified per Change #13 -->` and `<!-- Source: R2.5 invariant probe INV-011 — added per Change #13 -->` (3 locations)
- **Validation**: D1.1 cites source spec line 1212; D1.8 PgBouncer present; risk-register row added; dependency-graph constraint added.

### Change #14 — Reconcile Rollback with revokeAll Semantics (INV-013) — APPLIED

- **Status**: APPLIED
- **Source**: R2.5 invariant probe INV-013 (HIGH UNADDRESSED); also resolves V1 self-contradiction (line 184 vs line 132 TokenManager.revokeAll semantics)
- **Target location**: M5 Architectural Risks (replace V1 lines 183-184) + Rollout procedure language + Workstreams §Operational Readiness
- **Before**: V1 line 184 said "rollback procedure must include either honoring those tokens via the old service... or forcing affected users to re-login". This contradicted V1 line 132 (`TokenManager.revokeAll()` invalidates all sessions on password reset).
- **After**: M5 Architectural Risks now reads: "Rollback after a revokeAll event (password reset, security incident) is forward-only; affected users re-login on the legacy or new service. Pre-revokeAll tokens are flushed in both services upon rollback to prevent stale-token validation drift." D5.6 description says "forward-only rollback procedure". D5.3 runbook list adds "forward-only rollback after revokeAll events". Workstreams §Operational Readiness references forward-only contract. Risk Register adds row. Contradiction between V1 lines 184 and 132 resolved by removing the "honor refresh tokens" clause entirely.
- **Provenance tag**: `<!-- Source: R2.5 invariant probe INV-013 — modified per Change #14 -->` (1 location); referenced in 4 other locations
- **Validation**: M5 risks contains "forward-only"; D5.3 runbook list contains "forward-only rollback"; D5.6 contains "forward-only rollback procedure"; risk-register row added; original "honor refresh tokens" phrasing absent (grep verified — only appears in historical-context bullet which itself describes the replacement).

---

## Post-Merge Validation Results

### Structural Integrity — PASSED

- Heading hierarchy: H1 (root) → H2 (10 sections) → H3 (5 milestone sections + "Why These Metrics") → no H2→H4 gaps.
- All milestone sections (M1-M5) retain consistent structure: Scope / Deliverables / Exit Criteria / Architectural Risks / Dependencies.
- New sections (Success Metrics, Sprint-Level Breakdown, Validation Strategy, Out-of-Scope) inserted at H2 level matching parent document hierarchy.
- No orphaned subsections; "Why These Metrics — Strategic Objectives" is correctly nested under §Success Metrics as H3.

### Internal References — PASSED

All references scanned and verified to resolve:

- **Deliverable IDs**: D1.1-D1.8 (8 in M1), D2.1-D2.6 (6 in M2), D3.1-D3.6 (6 in M3), D4.1-D4.8 (8 in M4), D5.1-D5.7 (7 in M5). All defined; all cross-references resolve.
- **Milestone IDs**: M1-M5. All defined as H3 sections.
- **FR IDs**: FR-AUTH-001 through FR-AUTH-005. All referenced and traced via Validation Strategy matrix.
- **NFR IDs**: NFR-PERF-001, NFR-PERF-002, NFR-REL-001, NFR-SEC-001, NFR-SEC-002. All referenced with gate threshold and validation method.
- **INV IDs**: INV-001, INV-002, INV-004, INV-005, INV-007, INV-011, INV-013. All 7 R2.5 probe additions tagged at every insertion site.
- **Change IDs**: Change #1 through Change #14. All 14 changes referenced in body text where relevant.

### Contradiction Re-scan — PASSED (both V1 contradictions resolved)

- **V1 contradiction A** (lines 183 vs 214): V1 §M5 risks said "2-day buffer between D5.2 and D5.7" while V1 §Risk Register said "pen-test scheduled with 2-week remediation window". Per Change #12, D5.2 remediation window is explicitly 7 days; M5 architectural risk states "The 7-day remediation window in D5.2 (per Change #12) replaces V1's original 2-day buffer." Risk Register row mitigation says "7-day remediation window in D5.2." No "2-day buffer" language remains in the merged document.
- **V1 contradiction B** (line 184 "rollback honors refresh tokens" vs line 132 `TokenManager.revokeAll()` semantics): Per Change #14, rollback contract is now "forward-only; affected users re-login... Pre-revokeAll tokens are flushed in both services upon rollback." No "honor refresh tokens" language remains as a forward-going contract — the only mention of the phrase is in the bullet that explicitly describes its replacement.

### Provenance Tag Coverage — PASSED

- **Document header**: 5 HTML comments (Provenance / Base / Incorporations / R2.5 list / Merge date).
- **Per-section tags**: 40 HTML comments distributed across all sections.
  - Original V1 content tags: 7 sections (Executive Summary, Milestones table, M2, Workstreams §intro, Cross-Cutting Concerns, Risk Register, Dependency Graph intro)
  - Modified V1 content tags: 6 sections (Strategic Objectives → Why These Metrics rationale, M1, M3, M4, M5, Open Questions, Dependency Graph)
  - V2 incorporation tags: 6 sections (Success Metrics, Sprint-Level Breakdown, Validation Strategy, Performance & Reliability Gates, Out-of-Scope, plus TDD §19.4 verbatim quote)
  - R2.5 invariant probe tags: 21 inline tags across deliverables, exit criteria, risks, and dependencies (INV-001 ×4, INV-002 ×2, INV-004 ×3, INV-005 ×3, INV-007 ×4, INV-011 ×3, INV-013 ×2)

### V1 Substantive Content Preservation — PASSED

- **Risk Register**: V1's 10 original rows all preserved verbatim or with minor mitigation augmentation referencing new Changes. 5 new rows added per Changes #8/#10/#11/#13/#14 (15 total rows).
- **Dependency Graph**: V1's critical path preserved; new sequencing constraints (D1.7, D1.8, D3.2 atomic, D5.1 boundary) inserted without removing V1 content.
- **Cross-Cutting Concerns**: All 4 V1 categories (Observability, Security, Performance Budgets, Data Integrity) preserved. Security item (4) and (6) augmented per Changes #10/#11. Performance Budgets augmented per Change #13.
- **Open Questions**: V1's 8 OQs and recommended positions preserved verbatim; OQ-9 (INV-001) appended.
- **Strategic Objectives**: All 6 V1 objectives preserved verbatim under "Why These Metrics" subsection.

---

## Summary

| Field                 | Value |
|-----------------------|-------|
| Changes planned       | 14    |
| Changes APPLIED       | 14    |
| Changes SKIPPED       | 0     |
| Changes FAILED        | 0     |
| Validation failures   | 0     |
| Word count (output)   | 8083  |
| Provenance tags (total) | 45  |

All 14 planned changes from refactor-plan.md applied successfully. V1 substantive content preserved in full (risk register, dependency graph, cross-cutting concerns, open questions). V2 tables incorporated additively (Change #1, #2, #4, #5) and as restructures (Change #3 with V1 GA criteria preserved as cluster row; Change #6 with V1 recommended positions preserved as prose under V2 table). R2.5 HIGH UNADDRESSED invariants (INV-001/002/004/005/007/011/013) all applied per plan. Both V1 self-contradictions resolved per Changes #12 and #14.

Merge complete. Merged artifact ready at `/config/workspace/IronClaude/.dev/eval-roadmap/groupB-direct/run1/merged-output.md`.
