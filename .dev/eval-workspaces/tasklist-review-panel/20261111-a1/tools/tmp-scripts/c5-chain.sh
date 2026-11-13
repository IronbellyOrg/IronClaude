#!/usr/bin/env bash
EVAL=$1; RID=$2; MODEL=$3
for P in TASK-WF-designSpec-20261107-075614 TASK-WF-makeTheAliasOnly-20261105-051649 TASK-WF-design-20261108-041415; do
  bash $EVAL/tools/run-reviewer.sh $EVAL $P $RID $MODEL combos/c5-glm-haiku
  echo "done $P $RID"
done
echo CHAIN_DONE $RID
