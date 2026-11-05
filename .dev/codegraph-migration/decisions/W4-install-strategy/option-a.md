# Option A: IronClaude-owned verified tarball install (no upstream installer)

Context and evidence: `.dev/codegraph-migration/research/codegraph-evaluation.md` sections 1-5.

## What it does
- `superclaude install` (and so `./update.sh`, which runs `superclaude install --force`) gets a required "CodeGraph" phase that replaces the current Codebase Memory phase (`src/superclaude/cli/main.py:253-262`).
- The phase downloads a **pinned** release, e.g. `https://github.com/colbymchenry/codegraph/releases/download/v1.6.2/codegraph-<os>-<arch>.tar.gz`, and verifies it against a **SHA-256 hard-coded in IronClaude source** per platform (linux-x64, linux-arm64, darwin-x64, darwin-arm64). Optional extra check: `gh attestation verify` when `gh` is authenticated.
- Extracts into `~/.codegraph/versions/v1.6.2/` and links `~/.local/bin/codegraph` and `~/.codegraph/current` (the same layout upstream `install.sh` uses, so `codegraph upgrade` and `codegraph uninstall` still understand it).
- Registers the MCP server itself, like it registers codebase-memory today (`claude mcp add-json ... --scope user`, `install_mcp.py:775-786`):
  `claude mcp add-json codegraph '{"type":"stdio","command":"codegraph","args":["serve","--mcp"],"alwaysLoad":true,"env":{"CODEGRAPH_TELEMETRY":"0","CODEGRAPH_NO_UPDATE_CHECK":"1"}}' --scope user`
- Ships the agent guidance in `src/superclaude/core/CLAUDE.md` (which `superclaude install --force` copies over `~/.claude/CLAUDE.md`), and the `mcp__codegraph__*` permission through IronClaude's own settings handling. Does **not** install the `UserPromptSubmit` prompt hook.
- Never runs `codegraph install`. Receipt + removal logic reuses the existing pattern in `install_codebase_memory.py`.
- Version bumps = edit pin + hashes in one place, tested by unit tests.
- Coder image: does not bake codegraph; a new workspace gets it the first time `superclaude install` runs (the image already runs IronClaude install/update).

## Strengths
- Real integrity check: the hash is pinned in reviewed source, not taken from the same server as the tarball. Upstream `install.sh` does no checksum check at all.
- Deterministic: no "latest" resolution, no self-update, no upstream installer editing `~/.claude.json`, `~/.claude/settings.json` or `~/.claude/CLAUDE.md` behind IronClaude's back.
- Survives `./update.sh`: guidance lives in the file IronClaude overwrites anyway.
- Telemetry off by default, explicitly.
- Same code path on Coder and non-Coder machines; one place to bump.

## Weaknesses
- Most IronClaude code to write and maintain (download, hash table, extract, symlink, receipt, uninstall, tests), roughly mirroring `install_codebase_memory.py`.
- Hash table needs updating per release (4 hashes).
- Every new workspace downloads 63 MB and writes 286 MB under `$HOME` on first install (persistent home volume on Coder, so only once per workspace).
- Misses upstream installer improvements (e.g. future config migrations) unless copied.
