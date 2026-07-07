# Phase 1 Completeness QA Report

**Task:** `/config/workspace/IronClaude/.dev/worktrees/ReflectModelFallback/.dev/tasks/to-do/TASK-RF-t2-fallback-ladder-20260706-050832/TASK-RF-t2-fallback-ladder-20260706-050832.md`  
**Aggregation file:** `/config/workspace/IronClaude/.dev/worktrees/ReflectModelFallback/.dev/tasks/to-do/TASK-RF-t2-fallback-ladder-20260706-050832/phase-outputs/reports/phase1-output-summary.md`  
**Design checked:** `/config/workspace/IronClaude/.dev/worktrees/ReflectModelFallback/.dev/brainstorms/20260706-035624-reflect-t2-fallback-ladder/design.md`  
**Date:** 2026-07-06

## Verdict: FAIL

Phase 1 has the core pure helpers, data types, diversity extraction, and the four named unit test files. However, completeness against design §4/§9 is not sufficient. I found 6 issues: 1 CRITICAL, 4 IMPORTANT, 1 MINOR.

## Verification Summary

| Check | Verdict | Evidence |
|---|---:|---|
| Every required §4 pure helper exists | PASS | `classify_outcomes` at `fallback.py:56`, `evaluate_quorum` at `fallback.py:65`, `plan_next_attempt` at `fallback.py:86`, `select_contributing_set` at `fallback.py:133`, `make_fallback_slot_factory` at `fallback.py:167`. |
| §4.1 data types match | PASS | `FallbackDecision`, `QuorumState`, and `LadderOutcome` are present at `fallback.py:23-49` with matching fields and broad compatible types. |
| Diversity helpers moved to `_diversity.py` | PASS | `_diversity.py` contains `compute_model_class_diversity`, `compute_vendor_diversity`, and `_vendor_from_model_id` at `_diversity.py:8-55`. `fallback.py` imports from `_diversity.py` at `fallback.py:17`; `ensemble.py` re-exports/imports them at `ensemble.py:60-64`. |
| Diversity helpers not duplicated in `ensemble.py` | PASS | `ensemble.py` imports them from `_diversity.py` rather than defining them locally at `ensemble.py:60-64`. |
| Four Phase 1 unit test files exist | PASS | All four requested test files were read successfully. |
| Each test file fully covers its §9 row, including F1/F4 | FAIL | Several §9 row requirements are only partially covered; see findings below. |

## Findings

### Finding 1: `run_fallback_ladder` §4.3 surface is missing

- **Severity:** CRITICAL
- **Affected file:** `/config/workspace/IronClaude/.dev/worktrees/ReflectModelFallback/src/superclaude/cli/reflect/fallback.py`
- **Evidence:** Design §4 defines `reflect/fallback.py` as containing pure helpers plus the one impure function `run_fallback_ladder` in §4.3. The implementation currently ends after `make_fallback_slot_factory` at `fallback.py:167-188`; no `run_fallback_ladder` signature or stub is present.
- **Why this matters:** The Step 1.G2 prompt says to verify “§4 fallback.py surface.” The pure helper subset exists, but the full §4 module surface does not. If Phase 1 intentionally excludes the impure controller, the phase summary should explicitly carve that out; otherwise this is a design-surface miss.
- **Required fix:** Either implement the §4.3 `run_fallback_ladder` surface or update the Phase 1 acceptance/aggregation language to state that §4.3 is deferred and not part of Phase 1.

### Finding 2: `test_fallback_plan.py` does not cover every §9 “Transition Rules” branch

- **Severity:** IMPORTANT
- **Affected file:** `/config/workspace/IronClaude/.dev/worktrees/ReflectModelFallback/tests/cli/reflect/test_fallback_plan.py`
- **Evidence:** Design §9 says the plan tests pin “every §Transition Rules branch.” The implementation has untested branches in `plan_next_attempt`: `diversity_unrepairable` at `fallback.py:109-115` and `no_fallback_eligible_primary_failure` at `fallback.py:116-118`. The current plan tests cover certified, first dispatch, second dispatch, diversity-short escalation, wall-clock exhaustion, missing first slot, and full ladder exhaustion at `test_fallback_plan.py:23-158`, but do not assert those two terminal branches.
- **Why this matters:** These terminal reasons are part of the design’s degraded telemetry contract. A regression could change or remove them without Phase 1 tests failing.
- **Required fix:** Add tests for:
  - no eligible failures + `reviewer_count >= 2` + diversity not full/multi → `diversity_unrepairable`;
  - no eligible failures + quorum short → `no_fallback_eligible_primary_failure`.

### Finding 3: F1 is not tested end-to-end for “second fallback attempt resolves `T1Model02` → `pool[1]`”

- **Severity:** IMPORTANT
- **Affected files:**
  - `/config/workspace/IronClaude/.dev/worktrees/ReflectModelFallback/tests/cli/reflect/test_fallback_plan.py`
  - `/config/workspace/IronClaude/.dev/worktrees/ReflectModelFallback/tests/cli/reflect/test_fallback_slot_factory.py`
- **Evidence:** The plan test asserts the second attempt chooses slot `"T1Model02"` at `test_fallback_plan.py:81-92`. The slot-factory test separately asserts `"T1Model02"` maps to `"m-b"`/pool index 1 at `test_fallback_slot_factory.py:18-36`. But design §9’s plan row explicitly requires **F1: second fallback attempt resolves `T1Model02`→`pool[1]`, not `pool[0]` twice**. No single test exercises the second-attempt decision together with the slot-name factory resolution.
- **Why this matters:** The original F1 risk is an integration risk: one-worker dispatch can repeatedly resolve local `slot_index == 0`. Separate “planner chooses T1Model02” and “factory maps T1Model02” tests do not prove the second-attempt path actually uses the slot-name factory correctly.
- **Required fix:** Add a test that drives the second-attempt planner decision into `make_fallback_slot_factory` and asserts the resulting transport/model is `pool[1]`, not `pool[0]`.

### Finding 4: `evaluate_quorum` exists but has no direct unit coverage

- **Severity:** IMPORTANT
- **Affected files:**
  - `/config/workspace/IronClaude/.dev/worktrees/ReflectModelFallback/src/superclaude/cli/reflect/fallback.py`
  - `/config/workspace/IronClaude/.dev/worktrees/ReflectModelFallback/tests/cli/reflect/test_fallback_select.py`
- **Evidence:** `evaluate_quorum` is a required §4 pure helper at `fallback.py:65-83`. None of the four Phase 1 test files imports or directly asserts it. The existing tests indirectly exercise it through `select_contributing_set` at `test_fallback_select.py:11-75`.
- **Why this matters:** `evaluate_quorum` is the pure predicate bridge to the Tier-2 verdict gate: reviewer count, model-class diversity, vendor diversity, and `allow_single_vendor`. Indirect coverage through selection tests is weaker than the design’s stated emphasis on pure helper testability.
- **Required fix:** Add direct assertions for:
  - one success → `reviewer_count == 1`, `satisfies_tier2 == False`;
  - two distinct model IDs / distinct vendors → `satisfies_tier2 == True`;
  - same-vendor distinct models with `allow_single_vendor=False` → false;
  - same-vendor distinct models with `allow_single_vendor=True` → true;
  - same model ID → `model_class_diversity == "insufficient"`.

### Finding 5: Missing coverage for second-slot config/pool failure path

- **Severity:** IMPORTANT
- **Affected files:**
  - `/config/workspace/IronClaude/.dev/worktrees/ReflectModelFallback/src/superclaude/cli/reflect/fallback.py`
  - `/config/workspace/IronClaude/.dev/worktrees/ReflectModelFallback/tests/cli/reflect/test_fallback_plan.py`
  - `/config/workspace/IronClaude/.dev/worktrees/ReflectModelFallback/tests/cli/reflect/test_fallback_slot_factory.py`
- **Evidence:** `plan_next_attempt` maps an unavailable selected slot to `fallback_config_missing` at `fallback.py:125-128`. The current plan test only checks missing first slot at `test_fallback_plan.py:131-143`. The slot-factory test separately checks pool-too-small for `"T1Model02"` at `test_fallback_slot_factory.py:39-47`. There is no test for the planner choosing `"T1Model02"` after `"T1Model01"` and then reporting `fallback_config_missing` when the second slot is unavailable.
- **Why this matters:** The F1/F4 incident path depends on the second fallback slot being real and correctly handled. A bug in the T1Model02 unavailable path would not be caught.
- **Required fix:** Add a plan test with `attempts_made=["T1Model01"]`, `fallback_available={"T1Model01": True, "T1Model02": False}`, and assert `action == "degraded"`, `slot == "T1Model02"`, `reason == "fallback_config_missing"`.

### Finding 6: `_vendor_from_model_id` move/re-export has no explicit regression test

- **Severity:** MINOR
- **Affected files:**
  - `/config/workspace/IronClaude/.dev/worktrees/ReflectModelFallback/src/superclaude/cli/reflect/_diversity.py`
  - `/config/workspace/IronClaude/.dev/worktrees/ReflectModelFallback/src/superclaude/cli/reflect/ensemble.py`
- **Evidence:** `_vendor_from_model_id` exists in `_diversity.py` at `_diversity.py:39-55` and is re-exported/imported by `ensemble.py` at `ensemble.py:60-64`. No Phase 1 test asserts the moved helper remains available through the prior `ensemble.py` import surface.
- **Why this matters:** The prompt specifically asks to verify the diversity helpers were moved “with `_vendor_from_model_id`.” The code satisfies this now, but the compatibility surface is not pinned by a test.
- **Required fix:** Add a small regression assertion that imports `_vendor_from_model_id` from the expected public/backcompat path, or document that the helper is private and only `_diversity.py` direct import is supported.

## Passed Checks Worth Preserving

- `classify_outcomes` correctly splits successes and fallback-eligible terminal statuses; tests cover `success`, `timeout`, `proxy_error`, `parse_error`, and salvaged parse-error-as-success at `test_fallback_classify.py:23-66`.
- `make_fallback_slot_factory` correctly binds slot name to ladder position, proving the core F1 factory behavior at `test_fallback_slot_factory.py:18-36`.
- F4 pure planner behavior is covered: wall-clock exhaustion stops before dispatch at `test_fallback_plan.py:116-128`.
- The circular-import guard from design §10 is satisfied for the diversity-helper cycle: `fallback.py` imports diversity from `_diversity.py`, and `ensemble.py` imports/re-exports from `_diversity.py`; there is no `fallback.py -> ensemble.py` diversity import.

## Recommendation

Do not accept Phase 1 as complete until the test coverage gaps are closed or explicitly carved out in the Phase 1 acceptance notes. Minimum remediation should add direct tests for the missing `plan_next_attempt` terminal branches, direct `evaluate_quorum` coverage, and an F1 second-attempt-to-pool[1] assertion that combines planner output with slot-name factory resolution.
