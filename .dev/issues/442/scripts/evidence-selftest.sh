#!/usr/bin/env bash
# evidence-selftest.sh — Task 7 cases, run by selftest.sh.
# Synthetic logs are built from tests/hooks/fixtures/launch_level/ob_h1/*.json with a
# temp OB and a temp HOME; nothing touches /tmp/ob or the real ~/.claude.
set -u -o pipefail
umask 077

here=$(cd -- "$(dirname -- "$0")" && pwd)
RB=$(cd -- "$here/.." && pwd)/observation-runbook.md
FX=$(cd -- "$here/../../../.." && pwd)/tests/hooks/fixtures/launch_level/ob_h1
failures=0
ck() { if [ "$2" = "$3" ]; then printf 'OK %s\n' "$1"; else printf 'FAIL %s got=<%s> want=<%s>\n' "$1" "$2" "$3"; failures=$((failures+1)); fi; }
has() { case "$2" in *"$3"*) ck "$1" ok ok ;; *) ck "$1" "missing <$3>" ok ;; esac; }
hasnt() { case "$2" in *"$3"*) ck "$1" "found <$3>" absent ;; *) ck "$1" ok ok ;; esac; }

T=$(mktemp -d /tmp/ob-evid.XXXXXXXX)
trap 'rm -rf "$T"' EXIT
fx() { jq -c "$2" "$FX/$1"; }       # fx <fixture> <jq edit>

mkenv() {  # mkenv <tag>: fresh OB, HOME, results path; sets S, H, O
  S=$T/$1; H=$S/home; O=$S/ob
  rm -rf "$S"; mkdir -p "$O/logs" "$O/screens" "$H/.claude/hooks" "$S/art"
  : > "$O/state.env"; : > "$O/gov-log.txt"
  printf '{"hooks":{"PreToolUse":[{"matcher":"^(Bash|Skill|Agent|Task|Edit|Write|Monitor|SendMessage)$","hooks":[{"type":"command","command":"/x/launch-level-guard.sh"}]}]}}\n' > "$H/.claude/settings.json"
  printf 'guard\n' > "$H/.claude/hooks/launch-level-guard.sh"
  printf '== P1a\n2.0.0 (Claude Code)\nrc=0\n== P1b\norca 1.0\nrc=0\n== P1c\ngit version 2.47.3\nrc=0\n' > "$O/preconditions.txt"
  printf 'T1=421\nT2=422\nT3=423\nT4=424\n' >> "$O/state.env"
}
ev() {  # ev <args...>: run evidence.sh in the temp env; sets OUT and RC
  OUT=$(env OB="$O" HOME="$H" OB_RESULTS="$S/results.md" PKG_ART="$S/art" OB_TIMEOUT_S=20 timeout 120 bash "$here/evidence.sh" "$@" 2>&1); RC=$?
}
res() { awk -v h="## $1" '$0 == h { on = 1; next } on && /^## / { exit } on && /^- Result:/ { sub(/^- Result: /, ""); print; exit }' "$S/results.md"; }
part_of() { awk -v h="## $1" '$0 == h { on = 1; next } on && /^## / { exit } on' "$S/results.md" | grep -F "$2" | head -1; }

# a good session A log: item 1 to 9 and OB-CTX part 1 evidence from the fixtures
good_h1() {
  { printf '{"hook_event_name":"SessionStart","session_id":"parent-session-0001","source":"startup"}\n'
    printf '{"hook_event_name":"UserPromptSubmit","session_id":"parent-session-0001","prompt":"/hooks"}\n'
    fx item1-subagent-ids.json '.tool_input.command="echo ob-item1-sub"'
    fx item1-subagent-ids.json '.tool_input.command="echo ob-item1-nested" | .agent_id="subagent-0002"'
    fx item3-agent-isolation.json '.tool_input.isolation="worktree"'
    fx item4-typed-implement-prompt.json '.'
    fx item2-skill-keys.json '.'
    fx item2-skill-keys.json '.tool_input={"skill":"sc:implement-protocol","args":"ob-item2"}'
    for n in p04-item5a p05-item5b p06-item5c; do   # each probe: its prompt, a Stop, the notice prompt, a Stop
      jq -nc --rawfile p "$here/prompts/$n.txt" '{hook_event_name:"UserPromptSubmit",session_id:"parent-session-0001",prompt:$p}'
      printf '{"hook_event_name":"Stop","session_id":"parent-session-0001"}\n'
      printf '{"hook_event_name":"UserPromptSubmit","session_id":"parent-session-0001","prompt":"<task-notification>%s done</task-notification>"}\n' "$n"
      printf '{"hook_event_name":"Stop","session_id":"parent-session-0001"}\n'
    done
    printf '{"hook_event_name":"UserPromptSubmit","session_id":"parent-session-0001","prompt":"<task-notification>done</task-notification>"}\n'
    fx item9-tool-names.json '.'
    fx item9-tool-names.json '.tool_name="Write"'
    for n in Bash Agent Monitor SendMessage TaskCreate; do fx item9-tool-names.json ".tool_name=\"$n\""; done
    printf '%s\n' '{"hook_event_name":"PreToolUse","session_id":"parent-session-0001","tool_name":"Bash","tool_input":{"command":"timeout 60 claude \"reply with the single word ob-item8\" < /dev/null"}}'
    printf '%s\n' '{"hook_event_name":"PostToolUse","session_id":"parent-session-0001","tool_name":"Bash","tool_input":{"command":"timeout 60 claude \"reply with the single word ob-item8\" < /dev/null"},"tool_response":"exit 124"}'
    printf '{"hook_event_name":"UserPromptSubmit","session_id":"parent-session-0001","prompt":"hello [sc-launch:v1:0123456789abcdef0123456789abcdef]"}\n'
    for s in resume clear resume; do printf '{"hook_event_name":"SessionStart","session_id":"s-%s","source":"%s"}\n' "$s" "$s"; done
  } > "$O/logs/h1.jsonl"
  { printf '{"hook_event_name":"PreToolUse","session_id":"parent-session-0001","tool_name":"SendMessage","tool_input":{"to":"x"}}\n'
    fx item7-sendmessage-mcp.json '.tool_name="mcp__codegraph__codegraph_status"'
  } > "$O/logs/h1m.jsonl"
}

# --- 1. structure: 12 blocks, pending without logs -----------------------------------------
mkenv none
ev all
ck all-rc "$RC" 0
ck blocks-count "$(grep -c '^## ' "$S/results.md")" 12
ck pending-count "$(grep -c '^- Result: pending$' "$S/results.md")" 12
has header-claude "$(cat "$S/results.md")" '`claude --version`: 2.0.0 (Claude Code)'
has header-issues "$(cat "$S/results.md")" 'T1-T4 (numbers): 421 422 423 424'
has block-name "$(cat "$S/results.md")" '## OB-H1 item 9'
has block-test "$(cat "$S/results.md")" '`test_pending_live_observation[OB-CTX]`'

# --- 2. classification of good evidence: items 1 to 9 PASS ---------------------------------
mkenv good; good_h1
ev all
for i in 1 2 3 4 5 6 7 8 9; do ck "item$i-pass" "$(res "OB-H1 item $i")" PASS; done
has item2-keys "$(cat "$S/results.md")" '"keys"'
ck h2-pending-without-logs "$(res OB-H2)" pending

# --- 3. classification of bad evidence ----------------------------------------------------------
mkenv bad5; good_h1
printf '{"hook_event_name":"UserPromptSubmit","session_id":"parent-session-0001","prompt":"  Approved!"}\n' >> "$O/logs/h1.jsonl"
ev all; ck item5-bare-approved-fail "$(res 'OB-H1 item 5')" FAIL
has item5-fail-reason "$(part_of 'OB-H1 item 5' 'bare Approved')" 'FAIL'
mkenv noprobes; good_h1
jq -c 'select((.prompt // "") | test("sleep [23]; echo approved|general-purpose subagent") | not)' "$O/logs/h1.jsonl" > "$O/logs/h1.new" && mv "$O/logs/h1.new" "$O/logs/h1.jsonl"
ev all; ck item5-missing-probes-pending "$(res 'OB-H1 item 5')" pending
mkenv nonotice; good_h1
jq -c 'select((.prompt // "") | test("^<task-notification>p0") | not)' "$O/logs/h1.jsonl" > "$O/logs/h1.new" && mv "$O/logs/h1.new" "$O/logs/h1.jsonl"
ev all; ck item5-probe-without-notice-pending "$(res 'OB-H1 item 5')" pending
mkenv nodown4; good_h1
jq -c 'select(.tool_name != "Skill" and .hook_event_name != "UserPromptExpansion")' "$O/logs/h1.jsonl" > "$O/logs/h1.new" && mv "$O/logs/h1.new" "$O/logs/h1.jsonl"
ev all; ck item4-no-downstream-pending "$(res 'OB-H1 item 4')" pending
mkenv bad1; good_h1
jq -c 'if .tool_input.command? == "echo ob-item1-nested" then .session_id="someone-else" else . end' "$O/logs/h1.jsonl" > "$O/logs/h1.new" && mv "$O/logs/h1.new" "$O/logs/h1.jsonl"
ev all; ck item1-wrong-parent-fail "$(res 'OB-H1 item 1')" FAIL
mkenv miss1; good_h1
jq -c 'if .tool_input.command? == "echo ob-item1-nested" then del(.session_id) else . end' "$O/logs/h1.jsonl" > "$O/logs/h1.new" && mv "$O/logs/h1.new" "$O/logs/h1.jsonl"
ev all; ck item1-missing-parent-fail "$(res 'OB-H1 item 1')" FAIL
mkenv taskcreate; good_h1
sed -i 's/\^(Bash|/^(TaskCreate|Bash|/' "$H/.claude/settings.json"
ev all; ck item6-taskcreate-match-fail "$(res 'OB-H1 item 6')" FAIL
mkenv skillkey; good_h1
fx item2-skill-keys.json '.tool_input={"other":"sc:implement"}' >> "$O/logs/h1.jsonl"
ev all; ck item2-wrong-key-fail "$(res 'OB-H1 item 2')" FAIL
mkenv wrap9; good_h1
fx item9-tool-names.json '.tool_name="mcp__x__run_Bash"' >> "$O/logs/h1.jsonl"
ev all; ck item9-wrapped-fail "$(res 'OB-H1 item 9')" FAIL

# --- 4. each filter F1 to F8 equals the runbook text (diff against the extracted block) -------------
mkenv f
ev --print-filters
sed -n '505,520p' "$RB" > "$S/want-filters.txt"
printf '%s\n' "$OUT" > "$S/got-filters.txt"
ck filters-equal "$(cmp -s "$S/want-filters.txt" "$S/got-filters.txt" && echo equal)" equal
ck filters-count "$(grep -c '^# F[1-8]:' "$S/got-filters.txt")" 8

# --- 5. OB-H2, OB-H3 and OB-CTX from synthetic evidence ----------------------------------------------
full_gov() {  # session B to E records, logs, screens, trees, readings
  local t pre='git -c user.name=ob -c user.email=ob@invalid commit --allow-empty -m ob-442'
  {
    printf '{"hook_event_name":"UserPromptSubmit","session_id":"gsid-b-1","prompt":"[sc-launch:v1:abc] launch"}\n'
    printf '{"hook_event_name":"PreToolUse","session_id":"gsid-b-1","tool_name":"Skill","tool_input":{"skill":"sc:implement"}}\n'
    printf '{"hook_event_name":"PreToolUse","session_id":"gsid-b-1","tool_name":"Bash","tool_input":{"command":"%s"}}\n' "$pre"
    printf '{"hook_event_name":"PreToolUse","session_id":"gsid-b-1","tool_name":"Bash","tool_input":{"command":"%s"}}\n' "$pre"
  } > "$O/logs/h2-T1.jsonl"
  for l in 1 2 3 4; do printf '{"probe_env":{"HOME":"%s","CLAUDE_CONFIG_DIR":"<unset>","session_file":"worktree","at":"t"}}\n' "$H"; done > "$O/logs/h2-T1.env.jsonl"
  for t in T2 T3; do printf '{"hook_event_name":"PreToolUse","session_id":"g","tool_name":"Bash","tool_input":{"command":"%s"}}\n' "$pre" > "$O/logs/h2-$t.jsonl"; done
  { printf '{"hook_event_name":"PreToolUse","session_id":"g","tool_name":"Bash","tool_input":{"command":"git push origin master"}}\n'
    printf '{"hook_event_name":"PreToolUse","session_id":"g","tool_name":"Bash","tool_input":{"command":"git merge ob-442-no-such-ref"}}\n'; } > "$O/logs/h2-T4.jsonl"
  blk() { jq -nc --arg t "$2" '{result:{terminal:{tail:[$t]}}}' > "$O/screens/$1-1.json"; }
  blk gB 'Blocked: starting /sc:implement, /task, /sc:improve (or their skills).
Blocked: creating a commit (git commit, cherry-pick).'
  blk gC 'Blocked: creating a commit (git commit, cherry-pick).'
  blk gD 'Blocked: creating a commit (git commit, cherry-pick).'
  blk gE 'Blocked: a push to master or main.
Blocked: a merge (git merge, git pull).'
  blk sA 'Blocked: this launch prompt.'
  for t in bg-bash monitor pre-push subagent setsid nohup human gov-bg gov-det gov-clear; do printf 'tree\n' > "$O/logs/tree-$t.txt"; done
  { for id in badjson nohooks; do for k in claim pending no-mirror no-record; do printf 'BEGIN b-%s-%s\nOK b-%s-%s fine\n' "$id" "$k" "$id" "$k"; done; done
    printf 'BEGIN b-inode\nOK b-inode session file gsid-b-1 holds inode 5, equal to the claim 5\n'
    printf 'BEGIN b-approved-no-unlock\nOK b-approved-no-unlock x\nBEGIN b-implement-ok\nOK b-implement-ok x\nBEGIN c-implement-ok\nOK c-implement-ok x\n'
    printf 'BEGIN b-id-242\nOK b-id-242 pid=2 out={"status":"governed","session_id":"gsid-b-2"}\n'
    printf 'BEGIN b-id-241-after-clear\nOK b-id-241-after-clear pid=1 out={"status":"governed","session_id":"gsid-b-1"}\n'
    printf 'BEGIN b-id-243\nOK b-id-243 pid=3 out={"status":"ordinary"}\n'
    printf 'BEGIN b-ctx-released\nOK b-ctx-released ordinary, reason released\n'; } > "$O/gov-log.txt"
}
mkenv gov; good_h1; full_gov
ev all
ck h2-pending-until-reading "$(res OB-H2)" pending
has h2-needs-reading "$(part_of OB-H2 'U20')" 'needs reading'
ck h3-pending-until-readings "$(res OB-H3)" pending
ck ctx-pass "$(res OB-CTX)" PASS
ev --reading u20 'the Blocked: this launch prompt line was visible in the tab' "$O/screens/sA-1.json"
ev --reading retry-f7-f8 'no retried blocked commands' "$O/screens/gE-1.json"
ev --reading ac7 'Blocked: a push to master or main. as shown' "$O/screens/gE-1.json"
ev all
ck h2-pass "$(res OB-H2)" PASS
ck h3-pass "$(res OB-H3)" PASS
has h3-reading-shown "$(cat "$S/results.md")" 'reading ac7'
# a blocked-looking call that actually ran is a FAIL
printf '{"hook_event_name":"PostToolUse","session_id":"g","tool_name":"Bash","tool_input":{"command":"git push origin master"},"tool_response":"ok"}\n' >> "$O/logs/h2-T4.jsonl"
ev all; ck h3-push-ran-fail "$(res OB-H3)" FAIL
has fail-banner "$(cat "$S/results.md")" 'FAIL in OB-H3: no governed claim on a real issue'
# sleep 241 and sleep 242 that print the same cannot be told apart
sed -i 's/gsid-b-2/gsid-b-1/' "$O/gov-log.txt"
ev all; ck ctx-same-fail "$(res OB-CTX)" FAIL
# a missing inode record keeps OB-H2 pending; a FAIL inode record fails it
sed -i 's/^OK b-inode /FAIL b-inode /' "$O/gov-log.txt"
ev all; ck h2-inode-fail "$(res OB-H2)" FAIL
# a bare `approved` that unlocked, or a typed /sc:implement that did not, is a FAIL (never pending)
mkenv gov2; good_h1; full_gov
sed -i 's/^OK b-approved-no-unlock /FAIL b-approved-no-unlock /' "$O/gov-log.txt"
ev all; ck h3-approved-unlock-fail "$(res OB-H3)" FAIL
mkenv gov3; good_h1; full_gov
sed -i 's/^OK b-implement-ok /FAIL b-implement-ok /' "$O/gov-log.txt"
ev all; ck h3-implement-nounlock-fail "$(res OB-H3)" FAIL

# --- 6. a rerun gives the same file --------------------------------------------------------------------
mkenv rerun; good_h1; full_gov
ev all; cp "$S/results.md" "$S/first.md"
ev all
ck rerun-same "$(cmp -s "$S/first.md" "$S/results.md" && echo equal)" equal
ck rerun-blocks "$(grep -c '^## ' "$S/results.md")" 12
ck copy-made "$([ -d "$S/art/ob-logs/logs" ] && [ -f "$S/art/ob-logs/state.env" ] && echo yes)" yes
# the files the results cite by path travel with the copy
ck copy-gov-log "$([ -f "$S/art/ob-logs/gov-log.txt" ] && echo yes)" yes
# item 1 cites the evidence rows (a PreToolUse line naming ob-item1-sub or -nested), not the prompt line
ck item1-log-lines-are-rows "$(grep -F 'Log file and line' "$S/results.md" | head -1 | grep -c 'lines [0-9]')" 1

# --- 7. the secret scan stops the copy and the report never carries the value ------------------------------
mkenv sec1; good_h1; full_gov
printf '{"hook_event_name":"UserPromptSubmit","session_id":"x","prompt":"token ghp_abcdefghijklmnopqrstuvwxyz0123"}\n' >> "$O/logs/h1.jsonl"
ev all
ck secret-ghp-rc "$RC" 3
has secret-ghp-stop "$OUT" 'SECRET_SCAN_STOP'
has secret-ghp-where "$OUT" "$O/logs/h1.jsonl:"
hasnt secret-ghp-not-printed "$OUT" 'abcdefghijklmnopqrstuvwxyz0123'
ck secret-ghp-no-copy "$([ -e "$S/art/ob-logs" ] && echo copied || echo none)" none
hasnt secret-ghp-not-in-report "$(cat "$S/results.md")" 'abcdefghijklmnopqrstuvwxyz0123'
mkenv sec2; good_h1; full_gov
printf '{"hook_event_name":"UserPromptSubmit","session_id":"x","prompt":"Authorization: Bearer zzTopSecretValue99"}\n' >> "$O/logs/h1.jsonl"
ev all
ck secret-bearer-rc "$RC" 3
ck secret-bearer-no-copy "$([ -e "$S/art/ob-logs" ] && echo copied || echo none)" none
hasnt secret-bearer-not-in-report "$(cat "$S/results.md")" 'zzTopSecretValue99'
hasnt secret-bearer-not-printed "$OUT" 'zzTopSecretValue99'
# the quoted sk- pattern still matches inside another word, so a planted xsk- value stops the copy
mkenv sec4; good_h1; full_gov
printf '{"hook_event_name":"UserPromptSubmit","session_id":"x","prompt":"xsk-abcdefghij"}\n' >> "$O/logs/h1.jsonl"
ev all; ck secret-sk-rc "$RC" 3
hasnt secret-sk-not-in-report "$(cat "$S/results.md")" 'xsk-abcdefghij'
# an MCP tool named like send_message is an MCP name, not a SendMessage failure
mkenv mcpsend; good_h1
printf '{"hook_event_name":"PreToolUse","session_id":"parent-session-0001","tool_name":"mcp__slack__send_message","tool_input":{}}\n' >> "$O/logs/h1m.jsonl"
ev all; ck item7-mcp-send-message-pass "$(res 'OB-H1 item 7')" PASS
# the word task-notification is not a secret
mkenv sec3; good_h1; full_gov
printf '{"hook_event_name":"UserPromptSubmit","session_id":"x","prompt":"<task-id>aaea84</task-id><task-type>local_agent</task-type>"}\n' >> "$O/logs/h1.jsonl"
ev all; ck notice-word-not-secret "$RC" 0

exit $failures
