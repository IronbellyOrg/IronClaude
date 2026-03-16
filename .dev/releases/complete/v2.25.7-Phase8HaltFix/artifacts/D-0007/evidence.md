# D-0007: Per-Phase Isolation Directory with Single-File Copy

**Task:** T02.02 (Milestone M2.2)
**Date:** 2026-03-16
**Status:** COMPLETE

---

## Implementation

Per-phase isolation directory created at `config.results_dir / ".isolation" / f"phase-{phase.number}"` with `shutil.copy2(phase.file, isolation_dir / phase.file.name)` copying exactly one file.

**Location:** `executor.py` lines 535-538 (before per-phase try block, before subprocess launch)

```python
# Per-phase isolation directory: exactly one file (the phase file)
isolation_dir = config.results_dir / ".isolation" / f"phase-{phase.number}"
isolation_dir.mkdir(parents=True, exist_ok=True)
shutil.copy2(phase.file, isolation_dir / phase.file.name)
```

---

## Acceptance Criteria Verification

| Criterion | Status |
|-----------|--------|
| Isolation directory created before subprocess launch | PASS — created at lines 535-538, subprocess launched at line 554 |
| Path: `config.results_dir / ".isolation" / f"phase-{phase.number}"` | PASS |
| `shutil.copy2()` copies exactly one file (the phase file) | PASS |
| Deterministic naming based on phase number | PASS |
| `uv run pytest tests/sprint/ -v --tb=short` exits 0 | PASS — 629 passed |

---

## Single-File Constraint

Only `phase.file` is copied. The directory contains exactly one file at subprocess launch time:
- `isolation_dir / phase.file.name` — the phase tasklist file
- `tasklist-index.md` is NOT copied → mechanically unreachable from subprocess

---

## Test Results

```
uv run pytest tests/sprint/ -v --tb=short
629 passed in 37.27s
```

---

## Milestone M2.2: SATISFIED
