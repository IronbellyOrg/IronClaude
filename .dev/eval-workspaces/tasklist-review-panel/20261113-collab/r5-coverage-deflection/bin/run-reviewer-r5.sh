#!/usr/bin/env bash
# One reviewer (DESIGN 2.6): H1 brief, at most 2 attempts, hang guard, H2 normalise + one re-ask. No fallback ladder.
# usage: run-reviewer-r5.sh <outdir> <pkg> <rid> <model> <role> <t0_ms> <values.json|planning> [settings.json]
# env: PANEL_COLLAB, PANEL_KIT, NOFALLBACK=1 (required), DRY_RUN=1; test hooks: R5_SB, R5_CONFIG, CLAUDE_PROJECTS_DIR
set -u -o pipefail
OUT=$1; PKG=$2; RID=$3; MODEL=$4; ROLE=$5; T0=$6; VAL=$7; SETTINGS=${8:-}
R5=$(cd "$(dirname "$0")/.." && pwd); CFG=${R5_CONFIG:-$R5/config}; SB=${R5_SB:-/tmp/evalsb-collab-r5}
REPO=$(git -C "$R5" rev-parse --show-toplevel)
PROJ=${CLAUDE_PROJECTS_DIR:-$HOME/.claude/projects}
[ "${NOFALLBACK:-}" = 1 ] || { echo "refused: NOFALLBACK=1 is required" >&2; exit 2; }
case "$(tr 'A-Z' 'a-z' <<<"$MODEL")" in *glm*|*qwen*|*opus*) echo "refused: model $MODEL" >&2; exit 2;; esac
case " muse-ember-1.0 gpt-6-luna claude-haiku-5-5 claude-sonnet-5-5 grok-4.7 " in *" $MODEL "*) ;; *) echo "refused: model $MODEL not allowed" >&2; exit 2;; esac
py() { (cd "$REPO" && PYTHONPATH="$R5/lib" uv run --no-sync python -m "$@"); }
nowms() { date +%s%3N; }

if [ "$VAL" = planning ]; then HANG_MS=$(( T0 + 3000000 )); TURN=14
else
  HANG_MS=$(jq -r --argjson t0 "$T0" '($t0 + 1000*.hang_offset_s)|floor' "$VAL"); TURN=$(jq -r '.turn_p90_s' "$VAL")
fi
CAND=$SB/cand/$PKG/candidate.md; SOURCE=$SB/cand/$PKG/source.md
SHA=$(sha256sum "$CAND" | cut -d' ' -f1)
BRIEF=$(cat "$CFG/templates/brief-a1.txt")
BRIEF=${BRIEF//'{CAND}'/$CAND}; BRIEF=${BRIEF//'{SHA}'/$SHA}; BRIEF=${BRIEF//'{SOURCE}'/$SOURCE}
COLLAB=${PANEL_COLLAB:-0}; KIT=${PANEL_KIT:-0}; [ "$COLLAB" = 1 ] && KIT=1
[ "$KIT" = 1 ] && BRIEF+=$'\n\n'"$(cat "$CFG/templates/brief-kit.txt")"$'\n'"$(cat "$CFG/catalogue.md")"
[ "$COLLAB" = 1 ] && [ "$ROLE" = receiver ] && BRIEF+=$'\n\n'"$(cat "$CFG/templates/brief-receiver-f6.txt")"
CWD=$SB/$PKG/repo
cmd() { # <attempt>
  local a=(claude -p --model "$MODEL" --output-format json --permission-mode bypassPermissions --disallowedTools Edit Write NotebookEdit)
  [ "$1" = 1 ] && [ "$ROLE" = receiver ] && [ "$COLLAB" = 1 ] && [ -n "$SETTINGS" ] && a+=(--settings "$SETTINGS")
  printf '%s\n' "${a[@]}"
}
reask_cmd() { printf '%s\n' claude -p --resume "$1" --model "$MODEL" --output-format stream-json --verbose --permission-mode bypassPermissions --disallowedTools Edit Write NotebookEdit; }
if [ "${DRY_RUN:-}" = 1 ]; then
  echo "CWD: $CWD"; echo "CMD: timeout $(( (HANG_MS - $(nowms) + 999) / 1000 )) $(cmd 1 | tr '\n' ' ')"
  echo "CMD2: timeout <remaining_s> $(cmd 2 | tr '\n' ' ')"; echo "REASK_CMD: timeout <remaining_s> $(reask_cmd '<session_id>' | tr '\n' ' ')"
  printf 'BRIEF-BEGIN\n%s\nBRIEF-END\n' "$BRIEF"; exit 0
fi
mkdir -p "$OUT"
SLUG=$(realpath "$CWD" | sed 's/[^A-Za-z0-9]/-/g')

attempt=0; OK=false
while [ $attempt -lt 2 ]; do
  attempt=$((attempt+1)); P="$OUT/$RID.attempt$attempt"
  REM=$(( (HANG_MS - $(nowms) + 999) / 1000 ))
  [ "$REM" -gt 0 ] || { attempt=$((attempt-1)); break; }
  mapfile -t C < <(cmd $attempt)
  S=$(nowms)
  ( cd "$CWD" && timeout "$REM" "${C[@]}" <<<"$BRIEF" ) >"$P.json" 2>"$P.err"
  RC=$?; E=$(nowms)
  jq -r '[.[]|select(.type=="result")|.result]|.[0] // ""' "$P.json" > "$P.md" 2>/dev/null
  OBS=$(jq -r '[.[]|select(.type=="assistant" and (.parent_tool_use_id==null))|.message.model]|unique|join(",")' "$P.json" 2>/dev/null)
  TOK=$(jq '[.[]|select(.type=="result")|.usage.output_tokens]|.[0] // 0' "$P.json" 2>/dev/null)
  TOKALL=$(jq '[.[]|select(.type=="result")|.modelUsage|to_entries[]|.value.outputTokens]|add // 0' "$P.json" 2>/dev/null)
  SID=$(jq -r '[.[]|select(.type=="result")|.session_id]|.[0] // ""' "$P.json" 2>/dev/null)
  APIERR=false; grep -q 'API Error' "$P.md" 2>/dev/null && APIERR=true
  LOWOBS=$(echo "$OBS" | tr 'A-Z' 'a-z'); LOWEXP=$(echo "$MODEL" | tr 'A-Z' 'a-z')
  MODEL_OK=false; [ -n "$OBS" ] && [ "$OBS" != "<synthetic>" ] && { [ "$LOWOBS" = "$LOWEXP" ] || [ "$LOWOBS" = "$LOWEXP-build" ]; } && MODEL_OK=true
  BLOCK_OK=false; grep -q '^```findings-v1' "$P.md" && BLOCK_OK=true
  HANG=false; [ "$RC" = 124 ] && [ "$E" -ge "$HANG_MS" ] && HANG=true
  [ -n "$SID" ] && cp "$PROJ/$SLUG/$SID.jsonl" "$P.session.jsonl" 2>/dev/null
  SET_USED=false; printf '%s\n' "${C[@]}" | grep -qx -- --settings && SET_USED=true
  jq -n --arg rid "$RID" --arg exp "$MODEL" --arg obs "$OBS" --argjson mok $MODEL_OK --argjson bok $BLOCK_OK --argjson att $attempt \
    --argjson w $(( (E - S) / 1000 )) --argjson tok "${TOK:-0}" --argjson tokall "${TOKALL:-0}" --argjson rc $RC --argjson api $APIERR \
    --argjson ts "$S" --argjson te "$E" --argjson hang $HANG --arg sid "$SID" --argjson set $SET_USED --arg role "$ROLE" \
    '{reviewer_id:$rid,expected_model:$exp,observed_model:$obs,model_ok:$mok,findings_block:$bok,attempt:$att,wall_s:$w,output_tokens_main:$tok,output_tokens_all:$tokall,exit:$rc,api_error:$api,t_start_ms:$ts,t_end_ms:$te,hang_kill:$hang,session_id:$sid,settings:$set,role:$role,retry_isolated:($att>1)}' \
    > "$P.meta.json.tmp" && mv "$P.meta.json.tmp" "$P.meta.json"
  if $MODEL_OK && $BLOCK_OK && ! $APIERR; then OK=true; break; fi
done
[ $attempt -ge 1 ] || { echo "no attempt ran (hang guard already passed)" >&2; exit 1; }
F="$OUT/$RID.attempt$attempt"
cp "$F.md" "$OUT/$RID.raw.md"

# H2: normalise, then at most one re-ask on the final attempt's session
ERR0=$(py r5.h2 normalise "$F.md" "$OUT/$RID.norm.md") || ERR0='[{"line":0,"msg":"normaliser failed"}]'
printf '%s' "$ERR0" > "$OUT/$RID.h2-errors.json"
FINAL=$OUT/$RID.norm.md; NERR=$(jq length <<<"$ERR0"); REASK_S=0; SKIP=false; MISMATCH=false; USED=false
RMODEL=""; RMOK=null; RTOK=0; RW=0; END_MS=$(jq .t_end_ms "$F.meta.json")
SID=$(jq -r .session_id "$F.meta.json")
if [ "$NERR" -gt 0 ]; then
  LEFT=$(( (HANG_MS - $(nowms)) ))
  if [ -n "$SID" ] && awk -v l="$LEFT" -v t="$TURN" 'BEGIN{exit !(l/1000 >= 6 + t)}'; then
    mapfile -t RC_ < <(reask_cmd "$SID")
    py r5.h2 reask-prompt "$OUT/$RID.h2-errors.json" > "$OUT/$RID.reask-prompt.txt"
    S=$(nowms)
    ( cd "$CWD" && timeout $(( LEFT / 1000 )) "${RC_[@]}" < "$OUT/$RID.reask-prompt.txt" ) >"$OUT/$RID.reask.jsonl" 2>"$OUT/$RID.reask.err"
    END_MS=$(nowms); RW=$(( (END_MS - S) / 1000 )); REASK_S=$(awk -v a="$S" -v b="$END_MS" 'BEGIN{printf "%.3f",(b-a)/1000}')
    jq -rs '[.[]|select(.type=="result")|.result]|.[0] // ""' "$OUT/$RID.reask.jsonl" > "$OUT/$RID.reask.md" 2>/dev/null
    RMODEL=$(jq -rs '[.[]|select(.type=="assistant" and (.parent_tool_use_id==null))|.message.model]|unique|join(",")' "$OUT/$RID.reask.jsonl" 2>/dev/null)
    RTOK=$(jq -s '[.[]|select(.type=="result")|.modelUsage|to_entries[]|.value.outputTokens]|add // 0' "$OUT/$RID.reask.jsonl" 2>/dev/null)
    RAPI=false; grep -q 'API Error' "$OUT/$RID.reask.md" 2>/dev/null && RAPI=true
    LR=$(echo "$RMODEL" | tr 'A-Z' 'a-z'); LE=$(echo "$MODEL" | tr 'A-Z' 'a-z')
    RMOK=false; [ -n "$RMODEL" ] && [ "$RMODEL" != "<synthetic>" ] && { [ "$LR" = "$LE" ] || [ "$LR" = "$LE-build" ]; } && RMOK=true
    ERR1=$(py r5.h2 normalise "$OUT/$RID.reask.md" "$OUT/$RID.reask.norm.md") || ERR1='[{"line":0,"msg":"normaliser failed"}]'
    printf '%s' "$ERR1" > "$OUT/$RID.reask-errors.json"
    DEC=$(py r5.h2 decide "$OUT/$RID.h2-errors.json" "$OUT/$RID.reask-errors.json" "$RMOK" "$RAPI")
    case "$DEC" in reask*) FINAL=$OUT/$RID.reask.norm.md; NERR=$(jq length <<<"$ERR1"); USED=true;; esac
    case "$DEC" in *reask_model_mismatch) MISMATCH=true;; esac
  else SKIP=true; fi
fi
cp "$FINAL" "$OUT/$RID.md"
jq --arg rm "$RMODEL" --argjson rok "$RMOK" --argjson used $USED '. + {reask_observed_model:$rm,reask_model_ok:$rok,reask_used:$used}' "$F.meta.json" > "$OUT/$RID.meta.json"
jq -n --argjson rs "$REASK_S" --argjson sk $SKIP --argjson dl "$NERR" --argjson mm $MISMATCH --argjson e "$END_MS" --argjson s "$(jq -s 'map(.t_start_ms)|min' "$OUT/$RID".attempt*.meta.json)" \
  '{reask_s:$rs,reask_skipped:$sk,dropped_lines:$dl,reask_model_mismatch:$mm,t_start_ms:$s,t_end_ms:$e}' > "$OUT/$RID.timing.json"
jq -s --argjson rw "$RW" --argjson rt "${RTOK:-0}" '{attempts:length,total_wall_s:((map(.wall_s)|add)+$rw),total_output_tokens_all:((map(.output_tokens_all)|add)+$rt),reask_wall_s:$rw,reask_output_tokens_all:$rt}' "$OUT/$RID".attempt*.meta.json > "$OUT/$RID.cost.json"
$OK
