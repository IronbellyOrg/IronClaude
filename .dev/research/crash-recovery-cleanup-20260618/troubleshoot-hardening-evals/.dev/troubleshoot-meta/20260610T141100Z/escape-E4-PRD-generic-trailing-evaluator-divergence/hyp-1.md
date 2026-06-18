# Why-it-escaped hypothesis card: E4 PRD generic/trailing evaluator divergence

## Escape

- ID: `E4-PRD-generic-trailing-evaluator-divergence`
- Lens: runtime-entrypoint lens
- Symptom: PR #155 intended `parallel_instructions` to warn instead of halt, but normal PRD runtime uses `PrdExecutor._evaluate_gate`, not generic `pipeline.gates.gate_passed`; the PRD evaluator still treats any non-True semantic check result as fatal and ignores `SemanticCheck.advisory`.

## Hypothesis

The issue escaped because review validated the new advisory semantics against the named generic gate contract instead of proving the real runtime entrypoint for `superclaude prd run`. The change looked correct where the reviewer expected semantic gates to be evaluated (`pipeline.gates.gate_passed`), but PRD has a bespoke runtime gate path. That path consumes the same `GateCriteria.semantic_checks` data but does not share the generic evaluator implementation.

In other words, review was contract-centered but not entrypoint-centered: it checked that the generic evaluator honored `SemanticCheck.advisory`, while the production PRD command dispatches into `PrdExecutor.run()`, then `_execute_step()`, then `_evaluate_gate()`. The divergence remained hidden because the modified contract had multiple consumers and the PRD-specific consumer was not enumerated or regression-tested.

## Evidence chain

1. `superclaude prd run` constructs and calls `PrdExecutor`, not the generic pipeline executor.
   - `/config/workspace/IronClaude/src/superclaude/cli/prd/commands.py:112-141` imports `resolve_config` and `PrdExecutor`, builds config, constructs `PrdExecutor(config)`, and calls `executor.run()`.
   - The command returns early only for `--dry-run`; normal runtime proceeds through `PrdExecutor.run()`.

2. `PrdExecutor.run()` drives PRD-specific step execution.
   - `/config/workspace/IronClaude/src/superclaude/cli/prd/executor.py:526-553` iterates `_STAGE_A_STEPS` and calls `self._execute_step(step_id, step_name, builder_name)`.
   - `/config/workspace/IronClaude/src/superclaude/cli/prd/executor.py:566-589` halts the pipeline on hard failures or STRICT gate failures, so a false failure from a STRICT PRD gate can become a PRD run halt.

3. PRD gates are evaluated by the bespoke `_evaluate_gate` path.
   - `/config/workspace/IronClaude/src/superclaude/cli/prd/executor.py:741-764` resolves `gate_content`, determines step status, fetches `GATE_CRITERIA`, and calls `self._evaluate_gate(step_id, gate, gate_content)`.
   - `/config/workspace/IronClaude/src/superclaude/cli/prd/executor.py:765-770` maps a failed STRICT gate to `PrdStepStatus.HALT` and a failed non-STRICT gate to `VALIDATION_FAIL`.

4. The PRD evaluator ignores advisory semantics.
   - `/config/workspace/IronClaude/src/superclaude/cli/prd/executor.py:849-859` iterates `gate.semantic_checks`, calls each `check.check_fn(content)`, and returns `False` on any non-`True` result. There is no branch for `check.advisory`.

5. The generic evaluator does honor advisory semantics, but that is off the normal PRD runtime path.
   - `/config/workspace/IronClaude/src/superclaude/cli/pipeline/gates.py:88-110` checks `getattr(check, "advisory", False)`, logs a warning, and continues instead of returning failure.
   - `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/contract-implementations.md:14-18` independently summarizes the same divergence: PRD runtime calls `PrdExecutor._evaluate_gate`, while PR #155 made the generic `gate_passed()` honor advisory checks.

6. The A2 contract inventory explicitly identifies the review gap.
   - `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/contract-implementations.md:20-29` records the real runtime call chain and halt implications.
   - `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/contract-implementations.md:41-78` enumerates generic blocking, PRD runtime, trailing/off-path, and cosmetic-remediation semantic check consumers.
   - `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/contract-implementations.md:136-145` states the missed runtime-entrypoint verification, incomplete contract-implementation enumeration, and need to sweep every `semantic_checks` consumer.

## Why review missed it

- The fix target was named like a shared contract change (`SemanticCheck.advisory`), but the review surface appears to have been the generic implementation that already sounded canonical: `pipeline.gates.gate_passed`.
- The PRD runtime owns a parallel evaluator with the same semantic-check loop shape. Because it is inside `prd/executor.py`, it is easy to miss when searching only for the generic gate function or validating generic gate behavior.
- The symptom involved a PRD gate (`parallel_instructions`) whose data is stored in `GATE_CRITERIA`, creating a false sense that changing the data model plus generic evaluator was sufficient.
- The absence of a runtime-entrypoint proof meant no one had to demonstrate that the regression test executed the actual `superclaude prd run` path through `PrdExecutor._evaluate_gate`.

## Confidence

High. The runtime command dispatch and evaluator call chain are directly visible in current source, and the documented contract report corroborates the same off-path divergence. This hypothesis explains why a correct-looking generic advisory fix could merge while the real PRD runtime still halted on advisory semantic-check failures.
