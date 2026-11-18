# Visual Architecture Summary

This page is a contributor-facing visual map of the current `SuperClaude_Framework` repository.

It is grounded in the current repository state observed in:

- `pyproject.toml`
- `CLAUDE.md`
- `Makefile`
- `src/superclaude/`
- the generated contributor bundle in `docs/generated/contributor-knowledge-base/`

If older prose elsewhere in the repo conflicts with the current tree, prefer the current code and current repo instructions. In particular, some older docs describe the project primarily as a context-file framework; the current repository is broader and includes a substantial Python package, CLI subsystem, pytest plugin, and packaged framework assets.

## Table of contents

- [One-screen orientation](#one-screen-orientation)
- [High-level system architecture](#high-level-system-architecture)
- [Source-of-truth vs dev-mirror relationships](#source-of-truth-vs-dev-mirror-relationships)
- [Console entry points](#console-entry-points)
- [Major component map](#major-component-map)
- [CLI runner and subsystem map](#cli-runner-and-subsystem-map)
- [Protocol-backed command relationships](#protocol-backed-command-relationships)
- [Adversarial workflow as a reusable protocol](#adversarial-workflow-as-a-reusable-protocol)
- [Audit and recommendation orchestration family](#audit-and-recommendation-orchestration-family)
- [PM and validation support flows](#pm-and-validation-support-flows)
- [Task-surface deprecation map](#task-surface-deprecation-map)
- [Choosing the right change surface](#choosing-the-right-change-surface)
- [Repository map outside the package](#repository-map-outside-the-package)
- [Where to go next](#where-to-go-next)
- [Mermaid readability and style notes](#mermaid-readability-and-style-notes)
- [Current-state notes for contributors](#current-state-notes-for-contributors)

## One-screen orientation

```mermaid
flowchart TD
    A[Contributors] --> B[Repository guidance<br/>README.md, CLAUDE.md, docs/]
    B --> C[src/superclaude/<br/>canonical package and distributable assets]

    C --> D[CLI package<br/>superclaude.cli.main:main]
    C --> E[Pytest plugin<br/>superclaude.pytest_plugin]
    C --> F[Framework assets<br/>commands/, skills/, agents/, core/, mcp/, modes/]
    C --> G[Support logic<br/>pm_agent/, execution/, hooks/, scripts/]

    H[pyproject.toml] --> D
    H --> E
    H --> C

    I[Makefile] --> J[Test and verification flows<br/>make test, make verify, make doctor]
    I --> K[Local mirror sync flows<br/>make sync-dev, make verify-sync]
    I --> L[Plugin packaging flows<br/>make build-plugin, make sync-plugin-repo]

    D --> M[Installed CLI usage]
    E --> N[Pytest runtime integration]
    F --> O[Claude-facing assets]
    G --> D
    G --> E

    J --> C
    K --> P[Repo-local .claude/ mirror]
    L --> Q[dist/plugins/superclaude and plugin sync target]

    C --> P
    D --> R[User install targets under ~/.claude/]
    F --> R
```

## High-level system architecture

SuperClaude currently operates as a layered repository, not just a prompt/config bundle. The codebase centers on `src/superclaude/` as the canonical package and asset source, with packaging, test integration, local dev mirrors, and install outputs branching from that core.

```mermaid
flowchart TD
    A[Contributors] --> B[Repository guidance<br/>README.md, CLAUDE.md, docs/]

    B --> C[src/superclaude/<br/>canonical package and distributable assets]

    C --> D[CLI package<br/>superclaude.cli.main:main]
    C --> E[Pytest plugin<br/>superclaude.pytest_plugin]
    C --> F[Framework assets<br/>commands/, skills/, agents/, core/, mcp/, modes/]
    C --> G[Support logic<br/>pm_agent/, execution/, hooks/, scripts/]

    H[pyproject.toml] --> D
    H --> E
    H --> C

    I[Makefile] --> J[Test and verification flows<br/>make test, verify, doctor]
    I --> K[Local mirror sync flows<br/>make sync-dev, verify-sync]
    I --> L[Plugin packaging flows<br/>build-plugin, sync-plugin-repo]

    D --> M[Installed CLI usage]
    E --> N[Pytest runtime integration]
    F --> O[Claude-facing assets]
    G --> D
    G --> E

    J --> C
    K --> P[Repo-local .claude/ mirror]
    L --> Q[dist/plugins/superclaude and external plugin repo]

    C --> P
    D --> R[User install targets under ~/.claude/]
    F --> R
```

## Source-of-truth vs dev-mirror relationships

The current repository instructions are explicit: `src/superclaude/` is the source of truth for distributable components, while `.claude/` contains development-facing mirror copies used directly by Claude Code during local iteration.

This repository also has a second distribution surface: user install targets under `~/.claude/`, reached through the package CLI and install flow.

```mermaid
flowchart LR
    subgraph SOT[Source of truth]
        A1[src/superclaude/commands/*.md]
        A2[src/superclaude/agents/*.md]
        A3[src/superclaude/skills/*]
        A4[src/superclaude Python package code]
    end

    subgraph DEV[Repo-local dev mirror]
        B1[.claude/commands/sc/*.md]
        B2[.claude/agents/*.md]
        B3[.claude/skills/*]
    end

    subgraph INSTALL[User install outputs]
        C1[~/.claude/commands/sc]
        C2[~/.claude/agents]
        C3[~/.claude/skills]
        C4[~/.claude core framework files]
    end

    A1 -->|make sync-dev| B1
    A2 -->|make sync-dev| B2
    A3 -->|make sync-dev| B3

    A1 -->|CLI install flow| C1
    A2 -->|CLI install flow| C2
    A3 -->|CLI install flow| C3
    A4 -->|install_core / packaged runtime| C4

    D[make verify-sync] -. checks drift .-> B1
    D -. checks drift .-> B2
    D -. checks drift .-> B3

    E[pyproject.toml] --> A4
    E --> F[console script: superclaude]
    E --> G[pytest11 entry point]

    H[Makefile] --> D
    H -->|defines sync and validation flows| B1
```

### Practical rule

```mermaid
flowchart TD
    A[Change installable framework asset] --> B[Edit src/superclaude/... first]
    B --> C[Sync to .claude/ if needed]
    C --> D[Run make verify-sync]
    D --> E[Proceed with validation and review]
```

## Console entry points

The package has two executable registration surfaces defined in `pyproject.toml`:

- `superclaude` in `[project.scripts]` is the terminal-facing CLI entry point.
- `superclaude` in `[project.entry-points.pytest11]` is a pytest discovery surface, not a terminal command.

Only the console-script path leads into `src/superclaude/cli/main.py`.

```mermaid
flowchart TD
    A[pyproject.toml] --> B[[project.scripts]]
    A --> C[[project.entry-points.pytest11]]

    B --> D[superclaude = superclaude.cli.main:main]
    D --> E[Console command: superclaude]
    E --> F[Root Click group in src/superclaude/cli/main.py]

    C --> G[superclaude = superclaude.pytest_plugin]
    G --> H[Pytest plugin auto-discovery surface]
    H --> I[Non-CLI execution surface]
```

## Major component map

At contributor level, the most useful map is the component layout inside `src/superclaude/`. The current tree shows a broader implementation surface than older docs sometimes suggest.

```mermaid
flowchart TB
    ROOT[src/superclaude/]

    ROOT --> CLI[cli/]
    ROOT --> PYTEST[pytest_plugin.py]
    ROOT --> PM[pm_agent/]
    ROOT --> EXEC[execution/]
    ROOT --> CMD[commands/]
    ROOT --> SKILLS[skills/]
    ROOT --> AGENTS[agents/]
    ROOT --> CORE[core/]
    ROOT --> MCP[mcp/]
    ROOT --> MODES[modes/]
    ROOT --> HOOKS[hooks/]
    ROOT --> SCRIPTS[scripts/]
    ROOT --> EXAMPLES[examples/]

    CLI --> CLI_MAIN[main.py<br/>root Click group]
    CLI --> CLI_DOCTOR[doctor.py]
    CLI --> CLI_INSTALL[install_core.py<br/>install_commands.py<br/>install_agents.py<br/>install_skill.py<br/>install_skills.py<br/>install_mcp.py]
    CLI --> CLI_PIPELINE[pipeline/]
    CLI --> CLI_AUDIT[audit/]

    PYTEST --> FIXTURES[pytest fixtures and hooks]
    PM --> PM_FILES[confidence.py<br/>self_check.py<br/>reflexion.py<br/>token_budget.py]
    EXEC --> EXEC_FILES[parallel.py<br/>reflection.py<br/>self_correction.py]

    CMD --> CMD_DESC[markdown slash-command assets]
    SKILLS --> SKILLS_DESC[skill packages with SKILL.md<br/>rules, templates, refs, scripts]
    AGENTS --> AGENTS_DESC[agent definition markdown]
    CORE --> CONTENT[framework content layers]
    MCP --> CONTENT
    MODES --> CONTENT
```

## CLI runner and subsystem map

The current command registration shape in `src/superclaude/cli/main.py` separates thin command wiring from the runner and subsystem modules those commands delegate to.

```mermaid
flowchart TD
    A[Console script: superclaude] --> B[src/superclaude/cli/main.py<br/>Click root group: main]

    B --> C[install]
    B --> D[mcp]
    B --> E[update]
    B --> F[install-skill]
    B --> G[doctor]
    B --> H[version]

    C --> C1[install_core.py]
    C --> C2[install_commands.py]
    C --> C3[install_agents.py]
    C --> C4[install_skill.py<br/>list_available_skills]
    C --> C5[install_skills.py]

    D --> D1[install_mcp.py]

    E --> E1[install_core.py]
    E --> E2[install_commands.py]
    E --> E3[install_agents.py]
    E --> E4[install_skills.py]

    F --> F1[install_skill.py<br/>install_skill_command]

    G --> G1[doctor.py<br/>run_doctor]
    G1 --> G2[_check_pytest_plugin]
    G1 --> G3[_check_agents_installed]
    G1 --> G4[_check_skills_installed]
    G1 --> G5[_check_configuration]

    H --> H1[package __version__]

```

## Protocol-backed command relationships

The current repository has a clear split between thin command entry points in `src/superclaude/commands/` and protocol-heavy skills in `src/superclaude/skills/`.

For contributors, the key distinction is:

- command files define invocation UX, flags, boundaries, and when to delegate
- skill packages define the real multi-step workflow
- some commands remain command-defined and do not currently map to a dedicated skill package

```mermaid
flowchart LR
    subgraph Commands[Protocol-backed /sc commands]
        C3[/sc:task]
        C4[/sc:adversarial]
        C5[/sc:cleanup-audit]
        C6[/sc:recommend]
        C7[/sc:pm]
        C8[/sc:validate-tests]
    end

    subgraph Skills[Backing skills / protocols]
        S3[sc:task-protocol]
        S4[sc:adversarial-protocol]
        S5[sc:cleanup-audit-protocol]
        S6[sc-recommend]
        S7[sc:pm-protocol]
        S8[sc:validate-tests-protocol]
    end

    C3 -->|STANDARD / STRICT| S3
    C4 --> S4
    C5 --> S5
    C6 --> S6
    C7 --> S7
    C8 --> S8
```

### Important note

`/sc:task` is special: the command performs tier classification first, then only STANDARD and STRICT paths invoke `sc:task-protocol`; LIGHT and EXEMPT remain command-handled.

## Adversarial workflow as a reusable protocol

`sc:adversarial-protocol` is best understood as a reusable merge-and-pressure-test engine. The standalone `/sc:adversarial` command is one entry point, but the protocol also supports higher-level workflows such as brainstorm and release-split.

```mermaid
flowchart TD
    A[/sc:adversarial] --> B[sc:adversarial-protocol]

    B --> C{Input mode}
    C -->|Mode A| D[Compare existing files]
    C -->|Mode B| E[Generate variants from source]
    C -->|Pipeline mode| F[Multi-phase DAG]

    D --> G[Step 1: diff-analysis.md]
    E --> G
    F --> G

    G --> H[Step 2: debate-transcript.md]
    H --> I[Step 3: base-selection.md]
    I --> J[Step 4: refactor-plan.md]
    J --> K[Step 5: merge-log.md + merged output]

    K --> L[Reusable output for calling workflows]
    L --> O[design/spec comparison families]
```

## Audit and recommendation orchestration family

These flows are both skill-backed (`/sc:recommend` by the `sc-recommend` skill, the other by a `-protocol` skill), but they operate at different layers:

- `/sc:recommend` reads the routing table in the How We Work guide first and, when a row matches, returns that row's ordered steps and mandatory flags; only when no row matches does it enumerate the installed commands and skills, rank them with auggie, and Read-verify each candidate. It does not execute them
- `/sc:cleanup-audit` is a read-only multi-pass audit that writes reports only

```mermaid
flowchart TD
    subgraph Recommend[Recommendation flow]
        R1["/sc:recommend"] --> R2[sc-recommend]
        R2 --> R3["Read routing guide, match a routing row"]
        R3 -->|row matches| R4[Recommended command sequences]
        R3 -->|no match| R3b["Live surface enumeration + auggie rank + Read-verify"]
        R3b --> R4
    end

    subgraph Audit[Repository audit flow]
        A1["/sc:cleanup-audit"] --> A2[sc:cleanup-audit-protocol]
        A2 --> A3[Pass 1: surface scan]
        A3 --> A4[Pass 2: structural audit]
        A4 --> A5[Pass 3: cross-cutting comparison]
        A5 --> A6[Validator + consolidator]
        A6 --> A7[.claude-audit reports]
    end
```

## PM and validation support flows

This is support infrastructure rather than a primary user workflow chain. `/sc:pm` manages continuity and orchestration patterns across sessions, while `/sc:validate-tests` is specialized self-validation for task classification behavior.

```mermaid
flowchart LR
    A[/sc:pm] --> B[sc:pm-protocol]
    B --> C[Session restore from memory]
    C --> D[PDCA work cycle]
    D --> E[Sub-agent orchestration patterns]
    E --> F[Checkpoint + memory writeback]

    G[/sc:validate-tests] --> H[sc:validate-tests-protocol]
    H --> I[Load YAML behavioral test specs]
    I --> J[Run tier-classification logic]
    J --> K[Compare expected vs actual]
    K --> L[Validation report]
```

## Task-surface deprecation map

`task.md` (`/sc:task`) is the active task command; it invokes the `sc-task-protocol` skill for STANDARD and STRICT tiers.

```mermaid
flowchart LR
    C[task.md<br/>active /sc:task surface]
    C --> D[sc:task-protocol]
    D --> E[STANDARD / STRICT execution paths]
```

## Choosing the right change surface

This decision path is especially useful for contributors working across CLI, plugin, runtime, and generated-doc boundaries.

```mermaid
flowchart TD
    A[Start with the requested change] --> B{What execution surface is changing?}

    B -->|Terminal command behavior,<br/>command registration,<br/>CLI options, subgroup wiring| C[Edit src/superclaude/cli/]
    B -->|Pytest plugin behavior,<br/>PM agent logic,<br/>execution helpers| D[Edit non-CLI Python package surfaces]
    B -->|Plugin packaging or plugin asset layout| E[Edit plugin/build surfaces]
    B -->|Generated contributor documentation only| F[Edit docs/generated/ only]

    C --> C1[Start with pyproject.toml if entry-point wiring changes]
    C --> C2[Then inspect src/superclaude/cli/main.py]
    C --> C3[Then inspect the delegated module or workflow package]

    D --> D1[Typical surfaces:<br/>src/superclaude/pytest_plugin.py<br/>src/superclaude/pm_agent/<br/>src/superclaude/execution/]

    E --> E1[Plugin source/build surfaces:<br/>plugins/superclaude/...<br/>make build-plugin<br/>make sync-plugin-repo]
    E --> E2[Do not treat plugin output repos as primary edit targets]

    F --> F1[Ground claims in current code]
    F --> F2[Prefer generated inventory + live source over older prose]

    C3 --> G[Validate the smallest matching proof]
    D1 --> G
    E2 --> G
    F2 --> G

    G --> G1[CLI change: relevant CLI tests / make doctor / make verify]
    G --> G2[Python runtime change: uv run pytest ...]
    G --> G3[Plugin packaging change: build-plugin or sync-plugin-repo validation]
    G --> G4[Docs-only change: verify paths, symbols, and claims against repo state]
```

## Repository map outside the package

```mermaid
flowchart TB
    ROOT[SuperClaude_Framework/]
    ROOT --> SRC[src/]
    ROOT --> CLAUDE[.claude/]
    ROOT --> TESTS[tests/]
    ROOT --> DOCS[docs/]
    ROOT --> SCRIPTS[scripts/]
    ROOT --> PLUGINS[plugins/]
    ROOT --> VENDOR[.vendor/]
    ROOT --> DEV[.dev/]
    ROOT --> PYPROJECT[pyproject.toml]
    ROOT --> MAKE[Makefile]
    ROOT --> README[README.md]
    ROOT --> CLAUDEMD[CLAUDE.md]

    SRC --> PACKAGE[src/superclaude/]
    DOCS --> GENERATED[docs/generated/]
    GENERATED --> BUNDLE[contributor-knowledge-base/]
```

## Where to go next

Use this page as the hub, then jump to the generated document that matches your question:

- [README for this generated bundle](./README.md) — audience, scope, and reading order
- [Repository Overview](./repository-overview.md) — top-level layout and repository identity
- [Architecture Guide](./architecture-guide.md) — layered architecture and current-code interpretation
- [Components Guide](./components-guide.md) — subsystem-by-subsystem contributor map
- [Contributor Workflow Guide](./contributor-workflow.md) — how to work safely in the repo
- [CLI API Inventory](./cli-api-inventory.md) — module-by-module CLI package inventory
- [Commands Reference](../../user-guide/commands.md) — per-command syntax and options

## Mermaid readability and style notes

When reading these diagrams in GitHub markdown:

- use the table of contents to navigate one diagram section at a time
- treat the heading and nearby bullets as the legend for each graph
- zoom the page rather than copying diagrams out immediately
- jump to the linked detailed document when a diagram is summarizing too much at once

Authoring guidance used in this generated bundle:

- one diagram per architectural question
- avoid overloading a single graph with every subsystem
- keep node labels tied to real repo paths and current entry points
- prefer current code over older prose when diagramming relationships
- use top-to-bottom for layered systems and left-to-right for source/flow comparisons

## Current-state notes for contributors

- Current package metadata identifies `superclaude` version `4.2.0` with Python `>=3.10`.
- Current executable entry points are the CLI (`superclaude.cli.main:main`) and pytest plugin (`superclaude.pytest_plugin`).
- Current code shows a larger CLI tree than some older docs imply, including `pipeline` and `audit` subsystems.
- Current protocol-backed command families include task, adversarial, cleanup-audit, pm, and validate-tests; recommend is backed by the sc-recommend skill (no -protocol suffix).
- For conflicts between older architecture prose and the present tree, prefer `src/superclaude/`, `pyproject.toml`, `CLAUDE.md`, and `Makefile`.
