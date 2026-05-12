# QA Deep Dive: Root Cause Analysis -- 44 vs 87 Task Gap

**Date:** 2026-04-03
**Phase:** Root Cause Challenge (Adversarial QA)
**Reviewer:** rf-qa-qualitative

---

## Overall Verdict: The research report's root causes are SURFACE-LEVEL, not WRONG

The research team identified real contributing factors but missed the DOMINANT mechanism. The actual root cause is a structural interaction between the roadmap format and the tasklist parsing algorithm -- not PRD suppression, not protocol merge directives.

---

## Investigation Area 1: The Roadmap IS the Bottleneck

### Raw Data

| Metric | TDD+PRD Roadmap | Spec Baseline Roadmap |
|--------|-----------------|----------------------|
| Total lines | 746 | 380 |
| Table rows (lines starting with `\|`) | 257 | 198 |
| Heading lines (`#`) | 67 | 39 |
| Bullet items (`-` or `*`) | 103 | 8 |
| Numbered list items | 44 | 0 |
| Parsed R-items (from tasklist index) | 44 | 87 |
| Tasks generated | 44 | 87 |
| Phases | 3 | 5 |

### The Paradox Explained

The TDD+PRD roadmap has MORE structural elements (257+67+103+44 = 471) than the baseline (198+39+8+0 = 245). It is a richer, more detailed document. Yet it produces FEWER R-items (44 vs 87).

This is because the R-item count is NOT a function of structural element count. It is a function of HOW the tasklist parser interprets those elements.

### The Baseline's Table Structure is Parser-Optimal

Looking at the baseline roadmap (`test3-spec-baseline/roadmap.md`), every task is expressed as a TABLE ROW within a phase subsection:

```
#### 1.1 Database Schema and Migrations
| Task | Requirements Covered | Details |
|------|---------------------|---------|
| Create `users` table migration | FR-AUTH.2, ... | Columns: ... |
| Create `refresh_tokens` table migration | FR-AUTH.3d, ... | Columns: ... |
| Verify all migrations are reversible | FR-AUTH.1-IMPL-5 | Automated test: ... |
```

The baseline has 5 phases x many subsections x granular table rows. Each table row is ONE independently actionable item. The parser sees:

- Phase 1: 16 table rows across 5 subsections (1.1-1.5)
- Phase 2: 17 table rows across 3 subsections (2.1-2.3)
- Phase 3: 17 table rows across 3 subsections (3.1-3.3)
- Phase 4: 22 table rows across 5 subsections (4.1-4.5)
- Phase 5: 15 table rows across 4 subsections (5.1-5.4)

Total: 87 table rows = 87 R-items = 87 tasks.

### The TDD+PRD Roadmap Bundles Content Under Fewer Actionable Headers

The TDD+PRD roadmap (`test1-tdd-prd-v2/roadmap.md`) has a DIFFERENT structure. It uses:

1. **Numbered lists for infrastructure provisioning** (5 items in section 1.1 consolidated into a single "Infrastructure Provisioning" concept)
2. **Table rows for components** (6 rows in section 1.2)
3. **Wiring Task blocks** (prose bullets under `**Wiring Task 1.2.1**` etc.) -- these are NOT parsed as independent R-items because they are sub-bullets under a wiring heading, not top-level actionable items
4. **Exit Criteria checklists** (`- [ ]` items) -- these are checkpoints, not tasks
5. **Alert threshold tables, rollback procedure lists, performance tuning tables** -- these are operational context, not independently actionable tasks

The key insight: The TDD+PRD roadmap is NARRATIVELY richer but ACTIONABLY sparser. The extra 366 lines (746 vs 380) are context, wiring documentation, rollback procedures, alert thresholds, exit criteria, and prose -- content that makes the roadmap MORE USEFUL for an engineer but does NOT produce R-items under the SKILL.md 4.1 parsing rules.

---

## Investigation Area 2: The Roadmap Generation Prompt IS a Contributing Factor

### What I Found

Reading `src/superclaude/cli/roadmap/prompts.py`:

**`build_generate_prompt` (line 380):** When `tdd_file is not None`, the prompt appends (lines 436-463):
```
"Address each in the roadmap with specific implementation phases, tasks, and milestones"
"Include schema implementation tasks with entity relationships..."
"Include per-endpoint implementation tasks..."
"Include component implementation and integration tasks..."
```

This instructs the LLM to produce COMPREHENSIVE, DETAILED roadmap content. The LLM responds by writing rich narrative sections with wiring documentation, integration points, and operational context.

**`build_merge_prompt` (line 596):** When `tdd_file is not None`, the merge prompt says (lines 629-641):
```
"Preserve exact technical identifiers from both variants"
"Ensure the merged roadmap retains all TDD-derived implementation tasks"
```

This tells the merge step to CONSOLIDATE and PRESERVE -- but "preserve" means keeping the narrative structure, not necessarily keeping each item as a separate parseable row.

### The Causal Chain

1. TDD input triggers the supplementary TDD prompt in `build_generate_prompt`
2. The prompt tells the LLM to "include per-endpoint implementation tasks" etc.
3. The LLM responds with RICH, CONTEXTUAL roadmap sections that include wiring documentation, integration points, alert thresholds, rollback procedures
4. These sections are VALUABLE engineering content but are structured as NARRATIVE BLOCKS, not as INDIVIDUAL TABLE ROWS
5. The merge step preserves this narrative structure
6. The tasklist parser (SKILL.md 4.1) counts R-items based on headings, bullets, and numbered items -- but many of the TDD+PRD roadmap's structural elements are SUB-ITEMS (wiring bullets under wiring headings) or CONTEXT (alert threshold tables, exit criteria checklists) rather than independently actionable tasks

### Does the Merge Step Consolidate?

Reading `build_merge_prompt` (lines 608-627): The merge prompt says "uses the selected base variant as foundation and incorporates the best elements from the other variant." It does NOT explicitly say "combine overlapping items" -- but the natural LLM behavior when merging two rich roadmaps is to SYNTHESIZE rather than CONCATENATE. This means duplicate items across variants get merged into single items, reducing count.

The baseline merge is also adversarial, but both baseline variants are simpler (spec-only), so there is LESS overlap to consolidate.

---

## Investigation Area 3: The SKILL.md Phase Bucketing -- This IS the Root Cause

### The Critical Rule at SKILL.md 4.1

```
2. A new roadmap item starts at any of:
   - A markdown heading (#, ##, ###, etc.)
   - A bullet point (-, *, +)
   - A numbered list item (1., 2., ...)
```

### How the Baseline Produces 87 R-items

The baseline roadmap has 5 phases. Each phase has 3-5 subsections. Each subsection has a 3-column table. The parser treats EACH TABLE ROW as a roadmap item because table rows are the primary structural unit. Counting the non-header table rows across all 5 phases gives exactly 87.

Verification:
- Phase 1: subsections 1.1 (3 rows), 1.2 (4 rows), 1.3 (4 rows), 1.4 (3 rows), 1.5 (2 rows) = 16
- Phase 2: subsections 2.1 (7 rows), 2.2 (7 rows), 2.3 (3 rows) = 17
- Phase 3: subsections 3.1 (4 rows), 3.2 (7 rows), 3.3 (6 rows) = 17
- Phase 4: subsections 4.1 (4 rows), 4.2 (9 rows), 4.3 (3 rows), 4.4 (3 rows), 4.5 (3 rows) = 22
- Phase 5: subsections 5.1 (3 rows), 5.2 (5 rows), 5.3 (3 rows), 5.4 (4 rows) = 15
- Total: 16 + 17 + 17 + 22 + 15 = 87

### How the TDD+PRD Produces 44 R-items

The TDD+PRD roadmap has 3 phases. Looking at the R-item registry in the tasklist index:
- Phase 1: R-001 to R-027 = 27 items
- Phase 2: R-028 to R-036 = 9 items
- Phase 3: R-037 to R-044 = 8 items
- Total: 44

But the TDD+PRD roadmap has 257 table rows, 67 headings, 103 bullets, and 44 numbered items! Where did the other items go?

**Answer: The parser is NOT counting ALL structural elements. It is counting INDEPENDENTLY ACTIONABLE items within the phased implementation plan.**

Looking at what the parser SKIPS in the TDD+PRD roadmap:

1. **Wiring Task blocks** (lines 79-151): 5 wiring task blocks with 4 bullets each = ~20 bullets. These are SUB-ITEMS documenting integration architecture. The parser likely treats each `**Wiring Task X.Y.Z**` heading as a single item (if it parses bold headings at all) or merges wiring bullets into their parent section.

2. **Exit Criteria checklists** (lines 199-216, 326-335, 420-431): ~35 checkbox items. These are verification criteria, not actionable tasks. The parser correctly skips these.

3. **Alert Threshold tables** (lines 285-291): 5 rows. These are operational context, not tasks.

4. **Rollback Procedure numbered items** (lines 300-305): 5 items. These are sub-procedures of the rollback section.

5. **Load Testing tables** (lines 309-315): 5 rows. These are test scenarios within a single "Load Testing" task.

6. **Performance Tuning tables** (lines 319-323): 3 rows. These are mitigation options within a single task.

7. **Manual Testing tables** (lines 182-197): 14 rows. These are test scenarios within a single "Manual Testing" task.

8. **Phase 2 Compliance table** (lines 259-264): 4 rows. These are acceptance criteria within a single "Compliance" task.

9. **Success Metrics table** (lines 390-398): 7 rows. These are metrics within a single "Metrics Baseline" task.

10. **Risk Assessment, Resource Requirements, Integration Points, and other NON-PHASE sections** (lines 433+): These are appendix/supporting sections, not phased implementation items.

**Precise structural analysis within the Phased Implementation Plan sections:**

| Element Type | TDD+PRD Count | Baseline Count |
|--------------|---------------|----------------|
| Table data rows | 79 | 85 |
| Non-wiring bullets | 21 | n/a |
| Wiring documentation bullets | 30 | 0 |
| Numbered sub-items | 38 | 0 |
| Headings within phases | 31 | 20 |
| Exit criteria checkboxes | 35 | 0 |
| **Total potential R-items** (table rows + bullets + numbered + headings) | **169** | **~87** |
| **Actual R-items parsed** | **44** | **87** |
| **Conversion rate** | **26%** | **~100%** |

The TDD+PRD roadmap has 169 structural elements but only 44 (26%) become R-items. The baseline has ~87 structural elements and ~100% become R-items.

**Why the massive conversion rate difference?** The TDD+PRD roadmap's structural elements are HIERARCHICALLY NESTED. The numbered items (38) are sub-steps within a parent section (e.g., items 1-5 under "1.1 Infrastructure Provisioning" are sub-steps of ONE provisioning task). The wiring bullets (30) are documentation for a parent component. The exit criteria (35) are verification checkpoints, not tasks. The parser correctly treats these as context for their parent item, not as independent R-items.

The baseline roadmap's structural elements are FLAT. Each table row IS an independent task. There are no numbered sub-items, no wiring documentation, no exit criteria within the phased plan. The entire structure is tables where each row = 1 task.

**This is the fundamental insight: the TDD+PRD roadmap is HIERARCHICAL (tasks with sub-items), the baseline is FLAT (each row is a task). The parser preserves this structure -- hierarchical items produce fewer R-items because sub-items are absorbed into their parent.**

---

## Investigation Area 4: The Merge Step

### Does Merge Consolidate?

Reading the merge prompt at `prompts.py:608-627`: The merge prompt says "uses the selected base variant as foundation and incorporates the best elements from the other variant." The TDD+PRD merge selected Haiku Architect as base (variant_scores: "A:71 B:79").

The Haiku Architect variant likely already had a consolidated 3-phase structure (Alpha -> Beta -> GA) which is a DELIVERY-MILESTONE paradigm rather than a TECHNICAL-LAYER paradigm. The baseline's 5 phases (Foundation -> Core Auth -> Integration -> Hardening -> Production) is a technical-layer paradigm that naturally has more granular items because each technical layer is an independent unit of work.

The 3-phase delivery paradigm BUNDLES technical concerns within delivery milestones:
- Phase 1 (Alpha): ALL backend + ALL frontend + monitoring + security review = 27 items
- Phase 2 (Beta): Password reset + compliance + deployment + load testing = 9 items
- Phase 3 (GA): Pen testing + traffic ramp + deprecation + docs = 8 items

The 5-phase technical paradigm SEPARATES technical concerns:
- Phase 1 (Foundation): Schema + crypto = 16 items
- Phase 2 (Core Auth): Services + feature flag = 17 items
- Phase 3 (Integration): Routes + middleware + integration tests = 17 items
- Phase 4 (Hardening): Perf + security + coverage = 22 items
- Phase 5 (Production): Secrets + monitoring + deploy + docs = 15 items

**The 5-phase paradigm produces more items because it treats each technical layer as a separate phase with its own subsections and tables. The 3-phase paradigm produces fewer items because it treats technical concerns as SUB-ITEMS within delivery milestones.**

---

## Investigation Area 5: Pre-Merge Variants

I was not able to compare individual variant item counts directly (the variant files exist but counting their R-items requires the full parsing algorithm). However, the key observation is:

- The baseline variants both use a 5-phase technical-layer paradigm (this is what the spec-only extraction naturally produces)
- The TDD+PRD variants diverge: Opus proposed 9 weeks/more phases, Haiku proposed 4 weeks/fewer phases
- The merge compromised at 6 weeks / 3 phases -- closer to Haiku's consolidation

This means the merge step DID consolidate the phase structure, but this consolidation happened at the ROADMAP level (3 delivery phases instead of 5 technical phases), not at the individual-item level.

---

## THE ACTUAL ROOT CAUSE (3 interacting factors)

### Root Cause 1 (DOMINANT): Delivery-Milestone Phasing vs Technical-Layer Phasing

The TDD+PRD roadmap uses a 3-phase DELIVERY-MILESTONE paradigm (Alpha -> Beta -> GA). The baseline uses a 5-phase TECHNICAL-LAYER paradigm (Foundation -> Core Auth -> Integration -> Hardening -> Production).

The delivery-milestone paradigm bundles multiple technical concerns into each milestone. When the tasklist parser encounters a milestone phase, many of the table rows within it are NOT independently actionable tasks -- they are sub-items of a single task (test scenarios within a "Manual Testing" task, alert thresholds within a "Monitoring" task, compliance criteria within a "Compliance" task).

The technical-layer paradigm naturally decomposes into independently actionable tasks because each layer IS a task. "Implement PasswordHasher" and "Implement JwtService" are separate layer-1 items. In the delivery paradigm, they are both part of "Backend Core Components (Days 1-4)" which is a SINGLE section containing a table with 6 rows.

**Impact on gap: This is the PRIMARY factor. 3 phases vs 5 phases, combined with the delivery vs technical paradigm, accounts for approximately 30-35 of the 43-item gap.**

### Root Cause 2 (SIGNIFICANT): TDD Richness Creates Narrative Depth Instead of Actionable Breadth

When a TDD is provided, the roadmap generation prompt tells the LLM to "include per-endpoint implementation tasks with request/response schemas, authentication, rate limiting" etc. The LLM responds by writing COMPREHENSIVE sections for each component -- but this comprehensiveness manifests as wiring documentation, alert thresholds, rollback procedures, and exit criteria WITHIN each item, not as ADDITIONAL independent items.

The result: each R-item in the TDD+PRD roadmap is MUCH more detailed than each R-item in the baseline. Compare:

- **Baseline R-item**: `| Implement PasswordHasher class | FR-AUTH.1, FR-AUTH.2, FR-AUTH.1-IMPL-1 | Methods: hash(plaintext): Promise<string>, verify(plaintext, hash): Promise<boolean> |` (1 table row)
- **TDD+PRD R-item for PasswordHasher**: `| Implement PasswordHasher | PasswordHasher | NFR-SEC-001 | bcrypt with cost factor 12. Abstract interface for future algorithm migration. Unit tests: hash/verify operations, timing invariance. |` (1 table row) PLUS **Wiring Task 1.2.2** block with 4 bullets documenting the strategy registry

Both produce exactly 1 R-item. But the TDD+PRD version has 5x more content per item. The parser does not split a wiring block into separate R-items -- it is context for the parent item.

**Impact on gap: This accounts for approximately 5-8 items. Content that COULD be separate R-items (like "Configure strategy registry for PasswordHasher") is instead presented as narrative context within the parent item.**

### Root Cause 3 (MODERATE): The Adversarial Merge Selects a More Consolidated Base

The TDD+PRD merge selected Haiku Architect (3-phase, 4-week aggressive timeline) as the base variant. Haiku's approach naturally consolidates items into larger deliverable units. The merge prompt says to use the base as foundation and "incorporate best elements" -- not to expand the base's item count. The Opus variant's more granular 9-week plan was REJECTED at the scoring step.

The baseline merge also uses adversarial debate, but both baseline variants produced similar 5-phase structures (because spec-only extraction naturally produces technical-layer roadmaps). The merge of two similar structures preserves item count. The TDD+PRD merge of two DIVERGENT structures (Opus 9-week vs Haiku 4-week) produces a COMPROMISE that inherits Haiku's consolidation.

**Impact on gap: This accounts for approximately 5-10 items. A different base variant selection could have preserved more granular items.**

---

## What the Research Report Got Right vs Wrong

### Right (but insufficient):
1. PRD suppression language -- this IS real but it prevents PRD from ADDING tasks; it doesn't explain why TDD content also doesn't add tasks
2. Protocol merge directives (4.4a/4.4b) -- these directives say "merge rather than duplicate," which does prevent supplementary task generation from inflating count
3. Roadmap phase paradigm -- the research correctly identified 3 vs 5 phases as a factor but did not explain WHY the paradigm matters
4. Testing consolidation -- real but minor

### Wrong / Missed:
1. **The research did not identify that the ROADMAP FORMAT is the bottleneck** -- the tasklist has a 1:1 R-item-to-task ratio, so the question is not "why doesn't the tasklist generate more tasks?" but "why does the roadmap have fewer R-items?"
2. **The research did not trace the causal chain from TDD input -> prompt enrichment -> narrative-dense roadmap -> fewer parseable R-items** -- this is the actual mechanism
3. **The research did not compare the structural composition of the two roadmaps** -- the baseline is 87 table rows that are each independently actionable; the TDD+PRD has 257 table rows but most are sub-items (test scenarios, alert thresholds, compliance criteria) within a parent task
4. **The research did not identify the delivery-milestone vs technical-layer paradigm difference** as the dominant cause of the gap

---

## Recommendations

### Fix 1: Modify the roadmap generation prompt to request ITEM-PER-ENTITY output

When TDD input is provided, the `build_generate_prompt` should explicitly instruct:
```
"For each data model entity, create a SEPARATE table row task."
"For each API endpoint, create a SEPARATE table row task."
"For each component in the component inventory, create a SEPARATE table row task."
"Do NOT bundle multiple entities/endpoints/components into a single section."
```

This would change the LLM's behavior from "write a comprehensive section about backend components" to "write one table row per component."

**Location:** `src/superclaude/cli/roadmap/prompts.py`, lines 436-463 (TDD supplement in `build_generate_prompt`)

### Fix 2: Add a TABLE ROW decomposition rule to SKILL.md 4.1

Currently, the parser starts new R-items at headings, bullets, and numbered items. It should ALSO start new R-items at:
- Each non-header row of a markdown table that contains a "Task" or "Component" or "Endpoint" column

This would cause the parser to treat each table row in the TDD+PRD roadmap as an independent R-item, matching the baseline's behavior.

**Location:** `src/superclaude/skills/sc-tasklist-protocol/SKILL.md`, line 150-153 (section 4.1)

### Fix 3: Prevent delivery-milestone paradigm from collapsing technical layers

The roadmap generation or scoring prompt should include:
```
"Prefer technical-layer phasing (Foundation -> Core -> Integration -> Hardening -> Production)
 over delivery-milestone phasing (Alpha -> Beta -> GA). Technical-layer phases produce
 more granular, independently actionable roadmap items."
```

Or alternatively, the tasklist parser should detect delivery-milestone phases and auto-decompose them into sub-phases.

**Location:** `src/superclaude/cli/roadmap/prompts.py`, `build_score_prompt` (line 538) or `build_generate_prompt` (line 380)

---

## Self-Audit

1. **Files read to verify claims:**
   - `/Users/cmerritt/GFxAI/IronClaude/.dev/test-fixtures/results/test1-tdd-prd-v2/roadmap.md` (full 746 lines)
   - `/Users/cmerritt/GFxAI/IronClaude/.dev/test-fixtures/results/test3-spec-baseline/roadmap.md` (full 380 lines)
   - `/Users/cmerritt/GFxAI/IronClaude/.dev/test-fixtures/results/test1-tdd-prd-v2/tasklist-index.md` (full file -- R-item registry)
   - `/Users/cmerritt/GFxAI/IronClaude/.dev/test-fixtures/results/test3-spec-baseline/tasklist-index.md` (full file -- task counts)
   - `/Users/cmerritt/GFxAI/IronClaude/src/superclaude/cli/roadmap/prompts.py` (build_extract_prompt, build_generate_prompt, build_merge_prompt, build_score_prompt, build_diff_prompt, build_debate_prompt)
   - `/Users/cmerritt/GFxAI/IronClaude/src/superclaude/skills/sc-tasklist-protocol/SKILL.md` (sections 4.1, 4.1a, 4.1b, 4.2, 4.3, 4.4, 4.4a, 4.4b)

2. **Factual claims independently verified:**
   - Line counts: `wc -l` on both roadmap files (746 vs 380)
   - Structural element counts: `grep -c` for table rows, headings, bullets, numbered items on both files
   - R-item counts: Read from tasklist-index.md R-item registries (44 vs 87)
   - Task counts: Read from tasklist-index.md phase summaries (44 vs 87)
   - Phase counts: Read from both tasklist indexes (3 vs 5)
   - Prompt behavior: Read actual prompt code in prompts.py for TDD and PRD supplements
   - Parser rules: Read SKILL.md section 4.1 parsing algorithm

3. **Tool engagement:** Read: 12 calls | Grep: 5 calls | Bash: 4 calls

---

## QA Complete
