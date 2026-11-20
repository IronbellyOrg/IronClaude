#!/usr/bin/env bash
# driver-helpers.sh — wait logic for driver.sh (plan Task 3). Sourced, not run.
# wait_turn <name> <handle> <log> <stop_before> <block_before> <secs> <notice> <lines_before>

screen_json_field() {  # screen_json_field <file> — print the rendered screen text
  # Real shape (orca terminal read --screen --json): lines under result.terminal.tail.
  command timeout "${OB_TIMEOUT_S:-60}" jq -r '.result.terminal.tail // [] | join("\n")' "$1" 2>/dev/null || true
}

screen_block_count() {  # screen_block_count <name>: number of Blocked: lines on screen
  local f
  f=$(ls -1t "$OB_SCREENS/$1"-*.json 2>/dev/null | head -1)
  [ -n "$f" ] || { printf '0'; return; }
  screen_json_field "$f" | grep -c '^Blocked:' || true
}

wait_turn() {
  local name=$1 h=$2 log=$3 stop_before=$4 block_before=$5 secs=$6 notice=$7 lines_before=$8
  local deadline=$(( $(date +%s) + secs )) f why nl_stop nl_block
  while :; do
    f=$(save_screen "$name")
    nl_stop=$(grep -c '"hook_event_name":"Stop"' "$log" 2>/dev/null || true)
    nl_block=$(screen_block_count "$name")
    if [ "$nl_stop" -gt "$stop_before" ]; then
      if [ "$notice" -eq 1 ]; then
        # notice wait: hold until a background notice arrived and was answered
        if notice_answered "$log" "$lines_before"; then
          why=stop; break
        fi
      else
        why=stop; break
      fi
    fi
    if [ "$nl_block" -gt "$block_before" ]; then why=blocked; break; fi
    if needs_input "$f"; then printf 'NEEDS_INPUT %s\n' "$f"; exit 0; fi
    if command timeout 10 orca terminal wait --terminal "$h" --for tui-idle --timeout-ms 1000 >/dev/null 2>&1; then
      # idle: re-check Stop once, then accept idle as the end
      nl_stop=$(grep -c '"hook_event_name":"Stop"' "$log" 2>/dev/null || true)
      # a notice wait never ends on idle: it continues until the notice is answered or the timeout path below
      if [ "$notice" -ne 1 ] && [ "$nl_stop" -le "$stop_before" ]; then why=idle; break; fi
    fi
    [ "$(date +%s)" -ge "$deadline" ] && { why=timeout; break; }
    command sleep 2
  done
  if [ "$why" = timeout ] && [ "$notice" -eq 1 ]; then
    printf 'TURN_END timeout\nPENDING notice-not-arrived\n'
    exit 0
  fi
  printf 'TURN_END %s\n' "$why"
}

notice_answered() {  # notice_answered <log> <lines_before>: strict in-order Stop -> <task-notification> prompt -> Stop among the lines added after the send; fails by default
  command timeout "${OB_TIMEOUT_S:-60}" tail -n +"$(( $2 + 1 ))" "$1" 2>/dev/null | awk '
    st == 0 && /"hook_event_name":"Stop"/ { st = 1; next }
    st == 1 && /"hook_event_name":"UserPromptSubmit"/ && /<task-notification>|<agent-message/ { st = 2; next }   # a subagent hand-back arrives as <agent-message> (seen live, Claude Code 2.1.326)
    st == 2 && /"hook_event_name":"Stop"/ { st = 3 }
    END { exit (st == 3 ? 0 : 1) }'
}

needs_input() {  # needs_input <screen-file>: permission dialog or login screen
  local s
  # Only the bottom of the screen counts, and a bare word is not enough: the start banner of a new
  # session mentions "permission prompts" and "permission modes" and stays on the screen.
  s=$(screen_json_field "$1" | grep -v '^[[:space:]]*$' | tail -14)
  case "$s" in
    *"Do you want"*|*"/login"*|*"Not logged in"*|*"Please log in"*|*"Invalid API key"*) return 0 ;;
    *[Pp]ermission*"Yes"*|*[Pp]ermission*"Allow"*) return 0 ;;
  esac
  return 1
}
