# Research Prompt: Roadmap & Tasklist Generation Architecture Overhaul

## GOAL

Map the complete end-to-end pipeline for roadmap generation and tasklist generation — every step, every file, every prompt, every subprocess, every gate — and produce an implementation plan to replace the current extraction-based approach with a template-driven, incremental-write architecture that uses input documents (TDD, PRD, spec) directly and granularly.

## WHY

The current pipeline has three structural failures that compound:

1. **Extraction destroys granularity.** The extraction step summarizes dense TDD content (876 lines, 200+ work items) into a compressed format (~50 entities). The generate step then receives BOTH the extraction AND the raw TDD, but anchors on the extraction's compressed output. The extraction is counterproductive for structured inputs — it exists to normalize unstructured specs, but TDDs and PRDs are already structured.

2. **One-shot output architecture.** Every pipeline step runs as `claude --print --output-format text` — the LLM builds its entire output in memory and writes it as a single response to stdout. For large outputs (200+ roadmap task rows, 14-section extractions with per-entity IDs), this hits max output token limits and truncates. The pipeline has no mechanism for incremental writing, continuation, or recovery from truncation.

3. **No output templates.** The roadmap and tasklist structures are described inline in prompt strings. There is no template file that defines what the output should look like. Without a template, the LLM decides its own format — producing tables for spec input and prose narratives for TDD input, leading to wildly different task counts from the same pipeline.

These three issues caused the TDD+PRD pipeline to produce 44 tasks from 1,282 lines of input while the spec pipeline produced 87 tasks from 312 lines. After prompt fixes to the generate step (telling it to use TDD as primary and create per-entity rows), we got 148 roadmap table rows and 5 phases — but this is fragile because the one-shot architecture will break as documents get larger.

## WHAT TO INVESTIGATE

### Investigation Area 1: Complete Pipeline Step Map

Trace the FULL pipeline from CLI invocation to final output file. For EACH step:

**Files to read:**
- `src/superclaude/cli/roadmap/commands.py` — CLI entry point, argument parsing, input routing
- `src/superclaude/cli/roadmap/executor.py` — `_build_steps()` function that defines the step list, `roadmap_run_step()` that executes each step, `execute_roadmap()` orchestrator
- `src/superclaude/cli/roadmap/models.py` — `RoadmapConfig` dataclass
- `src/superclaude/cli/pipeline/executor.py` — `execute_pipeline()` generic executor
- `src/superclaude/cli/pipeline/process.py` — `ClaudeProcess` subprocess wrapper
- `src/superclaude/cli/pipeline/models.py` — `Step`, `StepResult`, `PipelineConfig` dataclasses
- `src/superclaude/cli/pipeline/gates.py` — gate definitions and `gate_passed()` function

For each of the 13 pipeline steps (extract, generate-A, generate-B, diff, debate, score, merge, anti-instinct, test-strategy, spec-fidelity, wiring-verification, deviation-analysis, remediate), document:
- What prompt function builds its instructions (`src/superclaude/cli/roadmap/prompts.py`)
- What input files it receives (via `Step.inputs`)
- What output file it writes
- What gate checks its output
- What timeout and retry limits it has
- Whether it's LLM-based or deterministic
- Whether it runs sequentially or in parallel with other steps

### Investigation Area 2: Input Routing and Auto-Detection

How does the pipeline determine what type of input it received and how to route it?

**Files to read:**
- `src/superclaude/cli/roadmap/executor.py` — `_route_input_files()` function
- `src/superclaude/cli/roadmap/commands.py` — how `input_files` positional args are processed
- Any auto-detection logic that classifies files as spec, TDD, or PRD

Document:
- How does `_route_input_files()` decide which file is spec, which is TDD, which is PRD?
- What happens when 1 file is provided vs 2 vs 3?
- How does `--input-type` override work?
- How does `input_type` propagate through the pipeline (which steps branch on it)?
- What changes when `input_type == "tdd"` vs `"spec"`?

### Investigation Area 3: Prompt Architecture

Read EVERY prompt-building function in `src/superclaude/cli/roadmap/prompts.py` and document:

- `build_extract_prompt()` — what it tells the LLM to produce, what format
- `build_extract_prompt_tdd()` — how it differs, what sections it adds
- `build_generate_prompt()` — what it tells the LLM to produce, how it references inputs, how TDD/PRD supplementary blocks change the instructions
- `build_merge_prompt()` — does it consolidate? does it reduce granularity?
- `build_diff_prompt()`, `build_debate_prompt()`, `build_score_prompt()` — do any of these affect task granularity?
- `build_test_strategy_prompt()`, `build_spec_fidelity_prompt()` — downstream consumers
- Any shared constants (`_INTEGRATION_ENUMERATION_BLOCK`, `_OUTPUT_FORMAT_BLOCK`, etc.)

For each prompt: what format does it request? Does it specify tables vs prose? Does it set minimum item counts? Does it reference a template?

### Investigation Area 4: ClaudeProcess and Output Mechanism

How does each step actually execute and capture output?

**Files to read:**
- `src/superclaude/cli/pipeline/process.py` — `ClaudeProcess` class, `build_command()`, `start()`, `wait()`
- How stdout is captured to the output file
- What `--output-format text` means for Claude CLI behavior
- What `--max-turns` actually controls — can the LLM continue across turns?
- What happens when output exceeds token limits — does it truncate silently?

Document:
- Is there any mechanism for the subprocess to write to disk incrementally?
- Could `--output-format stream-json` or tool-use mode enable incremental writing?
- What would need to change to let the subprocess use Write/Edit tools?
- What are the actual output token limits for each model (opus, haiku, sonnet)?

### Investigation Area 5: Gate Architecture

How do gates verify step output?

**Files to read:**
- `src/superclaude/cli/pipeline/gates.py` — all gate definitions
- `src/superclaude/cli/roadmap/executor.py` — gate constants (EXTRACT_GATE, EXTRACT_TDD_GATE, GENERATE_A_GATE, etc.)

Document:
- What does each gate check (frontmatter fields, section counts, semantic checks)?
- Which gates would need to change if the output format changes (e.g., from one-shot text to incrementally-written file)?
- What is the `GateMode.TRAILING` mechanism?
- What is the `GateMode.BLOCKING` mechanism?

### Investigation Area 6: Tasklist Generation Pipeline

Trace the tasklist generation from CLI to output.

**Files to read:**
- `src/superclaude/cli/tasklist/commands.py` — CLI entry point
- `src/superclaude/cli/tasklist/executor.py` — `execute_tasklist_validate()` and any generation functions
- `src/superclaude/cli/tasklist/prompts.py` — `build_tasklist_generate_prompt()`, `build_tasklist_fidelity_prompt()`
- `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` — the full generation algorithm (Sections 4.1-4.11)

Document:
- How does tasklist generation currently work? (CLI command? Skill invocation? Both?)
- What is the relationship between `superclaude tasklist validate` and `/sc:tasklist`?
- How does the skill's Section 4.1 parser determine R-items from the roadmap?
- What would a tasklist output template look like?
- How does the skill handle the one-shot problem (or does it)?

### Investigation Area 7: Template Design Requirements

Based on all findings, determine what templates are needed and what they should contain.

**Reference templates to study:**
- `src/superclaude/examples/tdd_template.md` — TDD template structure (1300+ lines, 28 sections)
- `src/superclaude/examples/release-spec-template.md` — Spec template
- `.claude/templates/workflow/02_mdtm_template_complex_task.md` — MDTM task template (PART 1 = building rules, PART 2 = output structure)

Document:
- What should a roadmap output template contain? (Section headers, table schemas, frontmatter fields, phase structure guidance)
- What should a tasklist output template contain? (Index structure, phase file structure, task format)
- How should the template interact with the prompt? (Template provides structure, prompt provides content instructions)
- Should the template be a file on disk that the subprocess reads, or embedded in the prompt?

## OUTPUT

A research report answering:

1. **Complete pipeline map** — every step, file, prompt, gate, input, output in a traceable table
2. **Input routing mechanics** — how files get classified and routed, with exact code paths
3. **Where granularity is lost** — for each step, does it preserve, expand, or compress the number of actionable items? Which steps are the bottlenecks?
4. **One-shot architecture assessment** — what are the actual output limits, what truncates, what would incremental writing require?
5. **Template specifications** — what a roadmap template and tasklist template should contain, modeled after the TDD/PRD/MDTM template patterns
6. **Implementation plan** — specific files to modify, in what order, to achieve:
   - Template-driven output (roadmap and tasklist both use templates)
   - Incremental writing (subprocess writes to disk section by section, not one-shot)
   - Direct input consumption (TDD/PRD content used directly at full granularity, no lossy extraction step)
   - Backward-compatible spec path (spec input continues working as before)
7. **Gate modifications** — which gates need updating for the new output format
8. **Risk assessment** — what could break, what needs regression testing

## CONTEXT FILES

| File | Why |
|------|-----|
| `src/superclaude/cli/roadmap/commands.py` | CLI entry, argument parsing, input routing |
| `src/superclaude/cli/roadmap/executor.py` | Pipeline orchestration, step definitions, run logic |
| `src/superclaude/cli/roadmap/models.py` | RoadmapConfig, AgentSpec |
| `src/superclaude/cli/roadmap/prompts.py` | ALL prompt-building functions |
| `src/superclaude/cli/pipeline/executor.py` | Generic pipeline executor |
| `src/superclaude/cli/pipeline/process.py` | ClaudeProcess subprocess wrapper |
| `src/superclaude/cli/pipeline/models.py` | Step, StepResult, PipelineConfig, GateMode |
| `src/superclaude/cli/pipeline/gates.py` | Gate definitions and checker |
| `src/superclaude/cli/tasklist/commands.py` | Tasklist CLI |
| `src/superclaude/cli/tasklist/executor.py` | Tasklist validation executor |
| `src/superclaude/cli/tasklist/prompts.py` | Tasklist prompt builders |
| `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` | Tasklist generation algorithm |
| `src/superclaude/examples/tdd_template.md` | TDD template (reference for output template design) |
| `src/superclaude/examples/release-spec-template.md` | Spec template (reference) |
| `.claude/templates/workflow/02_mdtm_template_complex_task.md` | MDTM template (reference for PART 1/PART 2 pattern) |
| `.dev/tasks/to-do/ISSUE-pipeline-one-shot-output.md` | Issue doc on one-shot architecture problem |
| `.dev/tasks/to-do/TASK-RESEARCH-20260403-tasklist-quality/RESEARCH-REPORT-tasklist-quality.md` | Prior research on task count regression |
| `.dev/tasks/to-do/TASK-RESEARCH-20260403-tasklist-quality/reviews/pipeline-trace-investigation.md` | Pipeline trace showing where granularity is lost |
| `.dev/tasks/to-do/TASK-RESEARCH-20260403-tasklist-quality/reviews/r-item-collapse-investigation.md` | R-item investigation showing 1:1 mapping |

## DEPTH

Deep — this spans the entire pipeline across 15+ files, two CLI subsystems (roadmap + tasklist), and requires architectural recommendations.
