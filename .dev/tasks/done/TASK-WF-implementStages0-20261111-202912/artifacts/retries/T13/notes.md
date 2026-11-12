b09d48f8b5aacc528ef2022e87add02402daf90a
A1 r1-1 F1.1 minor src/superclaude/cli/review/verify_cmd.py:47 ac=scope n,n,n,n snapshot membership compares raw strings, so a citation path like src/./a.py against a snapshot listing src/a.py is flagged missing-file; effect is an extra re-read only
