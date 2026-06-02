# Reviewer Card R1 — opus-analyzer (Root-Cause + Architectural Analysis)

**Reviewer ID:** R1-opus-analyzer
**Model:** claude-opus-4-7 (1M context)
**Persona focus:** Architectural / root-cause — assess whether the proposed task plan addresses the 4 INHERENT architectural flaws (master:§Flaws 1, 2, 3, 5) at their structural roots, not merely symptomatically. Probe the completeness of the substrate inversion.
**Reviewed artifact:** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260531-042405/TASK-RF-20260531-042405.md` (832 lines, 13 phases + 6 phase gates, ~108 checklist items)
**Authority:** `BUILD-REQUEST-roadmap-pipeline-rewrite.md` (225 lines) embedding §Contract verbatim from Vector C Q4 and §MVR verbatim from Vector A Q4; `master-report.md` §Architectural-flaw Thesis + §Verdict.

---

## Verdict: **PASS** (with one HIGH risk noted on R1.5/R1.6 sequencing)

The tasklist is a faithful, evidence-grounded execution plan for the BUILD-REQUEST. Every R0 and R1 phase from the spec maps cleanly to numbered phases/steps; §MVR §1-§5 are each implemented in dedicated phases; §Contract items 1-10 each have a wiring path; the four PRESERVE targets (commands.py, structural_checkers.py, convergence.py, cosmetic_remediator.py) are explicitly excluded across the scope block, named in every rf-qa probe, and never touched in any implementation step. The substrate inversion is structurally complete — Flaws 1 (R1.3 + R1.5), 2 (R1.4 generator-side schema), 3 (R1.2 envelope), 5 (R0.3 + R1.1 contracts) all have dedicated structural fixes, not just downstream-validator patches.

This is not a case for re-author; one HIGH finding (R1.5/R1.6 ordering creates a transient fail-open window) and a couple of MEDIUM risks (R1.4 cadence realism, dispatch-walker corner cases) warrant remediation notes before sprint kickoff but do not require restructuring the plan.

---

## 5-Dimension Calibration Rubric

### D1. Citation grounding — **4/5**

Spot-checked ≥8 file:line citations against current source:

| Tasklist citation | Verified location | Result |
|---|---|---|
| `spec_parser.py:extract_requirement_ids L333` (Step 2.2) | `src/.../spec_parser.py:333 def extract_requirement_ids` | ✅ exact |
| `spec_parser.py:parse_frontmatter L109` (Step 2.2, Step 11.2) | `src/.../spec_parser.py:109 def parse_frontmatter` | ✅ exact |
| `spec_parser.py:parse_document L608-639` (Step 2.2) | `src/.../spec_parser.py:608 def parse_document` | ✅ exact |
| `executor.py:_build_steps L1947` (Step 2.3) | `src/.../executor.py:1947 def _build_steps` | ✅ exact |
| `executor.py:build_certify_step L1899` (Step 8.3) | `src/.../executor.py:1899 def build_certify_step` | ✅ exact |
| `executor.py:2167 gate=None if config.convergence_enabled` (Step 11.4) | `src/.../executor.py:2167 gate=None if config.convergence_enabled else SPEC_FIDELITY_GATE` | ✅ exact |
| `gates.py:_parse_frontmatter L168` (Step 11.2) | `src/.../gates.py:168 def _parse_frontmatter` | ✅ exact |
| `gates.py:_cross_refs_resolve L48-91` (Step 11.3) | `src/.../gates.py:48 def _cross_refs_resolve` | ✅ exact |
| `pipeline/models.py: GateCriteria L91, SemanticCheck L82, Step L109` | `src/.../pipeline/models.py:82,91,109` | ✅ exact |
| `obligation_scanner.py:_DESCRIPTOR_NOUNS L109-125, _DEMOTED_H3_SUBSECTIONS L137-142, _is_descriptive_context L608, _is_demoted_h3 L694` | All four exact | ✅ exact |
| `obligation_scanner.py return-True stubs L719/L722/L725/L729/L733/L737/L741/L760` (Step 11.3) | All eight verified present | ✅ exact |
| `remediate_executor.py return-True stubs L326/L345/L362/L397/L412/L423/L706` (Step 11.3) | All seven verified present | ✅ exact |
| `fidelity_checker.py:287-303` fail-open block (Step 11.4) | The `found=True, # fail-open` lives at L296-303 inside the L287-303 `if not mapping.expected_names` block — **citation off by ~9 lines on the smoking-gun line** but the **L287-303 block boundary is exact**. | ⚠️ block-correct, line-pin slightly off |
| `fidelity_checker.py:314-337` partial-match fail-open (Step 11.4) | The `found = True` at L316 is inside the L314-337 partial-match block. Block boundaries correct; smoking-gun line is L316 not "314". | ⚠️ same pattern |

**Justification (−1):** The two fidelity_checker line ranges are accurate as *block boundaries* but the prose in Step 11.4 implies a tight pin on the L298/L316 lines themselves. A worker following these citations will land in the right block but the leading line may not contain the literal `found=True` they expect. This is research-mediated (the research/02 doc apparently used block ranges rather than line pins) and recoverable, but a true 5/5 grounding score requires line-exact citations on the load-bearing tokens. No false citations were found; this is a precision-not-correctness gap.

### D2. Coverage completeness — **5/5** (coverage_pct = 1.00)

Computed coverage of BUILD-REQUEST R0 + R1 + Acceptance gates against tasklist phases:

| Spec requirement | Tasklist mapping | Status |
|---|---|---|
| **R0 item 1** Spec-ID registry (Contract #9) | Phase 2 (Steps 2.1-2.8) | ✅ |
| **R0 item 2** Anti-instinct vocab-lint allowlist (Contract #10), MultiModelSwarm | Phase 3 (Steps 3.1-3.8) with explicit live re-run at 3.8 | ✅ |
| **R0 item 3** `superclaude.contracts` SoT + arch-lint (Contract #5 + #8) | Phase 4 (Steps 4.1-4.7) | ✅ |
| **R0 acceptance** | Phase 5 + Phase Gate PG5 (rf-qa-qualitative on R0 surface) | ✅ |
| **R1.1** Extend contracts (RETURN_CONTRACTS + thresholds) | Phase 6 | ✅ |
| **R1.2** PipelineEnvelope + sidecar JSON + dual-write | Phase 7 (post-extractors per step in Step 7.3) | ✅ |
| **R1.3** `GateCriteria.code_assertions` + first CodeAssertion (`build_certify_step` wiring) | Phase 8 | ✅ |
| **R1.4** Tool-write rewrite, 9 LLM steps, side-by-side ≥3 release cycles | Phase 9 (Steps 9.2-9.10 = 9 sub-phases + 9.11 secondary + 9.12 cutover gate) | ✅ |
| **R1.5** `verify-implementation` terminal step (Tasklist → AST) | Phase 10 | ✅ |
| **R1.6** Cleanup (parsers, fail-open, return-True, gate=None) | Phase 11 (Steps 11.1-11.7) | ✅ |
| **Acceptance gate 1** All 10 Contract items CI-enforced | Steps 13.4 + 13.7(a) | ✅ |
| **Acceptance gate 2** All passing tests still pass | Step 13.5 | ✅ |
| **Acceptance gate 3** Pipeline runs on `.dev/releases/complete/*/spec*.md` | Step 13.6 (live corpus run) | ✅ |
| **Acceptance gate 4** Recurrence corpus ≥1 per RECURRENT row | Steps 13.1-13.3 (seeding map + 15 new fixtures + master test) | ✅ |
| **Acceptance gate 5** MultiModelSwarm halt resolved | Step 3.8 + Step 5.2 + Step 13.7(e) | ✅ |
| **Acceptance gate 6** Step count ≤14 | Steps 10.1, 10.2, 11.3, 13.7(f) | ✅ |
| **Acceptance gate 7** Zero return-True stubs | Steps 11.3, 11.5, 13.7(g) | ✅ |
| **Acceptance gate 8** `verify-implementation` live + dispatch-reachability CI-enforced | Steps 10.2-10.3, 13.7(h) | ✅ |
| **§Contract item 1** Recurrence regression fixture | Step 2.5 (id_containment) + Step 3.4 (anti_instinct) + Step 11.6 (retry) + Phase 13 (full corpus) + Step 13.3 (master invariant test) | ✅ |
| **§Contract item 2** Dispatch-reachability invariant | Step 8.4 (`test_dispatch_reachability.py`) | ✅ |
| **§Contract item 3** Producer-side over validator (PR lint) | Step 13.4 (PR-review-blocking) | ✅ |
| **§Contract item 4** No silent PASS on empty target | Step 11.5 (`test_gate_empty_target.py`) | ✅ |
| **§Contract item 5** No return-True stubs lint | Step 11.5 (`test_no_fragility_stubs.py`) | ✅ |
| **§Contract item 6** Parser consistency | Step 11.2 + Step 13.2 (`frontmatter_parser/` fixtures) + Phase 13 corpus | ✅ |
| **§Contract item 7** Retry mutates input | Step 11.6 (`test_retry_contract.py`) | ✅ |
| **§Contract item 8** Threshold registry conformance | Step 4.5 (`test_threshold_registry.py`) | ✅ |
| **§Contract item 9** Spec↔Roadmap ID containment | Step 2.4 + Step 2.6 | ✅ |
| **§Contract item 10** Adversarial FP corpus | Step 3.4 (≥3 FP fixtures) | ✅ |

**Unmapped requirements:** None. Coverage = 28/28 = **1.00**.

### D3. Deviation-classification clarity (Contract↔step mapping + PRESERVE-target audit) — **5/5**

**Contract-to-step traceability:** Every checklist item carries an explicit `Contract #N` citation in either the step body or its phase header. All 10 Contract items appear with their specific test-surface filename:

- #1 → `test_recurrence_regression.py` (Step 13.3)
- #2 → `test_dispatch_reachability.py` (Step 8.4)
- #3 → PR description lint (Step 13.4)
- #4 → `test_gate_empty_target.py` (Step 11.5)
- #5 → `test_no_fragility_stubs.py` (Step 11.5)
- #6 → `test_parser_consistency.py` (Steps 11.2 + 13.2)
- #7 → `test_retry_contract.py` (Step 11.6)
- #8 → `test_threshold_registry.py` (Step 4.5)
- #9 → `test_spec_roadmap_id_containment.py` (Step 2.6)
- #10 → `test_anti_instinct_recurrence.py` (Step 3.5)

**PRESERVE-target audit:** The four named PRESERVE targets are protected at three layers:

1. **Scope block (L166-174)** explicitly lists `commands.py`, `structural_checkers.py`, `convergence.py`, `cosmetic_remediator.py` as "out-of-scope, do NOT touch" with the MVR section citation for each.
2. **Constraints block (L187)** restates: "`commands.py` 20 options frozen, `structural_checkers.py` v3.05 layer untouched, `convergence.py` public API + atexit + `compute_stable_id` SHA256 input format stable."
3. **Every rf-qa adversarial prompt** for R0.1, R0.3, R0 acceptance, R1.1, R1.2, R1.3, R1.4, R1.5, R1.6 explicitly verifies these files are unchanged. Phase Gate PG13.1 grep-diffs `commands.py` against research/01 §A.1 inventory for the 20 options.

No step in the tasklist edits these files. Step 11.4 explicitly notes "`convergence.py` is PRESERVE (only the gate wiring changes, not convergence.py itself)" — i.e., it modifies how `gates.py` *consumes* convergence, never `convergence.py` internals. The `refs/adversarial-integration.md` skill prose file is also held PRESERVE through Phase 12 (Step 12 phase header + Step 12.5 confirms it remains untouched).

### D4. Risk-surface coverage vs master:§Flaws 1-5 — **5/5**

| Master flaw | Tasklist structural fix | Adequacy |
|---|---|---|
| **Flaw 1** Artifact-centric gates, no code-reaching terminal link | R1.3 (`CodeAssertion` slot + AST walk) + R1.5 (`verify-implementation` terminal step) | Substrate inversion: gate signatures gain an AST-grounded predicate type, and the missing Link 3 (Tasklist → Code) is added as a fail-closed terminal step. Master §Flaw 1's "INHERENT — gate signature cannot be extended without rewriting every gate's contract" is exactly what R1.3 does. ✅ |
| **Flaw 2** Generator/validator asymmetry | R1.4 tool-write rewrite for all 9 LLM steps with JSON schemas, generator-side constraint `roadmap_ids ⊆ envelope.spec_ids ∪ accepted_deviations` | This is the structural inversion master §Flaw 2 says is missing: schemas pin output shape at production time, killing the "open-ended generator surface" property. The R1.4 sub-phase split (9 separate sub-phases each with side-by-side parity for ≥3 release cycles) directly addresses Vector A's stated risk. ✅ |
| **Flaw 3** Cross-step state in markdown frontmatter | R1.2 typed `PipelineEnvelope` + sidecar JSON + Python post-extractors that write gate-pass counts (LLM never writes them) | The state model is moved from frontmatter to a typed dataclass with deterministic-Python extraction. Master §Flaw 3's "INHERENT — replacing the substrate requires a typed state model at every step" is exactly Step 7.3's dispatch map of 14 post-extractors. ✅ |
| **Flaw 4** Retry without input mutation + silent-skip | Contract #7 lint (`test_retry_contract.py`, Step 11.6) for retry-mutates-input invariant; fail-closed defaults via R1.6 deletion of `found=True` + R1.5 fail-closed `verify-implementation` | Master §Flaw 4 is classified PATCH-FIXABLE for retry-with-mutation and INHERENT for silent-skip. The tasklist addresses both halves: retry mutation via Contract #7 CI gate; silent-skip via systematic fail-open removal in R1.6 + verify-implementation fail-closed terminal. ✅ |
| **Flaw 5** No cross-skill/cross-step contract schema | R0.3 + R1.1 `superclaude.contracts` SoT module (ID_PATTERNS, CONVERGENCE_THRESHOLDS, GATE_FIELD_NAMES, RETURN_CONTRACTS, threshold registry, parsers submodule) + arch-lint blocks duplicate definitions | Master §Flaw 5's "dozens of coupling points coordinated only via prose and `make verify-sync`" is directly inverted by R0.3+R1.1 plus the arch-lint blocker. ✅ |

The substrate inversion is structurally complete. No flaw is left to a downstream-validator-style patch.

### D5. Recommendation actionability — **5/5**

Sample of step actionability (file + concrete change + verifier):

- **Step 2.2** — File: `src/superclaude/cli/roadmap/id_registry.py` (NEW). Change: enumerated dataclass fields, function signature, method contracts. Verifier: Step 2.6 unit test + Step 2.7 pytest run.
- **Step 2.4** — File: `src/superclaude/cli/roadmap/gates.py` near L1180-1200. Change: new SemanticCheck `_roadmap_ids_within_spec` with exact `Callable[[str], bool | str]` signature. Verifier: Step 2.7 `test_phantom_id_rejected`.
- **Step 11.4** — File: `fidelity_checker.py` L287-303 + L314-337 + `executor.py:2167`. Change: explicit deletion + replacement. Verifier: `uv run pytest tests/roadmap/test_spec_fidelity.py tests/roadmap/test_convergence.py tests/roadmap/test_executor.py -v`.
- **Step 13.7** — Eight named acceptance gates each have an explicit verification command (`grep -rn "return True\s*#..."`, `uv run python -c "...len(_build_steps(...))..."` etc.) inline.

Every implementation item identifies the source file, the concrete change required, and the verifier (test, lint, grep, or live re-run). Items also include the path to write phase-output artifacts and the structured fix-cycle on QA FAIL.

---

## Coverage Matrix

See D2 table above — 28/28 spec requirements mapped.

---

## Unmapped Requirements

**None.**

---

## Findings

### CRITICAL: 0
None.

### HIGH: 1

**H-1 — Transient fail-open window between R1.5 and R1.6.** Step 10.2 (R1.5) wires `verify-implementation` as a *new* terminal step but instructs the worker to "DELETE the consolidated step per the design (e.g., delete the `wiring-verification` step at L2176 if that's the consolidation choice — this preserves step count ≤14)." Yet `fidelity_checker.py:287-303` and `executor.py:2167` `gate=None` are NOT deleted until Step 11.4. Therefore, in the window between R1.5 landing and R1.6 landing, the production pipeline contains both the *new* fail-closed `verify-implementation` terminal AND the *old* fail-open `found=True` fallback in `fidelity_checker._scan_codebase`. Step 10.2 also explicitly references "the deleted fidelity_checker.py:287-303 pattern" (saying "NO `found=True` fallback like the deleted pattern") — but at the time R1.5 ships, the block is not yet deleted; deletion is in Phase 11.4. The risk is two-fold:

1. **R1.5 acceptance theatre.** PG10.1 (rf-qa) verifies "fail-closed default (no `found=True` fallback)" — but `fidelity_checker.py:287-303` still contains it during R1.5 review. The gate may pass on the narrow grounds that verify-implementation itself is fail-closed while leaving the architectural Flaw 1 evidence chain partly intact.
2. **R1.6 dependency on R1.5.** Step 11.4 says "the R1.5 `verify-implementation` step now provides the AST-grounded resolution path, so fail-open is no longer needed" — this is only true if R1.5 actually replaced `wiring-verification` (one of the consolidation options) AND if all consumers of the deleted fail-open branch route through `verify-implementation` rather than `fidelity_checker` directly. The design decision is deferred to Step 10.1's design doc, which is fine, but the dependency should be made explicit: **R1.6 Step 11.4 MUST verify that R1.5's consolidation choice routed every former fail-open consumer through verify-implementation; otherwise some consumers of `fidelity_checker._scan_codebase` will get raw `found=True` for one release cycle.**

**Remediation:** Add a Step 10.4 (or strengthen 10.2) requiring R1.5 to land with the fail-open branches in fidelity_checker temporarily annotated `# DELETED IN R1.6 — re-routed through verify-implementation` and a smoke-test asserting that during the R1.5-only window the only path the production pipeline takes is through verify-implementation, never back through fidelity_checker fail-open. Alternatively, swap the order: do R1.6 fail-open deletion before R1.5 verify-implementation lands, by making verify-implementation a parallel branch that becomes terminal only when R1.6 ships. The current ordering carries a one-release-cycle architectural-flaw-1 window.

### MEDIUM: 3

**M-1 — R1.4 cadence realism: 9 sub-phases × ≥3 release cycles each = ~27 release cycles minimum.** Vector A's "stage one step at a time, side-by-side ≥3 releases each before deletion" is faithfully encoded in Steps 9.2-9.10 and the cutover criterion at Step 9.12 ("3 consecutive parity-passing releases"). However, the BUILD-REQUEST estimates R1 at 6-10 eng-weeks; if a "release cycle" is interpreted strictly (i.e., a full external-spec end-to-end run of the pipeline), 9 × 3 = 27 release cycles is plausibly 27+ weeks unless release cycles run in parallel across sub-phases. The tasklist does not state whether sub-phase parity can be batched (i.e., can extract + extract_tdd run their side-by-side cycles concurrently?) or must serialize. Step 9.12 implies serialization ("cutover only after the sub-phase has 3 passing releases").

**Remediation:** Phase 9 should add an explicit parallelism policy: "Sub-phases may run side-by-side dual-write *concurrently*, but each sub-phase's cutover decision is independent." Without this, an honest read of the cadence rules pushes R1.4 alone past the 10-week estimate.

**M-2 — Dispatch-reachability AST walker corner cases (Step 8.4).** Step 8.4 creates `test_dispatch_reachability.py` to assert "the symbol is reachable from a production entry point (`_build_steps()`, `execute_sprint()`, `run_portify()`, `execute_pipeline()`)" per Contract #2. Step 8.3 wires the first CodeAssertion as `build_certify_step` reachability. But the actual reachability for `build_certify_step` may be conditional — i.e., `_build_steps` may construct it only under certain config branches (`config.certify_enabled`?). The Step 8.4 test design as written ("AST walk + dispatch-graph trace") will produce false NEGATIVES on conditionally-wired steps, which is exactly the false-PASS condition Contract #2 is supposed to *prevent*. The test needs to enumerate config matrices, not just call `_build_steps(default_config)`.

**Remediation:** Step 8.4 should require the dispatch walker to enumerate all RoadmapConfig variants (convergence on/off, fix-tasklist mode, etc.) and assert reachability under at least one configuration. The Step 8.4 prose currently does not specify this; an attentive worker will get it right but an under-instructed one may produce a single-config walker that hits the same vacuous-PASS failure mode the contract is supposed to close.

**M-3 — Contract #3 PR-description lint enforcement mechanism is under-specified.** Step 13.4 wires Contract #3 ("Generator-Constraint Considered" PR description section) as a PR-review-blocking gate, but the actual mechanism — is it a GitHub Actions workflow that parses PR body? A bot comment? A `make` target that compares PR description against `gates.py`/`structural_checkers.py`/`*_validator.py` diff? — is left abstract. The §Contract spec says "CI lint blocks merge if section absent on PRs touching `gates.py`, `structural_checkers.py`, or `*_validator.py`"; the tasklist Step 13.4 says only "the Contract #3 'Generator-Constraint Considered' PR description lint." Without a specified mechanism, this gate is the most likely Contract item to ship as decorative.

**Remediation:** Step 13.4 should explicitly require either a GitHub Actions workflow file path (`.github/workflows/contract-3-generator-constraint.yml`) or a `make pr-lint-contract-3` Makefile target with a check command.

---

## Risk-Surface Coverage Assessment (vs master:§Flaws 1-5)

See D4 table above. All five flaws have dedicated structural fixes; only Flaw 1 carries a transient incomplete-substrate window between R1.5 and R1.6 (see HIGH H-1).

---

## PRESERVE-Target Audit

| Target | Cited in scope-out | Cited in constraints | Verified in rf-qa probes | Touched anywhere in tasklist? |
|---|---|---|---|---|
| `cli/roadmap/commands.py` | ✅ L170 (MVR §6.3) | ✅ L187 | ✅ R0.1, R0.3, R0-accept, R1.1, R1.2, R1.3, R1.4, R1.5, R1.6, PG13.1 | ❌ NO |
| `cli/roadmap/structural_checkers.py` | ✅ L171 (MVR §3) | ✅ L187 | ✅ R0-accept, R1.3, R1.4, R1.6, PG13.1 | ❌ NO |
| `cli/roadmap/convergence.py` | ✅ L172 (MVR §5) | ✅ L187 | ✅ R0-accept, R1.2, R1.3, R1.4, R1.5, R1.6, PG13.1 | ❌ NO (only `gates.py` consumes `convergence.RunMetadata`/`ConvergenceResult` per Step 11.4) |
| `cli/roadmap/cosmetic_remediator.py` | ✅ L173 (MVR §2.8 passthrough) | — | ✅ R1.4, R1.6, PG13.1 | ❌ NO |
| `skills/sc-roadmap-protocol/refs/adversarial-integration.md` | — | ✅ L207 (Open Q 4) | ✅ Phase 12 header + Step 12.5 + PG12.1(c) | ❌ NO (Phase 12 explicitly skips this file) |

**Verdict:** PRESERVE targets are systematically honored. No leakage detected.

---

## Open Questions Carried into Execution

The tasklist § Open Questions (L201-208) resolves all five flagged research-gate items in-line. None left unresolved.

---

## Recommendation

**Ship-as-is with two pre-execution clarifications:**

1. **Resolve HIGH H-1 (R1.5/R1.6 fail-open window)** by either (a) annotating fidelity_checker fail-open branches as "DELETED IN R1.6" with a parity assertion in PG10, or (b) re-ordering: do R1.6 cleanup of `_scan_codebase` fail-open before R1.5 wires verify-implementation as terminal. Option (a) is lower-cost.

2. **Resolve MEDIUM M-1 (R1.4 parallelism policy)** by adding an explicit statement at the head of Phase 9 that sub-phases run side-by-side cycles concurrently, with each sub-phase's cutover decision independent.

The two MEDIUM findings on dispatch walker (M-2) and Contract #3 lint mechanism (M-3) are deferrable to the affected phases but should be addressed in-step before those phases close.

Overall: this is a **PASS** for sc:reflect UC-1. The plan is architecturally complete, evidence-grounded, scope-disciplined, and structurally inverts the four INHERENT flaws at their roots. The substrate inversion is genuinely *not* a downstream-validator patch — every flaw's fix is at the substrate layer (gate signature, generator schema, state model, contract registry). The MultiModelSwarm seed case is explicitly wired as Phase 3's blocking driver, with both a unit-test invariant (Step 3.5) and a live-pipeline re-run verification (Step 3.8).
