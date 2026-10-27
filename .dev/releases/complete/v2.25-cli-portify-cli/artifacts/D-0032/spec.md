# D-0032 — Gate Diagnostics Formatting

**Produced by**: T04.03
**Sprint**: v2.25-cli-portify-cli
**Date**: 2026-03-16

---

## Summary

Implemented `format_gate_failure()` and `GateFailure` dataclass in
`src/superclaude/cli/cli_portify/gates.py`.

---

## Deliverables

### `format_gate_failure(gate_id, check_name, diagnostic, artifact_path) -> str`

Output format:
```
Gate {gate_id} FAILED: {check_name}
  Artifact: {artifact_path}
  Reason: {diagnostic}
  Fix: {remediation_hint}
```

### `GateFailure` dataclass

```python
@dataclass
class GateFailure:
    gate_id: str
    check_name: str
    diagnostic: str
    artifact_path: str
    tier: Literal["STRICT", "STANDARD", "LIGHT", "EXEMPT"] = "STANDARD"
```

---

## Acceptance Criteria Verification

- `format_gate_failure("G-003", "has_required_analysis_sections", "Missing: Step Graph", "portify-analysis-report.md")` returns multi-line string with all 4 fields ✓
- `GateFailure` dataclass importable from `superclaude.cli.cli_portify.gates` ✓
- Diagnostic string is never empty for a failing gate ✓
- `uv run pytest tests/cli_portify/ -k "gate_diagnostics or gate_failure"` exits 0 ✓

**Test count**: Covered by test_semantic_checks.py (TestFormatGateFailure, TestGateFailureDataclass) — all passing
