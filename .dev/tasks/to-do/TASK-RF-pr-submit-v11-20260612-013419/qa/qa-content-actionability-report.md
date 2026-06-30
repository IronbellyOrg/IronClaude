# QA Report — Content / Actionability / Test-Correctness Lens (Phase 3)

**Topic:** pr_submit V1.1 — decline classification detection contract tests
**Date:** 2026-06-12
**Phase:** task-qualitative (test-correctness / non-vacuity lens)
**Fix cycle:** N/A (fix_authorization: false — report only)
**Stance:** ADVERSARIAL. Assume weak/non-discriminating tests exist; find them by mutation.

---

## Overall Verdict: FAIL

The six new tests are mostly non-vacuous and individually discriminating for the
mutation each was *designed* to catch — **except** the task's premise that the
decline-positive tests catch the AND→OR weakening is FALSE, and the headline
"decline-first ordering" property is **under-tested**: a decline co-occurring with
a findings-bearing review is miscounted as `findings` under a plausible mutation
while **all 14 tests stay green**. That is a missing discriminating test, which
under the no-leniency rule is a FAIL.

All findings below are backed by executed source mutations (classifier restored
after each — `git diff` is clean on `src/`).

---

## Method

Baseline: `uv run pytest tests/pr_submit/test_detection_contract.py` → 14 passed.
For each claimed property I applied a targeted source mutation to
`src/superclaude/pr_submit/classifier.py` (and `detection.py` defaults audit),
re-ran the suite, then restored from backup. Seven mutations (A–G) executed.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | `contract` fixture actually carries decline regexes (not vacuous-because-None) | PASS | Fixture (test L31-41) omits the regexes, but `DetectionContract` bakes defaults (detection.py:78-81). Mutation G confirms the regexes are live. |
| 2 | t1110 positive — decline detected | PASS (with caveat) | Mutation A (remove decline loop) → t1110 fails (`declined`→`polling`). Discriminating for "decline removed". L197 `expected.state` assert is tautological (fixture self-check); L198-199 are load-bearing. |
| 3 | t1110b positive — decline at initial poll | PASS (with caveat) | Mutation A → t1110b fails. Same AND→OR caveat as #5. |
| 4 | t1111 phrase-only → NOT decline | PASS | Mutation G (AND→OR) → t1111 fails. Genuinely guards "phrase alone flips to declined". |
| 5 | t1112 retrigger-only → NOT decline | PASS | Mutation G (AND→OR) → t1112 fails. Genuinely guards the other side of the AND. |
| 6 | t1112b non-augment author → NOT decline | PASS | Mutation F (drop author guard) → t1112b fails. Discriminating. |
| 7 | ec23 watermark staleness | PASS | Mutation E (drop watermark comparison) → ec23 fails. Both branches (stale-ignored + None-accepted) exercised. |
| 8 | **AND→OR caught by decline-POSITIVE tests** (task claim #1) | **FAIL** | Mutation G leaves t1110/t1110b/ec23 GREEN. Positive tests do NOT discriminate AND→OR. |
| 9 | **decline-FIRST ordering vs a findings signal** (docstring "never miscounted as findings") | **FAIL** | Mutation D (decline checked AFTER findings) → all 14 GREEN, yet decline+findings payload returns `findings`. No co-occurrence test exists anywhere in `tests/pr_submit/`. |
| 10 | `inv` marker registered (not silently swallowed) | PASS | pyproject.toml:139 registers `inv`; `--strict-markers` (L111) on. |

---

## Summary
- Checks passed: 8 / 10
- Checks failed: 2 (items 8, 9)
- Critical issues: 1 (item 9 — unguarded miscount-as-findings)
- Important issues: 1 (item 8 — task premise false / coverage asymmetry)
- Minor issues: 1 (item 2 tautological self-assert, documented below)

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | CRITICAL | test_detection_contract.py (whole decline block) + classifier.classify L124-129 | **Decline-FIRST ordering is unguarded.** The docstring promises a decline "is never miscounted as findings" because it is checked FIRST. Mutation D moves the decline check to AFTER the findings determination; **all 14 tests stay green**, but a payload with an Augment review `has_findings:True` PLUS an Augment decline comment returns `findings` instead of `declined`. No test in the entire `tests/pr_submit/` tree exercises decline + findings co-occurrence (every decline fixture has `reviews: []`). | Add a positive test with `reviews:[{login:AUGMENT, has_findings:True}]` AND an Augment decline comment in `comments[]`, asserting `classify(...) == "declined"`. This is the ONLY test that pins the "FIRST" / "never miscounted as findings" property. |
| 2 | IMPORTANT | Task premise #1 / t1110, t1110b, ec23 | **Task's claim that decline-positive tests fail under AND→OR is FALSE.** Mutation G (AND→OR) keeps all positive tests green because their bodies satisfy BOTH regexes (phrase=True, retrigger=True → OR=True). The AND requirement is guarded ONLY by the negative tests t1111 (phrase-only) and t1112 (retrigger-only). Positive tests catch "decline detection removed" (Mutation A) but not the AND→OR weakening. | No code fix required if t1111/t1112 are retained — they fully cover AND→OR. But the task's stated expectation should be corrected: the AND→OR guard is the negatives' job, not the positives'. If positive-side AND coverage is also wanted, the co-occurrence test in issue #1 plus the existing negatives suffice. |
| 3 | MINOR | test_detection_contract.py:197 | `assert payload["expected"]["state"] == "declined"` is a tautology — it asserts the fixture's own embedded `expected` field, which is hand-written into the JSON, not classifier output. It tests nothing about the implementation. The real assertions are L198-199. | Remove L197 or convert `expected.state` into a parametrized driver so the embedded field is actually consumed by the assertion against `classify(...)`, not asserted in isolation. |

---

## Per-Test Discrimination Verdicts (task questions, point by point)

**Q1 — Would each decline-positive test FAIL if decline-first ordering were removed OR AND→OR weakened?**
- Ordering *removed entirely* (Mutation A): t1110, t1110b, ec23 all FAIL → YES, they catch removal.
- Ordering *defeated relative to findings* (Mutation D): all PASS → NO, they do NOT catch the genuine "FIRST" property (issue #1).
- AND→OR weakened (Mutation G): t1110, t1110b, ec23 all PASS → NO, positives do NOT catch AND→OR (issue #2). The task's expectation here is incorrect.

**Q2 — Does t1111 (phrase-only) genuinely guard against "abnormally large" alone flipping to declined?**
YES. Discriminating. Mutation G (AND→OR) makes phrase-only satisfy the predicate; t1111 fails. It catches exactly the regression where the phrase alone flips to `declined`. (phrase=True, retrigger=False → AND=False asserted; OR=True would break it.)

**Q3 — Does t1112 (retrigger-only) genuinely guard the other side?**
YES. Discriminating. Mutation G makes retrigger-only satisfy the predicate; t1112 fails. Catches the regression where a benign re-trigger instruction (no "abnormally large") flips to `declined`. (phrase=False, retrigger=True.)

**Q4 — Does ec23 genuinely exercise watermark staleness; would it fail if the comparison were dropped?**
YES. Discriminating. Mutation E (delete the `if watermark is not None:` block) makes the stale comment pass → ec23 fails on its first assertion (`is_decline(..., watermark=watermark) is False`). It also exercises the None-watermark accept branch (L279-280), so both sides of the watermark gate are covered.

---

## Bonus discrimination confirmed (not asked, but in scope)
- **t1112b** (non-augment author): Mutation F (drop the `_login_of(comment) != bot_login` guard) → t1112b fails. Genuinely guards the author filter; not redundant with t1112.

---

## Mutations Executed (audit trail)

| Mut | Change | Tests failed | Interpretation |
|-----|--------|--------------|----------------|
| A | Remove decline loop in `classify` | t1110, t1110b, ec23 | Positives catch total removal. |
| B | Move decline loop after `return STATE_POLLING` | t1110, t1110b, ec23 | Catches *this* reorder only because fixtures have empty reviews — not a real "FIRST" proof. |
| C | (insertion before findings) | t1110, t1110b, ec23 | Mis-placed; superseded by D. |
| D | Decline checked AFTER findings (empty-review declines preserved) | **none — all 14 green** | **GAP:** decline+findings → `findings`. Unguarded miscount. |
| E | Drop watermark comparison | ec23 | ec23 guards watermark. |
| F | Drop author guard in `is_decline` | t1112b | t1112b guards author. |
| G | AND→OR in `is_decline` | t1111, t1112 only | AND guarded by negatives, NOT positives. |

`src/` restored after every mutation; no source files modified (fix_authorization: false honored).

---

## Self-Audit

**(a) Reliance list — items relied on without re-deriving:**
- Relied on rf-qa / structural gate for: test collection, marker syntax, import resolution. (Independently confirmed 14 collected + `inv` registered anyway.)

**(b) Independent semantic checks (≥1 required):**
- Verified the `contract` fixture is non-vacuous by reading detection.py:78-88 (baked regex defaults) AND running Mutation G to prove the regexes are live, not None.
- Verified the decline-FIRST property by source Mutation D + a hand-crafted decline+findings payload run through the real `classify` — found the miscount the suite misses.
- Verified AND→OR discrimination empirically (Mutation G) rather than trusting the docstring, overturning the task's premise.
- Verified watermark + author guards by deletion mutations E and F.
- Grepped the full `tests/pr_submit/` tree to confirm no other file covers decline co-occurrence.

**Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
**Tool engagement:** Read: 7 | Grep: 4 | Bash(mutation runs): 8 | Glob: 0
No web research performed (all verification was local-file + source-mutation bound).

---

## Recommendations (paste-ready for the builder)

1. **(CRITICAL) Add the missing co-occurrence test** pinning decline-FIRST ordering:
   ```python
   @pytest.mark.inv
   def test_t1110c_decline_wins_over_findings(contract):
       """Decline + a findings-bearing Augment review → 'declined' (FR-9.1 ordering)."""
       payload = {
           "reviews": [{"author": {"login": AUGMENT}, "has_findings": True}],
           "comments": [{"user": {"login": AUGMENT},
                         "body": 'abnormally large; comment "augment review".', "id": 4104}],
       }
       assert classify(payload, contract) == "declined"
   ```
   This is the test that fails under Mutation D and makes "checked FIRST" real.

2. **(MINOR) Drop the tautological self-assert** at L197 (`expected.state == "declined"`), or wire `expected` into a parametrized driver so it is actually consumed.

3. **(IMPORTANT) Correct the task/spec note**: the AND-requirement guard is carried by the negative tests t1111/t1112, NOT by the decline-positive tests. Keep both negatives; do not assume the positives cover AND→OR.

## QA Complete

VERDICT: FAIL
