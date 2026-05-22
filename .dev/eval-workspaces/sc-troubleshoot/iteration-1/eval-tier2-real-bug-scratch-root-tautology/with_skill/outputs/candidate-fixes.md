# Candidate Fixes — Wave 3 distillation

All three hypothesis agents converge on the root cause:
> `eval_run` (snapshot `commands.py:1473-1477`) passes the operator-supplied `--output-dir` value as both the candidate path AND as the `output_dir=` kwarg to `resolve_scratch_root`, which extends the allowlist with that same path, making the OPS-002 gate a tautology.

They differ on the **fix mechanism**, so Wave 4 (`sc:adversarial`) runs.

| Fix | Supporting agent(s) | Mechanism | Surface area | Verdict |
|----:|---------------------|-----------|--------------|---------|
| Fix-1 | security-engineer | Drop `output_dir=output_dir` from the `eval_run` first-gate call only. | 1 call site, 1 line | competing |
| Fix-2 | root-cause-analyst | Fix-1 PLUS make `resolve_scratch_root` raise when `output_dir=` resolves equal to candidate (defensive helper guard). | 1 call site + 1 helper + special-case for `containment_guard` | competing |
| Fix-3 | quality-engineer | Fix-1 PLUS new regression test(s) at the `eval_run` CLI boundary asserting `/etc/foo` is rejected with OPS-002 stderr. | 1 call site + 1 test file | competing |

Wave 4 will debate correctness, risk, and test-coverage tradeoffs and produce a merged fix.
