# Option B: retire step that also removes IronClaude-provable binaries and the Serena uv tool

Read `context.md` in this folder first.

## What it does

Everything in Option A (exact user-scope registration removal of `codebase-memory-mcp` and `serena`, shape-matched, via the Claude CLI, verified), plus automatic removal of installed software when IronClaude can argue it owns it:

1. **Kind-B codebase-memory workspaces:** keep a slimmed copy of the receipt-gated removal from `install_codebase_memory.py` (receipt + sha256 identity check, private single-link files) for one release. When the receipt matches `~/.local/bin/codebase-memory-mcp`, run the upstream `codebase-memory-mcp uninstall -y --dir=~/.local/bin` (which removes its own client configs, skills, agents, hooks and instructions, keeps indexes), then `rm` the updater `~/.local/bin/install.sh` and the receipt. External binaries (Coder's `/usr/local/bin` copy) are never touched.
2. **Serena uv tool:** if `uv tool list` shows `serena-agent`, run `uv tool uninstall serena-agent` (removes `~/.local/bin/{serena,serena-agent,serena-hooks}`). Optionally `uv cache clean serena-agent`.
3. Data is still kept: `~/.cache/codebase-memory-mcp`, `~/.serena`, project `.serena/` folders and all indexes stay; the step prints how to delete them.
4. Non-fatal, non-interactive, bounded timeouts (upstream uninstall 60 s, uv 30 s).

## For

- Leaves the most workspaces fully clean with no human step: kind-B workspaces lose the binary and upstream companions; every workspace loses the Serena CLI.
- Reuses existing, already-tested receipt logic instead of inventing new ownership proof.

## Against

- The Serena uv tool is installed by Coder's bundle, not IronClaude (no receipt, no proof of ownership); uninstalling it breaks Coder's bundle health check (`serena --help`) and the bundle reinstalls it on the next start until Coder changes, so it churns and can fail workspace health.
- Keeps a large part of the 759-line `install_codebase_memory.py` (bounded supervisor, receipt parser) alive in a phase whose goal is to delete it, plus its tests; runs an account-wide, prompt-free upstream uninstall, which the current code deliberately forbids without consent (`install_mcp.py:981-986`).
- Upstream uninstall may exceed Coder's 60 s bound; it needs network-free behaviour that is UNVERIFIED.
- Kind-B workspaces may not exist at all (UNVERIFIED), so the cost may buy nothing.
