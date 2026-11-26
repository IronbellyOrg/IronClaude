# Issue 446: bounded index-lock retry review

Template: findings structure from /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g1/362/report-template.md, adapted to the coordinator's required fields.

## Verdict and evidence
**Verdict: still-relevant.** Reviewed 2026-11-23 at checkout commit `a7ae3dd30fcf88aaab655c37e94e58e121c2d863`. The approved retry is still absent: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/core/WORKER-CONTRACT.md:45 tells a worker to report `blocked` with the path, without a retry or lock age. Issue #446 remains OPEN; its 2026-11-17 comment accurately describes this gap. No linked closing PR is returned by the issue read. The comment mentions merged PRs #584 (`b6d038a30c15ebeab5797c7b039500ee5dc6bb63`) and #585 (`bfabf1d63225d71fda57680c3be125bd2662814d`), but those address approval wording, not the retry.

## Real current state
- The governing rule is plain-language worker guidance, not a lock-retry implementation. Canonical source: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/core/WORKER-CONTRACT.md:41-45. The installed copy at /home/coder/.claude/WORKER-CONTRACT.md:45 also retains the immediate-block rule.
- The existing test suite pins the worker's outward-action restriction, not this retry: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/skills/test_worker_contract.py:123-129. Searching that entire file for `index.lock` found no occurrence. The missing 1, 2, 3, 4 second schedule and lock-age report therefore have no specific contract test there.
- The technical reference repeats the immediate-block behavior at /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:711 and should stay aligned when the rule changes.
- Searches of the routing guide and its plugin copy found no `index.lock` restatement, so neither currently needs a lock-rule edit. The source tree has exactly one `index.lock` occurrence, in the contract. Separate worktree-cleanup tests mention locks but do not implement the requested worker retry.
- Historical investigation /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issues/339/analysis/inv-005-orca-index-lock.md:99-110 explains the false-block mechanism and recommends a separate bounded retry. It is historical evidence, not a rerun against today's Orca or Git.

## Concrete next steps
1. Change WC-9 in the canonical contract to re-check after waits of 1, 2, 3 and 4 seconds, stopping the wait when the lock disappears. Keep the total bound at about 10 seconds; never delete, move or edit the lock. If it persists, report `blocked` with its actual path and age from its modification time. These requirements are already specified in issue #446, not a new scope proposal.
2. Add a contract regression check for the schedule, total bound, never-delete/move/edit rule and path-plus-age report, following the existing phrase-pin and negative-test pattern. Keep the technical-reference sentence aligned; no new lock service is needed.
3. During implementation, run the issue's requested checks: `make sync-dev`, `make verify-sync`, `make lint`, and `uv run pytest tests/skills/test_worker_contract.py`. These are future checks, not claimed results of this report. Do not stage the generated development copies.
4. Keep GitHub changes with the coordinator after the owner's go. Nothing in this review authorizes implementation, a commit, or closure.

## Complexity and size
**Complexity: simple. Size: S.** The behavior is fully specified and localized to one contract sentence, its regression tests, and one technical-reference restatement; no application architecture or data migration is needed.

## Priority
**P2.** This reduces avoidable worker stoppages and coordinator intervention during parallel work, but the present rule fails safely rather than risking data loss; no verified urgent blocker or frequency measurement supports P0/P1.

## Dependencies
No hard issue dependency was verified. GitHub returns zero `blockedBy` and `blocking` relationships, no parent, and no subissues for #446. It supports #339's orchestration work but need not wait for that larger feature, and #534 explicitly excludes this retry from its own scope. No specific downstream issue is verified blocked by #446.

## Related issues
- [#339: orchestrator mode](https://github.com/IronbellyOrg/IronClaude/issues/339), OPEN: parent work in the narrative; the retry was intentionally split out.
- [#534: Phase 1 sweep follow-ups](https://github.com/IronbellyOrg/IronClaude/issues/534), OPEN: its body explicitly states WC-9 lock retry is tracked separately by #446 and is not part of #534.

## Related PRs
- [#584: issue-pipeline approval core](https://github.com/IronbellyOrg/IronClaude/pull/584), MERGED 2026-11-17, merge `b6d038a30c15ebeab5797c7b039500ee5dc6bb63`. The issue's comment names it because it changed the contract; its body identifies the contract edit as the chat-based approval amendment.
- [#585: narrow the approval amendment](https://github.com/IronbellyOrg/IronClaude/pull/585), MERGED 2026-11-17, merge `bfabf1d63225d71fda57680c3be125bd2662814d`. Its body describes a one-line approval-wording change, not index-lock handling.
- No implementing PR was verified. GitHub returns no linked closing PR for #446, and the repository PR search for `"index.lock"` returns none. Broad numeric searches returned older apparently unrelated hits, so those are not treated as evidence of implementation or a complete linkage inventory.

## Verification limits and negative evidence
- **UNVERIFIED: full GitHub event timeline.** The brief permits only `gh issue view/list` and `gh pr list/view`. An attempted `gh issue view 446 --repo IronbellyOrg/IronClaude --json timelineItems` failed with `Unknown JSON field: "timelineItems"`; the supported field list contains no timeline/events field. No API or browser access was substituted outside that allowlist. The issue body, its single returned comment, creation/update times, dependency metadata and closing-PR references were read, but label/assignment/cross-reference event history could not be verified.
- **UNVERIFIED: current runtime lock duration and frequency.** No lock was created, touched, removed or experimentally held. The issue's original timing observations and the historical investigation were not rerun.
- Negative evidence: the full contract-test file has no `index.lock` match; the canonical source tree has only the contract's immediate-block sentence; the routing guide and plugin copy have no index-lock restatement; no matching PR was found by the lock-name search. These searches do not prove that no unpushed/private work exists elsewhere.
- No tests, lint, sync, install, commit, staging, or GitHub write was performed. This is a static issue review; the contract still lacks the requested behavior, so tests passing today would not close the issue.
- Guard passed: the installed analyze command has an Unattended mode section, the project command copy is absent, and the dispatched command carries exactly one report directory and a standalone unattended flag.
- Supporting analysis: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g1/446/analyze/analyze-report.md. Handoff: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g1/446/analyze/handoff/1-analyze.md.
