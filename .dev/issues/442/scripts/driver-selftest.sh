#!/usr/bin/env bash
# driver-selftest.sh — Task 3 cases for driver.sh, run by selftest.sh.
# The stub orca is a state machine over $OB_STUB_LOG: screen.txt (screen text),
# idle-on (wait returns 0), sent.txt (send calls), stages.txt (one log line released
# per `terminal wait` poll, so the driver sees events arriving over time), and
# STUB_STOP_LOG + STUB_STOP=1 (the send itself appends one Stop event).
set -u -o pipefail
umask 077

here=$(cd -- "$(dirname -- "$0")" && pwd)
failures=0
ck() { if [ "$2" = "$3" ]; then printf 'OK %s\n' "$1"; else printf 'FAIL %s got=<%s> want=<%s>\n' "$1" "$2" "$3"; failures=$((failures+1)); fi; }
lines() { printf '%s\n' "$1" | sed '/^[[:space:]]*$/d' | wc -l; }

T=$(mktemp -d /tmp/ob-driver.XXXXXXXX)
export OB=$T
L=$OB_STUB_LOG   # shared stub log dir from selftest.sh
mkdir -p "$T/logs" "$T/screens"
: > "$T/state.env"

bash "$here/driver.sh" start s1 path:main 'echo hi' > "$T/o-start" 2>&1
ck start-out "$(cat "$T/o-start")" "STARTED s1 stub-handle"
grep -q -- '--worktree path:main --title ob-442-s1' "$L/orca.log" && ck start-flags ok ok || ck start-flags missing ok

# --- send outcome: stop ------------------------------------------------------
export STUB_STOP_LOG=$T/logs/h1.jsonl; : > "$STUB_STOP_LOG"
export STUB_STOP=1
out=$(bash "$here/driver.sh" send s1 'prompt one' h1 30 2>&1)
ck send-stop "$(printf '%s' "$out" | tail -1)" "TURN_END stop"
unset STUB_STOP

# --- send outcome: blocked (baseline + increase) ------------------------------
: > "$L/screen.txt"; : > "$STUB_STOP_LOG"
export STUB_BLOCK=1
out=$(bash "$here/driver.sh" send s1 'prompt two' h1 30 2>&1)
unset STUB_BLOCK
ck send-blocked-new "$(printf '%s' "$out" | tail -1)" "TURN_END blocked"

# two blocked prompts in a row: the second send must not end blocked from the
# first send's still-visible Blocked: line (no new block, no Stop => timeout)
: > "$L/screen.txt"; : > "$STUB_STOP_LOG"
printf 'Blocked: first\n' > "$L/screen.txt"
out=$(bash "$here/driver.sh" send s1 'prompt three' h1 5 2>&1)
ck send-blocked-baseline "$(printf '%s' "$out" | tail -1)" "TURN_END timeout"

# --- send outcome: idle -------------------------------------------------------
: > "$L/screen.txt"; rm -f "$L/idle-on"; : > "$STUB_STOP_LOG"
touch "$L/idle-on"
out=$(bash "$here/driver.sh" send s1 'prompt four' h1 30 2>&1)
ck send-idle "$(printf '%s' "$out" | tail -1)" "TURN_END idle"
rm -f "$L/idle-on"

# a notice wait does not end on idle: with no notice answered it runs to the pending timeout result
: > "$L/screen.txt"; : > "$STUB_STOP_LOG"; touch "$L/idle-on"
out=$(bash "$here/driver.sh" send s1 'prompt four-b' h1 4 wait-notice 2>&1)
ck send-notice-idle-not-end "$(printf '%s' "$out" | head -1)" "TURN_END timeout"
rm -f "$L/idle-on"

# --- send outcome: timeout ----------------------------------------------------
: > "$L/screen.txt"; : > "$STUB_STOP_LOG"
out=$(bash "$here/driver.sh" send s1 'prompt five' h1 3 2>&1)
ck send-timeout "$(printf '%s' "$out" | tail -1)" "TURN_END timeout"

# --- NEEDS_INPUT: permission dialog on screen ---------------------------------
printf 'Do you want to proceed? (y/n)\n' > "$L/screen.txt"; : > "$STUB_STOP_LOG"
out=$(bash "$here/driver.sh" send s1 'prompt six' h1 10 2>&1)
case "$out" in
  NEEDS_INPUT\ *) ck send-needs-input ok ok ;;
  *) ck send-needs-input "$out" "NEEDS_INPUT <file>" ;;
esac
grep -q -- 'prompt six' "$L/sent.txt" 2>/dev/null && ck needs-input-not-sent sent ok || ck needs-input-not-sent ok ok

# --- notice_answered: both notice wrappers count (a subagent hand-back is an <agent-message>) ---
na() { printf '%s\n%s\n%s\n' '{"hook_event_name":"Stop"}' "{\"hook_event_name\":\"UserPromptSubmit\",\"prompt\":\"$1\"}" '{"hook_event_name":"Stop"}' > "$T/na.jsonl"; (source "$here/lib.sh"; source "$here/driver-helpers.sh"; notice_answered "$T/na.jsonl" 0) && echo yes || echo no; }
ck notice-task-notification "$(na '<task-notification>x')" yes
ck notice-agent-message "$(na '<agent-message from=a>x')" yes
ck notice-typed-prompt "$(na 'typed words')" no

# --- turn_stops: a nested session's Stop does not end the driven session's turn ---------------------------------
ts() { (source "$here/lib.sh"; source "$here/driver-helpers.sh"; turn_stops "$T/ts.jsonl" "$1" "$2"); }
printf '%s\n' '{"session_id":"P","hook_event_name":"Stop"}' > "$T/ts.jsonl"                       # an earlier turn: 1 line before the send
printf '%s\n' '{"session_id":"P","hook_event_name":"UserPromptSubmit","prompt":"go"}' '{"session_id":"C","hook_event_name":"Stop"}' >> "$T/ts.jsonl"
ck turn-stops-child-ignored "$(ts 1 1)" 0
printf '%s\n' '{"session_id":"P","hook_event_name":"Stop"}' >> "$T/ts.jsonl"
ck turn-stops-parent-counts "$(ts 1 1)" 1
printf '%s\n' '{"session_id":"P","hook_event_name":"Stop"}' > "$T/ts.jsonl"
ck turn-stops-no-prompt-falls-back "$(ts 0 0)" 1

# --- marker refusal -----------------------------------------------------------
if bash "$here/driver.sh" send s1 '[sc-launch:v1:x]' h1 5 >/dev/null 2>&1; then
  ck marker-refuse called ok
else
  if grep -q 'sc-launch' "$L/sent.txt" 2>/dev/null; then ck marker-refuse reached-orca ok; else ck marker-refuse ok ok; fi
fi

# --- wait-notice: notice arrives late and is answered --------------------------
# The stub releases one staged log line per `terminal wait` poll, so send first
# sees only the turn's Stop and must keep waiting (stages.txt still holds lines).
: > "$L/screen.txt"; : > "$STUB_STOP_LOG"; rm -f "$L/stages.txt"
export STUB_STOP=1
cat > "$L/stages.txt" <<'STAGES'
{"hook_event_name":"UserPromptSubmit","prompt":"<task-notification>bg done"}
{"hook_event_name":"Stop"}
STAGES
out=$(bash "$here/driver.sh" send s1 'prompt seven' h1 30 wait-notice 2>&1)
ck wait-notice-answered "$(printf '%s' "$out" | tail -1)" "TURN_END stop"
ck wait-notice-stages-drained "$(lines "$(cat "$L/stages.txt" 2>/dev/null)")" 0
unset STUB_STOP; rm -f "$L/stages.txt"

# --- wait-notice: log ends at the turn's Stop (the pending state) ---------------
: > "$L/screen.txt"; : > "$STUB_STOP_LOG"; rm -f "$L/stages.txt"
export STUB_STOP=1
out=$(bash "$here/driver.sh" send s1 'prompt eight' h1 6 wait-notice 2>&1)
ck wait-notice-pending "$(printf '%s' "$out" | sed -n '2p')" "PENDING notice-not-arrived"
unset STUB_STOP; rm -f "$L/stages.txt"

# --- wait-notice: no event ever arrives ----------------------------------------
: > "$L/screen.txt"; : > "$STUB_STOP_LOG"; rm -f "$L/stages.txt"
out=$(bash "$here/driver.sh" send s1 'prompt ten' h1 4 wait-notice 2>&1)
ck wait-notice-none "$(printf '%s' "$out" | sed -n '2p')" "PENDING notice-not-arrived"

# --- wait-notice: a NON-notice prompt between two Stops must not count ----------
: > "$L/screen.txt"; : > "$STUB_STOP_LOG"; rm -f "$L/stages.txt"
export STUB_STOP=1
cat > "$L/stages.txt" <<'STAGES'
{"hook_event_name":"UserPromptSubmit","prompt":"just a user typing"}
{"hook_event_name":"Stop"}
STAGES
out=$(bash "$here/driver.sh" send s1 'prompt eleven' h1 10 wait-notice 2>&1)
ck wait-notice-nonnotice "$(printf '%s' "$out" | sed -n '2p')" "PENDING notice-not-arrived"
unset STUB_STOP; rm -f "$L/stages.txt"

# --- wait-notice: a notice from BEFORE the send must not count ------------------
: > "$L/screen.txt"; rm -f "$L/stages.txt"
{ printf '{"hook_event_name":"Stop"}\n'; printf '{"hook_event_name":"UserPromptSubmit","prompt":"<task-notification>old"}\n'; printf '{"hook_event_name":"Stop"}\n'; } > "$STUB_STOP_LOG"
export STUB_STOP=1
cat > "$L/stages.txt" <<'STAGES'
{"hook_event_name":"Stop"}
STAGES
out=$(bash "$here/driver.sh" send s1 'prompt twelve' h1 8 wait-notice 2>&1)
ck wait-notice-stale "$(printf '%s' "$out" | sed -n '2p')" "PENDING notice-not-arrived"
unset STUB_STOP; rm -f "$L/stages.txt"

# --- answer: logged, marker-refused -------------------------------------------
mkdir -p "${PKG_ART:-$T/art}"
export PKG_ART=$T/art
bash "$here/driver.sh" answer s1 y 'allowed: git status in WT_T1' > /dev/null 2>&1
ck answer-logged "$(lines "$(cat "$T/art/t10-run-log.md" 2>/dev/null)")" 1
if bash "$here/driver.sh" answer s1 '[sc-launch:v1:x]' r >/dev/null 2>&1; then ck answer-marker-refuse called ok; else ck answer-marker-refuse ok ok; fi
ck answer-one-key "$(tail -1 "$L/sent.txt" | grep -o -- '--text y --enter --json')" "--text y --enter --json"

# --- needs_input: the start banner is not a dialog; a real permission dialog is ----
ni() { printf '%s' "$1" | jq -Rs '{result:{terminal:{tail:split("\n")}}}' > "$T/ni.json"; (source "$here/lib.sh"; source "$here/driver-helpers.sh"; needs_input "$T/ni.json") && echo yes || echo no; }
ck needs-input-banner "$(ni $'Auto mode lets Claude handle permission prompts automatically.\nhttps://code.claude.com/docs/en/permission-modes\n❯\n  auto mode on')" no
ck needs-input-permission "$(ni $'Permission rule: Bash(rm)\n ❯ 1. Yes\n   2. No')" yes
ck needs-input-login "$(ni $'Not logged in · Please run /login')" yes

# --- adopt / screen / stop ----------------------------------------------------
bash "$here/driver.sh" adopt gov1 gov-handle >/dev/null 2>&1
ck adopt-state "$(OB=$T bash -c "source '$here/lib.sh'; state_get H_gov1")" "gov-handle"
# the handle is found in a wrapped create output as well (the shape the real orca prints)
ck handle-jq-wrapped "$(printf '{"id":"x","ok":true,"result":{"terminal":{"handle":"term_w1","title":"t"}}}' | jq -r '[.. | .handle? | select(type == "string")][0] // empty')" term_w1
ck handle-jq-flat "$(printf '{"status":"ok","handle":"stub-handle"}' | jq -r '[.. | .handle? | select(type == "string")][0] // empty')" stub-handle
f=$(bash "$here/driver.sh" screen s1 2>/dev/null | tail -1)
[ -s "$f" ] && ck screen-saved ok ok || ck screen-saved empty ok
bash "$here/driver.sh" stop s1 >/dev/null 2>&1
grep -q -- 'terminal close' "$L/orca.log" && ck stop-called ok ok || ck stop-called missing ok

exit $failures
