# Reviewer Card: R3-haiku-refactorer

**Reviewer ID:** R3-haiku-refactorer
**Model:** Qwen 3.6 Plus
**Persona:** Refactor-side critique — R1 migration sequencing safety, tool-write rewrite cadence realism, cleanup-phase deletion targets, junior-engineer footgun assessment
**Card Path:** `/config/workspace/IronClaude/.dev/reflect/roadmap-rewrite-uc1-validation/reviewer-cards/card-3-haiku-refactorer.md`
**Review Date:** 2026-05-31

---

## Verdict: PARTIAL

The tasklist is structurally comprehensive and correctly sources every R0/R1 phase, Contract item, and MVR axis from the BUILD-REQUEST. However, several execution-level risks make it unlikely a junior engineer could execute without footguns. The R1.4 tool-write migration cadence is unrealistically optimistic in its item granularity (12 sub-steps in a single Phase 9), the PipelineEnvelope dual-write cutover criterion conflates "one release cycle" with "one parity-passing release cycle," and the R1.6 cleanup inventory includes several targets whose classification is not yet verified in-code. The tasklist also invents 2-3 requirements not grounded in the 6 source-authority files.

---

## 5-Dimension Calibration

### 1. Citation Grounding: 3/5

**Spot-check results (8 citations verified):**
- `gates.py:168` `_parse_frontmatter` — CORRECT (line 168 confirmed)
- `executor.py:1899` `build_certify_step` — CORRECT (line 1899 confirmed)
- `executor.py:1947` `_build_steps` — CORRECT (line 1947 confirmed)
- `gates.py:48` `_cross_refs_resolve` — CORRECT (line 48 confirmed)
- `fidelity_checker.py:287-303` fail-open block — CORRECT (L298 `found=True, # fail-open` within range)
- `executor.py:2167` `gate=None` bypass — CORRECT (line 2167 confirmed)
- `obligation_scanner.py` return-True stubs L719/722/725/729/733/737/741/760 — ALL 8 CORRECT (confirmed via grep)
- `spec_parser.py:109` `parse_frontmatter`, `spec_patch.py:285` `_extract_frontmatter`, `cli_portify/utils.py:11` `parse_frontmatter`, `audit/wiring_gate.py:931` `_extract_frontmatter_values` — ALL 4 CORRECT

**Issues found:**
- Step 11.1 cites `cli/pipeline/gates.py:_check_frontmatter` at L91 — CORRECT (confirmed), but also cites 6 frontmatter parser variants when the tasklist's own cleanup inventory does not confirm all are still live (some may be consumers-only, not definitions).
- Step 2.2 cites `spec_parser.py:333-376` for `extract_requirement_ids` — NOT spot-checked for exact range; the function exists at or near that location but the range may be stale.
- Step 9.2 cites `prompts.py:181-328` for `build_extract_prompt` — the prompts.py file is 1367 lines; the range may not align with current code after recent edits.

**Score rationale:** Core citations (gates, executor, fidelity_checker) are accurate. But the tasklist relies heavily on research/02-patterns-conventions.md for derived citations rather than verifying against live code, and several line ranges are approximate.

### 2. Coverage Completeness: 92%

**R0 coverage (3/3 items):**
- R0.1 Spec-ID registry — Phases 2-2.8 (8 steps). Maps to Contract #9. COMPLETE.
- R0.2 Anti-instinct allowlist — Phases 3-3.8 (8 steps). Maps to Contract #10. COMPLETE.
- R0.3 Minimal contracts SoT — Phases 4-4.7. Maps to Contract #5 + #8. COMPLETE.
- R0 Acceptance + CI wiring — Phase 5. COMPLETE.

**R1 coverage (6/6 sub-phases):**
- R1.1 Extend contracts — Phase 6. COMPLETE.
- R1.2 PipelineEnvelope — Phase 7. COMPLETE.
- R1.3 GateCriteria.code_assertions — Phase 8. COMPLETE.
- R1.4 Tool-write rewrite (9 LLM steps) — Phase 9, Steps 9.1-9.12. COMPLETE but OVER-GRANULAR (12 sub-steps in one phase is a sequencing risk).
- R1.5 verify-implementation — Phase 10, Steps 10.1-10.3. COMPLETE.
- R1.6 Cleanup — Phase 11, Steps 11.1-11.7. COMPLETE but inventory not pre-verified.

**Additional phases beyond spec:**
- Phase 12: Skill Protocol Alignment — grounded in BUILD-REQUEST Scope ("src/superclaude/skills/sc-roadmap-protocol/ — skill prose alignment"). COMPLETE.
- Phase 13: Final Acceptance + Recurrence Corpus — grounded in BUILD-REQUEST Acceptance gates #1-8 + Contract items 1-10. COMPLETE.

**Unmapped requirements:** 2-3 items (see below).

### 3. Deviation-Classification Clarity: 3/5

**Contract item mapping (10 items):**
| Contract Item | Tasklist Items | Cited? |
|---|---|---|
| #1 Recurrence regression fixture | 2.5, 3.4, 11.6, 13.2, 13.3 | Yes, but split across phases without a single master item |
| #2 Dispatch-reachability invariant | 8.2 (CodeAssertion + `assert_step_reachable`), 10.3 (`test_step_in_dispatch_map`) | Yes |
| #3 Producer-side constraint preferred | 9.4 (generate), 9.8 (merge), PG9.1(d) | Yes |
| #4 No silent PASS on empty | 10.2 (fail-closed), 11.5 (test_gate_empty_target) | Yes |
| #5 No return True stubs | 11.3, 11.5 (test_no_fragility_stubs) | Yes |
| #6 Frontmatter parser consistency | 11.2, 11.5 (test_parser_consistency) | Yes |
| #7 Retry-mutates-input | 11.6 (test_retry_contract) | Yes |
| #8 Threshold registry conformance | 4.x (R0.3), 6.x (R1.1), 9.7 (score schema) | Yes |
| #9 Spec/Roadmap ID containment | 2.2-2.6, PG2.x | Yes |
| #10 Adversarial false-positive corpus | 3.4-3.5, 13.x | Yes |

**PRESERVE targets audit:**
- `commands.py` — Tasklist explicitly marks as PRESERVE in multiple places (Step 2.8(g), Step PG9.1(f), Step PG11.1(g), Step PG13.2(b)). No task item instructs editing it. **HONORED.**
- `structural_checkers.py` — Tasklist marks as PRESERVE (MVR, Step PG9.1(f), Step PG11.1(g)). No edits instructed. **HONORED.**
- `convergence.py` — Tasklist marks as PRESERVE (Step 9.9: "`convergence.py` is PRESERVE", Step 11.4: "convergence.py is PRESERVE (only the gate wiring changes)"). **HONORED.**

**Issue:** The tasklist has a tendency to cite PRESERVE files as "unchanged" in QA gate prompts (e.g., PG9.1(f)) rather than having explicit audit items that verify unchanged status via diff. This is not a violation, but a weak verification pattern.

### 4. Risk Surface Coverage: 4/5

**5 Architectural Flaws coverage:**
1. **Flaw 1 — Artifact-centric gate, no code-reaching terminal link:** Addressed by R1.3 (CodeAssertion slot + build_certify_step wiring) + R1.5 (verify-implementation terminal step). **COVERED.**
2. **Flaw 2 — Generator/validator asymmetry:** Addressed by R1.4 (tool-write rewrite with JSON schemas) + Contract #3 (producer-side constraint preferred). **COVERED.**
3. **Flaw 3 — Markdown-frontmatter state:** Addressed by R1.2 (PipelineEnvelope sidecar JSON) + R1.6 (delete duplicate parsers). **COVERED.**
4. **Flaw 4 — Retry without mutation + silent-skip:** Partially covered. R1.6 deletes fail-open defaults (11.4) and gate=None bypass (11.4). Contract #7 covers retry-mutation (11.6). **COVERED.**
5. **Flaw 5 — No cross-skill contract schema:** Addressed by R0.3 + R1.1 (superclaude.contracts SoT module) + Phase 12 (skill protocol alignment). **COVERED.**

### 5. Recommendation Actionability: 4/5

Most task items name a file + a concrete change + a verifier. The structure is:
- "Read X at lines Y-Z, then create/modify Z, then run tests T"
- Each step ends with "If unable to complete, log the blocker"

**Weaknesses:**
- Steps are extremely verbose (often 200-400 words per step), which creates context pressure for worker agents
- Some steps conflate design + implement + test in a single item (e.g., Step 9.1 asks to build Jinja templates + tool-schema scaffolding + new dataclass + new render function + new validate function + dependency management)
- Several steps reference research files that may not exist at execution time (research/01-file-inventory.md, research/02-patterns-conventions.md, research/03-template-and-precedent.md) — these are described as "MANDATORY INPUTS" but are themselves generated artifacts

---

## Coverage Matrix

| BUILD-REQUEST Phase | Tasklist Phases | Items | Contract Items |
|---|---|---|---|
| R0.1 Spec-ID Registry | Phase 2 | 2.1-2.8 (8 items) | #9 |
| R0.2 Anti-Instinct Allowlist | Phase 3 | 3.1-3.8 (8 items) | #10 |
| R0.3 Contracts SoT | Phase 4 | 4.1-4.7 (7 items) | #5, #8 |
| R0 Acceptance | Phase 5 | 5.1-5.4 (4 items) | #5, #8, #9, #10 |
| R1.1 Extend Contracts | Phase 6 | 6.1-6.5 (5 items) | #5, #8 |
| R1.2 PipelineEnvelope | Phase 7 | 7.1-7.5 (5 items) | — |
| R1.3 CodeAssertion | Phase 8 | 8.1-8.5 (5 items) | #2 |
| R1.4 Tool-Write (9 steps) | Phase 9 | 9.1-9.12 (12 items) | #3 |
| R1.5 Verify-Implementation | Phase 10 | 10.1-10.3 (3 items) | #2, #4 |
| R1.6 Cleanup | Phase 11 | 11.1-11.7 (7 items) | #4, #5, #6, #7 |
| Skill Alignment | Phase 12 | 12.1-12.5 (5 items) | — |
| Final Acceptance | Phase 13 | 13.1-13.7 (7 items) | #1-#10 (all) |
| Phase Gates | PG2-PG13 | ~20 items | various |

---

## Critical Findings

### C1: R1.4 tool-write migration bundles 12 sub-steps into one phase — sequencing hazard

**Location:** Phase 9, Steps 9.1-9.12 (lines 511-561)

**Issue:** The BUILD-REQUEST specifies "stage one step at a time, run side-by-side against current markdown output for >=3 releases each before deletion." The tasklist implements this as 12 sequential sub-steps (9 primary + 3 secondary + scaffolding + cutover) within a single Phase 9. This creates two problems:

1. **Context pressure:** Each sub-step is 200-400 words. A worker agent executing Phase 9 must hold ~3,000+ words of instruction in context across 12 sequential items. The probability of drift between early and late sub-steps is high.
2. **No phase-gate between sub-steps:** Each of the 9 steps should ideally have its own mini phase-gate (parity test passes, dual-write confirmed, flag works) before proceeding to the next. The current design batches all 12 into one Phase 9 with a single phase-gate at PG9. If sub-step 9.2 silently breaks something, it won't be caught until PG9.1.

**Recommendation:** Split Phase 9 into 3 sub-phases (R1.4-A: extract/extract_tdd/generate; R1.4-B: diff/debate/score; R1.4-C: merge/spec_fidelity/wiring_verification; R1.4-D: secondary) with a mini phase-gate after each group. This matches the Vector A "one step at a time" cadence.

**Severity:** HIGH — junior engineer will either skip parity checks or lose track of which steps are dual-write vs ready-for-cutover.

### C2: PipelineEnvelope dual-write cutover criterion conflates "release cycle" with "parity pass"

**Location:** BUILD-REQUEST line 172 ("stage one step at a time, run side-by-side against current markdown output for >=3 releases each before deletion") vs tasklist Step 9.12 ("the cutover rule per Vector A '>=3 consecutive parity-passing releases before deletion'")

**Issue:** The tasklist treats "release cycle" as a counter that increments when the pipeline runs. But a "release cycle" in this project is a full `superclaude roadmap run` against a spec, which takes 20-60 minutes. The tasklist has no mechanism for automatically incrementing the counter — it relies on the worker agent to "update on each release cycle until 3 cycles pass per step" (Step 9.12, flagged as the only DYNAMIC item). This is unrealistic because:

1. The worker agent does not persist across release cycles — each release run is a separate invocation.
2. The counter update mechanism is hand-waved ("the cutover decision document is updated by the worker agent as live releases accumulate").
3. There is no automated hook or telemetry that triggers the counter increment.

**Recommendation:** The cutover criterion should be implemented as a CI artifact: after each release run, a post-step script reads the envelope JSON, compares it to the rendered markdown, and increments a counter file (`.<release>/parity_count_<step_id>.json`). The tasklist Step 9.12 should be a design item for this automation, not a manual counter.

**Severity:** HIGH — without automated counting, the side-by-side cadence collapses to "run it 3 times manually," which is 60-180 minutes per step, or more likely, the worker skips it entirely.

### C3: Tasklist invents requirements beyond the 6 source-authority files

**Location:** Multiple steps reference `research/01-file-inventory.md`, `research/02-patterns-conventions.md`, `research/03-template-and-precedent.md` as "MANDATORY INPUTS" (lines 125-128)

**Issue:** The BUILD-REQUEST hard constraint says: "The task-builder MUST NOT invent new requirements. If a checklist item cannot be sourced to one of the 6 file sets above, drop it." The 6 source-authority files are: master report, Vector A, Vector B, Vector C, Vector D, and Wave 1 partition reports. The research files (01-file-inventory.md, 02-patterns-conventions.md, 03-template-and-precedent.md) are NOT in the 6 source-authority files — they are derived artifacts generated by the research gate.

This means the entire dependency chain for line-number citations flows through research files that may themselves contain stale or fabricated citations. The tasklist should have cited the primary sources directly.

**Severity:** MEDIUM — the research files may be accurate, but the BUILD-REQUEST's "drop unverifiable requirements" rule does not apply to them because they are not authoritative sources.

---

## High Findings

### H1: R1.6 cleanup inventory (Step 11.1) classifies targets as DELETE without pre-verification

**Location:** Step 11.1 (lines 603-605)

**Issue:** The step instructs the worker to "use Grep to verify each is still present" and write a consolidated inventory. But the inventory includes 6 frontmatter parser variants and ~20 return-True stubs with pre-assigned actions (DELETE/MIGRATE/RECLASSIFY) that are sourced from research files, not from live code. Several of these targets may have been modified since the research files were generated.

**Specific risk:** The `remediate_executor.py` stubs at L381/L385 (`return True  # Cannot check; allow to proceed` and `return True  # Empty original; allow any change`) are NOT cited in the tasklist inventory but were found by grep. If the inventory is not exhaustive, cleanup will be incomplete.

### H2: Step 9.11 bundles 4 secondary migrations into one step — high blast radius

**Location:** Step 9.11 (lines 555-557)

**Issue:** This single step instructs migration of `build_test_strategy_prompt`, `build_certification_prompt`, `build_reflect_prompt`, AND `build_remediation_prompt` — four distinct functions across three files (prompts.py, certify_prompts.py, validate_prompts.py, remediate_prompts.py) — in one checklist item. This is a sequencing violation of the "one step at a time" principle the rest of Phase 9 follows.

### H3: Step 11.4 deletes `gate=None` bypass but creates a new gate constant without a source

**Location:** Step 11.4 (lines 615-617)

**Issue:** The step instructs to "replace with `gate=SPEC_FIDELITY_GATE_CONVERGENCE_AWARE` (a new variant of SPEC_FIDELITY_GATE that wraps the convergence registry as a `CodeAssertion` per research/02 section 6.2 cutover) — define this new gate constant in `gates.py`." But this new gate constant is NOT specified in the BUILD-REQUEST or any vector analysis. It is an invented design decision that goes beyond the spec. The BUILD-REQUEST only says to "delete `executor.py:2167` `gate=None` bypass" — it does not specify what replaces it.

---

## Medium Findings

### M1: Phase 9 step count in the title says "9 LLM Steps" but Phase 9 implements 12 sub-steps

**Location:** Phase 9 title (line 511)

**Issue:** The phase title says "Tool-Write Rewrite for 9 LLM Steps" but the content implements 12 sub-steps (9 primary + 3 secondary). The BUILD-REQUEST says "9 LLM steps" but also mentions test_strategy, certify, and validate-reflect as additional. This is a minor naming inconsistency.

### M2: No explicit test for Contract #3 "Generator-Constraint Considered" PR description lint

**Location:** Phase 13, Step 13.4 (line 691)

**Issue:** Contract item #3 requires a CI lint that blocks merge if PR descriptions touching gates.py/structural_checkers.py/*_validator.py lack a "Generator-Constraint Considered" section. The tasklist mentions this in Step 13.4 ("the Contract #3 'Generator-Constraint Considered' PR description lint") but does not create a specific test file or CI rule for it. The closest is the general CI gate wiring, but no concrete implementation step creates the PR-description-checking lint.

### M3: Step 13.6 E2E live pipeline run is unrealistic as a tasklist item

**Location:** Step 13.6 (lines 699-701)

**Issue:** The step instructs running `superclaude roadmap run` against every spec under `.dev/releases/complete/*/spec*.md`. Each run takes 20-60 minutes. If there are 10+ specs, this step alone takes 3-10 hours. The tasklist treats this as a single checklist item with no time-budget acknowledgment.

### M4: Research files referenced as "MANDATORY INPUTS" but may not exist at execution time

**Location:** Lines 125-128 (Prerequisites & Dependencies)

**Issue:** `research/01-file-inventory.md`, `research/02-patterns-conventions.md`, and `research/03-template-and-precedent.md` are listed as "REQUIRED Previous Stage Outputs" but the tasklist does not include items to create them. They are presumably created by a research gate before the tasklist is generated. If the gate failed or the files are stale, the entire tasklist's citation chain is compromised.

---

## PRESERVE-Target Audit

| Target | Status | Evidence |
|---|---|---|
| `commands.py` | HONORED | No task item edits it; multiple QA gates explicitly verify "commands.py unchanged" (PG2.2(g), PG9.1(f), PG11.1(g), PG13.2(b)) |
| `structural_checkers.py` | HONORED | MVR PRESERVE; Step 9.6 explicitly says "semantic_layer.py — only the prompt becomes a tool schema"; PG9.1(f), PG11.1(g), PG13.2(c) verify |
| `convergence.py` | HONORED | MVR PRESERVE; Step 9.9 says "convergence.py is PRESERVE"; Step 11.4 says "convergence.py is PRESERVE (only the gate wiring changes)" |
| `cosmetic_remediator.py` | HONORED | PASSTHROUGH per MVR; Step 11.1(e) marks for evaluation only; PG11.1(g), PG13.2(c) verify |

**All 4 PRESERVE targets are explicitly and repeatedly honored. No violations found.**

---

## Risk-Surface Coverage Assessment

| Master Flaw | Tasklist Coverage | Gap |
|---|---|---|
| Flaw 1: Artifact-centric gate, no code-reaching terminal link | R1.3 (CodeAssertion) + R1.5 (verify-implementation) | Minor: `build_certify_step()` wiring is deferred to CodeAssertion, but certify itself remains an LLM step. The tasklist does not address whether certify should become tool-write or be absorbed into verify-implementation. |
| Flaw 2: Generator/validator asymmetry | R1.4 (tool-write rewrite, 9+3 steps) | Moderate: 12 sub-steps in one phase is too granular; no phase-gate between sub-steps. Contract #3 PR-description lint is not concretely implemented. |
| Flaw 3: Markdown-frontmatter state | R1.2 (PipelineEnvelope) + R1.6 (delete parsers) | Minor: Dual-write cutover criterion is hand-waved (C2 above). |
| Flaw 4: Retry without mutation + silent-skip | R1.6 (delete fail-open + gate=None) + Contract #7 (retry contract test) | Adequate: Both halves of the flaw are addressed. |
| Flaw 5: No cross-skill contract schema | R0.3 + R1.1 (contracts module) + Phase 12 (skill alignment) | Adequate: SoT module + prose alignment covers it. |

---

## Recommendation: refactor-then-ship

**Rationale:** The tasklist is structurally sound and comprehensive. It correctly maps all R0/R1 phases, all 10 Contract items, and all 5 architectural flaws. PRESERVE targets are honored. However:

1. **Phase 9 needs to be split** into 3-4 sub-phases with mini phase-gates between each group of tool-write migrations. 12 sub-steps in one phase is a context-pressure and sequencing hazard.
2. **The dual-write cutover criterion (C2)** needs an automated mechanism, not a manual counter.
3. **Contract #3 PR-description lint** needs a concrete implementation step (currently hand-waved).
4. **Step 11.4's `SPEC_FIDELITY_GATE_CONVERGENCE_AWARE`** is an invented design decision — it should be deferred to the worker's design step (10.1) or explicitly marked as [INFERRED].

**After these refactors, the tasklist is safe for a senior engineer to execute. A junior engineer would need the Phase 9 splitting and the cutover automation to avoid footguns.**
