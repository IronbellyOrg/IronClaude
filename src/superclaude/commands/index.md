---
name: index
description: "Generate comprehensive project documentation and knowledge base with intelligent organization"
category: special
complexity: standard
mcp-servers: [litellm, context7]
personas: [architect, scribe, quality]
---

# /sc:index - Project Documentation

## Triggers

- Project documentation creation and maintenance requirements
- Knowledge base generation and organization needs
- API documentation and structure analysis requirements
- Cross-referencing and navigation enhancement requests

## Usage

```
/sc:index [target] [--type docs|api|structure|readme] [--format md|json|yaml]
/sc:index [target] [--output <path>] [--unattended] [--report-dir <dir>]
```

`--output <path>` writes the generated documentation to that path. Without it a standalone run behaves as before.

## Behavioral Flow

1. **Analyze**: Examine project structure and identify key documentation components
2. **Organize**: Apply intelligent organization patterns and cross-referencing strategies
3. **Generate**: Create comprehensive documentation with framework-specific patterns
4. **Validate**: Ensure documentation completeness and quality standards
5. **Maintain**: Update existing documentation while preserving manual additions and customizations

Key behaviors:

- Multi-persona coordination (architect, scribe, quality) based on documentation scope and complexity
- Native reasoning for systematic analysis and comprehensive documentation workflows
- Context7 MCP integration for framework-specific patterns and documentation standards
- Intelligent organization with cross-referencing capabilities and automated maintenance

## MCP Integration

- **Native reasoning**: Complex multi-step project analysis and systematic documentation generation
- **Context7 MCP**: Framework-specific documentation patterns and established standards
- **Persona Coordination**: Architect (structure), Scribe (content), Quality (validation)

## Tool Coordination

- **Read/Grep/Glob**: Project structure analysis and content extraction for documentation generation
- **Write**: Documentation creation with intelligent organization and cross-referencing
- **TodoWrite**: Progress tracking for complex multi-component documentation workflows
- **Task**: Advanced delegation for large-scale documentation requiring systematic coordination

## Key Patterns

- **Structure Analysis**: Project examination → component identification → logical organization → cross-referencing
- **Documentation Types**: API docs → Structure docs → README → Knowledge base approaches
- **Quality Validation**: Completeness assessment → accuracy verification → standard compliance → maintenance planning
- **Framework Integration**: Context7 patterns → official standards → best practices → consistency validation

## Examples

### Project Structure Documentation

```
/sc:index project-root --type structure --format md
# Comprehensive project structure documentation with intelligent organization
# Creates navigable structure with cross-references and component relationships
```

### API Documentation Generation

```
/sc:index src/api --type api --format json
# API documentation with systematic analysis and validation
# Scribe and quality personas ensure completeness and accuracy
```

### Knowledge Base Creation

```
/sc:index . --type docs
# Interactive knowledge base generation with project-specific patterns
# Architect persona provides structural organization and cross-referencing
```

## Unattended mode

The shared rules are in `~/.claude/WORKER-CONTRACT.md`; read it first. This section lists only what `/sc:index` resolves itself.

- **Switch.** It applies only when `--unattended` is a standalone argument token outside any quoted argument; otherwise nothing here applies and no worker contract is written.
- **Report directory.** `--report-dir <dir>` only (`--output` is the documentation path, not the contract directory). Without it the run is refused before any work and the refusal is printed in chat only. A directory inside `.git/` or `.codegraph/`, one under the distributable skill, agent or command folders of a `.claude/` folder, or one that cannot be created or written, counts as no report directory known (refusal printed in chat only).
- **Contract.** `<report-dir>/return-contract.yaml` is written on every outcome. `--output <path>` is where the generated documentation goes, defaulting under `--unattended` to `<report-dir>/index-report.md`; `report_path` is that path. The run is succeeded when the documentation is written, and failed otherwise.
- **Knowledge base.** The knowledge-base mode (`--type docs`) does not wait for a person under `--unattended`.
- **Gates.** There is no other gate, and no person-mode flag. Under `--unattended` consent is never given: the rule "without explicit update permission" is not answered by assuming consent, so no existing manual documentation is overwritten and the command writes only the `--output` path or the default report file.
- **Nested invocations.** None.
- **Outward actions.** It pushes, commits and stages nothing.

## Boundaries

**Will:**

- Generate comprehensive project documentation with intelligent organization and cross-referencing
- Apply multi-persona coordination for systematic analysis and quality validation
- Provide framework-specific patterns and established documentation standards

**Will Not:**

- Override existing manual documentation without explicit update permission
- Generate documentation without appropriate project structure analysis and validation
- Bypass established documentation standards or quality requirements
