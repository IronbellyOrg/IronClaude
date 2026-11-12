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

## ABSOLUTE RULE: `.dev/tasks/` Is Always Staged

`.dev/tasks/` is always staged (`git add .dev/tasks`): task packages, `progress.md` ledgers and each package's `artifacts/` included. Never gitignore it, never leave it untracked, and never write "never stage" about it in a plan, prompt or memory. Staging is not committing: commit only when asked.

## ABSOLUTE RULE: PR Target = Fork (`IronbellyOrg/IronClaude`), NEVER Upstream

**SuperClaude upstream (`SuperClaude-Org/SuperClaude_Framework`) is never pushed to or interacted with.** No push, fetch or pull from it; no PR, issue, comment, review or reaction there; no remote pointing at it; and no tool call (gh, git or Orca) and no gh or Orca link flag that resolves to it. The fetch and pull ban is the literal reading of "interacted with".

This repository is a **fork**. This clone has only one remote, `origin` = `IronbellyOrg/IronClaude` (the user's private fork). The public parent is `SuperClaude-Org/SuperClaude_Framework`; no remote for it may be added.

**NEVER**, under any circumstance:

- Run a bare `gh pr create` without `--repo IronbellyOrg/IronClaude`. The GitHub CLI defaults `gh pr create` to the **parent repo of a fork**, which means PRs silently land on the public upstream — exposing private fork work and misrouting reviews.
- Open PRs against `SuperClaude-Org/SuperClaude_Framework`. That target is forbidden.
- Push to, fetch from or pull from `SuperClaude-Org/SuperClaude_Framework`, under any remote name or URL. `origin` is the only push target.
- Assume the upstream is the right target because gh's interactive flow suggests it. The interactive flow is the trap.

**Allowed gh forms:** a command that accepts `--repo` passes `--repo IronbellyOrg/IronClaude`; a command that takes the repo as a positional argument (`gh repo view`) names `IronbellyOrg/IronClaude` explicitly; a `gh api` path spells `repos/IronbellyOrg/IronClaude/...`, never the `{owner}/{repo}` placeholder.

**Orca:** Orca identified this project as `github:superclaude-org/superclaude_framework` in `orca worktree current --json` on 2026-11-02. The source of that id is unverified (possibly the upstream URLs in `pyproject.toml` or `package.json`). Until `orca worktree current --json` shows the fork's project id, `--issue`, `--pr` and other Orca link flags are never passed for this repo.

**Scope:** static references to the upstream repository in documentation and test fixtures (for example the negative fixtures in `tests/pr_submit/test_pre_pr_checks.py`) are not interaction and are out of scope.

**The mandatory way to open a PR:** always use `/sc:pr-submit --monitor 3`. It opens the PR with `gh pr create --repo IronbellyOrg/IronClaude` (it resolves the repo from the `origin` remote, which must be `IronbellyOrg/IronClaude`), then waits for the Augment and Codex reviews (a reviewer that shows no activity on the PR is skipped), fixes the confirmed findings of Medium severity or higher (lower ones are only reported) and failing CI checks, pushes the fixes without asking, and replies to and resolves the review comments it fixed. Run it in Claude Code (it is a slash command, not a shell command):

```text
/sc:pr-submit --monitor 3 --head <branch> --title "..." --body "..."
```

**Fallback only, when `/sc:pr-submit` cannot run:**

```bash
gh pr create --repo IronbellyOrg/IronClaude --base master --head <branch> --title "..." --body "..."
```

**Pre-PR checks (mandatory):**

1. `git remote get-url origin` must print the `IronbellyOrg/IronClaude` URL, and `gh repo view IronbellyOrg/IronClaude --json nameWithOwner -q .nameWithOwner` must print `IronbellyOrg/IronClaude`. If gh's default repo is wrong, run `gh repo set-default IronbellyOrg/IronClaude`.
2. `git fetch origin && git log master..origin/master` — if the fork's master is ahead of the local master, **rebase the branch onto `origin/master`** before pushing. The fork has additional commits (e.g., `.claude/` untrack, lint cleanup) that the local clone may not have. Without rebasing, the PR creation will fail with "No commits between master and <branch>".
3. After PR creation, **verify the returned URL points at `https://github.com/IronbellyOrg/IronClaude/pull/N`**. If it points at `SuperClaude-Org`, stop, report the URL to the user, and take no action on that PR; the user closes it. This matches `/sc:pr-submit`, which already halts on a misrouted URL.

**There are no exceptions.**

**Rationale:** This rule exists because gh's default-to-upstream behavior burned the user on 2026-05-25 (PR #558 on SuperClaude-Org instead of IronbellyOrg #86). The mechanical gates (gh's defaults, `git push` targeting) do NOT enforce the right outcome — only this CLAUDE.md rule + the repo named explicitly on every gh call does. See also: memory `feedback_pr_target_fork_only.md` and `reference_repo_remotes_IronClaude.md`.

## ABSOLUTE RULE: Never Hardcode `src/superclaude/` Paths in Installed Primitives

Commands, skills, agents, hooks and core files are copied to `~/.claude/` by `superclaude install` and then run in OTHER projects, where `src/superclaude/` does not exist. A path that tells an agent to read or verify something under `src/superclaude/...` breaks there.

**NEVER**, in `src/superclaude/{commands,skills,agents,core,hooks,templates}` or the `plugins/superclaude/` mirror, tell an agent to Read, verify or invoke another primitive through a `src/superclaude/...` path. Use the installed path:

| Primitive | Installed path |
|---|---|
| skill | `~/.claude/skills/<name>/SKILL.md` (refs: `~/.claude/skills/<name>/refs/...`) |
| agent | `~/.claude/agents/<name>.md` |
| command | `~/.claude/commands/sc/<name>.md` |
| core doc | `~/.claude/<FILE>.md` (e.g. `~/.claude/HOW-WE-WORK.md`) |
| template | `~/.claude/templates/...` |
| hook | `~/.claude/hooks/...` |

- Package code (`src/superclaude/cli/`, `pm_agent/`, `contracts/`) and `src/superclaude/examples/` are NOT installed to `~/.claude/`. Do not add new references to them from a primitive; reach package behavior through the `superclaude` CLI.
- **Dual surface:** when a primitive looks up another installed primitive, name both the installed copy and the project `.claude/` copy (created by `make sync-dev` in a dev checkout). For an existence check either one satisfies it. When the agent must read ONE file, follow Claude Code's own precedence: agents read project `.claude/agents/` first, then `~/.claude/agents/`; skills read `~/.claude/skills/` first, then `.claude/skills/`.
- **Allowed:** maintainer instructions about editing this repo ("edit `src/superclaude/...`, then `make sync-dev`"), commands that operate on this repo's own source by design (for example `/sc:cli-portify`), and a clearly labelled in-checkout fallback listed AFTER the global path.
- **Check before committing a new or edited primitive:** `grep -rn 'src/superclaude' src/superclaude/{commands,skills,agents,core,hooks}` and justify every hit against the list above. `tests/skills/test_primitive_dual_surface_lookup.py` pins the adversarial-skill and rf-qa lookups.

**Rationale:** 25 `src/superclaude/...` references in installed primitives broke them outside a checkout; they were rewritten in PR #278, and the first rewrite then dropped the project `.claude/` copy, which is why the dual-surface rule exists.

### Required Commands

```bash
# All Python operations must use UV
uv run pytest                    # Run tests
uv run pytest tests/pm_agent/   # Run specific tests
uv pip install package           # Install dependencies
uv run python script.py          # Execute scripts
```

## 📂 Project Structure

**Current v5.0.0 Architecture**: Python package with slash commands

```text
# Claude Code Configuration (v5.0.0)
.claude/
├── settings.json        # User settings
├── commands/sc/         # Dev copies of the slash commands, synced from src/ by `make sync-dev`
├── agents/              # Dev copies of the agents, synced from src/ by `make sync-dev`
└── skills/              # Dev copies of the skills, synced from src/ by `make sync-dev`

# Python Package
src/superclaude/         # Pytest plugin + CLI tools
├── core/                # Framework .md files installed to ~/.claude/ (CLAUDE.md, RULES, PRINCIPLES, etc.)
├── commands/            # Slash command definitions
├── pytest_plugin.py     # Auto-loaded pytest integration
├── pm_agent/            # confidence.py, self_check.py, reflexion.py
├── execution/           # parallel.py, reflection.py, self_correction.py
├── cli/                 # Python CLI: sprint, roadmap, tasklist, audit, pipeline
├── agents/              # Agent definition source files (.md)
└── skills/              # Skill packages (SKILL.md + rules/ + templates/ + scripts/)

# Project Files
tests/                   # Python test suite
docs/                    # Documentation (docs/generated/ = CLI pipeline artifacts)
scripts/                 # Analysis tools (workflow metrics, A/B testing)
KNOWLEDGE.md             # Accumulated insights
```

## 🔧 Development Workflow

### Essential Commands

```bash
# Setup
make install          # Install editable + dev dependencies (ruff included)
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
make sync-dev         # Copy src/superclaude/{skills,agents,commands,hooks,templates} → .claude/
make verify-sync      # Check src/ and .claude/ are in sync (CI-friendly)

# Pipelines
superclaude sprint run <tasklist-index.md>   # Execute sprint pipeline
superclaude roadmap run <spec.md>            # Generate roadmap pipeline
superclaude roadmap validate <output-dir>    # Validate roadmap artifacts

# MCP Servers
superclaude mcp                              # Interactive install (gateway default)
superclaude mcp --list                       # List available servers
superclaude mcp --servers airis-mcp-gateway  # Install AIRIS Gateway (recommended)
superclaude mcp --servers tavily --servers context7  # Install individual servers (one --servers per server)

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

### Slash Commands (v5.0.0)

- Install via: `pipx install git+https://github.com/IronbellyOrg/IronClaude && superclaude install` (the PyPI `superclaude` package is the upstream project, not this fork)
- Commands installed to: `~/.claude/commands/sc/`
- Available: run `/sc:help` to list every installed command and skill

> **Note**: A TypeScript plugin system is planned for a later release; it is not part of 5.0.0.

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

**CRITICAL**: When running multiple Claude Code sessions in parallel, each one works in its own worktree to avoid conflicts. A worktree is created by its orchestrator with an agent in it; a session does not open a worktree for itself.

**ABSOLUTE RULE — every project worktree is created through Orca and lives at Orca's default worktree location.**
Create it with `orca worktree create --name <name> --agent claude --prompt "<task>"`, adding `--repo <selector>`,
`--base-branch <ref>`, and `--parent-worktree <selector>` or `--no-parent` as needed. Orca places it at its default
worktree location, outside the main checkout; `orca worktree current --json` (from inside it) and `orca worktree list` show the real path.

- **Every worktree gets an agent, and its creator owns it.** Because every worktree gets an agent, a bare `orca worktree create` is wrong: always pass `--agent claude --prompt "<task>"`, and never create a worktree for your own use. The eligible session that creates a worktree owns its agent(s). An Orca coordinator is person-opened; ownership does not authorize a supervised worker to create worktrees or dispatch workers. A worktree a human creates needs an agent too. Supervised workers are started with `orca orchestration worker-start`, which already creates their worktree with an agent. A PreToolUse hook (`require-orca-worktree-agent.sh`) blocks a Bash call that runs `orca worktree create` without `--agent` once it is installed; the other parts of this rule are instructions only.
- Never create a project worktree with raw `git worktree add`, under the retired `.dev/worktrees/` location, or under `.claude/worktrees/`.
- Do **not** use the `EnterWorktree` tool: it hardcodes `.claude/worktrees/`, which is gitignored sync-dev territory.
- Never pass Orca link flags (`--issue`, `--pr`) for this repo; the fork rule above (`## ABSOLUTE RULE: PR Target = Fork`) governs them.
- **Exception — internal temporary checkouts:** a CLI, script or test that creates and removes its own checkout keeps using `git worktree add` directly and must work without Orca. The five cases are: the reflect `--isolate-reviewers` review snapshot; the troubleshoot backtest replay; test fixtures in a pytest temporary directory; `scripts/eval_runner.py`'s temporary master checkout; and the optional read-only release-tag checkout in `/sc:post-release`, removed after the scan.
- **Existing checkouts under the retired `.dev/worktrees/` location** may stay until their branch is merged, then are removed with `git worktree remove <path>`; no new checkout may be created there.

```bash
# Create a worktree named pm-agent, based on origin/master, with an agent in it
orca worktree create --name pm-agent --base-branch origin/master --agent claude --prompt "<task>"

# Show where Orca put it
orca worktree list
```

**Benefits**:

- Run Claude Code sessions on different branches simultaneously
- No branch switching conflicts
- Independent working directories
- Parallel development without state corruption

**Usage**:

- Session A: Open the main checkout (current branch); it is the orchestrator that creates the worktrees below
- Worktree `integration`: created by session A with `--agent claude`; that agent works there (path from `orca worktree list`)
- Worktree `pm-agent` (feature branch): created by session A with `--agent claude`; that agent works there

**Cleanup**:

```bash
orca worktree rm --worktree name:integration
```

## 📝 Key Documentation Files

**`src/superclaude/core/HOW-WE-WORK.md`** - the routing guide: which command or skill to use for each kind of work, in what order, with which required flags. Edit it here; it installs to `~/.claude/HOW-WE-WORK.md`. After editing, copy it byte-for-byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` and re-run the level-table copy into `src/superclaude/core/CLAUDE.md` (tests check both). Never add it as an `@` import.

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
**HIGHEST PRIORITY SERVER**
Auggie MCP should be used whenever broader codebase context and knowledge would be valuable.  It is free and costs little to no tokens

```bash
superclaude mcp  # Interactive install, gateway is default (requires Docker)
```

**Gateway Benefits** (advertised figures, also used in this repo's installer text; not measured here; UNVERIFIED): 60+ tools, 98% token reduction, single SSE endpoint, Web UI

**Servers the gateway can offer** depend on the backend configuration the installer downloads from the upstream gateway repository; that content and its availability are UNVERIFIED here:

- **Tavily**: Web search (Deep Research)
- **Context7**: Official documentation (prevent hallucination)

**Built-in install, successful fresh-template path: Mindbase and Airis Agent are disabled.** When the installer downloads the backend configuration (`mcp-config.json`) and parses it, it marks any `mindbase` and `airis-agent` entries `enabled: false`, because their containers are not in the distribution Compose file (`src/superclaude/cli/install_mcp.py`). Other paths differ: an already-existing `mcp-config.json` is reused unchanged, a failed download (non-zero exit) writes a minimal default config, any other exception writes an empty config, and an unparseable download is used as-is. Do not assume every installation matches, and whether the gateway honors the disabled flag at runtime is UNVERIFIED. The manual guides (`src/superclaude/mcp/MCP_Mindbase.md`, `src/superclaude/mcp/MCP_Airis-Agent.md`) describe a separate git clone plus `docker compose up` deployment; whether MindBase is available there is UNVERIFIED.

**Individual servers (not in the gateway; install with `superclaude mcp --servers <name>`)**:

- **Morphllm** (`morphllm-fast-apply`): Fast bulk edits (needs `MORPH_API_KEY`)
- **Auggie** (`auggie`): Codebase context retrieval (needs the global `auggie` npm binary and a one-time `auggie login`)

**Optional**: Playwright (browser automation)

**Usage**: TypeScript plugins and Python pytest plugin can call MCP servers. Always prefer MCP tools over speculation for documentation/research.

## 🚀 Development & Installation

### Current Installation Method (v5.0.0)

**Standard Installation**:

```bash
# Option 1: pipx (recommended; the PyPI "superclaude" package is upstream, so install from the fork)
pipx install git+https://github.com/IronbellyOrg/IronClaude
superclaude install        # Installs core files, commands, agents, skills, hooks, templates and user setup

# Option 2: From a clone
git clone https://github.com/IronbellyOrg/IronClaude.git
cd IronClaude
uv venv && make install && uv run superclaude install
```

**`superclaude install` installs these component types (plus ccsession, hooks, templates and user setup)**:

1. Core framework files (`.md`) → `~/.claude/`
2. Slash commands (`.md`) → `~/.claude/commands/sc/`
3. Agent definitions (`.md`) → `~/.claude/agents/`
4. Skills (directories with `SKILL.md`) → `~/.claude/skills/`

**Development Mode**:

```bash
# Install in editable mode
make install

# Run tests
make test

# Verify installation
make verify
```

### Plugin System (Not Yet Available)

The TypeScript plugin system (`.claude-plugin/`, marketplace) is planned for a later release; 5.0.0 does not include it.
See `docs/plugin-reorg.md` for details.

## 📊 Package Information

**Package name**: `superclaude`
**Version**: 5.0.0 (see `version` in `pyproject.toml`)
**Python**: >=3.10
**Build system**: hatchling (PEP 517)

**Entry points**:

- CLI: `superclaude` command
- Pytest plugin: Auto-loaded as `superclaude`

**Dependencies**:

- pytest>=7.0.0
- click>=8.0.0
- rich>=13.0.0
