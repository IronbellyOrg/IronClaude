---
title: "Troubleshoot Pipeline Hardening — Release Spec (G1)"
version: "1.1.0"
status: draft
feature_id: TSH-HARDEN-1
parent_feature: null
spec_type: infrastructure
complexity_score: 0.85
complexity_class: HIGH
target_release: "4.3.0-proposed"
authors: [user, claude]
created: 2026-06-10
quality_scores:
  clarity: 9.0
  completeness: 8.8
  testability: 9.0
  consistency: 8.8
  overall: 8.9
---

<!-- Provenance: produced by /sc:spec-panel (fresh release-spec from troubleshoot-pipeline-hardening-spec.md + EFFICACY-REPORT-MERGED.md §3/§9/§10/AppA). Panel: 11 experts, --focus correctness, 2 iterations. Mandatory correctness artifacts embedded (§2.2, §4.5, §5.2) with full versions under spec-panel/. -->

## 1. Problem Statement

The `/sc:troubleshoot` + `sc:troubleshoot-protocol` assurance stack diagnoses issues quickly but does **not** prevent a recurring class of *pipeline escape*: a defect that lives at a runtime, generated-artifact, shared-contract, or independent-review boundary, where a review can sign off from an *adjacent* proof (a command string, an edited helper, a PASS artifact, a generic evaluator path) while the real boundary still fails. Across the canonical episode every escape (E1–E5) surfaced at **runtime**, never by the design-stage review surface. This work hardens the protocol so that, when a diagnosed issue is a pipeline escape, remediation is not "complete" until the protocol proves the invariant at the same boundary where the escape can recur — via reusable, mechanism-based gates rather than issue-specific patches.

### 1.1 Evidence

| Evidence | Source | Impact |
|----------|--------|--------|
| E1 — PRD cloud `--file` misuse: helper/argv proof accepted while headless subprocess rejected local paths | `escape-E1-*/root-cause.md`; merged report §3 (MERGED #151 `7601ad25`) | Runtime crash; sibling pipelines already avoided the pattern |
| E2 — completion-phase false positive: substring phase matcher (`complete`⊂`incomplete`) enforced parallel-work invariant on a sequential bookend | `escape-E2-*/root-cause.md`; merged report §3 (MERGED #154 `e97aa4fd`) | Real work phases silently exempted; caught only by #154 review `r3383060121` |
| E3 — Task-Log heading sibling false positive: E2 fix not swept across same-token siblings | `escape-E3-*/root-cause.md`; merged report §3 (MERGED #155 `eb9a2633`) | Hard gate halted on non-executable placeholder headings |
| E4 — evaluator divergence: shared `SemanticCheck.advisory` honored by generic `gate_passed` but not by PRD `_evaluate_gate` | `escape-E4-*/root-cause.md`; merged report §9 (UNMERGED `b97c9960`) | Advisory treated as fatal on the live PRD path; fix committed-but-unmerged |
| E5 — POST-reflect wrong diff base: review selector audited a range omitting dirty `/task` work, possibly including foreign commits | `escape-E5-*/root-cause.md`; merged report §3 (MERGED #153 `10723863`) | Independent review consumed the wrong surface (false assurance) |
| External corroboration: consumer-driven contract testing, allow-list validation, conformance fixtures, executable terminal-state handling, explicit recovery semantics | merged report Appendix A (Pact, NCSC/OWASP, CommonMark, .NET-regex, Step Functions, Argo; 24/25 claims 3-0) | Validates the *design direction*; does not prove efficacy |

### 1.2 Scope Boundary

**In scope**: A new `Pipeline Hardening Closure` protocol mode for `sc:troubleshoot-protocol`, gated by waves H0–H5, a cross-cutting waiver/no-re-greening invariant, an additive versioned skill output contract, and a `REPORT.md` closure section. Reusable gates that generalize to future escapes E6+.

**Out of scope**: The product point-fixes themselves (E1/E2/E3/E5 already merged; E4 fix `b97c9960` committed-but-unmerged and tracked separately). Building/validating the hardening (this is the G1 spec; implementation is **halted pending G1 approval**). Any edit to `src/superclaude/` or `.claude/` skill/command files before approval.

## 2. Solution Overview

Add a **Pipeline Hardening Closure** mode that triggers after Tier-1 diagnosis when an issue touches a pipeline boundary. The mode runs an ordered wave pipeline (H0→H5). Each wave is an atomic, testable gate that rejects a specific *proof substitution* (command-string for runtime proof; PASS artifact for effective-input proof; edited-helper for runtime-evaluator proof; one-repro for unmask-and-sweep; generic-proof for all-consumer parity; off-path review of an empty/stale/foreign surface). A cross-cutting **waiver-policy invariant** ensures a waived or absent runtime probe downgrades the verdict to `blocked`/`advisory` and can **never** be re-greened to `pass`/`success` by a downstream stage. The command stays thin (advertise + handoff); all logic lives in the skill + refs.

### 2.1 Key Design Decisions

| Decision | Choice | Alternatives Considered | Rationale |
|----------|--------|------------------------|-----------|
| Gate granularity | Atomic FRs (FR-1..FR-13) over named waves | Prose waves only | Panel (Wiegers): prose waves are not verifiable; each gate must be a SMART, traceable requirement |
| Wave numbering | Adopt the draft's H0–H5 scheme as canonical | Merged report §10's variant (H3=classifier, H4=unmask, H5=effective-input) | Avoid a 4th competing scheme (the INV-006 collision lesson); §13 glossary records the crosswalk |
| Waiver semantics | Waived/absent runtime probe ⇒ verdict downgrade to `blocked`/`advisory`, one-way `partial` latch | Allow waiver to keep `pass` with a note | Anti-theatre: the entire episode came from accepting adjacent proof; a re-greenable waiver reintroduces theatre |
| Command vs skill | Thin command, fat skill + refs | Put hardening logic in command | Fowler: interface segregation; keep `/sc:troubleshoot` a handoff |
| Output contract | Additive + **versioned** (`contract_version`) | Add fields unversioned | Newman: existing result consumers must not break on new fields |
| `known_escapes_caught` | Each claimed escape must cite the evidence card that would catch it | Free-list of escape IDs | Adversarial F-A1: an un-earned list inflates coverage to E1–E5 |

### 2.2 Workflow / Data Flow

> Quantity Flow Diagram (mandatory correctness artifact; full version: `spec-panel/quantity-flow-diagram.md`). Count-divergence points are where gates historically measured the *enumerated/present* count and assumed it equalled the *true* count.

```
[Diagnosis: 1 issue]
      |
      v
[H0 Applicability] --applicable=false (+reason+boundary scan)--> [skip H1-H5, report]
      | applicable=true
      v
[H1 Runtime-entrypoint]  produce: entrypoint proof + >=1 negative control (witness FAIL w/ fix reverted)
      |
      v
[H2 Contract ledger]  N_true live consumers --enumerate--> M classified
        DIVERGENCE: FAIL unless M >= N_discovered AND unclassified==0 AND ledger non-empty
        (E4 scenario: N_enum=0 -> "0 unclassified" PASS, but N_true=2: gate_passed + _evaluate_gate)
      |
      v
[H3 Unmask-and-sweep]  1 anchor failure --fan-out--> K_true sibling surfaces
        DIVERGENCE: FAIL unless K_swept covers the full same-token/same-shape family
        (E3 scenario: 1 fix -> 4 sibling 'Findings' headings; sweeping 1 -> 3 escape)
        includes whole-artifact classifier boundary test + word-boundary/near-miss fixtures
      |
      v
[H4 Effective-input proof]  selector --resolve--> E commits/files
        DIVERGENCE: FAIL unless |E ∩ true_runtime_surface| proven correct (NOT merely E>0)
        (E5 scenario: selector -> 5 commits, intersection with real /task work = 0)
      |
      v
[H5 Off-path review]  required|performed|waived_with_rationale|not_required
      |
      v
[Closure verdict: pass | blocked | advisory]  <-- waiver/no-re-green latch: never upgrade downstream
```

## 3. Functional Requirements

> 13 atomic, testable requirements. Traceability: each maps to a wave and to the escape(s) it closes. Acceptance criteria encode the CRITICAL adversarial fixes.

### FR-1: Applicability Gate (H0)

**Description**: The protocol classifies whether the diagnosed issue is a pipeline escape/boundary change and sets `pipeline_hardening_applicable`.

**Acceptance Criteria**:

- [ ] When the issue touches any trigger boundary (CLI/subprocess, file/stdin/prompt delivery, generated-artifact parser, gate/severity/status enum, duplicated evaluator, persisted/resume state, review/audit selector, sibling pipeline, prior-escape unmask), `pipeline_hardening_applicable=true` and H1–H5 cannot be **silently** skipped; each wave must produce `PASS`, `FAIL`, or `N/A` with a valid rationale/waiver that feeds §5.4 aggregation.
- [ ] When skipped, the report records `pipeline_hardening_applicable=false`, a one-sentence reason, **and** the boundary scan that justifies the skip (a bare "looks local" is invalid).

**Dependencies**: None (entry wave).

### FR-2: Mechanism Statement (H0)

**Description**: H0 emits a one-paragraph, feature-agnostic mechanism statement and a candidate `known_escapes_caught` set.

**Acceptance Criteria**:

- [ ] Mechanism statement avoids feature-specific wording except where required as evidence.
- [ ] Each candidate escape ID in `known_escapes_caught` is justified by the wave/card that would catch it (see FR-12 anti-inflation rule).

**Dependencies**: FR-1.

### FR-3: Runtime-Entrypoint Verification (H1)

**Description**: Prove the production/operator entrypoint consumes/rejects the value at the real boundary, not at a helper.

**Acceptance Criteria**:

- [ ] H1 **FAILs** if proof stops at helper construction while the defect can appear only at a subprocess/gate/generated-artifact-parser/persisted-state/review-selector boundary.
- [ ] The evidence card records producer · transformer(s) · consumer/evaluator · boundary crossed · replay command · evidence the replay reaches the production boundary · external outcome asserted.
- [ ] Closes E1 (headless `--spec` replay rejects local-path `--file`), supports E4 (proves the live PRD path reaches `_evaluate_gate`).

**Dependencies**: FR-1.

### FR-4: Negative-Witness Requirement (H1)

**Description**: H1 requires at least one negative control: the oracle run against real captured input through the production entrypoint **with the fix reverted, showing FAIL**, paired with the positive (fix applied, PASS).

**Acceptance Criteria**:

- [ ] A green H1 is rejected unless a negative witness is recorded for every contract with a forbidden interpretation (local path as cloud file; advisory as fatal; dirty work omitted; empty artifact accepted; non-executable heading treated as executable).
- [ ] A test never observed to fail (no negative witness) does not satisfy H1.

**Dependencies**: FR-3.

### FR-5: Contract-Enumeration Ledger (H2)

**Description**: Build a producer/transformer/consumer ledger for the changed contract (field, flag, parser rule, semantic check, selector, status, predicate).

**Acceptance Criteria**:

- [ ] H2 **FAILs** if any live consumer is unclassified, if generic/shared proof is used for a product path without proving the product path reaches that implementation, **or if the ledger is empty/zero-row** (an empty ledger does NOT vacuously pass — fixes adversarial F-N3).
- [ ] The ledger enumerates ≥ the consumer count discovered by symbol/reference + semantic search; a `dead/legacy` Role requires an unreachability proof, not an assertion.
- [ ] Closes E4 (generic gate + PRD evaluator + trailing gate + remediation dispatch inventoried before closure).

**Dependencies**: FR-1.

### FR-6: Sibling / Duplicate-Evaluator Sweep (H2)

**Description**: When a concept is shared, sweep sibling pipelines and duplicate evaluators.

**Acceptance Criteria**:

- [ ] H2 FAILs if sibling pipelines/duplicate evaluators are not swept when the concept is shared.
- [ ] Closes E1 (PRD identified as sibling-contract outlier vs roadmap/tasklist/validate file delivery).

**Dependencies**: FR-5.

### FR-7: Whole-Artifact Classifier Boundary Test (H3)

**Description**: Test gates/parsers against **full generated artifacts** containing executable positives AND sibling negatives, not snippets.

**Acceptance Criteria**:

- [ ] Required controls: a positive case (intended violation still caught), a sibling/off-path negative (same-token/same-shape non-target does NOT hard-fail), a full-artifact case containing both, and a severity assertion (HALT/WARN/CONTINUE) per runtime consumer.
- [ ] Closes E2/E3 (setup/work/completion/Task-Log/findings headings classified by role/topology, not position).

**Dependencies**: FR-3.

### FR-8: Near-Miss Negatives + Allow-List Grammar + Word-Boundary Rule (H3)

**Description**: Behavior-controlling string matches use allow-list grammars with explicit boundaries and named near-miss negative fixtures.

**Acceptance Criteria**:

- [ ] Phase/verdict/completion-signal/resume-token matching uses word-boundary-anchored matching (`\b` / `re.escape` / exact grammar), **promoted from appendix to a first-class blocking rule** (fixes adversarial F-SC1).
- [ ] Mandatory near-miss negative fixtures: `incomplete` (vs `complete`), `representation` (vs `present`), decorated/bolded verdict lines, wrong-case tokens, setext-like headings. Regex timeouts are a guardrail, not a substitute for these fixtures.
- [ ] Closes E2 substring collision directly.

**Dependencies**: FR-7.

### FR-9: Unmask-and-Sweep Regression (H3)

**Description**: After any escape fix, search for adjacent masked defects in the same family before closure.

**Acceptance Criteria**:

- [ ] H3 FAILs if a fix only addresses the reported repro without searching same-token/same-shape sibling surfaces, or if a heuristic parser over generated prose is hard-fatal without adversarial false-positive fixtures + a cost rationale.
- [ ] The sweep documents `K_swept` and asserts it covers the full sibling family (fixes Quantity-Flow DIV-3).
- [ ] Closes E3 (sibling-heading negative case required after E2).

**Dependencies**: FR-7, FR-8.

### FR-10: Effective-Input Proof (H4)

**Description**: When an independent review/audit/reflect gate consumes an indirect selector, prove the reviewer consumed the runtime-produced surface.

**Acceptance Criteria**:

- [ ] H4 **fails closed** when effective input is absent, empty despite known changes, non-reproducible, **or non-empty but the wrong surface** — correctness of `|E ∩ true_runtime_surface|` must be proven, not merely `E>0` (fixes adversarial F-D1, the real E5 mechanism).
- [ ] Proof records dirty/staged/unstaged inclusion and foreign-commit exclusion via a machine-checkable manifest.
- [ ] Closes E5 directly.

**Dependencies**: FR-3.

### FR-11: Off-Path-Reviewer Rule + Waiver Standard (H5)

**Description**: Require off-path review when high-risk boundaries are crossed; constrain waivers.

**Acceptance Criteria**:

- [ ] Off-path review is `required` when a CLI invokes a subprocess, paths are reinterpreted by another layer, generated artifacts feed later gates, persisted state affects resume, a review selector chooses a surface, a hard gate uses heuristic parsing, a mock substitutes for runtime I/O, a sibling has a divergent contract, or the change controls HALT/WARN/CONTINUE/data-loss/review-integrity.
- [ ] A waiver is invalid if it merely says tests pass, the reviewer is independent, the command exists, or the issue looks local.

**Dependencies**: FR-1.

### FR-12: Waiver-Policy / No-Re-Greening Invariant + Anti-Inflation (cross-cutting)

**Description**: A waived or absent runtime probe downgrades the verdict and can never be re-greened; `known_escapes_caught` membership must be earned.

**Acceptance Criteria**:

- [ ] A `waived_with_rationale` or absent mandatory probe sets a one-way `waiver_status` latch and forces `pipeline_hardening_verdict ∈ {blocked, advisory}`; no later `task-builder`, `sc:reflect`, or `adversarial` stage may upgrade it to `pass`/`success` (fixes adversarial F-S1; bound to state variable SV-15, not prose).
- [ ] Production-facing pipeline-health signoff FAILs when a mandatory runtime probe is absent or `N/A` without rationale.
- [ ] An escape ID may appear in `known_escapes_caught` only if a passing wave/card is cited that would catch it (fixes adversarial F-A1).

**Dependencies**: FR-3, FR-5, FR-10, FR-11.

### FR-13: Versioned Additive Output Contract + REPORT.md Closure Section

**Description**: Extend the skill result with the hardening fields under a `contract_version`, and add a `Pipeline Hardening Closure` section to `REPORT.md`.

**Acceptance Criteria**:

- [ ] New fields (`pipeline_hardening_applicable`, `pipeline_hardening_verdict`, the 4 card/ledger path fields, `off_path_review_decision`, `known_escapes_caught`, `waiver_status`, `contract_version`) are additive; existing consumers reading prior fields do not break (backward-compat test required).
- [ ] `pipeline_hardening_verdict` is a deterministic aggregation of the H0–H5 statuses + `waiver_status` (the aggregation function is specified, not implied).
- [ ] REPORT.md closure section uses `NOT PROVEN` blockers (stronger than ordinary confidence language) when any required proof is absent.

**Dependencies**: FR-1 through FR-12.

### 3.1 Escape / Wave / Evidence Traceability Matrix

| Escape | Mechanism | Closing Wave(s) | FR(s) | Required Evidence Card(s) | Backtest Scenario |
|--------|-----------|-----------------|-------|---------------------------|-------------------|
| E1 | CLI/helper proof accepted while headless subprocess rejected local paths | H1, H2 | FR-3, FR-4, FR-6 | Runtime-entrypoint card with replay reaching production subprocess; contract ledger proving sibling file-delivery consumers swept | Replay headless PRD `--spec` with local-path `--file`; negative witness fails pre-fix and positive passes post-fix |
| E2 | Substring classifier accepted `complete` inside `incomplete` and applied the wrong phase invariant | H3 | FR-7, FR-8 | Whole-artifact classifier card with positive executable violation plus `incomplete` near-miss negative | Full generated artifact containing setup/work/completion sections; only executable target hard-fails |
| E3 | Single reported heading fixed while same-token sibling headings remained unswept | H3 | FR-7, FR-8, FR-9 | Unmask-and-sweep card with `K_true`, `K_swept`, same-token/same-shape family evidence, and false-positive fixture results | Artifact containing Task-Log/Findings sibling headings; non-executable headings WARN/CONTINUE rather than HALT |
| E4 | Shared `SemanticCheck.advisory` honored by generic gate but not PRD evaluator | H1, H2 | FR-3, FR-5, FR-12 | Runtime-entrypoint card proving PRD path reaches `_evaluate_gate`; H2 ledger classifying generic gate, PRD evaluator, trailing gate, remediation dispatch | Advisory semantic check runs through PRD evaluator; ledger fails until all live consumers classified |
| E5 | Review selector consumed an adjacent/foreign range instead of dirty `/task` work | H4, H5 | FR-10, FR-11, FR-12 | Effective-input manifest proving dirty/staged/unstaged inclusion and foreign-commit exclusion; off-path review decision | POST-reflect with dirty task work plus foreign commit; H4 fails until `E ∩ true_runtime_surface` is proven |

## 4. Architecture

### 4.1 New Files

| File | Purpose | Dependencies |
|------|---------|-------------|
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/pipeline-hardening-closure.md` | Mode overview, trigger, verdict aggregation, waiver latch | SKILL.md |
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/runtime-entrypoint-verification.md` | H1 card + negative-witness rule | pipeline-hardening-closure.md |
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/contract-enumeration.md` | H2 ledger schema + empty-ledger FAIL rule | pipeline-hardening-closure.md |
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/unmask-and-sweep.md` | H3 classifier boundary + word-boundary/near-miss fixtures | pipeline-hardening-closure.md |
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/effective-input-proof.md` | H4 fail-closed (incl. wrong-surface) proof | pipeline-hardening-closure.md |
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/hardening-output-contract.md` | Field schema, verdict aggregation truth table, waiver latch propagation contract, and downstream consumer obligations | pipeline-hardening-closure.md |

### 4.2 Modified Files

| File | Change | Rationale |
|------|--------|-----------|
| `src/superclaude/commands/troubleshoot.md` | Advertise pipeline-hardening trigger; mention hardening evidence paths; keep thin handoff | FR-1, thin-command segregation |
| `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` | Add mode trigger after Tier-1; wire failure states; reference new refs | FR-1..FR-13 |
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md` | Add `Pipeline Hardening Closure` section | FR-13 |
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/remediation-handoff.md` | Carry hardening verdict + waiver latch into handoff | FR-12 |

### 4.3 Removed Files

> None. This work is purely additive.

| File/Section | Reason | Migration |
|-------------|--------|-----------|
| (none) | Additive change | N/A |

### 4.4 Module Dependency Graph

```
troubleshoot.md (thin command)
        | handoff
        v
SKILL.md  --triggers-->  refs/pipeline-hardening-closure.md
                               |-- hardening-output-contract.md        (verdict, waiver latch, backtest status)
                               |-- runtime-entrypoint-verification.md  (H1)
                               |-- contract-enumeration.md             (H2)
                               |-- unmask-and-sweep.md                 (H3)
                               |-- effective-input-proof.md            (H4)
                               +-- report-template.md / remediation-handoff.md (output)
```

### 4.5 Data Models — State Variable Registry

> Mandatory correctness artifact (full version: `spec-panel/state-variable-registry.md`; 15 variables, 11 with previously-ASSUMED initial/range/invariant — each now pinned by an FR).

| Variable | Type | Initial | Invariant | Read | Write |
|----------|------|---------|-----------|------|-------|
| `pipeline_hardening_applicable` | bool | `false` | Set exactly once by H0; if `true`, H1–H5 must run or be waived | verdict aggregation, report | H0 (FR-1) |
| `pipeline_hardening_verdict` | enum `pass\|blocked\|advisory\|not_applicable` | `not_applicable` | Deterministic function of H-statuses + `waiver_status`; never upgraded post-waiver | report, downstream | aggregation (FR-13) |
| `h0..h5_status` | enum `PASS\|FAIL\|N/A` | `N/A` | `N/A` only with recorded rationale; FAIL is sticky | aggregation | each wave (FR-1,3,5,9,10,11) |
| `off_path_review_decision` | enum `required\|performed\|waived_with_rationale\|not_required` | `not_required` | `waived_with_rationale` requires a valid waiver | aggregation, report | H5 (FR-11) |
| `known_escapes_caught` | list of objects `{escape_id, wave, card_path, status}` | `[]` | Membership requires a cited passing wave/card with `status=PASS` (anti-inflation) | report | H0/closure (FR-2,12) |
| `waiver_status` | enum `none\|latched` | `none` | One-way latch: `none`→`latched` only; once `latched`, verdict ∈ {blocked, advisory} | aggregation (FR-13) | FR-12 |
| `backtest_status` | enum `not_run\|partial\|complete` | `not_run` | Production-facing coverage signoff remains advisory until E1–E5 backtests complete | report, roadmap | E1–E5 backtest gate (NFR-1) |
| `contract_version` | str (semver) | `"1.0.0"` | Monotonic; additive fields only within a major | consumers | FR-13 |
| `runtime_entrypoint_card_path` / `contract_ledger_path` / `unmask_sweep_path` / `effective_input_card_path` | str\|null | `null` | Non-null ⇒ file exists and is the proof for its wave | report | H1/H2/H3/H4 |

### 4.6 Implementation Order

```
1. refs/pipeline-hardening-closure.md (mode skeleton + H0 boundary scan schema) -- foundation for all waves
2. refs/hardening-output-contract.md (verdict truth table + waiver latch propagation) -- resolves OI-1/OI-6 before downstream wiring
3. refs/runtime-entrypoint-verification.md (H1 + negative witness)   -- depends on 1-2
   refs/contract-enumeration.md (H2 + empty-ledger FAIL)             -- [parallel with 3]
   refs/effective-input-proof.md (H4 fail-closed incl. wrong-surface)-- [parallel with 3]
4. refs/unmask-and-sweep.md (H3 classifier + formal grammar + word-boundary fixtures) -- depends on 3 and the parser decision in §5.7
5. SKILL.md trigger wiring + output contract (FR-13)                 -- depends on 1-4
6. report-template.md + remediation-handoff.md                       -- depends on 5
7. Tests (§8) + make sync-dev + make verify-sync                      -- depends on 6
```

### 4.7 Executable Validation Architecture

The protocol text remains markdown-first, but every closure artifact that affects `pipeline_hardening_verdict` has an executable validation surface so tests cannot pass from prose alone.

| Component | Location | Responsibility | Required Consumers |
|-----------|----------|----------------|--------------------|
| Verdict aggregation contract | `refs/hardening-output-contract.md` + `tests/troubleshoot/test_hardening_verdict.py` | Define and test the truth table in §5.4; reject any path that maps `waiver_status=latched` to `pass`/`success` | `SKILL.md`, `report-template.md`, `remediation-handoff.md`, post-run reflection/adversarial handoffs |
| Boundary scan schema | `refs/pipeline-hardening-closure.md` + H0 tests | Require typed boundary rows before `pipeline_hardening_applicable=false` can skip H1-H5 | H0 dispatcher, `REPORT.md` closure section |
| Contract ledger validator | `refs/contract-enumeration.md` + H2 tests | Reject empty ledgers, unclassified live consumers, and `dead/legacy` rows without unreachability proof | H2 ledger, report renderer |
| Classifier fixture harness | `refs/unmask-and-sweep.md` + H3 fixtures | Run full generated artifacts through the same classifier rules used by the protocol; assert HALT/WARN/CONTINUE by runtime consumer | H3 card, report renderer |
| Effective-input manifest validator | `refs/effective-input-proof.md` + H4 tests | Prove selector output intersects the true runtime surface and excludes foreign/stale surfaces | H4 card, off-path review decision |
| Output-contract compatibility harness | `tests/troubleshoot/test_hardening_output_contract.py` | Validate new fields are additive, nullable/defaulted as specified, and older consumers ignoring them still pass | Existing troubleshoot result consumers |

Test-only helpers may live under `tests/troubleshoot/` if they are purely validators for markdown contracts. Any reusable runtime logic promoted beyond tests must live under `src/superclaude/` and be referenced from this section before implementation.

## 5. Interface Contracts

### 5.1 CLI Surface

```
/sc:troubleshoot <issue>            # unchanged invocation; pipeline-hardening mode auto-triggers via FR-1
# Report gains a "Pipeline Hardening Closure" section when applicable=true
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| (no new CLI flags) | — | — | Hardening mode is triggered by issue topology (FR-1), not a flag; keeps the command thin |

### 5.2 Gate Criteria — Guard Condition Boundary Table (condensed)

> Mandatory correctness artifact (full version: `spec-panel/guard-boundary-table.md`; 6 guards × 6 input conditions = 36 rows, 16 GAP in the draft — each GAP closed by an FR below). `GAP→FIXED` = the draft left it unspecified; this spec specifies it.

| Guard | Input Condition | Guard Result | Specified Behavior | Status |
|-------|-----------------|--------------|--------------------|--------|
| H2 empty ledger | Zero/Empty (`[]` consumers) | would-pass vacuously | **FAIL** — empty ledger cannot satisfy "no unclassified consumer" (FR-5) | GAP→FIXED |
| H2 `dead/legacy` role | Sentinel match | guard disabled | Requires unreachability proof, not assertion (FR-5) | GAP→FIXED |
| H3 substring match | Sentinel collision (`incomplete`⊃`complete`) | false positive | Word-boundary/grammar match + near-miss fixtures (FR-8) | GAP→FIXED |
| H4 effective input | Legitimate edge (non-empty, wrong surface) | would-pass (E>0) | **FAIL closed** unless surface-correctness proven (FR-10) | GAP→FIXED |
| H4 effective input | Zero/Empty | unspecified default | FAIL closed (default specified, FR-10) | GAP→FIXED |
| H5 / verdict | Waived probe then downstream re-eval | could re-green | One-way `waiver_status` latch; verdict ∈ {blocked, advisory} (FR-12) | GAP→FIXED |

### 5.3 Phase Contracts

```yaml
# Inter-wave contract (each wave consumes prior outputs; verdict aggregates all)
H0: {in: diagnosis, out: {applicable: bool, mechanism: str, candidate_escapes: [str]}}
H1: {in: applicable=true, out: {status: PASS|FAIL|N/A, card_path: str, negative_witness: bool}}
H2: {in: changed_contract, out: {status, ledger_path: str, unclassified_count: int}}   # FAIL if unclassified>0 OR ledger empty
H3: {in: anchor_fix, out: {status, sweep_path: str, K_swept: int, fixtures: {positive, sibling_negative}}}
H4: {in: review_selector, out: {status, card_path: str, surface_correct: bool}}          # FAIL closed if !surface_correct
H5: {in: boundary_risk, out: {decision: required|performed|waived_with_rationale|not_required, status: PASS|FAIL|N/A}}
verdict: {in: [h0..h5_status, waiver_status], out: pass|blocked|advisory|not_applicable}  # never upgraded post-latch
```

### 5.4 Verdict Aggregation Truth Table (resolves OI-1 / OI-6)

The aggregation function is deterministic and evaluated after H0-H5. `FAIL` is sticky and outranks advisory waiver handling. `waiver_status=latched` is a one-way latch and is checked before any downstream success signal.

| Condition Priority | Input Condition | Output Verdict | Report Language | Downstream Override Allowed? |
|--------------------|-----------------|----------------|-----------------|------------------------------|
| 1 | `pipeline_hardening_applicable=false` AND H0 has reason + boundary scan | `not_applicable` | `Pipeline hardening not applicable: <reason>` | No |
| 2 | Any H1-H5 status is `FAIL` | `blocked` | `NOT PROVEN — failed hardening wave: <wave>` | No |
| 3 | `waiver_status=latched` AND any mandatory probe absent/waived without accepted substitute | `blocked` | `NOT PROVEN — mandatory runtime proof waived or absent` | No |
| 4 | Any H1-H5 status is `N/A` without rationale | `blocked` | `NOT PROVEN — unrationalized N/A: <wave>` | No |
| 5 | `waiver_status=latched` AND all mandatory probes have accepted substitutes + rationale AND no H-status is `FAIL` | `advisory` | `ADVISORY — closure relies on waived/substituted proof` | No |
| 6 | Any H1-H5 status is `N/A` with valid rationale and no failures/latch | `advisory` | `ADVISORY — scoped closure with rationalized N/A` | No |
| 7 | H0 applicable, all required H1-H5 statuses `PASS`, and `waiver_status=none` | `pass` | `Pipeline hardening closure proven` | No |

#### H5 Decision-to-Status Mapping

| H5 Decision | H5 Status | Waiver Status Effect | Notes |
|-------------|-----------|----------------------|-------|
| `performed` | `PASS` | `none` | Required off-path review completed and consumed the effective-input proof. |
| `not_required` | `PASS` | `none` | Pass-equivalent only when the boundary-risk scan proves no H5 trigger applies; no required proof is missing. |
| `required` | `FAIL` | `none` | Off-path review was required but not performed or validly waived. |
| `waived_with_rationale` | `N/A` with rationale | `latched` | Valid waiver downgrades final verdict through the truth table; invalid waiver maps to `FAIL`. |

Downstream `task-builder`, `sc:reflect`, `sc:adversarial`, and report-rendering stages may append findings, but they may not convert `blocked`/`advisory` into `pass` or `success`. If a downstream stage has its own success enum, the rendered result is `success_with_hardening_blocker` or `success_with_hardening_advisory`, never plain `success`, whenever this table returns `blocked` or `advisory`.

#### Backtest Status vs Run-Level Verdict

`pipeline_hardening_verdict` is the **run-level H0-H5 closure verdict**. It may be `pass` when every applicable wave passes and `waiver_status=none`. `backtest_status` is the separate **coverage-validation state** for NFR-1:

| Backtest Status | Meaning | Production-Facing Pipeline-Health Signoff |
|-----------------|---------|-------------------------------------------|
| `not_run` | No E1-E5 replay suite has run against the built hardening gates | `advisory` even if `pipeline_hardening_verdict=pass` |
| `partial` | Some, but not all, E1-E5 replay scenarios have passed | `advisory` with missing escape IDs listed |
| `complete` | E1-E5 replay scenarios all pass against the built gates | May mirror `pipeline_hardening_verdict` |

REPORT.md must render both fields so downstream consumers do not confuse a clean H0-H5 run with validated E1-E5 catch-rate coverage.

### 5.5 Output Contract Field Schema

| Field | Type | Required | Default | Nullability | Producer | Consumer Behavior If Missing |
|-------|------|----------|---------|-------------|----------|------------------------------|
| `contract_version` | semver string | yes | `1.0.0` | non-null | FR-13 | Treat missing as legacy contract; do not infer hardening pass |
| `pipeline_hardening_applicable` | bool | yes | `false` | non-null | H0 | Missing ⇒ legacy/unknown; report must not claim closure |
| `pipeline_hardening_verdict` | enum `pass\|blocked\|advisory\|not_applicable` | yes when applicable known | `not_applicable` | non-null | aggregation | Missing with applicable=true ⇒ `blocked` |
| `waiver_status` | enum `none\|latched` | yes | `none` | non-null | H1-H5 / FR-12 | Missing with any waiver marker ⇒ `blocked` |
| `backtest_status` | enum `not_run\|partial\|complete` | yes | `not_run` | non-null | NFR-1 replay suite | Missing ⇒ treat production-facing signoff as `advisory` |
| `off_path_review_decision` | enum `required\|performed\|waived_with_rationale\|not_required` | yes | `not_required` | non-null | H5 | Missing when H5 required ⇒ `blocked` |
| `runtime_entrypoint_card_path` | absolute path string | required when H1 runs | `null` | nullable before H1 | H1 | Missing when H1 required ⇒ `blocked` |
| `contract_ledger_path` | absolute path string | required when H2 runs | `null` | nullable before H2 | H2 | Missing when H2 required ⇒ `blocked` |
| `unmask_sweep_path` | absolute path string | required when H3 runs | `null` | nullable before H3 | H3 | Missing when H3 required ⇒ `blocked` |
| `effective_input_card_path` | absolute path string | required when H4 runs | `null` | nullable before H4 | H4 | Missing when H4 required ⇒ `blocked` |
| `known_escapes_caught` | list of objects `{escape_id, wave, card_path, status}` | yes | `[]` | non-null list | H0/closure | Missing/empty ⇒ no coverage claim |

### 5.6 Required Artifact Schemas

#### H0 Boundary Scan Row

| Field | Required | Meaning |
|-------|----------|---------|
| `boundary_type` | yes | One of CLI/subprocess, file-stdin-prompt, generated-artifact-parser, gate-status-enum, duplicate-evaluator, persisted-state, review-selector, sibling-pipeline, prior-escape-unmask |
| `producer` / `transformers` / `consumer` | yes | Concrete components in the data path |
| `evidence_source` | yes | File, command, report, or trace supporting the classification |
| `risk` | yes | Why this boundary can admit proof substitution |
| `decision` | yes | `applicable` or `not_applicable` |
| `rationale` | yes | One sentence; `looks local` is invalid |

#### H1 Runtime-Entrypoint Card

| Field | Required | Meaning |
|-------|----------|---------|
| `producer` | yes | Component that creates the value/artifact under test |
| `transformers` | yes | Ordered list of layers that reinterpret, serialize, parse, route, or persist the value |
| `consumer_or_evaluator` | yes | Production/operator boundary that ultimately consumes the value |
| `boundary_crossed` | yes | The concrete boundary type reached by the replay |
| `replay_command` | yes | Command or scripted invocation that reaches the production boundary |
| `production_boundary_reach_proof` | yes | Evidence that the replay did not stop at a helper/mock |
| `forbidden_interpretation` | yes when applicable | The bad interpretation the negative witness must expose |
| `negative_witness_command` / `negative_witness_result` | yes | Fix-reverted or accepted-substitute run showing FAIL |
| `positive_witness_command` / `positive_witness_result` | yes | Fix-applied run showing PASS |
| `accepted_substitute_rationale` | required if no literal revert | Why captured pre-fix replay, isolated worktree revert, synthetic contract fixture, or historical log is acceptable |

#### H2 Contract Ledger Row

| Field | Required | Meaning |
|-------|----------|---------|
| `contract_token` | yes | Field/flag/parser rule/semantic check/status/predicate under change |
| `role` | yes | `producer`, `transformer`, `consumer`, `evaluator`, `dead/legacy` |
| `component_path` | yes | Source/ref/test path or generated artifact path |
| `discovery_method` | yes | Symbol/reference search, exact grep, semantic retrieval, sibling scan, fixture scan, or manual evidence |
| `classification` | yes | `classified`, `unclassified`, or `dead/legacy_with_proof` |
| `unreachability_proof` | required for `dead/legacy` | Why runtime cannot reach the component |

#### H3 Unmask / Sweep / Classifier Card

| Field | Required | Meaning |
|-------|----------|---------|
| `anchor_failure` | yes | The original failure or repro that motivated the fix |
| `sibling_family_discovery_method` | yes | How same-token/same-shape sibling surfaces were discovered |
| `K_true` | yes | Count/list of sibling-family members discovered |
| `K_swept` | yes | Count/list of sibling-family members covered by fixtures or proof |
| `coverage_proof` | yes | Evidence that `K_swept` covers the full sibling family |
| `positive_fixture` | yes | Full-artifact or fixture case where the intended violation still HALTs |
| `sibling_negative_fixture` | yes | Same-token/same-shape off-path case that must not hard-fail |
| `full_artifact_mixed_fixture` | yes | Generated artifact containing positive and sibling-negative controls together |
| `severity_assertions_by_consumer` | yes | Expected HALT/WARN/CONTINUE for every runtime consumer |
| `heuristic_cost_rationale` | required for hard-fatal heuristic parser | Why the heuristic is worth hard-gating despite false-positive risk |

#### H4 Effective-Input Manifest

| Field | Required | Meaning |
|-------|----------|---------|
| `selector_command` / `selector_cwd` | yes | Command and working directory that selected the review surface |
| `base_ref` / `head_ref` | yes | Revision endpoints used by the selector |
| `dirty_files` / `staged_files` / `unstaged_files` | yes | Working-tree state at review time |
| `included_files` | yes | Files/commits/artifacts actually consumed |
| `excluded_foreign_commits` | yes | Foreign/stale commits excluded, or explicit empty list |
| `runtime_surface_claim` | yes | The true surface requiring review |
| `intersection_proof` | yes | Machine-checkable proof that `included_files ∩ runtime_surface_claim` is correct |
| `validation_command` / `validation_result` | yes | How the manifest was checked |

### 5.7 H3 Parser Decision

H3 uses a **small formal allow-list grammar**, not ad hoc substring matching and not a full CommonMark parser in the first implementation increment. The grammar is intentionally narrow:

1. Only ATX headings (`#`, `##`, ... with a required post-marker space) and explicit verdict/status lines are behavior-controlling.
2. Matching is exact-token or word-boundary anchored with escaped tokens; substring containment is never behavior-controlling.
3. Setext-like headings, decorated/bolded verdict lines, wrong-case tokens, and sibling sections are fixtures, not accepted control syntax unless explicitly added to the grammar later.
4. Every grammar expansion requires a positive fixture, a near-miss negative fixture, and a full-artifact mixed fixture.

This resolves OI-4 for the release increment while preserving a future option to replace the grammar with a CommonMark-derived parser if fixture pressure or false-positive measurement justifies it.

## 6. Non-Functional Requirements

| ID | Requirement | Target | Measurement |
|----|-------------|--------|-------------|
| NFR-1 | E1–E5 backtest catch rate | 100% would-have-caught (post-build, predicted until then) | Replay each escape against the built gates |
| NFR-2 | Applicability false-positive rate | <30% | Sample non-pipeline fixes; count spurious `applicable=true` |
| NFR-3 | Added cost of hardening mode | Bounded vs Tier-1 baseline; single-seam probe, no mandatory full E2E | Token/latency delta per run |
| NFR-4 | No-re-greening durability | 100% (no path upgrades a latched verdict) | Adversarial test: attempt downstream re-green |
| NFR-5 | Command thinness | Command advertises + hands off only | Diff review: no heavy logic in `troubleshoot.md` |
| NFR-6 | Output-contract backward compatibility | 100% of existing result consumers unaffected | Contract test on prior field set |

## 7. Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Waiver-abuse theatre (waived probe treated as pass) | Medium | High | FR-12 one-way latch + §5.4 truth table + downstream no-override rule + NFR-4 adversarial test |
| Over-triggering on local fixes (cost/noise) | High | Medium | FR-1 boundary scan; NFR-2 <30% false-positive target |
| Refs + ledger maintenance/drift | Medium | Medium | Keep refs small; sibling-sweep covers drift; verify-sync gate |
| Unversioned contract breaks consumers | Low | High | FR-13 `contract_version` + NFR-6 backward-compat test |
| Predicted coverage never validated post-G1 | Medium | High | `backtest_status` separates H0-H5 run verdict from production-facing coverage signoff; signoff stays `advisory` until E1-E5 `complete` |
| `N/A`-without-rationale bypass | Medium | High | FR-12: `N/A` requires rationale or pipeline-health FAILs |
| New heuristic hard-gate introduces an E3-class false positive | Medium | Medium | FR-8/FR-9 require false-positive fixtures + cost rationale before a hard gate ships |

## 8. Test Plan

### 8.1 Unit Tests

| Test | File | Validates |
|------|------|-----------|
| `test_h0_applicability_skip_requires_boundary_scan` | `tests/troubleshoot/test_hardening_h0.py` | FR-1 skip needs reason+scan |
| `test_h0_boundary_scan_schema_rejects_bare_local_reason` | `tests/troubleshoot/test_hardening_h0.py` | §5.6 boundary scan schema; `looks local` cannot skip hardening |
| `test_h1_runtime_card_requires_negative_and_positive_witness` | `tests/troubleshoot/test_hardening_h1.py` | FR-3/FR-4 and §5.6 runtime-entrypoint card schema |
| `test_h2_empty_ledger_fails` | `tests/troubleshoot/test_hardening_h2.py` | FR-5 empty ledger = FAIL (F-N3) |
| `test_h3_word_boundary_rejects_incomplete_representation` | `tests/troubleshoot/test_hardening_h3.py` | FR-8 near-miss negatives (F-SC1) |
| `test_h3_small_grammar_rejects_setext_and_decorated_verdicts` | `tests/troubleshoot/test_hardening_h3.py` | §5.7 parser decision and grammar fixtures |
| `test_h3_sweep_card_requires_k_true_k_swept_and_mixed_fixture` | `tests/troubleshoot/test_hardening_h3.py` | FR-9 and §5.6 unmask/sweep/classifier card schema |
| `test_h4_nonempty_wrong_surface_fails_closed` | `tests/troubleshoot/test_hardening_h4.py` | FR-10 wrong-surface (F-D1) |
| `test_h4_manifest_schema_requires_intersection_proof` | `tests/troubleshoot/test_hardening_h4.py` | §5.6 effective-input manifest schema |
| `test_waiver_latch_one_way` | `tests/troubleshoot/test_hardening_verdict.py` | FR-12 no re-green (F-S1) |
| `test_h5_decision_maps_to_status_and_latch` | `tests/troubleshoot/test_hardening_verdict.py` | §5.4 H5 decision-to-status mapping |
| `test_known_escapes_requires_cited_card` | `tests/troubleshoot/test_hardening_verdict.py` | FR-12 anti-inflation (F-A1) |

### 8.2 Integration Tests

| Test | Validates |
|------|-----------|
| `test_verdict_aggregation_from_h_statuses` | FR-13 deterministic verdict from H0–H5 + waiver_status; covers all §5.4 truth-table rows |
| `test_downstream_success_cannot_override_latched_hardening_verdict` | FR-12 downstream task-builder/reflect/adversarial cannot re-green `blocked`/`advisory` |
| `test_output_contract_backward_compat` | NFR-6 existing consumers read prior fields unbroken |
| `test_backtest_status_keeps_pipeline_health_advisory_until_complete` | NFR-1 separates H0-H5 run verdict from production-facing E1-E5 catch-rate signoff |
| `test_report_closure_section_not_proven_blockers` | FR-13 `NOT PROVEN` blockers when proof absent |

### 8.3 Manual / E2E Tests

| Scenario | Steps | Expected Outcome |
|----------|-------|------------------|
| E1 backtest | Replay headless PRD `--spec` with local-path `--file` against H1 | H1 FAIL pre-fix (negative witness), PASS post-fix |
| E2 backtest | Replay full generated artifact containing `complete` and near-miss `incomplete` phase text against H3 classifier | Intended executable violation still HALTs; near-miss sibling negative does not hard-fail |
| E3 backtest | Replay Task-Log/Findings sibling-heading artifact against H3 unmask/sweep card | H3 FAILs until `K_swept == K_true` and non-executable headings WARN/CONTINUE rather than HALT |
| E4 backtest | Run advisory check through PRD `_evaluate_gate` with H2 ledger | H2 FAIL until both `gate_passed` and `_evaluate_gate` consumers classified |
| E5 backtest | POST-reflect with dirty `/task` work + a foreign commit in range | H4 FAIL closed (wrong surface) until selector proven correct |
| Waiver re-green attempt | Waive H1, then run downstream reflect/adversarial | Verdict stays `blocked`/`advisory`; never `pass` |

## 9. Migration & Rollout

- **Breaking changes**: None. New output-contract fields are additive under `contract_version: 1.0.0`; the mode is off unless `applicable=true`.
- **Backwards compatibility**: Existing `sc:troubleshoot` result consumers read only prior fields; NFR-6 test guards this.
- **Rollback plan**: Revert the SKILL.md trigger block and remove the 6 new refs; the command reverts to a pure handoff. Then run `make sync-dev` and `make verify-sync` so `.claude/` dev mirrors match `src/superclaude/`; do not stage `.claude/` mirrors other than `.claude/settings.json`. No data migration. (Implementation is gated behind G1 approval; pre-approval the working tree is unchanged on protocol source files.)

## 10. Downstream Inputs

### For sc:roadmap

Themes: (T1) Wave gates H0–H5 as enforceable controls; (T2) Anti-theatre verdict/waiver invariant; (T3) Output-contract + report integration; (T4) Backtest validation of E1–E5. Milestones: M1 mode skeleton + verdict aggregation; M2 H1/H2/H4 gates; M3 H3 classifier + fixtures; M4 contract + report; M5 backtest + sync.

### For sc:tasklist

Break per FR (FR-1..FR-13) into atomic tasks; group by implementation order (§4.6). Each task's DoD = its FR acceptance criteria + the relevant unit test (§8.1). FR-12 (no-re-greening) is the highest-risk task — pair with the NFR-4 adversarial test and §5.4 truth-table/downstream no-override checks before marking done.

## 11. Open Items

| Item | Question | Impact | Resolution Target |
|------|----------|--------|-------------------|
| OI-1 | How is no-re-greening enforced *mechanically* (not just prose) across task-builder/reflect/adversarial? | High (core anti-theatre control) | **Resolved in §5.4**: persisted `waiver_status` latch + downstream no-override rule + `success_with_hardening_*` rendering |
| OI-2 | Which tokens are first-class ledger entries (flags, phase IDs, gate names, verdicts, step IDs, statuses)? | Medium | Roadmap M2; schema seeded in §5.6 `contract_token` |
| OI-3 | Cheapest reliable public-entrypoint probe per high-risk seam (esp. live Claude/agent execution)? | Medium | Roadmap M2; substitute witness classes governed by FR-4/§5.4 latch |
| OI-4 | Real CommonMark-derived parser vs a smaller PRD-specific grammar for FR-7/FR-8? | Medium | **Resolved in §5.7**: small formal allow-list grammar for this increment |
| OI-5 | `target_release` exact version (proposed 4.3.0) | Low | G1 approval |
| OI-6 | Verdict-enum reconciliation across §5.3, FR-13, and `waiver_status` latch | Low | **Resolved in §5.4** truth table |

## 12. Brainstorm Gap Analysis

> Gaps the panel found in the source draft, now closed by this spec.

| Gap ID | Description | Severity | Affected Section | Persona |
|--------|-------------|----------|-----------------|---------|
| G-1 | Waiver/no-re-greening was prose, bound to no variable | High | FR-12, §4.5 SV `waiver_status` | Whittaker/Hightower |
| G-2 | H2 empty ledger passes vacuously | High | FR-5, §5.2 | Nygard |
| G-3 | H4 missed non-empty-wrong-surface (real E5) | High | FR-10, §5.2 | Whittaker |
| G-4 | E2 word-boundary rule only in appendix, not a guard | High | FR-8 | Whittaker |
| G-5 | `known_escapes_caught` accepted un-earned membership | High | FR-12 | Whittaker |
| G-6 | Output contract unversioned | High | FR-13 | Newman |
| G-7 | Waves were prose, not SMART FRs | Critical | §3 (FR-1..13) | Wiegers |
| G-8 | No E1–E5 → wave → FR traceability | Medium | §3.1 | Wiegers |
| G-9 | Verdict aggregation was required but not truth-tabled | High | §5.4 | Fowler/Newman |
| G-10 | Boundary/ledger/manifest schemas were prose-only | High | §5.5-§5.6 | Hohpe/Nygard |
| G-11 | H3 parser strategy was unresolved | Medium | §5.7 | Whittaker/Crispin |
| G-12 | Executable validation architecture was implicit | Medium | §4.7, §8 | Fowler |

All High/Critical gaps are closed in this spec; remaining Medium items are either resolved in §5.7/§4.7 or tracked in §11 Open Items with implementation-phase targets.

---

## Appendix A: Glossary

| Term | Definition |
|------|-----------|
| Pipeline escape | A defect at a runtime/generated-artifact/shared-contract/review-input boundary that a review can miss by accepting adjacent proof |
| Proof substitution | Accepting a command string, edited helper, PASS artifact, or generic-path proof in place of the real boundary proof |
| Negative witness | The oracle run against real input through the production entrypoint with the fix reverted, showing FAIL |
| Effective input | The actual files/commits/artifacts a review/audit gate consumed (vs the selector that named them) |
| No-re-greening latch | One-way `waiver_status` state: once latched, the verdict can never be upgraded to `pass`/`success` downstream |
| Wave-numbering crosswalk | This spec uses the draft's H0–H5; merged report §10 used H3=classifier, H4=unmask, H5=effective-input. Canonical = this spec |

## Appendix B: Reference Documents

| Document | Relevance |
|----------|-----------|
| `troubleshoot-pipeline-hardening-spec.md` | Source draft (substrate) |
| `EFFICACY-REPORT-MERGED.md` §3/§9/§10/Appendix A | Escape ledger, contract-identity, hardening direction, external best-practice corroboration |
| `spec-panel/state-variable-registry.md` | Full State Variable Registry (15 vars) |
| `spec-panel/guard-boundary-table.md` | Full Guard Condition Boundary Table (36 rows, 16 GAP) |
| `spec-panel/quantity-flow-diagram.md` | Full Quantity Flow Diagram (count-divergence CRITICALs) |
| `spec-panel/adversarial-findings.md` | Whittaker 5-attack findings (6 CRITICAL, 10 MAJOR, 1 MINOR) |
| `spec-panel/panel-findings-req-arch.md` | Requirements/architecture/integration/ops critique + FR/NFR extraction |
