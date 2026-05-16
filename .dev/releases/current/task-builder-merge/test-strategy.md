---
complexity_class: HIGH
validation_philosophy: continuous-parallel
validation_milestones: 7
work_milestones: 7
interleave_ratio: 1:1
major_issue_policy: stop-and-fix
spec_source: TDD_TASK_BUILDER_CONVERGENCE.md
generated: "2026-05-15T15:47:58.660437+00:00"
generator: superclaude-roadmap-executor
---

# Task-Builder Convergence v3.9 — Test Strategy

## 1. Validation Milestone Mapping (1:1 interleave with M1-M7)

**V1: M1 / FR-CONV.1 (PR-06) Validation** | 1 week (concurrent with M1 final 3 days) | exit: TB-Add-1..8 fixtures green; contract-freeze byte-diff PASS
**V2: M2 / FR-CONV.2 (PR-01) Validation** | 1 week (concurrent with M2 final 3 days) | exit: Execution Context header fixtures green; hidden-input determinism PASS
**V3: M3 / FR-CONV.3 (PR-04) Validation** | 1 week (concurrent with M3 final 3 days) | exit: INV-002 freshness + INV-019 Self-Audit fixtures green; anti-inflation byte-stable
**V4: M4 / FR-CONV.4 (PR-07) Validation** | 1 week (concurrent with M4 final 3 days) | exit: Five Axes overlay fixtures green; severity-floor byte-diff 0
**V5: M5 / FR-CONV.5 (PR-02) Validation** | 1 week (concurrent with M5 final 3 days) | exit: monotonicity + regression halt fixtures green; INV-012 dedup-no-regression PASS
**V6: M6 / FR-CONV.6 (PR-03) Validation** | 1 week (concurrent with M6 final 3 days) | exit: DNSP twice-exhaust + dedup-collapse + all-fail-bypass + cohort-no-serialize fixtures green
**V7: M7 GA Validation** | 2 weeks (concurrent with M7) | exit: K-003 audit PASS (100% Self-Audit coverage, first 5 runs); NFR-CONV.4 ratio ≤1.10 on 5 BUILD_REQUESTs; NFR-CONV.6..10 composite green; v3.9 GA tag

## 2. Test Categories

### 2.1 Unit / Synthetic Fixture Tests (Engineering owned, `uv run pytest`)
Per-FR fixture-driven verification — 25 named fixtures from TDD §15.2. Coverage target: 100% of Acceptance Criteria across FR-CONV.1..6 + NFR-CONV.3,6..10.

| Test ID | Name | FR / NFR | Assertion |
|---|---|---|---|
| TEST-001 | test_placeholder_tb_add_1 | FR-CONV.1 | TB-Add-1 emits item-ID-naming error; gate FAILs on "TBD"/"TODO"/title-only |
| TEST-002 | test_dag_cycle_tb_add_4 | FR-CONV.1 | TB-Add-4 emits on circular dependency; 100% detection |
| TEST-003 | test_evidence_bound_tb_add_8 | FR-CONV.1 | 3-sub-fixture: bare path FAIL / `:N` PASS / justified-absence PASS; resolves INV-015 |
| TEST-004 | test_execution_context_full | FR-CONV.2 | grep matches all 3 labeled lines (References/Source areas/Key constraints) |
| TEST-005 | test_execution_context_minimal_buildrequest | FR-CONV.2 | Degraded References-only; other 2 lines absent (not blank) |
| TEST-006 | test_execution_context_no_file_paths | FR-CONV.2 | `grep -E "src/\|/.*:[0-9]+"` against header range = 0 hits |
| TEST-007 | test_inherited_verdict_present | FR-CONV.3 | `## Inherited Structural Verdict` block in spawn log |
| TEST-008 | test_inherited_verdict_freshness_inv_002 | FR-CONV.3 / INV-002 | 2-cycle fixture: cycle-2 spawn carries cycle-2 verdict (byte-diff vs cycle-1) |
| TEST-009 | test_self_audit_inv_019 | FR-CONV.3 / INV-019 | `## Self-Audit` section + ≥1 documented semantic check beyond inherited verdict |
| TEST-010 | test_dynamic_enumeration_inv_010 | FR-CONV.3 / INV-010 | Checklist auto-richens after FR-CONV.1 catalogue growth |
| TEST-011 | test_five_axes_overlay | FR-CONV.4 | `### Five Adversarial Axes` header BEFORE 15-item checklist (ordering assertion) |
| TEST-012 | test_axis_column_populated | FR-CONV.4 | Every Items Reviewed row carries non-empty Axis ∈ {AX-1..5, none} |
| TEST-013 | test_drift_axis_inactive_when_no_goal_baseline | FR-CONV.4 | `drift-axis-inactive` annotation emitted in Summary; NOT N/A |
| TEST-014 | test_severity_floor_unweakened | FR-CONV.4 | byte-diff Critical Rules block at rf-qa-qualitative.md:786-795 = 0 |
| TEST-015 | test_monotonicity_halt_F_5_5_5 | FR-CONV.5 | `\|F\|=5,5,5` halts cycle 2 with `[HALT-MONOTONICITY]\|F\|=5`; no cycle 3 log |
| TEST-016 | test_regression_halt_pass1_fail2 | FR-CONV.5 | Item flip emits verbatim regression message BEFORE monotonicity check |
| TEST-017 | test_slow_shrink_continues | FR-CONV.5 | `\|F\|=5,4` continues; X-003 not triggered |
| TEST-018 | test_dnsp_twice_exhaust | FR-CONV.6 | All 5 fixed fields + dedup_key + found_n_times populated; severity HIGH |
| TEST-019 | test_dnsp_dedup_collapse | FR-CONV.6 | 2 identical dedup_key → cardinality 1 + found_n_times=2 |
| TEST-020 | test_dnsp_all_agents_fail_bypass | FR-CONV.6 | Zero-success path: no synthetic; rf-team-lead.md:417 activates |
| TEST-021 | test_dnsp_does_not_serialize_cohort | FR-CONV.6 / NFR-CONV.10 / INV-021 | spawn-log timestamps prove N-1 partitions overlap exhausted synthesis |
| TEST-022 | test_synthetic_dnsp_dedup_not_regression | FR-CONV.5+6 / INV-012 | Cross-cycle identical dedup_key proceeds to cycle 3; no regression halt |
| TEST-023 | test_hidden_input_guard | NFR-CONV.3 | byte-diff structural fields populated-done/ vs empty-done/ = 0 |
| TEST-024 | test_sequencing_PR06_before_PR04 | INV-010 | PR-04-before-PR-06 inversion: enumeration still richens once catalogue activates |
| TEST-025 | test_invariant_preservation_NFR_6_through_10 | NFR-CONV.6..10 | Composite: 5 invariants exercised, all PASS per Negative Criteria |

### 2.2 Integration Tests (cross-FR composition)
- **INV-010 enumeration:** TEST-010 + TEST-024 (FR-CONV.3 consumes FR-CONV.1 catalogue, including inversion case)
- **INV-012 dedup composition:** TEST-019 + TEST-022 (FR-CONV.5 monotonicity vs FR-CONV.6 cross-cycle dedup)
- **INV-013 inherited-PASS composition:** TEST-007 + TEST-011 (FR-CONV.4 axes focus on surface NOT covered by FR-CONV.3 inherited PASS)
- **INV-002 freshness on fix-cycle:** TEST-008 + halt-message integration (cycle-N+1 spawn carries fresh verdict during fix loops)

### 2.3 E2E Tests (full A.1-A.11 pipeline)
- 5 representative BUILD_REQUESTs (Quick / Standard / Deep tiers — same set used for NFR-CONV.4 measurement)
- Full pipeline: BUILD_REQUEST → rf-task-builder → rf-qa task-integrity → rf-qa-qualitative → present
- Asserts: MDTM file written; all 4 gates PASS or documented halt; structural fields byte-identical across 2 runs (NFR-CONV.1)

### 2.4 Acceptance Tests / Manual Audits (QA Lead owned)
- **K-003 audit (V7):** Manual review of first 5 real rf-qa-qualitative runs after FR-CONV.3 lands. Verify Self-Audit ≥1 independent semantic check beyond inherited PASS. **Block release on FAIL.**
- **NFR-CONV.4 measurement (V7):** Token-cost ratio on 5 BUILD_REQUESTs; target ≤1.10. **Contingency K-010** if exceeded: summarise FR-CONV.3 verdict table.
- **rf-team-lead.md:417 NO-DRIFT (every V):** byte-diff line 417 pre/post each FR commit.

### 2.5 Contract Tests (per API-001..004 from TDD §8)
- **API-001 (BUILD_REQUEST → MDTM):** schema validation — 15 fields + optional EXECUTION_CONTEXT_REQUIREMENTS; MALFORMED retry ≤2; header insertion point verified.
- **API-002 (rf-qa → rf-qa-qualitative):** Inherited Structural Verdict block injection point at SKILL.md:923-1000 (~:966); table byte-exact vs `qa-task-integrity.md` Items Reviewed table; missing-verdict → gate halts at §A.10.
- **API-003 (Partition → orchestrator):** synthetic-dnsp emission in normal output stream; merge step picks up at SKILL.md §A.8/§A.10; closed-vocabulary exhaust_point rejection test.
- **API-004 (Fix-Loop Halt Signals):** verbatim halt-message byte-exact match (regression first, monotonicity second, hard-cap third); F-set dedup-key identity.

### 2.6 Data Model Validation Tests (per DM-001..005 from TDD §7)
- **DM-001 Execution Context:** field types + degradation rule (References never omitted; Source areas/Key constraints omitted under minimal BUILD_REQUEST).
- **DM-002 Inherited Structural Verdict:** byte-exact `rf_qa_table_verbatim`; fixed-value `prompt_directive` and `reinjection_rule`.
- **DM-003 Synthetic DNSP:** all 7 fields populated; severity HIGH fixed; closed vocabulary on `escalation_ladder_exhaust_point`.
- **DM-004 Per-Item Schema:** ⚠ **BLOCKED ON Q-DM-1** — fixture targets whichever schema resolves (Engineering Lead decision pre-M1).
- **DM-005 Phase Contract:** 10-field producer/consumer agreement; schema_version 1.0.0; delivery_semantics at-most-once-per-cycle.

### 2.7 Migration Rollback Tests (per MIG-001..007 from roadmap)
- **MIG-001 (PR-06 revert):** TB-Add lines individually revertable; `make verify-sync` PASS post-revert.
- **MIG-002 (PR-01 revert):** Disable header generation; per-item Context fields unchanged; MDTM degrades to pre-header form.
- **MIG-003 (PR-04 revert):** Disable passthrough; rf-qa-qualitative falls back to independent structural re-checking.
- **MIG-004 (PR-07 revert):** Remove Axis column + `drift-axis-inactive`; 15-item checklist untouched.
- **MIG-005 (PR-02 revert):** Disable guards individually; per-gate caps remain governing.
- **MIG-006 (PR-03 revert):** Revert DNSP sites; rf-team-lead.md:417 already handles zero-partitions case.
- **Co-revert matrix tests:** FR-CONV.5+6 pair revert, FR-CONV.1→FR-CONV.3 enumeration-source revert.

### 2.8 Operational Readiness Tests (per OPS-001..007 from M7)
Runbook validation: OPS-001 K-003 audit, OPS-002 DNSP triage, OPS-003 all-exhaust HALT, OPS-004 monotonicity rate >50%, OPS-005 regression rate >20%, OPS-006 `make verify-sync` FAIL, OPS-007 INV-018 layout change. Each runbook executed against synthetic alert fixture; verify diagnosis path + resolution + escalation SLA documented.

## 3. Test-Implementation Interleaving Strategy

**Ratio: 1:1 (one validation milestone per work milestone)** — justified by HIGH complexity_class (0.7), 6-step strict serial sequencing with mutual-shape coupling (FR-CONV.5↔FR-CONV.6 dedup-key, FR-CONV.3↔FR-CONV.1 enumeration INV-010, FR-CONV.4↔FR-CONV.3 INV-013), 5 load-bearing invariants requiring per-FR fixture coverage, and Q-DM-1 CRITICAL schema-contradiction blocker on M1. Each FR commit must land green tests BEFORE the next FR begins — this is the K-007 sequencing-inversion mitigation. Continuous-parallel: validation fixtures authored concurrently with implementation (last 3 days of each M overlap with V); `make verify-sync` PASS is the per-FR landing gate (K-009).

**Per-FR gating sequence:**
1. FR implementation lands in `src/superclaude/` only (A-001).
2. `make sync-dev` → `make verify-sync` PASS (K-009).
3. FR-specific fixtures from §2.1 green via `uv run pytest`.
4. Contract test for relevant API-### green (§2.5).
5. Integration test for cross-FR composition (if applicable) green (§2.2).
6. Byte-diff invariant preservation checks PASS (rf-team-lead.md:417, anti-inflation 766-775, severity-floor 786-795, zero-trust 141-142).
7. → next FR may begin.

## 4. Risk-Based Test Prioritization

| Risk | Severity | Validation Coverage | Priority |
|---|---|---|---|
| K-002 / Q-DM-1 — Schema contradiction blocks TB-Add-6/8 baseline | CRITICAL | Pre-M1 Engineering Lead decision; DM-004 fixture targets resolved schema | P0 — BLOCKING |
| K-008 — INV-018 `.dev/tasks/` layout change | HIGH | NFR-CONV.8 layout diff test (TEST-025 composite); OPS-007 runbook test | P0 |
| K-003 — PR-04 passthrough inflation | MEDIUM | TEST-009 INV-019 Self-Audit + V7 K-003 manual audit on first 5 runs | P0 |
| K-007 — PR-04/PR-06 sequencing inversion | MEDIUM | TEST-024 enumeration-still-richens; strict serial gate per §3 | P0 |
| K-009 — A-001 sync violation | MEDIUM | `make verify-sync` PASS gate per FR; OPS-006 runbook | P0 |
| K-001 — TB-Add false positives | LOW | Per-TB-Add individually revertable; source-check-ID traceability | P1 |
| K-005 — Monotonicity halts legitimate slow-cycle | LOW | TEST-017 slow_shrink_continues | P1 |
| K-006 — DNSP masks real findings | LOW | HIGH severity assertion; TEST-021 cohort-no-serialize | P1 |
| K-010 — NFR-CONV.4 token ceiling exceeded | LOW | V7 measurement on 5 BUILD_REQUESTs; contingency = summarise verdict | P1 |
| K-004 — Axis over-flagging | LOW | TEST-014 severity-floor unweakened; V7 axis-distribution audit | P2 |

**Risk-weighted execution order:** Q-DM-1 resolution → byte-diff invariant tests (every V) → cross-FR composition tests (V3, V5, V6) → per-FR fixtures (each V) → K-003 audit (V7) → NFR-CONV.4 measurement (V7).

## 5. Acceptance Criteria per Milestone

**V1 (M1 / FR-CONV.1):**
- TEST-001, TEST-002, TEST-003 green
- COMP-001..006 surface map ratified; DM-001..005 + API-001..004 contract-shapes frozen (byte-diff gate)
- TB-Add-1/3/4/5/6/7/8 block on violation; TB-Add-2 emits `[ADVISORY]` and does NOT block
- No existing rf-qa check renamed/renumbered/removed (A-002)
- `make verify-sync` PASS
- Q-DM-1 resolution recorded in DM-004

**V2 (M2 / FR-CONV.2):**
- TEST-004, TEST-005, TEST-006 green
- Header degrades to References-only on minimal BUILD_REQUEST (other 2 lines omitted, not blank)
- `grep -E "src/\|/.*:[0-9]+"` against header range = 0
- Per-item Context fields retain file:line citations (NFR-CONV.7)
- TB-Add-7 tolerates degraded References-only form
- `make verify-sync` PASS

**V3 (M3 / FR-CONV.3):**
- TEST-007, TEST-008, TEST-009, TEST-010 green
- Spawn prompt carries verdict table byte-for-byte
- Fix-cycle re-injects NEW cycle-N verdict (INV-002)
- Self-Audit lists relied-on PASS items AND ≥1 semantic check (INV-019)
- Anti-inflation bullet at rf-qa-qualitative.md:770 byte-identical pre/post
- `make verify-sync` PASS

**V4 (M4 / FR-CONV.4):**
- TEST-011, TEST-012, TEST-013, TEST-014 green
- Five Adversarial Axes header BEFORE 15-item checklist
- Every task-qualitative row carries Axis ∈ {AX-1..AX-5, none}
- `drift-axis-inactive` annotation when no GOAL-baseline
- Severity floor 786-795 byte-identical
- 15-item checklist body byte-identical
- `make verify-sync` PASS

**V5 (M5 / FR-CONV.5):**
- TEST-015, TEST-016, TEST-017, TEST-022, TEST-024 green
- Regression halt emits BEFORE monotonicity check (verbatim message)
- Monotonicity halt emits `[HALT-MONOTONICITY] |F|=<n>` (verbatim)
- Slow-shrink (`|F|=5,4`) continues (X-003 NOT triggered)
- Identical-dedup_key synthetic across cycles does NOT trigger regression
- 4 retry counters NOT collapsed
- rf-team-lead.md:417 NO-DRIFT
- `make verify-sync` PASS

**V6 (M6 / FR-CONV.6):**
- TEST-018, TEST-019, TEST-020, TEST-021 green
- All 7 fields (5 fixed + dedup_key + found_n_times) populated; severity HIGH non-overridable
- Within-cycle dedup collapse to cardinality 1
- Zero-success path: NO synthetic + rf-team-lead.md:417 activates
- N-1 partitions overlap exhausted partition's synthesis (timestamp evidence)
- escalation_ladder_exhaust_point in closed vocabulary
- `make verify-sync` PASS

**V7 (M7 GA):**
- K-003 audit: 100% Self-Audit coverage on first 5 rf-qa-qualitative runs, each with ≥1 independent semantic check
- NFR-CONV.4: token-cost ratio ≤1.10 across all 5 representative BUILD_REQUESTs
- NFR-CONV.5 diff inspection: zero new external dep introductions across all 6 FRs
- NFR-CONV.8: `.dev/tasks/<task-id>/` layout diff pre/post = 0
- TEST-023, TEST-025 green
- NFR-CONV-R1: ≥4 of 5 BUILD_REQUESTs PASS task-integrity on first cycle (≥80%)
- Consolidated GA-Readiness Governance Table published
- OPS-001..007 runbooks published
- v3.9 GA tag created

## 6. Quality Gates Between Milestones

Each work milestone → validation milestone → next work milestone gate enforces:

| Gate | Check | Action on FAIL |
|---|---|---|
| G1 — Sync discipline | `make verify-sync` PASS | stop-and-fix (K-009); revert direct `.claude/` edits |
| G2 — Invariant byte-stability | Diff rf-team-lead.md:417, rf-qa.md:141-142, rf-qa-qualitative.md:766-775, rf-qa-qualitative.md:786-795 vs pre-FR baseline = 0 | stop-and-fix; block next milestone |
| G3 — FR fixtures | All FR-specific tests from §2.1 green | stop-and-fix; CRITICAL/MAJOR halt; MINOR tracked |
| G4 — Contract preservation | API-### contract test green; DM-### schema validation green | stop-and-fix; MAJOR before next milestone |
| G5 — Cross-FR composition | INV-002 / INV-010 / INV-012 / INV-013 / INV-019 / INV-021 tests green where applicable | stop-and-fix; MAJOR before next milestone |
| G6 — Existing-item preservation (A-002) | grep + diff confirms no rename/renumber/removal of existing rf-qa check, checklist item, or pipeline stage | stop-and-fix; revert offending change |
| G7 — K-003 audit (V3 → M4 gate) | First 5 real rf-qa-qualitative runs show Self-Audit + ≥1 independent check | CRITICAL; disable passthrough flag; block M4 until resolved |
| G8 — NFR-CONV.4 ceiling (V7 GA gate) | Token ratio ≤1.10 across 5 BUILD_REQUESTs | MAJOR; apply K-010 contingency (summarise verdict table); re-measure |
| G9 — Consolidated governance (V7 GA gate) | All 6 FF_* flags + 6 MET-* metrics + 7 OPS-* runbooks enumerated and validated | MAJOR; block GA tag |

**Issue classification applied at each gate:**
- **CRITICAL** (e.g., Q-DM-1 unresolved at M1 entry, K-003 audit FAIL, rf-team-lead.md:417 drift): stop-and-fix immediately; block current milestone
- **MAJOR** (e.g., FR fixture fails, contract drift, A-002 violation): stop-and-fix before next milestone
- **MINOR** (e.g., TB-Add false-positive single instance, log formatting): track and fix in next sprint
- **COSMETIC** (e.g., runbook wording, metric label): backlog
