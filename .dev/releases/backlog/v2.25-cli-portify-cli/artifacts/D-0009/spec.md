# D-0009: CLI Name Derivation — Implementation Spec

**Task:** T02.02 | **Roadmap Item:** R-009 | **Status:** COMPLETE

## Implementation

`derive_cli_name(workflow_path, explicit_name=None)` in `config.py:242`
`_derive_name_from_path(workflow_path)` in `models.py:655`

### Derivation Algorithm
1. explicit_name provided → return as-is
2. Take directory name
3. Strip `sc-` prefix (case-insensitive)
4. Strip `-protocol` suffix (case-insensitive)
5. Normalize to lowercase kebab-case
6. Empty result → raise DerivationFailedError (DERIVATION_FAILED)

### Examples
- `sc-roadmap-protocol` → `roadmap`
- `sc-my-workflow-protocol` → `my-workflow`
- `sc-roadmap-protocol` + explicit `my-tool` → `my-tool`

## Verification
`uv run pytest tests/cli_portify/test_config.py::TestConfigHappyPath -v` → passed
