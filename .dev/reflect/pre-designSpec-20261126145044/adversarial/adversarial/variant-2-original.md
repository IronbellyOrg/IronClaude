reviewer: qa
model_class: haiku
findings:
  - id: F-1
    grade: Blocking
    blocking_reason: Decision
    claim: "Task 6 directs imports from jevlib that its package entry point does not export. Following that instruction literally makes runner imports fail before the runner tests can execute."
    evidence: ".dev/tasks/to-do/TASK-WF-designSpec-20261126-144507/TASK-WF-designSpec-20261126-144507.md:117; .dev/research/346-review-loop-experiments/p15/jev/jevlib/__init__.py:5"
    consequence: "The plan must name the defining submodules rather than require nonexistent package-level exports."
  - id: F-2
    grade: Blocking
    blocking_reason: Decision
    claim: "Task 6 relies on BudgetExhausted stopping the runner, but JevClient.ask catches that exception and returns status refused with error budget_exhausted. The stated generic non-ok handling would instead rerun the exhausted request and record a prompt error unless this returned error is explicitly treated as systemic."
    evidence: ".dev/tasks/to-do/TASK-WF-designSpec-20261126-144507/TASK-WF-designSpec-20261126-144507.md:119; .dev/research/346-review-loop-experiments/p15/jev/jevlib/client.py:114-117"
    consequence: "Correcting this changes required stop behavior and makes the spent-ledger acceptance check at plan line 125 achievable."
  - id: F-3
    grade: Blocking
    blocking_reason: Decision
    claim: "Task 6 replaces the specified mock-backed dry run with live=False, which returns dry_run refusal before calling any transport. The client limitation does not require this departure: the plan already identifies live=True with an injected MockTransport and fake key as an offline transport path."
    evidence: ".dev/tasks/to-do/TASK-WF-designSpec-20261126-144507/source.md:82; .dev/tasks/to-do/TASK-WF-designSpec-20261126-144507/TASK-WF-designSpec-20261126-144507.md:30; .dev/tasks/to-do/TASK-WF-designSpec-20261126-144507/TASK-WF-designSpec-20261126-144507.md:119; .dev/research/346-review-loop-experiments/p15/jev/jevlib/client.py:127-131"
    consequence: "Correcting this restores a dry run that exercises responses rather than producing refusals for every prompt."
  - id: F-4
    grade: Blocking
    blocking_reason: Missing
    claim: "The spec requires checking the whole-run estimate before the first request, but Tasks 5 and 6 specify only a per-request bound and cumulative ledger checks. T-09 can pass without implementing the whole-run preflight."
    evidence: ".dev/tasks/to-do/TASK-WF-designSpec-20261126-144507/source.md:82; .dev/tasks/to-do/TASK-WF-designSpec-20261126-144507/TASK-WF-designSpec-20261126-144507.md:103; .dev/tasks/to-do/TASK-WF-designSpec-20261126-144507/TASK-WF-designSpec-20261126-144507.md:119-124"
    consequence: "A run whose individual requests fit but whose total estimate exceeds the remaining allowance must be refused before any post."
coverage_assessment: "T-01 through T-15 are assigned acceptance checks, but the whole-run preflight required by source line 82 lacks a task and verifier. The matrix's unmatched source-change, offline-only, client-reuse and price-confirmation statements are covered by the constraints, Task 6 and Task 8 rather than being substantive omissions."
checked_and_found_clean:
  - "Sign-test cases and integer comparison match the spec."
  - "Noul boundary tests cover exact thresholds and neighboring values."
  - "Twice-failed prompts remain incorrect and stay in the accuracy denominator."
  - "Human labelling and live execution remain outside the build."
recommendations:
  - file: ".dev/tasks/to-do/TASK-WF-designSpec-20261126-144507/TASK-WF-designSpec-20261126-144507.md"
    change: "Revise Task 6 to name defining import modules, handle returned budget_exhausted explicitly, restore mock-backed dry runs, and add whole-run preflight."
    verifier: "Require runner import success, immediate exhausted-budget termination without rerun, successful no-live mock responses, and zero posts when only the aggregate estimate exceeds the remaining allowance."
