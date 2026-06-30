# Phase 7 Gate A — Structural Final-Verification (post-fix re-check)

**Stance:** adversarial, verify-only (`fix_authorization: false` — nothing modified).
**Scope:** confirm the 2 ACTIONABLE crossref fixes (F1, F2) landed and INV-001 is untouched.

## Checks

### (a) F1 — FR-9.5 arbiter + decline-not-a-finding — PASS

- `_is_attributed_review(review, watermark)` helper present: `classifier.py:100-115`.
  - `watermark is None → True` (initial poll treats any review as attributed): `classifier.py:110-111`.
  - watermark set → attributed only when `ts > watermark`, and a review with no timestamp cannot be attributed: `classifier.py:112-115`.
- FR-9.5 arbiter inside `classify()`: `classifier.py:151-164`. After `decline_present` is detected (`:147-151`), it computes
  `attributed_rereview = watermark is not None and any(_is_attributed_review(r, watermark) and not is_decline(r, ...) for r in augment_reviews)` (`:157-161`); returns `STATE_DECLINED` only when **not** attributed (`:162-163`), else falls through to clean/findings. This is exactly: S5 watermark + genuine attributed re-review → review wins; initial poll (`watermark=None`) → `attributed_rereview` is `False` → decline-first.
- Decline-shaped comment excluded from findings count: `classifier.py:177-179`
  `finding_comments = [c for c in augment_comments if not is_decline(c, contract, watermark=None)]` — a decline is never counted as a finding.
- Behavioral proof: `test_t1117_ec22_attributed_rereview_wins_over_decline` (`test_detection_contract.py:328-367`) asserts all four branches:
  findings-review-wins (`:350`), clean-review-wins (`:353-360`), initial-poll decline-first (`:362`), S5 decline-only stays declined (`:364-367`).

### (b) F2 — 3 phantom T-IDs + T-1117 each resolve to a real test — PASS

`grep -rnE 'T-?1113b|T-?1114|T-?1116|T-?1117' tests/pr_submit/`:

- T-1113b → `test_auggie_fallback.py:56` `test_t1110_t1113b_decline_at_initial_poll_...`
- T-1114  → `test_auggie_fallback.py:94` `test_t1114_auggie_at_most_once_...`
- T-1116  → `test_auggie_fallback.py:209` `test_t1116_fallback_findings_pass_verify_before_remediate`
- T-1117  → `test_detection_contract.py:328` `test_t1117_ec22_attributed_rereview_wins_over_decline`

All 4 resolve to real, named test functions (token in both name and docstring). No phantom remains.

### (c) INV-001 UNTOUCHED — PASS

- `grep -nE '[^_]round_counter \+= 1' fsm.py` → **exactly 1 hit**: `fsm.py:1001 result.round_counter += 1`.
- Cross-check `grep -rnE 'round_counter \+= 1' fsm.py` → 2 hits: `fsm.py:782` (`fallback_round_counter`, a SEPARATE counter, correctly excluded by the `[^_]` guard) + `fsm.py:1001` (the canonical INV-001 site). The single attributed-re-review increment at `fsm.py:1001` is intact; the fix is classifier-only — no fsm.py edit.

### (d) No new issue; FR-9.1 (decline-first at initial poll) still holds — PASS

- FR-9.1 preserved structurally: `classify(..., watermark=None)` ⇒ `attributed_rereview = False` (`classifier.py:157`, `watermark is not None` short-circuits) ⇒ `return STATE_DECLINED`.
- Independently tested: `test_detection_contract.py:362` (initial poll → "declined") AND `test_auggie_fallback.py:56` `test_t1110_t1113b_...` (initial-poll decline → fallback, `round_counter == 0`).
- Full suite: `uv run pytest tests/pr_submit/ -q` → **176 passed in 0.25s** (175 → +1 T-1117), matching the claimed count. No regression.

## Adversarial probes (negative findings)

- Checked the `_is_attributed_review` timestamp keys (`createdAt`/`created_at`/`submittedAt`, `classifier.py:112-114`) cover the T-1117 fixture's `createdAt` — match.
- Confirmed the arbiter re-runs `is_decline` to exclude a decline-shaped "review" from counting as the attributed re-review (`classifier.py:159`) — a decline can't win over itself.
- Confirmed the `[^_]` regex in (c) is the discriminating guard, not luck: line 782's `fallback_round_counter` is preceded by `_`, so it is correctly NOT counted as an INV-001 site.

## Confidence

- Verified: 4/4 claims | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
- Tool engagement: Read: 4 | Grep: 3 | Bash(pytest): 1

VERDICT: PASS
