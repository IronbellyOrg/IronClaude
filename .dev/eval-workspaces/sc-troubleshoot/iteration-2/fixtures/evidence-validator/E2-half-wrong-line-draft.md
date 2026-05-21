# Troubleshoot Report — Scratch-root tautology

**Type**: security | **Tier reached**: 2 | **Confidence**: 0.88 | **Status**: success (draft, awaiting validation)

## Summary

`eval_run` self-extends the scratch-root allowlist with the candidate path.

## Diagnosis

Root cause: `eval_run` passes the operator-supplied `--output-dir` as both the candidate AND the `output_dir=` kwarg to `resolve_scratch_root`. The kwarg extends the allowlist with the kwarg's value before the loop checks the candidate, so the candidate trivially matches itself.

## Evidence

1. `/config/workspace/IronClaude/.dev/eval-workspaces/sc-troubleshoot/evals/fixtures/real-bug-scratch-root/commands.py:1476` — `output_dir=output_dir,` (the self-referential kwarg)
2. `/config/workspace/IronClaude/.dev/eval-workspaces/sc-troubleshoot/evals/fixtures/real-bug-scratch-root/commands.py:1406` — `def eval_run(` (function definition)
3. `/config/workspace/IronClaude/.dev/eval-workspaces/sc-troubleshoot/evals/fixtures/real-bug-scratch-root/commands.py:42` — `output_dir=output_dir,` (FAKE — line 42 does not contain this; the snippet exists at line 1476 only)
4. `/config/workspace/IronClaude/.dev/eval-workspaces/sc-troubleshoot/evals/fixtures/real-bug-scratch-root/config.py:999` — `def resolve_scratch_root(` (WRONG LINE — actual function definition is elsewhere; line 999 may not even exist in this 217-line file)

## Proposed Fix

Drop the `output_dir=output_dir` kwarg from the `eval_run` call site at commands.py:1476.
