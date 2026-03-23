# Major Issue M3 — Eliminate Duplicate `TaskCreate` Entries

## Problem Statement

The current Spawn V2 spec assigns task creation to two different actors in the same execution path:

1. **Wave 3 Step 1 in the skill** creates one `TaskCreate` entry per task.
2. **`spawn-orchestrator` Responsibility 1** also creates one `TaskCreate` entry per delegated task.

When `tasks_created > 8`, the skill first creates tracked tasks and then dispatches `spawn-orchestrator` for Steps 3-5. Because the orchestrator is also instructed to create task entries, the same delegated tasks receive duplicate tracking records.

## Recommended Fix

Assign **all task creation to the skill**, and make the orchestrator operate only on **pre-created task IDs**.

This is the cleaner contract because:

- the skill already owns hierarchy generation and delegation readiness
- `tasks_created` is already defined as a skill-level return value
- the orchestrator is introduced as a scale-management layer for dispatch/monitoring/aggregation, not as a second planner
- this preserves one canonical source of truth for task identity before orchestration begins

## Decision

**Ownership rule**: The `sc:spawn-protocol` skill is the only component allowed to create `TaskCreate` entries for Wave 3 delegated tasks.

**Orchestrator rule**: `spawn-orchestrator` must consume the existing task records created by the skill and must never create duplicate tracking entries for the same hierarchy tasks.

---

## Exact Spec Changes

### 1. Update Wave 3 flow in `spec.md`

File:
`/config/workspace/IronClaude/.dev/releases/backlog/v4.xx-SpawnV2/spec.md`

#### Replace this current block

```markdown
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
```

#### With this revised block

```markdown
1. **Task Creation**: For each Task in the hierarchy, the skill MUST create exactly one tracked task entry:
   - `TaskCreate` with description, status `pending`, dependencies noted
   - Record the returned task ID in the delegation map
   - This skill is the ONLY component that creates TaskCreate entries for Wave 3 hierarchy tasks
2. **Prompt Construction**: For each delegated task, apply prompt
   construction rules (from delegation-matrix ref):
   - Rule 1: Resolve file paths before delegation (Glob/Read)
   - Rule 2: Inject tiered evidence requirements (verification vs discovery)
   - Rule 3: Inject cross-reference counts when available
   - Do NOT override delegated command's output structure
3. **Dispatch Execution**:
   - If `tasks_created <= 8`: the skill dispatches tasks inline via Task tool
   - If `tasks_created > 8`: dispatch `spawn-orchestrator` and pass the pre-created task IDs, hierarchy, DAG ordering, delegation map, and enriched prompts
4. **Progress Tracking**:
   - Inline mode (`tasks_created <= 8`): the skill performs `TaskUpdate`, `TaskList`, and `TaskGet`
   - Orchestrated mode (`tasks_created > 8`): `spawn-orchestrator` performs `TaskUpdate`, `TaskList`, and `TaskGet` against the pre-created task IDs
5. **Result Aggregation**: Collect outputs from all completed tasks.
   Compile summary with per-task status.

**Agent delegation**: If `tasks_created > 8`, dispatch `spawn-orchestrator`
agent to handle steps 3-5 only. Step 1 remains owned by the skill.
```

### 2. Tighten the agent delegation table wording

File:
`/config/workspace/IronClaude/.dev/releases/backlog/v4.xx-SpawnV2/spec.md`

#### Replace this row

```markdown
| `spawn-orchestrator` | Progress tracking and result aggregation | This skill (Wave 3) | When tasks_created > 8 |
```

#### With this row

```markdown
| `spawn-orchestrator` | Dispatch coordination, progress tracking, and result aggregation over pre-created tasks | This skill (Wave 3) | When tasks_created > 8 |
```

This removes any implication that the orchestrator is responsible for creating tracked tasks.

### 3. Update the orchestrator tools section to remove task creation authority

File:
`/config/workspace/IronClaude/.dev/releases/backlog/v4.xx-SpawnV2/spec.md`

#### Replace this current tools block line

```markdown
- **TaskCreate**: Create tracked tasks for each delegation
```

#### With this line

```markdown
- **TaskCreate**: Not used for Wave 3 hierarchy tasks; task records are pre-created by the skill
```

If you want the cleanest possible spec, an even stronger option is to remove `TaskCreate` from the orchestrator tools list entirely. But if you want to preserve flexibility for future non-hierarchy bookkeeping, the explicit prohibition above is safer and more precise.

### 4. Rewrite orchestrator Responsibility 1

File:
`/config/workspace/IronClaude/.dev/releases/backlog/v4.xx-SpawnV2/spec.md`

#### Replace this current responsibility block

```markdown
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
```

#### With this revised responsibility block

```markdown
1. **Consume existing task entries**: Use the pre-created task IDs supplied by the skill as the canonical tracking records for all delegated hierarchy tasks; do NOT create duplicate TaskCreate entries
2. **Dispatch parallel groups**: Launch concurrent Task agents for each
   parallel group, respecting DAG ordering between groups
3. **Monitor completion**: Poll TaskList/TaskGet for status updates on the pre-created task IDs
4. **Handle failures**: Retry failed tasks once, then mark as `manual`
   and continue with remaining tasks
5. **Aggregate results**: Collect outputs from all completed tasks,
   compile summary with per-task status and artifact paths
6. **Produce orchestration report**: Write hierarchy document with final
   status, delegation map, and completion summary
```

### 5. Add an explicit invariant sentence near Wave 3

File:
`/config/workspace/IronClaude/.dev/releases/backlog/v4.xx-SpawnV2/spec.md`

Add this sentence immediately after the Wave 3 delegation rule:

```markdown
**Invariant**: Each hierarchy task maps to exactly one `TaskCreate` entry, created by the skill before any inline or orchestrated dispatch begins.
```

This turns the anti-duplication requirement into a testable contract instead of an implied convention.

---

## Why This Option Is Better Than Making the Orchestrator Own Task Creation

The alternative fix would be: skip Wave 3 Step 1 when `tasks_created > 8`, and let the orchestrator create all task records. That is workable, but weaker.

Reasons to prefer skill-owned task creation:

1. **Stable identity before branching**
   - The skill creates the hierarchy and knows the final task set.
   - Creating task IDs at that point gives a stable record before execution mode splits into inline vs orchestrated.

2. **Single return-contract meaning for `tasks_created`**
   - `tasks_created` continues to mean tasks actually created by the skill.
   - No delayed or mode-dependent semantics.

3. **Cleaner separation of concerns**
   - Skill: decompose, define, create, hand off.
   - Orchestrator: dispatch, monitor, aggregate.

4. **Lower ambiguity for tests and future maintenance**
   - There is one creation site to validate.
   - Duplicate-entry regressions become easy to detect.

---

## Suggested Acceptance Criteria

Add these acceptance criteria to the remediation decision or test plan:

1. When `tasks_created <= 8`, the skill creates exactly one `TaskCreate` entry per hierarchy task and dispatches inline.
2. When `tasks_created > 8`, the skill still creates exactly one `TaskCreate` entry per hierarchy task before dispatching `spawn-orchestrator`.
3. In orchestrated mode, `spawn-orchestrator` does not call `TaskCreate` for any hierarchy task already represented in the delegation map.
4. Across both modes, every hierarchy task corresponds to exactly one tracked task entry.
5. The final orchestration summary reports status against the original task IDs created by the skill.

---

## Final Recommended Wording

If you want the shortest possible governing rule to reuse across the spec, use this exact sentence:

```markdown
Task creation is owned exclusively by the `sc:spawn-protocol` skill; `spawn-orchestrator` may dispatch, monitor, update, and aggregate pre-created tasks, but must not create duplicate `TaskCreate` entries for hierarchy tasks.
```

That sentence captures the entire fix in one normative contract.
