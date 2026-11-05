# Wave 1.5 Branch C (round 2), returned by troubleshoot-analyst, persisted on receipt
| source_file | line | quoted_text (abridged verbatim) | applies_to |
|---|---|---|---|
| src/superclaude/hooks/scripts/block-bare-python.sh | 9-14 | "allow -> exit 0; block -> one message on stderr + exit 2; never exit 1. ... blocks only when the scanner positively reports a bare command word. The hook itself runs no Python." | exit-code / fail-open contract |
| .dev/tasks/done/TASK-WF-implementIronbel-20261104-130647/TASK-WF-implementIronbel-20261104-130647.md | 21 | "...never exit 1, and fail open (exit 0) ... The hook itself must not run Python." | language and exit codes |
| .dev/tasks/done/TASK-WF-implementIronbel-20261104-130647/TASK-WF-implementIronbel-20261104-130647.md | 32 | "Copy it byte-for-byte to `plugins/superclaude/hooks/scripts/block-bare-python.sh` (mode 0755)." | mirror |
| tests/cli/test_install_hooks.py | 783-785 | "assert source.read_bytes() == mirror.read_bytes()" | mirror test |
| .dev/tasks/done/TASK-WF-implementIronbel-20261104-130647/TASK-WF-implementIronbel-20261104-130647.md | 41 | "Tokenising is done in `jq` ... or `awk`, not a per-character bash loop, so a 100 KB command is checked in well under the 3-second registration timeout." | performance |
| tests/hooks/test_block_bare_python.py | 233-238 | "assert elapsed < 1" (100 KB case) | performance test |
| src/superclaude/hooks/scripts/block-bare-python.sh | 16-18 | "...pipes it, on stdin, to one stateful awk scanner (never through awk -v or the environment...)" | input path |
| src/superclaude/hooks/scripts/block-bare-python.sh | 21-25 | "...process substitution, case patterns, array assignments, [[ ]] tests (their words, including ( and | in =~ patterns, are not commands, but $( ) inside them is scanned)..." | documented behaviour the defects contradict |
| .dev/tasks/done/TASK-WF-implementIronbel-20261104-130647/TASK-WF-implementIronbel-20261104-130647.md | 37 | "Text inside single quotes, and text inside double quotes, is never a command word ... Backslash escapes outside single quotes are honoured when tracking quotes." | quoted/escaped [[ is literal |
| tests/cli/test_install_hooks.py | 771-774 | "assert hook == {\"type\": \"command\", \"command\": _BLOCK_BARE_PYTHON_HOOK, \"timeout\": 3}" | registration, 3 s limit |
degraded: false
