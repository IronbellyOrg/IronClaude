VERDICT: PASS - AC2 satisfied; ruff format --check src/ tests/ exits 0.

Note: required one manual refactor in `src/superclaude/cli/prd/prompts.py` (build_gap_filling_prompt) — ruff format wanted to use double-outer-quotes for a nested f-string that contained inner double-quoted dict access, which is invalid Python 3.10 (added in 3.12). Refactored by extracting `failure["area"][:20]` to a `failure_area_slug` local variable so the nested f-string has no inner double quotes. Behavior preserved.
