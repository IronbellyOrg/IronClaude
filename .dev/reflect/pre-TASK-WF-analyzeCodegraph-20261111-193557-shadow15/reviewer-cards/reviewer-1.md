# Reviewer 1 card — persona: analyzer (root-cause / deviation lens)

## Scope checked
- Spec units R1-R7 and validation (a)-(f) in source.md, traced against Tasks 1-3 and their acceptance criteria in the tasklist.
- Execution log (progress.md) and the current `src/superclaude/commands/analyze.md` (lines 30-34, 66).
- Codegraph was not used. Checks were by Read and Grep only.

## Deviation summary (spec units audited: 7 requirements)
- Fully adherent: R1, R2, R3, R4, R5, R6.
- Constraint without enforcement: R7, which has a partial gap (F1).
- Authorized expansion: 0. Necessary deviation: 0. Regression: 0.
- Drift: 1 minor (F2).
- No before-state baseline exists for a strict byte-diff check of R5. I treat that as audit-vantage context, not an executor defect.

## Observations
- R2's `access: mcp` condition is not stated in Task 1 or Task 2 of the tasklist. The shipped file does include it at analyze.md:66, so the result conforms. The plan relies on the spec section 2.4 wording rather than pinning it with an acceptance criterion (F3).
- Spec section 2.4 item 1 (`SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off` means `graph:disabled`) is delegated to the guide. The tasklist drops it. This is acceptable because the spec says the guide handles it.
- Task 1's acceptance criterion for "no `allowed-tools` key" covers the "no wildcard allowlist" half of R7.
- H3 from the T1 card (the bundled PR) is coordinator-level and not an executor deviation.

## Findings block

```json
{"id":"F1","severity":"MINOR","blocking":false,"category":"missing-requirement","lens":"reflect-pre","claim":"R7 bans codegraph_node file mode without symbolsOnly:true, but no tasklist constraint or AC states this ban. It appears only as Scan usage text, so a later edit could break it without any check failing.","refs":["R7"],"citations":[{"role":"spec","path":".dev/tasks/done/TASK-WF-analyzeCodegraph-20261111-193557/source.md","line_start":17,"line_end":17,"quote":"no `codegraph_node` file mode without `symbolsOnly:true`, no wildcard allowlist."},{"role":"plan","path":".dev/tasks/done/TASK-WF-analyzeCodegraph-20261111-193557/TASK-WF-analyzeCodegraph-20261111-193557.md","line_start":33,"line_end":33}]}
{"id":"F2","severity":"MINOR","blocking":false,"category":"other","lens":"reflect-pre","claim":"Shipped Discover step adds codegraph_node symbolsOnly calls and a path parameter, and limits codegraph_search to named-symbol targets. The spec lists only codegraph_files and codegraph_search for Discover, so this is mild unplanned elaboration.","refs":["R2"],"citations":[{"role":"spec","path":".dev/tasks/done/TASK-WF-analyzeCodegraph-20261111-193557/source.md","line_start":28,"line_end":28},{"role":"plan","path":"src/superclaude/commands/analyze.md","line_start":32,"line_end":32}]}
{"id":"F3","severity":"MINOR","blocking":false,"category":"missing-requirement","lens":"reflect-pre","claim":"R2 requires index_state fresh AND access mcp. Tasks 1 and 2 and their ACs name only index_state: fresh, so the access: mcp half is not enforced by any AC even though the shipped file includes it.","refs":["R2"],"citations":[{"role":"spec","path":".dev/tasks/done/TASK-WF-analyzeCodegraph-20261111-193557/source.md","line_start":12,"line_end":12},{"role":"plan","path":".dev/tasks/done/TASK-WF-analyzeCodegraph-20261111-193557/TASK-WF-analyzeCodegraph-20261111-193557.md","line_start":43,"line_end":43}]}
```

reviewer_model_self_report: claude-gw-tier1b
