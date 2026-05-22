---
title: "Phase 2 — Failing Task-Builder Tests Summary (Adjudication + Fix Plan)"
captured: "2026-05-18"
captured_from: "phase-2-failing-tests-before.txt (pytest --tb=short output)"
adjudication: "Update test expectations to match SKILL.md / rf-task-builder.md final text (BUILD_REQUEST direction)"
---

# Phase 2 — Failing Task-Builder Tests Summary

All 3 tests confirmed FAILING at task-execution time on `feat/hook-sync-and-matcher-fix` HEAD.

Adjudication direction per BUILD_REQUEST: **the SKILL.md (and rf-task-builder.md) final state is authoritative** — Phases 6/7 of `task-builder-merge` succeeded and produced the canonical text. Therefore each fix updates the test's expected-literal string to match the present source text, NEVER the other way around. Source files (`SKILL.md`, `rf-task-builder.md`) are NOT modified.

## Test 1 — `TestPR01ExecutionContextHeader.test_execution_context_uses_source_areas_not_paths`

| Field | Value |
|------|------|
| File | `tests/skills/test_task_builder_merge.py` |
| Assertion line | **165** |
| Failing assertion | `assert "NEVER write specific" in skill_text` |
| Passing assertion | (line 166) `assert "path.py:NN" in skill_text` — PASSES (3 occurrences) |
| Current literal expected | `"NEVER write specific"` |
| Current SKILL.md substring options | L1140: `"NO specific file:line references"` (in TB-Add-7 check text); L953: `"no specific file paths"` (in DM-001 emitters); L1856: HTML-comment block "contains NO specific path.py:NN references" |
| **Chosen replacement** | `"NO specific file:line references"` (L1140 TB-Add-7 — semantically aligned with the test name `uses_source_areas_not_paths`) |

**Fix operation:** In `tests/skills/test_task_builder_merge.py` line 165, replace `"NEVER write specific"` → `"NO specific file:line references"`.

## Test 2 — `TestPR02RetryMonotonicityGuards.test_skill_regression_detection_precedence`

| Field | Value |
|------|------|
| File | `tests/skills/test_task_builder_merge.py` |
| Assertion lines | **378-387** (two OR-form assertions) |
| First assertion (L379-382) | `"regression detected" in skill_text.lower() or "Regression detection" in skill_text` — **PASSES** (both alternatives present at L1039) |
| Second assertion (L384-387) — FAILING | `"Regression takes precedence" in skill_text or "regression takes precedence" in skill_text` |
| Current literal expected | `"Regression takes precedence"` / `"regression takes precedence"` |
| Current SKILL.md substring | L1041: `"Precedence rule (regression > monotonicity)"` + `"Regression detection ALWAYS runs BEFORE the monotonicity check"` |
| **Chosen replacement** | `"Precedence rule (regression > monotonicity)"` (L1041 byte-exact; captures the precedence semantic uniquely) |

**Fix operation:** In `tests/skills/test_task_builder_merge.py` lines 384-387, replace the OR pair `"Regression takes precedence" in skill_text or "regression takes precedence" in skill_text` → single `"Precedence rule (regression > monotonicity)" in skill_text`.

## Test 3 — `TestPR02RetryMonotonicityGuards.test_rf_task_builder_has_protocol`

| Field | Value |
|------|------|
| File | `tests/skills/test_task_builder_merge.py` |
| Assertion lines | **404-409** |
| L407 | `assert "Retry Monotonicity Protocol" in rf_task_builder_text` — PASSES (3 matches in rf-task-builder.md) |
| L408 — FAILING | `assert "non-convergent" in rf_task_builder_text` — `"non-convergent"` is **ABSENT** (0 matches) |
| L409 | `assert "regression detected" in rf_task_builder_text.lower()` — PASSES (2 matches) |
| Current literal expected | `"non-convergent"` |
| Current rf-task-builder.md substring | `"byte-exact wire string"` (L358, 1 unique match — COMP-002-M5 halt-precedence rule) |
| **Chosen replacement** | `"byte-exact wire string"` (unique phrase from the protocol section; preserves the test's intent of verifying protocol presence) |

**Fix operation:** In `tests/skills/test_task_builder_merge.py` line 408, replace `"non-convergent"` → `"byte-exact wire string"`.

## Constraints

- All 3 fixes touch ONLY `tests/skills/test_task_builder_merge.py`.
- No edits to `src/superclaude/skills/task-builder/SKILL.md` or `src/superclaude/agents/rf-task-builder.md`.
- After each fix, re-run the specific test to verify PASS before proceeding.
- Final verification (Step 2.5): run all 3 tests together to confirm cumulative PASS.
