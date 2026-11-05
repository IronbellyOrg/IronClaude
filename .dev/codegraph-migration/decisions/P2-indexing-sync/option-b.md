# Option B: IronClaude SessionStart hook that initializes on first use

Read `context.md` first.

- New hook script `src/superclaude/hooks/scripts/codegraph-session-start.sh`, registered in `hooks.json` SessionStart with matcher `startup` and `timeout: 5`, listed in `_FRESHNESS_SCRIPTS`, mirrored in `plugins/superclaude/hooks/hooks.json`.
- Behaviour (fail-open, always exit 0, prints nothing on stdout so it adds no context):
  1. `command -v codegraph` or exit 0; honour `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0` to opt out.
  2. `top=$(git -C "$CLAUDE_PROJECT_DIR" rev-parse --show-toplevel)` or exit 0 (non-git dirs are never indexed); skip if `top` is `$HOME` or `/`.
  3. If `$top/.codegraph/codegraph.db` exists, exit 0 (watcher and catch-up keep it fresh).
  4. Otherwise start `codegraph init --yes "$top"` detached (`nohup … >"$top/.codegraph-init.log" 2>&1 &` is avoided; log goes to `${XDG_STATE_HOME:-~/.local/state}/superclaude/codegraph-init.log`), guarded by a `mkdir` lock so two sessions do not both init.
- Each worktree gets its own index on the first session opened in it; nested worktrees get their own instead of the parent's with a warning.
- Core CLAUDE.md rule from Option A is kept as the fallback for sessions that start before init finished.

Strengths: works on every machine IronClaude is installed on, not just Coder; per-worktree by construction; no global git config; cost paid once per checkout in the background.
Weaknesses: a background ~1 GB process at first session in a large repo; a new hook script to maintain and test; the first session's early queries may hit "not initialized" until init finishes (seconds to minutes).
