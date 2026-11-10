# Research (light): Claude Code hook behaviour relied on by the launch-level hook

quality_tier: fallback_1 (the research protocol skill is not installed as a Skill; official documentation was fetched directly with WebFetch, plus one live experiment in this session)
gathered: 2026-11-05; Claude Code version on this host: 2.1.318

Sources: https://code.claude.com/docs/en/hooks (fetched in three slices, bytes 0-200000 read, the last 86 KB not read), https://code.claude.com/docs/en/permissions, https://code.claude.com/docs/en/tools-reference. Section names are the page's own.

## Verified

| # | Fact | Source |
|---|---|---|
| V1 | PreToolUse input has `session_id`, `cwd`, `permission_mode`, `tool_name`, `tool_input`, `tool_use_id`. Fires for every tool except `EndConversation` (built-ins, `Agent`, `Workflow`, MCP tools). | hooks: "Common input fields", PreToolUse; permissions: "Extend permissions with hooks" |
| V2 | Exit code 2 blocks the call, stderr is the reason. A blocking hook "stops the tool call before permission rules are evaluated, so the block applies even when an allow rule would otherwise let the call proceed". "A call that a PreToolUse hook blocked stays blocked, whichever settings file the hook comes from." | hooks: "Exit code output"; permissions |
| V3 | LIVE EXPERIMENT: in this session (`permission_mode` bypassPermissions, prompts off) the installed `block-bare-python.sh` blocked `python3 --version` with exit 2 and its message. So a PreToolUse block holds when permission prompts are off. | this session, Bash tool |
| V4 | Hooks from settings, managed policy and plugins also run inside subagents; the payload then carries `agent_id` and `agent_type`. | hooks: "Hook locations" |
| V5 | A user-typed `/skill` bypasses PreToolUse; it fires `UserPromptExpansion` instead (fields `expansion_type`, `command_name`, `command_args`, `command_source`, `prompt`; matcher is `command_name`; block with `decision:"block"` or exit 2). A PreToolUse hook on `Skill` fires only when Claude calls the tool. | hooks: "UserPromptExpansion" |
| V6 | `UserPromptSubmit` has no matcher, receives `prompt` (typed slash lines arrive as typed), blocks with exit 2 or `decision:"block"`, and "also fires on turns Claude Code starts on its own". The input has no field telling who started the turn. | hooks: lifecycle table, "UserPromptSubmit input", "Common input fields" |
| V7 | Agent tool is named `Agent`; `tool_input` has `prompt`, `description`, `subagent_type`, `model`. | hooks: PreToolUse; tools-reference |
| V8 | A hook that crashes, exits with a code other than 0 or 2, prints invalid JSON, or times out does NOT block: "The action goes ahead". `"onFailure": "block"` (v2.1.295 or later) turns that into a block, per hook. | hooks: "Block the action when a hook fails" |
| V9 | Matching hooks for one event run in parallel. The page does not say how conflicting decisions combine, but any exit 2 blocks (V2). Default command timeout 600 s. | hooks: "Timeouts" |
| V10 | `if` filters (`"Bash(git *)"`) are best effort: when Claude Code cannot tell what a Bash input runs it runs the hook anyway, and the page says to use the permission system, not a hook, for hard denies. A hook script must therefore do its own matching. | hooks: "How `if` patterns match Bash commands" |
| V11 | Hooks merge across user, project and local settings; `disableAllHooks` and `--settings` can switch non-managed hooks off; only managed policy hooks are immune. The page does not discuss the agent editing settings files. | hooks: "Disable or remove hooks" |
| V12 | `@file` mentions add files without any tool call, so no PreToolUse fires for them. | hooks: UserPromptSubmit notes |
| V13 | `permission_mode` can be `bypassPermissions`; that mode "skips permission prompts, including for writes to protected paths such as `.git` and `.claude`". | permissions: modes table |
| V14 | `--resume <id>` keeps the id; `--fork-session` makes a new one (ccsession evidence, checks 6-8, 12). | `.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md` |

## UNVERIFIED (design must tolerate either answer, and the test plan carries an observed check)

| # | Question | Why it matters | Tolerance |
|---|---|---|---|
| U1 | Is a subagent's (and a nested subagent's) `session_id` equal to the parent session's? | The design keys state on `session_id`. | Key on `session_id`. If a call arrives with an unknown `session_id` but an `agent_id`, treat it as governed only if a bound session exists for the same `cwd` git-common-dir (fallback). Observed check OB-H1 logs the real payload of a subagent Bash call. |
| U2 | Exact `tool_name` and `tool_input` keys of the Skill tool in PreToolUse (`skill`? `name`? `args`?). The docs list built-ins but not `Skill`; the repo hook reads `.tool_input.skill // .tool_input.name`. | Skill gating. | Read both keys; if neither is present for a `Skill` call in a governed session, fail closed for gated levels. OB-H1 logs it. |
| U3 | Whether the model's `Agent` tool is still also called `Task` in PreToolUse. | Subagent rules. | Match `Agent|Task`. |
| U4 | Whether a user `!cmd` shell escape or a Monitor/Cron event passes through UserPromptSubmit. | Human-vs-agent test for "approved". | The approval phrase must be the whole prompt; self-scheduling tools are blocked in governed sessions (see requirements). |
| U5 | Whether `UserPromptExpansion` fires when a typed `/sc:implement` is queued while the agent is mid-turn. | Approval by typing the command. | Both approval routes also accept the plain `approved` reply. |
| U6 | Whether hooks run under `claude --bare`, and whether `--settings` JSON passed by the ccsession shim could carry hooks. | Bypass paths for the guard. | `--bare` is a human-chosen flag, listed as a residual risk. |
| U7 | Whether an `orca agent launch` session receives an Orca worker preamble (so WC-9 would forbid `--submit`). | `--submit` feasibility. | Open decision O-7 for the owner; the hook itself does not read the preamble. |
| U8 | Whether `UserPromptSubmit` fires before the first model call for a prompt passed as the last command-line argument. | First-prompt session binding. | Ccsession evidence shows the prompt arrives as the first user message; OB-H2 checks the binding happens before the first tool call. |

## Consequences used in the seed brief

1. Enforcement must be a PreToolUse block (V2, V3), registered at user level so it also covers subagents (V4).
2. Typed commands and model-called skills arrive on different events (V5), which is the only harness-level difference between "human" and "agent" for slash commands; a plain `approved` reply arrives on UserPromptSubmit (V6).
3. A hook that fails does not block by default (V8); fail-closed has to be done inside the script, and only for governed sessions, because `onFailure: block` would also block ordinary sessions on a hook crash.
4. `if` cannot be relied on to narrow Bash calls (V10); the script must match itself and keep its fast path cheap, because it runs for every tool call.
5. Shell parsing is expensive to get right (see `codebase-context.md` section 2); over-matching words is cheaper than parsing.
