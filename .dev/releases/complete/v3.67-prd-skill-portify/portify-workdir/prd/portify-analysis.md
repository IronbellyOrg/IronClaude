---
source_skill: prd
source_command: (none — skill-triggered via frontmatter)
step_count: 15
parallel_groups: 5
gate_count: 10
agent_count: 7
complexity: high
status: completed
---

# Portification Analysis: PRD Creator

## Source Components

| Component | Path | Lines | Purpose |
|-----------|------|-------|---------|
| Skill | `src/superclaude/skills/prd/SKILL.md` | 455 | Main orchestration: scope discovery, task file creation, execution delegation |
| Skill (original) | `src/superclaude/skills/prd/SKILL_Original.md` | 1,373 | Pre-refactor monolithic version (reference only) |
| Refactoring spec | `src/superclaude/skills/prd/REFACTORING_SPEC.md` | 423 | Documents the modularization from 1,373 → 455 lines |
| Ref: Agent Prompts | `src/superclaude/skills/prd/refs/agent-prompts.md` | 422 | 8 agent prompt templates (codebase, web, synthesis, analyst, QA x3, assembly) |
| Ref: Build Request | `src/superclaude/skills/prd/refs/build-request-template.md` | 165 | BUILD_REQUEST template passed to rf-task-builder |
| Ref: Synthesis Mapping | `src/superclaude/skills/prd/refs/synthesis-mapping.md` | 142 | 9-row synth-file-to-PRD-section mapping + output structure |
| Ref: Validation Checklists | `src/superclaude/skills/prd/refs/validation-checklists.md` | 153 | Synthesis QA (12 items), assembly process (steps 8-11), validation checklist (18+4 items), content rules (10 rules) |
| Ref: Operational Guidance | `src/superclaude/skills/prd/refs/operational-guidance.md` | 110 | Critical rules (16), research quality signals, artifact locations, update protocol, session mgmt |
| Agent: rf-task-builder | `.claude/agents/rf-task-builder.md` | — | Creates MDTM task files from BUILD_REQUEST |
| Agent: rf-task-researcher | `.claude/agents/rf-task-researcher.md` | — | Optional: deeper scope discovery for complex products |
| Agent: rf-analyst | `.claude/agents/rf-analyst.md` | — | Completeness verification + synthesis review |
| Agent: rf-qa | `.claude/agents/rf-qa.md` | — | Research gate, synthesis gate, report validation |
| Agent: rf-qa-qualitative | `.claude/agents/rf-qa-qualitative.md` | — | Content/scope/logic quality review (23-item checklist) |
| Agent: rf-assembler | `.claude/agents/rf-assembler.md` | — | Consolidates synthesis files into final PRD |
| **Total source content** | | **~2,820** | **Skill (455) + 5 refs (992) + original (1,373)** |

## Workflow Architecture

The PRD skill has a **two-stage architecture**:

- **Stage A** (Orchestrator-driven): Pre-task-file creation. The orchestrator reads the user request, discovers the product space, writes research notes, and spawns `rf-task-builder` to create an MDTM task file.
- **Stage B** (Task-file-driven): Delegates to the `/task` skill which reads the generated task file and executes each checklist item via the F1 loop (READ → IDENTIFY → EXECUTE → UPDATE → REPEAT).

### Phase Loading Contract

The skill enforces strict phase isolation for refs loading:

| Phase | Actor | Loads | Forbidden |
|-------|-------|-------|-----------|
| Stage A.1–A.6 | Orchestrator | SKILL.md only | All refs/ |
| Stage A.7 (orch) | Orchestrator | refs/build-request-template.md | Other refs/ |
| Stage A.7 (builder) | rf-task-builder | refs/agent-prompts.md, refs/synthesis-mapping.md, refs/validation-checklists.md, refs/operational-guidance.md | — |
| Stage B | /task execution | Generated task file | All refs/ |

This means the CLI pipeline must replicate this isolation model.

---

## Step Graph

### Step 1: Check Existing Work
- **Type**: pure-programmatic
- **Inputs**: User's product identifier
- **Output**: Existing task state (none / resumable / complete)
- **Gate**: EXEMPT
- **Agent**: none
- **Parallel**: no
- **Timeout**: 10s
- **Retry**: 0
- **Notes**: Glob `.dev/tasks/to-do/TASK-PRD-*/` for matching folders. Read task file frontmatter to determine status. Check for `research-notes.md` with `Status: Complete`. Returns one of: `no_existing` (continue to Step 2), `resume_stage_a` (skip to Step 5 with existing research notes), `resume_stage_b` (skip to Step 9 with existing task file), `already_complete` (inform user).

### Step 2: Parse PRD Request
- **Type**: claude-assisted
- **Inputs**: User message, product identifier
- **Output**: `{work_dir}/parsed-request.json` (structured: GOAL, WHY, WHERE, OUTPUT_TYPE, PRODUCT_SLUG, PRD_SCOPE, SCENARIO)
- **Gate**: STANDARD (required fields: GOAL, PRODUCT_SLUG, PRD_SCOPE, SCENARIO)
- **Agent**: claude subprocess
- **Parallel**: no
- **Timeout**: 120s
- **Retry**: 1
- **Notes**: Extracts 7 structured fields from natural language. Must classify scope (Product vs Feature PRD) and triage into Scenario A (explicit) or B (vague). If prompt is too incomplete (no product identified), the gate fails and pipeline HALTs with a prompt template for the user.

### Step 3: Scope Discovery
- **Type**: claude-assisted
- **Inputs**: `parsed-request.json`, project codebase
- **Output**: `{task_dir}/scope-discovery-raw.md` (unstructured findings)
- **Gate**: STANDARD (min 50 lines, required sections: EXISTING_FILES, PATTERNS, FEATURES)
- **Agent**: claude subprocess (with Glob/Grep/Read tools)
- **Parallel**: no
- **Timeout**: 300s
- **Retry**: 1
- **Notes**: Depth varies by scenario: Scenario A (focused — verify user-specified paths, scan for related code), Scenario B (broad — full codebase scan). Enumerates files, maps subsystems, identifies integration points, plans research assignments, identifies web research topics, determines synthesis mapping, selects tier. May optionally spawn rf-task-researcher for complex products.

### Step 4: Write Research Notes
- **Type**: hybrid (programmatic template + claude content)
- **Inputs**: `scope-discovery-raw.md`, `parsed-request.json`
- **Output**: `{task_dir}/research-notes.md`
- **Gate**: STRICT
  - Required frontmatter: Date, Scenario, Tier, PRD Scope
  - Required sections (7): EXISTING_FILES, PATTERNS_AND_CONVENTIONS, FEATURE_ANALYSIS, RECOMMENDED_OUTPUTS, SUGGESTED_PHASES, TEMPLATE_NOTES, AMBIGUITIES_FOR_USER
  - Semantic checks: each SUGGESTED_PHASES entry has (topic, agent_type, files, output_path); doc-sourced claims tagged with verification status
- **Agent**: claude subprocess
- **Parallel**: no
- **Timeout**: 180s
- **Retry**: 1
- **Notes**: This file is the primary contract between orchestrator and task builder. The gate is STRICT because downstream quality depends entirely on this file's completeness.

### Step 5: Review Research Sufficiency
- **Type**: hybrid
- **Inputs**: `{task_dir}/research-notes.md`
- **Output**: `{work_dir}/sufficiency-review.json` (verdict + gap list)
- **Gate**: STANDARD (required field: verdict = PASS|FAIL)
- **Agent**: claude subprocess
- **Parallel**: no
- **Timeout**: 120s
- **Retry**: 2 (up to 2 gap-fill rounds)
- **Notes**: Evaluates 8 criteria: (1) scope bounded, (2) subsystems identified, (3) integration points mapped, (4) docs inventoried, (5) assignments concrete, (6) section mapping reasonable, (7) stakeholders identified, (8) doc claims tagged. If FAIL, loops back: either self-fills gaps or spawns rf-task-researcher. Max 2 gap-fill rounds, then proceed with warnings.

### Step 6: Template Triage
- **Type**: pure-programmatic
- **Inputs**: `{task_dir}/research-notes.md` (Tier field)
- **Output**: template selection (01 or 02)
- **Gate**: EXEMPT
- **Agent**: none
- **Parallel**: no
- **Timeout**: 5s
- **Retry**: 0
- **Notes**: Almost always returns Template 02 for PRD creation. Template 01 only for simple PRD updates. The decision is a single if-else based on the Tier and request type in the research notes.

### Step 7: Build Task File
- **Type**: claude-assisted
- **Inputs**: `refs/build-request-template.md` (customized), `{task_dir}/research-notes.md`, `refs/agent-prompts.md`, `refs/synthesis-mapping.md`, `refs/validation-checklists.md`, `refs/operational-guidance.md`
- **Output**: `{task_dir}/TASK-PRD-{timestamp}.md`
- **Gate**: STRICT
  - Required frontmatter: id, title, status, complexity, created_date, template
  - Min lines: 200 (Lightweight) / 400 (Standard) / 600 (Heavyweight)
  - Semantic checks: (1) all planned phases present as checklist items, (2) B2 self-contained pattern (no references to "see above"), (3) agent prompts fully embedded, (4) phases 2/3/4/5 include parallel spawning instructions, (5) phase 6 uses rf-assembler, (6) phase 7 includes task-completion items
- **Agent**: rf-task-builder (via claude subprocess)
- **Parallel**: no
- **Timeout**: 600s
- **Retry**: 1
- **Notes**: This is the most complex Claude-assisted step. The BUILD_REQUEST template is filled from the parsed request and research notes, then passed as the prompt. The builder loads 4 refs files and generates a complete MDTM task file with all phases encoded as B2 self-contained checklist items. The gate enforces 6 structural semantic checks to catch common builder errors.

### Step 8: Verify Task File
- **Type**: hybrid
- **Inputs**: `{task_dir}/TASK-PRD-{timestamp}.md`
- **Output**: `{work_dir}/task-verification.json` (verdict + issues)
- **Gate**: STANDARD (required field: verdict = PASS|FAIL)
- **Agent**: claude subprocess (for content verification) + programmatic (structural checks)
- **Parallel**: no
- **Timeout**: 120s
- **Retry**: 1 (re-run builder with corrections if FAIL)
- **Notes**: Programmatic checks: frontmatter YAML valid, all `## Phase N` headers present, checklist items start with `- [ ]`. Claude checks: B2 self-contained pattern, agent prompts embedded, no "see above" references, parallel spawning instructions present.

### Step 9: Preparation
- **Type**: hybrid
- **Inputs**: Task file, `{task_dir}/research-notes.md`, PRD template
- **Output**: `{task_dir}/.preparation-complete` marker + updated task file status
- **Gate**: LIGHT (marker file exists)
- **Agent**: claude subprocess (for scope confirmation)
- **Parallel**: no
- **Timeout**: 120s
- **Retry**: 0
- **Notes**: Updates task status to "Doing", confirms scope from research notes, reads PRD template, creates task subfolders if not present. Mostly mechanical.

### Step 10: Deep Investigation
- **Type**: claude-assisted, **BATCHED PARALLEL**
- **Inputs**: Per-agent: file list + investigation topic from research notes
- **Output**: `{task_dir}/research/[NN]-[topic-name].md` (one per agent)
- **Gate**: STANDARD per file (min 50 lines, required sections: Summary, Gaps and Questions)
- **Agent**: N research agents (2-10+ based on tier)
- **Parallel**: yes — all research agents spawned in parallel via ThreadPoolExecutor
- **Timeout**: 600s per agent
- **Retry**: 1 per agent
- **Notes**: Dynamic step count determined by scope discovery. Agent count follows tier: Lightweight 2-3, Standard 4-6, Heavyweight 6-10+. Each agent uses the Codebase Research Agent Prompt with customized topic, files, and output path. Incremental File Writing Protocol enforced. Documentation Staleness Protocol mandatory.

### Step 11: Research Completeness Verification
- **Type**: claude-assisted, **PARALLEL (2 agents) + FIX CYCLE**
- **Inputs**: All research files in `{task_dir}/research/`, `{task_dir}/research-notes.md`
- **Output**: `{task_dir}/qa/analyst-completeness-report.md`, `{task_dir}/qa/qa-research-gate-report.md`, `{task_dir}/gaps-and-questions.md`
- **Gate**: STRICT
  - Required: QA verdict = PASS
  - Semantic checks: (1) all product areas covered, (2) evidence cites file paths, (3) doc-sourced claims tagged, (4) all files Status: Complete
  - BLOCKING gate — FAIL halts pipeline
- **Agent**: rf-analyst + rf-qa (parallel), then gap-filling agents (if FAIL)
- **Parallel**: yes — analyst and QA run in parallel; partitioned if >6 research files
- **Timeout**: 300s per agent, 900s total with fix cycles
- **Retry**: 3 fix cycles max, then HALT
- **Notes**: Two independent verification streams. rf-analyst applies 8-item completeness checklist. rf-qa applies 11-item research gate checklist. If FAIL, spawn targeted gap-filling agents, then re-run rf-qa with qa_phase: "fix-cycle". Max 3 fix cycles. Partitioning threshold: >6 research files → multiple analyst/QA instances with assigned_files subsets.

### Step 12: Web Research
- **Type**: claude-assisted, **BATCHED PARALLEL**
- **Inputs**: Gaps from Step 11, web research topics from research notes
- **Output**: `{task_dir}/research/web-[NN]-[topic].md` (one per agent)
- **Gate**: STANDARD per file (min 30 lines, required sections: Key External Findings, Recommendations)
- **Agent**: N web research agents (0-4 based on tier)
- **Parallel**: yes — all web agents spawned in parallel
- **Timeout**: 300s per agent
- **Retry**: 1 per agent
- **Notes**: Dynamic step count. Topics include: competitive landscape, TAM/SAM/SOM, industry standards, technology trends, user research, pricing models. Each agent uses the Web Research Agent Prompt. Source URLs mandatory. May be skipped for Lightweight tier (0 agents).

### Step 13: Synthesis + QA Gate
- **Type**: claude-assisted, **BATCHED PARALLEL → PARALLEL QA**
- **Inputs**: All research files, web research files, PRD template
- **Output**: `{task_dir}/synthesis/synth-[NN]-[topic].md` (9 files per mapping table), `{task_dir}/qa/analyst-synthesis-review.md`, `{task_dir}/qa/qa-synthesis-gate-report.md`
- **Gate**: STRICT
  - Per synth file: required sections match PRD template, tables use correct column structure, no fabrication
  - QA verdict: PASS required
  - BLOCKING gate
- **Agent**: 9 synthesis agents (parallel) → then rf-analyst + rf-qa (parallel)
- **Parallel**: yes — two parallel phases (synth agents, then QA agents); partitioned if >4 synth files
- **Timeout**: 300s per synth agent, 300s per QA agent, 1200s total with fix cycles
- **Retry**: 2 fix cycles for synthesis QA
- **Notes**: Synthesis agents use the Synthesis Mapping Table to map research files to template sections. 9 synth files standard (see mapping table in refs/synthesis-mapping.md). After synthesis, parallel QA: rf-analyst (synthesis-review) + rf-qa (synthesis-gate, fix_authorization: true). Partitioning threshold: >4 synth files. Max 2 fix cycles for synthesis QA.

### Step 14: Assembly & Validation
- **Type**: claude-assisted, **SEQUENTIAL (3 agents)**
- **Inputs**: All synth files (ordered), PRD template, validation checklists, content rules
- **Output**: Final PRD at configured output path, `{task_dir}/qa/qa-report-validation.md`, `{task_dir}/qa/qa-qualitative-review.md`
- **Gate**: STRICT
  - Required: all 28+ template sections present (or N/A with rationale)
  - Required frontmatter: id, title, status, created_date, tags, depends_on
  - Line count within tier budget
  - Semantic checks: 18-item validation checklist + 4 content quality checks + 23-item qualitative checklist
  - BLOCKING gate
- **Agent**: rf-assembler → rf-qa (report-validation, fix_authorization: true) → rf-qa-qualitative (prd-qualitative, fix_authorization: true)
- **Parallel**: no — strictly sequential (assembler must complete before structural QA, structural QA before qualitative QA)
- **Timeout**: 600s assembler, 300s structural QA, 300s qualitative QA
- **Retry**: 1 (re-run QA after fixes)
- **Notes**: Three-agent sequential chain. rf-assembler reads synth files in order and writes PRD incrementally (section by section). Must be single agent for cross-section consistency. rf-qa validates structure (18+4 checklist items) and fixes in-place. rf-qa-qualitative validates content/logic (23 items) and fixes in-place. Zero leniency — all severity levels must be addressed.

### Step 15: Present & Complete
- **Type**: hybrid
- **Inputs**: Final PRD, task file, research/synth artifact paths
- **Output**: Updated task file (status: Done, frontmatter updated), user presentation
- **Gate**: LIGHT (task file frontmatter status = Done)
- **Agent**: claude subprocess (for presentation generation)
- **Parallel**: no
- **Timeout**: 60s
- **Retry**: 0
- **Notes**: Presents to user: PRD location, line count, tier, sections populated vs skipped, artifact locations, gaps needing manual review. Offers downstream document creation (TDD). If consolidating existing docs, presents source docs for archival decision. Updates task file frontmatter: status → Done, completion_date → today.

---

## Parallel Groups

| Group | Steps | Max Concurrency | Rationale |
|-------|-------|-----------------|-----------|
| 1 | Step 10 (Deep Investigation) | 2-10+ agents | Independent research agents, each investigating different product areas |
| 2 | Step 11 (Research QA) | 2 agents (analyst + QA), partitioned to N×2 if >6 files | Independent quality streams with different checklists |
| 3 | Step 12 (Web Research) | 0-4 agents | Independent web research topics |
| 4a | Step 13 (Synthesis) | 9 agents | Independent synthesis files, each mapping different research to different template sections |
| 4b | Step 13 (Synthesis QA) | 2 agents, partitioned to N×2 if >4 files | Independent QA streams after all synthesis completes |

**Dynamic step counts**: Groups 1, 3, and 4a have step counts determined at runtime by scope discovery results. The pipeline needs a `build_steps()` function that reads the research notes and generates Step objects dynamically.

---

## Gates Summary

| Step | Tier | Required Frontmatter | Min Lines | Semantic Checks | Mode |
|------|------|---------------------|-----------|-----------------|------|
| 1. Check Existing | EXEMPT | — | — | — | — |
| 2. Parse Request | STANDARD | GOAL, PRODUCT_SLUG, PRD_SCOPE, SCENARIO | — | Required fields present and non-empty | BLOCKING |
| 3. Scope Discovery | STANDARD | — | 50 | Required sections: EXISTING_FILES, PATTERNS, FEATURES | BLOCKING |
| 4. Research Notes | STRICT | Date, Scenario, Tier, PRD Scope | 100 | 7 required sections; per-agent detail in SUGGESTED_PHASES; doc claims tagged | BLOCKING |
| 5. Sufficiency Review | STANDARD | — | — | verdict field = PASS or FAIL | BLOCKING |
| 6. Template Triage | EXEMPT | — | — | — | — |
| 7. Build Task File | STRICT | id, title, status, complexity, created_date, template | 200-600 (tier) | 6 structural checks (phases present, B2 pattern, prompts embedded, parallel instructions, assembler, completion items) | BLOCKING |
| 8. Verify Task File | STANDARD | — | — | verdict = PASS or FAIL | BLOCKING |
| 9. Preparation | LIGHT | — | — | marker file exists | BLOCKING |
| 10. Deep Investigation | STANDARD (per file) | — | 50 | Required sections: Summary, Gaps and Questions | BLOCKING |
| 11. Research QA | STRICT | — | — | QA verdict = PASS; all product areas covered; evidence cites file paths; doc claims tagged | BLOCKING |
| 12. Web Research | STANDARD (per file) | — | 30 | Required sections: Key External Findings, Recommendations | BLOCKING |
| 13. Synthesis + QA | STRICT | — | — | Template sections match; no fabrication; QA verdict = PASS | BLOCKING |
| 14. Assembly & Validation | STRICT | id, title, status, created_date, tags, depends_on | tier-dependent | 18+4+23 checklist items; line count within budget | BLOCKING |
| 15. Present & Complete | LIGHT | — | — | Task file status = Done | BLOCKING |

---

## Agent Delegation Map

| Agent | Used In Steps | Parallel | Contract |
|-------|--------------|----------|----------|
| Claude subprocess (generic) | 2, 3, 4, 5, 8, 9, 15 | no | Prompt + gate validation |
| rf-task-builder | 7 | no | BUILD_REQUEST → MDTM task file |
| rf-task-researcher | 3 (optional) | no | RESEARCH_REQUEST → research notes |
| Research agents (generic) | 10 | yes (N agents) | Codebase Research Agent Prompt → research file |
| Web research agents (generic) | 12 | yes (N agents) | Web Research Agent Prompt → web research file |
| Synthesis agents (generic) | 13 (phase 1) | yes (9 agents) | Synthesis Agent Prompt → synth file |
| rf-analyst | 11, 13 (phase 2) | yes (with rf-qa) | Completeness verification / synthesis review → analyst report |
| rf-qa | 11, 13 (phase 2) | yes (with rf-analyst) | Research gate / synthesis gate → QA report |
| rf-assembler | 14 (phase 1) | no (must be single) | Synth files → assembled PRD |
| rf-qa (report-validation) | 14 (phase 2) | no (sequential) | Assembled PRD → structural QA report (fix auth: true) |
| rf-qa-qualitative | 14 (phase 3) | no (sequential) | Assembled PRD → qualitative QA report (fix auth: true) |

---

## Data Flow Diagram

```
[user request]
      ↓
  Step 1: Check Existing ──→ (resume path if existing)
      ↓
  Step 2: Parse Request ──→ parsed-request.json
      ↓
  Step 3: Scope Discovery ──→ scope-discovery-raw.md
      ↓
  Step 4: Write Research Notes ──→ research-notes.md
      ↓
  Step 5: Sufficiency Review ──→ sufficiency-review.json
      ↓ (loop up to 2× on FAIL)
  Step 6: Template Triage ──→ template selection
      ↓
  Step 7: Build Task File ──→ TASK-PRD-{ts}.md
      ↓
  Step 8: Verify Task File ──→ task-verification.json
      ↓
  Step 9: Preparation ──→ .preparation-complete
      ↓
  Step 10: Deep Investigation (N parallel)
      ├── agent-1 → research/01-topic-a.md
      ├── agent-2 → research/02-topic-b.md
      └── agent-N → research/NN-topic-n.md
      ↓
  Step 11: Research QA (2 parallel + fix cycles)
      ├── rf-analyst → qa/analyst-completeness-report.md
      └── rf-qa → qa/qa-research-gate-report.md
      ↓ (PASS required, up to 3 fix cycles)
     gaps-and-questions.md
      ↓
  Step 12: Web Research (N parallel)
      ├── web-agent-1 → research/web-01-topic.md
      └── web-agent-N → research/web-NN-topic.md
      ↓
  Step 13a: Synthesis (9 parallel)
      ├── synth-1 → synthesis/synth-01-exec-problem-vision.md
      ├── synth-2 → synthesis/synth-02-business-market.md
      └── synth-9 → synthesis/synth-09-resources-maintenance.md
      ↓
  Step 13b: Synthesis QA (2 parallel + fix cycles)
      ├── rf-analyst → qa/analyst-synthesis-review.md
      └── rf-qa → qa/qa-synthesis-gate-report.md
      ↓ (PASS required, up to 2 fix cycles)
  Step 14a: Assembly
      rf-assembler → final PRD
      ↓
  Step 14b: Structural QA
      rf-qa (report-validation) → qa/qa-report-validation.md
      ↓
  Step 14c: Qualitative QA
      rf-qa-qualitative → qa/qa-qualitative-review.md
      ↓
  Step 15: Present & Complete
      → user presentation + task file updated
```

---

## Classification Summary

| Category | Count | Steps |
|----------|-------|-------|
| Pure Programmatic | 3 | Step 1 (Check Existing), Step 6 (Template Triage), plus inventory/filtering utilities |
| Hybrid | 4 | Step 4 (Research Notes), Step 5 (Sufficiency Review), Step 8 (Verify Task File), Step 15 (Present & Complete) |
| Claude-Assisted | 8 | Step 2 (Parse Request), Step 3 (Scope Discovery), Step 7 (Build Task File), Step 9 (Preparation), Step 10 (Deep Investigation), Step 11 (Research QA), Step 12 (Web Research), Step 13 (Synthesis + QA), Step 14 (Assembly & Validation) |
| Pure Inference | 0 | — |

### Pure Programmatic Functions

These operations should be Python functions, not Claude subprocesses:

| Function | Current Form | Proposed Implementation |
|----------|-------------|------------------------|
| `check_existing_work()` | Orchestrator reads `.dev/tasks/to-do/TASK-PRD-*/` | `glob.glob()` + read frontmatter YAML + return state enum |
| `select_template()` | Orchestrator picks 01 or 02 | Single if-else: `return 2 if tier != 'update' else 1` |
| `create_task_dirs()` | Orchestrator creates folders | `Path.mkdir(parents=True, exist_ok=True)` for research/, synthesis/, qa/, reviews/ |
| `discover_research_files()` | After Step 10 | `glob.glob('research/[0-9]*.md')` + validate Status: Complete |
| `discover_synth_files()` | After Step 13a | `glob.glob('synthesis/synth-*.md')` + validate section headers |
| `partition_files()` | Before Step 11/13b | Divide file list into N partitions based on thresholds |
| `validate_task_file_structure()` | Part of Step 8 | Regex-based: YAML frontmatter, `## Phase N` headers, `- [ ]` items |
| `check_line_count()` | Part of Step 14 gate | `len(content.splitlines())` vs tier budget |
| `validate_frontmatter_fields()` | Part of gates | Regex extraction + field presence check |
| `compile_gaps()` | After Step 11 | Merge gaps from all research files into single file |
| `merge_qa_partition_reports()` | After Step 11/13b partitions | Concatenate numbered reports into single report |
| `build_steps_dynamic()` | Before Step 10/12/13 | Read research notes, generate Step objects with counts from tier |

---

## Recommendations

### 1. Dynamic Step Generation is Critical

Steps 10, 12, and 13 have agent counts determined at runtime. The executor needs a `build_investigation_steps()`, `build_web_research_steps()`, and `build_synthesis_steps()` function that reads the research notes and generates Step objects. This is a first-class design concern, not an afterthought.

### 2. Fix Cycle Loops Need Special Executor Logic

Steps 11 and 13b have BLOCKING gates with fix cycles (3 max for research, 2 max for synthesis). The executor must support: run QA → if FAIL → spawn gap-filling agents → re-run QA → repeat up to N times → HALT on exhaustion. This is not a simple retry — it's a conditional re-execution with different prompts.

### 3. Three Distinct Parallel Patterns

| Pattern | Example | Implementation |
|---------|---------|----------------|
| Fan-out (N identical agents) | Step 10 research agents | ThreadPoolExecutor with N workers, each running ClaudeProcess |
| Dual-stream (2 independent agents) | Step 11 analyst + QA | ThreadPoolExecutor with 2 workers |
| Partitioned fan-out | Step 11 with >6 files | Calculate partitions, spawn N×2 agents with assigned_files |

### 4. The BUILD_REQUEST is a Complex Prompt Contract

Step 7 (Build Task File) has the most complex prompt construction: the BUILD_REQUEST template must be filled with values from Steps 2-6, then 4 refs files must be loaded as context. This is the highest-risk Claude-assisted step — the gate must be strict.

### 5. Resume Semantics are Well-Defined

The skill already has robust resume points:
- Step 1 detects prior work and routes to the correct resume point
- Step 5 can resume from existing research notes
- Stage B (Steps 9-15) resumes from the first unchecked task file item

The CLI pipeline should preserve these resume semantics with exact resume commands.

### 6. Phase Loading Contract Becomes Config Isolation

The skill's phase loading contract (which refs are visible at which phase) translates to subprocess isolation in the CLI: each subprocess gets only the refs files it's allowed to see, not the full set.

### 7. Tier-Dependent Parameters

Multiple steps have tier-dependent behavior:

| Parameter | Lightweight | Standard | Heavyweight |
|-----------|-------------|----------|-------------|
| Research agents | 2-3 | 4-6 | 6-10+ |
| Web research agents | 0-1 | 1-2 | 2-4 |
| Min research lines | 50 | 50 | 50 |
| Task file min lines | 200 | 400 | 600 |
| PRD line budget | 400-800 | 800-1,500 | 1,500-2,500 |
| QA partitioning | unlikely | possible | likely |
| Synthesis files | 5-7 | 9 | 9-12 |
