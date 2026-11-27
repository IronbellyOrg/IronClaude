#!/bin/bash
# usage: run_chain.sh <chain-name> ; scenarios are read from /tmp/createQuestionEv-scratch/chain-<chain-name>.tsv
# columns (tab separated): name depth mode type q c k description
SC=/tmp/createQuestionEv-scratch
chain=$1
log=$SC/logs/chain-$chain.log
: > $log
while IFS=$'\t' read -r name depth mode type q c k desc; do
  [ -z "$name" ] && continue
  echo "$(date -u +%FT%TZ) pre-run review of pending items" >> $log
  uv run --no-project python $SC/review_pending.py "before $name" >> $log 2>&1 || { echo "$(date -u +%FT%TZ) HELD before $name" >> $log; exit 2; }
  echo "$(date -u +%FT%TZ) start $name" >> $log
  $SC/run_one.sh "$name" "$depth" "$mode" "$type" "$q" "$c" "$k" "$desc"
  tail -2 $SC/logs/$name.out >> $log
  if ! tail -1 $SC/logs/$name.out | grep -q 'exit=0'; then echo "$(date -u +%FT%TZ) $name did not exit 0: chain stops" >> $log; exit 3; fi
  uv run --no-project python $SC/review_pending.py "$name" >> $log 2>&1 || { echo "$(date -u +%FT%TZ) HELD after $name" >> $log; exit 2; }
done < $SC/chain-$chain.tsv
echo "$(date -u +%FT%TZ) chain $chain complete" >> $log
