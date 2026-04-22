---
component: "tdd-skill"
component_version: "skill-v2 (refactored decomposition)"
covers_release: "refactor/prd-skill-decompose branch"
last_updated: "2026-04-03"
author: "Claude Opus 4.6"
---

# TDD Skill — Release Guide

This guide covers the `/tdd` skill for Technical Design Document generation, including:
- what the skill does and how it works,
- when to use it,
- how to invoke it,
- practical examples with all input combinations,
- the 7-phase multi-agent pipeline architecture (with parallel investigation, QA gates, and assembly),
- tier selection and depth control,
- quality gates and validation,
- output artifacts and file structure,
- the Phase Loading Contract and ref decomposition,
- performance and cost expectations by tier,
- known limitations and gotchas,
- troubleshooting common issues,
- and how it fits into the **PRD -> TDD -> roadmap -> tasklist -> execution** workflow.

---

## 1) Release Summary (What is included)

### Core capability

The `/tdd` skill creates comprehensive Technical Design Documents by orchestrating a multi-agent investigation, synthesis, and assembly pipeline. It uses Rigorflow's MDTM task file system for persistent progress tracking — every phase and step is encoded as checklist items in a task file that survives context compression and session restarts. Can be fed from a PRD to translate product requirements into engineering specifications.

### Migration notes (refactored decomposition)

This release refactors the TDD skill from a monolithic SKILL.md into a decomposed structure with external reference files:

- **What changed**: Agent prompt templates, synthesis mapping table, validation checklists, operational guidance, and the build-request template extracted into `refs/` subdirectory files (`agent-prompts.md`, `synthesis-mapping.md`, `validation-checklists.md`, `operational-guidance.md`, `build-request-template.md`). SKILL.md now references these files via a Phase Loading Contract rather than inlining all content.
- **What broke**: Nothing — the skill's invocation surface (`/tdd [description]`) is unchanged. The decomposition is internal.
- **What to do**: If you have local modifications to a pre-decomposition SKILL.md, merge your changes into the appropriate `refs/` file or the slimmed SKILL.md. Run `make sync-dev` after any edits to `src/superclaude/skills/tdd/`.
- **What was removed**: Duplicate content that now lives in `refs/` files. The SKILL.md still contains the full behavioral protocol; only reference material was extracted.
- **What was added**: `refs/operational-guidance.md` (critical execution rules, research quality signals, artifact locations, PRD-to-TDD pipeline, update protocol, session management) and `refs/build-request-template.md` (full BUILD_REQUEST structure for the task builder). The PRD skill has no equivalent to these files — the TDD skill's build request is more complex due to the additional operational guidance and PRD-to-TDD traceability requirements.

### Architecture overview

The TDD skill operates in two stages:
- **Stage A** — Scope Discovery & Task File Creation: Maps the component architecture, plans research assignments, and spawns `rf-task-builder` to create an MDTM task file encoding all phases.
- **Stage B** — Task File Execution: Delegates to the `/task` skill, which runs the F1 execution loop over the task file's checklist items, spawning parallel subagents as specified.

The pipeline uses **parallel multi-agent investigation** to achieve deep coverage: multiple specialized agents (Architecture Analyst, Code Tracer, Data Model Analyst, API Surface Mapper, Integration Mapper, Doc Analyst) explore the codebase simultaneously, writing incremental findings to disk. QA gates at three critical points prevent quality drift.

### Skill file structure

```
src/superclaude/skills/tdd/
├── SKILL.md                          # Full skill definition and behavioral protocol
└── refs/
    ├── agent-prompts.md              # Agent prompt templates (codebase, web, synthesis, analyst, QA, assembly, PRD extraction)
    ├── synthesis-mapping.md          # TDD template section -> synthesis file mapping + output structure
    ├── validation-checklists.md      # Synthesis quality review, assembly process, validation checklist, content rules
    ├── operational-guidance.md       # Critical rules, research quality signals, artifact locations, PRD-to-TDD pipeline
    └── build-request-template.md     # Full BUILD_REQUEST template for rf-task-builder

.claude/skills/tdd/                   # Dev copy (synced from src/ via make sync-dev)
├── SKILL.md
└── refs/
    ├── agent-prompts.md
    ├── synthesis-mapping.md
    ├── validation-checklists.md
    ├── operational-guidance.md
    └── build-request-template.md
```

### Key design decisions

- **MDTM task file as execution contract**: The task file on disk is the source of truth, not conversation context. Progress survives context compression and session restarts.
- **Incremental file writing**: All agents follow the Incremental File Writing Protocol — create file immediately, append findings as discovered. Never accumulate in context and one-shot.
- **Documentation staleness protocol**: Every doc-sourced claim is tagged `[CODE-VERIFIED]`, `[CODE-CONTRADICTED]`, or `[UNVERIFIED]`. Only code-verified claims appear in Architecture, Data Models, or API Specifications sections.
- **Zero-trust QA**: Dedicated `rf-analyst` and `rf-qa` agents verify at three gates (post-research, post-synthesis, post-assembly). The QA agent assumes everything is wrong until independently verified.
- **Parallel partitioning for scale**: When file counts exceed thresholds (>6 research files, >4 synthesis files), multiple analyst/QA instances run in parallel with assigned subsets to prevent context rot.
- **Template conformance**: Output always follows `src/superclaude/examples/tdd_template.md`. The template is the schema — every TDD must conform to it.
- **Phase Loading Contract**: Each phase has declared and forbidden `refs/` file loads. The orchestrator loads `refs/build-request-template.md` only at A.7; the builder loads the other 4 refs files. No phase may load a refs file listed in its Forbidden Loads column.
- **Ref decomposition with 5 files**: Unlike the PRD skill (3 refs files), the TDD skill uses 5 refs files — the additional `operational-guidance.md` and `build-request-template.md` support the more complex build request and PRD-to-TDD traceability pipeline.

---

## 2) Invocation Reference — When and How to Use

### `/tdd`

#### What it does

Performs scope discovery on a component, service, or system; creates an MDTM task file encoding the full investigation/synthesis/assembly pipeline; then delegates execution to `/task` for multi-agent parallel execution with QA gates. Produces a TDD conforming to the project's TDD template.

#### Use when

- You need a comprehensive technical design document for a component, service, or system.
- You want evidence-based design specifications grounded in actual codebase state.
- You want multi-agent parallel investigation for deep architectural coverage.
- You want persistent progress tracking that survives session restarts.
- You want to translate a PRD into engineering specifications (PRD-to-TDD pipeline).
- You want to feed the TDD into downstream `/sc:roadmap` or implementation task workflows.

#### Syntax

```
/tdd [description of what to design]
```

#### Input requirements

The skill needs four pieces of information. The first is mandatory; the rest improve quality:

| Input | Required | Description |
|-------|----------|-------------|
| **WHAT** | Yes | Component, service, or system to create a technical design for — not just a topic name |
| **PRD_REF** | Strongly recommended | Path to a PRD that this TDD implements (provides requirements traceability) |
| **WHERE** | Optional | Specific directories, files, or subsystems to focus on (saves significant time) |
| **OUTPUT** | Optional | Where the final TDD goes (existing stub or new location; default: `docs/[domain]/TDD_[COMPONENT-NAME].md`) |

#### Examples

```
# Strong — all four inputs
/tdd Create a TDD for the agent orchestration system. The PRD is at
docs/docs-product/tech/agents/PRD_AGENT_SYSTEM.md. Focus on
backend/app/agents/, backend/app/services/agent_service.py, and
backend/app/workers/. Write to docs/agents/TDD_AGENT_ORCHESTRATION.md.

# Strong — clear scope + PRD + tier
/tdd Turn the canvas roadmap PRD into a TDD. The PRD is at
docs/docs-product/tech/canvas/PRD_ROADMAP_CANVAS.md. Standard-tier
design covering the React canvas system, dependency management, and
node type architecture. Focus on frontend/app/roadmap/.

# Strong — new system design from scratch
/tdd Design the technical architecture for a shared GPU pool to replace
per-session VMs. Scope: ue_manager/, infrastructure/,
backend/app/services/streaming_service.py. This is a Heavyweight TDD —
new system, cross-team impact.

# Minimal — topic only (broader, less focused output)
/tdd Create a TDD for the wizard.
```

---

## 3) The 7-Phase Multi-Agent Pipeline

The TDD pipeline generates a comprehensive technical design document through parallel multi-agent investigation, synthesis, and assembly with QA gates at three critical points.

### Pipeline overview

```
Stage A: Scope Discovery (orchestrator)
  A.1: Check for existing task file
  A.2: Parse & triage TDD request (Scenario A vs B)
  A.3: Perform scope discovery (Glob, Grep, codebase-retrieval)
  A.4: Write research notes file (8 categories)
  A.5: Review research sufficiency (MANDATORY GATE)
  A.6: Template triage (01 or 02)
  A.7: Load refs/build-request-template.md, spawn rf-task-builder
       Builder loads: refs/agent-prompts.md, refs/synthesis-mapping.md,
                      refs/validation-checklists.md, refs/operational-guidance.md
  A.8: Verify task file
       |
       v
Stage B: Task File Execution (delegated to /task)
       |
  Phase 1: Preparation -----------------------------------------------+
       |                                                               |
  Phase 2: Deep Investigation ----------------------------------------+  <- parallel agents
       |                                                               |    (Architecture Analyst, Code Tracer,
       |                                                               |     Data Model Analyst, API Surface Mapper,
       |                                                               |     Integration Mapper, Doc Analyst)
  Phase 3: Completeness Verification ---------------------------------+  <- rf-analyst + rf-qa (parallel)
       |                                                               |
  Phase 4: Web Research ----------------------------------------------+  <- parallel agents
       |                                                               |
  Phase 5: Synthesis + QA Gate ---------------------------------------+  <- parallel agents, then analyst + qa
       |                                                               |
  Phase 6: Assembly & Validation -------------------------------------+  <- assembler, then qa, then qualitative
       |                                                               |
  Phase 7: Present to User & Complete --------------------------------+
```

### Phase details

| Phase | Parallel | Agent Types | Description |
|-------|----------|-------------|-------------|
| 1 | No | Orchestrator | Confirm scope, read TDD template, select tier, create task folders |
| 2 | Yes | Architecture Analyst, Code Tracer, Data Model Analyst, API Surface Mapper, Integration Mapper, Doc Analyst | Parallel codebase investigation — each agent writes findings to `research/` |
| 3 | Yes | rf-analyst, rf-qa | Completeness verification + research gate (parallel). QA verdict gates progression. |
| 4 | Yes | Web Research Agent | External research for design patterns, framework docs, API references, security best practices |
| 5 | Yes, then sequential | Synthesis Agent, rf-analyst, rf-qa | Parallel synthesis agents produce template-aligned sections, then analyst + QA verify |
| 6 | Sequential | rf-assembler, rf-qa, rf-qa-qualitative | Assembly -> structural QA -> qualitative QA, each with in-place fix authorization |
| 7 | No | Orchestrator | Present summary, offer implementation tasks, update task file to Done |

### Agent types and roles

| Agent Type | Investigation Focus | Used In |
|------------|---------------------|---------|
| **Architecture Analyst** | Trace architectural decisions, dependency chains, component relationships, design patterns | Phase 2 |
| **Code Tracer** | Read implementations, trace data flow, follow imports, document behavior | Phase 2 |
| **Data Model Analyst** | Map data shapes, entity relationships, schemas, type definitions, storage | Phase 2 |
| **API Surface Mapper** | Document API endpoints, request/response schemas, service boundaries | Phase 2 |
| **Integration Mapper** | Map extension points, plugin interfaces, config surfaces, cross-service communication | Phase 2 |
| **Doc Analyst** | Extract context from existing docs, cross-validate every architectural claim against code | Phase 2 |
| **Web Research Agent** | External design patterns, framework docs, security best practices, API standards, SLO benchmarks | Phase 4 |
| **Synthesis Agent** | Read research files, produce template-aligned TDD sections | Phase 5 |
| **rf-analyst** | Independent analytical verification (completeness, synthesis review) | Phases 3, 5 |
| **rf-qa** | Zero-trust QA verification (research gate, synthesis gate, report validation) | Phases 3, 5, 6 |
| **rf-qa-qualitative** | Content-level quality review (architecture coherence, API consistency, implementation specificity) | Phase 6 |
| **rf-assembler** | Consolidate synthesis files into final TDD with cross-section consistency | Phase 6 |

---

## 4) Tier Selection and Agent Counts

Match the tier to component scope. **Default to Standard** unless the component is clearly documentable with a quick scan of <5 files.

| Tier | When | Codebase Agents | Web Agents | Target Lines |
|------|------|-----------------|------------|-------------|
| **Lightweight** | Bug fixes, config changes, small features (<1 sprint), <5 relevant files | 2-3 | 0-1 | 300-600 |
| **Standard** | Most features and services (1-3 sprints), 5-20 files, moderate complexity | 4-6 | 1-2 | 800-1,400 |
| **Heavyweight** | New systems, platform changes, cross-team projects, 20+ files | 6-10+ | 2-4 | 1,400-2,200 |

### Tier selection rules

- If in doubt, pick **Standard**
- If the user says "detailed", "comprehensive", "thorough" — always **Heavyweight**
- Only use **Lightweight** for genuinely narrow designs (single service, <5 relevant files)
- If the scope spans multiple services, architectural layers, or integration boundaries — always **Heavyweight**

---

## 5) Quality Gates and Validation

The pipeline enforces quality at three critical gates plus a final dual-QA pass.

### Gate 1: Research Completeness (Phase 3)

**Agents**: rf-analyst (completeness-verification) + rf-qa (research-gate), run in parallel.

**rf-analyst checklist (8 items)**:
1. Coverage audit — every key file/subsystem from scope covered by at least one research file
2. Evidence quality — claims cite specific file paths, line numbers, function names
3. Documentation staleness — all doc-sourced claims tagged `[CODE-VERIFIED/CODE-CONTRADICTED/UNVERIFIED]`
4. Completeness — every file has Status: Complete, Summary, Gaps, Key Takeaways
5. Cross-reference check — cross-cutting concerns covered by multiple agents are cross-referenced
6. Contradiction detection — conflicting findings about the same component surfaced
7. Gap compilation — all gaps unified, deduplicated, and severity-rated (Critical/Important/Minor)
8. Depth assessment — investigation depth matches the stated tier (data models documented, API surfaces mapped, architecture patterns identified)

**rf-qa checklist (10 items)**:
1. File inventory — all research files exist with Status: Complete and Summary
2. Evidence density — sample 3-5 claims per file, verify file paths exist
3. Scope coverage — every key file from research-notes EXISTING_FILES examined
4. Documentation cross-validation — all doc-sourced claims tagged, spot-check 2-3 CODE-VERIFIED
5. Contradiction resolution — no unresolved conflicting findings
6. Gap severity — Critical gaps block synthesis, Important reduce quality, Minor still must be fixed
7. Depth appropriateness — matches the tier expectation
8. Integration point coverage — connection points documented
9. Pattern documentation — code patterns and conventions captured
10. Incremental writing compliance — files show iterative structure, not one-shot

**Verdict**: PASS proceeds to Phase 4. FAIL triggers targeted gap-filling agents (max 3 fix cycles). After 3 failed cycles, execution halts and issues are presented to the user.

**Parallel partitioning**: When >6 research files, multiple analyst/QA instances run with assigned subsets.

### Gate 2: Synthesis Quality (Phase 5)

**Agents**: rf-analyst (synthesis-review) + rf-qa (synthesis-gate, fix_authorization: true), run in parallel.

**rf-analyst synthesis review (9 items)**:
1. Template section headers match the TDD template exactly
2. Tables use the correct column structure (FR/NFR ID numbering, entity tables, SLO/SLI/Error Budget tables)
3. No content was fabricated beyond what research files contain
4. Findings cite actual file paths and evidence
5. Architecture sections include at least one diagram (ASCII or Mermaid)
6. Requirements use FR-001/NFR-001 ID numbering with priority and acceptance criteria
7. All cross-references between sections are consistent (requirements trace to architecture, risks to mitigations)
8. No doc-only claims in Architecture (Section 6), Data Models (Section 7), or API Specs (Section 8)
9. Stale documentation discrepancies surfaced in Open Questions (Section 22)

**rf-qa synthesis gate adds 4 checks (10-13)**:
10. Content rules compliance (tables over prose, no code reproductions)
11. All expected sections have content (no placeholders)
12. No hallucinated file paths (verify parent directories exist)
13. FR traceability — spot-check 3 FRs: each must cite a PRD epic ID in its Source column (or be marked `[NO PRD TRACE]`)

**Verdict**: PASS proceeds to Phase 6. FAIL triggers re-synthesis + re-QA (max 2 fix cycles). After 2 failed cycles, execution halts and issues are presented to the user.

**Parallel partitioning**: When >4 synthesis files, multiple analyst/QA instances run with assigned subsets.

### Gate 3: Report Validation (Phase 6)

**Agent**: rf-qa (report-validation, fix_authorization: true).

**Validation checklist (15 structural + 5 content quality)**:

**Structural completeness:**
1. All 28 template sections present (or explicitly marked as N/A with rationale per tier)
2. Frontmatter has all required fields (id, title, status, created_date, parent_doc, depends_on, tags)
3. Total line count within tier budget (Lightweight: 300-600, Standard: 800-1,400, Heavyweight: 1,400-2,200)
4. Document purpose block with tiered usage table present
5. Document Information table has all 7 rows plus Approvers table
6. Numbered Table of Contents present
7. Requirements use FR/NFR ID numbering with priority
8. Architecture section includes at least one diagram (ASCII or Mermaid)
9. Alternative 0: Do Nothing is present in Alternatives Considered (Section 21)
10. SLO/SLI tables present for Standard and Heavyweight tiers
11. No full source code reproductions
12. All file paths reference actual files that exist
13. Document History table present
14. Tables use correct column structure from template
15. No doc-sourced architectural claims presented as verified without code cross-validation tags

**Content quality checks:**
16. Table of Contents accuracy (matches actual section headers)
17. Internal consistency (no contradictions between sections)
18. Readability (scannable — tables, headers, bullets)
19. Web research findings include source URLs for every external claim
20. Actionability (engineer could begin implementation from the Architecture, Data Models, and API Specifications alone)

### Gate 4: Qualitative Review (Phase 6)

**Agent**: rf-qa-qualitative (tdd-qualitative, fix_authorization: true).

Verifies the TDD makes sense from product and engineering perspectives:
- Architecture decisions match PRD requirements (if PRD provided)
- API contracts are internally consistent
- Implementation details are specific enough to code from
- No PRD content repeated verbatim (translated into engineering specs instead)
- Data models match across diagrams, contracts, and migrations
- No requirements invented that aren't traceable to the PRD or codebase evidence

**Zero leniency**: All severity levels (CRITICAL, IMPORTANT, MINOR) must be resolved before proceeding.

---

## 6) Output Artifacts

All persistent artifacts go into the task folder at `.dev/tasks/to-do/TASK-TDD-YYYYMMDD-HHMMSS/`.

### Directory structure

```
.dev/tasks/to-do/TASK-TDD-YYYYMMDD-HHMMSS/
├── TASK-TDD-YYYYMMDD-HHMMSS.md          # MDTM task file (execution contract)
├── research-notes.md                     # Scope discovery results (8 categories)
├── gaps-and-questions.md                 # Compiled gaps from all phases
├── research/
│   ├── 00-prd-extraction.md              # PRD context extraction (if PRD provided)
│   ├── 01-architecture-overview.md       # Codebase research agent outputs
│   ├── 02-data-models.md
│   ├── 03-api-surface.md
│   ├── 04-integration-points.md
│   ├── 05-existing-docs.md
│   ├── web-01-design-patterns.md         # Web research agent outputs
│   └── web-02-security-practices.md
├── synthesis/
│   ├── synth-01-exec-problem-goals.md    # Template-aligned synthesis files
│   ├── synth-02-requirements.md
│   ├── synth-03-architecture.md
│   ├── synth-04-data-api.md
│   ├── synth-05-state-components.md
│   ├── synth-06-error-security.md
│   ├── synth-07-observability-testing.md
│   ├── synth-08-perf-deps-migration.md
│   └── synth-09-risks-alternatives-ops.md
├── qa/
│   ├── analyst-completeness-report.md    # Phase 3 analyst output
│   ├── qa-research-gate-report.md        # Phase 3 QA output
│   ├── analyst-synthesis-review.md       # Phase 5 analyst output
│   ├── qa-synthesis-gate-report.md       # Phase 5 QA output
│   ├── qa-report-validation.md           # Phase 6 structural QA output
│   └── qa-qualitative-review.md          # Phase 6 qualitative QA output
└── reviews/
    └── (reserved for future review artifacts)

# Final TDD output location:
docs/[domain]/TDD_[COMPONENT-NAME].md
```

### Synthesis mapping table

| Synth File | TDD Template Sections | Primary Research Sources |
|------------|----------------------|------------------------|
| `synth-01-exec-problem-goals.md` | 1. Executive Summary, 2. Problem Statement, 3. Goals & Non-Goals, 4. Success Metrics | PRD extraction, architecture overview, existing docs |
| `synth-02-requirements.md` | 5. Technical Requirements | PRD extraction, architecture overview, all subsystem research |
| `synth-03-architecture.md` | 6. Architecture | Architecture overview, integration points, subsystem research, PRD technical constraints |
| `synth-04-data-api.md` | 7. Data Models, 8. API Specifications | Data models research, API surface research, web research (API standards) |
| `synth-05-state-components.md` | 9. State Management, 10. Component Inventory, 11. User Flows | State management research, subsystem research, PRD user stories |
| `synth-06-error-security.md` | 12. Error Handling, 13. Security Considerations | Security research, all subsystem research, web research (security patterns) |
| `synth-07-observability-testing.md` | 14. Observability, 15. Testing Strategy | Architecture overview, integration points, web research (SLO benchmarks) |
| `synth-08-perf-deps-migration.md` | 16. Accessibility, 17. Performance, 18. Dependencies, 19. Migration & Rollout | PRD extraction, architecture overview, web research (performance) |
| `synth-09-risks-alternatives-ops.md` | 20. Risks, 21. Alternatives, 22. Open Questions, 23-26. Timeline/Release/Ops/Cost | PRD extraction, all research, web research, gaps log |

**PRD extraction fallback:** When `00-prd-extraction.md` is absent (no PRD provided), synthesis agents skip PRD-sourced content and note "PRD source unavailable — requirements derived from feature description and codebase research." They do not fail or block.

**Backend components** skip Section 9 (State Management) and Section 10 (Component Inventory). Small components can combine more sections per synth file.

---

## 7) Content Rules (Non-Negotiable)

These rules come from the TDD template and apply to every generated TDD.

| Rule | Do | Don't |
|------|-----|-------|
| **Architecture** | ASCII or Mermaid diagrams with component tables | Multi-paragraph prose for what could be a diagram |
| **Data models** | Entity tables with Field / Type / Required / Description / Constraints | Full TypeScript interface or schema reproductions |
| **API specs** | Endpoint overview tables plus key endpoint details with request/response examples | Reproducing entire OpenAPI specs inline |
| **Requirements** | Functional/Non-functional split with FR-001/NFR-001 ID numbering | Prose paragraphs mixing requirement types |
| **Testing** | Test pyramid tables by level with coverage targets and tools | Generic "write tests" instructions |
| **Performance** | Budget tables with specific metrics and measurement methods | Vague "should be fast" requirements |
| **Security** | Threat model tables plus security controls with verification methods | General security platitudes without specifics |
| **Alternatives** | Structured Pros/Cons with mandatory "Why Not Chosen" and Do Nothing option | Surface-level dismissal of alternatives |
| **Dependencies** | Tables with Version / Purpose / Risk Level / Fallback | Inline dependency mentions scattered through prose |
| **SLOs** | SLO / SLI / Error Budget tables with burn-rate alerts | Undefined or aspirational reliability targets |
| **Source code** | Summarize behavior with key signatures | Reproduce full function bodies or config files |
| **Evidence** | Inline citations: `file.cpp:123`, `ClassName::method()` | Say "the code does X" without citing where |
| **Uncertainty** | Explicit "Unverified" or "Open Question" markers | Present uncertain findings as verified facts |

---

## 8) Behind the Scenes: How Execution Works

### 8.1 Stage A: Scope Discovery flow

1. **Check for existing task file** — looks in `.dev/tasks/to-do/` for `TASK-TDD-*/` matching this component. If found with unchecked items, resumes from there. Also checks for `research-notes.md` with partial progress.
2. **Parse & triage** — classifies request into Scenario A (explicit, most inputs provided) or Scenario B (vague, broad discovery needed). Does NOT interrogate the user — proceeds with what it has.
3. **Scope discovery** — uses Glob, Grep, and codebase-retrieval to map files, subsystems, integration points, and existing documentation. Optionally spawns `rf-task-researcher` for complex Scenario B discoveries.
4. **Write research notes** — structured file with 8 categories: EXISTING_FILES, PATTERNS_AND_CONVENTIONS, PRD_CONTEXT, SOLUTION_RESEARCH, RECOMMENDED_OUTPUTS, SUGGESTED_PHASES, TEMPLATE_NOTES, AMBIGUITIES_FOR_USER.
5. **Sufficiency gate** — mandatory review of research notes quality (8-point checklist including doc staleness verification). Max 2 gap-fill rounds.
6. **Template triage** — almost always Template 02 (Complex Task) for TDD creation.
7. **Build task file** — orchestrator loads `refs/build-request-template.md`, fills in the BUILD_REQUEST, spawns `rf-task-builder`. Builder loads `refs/agent-prompts.md`, `refs/synthesis-mapping.md`, `refs/validation-checklists.md`, `refs/operational-guidance.md`.
8. **Verify task file** — checks frontmatter, phase completeness, B2 self-contained items, embedded agent prompts, parallel spawning instructions, assembler usage, anti-orphaning compliance.

### 8.2 Stage B: Task file execution

Delegated entirely to the `/task` skill:
1. `/task` reads the MDTM task file and processes each checklist item via the F1 loop (READ -> IDENTIFY -> EXECUTE -> UPDATE -> REPEAT).
2. Subagents are spawned as specified in B2 self-contained items.
3. Phase-gate QA runs after each phase (Phase 2+).
4. On context compression or session restart, `/task` re-reads the task file and resumes from the first unchecked item.
5. `/task` adds its own phase-gate QA on top of the skill-specific QA items, resulting in intentional double QA at gate phases.

### 8.3 Resumability

The MDTM task file provides automatic resume:
- Every completed step is a checked `[x]` box on disk.
- On restart, the skill finds the first unchecked `[ ]` item and resumes there.
- Research files written incrementally persist even if the agent is interrupted mid-investigation.
- No explicit `--resume` flag needed — it's inherent to the task file system.

### 8.4 Parallel execution strategy

- **Phase 2**: All research agents spawn simultaneously in a single message with multiple Agent tool calls. Agent count follows tier: Lightweight 2-3, Standard 4-6, Heavyweight 6-10+.
- **Phase 3**: rf-analyst and rf-qa spawn in parallel. With >6 research files, multiple instances of each with assigned subsets.
- **Phase 4**: All web research agents spawn simultaneously.
- **Phase 5**: All synthesis agents spawn simultaneously. After completion, rf-analyst and rf-qa spawn in parallel. With >4 synth files, multiple partitioned instances.
- **Phase 6**: Sequential — assembler first (single agent, not parallel, because cross-section consistency requires seeing the whole document), then structural QA, then qualitative QA (each depends on the prior).

### 8.5 Error handling

- **QA gate failure**: Triggers targeted fix cycles (max 3 for research gate, max 2 for synthesis gate). After max cycles, execution HALTS: issues logged to Task Log, presented to user, requires user approval to continue.
- **Agent failure**: Individual agent failures are logged. Remaining agents continue. Failed investigations are noted in the gaps log.
- **Session interruption**: Resume from task file. Partial research files persist on disk.

---

## 9) End-to-End Workflow: PRD -> TDD -> Roadmap -> Tasklist -> Execution

The TDD skill sits at the second stage of the full product development pipeline, translating product requirements into engineering specifications.

### Stage A: PRD (product requirements)
```
/prd Create a PRD for [product area]
```
Produces a comprehensive PRD at `docs/docs-product/tech/[feature]/PRD_[FEATURE].md` with research artifacts. See `docs/guides/prd-skill-release-guide.md`.

### Stage B: TDD (technical design) <- **This skill**
```
/tdd Create a TDD based on the PRD at docs/docs-product/tech/[feature]/PRD_[FEATURE].md
```
The PRD skill offers to invoke `/tdd` automatically after completion. Research files from the PRD investigation provide requirements context for the TDD. The TDD extracts epics, user stories, acceptance criteria, and technical requirements from the PRD.

### Stage C: Roadmap (adversarial generation)
```bash
superclaude roadmap run spec.md --depth standard
```
Generates a merged, adversarially validated roadmap from a specification. See `docs/guides/roadmap-cli-tools-release-guide.md`.

### Stage D: Tasklist (execution plan)
```
/sc:tasklist
```
Generates Sprint CLI-compatible phase files from the roadmap.

### Stage E: Sprint execution
```bash
superclaude sprint run .dev/releases/current/tasklist-index.md
```
Executes the phases with supervised Claude sessions. See `docs/guides/sprint-cli-tools-release-guide.md`.

### PRD-to-TDD Traceability

When a PRD is provided, the TDD pipeline adds:
1. **PRD Extraction** — reads the PRD and extracts requirements into `research/00-prd-extraction.md`
2. **Requirements Traceability** — every FR in TDD Section 5 traces back to a PRD epic/user story
3. **Success Metrics Alignment** — TDD Section 4 includes engineering proxy metrics for PRD business KPIs
4. **Scope Inheritance** — TDD Section 3 inherits scope boundaries from PRD
5. **Cross-referencing** — the TDD frontmatter's `parent_doc` field links back to the PRD

---

## 10) Performance & Cost Expectations

### Execution time estimates

| Tier | Approximate Wall Time | Total Agents Spawned | Notes |
|------|----------------------|---------------------|-------|
| **Lightweight** | 5-10 minutes | 5-8 (2-3 research + 0-1 web + 2-3 synth + QA) | Single service, <5 files. |
| **Standard** | 15-30 minutes | 12-20 (4-6 research + 1-2 web + 6-9 synth + QA) | Most common. Full component or service. |
| **Heavyweight** | 30-60 minutes | 20-35+ (6-10+ research + 2-4 web + 9 synth + QA with partitioning) | Platform-level designs. Multiple QA partitions. |

### Token consumption

- **Stage A (scope discovery + task file creation)**: ~5,000-15,000 tokens in the main session
- **Phase 2 (deep investigation)**: Largest consumer. Each codebase agent uses ~10,000-30,000 tokens depending on code complexity. Heavyweight tier with 10 agents: ~200,000-300,000 tokens total across all agents.
- **Phase 3 (research QA)**: ~10,000-20,000 tokens per analyst/QA instance
- **Phase 4 (web research)**: ~5,000-15,000 tokens per web agent (depends on search depth)
- **Phase 5 (synthesis + QA)**: ~8,000-15,000 per synthesis agent + ~10,000-20,000 for QA
- **Phase 6 (assembly + dual QA)**: ~15,000-30,000 for assembler + ~10,000-15,000 per QA agent
- **Rough total**: Lightweight ~100K-200K, Standard ~300K-500K, Heavyweight ~500K-1M+ tokens

### Resource requirements

- **Disk space**: Task artifacts typically 500KB-2MB (research files + synthesis + QA reports)
- **Network**: Web research agents require internet access for design patterns and framework docs (Phase 4). Codebase-only runs skip Phase 4.
- **Session stability**: Long-running Heavyweight TDDs benefit from stable sessions. The MDTM task file provides resilience against interruptions, but frequent restarts add overhead from re-reading context.

---

## 11) Known Limitations & Gotchas

### Vague prompts produce broad, less focused TDDs
**Symptom**: TDD covers too much surface area without depth in any architecture area.
**Cause**: When only the component name is provided (Scenario B), the skill does broad discovery and can't prioritize what matters for your specific design decision.
**Workaround**: Always provide at minimum WHAT + WHERE. Specifying directories dramatically focuses the investigation.

### Missing PRD reduces requirements traceability
**Symptom**: TDD Section 5 (Technical Requirements) has FRs marked `[NO PRD TRACE]` and Section 4 (Success Metrics) lacks business KPI alignment.
**Cause**: No PRD was provided, so the skill derives requirements from feature description and codebase research alone.
**Workaround**: Create a PRD first using `/prd`, then feed it into the TDD. The PRD-to-TDD pipeline produces significantly stronger requirements traceability.

### Context compression during Heavyweight runs
**Symptom**: Phase 5 or 6 agents produce thinner output than Phase 2 agents.
**Cause**: Long Heavyweight runs may approach context limits.
**Workaround**: Each agent is self-contained with full instructions. If quality degrades, restart the session; the skill resumes from the task file.

### Existing docs treated as ground truth
**Symptom**: TDD describes architecture that no longer exists in the codebase.
**Cause**: Despite the Documentation Staleness Protocol, Doc Analyst agents may miss stale claims if the original documentation is internally consistent but outdated.
**Workaround**: After TDD completion, review `gaps-and-questions.md` for `[UNVERIFIED]` tags. Cross-check surprising architectural claims against actual code.

### Web research agents blocked by network restrictions
**Symptom**: Phase 4 web research files are empty or contain only error messages.
**Cause**: Corporate networks, VPNs, or air-gapped environments may block web search.
**Workaround**: The skill continues without web research (Phase 4 is not a hard gate). Design pattern and security best practice sections will be thinner. Populate them manually after TDD generation.

### Backend component generates frontend-specific sections
**Symptom**: TDD includes State Management (Section 9) and Component Inventory (Section 10) for a backend service.
**Cause**: Scope classification didn't identify the component as backend-only. The synthesis mapping table allows skipping these sections for backend components, but the tier/scope classifier may miss edge cases.
**Workaround**: These sections should be marked N/A. If populated incorrectly, the rf-qa-qualitative agent typically catches this. If it persists, manually remove.

---

## 12) Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| Skill asks clarifying questions instead of starting | WHAT input is too vague to determine component scope | Provide a specific component name and at least one directory |
| Scope discovery takes unusually long | Large codebase with many matching files (Scenario B broad search) | Provide WHERE input to constrain the search space |
| Task builder produces malformed task file | Research notes are incomplete (failed sufficiency gate) | Check `research-notes.md` — ensure all 8 categories are populated |
| Research agents produce empty output files | Agent spawning failed or agent hit context limit immediately | Check agent error output; restart session to get fresh context |
| QA gate fails repeatedly (3+ fix cycles for research, 2+ for synthesis) | Fundamental gap in research coverage | Review the QA report, manually investigate flagged areas, then restart |
| Synthesis agents produce placeholder content | Research files don't cover the template sections assigned to that synth file | Check synthesis mapping — the research directory may be missing a topic |
| Assembly produces a TDD missing sections | Synthesis files incomplete or missing | Check `synthesis/` directory — ensure all `synth-*.md` files are present and populated |
| Final TDD line count exceeds tier budget | Synthesis agents over-produced; assembler didn't trim | The rf-qa report-validation agent should catch this. If it persists, manually trim. |
| "TDD already complete" when you want a fresh start | Prior `TASK-TDD-*` folder exists with all items checked | Archive the old folder: `mv .dev/tasks/to-do/TASK-TDD-* .dev/tasks/done/` |
| TDD contains `[UNVERIFIED]` tags in final output | Doc-sourced claims could not be cross-validated against code | Review each tagged claim manually — the claim may be stale, planned, or in another repo |
| Phase Loading Contract violation error | A refs file was loaded outside its declared phase | Review the Phase Loading Contract table in the SKILL.md; ensure orchestrator only loads `refs/build-request-template.md` and only at A.7 |

---

## 13) Practical Use Cases

### Use case 1: Standard TDD from PRD
```
/tdd Create a TDD for the agent orchestration system. The PRD is at
docs/docs-product/tech/agents/PRD_AGENT_SYSTEM.md. Focus on backend/app/agents/
and backend/app/services/.
```
Standard tier, 4-6 codebase agents + 1-2 web agents. Full PRD-to-TDD traceability. All 28 template sections populated.

### Use case 2: Heavyweight new system design
```
/tdd Design the technical architecture for a shared GPU pool to replace per-session
VMs. Scope: ue_manager/, infrastructure/, backend/app/services/streaming_service.py.
This is a Heavyweight TDD — new system, cross-team impact.
```
Heavyweight tier, 6-10+ agents. Web research targets GPU pooling patterns, infrastructure scaling, and security best practices.

### Use case 3: Lightweight config change
```
/tdd Create a TDD for the notification preference system. Focus on
backend/api/preferences/notification_prefs.py — it's a small feature.
```
Lightweight tier, 2-3 agents, 300-600 lines. Quick turnaround for a narrow design scope.

### Use case 4: PRD translation (downstream from /prd)
```
/tdd Turn the canvas roadmap PRD into a TDD. The PRD is at
docs/docs-product/tech/canvas/PRD_ROADMAP_CANVAS.md. Standard-tier covering
the React canvas system and node type architecture. Focus on frontend/app/roadmap/.
```
PRD extraction produces `00-prd-extraction.md`. FRs trace to PRD epics. Engineering proxy metrics generated for each business KPI.

### Use case 5: Resume interrupted TDD
```
/tdd Create a TDD for the wizard state management system.
```
If a `TASK-TDD-*` folder exists for "wizard state management", the skill reads the task file and resumes from the first unchecked item. No explicit resume flag needed.

### Use case 6: TDD feeding into roadmap
```
/tdd Create a TDD for the payment processing pipeline. After completion, we'll
generate a roadmap from the design specifications.
```
After TDD completion, Phase 7 offers to create implementation tasks. The TDD and its research artifacts feed into `superclaude roadmap run` for execution planning.

### Use case 7: TDD from existing documentation consolidation
```
/tdd Create a TDD for pixel streaming infrastructure by consolidating the existing
architecture docs at docs/streaming/. Need a single source of truth for the design.
```
Consolidation mode — Doc Analyst agents cross-validate existing docs against code. Document Provenance appendix tracks which source doc contributed to which section.

### Use case 8: Explicit output location with existing stub
```
/tdd Populate the TDD stub at docs/agents/TDD_AGENT_ORCHESTRATION.md. The PRD is at
docs/docs-product/tech/agents/PRD_AGENT_SYSTEM.md. Heavyweight — cross-team system.
```
Writes to the specified stub location rather than the default path. Preserves any existing content in the stub's scope section.

---

## 14) Quick Reference

### Invocation

```
/tdd [description]
```

### Key behaviors

- Automatically selects tier (Lightweight/Standard/Heavyweight) based on file count and scope
- Resumes from existing task files if found (checks `.dev/tasks/to-do/TASK-TDD-*/`)
- Asks for clarification only when genuine ambiguity about intent exists
- Offers downstream implementation task creation after completion
- Extracts PRD context automatically when PRD reference is provided

### Output locations

- Task artifacts: `.dev/tasks/to-do/TASK-TDD-YYYYMMDD-HHMMSS/`
- Final TDD: `docs/[domain]/TDD_[COMPONENT-NAME].md`

### Quality guarantees

- 3 independent QA gates (research completeness, synthesis quality, report validation)
- 1 qualitative review (architecture coherence, implementation specificity, PRD alignment)
- Documentation staleness cross-validation with `[CODE-VERIFIED]` tags
- Template conformance checking against `src/superclaude/examples/tdd_template.md`
- Zero-trust verification (assume wrong until proven correct)

### Phase Loading Contract summary

| Phase | Loads | Forbidden |
|-------|-------|-----------|
| SKILL.md load / A.1-A.6 | SKILL.md | All refs files |
| A.7 (orchestrator) | `refs/build-request-template.md` | Other refs |
| A.7 (builder) | `refs/agent-prompts.md`, `refs/synthesis-mapping.md`, `refs/validation-checklists.md`, `refs/operational-guidance.md` | None |
| Stage B | Task file + /task skill | All refs files |

### Failure modes prevented

- **Context rot** — isolated agents with incremental file writing
- **Shallow coverage** — parallel deep-dive investigation agents
- **Hallucinated design details** — separated research/synthesis/assembly with verification
- **Quality drift** — rf-analyst + rf-qa + rf-qa-qualitative at three gates
- **Stale documentation claims** — Documentation Staleness Protocol with code cross-validation tags
