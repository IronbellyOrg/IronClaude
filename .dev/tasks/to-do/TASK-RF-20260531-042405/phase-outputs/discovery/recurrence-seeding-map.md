# Recurrence Corpus Seeding Map (Step 13.1)

**Date:** 2026-06-03
**Source:** `master-report.md` §Recurrence Matrix (lines 402–429) + §Top-3 drivers (431–437) + §Pipeline-step Heat Map (438–456)
**Acceptance Gate #4 (BUILD-REQUEST):** ≥1 fixture per RECURRENT row — rows #1, 2, 4, 5, 6, 7, 8, 9, 10, 12, 14, 15, 16, 17, 19, 20, 21, 22 (18 rows).
**Corpus root:** `tests/roadmap/fixtures/recurrence/`

## On-disk verification of "Already created? = Y" claims (physically checked via `find`)

| Class dir | Fixtures present (verified on disk) | Covers row |
|-----------|--------------------------------------|------------|
| `anti_instinct/` | `imperative_verb_with_allowlist_phrase_case`, `module_path_fp_case`, `multimodelswarm_fp_case`, `stub_worker_parallelism_fp_case`, `valid_obligation_case` (5 pairs) | **#6** |
| `id_containment/` | `milestone_id_case`, `spec_roadmap_drift_case` (2 pairs) | **#4** |
| `retry_contract/` | `retry_loop_no_terminal_case` (1 pair) | **#9** |

Confirmed: exactly 3 rows (#4, #6, #9) already have fixtures — matching the task's expectation (row #4 from R0.1 Step 2.5, row #6 from R0.2 Step 3.4, row #9 from R1.6 Step 11.6). Row #9's `retry_loop_no_terminal_case` IS on disk at Phase-13 entry (R1.6 ran).

## Full seeding map (18 RECURRENT rows)

Columns: `Recurrence row #` | `Failure class` | `Source citation` | `Fixture filename (.md + .expected.json)` | `Already created?`

| Row # | Failure (short) | Failure class | Source citation | Fixture filename | Already? |
|-------|-----------------|---------------|-----------------|------------------|----------|
| 1 | Spec-fidelity LLM-only / phantom-ID gate | `spec_fidelity` | master:§Recurrence #1; A4:F-A4-005, A12:F-A12-01 | `phantom_id_high_severity_case` | N |
| 2 | Gate/step "written but not wired" | `dispatch_reachability` | master:§Recurrence #2 / §Top-3 #2; A10:F-A10-019, A11:F-A11-011 | `unwired_certify_step_case` | N |
| 4 | Roadmap fabricates/renumbers FR/NFR/SC/D IDs | `id_containment` | master:§Recurrence #4 / §Top-3 #3; A1b:F-A1b-004, A12:F-A12-01 | `spec_roadmap_drift_case`, `milestone_id_case` | **Y** |
| 5 | Phase restructure / module-layout deviation | `spec_fidelity` | master:§Recurrence #5; A1b:F-A1b-004, A7:F-A7-04 | `phase_restructure_deviation_case` | N (stub — see Deferral notes) |
| 6 | Anti-instinct false-positive on legit vocab | `anti_instinct` | master:§Recurrence #6; A2a:F-A2a-003, A11:F-A11-001 | (5 existing pairs) | **Y** |
| 7 | Convergence-threshold drift / advisory-not-enforcing | `threshold_registry` | master:§Recurrence #7; A1b:F-A1b-002, A10:F-A10-003 | `convergence_threshold_drift_case` | N |
| 8 | `_cross_refs_resolve` always-True stub | `fragility_stub` | master:§Recurrence #8; A9:F-A9-005, A11:F-A11-031 | `cross_refs_resolve_stub_case` | N |
| 9 | Retry without input mutation | `retry_contract` | master:§Recurrence #9; A1b:F-A1b-006, A12:F-A12-02 | `retry_loop_no_terminal_case` | **Y** |
| 10 | Generator/validator asymmetry (meta-pattern) | `(meta — no single scanner input)` | master:§Recurrence #10; A1b:F-A1b-005, A12:F-A12-03 | `generator_validator_asymmetry_case` (DEFER stub) | N (DEFER) |
| 12 | Validation declared PASS while impl incomplete | `verification` | master:§Recurrence #12; A2b:F-A2b-004, A4:F-A4-022 | `validation_complete_false_ships_case` | N (DEFER candidate → see notes) |
| 14 | Verification/certify silently skipped | `dispatch_reachability` | master:§Recurrence #14; A2b:F-A2b-003, A11:F-A11-011 | `skipped_verification_step_case` | N |
| 15 | Adversarial findings dropped silently at merge | `merge_completeness` | master:§Recurrence #15; A8:F-A8-005, A9:F-A9-011 | `merge_dropped_findings_case` | N |
| 16 | Telemetry/text-regex vs structured stream-json | `telemetry` | master:§Recurrence #16; A6:F-A6-001..004 | `telemetry_text_regex_case` (DEFER stub) | N (DEFER) |
| 17 | Context-window/OOM / max-turns collapse | `(runtime resource)` | master:§Recurrence #17; A1a:F-A1a-009, A6:F-A6-006 | `context_window_oom_case` (DEFER stub) | N (DEFER — hard) |
| 19 | Spec-fidelity classifier UNCLASSIFIED/hex/FP | `spec_fidelity` | master:§Recurrence #19; A6:F-A6-008, A10:F-A10-010 | `deviation_unclassified_case` | N |
| 20 | One-shot stdout / 64k cap / no truncation detection | `telemetry` | master:§Recurrence #20; A11:F-A11-005, A12:F-A12-12 | `truncation_no_detection_case` (DEFER stub) | N (DEFER) |
| 21 | Sprint executor ignores deps / vacuous gates | `(sprint — out of scope)` | master:§Recurrence #21; A11:F-A11-023, A12:F-A12-13 | `sprint_executor_vacuous_gate_case` (DEFER stub) | N (DEFER — out of scope) |
| 22 | "Silent skip on uncertainty" / fail-open institutionalised | `fragility_stub` | master:§Recurrence #22; A2a:F-A2a-008, A9:F-A9-002 | `fail_open_ambiguous_found_case` | N (DEFER candidate → see notes) |

**New failure-class subdirectories required beyond the 3 on-disk** (`anti_instinct`, `id_containment`, `retry_contract`): `spec_fidelity/`, `dispatch_reachability/`, `threshold_registry/`, `fragility_stub/`, `verification/`, `merge_completeness/`, `telemetry/`, plus a `deferred/` area for non-scanner-testable runtime/scope rows (`runtime_resource`, `sprint`, `meta`).

## Deferral / scope-tension classification (per Step 13.1 (b))

Rows where a genuine scanner-input fixture is NOT constructible — each receives a **documented STUB** (`{"deferred": true, "reason": "..."}`) + skip-registry entry in Step 13.2/13.3, NOT a silent drop:

| Row # | Deferral kind | Reason |
|-------|---------------|--------|
| **#17** | hard DEFER (runtime resource) | Context-window/OOM/max-turns is a runtime-resource failure (exit -9, "Prompt is too long"), not a scanner-input-testable shape. No deterministic component consumes a fixture to reproduce it. |
| **#21** | hard DEFER (out of scope) | Sprint executor is explicitly OUT of scope per BUILD-REQUEST §Scope. §Scope tension recorded: the roadmap-pipeline rewrite does not touch `sprint/executor.py`; this row is a sprint-layer recurrence outside R0/R1 boundaries. |
| **#10** | DEFER (meta-pattern) | Generator/validator asymmetry is the *architectural* meta-driver (every fix adds a downstream validator, none constrain the generator). It is not a single scanner input; R1.4 tool-write generator-side constraints address it structurally, attested in R1.4 Findings, not via a fixture. |
| **#12** | DEFER candidate → REALIZED as real fixture | "Validation PASS while incomplete" IS now scanner-testable post-R1.6: the `SPEC_FIDELITY_GATE_CONVERGENCE_AWARE` `_spec_fidelity_validation_complete_true` check rejects a `validation_complete:false` report. Promoted from DEFER to a real `verification`-class fixture (`validation_complete_false_ships_case`). |
| **#16** | DEFER (telemetry/sprint-adjacent) | Telemetry text-regex-vs-stream-json is a sprint/eval-harness concern (A6 cross-cuts), not a roadmap pipeline scanner. STUB. |
| **#20** | DEFER (telemetry/truncation) | One-shot stdout/64k truncation is a transport/harness concern; R1.4 tool-write mitigates structurally but there is no roadmap-scanner fixture input. STUB. |
| **#22** | DEFER candidate → REALIZED as real fixture | "Fail-open ambiguous=found / silent-skip" IS now scanner-testable: R1.6 made gates fail-closed and `test_no_fragility_stubs.py` enforces zero `return True` stubs. Promoted to a real `fragility_stub`-class fixture (`fail_open_ambiguous_found_case`). |

**Net Step 13.2 work:** real fixtures for rows #1, #2, #5(thin), #7, #8, #12, #14, #15, #19, #22 (10 real pairs); documented DEFER stubs for #10, #16, #17, #20, #21 (5 stub pairs). Rows #4, #6, #9 already on disk. Total corpus coverage = 18/18 RECURRENT rows (every row has a fixture pair, real or auditable-stub).

## Provenance guarantee

Every fixture's `.md` content derives verbatim from the cited master/partition incident — no fabricated cases. DEFER stubs carry `{"deferred": true, "reason": "<citation + why not scanner-testable>"}` and a corresponding `xfail`/`skip` registry entry (Step 13.3) so Gate #4's per-row count is honored and each deferral is auditable.
