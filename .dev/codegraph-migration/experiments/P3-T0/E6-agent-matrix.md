# E6-agent-matrix (Phase 3 Task 2, prerequisite experiment E-6)

Date: 2026-10-31. `claude --version`: **2.1.316 (Claude Code)**. codegraph 1.6.2, seven-tool branch (`CODEGRAPH_MCP_TOOLS=node,search,callers,callees,impact,files,status`).

## Method

- For each agent, a temporary copy `.claude/agents/cg-smoke-<agent>.md` was written in the scratch worktree `.dev/worktrees/cg-sandbox` (`.claude/*` is gitignored there; never staged; deleted with the sandbox). The copy keeps the agent's own frontmatter and body (`permissionMode: plan` and `model:` included) and changes only `name:` and `tools:`: the agent's Phase 1 native tools plus the target roster of source §1.2 (row 5 troubleshoot-analyst, row 7 reflect-reviewer, row 8 reuse-auditor, row 12 auggie-reviewer), plus `mcp__codegraph__codegraph_status` so the brief can make its status call (self decision, decision log).
- Each spawn ran in a fresh headless session started in the sandbox, so the new agent files were loaded at session start:
  `claude -p "<spawn prompt>" --permission-mode dontAsk --setting-sources user,project --output-format json --allowedTools "Agent Task mcp__codegraph__codegraph_status mcp__codegraph__codegraph_search"`.
  The spawn prompt asks for one Agent call with `run_in_background` false (foreground) or true (background); the Agent tool offered that parameter in every session. The brief calls `mcp__codegraph__codegraph_status` and then `mcp__codegraph__codegraph_search {query: install_core_files, limit: 1}`, both with `projectPath` = the sandbox root.
- Pass = the subagent returned real output from both calls (status header and a `file:line` hit) and the session's `permission_denials` list is empty. The session's init event shows the parent's `codegraph` MCP server `connected` in every run.
- A first run with `--setting-sources project` is discarded: that flag also drops the user-scope MCP registration, and a control call showed the headless parent itself had no codegraph tool, so every agent reported `NOT AVAILABLE` for a reason unrelated to the agent (decision log).

## Result

| Agent | Target roster (source §1.2) | Foreground | Background |
|---|---|---|---|
| troubleshoot-analyst | `mcp__codegraph__codegraph_search, mcp__codegraph__codegraph_node, mcp__codegraph__codegraph_callers, mcp__codegraph__codegraph_impact` (row 5) | pass | pass |
| reflect-reviewer | `mcp__codegraph__codegraph_search, mcp__codegraph__codegraph_node, mcp__codegraph__codegraph_callers, mcp__codegraph__codegraph_impact` (row 7) | pass | pass |
| reuse-auditor | `mcp__codegraph__codegraph_search, mcp__codegraph__codegraph_node, mcp__codegraph__codegraph_callers` (row 8) | pass | pass |
| auggie-reviewer | `mcp__codegraph__codegraph_search, mcp__codegraph__codegraph_node, mcp__codegraph__codegraph_callers` (row 12) | pass | pass |

All four agents passed both spawn modes, so Task 5 gives each agent its row's exact codegraph names (never `mcp__codegraph__*`). No permission prompt appeared: the parent session's allow rule covered the two tools, and `permission_denials` stayed empty. Not covered here, carried as known limits: a session with no allow rule for the codegraph tools (an interactive session may then prompt) and a Claude Code version other than 2.1.316 (access decision §9.2: re-run the matrix when the version changes).

## Raw session results

### troubleshoot-analyst / foreground (exit 0)
```text
spawn: ok
run_in_background parameter: yes; value used: false
status: **CodeGraph Status**
search: /home/coder/workspaces/IronClaude/.dev/worktrees/codegraph-adoption/.dev/worktrees/cg-sandbox/src/superclaude/cli/install_core.py:27
{"denials":[],"turns":2,"session":"e872c576-4e6d-4474-9394-5693bf1f962a"}
parent codegraph server: ["connected"]
```
### troubleshoot-analyst / background (exit 0)
```text
spawn: ok
run_in_background parameter: yes; used: true
status: **CodeGraph Status**
search: /home/coder/workspaces/IronClaude/.dev/worktrees/codegraph-adoption/.dev/worktrees/cg-sandbox/src/superclaude/cli/install_core.py:27
{"denials":[],"turns":4,"session":"762463e6-024a-49c0-bacd-62e843e09b9d"}
parent codegraph server: ["connected"]
```
### reflect-reviewer / foreground (exit 0)
```text
spawn: ok
run_in_background: yes, used false
status: **CodeGraph Status**
search: src/superclaude/cli/install_core.py:27
{"denials":[],"turns":2,"session":"ff3839b7-cb2d-4054-b9ac-d69cf7c69f4a"}
parent codegraph server: ["connected"]
```
### reflect-reviewer / background (exit 0)
```text
spawn: ok
run_in_background parameter: yes; value used: true
status: **CodeGraph Status**
search: src/superclaude/cli/install_core.py:27
spawn: ok
run_in_background parameter: yes; value used: true
status: **CodeGraph Status**
search: src/superclaude/cli/install_core.py:27
{"denials":[],"turns":5,"session":"057ffa17-a875-4f64-9c91-f5f9054578a4"}
{"denials":[],"turns":2,"session":"057ffa17-a875-4f64-9c91-f5f9054578a4"}
parent codegraph server: ["connected","connected"]
```
### reuse-auditor / foreground (exit 0)
```text
spawn: ok
run_in_background: yes; used false
status: **CodeGraph Status**
search: src/superclaude/cli/install_core.py:27
{"denials":[],"turns":2,"session":"fcbdee41-8ea5-4b3d-8a17-9b79368ac849"}
parent codegraph server: ["connected"]
```
### reuse-auditor / background (exit 0)
```text
The subagent is still running. Its completion notification has not arrived yet.
spawn: ok
run_in_background parameter: yes; value used: true
status: **CodeGraph Status**
search: src/superclaude/cli/install_core.py:27
{"denials":[],"turns":4,"session":"df92c93c-6bbf-4eea-8e66-b0f4ceec7ed2"}
{"denials":[],"turns":1,"session":"df92c93c-6bbf-4eea-8e66-b0f4ceec7ed2"}
parent codegraph server: ["connected","connected"]
```
### auggie-reviewer / foreground (exit 0)
```text
spawn: ok
run_in_background: yes; used false
status: **CodeGraph Status**
search: src/superclaude/cli/install_core.py:27
{"denials":[],"turns":2,"session":"d5c7687c-1bc3-4f23-999f-8415c97ef813"}
parent codegraph server: ["connected"]
```
### auggie-reviewer / background (exit 0)
```text

spawn: ok
run_in_background parameter: yes; value used: true
status: **CodeGraph Status**
search: src/superclaude/cli/install_core.py:27
{"denials":[],"turns":3,"session":"642f1458-c6ab-4bb2-877f-a3f0edd5753b"}
{"denials":[],"turns":1,"session":"642f1458-c6ab-4bb2-877f-a3f0edd5753b"}
parent codegraph server: ["connected","connected"]
```

Two background rows print the result block twice because the headless session emitted a second result event after the subagent's completion notification; both events carry the same session id and the same two lines.
