# P5 gate G-1 (Step 5.9)

- Command: `uv run pytest tests/issue_watch/ -v` (raw output `p5-g1-raw.txt`)
- Result: **PASSED**, exit 0; 1372 passed, 0 failed, 0 errors
- Summary line: `============================= 1372 passed in 2.69s =============================`
- Fixes recorded: the fixture-count pin in `test_github.py` was raised from 14 to 16 for the two Orca fixtures of Step 5.2, and the "every fixture is read by a test" check (DF-32) was changed to scan every `test_*.py` of the suite instead of only its own file.
