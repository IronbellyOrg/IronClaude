# D-0038: 0-files-analyzed assertion guard in wiring_gate.py

## Spec Reference
- FR-5.1: If `files_analyzed == 0` and source dir is non-empty, return FAIL with `failure_reason`
- R-039 (roadmap item)

## Change Summary

### Modified: `src/superclaude/cli/audit/wiring_gate.py`

**WiringReport dataclass** — added `failure_reason: str = ""` field to carry structured failure information.

**`run_wiring_analysis()`** — added additive early-return guard after file collection:
- If `files_analyzed == 0`, checks whether source dir contains any `*.py` files via `source_dir.rglob("*.py")`
- If Python files exist but none survived collection (all excluded), returns `WiringReport` with `failure_reason = "0 files analyzed in non-empty source directory"`
- Logs warning with skip count for observability
- Guard is purely additive: existing return paths are unmodified

## Acceptance Criteria Mapping
| Criterion | Status |
|---|---|
| Returns FAIL with `failure_reason` when `files_analyzed == 0` on non-empty dir | DONE |
| Change is additive (new early return); existing paths unmodified | DONE |
| No regressions (1520 passed, 10 skipped) | DONE |
| Docstring updated | DONE |
