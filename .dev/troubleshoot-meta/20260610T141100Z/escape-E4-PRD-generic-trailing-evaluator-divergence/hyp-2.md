# Why-it-escaped hypothesis card: E4 PRD generic/trailing evaluator divergence

## Lens

Verification-artifact/off-path-review lens. This card is based on existing review and troubleshooting artifacts, not a fresh implementation-path audit.

## Escape

`E4-PRD-generic-trailing-evaluator-divergence`

PR #155 intended `parallel_instructions` to warn instead of halt, but the reviewed proof packet centered on the generic gate framework and PRD gate wiring. The later contract report found that normal PRD runtime uses a separate PRD evaluator, so advisory semantics were not proven at the runtime consumer that matters.

## Hypothesis

The defect escaped because review artifacts accepted a **framework-level semantic contract proof** as if it were a **PRD runtime contract proof**. The PR #155 evidence package showed that `SemanticCheck.advisory` existed, that the generic gate evaluator warned and continued, that the PRD gate data marked `parallel_instructions` advisory, and that generic/PRD tests passed. It did not require a verification artifact that enumerated every consumer of `semantic_checks` or proved that `superclaude prd run` exercised the same evaluator under test.

In other words, the review surface was off-path: it validated the newly added advisory behavior where it was implemented and locally tested, then inferred coverage for PRD because PRD reused the data model. The missing review question was: “Which evaluator actually consumes this `SemanticCheck` during the production PRD run?”

## Evidence chain

1. The PR #155 summary framed the fix as a gate-framework capability: add `SemanticCheck.advisory`, make the STRICT loop in `pipeline/gates.py` warn and proceed for advisory checks, and mark only PRD `parallel_instructions` advisory. Its test evidence likewise emphasized advisory pass/warning behavior, non-advisory halt behavior, wiring lock, and green `tests/pipeline/` plus `tests/cli/prd/` suites. Evidence: `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/pr-targets-summary.txt` lines 81-99 and `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/pr-155.json` line 1.

2. The contract report later identified the missing distinction: normal PRD runtime does not use the generic `pipeline/gates.py:gate_passed()` evaluator or trailing gate runner; it uses a bespoke PRD evaluator. Evidence: `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/contract-implementations.md` lines 14-18.

3. The same contract report shows that the runtime call-chain proof, once performed, would have exposed the mismatch: `superclaude prd run` constructs `PrdExecutor`, resolves disk artifact content inside `_execute_step`, and calls the PRD evaluator; strict failures can halt. Evidence: `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/contract-implementations.md` lines 20-29.

4. The report explicitly inventories multiple semantic-check consumers: generic blocking gates, PRD runtime gates, trailing gates, and generic cosmetic-remediation dispatch. That is the consumer enumeration the PR #155 review packet lacked. Evidence: `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/contract-implementations.md` lines 41-78 and lines 141-145.

5. The reflect-stage value card independently classifies this as a review-stage miss: `sc:reflect` did not require runtime call-graph proof for `superclaude prd run` or a sweep of every `semantic_checks` consumer, so the fix intent “warn, don't halt” was not verified against the PRD runtime evaluator. Evidence: `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/stage-value-sc-reflect.md` lines 41-44 and lines 72-79.

6. The broader phase scorecard names the same pattern as ceremony/mis-targeted assurance: contract consumers were not enumerated, so generic advisory semantics and PRD-specific evaluator semantics diverged while reviews verified one path and implied coverage of the other. Evidence: `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/theatre-vs-value-scorecard.md` lines 27-33.

## Why review did not catch it

- **The artifacts treated PRD gate data wiring as sufficient PRD runtime evidence.** Marking `parallel_instructions` advisory in PRD gate criteria proved the data bit was set, but not that the PRD evaluator honored it.
- **The proof packet was organized around the edited generic framework path.** Because PR #155 changed `pipeline/models.py` and `pipeline/gates.py`, the natural tests and review attention followed those files. That created a plausible but incomplete “framework contract fixed” story.
- **The review lacked a consumer ledger.** No artifact before the A2 contract report appears to have forced the question “where is `semantic_checks` iterated?” across all implementations.
- **The failure mode was off-path from the successful tests.** Green generic-gate advisory tests can coexist with a PRD-specific evaluator that still fails advisory checks. The verification artifact needed a PRD-runtime assertion, not just model/generic evaluator assertions.
- **Cost-asymmetry reasoning substituted for entrypoint proof.** PR #155 correctly identified that false-positive hard halts were worse than slower serial execution, but the review did not convert that design rationale into a blocking runtime proof that hard halts were actually removed from the production PRD path.

## Falsifiable prediction

If the pre-merge verification packet for PR #155 is reconstructed, it will show tests or review notes for the generic `gate_passed` advisory behavior and PRD gate-data wiring, but it will not contain a runtime-entrypoint proof demonstrating that `superclaude prd run` evaluates `parallel_instructions` through an advisory-aware evaluator.

## Preventive review invariant

For any shared contract change such as `SemanticCheck.advisory`, a review artifact must include a consumer ledger with one row per live consumer and an explicit runtime-entrypoint proof for the affected product path. For this escape, the minimum proof would have been: `superclaude prd run` path identified, PRD runtime evaluator named, advisory failure observed as non-halting on that path, and all other `semantic_checks` loops classified as in-scope, off-path, or intentionally unchanged.
