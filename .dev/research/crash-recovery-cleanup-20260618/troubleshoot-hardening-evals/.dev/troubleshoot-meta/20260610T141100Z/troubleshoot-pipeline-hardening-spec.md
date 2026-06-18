# Troubleshoot Pipeline Hardening Spec — G1 Draft

Output root: `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z`

Status: G1 approval draft only. Do not edit `src/superclaude/` or `.claude/` skill/command files until G1 approval is granted.

## 1. Goal

Harden `/sc:troubleshoot` and `sc:troubleshoot-protocol` so pipeline escapes are closed by reusable protocol controls rather than by issue-specific patches. The hardened protocol must force evidence at the runtime and contract seams where the canonical escape set occurred.

The G1 change should encode the generalized remediation set as protocol waves/gates:

1. Runtime-entrypoint verification gate.
2. Contract-enumeration wave.
3. Unmask-and-sweep regression wave.
4. Off-path-reviewer rule, when the issue crosses high-risk boundaries or when local review does not execute the risky surface.

## 2. Source evidence

This spec is based on the frozen Phase 0/G0 input set:

- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/GATE-0.md`
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/theatre-vs-value-scorecard.md`
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/generalized-remediation-set.md`
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/escape-E1-PRD-cloud-file-misuse/root-cause.md`
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/escape-E1-PRD-cloud-file-misuse/remediation.md`
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/escape-E2-PRD-completion-phase-false-posit
- ive/root-cause.md`
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/escape-E2-PRD-completion-phase-false-positive/remediation.md`
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/escape-E3-PRD-tasklog-findings-heading-sibling/root-cause.md`
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/escape-E3-PRD-tasklog-findings-heading-sibling/remediation.md`
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/escape-E4-PRD-generic-trailing-evaluator-divergence/root-cause.md`
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/escape-E4-PRD-generic-trailing-evaluator-divergence/remediation.md`
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/escape-E5-Reflect-post-diff-wrong-base/root-cause.md`
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/escape-E5-Reflect-post-diff-wrong-base/remediation.md`

## 3. Canonical escapes this must catch in one shot

The hardened protocol must assert and enforce coverage for the full frozen set E1..E5:

| Escape | Failure shape | Required protocol catcher |
|---|---|---|
| E1 — PRD cloud `--file` misuse | Helper/argv proof was accepted while the real headless subprocess rejected local paths passed through a cloud/session-token-only file mechanism. Sibling pipelines already avoided the pattern. | Runtime-entrypoint verification gate + contract-enumeration wave + sibling boundary sweep. |
| E2 — completion-phase false positive | Parser enforced a parallel-work invariant on a final sequential completion/presentation bookend because the validator used syntactic/positional phase matching rather than semantic topology. | Whole-artifact classifier boundary proof inside runtime-entrypoint verification + unmask-and-sweep regression wave. |
| E3 — Task Log findings-heading sibling false positive | The E2 fix removed one symptom but did not sweep same-token sibling headings in the full generated artifact; a hard heuristic gate then halted on non-executable Task Log placeholder headings. | Unmask-and-sweep regression wave + severity blast-radius review. |
| E4 — PRD/generic/trailing evaluator divergence | A shared `SemanticCheck.advisory` contract was validated on the generic gate path while the real PRD runtime used a bespoke evaluator that still treated advisory failures as fatal. | Contract-enumeration wave + runtime-entrypoint proof for the affected command + parity/divergence tests. |
| E5 — POST-reflect wrong diff base | Independent review existed, but the generated review selector audited a commit range that omitted dirty `/task` work and could include foreign commits. | Effective-input proof + off-path-reviewer rule with selector/runtime-surface validation. |

## 4. Design principle

Troubleshoot currently diagnoses issues quickly and escalates when confidence is low. Pipeline hardening adds a different dimension: when the diagnosed issue is a pipeline escape, remediation is not complete until the protocol proves the invariant at the same runtime, generated-artifact, contract-consumer, and review-input boundaries where the escape can recur.

The hardened flow must reject the following proof substitutions:

- command-string construction instead of real entrypoint proof;
- artifact or PASS report presence instead of effective-input proof;
- edited-helper tests instead of concrete runtime evaluator proof;
- one observed repro fix instead of same-class unmask-and-sweep;
- generic evaluator proof instead of all-consumer contract parity;
- off-path review that consumes an empty, stale, or foreign surface.

## 5. Proposed protocol insertion points

### 5.1 `/sc:troubleshoot` command

Expected command-file changes after G1 approval:

- Update the behavioral summary to advertise pipeline hardening when the issue involves CLI pipelines, generated artifacts, gates, parsers, validators, subprocesses, persisted state, recovery/resume, or independent review selectors.
- Extend the output description to mention hardening evidence paths when the protocol enters pipeline-hardening mode.
- Keep the command thin: it should still hand off to `sc:troubleshoot-protocol`; hardening logic belongs in the skill and refs.

### 5.2 `sc:troubleshoot-protocol` skill

Expected skill changes after G1 approval:

- Add a pipeline-hardening trigger after Tier 1 diagnosis and before final report closure.
- Add one or more refs/templates for the closure cards, so the main `SKILL.md` remains navigable.
- Extend the output contract with optional hardening artifact paths and verdicts.
- Wire failure states: a pipeline escape cannot be marked remediated when required hardening gates are missing, failed, or marked `N/A` without rationale.

## 6. New protocol mode: Pipeline Hardening Closure

### 6.1 Trigger

Enter Pipeline Hardening Closure when any diagnosis or remediation touches one or more of:

- CLI/subprocess/tool boundary contracts;
- file/stdin/prompt delivery mechanisms;
- generated markdown/JSON/YAML/stdout/log parsers;
- gate severity, semantic checks, status enums, halt/warn/continue behavior;
- duplicated evaluators, adapters, callbacks, trailing gates, or remediation dispatchers;
- persisted state, resume/recovery, dynamic artifact lookup;
- review/audit/reflect selectors, diff ranges, path globs, or effective input surfaces;
- sibling pipelines implementing the same conceptual contract;
- a prior defect escape or an observed fix that unmasked a same-class sibling failure.

Pure local bug fixes may skip this mode, but the report must say `pipeline_hardening_applicable=false` with a one-sentence reason when the symptom looks near a pipeline boundary and the mode is skipped.

### 6.2 New output contract fields

Add optional fields to the skill result when pipeline-hardening mode is evaluated:

| Field | Type | Meaning |
|---|---|---|
| `pipeline_hardening_applicable` | bool | Whether the trigger fired. |
| `pipeline_hardening_verdict` | string | `pass`, `blocked`, `advisory`, or `not_applicable`. |
| `runtime_entrypoint_card_path` | string \| null | Repo-relative path to the runtime-entrypoint verification card. |
| `contract_ledger_path` | string \| null | Repo-relative path to the consumer/producer contract ledger. |
| `unmask_sweep_path` | string \| null | Repo-relative path to the unmask-and-sweep report. |
| `effective_input_card_path` | string \| null | Repo-relative path when review/audit inputs are involved. |
| `off_path_review_decision` | string | `required`, `performed`, `waived_with_rationale`, or `not_required`. |
| `known_escapes_caught` | list[string] | Known escape IDs the evidence would have caught. |

## 7. Required waves and gates

### Wave H0 — Applicability and mechanism statement

Goal: classify whether the issue is a pipeline escape or pipeline-boundary change.

Required outputs:

- `pipeline_hardening_applicable` decision.
- One-paragraph mechanism statement that avoids feature-specific wording unless needed for evidence.
- Candidate known escapes caught: e.g. `E1`, `E2`, `E3`, `E4`, `E5`, or `Future E6+`.

Pass criteria:

- If the issue involves a runtime boundary, generated artifact, shared contract, hard gate, or independent review selector, H1-H4 cannot be skipped.
- If skipped, the report must state the concrete reason and the boundary scan used to justify the skip.

### Gate H1 — Runtime-entrypoint verification gate

Maps to generalized R1, R3, R5, and R6.

Required evidence card:

```text
Runtime-entrypoint verification
- Production/operator entrypoint:
- Runtime call chain or executor path:
- Boundary crossed: CLI/subprocess/filesystem/stdin/prompt/generated artifact/gate/persisted state/review selector/other
- Producer of the value/artifact/signal:
- Transformer(s):
- Consumer/evaluator/reviewer:
- Relevant environment assumptions and absences:
- Exact replay command, fixture, or faithful harness:
- Evidence the replay reaches the production boundary:
- External outcome asserted: continue/warn/halt/pass/fail/reviewed-input
- Same-boundary negative control:
- If helper-only proof is used, why it is equivalent:
- Known escapes caught:
```

Blocking rule:

- H1 fails if proof stops at helper construction while the defect can appear only at a subprocess, gate, generated-artifact parser, persisted-state, or review-selector boundary.
- H1 requires at least one negative control when the contract has a forbidden interpretation: local path as cloud file, advisory as fatal, dirty work omitted, empty artifact accepted, or non-executable heading treated as executable.

Escapes caught in one shot:

- E1: headless PRD `--spec` replay would reject local-path `--file` misuse.
- E2/E3: full generated artifact replay would show whether the gate applies only to executable work sections.
- E4: PRD command/runtime proof would show the concrete evaluator consuming advisory checks.
- E5: `/task`-like dirty-working-tree harness would show whether review sees actual task work.

### Wave H2 — Contract-enumeration wave

Maps to generalized R1, R2, R5, and R6.

Required ledger:

| Field | Required content |
|---|---|
| Contract | Field, flag, parser rule, artifact shape, semantic check, selector, severity, status, or predicate. |
| Producers | Generators, templates, CLI args, prompts, persisted fields, fixtures, mocks. |
| Transformers | Shelling, serialization, chunking, persistence, resume/recovery, prompt injection, artifact resolution. |
| Consumers | Runtime evaluators, generic helpers, bespoke executors, trailing gates, reporting, remediation, validation, recovery, tests. |
| How found | Semantic retrieval, exact search terms, symbol/reference search, template inventory, generated fixture inventory. |
| Role | Primary runtime, generic path, bespoke path, off-path/trailing, remediation, validation-only, test-only, dead/legacy. |
| Expected behavior | HALT/WARN/CONTINUE, include/exclude, parse/ignore, local/cloud, dirty/committed. |
| Decision | Updated, already consistent, intentionally divergent, unaffected with proof, deprecated, or follow-up. |
| Evidence | File/function/artifact references or tests. |

Blocking rule:

- H2 fails if any live consumer is unclassified.
- H2 fails if generic/shared proof is used for a product path without proving the product path reaches that implementation.
- H2 fails if sibling pipelines or duplicate evaluators are not swept when the concept is shared.

Escapes caught in one shot:

- E1: PRD would be identified as a sibling-contract outlier relative to roadmap/tasklist/validate file delivery.
- E2/E3: executable phase-plan headings would be classified separately from setup/completion/Task Log/findings placeholders.
- E4: generic gate, PRD evaluator, trailing gate, and remediation dispatch consumers would be inventoried before closure.
- E5: generator, `/task` runtime producer, selector resolver, reviewer, proof artifact, and validation scanner would be mapped.

### Wave H3 — Unmask-and-sweep regression wave

Maps to generalized R3, R4, R6, and R7.

Required outputs:

- Anchor failure and family-level mechanism.
- Sweep dimensions searched.
- Search/query strategy.
- Implementation surfaces searched.
- Generated/runtime artifact surfaces searched.
- Positive controls that must still fail or be detected.
- Sibling negative controls that must not hard-fail.
- Adjacent hits and dispositions.
- Replay evidence beyond the original failing point when feasible.
- Severity cost review for hard gates.

Minimum regression pattern:

1. A positive case proves the intended violation is still caught.
2. A sibling/off-path negative case proves same-token or same-shape non-target content does not hard-fail.
3. A full-artifact or live-boundary case includes both intended and sibling surfaces.
4. A severity assertion proves HALT/WARN/CONTINUE on each relevant runtime consumer.

Blocking rule:

- H3 fails if a fix only addresses the reported repro and does not search for adjacent masked defects.
- H3 fails if a heuristic parser over generated prose is hard-fatal without adversarial false-positive fixtures and a cost rationale.

Escapes caught in one shot:

- E2 would not close on only a final-phase exception; it would require role/topology fixtures.
- E3 would be caught by the required sibling-heading negative case after E2.
- E4 would be caught by the required duplicate-consumer sweep after advisory semantics changed.
- E1 would be caught by sibling file-delivery sweeps.
- E5 would be caught by review selector sweeps for dirty work, foreign commits, empty input, and missing proof.

### Gate H4 — Effective-input proof for independent review/audit gates

Maps to generalized R5.

Trigger when a generated review, reflect, audit, validation, or off-path checker consumes an indirect selector: diff range, file list, path glob, artifact path, cached metadata, stdout/log capture, resume state, or model-produced filename.

Required proof:

```text
Effective Input Proof
- Runtime entrypoint that produced the work:
- Runtime-produced expected surface: files/commits/artifacts/logs/prompts/state
- Generated selector after placeholder resolution:
- Reviewer/auditor command actually run:
- Effective input consumed by reviewer:
- Dirty/staged/unstaged state included:
- Foreign commits/files excluded:
- Empty/missing/malformed input behavior:
- Machine-checkable manifest or equivalent evidence:
- Negative cases exercised:
```

Blocking rule:

- A PASS artifact, independent reviewer, or command presence is insufficient.
- H4 fails closed when effective input is absent, empty despite known changes, non-reproducible, or includes known foreign work.

Escapes caught in one shot:

- E5 directly: the generated POST-reflect command would be rejected unless it proved dirty `/task` work was included and foreign commits were excluded.
- E4 secondarily: off-path reports must prove they reviewed the concrete PRD evaluator path.
- E1 secondarily: runtime audit must prove the intended spec content was consumed through the correct delivery channel.

### Rule H5 — Off-path-reviewer rule

Maps to generalized R1, R3, R4, R5, and R6.

Off-path review is required when any of the following are true:

- CLI invokes a subprocess or external tool.
- Filesystem paths are reinterpreted by another layer.
- Generated artifacts are consumed by later gates.
- Persisted state affects resume or recovery behavior.
- Review/audit machinery selects a diff, branch, path, artifact, or working-tree state.
- A hard gate uses heuristic parsing or generated prose.
- A mock substitutes for runtime I/O.
- A sibling pipeline or duplicate evaluator has a different contract for the same concept.
- The change controls HALT/WARN/CONTINUE, data loss, review integrity, or external process invocation.

Acceptable off-path forms:

- adversarial review focused on the contract boundary;
- independent reflect review with effective-input proof;
- targeted runtime smoke/e2e reviewer;
- consumer-side contract-ledger audit;
- explicitly scoped heterogeneous reviewer for high-impact gates.

Waiver standard:

- The waiver must say why local evidence directly executes the risky boundary or why the boundary is not material.
- Waiver is invalid if it merely says tests pass, the reviewer is independent, the command exists, or the issue looks local.

## 8. Report and template changes

The final REPORT.md should gain a `Pipeline Hardening Closure` section when applicable:

```markdown
## Pipeline Hardening Closure

- Applicability: applicable | not applicable
- Mechanism statement:
- Runtime-entrypoint verification: PASS | FAIL | N/A — <card path>
- Contract enumeration: PASS | FAIL | N/A — <ledger path>
- Unmask-and-sweep: PASS | FAIL | N/A — <sweep path>
- Effective-input proof: PASS | FAIL | N/A — <card path>
- Off-path review decision: required | performed | waived_with_rationale | not_required
- Severity/blast-radius decision:
- Known escapes this would have caught: E...
- Closure verdict: pass | blocked | advisory
```

The protocol must use `NOT PROVEN` blockers when any required proof is absent. This is intentionally stronger than ordinary confidence language because the canonical escapes came from accepting adjacent proof as if it covered the runtime contract.

## 9. Likely files to edit after G1 approval

Source-of-truth files only; run `make sync-dev` afterward to refresh `.claude/` mirrors.

Primary expected edits:

- `/config/workspace/IronClaude/src/superclaude/commands/troubleshoot.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/remediation-handoff.md`

Likely new ref/template files:

- `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/pipeline-hardening-closure.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/runtime-entrypoint-verification.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/contract-enumeration.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/unmask-and-sweep.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/effective-input-proof.md`

Potential tests/docs after implementation planning, if approval scope includes validation:

- `/config/workspace/IronClaude/tests/` targeted tests for sync/install/package expectations if command/skill metadata is parsed by tests.
- `/config/workspace/IronClaude/docs/` only if user-facing command docs are expected to mirror the protocol change.

Forbidden before G1 approval:

- Do not edit `/config/workspace/IronClaude/src/superclaude/commands/troubleshoot.md` yet.
- Do not edit `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` yet.
- Do not edit `.claude/skills`, `.claude/commands`, `.claude/agents`, `.claude/hooks`, or `.claude/templates` directly.

## 10. Acceptance criteria for the post-G1 implementation

1. `/sc:troubleshoot` remains a thin command handoff and does not duplicate heavy protocol logic.
2. `sc:troubleshoot-protocol` includes a clear pipeline-hardening trigger and explicit closure verdict.
3. Runtime-entrypoint verification is blocking for CLI/subprocess/generated-artifact/gate/persisted-state/review-selector boundaries.
4. Shared-contract changes require a complete producer/transformer/consumer ledger.
5. Parser/gate fixes require whole-artifact positive and sibling-negative controls.
6. Any escape fix requires unmask-and-sweep before closure.
7. Independent review gates require effective-input proof, not just reviewer presence or PASS text.
8. Off-path review is required or explicitly waived with evidence when high-risk boundaries are crossed.
9. The report identifies known escapes caught, and the closure definition asserts issue-agnostic coverage.
10. `make sync-dev` and `make verify-sync` pass after source edits, with `.claude/` mirrors not staged except `.claude/settings.json` if explicitly changed.

## 11. Justification: why this catches E1..En in one shot

The controls are deliberately mechanism-based rather than PRD-specific:

- E1 is a runtime-boundary and sibling-contract failure. H1 proves the real headless subprocess contract; H2 compares sibling file-delivery implementations; H3 sweeps local-vs-cloud/session-token equivalents.
- E2 is a generated-artifact topology failure. H1 forces the live gate/artifact shape; H3 forces setup/work/completion positive-negative fixtures and severity assertions.
- E3 is an unmasked sibling classifier failure. H3 exists specifically to search same-token/same-shape sibling surfaces after an anchor fix and to downgrade or justify heuristic hard gates.
- E4 is a shared-contract consumer divergence. H2 requires all semantic-check consumers, not only the edited generic helper; H1 proves the affected user-visible runtime reaches the intended evaluator.
- E5 is an independent-review effective-input failure. H4 proves the reviewer consumed the runtime-produced work surface, including dirty work, and excluded foreign work.

The same controls generalize to future E6..En because each closure question is expressed as a reusable invariant:

1. What runtime boundary consumes or rejects the value?
2. Who produces, transforms, and consumes the changed contract?
3. What same-class sibling surfaces were masked by the first failure?
4. What positive and negative controls prove classifier or contract boundaries?
5. Does the severity behavior match the blast radius on every consumer?
6. If independent review is present, what did it actually review?

A future escape can still be novel in product details, but it should not bypass all four hardening controls unless it is outside runtime boundaries, shared contracts, generated artifacts, gates, parsers, selectors, and independent review. That is the intended meaning of catching E1..En in one shot.

## 12. G1 halt condition

This draft is the stop point before shared protocol edits. Proceed only after human approval of the G1 package.
