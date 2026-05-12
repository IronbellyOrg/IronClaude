---
name: reflect
description: "Task reflection and validation using Serena MCP analysis capabilities"
category: special
complexity: standard
mcp-servers: [serena, context7]
personas: []
---

# /sc:reflect - Task Reflection and Validation

## Triggers
- Task completion requiring validation and quality assessment
- Session progress analysis and reflection on work accomplished
- Cross-session learning and insight capture for project improvement
- Quality gates requiring comprehensive task adherence verification

## Usage
```
/sc:reflect [--type task|session|completion] [--analyze] [--validate]
```

## Behavioral Flow
1. **Analyze**: Examine current task state and session progress using Serena reflection tools
2. **Validate**: Assess task adherence, completion quality, and requirement fulfillment
3. **Reflect**: Apply deep analysis of collected information and session insights
4. **Re-scrutinize**: For any executable artifacts produced (shell commands, code blocks, action recommendations), extract `(verb, object)` tuples; pass each through session-fact lookup; for allowlisted CLI verbs unresolved by session, fetch external preconditions via context7; block or rewrite contradictions before delivery. Skipped entirely when no executable artifacts are present.
5. **Document**: Update session metadata and capture learning insights
6. **Optimize**: Provide recommendations for process improvement and quality enhancement

Key behaviors:
- Serena MCP integration for comprehensive reflection analysis and task validation
- Bridge between TodoWrite patterns and advanced Serena analysis capabilities
- Session lifecycle integration with cross-session persistence and learning capture
- Performance-critical operations with <200ms core reflection and validation
## MCP Integration
- **Serena MCP**: Mandatory integration for reflection analysis, task validation, and session metadata
- **Reflection Tools**: think_about_task_adherence, think_about_collected_information, think_about_whether_you_are_done
- **Memory Operations**: Cross-session persistence with read_memory, write_memory, list_memories
- **Performance Critical**: <200ms for core reflection operations, <1s for checkpoint creation
- **Context7 MCP**: Conditional invocation during Recommendation Re-scrutiny for CLI verb precondition lookup when session-fact pass is silent.

## Tool Coordination
- **TodoRead/TodoWrite**: Bridge between traditional task management and advanced reflection analysis
- **think_about_task_adherence**: Validates current approach against project goals and session objectives
- **think_about_collected_information**: Analyzes session work and information gathering completeness
- **think_about_whether_you_are_done**: Evaluates task completion criteria and remaining work identification
- **Memory Tools**: Session metadata updates and cross-session learning capture
- **Grep**: File-anchored augmentation during the session-fact pass — pattern lookup within config files, mirror files, or pasted log paths the conversation references. Grep operates on files, not the transcript; transcript scanning is handled by in-context reasoning.
- **WebSearch**: Fallback CLI precondition lookup when Context7 doesn't cover the tool.

## Key Patterns
- **Task Validation**: Current approach → goal alignment → deviation identification → course correction
- **Session Analysis**: Information gathering → completeness assessment → quality evaluation → insight capture
- **Completion Assessment**: Progress evaluation → completion criteria → remaining work → decision validation
- **Cross-Session Learning**: Reflection insights → memory persistence → enhanced project understanding
- **Recommendation Re-scrutiny**: Extract executable artifacts → session-fact lookup → conditional external-doc lookup → decision gate (pass/block/hedge) → audit annotation.

## Examples

### Task Adherence Reflection
```
/sc:reflect --type task --analyze
# Validates current approach against project goals
# Identifies deviations and provides course correction recommendations
```

### Session Progress Analysis
```
/sc:reflect --type session --validate
# Comprehensive analysis of session work and information gathering
# Quality assessment and gap identification for project improvement
```

### Completion Validation
```
/sc:reflect --type completion
# Evaluates task completion criteria against actual progress
# Determines readiness for task completion and identifies remaining blockers
```

## Boundaries

**Will:**
- Perform comprehensive task reflection and validation using Serena MCP analysis tools
- Bridge TodoWrite patterns with advanced reflection capabilities for enhanced task management
- Provide cross-session learning capture and session lifecycle integration
- Re-scrutinize executable artifacts emitted by the reflection itself before delivery.
- Block reflection-emitted recommendations that contradict facts asserted in the current session or in authoritative external documentation.
- Annotate every cleared recommendation with the basis on which it was cleared.

**Will Not:**
- Operate without proper Serena MCP integration and reflection tool access
- Override task completion decisions without proper adherence and quality validation
- Bypass session integrity checks and cross-session persistence requirements
- Maintain a persistent cross-session entity registry or knowledge graph; the session-fact set is ephemeral and lives only within one reflect call.
- Block on hedge cases for LOW/MEDIUM stakes — when neither session nor external docs resolve a precondition question for a non-HIGH-stakes verb, surface the unverified status and recommend a check, but do not refuse to deliver. (HIGH-stakes verbs DO block on hedge per the design's §3.6.)
- Validate non-executable commentary, prose analysis, or reasoning narratives — only artifacts the user is expected to act on are in scope.

