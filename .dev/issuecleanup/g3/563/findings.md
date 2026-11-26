## Verdict
**still-relevant.** Issue [#563](https://github.com/IronbellyOrg/IronClaude/issues/563), the reflection wrapper's inaccurate command preview, is OPEN and the mismatch remains in checkout `a7ae3dd30fcf88aaab655c37e94e58e121c2d863` (2026-11-24). This is not a fix to the interactive `/sc:reflect` skill.

- `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/reflect/runner.py:452-481` builds a `/sc:reflect --mode post` prompt. The preview prints it and returns without launching at the same file's lines 637-662.
- Actual standard/deep production execution takes the ensemble route, not that prompt (`/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/reflect/runner.py:535-548`). The ensemble invokes its scorer when there are at least two successful reviewer outputs and no supplied score (`/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/reflect/ensemble.py:423-435`). That scorer constructs and launches a process at lines 535-554, using the `/sc:adversarial` prompt at lines 582-598. Reviewer prompts are separately built from the review lens at lines 601-616, so blindly replacing every prompt would be wrong.
- The November 16 and November 18 issue comments explicitly keep this wrapper work in backlog, open and unassigned until it is used again. No later comment on #563 lifts that hold. The November 17 conclusion remains correct, but its claim of no recent file changes is historical: PR #653 merged as `2ca022bf7dd8200febd1106232a96b1cbbd5c5f2` on November 18 and changed remediation routing, not this preview mismatch.
- The issue records model-free reproductions on `5e513796b8f2087ef79323dbf928aaa9924508a0` and `d4d1662a85850cc25ab8546b79e14ce1d9d4dc76`. Those historical executions and their local captures were not rerun or independently reopened here: UNVERIFIED as new runtime evidence. This review establishes the current defect by source inspection only.

The requested quick architecture analysis is `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g3/563/analyze/analyze-report.md`. No implementation, dependency installation, model session or GitHub mutation was performed.

## Complexity and size
**complexity medium; size M.** A bounded wrapper change must describe both ensemble reviewers and the conditional scorer without launching, preserve distinct prompt roles, and add a model-free production-dispatch regression rather than just changing one printed string.

## Priority
**P3.** The preview misleads operators about an unused wrapper but no verified active workflow is blocked; the November 18 issue comment explicitly says lowest priority, backlog, and no work until that wrapper is used again.

## Concrete next steps
No fix starts while the owner hold remains. This is not an in-progress fix; the existing preview no-launch branch is only one satisfied acceptance condition, not resolution of the issue.

After the owner explicitly reopens wrapper work:
1. Make the preview describe the actual ensemble execution plan, preserving separate reviewer briefs and scorer prompts, and show scorer execution as conditional. Use clearly marked symbolic reviewer output paths where exact future paths depend on execution. Do not launch reviewers or a scorer to discover preview values.
2. Add the issue's requested model-free regression comparing preview intent with captured process stdin and argv at the real ensemble dispatch boundary. Keep the runner's production class identity intact when intercepting lower-level process launch, since replacing it selects the legacy route. Update preview tests and the guide to match; keep the no-launch guarantee.
3. Reassess closure only after that check passes. Do not silently fold the separate credential-exit or stub-cost defects into this change.

## Dependencies
No numbered implementation prerequisite or hard blocker of another issue is established by #563. Owner permission to resume headless-wrapper work is the gating prerequisite, not a technical dependency. Issue #556 is the umbrella evidence record and should not be considered fully resolved while #563 remains open. Issue #565 shares the scorer boundary, so coordinate preview semantics with any future stub-mode contract change, but it is not a demonstrated prerequisite.

## Related issues
- [#556](https://github.com/IronbellyOrg/IronClaude/issues/556): OPEN umbrella tracking three reflection-wrapper defects; live body and comments read, including the November 24 backlog review.
- [#564](https://github.com/IronbellyOrg/IronClaude/issues/564): OPEN sibling for missing credentials returning exit 1 instead of blocked exit 2; distinct from the preview defect. Current number/title/state verified, not re-investigated.
- [#565](https://github.com/IronbellyOrg/IronClaude/issues/565): OPEN sibling for stub reviewers still dispatching a scorer despite credit-free guidance; distinct from the preview defect. Current number/title/state verified, not re-investigated.
- [#354](https://github.com/IronbellyOrg/IronClaude/issues/354): original release-validation assignment. Its reflection-specific diagnostic comment was read and agrees that this was a model-free stand-in process capture, not model inference. UNVERIFIED: the full large assignment discussion and all its unrelated work were not reviewed.
- [#571](https://github.com/IronbellyOrg/IronClaude/issues/571): cleanup plan referenced by the umbrella and PR #653. UNVERIFIED: its live body/current disposition was not read in this focused review.

## Related PRs
No closing PR is named in #563's body or comments. An all-state PR search for `"563" in:title,body` returned no matches. Broader `563` and `reflect preview` searches returned merged PRs #622 and #626 respectively, whose titles concern command removal/help text rather than this fix; they are not evidence of closure. UNVERIFIED: the full GitHub event timeline and exhaustive PR linkage, which the allowed view/list reads do not establish.

- [#653](https://github.com/IronbellyOrg/IronClaude/pull/653): MERGED November 18, commit `2ca022bf7dd8200febd1106232a96b1cbbd5c5f2`. Its body and changed-file list describe remediation-route changes including the runner; current source still contains the preview defect. Do not repeat the old November 17 claim that these files have not changed since November 12.
- [#581](https://github.com/IronbellyOrg/IronClaude/pull/581): MERGED, commit `fc4b2240225080cbfc5e7bbc1a1f4f71cd24084d`, mentioned by the umbrella's older review. Live title/body identify safety-scan and implement follow-up work, not a preview fix. Its returned changed-file list has no reflection-wrapper or reflection-skill source path, so the old umbrella claim that it edited two reflection-skill text files is not supported by that list. GitHub returns only a bounded file listing, so exhaustive absence across all files is UNVERIFIED.

No tests, wrapper run, installed-console check or real model session was performed. Review confidence rests on current source and live issue comments, not on claims that a repaired product has been tested.
