# Hypothesis: `payments/refund_handler.py` uses `datetime.utcnow()` without importing `datetime`

**Agent**: root-cause-analyst
**Tier**: 1
**Timestamp**: 2026-05-21T00:00:00Z
**Cause class**: Missing/wrong import

## Claim

`payments/refund_handler.py` references `datetime.utcnow()` on line 47 of `process_refund`, but the module's import block (lines 1-5) never imports `datetime` from the standard library. At module import time the name `datetime` is undefined, so the first call to `process_refund(...)` raises `NameError: name 'datetime' is not defined` exactly at the `refund.processed_at = datetime.utcnow()` assignment. The companion function `build_refund` does not touch `datetime`, which is why nothing breaks until a refund is actually processed.

## Evidence

- `payments/refund_handler.py:1-5` — import block reads:

  ```python
  from typing import Optional
  from decimal import Decimal
  from payments.gateway import StripeGateway
  from payments.models import Refund, RefundStatus
  ```

  No `import datetime` and no `from datetime import datetime`.
- `payments/refund_handler.py:47` — `refund.processed_at = datetime.utcnow()  # line 47` — uses bare `datetime.utcnow()`, which requires the `datetime` class (or the `datetime` module) to be bound in module scope.
- User-reported stack: `NameError: name 'datetime' is not defined` at line 47 — the exact line and exact name match the missing-import hypothesis with no ambiguity.
- Reproduction by inspection: Python's `NameError` for `datetime` at line 47 with no other module-level rebinding is a deterministic outcome of the import gap; no other code path on lines 1-47 would mask or shadow it.

## Proposed Fix

Add a single import to the top of `payments/refund_handler.py`. Two equivalent forms:

- **Option A (recommended)** — `from datetime import datetime` (matches the call style `datetime.utcnow()` and is the most common Python idiom for this usage).
- **Option B** — `import datetime` and change line 47 to `datetime.datetime.utcnow()` (more verbose, only preferable if the module also needs `datetime.date`, `datetime.timedelta`, etc., which this snippet does not).

Files changed:

- `payments/refund_handler.py` — one-line import addition.

Test that proves it:

- Existing: any unit test that calls `process_refund(refund)` will go from `NameError` to passing the `refund.processed_at = ...` assignment.
- New (if none exists): `tests/payments/test_refund_handler.py::test_process_refund_sets_timestamp` — construct a `Refund`, stub `StripeGateway.refund` to return an `ok=True` result, call `process_refund`, assert `refund.processed_at` is a `datetime` instance and `refund.status == RefundStatus.COMPLETED`.

Note: `datetime.utcnow()` is deprecated in Python 3.12+ in favour of `datetime.now(timezone.utc)`. The minimal fix is just the import; the modernisation is a separate concern, flagged in Risks below.

## Confidence

Self-reported confidence: **0.95**

Per-dimension self-assessment:

- Evidence grounding: 1.0 — Exact `file:line` cited; the import block and line 47 are both quoted from the file content provided.
- Symptom coverage: 1.0 — Explains the exact error name (`NameError`), the exact identifier (`datetime`), the exact line (47), and why it only fires when the worker processes a refund (build_refund doesn't touch `datetime`).
- Reproducibility fit: 1.0 — Deterministic exception with a clear trigger (any call to `process_refund`).
- Fix directness: 1.0 — Single-line import addition at the identified file; no other files touched.
- Domain coherence: 1.0 — Single domain (Python module-level name resolution); pure logic fix.

Calibrated mean: **0.95**.

## Risks

- **Wrong import form**: choosing `import datetime` (the module) without updating the call site to `datetime.datetime.utcnow()` would still raise `AttributeError`. Recommend Option A unless the rest of the module needs the bare module.
- **Deprecation warning** (Python 3.12+): `datetime.utcnow()` emits `DeprecationWarning`. The minimal fix does not address this; if the project treats deprecation warnings as errors (e.g. `pytest -W error::DeprecationWarning`), the test will still fail after the import is added. In that case the real fix is `datetime.now(timezone.utc)` and an additional `timezone` import. Flag for the user but do not bundle into the minimum fix.
- **Worker process caching**: if the worker keeps the module loaded across requests, the first failing request may have left transient state (e.g. a half-recorded refund row). After deploying the import fix, confirm no orphan rows.
- **No other regression surface**: the change is purely additive (a new import) and cannot break any other code path in the file.

## If I'm wrong, it's probably because

There is a hidden re-export or a star-import in `payments/models` (or another upstream module) that *used* to bind `datetime` into this module's scope, and a recent change there removed it — making this look like a missing import in this file when the real regression is in the upstream module. Still resolvable by the same one-line import here, but root cause would shift.

## Alternatives considered

- **Stale `.pyc` / module cache**: would not produce a `NameError` at a specific line — it would produce stale behaviour. Rejected.
- **Monkey-patched `datetime` removed at runtime**: theoretically possible (e.g. a test fixture that deletes module attributes), but the user said "I don't see what changed" and the worker is in production, not a test harness. Rejected.
- **`from __future__ import annotations` + a stringified annotation that needs `datetime`**: would fail in `typing.get_type_hints()`, not at the assignment on line 47. Rejected.

## Grounding gaps

- The file is provided inline by the user; the skill could not perform live MCP grounding (auggie/serena) because `payments/refund_handler.py` does not exist on disk in this workspace (this is a contrived test file per the eval framing). All `file:line` citations are against the inline snippet, treated as authoritative per the eval instructions.
- No access to the actual worker logs, git history, or any test file for `payments/`. The hypothesis stands on the snippet + stack trace alone, which is sufficient because the symptom is deterministic and the cause is visible in the imports.
- Did not verify Python version of the runtime; deprecation-warning risk is conditional on 3.12+.
