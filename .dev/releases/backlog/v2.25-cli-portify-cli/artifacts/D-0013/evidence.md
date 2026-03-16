# D-0013: portify-config.yaml Emission — Evidence

**Task:** T02.06 | **Roadmap Item:** R-013 | **Status:** COMPLETE

## Implementation

`emit_portify_config_yaml(config, workdir)` in `workdir.py:35`

### Output Fields (G-000 compliant)
- `workflow_path` — resolved workflow directory path
- `cli_name` — kebab-case derived CLI name
- `cli_name_snake` — snake_case variant
- `output_dir` — output destination path
- `workdir_path` — the working directory path
- `dry_run`, `debug`, `max_turns`, `stall_timeout` — pipeline options

### G-000 Gate Compliance
All required fields present: workflow_path, cli_name, output_dir, workdir_path.
YAML parseable by `yaml.safe_load()`.

## Verification Evidence
`uv run pytest tests/cli_portify/test_config.py::TestWorkdirCreation::test_portify_config_yaml_parseable -v` → PASSED
All 5 workdir tests passed.
