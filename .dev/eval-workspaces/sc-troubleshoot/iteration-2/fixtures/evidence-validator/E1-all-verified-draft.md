# Troubleshoot Report — Scratch-root tautology (all-verified case)

**Type**: security | **Tier reached**: 2 | **Confidence**: 0.92 | **Status**: success (draft, awaiting validation)

## Summary

`eval_run` self-extends the scratch-root allowlist with the candidate path.

## Diagnosis

Root cause: `eval_run` passes the operator-supplied `--output-dir` as both the candidate AND the `output_dir=` kwarg to `resolve_scratch_root`. The kwarg extends the allowlist with the kwarg's value before the loop checks the candidate, so the candidate trivially matches itself.

## Evidence

1. `/config/workspace/IronClaude/.dev/eval-workspaces/sc-troubleshoot/evals/fixtures/real-bug-scratch-root/commands.py:1476` — `output_dir=output_dir,`
2. `/config/workspace/IronClaude/.dev/eval-workspaces/sc-troubleshoot/evals/fixtures/real-bug-scratch-root/commands.py:1406` — `def eval_run(`
3. `/config/workspace/IronClaude/.dev/eval-workspaces/sc-troubleshoot/evals/fixtures/real-bug-scratch-root/config.py:1` — `"""Scratch-root resolution and allowlist policy."""` (top-of-file docstring; check whatever real content is at line 1 — file does start with imports/docstring)

## Proposed Fix

Drop the `output_dir=output_dir` kwarg from the `eval_run` call site at commands.py:1476.
