# Adversarial QA Report -- Agent 10 (Semantic & Logical Coherence)

**Date:** 2026-03-28
**Phase:** Adversarial QA Round 5, Agent 10 of 10
**Scope:** Semantic correctness of prompts, logical consistency of design, edge cases in detection scoring, PRD enrichment value assessment, auto-wire soundness, documentation gaps
**Fix Authorization:** REPORT ONLY

---

## Overall Verdict: PASS WITH FINDINGS (3 new issues)

After systematic review of all 8 areas assigned, I found 3 new issues not covered by the prior 92 findings. The majority of the design is sound, and several areas I was asked to investigate turned out to be correct.

---

## Area 1: Semantic Correctness of PRD Supplementary Blocks

### Methodology
Read every PRD supplementary block in `prompts.py` and verified: (a) section references match actual PRD template, (b) instruction text is actionable and unambiguous, (c) severity ratings are appropriate, (d) no duplication with main prompt.

### PRD Section Reference Verification

| Prompt Function | PRD Section Referenced | Actual PRD Template Section | Correct? |
|---|---|---|---|
| `build_extract_prompt` | S19 Success Metrics | ## 19. Success Metrics & Measurement | YES |
| `build_extract_prompt` | S7 User Personas | ## 7. User Personas | YES |
| `build_extract_prompt` | S12 Scope Definition | ## 12. Scope Definition | YES |
| `build_extract_prompt` | S17 Legal & Compliance | ## 17. Legal & Compliance Requirements | YES |
| `build_extract_prompt` | S6 JTBD | ## 6. Jobs To Be Done (JTBD) | YES |
| `build_generate_prompt` | S5 Business Context | ## 5. Business Context | YES |
| `build_generate_prompt` | S19 Success Metrics | ## 19. Success Metrics & Measurement | YES |
| `build_generate_prompt` | S7 User Personas | ## 7. User Personas | YES |
| `build_generate_prompt` | S17 Legal & Compliance | ## 17. Legal & Compliance Requirements | YES |
| `build_generate_prompt` | S12 Scope Definition | ## 12. Scope Definition | YES |
| `build_generate_prompt` | S22 Customer Journey Map | ## 22. Customer Journey Map | YES |
| `build_score_prompt` | S19 Success Metrics | ## 19. Success Metrics & Measurement | YES |
| `build_score_prompt` | S7 User Personas | ## 7. User Personas | YES |
| `build_score_prompt` | S17 Legal & Compliance | ## 17. Legal & Compliance Requirements | YES |
| `build_spec_fidelity_prompt` | S7 User Personas | ## 7. User Personas | YES |
| `build_spec_fidelity_prompt` | S19 Success Metrics | ## 19. Success Metrics & Measurement | YES |
| `build_spec_fidelity_prompt` | S17 Legal & Compliance | ## 17. Legal & Compliance Requirements | YES |
| `build_spec_fidelity_prompt` | S12 Scope Definition | ## 12. Scope Definition | YES |
| `build_test_strategy_prompt` | S7 User Personas | ## 7. User Personas | YES |
| `build_test_strategy_prompt` | S22 Customer Journey Map | ## 22. Customer Journey Map | YES |
| `build_test_strategy_prompt` | S19 Success Metrics | ## 19. Success Metrics & Measurement | YES |
| `build_test_strategy_prompt` | S17 Legal & Compliance | ## 17. Legal & Compliance Requirements | YES |
| `build_test_strategy_prompt` | S23 Error Handling & Edge Cases | ## 23. Error Handling & Edge Cases | YES |

**Result:** All 23 PRD section references are correct.

### Instruction Quality Assessment

All PRD supplementary blocks follow a consistent pattern: numbered list of extraction/enrichment directives, each tied to a specific PRD section, with a clear closing guardrail ("do NOT treat PRD content as hard requirements"). The instructions are actionable and would produce useful LLM output. No contradictions with main prompts detected.

### Severity Ratings

- `build_spec_fidelity_prompt`: Compliance coverage flagged as HIGH severity, persona/metric/scope flagged as MEDIUM. This is appropriate -- missing compliance items have regulatory risk, while missing persona coverage is a quality concern but not a correctness issue.
- No severity rating issues found.

### Duplication Check

The PRD blocks across different pipeline steps address different concerns (extract: surface as requirements; generate: inform phasing; score: add scoring dimensions; fidelity: check coverage; test-strategy: add test categories). No inappropriate duplication found.

**PASS -- No issues in Area 1.**

---

## Area 2: Semantic Correctness of TDD Extraction Prompt

### Methodology
Read all 6 TDD-specific section instructions in `build_extract_prompt_tdd()` and verified against the TDD template structure and the downstream gate expectations.

### TDD Section Reference Verification (in `build_tasklist_generate_prompt` and `build_tasklist_fidelity_prompt`)

| Prompt Function | TDD Section Referenced | Actual TDD Template Section | Correct? |
|---|---|---|---|
| `build_tasklist_fidelity_prompt` | §15 Testing Strategy | ## 15. Testing Strategy | YES |
| `build_tasklist_fidelity_prompt` | §19 Migration & Rollout Plan | ## 19. Migration & Rollout Plan | YES |
| `build_tasklist_fidelity_prompt` | §10 Component Inventory | ## 10. Component Inventory | YES |
| `build_tasklist_generate_prompt` | S15 Testing Strategy | ## 15. Testing Strategy | YES |
| `build_tasklist_generate_prompt` | S8 API Specifications | ## 8. API Specifications | YES |
| `build_tasklist_generate_prompt` | S10 Component Inventory | ## 10. Component Inventory | YES |
| `build_tasklist_generate_prompt` | S19 Migration & Rollout Plan | ## 19. Migration & Rollout Plan | YES |
| `build_tasklist_generate_prompt` | S7 Data Models | ## 7. Data Models | YES |

### Extraction Instruction Clarity

The 6 TDD-specific body sections in `build_extract_prompt_tdd()` are highly specific:
- Data Models: "name, fields, types, constraints, relationships" -- actionable
- API Specifications: "HTTP method, URL path, auth requirements, rate limits..." -- actionable
- Component Inventory: "route/page tables, shared component tables with props/usage/locations" -- actionable
- Testing Strategy: "test pyramid breakdown with coverage levels/tooling/targets/ownership" -- actionable
- Migration and Rollout Plan: "migration phases with tasks/duration/dependencies/rollback" -- actionable
- Operational Readiness: "runbook scenarios with symptoms/diagnosis/resolution/escalation/prevention" -- actionable

Each instruction matches the corresponding frontmatter counter (e.g., `data_models_identified` maps to "Data Models and Interfaces" section).

**PASS -- No issues in Area 2.**

---

## Area 3: `detect_input_type` Scoring -- Hybrid Document Edge Case

### Analysis

The question posed: what about a hybrid document (spec with "Data Models" section + `coordinator` field)?

Score calculation:
- 12 numbered headings: +1 (>=10 threshold)
- `coordinator` field: +2
- "Data Models" section match: +1
- Total: 4 -- below threshold of 5, classified as `spec`

**This is correct behavior.** A spec that happens to discuss data models and has a coordinator is still a spec. The threshold of 5 provides adequate separation:
- A real TDD scores 10+: 20+ headings (3) + parent_doc + coordinator (4) + multiple TDD section names (5+) + type field (2) = 14+
- A spec with some TDD-like content scores at most 4-5, and only if it has `coordinator` AND `parent_doc` (both worth 2 each) would it cross the threshold.

The only theoretical concern: a spec with both `coordinator` AND `parent_doc` fields AND a "Data Models" section would score 1+2+2+1=6 and be misclassified as TDD. However, `parent_doc` is genuinely TDD-exclusive (it references the parent PRD), so a spec having it would be anomalous.

**PASS -- Detection logic is sound for the hybrid case.**

---

## Area 4: PRD Enrichment Value Assessment

### Comparison: test1-tdd-modified vs test1-tdd-prd extractions

| Metric | TDD-only | TDD+PRD | Delta | Assessment |
|---|---|---|---|---|
| functional_requirements | 5 | 5 | 0 | Same FR count -- PRD did not inflate |
| nonfunctional_requirements | 4 | 8 | +4 | PRD added compliance NFRs (GDPR, SOC2, data retention, breach notification) |
| total_requirements | 9 | 13 | +4 | Correct sum |
| dependencies_identified | 6 | 9 | +3 | PRD surfaced additional external deps |
| success_criteria_count | 7 | 10 | +3 | PRD added measurable business criteria |
| components_identified | 4 | 9 | +5 | More components surfaced |
| migration_items_identified | 3 | 15 | +12 | Significant enrichment |
| operational_items_identified | 2 | 12 | +10 | Significant enrichment |
| complexity_score | 0.65 | 0.55 | -0.10 | Slightly lower -- reasonable given more context |

### Qualitative Assessment

The PRD-enriched extraction added:
- **NFR-COMP-001** (GDPR consent at registration) -- sourced from PRD S17, not in TDD. Genuine value-add.
- **NFR-COMP-002** (SOC2 audit logging) -- sourced from PRD S17, not in TDD. Genuine value-add.
- Additional dependencies (Legal counsel, compliance review) -- real project dependencies.
- Richer operational readiness items -- genuine enrichment.

The functional requirements were NOT inflated (still 5), which means the guardrail "do NOT treat PRD content as hard requirements" is working.

**PASS -- PRD enrichment adds genuine value, not noise.**

---

## Area 5: Auto-Wire Design Soundness

### The Concern

When `input_type=tdd` and `tdd_file=null`, the auto-wire would use `spec_file` (the primary TDD input) as the `tdd_file` for downstream validators. But line 862-867 of `executor.py` explicitly prevents this:

```python
# Redundancy guard: when primary input IS a TDD, --tdd-file is redundant
if effective_input_type == "tdd" and config.tdd_file is not None:
    _log.warning(
        "Ignoring --tdd-file: primary input is already a TDD document. ..."
    )
    config = dataclasses.replace(config, tdd_file=None)
```

This guard fires when the user explicitly passes `--tdd-file` alongside a TDD primary input. However, the auto-wire from state (lines 1744-1753) runs during `--resume` and would restore a `tdd_file` value from state. If the state was saved from a prior run where `tdd_file` was set before the redundancy guard cleared it... let me check.

Looking at `_save_state` (line 1440): `"tdd_file": str(config.tdd_file) if config.tdd_file else None` -- this saves the config AFTER the redundancy guard has cleared it to None. So the state file would contain `tdd_file: null` for TDD-primary runs. The auto-wire would then find `null` and skip. **No issue.**

The broader concern about `spec_file` being used as TDD: the auto-wire only wires `tdd_file` and `prd_file` from state, never `spec_file`. The tasklist validator receives `tdd_file` as a supplementary document, not as the primary input. The primary input (spec/TDD) is always `spec_file`. So the validator does use it differently -- it checks roadmap-to-tasklist fidelity and only uses TDD/PRD for supplementary dimension checks.

**PASS -- Auto-wire design is sound. No redundancy or hidden coupling issues.**

---

## Area 6: `build_tasklist_generate_prompt` Quality Assessment

### Design Review

The function is well-structured:
1. Baseline generation prompt is clear and actionable
2. TDD enrichment adds 5 specific extraction directives with TDD section references
3. PRD enrichment adds 5 specific directives with PRD section references
4. Combined interaction note establishes clear precedence (TDD for engineering detail, PRD for product context)

### Issue Found: Ambiguous Section Notation

**FINDING 1 (NEW):**

The `build_tasklist_generate_prompt` uses `S` prefix for TDD section references (S7, S8, S10, S15, S19), while `build_tasklist_fidelity_prompt` uses `§` prefix for TDD sections (§10, §15, §19). Both prompts also reference PRD sections using `S` prefix (S7, S12, S19, S22).

This creates ambiguity: in `build_tasklist_generate_prompt`, the TDD enrichment block says "Data model field definitions from S7" and the PRD enrichment block says "User persona context from S7". When both TDD and PRD are present in the same prompt, the LLM sees **two different `S7` references meaning completely different things** -- TDD S7 = Data Models, PRD S7 = User Personas.

The `build_tasklist_fidelity_prompt` avoids this by using `§` for TDD sections, but `build_tasklist_generate_prompt` does not follow this convention.

---

## Area 7: Overall Design Coherence

### Supplementary File Architecture (--tdd-file, --prd-file)

The design choice to use explicit CLI flags rather than auto-detection is sound:
- Auto-detection of TDD/PRD from directory context would be fragile and error-prone
- Explicit flags make the pipeline reproducible
- The auto-wire from state file provides convenience for `--resume` without sacrificing explicitness

### Auto-Wire from State File

The pattern is reasonable for `--resume` workflows. The state file is written after the redundancy guard, so stale/contradictory values are not persisted. File-existence checks before wiring prevent dangling references.

### Architectural Concern: No Scale Issues Identified

The supplementary file architecture adds at most 2 extra files to each step's input list. The `_EMBED_SIZE_LIMIT` check (120 KB) provides a safety valve. No architectural decisions that would cause problems at scale.

---

## Area 8: Documentation Gaps

### User-Facing Documentation

**FINDING 2 (NEW):**

The `--tdd-file` and `--prd-file` flags have help text in `commands.py`:
- `--tdd-file`: "Path to a TDD file for supplementary technical context enrichment."
- `--prd-file`: "Path to a PRD file for supplementary business context enrichment."

These are functional but minimal. A user encountering these flags would not know:
1. Which pipeline steps are affected by these flags
2. What specific enrichment occurs (additional scoring dimensions in score, compliance checks in fidelity, etc.)
3. That `--tdd-file` is automatically ignored when the primary input is a TDD
4. That these values are persisted to state and auto-wired on `--resume`

The `roadmap_group` docstring (lines 17-28) lists examples but none use `--tdd-file` or `--prd-file`. The `run` command docstring (lines 142-146) mentions TDD auto-detection but not supplementary files.

**FINDING 3 (NEW):**

There is no documentation (README, user guide, or inline) explaining the interaction between `--input-type`, `--tdd-file`, and `--prd-file`. Specifically:
- `--input-type tdd` + `--tdd-file foo.md` silently ignores `--tdd-file` (with a log warning)
- `--input-type spec` + `--prd-file foo.md` adds PRD enrichment to a spec extraction
- `--input-type auto` + `--tdd-file foo.md` + `--prd-file bar.md` could result in either spec+TDD+PRD or TDD+PRD (depending on detection), with different behavior

These interactions are non-obvious and should be documented.

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|---|---|---|---|
| 1 | MINOR | `src/superclaude/cli/tasklist/prompts.py:180-194` | `build_tasklist_generate_prompt` uses `S` prefix for TDD section references (S7, S8, S10, S15, S19) while the same file's `build_tasklist_fidelity_prompt` uses `§` prefix. When both TDD and PRD are present, `S7` is ambiguous (TDD S7 = Data Models, PRD S7 = User Personas). | Change TDD section references in `build_tasklist_generate_prompt` to use `§` notation matching `build_tasklist_fidelity_prompt`: `§7 Data Models`, `§8 API Specifications`, `§10 Component Inventory`, `§15 Testing Strategy`, `§19 Migration & Rollout Plan`. |
| 2 | MINOR | `src/superclaude/cli/roadmap/commands.py:112-122` | `--tdd-file` and `--prd-file` help text is too minimal. Missing: which steps are affected, that `--tdd-file` is ignored for TDD primary input, that values are persisted for `--resume`. No examples in the command group docstring. | Expand help text to mention "enriches extraction, generation, scoring, fidelity, and test-strategy steps" and add at least one example to the `roadmap_group` docstring: `superclaude roadmap run spec.md --prd-file requirements.md`. |
| 3 | MINOR | No file (documentation gap) | No user-facing documentation explains the interaction between `--input-type`, `--tdd-file`, and `--prd-file`, including the silent ignore behavior when primary input is TDD and `--tdd-file` is also provided. | Add a section to the roadmap CLI documentation or the `run` command's docstring explaining the three-way interaction and the redundancy guard behavior. |

---

## Summary

- **Areas investigated:** 8
- **New issues found:** 3 (all MINOR)
- **Critical issues:** 0
- **Important issues:** 0
- **Minor issues:** 3

The core design is sound. PRD section references are all correct across all prompt builders. TDD section references are correct (the section numbers map to the right content). The detection scoring handles edge cases properly. PRD enrichment demonstrably adds value without inflating requirements. The auto-wire design is safe due to the redundancy guard and state-file ordering. The `build_tasklist_generate_prompt` is well-designed and would produce useful output.

The 3 findings are all minor quality improvements: a notation inconsistency that could cause LLM confusion in the combined TDD+PRD case, and two documentation gaps that would help users understand the supplementary file system.

## QA Complete
