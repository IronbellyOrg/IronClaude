# IronClaude

IronClaude is the current functional identity of this repository: a Claude Code–focused engineering framework for running structured workflows around planning, task execution, validation, auditing, and research.

Under the hood, much of the package and CLI surface still uses the historical `superclaude` name. In practice, this repository should be understood as **IronClaude evolving from the SuperClaude codebase**.

## What IronClaude does

IronClaude provides a working framework for:

- structured Claude Code commands, skills, and agents
- repeatable CLI pipelines for roadmap, tasklist, sprint, audit, and related workflows
- pytest-based validation and evaluation patterns
- evidence-first development with confidence checks and self-checking patterns
- MCP-assisted codebase analysis, research, and orchestration

## Current naming reality

This repository currently has two layers of identity:

- **Project identity**: IronClaude
- **Implementation/package identity**: `superclaude`

That means you will still see names like these in the codebase:

- Python package: `superclaude`
- CLI command: `superclaude`
- source tree: `src/superclaude/`
- pytest plugin entry point: `superclaude.pytest_plugin`

The README reflects the product/function of the repo first, while preserving the current technical names contributors still need to use.

## Highlights

- **CLI-driven workflows** for roadmap, tasklist, sprint, audit, and validation
- **Claude Code asset distribution** through commands, agents, and skills
- **PM-agent patterns** for confidence, self-check, and reflexion
- **MCP-aware development** with integrations such as Auggie, Serena, Tavily, Context7, and Sequential
- **Contributor workflow support** with source/dev-mirror sync between `src/superclaude/` and `.claude/`

## Repository purpose

This repository serves as:

- the source of truth for IronClaude’s current workflow framework
- the Python package implementation that still ships as `superclaude`
- the home of the `superclaude` CLI
- the implementation of the auto-loaded pytest plugin
- the source for distributable Claude Code commands, agents, and skills
- a workspace for generated docs, release/process artifacts, and evaluation work

## Installation

### Install the current package/CLI

The install surface still uses the historical package name:

```bash
pipx install superclaude
superclaude install
```

This installs the package and then installs its framework assets into your Claude Code directory.

### Install from source for development

This repository uses **UV** for Python operations.

```bash
git clone https://github.com/IronbellyOrg/IronClaude
cd IronClaude
make dev
make verify
```

## Quick start

### Core CLI commands

```bash
superclaude --version
superclaude doctor
superclaude install
superclaude mcp --list
```

### Run workflow pipelines

```bash
superclaude sprint run <tasklist-index.md>
superclaude roadmap run <spec.md>
superclaude roadmap validate <output-dir>
superclaude tasklist run <roadmap-dir>
```

### Run tests

```bash
make test
uv run pytest tests/pm_agent/ -v
uv run pytest -m confidence_check
```

## Core concepts

### 1. CLI and pipelines

The active CLI entry point is `superclaude`, implemented in `src/superclaude/cli/main.py`.

Key workflow areas include:

- sprint execution
- roadmap generation and validation
- tasklist generation
- audit and cleanup audit flows
- MCP installation and diagnostics

### 2. Pytest plugin

The package registers an auto-loaded pytest plugin via `pyproject.toml`.

It provides fixtures such as:

- `confidence_checker`
- `self_check_protocol`
- `reflexion_pattern`
- `token_budget`
- `pm_context`

It also exposes workflow-oriented markers including `confidence_check`, `self_check`, and `reflexion`.

### 3. PM-agent patterns

A major part of IronClaude’s operating model lives in `src/superclaude/pm_agent/`:

- **ConfidenceChecker** — assess confidence before implementation
- **SelfCheckProtocol** — validate implementation with evidence after changes
- **ReflexionPattern** — capture learning from errors and prevent repeats

### 4. Source of truth vs dev mirrors

For distributable framework assets, **`src/superclaude/` remains the source of truth**.

The `.claude/` directory contains development mirrors used directly by Claude Code during local iteration. When editing commands, agents, or skills, update `src/superclaude/` first and then sync to `.claude/`.

## Repository structure

```text
src/superclaude/         Canonical Python package and framework source
├── cli/                 CLI commands and pipeline entrypoints
├── pm_agent/            Confidence, self-check, reflexion patterns
├── execution/           Parallel execution and reflection helpers
├── commands/            Slash command definitions
├── agents/              Agent definition source files
├── skills/              Skill packages and support assets
├── core/                Framework rules and principles
└── pytest_plugin.py     Auto-loaded pytest integration

.claude/                 Dev mirrors used by Claude Code
plugins/                 Distribution/plugin artifacts
scripts/                 Build, analysis, and maintenance scripts
tests/                   Pytest suite and eval coverage
docs/                    User, developer, reference, and generated docs
```

## Development workflow

### Common commands

```bash
make dev                # Install editable package + dev dependencies
make verify             # Verify package, plugin, and health checks
make test               # Run the full test suite
make lint               # Run ruff checks
make format             # Format code with ruff
make doctor             # Run health diagnostics
make sync-dev           # Sync src/superclaude/ -> .claude/
make verify-sync        # Check src/ and .claude/ are in sync
make build-plugin       # Build plugin artifacts into dist/
make clean              # Remove build artifacts
```

### Working rules

- Use **UV** for Python commands
- Treat `src/superclaude/` as canonical until a code/package rename happens
- Run `make sync-dev` after editing distributable components
- Run `make verify-sync` before committing component changes
- Prefer evidence-backed changes validated by tests, docs, or real artifacts

## Documentation map

For deeper context, start with:

- `CLAUDE.md` — repository-specific workflow and contribution rules
- `PLANNING.md` — architecture decisions and constraints
- `TASK.md` — current priorities and active work
- `KNOWLEDGE.md` — accumulated findings and troubleshooting context
- `PROJECT_INDEX.md` — high-level repository index
- `docs/developer-guide/` — contributor and architecture guidance
- `docs/reference/` — reference material

## MCP integrations

IronClaude is built to work with MCP-assisted workflows.

Common integrations referenced in this repository include:

- Auggie
- Serena
- Tavily
- Context7
- Sequential
- Playwright
- Magic
- Chrome DevTools
- Mindbase

Inspect MCP-related configuration with:

```bash
superclaude mcp
superclaude mcp --list
```

## Contributing

1. Create a feature or fix branch.
2. Make changes in `src/superclaude/` for distributable assets.
3. Sync development mirrors when needed.
4. Run verification and test commands.
5. Use conventional commits.

If you work on commands, agents, or skills, make sure the package source and `.claude/` mirrors stay aligned.

## Requirements

- Python `>=3.10`
- UV for development workflows
- Claude Code for command, skill, and agent consumption

## License

MIT
