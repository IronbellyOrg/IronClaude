# Architecture analysis for issue 731

## Scope and grounding
Command: `/sc:analyze src/superclaude/skills/sc-implement-protocol --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g5/731/analyze`

Checkout: `a7ae3dd30fcf88aaab655c37e94e58e121c2d863`, checked 2026-11-24. This is the narrowest distributable execution component directly named by issue 731 and its dependency 733, not an audit of the entire proposed BMAD pipeline. Six files discovered: SKILL.md, four reference documents and one existing archive helper. The issue's draft pipeline lives on another branch, not as an installed pipeline component here.

Codegraph: index_state=fresh, checked_at=2026-11-24T14:17:58Z; degraded: graph:empty

Graph layout found only the Python archive helper; the explicit SKILL.md outline lookup returned no match because protocol markdown is not indexed. Markdown Glob/Grep/Read supplied the evidence. No source changes or runtime commands were made.

## Findings
- High impact for unattended execution, not an emergency production defect: the protocol's recognized options at `src/superclaude/skills/sc-implement-protocol/SKILL.md:55-59` do not include unattended/report-dir/plan-review/plan-only. Grep across the entire protocol directory found none of those names or E-PLAN-NOT-REVIEWED. The existing executor cannot be treated as issue 733's proposed unattended executor.
- Medium integration impact: halted work requires actual user acceptance, and automation may not start an operator review (`refs/qa.md:240-256,276-288`); resume rows P/H currently select an operator review (`refs/ledger.md:155-160`). A future unattended wrapper must return a blocked result rather than guessing consent or initiating that review. Existing attended safeguards must remain.
- Medium integration impact: existing managed staging instructions remain in `refs/ledger.md:3`, `refs/managed-workspace.md:36` and SKILL.md:139; conversion must implement the staging deferral required by the shared worker contract, not merely attach a flag to a brief.

All paths above are relative to `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup`. No quantified performance or security result is asserted; this was a static architecture pass. The archive helper's existing behavior is not evidence of a new release-pipeline implementation.

## Recommendations and limits
Keep issue 731 open as a trial-first backlog item. Build the bounded prerequisite in issue 733 before claiming unattended story execution; issue 734 supplies the separately dispatched plan-review loop. Preserve the existing acceptance and halt boundaries. Do not add a new release planner, filer or handoff command before the first trial demonstrates a need.

The pinned draft record at branch commit `fb97f77c1ddd7ef385df5d5730f6f7c17948f9e8` already records O3 as answered (panel approval, not human plan approval) and OD-1 as resolved into issue 734. Copies are retained beside this report's parent directory as source-pipeline-record.md and source-consensus.md. The issue body is stale on O3. Current remote draft-branch contents, a completed first release, and BMAD runtime compatibility remain UNVERIFIED. No UV, tests, builds, installs, commits, staging or GitHub writes were run.
