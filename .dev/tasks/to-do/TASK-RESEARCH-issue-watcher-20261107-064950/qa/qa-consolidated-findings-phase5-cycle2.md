# Consolidated findings: Phase 5 synthesis gate (Gate 2), fix cycle 2

Sources: cycle-1 verification reports `qa/qa-verification-phase5-structural.md` (VERDICT: PASS) and `qa/qa-verification-phase5-content.md` (VERDICT: FAIL). Halt guards before this cycle: (1) regression check: no previously PASS item is FAIL now (findings 1 to 3 are confirmed fixed; finding 4 was never PASS), so no regression halt; (2) monotonicity check: open blocking findings before the fix = 4, now = 1, so |F| shrank and no monotonicity halt; hard cap not reached (fix cycle 2 of 2 allowed).

Count line: blocking 1, minor 0 (resolved and minor findings are not listed again).

| # | Finding | Affected synthesis file | Severity | Blocking | Proposed fix |
|---|---|---|---|---|---|
| 1 | The truncation guard added for the approval-check page cap (synth-04 step 4.2 and the "Truncated read" test) checks whether a page is "still full (100 items)", but `events-jq` and `marker-jq` (synth-04 lines ~194-195) already reduce each page to label events or comment ids before the code sees it. A raw page of 100 events holding 40 label events comes back with 40 items, so the guard cannot fire on real data and a short filtered page looks like the end of the list; the approval and claim-marker checks can still decide on partial data. The test fixture feeds 100 label events per page and skips the filter, so it would pass anyway. | synth-04 (step 4.2, the jq filters, the "Truncated read" scenario and test, the claim-marker read) | IMPORTANT | yes | Return the raw page length with the filtered items (for example `{n: length, items: [...]}`); page while `n == 100`; raise `E-GH-TRUNCATED` when `n == 100` at `max_pages`, for both `label_events` and `own_claim_comment_ids`; build the test fixtures from raw pages that hold fewer than 100 label events (and one that reaches the cap with filtered pages shorter than 100) so the test exercises the filter. |

Consolidated verdict: FAIL (1 blocking finding). Minor notes from the cycle-1 content report remain notes.
