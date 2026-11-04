# Wave 1.6 Branch A (round 3), returned by troubleshoot-analyst, persisted on receipt
degraded: true; captured_bytes null
| file:line | call_type | note |
|---|---|---|
| src/superclaude/hooks/scripts/block-bare-python.sh:130 | print | only scanner output: matched basename; cmd[o] (line 128) never printed |
| src/superclaude/hooks/scripts/block-bare-python.sh:332 | exception_handler (silent) | awk stderr -> /dev/null; `|| WORD=""` |
| src/superclaude/hooks/scripts/block-bare-python.sh:331 | exception_handler (silent) | jq stderr -> /dev/null |
| src/superclaude/hooks/scripts/block-bare-python.sh:327 | exception_handler (silent) | stdin errors swallowed |
| src/superclaude/hooks/scripts/block-bare-python.sh:336 | silent allow | the {fd} miss looks like a correct allow |
| src/superclaude/hooks/scripts/block-bare-python.sh:339-340 | logger_call / exit 2 | block message names the matched word (the python3() false block) |
| src/superclaude/hooks/scripts/block-bare-python.sh:65, :69 | logger_call | fail-open notices, not on the symptom path |
| tests/hooks/test_block_bare_python.py:202-206 | assertion | block assertions |
| tests/hooks/test_block_bare_python.py:212-213 | assertion | allow assertions |
observability: blocked path visible through stderr; allowed path needs a scanner copy (already run by the parent: trace-probe.out).
