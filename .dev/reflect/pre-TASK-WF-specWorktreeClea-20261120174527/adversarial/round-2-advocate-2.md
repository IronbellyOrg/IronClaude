# Round 2: Advocate 2 rebuttal (variant 2, qa lens, haiku class)

Recorded by the orchestrator from the advocate's returned message (the advocate was told not to write files). Nothing below was added to the advocate's text.

- Helper writes (C-002): QUALIFY, MEDIUM. Conceded: fetch is conditional on MERGED, and temporary-file cleanup proves no data loss. Spec lines 32 and 299 require helper reuse; line 256 tests dry run as no removal. The recorder blind spot remains real. Withdraw the demand for a different live lookup. A throwaway checkout could retain the same GitHub origin, so the opponent's claim that it cannot query pull request 700 is incorrect.
- Manual patch and bundle (C-003): ACCEPT, BLOCKING. Reject the downgrade. Spec line 214 expressly promises manual archive behaviour; plan lines 25 and 170 expressly omit it. Correcting this changes a named verb's required behaviour. Missing format details and acceptance cases do not cancel that promise. The narrow reading of line 374 does not resolve the direct mismatch.
- Ordering (C-001): ACCEPT, BLOCKING. Concede variant 2's narrower coverage. Variant 1 supplies the wider cases and collector-test gap; retain variant 2's Task 7 check that needs Task 11. Declared later assertions are not independently blocking.
- Pull-request finish (C-004): ACCEPT, BLOCKING. Concede the original card was truncated. Verified independently: spec lines 276 and 379 require submission; the plan ends without it.
- Provenance count (C-005): ACCEPT, BLOCKING. Fifteen source rows conflict with the plan's required fourteen.
- Removal fallback (C-006): ACCEPT, BLOCKING. The chosen default is not proven unsafe, but replacing item 1's fallback with item 2's changes the required removal path.
- Coverage matrix (C-007): QUALIFY. Neither visible card establishes coverage; truncation is not evidence of a plan defect.
- Safety disagreement (X-001): QUALIFY, MEDIUM. Real side effects, no established destructive consequence. Dependency extent (X-002): ACCEPT, using both lists.
- Per-task timing (A-001): QUALIFY, supported by acceptance blocks and explicit deferrals. Uniform grading (A-002): QUALIFY; consequence, not either card's label, controls.
- New open-pull-request proof: ACCEPT, BLOCKING. Spec line 299 requires OPEN; plan lines 33 and 37 substitute NONE. Fixtures do not satisfy that named proof.
- Updated variant 1: stronger on ordering, count and fallback; incomplete on finish and archive behaviour. Overall FAIL remains.
