# Why-it-escaped hypothesis card: E2 PRD completion-phase false positive

## Lens

runtime-entrypoint lens

## Escape

- ID: `E2-PRD-completion-phase-false-positive`
- Symptom: STRICT `parallel_instructions` gate halted a live heavyweight PRD `build-task-file` run because the final sequential completion/presentation Phase 7 lacked parallel keywords.
- Fix reference: PR #154 / `e97aa4fd2a9d317abdc19f6ce2b5ccd35497df0e`

## Hypothesis

This escaped review because verification stopped at the semantic helper contract instead of exercising the actual PRD runtime entrypoint with a generated heavyweight task file. The runtime path evaluates `build-task-file` output through the disk-resolved gate artifact, looks up `GATE_CRITERIA["build-task-file"]`, runs the `parallel_instructions` semantic check, and, at the time of the escape, converted any failure under the STRICT `build-task-file` gate into `PrdStepStatus.HALT`. That made a parser-scope mismatch operationally fatal.

Review treated “later phases” as equivalent to “parallelizable work phases.” The actual generated heavyweight template had a different semantic boundary: Phase 1 was setup, Phases 2-6 were executable parallel work, and Phase 7 was the sequential anti-orphaning completion/presentation bookend. The pre-fix implementation did not encode that runtime/template contract. It found every heading matching `Phase <number>`, filtered only `>= 2`, and required a parallel keyword in each section. As a result, the final completion phase was indistinguishable from a missing-parallelism work phase.

The likely review blind spot was not the absence of any tests, but the absence of an entrypoint-shaped fixture. The existing pre-fix unit tests covered a small synthetic pass case with Phase 2 and Phase 3 containing parallel keywords and a small synthetic failure case where Phase 2 lacked them. They did not model the full generated 7-phase heavyweight artifact or assert that setup/completion bookends are outside the executable-work-phase scope. The docstring also said “phases 2-5,” while the implementation checked every phase `>=2`; because no invariant connected parser scope to template phase semantics, that contradiction remained review-visible but non-failing.

## Evidence chain

1. Runtime dispatch made this helper failure fatal. In `/config/workspace/IronClaude/src/superclaude/cli/prd/executor.py`, the step runner resolves disk content for gate evaluation, retrieves `GATE_CRITERIA.get(step_id)`, calls `_evaluate_gate`, and changes a successful step to `PrdStepStatus.HALT` when a STRICT gate fails. This is the runtime path that turned the semantic-check false positive into a live run halt.

2. The `build-task-file` gate is the runtime attachment point. In `/config/workspace/IronClaude/src/superclaude/cli/prd/gates.py`, `GATE_CRITERIA["build-task-file"]` is `STRICT` and includes the `parallel_instructions` semantic check. In the pre-PR #154 version from `10723863`, that semantic check was not advisory and therefore participated in the fatal STRICT gate outcome.

3. The pre-fix checker scoped by phase number, not phase role. `git show 10723863:src/superclaude/cli/prd/gates.py` shows `_check_parallel_instructions` documented as checking “phases 2-5,” but implemented by finding phase headings, filtering `int(phase) >= 2`, and requiring one of `parallel`, `concurrent`, `simultaneously`, or `batch` in every such section. There was no recognition of a final completion/presentation bookend.

4. The live failure was specifically a generated-template semantic mismatch, not a truly serial work phase. `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/pr-targets-summary.txt` states that Phases 2-6 were parallel work phases and that only Phase 7, “Present to User & Complete Task,” lacked parallel keywords because it was sequential by anti-orphaning convention. The same summary records the fatal message: `Phase 7 missing parallel execution instructions (expected one of: parallel, concurrent, simultaneously, batch)`.

5. The existing tests before the fix were too small to exercise the runtime template boundary. `git show 10723863:tests/cli/prd/test_gates.py` shows `TestCheckParallelInstructions` had a passing fixture with Phase 1 setup plus Phase 2/3 work phases, and a failing fixture with Phase 2 missing keywords. It lacked a generated 7-phase heavyweight fixture with a sequential final presentation/completion phase.

6. The defect table independently classifies the escape as a missed template-phase contract. `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/defect-escape-table.md` row `PRD-E05-final-phase-false-positive` says the pipeline missed that work phases are parallel while setup/completion bookends are intentionally sequential, and that the check docstring said phases 2-5 while implementation checked every phase `>=2`.

7. The broader timeline confirms this happened in live runtime, not only static review. `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/timeline.md` records PR #154 as a PRD `build-task-file` gate false positive that halted a live heavyweight run on final sequential completion/presentation Phase 7.

## Why review missed it

- Review looked at the helper-level requirement “later phases mention parallelism,” but did not replay the runtime entrypoint contract: generated task file -> disk-resolved gate content -> STRICT `build-task-file` gate -> HALT on semantic failure.
- The fixtures represented generic phase snippets, not the actual heavyweight PRD phase topology with setup, middle executable work, and final completion/presentation.
- The parser used a syntactic boundary (`Phase N`, `N >= 2`) while the template used a semantic boundary (middle work phases only). No invariant test forced those boundaries to agree.
- The docstring/implementation mismatch was not converted into an executable assertion. “Phases 2-5” in documentation did not prevent the implementation from checking Phase 7.
- The gate severity amplified the review miss: a brittle keyword heuristic was attached to a STRICT runtime gate, so one false positive halted a long live run instead of surfacing as an advisory warning.

## Pipeline check that should have caught it

A runtime-entrypoint regression should have run the PRD `build-task-file` gate against a live/generated heavyweight 7-phase task-file fixture:

- Phase 1 setup without parallel keyword: pass as setup bookend.
- Phases 2-6 executable work with parallel/concurrent/batch language: pass as work phases.
- Phase 7 `Present to User & Complete Task` without parallel keyword: pass as sequential completion bookend.
- A final non-completion work phase without a parallel keyword: fail, proving the exemption does not over-broaden.

That fixture would align parser scope with heavyweight template phase semantics and would have failed before PR #154.
