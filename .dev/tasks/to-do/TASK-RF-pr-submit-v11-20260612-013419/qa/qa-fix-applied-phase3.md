# Phase 3 — Fix Applied (Step 3.G6)

Single serial writer (the executor, satisfying I20). Fixes for the 4 ACTIONABLE
findings from `qa-consolidated-findings-phase3.md`; F5-F8 deferred/no-fix per the
consolidated dispositions.

| Finding | Fix | Files |
|---|---|---|
| F1 (CRITICAL) backtick-wrapped trigger missed | Widened `decline_retrigger_regex` char class to `["'`+"`"+`]?` (both detection.py sites + ref YAML); added necessary-deviation note comment; added `decline-backtick.json` fixture + `test_t1110_decline_backtick_wrapped_trigger` | detection.py, detection-contract.md, fixtures/decline-backtick.json, test_detection_contract.py |
| F2 (CRITICAL) decline-first ordering untested | Added `test_t1110c_decline_wins_over_cooccurring_findings` (findings-review + decline-comment → "declined"; sanity-asserts the review alone → "findings") | test_detection_contract.py |
| F3 (MINOR) poll_augment_review docstring stale 3-state | Updated module + function docstrings to 4-state (adds "declined") | detection.py |
| F4 (MINOR) EC-23 test not traceable to T-1118 | Renamed test to `test_ec23_t1118_stale_pre_watermark_decline_ignored` + docstring `EC-23 / T-1118` | test_detection_contract.py |

## Deferred / no-fix (documented in consolidated findings)
- F5 bot-login `augment-code[bot]` — Step 3.6 instructed matching existing fixtures; no runtime bug (classify keys on contract field; real locked override uses `augmentcode[bot]`). Logged as Follow-Up Item.
- F6 17 phantom T-IDs — Phase 4/5 tests, not yet built; will land in Steps 4.4/4.5/5.8/5.9.
- F7 phrase regex narrow — kept spec-literal `abnormally\s+large`.
- F8 tautological fixture self-check — harmless.

## Verification
- `pytest test_detection_contract.py` = **16 passed** (was 14; +backtick +co-occurrence).
- `ruff check detection.py` = All checks passed.
- `ruff format --check detection.py test_detection_contract.py` = 2 files already formatted.
- ref YAML still `locked: false`; regex round-trips byte-equal to detection.py default.

No `gh`/`git` token introduced. No `.claude/` path staged.
