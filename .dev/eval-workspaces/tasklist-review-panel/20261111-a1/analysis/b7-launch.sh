#!/usr/bin/env bash
# Batch 7: six ember/luna/haiku/grok combos (owner order 2026-11-12 19:38 UTC). Streams: ember -P4, other -P6 (10 concurrent, 4 muse max).
set -u
DS=TASK-WF-designSpec-20261107-075614
AL=TASK-WF-makeTheAliasOnly-20261105-051649
DE=TASK-WF-design-20261108-041415
EMBER=/tmp/b7-ember.txt; OTHER=/tmp/b7-other.txt; : > "$EMBER"; : > "$OTHER"
add() { case "$4" in muse-ember-1.0) echo "$2 $3 $4 $1" >> "$EMBER";; *) echo "$2 $3 $4 $1" >> "$OTHER";; esac }
for p in $DS $AL $DE; do
  # e1 grok + ember + luna
  add e1-grok-ember-luna $p t4-2 grok-4.7; add e1-grok-ember-luna $p t2b-1 muse-ember-1.0; add e1-grok-ember-luna $p t4-1 gpt-6-luna
  # e2 ember + 2x luna (same multiset as b4-muse-ember-luna2: a fresh replication)
  add e2-ember-luna2-rep $p t2b-1 muse-ember-1.0; add e2-ember-luna2-rep $p t4-1 gpt-6-luna; add e2-ember-luna2-rep $p t3-1 gpt-6-luna
  # e3 2x ember + luna
  add e3-ember2-luna $p t2b-1 muse-ember-1.0; add e3-ember2-luna $p t3-1 muse-ember-1.0; add e3-ember2-luna $p t4-1 gpt-6-luna
  # e4 2x haiku + ember
  add e4-haiku2-ember $p t4-1 claude-haiku-5-5; add e4-haiku2-ember $p t3-1 claude-haiku-5-5; add e4-haiku2-ember $p t2b-1 muse-ember-1.0
  # e5 haiku + ember + luna
  add e5-haiku-ember-luna $p t4-1 claude-haiku-5-5; add e5-haiku-ember-luna $p t2b-1 muse-ember-1.0; add e5-haiku-ember-luna $p t3-1 gpt-6-luna
  # e6 haiku + 2x ember
  add e6-haiku-ember2 $p t4-1 claude-haiku-5-5; add e6-haiku-ember2 $p t2b-1 muse-ember-1.0; add e6-haiku-ember2 $p t3-1 muse-ember-1.0
done
echo "ember jobs: $(wc -l < $EMBER), other jobs: $(wc -l < $OTHER)"
nohup bash -c 'xargs -P 4 -L 1 bash /tmp/b4-job-one.sh < /tmp/b7-ember.txt >> /tmp/b7-ember.log 2>&1; echo EMBER7_DONE >> /tmp/b7-ember.log' >/dev/null 2>&1 &
nohup bash -c 'xargs -P 6 -L 1 bash /tmp/b4-job-one.sh < /tmp/b7-other.txt >> /tmp/b7-other.log 2>&1; echo OTHER7_DONE >> /tmp/b7-other.log' >/dev/null 2>&1 &
echo "launched batch 7"
