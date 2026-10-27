# v3.05 Compatibility Audit — Merged Report

> Produced by adversarial merge of two independent audit runs against the same codebase.
> Claims verified against `src/superclaude/cli/roadmap/` at commit `f4d9035`.

---

## Executive Summary

**The v3.05 spec (Deterministic Fidelity Gates) cannot be implemented as written.** It was authored before v3.0 shipped. v3.0 pre-implemented ~60% of the v3.05 infrastructure. The spec must be rewritten from "greenfield build" to "extend existing code" before implementation begins.

By the numbers:

- **19** spec requirements already fully satisfied (zero work needed, including FR-10 run-to-run memory)
- **3** HIGH conflict files where spec says CREATE but code already exists
- **4** modifications needed on existing code
- **2** genuinely new modules to build (spec_parser.py, structural_checkers.py)
- **1** dead code file to remove (fidelity.py)
- **1** missing orchestration entrypoint (validate_semantic_high)
- **1** design-level mismatch (MorphLLM vs ClaudeProcess remediation model)
- **1** entirely new infrastructure module with no existing code (severity rule tables — FR-3)

**MorphLLM Decision (resolved)**: MorphLLM exists as an MCP server (`morphllm-fast-apply`) requiring `MORPH_API_KEY`. It is NOT integrated into the roadmap pipeline — all remediation currently uses `ClaudeProcess`. **Resolution**: Use ClaudeProcess with MorphLLM-compatible patch format (spec's JSON schema) so that MorphLLM can be adopted later without code changes. FR-9 patch dataclass is valid regardless of execution engine.

---

## 1. Module Existence Conflicts (CRITICAL)

The spec claims these as new modules. They already exist.

| Module | Spec Says | Reality | Lines | Resolution |
|--------|-----------|---------|-------|------------|
| convergence.py | CREATE new | Already exists (v3.0) | 323 | Reclassify → MODIFY. Extend with `execute_fidelity_with_convergence()` and `handle_regression()` |
| semantic_layer.py | CREATE new | Already exists (v3.0) | 336 | Reclassify → MODIFY. Add `validate_semantic_high()` and `run_semantic_layer()` orchestrators |
| remediate_executor.py | CREATE new | Already exists (v3.0) | 563 | Reclassify → MODIFY. Add MorphLLM patch format, change threshold 50→30, per-file rollback |
| deviation_registry.py | CREATE new | Class exists inside convergence.py | — | Either extract to own file or update spec to accept current location |
| spec_parser.py | CREATE new | **Does not exist** | — | ✅ Safe to create |
| structural_checkers.py | CREATE new | **Does not exist** | — | ✅ Safe to create |

**Verification**: `git diff f4d9035` confirms convergence.py, semantic_layer.py, and remediate_executor.py were ADDED in that commit.

---

## 2. Already-Implemented Requirements (No Work Needed)

| Requirement | Location | Status |
|-------------|----------|--------|
| ACTIVE in VALID_FINDING_STATUSES (FR-6/BF-1) | models.py:16 | ✅ Done |
| Finding.source_layer field (FR-6/BF-3) | models.py:44 | ✅ Done |
| RoadmapConfig.convergence_enabled (FR-7) | models.py:107 | ✅ Done |
| RoadmapConfig.allow_regeneration (FR-9.1) | models.py:108 | ✅ Done |
| --allow-regeneration CLI flag | commands.py:89-94 | ✅ Done |
| WIRING_GATE registered in ALL_GATES | gates.py:944 | ✅ Done |
| SPEC_FIDELITY_GATE conditional bypass | executor.py:521 | ✅ Done |
| DeviationRegistry full lifecycle (load/save/merge) | convergence.py:50-225 | ✅ Done |
| compute_stable_id() | convergence.py:24-32 | ✅ Done |
| ConvergenceResult dataclass | convergence.py:228-237 | ✅ Done |
| _check_regression() structural-only (BF-3) | convergence.py:240-272 | ✅ Done |
| Temp dir isolation + atexit cleanup (FR-8) | convergence.py:278-323 | ✅ Done |
| All prompt budget constants (FR-4.2) | semantic_layer.py constants | ✅ Done |
| build_semantic_prompt() with budget enforcement | semantic_layer.py | ✅ Done |
| Debate scoring (RubricScores, score_argument, judge_verdict) | semantic_layer.py | ✅ Done |
| Snapshot create/restore/cleanup | remediate_executor.py:53-101 | ✅ Done |
| Run-to-run memory: prior findings summary (FR-10) | convergence.py:179-188 (`get_prior_findings_summary`) | ✅ Done |
| Prior findings in semantic prompt (FR-10) | semantic_layer.py:140,215-221 (`prior_findings_summary` field + prompt integration) | ✅ Done |
| first_seen_run / last_seen_run tracking (FR-10) | convergence.py:104-130 | ✅ Done |

Gate authority mutual exclusion is also already implemented:
- `gate=None if config.convergence_enabled else SPEC_FIDELITY_GATE` (executor.py)

---

## 3. Modifications Needed on Existing Code

| What | Current | Spec Requires | File |
|------|---------|---------------|------|
| Diff-size threshold | 50% | 30% | remediate_executor.py:45 |
| Diff-size granularity | Per-file | Per-patch | remediate_executor.py |
| Rollback scope | All-or-nothing | Per-file | remediate_executor.py |
| TRUNCATION_MARKER | Missing heading name | Include `<heading>` | semantic_layer.py |

**Verified**: `_DIFF_SIZE_THRESHOLD_PCT = 50` at remediate_executor.py:45, used at lines 453, 458, 467.

---

## 4. Genuinely New Code to Build

| Component | Spec Ref | Description |
|-----------|----------|-------------|
| spec_parser.py | FR-2 | Spec & roadmap structural data extraction |
| structural_checkers.py | FR-1 | 5 deterministic dimension checkers (no LLM) |
| Severity rule tables | FR-3 | Anchored `(dimension, mismatch_type) → severity` mappings for all 5 checkers. Entirely new — no existing code. `compute_stable_id()` uses `mismatch_type` as a hash input (convergence.py:28-31) but no rule table infrastructure exists. |
| Section splitter for chunked comparison | FR-5 | Split spec/roadmap by headings for per-section checker input. `_truncate_to_budget()` exists in semantic_layer.py but no section-splitting logic. |
| validate_semantic_high() | FR-4.1 | Orchestrator: parallel prosecutor/defender via ClaudeProcess |
| run_semantic_layer() | FR-4 | Top-level semantic layer entry point |
| execute_fidelity_with_convergence() | FR-7 | 3-run convergence loop orchestrator |
| handle_regression() | FR-8 | Full regression flow (spawn agents, validate, debate, update) |
| RemediationPatch dataclass | FR-9 | MorphLLM lazy edit snippet model |
| apply_patches() | FR-9 | Sequential per-file, per-patch diff guard |
| fallback_apply() | FR-9 | Deterministic text replacement (anchor matching) |
| check_morphllm_available() | FR-9 | MCP runtime probe |
| roadmap_run_step() convergence branch | FR-7 | Bypass Claude subprocess, delegate to convergence engine |
| Finding fields: rule_id, spec_quote, roadmap_quote, stable_id | FR-6 | Extend dataclass in models.py |

**Verified gap**: `validate_semantic_high()` is referenced in a docstring at semantic_layer.py:321 but **no function definition exists**. This is a real gap, not a phantom.

---

## 5. Dead Code

| File | Verdict | Evidence |
|------|---------|----------|
| fidelity.py (66 lines) | **DELETE** | `from .fidelity import` returns zero matches across entire codebase. Severity enum and FidelityDeviation dataclass never wired. Superseded by Finding + DeviationRegistry. |
| convergence.py:RunMetadata | **Dead within file** | Dataclass defined at line 36. `RunMetadata(` never instantiated anywhere — begin_run() uses raw dicts instead. |

---

## 6. Files That Must Be Kept

| File | Why |
|------|-----|
| spec_patch.py | **Active call sites**: imported in commands.py:210 (`prompt_accept_spec_change`) and executor.py:1397 (`scan_accepted_deviation_records`). Handles spec-hash reconciliation and accepted-deviation workflow. No overlap with FR-9. |
| prompts.py:build_spec_fidelity_prompt() | Used in legacy mode (convergence_enabled=false). Still generates human-readable report even in convergence mode. |

**Note**: The v3.05 spec does not mention spec_patch.py at all. This is an omission — the accepted-deviation workflow must be explicitly scoped as either preserved legacy or coexisting with v3.05.

---

## 7. Architectural Tensions

### 7a. Convergence Loop vs Linear Pipeline

The pipeline is single-pass. v3.05's convergence engine needs up to 3 runs within step 8. The loop must be self-contained — not re-running the full pipeline. Pattern exists: wiring-verification bypass (executor.py:244-259).

Current pipeline order:
1. extract → 2. generate-* (parallel) → 3. diff → 4. debate → 5. score → 6. merge → 7. test-strategy → 8. spec-fidelity → 9. wiring-verification

FR-7 should describe convergence as **altering existing step-8 authority and behavior**, not adding a brand new pipeline phase.

### 7b. Remediation Ownership

Current remediation is post-pipeline. v3.05 needs remediation **within** the convergence loop (between runs). Tension with `_check_remediation_budget()` and `_print_terminal_halt()` which assume remediation is external.

### 7c. MorphLLM vs ClaudeProcess Design Gap (RESOLVED)

FR-9 describes "MorphLLM-compatible lazy edit snippets" as the remediation model. The current implementation uses **ClaudeProcess with remediation prompts** and a post-hoc diff-size check. **Decision**: Use ClaudeProcess (established pattern) with MorphLLM-compatible patch format (FR-9's JSON schema). MorphLLM MCP exists but requires API key and is not integrated. This approach preserves future MorphLLM migration without blocking implementation. See executive summary and Priority 3 for full rationale.

### 7d. SPEC_FIDELITY_GATE + Wiring Step Ordering

v3.0 places wiring-verification after spec-fidelity, assuming spec-fidelity always runs. When convergence_enabled=true, spec-fidelity gate is None. Wiring step still works (no dependency on spec-fidelity output), but step ordering semantics need documenting.

### 7e. FR-3 Severity Rules as Foundation Risk (HIGH)

Severity rule tables (FR-3) are entirely new — no code exists. Yet every structural checker (FR-1) depends on them to assign severity. If the rule tables are wrong, all 5 checkers produce incorrect findings, which cascade through the deviation registry (FR-6), convergence gate (FR-7), and regression detection (FR-8). This is a foundational dependency that must be built and validated early.

### 7f. spec_parser.py as Critical Path (MEDIUM)

spec_parser.py (FR-2) is on the critical path: FR-1 depends on FR-2. FR-4 depends on FR-1. FR-7 depends on FR-6 which consumes FR-1 output. Parser robustness against real-world specs (which deviate from templates) is flagged as implementation risk #1 in the spec itself but was not surfaced in the original audit.

### 7g. FR-7/FR-8 Circular Interface (MEDIUM)

FR-7 (convergence gate) triggers FR-8 (regression detection) when structural HIGHs increase. FR-8 consumes FR-7's budget tracking and produces findings that feed back into FR-7's registry evaluation. This circular dependency requires careful interface design — specifically, the regression validation flow must count as one "run" toward the budget of 3 (spec FR-8 AC item 13).

---

## 8. Spec Rewrite Queue (Prioritized)

### Priority 1 — Stop claiming greenfield creation of existing modules

Revise these FR sections to acknowledge existing code:
- **FR-4**: "complete existing semantic layer" not "build semantic layer module"
- **FR-7**: "audit and complete existing convergence.py" not "create convergence engine"
- **FR-8**: "fill missing integration points" not "create temp-dir isolation"
- **FR-9**: Split into already-implemented / conflicting / missing subsections

### Priority 2 — Add "existing baseline from v3.0" section

Document explicitly:
- Pre-existing modules (convergence.py, semantic_layer.py, remediate_executor.py)
- Pre-existing fields (ACTIVE, source_layer, convergence_enabled, allow_regeneration)
- Pre-existing pipeline wiring (gate bypass, wiring step, --allow-regeneration)

### Priority 3 — Resolve real behavior mismatches

Decisions (resolved during validation):

- [x] **Diff threshold**: Use **30%** per spec. The spec went through adversarial design review (BF-5); this was a deliberate decision, not a default.
- [x] **FR-9 remediation engine**: Use **ClaudeProcess with MorphLLM-compatible patch format**. MorphLLM MCP exists (`morphllm-fast-apply`) but requires `MORPH_API_KEY` and is not integrated into the roadmap pipeline. ClaudeProcess is the established pattern (executor.py:281, remediate_executor.py:198). Generate patches in FR-9's JSON schema so MorphLLM adoption is a future swap, not a rewrite.
- [x] **validate_semantic_high() location**: Add to **semantic_layer.py** — it's referenced in a docstring there (line 321), and the existing primitives it orchestrates (score_argument, judge_verdict, build_semantic_prompt) are all in that file. FR-4.1 fully specifies the protocol: 2 parallel ClaudeProcess calls → YAML parse → deterministic judge.
- [x] **Prosecutor/defender execution**: Lives in **semantic_layer.py** alongside validate_semantic_high(). Uses `ClaudeProcess` (same pattern as executor.py:281 and remediate_executor.py:198). Two parallel calls, YAML responses, deterministic Python judge.

### Priority 4 — Scope spec_patch.py

Mention spec_patch.py explicitly, either:
- As preserved legacy/support flow, or
- As part of accepted-deviation handling that coexists with v3.05

---

## Provenance

| Section | Primary Source | Verified Against |
|---------|---------------|-----------------|
| Module conflicts (§1) | Report 01 tables | git diff f4d9035, file reads |
| Implemented requirements (§2) | Report 01 tables | grep verification |
| Modifications (§3) | Report 01 tables | `_DIFF_SIZE_THRESHOLD_PCT = 50` confirmed |
| New code (§4) | Report 01 tables + Report 02 gap analysis | `validate_semantic_high` grep: docstring only |
| Dead code (§5) | Report 01 verdict | `from .fidelity import` → 0 matches; `RunMetadata(` → 0 matches |
| Files to keep (§6) | Report 01 + Report 02 | spec_patch.py import sites confirmed |
| Architectural tensions (§7) | Both reports + Report 02 MorphLLM insight | Code inspection |
| Rewrite queue (§8) | Report 02 structure | Merged with Report 01 specifics |

**Discarded from Report 02**: Suggestion that fidelity.py might be worth keeping — verified dead, zero imports.

**Adopted from Report 02 over Report 01**: Stronger framing ("do not implement as written"), MorphLLM design gap identification, spec_patch.py scoping recommendation, prioritized rewrite queue structure.

**Validation pass additions**: FR-3 (severity rules), FR-5 (sectional comparison), FR-10 (run-to-run memory) coverage added. FR-10 verified as already implemented. MorphLLM availability investigated — exists as MCP server but not integrated; decision resolved to use ClaudeProcess with compatible patch format. Three new architectural risks added (§7e-7g). All four Priority 3 decisions resolved with evidence.
