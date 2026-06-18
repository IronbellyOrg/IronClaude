# Remediation: shared-contract runtime proof and consumer sweep

## Classification

- Escape ID: `E4-PRD-generic-trailing-evaluator-divergence`
- Remediation style: issue-agnostic review gate with high defect-catch power and low execution cost
- Scope: pipeline-review protocol, not a PRD-specific product-code patch
- Optimization focus: generality, defect-catch power, and cost containment

## System rule

Any pipeline change that modifies the semantics of a shared contract must include both:

1. A runtime-entrypoint proof showing which concrete implementation the user-visible path reaches.
2. A complete consumer ledger showing every live implementation that consumes the changed contract and the decision made for each.

Review may not infer correctness from shared model usage, an edited implementation, a generic helper test, or documentation naming the intended evaluator. If multiple evaluators, dispatchers, runners, adapters, remediation paths, or trailing/background checks consume the same contract, each live consumer must be swept for parity or explicitly documented as intentionally divergent.

## Escape class addressed

This remediation targets the general class where a shared data or behavior contract appears fixed because one implementation honors the new rule, while another runtime or off-path consumer still enforces the old rule.

For E4, the concrete contract was that a semantic-check result can be advisory, meaning it can warn without failing the gate. The generalized failure was not PRD-specific: verification attached to one evaluator while another consumer of the same semantic-check contract preserved fatal behavior.

This rule should catch future divergence involving:

- Advisory vs fatal semantic checks.
- Strict vs standard gate severity handling.
- Status enum, predicate, or artifact-shape changes.
- Frontmatter, min-line, and validation-tier enforcement differences.
- Trailing/background evaluation versus blocking runtime gates.
- Cosmetic remediation or recovery paths that re-run or reinterpret checks.
- Dispatcher, callback, or runner defaults that duplicate a decision loop.
- Artifact path/content resolution differences between generic and bespoke executors.

## Mandatory review gate

Add a mandatory **Shared-Contract Consumer Proof** gate to troubleshooting, PRD, roadmap, tasklist, validation, remediation, and pipeline-runner fixes when a change touches any shared model, field, enum, status, predicate, artifact shape, halt/warn rule, retry/remediation state, evaluator semantics, or executor behavior.

Gate question:

> Does this fix change a contract consumed outside the edited function, and if so, has the review packet enumerated every live consumer and proven that the affected runtime entrypoint reaches an updated or intentionally divergent consumer?

The gate fails if any live consumer is missing, left unknown, assumed consistent because another implementation was updated, or dismissed as off-path without classification.

## Required remediation protocol

### 1. Prove the affected runtime entrypoint first

Before accepting a fix, the review packet must identify the user-visible command, API, job, or executor path whose behavior is being fixed, then trace it to the concrete implementation that consumes the changed contract.

Required evidence:

| Required field | Standard |
|---|---|
| Entrypoint | Name the command, API, job, or runner users actually invoke. |
| Runtime call chain | List the concrete path from entrypoint to runner/orchestrator to evaluator/dispatcher. |
| Contract boundary | Name where the changed field/status/predicate/artifact is created or injected. |
| Decision implementation | Name the exact evaluator, gate, dispatcher, or callback that interprets the contract. |
| External outcome | State what users observe: continues vs halts, warns vs blocks, remediates vs skips, records vs drops. |
| Runtime regression | Provide a test, fixture, dry run, or minimal reproducer that reaches that implementation through the real entrypoint or an explicitly justified near-equivalent. |

Acceptance-test shape:

1. Inject the failing condition at the contract boundary.
2. Invoke the runtime command or command-equivalent executor path.
3. Assert the externally meaningful outcome, not merely that a model field was set.
4. Reject evidence that proves only an adjacent helper unless the call chain proves that helper is the runtime consumer for the affected path.

### 2. Build a consumer ledger for the changed contract

Any change to a shared contract must trigger an implementation inventory. The ledger must enumerate every code path that consumes the contract, not only the file touched by the fix.

Minimum ledger fields:

| Field | Requirement |
|---|---|
| Contract | The changed field, behavior, enum, status, artifact shape, predicate, or semantic rule. |
| Consumer | Each loop, evaluator, dispatcher, runner, adapter, callback, remediation path, reporter, async/off-path checker, test fixture, or legacy path that reads the contract. |
| How found | Semantic retrieval, exact grep, symbol/reference search, call graph, or fixture discovery. |
| Runtime role | Primary runtime, generic shared path, bespoke path, trailing/off-path path, remediation path, validation-only path, CI-only path, test-only fixture, dead/legacy path. |
| Current behavior | How the consumer interprets the changed contract before and after the fix. |
| Decision | Updated to match, already consistent, intentionally divergent with rationale, unaffected with proof, removed/deprecated, or out of scope with justification. |
| Evidence | File/function references and tests or reproducer proving the decision. |

Minimum search standard:

- Search by the contract symbol and by the specific field, method, enum, predicate, or status whose semantics changed.
- Search for direct loops or dispatch over the contract collection, not only imports of the model.
- Include injected/default callbacks, runner defaults, sidecar processes, and background/trailing evaluators.
- Include remediation, reporting, validation, and cosmetic paths that re-run or partially duplicate checks.
- Combine semantic codebase retrieval with exact scans for names and consumption patterns.

The ledger is complete only when each discovered consumer has a runtime role, decision, and evidence.

### 3. Apply unmask-and-sweep after the first fix

When the first defect is found in a contract implementation, reviewers must assume the same contract may be duplicated elsewhere until proven otherwise.

Unmask-and-sweep requires:

1. Identify all independent implementations of the same decision loop.
2. Compare their behavior against the updated contract.
3. Sweep every live consumer for consistent semantics, or document intentional divergence.
4. Add parity tests for implementations that should match.
5. Add divergence tests and rationale for implementations that should differ.
6. Re-run the runtime-entrypoint proof after all consumers are swept.

A fix is incomplete if it updates only the implementation that failed the first test while leaving duplicate consumers unclassified.

### 4. Review heterogeneous off-path consumers separately

If the ledger finds asynchronous, trailing, cosmetic remediation, reporting, validation, recovery, or background consumers, they must be reviewed separately from the primary runtime path.

Off-path review must answer:

- Does this consumer call the same evaluator or reimplement the decision loop?
- Does it use the same artifact content or a transformed, compressed, derived, or sidecar artifact?
- Does it convert the contract result into a different severity, retry, remediation, halt, or report outcome?
- Could it reintroduce the old behavior after the primary path is fixed?
- Should it be consistent with primary runtime behavior, or intentionally stricter/looser?

This is deliberately lightweight: one reviewer/check takes an off-path stance and asks which implementation would still fail if the edited implementation were perfect. A full adversarial workflow is only necessary for high-impact changes.

### 5. Reject insufficient proof patterns

The following are insufficient for shared-contract fixes:

- A unit test for a generic helper when the runtime path has a bespoke evaluator.
- A test that only proves data wiring, such as a field being set on a model instance.
- A grep that finds the edited function but not every direct consumer of the changed field, list, enum, or predicate.
- Documentation claiming a contract behavior without proving all live evaluators implement it.
- A passing fixture that bypasses the command/executor path where halt, block, remediation, or report decisions occur.
- A review that treats trailing, reporting, validation, or remediation paths as irrelevant without first classifying them.
- Evidence from CI/test-only consumers used as the sole proof for runtime behavior.

## Paste-ready review checklist

Add this checklist to pipeline review artifacts for shared-contract changes:

```text
Shared-Contract Consumer Proof
- Changed contract: <model/field/function/enum/status/artifact/predicate/semantic rule>
- User-visible entrypoint proven: <command/API/job/runner>
- Runtime call chain: <entrypoint -> runner/orchestrator -> concrete evaluator/dispatcher>
- Contract boundary: <where the contract value is created/injected>
- External outcome asserted: <continues/halts/warns/blocks/remediates/skips/records/drops>
- Consumer search complete: <yes/no; semantic retrieval + exact terms/tools used>
- Consumer ledger complete: <yes/no; include primary/generic/bespoke/trailing/remediation/validation/test/dead roles>
- Unmask-and-sweep complete: <updated/consistent/intentionally divergent/unaffected/removed for each live consumer>
- Runtime regression: <test/reproducer/dry run proving behavior through affected path>
- Duplicate-consumer tests: <parity/divergence tests added or justified>
- Negative case still fails where contract says it should fail: <yes/no/evidence>
- Off-path review question answered: Which consumer would still be wrong if the edited implementation were correct? <answer>
```

## Gate pass and fail conditions

### Pass conditions

A future pipeline review passes this gate only if:

1. The affected runtime entrypoint is identified before accepting test evidence.
2. The call chain reaches the concrete decision implementation that consumes the changed contract.
3. Every live consumer of the changed contract is enumerated and classified.
4. Each live consumer is updated, proven already consistent, or explicitly justified as intentionally divergent.
5. Tests cover the actual runtime outcome and at least one duplicate-consumer parity or divergence case when duplicate consumers exist.
6. Review notes distinguish helper/framework proof from product/runtime proof.
7. Negative behavior still fails where the contract says it should fail.

### Fail conditions

The gate fails when:

- No runtime call-chain proof is provided for the affected user-visible path.
- No consumer ledger exists for the changed contract.
- Any live consumer remains unclassified or marked unknown.
- Tests prove only generic helper behavior while runtime uses a bespoke implementation.
- Off-path, trailing, reporting, validation, remediation, or recovery paths are dismissed without classification.
- A shared data-model assertion is used as a substitute for proving the decision implementation.
- A consumer is intentionally divergent without rationale and a divergence test or equivalent proof.

## Cost control

This remediation is intentionally cheaper than a broad architecture rewrite. For most changes, the expected cost is:

- One concise call-chain note.
- One targeted semantic retrieval query.
- A small set of exact scans for the contract symbol and consumption patterns.
- One consumer ledger table.
- One runtime-path regression.
- Parity/divergence tests only when duplicate live consumers are found.

Do not require a full adversarial workflow for every shared-contract change. Escalate to full adversarial review only when the changed contract controls halt/block behavior, recovery/remediation, external reporting, or high-impact pipeline decisions.

## Minimum acceptable remediation for E4-class escapes

For this escape class, the minimum acceptable remediation is not “patch the PRD evaluator.” The minimum acceptable pipeline remediation is:

1. Prove the real runtime entrypoint for the affected command.
2. Inventory all semantic-check consumers.
3. Sweep each consumer for advisory semantics or document intentional divergence.
4. Add a runtime regression proving an advisory failure is non-fatal on the real path.
5. Add parity or divergence tests so future contract changes cannot silently land on only one implementation.

## Source evidence used

- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/escape-E4-PRD-generic-trailing-evaluator-divergence/rem-1.md`
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/escape-E4-PRD-generic-trailing-evaluator-divergence/rem-2.md`
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/contract-implementations.md`
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/escape-E4-PRD-generic-trailing-evaluator-divergence/root-cause.md`
