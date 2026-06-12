# Root cause: E4 PRD generic/trailing evaluator divergence

## Verdict

The surviving merged root cause is: **PR #155 was verified as a shared `SemanticCheck.advisory` contract change on the generic gate path, but not as a PRD runtime behavior change on the actual `superclaude prd run` evaluator path.** Review accepted evidence that the data model and generic evaluator honored advisory checks, then inferred PRD coverage because PRD reused the same `GateCriteria.semantic_checks` data. That inference was false: normal PRD execution calls a bespoke evaluator, `PrdExecutor._evaluate_gate`, which consumes the same semantic checks but ignores `SemanticCheck.advisory` and returns failure on any non-`True` result.

This is not primarily a product-fix failure; it is a verification-scope failure. The missing requirement was to prove the runtime entrypoint and enumerate every consumer of the changed semantic-check contract before accepting the fix.

## Adversarial comparison of hypothesis cards

### Claims retained from hyp-1

- **Runtime-entrypoint miss is the core mechanism.** Hyp-1 correctly centers the failure on the actual command path: `superclaude prd run` constructs `PrdExecutor`, PRD step execution resolves gate content, and `_execute_step` calls `_evaluate_gate` rather than `pipeline.gates.gate_passed`.
- **The PRD evaluator is a separate implementation of the same contract.** This is stronger than merely saying the generic evaluator was off-path: PRD still consumes `GateCriteria.semantic_checks`, so the bug is duplicated contract implementation, not unrelated code.
- **A STRICT PRD gate false failure can halt the run.** This connects the evaluator mismatch to user-visible severity: `parallel_instructions` was intended to warn, but PRD STRICT failure handling can still halt.

### Claims retained from hyp-2

- **Framework-level proof was mistaken for PRD runtime proof.** Hyp-2 generalizes the miss well: review artifacts validated the changed framework path and PRD data wiring, not the runtime evaluator that matters.
- **A consumer ledger was absent.** The strongest generalizable lesson is that a shared contract change must enumerate all live consumers. The later contract report identified at least generic blocking gates, PRD runtime gates, trailing gates, and generic cosmetic-remediation semantic dispatch.
- **Green tests were not sufficient evidence.** Tests proving generic advisory behavior and PRD gate-data wiring can pass while the real PRD evaluator still fails advisory semantic checks.

### Claims weakened or rejected

- **“Trailing evaluator divergence” is not the primary runtime cause for this escape.** Trailing gates matter for the completeness of the consumer sweep, but the documented normal PRD runtime does not use the trailing gate runner. Treating trailing gates as equal to the PRD runtime path would dilute the root cause. They are evidence of why consumer enumeration was necessary, not the direct PRD failure mechanism.
- **“Cost-asymmetry reasoning substituted for entrypoint proof” is plausible but secondary.** The decisive evidence is missing runtime proof and incomplete consumer enumeration. Any design rationale about false-positive halts versus serial execution may have contributed to confidence, but it is not required to explain the escape.
- **“PRD tests passed” is only useful if scoped carefully.** The failure is not that all PRD behavior was untested; it is that the tests/review evidence did not prove an advisory failure was non-halting through `PrdExecutor._evaluate_gate` on the normal PRD runtime path.

## Evidence chain

1. The A2 contract report states that normal PRD runtime does not call the generic `pipeline/gates.py:gate_passed()` evaluator or `pipeline/trailing_gate.py:TrailingGateRunner`; it calls the bespoke `PrdExecutor._evaluate_gate()` after resolving disk artifact content.
2. The same report states why that matters: PR #155 made `SemanticCheck.advisory` and generic `gate_passed()` advisory-aware, but PRD `_evaluate_gate()` still iterates `gate.semantic_checks` and fails on any non-`True` result without checking `advisory`.
3. The runtime call-chain evidence identifies `superclaude prd run` constructing `PrdExecutor`, executing PRD-specific steps, resolving `gate_content`, and calling `self._evaluate_gate(step_id, gate, gate_content)`.
4. The PRD halt behavior evidence ties the mismatch to severity: a failed STRICT PRD gate is mapped to `HALT`, so an advisory check that should warn can remain fatal on the actual PRD path.
5. The implementation inventory identifies multiple semantic-check consumers: generic blocking gate evaluation, PRD runtime gate evaluation, trailing gate evaluation through the default/injected gate check, and generic cosmetic-remediation semantic dispatch.
6. The contract report’s meta-lessons explicitly name the failed review invariants: runtime-entrypoint verification was missed or insufficient; contract-implementation enumeration was incomplete; and every evaluator consuming `gate.semantic_checks` should have been swept after adding `SemanticCheck.advisory`.

## Root cause statement

PR #155 escaped because the verification process treated `SemanticCheck.advisory` as a single implementation contract when it was actually a multi-consumer contract. The review validated the implementation that was edited and easy to name, `pipeline.gates.gate_passed`, plus the PRD gate-data wiring that marked `parallel_instructions` advisory. It did not require proof that the production PRD entrypoint reached that evaluator, nor did it enumerate the other semantic-check loops that also consume `GateCriteria.semantic_checks`.

As a result, the fix landed on an off-path generic evaluator for the affected PRD runtime. The actual PRD evaluator kept its pre-existing behavior: any failed semantic check produced a gate failure, and STRICT PRD failures could halt the run. The escape was therefore caused by **off-path verification plus incomplete consumer enumeration for a shared semantic-check contract**.

## Generalized prevention invariant

For any change to a shared data/behavior contract such as `SemanticCheck.advisory`, review must require both:

1. **Runtime-entrypoint proof for the affected product path.** The verification packet must identify the user-visible command, the concrete evaluator it reaches, and a regression assertion on that path. For this escape, the minimum proof was: `superclaude prd run` reaches `PrdExecutor._evaluate_gate`, and an advisory `parallel_instructions` failure is observed as warning/non-halting there.
2. **Consumer-ledger sweep for the changed contract.** Every loop that consumes `semantic_checks` must be classified as in-scope, off-path but intentionally consistent, or intentionally different. A generic evaluator test is insufficient unless the runtime path under repair is proven to use that evaluator.

## Confidence

High. Both hypothesis cards converge on the same mechanism, and the A2 contract report independently documents the runtime call chain, the evaluator mismatch, the set of semantic-check consumers, and the missing verification invariants. The weaker claims are secondary explanatory context; the root cause does not depend on them.
