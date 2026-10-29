Task W4: codegraph research and hands-on validation in an isolated sandbox.

First read /home/coder/workspaces/worktrees/IronClaude/feat-codememory-codegraph-init/.dev/codegraph-migration/orchestration/README.md (shared rules; binding).

Target: https://github.com/colbymchenry/codegraph (and its fork sunerpy/codegraph-rust only if the main project is unsuitable). Read the repo README, releases, package manifest, install docs, MCP server docs and source as needed (gh api / WebFetch / Context7).

Change: write `.dev/codegraph-migration/research/codegraph-evaluation.md` with:
1. Facts with sources: implementation language and distribution (npm? cargo? release binaries? which platforms incl. linux amd64/arm64), latest release and version-pinning options, checksums/signatures, license, maintenance activity.
2. Install mechanics: exact install commands, what it writes (binary path, config, per-project index location such as `.codegraph/`, global state), whether it has its own installer that edits Claude config, hooks, CLAUDE.md or skills.
3. MCP integration: how it registers with Claude Code (`claude mcp add ...` exact argv, stdio/HTTP, scope), the exact MCP tool names and parameters it exposes, CLI subcommands (init, index, sync, status, query...).
4. Indexing lifecycle: how a project gets indexed, incremental sync, file watching, git hooks, behaviour with git worktrees (shared vs per-worktree index), what must happen on clone/new worktree, cost/time.
5. HANDS-ON validation in an isolated sandbox: `SANDBOX=$(mktemp -d /tmp/codegraph-eval.XXXX)`; set `HOME=$SANDBOX/home` and any npm/cargo prefix inside the sandbox for every command; copy (do not link) a small subset of this repo (e.g. `src/superclaude/cli/` plus `tests/cli/`) into `$SANDBOX/project` and `git init` it. Install codegraph there, index the project, exercise its CLI and, if possible, its MCP server over stdio (e.g. send an `initialize` + `tools/list` JSON-RPC request) and two real queries (find the definition of `install_codebase_memory_mcp`; find its callers). Record exact commands, outputs (trimmed), timings, index size, memory if measurable. Never touch the real HOME, ~/.claude.json or the real worktree's files. Record the sandbox path; leave it in place.
6. Gaps versus codebase-memory-mcp and Serena: map each codebase-memory tool (search_graph, trace_path, get_code_snippet, query_graph, get_architecture, detect_changes, search_code, index_status...) and each Serena capability (find_symbol, find_referencing_symbols, get_symbols_overview, symbol edits, memories) to a codegraph equivalent or "no equivalent".
7. Recommended install strategy for IronClaude (`superclaude install` + `./update.sh`) and for the Coder image (bake versus install-on-update), including pinning and verification. If two or more strategies are viable with real trade-offs, run `/sc:adversarial --depth quick` (positive return here) and adopt its recommendation.
8. `## Decisions` section.

Constraints: no changes outside `$SANDBOX` and your output file. If installation is impossible in the sandbox, say exactly why with the error and continue with documentation-based facts marked UNVERIFIED-HANDS-ON.

Ownership: write only `.dev/codegraph-migration/research/codegraph-evaluation.md` and files inside your sandbox.

Observable acceptance: file exists; hands-on section shows real command output for install, index, and at least one query (or the exact blocking error); tool-name list is quoted from source or live `tools/list` output.
