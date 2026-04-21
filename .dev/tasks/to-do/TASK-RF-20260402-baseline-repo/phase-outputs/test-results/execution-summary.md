# Execution Summary — E2E Test 3 (Baseline)

**Date:** 2026-04-02
**Pipeline:** superclaude roadmap run (baseline, master @ 4e0c621)
**Input:** test-spec-user-auth.md (312 lines)
**Output dir:** .dev/test-fixtures/results/test3-spec-baseline/

## File Count
- Content .md files: 9
- Error .err files: 7 (all zero-byte)
- State file: 1 (.roadmap-state.json)
- **Total: 17 files**

## Step Results

| Step ID | Status | Attempt | Output File | Size |
|---------|--------|---------|-------------|------|
| extract | PASS | 1 | extraction.md | 13,775 bytes |
| generate-opus-architect | PASS | 1 | roadmap-opus-architect.md | 18,407 bytes |
| generate-haiku-architect | PASS | 1 | roadmap-haiku-architect.md | 62,518 bytes |
| diff | PASS | 1 | diff-analysis.md | 9,831 bytes |
| debate | PASS | 1 | debate-transcript.md | 15,250 bytes |
| score | PASS | 1 | base-selection.md | 13,379 bytes |
| merge | PASS | 2 (resume) | roadmap.md | 27,192 bytes |
| anti-instinct | FAIL | 1 | anti-instinct-audit.md | 673 bytes |
| wiring-verification | PASS | 1 (trailing) | wiring-verification.md | 3,064 bytes |
| test-strategy | SKIPPED | — | — | — |
| spec-fidelity | SKIPPED | — | — | — |

## Notes
- Merge initially FAILED (duplicate headings gate), PASSED on resume
- Anti-instinct FAILED as expected (fingerprint_coverage < 0.7, GateMode.BLOCKING)
- test-strategy and spec-fidelity SKIPPED (blocked by anti-instinct)
- wiring-verification ran as trailing/deferred step (PASS)
- No Python errors or crashes

## Overall Verdict: PASS
Pipeline completed its expected steps. Anti-instinct failure is expected behavior (same as Test 1 and Test 2). 9 content artifacts produced matching expected count.
