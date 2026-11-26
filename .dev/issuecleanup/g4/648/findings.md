## Verdict

**close**. Reviewed 2026-11-24; issue #648 is still OPEN, but its measurement-only deliverable is complete in the live discussion. This recommends closure by the owner/coordinator, not a GitHub action by this worker and not a declaration that indexing meets a memory budget.

The report posted November 23 at https://github.com/IronbellyOrg/IronClaude/issues/648#issuecomment-7105420783 supplies the requested N=1,3,5,10 matrix for both LDToolkit and IronClaude: eight batches, 38 per-build peak-memory and elapsed-time rows, sums of individual peaks, minimum available memory, observed total-memory ranges and reported exit/completion states. It states 0.5-second sampling (largest reported gap 0.524 seconds), reports no killed/failed/stopped builds, and reports slowdown using measured durations. The parent link required by acceptance criterion 4 is present at https://github.com/IronbellyOrg/IronClaude/issues/354#issuecomment-7105434345. The issue explicitly requires no product-code changes, and none is needed to complete this measurement task.

Current source still permits concurrent first indexing: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/hooks/scripts/codegraph-session-start.sh:11-31 checks the off switch, binary, repository and database existence, then launches a detached init without a workspace-wide concurrency or memory guard. The hook last changed in commit `2f10a0e1e43bee841a4143235a92fc16171c9707` (merged PR #329), according to path-scoped git history. /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/docs/user-guide/codegraph.md:28 still states up to about 1 GB during first init, whereas the posted experiment reports IronClaude per-build peaks of 3,744,572-4,172,508 KiB. Those are possible separate follow-ups, not unfinished acceptance criteria for #648.

UNVERIFIED: raw benchmark logs, measuring-script correctness, the reported nine regression checks, the report's prior independent QA and present-version memory use were not independently reproduced. The published report tested IronClaude commit `1a6c8723fe9e6caa85bfffcdb97b2dc434978bf9` and LDToolkit commit `2c074679857f327a2b3bb153c597414710badcb4`, not this checkout. User-perceived machine slowness is explicitly untested; observed slowdown is supplied through timing instead. Summed individual peaks are not simultaneous aggregate memory. The completion verdict rests on the required posted measurements and backlink, not on a new safety/performance certification.

## Complexity and size

**medium; M.** The full issue is a bounded but nontrivial 38-build experiment with synchronized starts, per-process resource measurement, frequent workspace-memory sampling and safety stops across two repositories; that work is already reported complete, leaving only owner/coordinator closeout rather than implementation.

## Priority

**P1.** Concurrent first-index builds can place substantial memory pressure on one workspace, and the owner's November 18 priority comment explicitly ranks #648 jointly highest with parent #354; the posted results remove the measurement gap, so preserving that recorded priority does not imply an urgent rerun or an open product-fix requirement.

## Concrete next steps

No unfinished in-scope measurement or product implementation step is established. The coordinator can present the posted result and this close recommendation to the owner, then settle #648 only after the owner's go. Do not rerun the matrix, add locking/throttling, revise the memory documentation or open a follow-up issue under this assignment. Any resource-control or documentation follow-up needs its own scope and authorization.

## Dependencies

- **Needs:** no prerequisite issue is established by #648's body or comments. #354 supplies the prior single-build method and historical budget; it does not need to close first.
- **Supplies evidence to:** #354, the v5.0.0 impact-validation parent; the required backlink is already present. No claim is made that closing #648 closes all of #354.
- **UNVERIFIED:** formal GitHub blocked-by/blocking relationships and the full event timeline. The allowed issue/pr view/list calls were used for text and states only; no dedicated dependency endpoint or timeline API was called.

## Related issues

- **#354 OPEN:** v5.0.0 impact-validation parent, the source of the single-build method and recipient of the completed concurrent-build report. Its direct November 23 backlink verifies the posting requirement independently of later backlog-review commentary.
- **#323 CLOSED:** replacement of codebase-memory/Serena with CodeGraph, identified by the merged hook-origin PR #329; a historical implementation relationship, not a prerequisite to reopen. State/title were checked with the fork-qualified issue listing; its full discussion was not reread.
- Broad `codegraph memory` issue search returned unrelated workflow and release issues too. No additional load-bearing dependency is inferred from keyword matches.

## Related PRs

- **#329 MERGED**, `feat: replace codebase-memory and Serena with codegraph (#323)`, merge commit `2f10a0e1e43bee841a4143235a92fc16171c9707`: introduces the per-checkout SessionStart indexing architecture. Its body/state/merge commit were read live; path-scoped git history ties it to the current hook.
- No PR is mentioned or linked in #648's body/comments. The fork-qualified all-state PR search for `648` returned **#634 MERGED**, release preparation for 6.0.0, commit `741a0e1302412deb1ef02515ebc273eb0a471cf5`. Direct PR inspection found no #648 measurement relationship in its body or matching comments, so it is excluded as completion evidence (a search hit is not a relationship).
- No direct measurement-completion PR was verified or required: #648 expressly asks for a report comment and no product-code change. Full PR diffs, review histories, CI results and hidden cross-reference events are UNVERIFIED.

Evidence files: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g4/648/issue-648.json and /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g4/648/parent-link.json. Static command report: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g4/648/analyze/analyze-report.md. No source, index, dependency, benchmark environment, issue or PR was intentionally changed; only this task's report directory was written.
