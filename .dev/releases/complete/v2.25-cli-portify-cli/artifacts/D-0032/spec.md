# D-0032: Gate Diagnostics Formatting

**Task:** T04.03
**Roadmap Item:** R-036
**Status:** COMPLETE

## Deliverables

Both implemented in `src/superclaude/cli/cli_portify/gates.py`:

### `format_gate_failure(gate_id, check_name, diagnostic, artifact_path) -> str`

Produces multi-line human-readable gate failure message:
```
Gate {gate_id} FAILED: {check_name}
  Artifact: {artifact_path}
  Reason: {diagnostic}
  Fix: {remediation_hint}
```

Remediation hints are pre-defined for all known check names. Unknown checks fall back to a default hint.

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

Importable from `superclaude.cli.cli_portify.gates`.

## Acceptance Criteria Verification

```python
format_gate_failure(
    "G-003",
    "has_required_analysis_sections",
    "Missing: Step Graph",
    "portify-analysis-report.md",
)
```

Returns multi-line string containing all 4 fields: G-003, has_required_analysis_sections, portify-analysis-report.md, Missing: Step Graph.

## Verification

```
uv run pytest tests/cli_portify/test_semantic_checks.py -k "gate_failure or gate_diagnostics or GateFailure" -v
```

Result: **13 passed**
