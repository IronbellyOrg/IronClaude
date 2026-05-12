# Gaps and Questions Log

**Date compiled:** 2026-03-25
**Source:** Phase 3 analyst completeness report + QA research gate report
**QA Verdict:** PASS — synthesis may proceed

---

## Critical Gaps (affect Implementation Plan accuracy)

| # | Gap | Severity | Files Affected | Remediation |
|---|---|---|---|---|
| C-1 | `semantic_layer.py` (~400 lines) not investigated — unclear if it reads spec content in the active pipeline | Critical | 01-executor-data-flow.md, synthesis/synth-05-implementation-plan.md | Synthesis agents must treat semantic_layer.py as Unknown; flag as Open Question in §9 |
| C-2 | `structural_checkers.py` (~200 lines) not investigated — relationship to spec_structural_audit.py unknown | Critical | 01-executor-data-flow.md | Same — treat as Unknown in implementation plan |

---

## Important Gaps (affect synthesis quality)

| # | Gap | Severity | Evidence Location | Synthesis Handling |
|---|---|---|---|---|
| I-1 | `run_wiring_analysis(wiring_config, source_dir)` in executor.py:421-433 — does wiring_config reference spec_file? Not verified | Important | 01-executor-data-flow.md Gaps section | Note as open question in §9; exclude from definitive step count |
| I-2 | Downstream extraction frontmatter consumers not enumerated — which code reads `spec_source` or `functional_requirements` from extraction output? | Important | 02-prompt-language-audit.md Gaps section | Note in §4 Gap Analysis; add to §9 Open Questions |
| I-3 | `spec_source` rename strategy unresolved — alias both fields, rename only new outputs, or keep backward compat? | Important | 04-gate-compatibility.md | Options analysis must include renaming strategy; mark as open question |
| I-4 | `build_test_strategy_prompt()` TDD enrichment path not concretely specified | Important | 02-prompt-language-audit.md | Include in implementation plan with Medium priority |
| I-5 | ANTI_INSTINCT_GATE TDD performance is a hypothesis (more identifiers → better coverage) — not empirically verified | Important | 03-pure-python-modules.md, 04-gate-compatibility.md | Present as hypothesis with evidence rationale; flag in §9 |
| I-6 | `fidelity_checker.py` TypeScript blind spot not documented in §06-tdd-template-structure.md cross-reference | Important | 03-pure-python-modules.md vs. 06-tdd-template-structure.md | Synthesis agents should cross-reference explicitly |

---

## Minor Gaps

| # | Gap | Notes |
|---|---|---|
| M-1 | `SpecStructuralAudit` dataclass structure not documented | Can be inferred from check_extraction_adequacy behavior |
| M-2 | `_get_all_step_ids()` full step list not verified against _build_steps() | Docstring inconsistency only; pipeline behavior verified |
| M-3 | DEVIATION_ANALYSIS_GATE `ambiguous_count` vs. `ambiguous_deviations` field mismatch — pre-existing codebase bug | Confirmed independently by QA agent; note in §9 Open Questions |

---

## Pre-Existing Codebase Bug (not a gap in research)

DEVIATION_ANALYSIS_GATE:
- Required frontmatter field: `ambiguous_count`
- Semantic check `_no_ambiguous_deviations` reads: `ambiguous_deviations`
- Field name mismatch — a gate requiring `ambiguous_count` in frontmatter, while the semantic check reads `ambiguous_deviations`, may silently pass if `ambiguous_count` is present but `ambiguous_deviations` is 0 or absent
- Confirmed independently by rf-qa spot-check against gates.py

---

## Synthesis Guidance

**What synthesis CAN assert with high confidence (code-verified):**
- The 3 steps that receive spec_file directly: extract, anti-instinct, spec-fidelity
- `build_extract_prompt()` is the single chokepoint — all 8 missed TDD sections
- `spec_source` appears in 5 gates and 2+ prompt builders — aliasing strategy is the primary gate fix
- `RoadmapConfig` extension pattern: additive defaulted fields (confirmed by convergence_enabled, allow_regeneration)
- DEVIATION_ANALYSIS_GATE is the only structurally incompatible gate
- 5 CAPTURED / 15 PARTIAL / 8 MISSED TDD sections

**What synthesis MUST flag as Open Questions:**
- semantic_layer.py and structural_checkers.py involvement in spec processing
- run_wiring_analysis wiring_config spec reference
- ANTI_INSTINCT_GATE TDD performance (hypothesis, not measured)
- spec_source renaming backward-compatibility strategy
