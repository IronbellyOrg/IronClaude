# P1 Test Summary (Step 2.6)

**Command:** `uv run pytest tests/sprint/test_monitor.py -v`
**Result:** **39 passed, 0 failed** in 2.00s.

All 12 new `TestDetectProviderFailure` cases pass: the six exhaustion fixtures (single-account→SINGLE_ACCOUNT_LIMIT, all-account→ALL_ACCOUNT_COOLDOWN with resolved_model `claude-opus-4-8`, timeout→OPERATION_TIMEOUT, task-failure→NONE, clean→NONE, api_retry_maxed→SINGLE_ACCOUNT_LIMIT), the three OSError/parse-tolerance edges (truncated/empty/missing→NONE), the subtype-trap (subtype:"success"+is_error+429→SINGLE_ACCOUNT_LIMIT), the conservative-default (429 + neither body→SINGLE_ACCOUNT_LIMIT), and the text-core/path-wrapper equivalence. The 27 pre-existing `test_monitor.py` tests (TestPatterns, TestOutputMonitor, TestDetectErrorMaxTurns, TestCountTurnsFromOutput) all still pass — **no regressions**. Pass criterion met.
