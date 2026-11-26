#!/bin/bash
# Pilot arm merges (Step 2). Creates catfix copies (originals untouched),
# arm resolutions, and runs superclaude review merge for arms A/B/C on the
# three pilot packages. Idempotent-safe: refuses to overwrite existing merged-1.md.
set -u
EVAL=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1
PKGS="TASK-WF-designSpec-20261107-075614 TASK-WF-makeTheAliasOnly-20261105-051649 TASK-WF-design-20261108-041415"

for P in $PKGS; do
  R="$EVAL/$P/reviews"
  # 1. catfix copies for finals containing unpassable-ac
  for f in "$R"/t*.md; do
    case "$f" in *attempt*|*catfix*) continue;; esac
    if grep -q 'unpassable-ac' "$f"; then
      if [ ! -f "$f.catfix.md" ]; then sed 's/unpassable-ac/unpassable-check/g' "$f" > "$f.catfix.md"; echo "catfix: $(basename "$f")"; fi
    fi
  done
  # 2. arm resolutions
  for ARM in A B C; do
    D="$EVAL/arms/$ARM/$P"; mkdir -p "$D"
    case $ARM in
      A) jq '.reviewers = [.reviewers[] | select(.reviewer_id == "t1b-1")]' "$EVAL/$P/resolution-default.json" > "$D/resolution.json" ;;
      B) jq '.reviewers = [.reviewers[] | select(.model != "Qwen3.8-max")]' "$EVAL/$P/resolution-default.json" > "$D/resolution.json" ;;
      C) jq '.reviewers = [.reviewers[] | select(.model != "Qwen3.8-max")]' "$EVAL/$P/resolution-live7.json" > "$D/resolution.json" ;;
    esac
  done
done

# 3. merges
for P in $PKGS; do
  R="$EVAL/$P/reviews"
  for ARM in A B C; do
    D="$EVAL/arms/$ARM/$P"
    [ -f "$D/merged-1.md" ] && { echo "skip $ARM/$P (exists)"; continue; }
    ARGS=()
    while IFS= read -r RID; do
      F="$R/$RID.md"
      [ -f "$R/$RID.md.catfix.md" ] && F="$R/$RID.md.catfix.md"
      [ -f "$F" ] || { echo "MISSING $RID for $ARM/$P"; continue; }
      ARGS+=(--report "$RID=$F")
    done < <(jq -r '.reviewers[].reviewer_id' "$D/resolution.json")
    superclaude review merge --ledger "$D/ledger.json" --doc "$EVAL/$P/candidate.md" \
      --round 1 "${ARGS[@]}" --resolution "$D/resolution.json" --out "$D/merged-1.md" \
      > "$D/merge-stdout.txt" 2>&1
    RC=$?
    V=$(grep -m1 '^verdict:' "$D/merged-1.md" 2>/dev/null || echo "NO_VERDICT")
    ROWS=$(grep -c '^| ' "$D/merged-1.md" 2>/dev/null || echo 0)
    echo "$ARM/$P rc=$RC $V"
  done
done
echo DONE
