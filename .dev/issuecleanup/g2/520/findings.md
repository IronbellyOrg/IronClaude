# Issue 520 review
## Verdict and evidence
**verdict: in-progress**. Keep [issue #520, Centralized Review Panel](https://github.com/IronbellyOrg/IronClaude/issues/520), open. Reviewed 2026-11-24 at checkout HEAD `a7ae3dd30fcf88aaab655c37e94e58e121c2d863`.

The shared panel already exists and spec-panel uses it, but default reflect and therefore workflow still use the legacy review route. The live reflect protocol explicitly rejects the authoritative panel engine until Stage 3 and describes shadow as measurement only: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-reflect-protocol/SKILL.md:87,309-317`. Spec-panel's shared-panel call path is defined at `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/rules/prompts/document_review_loop_prompts.md:68-70`; workflow invokes reflect with defaults at `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-workflow-protocol/SKILL.md:91`.

PR #519 merged on 2026-11-12, commit `d2d8a2d166c945f556d921b31530a3673f00df89`, and explicitly shipped only measurement, dormant kernel and shadow stages. This is substantial partial delivery, not completed shared-model adoption. Programme issue #549 remains OPEN and its latest inspected comments say the unification plan remains outstanding; unmerged private-branch progress is UNVERIFIED.
## Real current state
| Requirement | Verified current state |
|---|---|
| Existing reusable component | Present, not a greenfield feature. The analyze inventory found 20 Python files in the shared package. Resolver, merge, ledger, telemetry, manifest and citation helpers are registered in `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/review/__init__.py:19-38`. |
| Spec-panel lifecycle | Shared prompts require panel resolution, merged reports and a revision ledger; v1 findings and fix maps remain the spec-facing format. `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/rules/prompts/document_review_loop_prompts.md:56-70`. Three-review cap and escalation are explicitly retained in `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/commands/spec-panel.md:256-268`. |
| Reflect integration | Optional pre-execution shadow uses the core; legacy remains authoritative and default. Post-execution ignores the shadow flag until Stage 5. The protocol now says contract **1.9.0**, not the issue body's 1.8.0: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-reflect-protocol/SKILL.md:309-349`. |
| Shared finding model | Partly reused, not completely unified: reflect's v2 parser imports v1 helpers/constants but adds lenses and channels at `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/review/findings_v2.py:1-38`; spec-panel still emits v1. These versions need an explicit shared-model/caller-boundary contract, not a second implementation. |
| Workflow | Calls reflect with defaults and retains `reflect_status` and `reflect_report_path`; this does not select shadow or the unshipped panel engine. Wave 4 is advisory; the separately added Wave 4R can repair a copy or escalate, so an outdated blanket no-plan-editing claim would be false. `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-workflow-protocol/SKILL.md:87-109`. |
| Existing tests | Source tests cover equal-input deterministic resolution, round-three escalation, invalid findings rejection, revision/re-review and telemetry validation. Evidence: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/review/test_review_panel.py:294-300`, `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/review/test_review_ledger.py:153-294,345-354`, `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/review/test_review_telemetry.py:111-162`. Not executed here, so current pass status and end-to-end caller proof are UNVERIFIED. |
| Current default panel | Packaged pointer selects `wonsol`: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/review/data/review-default.json:1`. PR #623 (`7f93c0d9f7b72938976127d59a2bf523c06d5e03`) calls this provisional because its confirming experiment missed its pre-registered bar; do not claim a confirmed quality win. |
| Additional callers | cli-eval delegates critique to spec-panel and says not to build another panel: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-cli-eval-protocol/refs/create-pipeline.md:21-25`. The issue's cli-portify caller is retired by merged PR #629 (`956f4964264d5efcfbe741ab3dd090fd97f1acb9`); the named source path is absent. |

The issue body is stale where it still calls #519 open. The November 17 comment's pointer to #581 is verified, not a false citation: merge commit `fc4b2240225080cbfc5e7bbc1a1f4f71cd24084d` is the #552 safety-scan change and is also the commit that added `.dev/eval-workspaces/shadow-model-combos/`. That folder's findings file records 5 combinations times 3 repeats, all 15 runs published, and no blind scoring against ground truth, so it does not say which combination finds more real defects (`/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/eval-workspaces/shadow-model-combos/FINDINGS.md:1-3,40-42`). The November 13 request to align orchestrator-mode work has no verified completed alignment record in this review.
## Concrete next steps
1. Have the coordinator propose corrections to the issue after the owner's go: mark #519 merged; keep the #581 pointer and describe it as both the #552 safety-scan change and the commit that landed the 15 unscored shadow runs; update the contract baseline to 1.9.0; remove cli-portify from current adoption requirements; distinguish advisory Wave 4 from Wave 4R remediation. No GitHub changes were made by this worker.
2. Finish the unification plan tracked by #549, capturing #550's proven-design inventory and an explicit orchestrator-mode alignment record. Define one common finding model and small caller-specific adapters; retain the existing panel core and lifecycle helpers.
3. Prove the reflect rollout gates and caller compatibility before enabling authoritative panel execution. Preserve current caller result fields and make engine selection explicit; do not treat shadow completion as a default change.
4. Add cross-caller integration evidence: spec-panel review, revision, re-review and third-review escalation; deterministic panel resolution; rejection of zero valid finding blocks; telemetry validation; workflow's `reflect_*` fields and separate remediation rules. Tests already present should be reused rather than duplicated.
5. Document the actual entry point and caller map, including cli-eval's indirect use and cli-portify's retirement. Close #520 only once the remaining adoption and integration criteria are demonstrated.
## Complexity and size
**complexity: complex; size: L.** The existing core avoids a rebuild, but shared finding semantics, staged reflect rollout, workflow compatibility and regression evidence span multiple caller contracts and experimental gates; this is larger than a documentation-only cleanup.
## Priority
**priority: P2.** Unification reduces duplicated review behavior and is needed for consistent shared-panel adoption across reflect and workflow, but current legacy/spec-panel paths remain available and this review found no evidence of an immediate outage, data-loss incident or release-stopping dependency.
## Dependencies
- **Needs #549**, Review-Panel Merged Efforts (OPEN): programme sequencing and the unification plan. This is a body-described dependency, not a GitHub blocked-by edge.
- **Needs coordination with #550**, proven tasklist experiment capture and re-test (OPEN): incorporate validated designs without losing their evidence; the precise implementation order belongs in #549's plan.
- **Enables #550's incorporation/re-test portion** once the unified panel exists. Inventory can proceed independently, so this is not a blanket circular hard block.
- **Related, not established hard prerequisites:** #531 (general shadow-run module), #487 (reusable evaluation framework), #489 (panel tier/alias follow-up). No source requires all of these broad features to finish before #520.
- GitHub issue view returned zero `blockedBy` and zero `blocking` edges for #520. No other formal dependency or downstream blocker was verified.
## Related issues
- #549 (OPEN): Review-Panel Merged Efforts, the programme tracker.
- #550 (OPEN): record, fold in and re-test proven tasklist experiment designs.
- #346 (CLOSED): original document-loop convergence problem; closure is not proof of #520's caller adoption.
- #531 (OPEN): general Shadow Run Module, broader than reflect's existing shadow route.
- #487 (OPEN): reusable Spec-Task Eval Framework, broader measurement/automation work.
- #489 (OPEN): follow-up for panel tiers and live alias mapping.
- #488 (CLOSED): ccsession tier reorganization, historical prerequisite for the original panel integration.
- #552: consequence-grading programme, linked by verified merged PRs #581/#582; this review did not fetch its full issue, so its current issue state is UNVERIFIED.

Only the relationships above were verified from issue bodies/comments and PR contents. No duplicate issue was established.
## Related PRs
All PR numbers below are on `IronbellyOrg/IronClaude`; states and merge commit ids were read directly using `gh pr view` or bounded `gh pr list`.

| PR | Verified state and significance | Merge commit |
|---|---|---|
| #482 | MERGED: removes finding quotas from producer QA; not caller adoption. | `b681ace43bd4c59f4e61c4e1afbc0430441a8379` |
| #484 | MERGED: shared document-review prompts and hard gate for spec-panel. | `ae9fcedfebe9651dd624942a3ab8c3e3c5fe9a21` |
| #490 | MERGED: live seven-reviewer template and existing panel/merge/ledger core. | `3b1f1eb109b9f7360fe8812a5825c0ea4fd9902e` |
| #498 | MERGED: promotes original review-loop/panel/tier integration to master. | `9163bd1c7d11091fd39c687a7b6935b58484fd4d` |
| #500 | MERGED: original A/B experiment artifacts; its mostly empty PR body does not establish a quality result. | `ec259f1b718ccdb9f08bba0237bfa47b2b7601a2` |
| #519 | MERGED: reflect Stage 0-2, default legacy, dormant/shadow only; outstanding exit gates stated in its body. | `d2d8a2d166c945f556d921b31530a3673f00df89` |
| #581 | MERGED: #552 safety-scan and print-only follow-up; the same merge commit also added the 15-run shadow-combination workspace. Those runs are published but not blind-scored, so they are not a quality verdict. | `fc4b2240225080cbfc5e7bbc1a1f4f71cd24084d` |
| #582 | MERGED: consequence-based grading and fixcheck. | `64e8eacf2b3ff40be07ae9c9959071684c3765a0` |
| #623 | MERGED: provisional wonsol default panel. | `7f93c0d9f7b72938976127d59a2bf523c06d5e03` |
| #629 | MERGED: removes cli-portify, invalidating that current-caller part of #520. | `956f4964264d5efcfbe741ab3dd090fd97f1acb9` |
| #696 | MERGED: workflow surgical remediation for #624, explaining the separate Wave 4R. | `f2904292eed1f6710ebc5dca2eb48394fd1775f6` |

Issue #520 has no closing PR in `closedByPullRequestsReferences`. Searches for `520`, `review panel`, `unification` and `shadow-model` found no verified PR completing the remaining cross-caller adoption; this is bounded search evidence, not proof that no unpublished or differently worded implementation exists.
## Verification limits and negative evidence
- **Timeline UNVERIFIED:** the brief's GitHub allowlist permits only issue view/list and PR view/list. Those reads returned #520's body, both comments, dates, direct dependency edges and closing-PR references, but not the complete event timeline or all incoming cross-references. No disallowed API/GraphQL call was used. This limits history completeness, not the locally verified missing default integration.
- **Runtime UNVERIFIED:** the required quick architecture command is static. Tests were inspected, not run; no live model review, end-to-end revision loop, benchmark or paid evaluation was executed. No pass count is claimed.
- **Off-checkout work UNVERIFIED:** #549's comments describe private-branch research and a comparison package; their live progress and the old-worktree transition were not inspected. No claim that the plan does not exist anywhere is made.
- **History check:** the November 17 comment's #581 pointer is confirmed by the merge commit's added files and by the workspace findings file (15 published runs, no blind quality score). An earlier draft of this report wrongly treated that pointer as false; the independent review caught it and this text is the correction. Broad PR output exceeded the tool limit once, so pertinent PRs were individually read rather than inferred from the truncated output.
- **Negative checks:** the initial issue lookup failed because it combined --comments with --json; the successful retry used JSON with the comments field. The project-local analyze command directory does not exist; the global copy passed the guard. The old cli-portify path and a source-name Glob are absent; merged #629 confirms retirement. A first report Edit was refused by the freshness hook, then recovered by a tracked Read and normal Edit.
- **Scope:** no source edits, GitHub changes, staging, commits, pushes, worktree changes or outward publication. All outputs stay under this task's report directory.
- **Analyze evidence:** `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g2/520/analyze/analyze-report.md`; `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g2/520/analyze/return-contract.yaml`.
- **Review:** independent review outcome is recorded separately at `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g2/520/evidence-review.md`.

Report structure derives from the coordinator's required fields and the task-local report template read at `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g2/468/report-template.md` (findings skeleton, analyze skeleton, handoff skeleton and review skeleton).
