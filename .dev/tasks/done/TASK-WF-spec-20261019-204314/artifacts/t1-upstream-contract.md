# Task 1 upstream contract revalidation

Date: 2026-10-19. Evidence was gathered read-only by the native acquisition implementation worker using curl/WebFetch and by the coordinator using Context7 `/deusdata/codebase-memory-mcp`. No remote installer or release executable was executed.

## Observed source and release

- Upstream main commit API: https://api.github.com/repos/DeusData/codebase-memory-mcp/commits/main — worker reports `32445b200156d23002aa6e11b8a808b2ca856795`, unchanged from design research.
- Latest release API: https://api.github.com/repos/DeusData/codebase-memory-mcp/releases/latest — worker reports tag `v0.12.1`, published `2026-10-16T23:35:48Z`. A Context7 README reference to `v0.11.0` was stale and was not used as the latest-release authority.
- Bootstrap sources read in full by worker: https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/install.sh and https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/v0.12.1/install.sh.
- Release native lifecycle implementation inspected with bounded literal searches: https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/v0.12.1/src/cli/cli.c.

## Relevant observed contract

The main and release-tag bootstrap sources match in the installation behavior used here:

- Default executable destination is `$HOME/.local/bin/codebase-memory-mcp`.
- Supported bootstrap options include `--dir` (separate or equal form), `--clients=...` and `--skip-config`. Both client filtering and config suppression must be omitted to preserve the requested full detected-client/companion setup.
- Linux uses portable release assets; amd64/arm64 aliases and macOS Rosetta selection are upstream-owned.
- SHA-256 verification through `checksums.txt` is mandatory. The archive namespace must contain exactly the binary, license, platform installer and third-party notice.
- The verified candidate runs its native installation with `-y --force --dir=...`. The official bootstrap, not this integration, owns binary activation and companion client configuration.
- The checksum-verified archive's adjacent updater is installed best-effort. Release archives carry that installer; the release asset list does not provide a standalone `install.sh` asset.
- Native install defaults to preserving existing indexes; reset is opt-in. The native uninstaller supports explicit directory and dry-run; `-y` preserves indexes unless deletion is explicitly requested. The adjacent updater is intentionally retained because its ownership cannot be proven.

## Boundaries and remaining release gate

No provenance receipt was established by this inspection: merely finding a canonical executable does not prove it was installed by upstream or that IronClaude owns it. Installation may reuse a working executable; removal must not infer ownership from its filename.

This is bootstrap/tag-source evidence, not verification of the packaged native executable, runtime client configuration merging, a live MCP connection, or graph indexing. The separately authorized smoke test in a disposable environment remains pending and is required before release. No real install/uninstall or developer configuration mutation occurred during this revalidation.
