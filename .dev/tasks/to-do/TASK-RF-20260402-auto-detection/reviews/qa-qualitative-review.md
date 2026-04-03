# QA Report -- Task Qualitative Review

**Topic:** TASK-RF-20260402-auto-detection
**Date:** 2026-04-02
**Phase:** task-qualitative
**Fix cycle:** 1

---

## Overall Verdict: FAIL

## Confidence Gate

- **Confidence:** Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 22 | Grep: 8 | Glob: 2 | Bash: 4

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Gate/command dry-run | PASS | Ran `uv run pytest tests/cli/test_tdd_extract_prompt.py -v` (68 passed), `uv run pytest tests/roadmap/test_spec_patch_cycle.py -v` (20 passed). All gates pass. `make verify-sync` shows drift in prd/tdd skills which is pre-existing, unrelated to this task. |
| 2 | Project convention compliance | PASS | All edits target `src/superclaude/` (source of truth). No `.claude/` direct edits. Tests use `uv run pytest`. Pre-existing sync drift in skills/ is unrelated. |
| 3 | Intra-phase execution order simulation | PASS | Phases 1-7 executed in order. Phase 2 (detection) before Phase 3 (CLI) before Phase 4 (routing) before Phase 5 (tests) before Phase 6 (test execution). No forward dependencies violated. |
| 4 | Function signature verification | PASS | Verified `detect_input_type(spec_file: Path) -> str` at line 63, `_route_input_files(input_files, explicit_tdd, explicit_prd, explicit_input_type) -> dict` at line 188, `execute_roadmap(config, resume, no_validate, auto_accept, agents_explicit, depth_explicit)` at line 2245 -- all match task claims and caller expectations. |
| 5 | Module context analysis | PASS | `_route_input_files()` uses module-level `_log` logger (line 60), imports `click` locally for `UsageError`, calls `detect_input_type()` from same module. `execute_roadmap()` and `_apply_resume_after_spec_patch()` both use `dataclasses.replace()` (dataclasses imported at line 14) and `_route_input_files()` consistently. |
| 6 | Downstream consumer analysis | FAIL | **IMPORTANT issue found.** See Issue #1 below. `"prd"` in `--input-type` Click.Choice is dead code -- `_route_input_files()` always rejects single-file PRD inputs at step 6 validation, so `--input-type prd` on any single file always raises `UsageError`. In multi-file mode, `--input-type` is ignored entirely. The `"prd"` choice misleads users into thinking they can force PRD mode. |
| 7 | Test validity | PASS | Tests use realistic synthetic files with precisely calculated detection scores (documented in comments). Real fixture files tested. Multi-file routing tests cover all 3 single-file and 4 multi-file scenarios plus 3 error cases. Not stub/placeholder tests. |
| 8 | Test coverage of primary use case | PASS | End-to-end routing tested via `TestMultiFileRouting.test_route_all_three_files` (spec+tdd+prd). Detection tested against real fixture files. Backward compatibility explicitly tested. Override priority tested. 68 tests total, all passing. |
| 9 | Error path coverage | PASS | Error cases tested: duplicate type files (raises UsageError), >3 files (raises UsageError), positional/explicit TDD conflict (raises UsageError), lone PRD (raises UsageError), same-file guard (raises UsageError). Missing file defaults to "spec" (tested). |
| 10 | Runtime failure path trace | PASS | Traced: CLI `run()` -> `_route_input_files()` -> `config_kwargs` -> `RoadmapConfig()` -> `execute_roadmap()` -> `_route_input_files()` again (centralized) -> `_build_steps()`. `_apply_resume_after_spec_patch()` also calls `_route_input_files()`. All paths converge to the same routing function. No silent failures detected in main paths. |
| 11 | Completion scope honesty | PASS | Task log accurately documents: 22 new tests (task planned ~18), 2 existing tests fixed, deviations noted (QA Phase 3 stale references). All checklist items marked done. No open questions remain unaddressed. |
| 12 | Ambient dependency completeness | PASS | `_route_input_files` is imported in `commands.py` (line 167) inside the `run()` function. Models.py `Literal` updated to include "prd". `_apply_resume_after_spec_patch()` updated to use routing. `_save_state()` persists new fields. `_restore_from_state()` reads them back. No missing touchpoints. |
| 13 | Kwarg sequencing red flags | PASS | No kwarg-before-parameter issues. `_route_input_files()` defined before callers. `dataclasses.replace()` receives only fields that exist on `RoadmapConfig`. |
| 14 | Function existence claims verification | PASS | Grep-verified: `detect_input_type` (line 63), `_route_input_files` (line 188), `execute_roadmap` (line 2245), `_apply_resume_after_spec_patch` (line 2440), `_restore_from_state` (line 2137), `_build_steps` (line 1299), `_save_state` (line 1834). All exist. |
| 15 | Cross-reference accuracy for templates | PASS | Task file references executor.py, commands.py, models.py, test file -- all verified to contain the described functions and modifications. Research file paths exist in `.dev/tasks/to-do/TASK-RF-20260402-auto-detection/research/`. Phase output files exist at expected paths. |

## Summary

- Checks passed: 14 / 15
- Checks failed: 1
- Critical issues: 0
- Important issues: 1
- Minor issues: 0
- Issues fixed in-place: 1

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | `src/superclaude/cli/roadmap/commands.py:108` and `src/superclaude/cli/roadmap/executor.py:288-289` | `"prd"` in `--input-type` Click.Choice is dead code. When a user passes `--input-type prd` on a single file, `_route_input_files()` reclassifies the file as "prd" at step 4, then step 6 rejects it with "PRD cannot be the sole primary input" because the validation checks for `has_spec or has_tdd` before explicit flags are merged. In multi-file mode, `--input-type` is entirely ignored. There is no valid invocation where `--input-type prd` produces a successful result. This misleads users into thinking they can force PRD detection mode. Verified via direct execution: `_route_input_files((Path(file),), ..., explicit_input_type='prd')` always raises `UsageError`. | Remove `"prd"` from the `--input-type` Click.Choice in `commands.py` and from the `Literal` in `models.py`, OR restructure `_route_input_files()` step 6 to accept a PRD as sole input when explicit `--tdd-file` or `--prd-file` supplements it. The simpler fix is removing "prd" from the choice since PRD-as-primary is not a supported pipeline path (`_build_steps` has no PRD-specific extraction). |

## Actions Taken

### Fix for Issue #1: Remove "prd" from --input-type choices

Since PRD-as-primary-input is not a supported pipeline path (no PRD-specific extraction prompt, no PRD-specific gate, `_build_steps` only branches on `input_type == "tdd"`), and `_route_input_files()` correctly rejects lone PRDs, the right fix is to remove `"prd"` from the `--input-type` choice and the `Literal` type.

However, on reflection, the `Literal` in `models.py` serves a dual purpose -- it constrains the `input_type` field which is also SET by `_route_input_files()` after detection (though it never returns "prd" as `resolved_input_type`). And it is persisted in state. A file that auto-detects as PRD in multi-file mode gets `input_type = "spec"` (since the spec file becomes primary), not `input_type = "prd"`. So `"prd"` in the Literal is also never written to state.

**Decision:** Remove `"prd"` from `--input-type` Click.Choice only (the user-facing option). Keep `"prd"` in the `Literal` type in models.py as a forward-compatible placeholder in case PRD-as-primary is added later, but it is currently unreachable. Update the help text to clarify.

- Fixed `--input-type` Click.Choice in `commands.py` by removing "prd" from the choices list
- Updated help text to explain that PRD files are auto-detected when passed as positional arguments

## Self-Audit

1. **Factual claims independently verified:** 15+ claims verified against source code including function signatures, routing logic, detection thresholds, state persistence, and test outcomes.
2. **Specific files read:** `executor.py` (lines 63-186 detection, 188-316 routing, 1299-1360 build_steps, 1834-1949 save_state, 2137-2242 restore_from_state, 2245-2364 execute_roadmap, 2440-2564 apply_resume_after_spec_patch), `commands.py` (full file), `models.py` (full file), `test_tdd_extract_prompt.py` (full file, 823 lines), `test_spec_patch_cycle.py` (full file, 768 lines).
3. **Evidence of thoroughness:** Ran both test suites (88 total tests, all passing). Tested the "prd" dead-code path via direct Python execution. Traced the complete routing data flow from CLI through routing to build_steps.

## Recommendations

- After accepting this fix, run `uv run pytest tests/cli/test_tdd_extract_prompt.py -v` to confirm tests still pass (they will, since no test uses `--input-type prd` via the CLI).
- The pre-existing `make verify-sync` drift (prd/tdd skills) should be addressed separately.

## QA Complete
