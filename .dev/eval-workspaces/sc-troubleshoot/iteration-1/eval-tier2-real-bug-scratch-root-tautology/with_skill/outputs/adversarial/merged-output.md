# Merged Fix Proposal

## Diagnosis

`superclaude eval run --output-dir /etc/foo` silently succeeds because the first-gate call to `resolve_scratch_root` at snapshot `commands.py:1473-1477` extends the AC12 allowlist with the same path it is checking. The OPS-002 gate becomes a tautology. `doctor` correctly rejects `/etc/foo` because its gate at snapshot `commands.py:817` does **not** pass the `output_dir=` kwarg, so its allowlist stays at the canonical pair.

## Chosen fix (merged)

**Two-part, minimum surface**:

1. **Production change** — `src/superclaude/cli/eval/commands.py`, `eval_run`: drop the `output_dir=output_dir` keyword argument from the first-gate `resolve_scratch_root` call. Add an inline anti-tautology comment so the next reader does not re-add it.
2. **Test change** — add `tests/cli/eval/test_eval_run_scratch_root.py` with at minimum `test_eval_run_rejects_forbidden_scratch_root` (CliRunner against `eval_group` with `--output-dir /etc/foo`), `test_eval_run_accepts_default_output_dir`, and `test_eval_run_accepts_tmp_eval_runs_root`.

## Follow-up tasks (deferred from this PR)

- **T-OPS002-helper-guard**: defensive anti-tautology guard inside `resolve_scratch_root` itself (Fix-2 mechanism). Debate on its own merits.
- **T-OPS002-generic-option-walker**: generic test that walks every `@click.option('--output-dir', ...)` and verifies rejection of `/etc/foo`.

## Risk + rollback

- Risk: zero meaningful — call-site change is one-line; test additions are pure additions.
- Rollback: `git revert` the single commit.

## Verification

- `uv run pytest tests/cli/eval/ -v`
- Manual: `superclaude eval run --output-dir /etc/foo --suite smoke` returns exit code 2 with the OPS-002 policy text on stderr, matching the doctor's behaviour.
