---
name: spawn
description: "Meta-system task orchestration with intelligent breakdown and delegation"
category: special
complexity: high
mcp-servers: []
personas: []
---

# /sc:spawn - Meta-System Task Orchestration

## Triggers
- Complex multi-domain operations requiring intelligent task breakdown
- Large-scale system operations spanning multiple technical areas
- Operations requiring parallel coordination and dependency management
- Meta-level orchestration beyond standard command capabilities

## Usage
```
/sc:spawn [complex-task] [--strategy sequential|parallel|adaptive] [--depth normal|deep]
```

## Behavioral Flow
1. **Analyze**: Parse complex operation requirements and assess scope across domains
2. **Decompose**: Break down operation into coordinated subtask hierarchies
3. **Enrich**: Construct delegated prompts with evidence and path injection (see Prompt Construction Rules)
4. **Orchestrate**: Execute tasks using optimal coordination strategy (parallel/sequential)
5. **Monitor**: Track progress across task hierarchies with dependency management
6. **Integrate**: Aggregate results and provide comprehensive orchestration summary

Key behaviors:
- Meta-system task decomposition with Epic → Story → Task → Subtask breakdown
- Intelligent coordination strategy selection based on operation characteristics
- Cross-domain operation management with parallel and sequential execution patterns
- Advanced dependency analysis and resource optimization across task hierarchies

## Prompt Construction Rules

When constructing prompts for delegated agents, sc:spawn MUST enrich the user's intent with operational specificity. Passing a bare goal to a delegated command produces structurally sound but evidence-thin output. However, do NOT override the delegated command's own output structure — delegated protocols produce better analytical organization than orchestrator-imposed templates.

### Rule 1: Resolve File Paths Before Delegation
Before spawning synchronous agents, resolve all input file paths using Glob/Read. Each agent prompt MUST include absolute paths to every file the agent needs to read. Never delegate path discovery to the sub-agent.

For async task hierarchies where agents run later or in separate contexts, include path hints (directory + glob pattern) rather than requiring pre-resolution of every path.

### Rule 2: Inject Tiered Evidence Requirements
Delegated prompts that produce analytical output MUST include an evidence standard, but the tier depends on the task type:

**Verification tasks** (coverage checks, dependency validation, consistency audits):
```
Evidence standard: cite specific line numbers, task IDs, section references,
or direct quotes from source documents for every finding. Unsupported
assertions must be flagged as LOW CONFIDENCE.
```

**Discovery tasks** (gap detection, risk assessment, open-ended reflection):
```
Evidence standard: support findings with specific references where possible.
Findings based on inference or absence of evidence should be flagged as
INFERENTIAL and include the reasoning chain. Do not let citation requirements
constrain exploratory analysis.
```

This tiered approach preserves evidence rigor for confirmatory work without constraining the open-ended discovery that catches gaps a rigid template would miss.

### Rule 3: Inject Cross-Reference Counts (When Available)
When Rule 1 has already read a source document and the delegated task involves coverage verification, extract and inject the known count (e.g., "The merged plan contains 20 edits — verify all 20 are covered"). Do NOT pre-read documents solely for counting — this rule applies opportunistically when path resolution has already loaded the file.
## MCP Integration
- **Native Orchestration**: Meta-system command uses native coordination without MCP dependencies
- **Progressive Integration**: Coordination with systematic execution for progressive enhancement
- **Framework Integration**: Advanced integration with SuperClaude orchestration layers

## Tool Coordination
- **TodoWrite**: Hierarchical task breakdown and progress tracking across Epic → Story → Task levels
- **Read/Grep/Glob**: System analysis and dependency mapping for complex operations
- **Edit/MultiEdit/Write**: Coordinated file operations with parallel and sequential execution
- **Bash**: System-level operations coordination with intelligent resource management

## Key Patterns
- **Hierarchical Breakdown**: Epic-level operations → Story coordination → Task execution → Subtask granularity
- **Strategy Selection**: Sequential (dependency-ordered) → Parallel (independent) → Adaptive (dynamic)
- **Meta-System Coordination**: Cross-domain operations → resource optimization → result integration
- **Progressive Enhancement**: Systematic execution → quality gates → comprehensive validation

## Examples

### Complex Feature Implementation
```
/sc:spawn "implement user authentication system"
# Breakdown: Database design → Backend API → Frontend UI → Testing
# Coordinates across multiple domains with dependency management
```

### Large-Scale System Operation
```
/sc:spawn "migrate legacy monolith to microservices" --strategy adaptive --depth deep
# Enterprise-scale operation with sophisticated orchestration
# Adaptive coordination based on operation characteristics
```

### Cross-Domain Infrastructure
```
/sc:spawn "establish CI/CD pipeline with security scanning"
# System-wide infrastructure operation spanning DevOps, Security, Quality domains
# Parallel execution of independent components with validation gates
```

## Boundaries

**Will:**
- Decompose complex multi-domain operations into coordinated task hierarchies
- Provide intelligent orchestration with parallel and sequential coordination strategies
- Execute meta-system operations beyond standard command capabilities

**Will Not:**
- Replace domain-specific commands for simple operations
- Override user coordination preferences or execution strategies
- Execute operations without proper dependency analysis and validation

## CRITICAL BOUNDARIES

**STOP AFTER TASK DECOMPOSITION**

This command produces a TASK HIERARCHY ONLY - delegates execution to other commands.

**Explicitly Will NOT**:
- Execute implementation tasks directly
- Write or modify code
- Create system changes
- Replace domain-specific commands

**Output**: Task breakdown document with:
- Epic decomposition
- Task hierarchy with dependencies
- Delegation assignments (which `/sc:*` command handles each task)
- Coordination strategy

**Next Step**: Execute individual tasks using delegated commands (`/sc:implement`, `/sc:design`, `/sc:test`, etc.)