---
status: success
tier_reached: 1
confidence: 0.95
escalation_reason: none
type: bug
fix_authorized: true
---

# Troubleshoot Report — `PROMPT_MAX_BYTES` import-time hard-fail

**Target:** PR #156 review comment [`r3385368388`](https://github.com/IronbellyOrg/IronClaude/pull/156#discussion_r3385368388) (augmentcode bot, severity medium)
**Scope:** `src/superclaude/cli/pipeline/process.py:24-26` (branch `fix/pipeline-stdin-large-prompts`)
**Tier reached:** 1 (single-domain, reviewer-confirmed root cause) · **Confidence:** 0.95

## Summary

`PROMPT_MAX_BYTES` is computed at **module import time** by a bare `int(os.environ.get("SUPERCLAUDE_PROMPT_MAX_BYTES", 16*1024*1024))`. If an operator sets `SUPERCLAUDE_PROMPT_MAX_BYTES` to anything `int()` can't parse (`"16MB"`, `"16_000_000 "` with stray chars, `""`, `"0x10"`), `int()` raises `ValueError` **during import** of `superclaude.cli.pipeline.process`. Because the failure is at top-level, the exception propagates out of the import and **every module that imports this one fails to load** — the CLI won't start. A configuration typo becomes a total import outage.

## Diagnosis

```python
# src/superclaude/cli/pipeline/process.py
PROMPT_MAX_BYTES: int = int(
    os.environ.get("SUPERCLAUDE_PROMPT_MAX_BYTES", 16 * 1024 * 1024)
)
```

- `os.environ.get(...)` returns the env value as a **`str`** when set (the `16*1024*1024` int default is only used when the var is **absent**).
- `int("not-a-number")` → `ValueError: invalid literal for int() with base 10`.
- Raised at module scope → uncaught import-time crash → cascading `ImportError` for all dependents.
- Secondary gap: a **non-positive** value (`"0"`, `"-1"`) parses fine but would make *every* prompt exceed the cap (or, at `0`, fail the guard for any non-empty prompt) — a silent foot-gun even when parsing succeeds.

This matches the documented intent (the comment calls it a "sanity guard … env-overridable for operators") — the contract is "operators may override," so a bad override must degrade gracefully, not brick the module. `consistency_with_docs: aligned` (the fix honors the stated intent).

## Evidence

- `src/superclaude/cli/pipeline/process.py:24-26` — the bare `int(os.environ.get(...))` at module top-level (read on `fix/pipeline-stdin-large-prompts`).
- `src/superclaude/cli/pipeline/process.py:21` — `_log = logging.getLogger("superclaude.pipeline.process")` is already defined above the constant, so a warning-on-fallback path is available without new imports.
- `tests/pipeline/test_process_stdin.py:126-175` — `TestPromptMaxBytesGuard` patches the **constant** (`monkeypatch.setattr(...PROMPT_MAX_BYTES, 1024)`), so it never exercised env-var parsing — the invalid-env path is currently untested.

## Proposed Fix

Extract a defensive parser; invalid or non-positive values fall back to the default with a logged warning (never raise at import). `Optional` and `_log` are already in scope.

```python
def _parse_prompt_max_bytes(
    raw: Optional[str], default: int = 16 * 1024 * 1024
) -> int:
    """Parse SUPERCLAUDE_PROMPT_MAX_BYTES defensively.

    A misconfigured env var must never hard-fail module import. Invalid or
    non-positive values fall back to the default with a logged warning.
    """
    if raw is None:
        return default
    try:
        value = int(raw)
    except (TypeError, ValueError):
        _log.warning(
            "Invalid SUPERCLAUDE_PROMPT_MAX_BYTES=%r (not an integer); "
            "falling back to default %d bytes.",
            raw,
            default,
        )
        return default
    if value <= 0:
        _log.warning(
            "SUPERCLAUDE_PROMPT_MAX_BYTES=%d is non-positive; "
            "falling back to default %d bytes.",
            value,
            default,
        )
        return default
    return value


PROMPT_MAX_BYTES: int = _parse_prompt_max_bytes(
    os.environ.get("SUPERCLAUDE_PROMPT_MAX_BYTES")
)
```

Plus a test covering: non-integer → default+warning, non-positive → default+warning, valid → parsed, absent → default.

## Risk + Rollback

- **Risk:** negligible. Behavior is unchanged for the absent-var and valid-int cases; only the previously-crashing path changes (now warns + defaults). No call-site changes; `PROMPT_MAX_BYTES` stays an `int`.
- **Rollback:** revert the single commit on `fix/pipeline-stdin-large-prompts`.

## Next Steps

`--fix` is set. Recommended remediation: apply the parser + test directly to `fix/pipeline-stdin-large-prompts`, run the pipeline suite, push (updates PR #156 and resolves the review thread). Alternative: full MDTM task via `task-builder`.
