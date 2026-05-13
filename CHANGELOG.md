# Changelog

All notable changes to IronClaude are documented in this file.

## [Unreleased]

### Added

- **Context Freshness System** (`src/superclaude/hooks/scripts/freshness-*.sh`) — seven active shell hooks plus `install_hooks.py` that:
  - Inject a `<session-context>` envelope on every user prompt (turn counter, Δ-since-last-prompt, dirty-git probe, background-agent count).
  - Block `Edit` / `Write` / `mcp__serena__replace_*` / `mcp__serena__insert_*_symbol` against files that have not been Read in the last 30 minutes.
  - Track every Read into `~/.claude/state/reads.jsonl`.
  - Emit telemetry to `~/.claude/logs/freshness-hook.jsonl` for week-1 tuning.
- New `superclaude install` step (`install_hooks`) — atomically copies hook scripts to `~/.claude/hooks/` and additively merges hook registrations into `~/.claude/settings.json` (existing user hooks preserved; backup at `~/.claude/settings.json.bak.<ISO-8601>` before any write).
- `make sync-dev` now also syncs `src/superclaude/hooks/scripts/*.sh` and `src/superclaude/scripts/session-init.sh` into `.claude/hooks/` for local development.
- Context freshness discipline section appended to `src/superclaude/core/CLAUDE.md` — codifies the five content-signal triggers (S1–S5) for citations that hooks cannot catch.

### Fixed

- `src/superclaude/hooks/hooks.json` `session-init.sh` command path changed from the fragile relative `./scripts/session-init.sh` to `~/.claude/hooks/session-init.sh` (Option B from `docs/analysis/hooks-json-relative-path-issue.md`).

### Known v1 limitation

- **External-modification detection is not active in v1.** The design called for a `FileChanged` hook to populate `~/.claude/state/changes.jsonl` and feed the `external_change` block reason in the freshness gate. Live probing in T05.01 revealed that Claude Code's `FileChanged` matcher only accepts pipe-separated literal filenames (not regex, not "watch all"), so the design's `matcher: ".*"` registration silently watched nothing. The FileChanged registration has been removed from v1; the `freshness-file-changed.sh` script remains in `src/` for v1.5 re-implementation. The `freshness-pre-edit.sh` gate still blocks on `no_prior_read` and `read_too_old`, which cover the two highest-impact stale-fact scenarios.
- **`Write` to nonexistent files is blocked.** The freshness gate fires on any `Write` target with no prior Read tracker, which is correct per the design (the gate doesn't check file existence). For fresh-session new-file creation, use Bash heredocs (`cat > new_file <<'EOF'…EOF`). v1.5 may add a "Write to nonexistent path → allow" branch.

### v1.5 work items (freshness-system)

- **FileChanged redesign.** Two viable approaches: (a) static per-project watch list via `|`-separated literal filenames in `matcher`; (b) dynamic via `hookSpecificOutput.watchPaths` returned from `PostToolUse(Read)` — needs a fresh probe to confirm Claude Code accepts watchPaths from non-FileChanged events. After redesign, re-run Test 1 to verify `external_change` block reason fires correctly.
- **`Write`-to-new-file refinement.** Add a "if target path does not exist on disk, allow" branch to `freshness-pre-edit.sh`. Verify the change doesn't introduce a false-allow path (e.g., for race conditions where file was deleted between Read and Write).
- **`install_hooks --no-orphans` flag.** Exclude scripts from the copy list that aren't currently registered in `src/superclaude/hooks/hooks.json`. Cleaner for strict-only deployments; preserves current v1 behavior by default. Today the package copies `freshness-file-changed.sh` even though it's unregistered.
- **`reads.jsonl` rotation.** File grows unbounded; PreToolUse gate scans it on every Edit. Design §2.1 calls for keeping the oldest 3 sessions; implement before users accumulate >10K rows.
- **`session_id` sanitization.** Hook scripts interpolate `session_id` into filenames without a regex check. `validate_session_id()` helper exists in `install_hooks.py` but isn't called by the hook scripts themselves. Defense-in-depth hardening; low priority since Claude Code session_ids are platform-generated UUIDs.

### Notes

- Hooks are user-scope only (`~/.claude/settings.json`). Repo-local hooks are silently bypassed when `--add-dir` is used. To opt out, remove the relevant entries from `~/.claude/settings.json` and delete the corresponding scripts from `~/.claude/hooks/`. See [docs/user-guide/freshness-hooks.md](docs/user-guide/freshness-hooks.md).
