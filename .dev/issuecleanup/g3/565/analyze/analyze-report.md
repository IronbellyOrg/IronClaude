# Architecture analysis: reflect scorer boundary

## Scope and grounding
Command: `/sc:analyze src/superclaude/cli/reflect/ensemble.py --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g3/565/analyze`.

The narrow target is the ensemble's scorer boundary. Adjacent caller, subprocess implementation, tests and two guides were read to trace that boundary. Report structure follows the loaded command's scope, severity-rated findings, metrics and recommendations requirements. Reviewed checkout: `a7ae3dd30fcf88aaab655c37e94e58e121c2d863`.

Codegraph: index_state=fresh, checked_at=2026-11-24T13:08:13Z; degraded: none

Graph access: mcp; worktree_root: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup`. File layout, outline, callees, callers and two-level impact provided leads subsequently confirmed in source. No indexing or source modification occurred.

## Severity-rated findings
1. **Medium architectural defect: stub transport applies to reviewer dispatch, not the whole audit.** `src/superclaude/cli/reflect/ensemble.py:169-174` returns in-process reviewer stubs, but `:424-435` selects the normal scorer whenever no score is supplied and at least two reviewers survive. No transport check exists at this scorer boundary. `:537-555` constructs and starts a `ClaudeProcess`; `src/superclaude/cli/pipeline/process.py:140-144,218` builds `claude --print` and launches it. The public runner calls the ensemble without a synthetic scoring function at `src/superclaude/cli/reflect/runner.py:538-542`.
2. **Medium documentation/coverage mismatch:** `docs/guides/reflect-cli-tools-guide.md:136-137,153-155` advertises credit-free deterministic stub operation. The historical manual guide explicitly describes the scorer child and its stand-in at `docs/testing/v5.0.0/user/D12-reflect.md:15,26-27`. The integration test deliberately injects a score (`tests/cli/reflect/test_ensemble_stub_integration.py:14-18,108-114`) before asserting no process construction (`:152-158`), so that witness is not a demonstration that the public stub CLI avoids a scorer.

Impact is limited here to the wrapper's end-to-end stub/cost contract, not a new defect claim about the interactive `/sc:reflect` skill. Live issue #565 remains open; its 2026-11-18 comment explicitly sets lowest priority and backlog until the wrapper is used again. These findings justify keeping the issue, not starting implementation.

## Metrics and limits
- One target source file, two adjacent production files, one integration-test file and two guides inspected for this boundary; ten Python modules discovered in the reflect package.
- Static architecture review only: no tests, imports, wrapper execution, installation, environment creation, model calls or network-model experiments. GitHub reads were confined to authorized issue/PR view/list operations.
- Graph identified the production ensemble caller and test callers of the scorer. Actual selection and launch sites were checked directly; graph definition lines were not mistaken for call sites.
- UNVERIFIED: authenticated model execution, billing, current installed-console behavior, older local probe files and complete GitHub event timeline. The reported historical stand-in run is evidence recorded by the issue, not a reproduction performed here.
- An initial report Edit was blocked because the freshness hook required a Read after stub creation; reading the stub and retrying the same section succeeded. No bypass was used.

## Recommendations
Keep #565 open as still-relevant, with P3 priority and no implementation while the recorded hold remains. After the hold lifts, explicitly decide whether stub means reviewer-only or whole-run model-free behavior. For the latter, keep scoring in process and prevent synthetic evidence from certifying real-model convergence; add a model-free public dispatch regression without injected scoring, plus the existing synthetic/live separation checks. Align the current user guide and manual testing guidance, retaining historical statements as historical rather than silently rewriting old release results. No source fix, commit, staging or GitHub mutation is authorized by this analysis.
