# Critical Issues — Consolidated Remediation Proposals

## Implementation Summary & Dependency Order

### Application Order

Proposals have interdependencies. Apply in this order to avoid conflicts:

| Order | Proposal | Title | Depends On | Touches |
|-------|----------|-------|------------|---------|
| 1 | **C3** | Output Directory Specification | — | SKILL.md (Wave 0, Wave 3, Pipeline, Return Contract), spawn.md, refs/delegation-matrix.md |
| 2 | **C6** | `generate` Phase Type Missing from Grammar | C3 (output paths) | refs/dependency-graph.md, refs/delegation-matrix.md, SKILL.md |
| 3 | **C1** | Zero/Empty Attack on `--agents` | C6 (agent spec usage) | SKILL.md (Step 2, generate-parallel, Error Handling) |
| 4 | **C2** | Complexity Threshold Boundary Fix | — | SKILL.md (Wave 1 Step 4) |
| 5 | **C5** | Missing `Skill` in allowed-tools | C6 (compare-merge dispatch) | spawn.md, SKILL.md (compare-merge pattern) |
| 6 | **C4** | Sub-Agent Timeout Specification | C3 (output paths), C5 (dispatch pattern) | refs/delegation-matrix.md, SKILL.md (Wave 3, Error Handling), spawn.md |

### Cross-Proposal Dependencies (Flagged)

1. **C1 <-> C6**: Both depend on `--agents` parsing. C1 defines adversarial validation for agent specs. C6 defines how those parsed specs feed into `generate` phase expansion. C1's parsing MUST run before C6's expansion step. Both proposals edit SKILL.md Step 2 (Expand Dynamic Phases) — edits must be merged carefully.

2. **C3 <-> C4**: Both reference `<output_dir>/tasks/<task_id>/`. C3 defines the directory structure; C4 assumes it exists for partial output handling. Apply C3 first so C4's path references are valid.

3. **C3 <-> C6**: Both define artifact output paths for `generate` phases. C3 Step 4 says generate produces `output.md`. C6 Step 2 says generate writes to `<output_dir>/phases/<phase_id>/output.md`. These are consistent but should be read together.

4. **C4 <-> C5**: Both define how compare-merge is dispatched. C5 defines the Task tool dispatch pattern; C4 defines the timeout applied to that dispatch. The timeout multiplier (2.0x) from C4 must be applied to the Task dispatch defined in C5 Step 4.

5. **C5 <-> C6**: Both add to `refs/delegation-matrix.md`. C6 adds a "Special Phase Types" section covering both `generate` and `compare-merge`. C5 defines the compare-merge dispatch pattern. These must be reconciled into a single coherent section in delegation-matrix.md — C6 Step 3 should be the canonical location, with C5 Step 4 providing the invocation detail.

### Shared File Edit Map

Files touched by multiple proposals (merge carefully):

| File | Proposals | Sections |
|------|-----------|----------|
| `SKILL.md` | C1, C2, C3, C4, C5, C6 | Step 2 (C1, C6), Wave 1 Step 4 (C2), Wave 0/3/Pipeline (C3), Wave 3 dispatch (C4, C5), Error matrix (C1, C4), Manifest schema (C6) |
| `spawn.md` | C3, C4, C5 | Flags table (C3: `--output`, C4: `--timeout`), allowed-tools (C5: remove `Skill`) |
| `refs/delegation-matrix.md` | C3, C4, C6 | Dispatch template (C3), Timeout config (C4), Special Phase Types (C6) |
| `refs/dependency-graph.md` | C6 | Grammar, shorthand parse error |

### Gaps Not Fully Covered by Any Proposal

1. **`--dry-run` interaction with output directory (C3 gap)**: C3 says "STOP if directory exists and is non-empty AND --resume is not set" but does not specify whether `--dry-run` should skip directory creation entirely. Recommendation: `--dry-run` should NOT create the output directory — it should validate the path and report what would be created.

2. **Pipeline Mode timeout/retry semantics (C4 gap)**: C4's retry logic ("retry runs in the NEXT dispatch cycle") is designed for Standard Mode parallel groups. In Pipeline Mode, a timed-out phase blocks all downstream DAG dependents. C4 should specify: in Pipeline Mode, retry the timed-out phase immediately (not deferred), because dependents cannot proceed until it completes or is marked manual. If marked manual, all transitive dependents should also be marked manual with reason "blocked by timed-out dependency <phase_id>".

3. **`generate` phase error handling (C4 + C6 gap)**: C4 adds timeout rows to the error handling matrix but does not address `generate`-specific errors (e.g., agent spec valid at parse time but model unavailable at dispatch time). C6 defines `generate` but doesn't add error handling rows. Recommendation: add to error matrix: `| generate phase model unavailable | STOP: "Model <model> unavailable for generate phase <id>" | None |`.

4. **`compare-merge` with 0 or 1 inputs (C5 + C6 gap)**: If all `generate` phases in a parallel group time out or fail, the `compare-merge` phase receives 0 inputs. If all but one fail, it receives 1 input. Neither C5 nor C6 defines behavior for these degenerate cases. Recommendation: 0 inputs = STOP with error; 1 input = WARN and pass through as merged output (no adversarial debate needed).

---

# C1: Zero/Empty Attack on `--agents` — Remediation Proposal

## Problem
The guard `STOP if source: agents but --agents not provided on CLI` only checks flag presence, not parsed content. `--agents ""`, `--agents ","`, or `--agents "invalid"` all bypass the guard.

## Cross-References
- **C6**: The parsed agent specs from C1's validation feed directly into C6's `generate` phase expansion. C1 validates; C6 consumes.
- **C3**: Validated agent count affects the number of output directories created under `<output_dir>/phases/`.

## Step-by-Step Solution

### Step 1: Replace presence check with parsed-count validation
**Location**: SKILL.md -> Pipeline Execution -> Step 2 (Expand Dynamic Phases)

Current:
```
STOP if `source: agents` but `--agents` not provided on CLI
```

Replace with:
```
1. STOP if `source: agents` but `--agents` flag not provided ->
   Error: "--agents required for generate-parallel phase"
2. Parse --agents value using adversarial agent-spec parsing rules
3. STOP if parsed agent list is empty (0 valid specs) ->
   Error: "--agents provided but contains no valid agent specifications.
   Expected format: model[:persona[:"instruction"]], e.g. opus:architect"
4. WARN if any individual spec failed parsing ->
   "Skipped invalid agent spec '<raw>': <reason>. Continuing with N valid agents."
5. STOP if valid agent count < 1 after filtering ->
   Error: "All --agents specs were invalid. None could be parsed."
```

### Step 2: Define parsing validation for each degenerate case

| Input | Parse Result | Behavior |
|-------|-------------|----------|
| `""` (empty string) | 0 specs | STOP: "contains no valid agent specifications" |
| `","` (commas only) | 0 specs after split+filter | STOP: same |
| `",,opus,"` | 1 valid (opus), 2 empty | WARN about empties, continue with 1 |
| `"invalid-model"` | 0 valid (model not recognized) | STOP: "All specs invalid" |
| `"opus:invalid-persona"` | 1 valid | WARN: "Unknown persona 'invalid-persona', using model defaults" (per adversarial convention) |
| `"opus:architect:unquoted instruction"` | Parse error | WARN: "Instruction must be quoted", skip this spec |

### Step 3: Align with adversarial agent-spec parsing rules
Import the exact parsing rules from `refs/agent-specs.md`:
- Split on `,` to get individual specs
- For each spec, split on `:` (max 3 segments)
- Segment 1 (model): REQUIRED, must be recognized model name
- Segment 2 (persona): OPTIONAL, WARN if unknown
- Segment 3 (instruction): OPTIONAL, must be double-quoted

### Step 4: Add validation to generate-parallel definition in SKILL.md

Add after the expansion rule:
```
**Post-parse validation**:
- Filter empty strings from split result
- Validate each spec against agent-spec parsing rules
- Collect valid specs and parsing warnings
- STOP if valid_count == 0
- WARN for each skipped spec (with reason)
- Proceed with valid specs only
```

### Step 5: Update error handling matrix
Add row:
```
| `--agents` present but all specs invalid | STOP: "All --agents specs invalid" | None |
| `--agents` has mix of valid/invalid | WARN per invalid, continue with valid | Skip invalid specs |
```

## Files to Modify
- `SKILL.md`: Pipeline Execution Step 2 validation
- `SKILL.md`: generate-parallel Validation section
- `SKILL.md`: Error Handling matrix (add 2 rows)


---

# C2: Complexity Threshold Boundary Fix — Remediation Proposal

## Problem
The complexity guard uses `> 0.7` but scoring factors can produce exactly 0.7, creating ambiguous boundary behavior. The same `>` vs `>=` issue exists across multiple thresholds.

## Cross-References
- **None**: C2 is self-contained. The complexity score does not interact with Pipeline Mode, agent parsing, or output directories.

## Step-by-Step Solution

### Step 1: Audit all threshold comparisons in the spec

| Guard | Current | Threshold | Boundary Behavior | Fix |
|-------|---------|-----------|-------------------|-----|
| Complexity auto-upgrade | `> 0.7` | 0.7 | At 0.7: no upgrade | Change to `>= 0.7` |
| domain_count planner dispatch | `> 4` | 4 | At 4: no dispatch | Keep `> 4` (5+ triggers) |
| tasks_created orchestrator | `> 8` | 8 | At 8: no orchestrator | Keep `> 8` (9+ triggers) |
| cross_module_deps ref load | `> 5` | 5 | At 5: no load | Keep `> 5` (6+ triggers) |
| MAX_CONCURRENT | `> 10` (implicit) | 10 | At 10: no split | Keep (10 fits in one batch) |

**Rationale**:
- Complexity: 0.7 IS the documented "complex" threshold -- it should trigger. Fix: `>=`
- domain_count: 4 domains is manageable inline. 5+ justifies planner agent. Keep `>`
- tasks_created: 8 tasks is manageable inline. 9+ justifies orchestrator. Keep `>`
- cross_module_deps: 5 deps is manageable. 6+ justifies Sequential MCP. Keep `>`

### Step 2: Cap complexity score at 1.0

Current scoring is additive with no cap:
- domain_count > 3: +0.3
- cross_module_deps > 5: +0.2
- estimated_files > 20: +0.2
- security_domain: +0.2

Maximum possible: 0.3 + 0.2 + 0.2 + 0.2 = 0.9 (cannot exceed 1.0 with current factors)

**Add explicit cap**: `complexity_score = min(1.0, sum_of_factors)`

This future-proofs against adding new factors that could push past 1.0.

### Step 3: Apply the fix to Wave 1 Step 4

Current text:
```
If complexity > 0.7 AND `--strategy auto`: auto-upgrade to `wave` strategy
```

Replace with:
```
If complexity >= 0.7 AND `--strategy auto`: auto-upgrade to `wave` strategy
```

### Step 4: Add scoring factor documentation

Add after the factor list:
```
**Scoring rules**:
- Factors are additive (each condition independently adds to score)
- Score is capped at 1.0: `complexity = min(1.0, sum_of_factors)`
- Threshold for wave auto-upgrade: >= 0.7
- All other thresholds in the spec use strict `>` (not `>=`)
```

## Files to Modify
- `SKILL.md`: Wave 1 Step 4 -- change `>` to `>=` for complexity only
- `SKILL.md`: Wave 1 Step 4 -- add `min(1.0, ...)` cap
- `refs/dependency-graph.md`: No changes (thresholds there are correct as `>`)


---

# C3: Output Directory Specification — Remediation Proposal

## Problem
The spec references `<output_dir>` throughout but never defines the `--output` flag or default convention. Artifact routing between pipeline phases is unresolvable without this.

## Cross-References
- **C4**: Timeout partial output handling (Step 3) writes to paths defined here.
- **C6**: `generate` phase output paths follow the convention established here.
- **C5**: compare-merge output path in Task dispatch (Step 4) uses `<output_dir>/phases/<phase_id>/`.

## Step-by-Step Solution

### Step 1: Add `--output` flag to command and skill

Add to spawn.md Options table:
```
| `--output` | `./spawn-output/` | Output directory for hierarchy, manifest, and phase artifacts |
```

Add to SKILL.md Wave 0 flag parsing (step 1):
```
Parse flags: --strategy, --depth, --no-delegate, --dry-run, --resume, --output
```

### Step 2: Define default output directory convention

```
Default: ./spawn-output/

When --output is provided: use that path directly.
When --output is not provided:
  - Standard Mode: ./spawn-output/
  - Pipeline Mode: ./spawn-output/

The directory is created at Wave 0 (Standard) or Pipeline Parse step (Pipeline).
STOP if directory exists and is non-empty AND --resume is not set AND --dry-run is not set.
WARN if directory exists and --resume IS set (will append/overwrite).
SKIP directory creation if --dry-run is set (validate path only).
```

**Implementation note**: The `--dry-run` clause was not in the original proposal but is necessary to prevent side effects during dry runs. See Gaps section in the summary.

### Step 3: Define complete directory structure

**Standard Mode**:
```
<output_dir>/
  spawn-classification.md       # Machine-readable classification header
  spawn-hierarchy.md            # Full task hierarchy with DAG
  spawn-summary.md              # Return contract as human-readable summary
  tasks/
    task_1_0_0/                 # Per-task output from delegated agents
      output.md
    task_1_0_1/
      output.md
    ...
```

**Pipeline Mode**:
```
<output_dir>/
  spawn-manifest.json           # Pipeline manifest with phase statuses
  spawn-classification.md       # Machine-readable classification header
  resolved-dag.md               # Resolved DAG (post-expansion, for debugging)
  phases/
    <phase_id>/
      output.md                 # Primary output from phase
      ...                       # Additional artifacts (phase-type dependent)
    <phase_id>/
      ...
```

### Step 4: Define artifact naming convention per phase type

| Phase Type | Primary Output | Additional Artifacts |
|-----------|---------------|---------------------|
| `analyze` | `output.md` | -- |
| `design` | `output.md` | -- |
| `implement` | `output.md` | Modified source files (in-place) |
| `test` | `output.md` | -- |
| `review` | `output.md` | -- |
| `deploy` | `output.md` | -- |
| `generate` (expanded) | `output.md` | -- |
| `compare-merge` | `merged-output.md` | `diff-analysis.md`, `debate-transcript.md`, `base-selection.md`, `refactor-plan.md`, `merge-log.md` |

### Step 5: Update artifact routing to use conventions

Current (vague):
```
Each phase writes to `<output_dir>/<phase_id>/`
Dependent phases receive resolved paths to dependency outputs
```

Replace with:
```
Each phase writes to `<output_dir>/phases/<phase_id>/`
Primary output is always `output.md` (or `merged-output.md` for compare-merge)
Dependent phases receive resolved paths:
  - For single-output phases: `<output_dir>/phases/<dep_id>/output.md`
  - For compare-merge phases: `<output_dir>/phases/<dep_id>/merged-output.md`
  - For generate-parallel (collecting all): glob `<output_dir>/phases/<parent_id>-*/output.md`
```

### Step 6: Update return contract

Add to return contract:
```
| `output_dir` | string | Absolute path to output directory |
| `artifacts_dir` | string|null | Path to compare-merge artifacts (Pipeline Mode with compare-merge only) |
```

### Step 7: Update Standard Mode to use output_dir

spawn-hierarchy.md currently has no defined location. Fix:
```
Wave 3 writes: <output_dir>/spawn-hierarchy.md
Wave 3 writes: <output_dir>/spawn-summary.md (return contract)
Per-task outputs: <output_dir>/tasks/<task_id>/output.md
```

## Files to Modify
- `spawn.md`: Add `--output` to flags table and usage line
- `SKILL.md`: Wave 0 flag parsing, directory creation
- `SKILL.md`: Wave 3 output paths
- `SKILL.md`: Pipeline Execution artifact routing
- `SKILL.md`: Return contract (add output_dir, artifacts_dir)
- `refs/delegation-matrix.md`: Dispatch template `{output_path}` resolution


---

# C4: Sub-Agent Timeout Specification — Remediation Proposal

## Problem
No timeout defined for delegated sub-agents. A hung agent blocks the entire parallel group and all dependent groups indefinitely.

## Cross-References
- **C3**: Partial output paths (`<output_dir>/tasks/<task_id>/`) depend on C3's directory structure.
- **C5**: The compare-merge Task dispatch defined in C5 Step 4 should include the 2.0x timeout multiplier defined here.
- **C6**: `generate` phases dispatched per C6 should use the `generate` command multiplier (1.0x base) defined here.

## Step-by-Step Solution

### Step 1: Define tiered timeout system

Timeouts are determined by TWO factors: depth level and command type.

**Base timeouts by depth**:
| Depth | Base Timeout | Rationale |
|-------|-------------|-----------|
| `shallow` | 120s (2 min) | Quick assessment, minimal analysis |
| `normal` | 300s (5 min) | Standard task execution |
| `deep` | 600s (10 min) | Thorough analysis with MCP calls |

**Command-type multipliers**:
| Command Category | Multiplier | Rationale |
|-----------------|-----------|-----------|
| Design commands (`/sc:design`) | 1.0x | Standard complexity |
| Implementation (`/sc:implement`, `/sc:build`) | 1.5x | Code generation takes longer |
| Analysis (`/sc:analyze`, `/sc:cleanup`) | 1.0x | Read-heavy, bounded |
| Testing (`/sc:test`) | 1.5x | Test execution adds time |
| Research (`/sc:research`) | 2.0x | Web search has latency |
| General (`/sc:task`) | 1.0x | Default |
| Pipeline generate phase | 1.0x | Uses base timeout |
| Pipeline compare-merge | 2.0x | Adversarial pipeline is multi-step |

**Effective timeout** = `base_timeout[depth] x command_multiplier`

Examples:
- `/sc:design` at `normal` depth: 300s x 1.0 = 300s (5 min)
- `/sc:research` at `deep` depth: 600s x 2.0 = 1200s (20 min)
- `/sc:implement` at `shallow` depth: 120s x 1.5 = 180s (3 min)

### Step 2: Define timeout -> retry -> escalation flow

**Standard Mode** (parallel task groups):
```
1. Dispatch agent with timeout_ms = effective_timeout x 1000
2. If agent completes within timeout -> success, collect output
3. If timeout fires:
   a. Mark task as TIMED_OUT (not failed -- distinction matters)
   b. Check for partial output at task's output_dir
   c. If partial output exists: save it as <task_id>/partial-output.md
   d. RETRY ONCE with timeout extended by 50%:
      retry_timeout = effective_timeout x 1.5
   e. If retry also times out:
      - Mark task as `manual`
      - Log: "Task <id> timed out after retry (<total_seconds>s).
        Marked as manual. Partial output at: <path>"
      - Continue with remaining tasks in the parallel group
4. Do NOT block the parallel group while retrying:
   - Retry runs in the NEXT dispatch cycle (after current batch)
   - Other tasks in the group continue unaffected
```

**Pipeline Mode** (DAG phases):
```
1-3. Same as Standard Mode
4. Pipeline-specific retry behavior:
   - Retry the timed-out phase IMMEDIATELY (not deferred to next cycle),
     because downstream DAG dependents are blocked until this phase
     completes or is marked manual.
   - If retry also times out:
     a. Mark phase as `manual`
     b. Mark all transitive dependents as `manual` with reason:
        "Blocked by timed-out dependency <phase_id>"
     c. Continue executing any independent DAG branches
```

**Implementation note**: The Pipeline Mode retry semantics differ from Standard Mode because DAG dependencies create blocking chains. Deferring retry to the next cycle (as in Standard Mode) would leave dependents in an unresolvable waiting state.

### Step 3: Handle partial output from timed-out agents

```
When a timeout fires:
1. The Task tool may have partial output in its working directory
2. Check if <output_dir>/tasks/<task_id>/output.md exists (Standard Mode)
   or <output_dir>/phases/<phase_id>/output.md exists (Pipeline Mode)
3. If it exists but may be incomplete:
   - Rename to partial-output.md
   - Add header: "<!-- PARTIAL: Agent timed out after Ns. Content may be incomplete. -->"
4. If no output exists: create empty marker file
   - <task_id>/TIMED_OUT with timestamp and timeout value
```

### Step 4: Specify where timeout config lives

Timeout configuration lives in `refs/delegation-matrix.md` (loaded Wave 3), not in SKILL.md.

Add section to delegation-matrix.md:
```
## Timeout Configuration

### Base Timeouts (by depth)
| Depth | Timeout (seconds) |
|-------|------------------|
| shallow | 120 |
| normal | 300 |
| deep | 600 |

### Command Multipliers
[table from Step 1]

### Timeout Formula
effective_timeout = base_timeout[depth] x command_multiplier
retry_timeout = effective_timeout x 1.5
```

### Step 5: Add `--timeout` override flag (optional, not default)

Add to spawn.md flags:
```
| `--timeout` | -- | Override timeout in seconds for all tasks (disables tiered system) |
```

When `--timeout N` is provided: all tasks use N seconds, ignoring the tiered system. This is an escape hatch for users who know their tasks need unusual time.

### Step 6: Update error handling matrix

Add rows:
```
| Sub-agent timeout (first attempt) | Retry once with 1.5x timeout | Save partial output |
| Sub-agent timeout (retry) | Mark as `manual`, continue | Log timeout, save partial |
| Pipeline phase timeout (retry) | Mark phase + transitive dependents as `manual` | Log cascade |
```

## Files to Modify
- `refs/delegation-matrix.md`: Add Timeout Configuration section
- `SKILL.md`: Wave 3 Step 3 (Agent Dispatch) -- add timeout to Task dispatch
- `SKILL.md`: Error handling matrix -- add 3 rows (not 2 -- Pipeline Mode adds one)
- `spawn.md`: Add `--timeout` optional override flag


---

# C5: Missing `Skill` in SKILL.md allowed-tools — Remediation Proposal

## Problem
Command frontmatter includes `Skill` in allowed-tools but SKILL.md omits it. The `compare-merge` phase needs to invoke `/sc:adversarial`.

## Cross-References
- **C6**: C6 Step 3 defines the delegation-matrix entry for compare-merge. C5 Step 4 defines the invocation pattern. These must be reconciled into a single coherent section in `refs/delegation-matrix.md`.
- **C4**: The Task dispatch in C5 Step 4 must include the timeout from C4 (compare-merge multiplier = 2.0x).

## Step-by-Step Solution

### Step 1: Analyze invocation approaches

**Option A -- Skill tool (direct skill invocation)**:
- Spawn skill invokes `Skill sc:adversarial-protocol` directly
- Runs in same context, shares tool access
- Pros: simple, efficient, natural skill-to-skill pattern
- Cons: loads adversarial protocol into spawn's context (token cost)

**Option B -- Task tool (sub-agent invocation)**:
- Spawn dispatches a Task agent whose prompt says "run /sc:adversarial --compare ..."
- Sub-agent has its own context and tool access
- Pros: isolated context, adversarial runs independently
- Cons: agent overhead, needs its own Skill access

### Step 2: Recommend Task tool approach

**Recommendation: Use Task tool** (Option B)

Rationale:
1. **Consistency**: All other delegation in spawn uses Task tool (Wave 3 dispatch, orchestrator, planner). compare-merge should follow the same pattern.
2. **Context isolation**: Adversarial is a heavy protocol (~2000 token SKILL.md + refs). Loading it into spawn's context via Skill tool would compete for token budget with spawn's own protocol.
3. **Error containment**: If adversarial fails, the Task agent fails cleanly. The spawn skill gets the failure and applies its retry-once policy. With Skill tool, a failure could corrupt spawn's own state.
4. **The adversarial command itself is a thin entry that invokes its skill**: The Task agent will load adversarial.md -> invoke `Skill sc:adversarial-protocol`. This is the standard flow.

### Step 3: Define exact allowed-tools changes

**spawn.md (command)** -- REMOVE `Skill` from allowed-tools:
```
Current:  allowed-tools: Read, Glob, Grep, Bash, TaskCreate, TaskUpdate, TaskList, TaskGet, Task, Write, Skill
Fixed:    allowed-tools: Read, Glob, Grep, Bash, TaskCreate, TaskUpdate, TaskList, TaskGet, Task, Write
```

Why: The spawn command delegates to the skill. The skill does all the work. The command doesn't need `Skill` -- it already invokes the skill via the `## Activation` section (which is handled by the framework, not the allowed-tools list).

**SKILL.md** -- NO change needed:
```
Current:  allowed-tools: Read, Glob, Grep, Bash, TaskCreate, TaskUpdate, TaskList, TaskGet, Task, Write
Fixed:    (same -- no change)
```

Why: The SKILL.md uses `Task` to dispatch sub-agents. Sub-agents have their own tool access. The spawn skill never directly calls `Skill` -- it delegates everything through `Task`.

### Step 4: Define compare-merge invocation pattern

In SKILL.md Pipeline Execution, the compare-merge phase dispatch should be:
```
For compare-merge phases:
1. Collect output file paths from all dependency phases
2. STOP if 0 dependency outputs exist (all predecessors failed/timed out):
   Error: "compare-merge phase <id> has no inputs. All dependency phases failed."
3. If exactly 1 dependency output exists:
   WARN: "compare-merge phase <id> has only 1 input. Skipping adversarial debate,
   passing through as merged output."
   Copy single input to <output_dir>/phases/<phase_id>/merged-output.md
   Skip adversarial dispatch.
4. If 2+ dependency outputs exist, construct adversarial invocation:
   /sc:adversarial --compare <file1>,<file2>,...,<fileN> --depth <depth> --merge
5. Dispatch via Task tool:
   - Agent type: general-purpose (adversarial handles its own agent delegation)
   - Model: opus
   - Timeout: effective_timeout with 2.0x compare-merge multiplier (see C4)
   - Prompt: "Execute: /sc:adversarial --compare <files> --depth <depth> --merge
              Output to: <output_dir>/phases/<phase_id>/"
6. The Task agent will:
   - Load adversarial.md command
   - Invoke Skill sc:adversarial-protocol
   - Execute the 5-step adversarial pipeline
   - Write artifacts to the specified output directory
```

**Implementation note**: Steps 2-3 handle the degenerate cases identified in the Gaps section of the summary. Without these guards, compare-merge would invoke adversarial with 0 or 1 inputs, causing undefined behavior.

### Step 5: Verify consistency with other cross-command patterns

| Command | Invokes | Via | Pattern |
|---------|---------|-----|---------|
| sc:task-unified | quality-engineer agent | Task | Sub-agent dispatch |
| sc:adversarial | debate-orchestrator | Task | Sub-agent dispatch |
| sc:adversarial | merge-executor | Task | Sub-agent dispatch |
| sc:spawn (proposed) | adversarial | Task | Sub-agent dispatch |

All follow the same pattern: parent skill -> Task tool -> sub-agent.

## Files to Modify
- `spawn.md`: Remove `Skill` from allowed-tools (it's unnecessary)
- `SKILL.md`: No change to allowed-tools (already correct)
- `SKILL.md`: Document compare-merge dispatch pattern using Task tool (including degenerate input guards)


---

# C6: `generate` Phase Type Missing from Grammar — Remediation Proposal

## Problem
The `generate-parallel` expansion produces phases with `type: generate` but `generate` is not in the valid phase type list. The grammar, manifest schema, and delegation matrix don't account for it.

## Cross-References
- **C1**: The `--agents` parsing validated by C1 produces the agent specs consumed by `generate` phase expansion here.
- **C3**: Output paths for `generate` phases follow C3's `<output_dir>/phases/<phase_id>/output.md` convention.
- **C5**: The `compare-merge` delegation-matrix entry defined in C5 must live in the same "Special Phase Types" section added here (Step 3). Merge these edits.
- **C4**: `generate` phases should use the "Pipeline generate phase" timeout multiplier (1.0x) from C4 Step 1.

## Step-by-Step Solution

### Step 1: Add `generate` as a valid phase type

`generate` is the expanded form of `generate-parallel`. It represents a single agent executing a prompt -- fundamentally different from the existing phase types which map to `/sc:*` commands.

**Updated grammar**:
```
type = "analyze" | "design" | "implement" | "test" | "review" | "deploy"
       | "generate-parallel" | "generate" | "compare-merge"
```

Note: `generate-parallel` is a YAML-only directive (expanded at parse time). `generate` is the resulting concrete phase type. `generate-parallel` does NOT appear in the inline shorthand grammar -- it only exists in YAML definitions.

### Step 2: Define `generate` phase behavior

Unlike other phase types, `generate` phases:
1. Do NOT map to a `/sc:*` command via the delegation matrix
2. Use the agent spec directly from the `--agents` expansion (model + persona)
3. Execute the `command_template` (resolved `${prompt}`) as the agent's task
4. Always produce `output.md` as primary artifact

```
generate phase dispatch:
  - Agent type: determined by --agents spec (e.g., opus -> general-purpose)
  - Model: from agent spec (e.g., opus, sonnet, haiku)
  - Persona: from agent spec (e.g., architect, analyzer)
  - Prompt: resolved command_template value
  - Timeout: effective_timeout with 1.0x generate multiplier (see C4)
  - Output: <output_dir>/phases/<phase_id>/output.md
```

### Step 3: Define delegation matrix bypass for `generate` phases

Add to `refs/delegation-matrix.md`:
```
## Special Phase Types

### generate (from generate-parallel expansion)
Generate phases bypass the standard delegation matrix. Agent selection
comes from the `--agents` CLI flag, not from command-to-agent mapping.

| Source | Agent Type | Model | Persona |
|--------|-----------|-------|---------|
| `--agents` spec | general-purpose | from spec | from spec |

The delegation matrix's Command Delegation Targets, Agent Selection,
and Prompt Construction Rules (Rules 1-3) still apply to generate phases:
- Rule 1: File paths resolved before delegation (if applicable)
- Rule 2: Evidence requirements injected (discovery tier)
- Rule 3: Cross-reference counts injected (if available)

### compare-merge (collect-all comparison)
Compare-merge phases use the adversarial command. Agent selection:
| Delegated Command | Agent Type | Model |
|-------------------|-----------|-------|
| `/sc:adversarial` | general-purpose | opus |

See SKILL.md Pipeline Execution compare-merge dispatch pattern (C5)
for full invocation details including degenerate input handling.
```

**Implementation note**: This section is also referenced by C5 Step 4. When applying both C5 and C6, write the Special Phase Types section once, incorporating both the `generate` bypass (from C6) and the compare-merge invocation details (from C5).

### Step 4: Update Pipeline Manifest Schema

Current type enum:
```
"type": "analyze|design|implement|test|review|deploy"
```

Updated:
```
"type": "analyze|design|implement|test|review|deploy|generate|compare-merge"
```

Note: `generate-parallel` is NEVER in the manifest -- it's expanded before the manifest is created. Only the resulting `generate` phases appear.

### Step 5: Update the expansion output to use `generate` consistently

Current expansion example (already correct but needs explicit validation):
```
Expands to:
  - id: branch-opus-architect
    type: generate          <- now a valid type
    agent: opus:architect
    command: "/sc:brainstorm Think through an ideal solution"
    parallel_group: auto
```

Add to expansion rule documentation:
```
Expansion produces phases with:
  - type: "generate" (NOT "generate-parallel" -- the directive is consumed)
  - id: "<parent_id>-<model>-<persona>" (auto-generated)
  - agent: "<model>:<persona>" (from --agents spec)
  - command: resolved command_template with ${prompt} substituted
  - parallel_group: auto (all siblings share same group)
```

### Step 6: Validate inline shorthand does not support generate-parallel

The inline shorthand grammar only supports concrete phase types. `generate-parallel` requires YAML because it needs structured fields (`source`, `command_template`, `output_format`).

Add clarification:
```
Note: `generate-parallel` and `compare-merge` are YAML-only phase types.
They cannot be expressed in inline shorthand because they require structured
configuration fields. Use YAML file input for DAGs that include dynamic phases.
```

If a user tries `--pipeline "generate-parallel -> compare-merge"`, the parser should STOP with:
```
Error: 'generate-parallel' requires YAML definition (--pipeline @file.yaml).
It cannot be used in inline shorthand because it needs 'source' and
'command_template' configuration fields.
```

### Step 7: Add error handling for generate-specific failures

Add to error handling matrix:
```
| generate phase model unavailable | STOP: "Model <model> unavailable for generate phase <id>" | None |
| generate phase agent spec invalid at dispatch | STOP: "Agent spec <spec> failed validation" | Should not occur if C1 validation ran |
```

**Implementation note**: This step was not in the original proposal. See Gaps section in the summary.

## Files to Modify
- `refs/dependency-graph.md`: Update grammar to include `generate`
- `refs/dependency-graph.md`: Add parse error for generate-parallel in shorthand
- `refs/delegation-matrix.md`: Add Special Phase Types section (merge with C5 compare-merge entry)
- `SKILL.md`: Update manifest schema type enum
- `SKILL.md`: Clarify expansion output type
- `SKILL.md`: Add inline shorthand restriction note
- `SKILL.md`: Error handling matrix -- add 2 rows for generate-specific failures


---
