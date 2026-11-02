| # | Primitive | Asserted behaviour | Defining artifact | Fetch query | Status |
|---|---|---|---|---|---|
| 1 | `superclaude update` / `superclaude install` (this repo's CLI) | update never runs the codegraph phase or the retire step; install (with or without --force) runs both | src/superclaude/cli/main.py:340-429 and :242-267 (function bodies) | the code that implements "update never runs the codegraph phase or the retire step" | fetched:source (Read this run) + observed: tests/cli/test_update_command.py:318-333 passed |
