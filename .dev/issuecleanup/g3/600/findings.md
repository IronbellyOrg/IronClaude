## Verdict

close: the requested documentation correction is already present in this checkout, although [issue 600](https://github.com/IronbellyOrg/IronClaude/issues/600) is still OPEN. The live issue has no comments. Reviewed on 2026-11-24 at checkout HEAD `a7ae3dd30`.

- The guide now says “Accepted remediation offers use design then workflow/implement, at every depth” at `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/core/HOW-WE-WORK.md:195`. The Auggie-only routing row at line 342 says “an accepted offer uses workflow at every depth.” Neither site retains the issue's task-builder/task or MDTM selection claim.
- The plugin guide is byte-identical: read its corresponding paragraph at `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md:195` and compared both whole files with `cmp` (exit 0).
- The regression assertions were updated too: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/core/test_how_we_work_routing_table.py:799-806` asserts workflow at every depth. The separate offer-suppression advice does not select a different executor. Its assertion requiring the design-referral warning is stale: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/commands/design.md:23-26` now declares `--output <file>`, matching Phase A. This separate warning is not an unmet retired-executor acceptance criterion and should not be retained as an accurate safety claim.
- The real primitive agrees: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-auggie-review-protocol/refs/remediation-handoff.md:7` explicitly includes deep in the common chain; `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-auggie-review-protocol/SKILL.md:345-351` reserves implementation for the user's explicit sign-off. `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/commands/test_auggie_review_remediation_chain.py:117-129` still contains the removed-route regression guard.
- Checked the optional fixture: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/recommend/fixtures/routing_refresh_cases.json:114-130` references the right row, preserves local-only deep review and does not pin the stale MDTM wording. No issue-600 fixture edit is needed.
- Local `git log -S 'Accepted remediation offers use design then workflow/implement'` identifies commit `a3edd84db5f4dfe8351b49ddd769f0e7ebe08ee6`, the merge of PR 656, as introducing the corrected paragraph. Live PR 656 is MERGED, with that merge commit, and includes the guide, mirror, routing test and fixture. The earlier primitive work was PR 296 for issue 263; PR 300 added the regression guard.

Static acceptance state is satisfied. Fresh pytest results and a whole-project `make verify-sync` result are UNVERIFIED: execution and environment creation were prohibited, so neither was run. The report does not reinterpret historical PR test claims as tests run here. Only reports were written; no source, issue or PR was changed.

## Complexity and size

complexity simple; size XS: no new implementation remains for issue 600; only the coordinator's owner-approved issue disposition remains.

## Priority

P3: the misleading route has already been corrected, so the remaining open issue is administrative cleanup and blocks no verified implementation work.

## Concrete next steps

No implementation follow-up for this issue. After the owner's go, the coordinator can close issue 600 as already addressed by PR 656, citing the current guide and updated regression assertions; this worker has not closed or commented on it. Do not create a replacement issue for the already-completed retired-executor correction or reintroduce task-builder/task. Separately record the obsolete design-output warning and the tests that require it for documentation cleanup: the design command already supports the option, so no primitive repair is needed. That follow-up is outside issue 600's declared scope, is not a closure dependency, and no new issue or source change was made here.

If the coordinator needs fresh runnable acceptance evidence before closing, it must arrange the routing-table and remediation-chain tests and whole-project synchronization check in an authorized environment; all are UNVERIFIED here, not claimed passing.

## Dependencies

No unresolved prerequisite or issue blocked by issue 600 was verified. Issue 263 (the primitive replacement) is CLOSED and its merged PR 296 already supplied the common chain. Issue 571 is a proposed parent in issue 600's prose, not a verified formal parent or a closure prerequisite. Issues 599 and 572 are related work, not required dependencies. Formal GitHub parent/sub-issue edges are UNVERIFIED under this task's restricted read commands.

## Related issues

- [263](https://github.com/IronbellyOrg/IronClaude/issues/263), CLOSED: replaced the Auggie review remediation chain with workflow/implement; read its body and comments (none).
- [599](https://github.com/IronbellyOrg/IronClaude/issues/599), OPEN: the separately scoped reflection deep-remediation route issue. Verified title and state only; whether it too should close is UNVERIFIED and not decided here.
- [571](https://github.com/IronbellyOrg/IronClaude/issues/571), OPEN: the release-removal program, named as proposed parent in issue 600. Verified title and state only; its completion is UNVERIFIED.
- [572](https://github.com/IronbellyOrg/IronClaude/issues/572), OPEN: evaluation of rf-* and other agents, explicitly outside issue 600. Verified title and state only.
- The issue also mentions a troubleshoot sibling without a number. Its exact issue number is UNVERIFIED; no dependency is inferred from that mention.

## Related PRs

- [656](https://github.com/IronbellyOrg/IronClaude/pull/656), MERGED 2026-11-18, merge commit `a3edd84db5f4dfe8351b49ddd769f0e7ebe08ee6`: removed the retired task route and corrected the guide and its mirror, plus routing tests and fixtures. The corrected paragraph's provenance is verified by local history, not just the PR description.
- [296](https://github.com/IronbellyOrg/IronClaude/pull/296), MERGED 2026-10-25, merge commit `401cdf8ed3872e1fbe30216064d634f96b83a7b9`: closes issue 263 and refactors the primitive to one chain for every depth. Its body explicitly left HOW-WE-WORK out of scope then.
- [300](https://github.com/IronbellyOrg/IronClaude/pull/300), MERGED 2026-10-25, merge commit `d3d545dfba976da945b5f37cc021cbe874f5196b`: fixes legacy resume behavior and adds the single-chain regression test.

Read live bodies and merge metadata for all three PRs. The initial number-based PR searches returned unrelated numeric matches and do not prove an issue-600 link; PRs above were found through source history and title search. No formal closing cross-reference from PR 656 to issue 600 is asserted. A first legacy-route grep failed because lookbehind is unsupported; retry with a supported boundary expression returned no matches in the protocol directory, not a passing pytest result.

