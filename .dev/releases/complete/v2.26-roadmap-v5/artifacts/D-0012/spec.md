# D-0012: _parse_routing_list() Implementation — spec.md

**Task:** T02.03
**Roadmap Items:** R-022, R-023
**Date:** 2026-03-16
**Status:** COMPLETE

---

## Module Placement

Per D-0006/D-0007 (T01.06 decision): `src/superclaude/cli/roadmap/remediate.py`

---

## Implementation

**File:** `src/superclaude/cli/roadmap/remediate.py`

### New module-level additions

```python
import logging
import re

_log = logging.getLogger(__name__)
_ROUTING_ID_PATTERN = re.compile(r"^DEV-\d+$")
```

### Function signature

```python
def _parse_routing_list(
    raw: str,
    total_analyzed: int | None = None,
) -> list[str]:
```

### Behavior

1. **Split on commas, strip whitespace** from each token
2. **Validate** each token against `^DEV-\d+$`
3. **Exclude** non-conforming tokens with `WARNING` log containing "malformed"
4. **Missing input** (empty/whitespace-only): logs WARNING containing "missing"; returns `[]`
5. **Count cross-check**: if `total_analyzed` is provided and `len(valid) != total_analyzed`, logs WARNING containing "mismatch"

### Distinct log message keywords

| Scenario | Keyword in log message |
|----------|------------------------|
| Empty/whitespace-only input | `missing` |
| Token fails regex | `malformed` |
| Count != total_analyzed | `mismatch` |

---

## Acceptance Criteria Verification

| Criterion | Result |
|-----------|--------|
| `_parse_routing_list("DEV-001, DEV-002")` returns `["DEV-001", "DEV-002"]` | PASS |
| `_parse_routing_list("")` returns `[]` | PASS |
| `_parse_routing_list("DEV-001, INVALID, DEV-002")` returns `["DEV-001", "DEV-002"]` with WARNING | PASS |
| Distinct log messages for missing, malformed, failing count | PASS |

## Test Results

- `uv run pytest tests/roadmap/test_remediate.py -v -k "routing"` → **13 passed**
- Full remediate suite: **69 passed**
