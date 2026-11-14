# Research: Claude Code headless and hook semantics (W2)
**Topic:** hook events and `PostToolUse` timing, hooks in `claude -p`, `--output-format stream-json` event shape, `--resume` / `--session-id`, `--settings` precedence, subagent and tool restrictions (allowlists, no-Bash agents), `--model` handling for non-Anthropic gateway ids
**Scope:** external web research only (Tavily first); codebase is source of truth
**Status:** Complete
**Date:** 2026-11-14
web-provenance: provider=tavily
---

## 1. Hook event list and when PostToolUse fires

**Source:** https://code.claude.com/docs/en/hooks (official Claude Code docs; reliability: official docs, highest)
**Relevance:** HIGH
**Extracted (Tavily extract, query-reranked passages, not the full page):**
- Event table rows seen: `PermissionDenied`, `PostToolUse` ("After a tool call succeeds"), `PostToolUseFailure` ("After a tool call fails"), `PostToolBatch` ("After a full batch of parallel tool calls resolves, before the next model call"), `Notification`, `MessageDisplay`, `SubagentStart` ("When a subagent is spawned"), `SubagentStop` ("When a subagent finishes"), `TaskCreated`. The rows before `PermissionDenied` (for example `SessionStart`, `PreToolUse`, `Stop`) were not in the extracted passages; the decision table names `UserPromptSubmit`, `UserPromptExpansion`, `Stop`, `ConfigChange`, `PreCompact`, `TeammateIdle`, `TaskCompleted`, so those events exist.
- `PostToolUse` fires only after a tool call SUCCEEDS; a failed call fires `PostToolUseFailure` instead. A collaboration design that posts to a shared board from `PostToolUse` alone would miss failed tool calls.
- `PostToolUse`, `PostToolUseFailure`, `PostToolBatch`, `Stop`, `SubagentStop` use the top-level decision pattern `decision: "block"` plus `reason`. `SubagentStop` with `decision: "block"` keeps the subagent running and delivers `reason` as its next instruction (a hook that exits 2 delivers its stderr the same way).
- To inject context into the PARENT session after a subagent returns, the docs say to use a `PostToolUse` hook on the `Agent` tool (not `SubagentStop`).
- Command hooks receive the event JSON on stdin; hook handler types are shell commands, HTTP endpoints, MCP tool calls, LLM prompts and subagents.
**Relation to codebase:** E2 collaboration designs r1-r5 assume a per-tool-call hook can publish a reviewer's progress to a board file. `PostToolUse` is the documented event for this, with the success-only caveat above. Supports (extends) the E2 assumption at the event level; says nothing yet about gateway model ids (see section 5). The `PostToolUse`-on-`Agent`-tool pattern is directly relevant to the product path, where the orchestrator dispatches reviewers through the Agent call: an orchestrator-side hook could observe each reviewer's return without any `claude -p` child process.

## 2. Hooks inside `claude -p` (print / headless mode) and `--bare`

**Source:** https://code.claude.com/docs/en/headless (official; reliability: official docs)
**Relevance:** HIGH
**Extracted:**
- `--output-format` values: `text` (default), `json` (result, session ID, metadata), `stream-json` (newline-delimited JSON for real-time streaming).
- The headless page says "In CI or other scripted environments, add `--bare` so Claude Code starts without loading the host's hooks, plugins, auto memory, or `CLAUDE.md`." This implies that WITHOUT `--bare`, `claude -p` loads the host's hooks, so hooks run in print mode by default.
- Bare mode: "Hooks still don't run in bare mode when you pass them with `--settings`, or in the `hooks/hooks.json` or `hooks` manifest key of a plugin you load with a flag. Don't use bare mode for a run that needs them." Flags that DO still load things in bare mode: `--append-system-prompt(-file)`, `--settings`, `--mcp-config`, `--agents`, `--plugin-dir`, `--plugin-url` (but not their hooks).
- A `SessionStart` or `Setup` hook that is configured emits `hook_started`, `hook_progress`, `hook_response` events into the `stream-json` stream, before or after the `system/init` event.
**Relation to codebase:** E2 marks "hooks fire in `claude -p`" as [UNVERIFIED]. The official docs support it for the NON-bare invocation. Any collaboration package that launches reviewers with `--bare` (a common recommendation for CI isolation) would silently lose its `PostToolUse` board-writer hook, even if the hook is passed via `--settings`. This is a concrete failure mode to add to the E2 risk list. The docs say nothing about hooks being model-specific, so whether hooks fire when `--model` is a gateway id is still NOT answered by official docs (see section 5).

## 3. stream-json shape, `--resume`, `--fork-session`, cost reporting

**Sources:** https://code.claude.com/docs/en/headless ; https://code.claude.com/docs/en/cli-reference (official docs)
**Relevance:** HIGH (stream-json, resume), MEDIUM (cost)
**Extracted:**
- `stream-json` needs `--verbose` (the documented example is `claude -p "..." --output-format stream-json --verbose --include-partial-messages`); each stdout line is one JSON event. `--include-partial-messages` adds token-level partial events.
- The `system/init` event is the first event in the stream (unless startup events precede it) and carries session metadata: model, tools, MCP servers, loaded plugins, and an optional `capabilities` array of strings (for example `interrupt_receipt_v1`) meant for feature detection. The session id is reported in the `json` result payload and in stream events.
- `--output-format json` payload includes `total_cost_usd` and a per-model cost breakdown. With `--continue` or `--resume` the run reports the whole conversation's total, earlier runs included. Both figures are client-side estimates.
- `--resume` / `--continue` work in print mode (the cost text refers to them for scripted callers). `--fork-session` creates a new session id instead of reusing the original when combined with `--resume` or `--continue`.
- Piped stdin is capped at 10MB; larger inputs must be passed as a file path in the prompt.
- Background work: a `claude -p` run does not wait for MCP work in the background; for other background work it waits and prints `Waiting for background work to finish` to stderr (only when stdout is not a terminal for json/stream-json).
- If the working directory is deleted mid-session the session keeps running and emits a warning in the stream-json output.
**Relation to codebase:** E2 designs need `--resume` to reopen a reviewer's session across rounds. Official docs support `--resume <id>` in `-p`. They do NOT state whether a session created under a gateway model id can be resumed, or whether session storage is keyed to the model. Stays [UNVERIFIED] for gateway ids. The `capabilities` array is a useful capability probe for any transport that must detect hook or resume support at runtime rather than assume it.

## 4. Tool restriction flags and Agent-tool restrictions (no-Bash reviewers)

**Source:** https://code.claude.com/docs/en/cli-reference (official docs)
**Relevance:** HIGH
**Extracted:**
- `--allowedTools` / `--allowed-tools`: tools that run WITHOUT a permission prompt. It does NOT restrict availability; the docs say "To restrict which tools are available, use `--tools` instead."
- `--disallowedTools` / `--disallowed-tools`: deny rules. A bare tool name removes the tool from Claude's context (`"Edit"` removes Edit; the extract shows an empty-looking pattern that removes every tool and an `mcp__` prefix pattern that removes every MCP tool, with the wildcard characters stripped by the extractor, so confirm the exact glob on the page before copying); a scoped rule such as `Bash(rm ...)` leaves the tool available and denies only matching calls.
- `--fallback-model` accepts a comma-separated chain tried in order when the primary model is overloaded or unavailable; `--fork-session` is described above.
**Relation to codebase:** The reflect-reviewer agent (`src/superclaude/agents/reflect-reviewer.md`) is described in the agent list as read-only with an allowlist that has no Bash/Edit/Write/Task. A common mistake is to treat `--allowedTools` as a restriction; per the docs it only pre-approves. For a headless reviewer process, no-Bash enforcement must use `--tools` (availability) or `--disallowedTools Bash`, not `--allowedTools`. Extends the codebase finding: the agent-frontmatter allowlist protects the in-session Agent path only; a `claude -p` reviewer needs its own CLI-level restriction. (Agent frontmatter semantics: see section 5.)

## 5. Subagent definitions: tools allowlist, disallowedTools, model field, nesting

**Source:** https://code.claude.com/docs/en/sub-agents (official docs)
**Relevance:** HIGH
**Extracted:**
- Subagent frontmatter has `tools` (allowlist) and `disallowedTools` (denylist). If both are set, `disallowedTools` is applied first, then `tools` is resolved against the remaining pool; a tool in both is removed. The docs' own example `tools: Read, Grep, Glob, Bash` "can't edit files, write files, or use any MCP tools" (an allowlist excludes MCP tools unless they are listed).
- A `disallowedTools` entry with a specifier such as `Bash(git push ...)` still removes the WHOLE tool for a subagent (unlike the CLI flag, where a scoped rule leaves the tool available).
- `model` field accepts `sonnet`, `opus`, `haiku`, `fable`, a full Anthropic model ID such as `claude-opus-5-5`, or `inherit`; when omitted, Claude Code picks the model by the "subagent model order". The documented values are all Anthropic-family; nothing in this passage documents arbitrary gateway model ids in agent frontmatter.
- If `Agent` is omitted from `tools`, the agent cannot spawn subagents. The `Agent(agent_type)` allowlist syntax only applies to an agent running as the main thread (`claude --agent`); in a subagent definition, listing `Agent` lets it spawn subagents while the depth limit allows, and any type list in parentheses is ignored.
- `permissionMode` in frontmatter is ignored for plugin subagents.
**Relation to codebase:** CODEBASE FINDING (from the task brief): `reflect-reviewer` has an allowlist with Read, Grep, Glob and search MCP tools, and no Bash/Edit/Write/Task. The docs confirm this is the supported way to make a read-only reviewer: because `Agent` is not listed, it cannot spawn nested reviewers, and with no Bash it cannot write the shared board file or run hooks' helper scripts itself. Therefore a collaboration design that needs a reviewer to WRITE to a board (E2 r1-r5) conflicts with the reviewer's own tool allowlist; the write must come from a hook process or from the orchestrator, not from the reviewer's tools. Extends the codebase finding. Note a plugin-shipped subagent also cannot set `permissionMode`, so a plugin-packaged reviewer cannot loosen its own permissions.

## 6. Settings precedence and `--settings`

**Source:** https://code.claude.com/docs/en/settings (official docs)
**Relevance:** HIGH
**Extracted:**
- Managed (organization) settings are the top level and cannot be overridden by user, project, local settings, or `--settings`.
- The command line (`--settings`) "sits above every file except managed" and lasts one session without writing to any file. So a per-reviewer `--settings` JSON can override user/project/local files for that process.
- Some keys do not merge across sources; the whole value comes from the highest source that defines it (managed, then `--settings`, then user), ignoring project and local. Array-valued keys such as `availableModels` are merged across NON-managed scopes as usual, but when managed settings define the list it is applied as-is.
- The extract does not state how `hooks` blocks from several sources combine; the full precedence table and hook merge rules were not in the returned passages. UNCONFIRMED here: whether a `--settings` hooks block replaces or adds to hooks from `~/.claude/settings.json`. Verify on https://code.claude.com/docs/en/settings before relying on either behaviour.
**Relation to codebase:** In this environment, user hooks in `~/.claude/` (freshness, policy hooks) are present. A `claude -p` reviewer launched without `--bare` would also load those host hooks, adding side effects (for example freshness blocks) to each reviewer process. Supports the E2 design choice of a per-reviewer `--settings` file, with the open question above about replace vs add.

## 7. `--model` with non-Anthropic gateway ids

**Sources:** https://code.claude.com/docs/en/model-config (official); https://code.claude.com/docs/en/env-vars (official); https://docs.litellm.ai/docs/tutorials/claude_non_anthropic_models (LiteLLM project docs, well-maintained vendor docs); https://github.com/anthropics/claude-code/issues/55182 (docs issue in the official repo)
**Relevance:** HIGH
**Extracted:**
- Official: `ANTHROPIC_CUSTOM_MODEL_OPTION` adds one custom id to the `/model` picker; "Claude Code skips validation for the model ID set in `ANTHROPIC_CUSTOM_MODEL_OPTION`, so you can use any string your API endpoint accepts." If `availableModels` is set, the custom id must also be in that allowlist, otherwise Claude Code filters it from the picker and "rejects a `--model` selection of it like any other excluded model".
- Official: the `--model` flag and `ANTHROPIC_MODEL` apply only to the session launched with them; "To run different models in different terminals at the same time, launch each one with its own `--model` flag". This supports the E2 pattern of one `claude -p --model <id>` process per reviewer.
- Official: `modelOverrides` keys must be Anthropic model ids; an unrecognised id (for example a gateway alias) produces a `[claude-code:unrecognized_model]` diagnostic line, which can be silenced by adding an entry with that id as its value. So a gateway id is allowed but flagged.
- Official: when routing through `ANTHROPIC_BASE_URL` to a model whose window differs from the built-in size for its name, set `CLAUDE_CODE_MAX_CONTEXT_TOKENS` (behaviour depends on how Claude Code resolves the id, v2.1.193 and later).
- Official: Claude Code v2.1.126 and later can fill the `/model` picker from the gateway's `/v1/models` when `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1` (documented in the official-repo docs issue #55182, which says the docs themselves are missing this behaviour).
- LiteLLM docs: "The `/model` picker only keeps gateway models whose id contains `claude` or `anthropic`", so a non-Anthropic model needs a claude-flavoured id such as `kimi-k3-claude-compatible` to appear in the PICKER; requests keep using that raw id for routing. This is a statement about the picker, not about `--model`; the docs reviewed do not say whether `--model <non-claude-id>` is accepted outright.
- Subagent frontmatter `model` documents only aliases and full Anthropic ids (section 5).
**Relation to codebase:** The product path dispatches reviewers through the orchestrator's Agent call "by model class" (task brief). Subagent frontmatter `model` is documented for aliases and Anthropic ids, so per-reviewer model choice for a NON-Anthropic gateway id is documented only on the `claude -p --model` side. The environment here is itself a LiteLLM-style gateway (model id `claude-gw-tier1b[1m]` shown in the session prompt, a claude-flavoured gateway id); that fits the LiteLLM note that ids containing `claude` pass the picker filter. Neither the official docs nor LiteLLM docs answer whether hooks or `--resume` behave differently for gateway ids; both remain [UNVERIFIED] for gateway ids and need a local probe (see Recommendations).

## 8. Field reports: hooks and resume in `claude -p` (GitHub issues)

**Sources and reliability:** GitHub issues in the official repo `anthropics/claude-code` (maintainer-adjacent but user-reported; reliability: forum-grade, lower than the docs; dates as given in the issue text)
**Relevance:** HIGH for the first three bullets, MEDIUM for the rest
**Extracted:**
- https://github.com/anthropics/claude-code/issues/79702 (opened 2026-07-21, Claude Code v2.1.216, macOS): in print mode `SessionStart` and `Stop` hooks fired but `SessionEnd` did NOT fire on a normal exit, using project `.claude/settings.json` hooks with no plugins. So a design that relies on `SessionEnd` to flush a board in `claude -p` is at risk; `Stop` fired.
- https://github.com/anthropics/claude-code/issues/10373 (date not shown in extract; older): the reporter notes "PreToolUse and PostToolUse hooks work correctly" and that the SessionStart bug "only affects the interactive CLI mode, not `--print` mode". Weak support that `PostToolUse` fires in print mode.
- https://github.com/anthropics/claude-code/issues/37559 (Mar 2026 per the thread): a user reported that no hooks fired in `-p` mode for a `type: "prompt"` hook; a reply in the thread said hooks fire in interactive mode "but not consistently in `-p` pipe mode" and recommended `type: "command"` hooks for automation, and the reporter asked the docs to state the print-mode behaviour. This CONTRADICTS the optimistic reading of section 2 for prompt-type hooks and is unresolved in the extract; command-type hooks are the safer choice.
- https://github.com/anthropics/claude-code/issues/9630 (date not shown): a response states "It is intentional that we do not support UserPromptSubmit hooks in non-interactive mode. Prefer SessionStart hooks for non-interactive mode." Possibly outdated for current versions; check before relying on `UserPromptSubmit` in `-p`.
- https://github.com/anthropics/claude-code/issues/18311 and #22724 (early 2026): `--resume` problems when `sessions-index.json` is out of sync with the `.jsonl` session files, and a resume failure from orphaned `tool_result` blocks after corrupted history; resuming with an explicit session id worked in one report where `--resume` without an id did not. So a transport should always resume by explicit session id, never by "most recent".
**Relation to codebase:** These are exactly the E2 [UNVERIFIED] assumptions (hooks in `claude -p`, resume). The reports show that `PostToolUse`/`Stop` command hooks work in print mode on Anthropic-routed runs, while `SessionEnd`, `UserPromptSubmit` and prompt-type hooks are unreliable there. None of the reports covers a gateway model id; that remains unverified.

## 9. Hooks inside subagents (the product-path Agent dispatch) and hook input fields

**Source:** https://code.claude.com/docs/en/hooks (official docs)
**Relevance:** HIGH
**Extracted:**
- "Hooks from settings files, managed policy settings, and plugins also run inside subagents. When a subagent calls a tool, tool events such as `PreToolUse` and `PostToolUse` fire the same configured hooks as in the main conversation, and the input carries the `agent_id` and `agent_type` common input fields that identify the subagent."
- Common input fields shown: `session_id`, `transcript_path`, `cwd`, `hook_event_name`. `SubagentStart` adds `agent_id` and `agent_type` (the matcher filters on `agent_type`, i.e. the agent name such as `reflect-reviewer`).
- `SubagentStop` adds `stop_hook_active`, `agent_id`, `agent_type`, `agent_transcript_path` (the subagent's own transcript in a nested `subagents/` folder), and `last_assistant_message` (the subagent's final response text, so a hook need not parse the transcript). `transcript_path` there is the MAIN session's transcript. Some `SubagentStop` events come from Claude Code's internal agents (for example prompt suggestions), not from agents Claude spawned, so a hook must filter on `agent_type`.
- Streaming (Agent SDK docs, https://code.claude.com/docs/en/agent-sdk/streaming-output): token-level stream events are emitted for the MAIN session only; subagent deltas are not forwarded. Complete messages carry `parent_tool_use_id` and are the way to attribute output to a subagent. Message types without partial messages: system (init), assistant, result, and a compact-boundary system message. https://code.claude.com/docs/en/agent-sdk/sessions: the session id is on the `result` message's `session_id` (present on success and error) and on the init system message; resume with a session id and `fork_session` yield a new id.
**Relation to codebase:** Extends the codebase finding that the product path dispatches reviewers through the orchestrator's Agent call. A `SubagentStop` hook with `agent_type` matcher `reflect-reviewer` can capture each reviewer's `last_assistant_message` and `agent_transcript_path` with no `claude -p` child, no `--resume` and no reviewer-side Bash. That is an official-docs-supported transport for the "shared board" idea that does not depend on the two [UNVERIFIED] assumptions. Limit: the Agent path runs reviewers on the orchestrator's gateway and model-class mapping, not on a per-reviewer arbitrary gateway id (section 7). The statement that hooks are model-independent is an inference from hooks being client-side shell commands; no source reviewed states it.

## 10. `--session-id`, `--settings`, restricted mode

**Source:** https://code.claude.com/docs/en/cli-reference (official docs)
**Relevance:** HIGH
**Extracted:**
- `--session-id <uuid>`: use a specific session id; must be a valid UUID. This lets an orchestrator choose each reviewer's session id up front and later `--resume` it by explicit id, instead of parsing the id from output.
- `--settings`: a path to a settings JSON file or an inline JSON string (file must be a regular file of at most 2 MiB). Values override the same keys in the settings files for this session; keys you omit keep their file-based values.
- `--setting-sources user,project,local`: choose which file sources load.
- `--restricted` (Claude Code v2.1.248 or later): for evaluation harnesses; removes built-in tools that run commands or code and WebFetch unless named in `--tools`, confines file tools to the working directories, loads only managed settings and `--settings`, and refuses `bypassPermissions`. Closest official analogue of a read-only reviewer process.
**Relation to codebase:** E2's per-reviewer process can pin its own session id with `--session-id`, which removes one parsing risk. `--restricted` is a candidate for the "read-only reviewer without Bash" requirement at process level, as an alternative to relying on the agent file's allowlist (which only applies to Agent-tool subagents). Version gates (v2.1.248 and later) must be checked against the installed client; not verified locally.

---

## Key External Findings

1. [Official docs, HIGH] `PostToolUse` fires only after a SUCCESSFUL tool call; failures fire `PostToolUseFailure`. A board-writer hook needs both events (https://code.claude.com/docs/en/hooks).
2. [Official docs, HIGH] Hooks load in `claude -p` unless `--bare` is used; in `--bare` mode hooks passed through `--settings` or a flag-loaded plugin still do NOT run (https://code.claude.com/docs/en/headless). A reviewer launched with `--bare` loses its hooks.
3. [Field reports, MEDIUM] In print mode `PostToolUse`, `Stop`, `SessionStart` command hooks worked in the reports reviewed; `SessionEnd` did not fire on normal exit in v2.1.216 (issue 79702); `UserPromptSubmit` is reported unsupported in non-interactive mode (issue 9630, date unknown); prompt-type hooks were reported unreliable in `-p` (issue 37559). Prefer `type: "command"` hooks.
4. [Official docs, HIGH] Hooks also run inside subagents spawned by the Agent tool, with `agent_id` and `agent_type` in the input; `SubagentStop` exposes `last_assistant_message` and `agent_transcript_path`. The product Agent-dispatch path can be observed by hooks without `claude -p`.
5. [Official docs, HIGH] `--allowedTools` only pre-approves; it does not remove tools. Availability restriction uses `--tools`, `--disallowedTools`, or `--restricted`. In subagent frontmatter, `tools` is an allowlist and `disallowedTools` a denylist applied first; omitting `Agent` stops nesting.
6. [Official docs, HIGH] `--model` and `ANTHROPIC_MODEL` are per-process, so one `claude -p --model <id>` per reviewer is a supported pattern; custom model ids skip validation (via `ANTHROPIC_CUSTOM_MODEL_OPTION`) but are rejected if `availableModels` is set and omits them.
7. [LiteLLM docs, MEDIUM] The `/model` picker keeps only gateway ids containing `claude` or `anthropic`; routing still uses the raw id. This says nothing about `--model` acceptance, hooks or resume for such ids.
8. [Official docs, HIGH] `--session-id <uuid>` pins the session id; `--resume <id>` and `--fork-session` exist; stream-json needs `--verbose`; the init system event carries model, tools and a `capabilities` array; `--output-format json` returns `total_cost_usd`. Field reports advise resuming by explicit id only.
9. [Official docs, HIGH] `--settings` overrides file settings for one session, below managed settings; precedence of the `hooks` key across sources (replace vs add) was NOT confirmed in the passages retrieved.

## Recommendations from External Research

1. Do not mark "hooks fire in `claude -p`" as verified for gateway model ids. The official docs support it for default (non-bare) print mode and the field reports support `PostToolUse`/`Stop`, but no source tests a non-Anthropic gateway id. Plan a one-call local probe: `claude -p --model <gateway-id> --settings <file with PostToolUse command hook that touches a marker> --output-format stream-json --verbose "read one file"` then check the marker, the `hook_*` events, and the `system/init` `model` field. Same probe for `--session-id <uuid>` followed by `--resume <uuid>` under the gateway id. (Probe command shape is derived from the documented flags, not tested here.)
2. Never launch collaboration reviewers with `--bare` if they depend on hooks.
3. Hook on both `PostToolUse` and `PostToolUseFailure`; prefer `type: "command"` hooks; do not depend on `SessionEnd` or `UserPromptSubmit` in print mode. Use `Stop` for end-of-run flushes.
4. For the unified Review Panel, prefer the Agent-dispatch path with a `SubagentStop` command hook (matcher `reflect-reviewer`) as the collaboration/board transport: it is documented, needs no reviewer Bash, no `--resume`, and no gateway-specific process. Keep per-reviewer `claude -p` processes (E2 r1-r5) only for reviewers that must run on a gateway model id that the Agent tool cannot select; for those use `--session-id`, `--resume <explicit id>`, `--settings` with a command hook, and a CLI-level read-only restriction (`--tools` or `--restricted`, not `--allowedTools`).
5. Keep the reviewer agent's tool allowlist as is (no Bash, no `Agent`); it matches the documented restriction model. Writes to a board must come from a hook or the orchestrator.
6. Treat the open `hooks` merge question (section 6) as a blocker only if a design layers a `--settings` hooks block on top of the user's `~/.claude` hooks; verify on the settings page or with a marker-file test.
7. Codebase precedence reminder: every item above that touches `src/superclaude/agents/reflect-reviewer.md`, the E2 packages or the orchestrator's dispatch code is context only; where verified code behaviour differs, the code wins. No discrepancy with the codebase was found in this research, because the codebase side for these items is marked [UNVERIFIED] in the brief and no code was read here.

## Gaps and unconfirmed items

- Full hook event list and the exact `PostToolUse` input schema (`tool_response` shape) were not in the passages retrieved; only the events named above were seen.
- Hook merge behaviour across settings sources: not confirmed.
- Gateway model id behaviour for hooks, `--resume`, `--session-id` and subagent `model:` frontmatter: not documented in any source reviewed.
- Dates of issues 9630 and 10373 were not shown; their statements may be outdated.
- Extractor output strips some wildcard characters from code spans; check exact globs on the source pages before copying.
- Tavily returned passages, not full pages, for the official docs; statements are limited to those passages.

