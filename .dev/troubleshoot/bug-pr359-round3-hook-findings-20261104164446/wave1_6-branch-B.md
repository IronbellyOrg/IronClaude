# Wave 1.6 Branch B (round 3), returned by troubleshoot-analyst, persisted on receipt
degraded: true (static reading)
| location | type | note |
|---|---|---|
| src/superclaude/hooks/hooks.json:87-93 / plugins/superclaude/hooks/hooks.json:57-63 | file | matcher Bash, timeout 3, sync |
| .claude/settings.json, ~/.claude/settings.json | file | no block-bare-python registration found by grep |
| src/superclaude/hooks/scripts/block-bare-python.sh:62 | pipeline_config | set -u only |
| src/superclaude/hooks/scripts/block-bare-python.sh:327-328 | pipeline_config | stdin errors swallowed; empty input exit 0 |
| src/superclaude/hooks/scripts/block-bare-python.sh:331-332 | pipeline_config | jq and awk stderr -> /dev/null; `|| WORD=""` |
| src/superclaude/hooks/scripts/block-bare-python.sh:332 | env_var | LC_ALL=C for awk only |
| src/superclaude/hooks/scripts/block-bare-python.sh:334-337 | pipeline_config | case filter: other words exit 0 silently |
## Reachability
| emitter | verdict |
|---|---|
| block message src/superclaude/hooks/scripts/block-bare-python.sh:339-340 | reaches_sink (reached for python3() false block) |
| jq/awk fail-open src/superclaude/hooks/scripts/block-bare-python.sh:64-70 | unknown |
| matched-word print src/superclaude/hooks/scripts/block-bare-python.sh:130 | reaches_sink indirectly for python3(); never emitted for {fd}> miss |
Mechanism notes (worker): python3() — endword at "(" prints before the "()" check at line 219; {fd} — line 206 tests ^[0-9]+$ only, so {fd} becomes the command word.
Parent check: src, plugins mirror and .claude dev copy are byte-identical (cmp).
