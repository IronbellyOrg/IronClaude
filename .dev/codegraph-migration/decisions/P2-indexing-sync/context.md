# P2 indexing and sync: shared context for the options

Decision: what IronClaude installs (if anything) so that this worktree and any project a user opens get a codegraph index and keep it fresh. Coder-side automation (image, Orca worktree creation, startup scripts) is researched separately by the Coder agent; this decision is only about what IronClaude itself ships.

## Verified codegraph behaviour (v1.6.2)
- Index is per working tree: `<checkout>/.codegraph/` (SQLite, self-ignoring `.gitignore`). `codegraph init --yes` creates and fully indexes (about 4.5 s and 34 MB for 500 files; ~100 s for 27k files upstream). Peak RSS about 1 GB during init. (`.dev/codegraph-migration/research/codegraph-evaluation.md` §4, §5.4)
- Re-running `codegraph init --yes` on an indexed checkout is a no-op that exits 0 in about 125 ms (P2 sandbox probe, `/tmp/codegraph-eval.fQfO/project`, 2026-10-29). `init` refuses the home directory or a filesystem root without `--force` (`codegraph init --help`).
- `codegraph status` exits 0 even when not initialized; `codegraph query` exits 1 when not initialized (P2 probe).
- Incremental sync: while an MCP client is connected a per-project daemon runs a native file watcher (2 s debounce) and does a connect-time catch-up of edits made while no server ran. `codegraph sync` is for scripts; it fails with a lock error while the daemon holds the writer lock. `codegraph sync --quiet` is documented "for git hooks". (W4 §4, §5.7; `codegraph sync --help`)
- Nothing upstream initializes a new clone or worktree automatically; `codegraph init` installs no git hooks. A nested worktree without its own index is answered from the parent index with a warning; a sibling worktree (IronClaude layout `~/workspaces/worktrees/<repo>/<branch>`) is "not initialized". (W4 §4, §5.8)
- MCP tools are read-only; indexing is CLI-only (W4 §6).

## IronClaude facts
- Hooks ship from `src/superclaude/hooks/hooks.json` (SessionStart already has 3 entries) with scripts in `src/superclaude/hooks/scripts/`, listed in `_FRESHNESS_SCRIPTS` (`src/superclaude/cli/install_hooks.py:42-79`); `make verify-sync` requires every script to be listed; `tests/unit/test_cli_install.py` pins the packaged script list; `plugins/superclaude/hooks/hooks.json` mirrors it.
- Installed core guidance lives in `src/superclaude/core/CLAUDE.md` (copied over `~/.claude/CLAUDE.md` by `superclaude install --force`; on Coder the user's CLAUDE.md is restored afterwards, Coder `catalogue/ironclaude/install.sh:44-66`).
- IronClaude does not touch global git config anywhere today (no `git config --global` in `src/superclaude/cli/`; UNVERIFIED beyond a grep of that directory).
