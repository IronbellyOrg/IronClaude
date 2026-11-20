# Issue 442 live observation results

- Person: coder
- Date (UTC): 2026-11-19T19:59:51Z
- `claude --version`: 2.1.328 (Claude Code)
- `orca --version`: 1.4.245-aidev02.9cfecdd30b2a
- `git --version`: git version 2.47.3
- `sha256sum ~/.claude/settings.json ~/.claude/hooks/launch-level-guard.sh`: 8c27418cccaced06eee321299b65d39677d3ace94f6ee90ad54afda7932aa059 3f1c5da85c1b3b78680bff1dea2fa9dd5cef3571d89f5f6847667fda27988b8d 
- Disposable issues T1-T4 (numbers):    679
- Disposable pull request URL: https://github.com/IronbellyOrg/IronClaude/pull/680
- Baseline files: /tmp/ob/baseline-sessions.txt, /tmp/ob/baseline-pending.txt

## OB-H1 item 1

- Replaces test: `test_pending_live_observation[OB-H1 item 1]` in tests/hooks/test_launch_level_observations.py
- Session: A
- Result: pending
- Evidence command:

```bash
jq -c 'select(.hook_event_name=="PreToolUse" and .tool_name=="Bash" and (.tool_input.command|test("ob-item1"))) | {session_id, agent_id, agent_type, cmd: .tool_input.command}' /tmp/ob/logs/h1.jsonl
```

- Evidence output:

```text

```

- Log file and line: /tmp/ob/logs/h1.jsonl: lines 
- What you saw in the tab (for block messages): none recorded
- Rule parts:
  - parent session_id in subagent payloads: pending (no ob-item1 line in the log)
- If pending: parent session_id in subagent payloads: pending (no ob-item1 line in the log);
- If FAIL: not a FAIL

## OB-H1 item 2

- Replaces test: `test_pending_live_observation[OB-H1 item 2]` in tests/hooks/test_launch_level_observations.py
- Session: A
- Result: pending
- Evidence command:

```bash
jq -c 'select(.hook_event_name=="PreToolUse" and .tool_name=="Skill") | {keys: (.tool_input|keys), raw: (.tool_input.skill // .tool_input.name), norm: ((.tool_input.skill // .tool_input.name // "") | (capture("^\\s*(?<w>\\S*)").w // "") | ascii_downcase | sub("^/";"") | split(":")[-1] | sub("^sc-";"") | sub("-protocol$";""))}' /tmp/ob/logs/h1.jsonl
```

- Evidence output:

```text

```

- Log file and line: /tmp/ob/logs/h1.jsonl: lines 
- What you saw in the tab (for block messages): none recorded
- Rule parts:
  - Skill call keys and name form: pending (fewer than two Skill calls (0))
- If pending: Skill call keys and name form: pending (fewer than two Skill calls (0));
- If FAIL: not a FAIL

## OB-H1 item 3

- Replaces test: `test_pending_live_observation[OB-H1 item 3]` in tests/hooks/test_launch_level_observations.py
- Session: A
- Result: pending
- Evidence command:

```bash
jq -c 'select(.hook_event_name=="PreToolUse" and (.tool_name=="Agent" or .tool_name=="Task")) | {tool_name, keys: (.tool_input|keys), isolation: .tool_input.isolation, subagent_type: .tool_input.subagent_type}' /tmp/ob/logs/h1.jsonl
```

- Evidence output:

```text

```

- Log file and line: /tmp/ob/logs/h1.jsonl: lines 
- What you saw in the tab (for block messages): none recorded
- Rule parts:
  - Agent tool name and the isolation key: pending (no Agent or Task call in the log)
- If pending: Agent tool name and the isolation key: pending (no Agent or Task call in the log);
- If FAIL: not a FAIL

## OB-H1 item 4

- Replaces test: `test_pending_live_observation[OB-H1 item 4]` in tests/hooks/test_launch_level_observations.py
- Session: A
- Result: pending
- Evidence command:

```bash
jq -c 'select(.hook_event_name=="UserPromptSubmit" or .hook_event_name=="UserPromptExpansion" or (.hook_event_name=="PreToolUse" and .tool_name=="Skill")) | {n: input_line_number, e: .hook_event_name, first_line: ((.prompt // "") | split("\n")[0] | .[0:80]), command_name, skill: (.tool_input.skill // .tool_input.name)}' /tmp/ob/logs/h1.jsonl
```

- Evidence output:

```text
{"n":2,"e":"UserPromptSubmit","first_line":"Reply with the word ok","command_name":null,"skill":null}
```

- Log file and line: /tmp/ob/logs/h1.jsonl: lines 
- What you saw in the tab (for block messages): none recorded
- Rule parts:
  - typed /sc:implement x, prompt event before expansion: pending (no /sc:implement x prompt line)
- If pending: typed /sc:implement x, prompt event before expansion: pending (no /sc:implement x prompt line);
- If FAIL: not a FAIL

## OB-H1 item 5

- Replaces test: `test_pending_live_observation[OB-H1 item 5]` in tests/hooks/test_launch_level_observations.py
- Session: A
- Result: PASS
- Evidence command:

```bash
jq -c 'select(.hook_event_name=="UserPromptSubmit") | {bare_approved: (.prompt|gsub("^\\s+|\\s+$";"")|ascii_downcase|test("^approved[.!]?$")), implement_first_line: (.prompt|split("\n")[0]|test("^\\s*/(sc:implement|sc:task|task)(\\s|$)")), head: (.prompt|.[0:120])}' /tmp/ob/logs/h1.jsonl
```

- Evidence output:

```text
{"bare_approved":false,"implement_first_line":false,"head":"Reply with the word ok"}
```

- Log file and line: /tmp/ob/logs/h1.jsonl: lines 2
- What you saw in the tab (for block messages): none recorded
- Rule parts:
  - self-started turns carry no bare Approved: PASS (1 prompt line(s) not typed by the run, none a bare Approved or an implement line)
- If pending: not pending
- If FAIL: not a FAIL

## OB-H1 item 6

- Replaces test: `test_pending_live_observation[OB-H1 item 6]` in tests/hooks/test_launch_level_observations.py
- Session: A
- Result: pending
- Evidence command:

```bash
M=$(jq -r '.hooks.PreToolUse[]|select(any(.hooks[];.command|test("launch-level-guard")))|.matcher' ~/.claude/settings.json)
jq -r 'select(.hook_event_name=="PreToolUse") | .tool_name' /tmp/ob/logs/h1.jsonl | sort -u | while read -r n; do printf '%s %s\n' "$n" "$(printf '%s' "$n" | grep -qE "$M" && echo match || echo no-match)"; done
```

- Evidence output:

```text

```

- Log file and line: /tmp/ob/logs/h1.jsonl: PreToolUse tool names
- What you saw in the tab (for block messages): none recorded
- Rule parts:
  - TaskCreate: pending (TaskCreate not seen in the log (the model may not offer it in this version))
  - matcher rows: pending (not seen in the log: Bash Skill Edit Write Monitor SendMessage Agent-or-Task)
- If pending: TaskCreate: pending (TaskCreate not seen in the log (the model may not offer it in this version));matcher rows: pending (not seen in the log: Bash Skill Edit Write Monitor SendMessage Agent-or-Task);
- If FAIL: not a FAIL

## OB-H1 item 7

- Replaces test: `test_pending_live_observation[OB-H1 item 7]` in tests/hooks/test_launch_level_observations.py
- Session: A, A2
- Result: pending
- Evidence command:

```bash
jq -c 'select(.hook_event_name=="PreToolUse" and (.tool_name=="SendMessage" or (.tool_name|startswith("mcp__")))) | {tool_name, keys: (.tool_input|keys)}' /tmp/ob/logs/h1.jsonl /tmp/ob/logs/h1m.jsonl
```

- Evidence output:

```text
jq: error: Could not open file /tmp/ob/logs/h1m.jsonl: No such file or directory
```

- Log file and line: /tmp/ob/logs/h1.jsonl, /tmp/ob/logs/h1m.jsonl: SendMessage and mcp__ tool names
- What you saw in the tab (for block messages): none recorded
- Rule parts:
  - SendMessage and MCP tool names: pending (no SendMessage call (record that the model has no SendMessage tool))
- If pending: SendMessage and MCP tool names: pending (no SendMessage call (record that the model has no SendMessage tool));
- If FAIL: not a FAIL

## OB-H1 item 8

- Replaces test: `test_pending_live_observation[OB-H1 item 8]` in tests/hooks/test_launch_level_observations.py
- Session: A
- Result: pending
- Evidence command:

```bash
jq -c 'select(.hook_event_name=="PreToolUse" and .tool_name=="Bash" and (.tool_input.command|test("(^|[;&|(\\s])(claude|claude-code)(\\s|$)"))) | .tool_input.command' /tmp/ob/logs/h1.jsonl
jq -r 'select(.hook_event_name=="SessionStart" or .hook_event_name=="Stop") | [.hook_event_name, .session_id] | @tsv' /tmp/ob/logs/h1.jsonl
```

- Evidence output:

```text
SessionStart	afb74195-5268-44bc-867f-7d09d4ca9467
Stop	afb74195-5268-44bc-867f-7d09d4ca9467
```

- Log file and line: /tmp/ob/logs/h1.jsonl: lines 
- What you saw in the tab (for block messages): none recorded
- Rule parts:
  - claude without -p runs no turn: pending (the claude command is not logged)
- If pending: claude without -p runs no turn: pending (the claude command is not logged);
- If FAIL: not a FAIL

## OB-H1 item 9

- Replaces test: `test_pending_live_observation[OB-H1 item 9]` in tests/hooks/test_launch_level_observations.py
- Session: A
- Result: pending
- Evidence command:

```bash
jq -r 'select(.hook_event_name=="PreToolUse") | .tool_name' /tmp/ob/logs/h1.jsonl | sort | uniq -c
```

- Evidence output:

```text

```

- Log file and line: /tmp/ob/logs/h1.jsonl: PreToolUse tool names
- What you saw in the tab (for block messages): none recorded
- Rule parts:
  - tool names of Bash, Edit, Write and Skill: pending (not seen: Bash, Edit, Write, Skill)
- If pending: tool names of Bash, Edit, Write and Skill: pending (not seen: Bash, Edit, Write, Skill);
- If FAIL: not a FAIL

## OB-H2

- Replaces test: `test_pending_live_observation[OB-H2]` in tests/hooks/test_launch_level_observations.py
- Session: A (LL-NOBIND), B
- Result: pending
- Evidence command:

```bash
# F1: first prompt, and where the strict marker sits in it (U7, O-11)
jq -c 'select(.hook_event_name=="UserPromptSubmit") | {marker_at: (.prompt | index("[sc-launch:v1:")), length: (.prompt | length), head: .prompt[0:160]}' "$L.jsonl" | head -1
# F2: the session file as seen at the first tool call (U8)
jq -nc --slurpfile a "$L.jsonl" --slurpfile b "$L.env.jsonl" 'first(range(0; $a|length) | select($a[.].hook_event_name=="PreToolUse")) as $i | {line: ($i+1), tool: $a[$i].tool_name, session_file: $b[$i].probe_env.session_file, at: $b[$i].probe_env.at}'
# F3: the hook's HOME and CLAUDE_CONFIG_DIR
jq -r '[.probe_env.HOME, .probe_env.CLAUDE_CONFIG_DIR] | @tsv' "$L.env.jsonl" | sort | uniq -c
# F4: session-file timeline, one line per run of identical states
jq -nr --slurpfile a "$L.jsonl" --slurpfile b "$L.env.jsonl" 'range(0; $a|length) | "\($a[.].hook_event_name) \($a[.].tool_name // "") \($b[.].probe_env.session_file)"' | uniq -c
jq -c 'select(.hook_event_name=="UserPromptSubmit" and (.prompt|test("sc-launch"))) | .prompt' /tmp/ob/logs/h1.jsonl
```

- Evidence output:

```text
# F1
jq: error: Could not open file /tmp/ob/logs/h2-T1.jsonl: No such file or directory
# F2
jq: Bad JSON in --slurpfile a /tmp/ob/logs/h2-T1.jsonl: Could not open /tmp/ob/logs/h2-T1.jsonl: No such file or directory
# F3
jq: error: Could not open file /tmp/ob/logs/h2-T1.env.jsonl: No such file or directory
# F4
jq: Bad JSON in --slurpfile a /tmp/ob/logs/h2-T1.jsonl: Could not open /tmp/ob/logs/h2-T1.jsonl: No such file or directory
# LL-NOBIND
# launch preflight and inode records
```

- Log file and line: /tmp/ob/logs/h2-T1.jsonl: lines 
- What you saw in the tab (for block messages): none recorded
- Rule parts:
  - log: pending (log file missing: /tmp/ob/logs/h2-T1.jsonl)
- If pending: log: pending (log file missing: /tmp/ob/logs/h2-T1.jsonl);
- If FAIL: not a FAIL

## OB-H3

- Replaces test: `test_pending_live_observation[OB-H3]` in tests/hooks/test_launch_level_observations.py
- Session: B, C, D, E
- Result: pending
- Evidence command:

```bash
# F5: every git and gh command the agent tried (U10)
jq -r 'select(.hook_event_name=="PreToolUse" and .tool_name=="Bash") | .tool_input.command | gsub("\n"; " ") | .[0:160]' "$L.jsonl" | grep -E '(^|[;&|( ])(git|gh) '
# F6: Blocked lines in the session transcript (transcript_path is U27, UNVERIFIED)
TP=$(jq -r 'select(.transcript_path) | .transcript_path' "$L.jsonl" | head -1); grep -o 'Blocked: [^\\"]*' "$TP" | sort | uniq -c
# F7: tool calls with no PostToolUse (blocked, or failed); NO-ID means the payload has no tool_use_id
jq -sr '(map(select(.hook_event_name=="PostToolUse") | .tool_use_id)) as $done | .[] | select(.hook_event_name=="PreToolUse") | select(.tool_use_id == null or (.tool_use_id as $i | $done | index($i) | not)) | "\(if .tool_use_id then "BLOCKED?" else "NO-ID" end) \(.tool_name) \((.tool_input.command // .tool_input.skill // "") | gsub("\n";" ") | .[0:120])"' "$L.jsonl"
# F8: blocked Bash commands whose only commit word is a bare "am" (O-21)
jq -sr '(map(select(.hook_event_name=="PostToolUse") | .tool_use_id)) as $done | .[] | select(.hook_event_name=="PreToolUse" and .tool_name=="Bash" and .tool_use_id != null and (.tool_use_id as $i | $done | index($i) | not)) | .tool_input.command | gsub("\n";" ")' "$L.jsonl" | grep -Ew 'am' | grep -Ev 'git +(commit|cherry-pick|revert|am|update-ref)'
```

- Evidence output:

```text
# F5 T3
jq: error: Could not open file /tmp/ob/logs/h2-T3.jsonl: No such file or directory
# F6 T3
jq: error: Could not open file /tmp/ob/logs/h2-T3.jsonl: No such file or directory
grep: : No such file or directory
# F7 T3
jq: error: Could not open file /tmp/ob/logs/h2-T3.jsonl: No such file or directory
# F8 T3
jq: error: Could not open file /tmp/ob/logs/h2-T3.jsonl: No such file or directory
# F5 T4
git branch --show-current && cat -A ob-442/T4.txt && git status --short && gh pr list --repo IronbellyOrg/IronClaude --head ironbelly/issue-679 --state all
git add ob-442/T4.txt && git commit -q -m "feat(ob-442): add disposable T4 launch-level observation target (#679)  Co-Authored-By: Claude Code <noreply@anthropi
git -C /home/coder/workspaces/worktrees/IronClaude/issue-679 add ob-442/T4.txt && git -C /home/coder/workspaces/worktrees/IronClaude/issue-679 commit -F /tmp/is
git push origin ironbelly/issue-679
REPO="$(git remote get-url origin | sed -E 's#^ssh://[^/]+/##; s#^git@[^:]+:##; s#^https?://[^/]+/##; s#\.git$##')"; echo "REPO=$REPO"; git remote -v; gh pr che
gh pr create --repo IronbellyOrg/IronClaude --base master --head ironbelly/issue-679 --title "feat(ob-442): add disposable T4 launch-level observation target (#
gh pr view 680 --repo IronbellyOrg/IronClaude --json headRefName,headRefOid,isCrossRepository,baseRefName,mergeable,mergeStateStatus,isDraft,state; git branch -
gh pr view 680 --repo IronbellyOrg/IronClaude --json headRefOid,commits -q '.headRefOid, [.commits[].oid]'; git ls-remote origin refs/heads/ironbelly/issue-679;
git fetch origin ironbelly/issue-679 -q && git log --format='%h %an %ae %s' f82d830..FETCH_HEAD && git diff f82d830 FETCH_HEAD && git show FETCH_HEAD:ob-442/T4.
git merge ob-442-no-such-ref
# F6 T4
      2 Blocked: a merge (git merge, git pull, gh pr merge, a call to a GitHub merge URL, or an MCP merge tool).
      2 Blocked: a push that is not one plain git push command, or a command that names git and push together.
# F7 T4
BLOCKED? Bash git add ob-442/T4.txt && git commit -q -m "feat(ob-442): add disposable T4 launch-level observation target (#679)  Co-Au
BLOCKED? Bash for i in 1 2 3 4 5 6 7 8; do sleep 30; out=$(~/.claude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh --pr 
BLOCKED? Bash git merge ob-442-no-such-ref
# F8 T4
```

- Log file and line: /tmp/ob/logs/h2-T1..T4.jsonl
- What you saw in the tab (for block messages):    
- Rule parts:
  - B implement blocked (LL-IMPL): pending (log file missing: /tmp/ob/logs/h2-T1.jsonl)
  - B commit blocked twice (LL-COMMIT): pending (log file missing: /tmp/ob/logs/h2-T1.jsonl)
  - B bare approved does not unlock (.ok file): pending (gov-log has no record b-approved-no-unlock)
  - B typed /sc:implement unlocks (.ok file): pending (gov-log has no record b-implement-ok)
  - C /sc:implement unlocks (.ok file): pending (gov-log has no record c-implement-ok)
  - C commit blocked (LL-COMMIT): pending (log file missing: /tmp/ob/logs/h2-T2.jsonl)
  - D commit blocked (LL-COMMIT): pending (log file missing: /tmp/ob/logs/h2-T3.jsonl)
  - E protected push refused (LL-PROTECTED): pending (0 attempt(s) logged, 1 expected)
  - E merge refused (LL-MERGE): PASS (1 blocked attempt(s) with no PostToolUse; 'Blocked: a merge' seen 1 time(s))
  - E counts recorded: PASS (git/gh commands tried: 10; am-only blocked first attempts (F8): 0; transcript Blocked: counts (LL-PUSH-FORM, LL-GH-WRITE, LL-UNKNOWN) and LL-TEXT notes are in the Evidence output)
  - F7 and F8 retry judgement: pending (needs reading: record it with evidence.sh --reading retry-f7-f8 <text> <screen file>)
  - one block message as seen in the tab (AC-7): pending (needs reading: record it with evidence.sh --reading ac7 <text> <screen file>)
- If pending: B implement blocked (LL-IMPL): pending (log file missing: /tmp/ob/logs/h2-T1.jsonl);B commit blocked twice (LL-COMMIT): pending (log file missing: /tmp/ob/logs/h2-T1.jsonl);B bare approved does not unlock (.ok file): pending (gov-log has no record b-approved-no-unlock);B typed /sc:implement unlocks (.ok file): pending (gov-log has no record b-implement-ok);C /sc:implement unlocks (.ok file): pending (gov-log has no record c-implement-ok);C commit blocked (LL-COMMIT): pending (log file missing: /tmp/ob/logs/h2-T2.jsonl);D commit blocked (LL-COMMIT): pending (log file missing: /tmp/ob/logs/h2-T3.jsonl);E protected push refused (LL-PROTECTED): pending (0 attempt(s) logged, 1 expected);F7 and F8 retry judgement: pending (needs reading: record it with evidence.sh --reading retry-f7-f8 <text> <screen file>);one block message as seen in the tab (AC-7): pending (needs reading: record it with evidence.sh --reading ac7 <text> <screen file>);
- If FAIL: not a FAIL

## OB-CTX

- Replaces test: `test_pending_live_observation[OB-CTX]` in tests/hooks/test_launch_level_observations.py
- Session: A, B
- Result: pending
- Evidence command:

```bash
ls /tmp/ob/logs/tree-*.txt; head -n 40 /tmp/ob/logs/tree-*.txt
jq -r '[.probe_env.at, .probe_env.hook_pid, (.probe_env.ancestors | split("\n") | map(select(length > 0)) | map(split(" ") | map(select(length > 0)) | .[-1]) | join(" < "))] | @tsv' /tmp/ob/logs/h1.env.jsonl | tail -n 20
jq -r 'select(.hook_event_name=="SessionStart") | [.session_id, (.source // "-")] | @tsv' /tmp/ob/logs/h1.jsonl
```

- Evidence output:

```text
ls: cannot access '/tmp/ob/logs/tree-*.txt': No such file or directory
head: cannot open '/tmp/ob/logs/tree-*.txt' for reading: No such file or directory
2026-11-19T19:38:43.573Z	3784568	sh < claude < timeout < bash < timeout < bash < claude < bash < orca-ide < orca-ide < orca-ide
2026-11-19T19:38:43.963Z	3784629	sh < claude < timeout < bash < timeout < bash < claude < bash < orca-ide < orca-ide < orca-ide
2026-11-19T19:38:45.588Z	3784756	sh < claude < timeout < bash < timeout < bash < claude < bash < orca-ide < orca-ide < orca-ide
afb74195-5268-44bc-867f-7d09d4ca9467	startup
# session B step 4 records
```

- Log file and line: /tmp/ob/logs/tree-*.txt, /tmp/ob/logs/h1.env.jsonl, /tmp/ob/gov-log.txt
- What you saw in the tab (for block messages): none recorded
- Rule parts:
  - process trees recorded: pending (tree files missing: bg-bash monitor pre-push subagent setsid nohup human gov-bg gov-det gov-clear)
  - session id events (start, resume, /clear, fork): pending (1 SessionStart lines, 4 expected)
  - sleep 241 and sleep 242 told apart: pending (no identify output for both processes (gov-log b-id-242 and b-id-241-after-clear))
  - detached sleep 243 recorded: pending (no identify output for sleep 243)
  - released case (ordinary, reason released): pending (no record)
- If pending: process trees recorded: pending (tree files missing: bg-bash monitor pre-push subagent setsid nohup human gov-bg gov-det gov-clear);session id events (start, resume, /clear, fork): pending (1 SessionStart lines, 4 expected);sleep 241 and sleep 242 told apart: pending (no identify output for both processes (gov-log b-id-242 and b-id-241-after-clear));detached sleep 243 recorded: pending (no identify output for sleep 243);released case (ordinary, reason released): pending (no record);
- If FAIL: not a FAIL
