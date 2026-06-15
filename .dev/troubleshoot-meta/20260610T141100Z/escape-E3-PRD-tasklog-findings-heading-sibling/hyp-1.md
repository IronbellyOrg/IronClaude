# Why-it-escaped hypothesis card: E3 PRD Task-Log findings heading sibling

## Lens

Runtime-entrypoint lens. This card follows the live PRD gate dispatch path rather than relying on review artifacts as the primary explanation.

## Hypothesis

PR #154 escaped because the review framed the failure as a phase-range/business-rule bug in `_check_parallel_instructions`, but the runtime entrypoint was actually a whole-file heading scanner attached to a STRICT `build-task-file` gate. The fix validated the observed final completion phase and preserved the same unscoped parser over the entire generated MDTM task file. That left sibling heading surfaces, especially Task Log placeholder headings, inside the same runtime scan domain. When the generated task file later contained `### Phase 2 - Codebase Research Findings`, the scanner treated it as an executable phase, extracted an empty section, returned a missing-parallel-instructions failure, and the STRICT PRD runtime converted that parser false positive into a HALT.

## Evidence chain

1. The live PRD step runner gates disk-resolved task-file content, not only structured phase-plan content. In `/config/workspace/IronClaude/src/superclaude/cli/prd/executor.py`, `_execute_step` resolves `gate_content` from the task directory/disk artifact and then calls `_evaluate_gate(step_id, gate, gate_content)` when the subprocess status is successful. The adjacent comments explicitly separate `gate_content` as the input for min-lines and semantic checks.

2. The PRD runtime gate evaluator is fail-closed for semantic checks. In `/config/workspace/IronClaude/src/superclaude/cli/prd/executor.py`, `_evaluate_gate` loops over `gate.semantic_checks`; any result other than `True` records a gate failure, logs it, and returns `False`. The caller then maps a failed STRICT gate to `PrdStepStatus.HALT`, and the Stage A loop halts the pipeline on STRICT-gate failure.

3. The `build-task-file` gate binds `_check_parallel_instructions` to a STRICT gate surface. In `/config/workspace/IronClaude/src/superclaude/cli/prd/gates.py`, `GATE_CRITERIA["build-task-file"]` has `enforcement_tier="STRICT"` and includes `parallel_instructions` among semantic checks. That means a parser miss in this heuristic was not merely diagnostic during the escape; it was on the live halt path.

4. The parser matched headings broadly across the whole file. In `/config/workspace/IronClaude/src/superclaude/cli/prd/gates.py`, `_check_parallel_instructions` discovers phase sections with a regex shaped as `(?:^|\n)\s*#{1,4}\s+.*Phase\s+(\d+)`, without anchoring to an executable phase-plan region or excluding Task Log sections. It then checks text until the next matched phase heading. This makes same-shaped headings outside the phase plan indistinguishable from executable phases at runtime.

5. PR #154's unit coverage targeted the observed completion-phase symptom and nearby completion-signal boundaries, not sibling heading surfaces. `/config/workspace/IronClaude/tests/cli/prd/test_gates.py` contains regression coverage for a live Phase 7 completion repro, short completion phase exemption, final work phase still checked, and `Incomplete` not being over-exempted. In the inspected test slice, there is no adversarial fixture where `## Task Log / Notes` contains `### Phase N - ... Findings` placeholder headings after otherwise valid executable phases.

6. The escape table and PR summaries confirm the same runtime interpretation. `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/defect-escape-table.md` row PRD-E06 states that loose `Phase \d` heading matching consumed Task Log placeholders and that #154 did not unmask-and-sweep parser behavior over all generated task sections. `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/pr-targets-summary.txt` lines 81-99 and `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/pr-broader-summary.txt` lines 97-112 record the second live halt on empty `Phase 2 - Codebase Research Findings` and the cost asymmetry of a hard gate. `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/timeline.md` line 22 places the subsequent escape after PR #154 and attributes PR #155 to making only `parallel_instructions` advisory.

## Why it escaped review

The review boundary stopped at the visible failing phase. PR #154 answered, "Should final completion/presentation phases be exempt?" It did not ask, "What exact text does the runtime parser scan, and what other headings in a full generated MDTM file satisfy the same regex?" Because the runtime entrypoint passes the entire generated task artifact into a broad heading regex, any sibling section that reused `Phase N` wording was in scope even though it was not an executable phase. That coupling was easy to miss if review used reduced fixtures or reasoned from the template's intended phase plan instead of the disk artifact delivered to `_evaluate_gate`.

The hard gate amplified the miss. A loose parser serving a performance/concurrency heuristic was placed on the STRICT halt path, so the expected review standard needed to be closer to parser boundary testing than business-rule testing. PR #154 added business-rule regression tests around completion bookends, but did not include a full-artifact false-positive sweep over Task Log headings or other generated heading siblings. As a result, the next sibling heading with `Phase 2` unmasked the parser-scope defect immediately.

## Pipeline that should have caught it

A runtime-entrypoint regression should have used a full generated MDTM task-file fixture as the gate input, including both executable phase-plan headings and non-executable Task Log placeholder headings. The assertion should have been that `_check_parallel_instructions` only evaluates executable work phases, or at minimum that a full valid task file with Task Log `### Phase N - ... Findings` placeholders does not fail the `build-task-file` gate. A severity review should also have compared false-positive cost against the guarded risk: a false positive HALTs a long PRD run, while missed parallel wording usually only makes the task slower.
