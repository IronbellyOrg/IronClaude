# /sc:spawn v2 — Architecture & Component Design

> **Version**: 2.0 | **Date**: 2026-03-22
> **Status**: Design Complete — Ready for Implementation
> **Prior Art**: `archive/spec-v1.md` (incorporated and extended)

---

## 1. Naming & File Layout

Following the mandatory `-protocol` suffix convention (prevents re-entry deadlock):

| Component | Name | Path |
|-----------|------|------|
| Command | spawn | `src/superclaude/commands/spawn.md` |
| Skill directory | sc-spawn-protocol/ | `src/superclaude/skills/sc-spawn-protocol/` |
| Skill manifest | sc:spawn-protocol | `src/superclaude/skills/sc-spawn-protocol/SKILL.md` |
| Ref: decomposition | — | `src/superclaude/skills/sc-spawn-protocol/refs/decomposition-patterns.md` |
| Ref: dependency graph | — | `src/superclaude/skills/sc-spawn-protocol/refs/dependency-graph.md` |
| Ref: delegation | — | `src/superclaude/skills/sc-spawn-protocol/refs/delegation-matrix.md` |
| Agent: orchestrator | spawn-orchestrator | `src/superclaude/agents/spawn-orchestrator.md` |
| Agent: planner | spawn-planner | `src/superclaude/agents/spawn-planner.md` |

**Design decision**: Three ref files instead of prior spec's prompt-construction.md + delegation-matrix.md + decomposition-patterns.md. Prompt construction rules are merged into delegation-matrix.md (they're both Wave 3 concerns). dependency-graph.md replaces it as a Wave 2 ref covering DAG construction and pipeline parsing.

---

## 2. Component Specifications

### 2.1 Command: spawn.md (Thin Entry — ~80 lines)

```markdown
---
name: spawn
description: "Meta-system task orchestration with intelligent breakdown and active delegation"
category: special
complexity: high
allowed-tools: Read, Glob, Grep, Bash, TaskCreate, TaskUpdate, TaskList, TaskGet, Task, Write, Skill
mcp-servers: [sequential, serena]
personas: [architect, analyzer]
---

# /sc:spawn - Meta-System Task Orchestration

## Triggers
- Complex multi-domain operations requiring intelligent task breakdown
- Large-scale system operations spanning multiple technical areas
- Operations requiring parallel coordination and dependency management
- Meta-level orchestration beyond standard command capabilities

## Usage
```
/sc:spawn [complex-task] [--strategy sequential|parallel|adaptive|wave]
                         [--depth shallow|normal|deep]
                         [--no-delegate] [--dry-run] [--resume]
                         [--pipeline "<shorthand>" | --pipeline @path.yaml]
                         [--agents <spec>[,...]] [--prompt "<text>"]
                         [--pipeline-seq] [--pipeline-resume]
```

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--strategy` | `adaptive` | Coordination strategy for task execution |
| `--depth` | `normal` | Decomposition granularity (also interpolated into DAG phases) |
| `--no-delegate` | `false` | Plan-only mode: produce hierarchy without spawning agents |
| `--dry-run` | `false` | Preview decomposition without creating tasks |
| `--resume` | `false` | Resume from Serena checkpoint |
| `--pipeline` | — | Inline shorthand or `@path.yaml` for multi-phase DAG |
| `--agents` | — | Agent specs in `model[:persona[:"instruction"]]` format (Pipeline Mode) |
| `--prompt` | — | Prompt text passed to DAG phases (also accepted as trailing quoted string) |
| `--pipeline-seq` | `false` | Force sequential phase execution (default is parallel) |
| `--pipeline-resume` | `false` | Resume from manifest checkpoint |

## Behavioral Summary

Decomposes complex multi-domain operations into Epic→Story→Task hierarchies with DAG-based dependency resolution, then actively delegates to specialist sub-agents via the Task tool. Supports multi-phase pipeline DAGs for complex orchestration flows. Uses Auggie MCP for codebase-aware domain detection, Serena for symbol-level dependency mapping and session persistence, and Sequential MCP for complex DAG reasoning.

## Activation

**MANDATORY**: Before executing any protocol steps, invoke:
> Skill sc:spawn-protocol

Do NOT proceed with protocol execution using only this command file.
The full behavioral specification is in the protocol skill.

## Examples

### Complex Feature Implementation
```
/sc:spawn "implement user authentication system"
# Domains detected: database, backend-api, frontend-ui, testing
# Delegates: /sc:design (schema) → /sc:implement (API) → /sc:build (UI) → /sc:test
```

### Large-Scale Migration (Deep Analysis)
```
/sc:spawn "migrate legacy monolith to microservices" --strategy wave --depth deep
# 5-wave orchestration with Serena checkpoints at each wave boundary
```

### Plan-Only Preview
```
/sc:spawn "establish CI/CD pipeline with security scanning" --no-delegate
# Produces hierarchy document without spawning agents
```

### Pipeline DAG
```
/sc:spawn --pipeline "analyze -> design | implement -> test" --depth deep
# Multi-phase: analyze first, then design and implement in parallel, then test
```

### Pipeline from YAML
```
/sc:spawn --pipeline @.dev/pipeline.yaml
# Load DAG from YAML definition, phases run in parallel by default
```

### Branch-N-Merge (dynamic agent fan-out)
```
/sc:spawn --pipeline @./DAGS/BranchNMerge.yaml \
  --agents opus:architect,haiku:analyzer,sonnet:performance \
  --depth deep \
  --prompt "/sc:brainstorm Think through an ideal solution to this problem"
# Spawns 3 parallel agents (one per --agents spec), each given the same prompt
# Collects all outputs → runs /sc:adversarial --compare --merge on results
```

## Boundaries

**Will:**
- Decompose complex operations into coordinated task hierarchies with dependency graphs
- Actively delegate tasks to sub-agents via Task tool (default behavior)
- Track delegation progress and aggregate results
- Execute multi-phase pipeline DAGs with parallel scheduling

**Will Not:**
- Execute leaf-level implementation tasks directly
- Write or modify application code
- Replace domain-specific commands for simple operations
- Override user coordination preferences
```

**Key changes from v1 spawn.md**:
- Frontmatter now declares MCP servers, personas, and allowed-tools
- Body reduced to ~80 lines with mandatory Skill activation
- Active delegation is default (not "STOP AFTER DECOMPOSITION")
- `--pipeline` mode added for multi-phase DAG execution
- TodoWrite replaced with Task tool family

---

### 2.2 Skill: sc-spawn-protocol/SKILL.md (~450 lines)

```markdown
---
name: sc:spawn-protocol
description: "Full behavioral protocol for sc:spawn — meta-system task orchestration
  with codebase-aware decomposition, DAG-based dependency resolution, and active delegation"
allowed-tools: Read, Glob, Grep, Bash, TaskCreate, TaskUpdate, TaskList, TaskGet, Task, Write
---

# /sc:spawn — Meta-System Orchestration Protocol

<!-- Extended metadata (for documentation, not parsed):
category: special
complexity: high
mcp-servers: [sequential, serena]
personas: [architect, analyzer]
-->

## Triggers

sc:spawn-protocol is invoked ONLY by the `sc:spawn` command via
`Skill sc:spawn-protocol` in the `## Activation` section.
It is never invoked directly by users.

## Classification (MANDATORY FIRST OUTPUT)

Emit this EXACT header format as your first output:

<!-- SC:SPAWN:CLASSIFICATION
strategy: [sequential|parallel|adaptive|wave]
depth: [shallow|normal|deep]
domains_detected: [N]
estimated_tasks: [N]
delegation_mode: [active|plan-only|dry-run]
pipeline_mode: [none|inline|yaml]
-->

## Execution Mode Selection

This protocol supports two execution modes:

### Standard Mode (default)
Task description → domain analysis → decomposition → delegation.
Triggered by: `/sc:spawn "task description" [flags]`

### Pipeline Mode
User-defined multi-phase DAG with explicit phase types and dependencies.
Triggered by: `/sc:spawn --pipeline "<shorthand>" [flags]` or `--pipeline @path.yaml`
Pipeline phases run in parallel by default (respecting DAG dependencies).
Use `--pipeline-seq` to force strictly sequential execution.

**Selection rule**: If `--pipeline` flag is present, enter Pipeline Mode (skip Waves 1-2,
use pipeline parser instead). Otherwise, enter Standard Mode.

---

## Standard Mode: 4-Wave Execution Protocol

### Wave 0: Prerequisites

**Preconditions**: User has provided a task description.
**STOP if**: No task description provided AND no `--pipeline` flag. Emit usage hint and exit.

1. Parse flags: `--strategy`, `--depth`, `--no-delegate`, `--dry-run`, `--resume`
2. If `--resume`: Load Serena memory checkpoint, skip to last incomplete wave
3. Load codebase context (parallel):
   - **Query 1** (Auggie): "{task_description} — find relevant code, existing
     implementations, module boundaries, and integration points"
   - **Query 2** (Auggie): "Project architecture, directory structure, domain
     boundaries, and conventions"
4. If Auggie unavailable: WARN, fall back to Serena `get_symbols_overview`
   on top-level directories (depth: 1). If Serena also unavailable, fall back
   to Glob pattern matching + Grep keyword search.

**Postconditions**: Codebase context loaded. Flags parsed. Ready for analysis.
**Checkpoint**: Save wave-0 state to Serena memory.

### Wave 1: Scope Analysis

**Preconditions**: Wave 0 complete. Codebase context available.

1. **Domain Detection**: From codebase context, identify distinct technical domains
   touched by the task. Classify each as one of:
   - `database` | `backend-api` | `frontend-ui` | `infrastructure` |
     `security` | `testing` | `documentation` | `devops` | `data-pipeline`
2. **Module Mapping**: For each detected domain, identify:
   - Primary directories/files affected
   - Key symbols (classes, functions, endpoints) via Serena `find_symbol`
   - External dependencies and integration points
3. **Dependency Detection**: Use Serena `find_referencing_symbols` to trace
   cross-module dependencies. Build adjacency list of domain→domain
   dependencies.
4. **Complexity Assessment**: Score overall complexity (0.0-1.0):
   - domain_count > 3: +0.3
   - cross-module_dependencies > 5: +0.2
   - estimated_files > 20: +0.2
   - security_domain_involved: +0.2
   - If complexity > 0.7 AND `--strategy auto`: auto-upgrade to `wave` strategy

**Agent delegation**: If `--depth deep` OR domain_count > 4, dispatch
`spawn-planner` agent via Task tool for thorough codebase analysis. Use its
structured output (domain_map, dependency_graph, complexity_score) instead
of inline analysis.

**Postconditions**: Domain list, module map, dependency adjacency list, complexity score.
**Checkpoint**: Save wave-1 state to Serena memory.

### Wave 2: Decomposition

**Preconditions**: Wave 1 complete. Domain and dependency data available.
**Load ref**: `refs/decomposition-patterns.md`
**Load ref**: `refs/dependency-graph.md` (if cross-module_dependencies > 5)

1. **Epic Construction**: One Epic per detected domain (or logical grouping
   if domains overlap heavily — merge when >60% shared files).
2. **Story Decomposition**: Break each Epic into Stories representing
   coherent units of work. Apply granularity rules from ref:
   - `shallow`: 1-2 Stories per Epic (high-level only)
   - `normal`: 2-5 Stories per Epic
   - `deep`: 3-8 Stories per Epic with subtask decomposition
3. **Task Assignment**: Each Story becomes one or more Tasks. Each Task
   maps to exactly one `/sc:*` command for delegation.
4. **DAG Construction**: Using the dependency adjacency list from Wave 1:
   - Tasks with no cross-domain dependencies → parallel group
   - Tasks depending on outputs from other domains → sequential with
     explicit `depends_on` edges
   - Detect parallel groups (tasks safe to run concurrently)
   - Use Sequential MCP for complex dependency reasoning if
     cross-module_dependencies > 5
5. **Strategy Application**:
   - `sequential`: All tasks in linear dependency order
   - `parallel`: Maximum parallelism, only hard dependencies enforced
   - `adaptive`: Hybrid — parallelize where safe, sequence where required
   - `wave`: Group into 3-5 execution waves with checkpoints between

**Postconditions**: Complete task hierarchy with DAG edges and parallel groups.
**Checkpoint**: Save wave-2 state to Serena memory.

### Wave 3: Delegation

**Preconditions**: Wave 2 complete. Task hierarchy with DAG available.
**Load ref**: `refs/delegation-matrix.md`

**If `--dry-run`**: Output the task hierarchy document and STOP. Do not
create tasks or spawn agents.

**If `--no-delegate`**: Create TaskCreate entries for tracking but do NOT
spawn sub-agents. Output hierarchy document with delegation map.

**Default (active delegation)**:

1. **Task Creation**: For each Task in the hierarchy:
   - `TaskCreate` with description, status `pending`, dependencies noted
2. **Prompt Construction**: For each delegated task, apply prompt
   construction rules (from delegation-matrix ref):
   - Rule 1: Resolve file paths before delegation (Glob/Read)
   - Rule 2: Inject tiered evidence requirements (verification vs discovery)
   - Rule 3: Inject cross-reference counts when available
   - Do NOT override delegated command's output structure
3. **Agent Dispatch**: For each parallel group, dispatch tasks via Task tool:
   - Read the appropriate agent `.md` file from `src/superclaude/agents/`
   - Inject agent definition + enriched prompt into Task prompt
   - Dispatch up to MAX_CONCURRENT (10) tasks per parallel group
   - If group exceeds 10: split into sub-groups, dispatch sequentially
   - Wait for group completion before dispatching dependent groups
4. **Progress Tracking**:
   - `TaskUpdate` as each sub-agent completes
   - `TaskList`/`TaskGet` for status monitoring
   - If a sub-agent fails: retry once, then mark as `manual` and continue
5. **Result Aggregation**: Collect outputs from all completed tasks.
   Compile summary with per-task status.

**Agent delegation**: If tasks_created > 8, dispatch `spawn-orchestrator`
agent to handle steps 3-5 instead of inline execution.

**Postconditions**: All tasks delegated (or documented). Results aggregated.

---

## Pipeline Mode

Pipeline Mode provides explicit multi-phase DAG execution for complex
orchestration flows that don't fit the standard decompose-and-delegate pattern.

### Pipeline Input Formats

#### Inline Shorthand
```
--pipeline "phase_type:details -> phase_type:details"
```

Syntax:
- `->` = sequential dependency (phase B depends on phase A)
- `|` = parallel group (phases run concurrently)
- Phase types: `analyze`, `design`, `implement`, `test`, `review`, `deploy`, `generate-parallel`, `compare-merge`
- Phases can include target hints: `implement:backend`, `test:integration`

Examples:
```
--pipeline "analyze -> design | implement -> test"
--pipeline "analyze:security -> implement:auth -> test:security | review:compliance"
--pipeline "design:schema -> implement:api | implement:frontend -> test:e2e"
```

#### YAML File
```
--pipeline @path/to/pipeline.yaml
```

YAML schema:
```yaml
phases:
  - id: analyze-scope
    type: analyze
    target: "authentication system"
    command: "/sc:analyze --focus architecture"
    config:
      depth: deep

  - id: design-schema
    type: design
    target: "user database schema"
    command: "/sc:design --type database"
    depends_on: [analyze-scope]

  - id: impl-backend
    type: implement
    target: "auth API endpoints"
    command: "/sc:implement"
    depends_on: [design-schema]

  - id: impl-frontend
    type: implement
    target: "login UI components"
    command: "/sc:build --feature"
    depends_on: [design-schema]
    parallel_group: 1  # Same group as impl-backend

  - id: test-integration
    type: test
    target: "end-to-end auth flow"
    command: "/sc:test --coverage --e2e"
    depends_on: [impl-backend, impl-frontend]
```

### Dynamic Phase Types

Beyond static phases, the YAML schema supports two dynamic phase types
that interact with `--agents` and `--prompt` from the CLI:

#### `generate-parallel` — Dynamic Agent Fan-Out

Expands at parse time into N parallel phases, one per `--agents` spec.
This is the primary mechanism for the "branch" pattern.

```yaml
- id: branch
  type: generate-parallel
  source: agents        # Expand from --agents CLI flag
  prompt: prompt        # Each agent receives --prompt CLI value
  command_template: "${prompt}"  # What each agent executes
  output_format: md     # Each agent writes <output_dir>/<branch_id>/<agent_id>.md
```

**Expansion rule**: At parse time, `generate-parallel` with `source: agents`
expands into N concrete phases where N = length of `--agents` list:

```
Input:  --agents opus:architect,haiku:analyzer,sonnet:performance
        --prompt "/sc:brainstorm Think through an ideal solution"

Expands to:
  - id: branch-opus-architect
    type: generate
    agent: opus:architect
    command: "/sc:brainstorm Think through an ideal solution"
    parallel_group: auto  (all siblings share same group)

  - id: branch-haiku-analyzer
    type: generate
    agent: haiku:analyzer
    command: "/sc:brainstorm Think through an ideal solution"
    parallel_group: auto

  - id: branch-sonnet-performance
    type: generate
    agent: sonnet:performance
    command: "/sc:brainstorm Think through an ideal solution"
    parallel_group: auto
```

**Validation**:
- STOP if `source: agents` but `--agents` not provided on CLI
- STOP if `--agents` list is empty
- WARN if agent count > MAX_CONCURRENT (10) — will dispatch in sub-batches

#### `compare-merge` — Collect-All Comparison

Automatically collects all output artifacts from a dependency group and
feeds them to `/sc:adversarial --compare`. This is the "merge" pattern.

```yaml
- id: merge
  type: compare-merge
  depends_on: [branch]       # Collects ALL outputs from 'branch' (expanded phases)
  command: "/sc:adversarial"
  config:
    depth: inherit           # Inherits --depth from CLI
    merge: true              # Passes --merge to adversarial
```

**Collection rule**: When `depends_on` references a `generate-parallel` phase ID,
`compare-merge` collects outputs from ALL expanded sub-phases:

```
depends_on: [branch]
  → resolves to: [branch-opus-architect, branch-haiku-analyzer, branch-sonnet-performance]
  → collects: [
      <output_dir>/branch-opus-architect/output.md,
      <output_dir>/branch-haiku-analyzer/output.md,
      <output_dir>/branch-sonnet-performance/output.md
    ]
  → passes to: /sc:adversarial --compare file1.md,file2.md,file3.md --depth deep --merge
```

**Validation**:
- STOP if collected files < 2 (need at least 2 for comparison)
- `depth: inherit` resolves to the `--depth` value from CLI invocation
- `merge: true` appends `--merge` flag to the adversarial invocation

### Complete DAG Example: BranchNMerge.yaml

```yaml
# BranchNMerge.yaml — Fan-out N agents with same prompt, merge results
# Usage: /sc:spawn --pipeline @./DAGS/BranchNMerge.yaml \
#          --agents opus:architect,haiku:analyzer,sonnet:performance \
#          --depth deep \
#          --prompt "/sc:brainstorm Think through an ideal solution"

phases:
  - id: branch
    type: generate-parallel
    source: agents
    prompt: prompt
    command_template: "${prompt}"
    output_format: md

  - id: merge
    type: compare-merge
    depends_on: [branch]
    command: "/sc:adversarial"
    config:
      depth: inherit
      merge: true
```

**Resolved DAG** (for 3 agents):
```
┌─────────────────────┐  ┌─────────────────────┐  ┌──────────────────────────┐
│ branch-opus-architect│  │branch-haiku-analyzer │  │branch-sonnet-performance │
│ /sc:brainstorm ...   │  │ /sc:brainstorm ...   │  │ /sc:brainstorm ...       │
│ model: opus          │  │ model: haiku         │  │ model: sonnet            │
│ persona: architect   │  │ persona: analyzer    │  │ persona: performance     │
└──────────┬──────────┘  └──────────┬──────────┘  └────────────┬─────────────┘
           │                        │                           │
           └────────────┬───────────┘───────────────────────────┘
                        │
           ┌────────────▼────────────┐
           │ merge                    │
           │ /sc:adversarial          │
           │   --compare a.md,b.md,  │
           │     c.md                 │
           │   --depth deep --merge   │
           └─────────────────────────┘
```

### Pipeline Execution

1. **Parse**: Parse inline shorthand or load YAML file
   - Validate: no cycles in dependency graph
   - Validate: all `depends_on` references exist
   - If parse error: STOP with details
2. **Expand Dynamic Phases**: Before DAG construction
   - For each `generate-parallel` phase: expand into N concrete phases
     from `--agents` list. STOP if `--agents` not provided.
   - For each `compare-merge` phase: resolve `depends_on` references
     to expanded phase IDs (fan-in collection)
   - Resolve `inherit` config values from CLI flags (`--depth`, etc.)
   - Substitute `${prompt}` from `--prompt` CLI value. STOP if missing.
   - Log resolved DAG for debugging (visible in `--dry-run`)
3. **DAG Construction**: Build execution graph from resolved phases
   - Assign auto-IDs to inline phases (phase_1, phase_2, ...)
   - Compute parallel groups from dependency structure
   - Apply concurrency cap: MAX_CONCURRENT = 10 (split oversized groups)
   - If `--pipeline-seq`: force all phases into linear chain (one at a time)
3. **Phase Dispatch**: Execute phases respecting DAG + concurrency cap
   - For each phase, construct Task prompt from phase definition
   - Use delegation-matrix ref for agent type and model selection
   - Dispatch phases in same parallel group concurrently (up to 10)
   - Wait for all dependencies before dispatching dependent phases
4. **Artifact Routing**: Pass outputs between phases
   - Each phase writes to `<output_dir>/<phase_id>/`
   - Dependent phases receive resolved paths to dependency outputs
   - Verify dependency output exists before dispatching consumer
5. **Progress & Resume**:
   - Write manifest at `<output_dir>/spawn-manifest.json` with phase statuses
   - `--pipeline-resume`: Read manifest, skip completed phases, resume from
     first incomplete phase
   - Save checkpoints to Serena memory at phase-group boundaries

### Pipeline Manifest Schema

```json
{
  "pipeline_id": "spawn-<timestamp>",
  "created": "ISO-8601",
  "phases": [
    {
      "id": "phase_id",
      "type": "analyze|design|implement|test|review|deploy",
      "status": "pending|running|completed|failed|skipped",
      "command": "/sc:* invocation",
      "depends_on": ["phase_ids"],
      "output_dir": "path",
      "started_at": "ISO-8601|null",
      "completed_at": "ISO-8601|null",
      "error": "message|null"
    }
  ]
}
```

---

## Return Contract

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | `success` \| `partial` \| `failed` |
| `task_hierarchy_path` | string | Path to written hierarchy document |
| `tasks_created` | int | Number of TaskCreate entries |
| `delegation_map` | object | Task ID → delegated `/sc:*` command |
| `parallel_groups` | list | Groups of tasks safe to run concurrently |
| `completion_summary` | object | Per-task status (completed/failed/manual) |
| `pipeline_manifest` | string\|null | Path to manifest (Pipeline Mode only) |

## Agent Delegation

| Agent | Role | Dispatched By | When |
|-------|------|--------------|------|
| `spawn-planner` | Deep codebase analysis for domain/dependency detection | This skill (Wave 1) | Always for `--depth deep`, or when domain_count > 4 |
| `spawn-orchestrator` | Progress tracking and result aggregation | This skill (Wave 3) | When tasks_created > 8 |

**Dispatch protocol**: Read agent `.md` via Read tool → inject into Task prompt.

## Error Handling

| Scenario | Behavior | Fallback |
|----------|----------|----------|
| Missing task description (no `--pipeline`) | STOP with usage hint | None |
| Auggie unavailable | WARN, use Serena `get_symbols_overview` | Glob + Grep |
| Serena unavailable | WARN, use Grep for dependency detection | Native file analysis |
| Sequential unavailable | WARN, use native reasoning for DAG | Simpler parallel groups |
| Sub-agent delegation fails | Retry once, mark as `manual` | Continue with N-1 tasks |
| Depth exceeds token budget | Auto-downgrade to `normal` | WARN user |
| `--resume` but no checkpoint | WARN, start from Wave 0 | Full restart |
| Pipeline YAML parse error | STOP with parse error details | None |
| Pipeline cycle detected | STOP, report cycle path | None |
| Pipeline phase fails | Mark failed, continue independent phases | Skip dependent phases |
| `generate-parallel` but no `--agents` | STOP with error: "--agents required for generate-parallel phase" | None |
| `${prompt}` but no `--prompt` | STOP with error: "--prompt required for this DAG" | None |
| `compare-merge` collects < 2 files | STOP with error: "Need ≥2 artifacts for comparison" | None |

## Will Do
- Decompose complex operations into DAG-structured task hierarchies
- Actively delegate to sub-agents with enriched prompts
- Track progress and aggregate results across parallel groups
- Persist state at wave boundaries for session resumability
- Execute multi-phase pipeline DAGs with parallel scheduling

## Will Not Do
- Execute leaf-level implementation tasks directly
- Write or modify application code
- Override delegated command protocols or output formats
- Skip dependency analysis for parallel safety
```

---

### 2.3 Ref: refs/decomposition-patterns.md (~130 lines)

Loaded: Wave 2 only.

```markdown
# Decomposition Patterns Reference

## Epic Construction Rules

### Domain-to-Epic Mapping
Each detected domain typically maps to one Epic. Merge domains when:
- Two domains share >60% of the same files
- One domain has only 1-2 files (absorb into nearest domain)

### Naming Convention
Epic names follow: `[DOMAIN] — [Outcome Description]`
Examples:
- `DATABASE — Design and implement user schema`
- `BACKEND-API — Build authentication endpoints`
- `TESTING — Establish integration test coverage`

## Story Granularity by Depth

### Shallow (--depth shallow)
- 1-2 Stories per Epic
- Each Story represents a complete domain deliverable
- No subtask decomposition
- Best for: High-level planning, estimation, overview

### Normal (--depth normal)
- 2-5 Stories per Epic
- Stories represent coherent feature slices
- Light subtask notes (bullet points, not formal tasks)
- Best for: Sprint planning, team coordination

### Deep (--depth deep)
- 3-8 Stories per Epic
- Stories decomposed into formal subtasks
- Each subtask has: description, estimated complexity, tool hints
- Best for: Solo execution, detailed delegation, complex migrations

## Task-to-Command Mapping Rules

Each Task maps to exactly ONE `/sc:*` command. Selection criteria:

| Task Type | Primary Command | Fallback |
|-----------|----------------|----------|
| Schema/model design | `/sc:design --type database` | `/sc:design --type component` |
| API design | `/sc:design --type api` | `/sc:design --type architecture` |
| Architecture decisions | `/sc:design --type architecture` | — |
| Feature implementation | `/sc:implement` | `/sc:build` |
| Bug fix | `/sc:task "fix ..."` | `/sc:troubleshoot` |
| Test creation | `/sc:test` | `/sc:task "test ..."` |
| Documentation | `/sc:document` | — |
| Code cleanup | `/sc:cleanup` | `/sc:improve` |
| Security hardening | `/sc:task --force-strict` | `/sc:analyze --focus security` |
| Infrastructure/DevOps | `/sc:task` with devops persona | `/sc:implement` |
| Research/investigation | `/sc:research` | `/sc:analyze` |

## DAG Edge Rules

### Hard Dependencies (sequential)
- Schema design MUST complete before API implementation
- API implementation MUST complete before frontend integration
- Core module changes MUST complete before dependent module changes
- Security audit SHOULD complete before deployment tasks

### Soft Dependencies (parallel-safe with coordination)
- Tests can start in parallel with implementation (test-first)
- Documentation can start in parallel with implementation
- Independent domain Epics with no shared files

### Parallel Group Assignment
Tasks in the same parallel group:
- Share no file dependencies
- Have no data-flow dependencies
- Can be dispatched as concurrent Task tool calls
```

---

### 2.4 Ref: refs/dependency-graph.md (~120 lines)

Loaded: Wave 2 only (when cross-module_dependencies > 5).

```markdown
# Dependency Graph Construction Reference

## DAG Data Structure

The dependency graph is represented as:
```
nodes: [{ id, epic, story, task_description, command, parallel_group }]
edges: [{ from_id, to_id, type: "hard"|"soft", reason }]
```

## Construction Algorithm

### Step 1: Initialize Nodes
For each Task produced by decomposition:
- Create node with auto-generated ID: `task_{epic_index}_{story_index}_{task_index}`
- Assign initial parallel_group: 0 (unassigned)

### Step 2: Detect Hard Edges
For each pair of nodes (A, B):
1. Check if A's output files overlap with B's input files → hard edge A→B
2. Check if A and B share domain dependencies from Wave 1 adjacency list
   → hard edge from the dependency direction
3. Apply domain ordering rules from decomposition-patterns ref:
   - database → backend → frontend → testing (canonical flow)
   - infrastructure → any dependent domain

### Step 3: Detect Soft Edges
For each pair of nodes without hard edges:
1. Same domain but independent features → soft edge (advisory)
2. Test tasks for implementation tasks → soft edge (can parallelize with test-first)

### Step 4: Cycle Detection
Run topological sort (Kahn's algorithm concept):
1. Compute in-degree for each node
2. Enqueue all nodes with in-degree 0
3. Process queue: dequeue → add to sorted order → reduce neighbors' in-degree
4. If sorted order contains all nodes: DAG is valid
5. If not: cycle exists — STOP and report the cycle path

### Step 5: Parallel Group Assignment
1. Compute topological levels: nodes with in-degree 0 are level 0
2. Each level becomes a candidate parallel group
3. Within each level, verify tasks share no file dependencies — tasks with
   shared files must be split into separate sub-groups (sequential within level)
4. Apply concurrency cap (see Concurrency Cap section below):
   if a parallel group has > MAX_CONCURRENT tasks, split into sub-groups
   of size MAX_CONCURRENT dispatched sequentially
5. If `--pipeline-seq`: collapse all groups into single-task sequential chain

### Concurrency Cap

**MAX_CONCURRENT = 10** (implicit, not user-configurable)

This cap applies uniformly across both Standard Mode and Pipeline Mode:

- When a parallel group contains N tasks and N > 10:
  split into ceil(N/10) sub-groups of up to 10 tasks each
- Sub-groups within the same topological level execute sequentially
  (group A's 10 tasks complete → group B's next 10 dispatch)
- All sub-groups must complete before the next topological level starts

**What CAN run in parallel** (must satisfy ALL):
1. No hard edge exists between the tasks (no `depends_on` relationship)
2. No shared output files (A doesn't write to files B reads)
3. Tasks are in the same topological level (all prerequisites satisfied)
4. Group size ≤ 10 (enforced by splitting)

**What CANNOT run in parallel** (any ONE blocks):
1. Hard edge: A→B means B waits for A to complete
2. File conflict: A and B both write to the same file
3. Different topological level: B depends (transitively) on A
4. `--pipeline-seq` flag: forces all tasks sequential regardless

## Strategy Application to DAG

### Sequential
Force all tasks into a single chain: flatten topological order,
add hard edge between each consecutive pair. parallel_groups = [[task_1], [task_2], ...]

### Parallel
Only hard edges enforced. Maximum parallelism within each topological level.
parallel_groups = [level_0_tasks, level_1_tasks, ...]

### Adaptive (default)
Respect both hard and soft edges. Group by topological level.
Split large levels into sub-groups for resource management.

### Wave
Group topological levels into 3-5 named waves:
- Wave A: Foundation (levels 0-1: infrastructure, schema, core)
- Wave B: Implementation (levels 2-3: features, endpoints, components)
- Wave C: Integration (levels 3-4: integration, testing, deployment)
- Wave D: Validation (final level: end-to-end tests, documentation)
Insert Serena checkpoint between each wave.

## Pipeline Shorthand Parser

### Grammar
```
pipeline     = phase_group ("→" phase_group)*
phase_group  = phase ("|" phase)*
phase        = type [":" target]
type         = "analyze" | "design" | "implement" | "test" | "review" | "deploy"
               | "generate-parallel" | "compare-merge"
target       = identifier  (alphanumeric + hyphens)
```

`->` (or `→`) = sequential dependency between groups
`|` = parallel within a group

### Parse Algorithm
1. Split on `->` to get sequential groups
2. Within each group, split on `|` to get parallel phases
3. Assign auto-IDs: `phase_{group_index}_{phase_index}`
4. Create hard edges: each phase in group N+1 depends on ALL phases in group N
5. Return nodes and edges in the standard DAG format
```

---

### 2.5 Ref: refs/delegation-matrix.md (~150 lines)

Loaded: Wave 3 only.

```markdown
# Delegation Matrix Reference

## Command Delegation Targets

### Implementation Commands
| Command | When to Delegate | Persona | MCP Hint |
|---------|-----------------|---------|----------|
| `/sc:implement` | New feature, endpoint, module | backend, frontend | --c7 |
| `/sc:build` | Compile, package, scaffold | devops | -- |
| `/sc:task` | General task, compound operations | auto-detect | --seq |
| `/sc:task --force-strict` | Security, auth, database changes | security | --seq |

### Design Commands
| Command | When to Delegate | Persona | MCP Hint |
|---------|-----------------|---------|----------|
| `/sc:design --type architecture` | System structure, patterns | architect | --seq |
| `/sc:design --type api` | Endpoint contracts, schemas | backend | --c7 |
| `/sc:design --type database` | Schema, migrations, models | backend | --c7 |
| `/sc:design --type component` | UI component interfaces | frontend | --magic |

### Quality Commands
| Command | When to Delegate | Persona | MCP Hint |
|---------|-----------------|---------|----------|
| `/sc:test` | Test creation, coverage analysis | qa | --play |
| `/sc:analyze` | Code review, quality assessment | analyzer | --seq |
| `/sc:cleanup` | Dead code, structure optimization | refactorer | --seq |

### Research Commands
| Command | When to Delegate | Persona | MCP Hint |
|---------|-----------------|---------|----------|
| `/sc:research` | External knowledge, library docs | — | --tavily |
| `/sc:explain` | Understanding existing code | mentor | --c7 |

## Agent Selection for Task Dispatch

When dispatching via the Task tool, select the Claude Code agent type
based on the delegated command:

| Delegated Command | Agent Type | Model Hint |
|-------------------|-----------|------------|
| `/sc:design` | system-architect | opus |
| `/sc:implement` | general-purpose | opus |
| `/sc:build` | devops-architect | sonnet |
| `/sc:test` | quality-engineer | sonnet |
| `/sc:analyze` | general-purpose | opus |
| `/sc:cleanup` | refactoring-expert | sonnet |
| `/sc:research` | deep-research-agent | opus |
| `/sc:task` | general-purpose | opus |

## Prompt Construction Rules

When constructing prompts for delegated agents, sc:spawn MUST enrich
the user's intent with operational specificity. Passing a bare goal
to a delegated command produces structurally sound but evidence-thin
output. However, do NOT override the delegated command's own output
structure — delegated protocols produce better analytical organization
than orchestrator-imposed templates.

### Rule 1: Resolve File Paths Before Delegation

Before spawning agents, resolve all input file paths using Glob/Read.
Each agent prompt MUST include absolute paths to every file the agent
needs to read. Never delegate path discovery to the sub-agent.

For async task hierarchies where agents run later or in separate
contexts, include path hints (directory + glob pattern) rather than
requiring pre-resolution of every path.

### Rule 2: Inject Tiered Evidence Requirements

Delegated prompts that produce analytical output MUST include an
evidence standard, but the tier depends on the task type:

**Verification tasks** (coverage checks, dependency validation,
consistency audits):
> Evidence standard: cite specific line numbers, task IDs, section
> references, or direct quotes from source documents for every finding.
> Unsupported assertions must be flagged as LOW CONFIDENCE.

**Discovery tasks** (gap detection, risk assessment, open-ended
reflection):
> Evidence standard: support findings with specific references where
> possible. Findings based on inference or absence of evidence should
> be flagged as INFERENTIAL and include the reasoning chain.

### Rule 3: Inject Cross-Reference Counts (When Available)

When Rule 1 has already read a source document and the delegated task
involves coverage verification, extract and inject the known count
(e.g., "The merged plan contains 20 edits — verify all 20 are
covered"). Do NOT pre-read documents solely for counting — this rule
applies opportunistically.

## Dispatch Template

When constructing a Task tool dispatch:

```
You are executing a delegated task from /sc:spawn orchestration.

## Task
{enriched_task_description}

## Files
{resolved_absolute_paths}

## Evidence Standard
{tiered_evidence_requirement}

## Cross-References
{injected_counts_if_available}

## Delegated Command
Execute this as: {delegated_sc_command}

## Output
Write results to: {output_path}
```
```

---

### 2.6 Agent: spawn-orchestrator.md (~70 lines)

```markdown
---
name: spawn-orchestrator
description: Progress tracking and result aggregation for sc:spawn multi-task orchestrations
category: meta
---

# Spawn Orchestrator

## Triggers
- Invoked by `sc:spawn-protocol` skill during Wave 3 when tasks_created > 8
- Large-scale delegations requiring dedicated progress management
- Multi-group parallel dispatches requiring coordination across groups

## Behavioral Mindset
Track progress across all delegated tasks with precision. Focus on status
accuracy, failure detection, and comprehensive result aggregation. Never
execute leaf tasks — only monitor and report.

## Model Preference
High-capability model (opus preferred). Requires strong reasoning for
coordinating many concurrent agents and synthesizing diverse outputs.

## Tools
- **TaskCreate**: Create tracked tasks for each delegation
- **TaskUpdate**: Update status as sub-agents complete or fail
- **TaskList**: Monitor overall progress across all tasks
- **TaskGet**: Retrieve detailed status for specific tasks
- **Task**: Dispatch sub-agents for delegated commands
- **Read**: Load agent definitions for prompt injection
- **Write**: Produce orchestration summary and hierarchy document
- **Glob**: Discover output artifacts from completed tasks

## Responsibilities

1. **Create task entries**: One TaskCreate per delegated task from the hierarchy
2. **Dispatch parallel groups**: Launch concurrent Task agents for each
   parallel group, respecting DAG ordering between groups
3. **Monitor completion**: Poll TaskList/TaskGet for status updates
4. **Handle failures**: Retry failed tasks once, then mark as `manual`
   and continue with remaining tasks
5. **Aggregate results**: Collect outputs from all completed tasks,
   compile summary with per-task status and artifact paths
6. **Produce orchestration report**: Write hierarchy document with final
   status, delegation map, and completion summary

## Outputs
- **spawn-hierarchy.md**: Full task hierarchy with DAG, delegation map,
  and per-task completion status
- **Return contract fields**: status, tasks_created, delegation_map,
  parallel_groups, completion_summary

## Does NOT
- Execute leaf-level implementation work
- Write or modify application code
- Make architectural decisions about task decomposition
- Override the delegation matrix from the skill protocol

## Boundaries

**Will:**
- Track and aggregate results from arbitrarily many concurrent delegations
- Apply retry-once policy for failed tasks with clear escalation path
- Report progress at group-completion boundaries

**Will Not:**
- Modify task decomposition produced by Wave 2
- Skip tasks or reorder DAG dependencies
- Proceed past a group boundary if a hard-dependency task failed
```

---

### 2.7 Agent: spawn-planner.md (~65 lines)

```markdown
---
name: spawn-planner
description: Deep codebase analysis for domain detection and dependency mapping in sc:spawn orchestrations
category: analysis
---

# Spawn Planner

## Triggers
- Invoked by `sc:spawn-protocol` skill during Wave 1 when `--depth deep`
  or when domain_count > 4
- Complex codebases requiring thorough module boundary and dependency analysis
- Tasks involving unfamiliar or large-scale codebases

## Behavioral Mindset
Investigate the codebase systematically to produce accurate domain maps
and dependency graphs. Prioritize precision over speed — missed dependencies
cause delegation failures. Use semantic tools (Auggie, Serena) first,
fall back to pattern-based tools only when semantic tools are unavailable.

## Model Preference
High-capability model (opus preferred). Deep codebase analysis requires
strong reasoning about code relationships and architectural boundaries.

## Tools
- **mcp__auggie-mcp__codebase-retrieval**: Semantic codebase search for
  domain detection and architecture understanding
- **Serena tools** (get_symbols_overview, find_symbol, find_referencing_symbols):
  Symbol-level navigation for dependency tracing
- **Read**: Load specific files identified by semantic search
- **Glob**: Discover file patterns within detected domains
- **Grep**: Keyword search for cross-module references

## Responsibilities

1. **Domain detection**: Identify distinct technical domains affected by
   the task using Auggie retrieval + directory structure analysis
2. **Module boundary mapping**: For each domain, identify primary
   directories, entry points, and key symbols
3. **Dependency tracing**: Use Serena `find_referencing_symbols` to build
   cross-module dependency adjacency list
4. **Complexity scoring**: Assess overall complexity based on domain count,
   dependency density, file count, and security involvement
5. **Produce structured analysis**: Output domain map, dependency graph,
   and complexity score in structured format for Wave 2 consumption

## Outputs
- **Domain map**: List of domains with primary directories and key symbols
- **Dependency graph**: Adjacency list of domain→domain dependencies with
  evidence (specific symbols/files that create the dependency)
- **Complexity score**: 0.0-1.0 with factor breakdown

## Does NOT
- Decompose tasks into Epics or Stories (that's Wave 2)
- Make delegation decisions (that's Wave 3)
- Modify any files
- Execute any implementation work

## Boundaries

**Will:**
- Produce accurate, evidence-backed domain maps and dependency graphs
- Use the best available tools (Auggie → Serena → Glob/Grep fallback chain)
- Flag LOW CONFIDENCE findings when dependency evidence is inferential

**Will Not:**
- Guess at dependencies without evidence from code analysis
- Proceed without investigating all domains detected in initial scan
- Modify the codebase or produce implementation artifacts
```

---

## 3. Data Flow Diagram

```
User: /sc:spawn "implement user auth system" --depth deep

┌─────────────────────────────────────────────┐
│  spawn.md (Thin Entry)                      │
│  Parse flags → Skill sc:spawn-protocol      │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│  SKILL.md — Wave 0: Prerequisites           │
│  ├─ Validate input (STOP if missing)        │
│  ├─ Parse flags                             │
│  ├─ Auggie Query 1 (task-specific) ─┐       │
│  └─ Auggie Query 2 (architecture)  ─┤parallel│
│                                      │       │
│  Checkpoint → Serena memory                  │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│  SKILL.md — Wave 1: Scope Analysis          │
│  ├─ Domain detection                        │
│  ├─ [If deep/complex] Task: spawn-planner   │
│  │   └─ Returns: domain_map, dep_graph,     │
│  │                complexity_score           │
│  ├─ Module mapping (Serena find_symbol)      │
│  └─ Dependency detection (find_referencing)  │
│                                              │
│  Checkpoint → Serena memory                  │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│  SKILL.md — Wave 2: Decomposition           │
│  Load: refs/decomposition-patterns.md       │
│  Load: refs/dependency-graph.md (if complex) │
│  ├─ Epic construction (1 per domain)        │
│  ├─ Story decomposition (by depth)          │
│  ├─ Task→Command mapping                    │
│  └─ DAG construction (parallel groups)      │
│      [If deps > 5] Sequential MCP reasoning │
│                                              │
│  Checkpoint → Serena memory                  │
└──────────────────┬──────────────────────────┘
                   │
       ┌───────────┼───────────┐
       │ --dry-run  │ default   │ --no-delegate
       ▼           ▼           ▼
    Output      Active       TaskCreate
    hierarchy   delegation   only + output
    + STOP      continues    hierarchy
                   │
┌──────────────────▼──────────────────────────┐
│  SKILL.md — Wave 3: Delegation              │
│  Load: refs/delegation-matrix.md            │
│  ├─ TaskCreate for each task                │
│  ├─ Prompt enrichment (Rules 1-3)           │
│  ├─ [If tasks > 8] Task: spawn-orchestrator │
│  │   └─ Handles dispatch + tracking         │
│  ├─ [If tasks ≤ 8] Direct dispatch:         │
│  │   ├─ Parallel Group 1 → [Task, Task]     │
│  │   ├─ Wait for completion                 │
│  │   ├─ Parallel Group 2 → [Task, Task]     │
│  │   └─ ...                                 │
│  └─ Result aggregation + return contract    │
└─────────────────────────────────────────────┘
```

### Pipeline Mode Data Flow

```
User: /sc:spawn --pipeline "analyze -> design | implement -> test"

┌─────────────────────────────────────────────┐
│  spawn.md (Thin Entry)                      │
│  Detect --pipeline → Skill sc:spawn-protocol │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│  SKILL.md — Pipeline Parser                 │
│  Load: refs/dependency-graph.md             │
│  ├─ Parse shorthand/YAML                    │
│  ├─ Validate DAG (cycle detection)          │
│  ├─ Compute parallel groups                 │
│  └─ Emit classification header              │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│  SKILL.md — Pipeline Execution              │
│  Load: refs/delegation-matrix.md            │
│  ├─ Phase Group 1: [analyze]                │
│  │   └─ Task: dispatch analyze phase        │
│  │   └─ Wait for completion                 │
│  ├─ Phase Group 2: [design, implement]      │
│  │   └─ Task: dispatch design (parallel)    │
│  │   └─ Task: dispatch implement (parallel) │
│  │   └─ Wait for all                        │
│  ├─ Phase Group 3: [test]                   │
│  │   └─ Task: dispatch test phase           │
│  │   └─ Wait for completion                 │
│  └─ Write manifest + return contract        │
└─────────────────────────────────────────────┘
```

---

## 4. Framework Registration Changes

| File | Change |
|------|--------|
| `COMMANDS.md` | Add/update spawn entry with new MCP servers, personas, tools, pipeline flags |
| `ORCHESTRATOR.md` | Update routing table entry for spawn with new complexity/confidence |
| `FLAGS.md` | Add `--no-delegate`, `--dry-run`, `--resume`, `--pipeline`, `--pipeline-seq`, `--pipeline-resume` |

---

## 5. Migration Checklist

- [ ] Create `src/superclaude/skills/sc-spawn-protocol/SKILL.md`
- [ ] Create `src/superclaude/skills/sc-spawn-protocol/refs/decomposition-patterns.md`
- [ ] Create `src/superclaude/skills/sc-spawn-protocol/refs/dependency-graph.md`
- [ ] Create `src/superclaude/skills/sc-spawn-protocol/refs/delegation-matrix.md`
- [ ] Create `src/superclaude/agents/spawn-orchestrator.md`
- [ ] Create `src/superclaude/agents/spawn-planner.md`
- [ ] Rewrite `src/superclaude/commands/spawn.md` as thin entry
- [ ] Remove all TodoWrite references (replace with Task tool family)
- [ ] Update COMMANDS.md, ORCHESTRATOR.md, FLAGS.md
- [ ] `make sync-dev && make verify-sync`
- [ ] Manual validation: invoke `/sc:spawn "test task" --dry-run`
- [ ] Manual validation: invoke `/sc:spawn --pipeline "analyze -> test" --dry-run`

---

## 6. Design Decisions Log

| Decision | Rationale |
|----------|-----------|
| Delegate by default | Name is "spawn" — it should spawn things. `--no-delegate` for plan-only. |
| 2 agents only (orchestrator + planner) | Tracker deferred to future CLI release. Orchestrator handles tracking inline for now. |
| 3 refs instead of prior spec's 3+1 | Prompt construction merged into delegation-matrix (both Wave 3). dependency-graph replaces it as Wave 2 ref. |
| Pipeline shorthand uses `->` and `\|` | Consistent with adversarial's shorthand but simplified for spawn's use case. |
| Pipeline YAML schema is flat (no nesting) | Keep it simple — DAG structure comes from `depends_on`, not YAML nesting. |
| Serena checkpoints at wave boundaries | Enables `--resume` for long-running orchestrations across conversations. |
| Sequential MCP only for complex DAGs | Most decompositions don't need it — only when cross_module_deps > 5. |
| Auggie as primary codebase tool | Best semantic understanding for domain detection. Serena as symbol-level supplement. |
| `generate-parallel` + `compare-merge` over `${var}` template engine | Purpose-built phase types cover branch-N-merge pattern (90% of dynamic DAG use cases) without general template complexity. Adding a full template engine would require: escaping rules, recursive substitution, loop constructs, error reporting for unresolved vars — all for marginal flexibility. New directive types can be added incrementally if needed. |
| Implicit MAX_CONCURRENT=10 over user-configurable flag | Simplifies CLI surface. 10 is generous enough for any realistic agent fan-out. `--pipeline-seq` covers the "I want sequential" case. |
| `--agents` and `--prompt` on spawn command (not in DAG) | CLI flags are the interface between user intent and DAG template. DAG references them by name (`source: agents`, `prompt: prompt`), keeping DAGs reusable across different agent sets and prompts. |
| Static BranchNMerge.yaml over BranchNMerge2/3/5 variants | One DAG + dynamic expansion beats N static files. Expansion is deterministic (N = len(--agents)), debuggable (resolved DAG logged in --dry-run), and composes with arbitrary agent specs. |
