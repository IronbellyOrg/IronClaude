# Option A: no IronClaude automation; guidance plus the upstream watcher

Read `context.md` first.

- IronClaude installs nothing for indexing. Fresh-index ownership goes entirely to the user and to Coder (worktree creation and workspace startup).
- `src/superclaude/core/CLAUDE.md` gains a short rule: "if a codegraph tool reports the project is not initialized, run `codegraph init --yes` at the git top-level, then retry; never run `codegraph sync` while a session is open (the daemon owns the index)".
- Freshness after the first index is the upstream watcher plus connect-time catch-up.
- Docs page lists `codegraph init --yes`, `codegraph uninit`, and `codegraph.json` excludes.

Strengths: zero new code, no hook latency, no surprise 1 GB RSS process at session start, no new failure mode.
Weaknesses: every new clone or worktree starts unindexed; the first agent that needs the graph pays a turn (or forgets and falls back to grep); outside Coder nothing ever automates it.
