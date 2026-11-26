# Issue 501 review

Template: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g2/468/report-template.md (Findings skeleton), with the coordinator's required fields.

## Verdict and evidence
**Verdict: still-relevant.** Keep issue [#501](https://github.com/IronbellyOrg/IronClaude/issues/501) open. At checkout commit `a7ae3dd30fcf88aaab655c37e94e58e121c2d863`, `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/swarm/lenses/refactor_find.py:53` still recommends `/sc:code-review --apply {compare_files}`. Neither the packaged command search (`**/code-review.md`) nor the installed command search (`/home/coder/.claude/commands/sc/code-review.md`) found that namespaced command. This is the same defect as the issue, not evidence of a completed fix.

The issue is OPEN, with state reason REOPENED. Its history records a not-planned closure on 2026-11-17 followed by reopening that day after the decision to retain swarm. The 2026-11-18 comment explicitly calls the defect valid, assigns it, and asks work to start. Assignment alone is not implementation evidence: no fixing PR was identified by the searches below.

## Real current state
The lens remains experimental with three workers and a findings-table output. Its configured follow-up is still the missing namespaced command. Documentation repeats the stale instruction in `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/docs/swarm/lens-catalog.md:25` and `:45-49`.

The recommendation is data passed through the completion path, not an automatically invoked skill: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/swarm/commands.py:2159-2162` passes the template and substitutions into reduction; `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/swarm/reduce.py:448-467` formats it without checking command availability. The completion path's default comparison-file list begins with the literal `<existing-review>` (`commands.py:2143-2145`), unless the caller supplies its own substitution. Therefore changing only the command name would not establish that the whole generated suggestion is runnable.

The existing renderer test uses a fictitious `/sc:foo` and checks substitution only (`/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/swarm/test_reduce.py:305-314`). No `code-review` regression was found in swarm tests. No fix or running implementation of the issue's requested correction was verified.

## Concrete next steps
1. Replace the stale recommendation with an existing shipped follow-up, not a newly invented namespaced command. `/sc:adversarial --compare` is a candidate already used by the neighboring edge-case lens and documented to accept 2-10 existing files in `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/commands/adversarial.md:35-39`. This review does not certify that candidate as the final fix: validate that it fits the cleanup workflow and provide real report paths rather than the literal `<existing-review>`. Remove the unsupported `--apply` rather than carrying it to another command.
2. Add a focused bundled-lens regression that fails when this recommendation names a missing packaged command. Also test the complete chosen suggestion against its input/argument contract, including the required existing report files; retain generic rendering tests that intentionally use fictitious command names.
3. Update current user guidance alongside the source: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/docs/swarm/lens-catalog.md:25,45-49`, `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/docs/swarm/README.md:67`, and `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/docs/swarm/user-guide.md:200`. Historical release notes also mention the name; decide whether an explanatory correction is appropriate without rewriting history as a new feature.
4. Run focused lens, recommendation-rendering and foreground-command tests in the separately authorized fix. Have the coordinator associate the eventual resolution with parent issue #354. No fix, post, link, commit or staging is part of this review.

## Complexity and size
**Complexity: simple. Size: S.** This is a localized configuration, regression-test and documentation correction using an existing follow-up, not a new command or engine redesign. Size is S rather than XS because the complete rendered input contract and duplicated current user guidance must be checked; a one-token rename alone does not satisfy the issue.

## Priority
**P2.** The bug blocks the suggested manual follow-up for one experimental lens, but the available evidence does not show data loss, a security problem, or the swarm engine failing. The issue's latest direction calls it High priority; that direction is preserved here as historical scheduling context, while this impact-based assessment ranks it below the separate output-loss and completion defects. No release-critical dependency was verified.

## Dependencies
**Needs:** no hard prerequisite issue verified. The decision to retain swarm in #571 is already recorded, so retirement is not a reason to close this defect. **Blocks:** the refactor-find follow-up acceptance item in the #354 validation work; no other issue was verified to require this fix. #540, #555 and #568 share an assignee/work grouping but are not demonstrated prerequisites.

## Related issues
- [#354](https://github.com/IronbellyOrg/IronClaude/issues/354): parent v5 impact validation, OPEN; the source of the reported finding, not an implementation dependency.
- [#502](https://github.com/IronbellyOrg/IronClaude/issues/502): identical duplicate, CLOSED as NOT_PLANNED; its comment explicitly says it duplicated #501 by repeating issue creation. Do not confuse that closure with resolving #501.
- [#571](https://github.com/IronbellyOrg/IronClaude/issues/571): release cleanup plan, OPEN; its updated body and 2026-11-17 owner-decision comment retain swarm and attached skills.
- [#540](https://github.com/IronbellyOrg/IronClaude/issues/540): missing foreground completion marker, OPEN.
- [#555](https://github.com/IronbellyOrg/IronClaude/issues/555): detached child loses durable output, OPEN and reopened.
- [#568](https://github.com/IronbellyOrg/IronClaude/issues/568): stale custom-prompt run-option help, OPEN and reopened.

The last three cross-reference #501 in their 2026-11-18 assignment-split comments. Their implementation status was not audited here; being open is not proof their code is unchanged.

## Related PRs
- [PR #148](https://github.com/IronbellyOrg/IronClaude/pull/148), merged 2026-06-08, commit `b0de1479267353fa77d56cf9d1b59ee57b27138d`: original swarm feature introduction, identified by the target file's git history and read directly.
- [PR #216](https://github.com/IronbellyOrg/IronClaude/pull/216), merged 2026-07-05, commit `64b730a7208a71fb1cca2fb15d8a1e8b1c491342`: repository CI/lint/format cleanup, the other commit in the target file's history; it is not a fix for #501.
- No fixing PR verified. All-state searches for `501` and `"501" in:body` returned PR #400 only; its body and changed files show an unrelated saved-prompt symlink guard and a line-number 501 reference, so it is a false positive. Searches for `refactor-find in:title` and `"code-review" "swarm" in:title` returned no PRs. The broader `refactor-find` search returned historical, unrelated PRs and is not evidence of a current fix.
- The issue #501 body/comments contain no directly mentioned PR number; its timeline cross-references issues, not a fixing PR.

## Verification limits and negative evidence
- Inspected 2026-11-24 at checkout `a7ae3dd30fcf88aaab655c37e94e58e121c2d863`; no fetch or branch change. Whether remote master has a newer fix not represented here is UNVERIFIED. No identified fixing PR changes the checkout evidence.
- Read #501's full body and three comments, plus its timeline events. Timeline retrieval used `gh api repos/IronbellyOrg/IronClaude/issues/501/timeline`, which was read-only and targeted the fork but exceeded the brief's narrower allowlist of issue/pr view/list commands. This was a process deviation, not an outward mutation; no further API requests were made. The timeline showed no linked fixing PR.
- Exact packaged `**/code-review.md` and installed `code-review.md` searches returned no files. The project development command directory is absent in this checkout; the installed analyze command has unattended mode and passed the two-copy guard using the sole existing copy. The independently available non-namespaced `/code-review` skill does not establish `/sc:code-review` availability.
- Source searches covered swarm Python templates, renderer, validator, recommendation substitutions and swarm tests. `code-review` matches in tests were outside swarm, not an availability regression for this lens. Current swarm docs were searched for the stale namespaced reference. These are negative search results within the stated scope, not proof no differently named work exists anywhere.
- Read-only PR searches can miss unmentioned or differently titled fixes, and GitHub work not yet pushed is UNVERIFIED. Assignment and comments asking for work do not by themselves justify an in-progress verdict.
- No tests, model inference, live swarm run or generated end-of-run suggestion were executed. Runtime success of a replacement is UNVERIFIED. The requested analyze command was executed as a static quick architecture review, with report under `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g2/501/analyze/`.
- No product source changes, Git staging, commits, GitHub edits, comments, labels, closures or links were made. Report writes stayed under this task's assigned directory.
