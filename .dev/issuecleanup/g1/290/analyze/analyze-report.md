# Primitive governance architecture analysis

Command: `/sc:analyze src/superclaude/core/HOW-WE-WORK.md --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g1/290/analyze`

Structure: `/sc:analyze` Output sections.

## Scope and grounding
Reviewed 2026-11-23 at checkout `a7ae3dd30fcf88aaab655c37e94e58e121c2d863`. The narrow primary target is the source routing guide, where the owner decided the basic contribution rules should live. Supporting scope is the contributor guide, onboarding contribution slide, issue/PR templates and CI workflow definitions. This is static architecture analysis; no runtime, tests, builds, fixes, stages or commits were run.

Codegraph: index_state=fresh, checked_at=2026-11-23T22:44:40Z; degraded: graph:empty

Access is MCP, worktree_root is `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup`. The single readiness check reported zero changed files. The grouped core listing contained only the Python initializer, and the routing-guide outline returned no indexed file: Markdown is not indexed, so direct Read/Grep supplied the evidence. No caller/impact claim is inferred from an empty graph result.

## Severity-rated findings
1. **Medium: contribution policy is missing from the authoritative rules.** `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/core/HOW-WE-WORK.md:251-263` covers general conduct but not the owner's issue-first restriction for new team members, reuse discovery before proposing a primitive, evidence requirements or caller revalidation. Readers cannot recover the October 29 decisions from their normal entry point.
2. **Medium: the contributor guide still teaches direct primitive PRs.** `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/docs/developer-guide/contributing-code.md:173-235` gives implementation and submission steps and a new-agent/command/skill checklist without the issue-first restriction. Ordinary push approval is not the same as the owner's temporary restriction on new members making primitive-change PRs.
3. **Medium: onboarding still defers the decision.** `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/docs/onboarding/ironclaude-onboarding.html:515-527` explicitly lists contribution rules as being worked out. The issue's completion requirement is visibly unmet.
4. **Medium: existing templates are generic, not the requested evidence contract.** `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.github/PULL_REQUEST_TEMPLATE.md:26-48` asks for tests and green CI, but not reviewer-first approval followed by a measured value-versus-cost evaluation. The existing feature form is already improvement intake; adapt it if it can carry discovery results and affected primitive/caller evidence rather than adding a duplicate form.

## Code quality metrics
- Four architecture/documentation gaps above; no numerical quality score or measured return on investment is claimed.
- All 363 lines of the primary routing guide were read in bounded chunks. Its general rules contain no primitive-contribution policy.
- Four issue-template/config files exist: bug, feature, other and configuration. A generic PR template also exists. This corrects the original issue body's historical claim that no issue templates exist.
- Local source changes: zero. Report-only artifacts are confined to the assigned report directory.

## Security vulnerabilities
No exploit or vulnerability was established by this documentation-focused review. The comment's proposed security-vetting pipeline, permissions and governed registry are future requirements, not verified deployed protections; registry security implementation is outside this narrow analysis.

## Performance issues
No performance measurement was run or needed for a contribution-policy document. An ROI acceptance threshold is not specified by the owner comment, and no such threshold or primitive-evaluation gate was found by searches across the checked-in CI workflows.

## Recommendations
Keep issue 290 open as still-relevant. First publish the already-decided issue-first policy in the routing guide, add the corresponding restriction and source link to the contributor guide, and replace only the contribution card in the onboarding deck. Reuse or extend generic improvement intake, and add the missing primitive-change evidence fields to the PR process without claiming that its future CI gate already exists. Define the ROI measure/threshold and approving role with the owner before opening contribution access; track registry and skill-creator-fork work separately rather than making this documentation issue a platform build. Issue 487 is a technical dependency for lifting the temporary restriction, not for documenting it now.
