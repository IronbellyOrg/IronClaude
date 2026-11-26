# Issue 376: adversarial scoring consistency review

- **Date:** 2026-11-23
- **Claims verified:** See Validation Results.
- **Template:** /home/coder/.claude/templates/modularization-template-review/analyst-cross-validation_report_template.md, extended with the exact issue-review fields in the dispatch brief.
- **Issue:** https://github.com/IronbellyOrg/IronClaude/issues/376
- **Revision:** a7ae3dd30fcf88aaab655c37e94e58e121c2d863

## Verdict with evidence

**verdict: still-relevant.** Keep the issue open. The current checkout still carries the exact conflicting scoring instructions; no issue-specific corrective PR was found. This is an unresolved defect in an existing feature, not evidence of an implementation currently in progress.

- Canonical rule: six dimensions, 30 criteria, `/30`, and a minimum invariant subtotal, with an all-zero suspension warning: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-adversarial-protocol/SKILL.md:237-252.
- Both actual pass instructions still request 25 criteria: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-adversarial-protocol/SKILL.md:1753-1759.
- The output template still has five summary dimensions and two `/25` cells, omitting the invariant subtotal and floor record: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-adversarial-protocol/refs/artifact-templates.md:189-212.
- A third stale instruction survives in the debate summary: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-adversarial-protocol/refs/debate-protocol.md:185-194.
- Evidence version is checkout commit a7ae3dd30fcf88aaab655c37e94e58e121c2d863. PR 458, merged as ed6074c476a6d2a9b64477a310cd1096284cc01b, concerns MCP tool names, not this fix. PR 519, merged as d2d8a2d166c945f556d921b31530a3673f00df89, concerns reflect's dormant/shadow panel work, not rubric consistency.

## Real current state

The scoring design is already written, but its pass instructions and report consumer disagree with it. A static fixed-verdict example still distinguishes the contracts: 25 ordinary criteria met and all five invariant criteria not met produces 25/30 = 0.833333 under the intended rule, versus 25/25 = 1.0 under the old template. If another candidate reaches the invariant minimum, the zero-invariant candidate must be ineligible; the template provides no place to demonstrate that decision. This is arithmetic and source evidence, not a reproduced live failure.

The issue is OPEN with one returned comment, the 2026-11-17 status review. Its core defect remains accurate. Its historical assertion that PR 458 was the most recent skill-folder change is no longer current: local history also contains 5b7d13e73 (PR 617, removal of spawn) and af5fb69eb (PR 632, removal of retired CLI families), without removing the stale scoring text.

The narrow architecture command completed as a static analysis; its evidence source is /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g1/376/analyze/analyze-report.md. No source was changed.

## Concrete next steps

1. Align the three active 25-criterion instructions and the base-selection template with the existing 30-criterion contract. Include the sixth evidence table/subtotal, normalized denominator and explicit eligibility or all-zero suspension warning. Do not redesign the floor policy.
2. Complete the issue's requested consistency checks and fixtures: stable unique criterion identities, matching forward/reverse sets, disagreement reconciliation including invariant criteria, exact dimension/total sums, bounded scores, missing/duplicate criterion rejection, denominator rejection, eligible-competitor floor enforcement and all-zero suspension. A prose-only number replacement does not satisfy these acceptance criteria.
3. Inspect scoring consumers and generated distributions; use the normal source sync process after an authorized fix, without staging generated skill/command mirrors. The source/test scan also found a score-comparison evaluation suite, so check its expectations rather than assuming only the three protocol files matter.
4. After static checks, obtain authorization for the one actual debate required by the issue, and save its fixture, source revision, observed score record and eligibility result. Do not claim the issue done without that evidence.

## Complexity and size

**complexity: medium. size: M.** The text repair spans three source files, but full acceptance also needs a criterion-identity/completeness check, deterministic scoring/floor/reconciliation fixtures, consumer/distribution review and a separately authorized observed debate. No architectural redesign is needed.

## Priority

**priority: P2.** Wrong totals and omitted eligibility can change the document chosen as the merge base in a shared debate/review path. That warrants a normal correctness fix, but no outage, security incident, demonstrated live mis-selection or release-blocking issue dependency was established.

## Dependencies

- **Needs:** No issue-number prerequisite found. GitHub's returned blockedBy and blocking connections are both empty, and the correction can use the existing scoring design without waiting on another issue.
- **Blocks:** Reliable scoring/eligibility evidence for adversarial base selection and its reflection consumers. No specific issue number was verified as formally blocked by 376.
- The live-debate acceptance step needs separate authorization; that is an execution gate, not an invented issue dependency.

## Related issues

- **Issue 346, closed:** https://github.com/IronbellyOrg/IronClaude/issues/346 concerns document review-loop growth and convergence. It is related review-quality work, explicitly not the 25-versus-30 scoring fix and not a prerequisite.
- The comment's reference to **519 is a PR**, not an issue dependency. Broad issue searches for adversarial scoring and rubric returned 376 as the direct match; other results were different feature areas, not verified duplicates.

## Related PRs

- **PR 458, merged:** https://github.com/IronbellyOrg/IronClaude/pull/458 updated MCP tool names. Its body and issue comments were read; the scoring contradictions remain in the current source.
- **PR 519, merged:** https://github.com/IronbellyOrg/IronClaude/pull/519 added reflect panel measurement and dormant/shadow machinery. Its body explicitly says the default remains legacy, so do not infer that this PR activated a new panel. Independently, the current reflection protocol delegates its deeper review merge to adversarial scoring at /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-reflect-protocol/SKILL.md:664-680.
- **PR 617, merged:** https://github.com/IronbellyOrg/IronClaude/pull/617 removed spawn and updated two references in the adversarial skill. Merge commit: 5b7d13e73b054bc99a6be3b1d4053d1b7c3137e2.
- **PR 632, merged:** https://github.com/IronbellyOrg/IronClaude/pull/632 removed retired CLI families. Merge commit: af5fb69eb9b016287e3560cda50bce2a16123349, the latest local commit touching the target skill folder. It did not resolve the scoring mismatch shown above.
- PR searches across all states for `376`, `adversarial scoring` and `rubric` found no verified PR implementing this fix. That is bounded search evidence, not proof about unmentioned private/unpushed work.

## Validation Results

| # | Claim | Source | Code Path Checked | Verdict | Notes |
|---|-------|--------|-------------------|---------|-------|
| 1 | The original mismatch and missing eligibility record persist. | Issue 376 body and its one returned comment | Source paths in Verdict with evidence; detailed canonical claim table at /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g1/376/analyze/analyze-report.md | VERIFIED | Three stale criterion-count instructions and one stale denominator row remain. |
| 2 | The affected scoring record has a real downstream protocol consumer. | Current reflection protocol | /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-reflect-protocol/SKILL.md:664-680 | VERIFIED | Deeper reviewer-card merging delegates to adversarial rather than reimplementing debate. This establishes a protocol dependency, not a reproduced runtime failure. |
| 3 | Existing evaluation checks prove arithmetic/floor correctness. | Closure check | /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/eval/suites/frontier_vs_cheap_combo.yaml:84-107 and targeted test searches documented in the analysis | CONTRADICTED | This inspected evaluation case checks file existence and score-name substrings, not score arithmetic or eligibility. No claim is made about all differently named tests. |
| 4 | The issue's complete event timeline has been verified. | Required review scope | Allowed GitHub issue/PR view/list interfaces | UNVERIFIED | Returned state, comments and closure relationships were inspected; full event history is not exposed by the allowed fields. |

## UNVERIFIED and limitations

- **Full issue timeline: UNVERIFIED.** The installed GitHub CLI rejects a combined comments-plus-JSON request; the successful JSON request returned the body, the comment list, OPEN state, empty closure-PR references and empty blocking connections. A complete event timeline requires an interface the brief did not allow, so no API/browser workaround was used.
- **Live behavior and acceptance run: UNVERIFIED.** No debate or paid model run occurred. This was a static architecture review; no test suite was run and no source fix was attempted.
- **Latest remote branch content: UNVERIFIED.** No fetch was authorized or performed; all source conclusions are scoped to the recorded local revision and freshly read files, not an assumed current remote master.
- **Full PR diff completeness: UNVERIFIED.** The two mentioned PR view requests returned empty file arrays despite local history showing target-folder changes under PR 458. The report uses returned PR bodies/merge metadata plus local source/history, not those empty arrays as proof that files were untouched. PR comments returned for 458 and 519 were read; complete review-thread/event history was not retrieved.
- **Absence of any future/in-flight implementation: UNVERIFIED.** Searches found no verified corrective PR, but cannot exclude unpushed work or a PR without searchable issue/scoring terms.
- All writes belong to this dispatch's report directory. No GitHub item was edited, commented on, labeled, closed or linked; no staging, commit, push, sync or external publication occurred.
