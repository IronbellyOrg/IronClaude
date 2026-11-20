#!/usr/bin/env bash
# evidence.sh <1..9|h2|h3|ctx|all> | --print-filters | --reading <u20|retry-f7-f8|ac7> <text> [screen file]
# Runs the runbook's evidence commands against $OB/logs, classifies each item by its
# PASS rule, and drafts .dev/issues/442/observation-results.md (section 4.1 template).
# `all` writes the file (a rerun replaces it) and then copies logs, screens and state
# to $PKG_ART/ob-logs after a secret scan. A single item prints its block to stdout.
# Plan Task 7. Classification is by jq/awk over the logs; a part that needs a person is
# marked `needs reading` and keeps its item pending until `--reading` records it.
set -u -o pipefail
umask 077
here=$(cd -- "$(dirname -- "$0")" && pwd)
# shellcheck source=lib.sh
source "$here/lib.sh"
RB=$(cd -- "$here/.." && pwd)/observation-runbook.md
RESULTS=${OB_RESULTS:-$(cd -- "$here/.." && pwd)/observation-results.md}
T=${OB_TIMEOUT_S:-60}
LOGS=$OB_LOGS
GOVLOG=$OB/gov-log.txt
READINGS=$OB/readings.txt
SECRET_RE='gh[pousr]_[A-Za-z0-9]{20,}|github_pat_|sk-[A-Za-z0-9]|CLICKUP_API_TOKEN=|Bearer |Authorization:|-----BEGIN|_TOKEN=|_KEY='
# The words "task-notification", "task-id" and "task-type" hold "sk-n", "sk-i", "sk-t"; neutralise every "task-" before a match and restore it after.
neutral() { sed -E 's/task-/task\x01/g'; }

# --- runbook extraction (the commands run are the runbook's own text) -------------------
section_block() {  # section_block <heading regex> <marker regex>: the first ```bash block after the marker
  awk -v h="$1" -v m="$2" '
    !inh && $0 ~ h { inh = 1; next }
    inh && !seen && $0 ~ m { seen = 1; next }
    seen && !inb && $0 == "```bash" { inb = 1; next }
    inb && $0 == "```" { exit }
    inb { print }' "$RB" | sed "s#/tmp/ob#$OB#g"
}
filter_text() {  # filter_text <n>: the text of filter F<n> from the block at runbook section 2.2.0
  section_block '^### 2\.2\.0|^#### 2\.2\.0' '^In the evidence terminal set' \
    | awk -v n="$1" '$0 ~ "^# F" n ":" { on = 1 } on && /^# F[0-9]+:/ && $0 !~ "^# F" n ":" { exit } on { print }'
}
case "${1:-}" in
  --print-filters)
    for n in 1 2 3 4 5 6 7 8; do filter_text "$n"; done
    exit 0 ;;
  --reading)
    [ $# -ge 3 ] || { printf 'usage: evidence.sh --reading <u20|retry-f7-f8|ac7> <text> [screen file]\n' >&2; exit 2; }
    case "$2" in u20|retry-f7-f8|ac7) ;; *) printf 'evidence: unknown reading key %s\n' "$2" >&2; exit 2 ;; esac
    mkdir -p "$OB"; touch "$READINGS"
    { grep -v "^$2	" "$READINGS" || true; printf '%s\t%s\t%s\n' "$2" "$3" "${4:-}"; } > "$READINGS.new" && mv "$READINGS.new" "$READINGS"
    printf 'READING %s recorded\n' "$2"
    exit 0 ;;
esac
sel=${1:-}
case "$sel" in 1|2|3|4|5|6|7|8|9|h2|h3|ctx|all) ;; *) printf 'usage: evidence.sh <1..9|h2|h3|ctx|all>\n' >&2; exit 2 ;; esac

# --- small helpers ------------------------------------------------------------------------
redact() { neutral | sed -E "s/.*($SECRET_RE).*/[line withheld: secret pattern]/" | sed 's/\x01/-/g'; }
run_text() {  # run_text <command text> [L]: run extracted text, redacted before it is cut
  L="${2:-}" MAIN="${MAIN_ID:-}" OB="$OB" command timeout "$T" bash -c "$1" 2>&1 | redact | cut -c1-240
}
jqs() { command timeout "$T" jq -s -r "$2" "${@:3}" "$1" 2>/dev/null; }          # jqs <prog> <file> [--arg ...]
jqs_files() { local prog=$1; shift; command timeout "$T" jq -s -r "$prog" "$@" 2>/dev/null; }
reading_of() { awk -F'\t' -v k="$1" '$1 == k { print $2; exit }' "$READINGS" 2>/dev/null; }
reading_screen() { awk -F'\t' -v k="$1" '$1 == k { print $3; exit }' "$READINGS" 2>/dev/null; }
gov_status() { awk -v id="$1" '($1 == "OK" || $1 == "FAIL" || $1 == "PENDING") && $2 == id { s = $1 } END { print s }' "$GOVLOG" 2>/dev/null; }
gov_detail() { awk -v id="$1" '($1 == "OK" || $1 == "FAIL" || $1 == "PENDING") && $2 == id { $1 = ""; $2 = ""; d = $0 } END { sub(/^ +/, "", d); print d }' "$GOVLOG" 2>/dev/null; }
first_lines() { grep -n -m3 -E "$2" "$1" 2>/dev/null | cut -d: -f1 | tr '\n' ',' | sed 's/,$//'; }
blocked_screens() {  # blocked_screens <prefix>: up to 3 newest screen files that show a Blocked: line
  local f out=""
  for f in $(ls -1t "$OB_SCREENS"/"$1"-*.json 2>/dev/null); do
    if command timeout "$T" jq -r '.result.terminal.tail // [] | join("\n")' "$f" 2>/dev/null | grep -q '^Blocked:'; then out="$out $f"; fi
  done
  printf '%s' "$out" | tr ' ' '\n' | sed '/^$/d' | head -3 | tr '\n' ' '
}

# the parts of one item: each part is PASS, FAIL or pending
PARTS=""; ANYFAIL=0; ANYPEND=0
part() {  # part <label> <PASS|FAIL|pending> <detail>
  PARTS="$PARTS
  - $1: $2 ($3)"
  case "$2" in FAIL) ANYFAIL=1 ;; pending) ANYPEND=1 ;; esac
}
from_rule() {  # from_rule <label> <"RES|why">
  local r=${2%%|*} w=${2#*|}
  [ -n "$2" ] || { r=pending; w="no log or unreadable log"; }
  part "$1" "$r" "$w"
}
finish() { if [ "$ANYFAIL" = 1 ]; then RES=FAIL; elif [ "$ANYPEND" = 1 ]; then RES=pending; else RES=PASS; fi; }

MAIN_ID=""
[ -s "$LOGS/h1.jsonl" ] && MAIN_ID=$(command timeout "$T" jq -r 'select(.hook_event_name=="SessionStart") | .session_id' "$LOGS/h1.jsonl" 2>/dev/null | head -1)

# --- the typed-prompt set of session A (item 5 compares against it) ------------------------
typed_json() {
  { for f in "$here"/prompts/p*.txt; do [ -e "$f" ] && command timeout "$T" jq -Rs 'sub("\\s+$";"")' "$f"; done
    printf '"%s"\n' '/hooks' '/sc:implement x' '/exit' 'say ok' '/clear'
  } | command timeout "$T" jq -s .
}

# --- per-item rules ---------------------------------------------------------------------------
# Each item sets NAME CMD OUT SESSION LOGREF TAB and the parts, then finish.
item_1() {
  local f=$LOGS/h1.jsonl
  CMD=$(section_block '^#### OB-H1 item 1:' '^Evidence:'); SESSION=A; LOGREF="$f: lines $(awk '/"hook_event_name":"PreToolUse"/ && /ob-item1-(sub|nested)"/ {printf "%s%d", s, NR; s=","}' "$f")"   # the evidence rows, not the prompt line that also names ob-item1
  OUT=$(run_text "$CMD"); [ -s "$f" ] || { part log pending "log file missing: $f"; return; }
  from_rule "parent session_id in subagent payloads" "$(jqs "$f" '
    [.[]|select(.hook_event_name=="PreToolUse" and .tool_name=="Bash" and ((.tool_input.command // "")|test("ob-item1")))] as $l
    | ([$l[]|select((.tool_input.command // "")|test("ob-item1-sub"))]|length) as $s
    | ([$l[]|select((.tool_input.command // "")|test("ob-item1-nested"))]|length) as $n
    | if ($l|length)==0 then "pending|no ob-item1 line in the log"
      elif $main=="" then "pending|no SessionStart line, so MAIN is unknown"
      elif any($l[]; (.session_id // "") != $main) then "FAIL|a line has a session_id that differs from MAIN or is missing (design O-9: no full or --submit claim on a real issue; report to the owner)"
      elif $s==0 or $n==0 then "pending|the nested line is absent (record the subagent reply if it has no Agent tool)"
      elif any($l[]; ((.agent_id // "")=="" or (.agent_type // "")=="")) then "pending|agent_id or agent_type is empty"
      else "PASS|both lines carry session_id equal to MAIN, with agent_id and agent_type" end' --arg main "$MAIN_ID")"
}
item_2() {
  local f=$LOGS/h1.jsonl
  CMD=$(section_block '^#### OB-H1 item 2:' '^Press Esc if'); SESSION=A; LOGREF="$f: lines $(first_lines "$f" '"tool_name":"Skill"')"
  OUT=$(run_text "$CMD")
  [ -s "$f" ] || { part log pending "log file missing: $f"; return; }
  from_rule "Skill call keys and name form" "$(jqs "$f" '
    [.[]|select(.hook_event_name=="PreToolUse" and .tool_name=="Skill")
      |{raw:(.tool_input.skill // .tool_input.name // ""), norm:((.tool_input.skill // .tool_input.name // "")|(capture("^\\s*(?<w>\\S*)").w // "")|ascii_downcase|sub("^/";"")|(split(":")|.[-1] // "")|sub("^sc-";"")|sub("-protocol$";""))}] as $l
    | if ($l|length)<2 then "pending|fewer than two Skill calls ("+($l|length|tostring)+")"
      elif any($l[]; .raw=="" or .norm!="implement") then "FAIL|a Skill call has no name under skill or name, or norm is not implement (the guard would block every skill as LL-SKILL)"
      else "PASS|every Skill call has its name under skill or name and norm is implement" end')"
}
item_3() {
  local f=$LOGS/h1.jsonl
  CMD=$(section_block '^#### OB-H1 item 3:' '^Evidence:'); SESSION=A; LOGREF="$f: lines $(first_lines "$f" '"isolation"')"
  OUT=$(run_text "$CMD"); [ -s "$f" ] || { part log pending "log file missing: $f"; return; }
  from_rule "Agent tool name and the isolation key" "$(jqs "$f" '
    [.[]|select(.hook_event_name=="PreToolUse" and (.tool_name=="Agent" or .tool_name=="Task"))] as $l
    | if ($l|length)==0 then "pending|no Agent or Task call in the log"
      elif any($l[]; .tool_input.isolation=="worktree") then "PASS|tool name "+([$l[]|select(.tool_input.isolation=="worktree")][0].tool_name)+" carries isolation=worktree"
      elif any($l[]; (.tool_input|keys|map(select(test("isol";"i") and (. != "isolation")))|length)>0) then "FAIL|the isolation choice arrives under another key (the guard would miss a remote subagent; report to the owner)"
      else "pending|no call set isolation; ask once more and record the reply" end')"
}
item_4() {
  local f=$LOGS/h1.jsonl
  CMD=$(section_block '^#### OB-H1 item 4:' '^Evidence:'); SESSION=A; LOGREF="$f: lines $(first_lines "$f" 'sc:implement x')"
  OUT=$(run_text "$CMD"); [ -s "$f" ] || { part log pending "log file missing: $f"; return; }
  from_rule "typed /sc:implement x, prompt event before expansion" "$(jqs "$f" '
    to_entries as $e
    | [$e[]|select(.value.hook_event_name=="UserPromptSubmit" and (((.value.prompt // "")|split("\n")[0])=="/sc:implement x"))|.key] as $u
    | [$e[]|select(.value.hook_event_name=="UserPromptExpansion" and ((.value.command_name // "")|test("implement")))|.key] as $x
    | [$e[]|select(.value.hook_event_name=="PreToolUse" and .value.tool_name=="Skill" and ((.value.tool_input.skill // .value.tool_input.name // "")|test("implement")))|.key] as $s
    | if ($u|length)==0 then (if ($x|length)>0 then "FAIL|the UserPromptSubmit prompt is not the typed line but an expansion event fired (record its command_name; design fallback FR-L-18)" else "pending|no /sc:implement x prompt line" end)
      elif (any($x[]; . < $u[0]) or any($s[]; . < $u[0])) then "FAIL|an expansion or Skill line comes before the prompt line"
      else "PASS|the first prompt line is /sc:implement x and it precedes the expansion and Skill lines" end')"
}
item_5() {
  local f=$LOGS/h1.jsonl
  CMD=$(section_block '^#### OB-H1 item 5:' '^Evidence'); SESSION=A; LOGREF="$f: lines $(first_lines "$f" 'UserPromptSubmit')"
  OUT=$(run_text "$CMD"); [ -s "$f" ] || { part log pending "log file missing: $f"; return; }
  from_rule "self-started turns carry no bare Approved" "$(jqs "$f" '
    [.[]|select(.hook_event_name=="UserPromptSubmit")
      |((.prompt // "")|gsub("^\\s+|\\s+$";"")) as $p
      |{p:$p, b:($p|ascii_downcase|test("^approved[.!]?$")), i:((.prompt // "")|split("\n")[0]|test("^\\s*/(sc:implement|sc:task|task)(\\s|$)"))}] as $l
    | [$l[]|select(.p as $p | ($typed|any(.[]; . == $p))|not)] as $u
    | if ($l|length)==0 then "pending|no UserPromptSubmit lines"
      elif any($u[]; .b) then "FAIL|a prompt that was not typed is a bare Approved: a self-started turn would approve a worktree-level session (no claim at any level; design O-17 applies; report to the owner)"
      elif any($u[]; .i) then "FAIL|a prompt that was not typed starts with an implement command"
      elif ($probes|any(.[]; . as $x | ($l|any(.p == $x))|not)) then "pending|the three background-notice probes (prompts p04, p05, p06) did not all run, so self-started turns were not exercised"
      else "PASS|"+($u|length|tostring)+" prompt line(s) not typed by the run, none a bare Approved or an implement line"+(if ($u|length)==0 then " (no prompt event fires for notices)" else "" end) end' --argjson typed "$(typed_json)" --argjson probes "$(for n in p04-item5a p05-item5b p06-item5c; do command timeout "$T" jq -Rs 'sub("\\s+$";"")' "$here/prompts/$n.txt"; done | command timeout "$T" jq -s .)")"
}
item_6() {
  local f=$LOGS/h1.jsonl M tc seen n r bad="" missing=""
  CMD=$(section_block '^#### OB-H1 item 6:' '^Evidence'); SESSION=A; LOGREF="$f: PreToolUse tool names"
  OUT=$(run_text "$CMD"); [ -s "$f" ] || { part log pending "log file missing: $f"; return; }
  M=$(command timeout "$T" jq -r '.hooks.PreToolUse[]|select(any(.hooks[];.command|test("launch-level-guard")))|.matcher' "$HOME/.claude/settings.json" 2>/dev/null | head -1)
  [ -n "$M" ] || { part "guard matcher" pending "no launch-level-guard PreToolUse registration found in $HOME/.claude/settings.json"; return; }
  seen=$(L="" command timeout "$T" bash -c "$CMD" 2>/dev/null)
  tc=$(printf '%s\n' "$seen" | awk '$1 == "TaskCreate" { print $2 }')
  [ -n "$tc" ] || { part "TaskCreate" pending "TaskCreate not seen in the log (the model may not offer it in this version)"; }
  [ "$tc" != match ] || bad="TaskCreate shows match"
  for n in Bash Skill Edit Write Monitor SendMessage; do
    r=$(printf '%s\n' "$seen" | awk -v n="$n" '$1 == n { print $2 }')
    [ -n "$r" ] || { missing="$missing $n"; continue; }
    [ "$r" = match ] || bad="$bad; $n shows no-match"
  done
  r=$(printf '%s\n' "$seen" | awk '$1 == "Agent" || $1 == "Task" { print $2 }' | sort -u | tr '\n' ' ')
  [ -n "$r" ] || missing="$missing Agent-or-Task"
  case "$r" in *no-match*) bad="$bad; Agent or Task shows no-match" ;; esac
  if [ -n "$bad" ]; then part "matcher rows" FAIL "$bad"
  elif [ -n "$missing" ] || [ -z "$tc" ]; then part "matcher rows" pending "not seen in the log:${missing:- TaskCreate}"
  else part "matcher rows" PASS "TaskCreate no-match; every guarded tool match (grep -E may differ from the Claude Code matcher: UNVERIFIED)"; fi
}
item_7() {
  local f1=$LOGS/h1.jsonl f2=$LOGS/h1m.jsonl
  CMD=$(section_block '^### 2\.1b' '^Evidence \(both logs\)'); SESSION="A, A2"; LOGREF="$f1, $f2: SendMessage and mcp__ tool names"
  OUT=$(run_text "$CMD")
  [ -s "$f1" ] || [ -s "$f2" ] || { part log pending "no log file: $f1, $f2"; return; }
  from_rule "SendMessage and MCP tool names" "$(jqs_files '
    [.[]|select(.hook_event_name=="PreToolUse")|.tool_name] as $n
    | if any($n[]; (startswith("mcp__")|not) and (test("send_?message";"i")) and . != "SendMessage") then "FAIL|SendMessage arrives in another form"
      elif any($n[]; contains("__") and (startswith("mcp__")|not)) then "FAIL|an MCP tool arrives in a form other than mcp__<server>__<tool>"
      elif (any($n[]; . == "SendMessage")|not) then "pending|no SendMessage call (record that the model has no SendMessage tool)"
      elif (any($n[]; startswith("mcp__"))|not) then "pending|no MCP tool call (no MCP server)"
      else "PASS|SendMessage arrives as SendMessage and MCP tools as mcp__<server>__<tool>: "+([$n[]|select(startswith("mcp__"))]|unique|join(", ")) end' "$f1" "$f2")"
}
item_8() {
  local f=$LOGS/h1.jsonl
  CMD=$(section_block '^#### OB-H1 item 8:' '^Evidence:'); SESSION=A; LOGREF="$f: lines $(first_lines "$f" 'ob-item8')"
  OUT=$(run_text "$CMD"); [ -s "$f" ] || { part log pending "log file missing: $f"; return; }
  from_rule "claude without -p runs no turn" "$(jqs "$f" '
    to_entries as $e
    | [$e[]|select(.value.hook_event_name=="PreToolUse" and .value.tool_name=="Bash" and ((.value.tool_input.command // "")|test("ob-item8")))] as $p
    | if ($p|length)==0 then "pending|the claude command is not logged"
      elif ($p[0].value.tool_input.command) != $typed then "pending|the logged command differs from the typed command"
      else $p[0] as $c
        | ([$e[]|select(.key>$c.key and .value.hook_event_name=="PostToolUse" and ((.value.tool_input.command // "")==$c.value.tool_input.command))][0]) as $post
        | if $post==null then "pending|no PostToolUse for the command, so its output is unknown"
          else ($post.value.tool_response|tostring) as $resp
            | if ([$e[]|select(.key>$c.key and .key<$post.key and .value.hook_event_name=="Stop" and .value.session_id!=$c.value.session_id)]|length)>0 then "FAIL|a new session_id has a Stop line while the command ran (a claude command without a launch flag can run a turn outside the launch level; report to the owner)"
              elif ($resp|test("ob-item8")) then "FAIL|the output contains ob-item8"
              else "PASS|the command is logged as typed; no new session_id with a Stop line; no ob-item8 reply; output: "+($resp|.[0:80]) end end end' \
    --arg typed 'timeout 60 claude "reply with the single word ob-item8" < /dev/null')"
}
item_9() {
  local f=$LOGS/h1.jsonl
  CMD=$(section_block '^#### OB-H1 item 9:' '^Evidence:'); SESSION=A; LOGREF="$f: PreToolUse tool names"
  OUT=$(run_text "$CMD"); [ -s "$f" ] || { part log pending "log file missing: $f"; return; }
  from_rule "tool names of Bash, Edit, Write and Skill" "$(jqs "$f" '
    [.[]|select(.hook_event_name=="PreToolUse")|.tool_name] | unique as $n
    | if any($n[]; test("^mcp__.*_(Bash|Edit|Write|Skill)$")) then "FAIL|a wrapped name such as mcp__<server>__<word>_Bash is not matched by the guard and would be allowed (design U21)"
      elif (["Bash","Edit","Write","Skill"] - $n | length) > 0 then "pending|not seen: "+((["Bash","Edit","Write","Skill"] - $n)|join(", "))
      else "PASS|the names Bash, Edit, Write and Skill appear exactly" end')"
}

# transcript path of a probe log (U27, UNVERIFIED), and Blocked: text counts in screens and transcript
code_seen() {  # code_seen <log> <screen prefix> <Blocked: text start>: count in screens plus transcript
  local log=$1 pre=$2 text=$3 tp n=0 f c
  for f in "$OB_SCREENS"/"$pre"-*.json; do
    [ -e "$f" ] || continue
    c=$(command timeout "$T" jq -r '.result.terminal.tail // [] | join("\n")' "$f" 2>/dev/null | grep -cF "Blocked: $text" || true); n=$((n + ${c:-0}))
  done
  tp=$(command timeout "$T" jq -r 'select(.transcript_path) | .transcript_path' "$log" 2>/dev/null | head -1)
  if [ -n "$tp" ] && [ -f "$tp" ]; then c=$(grep -cF "Blocked: $text" "$tp" || true); n=$((n + ${c:-0})); fi
  printf '%s' "$n"
}
tool_counts() {  # tool_counts <log> <tool> <regex> -> "pre post" (matched by command or skill text)
  local pre post
  pre=$(jqs "$1" '[.[]|select(.hook_event_name=="PreToolUse" and .tool_name==$t and ((.tool_input.command // .tool_input.skill // .tool_input.name // "")|test($r)))]|length' --arg t "$2" --arg r "$3")
  post=$(jqs "$1" '[.[]|select(.hook_event_name=="PostToolUse" and .tool_name==$t and ((.tool_input.command // .tool_input.skill // .tool_input.name // "")|test($r)))]|length' --arg t "$2" --arg r "$3")
  printf '%s %s' "${pre:-0}" "${post:-0}"
}
blocked_part() {  # blocked_part <label> <log> <screen prefix> <tool> <regex> <min blocked> <code text>
  local c pre post seen
  [ -s "$2" ] || { part "$1" pending "log file missing: $2"; return; }
  c=$(tool_counts "$2" "$4" "$5"); pre=${c% *}; post=${c#* }
  if [ "${8:-}" != lax ] && [ "$post" -gt 0 ]; then part "$1" FAIL "the call ran ($post PostToolUse line(s)); the guard did not block it"; return; fi
  if [ "$pre" -lt "$6" ]; then part "$1" pending "$pre attempt(s) logged, $6 expected"; return; fi
  seen=$(code_seen "$2" "$3" "$7")
  if [ "$seen" -gt 0 ]; then part "$1" PASS "$pre blocked attempt(s) with no PostToolUse; 'Blocked: $7' seen $seen time(s)"
  else part "$1" pending "$pre blocked attempt(s) with no PostToolUse, but no 'Blocked: $7' text in a screen or transcript (needs reading)"; fi
}

item_h2() {
  local l=$LOGS/h2-T1 f1 f2 f3 st line
  SESSION="A (LL-NOBIND), B"; LOGREF="$l.jsonl: lines $(first_lines "$l.jsonl" 'sc-launch')"
  CMD="$(filter_text 1)
$(filter_text 2)
$(filter_text 3)
$(filter_text 4)
$(section_block '^#### LL-NOBIND visibility' 'The probe line is still logged:')"
  OUT=$({ for n in 1 2 3 4; do printf '# F%s\n' "$n"; run_text "$(filter_text "$n")" "$l"; done
          printf '# LL-NOBIND\n'; run_text "$(section_block '^#### LL-NOBIND visibility' 'The probe line is still logged:')" ""
          printf '# launch preflight and inode records\n'; grep -E ' b-(badjson|nohooks|inode|approved-ok|backup|restore)' "$GOVLOG" 2>/dev/null | grep -v '^BEGIN' | cut -c1-200; } | redact)
  TAB=$(blocked_screens sA)
  [ -s "$l.jsonl" ] || { part log pending "log file missing: $l.jsonl"; return; }
  f1=$(command timeout "$T" bash -c "L=$l; $(filter_text 1)" 2>/dev/null | head -1)
  if printf '%s' "$f1" | command timeout "$T" jq -e '.marker_at | numbers' >/dev/null 2>&1; then part "F1 strict marker present in the first prompt" PASS "$f1"
  elif [ -n "$f1" ]; then part "F1 strict marker present in the first prompt" FAIL "marker_at is null: $f1"
  else part "F1 strict marker present in the first prompt" pending "no UserPromptSubmit line"; fi
  [ -s "$l.env.jsonl" ] || { part "F2 session file at the first tool call" pending "env log missing: $l.env.jsonl"; }
  f2=$(command timeout "$T" bash -c "L=$l; $(filter_text 2)" 2>/dev/null | head -1)
  case "$f2" in
    *'"session_file":"worktree"'*) part "F2 session file at the first tool call" PASS "$f2" ;;
    *'<no-session-file>'*) part "F2 session file at the first tool call" FAIL "the first tool call ran before the bind: $f2" ;;
    '') [ -s "$l.env.jsonl" ] && part "F2 session file at the first tool call" pending "no PreToolUse line" ;;
    *) part "F2 session file at the first tool call" FAIL "session_file is not worktree: $f2" ;;
  esac
  f3=$(command timeout "$T" bash -c "L=$l; $(filter_text 3)" 2>/dev/null)
  if [ -z "$f3" ]; then part "F3 hook HOME and CLAUDE_CONFIG_DIR" pending "no env lines"
  elif printf '%s\n' "$f3" | awk -F'\t' -v h="$HOME" '{ sub(/^ *[0-9]+ /, "", $1) } !($1 == h && ($2 == "<unset>" || $2 == h "/.claude")) { bad = 1 } END { exit bad }'; then
    part "F3 hook HOME and CLAUDE_CONFIG_DIR" PASS "every line shows the real home and an unset or default CLAUDE_CONFIG_DIR"
  else part "F3 hook HOME and CLAUDE_CONFIG_DIR" FAIL "a line differs from $HOME: $(printf '%s' "$f3" | head -2 | tr '\n' ' ')"; fi
  st=$(gov_status b-inode)
  case "$st" in OK) part "session file inode equals the claim's" PASS "$(gov_detail b-inode)" ;; FAIL) part "session file inode equals the claim's" FAIL "$(gov_detail b-inode)" ;; *) part "session file inode equals the claim's" pending "no record of session b step 2 in $GOVLOG" ;; esac
  for line in badjson nohooks; do
    st=PASS
    for k in claim pending no-mirror no-record; do
      case "$(gov_status b-$line-$k)" in OK) ;; '') [ "$st" = FAIL ] || st=pending ;; *) st=FAIL ;; esac
    done
    part "launch preflight refusal ($line)" "$st" "claim failed with W-ENFORCEMENT-ABSENT; no pending entry, mirror or launch record (gov-log b-$line-*)"
  done
  if grep -q '"hook_event_name":"UserPromptSubmit".*sc-launch' "$LOGS/h1.jsonl" 2>/dev/null; then part "LL-NOBIND prompt logged in session A" PASS "the probe line is in h1.jsonl"; else part "LL-NOBIND prompt logged in session A" pending "no sc-launch prompt line in $LOGS/h1.jsonl"; fi
  if [ -n "$(reading_of u20)" ]; then TAB="$TAB reading u20: $(reading_of u20) (screen $(reading_screen u20))"; part "LL-NOBIND visible on screen (U20)" PASS "reading recorded"
  else part "LL-NOBIND visible on screen (U20)" pending "needs reading: record it with evidence.sh --reading u20 <text> <screen file>"; fi
}
item_h3() {
  local c e
  SESSION="B, C, D, E"; LOGREF="$LOGS/h2-T1..T4.jsonl"
  CMD="$(filter_text 5)
$(filter_text 6)
$(filter_text 7)
$(filter_text 8)"
  OUT=$({ for t in T3 T4; do for n in 5 6 7 8; do printf '# F%s %s\n' "$n" "$t"; run_text "$(filter_text "$n")" "$LOGS/h2-$t"; done; done; } | redact)
  TAB="$(blocked_screens gB) $(blocked_screens gC) $(blocked_screens gD) $(blocked_screens gE)"
  # session B step 3: the implement block before the approval, the commit block twice, the unlock
  # lax: after the typed /sc:implement the implement step runs, so a later PostToolUse is expected
  blocked_part "B implement blocked (LL-IMPL)" "$LOGS/h2-T1.jsonl" gB Skill 'implement' 1 'starting /sc:implement' lax
  blocked_part "B commit blocked twice (LL-COMMIT)" "$LOGS/h2-T1.jsonl" gB Bash 'commit --allow-empty -m ob-442' 2 'creating a commit'
  # a recorded FAIL is a FAIL; only a missing record is pending
  gov_part() {  # gov_part <label> <gov-log id>
    case "$(gov_status "$2")" in
      OK) part "$1" PASS "$(gov_detail "$2")" ;;
      FAIL) part "$1" FAIL "$(gov_detail "$2")" ;;
      *) part "$1" pending "gov-log has no record $2" ;;
    esac
  }
  gov_part "B bare approved does not unlock (.ok file)" b-approved-no-unlock
  gov_part "B typed /sc:implement unlocks (.ok file)" b-implement-ok
  gov_part "C /sc:implement unlocks (.ok file)" c-implement-ok
  blocked_part "C commit blocked (LL-COMMIT)" "$LOGS/h2-T2.jsonl" gC Bash 'commit --allow-empty -m ob-442' 1 'creating a commit'
  blocked_part "D commit blocked (LL-COMMIT)" "$LOGS/h2-T3.jsonl" gD Bash 'commit --allow-empty -m ob-442' 1 'creating a commit'
  blocked_part "E protected push refused (LL-PROTECTED)" "$LOGS/h2-T4.jsonl" gE Bash 'git push origin master' 1 'a push to master or main'
  blocked_part "E merge refused (LL-MERGE)" "$LOGS/h2-T4.jsonl" gE Bash 'git merge ob-442-no-such-ref' 1 'a merge'
  # counts from F5 to F8 on session E (recorded, not judged)
  if [ -s "$LOGS/h2-T4.jsonl" ]; then
    c=$(run_text "$(filter_text 5)" "$LOGS/h2-T4" | wc -l | tr -d ' ')
    e=$(command timeout "$T" bash -c "L=$LOGS/h2-T4; $(filter_text 8)" 2>/dev/null | wc -l | tr -d ' ')
    part "E counts recorded" PASS "git/gh commands tried: $c; am-only blocked first attempts (F8): $e; transcript Blocked: counts (LL-PUSH-FORM, LL-GH-WRITE, LL-UNKNOWN) and LL-TEXT notes are in the Evidence output"
  else part "E counts recorded" pending "log file missing: $LOGS/h2-T4.jsonl"; fi
  if [ -n "$(reading_of retry-f7-f8)" ]; then part "F7 and F8 retry judgement" PASS "$(reading_of retry-f7-f8)"; else part "F7 and F8 retry judgement" pending "needs reading: record it with evidence.sh --reading retry-f7-f8 <text> <screen file>"; fi
  if [ -n "$(reading_of ac7)" ]; then part "one block message as seen in the tab (AC-7)" PASS "$(reading_of ac7)"; TAB="$TAB reading ac7: $(reading_of ac7) (screen $(reading_screen ac7))"; else part "one block message as seen in the tab (AC-7)" pending "needs reading: record it with evidence.sh --reading ac7 <text> <screen file>"; fi
}
item_ctx() {
  local f t miss="" n s2 a b
  SESSION="A, B"; LOGREF="$LOGS/tree-*.txt, $LOGS/h1.env.jsonl, $GOVLOG"
  CMD=$(section_block '^#### OB-CTX part 1' '^Evidence:')
  OUT=$(run_text "$CMD"; printf '# session B step 4 records\n'; grep -E ' b-(id-|ctx-|jobs|session-ids)' "$GOVLOG" 2>/dev/null | grep -v '^BEGIN' | cut -c1-200 | redact)
  for t in bg-bash monitor pre-push subagent setsid nohup human gov-bg gov-det gov-clear; do [ -s "$LOGS/tree-$t.txt" ] || miss="$miss $t"; done
  if [ -n "$miss" ]; then part "process trees recorded" pending "tree files missing:$miss"; else part "process trees recorded" PASS "tree files for all cases"; fi
  n=$(command timeout "$T" jq -r 'select(.hook_event_name=="SessionStart") | .session_id' "$LOGS/h1.jsonl" 2>/dev/null | wc -l | tr -d ' ')
  if [ "${n:-0}" -ge 4 ]; then part "session id events (start, resume, /clear, fork)" PASS "$n SessionStart lines in h1.jsonl"; else part "session id events (start, resume, /clear, fork)" pending "${n:-0} SessionStart lines, 4 expected"; fi
  a=$(gov_detail b-id-242); b=$(gov_detail b-id-241-after-clear)
  case "$(gov_status b-id-242)$(gov_status b-id-241-after-clear)" in
    OKOK) a=${a#*out=}; b=${b#*out=}
      if [ "$a" = "$b" ]; then part "sleep 241 and sleep 242 told apart" FAIL "identify prints the same for both (cannot be told apart: this stops deployment): $a"
      else part "sleep 241 and sleep 242 told apart" PASS "242: $a | 241: $b"; fi ;;
    *) part "sleep 241 and sleep 242 told apart" pending "no identify output for both processes (gov-log b-id-242 and b-id-241-after-clear)" ;;
  esac
  case "$(gov_status b-id-243)" in OK) part "detached sleep 243 recorded" PASS "$(gov_detail b-id-243)" ;; *) part "detached sleep 243 recorded" pending "no identify output for sleep 243" ;; esac
  case "$(gov_status b-ctx-released)" in OK) part "released case (ordinary, reason released)" PASS "$(gov_detail b-ctx-released)" ;; FAIL) part "released case (ordinary, reason released)" FAIL "$(gov_detail b-ctx-released)" ;; *) part "released case (ordinary, reason released)" pending "no record" ;; esac
}

# --- block output -----------------------------------------------------------------------------
emit_block() {  # emit_block <name>: reads NAME-less globals set by the item function
  PARTS=""; ANYFAIL=0; ANYPEND=0; CMD=""; OUT=""; SESSION=""; LOGREF=""; TAB=""; RES=pending
  "item_$2"; finish
  printf '\n## %s\n\n' "$1"
  printf -- '- Replaces test: `test_pending_live_observation[%s]` in tests/hooks/test_launch_level_observations.py\n' "$1"
  printf -- '- Session: %s\n- Result: %s\n' "${SESSION:-?}" "$RES"
  printf -- '- Evidence command:\n\n```bash\n%s\n```\n\n- Evidence output:\n\n```text\n%s\n```\n\n' "$CMD" "$OUT"
  printf -- '- Log file and line: %s\n' "${LOGREF:-none}"
  printf -- '- What you saw in the tab (for block messages): %s\n' "${TAB:-none recorded}"
  printf -- '- Rule parts:%s\n' "$PARTS"
  if [ "$RES" = pending ]; then printf -- '- If pending: %s\n' "$(printf '%s' "$PARTS" | grep -E ': pending \(' | sed -E 's/^  - //' | tr '\n' ';')"; else printf -- '- If pending: not pending\n'; fi
  if [ "$RES" = FAIL ]; then printf -- '- If FAIL: %s\n' "$(printf '%s' "$PARTS" | grep -E ': FAIL \(' | sed -E 's/^  - //' | tr '\n' ';')"; else printf -- '- If FAIL: not a FAIL\n'; fi
}
names=("OB-H1 item 1:1" "OB-H1 item 2:2" "OB-H1 item 3:3" "OB-H1 item 4:4" "OB-H1 item 5:5" "OB-H1 item 6:6" "OB-H1 item 7:7" "OB-H1 item 8:8" "OB-H1 item 9:9" "OB-H2:h2" "OB-H3:h3" "OB-CTX:ctx")

header() {
  local pre=$OB/preconditions.txt
  pf() { awk -v id="== $1" '$0 == id { getline; print; exit }' "$pre" 2>/dev/null; }
  [ -n "$(state_get RUN_DATE 2>/dev/null)" ] || state_set RUN_DATE "$(date -u +%FT%TZ)"
  printf '# Issue 442 live observation results\n\n'
  printf -- '- Person: %s\n- Date (UTC): %s\n' "${OB_PERSON:-${USER:-unknown}}" "$(state_get RUN_DATE)"
  printf -- '- `claude --version`: %s\n- `orca --version`: %s\n- `git --version`: %s\n' "$(pf P1a)" "$(pf P1b)" "$(pf P1c)"
  printf -- '- `sha256sum ~/.claude/settings.json ~/.claude/hooks/launch-level-guard.sh`: %s\n' "$(command timeout "$T" sha256sum "$HOME/.claude/settings.json" "$HOME/.claude/hooks/launch-level-guard.sh" 2>&1 | awk '{print $1}' | tr '\n' ' ')"
  printf -- '- Disposable issues T1-T4 (numbers): %s %s %s %s\n' "$(state_get T1 2>/dev/null)" "$(state_get T2 2>/dev/null)" "$(state_get T3 2>/dev/null)" "$(state_get T4 2>/dev/null)"
  printf -- '- Disposable pull request URL: %s\n' "$(state_get PR_URL 2>/dev/null || echo none)"
  printf -- '- Baseline files: %s, %s\n' "$OB_BASE_SESSIONS" "$OB_BASE_PENDING"
}

if [ "$sel" != all ]; then
  for e in "${names[@]}"; do
    [ "${e#*:}" = "$sel" ] || [ "${e%%:*}" = "OB-H1 item $sel" ] && { emit_block "${e%%:*}" "${e#*:}"; } | redact
  done
  exit 0
fi

TMP=$(mktemp "$RESULTS.XXXXXX")
{ header
  body=$(for e in "${names[@]}"; do emit_block "${e%%:*}" "${e#*:}"; done)
  for k in OB-H2 OB-H3 OB-CTX; do
    printf '%s\n' "$body" | awk -v h="## $k" '$0 == h { on = 1; next } on && /^## / { exit } on && /^- Result: FAIL$/ { f = 1 } END { exit !f }' \
      && printf '\n**FAIL in %s: no governed claim on a real issue (runbook section 3). Report it instead.**\n' "$k"
  done
  printf '%s\n' "$body"
} | redact > "$TMP" && mv "$TMP" "$RESULTS"
printf 'RESULTS %s blocks=%s\n' "$RESULTS" "$(grep -c '^## ' "$RESULTS")"

# --- copy logs, screens and state after the secret scan -----------------------------------------
hits=$(find "$LOGS" "$OB_SCREENS" "$OB_STATE" -type f 2>/dev/null | sort | while read -r f; do
  neutral < "$f" | grep -nIE "$SECRET_RE" | cut -d: -f1 | sed "s|^|$f:|"
done)
if [ -n "$hits" ]; then
  printf 'SECRET_SCAN_STOP the copy to ob-logs was not made; matches (file:line):\n%s\n' "$hits"
  exit 3
fi
dest=$PKG_ART/ob-logs
mkdir -p "$dest"
cp -r -- "$LOGS" "$dest/" && cp -r -- "$OB_SCREENS" "$dest/" && cp -- "$OB_STATE" "$dest/state.env"
# the files the results cite by path (gov-log, preconditions, baselines) go with the copy, when they exist and pass the same scan
for f in "$GOVLOG" "$OB/preconditions.txt" "$OB_BASE_SESSIONS" "$OB_BASE_PENDING"; do
  [ -f "$f" ] || continue
  if neutral < "$f" | grep -qIE "$SECRET_RE"; then printf 'SECRET_SCAN_SKIP %s not copied\n' "$f"; else cp -- "$f" "$dest/"; fi
done
printf 'COPIED %s\n' "$dest"
