# Research (light): how reviewer agents can exchange messages during a run

- Date: 2026-11-13
- Question: which communication method lets several headless reviewer sessions
  (`claude -p --model <id> --output-format json --permission-mode bypassPermissions
  --disallowedTools Edit Write NotebookEdit`, launched in parallel by a bash script,
  each in a sandbox repo copy, 2-15 minute runs, some on non-Claude gateway models)
  exchange short messages mid-run and between phases.
- Priority: simplicity and speed of implementation, then reliability, then latency.
- Method: read-only. Local CLI help (Claude Code 2.1.323, Orca shim), web docs.
  No messages sent, no sessions created.
- Status: complete (see end of file).

## 1. Orca agent mail (orchestration messages)

Executable: `ORCA_CLI_COMMAND` unset; this shell is inside an Orca terminal
(`ORCA_TERMINAL_HANDLE` set), so `orca` applies; it resolves to
`/home/coder/.config/orca/linux-orca-cli-shim/orca` (a shim that execs
`/opt/Orca/resources/bin/orca-ide`), not the screen reader. Orca app 1.4.245,
runtime `ready` (`orca status --json`). Sources: `orca --help`,
`orca orchestration {send,check,reply,ask,run-create,worker-start} --help`,
`orca skills get orchestration`, `... --reference references/messaging-and-gates.md`.

**Model.** A Run is a durable namespace plus one coordinator inbox. Mail goes to
`run:<id>` (the coordinator's FIFO inbox) or `dispatch:<id>` (one supervised
worker attempt). Group addresses (`@all`, `@claude`, `@grok`, ...) reach "the live
Dispatches of your own Run"; "a sender in no Run must use run:<id> or
dispatch:<id>" (`send --help`). Message types are fixed: status, dispatch,
worker_done, merge_ready, escalation, handoff, decision_gate, question, heartbeat.

**Send (headless reviewer).** Bash tool call, e.g.
`orca orchestration send --to dispatch:<peer_dispatch_id> --type status --subject "R2 finding" --body "<text>" --json`.
**Receive.** `orca orchestration check --terminal <own_handle> --json`, then
`check --terminal <own_handle> --ack <delivery_id> --json` until `count` is 0
(skill, worker obligation 3). `check` identifies the caller only by a
runtime-issued terminal handle (`--terminal`), or implicitly inside an Orca terminal.

**Fit with `claude -p`.** Poor. A bash-launched `claude -p` reviewer is not an
Orca terminal and owns no Dispatch, so it has no own mailbox: it can only send
to `run:<id>`/`dispatch:<id>`, and it cannot `check` a mailbox of its own.
Reading the shared Run inbox with `check --run` consumes the coordinator's FIFO
batch ("replays that exact batch until acknowledged"; concurrent waiters "share
the outstanding batch and reserve nothing"), so N peers draining one inbox would
steal each other's mail. Per-reviewer mailboxes require each reviewer to be a
supervised worker started with `orca orchestration worker-start --agent claude
--model <id>`, which launches a TUI agent (or chat, per the user's setting) in a
worktree, not a `claude -p` with JSON output. `--model` is supported for
Claude, Codex, Cursor, Antigravity and Muse ids; whether gateway ids like
`gpt-6-luna` or `grok` pass through `--agent claude --model` is UNVERIFIED.
Child processes of the harness also inherit the parent terminal's `ORCA_*` env
vars, so implicit caller resolution would make every reviewer look like the
harness terminal (inference from env inspection; not tested, no messages sent).

**Mid-run.** Works only between the reviewer's tool calls (it must run `check`);
`send` "proves durable enqueue; its wake or nudge is best-effort attention only"
(skill, safety floor). **Delivery:** durable, FIFO per mailbox, at-least-once
replay until ack. **Ordering:** FIFO per mailbox. **Latency:** one CLI round trip
(sub-second to seconds) plus the reader's polling cadence. **Failure modes:**
Orca runtime not running (any run of the harness off an Orca host loses the channel);
mailbox identity mistakes; unacked batches hide newer mail; heavy protocol
(Run/Task/Dispatch lifecycle, worker_done, release) the reviewer prompts would
have to follow. **Setup effort:** high: replace the `claude -p` launcher with
`worker-start`, capture Dispatch ids, inject them into each prompt, lose
`--output-format json` result capture (read output via `worker-read`), add
release/cleanup. **Verdict:** wrong tool for peer-to-peer reviewer chat; it is a
coordinator-to-worker supervision layer.

## 2. Claude Code built-in messaging (agent teams, subagents, cross-session SendMessage)

Three separate features share the `SendMessage` tool. Local version 2.1.323
(`claude --version`); all version floors below are met.

**2a. Agent teams (teammates).** Experimental, off by default
(`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`). "Spawning teammates also requires an
interactive session. In non-interactive mode with the `-p` flag, including Agent
SDK sessions, Claude doesn't spawn teammates" and a named subagent "runs as an
ordinary subagent" (https://code.claude.com/docs/en/agent-teams, "Enable agent
teams"). Teammates are spawned by one lead; per-teammate `model` comes from the
agent definition (same page, "tools"/"model" bullets). **Not usable** for
independent bash-launched `claude -p` reviewers.

**2b. Subagents inside one session.** "Subagents that Claude named when it
spawned them can also message each other" (agent-teams comparison table). This
would mean one lead `claude -p` spawning every reviewer as a subagent: a harness
rewrite, one shared process, no per-reviewer `--output-format json`, and the
model per subagent is limited to what an agent definition's `model` accepts
(gateway ids UNVERIFIED). Not recommended.

**2c. Cross-session messaging (separate processes). This one fits.** Source:
https://code.claude.com/docs/en/cross-session-messaging (fetched as `.md`).
- "Claude Code binds an inbox socket for a `claude -p` session like an
  interactive one, so a long-running `-p` worker can receive messages and appears
  in the listing." Bare mode (`--bare`) binds no socket.
- Delivery: "The receiving Claude reads the message between tool calls during an
  active turn. When the receiving session is idle, Claude Code starts a new turn
  with the message." So mid-run delivery is automatic; no polling in the prompt.
- Send/receive: the reviewer calls `ListAgents` then `SendMessage({to:
  "<session name>", message})`; a session answers to its `--name` (`-n`). The
  receiver gets plain text with sender name and a reply address. Same-machine
  transport is a per-session Unix socket, never Anthropic servers; available on
  every provider (v2.1.248+ on non-first-party providers / flag fetching off).
- Inbound gating: with no `crossSessionInbound` set, a receiver that bypasses
  permissions holds messages unless the sender also bypasses. All reviewers run
  `bypassPermissions`, so they should deliver to each other; to be explicit,
  start each with `--settings '{"crossSessionInbound":"accept"}'`. A `-p`
  session cannot show the approval dialog; held messages expire after
  `dialogExpiry` (5 min default) and the sender is told.
- Limits: plain text only; ~1M char cap; burst and loop throttling; receiver
  queues at most 50 accepted messages.
- Harness change: add `--name panel-<run>-<reviewer>` and the `--settings`
  JSON to each `claude -p` line; tell each prompt the peer names. Roughly 2
  lines of bash plus prompt text. `SendMessage`/`ListAgents` are not in the
  current `--disallowedTools` list.

Risks (UNVERIFIED, need a 10-minute spike): whether gateway non-Claude models
call `SendMessage` reliably with the right name; what happens to a message that
lands after a reviewer's final turn (an idle `-p` session "starts a new turn",
which could change or delay the `--output-format json` result, or the process
may already have exited and the send fails); `ListAgents` shows every local
session on this host (dozens here), so names must be unique per run; messages
leave no file the eval can audit except session transcripts; sandbox repo
copies are fine (same machine), but a reviewer in a different container could
not reach the others.

Side note: `claude -p --input-format stream-json --output-format stream-json`
lets the harness push user messages into a running session over stdin; SDK
messages carry `priority` `next` (default) / `later` / `now` for "when a message
sent during a running turn reaches Claude" (context7, agent-sdk/typescript
`SDKUserMessage`). It needs a long-lived stdin writer per reviewer and a
stream parser; more code than options 2c or 4.

## 3. A2A (Agent2Agent) protocol

- Status: spec v1.0.0 is "Latest Released Version" (https://a2a-protocol.org/latest/specification),
  released 2026-03-12; Linux Foundation project since 2025-06-23, accepted into
  the Agentic AI Foundation in 2026-08 (getmaxim.ai summary; LF press release).
  v1 transports: JSON-RPC 2.0, HTTP+JSON/REST, gRPC; updates by polling, SSE
  streaming, or webhook push.
- Minimal implementation: each agent is an HTTP server exposing an Agent Card
  (JSON at a well-known URI) plus `SendMessage`/`GetTask`; peers are A2A
  clients. Library: official Python SDK `a2a-sdk`
  (https://github.com/a2aproject/a2a-python; `uv add "a2a-sdk[http-server]"`),
  `A2AStarletteApplication` + `DefaultRequestHandler` + an `AgentExecutor`.
- Fit with `claude -p`: A2A is request/response between services; it has no
  way to put a message into a running `claude -p` turn. Wrapping a reviewer
  means a Python server per reviewer (or one router) that owns the session
  (Agent SDK or stream-json stdin) and translates A2A messages into injected
  user messages, plus a client tool (Bash `curl` or an MCP tool) for sending.
  That is option 4 or 2c with an HTTP server and a dependency in front.
- Delivery/ordering: per-HTTP-request; durability only if a task store is
  configured. Latency: milliseconds on localhost plus the same "between tool
  calls" limit. Failure modes: port allocation, server lifecycle, crashes,
  auth. Setup effort: highest of the four (days, new dependency, new process
  type). Value here: none beyond interoperability with external agents, which
  this panel does not need.

## 4. Plain JSON files on a shared directory (board) + hook injection

**Layout.** Harness creates `BOARD=$(mktemp -d)/board` outside every sandbox
copy and exports `PANEL_BOARD` and `PANEL_ID` before each `claude -p`. Each
reviewer appends only to `$PANEL_BOARD/<PANEL_ID>.jsonl` (single writer per file,
so no interleaving; one `>>` write of one short line is effectively atomic on
local Linux filesystems because `O_APPEND` positions each write at end of file).
Whole-file artifacts (phase outputs) use write-to-temp then `mv` (rename is
atomic on one filesystem).

**Send.** Reviewers have Bash (only Edit/Write/NotebookEdit are disallowed), so:
`printf '%s\n' '{"from":"r2","ts":"...","text":"..."}' >> "$PANEL_BOARD/$PANEL_ID.jsonl"`,
or better a 5-line helper `panel-post "<text>"` on `PATH` that builds the JSON
with `jq -cn` (avoids quoting errors by weaker models).

**Receive, option A (prompt polling).** Prompt says "before each new file or
check, run `panel-read`"; helper prints peer lines past a per-reviewer cursor
file. Simple, but compliance depends on the model remembering, which is the
weak point with non-Claude models.

**Receive, option B (hook injection, recommended).** Hooks run in `-p` sessions
(only `--bare` skips them, https://code.claude.com/docs/en/headless). A
`PostToolUse` hook (matcher `*`) returns
`{"hookSpecificOutput":{"hookEventName":"PostToolUse","additionalContext":"<new peer messages>"}}`;
"Claude Code wraps the string in a system reminder and inserts it at the point
where the hook fired"; values over 10,000 chars are spilled to a file with a
2,000-char preview (https://code.claude.com/docs/en/hooks, "Add context for
Claude", "PostToolUse decision control"). The hook script reads peer files past
its cursor, advances the cursor, prints nothing when there is nothing new.
Pass the hook per reviewer with `--settings '<json>'` so it does not touch
user settings. A `Stop` hook can run the same reader once more at the end and,
if there is unread mail, return `decision: "block"` with the messages as
`reason` so the reviewer reconsiders before finishing (loop guard:
`stop_hook_active` input and the 8-continuation cap, same page). PreToolUse
`additionalContext` is not documented in the fetched excerpts, so use PostToolUse.

**Properties.** Mid-run: yes, at the receiver's next tool call, automatically,
and it is CLI-side so it works the same for gateway models. Delivery: durable
(files persist), at-least-once with a cursor, exactly-once per reader if the
cursor advances only after printing. Ordering: per-sender order exact; across
senders, order by `ts` (good enough for chat). Latency: sender's write is
immediate; receiver sees it after its next tool call (seconds to tens of
seconds; a reviewer in a long no-tool generation sees nothing until it calls a
tool). Failure modes: malformed JSON lines (reader skips lines `jq` rejects);
cursor file races (one reader per cursor, so none); a reviewer that never calls
a tool after a message (Stop hook covers it); disk path not shared if a
reviewer runs in another container. Free audit log for the eval: the board is
the transcript of the exchange. Setup: about 40 lines of bash (post helper,
read helper/hook, `--settings` JSON, export of two env vars). Inference, not
tested: hook commands inherit the `claude -p` process environment, so
`PANEL_BOARD`/`PANEL_ID` reach the hook.

## Comparison

| | 1. Orca mail | 2c. Cross-session SendMessage | 3. A2A | 4. JSON board + PostToolUse hook |
|---|---|---|---|---|
| Works with bash-launched `claude -p` | No own mailbox; needs `worker-start` rewrite | Yes (not `--bare`) | Only via a wrapper server | Yes |
| Mid-run receive | Model must poll `check` | Automatic, between tool calls | Needs injection layer | Automatic, after each tool call |
| Non-Claude gateway models | Unverified `--model` passthrough | Depends on model calling the tool with the right name | n/a | Model-agnostic on receive; send via Bash helper |
| Delivery guarantee | Durable, ack-based | Socket; held msgs expire after 5 min; drops if receiver gone | Per request | Durable files, cursor-based |
| Ordering | FIFO per mailbox | Arrival order per receiver | Per request | Per sender exact; global by timestamp |
| Latency | CLI call + poll cadence | Next tool call | ms + next tool call | Next tool call |
| Audit log for the eval | Orca inbox | Transcripts only | Server logs if built | The board files |
| Setup effort | High | Very low (2 flags + prompt) | Highest | Low (~40 lines bash) |
| Main risk | Wrong layer (supervision, not peer chat) | End-of-turn behaviour and gateway tool use unverified | Overkill | Prompt or hook bug; shared path |

## Recommendation

(a) **Mid-run exchange: option 4, JSON board with a PostToolUse hook that
injects new peer lines as `additionalContext`, plus a Stop hook for one final
check, and a `panel-post` Bash helper for sending.** It is model-agnostic on the
receive side, durable, leaves an audit log, needs no new service, and is a small
change to the existing launcher (`export PANEL_BOARD PANEL_ID`,
`--settings '<hooks json>'`). Cheaper alternative worth a 10-minute spike:
cross-session `SendMessage` (2c) needs only `--name` and
`--settings '{"crossSessionInbound":"accept"}'`, but its end-of-turn behaviour
in `-p` and gateway-model tool use are unverified, and it leaves no board file.

(b) **Between-phase exchange: plain files, harness-mediated, no live channel.**
After phase 1 the harness collects each reviewer's JSON result, writes one
digest file (temp + `mv`), and starts phase 2 either fresh with the digest in
the prompt or with `claude -p --resume <session_id> "<digest>"` (session id is
in the `--output-format json` result). This is deterministic, needs no hooks,
and is the least code. Orca mail (1) and A2A (3) are not recommended for either.

- Status: complete.
