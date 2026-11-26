#!/usr/bin/env bash
# Batch 4: source.md impact study. Serial, one reviewer at a time.
set -u
EVAL=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1
RR="$EVAL/tools/run-reviewer.sh"
DS=TASK-WF-designSpec-20261107-075614
AL=TASK-WF-makeTheAliasOnly-20261105-051649
DE=TASK-WF-design-20261108-041415

run() { # pkg rid model combo
  echo "START $(date -u +%T) $4/$1/$2=$3"
  bash "$RR" "$EVAL" "$1" "$2" "$3" "combos/$4"
  echo "END $(date -u +%T) $4/$1/$2 $(jq -c '[.observed_model,.model_ok,.findings_block]' "$EVAL/$1/reviews/combos/$4/$2.meta.json" 2>/dev/null)"
}

# Row 1: sol alone (3 runs)
for p in $DS $AL $DE; do run "$p" t2-1 gpt-6.1-sol sol-alone-src; done
# Rows 2-5: sonnet rows with source.md (4 reviewers x 3 pkgs each)
declare -A ROWS=(
  [n2-sonnet-src]="t2b-1=muse-wonder-1.0 t4-1=claude-haiku-5-5 t4-2=grok-4.7 t1b-1=claude-sonnet-5-5"
  [n4-sonnet-src]="t2b-1=muse-wonder-1.0 t3-1=glm-5.3 t4-1=claude-haiku-5-5 t1b-1=claude-sonnet-5-5"
  [n5-sonnet-src]="t2b-1=muse-wonder-1.0 t3-1=glm-5.3 t4-1=gpt-6-luna t1b-1=claude-sonnet-5-5"
  [r2-sonnet-src]="t4-1=claude-haiku-5-5 t3-1=claude-haiku-5-5 t4-2=grok-4.7 t1b-1=claude-sonnet-5-5"
)
for C in n2-sonnet-src n4-sonnet-src n5-sonnet-src r2-sonnet-src; do
  for p in $DS $AL $DE; do
    for spec in ${ROWS[$C]}; do
      rid="${spec%%=*}"; model="${spec#*=}"
      run "$p" "$rid" "$model" "$C"
    done
  done
done
# Rows 6-8: top-3 cheap combos with source.md
declare -A TOP=(
  [r1-haiku-luna2-src]="t4-1=claude-haiku-5-5 t4-2=gpt-6-luna t3-1=gpt-6-luna"
  [n2-muse-haiku-grok-src]="t2b-1=muse-wonder-1.0 t4-1=claude-haiku-5-5 t4-2=grok-4.7"
  [n5-muse-glm-luna-src]="t2b-1=muse-wonder-1.0 t3-1=glm-5.3 t4-1=gpt-6-luna"
)
for C in r1-haiku-luna2-src n2-muse-haiku-grok-src n5-muse-glm-luna-src; do
  for p in $DS $AL $DE; do
    for spec in ${TOP[$C]}; do
      rid="${spec%%=*}"; model="${spec#*=}"
      run "$p" "$rid" "$model" "$C"
    done
  done
done
echo ALLDONE
