3e7c7011cc0c319cb87f6ca4c6b3d34cde643451
family=telemetry-parse (status-text parse rules that do not match the real codegraph 1.6.2 output)
defect form: a parse rule in the skill that assumes a line shape the 1.6.2 CLI or MCP output does not have
command: grep -n -E -e "first line" -e "Files:" -e "Pending Changes" -e "init_running" -- src/superclaude/skills/sc-graph-protocol/SKILL.md
before:
39:| R4 | `mcp__codegraph__codegraph_status {"projectPath": "<worktree_root>"}` when it is in this session's tool list → `access: mcp`. Else, only w
40:| R5 | classify the R4 text | "belongs to a different git working tree" → `foreign_index`, `worktree_relation: parent`, `graph:foreign_index`; CL
48:2. **G-T Telemetry.** If the binary is present: `codegraph telemetry status`. A first line with `enabled` or `on` → `telemetry: on` and token `gr
49:3. **G-C Counts.** From the R4 text: CLI `Files:`, `Nodes:`, `Edges:` lines, or MCP `Files indexed:`, `Total nodes:`, `Total edges:` → `counts {f
60:   | `stale` | `wait_for_sync` | `init_running` → "an init or index is running (usually the session-start hook); wait and run `/sc:graph status`"
74:   | `pgrep -f 'codegraph\.js (init|index)'` prints a line | any | blocked, `refused_reason: init_running`, `next_action: wait_for_sync`, message "
108:| `init.refused_reason` | enum or null | `disabled` \| `absent` \| `init_running` \| `already_initialized` \| `nested_worktree` \| `worktree_local
coupled sites: G-C counts (CLI prints thousands separators, e.g. "8,824"; MCP prints "**Files indexed:** 971"); R4 init_running branch (no status text to parse: worktree_relation and counts undefined); real outputs: codegraph telemetry status first line blank, then "Telemetry: enabled (your saved choice)"

after:
39:| R4 | `mcp__codegraph__codegraph_status {"projectPath": "<worktree_root>"}` when it is in this session's tool list → `access: mcp`. Else, only w
40:| R5 | classify the R4 text | "belongs to a different git working tree" → `foreign_index`, `worktree_relation: parent`, `graph:foreign_index`; CL
48:2. **G-T Telemetry.** If the binary is present: `codegraph telemetry status`, then classify the line that starts with `Telemetry:` (codegraph 1.6.2
49:3. **G-C Counts.** From the R4 text: CLI `Files:`, `Nodes:`, `Edges:` lines (printed with thousands separators, for example `8,824`; drop the comma
60:   | `stale` | `wait_for_sync` | `init_running` → "an init or index is running (usually the session-start hook); wait and run `/sc:graph status`"
74:   | `pgrep -f 'codegraph\.js (init|index)'` prints a line | any | blocked, `refused_reason: init_running`, `next_action: wait_for_sync`, message "
108:| `init.refused_reason` | enum or null | `disabled` \| `absent` \| `init_running` \| `already_initialized` \| `nested_worktree` \| `worktree_local
