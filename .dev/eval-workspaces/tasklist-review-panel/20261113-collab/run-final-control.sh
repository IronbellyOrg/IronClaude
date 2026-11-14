#!/usr/bin/env bash
# Owner approval 2026-11-14 ("approve the final batch"), part 2: 6 runs of the plain ember + 2x luna panel with the ORIGINAL launch path of the
# 20261111-a1 evaluation (run-reviewer.sh per reviewer -> superclaude review merge -> anonymise -> blind Opus judge with the old judge-one.sh),
# NOT the collaboration designs' launchers. Question it answers: is the same-harness baseline (about 1 of 14) the real level of this panel, or
# is it the earlier 1.83? Combo dirs h1-ember-luna2-r1..r6 (new names; existing combos untouched). Reviewer ids as in b4-muse-ember-luna2:
# t2b-1 = muse-ember-1.0, t4-1 = gpt-6-luna, t3-1 = gpt-6-luna. Opus is used only by the blind judge. NOFALLBACK=1. Resumable.
set -u -o pipefail
EVAL=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1
C0=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261113-collab
L=$C0/replicate-logs; mkdir -p "$L/done"
export NOFALLBACK=1
PKGS="TASK-WF-designSpec-20261107-075614 TASK-WF-makeTheAliasOnly-20261105-051649 TASK-WF-design-20261108-041415"
M='{"t2b-1":"muse-ember-1.0","t4-1":"gpt-6-luna","t3-1":"gpt-6-luna"}'
echo "START $(date -u +%T)"
for n in 1 2 3 4 5 6; do
  C=h1-ember-luna2-r$n
  [ -e "$L/done/control-$C" ] && { echo "SKIP $C"; continue; }
  echo "START $C $(date -u +%T)"
  for P in $PKGS; do
    mkdir -p "$EVAL/combos/$C/$P"
    # three reviewers of one package at once (as the earlier ember rows did)
    for spec in "t2b-1 muse-ember-1.0" "t4-1 gpt-6-luna" "t3-1 gpt-6-luna"; do
      set -- $spec
      [ -s "$EVAL/$P/reviews/combos/$C/$1.md" ] || bash "$EVAL/tools/run-reviewer.sh" "$EVAL" "$P" "$1" "$2" "combos/$C" >"$L/control-$C-$P-$1.log" 2>&1 &
    done
    wait
    jq --argjson m "$M" '.reviewers |= [ .[] | select(.reviewer_id as $i | $m|has($i)) | .model = $m[.reviewer_id] ]' "$EVAL/$P/resolution-live7.json" > "$EVAL/combos/$C/$P/resolution.json"
    R="$EVAL/$P/reviews/combos/$C"
    superclaude review merge --ledger "$EVAL/combos/$C/$P/ledger.json" --doc "$EVAL/$P/candidate.md" --round 1 \
      --report t2b-1="$R/t2b-1.md" --report t4-1="$R/t4-1.md" --report t3-1="$R/t3-1.md" \
      --resolution "$EVAL/combos/$C/$P/resolution.json" --out "$EVAL/combos/$C/$P/merged-1.md" >"$EVAL/combos/$C/$P/merge-stdout.txt" 2>&1
    echo "merge $C $P rc=$?"
  done
  # anonymise (same steps as tools/tmp-scripts/anon-b8.sh), then judge
  for P in $PKGS; do
    SRC="$EVAL/combos/$C/$P/merged-1.md"; [ -f "$SRC" ] || { echo "NO MERGE $C $P"; continue; }
    D="$EVAL/arms/scoring/combos/$C/$P"; mkdir -p "$D"
    while :; do Lb=$(printf 'Q\nR\nS\nT\nU\nV\n' | shuf -n1); [ ! -d "$D/$Lb" ] && break; done
    DD="$D/$Lb"; mkdir -p "$DD"; echo "{\"label\":\"$Lb\",\"combo\":\"$C\"}" > "$D/label-key.json"
    sed "s|$EVAL|<EVAL>|g" "$SRC" > "$DD/merged-anon.md"
    i=1; for ID in $(grep -oE '\bt[0-9a-z]+-[0-9]+\b' "$SRC" | sort -u); do sed -i "s/\b$ID\b/R$i/g" "$DD/merged-anon.md"; i=$((i+1)); done
    sed -i 's|^candidate: <EVAL>/[^ ]*/candidate.md sha256|candidate: <candidate file> sha256|' "$DD/merged-anon.md"
    sed -i 's|report <EVAL>/[^ ,]*|report <redacted>|g' "$DD/merged-anon.md"
    bash "$EVAL/tools/tmp-scripts/judge-one.sh" "$C" "$P" "$Lb" >"$L/control-$C-$P-judge.log" 2>&1
    cat "$L/control-$C-$P-judge.log" | tail -1
  done
  touch "$L/done/control-$C"
  echo "END $C $(date -u +%T)"
done
echo "ALLDONE $(date -u +%T)"
