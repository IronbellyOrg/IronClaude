---
name: improve
description: "Apply systematic improvements to code quality, performance, and maintainability"
category: workflow
complexity: standard
mcp-servers: [litellm, context7]
personas: [architect, performance, quality, security]
---

# /sc:improve - Code Improvement

## Triggers

- Code quality enhancement and refactoring requests
- Performance optimization and bottleneck resolution needs
- Maintainability improvements and technical debt reduction
- Best practices application and coding standards enforcement

## Usage

```
/sc:improve [target] [--type quality|performance|maintainability|style] [--safe] [--interactive]
/sc:improve [target] [--output <file>] [--unattended] [--report-dir <dir>]
```

`--output <file>` writes the improvement summary to that file; a run without `--unattended` writes a file only when the caller passes it.

## Behavioral Flow

1. **Analyze**: Examine codebase for improvement opportunities and quality issues
2. **Plan**: Choose improvement approach and activate relevant personas for expertise
3. **Execute**: Apply systematic improvements with domain-specific best practices
4. **Validate**: Ensure improvements preserve functionality and meet quality standards
5. **Document**: Generate improvement summary and recommendations for future work

Key behaviors:

- Multi-persona coordination (architect, performance, quality, security) based on improvement type
- Framework-specific optimization via Context7 integration for best practices
- Systematic analysis via native reasoning for complex multi-component improvements
- Safe refactoring with comprehensive validation and rollback capabilities

## MCP Integration

- **Native reasoning**: Complex multi-step improvement analysis and planning
- **Context7 MCP**: Framework-specific best practices and optimization patterns
- **Persona Coordination**: Architect (structure), Performance (speed), Quality (maintainability), Security (safety)

## Tool Coordination

- **Read/Grep/Glob**: Code analysis and improvement opportunity identification
- **Edit/MultiEdit**: Safe code modification and systematic refactoring
- **TodoWrite**: Progress tracking for complex multi-file improvement operations
- **Task**: Delegation for large-scale improvement workflows requiring systematic coordination

## Key Patterns

- **Quality Improvement**: Code analysis → technical debt identification → refactoring application
- **Performance Optimization**: Profiling analysis → bottleneck identification → optimization implementation
- **Maintainability Enhancement**: Structure analysis → complexity reduction → documentation improvement
- **Security Hardening**: Vulnerability analysis → security pattern application → validation verification

## Examples

### Code Quality Enhancement

```
/sc:improve src/ --type quality --safe
# Systematic quality analysis with safe refactoring application
# Improves code structure, reduces technical debt, enhances readability
```

### Performance Optimization

```
/sc:improve api-endpoints --type performance --interactive
# Performance persona analyzes bottlenecks and optimization opportunities
# Interactive guidance for complex performance improvement decisions
```

### Maintainability Improvements

```
/sc:improve legacy-modules --type maintainability --preview
# Architect persona analyzes structure and suggests maintainability improvements
# Preview mode shows changes before application for review
```

### Security Hardening

```
/sc:improve auth-service --type security --validate
# Security persona identifies vulnerabilities and applies security patterns
# Comprehensive validation ensures security improvements are effective
```

## Unattended mode

The shared rules are in `~/.claude/WORKER-CONTRACT.md`; read it first. This section lists only what `/sc:improve` resolves itself.

- **Switch.** It applies only when `--unattended` is a standalone argument token outside any quoted argument; otherwise nothing here applies and no worker contract is written.
- **Report directory.** `--report-dir <dir>` only (`--output` is file-valued). Without it the run is refused before any work and the refusal is printed in chat only. A directory inside `.git/` or `.codegraph/`, one under the distributable skill, agent or command folders of a `.claude/` folder, or one that cannot be created or written, counts as no report directory known (refusal printed in chat only).
- **Contract.** `<report-dir>/return-contract.yaml` is written on every outcome. `report_path` is the `--output` file, or `<report-dir>/improve-report.md`, holding the items applied, the items not applied and every changed file. `artifacts` lists every changed file, because the rollback mechanism is unverified; paths git ignores are left out (WC-4), and the report still names them. It is `[]` when nothing changed. The run is succeeded when the report is written and every applied change passed the command's own validation (or nothing was applied), partial when changes were applied and a validation failed or did not run (the report says which), and failed otherwise.
- **Person-mode flags.** `--interactive` is refused before any work (contract `worker_status: failed`, the flag in `reason`). `--force` is refused too, because it widens what is applied without confirmation.
- **Gates.** Under `--unattended` only the items outside the "Approval Required" list and outside the "Explicitly Will NOT (without `--force` flag)" list are applied: every item under "Approval Required" is listed as not applied, and so is every item of the second list. `--force` is refused, so that second list is never lifted. There is no other gate.
- **Nested invocations.** None.
- **Outward actions.** It pushes, commits and stages nothing.

## Boundaries

**Will:**

- Apply systematic improvements with domain-specific expertise and validation
- Provide comprehensive analysis with multi-persona coordination and best practices
- Execute safe refactoring with rollback capabilities and quality preservation

**Will Not:**

- Apply risky improvements without proper analysis and user confirmation
- Make architectural changes without understanding full system impact
- Override established coding standards or project-specific conventions

## AUTO-FIX VS APPROVAL-REQUIRED

**Auto-fix (applies automatically)**:

- Style fixes (formatting, naming conventions)
- Unused variable removal
- Import organization
- Simple type annotations

**Approval Required (prompts user first)**:

- Architectural changes
- Logic refactoring
- Function signature changes
- Removing code used by public APIs
- Changes affecting multiple files

**Explicitly Will NOT** (without `--force` flag):

- Make architectural decisions
- Refactor code structure without confirmation
- Remove functionality
