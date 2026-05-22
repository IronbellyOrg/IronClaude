# Tier 1 Hypothesis Card

**Agent**: root-cause-analyst
**Tier**: 1
**Issue**: `NameError: name 'datetime' is not defined` at `payments/refund_handler.py:47` when the worker processes a refund.

## Claim

`payments/refund_handler.py` calls `datetime.utcnow()` on line 47 but never imports the `datetime` module. The `NameError` is raised the first time `RefundHandler.process()` reaches the persistence step.

## Evidence

- **`fixtures/payments/refund_handler.py:7-11`** — Module imports are limited to:
  - `from typing import Optional`
  - `from decimal import Decimal`
  - `from payments.gateway import StripeGateway`
  - `from payments.models import Refund, RefundStatus`

  No `import datetime` or `from datetime import datetime` statement is present anywhere in the file.

- **`fixtures/payments/refund_handler.py:47`** — The offending line reads:
  ```python
          refund.processed_at = datetime.utcnow()
  ```
  At runtime, Python resolves the bare name `datetime` against the module globals, fails, and raises `NameError: name 'datetime' is not defined`. This matches the symptom exactly.

- **Symbol cross-check** — None of the imported symbols (`Optional`, `Decimal`, `StripeGateway`, `Refund`, `RefundStatus`) expose a `datetime` attribute, so there is no alias path that would resolve the name.

## Proposed Fix

Add a `datetime` import at the top of `payments/refund_handler.py`. The conventional form for using `datetime.utcnow()` (a classmethod on the `datetime` class) is:

```python
from datetime import datetime
```

Inserted alongside the existing stdlib imports (after `from decimal import Decimal`, before the first project-local import on line 10).

If the worker is on Python 3.12+, prefer the non-deprecated form:

```python
from datetime import datetime, timezone
...
refund.processed_at = datetime.now(timezone.utc)
```

`datetime.utcnow()` was deprecated in 3.12 in favor of timezone-aware `datetime.now(timezone.utc)`. The fix should match the project's Python version and existing conventions; the minimal change that resolves the NameError is the `from datetime import datetime` line.

## Confidence

**Self-reported: 0.95**

Rationale:
- Symptom (NameError, exact name, exact line) deterministically matches the missing-import explanation.
- File contents directly verified — no `datetime` import is present, line 47 references it.
- Single-domain (Python name resolution); no environment, concurrency, or state dependency.
- Reproducer is deterministic: any call to `RefundHandler.process()` that reaches line 47 fires the error.
- No competing hypothesis survives once imports are inspected.

## Risks

- **Wrong fix variant**: if the project already standardizes on `datetime.now(timezone.utc)` elsewhere, applying `from datetime import datetime` + leaving `utcnow()` perpetuates a deprecation warning. Mitigation: grep the project for prior `datetime` usage and match conventions before patching.
- **Hidden second cause**: extremely unlikely given the symptom, but if another caller monkey-patches `datetime` globally elsewhere, an unrelated name shadowing could re-emerge. The proposed fix at the module scope is robust to that.

## "If I'm wrong it's probably because..."

...the production worker is running a stale/cached `.pyc` from a previous version where `datetime` *was* imported and the missing import is a regression from a recent refactor that's already been reverted upstream. In that case the fix is still correct (defensive), and the diagnosis still names the same line; only the "what changed" narrative shifts.
