# sc:reflect UC-2 Validation — R0 Bridge Closure Audit

**Mode:** UC-2 (post-execution deviation audit) | **Diff:** `91095144..bdfad6d3` (4 commits, 29 files, +2107/-16 LOC) | **Tasklist:** TASK-RF-20260531-042405 (42 items) | **Spec:** BUILD-REQUEST-roadmap-pipeline-rewrite.md §R0

## Executive Summary

**Verdict: R0 close-with-caveats.** R0 deliverables (R0.1 Spec-ID registry + R0.2 anti-instinct allowlist + R0.3 contracts SoT + CI gates) are present, working, and verified end-to-end via independent empirical probes. **However, 9 NEW test failures introduced by the R0 bridge were missed by all 5 inline phase rf-qa runs** — 1 Drift + 1 Regression class spanning 8 pipeline-integration tests. These contradict BUILD-REQUEST Acceptance Gate #2. Mechanically fixable in ≤1 eng-hour via "R0.4 / M9 test-fixture sidecar registration" follow-up.

**Tier reached:** T1 with §5.3 rule 3 escalation noted (regression candidate). T2 parallel-reviewer fan-out NOT executed (single-agent invocation); sufficiency claim per §11.0 is CONDITIONAL on the empirical falsifiers (synthetic-violator probe + parent-vs-head pytest diff) substituting for the heterogeneous-ensemble mechanism.

**Counts:** CRITICAL=0, HIGH=2 (1 Drift + 1 Regression), MEDIUM=0, Necessary=3 (informational).

## Tier-Decision Recording

Rule fired: §5.3 **Rule 3** — UC-2 AND ≥1 hunk classified as Regression candidate → ESCALATE. Composite score 6.5/10. Signals: `S_scope=29`, `S_domains=1`, `S_dev_density=0.024`, `coverage_pct=0.976`, `regression_candidate_count=1`, `C_calibrated=0.87`.

## Coverage Map (5 phases × 42 items)

| Phase | Declared | Diff Evidence | Status |
|-------|----------|---------------|--------|
| Phase 1 Discovery | 4 | 4 | complete |
| Phase 2 R0.1 | 11 | 11 | complete |
| Phase 3 R0.2 | 11 | 11 | complete (incl. M8 fix) |
| Phase 4 R0.3 | 10 | 10 | complete (+ 2 logged Necessary deviations) |
| Phase 5 Acceptance | 6 | 5 | complete (+ 1 Necessary escape: missing `audit` CLI) |
| **Total** | **42** | **41** | **97.6% mapped, 0 unmapped diff hunks at phase level** |

## Deviation Taxonomy

| Class | Count | Items |
|-------|-------|-------|
| Authorized | 0 | — |
| Necessary | 3 | G + NFR broadening; missing `audit` CLI escape; anchor-free pattern bodies |
| **Drift** | **1 HIGH** | **D-DRIFT-01** below |
| **Regression** | **1 HIGH (class of 8 tests)** | **D-REGRESSION-01** below |

### D-DRIFT-01 (HIGH)

`tests/roadmap/test_gates_data.py:111` asserts `MERGE_GATE.semantic_checks == 7`; R0.1 added 8th (`_roadmap_ids_within_spec`); test now fails `assert 8 == 7`. **No tasklist item, commit body, or inline comment** references updating this assertion. PASSES parent 91095144, FAILS head bdfad6d3.

### D-REGRESSION-01 (HIGH, class of 8)

8 pipeline-integration tests pass on parent, FAIL on head:
- `test_executor.py::test_full_pipeline_all_pass`
- `test_pipeline_integration.py::test_e2e_steps_1_through_9_complete`
- `test_pipeline_integration.py::test_e2e_state_with_all_12_steps`
- `test_integration_v5_pipeline.py::test_pipeline_reaches_certify`
- `test_integration_v5_pipeline.py::test_remediate_step_is_last`
- `test_integration_v5_pipeline.py::test_no_step_fails`
- `test_integration_v5_pipeline.py::test_full_pipeline_sc1_through_sc6`
- `test_eval_gate_rejection.py::test_passing_fixture_passes[merge-gate6]`

**Root cause:** MERGE_GATE's new `_roadmap_ids_within_spec` check fails-shut when sidecar is not registered (returns truthy failure string); mock-subprocess test fixtures don't call `set_id_registry_sidecar_path` before exercising the gate.

**Contradicts BUILD-REQUEST Acceptance Gate #2** ("All current passing tests in `tests/roadmap/` still pass").

## Evidence-Validator Results

All 18 cited file:line refs re-Read against current head. **Citations dropped: 0. Citations [INFERRED]: 0.**

Empirical probes that established the findings:

1. **arch_lint end-to-end:** synthetic-violator probe → 2 violations flagged, exit 1. `make lint-architecture` Check 11 at Makefile:464-473; `make lint: lint-architecture` at Makefile:48 — **pipeline-blocking posture confirmed**.
2. **MERGE_GATE fail-shut probe:** `_roadmap_ids_within_spec("FR-001 ...")` without sidecar returns truthy failure string. Confirms fail-shut at Phase 2 acceptance — and is **the proximate cause of D-REGRESSION-01**.
3. **Parent-vs-head test diff:** `pytest tests/ --tb=no --ignore=tests/sprint` at parent 91095144: 29 failed. At head bdfad6d3: 38 failed. **Net +9 NEW failures**, none in any inline rf-qa verdict.
4. **MultiModelSwarm rescan honesty check:** Phase 5 Step 5.2 really re-ran the scan (didn't cheat by re-reading existing artifact). HIGH-undischarged=0, fingerprint_coverage=1.00.

## PRESERVE-Target Audit

`commands.py`, `structural_checkers.py`, `convergence.py`, `cosmetic_remediator.py` — none appear in any of the 4 commits' `git show --stat`. **PRESERVE invariant honored byte-identically.**

## Anti-Bias Notes — Divergences from the 5 Inline rf-qa Runs

All 5 inline phase rf-qa verdicts returned PASS. This UC-2 surfaces 2 HIGH findings they missed. **Structural reason:** same-agent same-context inline review cannot independently probe parent-vs-head test state. Every inline rf-qa ran AFTER its commit was already in place, with access only to current-head Python imports. None ran `git checkout 91095144 -- ; pytest`.

**The R0 Acceptance Report's "12 pre-existing test failures" claim is INCORRECT.** Inspection: 3 are genuinely pre-existing roadmap failures. 8-9 of the "12" appear **MISATTRIBUTED** — they are the test_pipeline_integration / test_integration_v5_pipeline / test_eval_gate_rejection failures **INTRODUCED by R0.1's MERGE_GATE addition**. This misattribution is exactly the failure mode UC-2 exists to catch.

## Contract Items CI-Gated Assessment

| Contract | Gate Type | Mechanism | Status |
|----------|-----------|-----------|--------|
| **#5** (arch-lint anti-duplication) | Pipeline-blocking | `make lint-architecture` Check 11 + `make lint` dep | ✅ CONFIRMED via synthetic-violator probe |
| **#8** (Threshold registry) | PR-blocking | `tests/roadmap/test_threshold_registry.py` (12 tests) | ✅ CONFIRMED |
| **#9** (Spec↔Roadmap ID containment) | Pipeline-blocking via MERGE_GATE | `_roadmap_ids_within_spec` SemanticCheck (gates.py:1327, fail-shut on missing sidecar) | ✅ CONFIRMED — but ⚠ proximate cause of D-REGRESSION-01 |
| **#10** (Adversarial FP corpus) | PR-blocking | `tests/roadmap/test_anti_instinct_recurrence.py` (8 tests post-M8) | ✅ CONFIRMED |

## Inline-rf-qa Effectiveness Review

What the 5 inline rf-qa verdicts collectively missed:

1. **Cross-phase test-state delta.** Each verified its own targeted tests pass; none ran full suite parent-vs-head. → 8-test regression unnoticed.
2. **Downstream-assertion lag.** Adding the 8th semantic_check to MERGE_GATE didn't trigger inspection of `find_referencing_symbols(MERGE_GATE.semantic_checks)`. Inline rf-qa pattern-matches tasklist items, not symbol-impact graphs.
3. **R0 acceptance report misattribution accepted on face value.** Inline rf-qa did not independently re-run parent vs head.

The Phase 3 M8 finding was prior evidence that inline rf-qa misses structural classes. This UC-2 surfaces a second class: **test-suite regression introduced by SemanticCheck additions to shared gate objects.** Inline checklist should add: "When modifying shared gate objects, run pytest at parent and head; failure-count delta MUST be 0."

## Recommendation

**R0 close-with-caveats.** Land "R0.4 / M9 test-fixture sidecar registration":

1. Update `tests/roadmap/test_gates_data.py:111`: `== 7` → `== 8`. Inline comment citing Contract #9 / R0.1.
2. Update 8 affected fixtures to call `gates.set_id_registry_sidecar_path(<test-sidecar>)` before exercising MERGE_GATE. Write minimal sidecar JSON with spec_ids matching fixture roadmap_ids.
3. Re-run `uv run pytest tests/ --tb=no --ignore=tests/sprint` from clean checkout: failures must drop 38 → 29 (matching parent baseline).
4. Add to inline rf-qa template: "If shared gate objects modified, run full pytest at parent and head; failure delta MUST be 0."

Estimated effort: ≤ 1 eng-hour. Not blocking R1 architectural planning.

## Return Contract

```yaml
verdict: close-with-caveats
calibrated_confidence: 0.87
tier_reached: 1
rule_fired: 3
citations_total: 18
citations_dropped: 0
deviation_counts:
  authorized: 0
  necessary: 3
  drift: 1
  regression: 1
critical_count: 0
high_count: 2
medium_count: 0
recommendation: close-with-caveats — land R0.4 sidecar-registration follow-up before declaring R0 closed
```
