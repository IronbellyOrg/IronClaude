#!/bin/bash
cd /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/clones/pn2
OUT=/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab2/offline
uv run pytest -q -rf tests/skills tests/cli tests/unit 2>&1 | grep -E "^FAILED|passed|failed" > $OUT/fail-after.txt
git stash -u -q
uv run pytest -q -rf tests/skills tests/cli tests/unit 2>&1 | grep -E "^FAILED|passed|failed" > $OUT/fail-before.txt
git stash pop -q
echo finished > $OUT/prefail.done
