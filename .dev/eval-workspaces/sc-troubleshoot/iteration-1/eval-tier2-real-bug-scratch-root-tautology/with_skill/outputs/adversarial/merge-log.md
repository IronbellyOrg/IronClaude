# Merge Log

| Element | Source | Action |
|---------|--------|--------|
| Drop `output_dir=` kwarg at `eval_run` first gate | Fix-1 | accepted into merged output |
| Anti-tautology inline comment | Fix-1 (+ live code's existing comment style) | accepted into merged output |
| CLI-boundary regression test suite | Fix-3 | accepted into merged output |
| Generic `@click.option('--output-dir', ...)` walker test | Fix-3 (optional step 3) | deferred — make follow-up task |
| Defensive `resolve_scratch_root` API guard | Fix-2 | deferred — make follow-up task T-OPS002-helper-guard |

## Self-review (Wave 4 step 4)

- **Tests?** Yes — Fix-3's regression test is the gate.
- **Edge cases?** `--output-dir` with a symlink that resolves to `/etc/foo` — covered because `resolve_scratch_root` uses `Path.resolve(strict=False)` before the allowlist check.
- **Requirements?** OPS-002 / AC12 policy doc is satisfied: doctor + eval_run now share the same gate semantics.
- **Follow-up?** Yes — T-OPS002-helper-guard tracked for Fix-2 mechanism.

No blockers found. Proceed to Wave 5.
