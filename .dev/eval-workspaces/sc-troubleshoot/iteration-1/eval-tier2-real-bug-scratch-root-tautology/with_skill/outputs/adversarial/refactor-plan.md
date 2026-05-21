# Refactor Plan (merged fix)

## Step 1 — Production: drop the kwarg

`src/superclaude/cli/eval/commands.py`, in `eval_run`, change the first-gate call from:

```python
resolved_output = resolve_scratch_root(
    requested_output,
    config=base_config,
    output_dir=output_dir,
)
```

to:

```python
# OPS-002 / AC12: the operator-supplied --output-dir is itself the
# candidate being validated. Do NOT pass it back through the
# ``output_dir=`` kwarg — that kwarg exists for layered helpers
# (HomeIsolation.containment_guard, FR-ISO2) that re-check a path
# that has *already* been validated against the allowlist. Passing
# the operator input as both the candidate AND the extension makes
# the gate a tautology and lets a malicious / mistyped path (e.g.
# /etc/foo, /root/.claude) escape the OPS-002 allowlist.
resolved_output = resolve_scratch_root(
    requested_output,
    config=base_config,
)
```

## Step 2 — Tests: pin the eval_run CLI boundary

Add `tests/cli/eval/test_eval_run_scratch_root.py` (or extend an existing eval_run test module) with:

```python
def test_eval_run_rejects_forbidden_scratch_root(tmp_path):
    runner = CliRunner(mix_stderr=False)
    result = runner.invoke(
        eval_group,
        ["run", "--suite", "smoke", "--output-dir", "/etc/foo"],
    )
    assert result.exit_code == SCRATCH_ROOT_VIOLATION_EXIT_CODE  # 2
    assert "AC12" in result.stderr
    assert "OPS-002" in result.stderr

def test_eval_run_accepts_default_output_dir(tmp_path):
    ...

def test_eval_run_accepts_tmp_eval_runs_root(tmp_path):
    ...
```

## Step 3 — Follow-up task (split from this PR)

Open a separate task `T-OPS002-helper-guard` for the defensive `resolve_scratch_root` API guard from Fix-2. Debate independently.

## Step 4 — Verification

- `uv run pytest tests/cli/eval/test_eval_run_scratch_root.py -v`
- `uv run pytest tests/cli/eval/test_scratch_root_policy.py -v` (existing policy drift gate continues to pass)
- Manual: `superclaude eval run --output-dir /etc/foo --suite smoke` → exit code 2, stderr quotes the OPS-002 policy.
