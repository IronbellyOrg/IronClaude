# Phase 3 QA — Content Verification (Step 3.G6 fixes F1 + F2)

**Agent:** CONTENT verification (adversarial). `fix_authorization: false` — verify only, modified nothing.
**Date:** 2026-06-12
**Scope:** Confirm the two CRITICAL fixes (F1 backtick regex, F2 decline-first ordering) added
NON-VACUOUS tests that genuinely exercise the fix and would FAIL under the corresponding mutation;
confirm the full module passes; confirm no regression in the pre-existing core tests.

---

## Overall Verdict: PASS

All four confirmations (a)-(d) verified with direct mutation simulation + a clean test run.
Both new tests are non-vacuous and mutation-sensitive, and they guard **orthogonal** failure modes.

---

## (a) F2 — `test_t1110c_decline_wins_over_cooccurring_findings` is NON-VACUOUS

**Test:** `tests/pr_submit/test_detection_contract.py:224-250`

The test builds ONE payload carrying BOTH a findings-bearing Augment review
(`has_findings: True`) AND an Augment decline comment (`abnormally large` + `"augment review"`).
It makes two assertions:

1. **Sanity precondition** (L247-248): `findings_only = {"reviews": payload["reviews"], "comments": []}`
   → `classify(findings_only, contract) == "findings"`. This proves the review alone WOULD be
   "findings", so the decline must actively *win* — it is not a tautology.
2. **Load-bearing assertion** (L250): with the co-occurring decline, `classify(payload, contract) == "declined"`.

**Adversarial mutation simulation** (decline check moved AFTER the findings branch in `classify`),
run against the real classifier internals (`_augment_entries`, `_entry_has_findings`):

| classify call | REAL code | MUTATED (decline-after-findings) |
|---|---|---|
| `findings_only` | `findings` (test expects `findings`) ✓ | `findings` (sanity still passes — correct) |
| co-occur `payload` | `declined` (test expects `declined`) ✓ | **`findings`** → assertion `== "declined"` **FAILS** |

**Result:** Confirmed. If the decline check were moved after the findings branch, the co-occurring
payload returns `"findings"` (the `has_findings: True` review wins), and the L250 assertion
`classify(payload, contract) == "declined"` FAILS. That is exactly the point of the test. The
sanity assertion (L247-248) passes under BOTH real and mutated code, confirming it is a genuine
precondition and the decline-win on L250 is the assertion that actually pins the ordering invariant.
**Source-of-truth:** `classifier.py:124-129` runs the decline loop BEFORE the `not augment_reviews`
/ `_entry_has_findings` branches — the decline-FIRST ordering the test guards.

## (b) F1 — `test_t1110_decline_backtick_wrapped_trigger` genuinely exercises the backtick shape

**Test:** `tests/pr_submit/test_detection_contract.py:210-220` · **Fixture:** `fixtures/decline-backtick.json`

Fixture body: `` "This PR is abnormally large. Comment `augment review` to trigger a new review." ``
(markdown-backtick-wrapped trigger — the real Augment decline shape per memory
`reference_augment_review_triggers`). The test asserts:
- L218 `` "`augment review`" in payload["comments"][0]["body"] `` — confirms the fixture really
  carries the backtick-wrapped shape (not a quote-wrapped substitute).
- L219 `is_decline(payload["comments"][0], contract) is True`
- L220 `classify(payload, contract) == "declined"`

**Adversarial mutation** (backtick removed from the retrigger char class → spec-literal `["']?`),
tested directly against the fixture body:

| body | current regex `["'\`]?` | mutated (spec-literal) `["']?` |
|---|---|---|
| backtick fixture (`` `augment review` ``) | match = **True** | match = **False** |

**Result:** Confirmed. With the backtick removed, the retrigger regex no longer matches the fixture
body, so `is_decline(...)` returns `False` and `classify(...)` returns `"polling"` (no formal review
present) — both L219 and L220 FAIL. The test genuinely exercises the backtick-wrapped real shape and
is mutation-sensitive. **Source-of-truth:** the backtick lives in the char class at
`classifier.py:71` (docstring default), `detection.py:85` (dataclass field default), and
`detection.py:115` (`from_yaml` default) — all three carry `[\"'\`]?`.

**Orthogonality check (adversarial):** the F2 test (a) uses a *double-quote*-wrapped trigger, which
matches the retrigger regex with OR without the backtick change (verified: `True` in both). So F2 is
a pure *ordering* guard and F1 is a pure *regex* guard — the two tests pin **independent** failure
modes; neither accidentally masks the other.

## (c) Full detection-contract module passes

```
$ uv run pytest tests/pr_submit/test_detection_contract.py -q
16 passed in 0.04s
```

16 collected, 16 passed, 0 failed/errored. Matches the 16 `def test_*` functions in the module
(8 core + 6 decline + F1 backtick + F2 co-occurrence; F4 was a rename, not an addition).

## (d) No regression in the 8 pre-existing core tests

The 8 Phase-2 core tests — `t201`, `t202`, `t203`, `t210`, `local_override`, `t211`, `tn31`, `t212`:

```
$ uv run pytest ... -k "t201 or t202 or t203 or t210 or local_override or t211 or tn31 or t212"
8 passed, 8 deselected in 0.04s
```

8 selected, 8 passed. Full-module `-v` grep: 16 PASSED, 0 FAILED/ERROR. No regression.

---

## Self-Audit

**(a) Reliance list — structural items relied on (not re-checked):**
- Relied on the consolidated-findings dispositions for F3/F4/F5-F8 (out of this agent's content scope).

**(b) Independent content checks (≥1 required):**
- F2 ordering invariant — independently re-implemented a mutated `classify` (decline-after-findings)
  against the REAL classifier internals and confirmed the co-occur payload flips `declined`→`findings`,
  i.e. the test assertion would fail. Evidence: `classifier.py:124-129` (decline loop precedes findings branch).
- F1 regex sensitivity — independently ran the current vs spec-literal char class against the actual
  `decline-backtick.json` body; confirmed `True`→`False`. Evidence: `detection.py:85,115`, `classifier.py:71`.
- Orthogonality — independently verified the F2 quote-wrapped body matches the retrigger regex with AND
  without the backtick, proving F1/F2 guard independent failure modes (no accidental masking).
- Fixtures read directly (`decline-backtick.json`, `decline-comment.json`) — backtick shape present in fixture, not asserted-into-existence.

**Confidence:** Verified 4/4 confirmations | Unverifiable 0 | Unchecked 0 | Confidence 100%
**Tool engagement:** Read: 5 (5 prompted files) | Bash: 6 (fixture reads, 2 mutation sims, orthogonality sim, full + filtered test runs) | Grep: 1 (test-fn enumeration)

---

VERDICT: PASS
