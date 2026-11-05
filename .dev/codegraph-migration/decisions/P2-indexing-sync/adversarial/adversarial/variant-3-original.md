# Option C: IronClaude installs global git template hooks

Read `context.md` first.

- `superclaude install` writes `~/.config/superclaude/git-template/hooks/{post-checkout,post-merge,post-rewrite}` and sets `git config --global init.templateDir` to it (only when unset), so every new `git clone`/`git init` copies the hooks. The hooks run `codegraph init --yes` if no index exists, else `codegraph sync --quiet` (ignoring the lock error when a daemon is running).
- Existing checkouts get nothing until re-cloned (templates only apply at clone/init); `git worktree add` runs `post-checkout` from the main repo's hooks dir, so worktrees of a templated repo get initialized.
- Core CLAUDE.md fallback rule as in Option A.

Strengths: indexes on clone and worktree creation, before any session; keeps the index fresh across branch switches and pulls even when no MCP client is connected.
Weaknesses: mutates the user's global git config (IronClaude never does this today); collides with `core.hooksPath` users (pre-commit, husky) where templates are ignored; does nothing for existing clones; hook runtime (1 GB, seconds to minutes) lands on `git clone`/`checkout` in the foreground unless backgrounded; `sync` fights the daemon's writer lock.
