# Issue 362: runner fallback review

## Verdict and evidence
**verdict: still-relevant**, as a parked org-infrastructure request, not an IronClaude implementation gap. Issue 362 remains OPEN and explicitly says low-priority backlog; its 2026-11-17 comment identifies private Coder as the remaining possible consumer. No verified owner decision cancels that fallback request. The closed Windows and ARM runner issues do not establish completion or cancellation of this separate request.

Reviewed on 2026-11-23 at checkout `a7ae3dd30fcf88aaab655c37e94e58e121c2d863` (also the locally recorded origin/master; no fetch performed). All seven runner declarations in current IronClaude workflows select `ubuntu-latest`: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.github/workflows/test.yml:13`, `:54`, `:84`, `:146`, `:193`; `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.github/workflows/boundary-guard.yml:38`; `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.github/workflows/contract3-generator-constraint-lint.yml:34`. There is no self-hosted job here to fall back from.

Issue: https://github.com/IronbellyOrg/IronClaude/issues/362 . Latest discussion: https://github.com/IronbellyOrg/IronClaude/issues/362#issuecomment-6941376595 . This is a recommendation only; no issue or PR was changed.

## Real current state
- **RUNS (configured, not executed during this review):** three workflow files, seven job definitions, all explicitly hosted. The marker matrix expands one job definition into two lanes, so there are eight job instances when all workflows and lanes are triggered; path-filtered workflows need not trigger on every change.
- **NOT BUILT in the active workflow surface:** no shared runner-selector workflow, no composite action under the inspected `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.github` tree, no online-runner API probe, and no dynamic runner output. Searching that tree for `runs-on:`, `self-hosted`, `workflow_call`, `actions/runners`, `runner-selection` and `fromJSON(needs` returned only the seven hosted declarations.
- **STUBBED:** no runner-fallback stub found in that inspected surface. This is not a claim about every script or the other repositories.
- The issue was created 2026-11-04; its latest update and sole comment are dated 2026-11-17. The body proposes a hosted first job to query runner availability and records cost, busy-runner and race limitations. It is a proposal, not an implemented component.
- The November 4 owner decision recorded on issues 363 and 364 keeps IronClaude and IronOrca on hosted runners. Their November 17 closure comments say there is no private Windows or ARM consumer; they do not say private Linux x64 jobs or fallback are unnecessary.
- **UNVERIFIED:** present Coder workflow inventory, whether its self-hosted migration landed, present org runner status, existence and permissions of a runner-read token, and actual CI execution success. The historical HTTP 403 is recorded by the issue, not reproduced here.

## Concrete next steps
Keep parked; do not add runner-selection code to IronClaude. If the owner picks this up, first verify a private Coder consumer and that its self-hosted migration has landed, then decide whether one extra hosted selector job per run is worth it. Obtain the runner-read credential through the owner's secret-management process, choose the reusable component's owning repository, classify jobs that cannot use hosted machines, implement label-compatible selection, and add mocked online/offline tests plus permission-error and non-fallback cases. Recheck API permissions and the issue's proposed design against current platform documentation then. Any issue move, closure or cross-repository link is a coordinator/owner action, not authorized here.

## Complexity and size
**complexity: medium; size: M.** The selector itself is small, but completing the stated acceptance criteria includes credential provisioning, reusable-workflow wiring, per-job network/capability exclusions and mocked outcomes in the consuming repository; cross-repository adoption and token readiness remain UNVERIFIED.

## Priority
**priority: P3.** The issue is explicitly parked low-priority work, no IronClaude workflow needs the feature, and GitHub records no issues blocked by it; impact on private Coder is UNVERIFIED, not a demonstrated current outage.

## Dependencies
- Verified GitHub dependency fields: `blockedBy.totalCount = 0`, `blocking.totalCount = 0`; no numbered needs/blocks dependency is recorded.
- Procedural prerequisites named by the issue: per-repository self-hosted migrations first, a runner-read secret, and a decision that fallback is worth its overhead. The issue does not name the migration PR numbers; their current state is **UNVERIFIED**.
- Issues 363 and 364 are context, not dependencies: Windows and ARM runner capacity is not required for a Linux x64 availability selector. No known issue is proven blocked by 362.

## Related issues
- **363, Windows self-hosted capacity:** CLOSED 2026-11-17, no closing PR; closure says no private Windows consumer currently exists. The earlier owner comment keeps the public repositories hosted. https://github.com/IronbellyOrg/IronClaude/issues/363
- **364, ARM self-hosted capacity:** CLOSED 2026-11-17, no closing PR; closure says no private ARM consumer currently exists. The same public-repository decision is recorded. https://github.com/IronbellyOrg/IronClaude/issues/364
- No additional related issue is established by the issue body/comments. A full org-wide issue inventory was outside the allowed repository scope.

## Related PRs
- **402, parallel tests and shorter timeout tests:** MERGED 2026-11-05, merge commit `80f361804b155e3fec842cc552b8f4f0c71b2cdd`. Its body describes test execution speed, not runner selection; its changed-file list includes the Tests workflow and README. It is the PR explicitly mentioned in the issue's latest comment. Local workflow history also lists this as the latest workflow-changing commit. https://github.com/IronbellyOrg/IronClaude/pull/402
- Issue 362 has no `closedByPullRequestsReferences`. An all-state PR search for `"#362" in:body` returned none. A broad `362` search returned PR 64 (Auggie review skill), but that loose search hit is not established as related and is excluded. The runner-title search returned application/task-runner PRs, not a hosted-fallback PR.
- The per-repository migration PRs referred to generically in the issue are unnamed and **UNVERIFIED**. No inference of implementation completion is made from search absence.

## Verification limits and negative evidence
- **Timeline: UNVERIFIED beyond issue/comment timestamps and linked-PR fields.** The allowed `gh issue view 362 --repo IronbellyOrg/IronClaude --json timelineItems` failed with `Unknown JSON field: "timelineItems"`. Its supported fields do not include the full event timeline. No `gh api`, browser workaround, other-repository read or GitHub mutation was used; the coordinator needs an approved timeline-capable read to finish that portion.
- Remote source freshness: only the local checkout and locally recorded origin/master were compared; both were `a7ae3dd30fcf88aaab655c37e94e58e121c2d863`. Current remote HEAD is **UNVERIFIED**, since the worker did not fetch or inspect PR-less remote source.
- Negative evidence is scoped: the active GitHub configuration tree was searched, all three workflow files were inspected for runner configuration, exact issue-reference and runner-title PR searches were run, and issue dependency/closing-PR fields were read. Absence from those sources is not proof of absence elsewhere.
- No CI jobs, mocked selector tests, live runner API, secrets, Coder workflows, historical audit files or external platform documentation were executed/read. API-permission and availability statements from the issue remain historical claims, not independently verified current infrastructure facts.
- The first report edit was blocked by the file-freshness hook because Write did not count as Read; reading the stub and retrying the normal Edit resolved it. No bypass was used.
- Required command was invoked through the Skill tool at top level. Its report is `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g1/362/analyze/analyze-report.md`; its contract and handoff are retained beside it. Final issue review status is partial solely because the full event timeline could not be read under the allowed command surface.
