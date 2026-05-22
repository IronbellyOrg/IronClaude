# Research Notes: Tasklist Generation Quality — Fewer Tasks from Richer Input

**Date:** 2026-04-03
**Scenario:** A (explicit hypotheses, specific files, clear output)
**Depth Tier:** Standard (focused question, known files, ~10 relevant files)

---

## EXISTING_FILES

### Tasklist Protocol
- `.claude/skills/sc-tasklist-protocol/SKILL.md` — Full tasklist generation algorithm. DIFFERS between master and feature branch (1 commit changed it, +122 lines starting at line 121)
- `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` — Source of truth version

### Tasklist Prompts
- `src/superclaude/cli/tasklist/prompts.py` — 237 lines. Contains `build_tasklist_fidelity_prompt` (line 17) and `build_tasklist_generate_prompt` (line 151). TDD/PRD supplementary blocks likely here.

### Baseline Results
- `.dev/test-fixtures/results/test3-spec-baseline/roadmap.md` — 380 lines, 38 ## or ### sections, 5 explicit phases
- `.dev/test-fixtures/results/test3-spec-baseline/tasklist-index.md` — 67 lines, 87 tasks, 5 phases
- `.dev/test-fixtures/results/test3-spec-baseline/phase-1-tasklist.md` — 617 lines, 16 tasks
- `.dev/test-fixtures/results/test3-spec-baseline/phase-{2-5}-tasklist.md` — 17, 17, 22, 15 tasks

### TDD+PRD Enriched Results
- `.dev/test-fixtures/results/test1-tdd-prd-v2/roadmap.md` — 746 lines, 66 ## or ### sections, 3 explicit phases
- `.dev/test-fixtures/results/test1-tdd-prd-v2/tasklist-index.md` — 219 lines, 44 tasks, 3 phases
- `.dev/test-fixtures/results/test1-tdd-prd-v2/phase-1-tasklist.md` — 1,325 lines, 27 tasks
- `.dev/test-fixtures/results/test1-tdd-prd-v2/phase-{2-3}-tasklist.md` — 9, 8 tasks

### Roadmap Prompts (context)
- `src/superclaude/cli/roadmap/prompts.py` — Roadmap generation prompts (may influence phase structure)

## PATTERNS_AND_CONVENTIONS

### Key Numbers
- Baseline: 312 input lines → 380 roadmap lines → 87 tasks (5 phases)
- TDD+PRD: 1,282 input lines → 746 roadmap lines → 44 tasks (3 phases)
- Ratio: 4.1x more input → 2.0x more roadmap → 49% FEWER tasks

### Protocol Diff
The tasklist protocol skill (SKILL.md) was modified between master and feature branch:
- 1 commit changed it (a9cf7ee)
- +122 lines added starting at line 121 (TDD/PRD supplementary blocks spanning Sections 3.x, 4.1a, 4.1b, and 4.4a/4.4b)

## SOLUTION_RESEARCH
N/A — this is a diagnosis investigation, not implementation planning

## RECOMMENDED_OUTPUTS

### Research Files (6 agents)
| # | Topic | Type | Output |
|---|-------|------|--------|
| 01 | Protocol diff analysis | Code Tracer | research/01-protocol-diff.md |
| 02 | Tasklist prompts analysis | Code Tracer | research/02-tasklist-prompts.md |
| 03 | Roadmap phase structure comparison | Pattern Investigator | research/03-roadmap-phases.md |
| 04 | Task decomposition comparison | Pattern Investigator | research/04-task-decomposition.md |
| 05 | Roadmap prompts analysis | Code Tracer | research/05-roadmap-prompts.md |
| 06 | Context window analysis | Architecture Analyst | research/06-context-analysis.md |

### Synthesis Files (3)
| # | Report Sections | Sources |
|---|----------------|---------|
| synth-01 | Problem Statement, Current State | research 01-06 |
| synth-02 | Gap Analysis, Root Cause Analysis, Options | research 01-06 |
| synth-03 | Recommendations, Implementation Plan, Open Questions | research 01-06 |

## SUGGESTED_PHASES

### Phase 2: Deep Investigation (6 parallel agents)
1. **Protocol Diff** (Code Tracer): Read `git diff master..HEAD -- src/superclaude/skills/sc-tasklist-protocol/SKILL.md`, understand what changed and how it affects decomposition rules (Section 4.4), phase bucketing (4.2), task conversion (4.4)
2. **Tasklist Prompts** (Code Tracer): Read `src/superclaude/cli/tasklist/prompts.py` line 151+, document the `build_tasklist_generate_prompt` function, find TDD/PRD supplementary blocks, check for language that suppresses task creation
3. **Roadmap Phase Structure** (Pattern Investigator): Read both roadmaps, count explicit phases, count discrete work items per phase, determine why TDD+PRD has 3 phases (66 sections) vs baseline 5 phases (38 sections)
4. **Task Decomposition** (Pattern Investigator): Pick 3 equivalent areas (login, password reset, testing) in both tasklists, compare task granularity, identify where the baseline splits and TDD+PRD consolidates
5. **Roadmap Prompts** (Code Tracer): Read `src/superclaude/cli/roadmap/prompts.py`, check if the merge/generate prompts influence phase count differently for TDD vs spec input
6. **Context Window** (Architecture Analyst): Calculate approximate token counts for both generation scenarios (roadmap + TDD + PRD + skill protocol), assess whether context saturation could explain fewer tasks

### Phase 3: Analyst + QA Gate (parallel)
Standard completeness verification

### Phase 4: Synthesis (3 parallel agents)
Standard synthesis from research files

### Phase 5: Assembly & Validation
Standard report assembly and QA

## TEMPLATE_NOTES
Template 02 — multi-phase investigation with parallel agents, synthesis, assembly, validation

## AMBIGUITIES_FOR_USER
None — the research prompt provides clear hypotheses, evidence, and expected output
