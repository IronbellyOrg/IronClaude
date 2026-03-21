---
finding_id: F2
status: analyzed
root_cause: "Opus architect agent defaulted to table format for structured task data; merge step preserved Opus tables as-is because Opus was selected as base variant"
recommended_fix: "Convert table rows to numbered task items in-place, preserving all cell data as inline annotations"
---

# F2: Table-Based Tasks Not Splitter-Parseable — Analysis

## 1. Evidence Summary

### 1.1 Merged Roadmap (roadmap.md) — TABLE FORMAT

All 7 phase sections encode tasks as Markdown table rows:

- **Phase 0** (lines 36-42): `| Task | Requirements | Description | Parallel? |` — 5 rows (T0.1-T0.5)
- **Phase 1** (lines 57-64): Same schema — 6 rows (T1.1-T1.6)
- **Phase 2** (lines 78-85): Same schema — 6 rows (T2.1-T2.6)
- **Phase 3** (lines 111-116): Same schema — 4 rows (T3.1-T3.4)
- **Phase 4** (lines 146-152): Same schema — 5 rows (T4.1-T4.5)
- **Phase 5** (lines 180-187): Same schema — 6 rows (T5.1-T5.6)
- **Phase 6** (lines 221-226): Same schema — 4 rows (T6.1-T6.4)

Total: 36 task rows across 7 tables.

### 1.2 Opus Architect Variant (roadmap-opus-architect.md) — TABLE FORMAT

Same `| Task | Requirements | Description | Parallel? |` table schema in all phases:

- Phase 0 (lines 28-33): 3 rows (T0.1-T0.3)
- Phase 1 (lines 45-52): 6 rows (T1.1-T1.6)
- Phase 2 (lines 62-69): 6 rows (T2.1-T2.6)
- Phase 3 (lines 80-85): 4 rows (T3.1-T3.4)
- Phase 4 (lines 106-114): 7 rows (T4.0-T4.6)
- Phase 5 (lines 131-138): 6 rows (T5.1-T5.6)
- Phase 6 (lines 162-167): 4 rows (T6.1-T6.4)

### 1.3 Haiku Analyzer Variant (roadmap-haiku-analyzer.md) — LIST FORMAT

Uses `#### Tasks` subheadings with numbered list items:

- Phase 0, Milestone 0.1 (line 79): `1. Upgrade and pin...` / `2. Validate import...` / `3. Run unchanged...` / `4. Preserve exact...`
- Phase 1, Milestone 1.2 (line 95): `1. Execute ONE-WAY DOOR...` / `2. Update all six...` / `3. Update init.sql...` / `4. Verify:...`
- Phase 1, Milestone 1.3 (line 116): `1. Fix config defaults...` / `2. Update CI...` / `3. Validate compose...` / `4. Confirm Redis...`
- Pattern continues through all phases with numbered lists under `#### Tasks` headings.

### 1.4 Release Spec (release-spec-ontrag-r0-r1.md) — CODE BLOCK + NUMBERED LIST

Implementation order (lines 389-417) uses a code block with numbered tasks:
```
1.  Task 1:  Dependency resolution spike
2.  Task 2:  Update requirements.txt
...
21. Task 20: Write R1 test suite (11 tests)
```

### 1.5 Downstream Consumer Expectation

From `validation-report.md:39`: "`sc:tasklist` splitter expects headings + bullets/numbered/checklist items."

The existing tasklist from a prior roadmap (`.dev/releases/past/devops-analysis/analysis/tasklist/tasklist.md:30-31`) confirms: "Phase buckets derived from explicit 'Phase 0' through 'Phase 8' headings in roadmap" and "Milestones converted to tasks 1:1."

### 1.6 Base Selection Decision

From `base-selection.md:2-3`: `base_variant: "Opus (architect)"`. Opus was selected as base due to superior task-level actionability (C2: 10/10 vs Haiku 5/10) and parallelism mapping (C4: 9/10 vs Haiku 3/10). The table format was integral to these high scores — the `Parallel?` column is what earned C4 points.

---

## 2. Root Cause Analysis — Three Proposed Causes

### Root Cause 1 (RC1): The Opus architect agent defaulted to tables for structured task data

**Hypothesis**: The Opus architect persona, when generating roadmaps, naturally produces Markdown tables for task lists because tables efficiently encode multi-dimensional data (task ID, requirements, description, parallelism). This is an LLM output preference, not a prompt-driven format.

### Root Cause 2 (RC2): The spec itself uses structured task encoding, causing the generator to mirror the format

**Hypothesis**: The release spec (`release-spec-ontrag-r0-r1.md`) Section 4.6 encodes implementation order as a structured numbered list with embedded dependency annotations. The roadmap generator adopted a structured format (tables) to preserve the multi-field nature of each task item.

### Root Cause 3 (RC3): The merge step preserved Opus tables without format conversion

**Hypothesis**: The merge step selected Opus as base variant and incorporated Haiku's semantic improvements (F6 timing, concern-aligned gates), but did not convert the base variant's table format to a splitter-compatible format. There was no format conversion requirement in the merge process.

---

## 3. Root Cause Debate Transcript

### RC1 Debate: Opus architect agent defaulted to tables

**Prosecution**:
The Opus architect variant (`roadmap-opus-architect.md`) uses tables in every single phase section without exception (lines 28, 45, 62, 80, 106, 131, 162). The Haiku analyzer variant (`roadmap-haiku-analyzer.md`) uses numbered lists under `#### Tasks` headings. This proves the table format is an Opus-specific output pattern, not a universal requirement. The two agents received the same spec input but produced different output formats. The format choice was agent-dependent.

Furthermore, `base-selection.md:49` explicitly notes: "7 phases with flat task lists. Each phase has a single objective, a task table, and a milestone." The evaluator described Opus's output as "a task table" — confirming this was recognized as a format choice, not a requirement.

**Defense**:
The Opus agent may have chosen tables because the roadmap generation prompt asked for parallelism annotations and requirement traceability per task. Tables are the natural Markdown structure for multi-column data. If the prompt had specified "use numbered lists with inline annotations," Opus would likely have complied. The root cause is not "Opus defaults to tables" but "the prompt did not constrain the format."

**Rebuttal**:
The defense concedes the core claim: Opus produced tables. Whether the prompt should have constrained the format is a separate question (addressed in RC3). The fact remains that Opus's output preference is the proximate cause of the table format appearing in the roadmap. The prompt's lack of constraint is a contributing factor, not an alternative root cause.

**Verdict**: LIKELY — Opus's table preference is the proximate cause of the format. Evidence is direct and unambiguous.

---

### RC2 Debate: Spec format caused generator to mirror tables

**Prosecution**:
The release spec Section 4.6 (`release-spec-ontrag-r0-r1.md:389-417`) uses a structured numbered list inside a code block with embedded dependency annotations (e.g., `-- depends on Task 1 spike results`). This multi-field-per-task pattern could have influenced the Opus agent to encode the same information as a table rather than a flat list.

Additionally, the spec uses tables extensively elsewhere: Section 4.1 (New Files), Section 4.2 (Modified Files), Section 3 (Functional Requirements use subsections with bullet points but acceptance criteria tables). The spec's overall style is table-heavy.

**Defense**:
The spec's Section 4.6 does NOT use tables — it uses a plain numbered list inside a code block. If the generator mirrored the spec format, it would have produced numbered lists, not tables. The spec's other table usage (Sections 4.1, 4.2) is for file manifests and metadata, not for task descriptions. There is no table-formatted task list in the spec that the generator could have mirrored.

Furthermore, the Haiku analyzer received the same spec and produced numbered lists. If the spec format were the root cause, both agents would have produced the same format.

**Rebuttal**:
The prosecution's argument is weak. The spec's Section 4.6 explicitly uses numbered lists, not tables. The two agents diverging on format from the same input directly contradicts the hypothesis that spec format drove the output.

**Verdict**: UNLIKELY — The spec uses numbered lists for tasks, not tables. Both agents received the same spec but produced different formats. The spec format is not the cause.

---

### RC3 Debate: Merge step preserved tables without conversion

**Prosecution**:
The merge step selected Opus as base variant (`base-selection.md:2`). The merge incorporated Haiku's semantic improvements but explicitly preserved Opus's structural format. Evidence from `base-selection.md:49`: Opus's "flat task lists" with "task table" format was scored as a positive feature (C3: 8/10). The merged roadmap's frontmatter (`roadmap.md:7`) confirms `incorporated_from: "Haiku (analyzer) — F6 timing, concern-aligned gates, integration points, decision rules, risk cadence"`. Note: "F6 timing" and "concern-aligned gates" are semantic changes, not format changes. The merge preserved Opus's tables because the merge criteria valued task actionability (which tables delivered) over downstream parseability (which was not evaluated).

The merge process had no criterion for "downstream tool compatibility." `base-selection.md` evaluates 10 criteria (C1-C10), none of which mention `sc:tasklist` splitter compatibility or output format requirements for downstream consumption.

**Defense**:
The merge step did exactly what it was designed to do — select the best variant and incorporate improvements from the other. Format conversion was not in scope for the merge step. The root cause is not "the merge failed to convert" but "no stage in the pipeline checked for downstream format compatibility." Blaming the merge step is misdirected — the gap is in the pipeline design, not the merge execution.

**Rebuttal**:
The defense is partially correct: the pipeline design lacks a format compatibility check. However, the merge step is the LAST opportunity to catch and fix format issues before the roadmap is finalized. The merge step's failure to include format conversion is the proximate cause of the final roadmap having tables. The pipeline design gap is the systemic root cause, but the merge step is where the fix should have applied.

**Verdict**: LIKELY (contributing cause) — The merge step preserved tables because its evaluation criteria did not include downstream parseability. This is accurate but is a contributing factor rather than the primary cause.

---

### Most Likely Root Cause Declaration

**PRIMARY ROOT CAUSE: RC1 — The Opus architect agent defaulted to tables for structured task data.**

The Opus architect naturally produces Markdown tables when encoding multi-dimensional task data (ID, requirements, description, parallelism). This is the proximate cause of the table format appearing in the roadmap. The evidence is direct: Opus produced tables, Haiku produced lists, both from the same spec input.

**CONTRIBUTING CAUSE: RC3 — The merge step had no format conversion requirement.**

The merge step preserved Opus's tables because its 10 evaluation criteria (C1-C10) did not include downstream tool compatibility. This allowed the table format to persist into the final merged roadmap unchecked.

**REJECTED: RC2 — The spec format was not the cause.** The spec uses numbered lists for tasks, contradicting the hypothesis.

---

## 4. Solution Brainstorm

### Solution A: In-Place Table-to-List Conversion

Convert each phase's task table into numbered list items, preserving all cell data as inline annotations.

**Before (table)**:
```markdown
| Task | Requirements | Description | Parallel? |
|------|-------------|-------------|-----------|
| T0.1 | FR-R0.1/AC1 | Clean virtualenv spike... | No — first task |
```

**After (numbered list)**:
```markdown
1. **T0.1** [FR-R0.1/AC1] — Clean virtualenv spike... *(Sequential: first task)*
```

All data preserved. Format is splitter-compatible (numbered list under phase headings).

### Solution B: Add a Parallel/Dependency Metadata Section

Convert tables to numbered lists but move parallelism and dependency data to a separate metadata section per phase (e.g., a DAG or dependency table after the task list). Task items become simpler single-line descriptions.

**After**:
```markdown
1. **T0.1** [FR-R0.1/AC1] — Clean virtualenv spike...
2. **T0.2** [Open Question 1 (F6)] — F6 API verification spike...

**Task Dependencies**: T0.2 after T0.1; T0.3 after T0.2; T0.4 after T0.1; T0.5 after T0.4
```

### Solution C: Dual Format — Keep Tables + Add List Summary

Preserve existing tables (they contain valuable structured data) and add a splitter-compatible numbered list summary below each table. The tables serve as reference; the lists serve as splitter input.

**After**:
```markdown
| Task | Requirements | Description | Parallel? |
|------|-------------|-------------|-----------|
| T0.1 | FR-R0.1/AC1 | Clean virtualenv spike... | No |

#### Task List (splitter input)
1. **T0.1** [FR-R0.1/AC1] — Clean virtualenv spike...
```

---

## 5. Solution Debate Transcript

### Solution A Debate: In-Place Table-to-List Conversion

**Advocate**:
Solution A is the simplest and most direct fix. It converts the format that the splitter cannot parse into one it can, while preserving all information. The `Parallel?` column data becomes an inline annotation (e.g., `*(Sequential: first task)*` or `*(Parallel with T3.1)*`). The `Requirements` column becomes a bracketed prefix `[FR-R0.1/AC1]`. No data is lost. No structural changes to the document. No duplication.

This approach also aligns with how the Haiku variant already structured its tasks — numbered lists are the proven format for roadmap tasks in this pipeline.

**Critic**:
The table format provides at-a-glance scanning of parallelism and requirements across all tasks in a phase. Converting to inline annotations loses this visual structure. A developer scanning the roadmap to understand which tasks can run in parallel must now read every line instead of scanning a column. The `Parallel?` column is what earned Opus a 9/10 on C4 (parallelism mapping) in `base-selection.md:58`.

Additionally, inline annotations like `*(Sequential: first task)*` are less standardized than table cells — different tasks may format the annotation differently, creating inconsistency.

**Rebuttal**:
The visual scanning argument is valid but secondary. The primary purpose of the roadmap is to feed the tasklist pipeline — if the pipeline cannot parse the roadmap, the visual structure is moot. Furthermore, the parallelism information is also captured in the `### Parallelism Opportunities` section (`roadmap.md:416-422`) and the `### Critical Path` section (`roadmap.md:424-426`), so it is not lost even if inline annotations are less scannable than columns.

The consistency concern is addressable: define a standard annotation format (e.g., `*(Seq: after T0.1)*` or `*(Par: with T3.1)*`) and apply it uniformly.

**Verdict**: RECOMMENDED — Simplest fix, preserves all data, aligns with proven Haiku format, directly solves the splitter parseability issue.

---

### Solution B Debate: Separate Dependency Metadata Section

**Advocate**:
Solution B produces the cleanest task items — each is a single line with task ID, requirements, and description. Parallelism/dependency data moves to a dedicated section where it can be expressed as a proper DAG or dependency graph. This separates concerns: task content vs task ordering. The splitter parses task items; the executor references the dependency section.

**Critic**:
This introduces a new document structure that the splitter must also understand. If the splitter expects self-contained task items (each item has all information needed to understand it), then separating dependencies into a different section breaks self-containment. The MDTM template rules (from `SKILL.md:862-870`) require checklist items to be self-contained with "context + action + output + verification + completion gate." Splitting dependency information away from the task item violates this principle.

Furthermore, the dependency section would need its own format — if it is a table, we have reintroduced the table parseability problem. If it is a list, the information is harder to scan than inline annotations.

**Rebuttal**:
The critic raises a valid point about self-containment. However, the roadmap task items are not MDTM checklist items — they are roadmap-level tasks that will be expanded into MDTM items by `sc:tasklist`. The self-containment rule applies to the final task file, not the roadmap. The dependency section is reference metadata, not a splitter input.

That said, the added complexity of maintaining a separate dependency section (and keeping it synchronized with task items) is a real cost with limited benefit over inline annotations.

**Verdict**: ACCEPTABLE — Cleaner task items, but added structural complexity and synchronization burden outweigh the benefits. Not preferred over Solution A.

---

### Solution C Debate: Dual Format (Tables + List Summary)

**Advocate**:
Solution C preserves the tables that earned high scores on C2 (actionability: 10/10) and C4 (parallelism: 9/10) while adding the splitter-compatible format as a parallel representation. No information is lost or reformatted. Both human readers (who benefit from tables) and the splitter tool (which needs lists) are served.

**Critic**:
This is pure duplication. Every task appears twice in different formats. When a task is modified, both representations must be updated — this is a synchronization hazard. The roadmap is already long (484 lines); adding 36 duplicate task items increases it by ~50-70 lines. Duplication violates the project's "Tech Debt Prevention is Priority #1" principle and the "Simplify the codebase with every change" rule from CLAUDE.md.

The tables also become dead weight — if the splitter only reads the list items, the tables serve no functional purpose beyond human readability, which is secondary to pipeline parseability.

**Rebuttal**:
The critic's duplication argument is decisive. Maintaining two representations of the same data is exactly the kind of tech debt the project rules prohibit. The tables served their purpose during evaluation and base selection — they do not need to persist in the final roadmap.

**Verdict**: REJECTED — Duplication violates core project principles. Synchronization hazard outweighs readability benefit.

---

### Recommended Solution Declaration

**RECOMMENDED: Solution A — In-Place Table-to-List Conversion**

**Reasoning**:
1. Directly solves the splitter parseability blocker with minimal structural change
2. Preserves all data (task ID, requirements, description, parallelism) as inline annotations
3. Aligns with the proven Haiku variant format (numbered lists under phase headings)
4. No duplication, no new document sections, no synchronization hazards
5. The parallelism data that tables encoded is also captured in dedicated sections (Parallelism Opportunities, Critical Path), so the table column is not the sole source of this information

**Implementation format**:
```markdown
1. **T0.1** [FR-R0.1/AC1] — Clean virtualenv spike: upgrade `langgraph`, install `langgraph-checkpoint-postgres`, `psycopg[binary]`, `pgvector`, `numpy`. Verify `add_messages` and `AsyncPostgresSaver` imports resolve. Document coordinated version constraints (addresses Open Question 9: langchain compatibility). *(Seq: first task)*
```

**Conversion rules**:
- `Task` cell -> bold prefix `**T0.1**`
- `Requirements` cell -> bracketed `[FR-R0.1/AC1]`
- `Description` cell -> main text after em dash
- `Parallel?` cell -> italic suffix `*(Seq: ...)* ` or `*(Par: with T3.1)*`
- Tasks with `—` in Requirements column -> omit brackets or use `[admin]`
