# OB-H1 fixtures (synthetic)

Every file in this folder is a synthetic hook payload in the documented input shape (top-level `hook_event_name`, `session_id`, and `tool_name` plus `tool_input`, or `prompt` for a prompt event). None of them was captured from a real session. They exist so tests can load a payload by item, and they are not evidence that any observation has been made.

`log-only-probe.sh` is the hook a person registers for a real observation. It appends each hook input as one line to the file named by `LAUNCH_LEVEL_PROBE_LOG`, always exits 0 and never blocks. The existing opt-in probe `../live_probe.py` is reused for what it already records from an actual hook input (`session_id`, `agent_id`, `agent_type`, the top-level and `tool_input` key names and `run_in_background`), plus job-identity selector results. It runs one Bash call with only the Bash tool enabled, and it records the tool name only as `Bash` or `other`. So it can show the ids of item 1 for that one call, and it cannot show a Skill, Agent, Task, SendMessage or MCP call (items 2, 3, 6, 7, 9), a typed prompt or notice (items 4, 5) or a `claude` command (item 8). `log-only-probe.sh` is the way to capture those.

What a real observation must capture, per item (design section 11, OB-H1):

| Item | File | A real observation must capture |
|---|---|---|
| 1 | item1-subagent-ids.json | `session_id`, `agent_id` and `agent_type` of a subagent call and of a nested-subagent call (does the parent's `session_id` appear?) |
| 2 | item2-skill-keys.json | the input keys of a Skill call and the form of the skill name (`skill` or `name`, with or without `sc:`) |
| 3 | item3-agent-isolation.json | the tool name for an Agent or Task call and the `isolation` key |
| 4 | item4-typed-implement-prompt.json | the exact prompt of a typed `/sc:implement x`, and whether the prompt event runs before expansion |
| 5 | item5-monitor-approved-line.json | the exact prompt of a Monitor line `approved` and of background-Bash and background-subagent notices |
| 6 | item6-taskcreate.json | whether `TaskCreate` matches the anchored tool matcher |
| 7 | item7-sendmessage-mcp.json | the tool names of SendMessage and of MCP tools |
| 8 | item8-claude-no-p.json | a `claude` command without `-p` |
| 9 | item9-tool-names.json | the tool names of Bash, Edit, Write and Skill |
