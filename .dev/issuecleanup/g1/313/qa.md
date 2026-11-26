# Research: Independent review of issue 313 report drafts

- **Topic type:** Independent report accuracy and completeness review
- **Scope:** Two report drafts, current named test dependencies, relevant deletion history and permitted GitHub records
- **Status:** Complete, independent static review
- **Date:** 2026-11-23
- **Template:** /home/coder/.claude/templates/modularization-template-review/codebase-research_template.md

---

## Findings

### Review verdict

[CODE-VERIFIED] **PASS.** Zero blocking findings and one minor historical-count wording error. The still-relevant verdict follows from current source, not the issue author's historical experiment: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/cli/reflect/test_grader_yaml_root.py:22-36 still imports a committed working-record file, and /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/recommend/test_routing_refresh.py:631-704 still reads planning records.

### Scope checked

[CODE-VERIFIED] Read both drafts completely, in requests of at most 80 lines: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g1/313/findings.md:1-76 and /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g1/313/analyze/analyze-report.md:1-47. Independently inspected current dependency definitions and consumers in all four surviving named test modules, relevant shared configuration and the hidden-input guard; checked exact tracked inputs, checkout revision and deletion history. GitHub checks used only issue/pr view/list with the explicit fork repository.

[CODE-VERIFIED] The five reflect dependencies are supported: one grader test executes `_load_grader`, and four parity tests consume the case files. The fifth parity test only compares constant tool sets. Evidence: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/cli/reflect/test_grader_yaml_root.py:22-36 and /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/cli/reflect/test_reviewer_finding_parity.py:25-98. Exact grader, YAML and patch paths were independently confirmed tracked with git ls-files.

[CODE-VERIFIED] The two recommend dependencies are supported: `_spec_path` locates a historical package, T75 reads its specification and inventory, and T76 reads its analyst reports and requires recorded dispositions. Evidence: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/recommend/test_routing_refresh.py:142-145,631-704. The specification and inventory paths were independently confirmed tracked. T75 also checks live command membership at lines 661-662, so preserving current behavior checks, as both drafts require, matters when removing historical assertions.

[CODE-VERIFIED] Four audit dependencies are supported: two directory-name tests share an enumeration fixture over the checkout's task folders, a separate test requires the root to exist, and the composite repeats the enumeration. Evidence: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/audit/test_invariant_preservation_NFR_6_through_10.py:163-166,268-309,444-459. The composite must not be missed during remediation.

### Blocking findings

[CODE-VERIFIED] **None.** The requested decision and fix boundary are supported by the direct imports, reads and directory enumeration above. The drafts explicitly limit the 11-test count to surviving issue-named files and do not present it as an executed failure count or a whole-suite inventory. Evidence: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g1/313/findings.md:20-38,64-69 and /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g1/313/analyze/analyze-report.md:32-43.

### Minor findings

[CODE-CONTRADICTED] **M1: "nine-test eval companion" confuses implicated historical tests with the module's total tests.** This wording appears at /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g1/313/findings.md:56 and /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g1/313/analyze/analyze-report.md:34. Local git source at parent a3edd84db5f4dfe8351b49ddd769f0e7ebe08ee6^ contains 64 top-level test functions in /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/cli/eval/test_workflow_vs_task_builder_companion.py (historical file, now deleted); git grep located definitions from lines 207 through 2192 and counted 64. Nine is the issue's old affected-test count, not the size of the deleted module. Consequence: readers could incorrectly report how much total coverage PR #656 removed. Replace with "deleted the eval companion that contained the nine dependencies listed in the original issue." Nonblocking: the module really is deleted, so this wording does not change the surviving 11 dependencies or the still-relevant decision. The historical nine failures themselves remain UNVERIFIED by this static review.

### Requested-field coverage

[CODE-VERIFIED] The combined deliverable includes the verdict, present source-backed dependency state, concrete next steps, complexity plus size plus priority with reasons, recorded dependencies and related issues/PRs. Evidence: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g1/313/findings.md:13-62. Medium complexity, M size and P2 are explicitly assessments rather than invented GitHub field values. The coordinated four-module cleanup and a temporary-input-aware guard make those assessments reasonable; no verified outage justifies overriding P2.

[CODE-VERIFIED] Independently read issue #313's body, one returned comment, open state, empty dependency/parent/sub-issue records and empty closing-PR list. Independently verified all eight listed PRs are merged with the stated commit IDs. PR #656's body explicitly names #647 and #571 and its file list records the companion deletion; local git deletion history identifies the same commit. These checks support the bounded related-work statements in /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g1/313/findings.md:44-62, without requiring a full event timeline.

[CODE-VERIFIED] The guard statement is appropriately bounded negative evidence, not an exhaustive absence claim. Independent phrase searches found no matching prevention guard; the existing hidden-input guard documents a different invariant. Evidence: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/audit/test_hidden_input_guard.py:1-38 and the qualifications at /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g1/313/findings.md:66-69. The open-PR search returned no matches, which supports only "no targeted fix verified," not a categorical claim that nobody is working on it.

## Gaps

- [UNVERIFIED] Complete issue event timeline. The permitted issue view/list surface supplied the body, comment, state, dates and dependency/closing-PR fields, not all timeline events. This limitation is already disclosed in the drafts. No decision-changing unsupported timeline claim remains: the still-relevant verdict rests on current source, the comment-before-deletion ordering is confirmed by returned dates, and absence of active work is expressly qualified as unverified rather than asserted absolutely.
- [UNVERIFIED] Original historical experiment, historical nine affected eval tests, current pass/fail counts and current CI health. No tests were run, as expected for this quick static review. The 11 count is a static count of direct current dependencies, not a reproduced failure count.
- [UNVERIFIED] Exhaustive suite-wide dependency/guard absence and all unlinked work. Searches were bounded; neither a complete guard absence proof nor an exhaustive inventory of later dependencies was attempted. The initial broad tracked-path query produced excessive output; the exact input paths were then checked in a separate bounded query, not inferred from that truncated output.
- [UNVERIFIED] The original drafts' Codegraph session statistics and tool-recovery narrative were not independently reproduced. Neither affects the decision because dependency evidence was checked directly.
- [UNVERIFIED] Acceptance criteria and complete issue histories for #647 and #571 were not reviewed. Their contextual relationship is explicit in PR #656; no prerequisite claim depends on their current state.
- Review boundaries: only this review file was written. No source/draft modifications, test execution, staging, commit, Orca calls, GitHub API/browser access or GitHub writes were performed.

## Key Takeaways

[CODE-VERIFIED] **PASS with one minor wording correction recommended.** Keep the still-relevant verdict and the proposed four-module cleanup plus prevention guard. Five reflect, four audit and two recommend dependencies are independently supported by the source cited above. M1 concerns the deleted module's total size, not the current scope, priority or closing decision.

[UNVERIFIED] Execution outcomes and the full issue timeline remain unknown. They do not justify closing the issue while direct current dependencies remain.
