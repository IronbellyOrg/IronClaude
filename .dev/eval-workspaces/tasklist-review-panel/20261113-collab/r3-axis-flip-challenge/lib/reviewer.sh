#!/usr/bin/env bash
# reviewer.sh phase1|phase2 <pkgdir> <rid> <model>
# reviewer.sh print-cmd <pkgdir> <rid> <model> phase1|reask|phase2|fallback|p2reask
# Phase 1 (attempts, H2 re-ask, seal) and phase 2 (resume or fresh fallback, deadline kill, re-ask) of one reviewer (sections 5, 7).
set -u -o pipefail
source "$(dirname "$0")/common.sh"
MODE=$1; PD=$2; RID=$3; MODEL=$4; FORM=${5:-}
PKG=$(basename "$PD")
CWD=$SB/$PKG/repo
DISALLOW=(--disallowedTools Edit Write NotebookEdit)

# build_cmd <form> <limit> <session id>: sets CMD (argv) for one claude session form.
build_cmd() {
  local form=$1 lim=$2 sid=$3
  case $form in
    phase1)   CMD=(timeout --kill-after=5 "$lim" claude -p --model "$MODEL" --output-format json --permission-mode bypassPermissions "${DISALLOW[@]}");;
    reask)    CMD=(timeout --kill-after=5 "$lim" claude -p --model "$MODEL" --resume "$sid" --output-format stream-json --verbose --permission-mode bypassPermissions "${DISALLOW[@]}");;
    phase2|p2reask) CMD=(timeout --kill-after=3 "$lim" claude -p --model "$MODEL" --resume "$sid" --output-format stream-json --verbose --permission-mode bypassPermissions "${DISALLOW[@]}");;
    fallback) CMD=(timeout --kill-after=3 "$lim" claude -p --model "$MODEL" --output-format stream-json --verbose --permission-mode bypassPermissions "${DISALLOW[@]}");;
    *) echo "unknown form $form" >&2; return 1;;
  esac
}

if [ "$MODE" = print-cmd ]; then
  build_cmd "$FORM" "<T>" "<id>" || exit 1
  case $FORM in phase1|reask) dl=HANG_AT;; *) dl=P2_DEADLINE;; esac
  printf '%s\n' "${CMD[@]}" | jq -Rnc --arg cwd "$CWD" --arg dl "$dl" '{cwd:$cwd,deadline:$dl,argv:[inputs]}'
  exit 0
fi

r3_assert_nofallback || exit 1
r3_assert_model "$MODEL" || exit 1
r3_assert_writable "$PD/reviews" || exit 1
RV=$PD/reviews; mkdir -p "$RV"
pj() { jq -r "$1" "$PD/pkg.json"; }
T0=$(pj .T0); HANG_AT=$(pj .HANG_AT); P2_DEADLINE=$(pj .P2_DEADLINE)
TURN=$(jq -r --arg m "$MODEL" '.turn_p90[$m]' "$PD/pkg.json")
COLLAB=$(jq -r .collab "$PD/../run.json")
left() { r3_calc "$1 - $(r3_now)"; }
fits() { awk -v a="$(r3_now)" -v b="$1" -v d="$2" 'BEGIN{exit !(a + b < d)}'; }  # now + b < d

obs_model() { jq -sr '[.[]|if type=="array" then .[] else . end|select(.type=="assistant" and (.parent_tool_use_id==null))|.message.model]|unique|join(",")' "$1" 2>/dev/null; }
tok_main() { jq -sr '[.[]|if type=="array" then .[] else . end|select(.type=="result")|.usage.output_tokens]|.[0] // 0' "$1" 2>/dev/null || echo 0; }
tok_all() { jq -sr '[.[]|if type=="array" then .[] else . end|select(.type=="result")|.modelUsage // {}|to_entries[]|.value.outputTokens]|add // 0' "$1" 2>/dev/null || echo 0; }
res_text() { jq -sr '[.[]|if type=="array" then .[] else . end|select(.type=="result")|.result]|.[0] // ""' "$1" 2>/dev/null; }
sess_id() { jq -sr '[.[]|if type=="array" then .[] else . end|select(.type=="result" or .type=="system")|.session_id|select(.!=null)]|.[0] // ""' "$1" 2>/dev/null; }
model_ok() { # RR:51-56 rule
  local obs lo le; obs=$1; lo=$(echo "$obs" | tr 'A-Z' 'a-z'); le=$(echo "$MODEL" | tr 'A-Z' 'a-z')
  [ -n "$obs" ] && [ "$obs" != "<synthetic>" ] && { [ "$lo" = "$le" ] || [ "$lo" = "$le-build" ]; }
}
copy_transcript() { # <sid> <dest>
  local f; [ -n "$1" ] || return 0
  f=$(find "$CLAUDE_PROJECTS" -maxdepth 2 -name "$1.jsonl" 2>/dev/null | head -1)
  [ -n "$f" ] && cp "$f" "$2"
  return 0
}

# ------------------------------------------------------------------ phase 1
phase1() {
  local CAND SRC SHA SRC_SHA BRIEF a rc S E lim obs mok bok api tm ta sid tout
  CAND=$(pj .cand_sb); SRC=$(pj .src_sb); SHA=$(pj .cand_sha256); SRC_SHA=$(pj .src_sha256)
  BRIEF=$(cat "$R3/config/phase1-brief.txt")
  BRIEF=${BRIEF//\{CAND\}/$CAND}; BRIEF=${BRIEF//\{SHA\}/$SHA}; BRIEF=${BRIEF//\{SRC\}/$SRC}; BRIEF=${BRIEF//\{SRC_SHA\}/$SRC_SHA}
  printf '%s' "$BRIEF" > "$RV/$RID.brief.txt"
  local good=0 last_timeout=false sessions='[]' sids='[]' wall1=0 tokall=0 attempts=0
  for a in 1 2; do
    if [ $a = 2 ]; then fits 6 "$HANG_AT" || break; fi
    attempts=$a
    lim=$(left "$HANG_AT")
    awk -v l="$lim" 'BEGIN{exit !(l>0)}' || { last_timeout=true; break; }
    build_cmd phase1 "$lim" ""
    S=$(r3_now)
    r3_event "$PD" "$RID" proc_start --arg kind "attempt$a"
    ( cd "$CWD" && "${CMD[@]}" <<<"$BRIEF" ) >"$RV/$RID.attempt$a.json" 2>"$RV/$RID.attempt$a.err"
    rc=$?; E=$(r3_now)
    r3_event "$PD" "$RID" proc_end --arg kind "attempt$a" --argjson rc $rc
    res_text "$RV/$RID.attempt$a.json" > "$RV/$RID.attempt$a.md"
    obs=$(obs_model "$RV/$RID.attempt$a.json"); tm=$(tok_main "$RV/$RID.attempt$a.json"); ta=$(tok_all "$RV/$RID.attempt$a.json")
    sid=$(sess_id "$RV/$RID.attempt$a.json")
    api=false; grep -q 'API Error' "$RV/$RID.attempt$a.md" 2>/dev/null && api=true
    mok=false; model_ok "$obs" && mok=true
    bok=false; grep -q '^```findings-v1' "$RV/$RID.attempt$a.md" && bok=true
    tout=false; { [ $rc = 124 ] || [ $rc = 137 ]; } && tout=true
    last_timeout=$tout
    tokall=$((tokall + ${ta:-0}))
    [ $a = 1 ] && wall1=$(r3_calc "$E - $S")
    jq -n --arg rid "$RID" --arg exp "$MODEL" --arg obs "$obs" --argjson mok $mok --argjson bok $bok --argjson att $a \
      --argjson w "$(r3_calc "$E - $S")" --argjson tok "${tm:-0}" --argjson tokall "${ta:-0}" --argjson rc $rc --arg sid "$sid" \
      --argjson ts "$S" --argjson te "$E" --argjson to $tout --argjson api $api \
      '{reviewer_id:$rid,expected_model:$exp,observed_model:$obs,model_ok:$mok,findings_block:$bok,attempt:$att,wall_s:$w,output_tokens_main:$tok,output_tokens_all:$tokall,exit:$rc,session_id:$sid,t_start:$ts,t_end:$te,timed_out:$to,api_error:$api}' \
      > "$RV/$RID.attempt$a.meta.json"
    if [ -n "$sid" ]; then
      sids=$(jq -c --arg s "$sid" '.+[$s]' <<<"$sids")
    fi
    if $mok && $bok && ! $api; then good=$a; break; fi
    $tout && break
  done
  local retry_iso=false; [ "$attempts" = 2 ] && [ "$COLLAB" = 1 ] && retry_iso=true
  local retry_s=null; [ "$attempts" = 2 ] && retry_s=$wall1
  if [ "$good" = 0 ]; then
    local st=failed; $last_timeout && st=hang_kill
    [ $st = hang_kill ] && r3_event "$PD" "$RID" hang_kill
    jq -n --arg rid "$RID" --arg exp "$MODEL" --arg st $st --argjson att "$attempts" --argjson sids "$sids" --argjson tok $tokall \
      --argjson ri $retry_iso --argjson rs "$retry_s" \
      '{reviewer_id:$rid,expected_model:$exp,model_ok:false,state:$st,attempts:$att,session_ids:$sids,output_tokens_all:$tok,retry_isolated:$ri,retry_s:$rs,sessions:[]}' > "$RV/$RID.meta.json"
    jq -s '{attempts:length,total_wall_s:(map(.wall_s)|add),total_output_tokens_all:(map(.output_tokens_all)|add)}' "$RV/$RID".attempt*.meta.json > "$RV/$RID.cost.json" 2>/dev/null
    echo $st > "$RV/$RID.p1.state"
    return 0
  fi
  local REPORT="$RV/$RID.attempt$good.md" SID; SID=$(jq -r .session_id "$RV/$RID.attempt$good.meta.json")
  local OBS; OBS=$(jq -r .observed_model "$RV/$RID.attempt$good.meta.json")
  # H2: normalise, re-ask once, then seal
  r3_py normalize --in "$REPORT" --out "$RV/$RID.h2.md" --json "$RV/$RID.h2.json" >/dev/null; local nrc=$?
  local reask_s=null reask_tok=0
  if { [ $nrc = 3 ] || [ $nrc = 4 ]; } && [ -n "$SID" ] && fits "$(r3_calc "6 + $TURN")" "$HANG_AT"; then
    local ERRS FRAME; ERRS=$(r3_py reask-errors --json "$RV/$RID.h2.json")
    FRAME=$(cat "$R3/config/reask-frame.txt"); FRAME=${FRAME//\{ERRORS\}/$ERRS}
    build_cmd reask "$(left "$HANG_AT")" "$SID"
    S=$(r3_now); r3_event "$PD" "$RID" proc_start --arg kind reask
    ( cd "$CWD" && "${CMD[@]}" <<<"$FRAME" ) >"$RV/$RID.reask.stream.jsonl" 2>"$RV/$RID.reask.err"
    rc=$?; E=$(r3_now); r3_event "$PD" "$RID" proc_end --arg kind reask --argjson rc $rc
    reask_s=$(r3_calc "$E - $S")
    res_text "$RV/$RID.reask.stream.jsonl" > "$RV/$RID.reask.md"
    reask_tok=$(tok_all "$RV/$RID.reask.stream.jsonl"); tokall=$((tokall + ${reask_tok:-0}))
    local rsid; rsid=$(sess_id "$RV/$RID.reask.stream.jsonl"); [ -n "$rsid" ] && sids=$(jq -c --arg s "$rsid" '.+[$s]|unique' <<<"$sids")
    if model_ok "$(obs_model "$RV/$RID.reask.stream.jsonl")" && [ -s "$RV/$RID.reask.md" ]; then
      local e0 e1; e0=$(r3_py errcount --in "$REPORT"); e1=$(r3_py errcount --in "$RV/$RID.reask.md")
      if [ "$e1" -lt "$e0" ]; then REPORT="$RV/$RID.reask.md"; r3_event "$PD" "$RID" reask_used; fi
    else
      r3_event "$PD" "$RID" reask_model_mismatch
    fi
    r3_py normalize --in "$REPORT" --out "$RV/$RID.h2.md" --json "$RV/$RID.h2.json" >/dev/null
  fi
  # seal (raw report after the re-ask, before normalisation)
  cp "$REPORT" "$RV/$RID.p1.md"; chmod 0444 "$RV/$RID.p1.md"
  local P1SHA; P1SHA=$(sha256sum "$RV/$RID.p1.md" | cut -d' ' -f1); echo "$P1SHA" > "$RV/$RID.p1.sha256"
  local SEAL_T; SEAL_T=$(r3_now)
  copy_transcript "$SID" "$RV/$RID.p1.session.jsonl"
  r3_event "$PD" "$RID" sealed --arg sha "$P1SHA"
  jq -n --arg rid "$RID" --arg exp "$MODEL" --arg obs "$OBS" --arg sid "$SID" --argjson att "$attempts" --argjson sids "$sids" \
    --argjson tok $tokall --argjson rtok "${reask_tok:-0}" --argjson ri $retry_iso --argjson rs "$retry_s" --argjson ra "$reask_s" \
    --argjson seal "$SEAL_T" --arg sha "$P1SHA" --slurpfile h2 "$RV/$RID.h2.json" --argjson good "$good" \
    '{reviewer_id:$rid,expected_model:$exp,observed_model:$obs,model_ok:true,state:"sealed",attempts:$att,good_attempt:$good,
      session_id:$sid,session_ids:$sids,output_tokens_all:$tok,reask_output_tokens:$rtok,retry_isolated:$ri,retry_s:$rs,reask_s:$ra,
      seal_t:$seal,p1_sha256:$sha,dropped_lines:($h2[0].would_drop),dropped_msgs:[$h2[0].errors[]|.msg],
      sessions:[{session_id:$sid,kind:"phase1",model_ok:true,used:true}]}' > "$RV/$RID.meta.json"
  jq -s '{attempts:length,total_wall_s:(map(.wall_s)|add),total_output_tokens_all:(map(.output_tokens_all)|add)}' "$RV/$RID".attempt*.meta.json > "$RV/$RID.cost.json"
  echo sealed > "$RV/$RID.p1.state"
}

# ------------------------------------------------------------------ phase 2
phase2() {
  local SID S E rc lim mode=resume fallback=false timeout=false STREAM sessions_json='[]'
  SID=$(jq -r .session_id "$RV/$RID.meta.json")
  local T_LAUNCH; T_LAUNCH=$(r3_now)
  lim=$(left "$P2_DEADLINE")
  awk -v l="$lim" 'BEGIN{exit !(l>0)}' || { r3_event "$PD" "$RID" no_launch --arg reason deadline; return 0; }
  STREAM="reviews/$RID.p2.stream.jsonl"
  build_cmd phase2 "$lim" "$SID"
  S=$(r3_now); r3_event "$PD" "$RID" proc_start --arg kind phase2
  ( cd "$CWD" && "${CMD[@]}" < "$PD/board/$RID.prompt.txt" ) >"$PD/$STREAM" 2>"$RV/$RID.p2.err"
  rc=$?; E=$(r3_now); r3_event "$PD" "$RID" proc_end --arg kind phase2 --argjson rc $rc
  { [ $rc = 124 ] || [ $rc = 137 ]; } && timeout=true
  local n_ass is_err init_sid
  n_ass=$(jq -s '[.[]|select(.type=="assistant")]|length' "$PD/$STREAM" 2>/dev/null || echo 0)
  is_err=$(jq -s '[.[]|select(.type=="result")|.is_error]|.[0] // false' "$PD/$STREAM" 2>/dev/null || echo false)
  init_sid=$(jq -sr '[.[]|select(.type=="system")|.session_id]|.[0] // ""' "$PD/$STREAM" 2>/dev/null)
  if { [ "$n_ass" = 0 ] && [ $rc != 0 ]; } || [ "$is_err" = true ] || [ "$init_sid" != "$SID" ]; then
    if ! $timeout || [ "$n_ass" = 0 ]; then
      fallback=true; mode=fresh; timeout=false
      r3_event "$PD" "$RID" resume_fallback --argjson rc $rc
      local out; out=$(r3_py digest --pkgdir "$PD" --rid "$RID" --t-launch "$(r3_now)" --start-cost 16); local drc=$?
      if [ $drc != 0 ]; then
        r3_event "$PD" "$RID" no_launch --arg reason deadline_after_fallback --arg digest "$out"
        jq -n --argjson tl "$T_LAUNCH" --arg sid "$SID" '{mode:"fresh",t_launch:$tl,resume_fallback:true,model_ok:false,n_launched:0,no_launch:"deadline_after_fallback",session_ids:[$sid],sessions:[]}' > "$RV/$RID.p2.meta.json"
        return 0
      fi
      local P1C; P1C=$(jq -r .sb_pkg "$PD/pkg.json")/p1/$(jq -r .run_id "$PD/pkg.json")
      mkdir -p "$P1C"; cp "$RV/$RID.p1.md" "$P1C/$RID.p1.md"; chmod 0444 "$P1C/$RID.p1.md"
      STREAM="reviews/$RID.p2.fallback.stream.jsonl"
      build_cmd fallback "$(left "$P2_DEADLINE")" ""
      S=$(r3_now); r3_event "$PD" "$RID" proc_start --arg kind fallback
      ( cd "$CWD" && "${CMD[@]}" < "$PD/board/$RID.fallback.prompt.txt" ) >"$PD/$STREAM" 2>"$RV/$RID.p2.fallback.err"
      rc=$?; E=$(r3_now); r3_event "$PD" "$RID" proc_end --arg kind fallback --argjson rc $rc
      { [ $rc = 124 ] || [ $rc = 137 ]; } && timeout=true
    fi
  fi
  $timeout && r3_event "$PD" "$RID" phase2_timeout
  res_text "$PD/$STREAM" > "$RV/$RID.p2.md"
  local obs mok=false P2SID tm ta
  obs=$(obs_model "$PD/$STREAM"); model_ok "$obs" && mok=true
  $mok || r3_event "$PD" "$RID" p2_model_mismatch --arg observed "$obs"
  P2SID=$(sess_id "$PD/$STREAM"); tm=$(tok_main "$PD/$STREAM"); ta=$(tok_all "$PD/$STREAM")
  [ "$mode" = fresh ] && ta=$((ta + $(tok_all "$PD/reviews/$RID.p2.stream.jsonl")))
  local sids; sids=$(jq -nc --arg a "$SID" --arg b "$P2SID" '[$a,$b]|map(select(.!=""))|unique')
  # phase-2 re-ask (7.4)
  local p2reask_s=null REASK_STREAM=""
  if $mok && ! $timeout; then
    local ERRS; ERRS=$(r3_py p2check --stream "$PD/$STREAM"); local prc=$?
    if [ $prc = 3 ] && [ -n "$P2SID" ] && fits "$(r3_calc "6 + $TURN")" "$P2_DEADLINE"; then
      local FRAME; FRAME=$(cat "$R3/config/reask-frame.txt"); FRAME=${FRAME//\{ERRORS\}/$ERRS}
      build_cmd p2reask "$(left "$P2_DEADLINE")" "$P2SID"
      local S2; S2=$(r3_now); r3_event "$PD" "$RID" proc_start --arg kind p2reask
      ( cd "$CWD" && "${CMD[@]}" <<<"$FRAME" ) >"$RV/$RID.p2reask.stream.jsonl" 2>"$RV/$RID.p2reask.err"
      rc=$?; E=$(r3_now); r3_event "$PD" "$RID" proc_end --arg kind p2reask --argjson rc $rc
      p2reask_s=$(r3_calc "$E - $S2")
      res_text "$RV/$RID.p2reask.stream.jsonl" > "$RV/$RID.p2reask.md"
      ta=$((ta + $(tok_all "$RV/$RID.p2reask.stream.jsonl")))
      if model_ok "$(obs_model "$RV/$RID.p2reask.stream.jsonl")"; then REASK_STREAM="reviews/$RID.p2reask.stream.jsonl"
      else r3_event "$PD" "$RID" p2reask_model_mismatch; fi
      local rs; rs=$(sess_id "$RV/$RID.p2reask.stream.jsonl"); [ -n "$rs" ] && sids=$(jq -c --arg s "$rs" '.+[$s]|unique' <<<"$sids")
    elif [ $prc = 3 ]; then
      r3_event "$PD" "$RID" p2_lines_dropped_no_reask
    fi
  fi
  copy_transcript "$P2SID" "$RV/$RID.p2.session.jsonl"
  local DJ="$PD/board/$RID.digest.json"
  jq -n --arg mode $mode --argjson tl "$T_LAUNCH" --argjson te "$E" --argjson mok $mok --arg obs "$obs" --argjson tm "${tm:-0}" \
    --argjson ta "${ta:-0}" --argjson to $timeout --argjson fb $fallback --argjson pr "$p2reask_s" --arg sid "$P2SID" \
    --argjson sids "$sids" --arg fs "$STREAM" --arg rs "$REASK_STREAM" --slurpfile dg "$DJ" \
    '{mode:$mode,t_launch:$tl,t_end:$te,phase2_s:($te-$tl),n_planned:$dg[0].n_planned,n_launched:$dg[0].n_launched,
      model_ok:$mok,observed_model:$obs,output_tokens_main:$tm,output_tokens_all:$ta,phase2_timeout:$to,resume_fallback:$fb,
      p2reask_s:$pr,session_id:$sid,session_ids:$sids,final_stream:$fs,p2reask_stream:(if $rs=="" then null else $rs end),
      sessions:[{session_id:$sid,kind:"phase2",model_ok:$mok,used:$mok}]}' > "$RV/$RID.p2.meta.json"
}

case $MODE in
  phase1) phase1;;
  phase2) phase2;;
  *) echo "usage: reviewer.sh phase1|phase2|print-cmd ..." >&2; exit 1;;
esac
