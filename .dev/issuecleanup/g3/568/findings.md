## Verdict
**still-relevant.** Reviewed 2026-11-24 at `a7ae3dd30fcf88aaab655c37e94e58e121c2d863`. Issue #568 is OPEN, and both misleading help strings remain: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/swarm/commands.py:435-439` (validate-lenses) and `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/swarm/commands.py:3902-3909` (scaffold). They describe `--custom-prompt-dir` as though it were an available run option. The complete run decorator block at that same absolute source path, lines 1368-1557, does not define it; the reusable decorator at lines 158-170 adds only `--auto-inject-guard`. These are the registered command implementations, not dead examples.

The supported configuration is the job-specification field `custom_prompt_dir` with `lens` set to `custom`, not a new command-line option. The static preflight chain reads that field and applies it before schema validation. This review does not establish that every custom-prompt mechanism works; runtime rendering, exit-2 rejection and tests on this checkout are UNVERIFIED because no application or test process was run.

The live issue's November 17 reopening explicitly reverses the retirement-based not-planned closure, and its November 18 comments say to fix it and reassign the work. Assignment and an instruction to start are not evidence that implementation began. No repair PR was identified by the scoped PR searches. Merged PR #739 (`3ecf3fee8d7cbf810098ad01807d9c7aa0af8627`) repairs related resume context, and merged PR #740 (`0dd726d181a15e4cb2c0cf9e4b9fb0ed0f91cfe6`) repairs related dashboard retention; neither closes this help defect, whose strings are still present after both merges. Original historical runtime captures referenced by the issue were not opened: UNVERIFIED.

Analysis: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g3/568/analyze/analyze-report.md`. Live issue snapshot: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g3/568/issue-568.json`.

## Complexity and size
**complexity simple; size XS.** Two help strings in one implementation file plus focused assertions in existing command tests; no parser feature, job-model change, migration or execution redesign is needed. This sizes the remaining fix, not the wider swarm subsystem.

## Priority
**P2.** Wrong help blocks the advertised invocation and wastes operator time, but the existing job-file route avoids the nonexistent option and this issue does not demonstrate data loss, a security failure or a release-critical dependency. This is an impact-based review recommendation, not a GitHub priority change: the November 18 comment explicitly records High priority, which remains the last stated owner-side scheduling direction.

## Concrete next steps
1. Replace the two public help mentions of `--custom-prompt-dir` with guidance to set job fields `lens` to `custom` and `custom_prompt_dir` to the prompt directory, supplied through a spec file or standard input. Keep the current parser and job semantics. Supporting implementation: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/swarm/preflight.py:1594-1619` and `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/swarm/preflight.py:1704-1709`.
2. Extend help coverage at `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/swarm/test_scaffold_cmd.py:63-69` and `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/swarm/test_validate_lenses_cmd.py:145-152` to require the actual field spelling and disallow the unsupported flag spelling; those checks currently only assert unrelated option names. Add a narrow parser rejection regression in `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/swarm/test_commands_run.py`, stopping at argument parsing rather than dispatching any workers.
3. In a separately authorized implementation run, execute the focused help/parser tests and existing custom-prompt tests. Confirm that help and accepted configuration agree without introducing a new option merely to match stale text. No fix, test run, commit, issue edit or PR action is authorized or performed in this review.

## Dependencies
**Needs:** no hard prerequisite issue was identified for the wording/test correction. The swarm-retention decision in #571 is already recorded in its updated body and the #568 reopening comment, so retirement is not a blocker.

**Blocks:** the help-guidance acceptance item in aggregate tracking issue #557. It does not block independent resume/raw-output/dashboard repairs (#566, #567 and #569). Those are related defects, not prerequisites for correcting these two strings. No broader release dependency was verified.

## Related issues
- [#557](https://github.com/IronbellyOrg/IronClaude/issues/557): original aggregate report, including this exact help/parser mismatch; live body read, still OPEN.
- [#354](https://github.com/IronbellyOrg/IronClaude/issues/354): original testing and measurement assignment; title/state verified OPEN. This review did not reopen its testing scope.
- [#571](https://github.com/IronbellyOrg/IronClaude/issues/571): release/removal plan; its updated body explicitly keeps swarm despite the older title.
- [#566](https://github.com/IronbellyOrg/IronClaude/issues/566), [#567](https://github.com/IronbellyOrg/IronClaude/issues/567), [#569](https://github.com/IronbellyOrg/IronClaude/issues/569): sibling resume-context, raw-artifact and dashboard findings as described in #568's assignment comment and #557. Their individual current issue states are UNVERIFIED here.
- [#501](https://github.com/IronbellyOrg/IronClaude/issues/501), [#540](https://github.com/IronbellyOrg/IronClaude/issues/540), [#555](https://github.com/IronbellyOrg/IronClaude/issues/555): other work in the same November 18 assignment split, concerning a missing recommended command, foreground completion marker and detached output. Their individual bodies/states are UNVERIFIED; the assignment grouping is not a dependency.

## Related PRs
No PR is explicitly linked in #568's body or its four live comments, and no #568 help-fix PR was identified by `gh pr list` searches for `568`, `"custom-prompt-dir"`, and `swarm help in:title,body` across all PR states. Search absence is not proof that no unlinked work exists; such work is UNVERIFIED.

- [#739](https://github.com/IronbellyOrg/IronClaude/pull/739), **MERGED**, `3ecf3fee8d7cbf810098ad01807d9c7aa0af8627`: accepted resume-context fix, references #566 and #557. Live body/file list read; touches the command file, but both #568 help strings remain. Local path-scoped history includes this merge.
- [#740](https://github.com/IronbellyOrg/IronClaude/pull/740), **MERGED**, `0dd726d181a15e4cb2c0cf9e4b9fb0ed0f91cfe6`: dashboard incremental-poll fix, references #569 and #557. Live body/file list read; its two changed files are the dashboard implementation and its test, not this issue's help text.

Numeric search also returned #622 (removal of the build command), whose body was inspected and does not fix #568. Broader help searches returned unrelated release/removal PRs; they are not treated as resolution evidence. The custom-option search returned #178 (historical swarm migration); only its list metadata was read, so its detailed relationship to the original wording is UNVERIFIED and not used to decide this issue.
