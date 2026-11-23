# Tier 1 callers
index_state: fresh
checked_at: 2026-11-23T17:03:50Z
projectPath: /home/coder/workspaces/worktrees/IronClaude/bug-swarm-refactor-find-recommends-unavailable-s

## Caller rows
Graph returned 48 rows including tests and import edges. Bounded table below shows the three production call sites, confirmed by source Read; remaining graph rows are not cited as verified calls.

| caller | call site | resolution | relevance |
|---|---|---|---|
| swarm run_cmd | src/superclaude/cli/swarm/commands.py:2145 | call-site-verified | Supplies live lens template and compare_files with literal existing-review prefix. |
| swarm _run_resume_branch | src/superclaude/cli/swarm/commands.py:2578 | call-site-verified | Supplies no next-command template, separate pre-existing resume behavior; not changed in this diagnosis. |
| reflect run_tier2_ensemble | src/superclaude/cli/reflect/ensemble.py:404 | call-site-verified | Supplies its own adversarial template and substitutions; must not be changed by refactor-find fix. |

Registry attachment: lenses/__init__.py:60 imports refactor_find.LENS and :110 installs it under refactor-find. Preflight.py:540-543 copies the default template only if caller omitted it. Tests/swarm/test_reduce.py:305-314 verifies interpolation using fictional /sc:foo, not shipped-command availability.
