# Phase 2 PRD Detection Check

**Date:** 2026-04-02
**Command:** `uv run superclaude roadmap run .dev/test-fixtures/test-prd-user-auth.md --dry-run`

## Output
```
Error: PRD cannot be the sole primary input; provide a spec or TDD file.
Exit code: 2
```

## Analysis

The error message "PRD cannot be the sole primary input" proves that:
1. `detect_input_type()` classified the PRD fixture as **"prd"** (not "tdd" or "spec")
2. `_route_input_files()` correctly identified no spec or TDD primary input
3. The validation check `if not has_spec and not has_tdd: if has_prd: raise UsageError(...)` fired correctly

This is the EXPECTED behavior. PRD documents are now auto-detected as "prd" (not "spec" as in the original E2E run). PRD cannot be a sole primary input — it must be accompanied by a spec or TDD file.

| Check | Expected | Actual | Result |
|-------|----------|--------|--------|
| Detected as "prd" | Yes | Yes (UsageError confirms PRD detection) | PASS |
| NOT detected as "tdd" | Correct | Correct | PASS |
| NOT detected as "spec" | Correct | Correct (would have proceeded to dry-run if spec) | PASS |
| UsageError for sole PRD | Yes | Yes — "PRD cannot be the sole primary input" | PASS |

## Result: ALL 4 DETECTION CHECKS PASS
