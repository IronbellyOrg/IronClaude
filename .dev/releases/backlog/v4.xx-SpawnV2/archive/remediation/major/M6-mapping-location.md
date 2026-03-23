# Major Issue M6 Remediation Proposal

## Issue

`refs/decomposition-patterns.md` currently mixes two concerns:
1. Wave 2 decomposition structure and granularity rules
2. Wave 3 task-to-command delegation rules

This violates the SpawnV2 lazy-loading principle because Wave 2 loads delegation information it does not need. The task-to-command mapping is only consumed when preparing delegation behavior in Wave 3.

## Goal

Move the Task-to-Command Mapping Rules out of `refs/decomposition-patterns.md` and into `refs/delegation-matrix.md`, so that:
- Wave 2 loads only decomposition and DAG-shaping guidance
- Wave 3 loads delegation-target selection and prompt-construction guidance together
- each ref cleanly owns one concern

## Proposed Design

### Responsibility split after remediation

#### `refs/decomposition-patterns.md`
Owns only:
- Epic construction rules
- Story granularity by depth
- decomposition-time task shaping rules
- DAG edge rules and parallel grouping constraints

#### `refs/delegation-matrix.md`
Owns only:
- command selection for delegated tasks
- persona and MCP hints by command
- agent selection by delegated command
- prompt construction and dispatch-time enrichment rules

This aligns with the current wave model:
- Wave 2 = decide what tasks exist and how they relate
- Wave 3 = decide how each task is delegated

## Exact Content Changes

---

## 1. Changes to `refs/decomposition-patterns.md`

### A. Remove the entire `## Task-to-Command Mapping Rules` section

Delete this block in full:

```markdown
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
```

### B. Replace it with a decomposition-only task-shaping section

Insert this section in the same location, between `## Story Granularity by Depth` and `## DAG Edge Rules`:

```markdown
## Task Shaping Rules

Wave 2 defines the task hierarchy and dependency structure only.
It does NOT choose the final delegated `/sc:*` command. Command selection
is a Wave 3 concern and lives in `refs/delegation-matrix.md`.

Each Task produced by decomposition MUST include:
- `task_description`: clear unit of work
- `task_type`: normalized category for later delegation
- `target_artifact`: what output the task is expected to produce
- `complexity_hint`: low | medium | high
- `domain`: owning Epic/domain

### Normalized Task Types
Use one of these task types during decomposition:
- `schema_design`
- `api_design`
- `architecture_design`
- `implementation`
- `bug_fix`
- `test_creation`
- `documentation`
- `code_cleanup`
- `security_hardening`
- `infrastructure`
- `research`

These normalized task types are the handoff contract into Wave 3.
Wave 3 resolves them into concrete commands using `refs/delegation-matrix.md`.
```

### C. Keep `## DAG Edge Rules` unchanged

No content move is needed for DAG rules. They are valid Wave 2 logic because they shape dependency structure before delegation.

### D. Expected final structure of `refs/decomposition-patterns.md`

After the change, the file should read structurally like this:

```markdown
# Decomposition Patterns Reference

## Epic Construction Rules
...

## Story Granularity by Depth
...

## Task Shaping Rules
...

## DAG Edge Rules
...
```

### Why this is the right replacement

Wave 2 still needs a way to produce consistent task records. Removing the mapping section entirely without replacement would leave decomposition underspecified. The replacement preserves a clean handoff contract by requiring normalized `task_type` values, while deferring actual command choice until Wave 3.

---

## 2. Changes to `refs/delegation-matrix.md`

### A. Add a new section before `## Agent Selection for Task Dispatch`

Insert this new section immediately after the existing command target tables and before `## Agent Selection for Task Dispatch`:

```markdown
## Task-to-Command Mapping Rules

Wave 3 resolves each decomposed Task into exactly ONE delegated `/sc:*`
command. The input to this mapping is the normalized `task_type` produced
by Wave 2 decomposition.

| Task Type | Primary Command | Fallback |
|-----------|----------------|----------|
| `schema_design` | `/sc:design --type database` | `/sc:design --type component` |
| `api_design` | `/sc:design --type api` | `/sc:design --type architecture` |
| `architecture_design` | `/sc:design --type architecture` | — |
| `implementation` | `/sc:implement` | `/sc:build` |
| `bug_fix` | `/sc:task "fix ..."` | `/sc:troubleshoot` |
| `test_creation` | `/sc:test` | `/sc:task "test ..."` |
| `documentation` | `/sc:document` | — |
| `code_cleanup` | `/sc:cleanup` | `/sc:improve` |
| `security_hardening` | `/sc:task --force-strict` | `/sc:analyze --focus security` |
| `infrastructure` | `/sc:task` with devops persona | `/sc:implement` |
| `research` | `/sc:research` | `/sc:analyze` |

### Resolution Rules
1. Use the Task's normalized `task_type` from Wave 2 as the primary selector.
2. Choose the Primary Command unless the task context clearly requires the fallback.
3. Preserve exactly one delegated command per Task.
4. Do not re-decompose the Task during delegation.
5. If no mapping fits, STOP and report an unmapped `task_type` instead of guessing.
```

### B. Add a bridging note tying command tables to task mapping

Immediately after the existing `## Command Delegation Targets` tables, add this short note if it is not already implicit enough:

```markdown
These command tables describe when each command is appropriate.
The formal Wave 3 selection step is defined in `## Task-to-Command Mapping Rules` below.
```

### C. Expected final structure of `refs/delegation-matrix.md`

After the change, the file should read structurally like this:

```markdown
# Delegation Matrix Reference

## Command Delegation Targets
...

## Task-to-Command Mapping Rules
...

## Agent Selection for Task Dispatch
...

## Prompt Construction Rules
...
```

This keeps all dispatch-time concerns together in one ref.

---

## 3. Required SKILL.md / spec wording updates

The ref move is not fully complete unless the wave instructions are also clarified.

### A. Update Wave 2 wording

Current Wave 2 wording says:

```markdown
3. **Task Assignment**: Each Story becomes one or more Tasks. Each Task
   maps to exactly one `/sc:*` command for delegation.
```

Replace with:

```markdown
3. **Task Assignment**: Each Story becomes one or more Tasks. Each Task
   must include a normalized `task_type` for later command resolution in
   Wave 3 delegation.
```

### B. Update Wave 3 wording

Current Wave 3 already loads `refs/delegation-matrix.md`, but it should explicitly mention command resolution.

Insert this step before Prompt Construction, or merge it into Task Creation:

```markdown
2. **Command Resolution**: For each Task, resolve the normalized
   `task_type` into exactly one delegated `/sc:*` command using the
   task-to-command mapping rules in `refs/delegation-matrix.md`.
```

Then renumber subsequent steps accordingly.

### Why these wording changes matter

Without this wording update, the refs would be corrected but the wave protocol would still describe command selection as a Wave 2 action. That would preserve a conceptual contradiction even after the file move.

---

## 4. Resulting behavior after remediation

### Wave 2 loads only what it needs
Wave 2 uses:
- `refs/decomposition-patterns.md`
- `refs/dependency-graph.md` when needed

Wave 2 outputs:
- Epics
- Stories
- Tasks with normalized `task_type`
- DAG edges
- parallel groups

### Wave 3 loads only what it needs
Wave 3 uses:
- `refs/delegation-matrix.md`

Wave 3 resolves:
- task_type -> delegated command
- persona/MCP hints
- agent type/model hint
- prompt enrichment rules

This cleanly restores lazy-loading alignment.

---

## 5. Benefits

### Fixes the lazy-loading violation
Delegation logic is no longer preloaded during decomposition.

### Improves separation of concerns
- decomposition ref = task structure
- delegation ref = dispatch behavior

### Creates a stronger handoff contract
Normalized `task_type` values make the Wave 2 -> Wave 3 boundary explicit and testable.

### Reduces future drift
If command routing evolves, only `refs/delegation-matrix.md` needs updating.

---

## 6. Risks and mitigation

### Risk 1: Wave 2 becomes too vague after removal
Mitigation: replace the removed mapping with normalized task shaping rules, not a pure deletion.

### Risk 2: Duplicate command-selection logic persists elsewhere
Mitigation: update the wave wording so only Wave 3 is described as resolving commands.

### Risk 3: Task types and mapping table diverge over time
Mitigation: require exact task_type vocabulary in both files and treat unmapped values as STOP conditions.

---

## 7. Acceptance criteria

This remediation is complete when all of the following are true:

- `refs/decomposition-patterns.md` no longer contains a task-to-command mapping table
- `refs/decomposition-patterns.md` contains decomposition-only task shaping rules with normalized `task_type`
- `refs/delegation-matrix.md` contains the task-to-command mapping table
- Wave 2 wording no longer says it selects `/sc:*` commands
- Wave 3 wording explicitly says it resolves `task_type` into one delegated command
- no delegation-target-selection logic remains in Wave 2-only refs

---

## Recommended final verdict

Adopt the move exactly as above.

This is the smallest correct fix because it:
- removes the lazy-loading violation,
- preserves decomposition completeness,
- avoids inventing a new ref,
- and strengthens the Wave 2/Wave 3 contract instead of merely relocating text.
