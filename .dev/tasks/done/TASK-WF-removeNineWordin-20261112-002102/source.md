Remove nine wording ambiguities found by a smoke test in the codegraph instructions of /sc:analyze and /sc:design (report: /tmp/smoke-504/result.md, section 'Ambiguous, contradictory or hard-to-follow instructions', items 1-9; re-verify each quote against the worktree before editing). Keep every fix small (a clause or one sentence); do not change behaviour, flags, the one-check-per-run rule, the fresh-and-access:mcp rule, the Grep/Read floor, or the never-halt rule. File ownership: src/superclaude/commands/analyze.md, src/superclaude/commands/design.md, src/superclaude/core/CODEGRAPH.md (shared by every primitive: additive clarifications only; grep src/superclaude for each phrase changed), their plugins/superclaude/ twins only if a test pins them byte-identical, and the tests pinning those files (tests/skills/test_codegraph_adoption.py, tests/core/test_codegraph_guide.py, scripts/eval_workflow_vs_task_builder.py pin).

Tasks:
(1) CODEGRAPH.md section 2 + one clause in commands: before the single codegraph_status call on the MCP path, if pgrep -f 'codegraph\.js (init|index)' prints a line, poll up to 60 s for it to end then make the one check; still running after 60 s => record graph:stale; still exactly one status call.
(2) codegraph_files grouped maxDepth:2 in analyze Discover, design Analyze row and CODEGRAPH.md: allow and recommend `path` set to the target directory when narrower than the repo.
(3) analyze Discover/Scan: directory/package target => codegraph_files with path + codegraph_node symbolsOnly on main files; codegraph_search only when target names a symbol; symbol bodies only for symbols Discover found.
(4) checked_at source: one `date -u +%Y-%m-%dT%H:%M:%SZ` Bash call immediately after the status call, in analyze, design and CODEGRAPH.md step 7.
(5) analyze quick depth: a Grep-found line need not be re-Read; a graph row cited as a finding still must be confirmed by Grep or Read; one sentence.
(6) design Validate row: run codegraph_impact at Validate only if not already run for the same symbol in Plan/Design.
(7) analyze and design: on a single lookup failure/empty, record a lookup-level token from the closed list in CODEGRAPH.md section 3 (add graph:empty/graph:truncated only if section 3 defines them).
(8) json output: put the Codegraph line in a top-level "codegraph" string field; code/diagram output: first comment line or caption line.
(9) analyze and design: reword 'read it when you use codegraph' to 'read it before the first codegraph call'.

Tests: extend tests/skills/test_codegraph_adoption.py with checks that fail if the pgrep/wait clause, the path argument, the date -u source, the quick-depth sentence or the json field rule returns to the old wording; show one mutant failing.

Flags: --depth quick --handoff none
