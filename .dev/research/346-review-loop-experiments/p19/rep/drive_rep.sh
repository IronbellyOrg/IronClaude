#!/bin/bash
# one cycle: fill free slots, then advance both arms; print LAUNCH/MANUAL/LOST lines
SP=/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad
cd $SP/p19/rep && python3 slotter.py 2>&1 | grep -E "SLOT|ALL SLOTS DONE|Traceback|rror"
for d in pn1o pn1d2; do
  [ -d $SP/p19/rep/$d/runs ] || continue
  (cd $SP/p19/rep/$d && uv run --no-project python advance.py 2>&1 | grep -v UV_NATIVE | grep -E "LAUNCH|MANUAL|LOST|lost|WARN|Traceback" | sed "s#$SP/##")
done
