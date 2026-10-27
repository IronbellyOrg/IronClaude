# D-0014 Evidence: config parameter added to DiagnosticBundle

**Task:** T04.02 — Add config to DiagnosticBundle
**Date:** 2026-03-16 (updated: remediation RT-01)
**Milestone:** M4.2, M4.3

---

## Change Made

**File:** `src/superclaude/cli/sprint/diagnostics.py`
**Class:** `DiagnosticBundle`

Added `config: SprintConfig | None = field(default=None, kw_only=True)` as a keyword-only dataclass field with `__post_init__` deprecation warning when `config=None`.

**Field added:**
```python
config: SprintConfig | None = field(default=None, kw_only=True)
```

**Deprecation warning in `__post_init__`:**
```python
def __post_init__(self) -> None:
    if self.config is None:
        import warnings
        warnings.warn(
            "DiagnosticBundle.config=None is deprecated; pass SprintConfig",
            DeprecationWarning,
            stacklevel=2,
        )
```

---

## RT-01 Remediation: Runtime Wiring Completed

**Gap identified:** `DiagnosticCollector.collect()` (line 88-91) constructed `DiagnosticBundle` without passing `config=self.config`, leaving the normal runtime path on the deprecated fallback branch.

**Fix applied:** Added `config=self.config` to the `DiagnosticBundle` construction in `collect()`:
```python
bundle = DiagnosticBundle(
    phase=phase,
    phase_result=phase_result,
    config=self.config,
)
```

**Tests added (3 new tests in `TestDiagnosticCollectorConfigWiring`):**
1. `test_collect_passes_config_to_bundle` — verifies `collector.collect()` produces a bundle with `config is config` and zero deprecation warnings
2. `test_bundle_without_config_emits_deprecation` — verifies backward-compat `DiagnosticBundle(config=None)` emits exactly one `DeprecationWarning`
3. `test_classifier_uses_config_path_via_collector` — verifies full runtime chain `collect → classify` uses config-driven paths without deprecation warnings

---

## Acceptance Criteria

| Criterion | Status |
|-----------|--------|
| `config: SprintConfig \| None = None` added as keyword-only parameter | ✅ |
| `config=None` emits `DeprecationWarning` | ✅ |
| All existing `DiagnosticBundle` construction sites compile unchanged (None default) | ✅ |
| `DiagnosticCollector.collect()` passes `config=self.config` into `DiagnosticBundle` | ✅ (RT-01) |
| Normal runtime classification no longer depends on legacy hardcoded-path fallback | ✅ (RT-01) |
| Tests cover config-present runtime path | ✅ (RT-01) |
| Tests cover config-none deprecated fallback path | ✅ (RT-01) |
| `uv run pytest tests/sprint/test_phase8_halt_fix.py -v` exits 0 | ✅ (25 passed) |

---

## Backward Compatibility

All existing construction sites (tests and non-test code) that construct `DiagnosticBundle` without `config=` receive the `DeprecationWarning` at construction, but the code continues to work correctly. The runtime path through `DiagnosticCollector.collect()` now uses the config-driven path as intended.
