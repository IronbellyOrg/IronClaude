# D-0043: user-review-p2 Gate and phase2-approval.yaml Validation

## Status: COMPLETE

## Deliverable

- `executor.py`: `execute_user_review_p2(config_cli_name, workdir, step_results, _exit) -> None`
- `executor.py`: `_validate_phase2_approval(workdir) -> None`
- Phase 2 approval uses `status: completed` (not `approved` as in Phase 1)
- Validates all blocking gates (G-005, G-006, G-007, G-008) passed before writing YAML
- Validates `portify-spec.md` has non-empty `step_mapping` section
- YAML parse + schema validation on resume (`_validate_phase2_approval`)

## Acceptance Criteria

- [x] `uv run pytest tests/cli_portify/ -k "phase2_approval"` exits 0
- [x] `execute_user_review_p2()` writes `phase2-approval.yaml` with `status: completed`
- [x] Resume with `status: pending` raises `PortifyValidationError`
- [x] Empty `step_mapping` in `portify-spec.md` blocks approval emission
- [x] All blocking gates must pass before approval YAML is written

## Test Results

All phase2_approval and user_review_p2 tests passing.
`_validate_phase2_approval()` correctly raises `PortifyValidationError` with `error_code="INVALID_PATH"` for all invalid states.
