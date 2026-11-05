# Option A: keep Phase 1's rule; Coder removes it at the first boot on the new image

Read `context.md` first.

- IronClaude: no change to Phase 1 (Tier K keeps the current-pin `serena` entry and prints the removal command).
- Coder (handoff step 5, after the pin bump): the bundle stops registering Serena, and a one-time, idempotent startup migration runs `claude mcp remove serena --scope user` only when the entry equals the bundle's argv, plus `uv tool uninstall serena-agent` and the marker removal. The image drops `/usr/local/bin/codebase-memory-mcp`.
- When "completely absent" holds: on Coder, at the first restart on the image that contains Coder step 5; `./update.sh` on its own does not get there. On non-Coder machines: never automatically; the printed command and the CHANGELOG tell the user.
- Acceptance check (Coder contract test + handoff "Done means"): `jq -e '.mcpServers | (has("serena") or has("codebase-memory-mcp")) | not' ~/.claude.json`, `! command -v serena`, `! command -v codebase-memory-mcp`.

Strengths: no change to Phase 1's carefully debated provenance rule; IronClaude never removes an entry another writer could have made; no flip-flop with the bundle.
Weaknesses: does not meet "absent after `./update.sh`" on non-Coder machines at all, and on Coder only after an image restart; relies entirely on another repo.
