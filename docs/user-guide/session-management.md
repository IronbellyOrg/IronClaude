# Session Management Guide

SuperClaude keeps project memory (decisions, patterns, and notes) across Claude Code conversations through the Serena MCP server. Project memory is not a way to resume work: to pick up a task, a plan, or a lost conversation, see [Resuming Existing Work](#resuming-existing-work-cross-conversation) below.

## Core Session Commands with Persistent Memory

### `/sc:load` - Context Loading with Persistent Memory

**Purpose**: Initialize session with project context and persistent memory from previous sessions  
**MCP Integration**: Triggers Serena MCP to read stored project memories  
**Syntax**: `/sc:load [project_path]`

**What Happens**:

- Serena MCP reads persistent memory files from previous sessions
- Project context is restored from stored memories
- Previous decisions and patterns are loaded as notes (task and plan progress is not; see [Resuming Existing Work](#resuming-existing-work-cross-conversation))

**Use Cases**:

```bash
# Load existing project context from persistent memory
/sc:load src/

# Load stored memory about a specific project (this does not resume a task or a plan)
/sc:load "authentication-system"

# Initialize with codebase analysis and previous insights
/sc:load . --analyze
```

### `/sc:save` - Session Persistence to Memory

**Purpose**: Save current session state and decisions to persistent memory  
**MCP Integration**: Triggers Serena MCP to write memory files  
**Syntax**: `/sc:save [--type session|learnings|context|all] [--summarize] [--checkpoint]`

The command takes no description argument. It decides what to record from the current conversation; say in the conversation what you want remembered before you run it.

**What Happens**:

- Current context and decisions are written to Serena memory
- Project notes are kept across conversations
- Key insights and patterns are stored for future sessions
- Session summary is created with timestamp for retrieval

**Use Cases**:

```bash
# Save what this session discovered
/sc:save

# Checkpoint during complex work (everything, plus a recovery checkpoint)
/sc:save --type all --checkpoint

# Store only new patterns and decisions
/sc:save --type learnings

# Write a session summary
/sc:save --summarize
```

## Persistent Memory Architecture

### How Serena MCP Enables True Persistence

**Memory Storage**:

- Session contexts stored as structured memory files
- Project decisions and architectural patterns preserved permanently
- Code analysis results and insights retained across conversations
- Progress tracking and milestone data maintained long-term

**Cross-Session Continuity**:

- Stored project memory available in new conversations after `/sc:load` (task and plan progress lives in the work's own files, not in memory)
- Decisions and rationale preserved and accessible across conversations
- Learning from past patterns and solutions maintained
- Consistent project understanding maintained indefinitely

**Memory Types**:

- **Project Memories**: Long-term project context and architecture
- **Session Memories**: Specific conversation outcomes and decisions  
- **Pattern Memories**: Reusable solutions and architectural patterns
- **Progress Memories**: Milestone tracking and completion status

## Session Lifecycle Patterns with Persistence

### New Project Initialization

```bash
# 1. Start fresh project
/sc:brainstorm "e-commerce platform requirements"

# 2. Save initial decisions to persistent memory
/sc:save --type learnings

# 3. Begin implementation planning
/sc:workflow "user authentication system" --depth quick

# 4. Save architectural decisions permanently
/sc:save --type learnings
```

### Resuming Existing Work (Cross-Conversation)

To pick up work in a new conversation, use section 3.12 ("Resume after a crash or a lost session") of the routing guide, [`HOW-WE-WORK.md`](../../src/superclaude/core/HOW-WE-WORK.md#312-resume-after-a-crash-or-a-lost-session), which `superclaude install` copies to `~/.claude/HOW-WE-WORK.md`. It gives two ways:

1. **Reopen the conversation.** This only works if you tagged the conversation before you lost it: inside Claude, run `/ccsession-tag <name>`. Later, from a terminal in any worktree or copy of the same repo (outside git, the same folder), run `ccsession <name>`. `ccsession --here` lists the names for this repo. `~/.local/bin` must be on your `PATH`.
2. **Rerun the same command on the work's own files.** This always works: `/task <path to the task file>` for a task file, or `/sc:implement .dev/tasks/to-do/<id>/<id>.md` for a plan.

`/sc:load` restores Serena project memory, which helps Claude remember project decisions, but it does not resume a task or a plan.

### Long-Term Project Management

```bash
# Weekly checkpoint pattern with persistence
/sc:load project-name
# ... work on features ...
/sc:save --summarize

# Phase completion pattern with memory
/sc:save --type all --checkpoint
/task-builder "Phase 2: payment and order processing"   # larger work goes through a task file (see How We Work)
```

## Per-Turn Session Context Envelope (v4.3+)

In addition to the long-term Serena memory layer described above, every user
prompt is prefixed with a **short, factual `<session-context>` block** injected
by the `freshness-user-prompt.sh` hook. This is per-turn ephemeral state, not
persistent memory.

```
<session-context>
  ts=2026-05-13T01:07:33+00:00 turn=2 Δ=07:43 mode=plan git=feat/x dirty=3M/4U bg=2
  changed_since_last_turn=/foo/a.go,/foo/b.go
</session-context>
```

Fields appear conditionally:

- `turn=N` — per-session turn counter (always present)
- `Δ=MM:SS` — elapsed since previous prompt, when ≥300s
- `mode=<m>` — when `permission_mode ≠ "default"`
- `git=<branch> dirty=NM/NU` — when the cwd has uncommitted changes
- `bg=<n>` — when subagents are running
- `RESUMED_AFTER_LONG_PAUSE` — when Δ ≥ 3600s

**Treat the envelope as ground truth for the turn.** Decisions based on
older context (cached memory of file contents, prior tool-call results) may be
stale; the envelope reflects what was true the instant the user pressed Enter.

The companion `freshness-pre-edit.sh` hook blocks `Edit`/`Write` against
files not Read in this session within the last 30 minutes — see
[Context Freshness Hooks](freshness-hooks.md) for the full story.

## Cross-Conversation Continuity

### Starting New Conversations with Persistence

When starting a new Claude Code conversation, Serena project memory allows:

1. **Loading project memory**

   ```bash
   /sc:load src/
   # Loads stored Serena project memory (decisions and notes); it does not resume a task or a plan
   ```

2. **Earlier decisions at hand**
   - Previous session decisions are available as notes
   - Architectural patterns and code insights are preserved
   - Project history and rationale are maintained
   - To continue unfinished work, use [Resuming Existing Work](#resuming-existing-work-cross-conversation) instead

3. **Intelligent Context Building**
   - Serena MCP provides relevant memories based on current work
   - Past solutions and patterns inform new implementations
   - Project evolution is tracked and understood

### Memory Optimization

**Effective Memory Usage**:

- Use descriptive, searchable memory names
- Include project phase and timestamp context
- Reference specific features or architectural decisions
- Make future retrieval intuitive

**Memory Content Strategy**:

- Store decisions and rationale, not just outcomes
- Include alternative approaches considered
- Document integration patterns and dependencies
- Preserve learning and insights for future reference

**Memory Lifecycle Management**:

- Regular cleanup of outdated memories
- Consolidation of related session memories
- Archiving of completed project phases
- Pruning of obsolete architectural decisions

## Best Practices for Persistent Sessions

### Session Start Protocol

1. To continue unfinished work, follow [Resuming Existing Work](#resuming-existing-work-cross-conversation); use `/sc:load` only to load project memory
2. Plan work based on stored decisions and patterns
3. Build on previous decisions and architectural choices

### Session End Protocol

1. Save key decisions with `/sc:save` as Serena project memory
2. Document next steps and open questions in memory
3. Keep unfinished work in its own files (a task file or a plan) so it can be resumed; project memory does not resume it

### Memory Quality Maintenance

- Use clear, descriptive memory names for easy retrieval
- Include context about decisions and alternative approaches
- Reference specific code locations and patterns
- Maintain consistency in memory structure across sessions

## Integration with Other SuperClaude Features

### MCP Server Coordination

- **Serena MCP**: Provides the persistent memory infrastructure
- **Context7 MCP**: References stored patterns and documentation approaches
- **Morphllm MCP**: Applies stored refactoring patterns consistently

### Agent Collaboration with Memory

- Agents access persistent memories for enhanced context
- Previous specialist decisions are preserved and referenced
- Cross-session agent coordination through shared memory
- Consistent specialist recommendations based on project history

### Command Integration with Persistence

- All `/sc:` commands can reference and build on persistent context
- Previous command outputs and decisions are available across sessions
- Workflow patterns are stored and reusable
- Implementation history guides future command decisions

## Troubleshooting Persistent Sessions

### Common Issues

**Memory Not Loading**:

- Verify Serena MCP is configured and running properly
- Check memory file permissions and accessibility
- Ensure consistent project naming conventions
- Validate memory file integrity and format

**Context Loss Between Sessions**:  

- To resume a task, a plan, or a lost conversation, follow [Resuming Existing Work](#resuming-existing-work-cross-conversation); `/sc:save` and `/sc:load` only keep project memory
- Use `/sc:save` before ending sessions to keep decisions as project memory
- Backup important memory files periodically

**Memory Conflicts**:

- Use timestamped memory names for version control
- Regular cleanup of obsolete memories
- Clear separation between project and session memories
- Consistent memory naming conventions across sessions

## Advanced Persistent Session Patterns

### Multi-Phase Projects

- Use phase-specific memory naming for organization
- Maintain architectural decision continuity across phases
- Cross-phase dependency tracking through persistent memory
- Progressive complexity management with historical context

### Team Collaboration

- Shared memory conventions and naming standards
- Decision rationale preservation for team context
- Integration pattern documentation accessible to all team members
- Consistent code style and architecture enforcement through memory

### Long-Term Maintenance

- Memory archiving strategies for completed projects
- Pattern library development through accumulated memories
- Reusable solution documentation built over time
- Knowledge base building through persistent memory accumulation

## Key Benefits of Persistent Session Management

### Project Continuity

- Project decisions and notes available across conversations
- Preserved architectural decisions and technical rationale
- Long-term project evolution tracking

### Enhanced Productivity

- Reduced need to re-explain project context
- Faster startup time for continued work
- Building on previous insights and patterns
- Cumulative project knowledge growth

### Quality Consistency

- Consistent architectural patterns across sessions
- Preserved code quality decisions and standards
- Reusable solutions and best practices
- Maintained technical debt awareness

---

**Key Takeaway**: Session management through Serena MCP keeps project decisions and learning across Claude Code conversations. It does not resume work; for that, see [Resuming Existing Work](#resuming-existing-work-cross-conversation).
