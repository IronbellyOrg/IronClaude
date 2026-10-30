# Option C: no automatic cleanup in `superclaude install`; explicit consented command plus handoffs

Read `context.md` in this folder first.

## What it does

1. `superclaude install` gains nothing; it simply stops installing codebase-memory (Phase 1 removal).
2. A new explicit command `superclaude mcp --retire-legacy [--dry-run] [--yes]` previews and, after interactive confirmation (or `--yes`), removes the exact user-scope `codebase-memory-mcp` and `serena` registrations (shape-matched, via the Claude CLI, verified) and prints the manual commands for binaries, uv tools and data.
3. `superclaude install` prints a one-line notice when either legacy registration is present: "Legacy MCP registrations found; run `superclaude mcp --retire-legacy` to remove them."
4. Coder workspaces: the Phase 2 Coder handoff tells Coder's startup to remove the registrations, bundle install and image binary itself.
5. Docs tell dev-workspace users to run the command once after `./update.sh`.

## For

- Keeps the existing consent rule for every removal (no prompt-free mutation of the user's MCP configuration).
- Smallest risk of surprising a user who registered their own `serena` by hand; still shape-matched.
- No change to the pinned `update.sh` command list.

## Against

- Does not meet the goal as written: `./update.sh` alone leaves both registrations in place until a human runs another command (a registration pointing at a binary the Coder image will stop shipping).
- Adds a new CLI flag, help text, docs and tests that exist only for the migration, then must be removed.
- Coder workspaces depend entirely on the Coder repo's schedule.
