# Option A: registration-only "retire legacy MCP servers" step inside `superclaude install`

Read `context.md` in this folder first.

## What it does

A new non-interactive step runs at the end of every `superclaude install` (so `./update.sh` and Coder's `ironclaude/install.sh` both reach it). For each retired server name it:

1. Reads the exact top-level user-scope entry with the existing `read_user_mcp_entry(name)` (no subprocess when the entry is absent; zero cost on fresh workspaces).
2. Removes it only if it matches a known IronClaude/Coder-written shape:
   - `codebase-memory-mcp`: `type` stdio (or absent), `args` `[]`, `command` whose basename is `codebase-memory-mcp`, no `env`/`headers`.
   - `serena`: stdio, argv (command + args joined) contains `serena-agent` and `start-mcp-server`, no `env`/`headers`.
3. Removes through `claude mcp remove <name> --scope user` (existing `_run_registration_command`, timeout lowered to 10 s), then re-reads to verify absence.
4. Never touches local scope (`projects.*.mcpServers`), project `.mcp.json`, a same-named user entry with a different shape (reported as "kept: not an IronClaude registration"), binaries, uv tools, caches, indexes, `~/.serena`, project `.serena/` folders.
5. Prints one line per action plus the manual commands for what it does not own (`uv tool uninstall serena-agent`, `codebase-memory-mcp uninstall -y` for kind-B workspaces, `rm -rf ~/.serena` "only if you no longer need Serena data").
6. Is non-fatal: a failed or unverifiable removal prints a warning and does not change the install exit code (a lookup failure never blocks a framework install). Missing `claude` CLI: skip with a note (same pattern as `install_plugins`).

Implementation: one small module (or a block in `install_mcp.py`) with a `RETIRED_MCP_SERVERS` table of name -> matcher, reusing `read_user_mcp_entry` and a name-parameterised version of `_cleanup_user_native_registration`. The parameterised helper is also what Phase 2's codegraph registration wants. About 4-6 unit tests plus one CLI integration test (temp HOME, stub `claude`). Sunset: the table carries a comment "remove after the first release in which Coder's image and bundle no longer ship either server" (a later cleanup task).

Stale primitives and hook matcher need no extra step: no primitive file is retired in Phase 1, and the forced install rewrites the hook matcher and `~/.claude/CLAUDE.md`.

## For

- Meets the goal on both paths (`update.sh`, Coder SHA bump, pipx users) with no prompt, no root and no network; works under Coder's 60 s bound (two local file reads; at most two ~0.25 s CLI calls).
- Narrowest blast radius: only removes entries IronClaude or Coder wrote, identified by exact shape; keeps every existing safety rule (exact user scope, CLI-only mutation, verify, no secret echo).
- Zero new destructive behaviour on user data; matches existing keep-indexes policy.

## Against

- Leaves the kind-B binary and upstream companions (if any kind-B workspace exists) behind with only a printed command; deleting `install_codebase_memory.py` removes the only automated path for them.
- Adds new code that names both servers to a tree being cleaned (needs an allowlist in the acceptance search and a later removal).
- On Coder, the bundle re-adds `serena` on the next workspace start until Coder's own change lands (the step is undone, harmlessly, for a while).
