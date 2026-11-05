# Wave 1.6 Branch B (round 2), returned by troubleshoot-analyst, persisted on receipt
degraded: true (static reading only)
| location | config_type | effective level / note |
|---|---|---|
| src/superclaude/hooks/hooks.json:86-95 | file | matcher Bash, timeout 3, sync |
| plugins/superclaude/hooks/hooks.json:56-65 | file | same as src |
| .claude/settings.json | file | no block-bare-python registration (installed ~/.claude registration only) |
| src/superclaude/hooks/scripts/block-bare-python.sh:59 | pipeline_config | `set -u` only |
| src/superclaude/hooks/scripts/block-bare-python.sh:61-68 | pipeline_config | jq / awk missing -> one stderr line, exit 0 |
| src/superclaude/hooks/scripts/block-bare-python.sh:317-318 | pipeline_config | stdin read errors swallowed; empty input exits 0 |
| src/superclaude/hooks/scripts/block-bare-python.sh:321 | pipeline_config | jq stderr -> /dev/null |
| src/superclaude/hooks/scripts/block-bare-python.sh:322 | env_var | LC_ALL=C for awk only; awk stderr -> /dev/null; `|| WORD=""` |
| src/superclaude/hooks/scripts/block-bare-python.sh:324-327 | pipeline_config | any other WORD -> exit 0, no output |
| src/superclaude/hooks/scripts/block-bare-python.sh:125 | pipeline_config | only scanner output: print of matched basename |
## Reachability verdicts
| site | verdict |
|---|---|
| src/superclaude/hooks/scripts/block-bare-python.sh:329-330 block message | reaches_sink (not reached for the three symptom inputs) |
| src/superclaude/hooks/scripts/block-bare-python.sh:62 jq fail-open | unknown (cannot fire: jq present) |
| src/superclaude/hooks/scripts/block-bare-python.sh:66 awk fail-open | unknown (cannot fire: awk present) |
| src/superclaude/hooks/scripts/block-bare-python.sh:125 matched-word print | filtered_out (captured into WORD; misses and crashes both end as silent exit 0) |
