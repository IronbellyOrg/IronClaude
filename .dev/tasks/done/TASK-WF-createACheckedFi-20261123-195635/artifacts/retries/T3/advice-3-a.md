model: claude-opus-5-5 family: claude rung: top
outcome: dispute

| AC | why earlier attempts missed it (path:line) | change |
|---|---|---|
| T3.AC1 | F3.1 (review-2.md:7) is supported by its own citations and is not fixable inside the plan's scope. The child argv carries only the snapshot path, with no --output (src/superclaude/cli/swarm/commands.py:1297-1304). The child's run_cmd passes its absent output_dir into preflight (commands.py:1739-1740, 1814-1817), and preflight writes the manifest only when output_dir is given (src/superclaude/cli/swarm/preflight.py:1871-1873). So state_output_dir stays None (commands.py:1843-1848), and reduction, the terminal state and the marker are all skipped (commands.py:2096, 2165, 2174-2178). The completion continuation is never reached with a contract, so no edit inside it can satisfy the AC1 clause the review anchors (review-2.md:7, plan:73). The fix sites are the launcher argv or the output resolution before preflight. The plan forbids both: "Production edits are limited to the two completion continuations" (plan:22), and "No ... adjacent behavior change is included" (plan:24). A test that adds --output itself would execute a repaired argv, not the actual child path (attempt-2.diff:67-68; plan:73 "exercises the child execution path"). | None possible in scope. Needs an operator ruling. |
| T3.AC2 | Same root cause. The live child left only .swarm-detached-spec.json (extras-2.log:17-23; review-2.md:4). The skip escape at plan:74 covers only missing or nested tmux. Tmux was available and not nested (review-2.md:4), so a skip is not an option. | Same ruling as T3.AC1. |
| T3.AC3 | Met. All eight modules ran and their results were recorded (review-2.md:5; extras-2.log:6-29). | None. Re-record after any authorized fix. |
| T3.AC4 | Met (review-2.md:6). The parent launches only (commands.py:1333-1336) and the killed marker path is untouched. | Keep. Any authorized argv change must not make the parent publish anything. |

differs-by: treat F3.1 as a conflict between the plan's scope limit and the AC, to be resolved by an operator ruling, not by a third implementation inside the two completion continuations (both earlier attempts stayed inside them: approach-2.md:4-6).

steps:
1. Halt with reason=dispute. Leave the A2 tree, which holds the failing tests (attempt-2.diff:29-145), in place for the operator.
2. Ask the operator for one ruling. Option (a): authorize a one-line change to the launcher's child argv at commands.py:1297-1304 that appends "--output" and the absolute output directory. The path must be absolute because the child runs with cwd=output_path (commands.py:1309). This keeps _launch_detached_run launch-only and leaves preflight and the foreground output resolution unchanged. Option (b): amend T3.AC1/T3.AC2 so detached completion is recorded as NOT PROVEN. Neither option is authorized by this advice.
3. Under (a): do not change preflight.py:1871-1873 or commands.py:1739-1740, because that would change every spec-only run. Rerun the existing tests unchanged; the two failures at extras-2.log:25-26 must pass. Then capture ./artifacts/detached-cli/ and ./artifacts/detached-check.txt and re-record ./artifacts/completion-compatibility.txt.
4. Under (b): the parent records the amended AC through the Ruling path. No source edit.
