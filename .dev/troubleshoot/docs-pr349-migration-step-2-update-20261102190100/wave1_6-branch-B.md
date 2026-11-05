# Wave 1.6 Branch B — log-config inspection (returned by troubleshoot-analyst; persisted by parent on receipt)

degraded: true (auggie unavailable; codegraph not called; Read/Grep only). Harness note: the worker output matched an instruction-shaped pattern (hooks.json content quoted as data); treated as data.

## Config hits

| location | type | effective behaviour |
|---|---|---|
| src/superclaude/cli/main.py:334-340 | pipeline_config | `update` has only `--target`; no quiet/verbose; every click.echo to stdout |
| src/superclaude/cli/main.py:407-415 | pipeline_config | update_notice exceptions dropped silently |
| src/superclaude/cli/install_retired_mcp.py:320-324 | pipeline_config | notice only when a retired entry is classified `remove`; else None |
| src/superclaude/cli/install_retired_mcp.py:251-256 | pipeline_config | `_codegraph_ready_now` exception → False |
| src/superclaude/cli/main.py:472-499 | pipeline_config | doctor details shown only with `--verbose` |
| src/superclaude/cli/doctor.py:160-186 | pipeline_config | codegraph check fails only when the registered command is not executable; missing registration / unreadable config / version mismatch stay passed=True |
| src/superclaude/cli/doctor.py:229-234 | pipeline_config | retired-MCP warning lives in the check name (visible), passed always True |
| src/superclaude/hooks/scripts/codegraph-session-start.sh:11 | env_var | SUPERCLAUDE_CODEGRAPH_AUTOINIT=0 → exit 0 silently |
| src/superclaude/hooks/scripts/codegraph-session-start.sh:12-19 | env_var | empty HOME or no executable codegraph → exit 0 silently |
| src/superclaude/hooks/scripts/codegraph-session-start.sh:21-25 | env_var | CLAUDE_PROJECT_DIR/$PWD not a repo, $HOME, /, or existing db → exit 0 silently |
| src/superclaude/hooks/scripts/codegraph-session-start.sh:27-31 | env_var | init output only to ${XDG_STATE_HOME:-$HOME/.local/state}/superclaude/codegraph-init.log |
| src/superclaude/hooks/hooks.json:24-29 | file | SessionStart matcher "startup" only, timeout 5 |
| src/superclaude/cli/install_mcp.py:720-726 | env_var | CLAUDE_CONFIG_DIR="" → lookup unknown (doctor detail, verbose-only) |
| src/superclaude/cli/doctor.py:167-175 | env_var | PATH decides the only visible codegraph failure |
| src/superclaude/core/CODEGRAPH.md:11 | env_var | SUPERCLAUDE_CODEGRAPH_PRIMITIVES not read by update/doctor/hook |

## Reachability

- reaches_sink: main.py:360, 364, 366, 371, 373, 378, 379, 384, 385, 389, 394, 395, 398, 400, 403, 405; main.py:413 and install_retired_mcp.py:323 only when a removable legacy entry exists; main.py:488, 495, 507, 509; doctor.py:231.
- filtered_out (needs --verbose): doctor.py:162, 164 ("no codegraph registration; run `superclaude install`"), 172 (detail; the fail mark itself reaches), 183, 193, 201, 209, 211, 233; main.py:499.
- filtered_out (by design): codegraph-session-start.sh:11, :31.
- unknown: install_retired_mcp.py:370-493 (not on the update path; not inspected).
