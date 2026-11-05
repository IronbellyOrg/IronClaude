# Wave 1.5 Branch C (round 3), returned by troubleshoot-analyst, persisted on receipt
| source_file | line | quoted_text (abridged verbatim) | applies_to |
|---|---|---|---|
| src/superclaude/hooks/scripts/block-bare-python.sh | 9-14 | "allow -> exit 0; block -> one message on stderr + exit 2; never exit 1. ... blocks only when the scanner positively reports a bare command word." | contract |
| .dev/tasks/done/TASK-WF-implementIronbel-20261104-130647/TASK-WF-implementIronbel-20261104-130647.md | 21 | "...bash plus `jq` ... never exit 1, and fail open ... The hook itself must not run Python." | language, exit codes |
| .dev/tasks/done/TASK-WF-implementIronbel-20261104-130647/TASK-WF-implementIronbel-20261104-130647.md | 39 | "Block when the command word's basename is exactly `python`, `python3`, `pip` or `pip3`." | block rule |
| src/superclaude/hooks/scripts/block-bare-python.sh | 59-60 | "Known false positive: a word that is not a command but sits in command position, for example a heredoc body fed to a shell that only echoes text." | accepted false positives |
| tests/hooks/test_block_bare_python.py | 101 | "\"function-body\": \"f() { python3 x.py; }\"," | python3 inside a function body must stay blocked |
| src/superclaude/hooks/scripts/block-bare-python.sh | 28-30 | "...the keywords if/then/elif/else/do/while/until/!/{ (like [[, case and function, a keyword only when unquoted and unescaped, as in bash)..." | command-position rules |
| .dev/tasks/done/TASK-WF-implementIronbel-20261104-130647/TASK-WF-implementIronbel-20261104-130647.md | 41 | "Tokenising is done in `jq` ... or `awk` ... 100 KB ... well under the 3-second registration timeout." | performance |
| .dev/tasks/done/TASK-WF-implementIronbel-20261104-130647/TASK-WF-implementIronbel-20261104-130647.md | 46 | "...byte-identical (`cmp` exits 0)." | mirror |
degraded: false
