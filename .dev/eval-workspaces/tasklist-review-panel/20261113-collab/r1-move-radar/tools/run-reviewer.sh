#!/usr/bin/env bash
# run-reviewer.sh <row> <pkg> <rid> <model> <collab 0|1> <T0_MS> [--root R1] [--sb SB]
# run-reviewer.sh --print-cmd <row> <pkg> <rid> <model> <collab 0|1> <T0_MS> [--root R1] [--sb SB]
# R1's reviewer launcher (DESIGN.md section 2.7): H1 brief, H3/H4 sandbox cwd, hang guard, one isolated retry,
# H2 normalise + at most one re-ask. No fallback model, ever. Reads runs/<row>/<pkg>/run.json (HANG_MS, role, T_report)
# and, with collab 1, runs/<row>/<pkg>/settings/<rid>.json. Writes runs/<row>/<pkg>/reviews/<rid>.*.
# Exit 0 = valid reviewer, 1 = INVALID, 2 = refused before running.
set -u -o pipefail
REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
TOOLS=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
R1=$(dirname "$TOOLS")
SB=/tmp/evalsb-collab-r1
PRINT=0; [ "${1:-}" = --print-cmd ] && { PRINT=1; shift; }
[ $# -ge 6 ] || { echo "usage: run-reviewer.sh [--print-cmd] <row> <pkg> <rid> <model> <collab 0|1> <T0_MS>" >&2; exit 2; }
ROW=$1; PKG=$2; RID=$3; MODEL=$4; COLLAB=$5; T0=$6; shift 6
while [ $# -gt 0 ]; do case $1 in --root) R1=$2; shift 2;; --sb) SB=$2; shift 2;; *) echo "bad arg $1" >&2; exit 2;; esac; done
case $COLLAB in 0|1) ;; *) echo "REFUSE collab must be 0 or 1" >&2; exit 2;; esac
[ $PRINT = 1 ] || [ "${NOFALLBACK:-}" = 1 ] || { echo "REFUSE NOFALLBACK must be 1" >&2; exit 2; }
D=$R1/runs/$ROW/$PKG; OUT=$D/reviews; RUNJ=$D/run.json
[ -f "$RUNJ" ] || { echo "REFUSE no $RUNJ" >&2; exit 2; }
HANG_MS=$(jq -r .HANG_MS "$RUNJ"); ROLE=$(jq -r --arg r "$RID" '.role[$r] // empty' "$RUNJ")
TREP=$(jq -r --arg r "$ROLE" '.T_report[$r] // 0' "$RUNJ")
[ -n "$ROLE" ] || { echo "REFUSE $RID has no role in run.json" >&2; exit 2; }
CAND=$SB/cand/$PKG/candidate.md; SRC=$SB/cand/$PKG/source.md; CWD=$SB/$PKG/repo
BRIEF=$(cat "$R1/config/brief.txt")
BRIEF=${BRIEF//@@CAND@@/$CAND}; BRIEF=${BRIEF//@@SRC@@/$SRC}
BRIEF=${BRIEF//@@SHA@@/$(sha256sum "$CAND" | cut -d' ' -f1)}; BRIEF=${BRIEF//@@SRCSHA@@/$(sha256sum "$SRC" | cut -d' ' -f1)}
SETTINGS=""; [ "$COLLAB" = 1 ] && SETTINGS=$(cat "$D/settings/$RID.json")
now() { date +%s%3N; }
build_argv() { # build_argv <attempt> <hang_left_s>: attempt 1 carries --settings (collab 1); attempt 2 never does
  A=(timeout --kill-after=5 "$2" claude -p --model "$MODEL" --output-format json --permission-mode bypassPermissions
     --disallowedTools Edit Write NotebookEdit)
  if [ "$1" = 1 ] && [ -n "$SETTINGS" ]; then A+=(--settings "$SETTINGS"); fi
}
if [ $PRINT = 1 ]; then
  build_argv 1 $(( (HANG_MS - $(now)) / 1000 ))
  printf '%s\n' "${A[@]}" | jq -R . | jq -s -c --arg cwd "$CWD" --arg stdin "$BRIEF" '{cwd:$cwd, argv:., stdin:$stdin}'
  exit 0
fi

mkdir -p "$OUT"
START_MS=$(now); SIDS=(); ARGVS=(); HANG=false; WALLS=(); TOKS=()
sids_json() { if [ ${#SIDS[@]} -eq 0 ]; then echo '[]'; else printf '%s\n' "${SIDS[@]}" | jq -R . | jq -s -c .; fi; }
partial_meta() { # session ids are written as soon as they are known (R-46, K-7)
  jq -n -c --arg rid "$RID" --argjson s "$(sids_json)" --argjson st "$START_MS" '{reviewer_id:$rid, session_ids:$s, start_ms:$st, partial:true}' > "$OUT/$RID.meta.json"
}
partial_meta
run_attempt() { # run_attempt <n>; returns 0 when model_ok && block_ok && no API error
  local a=$1 left s rc w obs tok tokall apierr mok bok sid lo le
  left=$(( (HANG_MS - $(now)) / 1000 ))
  if [ "$left" -le 0 ]; then HANG=true; return 1; fi
  build_argv "$a" "$left"
  ARGVS+=("$(printf '%s\n' "${A[@]}" | jq -R . | jq -s -c .)")
  s=$(now)
  ( cd "$CWD" && "${A[@]}" <<<"$BRIEF" ) > "$OUT/$RID.attempt$a.json" 2> "$OUT/$RID.attempt$a.err"
  rc=$?; w=$(( $(now) - s ))
  { [ $rc = 124 ] || [ $rc = 137 ]; } && HANG=true
  jq -r '[.[]|select(.type=="result")|.result]|.[0] // ""' "$OUT/$RID.attempt$a.json" > "$OUT/$RID.attempt$a.md" 2>/dev/null
  obs=$(jq -r '[.[]|select(.type=="assistant" and (.parent_tool_use_id==null))|.message.model]|unique|join(",")' "$OUT/$RID.attempt$a.json" 2>/dev/null)
  tok=$(jq '[.[]|select(.type=="result")|.usage.output_tokens]|.[0] // 0' "$OUT/$RID.attempt$a.json" 2>/dev/null)
  tokall=$(jq '[.[]|select(.type=="result")|.modelUsage|to_entries[]|.value.outputTokens]|add // 0' "$OUT/$RID.attempt$a.json" 2>/dev/null)
  sid=$(jq -r '[.[]|select(.type=="result")|.session_id]|.[0] // empty' "$OUT/$RID.attempt$a.json" 2>/dev/null)
  [ -n "$sid" ] && { SIDS+=("$sid"); SID=$sid; partial_meta; }
  apierr=false; grep -q 'API Error' "$OUT/$RID.attempt$a.md" 2>/dev/null && apierr=true
  lo=$(echo "$obs" | tr 'A-Z' 'a-z'); le=$(echo "$MODEL" | tr 'A-Z' 'a-z')
  mok=false; [ -n "$obs" ] && [ "$obs" != "<synthetic>" ] && { [ "$lo" = "$le" ] || [ "$lo" = "$le-build" ]; } && mok=true
  bok=false; grep -q '^```findings-v1' "$OUT/$RID.attempt$a.md" 2>/dev/null && bok=true
  WALLS+=("$w"); TOKS+=("${tokall:-0}")
  jq -n --arg rid "$RID" --arg exp "$MODEL" --arg obs "$obs" --argjson mok $mok --argjson bok $bok --argjson att "$a" \
    --argjson w "$(( w / 1000 ))" --argjson wms "$w" --argjson tok "${tok:-0}" --argjson tokall "${tokall:-0}" --argjson rc "$rc" \
    --argjson api $apierr --arg sid "$sid" \
    '{reviewer_id:$rid,expected_model:$exp,observed_model:$obs,model_ok:$mok,findings_block:$bok,attempt:$att,wall_s:$w,
      wall_ms:$wms,output_tokens_main:$tok,output_tokens_all:$tokall,exit:$rc,api_error:$api,session_id:$sid}' > "$OUT/$RID.attempt$a.meta.json"
  $mok && $bok && ! $apierr
}

SID=""; OK=false; ATT=1; RETRY_S=null; ISO=false
run_attempt 1 && OK=true
if ! $OK && [ $(( HANG_MS - $(now) )) -ge 30000 ]; then  # R-44: one isolated retry, same model, no --settings
  ATT=2; [ "$COLLAB" = 1 ] && ISO=true
  s=$(now); run_attempt 2 && OK=true; RETRY_S=$(jq -n "($(now) - $s) / 1000")
fi

# H2 (R-02): normalise; at most one re-ask on the same session when the block still has parser errors
DROPPED=0; REASK_S=null; REASK_TOK=0; REASK_MS=0
h2() { (cd "$REPO" && uv run python "$TOOLS/h2_normalize.py" "$1" "$2" "$3") >/dev/null 2>&1; }
if $OK; then
  h2 "$OUT/$RID.attempt$ATT.md" "$OUT/$RID.norm.md" "$OUT/$RID.h2.json"
  if [ "$(jq -r .ok "$OUT/$RID.h2.json")" != true ] && [ -n "$SID" ] \
     && [ $(( HANG_MS - $(now) )) -ge "$(jq -n "1000 * (6 + $TREP) | floor")" ]; then
    ERRS=$(jq -r '.errors[] | "line \(.line): \(.msg)"' "$OUT/$RID.h2.json")
    PROMPT="Your findings-v1 block has these parser errors:
$ERRS
Reply with the complete corrected report, ending with the ## Findings block and the final verdict line."
    left=$(( (HANG_MS - $(now)) / 1000 ))
    R=(timeout --kill-after=5 "$left" claude -p --resume "$SID" --model "$MODEL" --output-format stream-json --verbose
       --permission-mode bypassPermissions --disallowedTools Edit Write NotebookEdit)
    ARGVS+=("$(printf '%s\n' "${R[@]}" | jq -R . | jq -s -c .)")
    s=$(now)
    ( cd "$CWD" && "${R[@]}" <<<"$PROMPT" ) > "$OUT/$RID.reask.json" 2> "$OUT/$RID.reask.err"
    rc=$?; REASK_MS=$(( $(now) - s )); REASK_S=$(jq -n "$REASK_MS / 1000")
    { [ $rc = 124 ] || [ $rc = 137 ]; } && HANG=true
    jq -s -r '[.[]|select(.type=="result")|.result][0] // ""' "$OUT/$RID.reask.json" > "$OUT/$RID.reask.md" 2>/dev/null
    REASK_TOK=$(jq -s '[.[]|select(.type=="result")|.modelUsage|to_entries[]|.value.outputTokens]|add // 0' "$OUT/$RID.reask.json" 2>/dev/null || echo 0)
    rsid=$(jq -s -r '[.[]|select(.type=="result")|.session_id][0] // empty' "$OUT/$RID.reask.json" 2>/dev/null)
    [ -n "$rsid" ] && [ "$rsid" != "$SID" ] && { SIDS+=("$rsid"); partial_meta; }
    if [ -s "$OUT/$RID.reask.md" ]; then
      h2 "$OUT/$RID.reask.md" "$OUT/$RID.norm2.md" "$OUT/$RID.h2-reask.json"
      # the re-ask answer replaces the first report unless the merge would keep fewer of its lines
      # (more kept lines wins; on a tie, fewer dropped lines wins)
      if jq -e -n --slurpfile a "$OUT/$RID.h2-reask.json" --slurpfile b "$OUT/$RID.h2.json" \
           '[$a[0].kept_lines, -$a[0].dropped_lines] >= [$b[0].kept_lines, -$b[0].dropped_lines]' >/dev/null; then
        mv "$OUT/$RID.norm2.md" "$OUT/$RID.norm.md"; cp "$OUT/$RID.h2-reask.json" "$OUT/$RID.h2.json"
      fi
    fi
  fi
  DROPPED=$(jq '.dropped_lines' "$OUT/$RID.h2.json")  # block lines the merge parser will not keep
  cp "$OUT/$RID.norm.md" "$OUT/$RID.md"
else
  cp "$OUT/$RID.attempt$ATT.md" "$OUT/$RID.md" 2>/dev/null || : > "$OUT/$RID.md"
fi

END_MS=$(now)
LAST=$OUT/$RID.attempt$ATT.meta.json
[ -f "$LAST" ] || jq -n --arg rid "$RID" --arg exp "$MODEL" '{reviewer_id:$rid,expected_model:$exp,observed_model:"",model_ok:false,findings_block:false,attempt:0,exit:124}' > "$LAST"
ARGV_JSON=$(if [ ${#ARGVS[@]} -eq 0 ]; then echo '[]'; else printf '%s\n' "${ARGVS[@]}" | jq -s -c .; fi)
jq --argjson s "$(sids_json)" --argjson st "$START_MS" --argjson en "$END_MS" --argjson att "$ATT" --argjson rs "$RETRY_S" \
   --argjson iso $ISO --argjson ra "$REASK_S" --argjson dr "$DROPPED" --argjson hk $HANG --argjson ok $OK \
   --argjson argv "$ARGV_JSON" --arg role "$ROLE" --argjson collab "$COLLAB" \
   '. + {session_ids:$s, start_ms:$st, end_ms:$en, attempts:$att, retry_s:$rs, retry_isolated:$iso, reask_s:$ra,
         dropped_lines:$dr, hang_kill:$hk, valid:$ok, role:$role, collab:$collab, argv:$argv}' "$LAST" > "$OUT/$RID.meta.json"
W_SUM=0; for w in "${WALLS[@]}"; do W_SUM=$(( W_SUM + w )); done; W_SUM=$(( W_SUM + REASK_MS ))
T_SUM=$REASK_TOK; for t in "${TOKS[@]}"; do T_SUM=$(( T_SUM + t )); done
jq -n --argjson a "$ATT" --argjson w "$W_SUM" --argjson t "$T_SUM" '{attempts:$a, total_wall_s:($w/1000), total_output_tokens_all:$t}' > "$OUT/$RID.cost.json"
$OK && exit 0 || exit 1
