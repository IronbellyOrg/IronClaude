---
name: cleanup
description: "Systematically clean up code, remove dead code, and optimize project structure"
category: workflow
complexity: standard
mcp-servers: [context7]
personas: [architect, quality, security]
---

# /sc:cleanup - Code and Project Cleanup

## Triggers

- Code maintenance and technical debt reduction requests
- Dead code removal and import optimization needs
- Project structure improvement and organization requirements
- Codebase hygiene and quality improvement initiatives

## Usage

```
/sc:cleanup [target] [--type code|imports|files|all] [--safe|--aggressive] [--interactive]
/sc:cleanup [target] [--output <file>] [--unattended] [--report-dir <dir>]
```

`--output <file>` writes the cleanup summary to that file; a run without `--unattended` writes a file only when the caller passes it.

## Behavioral Flow

1. **Analyze**: Assess cleanup opportunities and safety considerations across target scope
2. **Plan**: Choose cleanup approach and activate relevant personas for domain expertise
3. **Execute**: Apply systematic cleanup with intelligent dead code detection and removal
4. **Validate**: Ensure no functionality loss through testing and safety verification
5. **Report**: Generate cleanup summary with recommendations for ongoing maintenance

Key behaviors:

- Multi-persona coordination (architect, quality, security) based on cleanup type
- Framework-specific cleanup patterns via Context7 MCP integration
- Systematic analysis via native reasoning for complex cleanup operations
- Safety-first approach with backup and rollback capabilities

## MCP Integration

- **Native reasoning**: Complex multi-step cleanup analysis and planning
- **Context7 MCP**: Framework-specific cleanup patterns and best practices
- **Persona Coordination**: Architect (structure), Quality (debt), Security (credentials)

## Tool Coordination

- **Read/Grep/Glob**: Code analysis and pattern detection for cleanup opportunities
- **Edit/MultiEdit**: Safe code modification and structure optimization
- **TodoWrite**: Progress tracking for complex multi-file cleanup operations
- **Task**: Delegation for large-scale cleanup workflows requiring systematic coordination

## Key Patterns

- **Dead Code Detection**: Usage analysis → safe removal with dependency validation
- **Import Optimization**: Dependency analysis → unused import removal and organization
- **Structure Cleanup**: Architectural analysis → file organization and modular improvements
- **Safety Validation**: Pre/during/post checks → preserve functionality throughout cleanup

## Examples

### Safe Code Cleanup

```
/sc:cleanup src/ --type code --safe
# Conservative cleanup with automatic safety validation
# Removes dead code while preserving all functionality
```

### Import Optimization

```
/sc:cleanup --type imports --preview
# Analyzes and shows unused import cleanup without execution
# Framework-aware optimization via Context7 patterns
```

### Comprehensive Project Cleanup

```
/sc:cleanup --type all --interactive
# Multi-domain cleanup with user guidance for complex decisions
# Activates all personas for comprehensive analysis
```

### Framework-Specific Cleanup

```
/sc:cleanup components/ --aggressive
# Thorough cleanup with Context7 framework patterns
```

## Unattended mode

The shared rules are in `~/.claude/WORKER-CONTRACT.md`; read it first. This section lists only what `/sc:cleanup` resolves itself.

- **Switch.** It applies only when `--unattended` is a standalone argument token outside any quoted argument; otherwise nothing here applies and no worker contract is written.
- **Report directory.** `--report-dir <dir>` only (`--output` is file-valued). Without it the run is refused before any work and the refusal is printed in chat only. A directory inside `.git/` or `.codegraph/`, one under the distributable skill, agent or command folders of a `.claude/` folder, or one that cannot be created or written, counts as no report directory known (refusal printed in chat only).
- **Contract.** `<report-dir>/return-contract.yaml` is written on every outcome. `report_path` is the `--output` file, or `<report-dir>/cleanup-report.md`, holding the items applied, the items not applied and every changed file. `artifacts` lists every changed file, because the rollback mechanism is unverified; paths git ignores are left out (WC-4), and the report still names them. It is `[]` when nothing changed. The run is succeeded when the report is written, and failed otherwise.
- **Person-mode flags.** `--interactive` is refused before any work (contract `worker_status: failed`, the flag in `reason`).
- **Gates.** Under `--unattended` only the items of the auto-fix list are applied: every item under "Approval Required" is listed as not applied, and so is every item the "Safety Threshold" would prompt for (code with any usage path, code that affects the public API, anything uncertain). There is no other gate.
- **Nested invocations.** None.
- **Outward actions.** It pushes, commits and stages nothing.

## Boundaries

**Will:**

- Systematically clean code, remove dead code, and optimize project structure
- Provide comprehensive safety validation with backup and rollback capabilities
- Apply intelligent cleanup algorithms with framework-specific pattern recognition

**Will Not:**

- Remove code without thorough safety analysis and validation
- Override project-specific cleanup exclusions or architectural constraints
- Apply cleanup operations that compromise functionality or introduce bugs

## AUTO-FIX VS APPROVAL-REQUIRED

**Auto-fix (applies automatically)**:

- Unused imports removal
- Dead code with zero references
- Empty blocks removal
- Redundant type annotations

**Approval Required (prompts user first)**:

- Code with indirect references
- Exports potentially used externally
- Test fixtures/utilities
- Configuration values

**Safety Threshold**:

- If code has ANY usage path, prompt user
- If code affects public API, prompt user
- If unsure, prompt user
