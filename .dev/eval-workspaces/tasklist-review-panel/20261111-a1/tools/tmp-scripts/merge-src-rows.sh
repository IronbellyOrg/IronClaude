#!/usr/bin/env bash
set -u
EVAL=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1
PKGS="TASK-WF-designSpec-20261107-075614 TASK-WF-makeTheAliasOnly-20261105-051649 TASK-WF-design-20261108-041415"
# combo -> reviewer specs "rid:model"
declare -A ROWS=(
  [sol-alone-src]="t2-1:gpt-6.1-sol"
  [terra-alone-src]="t2-1:gpt-6.1-terra"
  [n2-sonnet-src]="t2b-1:muse-wonder-1.0 t4-1:claude-haiku-5-5 t4-2:grok-4.7 t1b-1:claude-sonnet-5-5"
  [n4-sonnet-src]="t2b-1:muse-wonder-1.0 t4-1:claude-haiku-5-5 t1b-1:claude-sonnet-5-5"
  [n5-sonnet-src]="t2b-1:muse-wonder-1.0 t4-1:gpt-6-luna t1b-1:claude-sonnet-5-5"
  [r2-sonnet-src]="t4-1:claude-haiku-5-5 t3-1:claude-haiku-5-5 t4-2:grok-4.7 t1b-1:claude-sonnet-5-5"
  [r1-haiku-luna2-src]="t4-1:claude-haiku-5-5 t4-2:gpt-6-luna t3-1:gpt-6-luna"
  [n2-muse-haiku-grok-src]="t2b-1:muse-wonder-1.0 t4-1:claude-haiku-5-5 t4-2:grok-4.7"
  [n5-muse-luna-src]="t2b-1:muse-wonder-1.0 t4-1:gpt-6-luna"
  [r3-luna2-grok-src]="t4-1:gpt-6-luna t3-1:gpt-6-luna t4-2:grok-4.7"
  [c3-luna-grok-src]="t4-1:gpt-6-luna t4-2:grok-4.7"
  [n3-muse-luna-grok-src]="t2b-1:muse-wonder-1.0 t4-1:gpt-6-luna t4-2:grok-4.7"
  [b4-terra-muse-haiku]="t2-1:gpt-6.1-terra t2b-1:muse-wonder-1.0 t4-1:claude-haiku-5-5"
  [b4-terra-luna-muse]="t2-1:gpt-6.1-terra t2b-1:muse-wonder-1.0 t4-1:gpt-6-luna"
  [b4-sonnet-luna2]="t1b-1:claude-sonnet-5-5 t4-1:gpt-6-luna t3-1:gpt-6-luna"
  [b4-sonnet-terra]="t1b-1:claude-sonnet-5-5 t2-1:gpt-6.1-terra"
  [b4-muse-luna2]="t2b-1:muse-wonder-1.0 t4-1:gpt-6-luna t3-1:gpt-6-luna"
)
declare -A TIER; TIER[t1b-1]=tier1b; TIER[t2-1]=tier2; TIER[t2b-1]=tier2b; TIER[t3-1]=tier3; TIER[t4-1]=tier4; TIER[t4-2]=tier4
declare -A ALIAS; ALIAS[t1b-1]="claude-gw-tier1b[1m]"; ALIAS[t2-1]="claude-gw-tier2[1m]"; ALIAS[t2b-1]="claude-gw-tier2b[1m]"; ALIAS[t3-1]="claude-gw-tier3[1m]"; ALIAS[t4-1]="claude-gw-tier4[1m]"; ALIAS[t4-2]="claude-gw-tier4[1m]"
for C in "${!ROWS[@]}"; do
  for P in $PKGS; do
    # skip b4-muse-luna2 until its 2 muse retries land
    if [ "$C" = "b4-muse-luna2" ]; then continue; fi
    D="$EVAL/combos/$C/$P"; mkdir -p "$D"
    # skip if already merged
    [ -f "$D/merged-1.md" ] && { echo "skip $C/$P"; continue; }
    # build resolution
    REV="["
    first=1
    for spec in ${ROWS[$C]}; do
      rid="${spec%%:*}"; model="${spec#*:}"
      [ $first = 0 ] && REV="$REV,"
      REV="$REV{\"reviewer_id\":\"$rid\",\"model\":\"$model\",\"alias\":\"${ALIAS[$rid]}\",\"tier\":\"${TIER[$rid]}\",\"strategy\":\"fixed\",\"stand_in\":false,\"fallback_depth\":0,\"fallbacks\":[],\"launch\":null,\"seed\":null,\"slot_id\":\"${rid%%-*}\"}"
      first=0
    done
    REV="$REV]"
    jq -c --argjson rev "$REV" '.reviewers=$rev' "$EVAL/$P/resolution-live7.json" > "$D/resolution.json"
    # verify model_ok + files exist for all reviewers
    ok=1
    ARGS=()
    for spec in ${ROWS[$C]}; do
      rid="${spec%%:*}"; model="${spec#*:}"
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
