# Research: Claude CLI Output Formats, Tool-Use Mode, and Token Limits

**Topic**: Claude CLI `--output-format` options, tool-use mode capabilities, `--max-turns` behavior, output token limits by model tier, and `--print` continuation behavior  
**Date**: 2026-04-04  
**Status**: Complete  
**Researcher**: Claude Agent  

---

## Research Areas

1. Claude CLI `--output-format` options (text, json, stream-json)
2. Claude model output token limits by tier (Haiku, Sonnet, Opus)
3. Claude CLI tool-use mode and `--allowedTools` flag behavior
4. Claude CLI `--max-turns` behavior and multi-turn patterns
5. `claude --print` continuation and multi-turn output capabilities

---

## 1. `--output-format` Options (text, json, stream-json)

**Relevance**: HIGH  
**Sources**:
- https://code.claude.com/docs/en/cli-reference (official CLI reference)
- https://code.claude.com/docs/en/headless (official headless/programmatic docs)
- https://github.com/Roasbeef/claude-agent-sdk-go/blob/main/docs/cli-protocol.md (CLI protocol spec)

### Findings

The `--output-format` flag accepts three values. It is only valid with `--print` / `-p` mode.

| Format         | Description                                                    | Use Case                      |
|:---------------|:---------------------------------------------------------------|:------------------------------|
| `text`         | Plain text output (default). Only the final text response.     | Simple scripting, roadmap gates |
| `json`         | Structured JSON with `result`, `session_id`, metadata, usage.  | Programmatic consumption      |
| `stream-json`  | Newline-delimited JSON (NDJSON). Each line is a complete JSON object representing a message event. | Real-time streaming, sprint pipeline |

**Key details for `stream-json`**:
- Each line is a complete JSON object representing a message
- Event types include: assistant messages (with `content` blocks of type `text`, `tool_use`, `thinking`), user messages, result messages, system messages, stream messages (with `delta` for incremental text), and control messages
- The `--verbose` and `--include-partial-messages` flags enable token-level streaming: `select(.type == "stream_event" and .event.delta.type? == "text_delta")`
- `--include-hook-events` adds hook lifecycle events to the stream
- GitHub issue #24596 notes that event type documentation is incomplete -- there is no exhaustive reference of all event types

**Key details for `json`**:
- Returns a single JSON object after completion
- The text result is in the `result` field
- When combined with `--json-schema`, validated structured output appears in `structured_output` field
- Session metadata (session_id, usage/tokens) included

**How this relates to our codebase**:
- Our pipeline uses `output_format="text"` for roadmap gates and `output_format="stream-json"` for sprint
- The `text` format only captures the final assistant text response -- tool calls, intermediate reasoning, etc. are invisible
- With `stream-json`, we could observe tool use events, detect when the model is writing files via tools, and track turn counts


## 2. Claude Model Output Token Limits by Tier

**Relevance**: HIGH  
**Sources**:
- https://platform.claude.com/docs/en/about-claude/models/overview (official model comparison)
- https://devtk.ai/en/blog/claude-api-pricing-guide-2026/

### Findings -- Current Models (Messages API, synchronous)

| Model             | Context Window | Max Output (sync API) | Max Output (Batch API) | Pricing (input/output per MTok) |
|:------------------|:---------------|:----------------------|:-----------------------|:--------------------------------|
| **Opus 4.6**      | 1M tokens      | **128k tokens**       | 300k (beta header)     | $5 / $25                        |
| **Sonnet 4.6**    | 1M tokens      | **64k tokens**        | 300k (beta header)     | $3 / $15                        |
| **Haiku 4.5**     | 200k tokens    | **64k tokens**        | N/A mentioned          | $1 / $5                         |

### Legacy Models (still available)

| Model             | Context Window | Max Output |
|:------------------|:---------------|:-----------|
| Sonnet 4.5        | 200k tokens    | 64k tokens |
| Opus 4.5          | 200k tokens    | 64k tokens |
| Opus 4.1          | 200k tokens    | 32k tokens |
| Sonnet 4          | 200k tokens    | 64k tokens |
| Opus 4            | 200k tokens    | 32k tokens |
| Haiku 3 (deprecated April 19, 2026) | 200k tokens | 4k tokens |

### Critical Notes

- The Batch API supports up to **300k output tokens** for Opus 4.6 and Sonnet 4.6 via the `output-300k-2026-03-24` beta header. This is dramatically higher than the synchronous limit.
- The `max_tokens` parameter does NOT factor into OTPM (output tokens per minute) rate limit calculations, so there is no rate limit penalty for setting a higher max_tokens value.
- Opus 4.6 at 128k output tokens is approximately **96,000 words** of text -- a substantial single-turn output.
- Extended thinking is supported by all current models (Opus 4.6, Sonnet 4.6, Haiku 4.5). Adaptive thinking is supported by Opus 4.6 and Sonnet 4.6 only.
- The Models API endpoint can be queried programmatically for `max_input_tokens`, `max_tokens`, and `capabilities`.

**How this relates to our codebase**:
- Our roadmap pipeline generates large markdown documents in a single `--print` invocation
- With Opus 4.6, a single turn can produce up to 128k output tokens (~96k words) -- this is likely sufficient for most roadmap artifacts
- With Sonnet 4.6 / Haiku 4.5, the 64k limit (~48k words) may be tight for very large roadmaps
- The current one-shot architecture is NOT fundamentally limited by output token caps for typical roadmap artifacts (which are usually 5k-20k tokens)
- The REAL constraint is that a single prompt+response exchange must contain the entire output, with no ability to "continue" within `--print` mode (see section 5)


## 3. Claude CLI Tool-Use Mode and `--allowedTools` / `--tools` Behavior

**Relevance**: HIGH  
**Sources**:
- https://code.claude.com/docs/en/cli-reference (official)
- https://code.claude.com/docs/en/headless (official)
- https://www.instructa.ai/blog/claude-code/how-to-use-allowed-tools-in-claude-code

### Findings

#### `--tools` Flag (Restrict Available Tools)
- Controls **which built-in tools Claude can use** during the session
- Accepts: `""` (disable all), `"default"` (all tools), or comma-separated list like `"Bash,Edit,Read"`
- Available built-in tools include: `Read`, `Write`, `Edit`, `Bash`, `Grep`, `Glob`
- Our pipeline currently uses `--tools default` -- meaning Claude has access to ALL tools including file writing

#### `--allowedTools` Flag (Auto-Approve Tools)
- Controls **which tools run without prompting** (permission auto-approval)
- Uses permission rule syntax with pattern matching: e.g., `"Bash(git diff *)"` allows any command starting with `git diff`
- Does NOT restrict which tools are available -- only controls whether they auto-approve
- The trailing ` *` enables prefix matching (space before asterisk is important)

#### `--dangerously-skip-permissions` Flag
- Equivalent to `--permission-mode bypassPermissions`
- Skips ALL permission prompts -- all tool invocations auto-approve
- Our pipeline uses this flag, meaning Claude CAN and DOES use file-writing tools

#### Key Insight: Claude CAN Write Files in `--print` Mode

This is a critical finding. With `--tools default` and `--dangerously-skip-permissions`:
- Claude has access to `Write`, `Edit`, `Bash`, and all other tools
- All tool invocations are auto-approved (no prompts)
- Claude CAN and WILL use these tools to write/edit files on disk during a `--print` session
- Each tool invocation counts as an "agentic turn" toward the `--max-turns` limit

#### Permission Modes in Print Mode

| Mode                  | Behavior in Print Mode                              |
|:----------------------|:----------------------------------------------------|
| `bypassPermissions`   | All tools auto-approve (our current setup)          |
| `dontAsk`             | Denies anything not in `permissions.allow` rules    |
| `acceptEdits`         | File writes auto-approve; Bash/network need rules   |
| `default`             | Would block in non-interactive -- bad for print mode|

**How this relates to our codebase**:
- Our pipeline already has `--tools default` + `--dangerously-skip-permissions` -- meaning Claude subprocess instances already CAN write files directly to disk
- The subprocess is not constrained to stdout-only output. It can use `Write`, `Edit`, and `Bash` to create files
- This means an "incremental writing" architecture is viable: instead of capturing stdout, we could instruct the subprocess to write its output file(s) directly
- However, the subprocess output (stdout) currently goes to a file -- we would need to restructure to either (a) let Claude write files and ignore stdout, or (b) use `stream-json` to observe file-write tool calls


## 4. `--max-turns` Behavior and Multi-Turn Patterns

**Relevance**: HIGH  
**Sources**:
- https://code.claude.com/docs/en/cli-reference (official)
- https://code.claude.com/docs/en/headless (official)

### Findings

- `--max-turns N` -- limits the number of **agentic turns** (print mode only)
- **Exits with an error** when the limit is reached (non-zero exit code)
- **No limit by default** if `--max-turns` is not specified
- Each "agentic turn" is a complete request-response cycle. When Claude calls a tool, that tool result feeds back as a new turn.

#### What Counts as a Turn
- Initial prompt + response = 1 turn
- Each tool use (Read, Write, Bash, etc.) + Claude's next response = 1 additional turn
- So a session with 5 file reads = at least 6 turns (1 initial + 5 tool-use turns)

#### Interaction with Our Pipeline
- Our pipeline sets `max_turns=100` by default (from ClaudeProcess default)
- Sprint uses `timeout_seconds = config.max_turns * 120 + 300` (2 minutes per turn + 5 min buffer)
- If Claude uses tool calls for file writing, each write consumes a turn from the budget

**How this relates to our codebase**:
- If we switch to an incremental-write architecture where Claude writes files via tools, each file write costs a turn
- A roadmap with 8 sections written incrementally would consume ~16+ turns minimum (read context + write file for each section)
- This is well within the default 100-turn limit
- The timeout calculation (2 min/turn) should also remain adequate


## 5. `claude --print` Continuation and Multi-Turn Output

**Relevance**: HIGH  
**Sources**:
- https://code.claude.com/docs/en/headless (official)
- https://code.claude.com/docs/en/cli-reference (official)

### Findings

#### `--print` Mode Is NOT Single-Turn When Tools Are Available

This is the most important finding. Despite its name suggesting "print and exit," `--print` mode is fully agentic:
- With `--tools default`, Claude can make multiple tool calls across many turns
- The session continues until Claude produces a final text response (no more tool calls)
- `--max-turns` limits how many turns Claude takes, but the default is unlimited
- Each turn can include tool use (file reads, writes, bash commands, etc.)

#### Continuation Between Separate `--print` Invocations

The CLI supports continuing conversations between separate invocations:

```bash
# First request
claude -p "Review this codebase for performance issues"

# Continue the most recent conversation
claude -p "Now focus on the database queries" --continue

# Or capture session_id for explicit continuation
session_id=$(claude -p "Start a review" --output-format json | jq -r '.session_id')
claude -p "Continue that review" --resume "$session_id"
```

- `--continue` / `-c` resumes the most recent conversation in the current directory
- `--resume <session_id>` resumes a specific session by ID or name
- This means multi-turn output IS possible across separate `--print` invocations
- However, `--no-session-persistence` (which our pipeline uses) disables this capability

#### The `--no-session-persistence` Constraint

Our pipeline currently passes `--no-session-persistence`, which means:
- Sessions are NOT saved to disk
- Sessions CANNOT be resumed with `--continue` or `--resume`
- Each subprocess invocation is truly isolated

If we removed `--no-session-persistence`, we could:
1. Run a first `--print` invocation to generate part of a roadmap
2. Capture the `session_id` from the JSON output
3. Run subsequent `--print --resume <session_id>` invocations to continue generating

#### `--bare` Mode Note

The official docs recommend `--bare` for scripted/SDK calls and note it will become the default for `-p` in a future release. Bare mode skips auto-discovery of hooks, skills, plugins, MCP servers, auto memory, and CLAUDE.md -- only explicit flags take effect. This could be relevant for our pipeline's isolation needs.

**How this relates to our codebase**:
- Our pipeline uses `--no-session-persistence` which prevents cross-invocation continuation
- However, within a SINGLE `--print` invocation, Claude can make many agentic turns (tool calls) -- it is NOT limited to a single text response
- This means incremental file writing within a single invocation is already possible: Claude can Write file A, then Write file B, then Write file C, all in one `--print` session
- The alternative multi-invocation approach (using `--continue`/`--resume`) would require removing `--no-session-persistence` and adding session tracking logic


---

## Key External Findings

### Finding 1: Output Token Limits Are Not the Bottleneck
- Opus 4.6: 128k tokens (~96k words) per single turn
- Sonnet 4.6 / Haiku 4.5: 64k tokens (~48k words) per single turn
- Typical roadmap artifacts are 5k-20k tokens -- well within limits
- The one-shot architecture is NOT fundamentally limited by output token caps

### Finding 2: `--print` Mode Is Already Multi-Turn Capable
- With `--tools default` and `--dangerously-skip-permissions`, Claude can execute multiple agentic turns within a single `--print` invocation
- Claude can read files, write files, run bash commands, and produce intermediate outputs across many turns
- The session only ends when Claude produces a final response with no tool calls

### Finding 3: Claude CAN Write Files Directly in Our Current Setup
- Our pipeline already passes `--tools default` + `--dangerously-skip-permissions`
- This means Claude subprocess instances already have full tool access including `Write` and `Edit`
- We do NOT need any flag changes to enable file-writing behavior -- only prompt changes

### Finding 4: Cross-Invocation Continuation Exists But We Disable It
- `--continue` and `--resume` allow multi-invocation conversations
- Our `--no-session-persistence` flag explicitly disables this
- Removing that flag would enable a "generate in stages" architecture

### Finding 5: `stream-json` Enables Observability of Tool Use
- Using `--output-format stream-json` instead of `text` would let the orchestrator observe tool_use events in real-time
- This enables monitoring which files Claude writes, progress tracking, and error detection
- Sprint already uses `stream-json`; roadmap uses `text`

---

## Recommendations

### For Incremental Writing Architecture

1. **Lowest-effort approach**: Change the prompt (not the subprocess flags) to instruct Claude to write output files directly using the `Write` tool. The current `--tools default` + `--dangerously-skip-permissions` setup already supports this. The orchestrator would then verify the output files exist after the subprocess exits rather than reading stdout.

2. **Medium-effort approach**: Switch roadmap from `output_format="text"` to `output_format="stream-json"` (matching sprint). Parse the NDJSON stream to observe tool_use events and track which files Claude writes. This gives the orchestrator real-time visibility into incremental progress.

3. **Higher-effort approach**: Remove `--no-session-persistence` and implement session continuation. Run multiple `--print` invocations per artifact, using `--resume <session_id>` to continue. This enables true multi-stage generation but adds significant orchestration complexity.

4. **Consider `--bare` mode**: For pipeline isolation, `--bare` is recommended by Anthropic and will become the default for `-p`. It skips CLAUDE.md discovery, hooks, skills, plugins, and MCP servers -- which is exactly what our pipeline subprocess needs.

### Token Budget Implications
- At Opus 4.6 pricing ($5/$25 per MTok), a 20k-token roadmap artifact costs ~$0.50 in output tokens
- Incremental writing with tool calls will increase input token costs (tool results fed back as context) but output costs remain similar
- The `--max-turns` budget of 100 is generous for incremental writing (typically 10-20 turns needed)

---

## Source URLs

- https://code.claude.com/docs/en/cli-reference
- https://code.claude.com/docs/en/headless
- https://platform.claude.com/docs/en/about-claude/models/overview
- https://github.com/Roasbeef/claude-agent-sdk-go/blob/main/docs/cli-protocol.md
- https://github.com/anthropics/claude-code/issues/24596
- https://www.instructa.ai/blog/claude-code/how-to-use-allowed-tools-in-claude-code
- https://blakecrosley.com/guides/claude-code
- https://devtk.ai/en/blog/claude-api-pricing-guide-2026/
