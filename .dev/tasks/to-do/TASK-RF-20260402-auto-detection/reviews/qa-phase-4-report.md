# QA Report — Phase 4 Gate (Routing Function in executor.py)

**Topic:** Multi-File Auto-Detection — Phase 4 Routing Function
**Date:** 2026-04-02
**Phase:** task-integrity (phase-gate verification)
**Fix cycle:** N/A

---

## Overall Verdict: PASS

## Confidence Gate

- **Confidence:** Verified: 12/12 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 14 | Grep: 9 | Glob: 0 | Bash: 1

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | `_route_input_files()` exists between `detect_input_type()` and kernel constants | PASS | `detect_input_type()` ends at line 185, `_route_input_files()` at lines 188-316, kernel constants `_MAX_ARG_STRLEN` at line 320 |
| 2 | Imports `click` for `UsageError` | PASS | Line 199: `import click` (lazy import inside function body) |
| 3 | Uses `_log` for warnings | PASS | Lines 219, 293: `_log.warning(...)` — module-level `_log` defined at line 59 |
| 4 | Handles single-file backward-compatible path | PASS | Lines 216-217: single-file override via `explicit_input_type != "auto" and len(input_files) == 1` |
| 5 | All 12 algorithm steps from research present | PASS | Steps mapped: (1) count=0 at L202, (2) count>3 at L204, (3) classify at L211, (4) override at L216, (5) duplicates at L225, (6) primary check at L237, (7) slot assignment at L249, (8) flag merge at L265, (9) input_type at L282, (10) redundancy guard at L292, (11) same-file guard at L299, (12) return at L311. Comment numbering skips `# 2.` (cosmetic — steps 1-2 combined under `# 1. Validate count`) |
| 6 | `execute_roadmap()` no longer has inline auto-resolution, same-file guard, or redundancy guard | PASS | Grep for `resolved = detect_input_type` returns 0 matches. Lines 2295-2312 use `_route_input_files()` call + `dataclasses.replace()`. No inline same-file or redundancy guards remain. |
| 7 | `_apply_resume_after_spec_patch()` uses `_route_input_files()` | PASS | Lines 2530-2542: calls `_route_input_files(input_files=(config.spec_file,), ...)` followed by `dataclasses.replace()`. No inline `detect_input_type()` call. |
| 8 | `commands.py` imports `_route_input_files` from `.executor` | PASS | Line 167: `from .executor import _route_input_files, execute_roadmap` |
| 9 | `config_kwargs` uses `routing["spec_file"].resolve()` etc. | PASS | Line 211: `routing["spec_file"].resolve()`, Line 220: `routing["input_type"]`, Line 221: `routing["tdd_file"].resolve() if routing["tdd_file"] else None`, Line 222: same pattern for `prd_file` |
| 10 | No stale `detect_input_type` import in commands.py | PASS | Grep for `detect_input_type` in commands.py returns 0 matches |
| 11 | No other code in `execute_roadmap()` accidentally modified | PASS | Read lines 2245-2391 of execute_roadmap(). Structure intact: resume restore -> defaults -> hash capture -> routing -> build steps -> dry-run -> resume -> execute -> save -> failure handling -> validation. All non-routing code unchanged. |
| 12 | models.py and --input-type Choice include "prd" | PASS | models.py line 114: `Literal["auto", "tdd", "spec", "prd"]`. commands.py line 107: `click.Choice(["auto", "tdd", "spec", "prd"])` |

## Summary

- Checks passed: 12 / 12
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0

## Issues Found

None.

## Minor Observations (Non-Blocking)

| # | Severity | Location | Observation | Notes |
|---|----------|----------|-------------|-------|
| 1 | COSMETIC | executor.py:201-210 | Comment numbering skips `# 2.` — goes from `# 1. Validate count` to `# 3. Classify each file`. Research algorithm lists steps 1 (count=0) and 2 (count>3) separately, but code combines them under one comment. | Not a functional issue. All 12 algorithmic behaviors are present. No fix needed. |

## Verification Details

### Algorithm Step Mapping (Research 03-routing-logic.md Section 7.2 vs Implementation)

| Research Step | Code Line | Comment Label | Status |
|---------------|-----------|---------------|--------|
| 1. len == 0 raise | 202-203 | `# 1. Validate count` | Present |
| 2. len > 3 raise | 204-208 | (same block) | Present |
| 3. Classify each file | 211-213 | `# 3. Classify each file` | Present |
| 4. Apply explicit override | 216-222 | `# 4. Apply explicit override` | Present |
| 5. Validate no duplicates | 225-234 | `# 5. Validate no duplicates` | Present |
| 6. Validate primary input | 237-246 | `# 6. Validate primary input` | Present |
| 7. Assign slots | 249-262 | `# 7. Assign slots` | Present |
| 8. Merge explicit flags | 265-279 | `# 8. Merge explicit flags` | Present |
| 9. Determine input_type | 282-289 | `# 9. Determine input_type` | Present |
| 10. Redundancy guard | 292-296 | `# 10. Redundancy guard` | Present |
| 11. Same-file guard | 299-308 | `# 11. Same-file guard` | Present |
| 12. Return | 311-316 | `# 12. Return` | Present |

### Edge Cases Covered (Research Section 8)

| Edge Case | Handling | Verified |
|-----------|----------|----------|
| 8.1 Single PRD -> Error | Line 242-244: `"PRD cannot be the sole primary input"` | Yes |
| 8.2 Two files both spec -> Error | Lines 228-234: generic duplicate check covers this | Yes |
| 8.3 Three files: TDD + 2 specs -> Error | Same duplicate check | Yes |
| 8.4 Explicit --tdd-file + positional TDD | Lines 266-270: conflict check raises UsageError | Yes |
| 8.5 --input-type + multiple files | Lines 218-222: warning logged, override ignored | Yes |
| 8.6 Backward compat: single file | Lines 216-217: single-file override preserved | Yes |

## Recommendations

- None. Phase 4 implementation is complete and correct. Proceed to Phase 5 (Test Implementation).

## QA Complete
