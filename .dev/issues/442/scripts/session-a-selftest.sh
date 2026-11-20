#!/usr/bin/env bash
# session-a-selftest.sh — Task 4 cases, run by selftest.sh.
# Uses the stub orca; driver.sh send writes one Stop per call (STUB_STOP=1), so
# each scripted prompt "ends its turn" and the send order is observable in
# the stub's sent.txt log.
set -u -o pipefail
umask 077

here=$(cd -- "$(dirname -- "$0")" && pwd)
RB=$(cd -- "$here/.." && pwd)/observation-runbook.md
failures=0
ck() { if [ "$2" = "$3" ]; then printf 'OK %s\n' "$1"; else printf 'FAIL %s got=<%s> want=<%s>\n' "$1" "$2" "$3"; failures=$((failures+1)); fi; }

T=$(mktemp -d /tmp/ob-sessa.XXXXXXXX)
export OB=$T
L=$OB_STUB_LOG
mkdir -p "$T/logs" "$T/screens" "$T/bin" "$T/repo-a"
: > "$T/state.env"
# minimal repo-a so the own-shell git steps no-op safely
git init -q -b master "$T/repo-a" 2>/dev/null
git -C "$T/repo-a" -c user.name=ob -c user.email=ob@invalid commit -q --allow-empty -m init 2>/dev/null
git -C "$T/repo-a" remote add origin "$T/bare.git" 2>/dev/null || true

export STUB_STOP_LOG=$T/logs/h1.jsonl; : > "$STUB_STOP_LOG"
export STUB_STOP=1 STUB_NOTICE=1
export OB_READY_POLLS=0   # the stub shows no Claude banner
export OB_ITEM4_POLLS=1 OB_ITEM4_SLEEP_S=0   # the stub never logs a Skill event: send Esc after one look

out=$(timeout 120 bash "$here/session-a.sh" 2>&1); rc=$?
ck sessa-rc "$rc" 0
ck sessa-done "$(printf '%s' "$out" | tail -1)" "SESSION_A_DONE"

# 1. every text block extracted byte-for-byte (17 files, 0 bytes difference)
extract_count=0; byte_ok=0
for f in "$here"/prompts/p*.txt; do extract_count=$((extract_count+1)); done
ck prompts-count "$extract_count" 17
# re-extract independently and compare each file
n=0; infence=0; rm -f "$T"/want-*.txt
while IFS= read -r line; do
  if [ "$infence" = 0 ]; then
    [ "$line" = '```text' ] && infence=1
  else
    if [ "$line" = '```' ]; then infence=0; n=$((n+1)); else printf '%s\n' "$line" >> "$T/want-$n.txt"; fi
  fi
done < <(sed -n '228,472p' "$RB")
want_total=$n
byte_ok=0
for k in $(seq 0 $((want_total - 1))); do
  pf=$(ls "$here"/prompts/p*.txt | sed -n "$((k+1))p")
  if cmp -s "$T/want-$k.txt" "$pf"; then byte_ok=$((byte_ok+1)); fi
done
ck prompts-bytes "$byte_ok" "$want_total"

# 2. no prompt file starts with the launch marker; only p10 (LL-NOBIND) contains it
bad_marker=0
for f in "$here"/prompts/p*.txt; do
  case "$(head -1 "$f")" in '[sc-launch:v1:'*) bad_marker=$((bad_marker+1));; esac
done
ck prompts-no-marker-start "$bad_marker" 0
grep -l 'sc-launch:v1' "$here"/prompts/p*.txt | wc -l | grep -qx 1 && ck prompts-marker-only-llnobind ok ok || ck prompts-marker-only-llnobind wrong ok

# 3. runbook order: strictly increasing FIRST-occurrence positions for the
# single-occurrence keys, in runbook order (duplicate keys -- /exit x3, say ok x2 --
# cannot use first-occurrence ordering, so their counts are asserted instead).
order_ok=0; order_bad=""
prev=0
order_keys=(-- '--text /hooks' 'ob-item1-sub' 'ob-item3-iso' '--text /sc:implement x' \
  'ob-item2' 'Monitor tool to run `sleep 2' 'sleep 3; echo approved' \
  'single word approved' 'subject ob-item6' 'ob9.txt' 'ob-item8' 'sc-launch:v1' \
  'ob-tree.sh bg-bash' 'ob-tree.sh monitor' 'git -c user.name=ob' 'ob-tree.sh subagent' \
  'setsid /tmp/ob/bin/ob-tree.sh' 'nobody-ob442' '--text /exit' '--text say ok' '--text /clear')
for key in "${order_keys[@]}"; do
  pos=$(grep -n -F -- "$key" "$L/sent.txt" | head -1 | cut -d: -f1)
  if [ -z "$pos" ] || [ "$pos" -le "$prev" ]; then
    order_bad="$order_bad [$key@$pos]"; order_ok=$((order_ok+1))
  fi
  prev=${pos:-0}
done
if [ "$order_ok" -eq 0 ]; then ck order-full ok ok; else ck order-full "out-of-order:$order_bad" "strictly increasing"; fi
# duplicate-key counts: /exit sent 3x (end of A, end of resume leg, end of fork leg), say ok 2x
ck count-exit "$(grep -c -F -- '--text /exit' "$L/sent.txt")" 3
ck count-sayok "$(grep -c -F -- '--text say ok' "$L/sent.txt")" 2
# Escape: twice to close the /hooks dialog, once to stop the item 4 turn
ck count-esc "$(grep -c -F -- "--text $(printf '\033')" "$L/sent.txt")" 3
# Ctrl+U once, after the LL-NOBIND prompt, to empty the input box
ck count-ctrlu "$(grep -c -F -- "--text $(printf '\025')" "$L/sent.txt")" 1

# 4. the wait-notice prompts were sent with the notice wait (they appear before
#    their turn ends only via staged events; with the stub they simply send)
grep -q 'ob-item1-sub' "$L/sent.txt" && ck item1-sent ok ok || ck item1-sent missing ok

# 5. MAIN state recorded from the log
ck main-state "$(OB=$T bash -c "source '$here/lib.sh'; state_get MAIN")" "none"

# 6. NEEDS_INPUT stop: script a permission dialog at the LL-NOBIND step
: > "$L/sent.txt"; : > "$STUB_STOP_LOG"
printf 'Do you want to proceed?\n' > "$L/screen.txt"
# the first run finished every step (A_STEP at its end): reset it, so this run sends again
ck resume-recorded-last-step "$(OB=$T bash -c "source '$here/lib.sh'; state_get A_STEP")" 23
printf 'A_STEP=0\n' >> "$T/state.env"
out=$(timeout 60 bash "$here/session-a.sh" 2>&1)
case "$out" in
  *PENDING\ step=*) ck sessa-needs-input ok ok ;;   # a first line SKIP start may precede it (the handle is already in the state)
  *) ck sessa-needs-input "$(printf '%s' "$out" | head -1)" "PENDING step=..." ;;
esac
# a rerun after step 20 sends nothing before step 21 (finished steps are skipped)
: > "$L/sent.txt"; printf 'A_STEP=20\n' >> "$T/state.env"; printf 'ok\n' > "$L/screen.txt"
out=$(timeout 60 bash "$here/session-a.sh" 2>&1)
ck resume-skips "$(printf '%s\n' "$out" | grep -c '^SKIP step=')" 20
ck resume-first-send "$(printf '%s\n' "$out" | grep '^SEND' | head -1 | cut -d' ' -f2)" step=21
# 7. session-a2: h1m empty => PENDING probe (log absent)
: > "$L/sent.txt"; rm -f "$T/logs/h1m.jsonl"
out=$(timeout 60 bash "$here/session-a2.sh" 2>&1)
case "$out" in
  PENDING\ step=1*) ck sessa2-pending-probe ok ok ;;
  *) ck sessa2-pending-probe "$(printf '%s' "$out" | head -1)" "PENDING step=1..." ;;
esac
# h1m present => sends the MCP prompt and exits 0
: > "$L/screen.txt"   # clear case 6's dialog so the pre-send check passes
export STUB_STOP_LOG=$T/logs/h1m.jsonl; : > "$STUB_STOP_LOG"
printf '{"hook_event_name":"SessionStart","session_id":"x"}\n' > "$T/logs/h1m.jsonl"
# the log exists but the input box is not ready (no prompt on the screen): nothing is sent
: > "$L/sent.txt"
out=$(OB_READY_POLLS=2 OB_READY_SLEEP_S=0 timeout 60 bash "$here/session-a2.sh" 2>&1)
case "$out" in *"reason=not-ready"*) ck sessa2-not-ready-pending ok ok ;; *) ck sessa2-not-ready-pending "$(printf '%s' "$out" | head -1)" "PENDING ... reason=not-ready" ;; esac
grep -q 'codegraph status' "$L/sent.txt" && ck sessa2-not-ready-sends-nothing sent none || ck sessa2-not-ready-sends-nothing none none
printf 'bypass permissions on (shift+tab to cycle)\n❯ \n' > "$L/screen.txt"   # the prompt is ready
out=$(timeout 60 bash "$here/session-a2.sh" 2>&1)
ck sessa2-rc "$?" 0
grep -q 'codegraph status' "$L/sent.txt" && ck sessa2-mcp-sent ok ok || ck sessa2-mcp-sent missing ok

# an h1.jsonl that holds an earlier turn (setup's login check) is moved aside before a fresh session A,
# so MAIN is the session A id and not the login check's
printf 'PKG=x\n' > "$T/state.env"
printf '{"hook_event_name":"SessionStart","session_id":"login-check-id"}\n' > "$T/logs/h1.jsonl"
export STUB_STOP_LOG=$T/logs/h1.jsonl
out=$(OB_READY_POLLS=0 timeout 60 bash "$here/session-a.sh" 2>&1)
ck sessa-old-log-moved "$([ -s "$T/logs/before-session-a/h1.jsonl" ] && grep -q login-check-id "$T/logs/before-session-a/h1.jsonl" && echo moved)" moved
ck sessa-main-not-login-check "$(! grep -q 'MAIN=login-check-id' "$T/state.env" && echo ok)" ok

exit $failures
