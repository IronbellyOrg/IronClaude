# Phase 3: Dry-Run Comparison

**Date:** 2026-03-27

## Step Plan Comparison

Both TDD and spec dry-runs produce identical step plans with 11 steps:

| Step | TDD Dry-Run | Spec Dry-Run | Match |
|------|-------------|-------------|-------|
| 1: extract | STRICT, 50 min lines, 13 fields | STRICT, 50 min lines, 13 fields | YES |
| 2: generate-opus-architect (parallel) | STRICT, 100 min lines, model: opus | STRICT, 100 min lines, model: opus | YES |
| 3: generate-haiku-architect (parallel) | STRICT, 100 min lines, model: haiku | STRICT, 100 min lines, model: haiku | YES |
| 4: diff | STANDARD, 30 min lines | STANDARD, 30 min lines | YES |
| 5: debate | STRICT, 50 min lines | STRICT, 50 min lines | YES |
| 6: score | STANDARD, 20 min lines | STANDARD, 20 min lines | YES |
| 7: merge | STRICT, 150 min lines | STRICT, 150 min lines | YES |
| 8: anti-instinct | STRICT, 10 min lines | STRICT, 10 min lines | YES |
| 9: test-strategy | STRICT, 40 min lines | STRICT, 40 min lines | YES |
| 10: spec-fidelity | STRICT, 20 min lines | STRICT, 20 min lines | YES |
| 11: wiring-verification | STRICT, 10 min lines | STRICT, 10 min lines | YES |

## Expected Differences

| Difference | TDD | Spec | Expected? |
|------------|-----|------|-----------|
| Auto-detection type | "tdd" (confirmed via direct test) | "spec" (confirmed via direct test) | YES |
| TDD warning | Would print DEVIATION_ANALYSIS_GATE warning | No warning | YES |
| Extract prompt function | `build_extract_prompt_tdd()` (14 sections, 19 fields) | `build_extract_prompt()` (8 sections, 13 fields) | YES |

## CLI Feedback Issue

Auto-detection messages (`click.echo(..., err=True)`) are not visible in dry-run output for either fixture. This is a CLI display bug, not a functional issue — detection works correctly as confirmed by direct Python invocation.

## Conclusion

Step plans are structurally identical. Only the extract prompt differs (by design). Both fixtures are ready for full pipeline runs.
