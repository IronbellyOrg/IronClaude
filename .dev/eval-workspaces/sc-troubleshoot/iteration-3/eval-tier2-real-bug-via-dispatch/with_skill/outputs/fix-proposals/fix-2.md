# FIX-B — Remove the `output_dir` kwarg from `resolve_scratch_root` entirely

## Problem
Same root cause as FIX-A. Additionally: the `output_dir` kwarg's existence on `resolve_scratch_root` invites exactly this class of misuse. The legitimate use case (extend allowlist for sub-path checks) is already covered by constructing a `runtime_config` with the extended allowlist tuple (`commands.py:1490-1499` shows the pattern).

## Proposed change
Three-part change:
1. Remove the `output_dir` kwarg from `resolve_scratch_root` signature in `config.py:167-172`.
2. Remove the corresponding `if output_dir is not None: allowed.append(...)` block at `config.py:219-220`.
3. Update all callers (currently `eval_run` and possibly tests) to either (a) call with positional candidate only — same as doctor — or (b) construct a `runtime_config` with the extended allowlist before calling.

## Evidence
- Same bug site as FIX-A.
- `commands.py:1490-1499` proves the runtime_config pattern works as the documented "extend the allowlist for sub-paths" idiom — no kwarg needed.
- API hygiene argument: kwarg name + docstring are not loud enough about "do NOT pass the candidate you are validating".

## Risks
- Larger surface area. Touches the public `resolve_scratch_root` signature; any external programmatic caller (per `scratch-roots.md:91-97`, "Callers inside `src/superclaude/cli/eval/` invoke `resolve_scratch_root(path, config=config, output_dir=output_dir)` directly") breaks.
- The scratch-roots.md doc and `tests/cli/eval/test_scratch_root_allowlist.py::test_output_dir_is_call_scoped_not_persistent` explicitly cover the call-scoped extension behavior — removing the kwarg invalidates that test and that documented contract.
- Higher blast radius for a security bug that has a one-line fix available.

## Test plan
- Update or remove `test_output_dir_is_call_scoped_not_persistent`.
- All FIX-A tests.
- Audit all in-tree calls to `resolve_scratch_root` for `output_dir=` usage and rewrite each to use a `runtime_config`-style allowlist extension.
