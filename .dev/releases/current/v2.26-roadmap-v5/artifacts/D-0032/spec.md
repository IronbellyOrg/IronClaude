# D-0032: _print_terminal_halt() Implementation

## Summary

Implemented `_print_terminal_halt()` in `src/superclaude/cli/roadmap/executor.py`.

## Function Signature

```python
def _print_terminal_halt(
    attempt_count: int,
    failing_findings: list,
    certification_report_path: Path | None = None,
    output_dir: Path | None = None,
    spec_patch_budget_exhausted: bool = False,
) -> None:
```

## Output (to stderr)

```
======================================================================
TERMINAL HALT: Remediation budget exhausted
======================================================================
Remediation attempts made: N
Remaining failing findings: M

Failing findings:
  [F-01] [BLOCKING] Missing milestone
  [F-02] [WARNING] Unclear wording

----------------------------------------------------------------------
Manual fix required:
  Review certification report: /path/to/certification-report.md
  After fixing, resume with: superclaude roadmap run <spec> --resume
----------------------------------------------------------------------
```

## FR-077 Dual-Budget Placeholder

When `spec_patch_budget_exhausted=True`, appends:
```
Note: Both the remediation budget and the spec-patch cycle budget
are exhausted. Full dual-budget recovery is deferred to v2.26.
```

## Test Results

`uv run pytest tests/sprint/test_executor.py -v -k "terminal_halt"` — **9 passed**
- Writes to stderr (not stdout) ✓
- Includes attempt count ✓
- Includes failing finding count ✓
- Includes per-finding details (ID, severity, description) ✓
- Includes manual-fix instructions with resume command ✓
- Includes certification report path when provided ✓
- Dual-budget note appears when spec_patch_budget_exhausted=True ✓
- No dual-budget note for normal single-budget halt ✓
