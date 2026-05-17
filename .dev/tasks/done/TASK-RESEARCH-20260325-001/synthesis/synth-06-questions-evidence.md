# Synthesis 06 — Open Questions and Evidence Trail

**Report:** Technical Research Report — CLI TDD Integration
**Date:** 2026-03-25
**Phase:** Synthesis — Final Sections
**Sections:** §9 Open Questions · §10 Evidence Trail

---

## §9 Open Questions

The questions below are compiled from all gaps recorded across the six research files and the analyst/QA completeness reports. They are ordered by severity: Critical gaps that could change implementation plan scope appear first, followed by Important gaps that affect synthesis quality, then Minor gaps and the confirmed pre-existing codebase bug.

### Critical Questions

| # | Question | Impact | Suggested Resolution |
|---|----------|--------|----------------------|
| C-1 | Does `semantic_layer.py` (~400 lines) read `spec_file` at any point in the active pipeline? | If yes, it is a 4th implementation point for TDD support missed in this investigation; the implementation plan in synth-05 would be incomplete | Read `src/superclaude/cli/roadmap/semantic_layer.py` in full and trace its call path from `executor.py` — search for `spec_file`, `config.spec_file`, and `read_text` references |
| C-2 | Does `structural_checkers.py` (~200 lines) have spec-format-specific assumptions that would break on TDD structural patterns? | If yes, it requires changes when TDD input produces different section headings, table structures, or identifier patterns | Read `src/superclaude/cli/roadmap/structural_checkers.py` in full; check for hardcoded section names, FR/NFR ID assumptions, or spec-template field expectations |

### Important Questions

| # | Question | Impact | Suggested Resolution |
|---|----------|--------|----------------------|
| I-1 | Does `run_wiring_analysis(wiring_config, source_dir)` in `executor.py:421-433` read `spec_file` via the `wiring_config` object? | If yes, `wiring-verification` becomes a 5th implementation point; the step currently appears to receive only `roadmap.md` and `spec-fidelity.md` as step inputs | Read `executor.py:421-433` and inspect `wiring_config` construction to determine whether `spec_file` or its content is included |
| I-2 | Which downstream extraction frontmatter consumers read `spec_source` or the new TDD-specific count fields (`data_models_identified`, `api_surfaces_identified`, etc.) from extraction output? | If additional consumers exist beyond those documented in 02-prompt-language-audit.md, the aliasing/rename strategy must account for them | Search entire roadmap/ and pipeline/ directories for string `spec_source` to enumerate all read sites; verify each is accounted for in the implementation plan |
| I-3 | What is the correct `spec_source` rename strategy — alias both old and new field names in outputs, rename only new TDD-mode outputs, or keep `spec_source` with a TDD-filename value for full backward compatibility? | Determines whether any gate or prompt builder changes are required beyond the DEVIATION_ANALYSIS_GATE redesign; wrong choice creates silent backward-compat breaks | Enumerate all 5 gates and 2+ prompt builders that require `spec_source`; decide whether TDD-mode Claude output can simply emit `spec_source: <tdd-filename>` and pass unchanged, or whether a dedicated alias field is needed |
| I-4 | How should `build_test_strategy_prompt()` be enriched for TDD input? The current prompt does not read the original spec/TDD file and produces a generic roadmap-based testing plan. | TDD §15 Testing Strategy contains concrete test case tables (unit, integration, E2E) that should feed directly into the test-strategy step rather than being inferred from roadmap artifacts | Specify whether `test-strategy` step should receive an additional input (`config.spec_file` or `config.tdd_file`) and what extraction-level content `build_test_strategy_prompt()` should reference |
| I-5 | Is the hypothesis that ANTI_INSTINCT_GATE performs better on TDD input (more backtick identifiers → higher fingerprint coverage; richer architecture sections → more integration contracts) empirically correct? | If false, TDD inputs may fail ANTI_INSTINCT_GATE more often than expected, blocking the pipeline at a non-obvious point | Run `check_fingerprint_coverage()` and `extract_integration_contracts()` on a sample TDD file and on a comparable spec file; compare total fingerprints, found/missing ratios, and contract counts |
| I-6 | The `fidelity_checker.py` TypeScript blind spot (Python-only evidence scan via AST) is documented in 03-pure-python-modules.md but not cross-referenced in 06-tdd-template-structure.md — does this mean TDD §7 Data Models and §10 Component Inventory will silently produce near-zero FR coverage evidence? | If yes, `fidelity_checker.py` will undercount TDD-derived FRs when implementation is in TypeScript, producing false-negative findings | Explicitly document in the implementation plan that `fidelity_checker.py` Python-only scope is a known limitation for TypeScript-heavy TDD targets; mark as out-of-scope for the initial TDD integration pass or add to future work |

### Minor Questions

| # | Question | Impact | Suggested Resolution |
|---|----------|--------|----------------------|
| M-1 | What is the full `SpecStructuralAudit` dataclass field structure? | Low — can be inferred from `check_extraction_adequacy()` behavior; warning-only audit does not block pipeline | Read `spec_structural_audit.py` dataclass definition if implementation of TDD-aware structural thresholds is planned |
| M-2 | Does `_get_all_step_ids()` enumerate a step list consistent with `_build_steps()`? The docstring says "9-step pipeline" but runtime builds 11+ entries. | Low — pipeline behavior is verified; docstring inconsistency only; no runtime impact | Update docstrings in `executor.py` to reflect actual step count; no logic change required |

### Pre-Existing Codebase Bug (Not a Research Gap)

| # | Issue | Severity | Evidence | Recommended Action |
|---|-------|----------|----------|--------------------|
| B-1 | DEVIATION_ANALYSIS_GATE field name mismatch: required frontmatter field is `ambiguous_count` (gates.py field list) but semantic check `_no_ambiguous_deviations` reads `ambiguous_deviations` — the gate may silently pass when `ambiguous_count` is present but `ambiguous_deviations` is absent or zero | Medium — pre-existing bug; may mask ambiguous deviations in current pipeline runs regardless of TDD | Confirmed independently by rf-qa spot-check against `gates.py`; documented in both 04-gate-compatibility.md and gaps-and-questions.md | Fix the field name mismatch in `gates.py` as a standalone bug fix before or alongside TDD integration work |

---

## §10 Evidence Trail

This section records all research, synthesis, and QA artifacts produced during the CLI TDD Integration investigation, enabling reproducibility and audit traceability.

---

### Codebase Research

All six files were produced by dedicated research agents performing direct code inspection. No web research was performed.

| File | Topic | Agent Type | Key Finding |
|------|-------|-----------|------------|
| `.dev/tasks/to-do/TASK-RESEARCH-20260325-001/research/01-executor-data-flow.md` | Pipeline step wiring — which steps receive `spec_file` as a direct input and how `_run_anti_instinct_audit` calls pure-Python modules | Code Tracer | Only three steps receive `spec_file` directly (`extract`, `anti-instinct`, `spec-fidelity`). `wiring-verification` receives only a filename string in the prompt, not file content. `build_extract_prompt()` is the single chokepoint because all downstream generate steps receive only extraction output. |
| `.dev/tasks/to-do/TASK-RESEARCH-20260325-001/research/02-prompt-language-audit.md` | Spec-specific language in all 9 prompt builders in `prompts.py` | Code Tracer | `build_extract_prompt()` is CRITICAL — it hardcodes 8 spec-centric FR/NFR sections and misses 8+ major TDD content areas. `build_spec_fidelity_prompt()` is HIGH severity. Five other builders are LOW or require no changes. |
| `.dev/tasks/to-do/TASK-RESEARCH-20260325-001/research/03-pure-python-modules.md` | TDD compatibility of `spec_parser.py`, `fidelity_checker.py`, `integration_contracts.py`, `fingerprint.py`, `obligation_scanner.py` | Code Tracer + Integration Mapper | `integration_contracts.py`, `fingerprint.py`, and `obligation_scanner.py` are mostly TDD-compatible. `spec_parser.py` is partially compatible (generic parsing works but no TypeScript semantic extraction). `fidelity_checker.py` is the highest-risk module — its Python-only AST evidence scan is a fundamental limitation for TypeScript-heavy TDD targets. |
| `.dev/tasks/to-do/TASK-RESEARCH-20260325-001/research/04-gate-compatibility.md` | TDD compatibility of all 15 pipeline gates across `roadmap/gates.py`, `pipeline/gates.py`, and `tasklist/gates.py` | Architecture Analyst | Gates split into three classes: 5 already TDD-compatible (DIFF, DEBATE, SCORE, WIRING, REMEDIATE), 9 conditionally compatible pending `spec_source` aliasing and naming generalization, and 1 structurally incompatible (DEVIATION_ANALYSIS_GATE — requires schema redesign). Pre-existing `ambiguous_count`/`ambiguous_deviations` field mismatch confirmed. |
| `.dev/tasks/to-do/TASK-RESEARCH-20260325-001/research/05-cli-entry-points.md` | CLI command parameters, `RoadmapConfig`/`TasklistValidateConfig` dataclass fields, and extension patterns | Integration Mapper | No `--input-type` flag exists. The project uses additive defaulted dataclass fields as its backward-compatible extension pattern (confirmed by `convergence_enabled`, `allow_regeneration`). Adding `input_type: Literal["spec", "tdd"] = "spec"` and `tdd_file: Path | None = None` to `RoadmapConfig` is sufficient to propagate new config through all executor call sites. |
| `.dev/tasks/to-do/TASK-RESEARCH-20260325-001/research/06-tdd-template-structure.md` | Section-by-section capture analysis of all 28 TDD template sections against current `build_extract_prompt()` output | Doc Analyst | 5 CAPTURED / 15 PARTIAL / 8 MISSED. The 8 missed sections are §7 Data Models (TypeScript interfaces), §8 API Specifications (endpoint tables), §9 State Management, §10 Component Inventory, §15 Testing Strategy, §25 Operational Readiness, §26 Cost Estimation, §28 Glossary. TDD frontmatter `type: "📐 Technical Design Document"` provides a reliable auto-detection discriminator if the executor reads it. |

---

### Web Research

N/A — no web research was performed during this investigation. All findings are based on direct codebase inspection of files in `src/superclaude/cli/roadmap/`, `src/superclaude/cli/pipeline/`, `src/superclaude/cli/tasklist/`, and `src/superclaude/examples/`.

---

### Synthesis Files

| File | Report Sections |
|------|----------------|
| `.dev/tasks/to-do/TASK-RESEARCH-20260325-001/synthesis/synth-01-problem-current-state.md` | §1 Introduction · §2 Problem Statement · §3 Current State |
| `.dev/tasks/to-do/TASK-RESEARCH-20260325-001/synthesis/synth-02-target-gaps.md` | §4 Target State · §5 Gap Analysis |
| `.dev/tasks/to-do/TASK-RESEARCH-20260325-001/synthesis/synth-03-external-findings.md` | §6 External Findings (analogous CLI framework patterns, TDD-to-pipeline integration precedents) |
| `.dev/tasks/to-do/TASK-RESEARCH-20260325-001/synthesis/synth-04-options-recommendation.md` | §7 Options Analysis · §8 Recommendation |
| `.dev/tasks/to-do/TASK-RESEARCH-20260325-001/synthesis/synth-05-implementation-plan.md` | §9 Implementation Plan (step-by-step changes with priority tiers) |
| `.dev/tasks/to-do/TASK-RESEARCH-20260325-001/synthesis/synth-06-questions-evidence.md` | §9 Open Questions · §10 Evidence Trail *(this file)* |

---

### Gaps Log

- `.dev/tasks/to-do/TASK-RESEARCH-20260325-001/gaps-and-questions.md`

Compiled from Phase 3 analyst completeness review and Phase 4 QA research gate report. Contains 2 Critical gaps, 6 Important gaps, 3 Minor gaps, and 1 confirmed pre-existing codebase bug.

---

### QA Reports

| File | Type | Verdict |
|------|------|---------|
| `.dev/tasks/to-do/TASK-RESEARCH-20260325-001/qa/analyst-completeness-report.md` | Phase 3 — Research Completeness Verification (analyst) | CONDITIONAL PASS — 2 critical gaps (`semantic_layer.py`, `structural_checkers.py` uninvestigated) require targeted gap-fill before implementation plan is finalized; all other synthesis sections cleared to proceed |
| `.dev/tasks/to-do/TASK-RESEARCH-20260325-001/qa/qa-research-gate-report.md` | Phase 4 — Research Gate QA (independent spot-check) | PASS — all 10 checklist items pass; 12 code claims independently verified; no contradictions across 6 research files; synthesis cleared to proceed |

---

