# FIX-A — Remove the `output_dir=output_dir` self-reference

## Problem
`commands.py:1476` passes the operator-supplied `--output-dir` as both the candidate AND as the allowlist-extension kwarg, tautologically passing OPS-002 enforcement.

## Proposed change
In `eval_run`, change the call site from:
```python
resolved_output = resolve_scratch_root(
    requested_output,
    config=base_config,
    output_dir=output_dir,     # remove this line
)
```
to:
```python
resolved_output = resolve_scratch_root(
    requested_output,
    config=base_config,
)
```

## Evidence
- `commands.py:1472-1477` — bug site
- `commands.py:815-823` — doctor's correct call shape (positional-only)
- `config.py:225-229` — the trivial-match path the bug exploits
- `commands.py:1490-1499` — legitimate downstream extension is untouched

## Risks
- Operators relying on `eval run --output-dir <non-allowlisted>` will see exit 2. Same UX as doctor today. Communicate in release notes.
- Per-eval HOMEs under `resolved_output` (commands.py:1483-1484) still resolve because `runtime_allowed` (line 1490) extends the allowlist with the validated `resolved_output` + `home_root`.

## Test plan
1. Regression: `superclaude eval run --output-dir /etc/foo` exits 2, stderr contains `OPS-002` + `SCRATCH_ROOT_POLICY` body.
2. Positive: `superclaude eval run --output-dir /tmp/eval-runs/test` exits 0.
3. Add cross-module parity test (quality-engineer's suggestion).
