# Phase 7 Gate A — Final Content Verification (FR-9.5 / T-1117 arbiter + renamed tests)

**Mode:** content verification, `fix_authorization: false` (verify only, nothing modified).
**Scope:** classifier.py FR-9.5 arbiter, test_t1117 non-vacuity, renamed tests T-1113b/T-1114/T-1116.
**Test run:** `tests/pr_submit/test_detection_contract.py` + `test_auggie_fallback.py` = **26 passed**.

---

## (a) test_t1117 is NON-VACUOUS — and WOULD FAIL if the arbiter were removed

The test (`test_detection_contract.py:328-367`) makes four assertions; I reproduced all four
against the live classifier (`watermark="2026-06-12T09:30:00Z"`, decline at 10:00, attributed
re-review at 10:05):

| Assertion | Payload | Expected | Live result |
|---|---|---|---|
| A review-wins (findings) | findings re-review + decline @S5 | `findings` | `findings` ✓ |
| B review-wins (clean) | clean re-review + decline @S5 | `clean` | `clean` ✓ |
| C contrast: initial poll | same payload, `watermark=None` | `declined` | `declined` ✓ |
| D contrast: S5 decline-only | no review + decline @S5 | `declined` | `declined` ✓ |

**Kill-mutant proof.** I re-implemented the pre-fix classifier (unconditional decline-first, arbiter
deleted) and ran the same four payloads:

- A → `declined` → **test FAILS** (asserts `findings`)
- B → `declined` → **test FAILS** (asserts `clean`)
- C → `declined` (still passes — pins FR-9.1 boundary)
- D → `declined` (still passes — pins FR-9.1 boundary)

So removing the FR-9.5 arbiter breaks the test at assertions A and B. The test genuinely guards
review-wins behavior; it is not a tautology. The two contrast assertions (C/D) are load-bearing in
the opposite direction — they stay `declined` under BOTH classifiers, which is exactly what pins the
arbiter so it cannot over-fire into the initial-poll or decline-only cases. Non-vacuous on both
axes (positive: review wins; negative: arbiter doesn't leak).

## (b) Arbiter correctly implements FR-9.5 without breaking FR-9.1 — logic trace

`classify()` (classifier.py:118-182):
1. `decline_present` is computed first (FR-9.1 ordering preserved).
2. When a decline is present, the arbiter (lines 152-164) gates the early `return STATE_DECLINED`
   on `attributed_rereview`, which is `watermark is not None AND ∃ review that (a) `_is_attributed_review`
   (newer than watermark) AND (b) is itself `not is_decline`. Only then does it fall through to
   clean/findings. Otherwise `return STATE_DECLINED`.
3. `watermark is None` (initial poll) → `attributed_rereview` is `False` by construction →
   decline-first holds → **FR-9.1 preserved**.

I exercised the arbiter's three failure-guard edges; all correct:

| Edge | Result | Correct? |
|---|---|---|
| Re-review OLDER than watermark + decline @S5 | `declined` | ✓ stale review not attributed |
| Re-review with NO timestamp + decline @S5 | `declined` | ✓ cannot attribute (line 115 `ts is not None`) |
| Attributed-but-decline-shaped review + decline @S5 | `declined` | ✓ `not is_decline` guard (line 159) |
| Decline-only initial poll (`watermark=None`) | `declined` | ✓ FR-9.1 |

The `not is_decline(r, ...)` guard is essential and present: without it a decline arriving as a
review object (newer than watermark) would self-attribute and wrongly win. It does not.

**Findings-count exclusion** (lines 177-179): decline-shaped comments are filtered out of the
findings-comment count with `is_decline(c, contract, watermark=None)` — a decline is never counted as
a finding. Correct and consistent with the FR-9.1/FR-9.5 handling above.

**No production regression.** The only production caller of `classify` is
`detection.py:226` (`poll_augment_review`), which calls `classify(payload, contract)` with NO
watermark → `watermark=None` → initial-poll semantics → FR-9.5 arbiter dormant, FR-9.1 intact. The
S5 watermark-threading surface is the skill orchestrator (covered by the `run_skill`/`rereview_outcome`
fallback suite), not this convenience seam. The new `watermark` kwarg is keyword-only with a `None`
default, so the existing call site is untouched.

## (c) Renamed tests genuinely test their claimed behavior

| T-ID | Test | Claim | Body actually does | Verdict |
|---|---|---|---|---|
| T-1113b | `test_t1110_t1113b_decline_at_initial_poll_routes_to_fallback` | decline at INITIAL poll → fallback | `review_state="declined"` at initial poll; asserts `fallback_engaged`, `decline_detected`, `round_counter==0` (frozen, no Augment round) | matches ✓ |
| T-1114 | `test_t1114_auggie_at_most_once_across_two_declines_and_resume` | fallback INVOKES auggie, exactly once | drives `_run_fallback` twice on same `SkillResult`, asserts recorder fires once; fresh result invokes (count→2) proving guard is the cause | matches ✓ (explicitly non-vacuous) |
| T-1116 | `test_t1116_fallback_findings_pass_verify_before_remediate` | fallback findings re-enter verify-before-remediate | feeds `unverified` fallback finding; asserts `push_count==0` (dropped), `fallback_engaged`, `TERMINAL_CLEAN` | matches ✓ |

Each renamed test's assertions exercise the behavior its T-ID names; no phantom/label-only coverage.
T-1114 carries its own non-vacuity control (fresh-result re-invoke). T-1113b uses a dual-token name
(T-1110/T-1113b) but the body is the initial-poll decline-routing case the T-1113b token claims.

---

## Self-Audit

- Claims independently verified against source: arbiter logic (classifier.py:118-182), the four
  t1117 assertions (live + mutant), 4 arbiter edge cases, contract default regexes, the 3 renamed
  test bodies, the sole production caller (detection.py:226). All executed, not read-asserted.
- Files Read: classifier.py, test_detection_contract.py (t1117 + fixture), test_auggie_fallback.py
  (T-1113b/T-1114/T-1116), detection.py:205-227, qa-fix-applied-final.md.
- Tool engagement: Read 5 | Grep 3 | Bash 5 (incl. 2 mutant/edge simulations + 1 full suite run).
- Why trust this: I did not rely on the green suite alone — I rebuilt the arbiter-removed classifier
  and proved t1117 assertions A/B flip to `declined` and FAIL, which is the only way to distinguish a
  real guard from a vacuous one.

## Issues Found
None. The F1 fix (FR-9.5 arbiter + non-vacuous T-1117) and F2 fix (T-1113b/T-1114/T-1116 rename)
are correct, non-vacuous, and free of FR-9.1 regression. F3 (MINOR label drift) was deferred by the
fix author and is out of scope for this content gate.

VERDICT: PASS
