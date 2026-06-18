# Final Report Pre-G1 — Troubleshoot Meta-Investigation

Output root: `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z`

Status: **G1-ready, implementation pending approval**.

Base commit: `94d5baa05f6319b8ff6f2e1db8e8b7737465daaf`

## Executive verdict

The Phase 0/G0 evidence is sufficient to freeze the canonical escape set E1..E5 and request G1 approval for a troubleshoot protocol hardening implementation.

The core finding is that the existing assurance pipeline produced real value, but too often proved adjacent artifacts rather than the runtime or contract boundary that actually failed. The overall theatre-vs-value estimate is **41% value / 59% theatre or mis-targeted ceremony**.

This does not mean the process was empty. It caught important issues and created useful audit trails. The failure pattern is narrower: gates, reports, and reviews were often aimed at command strings, helper functions, local snippets, PASS artifacts, or generic evaluator paths instead of the operator entrypoints, generated artifacts, all contract consumers, and effective review inputs where the escapes occurred.

## Theatre-vs-value verdict

### Real value observed

- `sc:troubleshoot` provided the strongest direct contract mapping and surfaced the PRD/generic evaluator divergence behind E4.
- `task-builder` created durable routing, auditability, PRE/POST reflect wiring, and downstream dogfood value.
- `sc:reflect` had a distinct high-value niche: it caught the wrong-diff/base-selection trap in E5.
- QA gates improved evidence hygiene and caught fabricated or stale current-state claims.

### Mis-targeted ceremony observed

- Exact runtime entrypoints were not mandatory, allowing E1 to pass local argv/helper checks while failing headless PRD execution.
- Parser fixes were not followed by an unmask-and-sweep, allowing E2 to reappear as E3 on sibling headings.
- Shared-contract consumers were not enumerated, allowing E4 to validate generic advisory semantics while PRD runtime kept fatal behavior.
- Diff/base semantics were treated as review plumbing, not a primary invariant, allowing E5 to audit the wrong surface.
- Many artifacts improved traceability without adding an observation capable of catching the canonical defect.

### Highest-leverage stage to fix

Fix `task-builder` first in the broader ecosystem, because it shapes required evidence for later gates. For the requested G1 scope, harden `/sc:troubleshoot` and `sc:troubleshoot-protocol` so future investigations close pipeline escapes with reusable runtime and contract controls rather than issue-specific patches.

## Frozen canonical escape set

| ID | Escaped failure | General miss |
|---|---|---|
| E1 — PRD cloud `--file` misuse | Headless `superclaude prd run --spec` passed local paths through Claude CLI `--file`, which required a cloud/session token. | Runtime-entrypoint proof and sibling file-delivery contract sweep were missing. |
| E2 — completion-phase false positive | STRICT `parallel_instructions` halted a valid final sequential completion/presentation phase. | Generated-artifact topology was not tested; parser scope used syntax/position instead of executable phase role. |
| E3 — Task Log findings-heading sibling false positive | The same gate matched non-executable Task Log `Phase N ... Findings` placeholder headings. | The first fix did not unmask-and-sweep same-shape sibling headings in whole generated artifacts. |
| E4 — PRD/generic/trailing evaluator divergence | `SemanticCheck.advisory` was honored by the generic gate path but not by PRD runtime's bespoke evaluator. | Shared-contract consumers were not enumerated and runtime PRD evaluator proof was missing. |
| E5 — POST-reflect wrong diff base | Generated POST-reflect audited `<start_commit>..HEAD`, omitting dirty `/task` work and possibly including foreign commits. | Independent review presence was accepted without effective-input proof. |

## Merged root causes

### RC1: Runtime boundary proof was substituted with construction proof

E1 and E5 show the strongest form of this failure. In E1, PRD preserved paths and built argv, but no check proved the real headless Claude subprocess accepted those paths through `--file`. In E5, a generated reflect command existed, but no check proved the selected diff matched `/task`'s dirty working-tree output.

General root cause: pipeline closure accepted syntactic command presence or helper-level behavior instead of proving the actual runtime input consumed by the operator entrypoint.

### RC2: Generated-artifact parsers lacked topology-aware boundaries

E2 and E3 show that parser/gate logic treated locally matched `Phase N` headings as executable work without respecting generated artifact roles. Completion bookends and Task Log placeholders looked similar enough to trigger strict enforcement.

General root cause: validators over generated prose were tested against snippets and expected headings rather than full generated artifacts containing positive executable sections and sibling negative sections.

### RC3: First fixes did not generalize to same-class sibling surfaces

E3 followed E2 because the fix addressed the visible final-phase symptom but did not sweep all generated phase-like headings. E4 has the same shape at the contract level: a semantic change was validated on one evaluator while other consumers remained unswept.

General root cause: closure focused on the observed repro instead of the mechanism family and adjacent masked surfaces.

### RC4: Shared contracts had multiple live consumers but no consumer ledger

E4 is the canonical example. `SemanticCheck.advisory` was a multi-consumer contract: generic gates, PRD runtime gates, trailing gates, remediation dispatch, fixtures, and reports could all interpret it. Verification validated the edited generic helper and inferred PRD coverage incorrectly.

General root cause: shared field/predicate/status changes lacked mandatory producer/transformer/consumer enumeration and parity or intentional-divergence proof.

### RC5: Independent review was treated as present/absent instead of input-correct/incorrect

E5 shows that off-path review can exist and still be false assurance if it reviews an empty, stale, or foreign surface. A PASS artifact or reflect invocation is not enough.

General root cause: review gates lacked effective-input proof tying expected runtime-produced changes to the actual files, commits, artifacts, or logs consumed by the reviewer.

## Generalized remediation set

Use the following controls as reusable closure requirements for future pipeline escapes. PRD-only patches are insufficient unless a contract ledger proves the mechanism is truly PRD-local.

1. **Runtime-Boundary Contract Closure**
   - Enumerate producer, transformers, consumer, forbidden interpretations, and evidence surface.
   - Replay the real operator/runtime entrypoint.
   - Include a negative control for forbidden boundary interpretations.
   - Sweep sibling pipelines and shared utilities.
   - Primary coverage: E1, E4, E5.

2. **Shared-Contract Consumer Enumeration and Parity Proof**
   - Enumerate all consumers using semantic retrieval and exact-token search.
   - Classify each consumer as blocking, advisory, trailing, recovery, parser, fixture, or generated example.
   - Add parity tests where behavior should match and divergence documentation where it should not.
   - Primary coverage: E4; secondary coverage: E2, E3.

3. **Whole-Artifact Classifier Boundary Tests**
   - Test gates/parsers against full generated artifacts.
   - Include executable positive cases and sibling negative cases from logs, findings, examples, completion sections, and placeholders.
   - Review hard-HALT severity when classifier boundaries are heuristic.
   - Primary coverage: E2, E3.

4. **Unmask-and-Sweep After Any Escape Fix**
   - State the general mechanism, search adjacent surfaces, add adversarial sibling cases, and replay past the original failure point when feasible.
   - Primary coverage: E3, E4; secondary coverage: E1, E2.

5. **Effective-Input Proof for Independent Review and Audit Gates**
   - Capture expected vs consumed files, commits, ranges, artifacts, exclusions, and empty/missing behavior.
   - Prove dirty work is included when expected and foreign work is excluded.
   - Primary coverage: E5; secondary coverage: E1, E4.

6. **Severity Cost and Blast-Radius Review**
   - State whether the gate is local, advisory, recoverable halt, or terminal halt.
   - Require stronger proof for hard HALT than for WARN.
   - Verify HALT/WARN/CONTINUE behavior on every runtime consumer.
   - Primary coverage: E2, E3, E4.

7. **Generalized Escape Closure Definition**
   - Closure must answer: what shared mechanism failed, what reusable invariant prevents it, which runtime entrypoint proves it, which sibling surfaces were swept, which positive/negative cases prove boundaries, how severity behaves across consumers, and which known escapes the control would have caught.

## Proposed troubleshoot refactor spec

The G1 implementation should harden `/sc:troubleshoot` and `sc:troubleshoot-protocol` with a new **Pipeline Hardening Closure** mode.

### Trigger

Enter this mode when diagnosis or remediation touches any of the following:

- CLI, subprocess, tool, file, stdin, prompt, or generated-artifact boundary contracts.
- Generated markdown/JSON/YAML/stdout/log parsers.
- Gate severity, semantic checks, status enums, halt/warn/continue behavior.
- Duplicated evaluators, callbacks, trailing gates, remediation dispatchers, recovery/resume, or persisted state.
- Review/audit/reflect selectors, diff ranges, path globs, artifact paths, cached metadata, or effective input surfaces.
- Sibling pipelines implementing the same conceptual contract.
- Prior escapes or fixes that unmasked same-class sibling failures.

### Required waves and gates

1. **H0 — Applicability and mechanism statement**
   - Decide whether pipeline hardening applies.
   - Write a mechanism statement independent of one product symptom.
   - If skipped near a boundary, record the concrete reason and boundary scan.

2. **H1 — Runtime-entrypoint verification gate**
   - Record the production/operator entrypoint, call chain, boundary crossed, producer, transformers, consumer, environment assumptions, replay command or faithful harness, evidence that the replay reaches production boundary, asserted outcome, same-boundary negative control, and known escapes caught.
   - Fail if proof stops at helper construction while the defect can appear only at a runtime boundary.

3. **H2 — Contract-enumeration wave**
   - Build a ledger for the changed field, flag, parser rule, artifact shape, semantic check, selector, severity, status, or predicate.
   - Classify all producers, transformers, consumers, discovery method, role, expected behavior, decision, and evidence.
   - Fail if any live consumer is unclassified.

4. **H3 — Unmask-and-sweep regression wave**
   - Identify the anchor failure and mechanism family.
   - Sweep implementation and generated/runtime artifact surfaces.
   - Add positive controls, sibling negative controls, replay evidence beyond the first failure when feasible, and severity cost review.
   - Fail if the fix only addresses the reported repro.

5. **H4 — Effective-input proof for independent review/audit gates**
   - Trigger when review, reflect, audit, validation, or off-path checkers consume indirect selectors.
   - Prove expected surface, generated selector, actual reviewer command, consumed input, dirty/staged/unstaged inclusion, foreign exclusions, empty/missing behavior, manifest evidence, and negative cases.
   - Fail closed when input is absent, empty despite known changes, non-reproducible, or includes known foreign work.

6. **H5 — Off-path-reviewer rule**
   - Require off-path review for external subprocesses, path reinterpretation, generated artifacts consumed by later gates, persisted state, review selector logic, hard heuristic gates, mocks for runtime I/O, duplicate evaluator divergence, or HALT/WARN/CONTINUE controls.
   - Allow waiver only with evidence that local proof directly executes the risky boundary or the boundary is not material.

### Output contract additions

When hardening is evaluated, the skill result should include:

- `pipeline_hardening_applicable`
- `pipeline_hardening_verdict`: `pass`, `blocked`, `advisory`, or `not_applicable`
- `runtime_entrypoint_card_path`
- `contract_ledger_path`
- `unmask_sweep_path`
- `effective_input_card_path`
- `off_path_review_decision`
- `known_escapes_caught`

The final report template should include a `Pipeline Hardening Closure` section and use `NOT PROVEN` blockers when required evidence is absent.

## Likely post-G1 edit scope

Source-of-truth files only:

- `/config/workspace/IronClaude/src/superclaude/commands/troubleshoot.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/remediation-handoff.md`

Likely new refs/templates:

- `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/pipeline-hardening-closure.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/runtime-entrypoint-verification.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/contract-enumeration.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/unmask-and-sweep.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/effective-input-proof.md`

Validation after source edits:

- Run `make sync-dev`.
- Run `make verify-sync`.
- Add or run targeted tests only if existing test surfaces parse command/skill metadata or if a lightweight fixture can validate required protocol sections.

## Explicit G1 halt note

Implementation and backtest are **pending G1 approval** because the next step requires editing shared source-of-truth skill and command files under `/config/workspace/IronClaude/src/superclaude/`. No implementation edits should occur before approval.

Do not edit generated `.claude/` skill, command, agent, hook, or template mirrors directly. After approved source edits, refresh mirrors with `make sync-dev` and verify with `make verify-sync`; do not stage generated `.claude/` mirrors.

## Recommendation

Approve G1 if the desired next phase is to implement the mechanism-based troubleshoot hardening spec in source-of-truth protocol files.

Paste-ready approval prompt:

```text
Approved G1. Implement /config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/troubleshoot-pipeline-hardening-spec.md in source-of-truth files only. Do not edit .claude mirrors directly. After edits, run make sync-dev and make verify-sync, then report changed files and any tests run. Do not commit.
```
