## Verdict
**still-relevant**. Issue [#561](https://github.com/IronbellyOrg/IronClaude/issues/561) remains OPEN and its defect is still present in checkout `a7ae3dd30fcf88aaab655c37e94e58e121c2d863` (reviewed 2026-11-24). `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/eval/commands.py:1753` creates the run directory and `:1780` creates its `homes` child before missing-suite rejection at `:1785-1789` and unknown-eval rejection at `:1798-1810`. Both exits leave already-created directories; no cleanup is present in those branches. Existing acceptance checks at `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/cli/eval/test_eval_run.py:384-425` check exit and diagnostic, not absence of directories.

This is not permission to implement. The latest issue comment, [2026-11-18](https://github.com/IronbellyOrg/IronClaude/issues/561#issuecomment-6989290376), explicitly keeps the unused headless eval harness on Backlog, open and unassigned, with nobody working on it until it is used again. The earlier [2026-11-16 hold](https://github.com/IronbellyOrg/IronClaude/issues/561#issuecomment-6921979622) and [2026-11-17 review](https://github.com/IronbellyOrg/IronClaude/issues/561#issuecomment-6941353225) agree. Static triage only was performed under this brief; no fix or eval was run.

The issue's frozen-runtime observations are historical reports, not a new reproduction: retained probe files and frozen revisions were not independently replayed (UNVERIFIED). Current control-flow ordering is verified directly. Source history includes merged PR #75 (`0365a055f93e5703d9251873c8422d86e47911b3`) and subsequent formatting PR #108 (`59ef614e6`); neither removes the ordering now visible.

## Complexity and size
**Complexity: simple. Size: S.** One command function owns both validation and directory allocation; the bounded fix is to postpone allocation until selection validation succeeds, with regression assertions for both invalid inputs and preservation of valid-run and scratch-root behavior.

## Priority
**P3.** Low-impact scratch-folder litter in an unused harness, with no verified downstream blocker; the latest owner-directed issue comment explicitly says lowest priority and backlog.

## Concrete next steps
No implementation while the backlog hold remains. Keep the issue open and unassigned; this review makes no GitHub changes.

After the owner explicitly lifts that hold:
1. Reject an unresolved suite or unknown selected eval ID before creating the per-run directory or homes child, in `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/eval/commands.py`. Prefer postponing allocation, not deleting output after failure.
2. Extend the existing two rejection tests in `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/cli/eval/test_eval_run.py:384-425` to assert no new per-run directories, still exiting 2 with the correct diagnostics.
3. Verify valid selections still create the expected run artifacts and preserve scratch allowlist validation, runtime allowlist extension before writes, containment checks, and the separate coverage gate. The current allowlist check is at `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/eval/config.py:238-248`; coverage rejection follows selection validation at `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/eval/commands.py:1822-1829`. Test execution is deferred, not reported as passed.

## Dependencies
**Needs:** the owner's lift of the explicit backlog hold; this is an authorization gate, not another implementation issue. No prerequisite issue number is established in the live #561 body/comments or the related records checked.

**Blocks:** no downstream issue is verified as blocked by #561. Parent #354 tracks release follow-up and contains the filing instruction; the reviewed records establish a relationship, not that the whole parent can be completed merely by fixing #561. Siblings #560 and #562 are independent, not prerequisites.

## Related issues
- [#354](https://github.com/IronbellyOrg/IronClaude/issues/354), parent release-validation follow-up. Its [linked owner comment](https://github.com/IronbellyOrg/IronClaude/issues/354#issuecomment-6663807076), read live, explicitly says to file the leftover run folder separately from the refusal-policy question and wrong command prefix.
- [#560](https://github.com/IronbellyOrg/IronClaude/issues/560), OPEN, coverage failures show the wrong command label. Its body was read live; it is a separate diagnostic defect, not this allocation-order defect.
- [#562](https://github.com/IronbellyOrg/IronClaude/issues/562), OPEN, asks whether installed-hook coverage should reject unrelated suites. Its body was read live; coverage rejection is not established as defective by this review. Do not disable the coverage gate to fix #561.

## Related PRs
No PR is directly mentioned or linked in the #561 body or its three comments. A live search for `"#561" in:body` across all PR states returned no results; broader searches for `561` and defect terms produced unrelated matches. Exhaustive absence of a fix PR is UNVERIFIED, but the inspected local source is not fixed.

Historical context, not fixes for #561:
- [PR #75](https://github.com/IronbellyOrg/IronClaude/pull/75), MERGED, cliEval command and allowlist-ordering remediation, merge `0365a055f93e5703d9251873c8422d86e47911b3`. Its body and metadata were read live; it is in local commands.py history.
- [PR #68](https://github.com/IronbellyOrg/IronClaude/pull/68), MERGED, earlier eval-run and scratch-root correction, merge `dce3c3cb5b689cf47755f2f4f08c1b688a7054d7`. Its metadata was read live and it is in local commands.py history; its full implementation delta was not reviewed (UNVERIFIED).
