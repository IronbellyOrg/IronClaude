---
name: load
description: "Session lifecycle management with memory files for project context loading"
category: session
complexity: standard
mcp-servers: []
personas: []
---

# /sc:load - Project Context Loading

## Triggers

- Session initialization and project context loading requests
- Cross-session persistence and memory retrieval needs
- Project context and memory management requirements
- Session lifecycle management and checkpoint loading scenarios

## Usage

```
/sc:load [target] [--type project|config|deps|checkpoint] [--refresh] [--analyze]
```

## Behavioral Flow

1. **Initialize**: Resolve the project root and locate the `.superclaude/memory/` store
2. **Discover**: Analyze project structure and identify context loading requirements
3. **Load**: Retrieve project memories, checkpoints, and cross-session persistence data from the memory files
4. **Establish**: Establish project context and prepare for development workflow
5. **Validate**: Ensure loaded context integrity and session readiness

Key behaviors:

- Markdown memory files under `.superclaude/memory/` for cross-session persistence
- Project context loading with comprehensive validation
- Performance-critical operation with <500ms initialization target
- Session lifecycle management with checkpoint and memory coordination

## Memory Store

- **Location**: `<project>/.superclaude/memory/<key>.md`, flat markdown with subfolders for topics. `<project>` is the git top-level of the current directory (`git rev-parse --show-toplevel`), or the current directory outside git: one store per worktree
- **Legacy fallback**: For one release, `/sc:load` reads `.serena/memories/<key>.md` only when `.superclaude/memory/<key>.md` is absent, never writes there, and tells the user that folder is read-only history
- **Memory Operations**: Cross-session persistence, checkpoint loading, and context restoration
- **Performance Critical**: <200ms for core operations, <1s for checkpoint creation

## Tool Coordination

- **Glob** `.superclaude/memory/**/*.md`: List the available memories
- **Read**: Memory retrieval and session context loading from `.superclaude/memory/<key>.md`
- **Read/Grep/Glob**: Project structure analysis and configuration discovery
- **Write**: Session context documentation and checkpoint creation
- **Code-graph readiness**: end the session summary with one line telling the user to type `/sc:graph status` to see whether this worktree's code-graph index is ready; `/sc:load` never runs `/sc:graph` itself and never waits on the index

## Key Patterns

- **Project Context Loading**: Directory analysis → memory retrieval → context establishment
- **Session Restoration**: Checkpoint loading → context validation → workflow preparation
- **Memory Management**: Cross-session persistence → context continuity → development efficiency
- **Performance Critical**: Fast initialization → immediate productivity → session readiness

## Examples

### Basic Project Loading

```
/sc:load
# Loads current directory project context from .superclaude/memory/
# Establishes session context and prepares for development workflow
```

### Specific Project Loading

```
/sc:load /path/to/project --type project --analyze
# Loads specific project with comprehensive analysis
# Establishes project context and retrieves cross-session memories
```

### Checkpoint Restoration

```
/sc:load --type checkpoint --checkpoint session_123
# Restores specific checkpoint with session context
# Continues previous work session with full context preservation
```

### Dependency Context Loading

```
/sc:load --type deps --refresh
# Loads dependency context with fresh analysis
# Updates project understanding and dependency mapping
```

## Boundaries

**Will:**

- Load project context from the `.superclaude/memory/` markdown files
- Provide session lifecycle management with cross-session persistence
- Establish project context with comprehensive context loading

**Will Not:**

- Modify project structure or configuration without explicit permission
- Load context without validation
- Override existing session context without checkpoint preservation
