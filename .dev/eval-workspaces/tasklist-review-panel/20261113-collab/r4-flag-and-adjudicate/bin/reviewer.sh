#!/usr/bin/env bash
# reviewer.sh <pkgdir> <rid> <model> <role> <collab 0|1>: one reviewer (design 2.6).
# The copy of RR with H1-H4, the hang guard, the RR:61-64 retry rule, the H2 re-ask and the
# collaboration settings. No model fallback ladder. Exit 0 always; the outcome is in <rid>.meta.json.
set -u -o pipefail
PKGDIR=$1; RID=$2; MODEL=$3; ROLE=$4; COLLAB=$5
HERE=$(cd "$(dirname "$0")/.." && pwd)
REPO=${R4_REPO:-$(cd "$HERE/../../../../.." && pwd)}
OUT="$PKGDIR/reviews"; mkdir -p "$OUT"
P="$PKGDIR/panel.json"
pj() { jq -r "$1" "$P"; }
SB=$(pj .sandbox); CAND=$(pj .cand); SRC=$(pj .src); SHA=$(pj .cand_sha)
HANG=$(pj .hang_ms); K=$(pj .k)
SETF=$(jq -r --arg r "$RID" '.settings[$r] // ""' "$P")
now_ms() { date +%s%3N; }
PROJECTS="$HOME/.claude/projects"

# 1. brief: A1 brief with H1, plus the role paragraph when collaboration is on and k >= 1
fill() { local s; s=$(cat "$1"); s=${s//\{CAND\}/$CAND}; s=${s//\{SHA\}/$SHA}; s=${s//\{SRC\}/$SRC}; printf '%s' "$s"; }
BRIEF_A1=$(fill "$HERE/frozen/brief-a1.txt")
BRIEF=$BRIEF_A1
if [ "$COLLAB" = 1 ] && [ "$K" -ge 1 ]; then
  if [ "$ROLE" = flagger ]; then
    MOVES=$(jq -r 'to_entries[] | select(.key|IN("M3","M4","M5","M6","M9")) | "\(.key): \(.value)"' "$HERE/frozen/moves.json")
    PARA=$(cat "$HERE/frozen/brief-flagger.txt")
    PARA=${PARA//\{HELPER\}/$(pj .helper)}; PARA=${PARA//\{CAP\}/$((2 * K))}; PARA=${PARA//\{MOVES\}/$MOVES}
  else
    PARA=$(cat "$HERE/frozen/brief-adjudicator.txt")
  fi
  BRIEF="$BRIEF_A1

$PARA"
fi

attempt=0; HANG_KILL=false; RETRY_ISO=false; RETRY_S=0; T_FIRST=""; T_LAST=""; SID=""; LAST_OK=false
run_attempt() { # one attempt; returns 0 when model_ok && findings block && no API error
  local n=$1 tmo s e rc set_args=() brief=$BRIEF settings=false
  tmo=$(( (HANG - $(now_ms)) / 1000 ))
  if [ "$tmo" -lt 1 ]; then HANG_KILL=true; return 2; fi
  if [ "$n" = 1 ] && [ "$COLLAB" = 1 ] && [ -n "$SETF" ]; then set_args=(--settings "$SETF"); settings=true; fi
  if [ "$n" -ge 2 ]; then brief=$BRIEF_A1; [ "$COLLAB" = 1 ] && RETRY_ISO=true; fi
  SID=$(cat /proc/sys/kernel/random/uuid)  # uuidgen is not installed on this host
  s=$(now_ms); [ -z "$T_FIRST" ] && T_FIRST=$s
  ( cd "$SB" && timeout --kill-after=5 "$tmo" claude -p --model "$MODEL" --output-format json --session-id "$SID" --permission-mode bypassPermissions --disallowedTools Edit Write NotebookEdit "${set_args[@]}" <<<"$brief" ) >"$OUT/$RID.attempt$n.json" 2>"$OUT/$RID.attempt$n.err"
  rc=$?; e=$(now_ms); T_LAST=$e
  { [ "$rc" = 124 ] || [ "$rc" = 137 ]; } && HANG_KILL=true
  [ "$n" -ge 2 ] && RETRY_S=$(( (e - s) / 1000 ))
  local f="$OUT/$RID.attempt$n"
  jq -r '[.[]|select(.type=="result")|.result]|.[0] // ""' "$f.json" > "$f.md" 2>/dev/null || : > "$f.md"
  local obs tok tokall apierr=false mok=false bok=false mm=false
  obs=$(jq -r '[.[]|select(.type=="assistant" and (.parent_tool_use_id==null))|.message.model]|unique|join(",")' "$f.json" 2>/dev/null)
  tok=$(jq '[.[]|select(.type=="result")|.usage.output_tokens]|.[0] // 0' "$f.json" 2>/dev/null)
  tokall=$(jq '[.[]|select(.type=="result")|.modelUsage|to_entries[]|.value.outputTokens]|add // 0' "$f.json" 2>/dev/null)
  grep -q 'API Error' "$f.md" 2>/dev/null && apierr=true
  local lo le; lo=$(echo "$obs" | tr 'A-Z' 'a-z'); le=$(echo "$MODEL" | tr 'A-Z' 'a-z')
  [ -n "$obs" ] && [ "$obs" != "<synthetic>" ] && { [ "$lo" = "$le" ] || [ "$lo" = "$le-build" ]; } && mok=true
  [ -n "$obs" ] && [ "$mok" = false ] && mm=true
  grep -q '^```findings-v1' "$f.md" && bok=true
  # transcript of this attempt, found exactly by its session id (deviation D-5)
  local tr; tr=$(find "$PROJECTS" -maxdepth 2 -name "$SID.jsonl" 2>/dev/null | head -1)
  [ -n "$tr" ] && cp "$tr" "$f.transcript.jsonl"
  jq -n --arg rid "$RID" --arg exp "$MODEL" --arg obs "$obs" --argjson mok $mok --argjson bok $bok --argjson att "$n" \
    --argjson w $(( (e - s) / 1000 )) --argjson tok "${tok:-0}" --argjson tokall "${tokall:-0}" --argjson rc "$rc" \
    --arg sid "$SID" --argjson ts "$s" --argjson te "$e" --argjson tmo "$tmo" --argjson set $settings --argjson api $apierr --argjson mm $mm \
    '{reviewer_id:$rid,expected_model:$exp,observed_model:$obs,model_ok:$mok,model_mismatch:$mm,findings_block:$bok,api_error:$api,attempt:$att,wall_s:$w,output_tokens_main:$tok,output_tokens_all:$tokall,exit:$rc,session_id:$sid,t_start_ms:$ts,t_end_ms:$te,timeout_s:$tmo,settings:$set}' > "$f.meta.json"
  $mok && $bok && ! $apierr
}

# 2. attempt loop (RR:61-64), at most 2 attempts
while [ $attempt -lt 2 ]; do
  attempt=$((attempt + 1))
  run_attempt $attempt; rc=$?
  [ $rc = 0 ] && { LAST_OK=true; break; }
  [ $rc = 2 ] && { attempt=$((attempt - 1)); break; }
done
LAST="$OUT/$RID.attempt$attempt"
# 4. raw final report and the last attempt's transcript
if [ "$attempt" -ge 1 ]; then
  cp "$LAST.md" "$OUT/$RID.md"
  [ -f "$LAST.transcript.jsonl" ] && cp "$LAST.transcript.jsonl" "$OUT/$RID.transcript.jsonl"
  SID=$(jq -r .session_id "$LAST.meta.json")
  BOK=$(jq -r .findings_block "$LAST.meta.json"); MOK=$(jq -r .model_ok "$LAST.meta.json"); OBS=$(jq -r .observed_model "$LAST.meta.json")
  MM=$(jq -r .model_mismatch "$LAST.meta.json")
else
  : > "$OUT/$RID.md"; SID=""; BOK=false; MOK=false; OBS=""; MM=false
fi

# 5. H2: final report always exists; normalise when there is a block
PYRUN=(uv run --frozen --project "$REPO" python)
REASK=false; REASK_S=null; REASK_MOK=null; TRUNC=0; REASK_TOK=0
if [ "$BOK" = true ]; then
  "${PYRUN[@]}" "$HERE/lib/normalize.py" "$OUT/$RID.md" "$OUT/$RID.final.md" "$OUT/$RID.parse.json" 2>"$OUT/$RID.normalize.err"
  TRUNC=$(jq -r '.truncated // 0' "$OUT/$RID.parse.json" 2>/dev/null || echo 0)
  NERR=$(jq '.errors | length' "$OUT/$RID.parse.json" 2>/dev/null || echo 0)
  TMO=$(( (HANG - $(now_ms)) / 1000 ))
  # 6. one re-ask through --resume when the parser still rejects lines
  if [ "$NERR" -gt 0 ] && [ -n "$SID" ] && [ "$TMO" -ge 1 ]; then
    REASK=true
    ERRS=$(jq -r '.errors[] | "line \(.line): \(.msg)"' "$OUT/$RID.parse.json")
    TPL=$(jq -r .reask "$HERE/frozen/templates.json"); MSG=${TPL//\{errors\}/$ERRS}
    s=$(now_ms)
    ( cd "$SB" && timeout --kill-after=5 "$TMO" claude -p --resume "$SID" --model "$MODEL" --output-format stream-json --verbose --permission-mode bypassPermissions --disallowedTools Edit Write NotebookEdit <<<"$MSG" ) > "$OUT/$RID.reask.jsonl" 2>"$OUT/$RID.reask.err"
    rrc=$?; e=$(now_ms); T_LAST=$e; REASK_S=$(( (e - s) / 1000 ))
    { [ "$rrc" = 124 ] || [ "$rrc" = 137 ]; } && HANG_KILL=true
    jq -r 'select(.type=="result") | .result // ""' "$OUT/$RID.reask.jsonl" 2>/dev/null > "$OUT/$RID.reask.md" || : > "$OUT/$RID.reask.md"
    ROBS=$(jq -r 'select(.type=="assistant" and (.parent_tool_use_id==null)) | .message.model' "$OUT/$RID.reask.jsonl" 2>/dev/null | sort -u | paste -sd, -)
    REASK_TOK=$(jq -s '[.[]|select(.type=="result")|.modelUsage|to_entries[]|.value.outputTokens]|add // 0' "$OUT/$RID.reask.jsonl" 2>/dev/null || echo 0)
    lo=$(echo "$ROBS" | tr 'A-Z' 'a-z'); le=$(echo "$MODEL" | tr 'A-Z' 'a-z')
    REASK_MOK=false; [ -n "$ROBS" ] && { [ "$lo" = "$le" ] || [ "$lo" = "$le-build" ]; } && REASK_MOK=true
    if [ "$REASK_MOK" = true ] && grep -q '^```findings-v1' "$OUT/$RID.reask.md"; then
      "${PYRUN[@]}" "$HERE/lib/normalize.py" "$OUT/$RID.reask.md" "$OUT/$RID.reask.final.md" "$OUT/$RID.reask.parse.json" 2>>"$OUT/$RID.normalize.err" \
        && cp "$OUT/$RID.reask.final.md" "$OUT/$RID.final.md" && cp "$OUT/$RID.reask.parse.json" "$OUT/$RID.parse.json"
      TRUNC=$(( TRUNC + $(jq -r '.truncated // 0' "$OUT/$RID.parse.json") ))
    fi
    # the resumed session appends to the same transcript file
    tr=$(find "$PROJECTS" -maxdepth 2 -name "$SID.jsonl" 2>/dev/null | head -1)
    [ -n "$tr" ] && cp "$tr" "$OUT/$RID.transcript.jsonl"
  fi
else
  cp "$OUT/$RID.md" "$OUT/$RID.final.md"
  jq -n '{ok:false,errors:[{line:0,msg:"no findings-v1 block in the final attempt"}],truncated:0}' > "$OUT/$RID.parse.json"
fi
DROPPED=$(jq '.errors | length' "$OUT/$RID.parse.json" 2>/dev/null || echo 0)
[ "$BOK" = true ] || DROPPED=0
FINAL_OK=false; [ "$MOK" = true ] && [ "$BOK" = true ] && [ "$LAST_OK" = true ] && FINAL_OK=true

# R-01 check: a tool call in the transcript names the source document
SRC_OPENED=false
[ -f "$OUT/$RID.transcript.jsonl" ] && jq -c 'select(.type=="assistant") | .message.content[]? | select(.type=="tool_use") | .input' "$OUT/$RID.transcript.jsonl" 2>/dev/null | grep -qF -- "$SRC" && SRC_OPENED=true

# 7. meta and cost
T_START=${T_FIRST:-$(now_ms)}; T_END=${T_LAST:-$T_START}
TOKALL=$(jq -s '[.[].output_tokens_all] | add // 0' "$OUT/$RID".attempt*.meta.json 2>/dev/null || echo 0)
TOKALL=$(( ${TOKALL:-0} + ${REASK_TOK:-0} ))
jq -n --arg rid "$RID" --arg role "$ROLE" --arg exp "$MODEL" --arg obs "$OBS" --argjson mok "$MOK" --argjson mm "$MM" \
  --argjson bok "$BOK" --argjson fok $FINAL_OK --argjson src $SRC_OPENED --argjson att "$attempt" --argjson rs "$RETRY_S" \
  --argjson ri $RETRY_ISO --argjson hk $HANG_KILL --argjson ra $REASK --argjson ras "$REASK_S" --argjson ramok "$REASK_MOK" \
  --argjson tr "${TRUNC:-0}" --argjson dr "${DROPPED:-0}" --argjson ts "$T_START" --argjson te "$T_END" --argjson tok "$TOKALL" \
  --arg sid "$SID" \
  '{reviewer_id:$rid,role:$role,expected_model:$exp,observed_model:$obs,model_ok:$mok,model_mismatch:$mm,findings_block:$bok,
    final_ok:$fok,source_md_opened:$src,attempts:$att,retry_s:$rs,retry_isolated:$ri,hang_kill:$hk,reask:$ra,reask_s:$ras,
    reask_model_ok:$ramok,truncated:$tr,dropped_lines:$dr,t_start_ms:$ts,t_end_ms:$te,wall_s:(($te-$ts)/1000),
    output_tokens_all:$tok,session_id:$sid}' > "$OUT/$RID.meta.json"
WALL=$(jq -s '[.[].wall_s] | add // 0' "$OUT/$RID".attempt*.meta.json 2>/dev/null || echo 0)
[ "$REASK_S" != null ] && WALL=$(( ${WALL:-0} + REASK_S ))
jq -n --argjson a "$attempt" --argjson w "${WALL:-0}" --argjson t "$TOKALL" '{attempts:$a,total_wall_s:$w,total_output_tokens_all:$t}' > "$OUT/$RID.cost.json"
exit 0
