# C5: Missing `Skill` in SKILL.md allowed-tools — Remediation Proposal

## Problem
Command frontmatter includes `Skill` in allowed-tools but SKILL.md omits it. The `compare-merge` phase needs to invoke `/sc:adversarial`.

## Step-by-Step Solution

### Step 1: Analyze invocation approaches

**Option A — Skill tool (direct skill invocation)**:
- Spawn skill invokes `Skill sc:adversarial-protocol` directly
- Runs in same context, shares tool access
- Pros: simple, efficient, natural skill-to-skill pattern
- Cons: loads adversarial protocol into spawn's context (token cost)

**Option B — Task tool (sub-agent invocation)**:
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
4. **The adversarial command itself is a thin entry that invokes its skill**: The Task agent will load adversarial.md → invoke `Skill sc:adversarial-protocol`. This is the standard flow.

### Step 3: Define exact allowed-tools changes

**spawn.md (command)** — REMOVE `Skill` from allowed-tools:
```
Current:  allowed-tools: Read, Glob, Grep, Bash, TaskCreate, TaskUpdate, TaskList, TaskGet, Task, Write, Skill
Fixed:    allowed-tools: Read, Glob, Grep, Bash, TaskCreate, TaskUpdate, TaskList, TaskGet, Task, Write
```

Why: The spawn command delegates to the skill. The skill does all the work. The command doesn't need `Skill` — it already invokes the skill via the `## Activation` section (which is handled by the framework, not the allowed-tools list).

**SKILL.md** — NO change needed:
```
Current:  allowed-tools: Read, Glob, Grep, Bash, TaskCreate, TaskUpdate, TaskList, TaskGet, Task, Write
Fixed:    (same — no change)
```

Why: The SKILL.md uses `Task` to dispatch sub-agents. Sub-agents have their own tool access. The spawn skill never directly calls `Skill` — it delegates everything through `Task`.

### Step 4: Define compare-merge invocation pattern

In SKILL.md Pipeline Execution, the compare-merge phase dispatch should be:
```
For compare-merge phases:
1. Collect output file paths from all dependency phases
2. Construct adversarial invocation:
   /sc:adversarial --compare <file1>,<file2>,...,<fileN> --depth <depth> --merge
3. Dispatch via Task tool:
   - Agent type: general-purpose (adversarial handles its own agent delegation)
   - Model: opus
   - Prompt: "Execute: /sc:adversarial --compare <files> --depth <depth> --merge
              Output to: <output_dir>/phases/<phase_id>/"
4. The Task agent will:
   - Load adversarial.md command
   - Invoke Skill sc:adversarial-protocol
   - Execute the 5-step adversarial pipeline
   - Write artifacts to the specified output directory
```

### Step 5: Verify consistency with other cross-command patterns

| Command | Invokes | Via | Pattern |
|---------|---------|-----|---------|
| sc:task-unified | quality-engineer agent | Task | Sub-agent dispatch |
| sc:adversarial | debate-orchestrator | Task | Sub-agent dispatch |
| sc:adversarial | merge-executor | Task | Sub-agent dispatch |
| sc:spawn (proposed) | adversarial | Task | Sub-agent dispatch |

All follow the same pattern: parent skill → Task tool → sub-agent.

## Files to Modify
- `spawn.md`: Remove `Skill` from allowed-tools (it's unnecessary)
- `SKILL.md`: No change to allowed-tools (already correct)
- `SKILL.md`: Document compare-merge dispatch pattern using Task tool
