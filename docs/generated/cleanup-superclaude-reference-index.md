# SuperClaude Reference Index

Generated: 2026-03-24

## Summary

- **Total files with references**: 2,713
- **Variant breakdown (files containing each)**:
  - `superclaude` (lowercase, package name): 2,347 files
  - `SuperClaude` (brand name): 653 files
  - `SuperClaude_Framework` (repo/org name): 914 files
  - `SuperClaude-Org` (GitHub org): 37 files
  - `SUPERCLAUDE` (uppercase): 31 files
  - `SuperClaude_Plugin` (plugin repo): 8 files
  - `super_claude` (snake_case): 0 files

### By category

| Category | File Count | Risk Level |
|----------|-----------|------------|
| CONFIG (pyproject.toml, Makefile, MANIFEST.in, setup.py, package.json, workflows) | 15 | CRITICAL |
| PACKAGE (src/superclaude/ non-CLI) | 46 | HIGH |
| CLI (src/superclaude/cli/) | 80 | HIGH |
| TEST (tests/) | 247 | MEDIUM |
| DOTCLAUDE (.claude/) | 49 | MEDIUM |
| DOCS (docs/) | 139 | LOW |
| DEV (.dev/) | 2,093 | LOW |
| OTHER (scripts, plugins, root files) | 48 | MIXED |

---

## CRITICAL: Config & Package Identity Files

These files define the package name, entry points, build system, and CI. Renaming here has the widest blast radius.

### pyproject.toml

| Line | Content | Reference Type |
|------|---------|----------------|
| 6 | `name = "superclaude"` | PACKAGE name |
| 57 | `Homepage = "https://github.com/SuperClaude-Org/SuperClaude_Framework"` | URL/ORG |
| 58 | `GitHub = "https://github.com/SuperClaude-Org/SuperClaude_Framework"` | URL/ORG |
| 59 | `"Bug Tracker" = "https://github.com/SuperClaude-Org/SuperClaude_Framework/issues"` | URL/ORG |
| 60 | `Documentation = "https://github.com/SuperClaude-Org/SuperClaude_Framework/blob/main/README.md"` | URL/ORG |
| 64 | `superclaude = "superclaude.cli.main:main"` | CLI entry point |
| 68 | `superclaude = "superclaude.pytest_plugin"` | Plugin entry point |
| 71 | `packages = ["src/superclaude"]` | MODULE path |
| 78 | `"src" = "superclaude/_src"` | MODULE path |
| 79 | `"plugins" = "superclaude/_plugins"` | MODULE path |
| 136 | `source = ["src/superclaude"]` | MODULE path |

### Makefile

| Line(s) | Context | Reference Type |
|---------|---------|----------------|
| 5 | `Installing SuperClaude Framework` | BRAND |
| 19, 32, 35, 38, 41 | `grep superclaude`, `import superclaude`, `superclaude --version`, `superclaude doctor` | COMMAND, MODULE |
| 64 | `PLUGIN_DIST := dist/plugins/superclaude` | MODULE path |
| 65 | `PLUGIN_REPO ?= ../SuperClaude_Plugin` | URL/ORG |
| 68-70 | `Build SuperClaude plugin` | BRAND |
| 76 | `SuperClaude_Plugin` | URL/ORG |
| 107-310 | Sync logic: `src/superclaude/` paths throughout | MODULE path (50+ refs) |
| 339 | `SuperClaude Framework - Available commands` | BRAND |
| 359-360 | `Build SuperClaude plugin` | BRAND |
| 366-371 | `Remove legacy SuperClaude files` | BRAND |

### MANIFEST.in

| Line(s) | Content | Reference Type |
|---------|---------|----------------|
| 10-19 | `recursive-include src/superclaude ...` (10 lines) | MODULE path |
| 20-30 | `recursive-include plugins/superclaude ...` (11 lines) | MODULE path |

### setup.py

| Line | Content | Reference Type |
|------|---------|----------------|
| 2 | `Setup.py for SuperClaude Framework` | BRAND |

### package.json

| Line | Content | Reference Type |
|------|---------|----------------|
| 2 | `"name": "@bifrost_inc/superclaude"` | PACKAGE name |
| 4 | `"description": "SuperClaude Framework NPM wrapper..."` | BRAND |
| 17 | `"name": "SuperClaude Org"` | URL/ORG |
| 18 | `"url": "https://github.com/SuperClaude-Org"` | URL/ORG |
| 22 | `"url": "git+https://github.com/SuperClaude-Org/SuperClaude_Framework.git"` | URL/ORG |
| 25 | `"url": "https://github.com/SuperClaude-Org/SuperClaude_Framework/issues"` | URL/ORG |
| 27 | `homepage URL: SuperClaude_Framework` | URL/ORG |
| 30 | `"superclaude"` keyword | PACKAGE |

### .pre-commit-config.yaml

| Line | Content | Reference Type |
|------|---------|----------------|
| 1 | `# SuperClaude Framework - Pre-commit Hooks` | BRAND |

### .github/FUNDING.yml

| Line | Content | Reference Type |
|------|---------|----------------|
| 4 | `patreon: # SuperClaude` | BRAND |
| 6 | `ko_fi: # superclaude` | BRAND |

### .github/workflows/publish-pypi.yml

| Line(s) | Context | Reference Type |
|---------|---------|----------------|
| 30 | PyPI URL: `pypi.org/p/SuperClaude` | PACKAGE name |
| 54-55 | `Checking SuperClaude package`, `ls src/superclaude/` | BRAND, MODULE |
| 72 | `from superclaude import __version__` | MODULE |
| 120-134 | Summary block: `SuperClaude Package Deployment`, `pip install SuperClaude` | BRAND, COMMAND |
| 159 | `SuperClaude` in pip install | COMMAND |
| 163-164 | `import superclaude`, `SuperClaude v{...}` | MODULE, BRAND |
| 168 | `subprocess.run(['SuperClaude', '--version']` | COMMAND |

### .github/workflows/test.yml

| Line(s) | Context | Reference Type |
|---------|---------|----------------|
| 43 | `import superclaude; print(f'SuperClaude ...')` | MODULE, BRAND |
| 53 | `pytest --cov=superclaude` | MODULE |
| 118 | `grep -q "superclaude"` plugin check | MODULE |
| 125 | `name: SuperClaude Doctor Check` | BRAND |
| 148 | `superclaude doctor --verbose` | COMMAND |

### .github/workflows/quick-check.yml

| Line | Content | Reference Type |
|------|---------|----------------|
| 45 | `grep -q "superclaude"` | MODULE |

### .github/workflows/pull-sync-framework.yml

| Line(s) | Context | Reference Type |
|---------|---------|----------------|
| 23 | `git ls-remote https://github.com/SuperClaude-Org/SuperClaude_Framework` | URL/ORG |
| 47 | `repository: SuperClaude-Org/SuperClaude_Framework` | URL/ORG |

### .github/workflows/readme-quality-check.yml

| Line | Content | Reference Type |
|------|---------|----------------|
| 42 | `SuperClaude Multi-language README Quality Checker` | BRAND |

---

## HIGH: Python Source Code (src/superclaude/ non-CLI)

Core package identity files -- changing these requires updating all imports.

### Entry Points & Identity

| File | Ref Count | Key References |
|------|-----------|----------------|
| `src/superclaude/__init__.py` | 1 | Docstring: `SuperClaude Framework` |
| `src/superclaude/__version__.py` | 1 | Docstring: `Version information for SuperClaude` |
| `src/superclaude/pytest_plugin.py` | 6 | Docstring, entry point name `superclaude`, marker registration, header |
| `src/superclaude/execution/__init__.py` | 2 | Docstring, import path `superclaude.execution` |

### Commands (src/superclaude/commands/)

| File | Ref Count | Reference Types |
|------|-----------|-----------------|
| `sc.md` | 7 | BRAND, COMMAND |
| `README.md` | 6 | BRAND, MODULE |
| `help.md` | 6 | BRAND, COMMAND |
| `cli-portify.md` | 5 | BRAND, MODULE |
| `tasklist.md` | 2 | COMMAND |
| `spec-panel.md` | 2 | COMMAND |
| `recommend.md` | 2 | COMMAND |
| `agent.md` | 2 | COMMAND |
| `spawn.md` | 1 | COMMAND |
| `index-repo.md` | 1 | COMMAND |
| `adversarial.md` | 1 | COMMAND |

### Skills (src/superclaude/skills/)

| File | Ref Count | Reference Types |
|------|-----------|-----------------|
| `sc-cli-portify-protocol/refs/code-templates.md` | 12 | MODULE, BRAND |
| `sc-cli-portify-protocol/SKILL.md` | 7 | MODULE, BRAND |
| `sc-cli-portify-protocol/decisions.yaml` | 6 | MODULE |
| `sc-adversarial-protocol/SKILL.md` | 6 | BRAND, MODULE |
| `sc-validate-roadmap-protocol/SKILL.md` | 4 | MODULE, COMMAND |
| `sc-cli-portify-protocol/refs/pipeline-spec.md` | 4 | MODULE |
| `sc-roadmap-protocol/refs/adversarial-integration.md` | 3 | MODULE |
| `sc-cli-portify-protocol/refs/analysis-protocol.md` | 3 | MODULE |
| `sc-tasklist-protocol/SKILL.md` | 2 | MODULE, COMMAND |
| `sc-roadmap-protocol/SKILL.md` | 2 | MODULE, COMMAND |
| `sc-release-split-protocol/SKILL.md` | 2 | MODULE |
| `sc-adversarial-protocol/refs/agent-specs.md` | 2 | MODULE |

### Agents (src/superclaude/agents/)

| File | Ref Count |
|------|-----------|
| `self-review.md` | 4 |
| `README.md` | 4 |
| `repo-index.md` | 3 |
| `deep-research.md` | 2 |
| `socratic-mentor.md` | 1 |

### Core Framework Files (src/superclaude/core/)

| File | Ref Count |
|------|-----------|
| `CLAUDE.md` | 11 |
| `MODES.md` | 4 |
| `ORCHESTRATOR.md` | 2 |
| `MCP.md` | 2 |
| `COMMANDS.md` | 2 |
| `PERSONAS.md` | 1 |
| `FLAGS.md` | 1 |
| `BUSINESS_PANEL_EXAMPLES.md` | 1 |

### Other Package Files

| File | Ref Count |
|------|-----------|
| `scripts/README.md` | 4 |
| `hooks/README.md` | 4 |
| `scripts/clean_command_names.py` | 2 |
| `scripts/session-init.sh` | 1 |
| `modes/MODE_Introspection.md` | 1 |
| `modes/MODE_Business_Panel.md` | 1 |

---

## HIGH: CLI Entry Points & Commands (src/superclaude/cli/)

80 files total. Top files by reference density:

| File | Ref Count | Key Reference Types |
|------|-----------|---------------------|
| `main.py` | 33 | BRAND (prog_name, help text), COMMAND (usage examples), MODULE (imports) |
| `sprint/executor.py` | 19 | MODULE (imports, paths) |
| `doctor.py` | 16 | BRAND (health check labels), MODULE (import superclaude), COMMAND |
| `cli_portify/executor.py` | 12 | MODULE (paths) |
| `roadmap/commands.py` | 10 | MODULE, COMMAND |
| `install_commands.py` | 9 | BRAND, MODULE (plugins/superclaude/commands/) |
| `cli_portify/commands.py` | 9 | MODULE |
| `tasklist/commands.py` | 8 | MODULE, COMMAND |
| `sprint/commands.py` | 8 | MODULE, COMMAND |
| `cli_portify/steps/__init__.py` | 8 | MODULE |
| `__init__.py` | 7 | COMMAND (usage docstring) |
| `roadmap/executor.py` | 7 | MODULE |
| `cli_portify/steps/panel_review.py` | 6 | MODULE |
| `cli_portify/failures.py` | 6 | MODULE |
| `cleanup_audit/portify-summary.md` | 6 | MODULE, BRAND |
| `install_mcp.py` | 5 | COMMAND, MODULE |
| `install_core.py` | 5 | MODULE |
| `cli_portify/prompts.py` | 5 | MODULE |
| `cli_portify/config.py` | 5 | MODULE |

Remaining 61 CLI files have 1-4 references each (mostly `from superclaude...` imports).

---

## MEDIUM: Test Files

247 files across test directories:

| Directory | File Count |
|-----------|-----------|
| `tests/roadmap/` | 55 |
| `tests/audit/` | 49 |
| `tests/sprint/` | 48 |
| `tests/pipeline/` | 33 |
| `tests/cli_portify/` | 31 |
| `tests/v3.3/` | 10 |
| `tests/unit/` | 6 |
| `tests/integration/` | 5 |
| `tests/sc-roadmap/` | 4 |
| `tests/tasklist/` | 2 |
| `tests/ (root)` | 4 |

Most test files contain `from superclaude...` imports (MODULE type). The import paths are the primary concern; brand references are rare in tests.

---

## MEDIUM: Command/Skill/Agent Definitions (.claude/)

49 files total. These are dev-mirror copies synced from `src/superclaude/`.

| Subdirectory | File Count |
|-------------|-----------|
| `.claude/commands/sc/` | 10 |
| `.claude/agents/` | 4 |
| `.claude/skills/sc-*/` (active skills) | 9 |
| `.claude/skills/sc-release-split-protocol-workspace/` | 26 |

Reference types: BRAND, COMMAND, MODULE -- mirroring `src/superclaude/` content.

---

## MEDIUM: Plugins Directory (plugins/superclaude/)

23 files under `plugins/superclaude/`. This is a build artifact/distribution mirror.

| Subdirectory | File Count |
|-------------|-----------|
| `plugins/superclaude/commands/` | 8 |
| `plugins/superclaude/agents/` | 4 |
| `plugins/superclaude/templates/roadmaps/` | 6 |
| `plugins/superclaude/core/` | 2 |
| `plugins/superclaude/modes/` | 2 |
| `plugins/superclaude/scripts/` | 2 |

---

## MEDIUM: Root-Level Files

| File | Ref Count | Reference Types |
|------|-----------|-----------------|
| `README.md` | 40+ | BRAND, COMMAND, MODULE, URL/ORG |
| `CLAUDE.md` | 50+ | BRAND, COMMAND, MODULE, URL/ORG |
| `PROJECT_INDEX.md` | 20+ | BRAND, MODULE, COMMAND |
| `PROJECT_INDEX.json` | 5+ | MODULE, COMMAND, BRAND |
| `SECURITY.md` | 20+ | BRAND, URL/ORG |
| `AGENTS.md` | 3 | MODULE |
| `LICENSE` | 1 | `Copyright (c) 2024 SuperClaude Framework Contributors` |
| `.gitignore` | 2 | `# SuperClaude specific`, `.superclaude/` |
| `.env.example` | 1 | `# SuperClaude Environment Variables` |
| `superclaude` (file) | 1 | CLI wrapper script |

---

## MEDIUM: Scripts

| File | Ref Count | Reference Types |
|------|-----------|-----------------|
| `scripts/uninstall_legacy.sh` | 22 | BRAND, COMMAND, MODULE |
| `scripts/sync_from_framework.py` | 11 | URL/ORG, MODULE |
| `scripts/build_superclaude_plugin.py` | 4 | MODULE, BRAND |
| `scripts/publish.sh` | 4 | BRAND, COMMAND |
| `scripts/README.md` | 4 | BRAND, MODULE |
| `scripts/cleanup.sh` | 2 | BRAND |
| `scripts/eval_1.py` | varies | MODULE |
| `scripts/eval_2.py` | varies | MODULE |
| `scripts/eval_3.py` | varies | MODULE |
| `scripts/fidelity-check-setup.sh` | varies | MODULE |

---

## LOW: Documentation Files (docs/)

139 files across documentation subdirectories:

| Directory | File Count |
|-----------|-----------|
| `docs/generated/` | 61 |
| `docs/research/` | 25 |
| `docs/reference/` | 16 |
| `docs/analysis/` | 10 |
| `docs/user-guide/` | 8 |
| `docs/developer-guide/` | 6 |
| `docs/memory/` | 5 |
| `docs/mcp/` | 2 |
| `docs/getting-started/` | 2 |
| `docs/troubleshooting/` | 1 |
| `docs/testing/` | 1 |
| `docs/guides/` | 1 |
| `docs/agents/` | 1 |

Reference types: predominantly BRAND and COMMAND in prose. Some MODULE references in developer guides.

---

## LOW: Release Artifacts (.dev/)

2,093 files -- the largest category by far, almost entirely historical artifacts.

| Area | File Count |
|------|-----------|
| `.dev/releases/complete/` | ~1,950 (30+ release versions) |
| `.dev/benchmarks/` | 46 |
| `.dev/releases/backlog/` | ~55 |
| `.dev/releases/current/` | ~30 |
| `.dev/research/` | 5 |
| `.dev/test-sprints/` | 1 |
| `.dev/tasks/` | 1 |

Top release directories by file count:
- `v3.0_unified-audit-gating`: 119 files
- `cross-framework-deep-analysis`: 106 files
- `v2.02-Roadmap-v3`: 101 files
- `v.2.11-roadmap-v4`: 98 files
- `unified-audit-gating-v1.2.1`: 91 files
- `v2.20-WorkflowEvolution`: 84 files

These are sprint/tasklist output artifacts and release planning documents. Reference types are predominantly BRAND and MODULE in generated content. Low priority for renaming since they are archival.

---

## Rename Risk Assessment

### Tier 1 -- Breaking changes (must rename atomically)

1. `pyproject.toml` -- package name, entry points, module paths
2. `src/superclaude/` -- directory name (affects ALL imports)
3. `src/superclaude/cli/main.py` -- CLI entry point
4. `src/superclaude/pytest_plugin.py` -- plugin registration
5. `.github/workflows/*.yml` -- CI will break
6. `MANIFEST.in` -- build will exclude files
7. `package.json` -- NPM package name

### Tier 2 -- Functional but non-breaking

8. `Makefile` -- sync-dev, verify-sync, build-plugin targets
9. `src/superclaude/cli/doctor.py` -- health check labels
10. `src/superclaude/cli/install_*.py` -- install path logic
11. `scripts/build_superclaude_plugin.py` -- plugin build
12. `plugins/superclaude/` -- distribution mirror directory

### Tier 3 -- Cosmetic / documentation

13. All `.md` files in `src/superclaude/commands/`, `agents/`, `skills/`, `core/`
14. `.claude/` mirror copies (auto-synced from src)
15. `README.md`, `CLAUDE.md`, `SECURITY.md`, `LICENSE`
16. `docs/` and `.dev/` content (2,200+ files, mostly archival)

### Key Metrics

- **Python import statements to update**: ~300+ files (all `from superclaude` / `import superclaude`)
- **CLI command references**: ~50+ files reference `superclaude` as a command
- **GitHub URL references** (`SuperClaude-Org/SuperClaude_Framework`): 37 files
- **Directory path** `src/superclaude/`: referenced in Makefile, MANIFEST.in, pyproject.toml, CLAUDE.md, README.md, workflows
