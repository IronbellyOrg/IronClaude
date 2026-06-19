# SuperClaude Framework developer-guide Index

## Document Navigation Guide

This index provides comprehensive access to all SuperClaude Framework development documentation, organized by topic and skill level for efficient information discovery.

### Quick Navigation

**For New Contributors**: Start with [Contributing Guide → Setup](contributing-code.md#development-setup)

**For System Understanding**: Begin with [Technical Architecture Guide → Context Architecture](technical-architecture.md#context-file-architecture)

**For Verification**: Start with [Verification Guide → Installation Check](testing-debugging.md#installation-verification)

---

## Primary Documentation

### 📋 [Contributing Context Files Guide](contributing-code.md)

**Purpose**: Complete context file development and contribution guidelines  
**Target Audience**: Framework contributors and context file developers  
**Length**: ~1,000 lines focused on context file reality

**Key Sections**:

- [Development Setup](contributing-code.md#development-setup) - Environment configuration and prerequisites
- [Context File Guidelines](contributing-code.md#context-file-guidelines) - Standards and structure
- [Development Workflow](contributing-code.md#development-workflow) - Git workflow and submission process
- [Contributing to Components](contributing-code.md#contributing-to-components) - Agent, command, and mode development
- [File Validation](contributing-code.md#file-validation) - Context file verification methods

### 🌿 [Git Standards and Repository Protocols](git-standards-protocols.md)

**Purpose**: Git workflow, branching strategy, commit conventions, PR protocol, code review, release/hotfix, and CI automation standards  
**Target Audience**: All contributors and maintainers working with branches, commits, and pull requests  
**Length**: ~880 lines; consolidated git/repository governance reference

**Key Sections**:

- [Repository Structure](git-standards-protocols.md#section-1-repository-structure) - Layout and ownership
- [Branching Strategy](git-standards-protocols.md#section-2-branching-strategy) - Branch model and naming
- [Commit Standards](git-standards-protocols.md#section-3-commit-standards) - Conventional commit conventions
- [Pull Request Protocol](git-standards-protocols.md#section-4-pull-request-protocol) - PR lifecycle and targets
- [Code Review Standards](git-standards-protocols.md#section-5-code-review-standards) - Review expectations
- [Release and Tagging Protocol](git-standards-protocols.md#section-6-release-and-tagging-protocol) - Versioning and tags
- [Hotfix Procedures](git-standards-protocols.md#section-7-hotfix-procedures) - Emergency fix flow
- [GitHub Actions and Automation](git-standards-protocols.md#section-8-github-actions-and-automation) - CI/CD pipelines
- [Security and Access Controls](git-standards-protocols.md#section-9-security-and-access-controls) - Access governance

### 🏗️ [Context Architecture Guide](technical-architecture.md)

**Purpose**: Understanding how context files work and are structured  
**Target Audience**: Anyone wanting to understand or extend SuperClaude  
**Length**: ~800 lines focused on context file patterns and Claude Code integration

**Key Sections**:

- [Context File Architecture](technical-architecture.md#context-file-architecture) - Directory structure and file types
- [The Import System](technical-architecture.md#the-import-system) - How Claude Code loads context
- [Agent Context Structure](technical-architecture.md#agent-context-structure) - Domain specialist contexts
- [Command Context Structure](technical-architecture.md#command-context-structure) - Workflow patterns
- [How Claude Code Reads Context](technical-architecture.md#how-claude-code-reads-context) - Processing sequence
- [Extending the Framework](technical-architecture.md#extending-the-framework) - Adding new components

### 🧪 [cliEval Pipeline — Operator User Guide](../user-guide/eval-pipeline.md)

**Purpose**: Task-oriented walkthrough of the `superclaude eval` CLI surface (`eval doctor`, `eval list`, `eval describe`, `eval run`)
**Target Audience**: Operators running the cliEval harness; CI authors wiring eval into pipelines
**Length**: ~400 lines; source of truth for flag tables, exit codes, output layout, and the AC12 scratch-root allowlist policy

**Key Sections**:

- [Quick start](../user-guide/eval-pipeline.md#quick-start) — minimal command sequence for a new machine
- [The four subcommands](../user-guide/eval-pipeline.md#the-four-subcommands) — full flag reference for `doctor` / `list` / `describe` / `run`
- [Exit codes](../user-guide/eval-pipeline.md#exit-codes) — canonical 0/1/2/3 contract and the typed-exception mapping
- [Output layout](../user-guide/eval-pipeline.md#output-layout) — FR-G4 reproducible layout under `--output-dir`
- [Scratch-root allowlist (AC12 / OPS-002)](../user-guide/eval-pipeline.md#scratch-root-allowlist-ac12--ops-002) — H4 bare-prefix rule + H5 write-before-validate ordering
- [Coverage gate (FR-G5)](../user-guide/eval-pipeline.md#coverage-gate-fr-g5) — hook-matcher coverage enforcement
- [Common workflows + troubleshooting](../user-guide/eval-pipeline.md#common-workflows) — CI invocation, debugging, NFR-PERF4 disk budget

**Deep technical references:** [`docs/eval/`](../eval/) — `scratch-roots.md`, `runtime.md`, `retention.md`, `retry.md`, `validation-commands.md`, `release-checklist.md`.

### 🧪 [Verification & Troubleshooting Guide](testing-debugging.md)

**Purpose**: Verifying installation and troubleshooting context file issues  
**Target Audience**: Users and maintainers  
**Length**: ~500 lines focused on file verification and Claude Code integration

**Key Sections**:

- [Installation Verification](testing-debugging.md#installation-verification) - Check context file installation
- [Context File Verification](testing-debugging.md#context-file-verification) - File structure validation
- [MCP Server Verification](testing-debugging.md#mcp-server-verification) - External tool configuration
- [Common Issues](testing-debugging.md#common-issues) - Troubleshooting activation problems
- [Troubleshooting Commands](testing-debugging.md#troubleshooting-commands) - Diagnostic procedures

---

## Topic-Based Index

### 🚀 Getting Started

**Complete Beginners**:

1. [Contributing Guide → Setup](contributing-code.md#development-setup) - Environment setup
2. [Architecture Guide → Overview](technical-architecture.md#overview) - Understanding context files
3. [Verification Guide → Installation Check](testing-debugging.md#installation-verification) - Basic verification

**Environment Setup**:

- [Development Setup](contributing-code.md#development-setup) - Prerequisites and configuration
- [Installation Verification](testing-debugging.md#installation-verification) - File installation check

### 🏗️ Architecture & Design

**Context File Architecture**:

- [Context File Architecture](technical-architecture.md#context-file-architecture) - Complete system design
- [The Import System](technical-architecture.md#the-import-system) - How Claude Code loads context
- [Agent Context Structure](technical-architecture.md#agent-context-structure) - Domain specialist patterns
- [Command Context Structure](technical-architecture.md#command-context-structure) - Workflow definitions

**Component Development**:

- [Contributing to Components](contributing-code.md#contributing-to-components) - Agent, command, mode development
- [Adding New Agents](contributing-code.md#adding-new-agents) - Domain specialist creation
- [Adding New Commands](contributing-code.md#adding-new-commands) - Workflow pattern development
- [Extending the Framework](technical-architecture.md#extending-the-framework) - Framework expansion

### 🧪 Verification & Quality

**File Verification**:

- [Context File Verification](testing-debugging.md#context-file-verification) - File structure validation
- [File Validation](contributing-code.md#file-validation) - Context file verification methods

**Troubleshooting**:

- [Common Issues](testing-debugging.md#common-issues) - Activation and configuration problems
- [Troubleshooting Commands](testing-debugging.md#troubleshooting-commands) - Diagnostic procedures

### 🔧 Development Workflows

**Context File Development**:

- [Development Workflow](contributing-code.md#development-workflow) - Git workflow
- [Context File Guidelines](contributing-code.md#context-file-guidelines) - Standards and practices
- [Pull Request Process](contributing-code.md#pull-request-template) - Submission process

**Component Development**:

- [Agent Development](contributing-code.md#adding-new-agents) - Domain specialist creation
- [Command Development](contributing-code.md#adding-new-commands) - Workflow pattern creation
- [Mode Development](contributing-code.md#adding-new-modes) - Behavioral modification patterns

### 🛠️ MCP Integration

**MCP Configuration**:

- [MCP Server Configuration](technical-architecture.md#mcp-server-configuration) - External tool setup
- [MCP Server Verification](testing-debugging.md#mcp-server-verification) - Configuration validation

### 🚨 Support & Troubleshooting

**Common Issues**:

- [Commands Not Working](testing-debugging.md#issue-commands-not-working) - Context trigger problems
- [Agents Not Activating](testing-debugging.md#issue-agents-not-activating) - Activation issues
- [Context Not Loading](testing-debugging.md#issue-context-not-loading) - Loading problems

**Support Resources**:

- [Getting Help](contributing-code.md#getting-help) - Support channels
- [Issue Reporting](contributing-code.md#issue-reporting) - Bug reports and features

---

## Skill Level Pathways

### 🟢 Beginner Path (Understanding SuperClaude)

**Week 1: Foundation**

1. [Architecture Overview](technical-architecture.md#overview) - What SuperClaude is
2. [Installation Verification](testing-debugging.md#installation-verification) - Check your setup
3. [Context File Architecture](technical-architecture.md#context-file-architecture) - Directory structure

**Week 2: Basic Usage**

1. [How Claude Code Reads Context](technical-architecture.md#how-claude-code-reads-context) - Processing sequence
2. [Common Issues](testing-debugging.md#common-issues) - Troubleshooting basics
3. [Context File Guidelines](contributing-code.md#context-file-guidelines) - File standards

### 🟡 Intermediate Path (Contributing Context Files)

**Month 1: Context Development**

1. [Development Setup](contributing-code.md#development-setup) - Environment preparation
2. [Agent Context Structure](technical-architecture.md#agent-context-structure) - Domain specialists
3. [Command Context Structure](technical-architecture.md#command-context-structure) - Workflow patterns

**Month 2: Component Creation**

1. [Adding New Agents](contributing-code.md#adding-new-agents) - Domain specialist development
2. [Adding New Commands](contributing-code.md#adding-new-commands) - Workflow creation
3. [File Validation](contributing-code.md#file-validation) - Context verification

### 🔴 Advanced Path (Framework Extension)

**Advanced Understanding**

1. [The Import System](technical-architecture.md#the-import-system) - Context loading mechanics
2. [Extending the Framework](technical-architecture.md#extending-the-framework) - Framework expansion
3. [MCP Server Configuration](technical-architecture.md#mcp-server-configuration) - External tool integration

---

## Reference Materials

### 📚 Key Concepts

**Framework Fundamentals**:

- Context-Oriented Configuration Framework
- Agent Domain Specialists  
- Command Workflow Patterns
- Mode Behavioral Modifications
- MCP Integration Patterns

### 🔗 Cross-References

**Development → Architecture**:

- [Context File Guidelines](contributing-code.md#context-file-guidelines) → [Context File Architecture](technical-architecture.md#context-file-architecture)
- [Adding Components](contributing-code.md#contributing-to-components) → [Agent/Command Structure](technical-architecture.md#agent-context-structure)

**Development → Verification**:

- [Development Workflow](contributing-code.md#development-workflow) → [File Verification](testing-debugging.md#context-file-verification)
- [File Validation](contributing-code.md#file-validation) → [Installation Verification](testing-debugging.md#installation-verification)

**Architecture → Verification**:

- [How Claude Code Reads Context](technical-architecture.md#how-claude-code-reads-context) → [Troubleshooting](testing-debugging.md#common-issues)
- [MCP Configuration](technical-architecture.md#mcp-server-configuration) → [MCP Verification](testing-debugging.md#mcp-server-verification)

---

## Quality Standards

### ✅ Documentation Accuracy

- **Technical Precision**: All examples reflect SuperClaude reality (context files, not software)
- **Command Accuracy**: Correct Python module execution paths and Claude Code context triggers
- **No Fiction**: Removed all references to non-existent testing frameworks and performance systems

### ✅ Content Focus

- **Context Files**: Documentation centers on .md instruction files and Claude Code behavior
- **File Verification**: Practical approaches to validating context file installation and structure
- **Real Workflows**: Actual development processes for context file contribution

### ✅ User Experience

- **Clear Progression**: Skill-based learning paths from understanding to contribution
- **Practical Examples**: Working context file examples and Claude Code integration
- **Support Integration**: Clear guidance to help resources for real issues

---

## Usage Guidelines

### For Contributors

1. **Start with**: [Development Setup](contributing-code.md#development-setup)
2. **Context Development**: Follow [Context File Guidelines](contributing-code.md#context-file-guidelines)
3. **Validation**: Use [File Validation](contributing-code.md#file-validation)
4. **Support**: Reference [Getting Help](contributing-code.md#getting-help)

### For Architects

1. **System Understanding**: [Context File Architecture](technical-architecture.md#context-file-architecture)
2. **Component Patterns**: [Agent and Command Structure](technical-architecture.md#agent-context-structure)
3. **Extension**: [Extending the Framework](technical-architecture.md#extending-the-framework)
4. **Integration**: [MCP Configuration](technical-architecture.md#mcp-server-configuration)

### For Verification

1. **Installation Check**: [Installation Verification](testing-debugging.md#installation-verification)
2. **File Validation**: [Context File Verification](testing-debugging.md#context-file-verification)
3. **Troubleshooting**: [Common Issues](testing-debugging.md#common-issues)
4. **Diagnostics**: [Troubleshooting Commands](testing-debugging.md#troubleshooting-commands)

This comprehensive index reflects the reality of SuperClaude as a context-oriented configuration framework, focusing on practical context file development and Claude Code integration.
