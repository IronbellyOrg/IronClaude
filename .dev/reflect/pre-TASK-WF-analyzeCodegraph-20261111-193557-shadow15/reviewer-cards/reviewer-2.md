# Reflect Reviewer — Deviation Findings

**Reviewer persona**: qa (coverage / acceptance lens)
**Grounding root**: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel
**Diff scope**: n/a (pre-audit of the T1 coverage matrix and the tasklist ACs)
**Total deviations**: 0 (findings are coverage and passability gaps)

## Coverage audit

The matrix shows only the summary row "INF-001..INF-014". I could not see the individual row text. I mapped the 14 rows by their label, "R1-R7 + interface + validation", against the spec body (source.md).

Requirement-bearing spans with no matching AC in the tasklist, and so likely absent from the matrix:
- Section 2.4 items 3 and 6 (source.md:43, 46): graph rows are leads and never citations, an empty result is not a "no callers" finding, `graph:truncated`, and subagents receive `index_state`, `checked_at` and `worktree_root`. No AC covers them.
- R7 (source.md:17): the ban on `codegraph_node` file mode without `symbolsOnly:true`, and on a wildcard allowlist. Task 1 AC2 covers only the init/index/sync/explore/context ban.
- Section 2.5 (source.md:49): `return-contract.yaml` fields do not change. No AC checks it.
- Section 4 (source.md:63): keep the new section under about 25 lines. H4 measured 10 lines, but no tasklist AC requires it.

## Acceptance-criteria passability

- Task 3 AC1 (tasklist line 56) passes if the remaining `verify-sync` output names only other sessions' files. That is a non-mechanical escape clause.
- Task 3 AC2 (tasklist line 57) does not name the tests. It also passes when a failure is "reported and left unfixed", so it cannot mechanically fail. The evidence log shows 146 passed, so no harm resulted here.
- Task 2 AC2 (tasklist line 44) is byte-identical "apart from the intended additions". "Intended" is unbounded, so any diff can be declared intended.

## Adherence summary

- Spec units audited: 7 requirements (R1-R7), 5 interface subsections, 6 validation checks (a)-(f), 2 risks
- t3-test.log shows 146 passed, rc=0, which supports validation check (f).

## Notes

- I did not read the individual INF rows or the current `analyze.md`. I relied on the brief's H4 conformance claim for the 25-line limit.

## Findings block

```json
{"id":"F1","severity":"MINOR","blocking":false,"category":"missing-requirement","lens":"reflect-pre","claim":"Spec 2.4 items 3 and 6 (graph rows are leads not citations, graph:truncated, subagent hand-off of index_state) have no tasklist AC and no visible matrix row.","refs":["R2"],"citations":[{"role":"spec","path":".dev/tasks/done/TASK-WF-analyzeCodegraph-20261111-193557/source.md","line_start":43,"line_end":46,"quote":"Graph rows are leads, never citations"},{"role":"plan","path":".dev/tasks/done/TASK-WF-analyzeCodegraph-20261111-193557/TASK-WF-analyzeCodegraph-20261111-193557.md","line_start":31,"line_end":35}]}
{"id":"F2","severity":"MINOR","blocking":false,"category":"missing-requirement","lens":"reflect-pre","claim":"R7 bans codegraph_node file mode without symbolsOnly:true and wildcard allowlists; Task 1 AC covers only the init/index/sync/explore/context ban. Also the 25-line cap (spec section 4) and return-contract.yaml unchanged (2.5) have no AC.","refs":["R7"],"citations":[{"role":"spec","path":".dev/tasks/done/TASK-WF-analyzeCodegraph-20261111-193557/source.md","line_start":17,"line_end":17,"quote":"no `codegraph_node` file mode without `symbolsOnly:true`, no wildcard allowlist"},{"role":"spec","path":".dev/tasks/done/TASK-WF-analyzeCodegraph-20261111-193557/source.md","line_start":49,"line_end":49},{"role":"spec","path":".dev/tasks/done/TASK-WF-analyzeCodegraph-20261111-193557/source.md","line_start":63,"line_end":63}]}
{"id":"F3","severity":"MINOR","blocking":false,"category":"unpassable-check","lens":"reflect-pre","claim":"Task 3 ACs have escape clauses: verify-sync may fail if files belong to other sessions; pytest failures are 'reported and left unfixed', and the test set is unnamed. Neither AC can mechanically fail.","refs":[],"citations":[{"role":"plan","path":".dev/tasks/done/TASK-WF-analyzeCodegraph-20261111-193557/TASK-WF-analyzeCodegraph-20261111-193557.md","line_start":56,"line_end":57,"quote":"any failure not caused by `src/superclaude/commands/analyze.md` is reported as such and left unfixed"}]}
{"id":"F4","severity":"MINOR","blocking":false,"category":"unpassable-check","lens":"reflect-pre","claim":"Task 2 AC requires byte-identity 'apart from the intended additions' with no bound on what is intended, so any diff can be justified and the check cannot fail.","refs":["R5"],"citations":[{"role":"plan","path":".dev/tasks/done/TASK-WF-analyzeCodegraph-20261111-193557/TASK-WF-analyzeCodegraph-20261111-193557.md","line_start":44,"line_end":44,"quote":"apart from the intended additions"}]}
```

reviewer_model_self_report: claude-gw-tier1b[1m]
