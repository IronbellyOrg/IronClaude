# Option B: default but non-fatal phase, advisory doctor, documented removal

Read `context.md` in this folder first; this option adds only the contract.

## Contract
- **Default, non-fatal phase.** `superclaude install` always runs "Installing codegraph (default user-level phase)". On failure it prints the failed stage and the exact manual recovery command to stderr, but the phase does not contribute to the exit code: `install` exits 0 if the framework phases succeeded.
- **Doctor: advisory.** New `_check_codegraph` always returns `passed: True`; its `details` (shown with `--verbose`, and a one-line summary always) report missing binary, version drift, missing or stale registration, upstream `CODEGRAPH_START` block or `codegraph prompt-hook` leftovers. `./update.sh` never fails because of codegraph.
- **Removal: documented commands only.** Docs give: `claude mcp remove codegraph --scope user`; `rm -rf ~/.codegraph/versions/v1.6.2 ~/.codegraph/current ~/.local/bin/codegraph` (only for the IronClaude download, which is the only thing at those paths unless the user ran upstream `install.sh`); project indexes `codegraph uninit` per project. No new CLI flag.
- **No receipt.** Ownership is not tracked; IronClaude never deletes anything automatically.

## Code size estimate
`install_codegraph.py` about 140 lines (pin table, discover, download+verify+extract); `install_mcp.py` +60 (phase using generalised helpers); `doctor.py` +30; `main.py` +20. Tests about 22 cases.

## Strengths
- Smallest code; no uninstall surface to maintain.
- Never breaks `./update.sh` or the Coder slug, so ordering with the Coder bake is forgiving: an un-baked image still installs (online) or warns (offline).
- Matches the fact that codegraph is an aid, not a framework dependency: skills fall back to Read/Grep (Phase 1 gap policy).

## Weaknesses
- "Installed by default" can silently not happen; a user may run for weeks without codegraph and not notice (only a stderr line and an advisory doctor detail).
- Coder CI cannot use IronClaude's exit code to prove codegraph is registered; Coder must assert the registration itself.
- Manual removal commands can be run against an upstream `install.sh` copy at the same paths.
