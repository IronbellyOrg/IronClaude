# Web Agent 03 — Beads Current Capabilities

**Date:** 2026-06-02
**Status:** Complete
**Topic:** Beads CLI, issue graph, storage backend, JSON/CLI contract, Dolt/server mode, dependency semantics, UI options, and multi-writer behavior
**Provenance:** Tavily search/extract first and exclusively. No WebSearch/WebFetch fallback used.

---

## Findings

### 1. Current repo, ownership, activity, maturity — HIGH

Current public repo: `gastownhall/beads`. README: "Distributed graph issue tracker for AI agents, powered by Dolt." Platforms: macOS, Linux, Windows, FreeBSD. High activity (extracted: 9,182 commits, 91 releases, 227 open issues, 175 PRs, 24.3k stars). Packages: npm `@beads/bd`, PyPI `beads-mcp`.

- Source: https://github.com/gastownhall/beads [tavily]
- Relationship to codebase: Active dependency-aware issue graph candidate, but rapid churn / high open-issue load.

### 2. Release/version caution around v1.0.5 — MEDIUM-HIGH

GitHub releases showed v1.0.5 as pre-release/gated with warning "do not upgrade" — migration `0043` can silently/unrecoverably break multi-machine `bd dolt` sync after both clones upgrade (issue #4259). DoltHub blog (2026-05-29) shows `bd version 1.0.5` available. Issue #3870 documented v1.0.4 server-mode data-clobber regression needing v1.0.5 fix.

- Sources: https://github.com/gastownhall/beads/releases ; https://www.dolthub.com/blog/2026-05-29-evolving-with-beads ; https://github.com/gastownhall/beads/issues/3870 [tavily]
- Relationship to codebase: Use only behind explicit version pinning and upgrade gates.

### 3. Core CLI commands and agent workflow surfaces — HIGH

`bd ready` (unblocked tasks), `bd create "Title" -p 0`, `bd update <id> --claim` (atomic claim: assignee + in_progress), `bd dep add <child> <parent>`, `bd show <id>` (details/audit trail), `bd prime` (agent workflow context + persistent memories), `bd remember "insight"` (project memory). Always use `--json` for programmatic use. `bd prime --hook-json`, `bd prime --memories-only`.

- Sources: https://github.com/gastownhall/beads ; https://github.com/gastownhall/beads/discussions/506 ; SETUP.md [tavily]
- Relationship to codebase: Maps directly to SuperClaude orchestration primitives (discover ready work, claim, update, close, persist memory).

### 4. JSON/CLI contract present but migrating toward envelope mode — HIGH

`--json` is the stable contract (use `--json`, not `--format json`). Schema version `1`. `BD_JSON_ENVELOPE=1` opts into uniform envelope (`schema_version`, `data`); planned default in v2.0. Legacy: object commands include top-level `schema_version`; list commands emit raw arrays; errors emit JSON to stderr with `schema_version`/`error`/`code`. `bd list --json` required: `id`, `title`, `status`, `priority`, `issue_type`, `created_at`. `bd export --json` outputs JSONL, not envelope-wrapped.

- Source: https://github.com/gastownhall/beads/blob/main/docs/JSON_SCHEMA.md [tavily]
- Relationship to codebase: Integration should parse `--json` with envelope compatibility (dual parser for legacy + envelope).

### 5. Issue/dependency graph semantics richer than simple blockers — HIGH

Blocking types affecting `bd ready`: `blocks`, `parent-child`, `conditional-blocks`, `waits-for`. Non-blocking annotations: `related`, `tracks`, `discovered-from`, `caused-by`, `validates`, `supersedes`. `bd ready` = no open blocking dependencies; `bd dep add` rejects cycles at write time. FAQ differentiators: typed dependencies, deterministic ready-work detection, offline-first branch-scoped task memory, AI-resolvable conflicts/duplicate merge, version-controlled SQL database, agent-native APIs.

- Sources: https://github.com/gastownhall/beads/blob/main/docs/DEPENDENCIES.md ; FAQ.md [tavily]
- Relationship to codebase: Maps to SuperClaude wave/planning dependencies. Strong fit as dependency-aware execution graph.

### 6. Gates bridge Beads state to external code/CI state — HIGH

Gates are special issues blocking dependent work until external conditions met. Gate types: `gh:pr` (PR merged), `gh:run` (CI success), `timer` (time elapsed), `bead` (cross-rig issue closed), `human` (manual approval). `bd gate check` evaluates/closes resolved gates; `bd gate discover` matches CI run gates heuristically.

- Source: https://github.com/gastownhall/beads/blob/main/docs/DEPENDENCIES.md [tavily]
- Relationship to codebase: Directly relevant to SuperClaude "work done" vs "merged/validated" distinction. SuperClaude validation/PR-merge phases could be encoded as gates.

### 7. Storage backend is Dolt, not SQLite/JSONL in current versions — HIGH (corrects stale claims)

README: "Beads uses Dolt as its database." Dolt = version-controlled SQL with cell-level merge, native branching, two deployment modes. SYNC_CONCEPTS: "The local Dolt database is the source of truth for `bd list`, `bd show`, `bd ready`, and every write command." `.beads/issues.jsonl` is export/interchange/migration/backup — NOT canonical cross-machine sync. Tools reading old `.beads/issues.jsonl` directly are incompatible with current versions. Use `bd backup` for restorable DB backup.

- Sources: https://github.com/gastownhall/beads ; DOLT.md ; SYNC_CONCEPTS.md ; COMMUNITY_TOOLS.md [tavily]
- Relationship to codebase: **Contradicts the seed-brief's "embedded SQLite or Dolt server-mode" and "`.beads/` Dolt or SQLite + JSONL" framing.** Current Beads is Dolt-first; JSONL is export only.

### 8. Embedded mode vs server mode — HIGH

Embedded (default): in-process Dolt, no external server, data in `.beads/embeddeddolt/`, single-writer with file locking, recommended for solo. Server: connects to `dolt sql-server`, data in `.beads/dolt/`, multiple concurrent writers, configured via `--server-host/port/socket/user` + `BEADS_DOLT_PASSWORD`; `bd init --server`. History: v0.56.1 removed embedded; v0.63.0 reintroduced as default; v1.0.0 carried embedded default stable.

- Sources: https://github.com/gastownhall/beads ; DOLT.md ; discussions/2332 ; DoltHub blog [tavily]
- Relationship to codebase: Server mode required for SuperClaude parallel/multi-agent orchestration; embedded insufficient for concurrent writers.

### 9. Multi-writer behavior and concurrency limitations — HIGH

Server mode supports concurrent writers; embedded is single-writer ("database is locked" under contention). FAQ multi-agent recipe: `bd ready --assignee agent-name`, `bd update <id> --assignee agent-name`, `bd update <id> --status in_progress`, `bd create "..." --deps discovered-from:<parent-id>`, `bd dolt push`/`bd dolt pull`, atomic `bd update <id> --claim --assignee agent-name`. Issues #3400/#3583: active work on session attribution; a bug where `--claim` could lose session info (acceptance criteria included `--session`, `CLAUDE_SESSION_ID`, `BEADS_SESSION_ID`).

- Sources: DOLT.md ; FAQ.md ; discussions/2332 ; issues/3400 ; issues/3583 [tavily]
- Relationship to codebase: Supports multi-agent via server mode + atomic claim, but session attribution/observability is actively changing.

### 10. Sync/remotes use Dolt refs, not source branches or JSONL — HIGH

Cross-machine sync via Dolt remotes; for git-hosted projects, Dolt remote can be same `origin` URL. Dolt stores issue history under `refs/dolt/data`, separate from `refs/heads/main`. `bd init` auto-detects `git remote get-url origin`. First `bd dolt push` publishes `refs/dolt/data`. Fresh clones run `bd bootstrap`. `bd dolt remote add` supports DoltHub, S3, GCS, git SSH, local filesystem.

- Sources: SYNC_CONCEPTS.md ; DOLT.md ; https://github.com/gastownhall/beads [tavily]

### 11. Shared server mode for multi-project/multi-agent machines — MEDIUM-HIGH

One Dolt server at `~/.beads/shared-server/` for all projects. Enable: `bd dolt set shared-server true`, `BEADS_DOLT_SHARED_SERVER=1`, `bd init --prefix myproject --shared-server`. Default shared port 3308 (avoids orchestrator port 3307). Each project needs unique prefix/database name.

- Sources: DOLT.md ; FAQ.md ; DoltHub blog [tavily]

### 12. UI/orchestration ecosystem is broad; current tools must use CLI/Dolt-compatible APIs — HIGH

TUIs: Mardi Gras (real-time, multi-agent orchestration, tmux, Claude Code dispatch), perles. Web UIs: beads-ui, BeadBoard (multi-agent orchestration/dashboard, DAG graph, swarm coordination), beads-web (Dolt direct SQL, drag/drop). Editor/native: VS Code, JetBrains, Neovim, Tauri. Claude Code orchestration: Foolery (wave planning, verification queue), beads-compound, claude-handoff, etc. Warning: tools reading old JSONL directly are incompatible.

- Source: COMMUNITY_TOOLS.md [tavily]

### 13. Git-free/stealth operation exists — MEDIUM

Works without git; `BEADS_DIR` controls `.beads/` location; `bd init --stealth` sets `no-git-ops: true`.

- Source: https://github.com/gastownhall/beads [tavily]

### 14. Migration/backup: `bd backup` for restorable DB, `bd export` for portability — HIGH

`bd backup init/sync/restore/remove/status`. Embedded↔server migration uses backup/restore. `bd export`/`.beads/issues.jsonl` do NOT capture branches, commit history, working-set state, or non-issue tables.

- Sources: https://github.com/gastownhall/beads ; DOLT.md ; FAQ.md [tavily]

### 15. Production readiness: usable but fast-moving with sharp edges — HIGH

FAQ: active 1.x development, dogfooded; core stable but CLI/API changes still happen; safe for dev/internal with backup/sync hygiene; wait for mission-critical without tested backup/restore, enterprise compatibility, or long-term archival as sole record. Issue #2938: user pain from frequent bugs/sharp edges. Active issues around Dolt server daemons, schema migrations, sync, panics.

- Sources: FAQ.md ; issues/2938 ; releases [tavily]

### 16. Third-party writeups can be stale (SQLite/JSONL claims) — HIGH

Peter Warnock and Better Stack describe older SQLite + JSONL architecture; official docs now state Dolt is source of truth and JSONL is export only.

- Sources: peterwarnock.com ; betterstack.com ; SYNC_CONCEPTS.md ; COMMUNITY_TOOLS.md [tavily]

## Key External Findings

1. Current Beads is **Dolt-first**; `.beads/issues.jsonl` is export/interchange only (corrects seed-brief SQLite/JSONL framing).
2. `bd --json` is the integration surface; handle legacy + future envelope mode.
3. `bd ready`, dependency types, and gates provide a credible dependency-aware execution graph.
4. Embedded mode is default and single-writer; multi-agent needs server/shared-server mode.
5. Atomic claim via `bd update <id> --claim`; agent workflows first-class via `bd prime`/`bd remember`.
6. Sync uses Dolt remotes under `refs/dolt/data`.
7. Active UI/orchestration ecosystem with dependency-aware wave planning.
8. Suitable for internal/prototype with backups/version pinning; risky for mission-critical without tested recovery.
9. Official docs contradict older SQLite/JSONL descriptions.
10. Version/release caution necessary (v1.0.5 sync/migration warnings).

## Recommendations from External Research

1. Treat Beads as an orchestration graph candidate, not a markdown replacement. Map SuperClaude tasks/waves to issues/dependencies/gates; use `bd ready --json` as scheduler input; `bd update <id> --claim --assignee <agent>` for acquisition.
2. Integrate through `bd` CLI with `--json` (not JSONL reads); support legacy arrays/objects, envelope mode, and JSON error payloads. Prefer `BD_JSON_ENVELOPE=1`.
3. Require server mode for any multi-agent writer scenario; embedded only for solo evaluation.
4. Pin and gate Beads versions; avoid gated/pre-release builds; include `bd doctor`, backup/restore smoke tests, and push/pull tests in adoption gates.
5. Use Dolt-native sync/backup (`bd dolt push/pull`, `bd bootstrap`, `bd backup`); JSONL only for viewers/interchange.
6. Represent SuperClaude validation/merge barriers as Beads gates (`gh:pr`, `gh:run`, `human`, `timer`).
7. Validate cross-project/cross-rig dependency behavior with the actual CLI (FAQ says no cross-project refs; DEPENDENCIES.md mentions cross-rig — empirically verify).
8. Prefer Dolt-compatible UI tools (beads-ui/beads-web, Foolery/BeadBoard, Mardi Gras); exclude JSONL-direct tools unless updated.
9. Beads can own: dependency DAG, ready queue, task claim/status, durable memory, audit trail, external gates. Mastra/SuperClaude still owns: agent spawning/execution policy, tool permissioning, branch/worktree management, validation/test execution, failure recovery, user-facing command protocol.

## Sources

- https://github.com/gastownhall/beads [tavily]
- https://github.com/gastownhall/beads/blob/main/docs/FAQ.md [tavily]
- https://github.com/gastownhall/beads/blob/main/docs/DOLT.md [tavily]
- https://github.com/gastownhall/beads/blob/main/docs/SYNC_CONCEPTS.md [tavily]
- https://github.com/gastownhall/beads/blob/main/docs/DEPENDENCIES.md [tavily]
- https://github.com/gastownhall/beads/blob/main/docs/JSON_SCHEMA.md [tavily]
- https://github.com/gastownhall/beads/blob/main/docs/COMMUNITY_TOOLS.md [tavily]
- https://github.com/gastownhall/beads/releases [tavily]
- https://github.com/gastownhall/beads/discussions/2332 [tavily]
- https://github.com/gastownhall/beads/issues/2938 ; /3400 ; /3583 ; /3870 [tavily]
- https://www.dolthub.com/blog/2026-05-29-evolving-with-beads [tavily]
- https://betterstack.com/community/guides/ai/beads-issue-tracker-ai-agents [tavily]
