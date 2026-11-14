#!/usr/bin/env bash
# Receiver PostToolUse hook (DESIGN 2.4). Arguments are baked into the settings command string; nothing is
# read from the environment (R-21). Any failure prints nothing, logs hook_error and exits 0 (R-22).
# usage: hook-posttool.sh <board> <rid> <t0_ms> <finish_ms> <min_calls> <k> <r5_root>
set -u -o pipefail
BOARD=$1; RID=$2; T0=$3; FIN=$4; MINC=$5; K=$6; R5=$7
M="$BOARD/metrics/$RID.jsonl"; ST="$BOARD/state"; SNAP="$BOARD/snap"; DEL="$BOARD/delivered/$RID.jsonl"
START=$(date +%s%3N)
log() { printf '%s\n' "$1" >> "$M" 2>/dev/null || true; }
done_() { log "{\"event\":\"call\",\"n\":${N:-0},\"ms\":$(( $(date +%s%3N) - START )),\"result\":\"$1\"}"; exit 0; }
fail() { log "{\"event\":\"hook_error\",\"step\":\"$1\",\"t\":$(date +%s%3N)}"; done_ error; }

IN=$(cat) || fail stdin
AGENT=$(jq -r '.agent_id // ""' <<<"$IN" 2>/dev/null) || fail parse_input
if [ -n "$AGENT" ]; then log "{\"event\":\"subagent_call\",\"agent_id\":\"$AGENT\",\"t\":$START}"; exit 0; fi

exec 9>>"$ST/$RID.lock" || fail lock
flock 9 || fail lock
N=$(( $(cat "$ST/$RID.calls" 2>/dev/null || echo 0) + 1 )) || fail count
echo "$N" > "$ST/$RID.calls" || fail count

NOW=$(date +%s%3N)
if [ "$NOW" -ge "$FIN" ]; then
  if ( set -o noclobber; : > "$ST/$RID.finish_sent" ) 2>/dev/null; then
    TEXT=$(cat "$R5/config/templates/finish.txt") || fail finish_text
    OUT=$(jq -nc --arg t "$TEXT" '{hookSpecificOutput:{hookEventName:"PostToolUse",additionalContext:$t}}') || fail finish_json
    log "{\"event\":\"finish_signal_t\",\"t\":$NOW,\"call\":$N}"
    printf '%s\n' "$OUT"
    done_ finish
  fi
  done_ after_finish
fi
[ "$N" -lt "$MINC" ] && done_ below_min_calls
[ "$K" -le 0 ] && done_ k0
[ -e "$ST/$RID.snapfail" ] && done_ snapfail

CARDS=$(jq -c --arg r "$RID" 'select(.to==$r)' "$BOARD/msgs/watcher.jsonl") || fail read_cards
DONE_IDS=$(jq -r '.id' "$DEL" 2>/dev/null) || DONE_IDS=""
PENDING=$(jq -c --arg ids "$DONE_IDS" 'select((.id as $i | ($ids|split("\n")) | index($i)) | not)' <<<"$CARDS") || fail pending
[ -z "$PENDING" ] && done_ none_pending

if [ ! -s "$SNAP/$RID.sha256" ]; then  # seal before the first delivery; fail closed on the seal
  TP=$(jq -r '.transcript_path // ""' <<<"$IN")
  if [ -z "$TP" ] || [ ! -s "$TP" ] || ! cp "$TP" "$SNAP/$RID.jsonl" 2>/dev/null \
     || ! sha256sum "$SNAP/$RID.jsonl" > "$SNAP/$RID.sha256" 2>/dev/null; then
    rm -f "$SNAP/$RID.sha256" 2>/dev/null
    : > "$ST/$RID.snapfail" 2>/dev/null
    log "{\"event\":\"snapshot_missing\",\"t\":$NOW,\"transcript\":$(jq -Rn --arg p "$TP" '$p')}"
    done_ snapshot_missing
  fi
  echo "$NOW" > "$SNAP/$RID.t" || fail seal_time
  log "{\"event\":\"seal\",\"t\":$NOW}"
fi

NEWEST=$(tail -n1 <<<"$PENDING")
BYTES=$(printf '%s' "$NEWEST" | LC_ALL=C wc -c)
[ "$BYTES" -le 600 ] || fail card_size
jq -e --argjson k "$K" '.kind=="coverage" and .from=="watcher" and (.items|type=="array" and length>=1 and length<=$k)' <<<"$NEWEST" >/dev/null || fail card_check
ID=$(jq -r .id <<<"$NEWEST") || fail card_id
TASKS=$(jq -r '[.items[]|"Task "+ltrimstr("T")]|join(", ")' <<<"$NEWEST") || fail card_tasks
if jq -e 'select(.status=="delivered")' "$DEL" >/dev/null 2>&1; then TPL=card-2.txt; else TPL=card-1.txt; fi
TEXT=$(cat "$R5/config/templates/$TPL") || fail template
TEXT=${TEXT//'{TASKS}'/$TASKS}; TEXT=${TEXT//'{K}'/$K}
[ "${#TEXT}" -le 1500 ] || fail text_size
OUT=$(jq -nc --arg t "$TEXT" '{hookSpecificOutput:{hookEventName:"PostToolUse",additionalContext:$t}}') || fail out_json
TSHA=$(printf '%s' "$TEXT" | sha256sum | cut -d' ' -f1)
while IFS= read -r old; do
  [ -n "$old" ] && [ "$old" != "$NEWEST" ] && jq -c --argjson n "$N" --argjson t "$NOW" '{id,t:$t,call:$n,status:"superseded"}' <<<"$old" >> "$DEL"
done <<<"$PENDING"
printf '%s\n' "{\"id\":\"$ID\",\"t\":$NOW,\"call\":$N,\"status\":\"delivered\",\"text_sha256\":\"$TSHA\",\"template\":\"$TPL\"}" >> "$DEL" || fail record
printf '%s\n' "$OUT"
done_ delivered
