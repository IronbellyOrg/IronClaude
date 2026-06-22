# ruff format --check (Step 3.8) — the SEPARATE CI format gate

**Date:** 2026-06-22

## What happened

A repo-wide `uv run ruff format --check src/ tests/` reported 103 files "would be reformatted" with EXIT 1. **This is the known worktree ruff-version-mismatch footgun** (the worktree `.venv` ruff diverges from CI ruff and mass-reformats ~100 unrelated files). Per project memory `reference_ruff_version_mismatch_worktree.md`, the broad command must NOT be applied — it would corrupt ~100 unrelated files' diffs. The format check is therefore SCOPED to this task's changed files only.

## Scoped result on the 3 modified files

Initial scoped check flagged exactly ONE genuine issue in `ensemble.py`:

```
@@ -68,6 +68,7 @@
 MZERO_CONTRACT_MISSING_SLUG = "contract-missing"

+
 @dataclasses.dataclass
```

A real PEP8/black fix to NEW code — a top-level class needs 2 blank lines before its decorator; my insert had 1. Applied via `uv run ruff format src/superclaude/cli/reflect/ensemble.py` (scoped to ONLY this file).

## Final verdict: PASS (scoped)

```bash
uv run ruff format --check \
  src/superclaude/cli/reflect/ensemble.py \
  tests/cli/reflect/test_ensemble_stub_integration.py \
  tests/cli/reflect/test_ensemble_unit.py
# -> 3 files already formatted   (EXIT 0)
```

All three modified files are correctly formatted. The 103-file repo-wide noise is a pre-existing version-mismatch condition unrelated to R6 and was deliberately NOT touched (only `ensemble.py`, my own file, was formatted).
