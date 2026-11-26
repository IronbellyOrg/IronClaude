## Verdict
still-relevant. The label defect is present, but implementation must remain on backlog under the existing hold. DRAFT, NOT ACCEPTED: the required independent review did not produce a report after two Agent attempts; `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g3/560/qa.md` records FAIL for that missing gate and is explicitly worker-authored, not independent verification.

Live issue: https://github.com/IronbellyOrg/IronClaude/issues/560 is OPEN. Its latest comment (2026-11-18, https://github.com/IronbellyOrg/IronClaude/issues/560#issuecomment-6989289883) explicitly sets lowest priority and Backlog and says nobody works on the unused eval harness until it returns to use. That is a hold, not a decision to abandon the fix, so neither close nor not-planned is supported. This review changes neither the issue nor the hold.

Current checkout: `a7ae3dd30fcf88aaab655c37e94e58e121c2d863` (latest commit references PR #754, coordinator-description documentation, not an eval repair). `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/eval/commands.py:642-647` hardcodes the doctor prefix in the shared failure formatter. Both the doctor branch at `:919-921` and run branch at `:1827-1829` call that same formatter before exiting through the coverage failure constant. This directly verifies the wrong run label in source, without running a model. The file's latest logged change is `59ef614e6fd3d3a4c396591e21e4ac1b6a760c26` (formatting, PR #108).

The existing integration tests at `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/cli/eval/test_coverage_gate_integration.py:144-194` and `:238-266` check rejection and missing-pattern text but do not distinguish doctor from run in their prefix assertions. `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/docs/testing/v5.0.0/user/D15-eval-harness.md:445-459` still records the doctor-labelled run output. The required quick architecture analysis is saved at `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g3/560/analyze/analyze-report.md`.

UNVERIFIED: fresh runtime reproduction, installed-console behavior, historical retained probes and their frozen-revision blob equality. None was executed or independently reconstructed in this review, and no product repair or repaired-runtime PASS is claimed.

## Complexity and size
complexity simple; size S. One shared formatter, its two command callers, existing model-free integration tests and one user-guide output example cover the repair; no coverage-policy or runner redesign is needed.

## Priority
P3. Misidentifying the command confuses failure diagnosis but does not remove the coverage rejection, and the latest issue comment explicitly parks this currently unused harness at lowest priority; no active release or implementation blocker is established.

## Concrete next steps
No implementation now. Keep the issue open, unassigned and on Backlog under the recorded hold. The following is a future repair outline only, after the maintainer explicitly lifts that hold:
1. Give the existing shared formatter the command context and update both callers so run says `eval run` while doctor still says `eval doctor`; a global literal replacement alone would break the doctor diagnostic.
2. Extend `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/cli/eval/test_coverage_gate_integration.py` with model-free assertions for both caller labels. Retain the missing-pattern roster, rejection exit 2 and pre-worker rejection behavior. Execute those tests only under a future authorized implementation task, not this read-only review.
3. Update the expected-output example and explanatory text in `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/docs/testing/v5.0.0/user/D15-eval-harness.md:445-459` to distinguish the corrected behavior from the historical observation; do not claim a new manual run without evidence.
4. Do not weaken coverage enforcement or bundle invalid-selection directory cleanup into this diagnostic-label fix.

## Dependencies
Needs: an explicit lifting of the existing backlog hold, not a code dependency. No issue-number prerequisite for the label repair is established.

Parent #354 (v5.0.0 impact-testing assignment, https://github.com/IronbellyOrg/IronClaude/issues/354) tracks this as bug 17; fixing the label contributes only to that item, not the whole assignment. #561 (invalid-selection scratch directories) and #562 (coverage-policy question) are separate and are not prerequisites for supplying caller context. No active issue is verified as blocked solely by #560.

## Related issues
- #354: parent impact-testing assignment. Its comment https://github.com/IronbellyOrg/IronClaude/issues/354#issuecomment-6907496517 reports the wrong-label split and explicitly says that reporting it does not complete bug 17. Later parent discussion retains #560 as open follow-up, with priority and repair scope separate from the parent assignment.
- #561: https://github.com/IronbellyOrg/IronClaude/issues/561, OPEN, run/homes directories remain after invalid selection. Read its body and comments; latest comment also preserves the backlog hold. Different behavior from the label.
- #562: https://github.com/IronbellyOrg/IronClaude/issues/562, OPEN, asks whether installed-hook coverage should reject unrelated suites. Read its body and comments; latest comment also preserves the hold. This is a policy question, not proof the current coverage gate should be removed.

## Related PRs
Issue #560 itself names no PR in its body or three live comments. No dedicated fix PR was identified in bounded, all-state fork searches for `560`, coverage in titles, `coverage gate` in bodies, and `eval doctor` in titles/bodies. Search absence is not proof of exhaustive absence: an unreferenced or differently worded fix PR is UNVERIFIED. The current source independently proves the defect is not repaired in this checkout.

- #75: https://github.com/IronbellyOrg/IronClaude/pull/75, MERGED 2026-05-22, merge commit `0365a055f93e5703d9251873c8422d86e47911b3`. Read its live PR body: historical cliEval remediation and canonical exit-code work, not a verified #560 fix. Its API file subset returned no matching entries, so file-level scope was not established from that response.
- #108: https://github.com/IronbellyOrg/IronClaude/pull/108, MERGED 2026-05-30, merge commit `59ef614e6fd3d3a4c396591e21e4ac1b6a760c26`. Local history identifies it as the target file's latest change; its live body explicitly describes a cosmetic formatting pass with no logic changes. Read the body and comment. This is not evidence of a label fix.
- Search results #667 (post-release documentation), #359 (bare-Python hook), #202 (Tavily integration), #479/#164/#43/#49/#8 (other coverage work), and #260/#259/#68 (other eval mentions) are not established label-fix links; no repair credit is assigned to them.
