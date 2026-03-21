# D-0021: cli-portify Fixture Integration Test Evidence

## Task: T04.01
## SC-010 Behavioral Contract Validation

### Test File
`tests/audit/test_wiring_integration.py`

### Test Results
```
tests/audit/test_wiring_integration.py::TestCliPortifyWiringIntegration::test_analyze_unwired_callables_detects_noop_bug PASSED
tests/audit/test_wiring_integration.py::TestCliPortifyWiringIntegration::test_run_wiring_analysis_full_report PASSED
tests/audit/test_wiring_integration.py::TestCliPortifyWiringIntegration::test_finding_references_original_noop_pattern PASSED
tests/audit/test_wiring_integration.py::TestCliPortifyWiringIntegration::test_wiring_fixed_produces_zero_findings PASSED

4 passed in 0.10s
```

### Finding Details
- **finding_type**: `unwired_callable`
- **symbol_name**: `PortifyExecutor.step_runner`
- **severity**: `critical`
- **detail**: Parameter 'step_runner' typed Optional[Callable] with default None is never wired by any call site

### Fixture Design
The fixture models the original cli-portify defect pattern:
- `executor.py`: Declares `PortifyExecutor.__init__(step_runner: Optional[Callable] = None)`
- `main.py`: Instantiates `PortifyExecutor("/tmp/work")` WITHOUT passing `step_runner`
- Result: analyzer correctly identifies 1 unwired_callable finding

### Negative Control
`test_wiring_fixed_produces_zero_findings` confirms that when `step_runner` IS wired
at the call site, zero findings are produced.

### Note on kwonly args
The analyzer currently scans `args.args` (positional params) but not `args.kwonlyargs`.
The real cli-portify executor uses keyword-only `step_runner` (after `*`). The fixture
uses positional form to match the analyzer's current detection scope. This limitation
is documented for future enhancement.
