# /sc:spec-panel Review — sc:spawn v2 Architecture & Component Design

> **Spec**: `.dev/releases/backlog/v4.xx-SpawnV2/spec.md`
> **Mode**: critique | **Focus**: requirements, architecture, correctness
> **Date**: 2026-03-22

---

## Quality Assessment

| Dimension | Score | Notes |
|-----------|-------|-------|
| **Clarity** | 8.2/10 | Well-structured, good use of tables and diagrams; some ambiguities in mode interactions |
| **Completeness** | 7.5/10 | Strong core protocol; gaps in edge cases, output directory, and mode interaction |
| **Testability** | 6.8/10 | Classification header is machine-readable; most behaviors lack measurable criteria |
| **Consistency** | 7.0/10 | Step numbering bug; some terms shift meaning between sections |

---

## Expert Reviews

### 1. KARL WIEGERS — Requirements Quality Assessment

**CRITICAL: `--strategy` flag has no effect in Pipeline Mode**
The spec defines `--strategy sequential|parallel|adaptive|wave` for Standard Mode (Wave 2, Step 5) but never states whether it applies to Pipeline Mode. Pipeline Mode has `--pipeline-seq` as its own parallelism control. If a user passes `--strategy sequential --pipeline @dag.yaml`, behavior is unspecified.
- RECOMMENDATION: Add explicit statement: "`--strategy` is ignored in Pipeline Mode. Use `--pipeline-seq` for sequential pipeline execution."
- PRIORITY: High — ambiguous flag interaction leads to unpredictable behavior

**MAJOR: No output directory specification**
The spec mentions `<output_dir>/<phase_id>/` multiple times but never defines where `<output_dir>` comes from. There's no `--output` flag and no default convention.
- RECOMMENDATION: Add `--output` flag with default `./spawn-output/<timestamp>/` or follow the existing framework convention of writing next to source.
- PRIORITY: High — without this, artifact routing is unresolvable

**MAJOR: `--prompt` accepts trailing quoted string but parsing is unspecified**
The flags table says `--prompt` is "also accepted as trailing quoted string" but the spec never defines the parsing rule. Does `"text at end"` always become the prompt? What if the user's task description is also quoted?
- RECOMMENDATION: Define explicit precedence: `--prompt` flag wins; trailing quoted string is only used in Pipeline Mode when no `--prompt` flag is present; in Standard Mode, the trailing string IS the task description, not a prompt.
- PRIORITY: High — ambiguous input parsing

**MINOR: `--resume` vs `--pipeline-resume` overlap**
Both flags exist but their scoping is unclear. `--resume` loads Serena checkpoint (Standard Mode). `--pipeline-resume` reads manifest (Pipeline Mode). But what if both are passed? What if `--resume` is passed in Pipeline Mode?
- RECOMMENDATION: `--resume` should be the single flag that works in both modes (Serena checkpoint in Standard, manifest in Pipeline). Eliminate `--pipeline-resume` as redundant.
- PRIORITY: Medium — simplifies CLI surface

---

### 2. GOJKO ADZIC — Specification by Example

**MAJOR: No concrete Given/When/Then for Standard Mode decomposition**
The spec describes the 4-wave protocol abstractly but provides no worked example showing what a real decomposition looks like. The examples section shows invocations but not outputs.
- RECOMMENDATION: Add one complete worked example:
  ```
  Given: /sc:spawn "implement user authentication" --depth normal
  When: Wave 1 detects domains [database, backend-api, frontend-ui, testing]
  Then: Wave 2 produces:
    Epic 1: DATABASE — Design user schema
      Story 1.1: Create users table migration → /sc:design --type database
      Story 1.2: Add index on email column → /sc:implement
    Epic 2: BACKEND-API — Build auth endpoints
      Story 2.1: POST /auth/login → /sc:implement
      ...
    DAG: [1.1] → [1.2, 2.1] → [3.1] → [4.1]
  ```
- PRIORITY: High — without this, implementers must guess what output looks like

**MAJOR: `generate-parallel` expansion produces `type: generate` but `generate` is not a listed phase type**
The expansion example shows `type: generate` as the expanded phase type, but the grammar only lists `analyze | design | implement | test | review | deploy | generate-parallel | compare-merge`. What is `type: generate`?
- RECOMMENDATION: Either add `generate` to the phase type list, or clarify that expanded phases use the original type with a subtype marker.
- PRIORITY: High — invalid type in expanded output

**MINOR: BranchNMerge example has redundant `source` and `prompt` fields**
The `generate-parallel` definition has both `source: agents` and `prompt: prompt` as field references, plus `command_template: "${prompt}"`. The relationship between `prompt` field and `command_template` is unclear — are they the same thing?
- RECOMMENDATION: Simplify to two fields: `source` (where to get agent list) and `command_template` (what each agent runs, with `${prompt}` interpolation). Remove the separate `prompt` field.
- PRIORITY: Low — confusing but inferrable

---

### 3. ALISTAIR COCKBURN — Use Case & Stakeholder Analysis

**MAJOR: Two execution modes with fundamentally different mental models**
Standard Mode is goal-driven ("implement auth system" → automatic decomposition). Pipeline Mode is plan-driven (user defines the DAG). The spec treats them as equal alternatives but they serve very different users:
- Standard Mode: user who knows WHAT but not HOW
- Pipeline Mode: user who knows the exact execution plan

The spec doesn't help users choose between them. The `--pipeline` flag silently switches to a completely different execution path.
- RECOMMENDATION: Add a "When to Use Which Mode" section at the top of the SKILL.md with clear guidance. Consider whether Pipeline Mode should auto-suggest when domain_count = 1 (no decomposition needed).
- PRIORITY: Medium — user confusion, not correctness issue

**MINOR: The spec serves two stakeholders (framework users and implementers) without clear separation**
The command file (spawn.md) is user-facing. The SKILL.md is implementer-facing. But the design doc mixes them in code blocks without clear "this is what the user sees" vs "this is internal protocol."
- RECOMMENDATION: The design doc is fine as-is (it's for implementers). But ensure the actual spawn.md file produced during implementation has a pure user-facing voice.
- PRIORITY: Low

---

### 4. MARTIN FOWLER — Architecture & Interface Design

**CRITICAL: `Skill` not listed in SKILL.md `allowed-tools` but command frontmatter includes it**
The command frontmatter declares `allowed-tools: Read, Glob, Grep, Bash, TaskCreate, TaskUpdate, TaskList, TaskGet, Task, Write, Skill`. The SKILL.md frontmatter declares `allowed-tools: Read, Glob, Grep, Bash, TaskCreate, TaskUpdate, TaskList, TaskGet, Task, Write` — missing `Skill`. If the skill needs to invoke `/sc:adversarial` via the Skill tool (as `compare-merge` implies), it needs `Skill` in its allowlist.
- RECOMMENDATION: Add `Skill` to the SKILL.md allowed-tools, or clarify that `/sc:adversarial` is invoked via the Task tool (as a sub-agent), not the Skill tool.
- PRIORITY: High — `compare-merge` phase may not be able to invoke adversarial

**MAJOR: Dual responsibility in `refs/decomposition-patterns.md`**
This ref contains both decomposition templates (Epic/Story/Task structure) AND task-to-command mapping rules AND DAG edge rules. These are three distinct concerns loaded together in Wave 2. The task-to-command mapping is actually consumed in Wave 3 (delegation), not Wave 2.
- RECOMMENDATION: Move Task-to-Command Mapping Rules to `refs/delegation-matrix.md` where they belong (Wave 3 concern). Keep decomposition-patterns focused on Epic/Story/Task structure and granularity only.
- PRIORITY: Medium — violates lazy-loading principle (loading delegation info in Wave 2)

**MAJOR: Pipeline Execution has duplicate step numbering**
Lines 546-551 show two steps numbered "3" — DAG Construction (step 3) and Phase Dispatch (also step 3). Step 4 (Artifact Routing) and Step 5 (Progress & Resume) follow.
- RECOMMENDATION: Renumber: 1. Parse → 2. Expand → 3. DAG Construction → 4. Phase Dispatch → 5. Artifact Routing → 6. Progress & Resume
- PRIORITY: Medium — implementation will misinterpret step sequence

**MINOR: `dependency-graph.md` ref serves double duty**
It contains both the DAG construction algorithm (Standard Mode) AND the Pipeline Shorthand Parser (Pipeline Mode). These are architecturally separate concerns that happen to share a data structure.
- RECOMMENDATION: Acceptable for now since both produce the same DAG structure. Flag for split if the file exceeds 200 lines during implementation.
- PRIORITY: Low

---

### 5. MICHAEL NYGARD — Reliability & Failure Mode Analysis

**CRITICAL: No timeout specification for sub-agent delegation**
The spec says "retry once, then mark as `manual`" but never defines what constitutes a failure. If a sub-agent hangs indefinitely, there's no timeout to trigger the retry path.
- RECOMMENDATION: Define per-task timeout. Suggest: `shallow` depth = 120s, `normal` = 300s, `deep` = 600s. Timeout triggers the retry-once logic.
- PRIORITY: High — without timeouts, a stuck agent blocks the entire pipeline

**MAJOR: Serena checkpoint data structure undefined**
The spec says "Checkpoint → Serena memory" at every wave boundary but never defines what's saved. What fields? What format? How is it keyed? Can two concurrent spawn sessions collide?
- RECOMMENDATION: Define checkpoint schema:
  ```
  key: spawn-{session_id}-wave-{N}
  data: { task_description, flags, domain_map, dependency_graph,
          task_hierarchy, delegation_map, completed_tasks }
  ```
  Use session-scoped keys to prevent collision.
- PRIORITY: Medium — resume feature is unimplementable without this

**MAJOR: No partial failure recovery in Pipeline Mode**
Error handling says "Pipeline phase fails → Mark failed, continue independent phases → Skip dependent phases." But the manifest schema has no field for tracking which dependent phases were skipped vs never started. On `--pipeline-resume`, how does the system distinguish "skipped because dependency failed" from "not yet started"?
- RECOMMENDATION: Add `skipped_reason` field to manifest phase entries. On resume, phases with `status: skipped` where the dependency is now `completed` (from manual intervention) should be eligible for dispatch.
- PRIORITY: Medium — affects resume correctness

**MINOR: `compare-merge` silently depends on `/sc:adversarial` being available**
If adversarial is not installed or its skill fails to load, `compare-merge` has no fallback defined.
- RECOMMENDATION: Add to error handling: "compare-merge invocation fails → STOP with error, output collected artifacts path for manual comparison"
- PRIORITY: Low — adversarial is a core command, unlikely to be missing

---

### 6. JAMES WHITTAKER — Adversarial Attack Analysis

**CRITICAL — Zero/Empty Attack on `--agents`**: I can break this specification by **Zero/Empty Attack**. The invariant at **generate-parallel validation** fails when **`--agents` is provided but contains zero valid specs after parsing**.
- Concrete attack: `--agents ""` or `--agents ","` or `--agents "invalid-not-a-model"`. State before: `--agents` flag is present (not missing), so the STOP guard "STOP if `source: agents` but `--agents` not provided" does NOT fire. State after: expansion produces 0 phases (empty string) or phases with invalid model specs. The `compare-merge` phase then collects 0 or garbage files.
- SEVERITY: CRITICAL
- REMEDIATION: Validate parsed agent count > 0 after parsing, not just flag presence.

**CRITICAL — Divergence Attack on complexity score boundaries**: I can break this specification by **Divergence Attack**. The invariant at **Wave 1 Step 4 (Complexity Assessment)** fails when **complexity score is exactly 0.7 AND `--strategy` is not explicitly set**.
- Concrete attack: A project with domain_count=3 (+0.3), cross_module_deps=5 (+0.2), estimated_files=20 (+0.2), no security (+0.0) = exactly 0.7. The guard says "If complexity > 0.7 AND `--strategy auto`: auto-upgrade to wave." At 0.7, the `>` check fails — no upgrade. But the scoring factors add exactly to 0.7, which is the documentation's own threshold for "complex." The spec's threshold and scoring formula are misaligned.
- SEVERITY: CRITICAL
- REMEDIATION: Change guard to `>= 0.7` or adjust scoring factors so 0.7 is unambiguously above or below threshold.

**MAJOR — Sequence Attack on Wave 3 delegation ordering**: I can break this specification by **Sequence Attack**. The invariant at **Wave 3 Step 3 (Agent Dispatch)** fails when **the spawn-orchestrator agent is dispatched (tasks > 8) but the orchestrator creates its OWN TaskCreate entries (Responsibility 1) that collide with the skill's TaskCreate entries (Wave 3 Step 1)**.
- Concrete attack: SKILL.md Step 1 creates TaskCreate entries for each task. Then Step 3 dispatches spawn-orchestrator. Orchestrator Responsibility 1 says "Create task entries: One TaskCreate per delegated task." This creates DUPLICATE task entries. The skill already created them; the orchestrator creates them again.
- SEVERITY: MAJOR
- REMEDIATION: Either (a) the skill creates tasks and passes IDs to the orchestrator, or (b) the skill skips Step 1 when delegating to orchestrator (orchestrator owns task creation).

**MAJOR — Sentinel Collision Attack on `${prompt}` interpolation**: I can break this specification by **Sentinel Collision Attack**. The invariant at **Pipeline Execution Step 2 (Expand Dynamic Phases)** fails when **the `--prompt` value contains the literal string `${prompt}`**.
- Concrete attack: `--prompt 'debug the ${prompt} variable handler'`. If `command_template: "${prompt}"` uses naive string replacement, the output becomes `debug the debug the ${prompt} variable handler variable handler` — recursive expansion. Or if not recursive, the literal `${prompt}` in the output is ambiguous.
- SEVERITY: MAJOR
- REMEDIATION: Specify single-pass substitution (no recursive expansion). Document that `${prompt}` in the resolved value is literal text, not a variable reference.

**MAJOR — Accumulation Attack on concurrency cap splitting**: I can break this specification by **Accumulation Attack**. The invariant at **Concurrency Cap** fails when **a topological level contains exactly 10 tasks AND one fails, triggering retry**.
- Concrete attack: Level has 10 tasks. All 10 dispatch. Task 7 fails. Retry policy: "retry once." The retry dispatches task 7 again. Now there are 10 tasks (9 running + 1 retry) — hitting MAX_CONCURRENT. If another task fails during the retry window, it can't retry because the slot is occupied.
- SEVERITY: MAJOR
- REMEDIATION: Clarify that retries happen AFTER the batch completes (not during), or that the retry slot is reserved within the 10-cap (effective dispatch is 9 + 1 retry reserve).

---

### 7. SAM NEWMAN — Service Boundaries & API Evolution

**MAJOR: Return contract is the same for both modes but the data differs**
The return contract has 7 fields. In Pipeline Mode, `task_hierarchy_path` has no hierarchy (no Epics/Stories). In Standard Mode, `pipeline_manifest` is always null. The contract pretends both modes produce the same shape of output.
- RECOMMENDATION: Either (a) define mode-specific return contracts, or (b) add a `mode` field to the return contract and document which fields are null in which mode.
- PRIORITY: Medium — consuming commands/skills need to know which fields are populated

**MINOR: No versioning on the YAML schema**
The pipeline YAML has no `version` field. When `generate-parallel` or new phase types are added in future releases, existing YAML files may break silently.
- RECOMMENDATION: Add `schema_version: 1` to the YAML root. Validate on parse.
- PRIORITY: Low — good practice for future-proofing

---

### 8. GREGOR HOHPE — Integration Patterns & Data Flow

**MAJOR: Artifact routing between phases is file-system-coupled**
Phase outputs go to `<output_dir>/<phase_id>/` and consumers resolve paths by convention. But there's no contract for what a phase writes inside its directory. Is it always `output.md`? Multiple files? A directory?
- RECOMMENDATION: Define artifact naming convention per phase type:
  - `generate` phases: `<phase_id>/output.md`
  - `compare-merge` phases: `<phase_id>/merged-output.md` + `<phase_id>/debate-transcript.md` (from adversarial)
  - Static phases: `<phase_id>/output.md`
  Document this in the delegation-matrix ref.
- PRIORITY: Medium — artifact routing breaks without naming convention

**MINOR: No data flow diagram for BranchNMerge pattern**
The spec has data flow diagrams for Standard Mode and simple Pipeline Mode, but not for the BranchNMerge dynamic expansion pattern. The resolved DAG diagram is helpful but doesn't show the data flow (what goes in/out of each phase).
- RECOMMENDATION: Add a quantity-annotated data flow for BranchNMerge showing: `--prompt` → [3 agents each produce 1 .md] → [adversarial receives 3 .md files] → [1 merged output + 5 artifacts].
- PRIORITY: Low

---

### 9. LISA CRISPIN — Testing Strategy & Acceptance Criteria

**MAJOR: Migration checklist has only 2 manual validation tests**
The spec defines 10 flags, 2 execution modes, 2 dynamic phase types, 7 error scenarios, and 4 strategy options. The migration checklist has exactly 2 test invocations: `--dry-run` and `--pipeline "analyze -> test" --dry-run`.
- RECOMMENDATION: Expand validation matrix:
  - Standard Mode: `--dry-run`, `--no-delegate`, `--depth shallow/deep`, `--strategy wave`
  - Pipeline Mode: inline shorthand, YAML file, `--pipeline-seq`, `--pipeline-resume`
  - BranchNMerge: `--agents` with 2/3/10+ agents, `--agents` with invalid spec
  - Error paths: missing task description, missing `--agents` for generate-parallel, cycle in YAML
  - Resume: checkpoint save + restore across sessions
- PRIORITY: High — insufficient test coverage for a high-complexity command

**MINOR: No acceptance criteria for "success" of a spawn execution**
What does `status: success` vs `status: partial` mean concretely? How many tasks can fail before `partial`? Is one failure enough?
- RECOMMENDATION: Define: `success` = all tasks completed; `partial` = ≥1 task completed + ≥1 failed/manual; `failed` = 0 tasks completed or STOP condition hit.
- PRIORITY: Medium

---

### 10. JANET GREGORY — Quality Practices

**MINOR: Spec was developed iteratively across a brainstorm session but no stakeholder validation checkpoint**
The spec evolved through multiple rounds (brainstorm → requirements → design → pipeline addition → concurrency cap). Each addition built on the last without returning to validate earlier sections.
- RECOMMENDATION: After addressing the panel findings, do a consistency pass: verify all flag references match the flags table, all phase types match the grammar, all error scenarios in the matrix are reachable.
- PRIORITY: Medium

---

### 11. KELSEY HIGHTOWER — Operational Concerns

**MINOR: No observability specification**
For a command that orchestrates 10+ parallel agents, there's no specification for logging, progress reporting, or diagnostic output. The `--dry-run` flag helps but running orchestrations have no visibility.
- RECOMMENDATION: Define progress output format: emit a status line after each parallel group completes showing `[group N/M] completed K/L tasks (F failed)`. This is the orchestrator's primary user feedback mechanism.
- PRIORITY: Medium — essential for user confidence in long-running orchestrations

---

## Guard Condition Boundary Table

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| Task description required | Wave 0 STOP | Zero/Empty | `""`, `null` | true (stops) | "STOP if: No task description provided AND no --pipeline flag" | OK |
| Task description required | Wave 0 STOP | One/Minimal | `"x"` | false (continues) | Proceeds to Wave 0 step 1 | OK |
| Task description required | Wave 0 STOP | Pipeline present | `""` + `--pipeline @f` | false (continues) | Enters Pipeline Mode | OK |
| Task description required | Wave 0 STOP | Both present | `"task"` + `--pipeline @f` | false | Unspecified — which mode wins? | **GAP** |
| Complexity > 0.7 | Wave 1 Step 4 | Zero | 0.0 | false | No upgrade | OK |
| Complexity > 0.7 | Wave 1 Step 4 | At threshold | 0.7 | false | No upgrade (> not >=) | **GAP** |
| Complexity > 0.7 | Wave 1 Step 4 | Above threshold | 0.9 | true | Auto-upgrade to wave | OK |
| Complexity > 0.7 | Wave 1 Step 4 | Maximum/Overflow | 1.0+ | true | Upgrade — but can score exceed 1.0? | **GAP** |
| domain_count > 4 | Wave 1 delegation | Zero/Empty | 0 | false | No planner dispatch | OK |
| domain_count > 4 | Wave 1 delegation | At threshold | 4 | false | No planner dispatch (> not >=) | OK |
| domain_count > 4 | Wave 1 delegation | Typical | 6 | true | Dispatch spawn-planner | OK |
| tasks_created > 8 | Wave 3 delegation | Zero/Empty | 0 | false | Direct dispatch | OK |
| tasks_created > 8 | Wave 3 delegation | At threshold | 8 | false | Direct dispatch | OK |
| tasks_created > 8 | Wave 3 delegation | Above threshold | 9 | true | Dispatch orchestrator | OK |
| tasks_created > 8 | Wave 3 delegation | Overflow | 100 | true | Dispatch orchestrator | OK |
| MAX_CONCURRENT | Concurrency Cap | Zero/Empty | 0 tasks in group | — | Unspecified — empty parallel group | **GAP** |
| MAX_CONCURRENT | Concurrency Cap | One/Minimal | 1 task | dispatch 1 | Implicit — no splitting needed | OK |
| MAX_CONCURRENT | Concurrency Cap | At threshold | 10 tasks | dispatch 10 | No splitting | OK |
| MAX_CONCURRENT | Concurrency Cap | Above threshold | 11 tasks | split: 10+1 | Split into sub-groups | OK |
| MAX_CONCURRENT | Concurrency Cap | Overflow | 100 tasks | split: 10×10 | 10 sub-groups sequentially | OK |
| Agent count for generate-parallel | Pipeline Expand | Zero/Empty | `--agents ""` | — | Unspecified — flag present but empty | **GAP** |
| Agent count for generate-parallel | Pipeline Expand | One/Minimal | 1 agent | expand to 1 phase | 1 phase → compare-merge gets 1 file → STOP (< 2) | OK |
| Agent count for generate-parallel | Pipeline Expand | Typical | 3 agents | expand to 3 phases | 3 parallel phases | OK |
| Agent count for generate-parallel | Pipeline Expand | Overflow | 15 agents | expand to 15 → split | WARN, sub-batch at 10 | OK |
| Collected files for compare-merge | Pipeline Expand | Zero/Empty | 0 files | — | STOP: "Need ≥2 artifacts" | OK |
| Collected files for compare-merge | Pipeline Expand | One/Minimal | 1 file | — | STOP: "Need ≥2 artifacts" | OK |
| Collected files for compare-merge | Pipeline Expand | Typical | 3 files | proceed | Pass to adversarial | OK |
| cross_module_deps > 5 | Wave 2 ref load | Zero/Empty | 0 | false | Don't load dependency-graph.md | OK |
| cross_module_deps > 5 | Wave 2 ref load | At threshold | 5 | false | Don't load (> not >=) | OK |
| cross_module_deps > 5 | Wave 2 ref load | Above threshold | 6 | true | Load dependency-graph.md + Sequential MCP | OK |

---

## Quantity Flow Diagram (Pipeline Dimensional Analysis)

Pipeline Dimensional Analysis triggers: the spec describes a multi-stage data flow (generate-parallel → compare-merge) where output count diverges.

### BranchNMerge Pipeline

```
[CLI: --agents N specs]
        |
        v
[generate-parallel: expand]  -->  N concrete phases (N = len(--agents))
        |
        v
[Parallel Dispatch: N agents] --> N output files (1 per agent)
        |                          N in = N out (no divergence)
        v
[compare-merge: collect-all]  <-- collects N files
        |                         N in → 1 merged + 5 artifacts out
        v                         COUNT DIVERGENCE: N → 6
[Return Contract]             <-- expects: 1 merged_output_path
                                  NOTE: adversarial produces 6 artifacts,
                                  but return contract has 1 pipeline_manifest field
```

**Divergence point**: compare-merge takes N files in, produces 6 artifacts (diff-analysis, debate-transcript, base-selection, refactor-plan, merge-log, merged-output). The return contract's `task_hierarchy_path` field expects a single path. The 5 supplementary artifacts from adversarial are not surfaced in spawn's return contract.

SEVERITY: **MAJOR** — downstream consumers of spawn's return contract cannot access adversarial's supplementary artifacts without knowing the internal directory structure.

RECOMMENDATION: Add `artifacts_dir` field to return contract (path to directory containing all adversarial outputs), or document that `pipeline_manifest` contains the phase output_dir which in turn contains all artifacts.

---

## Synthesis — Priority-Ranked Findings

### CRITICAL (must fix before implementation)

| # | Finding | Expert | Remediation |
|---|---------|--------|-------------|
| C1 | Zero/Empty Attack on `--agents` — flag present but empty string passes guard | Whittaker | Validate parsed agent count > 0 after parsing |
| C2 | Complexity threshold uses `>` 0.7 but scoring formula can produce exactly 0.7 | Whittaker | Change to `>= 0.7` |
| C3 | No output directory (`--output` flag or default) | Wiegers | Add `--output` flag, default to `./spawn-output/` |
| C4 | Sub-agent delegation has no timeout | Nygard | Define per-depth timeouts: shallow=120s, normal=300s, deep=600s |
| C5 | `Skill` missing from SKILL.md allowed-tools | Fowler | Add `Skill` or clarify adversarial is invoked via Task |
| C6 | `type: generate` in expansion output is not a valid phase type | Adzic | Add `generate` to phase type list |

### MAJOR (should fix before implementation)

| # | Finding | Expert | Remediation |
|---|---------|--------|-------------|
| M1 | Both task description and `--pipeline` provided — behavior undefined | Wiegers/Boundary | Define: `--pipeline` takes precedence, task description becomes `--prompt` |
| M2 | Prompt parsing ambiguity (trailing string vs `--prompt` flag) | Wiegers | Define explicit precedence rules |
| M3 | Duplicate TaskCreate between skill Wave 3 and orchestrator | Whittaker | Skill skips task creation when delegating to orchestrator |
| M4 | `${prompt}` recursive expansion risk | Whittaker | Single-pass substitution, document literal `${prompt}` in output |
| M5 | Retry during MAX_CONCURRENT batch conflicts | Whittaker | Retries happen after batch completes |
| M6 | Task-to-Command mapping in wrong ref (loaded Wave 2, consumed Wave 3) | Fowler | Move to delegation-matrix.md |
| M7 | Pipeline step numbering: two step 3s | Fowler | Renumber 1-6 |
| M8 | No artifact naming convention per phase type | Hohpe | Define `output.md` / `merged-output.md` conventions |
| M9 | Return contract same for both modes — misleading null fields | Newman | Add `mode` field, document per-mode population |
| M10 | No worked example showing actual decomposition output | Adzic | Add complete Given/When/Then with hierarchy output |
| M11 | Manifest `skipped` status indistinguishable from `not started` | Nygard | Add `skipped_reason` field |
| M12 | Migration checklist: only 2 tests for 10+ flags | Crispin | Expand to 15+ validation scenarios |
| M13 | Count divergence: adversarial's 6 artifacts not surfaced in return contract | Pipeline Analysis | Add `artifacts_dir` to return contract |
| M14 | Serena checkpoint schema undefined | Nygard | Define key format and data fields |
| M15 | Success/partial/failed criteria undefined | Crispin | Define: success=all, partial=mixed, failed=none |

### MINOR (nice to fix, not blocking)

| # | Finding | Expert | Remediation |
|---|---------|--------|-------------|
| m1 | `--resume` / `--pipeline-resume` redundancy | Wiegers | Merge into single `--resume` |
| m2 | No "When to Use Which Mode" guidance | Cockburn | Add mode selection section |
| m3 | BranchNMerge `source`/`prompt`/`command_template` field confusion | Adzic | Simplify to `source` + `command_template` |
| m4 | No YAML schema version | Newman | Add `schema_version: 1` |
| m5 | dependency-graph.md serves dual purpose | Fowler | Acceptable; flag for split if >200 lines |
| m6 | No progress reporting format for running orchestrations | Hightower | Define status line format |
| m7 | Consistency pass needed after iterative development | Gregory | Post-fix review |
| m8 | Complexity score can theoretically exceed 1.0 (no cap) | Boundary Table | Cap at 1.0 or document additive factors |

---

## Expert Consensus

1. **The core 4-wave architecture is sound.** All experts agree the thin-entry + skill + refs + agents pattern is well-applied and the wave structure provides clear execution phases.

2. **Pipeline Mode is the highest-risk addition.** Dynamic phase expansion (`generate-parallel`), variable interpolation (`${prompt}`), and artifact routing between phases introduce significant complexity that needs tighter specification — particularly around edge cases (empty agents, recursive expansion, naming conventions).

3. **The spec needs an output directory convention and artifact naming standard.** Without these, artifact routing (the backbone of Pipeline Mode) is unresolvable.

4. **Guard conditions use `>` where `>=` would be more appropriate.** The complexity threshold (0.7), domain count (4), and task count (8) all use strict greater-than, creating ambiguous boundary behavior at the exact threshold values.

5. **The error handling matrix is comprehensive for the happy path but thin on operational failures.** Timeouts, checkpoint schemas, retry timing, and partial failure recovery need specification.

---

**Next Step**: Address C1-C6 (critical) and M1-M15 (major) findings, then re-run `/sc:spec-panel --focus correctness` to validate fixes. After that, proceed to `/sc:implement`.
