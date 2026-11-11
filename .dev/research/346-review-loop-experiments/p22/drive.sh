#!/bin/bash
# one cycle: fill free slots, then advance both arms; print LAUNCH/MANUAL/LOST lines. The Jev key is sourced inside the j3 subshell only.
SP=/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad
cd $SP/p22 && python3 slotter.py 2>&1 | grep -E "SLOT|ALL SLOTS DONE|Traceback|rror"
for d in pn1c pn1j; do
  [ -d $SP/p22/$d/runs ] || continue
  ( [ $d = pn1j ] && { set -a; . $SP/.jev.env; set +a; }
    cd $SP/p22/$d && uv run --no-project python advance.py 2>&1 | grep -v UV_NATIVE | grep -E "LAUNCH|MANUAL|LOST|lost|WARN|Traceback|rror" | sed "s#$SP/##")
done
