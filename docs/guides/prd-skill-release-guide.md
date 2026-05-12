---
component: "prd-skill"
component_version: "skill-v2 (refactored decomposition)"
covers_release: "refactor/prd-skill-decompose branch"
last_updated: "2026-04-03"
author: "Claude Opus 4.6"
---

# PRD Skill — Release Guide

This guide covers the `/prd` skill for Product Requirements Document generation, including:
- what the skill does and how it works,
- when to use it,
- how to invoke it,
- practical examples with all options,
- the 7-phase multi-agent pipeline architecture (with parallel investigation, QA gates, and assembly),
- tier selection and depth control,
- quality gates and validation,
- output artifacts and file structure,
- performance and cost expectations by tier,
- known limitations and gotchas,
- troubleshooting common issues,
- and how it fits into the **PRD -> TDD -> roadmap -> tasklist -> execution** workflow.

---

## 1) Release Summary (What is included)

### Core capability
The `/prd` skill creates comprehensive Product Requirements Documents by orchestrating a multi-agent investigation, synthesis, and assembly pipeline. It uses Rigorflow's MDTM task file system for persistent progress tracking — every phase and step is encoded as checklist items in a task file that survives context compression and session restarts.

### Migration notes (refactored decomposition)

This release refactors the PRD skill from a monolithic SKILL.md into a decomposed structure with external reference files:

- **What changed**: Agent prompt templates, synthesis mapping table, and validation checklists extracted into `refs/` subdirectory files (`agent-prompts.md`, `synthesis-mapping.md`, `validation-checklists.md`). SKILL.md now references these files rather than inlining all content.
- **What broke**: Nothing — the skill's invocation surface (`/prd [description]`) is unchanged. The decomposition is internal.
- **What to do**: If you have local modifications to a pre-decomposition SKILL.md, merge your changes into the appropriate `refs/` file or the slimmed SKILL.md. Run `make sync-dev` after any edits to `src/superclaude/skills/prd/`.
- **What was removed**: Duplicate content that now lives in `refs/` files. The SKILL.md still contains the full behavioral protocol; only reference material was extracted.

### Architecture overview
The PRD skill operates in two stages:
- **Stage A** — Scope Discovery & Task File Creation: Maps the product space, plans research assignments, and spawns `rf-task-builder` to create an MDTM task file encoding all phases.
- **Stage B** — Task File Execution: Delegates to the `/task` skill, which runs the F1 execution loop over the task file's checklist items, spawning parallel subagents as specified.

The pipeline uses **parallel multi-agent investigation** to achieve deep coverage: multiple specialized agents (Feature Analyst, Doc Analyst, Integration Mapper, UX Investigator, Architecture Analyst) explore the codebase simultaneously, writing incremental findings to disk. QA gates at three critical points prevent quality drift.

### Skill file structure
```
src/superclaude/skills/prd/
├── SKILL.md                        # Full skill definition and behavioral protocol
└── refs/
    ├── agent-prompts.md            # Agent prompt templates (codebase, web, synthesis, QA, assembly)
    ├── synthesis-mapping.md        # PRD template section -> synthesis file mapping
    ├── validation-checklists.md    # Synthesis quality, assembly process, validation checklist, content rules
    └── .gitkeep

.claude/skills/prd/                 # Dev copy (synced from src/ via make sync-dev)
├── SKILL.md
└── refs/
    ├── agent-prompts.md
    ├── synthesis-mapping.md
    ├── validation-checklists.md
    └── .gitkeep
```

### Key design decisions
- **MDTM task file as execution contract**: The task file on disk is the source of truth, not conversation context. Progress survives context compression and session restarts.
- **Incremental file writing**: All agents follow the Incremental File Writing Protocol — create file immediately, append findings as discovered. Never accumulate in context and one-shot.
- **Documentation staleness protocol**: Every doc-sourced claim is tagged `[CODE-VERIFIED]`, `[CODE-CONTRADICTED]`, or `[UNVERIFIED]`. Only code-verified claims appear as current product capabilities.
- **Zero-trust QA**: Dedicated `rf-analyst` and `rf-qa` agents verify at three gates (post-research, post-synthesis, post-assembly). The QA agent assumes everything is wrong until independently verified.
- **Parallel partitioning for scale**: When file counts exceed thresholds (>6 research files, >4 synthesis files), multiple analyst/QA instances run in parallel with assigned subsets to prevent context rot.
- **Template conformance**: Output always follows `src/superclaude/examples/prd_template.md`. The template is the schema — every PRD must conform to it.
- **Ref decomposition**: Agent prompts, synthesis mapping, and validation checklists are extracted into `refs/` files loaded by the task builder, keeping the main SKILL.md focused on behavioral protocol and reducing context pressure during scope discovery.

---

## 2) Invocation Reference — When and How to Use

### `/prd`

#### What it does
Performs scope discovery on a product area, creates an MDTM task file encoding the full investigation/synthesis/assembly pipeline, then delegates execution to `/task` for multi-agent parallel execution with QA gates.

#### Use when
- You need a comprehensive PRD for a product, feature, or platform capability.
- You want evidence-based documentation grounded in actual codebase state.
- You want multi-agent parallel investigation for deep coverage.
- You want persistent progress tracking that survives session restarts.
- You want to feed the PRD into downstream `/tdd` or `/sc:roadmap` workflows.

#### Syntax
```
/prd [description of what to document]
```

#### Input requirements

The skill needs four pieces of information. The first is mandatory; the rest improve quality:

| Input | Required | Description |
|-------|----------|-------------|
| **WHAT** | Yes | Product area, feature, or platform capability to document |
| **WHY** | Strongly recommended | What decisions this PRD supports (engineering planning, investor materials, stakeholder alignment) |
| **WHERE** | Optional | Specific directories, services, or subsystems to focus on |
| **OUTPUT** | Optional | Where the final PRD goes (existing stub or new location) |

#### Examples

```
# Strong — all four inputs
/prd Create a PRD for the GameFrame AI multi-agent system. We need this for
Series A investor materials and to align engineering on next quarter's roadmap.
Focus on: backend/app/agents/, backend/app/services/, frontend/src/components/Chat/.
Output to docs/docs-product/tech/agents/PRD_MULTI_AGENT_SYSTEM.md.

# Strong — clear scope + purpose
/prd Create a PRD for the wizard configuration system. We want to add new stages
and need to document current capabilities vs planned features for the product team.
Key areas: frontend/app/wizard/, the stage configs, and the Zustand store slices.

# Minimal — topic only (broader, less actionable output)
/prd Write a PRD for the platform.
```

---

## 3) The 7-Phase Multi-Agent Pipeline

The PRD pipeline generates a comprehensive product requirements document through parallel multi-agent investigation, synthesis, and assembly with QA gates at three critical points.

### Pipeline overview

```
Stage A: Scope Discovery (orchestrator)
  A.1: Check for existing task file
  A.2: Parse & triage PRD request
  A.3: Perform scope discovery (Glob, Grep, codebase-retrieval)
  A.4: Write research notes file
  A.5: Review research sufficiency (MANDATORY GATE)
  A.6: Template triage (01 or 02)
  A.7: Spawn rf-task-builder -> MDTM task file
  A.8: Verify task file
       |
       v
Stage B: Task File Execution (delegated to /task)
       |
  Phase 1: Preparation -----------------------------------------------+
       |                                                               |
  Phase 2: Deep Investigation ----------------------------------------+  <- parallel agents
       |                                                               |
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
| 1 | No | Orchestrator | Confirm scope, read template, select tier, create task folders |
| 2 | Yes | Feature Analyst, Doc Analyst, Integration Mapper, UX Investigator, Architecture Analyst | Parallel codebase investigation — each agent writes findings to `research/` |
| 3 | Yes | rf-analyst, rf-qa | Completeness verification + research gate (parallel). QA verdict gates progression. |
| 4 | Yes | Web Research Agent | External research for market context, competitive landscape, industry standards |
| 5 | Yes, then sequential | Synthesis Agent, rf-analyst, rf-qa | Parallel synthesis agents produce template-aligned sections, then analyst + QA verify |
| 6 | Sequential | rf-assembler, rf-qa, rf-qa-qualitative | Assembly -> structural QA -> qualitative QA, each with in-place fix authorization |
| 7 | No | Orchestrator | Present summary, offer downstream TDD creation, update task file to Done |

### Agent types and roles

| Agent Type | Investigation Focus | Used In |
|------------|---------------------|---------|
| **Feature Analyst** | Inventory product capabilities, trace user-facing features | Phase 2 |
| **Doc Analyst** | Extract context from existing docs, cross-validate against code | Phase 2 |
| **Integration Mapper** | Map APIs, extension points, service boundaries, external dependencies | Phase 2 |
| **UX Investigator** | Trace interaction patterns, UI flows, accessibility patterns | Phase 2 |
| **Architecture Analyst** | Trace architectural decisions, dependency chains, technology choices | Phase 2 |
| **Web Research Agent** | External market data, competitive landscape, industry standards | Phase 4 |
| **Synthesis Agent** | Read research files, produce template-aligned PRD sections | Phase 5 |
| **rf-analyst** | Independent analytical verification (completeness, synthesis review) | Phases 3, 5 |
| **rf-qa** | Zero-trust QA verification (research gate, synthesis gate, report validation) | Phases 3, 5, 6 |
| **rf-qa-qualitative** | Content-level quality review (scope, logic, contradictions, audience) | Phase 6 |
| **rf-assembler** | Consolidate synthesis files into final PRD with cross-section consistency | Phase 6 |

---

## 4) Tier Selection and Agent Counts

Match the tier to product scope. **Default to Standard** unless the product is clearly documentable with a quick scan of <5 files.

| Tier | When | Codebase Agents | Web Agents | Target Lines |
|------|------|-----------------|------------|-------------|
| **Lightweight** | Single feature, narrow scope, <5 user stories, <5 relevant files | 2-3 | 0-1 | 400-800 |
| **Standard** | Full product area, 5-20 user stories, moderate complexity, 5-20 files | 4-6 | 1-2 | 800-1,500 |
| **Heavyweight** | Platform-level PRD, 20+ user stories, multiple product areas, 20+ files | 6-10+ | 2-4 | 1,500-2,500 |

### Tier selection rules
- If in doubt, pick **Standard**
- If the user says "detailed", "comprehensive", "thorough" — always **Heavyweight**
- Only use **Lightweight** for genuinely narrow products (<5 files, single concern)
- If the scope spans multiple product areas, architectural layers, or integration boundaries — always **Heavyweight**

### PRD scope classification

| Type | When | Template Impact |
|------|------|-----------------|
| **Product PRD** | Entire standalone product or platform | All 32 sections applicable. Include TAM/SAM/SOM, pricing, GTM, competitive analysis, full compliance. |
| **Feature/Component PRD** | Feature or subsystem within the platform | Sections S5, S8, S9, S16, S17, S18 are N/A or abbreviated. Reference Platform PRD for platform-level concerns. |

---

## 5) Quality Gates and Validation

The pipeline enforces quality at three critical gates plus a final dual-QA pass.

### Gate 1: Research Completeness (Phase 3)

**Agents**: rf-analyst (completeness-verification) + rf-qa (research-gate), run in parallel.

**rf-analyst checklist (8 items)**:
1. Coverage audit — every key product area covered by at least one research file
2. Evidence quality — claims cite specific file paths and feature names
3. Documentation staleness — all doc-sourced claims tagged `[CODE-VERIFIED/CODE-CONTRADICTED/UNVERIFIED]`
4. Completeness — every file has Status: Complete, Summary, Gaps, Key Takeaways
5. Cross-reference check — cross-cutting concerns covered by multiple agents
6. Contradiction detection — conflicting findings surfaced
7. Gap compilation — all gaps unified, deduplicated, severity-rated
8. Depth assessment — investigation depth matches stated tier

**rf-qa checklist (11 items)**:
1. File inventory — all research files exist with Status: Complete
2. Evidence density — sample 3-5 claims per file, verify file paths exist
3. Scope coverage — every key product area from research notes examined
4. Documentation cross-validation — spot-check CODE-VERIFIED tags
5. Contradiction resolution — no unresolved conflicting findings
6. Gap severity — Critical gaps block synthesis
7. Depth appropriateness — matches tier expectation
8. User flow coverage — key interactions documented
9. Integration point coverage — external dependencies documented
10. Pattern documentation — code conventions captured
11. Incremental writing compliance — files show iterative structure

**Verdict**: PASS proceeds to Phase 4. FAIL triggers targeted gap-filling agents (max 3 fix cycles).

**Parallel partitioning**: When >6 research files, multiple analyst/QA instances run with assigned subsets.

### Gate 2: Synthesis Quality (Phase 5)

**Agents**: rf-analyst (synthesis-review) + rf-qa (synthesis-gate, fix_authorization: true), run in parallel.

**Synthesis QA checklist (12 items)**:
1. Section headers match PRD template structure
2. Table column structures correct
3. No fabrication (trace claims to research files)
4. Evidence citations use actual file paths
5. User stories follow As a / I want / So that format
6. Requirements use RICE or MoSCoW prioritization
7. Cross-section consistency (personas referenced in stories, etc.)
8. No doc-only claims in product capability sections
9. Stale docs surfaced in Open Questions or Assumptions & Constraints
10. Content rules compliance (tables over prose)
11. All expected sections have content (no placeholders)
12. No hallucinated file paths

**Verdict**: PASS proceeds to Phase 6. FAIL triggers re-synthesis + re-QA (max 2 fix cycles).

**Parallel partitioning**: When >4 synthesis files, multiple analyst/QA instances run with assigned subsets.

### Gate 3: Report Validation (Phase 6)

**Agent**: rf-qa (report-validation, fix_authorization: true).

**Validation checklist (18 structural + 4 content quality)**:

**Structural completeness:**
- All 32 template sections present (or N/A with rationale)
- Frontmatter has all required fields
- Total line count within tier budget
- HOW TO USE blockquote present
- Document Information table (9 rows)
- Numbered Table of Contents

**Content quality:**
- User stories with testable acceptance criteria
- Feature prioritization with RICE/MoSCoW
- Competitive analysis with comparison matrix
- KPI tables with measurement methods
- No full source code reproductions
- All file paths reference actual files
- Web research findings include source URLs

**Content quality checks:**
- Table of Contents accuracy
- Internal consistency (no contradictions)
- Readability (scannable)
- Actionability (product team could plan from this PRD alone)

### Gate 4: Qualitative Review (Phase 6)

**Agent**: rf-qa-qualitative (prd-qualitative, fix_authorization: true).

Verifies the PRD makes sense from product and engineering perspectives:
- Correct scoping (feature vs platform content)
- Logical flow between sections
- Realistic requirements
- No contradictions or red flags
- Appropriate audience targeting

**Zero leniency**: All severity levels (CRITICAL, IMPORTANT, MINOR) must be resolved before proceeding.

---

## 6) Output Artifacts

All persistent artifacts go into the task folder at `.dev/tasks/to-do/TASK-PRD-YYYYMMDD-HHMMSS/`.

### Directory structure

```
.dev/tasks/to-do/TASK-PRD-YYYYMMDD-HHMMSS/
├── TASK-PRD-YYYYMMDD-HHMMSS.md          # MDTM task file (execution contract)
├── research-notes.md                     # Scope discovery results
├── gaps-and-questions.md                 # Compiled gaps from all phases
├── research/
│   ├── 01-feature-inventory.md           # Codebase research agent outputs
│   ├── 02-user-experience.md
│   ├── 03-integration-points.md
│   ├── 04-architecture.md
│   ├── 05-existing-docs.md
│   ├── web-01-competitive-landscape.md   # Web research agent outputs
│   └── web-02-market-data.md
├── synthesis/
│   ├── synth-01-exec-problem-vision.md   # Template-aligned synthesis files
│   ├── synth-02-business-market.md
│   ├── synth-03-competitive-scope.md
│   ├── synth-04-stories-requirements.md
│   ├── synth-05-technical-stack.md
│   ├── synth-06-ux-legal-business.md
│   ├── synth-07-metrics-risk-impl.md
│   ├── synth-08-journey-design-api.md
│   └── synth-09-resources-maintenance.md
├── qa/
│   ├── analyst-completeness-report.md    # Phase 3 analyst output
│   ├── qa-research-gate-report.md        # Phase 3 QA output
│   ├── analyst-synthesis-review.md       # Phase 5 analyst output
│   ├── qa-synthesis-gate-report.md       # Phase 5 QA output
│   ├── qa-report-validation.md           # Phase 6 structural QA output
│   └── qa-qualitative-review.md          # Phase 6 qualitative QA output
└── reviews/
    └── (reserved for future review artifacts)

# Final PRD output location:
docs/docs-product/tech/[feature-name]/PRD_[FEATURE-NAME].md
```

### Synthesis mapping table

| Synth File | PRD Template Sections | Primary Research Sources |
|------------|----------------------|------------------------|
| `synth-01-exec-problem-vision.md` | S1 Executive Summary, S2 Problem Statement, S3 Background, S4 Vision | Product capabilities, web research (market), existing docs |
| `synth-02-business-market.md` | S5 Business Context, S6 JTBD, S7 Personas, S8 Value Proposition | User flows, web research (market), capabilities |
| `synth-03-competitive-scope.md` | S9 Competitive Analysis, S10 Assumptions, S11 Dependencies, S12 Scope | Web research (competitive), tech stack, integrations |
| `synth-04-stories-requirements.md` | S13 Open Questions, S21.1 Epics/Stories, S21.2 Requirements | Per-area research, user flows, gaps log |
| `synth-05-technical-stack.md` | S14 Technical Requirements, S15 Technology Stack | Tech stack, architecture, web (tech trends) |
| `synth-06-ux-legal-business.md` | S16 UX Requirements, S17 Legal, S18 Business Requirements | User flows, capabilities, web (compliance) |
| `synth-07-metrics-risk-impl.md` | S19 Metrics, S20 Risk Analysis, S21.3-5 Phasing/Criteria/Timeline | All research, web research, tech stack |
| `synth-08-journey-design-api.md` | S22 Journey Map, S23 Error Handling, S24 UI Design, S25 API Contracts | User flows, per-area research, tech stack |
| `synth-09-resources-maintenance.md` | S26 Contributors, S27 Resources, S28 Maintenance | Existing docs, all research, gaps log |

---

## 7) Content Rules (Non-Negotiable)

These rules come from the PRD template and apply to every generated PRD.

| Rule | Do | Don't |
|------|-----|-------|
| **Product vision** | Concise statement + 1-2 paragraph expansion | Multi-page essays or vague aspirations |
| **User personas** | Structured attribute tables with representative quotes | Lengthy narrative descriptions |
| **User stories** | As a / I want / So that with acceptance criteria | Vague feature descriptions |
| **Competitive analysis** | Feature comparison matrices with status icons | Prose-based competitor descriptions |
| **Requirements** | Prioritized tables with RICE/MoSCoW scores | Unprioritized feature lists |
| **Market data** | TAM/SAM/SOM tables with sources | Unsourced market claims |
| **KPIs** | Category / KPI / Target / Measurement Method table | Vague success metrics |
| **Scope** | In/Out/Deferred tables with rationale | Unbounded descriptions |
| **Risk analysis** | Probability/Impact matrices with mitigations | Concern lists without assessment |
| **Timeline** | ASCII timeline diagrams with milestones | Vague "Q3" dates |

---

## 8) Behind the Scenes: How Execution Works

### 8.1 Stage A: Scope Discovery flow

1. **Check for existing task file** — looks in `.dev/tasks/to-do/` for `TASK-PRD-*/` matching this product. If found with unchecked items, resumes from there.
2. **Parse & triage** — classifies request into Scenario A (explicit, all inputs provided) or Scenario B (vague, broad discovery needed).
3. **Scope discovery** — uses Glob, Grep, and codebase-retrieval to map files, subsystems, integration points, and existing documentation.
4. **Write research notes** — structured file with 7 categories: EXISTING_FILES, PATTERNS_AND_CONVENTIONS, FEATURE_ANALYSIS, RECOMMENDED_OUTPUTS, SUGGESTED_PHASES, TEMPLATE_NOTES, AMBIGUITIES_FOR_USER.
5. **Sufficiency gate** — mandatory review of research notes quality (8-point checklist). Max 2 gap-fill rounds.
6. **Template triage** — almost always Template 02 (Complex Task) for PRD creation.
7. **Build task file** — spawns `rf-task-builder` with full BUILD_REQUEST. Builder reads research notes + refs/ files + MDTM template.
8. **Verify task file** — checks frontmatter, phase completeness, B2 self-contained items, embedded agent prompts.

### 8.2 Stage B: Task file execution

Delegated entirely to the `/task` skill:
1. `/task` reads the MDTM task file and processes each checklist item via the F1 loop (READ -> IDENTIFY -> EXECUTE -> UPDATE -> REPEAT).
2. Subagents are spawned as specified in B2 self-contained items.
3. Phase-gate QA runs after each phase (Phase 2+).
4. On context compression or session restart, `/task` re-reads the task file and resumes from the first unchecked item.

### 8.3 Resumability

The MDTM task file provides automatic resume:
- Every completed step is a checked `[x]` box on disk.
- On restart, the skill finds the first unchecked `[ ]` item and resumes there.
- Research files written incrementally persist even if the agent is interrupted mid-investigation.
- No explicit `--resume` flag needed — it's inherent to the task file system.

### 8.4 Parallel execution strategy

- **Phase 2**: All research agents spawn simultaneously in a single message with multiple Agent tool calls.
- **Phase 3**: rf-analyst and rf-qa spawn in parallel. With >6 research files, multiple instances of each with assigned subsets.
- **Phase 4**: All web research agents spawn simultaneously.
- **Phase 5**: All synthesis agents spawn simultaneously. After completion, rf-analyst and rf-qa spawn in parallel. With >4 synth files, multiple partitioned instances.
- **Phase 6**: Sequential — assembler first, then structural QA, then qualitative QA (each depends on the prior).

### 8.5 Error handling

- **QA gate failure**: Triggers targeted fix cycles (max 3 for research, max 2 for synthesis). After max cycles, execution halts and issues are presented to the user.
- **Agent failure**: Individual agent failures are logged. Remaining agents continue. Failed investigations are noted in the gaps log.
- **Session interruption**: Resume from task file. Partial research files persist on disk.

---

## 9) End-to-End Workflow: PRD -> TDD -> Roadmap -> Tasklist -> Execution

The PRD skill is the starting point of the full product development pipeline.

### Stage A: PRD (product requirements) <- **This skill**
```
/prd Create a PRD for [product area]
```
Produces a comprehensive PRD at `docs/docs-product/tech/[feature]/PRD_[FEATURE].md` with research artifacts in `.dev/tasks/to-do/TASK-PRD-*/`.

### Stage B: TDD (technical design)
```
/tdd Create a TDD based on the PRD at docs/docs-product/tech/[feature]/PRD_[FEATURE].md
```
The PRD skill offers to invoke `/tdd` automatically after completion. Research files from the PRD investigation feed into the TDD.

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

---

## 10) Performance & Cost Expectations

### Execution time estimates

| Tier | Approximate Wall Time | Total Agents Spawned | Notes |
|------|----------------------|---------------------|-------|
| **Lightweight** | 5-10 minutes | 5-8 (2-3 research + 0-1 web + 2-3 synth + QA) | Fastest option. Single feature, narrow scope. |
| **Standard** | 15-30 minutes | 12-20 (4-6 research + 1-2 web + 6-9 synth + QA) | Most common. Full product area. |
| **Heavyweight** | 30-60 minutes | 20-35+ (6-10+ research + 2-4 web + 9 synth + QA with partitioning) | Platform-level PRDs. Multiple QA partitions. |

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
- **Network**: Web research agents require internet access for market data (Phase 4). Codebase-only runs skip Phase 4.
- **Session stability**: Long-running Heavyweight PRDs benefit from stable sessions. The MDTM task file provides resilience against interruptions, but frequent restarts add overhead from re-reading context.

---

## 11) Known Limitations & Gotchas

### Vague prompts produce broad, less actionable PRDs
**Symptom**: PRD covers too much surface area without depth in any single area.
**Cause**: When only the product name is provided (Scenario B), the skill does broad discovery and can't prioritize what matters for your specific decision.
**Workaround**: Always provide at minimum WHAT + WHY. Specifying WHERE (directories) dramatically focuses the investigation.

### Feature PRD vs Product PRD misclassification
**Symptom**: A feature PRD includes full TAM/SAM/SOM market sizing, or a product PRD skips competitive analysis.
**Cause**: The scope classification (Product PRD vs Feature PRD) is inferred from the request. Ambiguous requests may be misclassified.
**Workaround**: Explicitly state in your prompt: "This is a feature PRD for [X] within the [Y] platform" or "This is a standalone product PRD for [X]".

### Context compression during Heavyweight runs
**Symptom**: Phase 5 or 6 agents produce thinner output than Phase 2 agents.
**Cause**: Long Heavyweight runs may approach context limits. The task file ensures no steps are skipped, but agents spawned later in the session have less main-session context.
**Workaround**: The skill is designed to handle this — each agent is self-contained with full instructions. If quality degrades, restart the session; the skill resumes from the task file.

### Existing docs treated as ground truth
**Symptom**: PRD contains product capabilities that no longer exist in the codebase.
**Cause**: Despite the Documentation Staleness Protocol, Doc Analyst agents may miss stale claims if the original documentation is internally consistent but outdated.
**Workaround**: After PRD completion, review the `gaps-and-questions.md` file for `[UNVERIFIED]` tags. Cross-check any surprising product claims against the actual code.

### Web research agents blocked by network restrictions
**Symptom**: Phase 4 web research files are empty or contain only error messages.
**Cause**: Corporate networks, VPNs, or air-gapped environments may block web search.
**Workaround**: The skill continues without web research (Phase 4 is not a hard gate). Market data sections will be thinner. You can manually populate competitive analysis and market sizing data after PRD generation.

### Task file not found on resume
**Symptom**: Starting a new PRD for a product that already has a completed task file.
**Cause**: If all items in the existing task file are checked, the skill reports the PRD is already complete rather than starting a new one.
**Workaround**: If you need a fresh PRD, specify a different output path or rename/archive the existing `TASK-PRD-*` folder.

---

## 12) Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| Skill asks clarifying questions instead of starting | WHAT input is too vague to determine product scope | Provide at minimum a specific product area or feature name |
| Scope discovery takes unusually long | Large codebase with many matching files (Scenario B broad search) | Provide WHERE input to constrain the search space |
| Task builder produces malformed task file | Research notes are incomplete (failed sufficiency gate) | Check `research-notes.md` — ensure all 7 categories are populated |
| Research agents produce empty output files | Agent spawning failed or agent hit context limit immediately | Check agent error output; restart session to get fresh context |
| QA gate fails repeatedly (3+ fix cycles) | Fundamental gap in research coverage — targeted fixes insufficient | Review the QA report, manually investigate the flagged areas, then restart |
| Synthesis agents produce placeholder content | Research files don't cover the template sections assigned to that synth file | Check synthesis mapping — the research directory may be missing a topic |
| Assembly produces a PRD missing sections | Synthesis files incomplete or missing | Check `synthesis/` directory — ensure all `synth-*.md` files are present and populated |
| Final PRD line count exceeds tier budget | Synthesis agents over-produced; assembler didn't trim | The rf-qa report-validation agent should catch this. If it persists, manually trim. |
| "PRD already complete" when you want a fresh start | Prior `TASK-PRD-*` folder exists with all items checked | Archive the old folder: `mv .dev/tasks/to-do/TASK-PRD-* .dev/tasks/done/` |
| PRD contains `[UNVERIFIED]` tags in final output | Doc-sourced claims could not be cross-validated against code | Review each tagged claim manually — the claim may be stale, planned, or in another repo |

---

## 13) Practical Use Cases

### Use case 1: Standard product PRD
```
/prd Create a PRD for the GameFrame AI multi-agent system for engineering planning.
Focus on backend/app/agents/ and backend/app/services/.
```
Standard tier, 4-6 codebase agents + 1-2 web agents. All 32 template sections populated.

### Use case 2: Feature-scoped PRD
```
/prd Create a PRD for the wizard configuration system. We want to add new stages
and need to document current vs planned capabilities. Key areas: frontend/app/wizard/.
```
Feature PRD — sections S5, S8, S9, S16-S18 abbreviated or N/A. References Platform PRD.

### Use case 3: Comprehensive platform PRD
```
/prd Create a detailed, comprehensive PRD for the entire platform. We need this for
Series A investor materials. Include full market analysis and competitive positioning.
```
Heavyweight tier (user said "detailed, comprehensive"), 6-10+ codebase agents, 2-4 web agents, 1500-2500 lines.

### Use case 4: PRD from existing documentation
```
/prd Create a PRD for pixel streaming by consolidating the existing docs at
docs/docs-product/tech/streaming/. Need a single source of truth.
```
Consolidation mode — Doc Analyst agents cross-validate existing docs against code. Document Provenance appendix added.

### Use case 5: Resume interrupted PRD
```
/prd Create a PRD for the task management system.
```
If a `TASK-PRD-*` folder exists for "task management", the skill reads the task file and resumes from the first unchecked item.

### Use case 6: PRD feeding into TDD
```
/prd Create a PRD for the canvas roadmap feature. After completion, I want to create
a technical design document from it.
```
After PRD completion, Phase 7 offers to invoke `/tdd` with the PRD and research artifacts as input.

### Use case 7: Investor-focused PRD with market emphasis
```
/prd Create a PRD for the AI assistant product. This is for our Series A deck —
emphasize market sizing, competitive positioning, and value proposition.
```
Product PRD with emphasis on S5 (Business Context), S8 (Value Proposition), S9 (Competitive Analysis). Web research agents focus on TAM/SAM/SOM data and competitive landscape.

### Use case 8: Narrow feature with no web research needed
```
/prd Create a PRD for the notification preference system. Engineering-only — no market
context needed. Focus on frontend/src/notifications/ and backend/api/preferences/.
```
Lightweight tier. Web research agents skipped (0 web agents). Fast execution focused on codebase evidence only.

---

## 14) Quick Reference

### Invocation
```
/prd [description]
```

### Key behaviors
- Automatically selects tier (Lightweight/Standard/Heavyweight) based on scope
- Resumes from existing task files if found
- Asks for clarification only when genuine ambiguity exists
- Offers downstream TDD creation after completion

### Output locations
- Task artifacts: `.dev/tasks/to-do/TASK-PRD-YYYYMMDD-HHMMSS/`
- Final PRD: `docs/docs-product/tech/[feature-name]/PRD_[FEATURE-NAME].md`

### Quality guarantees
- 3 independent QA gates (research, synthesis, assembly)
- Documentation staleness cross-validation
- Template conformance checking
- Zero-trust verification (assume wrong until proven correct)

### Failure modes prevented
- **Context rot** — isolated agents with incremental file writing
- **Shallow coverage** — parallel deep-dive investigation agents
- **Hallucinated requirements** — separated research/synthesis/assembly with verification
- **Quality drift** — rf-analyst + rf-qa + rf-qa-qualitative at three gates
