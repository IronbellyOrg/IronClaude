# Wave 1.5 Branch C (semantic restrictions), returned by troubleshoot-analyst, persisted on receipt

| source_file | line | quoted_text | applies_to |
|---|---|---|---|
| .dev/tasks/done/TASK-WF-implementIronbel-20261104-130647/TASK-WF-implementIronbel-20261104-130647.md | 21 | "...block with a message on stderr and exit 2, allow with exit 0, never exit 1, and fail open (exit 0) when `jq` is missing, the input is not valid JSON, the tool is not `Bash`, or `tool_input.command` is absent or empty. The hook itself must not run Python." | exit-code / fail-open contract |
| src/superclaude/hooks/scripts/block-bare-python.sh | 10 | "allow -> exit 0; block -> one message on stderr + exit 2; never exit 1." | header contract |
| src/superclaude/hooks/scripts/block-bare-python.sh | 13 | "blocks only when the scanner positively reports a bare command word." | scanner fail-open |
| src/superclaude/hooks/scripts/block-bare-python.sh | 14 | "The hook itself runs no Python." | no Python in hook |
| .dev/tasks/done/.../TASK-WF-implementIronbel-20261104-130647.md | 19 | "...does not block commands that only mention python in arguments, paths or quoted text; tests cover both the blocked and the allowed cases, including commands chained with `&&`, `;` and `|`" | Done-when allowed cases (defect 3 breaks it) |
| .dev/tasks/done/.../TASK-WF-implementIronbel-20261104-130647.md | 37 | "Text inside single quotes, and text inside double quotes, is never a command word ... Backslash escapes outside single quotes are honoured when tracking quotes." | quote handling (decoding must not turn quoted text into a command word) |
| .dev/tasks/done/.../TASK-WF-implementIronbel-20261104-130647.md | 38 | "the wrappers `sudo`, `exec`, `nohup`, `time`, `nice`, `env` (plus its following options and `NAME=value` words), `timeout` (plus its options and its duration argument) and `command` (only when not followed by `-v` or `-V` ...)" | wrapper skipping (defect 2 source rule) |
| .dev/tasks/done/.../TASK-WF-implementIronbel-20261104-130647.md | 39 | "Block when the command word's basename is exactly `python`, `python3`, `pip` or `pip3`." | block criterion |
| .dev/tasks/done/.../TASK-WF-implementIronbel-20261104-130647.md | 46 | "...exist, are executable, and are byte-identical (`cmp` exits 0)." | plugin mirror |
| tests/cli/test_install_hooks.py | 785 | "assert source.read_bytes() == mirror.read_bytes()" | mirror test |
| .dev/tasks/done/.../TASK-WF-implementIronbel-20261104-130647.md | 41 | "Tokenising is done in `jq` ... or `awk`, not a per-character bash loop, so a 100 KB command is checked in well under the 3-second registration timeout." | performance |
| tests/hooks/test_block_bare_python.py | 204 | "assert elapsed < 1" | 100 KB under 1 s |
| tests/hooks/test_block_bare_python.py | 208 | "Above the 128 KB single-argument limit: the command must still be scanned (AMD-06)." | stdin input path |

degraded: true (Grep/Read; auggie not available)
