# Fix-1 — Drop the `output_dir=` kwarg at the `eval_run` first gate

**Author**: security-engineer
**Surface area**: 1 file, 1 line

## Problem statement

`superclaude eval run --output-dir /etc/foo --target ...` silently succeeds because the first-gate call to `resolve_scratch_root` at snapshot `commands.py:1473-1477` extends the AC12 allowlist with the same path it is supposed to be checking. The OPS-002 gate becomes a tautology. `superclaude doctor --output-dir /etc/foo` correctly rejects the path because its gate call at snapshot `commands.py:817` does **not** pass the `output_dir=` kwarg, so its allowlist stays at the canonical pair.

## Proposed change

`src/superclaude/cli/eval/commands.py`, in `eval_run`, replace:

```python
resolved_output = resolve_scratch_root(
    requested_output,
    config=base_config,
    output_dir=output_dir,
)
```

with:

```python
resolved_output = resolve_scratch_root(
    requested_output,
    config=base_config,
)
```

Add an inline comment explaining that the `output_dir=` kwarg is reserved for layered re-checks (`containment_guard`) where the path has *already* been gate-validated, never for the first gate.

## Evidence

- Snapshot `commands.py:815-823` — doctor's correct first-gate call (no kwarg).
- Snapshot `commands.py:1473-1477` — eval_run's tautological first-gate call.
- Snapshot `config.py:217-238` — the helper that performs the extension + match loop.
- Snapshot `scratch-roots.md:62-76` — the operator-facing policy that `/etc/foo` must be rejected.

## Risks

- None at this call site.
- Future drift: another command could repeat the pattern. Mitigated indirectly by Fix-3's CLI-boundary test.

## Test plan

- Unit: existing `test_scratch_root_policy.py` continues to pass.
- Integration: extend `tests/cli/eval/test_scratch_root_allowlist.py` with `test_eval_run_rejects_forbidden_scratch_root` (CliRunner against `eval_group`).

## Rollback

`git revert` of the single-line change.
