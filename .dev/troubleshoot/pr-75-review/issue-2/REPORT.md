# Troubleshoot Report — PR #75 Issue 2: artifact_layout FR-SCH2 label drift

**Target**: auggie review #3290878762 on PR #75
**Tier reached**: 1
**Confidence**: 0.97
**Status**: success
**Severity**: LOW

## Root Cause

The rename "FR-SCH2 → `_EVAL_ID_PATH_SAFETY_PATTERN`" was partial: the module-level constant + leading comment got updated, but the docstring + ValueError message inside `compose_per_eval_dir` were missed.

Verified design intent from file (lines 96-108):
- Line 96-105: `_EVAL_ID_PATH_SAFETY_PATTERN` is explicitly the **path-safety** regex, deliberately separate from FR-SCH2
- Line 97 comment: "**NOT** the FR-SCH2 schema contract"
- Lines 102-105 docstring: "**NOT** the FR-SCH2 schema... two patterns are deliberately separate defense-in-depth layers"
- Line 108: `EVAL_ID_PATTERN` (no underscore prefix) is the actual FR-SCH2 schema regex

Inconsistencies at lines 220-227 (inside `compose_per_eval_dir`):
1. Docstring says "Validates `eval_id` against the FR-SCH2 character set" — **wrong**. The pattern at line 237 is `_EVAL_ID_PATH_SAFETY_PATTERN`, the path-safety regex.
2. ValueError says "fails the FR-SCH2 [A-Za-z0-9_.-]{1,64} guard" — **wrong**. The `[A-Za-z0-9_.-]{1,64}` literal is the path-safety pattern; FR-SCH2 is `^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$`. Calling it "FR-SCH2" actively contradicts lines 96-105.

## Proposed Fix

**Edit 1 — `src/superclaude/cli/eval/artifact_layout.py`** (around line 219-227, the `compose_per_eval_dir` docstring + ValueError):

`old_string`:
```python
def compose_per_eval_dir(run_dir: Path | str, eval_id: str) -> Path:
    """Return ``<run_dir>/per-eval/<eval_id>/``.

    Validates ``eval_id`` against the FR-SCH2 character set so a
    crafted id cannot escape the per-eval subtree via path-traversal
    components.
    """

    if not isinstance(eval_id, str) or not _EVAL_ID_PATH_SAFETY_PATTERN.match(eval_id):
        raise ValueError(
            f"eval_id {eval_id!r} fails the FR-SCH2 [A-Za-z0-9_.-]{{1,64}} guard"
        )
```

`new_string`:
```python
def compose_per_eval_dir(run_dir: Path | str, eval_id: str) -> Path:
    """Return ``<run_dir>/per-eval/<eval_id>/``.

    Validates ``eval_id`` against the path-safety character set
    (``_EVAL_ID_PATH_SAFETY_PATTERN``) so a crafted id cannot escape
    the per-eval subtree via path-traversal components. This is the
    path-safety defense-in-depth layer, NOT the FR-SCH2 schema contract
    (which is enforced earlier via ``EVAL_ID_PATTERN`` — see the
    docstring on ``_EVAL_ID_PATH_SAFETY_PATTERN`` for the split).
    """

    if not isinstance(eval_id, str) or not _EVAL_ID_PATH_SAFETY_PATTERN.match(eval_id):
        raise ValueError(
            f"eval_id {eval_id!r} fails the path-safety [A-Za-z0-9_.-]{{1,64}} guard"
        )
```

## Risk + Rollback

Very low. Docstring + error-message text changes only. No test asserts on the exact "FR-SCH2" string (verified). Behavior unchanged.

## Files that MUST NOT change

- `_EVAL_ID_PATH_SAFETY_PATTERN` constant definition (lines 96-108) — already correctly labeled
- `EVAL_ID_PATTERN` (the actual FR-SCH2 schema regex)
- Any other ValueError raises in the same file
