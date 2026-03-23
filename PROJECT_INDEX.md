# Project Index: SuperClaude Framework

**Generated**: 2026-03-23
**Version**: 4.2.0
**Package**: `superclaude`
**Python**: >=3.10
**Build**: hatchling (PEP 517)
**License**: MIT

---

## Project Structure

```
SuperClaude_Framework/
├── src/superclaude/              # Python package — source of truth
│   ├── __init__.py               # Exports: ConfidenceChecker, SelfCheckProtocol, ReflexionPattern
│   ├── __version__.py            # 4.2.0
│   ├── pytest_plugin.py          # Auto-loaded pytest integration (entry point: pytest11)
│   ├── cli/                      # CLI tool + pipeline runners
│   │   ├── main.py               # Click CLI entry point → `superclaude` command
│   │   ├── doctor.py             # Health check diagnostics
│   │   ├── install_*.py          # Component installers (core, commands, agents, skills, mcp)
│   │   ├── sprint/               # Sprint pipeline (16 modules)
│   │   ├── roadmap/              # Roadmap pipeline (24 modules)
│   │   ├── tasklist/             # Tasklist pipeline (6 modules)
│   │   ├── pipeline/             # Shared pipeline infrastructure (24 modules)
│   │   ├── audit/                # Cleanup audit pipeline (42 modules)
│   │   ├── cleanup_audit/        # Cleanup audit runner (13 modules)
│   │   └── cli_portify/          # Portify pipeline (22 modules + steps/)
│   ├── pm_agent/                 # PM Agent core patterns
│   │   ├── confidence.py         # Pre-execution confidence (≥90% proceed)
│   │   ├── self_check.py         # Post-implementation validation
│   │   ├── reflexion.py          # Error learning + cross-session matching
│   │   └── token_budget.py       # Token budget allocation
│   ├── execution/                # Execution patterns
│   │   ├── parallel.py           # Wave → Checkpoint → Wave (3.5x speedup)
│   │   ├── reflection.py         # Reflection utilities
│   │   └── self_correction.py    # Self-correction logic
│   ├── core/                     # Framework definition files (13 .md)
│   │   ├── RULES.md              # Behavioral rules
│   │   ├── PRINCIPLES.md         # Engineering principles
│   │   ├── PERSONAS.md           # 9 personas (architect…devops)
│   │   ├── COMMANDS.md           # Command registry
│   │   ├── FLAGS.md              # Flag definitions
│   │   ├── MCP.md                # MCP integration guide
│   │   ├── MODES.md              # Operating modes
│   │   └── ORCHESTRATOR.md       # Orchestration rules
│   ├── commands/                 # Slash command definitions (38 .md files)
│   ├── agents/                   # Agent definitions (29 .md files)
│   ├── skills/                   # Skill packages (13 directories)
│   │   ├── confidence-check/     # SKILL.md + confidence.ts
│   │   ├── sc-adversarial-protocol/
│   │   ├── sc-cleanup-audit-protocol/
│   │   ├── sc-cli-portify-protocol/
│   │   ├── sc-pm-protocol/
│   │   ├── sc-recommend-protocol/
│   │   ├── sc-release-split-protocol/
│   │   ├── sc-review-translation-protocol/
│   │   ├── sc-roadmap-protocol/
│   │   ├── sc-task-unified-protocol/
│   │   ├── sc-tasklist-protocol/
│   │   └── sc-validate-tests-protocol/
│   ├── mcp/                      # MCP server configs + docs (10 servers)
│   │   ├── configs/              # JSON configs per server
│   │   └── MCP_*.md              # Per-server documentation
│   ├── modes/                    # Operating mode definitions (7 modes)
│   ├── hooks/                    # Hook definitions (hooks.json)
│   ├── examples/                 # Example templates
│   └── scripts/                  # Internal scripts
├── tests/                        # Test suite
│   ├── conftest.py               # Shared fixtures
│   ├── unit/                     # Unit tests
│   ├── integration/              # Integration tests
│   ├── sprint/                   # Sprint pipeline tests
│   ├── pipeline/                 # Pipeline tests
│   ├── roadmap/                  # Roadmap tests
│   ├── tasklist/                 # Tasklist tests
│   ├── audit/                    # Audit pipeline tests
│   ├── cli_portify/              # Portify tests
│   └── headless-adversarial/     # Adversarial pipeline tests
├── .claude/                      # Dev copies (synced from src/)
│   ├── settings.json
│   ├── commands/sc/              # Active slash commands
│   ├── agents/                   # Active agent definitions
│   └── skills/                   # Active skill packages
├── docs/                         # Documentation
│   ├── user-guide/               # English user guide
│   ├── user-guide-jp/            # Japanese
│   ├── user-guide-kr/            # Korean
│   ├── user-guide-zh/            # Chinese
│   ├── developer-guide/          # Developer docs
│   ├── reference/                # API reference
│   ├── architecture/             # Architecture decisions
│   ├── research/                 # Research notes
│   ├── generated/                # CLI pipeline artifacts
│   ├── mcp/                      # MCP documentation
│   ├── testing/                  # Testing guides
│   ├── troubleshooting/          # Troubleshooting
│   └── agents/                   # Agent documentation
├── scripts/                      # Dev/ops scripts
│   ├── eval_*.py                 # Evaluation runners
│   ├── ab_test_workflows.py      # A/B workflow testing
│   ├── analyze_workflow_metrics.py
│   ├── build_superclaude_plugin.py
│   ├── sync_from_framework.py    # Framework sync
│   └── validators/               # Validation scripts
├── .dev/                         # Release management
│   └── releases/                 # Current + backlog releases
├── .github/                      # CI/CD workflows + templates
├── plugins/                      # Plugin artifacts
├── remediation/                  # Remediation tracking
└── .serena/                      # Serena MCP project config
```

---

## Entry Points

### CLI: `superclaude`
- **Source**: `src/superclaude/cli/main.py:main`
- **Framework**: Click
- **Subcommands**: `install`, `mcp`, `doctor`, `sprint run`, `roadmap run`, `roadmap validate`, `tasklist run`

### Pytest Plugin
- **Auto-loaded**: via `[project.entry-points.pytest11]`
- **Source**: `src/superclaude/pytest_plugin.py`
- **Fixtures**: `confidence_checker`, `self_check_protocol`, `reflexion_pattern`, `token_budget`, `pm_context`
- **Auto-markers**: tests in `/unit/` → `unit`, tests in `/integration/` → `integration`

---

## Core Subsystems

### 1. PM Agent (`src/superclaude/pm_agent/`)
Three-pattern system for AI-guided development:

| Pattern | File | Purpose |
|---------|------|---------|
| **ConfidenceChecker** | `confidence.py` | Pre-execution assessment. ≥90% proceed, 70-89% present alternatives, <70% ask |
| **SelfCheckProtocol** | `self_check.py` | Post-implementation evidence-based validation |
| **ReflexionPattern** | `reflexion.py` | Error learning, cross-session pattern matching |
| **TokenBudget** | `token_budget.py` | Token allocation: simple=200, medium=1000, complex=2500 |

### 2. CLI Pipelines (`src/superclaude/cli/`)

| Pipeline | Dir | Modules | Purpose |
|----------|-----|---------|---------|
| **Sprint** | `cli/sprint/` | 16 | Supervised task execution with KPI tracking, TUI, tmux |
| **Roadmap** | `cli/roadmap/` | 24 | Spec → roadmap generation with convergence, remediation |
| **Tasklist** | `cli/tasklist/` | 6 | Roadmap → sprint-compatible tasklist bundles |
| **Pipeline** | `cli/pipeline/` | 24 | Shared infrastructure: gates, FMEA, dataflow, invariants |
| **Audit** | `cli/audit/` | 42 | Multi-pass repo audit with evidence gates |
| **Cleanup Audit** | `cli/cleanup_audit/` | 13 | Audit runner with diagnostics + TUI |
| **CLI Portify** | `cli/cli_portify/` | 22+8 | Convert inference workflows → programmatic pipelines |

### 3. Execution Engine (`src/superclaude/execution/`)
- **Parallel**: Wave → Checkpoint → Wave pattern (3.5x speedup)
- **Reflection**: Post-execution analysis
- **Self-correction**: Automated error recovery

### 4. Framework Core (`src/superclaude/core/`)
13 markdown files defining behavioral rules, personas, commands, flags, MCP integration, orchestration, and operating modes.

### 5. Slash Commands (`src/superclaude/commands/`)
38 command definitions. Key commands:
- `sc.md` — Dispatcher
- `task-unified.md` — Unified task execution with MCP compliance
- `pm.md` — Project manager orchestration
- `roadmap.md`, `tasklist.md`, `sprint.md` — Pipeline commands
- `adversarial.md` — Structured debate pipeline
- `cleanup-audit.md` — Repository audit
- `cli-portify.md` — Workflow portification
- `research.md`, `analyze.md`, `implement.md`, `test.md`, `build.md`

### 6. Agents (`src/superclaude/agents/`)
29 agent definitions for Claude Code subagent delegation:

| Category | Agents |
|----------|--------|
| **Audit** | audit-scanner, audit-analyzer, audit-comparator, audit-consolidator, audit-validator |
| **Architecture** | system-architect, backend-architect, frontend-architect, devops-architect |
| **Quality** | quality-engineer, performance-engineer, security-engineer |
| **Research** | deep-research, deep-research-agent |
| **Development** | python-expert, refactoring-expert, merge-executor |
| **Analysis** | root-cause-analyst, requirements-analyst |
| **Communication** | technical-writer, learning-guide, socratic-mentor |
| **Orchestration** | pm-agent, debate-orchestrator, self-review, repo-index |
| **Domain** | business-panel-experts |

### 7. Skills (`src/superclaude/skills/`)
13 skill packages, each containing `SKILL.md` + optional `refs/`, `rules/`, `templates/`, `scripts/`:

| Skill | Purpose |
|-------|---------|
| `confidence-check` | Pre-implementation confidence assessment |
| `sc-adversarial-protocol` | Debate, comparison, merge pipeline |
| `sc-cleanup-audit-protocol` | Multi-pass repo audit |
| `sc-cli-portify-protocol` | Workflow → CLI pipeline conversion |
| `sc-pm-protocol` | PM agent PDCA orchestration |
| `sc-recommend-protocol` | Command recommendation engine |
| `sc-release-split-protocol` | Release split analysis |
| `sc-review-translation-protocol` | Localization review |
| `sc-roadmap-protocol` | Roadmap generation |
| `sc-task-unified-protocol` | Unified task execution |
| `sc-tasklist-protocol` | Roadmap → tasklist generation |
| `sc-validate-tests-protocol` | Tier classification validation |

### 8. MCP Servers (`src/superclaude/mcp/`)
10 server integrations with JSON configs:

| Server | Purpose |
|--------|---------|
| **Airis Gateway** | Unified MCP management (60+ tools) |
| **Auggie** | Codebase retrieval + context |
| **Tavily** | Web search |
| **Context7** | Official library docs |
| **Sequential** | Multi-step reasoning |
| **Serena** | Symbol navigation + project memory |
| **Playwright** | Browser automation |
| **Magic** | UI component generation |
| **Chrome DevTools** | Performance profiling |
| **Mindbase** | Cross-session learning |

---

## Dependencies

**Runtime**: pytest >=7.0, click >=8.0, rich >=13.0, pyyaml >=6.0
**Dev**: pytest-cov, pytest-benchmark, scipy, black, ruff, mypy

---

## Test Organization

| Directory | Scope | Key Markers |
|-----------|-------|-------------|
| `tests/unit/` | Unit tests | `unit` |
| `tests/integration/` | Integration | `integration` |
| `tests/sprint/` | Sprint pipeline | `diagnostic`, `e2e_trailing`, `backward_compat` |
| `tests/pipeline/` | Pipeline infra | `diagnostic_l0`…`l3` |
| `tests/roadmap/` | Roadmap pipeline | — |
| `tests/tasklist/` | Tasklist pipeline | — |
| `tests/audit/` | Audit pipeline | — |
| `tests/cli_portify/` | Portify pipeline | — |
| `tests/headless-adversarial/` | Adversarial | — |

Custom pytest markers: `confidence_check`, `self_check`, `reflexion`, `complexity(level)`, `diagnostic`, `e2e_trailing`, `backward_compat`, `property_based`, `nfr_benchmark`, `gate_performance`, `thread_safety`, `agent_regression`

---

## Development Commands

```bash
make dev              # Install editable + dev deps
make test             # Full test suite
make lint             # Ruff linter
make format           # Ruff formatter
make doctor           # Health check
make sync-dev         # src/ → .claude/
make verify-sync      # Confirm sync
make build-plugin     # Build plugin artifacts
make clean            # Remove build artifacts
```

---

## Git Workflow

- **Branches**: `master` (production) ← `integration` (testing) ← `feature/*`, `fix/*`, `docs/*`
- **Commits**: Conventional commits (`feat:`, `fix:`, `docs:`, etc.)
- **Current branch**: `v3.0-v3.2-Fidelity`

---

## Key Configuration Files

| File | Purpose |
|------|---------|
| `pyproject.toml` | Build config, dependencies, tool settings |
| `Makefile` | Development commands |
| `.pre-commit-config.yaml` | Pre-commit hooks |
| `.gitmodules` | Git submodules |
| `CODEOWNERS` | Code ownership |
| `return-contract.yaml` | Return contract definitions |
| `PLANNING.md` | Architecture decisions, absolute rules |
| `KNOWLEDGE.md` | Accumulated insights |
| `CLAUDE.md` | Claude Code project instructions |
