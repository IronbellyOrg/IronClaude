# TASKLIST INDEX -- Task-Builder Convergence v3.9

## Metadata & Artifact Paths

| Field | Value |
|---|---|
| Sprint Name | Task-Builder Convergence v3.9 |
| Generator Version | Roadmap->Tasklist Generator v4.0 |
| Generated | 2026-05-17 |
| TASKLIST_ROOT | `.dev/releases/current/task-builder-merge/` |
| Total Phases | 7 |
| Total Tasks | 121 (100 regular + 21 checkpoints) |
| Total Deliverables | 100 regular (D-0001..D-0099 + D-0100) + 21 checkpoint (D-CP01..D-CP07 + 14 mid) |
| Complexity Class | HIGH |
| Primary Persona | architect |
| Consulting Personas | qa, refactorer, devops |

**Artifact Paths**

| Asset | Path |
|---|---|
| This file | `TASKLIST_ROOT/tasklist-index.md` |
| Phase 1 Tasklist | `TASKLIST_ROOT/phase-1-tasklist.md` |
| Phase 2 Tasklist | `TASKLIST_ROOT/phase-2-tasklist.md` |
| Phase 3 Tasklist | `TASKLIST_ROOT/phase-3-tasklist.md` |
| Phase 4 Tasklist | `TASKLIST_ROOT/phase-4-tasklist.md` |
| Phase 5 Tasklist | `TASKLIST_ROOT/phase-5-tasklist.md` |
| Phase 6 Tasklist | `TASKLIST_ROOT/phase-6-tasklist.md` |
| Phase 7 Tasklist | `TASKLIST_ROOT/phase-7-tasklist.md` |
| Execution Log | `TASKLIST_ROOT/execution-log.md` |
| Checkpoint Reports | `TASKLIST_ROOT/checkpoints/` |
| Evidence Directory | `TASKLIST_ROOT/evidence/` |
| Artifacts Directory | `TASKLIST_ROOT/artifacts/` |
| Validation Reports | `TASKLIST_ROOT/validation/` |
| Feedback Log | `TASKLIST_ROOT/feedback-log.md` |

## Phase Files

| Phase | File | Phase Name | Task IDs | Tier Distribution |
|---|---|---|---|---|
| 1 | phase-1-tasklist.md | M1 Architectural Surface + TB-Add Gates | T01.01-T01.18 | STRICT: 6, STANDARD: 8, LIGHT: 4 |
| 2 | phase-2-tasklist.md | M2 Execution Context Header | T02.01-T02.12 | STRICT: 3, STANDARD: 7, LIGHT: 2 |
| 3 | phase-3-tasklist.md | M3 Inherited Verdict + Self-Audit | T03.01-T03.18 | STRICT: 5, STANDARD: 10, LIGHT: 3 |
| 4 | phase-4-tasklist.md | M4 Five Adversarial Axes Overlay | T04.01-T04.16 | STRICT: 2, STANDARD: 11, LIGHT: 3 |
| 5 | phase-5-tasklist.md | M5 Retry Monotonicity + Regression Halts | T05.01-T05.18 | STRICT: 6, STANDARD: 9, LIGHT: 3 |
| 6 | phase-6-tasklist.md | M6 Synthetic DNSP on Partition Exhaust | T06.01-T06.18 | STRICT: 6, STANDARD: 9, LIGHT: 3 |
| 7 | phase-7-tasklist.md | M7 Production Readiness + GA | T07.01-T07.21 | STRICT: 2, STANDARD: 15, LIGHT: 4 |

## Source Snapshot

- Spec: Task-Builder Convergence v3.9 — six FR-CONV.1..6 functional requirements + post-merge M7 audit milestone, strictly serial per-FR-revertable delivery (PR-06 → PR-01 → PR-04 → PR-07 → PR-02 → PR-03).
- Intent-port (not implementation-port): adopts five sc-tasklist rigor mechanisms into task-builder skill without copying code; preserves five load-bearing invariants (NFR-CONV.6..10).
- Modification surface: 5 files (`src/superclaude/skills/task-builder/SKILL.md` + 4 rf-* agents totalling ~3,776 lines) plus preservation-only `rf-team-lead.md:417` anchor.
- Per-FR rollback granularity with explicit co-revert matrix (FR-CONV.5↔.6 dedup-key; FR-CONV.3↔.1 INV-010 enumeration; FR-CONV.4↔.3 INV-013 composition).
- 14-week timeline (2026-05-15 → 2026-08-21) within v3.9 GA = 2026-Q3 commitment.
- Critical-path blocker: Q-DM-1 schema-contradiction (PRD §25.4 vs SKILL.md:1450-1460) requires Engineering Lead decision pre-M1.

## Deterministic Rules Applied

- Phase buckets follow roadmap milestone headings M1..M7; renumbered sequentially with no gaps.
- Task IDs are zero-padded `T<PP>.<TT>`; checkpoints occupy their own task slot per v3.7 Wave 4 rule.
- Mid-phase checkpoints emitted after every 5 regular tasks; end-of-phase checkpoint is the last task in each phase.
- Roadmap items consolidated 1.4:1 average (165 source rows → 104 regular tasks) to satisfy structural gate <=25 tasks/phase while preserving R-### traceability.
- Effort/Risk computed per Section 5.2 keyword-scoring; tier classified per Section 5.3 priority order STRICT > EXEMPT > LIGHT > STANDARD.
- Verification routing aligned to tier per Section 4.10: STRICT → sub-agent; STANDARD → direct test; LIGHT → sanity check.
- Critical-path override applied where paths touch `auth/`, `security/`, `crypto/`, `models/`, `migrations/`; for this roadmap that means MIG-* tasks and DM-* schema-freeze tasks.
- No vague acceptance criteria; every task names a specific artifact at a specific path or a verbatim grep/diff command from the roadmap.
- No invented file paths beyond `TASKLIST_ROOT/artifacts/D-####/` placeholders; repository file paths copied verbatim from roadmap (`src/superclaude/skills/task-builder/SKILL.md`, `src/superclaude/agents/rf-qa.md`, etc.).
- Deliverable IDs (D-####) are globally unique and zero-padded; checkpoint deliverables use the `D-CP<PP>` and `D-CP<PP>-MID` reserved space.
- Traceability matrix preserves every R-### ID from the source roadmap; every task carries at least one R-### reference.
- Multi-file emission per File Emission Rules: index + 7 phase files, validation artifacts in `validation/` post-generation.

## Roadmap Item Registry

| Roadmap Item ID | Phase Bucket | Original Text (<= 20 words) |
|---|---|---|
| R-001 | M1 | COMP-001 task-builder Orchestrator surface anchor; SKILL.md Stage A orchestrator; central integration surface for FR-CONV.1..6 |
| R-002 | M1 | COMP-002 rf-task-builder Agent surface anchor; BUILD_REQUEST consumer and MDTM emitter; modified by FR-CONV.5 |
| R-003 | M1 | COMP-003 rf-qa Agent surface anchor; Structural QA agent — 4 phases; modified by FR-CONV.1/.5/.6 |
| R-004 | M1 | COMP-004 rf-qa-qualitative Agent surface anchor; consumes inherited verdict + axes overlay; modified by FR-CONV.3/.4/.6 |
| R-005 | M1 | COMP-005 rf-analyst Agent surface anchor; completeness verification + synthesis review; modified by FR-CONV.6 |
| R-006 | M1 | COMP-006 rf-team-lead Preservation surface anchor; existing all-agents-fail escalation guard UNMODIFIED line 417 |
| R-007 | M1 | FR-CONV.1 Append TB-Add-1..8 to rf-qa task-integrity gate (3 surface mirror); preserve zero-trust QA |
| R-008 | M1 | TB-Add-1 Placeholder scan check (Hard, blocking); detect TBD/TODO/title-only items |
| R-009 | M1 | TB-Add-2 Item-count bounds check (ADVISORY only); emits [ADVISORY] prefix and does NOT block gate |
| R-010 | M1 | TB-Add-3 Clarification-adjacency check (Hard, blocking); detect non-adjacent clarification items |
| R-011 | M1 | TB-Add-4 Circular-dependency DAG check (Hard, blocking); detect circular intra-/inter-phase dependencies |
| R-012 | M1 | TB-Add-5 Granularity / XL-has-subtasks check (Hard, blocking); detect XL items lacking decomposition |
| R-013 | M1 | TB-Add-6 Confidence / Verification format consistency check (Hard, blocking); validate enums + rationale |
| R-014 | M1 | TB-Add-7 Execution-Context source-areas cross-validation (Hard, blocking); validate Source areas reappear |
| R-015 | M1 | TB-Add-8 Per-item Context citation check (Hard, blocking; resolves INV-015); validate file:line citations |
| R-016 | M1 | DM-001 Execution Context Header schema (contract-freeze); 3 labeled lines |
| R-017 | M1 | DM-002 Inherited Structural Verdict Block schema (contract-freeze); rf_qa_table_verbatim + prompt_directive |
| R-018 | M1 | DM-003 Synthetic DNSP Finding schema (contract-freeze); 7 fields including dedup_key + found_n_times |
| R-019 | M1 | DM-004 Per-Item Checklist Schema (Q-DM-1 blocked); lands whichever schema resolves |
| R-020 | M1 | DM-005 Phase Contract schema rf-qa → rf-qa-qualitative (contract-freeze); 10-field producer/consumer |
| R-021 | M1 | API-001 BUILD_REQUEST → MDTM contract (contract-freeze); 15-field schema preservation |
| R-022 | M1 | API-002 Structural Verdict Handoff contract (contract-freeze); spawn-prompt injection mechanics |
| R-023 | M1 | API-003 Partition Finding Stream contract (contract-freeze); partition synthetic DNSP emission |
| R-024 | M1 | API-004 Fix-Loop Halt Signals contract (contract-freeze); monotonicity + regression halt strings |
| R-025 | M1 | TEST-001 test_placeholder_tb_add_1 synthetic fixture asserting TB-Add-1 fires |
| R-026 | M1 | TEST-002 test_dag_cycle_tb_add_4 synthetic fixture asserting TB-Add-4 fires on circular dependency |
| R-027 | M1 | TEST-003 test_evidence_bound_tb_add_8 three-fixture triple asserting TB-Add-8 behavior |
| R-028 | M1 | MIG-001 M1.1 PR-06 landing migration; strictly-additive append commits; per-line revertable |
| R-029 | M1 | NFR-CONV.1 Structural-field determinism instrumentation (M1 scope); byte-identical across runs |
| R-030 | M1 | NFR-CONV.5 No new external dependencies — diff inspection gate (contract-freeze at M1) |
| R-031 | M1 | FF_TB_ADD_1_THROUGH_8 Feature-flag governance (logical, no runtime flag); per-line revertable |
| R-032 | M2 | FR-CONV.2 Insert task-level Execution Context header (3 labeled lines, CASE-D PR-01) |
| R-033 | M2 | DM-001.References References field emitter; emit BUILD_REQUEST refs as R-###: list entries |
| R-034 | M2 | DM-001.SourceAreas Source areas field emitter (no file paths); hidden-input determinism rule |
| R-035 | M2 | DM-001.KeyConstraints Key constraints field emitter (1-3 entries); top invariants from BUILD_REQUEST |
| R-036 | M2 | API-001-M2 BUILD_REQUEST → MDTM contract update (M2 implementation); EXECUTION_CONTEXT_REQUIREMENTS signal |
| R-037 | M2 | DM-005-M2 Phase Contract DM-005 (10 fields, explicit row); published at M2 |
| R-038 | M2 | Degradation rule Minimal BUILD_REQUEST degradation behavior; block degrades to References-only |
| R-039 | M2 | Hidden-input guard No-file-paths invariant in header; grep returns 0 |
| R-040 | M2 | COMP-001-M2 SKILL.md primary template insertion (1407-1487) |
| R-041 | M2 | COMP-001-M2-r10 SKILL.md BUILD_REQUEST guidance update (715-725) |
| R-042 | M2 | COMP-002-M2 rf-task-builder header emission logic |
| R-043 | M2 | TEST-004 test_execution_context_full 3-labeled-line block in generated MDTM |
| R-044 | M2 | TEST-005 test_execution_context_minimal_buildrequest References-only degradation |
| R-045 | M2 | TEST-006 test_execution_context_no_file_paths grep returns 0 in header range |
| R-046 | M2 | NFR-CONV.7 Evidence-bound-item invariant preservation; per-item Context retains citations |
| R-047 | M2 | MIG-002 M1.2 PR-01 landing migration; strictly-additive header emission |
| R-048 | M2 | FF_EXECUTION_CONTEXT_HEADER Feature-flag governance (logical) |
| R-049 | M3 | FR-CONV.3 Inject Inherited Structural Verdict + Self-Audit (CASE-B PR-04) |
| R-050 | M3 | DM-002-M3 Inherited Structural Verdict Block schema (M3 implementation) |
| R-051 | M3 | DM-002.rf_qa_table_verbatim Verbatim table copy field; byte-exact |
| R-052 | M3 | DM-002.prompt_directive Fixed-value prompt directive string |
| R-053 | M3 | DM-002.reinjection_rule Fixed-value reinjection rule string |
| R-054 | M3 | API-002-M3 rf-qa → rf-qa-qualitative inter-agent API (M3 implementation); spawn-prompt injection |
| R-055 | M3 | Self-Audit output schema Add ## Self-Audit section to rf-qa-qualitative output |
| R-056 | M3 | INV-002 Freshness rule — cycle-N+1 reinjection; orchestrator MUST re-extract verdict |
| R-057 | M3 | INV-010 Dynamic checklist enumeration; auto-richens against TB-Add catalogue |
| R-058 | M3 | INV-019 Self-Audit consumer obligation; lists relied-on PASS + ≥1 semantic check |
| R-059 | M3 | Anti-inflation preservation rf-qa-qualitative.md:766-775 byte-stable |
| R-060 | M3 | Failure-mode handling rf-qa task-integrity verdict missing → halt before A.10.5 |
| R-061 | M3 | COMP-001-M3 SKILL.md A.10.5 spawn prompt injection (923-1000) |
| R-062 | M3 | COMP-004-M3 rf-qa-qualitative.md EOF append (line 794) |
| R-063 | M3 | TEST-007 test_inherited_verdict_present block in spawn prompt |
| R-064 | M3 | TEST-008 test_inherited_verdict_freshness_inv_002 2-cycle fixture |
| R-065 | M3 | TEST-009 test_self_audit_inv_019 ≥1 documented semantic check |
| R-066 | M3 | TEST-010 test_dynamic_enumeration_inv_010 checklist auto-richens |
| R-067 | M3 | MIG-003 M1.3 PR-04 landing migration; strictly-additive passthrough |
| R-068 | M3 | FF_INHERITED_STRUCTURAL_VERDICT Feature-flag governance; cleanup post-K-003 audit |
| R-069 | M3 | K-007 mitigation PR-04/PR-06 sequencing inversion contingency |
| R-070 | M4 | FR-CONV.4 Insert Five Adversarial Axes overlay (CASE-D PR-07); overlay-only |
| R-071 | M4 | AX-1 Drift axis definition; cited fact no longer matches current source |
| R-072 | M4 | AX-2 Contradictions axis definition; mutually incompatible facts |
| R-073 | M4 | AX-3 Omissions axis definition; required touchpoint absent from plan |
| R-074 | M4 | AX-4 Weakened-criteria axis definition; trivially satisfiable |
| R-075 | M4 | AX-5 Invented-content axis definition; requirement not present in upstream source |
| R-076 | M4 | none sentinel none-axis sentinel value; check passed and axis surfaced nothing |
| R-077 | M4 | drift-axis-inactive annotation Summary-block annotation when no GOAL-baseline |
| R-078 | M4 | Axis column on Items Reviewed table (rf-qa-qualitative.md:675-714) |
| R-079 | M4 | Five Adversarial Axes header subsection (rf-qa-qualitative.md:527) |
| R-080 | M4 | 15-item checklist preservation body unchanged at :527-583 |
| R-081 | M4 | Severity-floor preservation (786-795) rf-qa-qualitative severity floor unchanged |
| R-082 | M4 | COMP-004-M4 rf-qa-qualitative.md axis-column site (675-714) |
| R-083 | M4 | COMP-001-M4 SKILL.md task-qualitative prompt axis directive (961) |
| R-084 | M4 | TEST-011 test_five_axes_overlay axes header before immutable 15-item checklist |
| R-085 | M4 | TEST-012 test_axis_column_populated non-empty Axis value on every row |
| R-086 | M4 | TEST-013 test_drift_axis_inactive_when_no_goal_baseline annotation emitted |
| R-087 | M4 | TEST-014 test_severity_floor_unweakened block at :786-795 unchanged |
| R-088 | M4 | MIG-004 M1.4 PR-07 landing migration; strictly-additive overlay |
| R-089 | M4 | FF_FIVE_ADVERSARIAL_AXES Feature-flag governance; cleanup post-K-004 axis distribution audit |
| R-090 | M5 | FR-CONV.5 Add monotonicity + regression halt guards (CASE-D PR-02) |
| R-091 | M5 | API-004-M5 Fix-Loop Halt Signals contract (M5 implementation); ordering rule |
| R-092 | M5 | Monotonicity halt message [HALT-MONOTONICITY] \|F\|=<n> halt-string emitter |
| R-093 | M5 | Regression halt message verbatim regression-detection halt-string emitter |
| R-094 | M5 | F-set definition F_n set with dedup-key identity; cardinality post-dedup |
| R-095 | M5 | Ordering precedence rule regression > monotonicity > hard-cap > proceed |
| R-096 | M5 | INV-012 Cross-cycle synthetic-dnsp dedup composition; not regression |
| R-097 | M5 | 3-cycle hard cap preservation existing rf-team-lead.md:417 preservation |
| R-098 | M5 | Four-counter preservation Four independent retry counters MUST NOT collapse |
| R-099 | M5 | X-003 rejection enforcement No shrinks too slowly threshold |
| R-100 | M5 | COMP-001-M5 SKILL.md A.9 separate-counters invariant tail (867-873) |
| R-101 | M5 | COMP-001-M5-r12 SKILL.md Behavioral Constraints hard-invariants (1547-1553) |
| R-102 | M5 | COMP-002-M5 rf-task-builder.md I16 fix-cycle encoding (334-361) |
| R-103 | M5 | COMP-003-M5 rf-qa.md Fix Cycle Protocol Rules (308-315) |
| R-104 | M5 | TEST-015 test_monotonicity_halt_F_5_5_5 3-cycle fixture halts at cycle 2 |
| R-105 | M5 | TEST-016 test_regression_halt_pass1_fail2 PASS@1/FAIL@2 fixture |
| R-106 | M5 | TEST-017 test_slow_shrink_continues \|F\|=5,4 fixture continues |
| R-107 | M5 | TEST-022 test_synthetic_dnsp_dedup_not_regression cross-cycle same dedup_key proceeds |
| R-108 | M5 | TEST-024 test_sequencing_PR06_before_PR04 sequencing inversion mitigation |
| R-109 | M5 | MIG-005 M1.5 PR-02 landing migration; strictly-additive halts on existing loops |
| R-110 | M5 | FF_RETRY_MONOTONICITY_GUARDS Feature-flag governance; cleanup post-K-005 audit |
| R-111 | M6 | FR-CONV.6 Emit synthetic-dnsp on partition exhaust (CASE-B PR-03 BASE) |
| R-112 | M6 | DM-003-M6 Synthetic DNSP Finding schema (M6 implementation); 7 fields |
| R-113 | M6 | DM-003.severity severity field — fixed HIGH non-overridable |
| R-114 | M6 | DM-003.source source field — fixed synthetic-dnsp literal sentinel |
| R-115 | M6 | DM-003.affected_range affected_range field — assigned_files slice |
| R-116 | M6 | DM-003.evidence evidence field — spawn-log path or stub |
| R-117 | M6 | DM-003.recommendation recommendation field — fixed string Manual review required |
| R-118 | M6 | DM-003.dedup_key dedup_key field — 2-tuple identity; YAML list |
| R-119 | M6 | DM-003.found_n_times found_n_times field — collision counter; default 1 |
| R-120 | M6 | API-003-M6 Partition agent → orchestrator API (M6 implementation) |
| R-121 | M6 | escalation_ladder_exhaust_point vocabulary closed-vocabulary registry |
| R-122 | M6 | All-agents-fail guard precedence Zero-partitions-succeeded → NO synthetic |
| R-123 | M6 | Within-cycle dedup collapse Within-cycle identical-dedup_key collapse |
| R-124 | M6 | Cross-cycle dedup non-regression Cross-cycle identical-dedup_key NOT regression (INV-012) |
| R-125 | M6 | INV-021 Within-agent-instance emission; N-1 partitions continue concurrently |
| R-126 | M6 | HIGH severity non-overridable Synthetic findings emit ALONGSIDE real findings |
| R-127 | M6 | COMP-001-M6 SKILL.md A.8 Research Quality Gate (572-656) |
| R-128 | M6 | COMP-001-M6-r18 SKILL.md A.10 Task File Validation (870-918) |
| R-129 | M6 | COMP-005-M6 rf-analyst partition + DNSP edit site (58-71) |
| R-130 | M6 | COMP-003-M6 rf-qa DNSP edit site (49-77, primary at 70-77) |
| R-131 | M6 | COMP-004-M6 rf-qa-qualitative DNSP edit site (70-80) |
| R-132 | M6 | COMP-006-M6 rf-team-lead.md preservation (line 417 NO DRIFT) |
| R-133 | M6 | TEST-018 test_dnsp_twice_exhaust synthetic-dnsp finding with all 5 fixed fields |
| R-134 | M6 | TEST-019 test_dnsp_dedup_collapse identical-dedup_key collapse to found_n_times=2 |
| R-135 | M6 | TEST-020 test_dnsp_all_agents_fail_bypass zero partitions → no synthetic |
| R-136 | M6 | TEST-021 test_dnsp_does_not_serialize_cohort N-1 partitions concurrent (INV-021) |
| R-137 | M6 | MIG-006 M1.6 PR-03 landing migration; strictly-additive emission logic |
| R-138 | M6 | FF_SYNTHETIC_DNSP_EMISSION Feature-flag governance; cleanup post-K-006 emission audit |
| R-139 | M6 | NFR-CONV.10 Parallel-research invariant preservation; N partitions concurrent |
| R-140 | M7 | MIG-007a K-003 first-5-runs audit orchestration; publish audit report |
| R-141 | M7 | NFR-CONV.4 Token-cost ratio empirical measurement (≤1.10); 5 representative BUILD_REQUESTs |
| R-142 | M7 | NFR-CONV.5-M7 No-new-dependencies post-merge audit; diff inspection 6 FRs |
| R-143 | M7 | NFR-CONV.6 self-contained-item invariant fixture PASS; 5 fields populated |
| R-144 | M7 | NFR-CONV.8 Persistent .dev/tasks/ artifact invariant verification; diff layout |
| R-145 | M7 | NFR-CONV.9 Zero-trust QA invariant verification; two-part fixture |
| R-146 | M7 | NFR-CONV.2 Research-driven prose determinism exclusion documentation |
| R-147 | M7 | NFR-CONV-R1 Single-pass gate PASS rate baseline measurement; ≥80% target |
| R-148 | M7 | NFR-CONV.3 Hidden-input determinism guard verification; byte-identical output |
| R-149 | M7 | TEST-023 test_hidden_input_guard fixture populated .dev/tasks/done/ byte-identical |
| R-150 | M7 | TEST-025 test_invariant_preservation_NFR_6_through_10 composite |
| R-151 | M7 | Consolidated FLAG-*/MET-*/OPS-* governance table single-page audit artifact |
| R-152 | M7 | OPS-001 K-003 audit-target runbook first 5 rf-qa-qualitative runs |
| R-153 | M7 | OPS-002 DNSP triage runbook synthetic-dnsp emission count >0 |
| R-154 | M7 | OPS-003 All-partitions-exhaust HALT runbook no DNSP |
| R-155 | M7 | OPS-004 [HALT-MONOTONICITY] rate >50% runbook |
| R-156 | M7 | OPS-005 Regression-halt rate >20% runbook |
| R-157 | M7 | OPS-006 make verify-sync FAIL post-FR-merge runbook |
| R-158 | M7 | OPS-007 INV-018 layout-change runbook (K-008) |
| R-159 | M7 | MET-001 Single-Pass Gate PASS Rate measurement |
| R-160 | M7 | MET-002 Detection Rate measurement; unresolved-token + DAG-cycle |
| R-161 | M7 | MET-003 Self-Audit Coverage measurement |
| R-162 | M7 | MET-004 Halt Rate measurement (synthetic-dnsp + HALT-MONOTONICITY + regression-halt) |
| R-163 | M7 | MET-005 DNSP Emission measurement |
| R-164 | M7 | MET-006 Token-Cost measurement (NFR-CONV.4) |
| R-165 | M7 | MIG-007b GA tag creation gate (v3.9); audit PASS + ratio + governance + runbooks |

## Deliverable Registry

| Deliverable ID | Task ID | Roadmap Item ID(s) | Deliverable (short) | Tier | Verification | Intended Artifact Paths | Effort | Risk |
|---:|---:|---:|---|---|---|---|---|---|
| D-0001 | T01.01 | R-001..R-006 | COMP-001..006 surface-map document | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0001/spec.md | M | Medium |
| D-0002 | T01.02 | R-007 | FR-CONV.1 wrapper landed in rf-qa A.10 across 3 surfaces | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0002/spec.md | L | Medium |
| D-0003 | T01.03 | R-008 | TB-Add-1 placeholder-scan check live | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0003/evidence.md | S | Low |
| D-0004 | T01.04 | R-009 | TB-Add-2 item-count bounds advisory check live | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0004/evidence.md | S | Low |
| D-0005 | T01.05 | R-010 | TB-Add-3 clarification-adjacency check live | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0005/evidence.md | S | Low |
| D-0006 | T01.07 | R-011 | TB-Add-4 circular-dependency DAG check live | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0006/evidence.md | S | Low |
| D-0007 | T01.08 | R-012 | TB-Add-5 granularity/XL-subtasks check live | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0007/evidence.md | S | Low |
| D-0008 | T01.09 | R-013 | TB-Add-6 confidence/verification format check live | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0008/evidence.md | S | Low |
| D-0009 | T01.10 | R-014 | TB-Add-7 source-areas cross-validation check live | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0009/evidence.md | S | Low |
| D-0010 | T01.11 | R-015 | TB-Add-8 per-item Context citation check live | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0010/evidence.md | S | Medium |
| D-0011 | T01.13 | R-016..R-020 | DM-001..005 schema contract-freeze ratification | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0011/spec.md | M | Medium |
| D-0012 | T01.14 | R-021..R-024 | API-001..004 contract-freeze ratification | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0012/spec.md | M | Medium |
| D-0013 | T01.15 | R-025..R-027 | TEST-001..003 synthetic fixtures committed | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0013/evidence.md | S | Low |
| D-0014 | T01.16 | R-028 | MIG-001 PR-06 landing commit | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0014/spec.md | M | High |
| D-0015 | T01.17 | R-029..R-031 | NFR-CONV.1 + NFR-CONV.5 audits + FF_TB governance | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0015/evidence.md | S | Low |
| D-CP01-MID-T01-T05 | T01.06 | R-001..R-010 | Mid-phase checkpoint report after T01.01-T01.05 | LIGHT | Quick sanity check | TASKLIST_ROOT/checkpoints/CP-P01-T01-T05.md | XS | Low |
| D-CP01-MID-T07-T11 | T01.12 | R-011..R-015 | Mid-phase checkpoint report after T01.07-T01.11 | LIGHT | Quick sanity check | TASKLIST_ROOT/checkpoints/CP-P01-T07-T11.md | XS | Low |
| D-CP01 | T01.18 | R-001..R-031 | End-of-phase 1 checkpoint report | LIGHT | Quick sanity check | TASKLIST_ROOT/checkpoints/CP-P01-END.md | XS | Low |
| D-0016 | T02.01 | R-032 | FR-CONV.2 Execution Context header landed | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0016/spec.md | S | Low |
| D-0017 | T02.02 | R-033..R-035 | DM-001 References / SourceAreas / KeyConstraints emitters | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0017/spec.md | S | Low |
| D-0018 | T02.03 | R-036 | API-001-M2 BUILD_REQUEST contract update | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0018/spec.md | M | Medium |
| D-0019 | T02.04 | R-037 | DM-005-M2 Phase Contract row published | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0019/spec.md | S | Low |
| D-0020 | T02.05 | R-038..R-039 | Degradation rule + hidden-input guard wired | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0020/evidence.md | S | Low |
| D-0021 | T02.07 | R-040..R-041 | COMP-001-M2 SKILL.md template insertion + guidance update | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0021/spec.md | S | Low |
| D-0022 | T02.08 | R-042 | COMP-002-M2 rf-task-builder header emission logic | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0022/spec.md | S | Low |
| D-0023 | T02.09 | R-043..R-045 | TEST-004..006 fixtures committed | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0023/evidence.md | S | Low |
| D-0024 | T02.10 | R-046 | NFR-CONV.7 evidence-bound preservation evidence | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0024/evidence.md | S | Medium |
| D-0025 | T02.11 | R-047..R-048 | MIG-002 landing + FF_EXECUTION_CONTEXT_HEADER governance | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0025/spec.md | M | High |
| D-CP02-MID-T01-T05 | T02.06 | R-032..R-039 | Mid-phase checkpoint report after T02.01-T02.05 | LIGHT | Quick sanity check | TASKLIST_ROOT/checkpoints/CP-P02-T01-T05.md | XS | Low |
| D-CP02 | T02.12 | R-032..R-048 | End-of-phase 2 checkpoint report | LIGHT | Quick sanity check | TASKLIST_ROOT/checkpoints/CP-P02-END.md | XS | Low |
| D-0026 | T03.01 | R-049 | FR-CONV.3 Inherited Verdict + Self-Audit wrapper landed | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0026/spec.md | M | Medium |
| D-0027 | T03.02 | R-050..R-053 | DM-002-M3 schema implementation (3 sub-fields) | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0027/spec.md | M | Medium |
| D-0028 | T03.03 | R-054 | API-002-M3 spawn-prompt injection at SKILL.md §A.10.5 | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0028/spec.md | M | Medium |
| D-0029 | T03.04 | R-055, R-058 | Self-Audit output schema + INV-019 obligation | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0029/spec.md | S | Medium |
| D-0030 | T03.05 | R-056 | INV-002 freshness rule wired | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0030/evidence.md | S | Low |
| D-0031 | T03.07 | R-057 | INV-010 dynamic checklist enumeration wired | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0031/evidence.md | S | Low |
| D-0032 | T03.08 | R-059..R-060 | Anti-inflation preservation + failure-mode halt | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0032/spec.md | S | Medium |
| D-0033 | T03.09 | R-061 | COMP-001-M3 SKILL.md A.10.5 spawn injection (923-1000) | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0033/evidence.md | S | Low |
| D-0034 | T03.10 | R-062 | COMP-004-M3 rf-qa-qualitative EOF append (line 794) | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0034/evidence.md | S | Low |
| D-0035 | T03.11 | R-063 | TEST-007 inherited verdict present fixture | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0035/evidence.md | S | Low |
| D-0036 | T03.13 | R-064 | TEST-008 freshness INV-002 2-cycle fixture | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0036/evidence.md | S | Low |
| D-0037 | T03.14 | R-065 | TEST-009 self-audit INV-019 semantic-check fixture | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0037/evidence.md | S | Low |
| D-0038 | T03.15 | R-066 | TEST-010 dynamic enumeration INV-010 fixture | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0038/evidence.md | S | Low |
| D-0039 | T03.16 | R-067..R-068 | MIG-003 landing + FF_INHERITED_STRUCTURAL_VERDICT governance | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0039/spec.md | M | Medium |
| D-0040 | T03.17 | R-069 | K-007 sequencing inversion mitigation note | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0040/evidence.md | S | Low |
| D-CP03-MID-T01-T05 | T03.06 | R-049..R-056 | Mid-phase checkpoint report after T03.01-T03.05 | LIGHT | Quick sanity check | TASKLIST_ROOT/checkpoints/CP-P03-T01-T05.md | XS | Low |
| D-CP03-MID-T07-T11 | T03.12 | R-057..R-063 | Mid-phase checkpoint report after T03.07-T03.11 | LIGHT | Quick sanity check | TASKLIST_ROOT/checkpoints/CP-P03-T07-T11.md | XS | Low |
| D-CP03 | T03.18 | R-049..R-069 | End-of-phase 3 checkpoint report | LIGHT | Quick sanity check | TASKLIST_ROOT/checkpoints/CP-P03-END.md | XS | Low |
| D-0041 | T04.01 | R-070 | FR-CONV.4 axis overlay wrapper landed | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0041/spec.md | S | Low |
| D-0042 | T04.02 | R-071..R-072 | AX-1 + AX-2 axis definitions in canonical block | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0042/spec.md | S | Low |
| D-0043 | T04.03 | R-073..R-074 | AX-3 + AX-4 axis definitions in canonical block | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0043/spec.md | S | Low |
| D-0044 | T04.04 | R-075 | AX-5 axis definition in canonical block | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0044/spec.md | S | Low |
| D-0045 | T04.05 | R-076..R-077 | `none` sentinel + `drift-axis-inactive` annotation | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0045/spec.md | S | Low |
| D-0046 | T04.07 | R-078 | Axis column on Items Reviewed table | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0046/spec.md | S | Low |
| D-0047 | T04.08 | R-079 | Five Adversarial Axes header subsection | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0047/spec.md | S | Low |
| D-0048 | T04.09 | R-080 | 15-item checklist preservation diff | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0048/evidence.md | S | Low |
| D-0049 | T04.10 | R-081 | Severity-floor preservation (786-795) diff | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0049/evidence.md | S | Low |
| D-0050 | T04.11 | R-082 | COMP-004-M4 axis-column site edit | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0050/spec.md | S | Low |
| D-0051 | T04.13 | R-083 | COMP-001-M4 SKILL.md task-qualitative prompt axis directive | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0051/spec.md | S | Low |
| D-0052 | T04.14 | R-084..R-087 | TEST-011..014 axis overlay fixtures | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0052/evidence.md | S | Low |
| D-0053 | T04.15 | R-088..R-089 | MIG-004 landing + FF_FIVE_ADVERSARIAL_AXES governance | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0053/spec.md | M | Medium |
| D-CP04-MID-T01-T05 | T04.06 | R-070..R-077 | Mid-phase checkpoint report after T04.01-T04.05 | LIGHT | Quick sanity check | TASKLIST_ROOT/checkpoints/CP-P04-T01-T05.md | XS | Low |
| D-CP04-MID-T07-T11 | T04.12 | R-078..R-082 | Mid-phase checkpoint report after T04.07-T04.11 | LIGHT | Quick sanity check | TASKLIST_ROOT/checkpoints/CP-P04-T07-T11.md | XS | Low |
| D-CP04 | T04.18 | R-070..R-089 | End-of-phase 4 checkpoint report | LIGHT | Quick sanity check | TASKLIST_ROOT/checkpoints/CP-P04-END.md | XS | Low |
| D-0054 | T05.01 | R-090 | FR-CONV.5 halt-guards wrapper landed | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0054/spec.md | M | Medium |
| D-0055 | T05.02 | R-091 | API-004-M5 fix-loop halt-signals contract | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0055/spec.md | S | Low |
| D-0056 | T05.03 | R-092 | Monotonicity halt-message emitter | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0056/spec.md | S | Low |
| D-0057 | T05.04 | R-093 | Regression halt-message emitter | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0057/spec.md | S | Low |
| D-0058 | T05.05 | R-094..R-095 | F-set definition + ordering precedence rule | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0058/spec.md | S | Medium |
| D-0059 | T05.07 | R-096 | INV-012 cross-cycle dedup composition rule | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0059/spec.md | S | Medium |
| D-0060 | T05.08 | R-097..R-099 | 3-cycle hard cap + four-counter + X-003 preservation evidence | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0060/evidence.md | S | Medium |
| D-0061 | T05.09 | R-100..R-101 | COMP-001-M5 SKILL.md A.9 + behavioral constraints edits | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0061/spec.md | S | Low |
| D-0062 | T05.10 | R-102 | COMP-002-M5 rf-task-builder.md I16 edit | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0062/spec.md | S | Low |
| D-0063 | T05.11 | R-103 | COMP-003-M5 rf-qa.md Fix Cycle Protocol Rules edit | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0063/spec.md | S | Low |
| D-0064 | T05.13 | R-104..R-105 | TEST-015 + TEST-016 monotonicity + regression fixtures | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0064/evidence.md | S | Low |
| D-0065 | T05.14 | R-106..R-107 | TEST-017 + TEST-022 slow-shrink + dedup fixtures | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0065/evidence.md | S | Low |
| D-0066 | T05.15 | R-108 | TEST-024 sequencing inversion fixture | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0066/evidence.md | S | Low |
| D-0067 | T05.16 | R-109..R-110 | MIG-005 landing + FF_RETRY_MONOTONICITY_GUARDS governance | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0067/spec.md | M | High |
| D-0100 | T05.17 | R-099 | False-halt-rate sweep prep for M7 K-005 audit | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0100/notes.md | S | Low |
| D-CP05-MID-T01-T05 | T05.06 | R-090..R-095 | Mid-phase checkpoint report after T05.01-T05.05 | LIGHT | Quick sanity check | TASKLIST_ROOT/checkpoints/CP-P05-T01-T05.md | XS | Low |
| D-CP05-MID-T07-T11 | T05.12 | R-096..R-103 | Mid-phase checkpoint report after T05.07-T05.11 | LIGHT | Quick sanity check | TASKLIST_ROOT/checkpoints/CP-P05-T07-T11.md | XS | Low |
| D-CP05 | T05.18 | R-090..R-110 | End-of-phase 5 checkpoint report | LIGHT | Quick sanity check | TASKLIST_ROOT/checkpoints/CP-P05-END.md | XS | Low |
| D-0068 | T06.01 | R-111 | FR-CONV.6 synthetic-dnsp emission wrapper landed | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0068/spec.md | L | Medium |
| D-0069 | T06.02 | R-112 | DM-003-M6 7-field schema implementation | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0069/spec.md | M | Medium |
| D-0070 | T06.03 | R-113..R-114 | DM-003.severity + DM-003.source fixed-field emitters | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0070/spec.md | S | Low |
| D-0071 | T06.04 | R-115..R-116 | DM-003.affected_range + DM-003.evidence emitters | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0071/spec.md | S | Low |
| D-0072 | T06.05 | R-117..R-119 | DM-003.recommendation + dedup_key + found_n_times emitters | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0072/spec.md | S | Medium |
| D-0073 | T06.07 | R-120..R-121 | API-003-M6 partition emission API + exhaust-point vocabulary | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0073/spec.md | M | Medium |
| D-0074 | T06.08 | R-122 | All-agents-fail guard precedence mutually-exclusive paths | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0074/spec.md | S | High |
| D-0075 | T06.09 | R-123..R-124 | Within-cycle dedup collapse + cross-cycle non-regression (INV-012) | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0075/spec.md | S | Medium |
| D-0076 | T06.10 | R-125..R-126 | INV-021 N-1 concurrency + HIGH severity non-overridable | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0076/spec.md | S | Medium |
| D-0077 | T06.11 | R-127..R-128 | COMP-001-M6 + r18 SKILL.md A.8 + A.10 merge step | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0077/spec.md | S | Low |
| D-0078 | T06.13 | R-129..R-130 | COMP-005-M6 + COMP-003-M6 rf-analyst + rf-qa DNSP edit sites | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0078/spec.md | S | Low |
| D-0079 | T06.14 | R-131..R-132 | COMP-004-M6 + COMP-006-M6 rf-qa-qualitative DNSP + rf-team-lead preservation | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0079/spec.md | S | Medium |
| D-0080 | T06.15 | R-133..R-134 | TEST-018 + TEST-019 dnsp twice-exhaust + dedup-collapse fixtures | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0080/evidence.md | S | Low |
| D-0081 | T06.16 | R-135..R-136 | TEST-020 + TEST-021 all-agents-fail + cohort-concurrency fixtures | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0081/evidence.md | S | Low |
| D-0082 | T06.17 | R-137..R-139 | MIG-006 + FF_SYNTHETIC_DNSP_EMISSION + NFR-CONV.10 invariant | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0082/spec.md | M | High |
| D-CP06-MID-T01-T05 | T06.06 | R-111..R-119 | Mid-phase checkpoint report after T06.01-T06.05 | LIGHT | Quick sanity check | TASKLIST_ROOT/checkpoints/CP-P06-T01-T05.md | XS | Low |
| D-CP06-MID-T07-T11 | T06.12 | R-120..R-128 | Mid-phase checkpoint report after T06.07-T06.11 | LIGHT | Quick sanity check | TASKLIST_ROOT/checkpoints/CP-P06-T07-T11.md | XS | Low |
| D-CP06 | T06.18 | R-111..R-139 | End-of-phase 6 checkpoint report | LIGHT | Quick sanity check | TASKLIST_ROOT/checkpoints/CP-P06-END.md | XS | Low |
| D-0083 | T07.01 | R-140 | MIG-007a K-003 first-5-runs audit report | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0083/spec.md | S | Medium |
| D-0084 | T07.02 | R-141 | NFR-CONV.4 token-cost ratio measurement (≤1.10) | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0084/spec.md | S | Low |
| D-0085 | T07.03 | R-142 | NFR-CONV.5-M7 no-new-dependencies diff audit | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0085/evidence.md | S | Low |
| D-0086 | T07.04 | R-143 | NFR-CONV.6 self-contained-item fixture PASS | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0086/evidence.md | S | Low |
| D-0087 | T07.05 | R-144 | NFR-CONV.8 persistent .dev/tasks/ layout diff | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0087/evidence.md | S | Low |
| D-0088 | T07.07 | R-145..R-146 | NFR-CONV.9 zero-trust + NFR-CONV.2 prose-determinism docs | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0088/spec.md | M | Medium |
| D-0089 | T07.08 | R-147..R-149 | NFR-CONV-R1 + NFR-CONV.3 + TEST-023 hidden-input determinism | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0089/spec.md | S | Low |
| D-0090 | T07.09 | R-150 | TEST-025 invariant preservation composite fixture | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0090/evidence.md | S | Low |
| D-0091 | T07.10 | R-151 | Consolidated FLAG/MET/OPS governance table published | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0091/spec.md | S | Low |
| D-0092 | T07.11 | R-152 | OPS-001 K-003 audit runbook published | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0092/spec.md | S | Low |
| D-0093 | T07.13 | R-153 | OPS-002 DNSP triage runbook published | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0093/spec.md | S | Low |
| D-0094 | T07.14 | R-154 | OPS-003 All-partitions-exhaust HALT runbook published | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0094/spec.md | S | Low |
| D-0095 | T07.15 | R-155 | OPS-004 HALT-MONOTONICITY rate runbook published | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0095/spec.md | S | Low |
| D-0096 | T07.16 | R-156 | OPS-005 Regression-halt rate runbook published | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0096/spec.md | S | Low |
| D-0097 | T07.17 | R-157..R-158 | OPS-006 sync failure + OPS-007 layout-change runbooks | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0097/spec.md | S | Low |
| D-0098 | T07.19 | R-159..R-164 | MET-001..006 observability counters live | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0098/spec.md | M | Medium |
| D-0099 | T07.20 | R-165 | MIG-007b v3.9 GA tag creation gate | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0099/spec.md | M | Medium |
| D-CP07-MID-T01-T05 | T07.06 | R-140..R-144 | Mid-phase checkpoint report after T07.01-T07.05 | LIGHT | Quick sanity check | TASKLIST_ROOT/checkpoints/CP-P07-T01-T05.md | XS | Low |
| D-CP07-MID-T07-T11 | T07.12 | R-145..R-152 | Mid-phase checkpoint report after T07.07-T07.11 | LIGHT | Quick sanity check | TASKLIST_ROOT/checkpoints/CP-P07-T07-T11.md | XS | Low |
| D-CP07-MID-T13-T17 | T07.18 | R-153..R-158 | Mid-phase checkpoint report after T07.13-T07.17 | LIGHT | Quick sanity check | TASKLIST_ROOT/checkpoints/CP-P07-T13-T17.md | XS | Low |
| D-CP07 | T07.21 | R-140..R-165 | End-of-phase 7 / Release GA checkpoint report | LIGHT | Quick sanity check | TASKLIST_ROOT/checkpoints/CP-P07-END.md | XS | Low |

## Traceability Matrix

| Roadmap Item ID | Task ID(s) | Deliverable ID(s) | Tier | Confidence | Artifact Paths (rooted) |
|---:|---:|---:|---|---|---|
| R-001..R-006 | T01.01 | D-0001 | STRICT | 92% | TASKLIST_ROOT/artifacts/D-0001/ |
| R-007 | T01.02 | D-0002 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0002/ |
| R-008 | T01.03 | D-0003 | STANDARD | 85% | TASKLIST_ROOT/artifacts/D-0003/ |
| R-009 | T01.04 | D-0004 | STANDARD | 85% | TASKLIST_ROOT/artifacts/D-0004/ |
| R-010 | T01.05 | D-0005 | STANDARD | 85% | TASKLIST_ROOT/artifacts/D-0005/ |
| R-011 | T01.07 | D-0006 | STANDARD | 85% | TASKLIST_ROOT/artifacts/D-0006/ |
| R-012 | T01.08 | D-0007 | STANDARD | 85% | TASKLIST_ROOT/artifacts/D-0007/ |
| R-013 | T01.09 | D-0008 | STANDARD | 80% | TASKLIST_ROOT/artifacts/D-0008/ |
| R-014 | T01.10 | D-0009 | STANDARD | 85% | TASKLIST_ROOT/artifacts/D-0009/ |
| R-015 | T01.11 | D-0010 | STANDARD | 80% | TASKLIST_ROOT/artifacts/D-0010/ |
| R-016..R-020 | T01.13 | D-0011 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0011/ |
| R-021..R-024 | T01.14 | D-0012 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0012/ |
| R-025..R-027 | T01.15 | D-0013 | STANDARD | 90% | TASKLIST_ROOT/artifacts/D-0013/ |
| R-028 | T01.16 | D-0014 | STRICT | 92% | TASKLIST_ROOT/artifacts/D-0014/ |
| R-029..R-031 | T01.17 | D-0015 | STANDARD | 85% | TASKLIST_ROOT/artifacts/D-0015/ |
| R-032 | T02.01 | D-0016 | STANDARD | 90% | TASKLIST_ROOT/artifacts/D-0016/ |
| R-033..R-035 | T02.02 | D-0017 | STANDARD | 88% | TASKLIST_ROOT/artifacts/D-0017/ |
| R-036 | T02.03 | D-0018 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0018/ |
| R-037 | T02.04 | D-0019 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0019/ |
| R-038..R-039 | T02.05 | D-0020 | STANDARD | 85% | TASKLIST_ROOT/artifacts/D-0020/ |
| R-040..R-041 | T02.07 | D-0021 | STANDARD | 85% | TASKLIST_ROOT/artifacts/D-0021/ |
| R-042 | T02.08 | D-0022 | STANDARD | 85% | TASKLIST_ROOT/artifacts/D-0022/ |
| R-043..R-045 | T02.09 | D-0023 | STANDARD | 90% | TASKLIST_ROOT/artifacts/D-0023/ |
| R-046 | T02.10 | D-0024 | STANDARD | 85% | TASKLIST_ROOT/artifacts/D-0024/ |
| R-047..R-048 | T02.11 | D-0025 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0025/ |
| R-049 | T03.01 | D-0026 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0026/ |
| R-050..R-053 | T03.02 | D-0027 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0027/ |
| R-054 | T03.03 | D-0028 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0028/ |
| R-055, R-058 | T03.04 | D-0029 | STANDARD | 85% | TASKLIST_ROOT/artifacts/D-0029/ |
| R-056 | T03.05 | D-0030 | STANDARD | 85% | TASKLIST_ROOT/artifacts/D-0030/ |
| R-057 | T03.07 | D-0031 | STANDARD | 85% | TASKLIST_ROOT/artifacts/D-0031/ |
| R-059..R-060 | T03.08 | D-0032 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0032/ |
| R-061 | T03.09 | D-0033 | STANDARD | 85% | TASKLIST_ROOT/artifacts/D-0033/ |
| R-062 | T03.10 | D-0034 | STANDARD | 85% | TASKLIST_ROOT/artifacts/D-0034/ |
| R-063 | T03.11 | D-0035 | STANDARD | 90% | TASKLIST_ROOT/artifacts/D-0035/ |
| R-064 | T03.13 | D-0036 | STANDARD | 90% | TASKLIST_ROOT/artifacts/D-0036/ |
| R-065 | T03.14 | D-0037 | STANDARD | 90% | TASKLIST_ROOT/artifacts/D-0037/ |
| R-066 | T03.15 | D-0038 | STANDARD | 90% | TASKLIST_ROOT/artifacts/D-0038/ |
| R-067..R-068 | T03.16 | D-0039 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0039/ |
| R-069 | T03.17 | D-0040 | STANDARD | 80% | TASKLIST_ROOT/artifacts/D-0040/ |
| R-070 | T04.01 | D-0041 | STANDARD | 90% | TASKLIST_ROOT/artifacts/D-0041/ |
| R-071..R-072 | T04.02 | D-0042 | STANDARD | 88% | TASKLIST_ROOT/artifacts/D-0042/ |
| R-073..R-074 | T04.03 | D-0043 | STANDARD | 88% | TASKLIST_ROOT/artifacts/D-0043/ |
| R-075 | T04.04 | D-0044 | STANDARD | 90% | TASKLIST_ROOT/artifacts/D-0044/ |
| R-076..R-077 | T04.05 | D-0045 | STANDARD | 85% | TASKLIST_ROOT/artifacts/D-0045/ |
| R-078 | T04.07 | D-0046 | STANDARD | 90% | TASKLIST_ROOT/artifacts/D-0046/ |
| R-079 | T04.08 | D-0047 | STANDARD | 90% | TASKLIST_ROOT/artifacts/D-0047/ |
| R-080 | T04.09 | D-0048 | STANDARD | 90% | TASKLIST_ROOT/artifacts/D-0048/ |
| R-081 | T04.10 | D-0049 | STANDARD | 90% | TASKLIST_ROOT/artifacts/D-0049/ |
| R-082 | T04.11 | D-0050 | STANDARD | 85% | TASKLIST_ROOT/artifacts/D-0050/ |
| R-083 | T04.13 | D-0051 | STANDARD | 85% | TASKLIST_ROOT/artifacts/D-0051/ |
| R-084..R-087 | T04.14 | D-0052 | STANDARD | 90% | TASKLIST_ROOT/artifacts/D-0052/ |
| R-088..R-089 | T04.15 | D-0053 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0053/ |
| R-090 | T05.01 | D-0054 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0054/ |
| R-091 | T05.02 | D-0055 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0055/ |
| R-092 | T05.03 | D-0056 | STANDARD | 90% | TASKLIST_ROOT/artifacts/D-0056/ |
| R-093 | T05.04 | D-0057 | STANDARD | 90% | TASKLIST_ROOT/artifacts/D-0057/ |
| R-094..R-095 | T05.05 | D-0058 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0058/ |
| R-096 | T05.07 | D-0059 | STRICT | 88% | TASKLIST_ROOT/artifacts/D-0059/ |
| R-097..R-099 | T05.08 | D-0060 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0060/ |
| R-100..R-101 | T05.09 | D-0061 | STANDARD | 85% | TASKLIST_ROOT/artifacts/D-0061/ |
| R-102 | T05.10 | D-0062 | STANDARD | 85% | TASKLIST_ROOT/artifacts/D-0062/ |
| R-103 | T05.11 | D-0063 | STANDARD | 85% | TASKLIST_ROOT/artifacts/D-0063/ |
| R-104..R-105 | T05.13 | D-0064 | STANDARD | 90% | TASKLIST_ROOT/artifacts/D-0064/ |
| R-106..R-107 | T05.14 | D-0065 | STANDARD | 90% | TASKLIST_ROOT/artifacts/D-0065/ |
| R-108 | T05.15 | D-0066 | STANDARD | 88% | TASKLIST_ROOT/artifacts/D-0066/ |
| R-109..R-110 | T05.16 | D-0067 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0067/ |
| R-099 | T05.17 | D-0100 | STANDARD | 88% | TASKLIST_ROOT/artifacts/D-0100/ |
| R-111 | T06.01 | D-0068 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0068/ |
| R-112 | T06.02 | D-0069 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0069/ |
| R-113..R-114 | T06.03 | D-0070 | STANDARD | 90% | TASKLIST_ROOT/artifacts/D-0070/ |
| R-115..R-116 | T06.04 | D-0071 | STANDARD | 90% | TASKLIST_ROOT/artifacts/D-0071/ |
| R-117..R-119 | T06.05 | D-0072 | STANDARD | 88% | TASKLIST_ROOT/artifacts/D-0072/ |
| R-120..R-121 | T06.07 | D-0073 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0073/ |
| R-122 | T06.08 | D-0074 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0074/ |
| R-123..R-124 | T06.09 | D-0075 | STANDARD | 88% | TASKLIST_ROOT/artifacts/D-0075/ |
| R-125..R-126 | T06.10 | D-0076 | STRICT | 88% | TASKLIST_ROOT/artifacts/D-0076/ |
| R-127..R-128 | T06.11 | D-0077 | STANDARD | 85% | TASKLIST_ROOT/artifacts/D-0077/ |
| R-129..R-130 | T06.13 | D-0078 | STANDARD | 85% | TASKLIST_ROOT/artifacts/D-0078/ |
| R-131..R-132 | T06.14 | D-0079 | STANDARD | 85% | TASKLIST_ROOT/artifacts/D-0079/ |
| R-133..R-134 | T06.15 | D-0080 | STANDARD | 90% | TASKLIST_ROOT/artifacts/D-0080/ |
| R-135..R-136 | T06.16 | D-0081 | STANDARD | 90% | TASKLIST_ROOT/artifacts/D-0081/ |
| R-137..R-139 | T06.17 | D-0082 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0082/ |
| R-140 | T07.01 | D-0083 | STANDARD | 85% | TASKLIST_ROOT/artifacts/D-0083/ |
| R-141 | T07.02 | D-0084 | STANDARD | 85% | TASKLIST_ROOT/artifacts/D-0084/ |
| R-142 | T07.03 | D-0085 | STANDARD | 90% | TASKLIST_ROOT/artifacts/D-0085/ |
| R-143 | T07.04 | D-0086 | STANDARD | 90% | TASKLIST_ROOT/artifacts/D-0086/ |
| R-144 | T07.05 | D-0087 | STANDARD | 90% | TASKLIST_ROOT/artifacts/D-0087/ |
| R-145..R-146 | T07.07 | D-0088 | STRICT | 88% | TASKLIST_ROOT/artifacts/D-0088/ |
| R-147..R-149 | T07.08 | D-0089 | STANDARD | 85% | TASKLIST_ROOT/artifacts/D-0089/ |
| R-150 | T07.09 | D-0090 | STANDARD | 88% | TASKLIST_ROOT/artifacts/D-0090/ |
| R-151 | T07.10 | D-0091 | STANDARD | 90% | TASKLIST_ROOT/artifacts/D-0091/ |
| R-152 | T07.11 | D-0092 | STANDARD | 90% | TASKLIST_ROOT/artifacts/D-0092/ |
| R-153 | T07.13 | D-0093 | STANDARD | 90% | TASKLIST_ROOT/artifacts/D-0093/ |
| R-154 | T07.14 | D-0094 | STANDARD | 90% | TASKLIST_ROOT/artifacts/D-0094/ |
| R-155 | T07.15 | D-0095 | STANDARD | 90% | TASKLIST_ROOT/artifacts/D-0095/ |
| R-156 | T07.16 | D-0096 | STANDARD | 90% | TASKLIST_ROOT/artifacts/D-0096/ |
| R-157..R-158 | T07.17 | D-0097 | STANDARD | 90% | TASKLIST_ROOT/artifacts/D-0097/ |
| R-159..R-164 | T07.19 | D-0098 | STANDARD | 85% | TASKLIST_ROOT/artifacts/D-0098/ |
| R-165 | T07.20 | D-0099 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0099/ |

## Execution Log Template

**Intended Path:** `TASKLIST_ROOT/execution-log.md`

| Timestamp (ISO 8601) | Task ID | Tier | Deliverable ID(s) | Action Taken (<= 12 words) | Validation Run (verbatim cmd or "Manual") | Result (Pass/Fail/TBD) | Evidence Path |
|---|---:|---|---:|---|---|---|---|

## Checkpoint Report Template

- `# Checkpoint Report -- <Checkpoint Title>`
- `**Checkpoint Report Path:** TASKLIST_ROOT/checkpoints/<deterministic-name>.md`
- `**Scope:** <tasks covered>`
- `## Status` — `Overall: Pass | Fail | TBD`
- `## Verification Results` (exactly 3 bullets; align to checkpoint Verification bullets)
- `## Exit Criteria Assessment` (exactly 3 bullets; align to checkpoint Exit Criteria bullets)
- `## Issues & Follow-ups` — list blocking issues; reference `T<PP>.<TT>` and `D-####`
- `## Evidence` — bullet list of intended evidence paths under `TASKLIST_ROOT/evidence/`

## Feedback Collection Template

**Intended Path:** `TASKLIST_ROOT/feedback-log.md`

| Task ID | Original Tier | Override Tier | Override Reason (<= 15 words) | Completion Status | Quality Signal | Time Variance |
|---:|---|---|---|---|---|---|

## Generation Notes

- Roadmap items consolidated where related rows shared a single FR/contract scope (e.g., DM-001..005 freeze in one task) to satisfy the structural gate `<=25 tasks/phase`. Each consolidated task preserves explicit `R-###` references in its Roadmap Item IDs metadata field.
- Q-DM-1 (PRD §25.4 vs SKILL.md:1450-1460 per-item schema contradiction) surfaced as a Clarification Task placeholder before T01.09 (TB-Add-6) where format enforcement depends on the resolved schema; gate confidence is therefore at 80% for that task pending Engineering Lead decision.
- Effort/Risk computed deterministically; no story points, owners, or absolute dates introduced beyond what the roadmap states verbatim (the M1..M7 calendar dates are preserved as-is in phase Goal sentences).
