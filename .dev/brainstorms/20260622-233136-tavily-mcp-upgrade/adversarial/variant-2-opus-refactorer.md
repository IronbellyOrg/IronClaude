# Variant 2 — Refactorer Lens

## Position

Apply the smallest safe transformation first: keep local stdio, replace the stale Tavily package, remove or neutralize dead divergent configs, and add regression tests. Avoid turning a package-version correction into a full remote-transport migration.

## Requirements

1. Update the live Tavily registry entry in `src/superclaude/cli/install_mcp.py` from `tavily-mcp@0.1.2` to the chosen current package policy.
2. Prefer one centralized constant or metadata field for the package spec so docs/tests can parse it.
3. Delete the dormant Tavily JSON configs under `src/superclaude/mcp/configs/` and `plugins/superclaude/mcp/configs/`, or rewrite them to explicitly mirror the live registry and mark them non-authoritative. Deletion is preferred because no Python loader uses them.
4. Add a Tavily-specific stale install detector so current name-only installed checks do not skip users on 0.1.x.
5. Keep `TAVILY_API_KEY` env handling unchanged for local stdio but mask values in dry-run output.
6. Treat remote HTTP/OAuth as a documented future option, not the default transport in this change.

## Acceptance Criteria

- No active source file contains `tavily-mcp@0.1.2`.
- A stale existing Tavily install triggers remove/re-add or a clear dry-run description, not "Already installed".
- No dead Tavily config file advertises `mcp-remote` as if it were the live installer.
- Unit tests do not call the real Claude CLI.
