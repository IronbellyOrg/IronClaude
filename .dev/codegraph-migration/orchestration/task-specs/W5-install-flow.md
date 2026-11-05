Task W5: IronClaude install/update flow and Coder workspace touchpoints.

First read /home/coder/workspaces/worktrees/IronClaude/feat-codememory-codegraph-init/.dev/codegraph-migration/orchestration/README.md (shared rules; binding).

Target: `update.sh`, `Makefile`, `pyproject.toml`, `src/superclaude/cli/main.py` (install, update, doctor, mcp commands), `src/superclaude/cli/install_mcp.py`, `src/superclaude/cli/install_*.py` (user setup, hooks, settings defaults), `src/superclaude/core/` files installed to ~/.claude, `.claude/settings.json`, and in IronbellyOrg/Coder (read-only through `gh api repos/IronbellyOrg/Coder/contents/...`): `templates/VSCode-AIDev02/Dockerfile.coder`, the workspace update/startup scripts and tests that run `superclaude install` or reference codebase-memory/serena (find them with `gh search code 'repo:IronbellyOrg/Coder superclaude'` and similar).

Change: write `.dev/codegraph-migration/research/install-update-flow.md` with:
1. Step-by-step flow of `./update.sh` and `superclaude install` / `superclaude update` / `superclaude install --list` / `superclaude doctor` / `superclaude mcp`, with `path:line` for each phase, showing exactly where an MCP server is installed and registered, which phases are required versus optional, and which exit codes they drive.
2. The extension point a new required codegraph phase should use (reuse existing helpers, e.g. the generic MCP_SERVERS registry or the native-binary pattern), and the minimum code shape. Do not design the whole thing; identify the seams.
3. How removal of previously installed servers on existing workspaces could be triggered by `./update.sh` / `superclaude install` (is there any existing "migration" or cleanup mechanism? if not, say so), and the safety rules the existing codebase-memory uninstall path follows (receipts, exact user scope) that a codegraph-era cleanup should keep.
4. Coder touchpoints: where the Coder image or its startup/update scripts install, bake, register, test or pin codebase-memory, Serena or IronClaude (`ARG IRONCLAUDE_GIT_SHA`, tests that assert codebase-memory registration, the auto-bump workflow). Output as a list of Coder `path:line` items with what each does. This is input for a handoff prompt, not a Coder implementation plan.
5. Ordering constraints between an IronClaude release and a Coder pin bump (what breaks in Coder CI if IronClaude stops requiring codebase-memory first, and vice versa).
6. `## Decisions` section.

Constraints: read-only. No Coder clones that write outside /tmp.

Ownership: write only `.dev/codegraph-migration/research/install-update-flow.md`.

Observable acceptance: file exists; every flow step has a `path:line`; the Coder list cites Coder paths with line numbers from the fetched contents.
