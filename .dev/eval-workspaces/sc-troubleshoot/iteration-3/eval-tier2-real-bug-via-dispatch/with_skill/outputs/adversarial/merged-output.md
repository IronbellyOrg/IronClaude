# Merged Fix Output (chosen)

## Change
File: `src/superclaude/cli/eval/commands.py`, `eval_run` function, around line 1473.

```diff
     try:
         resolved_output = resolve_scratch_root(
             requested_output,
             config=base_config,
-            output_dir=output_dir,
         )
     except ScratchRootViolation as exc:
         click.echo(format_scratch_root_violation(exc), err=True)
         sys.exit(SCRATCH_ROOT_VIOLATION_EXIT_CODE)
```

## Docstring hardening (additive, in `config.py`)
Add to the `output_dir` kwarg docstring in `resolve_scratch_root`:

> WARNING: do NOT pass the candidate path being validated as `output_dir`. The kwarg extends the allowlist for **sub-path** checks under an already-validated root; passing the candidate creates a tautology that bypasses enforcement. CLI surfaces validating an operator-supplied `--output-dir` should call this helper positionally with the candidate only (see `eval_doctor`).

## Tests
1. Regression test: `eval run --output-dir /etc/foo` exits 2 + emits SCRATCH_ROOT_POLICY.
2. Positive test: `eval run --output-dir /tmp/eval-runs/test` exits 0.
3. Parity test: parameterized over `[/etc/foo, /var/lib/test, /, ~/]` — both `eval doctor` and `eval run` reject identically.

## Follow-up (separate task, not part of this fix)
- FIX-B refactor: remove the `output_dir` kwarg from `resolve_scratch_root` with a deprecation cycle. Update all callers to use `runtime_config`-style allowlist extension instead.
- Audit all `resolve_scratch_root` call sites in `src/superclaude/cli/eval/` for similar misuse patterns.
