# D-0015 Evidence: FailureClassifier uses config-driven path resolution

**Task:** T04.02 — Update FailureClassifier path resolution
**Date:** 2026-03-16 (updated: remediation RT-01)
**Milestone:** M4.2

---

## Change Made

**File:** `src/superclaude/cli/sprint/diagnostics.py`
**Method:** `FailureClassifier.classify()`

Replaced hardcoded output-file path construction with `bundle.config.output_file(bundle.phase_result.phase)` when config is available. Falls back to legacy hardcoded path with deprecation warning when `config is None`.

**Code:**
```python
if bundle.config is not None:
    output_file = bundle.config.output_file(bundle.phase_result.phase)
else:
    import warnings
    warnings.warn(
        "DiagnosticBundle.config=None is deprecated; pass SprintConfig",
        DeprecationWarning,
        stacklevel=2,
    )
    output_file = bundle.phase_result.phase.file.parent.parent / "results" / f"phase-{bundle.phase_result.phase.number}-output.txt"
```

---

## RT-01 Remediation: Full Runtime Path Now Config-Driven

**Gap identified:** While `FailureClassifier.classify()` correctly used `bundle.config.output_file()` when config was present, `DiagnosticCollector.collect()` was constructing `DiagnosticBundle` **without** `config=self.config` — so the runtime path always hit the deprecated fallback.

**Fix applied:** `DiagnosticCollector.collect()` now passes `config=self.config`:
```python
bundle = DiagnosticBundle(
    phase=phase,
    phase_result=phase_result,
    config=self.config,
)
```

**Verified by:** `test_classifier_uses_config_path_via_collector` — exercises full chain `DiagnosticCollector.collect()` → `FailureClassifier.classify()` with zero deprecation warnings, confirming the runtime path is fully config-driven.

---

## Acceptance Criteria

| Criterion | Status |
|-----------|--------|
| `FailureClassifier.classify()` uses `bundle.config.output_file()` when config is available | ✅ |
| `config=None` path emits deprecation warning and falls back to legacy path | ✅ |
| Runtime path through `DiagnosticCollector` → `FailureClassifier` is fully config-driven | ✅ (RT-01) |
| `uv run pytest tests/sprint/test_phase8_halt_fix.py -v` exits 0 | ✅ (25 passed) |
