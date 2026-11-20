ead53a8a2644bd9e8c6f5e44f0b826018cc00c5c
family detail-echo: a ConfigError detail built from text read out of the file
command: git grep -n -e "sorted(map(str" -e "_invalid(f" -- src/superclaude/cli/issue_watch/defaults.py
before: defaults.py joined the unknown key names into the detail
coupled sites: none other in defaults.py (every other detail is a fixed string)
after: the unknown-key detail is the fixed text "it holds an unknown key"
