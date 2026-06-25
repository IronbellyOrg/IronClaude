# Base State (pre-remediation snapshot)

- **pytest tests/sprint/:** 1163 passed, 0 failed, 20 warnings (deprecation only) — fully green at base.
- **ruff check src/superclaude/cli/sprint/ tests/sprint/:** All checks passed (clean).
- **Baseline note:** No pre-existing failures in scope. Any new failure in later phases is attributable to this remediation. The new positive tests (FIX-1 PRIMARY, FIX-2 injection, FIX-3 strengthened case) are expected to FAIL when first added on this base — that is the fail-on-base proof.
