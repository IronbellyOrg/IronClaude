# Project Index: SuperClaude (IronClaude fork)

Generated: 2026-11-05 (mode=quick: tests not analyzed)
Package: `superclaude` 5.0.0 (pyproject.toml) | Python >=3.10 | Build: hatchling
Version files that disagree with pyproject: `VERSION` = 3.7, `package.json` = 4.1.7.
Excluded: `.dev/`, `.claude/`, `.venv/`, `node_modules/`, `dist/`, `.git/`.

## Project Structure

```text
src/superclaude/          # Source of truth for everything distributable (358 .py files)
├── cli/                  # `superclaude` and `ic` CLIs (click); 12 sub-packages
├── core/                 # 11 framework .md files (installed to ~/.claude/)
├── commands/             # 46 slash command .md files
├── agents/               # 48 agent definition .md files
├── skills/               # 39 skill packages (SKILL.md + refs/rules/templates/scripts)
├── modes/                # 7 MODE_*.md behavioral modes
├── mcp/  hooks/  rules/  templates/  output-styles/  contracts/  examples/  scripts/
├── pm_agent/             # confidence, self_check, reflexion, token_budget
├── execution/            # parallel, reflection, self_correction
├── pr_submit/            # PR-review auto-remediation state machine
├── tools/                # arch_lint.py
├── compression.py  __version__.py
└── pytest_plugin.py      # auto-loaded pytest plugin
plugins/superclaude/      # plugin packaging mirror (120 files)
tests/                    # 23 test sub-folders (skipped in quick mode)
docs/                     # 132 .md files in 17 folders
scripts/                  # 24 helper scripts
agents/ commands/ skills/ superclaude/ repro/   # legacy root-level tracked folders
```

## Entry Points

- CLI: `src/superclaude/cli/main.py` - `superclaude` group; sub-groups sprint, roadmap, cleanup-audit, tasklist, cli-portify, prd, eval, swarm, recommend, init-lite, reflect
- CLI: `src/superclaude/cli/ic.py` - `ic` command
- Pytest plugin: `src/superclaude/pytest_plugin.py` (entry point `pytest11`)
- Install: `src/superclaude/cli/install_*.py` (core, commands, agents, skills, hooks, mcp, templates, ccsession, codegraph, user_setup)
- Diagnostics: `src/superclaude/cli/doctor.py`

## Core Modules

- `cli/sprint`, `cli/roadmap`, `cli/tasklist`, `cli/pipeline`: pipeline CLIs
- `cli/audit`, `cli/cleanup_audit`: repository audit passes
- `cli/cli_portify`, `cli/eval`, `cli/swarm`, `cli/reflect`, `cli/recommend`, `cli/prd`: feature CLIs
- `pm_agent/`: ConfidenceChecker, SelfCheckProtocol, ReflexionPattern
- `execution/parallel.py`: wave, checkpoint, wave execution
- `pr_submit/`: PR monitor state machine

## Configuration

- `pyproject.toml`: package, deps, pytest options, entry points
- `Makefile`: install, test, lint, format, sync-dev, verify-sync, build-plugin, verify-deps, lint-architecture, eval-skill, reflect-eval
- `.pre-commit-config.yaml`: hooks incl. verify-sync
- `.github/workflows/`: test.yml, boundary-guard.yml, contract3-generator-constraint-lint.yml
- `CLAUDE.md`, `AGENTS.md`: project instructions

## Documentation

- `README.md`, `CONTRIBUTING.md`, `SECURITY.md`, `CHANGELOG.md`, `KNOWLEDGE.md`
- `docs/`: user-guide, developer-guide, getting-started, reference, guides, mcp, swarm, eval, releases, onboarding, designs, testing
- `src/superclaude/core/HOW-WE-WORK.md`: routing guide; `WORKER-CONTRACT.md`: Orca worker rules

## Key Dependencies

- pytest>=7.0, click>=8.0, rich>=13.0, pyyaml>=6.0, jsonschema>=4.0, jinja2>=3.0, pexpect>=4.9, httpx>=0.27
- Dev: pytest-cov, pytest-benchmark, scipy, ruff==0.15.20, mypy

## Quick Start

1. `make install`
2. `uv run superclaude install`
3. `make test` (or `uv run pytest tests/<folder> -v`)
4. After editing `src/superclaude/{skills,agents,commands}`: `make sync-dev && make verify-sync`
