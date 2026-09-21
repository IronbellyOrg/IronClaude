# Pre-change sync baseline

- **Command:** `make verify-sync`
- **Exit code:** `2` (recorded in `verify-sync-pre.exit`)
- **Classification:** Pre-existing, unrelated source/mirror drift.
- **Observed causes:** generated `.claude/skills/sc-bare-review/` has extra refs/scripts; several installed skills/hooks are missing matching source distributions. No MCP registry/config path appeared in the failure output.
- **Policy:** Run `make sync-dev` after source edits. A post-change `make verify-sync` success is preferred; an identical failure is baseline/non-blocking. Do not repair or stage unrelated generated `.claude/` content.
