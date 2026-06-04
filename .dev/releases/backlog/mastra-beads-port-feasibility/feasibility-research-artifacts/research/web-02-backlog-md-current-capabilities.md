# Web Agent 02 — Backlog.md Current Capabilities

**Date:** 2026-06-02
**Status:** Complete
**Topic:** Backlog.md CLI/MCP/schema/docs/decision/browser capabilities, metadata extensibility, no-git/git modes, agent workflow guidance, and current maturity
**Provenance:** Tavily search/extract only. No WebSearch/WebFetch fallback used.

---

## Findings

### 1. Backlog.md is markdown-native task/work-record with CLI, TUI board, web UI, search, docs, decisions, MCP, and agent instructions — HIGH

Data lives in a project-local backlog folder (`backlog/`, `.backlog/`, or custom via `backlog.config.yml`). Tasks are human-readable Markdown (`task-10 - Add core search functionality.md`). Features: markdown-native tasks, AI-ready operation (Claude Code/Gemini CLI/Codex/Kiro), terminal Kanban (`backlog board`), browser UI (`backlog browser`), fuzzy search (`backlog search`), board export, offline/private local storage, cross-platform, MIT license.

- Source: https://github.com/MrLesk/Backlog.md [tavily]
- Relationship to codebase: Supports target ownership need for human-readable work-of-record and agent-operable task store. Does not by itself prove arbitrary SuperClaude orchestration metadata can be represented without schema adaptation.

### 2. Broad CLI surface: init/config, tasks, drafts, docs, decisions, search, board, browser, overview, cleanup, completion — HIGH

Init/config (`backlog init`, `backlog config` wizard), MCP-connector vs legacy CLI integration choice, task create/list/view/edit/archive, drafts, parent/subtasks, dependencies, references, documentation links, acceptance criteria, Definition of Done, plan, notes, final summary, priority, assignee, labels, status. Search across tasks/docs/decisions. `backlog board` + export. `backlog browser --port 8080 --no-open`. Docs (`backlog doc create/update/list/view`). Decisions (`backlog decision create "..." -s proposed`). Shell completions.

- Source: https://raw.githubusercontent.com/MrLesk/Backlog.md/main/CLI-INSTRUCTIONS.md [tavily]
- Relationship to codebase: Supports mapping task lifecycle + docs/decisions, but orchestration must call CLI/MCP rather than hand-edit files. **No built-in sprint/roadmap pipeline equivalent** — those need orchestration above Backlog.md.

### 3. Rich first-class task schema but not arbitrarily extensible via typed/MCP schema — HIGH

`Task` fields: `id`, `title`, `status`, `assignee`, `reporter`, dates, `labels`, `milestone`, `dependencies`, `references`, `documentation`, `modifiedFiles`, `description`, `implementationPlan`, `implementationNotes`, `finalSummary`, acceptance criteria, Definition of Done, parent/subtasks, `priority`, `branch`, `ordinal`, `filePath`, `source`, `onStatusChange`. `BacklogConfig` includes statuses, labels, defaultStatus, git settings, filesystemOnly, zero-padded IDs, backlogDirectory, prefixes, MCP HTTP config.

- Source: https://raw.githubusercontent.com/MrLesk/Backlog.md/main/src/types/index.ts [tavily]
- Relationship to codebase: Supports mapping many SuperClaude task fields into native fields, but custom metadata may need explicit mapping or raw-content conventions. Contradicts assumption that arbitrary custom frontmatter is safely accepted by MCP schemas.

### 4. Current MCP task schemas reject unknown properties (`additionalProperties: false`) — HIGH

MCP task list/search/view/archive/complete schemas use `additionalProperties: false`. Search supports `query`, `status`, `priority`, `modifiedFiles`, `limit`. List supports `status`, `assignee`, `milestone`, `labels`, `search`, `limit`.

- Source: https://raw.githubusercontent.com/MrLesk/Backlog.md/main/src/mcp/tools/tasks/schemas.ts [tavily]
- Relationship to codebase: Supports validated MCP operation for known fields, but SuperClaude-specific metadata cannot simply be added as arbitrary MCP fields — must use supported fields, body sections, docs, references, or extend Backlog.md.

### 5. Current MCP is an MVP stdio surface — reduced relative to older "75+ tools" claims — HIGH

Current MCP README describes "Backlog.md MCP Implementation (MVP)" — a "minimal stdio MCP surface" routing through existing Core APIs. Tools: `task_*`, `milestone_*`, `definition_of_done_defaults_*`, `document_*`. Document `path` inputs are docs-directory-relative and reject absolute paths/traversal.

- Source: https://raw.githubusercontent.com/MrLesk/Backlog.md/main/src/mcp/README.md [tavily]
- Relationship to codebase: Contradicts older "75+ tools" or decision-tools-current claims. Current MCP task tools: `task_create`, `task_list`, `task_search`, `task_edit`, `task_view`, `task_archive`, `task_complete` (per `src/mcp/tools/tasks/index.ts`).

### 6. Docs first-class; decisions first-class in CLI but not clearly in current MCP MVP — HIGH

Docs: global IDs across `backlog/docs` subdirectories; `backlog doc create "New Guide" -p guides`; `--title/--type/--tags/--path` metadata; absolute paths/`..` rejected. Decisions: `backlog decision create "..."`, `-s proposed`. Current MCP README does not mention decision tools → CLI-vs-MCP coverage gap.

- Source: https://raw.githubusercontent.com/MrLesk/Backlog.md/main/CLI-INSTRUCTIONS.md [tavily]

### 7. Git is optional; no-git mode disables cross-branch/remote/auto-commit — HIGH

`backlog init --no-git` creates filesystem-only project. Config: `remoteOperations`, `autoCommit` (default false), `bypassGitHooks`, `checkActiveBranches`, `activeBranchDays`, `filesystemOnly`.

- Sources: https://github.com/MrLesk/Backlog.md ; https://raw.githubusercontent.com/MrLesk/Backlog.md/main/ADVANCED-CONFIG.md [tavily]
- Relationship to codebase: Supports both repository-native and filesystem-only orchestration. Contradicts older "Git repos only" descriptions.

### 8. Explicit agent workflow guidance aligns with SuperClaude discipline — HIGH

Recommended AI flow: decompose into small tasks with descriptions + AC, review, one task per session/PR, research+plan before coding, review plan, implement+verify, rerun fresh if inadequate. README recommends CLI/MCP/Web over manual file editing to keep field types consistent.

- Source: https://github.com/MrLesk/Backlog.md [tavily]
- Relationship to codebase: Supports replacing some SuperClaude tasklist discipline with Backlog.md-native checkpoints, but **not a full SuperClaude compliance gate/pipeline** (no automated QA/reflection/routing equivalent).

### 9. MCP workflow instruction surface shows doc drift — HIGH

Source `agent-nudge.md`: read `backlog://workflow/overview` for MCP-resource clients; else call `backlog.get_backlog_instructions()` with `instruction` selectors `task-creation`/`task-execution`/`task-finalization`. README still references `backlog://docs/task-workflow`. Search found BACK-408 consolidating workflow guide tools, not BACK-407. Treat as doc drift requiring runtime verification.

- Sources: https://raw.githubusercontent.com/MrLesk/Backlog.md/main/src/guidelines/mcp/agent-nudge.md ; https://github.com/MrLesk/Backlog.md [tavily]
- Note: The seed-brief's BACK-407 (MCP spec alignment) claim is [UNVERIFIED — could not confirm BACK-407 specifically; BACK-408 found instead].

### 10. Browser UI exists but has an open state-loss bug under background file changes — HIGH

`backlog browser` provides web UI; `--port 8080 --no-open` supported. Open bug #578: "UI state resets if files change while browser UI is running" — unsaved draft text cleared when an agent updates tasks/files. BACK-429 created to preserve unsaved drafts; issue remains open.

- Sources: https://github.com/MrLesk/Backlog.md ; https://github.com/MrLesk/Backlog.md/issues/578 [tavily]

### 11. Maturity: active, version 1.45.2, MIT, many releases — HIGH

Package `backlog.md` version `1.45.2`, MIT, TypeScript/Bun. Dependencies include MCP SDK, React, Tailwind, Fuse.js, gray-matter, proper-lockfile, commander. GitHub showed ~5.7k stars, 340 forks, 38 issues, 18 PRs, 888 commits, 185 releases at extraction. Recent commits: MCP/document Windows fixes, no-git support, custom backlog directory, touched-files metadata, web milestone editing.

- Sources: https://raw.githubusercontent.com/MrLesk/Backlog.md/main/package.json ; https://github.com/MrLesk/Backlog.md [tavily]

### 12. Local-file/git-centric, not a centralized multi-user PM backend — MEDIUM-HIGH

README: "100% private & offline," lives in the repo, operates on Markdown files. `proper-lockfile` dependency suggests file-locking awareness. Concurrent agents/users need process discipline.

- Sources: https://github.com/MrLesk/Backlog.md ; package.json [tavily]
- Relationship to codebase: Supports work-of-record, not a full multi-user coordination server / transactional PM database.

### 13. Beads integration not mature; maintainers suggest narrow scope first — HIGH

Open feature request #588 (Beads/pi-task integration). Maintainer: "This needs a narrower integration decision before tasking... start by choosing one workflow, such as import/export sync with Beads, rather than committing to a broad integration surface."

- Source: https://github.com/MrLesk/Backlog.md/issues/588 [tavily]
- Relationship to codebase: Beads ↔ Backlog.md integration is an external design task, not an existing capability. This directly tempers the seed-brief's "Backlog.md ↔ Beads via shared repo metadata references" claim.

## Key External Findings

1. Strong candidate for human-readable, repo-local work-of-record (tasks, docs, decisions, board, browser).
2. CLI surface is more complete than current MCP (MCP MVP lacks decisions).
3. Task metadata is rich but not arbitrarily extensible via typed/MCP schema.
4. No-git mode is real and current.
5. Agent workflow guidance aligns with SuperClaude decomposition/plan/checkpoint discipline.
6. MCP workflow instruction surface shows doc drift; BACK-407 specifically unverified (BACK-408 found).
7. Browser UI useful but has an open unsaved-state bug under concurrent file changes.
8. Active and mature (v1.45.2, MIT).
9. Local-file/git-centric, not a central multi-user transactional backend.
10. Beads integration is not currently mature.

## Recommendations from External Research

1. Use Backlog.md as the human-readable task/docs/decision work-of-record, not the orchestration engine.
2. Put SuperClaude/Mastra orchestration above Backlog.md (routing, gates, reflection, sprint/roadmap semantics, multi-agent sequencing).
3. Use CLI/MCP/Web as the mutation interface; avoid direct markdown edits except controlled migration/import tooling.
4. Map SuperClaude fields into supported Backlog.md fields (identity/status/priority/labels/milestone/dependencies native; plans/notes/final summary body sections; AC/DoD checklists; touched files via `modifiedFiles`; specs via references/documentation; custom orchestration state via body sections/docs/decisions or schema extension).
5. Treat current MCP as useful but incomplete (CLI for decisions until MCP decision support verified).
6. Runtime-test MCP instruction resources before building on them (prefer source `agent-nudge.md` over README on conflict).
7. Warn users not to keep long unsaved browser drafts open during agent mutation (issue #578).
8. For Beads, start with narrow import/export/cross-reference sync; do not assume native integration.
9. For no-git environments, init with `--no-git` and avoid cross-branch/remote/auto-commit assumptions.
10. For concurrent multi-agent use, enforce one-task-per-agent/session discipline.

## Sources

- https://github.com/MrLesk/Backlog.md [tavily]
- https://raw.githubusercontent.com/MrLesk/Backlog.md/main/CLI-INSTRUCTIONS.md [tavily]
- https://raw.githubusercontent.com/MrLesk/Backlog.md/main/ADVANCED-CONFIG.md [tavily]
- https://raw.githubusercontent.com/MrLesk/Backlog.md/main/src/types/index.ts [tavily]
- https://raw.githubusercontent.com/MrLesk/Backlog.md/main/src/mcp/README.md [tavily]
- https://raw.githubusercontent.com/MrLesk/Backlog.md/main/src/mcp/tools/tasks/index.ts [tavily]
- https://raw.githubusercontent.com/MrLesk/Backlog.md/main/src/mcp/tools/tasks/schemas.ts [tavily]
- https://raw.githubusercontent.com/MrLesk/Backlog.md/main/src/guidelines/mcp/agent-nudge.md [tavily]
- https://raw.githubusercontent.com/MrLesk/Backlog.md/main/package.json [tavily]
- https://github.com/MrLesk/Backlog.md/issues/578 [tavily]
- https://github.com/MrLesk/Backlog.md/issues/588 [tavily]
- https://smithery.ai/skills/kasuboski/backlog-manager [tavily]
