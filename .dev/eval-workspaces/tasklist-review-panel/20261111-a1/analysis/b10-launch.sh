#!/usr/bin/env bash
# Batch 10 (owner order 2026-11-13 00:28 UTC): i1 grok+sonnet, i2 haiku+sonnet, 4 replicates x 3 packages = 48 runs. No ember; one stream -P10.
set -u
DS=TASK-WF-designSpec-20261107-075614; AL=TASK-WF-makeTheAliasOnly-20261105-051649; DE=TASK-WF-design-20261108-041415
J=/tmp/b10-jobs.txt; : > "$J"
SO=claude-sonnet-5-5; GR=grok-4.7; HA=claude-haiku-5-5
for rep in 1 2 3 4; do for p in $DS $AL $DE; do
  echo "$p t4-2 $GR i1-grok-sonnet-r$rep" >> $J; echo "$p t1b-1 $SO i1-grok-sonnet-r$rep" >> $J
  echo "$p t4-1 $HA i2-haiku-sonnet-r$rep" >> $J; echo "$p t1b-1 $SO i2-haiku-sonnet-r$rep" >> $J
done; done
echo "jobs: $(wc -l < $J)"
nohup bash -c 'xargs -P 10 -L 1 bash /tmp/b4-job-one.sh < /tmp/b10-jobs.txt >> /tmp/b10.log 2>&1; echo B10_DONE >> /tmp/b10.log' >/dev/null 2>&1 &
echo "launched batch 10"
