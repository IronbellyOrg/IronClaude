```yaml
---
title: "PRD Creator CLI Pipeline (Portification)"
version: "1.0.0"
status: draft
feature_id: FR-PRD-CLI
parent_feature: superclaude-cli
spec_type: portification
complexity_score: 0.85
complexity_class: HIGH
target_release: v3.67-prd-skill-portify
authors: [user, claude]
created: 2026-04-12
quality_scores:
  clarity: 8.5
  completeness: 8.4
  testability: 8.2
  consistency: 8.3
  overall: 8.4
---
```

## 1. Problem Statement

The PRD Creator skill (`src/superclaude/skills/prd/`) is a multi-agent, multi-phase workflow that relies entirely on Claude's inference for orchestration. It produces comprehensive Product Requirements Documents through a two-stage pipeline: scope discovery and task file creation (Stage A), then task-file-driven execution via the `/task` skill (Stage B). The workflow involves 7 agent types, 15 logical steps, 5 parallel groups, and multiple QA fix cycles.

This inference-only orchestration creates several operational problems:
- **Non-deterministic control flow** -- the orchestrator may skip phases, under-scope research, or fail to enforce quality gates depending on context window state
- **No resume capability** -- if a run fails partway through (budget exhaustion, timeout, crash), the entire pipeline must restart from scratch
- **No budget management** -- a 15-step pipeline with 10-20+ subprocesses has no mechanism to track turn consumption or prevent budget exhaustion mid-run
- **No live monitoring** -- the user has no visibility into which agents are running, which have completed, or where quality gates failed
- **Inconsistent quality gates** -- gate enforcement depends on the orchestrator's reasoning, which varies between runs
- **No parallel execution control** -- inference-based "spawn agents in parallel" is a suggestion, not a guarantee

### 1.1 Evidence

| Evidence | Source | Impact |
|----------|--------|--------|
| PRD skill is 455 lines of orchestration logic + 992 lines of refs, all interpreted by inference | `src/superclaude/skills/prd/SKILL.md` + `refs/` | Behavior varies between runs; no structural guarantees |
| No existing CLI module for PRD creation | `src/superclaude/cli/` directory scan | Users cannot invoke PRD creation programmatically |
| Sprint and roadmap pipelines already exist as CLI modules | `src/superclaude/cli/sprint/`, `src/superclaude/cli/roadmap/` | Proven patterns exist for portification |
| The skill's phase loading contract (strict refs isolation per phase) cannot be enforced by inference alone | `SKILL.md` lines 125-145, Phase Loading Contract table | Refs leakage between phases degrades output quality |
| Fix cycles (3 for research, 2 for synthesis) require precise loop control | `refs/agent-prompts.md`, QA agent templates | Inference may skip fix cycles or retry blindly instead of spawning targeted gap-fillers |

### 1.2 Scope Boundary

**In scope**: Converting the PRD Creator skill's orchestration into a programmatic CLI pipeline (`src/superclaude/cli/prd/`) with deterministic control flow, formal gate validation, budget tracking, live monitoring, resume/retry, and parallel execution via `ThreadPoolExecutor`.

**Out of scope**: Modifying the PRD skill files themselves (`src/superclaude/skills/prd/`); changing the PRD template (`docs/docs-product/templates/prd_template.md`); modifying the agent definitions (`rf-task-builder`, `rf-analyst`, `rf-qa`, `rf-qa-qualitative`, `rf-assembler`); adding new PRD sections or changing the synthesis mapping.

## 2. Solution Overview

Create a new CLI module `src/superclaude/cli/prd/` that implements the PRD Creator workflow as a programmatic pipeline. The pipeline uses the sprint-style synchronous supervisor pattern with `ThreadPoolExecutor` for parallelism, formal `GateCriteria` validation at every step, `TurnLedger` budget tracking, and a Rich TUI for live monitoring.

The pipeline decomposes the PRD skill's 2-stage, 7-phase workflow into 15 discrete steps:
- **3 pure-programmatic steps** (file discovery, template selection, directory creation)
- **4 hybrid steps** (programmatic setup + Claude verification)
- **8 Claude-assisted steps** (content generation via Claude subprocesses)

Dynamic step generation handles the variable agent counts (research: 2-10+, web: 0-4, synthesis: 5-12) determined at runtime from scope discovery. Fix cycle execution for QA gates uses targeted gap-filling agents rather than blind retry.

### 2.1 Key Design Decisions

| Decision | Choice | Alternatives Considered | Rationale |
|----------|--------|------------------------|----------|
| Execution model | Synchronous supervisor + ThreadPoolExecutor | async/await, multiprocessing | Matches sprint/roadmap patterns; simpler debugging; no event loop complexity |
| Dynamic step generation | `build_*_steps()` functions called after prerequisites complete | Static max-count with skip logic | Agent counts vary 2-10x by tier; static allocation wastes budget |
| Fix cycle pattern | Targeted gap-filling agents + re-QA | Simple retry of failed step | QA failures require new investigation, not repeated identical prompts |
| Phase loading isolation | Subprocess `--file` args scoped per step | Pass all refs to every subprocess | Matches skill's phase loading contract; prevents context pollution |
| Gate validation | Programmatic `gate_passed()` with semantic check functions | Claude-based gate evaluation | Deterministic, consistent, no inference variance |
| Budget tracking | Reuse `TurnLedger` from sprint module | New budget system | Proven pattern; PRD pipeline is turn-heavy (300 default budget) |
| QA partitioning | Threshold-based (>6 research, >4 synth) | Always partition, never partition | Balances QA depth vs. subprocess count |
| Resume semantics | Step-level resume via `--resume <step-id>` | Phase-level resume, full restart | Fine-grained recovery minimizes re-work |

### 2.2 Workflow / Data Flow

```
[user request]
      |
  Step 1: check_existing_work()     [pure-programmatic]
      |                              (glob TASK-PRD-*/ dirs)
      v
  Step 2: parse_request              [claude-assisted]
      |                              -> parsed-request.json
      v
  Step 3: scope_discovery            [claude-assisted]
      |                              -> scope-discovery-raw.md
      v
  Step 4: write_research_notes       [hybrid]
      |                              -> research-notes.md
      v
  Step 5: review_sufficiency         [hybrid, retry x2]
      |                              -> sufficiency-review.json
      v
  Step 6: template_triage()          [pure-programmatic]
      |                              -> template-selection.json
      v
  Step 7: build_task_file            [claude-assisted]
      |                              -> TASK-PRD-{slug}.md
      v
  Step 8: verify_task_file           [hybrid, retry x1]
      |                              -> task-verification.json
      v
  Step 9: preparation                [hybrid]
      |                              -> .preparation-complete
      |
  === DYNAMIC STEP GENERATION ===
  (read research-notes.md, build Step objects)
      |
      v
  Step 10: investigation             [parallel fan-out, N=2-10+]
      |-- agent-01 -> research/01-topic-a.md
      |-- agent-02 -> research/02-topic-b.md
      |-- agent-NN -> research/NN-topic-n.md
      v
  Step 11: research_qa               [parallel dual-stream + fix cycles]
      |-- rf-analyst -> qa/analyst-completeness-report.md
      |-- rf-qa      -> qa/qa-research-gate-report.md
      |                [if FAIL: spawn gap-fillers, re-QA, max 3 cycles]
      v
  Step 12: web_research              [parallel fan-out, N=0-4]
      |-- web-01 -> research/web-01-competitive.md
      |-- web-NN -> research/web-NN-topic.md
      v
  Step 13a: synthesis                [parallel fan-out, N=9]
      |-- synth-01 -> synthesis/synth-01-exec-problem-vision.md
      |-- synth-09 -> synthesis/synth-09-resources-maintenance.md
      v
  Step 13b: synthesis_qa             [parallel dual-stream + fix cycles]
      |-- rf-analyst -> qa/analyst-synthesis-review.md
      |-- rf-qa      -> qa/qa-synthesis-gate-report.md
      |                [if FAIL: targeted fixes, re-QA, max 2 cycles]
      v
  Step 14a: assembly                 [sequential]
      |   rf-assembler -> final-prd.md
      v
  Step 14b: structural_qa            [sequential]
      |   rf-qa (report-validation) -> qa/qa-report-validation.md
      v
  Step 14c: qualitative_qa           [sequential]
      |   rf-qa-qualitative -> qa/qa-qualitative-review.md
      v
  Step 15: present_complete          [hybrid]
      |   -> completion-summary.md + user presentation
      v
  [done]
```

## 3. Functional Requirements

### FR-PRD.1: Existing Work Detection

**Description**: On pipeline start, scan `.dev/tasks/to-do/TASK-PRD-*/` for existing PRD task work matching the requested product. Route to the appropriate resume point based on work state.

**Acceptance Criteria**:
- [ ] Detects four states: `no_existing`, `resume_stage_a`, `resume_stage_b`, `already_complete`
- [ ] `resume_stage_a` skips Steps 1-4 and resumes from Step 5 with existing research notes
- [ ] `resume_stage_b` skips Steps 1-8 and resumes from Step 9 with existing task file
- [ ] `already_complete` informs user and exits without re-running
- [ ] Matching uses product name substring matching against research-notes.md content. Product names shorter than 3 characters require frontmatter `product_name` field match instead of full-content substring match to prevent false positives [F-008 INCORPORATED]

**Dependencies**: None (first step in pipeline)

### FR-PRD.2: Request Parsing

**Description**: Parse a natural-language user request into structured JSON fields required by downstream steps. Classify scope (product vs feature) and scenario (explicit vs vague).

**Acceptance Criteria**:
- [ ] Produces `parsed-request.json` with fields: GOAL, PRODUCT_NAME, PRODUCT_SLUG, PRD_SCOPE, SCENARIO, WHERE, WHY, TIER_RECOMMENDATION
- [ ] PRD_SCOPE correctly classifies as "product" or "feature"
- [ ] SCENARIO correctly classifies as "A" (explicit paths provided) or "B" (requires exploration)
- [ ] Gate validates all required fields present and non-empty
- [ ] Pipeline HALTs with user-facing error if no product can be identified

**Dependencies**: FR-PRD.1

### FR-PRD.3: Scope Discovery

**Description**: Explore the codebase to understand the product space, identify areas requiring research, and plan agent assignments.

**Acceptance Criteria**:
- [ ] Produces `scope-discovery-raw.md` with minimum 50 lines
- [ ] Contains sections: Project Overview, Directory Structure, Product Areas, Technology Stack, Existing Documentation, Integration Points, Complexity Assessment, Recommended Research Assignments
- [ ] Scenario A (explicit) verifies user-specified paths and scans for related code
- [ ] Scenario B (vague) performs full codebase scan

**Dependencies**: FR-PRD.2

### FR-PRD.4: Research Notes Generation

**Description**: Transform scope discovery into structured research notes that serve as the primary contract between orchestration and all downstream agents.

**Acceptance Criteria**:
- [ ] Produces `research-notes.md` with all 7 required sections: EXISTING_FILES, PATTERNS_AND_CONVENTIONS, FEATURE_ANALYSIS, RECOMMENDED_OUTPUTS, SUGGESTED_PHASES, TEMPLATE_NOTES, AMBIGUITIES_FOR_USER
- [ ] Frontmatter includes Date, Scenario, Tier fields
- [ ] Each SUGGESTED_PHASES entry has topic, agent_type, files, output_path
- [ ] Agent count follows tier: lightweight 2-3, standard 4-6, heavyweight 6-10+
- [ ] STRICT gate validates all sections present and agent detail complete

**Dependencies**: FR-PRD.3

### FR-PRD.5: Research Sufficiency Review

**Description**: Evaluate research notes completeness and identify gaps before spawning agents. Supports up to 2 gap-fill rounds.

**Acceptance Criteria**:
- [ ] Produces `sufficiency-review.json` with verdict (PASS/FAIL) and gap list
- [ ] PASS requires coverage_score >= 80 and no critical gaps
- [ ] On FAIL, either self-fills gaps or spawns rf-task-researcher
- [ ] Maximum 2 gap-fill rounds, then proceeds with warnings
- [ ] Gate validates verdict field present

**Dependencies**: FR-PRD.4

### FR-PRD.6: Template Triage

**Description**: Select MDTM template (01 or 02) based on request type. Pure-programmatic decision.

**Acceptance Criteria**:
- [ ] Returns Template 02 for all PRD creation requests
- [ ] Returns Template 01 only for simple PRD update requests
- [ ] No Claude subprocess -- runs as direct Python function call

**Dependencies**: FR-PRD.4

### FR-PRD.7: Task File Construction

**Description**: Generate a complete MDTM task file encoding the full PRD workflow as self-contained checklist items. The most complex Claude-assisted step.

**Acceptance Criteria**:
- [ ] Produces `TASK-PRD-{slug}.md` with valid YAML frontmatter (id, title, status, complexity, created_date, type, tier)
- [ ] Line count meets tier minimum: lightweight 200, standard 400, heavyweight 600
- [ ] All 7 PRD phases encoded as section headers
- [ ] All checklist items are self-contained (no "see above" references -- B2 pattern)
- [ ] Agent prompts fully embedded with specific files and output paths
- [ ] Phases 2/3/4/5 include parallel spawning instructions
- [ ] STRICT gate with 6 semantic checks validates structural requirements

**Dependencies**: FR-PRD.4, FR-PRD.5, FR-PRD.6

### FR-PRD.8: Task File Verification

**Description**: Independent verification of task file quality with structural + content checks.

**Acceptance Criteria**:
- [ ] Produces `task-verification.json` with verdict (PASS/FAIL) and issues list
- [ ] Programmatic checks: valid YAML frontmatter, all Phase N headers, checklist format
- [ ] Claude checks: B2 self-containment, embedded prompts, parallel instructions
- [ ] On FAIL, triggers re-build of task file with specific corrections

**Dependencies**: FR-PRD.7

### FR-PRD.9: Preparation

**Description**: Create task subdirectories and prepare for Stage B parallel execution.

**Acceptance Criteria**:
- [ ] Creates `research/`, `synthesis/`, `qa/`, `reviews/`, `results/` subdirectories
- [ ] Writes `.preparation-complete` marker with status summary
- [ ] Verifies all assigned output paths have existing parent directories

**Dependencies**: FR-PRD.8

### FR-PRD.10: Deep Investigation (Parallel)

**Description**: Spawn N research agents in parallel, each investigating a distinct product area as assigned in research notes.

**Acceptance Criteria**:
- [ ] Dynamic step count from research notes SUGGESTED_PHASES (2-10+ agents)
- [ ] Each agent uses Codebase Research Agent Prompt with topic-specific files
- [ ] Each agent produces `research/NN-topic.md` with min 50 lines
- [ ] Incremental File Writing Protocol enforced (create header, append sections)
- [ ] Documentation Staleness Protocol enforced (CODE-VERIFIED/CODE-CONTRADICTED/UNVERIFIED tags)
- [ ] All agents run in parallel via `ThreadPoolExecutor`
- [ ] Per-agent timeout: 600s, retry: 1
- [ ] Partial group failure strategy: if K of N agents fail, the pipeline continues with the K-N successful results; failed agents are logged with diagnostic output; the subsequent QA step (FR-PRD.11) evaluates whether the successful subset provides sufficient coverage [GAP-001 INCORPORATED]

**Dependencies**: FR-PRD.9

### FR-PRD.11: Research QA with Fix Cycles

**Description**: Verify research completeness via dual-stream QA (rf-analyst + rf-qa). On FAIL, spawn targeted gap-filling agents and re-run QA. Maximum 3 fix cycles.

**Acceptance Criteria**:
- [ ] rf-analyst applies 8-item completeness checklist
- [ ] rf-qa applies 11-item research gate checklist
- [ ] Both agents run in parallel
- [ ] Partitioned execution when >6 research files (N x 2 agents with assigned subsets)
- [ ] Partition reports merged into single report before verdict evaluation. Merge strategy: overall verdict is FAIL if ANY partition verdict is FAIL (pessimistic merge). Individual partition verdicts are preserved in the merged report for diagnostic purposes [GAP-005 INCORPORATED]
- [ ] On FAIL: QA report parsed for specific failures; targeted gap-filling agents spawned; re-QA run
- [ ] Maximum 3 fix cycles, then HALT with exhaustion message and resume command
- [ ] BLOCKING gate: pipeline proceeds only on PASS
- [ ] Produces `gaps-and-questions.md` compiling all gaps from research files

**Dependencies**: FR-PRD.10

### FR-PRD.12: Web Research (Parallel)

**Description**: Spawn N web research agents in parallel to gather external market/competitive intelligence.

**Acceptance Criteria**:
- [ ] Dynamic step count from research notes (0-4 agents by tier)
- [ ] Each agent uses Web Research Agent Prompt with specific topic and codebase context
- [ ] Each agent produces `research/web-NN-topic.md` with min 30 lines
- [ ] Source URLs required for every external claim
- [ ] May be empty for lightweight tier (0 agents)
- [ ] All agents run in parallel via `ThreadPoolExecutor`

**Dependencies**: FR-PRD.11

### FR-PRD.13: Synthesis + Synthesis QA

**Description**: 9 synthesis agents run in parallel to produce PRD template sections from research. Then dual-stream QA verifies synthesis quality with up to 2 fix cycles.

**Acceptance Criteria**:
- [ ] 9 synthesis agents (per standard mapping table) run in parallel
- [ ] Each agent maps specific research files to specific PRD template sections
- [ ] Each synth file has min 80 lines with correct template section headers
- [ ] Synthesis QA: rf-analyst (synthesis-review) + rf-qa (synthesis-gate) run in parallel
- [ ] rf-qa has fix authorization: can fix issues in-place with Edit
- [ ] Partitioned QA when >4 synth files
- [ ] Maximum 2 fix cycles for synthesis QA
- [ ] BLOCKING gate: pipeline proceeds only on QA PASS

**Dependencies**: FR-PRD.12

### FR-PRD.14: Assembly and Validation

**Description**: Three-agent sequential chain: rf-assembler produces final PRD, rf-qa validates structure, rf-qa-qualitative validates content.

**Acceptance Criteria**:
- [ ] rf-assembler reads synth files in template order and writes PRD incrementally
- [ ] Incremental assembly: header first, then sections, then ToC, then appendices
- [ ] Cross-section consistency checked (personas in S7 match stories in S21.1, etc.)
- [ ] rf-qa applies 18-item structural validation checklist + 4 content quality checks
- [ ] rf-qa-qualitative applies qualitative review (scope correctness, coherence, actionability)
- [ ] Both QA agents have fix authorization (fix in-place with Edit)
- [ ] Line count within tier budget: lightweight 400-800, standard 800-1500, heavyweight 1500-2500
- [ ] Frontmatter includes id, title, status, created_date, tags
- [ ] No placeholder text remains (TODO, TBD, PLACEHOLDER)
- [ ] Strictly sequential execution: assembler -> structural QA -> qualitative QA

**Dependencies**: FR-PRD.13

### FR-PRD.15: Completion and Presentation

**Description**: Generate completion summary and present results to user.

**Acceptance Criteria**:
- [ ] Produces `completion-summary.md` with PRD path, line count, section count, pipeline statistics, quality verdicts
- [ ] Updates task file frontmatter: status -> Done, completion_date -> today
- [ ] Presents resume command if pipeline was halted
- [ ] Reports: total duration, agents spawned, fix cycles used, final QA verdicts

**Dependencies**: FR-PRD.14

## 4. Architecture

### 4.1 New Files

| File | Purpose | Dependencies |
|------|---------|-------------|
| `src/superclaude/cli/prd/__init__.py` | Package exports | `commands` |
| `src/superclaude/cli/prd/models.py` | `PrdConfig`, `PrdStepStatus` (12 states), `PrdStepResult`, `PrdPipelineResult`, `PrdMonitorState`, `ExistingWorkState` | `pipeline.models` |
| `src/superclaude/cli/prd/gates.py` | Gate criteria constants + 10 semantic check functions. Internally organized as two layers: reusable gate checks (`_check_verdict_field`, `_check_no_placeholders`) and PRD-specific checks (`_check_task_phases_present`, `_check_b2_self_contained`, `_check_parallel_instructions`). All semantic checks wrapped in try/except at the call site -- exceptions return `(False, "check '{name}' crashed: {error}")` rather than propagating [F-001, F-005 INCORPORATED] | `pipeline.models` |
| `src/superclaude/cli/prd/prompts.py` | 19 prompt builder functions for all Claude-assisted steps. The `_read_file()` helper truncates at 50KB and appends `[TRUNCATED -- file exceeds 50KB inline limit. Full file available at {path}]` so the subprocess knows the content was truncated and can read the full file via `--file` arg if needed [GAP-010 INCORPORATED] | `models` |
| `src/superclaude/cli/prd/config.py` | CLI arg resolution, `PrdConfig` construction, file discovery | `models` |
| `src/superclaude/cli/prd/inventory.py` | `check_existing_work()`, `discover_research_files()`, `discover_synth_files()`, `create_task_dirs()`. Note: `load_synthesis_mapping()` moved to `filtering.py` [F-002] | `models` |
| `src/superclaude/cli/prd/filtering.py` | `partition_files()`, `compile_gaps()`, `merge_qa_partition_reports()`, `_filter_research_for_sections()`, `load_synthesis_mapping()`. Synthesis mapping and filtering colocate here so the synthesis step builder has a single dependency for its data flow [F-002 INCORPORATED] | `models` |
| `src/superclaude/cli/prd/executor.py` | Main execution loop, parallel dispatch, fix cycles, status classification | `models`, `gates`, `prompts`, `inventory`, `filtering`, `process`, `monitor`, `tui` |
| `src/superclaude/cli/prd/process.py` | `PrdClaudeProcess` extending `ClaudeProcess` with PRD-specific prompt building. Constructs `--file` arguments per step's `allowed_refs` from the Phase Loading Contract (Section 5.3): each subprocess receives only the refs files permitted for its phase. Files >50KB are passed as `--file` args; files <50KB are inlined in the prompt [GAP-003 INCORPORATED] | `pipeline.process`, `models` |
| `src/superclaude/cli/prd/monitor.py` | NDJSON output parser with PRD-specific signals (research completion, QA verdicts, fix cycles). NOTE: monitor.py depends only on models.py; executor.py consumes monitor state but monitor does not import executor types -- this prevents circular dependency [GAP-002 INCORPORATED] | `models` |
| `src/superclaude/cli/prd/tui.py` | Rich live dashboard with step progress, QA verdicts, fix cycle state | `models`, `monitor` |
| `src/superclaude/cli/prd/logging_.py` | Dual JSONL + Markdown execution logging | `models` |
| `src/superclaude/cli/prd/diagnostics.py` | `DiagnosticCollector`, `FailureClassifier`, resume output generation | `models` |
| `src/superclaude/cli/prd/commands.py` | Click CLI group: `prd run`, `prd resume` | `config`, `executor` |

### 4.2 Modified Files

| File | Change | Rationale |
|------|--------|----------|
| `src/superclaude/cli/main.py` | Add `from superclaude.cli.prd.commands import prd_group; app.add_command(prd_group)` | Register PRD subcommand with CLI entry point |

### 4.3 Removed Files

None. The PRD skill files are NOT modified or removed -- they remain as the inference-based workflow. The CLI pipeline is an alternative execution path.

### 4.4 Module Dependency Graph

```
pipeline.models ----+
                    |
                    v
             prd/models.py
               /   |   \
              /    |    \
             v     v     v
     gates.py  inventory.py  config.py
               |         |
               v         v
          filtering.py   prompts.py
                \       /
                 \     /
                  v   v
              monitor.py  process.py  logging_.py  diagnostics.py
                   \         |           /          /
                    \        |          /          /
                     v       v         v          v
                         tui.py
                            |
                            v
                       executor.py
                            |
                            v
                       commands.py
                            |
                            v
                      __init__.py
```

### 4.5 Data Models

```python
# Core domain types (from portify-spec.md Section 2)

@dataclass
class PrdConfig(PipelineConfig):
    """Configuration for the PRD pipeline."""
    user_message: str = ""
    product_name: str = ""
    product_slug: str = ""
    prd_scope: str = "feature"           # "product" or "feature"
    scenario: str = "B"                  # "A" (explicit) or "B" (vague)
    where: list[str] = field(default_factory=list)
    why: str = ""
    output_path: Path = field(default_factory=lambda: Path("."))
    tier: str = "standard"               # "lightweight", "standard", "heavyweight"
    task_dir: Path = field(default_factory=lambda: Path("."))
    template_path: Path = field(default_factory=lambda: Path("docs/docs-product/templates/prd_template.md"))
    skill_refs_dir: Path = field(default_factory=lambda: Path("src/superclaude/skills/prd/refs"))
    max_turns: int = 300
    stall_timeout: int = 120
    stall_action: str = "warn"
    max_research_fix_cycles: int = 3
    max_synthesis_fix_cycles: int = 2
    research_partition_threshold: int = 6
    synthesis_partition_threshold: int = 4
    resume_from: str | None = None


class PrdStepStatus(Enum):
    """Lifecycle status for PRD pipeline steps."""
    PENDING = "pending"
    RUNNING = "running"
    PASS = "pass"
    PASS_NO_SIGNAL = "pass_no_signal"
    PASS_NO_REPORT = "pass_no_report"
    INCOMPLETE = "incomplete"
    HALT = "halt"
    TIMEOUT = "timeout"
    ERROR = "error"
    SKIPPED = "skipped"
    QA_FAIL = "qa_fail"
    QA_FAIL_EXHAUSTED = "qa_fail_exhausted"
    VALIDATION_FAIL = "validation_fail"


@dataclass
class PrdStepResult(StepResult):
    """Outcome of executing a single PRD pipeline step."""
    exit_code: int = 0
    output_bytes: int = 0
    error_bytes: int = 0
    artifacts_produced: list[str] = field(default_factory=list)
    agent_type: str = ""
    fix_cycle: int = 0
    qa_verdict: str | None = None


@dataclass
class PrdPipelineResult:
    """Aggregate result for the entire PRD pipeline."""
    config: PrdConfig
    step_results: list[PrdStepResult] = field(default_factory=list)
    outcome: str = "success"
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    finished_at: datetime | None = None
    halt_step: str | None = None
    halt_reason: str | None = None
    research_agent_count: int = 0
    web_agent_count: int = 0
    synthesis_agent_count: int = 0
    research_fix_cycles: int = 0
    synthesis_fix_cycles: int = 0
    final_prd_lines: int = 0
    final_prd_path: str = ""


@dataclass
class PrdMonitorState:
    """Real-time state extracted by the sidecar monitor thread."""
    output_bytes: int = 0
    last_event_time: float = field(default_factory=time.monotonic)
    events_received: int = 0
    last_step_id: str = ""
    current_artifact: str = ""
    research_files_completed: int = 0
    synth_files_completed: int = 0
    qa_verdict: str | None = None
    current_agent_type: str = ""
    fix_cycle_count: int = 0
```

### 4.6 Implementation Order

```
1.  models.py          -- zero internal deps, defines all domain types
2.  gates.py           -- depends on pipeline.models only
3.  inventory.py       -- depends on models (file discovery utilities)
4.  filtering.py       -- depends on inventory (partitioning, gap compilation)
5.  prompts.py         -- depends on models (prompt builders read config + files)
6.  config.py          -- depends on models, inventory (CLI arg -> PrdConfig)
7.  monitor.py         -- depends on models (NDJSON signal parsing)
8.  process.py         -- depends on pipeline.process, models (ClaudeProcess extension)
9.  logging_.py        -- depends on models (JSONL + Markdown logging)
10. diagnostics.py     -- depends on models (failure classification, resume output)
11. tui.py             -- depends on models, monitor (Rich live dashboard)
12. executor.py        -- depends on all above (main execution loop)
13. commands.py        -- depends on config, executor (Click CLI group)
14. __init__.py        -- depends on commands (package exports)

Parallelization: steps 3-6 are independent of 7-10 and could be implemented concurrently.
```

## 5. Interface Contracts

### 5.1 CLI Surface

```
superclaude prd run [REQUEST] [OPTIONS]
superclaude prd resume STEP_ID [OPTIONS]
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `REQUEST` | str (positional) | None | Natural-language product request |
| `--product, -p` | str | None | Product name or scope |
| `--where, -w` | str (multiple) | [] | Source directories to focus on |
| `--output, -o` | path | . | Output path for final PRD |
| `--tier` | choice | standard | `lightweight`, `standard`, `heavyweight` |
| `--max-turns` | int | 300 | Turn budget for all subprocesses |
| `--model` | str | None | Claude model to use |
| `--dry-run` | flag | false | Validate config without executing |
| `--debug` | flag | false | Enable debug logging |

### 5.2 Gate Criteria

| Step | Gate Tier | Frontmatter | Min Lines | Semantic Checks |
|------|-----------|-------------|-----------|----------------|
| 1. Check Existing | EXEMPT | -- | -- | -- |
| 2. Parse Request | STRICT | -- | -- | `_check_parsed_request_fields`: GOAL, PRODUCT_SLUG, PRD_SCOPE, SCENARIO present and non-empty |
| 3. Scope Discovery | STANDARD | -- | 50 | -- |
| 4. Research Notes | STRICT | Date, Scenario, Tier | 100 | `_check_research_notes_sections`: 7 required sections; `_check_suggested_phases_detail`: per-agent detail |
| 5. Sufficiency Review | STRICT | -- | -- | `_check_verdict_field`: verdict = PASS or FAIL |
| 6. Template Triage | EXEMPT | -- | -- | -- |
| 7. Build Task File | STRICT | id, title, status, complexity, created_date | tier-dependent (200/400/600) | `_check_task_phases_present`; `_check_b2_self_contained`; `_check_parallel_instructions` |
| 8. Verify Task File | STRICT | -- | -- | `_check_verdict_field` |
| 9. Preparation | LIGHT | -- | -- | -- |
| 10. Investigation (per file) | STANDARD | -- | 50 | -- |
| 11. Research QA | STRICT | -- | 20 | `_check_qa_verdict` |
| 12. Web Research (per file) | STANDARD | -- | 30 | -- |
| 13a. Synthesis (per file) | STANDARD | -- | 80 | -- |
| 13b. Synthesis QA | STRICT | -- | 20 | `_check_qa_verdict` |
| 14a. Assembly | STRICT | id, title, status, created_date, tags | tier-dependent (400-800/800-1500/1500-2500) | `_check_prd_template_sections`; `_check_no_placeholders` |
| 14b. Structural QA | STRICT | -- | 20 | `_check_qa_verdict` |
| 14c. Qualitative QA | STRICT | -- | 20 | `_check_qa_verdict` |
| 15. Present & Complete | LIGHT | -- | -- | -- |

### 5.3 Phase Contracts

```yaml
# Phase Loading Contract (subprocess isolation)
stage_a_orchestrator:        # Steps 1-6, 9
  allowed_refs: []
  subprocess_files: [parsed-request.json, scope-discovery-raw.md, research-notes.md]

stage_a_builder:             # Step 7
  allowed_refs:
    - refs/build-request-template.md
    - refs/agent-prompts.md
    - refs/synthesis-mapping.md
    - refs/validation-checklists.md
    - refs/operational-guidance.md
  subprocess_files: [research-notes.md, sufficiency-review.json]

stage_b_research:            # Steps 10, 12
  allowed_refs: []           # Prompts embedded in Step objects
  subprocess_files: [per-agent file assignments from research-notes.md]

stage_b_qa:                  # Steps 11, 13b
  allowed_refs: []           # QA checklists embedded in prompts
  subprocess_files: [research files, synth files, analyst reports]

stage_b_assembly:            # Step 14
  allowed_refs: []           # Assembly rules embedded in prompt
  subprocess_files: [all synth files, PRD template]
```

## 6. Non-Functional Requirements

| ID | Requirement | Target | Measurement |
|----|-------------|--------|-------------|
| NFR-PRD.1 | Synchronous execution model | No async/await anywhere in the PRD module | Code review: zero `async def` or `await` in `src/superclaude/cli/prd/` |
| NFR-PRD.2 | Gate function signatures | All semantic checks return `bool \| str` (True for pass, error string for fail) | Type checking: all `_check_*` functions match `Callable[[str], bool \| str]` |
| NFR-PRD.3 | Runner-authored truth | Reports derive from observed data (file existence, line counts, exit codes), not Claude self-reporting. Sentinel detection (`EXIT_RECOMMENDATION`, `verdict`) uses `^` anchored regex with `re.MULTILINE` and skips matches inside fenced code blocks to prevent sentinel collision when documenting the PRD skill itself [F-007 INCORPORATED] | Code review: executor reads artifacts directly, not subprocess stdout claims; unit test: sentinel inside code block is not matched |
| NFR-PRD.4 | Budget tracking | TurnLedger guards every subprocess launch including fix cycle gap-fillers and re-QA runs; pipeline halts before budget exhaustion. Fix cycle turns are deducted from the main TurnLedger budget (no separate reserve). If budget exhausts mid-fix-cycle, pipeline halts with `QA_FAIL_EXHAUSTED` and includes partial fix cycle results in resume state [F-006 INCORPORATED] | Integration test: pipeline halts with resume command when budget < minimum_allocation; integration test: budget exhaustion mid-fix-cycle produces correct resume state |
| NFR-PRD.5 | Stall detection | Detect subprocess stalls within `stall_timeout` (default 120s) | Monitor thread reports stall_seconds > threshold; TUI shows STALLED status |
| NFR-PRD.6 | Resume granularity | Resume from any step ID with `--resume`. For parallel groups: resume re-runs only the failed agents within the group, not the entire group. The executor tracks per-agent completion state and skips agents whose output files exist and passed gate validation. [GAP-007 INCORPORATED] | Integration test: `prd resume investigate-03` skips steps 1-9 and earlier investigation agents; `prd resume investigate-05` re-runs only agent 05 if agents 01-04 and 06 already completed |
| NFR-PRD.7 | Parallel execution cap | ThreadPoolExecutor max_workers capped at 10. Zero-step guard: if step list is empty, `_execute_parallel_group` returns empty results immediately without creating a ThreadPoolExecutor [F-004/boundary] | Code review: `min(len(steps), 10)` in `_execute_parallel_group`; `min(len(steps), 10)` is never 0 because empty groups are filtered before dispatch |
| NFR-PRD.13 | Subprocess timeout enforcement | `PrdClaudeProcess` uses `subprocess.Popen` with an external watchdog timer. On timeout: (1) send SIGTERM to subprocess, (2) wait 5s, (3) send SIGKILL if still alive. `_execute_claude_step` handles `TimeoutError` from the watchdog and returns `PrdStepStatus.TIMEOUT`. The `timeout_seconds` field on Step objects is enforced programmatically, not via `Future.result(timeout=)` [F-004 INCORPORATED] | Integration test: subprocess exceeding timeout is killed and returns TIMEOUT status |
| NFR-PRD.8 | Incremental file writing | All Claude-assisted steps produce output incrementally (header first, then sections). Prompt builders enforce a 100KB maximum prompt size: inline content is capped at 50KB per file, and files exceeding this are passed as `--file` args instead [GAP-008 INCORPORATED] | Prompt contracts include Incremental File Writing Protocol; monitor detects growth; unit test validates prompt size < 100KB for synthetic worst-case inputs |
| NFR-PRD.9 | Signal-aware shutdown | SIGINT/SIGTERM triggers graceful shutdown with state preservation | Integration test: send SIGINT mid-run, verify resume state written |
| NFR-PRD.12 | Subprocess launch resilience | `PrdClaudeProcess.launch()` retries up to 2 times with exponential backoff (5s, 15s) on transient failures (rate limiting, temporary API unavailability). Non-transient failures (invalid args, permission denied) fail immediately without retry [GAP-011 INCORPORATED] | Unit test: mock transient failure, verify retry count and backoff delays |
| NFR-PRD.10 | Execution logging | Dual JSONL (machine) + Markdown (human) logs for every step | Log files exist after run with correct entry counts |
| NFR-PRD.11 | Context injection | Downstream Claude-assisted steps receive compressed summaries of upstream results via `PrdStepResult.to_context_summary()`. The executor appends a `## Prior Step Results` section to each prompt containing verbose summaries of directly-dependent steps and terse summaries of transitively-dependent steps [GAP-004 INCORPORATED] | Code review: every prompt builder that accepts `inputs` also receives context summaries |

## 7. Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Dynamic step generation produces too many agents for budget | Medium | High | TurnLedger guards every launch; tier caps agent counts; budget warning at 80% consumption |
| QA fix cycles exhaust budget without achieving PASS | Medium | Medium | Hard cap on fix cycles (3 research, 2 synthesis); exhaustion produces resume command with suggested budget |
| Research notes quality varies, producing poor downstream synthesis | Medium | High | STRICT gate on research notes with 2 semantic checks; sufficiency review with gap-fill rounds |
| Task file builder produces malformed output | Medium | High | STRICT gate with 6 semantic checks; verification step with re-build on failure |
| Parallel agent execution causes resource contention | Low | Medium | ThreadPoolExecutor cap at 10 workers; per-agent timeout; stall detection |
| Assembly cross-section consistency check misses contradictions | Low | Medium | Sequential assembly (single agent); structural QA + qualitative QA double-check |
| Subprocess isolation fails (refs leakage between phases) | Low | High | Phase loading contract enforced programmatically via `--file` arg scoping |
| Context window exhaustion in complex products (heavyweight tier) | Medium | Medium | Incremental File Writing Protocol; prompt size limits (50KB inline cap); partition-based QA |
| PRD template changes break gate semantic checks | Low | Medium | Template section patterns are regex-based with fallback; gate functions are isolated for easy update |

## 8. Test Plan

### 8.1 Unit Tests

| Test | File | Validates |
|------|------|-----------|
| `test_check_existing_work_no_existing` | `tests/cli/prd/test_inventory.py` | Returns `NO_EXISTING` when no task dirs exist |
| `test_check_existing_work_resume_stage_b` | `tests/cli/prd/test_inventory.py` | Detects existing task file with unchecked items |
| `test_select_template` | `tests/cli/prd/test_inventory.py` | Returns 2 for creation, 1 for update |
| `test_discover_research_files` | `tests/cli/prd/test_inventory.py` | Finds completed research files, skips incomplete |
| `test_discover_synth_files` | `tests/cli/prd/test_inventory.py` | Finds synth files matching `synth-*.md` pattern |
| `test_partition_files_below_threshold` | `tests/cli/prd/test_filtering.py` | Returns single partition when count <= threshold |
| `test_partition_files_above_threshold` | `tests/cli/prd/test_filtering.py` | Splits into correct partition count |
| `test_merge_qa_partition_reports` | `tests/cli/prd/test_filtering.py` | Merges reports, correctly determines overall verdict |
| `test_compile_gaps` | `tests/cli/prd/test_filtering.py` | Extracts and deduplicates gaps from research files |
| `test_load_synthesis_mapping` | `tests/cli/prd/test_inventory.py` | Returns 9 entries with correct section assignments |
| `test_check_parsed_request_fields_valid` | `tests/cli/prd/test_gates.py` | Returns True for valid JSON with all fields |
| `test_check_parsed_request_fields_missing` | `tests/cli/prd/test_gates.py` | Returns error string listing missing fields |
| `test_check_research_notes_sections` | `tests/cli/prd/test_gates.py` | Validates all 7 sections present |
| `test_check_verdict_field` | `tests/cli/prd/test_gates.py` | Detects PASS/FAIL in both JSON and markdown format |
| `test_check_b2_self_contained` | `tests/cli/prd/test_gates.py` | Catches "see above" violations in checklist items |
| `test_check_parallel_instructions` | `tests/cli/prd/test_gates.py` | Validates parallel keywords in phases 2-5 |
| `test_check_prd_template_sections` | `tests/cli/prd/test_gates.py` | Detects missing critical PRD sections |
| `test_check_no_placeholders` | `tests/cli/prd/test_gates.py` | Catches TODO, TBD, PLACEHOLDER text |
| `test_determine_status_pass` | `tests/cli/prd/test_executor.py` | EXIT_RECOMMENDATION: CONTINUE -> PASS |
| `test_determine_status_halt` | `tests/cli/prd/test_executor.py` | EXIT_RECOMMENDATION: HALT -> HALT |
| `test_determine_status_qa_fail` | `tests/cli/prd/test_executor.py` | verdict: FAIL -> QA_FAIL |
| `test_determine_status_timeout` | `tests/cli/prd/test_executor.py` | Exit code 124 -> TIMEOUT |
| `test_prd_config_derived_paths` | `tests/cli/prd/test_models.py` | research_dir, synthesis_dir, qa_dir resolve correctly |
| `test_prd_step_status_properties` | `tests/cli/prd/test_models.py` | is_terminal, is_success, is_failure, needs_fix_cycle |
| `test_prd_pipeline_result_resume_command` | `tests/cli/prd/test_models.py` | Generates correct resume command on halt |
| `test_build_investigation_prompt_includes_staleness_protocol` | `tests/cli/prd/test_prompts.py` | Prompt contains Documentation Staleness Protocol markers [F-011 INCORPORATED] |
| `test_build_synthesis_prompt_includes_template_reference` | `tests/cli/prd/test_prompts.py` | Prompt contains template path reference [F-011 INCORPORATED] |
| `test_prompt_size_under_100kb` | `tests/cli/prd/test_prompts.py` | All prompt builders produce output < 100KB for synthetic worst-case inputs [F-011 INCORPORATED] |
| `test_read_file_truncation_at_50kb` | `tests/cli/prd/test_prompts.py` | `_read_file()` truncates at 50KB with marker text [F-011 INCORPORATED] |
| `test_sentinel_not_matched_in_code_block` | `tests/cli/prd/test_executor.py` | EXIT_RECOMMENDATION inside code block is ignored [F-007 INCORPORATED] |

### 8.2 Integration Tests

| Test | Validates |
|------|-----------|
| `test_prd_pipeline_dry_run` | Config construction and validation without execution |
| `test_prd_pipeline_check_existing_integration` | Full existing work detection against real directory structure |
| `test_prd_pipeline_budget_exhaustion` | Pipeline halts when TurnLedger reports insufficient budget |
| `test_prd_pipeline_signal_shutdown` | SIGINT triggers graceful shutdown with resume state |
| `test_prd_pipeline_gate_enforcement` | STRICT gate failures halt pipeline with diagnostic output |
| `test_prd_pipeline_fix_cycle_flow` | QA FAIL -> gap-fill agents -> re-QA -> PASS flow |
| `test_prd_pipeline_parallel_execution` | ThreadPoolExecutor correctly runs N agents concurrently |
| `test_build_investigation_steps_standard_tier` | Dynamic step generation produces correct count and output paths for standard tier [F-012 INCORPORATED] |
| `test_build_investigation_steps_heavyweight_tier` | Dynamic step generation produces correct count for heavyweight tier [F-012 INCORPORATED] |

### 8.3 Manual / E2E Tests

| Scenario | Steps | Expected Outcome |
|----------|-------|------------------|
| Full PRD creation (standard tier) | `superclaude prd run "Create PRD for SuperClaude CLI"` | Complete PRD at output path, 800-1500 lines, all QA passed |
| Lightweight PRD | `superclaude prd run "PRD for install command" --tier lightweight` | Shorter PRD (400-800 lines), 2-3 research agents, 0-1 web agents |
| Resume from halted step | `superclaude prd resume investigate-03 --max-turns 150` | Skips completed steps, resumes from specified agent |
| Existing work detection | Run twice with same product | Second run detects existing work, offers resume |
| Budget exhaustion | `superclaude prd run "Full platform PRD" --max-turns 50` | Halts mid-run with resume command and suggested budget |

## 9. Migration & Rollout

- **Breaking changes**: None. The CLI pipeline is a new execution path; the inference-based skill remains unchanged.
- **Backwards compatibility**: Full. Users can continue using `/sc:prd` (inference) or switch to `superclaude prd run` (CLI pipeline). Both produce the same output format (PRD from the same template).
- **Rollback plan**: Remove the `prd` subcommand import from `main.py`. Delete `src/superclaude/cli/prd/`. No other changes needed.

## 10. Downstream Inputs

### For sc:roadmap

**Themes**:
- CLI Pipeline Extension: PRD module extends the `superclaude` CLI with a new subcommand family
- Quality Gate Framework: 10 semantic check functions establish patterns for future portified pipelines
- Dynamic Step Generation: `build_*_steps()` pattern reusable for any pipeline with runtime-determined agent counts

**Milestones**:
1. Core models + gates (estimated: models.py, gates.py, inventory.py, filtering.py)
2. Prompts + config (estimated: prompts.py, config.py)
3. Execution engine (estimated: executor.py, process.py, monitor.py, tui.py, logging_.py, diagnostics.py)
4. CLI integration (estimated: commands.py, __init__.py, main.py modification)
5. Test suite (estimated: test_models.py, test_gates.py, test_inventory.py, test_filtering.py, test_executor.py)

### For sc:tasklist

**Task breakdown guidance**:
- Group by implementation order (Section 4.6): models -> gates -> inventory -> filtering -> prompts -> config -> monitor -> process -> logging -> diagnostics -> tui -> executor -> commands
- Each file is a natural task boundary with clear inputs/outputs
- Gates and inventory are independently testable and should be completed first
- Executor is the integration point -- implement last after all dependencies are stable
- Test tasks should parallel implementation tasks (write tests as you implement each module)

## 11. Open Items

| Item | Question | Impact | Resolution Target |
|------|----------|--------|-------------------|
| OI-001 | Should the CLI pipeline support `--scope product` vs `--scope feature` as explicit flags, or always infer from request parsing? | Affects config.py and FR-PRD.2 | Pre-implementation |
| OI-002 | What is the maximum acceptable wall-clock time for a full heavyweight PRD run? | Affects timeout budgets and stall thresholds | Pre-implementation |
| OI-003 | Should partitioned QA reports be preserved as individual files or only as merged reports? | Affects filtering.py and diagnostic output | During implementation |
| OI-004 | How should the TUI display parallel agent progress -- individual rows per agent or aggregate progress bar? | Affects tui.py design | During implementation |
| OI-005 | Should `_check_research_notes_sections` use case-insensitive matching for section headers to handle formatting variations? [GAP-006 OPEN] | Affects gates.py robustness | During implementation |
| OI-006 | Should concurrent QA agents writing to the same `qa/` directory use file-level atomic writes or unique filenames to prevent race conditions? [GAP-009 OPEN] | Affects filtering.py and inventory.py | During implementation |
| OI-007 | What deduplication strategy should `compile_gaps()` use for identical gaps reported across multiple research files? [GAP-012 OPEN] | Affects filtering.py | During implementation |
| OI-008 | `PrdPipelineResult.outcome` is `str` but `PrdStepStatus` is an enum -- should `outcome` also be a typed enum (`PipelineOutcome`) for consistency? [F-003 OPEN] | Affects models.py | During implementation |
| OI-009 | `_check_no_placeholders` may false-positive on content-appropriate uses of "TODO" (e.g., "TODO items are tracked in..."). Should detection be restricted to bracket/brace patterns like `[TODO]`, `[TBD]`, `{{PLACEHOLDER}}`? [F-009 OPEN] | Affects gates.py | During implementation |
| OI-010 | If sufficiency review returns `{"verdict": "FAIL", "gaps": []}`, the fix cycle has nothing to fix. Should empty-gaps FAIL be treated as PASS-with-warning? [F-010 OPEN] | Affects executor.py fix cycle logic | During implementation |
| OI-011 | `_check_verdict_field` should test both JSON and markdown formats explicitly in unit tests. [F-013 OPEN] | Affects test_gates.py | During implementation |

## 12. Brainstorm Gap Analysis

### Architect Persona Findings

| Gap ID | Description | Severity | Affected Section | Persona |
|--------|-------------|----------|------------------|---------|
| GAP-001 | No error recovery strategy defined for partial parallel group failures (e.g., 3 of 6 research agents succeed, 3 fail) | high | 3 (FR-PRD.10, FR-PRD.13), 5.2 (Gate Criteria) | architect |
| GAP-002 | Module dependency graph shows tui.py depending on monitor.py, but executor.py also directly uses monitor -- potential circular dependency if monitor imports executor types | medium | 4.4 (Module Dependency Graph) | architect |
| GAP-003 | No specification for how `PrdClaudeProcess` constructs subprocess `--file` arguments to enforce phase loading isolation | medium | 4.1 (process.py), 5.3 (Phase Contracts) | architect |
| GAP-004 | Context injection pattern undefined: how do later steps receive compressed summaries of earlier step results? | medium | 2.2 (Data Flow), 6 (NFR-PRD.3) | architect |

### Analyzer Persona Findings

| Gap ID | Description | Severity | Affected Section | Persona |
|--------|-------------|----------|------------------|---------|
| GAP-005 | FR-PRD.11 acceptance criteria for "partition reports merged" does not specify what happens when partitions produce conflicting verdicts (one PASS, one FAIL) | medium | 3 (FR-PRD.11) | analyzer |
| GAP-006 | `_check_research_notes_sections` uses simple string matching for section headers but does not account for slight formatting variations (e.g., `## EXISTING_FILES` vs `## Existing Files` vs `### EXISTING_FILES`) | low | 5.2 (Gate Criteria) | analyzer |
| GAP-007 | Resume semantics for mid-parallel-group failures are undefined -- if investigation agent 3 of 6 fails, does resume re-run agent 3 only or the entire group? | high | 3 (FR-PRD.10), 6 (NFR-PRD.6) | analyzer |
| GAP-008 | No acceptance criterion for verifying that prompt builders produce prompts within a maximum size limit (to prevent context window overflow in subprocesses) | medium | 3 (FR-PRD.7), 6 (NFR-PRD.8) | analyzer |

### Backend Persona Findings

| Gap ID | Description | Severity | Affected Section | Persona |
|--------|-------------|----------|------------------|---------|
| GAP-009 | No file locking strategy for concurrent agents writing to the same QA directory (e.g., partitioned QA agents all writing to `qa/`) | low | 4.1 (inventory.py, filtering.py) | backend |
| GAP-010 | `_read_file()` helper truncates at 50KB but no spec for how the prompt builder signals truncation to the Claude subprocess or adjusts prompt accordingly | medium | portify-prompts.md (helpers) | backend |
| GAP-011 | Missing retry/backoff specification for `ClaudeProcess` launch failures (e.g., rate limiting, temporary API unavailability) | medium | 4.1 (process.py), 6 (NFRs) | backend |
| GAP-012 | `compile_gaps()` deduplication logic is unspecified -- how are duplicate gaps across research files identified and merged? | low | 4 (filtering.py) | backend |

**Gap Analysis Summary**: 12 total gaps identified. Severity distribution: 2 high, 7 medium, 3 low.

**Incorporation Status**: 9 incorporated into spec body, 3 routed to Open Items (Section 11).

| Gap ID | Status | Resolution |
|--------|--------|------------|
| GAP-001 | [INCORPORATED] | Added partial group failure strategy to FR-PRD.10 acceptance criteria |
| GAP-002 | [INCORPORATED] | Clarified monitor.py dependency direction in Architecture 4.1 |
| GAP-003 | [INCORPORATED] | Added `--file` arg construction spec to process.py description |
| GAP-004 | [INCORPORATED] | Added NFR-PRD.11 (Context Injection) to NFR table |
| GAP-005 | [INCORPORATED] | Added pessimistic merge strategy to FR-PRD.11 acceptance criteria |
| GAP-006 | [OPEN] | Routed to OI-005 (case-insensitive section header matching) |
| GAP-007 | [INCORPORATED] | Added per-agent resume semantics to NFR-PRD.6 |
| GAP-008 | [INCORPORATED] | Added 100KB prompt size cap to NFR-PRD.8 |
| GAP-009 | [OPEN] | Routed to OI-006 (concurrent QA directory writes) |
| GAP-010 | [INCORPORATED] | Added truncation signaling to prompts.py description |
| GAP-011 | [INCORPORATED] | Added NFR-PRD.12 (Subprocess Launch Resilience) to NFR table |
| GAP-012 | [OPEN] | Routed to OI-007 (gap deduplication strategy) |

---

## Appendix A: Glossary

| Term | Definition |
|------|------------|
| MDTM | Markdown-Driven Task Management -- task file format using checklist items as execution steps |
| B2 pattern | Self-contained checklist items that embed all required context, not referencing other sections |
| Fix cycle | Sequence of: QA gate FAIL -> spawn targeted gap-filling agents -> re-run QA |
| Phase loading contract | The skill's isolation model specifying which refs files are visible at which phase |
| Runner-authored truth | Reports derive from observed data (file existence, exit codes), not subprocess self-reporting |
| TurnLedger | Budget tracking dataclass that guards subprocess launches against budget exhaustion |
| Fan-out | Parallel pattern where N identical agents run concurrently on different inputs |
| Dual-stream | Parallel pattern where 2 agents with different roles (analyst + QA) run concurrently |
| Partitioned fan-out | Fan-out variant where inputs are split into subsets, each with its own agent pair |
| Stall detection | Monitor thread checking for output growth; STALLED when no events for > stall_timeout |

## Appendix B: Reference Documents

| Document | Relevance |
|----------|-----------|
| `src/superclaude/skills/prd/SKILL.md` | Source workflow being portified |
| `src/superclaude/skills/prd/refs/agent-prompts.md` | Agent prompt templates adapted into prompt builders |
| `src/superclaude/skills/prd/refs/synthesis-mapping.md` | Synthesis file to PRD section mapping table |
| `src/superclaude/skills/prd/refs/validation-checklists.md` | QA checklists encoded into gate semantic checks |
| `src/superclaude/skills/prd/refs/build-request-template.md` | BUILD_REQUEST template for task file construction |
| `src/superclaude/skills/prd/refs/operational-guidance.md` | Critical rules encoded into gate and prompt logic |
| `src/superclaude/cli/pipeline/models.py` | Base pipeline types extended by PRD models |
| `src/superclaude/cli/pipeline/gates.py` | `gate_passed()` function used for gate evaluation |
| `src/superclaude/cli/sprint/models.py` | `TurnLedger` reused for budget tracking |
| `src/superclaude/cli/sprint/executor.py` | Sprint executor pattern replicated for PRD pipeline |
| `.dev/portify-workdir/prd/portify-analysis.md` | Phase 1 workflow decomposition |
| `.dev/portify-workdir/prd/portify-spec.md` | Phase 2 pipeline specification |
| `.dev/portify-workdir/prd/portify-prompts.md` | Phase 2 prompt builder companion |
