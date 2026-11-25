start=1e33f422dadf9034876adec8c03894ab6ccfca76

## Family detached-child-output-propagation

Defect form: the child request must carry an output argument before it can enter the durable completion continuation; the unchanged launcher supplies only the snapshot.
Command: git grep -n -E -e 'child_argv|str\(snapshot_path\)|if output_dir is not None' -- src/superclaude/cli/swarm/commands.py src/superclaude/cli/swarm/preflight.py tests/swarm/test_tmux_detached.py
Before-output:
- commands.py:1297 child_argv list; :1303 snapshot argument; :1309 launch_detached call.
- commands.py:1716,1739,3704 output-option guards.
- preflight.py:1872 manifest persistence guarded by output_dir is not None.
Coupled sites: launcher child argv at commands.py:1297-1304; preflight persistence at preflight.py:1871-1873; new captured-child marker assertion at test_tmux_detached.py:315-317; live-child marker assertion at :375. The two permitted completion continuations cannot publish a real contract when the child never materializes an output root.
Fix-pass outcome: No scope-conforming source repair is available. Changing child argv or preflight violates the plan's production-edit boundary and may overlap another session's issue. No source/test expectations were changed, no conditional skip was added, and no missing marker was fabricated. The one Q5 fix attempt therefore preserves the failing artifacts and requests independent re-review of the unchanged scoped outcome, rather than disguising it as repaired.
After-output: unchanged; the same validated literal git-grep command was rerun before re-review.
after: On 2026-11-23 the user explicitly authorized including the launcher change and finishing the fix. The validated literal search was rerun before the operator review: commands.py:1297 child_argv, :1311 launch_detached, :1718/:1741/:3706 output-option guards; preflight.py:1872 manifest guard remains unchanged. Child argv now carries --output and both output/snapshot paths are absolute; the new positive CLI capture is in detached-cli/verified/ and appended to detached-check.txt. No preflight behavior, helper API, kill path or policy persistence changed.
