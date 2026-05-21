# Troubleshoot Report — `NameError: name 'datetime' is not defined`

**File**: `payments/refund_handler.py`
**Symptom**: `NameError: name 'datetime' is not defined` at line 47, raised when the worker processes a refund.
**Mode**: Diagnosis-only (no `--fix` flag provided). No code changes applied.

---

## 1. Issue Description

`process_refund()` sets:

```python
refund.processed_at = datetime.utcnow()  # line 47
```

At runtime Python resolves the bare name `datetime` against the module's global namespace. That namespace does not contain a binding called `datetime`, so a `NameError` is raised the moment that line executes.

`build_refund()` does not touch `datetime`, which is why the error only surfaces on the `process_refund` code path (worker refund processing), not on refund construction.

## 2. Root Cause Analysis

The imports block at the top of the file is:

```python
from typing import Optional
from decimal import Decimal
from payments.gateway import StripeGateway
from payments.models import Refund, RefundStatus
```

There is **no import of `datetime`** — neither `import datetime` (which would bind the *module* `datetime`, requiring `datetime.datetime.utcnow()`) nor `from datetime import datetime` (which would bind the *class* `datetime`, giving access to `datetime.utcnow()` exactly as used on line 47).

Because line 47 calls `datetime.utcnow()` — `utcnow` invoked directly on `datetime` — the code is written against the **class** `datetime`, not the module. The required import is:

```python
from datetime import datetime
```

### Why "I don't see what changed" is plausible

`utcnow()` is a `classmethod` on `datetime.datetime`. If this file was recently refactored (unused-import sweep, import reordering, dropped merge hunk) the `from datetime import datetime` line could have been removed without any test catching it — `build_refund` does not exercise the missing name, and unit tests that only touch `build_refund` would still pass. The error only manifests on the worker's `process_refund` path, matching the reported symptom.

Evidence:

- Line 47 uses `datetime.utcnow()` — confirms a `datetime`-class call site.
- Lines 2–5 contain no `datetime` import — confirms the name is unbound at module scope.
- No local assignment or parameter shadows `datetime` inside `process_refund` — confirms the failure is at global lookup.
- `build_refund` does not reference `datetime` — explains why the bug is path-specific.

Confidence: high (>=95%). The error message, the offending line, and the imports block are mutually consistent; no alternative root cause fits all three.

## 3. Proposed Solutions (Ranked)

### Option A (recommended) — Add the missing import

Add to the imports block:

```python
from datetime import datetime
```

- **Effort**: 1 line.
- **Risk**: Negligible. Matches the existing call shape `datetime.utcnow()` exactly; no other code changes.
- **Why first**: Minimum-diff fix that restores the original intent of line 47 with zero behavioral change beyond resolving the `NameError`.

### Option B — Switch to timezone-aware UTC (modernization)

```python
from datetime import datetime, timezone
...
refund.processed_at = datetime.now(timezone.utc)
```

- **Effort**: 1 import line + 1 call-site change.
- **Risk**: Low–medium. `datetime.utcnow()` returns a *naive* datetime; `datetime.now(timezone.utc)` returns an *aware* one. If `Refund.processed_at` (or downstream serializer / DB column / comparison) assumes naive UTC, this can produce subtle bugs ("can't compare offset-naive and offset-aware datetimes"). Requires checking `payments.models.Refund` and persistence layer.
- **Why second**: `utcnow()` is deprecated in Python 3.12+, so this is long-term correct — but it expands scope beyond the reported bug and should not be bundled into the `NameError` fix without confirming downstream tolerance.

### Option C — Import the module instead

```python
import datetime
...
refund.processed_at = datetime.datetime.utcnow()
```

- **Effort**: 1 import line + 1 call-site change.
- **Risk**: Low, but stylistically worse and touches the call site unnecessarily.
- **Why third**: Functionally equivalent to A with worse ergonomics.

## 4. Risk Assessment Summary

| Option | Diff size | Behavioral change | Recommended? |
|---|---|---|---|
| A — `from datetime import datetime` | 1 line | None beyond fixing the crash | Yes |
| B — `datetime.now(timezone.utc)` | 2 lines + downstream audit | Naive → aware datetime; possible downstream impact | Only if modernization is in scope |
| C — `import datetime` + `datetime.datetime.utcnow()` | 2 lines | None beyond fixing the crash | No (worse ergonomics than A) |

## 5. Next Step

Per the command's CRITICAL BOUNDARIES, no fix has been applied. To proceed:

- Re-run with `--fix` to apply **Option A** (`from datetime import datetime`).
- Or, if modernizing simultaneously, request **Option B** explicitly and first confirm `Refund.processed_at` / its serializer tolerates timezone-aware datetimes.
