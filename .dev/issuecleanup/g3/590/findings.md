## Verdict
**still-relevant.** Issue [590](https://github.com/IronbellyOrg/IronClaude/issues/590) is OPEN, with no comments at the review on 2026-11-24. Its two core gaps remain in the current checkout:

- Detailed worker reads still stop at 50: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/sweep/probes.py:127-183` sets and enforces the limit.
- Ordinary settled workers still need a parsed result contract to appear as finished: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/sweep/classify.py:272-291`. Without it they fall into the unknown class with an explanatory note (`:330-342`). A guard-refused first line is an explicit exception (`:274-278`), so it would be false to say every finished worker needs a contract.

The original sweep and restoration of working-session recognition are already merged in PRs 539 and 579, commits `4d3c0b126151789bd0cb5b481b10f572a0c4e6b7` and `b46ecc1bd47ad817f8cd6181fde0b968dd3f24a0`. Local package history contains those two changes only; this is not evidence of a completed paging fix. No relevant open implementation PR was found in the permitted PR searches for `590` and `sweep`; those searches are not an exhaustive GitHub timeline audit.

## Complexity and size
**complexity medium; size M.** This is a bounded collector/classifier/report change, but list continuation, permitted-command validation, bounded reading, regression tests and one before/after live comparison must agree; changing one number is insufficient.

## Priority
**P2.** Incomplete large-Run visibility makes coordinator decisions harder and is an acceptance gap for the sweep follow-up tracker; there is no verified emergency, data loss or hard block on every other orchestration feature.

## Concrete next steps
1. Keep this issue open. Finish measuring the cause split in `/home/coder/workspaces/IronClaude/.dev/sweeps/20261117-065633-sweep.md` before selecting the implementation. Its header confirms the 264-session, first-page-limited baseline; sampled rows confirm skipped reads and missing contracts. Exhaustive cause counts remain **UNVERIFIED** in this review. Count distinct session IDs in the classification section, not repeated occurrences elsewhere in the report.
2. Have the coordinator reconcile two live owner records on parent issue 534 before choosing cap/paging/newest-first behavior: [07:20:54 paging decision](https://github.com/IronbellyOrg/IronClaude/issues/534#issuecomment-6941538511) says "page", while [07:21:58 measure-before-choice record](https://github.com/IronbellyOrg/IronClaude/issues/534#issuecomment-6941558535) requires measuring before choosing among approaches. Do not silently treat either as revoked. The [2026-11-24 parent review](https://github.com/IronbellyOrg/IronClaude/issues/534#issuecomment-7131840316) likewise leaves reconciliation to the owner. This is a future implementation gate, not a blocker to completing this read-only review.
3. If paging is confirmed, capture current list-continuation responses read-only, then change continuation, permitted-command validation and the detail-read/time budget together. Current collection only marks a full page as truncated; it does not follow it. Preserve an explicit reason for each skipped worker and document the chosen cap/budget rationale.
4. Obtain the separate owner decision on settled/asleep wording, or improve bounded contract discovery/reading instead. Contract collection already exists; do not implement a second reader on the mistaken assumption that none exists. Do not equate an unread result with proven completion, safe closure or a stopped process.
5. Update existing expectations and add focused checks for more than 50 workers, multiple list pages, and a settled worker whose contract cannot be read. Then record a second live run and before/after counts, retaining read-only behavior and the five-minute minimum between sweeps. Neither a test run nor that second live run was authorized/performed here.

## Dependencies
- **Needs evidence and owner decisions:** the historical cause split and reconciliation above; settled/asleep wording is a separate unresolved choice. These are evidence/approval gates, not invented GitHub dependency edges.
- **Feeds issue [534](https://github.com/IronbellyOrg/IronClaude/issues/534), the Phase 1 sweep follow-up tracker:** resolving 590 completes only its scale/restart-visibility slice, not the entire umbrella.
- **Supports issue [339](https://github.com/IronbellyOrg/IronClaude/issues/339), the orchestration program:** 590 says the baseline is too thin for Phase 2. A formal GitHub blocking edge and the claim that all Phase 2 work must wait are **UNVERIFIED**, because the permitted issue-view/list surface was not used to obtain dependency-edge data.

## Related issues
- [534](https://github.com/IronbellyOrg/IronClaude/issues/534), OPEN: parent sweep follow-ups and the two owner records governing the next step. Its accepted output-buffering and outage-summary limits must not be reopened as part of this issue.
- [339](https://github.com/IronbellyOrg/IronClaude/issues/339), OPEN: orchestration program whose first phase introduced sweep.
- No exhaustive related-issue or GitHub event-timeline claim is made; further relationships are **UNVERIFIED**.

## Related PRs
- [539](https://github.com/IronbellyOrg/IronClaude/pull/539), MERGED 2026-11-14: original read-only sweep. Merge commit `4d3c0b126151789bd0cb5b481b10f572a0c4e6b7`; body and comments read.
- [579](https://github.com/IronbellyOrg/IronClaude/pull/579), MERGED 2026-11-17: restores working-session recognition using captured Orca fields. Merge commit `b46ecc1bd47ad817f8cd6181fde0b968dd3f24a0`; body and comments read. It predates the reported run and does not fix list paging or missing-contract presentation. Its reported test count is historical, not a test executed by this review.
- Searches for `590` and `sweep` found no relevant open fix PR. Search returned unrelated PRs too; they were not treated as evidence of a fix. A complete event timeline and unmerged implementations outside those searches remain **UNVERIFIED**.
