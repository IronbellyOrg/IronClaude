#!/usr/bin/env bash
# Batch 8 (owner order 2026-11-12 20:37 UTC): 8 requested combos + ember+luna 1x baseline, 4 replicates each, 3 packages.
# Rep-major job order so every replicate completes early. Streams: ember -P4, other -P6.
set -u
DS=TASK-WF-designSpec-20261107-075614
AL=TASK-WF-makeTheAliasOnly-20261105-051649
DE=TASK-WF-design-20261108-041415
EMBER=/tmp/b8-ember.txt; OTHER=/tmp/b8-other.txt; : > "$EMBER"; : > "$OTHER"
add() { case "$4" in muse-ember-1.0) echo "$2 $3 $4 $1" >> "$EMBER";; *) echo "$2 $3 $4 $1" >> "$OTHER";; esac }
EM=muse-ember-1.0; LU=gpt-6-luna; TE=gpt-6.1-terra; HA=claude-haiku-5-5; SO=claude-sonnet-5-5
for rep in 1 2 3 4; do for p in $DS $AL $DE; do
  c=g1-ember-luna2-r$rep;      add $c $p t2b-1 $EM; add $c $p t4-1 $LU; add $c $p t3-1 $LU
  c=g2-sonnet-ember-r$rep;     add $c $p t1b-1 $SO; add $c $p t2b-1 $EM
  c=g3-sonnet-luna-ember-r$rep; add $c $p t1b-1 $SO; add $c $p t4-1 $LU; add $c $p t2b-1 $EM
  c=g4-haiku-ember-terra-r$rep; add $c $p t4-1 $HA; add $c $p t2b-1 $EM; add $c $p t2-1 $TE
  c=g5-ember2-luna-r$rep;      add $c $p t2b-1 $EM; add $c $p t3-1 $EM; add $c $p t4-1 $LU
  c=g6-luna2-ember2-r$rep;     add $c $p t4-1 $LU; add $c $p t4-2 $LU; add $c $p t2b-1 $EM; add $c $p t3-1 $EM
  c=g7-haiku-luna2-r$rep;      add $c $p t4-1 $HA; add $c $p t3-1 $LU; add $c $p t4-2 $LU
  c=g8-ember-terra-r$rep;      add $c $p t2b-1 $EM; add $c $p t2-1 $TE
  c=g9-ember-luna-r$rep;       add $c $p t2b-1 $EM; add $c $p t4-1 $LU
done; done
echo "ember jobs: $(wc -l < $EMBER), other jobs: $(wc -l < $OTHER)"
nohup bash -c 'xargs -P 4 -L 1 bash /tmp/b4-job-one.sh < /tmp/b8-ember.txt >> /tmp/b8-ember.log 2>&1; echo EMBER8_DONE >> /tmp/b8-ember.log' >/dev/null 2>&1 &
nohup bash -c 'xargs -P 6 -L 1 bash /tmp/b4-job-one.sh < /tmp/b8-other.txt >> /tmp/b8-other.log 2>&1; echo OTHER8_DONE >> /tmp/b8-other.log' >/dev/null 2>&1 &
echo "launched batch 8"
