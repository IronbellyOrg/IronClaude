#!/bin/bash
# drive-jev.sh: like $SP/drive.sh, for p15 experiments; sources the key inside the subshell only.
SP=/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad
for d in "$@"; do
  echo "== $d"
  (set -a; . "$SP/.jev.env"; set +a; cd "$SP/$d" && uv run --no-project python advance.py 2>&1 \
    | grep -v UV_NATIVE | grep -E "LAUNCH|RUNNING|ALL DONE|MANUAL|rror|WARN|lost|JEV" | sed "s#$SP/##" | head -20)
done
