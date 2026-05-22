# Troubleshoot Report — PR #75 Issue 3: executor_factory probe-and-discard leak risk

**Target**: auggie review #3290878763 on PR #75
**Tier reached**: 1
**Confidence**: 0.92
**Status**: success
**Severity**: medium

## Root Cause

The one-shot WARNING probe at `src/superclaude/cli/eval/commands.py` (~line 1873) classifies the factory by **instantiating-then-discarding**: `_executor_probe = executor_factory()` → `isinstance(...)` → `del _executor_probe`. Currently benign only because `_NullLifecycleExecutor.__init__` is the default object init (no allocations).

The docstring at lines 1394-1400 explicitly states M5/M6 will land `ClaudeProcessAdapter + PtyDriver`. Real PTY-backed executors will allocate file descriptors, scratch dirs, and helper threads in `__init__`. At that point:

1. The probe builds a real executor whose resources are never released — `del` drops the reference but does not invoke any `close()` semantics; finalization is GC-deferred.
2. The probe leak happens BEFORE `RunOrchestrator` starts, so the leaked executor is untracked.
3. If the real `__init__` raises (PTY allocation failure), the probe crashes a run that should have been recoverable via the per-spec `EXECUTOR_ERROR → ERRORED` outcome path.

The shape error: the probe asks a **classification** question via an **instantiation** mechanism. Correct fix is to introspect the factory itself.

## Proposed Fix (Option C — tag-and-introspect)

Two surgical edits to `src/superclaude/cli/eval/commands.py`.

**Edit 1** — tag the null factory in `_resolve_executor_factory`:

`old_string`:
```python
def _resolve_executor_factory() -> Callable[..., LifecycleExecutor]:
    """Return the factory that constructs a per-eval :class:`LifecycleExecutor`.

    Production wiring (``ClaudeProcessAdapter`` + ``PtyDriver``) lands
    with the vendored PTY harness (M5 / M6). Until then this factory
    returns the :class:`_NullLifecycleExecutor` documented above. Tests
    monkeypatch this function to inject canned executors.
    """

    def factory(**_kwargs: Any) -> LifecycleExecutor:
        return _NullLifecycleExecutor()  # type: ignore[return-value]

    return factory
```

`new_string`:
```python
def _resolve_executor_factory() -> Callable[..., LifecycleExecutor]:
    """Return the factory that constructs a per-eval :class:`LifecycleExecutor`.

    Production wiring (``ClaudeProcessAdapter`` + ``PtyDriver``) lands
    with the vendored PTY harness (M5 / M6). Until then this factory
    returns the :class:`_NullLifecycleExecutor` documented above. Tests
    monkeypatch this function to inject canned executors.

    The returned factory is tagged with ``produces_null_executor = True``
    so the one-shot WARNING probe in ``run_eval`` can classify it
    without instantiating an executor. Constructor side-effects in
    future real executors (PTY descriptors, helper threads, scratch
    dirs) would otherwise leak resources before orchestration starts.
    """

    def factory(**_kwargs: Any) -> LifecycleExecutor:
        return _NullLifecycleExecutor()  # type: ignore[return-value]

    factory.produces_null_executor = True  # type: ignore[attr-defined]
    return factory
```

**Edit 2** — replace the probe with attribute introspection at the WARNING site:

`old_string`:
```python
    _executor_probe = executor_factory()
    if isinstance(_executor_probe, _NullLifecycleExecutor) and not as_json:
        click.echo(
            "eval run: WARNING: _NullLifecycleExecutor active — "
            "non-production executor selected; run results MUST NOT be "
            "treated as authoritative.",
            err=True,
        )
    del _executor_probe
```

`new_string`:
```python
    # We classify by inspecting the ``produces_null_executor`` attribute the
    # factory carries (set in ``_resolve_executor_factory``) rather than by
    # calling ``executor_factory()`` and discarding the result. When M5 / M6
    # lands ``ClaudeProcessAdapter + PtyDriver`` the real executor's
    # constructor will allocate PTY descriptors / helper threads / scratch
    # dirs; instantiating-and-discarding here would leak those resources
    # before per-spec orchestration even starts. Test monkeypatches that
    # inject real executors simply won't set the attribute, so the WARNING
    # correctly suppresses.
    if getattr(executor_factory, "produces_null_executor", False) and not as_json:
        click.echo(
            "eval run: WARNING: _NullLifecycleExecutor active — "
            "non-production executor selected; run results MUST NOT be "
            "treated as authoritative.",
            err=True,
        )
```

## Why this fix is correct

1. **Eliminates all constructor side-effects from the probe** — the only remaining executor-build site is `_run_one_spec` (~line 1453), which is exactly where per-spec construction belongs.
2. **Preserves the test monkeypatch contract** — overrides of `_resolve_executor_factory` that return non-null factories simply won't carry the attribute. `getattr(..., False)` → `False` → WARNING suppresses. Matches the docstring comment.
3. **Preserves `--json` suppression** — `not as_json` clause unchanged.
4. **Forward-compatible with M5/M6** — real factories don't tag themselves; WARNING automatically skips.
5. **Minimal diff** — two edits, no signature changes, no caller updates.

## Alternatives rejected

- **Option A** (identity-compare `executor_factory is _DEFAULT_FACTORY`): rejected — current factory is a fresh closure each call; would need a module-level singleton refactor plus test-monkeypatch surgery.
- **Option B** (instantiate once and reuse as the first spec's executor): rejected — `_run_one_spec` deliberately calls `executor_factory()` per spec for fresh per-eval state; reusing one executor across N specs is itself a side-effect bug.

## Risk + Rollback

Low. Surgical change to one function + one block. No signature or behavior changes for callers. Test monkeypatch contract preserved. Forward-compatible with M5/M6.

Edge case: accidental attribute collision on a mock factory would falsely emit the WARNING. The name `produces_null_executor` is namespaced enough that collision is unlikely; if the team prefers a private contract, change to `_sc_produces_null_executor` (leading underscore + prefix).

## Files that MUST NOT change

- `_NullLifecycleExecutor` class definition (lines ~1365-1391)
- `_run_one_spec` per-spec `executor_factory()` call (around line 1453) — this is the legitimate construction site
- Other callers of `_resolve_executor_factory`
