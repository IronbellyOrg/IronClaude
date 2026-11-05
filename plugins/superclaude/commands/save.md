---
name: save
description: "Session lifecycle management with memory files for session context persistence"
category: session
complexity: standard
mcp-servers: []
personas: []
---

# /sc:save - Session Context Persistence

## Triggers

- Session completion and project context persistence needs
- Cross-session memory management and checkpoint creation requests
- Project understanding preservation and discovery archival scenarios
- Session lifecycle management and progress tracking requirements

## Usage

```
/sc:save [--type session|learnings|context|all] [--summarize] [--checkpoint]
```

## Behavioral Flow

1. **Analyze**: Examine session progress and identify discoveries worth preserving
2. **Persist**: Save session context and learnings as markdown memory files under `.superclaude/memory/`
3. **Checkpoint**: Create recovery points for complex sessions and progress tracking
4. **Validate**: Ensure session data integrity and cross-session compatibility
5. **Prepare**: Ready session context for seamless continuation in future sessions

Key behaviors:

- Markdown memory files under `.superclaude/memory/` for cross-session persistence
- Automatic checkpoint creation based on session progress and critical tasks
- Session context preservation with comprehensive discovery and pattern archival
- Cross-session learning with accumulated project insights and technical decisions

## Memory Store

- **Location**: `<project>/.superclaude/memory/<key>.md`, flat markdown with subfolders for topics. `<project>` is the git top-level of the current directory (`git rev-parse --show-toplevel`), or the current directory outside git: one store per worktree
- **First write**: if `<project>/.superclaude/.gitignore` is absent, create it with the single line `*`
- **Single-owner keys** (`pm_context`, `last_session`, `next_actions`): overwritten whole on each save
- **Keys parallel sessions may write** (`checkpoint`, `decision`, handoffs): written as `<key>-<session-or-timestamp>.md` and never edited in place
- **Performance Critical**: <200ms for memory operations, <1s for checkpoint creation

## Tool Coordination

- **Write/Read**: Core session context persistence and retrieval of `.superclaude/memory/` files
- **Glob** `.superclaude/memory/**/*.md`: Listing existing memories before a save
- **Session analysis and summary**: Done in the session itself; the discovery analysis and summary are written into the memory files
- **TodoRead**: Task completion tracking for automatic checkpoint triggers

## Key Patterns

- **Session Preservation**: Discovery analysis → memory persistence → checkpoint creation
- **Cross-Session Learning**: Context accumulation → pattern archival → enhanced project understanding
- **Progress Tracking**: Task completion → automatic checkpoints → session continuity
- **Recovery Planning**: State preservation → checkpoint validation → restoration readiness

## Examples

### Basic Session Save

```
/sc:save
# Saves current session discoveries and context to .superclaude/memory/
# Automatically creates checkpoint if session exceeds 30 minutes
```

### Comprehensive Session Checkpoint

```
/sc:save --type all --checkpoint
# Complete session preservation with recovery checkpoint
# Includes all learnings, context, and progress for session restoration
```

### Session Summary Generation

```
/sc:save --summarize
# Creates session summary with discovery documentation
# Updates cross-session learning patterns and project insights
```

### Discovery-Only Persistence

```
/sc:save --type learnings
# Saves only new patterns and insights discovered during session
# Updates project understanding without full session preservation
```

## Boundaries

**Will:**

- Save session context as markdown files under `.superclaude/memory/` for cross-session persistence
- Create automatic checkpoints based on session progress and task completion
- Preserve discoveries and patterns for enhanced project understanding

**Will Not:**

- Operate without write access to the `.superclaude/memory/` store
- Save session data without validation and integrity verification
- Override existing session context without proper checkpoint preservation
