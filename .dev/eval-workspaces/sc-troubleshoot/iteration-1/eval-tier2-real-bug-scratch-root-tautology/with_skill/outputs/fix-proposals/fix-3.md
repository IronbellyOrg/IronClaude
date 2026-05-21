# Fix-3 — Fix-1 PLUS CLI-boundary regression test for the OPS-002 policy at `eval_run`

**Author**: quality-engineer
**Surface area**: 1 call site + 1 test file

## Problem statement

Same as Fix-1. Additional concern: the existing test suite pins the policy text, the helper, and the doctor — but does **not** pin the `eval_run` CLI boundary. That coverage gap is what allowed the tautology to ship. Without a regression test at the eval_run boundary, the next refactor can re-introduce the same bug.

## Proposed change

1. Same call-site change as Fix-1.
2. Add `tests/cli/eval/test_eval_run_scratch_root.py` with at minimum:
   - `test_eval_run_rejects_forbidden_scratch_root`: `CliRunner().invoke(eval_group, ["run", "--suite", "smoke", "--output-dir", "/etc/foo"])` → `result.exit_code == SCRATCH_ROOT_VIOLATION_EXIT_CODE` (2), `"AC12"` in `result.stderr`, `"OPS-002"` in `result.stderr`.
   - `test_eval_run_accepts_default_output_dir`: no `--output-dir` → succeeds, uses `.dev/eval-runs/<run-id>/`.
   - `test_eval_run_accepts_tmp_eval_runs_root`: explicit `--output-dir /tmp/eval-runs/<unique>/` → succeeds.
3. Optional (not blocking, follow-up task): a generic test that iterates every `@click.option("--output-dir", ...)` in `commands.py` and verifies the command rejects `/etc/foo`. This is the wider drift-prevention gate.

## Evidence

- Snapshot `scratch-roots.md:108-110` — confirms tests pin policy text + helper, not the eval_run CLI boundary.
- Snapshot `commands.py:815-823` — doctor's gate is tested; eval_run's was not.
- Snapshot `commands.py:1473-1477` — the tautology.

## Risks

- The generic option-walker test (#3, optional) could flake on future `--output-dir` flags that are intentionally unrestricted. Mitigate with an explicit exemption list in the test.
- Otherwise: none — pure test addition, no production code surface change beyond Fix-1.

## Test plan

- Self-validating: the new tests are the test plan.
- Existing `test_scratch_root_policy.py` continues to pass.

## Rollback

Revert the test file. The call-site fix from Fix-1 still stands.
