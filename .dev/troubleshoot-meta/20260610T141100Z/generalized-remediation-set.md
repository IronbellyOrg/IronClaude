# Generalized Remediation Set

## Scope and Non-Goals

This remediation set deduplicates the per-escape fixes for E1 through E5 into reusable, issue-agnostic controls. The controls apply to generated pipelines, CLI wrappers, semantic gates, artifact parsers, independent-review hooks, and recovery/remediation paths.

PRD-only patches are explicitly rejected. A fix is insufficient if it only changes one PRD call site, one observed phase number, one heading string, one evaluator, or one reflect command template while leaving the shared contract, sibling consumers, runtime entrypoint, and generated-artifact surfaces unverified.

Every remediation below must be implemented as a reusable gate/checklist/test pattern with an escape coverage note that states which known escapes it would have caught.

## Remediation R1: Runtime-Boundary Contract Closure

### Problem class

A generated or orchestrated command crosses a runtime boundary, but tests validate only construction-time strings or an idealized helper path rather than the real subprocess/runtime entrypoint. This allows local paths, tokens, selectors, environment assumptions, and stream contracts to diverge from what the runtime actually consumes.

### Required control

For any change that emits, transforms, or consumes a CLI/subprocess/tool boundary contract:

1. Enumerate the boundary contract in a small ledger:
   - Producer: where the command/input is generated.
   - Transformer: any layer that rewrites, serializes, shells, chunks, persists, resumes, or remediates it.
   - Consumer: the real runtime entrypoint that consumes it.
   - Forbidden interpretations: e.g. local filesystem path vs cloud-session file token.
   - Required evidence surface: stdout/stderr, generated artifact, effective command, or parsed result.
2. Replay the real runtime entrypoint, not only a helper/unit constructor.
3. Include a negative control that proves the forbidden interpretation fails the gate before the fix.
4. Sweep sibling pipelines and shared utilities for the same contract, not only the failing feature.
5. Record whether off-path review is required. It is required when the boundary controls data loss, HALT/continue behavior, external process invocation, VCS scope, or independent review.

### Minimal acceptance evidence

- A runtime-entrypoint test or fixture that exercises the same path an operator uses.
- A contract ledger naming all known producers, transformers, and consumers.
- A grep/retrieval-backed sibling sweep for equivalent boundary usage.
- A negative assertion for the forbidden boundary interpretation.

### Escapes caught

- E1: Would have rejected delivering a local path through Claude CLI `--file` because the runtime boundary contract would identify `--file` as a cloud-download/session-token mechanism and replay headless PRD `--spec` without a session token.
- E4: Would have forced proof of the real PRD evaluator rather than relying on the generic gate helper.
- E5: Would have required proof of the effective diff surface consumed by POST-reflect, including dirty working tree semantics.

## Remediation R2: Shared-Contract Consumer Enumeration and Parity Proof

### Problem class

A shared field, predicate, enum, status, semantic check, advisory flag, parser result, artifact shape, or gate outcome changes in one implementation while duplicate or downstream consumers retain old semantics.

### Required control

For any shared-contract change:

1. Enumerate every consumer using both semantic retrieval and exact-token search.
2. Classify each consumer role:
   - Blocking gate/evaluator.
   - Advisory/reporting gate.
   - Trailing/cosmetic remediation.
   - Recovery/resume logic.
   - Artifact reader/parser.
   - Test fixture or generated example.
3. Define expected behavior for each consumer, especially HALT vs WARN vs CONTINUE.
4. Add parity tests when two consumers should behave the same.
5. Add intentional-divergence documentation when two consumers should differ.
6. Fail the change if any consumer is unclassified.

### Minimal acceptance evidence

- Consumer ledger with file/function or artifact references.
- Runtime-path proof for the highest-impact consumer.
- Parity or divergence tests for duplicate evaluators.
- Explicit assertions for halt/warn/continue behavior.

### Escapes caught

- E4: Would have identified `PrdExecutor._evaluate_gate` as a separate semantic-check consumer from generic `pipeline.gates.gate_passed`, preventing advisory semantics from being fixed only off the normal PRD runtime path.
- E2: Would have aligned parser scope with the heavyweight template's executable work phases rather than applying the gate to every phase-like section.
- E3: Would have forced classification of Task Log headings as non-executable artifact content before the strict parallel gate parsed them.

## Remediation R3: Whole-Artifact Classifier Boundary Tests

### Problem class

A parser, scanner, gate, or validator matches a local syntax pattern in generated artifacts but does not respect artifact topology. It accidentally consumes placeholders, logs, examples, summaries, quoted commands, or completion sections as executable work.

### Required control

For any gate/parser over generated artifacts:

1. Test against a full generated artifact, not only extracted snippets.
2. Define classifier boundaries by role, not by fragile text patterns or phase numbers.
3. Include positive examples that must be gated.
4. Include sibling negative examples that look similar but must not be gated.
5. Include generated placeholder/empty-section examples.
6. Review severity when false positives can HALT live work; prefer advisory mode unless the classifier has strong topology proof.

### Minimal acceptance evidence

- One full-artifact fixture from the real generator or an intentionally faithful golden fixture.
- At least one positive executable-section assertion.
- At least one sibling negative assertion from logs/findings/examples/completion/bookends.
- Severity rationale for hard HALT vs advisory.

### Escapes caught

- E2: Would have excluded the sequential completion/presentation bookend from a middle-work-phase parallelism gate.
- E3: Would have excluded Task Log `Phase N - ... Findings` placeholder headings from executable phase parsing.
- E1: Would have helped catch sibling pipeline contract drift if artifact scanners verified all generated local-file delivery surfaces, though R1 is the primary control.

## Remediation R4: Unmask-and-Sweep After Any Escape Fix

### Problem class

A first fix addresses only the symptom that halted execution, leaving adjacent false positives, false negatives, sibling headings, sibling pipelines, duplicate evaluators, or downstream consumers to fail immediately afterward.

### Required control

After any defect escape fix, perform an unmask-and-sweep before declaring closure:

1. Identify the general failure mechanism, not only the observed symptom.
2. Search for adjacent surfaces with the same mechanism.
3. Add at least one adversarial sibling case that was not in the original failure.
4. Re-run or replay far enough past the original failing point to expose the next layer.
5. Document what was deliberately left out and why.

### Minimal acceptance evidence

- Mechanism statement independent of the specific escaped issue.
- Adjacent-surface sweep result.
- A sibling/adversarial regression case.
- Replay evidence beyond the original failure point when runtime cost is reasonable.

### Escapes caught

- E3: Would have followed E2/#154 with a sweep of all generated phase-like headings and caught Task Log placeholder headings before the next live HALT.
- E4: Would have followed E3/#155 with a sweep of all semantic-check consumers and caught the PRD-specific evaluator divergence.
- E1: Would have swept roadmap/tasklist/validate vs PRD local-file delivery contracts and caught PRD's lingering `--file` misuse.

## Remediation R5: Effective-Input Proof for Independent Review and Audit Gates

### Problem class

An independent reviewer, reflect command, audit gate, or off-path checker is present, but the actual input it reviews is empty, stale, foreign, committed-only, or otherwise not the work under evaluation.

### Required control

For any generated review/audit/reflect gate:

1. Prove the effective input surface, not just command presence.
2. Capture an expected-vs-consumed summary:
   - Expected files/artifacts/commits/ranges.
   - Actual files/artifacts/commits/ranges consumed.
   - Exclusions and rationale.
3. Include dirty-working-tree, uncommitted, missing-input, empty-input, and foreign-input negative cases where applicable.
4. Make off-path review block only when it can prove it reviewed the intended surface; otherwise fail closed or clearly mark the review as advisory/incomplete.

### Minimal acceptance evidence

- Machine-checkable effective-input summary or equivalent parsed evidence.
- Regression proving the reviewer sees uncommitted task work when that is expected.
- Negative regression proving unrelated/foreign commits are excluded.
- Failure or warning when the review input is empty or cannot be proven.

### Escapes caught

- E5: Would have caught POST-reflect using `<start_commit>..HEAD` when the actual task work was uncommitted or when unrelated commits entered the range.
- E4: Would have strengthened off-path contract reports by requiring proof they covered the real PRD runtime evaluator path.
- E1: Would have required the headless PRD runtime audit to prove the command consumed the intended local spec content through the correct channel.

## Remediation R6: Severity Cost and Blast-Radius Review

### Problem class

A validator with uncertain classifier boundaries or incomplete runtime proof is wired as a hard stop. False positives become live build halts, while intended advisory checks still behave as fatal in some consumers.

### Required control

For any new or changed gate severity:

1. State the blast radius: local test only, generated artifact warning, runtime warning, recoverable halt, or terminal halt.
2. Require stronger evidence for hard HALT than for advisory WARN.
3. Verify severity on every runtime consumer, not only the generic helper.
4. Include a false-positive cost review for generated artifact parsers.
5. Include a false-negative cost review for security/data-loss/review-integrity contracts.

### Minimal acceptance evidence

- Severity matrix for each consumer.
- Runtime assertion for HALT/WARN/CONTINUE.
- Justification that hard HALT is warranted or downgrade to advisory.
- Regression for advisory failures not stopping the real runtime path.

### Escapes caught

- E2: Would have challenged using a STRICT hard gate on a phase classifier that had not been proven against completion bookends.
- E3: Would have reduced the cost of Task Log heading false positives by requiring severity review for parser uncertainty.
- E4: Would have caught that `SemanticCheck.advisory` did not change fatal behavior in the PRD evaluator.

## Remediation R7: Generalized Escape Closure Definition

### Required closure standard

An escape is not closed until the remediation package answers all of the following in issue-agnostic terms:

1. What shared mechanism failed?
2. What reusable invariant now prevents the mechanism?
3. Which runtime entrypoint proves the invariant under operator-like execution?
4. Which sibling producers/consumers/parsers were swept?
5. Which positive and negative cases prove classifier or contract boundaries?
6. What is the severity behavior across all consumers?
7. Which known escapes E1..En would this control have caught?

### Escapes caught

- E1: Closure would require runtime boundary proof and sibling contract sweep.
- E2: Closure would require topology-aware executable-phase boundaries and severity review.
- E3: Closure would require unmask-and-sweep plus full-artifact sibling negative cases.
- E4: Closure would require complete consumer enumeration and runtime parity/advisory proof.
- E5: Closure would require effective-input proof for review/audit surfaces.

## Deduplicated Coverage Matrix

| Remediation | Primary escapes caught | Secondary escapes mitigated |
|---|---|---|
| R1 Runtime-Boundary Contract Closure | E1, E4, E5 | E3 |
| R2 Shared-Contract Consumer Enumeration and Parity Proof | E4 | E2, E3 |
| R3 Whole-Artifact Classifier Boundary Tests | E2, E3 | E1 |
| R4 Unmask-and-Sweep After Any Escape Fix | E3, E4 | E1, E2 |
| R5 Effective-Input Proof for Independent Review and Audit Gates | E5 | E1, E4 |
| R6 Severity Cost and Blast-Radius Review | E2, E3, E4 | E5 |
| R7 Generalized Escape Closure Definition | E1, E2, E3, E4, E5 | Future E6..En |

## Required Implementation Shape

For future fixes, use this checklist instead of per-issue bespoke patches:

1. Write a one-paragraph mechanism statement that avoids feature names unless necessary for evidence.
2. Add or update the relevant reusable gate/test/checklist from R1 through R6.
3. Include a coverage note: `Known escapes caught: E...`.
4. Include at least one positive and one negative control when the fix involves parsing, selection, gating, or review input.
5. Prove the operator runtime path for any boundary, HALT/WARN, or independent-review behavior.
6. Reject PRD-only fixes unless the contract ledger proves the contract is truly PRD-local and has no sibling producers or consumers.
