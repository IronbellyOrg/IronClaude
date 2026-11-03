# SuperClaude Framework Developer Guide

A documentation suite for understanding and extending the SuperClaude Context-Oriented Configuration Framework.

## Documentation Overview

This Developer Guide provides documentation for understanding SuperClaude's context architecture and how to extend it:

### [Contributing Code Guide](contributing-code.md)

**Purpose**: Guidelines for contributing context files and framework improvements  
**Audience**: Contributors and framework maintainers  
**Key Topics**: Adding context files, naming conventions, documentation standards

### [Context Architecture Guide](technical-architecture.md)

**Purpose**: Understanding how context files work and are structured  
**Audience**: Anyone wanting to understand or extend SuperClaude  
**Key Topics**: Context file structure, import system, agent/command patterns

### [Verification & Troubleshooting Guide](testing-debugging.md)

**Purpose**: Verifying installation and troubleshooting context file issues  
**Audience**: Users and maintainers  
**Key Topics**: File verification, common issues, diagnostic commands

### [Documentation Index](documentation-index.md)

**Purpose**: Comprehensive navigation guide and topic-based organization  
**Audience**: All users seeking efficient information discovery  
**Key Features**: Skill level pathways, cross-references, quality validation, usage guidelines

## Quick Navigation

### For New Contributors

1. Start with [Contributing Code Guide](contributing-code.md#development-setup) for environment setup
2. Review [Technical Architecture Guide](technical-architecture.md#context-file-architecture) for system understanding
3. Use [Testing & Debugging Guide](testing-debugging.md#installation-verification) for testing basics

### For System Architects

1. Begin with [Technical Architecture Guide](technical-architecture.md) for complete system design
2. Reference [Contributing Code Guide](contributing-code.md#architecture-overview) for component patterns
3. Review [Testing & Debugging Guide](testing-debugging.md#running-the-test-suite) for the test suite

### For Testing Engineers

1. Start with [Testing & Debugging Guide](testing-debugging.md) for comprehensive testing procedures
2. Reference [Contributing Code Guide](contributing-code.md#development-workflow) for development integration
3. Use [Technical Architecture Guide](technical-architecture.md#important-clarifications) for what runs code and what is only context

### Technical Notes

- [Codegraph Integration](codegraph-integration.md): pinned codegraph download, MCP registration, the auto-index hook and the MCP retire step
- [Session Memory](session-memory.md): the file-based `.superclaude/memory/` store behind `/sc:save` and `/sc:load`
- [Review Severity Rule](review-severity-rule.md): blocking vs minor findings and the two-fix-cycle limit
- [Release Procedure](release-procedure.md): go/no-go checks, release notes, tag and GitHub release

## Key Framework Concepts

### Context Files and the CLI

SuperClaude has two parts. Most of it is `.md` instruction files (core files, commands, agents, skills) that Claude Code reads to change its behavior. The Python package also ships the `superclaude` CLI: `install`, `update`, `doctor` and `mcp` set up and check the installation, and commands such as `sprint`, `roadmap` and `eval` run multi-step pipelines. Run `superclaude --help` for the full list.

`/sc:` commands are typed in a Claude Code conversation, not in a terminal. `superclaude <command>` is typed in a terminal.

### Agent Context Files

Specialized instruction sets that provide domain expertise when invoked with `@agent-[name]` or chosen by Claude Code from the agent's `description`.

### Command Context Files

Workflow instructions triggered by typing `/sc:[command]` in a Claude Code conversation. They guide Claude Code through structured development tasks; some of them call the `superclaude` CLI.

### MCP Integration

External tools (actual software) that can be configured to provide additional capabilities like documentation lookup or code analysis.

### Session Memory

`/sc:save` and `/sc:load` keep session context in plain markdown files under `<project>/.superclaude/memory/`, so a later conversation can pick up where an earlier one stopped.

## What SuperClaude Contains

- **Instructions**: Core files, commands, agents and skills are `.md` files Claude Code reads; nothing enforces them in code unless a workflow calls a CLI pipeline or a hook applies
- **Code**: The `superclaude` CLI, its pipelines and the hook scripts are Python and shell code
- **Tests**: The repository has a pytest suite (`make test`)
- **Persistent memory**: Session memory is stored in files, not in the conversation

## Getting Started

### Prerequisites

- Python 3.10+
- Claude Code installed
- Optional: Node.js 18+ for npm-based MCP servers

### Understanding the Framework

```bash
# Check installation
ls ~/.claude/
# You'll see core files and the commands/, agents/, skills/ and hooks/ folders

# View a command context
cat ~/.claude/commands/sc/implement.md
# You'll see instructions for Claude

# View an agent context
cat ~/.claude/agents/python-expert.md
# You'll see expertise definitions
```

### Extending SuperClaude

1. **Add Commands**: Create new `.md` files in `~/.claude/commands/sc/` (they appear as `/sc:<name>`)
2. **Add Agents**: Create new `.md` files in `~/.claude/agents/`

To ship a command or agent with the package, add it under `src/superclaude/` instead and follow the [Contributing Code Guide](contributing-code.md).

## Support and Resources

### Documentation Issues

- **Broken Links**: Report cross-reference issues in GitHub issues
- **Unclear Content**: Request clarification through GitHub discussions
- **Missing Information**: Suggest improvements through pull requests

### Development Support

- **Technical Questions**: Use GitHub discussions for architecture and implementation questions
- **Bug Reports**: Submit detailed issues with reproduction steps
- **Feature Requests**: Propose enhancements through GitHub issues

### Community Resources

- **[GitHub Repository](https://github.com/IronbellyOrg/IronClaude)**: Main development and collaboration hub

## Contributing to Documentation

We welcome contributions to improve documentation quality, accuracy, and completeness:

### Documentation Standards

- **Clarity**: Write for your target audience skill level
- **Consistency**: Follow established terminology and formatting
- **Completeness**: Provide working examples and complete procedures
- **Cross-References**: Link related concepts across documents

### Submission Process

1. Fork the repository and create a feature branch
2. Make documentation improvements following our standards
3. Test all code examples and verify cross-references
4. Submit pull request with clear description of changes

---

**SuperClaude Framework**: Building the future of AI-assisted development through intelligent orchestration and behavioral programming.

For the latest updates and community discussions, visit our [GitHub repository](https://github.com/IronbellyOrg/IronClaude).
