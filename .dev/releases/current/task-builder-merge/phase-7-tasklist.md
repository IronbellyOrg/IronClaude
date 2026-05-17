# Phase 7 -- M7 Production Readiness + GA

**Phase Goal:** Audit first 5 rf-qa-qualitative runs post-FR-CONV.3 (K-003 / X-002 audit-target); measure token-cost on 5 representative BUILD_REQUESTs against NFR-CONV.4 ≤1.10 ratio; consolidate FLAG-*/MET-*/OPS-* into a single GA-readiness governance table; instrument observability counters (synthetic-dnsp, HALT-MONOTONICITY, regression-halt, Self-Audit coverage, make verify-sync PASS rate); ship runbook for OPS-001..007 scenarios; remove fallback paths at GA + 30 days; commit v3.9 GA. Duration: 2 weeks (2026-08-07 → 2026-08-21). Exit: K-003 audit PASS on first 5 rf-qa-qualitative runs (100% Self-Audit coverage with ≥1 independent semantic check each); NFR-CONV.4 ratio ≤1.10 across all 5 representative BUILD_REQUESTs; consolidated governance table published; observability counters live; v3.9 GA tagged.

### T07.01 -- Orchestrate MIG-007a K-003 first-5-runs audit

| Field | Value |
|---|---|
| Roadmap Item IDs | R-140 |
| Why | Coordinate K-003 audit on first 5 post-FR-CONV.3 rf-qa-qualitative runs; publish audit report with Self-Audit-coverage + independent-semantic-check evidence per run; QA-Lead sign-off. |
| Effort | S |
| Risk | Medium |
| Risk Drivers | scope:cross-cutting |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None; Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0083 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0083/spec.md`
- `TASKLIST_ROOT/artifacts/D-0083/evidence.md`

**Deliverables:**
- K-003 audit report published.
- First 5 rf-qa-qualitative runs with 100% Self-Audit coverage.
- Each run carries ≥1 independent semantic check.

**Steps:**
1. **[PLANNING]** Confirm M6 PASS; FR-CONV.3 + INV-019 live.
2. **[PLANNING]** Identify first 5 rf-qa-qualitative runs post-merge.
3. **[EXECUTION]** Collect Self-Audit content from each run.
4. **[EXECUTION]** Tabulate Self-Audit coverage + ≥1-semantic-check evidence per run.
5. **[VERIFICATION]** QA-Lead sign-off on audit report.
6. **[COMPLETION]** Publish at `TASKLIST_ROOT/artifacts/D-0083/spec.md`.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/artifacts/D-0083/spec.md` exists and lists all 5 runs with Self-Audit coverage = 100%.
- Each run carries ≥1 documented independent semantic check.
- QA-Lead sign-off recorded.
- Audit report cross-references OPS-001 runbook.

**Validation:**
- Manual check: reviewer (QA Lead) signs off on audit report.
- Evidence: published audit report + sign-off note.

**Dependencies:** Phase 6 (M6 PASS); FR-CONV.3 (M3)
**Rollback:** As stated in roadmap (if audit FAIL, roll back FR-CONV.3 per §19.4)
**Notes:** None.

### T07.02 -- Measure NFR-CONV.4 token-cost ratio (≤1.10)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-141 |
| Why | Measure token-cost ratio post-merge / pre-merge per equivalent BUILD_REQUEST across 5 representative BUILD_REQUESTs covering Quick/Standard/Deep tiers; ceiling 1.10. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None; Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0084 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0084/spec.md`
- `TASKLIST_ROOT/artifacts/D-0084/evidence.md`

**Deliverables:**
- Pre-merge baseline token counts for 5 representative BUILD_REQUESTs.
- Post-merge token counts for the same 5 BUILD_REQUESTs.
- Ratio table; all ≤1.10.

**Steps:**
1. **[PLANNING]** Read R-141 measurement spec.
2. **[PLANNING]** Select 5 BUILD_REQUESTs covering Quick/Standard/Deep tiers.
3. **[EXECUTION]** Capture pre-merge baseline token counts.
4. **[EXECUTION]** Capture post-merge token counts.
5. **[VERIFICATION]** Compute ratio per BUILD_REQUEST; assert all ≤1.10.
6. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/artifacts/D-0084/spec.md` exists and lists all 5 BUILD_REQUESTs with pre/post counts and ratios.
- All 5 ratios are ≤1.10.
- If any exceeds, K-010 contingency (summarise FR-CONV.3 verdict table) triggered.
- Evidence at `TASKLIST_ROOT/artifacts/D-0084/evidence.md`.

**Validation:**
- Manual check: Engineering Lead confirms ratios.
- Evidence: token-count tables.

**Dependencies:** Phase 6 (M6 PASS)
**Rollback:** As stated in roadmap (K-010 contingency)
**Notes:** None.

### T07.03 -- NFR-CONV.5-M7 no-new-dependencies diff audit

| Field | Value |
|---|---|
| Roadmap Item IDs | R-142 |
| Why | Audit all 6 FR diffs to confirm only Read/Grep/Glob/Bash used; no new MCP servers; no synchronous network calls. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None; Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0085 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0085/evidence.md`

**Deliverables:**
- Diff inspection across all 6 FR-CONV.X commits.
- Zero new MCP servers, libraries, or sync network calls.

**Steps:**
1. **[PLANNING]** Read R-142 audit spec.
2. **[EXECUTION]** Inspect MIG-001..MIG-006 diffs.
3. **[VERIFICATION]** Grep diffs for new MCP, libraries, network call patterns.
4. **[VERIFICATION]** Confirm only Read/Grep/Glob/Bash tooling used.
5. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- Diff inspection across 6 FR commits returns zero new external dep introductions.
- Tooling used confined to Read/Grep/Glob/Bash.
- No new MCP servers, libraries, or synchronous network calls.
- Evidence at `TASKLIST_ROOT/artifacts/D-0085/evidence.md`.

**Validation:**
- Manual check: reviewer confirms zero-new-dep finding.
- Evidence: diff inspection log.

**Dependencies:** Phase 6 (M6 PASS)
**Rollback:** As stated in roadmap
**Notes:** None.

### T07.04 -- Verify NFR-CONV.6 self-contained-item fixture

| Field | Value |
|---|---|
| Roadmap Item IDs | R-143 |
| Why | Synthetic fixture with all 5 fields populated PASSES all 8 TB-Add checks; same fixture with one field stripped FAILS TB-Add-1. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None; Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0086 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0086/evidence.md`

**Deliverables:**
- NFR-CONV.6 composite fixture committed.
- All 5 fields populated → PASS; one field stripped → FAIL TB-Add-1.

**Steps:**
1. **[PLANNING]** Confirm Q-DM-1 resolution recorded.
2. **[PLANNING]** Read R-143 fixture spec.
3. **[EXECUTION]** Author composite fixture under `tests/audit/`.
4. **[VERIFICATION]** Full-fields variant: assert all 8 TB-Add PASS.
5. **[VERIFICATION]** Field-stripped variant: assert TB-Add-1 FAIL.
6. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- `uv run pytest tests/audit/test_nfr_conv_6_self_contained.py -v` exits 0.
- Full-fields variant passes all 8 TB-Add checks.
- One-field-stripped variant fails TB-Add-1 with named field-ID.
- Fixture's schema reference matches the recorded Q-DM-1 resolution artifact (machine-checkable).
- Evidence at `TASKLIST_ROOT/artifacts/D-0086/evidence.md`.

**Validation:**
- Manual check: reviewer confirms binding to Q-DM-1 resolution.
- Evidence: pytest log.

**Dependencies:** Phase 1 (TB-Add-1..8 live); Q-DM-1
**Rollback:** As stated in roadmap
**Notes:** None.

### T07.05 -- Verify NFR-CONV.8 persistent .dev/tasks/ artifact

| Field | Value |
|---|---|
| Roadmap Item IDs | R-144 |
| Why | Diff `.dev/tasks/<task-id>/` directory layout pre-merge vs post-merge — zero structural changes (no new mandatory subdirectory, no rename, no naming-pattern change). |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None; Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0087 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0087/evidence.md`

**Deliverables:**
- Pre/post diff of `.dev/tasks/<task-id>/` directory layout.
- Zero structural changes (INV-018 preservation).

**Steps:**
1. **[PLANNING]** Read R-144 layout spec.
2. **[EXECUTION]** Capture pre-merge layout snapshot.
3. **[EXECUTION]** Capture post-merge layout snapshot.
4. **[VERIFICATION]** Diff snapshots; assert empty diff.
5. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- Diff output between pre-merge and post-merge directory layouts is empty.
- No new mandatory subdirectory; no rename of research/qa/synthesis/reviews/adversarial; no naming-pattern change.
- INV-018 preservation verified.
- Evidence at `TASKLIST_ROOT/artifacts/D-0087/evidence.md`.

**Validation:**
- Manual check: reviewer confirms layout stability.
- Evidence: diff output.

**Dependencies:** Phase 6 (M6 PASS)
**Rollback:** As stated in roadmap
**Notes:** None.

### T07.06 -- Checkpoint: Phase 7 / Tasks T07.01-T07.05

| Field | Value |
|---|---|
| Roadmap Item IDs | R-140, R-141, R-142, R-143, R-144 |
| Why | Gate: verify K-003 audit, NFR-CONV.4 token-cost ratio, NFR-CONV.5-M7 diff audit, NFR-CONV.6 self-contained, NFR-CONV.8 persistent-artifact preservation. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None |
| Tier | LIGHT |
| Confidence | [██████████] 100% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Quick sanity check |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-CP07-MID-T01-T05 |

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P07-T01-T05.md`

**Purpose:** Mid-phase gate confirming K-003 + NFR-CONV.4..8 audits PASS.

**Verification:**
- K-003 audit PASS on first 5 rf-qa-qualitative runs (D-0083 evidence).
- NFR-CONV.4 ratio ≤1.10 across 5 BUILD_REQUESTs (D-0084 evidence).
- NFR-CONV.5/.6/.8 invariants verified (D-0085..D-0087 evidence).

**Exit Criteria:**
- All 5 regular tasks T07.01-T07.05 report PASS.
- Zero new external dependency introduced.
- INV-018 layout stable.

**Steps:**
1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for the covered tasks.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/checkpoints/CP-P07-T01-T05.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report lists task IDs T07.01-T07.05.

**Validation:**
- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T07.01..T07.05
**Rollback:** N/A (checkpoints are read-only verifications)

### T07.07 -- Verify NFR-CONV.9 + NFR-CONV.2 (zero-trust + prose-determinism docs)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-145, R-146 |
| Why | NFR-CONV.9: two-part fixture verifying (a) 1-LOW-finding fixture → gate FAILS; (b) FR-CONV.3 inherited-verdict applied → no item marked VERIFIED unless Self-Audit lists independent semantic-check engagement. NFR-CONV.2: documentation of scope split (structural fields byte-deterministic; research-prose nondeterminism acceptable). |
| Effort | M |
| Risk | Medium |
| Risk Drivers | scope:cross-cutting |
| Tier | STRICT |
| Confidence | [████████--] 88% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0088 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0088/spec.md`
- `TASKLIST_ROOT/artifacts/D-0088/evidence.md`

**Deliverables:**
- NFR-CONV.9 two-part fixture PASS.
- NFR-CONV.2 prose-determinism documentation published.
- Verbatim PASS/FAIL definitions at rf-qa.md:141-142 byte-identical.

**Steps:**
1. **[PLANNING]** Read R-145, R-146 specs.
2. **[EXECUTION]** Author 1-LOW-finding fixture; assert FAIL.
3. **[EXECUTION]** Author inherited-verdict fixture; assert no VERIFIED without semantic-check.
4. **[EXECUTION]** Publish NFR-CONV.2 documentation page.
5. **[VERIFICATION]** Byte-diff rf-qa.md:141-142 pre/post; assert zero.
6. **[COMPLETION]** Sub-agent report.

**Acceptance Criteria:**
- Both fixture parts pass per spec.
- Byte-diff of rf-qa.md:141-142 PASS/FAIL definitions pre/post M5+M6 is zero.
- NFR-CONV.2 documentation page exists with structural vs prose boundary enumerated.
- Sub-agent report confirms structural annotations within prose remain byte-equal across 2 runs.

**Validation:**
- Manual check: reviewer confirms zero-trust QA preservation.
- Evidence: fixture logs + documentation page.

**Dependencies:** Phase 6 (M6 PASS); FR-CONV.3 (M3)
**Rollback:** As stated in roadmap
**Notes:** None.

### T07.08 -- Verify NFR-CONV-R1 + NFR-CONV.3 + TEST-023 hidden-input determinism

| Field | Value |
|---|---|
| Roadmap Item IDs | R-147, R-148, R-149 |
| Why | NFR-CONV-R1: run 5 representative BUILD_REQUESTs; count first-cycle PASS verdicts; target ≥80%. NFR-CONV.3: byte-identical structural output across populated vs empty `.dev/tasks/done/`. TEST-023 fixture asserting the same. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None; Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0089 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0089/spec.md`
- `TASKLIST_ROOT/artifacts/D-0089/evidence.md`

**Deliverables:**
- NFR-CONV-R1 first-cycle PASS rate ≥80% across 5 BUILD_REQUESTs.
- NFR-CONV.3 + TEST-023 byte-identical structural output.

**Steps:**
1. **[PLANNING]** Read R-147..R-149 specs.
2. **[EXECUTION]** Run 5 BUILD_REQUESTs; count first-cycle PASS.
3. **[EXECUTION]** Author TEST-023 fixture: populated vs empty `done/`.
4. **[VERIFICATION]** Assert ≥4 of 5 first-cycle PASS.
5. **[VERIFICATION]** Byte-diff structural fields = 0.
6. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- First-cycle PASS rate ≥80% (≥4 of 5 BUILD_REQUESTs) per `TASKLIST_ROOT/artifacts/D-0089/spec.md`.
- `uv run pytest tests/audit/test_hidden_input_guard.py -v` exits 0; byte-diff structural fields=0.
- PR-05 advisory mechanism remains REJECTED for Phase-1.
- Evidence at `TASKLIST_ROOT/artifacts/D-0089/evidence.md`.

**Validation:**
- Manual check: reviewer confirms ≥80% PASS rate.
- Evidence: pytest log + structural diff.

**Dependencies:** Phase 6 (M6 PASS)
**Rollback:** As stated in roadmap
**Notes:** None.

### T07.09 -- Commit TEST-025 invariant preservation composite

| Field | Value |
|---|---|
| Roadmap Item IDs | R-150 |
| Why | Composite fixture exercising all 5 invariants (self-contained-item, evidence-bound-item, persistent-artifact, zero-trust QA, parallel-research) per Negative Criteria. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 88% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None; Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0090 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0090/evidence.md`

**Deliverables:**
- TEST-025 composite fixture committed.
- All 5 invariants PASS.

**Steps:**
1. **[PLANNING]** Read R-150 fixture spec.
2. **[EXECUTION]** Author composite fixture exercising each invariant surface.
3. **[VERIFICATION]** Run pytest; assert all 5 invariants PASS.
4. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- `uv run pytest tests/audit/test_invariant_preservation_NFR_6_through_10.py -v` exits 0.
- Composite fixture exercises each of the 5 invariants (NFR-CONV.6..10).
- All 5 invariant assertions pass.
- Evidence at `TASKLIST_ROOT/artifacts/D-0090/evidence.md`.

**Validation:**
- Manual check: reviewer confirms each invariant surface exercised.
- Evidence: pytest log.

**Dependencies:** T07.04, T07.07, T07.08
**Rollback:** As stated in roadmap
**Notes:** None.

### T07.10 -- Publish Consolidated FLAG/MET/OPS governance table

| Field | Value |
|---|---|
| Roadmap Item IDs | R-151 |
| Why | Single consolidated governance table aggregating all 6 logical FF_* flags, 6 MET-* metrics with thresholds, and 7 OPS-* runbooks for the GA-tagging decision. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None; Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0091 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0091/spec.md`
- `TASKLIST_ROOT/artifacts/D-0091/evidence.md`

**Deliverables:**
- Single-page consolidated governance table published.
- 6 FF_* + 6 MET-* + 7 OPS-* enumerated.

**Steps:**
1. **[PLANNING]** Read R-151 table spec.
2. **[EXECUTION]** Author consolidated table aggregating all FF_*, MET-*, OPS-* with cleanup windows.
3. **[VERIFICATION]** Confirm all 6 FF_*, 6 MET-*, 7 OPS-* present.
4. **[COMPLETION]** Publish.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/artifacts/D-0091/spec.md` exists and lists exactly 6 FF_* flags, 6 MET-* metrics, 7 OPS-* runbooks.
- Each row includes cleanup window / SLA / threshold per roadmap §M7 Consolidated Governance Table.
- GA-tagging committee referenced as the audience.
- Evidence at `TASKLIST_ROOT/artifacts/D-0091/evidence.md`.

**Validation:**
- Manual check: GA-tagging committee confirms table is decision-ready.
- Evidence: published table.

**Dependencies:** Phase 6 (M6 PASS)
**Rollback:** As stated in roadmap
**Notes:** None.

### T07.11 -- Publish OPS-001 K-003 audit runbook

| Field | Value |
|---|---|
| Roadmap Item IDs | R-152 |
| Why | Runbook: symptoms / diagnosis / resolution / escalation / prevention for Self-Audit missing or zero-independent-checks; QA-Lead 4-business-hour response SLA. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None; Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0092 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0092/spec.md`

**Deliverables:**
- OPS-001 runbook published.
- Self-Audit-coverage gauge documented (100% first-5-runs).
- QA-Lead 4-business-hour SLA.

**Steps:**
1. **[PLANNING]** Read R-152 runbook spec.
2. **[EXECUTION]** Author OPS-001 runbook covering 5 sections (symptoms / diagnosis / resolution / escalation / prevention).
3. **[VERIFICATION]** Reviewer confirms 5 sections + SLA + gauge.
4. **[COMPLETION]** Publish.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/artifacts/D-0092/spec.md` exists and includes 5 runbook sections.
- Self-Audit-coverage gauge target documented at 100% first-5-runs.
- QA-Lead 4-business-hour response SLA explicitly stated.
- Cross-reference to MET-003 metric included.

**Validation:**
- Manual check: QA Lead reviews runbook.
- Evidence: published runbook.

**Dependencies:** T07.01
**Rollback:** As stated in roadmap
**Notes:** None.

### T07.12 -- Checkpoint: Phase 7 / Tasks T07.07-T07.11

| Field | Value |
|---|---|
| Roadmap Item IDs | R-145, R-146, R-147, R-148, R-149, R-150, R-151, R-152 |
| Why | Gate: verify NFR-CONV.9/.2/-R1/.3, TEST-025 composite, consolidated governance table, OPS-001 runbook. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None |
| Tier | LIGHT |
| Confidence | [██████████] 100% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Quick sanity check |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-CP07-MID-T07-T11 |

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P07-T07-T11.md`

**Purpose:** Mid-phase gate after NFR audits + invariant composite + governance table + first OPS runbook.

**Verification:**
- NFR-CONV.9 + NFR-CONV.2 fixtures + docs (D-0088 evidence).
- NFR-CONV-R1 + NFR-CONV.3 + TEST-025 invariant composite PASS (D-0089 + D-0090 evidence).
- Consolidated governance table + OPS-001 published (D-0091 + D-0092 evidence).

**Exit Criteria:**
- All 5 regular tasks T07.07-T07.11 report PASS.
- 6 FF_*, 6 MET-*, 7 OPS-* enumerated.
- First-cycle PASS rate ≥80%.

**Steps:**
1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for the covered tasks.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/checkpoints/CP-P07-T07-T11.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report lists task IDs T07.07-T07.11.

**Validation:**
- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T07.07..T07.11
**Rollback:** N/A (checkpoints are read-only verifications)

### T07.13 -- Publish OPS-002 DNSP triage runbook

| Field | Value |
|---|---|
| Roadmap Item IDs | R-153 |
| Why | Runbook: read affected partition's spawn-log; identify root cause of escalation-ladder exhaust; check dedup_key for prior similar events; escalate ≥3 distinct dedup-keys/week; 24-hour response SLA; weekly inspection cadence. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None; Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0093 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0093/spec.md`

**Deliverables:**
- OPS-002 runbook published.
- 24-hour SLA + weekly cadence.

**Steps:**
1. **[PLANNING]** Read R-153 spec.
2. **[EXECUTION]** Author OPS-002 runbook.
3. **[VERIFICATION]** Reviewer confirms SLA + cadence + escalation thresholds.
4. **[COMPLETION]** Publish.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/artifacts/D-0093/spec.md` exists with 5 runbook sections.
- 24-hour response SLA stated.
- Weekly inspection cadence documented.
- Escalation threshold (≥3 distinct dedup-keys/week) explicit.

**Validation:**
- Manual check: rf-qa maintainer reviews.
- Evidence: published runbook.

**Dependencies:** Phase 6 (M6 PASS); T07.12
**Rollback:** As stated in roadmap
**Notes:** None.

### T07.14 -- Publish OPS-003 All-partitions-exhaust HALT runbook

| Field | Value |
|---|---|
| Roadmap Item IDs | R-154 |
| Why | Runbook: confirm zero partition successes; verify line-417 escalation fired and NO synthetic-dnsp emitted (correct per FR-CONV.6 mutual-exclusivity); user resolves unresolved findings. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None; Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0094 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0094/spec.md`

**Deliverables:**
- OPS-003 runbook published.
- Mutual-exclusivity check documented.

**Steps:**
1. **[PLANNING]** Read R-154 spec.
2. **[EXECUTION]** Author OPS-003 runbook.
3. **[VERIFICATION]** Reviewer confirms mutual-exclusivity check.
4. **[COMPLETION]** Publish.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/artifacts/D-0094/spec.md` exists with 5 runbook sections.
- Mutual-exclusivity check explicitly documented.
- Cross-reference to rf-team-lead.md:417.
- Resolution path: user resolves unresolved findings.

**Validation:**
- Manual check: rf-team-lead maintainer reviews.
- Evidence: published runbook.

**Dependencies:** Phase 6 (M6 PASS); T07.13
**Rollback:** As stated in roadmap
**Notes:** None.

### T07.15 -- Publish OPS-004 HALT-MONOTONICITY rate runbook

| Field | Value |
|---|---|
| Roadmap Item IDs | R-155 |
| Why | Runbook: sample 3 halt events; inspect BUILD_REQUESTs for upstream defects; inspect MDTM for structural issues; resolution = improve upstream BUILD_REQUESTs or TB-Add-2 calibration (OPEN-INV-006). |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None; Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0095 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0095/spec.md`

**Deliverables:**
- OPS-004 runbook published.
- >50% threshold documented; upstream-quality-gate referral path.

**Steps:**
1. **[PLANNING]** Read R-155 spec.
2. **[EXECUTION]** Author OPS-004 runbook.
3. **[VERIFICATION]** Reviewer confirms threshold + referral path.
4. **[COMPLETION]** Publish.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/artifacts/D-0095/spec.md` exists with 5 runbook sections.
- >50% threshold documented.
- Resolution path: improve upstream BUILD_REQUESTs or TB-Add-2 calibration.
- Cross-reference to OPEN-INV-006.

**Validation:**
- Manual check: rf-task-builder maintainer reviews.
- Evidence: published runbook.

**Dependencies:** Phase 5 (M5 PASS); T07.14
**Rollback:** As stated in roadmap
**Notes:** None.

### T07.16 -- Publish OPS-005 Regression-halt rate runbook

| Field | Value |
|---|---|
| Roadmap Item IDs | R-156 |
| Why | Runbook: sample 3 regression events; inspect what changed between cycles; resolution = tighten fix-cycle prompts (X-003 slow-convergence threshold REJECTED). |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None; Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0096 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0096/spec.md`

**Deliverables:**
- OPS-005 runbook published.
- >20% threshold documented; Engineering-Lead escalation.

**Steps:**
1. **[PLANNING]** Read R-156 spec.
2. **[EXECUTION]** Author OPS-005 runbook.
3. **[VERIFICATION]** Reviewer confirms threshold + escalation.
4. **[COMPLETION]** Publish.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/artifacts/D-0096/spec.md` exists with 5 runbook sections.
- >20% threshold documented.
- Resolution path: tighten fix-cycle prompts; X-003 stays REJECTED.
- Engineering-Lead escalation path documented.

**Validation:**
- Manual check: Engineering Lead reviews.
- Evidence: published runbook.

**Dependencies:** Phase 5 (M5 PASS); T07.15
**Rollback:** As stated in roadmap
**Notes:** None.

### T07.17 -- Publish OPS-006 sync failure + OPS-007 layout-change runbooks

| Field | Value |
|---|---|
| Roadmap Item IDs | R-157, R-158 |
| Why | OPS-006: re-run `make sync-dev`; check git status for unsynced changes; verify CLAUDE.md sync-discipline (A-001); revert direct `.claude/` edit on persistent failure (K-009). OPS-007: inspect all 6 FRs for path/naming references; re-integration commit covering all 6 FRs per §19.4 (K-008). |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None; Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0097 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0097/spec.md`

**Deliverables:**
- OPS-006 runbook (sync failure).
- OPS-007 runbook (layout change).

**Steps:**
1. **[PLANNING]** Read R-157, R-158 specs.
2. **[EXECUTION]** Author OPS-006 + OPS-007 runbooks.
3. **[VERIFICATION]** Reviewer confirms SLAs + blast-radius response.
4. **[COMPLETION]** Publish.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/artifacts/D-0097/spec.md` exists with both OPS-006 + OPS-007 sections.
- OPS-006 references A-001 sync-discipline and K-009 contingency.
- OPS-007 references K-008 portfolio-wide blast radius and SP-33 stability commitment.
- Both runbooks have 5 sections each.

**Validation:**
- Manual check: Engineering Lead reviews.
- Evidence: published runbooks.

**Dependencies:** T07.16
**Rollback:** As stated in roadmap
**Notes:** None.

### T07.18 -- Checkpoint: Phase 7 / Tasks T07.13-T07.17

| Field | Value |
|---|---|
| Roadmap Item IDs | R-153, R-154, R-155, R-156, R-157, R-158 |
| Why | Gate: verify OPS-002..007 runbooks published before observability + GA-tag tasks. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None |
| Tier | LIGHT |
| Confidence | [██████████] 100% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Quick sanity check |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-CP07-MID-T13-T17 |

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P07-T13-T17.md`

**Purpose:** Mid-phase gate verifying OPS-002..007 runbooks are published with SLAs + thresholds.

**Verification:**
- OPS-002, OPS-003, OPS-004, OPS-005 runbooks published (D-0093..D-0096 evidence).
- OPS-006 + OPS-007 published (D-0097 evidence).
- All runbooks have 5 sections each.

**Exit Criteria:**
- All 5 regular tasks T07.13-T07.17 report PASS.
- 6 OPS-* runbooks (OPS-002..007) live (OPS-001 from T07.11).
- All SLAs + thresholds documented.

**Steps:**
1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for the covered tasks.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/checkpoints/CP-P07-T13-T17.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report lists task IDs T07.13-T07.17.

**Validation:**
- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T07.13..T07.17
**Rollback:** N/A (checkpoints are read-only verifications)

### T07.19 -- Instrument MET-001..006 observability counters

| Field | Value |
|---|---|
| Roadmap Item IDs | R-159, R-160, R-161, R-162, R-163, R-164 |
| Why | MET-001 Single-Pass Gate PASS Rate; MET-002 Detection Rate (unresolved-token + DAG-cycle 100%); MET-003 Self-Audit Coverage; MET-004 Halt Rate (synthetic-dnsp + HALT-MONOTONICITY + regression-halt); MET-005 DNSP Emission; MET-006 Token-Cost (NFR-CONV.4). |
| Effort | M |
| Risk | Medium |
| Risk Drivers | scope:cross-cutting |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None; Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0098 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0098/spec.md`
- `TASKLIST_ROOT/artifacts/D-0098/evidence.md`

**Deliverables:**
- MET-001..006 observability counters live via offline-grep aggregation.
- Each metric cross-referenced to OPS runbook trigger.

**Steps:**
1. **[PLANNING]** Read R-159..R-164 metric specs.
2. **[EXECUTION]** Wire offline-grep aggregation across QA reports for the 6 metrics.
3. **[EXECUTION]** Cross-reference each metric to its OPS trigger (e.g., MET-004 → OPS-004/OPS-005).
4. **[VERIFICATION]** Run aggregation; assert counts populated.
5. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/artifacts/D-0098/spec.md` exists and lists all 6 MET-001..006 with thresholds.
- MET-002 unresolved-token detection 100% on TB-Add-1 fixtures.
- MET-002 DAG-cycle detection 100% on TB-Add-4 fixtures.
- MET-006 token-cost ratio target ≤1.10 documented.
- Evidence at `TASKLIST_ROOT/artifacts/D-0098/evidence.md` including aggregation output.

**Validation:**
- Manual check: reviewer confirms each metric ties to an OPS runbook.
- Evidence: aggregation output.

**Dependencies:** T07.18
**Rollback:** As stated in roadmap
**Notes:** None.

### T07.20 -- Create MIG-007b v3.9 GA tag

| Field | Value |
|---|---|
| Roadmap Item IDs | R-165 |
| Why | Create v3.9 GA tag only after MIG-007a audit PASS + NFR-CONV.4 ratio ≤1.10 + consolidated governance table published + all 7 OPS runbooks live; rollback procedure documented. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | migration |
| Tier | STRICT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena; Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0099 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0099/spec.md`
- `TASKLIST_ROOT/artifacts/D-0099/evidence.md`

**Deliverables:**
- v3.9 GA tag created.
- PASS-gate criteria verified.
- Rollback procedure documented.

**Steps:**
1. **[PLANNING]** Confirm T07.01 K-003 audit PASS.
2. **[PLANNING]** Confirm T07.02 NFR-CONV.4 ratio ≤1.10.
3. **[PLANNING]** Confirm T07.10 consolidated governance table published.
4. **[PLANNING]** Confirm all 7 OPS runbooks live (T07.11 + T07.13..T07.17).
5. **[EXECUTION]** Spawn quality-engineer sub-agent for final PASS-gate verification.
6. **[EXECUTION]** Create v3.9 git tag with rollback procedure in tag message.

**Acceptance Criteria:**
- v3.9 git tag created and visible via `git tag -l v3.9`.
- Tag message references K-003 audit PASS + NFR-CONV.4 ratio + consolidated governance + 7 OPS runbooks.
- Sub-agent quality-engineer report confirms all PASS-gate criteria met.
- Rollback procedure documented in `TASKLIST_ROOT/artifacts/D-0099/spec.md`.

**Validation:**
- Manual check: GA-tagging committee approves.
- Evidence: git tag + sub-agent report + rollback documentation.

**Dependencies:** T07.01, T07.02, T07.10, T07.11, T07.13, T07.14, T07.15, T07.16, T07.17, T07.19
**Rollback:** As stated in roadmap (delete tag; revert per-FR commits in reverse order)
**Notes:** Critical-path override applied because GA tag governs production release.

### T07.21 -- Checkpoint: End of Phase 7 / Release GA

| Field | Value |
|---|---|
| Roadmap Item IDs | R-140, R-141, R-142, R-143, R-144, R-145, R-146, R-147, R-148, R-149, R-150, R-151, R-152, R-153, R-154, R-155, R-156, R-157, R-158, R-159, R-160, R-161, R-162, R-163, R-164, R-165 |
| Why | Gate: verify all M7 deliverables (K-003 audit, NFR-CONV.4..9 audits, invariant composite, consolidated governance table, OPS-001..007 runbooks, MET-001..006 counters, v3.9 GA tag) for release commitment. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None |
| Tier | LIGHT |
| Confidence | [██████████] 100% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Quick sanity check |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-CP07 |

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P07-END.md`

**Purpose:** End-of-Phase-7 / Release GA gate confirming all production-readiness deliverables landed and v3.9 GA tagged.

**Verification:**
- K-003 audit PASS + NFR-CONV.4 ratio ≤1.10 + NFR-CONV.5..9 audits verified (D-0083..D-0090 evidence).
- Consolidated governance table + OPS-001..007 runbooks + MET-001..006 observability live (D-0091..D-0098 evidence).
- v3.9 GA tag created with rollback procedure (D-0099 evidence).

**Exit Criteria:**
- All 18 regular tasks T07.01-T07.20 (skipping mid-checkpoints) report PASS.
- M7 Exit Conditions per roadmap (audit 100% Self-Audit coverage with ≥1 semantic check, NFR-CONV.4 ratio ≤1.10, governance table published, observability counters live, v3.9 GA tagged) all met.
- 14-week timeline (2026-05-15 → 2026-08-21) achieved within v3.9 GA = 2026-Q3 commitment.

**Steps:**
1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Inspect M7 Exit Conditions checklist; assert every item is satisfied.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above with `Overall: Pass` and release-GA confirmation.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/checkpoints/CP-P07-END.md` exists and contains `status: PASS` plus release-GA declaration.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report lists task IDs T07.01-T07.20 it covers.

**Validation:**
- Manual check: GA-tagging committee signs off.
- Evidence: the generated checkpoint markdown file + git tag confirmation.

**Dependencies:** T07.01..T07.20
**Rollback:** N/A (checkpoints are read-only verifications)
