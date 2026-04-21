# v3.xx: PRD+TDD Integration into Roadmap & Tasklist Pipeline

---

## User Story

**As a** developer using the SuperClaude roadmap/tasklist pipeline,
**I want** the pipeline to produce output proportional to the richness of TDD+PRD input,
**So that** richer structured input (TDD+PRD) generates more detailed, higher-coverage roadmaps and tasklists instead of regressing compared to a simple spec.

---

## Problem Statement

### What is broken or missing

The roadmap/tasklist pipeline regresses when given richer input. A 312-line spec produces 87 tasklist tasks, but a 1,282-line TDD+PRD (4x richer) produces only 44 tasks u2014 a 0.5:1 output ratio where it should be significantly higher. The pipeline compresses structured documents through a lossy extraction step, generates output in a single LLM response without templates, and validates against its own compressed summary rather than the original input. The result is that the most detailed input produces the least detailed output.

### Pipeline stage affected

```
spec/prd/tdd  -->  extraction  -->  roadmap generation  -->  tasklist  -->  sprint run
                   ^^^^^^^^^^      ^^^^^^^^^^^^^^^^^^^      ^^^^^^^^
                   Lossy compress   One-shot, no template   PRD suppressed
```

Three stages are affected: extraction destroys granularity, roadmap generation lacks output structure, and tasklist generation suppresses PRD content.

### Evidence

| Observation | Data / Source |
|-------------|---------------|
| 4.1x richer input produces 49% fewer tasks | TDD+PRD (1,282 lines) u2192 44 tasks vs Spec (312 lines) u2192 87 tasks u2014 test fixture runs 2026-04-03 |
| Extraction compresses ~1,282 lines into ~50 entities | Extraction step always runs first, summarizing TDD into prose regardless of input richness |
| Large outputs truncate silently | TDD extraction produced 10/14 sections before cutting off u2014 one-shot `claude --print` architecture |
| Output format varies wildly between runs | Spec input u2192 table-based roadmap; TDD input u2192 prose narrative u2014 no output template enforced |
| Validation never reads the original input | `validate_executor.py` checks roadmap against extraction (the lossy intermediary), not against the TDD/PRD source |
| PRD content stripped from tasklist input | `tasklist/prompts.py:221-223` actively removes PRD content before tasklist validation |

---

## What Changes

### Pipeline modifications

| Stage | Change | How it improves the flow |
|-------|--------|-------------------------|
| Extraction | Converts from full content transformation to thin metadata-only pass (type detection, complexity score, section inventory, entity count) | LLM works directly from source document at full granularity instead of a compressed summary |
| Roadmap Generation | Adds output templates (skeleton with section headers, table schemas, frontmatter) and switches from one-shot stdout to incremental section-by-section writing via Write/Edit tools | Each section gets full LLM attention; format is enforced by template; self-correction is possible between sections |
| Roadmap Generation | Adds task table schema, granularity floor, and ID preservation to prompts | Prevents the LLM from collapsing "8 API endpoints" into a single row; output scales proportionally to input |
| Tasklist Generation | Removes PRD suppression bug; adds anti-consolidation guards and output templates | Tasklist receives and uses all available input; format is template-driven, not inference-driven |
| Validation | Adds original input files (TDD/PRD/spec) to validation scope; adds coverage and proportionality dimensions | Validation answers "does the roadmap cover the input?" not just "is the roadmap internally consistent?" |
| Gates | Updates EXTRACT, GENERATE, MERGE gates to accept new formats; adds sentinel validation and minimum task row checks | Gates enforce the new quality bar instead of passing vacuously |

### Key architectural decisions

- Switch from one-shot LLM output to incremental tool-use file writing (the Sprint pattern already does this)
- Extraction becomes metadata-only u2014 the generate step receives the full original document, not a summary
- Output templates define the contract; the LLM populates, not invents the format
- Validation must compare output against original input, not just against itself

---

## Milestones & Phases

| Phase | Description | Expected Outcome | Done when |
|-------|-------------|-------------------|----------|
| Phase 1: Prompt Fixes | Fix PRD suppression, add task table schema to generate prompt, add ID preservation to merge prompt, add granularity floor, tighten SKILL.md merge directives | Immediate improvement in task row counts without architectural changes | Re-run TDD+PRD test fixture; task count rises above 70 (from current 44). Decision gate: if still below 70, proceed to Phase 2 |
| Phase 2: Output Templates | Create roadmap output template, tasklist index template, and tasklist phase template using PART 1/PART 2 pattern with `{{SC_PLACEHOLDER}}` sentinels | Output format is defined by template, not LLM invention; enables automated completeness validation via `grep -c` | Templates exist in `src/superclaude/examples/`; manual review confirms schema covers all required sections and columns |
| Phase 3: Incremental Writing | Add `tool_write_mode` to ClaudeProcess, update all 10 prompt builders to instruct section-by-section writing via Write/Edit tools, add template loading utility | Pipeline writes output incrementally (section by section) instead of one-shot; each section gets full LLM attention | TDD+PRD pipeline run produces a roadmap written via tool-use; output matches template structure; no silent truncation |
| Phase 4: Metadata-Only Extraction | Replace content-transformation extraction with thin metadata pass (type, complexity, domain, section inventory, entity count estimate) | Generate step receives full original document + metadata stub; no more lossy compression of input | TDD+PRD pipeline run: extraction output is <50 lines of metadata; generate step references original TDD directly |
| Phase 5: Gate Updates | Update EXTRACT, GENERATE, MERGE gates for new formats; add sentinel validation and minimum row count checks | Gates enforce new quality bar; prevent regressions | All gates pass on both spec-only and TDD+PRD test fixtures; sentinel completeness check catches incomplete templates |
| Phase 6: Validation Overhaul | Add original input to validation scope; add coverage and proportionality dimensions to reflect prompt | Validation answers "does the roadmap cover the input?" and "is output proportional to input detail?" | `superclaude roadmap validate` on TDD+PRD output: coverage report shows which input requirements have roadmap tasks and flags gaps |
| Phase 7: Testing & Regression | Unit tests for templates/bypass/gates/prompts; integration tests for spec-only, TDD-only, TDD+PRD; regression against spec baseline | Full test coverage for new architecture; spec path continues working as before | `make test` passes; both test fixture paths (spec baseline and TDD+PRD) produce expected task counts; spec baseline not regressed |

---

## Dependencies & Risks

| Item | Type | Detail |
|------|------|--------|
| Pre-existing repo issues (69 findings) | Context | 11 CRITICAL, 30 IMPORTANT, 27 MINOR findings exist independently of this work. 6 findings directly overlap with this release's scope (C-01, C-02, C-29, C-37, C-80/81, C-108). Those 6 get addressed as part of this release; the rest are deferred. |
| Sprint pipeline issues (Workstream B) | Parallel work | Sprint prompt enrichment and output collision fixes are a separate but related workstream. Can be developed in parallel. Not a blocker for this release. |
| One-shot architecture risk | Risk | Switching to incremental writing changes a core pipeline pattern. Mitigation: the subprocess already has `--tools default` and `--dangerously-skip-permissions` flags u2014 only prompt changes needed, not flag changes. Sprint already uses this pattern. |
| LLM output variability | Risk | Even with templates, LLM may produce inconsistent results. Mitigation: sentinel validation (`{{SC_PLACEHOLDER}}` completeness check) and gate enforcement catch incomplete output. |
| Phase 1 may be sufficient | Opportunity | If prompt fixes alone raise task count above target, Phases 2-4 can be deprioritized. Decision gate after Phase 1 determines whether to proceed. |

---

## Research & Artifacts

| Artifact | Location | Summary |
|----------|----------|---------|
| Handover document | `.dev/releases/backlog/v3.xx-prd-tdd-integration-into-roadmap-and-tasklist/HANDOVER-roadmap-tasklist-architecture.md` | Full architecture analysis: 12-step pipeline trace, prompt granularity impact, 7-phase remediation plan, 69 pre-existing findings |
| Roadmap/Tasklist research report | `.dev/tasks/to-do/TASK-RESEARCH-20260404-roadmap-tasklist-overhaul/RESEARCH-REPORT-roadmap-tasklist-overhaul.md` | 863-line deep research: 8 codebase + 2 web research files, 6 synthesis files, 11 QA reports |
| Sprint task execution research | `.dev/tasks/to-do/TASK-RESEARCH-20260403-sprint-task-exec/RESEARCH-REPORT-sprint-task-execution.md` | 10 confirmed gaps (3 CRITICAL, 4 HIGH, 3 MEDIUM) + ~1,262 lines of dead code inventory |
| Tasklist quality investigation | `.dev/tasks/to-do/TASK-RESEARCH-20260403-tasklist-quality/RESEARCH-REPORT-tasklist-quality.md` | First investigation into pipeline granularity loss and R-item collapse |
| Test fixtures (TDD+PRD baseline) | `.dev/test-fixtures/results/test-fix-tdd-prd/` | Most recent pipeline run: 60 roadmap rows, 44 tasklist tasks from 1,282-line input |
| Test fixtures (Spec baseline) | `.dev/test-fixtures/results/test3-spec-baseline/` | Comparison baseline: ~140 roadmap rows, 87 tasklist tasks from 312-line input |
| Pre-existing findings (69 issues) | `.dev/tasks/to-do/TASK-E2E-20260327-prd-pipeline-e2e/reviews/pre-existing-findings.md` | Adversarial QA pass: 11 CRITICAL, 30 IMPORTANT, 27 MINOR u2014 deferred, 6 overlap with this release |

---

## Definition of Done

- [ ] TDD+PRD test fixture produces >= 80 tasklist tasks (from current 44), closing the gap with spec baseline (87)
- [ ] Spec-only test fixture continues to produce >= 80 tasklist tasks (no regression from current 87)
- [ ] Roadmap output matches defined template structure (sentinel completeness check passes)
- [ ] Validation reports coverage against original input document (not just extraction)
- [ ] `make test` passes with new unit and integration tests for templates, gates, and prompts
- [ ] Both pipeline paths (spec-only and TDD+PRD) run to completion without silent truncation

---

## Next Release

**v3.7: Task Unified v2 u2014 Pipeline Reliability & Sprint TUI**

Split into two sub-releases after adversarial analysis: **v3.7a** (Pipeline Reliability & Naming u2014 checkpoint enforcement, canonical `/sc:task` naming, data contracts) and **v3.7b** (Sprint TUI v2 u2014 real-time telemetry, tmux integration, retrospective synthesis). v3.7a establishes the infrastructure layer that v3.7b consumes. This release (v3.xx) improves the quality of what the pipeline *produces*; v3.7 improves the reliability of how it *executes*. Path: `.dev/releases/backlog/v3.7-task-unified-v2/`

---

*Generated from template v1.0 | Source: `.dev/releases/templates/CLICKUP-RELEASE-TASK-TEMPLATE.md`*
