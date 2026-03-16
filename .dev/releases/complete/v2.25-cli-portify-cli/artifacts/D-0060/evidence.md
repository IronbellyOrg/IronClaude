# D-0060: Register cli_portify_group in main.py

## Status: COMPLETE

## Deliverable
`src/superclaude/cli/main.py` — `cli_portify_group` registered

## Changes
Added after `tasklist_group` registration:
```python
from superclaude.cli.cli_portify.commands import cli_portify_group
main.add_command(cli_portify_group)
```

## Verification
```
uv run python -c "from superclaude.cli.main import main; assert 'cli-portify' in main.commands"
```
Output: `cli-portify registered: ['install', 'mcp', 'update', 'install-skill', 'doctor', 'version', 'sprint', 'roadmap', 'cleanup-audit', 'tasklist', 'cli-portify']`

- `'cli-portify' in main.commands` → True ✓
- Import follows existing main.py registration pattern ✓
- No other command groups broken ✓
