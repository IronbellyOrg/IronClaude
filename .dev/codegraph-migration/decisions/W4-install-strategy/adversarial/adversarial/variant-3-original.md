# Option C: bake the binary in the Coder image; IronClaude only verifies and registers

Context and evidence: `.dev/codegraph-migration/research/codegraph-evaluation.md` sections 1-5. Today codebase-memory-mcp is baked this way at `/usr/local/bin/codebase-memory-mcp` by `templates/VSCode-AIDev02/Dockerfile.coder` in IronbellyOrg/Coder (coordinator-verified fact in the orchestration README).

## What it does
- Coder `Dockerfile.coder` downloads the pinned `codegraph-linux-<arch>.tar.gz`, checks a pinned SHA-256 at build time, extracts to `/opt/codegraph/v1.6.2/`, and links `/usr/local/bin/codegraph`. Sets `CODEGRAPH_TELEMETRY=0` in the image env.
- `superclaude install` codegraph phase: checks `codegraph --version` equals the IronClaude-expected version; if present, only registers the MCP server (`claude mcp add-json codegraph '{...alwaysLoad...}' --scope user`) and relies on `src/superclaude/core/CLAUDE.md` for guidance. If missing (non-Coder machine), it fails with a clear message, or falls back to Option A's verified download (if both are built).
- Version bumps require an image rebuild plus an IronClaude pin bump, kept in sync.

## Strengths
- New workspaces start with codegraph already on PATH: no first-run 63 MB download, no 286 MB per-home copy, works offline.
- Root-owned binary in `/usr/local/bin`, not user-writable; matches the current codebase-memory pattern, so the Coder team already knows it.
- Build-time hash check gives the same integrity as Option A for Coder users.

## Weaknesses
- Two repos must agree on the version; existing workspaces only get a new codegraph after an image rebuild/restart, while IronClaude `./update.sh` may expect a newer one.
- Non-Coder installs (macOS dev laptops, other Linux) still need an install path: without Option A's fallback, `superclaude install` cannot make codegraph available there.
- `codegraph upgrade` cannot update a root-owned `/usr/local/bin` install from a user shell; upgrades must go through the image.
- Image size grows by ~286 MB uncompressed.
