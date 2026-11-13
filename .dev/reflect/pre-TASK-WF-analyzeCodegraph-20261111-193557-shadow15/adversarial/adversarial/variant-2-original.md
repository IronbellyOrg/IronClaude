persona: qa
model_class: haiku
model: claude-haiku-5-5
model_observed: claude-gw-tier1b[1m]

## Findings block

```findings-v2
{"id":"F1","severity":"MINOR","blocking":false,"category":"missing-requirement","lens":"reflect-pre","claim":"Spec 2.4 items 3 and 6 (graph rows are leads not citations, graph:truncated, subagent hand-off of index_state) have no tasklist AC and no visible matrix row.","refs":["R2"],"citations":[{"role":"spec","path":".dev/tasks/done/TASK-WF-analyzeCodegraph-20261111-193557/source.md","line_start":43,"line_end":46,"quote":"Graph rows are leads, never citations"},{"role":"plan","path":".dev/tasks/done/TASK-WF-analyzeCodegraph-20261111-193557/TASK-WF-analyzeCodegraph-20261111-193557.md","line_start":31,"line_end":35}]}
{"id":"F2","severity":"MINOR","blocking":false,"category":"missing-requirement","lens":"reflect-pre","claim":"R7 bans codegraph_node file mode without symbolsOnly:true and wildcard allowlists; Task 1 AC covers only the init/index/sync/explore/context ban. Also the 25-line cap (spec section 4) and return-contract.yaml unchanged (2.5) have no AC.","refs":["R7"],"citations":[{"role":"spec","path":".dev/tasks/done/TASK-WF-analyzeCodegraph-20261111-193557/source.md","line_start":17,"line_end":17,"quote":"no `codegraph_node` file mode without `symbolsOnly:true`, no wildcard allowlist"},{"role":"spec","path":".dev/tasks/done/TASK-WF-analyzeCodegraph-20261111-193557/source.md","line_start":49,"line_end":49},{"role":"spec","path":".dev/tasks/done/TASK-WF-analyzeCodegraph-20261111-193557/source.md","line_start":63,"line_end":63}]}
{"id":"F3","severity":"MINOR","blocking":false,"category":"unpassable-check","lens":"reflect-pre","claim":"Task 3 ACs have escape clauses: verify-sync may fail if files belong to other sessions; pytest failures are 'reported and left unfixed', and the test set is unnamed. Neither AC can mechanically fail.","refs":[],"citations":[{"role":"plan","path":".dev/tasks/done/TASK-WF-analyzeCodegraph-20261111-193557/TASK-WF-analyzeCodegraph-20261111-193557.md","line_start":56,"line_end":57,"quote":"any failure not caused by `src/superclaude/commands/analyze.md` is reported as such and left unfixed"}]}
{"id":"F4","severity":"MINOR","blocking":false,"category":"unpassable-check","lens":"reflect-pre","claim":"Task 2 AC requires byte-identity 'apart from the intended additions' with no bound on what is intended, so any diff can be justified and the check cannot fail.","refs":["R5"],"citations":[{"role":"plan","path":".dev/tasks/done/TASK-WF-analyzeCodegraph-20261111-193557/TASK-WF-analyzeCodegraph-20261111-193557.md","line_start":44,"line_end":44,"quote":"apart from the intended additions"}]}
```

calibration:
  per_finding:
    F1: 0.6
    F2: 0.65
    F3: 0.75
    F4: 0.7
