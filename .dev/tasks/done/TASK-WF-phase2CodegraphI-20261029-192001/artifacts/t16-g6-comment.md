**G6 report: codegraph is live on this workspace and Serena and codebase-memory are gone from user scope. Task 16 checks pass.**

PR: https://github.com/IronbellyOrg/IronClaude/pull/329 (merged 2026-10-30T15:23:26Z as 2f10a0e1). The user reported running `./update.sh` on this workspace afterwards (I did not observe that run).

**Coder ordering status (merge gate, re-run just now):** all three print. Step 1 (image bake, Coder #420) merged 12:04Z. Step 2 (Serena retired from the bundle, test-57 asserts codegraph, Coder #422) merged 20:55Z, which is AFTER PR #329 merged at 15:23Z. The plan said to merge #329 only once all three printed, so #329 went in about 5.5 hours before step 2. I did not check whether anything was affected during that gap; it is recorded for the record.

**Read-only checks (the plan's block, run from the worktree; no `claude mcp add/remove`, no install other than `--list`). Block exit: 0**
```
true
=== user-scope clean rc=0
true
=== local-scope clean rc=0
=== user cmds
=== local cmds
MT=node,search,callers,callees,impact,files,status
=== codegraph entry
true
=== version
1.6.2
=== claude mcp get
codegraph:
  Scope: User config (available in all your projects)
  Status: ✔ Connected
  Type: stdio
  Command: /home/coder/.codegraph/versions/v1.6.2/bin/codegraph
  Args: serve --mcp
  Environment:
    CODEGRAPH_TELEMETRY=0
    CODEGRAPH_NO_UPDATE_CHECK=1
    CODEGRAPH_MCP_TOOLS=node,search,callers,callees,impact,files,status

To remove this server, run: claude mcp remove codegraph -s user
=== install --list (codegraph lines)
codegraph MCP (pinned v1.6.2; user scope):
   Executable: /home/coder/.codegraph/versions/v1.6.2/bin/codegraph (1.6.2)
   Owner: owned (receipt) /home/coder/.codegraph/versions/v1.6.2, /home/coder/.local/bin/codegraph -> /home/coder/.codegraph/versions/v1.6.2/bin/codegraph, /home/coder/.codegraph/current -> /home/code
   Ready for Serena retirement: yes
Retired MCP registrations (user scope):
   serena                 absent
=== doctor
🔍 SuperClaude Doctor

✅ pytest plugin loaded
✅ Agents installed
✅ Skills installed
✅ Configuration
✅ ccsession installed
✅ codegraph MCP registration
✅ Retired MCP registrations

✅ SuperClaude is healthy
BLOCK_EXIT=0
```

User-scope removal commands to run: none (`/tmp/p2-t16-user-cmds.txt` is empty, user-scope rc 0). Local-scope removal commands: none (`/tmp/p2-t16-local-cmds.txt` is empty, local-scope rc 0).

**Tool-list observation (fresh headless session started after the update, from a temp directory):** MCP server codegraph = connected. Tools listed: mcp__codegraph__codegraph_callees, _callers, _files, _impact, _node, _search, _status (exactly the seven in MCP_TOOLS). `mcp__codegraph__codegraph_callers` is listed; `mcp__codegraph__codegraph_explore` is not. No serena or codebase-memory tool is listed. (The long-running session that ran this work still shows the old Serena and codebase-memory tools because its tool list was fixed before the update; that is stale session state, not configuration.)
