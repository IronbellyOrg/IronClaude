#!/usr/bin/env bash
# superclaude review merge for one row-package (DESIGN 5.2; merge-b11.sh:11-34). Writes pkg-status.json merge fields.
# usage: merge.sh <row> <pkg>; exit = merge exit code (3 when every reviewer is invalid)
set -u -o pipefail
ROW=$1; PKG=$2
R5=$(cd "$(dirname "$0")/.." && pwd); OUTR=${R5_OUT:-$R5}
EVAL=${R5_EVAL:-$(cd "$R5/../../20261111-a1" && pwd)}
D=$OUTR/runs/$ROW/$PKG
declare -A TIER; TIER[t1b-1]=tier1b; TIER[t2-1]=tier2; TIER[t2b-1]=tier2b; TIER[t3-1]=tier3; TIER[t4-1]=tier4; TIER[t4-2]=tier4
declare -A ALIAS; ALIAS[t1b-1]="claude-gw-tier1b[1m]"; ALIAS[t2-1]="claude-gw-tier2[1m]"; ALIAS[t2b-1]="claude-gw-tier2b[1m]"; ALIAS[t3-1]="claude-gw-tier3[1m]"; ALIAS[t4-1]="claude-gw-tier4[1m]"; ALIAS[t4-2]="claude-gw-tier4[1m]"
status() { # <merge status> <rc>
  local f=$D/pkg-status.json; [ -f "$f" ] || echo '{}' > "$f"
  jq --arg m "$1" --argjson rc "$2" --argjson inv "$(printf '%s\n' "${INVALID[@]:-}" | jq -R 'select(length>0)' | jq -s .)" \
    '.merge=$m|.merge_rc=$rc|.invalid=$inv' "$f" > "$f.tmp" && mv "$f.tmp" "$f"
}
REV="["; first=1; ARGS=(); INVALID=()
while read -r rid model; do
  [ $first = 0 ] && REV="$REV,"
  REV="$REV{\"reviewer_id\":\"$rid\",\"model\":\"$model\",\"alias\":\"${ALIAS[$rid]}\",\"tier\":\"${TIER[$rid]}\",\"strategy\":\"fixed\",\"stand_in\":false,\"fallback_depth\":0,\"fallbacks\":[],\"launch\":null,\"seed\":null,\"slot_id\":\"${rid%%-*}\"}"
  first=0
  M=$D/reviews/$rid.meta.json
  if [ -f "$M" ] && [ "$(jq -r .model_ok "$M")" = true ]; then ARGS+=(--report "$rid=$D/reviews/$rid.md"); else INVALID+=("$rid"); fi
done < <(jq -r '.models|to_entries[]|"\(.key) \(.value)"' "$D/run.json")
REV="$REV]"
jq -c --argjson rev "$REV" '.reviewers=$rev' "$EVAL/$PKG/resolution-live7.json" > "$D/resolution.json"
if [ ${#ARGS[@]} -eq 0 ]; then status merge_skipped_all_invalid 3; exit 3; fi
"${SUPERCLAUDE:-superclaude}" review merge --ledger "$D/ledger.json" --doc "$EVAL/$PKG/candidate.md" --round 1 "${ARGS[@]}" \
  --resolution "$D/resolution.json" --out "$D/merged-1.md" > "$D/merge-stdout.txt" 2>&1
rc=$?
if [ $rc -eq 0 ] && [ -f "$D/merged-1.md" ]; then status ok 0; else status merge_refused $rc; fi
exit $rc
