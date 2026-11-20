#!/usr/bin/env bash
# session-gov.sh <b|c|d|e> — runbook §2.2 governed sessions B to E. Plan Task 6.
# Every subcommand refuses at entry unless OB-H1 item 5 is PASS in the results file
# (d and e also need item 1; runbook section 3.3). Prompt files g*.txt are extracted
# byte for byte from the runbook's text blocks into prompts/ at start.
set -u -o pipefail
umask 077
here=$(cd -- "$(dirname -- "$0")" && pwd)
# shellcheck source=lib.sh
source "$here/lib.sh"
RB=$(cd -- "$here/.." && pwd)/observation-runbook.md
RESULTS=${OB_RESULTS:-$(cd -- "$here/.." && pwd)/observation-results.md}
P=$here/prompts
T=${OB_TIMEOUT_S:-60}
POLL=${OB_POLL_S:-5}
SESS=$HOME/.claude/state/launch-level/sessions
IDENT=${OB_IDENTIFY:-$HOME/.claude/hooks/launch-job-identity.sh}
GOVLOG=$OB/gov-log.txt
BACKUP=$OB/t1-local.json
BARE=$OB/bare-push.git

sub=${1:-}
case "$sub" in b|c|d|e) ;; *) printf 'usage: session-gov.sh b|c|d|e\n' >&2; exit 2 ;; esac

# --- stop rule at entry (runbook 3.3, lines 720-726) -----------------------------
result_of() {  # result_of "<item name>": the Result of that block, or "missing"
  [ -f "$RESULTS" ] || { printf 'missing'; return; }
  awk -v h="## $1" '
    { sub(/[ \t\r]+$/, "") }
    $0 == h { on = 1; next }
    on && /^## / { exit }
    on && /^- Result:/ { sub(/^- Result:[ \t]*/, ""); print; found = 1; exit }
    END { if (!found) print "missing" }' "$RESULTS"
}
gate() {  # gate <n>...: each OB-H1 item must read PASS
  local n r
  for n in "$@"; do
    r=$(result_of "OB-H1 item $n")
    [ "$r" = PASS ] || { printf 'REFUSED gate item=%s result=%s (runbook section 3.3)\n' "$n" "$r"; exit 4; }
  done
}
case "$sub" in b|c) gate 5 ;; d|e) gate 5 1 ;; esac

mkdir -p "$OB_LOGS" "$OB_SCREENS"
rec() { step "$@" | tee -a "$GOVLOG"; }
die() { rec "$1" FAIL "${2:-}"; exit "${3:-1}"; }
pending() { printf 'PENDING %s\n' "$*" | tee -a "$GOVLOG"; exit 0; }
runlog() { mkdir -p "$PKG_ART"; printf '%s %s\n' "$(date -u +%FT%TZ)" "$*" >> "$PKG_ART/t10-run-log.md"; }
tgit() { command timeout "$T" git "$@"; }
need() {  # need <VAR> <state key>: set VAR from the state file, or stop
  local v
  v=$(state_get "$2") && [ -n "$v" ] || die state "missing state key $2"
  printf -v "$1" '%s' "$v"
}

# --- prompt files: the 9 text blocks of section 2.2.1 to 2.2.4 --------------------
names=(g01-b-implement g02-commit g03-approved g04-gov-bg g05-gov-det g06-gov-clear \
       g07-c-implement g08-e-push g09-e-merge)
extract_prompts() {
  local i=0 infence=0 line
  mkdir -p "$P"; rm -f "$P"/g*.txt
  while IFS= read -r line; do
    if [ "$infence" = 0 ]; then
      [ "$line" = '```text' ] && infence=1 || :
    elif [ "$line" = '```' ]; then
      infence=0; i=$((i+1))
    else
      printf '%s\n' "$line" >> "$P/${names[$i]:-unnamed}.txt"
    fi
  done < <(sed -n '/^#### 2\.2\.1 /,/^## 3\. /p' "$RB")
  [ "$i" -eq 9 ] || die extract "expected 9 text blocks, got $i"
}
extract_prompts

# --- sending ----------------------------------------------------------------------
SN=0
gsend() {  # gsend <name> <label> <text> [secs] [wait-notice]
  local name=$1 label=$2 text=$3 out rc; shift 3
  SN=$((SN+1))
  out=$(bash "$here/driver.sh" send "$name" "$text" "$label" "$@" 2>&1); rc=$?
  case "$out" in
    NEEDS_INPUT\ *) pending "step=$SN reason=needs-input name=$name screen=${out#NEEDS_INPUT }" ;;
    *PENDING*|TURN_END\ timeout*) pending "step=$SN reason=timeout name=$name label=$label" ;;
  esac
  [ "$rc" -eq 0 ] || die "send-$SN" "driver exit $rc: $(printf '%s' "$out" | tail -1)"
  rec "send-$SN" OK "$name $label $(printf '%s' "$text" | head -1 | cut -c1-60)"
}
screen_text() {  # screen_text <name>: the newest screen of that session as plain text
  local f
  f=$(bash "$here/driver.sh" screen "$1")
  command timeout "$T" jq -r '.result.terminal.tail // [] | join("\n")' "$f" 2>/dev/null
}
count_stops() {  # count_stops <log>
  local c; c=$(grep -c '"hook_event_name":"Stop"' "$1" 2>/dev/null || true); printf '%s' "${c:-0}"
}
wait_first_stop() {  # wait_first_stop <label> <secs>: the agent's first turn has ended
  local f=$OB_LOGS/$1.jsonl end=$(( $(date +%s) + $2 ))
  while :; do
    [ "$(count_stops "$f")" -ge 1 ] && return 0
    [ "$(date +%s)" -ge "$end" ] && return 1
    command sleep "$POLL"
  done
}
wait_gsid() {  # wait_gsid <label>: the governed session id from the probe log
  local f=$OB_LOGS/$1.jsonl end=$(( $(date +%s) + ${OB_LAUNCH_WAIT_S:-120} )) g
  while :; do
    g=$(command timeout "$T" jq -r 'select(.session_id) | .session_id' "$f" 2>/dev/null | head -1)
    [ -n "$g" ] && { printf '%s' "$g"; return 0; }
    [ "$(date +%s)" -ge "$end" ] && return 1
    command sleep "$POLL"
  done
}

# --- the claim and its printed result ---------------------------------------------
# CLAIM_TXT is the claim session's screen with spaces, newlines and backslashes
# removed, so wrapped JSON still matches; CLAIM_LAST is the text after the newest
# "status" key (the stale results of earlier claims stay above it).
claim_send() {  # claim_send <issue number> <flags>
  # a claim terminal that no longer exists shows an empty screen for ever: stop at once, send nothing
  local cs; cs=$(bash "$here/driver.sh" screen claim 2>/dev/null | tail -1)
  if [ -z "$cs" ] || [ "$(command timeout "$T" jq -r '(.result.terminal.tail // []) | length' "$cs" 2>/dev/null || echo 0)" = 0 ]; then
    pending "reason=claim-terminal-gone screen=${cs:-none}"
  fi
  # A clean screen first, so the result read below is this claim's. Then type and return at once: the driver's own turn
  # wait has no probe log for the claim session and can hold the full 900 s after the claim is done (seen live).
  local i raw fo
  if [ "${OB_CLAIM_POLLS:-180}" -ne 0 ]; then bash "$here/driver.sh" send claim "/clear" claim 60 >/dev/null 2>&1; fi
  SN=$((SN+1))
  fo=$(bash "$here/driver.sh" fire claim "/sc:issue --claim $1 $2" 2>&1) || die "send-$SN" "claim send failed: $(printf '%s' "$fo" | tail -1)"
  rec "send-$SN" OK "claim claim /sc:issue --claim $1 $2"
  for i in $(seq 1 "${OB_CLAIM_POLLS:-180}"); do
    raw=$(screen_text claim)
    if printf '%s' "$raw" | grep -qE 'launch_status:|"status"' && ! printf '%s' "$raw" | grep -q 'esc to interrupt'; then break; fi
    if printf '%s' "$raw" | grep -qE 'Do you want|/login|Not logged in'; then pending "step=$SN reason=needs-input name=claim"; fi
    command sleep "${OB_CLAIM_SLEEP_S:-5}"
  done
  CLAIM_SCREEN=$(bash "$here/driver.sh" screen claim)
  raw=$(command timeout "$T" jq -r '.result.terminal.tail // [] | join("\n")' "$CLAIM_SCREEN" 2>/dev/null)
  CLAIM_TXT=$(printf '%s' "$raw" | tr -d ' \t\r\n\\')
  case "$CLAIM_TXT" in
    *'"status":"'*) CLAIM_LAST=${CLAIM_TXT##*\"status\":\"}; CLAIM_STATUS=${CLAIM_LAST%%\"*} ;;
    *launch_status:*)   # the claim prints "launch_status: <value>" lines (seen live); the text after the newest issue_number line is this claim's
      CLAIM_STATUS=$(printf '%s\n' "$raw" | grep -oE 'launch_status: *[a-z_]+' | tail -1 | sed 's/.*: *//')
      CLAIM_LAST=${CLAIM_TXT##*issue_number:}; [ -n "$CLAIM_LAST" ] || CLAIM_LAST=$CLAIM_TXT ;;
    *) pending "reason=claim-unreadable screen=$CLAIM_SCREEN" ;;
  esac
}
claim_has() {  # claim_has <text>: the newest claim result contains that text
  local n; n=$(printf '%s' "$1" | tr -d ' ')
  case "$CLAIM_LAST" in *"$n"*) return 0 ;; esac
  return 1
}
pend_count() { ls -A "$HOME/.claude/state/launch-level/pending" 2>/dev/null | wc -l | tr -d ' '; }

launch_real() {  # launch_real <T1..T4> <flags> <session name> [first-stop wait secs; absent or 0 = do not wait]
  local t=$1 n h label=h2-$1
  need n "$t"
  if [ -n "$(state_get "RESUME_LAUNCH_$t" 2>/dev/null)" ] && [ -s "$OB/claim-$t.txt" ]; then
    # the real launch already happened in an earlier run of this script (its claim text was saved then): do not claim again
    CLAIM_LAST=$(cat "$OB/claim-$t.txt"); CLAIM_STATUS=launched; CLAIM_SCREEN=none
    rec "$sub-resume" OK "launch of $t reused from the saved claim text $OB/claim-$t.txt"
  else
    claim_send "$n" "$2"
    [ "$CLAIM_STATUS" = launched ] || die "$sub-claim" "status=$CLAIM_STATUS screen=$CLAIM_SCREEN"
    printf '%s\n' "$CLAIM_LAST" > "$OB/claim-$t.txt"
    state_set "RESUME_LAUNCH_$t" "$(date -u +%FT%TZ)"
  fi
  claim_has 'L1 guard: effective' && rec "$sub-layers" OK "L1 guard: effective" || rec "$sub-layers" FAIL "no 'L1 guard: effective' line (the claim session printed its own summary; enforcement_hook line: $(printf '%s' "$CLAIM_LAST" | grep -oE 'enforcement_hook:[a-z]+' | head -1))"
  case "$CLAIM_LAST" in
    *'"terminal":"'*) h=${CLAIM_LAST#*\"terminal\":\"}; h=${h%%\"*} ;;
    *) h="" ;;
  esac
  if [ -z "$h" ]; then
    # the real claim output has no terminal key: take the one Orca terminal of this issue's worktree whose title is the launch marker
    h=$(command timeout "$T" orca terminal list --json 2>/dev/null | command timeout "$T" jq -r --arg wt "$(state_get "WT_$t")" \
        '[.result.terminals[] | select(.worktreePath == $wt and ((.title // "") | test("sc-launch")))] | if length == 1 then .[0].handle else empty end' 2>/dev/null)
    [ -z "$h" ] || rec "$sub-terminal" OK "terminal $h found by worktree path and launch title (the claim output has no terminal key)"
  fi
  if [ -z "$h" ]; then
    runlog "claim $t: no terminal key in the claim output; record: $CLAIM_LAST"
    runlog "claim $t: launch record: $(command timeout "$T" jq -c '.launch // "none"' "${MAIN:-.}/.dev/issues/$n/worktree.json" 2>&1)"
    pending "reason=terminal-handle-missing screen=$CLAIM_SCREEN (full record in $PKG_ART/t10-run-log.md)"
  fi
  bash "$here/driver.sh" adopt "$3" "$h" >/dev/null
  GSID=$(wait_gsid "$label") || { rec "$sub-probe-loaded" FAIL "no session_id in $label.jsonl"; exit 1; }
  state_set "GSID_$t" "$GSID"
  rec "$sub-launched" OK "terminal=$h gsid=$GSID"
  # b and c wait for the plan boundary; d and e own longer waits of their own
  [ "${4:-0}" = 0 ] || wait_first_stop "$label" "$4" || pending "reason=no-first-stop label=$label"
}

# --- release: the claim's printed rm, only for this run's GSID --------------------
release_session() {  # release_session <gsid> <claim text>
  local gsid=$1 m p1 p2
  case "$gsid" in ''|*[!0-9A-Za-z_-]*) die release "refusing an odd session id" ;; esac
  m=$(printf '%s' "$2" | grep -oE 'rm"[^"]+""[^"]+"' | tail -1)
  if [ -n "$m" ]; then
    p1=$(printf '%s' "$m" | sed -E 's/^rm"([^"]+)""([^"]+)"$/\1/')
    p2=$(printf '%s' "$m" | sed -E 's/^rm"([^"]+)""([^"]+)"$/\2/')
    p1=${p1//<sessionid>/$gsid}; p2=${p2//<sessionid>/$gsid}
  else
    # the claim session paraphrased the release text (no printed rm line, seen live): the same two files, named from this run's GSID
    rec release-text FAIL "the claim output has no printed rm line; releasing this run's own two session files (UNVERIFIED claim text)"
    p1=$SESS/$gsid; p2=$SESS/$gsid.ok
  fi
  if [ "$p1" != "$SESS/$gsid" ] || [ "$p2" != "$SESS/$gsid.ok" ]; then
    die release "refused: the printed rm paths are not this run's session files ($p1 $p2)"
  fi
  rm -f -- "${p1:?}" "${p2:?}"   # an already-absent file is released, not an error
  if [ ! -e "$p1" ] && [ ! -e "$p2" ]; then rec release OK "$gsid"; else die release "still present: $gsid"; fi
}
plan_path() {  # plan_path <name> <worktree>: the newest .md path on the screen that exists under the worktree or the main checkout
  local p r=""
  for p in $(screen_text "$1" | grep -oE '[A-Za-z0-9_./~-]+\.md' | awk '!s[$0]++'); do
    if [ -f "$2/$p" ] || [ -f "$MAIN/$p" ] || [ -f "$p" ]; then r=$p; fi
  done
  printf '%s' "$r"
}
ok_file_check() {  # ok_file_check <gsid> <id>
  if [ -e "$SESS/$1.ok" ]; then rec "$2" OK "$SESS/$1.ok exists"; else rec "$2" FAIL "$SESS/$1.ok missing"; fi
}

# --- exit-time restores (flags keep them idempotent) --------------------------------
corrupt=0; push_set=0
SETTINGS=""; WT4=""
restore_probe() {  # put the probe file back from the backup (session b)
  [ "$corrupt" = 1 ] || return 0
  cp -- "$BACKUP" "$SETTINGS" && corrupt=0
}
restore_push() {  # runbook lines 690-691, from this shell (the agent must never run it: LL-TAMPER)
  [ "$push_set" = 1 ] || return 0
  tgit -C "$WT4" config --worktree --unset remote.origin.pushurl
  [ "$(state_get worktreeConfigPre)" = true ] || tgit -C "$WT4" config --unset extensions.worktreeConfig
  push_set=0
}
trap 'restore_probe; restore_push' EXIT

# --- session b ------------------------------------------------------------------------
preflight_refusal() {  # preflight_refusal <tag> <needle>: runbook lines 546-552 and 560
  local now sig rec2
  claim_send "$N1" "--pipeline worktree"
  case "$CLAIM_STATUS" in launched|already_launched) die "b-$1" "a refused launch started an agent (status=$CLAIM_STATUS)" ;; esac
  if [ "$CLAIM_STATUS" = failed ] && claim_has W-ENFORCEMENT-ABSENT && claim_has "$2"; then
    rec "b-$1-claim" OK "failed W-ENFORCEMENT-ABSENT"
  else
    rec "b-$1-claim" FAIL "status=$CLAIM_STATUS screen=$CLAIM_SCREEN"
  fi
  now=$(pend_count)
  if [ "$now" = "$PEND0" ]; then rec "b-$1-pending" OK "count $now"; else rec "b-$1-pending" FAIL "before=$PEND0 after=$now"; fi
  sig=$(tgit -C "$WT1" rev-parse --absolute-git-dir)/sc-issue-launch-$N1.json
  if [ ! -e "$sig" ]; then rec "b-$1-no-mirror" OK "$sig absent"; else rec "b-$1-no-mirror" FAIL "$sig exists"; fi
  rec2=$(command timeout "$T" jq -c '.launch // "none"' "$MAIN/.dev/issues/$N1/worktree.json" 2>&1)
  if [ "$rec2" = '"none"' ]; then rec "b-$1-no-record" OK '"none"'; else rec "b-$1-no-record" FAIL "$rec2"; fi
}
ident() {  # ident <id> <pgrep pattern>: record what identify prints for that process
  local pid
  pid=$(pgrep -xf "$2" | head -1)
  if [ -z "$pid" ]; then IDENT_OUT=no-process; rec "$1" PENDING "no process matches: $2"; return 0; fi
  IDENT_OUT=$(command timeout "$T" "$IDENT" identify "$pid" 2>&1 | tr '\n' ' ')
  rec "$1" OK "pid=$pid out=$IDENT_OUT"
}

inode_record() {  # runbook step 2 (lines 576-580): the session file's inode against the number in the claim's release text
  local want have f=$SESS/$GSID
  want=$(printf '%s' "$CLAIM_LAST" | grep -oE 'inodenumber[0-9]+' | head -1 | tr -dc '0-9')
  if [ ! -e "$f" ]; then rec b-inode FAIL "no session file named $GSID in $SESS"; return 0; fi
  have=$(stat -c '%i %h' "$f")
  if [ -z "$want" ]; then
    rec b-inode PENDING "the claim printed no inode number (session file inode ${have%% *}, link count ${have##* }); check by hand which file is this launch's"
  elif [ "${have%% *}" = "$want" ]; then
    rec b-inode OK "session file $GSID holds inode ${have%% *}, equal to the claim's $want; link count ${have##* }"
  else
    rec b-inode FAIL "session file inode ${have%% *} (link count ${have##* }), claim inode ${want:-unreadable}"
  fi
}

run_b() {
  local L=$OB_LOGS/h2-T1 n s path cmd
  need N1 T1; need WT1 WT_T1
  MAIN=${OB_MAIN:-$(main_checkout)}
  SETTINGS=$WT1/.claude/settings.local.json
  if [ -n "$(state_get RESUME_LAUNCH_T1 2>/dev/null)" ]; then
    rec b-steps-1-2-skipped OK "the real launch of T1 already happened in an earlier run; the refusals are not repeated"
  else
  # step 1 starts with the backup (runbook 541); nothing is touched unless it worked
  cp -- "$SETTINGS" "$BACKUP" 2>/dev/null
  [ -s "$BACKUP" ] || die b-backup "t1-local.json missing or empty"
  rec b-backup OK "$BACKUP"
  PEND0=$(pend_count); rec b-pending-before OK "$PEND0"
  corrupt=1
  printf '{' > "$SETTINGS"
  preflight_refusal badjson "settings.local.json cannot be read as JSON"
  printf '{"disableAllHooks": true}' > "$SETTINGS"
  preflight_refusal nohooks "sets disableAllHooks to true, so no hook runs"
  restore_probe
  if cmp -s "$BACKUP" "$SETTINGS"; then rec b-restore OK "byte-equal to the backup"; else die b-restore "restored file differs from the backup"; fi
  fi
  launch_real T1 "--pipeline worktree" gB "${OB_INITIAL_WAIT_S:-900}"
  PLAN_B=$(plan_path gB "$WT1")   # read at the plan boundary, before the prompts echo and the block text add other words
  inode_record
  # step 3: OB-H3 at worktree level
  gsend gB h2-T1 "$(cat "$P/g01-b-implement.txt")" 600
  gsend gB h2-T1 "$(cat "$P/g02-commit.txt")" 600
  # the bare word `approved` is a negative control: this flow does not unlock on it
  gsend gB h2-T1 "$(cat "$P/g03-approved.txt")" 1800
  if [ -e "$SESS/$GSID.ok" ]; then rec b-approved-no-unlock FAIL "$SESS/$GSID.ok exists after the bare word approved"; else rec b-approved-no-unlock OK "no .ok file after the bare word approved"; fi
  # the unlock is a typed /sc:implement <plan path> (same template as session c)
  path=$PLAN_B
  [ -n "$path" ] || pending "reason=plan-path-not-on-screen name=gB"
  cmd=$(cat "$P/g07-c-implement.txt")
  cmd=${cmd/<the plan path it printed>/$path}
  gsend gB h2-T1 "$cmd" 1800
  ok_file_check "$GSID" b-implement-ok
  gsend gB h2-T1 "$(cat "$P/g02-commit.txt")" 600
  # step 4: OB-CTX part 2
  gsend gB h2-T1 "$(cat "$P/g04-gov-bg.txt")" 600
  gsend gB h2-T1 "$(cat "$P/g05-gov-det.txt")" 600
  ident b-id-241 'sleep 241'
  ident b-id-243 'sleep 243'
  rec b-jobs OK "$(ls "$HOME/.claude/state/launch-level/jobs/" 2>/dev/null | wc -l | tr -d ' ') job entries"
  IDENT_OUT=$(cd "$WT1" && command timeout "$T" "$IDENT" identify $$ 2>&1 | tr '\n' ' ')
  rec b-id-human OK "$IDENT_OUT"
  gsend gB h2-T1 '/clear' 120
  gsend gB h2-T1 "$(cat "$P/g06-gov-clear.txt")" 600
  ident b-id-242 'sleep 242'
  ident b-id-241-after-clear 'sleep 241'
  n=$(command timeout "$T" jq -r 'select(.session_id) | .session_id' "$L.jsonl" | uniq | wc -l | tr -d ' ')
  rec b-session-ids OK "$n distinct id runs in the log (a second id after /clear is U18)"
  # release mid step 4 (runbook 635), then the final identify of sleep 241
  release_session "$GSID" "$(cat "$OB/claim-T1.txt")"
  ident b-id-241-released 'sleep 241'
  case "$IDENT_OUT" in
    no-process) : ;;
    *ordinary*released*) rec b-ctx-released OK "ordinary, reason released" ;;
    *) rec b-ctx-released FAIL "$IDENT_OUT" ;;
  esac
  printf 'SESSION_B_DONE\n'
}

# --- session c --------------------------------------------------------------------------
run_c() {
  local s path cmd
  need N2 T2; need WT2 WT_T2
  launch_real T2 "--pipeline worktree" gC "${OB_INITIAL_WAIT_S:-900}"
  MAIN=${OB_MAIN:-$(main_checkout)}
  path=$(plan_path gC "$WT2")
  [ -n "$path" ] || pending "reason=plan-path-not-on-screen name=gC"
  cmd=$(cat "$P/g07-c-implement.txt")
  cmd=${cmd/<the plan path it printed>/$path}
  gsend gC h2-T2 "$cmd" 1800
  ok_file_check "$GSID" c-implement-ok
  gsend gC h2-T2 "$(cat "$P/g02-commit.txt")" 600
  release_session "$GSID" "$(cat "$OB/claim-T2.txt")"
  printf 'SESSION_C_DONE\n'
}

# --- session d --------------------------------------------------------------------------
final_status_seen() {  # a Bash call with `git status --short`, then a Stop after it
  local r
  r=$(command timeout "$T" jq -s '
    to_entries
    | (map(select(.value.hook_event_name == "PreToolUse" and .value.tool_name == "Bash"
                  and ((.value.tool_input.command // "") | test("git status --short"))))
       | last | .key // null) as $i
    | if $i == null then false
      else (.[($i + 1):] | map(select(.value.hook_event_name == "Stop")) | length > 0) end' \
    "$OB_LOGS/h2-T3.jsonl" 2>/dev/null)
  [ "$r" = true ]
}
run_d() {
  local end
  need N3 T3; need WT3 WT_T3
  MAIN=${OB_MAIN:-$(main_checkout)}
  launch_real T3 "--pipeline full" gD
  end=$(( $(date +%s) + ${OB_D_WAIT_S:-5400} ))
  until final_status_seen; do
    [ "$(date +%s)" -ge "$end" ] && pending "reason=no-final-git-status-within-90-minutes label=h2-T3"
    command sleep "$POLL"
  done
  rec d-final-status OK "agent ended with git status --short"
  gsend gD h2-T3 "$(cat "$P/g02-commit.txt")" 600
  release_session "$GSID" "$(cat "$OB/claim-T3.txt")"
  printf 'SESSION_D_DONE\n'
}

# --- session e --------------------------------------------------------------------------
PR_RE='https://github\.com/[^/ "\\]+/[^/ "\\]+/pull/[0-9]+'
find_pr_url() {  # the pull request URL of THIS run: a fork URL whose head branch is the T4 worktree branch
  local u br wtbr cands
  wtbr=$(tgit -C "$WT4" rev-parse --abbrev-ref HEAD 2>/dev/null)
  cands=$({ grep -ohE "$PR_RE" "$OB_LOGS/h2-T4.jsonl" 2>/dev/null; screen_text gE | grep -oE "$PR_RE"; } | awk '!s[$0]++' | head -20)
  for u in $cands; do   # an upstream URL is returned as it is, so the caller refuses it
    case "${u,,}" in *superclaude-org*) printf '%s' "$u"; return 0 ;; esac
  done
  for u in $cands; do
    case "$u" in https://github.com/IronbellyOrg/IronClaude/pull/[0-9]*) ;; *) continue ;; esac
    br=$(gh_fork pr view "${u##*/}" --json headRefName -q .headRefName 2>/dev/null) || continue
    if [ -n "$wtbr" ] && [ "$br" = "$wtbr" ]; then printf '%s' "$u"; return 0; fi
  done
  return 0
}
cycle_ended() {  # a Stop at or after the last pr-submit line, and a quiet log
  local f=$OB_LOGS/h2-T4.jsonl last stops
  last=$(grep -n 'pr-submit' "$f" 2>/dev/null | tail -1 | cut -d: -f1)
  [ -n "$last" ] || return 1
  stops=$(tail -n +"$last" "$f" | grep -c '"hook_event_name":"Stop"' || true)
  [ "${stops:-0}" -ge 1 ] || return 1
  [ $(( $(date +%s) - $(stat -c %Y "$f") )) -ge "${OB_QUIET_S:-120}" ]
}
fire_o10() {  # O-10: stand-in for the web UI edit, via the contents API (path first, then flags)
  local num=${1##*/} br wtbr sha args
  br=$(gh_fork pr view "$num" --json headRefName -q .headRefName 2>/dev/null) || br=""
  [ -n "$br" ] || { rec e-o10 FAIL "no head branch for pull request $num"; state_set O10 failed; return 0; }
  # the log holds everything the agent read, so write only to the disposable branch
  wtbr=$(tgit -C "$WT4" rev-parse --abbrev-ref HEAD 2>/dev/null)
  if [ "$br" != "$wtbr" ]; then
    rec e-o10 FAIL "pull request $num head branch $br is not the T4 worktree branch ${wtbr:-unknown}; no write made"
    state_set O10 skipped; return 0
  fi
  sha=$(gh_fork api "repos/IronbellyOrg/IronClaude/contents/ob-442/T4.txt?ref=$br" --jq .sha 2>/dev/null) || sha=""
  args=(-X PUT -f "message=ob-442 O-10 edit" -f "content=$(printf 'ob-442 T4\nob-442 o10 edit\n' | base64 -w0)" -f "branch=$br")
  [ -z "$sha" ] || args+=(-f "sha=$sha")
  if gh_fork api repos/IronbellyOrg/IronClaude/contents/ob-442/T4.txt "${args[@]}" >/dev/null 2>&1; then
    state_set O10 fired
    rec e-o10 OK "edit on $br via the contents API; stand-in for the web UI edit, and whether /sc:pr-submit reacts the same way is UNVERIFIED"
  else
    state_set O10 failed
    rec e-o10 FAIL "contents API call failed on $br"
  fi
}
push_url_is_bare() { [ "$(tgit -C "$WT4" remote get-url --push origin 2>/dev/null)" = "$BARE" ]; }

run_e() {
  local url end o10=0
  need N4 T4; need WT4 WT_T4
  MAIN=${OB_MAIN:-$(main_checkout)}
  launch_real T4 "--pipeline full --submit" gE
  end=$(( $(date +%s) + ${OB_E_WAIT_S:-5400} ))
  url=""
  while :; do
    [ -n "$url" ] || url=$(find_pr_url)
    if [ -n "$url" ] && [ "$o10" = 0 ]; then
      case "$url" in
        https://github.com/IronbellyOrg/IronClaude/pull/[0-9]*) rec e-pr-url OK "$url"; state_set PR_URL "$url" ;;
        *) printf 'FAIL misrouted-pr %s\n' "$url" | tee -a "$GOVLOG"; rec e-pr-url FAIL "misrouted-pr $url; no action taken on it"; exit 5 ;;
      esac
      fire_o10 "$url"; o10=1
    fi
    if [ -n "$url" ] && cycle_ended; then break; fi
    [ "$(date +%s)" -ge "$end" ] && pending "reason=cycle-not-ended O-10=pending url=${url:-none} label=h2-T4"
    command sleep "$POLL"
  done
  rec e-cycle OK "a Stop follows the last pr-submit line (heuristic, UNVERIFIED)"
  # the refused protected push and merge: only after the cycle (runbook 665-692)
  state_set worktreeConfigPre "$([ "$(tgit -C "$WT4" config --get extensions.worktreeConfig 2>/dev/null)" = true ] && echo true || echo unset)"
  push_set=1
  [ "$(state_get worktreeConfigPre)" = true ] || tgit -C "$WT4" config extensions.worktreeConfig true
  tgit -C "$WT4" config --worktree remote.origin.pushurl "$BARE"
  if push_url_is_bare; then rec e-push-url OK "$BARE"; else die e-push-url "the worktree push URL is not $BARE"; fi
  rec e-main-push-url OK "$(tgit -C "$MAIN" remote get-url --push origin 2>&1)"
  # the push prompt goes out only if the URL still reads as the bare repository right now
  push_url_is_bare || { rec e-push-refused FAIL "REFUSED push prompt: push URL is not $BARE"; exit 6; }
  gsend gE h2-T4 "$(cat "$P/g08-e-push.txt")" 600
  gsend gE h2-T4 "$(cat "$P/g09-e-merge.txt")" 600
  restore_push
  rec e-versions OK "claude=$(command timeout "$T" claude --version 2>&1 | head -1) orca=$(command timeout "$T" orca --version 2>&1 | head -1) sha=$(command timeout "$T" sha256sum "$HOME/.claude/settings.json" "$HOME/.claude/hooks/launch-level-guard.sh" 2>&1 | tr '\n' ' ')"
  release_session "$GSID" "$(cat "$OB/claim-T4.txt")"
  printf 'SESSION_E_DONE\n'
}

"run_$sub"
