# D-0006 Evidence — TaskEntry.classifier Field

## Task
T01.04 — Add `classifier` Field to `TaskEntry`

## Change Locations
- `src/superclaude/cli/sprint/models.py` — `TaskEntry` dataclass
- `src/superclaude/cli/sprint/config.py` — `_CLASSIFIER_RE` regex, `parse_tasklist()`

## Changes Made

### models.py — TaskEntry
Added `classifier: str = ""` field (see D-0004 for full dataclass listing).

### config.py — New regex
```python
_CLASSIFIER_RE = re.compile(
    r"^\|\s*Classifier\s*\|\s*([^|]+)\|",
    re.IGNORECASE | re.MULTILINE,
)
```

### config.py — parse_tasklist()
Added extraction: searches for `| Classifier | value |` table row in each task block, strips whitespace.

## Verification
- `uv run pytest tests/sprint/test_preflight.py::TestTaskEntryClassifier -v` → **3 passed**
- `| Classifier | empirical_gate_v1 |` → `"empirical_gate_v1"` ✓
- Missing row → `""` ✓

## Date
2026-03-16
