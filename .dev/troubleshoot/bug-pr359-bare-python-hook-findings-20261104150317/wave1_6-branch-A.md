# Wave 1.6 Branch A (log-call inspection), returned by troubleshoot-analyst, persisted on receipt

degraded: true (Grep/Read only; captured_bytes null, none supplied)

| file:line | construct | call_type | level | snippet | richness | distance |
|---|---|---|---|---|---|---|
| src/superclaude/hooks/scripts/block-bare-python.sh:54 | suppression | exception_handler | n/a | `if ! command -v jq >/dev/null 2>&1; then` | silent | module |
| src/superclaude/hooks/scripts/block-bare-python.sh:55 | echo | print | stderr | `echo "block-bare-python: jq not found; allowing the command (fail open)." >&2` | | module |
| src/superclaude/hooks/scripts/block-bare-python.sh:56 | exit | exception_handler | n/a | `exit 0` | rich | module |
| src/superclaude/hooks/scripts/block-bare-python.sh:58 | suppression | exception_handler | n/a | `if ! command -v awk >/dev/null 2>&1; then` | silent | module |
| src/superclaude/hooks/scripts/block-bare-python.sh:59 | echo | print | stderr | awk-missing fail-open message | | module |
| src/superclaude/hooks/scripts/block-bare-python.sh:60 | exit | exception_handler | n/a | `exit 0` | rich | module |
| src/superclaude/hooks/scripts/block-bare-python.sh:111 | awk_print | print | stdout | `if (b == "python" \|\| ...) { print b; exit }` | | in_function |
| src/superclaude/hooks/scripts/block-bare-python.sh:101 | silent state transition | exception_handler | n/a | `if (wrap[o] == "timeout") { wrap[o] = "timeout-duration"; return }` | silent | in_function |
| src/superclaude/hooks/scripts/block-bare-python.sh:206 | silent state transition | exception_handler | n/a | `if (c == "\\") { i++; addc(o, substr(s, i, 1)); return }` | silent | in_function |
| src/superclaude/hooks/scripts/block-bare-python.sh:190-191 | silent state transition | exception_handler | n/a | `pushc("par")` for every `(` outside case/array | silent | in_function |
| src/superclaude/hooks/scripts/block-bare-python.sh:266 | suppression | exception_handler | n/a | `INPUT="$(cat 2>/dev/null \|\| true)"` | silent | module |
| src/superclaude/hooks/scripts/block-bare-python.sh:267 | exit | exception_handler | n/a | `[ -n "$INPUT" ] \|\| exit 0` | silent | module |
| src/superclaude/hooks/scripts/block-bare-python.sh:270 | suppression | exception_handler | n/a | jq `2>/dev/null` | silent | caller |
| src/superclaude/hooks/scripts/block-bare-python.sh:271 | suppression | exception_handler | n/a | `\| LC_ALL=C awk "$SCANNER" 2>/dev/null)" \|\| WORD=""` | silent | caller |
| src/superclaude/hooks/scripts/block-bare-python.sh:275 | exit | exception_handler | n/a | `*) exit 0 ;;` | silent | caller |
| src/superclaude/hooks/scripts/block-bare-python.sh:278 | echo | print | stderr | `echo "UV-ONLY BLOCK: ... \`$WORD\` ..." >&2` | | caller |
| src/superclaude/hooks/scripts/block-bare-python.sh:279 | exit | print | n/a | `exit 2` | | caller |
| tests/hooks/test_block_bare_python.py:39 | capture | error_reporter_init | n/a | `capture_output=True` | | caller |
| tests/hooks/test_block_bare_python.py:154 | assertion | error_reporter_init | stderr | `assert result.returncode == 2, result.stderr.decode()` | minimal | caller |
| tests/hooks/test_block_bare_python.py:164 | assertion | error_reporter_init | stderr | `assert result.returncode == 0, ...; assert result.stderr == b""` | rich | caller |
| tests/hooks/test_block_bare_python.py:190 | assertion | error_reporter_init | stderr | jq-not-found marker assert | rich | caller |

Coverage gaps (worker): no `$'\NNN'` case in command position; no wrapper long option with a separate argument; no `[[ ... =~ ... ]]` allowed case.

Direct observation without edit: partly. The only scanner output is line 111 (a matching word). Seeing the word picked on a wrong allow needs a copy of the scanner that also prints `cmd[o]` at line 109 (the hook itself unchanged). Pending observation proposed: expected `30` (timeout input), `160ython3` (ANSI-C input), `[[` then `python` (=~ input).
