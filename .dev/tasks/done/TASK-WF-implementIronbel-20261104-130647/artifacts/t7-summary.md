# T7 fresh-session proof (issue #357)

Run: 2026-11-04. Both sessions are fresh non-interactive `claude -p` runs (Claude Code 2.1.318, model claude-sonnet-5-5) started in `/tmp/bbp-t7-scratch`, with the hook registered only through `--settings ./artifacts/t7-settings.json` (the repo script by absolute path). No `bypassPermissions`: `--allowedTools Bash` (main) and `--allowedTools Bash Agent Task` (subagent run); no `--bare`; `--append-system-prompt` told the model this is a hook test so it would not rewrite the bare call (amendment AMD-08).

## Main session: ./artifacts/t7-main-session.jsonl
- The model called Bash with exactly `echo '{}' | python3 -c 'import sys,json; json.load(sys.stdin)'`.
- Line 15 holds the tool result: is_error true, `PreToolUse:Bash hook error: [.../block-bare-python.sh]: UV-ONLY BLOCK: this command runs bare \`python3\`. Use \`uv run python ...\` (or \`uv pip ...\` / \`uvx ...\`) instead, or \`jq\` to parse JSON.`
- python3 never ran: the only tool result for that call is the block.

## Subagent session: ./artifacts/t7-subagent-session.jsonl
- The main agent made one Agent call and no Bash call; line 18 is the subagent's Bash call (parent_tool_use_id set to the Agent call) with the same command.
- Line 19 holds that call's tool result inside the Agent call: is_error true, the same `UV-ONLY BLOCK:` message naming `uv run python` and `jq`.

## Live ~/.claude was not installed into
## live ~/.claude state BEFORE (2026-11-04T14:44:58Z)
$ ls -l ~/.claude/hooks/block-bare-python.sh
ls: cannot access '/home/coder/.claude/hooks/block-bare-python.sh': No such file or directory
$ grep -c block-bare-python ~/.claude/settings.json
0

## live ~/.claude state AFTER (2026-11-04T14:45:54Z)
$ ls -l ~/.claude/hooks/block-bare-python.sh
ls: cannot access '/home/coder/.claude/hooks/block-bare-python.sh': No such file or directory
$ grep -c block-bare-python ~/.claude/settings.json
0

Before and after values are identical (the hook file is absent and settings.json has 0 matches both times). Expected live side effects of the two runs: transcripts under ~/.claude/projects/ for /tmp/bbp-t7-scratch and the existing user hooks' state files; neither touches ~/.claude/settings.json or ~/.claude/hooks/.

## Artifact review before staging
The jsonl files contain the init record (tool, skill, plugin and MCP server names, cwd /tmp/bbp-t7-scratch, apiKeySource none) and the conversation; no credentials or tokens (checked by grep for api_key/token/secret/password fields).
