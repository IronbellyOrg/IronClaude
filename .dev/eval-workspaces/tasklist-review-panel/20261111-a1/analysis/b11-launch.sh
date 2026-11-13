#!/usr/bin/env bash
# Batch 11 (owner order 2026-11-13 13:43 UTC): sonnet + 2x luna, 5 replicates, one independent runner process ("session") per replicate, NOFALLBACK=1.
set -u
DS=TASK-WF-designSpec-20261107-075614; AL=TASK-WF-makeTheAliasOnly-20261105-051649; DE=TASK-WF-design-20261108-041415
for rep in 1 2 3 4 5; do
  J=/tmp/b11-jobs-r$rep.txt; : > $J
  for p in $DS $AL $DE; do
    c=j1-sonnet-luna2-r$rep
    echo "$p t1b-1 claude-sonnet-5-5 $c" >> $J; echo "$p t4-1 gpt-6-luna $c" >> $J; echo "$p t3-1 gpt-6-luna $c" >> $J
  done
  nohup bash -c "export NOFALLBACK=1; xargs -P 2 -L 1 bash /tmp/b4-job-one.sh < $J >> /tmp/b11-r$rep.log 2>&1; echo R${rep}_DONE >> /tmp/b11-r$rep.log" >/dev/null 2>&1 &
  echo "session r$rep launched (9 runs)"
done
