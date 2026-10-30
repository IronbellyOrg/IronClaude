---
name: reflect
description: "Task reflection and validation using native analysis tools and plain-markdown memory files"
category: special
complexity: standard
mcp-servers: []
personas: []
---

# /sc:sc:sc:reflect - Task Reflection and Validation

## Triggers
- Task completion requiring validation and quality assessment
- Session progress analysis and reflection on work accomplished
- Cross-session learning and insight capture for project improvement
- Quality gates requiring comprehensive task adherence verification

## Usage
```
/sc:sc:reflect [--type task|session|completion] [--analyze] [--validate]
```

## Behavioral Flow
1. **Analyze**: Examine current task state and session progress using native tools (TodoRead/TodoWrite, Read, Grep, Glob)
2. **Validate**: Assess task adherence, completion quality, and requirement fulfillment
3. **Reflect**: Apply deep analysis of collected information and session insights
4. **Document**: Update session metadata and capture learning insights
5. **Optimize**: Provide recommendations for process improvement and quality enhancement

Key behaviors:
- Native-tool reflection analysis and task validation (no MCP server required)
- Bridge between TodoWrite patterns and advanced reflection analysis capabilities
- Session lifecycle integration with cross-session persistence and learning capture
- Performance-critical operations with <200ms core reflection and validation
## MCP Integration
- **Native tools**: Reflection analysis, task validation, and session metadata use TodoRead/TodoWrite, Read, Grep, and Glob; no MCP server is required
- **Memory Operations**: Cross-session persistence with plain markdown files under `.superclaude/memory/` (Read, Write, Glob `.superclaude/memory/**/*.md`)
- **Performance Critical**: <200ms for core reflection operations, <1s for checkpoint creation

## Tool Coordination
- **TodoRead/TodoWrite**: Bridge between traditional task management and advanced reflection analysis
- **Task adherence check**: Validates current approach against project goals and session objectives
- **Collected-information check**: Analyzes session work and information gathering completeness
- **Completion check**: Evaluates task completion criteria and remaining work identification
- **Memory Files**: Session metadata updates and cross-session learning capture

## Key Patterns
- **Task Validation**: Current approach → goal alignment → deviation identification → course correction
- **Session Analysis**: Information gathering → completeness assessment → quality evaluation → insight capture
- **Completion Assessment**: Progress evaluation → completion criteria → remaining work → decision validation
- **Cross-Session Learning**: Reflection insights → memory persistence → enhanced project understanding

## Examples

### Task Adherence Reflection
```
/sc:sc:reflect --type task --analyze
# Validates current approach against project goals
# Identifies deviations and provides course correction recommendations
```

### Session Progress Analysis
```
/sc:sc:reflect --type session --validate
# Comprehensive analysis of session work and information gathering
# Quality assessment and gap identification for project improvement
```

### Completion Validation
```
/sc:sc:reflect --type completion
# Evaluates task completion criteria against actual progress
# Determines readiness for task completion and identifies remaining blockers
```

## Boundaries

**Will:**
- Perform comprehensive task reflection and validation using native analysis tools
- Bridge TodoWrite patterns with advanced reflection capabilities for enhanced task management
- Provide cross-session learning capture and session lifecycle integration

**Will Not:**
- Operate without the task-state and file-reading tools reflection depends on
- Override task completion decisions without proper adherence and quality validation
- Bypass session integrity checks and cross-session persistence requirements

