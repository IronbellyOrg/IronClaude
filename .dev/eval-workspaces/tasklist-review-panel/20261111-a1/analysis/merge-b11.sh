#!/usr/bin/env bash
set -u
EVAL=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1
PKGS="TASK-WF-designSpec-20261107-075614 TASK-WF-makeTheAliasOnly-20261105-051649 TASK-WF-design-20261108-041415"
declare -A ROWS
ROWS[j1-sonnet-luna2-r1]="t1b-1:claude-sonnet-5-5 t4-1:gpt-6-luna t3-1:gpt-6-luna"
ROWS[j1-sonnet-luna2-r2]="t1b-1:claude-sonnet-5-5 t4-1:gpt-6-luna t3-1:gpt-6-luna"
ROWS[j1-sonnet-luna2-r3]="t1b-1:claude-sonnet-5-5 t4-1:gpt-6-luna t3-1:gpt-6-luna"
ROWS[j1-sonnet-luna2-r4]="t1b-1:claude-sonnet-5-5 t4-1:gpt-6-luna t3-1:gpt-6-luna"
ROWS[j1-sonnet-luna2-r5]="t1b-1:claude-sonnet-5-5 t4-1:gpt-6-luna t3-1:gpt-6-luna"
declare -A TIER; TIER[t1b-1]=tier1b; TIER[t2-1]=tier2; TIER[t2b-1]=tier2b; TIER[t3-1]=tier3; TIER[t4-1]=tier4; TIER[t4-2]=tier4
declare -A ALIAS; ALIAS[t1b-1]="claude-gw-tier1b[1m]"; ALIAS[t2-1]="claude-gw-tier2[1m]"; ALIAS[t2b-1]="claude-gw-tier2b[1m]"; ALIAS[t3-1]="claude-gw-tier3[1m]"; ALIAS[t4-1]="claude-gw-tier4[1m]"; ALIAS[t4-2]="claude-gw-tier4[1m]"
for C in "${!ROWS[@]}"; do
  for P in $PKGS; do
    D="$EVAL/combos/$C/$P"; mkdir -p "$D"
    [ -f "$D/merged-1.md" ] && { echo "skip $C/$P"; continue; }
    REV="["; first=1
    for spec in ${ROWS[$C]}; do
      rid="${spec%%:*}"; model="${spec#*:}"
      [ $first = 0 ] && REV="$REV,"
      REV="$REV{\"reviewer_id\":\"$rid\",\"model\":\"$model\",\"alias\":\"${ALIAS[$rid]}\",\"tier\":\"${TIER[$rid]}\",\"strategy\":\"fixed\",\"stand_in\":false,\"fallback_depth\":0,\"fallbacks\":[],\"launch\":null,\"seed\":null,\"slot_id\":\"${rid%%-*}\"}"
      first=0
    done
    REV="$REV]"
    jq -c --argjson rev "$REV" '.reviewers=$rev' "$EVAL/$P/resolution-live7.json" > "$D/resolution.json"
    ok=1; ARGS=()
    for spec in ${ROWS[$C]}; do
      rid="${spec%%:*}"
      M="$EVAL/$P/reviews/combos/$C/$rid.meta.json"; F="${M%.meta.json}.md"
      if [ ! -f "$M" ] || [ "$(jq -r .model_ok "$M")" != "true" ]; then ok=0; echo "BADMETA $C/$P/$rid"; fi
      ARGS+=(--report "$rid=$F")
    done
    [ $ok = 1 ] || continue
    superclaude review merge --ledger "$D/ledger.json" --doc "$EVAL/$P/candidate.md" --round 1 "${ARGS[@]}" --resolution "$D/resolution.json" --out "$D/merged-1.md" > "$D/merge-stdout.txt" 2>&1
    rc=$?
    if [ $rc -ne 0 ] && grep -q 'expects round 2' "$D/merge-stdout.txt" 2>/dev/null; then
      mkdir -p "$D/stale-r1"; mv "$D/ledger.json" "$D/stale-r1/" 2>/dev/null; mv "$D/merged-1.md" "$D/stale-r1/" 2>/dev/null
      superclaude review merge --ledger "$D/ledger.json" --doc "$EVAL/$P/candidate.md" --round 1 "${ARGS[@]}" --resolution "$D/resolution.json" --out "$D/merged-1.md" > "$D/merge-stdout.txt" 2>&1; rc=$?
    fi
    echo "$C/$P rc=$rc verdict=$(grep -m1 '^verdict:' "$D/merged-1.md" 2>/dev/null | awk '{print $2}')"
  done
done
