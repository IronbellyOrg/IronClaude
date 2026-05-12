# Research 04: MDTM Template 02 Patterns and Prior Report Conventions

**Date:** 2026-04-02
**Source:** `.claude/templates/workflow/02_mdtm_template_complex_task.md`, prior E2E summary reports
**Purpose:** Document template requirements and comparison table patterns for the quality-comparison task builder

---

## 1. MDTM Template 02 — Required Sections (PART 2 Structure)

The template divides into PART 1 (orchestrator instructions, omitted from output) and PART 2 (the actual task file). The task file produced from Template 02 must include:

### Frontmatter (YAML)
- `id`, `title`, `description`, `status`, `type`, `priority`, `created_date`, `updated_date`, `assigned_to`
- `autogen`, `autogen_method`, `coordinator`, `parent_task`, `depends_on` (array), `related_docs` (array of {path, description})
- `tags` (array), `template_schema_doc`, `estimation`, `sprint`, `due_date`, `start_date`, `completion_date`
- `blocker_reason`, `ai_model`, `model_settings`, `review_info` (nested), `task_type` ("static" or "dynamic")

### Body Sections (in order)
1. `# [Task Title]`
2. `## Task Overview` — comprehensive description
3. `## Key Objectives` — numbered list of concrete outcomes
4. `## Prerequisites & Dependencies` — parent task, blocking deps, previous stage outputs, handoff file convention, frontmatter update protocol
5. `## Detailed Task Instructions` — phases with checklist items
   - `### Phase 1: Preparation and Setup` — status update, context loading
   - `### Phase 2+: [Execution Phases]` — the core work
   - Phase-gate QA checkpoints between phases (M1 pattern)
   - `## Post-Completion Actions` — validation + frontmatter update
6. `## Task Log / Notes` — with per-phase findings subsections and execution log

### Handoff File Convention
Complex tasks write intermediate outputs to `.dev/tasks/TASK-NAME/phase-outputs/` with subdirectories:
- `discovery/` — scan results, inventories
- `test-results/` — test output and summaries
- `reviews/` — quality review verdicts
- `plans/` — fix plans, conditional action outputs
- `reports/` — aggregated reports and summaries

---

## 2. Checklist Item Format (Section B — Critical)

Every checklist item must be a **single self-contained paragraph** containing all 6 elements:

1. **Context Reference + WHY** — what file(s) to read and why
2. **Action + WHY** — what to do with that context
3. **Output Specification** — exact file name, location, content requirements, template
4. **Integrated Verification** — "ensuring..." clause (100% accuracy, no fabrication)
5. **Evidence on Failure Only** — log to task notes ONLY if blocked
6. **Completion Gate** — "Once done, mark this item as complete."

**Forbidden patterns:**
- Standalone "read context" items that produce no output
- Separate verification/confirmation items
- Multi-line/bulleted checklist items
- Parent checkboxes before child items

---

## 3. Intra-Task Handoff Patterns (Section L — Template 02 Specific)

Template 02 extends Template 01 with these handoff patterns for complex inter-item dependencies:

| Pattern | Code | When | Output Location |
|---------|------|------|-----------------|
| Discovery | L1 | Explore codebase/data, produce structured findings | `phase-outputs/discovery/` |
| Build-from-Discovery | L2 | Create output using discovery findings | Deliverable location |
| Test/Execute | L3 | Run commands, capture raw output + structured summary | `phase-outputs/test-results/` |
| Review/QA | L4 | Assess quality, produce PASS/FAIL verdict with findings | `phase-outputs/reviews/` |
| Conditional-Action | L5 | Branch based on previous results (must handle BOTH branches) | `phase-outputs/plans/` |
| Aggregation | L6 | Consolidate multiple outputs into single report | `phase-outputs/reports/` |

**Common phase structures:**
- Discovery -> Build -> Review: L1 -> L2 -> L4 -> L6
- Build -> Test -> Fix: K1/K2 -> L3 -> L5
- Full Lifecycle with QA Gates: L1 -> L2 -> **M1 QA Gate** -> L3 -> L5 -> L4 -> L6 -> **M1 QA Gate**

**For this quality-comparison task**, the relevant patterns are:
- **L1 (Discovery)** for Phase 1 prerequisite verification (scan result directories)
- **L3 (Test/Execute)** for Phase 2 quantitative data collection (grep counts, wc -l, YAML reads)
- **L4 (Review/QA)** for Phase 3 qualitative assessment
- **L6 (Aggregation)** for Phase 4 cross-pipeline matrix and Phase 5 final report

---

## 4. Phase-Gate QA Requirements (Sections I15-I16, M1)

Tasks with 2+ execution phases require phase-gate QA checkpoints:
- **Aggregation item** (L6) collecting phase outputs
- **QA agent spawn** (rf-qa structural, optionally rf-qa-qualitative)
- **Conditional proceed** (L5) — PASS continues, FAIL triggers fix cycle

Fix cycle limits per gate type:

| Gate Type | Max Fix Cycles | After Max |
|-----------|---------------|-----------|
| research-gate | 3 | HALT and escalate |
| synthesis-gate | 2 | Unresolved -> Open Questions |
| report-validation | 3 | HALT and escalate |
| task-integrity | 2 | Unresolved -> Open Questions |
| Any qualitative gate | 3 | HALT and escalate |

---

## 5. Prior Comparison Report Patterns

### Pattern A: Pass/Fail Verification Table (test1-tdd-prd-v2-summary.md)

```
| Item | Check | Result |
|------|-------|--------|
| 3.2 Extraction frontmatter | 20 fields (14 standard + 6 TDD), data_models=2, api_surfaces=6 | **PASS** |
| 3.7 Anti-instinct | fingerprint_coverage=0.73, undischarged=1, uncovered=4 — gate FAIL (expected) | **FAIL** |
| 3.8 Test strategy | Skipped (pipeline halted at anti-instinct) | **SKIPPED** |
```

Key characteristics:
- Item column uses phase-prefixed numbering (3.2, 3.3, etc.)
- Check column includes actual measured values inline
- Result column is bolded PASS/FAIL/SKIPPED
- Aggregate score at bottom: "PASS: 9/11, FAIL: 1, SKIPPED: 2"

### Pattern B: Cross-Run Comparison Table (test2-spec-prd-v2-summary.md)

```
| Aspect | Phase 3 (TDD+PRD) | Phase 4 (Spec+PRD) |
|--------|-------------------|-------------------|
| input_type | tdd | spec |
| TDD frontmatter fields | 6 present | 0 present (correct) |
| Extraction sections | 14 | 8 |
| Roadmap lines | 746 | 558 |
| Anti-instinct result | FAIL (1 undischarged) | FAIL (2 undischarged) |
| PRD enrichment | 31 refs in roadmap | 83 refs in roadmap |
```

Key characteristics:
- Aspect column names the metric
- One column per pipeline run, with raw values
- Parenthetical annotations for context ("correct", "expected behavior")
- No normalization or scoring — raw values side by side

### Pattern C: Enrichment Measurement Table (test2-spec-prd-v2-summary.md)

```
| Artifact | persona | GDPR | SOC2 | PRD | Named Personas |
|----------|---------|------|------|-----|----------------|
| extraction.md | 7 | 6 | 6 | 34 | Alex:5, Jordan:2, Sam:3 |
| roadmap.md | 14 | 10 | 11 | 26 | Alex:8, Jordan:4, Sam:10 |
```

Key characteristics:
- Rows are artifacts (pipeline stages)
- Columns are enrichment categories
- Values are grep counts
- Named persona breakdown in final column

### Pattern D: Leak/Contamination Check Table

```
| Check | Expected | Actual | Verdict |
|-------|----------|--------|---------|
| TDD frontmatter fields (6) | ABSENT | 0 found | CLEAN |
| tdd_file in state | null | null | CLEAN |
```

Key characteristics:
- Expected vs actual comparison
- Verdict column (CLEAN/CONTAMINATED)
- Binary pass/fail framing

---

## 6. QA Focus Guidance from Build Request

**QA gates MUST focus on metric accuracy against actual files, NOT report prose quality.**

### What QA Should Verify
- Do metric values in comparison tables match actual files they claim to measure?
- Are grep counts accurate against actual artifact files?
- Does the verdict follow logically from collected data?
- Are any claims made without supporting evidence?

### What QA Should NOT Verify
- Whether prose summaries are well-written
- Whether section cross-references are correct
- Formatting consistency

**Implication for task design:** QA checklist items should instruct the rf-qa agent to spot-check specific metric values by re-running grep/wc commands against source artifacts, NOT to review report prose. The QA gate type should be `report-validation` (max 3 fix cycles) since the primary deliverable is a comparison report.

---

## 7. Recommendations for Task Builder

### Template Selection
- Use Template 02 (complex) — confirmed by build request ("02 complex — 8-dimensional analysis")
- `task_type: static` — all dimensions and runs are pre-known; no dynamic discovery needed

### Phase Structure Mapping
| Build Request Phase | Template Pattern | Gate |
|--------------------|-----------------|------|
| Phase 1: Prerequisite Verification | L1 Discovery (scan dirs) | None (setup) |
| Phase 2: Quantitative Data Collection | L3 Test/Execute (grep/wc/read) | research-gate after Phase 2 |
| Phase 3: Qualitative Assessment | L4 Review/QA (read + assess) | synthesis-gate after Phase 3 |
| Phase 4: Cross-Pipeline Matrix | L6 Aggregation | None (feeds into Phase 5) |
| Phase 5: Verdict and Report | L6 Aggregation (final) | report-validation before Post-Completion |

### Comparison Table Format
Adopt **Pattern B** (cross-run comparison) as the primary format for dimension data files:
- One column per run (Baseline / Spec+PRD / TDD+PRD)
- Raw metric values, not scores
- Parenthetical annotations for context

Adopt **Pattern C** (enrichment measurement) for Dimension 8 cross-stage enrichment flow.

### Output File Structure
8 dimension data files in `phase-outputs/data/` + 2 reports in `phase-outputs/reports/` + 1 final report in `.dev/test-fixtures/results/` — matches build request artifact table exactly.

---

## 8. Key Constraints for Checklist Item Authoring

1. Each Phase 2 dimension item must be ONE self-contained paragraph that: reads the relevant artifacts from all 3 runs, runs the specified grep/wc/YAML-read commands, writes the comparison table to the correct `phase-outputs/data/dimN-*.md` file, and includes an "ensuring..." clause requiring metric values to match actual file contents.

2. Phase 3 qualitative items must read actual roadmap/tasklist content and quote specific examples — no vague assessments.

3. Phase 4-5 aggregation items must use Glob to discover all `phase-outputs/data/dim*.md` files rather than hardcoding the list.

4. QA gate items must instruct rf-qa to re-run specific grep commands against source artifacts to verify reported counts, per the QA Focus Guidance.

5. Handle missing artifacts gracefully: "N/A -- anti-instinct halted" or "N/A -- tasklist not generated" rather than blocking.
