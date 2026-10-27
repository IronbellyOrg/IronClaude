# Evidence: D-0021 — Integration Tests: Evidence and Result File Structure

## Task
T03.06 — Integration Tests for Evidence and Result File Structure

## Test File
`tests/sprint/test_preflight.py` — class `TestPreflightEvidenceAndResultFile`

## Tests

### test_evidence_structure
- Runs `echo evidence_test` via execute_preflight_phases()
- Reads evidence file at `results/preflight-artifacts/T01.01/evidence.md`
- Asserts all 6 required fields present: command, exit_code (Exit code:), stdout, stderr, duration (Duration:), classification (Classification:)

### test_result_parseable
- Runs `echo pass` via execute_preflight_phases()
- Reads `results/phase-1-result.md`
- Passes to `_determine_phase_status(exit_code=0, ...)`
- Asserts return value == PhaseStatus.PASS

### test_result_file_halt_parseable
- Runs `false` via execute_preflight_phases()
- Reads `results/phase-1-result.md`
- Passes to `_determine_phase_status(exit_code=0, ...)`
- Asserts return value == PhaseStatus.HALT

### test_result_file_contains_source_preflight
- Runs `echo source` via execute_preflight_phases()
- Reads `results/phase-1-result.md`
- Asserts `source: preflight` present in content

## File Formats

### Evidence File Fields Verified
1. command — present as code block
2. exit_code — present as "Exit code:" label
3. stdout — present as "stdout" heading
4. stderr — present as "stderr" heading
5. duration — present as "Duration:" label
6. classification — present as "Classification:" label

### Result File Compatibility
`_determine_phase_status()` correctly interprets preflight-generated result files
with no code modifications required.

## Verification

Test command: `uv run pytest tests/sprint/test_preflight.py -v -k "evidence_structure or result_parseable"` — 2 passed
