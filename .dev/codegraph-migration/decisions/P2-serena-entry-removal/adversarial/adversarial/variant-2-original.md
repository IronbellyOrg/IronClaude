# Option B: replacement-based retirement in IronClaude once codegraph is registered, plus Coder for what IronClaude cannot touch

Read `context.md` first.

- IronClaude Phase 2 adds one rule to Phase 1's retire step (`install_retired_mcp.py`): when the codegraph phase in the same run returned success (registration verified), the current-pin Serena argv (Phase 1's Tier K row 1, exact `command` + `args`, stdio, no env/headers) is promoted to removed. Rationale: every known writer of that exact argv is IronClaude or a declared mirror of IronClaude's pin; the replacement is now registered, so removing it is a replacement, not a deletion. Other Tier K shapes (`--project <path>`, `ide-assistant` bare form, anything else with `start-mcp-server`) stay kept.
- If the codegraph phase failed, nothing changes from Phase 1 (Serena kept, so the user is never left with neither).
- Coder (handoff step 5): stop the bundle from re-adding `serena` in the same Coder change that the pin bump depends on, or IronClaude's removal is undone at the next boot; `uv tool uninstall serena-agent`; markers; image drops `/usr/local/bin/codebase-memory-mcp`. Until then a Coder workspace flips back to Serena at boot (registration only), visible in the next `superclaude install` output.
- When "completely absent" holds: non-Coder machines, right after `./update.sh` (registration gone; no Serena binary was installed by IronClaude). Coder: registration gone after `./update.sh` or the slug run; binaries and uv tool gone at the first restart on the image with Coder step 5.
- Acceptance check: a Phase 2 unit test (current-pin entry removed only when codegraph succeeded; kept otherwise); layer-2 sandbox step seeding the current-pin entry and asserting `jq -e '.mcpServers | has("serena") | not'` after install; the Coder "Done means" check above plus `! command -v serena`, `! command -v codebase-memory-mcp`.

Strengths: meets the requirement after `./update.sh` wherever IronClaude can act; never leaves a user with neither server; one small, test-pinned rule.
Weaknesses: overrides part of Phase 1's provenance rule (a hand-typed copy of the docs command is removed); flip-flop on Coder until Coder step 5 lands; Phase 2 edits a Phase 1 module.
