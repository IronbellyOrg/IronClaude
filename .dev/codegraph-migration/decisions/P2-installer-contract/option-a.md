# Option A: required phase, strict doctor, CLI uninstall

Read `context.md` in this folder first; this option adds only the contract.

## Contract
- **Required phase.** `superclaude install` runs "Installing codegraph (required user-level phase)"; any failure (no Claude CLI, unsupported platform with no matching binary, download or checksum failure, registration failure) makes the command exit 1 after all other phases ran (same aggregation as `main.py:264-275`).
- **Doctor: hard check.** New `_check_codegraph` in `doctor.py` fails when: no `codegraph` with version `1.6.2` is found, the user entry `codegraph` in `~/.claude.json` is absent or differs from the expected shape, or `~/.claude/CLAUDE.md` holds a `CODEGRAPH_START` block / `settings.json` holds a `codegraph prompt-hook` hook. A failure makes `./update.sh` exit 1.
- **Removal: CLI.** Keep (re-scope) `superclaude mcp --uninstall --servers codegraph [--yes] [--dry-run]`: removes the exact user entry through `claude mcp remove codegraph --scope user`; removes `~/.codegraph/versions/<tag>`, `~/.codegraph/current` and `~/.local/bin/codegraph` only when a private receipt `~/.codegraph/.superclaude-receipt.json` (tag, sha256, paths) written by IronClaude's own download matches; never touches a baked/external binary or any `.codegraph/` project index.
- **Receipt.** Written after a verified download; holds the tarball sha256 and the link targets.

## Code size estimate
New module `install_codegraph.py` about 220 lines (platform map, pin table, discover, download+verify+extract, receipt, removal); `install_mcp.py` gains about 80 lines (phase + uninstall) using generalised registration helpers; `doctor.py` +40; `main.py` +30 (phase, `--list` block, uninstall flags kept). Tests about 35 cases.

## Strengths
- Strongest guarantee: a workspace where `./update.sh` is green definitely has a working, registered, pinned codegraph.
- Same lifecycle shape users already know from Codebase Memory (install, list, uninstall).
- Drift (stale bake, upstream `codegraph install` leftovers) is surfaced loudly.

## Weaknesses
- Any transient network or GitHub failure on a machine without the bake turns `./update.sh` red twice (install and doctor).
- Coder must bake before the IronClaude pin bump, or every Coder workspace slug fails; strict doctor adds a second failure point.
- Keeps an uninstall surface that Phase 1 just deleted, so more code and tests.
- macOS developers without network get a red install.
