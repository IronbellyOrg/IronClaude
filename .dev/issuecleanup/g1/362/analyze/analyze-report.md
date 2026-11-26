# Runner architecture analysis

## Scope and grounding
Command: `/sc:analyze .github/workflows --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g1/362/analyze`

Target: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.github/workflows`, the narrowest directory covering all current workflow runner choices. Static review only; no source changes or workflow execution. The governing section structure is the Analysis template in `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g1/362/report-template.md`.

Codegraph: index_state=fresh, checked_at=2026-11-23T23:04:22Z; degraded: none

Access: mcp. Worktree root: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup`. Graph discovery found three YAML workflows; each outline contains zero symbols, so there are no discovered code symbols on which to run call or impact queries. Native file reads and search provide the runner evidence.

## Architecture and metrics
Three YAML workflows contain seven job definitions and seven explicit `ubuntu-latest` runner choices; the two-value swarm matrix adds one instance beyond the seven definitions. The Tests workflow has four upstream job definitions and a summary job that needs those four; there is no runner-selection prerequisite. The two other workflows provide separate pull-request checks. No shared runner selection or self-hosted label is present in the inspected GitHub configuration.

Evidence: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.github/workflows/test.yml:13`, `:54-58`, `:84`, `:146`, `:193-195`; `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.github/workflows/boundary-guard.yml:38`; `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.github/workflows/contract3-generator-constraint-lint.yml:34`. These are configuration facts, not observed workflow runs.

## Severity-rated findings
**P3, backlog mismatch rather than a current defect:** the requested fallback has no IronClaude self-hosted caller. The issue's November 17 comment agrees, identifying private Coder as the only remaining possible consumer; the owner decision recorded on issues 363 and 364 keeps the public repositories hosted. Building a selector here would add an availability-probe dependency to jobs that already use hosted runners.

The requested shared selector, runner-token documentation, non-fallback classification and mocked online/offline tests are not supplied by these workflows. Their absence is not a regression in the currently configured hosted-only architecture. No issue-related P0/P1/P2 defect was established in this narrow quick analysis. This is not a security or performance audit of the workflow steps.

## Recommendations and roadmap
Keep current IronClaude runner declarations unchanged. Retain issue 362 as a parked org-infrastructure request unless the owner separately decides to cancel it. If revived, verify a private Coder consumer and its migration status, agree the component's owning repository and hosted-job overhead, provision credentials outside tracked files, then implement the smallest shared selector with job exclusions and mocked outcomes there. No source modification, staging, commit, remote write or new issue is part of this analysis.

## Verification limits
The analysis is static and narrowly about runner selection. No workflows or tests were executed and no assertion of passing CI is made. Other repositories, secret availability, org runner permissions, live infrastructure state and a full GitHub event timeline are UNVERIFIED. Full issue-review limits are recorded once in the main findings report rather than duplicated here.
