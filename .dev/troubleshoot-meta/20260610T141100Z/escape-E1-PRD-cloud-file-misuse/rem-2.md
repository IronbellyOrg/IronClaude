# Remediation 2: Runtime-boundary contract closure rule

## Remediation style

High-catch-power system rule. This is an issue-agnostic pipeline remediation, not a PRD patch.

## Rule

A pipeline change is not review-complete until it proves the edited behavior at the same runtime boundary that production uses, enumerates every implementation of the affected contract across sibling pipelines, and sweeps for the newly exposed failure family before closure.

This rule applies to any pipeline surface that crosses a CLI, subprocess, filesystem, persisted-state, generated-artifact, gate, prompt, or producer/consumer boundary. It is intentionally broader than the PRD `--spec` incident.

## Required closure gates

### 1. Runtime-entrypoint replay

For every pipeline bug or feature whose behavior is observable through a CLI/runtime entrypoint, the remediation must include a runtime-entrypoint replay card and at least one verification artifact that executes or faithfully models the production boundary.

The card must name:

- operator-facing command or entrypoint
- subprocess command shape, if any
- relevant environment assumptions and absences
- input source and delivery mechanism
- runtime producer of the artifact or signal
- runtime consumer/gate of that artifact or signal
- whether tests/mocks exercise the same boundary or bypass it

A unit test that only validates helper output, argv construction, prompt text, static maps, or mocked stream content is insufficient when the failure can occur after that helper at the real process, filesystem, resume-state, or gate boundary.

Minimum acceptance standard:

- The verification must fail on the old behavior for the same class of reason the incident exposed, or the report must explicitly justify why faithful modeling is the highest safe substitute.
- The environment must include meaningful negative conditions, such as missing credentials/session tokens, uncommitted working-tree state, absent/corrupt persisted artifacts, stale paths, or runtime-created dynamic filenames when those conditions are part of the contract.

### 2. Contract-implementation enumeration

For each affected contract, the remediation must enumerate all known producers, consumers, and sibling implementations before declaring the fix complete.

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

The enumeration must classify each implementation as one of:

- conforms to the contract
- intentionally different, with rationale
- dead/unconsumed and removed or explicitly quarantined
- violating and remediated

Minimum acceptance standard:

- A sibling pipeline or adjacent implementation cannot remain unexamined merely because the current defect was observed in one pipeline.
- If one sibling already encodes a safer contract, the report must compare whether other siblings should converge or document why divergence is intentional.

### 3. Unmask-and-sweep after the anchor bug

Finding an anchor bug must trigger a family sweep before closure. The sweep must search for structurally similar failure modes, not only instances of the literal token that failed.

Required sweep dimensions:

- helper-path verification vs actual entrypoint verification
- construction-time checks vs runtime subprocess semantics
- prompt/schema/gate agreement
- stdout/commentary artifacts vs disk artifacts
- run vs resume behavior
- static maps vs runtime dynamic outputs
- local filesystem paths vs remote/cloud/session-scoped mechanisms
- strict gates whose false-positive cost exceeds the defect cost
- tests that can pass for the wrong reason
- mocks that bypass the interface they claim to cover

Minimum acceptance standard:

- The report must include the sweep query/strategy and the resulting pass/fail classification.
- If a second defect is unmasked, closure must widen to the family-level rule rather than patching only the first symptom.

### 4. Heterogeneous off-path review when the boundary is risky

If a change crosses more than one runtime seam, or if prior evidence shows same-frame review missed the class, the pipeline must include heterogeneous off-path review or explain why it is unnecessary.

Escalate beyond same-frame review when any of these are true:

- CLI invokes a subprocess or external tool
- filesystem paths are reinterpreted by another layer
- generated artifacts are consumed by later gates
- persisted state affects resume behavior
- task/review machinery audits a diff, branch, or working-tree state
- a hard gate uses heuristic parsing
- a mock substitutes for runtime I/O
- a sibling pipeline has a different contract for the same concept

Acceptable off-path review forms include adversarial review, independent reflect review, a separate runtime smoke/e2e reviewer, or a contract-ledger audit performed from the consumer side rather than the producer side.

Minimum acceptance standard:

- Tier 1 remains acceptable only when the report proves the runtime boundary is narrow and directly exercised.
- If off-path review is used, it must validate that it is looking at the actual changed surface, not an empty or foreign diff.

## Pipeline implementation requirement

Add a reusable remediation checklist section to troubleshoot/debug/task outputs for pipeline defects:

```markdown
## Runtime-boundary contract closure

- Runtime-entrypoint replay card: PASS/FAIL/N/A
- Faithful runtime verification artifact: <path or command evidence>
- Contract-implementation enumeration: PASS/FAIL
- Sibling pipeline sweep: PASS/FAIL/N/A
- Unmask-and-sweep family query: PASS/FAIL
- Heterogeneous off-path review: PASS/FAIL/N/A, with rationale
- Same-boundary negative condition tested: PASS/FAIL/N/A
- Mock/runtime equivalence justified: PASS/FAIL/N/A
```

A remediation cannot be marked complete while any required item is FAIL. N/A requires a one-sentence rationale tied to the boundary analysis, not convenience.

## Why this would have caught the escape

The observed escape was not just a bad file flag. It was a review-surface mismatch: tests validated intended command construction while production failed at the headless subprocess contract. The runtime-entrypoint replay gate would have required a headless run or faithful subprocess replay without the relevant session credential. The contract enumeration gate would have compared PRD against roadmap/tasklist/validate and exposed the inconsistent local-file delivery mechanism. The unmask sweep would have searched sibling contract surfaces instead of stopping at the immediate PRD symptom. Off-path review would have been required because the change crossed CLI, subprocess, filesystem-path, and headless-environment seams.

## Generalized catch power

This rule catches more than the original incident because it targets the recurring failure shape:

- source-level proof that bypasses runtime behavior
- contract drift between producers and consumers
- sibling pipelines implementing the same concept differently
- mocks that make failing runtime paths unobservable
- narrowly patched anchor bugs that leave adjacent defects masked
- review tools auditing the wrong diff or state
- hard gates that fail on heuristic false positives rather than material correctness

The rule should therefore be enforced for future pipeline work even when the concrete symptom is not file delivery, Claude CLI flags, PRD, or `--spec`.

## Evidence basis

- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/escape-E1-PRD-cloud-file-misuse/root-cause.md`
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/defect-escape-table.md`
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/pr-targets-summary.txt`
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/pr-broader-summary.txt`
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/timeline.md`
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/pipeline-artifact-audit.md`
