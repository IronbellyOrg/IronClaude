# Troubleshoot Report — Imaginary module

**Type**: bug | **Tier reached**: 1 | **Status**: success (draft)

## Summary

NameError in an imaginary module.

## Diagnosis

Missing import in a module that does not exist.

## Evidence

1. `/config/workspace/IronClaude/src/superclaude/cli/imaginary_module.py:42` — `result = Path(scratch_root)` (the unimported Path reference)
2. `/config/workspace/IronClaude/.dev/eval-workspaces/sc-troubleshoot/evals/fixtures/real-bug-scratch-root/commands.py:1406` — `def eval_run(` (this one is real, for control)

## Proposed Fix

Add `from pathlib import Path` to the imaginary module.
