## Verdict
still-relevant. This remains an unanswered policy question, not a confirmed wrong-refusal bug and not active implementation. The [live issue](https://github.com/IronbellyOrg/IronClaude/issues/562) is OPEN; the [2026-11-18 owner direction](https://github.com/IronbellyOrg/IronClaude/issues/562#issuecomment-6989290993) explicitly keeps it open, unassigned and Backlog until the eval harness returns to use. That is a hold, not a not-planned decision.

At checkout commit `a7ae3dd30fcf88aaab655c37e94e58e121c2d863`, the selected suite is still checked against installed matcher patterns: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/eval/coverage.py:321-335 collects missing coverage, and /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/eval/commands.py:1798-1829 passes the selected, optionally eval-ID-filtered specs to that gate and exits on rejection before worker dispatch. The empty-HOME workaround remains documented at /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-cli-eval-protocol/refs/eval-contracts.md:54-62, but documentation is not an owner decision accepting it or proof of preserved installed-hook testing. PR #75 (merge `0365a055f93e5703d9251873c8422d86e47911b3`) hardened corrupt-settings rejection; it did not answer this later policy question.

UNVERIFIED: the issue's November 15 count of 16 rejecting suites out of 17, its retained local probe captures, full-install behavior, a passing real-suite run, empty-HOME execution, and current remote-master parity were not re-tested or fetched. This assessment uses current local source and live GitHub issue/PR reads, not a fresh runtime reproduction.

## Complexity and size
complexity simple; size XS. The requested deliverable is an owner policy answer and a short supported-workflow clarification, not a coverage-gate implementation change; any later behavior change needs separate scope and regression planning.

## Priority
P3. The latest issue direction explicitly says lowest priority, open, unassigned and Backlog because the eval harness is not in use; the refusal matters when that tooling returns, but no active delivery blocker is verified ([2026-11-18 decision](https://github.com/IronbellyOrg/IronClaude/issues/562#issuecomment-6989290993)).

## Concrete next steps
1. Now: retain the issue as parked, open and unassigned at low priority. This review does not lift the owner's no-implementation hold or authorize GitHub changes.
2. Only after the owner resumes use of the eval harness: obtain the policy answer requested in the issue, namely whether each selected suite must cover installed checked matcher patterns, what workflow unrelated suites should use, and whether empty-HOME testing is accepted with installed-hook coverage tested separately. Ryan is named in the existing issue comments as a possible policy respondent; no new request was sent.
3. Record that answer and the supported workflow in the issue and operator guidance through the coordinator after the owner's go. Do not present the documented workaround as already approved.
4. Only if the answer requires changed behavior: open a separately scoped implementation plan with model-free regression checks for the accepted policy, preserving rejection of malformed settings and missing required coverage. Do not disable the gate to make unrelated suites pass.

## Dependencies
No prerequisite issue or blocked implementation issue is established by the live issue record. The gating dependency is a future owner decision to resume use of the eval harness and answer the policy question, not a fix to either sibling issue. Issue #354 is the parent validation assignment, not a demonstrated code dependency. Project-board fields were not queried because this task allows only issue and pull-request reads; their current values are UNVERIFIED.

## Related issues
- [#354, release validation assignment](https://github.com/IronbellyOrg/IronClaude/issues/354): the [owner's original filing direction](https://github.com/IronbellyOrg/IronClaude/issues/354#issuecomment-6663807076) explicitly distinguishes the unresolved refusal question from confirmed diagnostic and directory problems.
- [#560, wrong command name on coverage failure](https://github.com/IronbellyOrg/IronClaude/issues/560): open sibling defect, parked under the same lowest-priority hold; fixing its diagnostic does not answer #562.
- [#561, leftover directories after invalid selections](https://github.com/IronbellyOrg/IronClaude/issues/561): open sibling defect, parked under the same hold; its cleanup policy is separate from selected-suite hook coverage.

## Related PRs
- No PR is linked or mentioned in #562's body or its three comments. A live all-state PR search for `562` returned no matches; this is negative search evidence, not proof that no unlinked work exists.
- [#49, widened hook matcher and added consistency checks](https://github.com/IronbellyOrg/IronClaude/pull/49), MERGED, merge `ff99449fefb268d61cc6a0e5f7650240464ec0e5`: historical motivation cited by the coverage module, not a resolution of #562.
- [#75, eval harness remediation](https://github.com/IronbellyOrg/IronClaude/pull/75), MERGED, merge `0365a055f93e5703d9251873c8422d86e47911b3`: its body explicitly records fail-closed handling of corrupt settings. This predates the question and must not be represented as its policy answer.
- Broader all-state search for `"coverage" "eval"` returned historical and unrelated work, with no direct resolution established. Unlinked/private work outside the permitted searches remains UNVERIFIED.
