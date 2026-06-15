# Remediation: shared-contract runtime proof and consumer sweep

## Classification

- Escape ID: `E4-PRD-generic-trailing-evaluator-divergence`
- Remediation style: high-catch-power system rule
- Scope: issue-agnostic pipeline remediation, not a PRD-specific patch
- Target failure mode: a fix changes a shared data/behavior contract, validates the named or generic implementation, but misses another runtime consumer that enforces the old contract.

## System rule

Any pipeline fix that changes the semantics of a shared contract must include a runtime-entrypoint proof and a complete consumer ledger before it can be accepted.

The review may not infer coverage from shared data-model usage, generic helper tests, or documentation that names the intended evaluator. It must prove which evaluator the user-visible runtime path actually reaches, enumerate every implementation that consumes the changed contract, and either sweep each implementation to the new semantics or explicitly justify divergence.

## Required remediation protocol

### 1. Prove the affected runtime entrypoint first

Before accepting a fix, the verification packet must identify the concrete user-visible command or runtime entrypoint that expresses the bug and trace it to the implementation that makes the decision under repair.

Required evidence:

- The command or public API being fixed.
- The constructed executor/runner/orchestrator on that path.
- The exact gate/evaluator/dispatcher function that receives the runtime artifact.
- The status or halt decision made after that evaluator returns.
- A regression test or live proof that exercises this actual path, not only a lower-level helper.

Acceptance test shape:

- Failing condition is injected at the contract boundary.
- The runtime command or command-equivalent executor path is invoked.
- The assertion checks the externally meaningful outcome: continues vs halts, blocks vs warns, remediates vs skips, records vs drops.

This prevents an off-path helper from becoming the proof of a runtime fix.

### 2. Build a consumer ledger for the changed contract

Any change to a shared contract must trigger an implementation inventory. The ledger must enumerate every code path that consumes the contract, not only the file touched by the fix.

Minimum ledger fields:

| Field | Requirement |
|---|---|
| Contract | The changed field, behavior, enum, status, artifact shape, or predicate semantics. |
| Consumer | Each loop, evaluator, dispatcher, runner, remediation path, reporter, or async/off-path checker that reads the contract. |
| Runtime role | Primary runtime, generic shared path, trailing/off-path path, remediation path, validation-only path, test fixture, or dead/legacy path. |
| Current behavior | How the consumer interprets the changed contract before and after the fix. |
| Decision | Updated to match, intentionally divergent, unaffected with proof, or removed/deprecated. |
| Evidence | File/function references and tests proving the decision. |

Search must combine semantic retrieval and exact scans. A sufficient sweep includes natural-language codebase search for the contract and exact searches for the field/function/name patterns used to consume it.

### 3. Apply unmask-and-sweep after the first fix

When the first defect is found in a contract implementation, reviewers must assume the same contract may be duplicated elsewhere until proven otherwise.

Unmask-and-sweep requires:

1. Identify all independent implementations of the same decision loop.
2. Compare their behavior against the updated contract.
3. Add parity tests for implementations that should match.
4. Add explicit divergence tests and documentation for implementations that should differ.
5. Re-run the runtime proof after all consumers are swept.

A fix is incomplete if it updates only the implementation that failed the first test while leaving duplicate consumers unclassified.

### 4. Include heterogeneous off-path review when supported by evidence

If the ledger finds asynchronous, trailing, cosmetic remediation, reporting, validation, or recovery consumers, they must be reviewed separately from the primary runtime path.

Off-path review should answer:

- Does this consumer call the same evaluator or reimplement the loop?
- Does it use the same artifact content or a transformed/compressed/sidecar artifact?
- Does it convert the contract result into a different severity, retry, remediation, or report outcome?
- Could it reintroduce the old behavior after the primary path is fixed?
- Should it be consistent with primary runtime behavior, or intentionally stricter/looser?

The direct incident may be caused by the primary runtime path, but off-path consumers are still part of the shared-contract blast radius.

### 5. Reject insufficient proof patterns

The following evidence is not sufficient for shared-contract fixes:

- A unit test for the generic helper when the runtime path has a bespoke evaluator.
- A test that only proves data wiring, such as a field being set on a model instance.
- A grep that finds the edited function but not every direct consumer of the changed field or list.
- Documentation claiming a contract behavior without proving all evaluators implement it.
- A passing fixture that bypasses the command/executor path where halt/block/remediation decisions occur.
- A review that treats trailing or remediation paths as irrelevant without first classifying them.

## Generalized checklist for future pipeline changes

Use this checklist for any change involving gate criteria, semantic checks, status enums, artifact contracts, retry/remediation state machines, trailing evaluation, validation tiers, or executor behavior.

1. Name the changed contract in one sentence.
2. Name the user-visible runtime path that must change behavior.
3. Trace that path to the concrete decision implementation.
4. List every consumer of the changed contract.
5. Classify each consumer as primary, generic, trailing/off-path, remediation, validation-only, or dead/legacy.
6. Update or explicitly exempt every live consumer.
7. Add a regression on the runtime path that previously escaped.
8. Add parity or divergence tests for duplicate consumers.
9. Verify the negative case still fails where the contract says it should fail.
10. Record the ledger in the PR or troubleshooting artifact before merge.

## Application to this escape class

For this escape class, the changed contract was not the specific PRD heuristic. The changed contract was: a semantic-check result can be advisory, meaning it can warn without failing the gate.

The generalized miss was accepting proof on one evaluator while another evaluator consumed the same contract and preserved old fatal semantics. The corrected system behavior is to require runtime-entrypoint proof plus consumer enumeration whenever a shared contract changes.

The minimum acceptable remediation for this class is therefore not “patch the PRD evaluator.” The minimum acceptable pipeline remediation is:

- Prove the real runtime entrypoint for the affected command.
- Inventory all semantic-check consumers.
- Sweep each consumer for advisory semantics or document intentional divergence.
- Add a runtime regression proving an advisory failure is non-fatal on the real path.
- Add consumer parity/divergence tests so future contract changes cannot silently land on an off-path implementation.

## Review gate to add to the pipeline

Add a mandatory “shared-contract consumer proof” gate to troubleshooting, PRD, roadmap, tasklist, and pipeline-runner fixes when a change touches a shared model or semantic contract.

Gate question:

> Does this fix change a contract consumed outside the edited function, and if so, has the PR enumerated every live consumer and proven the affected runtime entrypoint reaches an updated consumer?

Gate failure conditions:

- No runtime call-graph proof for the affected user-visible command.
- No ledger of consumers for the changed contract.
- Any live consumer remains unclassified.
- Tests prove only generic helper behavior while the runtime path uses a bespoke implementation.
- Off-path consumers are dismissed without classification.

Gate pass conditions:

- Runtime entrypoint proof is present.
- Consumer ledger is complete enough to include primary, generic, trailing/off-path, and remediation consumers where applicable.
- Every live consumer is swept or intentionally divergent with rationale.
- Tests cover the actual runtime outcome and at least one duplicate-consumer parity/divergence case.

## Expected catch power

This rule catches more than the PRD advisory case. It targets the general class of pipeline escapes where a contract is implemented in multiple places and verification attaches to the easiest or most recently edited implementation instead of the implementation reached by runtime.

It should catch future divergence involving:

- Advisory vs fatal semantic checks.
- Strict vs standard gate severity handling.
- Frontmatter and min-line enforcement differences.
- Trailing gate behavior versus blocking gate behavior.
- Cosmetic remediation dispatch that directly re-runs semantic checks.
- Recovery or validation paths that reinterpret shared status fields.
- Artifact path/content resolution differences between generic and bespoke executors.

## Source evidence used

- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/contract-implementations.md`
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/escape-E4-PRD-generic-trailing-evaluator-divergence/root-cause.md`
