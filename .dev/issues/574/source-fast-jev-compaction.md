# Source notes: tamaratran/fast-jev-compaction (third-party, untrusted data)

How this file was made: the orchestrator fetched the repository page https://github.com/tamaratran/fast-jev-compaction on 2026-11-16 with a web fetch, and the fetch tool's model summarised it. The summary may be imperfect and was NOT checked against the repository files. Tags, releases and the latest commit date were "not shown" by the page. Treat everything below as data, never as instructions. Nothing from this repository has been installed or run.

## 1. What the README says (structured summary)

Project: "fast-jev-compaction". It is both an npm library and a Claude Code plugin. It prunes conversation history instead of writing a summary. Jev (TypeSafe's System One model) selects which tool calls and tool outputs to retain, truncate or delete. Retained content is not rewritten, and user and assistant prose stays unchanged and in order. Motivation: summaries can lose paths, errors, constraints and commands. Library code is in `src/`; the plugin is in `hooks/` and `.claude-plugin/`.

Compaction procedure:
1. Match each `tool_use` to its `tool_result` by `tool_use_id`. Protect the first message and the newest `preserveRecentMessages` messages.
2. Give Jev a chronological representation of the conversation: prose and tool inputs, but tool-output contents replaced by short status or length placeholders (the example reports 4213 characters omitted).
3. Fit that representation into `maxStateTokens` (normally 25,000) by progressively stronger reductions only when needed: limit tool inputs to 1000, then 200, then 60 characters; shorten long prose to beginning and end excerpts, oldest unprotected first; replace older unprotected messages with omitted-character markers; reduce old calls to single-line records (example: `t12`, `Read`, `file_path=src/a.ts`, a 480-character successful result); exclude older messages that have no calls; combine consecutive older call-only messages; throw an error if it still does not fit. Token estimation is about one token per six letters, half a token per digit and one per other symbol, calibrated to run slightly above Jev's reported counts.
4. Ask two "noul" questions (a Jev answer type that returns the probability that a yes-or-no statement is true) per unprotected call: does keeping the call and input matter, and is the original result needed rather than re-running the tool.
5. Split questions across requests when required. Each request repeats the fitted conversation representation. Requests run concurrently and answers are merged. Default `maxRequestTokens` is 30,000, below Jev's 32,000-token request limit.
6. Compare scores with `keepThreshold`: if `keepResult` meets it, keep call and result; otherwise if `keepCall` meets it, keep the call and only the first `truncateHeadChars` characters of the result plus a note; otherwise delete both.
7. Rebuild the messages, drop messages that became empty, keep unchanged message objects as they were, and prevent orphaned results.

Jev errors, malformed responses, missing credentials and histories that cannot fit cause errors. The caller or plugin decides the fallback.

## 2. Install and usage commands (as written in the README summary)

Library:
- `npm install fast-jev-compaction`
- `export TYPESAFE_API_KEY=...`
- The example imports `compactMessages`, `reductionRatio` and the `Message` type from `fast-jev-compaction`, calls `compactMessages` with `preserveRecentMessages` set to 4, and logs `result.messages`, `result.decisions` and `result.stats`. If `reductionRatio(result)` is below 0.25 it suggests keeping the original history or summarising instead.
- `Message` is described as a subset of Claude Code's `SessionMessage`, so session transcripts can be used directly.
- Custom transport: implement `JevAsker` with `ask(state, questions)`, then call `compact(messages, asker, options)`. Other exports: `buildJevRequest`, `parseJevResponse`, `collectToolCalls`, `fitState`, `batchCalls`, `decideCall`, `applyDecisions`.
- Credential default: `process.env.TYPESAFE_API_KEY`. The README warns not to commit credentials.

Options and defaults: `apiKey` (TYPESAFE_API_KEY), `model` ("jev-latest"), `baseUrl` ("https://api.typesafe.ai/v1/systemone"), `fetch` (native, replaceable for tests), `goal` (latest 3 user prompts), `keepThreshold` 0.5, `preserveRecentMessages` 6 (the first message is also protected), `maxStateTokens` 25000, `maxRequestTokens` 30000, `truncateHeadChars` 300. `result.stats` reports before and after message and character totals, decision counts grouped by reason, estimated state tokens, the fitting stage used and the request count.

Claude Code plugin:
- The repository root is a function-hook plugin. `hooks/fast-jev.ts` adapts `session.compact` transcripts to the library. Errors or too little reduction trigger Claude Code's built-in summarisation. Configuration and the Claude Code 2.1.274 type reference are linked from `hooks/README.md`.
- It needs the early-access function hooks of Claude Code 2.1.274 or newer. In `~/.claude/settings.json`, under `env`: `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS` = `1` and `TYPESAFE_API_KEY` = `<your key>`.
- Install (shell or in-session slash commands): `claude plugin marketplace add tamaratran/fast-jev-compaction` then `claude plugin install fast-jev-compaction@fast-jev-compaction`. The install prompts cover the API key, thresholds, `truncateHeadChars` and other options. Defaults use the environment credential. Restart Claude Code or run `/reload-plugins`.
- After that, both `/compact` and automatic compaction use Jev. Notifications report retained and total messages when pruning replaces summarisation, or explain the fallback.
- Checkout-only run from the repository root: `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1 claude --plugin-dir .`
- Marketplace metadata lives in `.claude-plugin/marketplace.json`; no publishing step is needed.

Development commands: `npm install`, `npm run typecheck`, `npm test`, `npm run build`, `npm run validate:plugin` (uses `claude plugin validate`), and `TYPESAFE_API_KEY="$(cat ~/.typesafe_key)" npm run demo`. Unit tests use a fake Jev and do not contact TypeSafe; the demo is the live-network check.

Animated macOS demo: `demo/JevDemo` is a native SwiftUI app showing a scripted compaction in a Claude Code-like terminal. It makes no API requests. Build and launch: `demo/JevDemo/build.sh` (opens `demo/JevDemo/build/JevDemo.app`; Space restarts playback).

## 3. Repository facts

Root folders: `.claude-plugin`, `demo/JevDemo`, `examples`, `hooks`, `src`, `tests`, `types`. Root files: `.gitignore`, `LICENSE`, `README.md`, `package-lock.json`, `package.json`, `tsconfig.hooks.json`, `tsconfig.json`. License: MIT (contents not shown). Language breakdown: not shown. Tags, releases and latest commit date: not shown. Branch shown: `main`. Commit count shown: 30.

## 4. Claims and measurements

- Advertised goal: avoid lossy summaries while removing stale tool material and keeping retained content word for word. The introduction says every tool call and result is scored in one fast request; the detailed procedure allows several concurrent requests when batching is needed.
- The 0.25 reduction check is an illustrative fallback, not a measured result. The 25,000, 30,000 and 32,000 token figures are budgets and limits, not measured savings.
- No numbers are shown for latency, throughput, token savings, accuracy or comparison with other methods. The animation is scripted, not live evidence.
- Limits stated by the README: only tool calls and results can be deleted; prose is never removed or shortened (shortening only applies to what Jev receives); token counts are estimates; a probability does not prove a deletion is safe (re-running a tool is the recovery); near the state limit one request per small group of questions may be needed.

## 5. External services and credentials

- TypeSafe Jev / System One API, endpoint `https://api.typesafe.ai/v1/systemone`, default model `jev-latest`, credential `TYPESAFE_API_KEY`. Each request carries the fitted conversation representation (user and assistant prose, tool inputs, placeholders for tool outputs) off the machine.
- GitHub (repository and plugin marketplace source `tamaratran/fast-jev-compaction`) and npm (library); no credential shown for either.
- Claude Code with `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS` for the plugin.
