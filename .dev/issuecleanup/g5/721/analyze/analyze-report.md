# Claim pipeline architecture analysis

## Scope and method
Target: `src/superclaude/skills/sc-issue-protocol`, the smallest package containing claim estimation, create classification, summary templates and launch rendering. Adjacent agent definitions and existing tests were read only to trace its inputs and consumers. Static architecture pass only; no source changes or runtime tests.

Codegraph: index_state=fresh, checked_at=2026-11-24T14:07:20Z; degraded: none

The graph lists three Python helpers but does not index the Markdown where the estimate is specified. Glob, Grep and Read supply the evidence for that control path. Graph call-path evidence was confirmed at the actual call to `render_prompt` in `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:815-817`; its direct consumer is prompt generation, not an independent estimator.

## Findings
1. **Medium: hours remain an unsupported scalar.** `src/superclaude/skills/sc-issue-protocol/refs/claim.md:60-73` requires hours but no per-piece breakdown, and `templates/issue-summary.md:8-10` stores one hours figure. Nothing in the inspected package requires measured active-time evidence.
2. **Medium: first sizing remains visible to the detail worker.** `refs/claim.md:31,55-60` records a first complexity guess, selects the detail tier from it and tells the worker to inspect the same scout report. Both `src/superclaude/agents/issue-worker-t1.md:21` and `issue-worker-t2.md:21` repeat that input. This verifies exposure and tier selection, not the unmeasured psychological effect on actual estimates.
3. **Medium: classification has an undefined cross-area trigger.** `refs/claim.md:71` classifies more than one subsystem as complex. Grep for subsystem, breakdown, anchoring, active time and Jev across this package found only that subsystem line, with no definition or requested research/back-test method.
4. **Medium: estimate errors change the default execution boundary.** `refs/claim.md:81-83` makes explicit pipeline choice win; otherwise a valid simple/medium feature at 16 hours or less gets full execution and a complex or over-16-hour feature gets plan-only execution. Invalid summary values fall back to plan-only; valid bugs get full execution. `templates/launch-prompt.md:22-28` makes these different permissions concrete. This is not evidence of an unauthorized launch or a security bypass.
5. **Context: create classification is also heuristic.** `refs/create.md:36` maps quick/standard/deep analysis to Simple/Medium/Complex. Changing this is conditional in the issue, not an automatic expansion of its scope.
6. **Existing coverage, not a proven fix.** `tests/skills/test_issue_protocol.py:878-927` checks the current routing text and fallback ordering. These are static assertions, not historical estimation calibration or measured active-work tests. No tests were executed.

## Recommendations and limits
Keep issue 721 open. Follow its research-first order: establish active-work evidence and Jev suitability, design independent historical back-tests, then change the estimate format, blind sizing inputs and subsystem definition and evaluate the default launch boundary. Reuse the existing summary and routing tests, adding checks for both sides of the boundary and explicit pipeline overrides. No new helper or dependency is justified by this static pass alone.

This review does not reproduce the reported single-folder misclassification, measure agent working time, run a Jev experiment or verify a historical estimate's accuracy. Those remain UNVERIFIED. No source, GitHub object, Git index or environment was changed; only this task's report directory was written.
