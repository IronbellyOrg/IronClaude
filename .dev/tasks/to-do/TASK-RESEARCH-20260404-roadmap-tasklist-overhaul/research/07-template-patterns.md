# 07 - Existing Template Patterns Analysis

**Status**: Complete
**Investigator**: Pattern Investigator
**Date**: 2026-04-04
**Research Question**: What structural patterns in existing templates (TDD, PRD, Release Spec, MDTM) can inform the design of roadmap and tasklist output templates?

---

## Templates Under Analysis

| Template | Location | Size | Sections | Purpose |
|----------|----------|------|----------|---------|
| TDD Template | `src/superclaude/examples/tdd_template.md` | ~1335 lines | 28 numbered + appendices | Technical Design Document |
| Release Spec Template | `src/superclaude/examples/release-spec-template.md` | ~265 lines | 12 + 2 appendices | Release specification |
| PRD Template | `src/superclaude/examples/prd_template.md` | ~800+ lines | 28 numbered | Product Requirements Document |
| MDTM Complex Task | `.claude/templates/workflow/02_mdtm_template_complex_task.md` | ~1198 lines | PART 1 (13 sections A-M) + PART 2 (task body) | Task execution with handoff patterns |

---

## Template 1: TDD Template (`tdd_template.md`)

### Structure

**Frontmatter (lines 1-52):** Rich YAML frontmatter with 30+ fields including `id`, `title`, `status`, `type`, `priority`, `feature_id`, `spec_type`, `complexity_score`, `complexity_class`, `target_release`, `quality_scores` (sub-fields: clarity, completeness, testability, consistency, overall), `depends_on`, `related_docs`, `tags`, `review_info`, and `approvers`.

**Header Block (lines 54-59):** WHAT / WHY / HOW TO USE triple that establishes document purpose in one glance.

**Sentinel Self-Check (lines 60-68):** Machine-verifiable validation rules that can be run before pipeline consumption. Specifies which frontmatter fields must not retain placeholder values, and which fields are computed by downstream tools versus authored manually. Also documents which downstream pipeline steps consume which fields.

**Completeness Checklist (lines 119-149):** A top-level checkbox list enumerating every section, enabling a reviewer to track which sections are populated. This is a structural enforcement mechanism.

**Contract Table (lines 151-159):** Documents upstream/downstream relationships (what feeds this doc, what this doc feeds into, who to notify on change). Explicit dependency declaration.

**28 Numbered Sections (lines 163-1270):** Each section follows a consistent pattern:
- Section title with number
- Guidance block (blockquote or comment) explaining what goes here
- Table(s) with placeholder columns
- Code blocks where applicable
- Conditional markers `*(if applicable)*` or `[CONDITIONAL: ...]` for sections that only apply to certain spec types

**HTML Comments at Bottom (lines 1283-1335):** Metadata block containing:
- Line budget per tier (Lightweight: 300-500, Standard: 800-1200, Heavyweight: 1200-1800)
- Content rules table (Do/Don't for TDD vs PRD vs Tech Ref)
- File naming convention
- Callout conventions
- Template version and provenance

### Key Patterns Identified

1. **Tiered Usage Model**: Three tiers (Lightweight / Standard / Heavyweight) with explicit section requirements per tier. This prevents over-engineering for small tasks while ensuring completeness for large ones.

2. **Placeholder Convention**: Uses `[bracketed text]` for fill-in-the-blank placeholders. Not machine-parseable sentinels, but human-readable guidance.

3. **Table-Heavy Structure**: Nearly every section uses markdown tables as the primary content format. Tables enforce column structure and prevent prose drift.

4. **Conditional Sections**: Sections marked with `*(if applicable)*` or specific spec-type conditions (e.g., "CONDITIONAL: refactoring, portification") allow template reuse across document types.

5. **Guidance Blocks**: Every section includes either a blockquote or HTML comment explaining what to put there, who should fill it, and how it differs from other documents.

6. **Cross-Reference Links**: Explicit links to related templates (PRD, Tech Reference) at the bottom.

7. **Version Provenance**: Template version, creation date, update date, and the design doc standards it's based on (Google Design Docs, Stripe API Governance, etc.).

8. **Line Budget Enforcement**: Explicit line count targets per tier, with the warning "If a document exceeds the tier ceiling, it needs editing -- not a larger tier."

### Relevance to Roadmap/Tasklist Templates

- The **tiered usage model** is directly applicable to roadmaps (simple feature vs. multi-phase platform overhaul).
- The **completeness checklist** pattern could enforce minimum section requirements in roadmap output.
- The **contract table** pattern (upstream/downstream) maps directly to the spec-to-roadmap-to-tasklist pipeline.
- The **sentinel self-check** pattern with machine-verifiable rules should be adopted for roadmap output validation.
- The **line budget** concept could prevent roadmaps from being either too thin or too bloated.

---

## Template 2: Release Spec Template (`release-spec-template.md`)

### Structure

**Usage Block (lines 1-16):** Detailed usage instructions including:
- Supported spec types (new feature, refactoring, portification, infrastructure)
- Conditional section mapping per spec type
- Quality gate command to run before submission
- Sentinel self-check command (`grep -c '{{SC_PLACEHOLDER:' <output-file>` should return 0)

**YAML Frontmatter Block (lines 19-39):** Embedded in a code fence, with `{{SC_PLACEHOLDER:*}}` sentinels for every field. Quality scores sub-fields included.

**12 Numbered Sections + 2 Appendices (lines 41-260):** Compact structure with:
- Problem Statement with Evidence table and Scope Boundary
- Solution Overview with Key Design Decisions table
- Functional Requirements with numbered FR-IDs and acceptance criteria checkboxes
- Architecture (New Files, Modified Files, Removed Files tables, Implementation Order)
- Interface Contracts (CLI Surface, Gate Criteria, Phase Contracts)
- NFRs, Risks, Test Plan (Unit/Integration/E2E)
- Migration & Rollout
- Downstream Inputs (explicit "For sc:roadmap" and "For sc:tasklist" sections)
- Open Items, Brainstorm Gap Analysis
- Glossary and References appendices

### Key Patterns Identified

1. **Machine-Parseable Sentinels**: `{{SC_PLACEHOLDER:descriptive_name}}` format. Unlike the TDD's `[bracketed]` style, this is grep-able and can be validated programmatically. The sentinel names are descriptive (e.g., `{{SC_PLACEHOLDER:spec_title}}`, `{{SC_PLACEHOLDER:0.0_to_1.0}}`).

2. **Conditional Section Tags**: Explicit `[CONDITIONAL: spec_type_list]` markers on section headers, enabling programmatic template pruning.

3. **Downstream Inputs Section (Section 10)**: Explicitly documents how this spec feeds into `sc:roadmap` and `sc:tasklist`. This is a pipeline-aware template design -- it knows it's part of a chain.

4. **Acceptance Criteria as Checkboxes**: `- [ ] criterion` format within functional requirements, making them checkable.

5. **Compact Design**: At ~260 lines, this is the most concise template. Every line earns its place. Tables dominate; prose is minimal.

6. **Quality Gate Integration**: The template header specifies the exact command to validate it (`/sc:spec-panel --focus correctness,architecture`).

### Relevance to Roadmap/Tasklist Templates

- The **`{{SC_PLACEHOLDER:*}}`** sentinel pattern is the strongest candidate for roadmap/tasklist output templates. It enables programmatic validation (zero remaining sentinels = complete document).
- The **downstream inputs section** pattern should be inverted for roadmap output: a roadmap template should have an "Upstream Source" section declaring what spec it was generated from.
- The **conditional section** pattern can accommodate different roadmap complexities (single-spec vs. multi-spec).
- The **compact design** is a model for tasklist output templates, which should be dense and actionable rather than expansive.

---

## Template 3: PRD Template (`prd_template.md`)

### Structure

**Frontmatter (lines 1-40):** Similar to TDD but product-focused. Includes `task_type: "static"` field and `ai_model`/`model_settings` fields (empty placeholders).

**Header Block (lines 42-47):** Same WHAT / WHY / HOW TO USE triple as TDD.

**Document Lifecycle Position (lines 49-55):** Table showing where this document sits in the Requirements -> Design -> Implementation chain. Same pattern as TDD.

**Tiered Usage (lines 57-63):** Three tiers (Lightweight / Standard / Heavyweight) with "Sections to Skip" column rather than "Sections Required" -- inverse framing vs. TDD.

**Completeness Status (lines 92-117):** Grouped checkbox list (sections bundled by theme) plus Contract Table.

**28 Numbered Sections:** Same depth as TDD but product-oriented:
- Sections 1-5: Executive Summary, Problem, Background, Vision, Business Context
- Sections 6-9: JTBD, Personas, Value Proposition Canvas, Competitive Analysis
- Sections 10-13: Assumptions, Dependencies, Scope, Open Questions
- Sections 14-15: Technical Requirements, Technology Stack
- Sections 16-18: UX, Legal/Compliance, Business Requirements
- Sections 19-20: Success Metrics, Risk Analysis
- Section 21: Implementation Plan (Epics/Stories, Product Reqs, Phasing, DoD, Timeline)
- Sections 22-25: Customer Journey, Error Handling, Design, API Contracts
- Sections 26-28: Contributors, Related Resources, Maintenance & Ownership

### Key Patterns Identified

1. **SCOPE NOTE Comments**: HTML comments at the top of certain sections that explain how to adapt the section for different PRD types (product PRD vs. feature/component PRD). Example: `<!-- SCOPE NOTE: For feature/component PRDs, skip market sizing... -->`. This is more sophisticated than the TDD's conditional markers.

2. **Persona-Driven Structure**: Sections 6-9 (JTBD, Personas, Value Proposition Canvas, Competitive Analysis) use structured templates with prescribed attributes per entry.

3. **Structured Quote Patterns**: Each persona includes `**Quote:** "[Representative quote]"` and `**A Day in Their Life:**` -- forcing concrete characterization rather than abstract descriptions.

4. **Anti-Persona Section**: Section 7.4 explicitly defines who the product is NOT for.

5. **Living Document Declaration**: Contract table includes `**Living Document** | This PRD evolves as the product learns and iterates`.

6. **Framework References**: Sections reference specific frameworks (Jobs To Be Done, Value Proposition Canvas) with brief explanations of the framework.

### Relevance to Roadmap/Tasklist Templates

- The **SCOPE NOTE** comment pattern is more flexible than conditional section tags for roadmap templates, allowing guidance to vary by context without removing sections entirely.
- The **anti-pattern** concept (anti-personas) could translate to "Anti-Requirements" or "Out of Scope" sections in roadmap output, preventing scope creep.
- The **living document** concept is relevant for roadmaps that evolve across iterations.

---

## Template 4: MDTM Complex Task Template (`02_mdtm_template_complex_task.md`)

### PART 1 / PART 2 Architecture

This is the most structurally innovative template. It uses a **dual-audience architecture**:

**PART 1: Task Building Instructions (lines 46-870)**
- Audience: The orchestrator/task builder agent that creates tasks
- Wrapped entirely in an HTML comment (`<!-- ... -->`) so it's invisible to the worker agent executing the task
- Contains 13 lettered sections (A through M) of prescriptive rules
- Purpose: Ensure every task created from this template is structurally sound

**PART 2: Task File Template (lines 878-1198)**
- Audience: The worker agent executing the task
- The actual template that gets copied and populated
- Contains executable phases with checklist items
- Purpose: The artifact the worker agent reads and executes

**Boundary**: A prominent ASCII-art separator block marks the transition between PART 1 and PART 2. Within PART 2, orchestrator instruction blocks are wrapped in `<!-- ORCHESTRATOR: ... -->` HTML comments.

### PART 1 Section Analysis

| Section | Name | Lines | Purpose |
|---------|------|-------|---------|
| A | Core Principles | 6 rules | Workflow document checks, granularity requirements |
| B | Self-Contained Checklist Items | 7 rules + examples | The most critical section -- defines the 6-element pattern for every checklist item |
| C | Embedding Requirements | 4 rules | What NOT to make into separate sections |
| D | Mandatory Task Sections | 3 rules | What every task must include |
| E | Checklist Structure Rules | 4 rule groups | Checkbox format, sequential order, parent-child rules |
| F | Execution Requirements | 5 rules | The READ-IDENTIFY-EXECUTE-UPDATE-REPEAT loop |
| G | Context for Headless Agents | 4 rules | How to handle agents without framework context |
| H | Tool Specification | 4 rules | When to specify tools vs. let model choose |
| I | Additional Guidelines | 18 rules (I1-I18) | Directive language, granularity, dynamic content, QA gates, testing |
| J | Error Handling | 3 rules | The error pattern for checklist items |
| K | Example Patterns | 2 patterns | File-by-file and multi-item processing |
| L | Intra-Task Handoff Patterns | 7 patterns (L1-L7) | Discovery, Build, Test, Review, Conditional, Aggregation + selection guide |
| M | Phase-Gate Composite Patterns | 2 patterns (M1-M2) | QA gate sequences between phases |

### PART 2 Structure

1. **Task Title + Overview + Key Objectives**: High-level framing
2. **Prerequisites & Dependencies**: Parent task, blocking deps, previous stage outputs, handoff file convention, frontmatter update protocol
3. **Detailed Task Instructions** (with embedded orchestrator instruction block)
4. **Phase 1: Preparation and Setup**: Status update, directory creation, context file listing
5. **Phase 2: Main Execution**: Placeholder steps using L-patterns (Discovery -> Build -> Test -> Assess)
6. **Phase Gate: Quality Verification**: QA agent spawn placeholder
7. **Phase N: Testing & Verification**: Test execution placeholder
8. **Phase 3: Review and Quality Assessment**: Review + Aggregation
9. **Post-Completion Actions**: 4 items (verify outputs exist, run tests, create summary, update frontmatter)
10. **Task Log / Notes**: Structured sections for Task Summary, Execution Log, Phase Findings (per phase), Phase Gate Findings, Follow-Up Items, Deviations from Process

### Key Patterns Identified

1. **PART 1 / PART 2 Separation**: Instructions for the template user (how to build) are physically separated from the template output (what gets produced). This prevents instruction leakage into output.

2. **6-Element Checklist Item Pattern (B2)**: Every checklist item must contain:
   - Context Reference + WHY
   - Action + WHY
   - Output Specification
   - Integrated Verification ("ensuring..." clause)
   - Evidence on Failure Only
   - Explicit Completion Gate

3. **Anti-Pattern Documentation**: Section B5 explicitly lists FORBIDDEN patterns with examples, not just what to do but what NOT to do.

4. **Handoff File Convention**: Standardized directory structure for inter-item communication (`phase-outputs/discovery/`, `test-results/`, `reviews/`, `plans/`, `reports/`).

5. **Phase Gate Enforcement (I15-I16, M1-M2)**: Codified QA checkpoints between phases with fix cycle limits per gate type and escalation rules.

6. **Self-Containment Principle**: Each checklist item is a complete, self-contained prompt that can execute independently across session rollovers. This is the most important design principle for AI-agent-consumed templates.

7. **Embedded Orchestrator Blocks in PART 2**: Within the output template, `<!-- ORCHESTRATOR: ... -->` comments provide build-time guidance that is stripped from the worker's view.

### Relevance to Roadmap/Tasklist Templates

- The **PART 1 / PART 2 pattern** is the strongest candidate for roadmap and tasklist output templates. PART 1 would contain the generation rules (for the LLM generating the roadmap), and PART 2 would be the output structure (what the roadmap must look like).
- The **self-containment principle** applies to tasklist items: each task in a tasklist should carry enough context to be executed without referring back to the roadmap.
- The **handoff file convention** establishes a naming and directory pattern that tasklist output could follow.
- The **phase gate** concept maps to milestone validation in roadmaps.
- The **anti-pattern documentation** should be included in roadmap/tasklist templates to prevent known failure modes (e.g., tasks that are too coarse, milestones without acceptance criteria).

---

## Cross-Template Pattern Synthesis

### Pattern 1: Frontmatter Schemas

| Template | Frontmatter Style | Machine-Readable? | Pipeline Consumption? |
|----------|-------------------|--------------------|-----------------------|
| TDD | Rich YAML, 30+ fields | Yes | Partially (complexity fields computed externally) |
| Release Spec | YAML with `{{SC_PLACEHOLDER:*}}` sentinels | Yes, grep-validated | Yes (fields consumed by spec-panel, roadmap) |
| PRD | Rich YAML, 40+ fields | Yes | Not documented |
| MDTM | YAML with placeholder text | Yes | Yes (status, dates consumed by orchestrator) |

**Finding**: Roadmap and tasklist output templates MUST have YAML frontmatter. The Release Spec's sentinel pattern (`{{SC_PLACEHOLDER:*}}`) is the strongest for validation. The TDD's pipeline consumption documentation (which fields are consumed by which downstream step) should be adopted.

### Pattern 2: Section Enforcement Mechanisms

| Mechanism | Used By | Enforcement Level |
|-----------|---------|-------------------|
| Completeness checklist at top | TDD, PRD | Human review |
| Sentinel self-check (grep) | Release Spec | Automated |
| Line budget per tier | TDD | Human review |
| Phase-gate QA agents | MDTM | Agent-automated |
| Tiered usage (required sections per tier) | TDD, PRD | Human judgment |
| Conditional section markers | Release Spec, TDD | Human/tooling |

**Finding**: Roadmap output templates need multiple enforcement layers: a completeness checklist (for human review), sentinel checks (for automated validation), and structural validation rules (for the `superclaude roadmap validate` CLI command).

### Pattern 3: Placeholder Conventions

| Convention | Template | Example | Pros | Cons |
|------------|----------|---------|------|------|
| `[bracketed guidance]` | TDD, PRD | `[Component Name]` | Human-readable | Not machine-parseable |
| `{{SC_PLACEHOLDER:name}}` | Release Spec | `{{SC_PLACEHOLDER:spec_title}}` | Grep-able, descriptive | Verbose |
| `[PLACEHOLDER-STYLE]` | MDTM frontmatter | `[AGENT-NAME]` | Readable | Not consistently formatted |

**Finding**: Use `{{SC_PLACEHOLDER:*}}` for fields that must be programmatically validated (frontmatter, key structural elements). Use `[bracketed guidance]` for content areas where the author needs flexibility.

### Pattern 4: Instruction vs. Output Separation

| Template | Separation Method | Effectiveness |
|----------|-------------------|---------------|
| TDD | Guidance blockquotes within sections | Moderate -- guidance mixed with output structure |
| Release Spec | Usage block at top, removed from final | Good -- clear separation |
| PRD | SCOPE NOTE HTML comments | Good -- invisible in rendered markdown |
| MDTM | PART 1/PART 2 with HTML comments | Excellent -- complete physical separation |

**Finding**: The MDTM PART 1/PART 2 pattern provides the cleanest separation. For roadmap/tasklist output templates, this pattern allows the generation instructions (prompt engineering) to live in the same file as the output structure, without risk of instruction leakage.

### Pattern 5: Downstream Awareness

| Template | Awareness of Pipeline Position | Mechanism |
|----------|-------------------------------|-----------|
| TDD | High | Pipeline field consumption docs, "Feeds to" contract table |
| Release Spec | High | Explicit "For sc:roadmap" and "For sc:tasklist" sections |
| PRD | Medium | Contract table with downstream references |
| MDTM | High | Previous Stage Outputs section, handoff file convention |

**Finding**: Every template in this codebase documents its position in the pipeline. Roadmap and tasklist output templates must do the same: a roadmap must declare what spec(s) it was generated from (upstream) and what tasklist(s) it feeds (downstream). A tasklist must declare its source roadmap.

---

## Gaps and Questions

### Gaps Identified

1. **No Existing Roadmap Output Template**: The `sc:roadmap-protocol` skill generates roadmaps, but there is no template defining what the output must look like. The roadmap structure is entirely inference-dependent -- whatever the LLM produces on a given run is what you get.

2. **No Existing Tasklist Output Template**: Similarly, `sc:tasklist-protocol` has no output template. The tasklist bundle format is defined by convention in the skill's behavioral rules, but not enforced by a template.

3. **No Sentinel Validation for Pipeline Artifacts**: The Release Spec has `grep -c '{{SC_PLACEHOLDER:'` validation, but no equivalent exists for roadmap or tasklist output. The `superclaude roadmap validate` CLI exists but validates against different (weaker) criteria.

4. **Template-to-Template Traceability Gap**: While templates reference each other in prose, there is no machine-readable traceability chain (spec ID -> roadmap section -> tasklist task ID). This makes fidelity validation difficult.

5. **No Anti-Pattern Documentation for Roadmap/Tasklist**: The MDTM template has extensive anti-pattern documentation (Section B5 FORBIDDEN patterns). Roadmap and tasklist generation has known anti-patterns (granularity collapse, milestone without acceptance criteria, theme without tasks) but these are not codified.

### Questions for Design Phase

1. Should roadmap and tasklist output templates use the PART 1/PART 2 pattern, or is a simpler structure sufficient given that the generation is handled by a CLI pipeline rather than a task-builder agent?

2. Should the sentinel convention be `{{SC_PLACEHOLDER:*}}` (matching Release Spec) or a roadmap-specific convention like `{{ROADMAP:*}}`?

3. How should the tiered usage model map to roadmaps? Options: (a) by spec count (single-spec vs. multi-spec), (b) by complexity class from the spec, (c) by total feature count.

4. Should the output template enforce a specific section ordering, or allow the LLM to organize sections by theme/priority?

---

## Stale Documentation Found

1. **TDD Template line 333 references "SLODLC"** in its provenance without a link or definition. This acronym is not widely known and may confuse template users.

2. **PRD Template `ai_model` and `model_settings` frontmatter fields** are present but not documented anywhere in terms of what they're used for or who consumes them. They appear to be dead fields.

3. **Release Spec references `/sc:spec-panel --focus correctness,architecture` and `/sc:spec-panel --mode critique`** as quality gates, but these appear to be inference-time commands that may not exist as CLI-invocable commands. The actual validation pathway is unclear.

---

## Summary

### Top 5 Design Principles for Roadmap/Tasklist Output Templates

1. **Adopt the PART 1 / PART 2 pattern from the MDTM template.** PART 1 contains generation instructions (what the LLM must produce, anti-patterns to avoid, structural rules). PART 2 is the output skeleton with sentinels. This prevents instruction leakage and enables the same file to serve as both prompt and schema.

2. **Use `{{SC_PLACEHOLDER:*}}` sentinels for all required fields.** This is the only convention in the codebase that enables automated validation. Combine with a sentinel self-check command in the template header.

3. **Enforce minimum structure with tables, not prose.** All four templates use tables as the primary structural enforcement mechanism. Tables prevent granularity collapse because every row must have values for every column. A roadmap milestone table with columns like `| Milestone | Themes | Tasks | Acceptance Criteria | Dependencies |` prevents the failure mode where milestones are listed without supporting detail.

4. **Include a completeness checklist and contract table.** The TDD/PRD pattern of a top-level completeness checklist enables both human review and automated checking. The contract table (upstream spec, downstream tasklist) enforces pipeline awareness.

5. **Document anti-patterns explicitly.** Following the MDTM Section B5 pattern, include a FORBIDDEN section in the roadmap template's PART 1 that lists known failure modes: tasks without acceptance criteria, milestones without task decomposition, themes that don't trace to spec requirements, granularity that collapses multi-step work into single items.

### Recommended Template Structure for Roadmap Output

```
PART 1: Generation Instructions (HTML comment)
  - Structural rules (required sections, minimum content)
  - Table format requirements (columns per table type)
  - Anti-patterns (FORBIDDEN section)
  - Sentinel convention
  - Downstream contract (what sc:tasklist expects)

PART 2: Roadmap Output Template
  - YAML frontmatter (source spec, complexity, feature count, version)
  - Completeness Checklist
  - Contract Table (upstream spec, downstream tasklist)
  - Executive Summary
  - Themes (table: Theme ID, Name, Spec Sections, Description)
  - Milestones (table: Milestone ID, Name, Themes, Acceptance Criteria, Dependencies)
  - Task Decomposition per Milestone (table: Task ID, Name, Milestone, Complexity, Dependencies, Files)
  - Dependency Graph (text or mermaid)
  - Risk Assessment
  - Implementation Order
  - Sentinel Self-Check command
```

### Recommended Template Structure for Tasklist Output

```
PART 1: Generation Instructions (HTML comment)
  - Self-containment rules (each task must be independently executable)
  - Granularity requirements (maximum scope per task)
  - Dependency encoding rules
  - Sprint CLI compatibility requirements
  - Anti-patterns (FORBIDDEN section)

PART 2: Tasklist Index Template
  - YAML frontmatter (source roadmap, milestone ID, task count)
  - Completeness Checklist
  - Contract Table (upstream roadmap, downstream sprint execution)
  - Task Table (table: Task ID, Name, Type, Complexity, Dependencies, Status)
  - Per-Task Detail Sections (or separate files per the MDTM convention)
  - Validation command
```
