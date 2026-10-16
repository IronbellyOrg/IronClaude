# Project Index: SuperClaude (IronClaude fork)

Generated: 2026-10-14
Package: `superclaude` version 4.3.5 (from pyproject.toml) | Python >=3.10 | Build: hatchling

Excluded from this index: `.dev/`, `.claude/`, `.venv/`, `node_modules/`, `dist/`.

## Project Structure

```text
src/superclaude/          # Source of truth for all distributable components
├── cli/                  # `superclaude` and `ic` CLI (click)
├── core/                 # 8 core framework .md files (installed to ~/.claude/)
├── commands/             # 43 slash command .md files (+ README)
├── agents/               # 43 agent definition .md files (+ README)
├── skills/               # 36 skill packages (SKILL.md + refs/rules/templates/scripts)
├── modes/                # 7 MODE_*.md behavioral modes
├── mcp/                  # MCP_*.md server docs + configs/
├── hooks/                # hooks.json + hook scripts
├── pm_agent/             # confidence, self_check, reflexion, token_budget
├── execution/            # parallel, reflection, self_correction
├── pr_submit/            # PR-review auto-remediation FSM
├── tools/                # arch_lint.py
├── rules/, templates/, output-styles/, contracts/, examples/, scripts/
└── pytest_plugin.py      # Auto-loaded pytest plugin
plugins/superclaude/      # Plugin packaging mirror
tests/                    # 727 test_*.py files
docs/                     # 96 .md files
scripts/                  # Build, eval, sync, verification helpers
```

## Entry Points

- CLI: `superclaude` -> `src/superclaude/cli/main.py:main`
  - Commands: `install`, `mcp`, `update`, `install-skill`, `doctor`, `version`
  - Groups: `sprint`, `roadmap`, `cleanup-audit`, `tasklist`, `cli-portify`, `prd`, `eval`, `swarm`, `recommend`, `init-lite`, `reflect`
- CLI: `ic` -> `src/superclaude/cli/ic.py:main`
- Pytest plugin: `superclaude.pytest_plugin` (entry point `pytest11`)

## Core Framework Files (`src/superclaude/core/`)

Exactly 8 files on disk:

- `BASH_INSPECTION_POLICY.md` - Bash inspection policy
- `BUSINESS_PANEL_EXAMPLES.md` - Business panel usage examples
- `BUSINESS_SYMBOLS.md` - Business panel symbol system
- `CLAUDE.md` - Core entry file loaded into ~/.claude/
- `HOW-WE-WORK.md` - Routing guide: which command or skill to use for each kind of work (read on demand, never @-imported)
- `PRINCIPLES.md` - Engineering principles
- `RESEARCH_CONFIG.md` - Deep research configuration
- `RULES.md` - Behavioral rules

## Core Python Modules

### pm_agent (`src/superclaude/pm_agent/`)
- `confidence.py` - ConfidenceChecker: >=90% proceed, 70-89% alternatives, <70% ask
- `self_check.py` - SelfCheckProtocol: evidence-based post-implementation validation
- `reflexion.py` - ReflexionPattern: error learning, cross-session matching
- `token_budget.py` - Token budget by complexity (200 / 1000 / 2500)

### execution (`src/superclaude/execution/`)
- `parallel.py` - Wave -> Checkpoint -> Wave parallel execution
- `reflection.py`, `self_correction.py` - Reflection and self-correction loops

### cli (`src/superclaude/cli/`)
- `install_core.py`, `install_commands.py`, `install_agents.py`, `install_skills.py`, `install_skill.py`, `install_hooks.py`, `install_mcp.py`, `install_templates.py`, `install_user_setup.py`, `install_ccsession.py` - installers
- `doctor.py` - health checks
- Subpackages: `sprint/`, `roadmap/`, `tasklist/`, `cli_portify/`, `cleanup_audit/`, `audit/`, `prd/`, `eval/`, `swarm/`, `recommend/`, `reflect/`, `pipeline/`

### pr_submit (`src/superclaude/pr_submit/`)
- `fsm.py`, `classifier.py`, `severity_router.py`, `loop_guard.py`, `recovery.py`, `ci.py` - PR-review monitor state machine

## Skills (36)

Including `sc-recommend`, `confidence-check`, `task`, `task-builder`, `roadmap`, `prd`, `tdd`, `tech-research`, `tech-reference`, and the `sc-*-protocol` family (adversarial, brainstorm, implement, pm, reflect, roadmap, tasklist, troubleshoot, workflow, and others).

## Configuration

- `pyproject.toml` - package metadata, entry points, ruff/pytest config
- `Makefile` - dev workflow targets
- `uv.lock` - locked dependencies
- `src/superclaude/hooks/hooks.json` - hook registrations
- `src/superclaude/cli/user_settings_defaults.json` - user settings defaults

## Documentation

- `README.md`, `CLAUDE.md`, `AGENTS.md`, `KNOWLEDGE.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, `SECURITY.md`
- `docs/getting-started/` - installation, quick start
- `docs/user-guide/` - commands, agents, modes, flags, MCP servers, sessions, eval pipeline, memory system
- `docs/developer-guide/` - architecture, contributing, testing/debugging, commands-skills-agents guide
- `docs/reference/` - diagnostics, troubleshooting, MCP server guide, deviation report format

## Tests

- 727 `test_*.py` files under `tests/`
- `tests/unit/` (20 files, auto-marked `unit`), `tests/integration/` (12 files, auto-marked `integration`)
- Feature suites: `sprint/`, `roadmap/`, `tasklist/`, `swarm/`, `recommend/`, `pr_submit/`, `cli_portify/`, `audit/`, `pipeline/`, `skills/`, `hooks/`, and others

## Key Dependencies

pytest>=7.0.0, click>=8.0.0, rich>=13.0.0, pyyaml>=6.0, jsonschema>=4.0.0, jinja2>=3.0, pexpect>=4.9, httpx>=0.27

## Quick Start

1. `make install` - editable install with dev extras (`uv pip install -e ".[dev]"`)
2. `make verify` - check package, version, and pytest plugin
3. `make test` - run the test suite (`uv run pytest`)
4. `make lint` / `make format` - ruff
5. `make sync-dev` then `make verify-sync` - mirror `src/superclaude/` components into `.claude/`
