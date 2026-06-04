# Reviewer Card — R2-sonnet-qa

**Reviewer ID:** R2-sonnet-qa  
**Model:** gpt-5.5  
**Persona:** QA-side adversarial review — testability, contract-to-CI mapping, recurrence corpus realism, B2 self-contained task pattern

## Verdict

**PARTIAL — refactor-then-ship.**

The tasklist is unusually complete in breadth: it covers R0's three bridge items, R1.1-R1.6, the 10 Contract items, recurrence corpus expansion, CI wiring, terminal QA gates, and PRESERVE audits. However, it has two material pre-execution defects that should be fixed before execution:

1. **Critical MVR deviation:** R1.6 canonizes `pipeline/gates.py:_check_frontmatter` as the parser instead of deleting `_check_frontmatter` and moving parser authority into the post-step/envelope extractor as BUILD-REQUEST §MVR requires.
2. **High CI classification inconsistency:** Phase 5 misclassifies Contract #9 as pipeline-blocking and Contract #5 as PR-blocking, contradicting BUILD-REQUEST §Contract pass criterion. Phase 13 later corrects this, but worker agents will execute Phase 5 first and may wire CI incorrectly.

Recommendation: **refactor-then-ship**. Do not re-author from scratch; patch the deviations, then proceed.

## 5-Dimension Scores

### 1. Citation grounding — **4/5**

Spot-checks against current code found most cited file:line references grounded:

- Tasklist Step 8.2 cites `src/superclaude/cli/pipeline/models.py` lines 82-105 for `SemanticCheck`/`GateCriteria`; current code has `SemanticCheck` at `src/superclaude/cli/pipeline/models.py:81-87` and `GateCriteria` at `src/superclaude/cli/pipeline/models.py:90-105`.
- Tasklist Step 8.3 cites `build_certify_step` at `executor.py:1899-1944`; current code matches `src/superclaude/cli/roadmap/executor.py:1899-1944`.
- Tasklist Step 11.4 cites the `gate=None if config.convergence_enabled else SPEC_FIDELITY_GATE` bypass at `executor.py:2167`; current code matches `src/superclaude/cli/roadmap/executor.py:2157-2168`.
- Tasklist Step 11.1 cites `_cross_refs_resolve` at `gates.py:L48-91`; current code matches `src/superclaude/cli/roadmap/gates.py:48-91`.
- Tasklist Step 11.1 cites `_parse_frontmatter` at `gates.py:L168`; current code matches `src/superclaude/cli/roadmap/gates.py:168-189`.
- Tasklist Step 11.1 cites `fidelity_checker.py:287-303` and `314-337`; current fail-open blocks match `src/superclaude/cli/roadmap/fidelity_checker.py:287-303` and `314-337`.
- Tasklist Step 11.1 cites `spec_patch.py:_extract_frontmatter L285`; current code matches `src/superclaude/cli/roadmap/spec_patch.py:285-304`.
- Tasklist Step 11.1 cites `obligation_scanner.py` return-True lines around 719/722/725/729/733/737/741/760; current code has those early exits at `src/superclaude/cli/roadmap/obligation_scanner.py:718-741` and `760`.

Deduction: some tasklist line references depend on generated research files rather than direct current-code checks, and a few citations are semantically questionable even when line-grounded, especially the `_check_frontmatter` canonicalization choice.

### 2. Coverage completeness — **4.5/5**

**Coverage pct:** 0.90.

The tasklist covers all required R0 and R1 phases:

| Requirement | Tasklist mapping | Coverage |
|---|---|---|
| R0.1 Spec-ID registry | 2.1-2.8, PG2.1-PG2.3 | Covered |
| R0.2 Anti-instinct allowlist | 3.1-3.8, PG3.1-PG3.3 | Covered |
| R0.3 minimal contracts module | 4.1-4.7, PG4.1-PG4.3 | Covered |
| R0 acceptance | 5.1-5.4, PG5.1-PG5.2 | Covered with CI-classification issue |
| R1.1 contracts extension | 6.1-6.4, PG6.1-PG6.2 | Covered |
| R1.2 PipelineEnvelope | 7.1-7.4, PG7.1-PG7.2 | Covered |
| R1.3 GateCriteria.code_assertions | 8.1-8.4, PG8.1-PG8.2 | Covered |
| R1.4 tool-write rewrite | 9.1-9.12, PG9.1-PG9.2 | Covered but operationally heavy |
| R1.5 verify-implementation | 10.1-10.3, PG10.1-PG10.2 | Covered |
| R1.6 cleanup | 11.1-11.7, PG11.1-PG11.2 | Covered with parser-MVR deviation |
| Skill alignment | 12.1-12.5, PG12.1-PG12.2 | Covered |
| Final acceptance | 13.1-13.7, PG13.1-PG13.2 | Covered |

Deduction: the tasklist permits R1.4 dual-write remnants to remain as tracked follow-up at task completion (line 818), which is operationally honest but weakens the claim that the rewrite has fully inverted markdown-as-substrate.

### 3. Deviation-classification clarity — **3.5/5**

The tasklist maps all 10 Contract items to concrete test files and CI gates, with the clearest final mapping in Step 13.4:

| Contract item | Tasklist mapping | CI/test mapping |
|---|---|---|
| #1 Recurrence fixture | 2.5, 3.4, 11.6, 13.1-13.3 | `test_recurrence_regression.py` |
| #2 Dispatch reachability | 8.3-8.4, 10.3, 13.4 | `test_dispatch_reachability.py` |
| #3 Producer-side constraint | 9.2, 9.4, 9.8, PG9.1, 13.4 | PR-description lint + schema tests |
| #4 No silent PASS | 10.2, 11.5, 13.4 | `test_gate_empty_target.py` |
| #5 No fragility stubs | 4.4-4.5, 11.3, 11.5, 13.4 | `test_no_fragility_stubs.py` / arch-lint |
| #6 Parser consistency | 11.2, 13.4 | `test_parser_consistency.py` |
| #7 Retry mutates input | 11.6, 13.4 | `test_retry_contract.py` |
| #8 Threshold registry | 4.1-4.7, 6.1-6.4, 12.5, 13.4 | `test_threshold_registry.py` |
| #9 ID containment | 2.1-2.8, 9.4, 9.8, 13.4 | `test_spec_roadmap_id_containment.py` |
| #10 False-positive corpus | 3.1-3.5, 13.4 | `test_anti_instinct_recurrence.py` |

PRESERVE targets are mostly honored: tasklist explicitly declares `commands.py`, `structural_checkers.py`, and `convergence.py` out-of-scope/PRESERVE at lines 170-172 and repeats preserve audits in phase gates. I found no checklist item directly instructing edits to `commands.py` or `structural_checkers.py`; `convergence.py` is read/imported but repeatedly constrained as PRESERVE.

Deduction: the Contract gate split is inconsistent between Phase 5 and Phase 13. Phase 5 line 397 says `test_spec_roadmap_id_containment.py` / Contract #9 is pipeline-blocking and `make lint-architecture` / Contract #5 is PR-blocking, but BUILD-REQUEST §Contract says #5 is pipeline-blocking and #9 is PR-review-blocking.

### 4. Risk surface coverage — **4/5**

The tasklist addresses all five master architectural flaws:

| Master flaw | Tasklist coverage |
|---|---|
| Flaw 1 — artifact-centric gates / no code-reaching link | 8.1-8.4 (`CodeAssertion`), 10.1-10.3 (`verify-implementation`), 13.7 acceptance gate #8 |
| Flaw 2 — generator/validator asymmetry | 9.1-9.12 tool-write rewrite; Contract #3 checks in generate/merge schemas |
| Flaw 3 — markdown-as-state | 7.1-7.4 `PipelineEnvelope`; 11.2 parser cleanup; 12.3 skill prose alignment |
| Flaw 4 — retry without mutation / silent skip | 10.2 fail-closed verify step; 11.4 fail-open deletion; 11.5 empty-target gate; 11.6 retry contract |
| Flaw 5 — no cross-skill contract | 4.1-4.7, 6.1-6.4, 12.1-12.5 contracts + prose alignment |

Deduction: Flaw 3 coverage is undermined by the parser canonicalization issue. Keeping `_check_frontmatter` as the canonical parser and exporting it from `superclaude.contracts.parsers` at Step 11.2 preserves a markdown/frontmatter parser as shared state instead of making markdown render-only.

### 5. Recommendation actionability — **4/5**

Most checklist items follow the B2 self-contained pattern: each item names the exact file(s), concrete edits, and a verifier. Examples: 2.2 names `id_registry.py` and its dataclass/functions; 3.5 names the recurrence test and exact assertions; 8.4 names dispatch reachability tests; 10.3 names verify-implementation tests; 13.7 names the acceptance report and verification commands.

Deductions:

- Some items are too large for a single implementer step (9.11 migrates test_strategy + certify + validate-reflect + remediation together).
- Some items include impossible/unsafe pre-fix verification instructions (`checking out before Step 2.4`) inside a long-running implementation checklist; this is testability-useful but operationally awkward.
- The R1.4 3-release cadence is realistic only if treated as a multi-release program, not a single task completion path. The task admits this at line 818, but the frontmatter still estimates one coherent task.

## Coverage Matrix

### R0

- **R0.1 Spec-ID registry:** 2.1 discovery; 2.2 `id_registry.py`; 2.3 extract wiring; 2.4 MERGE_GATE assertion; 2.5 fixture; 2.6 regression test; 2.7 pytest; 2.8 lint; PG2 QA.
- **R0.2 anti-instinct allowlist:** 3.1 seed discovery; 3.2 design; 3.3 implementation; 3.4 fixtures; 3.5 tests; 3.6 pytest; 3.7 lint; 3.8 live MultiModelSwarm run; PG3 QA.
- **R0.3 contracts module:** 4.1 consumer discovery; 4.2 `superclaude.contracts`; 4.3 consumers; 4.4 arch-lint; 4.5 tests; 4.6 validation; 4.7 lint; PG4 QA.
- **R0 acceptance:** 5.1 CI plan/wiring; 5.2 fresh MultiModelSwarm run; 5.3 full R0 lint/sync; 5.4 report; PG5 QA.

### R1

- **R1.1 contracts SoT module:** 6.1 return-contract discovery; 6.2 `RETURN_CONTRACTS`; 6.3 consumer migration; 6.4 tests; PG6 QA.
- **R1.2 PipelineEnvelope:** 7.1 design; 7.2 `envelope.py`; 7.3 post-extractors; 7.4 tests; PG7 QA.
- **R1.3 GateCriteria.code_assertions:** 8.1 design; 8.2 model slot; 8.3 code assertions + certify wiring; 8.4 tests; PG8 QA.
- **R1.4 tool-write:** 9.1 scaffolding; 9.2 extract; 9.3 extract_tdd; 9.4 generate; 9.5 diff; 9.6 debate; 9.7 score; 9.8 merge; 9.9 spec_fidelity; 9.10 wiring_verification; 9.11 secondary prompts/remediation; 9.12 cutover; PG9 QA.
- **R1.5 verify-implementation:** 10.1 design; 10.2 implementation/wiring; 10.3 tests; PG10 QA.
- **R1.6 migration cleanup:** 11.1 inventory; 11.2 parsers; 11.3 stubs; 11.4 fail-open/gate-none; 11.5 contract lints; 11.6 retry contract; 11.7 full validation; PG11 QA.
- **Skill alignment:** 12.1 SKILL.md; 12.2 extraction-pipeline ref; 12.3 templates ref; 12.4 validation ref; 12.5 scoring ref; PG12 QA.
- **Final acceptance:** 13.1 seeding map; 13.2 remaining fixtures; 13.3 recurrence regression; 13.4 final CI; 13.5 tests; 13.6 E2E corpus; 13.7 acceptance audit; PG13 QA.

## Unmapped Requirements

None fully unmapped. Partial/misaligned requirements:

1. **BUILD-REQUEST §MVR parser deletion intent** is not cleanly mapped: tasklist maps parser cleanup to retaining `pipeline/gates.py:_check_frontmatter`, contrary to the MVR's typed-envelope direction.
2. **R1.4 cutover completion** is not guaranteed inside the task: Step 9.12 and follow-up line 818 allow steps to remain dual-write at completion.
3. **Contract CI classification** is internally inconsistent at Phase 5 vs final Phase 13.

## Findings

### Critical

**C1 — R1.6 preserves a canonical frontmatter parser, contradicting the MVR substrate inversion.**  
The BUILD-REQUEST §MVR says `PipelineEnvelope` sidecar JSON makes markdown render-only and that one `_parse_frontmatter` lives in the post-step extractor only; it explicitly says the divergent variants at `gates.py:168` and `_check_frontmatter` are deleted. The tasklist instead says to canonicalize on `pipeline/gates.py:_check_frontmatter L91` at Step 10 and Step 11.2, then export it from `superclaude.contracts.parsers`. Current code confirms `_check_frontmatter` is a gate-level frontmatter parser at `src/superclaude/cli/pipeline/gates.py:91-128`, while the other duplicate parser exists at `src/superclaude/cli/roadmap/gates.py:168-189`. This risks preserving markdown-as-state under a new package name.  
**Task citations:** 10, 11.2. **Source citations:** `src/superclaude/cli/pipeline/gates.py:91-128`; `src/superclaude/cli/roadmap/gates.py:168-189`.

### High

**H1 — Phase 5 CI classification contradicts the Contract pass criterion.**  
BUILD-REQUEST §Contract pass criterion makes Contract items 1, 2, 4, 5 pipeline-blocking and 3, 6-10 PR-review-blocking. Tasklist Step 5.1 says Contract #9 is pipeline-blocking and Contract #5 is PR-blocking, while Step 13.4 later uses the correct split. This internal inconsistency can wire R0 CI incorrectly before final cleanup.  
**Task citations:** 5.1, 13.4.

**H2 — R1.4 cutover can remain incomplete at task completion.**  
Step 9.12 correctly defines `>=3 consecutive parity-passing releases` before deletion, but it also starts at 0 cycles and line 818 explicitly tracks any R1.4 sub-step that remains dual-write at completion. That is honest project management, but it means the task can mark completion while markdown paths remain production default for some steps, weakening the rewrite acceptance claim.  
**Task citations:** 9.12, follow-up item line 818.

**H3 — `CodeAssertion`/`GateCriteria` migration under-specifies gate API compatibility.**  
Current `GateCriteria` accepts only `required_frontmatter_fields`, `min_lines`, `enforcement_tier`, and `semantic_checks` at `src/superclaude/cli/pipeline/models.py:90-105`. The task asks to add `code_assertions` and also design `required_envelope_fields`, but most existing gates still consume frontmatter and `gate_passed()` currently calls `_check_frontmatter`. The task covers backward compatibility but not a crisp migration rule for when `required_frontmatter_fields` is retired versus coexisting with `required_envelope_fields`. This could leave dual gate contracts indefinitely.  
**Task citations:** 8.1, 8.2, 11.2. **Source citation:** `src/superclaude/cli/pipeline/models.py:90-105`.

### Medium

**M1 — R1.4 secondary migration step is too large and may hide partial failures.**  
Step 9.11 combines test_strategy, certify, validate-reflect, and remediation tool-write migrations into one item. It is less B2-self-contained than the primary 9 sub-steps and should be split into separate steps or separate phaselets with independent parity gates.

**M2 — Recurrence corpus realism is deferred too late.**  
The task seeds some fixtures early, but the full per-RECURRENT-row seeding map and remaining ~15 fixtures are deferred to Phase 13. Contract #1 says every future fix must add a named fixture for the specific failure shape being closed; delaying most fixture derivation until terminal acceptance risks implementing fixes before realistic failure-class fixtures constrain them.  
**Task citations:** 13.1, 13.2.

**M3 — Current task file includes placeholder log entries that look completed.**  
The execution log includes template entries for task started and completed with `[YYYY-MM-DD HH:MM]` placeholders. This is not an implementation defect, but it is a QA hazard: automation or human reviewers may misread placeholders as actual status.  
**Task citation:** Task Log / Notes lines 756-764.

## Risk-Surface Coverage vs Master Flaws 1-5

- **Flaw 1 artifact-centric gates:** Strong coverage via 8.1-8.4 and 10.1-10.3. The dispatch-reachability invariant directly targets `build_certify_step` dead code; current code confirms `build_certify_step` exists at `src/superclaude/cli/roadmap/executor.py:1899-1944` and `_build_steps` only has a comment about dynamic certify construction at `src/superclaude/cli/roadmap/executor.py:2205`.
- **Flaw 2 generator/validator asymmetry:** Strong conceptual coverage via 9.1-9.12, especially generate/merge schema rejection of phantom IDs. Risk: Step 9.12 can leave production default on markdown path.
- **Flaw 3 markdown-as-state:** Partial coverage. `PipelineEnvelope` is covered, but parser canonicalization conflicts with the MVR.
- **Flaw 4 retry/no mutation + silent skip:** Good coverage via fail-open deletion, gate-empty-target test, retry-contract test. Current fail-open evidence is grounded in `src/superclaude/cli/roadmap/fidelity_checker.py:287-303` and `314-337`.
- **Flaw 5 cross-skill contracts:** Good coverage via `superclaude.contracts`, arch-lint, skill prose alignment, threshold registry, and final CI checks.

## PRESERVE-Target Audit

- **`src/superclaude/cli/roadmap/commands.py`:** Preserved. Tasklist declares out-of-scope at line 170 and repeatedly QA-checks it unchanged.
- **`src/superclaude/cli/roadmap/structural_checkers.py`:** Preserved. Tasklist declares out-of-scope at line 171 and QA-checks it unchanged in PG9/PG11/PG13.
- **`src/superclaude/cli/roadmap/convergence.py`:** Mostly preserved. Tasklist declares out-of-scope at line 172 and warns not to modify it in 7.2/7.3/9.9/11.4. Some imports/read-only use are planned, which is acceptable. Watch `SPEC_FIDELITY_GATE_CONVERGENCE_AWARE` to ensure it does not mutate `convergence.py` public API.

## Recommendation

**Refactor-then-ship.** Required pre-execution edits:

1. Rewrite Steps 10 / 11.2 / 12.3 so the MVR parser plan is: envelope/post-step extractor is the only parser authority for roadmap gates; `_check_frontmatter` is not re-exported as a durable contract parser for the rewritten roadmap pipeline. If a legacy parser remains for non-roadmap consumers, mark it legacy/out-of-roadmap-gate-path and test that roadmap gates consume envelope fields.
2. Fix Step 5.1 CI classification: Contract #5 must be pipeline-blocking; Contract #9 must be PR-review-blocking with override-with-reason, matching Step 13.4 and BUILD-REQUEST §Contract.
3. Split Step 9.11 into four independent sub-steps.
4. Move recurrence fixture derivation for each failure class closer to the phase that closes it, or add per-phase blocker language that no fix can land before its Contract #1 fixture exists.
5. Replace placeholder execution-log entries with comments only, or make clear they are examples not actual log entries.
