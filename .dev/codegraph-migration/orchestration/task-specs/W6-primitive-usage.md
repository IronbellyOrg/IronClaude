Task W6: semantic usage map of codebase-memory and Serena inside primitives (skills, commands, agents, refs, hooks, core docs).

First read /home/coder/workspaces/worktrees/IronClaude/feat-codememory-codegraph-init/.dev/codegraph-migration/orchestration/README.md (shared rules; binding).

Target: `src/superclaude/{skills,commands,agents,core,hooks,templates,mcp}` and `plugins/superclaude/` (mirror). Also the user's installed ~/.claude/{skills,agents,hooks,CLAUDE.md} read-only, to catch primitives added by the upstream codebase-memory installer, and `~/.claude/CLAUDE.md` / `src/superclaude/core/CLAUDE.md` MCP tables and flags (`--serena`).

Change: write `.dev/codegraph-migration/inventory/primitive-usage.md` with:
1. One row per (primitive, reference): primitive path, line, server (codebase-memory | serena), tool or concept named (e.g. `mcp__serena__find_symbol`, `search_graph`, "Serena memory", `--serena` flag, allowed-tools frontmatter), the JOB the primitive uses it for (symbol lookup, reference tracing, impact analysis, architecture overview, memory persistence, symbol-level edit, onboarding...), and whether it is load-bearing (the workflow fails or degrades without it) or decorative (mention only).
2. Grouping by job, with counts, so Phase 3 can design one replacement per job.
3. Frontmatter/tool allowlists (`tools:`/`allowed-tools:` in agents and skills, settings permissions) that name these servers' tools, since those must change in Phase 1 or 3.
4. Tests that pin these references (e.g. tests asserting a primitive mentions serena) with `path:line`.
5. `## Decisions` section (likely empty).

Constraints: read-only. Do not propose codegraph replacements in detail (Phase 3 planner does that); you may add a one-line hint per job.

Ownership: write only `.dev/codegraph-migration/inventory/primitive-usage.md`.

Observable acceptance: file exists; includes the exact rg commands and hit counts; every load-bearing row has a quoted line.
