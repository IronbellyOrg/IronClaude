# Technical Research Report: SpecStory Comparables for Unified Agent Conversation Context

**Date:** 2026-05-01
**Depth:** Deep
**Research files:** 1 codebase (native storage formats) + 8 web research (comparables landscape)
**Scope:** SpecStory and the broader landscape of tools for unifying engineer-AI agent conversation context (capture, storage, search, RAG, team aggregation)
**Status:** Final

---

## Table of Contents

1. [Problem Statement](#1-problem-statement)
2. [Current State Analysis](#2-current-state-analysis)
3. [Target State](#3-target-state)
4. [Gap Analysis](#4-gap-analysis)
5. [External Research Findings](#5-external-research-findings)
6. [Options Analysis](#6-options-analysis)
7. [Recommendation](#7-recommendation)
8. [Implementation Plan](#8-implementation-plan)
9. [Open Questions](#9-open-questions)
10. [Evidence Trail](#10-evidence-trail)

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

---

## 3. Target State

### 3.1 Desired Behavior

The unified store ingests, normalizes, indexes, and re-injects engineer-AI conversation context across the team's full toolchain. Concretely:

| Dimension | Target |
|---|---|
| Ingestion sources (N tools) | At minimum the 9 mainstream AI coding tools whose native storage was investigated: **Claude Code** (`~/.claude/projects/<slug>/<sessionId>.jsonl`), **Cursor IDE** (`…/Cursor/User/workspaceStorage/<hash>/state.vscdb`), **Aider** (`<project>/.aider.chat.history.md`), **Continue.dev** (`.continue/dev_data/*.jsonl` + optional HTTP destination), **Cline** (`…/globalStorage/saoudrizwan.claude-dev/tasks/<id>/{api_conversation_history,ui_messages,task_metadata}.json`), **Roo Code** (`…/globalStorage/rooveterinaryinc.roo-cline/tasks/<id>/*.json`), **Copilot CLI** (`~/.copilot/session-state/<sessionId>/` + `~/.copilot/session-store.db`), **Gemini CLI** (`~/.gemini/tmp/<projectHash>/{chats/checkpoint-*.json,logs.json}`), **Codex CLI** (`~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl` + `state.sqlite` + `session_index.jsonl`). Source: `01-native-storage-formats.md`. |
| Normalized schema | One canonical schema absorbing the **9 codecs** documented in `01-native-storage-formats.md`: Anthropic content-blocks, Google content-parts, OpenAI `RolloutItem.ResponseItem`, free-form JSON-in-SQLite (Cursor), Markdown + SEARCH/REPLACE (Aider), Cline-style split (`api_conversation_history` machine-view vs `ui_messages` user-view), Continue versioned-schema events. Schema must preserve: prompt text, full assistant output (incl. thinking blocks where present), structured tool-call name + arguments + result, model id, token usage with cache breakdown, timestamps, working directory, git branch/SHA, session lineage (`parentUuid`/sub-agent threads), engineer identity. |
| Indexed lexical search | Full-text over prompts, responses, tool calls, file paths. Comparable to Langfuse / LibreChat MeiliSearch / Onyx Vespa BM25 / pgvector tsvector. Source: `web-04`, `web-05`. |
| Indexed semantic search | Vector retrieval with hybrid (sparse + dense) ranking. Comparable to SpecStory Cloud's "hybrid lexical + semantic" (web-01), Helicone Pro semantic, Phoenix vector search, Braintrust BTQL + semantic, Glean permission-aware hybrid. Source: `web-01`, `web-04`, `web-06`. |
| RAG retrieval into next prompt | Captured history retrievable into the next agent prompt — the explicit capability SpecStory lists as "RAG coming soon" but does not ship today (web-01). Comparable shipping models: Mem0 `memory.add(messages)` + retrieve, Graphiti `add_episode_bulk` + temporal-graph retrieve, Zep messages.add + graph search, SuperMemory MCP for Cursor/Claude Code/VSCode, Onyx ingestion API + ACL-aware Vespa retrieve. Source: `web-03`, `web-05`. |
| Team-wide aggregation | Multi-engineer corpus: cross-machine sync, single team store. Today **none of the 9 native tools ships team aggregation OOB** (`01-native-storage-formats.md`); SpecStory Cloud is single-user-workspace today with team collaboration on roadmap (web-01). |
| RBAC | Per-user / per-group / per-project access control with permission-aware retrieval (so engineer A's retrieval cannot leak engineer B's customer-bearing transcripts). Comparable models: Glean per-doc ACLs at push time (web-06), Onyx ACL inheritance from source connectors (web-05), Langfuse EE project-level RBAC (web-04), Confluence space-page-group permissions (web-06), Slack channel-membership ACLs (web-06). |
| Cross-tool conversation linking | Recognise that one engineer's task may span Claude Code + Cursor + Aider — link by repo identity, time window, and file-path overlap. No surveyed tool does this today; mapping per-tool path conventions back to a canonical repo identity is a documented ingestion concern (`01-native-storage-formats.md` "Per-project hashing is common but inconsistent"). |
| File-edit fidelity | Diffs reconstructible from tool-call payloads (`apply_patch`, `write_to_file`, `str_replace_editor`, SEARCH/REPLACE). Per-tool adapters required because **only Cline distinguishes machine-view from user-view conversation logs** (`01-native-storage-formats.md`). |

ASCII context flow:

```
+------------------+   +---------------+   +------------------+   +---------------+
| AI tools (9):    |   | Per-tool      |   | Normalized       |   | Index:        |
|  Claude Code     |-->| adapters      |-->| schema           |-->|  lexical+     |
|  Cursor          |   | (read native  |   | (one event       |   |  semantic     |
|  Aider           |   | path/format)  |   | shape, tool      |   |  + ACL        |
|  Continue        |   |               |   | calls preserved) |   +-------+-------+
|  Cline / Roo     |   +---------------+   +------------------+           |
|  Copilot CLI     |                                                      v
|  Gemini CLI      |                                            +-------------------+
|  Codex CLI       |                                            | Retrieval API     |
+------------------+                                            | (RAG into prompt) |
                                                                +---------+---------+
                                                                          |
                                                                          v
                                                                +-------------------+
                                                                | Team UI / MCP /   |
                                                                | next-prompt inject|
                                                                +-------------------+
```

### 3.2 Success Criteria (Measurable)

| ID | Criterion | Measurement | Source / Comparable |
|---|---|---|---|
| SC-1 | Engineer can search across the team's last 12 months of AI conversations in <2 s p95 | Latency benchmark on 500k-chunk corpus (the modelled 10-engineer-team workload in web-07) | `web-07` cost model: 10 engineers × 50 conv/wk × 50 msg × 200 tok ≈ 50M tokens/yr → ~500k chunks/yr. Comparable latency: Turbopuffer warm p50 ~8 ms / cold p90 ~444 ms (1M vecs); Qdrant Rust-native sub-100 ms typical (`web-07`). |
| SC-2 | Cross-tool ingestion fidelity ≥ 95% of source events captured into normalized schema | Per-tool adapter conformance test: replay JSONL/SQLite/JSON/Markdown source → count events lost or malformed | `01-native-storage-formats.md` documents 9 native formats; SpecStory's lossy-by-default conversion ("formats differ by tool and can change") sets the floor that the target must beat (`web-01`). |
| SC-3 | Tool-call structure preserved end-to-end | Round-trip test: tool_call_id linkage between caller and result preserved through chunk → embed → retrieve | `web-07`: "naive 512-token chunkers shred tool-call/tool-result pairs"; LlamaIndex `ChatStore` and Haystack `ChatMessage` are the only pipeline tools with first-class preservation. |
| SC-4 | RAG retrieval increases recall on related-prior-decisions queries by Nx vs. lexical-only baseline | Golden-set eval (e.g., 50 queries with known prior decisions) measured at recall@10 | Comparable: Voyage voyage-code-3 reports +13.8% to +16.3% over OpenAI text-embedding-3-large on 32 code-retrieval datasets (web-07). Specific N target to be set in Implementation Plan. |
| SC-5 | Team aggregation query coverage = 100% of opted-in engineers, 0% of opted-out | Audit: ingestion log shows N engineers; RBAC test confirms exclusion | `web-01` (SpecStory single-user today, team roadmap-only); `web-06` Glean permission-aware hybrid is the reference enterprise pattern. |
| SC-6 | Onboarding-time reduction (new engineer time-to-first-merged-PR) | Measure cohort onboarded with RAG-over-team-chat vs. cohort without | Hypothesis-driven (no benchmark in research files). To be set during Implementation Plan. |
| SC-7 | Capture overhead does not require routing live LLM calls through the store | Adapter test: works on quiescent disk artifacts only | All major memory-layer products surveyed (Mem0, Graphiti, Zep, Cognee, SuperMemory) accept arbitrary message arrays via `add()` API and **do not require LLM-call routing** (`web-03` Key Findings). Confirms criterion is achievable. |
| SC-8 | RBAC enforcement at retrieval time (not only at ingestion time) | Permission-aware search test: revoking access removes results within < 60 s | Comparable: Glean permission-aware ranking, Onyx ACL inheritance (`web-05`, `web-06`). |
| SC-9 | Operates on captured-archive ingestion, not LLM-call interception | Architecture review: no proxy-mode dependency | Helicone proxy-mode is fastest forward-capture but cannot ingest historical archives (`web-04`); the target must work on existing `~/.claude/projects/` etc. |

### 3.3 Constraints

Constraints derived from research findings (not from research-notes AMBIGUITIES; that section recorded "None blocking" but flagged two judgment calls):

| ID | Constraint | Rationale / Source |
|---|---|---|
| C-1 | Must work with the engineers' existing tools — Cursor, Claude Code, Aider, Continue, Cline, Roo, Copilot CLI, Gemini CLI, Codex CLI — without requiring tool replacement | All 9 tools persist locally by default; none ships team aggregation OOB (`01-native-storage-formats.md` Cross-Tool Summary Table). The user's stated goal is "all engineers' agent conversations" — adoption requires meeting tools where they are. |
| C-2 | Must support OSS / self-hosted deployment if data sensitivity demands it | Engineer-AI transcripts may contain customer data, secrets, internal architecture (`web-07` "GDPR / data retention"). On-prem options exist for: Pieces Enterprise, Mem0 self-host, Graphiti (OSS only), Cognee Apache-2.0, Zep BYOC enterprise tier, Langfuse MIT self-host, Helicone Apache-2.0 self-host, Phoenix Apache-2.0, Onyx MIT, Outline self-host (`web-03`, `web-04`, `web-05`, `web-06`). License-clean Apache-2.0/MIT options exist across every layer. |
| C-3 | Must NOT require routing live LLM calls through the store | Two reasons: (a) the user explicitly noted archive-side ingestion is acceptable [research-notes scenario], (b) all credible memory-layer products treat ingestion as data-shaped not call-shaped (`web-03` Key Findings — "No memory-layer product *requires* LLM-call routing"), (c) Helicone proxy-mode would be the alternative but it cannot ingest historical archives (`web-04`). |
| C-4 | Adapter design must absorb 9 codecs into 1 schema and walk per-tool path conventions | Per-tool adapters required: hashed (Cursor `workspaceHash`, Gemini `projectHash`), slugified (Claude Code cwd-slug), workspace-scoped (Cline/Roo VSCode globalStorage tagged by UUID), project-relative (Aider). Mapping back to canonical repo identity is itself non-trivial (`01-native-storage-formats.md` Key Takeaways). |
| C-5 | SpecStory's lossy-by-default Markdown is unsuitable as the canonical store for tool-call fidelity | "Capture fidelity is per-tool and 'may change'" (`web-01` Key Findings). If tool-call traces matter, plan a parallel capture path bypassing SpecStory's Markdown (`web-01` Recommendation 5). |
| C-6 | Must accommodate format drift across tool versions | Claude Code JSONL has evolved across versions (samples cover 2.1.121 and 2.1.126); Cursor `state.vscdb` schema breakage between Cursor releases reported on the forum; Continue.dev events tagged with `schema` version (`0.1.0`, `0.2.0`); GitHub `gh-copilot` deprecated 2025-10-25 in favor of `copilot-cli` with completely different on-disk layout (`01-native-storage-formats.md`). |
| C-7 | Must address per-engineer privacy vs. team-pooling | Two indexes per tenant (private + shared) with explicit publish step is the documented pattern (`web-07` "Hidden complexity"). Multi-tenancy primitives by DB: Weaviate native > Pinecone namespaces > pgvector RLS > Qdrant payload-shard (`web-07`). |
| C-8 | Embedding-model upgrades incur full re-embedding cost (~2-4× steady-state, ~yearly) | `web-07` "Hidden complexity #6". Architecture must support re-embedding without downtime. |
| C-9 | Must respect that SpecStory's RAG, team workspace, RBAC, audit log, and shared-team-space are roadmap-only today (2026-05-01) | `web-01` Capability Matrix; `qa/gaps-and-questions.md` I2 — RAG-coming-soon must not be counted as available capability. |
| C-10 | Pricing opacity for SpecStory team tier is a procurement risk; must not anchor architecture on un-priced commitments | `web-01` — `specstory.com/pricing` returns 404; `specstory.com/teams` is a Design Partner application form, no public SKU. `qa/gaps-and-questions.md` I1. |
| C-11 | License hygiene for any embedded/redistributed components | Open WebUI's branding clause for >50-user deployments [UNVERIFIED — `qa/gaps-and-questions.md` I6]; Khoj AGPLv3 is a copyleft constraint; Onyx MIT, LibreChat MIT, AnythingLLM MIT, Lobe Chat Apache-2.0, Langfuse MIT-with-EE, Helicone/Phoenix/Opik/Lunary/Laminar Apache-2.0 are clean (`web-04`, `web-05`). |

---

## 4. Gap Analysis

Each row contrasts today's fragmented per-tool storage (Current State) with the desired unified searchable RAG-capable team store (Target State). Severity uses Critical / Important / Minor.

| # | Gap | Current State | Target State | Severity | Notes |
|---|---|---|---|---|---|
| G-01 | Storage fragmentation across N tools | Each tool persists to its own silo: Claude Code `~/.claude/projects/<slug>/<sessionId>.jsonl`; Cursor `…/Cursor/User/workspaceStorage/<hash>/state.vscdb`; Aider `<project>/.aider.chat.history.md`; Continue.dev `.continue/dev_data/*.jsonl`; Cline `…/globalStorage/saoudrizwan.claude-dev/tasks/<id>/{api_conversation_history,ui_messages,task_metadata}.json`; Roo `…/globalStorage/rooveterinaryinc.roo-cline/tasks/<id>/*.json`; Copilot CLI `~/.copilot/session-state/` + `session-store.db`; Gemini CLI `~/.gemini/tmp/<projectHash>/`; Codex CLI `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl` (`01-native-storage-formats.md` Cross-Tool Summary Table) | Single normalized event store ingesting all 9 tools | Critical | Single largest gap — every other gap in this table inherits from it. |
| G-02 | Per-machine vs. team-shared | Every surveyed tool is local-only by default; "All nine tools persist locally by default. None of them ship a built-in team aggregator" (`01-native-storage-formats.md` Key Takeaways). Continue.dev gets closest via optional HTTP destination; Cline-enterprise + Copilot CLI offer partial introspection. | Team-wide aggregated corpus with cross-machine sync | Critical | Continue.dev's `data:` block + HTTP destination is the only first-party "fan-out plumbing" in the field. |
| G-03 | Format heterogeneity (JSONL vs Markdown vs SQLite vs per-task JSON vs JSON-arrays) | JSONL: Claude Code, Codex CLI, Copilot CLI, Continue. SQLite (KV blob): Cursor `state.vscdb`. Markdown + plaintext: Aider. Per-task JSON: Cline, Roo. JSON role/parts arrays: Gemini CLI. JSONL+SQLite hybrid: Codex CLI, Copilot CLI. (`01-native-storage-formats.md`) | One canonical schema with per-tool adapters | Critical | "JSONL is the de-facto wire format for agentic CLIs (Claude Code, Codex CLI, Copilot CLI, Continue.dev). Markdown (Aider) and SQLite-blob (Cursor) are the outliers" (`01-native-storage-formats.md`). |
| G-04 | Tool-call capture inconsistency | "Tool calls are universally captured but never normalized": Anthropic content-blocks (Claude Code), Google content-parts (Gemini CLI), OpenAI `RolloutItem.ResponseItem` (Codex), free-form JSON-in-SQLite (Cursor), SEARCH/REPLACE text (Aider). (`01-native-storage-formats.md` Key Takeaways) | Tool-call name + arguments + result preserved through normalization, chunking, embedding, retrieval | Critical | "Naive 512-token chunkers shred tool-call/tool-result pairs; need custom splitter that preserves message boundaries. 1-2 week investment" (`web-07`). LlamaIndex `ChatStore` and Haystack `ChatMessage` preserve structure; LangChain default loaders historically flatten it. |
| G-05 | File-edit fidelity is almost never first-class | "Diffs are typically reconstructible only by parsing tool-call payloads (apply_patch, write_to_file, str_replace_editor, SEARCH/REPLACE) — i.e., per-tool adapters required." Only Cline distinguishes machine-view (`api_conversation_history`) from user-view (`ui_messages`). (`01-native-storage-formats.md` Key Takeaways) | Diffs reconstructible per-tool with structured before/after | Important | Aider's git auto-commits are themselves a parallel persistence layer; "for diff/edit reconstruction the git log is more reliable than the markdown" (`01-native-storage-formats.md` Aider Notes). |
| G-06 | No semantic index over native storage | None of the 9 native tools indexes its own conversation history semantically. Copilot CLI ships `session-store.db` SQLite for indexed/queryable structure but field-level schema is not public, and it is per-user local. Codex CLI ships `state.sqlite` + `session_index.jsonl` (similar shape). (`01-native-storage-formats.md`) | Hybrid lexical + semantic index across normalized corpus | Critical | "Index/replay split is emerging. Codex CLI and Copilot CLI both ship JSONL-plus-SQLite. Claude Code ships only JSONL (no first-party index), which is precisely the gap a SpecStory-style aggregator fills" (`01-native-storage-formats.md`). |
| G-07 | No RAG retrieval into future prompts (native tools) | None of the 9 tools retrieves past conversations into the next prompt. Cursor's `@Past Chats` provides retrieval inside Cursor only, no external RAG API and no team-wide search surface (`web-08`). | Captured history retrievable into next agent prompt across team | Critical | This is the core capability the user's question asks for ("used as context for future conversations"). |
| G-08 | SpecStory does NOT ship RAG / context-injection today | "RAG coming soon" — `web-01` confirms no shipping retrieval-into-prompt feature; FAQ confirms no write-back into editor chat history; beta.specstory.com surfaced "memory retrieval" / "AI knowledge base" as coming-soon only (host returned ECONNREFUSED at research time). | Shipping RAG | Critical | `qa/gaps-and-questions.md` I2: do NOT count it as available capability. SpecStory is a one-way capture pipeline today, not a two-way memory layer. |
| G-09 | SpecStory team workspace / shared-team-space NOT shipping | "Single-user workspaces — explicitly stated" today; "Team collaboration on roadmap"; no RBAC documented; no audit log documented; no shared workspace as a first-class entity documented today; team-product page = Design Partner CTA. (`web-01` Capability Matrix; `web-01` Question 8 cont.) | Multi-engineer team workspace with RBAC and audit | Critical | Pre-revenue / closed-beta on team tier as of 2026-05-01. No paid SKU publicly purchasable. |
| G-10 | No team aggregation OOB across the 9 native tools | All nine native tools' team aggregation column = "No" except: Continue.dev = "Partial (plumbing yes, dashboard no)"; Cline = "Partial (enterprise tier adds prompt-storage forwarding)". (`01-native-storage-formats.md` Cross-Tool Summary Table) | Team-wide corpus visible to all opted-in members | Critical | Continue's HTTP destination is the closest first-party path; everything else is third-party scrape. |
| G-11 | No RBAC / access control on per-engineer or per-conversation basis | Native tools: no team identity beyond local OS user (Claude Code "no team/user identity beyond local OS user, no commit SHA — only branch"; `01-native-storage-formats.md`). SpecStory: keys user-scoped (no granular OAuth-style scopes), 403 = trying to access another user's resources, but NO documented RBAC for shared content (`web-01`). | Per-doc / per-namespace ACLs with permission-aware retrieval | Critical | Comparable RBAC models exist in: Glean per-doc ACLs at push time, Onyx ACL inheritance from connectors (e.g., Slack channel ACLs propagate to search), Langfuse EE project-level RBAC, Confluence space/page/group permissions (`web-04`, `web-05`, `web-06`). |
| G-12 | No cross-tool conversation linking | Each tool encodes session/project identity differently: Cursor opaque `workspaceHash`, Gemini `projectHash` of project root, Claude Code slugified-cwd, Aider keeps files in the project itself, Cline/Roo VS Code extension globalStorage tagged by UUID. (`01-native-storage-formats.md` Key Takeaways) | Engineer-task threads link sessions across Claude Code + Cursor + Aider via repo identity + time + file overlap | Important | "Mapping all of these back to a canonical repo identity is itself a non-trivial ingestion concern" (`01-native-storage-formats.md`). No surveyed product does this today. |
| G-13 | Cursor's roadmap "Generate Cursor Rules from chat history" partially mitigates a related but different gap | Shipped in Cursor v0.49: `/Generate Cursor Rules` from chat history, derives rules per workspace, no team or cross-tool dimension (`web-02`, `web-08`). Cross-device chat sync remains a long-running open feature request. | Cross-tool, cross-engineer rule + retrieval surface | Important | Flag per `qa/gaps-and-questions.md` M3 — "biggest medium-term threat". Cursor's eventual native team-chat-sync would shrink the Cursor portion of any aggregator's value. Differentiation has to come from multi-tool aggregation + vendor-neutral export + dev-first storage (`web-02` Recommendation 2). |
| G-14 | SpecStory capture fidelity is per-tool and lossy-by-default | "Formats differ by tool and can change" — SpecStory's canonical store is uniform Markdown converted from per-tool sources; original tool-call structure is best-effort (`web-01` capture-mechanics summary). | Lossless or near-lossless capture for tool calls and structured fields | Critical | If tool-call traces are required, plan a parallel capture path (e.g., Claude Code transcript JSONL ingest direct from `~/.claude/projects/`, bypassing SpecStory's Markdown) — `web-01` Recommendation 5. |
| G-15 | SpecStory cloud is read-mostly — no POST to create sessions | "No POST for create — projects appear to be auto-created by sync"; "No POST for create — write path is exclusively via the CLI / extension sync, not direct API upload" (`web-01` Question 4). | Programmatic ingestion endpoint accepting arbitrary normalized events | Important | External systems cannot inject synthetic conversations into SpecStory cloud; integrations must run through `specstory run` / `specstory sync`. |
| G-16 | SpecStory Cloud auth is user-scoped, not team-scoped | "No granular OAuth-style scopes — keys are user-scoped (403 = trying to access another user's resources)" (`web-01` Question 4 cont.) | OAuth scopes / team-scoped keys / SSO | Important | No SDKs shipped today (JS/TS, Python, Go listed as "coming soon" — `web-01`). |
| G-17 | No shipped "RAG over own past chats" in any OSS chat platform | "The pattern across all eight platforms is identical: RAG = 'chat with your uploaded documents'. None of them ship native semantic RAG over the user's *own past chats*" (`web-05` Key Findings). Open WebUI: indirect (chat → Knowledge re-import); LibreChat: keyword Meilisearch only; AnythingLLM: no; Onyx: chats stored in Postgres, not re-indexed into Vespa by default; Lobe Chat: no; Khoj: partial (notes yes, chats summarized); Chatbox/BetterChatGPT: none. | RAG over team's own AI conversation history | Critical | "Universal gap: RAG-over-own-chat is unsolved in OSS chat platforms. This is a real differentiator opportunity" (`web-05` Recommendation 6). |
| G-18 | Native tools have no embeddings | Claude Code: "no embeddings". Cline: "no embeddings". Copilot CLI: "no documented embeddings". (`01-native-storage-formats.md`) | Vector-indexed corpus | Critical | Subsumed by G-06 but flagged separately because it constrains build options (any solution must add embedding pipeline). Voyage voyage-code-3 reports +13.8% over OpenAI text-embedding-3-large on code retrieval (`web-07`, with `[UNVERIFIED]` precision per `qa/gaps-and-questions.md` I5). |
| G-19 | No structured diff capture | Claude Code: "no structured diff capture for file edits (Edit tool input/output is stored verbatim as strings, not as a parsed unified diff)". Codex CLI: "No dedicated `FileEdit` rollout type — edits ride along inside `ResponseItem` tool-call content (e.g., `apply_patch`); a parser must extract them. No diff normalization". Continue: "No structured diff per edit (edit is captured as before/after spans, not unified diff)". Cursor: "No first-class diff capture (edits are reconstructed from message blocks)". (`01-native-storage-formats.md`) | Normalized diff representation per accepted edit | Important | Aider's git auto-commits provide a workaround for Aider only — the git log is more reliable than its markdown for diff/edit reconstruction. |
| G-20 | No published field-level schemas for some sources | UNVERIFIED schema surfaces: Cursor `state.vscdb` JSON shape; Cline / Roo per-file fields; Gemini CLI `logs.json`; Copilot CLI `session-store.db` table layout; Continue.dev event-type catalog at field-level; Aider `.aider.llm.history`; Codex CLI `state.sqlite` columns; Claude Code sidecar dirs of same-UUID. (`01-native-storage-formats.md` Gaps and Questions) | Source-stable adapter contracts | Important | Adapters require empirical schema dumps + version-pinned tests; brittle without monitoring. |
| G-21 | Per-project hashing/identity inconsistency across tools | Cursor opaque `workspaceHash`, Gemini `projectHash`, Claude Code slugified-cwd, Aider in-project, Cline/Roo VS Code globalStorage by UUID. (`01-native-storage-formats.md`) | Canonical repo identity (commit-SHA-based or remote-URL-based) | Important | Required for G-12 cross-tool linking; Gemini's hash mapping is internal-only and must be re-derived by the aggregator. |
| G-22 | Aider has no machine-readable schema | Markdown + plaintext only; no per-message UUIDs; no structured tool-call objects; "LLM request bodies only present if `--llm-history-file` is enabled". Aider docs describe `.aider.chat.history.md` as the chat history file but do not warn it is the ONLY machine-readable artifact unless `--llm-history-file` is set. (`01-native-storage-formats.md`) | Structured ingestion of Aider sessions including tool calls | Important | Of all surveyed, Aider has the most human-friendly transcript and the *least* machine-friendly schema. Adapter must parse SEARCH/REPLACE blocks textually. |
| G-23 | Stale documentation references to deprecated tools | `gh-copilot` deprecated 2025-10-25 in favor of standalone `copilot-cli` with completely different on-disk layout (`~/.copilot/`); older blog posts that point at `gh-copilot` paths are stale. Cursor community guidance still recommends manually copying `state.vscdb` between machines despite product moving toward account-bound chat in newer versions. (`01-native-storage-formats.md` Stale Documentation Found; `qa/gaps-and-questions.md` M5) | Adapter version-pinning + deprecation tracking | Minor | Continuous-integration concern, not a fundamental architecture concern. |
| G-24 | None of the LLM observability platforms harvests IDE-side artifacts natively | "None of these platforms harvest IDE-side artifacts natively. They all expect to sit at the API call site. SpecStory's architectural niche (post-hoc IDE-archive harvesting) is not duplicated by any Bucket-C platform" (`web-04` Key Findings). Phoenix is the only platform with a community-documented playbook for migrating user conversations into traces post-hoc. | Captured-archive ingestion path is canonical | Important | Implies hybrid: SpecStory-style harvester + Helicone/Langfuse forward API-side capture is plausible (`web-04` Recommendation 4). |
| G-25 | Memory-layer products do not ingest from native tool storage by default | None of Mem0, Letta, Zep, Graphiti, Cognee, LangMem, SuperMemory, Mastra, Basic Memory MCP ships a Cursor / Claude Code / Cline / Aider / Roo / Continue / Gemini-CLI / Copilot-CLI / Codex-CLI native-storage adapter. They accept arbitrary message arrays / episodes via `add()` API but the adapter from native silo → memory layer is BYO. (`web-03` Key Findings — "Batch ingestion of arbitrary transcripts is supported by most products as a side effect of an open `add()` API") | Native-storage adapter chain feeding memory layer | Critical | Strongest direct-replay match: Graphiti's `add_episode_bulk` API accepts arbitrary text or structured JSON with reference timestamps — perfect for replaying a `.specstory/history/` archive. |
| G-26 | SuperMemory has IDE integration but narrow OSS surface | SuperMemory is the standout with first-party Cursor / Claude Code / VS Code / Windsurf MCP support — unique among memory-layer products. Trade-off: full feature parity requires hosted plan; OSS surface narrower than Mem0/Graphiti (`web-03`). | First-party multi-IDE integration AND clean OSS self-host | Important | Choice axis: integration UX vs. data sovereignty. |
| G-27 | OSS chat platforms are wrong-shaped as the unified store | Open WebUI: data model is "chats started in this UI", not external transcripts; ingesting external chats as Knowledge docs loses chat structure → becomes RAG corpus. LibreChat: MongoDB schema opinionated around interactive UI chats; agent transcripts (with tool calls, large context, cache hits) don't map cleanly. AnythingLLM: chat-with-docs not search-prior-chats; bug #4598 — `user_id = NULL` for API-key chats — disqualifying for team-of-record. Lobe Chat: assumes interactive UI sessions. Khoj: per-user, AGPLv3 copyleft. (`web-05`) | Substrate that natively models normalized AI-tool conversation events | Important | Onyx is the exception — its ingestion API + Vespa + ACL is purpose-built for "ingest stuff from N sources, search across all of it" (`web-05` Recommendation 1). |
| G-28 | Enterprise knowledge platforms require per-tenant procurement and per-platform format conversions | Glean: enterprise-only, sales-led, no public pricing; ingestion text-content cap ~16.875 MB per doc. Notion: 3 rps rate limit, rich-text 2000 chars per element, code blocks ~2000 chars per block — long transcripts produce 100s of API calls. Confluence: ~5 MB per page REST save-request limit, requires conversion to storage format (XHTML) or ADF (Markdown not native). Slack: 40k chars per message, Block Kit 50 blocks max, ~1 msg/sec/channel. (`web-06`) | Generic ingestion sink not bottlenecked by per-platform constraints | Important | "Rate limits and per-document size caps mean the ingestion design should batch transcripts into digest documents (per session or per day), not stream per-turn — universally true across Notion (3 rps), Confluence (5 MB), Slack (1 msg/s/channel), and even Glean (bulk preferred)" (`web-06` Recommendations). |
| G-29 | Tool-call-aware chunking is rare in pipeline frameworks | "Most pipeline tools' default loaders flatten ToolMessages incorrectly; need to preserve tool_call_id linkage so retrieval can fetch a tool result + its caller together" (`web-07` Hidden complexity #2). LlamaIndex `ChatMessage` + `ChatStore` and Haystack `ChatMessage` (text + tool_calls + tool_call_results) preserve structure; LangChain works but requires more glue; Mastra preserves in TypeScript Agent SDK; txtai requires custom adapter. | Default chunker preserves tool_call_id linkage | Important | One of the "hidden hard problems" enumerated in `web-07` — directly threatens SC-3. |
| G-30 | Incremental ingest deduplication is non-trivial | "Chat archives are append-mostly with rare in-place edits (Cursor's draft mode). Need content-addressed dedup; LangChain `SQLRecordManager` is the cleanest pattern" (`web-07` Hidden complexity #3). | Content-addressed dedup so re-running ingestion is idempotent | Important | Without this, every ingestion run re-embeds the corpus — economically painful at G-08 (re-embed) cost. |
| G-31 | Per-engineer privacy vs. team pooling has no default model | "Per-engineer privacy vs. team pooling — typically two indexes per tenant (private + shared) with explicit publish step" is the documented pattern but no surveyed product enforces it OOB (`web-07` Hidden complexity #5). | Two-index (private + shared) with explicit publish workflow | Important | Implementation choice constrained by DB primitive: Weaviate native multi-tenancy, Pinecone namespaces, pgvector RLS, Qdrant payload-shard (`web-07`). |
| G-32 | Re-embedding cost on model upgrade is a recurring tax | "When Voyage releases voyage-4, you re-embed everything. Budget 2-4x the steady-state embedding cost as a one-time event every ~12 months" (`web-07` Hidden complexity #6). | Re-embed pipeline tested + sized for ~yearly model bumps | Minor | Embedding cost is negligible at 10-engineer scale ($1-$18/yr — `web-07` cost model), so the tax is operational not financial. |
| G-33 | Quality eval loop is ungated by default | "Without an eval harness (golden-set queries → expected results), retrieval quality drifts silently. 1-2 weeks to set up properly" (`web-07` Hidden complexity #7). | Golden-set eval CI gate | Important | Directly enables SC-4 (recall-uplift measurement). |
| G-34 | GDPR / data-retention / secret-redaction not handled by capture tools | "Engineer transcripts may contain customer data, secrets, internal architecture. Redaction pipeline is non-trivial" (`web-07` Hidden complexity #8). SpecStory ships `specstory-guard` Agent Skill (pre-commit secret scan over `.specstory/history/`) but this is opt-in and post-hoc (`web-01`). | Inline redaction + retention policy + per-region storage | Critical | Compliance-blocking for customer-data-touching engineering teams. SpecStory's at-rest encryption is "Not documented" (`web-01` Question 2). |
| G-35 | None of the surveyed memory-layer products requires LLM-call routing | Mem0, Letta, Zep, Graphiti, Cognee, LangMem, SuperMemory, Mastra, Basic Memory MCP — "No memory-layer product *requires* LLM-call routing through itself. They all sit beside the LLM rather than as a proxy" (`web-03` Key Findings). | Confirms target architecture is achievable | Minor (positive finding) | Validates C-3 constraint. The ingest-from-archive design is architecturally available across the field. |
| G-36 | Dominant industry pattern is "distilled knowledge", not "raw chat archives" | Cody, Tabnine, Devin, Augment, Cline (Memory Bank), Cascade (Memories), Cursor (`.cursor/rules`), Continue (Hub) all invest in curated rules / memory files / org knowledge entries — small, retrievable, hand-maintained — rather than indexing raw conversation transcripts. (`web-08` Key Findings) | Raw transcript indexing co-existing with distilled-knowledge patterns | Important | "SpecStory's thesis (index the raw stream) is genuinely contrarian, and the market gap is real" (`web-08`). The two are complementary; target should write back to `AGENTS.md` / Memory Bank patterns, not replace them. |
| G-37 | No mainstream code-AI vendor ships team-shared, indexed, RAG-capable chat-history product | "Every major IDE-AI keeps chat history per-user/local. Cross-device chat sync is a frequent forum request even for Cursor" (`web-08` Key Findings). Cody: per-user chat history, no team chat search. JetBrains AI: per-project local, no team. Tabnine: chat GA but team value-prop = shared commands not chat. Devin Knowledge: curated docs, not transcripts. Augment Code: code-RAG, not chat-RAG. (`web-08`) | Team-shared indexed RAG-capable chat history | Critical | Confirms no ready-to-buy alternative exists today. |
| G-38 | Pricing for SpecStory team tier unobtainable without Design Partner application | `specstory.com/pricing` returns 404; `specstory.com/teams` is a Design Partner CTA; cloud pricing not visible publicly. (`web-01`; `qa/gaps-and-questions.md` I1) | Public pricing or contracted pricing before architecture commitment | Important | Procurement risk; time-box a Design Partner intake before anchoring on SpecStory. |
| G-39 | Agent Skills are post-hoc analyses, not retrieval/RAG primitives | SpecStory's 6 published Agent Skills (specstory-guard, link-trail, organize, project-stats, session-summary, yak) read/parse local Markdown or call Cloud API; none feeds history back into a live prompt. (`web-01` Question 5) | Retrieval/RAG primitive callable from agents | Important | "Agent Skills" is a side-channel summarization/hygiene layer, not the missing RAG primitive. |
| G-40 | Open WebUI license clause for >50-user deployments | Recently moved to a modified license that requires preserving "Open WebUI" branding for deployments serving >50 users without a commercial license. [UNVERIFIED — `qa/gaps-and-questions.md` I6 — needs verification against actual license text.] | License-clean substrate for embedding/re-skinning | Minor | Constraint surfaces only if Open WebUI is selected as substrate. |
| G-41 | Onyx chats are stored in Postgres but not re-indexed into Vespa by default | "Onyx's own chat sessions are stored in Postgres and are visible/searchable in the UI, but they aren't (by default) re-indexed into Vespa as documents. There's a community pattern of running a connector against your own chat exports to feed them back in" (`web-05`). | Self-chat re-indexing built-in | Minor | Solvable with a connector; doesn't disqualify Onyx as substrate. |
| G-42 | Pieces for Developers export surface and team-SKU posture unclear | Pieces is the closest *architectural* analogue to "engineer-AI context bus" — captures across IDEs/browsers, on-device LTM. Whether team SKU and export API meet the requirement is the open question worth a follow-up evaluation. (`web-08` Pieces; Recommendation 1) | Verified export contract + team SKU pricing | Important | Bench-evaluate: (a) chat export format/API, (b) team workspace SKU posture, (c) whether external transcripts can be ingested into Pieces' LTM. |
| G-43 | Capture mechanism per-tool fragility | SpecStory capture mechanisms differ per tool: Cursor reads `state.vscdb`, Copilot reads `chatSessions` JSON, Claude Code uses `specstory run` wrapper + reads `~/.claude/projects/`, CLI providers follow wrapper-and-translate pattern. "Formats differ by tool and can change" (`web-01`). | Adapter framework with version-pinned codecs and CI tests against fixtures | Important | Vendor coupling concentrates risk on adapter layer. |
| G-44 | No webhooks from SpecStory cloud | "Webhooks: Not mentioned — likely not available" (`web-01` Question 4). | Event-driven downstream consumers | Minor | Workaround: poll SpecStory REST API at rate limit (1000/hr REST). |
| G-45 | No published encryption-at-rest claim from SpecStory | "Encryption: Not documented in any page reached. Likely standard TLS for transport; at-rest encryption not explicitly claimed" (`web-01` Question 2). | Documented at-rest encryption + key management | Critical | Compliance-blocking for many teams. |
| G-46 | SpecStory is one-way (no write-back into editor chat) | "Round-trip back into the editor: NOT SUPPORTED today. SpecStory does not write to Cursor's `state.vscdb` or Copilot's chat storage — workaround is 'reference the saved markdown file in your prompt'." (`web-01` Question 1 cont.) | Two-way: retrieval results injected into the next prompt programmatically (e.g., via MCP) | Important | Subsumed by G-07 / G-08; flagged separately because it is the architectural reason SpecStory is not yet a RAG product. |
| G-47 | Tool-call structure preserved differently per tool | Anthropic content-blocks vs. Google content-parts vs. OpenAI `RolloutItem.ResponseItem` vs. JSON-in-SQLite (Cursor) vs. SEARCH/REPLACE text (Aider). Each requires its own tool-call extraction logic. (`01-native-storage-formats.md`) | Single canonical tool-call event with `tool_call_id`, `name`, `input`, `result` | Important | Granular instance of G-04. |
| G-48 | LLM observability platforms require API-call-site instrumentation | "Two distinct architectures dominate Bucket C ... Proxy/gateway (Helicone) ... OTLP / OpenLLMetry instrumentation" — all expect to sit at API call site (`web-04`). Cline / Aider / Continue lack first-class hooks today; Helicone proxy-mode covers them only via custom base URLs. | Archive-side ingestion compatible with observability backends | Important | Phoenix is the only platform with documented community import path for archived conversations. |
| G-49 | Repo identity not always captured | Claude Code: "no commit SHA (only branch); no project-level metadata file (project dir contains only the JSONL files)". (`01-native-storage-formats.md`) | Per-event commit SHA + repo remote URL captured at ingest time | Important | Enables G-12 cross-tool linking and G-21 canonical repo identity. |
| G-50 | Sub-agent / sidechain capture only in Claude Code | Claude Code captures sub-agent threads via `isSidechain` boolean on each event; no other surveyed tool exposes this dimension explicitly. (`01-native-storage-formats.md` Claude Code) | Sub-agent / parent-thread linkage in normalized schema | Minor | Source-coupled — only one tool exposes it; preserve where present. |

### Section 4 Summary — Most Severe Gaps Driving Section 6 Options

The 50-row gap inventory above clusters into a small number of architecturally load-bearing gaps that drive the Options Analysis:

- **No team aggregation, no team-shared store, no team RAG exists today across the 9 native tools or in shipping SpecStory** (G-01, G-02, G-08, G-09, G-10, G-37). This is the central capability gap and the single largest driver of build/buy/adopt — every credible option must add this layer because none of the surveyed comparables ship it end-to-end (memory-layer products require BYO ingestion adapters per G-25; OSS chat platforms are wrong-shaped per G-27; observability platforms require API-call-site instrumentation per G-48; SpecStory's RAG and team workspace are roadmap-only).
- **Format heterogeneity + lossy capture + tool-call inconsistency are the technical hardest sub-problems** (G-03, G-04, G-05, G-14, G-22, G-29, G-47, G-49, G-50). Any option must absorb 9 codecs into 1 schema, preserve tool_call_id linkage through chunking, reconstruct diffs from per-tool tool-call payloads, and pin per-tool schemas against documented version-drift (G-23). Choice of pipeline framework (LlamaIndex / Haystack vs. LangChain default) and DB multi-tenancy primitive (Weaviate native vs. pgvector RLS — G-31) is downstream of how seriously these are treated.
- **Compliance-grade capabilities (RBAC, redaction, encryption-at-rest, retention, audit) are absent or undocumented across SpecStory and most native tools** (G-11, G-34, G-45, G-09 audit-log roadmap-only). Combined with the requirement to support OSS / self-hosted deployment (C-2), this set of gaps eliminates closed-SaaS-only options for compliance-bound teams and steers the recommendation toward Apache-2.0 / MIT-licensed self-hostable substrates (Onyx, Langfuse, Helicone, Phoenix, Graphiti, Mem0 self-host) — exactly the shortlist the Options Analysis must compare to SpecStory-adopt and BYO.

---

## 5. External Research Findings

This section consolidates the comparables landscape across 8 web-research partitions (web-01..web-08) into 9 thematic subsections covering: SpecStory itself (5.1), direct competitors (5.2), AI agent memory layers (5.3), LLM observability platforms (5.4), self-hosted/OSS chat platforms (5.5), enterprise org-memory & knowledge platforms (5.6), build-your-own RAG-over-conversations stack (5.7), adjacent/less-direct tools (5.8), and a synthesis summary (5.9).

## 5.1 SpecStory (the reference baseline)

SpecStory is the closest-named comparable and the user's stated reference point. It is a multi-tool conversation-capture pipeline (local-first Markdown into `.specstory/history/`) with an opt-in cloud index that adds hybrid lexical+semantic search. It is **NOT a RAG product today** — it does not write retrieved context back into editor chat. Team workspace and RAG are roadmap-only. OSS surface is the CLI + provider plugins; IDE extensions and the cloud are closed. (Source: `web-01-specstory-deep-dive.md` — github.com/specstoryai/getspecstory, docs.specstory.com.)

### 5.1.1 SpecStory product surfaces

| Surface | Deployment | Storage | Search | RAG | Team Agg | License | Pricing | Relevance | Source |
|---------|-----------|---------|--------|-----|---------|---------|---------|-----------|--------|
| SpecStory CLI (`specstory run/sync`) | Local-first; binary via Homebrew tap | `.specstory/history/*.md` (Markdown, per-project, per-session) | Local: filesystem only; Cloud (when synced): hybrid lexical+semantic | No (one-way capture; no write-back to editor) | No | Apache-2.0 (Go 99.8%) | Free | HIGH (capture baseline) | web-01 (github.com/specstoryai/getspecstory) |
| SpecStory Cursor / Copilot IDE extensions | Local plugin reading `state.vscdb` (Cursor) / `chatSessions` JSON (Copilot) | Translates source → `.specstory/history/*.md` | Same as CLI | No | No | **Closed source** | Free | HIGH (capture baseline) | web-01 (github.com/specstoryai/getspecstory README support matrix) |
| SpecStory Cloud (cloud.specstory.com) | SaaS; closed-source backend | Cloud-side index of synced Markdown sessions | Hybrid lexical + semantic; filters by project & time-range | No (search yes, injection no) | Single-user workspaces only today | **Closed source** | No public pricing — `/pricing` 404s; `/teams` is a Design Partner application form `[I1, I2]` | HIGH | web-01 (docs.specstory.com cloud overview, /teams) |
| SpecStory Cloud REST + GraphQL API | SaaS API on `https://cloud.specstory.com` | Read-mostly; no POST to create sessions; HEAD for cheap dedup | Sessions/Projects list/get; GraphQL at `/api/v1/graphql` | n/a | n/a | Closed (API itself documented) | Bundled with cloud | HIGH (integration vector for "build on top") | web-01 (docs.specstory.com/api-reference/introduction) |
| SpecStory Agent Skills (6 skills) | Local; `npx skills add specstoryai/agent-skills` | Reads `.specstory/history/*.md` (5/6) or Cloud API (1/6 — project-stats) | Per-skill (yak detection, summary, organize, link-trail, secret-guard, project-stats) | **No retrieval/RAG primitive** — post-hoc analyses only | No | Apache-2.0 | Free | MEDIUM (illustrates skill-pattern, NOT a RAG layer) | web-01 (github.com/specstoryai/agent-skills) |
| AIrgap (separate SpecStory OSS) | Local hooks / CI / Git diff guardrail | n/a (operates on diffs, not chat) | n/a | n/a | n/a | OSS (Apache-style) | Free | LOW (orthogonal — not a chat-history product) | web-01 (docs.specstory.com/airgap) |

### 5.1.2 SpecStory capture fidelity per source tool

| Source tool | On-disk source | Conversion to Markdown | Tool-call fidelity | Source |
|-------------|---------------|------------------------|-------------------|--------|
| Cursor IDE | `state.vscdb` (SQLite) | Read & translate | Unconfirmed (depends on what Cursor stores) | web-01 (docs.specstory.com FAQs) |
| Copilot (VSCode) | `chatSessions` JSON | Read & translate | Unconfirmed | web-01 (docs.specstory.com FAQs) |
| Claude Code | `~/.claude/projects/*.jsonl` | Read JSONL & translate | **Likely yes** (JSONL contains tool_use blocks) — but docs say "formats differ by tool and can change" | web-01 (docs.specstory.com FAQs) |
| Codex / Cursor CLI / Droid / Gemini CLI | Per-tool transcript | `specstory run` wrapper + sync converter | Per-tool; lossy-by-default | web-01 (docs.specstory.com FAQs) |

### 5.1.3 SpecStory capability gaps that drive comparables search

- No RAG / context injection into next prompt (roadmap only, no shipping date) — `[I2]` source web-01
- No team workspace as first-class entity (single-user today; team on roadmap) — web-01
- No RBAC, audit log, or shared workspace documented today — web-01
- No self-hosted / on-prem option announced — web-01
- No published encryption-at-rest claim — web-01
- No webhooks; no official SDK shipped (JS/TS/Py/Go "coming soon") — web-01
- Cursor-rules-generation lives in closed-source extension; mechanism undisclosed — web-01
- Pricing not externally obtainable without Design Partner application `[I1]` — web-01

---

## 5.2 Direct competitors (specstory-shaped)

Tools positioned the same way SpecStory is — capture AI coding chats, sync, share/search across team. Per cross-partition dedup `[M1]`: AnythingLLM is treated as primary in 5.5; Cline Memory Bank as primary in 5.8; Pieces as primary in 5.8; MCP-memory servers (Omega Memory) as primary in 5.3. Cursor coverage as a target tool for capture is in 5.1; Cursor's own emerging features as a competitor are in this section.

| Tool | Deployment | Storage | Search | RAG | Team Agg | License | Pricing | Relevance | Source |
|------|-----------|---------|--------|-----|---------|---------|---------|-----------|--------|
| **CursorShare** | SaaS (apparent) | Cloud (apparent) | Unknown | Unknown | Yes (advertised) | Closed | Unknown | LOW (weak evidence — site flaky `[I3]`) but HIGH shape match if real | web-02 (https://www.cursorshare.com/) |
| **Continue Hub** | OSS extension (Apache-2.0) + SaaS hub (proprietary); self-host for Enterprise | Cloud (Hub) + local for extension | Lexical (browse Hub blocks/bundles) | Yes — assistants include codebase context blocks | Yes — "manage and share private agents across your team" — but aggregates **configs/assistants/rules**, not chat transcripts | Continue ext: Apache-2.0; Hub: proprietary | Solo $3/M tokens PAYG; Team $20/seat/mo + $10 credits/seat; Enterprise custom | MEDIUM (validates team-aggregation thesis but for configs, not chats) | web-02 (https://hub.continue.dev/, https://continue.dev/pricing) |
| **Charlie Mnemonic** (GoodAI) | OSS self-hosted (web app + Ollama backend) | Local | Semantic + structured memory tiers | Yes (memory recall is the product) | No — explicitly "personal" assistant | OSS (permissive) | Free | LOW (out of category — personal AI, not coding-chat capture) | web-02 (https://github.com/GoodAI/charlie-mnemonic) |
| **Cursor (native)** | SaaS-tied desktop (proprietary) | Local SQLite for foreground; remote storage for background-agent chats | Lexical via in-app history UI; markdown export | Yes — `/Generate Cursor Rules` from chat history shipped v0.49 | **Not yet natively** — long-running open request | Proprietary | Pro $20/mo; Business $40/seat/mo; Enterprise custom | HIGH (defensive/incumbent — biggest medium-term threat per `[M3]`) | web-02 (https://docs.cursor.com/agent/chat/history, cursor.com/en/changelog/0-49) |
| **claude-replay / CC Replay / vibe-replay** | OSS CLI (claude-replay) + small SaaS viewers (ccreplay.com, vibe-replay.com) | Reads local `~/.claude/projects/**/*.jsonl`; output is local HTML or hosted viewer | Limited — replay/timeline UI; lexical at best | No | Manual link sharing only; no workspace concept | claude-replay OSS; commercial viewers proprietary | OSS free; SaaS TBD | HIGH (narrow) — direct shape match for Claude Code slice | web-02 (https://github.com/es617/claude-replay, https://www.ccreplay.com/, https://vibe-replay.com/) |
| **GroundRules** | SaaS beta | Cloud (apparent) | N/A — analysis tool | No (rule generation, not retrieval) | Unknown | Closed | Beta — likely free | MEDIUM — single-feature overlap with SpecStory's "Cursor rules from chat history" | web-02 (https://www.groundrules.ai/) |
| **Packmind** | SaaS (likely) | Unknown | Unknown | Implied via "context engineering" framing | Yes (team-context positioning) | Closed | Unknown | LOW (weak evidence `[I3]`) | web-02 (https://packmind.com/context-engineering-for-ai-coding-101/) |

**Cross-references:**
- AnythingLLM — see 5.5 (primary). Mentioned in web-02 only as comparable-but-different (it is a chat *destination*, not a *capturer*).
- Pieces for Developers — see 5.8 (primary). web-02 frames it as adjacent (OS-wide capture, not coding-chat-specific).
- Cline Memory Bank — see 5.8 (primary). web-02 highlights its git-native team-aggregation pattern as a borrowable model.
- Omega Memory — see 5.3 (primary as MCP memory server).

---

## 5.3 AI agent memory layer

Persistent memory / RAG-over-conversation backends that sit beside the LLM (not as a proxy). Per cross-partition dedup `[M1]`: MCP memory servers (Omega Memory, Basic Memory) are primary here. The bake-off shortlist for "BYO storage+retrieval over captured transcripts" lives here.

| Tool | Deployment | Storage | Search | RAG | Team Agg | License | Pricing | Relevance | Source |
|------|-----------|---------|--------|-----|---------|---------|---------|-----------|--------|
| **Mem0** | OSS self-host + managed cloud; Enterprise on-prem | Vector store (memory-record) + optional graph (Neo4j/Memgraph) | Semantic over LLM-extracted "facts" | Yes — primary use case | `user_id`/`agent_id`/`run_id`/`app_id` scoping; Enterprise SSO+audit | Apache-2.0 | Hobby free (10k adds, 1k retrievals/mo); Starter $19; Pro $249; Enterprise custom | HIGH (STRONG fit — `add(messages, user_id=...)` accepts arbitrary historical transcripts in batch) | web-03 (https://mem0.ai, https://github.com/mem0ai/mem0 — ~54.5k stars) |
| **Letta (formerly MemGPT)** | OSS self-host (Docker) + Letta Cloud | Hierarchical `memory_blocks` (`human`, `persona`) + archival vector overflow | Semantic recall over archival | Yes — but as agent runtime, not memory CRUD | Cloud orgs/projects; OSS shards via agent-per-user | Apache-2.0 | OSS free; Cloud usage-based (sales for Enterprise) | MEDIUM (WEAK-MEDIUM fit — agent-loop-centric, no clean batch replay path) | web-03 (https://www.letta.com, https://github.com/letta-ai/letta — ~22.4k stars) |
| **Zep Cloud** | Managed SaaS; Enterprise BYOC (your AWS VPC) + BYOK/BYOM | Temporal knowledge graph (Graphiti-backed) + vector retrieval; bi-temporal fact validity | Hybrid semantic + BM25 + graph traversal | Yes — Graph-RAG positioning | Users/sessions/threads; Enterprise SSO; SOC2 Type II + HIPAA | Closed (cloud); OSS path is Graphiti | Free Starter (1k credits/mo); Flex $125; Flex Plus $375; Enterprise custom | HIGH (STRONG fit — `messages.add`/`graph.add` accept historical transcripts) | web-03 (https://www.getzep.com/, https://www.getzep.com/pricing/) |
| **Graphiti (Zep OSS)** | Self-host only; requires Neo4j or FalkorDB + LLM provider | Temporal knowledge graph (bi-temporal validity) | Hybrid semantic + BM25 + graph | Yes | `group_id` partition (logical multi-tenancy) | Apache-2.0 | Free OSS (LLM extraction + Neo4j costs apply) | HIGH (**EXCELLENT** fit — `add_episode_bulk` API is the single cleanest match for replaying timestamped `.specstory/history/`) | web-03 (https://github.com/getzep/graphiti — ~25.6k stars; arxiv.org/abs/2501.13956) |
| **Cognee** | OSS self-host (Modal/Railway/Fly/Render/Daytona/local) + Cloud | Hybrid vector + KG; plugin model (Neo4j/Kuzu graph; LanceDB/Qdrant vector) | Hybrid via cognify→memify pipeline | Yes | Explicit user/tenant isolation | Apache-2.0 | Free OSS; Cloud Dev $35/mo (1k docs/1GB/1 user); Cloud Team $200/mo (2.5k docs/2GB/10 users); On-Prem Enterprise custom | HIGH (STRONG fit — `add()` accepts strings/files/URLs/dirs for bulk ingest) | web-03 (https://www.cognee.ai/, https://github.com/topoteretes/cognee — ~17k stars) |
| **LangMem (LangChain)** | Library; runs on LangGraph `BaseStore` (InMemory/AsyncPostgres/etc.) | Memory record over any LangGraph store | Semantic over stored memories | Yes (with extraction) | Namespace tuples in BaseStore | MIT | Free OSS (LangSmith/LangGraph Cloud separate) | MEDIUM (building block, not standalone product; ~1.4k stars) | web-03 (https://langchain-ai.github.io/langmem/) |
| **SuperMemory** | Hosted SaaS + partial OSS (MCP server MIT) | Hybrid RAG + persistent memory graph | Vector + graph overlay | Yes | Unlimited users across all tiers | Core MIT; full pipeline closed | Free $0 (1M tokens/10k queries); Pro $19; Scale $399; Enterprise custom | HIGH (STRONG fit — only product with first-party Cursor/Windsurf/VSCode/Claude Code MCP integration; ~22.4k stars) | web-03 (https://supermemory.ai, https://github.com/supermemoryai/supermemory) |
| **Mastra Memory** | OSS framework + Mastra Cloud | Working memory + semantic recall over LibSQL/Postgres/Upstash/MongoDB | Vector over thread/resource | Yes (live agent loops) | Thread/resource keys | OSS (license per repo) | Framework free; Cloud separate | LOW-MEDIUM (WEAK fit — coupled to TS agent framework; live-only ingest) | web-03 (https://mastra.ai/docs/storage/overview) |
| **Basic Memory MCP** | Local-only by default; cloud sync option | Markdown files + SQLite index + semantic graph from internal links | Semantic + lexical | Yes | Single-user | OSS (license unspecified on page) | Free OSS; cloud sync separate | MEDIUM (good individual fallback; weak for team-scale) | web-03 (https://docs.basicmemory.com/) |
| **Omega Memory** (cross-ref from 5.2) | OSS local/self-host; Pro tier hinted | Local | Semantic (vector recall over captured memory) | Yes — purpose-built MCP RAG memory layer for agents | Limited | Apache-2.0 | Free OSS install; Pro tier (no published numbers) | MEDIUM (MCP-native — Cursor/Claude Code/Windsurf/Cline/Obsidian) | web-02 (https://omegamax.co/, pypi.org/project/omega-memory/) |

**Adjacent products surveyed but excluded as low-relevance** (web-03): Context.ai (LLM analytics, not memory), Helicone Mem (no standalone memory product — observability/proxy; see 5.4), Arcade.dev (MCP runtime, not memory), Rememberall (early-stage, no track record), OpenAI Agents SDK Memory (in-framework primitive), Cloudflare Agent Memory (edge primitive, not transcript ingest target).

---

## 5.4 LLM observability platforms

Tracing/eval platforms that capture LLM traffic at the API layer (proxy or OTLP instrumentation). Architecturally distinct from memory layers (5.3): they sit at the call site, not as a CRUD memory store. Two dominant patterns: **proxy/gateway** (Helicone) and **OTLP/OpenLLMetry instrumentation** (Phoenix, Langfuse, Traceloop, Opik, Laminar).

| Tool | Deployment | Storage | Search | RAG | Team Agg | License | Pricing | Relevance | Source |
|------|-----------|---------|--------|-----|---------|---------|---------|-----------|--------|
| **LangSmith (LangChain)** | SaaS; Enterprise/hybrid self-host | Full traces (sessions, threads, tool calls, retrieval) | UI filters + full-text + thread query language; **no native semantic** | Datasets (JSONL/CSV); **RAG re-inject = user code** | Workspaces/projects/orgs; RBAC on paid | Closed (SDK MIT) | Dev free (~5k traces/mo); Plus $39/seat/mo + usage; Enterprise contact; overage $0.50/1k | HIGH (documented Claude Code + Cursor connect via env vars/proxy/OTLP) | web-04 (https://www.langchain.com/pricing-langsmith, support article on connecting Claude Code/Cursor) |
| **Langfuse** | OSS self-host (Docker/Helm) + Cloud | Sessions/traces/spans/generations/observations; threaded view via `session.id` | UI filters + full-text + metadata filters; **no native vector** | First-class Datasets; REST + Python/TS SDK; user-code RAG re-inject | Orgs/projects/members/RBAC; project-level RBAC + audit + retention + SCIM in `/ee` | MIT core + commercial EE for `/ee` modules | OSS free; Cloud Hobby free (50k obs/mo); Core $59/mo; Pro $199/mo; Enterprise | HIGH — official Claude Code integration page (uses OTLP hooks); Cursor + Continue + Aider via OpenLLMetry; ~26.4k stars; ingest viable via `/api/public/ingestion` | web-04 (https://langfuse.com/, github.com/langfuse/langfuse, langfuse.com/integrations/other/claude-code) |
| **Helicone** | OSS self-host (Docker Compose + Helm) + Cloud | Full request/response, multi-turn Sessions, tool-call payloads | UI filters + body search + tags + **semantic vector index on Pro+** | Datasets + Jobs API for export; webhooks | Orgs/projects/member roles | Apache-2.0 | Hobby free (10k req/mo, 1GB); Pro $79/mo + usage; Team $799/mo + usage; Enterprise | HIGH — **best architectural fit for "minimal-instrumentation forward capture"** (proxy mode `api.anthropic.com` → `anthropic.helicone.ai`; covers Claude Code via `ANTHROPIC_BASE_URL`, Cursor, Continue, Cline, Aider); Helicone MCP for Claude Code/Cursor; ~3-4k stars | web-04 (https://www.helicone.ai/, github.com/Helicone/helicone) — license corrected to Apache-2.0 per `[merged-gaps issue]` |
| **Arize Phoenix** | OSS self-host (Docker, runs locally as notebook) + Phoenix Cloud + Arize AX (paid SaaS) | OTEL/OpenInference spans (LLM/retriever/tool/agent/embedding); Sessions for multi-turn | UI filters + full-text + span attributes + **built-in semantic search over inputs/outputs** | First-class Datasets + community guide for "Migrating User Conversations to Traces" + pandas/REST/OTLP export | OSS single-tenant by default; multi-tenant via Arize AX | Apache-2.0 (core); some adjacent packages flagged Elastic-2.0 in some channels `[I7]` | Free OSS; Phoenix Cloud free tier; Arize AX contact | HIGH — **only platform with documented historical-ingest playbook**; ~5k+ stars; OTEL-native (Claude Code OTLP, Cursor via OpenLLMetry) | web-04 (https://phoenix.arize.com/, community.arize.com migration guide) |
| **HoneyHive** | SaaS multi-tenant; dedicated cloud; self-hosting; **air-gapped** | Full sessions/traces/tool calls/retrieval; OpenInference compatible | UI filters + semantic + **SQL on enterprise** | Datasets, eval suites, API export | Orgs/projects/RBAC; enterprise focus | Closed | Free tier; Pro ~$300+/mo; Enterprise contact; event-based metering | MEDIUM (compliance-heavy/regulated; no first-class IDE coding-tool integration) | web-04 (https://www.honeyhive.ai/) |
| **Braintrust** | SaaS + Enterprise self-host (AWS Terraform) | Full traces (input messages, tool calls, output, span tree, metadata, cost) | UI filters + **SQL/BTQL** (first-class) + semantic ("deep") + structured | **Strongest export story**: annotated JSON/Parquet via UI/SDK/API + BTQL endpoint | Orgs/projects/RBAC | Closed (SDK permissive) | Free tier (limited); Pro per-seat + usage; Enterprise; processed-data billing | HIGH (best-in-class search/SQL for closed-source SaaS) | web-04 (https://www.braintrust.dev/) |
| **PromptLayer** | SaaS; Enterprise self-host | Request-level (prompts/completions/metadata/tool calls); OTEL span-level | UI filters + tags + full-text + SQL-like | "Datasets from history" + CSV/API; prompt registry/evals | Workspaces/members | Closed (SDK MIT) | Free tier (limited); Pro $50/seat/mo; Enterprise | MEDIUM (mature SDK; REST `log_request` makes archive-replay easy) | web-04 (https://docs.promptlayer.com/) |
| **W&B Weave** | SaaS + mature on-prem / dedicated cloud (CoreWeave-managed) | Ops/Calls/Traces; structured span tree; tool-call capture | UI filters + attribute filters + plots; **weak semantic** | Datasets + evals export REST API | W&B teams/projects/RBAC; mature multi-tenant | SDK Apache-2.0; backend closed | W&B Free (single user); Teams ~$50/seat/mo; Enterprise; Weave bundled | MEDIUM (best fit only if team already on W&B) | web-04 (https://docs.wandb.ai/weave) |
| **Opik (Comet)** | OSS full self-host (Docker/Helm/K8s) + Comet Cloud | Traces/spans/conversation threads/tool calls/retrieval; OTEL-friendly | UI filters + full-text + attribute | First-class Datasets, prompt mgmt, **Ragas integration** | Workspaces/projects/members | Apache-2.0 | OSS free; Cloud Free; Pro per-seat + usage; Enterprise | HIGH (~19k stars; most permissive OSS license; Ragas integration for RAG eval) | web-04 (https://www.comet.com/site/products/opik/, github.com/comet-ml/opik) |
| **Lunary** | OSS self-host (Docker, Apache-2.0) + Cloud | Runs/threads (conversation grouping)/tool calls/costs/feedback signals | UI filters + tags + run/thread search + full-text | Datasets/exports/prompt registry | Orgs/projects | Apache-2.0 | OSS free; Cloud Free (1k events/day); Team $20/seat/mo + usage; Enterprise | MEDIUM (~1-2k stars; smaller ecosystem) | web-04 (https://lunary.ai/) |
| **AgentOps** | SaaS + AWS/GCP/Azure self-host | Sessions/events/LLM calls/tool calls/errors; agent-step replay | UI filters + session search; less mature | Limited — session export via API; **no first-class datasets→RAG** workflow | Orgs/projects | SDK MIT; backend closed | Free dev; Pro per-seat + usage; Enterprise | MEDIUM (agent-framework-centric — CrewAI/AutoGen/LangGraph; weaker for IDE coding tools) | web-04 (https://www.agentops.ai/) |
| **Traceloop / OpenLLMetry** | OpenLLMetry SDK Apache-2.0 self-host-anywhere; Traceloop SaaS backend (limited self-host) | OpenLLMetry spans (LLM/vector DB/embedding/agent/tool); Traceloop visualizes trees | Traceloop UI filter + semantic; OTEL backends determine UX | Traceloop datasets/evals; OpenLLMetry export = standard OTLP | Traceloop SaaS orgs/projects | OpenLLMetry Apache-2.0; Traceloop closed | OpenLLMetry free; Traceloop free tier + paid (per span/trace) | HIGH (de-facto OTEL standard; ~7k+ stars on OpenLLMetry; **Traceloop MCP server Dec 2025 brings OTEL to Cursor and Claude Code** — pypi `opentelemetry-mcp`) | web-04 (https://www.traceloop.com/, github.com/traceloop/openllmetry, github.com/traceloop/opentelemetry-mcp-server) |
| **Laminar (lmnr.ai)** | OSS self-host Apache-2.0 + Cloud | Sessions/traces/spans/tool calls; OTEL ingest | UI filters + semantic on input/output + tags | Datasets + evals; SDK export | Workspaces/projects | Apache-2.0 | OSS free; Cloud free tier (limited spans); Pro tier; Enterprise | MEDIUM (~3k+ stars; YC-backed; OTEL via OpenLLMetry; no first-class IDE plugin) | web-04 (https://www.lmnr.ai/, github.com/lmnr-ai/lmnr) |

**Critical observation:** None of these platforms harvest IDE-side artifacts natively — they all expect to sit at the API call site. SpecStory's architectural niche (post-hoc IDE-archive harvesting) is not duplicated by any 5.4 platform. They are **complementary, not competitive**.

---

## 5.5 Self-hosted / OSS chat platforms

Chat platforms that could serve as a unified conversation store. Per cross-partition dedup `[M1, M2]`: AnythingLLM and Onyx are primary in this section. Universal pattern: every platform here treats RAG as "chat with uploaded documents" — **none ship native semantic RAG over the user's own past chats**.

| Tool | Deployment | Storage | Search | RAG | Team Agg | License | Pricing | Relevance | Source |
|------|-----------|---------|--------|-----|---------|---------|---------|-----------|--------|
| **Open WebUI** | Self-host (Docker/Helm/Railway/Render/pip) | SQLite default → PostgreSQL via `DATABASE_URL`; ChromaDB default vectors (Qdrant/Milvus/pgvector swappable) | UI search; semantic via Knowledge | **Indirect/PARTIAL** — RAG is over uploaded files/URLs; chats not auto-indexed; manual re-ingest as Knowledge possible | Yes — local accounts + RBAC (admin/user/pending) + OAuth (Google/MS/OIDC) + LDAP; group permissions + per-model access | **BSD-3-Clause-ish (modified post-2024)** — preserve "Open WebUI" branding for deployments >50 users without commercial license `[I6]` | OSS free | HIGH (closest off-the-shelf "unified chat store"; ~95k stars; import API + Knowledge API) | web-05 (https://github.com/open-webui/open-webui, docs.openwebui.com/features) |
| **LibreChat** | Self-host Docker Compose (Mongo+Meili+rag_api), Helm, Render/Railway | MongoDB (chats/users/messages); MeiliSearch (full-text); separate `rag_api` service with pgvector; local or S3 file storage | MeiliSearch keyword over own chats; no semantic on conversations | **NO native chat-RAG** — bundled `rag_api` operates on uploaded files only | Yes — local auth + OAuth (Google/GitHub/Discord/Facebook/Apple) + OIDC + LDAP; RBAC admin/user + granular per-feature permissions | MIT | OSS free | HIGH (~22k stars; explicit Import Conversations feature accepting ChatGPT format + LibreChat normalized JSON) | web-05 (https://github.com/danny-avila/LibreChat, librechat.ai/docs/features/import_convos) |
| **AnythingLLM** | Self-host Docker (`mintplexlabs/anythingllm`); desktop Electron; Render/Railway/Helm | SQLite default (Prisma) → Postgres switchable; pluggable vector (LanceDB default, Chroma/Pinecone/Weaviate/Qdrant/Milvus/AstraDB/pgvector) | Vector + lexical via embedded RAG | Yes — but doc-centric. **No chat-RAG**: chats stored as conversation rows for replay; not embedded | Yes — multi-user mode (admin/manager/default); local accounts; OAuth/SSO in cloud; RBAC scoped per workspace | MIT | OSS free; managed cloud + Enterprise paid | LOW-MEDIUM (~30k stars; doc upload API ingests transcripts as documents — loses turn structure; known multi-user audit-trail bug issue #4598 `user_id = NULL` for API-key chats) | web-05 (https://github.com/Mintplex-Labs/anything-llm, anythingllm.com/) |
| **Onyx (formerly Danswer)** | Self-host Docker Compose / Helm / AWS Terraform; managed cloud | Postgres (metadata/chats/users/ACLs) + **Vespa** (default vector + keyword index) + Redis (queues) + MinIO/S3 (blobs) — most production-shaped storage in this category | Hybrid (Vespa); ACL-aware | **PARTIAL** — own chats stored in Postgres but not re-indexed into Vespa by default; community pattern: run a connector against your own chat exports | Yes — local + OAuth + OIDC + **SAML SSO** + Google Workspace; RBAC admin/curator/basic; **per-document ACL inheritance from source connectors** (e.g., Slack channel ACLs propagate) | MIT (core); enterprise features (advanced RBAC, audit, SSO upgrades) gated paid | OSS free; managed cloud + Enterprise paid | **HIGH — STRONGEST adopt-as-product candidate** (~14k stars; YC-backed; first-class JSON ingestion API `{document_id, sections[], metadata, semantic_identifier, ...}` paired with `cc_pair_id`; SpecStory transcripts map cleanly to document/section model; public refs: Ramp, mid-size SaaS, multiple YC cos) | web-05 (https://github.com/onyx-dot-app/onyx, docs.onyx.app/developers/guides/index_files_ingestion_api) |
| **Lobe Chat** | Self-host Docker (`lobehub/lobe-chat-database` for server mode); Vercel one-click; Railway/Zeabur | Two modes: client-side IndexedDB (single-user) OR server-side Postgres + pgvector + Redis cache + S3 blobs; NextAuth/Clerk auth | UI search; semantic via knowledge base | **NO native chat-RAG** — knowledge base RAG operates on uploaded files | Server-mode only — Clerk/NextAuth OAuth; per-user data isolation; **no formal RBAC/team roles** ("many individual accounts" not "team workspace") | Apache-2.0 (core); some advanced features require LobeHub Cloud or commercial config | OSS free; managed Cloud paid | LOW (~50k stars but UX-driven not platform-driven; 40+ provider matrix is largest) | web-05 (https://github.com/lobehub/lobe-chat) |
| **Chatbox** | Native installers Win/Mac/Linux/iOS/Android/Web; **no server** | Local only — IndexedDB (web), local FS (desktop) | Local UI only | No native RAG | **No** (single-user desktop) | GPLv3 (community); commercial editions | OSS free | LOW (~30k stars; useful only as a possible *client* over a custom backend) | web-05 (https://github.com/chatboxai/chatbox) |
| **Khoj** | Self-host Docker Compose; pip dev; native installers; managed cloud | Postgres (with pgvector) for users/conversations/embeddings; local file/cloud blob; optional Redis | Vector over synced docs; conversation memory summarized for follow-ups | **PARTIAL** — indexes notes/PDFs/sync'd docs; cross-conversation semantic search not default | Multi-user self-hosted (email magic-link, Google OAuth); per-user isolation; **NOT team workspaces** — each user has own Khoj | **AGPLv3** (copyleft — friction for commercial fork) | OSS free; hosted cloud paid | LOW-MEDIUM (~25k stars; closest in spirit to "RAG over own past chats" but personal-scale; weak file API for transcript ingest) | web-05 (https://github.com/khoj-ai/khoj, docs.khoj.dev/) |
| **BetterChatGPT** | Static site (Vercel/Netlify); **no server** | Browser localStorage / IndexedDB | None | No | **No** | CC0-1.0 (public domain) | Free | LOW (~8k stars; lightly maintained; not a viable substrate) | web-05 (https://github.com/ztjhz/BetterChatGPT) |

**Universal gap (per web-05 finding):** **None of these platforms ship native semantic RAG over the user's own past chats.** The closest is Khoj (summarizes prior conversations) and Open WebUI (manual re-import as Knowledge). This is a real product gap in OSS land — and the most important architectural finding from the entire landscape survey.

---

## 5.6 Enterprise org-memory & knowledge platforms

Could enterprise knowledge tools ingest AI conversation transcripts? Every platform here exposes a documented REST ingestion path; the question is **fit and cadence**, not feasibility. Markdown is the lingua franca; rate limits and size caps universally favor batched/digest ingestion over per-turn streaming.

| Tool | Deployment | Storage | Search | RAG | Team Agg | License | Pricing | Relevance | Source |
|------|-----------|---------|--------|-----|---------|---------|---------|-----------|--------|
| **Glean** | SaaS multi-tenant; enterprise data residency US/EU; private VPC / dedicated tenancy | Custom-datasource push API; permission-aware ACLs | Hybrid (lexical + semantic + ranking); permission-aware | **Yes** — Glean Assistant generates grounded citations over indexed content; Custom datasources participate by default | Strong RBAC; per-doc ACLs at push time; allow lists/group lists/public-to-org | Closed (enterprise) | **Enterprise-only**, sales-led, no public pricing; API access included with platform license | HIGH (purpose-built for arbitrary corporate text ingestion; >64MB skipped for content; ~16.875MB indexed text cap) | web-06 (https://docs.glean.com/connectors/custom/about, glean.com/product/api) |
| **Mem (mem.ai)** | SaaS-only, US-hosted; no on-prem | Per-account; bearer-token; primary `mem-it` REST endpoint accepts markdown/text | Lexical + AI semantic recall via REST | **Yes** — "Chat with Mem" answers over notes with citations | Per-user account; team/RBAC story is thin | Closed | Paid plan required (Mem+); API gated to paying users; no clear enterprise SKU | MEDIUM (personal-first; one-doc-per-call; weak team rollout) | web-06 (https://help.mem.ai/features/api, docs.mem.ai/) |
| **Notion AI / Notion API** | SaaS US/EU options on Enterprise; no on-prem | `POST /v1/pages` + `PATCH /v1/blocks/{id}/children`; internal integration token or OAuth; JSON block schema | Built-in lexical + Notion AI semantic/RAG | **Yes** via Notion AI (paid add-on); Q&A across workspace permitted by user access | Page/database-level permissions; strong RBAC at workspace/group/page | Closed | API free on all plans; Notion AI per-seat paid add-on | HIGH (most likely "already deployed"; well-trodden community precedent — many ChatGPT/Claude→Notion integrations); rate limit ~3 rps; rich-text 2000 char/element; arrays max 100 elements; produces 100s of API calls per long transcript | web-06 (https://developers.notion.com/) |
| **Coda AI / Coda** | SaaS only; no on-prem | REST API at `coda.io/apis/v1`: rows or pages; Pack SDK for connector-style ingestion | Lexical inside docs; cross-doc weaker than Glean/Notion | **Yes** — Coda AI Block / Coda Brain answer over doc/workspace | Doc-level sharing + workspace RBAC; less granular than Notion | Closed | API on Pro+ paid; Coda AI paid add-on | MEDIUM (~10 rps typical; doc size caps stricter than Notion; structured-doc-first — transcripts fit awkwardly) | web-06 (https://coda.io/developers) |
| **Slack AI / Slack API** | SaaS; Enterprise Grid offers EKM, residency US/EU/JP/AU | `chat.postMessage` (~40k chars/msg, ~4k visible without "show more"); Block Kit max 50 blocks/msg; `files.upload` up to 1GB | Lexical (in:/from:/has:) + Slack AI semantic on Enterprise+ | **Yes** via Slack AI ("Ask anything") — requires Enterprise Grid + Slack AI add-on (per-seat) | Channel membership = visibility; private/shared channels respected | Closed | API free; Slack AI = paid add-on (Enterprise Grid) | MEDIUM (cheapest "drop somewhere indexable" since Slack is ubiquitous; Tier 1-4 rate limits ~1 msg/sec/channel sustained; quality workspace-bounded) | web-06 (https://api.slack.com/methods/chat.postMessage) |
| **Confluence AI / Confluence Cloud** | SaaS + **Confluence Data Center (self-hosted)** with separate REST API; residency US/EU/AU/DE on Premium+ | REST v2: `POST /pages` with `storage` (XHTML) or `atlas_doc_format` body; OAuth2 (3LO) or API token + email; markdown not native (conversion required) | CQL lexical + Atlassian Intelligence (Rovo) semantic + agentic on Premium/Enterprise | **Yes** via Atlassian Intelligence/Rovo with citations, permission-respecting | Space → page restrictions → group/user; robust enterprise RBAC | Closed | API on all paid; Atlassian Intelligence Premium+; Rovo typically Enterprise | HIGH (~5 MB REST save-request limit/page; strong for Atlassian-shop orgs; better for digest pages than per-turn capture) | web-06 (https://developer.atlassian.com/cloud/confluence/rest/v2/) |
| **Slite** | SaaS only; EU hosting on Enterprise | `POST /v1/notes` (createNote) accepts markdown + parentNoteId/folderId; API-key auth; OpenAPI spec published | Lexical + "Ask" semantic | **Yes** — "Ask" with citations | Workspace + channel + note-level permissions; team RBAC | Closed | API on Standard+/Premium/Enterprise; Ask AI typically Premium+ | MEDIUM (decent if Slite already team wiki) | web-06 (https://slite.com/integrations/api) |
| **Outline (getoutline.com)** | **On-prem / self-host supported (Docker, Postgres, Redis)** + SaaS US/EU | `documents.create` (markdown body, collectionId, parentDocumentId) + `documents.import` (file upload); API-key auth | Postgres full-text (lexical); newer cloud builds add AI | **LIMITED** — cloud has experimental AI; **self-hosted requires you to bolt on your own** (e.g., `documents.search` API + your own embeddings) | Collection + document permissions, group ACLs; decent RBAC | **BSL** (Business Source License — open-source-licensed) | Free OSS / free on all cloud tiers | MEDIUM-HIGH (uniquely on-prem-capable in this bucket; markdown-native; only fully OSS markdown-native API here) | web-06 (https://docs.getoutline.com/, getoutline.com) |
| **Guru (getguru.com)** | SaaS; Enterprise data residency options | Cards API + Sources for Answers + **Guru MCP server** (read/write to cards from Claude/ChatGPT/Cursor); API token (user + collection) | Hybrid lexical + Guru Answers semantic; permission-aware | **Yes** — Guru Answers first-class with cited responses; `POST /v1/answers` programmatic | Collection + group permissions; trust score / verification metadata | Closed | API on Builder/Enterprise paid; Guru Answers typically Enterprise | MEDIUM-HIGH (only platform here shipping MCP server natively; strong AI-tool integration signal; cards meant to be curated/verified, not append-only) | web-06 (https://help.getguru.com/docs/gurus-api, developer.getguru.com/docs/guru-mcp-server-overview) |
| **Bloomfire** | SaaS multi-tenant; enterprise residency on request | REST endpoints (limited public visibility — full reference often under NDA); Celigo iPaaS docs surface create-post / upload-content | Hybrid lexical + AI semantic / "AI Authoring" | **Yes** — AI search and answers over corpus | Series + group permissions; enterprise RBAC | Closed | Enterprise-only, sales-led | LOW-MEDIUM (sparse developer portal; weaker general fit — optimized for support-team vetted Q&A, not raw engineer-AI dialog) | web-06 (https://bloomfire.com/build-with-bloomfire/) |

**Universal pattern (per web-06):** Every platform exposes documented REST ingestion. Markdown is the lingua franca. Rate limits + per-document size caps (Notion 3 rps; Confluence 5 MB; Slack 1 msg/s/channel; Glean bulk preferred) mean **ingestion design should batch transcripts into digest documents (per session or per day), not stream per-turn**.

---

## 5.7 Build-your-own RAG-over-conversations stack

Components for assembling a custom unified AI-conversation DB. **Embedding API cost is a non-issue at 10-engineer scale** (~$1-18/yr regardless of provider) — vector DB hosting and engineering time dominate economics. Per cross-partition dedup `[M1, M2]`: Spool primary in this section (web-07 has the deeper cost-comparison precedent); Onyx primary in 5.5 — its appearance here is as a reference architecture.

### 5.7.1 Vector databases

| Vector DB | Deployment | Hybrid Search | Multi-tenant | License | Pricing | Scale ceiling | Source |
|-----------|-----------|---------------|--------------|---------|---------|---------------|--------|
| **Pinecone** | **Managed only** (no self-host) | Yes — sparse + dense + integrated reranking | Namespaces (10k Standard / 100k Enterprise per index) | Closed | Serverless: storage $0.33/GB-mo; Write Units $4-6.75/1M; Read Units $16-27/1M; Reranking $2/1k; Starter free 2GB/2M WU/1M RU | Billions; pod model deprecated for new signups Aug 2025 | web-07 (https://www.pinecone.io/pricing/) |
| **Weaviate** | Managed Serverless + Enterprise Cloud + BYOC + OSS self-host (Apache-2.0 Docker/K8s) | **Best-in-class** — built-in BM25F + vector fusion (alpha parameter) | **Native multi-tenancy** (tenants per collection — best in field) | Apache-2.0 | Sandbox free; Serverless ~$0.05/M dimensions/mo | 10B+ vectors real-world | web-07 (https://docs.weaviate.io/cloud/platform/billing) |
| **Qdrant** | OSS self-host (Apache-2.0 single binary or Helm) + Cloud (Standard/Premium) + Hybrid Cloud | Yes — sparse + dense + late fusion + Query API; ColBERT/Multivector 2024 | **Designed for it** — tenant-key payload indexing routes shards by tenant; supports millions of tenants | Apache-2.0 | Free single-node forever (0.5 vCPU/1GB/4GB disk); Standard usage-based; Premium min spend; Hybrid Cloud sales-led | Strong benchmark leader on QPS/latency | web-07 (https://qdrant.tech/pricing/) |
| **Chroma** | OSS embedded (SQLite) + self-host server + Chroma Cloud (2024) | **Limited** — basic metadata filters; full BM25/hybrid newer/less mature | "Tenants" + "databases" + "collections" hierarchy; less battle-tested | Apache-2.0 | OSS free; Cloud $0/mo Starter then usage-based | Distributed Chroma (2024) targets cloud-scale | web-07 (https://www.trychroma.com/) |
| **Milvus** | OSS self-host (Apache-2.0) requires etcd + MinIO/S3 + Pulsar/Kafka; Milvus Lite single-process for dev; Zilliz Cloud managed | Yes — sparse + dense + BM25 v2.5+ + weighted fusion + RRF | Partition keys + RBAC; more overhead than Qdrant/Weaviate | Apache-2.0 | OSS free; Zilliz Cloud Serverless from $0.10/M reads + storage; Dedicated CU from ~$99/mo | **Highest scale ceiling** (10B+ vec installations); also highest ops burden | web-07 (https://milvus.io/, https://zilliz.com/pricing) |
| **pgvector (Postgres)** | **Self-host (anywhere Postgres runs)**; RDS/Supabase/Neon all support | Yes — Postgres tsvector + pgvector cosine; RRF hand-written but trivial | Rows-with-tenant-id + row-level security | PostgreSQL License | Free extension; cost = whatever Postgres host charges | Genuinely competitive up to ~10-50M vec/node with HNSW + pgvectorscale; CIDR 2026 paper closing gap fast | web-07 (github.com/pgvector/pgvector, www.cidrdb.org/cidr2026/papers/p2-liu.pdf) |
| **Turbopuffer** | **Managed only** (no self-host as of 2026) | Yes — vector + BM25 full-text; namespace-scoped | Namespaces (cheap; millions supported — per-engineer or per-conversation viable) | Closed | Object-storage-backed serverless; writes ~$2/GB; queries ~$0.04/query at scale; storage ~$0.05/GB-mo | Billions; cold-query p90 ~444ms, warm p50 ~8ms (1M vec); **architecturally cheapest for chat-archive workloads** (most data cold) | web-07 (https://turbopuffer.com/docs, used by Cursor and Notion AI per web-07 — `[I4, UNVERIFIED — no public URL citation provided]`) |
| **LanceDB** | OSS embedded library + self-hosted server + LanceDB Cloud | Yes — vector + full-text (tantivy-based); reranker integrations | Table-per-tenant or tenant-id column; less native than Weaviate | Apache-2.0 | OSS free; Cloud usage-based on storage + queries | Embedded + serverless modes; columnar Lance format on S3 → cheap storage; targets billions | web-07 (https://lancedb.com/) |

### 5.7.2 Embedding APIs / models

| Embedding | $/1M tokens | Max input | Dims | Code-retrieval benchmark | Self-host? | Source |
|-----------|-------------|-----------|------|--------------------------|------------|--------|
| **OpenAI text-embedding-3-large** | $0.13 ($0.065 batch) | 8,192 | 3072 (Matryoshka) | ~71-78% on code | No | web-07 (platform.openai.com/docs/models/text-embedding-3-large) |
| **OpenAI text-embedding-3-small** | $0.02 ($0.01 batch) | 8,192 | 1536 | Lower than large | No | web-07 |
| **Cohere Embed v3** | ~$0.10 | 512 (v3 English) | 1024 | Strong MTEB; trails Voyage on code | Yes (Model Vault: $4-5/hr instance) | web-07 (cohere.com/pricing) |
| **Cohere Embed v4** (multimodal) | Partly contact-sales | 128k context | 256/512/1024/1536 (Matryoshka) | Multimodal text+image | Yes (Model Vault) | web-07 |
| **Voyage voyage-3** | $0.06 | 32k | — | Strong; trails code-3 | No | web-07 (docs.voyageai.com/docs/pricing) |
| **Voyage voyage-3-large** | $0.18 | 32k | — | Top general | No | web-07 |
| **Voyage voyage-3-lite** | $0.02 | 32k | — | Lower quality | No | web-07 |
| **Voyage voyage-code-3** | $0.18 | 32k (4x OpenAI) | — | **+13.8% over OpenAI text-embedding-3-large on code retrieval** `[I4, I5 — verified single-value claim]`; ~92% vs OpenAI ~78% on coding tasks | No | web-07 (blog.voyageai.com/2024/12/04/voyage-code-3/); MongoDB acquired Voyage 2025 `[I4, UNVERIFIED — no URL citation]` |
| **Jina jina-embeddings-v3** | ~$0.018 (free 10M/mo); Apache-2.0 weights → self-host free | 8,192 | 1024 (Matryoshka to 32) | Competitive with OpenAI large; weaker than Voyage code-3 on pure code | Yes (Apache-2.0) | web-07 (jina.ai/embeddings/) |
| **BGE-M3 (BAAI)** | Free (MIT); ~$0.001-0.005/1M on $0.50/hr A10 | 8,192 | 1024 dense + sparse + multi-vector (ColBERT) **in one pass** — uniquely versatile | Top-3 OSS on MTEB; 100+ languages | Yes (MIT) | web-07 (arxiv.org/abs/2402.03216, huggingface.co/BAAI/bge-m3) |
| **E5 family (intfloat/multilingual-e5-large)** | Free (MIT) | 512 (older) / 8k (v2 instruct) | 1024 | Strong general; weaker on specialist code than BGE-M3 / Voyage | Yes (MIT) | web-07 (arxiv.org/abs/2212.03533) |
| **GTE (Alibaba gte-large-en-v1.5, gte-Qwen2-7B)** | Free (Apache-2.0) | 8,192 | 1024 / 3584 | gte-Qwen2-7B top of MTEB OSS; expensive (7B params, A100-class) | Yes (Apache-2.0) | web-07 (huggingface.co/Alibaba-NLP/gte-large-en-v1.5) |

### 5.7.3 Pipeline / orchestration tools

| Tool | License | Chat-transcript ingestion | Chunking strategies | Tool-call-aware? | Source |
|------|---------|---------------------------|---------------------|------------------|--------|
| **LlamaIndex** | MIT | YES — `ChatMessage` + `ChatStore` abstractions; loaders for JSONL/SQLite/Notion/Slack; `SemanticSplitterNodeParser` | Semantic, sentence, token, hierarchical, document-aware; agentic chunkers 2024-2025 | **Yes** — `ToolMessage`/`FunctionMessage` types preserved; built-in tool-call retrieval examples | web-07 (docs.llamaindex.ai) |
| **LangChain / LangGraph** | MIT | YES — `ChatMessageHistory` + `SQLChatMessageHistory` + `RedisChatMessageHistory`; `SQLRecordManager` for incremental re-indexing; LangGraph checkpointing | RecursiveCharacterTextSplitter (default); MarkdownHeaderTextSplitter; semantic_chunker | **Yes** — `ToolMessage` natively; LangGraph state graphs preserve full tool-call traces | web-07 (python.langchain.com) |
| **Haystack (deepset)** | Apache-2.0 | YES — `ChatMessage` (text + tool_calls + tool_call_results); **explicit indexing-vs-query pipeline separation** | DocumentSplitter (word/sentence/passage); custom splitters easy | **Yes** — `ToolMessage` and tool_call/tool_call_results are first-class fields | web-07 (docs.haystack.deepset.ai) |
| **txtai** | Apache-2.0 | Yes — embeddings-database supports incremental upserts | Configurable; sentence/segment + custom | Less explicit; needs custom adapter to preserve tool calls as metadata | web-07 (github.com/neuml/txtai) |
| **Mastra (TypeScript)** | **Elastic License v2** (source-available; commercial restrictions for SaaS reselling) | Yes — chunking + embedding helpers; **"observational memory" feature** targets long-running agent histories — claims **10x cost reduction vs naive RAG** `[I4, UNVERIFIED — no URL citation provided]` | text/markdown/code/json/html splitters; recursive | **Yes** — Agent SDK preserves tool calls in conversation state | web-07 (mastra.ai/en/docs/rag/overview) |

### 5.7.4 Reference architectures

| Architecture | Description | Source |
|-------------|-------------|--------|
| **Spool** | OSS local + paid cloud. Local pgvector on `:5434`, FastAPI cloud sync, **$25/user/mo team tier**. Closest direct precedent for this use case. Uses pgvector for both single-user and multi-tenant cloud. Supports Claude Code + Cursor. | web-07 (https://spooling.ai/) |
| **MyChatArchive** | Local-first; semantic search via local embeddings; ChatGPT/Claude/Cursor exports | web-07 (https://mcpmarket.com/server/mychatarchive) |
| **searchat** | PyPI package for semantic search over agent histories — reference for ingestion contract | web-07 (https://pypi.org/project/searchat/) |
| **claude-history** | Pure-fuzzy, no vectors — "do we even need a vector DB?" baseline | web-07 (https://github.com/raine/claude-history) |
| **Claude Historian MCP** | MCP server pattern surfacing chat history as a tool callable by other agents | web-07 (https://mcp.directory/mcp/details/346/claude-historian) |
| **AgentsView** | Cross-agent session history with optional Postgres sync — closest "team mode" pattern | web-07 (https://www.agentsview.io/) |
| **AWS multi-tenant vector search** | Aurora pgvector + Bedrock KBs; metadata-filter tenant isolation | web-07 (aws.amazon.com/blogs/database/multi-tenant-vector-search-with-amazon-aurora-postgresql-and-amazon-bedrock-knowledge-bases/) |
| **Azure secure multi-tenant RAG** | End-to-end auth-aware grounding architecture | web-07 (learn.microsoft.com/azure/architecture/ai-ml/guide/secure-multitenant-rag) |
| **ChatRAG multi-tenant** | pgvector + RLS pattern for shared KB + private chats | web-07 (chatrag.ai/docs/multi-tenant) |
| **Onyx** (cross-ref to 5.5) | OSS enterprise search; widely-cited ref for team-scale conversation/document RAG with auth — primary coverage in 5.5 | web-07 (github.com/onyx-dot-app/onyx) |
| **LangChain "Building Chat LangChain"** | Walkthrough: `SQLRecordManager` + Weaviate for iteratively re-indexed chat over docs | web-07 (langchain.com/blog/building-chat-langchain-2) |
| **Microsoft Agent Framework chat history patterns** | Tool-call-preserving conversation storage with compaction | web-07 (devblogs.microsoft.com/agent-framework/chat-history-storage-patterns-in-microsoft-agent-framework/) |
| **Snowplow agent memory** | Event-level memory indexed as vectors, retrieved during conversation; observability angle | web-07 (snowplow.io/blog/ai-agent-memory-behavioral-patterns) |

### 5.7.5 Cost model — example 10-engineer team (per web-07)

**Workload assumptions:** 10 engineers × 50 conversations/week × 50 messages × 200 tokens = 50M tokens/year of new content; ~500k chunks/year; vector DB stored ~3-5 GB; query volume ~50k/year (~140/day).

| Stack | Embeddings | Vector DB | Hosting | TOTAL/yr | Build effort |
|-------|-----------|-----------|---------|----------|--------------|
| **Cheapest** (pgvector-on-existing-PG + Voyage-3-lite + LlamaIndex) | $1 | $0 | $0 | **$1/yr** | 3-5 days prototype; 2-3 weeks team-ready |
| **Recommended baseline** (pgvector-on-Supabase Pro + Voyage-code-3 + LlamaIndex) | $9 | $300 | $0 | **~$310/yr** | 1-2 weeks prototype; 4-6 weeks team-ready |
| **Best quality** (Qdrant Cloud + Voyage-code-3 + LlamaIndex + Cohere reranker) | $9 | $700 | $50 | **~$760/yr** | 2 weeks prototype; 6-8 weeks team-ready |
| **OSS-only / air-gapped** (self-host Qdrant + BGE-M3 on idle GPU + Haystack) | $0 | $240 (VPS) | included | **~$240/yr + GPU idle** | 3-4 weeks prototype; 8-12 weeks team-ready |

**Critical economic finding:** Build alone (4-12 weeks engineering) at $200k/yr loaded engineer cost = **$30-100k upfront** vs. Spool managed at $25/user/mo × 10 × 24 months = **$6k**. Crossover with managed/buy depends entirely on engineer-time pricing.

### 5.7.6 Hidden complexity (where BYO projects slow down — per web-07)

1. **Conversation chunking** — naive 512-token chunks shred tool-call/tool-result pairs; need custom splitter preserving message boundaries (1-2 weeks)
2. **Tool-call ingestion** — pipeline tools' default loaders flatten ToolMessages incorrectly; preserve `tool_call_id` linkage
3. **Incremental sync** — chat archives are append-mostly with rare in-place edits (Cursor draft mode); content-addressed dedup; LangChain `SQLRecordManager` is cleanest pattern
4. **Authentication & multi-tenancy** — pgvector + RLS or Weaviate native are easiest; Pinecone namespaces lock you in
5. **Per-engineer privacy vs. team pooling** — typically two indexes per tenant (private + shared) with explicit publish step
6. **Re-embedding cost on model upgrade** — when Voyage releases voyage-4, re-embed everything (budget 2-4x steady-state every ~12 months)
7. **Quality eval loop** — without golden-set eval harness, retrieval drifts silently (1-2 weeks setup)
8. **GDPR / data retention** — engineer transcripts may contain customer data, secrets, internal architecture; redaction pipeline is non-trivial

---

## 5.8 Adjacent / less-direct tools

Tools that don't fit primary buckets but inform architecture. **The dominant industry pattern is *distilled knowledge*, not *raw chat archives*** — Cody, Tabnine, Devin, Augment, Cline Memory Bank, Cascade Memories all invest in curated rules / memory files rather than indexing raw conversation transcripts. SpecStory's "index the raw stream" thesis is genuinely contrarian.

| Tool | Deployment | Storage | Search | RAG | Team Agg | License | Pricing | Relevance | Source |
|------|-----------|---------|--------|-----|---------|---------|---------|-----------|--------|
| **Charlie Mnemonic (GoodAI)** (cross-ref to 5.2) | OSS self-host (web app + Ollama) | Local | Semantic | Implicit retrieval over stored memory | **No** (personal) | OSS | Free | LOW (interesting reference architecture only) | web-08 (https://github.com/GoodAI/charlie-mnemonic) |
| **Pieces for Developers** | Hybrid — desktop local-first + cloud-optional + self-hosted/on-prem in Enterprise | LTM up to 9 months of OS-wide context; on-device + cloud workflows | Both lexical and semantic | **Yes** — Pieces Copilot uses local LTM + files + snippets as RAG context | Pieces Drive supports team snippet sharing; LTM team-sharing **not explicitly stated and appears individual-first** | Closed (Pieces OS components partially open) | Free tier; paid Enterprise with self-hosting | **HIGH — only product in this bucket whose architecture genuinely overlaps with the user's goal**: captures AI Copilot chats across IDEs/browsers; supports continuing same chat across tools; on-device LTM. **further-investigation-needed**: (a) chat export format/API, (b) team workspace SKU, (c) external transcript ingestion | web-08 (https://pieces.app/features/copilot, pieces.app/features/context-switching, pieces.app/enterprise) |
| **Continue.dev Hub** (cross-ref to 5.2) | OSS extension + SaaS Hub; self-host for Enterprise | Cloud Hub + local | Lexical (browse blocks/bundles) | Yes (assistants include codebase context) | Yes — explicit team/org governance — but for **configs**, not chats | Continue ext: Apache-2.0; Hub: proprietary | Solo $3/M tokens; Team $20/seat; Enterprise custom | LOW for chat goal; **separate market** (shared assistant configs vs. shared conversation history) | web-08 (https://hub.continue.dev/, techcrunch.com/2025/02/26 launch) |
| **Cursor — `.cursor/rules` + `@Past Chats`** (cross-ref to 5.2 for the competitor framing) | SaaS-tied desktop | Local SQLite for chat; `.cursor/rules` files travel with repo (team-shareable) | `@Past Chats` retrieval inside Cursor; no external RAG API | Limited (no team-wide search surface) | **Partial** — rules in repo are team-shareable; cross-device chat sync **not officially supported** | Proprietary | Pro $20; Business $40; Enterprise | MEDIUM — pipeline-with: keep as one of the capture sources for unified store | web-08 (docs.cursor.com/agent/chat/history, docs.cursor.com/context/rules, forum.cursor.com cross-device-sync threads) |
| **Cline Memory Bank** | Convention/protocol — markdown files in repo (`projectbrief.md`, `productContext.md`, `activeContext.md`, `progress.md`) read at session start | Local md in repo (committed to git) | Filesystem (lexical) | **No** — read whole-file at session start; not retrieved | Yes via git — `.clinerules` and `memory-bank/` files committed | Cline core: Apache-2.0; community Memory Bank repos vary | Free | LOW (architectural reference; NOT a transcript store — captures distilled *project state*, not raw chats); **convergent pattern with `AGENTS.md`/`.cursor/rules`** for distilled team-shared project memory | web-08 (mintlify.com/cline/cline/features/memory-bank, deepwiki.com/cline/prompts/4.2-memory-bank-system) |
| **MCP Memory Servers** (general category) | Local + self-hosted variants; Memory Bank MCP supports Postgres/Qdrant/MongoDB backends | Knowledge graph (official `@modelcontextprotocol/server-memory`); local Markdown (Basic Memory); pgvector/Qdrant/Mongo (Memory Bank MCP protocol-lattice variant) | Graph traversal (official); semantic (vector variants) | **Yes** for vector-backed and graph-backed servers | Depends on server — most reference impls local; some support team-deploy backends | Varies (mostly OSS) | Free OSS | **HIGH (as substrate, not competitor)** — Memory Bank MCP (protocol-lattice) with pgvector/Qdrant is **strongest team-deploy substrate**; most architecturally interesting alternative architecture | web-08 (github.com/modelcontextprotocol/servers, mcpservers.org/servers/protocol-lattice/memory-bank-mcp) |
| **Sourcegraph Cody** | SaaS + Enterprise self-hosted | Per-user chat session history (closed surface) | Heavy RAG over **code**, not chat history | RAG over code, not chat history | Partial — Enterprise admin/team management; **chat history itself is per-user; no team chat search** | Proprietary | Enterprise SKU | LOW (closed; no documented export API for transcripts; reinforces gap pattern) | web-08 (sourcegraph.com/docs/cody/enterprise/features) |
| **JetBrains AI Assistant** | IDE plugin | Per-project chat history persists across IDE sessions (local) | Standard code-aware retrieval; no chat-history search | No (over chat) | **Not documented** — no first-party "team chat search" in 2025 releases | Proprietary | JetBrains licensing | LOW — pipeline-with as future capture source | web-08 (jetbrains.com/help/ai-assistant/chat-mode.html) |
| **Tabnine** | SaaS + private deployment / on-prem | Closed chat surface; **Enterprise Context Engine** RAG over team code | Code-RAG via Enterprise Context Engine | RAG over **team code**, not chat history | Yes — shared commands/rules; team feature set is **shared customization**, not transcripts | Proprietary | Enterprise licensing | LOW (closed chat persistence; bespoke export only) | web-08 (docs.tabnine.com/, globenewswire 2025-11-05 Enterprise Context Engine launch) |
| **Codeium / Windsurf Cascade** | IDE plugin (Windsurf) | **Cascade Memories** (workspace-local distilled facts); Rules/`AGENTS.md` for team-shared context | Memories retrieved by Cascade at runtime; no external RAG API | Memories at runtime | Partial — Rules/`AGENTS.md` explicitly recommended for team-shared; auto-Memories are local | Proprietary | Codeium/Windsurf licensing | MEDIUM — pipeline-with on write-side (`AGENTS.md`); ignore on chat-capture until export documented | web-08 (docs.windsurf.com/windsurf/cascade/memories) |
| **Devin / Cognition Labs** (Knowledge feature) | SaaS | Knowledge entries (curated org docs/instructions); **NOT searchable chat archives** | RAG over Knowledge | Yes over Knowledge entries; no documented RAG-over-chat-history surface | Yes — Knowledge is org-scoped | Proprietary | Enterprise SaaS | LOW — closed; **cleanest articulation of alternate philosophy**: "give agent curated org knowledge, don't mine raw transcripts" | web-08 (cognition.ai/, docs.devin.ai/enterprise/overview) |
| **Augment Code (Context Engine)** | SaaS | **Context Engine**: semantic index over team code, commit history, coding patterns, exposed via MCP/SDK/connectors | Hybrid (Context Engine) | Yes — over team code/patterns/commit history; **chat history not called out** | Yes — Context Engine team-scoped | Proprietary | Enterprise SaaS | MEDIUM — **closest competitor to "team RAG over everything engineering produces"**; if they ever ingest chat transcripts they become direct SpecStory competitor; further-investigation-needed | web-08 (augmentcode.com/context-engine/, docs.augmentcode.com) |

### 5.8.1 MCP Memory Servers — detailed survey (per web-08)

| Server | License/Storage | Source |
|--------|-----------------|--------|
| `@modelcontextprotocol/server-memory` | Knowledge-graph based; canonical reference impl; maintained by MCP org | web-08 (github.com/modelcontextprotocol/servers) |
| **Basic Memory** (cross-ref to 5.3) | Persistent semantic-graph memory backed by **local Markdown** files; Obsidian-compatible | web-08 (github.com/basicmachines-co/basic-memory) |
| **Memory Bank MCP (protocol-lattice)** | **Production-ready; vector-native; PostgreSQL/pgvector + Qdrant + MongoDB backends — strongest team-deploy posture** | web-08 (mcpservers.org/servers/protocol-lattice/memory-bank-mcp) |
| Memory Bank MCP (Roo Code variant) | File-based project context via structured markdown; less mature | web-08 (mcplane.com/mcp_servers/roo-code-memory-bankserver-1) |
| `mcp-memory-bank` (PyPI) | Python-package memory MCP, project-local | web-08 (pypi.org/project/mcp-memory-bank/) |
| Filesystem (reference) | Not memory per se; durable file substrate used by many memory tools | web-08 (github.com/modelcontextprotocol/servers) |
| TensorBlock awesome-mcp-servers (catalog) | Community-curated list; Knowledge & Memory section | web-08 (github.com/TensorBlock/awesome-mcp-servers) |
| MCP Registry (official) | Official discovery layer for MCP servers including memory | web-08 (modelcontextprotocol.io/registry) |

---

## 5.9 External Research Summary

### 5.9.1 Aggregate counts (products surveyed across 5.1–5.8)

| Metric | Count |
|--------|-------|
| Total products surveyed | ~60 distinct products/tools |
| HIGH relevance | ~22 (SpecStory, Cursor native, Continue Hub, Mem0, Zep, Graphiti, Cognee, SuperMemory, Langfuse, Helicone, Phoenix, Braintrust, Traceloop/OpenLLMetry, Onyx, Open WebUI, LibreChat, Glean, Notion, Confluence, Pieces, MCP Memory Servers, Spool — depending on cut) |
| MEDIUM relevance | ~23 (Letta, LangMem, Mastra Memory, Basic Memory, Cline Memory Bank, GroundRules, Continue Hub for chats, claude-replay, AnythingLLM, Coda AI, Slack AI, Slite, Outline, Guru, Lobe Chat, Khoj, Codeium/Windsurf, Augment Code, JetBrains AI, etc.) |
| LOW relevance | ~19 (Charlie Mnemonic, Chatbox, BetterChatGPT, Bloomfire, Cody, Tabnine, Devin, packmind, etc.) |
| OSS deployment available | ~35 products (Apache-2.0/MIT/BSD/AGPL) |
| SaaS-only / closed | ~15 products (Pinecone, Turbopuffer, Glean, Devin, Tabnine, Cody, LangSmith, Braintrust, HoneyHive, etc.) |
| Hybrid (OSS core + paid cloud / Enterprise self-host) | ~10 products (Mem0, Zep cloud + Graphiti OSS, Cognee, Pieces, Open WebUI, Onyx, Continue, Outline) |

### 5.9.2 Top 3-5 highest-relevance products for the user's goal (unified engineer-AI conversation context with RAG + team aggregation)

| Rank | Product | Why it's the highest-relevance match |
|------|---------|---------------------------------------|
| 1 | **SpecStory** (5.1) | Reference baseline; closest-named comparable; capture pipeline is solved; RAG and team are roadmap-only; user's stated reference point |
| 2 | **Onyx (Danswer)** (5.5) | Strongest **adopt-as-product** candidate: first-class JSON ingestion API + ACL-aware Vespa + connector framework + production storage stack; SpecStory transcripts map cleanly to document/section model |
| 3 | **Spool** (5.7) | Closest **direct precedent** for the use case: OSS pgvector locally + $25/user/mo paid cloud; supports Claude Code + Cursor; addresses ~80% of requirements; the build-vs-buy crossover anchor |
| 4 | **Graphiti (Zep OSS) + Mem0** (5.3) | Strongest **BYO storage+retrieval layer**: `add_episode_bulk` with timestamped episodes is the cleanest match for replaying `.specstory/history/`; Mem0's `add(messages)` API is the cleanest hosted/OSS option |
| 5 | **Pieces for Developers** (5.8) | Only adjacent tool whose architecture **genuinely overlaps**: cross-IDE/cross-browser AI chat capture + LTM + Enterprise self-host. Open question: team SKU + transcript export |

### 5.9.3 Architectural patterns observed (3-5)

| Pattern | What it means | Representative tools | Source synth |
|---------|---------------|---------------------|--------------|
| **Pattern 1 — Harvest-IDE-archive** | Read tool-specific local stores (Cursor `state.vscdb`, Copilot `chatSessions`, Claude Code `~/.claude/projects/*.jsonl`) and translate to uniform Markdown/JSON; one-way pipeline | SpecStory, claude-replay/CC Replay/vibe-replay, Cline Memory Bank (for derived state) | 5.1, 5.2, 5.8 |
| **Pattern 2 — Proxy-LLM-call** | Sit in front of provider API as a transparent proxy; capture every request/response by base-URL change | Helicone (`api.anthropic.com` → `anthropic.helicone.ai`); applies to any tool supporting custom base URLs (Claude Code, Cursor, Continue, Cline, Aider) | 5.4 |
| **Pattern 3 — Instrument-LLM-call (OTLP)** | Emit OpenTelemetry/OpenLLMetry spans from the calling tool; backend-agnostic; replayable | Langfuse, Phoenix, Opik, Laminar, Traceloop/OpenLLMetry (de-facto standard); Claude Code OTEL hooks | 5.4 |
| **Pattern 4 — Memory-CRUD beside the LLM** | Provide `add(messages, user_id)` / `add_episode_bulk` style API; arbitrary historical transcripts ingestible in batch; no LLM-call routing required | Mem0, Graphiti, Zep, Cognee, SuperMemory; convergent pattern across the field | 5.3 |
| **Pattern 5 — Enterprise-knowledge-ingestion** | Push transcripts as documents/pages/cards into existing org knowledge platform with permission-aware search and built-in RAG | Glean (custom datasource Indexing API), Notion API, Confluence Cloud REST v2, Outline (on-prem capable), Guru MCP server | 5.6 |
| **Pattern 6 — MCP-server-as-substrate** | Use an MCP memory server (knowledge-graph or vector) as the storage+retrieval substrate; agents read/write via MCP protocol | Memory Bank MCP (protocol-lattice) on pgvector/Qdrant; official `@modelcontextprotocol/server-memory`; Basic Memory; SuperMemory MCP; Guru MCP | 5.3, 5.8 |
| **Pattern 7 — Distilled-knowledge-not-transcripts** | Curate small, hand-maintained team rules / memory files / knowledge entries — explicitly the alternate philosophy to indexing raw chat | Cline Memory Bank, Cascade Memories, `AGENTS.md`/`.cursor/rules`, Devin Knowledge, Continue Hub, Tabnine personalization | 5.8 |
| **Pattern 8 — BYO RAG stack** | Vector DB + embedding API + pipeline tool, often pgvector + Voyage code-3 + LlamaIndex/Haystack; ~$310/yr, 4-6 weeks build | Spool (precedent), AWS multi-tenant pgvector ref arch, Azure secure multi-tenant RAG, ChatRAG | 5.7 |

### 5.9.4 Universal gaps observed across the landscape

| Gap | Evidence | Source |
|-----|----------|--------|
| **None of the OSS chat platforms ship native semantic RAG over the user's own past chats** | Open WebUI, LibreChat, AnythingLLM, Onyx, Lobe Chat, Khoj — every platform treats RAG as "chat with uploaded documents"; chats stored but **not auto-indexed for retrieval** | web-05 finding (5.5) |
| **No mainstream code-AI vendor ships a team-shared, indexed, RAG-capable chat-history product** | Cody, Tabnine, Devin, Augment, JetBrains AI — every major IDE-AI keeps chat history per-user/local; cross-device sync is forum request even for Cursor; "team chat search" not in any vendor's GA roadmap | web-08 (5.8); web-02 (5.2) |
| **No memory-layer product *requires* LLM-call routing through itself** — they sit beside the LLM | Mem0, Letta, Zep, Graphiti, Cognee, LangMem, SuperMemory, Mastra all expose `add()` / `add_episode_bulk` style data-shaped APIs | web-03 (5.3) |
| **No observability platform harvests IDE-side artifacts natively** — they all expect API call site | LangSmith, Langfuse, Helicone, Phoenix, HoneyHive, Braintrust, PromptLayer, W&B Weave, Opik, Lunary, AgentOps, Traceloop, Laminar — all 13 surveyed | web-04 (5.4) |
| **Tool-call-aware ingestion is rare in pipeline tools** — naive 512-token chunkers break `tool_call_id` ↔ `tool_call_result` linkage | Haystack and LlamaIndex preserve structure; LangChain's default loaders historically flatten it | web-07 (5.7) |
| **SpecStory itself does NOT ship RAG today** — roadmap-only | docs.specstory.com FAQs explicitly state "import history into editor: NOT SUPPORTED"; beta.specstory.com surfaces "memory retrieval" / "AI knowledge base" as coming-soon only `[I2]` | web-01 (5.1) |
| **No multi-tool, team-shared chat-archive product directly competes with SpecStory across all four pillars** (multi-tool capture + search + team share + rules-derivation) | Closest matches are either single-IDE (CursorShare, claude-replay, GroundRules) or adjacent in concept (Pieces OS-wide, Continue Hub configs, AnythingLLM chat-with-docs) | web-02 (5.2) |
| **The dominant industry pattern is *distilled knowledge*, not *raw chat archives*** — SpecStory's thesis is contrarian | Cline Memory Bank, Cascade Memories, `AGENTS.md`/`.cursor/rules`, Devin Knowledge, Tabnine personalization, Augment Context Engine — all curated/distilled approaches | web-08 (5.8) |

---

## 6. Options Analysis

The research surfaces five architecturally distinct paths to the stated goal — a unified, indexed, searchable, RAG-capable database of all engineer-AI conversation context across the team. They are evaluated below against the same six aspects, then compared head-to-head in the comparison table that follows.

### Option A — Adopt SpecStory + wait for shipped RAG roadmap

Use the SpecStory CLI/extension as the multi-tool capture layer (already covers Cursor, Copilot, Claude Code, Codex CLI, Cursor CLI, Droid CLI, Gemini CLI per `web-01`), sync to SpecStory Cloud for hybrid lexical + semantic search, and rely on SpecStory's "AI knowledge base / memory retrieval coming soon" roadmap to deliver RAG context-injection.

| Aspect | Assessment |
|--------|-----------|
| Effort | XS (install CLI + extensions; `specstory login`; `specstory sync`) |
| Risk | High |
| Reuse of existing tools | Full — SpecStory ingests directly from the team's existing AI tools without modification (Cursor `state.vscdb`, Claude Code `~/.claude/projects/*.jsonl`, Copilot `chatSessions`, etc., per `web-01`). |
| Files/systems affected | Each engineer's machine: install `specstory` binary + IDE extensions; nothing in the team repo or shared infra. |
| Pros | (1) Multi-tool capture is solved (7 tools, per `web-01`). (2) Hybrid lexical + semantic cloud search ships today. (3) Cloud REST + GraphQL API exist for downstream integrations. (4) OSS CLI providers under Apache-2.0; capture remains usable even if cloud product changes. (5) Local Markdown corpus at `.specstory/history/*.md` is reusable by any future architecture (per `web-01` Recommendation 2). |
| Cons | (1) RAG is roadmap-only — no shipping retrieval-into-prompt feature today (`web-01`, gap I2). (2) Team workspace is roadmap-only — single-user workspaces today; "team collaboration" is on the roadmap but no RBAC/audit-log documented (`web-01`). (3) Pricing is unobtainable — `/pricing` 404s, Teams page is a Design Partner application, no paid SKU publicly purchasable (`web-01`, gap I1). (4) Cloud server and IDE extensions are closed-source — vendor lock-in risk (`web-01`). (5) Capture fidelity is per-tool and "may change" — structural risk for downstream consumers (`web-01` Recommendation 5). (6) Round-trip back into editor chat is explicitly NOT supported — one-way pipeline (`web-01`). (7) Cursor itself shipped `/Generate Cursor Rules from chat history` in v0.49 — overlaps SpecStory's headline feature and may shrink TAM (`web-02`). |

### Option B — Adopt a memory-layer product as storage+RAG backend

Build a thin ingestion layer that reads the team's native AI-tool storage (Cursor SQLite, Claude Code JSONL, Cline JSON, Codex JSONL, etc., per `01-native-storage-formats.md`) and pushes structured episodes into a memory-layer product. Top candidates from `web-03` are Graphiti (OSS, `add_episode_bulk` is "the cleanest direct match" for replaying timestamped historical conversations), Mem0 (Apache-2.0, `memory.add(messages, user_id=...)` accepts arbitrary historical message arrays), Zep cloud (managed Graph-RAG, BYOC for enterprise), and SuperMemory (the only memory-layer product with first-party Cursor / Claude Code / VS Code / Windsurf integrations).

| Aspect | Assessment |
|--------|-----------|
| Effort | M (write per-tool ingestion adapters into a uniform message schema; configure memory-layer multi-tenancy; build minimal search UI / MCP exposure) |
| Risk | Medium |
| Reuse of existing tools | High — keeps each engineer's existing AI tool unchanged (Cursor, Claude Code, Cline, etc. continue to write to their native locations); the ingestion layer reads from those locations on a schedule. |
| Files/systems affected | New ingestion service (per-tool adapters → memory-layer client); memory-layer deployment (self-host Graphiti on Neo4j/FalkorDB, or Mem0 self-host, or hosted Zep/SuperMemory); minimal search UI or MCP server. No changes to the AI tools themselves. |
| Pros | (1) Shipping RAG today — Mem0 and Graphiti have production retrieval; Zep is managed Graph-RAG; SuperMemory has IDE-side RAG injection (`web-03`). (2) Permissive OSS for the leading candidates — Apache-2.0 (Mem0, Graphiti, Cognee, Letta) or MIT (LangMem, SuperMemory) (`web-03`). (3) Batch ingestion of arbitrary historical transcripts is supported by most products as a side effect of an open `add()` API — Mem0, Graphiti, Cognee, SuperMemory, Zep all accept this (`web-03`). (4) Multi-tenancy is solved via `user_id`/`agent_id`/`group_id`/namespace patterns; "unlimited users" is typical pricing posture (`web-03`). (5) None of these products *requires* LLM-call routing through itself — all sit beside the LLM, opposite of observability proxies (`web-03`). (6) SuperMemory uniquely ships first-party Cursor/Claude Code MCP integration if IDE-side injection is a hard requirement (`web-03`). |
| Cons | (1) Ingestion glue is still required — per-tool adapter for each of 9 native storage formats (`01-native-storage-formats.md`: JSONL, SQLite, Markdown, JSON-files, hashed-temp variants); "9 codecs into 1 schema" is the universal cost. (2) Search UI is unbundled in the OSS options — Graphiti and Mem0 self-host ship retrieval APIs, not engineer-friendly UIs (`web-03`). (3) IDE integration is rare across the field — only SuperMemory has first-party plugins; others rely on generic MCP adapters or framework SDKs (`web-03`). (4) Letta and Mastra are agent runtimes with bundled memory, not memory layers — they do not naturally accept replay of captured chats (`web-03`). (5) Hosted-tier pricing scales with usage credits, not seats — at engineering-team scale Pro tiers are $19-$249/mo for Mem0, $125-$375/mo for Zep, $19-$399/mo for SuperMemory (`web-03`). |

### Option C — Adopt an LLM observability platform

Capture engineer-AI traffic at the API call site, either via a forward proxy (Helicone — change `ANTHROPIC_BASE_URL`) or via OTLP/OpenLLMetry instrumentation (Langfuse, Phoenix, Opik, Traceloop). Phoenix has the only community-documented playbook for migrating archived user conversations into traces (`web-04`); the others can replay archives via SDK/REST but require custom adapter code.

| Aspect | Assessment |
|--------|-----------|
| Effort | S-M (proxy: change one env var per engineer for the proxy variant; OTLP: per-tool instrumentation where tools support it, custom replay shim for archives) |
| Risk | Medium |
| Reuse of existing tools | High — Claude Code has first-class Langfuse and Helicone integrations; Cursor has Langfuse + Helicone integrations; Traceloop launched an MCP server in Dec 2025 specifically to bring OpenTelemetry into Cursor and Claude Code workflows (`web-04`). Cline/Aider/Continue support custom base URLs so Helicone proxy mode covers them. |
| Files/systems affected | Proxy variant: each engineer's tool config (env var); team-deploys self-hosted Helicone backend. OTLP variant: per-tool OTEL hook configuration; team-deploys self-hosted Langfuse or Phoenix. Optional: SpecStory→Langfuse `/api/public/ingestion` shim, or Phoenix's documented chat-archive-to-trace migration. |
| Pros | (1) Shipping search/dataset/RAG-export — Langfuse Datasets API, Braintrust BTQL/SQL, Phoenix datasets + community import guide (`web-04`). (2) Multiple permissive OSS leaders — Apache-2.0 self-host for Helicone, Phoenix, Opik, Laminar, Lunary; MIT core for Langfuse with EE for advanced RBAC/audit (`web-04`). (3) Team aggregation is native and mature — orgs/projects/RBAC across the field (`web-04`). (4) Phoenix has the only community-documented historical ingest path of any candidate in the entire research corpus (`web-04`). (5) Helicone proxy mode = lowest engineering lift for forward capture; works for any tool that supports custom base URL (Claude Code, Cursor, Continue, Cline, Aider all do per `web-04`). (6) OpenLLMetry as transport keeps backend swappable. |
| Cons | (1) Instrumentation-side by default — these platforms expect to sit at the API call site, not harvest IDE archives (`web-04`). Forward-only without an explicit replay shim. (2) Cline/Aider/Continue lack first-class observability-platform plugins; they rely on proxy-mode or user-code SDK glue (`web-04`). (3) None of these platforms harvests IDE-side artifacts natively — SpecStory's architectural niche is not duplicated (`web-04`). (4) Proxy outage = no LLM (Helicone variant) — must run HA. (5) Search UX varies — Braintrust SQL/BTQL is unmatched but closed-source; Langfuse/Phoenix are open but UI-filters + full-text + semantic only (`web-04`). (6) Phoenix self-host is single-tenant by default; multi-tenant requires Arize AX paid product (`web-04`). |

### Option D — BYO: pgvector + Voyage code-3 + LlamaIndex + custom ingestion adapters

Assemble a minimal stack from the components surveyed in `web-07`: pgvector on existing or Supabase Pro Postgres for storage, Voyage `voyage-code-3` embeddings (`web-07` reports +13.8% over OpenAI text-embedding-3-large on code retrieval per Voyage's own benchmark wording — see gap I5), LlamaIndex's `ChatStore`/`ChatMessage` abstraction for tool-call-aware ingestion, and per-tool adapters for the 9 native formats catalogued in `01-native-storage-formats.md`.

| Aspect | Assessment |
|--------|-----------|
| Effort | L (4-6 weeks team-ready per `web-07`; 9 ingestion adapters; chunking that preserves tool_call_id ↔ tool_call_result linkage; multi-tenant auth; eval harness; re-embed pipeline) |
| Risk | Medium-High |
| Reuse of existing tools | Maximum — everything runs against the team's existing AI tools' native storage with no behavioral change; Postgres likely already in the stack. |
| Files/systems affected | New service repo (ingestion + embedding + retrieval + minimal UI/MCP); Supabase Pro or existing Postgres + pgvector extension; Voyage API key; LlamaIndex pipeline code; eval harness with golden-set queries. |
| Pros | (1) Lowest recurring OPEX — `web-07` cost-models recommended baseline at ~$310/yr for a 10-engineer team (Supabase Pro $300 + Voyage code-3 $9 + LlamaIndex free); cheapest stack on existing Postgres ~$1/yr. (2) Full control over ingestion fidelity — adapters can preserve tool-call structure that SpecStory's "lossy-by-default" Markdown conversion drops (`web-01` capture summary; `web-07` recommendation 5). (3) Exact fit for the team's tools — adapter set sized to actual Claude Code / Cursor / Cline mix (`01-native-storage-formats.md`). (4) Apache-2.0/MIT throughout — no vendor lock-in (LlamaIndex MIT, pgvector PostgreSQL license, Voyage SDK permissive). (5) pgvector closed the perf gap in 2024-2025 with pgvectorscale + HNSW maturity; competitive at <50M vectors (`web-07`). (6) Voyage code-3's code-retrieval lead is meaningful for engineer-AI archives. |
| Cons | (1) Largest upfront cost — at $200k/yr loaded engineer, 4-6 weeks build = $30-100k engineer-time vs. $25/user/mo × 10 × 24 months = $6k for hosted alternatives (`web-07` recommendation 7). (2) Hidden complexity: tool-call-preserving chunking (1-2 weeks), incremental dedup via `SQLRecordManager` pattern, multi-tenant policy, eval harness, GDPR/redaction (`web-07`). (3) Re-embed cost on model upgrade is the largest amortized cost — budget 2-4x steady-state every ~12 months (`web-07`). (4) Ongoing maintenance ~1 day/week stable state for the recommended baseline (`web-07`). (5) Spool already does ~80% of this for $25/user/mo (`web-07` recommendation 3) — buy-vs-build math hinges on whether the team needs (a) air-gap, (b) custom integrations beyond Spool's coverage, or (c) tool-call-structure that Spool may not preserve. (6) Some load-bearing claims in `web-07` are flagged `[UNVERIFIED]` (Voyage/MongoDB acquisition, Turbopuffer customers, Mastra 10x cost reduction — see gap I4). |

### Option E — Hybrid: harvest-archive + forward-capture + unified backend

Run two ingestion pipelines into a single shared store. Harvest path: SpecStory-style scrape of IDE-side artifacts (covers free-tier Cursor chats, `.specstory/history/*.md`, Claude Code `~/.claude/projects/*.jsonl`, Cline `tasks/<id>/api_conversation_history.json`, etc., per `01-native-storage-formats.md`). Forward path: Helicone-style proxy or OpenLLMetry instrumentation for everything going to provider APIs from then on. Both pipelines write into one backend — Phoenix (uses its documented chat-archive-to-trace migration), Langfuse (custom adapter to `/api/public/ingestion`), Graphiti (`add_episode_bulk` for batch + incremental for live), or pgvector with LlamaIndex orchestrating both ingest paths. This is the "probably superior" path explicitly flagged in `web-04` recommendation 4.

| Aspect | Assessment |
|--------|-----------|
| Effort | L-XL (combines Option C forward-capture with archive ingestion adapters and a unified backend; eval harness; multi-tenant policy across two pipelines) |
| Risk | Medium |
| Reuse of existing tools | Maximum — harvest path leaves AI tools unchanged; forward path uses custom-base-URL or OTEL hooks the tools already support (`web-04`). |
| Files/systems affected | Harvest service (per-tool adapters into common schema); forward proxy or OTLP collector; unified backend (Phoenix or Langfuse self-host, or Graphiti on Neo4j, or pgvector); search UI / MCP server in front of backend. |
| Pros | (1) Covers both gaps the single-architecture options leave open — archive of past conversations (Option C alone misses this) AND forward capture from now on (Options A/D depend on per-tool adapter coverage that may lag behind tool releases). (2) Phoenix's community-documented migration playbook is the only turnkey archive-ingest path in the entire research corpus — making Phoenix-as-backend the de-risked choice for the historical pipeline (`web-04`). (3) Helicone proxy mode is the lowest-lift forward capture (single env var per engineer, covers all tools that support custom base URLs per `web-04`). (4) Unified backend means one search/retrieval API for downstream RAG/UI/MCP. (5) Backend-agnostic via OpenLLMetry — if backend choice changes, transport stays. (6) Graphiti's `add_episode_bulk` makes it the cleanest direct match if a temporal knowledge graph is desired (`web-03`). |
| Cons | (1) Highest engineering complexity — two ingest pipelines, schema reconciliation between them, dedup across overlapping captures (proxy + archive may capture the same conversation). (2) Backend must absorb both shapes (trace events from forward path; episode/document from archive path). (3) None of the candidate backends ships this hybrid out of the box — explicit integration work required. (4) Maintenance surface is larger than any single-architecture option. (5) Buy-vs-build math gets murky — much of the value can be obtained by doing Option C with Phoenix and accepting that pre-existing archives are best-effort. |

### Options Comparison

Cost figures use the 10-engineer team scale modelled in `web-07`. "Today" means shipping/usable as of 2026-05-01 per the cited research files; "roadmap" means announced but not shipping.

| Criterion | Option A (Adopt SpecStory) | Option B (Memory layer) | Option C (Observability) | Option D (BYO pgvector) | Option E (Hybrid) |
|---|---|---|---|---|---|
| Cost (build + 1yr ops) | $0 build; ops unobtainable (Design-Partner gated, gap I1) | $0–$5k build (adapter glue) + hosted $228–$2,988/yr (Mem0 Pro $19/mo–$249/mo, Zep Flex $125/mo–$375/mo, SuperMemory $19/mo–$399/mo per `web-03`) or self-host infra | Self-host: ~$5k build + ~$1–5k/yr infra (Helicone/Langfuse/Phoenix Apache-2.0 or MIT). Cloud: Langfuse Core $59/mo+, Helicone Pro $79/mo+ (`web-04`) | $30–100k engineer-time build (4–6 weeks) + ~$310/yr OPEX recommended baseline (Supabase Pro $300 + Voyage code-3 $9, per `web-07`) | $40–120k engineer-time (combines C + archive adapters) + ~$1–5k/yr infra |
| Time-to-Value | Days (install + sync); but RAG never arrives without vendor delivering roadmap | 2–4 weeks (adapter + memory-layer wiring) | Forward capture: hours (proxy) to days (OTEL); archive ingest: 1–2 weeks for Phoenix path, longer for others | 4–6 weeks team-ready (`web-07`) | 6–10 weeks team-ready |
| Flexibility | Low — capture mechanics are vendor-controlled, "may change" per tool (`web-01`) | High — open `add()` APIs; can swap memory layer behind ingestion abstraction | High — OpenLLMetry transport keeps backend swappable (`web-04`) | Maximum — every component is replaceable | Maximum — both pipelines and backend are decoupled |
| Vendor lock-in | High — closed cloud + closed IDE extensions; no SDK shipped yet (`web-01`) | Low for OSS path (Graphiti/Mem0/Cognee Apache-2.0); Medium for hosted (Zep/SuperMemory) | Low — Apache-2.0 self-host across 5 OSS leaders (Phoenix, Opik, Helicone, Laminar, Lunary); MIT core for Langfuse (`web-04`) | None — Apache-2.0/MIT throughout | None — same as D, plus backend swappable via OpenLLMetry |
| Engineering effort | XS | M | S–M | L | L–XL |
| RAG capability today | No — roadmap-only ("AI knowledge base coming soon", `web-01`, gap I2) | Yes — Mem0/Graphiti/Zep/SuperMemory all ship retrieval (`web-03`) | Partial — datasets/eval/export ship; "RAG re-injection" requires user code on most platforms (`web-04`) | Yes — assembled by definition | Yes — backend choice dictates |
| Team aggregation today | No — single-user workspaces; team is roadmap-only, no RBAC/audit-log documented (`web-01`) | Yes — `user_id`/`group_id`/namespace patterns; "unlimited users" pricing posture (`web-03`) | Yes — orgs/projects/RBAC native and mature (`web-04`) | Yes — pgvector RLS or tenant-id column; multi-tenancy is the build choice | Yes — inherits backend's team model |
| Self-host option | No — cloud is closed; only CLI/providers OSS (`web-01`) | Yes — Graphiti, Mem0, Cognee, LangMem, Letta all self-hostable (`web-03`); SuperMemory partial | Yes — Helicone, Langfuse, Phoenix, Opik, Laminar, Lunary all self-hostable (`web-04`) | Yes — pgvector + LlamaIndex run anywhere | Yes — depends on backend (Phoenix/Langfuse/Graphiti/pgvector all self-hostable) |
| OSS license available | Partial — Apache-2.0 CLI + providers; Cloud + IDE extensions closed (`web-01`) | Yes — Apache-2.0 (Mem0, Graphiti, Cognee, Letta, Cline core); MIT (LangMem, SuperMemory) (`web-03`) | Yes — Apache-2.0 leaders (Phoenix, Opik, Helicone, Laminar, Lunary); MIT core for Langfuse (`web-04`) | Yes — pgvector + LlamaIndex MIT/permissive (`web-07`) | Yes — same as backend choice |

---

## 7. Recommendation

**Recommended option: Option E — Hybrid (harvest-archive + forward-capture + unified backend), with Phoenix as the backend, Helicone proxy as the forward-capture path, and a SpecStory-style harvest adapter set as the archive-ingest path.**

If the team's engineering capacity does not support the L–XL effort of Option E in a single phase, the recommended sequencing is: ship Option C first (Phoenix + Helicone proxy = forward capture from day one with shipping team-aggregation, RAG-export, and self-host), then add the harvest path on top to upgrade in place to Option E. Option C is the largest subset of Option E that still satisfies the four hard requirements (unified, indexed, searchable, RAG-capable) on its own.

### Rationale (with explicit references to comparison-table cells)

1. **The "RAG capability today" cell rules out Option A as the primary path.** SpecStory's RAG roadmap explicitly does not ship — `web-01` could not verify any shipping retrieval-into-prompt feature, and the only public references ("AI knowledge base / memory retrieval coming soon") are on a host that returned ECONNREFUSED at research time (gap I2). The user's stated objective — "efficiently indexed and searched and used as context for all future conversations" — explicitly requires the capability SpecStory itself lists as not-yet-shipped. SpecStory remains valuable as a *capture* baseline (its multi-tool capture is its hardest engineering problem, per `web-01` recommendation 1) but cannot be the RAG primitive on its own.

2. **The "Team aggregation today" cell separates the credible options.** SpecStory has single-user workspaces only (`web-01`); team workspace, RBAC, and audit log are all on the roadmap with no published timeline. Options B, C, D, and E all ship team aggregation today: memory layers via `user_id`/`group_id` partitioning (`web-03`), observability platforms via mature orgs/projects/RBAC (`web-04`), BYO via pgvector RLS or tenant-id columns (`web-07`), and Hybrid via whichever backend is chosen. For an engineering team's unified-context goal, "team aggregation today" is not optional — it is the goal — which moves Option A to "wait-and-see" rather than "adopt."

3. **The "Engineering effort" and "Cost (build + 1yr ops)" cells together explain why Option E with Phoenix is preferred over Option D pure BYO.** Option D pure BYO requires 4–6 weeks team-ready (`web-07`) and re-implements work that Phoenix already ships — sessions/threads, multi-project aggregation, dataset/RAG export, OTEL ingestion, semantic search over inputs/outputs, and crucially a *community-documented chat-archive-to-trace migration playbook* (`web-04`, the only turnkey historical-ingest path in the entire research corpus). Option E with Phoenix as backend reuses all of that — the team only writes the harvest-side adapters and the forward-capture proxy config. The build effort delta vs. Option C alone is the harvest adapters; in exchange you get full coverage of pre-existing archives, which is precisely the corpus the team has accumulated to date.

4. **The "Vendor lock-in" and "OSS license available" cells make Phoenix and Helicone safe choices.** Both are Apache-2.0, both self-hostable, and OpenLLMetry as transport keeps the backend swappable later if Phoenix is outgrown (`web-04`). This avoids the vendor risk that Option A inherits from SpecStory's closed cloud + closed IDE extensions and the partial lock-in of hosted memory-layer products in Option B. The five Apache-2.0 OSS leaders (Phoenix, Opik, Helicone, Laminar, Lunary) form a "preferable-for-we-own-the-data" group identified explicitly in `web-04` recommendation 5.

5. **The "Flexibility" cell justifies the dual-pipeline cost.** A single-pipeline architecture commits the team to one capture mode forever — proxy mode misses tools that don't support custom base URLs and misses any past corpus; OTEL misses tools without OTLP support today (Cline/Aider/Continue per `web-04`); harvest-only misses ephemeral conversations and lags new tool versions. Option E's dual-pipeline tolerates per-tool gaps in either path because the other can compensate, and `web-04` recommendation 4 explicitly identifies this hybrid as "probably superior" — a SpecStory-style harvester for IDE-side artifacts plus Helicone/Langfuse for forward API-side capture combines the strengths of Bucket A and Bucket C.

### Addressing the two judgment calls from `research-notes.md` AMBIGUITIES_FOR_USER

**(a) Whether LLM observability platforms count as comparables — yes.** They are a different *architecture* (instrument the LLM call path vs. harvest existing IDE chat archives) but converge on the same *end-state* the user is asking for: a unified, indexed, searchable, RAG-capable conversation database with team aggregation. `web-04` confirms this — Claude Code and Cursor have first-class integrations with Langfuse and Helicone today; Traceloop launched an MCP server in Dec 2025 specifically targeting Cursor and Claude Code; Phoenix has a community-documented playbook for migrating archived conversations into traces. The end-state outcome is identical to what a SpecStory-RAG product would deliver if SpecStory shipped its roadmap. Excluding observability platforms would have hidden the option that this recommendation is built on.

**(b) Interpretation of "unified single database" — one pipeline assembling many sources into a shared store, not one product covering everything.** The research evidence is decisive: every native AI-tool storage format is different (`01-native-storage-formats.md` documents 9 formats — JSONL, SQLite, Markdown, JSON-files, hashed temp directories), no single product captures all 9 sources today (SpecStory captures 7 but loses tool-call fidelity in the Markdown conversion per `web-01`), and the convergent industry pattern is "data-shaped ingestion, not product-shaped" — every credible memory-layer product treats ingestion as message-array or episode input rather than requiring LLM-call routing through itself (`web-03` finding). The recommendation therefore selects a *pipeline* (harvest + forward) that *converges on* a *shared store* (Phoenix). This matches how Cursor, Claude Code, Cline, Aider already work — each tool keeps its native format; the unified layer is the indexed/searchable/RAG-capable backend that all of them feed.

### Trade-offs being accepted

- **Engineering effort up front.** Option E is L–XL effort. The team accepts 6–10 weeks team-ready in exchange for full archive coverage, full forward coverage, and shipping team aggregation + RAG today. The alternative — Option A's XS effort — buys nothing the user asked for because the RAG and team capabilities are not shipping (`web-01`, gap I2).
- **Two ingestion pipelines to maintain.** Schema reconciliation between trace-shaped forward events and episode-shaped harvest documents is real work. Mitigation: use Phoenix's native session/trace model for both sides (forward path emits OTLP spans; harvest path uses the documented chat-archive-to-trace migration that `web-04` cites) so the backend sees one shape.
- **Forward-capture has an outage failure mode in proxy variant.** If Helicone proxy is down, Claude Code calls fail (Helicone sits between client and Anthropic). Mitigation: deploy Helicone HA, or use OTLP path (Phoenix is non-blocking) for tools that support it, and reserve proxy mode for tools that don't.
- **Dedup across overlapping captures.** Proxy + harvest may both record the same conversation. Mitigation: content-addressed dedup (SHA over message arrays); the `SQLRecordManager` pattern from LangChain is the standard reference here per `web-07`.
- **Phoenix self-host is single-tenant by default.** Multi-tenant requires the paid Arize AX product (`web-04`). Mitigation: at engineering-team scale (10–50 engineers), single-tenant is sufficient; revisit if the deployment grows beyond one team.
- **Re-embed cost on model upgrade.** When the chosen embedding model (e.g., Voyage code-3 if Phoenix's vector store is fed Voyage embeddings) releases a new version, full re-embed is required; budget 2–4x steady-state embedding cost annually per `web-07` recommendation. At 10-engineer scale this is still a rounding error in absolute terms ($9–$36/yr).
- **SpecStory may ship its team + RAG roadmap inside the build window.** If it ships during the 6–10 week build, Option A becomes credible mid-build. Mitigation: design Option E's harvest path to read directly from `.specstory/history/*.md` (already a uniform Markdown corpus per `web-01`) so SpecStory's capture work is reused regardless of whether SpecStory ships its own RAG; this matches `web-01` recommendation 2 ("any custom architecture can adopt SpecStory as the *capture layer*… and bolt its own RAG/memory/team layer on top").

---

## 8. Implementation Plan

### Architecture Assumed (Option E — Hybrid)

This plan assumes the recommended Option E architecture: harvest existing IDE-side conversation archives (covering Claude Code, Cursor, Aider, Cline, Roo Code, Continue.dev, Copilot CLI, Codex CLI, Gemini CLI) into a normalized canonical schema; layer optional forward-capture (Helicone proxy and/or OTLP/OpenLLMetry instrumentation per `web-04-observability-platforms.md`) for going-forward LLM API traffic; persist into a self-hostable storage tier (default: pgvector on Postgres/Supabase per `web-07-byo-rag-stack.md`; alternative: Arize Phoenix as observability-native ingestor per `web-04`; alternative: Mem0 / Zep-Graphiti / Cognee as memory-layer products per `web-03-memory-layer.md`); expose retrieval via a thin RAG API and an MCP server for IDE integration (pattern attested by Helicone MCP, Traceloop OpenLLMetry MCP, OpenMemory MCP, Claude Historian MCP per `web-03`, `web-04`, `web-07`).

The plan is staged so each phase produces a verifiable artifact. Phases 1-3 are mandatory for any usable system; Phase 4 (team aggregation) and Phase 5 (IDE integration via MCP) are the differentiators against existing single-user OSS precedents (Spool, claude-history, MyChatArchive, Claude Historian MCP per `web-07`).

---

### Phase 1 — Foundation: Data Ingestion Pipeline + Canonical Schema

**Goal:** Land every supported tool's native conversation artifact into a single normalized JSONL+SQLite stream, addressable by `(tool, repo_root, session_id, message_id)`, with tool-call structure preserved (per `web-07` finding 5 — naive chunkers shred tool-call/tool-result pairs; per `01-native-storage-formats.md` Key Takeaways — tool calls universally captured but never normalized).

**Dependencies:** None — this is the seam everything else attaches to.

**Step table:**

| Step | Action | Files | Details |
|------|--------|-------|---------|
| 1.1 | Define canonical message schema (Pydantic) capturing fields seen across all 9 tools | new file: `src/unified_chat/schema/canonical.py` | Fields: `tool` (enum: claude_code, cursor, aider, continue_dev, cline, roo_code, copilot_cli, gemini_cli, codex_cli), `tool_version`, `session_id`, `parent_uuid` (Claude Code), `message_id`, `timestamp` (ISO8601 UTC), `role` (user/assistant/tool/system), `content_blocks` (typed list: text, thinking, tool_use, tool_result, file_edit), `model`, `usage` (input/output/cache_creation/cache_read tokens), `cwd`, `git_branch`, `repo_root`, `repo_id` (canonical hash), `attribution_skill`, `attribution_plugin`, `is_sidechain`. Schema derived from richest superset (Claude Code JSONL per `01-native-storage-formats.md` Claude Code section) — leaner tools get NULL for fields they do not emit. |
| 1.2 | Implement Claude Code JSONL adapter | new file: `src/unified_chat/adapters/claude_code.py` | Walk `~/.claude/projects/<slugified-cwd>/*.jsonl`. For each line: parse JSON, map `type`/`message.role`/`message.content` blocks (including `thinking` with encrypted `signature`, `tool_use`, `tool_result` per `01-native-storage-formats.md` Claude Code lines 16-20). Reverse the cwd-slug to recover `repo_root` (`-` → `/`). Preserve `parentUuid` lineage. Emit canonical messages. Skip `queue-operation` events or carry as `system` role with subtype. |
| 1.3 | Implement Codex CLI JSONL adapter | new file: `src/unified_chat/adapters/codex_cli.py` | Walk `$CODEX_HOME/sessions/YYYY/MM/DD/rollout-*.jsonl` (default `~/.codex/sessions/`). Each line is `{timestamp, item: RolloutItem}` with `RolloutItem` variants `SessionMeta`, `TurnContext`, `ResponseItem`, `EventMsg`, `Compacted` per `01-native-storage-formats.md` Codex section. Use `SessionMeta.cwd`/`provider`/CLI version as session header; emit `ResponseItem.tool_calls` as canonical `tool_use` blocks. Read sibling `state.sqlite` for index hints if present. |
| 1.4 | Implement Copilot CLI JSONL+SQLite adapter | new file: `src/unified_chat/adapters/copilot_cli.py` | Walk `~/.copilot/session-state/<sessionId>/*.jsonl` (override via `$COPILOT_HOME`) for transcripts. Open `~/.copilot/session-store.db` (SQLite) read-only and JOIN session metadata onto JSONL lines by `sessionId`. Field-level schema is undocumented per `01-native-storage-formats.md` Copilot CLI section — adapter must tolerate column drift; flag `[UNVERIFIED]` keys in canonical `raw_extra` blob. |
| 1.5 | Implement Cursor SQLite-blob adapter | new file: `src/unified_chat/adapters/cursor.py` | Open `~/Library/Application Support/Cursor/User/workspaceStorage/<workspaceHash>/state.vscdb` (mac) / `~/.config/Cursor/User/workspaceStorage/<workspaceHash>/state.vscdb` (linux) / `%APPDATA%\Cursor\User\workspaceStorage\<workspaceHash>\state.vscdb` (win) and `…/User/globalStorage/state.vscdb`. Query `SELECT key, value FROM ItemTable WHERE key IN ('aiService.prompts', 'workbench.panel.aichat.view.aichat.chatdata', 'composer.composerData')` per `01-native-storage-formats.md` Cursor section. JSON-decode each blob; Cursor-version detector dispatches to per-version JSON-path extractors (gap I3-style; schema is version-coupled). Map `workspaceHash` → `repo_root` via Cursor's own mapping (sniff workspace.json siblings under same hash dir). |
| 1.6 | Implement Aider markdown adapter | new file: `src/unified_chat/adapters/aider.py` | Walk every git working tree under monitored repo roots; for each, read `<repo>/.aider.chat.history.md` plus `.aider.input.history` and (if present) `.aider.llm.history` per `01-native-storage-formats.md` Aider section. Parse session boundaries by `# aider chat started at <timestamp>` headers; user prompts at `#### ` headings; assistant body verbatim; extract SEARCH/REPLACE blocks as canonical `file_edit` content_blocks; pull commit SHAs from `Applied edit to <file>` lines and cross-reference git log for the commit-side persistence layer noted in `01-native-storage-formats.md` Aider Notes. |
| 1.7 | Implement Cline JSON-trio adapter | new file: `src/unified_chat/adapters/cline.py` | Walk `~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/tasks/<taskId>/` (mac), `~/.config/Code/User/globalStorage/saoudrizwan.claude-dev/tasks/<taskId>/` (linux), `%APPDATA%\Code\User\globalStorage\saoudrizwan.claude-dev\tasks\<taskId>\` (win); also Code-Insiders, JetBrains analog, and `~/.cline/data/tasks/<taskId>/` per `01-native-storage-formats.md` Cline section. For each task dir, read the trio: `api_conversation_history.json` (model-eye view → canonical), `ui_messages.json` (preserve as supplementary `ui_view` field on each message), `task_metadata.json` (session header). |
| 1.8 | Implement Roo Code adapter (Cline-fork delta) | new file: `src/unified_chat/adapters/roo_code.py` | Reuse Cline parser; substitute extension id `rooveterinaryinc.roo-cline` and add VS Code Server path `~/.vscode-server/data/User/globalStorage/rooveterinaryinc.roo-cline/tasks/<taskId>/` per `01-native-storage-formats.md` Roo Code section. Set canonical `tool=roo_code`. Per Roo Notes line 119, no other code change needed. |
| 1.9 | Implement Continue.dev JSONL adapter | new file: `src/unified_chat/adapters/continue_dev.py` | Walk `<project>/.continue/dev_data/*.jsonl` per `01-native-storage-formats.md` Continue.dev section. Honour the `schema` field on each line (versions `0.1.0`, `0.2.0`); dispatch per-version mappers for event categories `chat`, `autocomplete`, `tokens_generated`, `quickEdit`. For events with `data.destination` HTTP form, document a separate Phase 2.x path where Continue posts directly to our ingestion API instead of writing JSONL. |
| 1.10 | Implement Gemini CLI per-project-hash adapter | new file: `src/unified_chat/adapters/gemini_cli.py` | Walk `~/.gemini/tmp/<projectHash>/{chats/checkpoint-*.json, logs.json}` per `01-native-storage-formats.md` Gemini CLI section. `chats/checkpoint-*.json` is an array of `{role, parts}` objects (Google content-parts schema; `role` ∈ user/model). Map function-call `parts` to canonical `tool_use` blocks. Resolve `<projectHash>` back to a repo path by reading Gemini's internal mapping file; fall back to "unknown_repo" with the hash recorded if unresolvable (gap noted in `01-native-storage-formats.md` Gemini Notes). |
| 1.11 | Build the harvester orchestrator + watcher | new file: `src/unified_chat/harvester/orchestrator.py` | Each adapter exposes `discover() -> Iterable[SourceArtifact]` and `parse(SourceArtifact) -> Iterable[CanonicalMessage]`. Orchestrator dispatches in parallel (asyncio + per-tool worker pool). Two modes: (a) one-shot scan (`unified-chat ingest --once`), (b) inotify/FSEvents/ReadDirectoryChangesW watcher loop on the per-tool root paths. Idempotency keyed by `(tool, session_id, message_id)` → no double-write on rescan. |
| 1.12 | Tool-call-preserving chunker | new file: `src/unified_chat/chunking/tool_aware.py` | Per `web-07-byo-rag-stack.md` finding 5 + Hidden Complexity #1: naive 512-token chunkers break `tool_call_id` ↔ `tool_call_result` linkage. Implement chunker that respects message boundaries first, splits long assistant turns at content_block boundaries, and never separates a `tool_use` block from its matching `tool_result` (paired by `tool_use_id`). Default to LlamaIndex `ChatStore` semantics or Haystack `ChatMessage` semantics rather than `RecursiveCharacterTextSplitter` (per `web-07` Pipeline Tools section). |
| 1.13 | Canonical landing format + dedup ledger | new file: `src/unified_chat/storage/landing.py` (writes), `data/landing/<yyyy>/<mm>/<dd>/<tool>/*.jsonl` (output) | Each canonical message is appended to per-day, per-tool JSONL. SQLite sidecar `data/landing/_index.sqlite` records `(tool, session_id, message_id, content_hash, ingest_ts)` for incremental dedup — pattern derived from LangChain `SQLRecordManager` cited in `web-07` Hidden Complexity #3. Mirrors the Codex CLI / Copilot CLI dual JSONL+SQLite pattern noted as the emerging cross-tool best practice in `01-native-storage-formats.md` Key Takeaways. |
| 1.14 | Repo-identity resolver | new file: `src/unified_chat/identity/repo_resolver.py` | Per `01-native-storage-formats.md` Key Takeaways line 194: per-project hashing is inconsistent — Cursor `workspaceHash`, Gemini `projectHash`, Claude Code slugified cwd, Aider repo-relative, Cline/Roo VS Code globalStorage UUID. Resolver canonicalises each to a stable `repo_id` (default: SHA256 of `git remote get-url origin` if available, else SHA256 of absolute repo path). Resolver is a single bottleneck so all adapters call into it. |
| 1.15 | Redaction pre-processor | new file: `src/unified_chat/privacy/redactor.py` | Per `web-07-byo-rag-stack.md` Hidden Complexity #8 (GDPR / data retention — engineer transcripts may contain customer data, secrets, internal architecture). Run regex + entropy heuristics to redact API keys, JWT, AWS access keys, GitHub PATs, private keys; replace with stable hashes so retrieval can still match. Run BEFORE landing write, not after, to avoid retaining secrets on disk. |

---

### Phase 2 — Storage + Indexing Layer

**Goal:** Persist canonical messages into a queryable, embedded-vector + full-text store with multi-tenant scoping (per-engineer private + per-team shared, per `web-07` Hidden Complexity #5). Default substrate: pgvector on Postgres (per `web-07` Stack Recommendation Matrix "Team-of-10 baseline" row — pgvector on Supabase Pro + Voyage voyage-code-3 + LlamaIndex; ~$310/yr). Phoenix and Mem0/Zep-Graphiti are documented as alternatives but not Phase-2 default.

**Dependencies:** Phase 1 landing JSONL + ledger SQLite.

**Step table:**

| Step | Action | Files | Details |
|------|--------|-------|---------|
| 2.1 | Provision Postgres with pgvector + pgvectorscale | new file: `infra/postgres/init/01-extensions.sql`, `infra/postgres/init/02-schema.sql` | Enable `CREATE EXTENSION vector;` and `CREATE EXTENSION vectorscale;` (StreamingDiskANN per `web-07` pgvector entry). Create schema `unified_chat` with tables `sessions`, `messages`, `content_blocks`, `embeddings`, `repos`, `engineers`, `teams`. Use `tsvector` GENERATED column on message text for full-text. |
| 2.2 | Define embeddings table with HNSW index | edit `infra/postgres/init/02-schema.sql` | `embeddings(id, message_id, content_block_id, embedding vector(1024), model_id text, created_at)`. CREATE INDEX `embeddings_hnsw` USING hnsw (embedding vector_cosine_ops) WITH (m=16, ef_construction=64). Dimension 1024 matches Voyage voyage-code-3 / Cohere v3 / BGE-M3 / Jina v3 default per `web-07` Embedding APIs section. Reserve a parallel pgvectorscale `diskann` index for the same column to allow A/B between HNSW and StreamingDiskANN. |
| 2.3 | Multi-tenant scoping via Postgres RLS | edit `infra/postgres/init/02-schema.sql` (RLS clauses) | Per `web-07` Hidden Complexity #4 + ChatRAG multi-tenant reference architecture: enable Row-Level Security on `messages`, `content_blocks`, `embeddings`. Policies: `engineer_private` (filter by `engineer_id = current_setting('app.current_engineer')`), `team_shared` (filter by `team_id IN (...)`), `published_to_team` (engineer-owned but flagged `published=true`). Two indices per tenant pattern (private + shared) per `web-07` Hidden Complexity #5. |
| 2.4 | Embedding worker | new file: `src/unified_chat/embed/worker.py` | Consumes new rows from `messages` where `embedding IS NULL`. Default model: Voyage voyage-code-3 (per `web-07` finding 2 — +13.8% over OpenAI text-embedding-3-large on 32 code-retrieval datasets). Configurable to OpenAI text-embedding-3-large/small, Cohere Embed v3, Jina v3, BGE-M3 self-hosted (per `web-07` Embedding APIs catalog). Batches 64 chunks per request; respects voyage 32k token limit. Writes back to `embeddings` table with `model_id` so re-embed on model upgrade is tractable (per `web-07` Hidden Complexity #6). |
| 2.5 | Content-addressed dedup on ingest | edit `src/unified_chat/storage/landing.py` and add `src/unified_chat/storage/upsert.py` | UPSERT into `messages` keyed by `content_hash`. Hash = SHA256 of canonical normalized message (excluding wall-clock timestamps). Skips re-embed when row already exists. Pattern derived from LangChain `SQLRecordManager` cited in `web-07` Hidden Complexity #3. |
| 2.6 | Loader from landing JSONL → Postgres | new file: `src/unified_chat/storage/loader.py` | Reads `data/landing/<yyyy>/<mm>/<dd>/<tool>/*.jsonl`, runs Phase-1.12 chunker, runs Phase-1.15 redactor (idempotent if already done), upserts messages + content_blocks + tsvector + queues embedding. Streams in chunks of 1000; progress reported via SQLite ledger from 1.13. |
| 2.7 | Optional Phoenix alternative path | new file: `src/unified_chat/storage/phoenix_sink.py` | Per `web-04-observability-platforms.md` Arize Phoenix entry: Phoenix has the only community-documented "Migrating User Conversations to Traces in Phoenix" playbook. Implement a sink that converts canonical messages to OpenInference spans via `arize-phoenix-otel` and POSTs to a Phoenix OTLP endpoint. Used for teams that prefer Phoenix's semantic search + community import path over BYO pgvector. Mark `arize-phoenix-otel` license as `[UNVERIFIED — gap I7 from qa/gaps-and-questions.md]` — verify Apache-2.0 vs Elastic-2.0 per package before adoption. |
| 2.8 | Optional Mem0 / Zep-Graphiti / Cognee alternative path | new file: `src/unified_chat/storage/memory_layer_sink.py` | Per `web-03-memory-layer.md` Mem0/Graphiti/Cognee entries: each accepts batch-replay of historical messages without requiring LLM-call instrumentation (Mem0 `memory.add(messages, user_id=...)`, Graphiti `add_episode_bulk`, Cognee `add()` accepts strings/files/URLs/directories). Implement a single sink that writes canonical messages to whichever memory layer the operator selects. Mem0 self-host = Apache-2.0; Graphiti = Apache-2.0 (requires Neo4j or FalkorDB); Cognee = Apache-2.0. |
| 2.9 | Storage-layer selection guard | new file: `src/unified_chat/config/storage_choice.py` | Operator picks one of `pgvector` (default), `phoenix`, `mem0`, `graphiti`, `cognee`. Loader (2.6) dispatches accordingly. Per `web-07` finding 8 — multi-tenancy is solved differently per backend; pgvector RLS is the cleanest small-team path; Weaviate native MT and Qdrant payload-shard are documented alternatives if the team outgrows pgvector. |
| 2.10 | Idempotent re-embed pipeline (model-upgrade) | new file: `src/unified_chat/embed/reembed.py` | Per `web-07` Hidden Complexity #6: budget 2-4x steady-state embedding cost when Voyage releases voyage-4. Job re-embeds in tagged generations; old vectors retained until cutover; dual-index search supports rolling cutover. Operator-triggered via CLI: `unified-chat reembed --from voyage-code-3 --to voyage-code-4`. |
| 2.11 | Storage observability hooks | new file: `src/unified_chat/storage/metrics.py` | Counters: messages_ingested, dedup_skipped, embed_pending, embed_failed, redaction_hits. Exposed via Prometheus endpoint on the harvester process for ops. Required because `web-07` Hidden Complexity #7 calls out silent quality drift without an eval harness. |

---

### Phase 3 — Search and RAG Retrieval API

**Goal:** Expose hybrid (vector + BM25) search and a RAG-shaped retrieval endpoint over the storage layer. Pattern matches the strongest-fit findings from `web-07-byo-rag-stack.md` (LlamaIndex `ChatStore` + Haystack indexing/query pipeline separation) and the search/dataset story rated highest in `web-04-observability-platforms.md` (Braintrust BTQL + Langfuse Datasets + Phoenix semantic).

**Dependencies:** Phase 2 storage populated.

**Step table:**

| Step | Action | Files | Details |
|------|--------|-------|---------|
| 3.1 | FastAPI retrieval service skeleton | new file: `src/unified_chat/api/main.py` | Endpoints: `POST /search` (hybrid query), `POST /retrieve` (RAG — returns top-k snippets + citations), `GET /sessions/{session_id}` (full transcript replay), `GET /messages/{message_id}` (single message + parent chain), `POST /datasets` (export filtered slice as JSONL — pattern attested in `web-04` Langfuse / Braintrust / Phoenix Datasets entries). |
| 3.2 | Hybrid query implementation | new file: `src/unified_chat/api/search.py` | Per `web-07` finding 5 + Weaviate/Qdrant/pgvector hybrid sections: (a) embed query with same model as corpus (Voyage voyage-code-3 default); (b) run pgvector cosine top-k=200 ON embeddings; (c) run tsvector full-text top-k=200 on messages.text; (d) Reciprocal Rank Fusion at k=60 (default RRF constant); (e) optional cross-encoder rerank via Voyage rerank-2 or Cohere rerank-v3 (per `web-07` Cost Model — $2.50/yr for full team). |
| 3.3 | Tool-call-aware result hydration | new file: `src/unified_chat/api/hydrate.py` | When a `tool_use` block is in the result set, fetch its sibling `tool_result` (matched by `tool_use_id`) and return them as a single hit. Inverse for `tool_result` matches. Per `01-native-storage-formats.md` Cline Notes line 103 — Cline's split between `api_conversation_history` and `ui_messages` is uniquely useful, so when source is Cline/Roo, hydration optionally returns both views. |
| 3.4 | Repo + engineer + time scoping | edit `src/unified_chat/api/search.py` | Query parameters: `repo_id`, `engineer_id`, `team_id`, `tool` (filter by source — claude_code/cursor/aider/etc.), `since`, `until`, `model`, `is_sidechain`. Filters compile to SQL WHERE atop pgvector ANN. Per `web-07` Hidden Complexity #5 — explicit "team vs. private" axis is wired into RLS context-set on each request. |
| 3.5 | Citation envelope | edit `src/unified_chat/api/main.py` (response schemas) | Each retrieved chunk returns `{tool, repo_id, session_id, message_id, timestamp, role, model, snippet, score, source_url}` where `source_url` is a deeplink: `unified-chat://session/{session_id}#msg-{message_id}` resolvable by the Phase-5 MCP server. Pattern matches Helicone/Langfuse/Phoenix search UX (UI rows hyperlink to trace) per `web-04`. |
| 3.6 | Dataset export endpoint | new file: `src/unified_chat/api/datasets.py` | Filtered JSONL export, mirroring `web-04` "RAG export" row across Langfuse / Braintrust / Phoenix / Opik. Output is a stable, schema-versioned canonical-message JSONL (same as Phase-1 landing format) so an external eval harness or fine-tuning pipeline can consume it directly. |
| 3.7 | Eval harness golden set | new file: `tests/eval/golden_set.yaml` + `src/unified_chat/eval/runner.py` | Per `web-07` Hidden Complexity #7 — without an eval harness, retrieval quality drifts silently. Define ~50 (query, expected_message_id) tuples across the 9 tools. Runner posts each query to `/search`, computes MRR@10 and Recall@10, fails CI on regression. |
| 3.8 | API authentication | new file: `src/unified_chat/api/auth.py` | OIDC bearer token verification (per `web-06-enterprise-knowledge.md` patterns — referenced via `qa/gaps-and-questions.md` cross-partition note). Token claims map `engineer_id`/`team_ids` into Postgres session GUC for RLS (2.3). |
| 3.9 | Streaming + pagination | edit `src/unified_chat/api/search.py` | `/search?stream=true` returns NDJSON; `/sessions/{id}` paginates by message_id cursor for transcripts up to 100k messages (Claude Code session JSONLs in observed `46021a18-…jsonl` and `56bae2f8-…jsonl` per `01-native-storage-formats.md` verification tag are routinely large append-only files). |
| 3.10 | Optional: BTQL-style ad-hoc query path | new file: `src/unified_chat/api/sql.py` | Per `web-04` Braintrust entry — SQL/BTQL is the strongest search story among observability platforms. Expose a constrained read-only SQL endpoint over a curated view (no DDL, no UPDATE, statement timeout). Pattern: pg_partman + read-replica. Optional in MVP, but called out as differentiator vs. SpecStory which lacks an exposed query language. |

---

### Phase 4 — Team Aggregation, RBAC, Deployment

**Goal:** Make the system usable by 10+ engineers, not just one. Closes the gap that `01-native-storage-formats.md` Cross-Tool Summary Table identifies — every native tool is local-only and none ships team aggregation OOB. Continue.dev (HTTP `data:` destination) and Cline-enterprise (prompt-storage forwarding) are partial precedents per `01-native-storage-formats.md` Continue.dev / Cline sections. Deployment defaults: Docker Compose for the harvester sidecar; Kubernetes Helm chart for the central Postgres + API + MCP server.

**Dependencies:** Phases 2-3 functional for a single tenant.

**Step table:**

| Step | Action | Files | Details |
|------|--------|-------|---------|
| 4.1 | Per-engineer harvester agent | new file: `src/unified_chat/agent/local.py` and `packaging/agent/Dockerfile.local` | Lightweight long-running process that runs Phase-1 adapters + watchers locally on each engineer's machine, streams canonical messages to the central API over the `/ingest` endpoint (Phase 4.2). Patterned after Continue.dev's HTTP destination and Cline-enterprise prompt-storage forwarding noted in `01-native-storage-formats.md`. Distributed as Homebrew tap + apt PPA + Windows MSI + raw Python wheel for cross-platform reach (Cline/Roo exist on mac/linux/win per `01-native-storage-formats.md`). |
| 4.2 | Central ingest API endpoint | new file: `src/unified_chat/api/ingest.py` | `POST /ingest` accepts batched canonical messages, authenticates with engineer-bound bearer token, runs Phase-1.13 dedup + Phase-1.15 redaction server-side, writes through to Phase-2 storage. Idempotent on `(tool, session_id, message_id, content_hash)`. |
| 4.3 | Engineer + team identity model | edit `infra/postgres/init/02-schema.sql` (extend) + new file: `src/unified_chat/identity/teams.py` | Tables `engineers(id, email, github_login, machine_fingerprints[])`, `teams(id, name)`, `team_members(team_id, engineer_id, role)`, `repo_team_grants(repo_id, team_id, scope: 'view' | 'publish' | 'admin')`. Per `web-07` Hidden Complexity #5 — two indices per tenant (private + shared) realized via `messages.published_to_team_at` nullable timestamp. |
| 4.4 | Publish-to-team workflow | new file: `src/unified_chat/api/publish.py` | `POST /messages/{id}/publish` flips `published_to_team_at` and copies the embedding into the team-scope vector partition. Pattern matches `web-07` Hidden Complexity #5 ("typically two indexes per tenant (private + shared) with explicit publish step"). |
| 4.5 | Helm chart for central deployment | new dir: `deploy/helm/unified-chat/` (Chart.yaml, values.yaml, templates/api.yaml, templates/postgres.yaml, templates/migrate-job.yaml, templates/mcp.yaml) | Single chart deploys: Postgres (with pgvector + pgvectorscale), embedding worker StatefulSet, FastAPI service, MCP server (Phase 5), Prometheus exporter sidecar. Uses cert-manager + ingress-nginx by default. Patterned after Langfuse/Helicone Helm charts cited as supported in `web-04`. |
| 4.6 | Audit log + retention | new file: `src/unified_chat/audit/log.py`, edit schema for `audit_events` table | Enterprise-grade audit on read (who searched what, when), write (who ingested what, when), publish (who exposed what to whom). Per `qa/gaps-and-questions.md` gap I8 baseline + Langfuse `/ee` audit-log feature pattern (`web-04` Langfuse OSS license note). Configurable retention (default 90 days for trace data, 1 year for audit). |
| 4.7 | RBAC role catalog | new file: `src/unified_chat/auth/roles.yaml` | Roles: `engineer` (own + published team data), `team_lead` (team scope full), `admin` (cross-team), `auditor` (read-only audit). Maps to RLS policies set in 2.3. Pattern matches Langfuse EE / Helicone team / Braintrust roles per `web-04`. |
| 4.8 | Forward-capture: Helicone proxy mode | new file: `deploy/helm/helicone-proxy/values.yaml` + docs `docs/forward-capture-helicone.md` | Per `web-04-observability-platforms.md` Helicone entry: deploy self-hosted Helicone (Apache-2.0) as `chat-proxy.<corp>.<tld>`. Engineers set `ANTHROPIC_BASE_URL=https://chat-proxy.<corp>.<tld>` (Claude Code), Cursor custom Anthropic proxy URL, Continue/Cline/Aider custom base URL — all of which are documented support paths. Helicone webhook posts each completed call to `POST /ingest` from 4.2. Forward-capture is the second leg of the hybrid; harvester (Phase 1) is the first. |
| 4.9 | Forward-capture: OTLP / OpenLLMetry collector | new file: `deploy/helm/otel-collector/values.yaml` + new file: `src/unified_chat/forward/otlp_receiver.py` | Per `web-04` Traceloop/OpenLLMetry entry: deploy an OpenTelemetry Collector with the OpenLLMetry-flavored attributes. Claude Code's official OTLP hooks (per `web-04` Langfuse Claude Code integration page reference) emit spans directly. Receiver translates LLM/tool spans to canonical messages and writes through Phase 4.2 ingest. Provides parity with Langfuse/Phoenix/Opik/Laminar backends if the team chooses one of those over the BYO pgvector path. |
| 4.10 | Operator runbook | new file: `docs/runbook.md` | Backup (Postgres pg_basebackup → S3), DR (warm replica), index rebuild (pgvector REINDEX CONCURRENTLY), re-embed campaigns (Phase 2.10), audit export, GDPR right-to-erase implementation. Required to flip the system from prototype to "team-of-10 baseline" per `web-07` Operational Complexity Assessment table (4-6 weeks team-ready). |

---

### Phase 5 — IDE / Agent Integration (MCP Server, Retrieval-on-Demand)

**Goal:** Surface the unified-chat retrieval API inside the same IDEs and CLIs that produced the data, so engineers query their (and their team's) prior conversations without context-switching. MCP is the natural channel — the `web-03-memory-layer.md` Mem0/Cognee/Graphiti entries each note MCP servers; `web-04` Helicone and Traceloop both ship MCP servers for Claude Code / Cursor; `web-07` references Claude Historian MCP and AgentsView as patterns.

**Dependencies:** Phase 3 retrieval API live.

**Step table:**

| Step | Action | Files | Details |
|------|--------|-------|---------|
| 5.1 | MCP server scaffold | new file: `src/unified_chat/mcp/server.py` | Implements MCP tools: `search_chat_history(query, repo, since, tool?, model?, limit?)` → array of citation envelopes (Phase 3.5); `get_session(session_id)` → ordered messages; `get_session_around_message(message_id, n_before=10, n_after=10)`; `find_prior_decision(query, repo)` (RAG-shaped — runs `/retrieve` with a higher k and rerank); `publish_to_team(message_id)` (writes via 4.4). |
| 5.2 | Claude Code integration | new file: `~/.claude/mcp.json` snippet under `docs/integrations/claude-code.md` | Document `claude mcp add unified-chat http://unified-chat.<corp>.<tld>/mcp --header 'Authorization: Bearer …'`. Pattern matches Helicone MCP and Traceloop OpenLLMetry MCP integration paths cited in `web-04`. |
| 5.3 | Cursor integration | edit `docs/integrations/cursor.md` | Cursor MCP setup via `~/.cursor/mcp.json` adding the same server URL. Cursor's MCP host loads the same tool surface as Claude Code. |
| 5.4 | VS Code (Cline / Roo Code / Continue.dev) integration | new file: `docs/integrations/vscode.md` | Via VS Code's MCP host (1.95+) configure the same server. For Cline/Roo specifically, document that the MCP server can be invoked from inside the agent loop to retrieve prior tool-call traces. |
| 5.5 | Retrieval-on-demand auto-context plugin | new file: `src/unified_chat/mcp/auto_context.py` | Optional middleware: when an agent message exceeds a threshold or invokes a recurring keyword (e.g., "as we did before…"), the MCP server pre-fetches `find_prior_decision` and inserts the top-3 hits as system context. Pattern attested by `web-08-adjacent-tools.md` Pieces LTM / Cline Memory Bank / MCP-memory-server findings (cross-partition note M1 in `qa/gaps-and-questions.md`). |
| 5.6 | CLI for ad-hoc queries | new file: `src/unified_chat/cli/main.py` | `unified-chat search <query>`, `unified-chat session <id>`, `unified-chat publish <message_id>`, `unified-chat ingest --once`, `unified-chat reembed`, `unified-chat doctor`. Pattern matches `superclaude` CLI style from this codebase's `CLAUDE.md`. |
| 5.7 | Web UI (lightweight) | new dir: `web/` (Next.js or SvelteKit) | Surfaces session browser, search box, dataset export trigger. Optional in MVP — many `web-04` platforms (Langfuse, Phoenix, Helicone) ship UIs and engineers may prefer those if pgvector is replaced by Phoenix. |
| 5.8 | First-party SuperClaude skill | new file: `src/superclaude/skills/unified-chat-retrieve/SKILL.md` (per project `CLAUDE.md` skill packaging) | Skill that wraps `find_prior_decision` for use inside `/sc:research`, `/sc:task`, `/sc:implement`. Loads on-demand (~50 tokens). Per project `CLAUDE.md` Component Sync rules — edit `src/superclaude/skills/` then `make sync-dev`. |
| 5.9 | Smoke-test integration matrix | new file: `tests/integration/test_mcp_clients.py` | Test fixtures spin up unified-chat against a known session corpus and verify each MCP client (Claude Code, Cursor, Cline, Continue.dev) can invoke `search_chat_history` and recover an injected canary message. Required to catch MCP protocol drift (MCP spec versioning is fast-moving per `web-04` Traceloop Dec 2025 launch note). |

---

### Integration Checklist (Per AI Coding Tool)

Each row below specifies the canonical on-disk path, native format, and the recommended Phase-1 ingestion approach. All paths and formats are sourced from `01-native-storage-formats.md`.

| Tool | Path(s) on disk | Format | Ingestion approach | Adapter file (Phase 1.x) |
|------|-----------------|--------|--------------------|--------------------------|
| **Claude Code** | `~/.claude/projects/<slugified-cwd>/<sessionId>.jsonl` (slug = absolute cwd with `/` replaced by `-`); sibling stores `~/.claude/todos/`, `~/.claude/shell-snapshots/`, `~/.claude/file-history/`, `~/.claude/sessions/`, `~/.claude/plans/`, `~/.claude/telemetry/`, `~/.claude/history.jsonl` | JSON Lines, append-only; rich Anthropic content-block schema with `thinking`/`text`/`tool_use`/`tool_result`, `usage` cache breakdown, `attributionSkill`/`attributionPlugin`, `parentUuid` lineage, `isSidechain` sub-agent marker (per `01-native-storage-formats.md` Claude Code section) | **File watcher** (inotify/FSEvents/ReadDirectoryChangesW) on `~/.claude/projects/`. New JSONL line → tail-read → adapter parse → canonical append. Backfill on first run by walking all subdirs. JSONL format has evolved across versions (2.1.121 / 2.1.126 observed); adapter must be tolerant. Forward-capture via Claude Code's official OTLP hooks is documented in `web-04` Langfuse / Traceloop entries — register the OTLP collector (Phase 4.9) as a secondary path. | 1.2 (`adapters/claude_code.py`) |
| **Cursor IDE** | `~/Library/Application Support/Cursor/User/workspaceStorage/<workspaceHash>/state.vscdb` (mac); `~/.config/Cursor/User/workspaceStorage/<workspaceHash>/state.vscdb` (linux); `%APPDATA%\Cursor\User\workspaceStorage\<workspaceHash>\state.vscdb` (win); plus `…/User/globalStorage/state.vscdb` | SQLite single-file `ItemTable(rowid, key, value BLOB)`; conversation in JSON blobs under keys `aiService.prompts`, `workbench.panel.aichat.view.aichat.chatdata`, version-dependent `composer.composerData` (per `01-native-storage-formats.md` Cursor section) | **Scheduled scan** + lightweight file-mtime watcher. Cursor holds open SQLite connections — read with `sqlite3` in WAL-aware read-only mode (`?mode=ro&immutable=0`) and tolerate live writes. Per-Cursor-version JSON-path extractors required (schema drift documented in forum). Cross-workspace querying needs merging multiple `state.vscdb` files. No first-class cloud sync, so harvesting must run on each engineer's machine. | 1.5 (`adapters/cursor.py`) |
| **Aider** | `<repo>/.aider.chat.history.md`, `<repo>/.aider.input.history`, `<repo>/.aider.llm.history` (latter only if `--llm-history-file` set); locations configurable via `--chat-history-file`, `--input-history-file`, `--llm-history-file`; typically `.gitignore`'d | Markdown chat transcript; plain-text input log; plain-text/JSON-ish LLM request/response blocks. Session boundary `# aider chat started at <timestamp>`; user prompts as `#### ` headings; SEARCH/REPLACE edit blocks inline; `Applied edit to <file>` lines; commit SHAs (per `01-native-storage-formats.md` Aider section) | **File watcher** on each known repo root. Discovery: walk monitored repo list (configured) for `.aider.chat.history.md` presence. Parse markdown by header. Cross-reference git log to recover diff content per `01-native-storage-formats.md` Aider Notes (commits are the parallel persistence layer, more reliable than the markdown for diff reconstruction). LLM history file is the only structured replay artifact and is opt-in — flag missing as `[UNVERIFIED — opt-in by user]`. | 1.6 (`adapters/aider.py`) |
| **Continue.dev** | `<project>/.continue/dev_data/*.jsonl` by default; configurable in `config.yaml` via `data:` block — `destination: file://<path>` writes JSONL there, or `destination: https://<endpoint>` POSTs events; live session state also in IDE-extension globalStorage | JSONL per event type with versioned `schema` field (`0.1.0`, `0.2.0`); event categories autocomplete, chat, tokens_generated, quickEdit (per `01-native-storage-formats.md` Continue.dev section) | **Hybrid: file watcher + push-from-tool**. For default JSONL-on-disk: watcher under `.continue/dev_data/`. Recommend operators set `data.destination` to point at the Phase-4.2 `/ingest` HTTPS endpoint, so Continue posts directly (this is the only tool of the 9 explicitly designed for HTTP fan-out per `01-native-storage-formats.md` Continue.dev Notes line 81). Per-version mappers required since fields-by-event-type live in `@continuedev/config-yaml` types in source, not docs (`qa/gaps-and-questions.md` gap I8 baseline). | 1.9 (`adapters/continue_dev.py`) |
| **Cline** | VS Code mac: `~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/tasks/<taskId>/`; VS Code linux: `~/.config/Code/User/globalStorage/saoudrizwan.claude-dev/tasks/<taskId>/`; VS Code win: `%APPDATA%\Code\User\globalStorage\saoudrizwan.claude-dev\tasks\<taskId>\`; Code-Insiders variants; JetBrains analog under `JetBrains/<IDE>/globalStorage/saoudrizwan.claude-dev/`; alt `~/.cline/data/tasks/<taskId>/` | Per-task directory with three JSON files: `api_conversation_history.json` (model-eye view — system+user+assistant+tool messages as the model receives them), `ui_messages.json` (UI-side records — streamed tool invocations, approvals, mode changes), `task_metadata.json` (id, title, timestamps, model, mode, token totals) (per `01-native-storage-formats.md` Cline section) | **File watcher** on the globalStorage `tasks/` dir with task-scoped finalization detection (write task as canonical only when `task_metadata.json` ends with terminal status). Field-level schema not published in docs (per `01-native-storage-formats.md` Cline Missing) — adapter relies on observed keys; surface unknowns into `raw_extra`. Cline-enterprise prompt-storage forwarding can substitute push-from-tool path for licensed customers. | 1.7 (`adapters/cline.py`) |
| **Roo Code** | Linux remote-server: `~/.vscode-server/data/User/globalStorage/rooveterinaryinc.roo-cline/tasks/<taskId>/`; local VS Code: same pattern at platform User globalStorage (mac `~/Library/Application Support/Code/...`, win `%APPDATA%\Code\...`) | Cline-fork JSON trio: `api_conversation_history.json`, `ui_messages.json`, plus task metadata file (per `01-native-storage-formats.md` Roo Code section) | **File watcher** — reuse Cline adapter with extension-id substitution to `rooveterinaryinc.roo-cline` and add the VS Code Server path for remote deployments. Per `01-native-storage-formats.md` Roo Notes line 119, no other code change needed. | 1.8 (`adapters/roo_code.py`) |
| **OpenAI Codex CLI** | `$CODEX_HOME/sessions/YYYY/MM/DD/rollout-<timestamp>-<uuid>.jsonl` (default `CODEX_HOME=~/.codex`); sibling `session_index.jsonl` and `state.sqlite` in same tree | JSON Lines (`RolloutLine = {timestamp, item: RolloutItem}` with variants `SessionMeta`, `TurnContext`, `ResponseItem`, `EventMsg`, `Compacted`) + SQLite index + JSONL session index (per `01-native-storage-formats.md` Codex CLI section) | **File watcher** on `$CODEX_HOME/sessions/`. Use `session_index.jsonl` to discover active sessions; tail individual rollout files. Parse `ResponseItem` tool calls (e.g., `apply_patch`) into canonical `tool_use`/`file_edit` blocks. Read `state.sqlite` for resume metadata if present (column layout `[UNVERIFIED]` per `01-native-storage-formats.md` Gaps — adapter must be tolerant). | 1.3 (`adapters/codex_cli.py`) |
| **GitHub Copilot CLI** (post-2025-10-25 layout, replacing the deprecated `gh-copilot`) | `~/.copilot/session-state/<sessionId>/*.jsonl` and `~/.copilot/session-store.db` (override via `$COPILOT_HOME`); plus `~/.copilot/logs/`, `config.json`, `settings.json`, `mcp-config.json`, `permissions-config.json`, `instructions/`, `agents/`, `skills/`, `hooks/`, `installed-plugins/`, `plugin-data/`. Cache root separate: `~/Library/Caches/copilot` (mac), `$XDG_CACHE_HOME/copilot` or `~/.cache/copilot` (linux), `%LOCALAPPDATA%\copilot` (win) | JSONL per-session transcript + SQLite `session-store.db` index (per `01-native-storage-formats.md` Copilot CLI section) | **File watcher** on `~/.copilot/session-state/` for JSONL + scheduled SQLite read for index/metadata join. JOIN session-state JSONL with `session-store.db` rows by `sessionId` — preferred over JSONL-alone because Copilot's docs say the SQLite index is the canonical query layer. Field-level schema unpublished (gap noted in `qa/gaps-and-questions.md` baseline) — tolerate column drift; flag unknown columns into `raw_extra`. Old `gh-copilot` paths are stale and out of scope (deprecated 2025-10-25 per `01-native-storage-formats.md` Stale Documentation). | 1.4 (`adapters/copilot_cli.py`) |
| **Gemini CLI** | `~/.gemini/tmp/<projectHash>/chats/checkpoint-<name>.json` (explicit `/chat save` snapshots), `~/.gemini/tmp/<projectHash>/logs.json` (runtime/session log), `~/.gemini/tmp/<projectHash>/shell_history`. `<projectHash>` is a hash of the project root path | JSON arrays of `{role, parts}` objects (Google content-parts schema; `role` ∈ user/model; `parts` includes text and tool/function-call parts) (per `01-native-storage-formats.md` Gemini CLI section) | **File watcher** + scheduled scan. Walk all `~/.gemini/tmp/*/` directories on first run; resolve `<projectHash>` back to repo root via Gemini's internal mapping (the resolver in Phase 1.14 owns this). `logs.json` schema is `[UNVERIFIED]` (source-of-truth is `chatRecordingService.ts` per `01-native-storage-formats.md` Gemini Source) — adapter must tolerate field drift. No global cross-project index, so adapter walks all hash buckets. | 1.10 (`adapters/gemini_cli.py`) |

**Notes on the checklist:**

- **Push-from-tool** is only practical for Continue.dev (built-in HTTP destination) and Cline-enterprise (prompt-storage forwarding) per `01-native-storage-formats.md` Continue.dev / Cline sections. For all other tools, file watcher or scheduled scan is the only available channel because none of them ship a forwarding feature.
- **Forward-capture parallel paths** (Phase 4.8 Helicone proxy, Phase 4.9 OTLP collector) supplement the harvester for any tool that supports a custom API base URL or OTLP export — captures going-forward but cannot fill the historical archive. The harvester remains required for backfill.
- **Schema-drift exposure** is highest for Cursor (version-coupled JSON blobs), Copilot CLI (undocumented SQLite columns), Gemini CLI (`logs.json`), and Cline/Roo (per-file fields not in docs). Adapters carry a `raw_extra` JSON column on canonical messages so unknown fields survive future inspection without blocking ingest.
- **Repo-identity reconciliation** (Phase 1.14) is required for every row above because each tool uses a different project-scoping mechanism (slugified-cwd, opaque hashes, repo-relative, taskId UUIDs, date hierarchy) per `01-native-storage-formats.md` Key Takeaways line 194.
- **Tool calls preserved everywhere, normalized nowhere** (per `01-native-storage-formats.md` Key Takeaways line 191) — the canonical `content_blocks` model in Phase 1.1 unifies Anthropic content-blocks (Claude Code), Google content-parts (Gemini CLI), OpenAI `RolloutItem.ResponseItem` (Codex), free-form JSON (Cursor), Cline JSON-trio, and SEARCH/REPLACE text (Aider) into one schema.

---

## 9. Open Questions

The questions below capture real residual uncertainty in this report. They are grouped into:
(a) UNVERIFIED claims surfaced by the research-completeness gate that the synthesis chose to retain rather than excise; (b) two scoping judgment calls flagged in `research-notes.md` AMBIGUITIES_FOR_USER (addressed by the Section 7 recommendation, but worth confirming with stakeholders before implementation); (c) competitive-landscape items that could materially affect the build/buy/adopt decision over the next 6–12 months; and (d) cross-partition reconciliation choices that synthesis made on its own authority and should be sanity-checked.

| # | Question | Impact | Suggested Resolution |
|---|----------|--------|---------------------|
| 1 | What is SpecStory's actual paid-tier pricing? `/pricing` returns 404 and the Teams page is a Design Partner application form. (Gap I1) | Blocks an apples-to-apples adopt-vs-build cost comparison in Section 6/7. Recommendation currently assumes "free OSS today + custom enterprise pricing TBD." | Submit a Design Partner application via `specstory.com/teams`, or contact SpecStory sales directly, before committing to an adopt-path budget. |
| 2 | Has SpecStory's "RAG coming soon" actually shipped, and on what timeline? Roadmap rests on unreachable `beta.specstory.com` references; no shipped product to verify. (Gap I2) | Section 7 recommends NOT waiting on SpecStory RAG. If it ships in <90 days with strong team-aggregation, the build-vs-adopt calculus flips. | Track SpecStory's GitHub releases, blog, and X/Twitter weekly through the planned implementation horizon. Re-evaluate the recommendation if RAG ships before Phase 2 of the build plan completes. |
| 3 | Is the Voyage / MongoDB acquisition claim (web-07) accurate as stated, and what license/availability changes followed? Claim appears in web-07 without a primary URL citation. (Gap I4 — `[UNVERIFIED]`) | If Voyage embeddings are recommended in Section 6/8 but acquisition altered terms (e.g., MongoDB-Atlas-only access), the BYO stack guidance breaks. | Verify against MongoDB's official press release archive and Voyage's current pricing/licensing docs before any embedding-vendor commitment. |
| 4 | Are Cursor and Notion AI confirmed Turbopuffer customers? (web-07 claim, no URL citation. Gap I4 — `[UNVERIFIED]`) | Used as social-proof in vector-DB selection. If false, Turbopuffer's positioning weakens and BYO ranking shifts. | Search Turbopuffer's customer page / case studies; check Cursor and Notion AI engineering blogs for stack disclosures. |
| 5 | Is Mastra's claimed "10x cost reduction" reproducible, on what workload, vs. what baseline? (web-07 claim, no URL citation. Gap I4 — `[UNVERIFIED]`) | Cost claims that don't survive scrutiny would weaken any Mastra-anchored BYO recommendation. | Locate the original Mastra benchmark post or whitepaper; reproduce on an internal representative workload before relying on the figure. |
| 6 | Does Open WebUI's license actually contain a clause requiring branding preservation for deployments >50 users? Sourced to an unlinked Reddit thread. (Gap I6 — `[UNVERIFIED]`) | If the clause exists, Open WebUI as an adopt-path option in Section 6 carries a re-branding constraint that affects internal rollout. If it does not, that risk drops out. | Read the actual `LICENSE` file in the Open WebUI GitHub repo at the version under consideration; confirm with their maintainers if ambiguous. |
| 7 | What is the exact license of the `arize-phoenix-otel` adjacent package? web-04 notes "Elastic-2.0 in some channels — verify per package." (Gap I7) | Phoenix is short-listed as an observability option. An Elastic-2.0 sub-package would constrain self-hosted commercial use. | Check the package's PyPI metadata and the Arize GitHub repo `LICENSE` for that specific package, not just the umbrella `arize-phoenix` repo. |
| 8 | Is Voyage's "+13.8% over text-embedding-3-large on code retrieval" a single benchmark or an average across several? web-07 wording is imprecise ("+13.8% to +16.3% average"). (Gap I5) | Affects how confidently we cite the uplift in Section 6/8 vendor comparison. | Locate Voyage's primary benchmark post for `voyage-code-3` and pin the exact metric, dataset, and baseline. |
| 9 | Should LLM observability platforms (LangSmith, Langfuse, Helicone, Phoenix, etc.) be in scope as comparables? They capture LLM conversations between IDE and model — but they instrument the call path rather than harvest IDE chat archives. (research-notes AMBIGUITY 1) | Section 7 evaluates both architectures and includes observability as a partial comparable, but stakeholders may want to narrow scope to "harvest existing IDE chat archives only." | Confirm with the user/sponsor: should the project capture LLM calls at the proxy boundary, harvest existing local chat files, or both? Decision changes the bucket weighting in Section 5/6. |
| 10 | What does "unified single database" mean operationally? (a) one product covering everything, (b) one pipeline assembling outputs from many tools into a shared store, or (c) team-wide deployment of one of the above. (research-notes AMBIGUITY 2) | Section 7 evaluates all three; the recommendation leans toward (b) the pipeline model. If the sponsor expects (a) a single off-the-shelf product, the recommendation must change. | Confirm with the sponsor in writing before kicking off the implementation plan. The answer determines whether the work is integration engineering or vendor selection. |
| 11 | When does Cursor ship, or expand, its "Generate Cursor Rules from chat history" feature, and how broadly? Identified by web-02 as the biggest medium-term competitive threat. (Gap M3) | If Cursor's native feature evolves into team-wide chat aggregation + RAG, much of the build-path value disappears. The decision window for "build" narrows. | Subscribe to the Cursor changelog (track v0.50+ releases) and watch their docs/forum for any "team chat history" or "rules from team history" expansion. Re-evaluate at each Cursor minor version. |
| 12 | Is the cross-partition deduplication choice (AnythingLLM → web-05 primary; Pieces → web-08 primary; Cline Memory Bank → web-08 primary; MCP memory → substrate not competitor; Spool → web-07 primary; Onyx → web-05 primary) the right framing for Section 5? Synthesis decided this on its own authority per Gap M1. | If a primary-source choice is wrong, Section 5 entries may underweight or miss key capabilities (e.g., treating Pieces only as adjacent and missing its LTM-as-substrate angle, or vice versa). | Have a domain reviewer (or the rf-qa synthesis-gate) sanity-check the primary-source assignments before final assembly. Adjust if any product was materially miscategorized. |
| 13 | Are all web-07 sources actually Official-or-Repo reliability, as synthesis treats them by default? (Gap I9 — file lacks per-row Reliability tags) | If a load-bearing claim in Section 5/6/8 originated from a lower-reliability source, downstream confidence is overstated. | When citing any specific web-07 claim in the final report, re-open the source and tag it explicitly; default-Official is a synthesis convenience, not a verified file-level property. |

---

## 10. Evidence Trail

### 10.1 Codebase Research

| File | Topic | Agent Type | Status |
|------|-------|------------|--------|
| `research/01-native-storage-formats.md` | Native conversation storage formats of mainstream AI coding tools (Cursor, Claude Code, Aider, Continue.dev, Cline, Roo Code, Copilot CLI, Gemini CLI, Codex CLI): on-disk paths, file format (JSON/Markdown/SQLite), schema fields captured, per-machine vs. synced, deprecation flags. Establishes the "as-is" baseline that any unified-context system must ingest from. | Pattern Investigator | Complete |

### 10.2 Web Research

| File | Topic | Status |
|------|-------|--------|
| `research/web-01-specstory-deep-dive.md` | SpecStory deep-dive: features, architecture, OSS license, cloud product, pricing (unobtainable — Design Partner gated), team-aggregation status, RAG-coming-soon roadmap, Agent Skills, Cursor-rules generation, API surface. | Complete |
| `research/web-02-direct-competitors.md` | Direct competitors positioned as "capture AI coding chats, sync, search across team" — landscape, deployment models, supported tools, RAG/team aggregation status, pricing. Includes Cursor's own "Generate Rules from chat history" as a medium-term threat. | Complete |
| `research/web-03-memory-layer.md` | AI agent memory layer: Mem0, Letta (MemGPT), Zep, Cognee, Graphiti, LangMem, SuperMemory, Mastra Memory, Basic Memory MCP. Abstraction model, multi-user/team support, self-host options, pricing, ingestion shape. | Complete |
| `research/web-04-observability-platforms.md` | LLM observability platforms: LangSmith, Langfuse, Helicone, Arize Phoenix, HoneyHive, Braintrust, PromptLayer, W&B Weave, Opik (Comet), Lunary, AgentOps, Traceloop. Conversation capture, search, replay, dataset/RAG export, self-host vs. SaaS, license per platform. | Complete |
| `research/web-05-self-hosted-chat.md` | Self-hosted / OSS chat platforms: Open WebUI, LibreChat, AnythingLLM, Onyx (formerly Danswer), Chatbox. Chat-history storage, multi-user, RAG over chat history, external-chat ingestion APIs, team aggregation. | Complete |
| `research/web-06-enterprise-knowledge.md` | Enterprise org-memory & knowledge platforms: Glean, Mem (mem.ai), Notion AI, Coda AI, Slack AI, Confluence AI, Slite. Can they index AI conversation transcripts as another data source? Connectors, custom-ingestion APIs, pricing tier required. | Complete |
| `research/web-07-byo-rag-stack.md` | Build-your-own RAG-over-conversations: vector DBs (Pinecone, Weaviate, Qdrant, Chroma, Milvus, pgvector, Turbopuffer); embedding APIs (OpenAI, Voyage, Cohere); pipeline tools (LlamaIndex, LangChain, Haystack, txtai, Mastra); reference architectures and cost-precedent (Spool). | Complete |
| `research/web-08-adjacent-tools.md` | Adjacent / less-direct tools: Charlie Mnemonic, Pieces for Developers (LTM cross-IDE), Continue Hub, Cursor team features, Cline Memory Bank, MCP-memory servers (mcp-memory, basic-memory), Sourcegraph Cody history, JetBrains AI Assistant team features. Brief positioning + relevance to the unified-context goal. | Complete |

### 10.3 Synthesis Files

| File | Sections produced |
|------|-------------------|
| `synthesis/synth-01-problem-current-state.md` | Section 1 (Problem Statement), Section 2 (Current State Analysis) |
| `synthesis/synth-02-target-gaps.md` | Section 3 (Target State), Section 4 (Gap Analysis) |
| `synthesis/synth-03-external-findings.md` | Section 5 (External Research Findings — the consolidated comparables landscape, with cross-partition reconciliation per Gap M1/M2) |
| `synthesis/synth-04-options-recommendation.md` | Section 6 (Options Analysis), Section 7 (Recommendation — addresses the two AMBIGUITIES_FOR_USER) |
| `synthesis/synth-05-implementation-plan.md` | Section 8 (Implementation Plan) |
| `synthesis/synth-06-questions-evidence.md` | Section 9 (Open Questions), Section 10 (Evidence Trail) |

### Gaps Log

The research-completeness gate (Phase 3) initially returned **FAIL** on both partition reports. The failures were gate-driven rather than substantive: 5 files (web-01, web-03, web-04, web-05, web-08) carried `Status: In Progress` markers that needed flipping to `Complete`, plus 2 minor content corrections in web-04 (the Helicone OSS license needed correction from "MIT-style" to Apache-2.0, and a duplicated "Activity signal" line under Phoenix needed merging). Exactly **one fix-cycle** was applied: 5 status flips and 2 in-place content fixes in web-04. After that fix-cycle, the merged research-gate verdict was **PASS (post-fix)**, and Phase 5 synthesis was authorized to proceed. Both QA partition reports explicitly noted that, with status fields corrected, remaining minor findings could be deferred to synthesis (Sections 4, 6, and 9) without re-spawning research — which is what happened: Important gaps I1–I9 and Minor gaps M1–M6 from `qa/gaps-and-questions.md` are carried forward into Sections 4, 5, 6, and the Section 9 Open Questions table above. **No synthesis-gate fix cycles have been run yet** — those are scheduled as part of Phase 5 QA and will be appended to this Gaps Log if/when triggered.
