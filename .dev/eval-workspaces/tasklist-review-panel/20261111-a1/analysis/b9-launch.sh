#!/usr/bin/env bash
# Batch 9 (owner order 2026-11-12 22:16 UTC): haiku+2luna+2ember (h1) and sonnet+2luna+2ember (h2), 4 replicates x 3 packages.
set -u
DS=TASK-WF-designSpec-20261107-075614; AL=TASK-WF-makeTheAliasOnly-20261105-051649; DE=TASK-WF-design-20261108-041415
EMBER=/tmp/b9-ember.txt; OTHER=/tmp/b9-other.txt; : > "$EMBER"; : > "$OTHER"
add() { case "$4" in muse-ember-1.0) echo "$2 $3 $4 $1" >> "$EMBER";; *) echo "$2 $3 $4 $1" >> "$OTHER";; esac }
EM=muse-ember-1.0; LU=gpt-6-luna; HA=claude-haiku-5-5; SO=claude-sonnet-5-5
for rep in 1 2 3 4; do for p in $DS $AL $DE; do
  c=h1-haiku-luna2-ember2-r$rep; add $c $p t2-1 $HA; add $c $p t4-1 $LU; add $c $p t4-2 $LU; add $c $p t2b-1 $EM; add $c $p t3-1 $EM
  c=h2-sonnet-luna2-ember2-r$rep; add $c $p t1b-1 $SO; add $c $p t4-1 $LU; add $c $p t4-2 $LU; add $c $p t2b-1 $EM; add $c $p t3-1 $EM
done; done
echo "ember jobs: $(wc -l < $EMBER), other jobs: $(wc -l < $OTHER)"
nohup bash -c 'xargs -P 4 -L 1 bash /tmp/b4-job-one.sh < /tmp/b9-ember.txt >> /tmp/b9-ember.log 2>&1; echo EMBER9_DONE >> /tmp/b9-ember.log' >/dev/null 2>&1 &
nohup bash -c 'xargs -P 6 -L 1 bash /tmp/b4-job-one.sh < /tmp/b9-other.txt >> /tmp/b9-other.log 2>&1; echo OTHER9_DONE >> /tmp/b9-other.log' >/dev/null 2>&1 &
echo "launched batch 9"
