---
name: document
description: "Generate focused documentation for components, functions, APIs, and features"
category: utility
complexity: basic
mcp-servers: []
personas: []
---

# /sc:document - Focused Documentation Generation

## Triggers

- Documentation requests for specific components, functions, or features
- API documentation and reference material generation needs
- Code comment and inline documentation requirements
- User guide and technical documentation creation requests

## Usage

```
/sc:document [target] [--type inline|external|api|guide] [--style brief|detailed]
/sc:document [target] [--output <path>] [--unattended] [--report-dir <dir>]
```

`--output <path>` writes the generated documentation to that path. `--type inline` edits files in place and needs no `--output`.

## Behavioral Flow

1. **Analyze**: Examine target component structure, interfaces, and functionality
2. **Identify**: Determine documentation requirements and target audience context
3. **Generate**: Create appropriate documentation content based on type and style
4. **Format**: Apply consistent structure and organizational patterns
5. **Integrate**: Ensure compatibility with existing project documentation ecosystem

Key behaviors:

- Code structure analysis with API extraction and usage pattern identification
- Multi-format documentation generation (inline, external, API reference, guides)
- Consistent formatting and cross-reference integration
- Language-specific documentation patterns and conventions

## Tool Coordination

- **Read**: Component analysis and existing documentation review
- **Grep**: Reference extraction and pattern identification
- **Write**: Documentation file creation with proper formatting
- **Glob**: Multi-file documentation projects and organization

## Key Patterns

- **Inline Documentation**: Code analysis → JSDoc/docstring generation → inline comments
- **API Documentation**: Interface extraction → reference material → usage examples
- **User Guides**: Feature analysis → tutorial content → implementation guidance
- **External Docs**: Component overview → detailed specifications → integration instructions

## Examples

### Inline Code Documentation

```
/sc:document src/auth/login.js --type inline
# Generates JSDoc comments with parameter and return descriptions
# Adds comprehensive inline documentation for functions and classes
```

### API Reference Generation

```
/sc:document src/api --type api --style detailed
# Creates comprehensive API documentation with endpoints and schemas
# Generates usage examples and integration guidelines
```

### User Guide Creation

```
/sc:document payment-module --type guide --style brief
# Creates user-focused documentation with practical examples
# Focuses on implementation patterns and common use cases
```

### Component Documentation

```
/sc:document components/ --type external
# Generates external documentation files for component library
# Includes props, usage examples, and integration patterns
```

## Unattended mode

The shared rules are in `~/.claude/WORKER-CONTRACT.md`; read it first. This section lists only what `/sc:document` resolves itself.

- **Switch.** It applies only when `--unattended` is a standalone argument token outside any quoted argument; otherwise nothing here applies and no worker contract is written.
- **Report directory.** `--report-dir <dir>` only (`--output` is the documentation path, not the contract directory). Without it the run is refused before any work and the refusal is printed in chat only. A directory inside `.git/` or `.codegraph/`, one under the distributable skill, agent or command folders of a `.claude/` folder, or one that cannot be created or written, counts as no report directory known (refusal printed in chat only).
- **Output path.** For the `external`, `api` and `guide` types `--output <path>` is required under `--unattended`; without it the contract is failed with a `reason` saying so, before any documentation is written. For `--type inline` the command edits files in place and needs no `--output`.
- **Contract.** `<report-dir>/return-contract.yaml` is written on every outcome. `report_path` is the `--output` path (null for `--type inline`); for `--type inline`, `artifacts` lists every file edited. The run is succeeded when the documentation is written, and failed otherwise.
- **Gates.** None else, and no person-mode flag. Nested invocations: none.
- **Outward actions.** It pushes, commits and stages nothing.

## Boundaries

**Will:**

- Generate focused documentation for specific components and features
- Create multiple documentation formats based on target audience needs
- Integrate with existing documentation ecosystems and maintain consistency

**Will Not:**

- Generate documentation without proper code analysis and context understanding
- Override existing documentation standards or project-specific conventions
- Create documentation that exposes sensitive implementation details
