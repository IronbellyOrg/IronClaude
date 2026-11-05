# Wave 1.6 Branch B (log-config inspection), returned by troubleshoot-analyst, persisted on receipt

degraded: true (no shell; Grep/Glob/Read only)

## Hits
| location | config_type | effective level | note |
|---|---|---|---|
| src/superclaude/hooks/hooks.json:87-93 | file | timeout=3s, sync | exit-2 decision takes effect (no async key) |
| plugins/superclaude/hooks/hooks.json:57-63 | file | timeout=3s, sync | matches src |
| .dev/tasks/done/TASK-WF-implementIronbel-20261104-130647/artifacts/t7-settings.json:9 | file | unknown | test registration pointing at the src script |
| src/superclaude/hooks/scripts/block-bare-python.sh:52 | pipeline_config | `set -u` only | no pipefail: WORD pipeline status is awk's |
| src/superclaude/hooks/scripts/block-bare-python.sh:266-267 | pipeline_config | stderr -> /dev/null | empty input exits 0 silently |
| src/superclaude/hooks/scripts/block-bare-python.sh:270 | pipeline_config | jq stderr -> /dev/null | invalid JSON fails open silently |
| src/superclaude/hooks/scripts/block-bare-python.sh:271 | env_var | LC_ALL=C for awk | only env var set; awk stderr discarded; `|| WORD=""` fails open |
| src/superclaude/hooks/scripts/block-bare-python.sh:9-13 | pipeline_config | allow=0, block=stderr+2, never 1 | repo contract |
| pyproject.toml:107-116 | file | addopts -v --strict-markers --tb=short | does not affect hook stderr |
| tests/hooks/test_block_bare_python.py:32-41 | pipeline_config | capture_output=True, timeout=10 | tests capture hook output themselves |

## Reachability verdicts
| site | verdict | rationale |
|---|---|---|
| block-bare-python.sh:278-279 (block message, exit 2) | reaches_sink | shown to the model on exit 2 (external semantics) |
| block-bare-python.sh:54-56 (jq fail-open) | filtered_out | stderr with exit 0 not shown to the model |
| block-bare-python.sh:58-60 (awk fail-open) | filtered_out | same exit-0 path |
| block-bare-python.sh:111 (awk `print b`) | filtered_out | data channel captured into WORD; no other scanner state emitted |
