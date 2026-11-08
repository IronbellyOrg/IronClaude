---
name: explain
description: "Provide clear explanations of code, concepts, and system behavior with educational clarity"
category: workflow
complexity: standard
mcp-servers: [litellm, context7, codegraph]
personas: [educator, architect, security]
---

# /sc:explain - Code and Concept Explanation

## Triggers

- Code understanding and documentation requests for complex functionality
- System behavior explanation needs for architectural components
- Educational content generation for knowledge transfer
- Framework-specific concept clarification requirements

## Usage

```
/sc:explain [target] [--level basic|intermediate|advanced] [--format text|examples|interactive] [--context domain]
/sc:explain [target] [--output <file>] [--unattended] [--report-dir <dir>]
```

`--output <file>` writes the explanation to that file. A standalone run writes a file only when you pass it.

## Behavioral Flow

1. **Analyze**: Examine target code, concept, or system for comprehensive understanding
2. **Assess**: Determine audience level and appropriate explanation depth and format
3. **Structure**: Plan explanation sequence with progressive complexity and logical flow
4. **Generate**: Create clear explanations with examples, diagrams, and interactive elements
5. **Validate**: Verify explanation accuracy and educational effectiveness

Key behaviors:

- Multi-persona coordination for domain expertise (educator, architect, security)
- Framework-specific explanations via Context7 integration
- Systematic analysis via native reasoning for complex concept breakdown
- Adaptive explanation depth based on audience and complexity

## MCP Integration

- **Native reasoning**: Complex multi-component analysis and structured reasoning
- **Context7 MCP**: Framework documentation and official pattern explanations
- **Persona Coordination**: Educator (learning), Architect (systems), Security (practices)

## Tool Coordination

- **Read/Grep/Glob**: Code analysis and pattern identification for explanation content
- **TodoWrite**: Progress tracking for complex multi-part explanations
- **Write**: Used only for the explanation file under `--output` or `--unattended`
- **Task**: Delegation for comprehensive explanation workflows requiring systematic breakdown
- **Codegraph one-hop view** (code targets only, when codegraph is usable): `codegraph_search` (limit 10) to find the target symbol, then `codegraph_callers` and `codegraph_callees` (limit 10 each) for its direct callers and callees; Read every row before citing it, and use Read/Grep alone when codegraph is unusable. Codegraph usage rules: read `~/.claude/CODEGRAPH.md` (in a dev checkout without an install, the labelled fallback is `src/superclaude/core/CODEGRAPH.md`).

## Key Patterns

- **Progressive Learning**: Basic concepts → intermediate details → advanced implementation
- **Framework Integration**: Context7 documentation → accurate official patterns and practices
- **Multi-Domain Analysis**: Technical accuracy + educational clarity + security awareness
- **Interactive Explanation**: Static content → examples → interactive exploration

## Examples

### Basic Code Explanation

```
/sc:explain authentication.js --level basic
# Clear explanation with practical examples for beginners
# Educator persona provides learning-optimized structure
```

### Framework Concept Explanation

```
/sc:explain react-hooks --level intermediate --context react
# Context7 integration for official React documentation patterns
# Structured explanation with progressive complexity
```

### System Architecture Explanation

```
/sc:explain microservices-system --level advanced --format interactive
# Architect persona explains system design and patterns
```

### Security Concept Explanation

```
/sc:explain jwt-authentication --context security --level basic
# Security persona explains authentication concepts and best practices
# Framework-agnostic security principles with practical examples
```

## Unattended mode

The shared rules are in `~/.claude/WORKER-CONTRACT.md`; read it first. This section lists only what `/sc:explain` resolves itself.

- **Switch.** It applies only when `--unattended` is a standalone argument token outside any quoted argument; otherwise nothing here applies and no worker contract is written.
- **Report directory.** `--report-dir <dir>` only (`--output` is file-valued). Without it the run is refused before any work and the refusal is printed in chat only. A directory inside `.git/` or `.codegraph/`, one under the distributable skill, agent or command folders of a `.claude/` folder, or one that cannot be created or written, counts as no report directory known (refusal printed in chat only).
- **Contract.** `<report-dir>/return-contract.yaml` is written on every outcome. The explanation is written to the `--output` file, or to `<report-dir>/explain-report.md` when `--output` is absent; Write is used only for that file. `report_path` is that file. The run is succeeded when the explanation is written, and failed otherwise.
- **Person-mode flags.** `--format interactive` and `--format=interactive` are refused before any work (contract `worker_status: failed`, the flag in `reason`).
- **Gates.** There is no other gate. Nested invocations: none.
- **Outward actions.** It pushes, commits and stages nothing.

## Boundaries

**Will:**

- Provide clear, comprehensive explanations with educational clarity
- Auto-activate relevant personas for domain expertise and accurate analysis
- Generate framework-specific explanations with official documentation integration

**Will Not:**

- Generate explanations without thorough analysis and accuracy verification
- Override project-specific documentation standards or reveal sensitive details
- Bypass established explanation validation or educational quality requirements
