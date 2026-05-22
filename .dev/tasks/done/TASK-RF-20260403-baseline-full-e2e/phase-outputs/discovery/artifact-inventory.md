# Artifact Inventory — Baseline Pipeline Run

**Date:** 2026-04-03

## Files Produced

| File Name | Size (bytes) | Status |
|-----------|-------------|--------|
| extraction.md | 14,648 | PASS |
| roadmap-opus-architect.md | 19,645 | PASS |
| roadmap-haiku-architect.md | 63,240 | PASS |
| diff-analysis.md | 10,587 | PASS |
| debate-transcript.md | 12,594 | PASS |
| base-selection.md | 9,686 | PASS |
| roadmap.md | 25,773 | PASS |
| anti-instinct-audit.md | 658 | PASS |
| test-strategy.md | 14,657 | PASS |
| spec-fidelity.md | 9,101 | FAIL (high_severity_count > 0) |
| wiring-verification.md | 3,064 | PASS (trailing) |
| .roadmap-state.json | 3,981 | STATE |
| extraction.err | 0 | ERR |
| roadmap-opus-architect.err | 0 | ERR |
| roadmap-haiku-architect.err | 0 | ERR |
| diff-analysis.err | 0 | ERR |
| debate-transcript.err | 0 | ERR |
| base-selection.err | 0 | ERR |
| roadmap.err | 0 | ERR |
| test-strategy.err | 0 | ERR |
| spec-fidelity.err | 0 | ERR |

## Summary
- **Content .md files:** 11 (expected 9 if anti-instinct failed; got 11 because anti-instinct PASSED)
- **Error .err files:** 9 (all zero-byte)
- **State file:** 1
- **Total:** 21 files

## Notable Difference from Prior Run
Anti-instinct PASSED this time (LLM non-determinism — different merged roadmap content hit fingerprint threshold). This means test-strategy and spec-fidelity steps executed (they were SKIPPED in the prior baseline run). Pipeline halted at spec-fidelity due to high_severity_count > 0.

## Missing/Skipped
- remediate: SKIPPED (blocked by spec-fidelity failure)
- certify: SKIPPED (blocked by spec-fidelity failure)
