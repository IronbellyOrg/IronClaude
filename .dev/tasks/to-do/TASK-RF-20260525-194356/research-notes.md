# Research Notes: Implement context-optimized init-lite

**Date:** 2026-05-25
**Scenario:** A — explicit goal from design/spec-panel output
**Depth Tier:** Standard
**Track Count:** 1
**Status:** Complete

---

## EXISTING_FILES

Key source files and directories for implementation:

- `src/superclaude/cli/main.py` — Click root command surface. Top-level Click command group is defined at `src/superclaude/cli/main.py:18`; manually registered subgroups are appended at `src/superclaude/cli/main.py:400` through `src/superclaude/cli/main.py:426`.
- `tests/cli/test_cli_registration.py` — pins top-level CLI command roster and help behavior; adding `init-lite` must update `EXPECTED_TOP_LEVEL_COMMANDS` and related help smoke tests.
- `src/superclaude/commands/` — source-of-truth for `/sc:*` command markdown files; current command files include thin dispatchers such as `src/superclaude/commands/roadmap.md`.
- `src/superclaude/commands/roadmap.md` — example thin dispatcher: it mandates invoking a protocol skill and says not to execute from the command file alone at `src/superclaude/commands/roadmap.md:71` through `src/superclaude/commands/roadmap.md:79`.
- `src/superclaude/skills/` — source-of-truth for skill packages. New protocol skill should follow existing protocol naming as `src/superclaude/skills/sc-init-lite-protocol/SKILL.md`.
- `src/superclaude/cli/install_skills.py` — current standalone-skill skip logic strips only `sc-`, so `sc-init-lite-protocol` maps to `commands/init-lite-protocol.md`, not `commands/init-lite.md`. The task must either add installer handling for `sc-<command>-protocol` or explicitly accept standalone protocol-skill installation. Recommended decision: keep the existing protocol naming pattern and add installer tests/fix so protocol skills with matching command names are not installed as standalone skills.
- `CLAUDE.md` — project constraints: UV-only at `CLAUDE.md:5` through `CLAUDE.md:7`; `/sc:*` commands must invoke corresponding skills at `CLAUDE.md:9` through `CLAUDE.md:14`; `.claude/` mirrors must not be staged or treated as source-of-truth at `CLAUDE.md:16` through `CLAUDE.md:24`.

Implementation files likely needed:

- Add CLI support module, suggested: `src/superclaude/cli/init_lite.py` or `src/superclaude/cli/init_lite/commands.py`.
- Modify `src/superclaude/cli/main.py` to register `init-lite`.
- Add `src/superclaude/commands/init-lite.md`.
- Add `src/superclaude/skills/sc-init-lite-protocol/SKILL.md` and update `src/superclaude/cli/install_skills.py` so `sc-<command>-protocol` skills with matching `commands/<command>.md` are treated as command-backed protocol skills rather than standalone install targets.
- Add tests under `tests/cli/`, likely `tests/cli/test_init_lite.py`, and update `tests/cli/test_cli_registration.py`.

## PATTERNS_AND_CONVENTIONS

- CLI uses Click decorators and `click.echo`; root command lives in `src/superclaude/cli/main.py`.
- Some feature-heavy CLI areas use subpackages and command groups (`roadmap`, `cleanup-audit`, `tasklist`, `cli-portify`, `prd`, `eval`) registered near the end of `src/superclaude/cli/main.py`.
- Thin `/sc:*` commands should include usage, examples, boundaries, and an activation section that invokes a skill; the roadmap command is a current example.
- Protocol-heavy behavior should live in a skill, not the command markdown.
- Existing protocol skills use `sc-*-protocol` naming, but current installer skip logic does not map `sc-<command>-protocol` to `commands/<command>.md`; task scope must include the installer mapping fix if `sc-init-lite-protocol` is used.
- Project source-of-truth is `src/superclaude/`; `.claude/` mirrors are sync-dev output and should not be edited/staged directly.

## GAPS_AND_QUESTIONS

- Resolved: prefer a focused CLI module or package for `init-lite`, registered additively from `src/superclaude/cli/main.py`, rather than expanding inline logic in `main.py`.
- Resolved: report and optional scaffold artifacts belong under `.dev/superclaude/`; there is no reusable report helper required for this small feature.
- Resolved: command/skill source assets should follow the thin-command plus protocol-skill pattern, with protocol naming `sc-init-lite-protocol` and an accompanying installer mapping fix for `sc-<command>-protocol` skills.
- Resolved: tests should use `CliRunner` against `superclaude.cli.main:main`, update the frozen top-level roster, and add focused `init-lite` behavior tests.

## RECOMMENDED_OUTPUTS

Research files to create:

1. `.dev/tasks/to-do/TASK-RF-20260525-194356/research/01-cli-registration.md` — CLI registration, Click patterns, tests.
2. `.dev/tasks/to-do/TASK-RF-20260525-194356/research/02-command-skill-patterns.md` — `/sc:*` command and protocol skill source conventions.
3. `.dev/tasks/to-do/TASK-RF-20260525-194356/research/03-report-scaffold-behavior.md` — context surface discovery, report writing, `.dev` output, no `.claude/` writes.
4. `.dev/tasks/to-do/TASK-RF-20260525-194356/research/04-test-verification.md` — test plan, target tests, commands, sync validation.

## SUGGESTED_PHASES

Researcher 1 — CLI Registration:
- Topic type: File Inventory + Integration Points
- Scope: `src/superclaude/cli/main.py`, `src/superclaude/cli/*`, `tests/cli/test_cli_registration.py`
- Output: `research/01-cli-registration.md`
- Other researchers cover command/skill markdown and report behavior; do not duplicate those.

Researcher 2 — Command & Skill Patterns:
- Topic type: Patterns & Conventions + Template & Examples
- Scope: `src/superclaude/commands/*.md`, `src/superclaude/skills/*/SKILL.md`, `src/superclaude/cli/install_skills.py`
- Output: `research/02-command-skill-patterns.md`
- Other researchers cover CLI code and tests; focus on markdown/source-of-truth patterns.

Researcher 3 — Report & Scaffold Behavior:
- Topic type: Patterns & Conventions + Integration Points
- Scope: `.dev/`, docs mentioning `.dev/superclaude`, existing report writers under `src/superclaude/cli/**`, project `CLAUDE.md` source-of-truth constraints
- Output: `research/03-report-scaffold-behavior.md`
- Focus on safe artifact locations and idempotency rules.

Researcher 4 — Test & Verification:
- Topic type: Test & Verification
- Scope: `tests/cli/`, `tests/test_*.py`, `Makefile`, `pyproject.toml`
- Output: `research/04-test-verification.md`
- Focus on exact tests and validation commands using UV/make only.

## TEMPLATE_NOTES

Use MDTM Template 02 (Complex Task). Rationale: the task-builder template-selection rule maps "Build X with tests" and "Refactor X and verify nothing breaks" to Template 02 at `src/superclaude/skills/task-builder/SKILL.md:237` through `src/superclaude/skills/task-builder/SKILL.md:246`; the Template 02 triage says to use Template 02 for discovery before building, multiple phases, conditional flows, and quality gates at `src/superclaude/skills/task-builder/SKILL.md:390` through `src/superclaude/skills/task-builder/SKILL.md:408`. This feature requires multiple conditional implementation/verification phases: add CLI behavior, update installer protocol-skill handling, add command/skill source assets, add report/scaffold generation, add tests, run sync verification, and remediate failures if validation fails.

Tier: Standard. Scope is moderate and localized to CLI/command/skill/test files. It is not multi-track because all deliverables contribute to one cohesive feature; track-splitting rules say not to split when work items build on each other or share source context that must be understood holistically at `src/superclaude/skills/task-builder/SKILL.md:232` through `src/superclaude/skills/task-builder/SKILL.md:235`.

Generated task should include per-file checklist items for each implementation target. It must preserve the invariant that `CLAUDE.md` is never modified by the new command and `.claude/` mirrors are not written by the feature in ordinary target projects.

## AMBIGUITIES_FOR_USER

None — intent is clear from the request and codebase context. The user wants a simple, non-destructive `init-lite --context-optimized` implementation task file based on the critiqued design.
