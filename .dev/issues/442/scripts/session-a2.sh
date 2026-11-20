#!/usr/bin/env bash
# session-a2.sh — runbook §2.1b session A2 (label h1m) via the driver.
# The item-7 first prompt is sent by session-a.sh inside session A; this script
# only starts A2 and sends the MCP prompt. Plan Task 4.
set -u -o pipefail
umask 077
here=$(cd -- "$(dirname -- "$0")" && pwd)
# shellcheck source=lib.sh
source "$here/lib.sh"
P=$here/prompts
# self-sufficient: extract prompt 17 (the A2 MCP prompt) if session-a.sh has not run
if [ ! -f "$P/p17-item7b.txt" ]; then
  RB=$(cd -- "$here/.." && pwd)/observation-runbook.md
  mkdir -p "$P"
  n=0; infence=0
  while IFS= read -r line; do
    if [ "$infence" = 0 ]; then
      [ "$line" = '```text' ] && infence=1
    else
      if [ "$line" = '```' ]; then infence=0; n=$((n+1)); else [ "$n" -eq 16 ] && printf '%s\n' "$line" >> "$P/p17-item7b.txt"; fi
    fi
  done < <(sed -n '228,472p' "$RB")
fi

MAIN_WT=$(main_checkout)
START_CMD="cd $OB/repo-a && claude --settings $OB/settings-a2.json"
bash "$here/driver.sh" start sA2 "path:$MAIN_WT" "$START_CMD" >/dev/null

# probe loaded? (runbook line 455)
if [ ! -s "$OB_LOGS/h1m.jsonl" ]; then
  sleep 3
fi
if [ ! -s "$OB_LOGS/h1m.jsonl" ]; then
  printf 'PENDING step=1 text=probe reason=h1m-log-empty\n'
  bash "$here/driver.sh" stop sA2 >/dev/null
  exit 0
fi

out=$(bash "$here/driver.sh" send sA2 "$(cat "$P/p17-item7b.txt")" h1m 600 2>&1)
case "$out" in
  NEEDS_INPUT\ *) printf 'PENDING step=2 file=%s screen=%s\n' "$P/p17-item7b.txt" "${out#NEEDS_INPUT }";;
  TURN_END\ timeout*) printf 'PENDING step=2 file=%s reason=timeout screen=%s\n' "$P/p17-item7b.txt" "$(ls -1t "$OB_SCREENS"/sA2-*.json 2>/dev/null | head -1)";;
  *PENDING*) printf 'PENDING step=2 file=%s reason=notice screen=%s\n' "$P/p17-item7b.txt" "$(ls -1t "$OB_SCREENS"/sA2-*.json 2>/dev/null | head -1)";;
  *) printf 'SEND step=2 file=p17-item7b.txt %s\n' "$(printf '%s' "$out" | tail -1)";;
esac
# End A2 with /exit (runbook line 470); a 5s bound, the wait is futile once it exits.
bash "$here/driver.sh" send sA2 '/exit' h1m 5 >/dev/null 2>&1
bash "$here/driver.sh" stop sA2 >/dev/null
printf 'SESSION_A2_DONE\n'
