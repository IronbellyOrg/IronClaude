# codegraph migration planning run (issue #323)

Shared context for every worker in this run. Read this file first.

## Goal
Plan (do NOT implement) the removal of codebase-memory-mcp and Serena MCP from IronClaude and their replacement by codegraph (https://github.com/colbymchenry/codegraph). Tracking issue: https://github.com/IronbellyOrg/IronClaude/issues/323.

Worktree (repo root for every path below): /home/coder/workspaces/worktrees/IronClaude/feat-codememory-codegraph-init
Branch: ironbelly/feat-codememory-codegraph-init. Base: master.

## Phases being planned
1. Phase 1, removal: remove codebase-memory-mcp and Serena entirely (installers, `update.sh` path, `superclaude install`/`update`, skills, commands, agents, refs, hooks, core docs, plugin mirror `plugins/superclaude/`, docs, tests, user-environment registration) so that running `./update.sh` or creating a fresh Coder workspace leaves both absent. Historical `.dev/` artifacts stay untouched. Removal from other IronbellyOrg repos is planned (inventory + handoff), not executed here.
2. Phase 2, install codegraph: install and test codegraph; make `superclaude install` install it by default and `./update.sh` install it on existing workspaces; write a handoff prompt plus documents for the Coder repo (IronbellyOrg/Coder) so existing workspaces, on update, remove codebase-memory and Serena and install and sync codegraph. The handoff must tell the Coder agent to research what other configuration keeps new worktrees and projects indexed/synced on clone or creation.
3. Phase 3, adopt codegraph: map every skill, command, ref, agent and hook that used codebase-memory or Serena to the simplest codegraph equivalent; brainstorm further codegraph uses; design 2-3 new commands built around codegraph (callable by other skills or standalone).

## Known facts (coordinator-verified 2026-10-29)
- `update.sh` (10 lines) runs: `pipx install --force ./`, `superclaude install --force`, `make sync-dev`, `superclaude doctor`.
- `superclaude install` has a REQUIRED Codebase Memory phase: `src/superclaude/cli/main.py:254-262` calls `install_codebase_memory_mcp` (`src/superclaude/cli/install_mcp.py:815`), which uses `src/superclaude/cli/install_codebase_memory.py` (upstream install.sh acquisition, receipt, removal).
- Codebase-memory hits outside `.dev/` and `.claude/`: docs/reference/mcp-server-guide.md, docs/user-guide/mcp-installation.md, src/superclaude/cli/{install_codebase_memory.py,install_mcp.py,main.py}, tests/cli/{test_install_codebase_memory.py,test_install_mcp_registry.py,test_install_mcp_tavily.py,test_update_command.py}.
- Serena: about 166 files outside `.dev/`/`.claude/` mention it (73 under src/superclaude, 32 tests/cli, 18 plugins/superclaude, docs, README, CLAUDE.md, SECURITY.md).
- Live user environment (`claude mcp list`): `serena` registered as `uvx --from serena-agent==1.7.0 serena start-mcp-server ...`; `codebase-memory-mcp` registered as `/usr/local/bin/codebase-memory-mcp` (baked by the Coder image, `templates/VSCode-AIDev02/Dockerfile.coder` lines 323-351 in IronbellyOrg/Coder). Upstream codebase-memory install may also add companion skills/agents/hooks/instructions to ~/.claude, ~/.codex, ~/.config/opencode.
- The user's global `~/.claude/CLAUDE.md` (installed from `src/superclaude/core/CLAUDE.md`) lists serena as an MCP server.

## Rules for every worker
- Planning run only. Do NOT edit source, tests, docs, `~/.claude`, `~/.claude.json` or any MCP registration. Write only your assigned output file(s) under `.dev/codegraph-migration/`.
- Never run `claude mcp add/remove`, `superclaude install`, `./update.sh`, `make sync-dev`, or anything that mutates the real user environment or other repos. No git commits, no pushes, no cross-repo edits, no GitHub comments.
- Tests: do not run the full suite or `tests/cli/eval/` (it rewrites the tracked file `.dev/releases/current/cliEval/evidence/T02.15/perf.json`). Run only specific test files you need to confirm a claim. After any command, `git status --short` must show no modified tracked file; if one appears because of you, say so in your report.
- Use `uv run` for Python (it may create the gitignored `.venv`; that is acceptable). For standalone parsing scripts use `uv run --no-project`. Prefer rg/Read over MCP tools that are being removed (do not depend on codebase-memory or Serena tools for your investigation).
- Create your output file as a header stub first, then fill it section by section.
- Every claim cites `path:line` (or a URL) you actually read. Mark anything unverified as UNVERIFIED.
- Decisions: make simple decisions yourself. For a mid-level decision (two or more viable options with real trade-offs), write each option to a short file under `.dev/codegraph-migration/decisions/<task>-<slug>/option-<x>.md` and spawn an agent (Agent tool) to invoke `/sc:adversarial --compare <option files> --depth quick`; for a complex/architectural decision do the same without `--depth quick` (default standard depth). Follow its recommendation. Never stop to ask the user. Record every autonomous decision in a `## Decisions` section of your output as: decision, options considered, method (self / adversarial quick / adversarial full), rationale.
- Skills: only use a skill when your task spec says it has positive return. Do not run /task-builder or /sc:analyze in this run.
- Finish with `worker_done` per your Orca preamble, `--report-path` set to your output file.

## Coordinator concerns for the reviewer (task R) and finalizers (F1-F3)
- User requirement: after `./update.sh` on an existing workspace, Serena and codebase-memory must be **completely absent**. Phase 1 spec section 3 keeps the user-scope `serena-agent==1.7.0` registration because Coder's MCP bundle writes the identical argv, and relies on the Coder handoff to close it. Check that the combined plan (Phase 1 + Phase 2 + Coder handoff) actually removes that registration on existing workspaces after update, names who removes it and when, and has an acceptance check for it. If it does not, that is a CRITICAL finding.
- Cross-phase amendment (from P2): Phase 2 decided that IronClaude removes every user-scope Serena launcher entry once codegraph is ready, and that Coder stops its bundle re-adding Serena before the IronClaude merge. The Phase 1 spec must be amended to that "Serena gate" (Phase 2 spec task T0b). F1 owns that amendment to the Phase 1 spec; the reviewer must check the two specs agree.
- Known residuals `./update.sh` cannot remove (from P2): the root-owned baked `/usr/local/bin/codebase-memory-mcp` (removed by Coder's new image) and an upstream-installed `~/.local/bin/codebase-memory-mcp` with its companion files (uninstall command printed). The reviewer must check each has a named owner and an acceptance check.
- Phase 3 was written while the Phase 1 spec was still a stub, so it designs for both gap-policy outcomes and marks Phase 1's policy UNVERIFIED. The actual Phase 1 policy is: load-bearing Serena steps are rewritten to a Grep/Read floor in Phase 1, with a slots ledger that Phase 3 upgrades to codegraph. F3 must reconcile Phase 3 to that, and the reviewer must check the slots ledger and Phase 3's per-primitive rows match.
- Cross-phase dependency (from P3): Phase 3 needs Phase 2 to set `CODEGRAPH_MCP_TOOLS=node,search,callers,callees,impact,files,status` (default exposes only `codegraph_explore`) after a schema-cost check. F2 owns adding that to Phase 2; the reviewer must check it is present.
- For F3 (from F2, see `.dev/codegraph-migration/review/F2-result.md`): Phase 2 now sets `CODEGRAPH_MCP_TOOLS` only after a schema-cost check in its T2 step 0. The measured delta today (7,597 bytes) sits in the close-call band, so an executor without a logged-in `claude` ships `CODEGRAPH_MCP_TOOLS=status`. Phase 3 must therefore work in both cases: full tool list, or `status` only with the codegraph CLI as fallback. Phase 2 also ships the init hook, so Phase 3 must not assume nothing runs `codegraph init`. Read the revised Phase 2 spec before editing Phase 3.
- Test baseline: W1 observed 27 failures and 16 errors on the full suite at the branch base, none in codebase-memory files. Every "tests stay green" check must compare against a recorded baseline, not assume a clean suite.
