# Option C: environment-aware: IronClaude removes it off Coder; Coder removes it on Coder

Read `context.md` first.

- IronClaude Phase 2 adds to the retire step: when the codegraph phase succeeded **and** `/etc/aidev02/ironclaude-provenance` does not exist (not a Coder workspace), remove the current-pin Serena entry (exact match, as in Option B). On a Coder workspace, keep it (Phase 1 Tier K) and print that Coder's image update removes it.
- Coder (handoff step 5): bundle stops re-adding; one-time startup migration removes the exact bundle entry; `uv tool uninstall serena-agent`; markers; image drops `/usr/local/bin/codebase-memory-mcp`.
- When "completely absent" holds: non-Coder, right after `./update.sh`; Coder, at the first restart on the image with Coder step 5 (no flip-flop in between, because IronClaude does not fight the bundle).
- Acceptance check: unit tests for both branches (provenance file present/absent, codegraph success/failure); Coder "Done means" check; layer-2 sandbox asserts removal with no provenance file.

Strengths: meets the requirement on non-Coder machines immediately; avoids the remove/re-add churn on Coder; each repo removes what its own installer wrote.
Weaknesses: IronClaude code gains an environment check keyed on a Coder file path (coupling to another repo's layout, UNVERIFIED uniqueness); on Coder, `./update.sh` alone still leaves the entry until the image restart; two code paths to test.
