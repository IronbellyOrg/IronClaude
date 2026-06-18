# Remediation: Runtime-boundary contract closure gate

Escape ID: `E1-PRD-cloud-file-misuse`

## Decision

Adopt a reusable **Runtime-boundary contract closure gate** for pipeline defects and fixes.

This remediation merges the strongest parts of `rem-1` and `rem-2`:

- From `rem-1`: low implementation cost, concrete evidence card, and explicit rejection of helper-only proof.
- From `rem-2`: broader contract taxonomy, stronger negative-condition requirement, and clearer family-level sweep semantics.

The merged rule is deliberately issue-agnostic. PR #151 already addressed the observed PRD implementation defect. The durable fix is a closure rule that prevents future pipeline changes from being accepted when proof stops at source code, helper behavior, mocked argv, or a single patched symptom while the real defect lives at a runtime/process/filesystem/persisted-state/producer-consumer boundary.

## Rule

A pipeline change is not remediation-complete until it proves the edited behavior at the same runtime boundary production uses, enumerates every implementation of the affected contract across sibling pipelines, sweeps for the newly exposed failure family, and makes an explicit off-path review decision when local review does not exercise the risky boundary.

## Applicability

Require this gate before marking a pipeline remediation, troubleshoot report, reflect report, task-builder fix, validation fix, or generated-task workflow complete when any of the following are true:

1. The defect was observed through a runtime entrypoint, subprocess, CLI invocation, generated artifact, persisted state, resume path, gate, monitor, or filesystem boundary.
2. The fix changes command arguments, file delivery, artifact paths, prompt-required paths, persisted fields, generated output contracts, gate criteria, parser assumptions, environment assumptions, or producer/consumer wiring.
3. A sibling pipeline implements the same conceptual contract differently.
4. Tests or review primarily inspect helpers, command construction, mocks, markdown output, static maps, or local source surfaces rather than the failing runtime seam.
5. A single anchor bug plausibly indicates a family of related defects.

## Required closure card

Every applicable fix must include this card in the task log, review report, remediation report, or closeout artifact:

```markdown
## Runtime-boundary contract closure

### 1. Runtime-entrypoint replay
- Production entrypoint:
- Exact command or equivalent replay:
- Subprocess/external command shape, if any:
- Boundary crossed: [CLI | subprocess | filesystem | persisted state | generated artifact | gate | prompt | external tool | other]
- Input source and delivery mechanism:
- Runtime producer of the artifact/value/signal:
- Runtime consumer/gate of the artifact/value/signal:
- Relevant environment assumptions and absences:
- Same-boundary negative condition tested:
- Evidence that replay reaches the production boundary:
- If not replayed, faithful substitute and justification:

### 2. Contract-implementation enumeration
- Contract name:
- Producers:
- Consumers:
- Shared helpers / sibling pipelines checked:
- Mock fixtures or tests that claim to represent this contract:
- Forbidden, deprecated, cloud-only, local-only, runtime-only, or mock-only mechanisms:
- Classification for each implementation: [conforms | intentionally different | dead/quarantined | violating/remediated]
- Guard added or existing guard cited:

### 3. Unmask-and-sweep
- Anchor failure:
- Family-level failure shape:
- Sweep dimensions used:
- Search method/query/strategy:
- Implementation surfaces searched:
- Generated-output/runtime artifact surfaces searched:
- Additional hits:
- Disposition for each hit: [fixed now | already guarded | irrelevant with reason | follow-up with owner/path]

### 4. Review-path decision
- Does this cross a runtime/process/filesystem/persisted-state/generated-artifact/gate boundary?
- Does same-frame/local review execute that boundary directly?
- If yes, evidence:
- If no, heterogeneous/off-path review or targeted runtime smoke used:
- If Tier 1/local review is sufficient, why:
- If off-path review is used, evidence it reviewed the actual changed surface rather than an empty or foreign diff:

### 5. Closure checklist
- Runtime-entrypoint replay: PASS/FAIL/N/A
- Faithful runtime verification artifact: PASS/FAIL/N/A
- Same-boundary negative condition tested: PASS/FAIL/N/A
- Contract-implementation enumeration: PASS/FAIL
- Sibling pipeline sweep: PASS/FAIL/N/A
- Unmask-and-sweep family query: PASS/FAIL
- Mock/runtime equivalence justified: PASS/FAIL/N/A
- Heterogeneous off-path review decision: PASS/FAIL/N/A
```

A remediation cannot close while any required item is `FAIL`. `N/A` requires a one-sentence rationale tied to the boundary analysis, not convenience.

## Pass criteria

### 1. Runtime-entrypoint replay

The fix must execute, or faithfully model, the same boundary that failed in production.

Minimum evidence:

- The named entrypoint is the operator-facing or pipeline-facing entrypoint, not only a helper.
- The replay includes relevant environment presences and absences that affect behavior.
- The replay reaches the process/file/state/gate boundary where the original defect became visible.
- The result has a failure-specific assertion, not only a broad success check.
- If feasible, the verification fails on the old behavior for the same class of reason the incident exposed.

Negative conditions are mandatory when they are part of the contract: missing credentials/session tokens, uncommitted working-tree state, absent or corrupt persisted artifacts, stale paths, runtime-created dynamic filenames, empty diffs, or unavailable local files.

For this escape class, the missing evidence was a headless pipeline run or faithful subprocess replay with no session-token file mechanism reaching the Claude subprocess boundary. Generalized, the missing evidence is any runtime replay proving the real process contract accepts the implementation's inputs.

### 2. Contract-implementation enumeration

The fix must enumerate the affected contract across producers, consumers, mocks, shared helpers, and sibling implementations.

Contracts include, at minimum:

- CLI flags and subprocess arguments
- file-delivery mechanisms
- prompt-required artifact paths
- gate criteria and status enums
- generated output scanners
- persisted run/resume fields
- dynamic filename patterns
- static dispatch maps
- monitor/dead-knob surfaces
- mock fixtures that claim to represent runtime behavior

Minimum evidence:

- List every producer of the value: CLI flag, generated file, prompt section, persisted JSON field, subprocess arg, gate criterion, static map entry, monitor, recovery path, or mock fixture.
- List every consumer that interprets the value.
- Identify sibling pipelines or shared helpers that implement the same conceptual contract.
- Classify each implementation as `conforms`, `intentionally different`, `dead/quarantined`, or `violating/remediated`.
- If one sibling encodes a safer contract, compare whether other siblings should converge or document why divergence is intentional.
- Add or cite at least one guard that prevents recurrence across the contract family.

For this escape class, enumeration would have shown that roadmap/tasklist/validate already forbade local-file delivery through cloud/session-token-only file mechanisms while PRD still emitted it.

### 3. Unmask-and-sweep

The observed bug must be treated as an anchor, not a one-off.

Required sweep dimensions:

- helper-path verification vs actual entrypoint verification
- construction-time checks vs runtime subprocess semantics
- prompt/schema/gate agreement
- stdout/commentary artifacts vs disk artifacts
- run vs resume behavior
- static maps vs runtime dynamic outputs
- local filesystem paths vs remote/cloud/session-scoped mechanisms
- strict gates whose false-positive cost exceeds defect cost
- tests that can pass for the wrong reason
- mocks that bypass the interface they claim to cover
- review tools auditing the wrong diff, branch, or working-tree state

Minimum evidence:

- Search structurally similar failure modes, not only the literal token that failed.
- Include implementation and generated-output/runtime artifact surfaces when relevant.
- Record the sweep query or strategy and the resulting pass/fail classification.
- Record all hits and dispositions.
- If a second defect is unmasked, widen closure to the family-level rule rather than patching only the first symptom.

### 4. Heterogeneous off-path review decision

Local/Tier 1 review is acceptable only when it directly exercises the failing surface or the artifact explains why runtime/off-path review is unnecessary with deterministic evidence.

Escalate beyond same-frame review when any of these are true:

- CLI invokes a subprocess or external tool.
- Filesystem paths are reinterpreted by another layer.
- Generated artifacts are consumed by later gates.
- Persisted state affects resume behavior.
- Task/review machinery audits a diff, branch, or working-tree state.
- A hard gate uses heuristic parsing.
- A mock substitutes for runtime I/O.
- A sibling pipeline has a different contract for the same concept.

Acceptable off-path forms include adversarial review, independent reflect review, a separate runtime smoke/e2e reviewer, or a contract-ledger audit performed from the consumer side rather than the producer side.

If off-path review is used, it must validate that it is reviewing the actual changed surface, not an empty or foreign diff.

## Low-cost implementation path

Implement this as a checklist/template change, not a pipeline redesign:

1. Add the `Runtime-boundary contract closure` card to troubleshoot/remediation/task templates used for pipeline defects.
2. Add a reviewer checklist item: `Did the evidence execute or faithfully model the runtime boundary that failed?`
3. Add a reviewer checklist item: `Did the fix enumerate sibling implementations of the same contract?`
4. Require one grep, semantic search, or contract-ledger sweep per anchor bug for sibling/family recurrence.
5. Require an explicit off-path review decision when the failure crosses a runtime/process/filesystem/persisted-state/generated-artifact/gate boundary.

This keeps cost low: the default burden is one structured card, one same-boundary replay or faithful substitute, one contract enumeration, one family sweep, and one review-path decision. Heavyweight e2e or independent review is required only when the failing boundary is not otherwise exercised.

## Anti-patterns this gate rejects

- Unit tests that assert command construction while the real subprocess contract is never exercised.
- Review reports that prove the edited helper works but do not prove the production entrypoint uses it correctly.
- Fixes that patch one pipeline without checking sibling pipelines that implement the same contract.
- Mocks that bypass the real interface where the defect surfaced.
- Closeout evidence that says `tests pass` without naming the boundary, contract, and environment assumptions.
- Product-specific remediation that only prevents the PRD `--file` case and does not generalize to other local-vs-runtime contract mismatches.
- Literal-token sweeps that miss structural equivalents.
- Off-path review that audits an empty diff, wrong branch, or foreign working tree.

## Why this catches the original escape

The observed escape was not merely a bad file flag. It was a review-surface mismatch: verification stopped at PRD's intended local-file abstraction and helper-level command construction while production failed at the headless Claude subprocess contract.

This gate would have forced four catches before closure:

1. **Runtime replay:** a headless run or faithful subprocess replay without the relevant session credential would have exposed that the delivery mechanism failed at the actual process boundary.
2. **Contract enumeration:** comparing PRD with roadmap/tasklist/validate would have exposed PRD as the outlier in local-file delivery semantics.
3. **Family sweep:** the fix would have searched sibling contract surfaces and generated artifacts rather than stopping at the immediate PRD symptom.
4. **Off-path review:** the change crossed CLI, subprocess, filesystem-path, and headless-environment seams, so same-frame helper review would not have been enough without boundary evidence.

## Generalized catch power

This remediation catches more than the original incident because it targets the recurring failure shape:

- source-level proof that bypasses runtime behavior
- contract drift between producers and consumers
- sibling pipelines implementing the same concept differently
- mocks that make failing runtime paths unobservable
- narrowly patched anchor bugs that leave adjacent defects masked
- review tools auditing the wrong diff or state
- hard gates that fail on heuristic false positives rather than material correctness

## Evidence basis

- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/escape-E1-PRD-cloud-file-misuse/root-cause.md`
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/defect-escape-table.md`
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/pr-targets-summary.txt`
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/pr-broader-summary.txt`
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/timeline.md`
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/pipeline-artifact-audit.md`

## Success signal

A future pipeline escape of this class should be caught before merge because the closeout artifact will be unable to answer these questions without exposing the mismatch:

1. What runtime boundary actually rejects or consumes this value?
2. Which producers, consumers, mocks, and sibling implementations share the contract?
3. Where else does the same structural pattern appear?
4. Did the verification include the negative conditions that make the contract fail?
5. Who or what reviewed the off-path boundary if local tests did not execute it?
