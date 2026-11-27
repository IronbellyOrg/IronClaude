# Notes for NP-4 (TASK-WF-designOutput-20261111-193642)

## Dropped findings

- MF-2 (conditional codegraph_impact in shipped design.md:65) and MF-10 (extra fallback tokens): refuted in the report as post-execution evolution (commit 930c5ebc8, PR #513), not plan defects.
- MF-3 (no before-state baseline for the archived package): the report records dissent; it is a vantage artifact of reviewing an archived package, since `git diff` against HEAD is a valid baseline at execution time.
- MF-5 (shipped design.md never mentions SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off): the plan (line 28) does require it; the omission is a defect of the code written, not of the plan. Its plan-side cause is item GT2.
- MF-7's coverage-matrix traceability slip: a defect of the review artifact, not the plan; only the AC gap is kept (GT4).

## Verification and caveats

- Base: first 'start sha=' (accd0d88...) is a tree hash, not a commit. The task-start HEAD recorded in artifacts/retries/T1/q0-head (ec259f1b718ccdb9f08bba0237bfa47b2b7601a2) is a real commit and an ancestor of the implementation commit 7764bb623 (a squash that bundles four commands). The start tree differs from it only by untracked .dev package folders. design.md, CODEGRAPH.md, reflect.md and the four named test files exist at base, and design.md has `mcp-servers: []` at line 6 as the plan states. The implementation created no repo file that exists at base, so masked_paths is empty.
- Plan text verified: sha256 of the done-folder plan equals the PLAN: hash in progress.md (9f610e5d...); plan lines cited by the report (28,31-33,41,44,46,47) match. The source.md cited (.dev/issues/504/design-output.md) is the package's own source.md.
- The report notes shipped design.md evolved after execution (PR #513); items here rest on plan text and source.md only.
- No blocking items: report says 'All MINOR, none blocking'; the package has no review record under artifacts/retries.
