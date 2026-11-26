# Cross-Validation Report: issue 354

- **Date:** 2026-11-23
- **Template:** /home/coder/.claude/templates/modularization-template-review/analyst-cross-validation_report_template.md, extended with the dispatch's required issue-review fields.
- **Claims verified:** 4 source-backed determinations; 2 explicitly UNVERIFIED coverage claims. Posted historical measurements are attributed, not freshly reproduced.

## Verdict and evidence
**verdict: in-progress.** Keep the issue open for the remaining dated follow-up and owner closeout, not for redoing the original investigation or reviving removed commands.

- Issue #354 is OPEN. Both testers have posted final workflow records: William on November 17 ([comment 6956051592](https://github.com/IronbellyOrg/IronClaude/issues/354#issuecomment-6956051592)), Leandro on November 18 ([comment 6990572258](https://github.com/IronbellyOrg/IronClaude/issues/354#issuecomment-6990572258)). The latter explicitly leaves the **December 16, 2026 review/PR repeat due**. No later comment in the complete 80-comment snapshot cancels it or provides the owner's closing summary.
- The November 18 re-run is posted ([comment 6990559105](https://github.com/IronbellyOrg/IronClaude/issues/354#issuecomment-6990559105)); its incomplete evidence and failed regrade are results, not evidence that no work occurred.
- The expanded concurrent-index measurement is now issue #648, with its full result posted November 23 and linked back to #354 ([comment 7105434345](https://github.com/IronbellyOrg/IronClaude/issues/354#issuecomment-7105434345)). It is no longer an unrun measurement.
- The original supporting PR #353 merged as `5e513796b8f2087ef79323dbf928aaa9924508a0`; assignment PR #377 merged as `e2a79d95651e312d730e954fa2e8d9a5ed61b374`. The issue body's claims that #353 is open and its guides are not on master are stale.

## Real current state
1. **Investigation and first follow-up are reported.** William records investigation/reporting for all 16 bug entries and both measurements; their final ledger was accepted by the owner on November 18. Leandro posted the first-pass ledger and the November 18 repeat. These are reporting milestones, not a blanket product PASS.
2. **Latest review measurements remain qualified.** The November 18 result reports 2 of 1,155 tasks at high retry count (0.17%), but one lacks proven blocking cause; a separate historical experimental group remains 3/53 (5.66%) and is not pooled. The ten-finding regrade is FAIL: one blocking, four Medium, five Note; the blocking defect had been caught and fixed in its original loop. Static guard: 65 tests passed in that reported run. No new tests were run for this cleanup review.
3. **PR measurements have explicit missing evidence.** November 18 lists 148 fork URLs, but that fork-only query cannot detect PRs elsewhere. Six known pushes across three PRs were measured earlier; 102 older and 29 new PRs lack push/reversal evidence. A November 18 sentence calls these 'six PRs'; the detailed earlier table establishes **six pushes across three PRs**, not six PRs. Missing logs stay NOT CHECKED under the owner's ruling.
4. **Scope was narrowed.** November 16 rulings parked headless-command work, later put swarm in backlog, dropped the workspace survey and removed guide Step 9. November 18 accepted the measured 3,606-token overhead despite the 2,000-token threshold, with no issue or fix requested. These historical rulings are not new authorizations for this worker.
5. **The code has moved on.** The checkout declares 6.1.0, not 5.0.0. Roadmap, tasklist, sprint and cli-portify packages/registrations are absent. The retained release guides are historical material. Merged PRs #739 and #740 now address swarm resume context and incremental dashboard rows, while related issues remain OPEN. Neither an open issue nor its old reproduction proves the defect persists unchanged.
6. **Concurrent indexing is measured, not yet owner-settled here.** Issue #648 reports all 38 requested builds completed. Every individual build exceeded the earlier 1 GiB budget; ten IronClaude builds had a 38.351 GiB sum of individual peaks, not an instantaneous combined peak. Available memory stayed above the safety threshold on that test workspace. Raw machine captures were not re-inspected in this review.

## Validation Results
| # | Claim | Source | Code Path Checked | Verdict | Notes |
|---|-------|--------|-------------------|---------|-------|
| 1 | The historical runbook still has a dated follow-up | Latest final ledger plus assignment | docs/testing/v5.0.0/impact-validation/leandro.md:44-46 | VERIFIED | December 16 repeat retained; survey subsequently excluded by owner ruling. |
| 2 | Current source can be treated as the 5.0.0 release | Original issue-body setup | pyproject.toml:7; src/superclaude/cli/main.py:557-596 | CONTRADICTED | Checkout is 6.1.0; historical command families removed by #629/#632. |
| 3 | Auto-indexing includes a cross-worktree memory limit | #648 concurrency rationale | src/superclaude/hooks/scripts/codegraph-session-start.sh:11-31 | CONTRADICTED | Per-checkout existence guard and detached launch; no global scheduler or available-memory guard in this hook. |
| 4 | Token/resource measurements have numeric acceptance thresholds | Posted measurements | docs/testing/v5.0.0/impact-validation/william.md:85-86,103-104 | VERIFIED | Token overage was later accepted; memory exceedance remains reported in #648. |
| 5 | All acceptance conditions passed | November 18 results | Historical runtime captures not available in this checkout | UNVERIFIED | Posted results explicitly include FAIL/NOT CHECKED and unresolved blocker attribution; no overall PASS claimed. |
| 6 | All issue timeline events were inspected | Requested cleanup coverage | gh issue view --help JSON field list | UNVERIFIED | Allowed gh view/list interface exposes comments and current relationships, not the full event timeline; see limits. |

## Concrete next steps
1. Keep only the already-required December 16 review/PR repeat in scope, unless the owner explicitly cancels it. Reuse the posted November 18 definitions, preserve separate task populations, count sequential reviews rather than parallel-agent filenames, and keep unavailable push/reversal logs NOT CHECKED.
2. The coordinator/owner can settle the **already-posted** #648 results and determine whether a separate resource-control follow-up is wanted. Do not rerun the 38-build matrix or reopen the accepted token overhead as part of #354 cleanup.
3. After that final dated round, the owner supplies the required short closing summary: confirmed impacts, failed/unknown measurements, accepted exceptions and which child issues remain separate. Then #354 can close without requiring every child product defect to be fixed.
4. No tester product fixes, survey restart, guide rewrite, new issue creation or GitHub changes are authorized by this report. Closed/removed command defects need no resurrected implementation work.

## Complexity, size and priority
- **complexity: medium.** Remaining work is a version-aware measurement repeat and evidence reconciliation, not a new architecture or product implementation.
- **size: M.** Several review/retry/regrade/PR measurements plus final reporting remain; most investigation and both workflow ledgers already exist. This sizes the remaining #354 work, excluding child defect repairs and the completed #648 matrix.
- **priority: P1.** Preserve the owner's latest explicit November 18 'Urgent/highest priority together with #648' instruction as high priority. It gates confidence and owner closeout, not service availability; no evidence supports a P0 incident. The next fixed repeat is December 16, not an immediate license to rerun expensive tests. Mapping the owner's wording onto the requested P-scale is this review's judgment.

## Dependencies
- **Formal GitHub needs/blocks:** blockedBy and blocking each return totalCount 0; no formal dependency edge is recorded.
- **Needs:** no hard prerequisite issue verified. #648 supplies related resource evidence and now has a posted result; it does not prevent the December 16 review/PR repeat. Its owner's acceptance/closure is separate and UNVERIFIED.
- **Blocks:** final #354 impact-assessment closeout and its owner summary in practice. No downstream numbered issue was verified as formally blocked by #354.
- **Does not require:** fixing every child issue, restoring removed pipeline families, completing the dropped survey, or obtaining logs already permitted to remain NOT CHECKED.

## Related issues
Current states below are read from the fork issue listing, not copied from the stale November 17 status comment. Closure alone is not proof of a code repair.

- **#648 OPEN:** expanded concurrent first-index measurements; all requested results posted and linked back November 23.
- **#571 OPEN:** later release/removal umbrella. Its merged removal PRs explain why old pipeline findings are not current features to rebuild.
- **#346 CLOSED:** earlier review-convergence investigation related to the review/retry measurements.
- **Swarm follow-ups OPEN:** #501 (unavailable follow-up command), #540 (completion marker), #555 (detached output), #557 (grouped evidence), #566 (resume context), #567 (raw artifact inventory), #568 (unsupported help flag), #569 (dashboard rows). Some have merged fixes, including #739/#740; do not equate open state with an unchanged defect.
- **Retained reflect/eval follow-ups OPEN:** #556 and split #563/#564/#565 (preview/exit/stub evidence), #560 (wrong coverage prefix), #561 (invalid-selection output directories), #562 (coverage policy question). Their priority/repair scope remains a separate owner decision, not new #354 work.
- **Closed reports from the assignment:** #472/#473 (help examples), #476/#495/#496/#521/#524/#533/#535/#537/#538/#554/#558/#559 (retired pipeline behavior), #505/#506/#510/#536 (help/usage/doctor/memory promise), #542/#543/#544/#545 (launcher and recommend help). This review does not independently revalidate every fix.
- **Earlier context:** #352 (shim-test flakiness), #29 (cleanup-audit crash), #332 (session-memory ignore handling), #404 (tracked performance evidence). They are references from the original runbook, not prerequisites asserted here; their complete histories were not reread.

## Related PRs
Primary PR bodies, states and merge commits were read directly with fork-qualified gh pr view. Incidental PRs in the tester's large measurement window are preserved as metadata in pr-catalog.json; their individual diffs/CI histories were not audited.

| PR | Role | Verified state / merge commit |
|---|---|---|
| #353 | Original post-release guides and install evidence | MERGED; 5e513796b8f2087ef79323dbf928aaa9924508a0 |
| #377 | Two tester assignment documents | MERGED; e2a79d95651e312d730e954fa2e8d9a5ed61b374 |
| #494 | Corrected workspace marker/survey check | MERGED; 0c2b41f8e440b306d4af317ccfaed06820a57179 |
| #475 | Fixed #472/#473 help/example errors | MERGED; a27d798f3da636f4693daf2e4a6b8bfc02a82eb7 |
| #410 | Fixed #404 tracked performance-report mutation | MERGED; 0c4da08f639e9346e382d8e81a68beadebfeb1a3 |
| #629 | Removed cli-portify, not a repair of its retired execution path | MERGED; 956f4964264d5efcfbe741ab3dd090fd97f1acb9 |
| #632 | Removed roadmap/tasklist/sprint packages and CLI registration | MERGED; af5fb69eb9b016287e3560cda50bce2a16123349 |
| #739 | Later resume-context fix, references #566/#557 | MERGED; 3ecf3fee8d7cbf810098ad01807d9c7aa0af8627 |
| #740 | Later dashboard-row fix, references #569/#557 | MERGED; 0dd726d181a15e4cb2c0cf9e4b9fb0ed0f91cfe6 |

Earlier measurement samples: #350 (worktree-specific session listing), #355 (Orca resume), #374 (tier-policy docs) and #402 (CI changes) are MERGED according to pr-catalog.json. The #354 thread establishes measured push data for #350/#355/#377 and no pushes in the supplied #374 log; a mislabeled #402 attachment was actually another #374 log. Those raw logs and their historical patch comparisons are **UNVERIFIED in this review**, not fresh evidence of #402 behavior.

## Verification limits and negative evidence
- **Full event timeline: UNVERIFIED.** Read the issue body, all 80 comments in chronological batches, current state, created/updated/closed fields, closing-PR references and dependency fields. gh issue view --help does not expose timeline events. The brief allows only gh issue view/list and gh pr list/view on GitHub, so no API, GraphQL, browser or upstream workaround was used. Historical label/assignment/reference events and edits outside the comments could change the account; coordinator must obtain that timeline through a separately authorized route if required before acting.
- **Runtime evidence: UNVERIFIED independently.** Posted measurements and reviewer statements are attributed to their comments, not certified anew. No remote machine, private attachment, proxy, model, installer, expensive index build or regression suite was exercised. No product source was modified.
- **PR review depth:** primary related PR bodies and metadata were inspected; the large historical window's incidental PRs received metadata lookup only. Their complete diffs, reviews, CI, and per-PR automatic-push history remain UNVERIFIED. No parent-upstream repository was queried.
- **Scope freshness:** checkout version/removals and hook implementation were read locally. A merged fix PR plus an OPEN child issue is not proof of either current failure or complete repair; relevant behavior tests were not rerun.
- **Negative lookups:** project-local .claude/commands/sc/analyze.md absent, installed copy has Unattended mode and passed the brief guard; guessed src/superclaude/hooks/codegraph-session-start.sh absent, actual source is hooks/scripts/codegraph-session-start.sh; removed CLI-family glob returned no files. Augment main lookup failed BRANCH_NOT_FOUND, master retry succeeded. Codegraph returned fresh with truncated layout/caller lists; source Read/Grep/Glob remained the evidence floor. An initial Edit was freshness-blocked; required Read resolved it without bypassing the edit tool.
- **Artifacts:** analyze/analyze-report.md and analyze/return-contract.yaml record the actual command; analyze/handoff/1-analyze.md records the chain checkpoint. issue-snapshot.json preserves the complete current issue/comments; issue-catalog.json and pr-catalog.json preserve read-only relationship/state context. These are local evidence files, not publications.
- No commit, staging, push, issue edit, label, comment, close, link, or other outward mutation occurred. The coordinator retains any decision/action authority.
