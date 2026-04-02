# QA Report -- Phase 3 Gate (CLI Multi-File Argument)

**Topic:** Multi-File Auto-Detection -- nargs=-1 CLI argument
**Date:** 2026-04-02
**Phase:** phase-3-gate
**Fix cycle:** N/A

---

## Overall Verdict: FAIL

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | `@click.argument` decorator correct | PASS | Line 33: `@click.argument("input_files", nargs=-1, required=True, type=click.Path(exists=True, path_type=Path))` -- exact match to acceptance criteria. Verified via Read of commands.py. |
| 2 | `required=True` is set | PASS | Line 33: `required=True` present in the decorator. Verified via Read. |
| 3 | `type=click.Path(exists=True, path_type=Path)` preserved | PASS | Line 33: `type=click.Path(exists=True, path_type=Path)` present in decorator. Verified via Read. |
| 4 | Parameter name `input_files` matches decorator | PASS | Line 33 decorator uses `"input_files"`, line 136 function param is `input_files: tuple[Path, ...]`. Names match. Verified via Read. |
| 5 | Function parameter type is `tuple[Path, ...]` | PASS | Line 136: `input_files: tuple[Path, ...]`. Exact match. Verified via Read. |
| 6 | File count validation raises `click.UsageError` for >3 files | PASS | Lines 162-166: `if len(input_files) > 3: raise click.UsageError(f"Expected 1-3 input files, got {len(input_files)}. ...")`. Correct. Verified via Read. |
| 7 | Docstring describes multi-file usage with examples | PASS | Lines 152-161: Docstring mentions "INPUT_FILES accepts 1-3 markdown files (spec, TDD, PRD) in any order" with three usage examples. Verified via Read. |
| 8 | Stale `spec_file` references cleaned up | **FAIL** | Lines 186, 205: `spec_file.parent` and `spec_file.resolve()` still referenced but `spec_file` is no longer a parameter -- it was renamed to `input_files`. These will cause `NameError` at runtime. Verified via Grep for `spec_file` in commands.py. |
| 9 | `--input-type` Choice includes "prd" | PASS | Line 107: `click.Choice(["auto", "tdd", "spec", "prd"], ...)`. Verified via Read. |

## Summary
- Checks passed: 8 / 9
- Checks failed: 1
- Critical issues: 1
- Issues fixed in-place: 0 (pending)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | CRITICAL | `src/superclaude/cli/roadmap/commands.py:186` | `spec_file.parent` references undefined variable `spec_file` (renamed to `input_files` in Phase 3). Will cause `NameError` at runtime. | Change `spec_file.parent` to `input_files[0].parent` to use the first positional file as the default output directory. |
| 2 | CRITICAL | `src/superclaude/cli/roadmap/commands.py:205` | `spec_file.resolve()` references undefined variable `spec_file`. Will cause `NameError` at runtime. | This line is in the `config_kwargs` block which will be overhauled in Phase 4 (step 4.2) when routing is integrated. However, as-is after Phase 3, the code is broken. |

## Analysis of Stale References

The Phase 3 task items (3.1 and 3.2) correctly changed the decorator and function signature but did NOT update the downstream usages of the old `spec_file` variable name in the function body. Three stale references exist:

1. **Line 186:** `resolved_output = output_dir if output_dir is not None else spec_file.parent` -- should be `input_files[0].parent`
2. **Line 205:** `"spec_file": spec_file.resolve()` -- should be `input_files[0].resolve()` as a transitional fix (Phase 4 will replace this with routing)
3. **Line 231:** `resolved_type = detect_input_type(config.spec_file)` -- this is fine, it references `config.spec_file` (a field on RoadmapConfig), not the local variable.

**Impact:** The `run` command will crash with `NameError: name 'spec_file' is not defined` on ANY invocation. This is a blocking defect.

**Relationship to Phase 4:** Phase 4 step 4.2 plans to overhaul the `config_kwargs` block, which would fix issue #2. However, Phase 3 should leave the code in a runnable state between phases. The stale references make the CLI broken after Phase 3 and before Phase 4.

## Actions Taken

1. **Fixed** stale `spec_file.parent` on line 186 of `commands.py` -- changed to `input_files[0].parent`. Verified via Grep that no stale local `spec_file` references remain.
2. **Fixed** stale `spec_file.resolve()` on line 205 of `commands.py` -- changed to `input_files[0].resolve()`. Verified via Grep and Read of surrounding context (lines 183-207).
3. **Verified** line 231 `config.spec_file` is NOT stale -- it references the `spec_file` field on the `RoadmapConfig` dataclass, not the old local parameter. No fix needed.

Post-fix verification: Grep for `spec_file` in commands.py returns only:
- Line 205: `"spec_file": input_files[0].resolve()` (dict key, correct)
- Line 231: `config.spec_file` (dataclass field access, correct)

## Updated Summary (Post-Fix)
- Checks passed: 9 / 9 (after fixes)
- Checks failed: 0
- Critical issues fixed in-place: 2

## Updated Verdict: PASS (after in-place fixes)

## Confidence Gate

- **Verified:** 9/9 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 5 | Grep: 4 | Glob: 0 | Bash: 1

## Recommendations
- Phase 4 step 4.2 will overhaul the `config_kwargs` block with routing integration, which will replace the transitional `input_files[0]` references with proper routing dict values. The transitional fixes applied here are intentionally minimal to avoid conflict with Phase 4.
- No further action needed before proceeding to Phase 4.

## QA Complete
