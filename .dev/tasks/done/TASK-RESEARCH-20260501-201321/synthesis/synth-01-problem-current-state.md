# Synthesis: Problem Statement + Current State Analysis

**Source files:** research-notes.md, 01-native-storage-formats.md, web-01-specstory-deep-dive.md
**Target sections:** 1 (Problem Statement), 2 (Current State Analysis)
**Date:** 2026-05-01

---

## 1. Problem Statement

### 1.1 The question

The user's explicit request, recorded in `research/research-notes.md`:

> "Find as many comparables to https://github.com/specstoryai/getspecstory as possible … to inform a build/buy/adopt decision for a system that unifies the context of all agent conversations from all engineers into a single database that can be efficiently indexed, searched, and used as context for future conversations."

In short: **unify every engineer's AI-coding-agent conversations into one indexed, searchable, RAG-capable team-wide store.**

### 1.2 Why it matters

The user's framing in `research-notes.md` and the SpecStory positioning summarized in `web-01-specstory-deep-dive.md` align on three motivations:

| Driver | Description (paraphrased from sources) |
|---|---|
| Engineering productivity | Reuse prior solved problems instead of re-prompting from scratch; "faster onboarding" via shared past chats (web-01, landing copy). |
| Knowledge retention | Conversations carry the *intent* behind code changes — "Intent is the new source code" (web-01). Without capture, that intent evaporates when the chat closes. |
| Cross-team learning | Each engineer's discoveries are siloed on their machine today; "Share context with teammates … review with decision rationale" (web-01, landing). |

### 1.3 Trigger

Per `research-notes.md` and SpecStory's own product framing in `web-01-specstory-deep-dive.md`:

- Conversation context is **lost across projects** because every tool persists only locally and per-machine (see Section 2 below).
- **Cross-project search is weak-to-absent**: each tool's storage is per-workspace or per-project-hash, with no built-in cross-corpus index.
- **Knowledge sharing does not scale** beyond ad-hoc "paste the chat into Slack" — none of the tools surveyed ships team aggregation by default.

### 1.4 Constraints (user-stated requirements)

| Requirement | Source | Implication |
|---|---|---|
| **RAG capability** — captured history must be usable as context for future conversations | `research-notes.md` line 16-17, 35 | Capture-only products (e.g., SpecStory today, per `web-01`) are insufficient. RAG/retrieval-into-prompt is mandatory, not optional. |
| **Team aggregation** — all engineers' conversations into a single database | `research-notes.md` line 14-17 | Single-user products are insufficient. Solution must support multi-engineer ingest. |
| **Efficient indexing & search** | `research-notes.md` line 16-17 | Implies a queryable store (vector + lexical), not just an archive. |

### 1.5 Success criteria preview

A successful solution to this problem will, at minimum:

1. Ingest conversations from each AI coding tool the engineering team actually uses (the tools enumerated in Section 2).
2. Aggregate across engineers into a shared store.
3. Provide indexed lexical + semantic search across the corpus.
4. Re-inject relevant prior context into new prompts (the RAG capability SpecStory itself lists as not-yet-shipped — `web-01`, "Question 9 — RAG roadmap").
5. Survive per-tool schema drift (`web-01` warns "formats differ by tool and can change").

These criteria frame the gap analysis in later synthesis sections.

---

## 2. Current State Analysis

This section documents the as-is baseline: where each mainstream AI coding tool stores its conversation history on disk, in what format, and with what gaps relative to the user's "unified team RAG store" objective. All findings are sourced from `research/01-native-storage-formats.md`. Per Rule 9, only [CODE-VERIFIED] subsections may be presented as firm current architecture; [DOC-ONLY] and [UNVERIFIED] findings are flagged inline.

### 2.1 Claude Code (Anthropic CLI)

**Storage path:** `~/.claude/projects/<slugified-cwd>/<sessionId>.jsonl` | **Format:** JSON Lines (rich, append-only) | **Synced?:** Local-only

Append-only event log per session, named by UUID, with the project slug derived from absolute cwd (`/` -> `-`). Sibling stores at `~/.claude/{todos,shell-snapshots,file-history,sessions,plans,telemetry}/` plus a top-level `~/.claude/history.jsonl` cross-session prompt log.

**What's captured:**
- Full prompt text and assistant output (including `thinking` blocks with encrypted `signature`).
- Every tool call: `tool_use` with `name`+`input` and matching `tool_result` blocks linked by `tool_use_id`.
- Model id (e.g., `claude-opus-4-7`), full Anthropic `usage` (input/output tokens, cache creation/read, ephemeral cache, per-iteration usage).
- Per-event `uuid`, `parentUuid` (lineage), `timestamp` (ISO8601 UTC), `sessionId`, `cwd`, `gitBranch`, `version`.
- Sub-agent threads via `isSidechain`; skill/plugin attribution via `attributionSkill` / `attributionPlugin`.
- Internal control entries: `queue-operation` (enqueue/dequeue) interleaved with conversation.

**What's missing for unified team RAG:**
- No team aggregation (each developer's `~/.claude/projects/` is private to their machine).
- No semantic / vector index.
- No first-party sync (Anthropic's `claude.ai/projects` is a separate product and does not ingest these JSONL files).
- No structured diff for file edits (Edit-tool input/output stored verbatim as strings, not as parsed unified diffs).
- No commit SHA (only `gitBranch`); no team/user identity beyond local OS user.
- Format is undocumented and version-evolving (samples cover 2.1.121 and 2.1.126); recent additions like `attributionSkill` and the per-iteration `usage.iterations` array signal ongoing schema drift.

**Verification:** [CODE-VERIFIED]
**Evidence:** `01-native-storage-formats.md` (Claude Code section; verified at `/config/.claude/projects/-config-workspace-IronClaude/46021a18-...jsonl` and `56bae2f8-...jsonl`).

### 2.2 Cursor IDE

**Storage path:** `…/Cursor/User/workspaceStorage/<workspaceHash>/state.vscdb` (+ `globalStorage/state.vscdb`) | **Format:** SQLite key/value blob (inherits VS Code scheme) | **Synced?:** Local-only at the file level (cloud chat features exist in newer versions but the canonical historical store is per-workspace SQLite)

Per-platform paths:

| OS | Path |
|---|---|
| macOS | `~/Library/Application Support/Cursor/User/workspaceStorage/<workspaceHash>/state.vscdb` |
| Linux | `~/.config/Cursor/User/workspaceStorage/<workspaceHash>/state.vscdb` |
| Windows | `%APPDATA%\Cursor\User\workspaceStorage\<workspaceHash>\state.vscdb` |

Single key/value table `ItemTable` (`rowid`, `key`, `value` BLOB) with conversation JSON serialized into specific keys: `aiService.prompts` (prompt history), `workbench.panel.aichat.view.aichat.chatdata` (chat panel state), and `composer.composerData` for Composer/Agent sessions.

**What's captured:**
- Prompts, responses, message threads, attached file context, agent/composer turns.
- Tool-call structure and code-edit deltas embedded inside chat-panel JSON blob.

**What's missing for unified team RAG:**
- No team aggregation; Pro/Business analytics exist but conversation aggregation is not exposed as a downloadable artifact.
- No semantic / vector index.
- No cross-tool unification.
- No first-class diff capture (edits reconstructed from message blocks).
- No normalized schema across keys; key/value blobs are version-coupled and undocumented.
- Cross-workspace querying requires merging multiple `state.vscdb` files.
- Schema breakage between Cursor releases reported on community forum.

**Verification:** [DOC-ONLY] (no Cursor install available on host to query SQLite directly; sourced from cursor.fan tutorial, forum.cursor.com, Stack Overflow).
**Evidence:** `01-native-storage-formats.md` (Cursor IDE section).

### 2.3 Aider

**Storage path:** project-relative — `<project>/.aider.chat.history.md`, `.aider.input.history`, `.aider.llm.history` | **Format:** Markdown transcript + plain-text input log + plain-text/JSON-ish LLM log (LLM log only when `--llm-history-file` is set) | **Synced?:** Local-only, project-relative (typically `.gitignore`'d)

Locations are configurable via `--chat-history-file`, `--input-history-file`, `--llm-history-file`.

**What's captured:**
- Session header `# aider chat started at <timestamp>`; startup metadata blockquoted (version, model, repo-map info, CLI invocation).
- User prompts as `#### ` markdown headings; assistant responses as plain markdown body.
- SEARCH/REPLACE edit blocks (Aider's edit format) inline in assistant body.
- Operational events: token/cost summaries, `Applied edit to <file>`, **commit messages and SHAs** (Aider auto-commits each accepted edit), `^C` interrupts, exception tracebacks, `/add`/`/drop` outputs.

**What's missing for unified team RAG:**
- No team aggregation.
- No semantic / vector index.
- No cross-tool unification.
- **No machine-readable schema** — text only, must be parsed; no per-message UUIDs.
- No structured tool-call objects (edits are text in the response body).
- LLM request/response bodies absent unless user opts into `--llm-history-file`.

**Verification:** [DOC-ONLY] for schema (format consistently described in official docs and gist samples).
**Evidence:** `01-native-storage-formats.md` (Aider section); aider.chat/docs/config/options.html and faq.html. Note: of all surveyed tools, Aider has the most human-friendly transcript and the *least* machine-friendly schema. The git log of Aider's auto-commits is more reliable for diff reconstruction than the markdown.

### 2.4 Continue.dev

**Storage path:** `.continue/dev_data/*.jsonl` (configurable `data` block in `config.yaml` — `destination` may be `file://<path>` or an HTTP(S) endpoint) | **Format:** JSON Lines per event type, each event tagged with `schema` version (`0.1.0`, `0.2.0`) | **Synced?:** **Hybrid** — local JSONL by default, with first-class HTTP fan-out designed in

Active session/chat state is also in IDE-extension globalStorage (similar pattern to Cline).

**What's captured:**
- Documented event categories: autocomplete acceptance/rejection, chat interaction, `tokens_generated`, `quickEdit`.
- Each event carries `schema`, event-type-specific payload (prompt, completion, accepted bool, latency, model, provider, file path/language for autocomplete, repo/git info where available).
- Continue is unique in surveying both *suggestion telemetry* and *conversation*.

**What's missing for unified team RAG:**
- No team aggregation **dashboard** out of the box (plumbing exists; teams wire to their own warehouse or to Continue Hub).
- No semantic / vector index.
- No cross-tool unification.
- No structured diff per edit (before/after spans, not unified diff).
- Chat tool-call schema less rich than Claude Code's.
- Raw responses can be omitted depending on config.
- Per-event field list lives in `@continuedev/config-yaml` source types, not user-facing docs (`[UNVERIFIED at field-level]`).

**Verification:** [DOC-ONLY] (path and JSONL shape from docs.continue.dev/development-data; field-level schema deferred to source).
**Evidence:** `01-native-storage-formats.md` (Continue.dev section). Notable: this is the most "ingestion-friendly" design surveyed — versioned-schema JSONL + first-class HTTP destination — closest peer to what an aggregator would natively want as input.

### 2.5 Cline

**Storage path:** VS Code (or JetBrains) globalStorage under extension id `saoudrizwan.claude-dev` — `…/Code/User/globalStorage/saoudrizwan.claude-dev/tasks/<taskId>/` | **Format:** JSON files per task (one task = one directory) | **Synced?:** Local-only by default; **enterprise tier** offers "Prompt Storage" stream-to-self-hosted-backend

Per-platform paths:

| Surface | Path |
|---|---|
| VS Code macOS | `~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/tasks/<taskId>/` |
| VS Code Linux | `~/.config/Code/User/globalStorage/saoudrizwan.claude-dev/tasks/<taskId>/` |
| VS Code Windows | `%APPDATA%\Code\User\globalStorage\saoudrizwan.claude-dev\tasks\<taskId>\` |
| JetBrains | `JetBrains/<IDE>/globalStorage/saoudrizwan.claude-dev/` |
| Code-Insiders | replace `Code` with `Code - Insiders` |
| Alt | `~/.cline/data/tasks/<taskId>/` (referenced for some configurations) |

Per-task files:

| File | Content |
|---|---|
| `api_conversation_history.json` | Full LLM API conversation (system + user + assistant + tool messages — the format the model actually receives, the "raw" model-eye-view) |
| `ui_messages.json` | UI-side message records (what the human sees: streamed tool invocations, approvals, mode changes) |
| `task_metadata.json` | Task-level metadata (id, title, timestamps, model, mode, token totals, possibly cwd) |

**What's captured:**
- Prompts, assistant outputs, tool invocations, approvals/denials (Cline is approval-driven).
- File diffs the agent applied; terminal output it consumed; token/cost.

**What's missing for unified team RAG:**
- No team aggregation (OSS); enterprise SKU adds prompt-storage forwarding (partial).
- No semantic / vector index.
- No cross-tool unification.
- Field-level schema not published in docs — must be reverse-engineered from JSON or `cline/cline` source (`[UNVERIFIED]`).
- No built-in cross-task index; no embeddings.

**Verification:** [DOC-ONLY] for paths/file names (corroborated across two official Cline doc pages plus extension id).
**Evidence:** `01-native-storage-formats.md` (Cline section); docs.cline.bot/troubleshooting/task-history-recovery, docs.cline.bot/enterprise-solutions/monitoring/prompt-storage. The split between machine-view (`api_conversation_history`) and human-view (`ui_messages`) is unusual and useful — the former is what an LLM-replay needs, the latter is what a UX summarizer wants.

### 2.6 Roo Code

**Storage path:** VS Code globalStorage under extension id `rooveterinaryinc.roo-cline` — e.g. `~/.vscode-server/data/User/globalStorage/rooveterinaryinc.roo-cline/tasks/<taskId>/` (Linux/remote-server); analogous platform-rooted paths on macOS/Windows | **Format:** JSON files per task (Cline-fork layout: same trio of files) | **Synced?:** Local-only

**What's captured:**
- Same as Cline (Roo is a Cline fork): full API conversation, UI message log, tool calls, approvals, file edits via tool messages.
- Roo additionally maintains state in VS Code globalState; issue #3784 discusses migrating more state out of globalState pressure into file-based per-task storage.

**What's missing for unified team RAG:**
- No team aggregation.
- No semantic / vector index.
- No cross-tool unification.
- Same gaps as Cline; additionally Roo's docs are sparser, so schema details rely on reading source.

**Verification:** [DOC-ONLY] (corroborated by Roo issue tracker referencing the exact paths — issues #4174, #3784).
**Evidence:** `01-native-storage-formats.md` (Roo Code section). Important practical note: an ingestion adapter for Cline will work for Roo with only path / extension-id substitution.

### 2.7 GitHub Copilot CLI

**Storage path:** `~/.copilot/` (override via `$COPILOT_HOME`); per-session JSONL at `~/.copilot/session-state/<sessionId>/`; SQLite index at `~/.copilot/session-store.db` | **Format:** **JSONL + SQLite** (JSONL transcripts plus SQLite index used for `/chronicle`, history Q&A, resume) | **Synced?:** Local-only, "tied to your user account" per docs

Adjacent files: `~/.copilot/logs/`, configs (`config.json`, `settings.json`, `mcp-config.json`, `permissions-config.json`), `instructions/`, `agents/`, `skills/`, `hooks/`, `installed-plugins/`, `plugin-data/`. Cache root is separate — `~/Library/Caches/copilot` (mac), `$XDG_CACHE_HOME/copilot` or `~/.cache/copilot` (linux), `%LOCALAPPDATA%\copilot` (win).

**What's captured (per docs):**
- Each session records prompts, model replies, tools used, file-modification details ("complete" session record).

**What's missing for unified team RAG:**
- No team aggregation of CLI sessions documented (org-level Copilot usage analytics exist, but not a sessions feed).
- No semantic / vector index documented.
- No cross-tool unification.
- Public field-level schema not published; SQLite column layout not documented (`[UNVERIFIED]`).
- Explicit timestamps not named in docs (likely present per-line).

**Verification:** [DOC-ONLY] (paths and JSONL/SQLite split confirmed in two official GitHub docs pages).
**Evidence:** `01-native-storage-formats.md` (Copilot CLI section); docs.github.com/copilot/concepts/agents/copilot-cli/chronicle, docs.github.com/.../cli-config-dir-reference. Of the surveyed tools, Copilot CLI is the only one shipping *both* a JSONL replay log *and* a SQLite index out of the box — i.e., an internal version of the architecture an aggregator would build. Older `gh-copilot` extension was deprecated 2025-10-25 in favor of standalone `copilot-cli` with a completely different on-disk layout.

### 2.8 Gemini CLI

**Storage path:** `~/.gemini/tmp/<projectHash>/` per-project hashed temp directory: `chats/checkpoint-<name>.json` (explicit `/chat save` snapshots), `logs.json` (runtime/session log), `shell_history` | **Format:** JSON (array of `{role, parts}` objects per Google content-parts schema) | **Synced?:** Local-only (no built-in cloud sync of CLI chats; separate from Gemini web/app history)

`<projectHash>` is a hash of the project root path so each repo gets its own bucket.

**What's captured:**
- Chat turns including tool/function calls (parts schema supports text and tool/function-call parts).
- Per-project scoping.

**What's missing for unified team RAG:**
- No team aggregation.
- No semantic / vector index.
- No cross-tool unification.
- No published field-by-field schema for `logs.json` (`[UNVERIFIED]` — `chatRecordingService.ts` is source of truth).
- No first-class diff records (edits are tool-call parts whose content the consumer must parse).
- No global cross-project index — aggregator must walk all `~/.gemini/tmp/*/` buckets and resolve hashes back to repo paths.

**Verification:** [DOC-ONLY] (path/format confirmed by two official sources + a source-tree mirror of `chatRecordingService.ts`).
**Evidence:** `01-native-storage-formats.md` (Gemini CLI section); github.com/google-gemini/gemini-cli discussion #4974, google-gemini.github.io/gemini-cli/docs.

### 2.9 OpenAI Codex CLI

**Storage path:** `$CODEX_HOME/sessions/YYYY/MM/DD/rollout-<timestamp>-<uuid>.jsonl` (default `CODEX_HOME=~/.codex`); companions `session_index.jsonl` (cross-session index) and `state.sqlite` (query/resume metadata) | **Format:** **JSONL + SQLite + JSONL index** | **Synced?:** Local-only filesystem; no remote shipping documented

Each line is `RolloutLine = { timestamp (UTC), item: RolloutItem }` with typed `RolloutItem` variants:

| Variant | Payload |
|---|---|
| `SessionMeta` | `id`, `source`, `cwd`, `provider`, CLI version |
| `TurnContext` | model + policies (sandbox / approval mode) |
| `ResponseItem` | assistant output, includes tool calls and end-of-turn |
| `EventMsg` | user / agent / token / lifecycle events |
| `Compacted` | summary-compaction entries (when context is compressed) |

**What's captured:**
- Full session meta (model, provider, cwd, sandbox policy).
- Every assistant turn, tool calls, lifecycle events, token counts, compaction snapshots.

**What's missing for unified team RAG:**
- No team aggregation.
- No semantic / vector index (the local SQLite is for resume/query metadata, not embeddings).
- No cross-tool unification.
- No dedicated `FileEdit` rollout type — edits ride along inside `ResponseItem` tool-call content (e.g., `apply_patch`); a parser must extract them. No diff normalization.
- `state.sqlite` column layout not published (`[UNVERIFIED]` — defined in Rust source).

**Verification:** [DOC-ONLY] (high confidence — schema item names match Rust types in the open-source repo per cited deepwiki extraction).
**Evidence:** `01-native-storage-formats.md` (OpenAI Codex CLI section); github.com/openai/codex issue #2288 / discussion #3827; deepwiki sections 3.5.2 and 4.4. Codex CLI's design is the closest analogue to Claude Code's — append-only JSONL of structured items — but Codex *adds* the built-in index file Claude Code lacks.

### 2.10 Current State Summary

#### 2.10.1 Cross-tool comparison

| Tool | Storage path | Format | Synced? | Tool calls captured? | Team agg OOB? |
|---|---|---|---|---|---|
| Claude Code | `~/.claude/projects/<slug-cwd>/<sessionId>.jsonl` | JSONL (rich) | Local-only | Yes (full `tool_use`/`tool_result` blocks, with thinking + usage) | No |
| Cursor IDE | `…/Cursor/User/workspaceStorage/<hash>/state.vscdb` | SQLite (KV blob) | Local-only (cloud sync not built-in) | Yes, embedded in JSON blob under `aiService.prompts` / `…chatdata` | No |
| Aider | `<project>/.aider.chat.history.md` (+ `.input.history`, `.llm.history`) | Markdown + plaintext | Local-only (project-relative) | No structured tool-calls (text + SEARCH/REPLACE blocks) | No |
| Continue.dev | `.continue/dev_data/*.jsonl` (configurable HTTP destination) | JSONL with versioned `schema` | **Hybrid** (local + optional HTTP fan-out) | Yes (chat events) | Partial (plumbing yes, dashboard no) |
| Cline | `…/Code/.../saoudrizwan.claude-dev/tasks/<id>/{api_conversation_history,ui_messages,task_metadata}.json` | JSON files | Local-only (enterprise tier adds forwarding) | Yes (split api vs ui views) | Partial (enterprise) |
| Roo Code | `…/Code/.../rooveterinaryinc.roo-cline/tasks/<id>/*.json` | JSON files (Cline-fork layout) | Local-only | Yes (inherited from Cline) | No |
| Copilot CLI | `~/.copilot/session-state/<sessionId>/` (JSONL) + `~/.copilot/session-store.db` (SQLite) | JSONL + SQLite | Local-only | Yes (per docs: prompts, replies, tools used, file mods) | No |
| Gemini CLI | `~/.gemini/tmp/<projectHash>/{chats/checkpoint-*.json,logs.json}` | JSON (role/parts) | Local-only | Yes (function-call parts) | No |
| Codex CLI | `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl` + `state.sqlite` + `session_index.jsonl` | JSONL + SQLite | Local-only | Yes (`ResponseItem.tool_calls`, plus typed `RolloutItem` variants) | No |

#### 2.10.2 Key gaps motivating the rest of the report

- **Universal local-only persistence.** All nine tools persist conversations locally by default; **none ships a built-in team aggregator.** Continue.dev gets closest by exposing an HTTP destination, and Cline-enterprise / Copilot-CLI offer partial introspection — but none is a finished team store.
- **Tool calls captured everywhere, normalized nowhere.** Each tool encodes its tool-call schema differently — Anthropic content-blocks (Claude Code), Google content-parts (Gemini), OpenAI `RolloutItem.ResponseItem` (Codex), free-form JSON in a SQLite blob (Cursor), SEARCH/REPLACE text (Aider). A unified RAG store must adapt **N codecs into 1 schema**.
- **File edits are almost never first-class.** Only Cline distinguishes "what the model saw" (`api_conversation_history`) from "what the user saw" (`ui_messages`). Diffs are typically reconstructible only by parsing tool-call payloads (`apply_patch`, `write_to_file`, `str_replace_editor`, SEARCH/REPLACE) — i.e., per-tool adapters required.
- **Per-project identity is inconsistent.** Cursor uses opaque `workspaceHash`, Gemini uses `projectHash`, Claude Code uses slugified cwd, Aider keeps files in the project itself, Cline/Roo group by VS Code extension globalStorage and tag tasks by UUID. **Mapping all of these back to a canonical repo identity is itself a non-trivial ingestion concern.**
- **Index/replay split is emerging but partial.** Codex CLI and Copilot CLI ship JSONL-plus-SQLite. Claude Code ships only JSONL (no first-party index). No tool ships a *semantic* (vector) index — that gap is precisely what a SpecStory-style aggregator (or a build-your-own RAG stack) is meant to fill.

#### 2.10.3 As-is fragmentation (ASCII diagram)

```
                             AS-IS: per-engineer, per-machine silos
                             (no team store; no cross-tool index)

  Engineer A's laptop                  Engineer B's laptop                  Engineer C's laptop
  +-------------------+                +-------------------+                +-------------------+
  |  Claude Code      |                |  Cursor IDE       |                |  Aider            |
  |  ~/.claude/       |                |  …/workspaceStor- |                |  <project>/       |
  |   projects/       |                |   age/<hash>/     |                |   .aider.chat.    |
  |   <slug>/*.jsonl  |                |   state.vscdb     |                |   history.md      |
  +-------------------+                +-------------------+                +-------------------+
  +-------------------+                +-------------------+                +-------------------+
  |  Codex CLI        |                |  Cline / Roo      |                |  Continue.dev     |
  |  ~/.codex/        |                |  …/globalStorage/ |                |  .continue/       |
  |   sessions/       |                |   <ext-id>/tasks/ |                |   dev_data/       |
  |   rollout*.jsonl  |                |   <id>/*.json     |                |   *.jsonl         |
  |   + state.sqlite  |                +-------------------+                |   (HTTP optional) |
  +-------------------+                +-------------------+                +-------------------+
  +-------------------+                |  Copilot CLI      |                +-------------------+
  |  Gemini CLI       |                |  ~/.copilot/      |                |  …               |
  |  ~/.gemini/tmp/   |                |   session-state/  |                +-------------------+
  |   <projHash>/...  |                |   + session-      |
  +-------------------+                |    store.db       |
                                       +-------------------+

           (No arrows. No shared store. No cross-engineer search. No RAG.)

  Each silo:  - private to one machine
              - private to one tool
              - format-specific (JSONL / SQLite-blob / Markdown / per-task JSON / JSON role-parts)
              - per-project identifier scheme is tool-specific (slug / hash / project-relative / UUID-task)
              - tool calls captured but in N incompatible codecs
              - no semantic index; no embeddings; no team aggregation OOB
```

This fragmentation is the baseline that any unified-context solution — built, bought, or adopted — must overcome. Sections 3+ (Target State, Gap Analysis, External Findings, Options, Recommendation) develop the response.
