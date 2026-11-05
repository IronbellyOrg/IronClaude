# P2 decision: who removes the current-pin Serena registration (and other Coder leftovers) on existing workspaces

## Requirement (user, via coordinator; `.dev/codegraph-migration/orchestration/README.md` "Coordinator concerns")
After `./update.sh` on an existing workspace, Serena and codebase-memory must be **completely absent**. The combined plan (Phase 1 + Phase 2 + Coder handoff) must remove the user-scope `serena` registration on existing workspaces, name who removes it and when, and have an acceptance check. Missing that is a CRITICAL finding.

## Verified facts
- The live entry on this Coder workspace: user scope `serena` = `uvx --from serena-agent==1.7.0 serena start-mcp-server --context claude-code --project-from-cwd --enable-web-dashboard false --enable-gui-log-window false` (`inventory/serena.md` E1/E2). This argv is identical to IronClaude's own registry entry (`src/superclaude/cli/install_mcp.py:59`, written by `superclaude mcp --servers serena`), the IronClaude docs command, and Coder's bundle (`T/catalogue/mcp-bundle-core/install.sh:74-75`; its comment at `:17` says it mirrors IronClaude's `MCP_SERVERS` pin).
- Phase 1 spec §3.2 (`specs/phase-1-removal-spec.md`) classifies that argv as **Tier K: kept** and prints `claude mcp remove serena --scope user`, because IronClaude cannot prove it wrote it. Three older argv shapes only IronClaude code produced are removed (Tier R).
- Coder's bundle re-adds `serena` on every workspace start if absent (`install.sh:67-119`) and installs `serena-agent` with `uv tool` (`:148-170`); `superclaude install` reruns on Coder only when the image's IronClaude SHA changes (`T/catalogue/ironclaude/install.sh:88-95`).
- `/usr/local/bin/codebase-memory-mcp` is root-owned and baked by the image (`Dockerfile.coder:323-351`); user `coder` cannot delete it; only a new image removes it. The `codebase-memory-mcp` registration IS removed by Phase 1's retire step (Tier R, absolute path with that basename).
- On non-Coder machines (dev checkouts running `./update.sh`) the current-pin `serena` entry can exist only if the user ran IronClaude's `superclaude mcp --servers serena` or copied IronClaude's docs command. No bundle re-adds it there.
- Coder workspaces carry `/etc/aidev02/ironclaude-provenance` (mode 0444, `Dockerfile.coder:395-399`); non-Coder machines do not (UNVERIFIED that no other environment creates that path).
- Phase 2 makes codegraph a required phase that runs immediately before Phase 1's retire step; the retire step currently runs regardless of the codegraph result (Phase 2 spec §2.1).
- Removing a user-scope entry is reversible by the user (`claude mcp add …`); the entry carries no secrets (no env/headers).
