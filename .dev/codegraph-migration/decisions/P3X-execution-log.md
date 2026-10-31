# Phase 3 execution log (issue #323)

Plan: `.dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/TASK-WF-phase3CodegraphA-20261029-204913.md` (source `./source.md`), executed with `/sc:implement` in worktree `.dev/worktrees/codegraph-adoption` on branch `feat/codegraph-adoption`.

## Gate and baselines (Task 1, 2026-10-31)

| Check | Command | Result |
|---|---|---|
| G1 | `command -v codegraph && codegraph --version` vs `install_codegraph.VERSION` | PASS: `/home/coder/.local/bin/codegraph` prints `1.6.2`; pin `VERSION` = `1.6.2`. Recorded per G1: `~/.codegraph/.superclaude-bin` holds `/opt/codegraph/v1.6.2/bin/codegraph`, while `realpath "$(command -v codegraph)"` is `/home/coder/.codegraph/versions/v1.6.2/bin/codegraph`; both are version 1.6.2, and the MCP server runs the `/opt` binary (standing rule 8: primitives call bare `codegraph`) |
| G2 | `claude mcp list \| rg -n '^codegraph:'` | PASS: `codegraph: /opt/codegraph/v1.6.2/bin/codegraph serve --mcp - ✔ Connected` |
| G3 | `jq -e --arg t "$MT" '.mcpServers.codegraph.env.CODEGRAPH_MCP_TOOLS == $t' ~/.claude.json` | PASS (exit 0, `true`); `MT` = `node,search,callers,callees,impact,files,status`: **seven-tool branch** |
| G4 | MCP `codegraph_status` with `projectPath` = `/home/coder/workspaces/IronClaude/.dev/worktrees/codegraph-adoption` | PASS: 971 files, 8824 nodes, 19695 edges, "Changes since index: 0 added, 0 modified, 0 removed" (no init running: `pgrep -f 'codegraph\.js (init\|index)'` printed nothing) |
| G5 | this session's tool list | PASS: lists `mcp__codegraph__codegraph_{callers,callees,files,impact,node,search,status}`; no `mcp__codegraph__codegraph_explore` |
| G6 | `rg -n 'mcp__serena__' src/superclaude plugins/superclaude commands agents`; `test -s .dev/codegraph-migration/handoffs/phase3-codegraph-slots.md` | PASS: `rg` printed nothing (exit 1); slots ledger exists and is non-empty |
| Reference inputs | `test -s` on the six inputs of the plan Constraints | PASS: all present (committed on `master`) |
| Baseline (a) | `grep -rIn 'src/superclaude' src/superclaude/{commands,skills,agents,core,hooks} \| wc -l` | **157** |
| Baseline (b) | `$TESTSET` through the Constraints pipeline into `.dev/codegraph-migration/experiments/P3-baseline-failures.txt` | **1897 passed, 0 failed** (1874 passed + 87 skipped + 1 xpassed in group 1; 23 passed in group 2); failure file empty and sorted. Logs: package `artifacts/t1-baseline-pytest-a.log`, `artifacts/t1-baseline-pytest-b.log` |

Environment note: the worktree had no virtual environment after the workspace restart; `uv sync --all-extras` created the gitignored `.venv` so `uv run --no-sync python -c 'from superclaude.cli.install_codegraph import …'` works. No installer, MCP registration or `~/.claude` file was touched. Claude Code version: 2.1.316.

## Decisions

| Date | Task | Decision | Options considered | Method | Rationale | Files touched |
|---|---|---|---|---|---|---|
| 2026-10-31 | T1 | Run `$TESTSET` as two pytest invocations (group 1: every path except `tests/roadmap/test_threshold_registry.py`; group 2: that file) and union their failing ids into the one baseline file | one invocation (fails at collection); two invocations | self | One invocation cannot collect: `tests/roadmap/conftest.py:25` runs `from conftest import AuditTrailHelper`, which resolves to `tests/sc-roadmap/conftest.py` once that directory is collected first (`ImportError`, log `artifacts/t1-baseline-pytest.log`). This is an existing test-isolation defect, out of scope; two invocations run the same path set, and every later `$TESTSET` run (Task 13 check 8) uses the same split | `.dev/codegraph-migration/experiments/P3-baseline-failures.txt` |
| 2026-10-31 | T1 | Tool-list branch is seven-tool | seven-tool; status-only | self (read from `install_codegraph.MCP_TOOLS`, G3) | Phase 2's constant and the registered value both equal `node,search,callers,callees,impact,files,status` | this log |
