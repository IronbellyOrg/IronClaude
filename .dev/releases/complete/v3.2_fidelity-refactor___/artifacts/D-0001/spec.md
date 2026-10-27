# D-0001: WiringFinding and WiringReport Dataclasses

- **File**: `src/superclaude/cli/audit/wiring_gate.py`
- **WiringFinding**: 7 fields (finding_type, file_path, symbol_name, line_number, detail, severity, suppressed)
- **WiringReport**: 8 fields + 5 computed properties (all_findings, total_findings, unsuppressed_findings, clean, blocking_count)
- **Verification**: 78 tests pass in test_wiring_gate.py
