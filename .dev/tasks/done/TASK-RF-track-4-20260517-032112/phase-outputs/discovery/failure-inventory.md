# tests/audit/ Failure Inventory

**Total failures:** 1
**Total errors:** 0
**Per-classification:**
- fixture-short: 1
- scanner-wrong: 0
- env-dependent: 0
- flaky: 0

## Classification table

| test_path | assertion_summary | classification | recommended-action | evidence_lines |
|-----------|-------------------|----------------|---------------------|----------------|
| tests/audit/test_credential_scanner.py::TestScanContent::test_detects_real_secrets | `assert result.real_secret_count >= 3` failed: only 2 of 3 expected secrets matched (`aws_access_key`, `generic_password`). The 3rd expected secret `api_key = "FAKEAPIKEY"` cannot match because the regex's trailing character class does NOT include the `"` character. | fixture-short | fix-fixture | src/superclaude/cli/audit/credential_scanner.py:28 — `generic_api_key` pattern `(?:api[_-]?key\|apikey\|api[_-]?secret)\s*[=:"']\s*[A-Za-z0-9_\-]{20,}`. Trailing class `[A-Za-z0-9_\-]` excludes `"`. |

## Notes

This is the AC6 worked example. The fixture in `tests/audit/test_credential_scanner.py` lines 17-26 currently contains `api_key = "FAKEAPIKEY"` (10 chars, double-quoted). The regex character class cannot consume `"`, so the value never enters the `{20,}` quantifier — the inner text length is irrelevant. Fix: remove the surrounding double quotes AND lengthen to ≥20 chars from `[A-Za-z0-9_\-]`.

Sixty-five other pre-existing failures from PR1-3 baseline are OUTSIDE `tests/audit/` (e.g., in `tests/integration/`, `tests/roadmap/`, `tests/sprint/`, etc.) — they are out of scope for this PR per the explicit `tests/audit/` scope in the task title and key objectives.
