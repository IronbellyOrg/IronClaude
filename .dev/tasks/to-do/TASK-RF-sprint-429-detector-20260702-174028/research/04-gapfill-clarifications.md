# Research: Gap-Fill Clarifications (round 1)

**Topic type:** Gap-fill (authoritative resolutions for A.8 research-gate FAILs)
**Status:** Complete
**Date:** 2026-07-02

This file resolves the IMPORTANT/MINOR findings from the research gate (G-C, G-D, G-E, G-A/F).
Where it conflicts with earlier research, **this file is authoritative**. No re-research was needed —
these are authoring-precision clarifications for the verification surface. All resolutions are
grounded in the current source + the verified Shape-2 behavior (the current detector returns
`ProviderFailure.NONE` on `research/shape2-verbatim-transcript.jsonl`; the loosened C8 regex captures
`gpt-5.5` — both verified this turn).

---

## R-GE — Shape-2 fixture source is the verbatim capture (re-fabrication trap closed)

`research/02` §3 + Summary are now corrected. **Authoritative rule:** author
`tests/sprint/fixtures/exhaustion/all_account_cooldown_apierror429.jsonl` by copying the LAST
`{"type":"result"}` line of `research/shape2-verbatim-transcript.jsonl` **byte-for-byte**. Do NOT use
`.dev/troubleshoot/429-signature-ground-truth.md` (Shape 1 only) and do NOT copy the non-authoritative
illustration. The fixture may be just that single `result` line (the detector keys on the last result
event), or all 3 lines of the reference transcript for realism — the `result` line MUST be verbatim.

## R-GC — F5 "timeout unreachability" = mutual-exclusivity, TWO directional assertions

The naive "both signals in one body" fixture is **impossible and must NOT be authored**: the timeout
branch requires `body == "API Error: The operation timed out."` (exact equality, `monitor.py:335-338`)
while the new 429 text-gate requires `"rate_limit_error" in body` (substring) — a single body cannot
satisfy both. F5 instead asserts the two branches stay **mutually exclusive** under the widened gate,
with two directional assertions (both against real fixtures, no new fixture needed):

- **F5.a (timeout not swallowed):** `detect_provider_failure(operation_timeout.jsonl).kind is
  ProviderFailure.OPERATION_TIMEOUT`. Rationale: the timeout body has no `rate_limit_error` and
  `api_error_status is None` (not 429), so BOTH disjuncts of the new C1 gate are False → the 429 block
  is skipped → control reaches the timeout branch. This is the existing behavior, and it PROVES
  widening the gate did not capture the timeout. (This row = contract-table row 10; F5.a may simply be
  that row, or a dedicated assertion citing it.)
- **F5.b (429 returns before the timeout branch):** `detect_provider_failure(
  all_account_cooldown_apierror429.jsonl).kind is ProviderFailure.ALL_ACCOUNT_COOLDOWN` (NOT
  `OPERATION_TIMEOUT`). Rationale: the 429 block at `:323-333` returns before `:335` is reached.

Together F5.a + F5.b are the unreachability guard. No mutually-impossible fixture is created; the
timeout branch stays byte-unchanged (C3). Keep this as ONE task item titled "F5 timeout mutual-
exclusivity guard (two directional assertions)".

## R-GD — Contract-table matrix: the 12 enumerated rows ARE the table; xfail only for the unrealizable

The spec's "empty/impossible cells are explicit `xfail` — never silent omission" does **not** mean
author a full 2×2×2 combinatorial grid with blank cells. It means: enumerate every MEANINGFUL
transcript case as a concrete `pytest.mark.parametrize` row, and if a case is impossible or not
capturable, represent it with an EXPLICIT marked row rather than dropping it. Concrete convention:

- One `pytest.param(...)` per row with a stable `id=` (e.g. `id="shape2-all-account-gpt55"`).
- Each row is `(source, expected_kind, expected_model)` where `source` is EITHER a fixture filename
  under `_FIXTURES` (for the 6 existing + 3 new fixtures) OR an inline transcript written via
  `tmp_path.write_text('{...}\n')` (for synthetic permutation rows 5 and 6).
- Assert BOTH `sig.kind is ProviderFailure.<X>` AND `sig.resolved_model == <str|None>` on EVERY row
  (incl. `None` on the 8 non-cooldown rows — OQ4; guards a greedy-regex regression).
- The ONLY row that may carry an `xfail`/marker is the OQ2 synthesized single-account (row 7): it is a
  documented ASSUMPTION (no verbatim capture). Represent it as a normal passing row against the
  `_SYNTHESIZED` fixture, with an in-test comment; optionally
  `marks=pytest.mark.xfail(reason="synthesized — no verbatim Shape-2 single-account capture; flip to a
  real fixture when captured", strict=False)` if you prefer it to advertise the assumption. Either is
  acceptable; do NOT silently omit it.
- There are NO other blank cells to xfail — the 12 rows below cover the matrix.

## R-row5 — Row 5 model string pinned

Row 5 (all-account body WITHOUT "via provider" but WITH `api_error_status:429`; proves C8 is
independent of the structured field) uses model **`claude-opus-4-8`** (a minimal delta from the
Shape-1 all-account fixture). Expected `(ALL_ACCOUNT_COOLDOWN, "claude-opus-4-8")`. Author it inline
via `tmp_path.write_text` with body `API Error: Request rejected (429) · All credentials for model
claude-opus-4-8 are cooling down` (no "via provider") and `"api_error_status":429`.

## R-GA/7c — FP parity assertion is the NEGATIVE, not "is PASS"

For the `is_error:false` incidental-429 FP fixture (`provider_429_incidental_ratelimit_text.jsonl`):
- `detect_provider_failure(fp).kind is ProviderFailure.NONE` (the `is_error` guard short-circuits).
- Offline parity (7c): assert `_classify_transcript(fp_text) is not TaskStatus.FAIL_PROVIDER_EXHAUSTED`
  — the NEGATIVE form. Do NOT assert `is TaskStatus.PASS_RECOVERED`/`is <specific PASS>`; a non-429
  result may legitimately map to several non-exhaustion statuses, and the contract we defend is only
  "not misclassified as provider-exhausted." (The FP fixture with `is_error:false` will in practice
  map to a success/clean status, but the robust, non-brittle assertion is the negative.)

## R-GF — RED→GREEN set (which assertions must be RED pre-fix)

Author fixtures + tests FIRST and confirm these FAIL against the UNPATCHED `monitor.py`, proving they
exercise the real gap (verified reasoning against current source):
- **Row 4** (Shape-2 all-account, `api_error_status` absent): pre-fix → NONE (gate never opens). RED.
- **Row 6** (Shape-1 all-account WITH "via provider" but `api_error_status` ABSENT): pre-fix → NONE
  (gate never opens; proves the C1 text gate). RED.
- **Row 5** (all-account NO "via provider", `api_error_status:429`): pre-fix the gate opens (aes==429)
  but `_RE_ALL_ACCOUNT` needs "via provider" → neither-body default → SINGLE_ACCOUNT_LIMIT ≠ expected
  ALL_ACCOUNT_COOLDOWN. RED (proves C8).
- **Parity 7b** (`_classify_transcript(shape2)` → FAIL_PROVIDER_EXHAUSTED): pre-fix → not-exhausted. RED.
- Rows 1-3, 9-12 + parity 7c/7d + F5.a: GREEN both pre- and post-fix (back-compat / already-correct
  paths). Post-fix: ALL rows + all 4 parity asserts + F5.a/F5.b GREEN, and all 6 legacy fixtures pass.

## The 12 contract-table rows (authoritative, parametrize-ready)

| id | is_error | api_error_status | body signature | source | expected kind | expected model | RED pre-fix? |
|----|----------|------------------|----------------|--------|---------------|----------------|--------------|
| 1 shape1-all-account | true | 429 | Request rejected (429)…via provider | fixture all_account_cooldown | ALL_ACCOUNT_COOLDOWN | claude-opus-4-8 | no |
| 2 shape1-single | true | 429 | would exceed your account's rate limit | fixture single_account_429 | SINGLE_ACCOUNT_LIMIT | None | no |
| 3 shape1-retry-maxed | true | 429 | would exceed…(api_retry maxed) | fixture api_retry_maxed | SINGLE_ACCOUNT_LIMIT | None | no |
| 4 shape2-all-account | true | absent | API Error: 429 …gpt-5.5 cooling down | fixture all_account_cooldown_apierror429 (VERBATIM) | ALL_ACCOUNT_COOLDOWN | gpt-5.5 | **YES** |
| 5 all-account-no-viaprovider-aes | true | 429 | Request rejected (429)…cooling down (no via provider) | inline tmp_path | ALL_ACCOUNT_COOLDOWN | claude-opus-4-8 | **YES** |
| 6 shape1-all-account-no-aes | true | absent | Request rejected (429)…via provider | inline tmp_path | ALL_ACCOUNT_COOLDOWN | claude-opus-4-8 | **YES** |
| 7 shape2-single-SYNTHESIZED | true | absent | API Error: 429 …would exceed…rate limit | fixture single_account_apierror429_SYNTHESIZED | SINGLE_ACCOUNT_LIMIT | None | maybe |
| 8 rate_limit_error-neither-body | true | absent | rate_limit_error, no all/single markers | inline tmp_path | SINGLE_ACCOUNT_LIMIT | None | maybe |
| 9 fp-incidental-429 | false | null/absent | "429"/"rate limit" incidental prose | fixture provider_429_incidental_ratelimit_text | NONE | None | no |
| 10 timeout | true | null | API Error: The operation timed out. | fixture operation_timeout | OPERATION_TIMEOUT | None | no |
| 11 real-task-failure | true | absent | error_during_execution "pytest exited 1" (no rate_limit_error) | fixture task_failure_real | NONE | None | no |
| 12 clean-pass | false | null | Task complete. | fixture clean_pass | NONE | None | no |

Rows 5, 6, 8 are inline synthetic transcripts (author via `tmp_path.write_text`); rows 1-3, 9-12 use
existing fixtures; rows 4, 7 use the new fixtures. Row 8 documents the INV-001 residual (rate_limit_error
present but no provider body → conservative SINGLE_ACCOUNT_LIMIT default; expected, bounded).
