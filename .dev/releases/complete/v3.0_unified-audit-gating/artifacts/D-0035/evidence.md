# D-0035: Unit Tests for AST Plugin Integration

## Test Evidence

### Plugin Tests (>=3 tests, SC-013)
```
tests/audit/test_wiring_analyzer.py::TestPluginRegistration::test_plugin_registers_with_orchestrator PASSED
tests/audit/test_wiring_analyzer.py::TestPluginRegistration::test_plugin_callable_through_orchestrator PASSED
tests/audit/test_wiring_analyzer.py::TestPluginRegistration::test_plugin_does_not_modify_orchestrator_interface PASSED
tests/audit/test_wiring_analyzer.py::TestReferencesPopulated::test_references_populated_for_file_with_imports PASSED
tests/audit/test_wiring_analyzer.py::TestReferencesPopulated::test_references_empty_for_file_without_calls PASSED
tests/audit/test_wiring_analyzer.py::TestReferencesPopulated::test_plugin_handles_syntax_error_gracefully PASSED
tests/audit/test_wiring_analyzer.py::TestDualEvidenceRule::test_dual_evidence_prevents_false_positive PASSED
tests/audit/test_wiring_analyzer.py::TestDualEvidenceRule::test_dual_evidence_still_flags_true_orphans PASSED
tests/audit/test_wiring_analyzer.py::TestDualEvidenceRule::test_fallback_to_import_only_without_plugin PASSED
tests/audit/test_wiring_analyzer.py::TestDualEvidenceRule::test_dual_evidence_note_in_detail PASSED
```

### Test Results Summary
- Total tests in test_wiring_analyzer.py: 19 (9 pre-existing + 10 new)
- Plugin-specific tests (`-k "plugin"`): 5 passed
- Dual evidence tests (`-k "dual_evidence"`): 3 passed
- Regression tests (test_wiring_gate.py): 78 passed, 0 failures

### Acceptance Criteria
- [x] `uv run pytest tests/audit/test_wiring_analyzer.py -k "plugin" -v` exits 0 with >=3 tests
- [x] Plugin registration test confirms successful hookup with ToolOrchestrator
- [x] References populated test confirms FileAnalysis.references non-empty for files with imports
- [x] Dual evidence test confirms false positive reduction for orphan detection
