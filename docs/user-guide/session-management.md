# Session Management Guide

SuperClaude keeps project memory (decisions, patterns, and notes) across Claude Code conversations as plain markdown files under `<project>/.superclaude/memory/`. `<project>` is the git top-level of the current directory (the current directory outside git), so each worktree has its own store. The first write creates `<project>/.superclaude/.gitignore` containing `*`, so the files stay out of version control. Project memory is not a way to resume work: to pick up a task, a plan, or a lost conversation, see [Resuming Existing Work](#resuming-existing-work-cross-conversation) below.

## Who Reads and Writes Project Memory

The PM agent and the `sc:pm-protocol` skill, which `/sc:pm` loads, read and write the memory files. Nothing else reads them for you at the start of a conversation, and no command is dedicated to saving or loading them.

- **At the start**, the PM agent lists `.superclaude/memory/**/*.md` and reads `pm_context.md`, `current_plan.md`, `last_session.md` and `next_actions.md`.
- **During work**, it writes the goal to `current_plan.md` and progress to `checkpoint-<timestamp>.md`.
- **At the end**, it writes `last_session.md`, `next_actions.md` and `pm_context.md`.
- Some skills (`/sc:task`, `/sc:reflect`, `/sc:validate-roadmap`) keep their own subfolders in the same store. The developer note [File-Based Session Memory](../developer-guide/session-memory.md) lists every writer.

You can also read, edit or delete the files by hand: they are plain markdown.

### Upgrading from Serena memory (5.0.0)

Before 5.0.0, memories were kept through Serena in `<project>/.serena/memories/`. 5.0.0 removed Serena and keeps memory in `<project>/.superclaude/memory/`. 6.0.0 removed the memory save and load commands and the read-only fallback to `.serena/memories/`, so nothing reads the old folder any more. To keep your old memories, copy them across from the project root:

```bash
mkdir -p .superclaude/memory
cp -Rn .serena/memories/. .superclaude/memory/
[ -e .superclaude/.gitignore ] || printf '*\n' > .superclaude/.gitignore
```

The last line adds the `.gitignore` that the PM agent creates on its first write, so the copied files stay out of version control.

## Persistent Memory Architecture

### How Memory Files Enable Persistence

**Memory Storage**:

- Session contexts stored as markdown memory files, one per key, in `<project>/.superclaude/memory/` (subfolders for topics)
- Project decisions and architectural patterns preserved permanently
- Code analysis results and insights retained across conversations
- Progress tracking and milestone data maintained long-term

**Cross-Session Continuity**:

- Stored project memory available in new conversations once the PM agent reads it (task and plan progress lives in the work's own files, not in memory)
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

# 2. Begin implementation planning
/sc:workflow "user authentication system" --depth quick

# 3. Ask the PM agent to record the architectural decisions in project memory
/sc:pm
```

### Resuming Existing Work (Cross-Conversation)

To pick up work in a new conversation, use section 3.12 ("Resume after a crash or a lost session") of the routing guide, [`HOW-WE-WORK.md`](../../src/superclaude/core/HOW-WE-WORK.md#312-resume-after-a-crash-or-a-lost-session), which `superclaude install` copies to `~/.claude/HOW-WE-WORK.md`. It gives two ways:

1. **Reopen the conversation.** This only works if the conversation had a name before you lost it: start it with `ccsession <name>`, or inside Claude Code run `/rename <name>` and send one more message (or quit) so ccsession records it. Later, from a terminal in any worktree or copy of the same repo (outside git, the same folder), run `ccsession <name>` (quote a name with spaces). `ccsession --here` lists the names for this worktree (and for removed ones); `ccsession --here --all` lists every worktree's. `~/.local/bin` must be on your `PATH`.
2. **Rerun the same command on the work's own files.** This always works: `/task <path to the task file>` for a task file, or `/sc:implement .dev/tasks/to-do/<id>/<id>.md` for a plan.

Project memory in the `.superclaude/memory/` files helps Claude remember project decisions, but it does not resume a task or a plan.

### Long-Term Project Management

```bash
# Phase completion pattern
/sc:workflow "Phase 2: payment and order processing" --depth standard --handoff none
# then run the plan it prints: /sc:implement <printed plan path>
```

## Per-Turn Session Context Envelope

In addition to the long-term memory files described above, every user
prompt is prefixed with a **short, factual `<session-context>` block** injected
by the `freshness-user-prompt.sh` hook. This is per-turn ephemeral state, not
persistent memory.

```text
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

When starting a new Claude Code conversation, the project memory files allow:

1. **Reading project memory**

   ```bash
   /sc:pm
   # The PM agent reads the stored project memory (decisions and notes); it does not resume a task or a plan
   ```

2. **Earlier decisions at hand**
   - Previous session decisions are available as notes
   - Architectural patterns and code insights are preserved
   - Project history and rationale are maintained
   - To continue unfinished work, use [Resuming Existing Work](#resuming-existing-work-cross-conversation) instead

3. **Intelligent Context Building**
   - The PM agent reads the memories relevant to current work
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

1. To continue unfinished work, follow [Resuming Existing Work](#resuming-existing-work-cross-conversation); project memory does not resume it
2. Plan work based on stored decisions and patterns
3. Build on previous decisions and architectural choices

### Session End Protocol

1. Have the PM agent record key decisions as project memory
2. Document next steps and open questions in memory
3. Keep unfinished work in its own files (a task file or a plan) so it can be resumed; project memory does not resume it

### Memory Quality Maintenance

- Use clear, descriptive memory names for easy retrieval
- Include context about decisions and alternative approaches
- Reference specific code locations and patterns
- Maintain consistency in memory structure across sessions

## Integration with Other SuperClaude Features

### MCP Server Coordination

- **Context7 MCP**: References stored patterns and documentation approaches

Memory is plain markdown files that Claude reads and writes with its file tools; no MCP server stores or applies memories.

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

- Check that `<project>/.superclaude/memory/` exists for the project you are in (one store per worktree)
- Check memory file permissions and accessibility
- Ensure consistent memory key naming
- Validate memory file integrity and format

**Context Loss Between Sessions**:  

- To resume a task, a plan, or a lost conversation, follow [Resuming Existing Work](#resuming-existing-work-cross-conversation); project memory does not resume work
- Have the PM agent record decisions as project memory before ending sessions
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

**Key Takeaway**: Session management through the `.superclaude/memory/` files keeps project decisions and learning across Claude Code conversations. It does not resume work; for that, see [Resuming Existing Work](#resuming-existing-work-cross-conversation).
