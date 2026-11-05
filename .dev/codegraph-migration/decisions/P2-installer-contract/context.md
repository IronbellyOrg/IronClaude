# P2 installer contract: shared context for the options

Decision: what contract the new `superclaude install` codegraph phase has (required or not, how doctor reports, how removal works). Everything below is common to every option and is already decided (W4 adversarial, `.dev/codegraph-migration/research/codegraph-evaluation.md` section 7).

## Already decided baseline (all options)
- Pin `v1.6.2` in IronClaude source with a SHA-256 table from the release `SHA256SUMS`: linux-x64 `ef0af416…b828`, linux-arm64 `c8c6be29…5b64`, darwin-x64 `53d1a4d1…f9bc`, darwin-arm64 `d74d1bfb…662e`.
- Reuse first: a `codegraph` whose `--version` prints exactly `1.6.2` (PATH winner, for example the Coder-baked `/usr/local/bin/codegraph`, then `~/.local/bin/codegraph`) is used with no network.
- Fallback: download `https://github.com/colbymchenry/codegraph/releases/download/v1.6.2/codegraph-<os>-<arch>.tar.gz`, verify SHA-256, extract to `~/.codegraph/versions/v1.6.2/`, link `~/.local/bin/codegraph` and `~/.codegraph/current`. Never run upstream `install.sh` (no checksum step) or `codegraph install` (writes a `~/.claude/CLAUDE.md` block that `superclaude install --force` erases, and a prompt hook).
- Register: `claude mcp add-json codegraph '{"type":"stdio","command":"<abs realpath>","args":["serve","--mcp"],"alwaysLoad":true,"env":{"CODEGRAPH_TELEMETRY":"0","CODEGRAPH_NO_UPDATE_CHECK":"1"}}' --scope user`, verify by re-reading `~/.claude.json`, restore previous entry on failure (existing pattern `src/superclaude/cli/install_mcp.py:815-913`).

## Verified constraints that shape the contract
1. `./update.sh` is `set -euo pipefail`, then `pipx install --force ./`, `superclaude install --force`, `make sync-dev`, `superclaude doctor` (`update.sh:2-10`). A non-zero `install` or a failing doctor check turns `./update.sh` red.
2. `superclaude install` aggregates phase flags and exits 1 if any is false (`src/superclaude/cli/main.py:264-275`). Codebase Memory is a required phase today (`main.py:254-262`); Phase 1 removes it.
3. Coder runs `timeout 60 superclaude install … </dev/null`; non-zero exit fails the `ironclaude` slug and no install marker is written (Coder `catalogue/ironclaude/install.sh:120-123`). Coder CI runs that install with `--network=none` and expects exit 0 (Coder `test-57-catalogue-configure.sh:228`, `coder-ci-aidev02-contract.yml:1221`). So a required phase is only safe once the image bakes the pinned binary first.
4. `superclaude doctor` has five checks and no MCP check today (`src/superclaude/cli/doctor.py:16-49`); exit 1 if any check fails (`main.py:508-512`); `make verify` greps for "SuperClaude is healthy" (`Makefile:42`).
5. Phase 1 deletes the Codebase Memory `--uninstall`/`--yes` flags from `superclaude mcp` (W1 inventory step 3). Today the only MCP removal path is that flag.
6. Existing safety rules to keep: exact user-scope entry only, remove through `claude mcp remove`, never replace an entry carrying `env`/`headers` that the user wrote, never delete an external (unowned) binary, receipt proves ownership (`install_codebase_memory.py:297-304`).
7. The 759-line `install_codebase_memory.py` is deleted by Phase 1. "Prefer the smallest correct code" is a project rule.
8. A daemon may keep the old version dir busy for 300 s after use (W4 §5.7); IronClaude must not delete the active version dir under a running daemon.
