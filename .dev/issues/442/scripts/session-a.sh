#!/usr/bin/env bash
# session-a.sh — runbook §2.1 session A (isolated HOME, label h1) via the driver.
# Plan Task 4. Prompt files are extracted byte-for-byte from the runbook's text
# blocks into prompts/ at start; control strings (/hooks, /exit, ...) are inline.
set -u -o pipefail
umask 077
here=$(cd -- "$(dirname -- "$0")" && pwd)
# shellcheck source=lib.sh
source "$here/lib.sh"
RB=$(cd -- "$here/.." && pwd)/observation-runbook.md
P=$here/prompts
mkdir -p "$P" "$OB_SCREENS"
rm -f "$P"/p*.txt   # idempotent: extraction is the single source of the prompt files

# --- extract every fenced ```text block in runbook lines 228-472 ----------------
names=(p01-item1 p02-item3 p03-item2 p04-item5a p05-item5b p06-item5c p07-item6 \
       p08-item9 p09-item8 p10-llnobind p11-ctx1 p12-ctx2 p13-ctx3 p14-ctx4 \
       p15-ctx5 p16-item7a p17-item7b)
i=0; infence=0
while IFS= read -r line; do
  if [ "$infence" = 0 ]; then
    [ "$line" = '```text' ] && infence=1 || :
  else
    if [ "$line" = '```' ]; then
      infence=0; i=$((i+1))
    else
      printf '%s\n' "$line" >> "$P/${names[$i]:-unnamed}.txt"
    fi
  fi
done < <(sed -n '228,472p' "$RB")
[ "$i" -eq 17 ] || { printf 'session-a: expected 17 text blocks, got %d\n' "$i" >&2; exit 1; }

# --- session start ---------------------------------------------------------------
# F05: `orca terminal create` has no directory flag (artifacts/t3-orca-help.txt),
# so the cd runs inside the terminal shell via --command; the worktree selector
# is the main checkout.
MAIN_WT=$(main_checkout)
START_CMD="cd $OB/repo-a && HOME=$OB/home CLAUDE_CONFIG_DIR=$OB/home/.claude claude"
wait_ready() {  # the terminal types START_CMD into a shell that may still be starting: send nothing before the Claude banner and prompt show
  local i f picked=""
  for i in $(seq 1 "${OB_READY_POLLS:-60}"); do
    f=$(bash "$here/driver.sh" screen sA | tail -1)
    # ready = the prompt line and the footer of the loaded screen (a resumed session has scrolled its banner away)
    if grep -q 'shift+tab' "$f" 2>/dev/null && grep -q '❯' "$f" 2>/dev/null && ! grep -qi 'resume session' "$f"; then return 0; fi
    # `claude --resume` opens a picker first: Enter takes the highlighted (newest) session, once
    if grep -qi 'resume session' "$f" 2>/dev/null && [ -z "${picked:-}" ]; then
      command timeout "${OB_TIMEOUT_S:-60}" orca terminal send --terminal "$(state_get H_sA)" --enter --json >/dev/null 2>&1 || true
      picked=1
    fi
    command sleep "${OB_READY_SLEEP_S:-2}"
  done
  [ "${OB_READY_POLLS:-60}" -eq 0 ] && return 0
  printf 'PENDING reason=claude-not-ready screen=%s\n' "$f"; exit 0
}
if [ -n "$(state_get H_sA 2>/dev/null)" ]; then
  printf 'SKIP start: session sA already has handle %s (adopted or started earlier)\n' "$(state_get H_sA)"
else
  # setup.sh's login check ran a Claude turn in this same isolated HOME and logged it to h1.jsonl. MAIN below is the first
  # SessionStart of the file, so move that older log aside first (seen live: MAIN was the login check, and OB-H1 item 1 failed).
  if [ -s "$OB_LOGS/h1.jsonl" ] && [ -z "$(state_get A_STEP 2>/dev/null)" ]; then
    mkdir -p "$OB_LOGS/before-session-a" && mv -- "$OB_LOGS"/h1.jsonl "$OB_LOGS"/h1.env.jsonl "$OB_LOGS/before-session-a/" 2>/dev/null
    printf 'MOVED the log of earlier turns (setup login check) to %s/before-session-a\n' "$OB_LOGS"
  fi
  bash "$here/driver.sh" start sA "path:$MAIN_WT" "$START_CMD" >/dev/null || { printf 'FAIL start sA: the driver could not start the session\n' >&2; exit 1; }
  wait_ready   # only a session this run started: an adopted or resumed one has scrolled its banner away
fi

step_id=0
# A rerun resumes: A_STEP in the state file is the last step that finished, and a finished step is not sent again.
DONE=$(state_get A_STEP 2>/dev/null || true); DONE=${DONE:-0}
todo() { [ "$DONE" -lt "$1" ]; }   # todo <n>: step n has not finished yet
last_screen() { ls -1t "$OB_SCREENS"/sA-*.json 2>/dev/null | head -1; }
send_file() {  # send_file <file> <label> [wait-notice]
  step_id=$((step_id+1))
  if ! todo "$step_id"; then printf 'SKIP step=%d (finished in an earlier run)\n' "$step_id"; return 0; fi
  local out f=$1 lbl=$2; shift 2
  out=$(bash "$here/driver.sh" send sA "$(cat "$f")" "$lbl" 600 "$@" 2>&1)
  case "$out" in
    NEEDS_INPUT\ *) printf 'PENDING step=%d file=%s screen=%s\n' "$step_id" "$f" "${out#NEEDS_INPUT }"; exit 0 ;;
    TURN_END\ timeout*) printf 'PENDING step=%d file=%s reason=timeout screen=%s\n' "$step_id" "$f" "$(last_screen)"; exit 0 ;;
    *PENDING*) printf 'PENDING step=%d file=%s reason=notice screen=%s\n' "$step_id" "$f" "$(last_screen)"; exit 0 ;;
    *driver:*) printf 'FAIL step=%d file=%s %s\n' "$step_id" "$f" "$(printf '%s' "$out" | tail -1)"; exit 1 ;;
  esac
  printf 'SEND step=%d file=%s %s\n' "$step_id" "$(basename "$f")" "$(printf '%s' "$out" | tail -1)"
  state_set A_STEP "$step_id"
}
send_str() {  # send_str <text> <label> [wait-notice]
  step_id=$((step_id+1))
  if ! todo "$step_id"; then printf 'SKIP step=%d (finished in an earlier run)\n' "$step_id"; return 0; fi
  local out t=$1 lbl=$2; shift 2
  out=$(bash "$here/driver.sh" send sA "$t" "$lbl" 600 "$@" 2>&1)
  case "$out" in
    NEEDS_INPUT\ *) printf 'PENDING step=%d text=%s screen=%s\n' "$step_id" "$t" "${out#NEEDS_INPUT }"; exit 0 ;;
    TURN_END\ timeout*) printf 'PENDING step=%d text=%s reason=timeout screen=%s\n' "$step_id" "$t" "$(last_screen)"; exit 0 ;;
    *PENDING*) printf 'PENDING step=%d text=%s reason=notice screen=%s\n' "$step_id" "$t" "$(last_screen)"; exit 0 ;;
    *driver:*) printf 'FAIL step=%d text=%s %s\n' "$step_id" "$t" "$(printf '%s' "$out" | tail -1)"; exit 1 ;;
  esac
  printf 'SEND step=%d text=%s %s\n' "$step_id" "$t" "$(printf '%s' "$out" | tail -1)"
  state_set A_STEP "$step_id"
}

send_str '/hooks' h1                                    # runbook line 168
# the /hooks dialog stays open and would swallow every later prompt: close it (Esc goes back one level, so twice)
if todo 2; then bash "$here/driver.sh" esc sA >/dev/null; command sleep 2; bash "$here/driver.sh" esc sA >/dev/null; command sleep 2; fi
send_file "$P/p01-item1.txt" h1
send_file "$P/p02-item3.txt" h1
# item 4: the literal command, then Esc once the Skill call shows (runbook line 270).
# The probe log is the signal: a PreToolUse event for the Skill tool. After 120 s Esc is sent anyway.
if todo 4; then
  sk0=$(grep -c '"tool_name":"Skill"' "$OB_LOGS/h1.jsonl" 2>/dev/null || true)
  bash "$here/driver.sh" fire sA '/sc:implement x' >/dev/null || { printf 'FAIL item4: the command was not sent\n' >&2; exit 1; }
  for _ in $(seq 1 "${OB_ITEM4_POLLS:-60}"); do
    [ "$(grep -c '"tool_name":"Skill"' "$OB_LOGS/h1.jsonl" 2>/dev/null || true)" -gt "$sk0" ] && break
    command sleep "${OB_ITEM4_SLEEP_S:-2}"
  done
  bash "$here/driver.sh" esc sA >/dev/null
  command timeout 40 orca terminal wait --terminal "$(state_get H_sA)" --for tui-idle --timeout-ms 30000 >/dev/null 2>&1 || true
  printf 'ITEM4 Esc sent; Skill events before %s, now %s\n' "$sk0" "$(grep -c '"tool_name":"Skill"' "$OB_LOGS/h1.jsonl" 2>/dev/null || true)"
fi
send_file "$P/p03-item2.txt" h1
send_file "$P/p04-item5a.txt" h1 wait-notice
send_file "$P/p05-item5b.txt" h1 wait-notice
send_file "$P/p06-item5c.txt" h1 wait-notice
send_file "$P/p07-item6.txt" h1
send_file "$P/p08-item9.txt" h1
send_file "$P/p09-item8.txt" h1
send_file "$P/p10-llnobind.txt" h1
# the guard refuses that prompt and Claude puts its text back into the input box: empty the box (Ctrl+U),
# or every later prompt is appended to the marker text and refused as well (seen live)
if todo 12; then bash "$here/driver.sh" raw sA $'\025' >/dev/null; command sleep 2; fi
send_file "$P/p11-ctx1.txt" h1
send_file "$P/p12-ctx2.txt" h1
send_file "$P/p13-ctx3.txt" h1
send_file "$P/p14-ctx4.txt" h1
send_file "$P/p15-ctx5.txt" h1
# own-shell steps (runbook lines 224-225, 424-425): MAIN id, human tree, human push
if todo 17; then
  MAIN=$(command timeout "${OB_TIMEOUT_S:-60}" jq -r 'select(.hook_event_name=="SessionStart") | .session_id' "$OB_LOGS/h1.jsonl" 2>/dev/null | head -1)
  state_set MAIN "${MAIN:-none}"
  command timeout "${OB_TIMEOUT_S:-60}" "$OB_BIN/ob-tree.sh" human >/dev/null 2>&1 || true
  ( cd "$OB/repo-a" && command timeout "${OB_TIMEOUT_S:-60}" git -c user.name=ob -c user.email=ob@invalid commit -q --allow-empty -m human \
    && command timeout "${OB_TIMEOUT_S:-60}" git push -q origin master ) >/dev/null 2>&1 || true
fi
# item 7 part 1 stays in session A (runbook line 442-446)
send_file "$P/p16-item7a.txt" h1
# end A, restart with --resume, /clear, say ok; exit; restart --continue --fork-session, say ok
send_str '/exit' h1
if todo 19; then
  bash "$here/driver.sh" stop sA >/dev/null
  bash "$here/driver.sh" start sA "path:$MAIN_WT" "$START_CMD --resume" >/dev/null
  wait_ready
fi
send_str 'say ok' h1
send_str '/clear' h1
send_str '/exit' h1
if todo 22; then
  bash "$here/driver.sh" stop sA >/dev/null
  bash "$here/driver.sh" start sA "path:$MAIN_WT" "$START_CMD --continue --fork-session" >/dev/null
  wait_ready
fi
send_str 'say ok' h1
send_str '/exit' h1
bash "$here/driver.sh" stop sA >/dev/null
printf 'SESSION_A_DONE\n'
