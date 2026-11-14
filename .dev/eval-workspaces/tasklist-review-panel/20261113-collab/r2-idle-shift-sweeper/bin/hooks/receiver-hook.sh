#!/usr/bin/env bash
# Receiver (luna) PostToolUse hook: count, seal, deal, deliver, finish signal (DESIGN 2.5.1).
# Every parameter is a baked argument; nothing is read from the environment (R-21). Always exits 0 (R-22).
PATH=/usr/bin:/bin
START_MS=$(date +%s%3N)
JQ=/usr/bin/jq B="" RID="" RI=0 T0=0 FIN=0 K=0 DR=0 CAT=""
while [ $# -gt 0 ]; do case "$1" in
  --jq) JQ=$2;; --board) B=$2;; --rid) RID=$2;; --recv-index) RI=$2;; --t0-ms) T0=$2;;
  --finish-ms) FIN=$2;; --k) K=$2;; --deal-r) DR=$2;; --catalogue) CAT=$2;; esac; shift 2; done
LIB=$(cd "$(dirname "$0")/../lib" && pwd)
INPUT=$(cat)
S="$B/state"

mlog() { printf '%s\n' "$1" >> "$B/metrics/$RID.jsonl"; }
ev() { # ev <name> [jq-args...] <extra-object-expr>
  local name=$1; shift
  mlog "$("$JQ" -cn --arg ev "$name" --argjson t "$(date +%s%3N)" "$@")"
}

main() {
  set -e -o pipefail
  local tp tool c fp repo now ndel pick idx fline text
  tp=$("$JQ" -r '.transcript_path // ""' <<<"$INPUT")
  tool=$("$JQ" -r '.tool_name // ""' <<<"$INPUT")
  # One critical section for the whole call: a model can issue parallel tool calls, so two hook processes of the same
  # receiver may run at once; count, finish flag, k check, pick, seal and record must not interleave.
  exec 9>>"$S/lock"
  flock -w 4 9
  c=$(( $(cat "$S/$RID.calls" 2>/dev/null || echo 0) + 1 )); echo "$c" > "$S/$RID.calls"
  done_call() {
    ev call --argjson c "$c" --arg tool "$tool" --argjson ms $(( $(date +%s%3N) - START_MS )) '{ev:$ev,t:$t,c:$c,tool:$tool,ms:$ms}'
    exit 0
  }
  # step 3: union of opened paths (harvest filter)
  if [ "$tool" = Read ]; then
    fp=$("$JQ" -r '.tool_input.file_path // ""' <<<"$INPUT")
    repo=$("$JQ" -r .repo "$B/conf.json")
    fp=${fp#"$repo"/}
    printf '%s\n' "$fp" >> "$S/opened.txt"
  fi
  # step 4: finish signal
  now=$(date +%s%3N)
  if [ "$now" -ge "$FIN" ]; then
    if [ ! -e "$S/$RID.finish_sent" ]; then
      : > "$S/$RID.finish_sent"
      ev finish_signal '{ev:$ev,t:$t}'
      "$JQ" -cn --arg t "Time check: finish now with what you have. Write your final report with its findings block now." \
        '{hookSpecificOutput:{hookEventName:"PostToolUse",additionalContext:$t}}'
    fi
    done_call
  fi
  [ "$c" -ge 6 ] || done_call                      # step 5
  [ ! -e "$S/$RID.snapfail" ] || done_call          # step 6: fail closed for the rest of the run
  ndel=$(grep -c . "$S/$RID.delivered" 2>/dev/null || true); ndel=${ndel:-0}
  [ "$ndel" -lt "$K" ] || done_call                 # step 7
  [ -s "$B/msgs/board.jsonl" ] || done_call
  # step 8: balanced deal + rank (unnamed test 0, root document 1, other or witness 2), ties by board index
  pick=$("$JQ" -cs --argjson r "$DR" --argjson ri "$RI" \
      --rawfile del <(cat "$S/$RID.delivered" 2>/dev/null || true) --rawfile named "$B/named.txt" '
    ($del|split("\n")|map(select(length>0))) as $d | ($named|split("\n")|map(select(length>0))) as $nm
    | [to_entries[] | select(((.key + $r) % 2) == $ri) | select(.value.id as $id | ($d|any(.[]; . == $id))|not)
       | .value as $f | (($f.items // [])[0] // "" | sub(":[0-9]+$"; "")) as $p
       | {i:.key, f:$f, rank:(if ($f.move == "M6" or $f.move == "M9") then 2
           elif ($p|startswith("tests/")) and (($nm|any(.[]; . == $p))|not) then 0
           elif ($p|test("/")|not) and ($p|endswith(".md")) then 1 else 2 end)}]
    | sort_by(.rank, .i) | .[0] // empty' "$B/msgs/board.jsonl")
  [ -n "$pick" ] || done_call
  idx=$("$JQ" -r .i <<<"$pick"); fline=$("$JQ" -c .f <<<"$pick")
  # step 9: seal immediately before the first delivery; fail closed
  if [ ! -e "$S/$RID.sealed" ]; then
    local h
    if [ -n "$tp" ] && cp "$tp" "$B/snap/$RID.jsonl.tmp" 2>/dev/null \
       && h=$(sha256sum "$B/snap/$RID.jsonl.tmp" | cut -d' ' -f1) \
       && { printf '%s\n' "$h" > "$B/snap/$RID.sha256"; } 2>/dev/null \
       && mv "$B/snap/$RID.jsonl.tmp" "$B/snap/$RID.jsonl" 2>/dev/null; then
      : > "$S/$RID.sealed"
      ev seal --arg h "$h" '{ev:$ev,t:$t,sha256:$h}'
    else
      : > "$S/$RID.snapfail"
      ev snapshot_missing '{ev:$ev,t:$t}'
      done_call
    fi
  fi
  # step 10: render, record, deliver (one fact per call)
  text=$(bash "$LIB/render-fact.sh" --catalogue "$CAT" --jq "$JQ" --line "$fline")
  printf '%s\n' "$("$JQ" -r .id <<<"$fline")" >> "$S/$RID.delivered"
  ev deliver --argjson c "$c" --arg f "$("$JQ" -r .id <<<"$fline")" --argjson i "$idx" '{ev:$ev,t:$t,c:$c,fact:$f,i:$i}'
  "$JQ" -cn --arg t "$text" '{hookSpecificOutput:{hookEventName:"PostToolUse",additionalContext:$t}}'
  done_call
}

ERRF=$(mkdir -p /tmp/collab-r2 2>/dev/null; mktemp /tmp/collab-r2/r2-rhook.XXXXXX 2>/dev/null || echo /dev/null)
OUTPUT=$( (main) 2>"$ERRF" ); RC=$?
if [ $RC -ne 0 ]; then
  MSG=$(head -c 300 "$ERRF" 2>/dev/null | tr -cd 'A-Za-z0-9 ._:/=-' )
  printf '{"ev":"hook_error","t":%s,"rc":%s,"msg":"%s"}\n' "$(date +%s%3N)" "$RC" "$MSG" >> "$B/metrics/$RID.jsonl" 2>/dev/null
else
  [ -n "$OUTPUT" ] && printf '%s\n' "$OUTPUT"
fi
[ "$ERRF" = /dev/null ] || rm -f "$ERRF"
exit 0
