# Pipeline Trace Investigation: Why TDD+PRD Produces Fewer Tasks Than Spec-Only

**Investigator**: Claude Opus 4.6 (1M context)
**Date**: 2026-04-03
**Methodology**: Full-file reads of all pipeline artifacts at every stage, plus code-level analysis of prompts and parser rules.

---

## Pipeline Trace Table

| Stage | Spec-Only | TDD+PRD | Delta | Notes |
|-------|-----------|---------|-------|-------|
| Input lines | 312 | 1,282 (TDD+PRD) | +4.1x | TDD has 876 lines, PRD adds 406 |
| Extraction lines | 303 | 660 | +2.2x | TDD extraction has 14 sections vs 8 |
| Extraction entities | ~49 distinct | ~85 distinct | +1.7x | FRs, NFRs, endpoints, components, tests, migration phases, etc. |
| Variant A (Opus) lines | 319 | 438 | +1.4x | Opus variant |
| Variant A actionable items | ~45 table rows + headings | ~44 headings + tables | ~1:1 | Comparable density |
| Variant B (Haiku) lines | 1,026 | 886 | -0.9x | Haiku variant |
| Variant B actionable items | ~64 headings + 45 sub-items | ~68 headings + tables | ~1:1 | TDD variant is actually LESS verbose |
| Merged roadmap lines | 380 | 746 | +2.0x | TDD roadmap is twice as long |
| Merged roadmap phases | 5 | 3 | -40% | **KEY: Fewer phases = fewer task buckets** |
| Parser-visible items (headings + bullets + numbered) | 47 | 204 | +4.3x | TDD roadmap has MORE parseable items |
| R-items parsed | 87 | 88 | +1% | Parser extracted ~equal R-items from both |
| Tasks generated | 87 | 44 | -49% | **THE COLLAPSE** |
| R-items per task (mode) | 1:1 | 2:1 (38 tasks have 2+ R-items) | -49% | Multiple R-items consolidated into single tasks |

---

## Stage-by-Stage Analysis

### STAGE 1: EXTRACTION -- No Collapse

**Spec-only extraction** (`test3-spec-baseline/extraction.md`):
- 5 FRs, 3 NFRs, 5 implicit FRs, 4 implicit NFRs = ~17 requirement items
- 19 acceptance criteria sub-items
- 9 success criteria, 4 risks, ~7 dependencies
- 8 structured sections, 303 lines
- Format: Markdown headings + bullets, relatively flat

**TDD+PRD extraction** (`test1-tdd-prd-v2/extraction.md`):
- 5 FRs, 8 NFRs = 13 requirement items
- 19 acceptance criteria sub-items
- 2 data model entities (UserProfile, AuthToken) with field-level detail (11 field rows)
- 6 API endpoint detail sections with request/response schemas and error tables
- 9 components (5 backend, 4 frontend) with dependency mappings
- 6 test cases, 3 migration phases, 6 rollback steps, 2 runbook scenarios
- 10 success criteria, 7 risks, 10 dependencies, 5 gaps
- 14 structured sections, 660 lines
- Format: Deep mix of headings, bullets, tables, code blocks

**Verdict**: Extraction PRESERVES TDD granularity. The TDD extraction has ~85 distinct actionable entities vs ~49 for spec-only. The `build_extract_prompt_tdd()` function at `prompts.py:208-377` explicitly asks for 6 additional TDD-specific sections (Data Models, API Specs, Component Inventory, Testing Strategy, Migration Plan, Operational Readiness) with per-entity extraction. **No collapse at this stage.**

### STAGE 2: GENERATION -- Moderate Structural Shift

**Spec-only variants**:
- Opus (319 lines, 30 headings): Fine-grained table-based structure. Each table row = one task. ~45 actionable table rows within a 5-phase structure.
- Haiku (1,026 lines, 64 headings): Extremely detailed subsection-based structure. 6 phases with named deliverables under each component. ~45+ sub-items.

**TDD+PRD variants**:
- Opus (438 lines, 44 headings): 3-phase structure with dense tables. Each table row covers a component. ~44 headings but tasks are bundled into component-level rows rather than per-deliverable rows.
- Haiku (886 lines, 68 headings): 3-phase structure with wiring tasks, subsections, tables. More verbose but the phases themselves are LARGER -- Phase 1 alone has 19 subsections.

**Key observation**: The TDD+PRD variants consolidate the 5 spec-only phases into 3 phases. This happens because the generate prompt (`prompts.py:380-483`) says:

```
"After the frontmatter, provide a complete roadmap including:
1. Executive summary
2. Phased implementation plan with milestones
3. Risk assessment and mitigation strategies
..."
```

When TDD content provides explicit phased rollout (Alpha/Beta/GA), the LLM adopts that 3-phase structure rather than creating its own 5-phase breakdown. The generate prompt does NOT instruct the LLM to "create at least N phases" or "create one phase per major domain area."

The TDD supplementary context at `prompts.py:436-462` says:
```
"Address each [section] in the roadmap with specific implementation phases, tasks, and milestones"
```

But it does NOT say "create a separate phase for each" or "ensure at least as many phases as the spec-only variant would produce." The LLM is free to bundle everything into fewer, larger phases.

**Verdict**: Generation creates **fewer phases** for TDD+PRD because the TDD's own rollout plan (3 phases) becomes the structural template. The content per phase is DENSER (Phase 1 alone has 19 subsections in Haiku) but there are only 3 buckets instead of 5. **Partial collapse -- structural, not content-level.**

### STAGE 3: MERGE -- Consolidation Amplifies Phase Reduction

**Spec-only merged roadmap** (380 lines, 39 headings):
- 5 phases with clear separation of concerns
- Phase 1: Foundation (schema, crypto, DI) - 4 subsections
- Phase 2: Core Auth Logic (services) - 3 subsections  
- Phase 3: Integration (routes, middleware, tests) - 3 subsections
- Phase 4: Hardening (perf, security, coverage, rollback) - 5 subsections
- Phase 5: Production Readiness (secrets, monitoring, deploy, docs) - 4 subsections
- Each subsection has a task table with individual rows = individual items
- ~66 actionable table rows + 8 top-level bullets = ~74 parseable items

**TDD+PRD merged roadmap** (746 lines, 67 headings):
- 3 phases with dense, multi-section structure
- Phase 1 (200+ lines): Infrastructure, Backend Components, API Endpoints, Audit Logging, Frontend, API Gateway, Monitoring, Security Checkpoint, Manual Testing, Exit Criteria = 10 subsections
- Phase 2 (137 lines): Password Reset, Admin Audit API, Compliance, Production Deploy, Beta, Load Testing, Tuning, Exit Criteria = 8 subsections
- Phase 3 (94 lines): Security Gate, Traffic Ramp, Legacy Deprecation, Flag Cleanup, Runbooks, Metrics, Docs, Post-GA, Exit Criteria = 9 subsections
- Dense mix of tables, numbered lists, bullets, wiring tasks
- BUT: many items are inside tables (not parseable as R-items) or are "Wiring Task" narrative blocks

The merge prompt (`prompts.py:596-658`) says:
```
"Produce a final merged roadmap that uses the selected base variant as foundation
and incorporates the best elements from the other variant"
```

It does NOT say "consolidate overlapping items" or "remove redundancy." But the base variant (Haiku, score 79) already has a 3-phase structure, and the merge preserves that. The Opus variant's 9-week timeline is compressed to 6 weeks per debate convergence.

**Verdict**: The merge does NOT actively reduce granularity. It preserves the 3-phase structure from the winning base variant. The granularity loss is inherited from generation. **No additional collapse at merge.**

### STAGE 4: PARSING -- The Primary Collapse Point

The SKILL.md Section 4.1 (`src/superclaude/skills/sc-tasklist-protocol/SKILL.md`) defines R-item boundaries:

```
1. Split the roadmap into "roadmap items" by scanning top-to-bottom.
2. A new roadmap item starts at any of:
   - A markdown heading (#, ##, ###, etc.)
   - A bullet point (-, *, +)
   - A numbered list item (1., 2., ...)
```

**The parser correctly finds 88 R-items in the TDD+PRD roadmap** (vs 87 in spec-only). So the PARSER is not failing to see items.

**The collapse happens in R-item-to-task mapping (Section 4.2-4.4)**:

Section 4.2 creates phase buckets:
```
If the roadmap explicitly labels phases/versions/milestones:
  Treat each such heading as a phase bucket in order of appearance.
```

The TDD+PRD roadmap has 3 phases. The spec-only roadmap has 5 phases.

Section 4.4 then assigns R-items to phase buckets. With only 3 phase buckets, all 88 R-items must fit into 3 phases. The tasks-per-phase ratio becomes:
- Spec-only: 87 tasks / 5 phases = ~17 tasks/phase
- TDD+PRD: 44 tasks / 3 phases = ~15 tasks/phase

But the KEY issue is: **multiple R-items are being consolidated into single tasks**. The traceability matrix shows:
- 38 tasks have 2 R-items each
- 5 tasks have 3 R-items each
- 1 task has 5 R-items
- 1 task has 8 R-items
- 1 task has 9 R-items
- 1 task has 27 R-items (!!!)

The "1 task per roadmap item by default; splits only when item contains independently deliverable outputs" rule (from the tasklist-index deterministic rules) is applied. But the generator is MERGING R-items that share a phase subsection into a single task.

**Root cause**: The TDD+PRD roadmap uses DEEPER heading nesting. Phase 1 has subsections like "1.2 Backend Core Components" which contains a table with 6 component rows. The parser sees the heading "1.2 Backend Core Components" as one R-item, the 6 table rows as 6 more R-items, but then the task generator CONSOLIDATES them into 1-2 tasks because they share the same subsection context.

In the spec-only roadmap, each component is in its own subsection (1.2, 1.3, 1.4) with its own tasks table. So each gets its own task(s).

---

## Root Cause Diagnosis

**Answer: E -- Multiple stages compounding, but two stages dominate.**

### Primary Cause 1: Generation Creates Fewer Phases (STAGE 2)

**File**: `src/superclaude/cli/roadmap/prompts.py`, lines 380-483 (`build_generate_prompt`)
**Specific text causing collapse**:

The prompt at line 421-427 says:
```python
"After the frontmatter, provide a complete roadmap including:\n"
"1. Executive summary\n"
"2. Phased implementation plan with milestones\n"
...
```

It provides NO guidance on phase count. When TDD content includes a 3-phase rollout (Alpha/Beta/GA), the LLM adopts it. The spec-only path has no rollout plan, so the LLM creates 5 phases organically from the layered architecture.

The TDD supplementary context (lines 436-462) says:
```python
"- **Migration and Rollout Plan**: Include phased rollout tasks with feature "
"flags, rollback procedures, and success criteria per stage.\n"
```

This tells the LLM to INCLUDE rollout phases, which then becomes the ORGANIZING STRUCTURE for the entire roadmap rather than a section within development phases.

### Primary Cause 2: Tasklist Generator Consolidates R-items Into Fewer Tasks (STAGE 4)

**File**: `src/superclaude/skills/sc-tasklist-protocol/SKILL.md`, Section 4.4 (task generation)

The rule "1 task per roadmap item by default; splits only when item contains independently deliverable outputs" allows the generator to keep the 1:1 ratio. But in practice, when a roadmap heading like "1.2 Backend Core Components" is followed by a table listing 6 components, the generator treats the heading as the task and the table as details WITHIN that task, rather than creating 6 separate tasks.

The spec-only roadmap avoids this because each component gets its own `#### 1.2 PasswordHasher Service` heading, which the parser and generator treat as a separate work unit.

---

## Specific Fixes

### Fix 1: Generate Prompt -- Mandate Minimum Phase Granularity (Impact: HIGH)

In `build_generate_prompt()` at `prompts.py:421`, after "Phased implementation plan with milestones", add:

```
"Create phases based on architectural layers and concerns, NOT based on 
deployment/rollout stages. A phased implementation plan should have at 
least one phase per major architectural layer (e.g., foundation/data layer, 
service layer, integration/API layer, testing/hardening, production readiness). 
Deployment rollout stages (alpha, beta, GA) should be subsections within 
the appropriate development phase, not top-level phases that subsume 
development work."
```

### Fix 2: Generate Prompt -- Mandate Per-Entity Tasks for TDD Content (Impact: HIGH)

In the TDD supplementary context at `prompts.py:448-462`, change from:

```python
"- **Component Inventory**: Include component implementation and integration "
"tasks with dependency wiring and prop/interface contracts.\n"
```

To:

```python
"- **Component Inventory**: Create a SEPARATE implementation task for EACH 
component listed in the extraction (e.g., one task for PasswordHasher, one 
for JwtService, one for TokenManager). Do NOT combine multiple components 
into a single 'implement backend components' task.\n"
```

Apply the same pattern to Data Models, API Endpoints, and Testing Strategy sections.

### Fix 3: SKILL.md Parser -- Recognize Table Rows as Separate R-items (Impact: MEDIUM)

In Section 4.1, add after the current boundary rules:

```
- A markdown table row that begins with `|` followed by actionable content 
  (implementation task, component name, endpoint specification) is a 
  separate roadmap item. Table headers and separator rows (`|---|`) are 
  NOT roadmap items.
```

This would increase TDD+PRD R-items from 88 to ~150+, giving more granular inputs to the task generator.

### Fix 4: SKILL.md Task Generator -- Limit R-item Consolidation (Impact: HIGH)

In Section 4.4, add:

```
A task MUST NOT consolidate more than 3 R-items unless those R-items are 
genuinely inseparable (e.g., a migration up and down are one task). If a 
roadmap subsection produces more than 3 R-items, split into multiple tasks 
grouped by deliverable type (implementation, testing, configuration).
```

---

## Summary

The TDD+PRD pipeline produces fewer tasks due to a compounding effect across two stages:

1. **Generation (primary)**: The LLM adopts the TDD's 3-phase rollout plan as the roadmap's organizing structure, creating 3 dense phases instead of 5 architectural phases. This means Phase 1 alone contains work that the spec-only pipeline spreads across Phases 1-3.

2. **Task generation (secondary)**: Dense phases with nested content (heading + table of components) get consolidated into fewer tasks. The spec-only roadmap's flatter structure (one heading per component) naturally produces 1:1 R-item-to-task mapping, while the TDD+PRD roadmap's nested structure produces 2:1 or worse.

The irony is that the parser DOES see the granularity (88 R-items vs 87), but the task generator consolidates multiple R-items into single tasks because they share subsection context. The fix requires changes at both the generation prompt level (create more phases, create per-entity tasks) and the tasklist skill level (limit consolidation, recognize table rows).
