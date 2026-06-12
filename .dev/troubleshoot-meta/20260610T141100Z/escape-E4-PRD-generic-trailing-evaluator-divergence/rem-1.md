# Remediation 1: Contract-consumer runtime proof gate

## Scope

This is an issue-agnostic protocol gate for pipeline reviews. It is not a PRD patch and does not prescribe a product-code change. It prevents escapes where a fix is validated on an edited or obvious implementation while the real runtime path uses another consumer of the same contract.

## Escape class addressed

A shared contract change can appear fixed when the reviewed path honors the new contract, but another live consumer remains inconsistent. The E4 instance involved `SemanticCheck.advisory`, but the prevention rule applies to any shared data or behavior contract consumed by multiple evaluators, dispatchers, adapters, runners, or remediation paths.

## Low-cost gate

Before accepting any pipeline change that modifies a shared contract, adds a flag/field to a shared model, changes an evaluator's pass/fail semantics, or changes halt/warn behavior, the review packet must include a **Contract Consumer Runtime Proof** section with four short tables.

### 1. Runtime-entrypoint proof

Require proof for the user-visible path the fix claims to affect.

| Required field | Standard |
|---|---|
| Entrypoint | Name the command/API/job that users run. |
| Runtime call chain | List the concrete call path from entrypoint to the evaluator/dispatcher that consumes the changed contract. |
| Evaluator under test | Name the exact implementation whose behavior is asserted. |
| Regression on that path | Show a test, fixture, dry run, or minimal reproducer that reaches that evaluator through the real entrypoint or an explicitly justified near-equivalent. |

Reject evidence that only proves an adjacent framework utility unless the call chain proves that utility is the runtime evaluator for the affected path.

### 2. Contract-implementation enumeration

Require a small ledger of every consumer of the changed contract.

| Consumer | How found | Runtime role | Required action |
|---|---|---|---|
| Implementation name/path | grep, codebase retrieval, symbol/reference search, or call graph | blocking runtime, trailing/off-path, remediation, CI-only, test-only, dead | updated, already consistent, intentionally divergent with rationale, or out of scope |

Minimum search standard:

- Search by the contract symbol and the key field/method whose semantics changed.
- Search for direct loops/dispatch over the contract collection, not only imports of the model.
- Include injected/default callbacks and background/trailing evaluators.
- Include cosmetic/remediation paths that re-run or partially duplicate checks.

For E4, the relevant principle was not “PRD has a special evaluator”; it was “a semantic-check contract had multiple consumers, so all consumers needed enumeration.”

### 3. Unmask-and-sweep decision

Require a decision for every consumer in the ledger.

| Classification | Review requirement |
|---|---|
| In-scope runtime consumer | Must have implementation proof and a regression/assertion for the new contract behavior. |
| Off-path but same contract | Must either be swept for consistency or explicitly documented as intentionally different. |
| Trailing/background consumer | Must be checked for equivalent semantics when it reports, retries, remediates, or escalates failures. |
| Remediation/cosmetic consumer | Must not silently reintroduce old blocking behavior while diagnosing or dispatching fixes. |
| CI/test-only consumer | Must be identified as non-runtime and must not be used as the sole proof for runtime behavior. |

The gate fails if any live consumer is missing, left as “unknown,” or assumed consistent because another implementation was updated.

### 4. Heterogeneous off-path review

When the change affects halt/warn behavior, advisory/blocking semantics, recovery, or anything that can silently continue on degraded evidence, require one reviewer/check to take an off-path stance:

- Start from the user-visible command or job, not from the edited diff.
- Ask which implementation would still fail if the edited implementation were perfect.
- Look for duplicated loops, callback defaults, sidecar/background runners, and remediation shortcuts.
- Confirm that green tests are proving the runtime path, not only data wiring or a helper function.

This can be a lightweight checklist item in the review artifact; it does not require a full adversarial workflow unless the change is high-impact.

## Paste-ready review checklist

Add this checklist to pipeline review artifacts for shared-contract changes:

```text
Contract Consumer Runtime Proof
- Entrypoint proven: <command/API/job>
- Runtime call chain: <entrypoint -> ... -> concrete evaluator/dispatcher>
- Changed contract: <model/field/function/semantic rule>
- Consumer ledger complete: <yes/no; search terms/tools used>
- Consumers classified: <in-scope/off-path/trailing/remediation/CI-only>
- Unmask-and-sweep complete: <updated/consistent/intentionally divergent for each live consumer>
- Runtime regression: <test/reproducer/dry run proving behavior through the affected path>
- Off-path review question answered: “Which consumer would still be wrong if the edited implementation were correct?” <answer>
```

## Acceptance criteria for the remediation

A future pipeline review passes this protocol gate only if:

1. The runtime entrypoint for the affected behavior is identified before accepting test evidence.
2. Every implementation that consumes the changed contract is enumerated and classified.
3. Any duplicated or off-path consumer is swept or explicitly justified as intentionally divergent.
4. At least one regression or proof exercises the actual runtime evaluator for the claimed user-visible behavior.
5. Review notes distinguish framework/helper proof from product/runtime proof.

## Why this is low cost

The gate requires a short ledger and call-chain proof, not new architecture. It can usually be satisfied with a targeted symbol/reference search, one runtime call-chain note, and one path-specific regression. The cost is small compared with repeatedly patching symptoms when a contract change lands on only one of several consumers.
