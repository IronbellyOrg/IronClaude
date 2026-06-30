# Phase 3 — detection/classifier test summary

**Overall:** PASS
**Counts:** 14 passed, 0 failed (0.05s) — `uv run pytest tests/pr_submit/test_detection_contract.py -v`

## New V1.1 decline tests (all present and passing)

| Test | FR/EC | Asserts |
|---|---|---|
| `test_t1110_decline_both_regexes_match` | FR-9.1 / T-1110 | both-regex Augment comment → `classify == "declined"`; `is_decline` True |
| `test_t1110b_decline_from_initial_poll` | FR-9.1 | decline at initial S2 poll → "declined" |
| `test_t1111_abnormally_large_without_retrigger_is_not_decline` | T-1111 | phrase-only body is NOT a decline → "polling" |
| `test_t1112_retrigger_instruction_without_phrase_is_not_decline` | T-1112 | re-trigger-only body is NOT a decline → "polling" |
| `test_t1112b_decline_from_non_augment_author_ignored` | T-211 sibling | non-Augment author decline-shape ignored |
| `test_ec23_stale_pre_watermark_decline_ignored` | EC-23 | watermark'd stale decline ignored; None-watermark accepted |

8 pre-existing tests (T-201/202/203/210/211/212, local-override, T-N31) still pass.

## Fixtures added
- `fixtures/decline-comment.json` (schema (a), bot login `augment-code[bot]`)
- `fixtures/decline-initial-poll.json`
- `fixtures/stale-decline-pre-watermark.json` (carries `watermark` + `expected`)

Marker: reused the registered `inv` marker (`--strict-markers` safe). No new marker added.
