# SuperClaude — Framework Context

## Python Environment

Use UV for all Python operations. Never use `python -m`, `pip install`, or `python script.py`.

```
uv run pytest                    # run tests
uv run pytest tests/path/ -v     # specific tests
uv pip install package           # install deps
uv run python script.py          # execute scripts
```

## Project Structure

```
src/superclaude/        # Source of truth for all distributable components
  core/                 # This file + framework .md files (RULES, PRINCIPLES, etc.)
  commands/             # Slash command definitions
  skills/               # Skill packages (SKILL.md + refs/ + rules/ + templates/)
  agents/               # Agent definitions
  cli/                  # Python CLI: sprint, roadmap, tasklist, audit, pipeline
  pm_agent/             # confidence.py, self_check.py, reflexion.py
.claude/                # Dev copies — synced from src/, read by Claude Code
  commands/sc/          # Active slash commands
  skills/               # Active skills (loaded on-demand, ~50 tokens each)
  agents/               # Active agents
tests/                  # Python test suite
docs/                   # Documentation (docs/generated/ = CLI pipeline artifacts)
```

## Dev Commands

```
make dev                # Install editable + dev dependencies
make test               # Full test suite
make sync-dev           # src/superclaude/{skills,agents,commands} → .claude/
make verify-sync        # Confirm src/ and .claude/ match (run before committing)
make lint && make format
superclaude sprint run <tasklist-index.md>   # Execute sprint pipeline
superclaude roadmap run <spec.md>            # Generate roadmap pipeline
superclaude roadmap validate <output-dir>    # Validate roadmap artifacts
```

## Component Sync

Source of truth is `src/superclaude/`. Always edit there first, then `make sync-dev`.
If you edited `.claude/` directly: copy changes back to `src/superclaude/`, then `make verify-sync`.

## MCP Servers

| Server         | Primary Use                                  | Flag       |
|----------------|----------------------------------------------|------------|
| auggie         | Codebase search — call before significant edits | (auto)  |
| serena         | Symbol navigation, project memory            | --serena   |
| sequential     | Multi-step reasoning, deep analysis          | --seq      |
| context7       | Official library/framework docs              | --c7       |
| tavily         | Web search, current information              | --tavily   |
| magic          | UI component generation                      | --magic    |
| playwright     | Browser automation, E2E testing              | --play     |

## Personas (auto-activated by context; override with --persona-X)

| Persona      | Domain                         | Primary MCP       |
|--------------|--------------------------------|-------------------|
| architect    | systems design, scalability    | sequential, c7    |
| frontend     | UI/UX, components              | magic, playwright |
| backend      | APIs, reliability              | c7, sequential    |
| security     | vulnerabilities, auth          | sequential        |
| analyzer     | root cause, investigation      | sequential, c7    |
| qa           | testing, coverage              | playwright, seq   |
| refactorer   | cleanup, tech debt             | sequential        |
| devops       | deploy, infrastructure         | sequential        |
| scribe       | docs, localization             | c7, sequential    |

## Core Rules

1. **UV only** — never `python -m` or bare `pip`
2. **Parallel by default** — batch independent tool calls; sequential only for true dependencies
3. **Confidence check** — ≥90% proceed, 70-89% present options, <70% ask. Trigger surface is not just code edits: run it (or its lightweight form — verify the specific token via `--help`/grep/file read/`codebase-retrieval`) BEFORE any reply that suggests an action, emits a command/snippet, or names a specific flag/path/function/version. Recommendation = action.
4. **Git** — feature branches only; never commit directly to master/main
5. **Output paths** — write files next to their source or to the `--output` dir the CLI command specifies; `docs/generated/` is a roadmap pipeline artifact directory, not a general output sink
6. **Component edits** — `src/superclaude/` → `make sync-dev` → `.claude/`; never reverse without syncing back
7. **Finish what you start** — no TODO stubs for core logic; if you begin a feature, complete it to working state
8. **Scope discipline** — build exactly what's asked; no speculative additions
9. **Auggie first** — call `codebase-retrieval` before significant edits to load relevant context
10. **Temporal** — verify current date from env context before any date/version reasoning

## Key Docs

- `PLANNING.md` — architecture decisions, absolute rules
- `TASK.md` — current tasks and priorities
- `KNOWLEDGE.md` — accumulated insights and debugging patterns
- `src/superclaude/core/RULES.md` — full behavioral rules (referenced by skills)
- `src/superclaude/core/PRINCIPLES.md` — engineering principles (referenced by skills)

## Skills & Commands

Skills in `~/.claude/skills/` load on-demand (~50 tokens each at session start).
Commands in `~/.claude/commands/sc/` — use `/sc:help` to list all available.
Agents in `~/.claude/agents/` — delegated by skills and commands.
Full behavioral specs (personas, MCP workflows, wave strategies) live in the skill files.

## Context freshness discipline

Long sessions accumulate **derived facts** in working memory: file paths,
line numbers, IPs, credential IDs, mtime relationships. These age out
silently when the user (or other agents) modifies the underlying files.
The hook layer enforces this at edit time; this section binds the
behavior for **citations made in chat responses with no tool call**, which
hooks cannot catch.

### The five content-signal triggers

Treat the following as **mandatory re-verification triggers** before
output:

- **S1.** About to cite `file:line` or "at line N" of a specific file.
- **S2.** About to issue an Edit / Write / replace_content / replace_symbol_body
  / insert_*_symbol against a file. (Hook enforces; mention here for completeness.)
- **S3.** About to assert that file A agrees or disagrees with file B.
- **S4.** About to quote an IP, hostname, credential ID, port, path, or
  config value tied to a specific source file.
- **S5.** About to recommend an infrastructure change that depends on a
  remembered fact.

### Self-check pattern (factual phrasing)

Before producing output that hits S1, S3, S4, or S5: ask, "Did I Read the
source file in the last 5 tool calls of this turn, AND has nothing
modified it since?" If the answer is no, OR uncertain, perform a fresh
Read first. The cost of a Read is trivial compared to a wrong citation.

### Refresh-tool selection

Pick the refresh tool by the content type of the claim:

| Content | Tool |
|---|---|
| Exact line numbers / file content | `Read` |
| Symbolic queries (which function, where defined, what references) | `mcp__serena__find_symbol` / `find_referencing_symbols` |
| Semantic / cross-cutting ("is there an X anywhere") | `mcp__auggie__codebase-retrieval` |
| Runtime state (permissions, mounts, sockets) | `Bash` (user-executed read-only command) |

### Session context envelope

Every user prompt is prefixed with a `<session-context>` block injected
by the UserPromptSubmit hook. Fields like `turn=`, `Δ=`, `git=dirty=...`,
`changed_since_last_turn=...` are factual and current as of that prompt.
Treat as ground truth for that turn; do not override from older context.
