# D-0058: Click Command Group with All Options in commands.py

## Status: COMPLETE

## Deliverable
`src/superclaude/cli/cli_portify/commands.py`

## Implementation
- `cli_portify_group = click.Group("cli-portify")` via `@click.group("cli-portify")`
- `run` subcommand with all 7 options:
  - `--name` (str, default "")
  - `--output` (str, default "")
  - `--max-turns` (int, default 200)
  - `--model` (str, default "")
  - `--dry-run` (flag, bool)
  - `--resume` STEP_ID (str, default "")
  - `--debug` (flag, bool)
- Command body calls `run_portify(config)` from `executor.py`
- `PortifyValidationError` → print error + exit 1
- `KeyboardInterrupt` → emit return contract marker + exit 0

## Verification
```
uv run python -c "from superclaude.cli.cli_portify.commands import cli_portify_group; assert isinstance(cli_portify_group, __import__('click').Group)"
```
- `cli_portify_group` is a `click.Group` ✓
- `run` subcommand present ✓
- All 7 options with correct types and defaults ✓
- `--max-turns` defaults to 200 ✓
