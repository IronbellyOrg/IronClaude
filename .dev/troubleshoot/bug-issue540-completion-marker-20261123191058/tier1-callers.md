# Tier 1 caller lookup

## Run state
index_state: fresh; checked_at: 2026-11-23T19:11:34Z; worktree_root/projectPath: current worktree. emit_done_sentinel caller rows shown/total: 15/15. reduce_wave3 rows shown/total: 48/48.

## Caller rows
| Symbol | Dependent | Resolution |
|---|---|---|
| emit_done_sentinel | src/superclaude/cli/reflect/ensemble.py:421 | call-site-verified |
| emit_done_sentinel | tests/swarm/test_done_sentinel.py:52 | call-site-verified (test only) |
| emit_done_sentinel | tests/swarm/test_three_layer_artifacts.py:124, test_normalize.py:1029 | def-line (not claimed as production paths) |
| reduce_wave3 | src/superclaude/cli/swarm/commands.py:2145 (run_cmd) | call-site-verified |
| reduce_wave3 | src/superclaude/cli/swarm/commands.py:2578 (_run_resume_branch) | call-site-verified |
| reduce_wave3 | src/superclaude/cli/reflect/ensemble.py:404 | def-line; writer call itself verified at :421 |

Remaining graph rows are helper tests/import rows, not additional asserted production call sites. Source-wide Grep for emit_done_sentinel calls under src found the definition and reflect caller only; absence conclusions do not rest on graph emptiness.
