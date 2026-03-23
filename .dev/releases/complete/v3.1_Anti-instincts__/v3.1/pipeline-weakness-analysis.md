# Pipeline Weakness Analysis: v3.1 Anti-Instinct Gate

**Analyst**: Claude Opus 4.6 (1M context)
**Date**: 2026-03-21
**Input**: v3.1 merged gap analysis, roadmap CLI pipeline source, sprint executor source, skill/command definitions
**Method**: Source analysis + adversarial self-debate

---

## Executive Summary

The v3.1 gap analysis revealed that all anti-instinct gate components were correctly implemented in isolation but completely disconnected from the production sprint loop. This analysis identifies 5 pipeline weaknesses that allowed this class of failure to occur or go undetected.

---

## Weakness 1: No Cross-Boundary Call-Chain Gate

**Description**: The roadmap pipeline validates individual step outputs (via `GateCriteria` checks on file content) but never validates that components produced by one pipeline context (roadmap) are actually callable from another context (sprint). The pipeline assumes that if each step's output file passes its gate, the system works end-to-end. There is no gate that verifies cross-boundary wiring between the roadmap-produced artifacts and the sprint executor that consumes them.

**Evidence**: BUG-001 through BUG-003. `execute_sprint()` never calls `execute_phase_tasks()`. The anti-instinct hook, TurnLedger integration, and ShadowGateMetrics -- all produced by the v3.1 roadmap phases -- exist in `execute_phase_tasks()` but are unreachable from the production entry point. The wiring-verification step (`run_wiring_analysis`) scans Python files for orphan modules, unwired callables, and unregistered dispatch entries via AST analysis, but it analyzed the wrong directory (`config.output_dir.parent` -- the release directory containing markdown artifacts, not the `src/` tree). It found 0 files to analyze and reported 0 findings.

**Mechanism**: The roadmap pipeline's wiring-verification step (step 9) runs `run_wiring_analysis()` against the output directory (markdown artifacts), not against the Python source tree where the actual wiring gap exists. The step's `source_dir` is set to `config.output_dir.parent`, which points to the release artifact directory. Even if it pointed at `src/`, the AST-based static analysis looks for orphan modules and unwired callables -- not for "function A should call function B but doesn't." The gap between `execute_sprint()` and `execute_phase_tasks()` is a missing call, not a dead import or orphan module.

**Severity**: CRITICAL

**Proposed Fix**: Add a "call-chain reachability" gate that takes a list of expected production entry points and verifies (via static analysis or explicit assertion) that specified downstream functions are reachable from those entry points. For the sprint executor specifically: assert that `execute_sprint()` reaches `execute_phase_tasks()`, `run_post_task_anti_instinct_hook()`, and `build_kpi_report()` in its call graph. This could be a new gate type alongside the existing wiring-verification.

---

## Weakness 2: Wiring Verification Targets Wrong Directory

**Description**: The wiring-verification step in the roadmap executor passes `config.output_dir.parent` as the `source_dir` to `run_wiring_analysis()`. This points to the release artifact directory (containing `.md` files), not to the Python source tree (`src/superclaude/`). The analyzer therefore finds 0 Python files, analyzes nothing, and reports a clean pass.

**Evidence**: The wiring-verification output from the v3.1 run shows `files_analyzed: 0`, `files_skipped: 0`, `total_findings: 0`. This is a vacuous pass -- the gate passed because it had nothing to check. The v3.1 merged gap analysis notes that all infrastructure components exist but none are reachable from `execute_sprint()`.

**Mechanism**: In `roadmap/executor.py` line 429: `source_dir = config.output_dir.parent if hasattr(config, 'output_dir') else Path(".")`. This resolves to the release directory (e.g., `.dev/releases/complete/v3.1_Anti-instincts__/`), which contains only markdown files. The wiring analyzer's `_collect_python_files()` finds nothing, so all three analysis passes (unwired callables, orphan modules, unregistered registries) return empty lists. The gate passes with 0 findings, which is indistinguishable from "all wiring is correct."

**Severity**: CRITICAL

**Proposed Fix**: The wiring-verification step should target the actual Python source tree (`src/` or the project root). This requires either: (a) adding a `source_root` field to `RoadmapConfig` that points to the project's Python source, or (b) having the wiring-verification step discover the source root by walking up from `config.output_dir` to find `src/` or `pyproject.toml`. Additionally, a 0-files-analyzed result should be treated as a WARNING, not a silent PASS.

---

## Weakness 3: No Production-Path Integration Test Gate

**Description**: The roadmap pipeline produces test files as part of its output (8 test files for v3.1), but the pipeline has no gate that verifies these tests actually exercise the production code path. The pipeline checks that test files exist and pass their own gates, but never runs the tests or validates their coverage target. This allowed a test suite that exclusively exercised `execute_phase_tasks()` (the unreachable path) while `execute_sprint()` (the production path) remained untested.

**Evidence**: BUG-008. All 8 test files exist and presumably pass their format gates. However, "No integration test verifies that `execute_sprint()` invokes TurnLedger, ShadowGateMetrics, or gate hooks. Current tests only cover `execute_phase_tasks()` path." The roadmap pipeline's test-strategy step generates a testing philosophy document but does not validate that the generated tests cover the actual production dispatch path.

**Mechanism**: The pipeline's TEST_STRATEGY_GATE validates the test-strategy.md file for structure (frontmatter fields, minimum lines, semantic checks). It does not validate that the test files generated during implementation actually test the right code paths. The test-strategy artifact describes *what should be tested*, but the pipeline has no feedback loop to verify that the implementation's tests match the strategy. The spec-fidelity step compares roadmap against spec, not implementation against spec.

**Severity**: HIGH

**Proposed Fix**: Add a post-implementation "test coverage audit" gate that: (1) identifies the production entry points from the roadmap/spec, (2) scans test files for references to those entry points, and (3) flags when production entry points have no test coverage. This is a lighter-weight alternative to actually running tests (which may not be feasible in the roadmap pipeline context).

---

## Weakness 4: Spec-Fidelity Checks Roadmap-vs-Spec, Not Implementation-vs-Spec

**Description**: The spec-fidelity step (step 8 in the roadmap pipeline) compares the *roadmap* against the *spec* to find deviations. It does not compare the *implementation* against either. This means the pipeline can certify a roadmap as spec-faithful even when the implementation diverges from both. The v3.1 roadmap correctly specified that `execute_sprint()` should wire TurnLedger and delegate to per-task hooks, but the implementation did not follow through -- and no pipeline gate caught this.

**Evidence**: BUG-001 through BUG-007 all represent implementation-vs-spec gaps, not roadmap-vs-spec gaps. The spec-fidelity report from v3.1 found 10 deviations between roadmap and spec (DEV-001 through DEV-010), including DEV-007 which noted "no explicit KPI integration task" in the roadmap. However, even DEV-007 was rated MEDIUM and described a roadmap omission, not an implementation failure. The actual CRITICAL bugs (execute_sprint not calling execute_phase_tasks) are invisible to spec-fidelity because that step doesn't look at code.

**Mechanism**: The spec-fidelity step receives `config.spec_file` and `merge_file` (roadmap.md) as inputs. It builds a prompt comparing these two documents. The convergence engine runs structural checkers and a semantic layer, both operating on the spec and roadmap text. At no point does any checker examine `src/superclaude/cli/sprint/executor.py` to verify that the roadmap's instructions were actually followed in code. The pipeline's scope ends at roadmap generation; implementation verification is outside its purview.

**Severity**: HIGH

**Proposed Fix**: This is partly by design -- the roadmap pipeline generates a roadmap, not an implementation. However, the pipeline could include a "post-implementation spec-fidelity" mode (invoked separately, after sprint execution) that compares implementation artifacts against the spec. Alternatively, the sprint executor itself should include a self-check: after completing all phases, verify that specified integration points are actually wired. The existing `run_wiring_analysis()` infrastructure is the right vehicle for this, if pointed at the correct directory.

---

## Weakness 5: Dual Execution Model Not Surfaced in Pipeline Artifacts

**Description**: The sprint executor has two execution models: `execute_sprint()` (per-phase subprocess, production entry point) and `execute_phase_tasks()` (per-task subprocess with hooks). The roadmap pipeline's extraction and generation steps did not surface this architectural split, so the v3.1 roadmap targeted `execute_phase_tasks()` without noting that it is unreachable from `execute_sprint()`. No pipeline stage requires explicit mapping of "which function is the production entry point" vs "which function is the integration target."

**Evidence**: The merged gap analysis root cause: "Dual execution context confusion: The spec identified the dual context (standalone roadmap vs sprint-invoked) but the sprint executor's internal dual architecture (per-phase vs per-task) was not surfaced in the spec or roadmaps." The extraction step did not extract the architectural constraint that `execute_sprint()` is the production entry point. The generation step produced a roadmap that correctly targeted `execute_phase_tasks()` for hook integration but did not include a task for wiring `execute_sprint()` to delegate to it.

**Mechanism**: The extraction prompt (`build_extract_prompt`) focuses on requirements, domain analysis, and complexity scoring from the spec file. It does not direct the LLM to identify existing architectural constraints in the codebase (e.g., "the production entry point is X, which currently uses model Y"). The generate prompt (`build_generate_prompt`) produces milestones and tasks from the extraction, but without knowledge of the existing code architecture, it cannot flag that the integration target differs from the production entry point. The anti-instinct audit (obligation scanner, integration contracts, fingerprint coverage) checks the roadmap for completeness against the spec, not against the codebase's actual dispatch architecture.

**Severity**: HIGH

**Proposed Fix**: Enhance the extraction step to include a "codebase architecture scan" sub-step that identifies: (a) production entry points (functions called by CLI commands or main loops), (b) the current execution model, and (c) any existing but disconnected infrastructure. This context should be passed to the generation step so the roadmap includes explicit wiring tasks between the production entry point and the integration target. The anti-instinct audit's integration contracts checker should also verify that the roadmap maps each new component to its production call site, not just to any function.

---

## Adversarial Self-Debate

### Weakness 1: No Cross-Boundary Call-Chain Gate

**Challenge**: Is this really a pipeline weakness, or is it a spec/implementation issue? The pipeline generates a roadmap -- it doesn't implement code. Asking the roadmap pipeline to verify call chains is like asking a blueprint reviewer to verify the building was built correctly.

**Rebuttal**: Fair point. However, the pipeline *does* include a wiring-verification step that runs AST analysis on Python code. The infrastructure for code-level verification exists; it just targets the wrong scope. The pipeline has already crossed the boundary from "document review" to "code analysis" -- it just does it incorrectly.

**Verdict**: VALID weakness. The pipeline includes a code analysis step but it's misconfigured. Confidence: HIGH.

**Practical?**: A call-chain reachability check is implementable via AST analysis (follow function calls from entry point, check if target is reachable). The `wiring_gate.py` module already does AST parsing. The fix is proportionate. Confidence: HIGH.

---

### Weakness 2: Wiring Verification Targets Wrong Directory

**Challenge**: Could the pipeline reasonably have caught this? The wiring verification was designed as a trailing gate for roadmap artifacts. Maybe it was intentionally pointed at the artifact directory.

**Rebuttal**: The wiring-verification step analyzes Python files for unwired callables and orphan modules. It makes no sense to run this on a directory of markdown files. The 0-files-analyzed result is a clear indicator that the configuration is wrong. A non-vacuous gate would have required at least 1 file to analyze.

**Verdict**: VALID weakness. This is a clear misconfiguration, not a design choice. Confidence: HIGH.

**Practical?**: Pointing `source_dir` at the project root or `src/` is trivial. Adding a minimum-files-analyzed threshold to prevent vacuous passes is equally straightforward. Confidence: HIGH.

---

### Weakness 3: No Production-Path Integration Test Gate

**Challenge**: Is this really a pipeline weakness? The roadmap pipeline generates test strategy documents, not test implementations. Asking it to validate test coverage is asking it to do something after its scope ends.

**Rebuttal**: Partially valid. The pipeline's scope is roadmap generation. However, the pipeline does include a test-strategy step that defines what should be tested. If the pipeline can specify "test X," it can also check whether the roadmap includes tasks that target the production path. The weakness is that the test-strategy step doesn't flag when the roadmap's test tasks target a non-production code path.

**Verdict**: PARTIALLY VALID. The pipeline can't run tests, but it could validate that the roadmap's test plan targets production entry points. Downgrade from a pipeline weakness to a roadmap content gap that the pipeline could detect with better semantic checks. Confidence: MEDIUM.

**Practical?**: Adding a semantic check to the test-strategy gate that verifies "production entry point" is mentioned in test targets is feasible but requires the extraction step to identify production entry points first (ties to Weakness 5). Confidence: MEDIUM.

---

### Weakness 4: Spec-Fidelity Checks Roadmap-vs-Spec, Not Implementation-vs-Spec

**Challenge**: This is by design. The roadmap pipeline generates a roadmap. It cannot be expected to validate an implementation that doesn't exist yet at pipeline execution time.

**Rebuttal**: Correct for the initial roadmap run. But the v3.1 execution happened *after* implementation -- the gap analysis was run post-implementation. The pipeline's validation subsystem (invoked via `superclaude roadmap validate`) runs after implementation. If the validate step also only checks roadmap-vs-spec, then the entire pipeline has a blind spot for implementation fidelity.

**Verdict**: PARTIALLY VALID. For the initial roadmap generation, this is by design. For the post-implementation validation pass, it is a real gap. Refine: the weakness is that the post-implementation validation does not include an implementation-vs-roadmap check. Confidence: MEDIUM.

**Practical?**: An implementation-vs-roadmap check requires code analysis and is significantly more complex than document comparison. More practical: the sprint executor itself should have a self-check. Confidence: LOW for pipeline fix, HIGH for sprint self-check.

---

### Weakness 5: Dual Execution Model Not Surfaced in Pipeline Artifacts

**Challenge**: The extraction step parses a spec file, not source code. It cannot discover the sprint executor's internal architecture. This is a spec authoring issue, not a pipeline issue -- the spec should have documented the dual execution model.

**Rebuttal**: The spec did identify the dual context (standalone roadmap vs sprint-invoked). But the sprint executor's *internal* dual model (per-phase vs per-task) is a codebase concern, not a spec concern. The pipeline's extraction step could be enhanced to also scan the target codebase and identify architectural constraints. The existing prompt infrastructure supports this (the prompt builder can embed file content).

**Verdict**: VALID weakness. The pipeline extracts from the spec document but not from the codebase. This creates a systematic blind spot for architectural constraints that exist in code but not in the spec. Confidence: HIGH.

**Practical?**: Adding a codebase scan to the extraction step is feasible but significantly increases scope and cost (more Claude turns, more context). A lighter approach: require the spec to include a "Codebase Architecture" section that documents production entry points. The pipeline could then check for this section's presence. Confidence: HIGH for the lighter approach.

---

## Final Validated Weaknesses

| # | Name | Severity | Self-Debate Confidence | Retained? |
|---|------|----------|----------------------|-----------|
| 1 | No Cross-Boundary Call-Chain Gate | CRITICAL | HIGH | YES |
| 2 | Wiring Verification Targets Wrong Directory | CRITICAL | HIGH | YES |
| 3 | No Production-Path Integration Test Gate | HIGH | MEDIUM | YES (refined) |
| 4 | Spec-Fidelity Scope Gap (Post-Implementation) | HIGH | MEDIUM | YES (refined) |
| 5 | Dual Execution Model Not Surfaced in Extraction | HIGH | HIGH | YES |

### Summary of Refinements

- **Weakness 3** refined: The core issue is not that the pipeline should run tests, but that the pipeline's test-strategy gate has no semantic check verifying that test targets map to production entry points. The fix should be a semantic check enhancement, not a test runner.
- **Weakness 4** refined: The initial roadmap generation scope is correct. The gap is in the post-implementation validation pass (`superclaude roadmap validate`), which should include an implementation-vs-roadmap comparison. Alternatively, the sprint executor should include a post-sprint self-check.
- All 5 weaknesses are retained. None were rejected during self-debate.

### Root Cause Chain

The 5 weaknesses form a chain of missed opportunities:

1. **Extraction** did not surface the codebase's dual execution model (W5)
2. **Generation** therefore produced a roadmap targeting the wrong function (consequence of W5)
3. **Spec-fidelity** validated roadmap-vs-spec but not implementation-vs-roadmap (W4)
4. **Wiring-verification** analyzed 0 files due to wrong directory (W2)
5. **No call-chain gate** existed to catch the missing `execute_sprint()` -> `execute_phase_tasks()` link (W1)
6. **Test-strategy** did not verify tests target the production path (W3)

Each weakness represents a point where the pipeline could have detected the v3.1 bugs but did not. Fixing any one of them would likely have caught the issue.
