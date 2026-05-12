# Research Notes: Option 3 Implementation — TDD Template + Pipeline Upgrades

**Date:** 2026-03-25
**Scenario:** A — explicit request with pre-existing verified research
**Depth Tier:** Deep
**Track Count:** 1
**Status:** Complete

---

## EXISTING_FILES

All files verified by prior research (TASK-RESEARCH-20260324-001, 6 agents, analyst + QA gates passed).

### Files to EDIT (implementation targets)

| File | Purpose | Approx Lines | Phase |
|------|---------|-------------|-------|
| `src/superclaude/examples/tdd_template.md` | TDD template — add 8 pipeline frontmatter fields + sentinel self-check | ~1,309 lines | Phase 1 |
| `.claude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md` | Add 2 domain keyword dictionaries + Steps 9-14 for TDD extraction | ~200+ lines | Phase 2 |
| `.claude/skills/sc-roadmap-protocol/refs/scoring.md` | Add 7-factor TDD scoring formula + TDD-format detection rule | ~100+ lines | Phase 2 |
| `.claude/commands/sc/spec-panel.md` | Add Steps 6a/6b, TDD output mode, template reference | 624 lines | Phase 3 |
| `.claude/skills/sc-tasklist-protocol/SKILL.md` | Implement --spec flag (Step 4.1a, 4.4a, Stage 7 validation) | large | Phase 4 |
| `.claude/skills/tdd/SKILL.md` | Add PRD Extraction Agent Prompt, update synthesis mapping, add rules 12-13, add QA item 13 | ~1,344 lines | Phase 5 |

### Pre-existing research (reuse, do NOT re-research)

All research files from TASK-RESEARCH-20260324-001 are the evidence base:
- `research/01-spec-panel-audit.md` — spec-panel full behavior audit
- `research/02-roadmap-pipeline-audit.md` — extraction pipeline + scoring formula + template selection
- `research/03-tasklist-audit.md` — tasklist input contract + task generation algorithm
- `research/04-tdd-template-audit.md` — TDD + spec template frontmatter comparison
- `research/05-prd-tdd-skills-audit.md` — PRD/TDD skills + handoff gaps
- `research/06-analysis-doc-verification.md` — 5 CODE-CONTRADICTED corrections

### Implementation plan source

Section 8 of `RESEARCH-REPORT-prd-tdd-spec-pipeline.md` (lines 639-931) contains the verified, QA-validated implementation plan with exact file paths, field names, insertion points, and a 16-item integration checklist.

---

## PATTERNS_AND_CONVENTIONS

From prior research:
- YAML frontmatter in TDD template uses `---` delimiters (not `+++`)
- Section headings follow `## N. Title` pattern
- Skill SKILL.md files use markdown with embedded code blocks for agent prompts
- sc:roadmap refs/ files use markdown tables for data structures
- Domain keyword dictionaries use comma-separated quoted strings
- Scoring formula uses `| Factor | Raw | Norm | Weight |` table format
- `make sync-dev` propagates src/superclaude/ changes to .claude/

---

## GAPS_AND_QUESTIONS

No gaps — the implementation plan is fully specified with exact insertion points from verified research. The 13 open questions from Section 9 are documented but none block implementation.

---

## RECOMMENDED_OUTPUTS

No additional research needed. The task builder should consume the implementation plan directly from Section 8 of the research report.

Research files: 0 new (reuse existing TASK-RESEARCH-20260324-001 corpus)
Output: 1 MDTM task file at `${TASK_DIR}TASK-RF-20260325-001.md`

---

## SUGGESTED_PHASES

The task file should encode 5 implementation phases matching Section 8 of the research report, plus a Phase 0 (preparation) and Phase 6 (verification/completion). Each phase has multiple checklist items — one per specific edit.

Phase 0: Preparation (read files, confirm structure)
Phase 1: TDD Template Frontmatter Additions (1 file, ~3 edits)
Phase 2: sc:roadmap Extraction + Scoring Upgrades (2 files, ~4 edits)
Phase 3: sc:spec-panel Additions (1 file, 3 edits)
Phase 4: sc:tasklist --spec Implementation (1 file, 3 edits)
Phase 5: PRD→TDD Handoff Improvements (1 file, 4 edits)
Phase 6: Integration Verification + make sync-dev + completion (16 checks)

---

## TEMPLATE_NOTES

Use Template 02 (Complex Task):
- Multiple phases with different file targets
- Each edit requires reading the target file first to find exact insertion point
- Verification steps after each phase
- Integration checklist in final phase

---

## AMBIGUITIES_FOR_USER

None — the implementation plan is fully specified from verified research. All 5 CODE-CONTRADICTED claims have been corrected. The 13 open questions from Section 9 are documented but none block implementation.
