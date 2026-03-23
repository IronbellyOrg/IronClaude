# Unified Eval Design Proposal — v3.05 Deterministic Fidelity Gates, v3.1 Anti-Instincts Gate, and v3.2 Wiring Verification Gate

**Date**: 2026-03-21
**Purpose**: Provide a single, evidence-first proposal document that can be executed via `sc:task` to build a real eval portfolio covering v3.05, v3.1, and v3.2.
**Execution intent**: This document is tasklist-source material, not a unit-test plan. Every recommended eval must invoke the real CLI pipeline and produce third-party-verifiable artifacts.

---

## 1. Purpose and evidence thesis

This proposal defines the smallest convincing eval portfolio that can prove the three releases materially improved the roadmap pipeline in the exact failure classes they were intended to address:

- **v3.1 Anti-Instincts Gate** should surface roadmap/spec omissions that previously looked superficially complete.
- **v3.2 Wiring Verification Gate** should surface code that is defined but not actually wired into runtime behavior.
- **v3.05 Deterministic Fidelity / TurnLedger** should prove remediation and convergence are economically governed, artifact-backed, and not just retry loops with opaque stopping behavior.

The evidence standard is strict:

1. The eval must invoke the **real CLI pipeline**.
2. The eval must produce **inspectable disk artifacts**.
3. Pass/fail must be **third-party verifiable from artifacts**, not inferred from internal state.
4. Findings based on absence of evidence or indirect inference must be labeled **INFERENTIAL**.

This proposal intentionally rejects fake confidence from unit tests that exercise gate functions without executing the real workflow.

---

## 2. Source inputs and release traceability

Use these exact source files as the authoritative basis for all eval design and implementation:

- `/config/workspace/IronClaude/.dev/releases/complete/v3.05_DeterministicFidelityGates/turnledger-refactor-proposal-agent1.md`
- `/config/workspace/IronClaude/.dev/releases/complete/v3.2_fidelity-refactor___/wiring-verification-gate-v1.0-release-spec.md`
- `/config/workspace/IronClaude/.dev/releases/complete/v3.1_Anti-instincts__/anti-instincts-gate-unified.md`

### Release-by-release evidence goals

#### v3.1 — Anti-Instincts Gate
Must prove that the system now emits explicit evidence for:
- dropped identifiers
- missing wiring/integration tasks
- scaffold/mock/no-op language with no later discharge
- extraction-stage requirement loss or suspicious adequacy gaps

Primary expected artifacts:
- `extraction.md`
- `roadmap.md`
- `anti-instinct-audit.md`

#### v3.2 — Wiring Verification Gate
Must prove that the system now emits explicit code-level evidence for:
- optional callables never meaningfully injected
- orphan provider modules
- unwired registries or unresolved dispatch targets
- suspicious analyzer null results caused by directory/config mismatch

Primary expected artifacts:
- `wiring-report.md`
- sprint/task result artifacts
- gate/KPI summaries if emitted by the pipeline

#### v3.05 — Deterministic Fidelity / TurnLedger
Must prove that the system now emits explicit economic/convergence evidence for:
- bounded progress under budget pressure
- halt reasons tied to budget/guard semantics
- visible debit/credit/progress evidence rather than generic retry exhaustion

Primary expected artifacts:
- convergence result/diagnostic artifact
- halt-reason-bearing output
- budget/debit/credit traces if emitted by the real pipeline

---

## 3. Parallel brainstorm outputs summarized

This proposal synthesizes three independent brainstorm tracks:

### Track A — Historical failure reproduction
Goal: reproduce realistic failure modes these releases were created to catch.

Highest-value candidates:
1. roadmap omission of explicit wiring tasks
2. scaffold/mock/no-op steps never discharged
3. dropped code-level identifiers in roadmap generation
4. extraction under-capture of structurally rich requirements
5. unwired optional callable in real generated code
6. orphan provider module never consumed
7. registry entry that looks present but does not resolve correctly
8. convergence/remediation loop that appears active but is economically uncontrolled

### Track B — Before/after comparative proof
Goal: show what previously passed silently but should now fail or emit evidence.

Most convincing comparisons:
1. pre-v3.1 silent omission vs post-v3.1 uncovered contracts
2. pre-v3.1 scaffold drift vs post-v3.1 undischarged obligation evidence
3. pre-v3.2 silent unwired code vs post-v3.2 `wiring-report.md`
4. pre-v3.1 hidden identifier loss vs post-v3.1 fingerprint coverage artifact
5. pre-v3.1 invisible extraction undercount vs post-v3.1 adequacy warning/evidence
6. pre-v3.05 generic non-convergence vs post-v3.05 structured halt reasons and budget evidence

### Track C — Adversarial blind-spot pressure
Goal: try to make the system look correct while hiding the exact failure classes the releases target.

Strongest blind-spot tests:
1. provider-dir null-result masking
2. identifier appendix laundering
3. optional callable dummy injection
4. generic “wire integrations” placebo task
5. same-phase scaffold “discharge” laundering
6. dead-import orphan suppression
7. importable-but-nonfunctional registry entries
8. cosmetic structural progress to game convergence credit

---

## 4. Normalized eval comparison matrix

| Eval ID | Eval title | Category | Primary target release(s) | Real artifact(s) expected | Detection mechanism exercised | Proof strength | Setup complexity | False-positive risk | Priority |
|---|---|---|---|---|---|---|---|---|---|
| E01 | Omission recovery | reproduction | v3.1 | `roadmap.md`, `anti-instinct-audit.md` | contract extraction + uncovered contracts | High | Medium | Low-Med | P1 |
| E02 | Scaffold discharge failure | reproduction | v3.1 | `anti-instinct-audit.md` | obligation scanner | High | Low | Med | P1 |
| E03 | Fingerprint loss | comparative | v3.1 | `anti-instinct-audit.md` | fingerprint coverage | Medium | Low | Med | P2 |
| E04 | Extraction adequacy loss | reproduction | v3.1 | `extraction.md`, structural warning, audit context | structural audit | Medium | Medium | Med | P2 |
| E05 | Unwired optional callable | reproduction | v3.2 | `wiring-report.md`, sprint result | unwired callable analysis | High | Medium | Low | P1 |
| E06 | Orphan module | reproduction | v3.2 | `wiring-report.md` | orphan module analysis | High | Medium | Low-Med | P1 |
| E07 | Broken registry target | reproduction | v3.2 | `wiring-report.md` | registry resolution analysis | High | Medium | Low | P1 |
| E08 | Provider-dir null masking | adversarial | v3.2 | suspicious zero-findings report + warning path | first-run sanity / provider-dir validation | High | Medium | Low | P1 |
| E09 | TurnLedger convergence economics | reproduction | v3.05 | convergence result, halt reason, budget traces | launch/remediation budget guards | High | Medium | Low | P1 |
| E10 | Cosmetic progress gaming | adversarial | v3.05 | convergence diagnostics, repeated credits/debits | forward-progress credit logic | Medium | High | Med | P3 |
| E11 | Mocked-steps to unwired-runtime composite | composite | v3.1 + v3.2 | audit + wiring report | obligation + wiring | High | High | Low-Med | P1 |
| E12 | Spec omission to roadmap drift to wiring failure composite | composite | v3.1 + v3.2 | extraction, audit, wiring report | structural + contract + wiring | Very High | High | Low | P1 |
| E13 | Superficially complete but operationally disconnected pipeline | adversarial composite | v3.1 + v3.2 + v3.05 | cross-release artifact bundle | cross-release composite | Very High | High | Med | P2 |

---

## 5. Deduplicated eval families

### 5.1 Economic convergence evidence — v3.05
- **E09** TurnLedger convergence-economics core eval
- **E10** cosmetic-progress adversarial stress eval

### 5.2 Omission and scaffolding evidence — v3.1
- **E01** omission recovery core eval
- **E02** scaffold discharge core eval
- **E03** fingerprint-loss supporting comparative eval
- **E04** extraction adequacy supporting eval

### 5.3 Code wiring evidence — v3.2
- **E05** unwired optional callable core eval
- **E06** orphan module core eval
- **E07** broken registry core eval
- **E08** analyzer-misconfiguration blind-spot eval

### 5.4 Cross-cutting composite evals
- **E11** mocked-steps-to-unwired-runtime composite
- **E12** spec omission → roadmap drift → code wiring failure composite
- **E13** superficially complete but operationally disconnected pipeline

---

## 6. Final recommended eval portfolio

### 6.1 Minimum convincing set

This is the smallest portfolio that still proves the releases work in a skeptic-proof way.

#### Core eval 1 — Anti-Instincts omission recovery eval
Seed a spec/roadmap scenario with:
- dropped identifiers
- missing explicit wiring tasks
- scaffold/mock/no-op language

Expected artifact outcomes:
- `anti-instinct-audit.md` shows uncovered contracts
- `anti-instinct-audit.md` shows undischarged obligations
- fingerprint coverage and missing-fingerprint evidence are inspectable

Why this belongs:
- It directly targets the primary v3.1 claim: superficially complete output is no longer accepted without explicit evidence.

#### Core eval 2 — Wiring verification integration-gap eval
Seed defined-but-not-wired runtime patterns such as:
- optional callable never meaningfully injected
- orphan module never consumed
- registry/dispatch target not truly connected

Expected artifact outcomes:
- `wiring-report.md` shows non-zero findings with file-backed evidence
- gate outcome is explicit and inspectable

Why this belongs:
- It directly targets the primary v3.2 claim: code integration failures are no longer invisible.

#### Core eval 3 — TurnLedger convergence-economics eval
Seed a convergence/remediation workflow with:
- bounded forward progress
- budget pressure
- at least one opportunity for debit/credit behavior

Expected artifact outcomes:
- explicit halt/progress evidence
- budget-aware stop reason instead of generic failure

Why this belongs:
- It directly targets the primary v3.05 claim: convergence is economically governed and explainable.

### 6.2 Composite evals

#### Composite eval 4 — Mocked-steps-to-unwired-runtime composite
Chain a planning-stage omission into a runtime-stage wiring gap.

Expected proof shape:
- v3.1 should object to mocked/scaffolded steps without discharge
- if that debt propagates, v3.2 should emit code-level wiring findings

#### Composite eval 5 — Spec omission to roadmap drift to code wiring failure composite
Begin with spec/extraction loss, continue through roadmap omission, and end in an unwired implementation.

Expected proof shape:
- extraction/structural evidence
- anti-instinct evidence
- wiring evidence

### 6.3 Adversarial stretch eval

#### Stretch eval 6 — Superficially complete but operationally disconnected pipeline scenario
Combine the hardest blind spots into one scenario:
- identifiers mentioned but not planned
- vague integration tasks that sound correct
- runtime injection that is present but operationally inert
- convergence progress that appears positive without meaningful closure

This eval is intentionally expensive and should be implemented after the five higher-confidence evals.

---

## 7. Required seeded inputs / fixtures / specs

### 7.1 v3.1 fixture requirements
Create at least one spec fixture containing:
- explicit registry/dispatch/injection requirements
- multiple concrete identifiers that should survive into roadmap tasks
- scaffold/mock/no-op language requiring later discharge
- structurally rich sections to exercise extraction adequacy logic

### 7.2 v3.2 fixture requirements
Create at least one real code-generation or sprint fixture containing:
- optional callable defaulted but not meaningfully injected
- provider/orphan module that exists but is not consumed
- registry entry that appears present but does not resolve or does not connect to real execution
- directory layout variant that can trigger analyzer null-result risk

### 7.3 v3.05 fixture requirements
Create at least one convergence fixture containing:
- bounded but insufficient progress
- at least one remediation trigger
- at least one regression/debit opportunity if that path is part of the pipeline
- enough pressure to make halt reason and budget semantics visible in artifacts

### 7.4 Composite fixture requirements
Build composite fixtures that deliberately exercise two or more releases in one run:
- mocked/scaffolded roadmap item that later materializes as unwired runtime behavior
- dropped spec requirement that disappears in roadmap and later manifests as disconnected implementation

---

## 8. Required real artifacts per eval

Each eval must define its required artifact set before implementation.

### v3.1 artifact contract
At minimum:
- `extraction.md` when extraction is part of the run
- `roadmap.md`
- `anti-instinct-audit.md`

### v3.2 artifact contract
At minimum:
- `wiring-report.md`
- task/sprint result artifact showing gate outcome

### v3.05 artifact contract
At minimum:
- convergence result/diagnostic artifact
- halt reason or equivalent budget/convergence status artifact

### Composite artifact contract
At minimum:
- one artifact from each targeted release’s proof surface
- explicit cross-artifact mapping that shows how the same seeded defect propagated

### Rejection rule
An eval is not acceptable if the proof depends only on:
- console logs without persisted artifacts
- internal memory/state that a third party cannot inspect
- reading source code to infer what the gate “must have done”

---

## 9. Pass/fail interpretation rules

### Pass
An eval passes if:
1. the real CLI pipeline runs,
2. the required artifacts are produced,
3. the artifacts explicitly show the expected gate behavior for the seeded defect,
4. the outcome is interpretable by a third party without insider context.

### Fail
An eval fails if:
1. no required artifact is produced,
2. the seeded defect is not reflected in artifacts,
3. the pipeline silently passes a defect that the target release claims to catch,
4. the result is only explainable by reading code rather than inspecting output artifacts.

### Ambiguous
Mark as ambiguous if:
- warning-only behavior occurs without stable persisted evidence,
- an artifact shows a superficially positive summary but lacks defect-specific detail,
- a zero-finding result appears without required null-result sanity warnings.

Ambiguous evals should not count toward the minimum convincing set until tightened.

---

## 10. Ranking rubric for implementation priority

Rank candidates by this order:

1. Uses the **real CLI pipeline**
2. Produces **third-party-verifiable artifacts**
3. Directly targets the **stated release goal**
4. Has **low ambiguity** in interpreting pass/fail
5. Is convincing to a **skeptical reviewer**
6. Has reasonable implementation cost

This rubric yields the following portfolio order:

1. **C1** Anti-Instincts omission recovery
2. **C2** Wiring verification integration-gap
3. **C3** TurnLedger convergence-economics
4. **X1** Mocked-steps-to-unwired-runtime composite
5. **X2** Spec omission → roadmap drift → wiring failure composite
6. **A1** Superficially complete but operationally disconnected pipeline scenario

---

## 11. Implementation sequencing

Recommended build order:

1. **v3.1 omission/scaffolding eval**
   - fastest route to artifact-backed proof
   - clarifies roadmap-side fixture vocabulary for later composite runs

2. **v3.2 wiring verification eval**
   - next highest proof value
   - directly verifies file-backed runtime integration evidence

3. **v3.05 TurnLedger economic eval**
   - then validate convergence/budget semantics
   - may require more calibration than v3.1/v3.2

4. **Composite cross-release evals**
   - once single-release proof surfaces are stable

5. **Adversarial stretch eval**
   - last, after artifact contracts and thresholds are already hardened

---

## 12. Risks and ambiguity controls

### Risk 1 — Artifact-free “proof”
Control:
- reject any eval that cannot point to concrete files produced by the real run

### Risk 2 — Presence mistaken for planning
Control:
- do not accept identifier presence alone as proof; require task/action mapping where applicable

### Risk 3 — Zero-findings mistaken for cleanliness
Control:
- require sanity signaling for suspicious first-run zero-finding cases

### Risk 4 — Warning-only outputs too weak for release proof
Control:
- label warning-only evals as supporting evidence, not core proof, unless they persist stable artifacts

### Risk 5 — Overly expensive adversarial scenarios blocking initial delivery
Control:
- sequence adversarial stretch last and deliver the minimum convincing set first

### Risk 6 — v3.05 proposal/implementation drift
Control:
- verify final real artifact names and fields when implementing the TurnLedger evals; treat assumptions from the proposal as provisional until observed in the current pipeline

---

## 13. Tasklist-ready implementation breakdown

### Story 1 — Create seeded input scenarios
1. Create v3.1 omission/scaffold spec fixture
2. Create v3.2 unwired runtime fixture
3. Create v3.05 convergence-budget fixture
4. Create composite fixture for mocked-steps → unwired-runtime
5. Create composite fixture for spec omission → drift → wiring failure
6. Create adversarial stretch fixture

### Story 2 — Define execution harness for real CLI runs
7. Define canonical roadmap-run invocation for v3.1 evals
8. Define canonical sprint/code-run invocation for v3.2 evals
9. Define canonical convergence-run invocation for v3.05 evals
10. Standardize output capture locations per eval
11. Add deterministic wrapper or runner script if needed for repeatable artifact collection

### Story 3 — Capture and formalize expected artifacts
12. Define artifact contract for v3.1 evals
13. Define artifact contract for v3.2 evals
14. Define artifact contract for v3.05 evals
15. Define cross-release artifact mapping contract for composite evals

### Story 4 — Implement artifact verification
16. Implement verifier for `anti-instinct-audit.md`
17. Implement verifier for `wiring-report.md`
18. Implement verifier for convergence/halt artifact
19. Implement cross-release verifier for composite evals
20. Implement “third-party verifiable” guard that rejects log-only proof

### Story 5 — Run pilot evals
21. Pilot C1 omission recovery eval
22. Pilot C2 wiring integration-gap eval
23. Pilot C3 TurnLedger convergence-economics eval
24. Pilot X1 mocked-steps-to-unwired-runtime composite
25. Pilot X2 omission-to-drift-to-wiring composite
26. Pilot A1 adversarial stretch eval

### Story 6 — Review false positives and ambiguity
27. Review v3.1 wording sensitivity and obligation vocabulary edge cases
28. Review v3.2 intentional optional-hook / whitelist cases
29. Review v3.2 provider-dir null-result sanity behavior
30. Review v3.05 progress-credit and halt-reason interpretation edge cases

### Story 7 — Finalize acceptance thresholds
31. Freeze v3.1 pass/fail thresholds
32. Freeze v3.2 pass/fail thresholds
33. Freeze v3.05 pass/fail thresholds
34. Freeze composite eval scoring and acceptance rules

---

## 14. Final recommendation

Implement **six evals** first:

- **3 core evals** — one per release
- **2 composite evals** — to prove cross-release interactions
- **1 adversarial stretch eval** — strongest skeptic-proof scenario

This is the smallest portfolio that still convincingly demonstrates:
- roadmap omissions are surfaced,
- unwired runtime integrations are surfaced,
- convergence is economically controlled,
- and interactions across releases are not merely locally correct.

---

## 15. Suggested `sc:task` handoff usage

Suggested next action:

```text
/sc:task --parallel Use /config/workspace/IronClaude/.dev/releases/complete/v3.2_fidelity-refactor___/unified-eval-design-proposal-v3.05-v3.1-v3.2.md as the source proposal. Convert Section 13 into an implementation-ready tasklist bundle for building the minimum convincing eval set (C1, C2, C3, X1, X2, A1). Preserve the real-artifact evidence standard and reject any unit-test-only approach.
```

If desired, a narrower first handoff can target only the first three core evals before generating the composite and adversarial follow-up work.
