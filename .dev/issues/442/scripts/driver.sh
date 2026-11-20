#!/usr/bin/env bash
# driver.sh — Orca terminal driver for the #442 observation run (plan Task 3).
# Subcommands: start | send | screen | adopt | answer | stop
set -u -o pipefail
umask 077
here=$(cd -- "$(dirname -- "$0")" && pwd)
# shellcheck source=lib.sh
source "$here/lib.sh"
# shellcheck source=driver-helpers.sh
source "$here/driver-helpers.sh"
T=${OB_TIMEOUT_S:-60}

usage() { printf 'usage: driver.sh start|send|screen|adopt|answer|stop ...\n' >&2; exit 2; }
handle_of() { state_get "H_${1:?name}" || { printf 'driver: unknown session %s\n' "$1" >&2; return 1; }; }
n_saved() { ls -1 "$OB_SCREENS/$1"-*.json 2>/dev/null | wc -l; }
save_screen() {  # save_screen <name> — capture once to the next screen file
  local f="$OB_SCREENS/$1-$(date -u +%H%M%S)-$(n_saved "$1").json"
  command timeout "$T" orca terminal read --terminal "$(handle_of "$1")" --screen --json > "$f" 2>/dev/null || true
  printf '%s' "$f"
}
send_refuse_marker() {  # refuse [sc-launch:v1: prompts (runbook 5.1)
  case "$1" in
    '[sc-launch:v1:'*) printf 'driver: refusing marker prompt\n' >&2; return 1 ;;
  esac
  return 0
}

cmd=${1:-}; shift || true
case "$cmd" in
  start)
    [ $# -ge 3 ] || usage
    name=$1 sel=$2; shift 2; cmdstr=$*
    out=$(command timeout "$T" orca terminal create --worktree "$sel" --title "ob-442-$name" --command "$cmdstr" --json) \
      || { printf 'driver: orca terminal create failed\n' >&2; exit 1; }
    # the real create output wraps the terminal (the Orca envelope has `result`); take the first `handle` string anywhere
    h=$(printf '%s' "$out" | jq -r '[.. | .handle? | select(type == "string")][0] // empty')
    [ -n "$h" ] || { printf 'driver: no handle in create output\n' >&2; exit 1; }
    state_set "H_$name" "$h"
    printf 'STARTED %s %s\n' "$name" "$h"
    ;;
  send)
    # send <name> <text> <label> [timeout-s] [wait-notice]
    [ $# -ge 3 ] || usage
    name=$1 text=$2 label=$3; shift 3
    secs=600; notice=0
    for a in "$@"; do
      case "$a" in
        wait-notice) notice=1 ;;
        ''|*[!0-9]*) : ;;
        *) secs=$a ;;
      esac
    done
    send_refuse_marker "$text" || exit 1
    h=$(handle_of "$name") || exit 1
    log="$OB_LOGS/$label.jsonl"
    # Pre-send check: a dialog already on screen means the prompt is not sent.
    pre=$(save_screen "$name")
    if needs_input "$pre"; then printf 'NEEDS_INPUT %s\n' "$pre"; exit 0; fi
    stop_before=$(grep -c '"hook_event_name":"Stop"' "$log" 2>/dev/null || true)
    lines_before=0; [ -f "$log" ] && lines_before=$(wc -l < "$log")
    block_before=$(screen_block_count "$name")
    command timeout "$((secs + T))" orca terminal send --terminal "$h" --text "$text" --enter --json >/dev/null \
      || { printf 'driver: orca terminal send failed\n' >&2; exit 1; }
    wait_turn "$name" "$h" "$log" "$stop_before" "$block_before" "$secs" "$notice" "$lines_before"
    ;;
  esc)
    # esc <name>: one Escape key (closes the /hooks dialog, stops a turn); nothing else is sent
    [ $# -ge 1 ] || usage
    h=$(handle_of "$1") || exit 1
    command timeout "$T" orca terminal send --terminal "$h" --text $'\e' --json >/dev/null \
      || { printf 'driver: esc send failed\n' >&2; exit 1; }
    printf 'ESC %s\n' "$1"
    ;;
  fire)
    # fire <name> <text>: type the text and Enter, return at once (the caller waits itself)
    [ $# -ge 2 ] || usage
    send_refuse_marker "$2" || exit 1
    h=$(handle_of "$1") || exit 1
    command timeout "$T" orca terminal send --terminal "$h" --text "$2" --enter --json >/dev/null \
      || { printf 'driver: fire send failed\n' >&2; exit 1; }
    printf 'FIRED %s\n' "$1"
    ;;
  raw)
    # raw <name> <text>: type the text WITHOUT Enter (for a control key such as Ctrl+U that empties the input box)
    [ $# -ge 2 ] || usage
    send_refuse_marker "$2" || exit 1
    h=$(handle_of "$1") || exit 1
    command timeout "$T" orca terminal send --terminal "$h" --text "$2" --json >/dev/null \
      || { printf 'driver: raw send failed\n' >&2; exit 1; }
    printf 'RAW %s\n' "$1"
    ;;
  screen)
    [ $# -ge 1 ] || usage
    printf '%s\n' "$(save_screen "$1")"
    ;;
  adopt)
    [ $# -ge 2 ] || usage
    state_set "H_$1" "$2"
    printf 'ADOPTED %s %s\n' "$1" "$2"
    ;;
  answer)
    # answer <name> <key> <reason>: one keypress, marker-refused, logged
    [ $# -ge 3 ] || usage
    name=$1 key=$2; shift 2; reason=$*
    send_refuse_marker "$key" || exit 1
    h=$(handle_of "$name") || exit 1
    command timeout "$T" orca terminal send --terminal "$h" --text "$key" --enter --json >/dev/null \
      || { printf 'driver: answer send failed\n' >&2; exit 1; }
    mkdir -p "$PKG_ART"
    printf '%s %s %s\n' "$(date -u +%FT%TZ)" "$name" "$key $reason" >> "$PKG_ART/t10-run-log.md"
    printf 'ANSWERED %s\n' "$name"
    ;;
  stop)
    [ $# -ge 1 ] || usage
    command timeout "$T" orca terminal close --terminal "$(handle_of "$1")" >/dev/null 2>&1 || true
    printf 'STOPPED %s\n' "$1"
    ;;
  *) usage ;;
esac
