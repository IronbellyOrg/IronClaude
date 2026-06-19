# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 🐍 Python Environment Rules

**CRITICAL**: This project uses **UV** for all Python operations. Never use `python -m`, `pip install`, or `python script.py` directly.

## ABSOLUTE RULE: Custom Command Skill Invocation

When ANY message starts with /sc:<command>, you MUST invoke the corresponding skill via the Skill tool BEFORE generating any other output. If the command file says "invoke Skill X", that is BLOCKING.
  Generating protocol output without invoking the skill is a VIOLATION.  No exceptions. No "I already loaded it." No "I know the protocol."

In the event where context pressure would otherwise have the agent take shortcuts or improvise instead of initiating the command/skill/protoco - ALWAYS WARN THE USER AND INSTRUCT THEM TO RUN THE CUSTOM COMMAND IN A NEW CHAT.

## ABSOLUTE RULE: Never Stage or Commit `.claude/` Contents

`.claude/{skills,commands,agents,hooks,templates}/*` is **gitignored sync-dev output** of `src/superclaude/`. The ONLY tracked file under `.claude/` is `.claude/settings.json` (project hook + permission registrations, not auto-generated). Upstream regenerates `.claude/` via `superclaude install`; the local copy exists for Claude Code to read during development.

**NEVER**, under any circumstance:

- `git add .claude/skills/...`, `.claude/commands/...`, `.claude/agents/...`, `.claude/hooks/...`, `.claude/templates/...`
- `git add -f` on any `.claude/` path
- Suggest staging `.claude/` mirrors in paste-ready commit commands
- Author task-file instructions, follow-ups, or risk notes telling the user to stage `.claude/` paths

**The `-f` rule:** If `git add` requires `-f` on any `.claude/` path, that `-f` is the violation siren. STOP. Move the change to `src/superclaude/` first, run `make sync-dev`, and stage only the `src/` side.

**Exceptions:** ONLY `.claude/settings.json`. ANY other exception requires explicit user instruction in the same session and must be called out (e.g., "user authorized staging `.claude/foo` because X"). Without that, treat every `.claude/<not-settings.json>` path as forbidden to stage.

**Rationale:** SoT discipline. Committing `.claude/skills/foo/SKILL.md` alongside `src/superclaude/skills/foo/SKILL.md` doubles every diff, invites drift, and breaks `make verify-sync` for the next contributor. The gitignore (`.claude/` + `!.claude/settings.json`) and the pre-commit `verify-sync` local hook enforce this together — but neither catches `git add -f` or hand-edited paste-ready commands. That's why this rule exists at the CLAUDE.md level: it must hold even when the mechanical gates are bypassed.

See also: memory `feedback_claude_dir_gitignored.md`.

## ABSOLUTE RULE: PR Target = Fork (`IronbellyOrg/IronClaude`), NEVER Upstream

This repository is a **fork**. `origin` = `IronbellyOrg/IronClaude` (the user's private fork). `upstream` = `SuperClaude-Org/SuperClaude_Framework` (the public parent).

**NEVER**, under any circumstance:

- Run a bare `gh pr create` without `--repo IronbellyOrg/IronClaude`. The GitHub CLI defaults `gh pr create` to the **parent repo of a fork**, which means PRs silently land on the public upstream — exposing private fork work and misrouting reviews.
- Open PRs against `SuperClaude-Org/SuperClaude_Framework` without explicit user authorization in the same session. Treat that target as forbidden.
- Push to `upstream` (the `upstream` remote name above). The `origin` remote is the correct push target.
- Assume the upstream is the right target because gh's interactive flow suggests it. The interactive flow is the trap.

**The mandatory command shape:**

```bash
gh pr create --repo IronbellyOrg/IronClaude --base master --head <branch> --title "..." --body "..."
```

**Pre-PR checks (mandatory):**

1. `git remote -v` — confirm `origin` = `IronbellyOrg/IronClaude.git`.
2. `git fetch origin && git log master..origin/master` — if the fork's master is ahead of the local master, **rebase the branch onto `origin/master`** before pushing. The fork has additional commits (e.g., `.claude/` untrack, lint cleanup) that the local clone may not have. Without rebasing, the PR creation will fail with "No commits between master and <branch>".
3. After PR creation, **verify the returned URL points at `https://github.com/IronbellyOrg/IronClaude/pull/N`**, not `SuperClaude-Org`. If it shows the wrong owner, close it immediately and reopen with `--repo IronbellyOrg/IronClaude`.

**Exceptions:** Contributing back to upstream is explicit, separate, deliberate user authorization in the same session — never a default behavior. Without that explicit instruction, every PR goes on the fork.

**Rationale:** This rule exists because gh's default-to-upstream behavior burned the user on 2026-05-25 (PR #558 on SuperClaude-Org instead of IronbellyOrg #86). The mechanical gates (gh's defaults, `git push` targeting) do NOT enforce the right outcome — only this CLAUDE.md rule + explicit `--repo` on every invocation does. See also: memory `feedback_pr_target_fork_only.md` and `reference_repo_remotes_IronClaude.md`.

### Required Commands

```bash
# All Python operations must use UV
uv run pytest                    # Run tests
uv run pytest tests/pm_agent/   # Run specific tests
uv pip install package           # Install dependencies
uv run python script.py          # Execute scripts
```

## 📂 Project Structure

**Current v4.2.0 Architecture**: Python package with slash commands

```text
# Claude Code Configuration (v4.2.0)
.claude/
├── settings.json        # User settings
├── commands/            # Slash commands (installed via `superclaude install`)
├── agents/              # Agent definitions (installed via `superclaude install`)
└── skills/              # Skills (installed via `superclaude install`)

# Python Package
src/superclaude/         # Pytest plugin + CLI tools
├── pytest_plugin.py     # Auto-loaded pytest integration
├── pm_agent/            # confidence.py, self_check.py, reflexion.py
├── execution/           # parallel.py, reflection.py, self_correction.py
├── cli/                 # main.py, doctor.py, install_skill.py, install_agents.py, install_skills.py
├── agents/              # Agent definition source files (.md)
└── skills/              # Skill packages (SKILL.md + rules/ + templates/ + scripts/)

# Project Files
tests/                   # Python test suite
docs/                    # Documentation
scripts/                 # Analysis tools (workflow metrics, A/B testing)
KNOWLEDGE.md             # Accumulated insights
```

## 🔧 Development Workflow

### Essential Commands

```bash
# Setup
make dev              # Install in editable mode with dev dependencies
make verify           # Verify installation (package, plugin, health)

# Testing
make test             # Run full test suite
uv run pytest tests/pm_agent/ -v              # Run specific directory
uv run pytest tests/test_file.py -v           # Run specific file
uv run pytest -m confidence_check             # Run by marker
uv run pytest --cov=superclaude               # With coverage

# Code Quality
make lint             # Run ruff linter
make format           # Format code with ruff
make doctor           # Health check diagnostics

# Component Sync (skills + agents)
make sync-dev         # Copy src/superclaude/{skills,agents} → .claude/
make verify-sync      # Check src/ and .claude/ are in sync (CI-friendly)

# MCP Servers
superclaude mcp                              # Interactive install (gateway default)
superclaude mcp --list                       # List available servers
superclaude mcp --servers airis-mcp-gateway  # Install AIRIS Gateway (recommended)
superclaude mcp --servers tavily context7    # Install individual servers

# Plugin Packaging
make build-plugin            # Build plugin artefacts into dist/
make sync-plugin-repo        # Sync artefacts into ../SuperClaude_Plugin

# Maintenance
make clean            # Remove build artifacts
```

## 🔄 Component Sync

**Source of truth**: `src/superclaude/` is the canonical location for all distributable components (skills, agents, commands, core files). The `superclaude install` CLI reads from here.

**Dev copies**: `.claude/skills/` and `.claude/agents/` in the repo root are convenience copies that Claude Code reads directly during development.

**Workflow when adding/editing components**:

1. Edit files in `src/superclaude/skills/` or `src/superclaude/agents/`
2. Run `make sync-dev` to copy changes to `.claude/`
3. Run `make verify-sync` to confirm sync (also run before committing)

**If you edited `.claude/` directly** (e.g., iterating on a skill with Claude Code):

1. Copy your changes to `src/superclaude/` manually
2. Run `make verify-sync` to confirm both sides match

## Plugin Override — Skill-Creator Workspace Destination

**Override:** The `skill-creator` plugin (and any plugin following the same convention) creates an eval/iteration workspace as a **sibling to the skill directory** — e.g. `.claude/skills/<skill-name>-workspace/`. **In this project that convention is overridden.**

**Destination rule:** When invoking `skill-creator` or any plugin that uses a sibling-workspace convention, the eval workspace **MUST** be written to `.dev/eval-workspaces/<skill-name>/` instead of `.claude/skills/<skill-name>-workspace/`. This applies regardless of any path the plugin itself suggests or attempts.

**Rationale (behavior, not file path):** `.claude/skills/<skill-name>/` is reserved for the distributable skill package (`SKILL.md` + `refs/`, `rules/`, `templates/`, `scripts/`). Anything generated by a skill's evaluation, debugging, or release workflow belongs under `.dev/`, never under `.claude/skills/`. This addendum cites the *sibling-workspace behavior* rather than a specific plugin file or line number so the override survives upstream skill-creator updates.

**Authoritative source:** See `.dev/README.md` for the canonical convention and the full "where things go" decision guide. Enforcement is layered: the PreToolUse hook in `.claude/settings.json` rejects writes to `.claude/skills/*-workspace/**` with a redirect to `.dev/eval-workspaces/<skill-name>/`, and `.gitignore` matches `.claude/skills/*-workspace/` so any misplaced workspace cannot be committed.

## 📦 Core Architecture

### Pytest Plugin (Auto-loaded)

Registered via `pyproject.toml` entry point, automatically available after installation.

**Fixtures**: `confidence_checker`, `self_check_protocol`, `reflexion_pattern`, `token_budget`, `pm_context`

**Auto-markers**:

- Tests in `/unit/` → `@pytest.mark.unit`
- Tests in `/integration/` → `@pytest.mark.integration`

**Custom markers**: `@pytest.mark.confidence_check`, `@pytest.mark.self_check`, `@pytest.mark.reflexion`

### PM Agent - Three Core Patterns

**1. ConfidenceChecker** (src/superclaude/pm_agent/confidence.py)

- Pre-execution confidence assessment: ≥90% required, 70-89% present alternatives, <70% ask questions
- Prevents wrong-direction work, ROI: 25-250x token savings

**2. SelfCheckProtocol** (src/superclaude/pm_agent/self_check.py)

- Post-implementation evidence-based validation
- No speculation - verify with tests/docs

**3. ReflexionPattern** (src/superclaude/pm_agent/reflexion.py)

- Error learning and prevention
- Cross-session pattern matching

### Parallel Execution

**Wave → Checkpoint → Wave pattern** (src/superclaude/execution/parallel.py):

- 3.5x faster than sequential execution
- Automatic dependency analysis
- Example: [Read files in parallel] → Analyze → [Edit files in parallel]

### Slash Commands (v4.2.0)

- Install via: `pipx install superclaude && superclaude install`
- Commands installed to: `~/.claude/commands/`
- Available: `/pm`, `/research`, `/index-repo`, and 27 others

> **Note**: TypeScript plugin system planned for v5.0 ([#419](https://github.com/SuperClaude-Org/SuperClaude_Framework/issues/419))

## 🧪 Testing with PM Agent

### Example Test with Markers

```python
@pytest.mark.confidence_check
def test_feature(confidence_checker):
    """Pre-execution confidence check - skips if < 70%"""
    context = {"test_name": "test_feature", "has_official_docs": True}
    assert confidence_checker.assess(context) >= 0.7

@pytest.mark.self_check
def test_implementation(self_check_protocol):
    """Post-implementation validation with evidence"""
    implementation = {"code": "...", "tests": [...]}
    passed, issues = self_check_protocol.validate(implementation)
    assert passed, f"Validation failed: {issues}"

@pytest.mark.reflexion
def test_error_learning(reflexion_pattern):
    """If test fails, reflexion records for future prevention"""
    pass

@pytest.mark.complexity("medium")  # simple: 200, medium: 1000, complex: 2500
def test_with_budget(token_budget):
    """Token budget allocation"""
    assert token_budget.limit == 1000
```

## 🌿 Git Workflow

**Branch structure**: `master` (production) ← `integration` (testing) ← `feature/*`, `fix/*`, `docs/*`

**Standard workflow**:

1. Create branch from `integration`: `git checkout -b feature/your-feature`
2. Develop with tests: `uv run pytest`
3. Commit: `git commit -m "feat: description"` (conventional commits)
4. Merge to `integration` → validate → merge to `master`

**Current branch**: See git status in session start output

### Parallel Development with Git Worktrees

**CRITICAL**: When running multiple Claude Code sessions in parallel, use `git worktree` to avoid conflicts.

**ABSOLUTE RULE — worktree location is `./.dev/worktrees/`, NEVER `.claude/worktrees/`.**
Every worktree this project creates MUST live under `<repo>/.dev/worktrees/<name>/`. Do **not** use the
`EnterWorktree` tool (it hardcodes `.claude/worktrees/`, which is gitignored sync-dev territory) — instead
create worktrees explicitly with `git worktree add .dev/worktrees/<name> <branch>`. Add `.dev/worktrees/`
to `.gitignore` if it is not already ignored, so nested worktree checkouts never get staged.

```bash
# Create a worktree for a feature branch (canonical location)
git worktree add .dev/worktrees/pm-agent -b feature/pm-agent origin/master

# Create a worktree for an existing branch
git worktree add .dev/worktrees/integration integration
```

**Benefits**:

- Run Claude Code sessions on different branches simultaneously
- No branch switching conflicts
- Independent working directories
- Parallel development without state corruption

**Usage**:

- Session A: Open `<repo>/` (current branch)
- Session B: Open `<repo>/.dev/worktrees/integration/` (integration)
- Session C: Open `<repo>/.dev/worktrees/pm-agent/` (feature branch)

**Cleanup**:

```bash
git worktree remove .dev/worktrees/integration
```

## 📝 Key Documentation Files

**KNOWLEDGE.md** - Accumulated insights and troubleshooting

Additional docs in `docs/user-guide/`, `docs/developer-guide/`, `docs/reference/`

## 💡 Core Development Principles

### 1. Evidence-Based Development

**Never guess** - verify with official docs (Context7 MCP, WebFetch, WebSearch) before implementation.

### 2. Confidence-First Implementation

Check confidence BEFORE starting: ≥90% proceed, 70-89% present alternatives, <70% ask questions.

### 3. Parallel-First Execution

Use **Wave → Checkpoint → Wave** pattern (3.5x faster). Example: `[Read files in parallel]` → Analyze → `[Edit files in parallel]`

### 4. Token Efficiency

- Simple (typo): 200 tokens
- Medium (bug fix): 1,000 tokens
- Complex (feature): 2,500 tokens
- Confidence check ROI: spend 100-200 to save 5,000-50,000

## 🔧 MCP Server Integration

**Recommended**: Use **airis-mcp-gateway** for unified MCP management.
**HIGHET PRIORITY SERVER**
Auggie MCP should be used whenever broader codebase context and knowledge would be valuable.  It is free and costs little to no tokens

```bash
superclaude mcp  # Interactive install, gateway is default (requires Docker)
```

**Gateway Benefits**: 60+ tools, 98% token reduction, single SSE endpoint, Web UI

**High Priority Servers** (included in gateway):

- **Tavily**: Web search (Deep Research)
- **Context7**: Official documentation (prevent hallucination)
- **Sequential**: Token-efficient reasoning (30-50% reduction)
- **Serena**: Session persistence
- **Mindbase**: Cross-session learning

**Optional**: Playwright (browser automation), Magic (UI components), Chrome DevTools (performance)

**Usage**: TypeScript plugins and Python pytest plugin can call MCP servers. Always prefer MCP tools over speculation for documentation/research.

## 🚀 Development & Installation

### Current Installation Method (v4.2.0)

**Standard Installation**:

```bash
# Option 1: pipx (recommended)
pipx install superclaude
superclaude install        # Installs: core files → commands → agents → skills

# Option 2: Direct from repo
git clone https://github.com/SuperClaude-Org/SuperClaude_Framework.git
cd SuperClaude_Framework
./install.sh
```

**`superclaude install` installs 4 component types**:

1. Core framework files (`.md`) → `~/.claude/`
2. Slash commands (`.md`) → `~/.claude/commands/sc/`
3. Agent definitions (`.md`) → `~/.claude/agents/`
4. Skills (directories with `SKILL.md`) → `~/.claude/skills/`

**Development Mode**:

```bash
# Install in editable mode
make dev

# Run tests
make test

# Verify installation
make verify
```

### Plugin System (v5.0 - Not Yet Available)

The TypeScript plugin system (`.claude-plugin/`, marketplace) is planned for v5.0.
See `docs/plugin-reorg.md` for details.

## 📊 Package Information

**Package name**: `superclaude`
**Version**: 4.2.0
**Python**: >=3.10
**Build system**: hatchling (PEP 517)

**Entry points**:

- CLI: `superclaude` command
- Pytest plugin: Auto-loaded as `superclaude`

**Dependencies**:

- pytest>=7.0.0
- click>=8.0.0
- rich>=13.0.0
