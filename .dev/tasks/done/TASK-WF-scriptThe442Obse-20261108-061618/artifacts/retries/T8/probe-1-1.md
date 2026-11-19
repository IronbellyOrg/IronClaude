13ed148d783a90f2b81912b67370f1371efd856a

# Family probe probe-1-1.md (failing review r1-1)

## family: store-diff-timing
defect form: a quoted "diff right after step N" that is printed before the step's own removals.
search command: grep -n 'store_diff' .dev/issues/442/scripts/cleanup.sh
before-output (touched files):
  cleanup.sh:47: store_diff definition
  cleanup.sh:64: the only diff in step 2, before the removal loops
  cleanup.sh:157: the diff in step 7 (correct, immediately before the removal)
coupled sites: the plan-mode path of step 2 (no removals happen, so no second diff); cleanup-selftest.sh needs a case that reads the post-removal diff.
after: step 2 re-runs both diffs after the removal loops (apply only) and prints them under "after step 2".

## family: swallowed-failure
defect form: an action wrapper that turns a failed command into success, so a step reports OK and a later step deletes the record needed to retry.
search command: grep -n -e '|| true' -e '^act()' -e 'act ' -e 'line [0-9] OK' .dev/issues/442/scripts/cleanup.sh
before-output (touched files):
  cleanup.sh:30-31: act with "$@" || true
  cleanup.sh:42: act pkill (exit 1 means no process matched, a normal result)
  cleanup.sh:70: act rm of a session file; :80 line 2 OK
  cleanup.sh:89-90: act git config --unset; :91 line 3 OK
  cleanup.sh:128 and 134: act gh_fork pr close and issue close; :137 line 5 OK
  cleanup.sh:154 (plan) and 163: act rm -rf OB; :164 line 7 OK "removed"
  cleanup.sh:34, 40, 48: other || true are reads that may legitimately be empty
coupled sites: line() counts only REFUSED; step 7's gate; step 4 already reports its own refusal.
after: act counts a failed command in ACTFAIL (act_soft for pkill); line() counts REFUSED and FAIL; steps 2, 3, 5 and 7 print FAIL when ACTFAIL grew during the step; step 7 refuses while ACTFAIL or REFUSED is above 0, and prints removed only when the folder is gone.
