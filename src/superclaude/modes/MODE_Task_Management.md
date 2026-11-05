# Task Management Mode

**Purpose**: Hierarchical task organization with persistent memory for complex multi-step operations

## Activation Triggers

- Operations with >3 steps requiring coordination
- Multiple file/directory scope (>2 directories OR >3 files)
- Complex dependencies requiring phases
- Manual flags: `--task-manage`, `--delegate`
- Quality improvement requests: polish, refine, enhance

## Task Hierarchy with Memory

📋 **Plan** → Write goal_statement to `.superclaude/memory/current_plan.md`
→ 🎯 **Phase** → Write milestone to `.superclaude/memory/phase_X.md`
  → 📦 **Task** → Write deliverable to `.superclaude/memory/task_X.Y.md`
    → ✓ **Todo** → TodoWrite + Write status to `.superclaude/memory/todo_X.Y.Z.md`

## Memory Operations

Memory is plain markdown in `<project>/.superclaude/memory/<key>.md`, with subfolders for topics. `<project>` is the git top-level of the current directory (`git rev-parse --show-toplevel`), or the current directory outside git: one store per worktree. On the first write, if `<project>/.superclaude/.gitignore` is absent, create it with the single line `*`. Single-owner keys (`current_plan`, `last_session`, `next_actions`, and the `phase_*`, `task_*`, `todo_*` keys of the owning session) are overwritten whole; keys parallel sessions may write (`checkpoint`, `decision`, handoffs) are written as `<key>-<session-or-timestamp>.md` and never edited in place. This mode never deletes memory files; deletion is left to the user.

### Session Start

```
1. Glob `.superclaude/memory/**/*.md` → Show existing task state
2. Read `.superclaude/memory/current_plan.md` → Resume context
```

### During Execution

```
1. Write "completed: auth middleware" to `.superclaude/memory/task_2.1.md`
2. Update TodoWrite status in parallel
3. Write current_state to `.superclaude/memory/checkpoint-<timestamp>.md` every 30min
```

### Session End

```
1. Write outcomes to `.superclaude/memory/session_summary-<timestamp>.md`
2. List completed temporary items (checkpoint-*.md) as cleanup candidates for the user to delete
```

## Execution Pattern

1. **Load**: Glob `.superclaude/memory/**/*.md` → Read → Resume state
2. **Plan**: Create hierarchy → Write a memory file for each level
3. **Track**: TodoWrite + memory updates in parallel
4. **Execute**: Update memories as tasks complete
5. **Checkpoint**: Periodic Write of `checkpoint-<timestamp>.md` for state preservation
6. **Complete**: Final memory update with outcomes

## Tool Selection

| Task Type | Primary Tool | Memory Key |
|-----------|-------------|------------|
| Implementation | MultiEdit/Morphllm | "code_changes" |
| UI Components | Magic MCP | "ui_components" |
| Testing | Playwright MCP | "test_results" |
| Documentation | Context7 MCP | "doc_patterns" |

## Memory Schema

```
current_plan: Overall goal statement
phase_[1-5]: Major milestone descriptions
task_[phase].[number]: Specific deliverable status
todo_[task].[number]: Atomic action completion
checkpoint-[timestamp]: Current state snapshot
blockers: Active impediments requiring attention
decision-[timestamp]: Key architectural/design choices made
```

Each key is the file `.superclaude/memory/<key>.md`.

## Examples

### Session 1: Start Authentication Task

```
Glob `.superclaude/memory/**/*.md` → Empty
Write "Implement JWT authentication system" to current_plan.md
Write "Analysis - security requirements review" to phase_1.md
Write "pending: Review existing auth patterns" to task_1.1.md
TodoWrite: Create 5 specific todos
Execute task 1.1 → Write "completed: Found 3 patterns" to task_1.1.md
```

### Session 2: Resume After Interruption

```
Glob `.superclaude/memory/**/*.md` → Shows current_plan.md, phase_1.md, task_1.1.md
Read current_plan.md → "Implement JWT authentication system"
Write "Implementation - middleware and endpoints" to phase_2.md
Continue with implementation tasks...
```

### Session 3: Completion Check

```
Complete remaining testing tasks
Write "Successfully implemented with 95% test coverage" to outcome_auth.md
List checkpoint-*.md files as cleanup candidates → the user deletes them
Write "Auth system complete and validated" to session_summary-<timestamp>.md
```
