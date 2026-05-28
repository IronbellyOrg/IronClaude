# Research: Native conversation storage formats of mainstream AI coding tools

**Investigation type:** Pattern Investigator
**Scope:** Cursor, Claude Code, Aider, Continue.dev, Cline, Roo Code, Copilot CLI, Gemini CLI, Codex CLI
**Status:** Complete
**Date:** 2026-05-01

---

## Claude Code (Anthropic CLI)

- **Source:** github.com/anthropics/claude-code; local ground-truth `/config/.claude/projects/` (sampled `46021a18-...jsonl`, `56bae2f8-...jsonl`)
- **Storage path on disk:** `~/.claude/projects/<slugified-cwd>/<sessionId>.jsonl`. The slug is the absolute cwd with `/` replaced by `-` (e.g., `/config/workspace/IronClaude` -> `-config-workspace-IronClaude`). Each session is a single JSONL file named after a UUID `sessionId`. Some sessions also have a sibling directory of the same UUID (used for sidecar artifacts/checkpoints). Adjacent sibling stores: `~/.claude/todos/`, `~/.claude/shell-snapshots/`, `~/.claude/file-history/`, `~/.claude/sessions/`, `~/.claude/plans/`, `~/.claude/telemetry/`, `~/.claude/history.jsonl` (top-level cross-session prompt history).
- **File format:** JSON Lines (newline-delimited JSON). One event per line, append-only.
- **Schema fields (observed in real transcripts):**
  - Common: `type` (one of `user` | `assistant` | `queue-operation` | `system` | others), `uuid`, `parentUuid`, `timestamp` (ISO8601 UTC), `sessionId`, `cwd`, `gitBranch`, `version` (Claude Code build, e.g. `2.1.121`), `userType` (`external`), `entrypoint` (`cli` | `sdk-cli`), `permissionMode` (e.g., `bypassPermissions`), `isSidechain` (boolean — marks sub-agent threads), `promptId`.
  - User entries: `message.role: "user"`, `message.content` (string OR an array containing `tool_result` blocks with `tool_use_id`).
  - Assistant entries: `message.model` (e.g., `claude-opus-4-7`), `message.id` (Anthropic msg id), `message.role: "assistant"`, `message.content` (array of typed blocks: `thinking` (with encrypted `signature`), `text`, `tool_use` with `name`+`input`), `stop_reason` (`tool_use`/`end_turn`), full Anthropic `usage` block (`input_tokens`, `output_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens`, `service_tier`, ephemeral cache breakdown, per-iteration usage), plus `attributionSkill` and `attributionPlugin` (e.g. `sc:explain`, `sc`).
  - Tool results: appear as user-role entries whose `message.content` array contains `{type: "tool_result", tool_use_id, content}` items.
  - Internal control: `queue-operation` entries (`enqueue`/`dequeue`) interleaved with the conversation.
- **What is captured:** full prompt text, full assistant output (incl. thinking), every tool call name + arguments + result, model id, token usage with cache breakdown, timestamps, working directory, git branch at time of message, session lineage via `parentUuid`, sub-agent threads via `isSidechain`, skill/plugin attribution.
- **What is missing:** No structured diff capture for file edits (Edit tool input/output is stored verbatim as strings, not as a parsed unified diff); no embeddings; no team/user identity beyond local OS user; no commit SHA (only branch); no project-level metadata file (project dir contains only the JSONL files).
- **Per-machine vs. synced:** Local-only. There is no first-party sync. (Anthropic's hosted `claude.ai/projects` is a separate product and does not ingest these JSONL files.)
- **Team aggregation OOB:** No. Each developer's `~/.claude/projects/` is private to their machine. Third-party tools (e.g., `ccusage`, SpecStory) read these files post-hoc.
- **Verification tag:** [CODE-VERIFIED at /config/.claude/projects/-config-workspace-IronClaude/46021a18-d859-4696-aed8-79e7727aba42.jsonl and 56bae2f8-...jsonl]
- **Notes:** Format is undocumented and has evolved across versions; samples here come from versions 2.1.121 and 2.1.126. The presence of `attributionSkill`/`attributionPlugin` and the `iterations` array in `usage` is recent. The JSONL is unusually rich compared to peers — it is effectively a complete replay log of the agent loop, not just a conversation transcript.

## Cursor IDE

- **Source:** Cursor community forum (cursor.fan tutorial, forum.cursor.com), Stack Overflow.
- **Storage path on disk:**
  - macOS: `~/Library/Application Support/Cursor/User/workspaceStorage/<workspaceHash>/state.vscdb` and `~/Library/Application Support/Cursor/User/globalStorage/state.vscdb`
  - Linux: `~/.config/Cursor/User/workspaceStorage/<workspaceHash>/state.vscdb`
  - Windows: `%APPDATA%\Cursor\User\workspaceStorage\<workspaceHash>\state.vscdb`
- **File format:** SQLite (single file per workspace), inheriting VS Code's storage scheme.
- **Schema fields:** Single key/value table `ItemTable` with columns `rowid`, `key`, `value` (BLOB). Conversation data is JSON serialized into `value` under specific keys, primarily:
  - `aiService.prompts` — the prompt history.
  - `workbench.panel.aichat.view.aichat.chatdata` — the rich chat panel state (messages, tool calls, file context refs, model selection).
  - Composer/Agent sessions may also use `composer.composerData` and additional keys depending on Cursor version.
- **What is captured:** prompts, responses, message threads, attached file context, agent/composer turns. Tool-call structure and code-edit deltas are embedded inside the chat-panel JSON blob.
- **What is missing:** No first-class diff capture (edits are reconstructed from message blocks); no normalized schema across keys; key/value blobs are version-coupled and undocumented; cross-workspace querying requires merging multiple `state.vscdb` files; cloud sync of chats is not built in (per docs at time of writing).
- **Per-machine vs. synced:** Local-only at the file level. Cursor's cloud has chat features (e.g., shareable chats, account-bound prompts in newer versions), but the canonical historical store is the per-workspace SQLite. Forum guidance recommends manually copying `state.vscdb` to migrate history.
- **Team aggregation OOB:** No. Pro/Business plans expose usage analytics, but conversation aggregation across a team is not exposed as a downloadable artifact.
- **Verification tag:** [DOC-ONLY] (no Cursor install on this host to query SQLite directly)
- **Notes:** Because everything is stuffed into a few JSON blobs in a generic key/value table, ingestion requires custom JSON-path extraction per Cursor version. Schema breakage between Cursor releases is reported on the forum.

## Aider

- **Source:** github.com/Aider-AI/aider; docs at aider.chat/docs/config/options.html and aider.chat/docs/faq.html.
- **Storage path on disk:** Project-relative by default (the cwd / git root), three sibling files:
  - `.aider.chat.history.md` — full chat transcript (markdown)
  - `.aider.input.history` — readline-style raw user input log
  - `.aider.llm.history` — raw LLM API request/response log (only when `--llm-history-file` is set)
  Locations are configurable via `--chat-history-file`, `--input-history-file`, `--llm-history-file`. Files are typically `.gitignore`'d.
- **File format:** Markdown (chat history), plain-text (input history), plain-text/JSON-ish (llm history — request/response blocks).
- **Schema fields (transcript-style, not a strict schema):**
  - Session header: `# aider chat started at <timestamp>`
  - Startup metadata blockquoted lines: aider version, model name(s), repo map info, command-line invocation
  - User prompts as `#### ` markdown headings
  - Assistant responses as plain markdown body
  - SEARCH/REPLACE edit blocks (Aider's edit format) inline in the assistant body
  - Operational events: token/cost summaries, `Applied edit to <file>`, commit messages and SHAs, `^C` interrupts, exception tracebacks, `/add`/`/drop` slash-command outputs.
- **What is captured:** prompts, responses, edit hunks, applied-edit confirmations, git commit SHAs and messages (Aider auto-commits), token/cost rollups, model name in header.
- **What is missing:** No machine-readable schema (text only — must be parsed); no per-message UUIDs; no structured tool-call objects (Aider treats edits as text in the response); LLM request bodies only present if `--llm-history-file` is enabled.
- **Per-machine vs. synced:** Local-only, project-relative. Often committed-out via .gitignore, but nothing prevents committing them.
- **Team aggregation OOB:** No.
- **Verification tag:** [DOC-ONLY] for schema; format itself is consistently described in official docs and gist samples.
- **Notes:** Of all the tools surveyed, Aider has the most human-friendly transcript and the *least* machine-friendly schema. Git commits Aider creates are themselves a parallel persistence layer (each accepted edit ⇒ a commit), so for diff/edit reconstruction the git log is more reliable than the markdown.

## Continue.dev

- **Source:** docs.continue.dev/development-data and docs.continue.dev/customize/deep-dives/development-data; docs.continue.dev/reference/config.
- **Storage path on disk:** Default `.continue/dev_data/` (project-relative, in the `.continue` config directory). Configurable via `data` block in `config.yaml` — `destination` may be `file://<path>` (writes JSONL there) or an HTTP(S) endpoint (POSTs events). Active Continue session/chat state is also in the IDE-extension globalStorage (similar to Cline).
- **File format:** JSON Lines per event type, one file per event stream; each event tagged with a `schema` version (`0.1.0`, `0.2.0`).
- **Schema fields:** Documented event categories include autocomplete acceptance/rejection, chat interaction, `tokens_generated`, `quickEdit`, plus model/provider metadata. Each event carries `schema`, event-type-specific payload (prompt, completion, accepted bool, latency, model, provider, file path/language for autocomplete, repo/git info where available). Specific field-by-field schema is in source (`@continuedev/config-yaml` types) rather than docs prose.
- **What is captured:** chat turns, completion suggestions and acceptance, token counts, edit interactions, model/provider, language/file context. Continue is unique in surveying both *suggestion telemetry* and *conversation*.
- **What is missing:** No structured diff per edit (edit is captured as before/after spans, not unified diff); chat tool-call schema less rich than Claude Code's; raw responses can be omitted depending on config.
- **Per-machine vs. synced:** Hybrid by design. Local JSONL by default, but the `data` block was explicitly built for shipping events to a team HTTP endpoint (Continue Hub / self-hosted collector).
- **Team aggregation OOB:** Partial — Continue ships the *plumbing* for team aggregation (HTTP destination + schemas) but does not provide a hosted dashboard out of the box; teams typically wire it to their own warehouse or to Continue Hub.
- **Verification tag:** [DOC-ONLY] (path and JSONL shape from docs; field-level schema referenced as living in source).
- **Notes:** This is the most "ingestion-friendly" design of the bunch — JSONL with versioned schemas and a first-class HTTP fan-out — and is the closest peer to what an aggregation system like SpecStory would natively want as input.

## Cline

- **Source:** docs.cline.bot/troubleshooting/task-history-recovery, docs.cline.bot/enterprise-solutions/monitoring/prompt-storage, github.com/cline/cline (extension id `saoudrizwan.claude-dev`).
- **Storage path on disk:** Inside VS Code (or JetBrains) globalStorage for the extension:
  - VS Code macOS: `~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/tasks/<taskId>/`
  - VS Code Linux: `~/.config/Code/User/globalStorage/saoudrizwan.claude-dev/tasks/<taskId>/`
  - VS Code Windows: `%APPDATA%\Code\User\globalStorage\saoudrizwan.claude-dev\tasks\<taskId>\`
  - JetBrains: analogous paths under `JetBrains/<IDE>/globalStorage/saoudrizwan.claude-dev/`
  - Code-Insiders: replace `Code` with `Code - Insiders`.
  - Cline docs also reference an alternative `~/.cline/data/tasks/<taskId>/` location for some configurations.
- **File format:** JSON files per task (one task = one directory of JSON files).
- **Schema fields:** Per-task files documented:
  - `api_conversation_history.json` — full LLM API conversation (system + user + assistant + tool messages, the format the model actually receives). This is the "raw" model-eye-view.
  - `ui_messages.json` — UI-side message records (what the human sees, including streamed tool invocations, approvals, mode changes).
  - `task_metadata.json` — task-level metadata (id, title, timestamps, model, mode, token totals, possibly cwd).
- **What is captured:** prompts, assistant outputs, tool invocations, approvals/denials (Cline is approval-driven), file diffs the agent applied, terminal output it consumed, token/cost.
- **What is missing:** Field-level schema not published in docs (must be reverse-engineered from the JSON or from `cline/cline` source); no built-in cross-task index; no embeddings.
- **Per-machine vs. synced:** Local-only by default. Cline's enterprise tier offers a "Prompt Storage" feature that can stream task data to a self-hosted backend.
- **Team aggregation OOB:** Partial — open-source Cline is local-only; enterprise SKU adds prompt-storage forwarding.
- **Verification tag:** [DOC-ONLY] for paths/file names (corroborated across two official Cline doc pages plus the extension id).
- **Notes:** Cline's split between `api_conversation_history` (machine view) and `ui_messages` (human view) is unusual and useful — the former is what an LLM-replay needs, the latter is what a UX summarizer wants.

## Roo Code

- **Source:** github.com/RooCodeInc/Roo-Code (issues #4174, #3784); zenn.dev write-up.
- **Storage path on disk:** VS Code globalStorage under extension id `rooveterinaryinc.roo-cline`:
  - Linux (incl. remote-server): `~/.vscode-server/data/User/globalStorage/rooveterinaryinc.roo-cline/tasks/<taskId>/`
  - Local VS Code: same pattern but rooted at the platform's User globalStorage (mac `~/Library/Application Support/Code/...`, Win `%APPDATA%\Code\...`).
- **File format:** JSON files per task — Roo Code is a fork of Cline and inherits the same per-task layout.
- **Schema fields:** Same trio as Cline — `api_conversation_history.json`, `ui_messages.json`, plus task metadata files. Roo additionally maintains state in VS Code globalState; issue #3784 discusses migrating more state from globalState pressure into file-based per-task storage.
- **What is captured:** Same as Cline — full API conversation, UI message log, tool calls, approvals, file edits via tool messages.
- **What is missing:** Same gaps as Cline; additionally Roo's docs are sparser than Cline's, so schema details rely on reading source.
- **Per-machine vs. synced:** Local-only.
- **Team aggregation OOB:** No.
- **Verification tag:** [DOC-ONLY] (corroborated by Roo issue tracker referencing the exact paths).
- **Notes:** Because Roo is a Cline fork, an ingestion adapter for Cline will work for Roo with only path / extension-id substitution — they share file names and structure.

## GitHub Copilot CLI

- **Source:** docs.github.com/copilot/concepts/agents/copilot-cli/chronicle, docs.github.com/en/copilot/reference/copilot-cli-reference/cli-config-dir-reference, github.com/github/copilot-cli (the new CLI; old `gh-copilot` deprecated 2025-10-25).
- **Storage path on disk:** `~/.copilot/` (override via `$COPILOT_HOME`). Relevant subpaths:
  - `~/.copilot/session-state/<sessionId>/` — per-session JSONL transcripts ("session files").
  - `~/.copilot/session-store.db` — SQLite index used for `/chronicle`, history Q&A, and resume.
  - `~/.copilot/logs/` — diagnostic logs.
  - Plus configs: `config.json`, `settings.json`, `mcp-config.json`, `permissions-config.json`, `instructions/`, `agents/`, `skills/`, `hooks/`, `installed-plugins/`, `plugin-data/`.
  - Cache root separate: `~/Library/Caches/copilot` (mac), `$XDG_CACHE_HOME/copilot` or `~/.cache/copilot` (linux), `%LOCALAPPDATA%\copilot` (win).
- **File format:** JSONL per session (raw transcript) + SQLite (`session-store.db`) for indexed/queryable structure.
- **Schema fields (per docs):** Each session records prompts, model replies, tools used, file-modification details. Specific column names of `session-store.db` and exact JSONL line shape are not published.
- **What is captured:** prompts, responses, tool invocations, file edits made by the agent; "complete" session record per docs.
- **What is missing:** Public field-level schema; no documented embeddings; explicit timestamps not named in docs (likely present per-line).
- **Per-machine vs. synced:** Local-only and "tied to your user account" per docs. Some content is sent to the model during interactions, but persistence is local.
- **Team aggregation OOB:** No team aggregation of CLI sessions documented. (GitHub does have org-level Copilot usage analytics, but not a sessions feed.)
- **Verification tag:** [DOC-ONLY] (paths and SQLite/JSONL split confirmed in two official GitHub docs pages).
- **Notes:** Copilot CLI is the only mainstream tool here that ships *both* a JSONL replay log *and* a SQLite index out of the box — i.e., an internal version of the architecture an aggregator would build. Reusing or reading `session-store.db` directly would be schema-coupled to Copilot CLI versions.

## Gemini CLI

- **Source:** github.com/google-gemini/gemini-cli (discussions #4974), google-gemini.github.io/gemini-cli/docs, fossies mirror of `chatRecordingService.ts`.
- **Storage path on disk:** Per-project hashed temp directory under `~/.gemini/tmp/<projectHash>/`:
  - `~/.gemini/tmp/<hash>/chats/checkpoint-<name>.json` — explicit `/chat save <name>` snapshots.
  - `~/.gemini/tmp/<hash>/logs.json` — runtime/session interaction log.
  - `~/.gemini/tmp/<hash>/shell_history` — shell command history.
  - `<projectHash>` is a hash of the project root path so each repo gets its own bucket.
- **File format:** JSON (array of message objects); `logs.json` is also JSON.
- **Schema fields:** Checkpoint files are arrays of `{role, parts}` objects (Google's content-parts schema — `role` ∈ `user`/`model`, `parts` is an array including text and tool/function-call parts). `logs.json` records turn/event entries.
- **What is captured:** chat turns including tool/function calls (parts schema supports them), per-project scoping.
- **What is missing:** No published field-by-field schema for `logs.json`; no first-class diff records (edits are tool-call parts whose content the consumer must parse); no global cross-project index.
- **Per-machine vs. synced:** Local-only. There is no built-in cloud sync of CLI chats (separate from Gemini web/app history).
- **Team aggregation OOB:** No.
- **Verification tag:** [DOC-ONLY] (path/format confirmed by two official sources + a source-tree mirror of `chatRecordingService.ts`).
- **Notes:** The hashing scheme means an aggregator must walk all `~/.gemini/tmp/*/` buckets and resolve hashes back to repo paths (Gemini stores the mapping internally; the project-root↔hash mapping can also be rederived).

## OpenAI Codex CLI

- **Source:** github.com/openai/codex (issue #2288, discussion #3827); deepwiki.com/openai/codex sections 3.5.2 (rollouts) and 4.4 (resumption).
- **Storage path on disk:** `$CODEX_HOME/sessions/YYYY/MM/DD/rollout-<timestamp>-<uuid>.jsonl` (default `CODEX_HOME=~/.codex`). Companion files in the same dir tree: `session_index.jsonl` (cross-session index) and a local `state.sqlite` for query/resume metadata.
- **File format:** JSON Lines (rollout log) + SQLite (`state.sqlite`) + JSONL index (`session_index.jsonl`).
- **Schema fields:** Each line is a `RolloutLine = { timestamp (UTC), item: RolloutItem }`. `RolloutItem` variants:
  - `SessionMeta`: `id`, `source`, `cwd`, `provider`, CLI version
  - `TurnContext`: model + policies (sandbox / approval mode)
  - `ResponseItem`: assistant output, includes tool calls and end-of-turn
  - `EventMsg`: user / agent / token / lifecycle events
  - `Compacted`: summary-compaction entries (when context is compressed)
- **What is captured:** Full session meta (model, provider, cwd, sandbox policy), every assistant turn, tool calls, lifecycle events, token counts, compaction snapshots.
- **What is missing:** No dedicated `FileEdit` rollout type — edits ride along inside `ResponseItem` tool-call content (e.g., `apply_patch`); a parser must extract them. No diff normalization.
- **Per-machine vs. synced:** Local-only filesystem persistence. No remote shipping documented.
- **Team aggregation OOB:** No.
- **Verification tag:** [DOC-ONLY] (high confidence — schema item names match Rust types in the open-source repo per the cited deepwiki extraction).
- **Notes:** Codex CLI's design is the closest analogue to Claude Code's: append-only JSONL of structured `RolloutItem`s, with a sibling SQLite for indexing — Codex effectively *adds* what Claude Code lacks (a built-in index file). Both use UUID-named session files under a date hierarchy (Codex `YYYY/MM/DD/`, Claude Code flat by slugified-cwd).

## Cross-Tool Summary Table

| Tool | Storage path | Format | Synced? | Tool calls captured? | Team aggregation OOB? |
|---|---|---|---|---|---|
| Claude Code | `~/.claude/projects/<slug-cwd>/<sessionId>.jsonl` | JSONL (rich) | Local-only | Yes (full `tool_use`/`tool_result` blocks, with thinking + usage) | No |
| Cursor IDE | `…/Cursor/User/workspaceStorage/<hash>/state.vscdb` | SQLite (KV blob) | Local-only (cloud sync not built-in) | Yes, embedded in JSON blob under `aiService.prompts` / `…chatdata` | No |
| Aider | `<project>/.aider.chat.history.md` (+ `.input.history`, `.llm.history`) | Markdown + plaintext | Local-only (project-relative) | No structured tool-calls (text + SEARCH/REPLACE blocks) | No |
| Continue.dev | `.continue/dev_data/*.jsonl` (configurable HTTP destination) | JSONL with versioned `schema` | Hybrid (local + optional HTTP fan-out) | Yes (chat events) | Partial (plumbing yes, dashboard no) |
| Cline | `…/Code/User/globalStorage/saoudrizwan.claude-dev/tasks/<id>/{api_conversation_history,ui_messages,task_metadata}.json` | JSON files | Local-only (enterprise tier adds forwarding) | Yes (split api vs ui views) | Partial (enterprise) |
| Roo Code | `…/Code/User/globalStorage/rooveterinaryinc.roo-cline/tasks/<id>/*.json` | JSON files (Cline-fork layout) | Local-only | Yes (inherited from Cline) | No |
| Copilot CLI | `~/.copilot/session-state/<sessionId>/` (JSONL) + `~/.copilot/session-store.db` (SQLite) | JSONL + SQLite | Local-only | Yes (per docs: prompts, replies, tools used, file mods) | No |
| Gemini CLI | `~/.gemini/tmp/<projectHash>/{chats/checkpoint-*.json,logs.json}` | JSON (role/parts) | Local-only | Yes (function-call parts) | No |
| Codex CLI | `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl` + `state.sqlite` + `session_index.jsonl` | JSONL + SQLite | Local-only | Yes (`ResponseItem.tool_calls`, plus typed `RolloutItem` variants) | No |

## Key Takeaways

- **JSONL is the de-facto wire format** for agentic CLIs (Claude Code, Codex CLI, Copilot CLI, Continue.dev). Markdown (Aider) and SQLite-blob (Cursor) are the outliers.
- **All nine tools persist locally by default. None of them ship a built-in team aggregator.** Continue.dev is the only one whose schema/transport (`data:` block + HTTP destination) was explicitly designed to be re-emitted; Cline-enterprise and Copilot CLI get partway there but don't expose it as a feature.
- **Tool calls are universally captured but never normalized.** Each tool encodes its tool-call schema differently: Anthropic content-blocks (Claude Code), Google content-parts (Gemini CLI), OpenAI `RolloutItem.ResponseItem` (Codex), free-form JSON in a SQLite blob (Cursor), or SEARCH/REPLACE text (Aider). A unified RAG store must adapt N codecs → 1 schema.
- **File edits are almost never first-class.** Only Cline distinguishes "what the model saw" (`api_conversation_history`) from "what the user saw" (`ui_messages`). Diffs are typically reconstructible only by parsing tool-call payloads (apply_patch, write_to_file, str_replace_editor, SEARCH/REPLACE) — i.e., per-tool adapters required.
- **Index/replay split is emerging.** Codex CLI and Copilot CLI both ship JSONL-plus-SQLite. Claude Code ships only JSONL (no first-party index), which is precisely the gap a SpecStory-style aggregator fills.
- **Per-project hashing is common but inconsistent** — Cursor uses opaque `workspaceHash`, Gemini uses `projectHash`, Claude Code uses slugified cwd, Aider keeps files in the project itself, Cline/Roo group by VS Code extension globalStorage and tag tasks by UUID. Mapping all of these back to a canonical repo identity is itself a non-trivial ingestion concern.

## Gaps and Questions

- **Cursor `state.vscdb` schema** [UNVERIFIED]: exact JSON shape of `aiService.prompts` and `workbench.panel.aichat.view.aichat.chatdata` blobs differs across Cursor releases; need an empirical dump from a current Cursor install to lock the schema for an ingester.
- **Cline / Roo per-file fields** [UNVERIFIED]: docs name the three files but don't publish their JSON keys; needs source inspection of `cline/cline` / `RooCodeInc/Roo-Code` to enumerate fields.
- **Gemini CLI `logs.json` schema** [UNVERIFIED]: `chatRecordingService.ts` is the source of truth — schema not in user docs.
- **Copilot CLI `session-store.db` table layout** [UNVERIFIED]: not published; would require runtime inspection.
- **Continue.dev event-type catalog** [UNVERIFIED at field-level]: docs name categories (autocomplete/chat/tokens_generated/quickEdit) but the per-event field list is in `@continuedev/config-yaml` types in the source repo, not in user-facing docs.
- **Aider `.aider.llm.history` exact format** [UNVERIFIED]: text/JSON-ish with model request/response blocks, but no formal schema in docs.
- **Codex CLI `state.sqlite` columns** [UNVERIFIED]: deepwiki references its existence; the Rust source defines the actual schema.
- **Claude Code sidecar dirs** [PARTIAL]: same-UUID directories adjacent to JSONL transcripts contain checkpoint/snapshot artifacts whose format is not documented; sampling here only covered the JSONL.

## Stale Documentation Found

- **Aider docs** describe `.aider.chat.history.md` as "the chat history file" but do not warn that it is the *only* machine-readable artifact unless `--llm-history-file` is set — i.e., if a user wants a structured replay they must opt in. This is easy to miss in docs.
- **Cursor community guidance** still recommends manually copying `state.vscdb` between machines despite the product moving toward account-bound chat in newer versions; older forum threads contradict newer Cursor behavior.
- **GitHub `gh-copilot`** (the older extension on github.com/github/gh-copilot) was deprecated 2025-10-25 in favor of the standalone `copilot-cli` (github.com/github/copilot-cli) with a completely different on-disk layout (`~/.copilot/`). Older blog posts that point at `gh-copilot` paths are stale.
- **Roo Code docs** are sparse on storage and mostly inherit from Cline; the Roo issue tracker (#3784, #4174) is more current than the docs site.
- **Continue.dev docs** for `dev_data` document the *destination* configuration but defer field schemas to source — this is by design but means doc-only readers will not see the actual event keys.

## Summary

Every mainstream AI coding tool persists conversations *locally and in its own format*: Claude Code and Codex CLI use rich JSONL; Copilot CLI pairs JSONL with a SQLite index; Cursor stuffs blobs into VS Code's `state.vscdb`; Cline and Roo Code split per-task into 2–3 JSON files in extension globalStorage; Gemini CLI uses per-project-hash JSON files; Continue.dev emits versioned-schema JSONL designed for fan-out; Aider writes a human-readable Markdown transcript. None ships team aggregation out of the box — Continue.dev gets closest by exposing an HTTP destination, and Cline-enterprise/Copilot-CLI offer partial introspection. Tool calls and file edits are captured everywhere but normalized nowhere, so any unified-context system must absorb 9 codecs into 1 schema, walk per-tool path conventions (some hashed, some slugified, some workspace-scoped), and synthesize diffs by parsing tool-call payloads since only Cline distinguishes machine-view from user-view conversation logs.

**Status:** Complete
