# Wave 1.6 Branch A (round 2), returned by troubleshoot-analyst, persisted on receipt
degraded: true; captured_bytes null
| file:line | call_type | note |
|---|---|---|
| src/superclaude/hooks/scripts/block-bare-python.sh:125 | print | only output: matched basename; other chosen words leave no trace |
| src/superclaude/hooks/scripts/block-bare-python.sh:313 | print | END flush via endword |
| src/superclaude/hooks/scripts/block-bare-python.sh:322 | exception_handler (silent) | awk stderr -> /dev/null; `|| WORD=""` |
| src/superclaude/hooks/scripts/block-bare-python.sh:321 | exception_handler (silent) | jq stderr -> /dev/null |
| src/superclaude/hooks/scripts/block-bare-python.sh:317-318 | exception_handler (silent) | stdin errors swallowed; empty input exit 0 |
| src/superclaude/hooks/scripts/block-bare-python.sh:326 | exit (silent) | the observed wrong allow |
| src/superclaude/hooks/scripts/block-bare-python.sh:329-330 | logger_call / exit 2 | expected block signal, absent in the symptom |
| src/superclaude/hooks/scripts/block-bare-python.sh:62, :66 | logger_call | fail-open notices, not on the symptom path |
| tests/hooks/test_block_bare_python.py:188-192 | assertion | block assertions; the three inputs are not in BLOCKED |
| tests/hooks/test_block_bare_python.py:198-199 | assertion | allow assertions (exit 0, empty stderr) |
observable_without_edit: no from the hook itself; proposed scratch-copy trace = already run by the parent (trace-probe.out).
