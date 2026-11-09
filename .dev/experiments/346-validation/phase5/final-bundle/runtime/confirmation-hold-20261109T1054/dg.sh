#!/usr/bin/env bash
# Coordinator-run diffgate steps (S-begin, S-check, S-fixcheck), run in the replicate worktree.
# usage: dg.sh begin <N> | check <N> <report> | fixcheck <N> <disposition>
# Exit: 0 = continue; 20 = early terminal PASS (pause); other non-zero = stop for the coordinator.
set -u
DIR=.dev/orca-command-refactor/review/diffgate-loop
DOC=.dev/orca-command-refactor/specs/orca-worker-contract-spec.md
SC="uv run --no-project python $HOME/.claude/skills/sc-diffgate/scripts/diffgate.py"
cmd="$1"; N="$2"
case "$cmd" in
  begin)
    $SC begin --dir $DIR --doc $DOC --expect-round $N; rc=$?
    echo "S-begin r$N exit=$rc"; exit $rc;;
  check)
    rep="$3"
    checkout=$DIR/coordinator-check-r$N.json
    $SC check --dir $DIR --report $rep > "$checkout"; rc=$?
    head -c 1500 "$checkout"; echo
    if [ $rc -eq 1 ]; then
      if jq -e '[.. | objects | select(has("rule") and .structural == true)] | length > 0' "$checkout" >/dev/null 2>&1; then echo "STRUCTURAL failure"; exit 31; fi
      retryout=$DIR/coordinator-check-r$N-retry.json
      echo "finding-level errors: re-running check once"; $SC check --dir $DIR --report $rep > "$retryout"; rc=$?; head -c 1500 "$retryout"; echo
    fi
    [ $rc -eq 0 ] || { echo "S-check r$N exit=$rc"; exit $rc; }
    [ -f $DIR/close-r$N.md ] || { echo "missing close-r$N.md"; exit 32; }
    printf '\n' >> $rep; cat $DIR/close-r$N.md >> $rep
    echo "appended close-r$N.md to $rep; last line: $(tail -n 1 $rep)"
    if tail -n 1 $rep | grep -q "verdict: PASS"; then echo "EARLY TERMINAL PASS at review $N"; exit 20; fi
    exit 0;;
  fixcheck)
    disp="$3"
    $SC fixcheck --dir $DIR --doc $DOC --map $disp; rc=$?
    echo "S-fixcheck r$N exit=$rc"; exit $rc;;
esac
