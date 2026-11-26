# Issue 560 architecture analysis

## Scope and method
Read-only, quick architecture analysis of `src/superclaude/cli/eval/commands.py`, the narrowest source file containing the reported shared formatter and both callers. Read the live issue and all three comments, the two caller branches, the existing coverage integration tests, and the historical user guide. No source changes, tests, eval executions, installs, or model launches. Scope is the command label, not coverage-policy or output-directory behavior.

## Findings and evidence
1. Low impact, confirmed source defect: the shared formatter embeds `eval doctor` at `src/superclaude/cli/eval/commands.py:642-647`. Both `doctor` at `:919-921` and `eval_run` at `:1827-1829` call it on coverage failure. Consequently the run path prints the doctor label while retaining its rejection branch. Call sites were read directly, not inferred from graph definition lines.
2. Regression gap in the inspected integration tests: `tests/cli/eval/test_coverage_gate_integration.py:144-163` and `:238-266` assert failure text and rejection code, but do not distinguish the command prefix. The roster checks at `:166-194` already protect missing-pattern content.
3. Documentation coupling: `docs/testing/v5.0.0/user/D15-eval-harness.md:445-459` records the doctor prefix as observed output of run. A future fix must explain the changed diagnostic without rewriting historical observations as if a corrected run occurred.
Graph impact identifies the formatter plus the two command functions. The file outline reports 66 symbols and 23 dependent files; those counts are navigation metrics, not a complete review of all dependents. No broad restructuring is needed for this defect.

## Recommendations and verification limits
Keep issue 560 open and parked at low priority: the latest live issue comment (2026-11-18) explicitly says nobody works on the unused eval harness until it returns to use. This read-only review does not lift that hold. After an explicit release of the hold, supply caller context to the existing formatter, update both callers, add model-free assertions distinguishing doctor and run, and document the corrected prefix. Preserve the matcher roster and exit behavior; do not disable coverage enforcement or solve issues 561/562 here.
Static verification only: current runtime behavior and old retained probes were not re-executed. The live source supports the reported label defect independently of those old probes.
The first four report population Edits were stopped by the freshness hook because the newly written stub had not been Read; a bounded Read resolved that local writing check before the successful Edits. No source action was attempted.

## Codegraph
Codegraph: index_state=fresh, checked_at=2026-11-24T13:03:51Z; degraded: graph:empty
Access: mcp. Worktree root: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup`. One status call; no index writes. The callees lookup returned no callees and mentioned a fixture copy as well as the production definition; this is not used to establish absence. Source Reads establish the production formatter and both call sites.
