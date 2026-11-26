# Notes for NP-5 (TASK-WF-analyzeCodegraph-20261111-193557)

## Dropped findings

- F6 (guide section 7 says it is the only section naming the forbidden verbs, but analyze.md restates them): concerns the design chosen in source.md section 2.4 item 4 and the shipped text, not a plan defect.
- F7 (Leads bullet packs four rules in one line): a maintainability remark about shipped text, weakest finding (confidence 0.55), partly contaminated by later PR #513.
- Refuted findings V1-F2, V2-F1 matrix clause, V2-F2 return-contract clause, V3-F2: refuted or misattributed to post-execution evolution in the report.

## Verification and caveats

- Base: first 'start sha=' (54799c0c...) is a tree hash, not a commit. The task-start HEAD in artifacts/retries/T1/q0-head (ec259f1b718ccdb9f08bba0237bfa47b2b7601a2) is a real commit and an ancestor of 7764bb623. At base analyze.md exists with `mcp-servers: []` (line 6) as the plan says; CODEGRAPH.md and reflect.md exist. The start tree additionally contains the design.md edits of the sibling package (implemented first in the same worktree); base correctly excludes them because this plan does not touch design.md. masked_paths is empty (no created repo file exists at base).
- Plan text verified: sha256 of the done-folder plan equals the PLAN: hash in progress.md (674f7eb8...); plan lines cited by the report (29,33,34,43,44,56,57) match.
- The report states analyze.md changed after execution (PR #513 and #515); the five items rest on plan text and source.md only.
- No blocking items: report says 'Zero blocking findings', all MINOR; no review record under artifacts/retries.
