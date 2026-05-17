# QA Combined Validation Report — TASK-RF-track-4-20260517-032112

**Mode:** Combined structural + qualitative
**Stance:** Adversarial (assume errors)
**Fix Authorization:** TRUE
**Validator:** rf-qa agent
**Date:** 2026-05-17

---

## CRITICAL FINDING (caught in adversarial verification)

The task's worked example (Step 3.1, repeated in Task Overview, Key Objective 2, Step 5.2 PR body, and Step 5.3 review comment) specifies changing `api_key = "FAKEAPIKEY"` to `api_key = "FAKEAPIKEY_1234567890ABCD"` and claims this satisfies the `[A-Za-z0-9_\-]{20,}` constraint in `src/superclaude/cli/audit/credential_scanner.py:28`.

**This is FACTUALLY WRONG.** Empirically verified by running the actual scanner against the proposed fixture:

```
api_key = "FAKEAPIKEY_1234567890ABCD"  → real_secret_count == 2  (FAIL, needs >= 3)
api_key = FAKEAPIKEY_1234567890ABC     → real_secret_count == 3  (PASS)
```

### Root cause

The `generic_api_key` regex at line 28-31 is:

```python
re.compile(
    r"""(?:api[_-]?key|apikey|api[_-]?secret)\s*[=:"']\s*[A-Za-z0-9_\-]{20,}""",
    re.IGNORECASE,
)
```

The trailing character class `[A-Za-z0-9_\-]` does NOT include the double-quote character `"`. When the value is wrapped in double quotes (`api_key = "FAKEAPIKEY..."`), the regex behavior is:
- `\s*` matches the space after `api_key`
- `[=:"']` matches the `=` (single char)
- `\s*` matches the space after `=`
- `[A-Za-z0-9_\-]{20,}` is asked to start matching at the `"` — which is not in the class, so the match fails.

The fixture value MUST be UNQUOTED for the scanner to detect it as a generic_api_key. Adding more characters inside the quotes makes no difference because the regex can never start consuming inside a quote.

### Secondary inaccuracy

The task narrative claims `"FAKEAPIKEY_1234567890ABCD"` is "24 characters". Empirically it is **25 characters** (F-A-K-E-A-P-I-K-E-Y=10, `_`=11, 1-2-3-4-5-6-7-8-9-0=21, A-B-C-D=25). Even if the regex would have matched, the character count claim is off-by-one.

### Fix applied (per FIX AUTHORIZATION = TRUE)

Worked example corrected to use the **unquoted** form `api_key = FAKEAPIKEY_1234567890ABC` (24 chars, no surrounding quotes). This passes the scanner empirically. All five references in the task file updated:

1. Task Overview (line 57)
2. Key Objectives item 2 (line 64)
3. Step 3.1 worked-example diff (line 169) — added explicit note about why the quote is removed
4. Step 5.2 PR body bullet (line 209)
5. Step 5.3 in-line review comment body (line 213)

Empirical verification log (run against current `src/superclaude/cli/audit/credential_scanner.py`):

```
Baseline (existing fixture):
  api_key = "FAKEAPIKEY"               → real_secret_count == 2  (test FAILS)

Original proposed fix in task:
  api_key = "FAKEAPIKEY_1234567890ABCD" → real_secret_count == 2  (test STILL FAILS — quote-class mismatch)

Corrected fix (applied by QA):
  api_key = FAKEAPIKEY_1234567890ABC    → real_secret_count == 3  (test PASSES)
```

---

## Structural Checklist

| # | Check | Status | Evidence |
|---|---|---|---|
| 1-13 | Standard frontmatter, branch `fix/ci-rot-pr4-test-fixture-repair`, PR title `fix(tests): repair tests/audit/ fixtures + xfail genuinely-broken cases` | PASS | Frontmatter lines 1-51 present; branch name in Step 1.4 (line 135); PR title in Step 5.2 (line 209) |
| 14 | `blockedBy: TASK-RF-track-3-…`; `blocks: TASK-RF-track-5-…` | PASS | Lines 47-50 |
| 15 | Discovery phase produces classification table (test_path, assertion_summary, classification, recommended-action) | PASS | Step 2.2 (line 149) specifies columns `test_path | assertion_summary | classification | recommended-action | evidence_lines` |
| 16 | NFR4 escalation gate present: >20 failures → HALT + escalate | PASS | Step 2.3 (line 153) with explicit >20 threshold and `/sc:task --compliance strict` escalation |
| 17 | Worked example (3.1) cites exact line numbers + exact diff | PASS (post-fix) | Step 3.1 cites `tests/audit/test_credential_scanner.py` lines 17-26 and scanner file line 28; diff explicit after correction |
| 18 | AC6 in-line PR comment requirement explicit | PASS | Step 5.3 (line 213) is dedicated to AC6 in-line comment with `gh api repos/:owner/:repo/pulls/<PR-NUMBER>/comments` |
| 19 | Umbrella issue or per-xfail issue pattern decision made | PASS | Step 2.4 (line 157) draft + create single umbrella issue; xfail `reason=` uses its URL |

## Qualitative Checklist

| # | Check | Status | Evidence |
|---|---|---|---|
| 20 | `uv run pytest tests/audit/ -v --tb=short` is the discovery command | PASS | Step 2.1 (line 145) |
| 21 | `@pytest.mark.xfail(strict=True, reason="...")` syntax is correct | PASS | Used in Overview, Key Objectives 3, Step 2.3, Step 3.2, etc. `strict=True` correctly chosen so accidental fixture fixes XPASS loudly |
| 22 | Worked example matches scanner `{20,}` requirement | **FAIL (original) → PASS (post-fix)** | Original: quoted form never matches regex — see Critical Finding above. Post-fix: unquoted 24-char form matches and produces `real_secret_count == 3`. |
| 23 | Verify phase runs `pytest tests/audit/test_credential_scanner.py::TestScanContent::test_detects_real_secrets -v` and asserts pass | PARTIAL | Step 3.1 (line 169) runs `uv run pytest tests/audit/test_credential_scanner.py -v` (whole file, not single test) and requires `test as PASSED` before marking complete. Whole-file scope is acceptable — strictly broader than spec, but satisfies the assert-pass requirement. Step 4.1 then re-runs full `tests/audit/` (AC3). |
| 24 | NFR2 transitivity: full pytest outside tests/audit/ runs in Verify phase | PASS | Step 4.2 (line 189) runs `uv run pytest -v --ignore=tests/audit 2>&1` |
| 25 | PR body has explicit AC6 placeholder/instruction for reviewer to add in-line comment | PASS | Step 5.2 PR body (line 209) includes closing line "AC6 in-line review comment to be added on the credential_scanner.py fixture diff explaining the 10→24 char change and the {20,} pattern constraint"; Step 5.3 then automates the comment posting via `gh api`. Both belt-and-suspenders coverage. |

---

## Additional observations (non-blocking)

- **Step 3.1 dependency on FIXTURE_CONTENT line numbers:** Task cites lines 17-26 for `FIXTURE_CONTENT`. Empirically the constant spans lines 17-26 in current `test_credential_scanner.py`. Verified accurate.
- **Step 5.3 escape sequences:** The bash heredoc-style `gh api ... -f body="..."` includes `[A-Za-z0-9_\\\\-]{20,}` (four backslashes) to survive shell + JSON escaping. After QA fix, the body text also updated to reflect the corrected worked example (unquoted form, accurate char count).
- **Step 3.1 verification scope:** The step writes raw pytest output to `credential-scanner-after-fix.txt` then visually checks for PASSED. Adversarial concern: if pytest exits non-zero, the redirect still captures output, and the orchestrator may incorrectly mark complete. Mitigation: Step 3.1 final clause explicitly says "do not mark complete until the test passes — this is the AC6 worked example and MUST succeed". Acceptable.
- **Step 5.3 fallback to PR-level comment:** When `gh api` rejects line/path combo, fallback to `gh pr comment` is acceptable per the task wording. AC6 in-line preference preserved, fallback documented.

---

## Verdict Summary

| Layer | Original | Post-Fix |
|---|---|---|
| Structural | PASS | PASS |
| Qualitative | **FAIL** (item 22 — worked example does not actually pass the test) | PASS |
| Overall | **FAIL** | **PASS** |

**VERDICT: PASS (after in-place fix applied per FIX AUTHORIZATION = TRUE)**

Without the fix this task would have looped in the F1 execution loop at Step 3.1 indefinitely, because the test would never reach PASSED status with the originally-prescribed fixture edit. The corrected unquoted 24-char form is empirically verified to produce `real_secret_count == 3`.
