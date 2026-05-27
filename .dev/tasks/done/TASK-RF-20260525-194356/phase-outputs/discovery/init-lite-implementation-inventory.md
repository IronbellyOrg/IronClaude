# Implementation Inventory: superclaude init-lite --context-optimized

**Task:** TASK-RF-20260525-194356
**Date:** 2026-05-27
**Source-of-truth root:** `src/superclaude/`
**Worktree note:** This task executes inside the worktree `.claude/worktrees/task-rf-20260525-194356/`. All absolute `/config/workspace/IronClaude/...` paths in the task file resolve to the worktree's repo root.

This inventory is the implementation map for Phases 2-4. Every file listed is backed by research citations (research/01-04 + research-notes.md). No content is fabricated beyond cited research.

## Source Files To Create

| Path | Purpose | Evidence |
|------|---------|----------|
| `src/superclaude/cli/init_lite.py` | Focused Click module implementing the `init-lite` command, surface discovery, deterministic `ceil(bytes / 4)` token estimate, low/medium/high thresholds, report writer with generated marker, dry-run handling, scaffold creation, force-overwrite gating, and output ownership check. | research-notes.md:25 ("Add CLI support module, suggested: `src/superclaude/cli/init_lite.py`"); research/01-cli-registration.md:25 (TASK-DECISION: focused module registered additively); research/03-report-scaffold-behavior.md:20-23 (mkdir behavior, dry-run no-write, scaffold opt-in, force overwrite); research/03-report-scaffold-behavior.md:28 (ceil(bytes/4) and low/medium/high thresholds); research/03-report-scaffold-behavior.md:37 (generated marker string). |
| `src/superclaude/commands/init-lite.md` | Thin `/sc:init-lite` dispatcher with YAML frontmatter (`name: init-lite`, description, category, complexity, mcp-servers, personas), Usage, flags table, behavior summary, mandatory Activation invoking `Skill sc-init-lite-protocol`, Examples, Boundaries. | research-notes.md:27; research/02-command-skill-patterns.md:54-58 (existing thin dispatcher patterns); research/02-command-skill-patterns.md:99-104 (recommended command skeleton constraints); research/02-command-skill-patterns.md:38-44 (mandatory Activation handoff pattern). |
| `src/superclaude/skills/sc-init-lite-protocol/SKILL.md` | Protocol skill frontmatter (name, description, allowed-tools without `Edit`, argument-hint) + body sections stating "invoked only by /sc:init-lite", safe audit/report workflow, dry-run/default/scaffold/force behavior, target-project no-mutation rules, deterministic token estimate+thresholds, report/scaffold outputs, lazy-ref loading instructions. | research-notes.md:28; research/02-command-skill-patterns.md:65-73 (protocol skill frontmatter patterns + allowed-tools without Edit); research/02-command-skill-patterns.md:106-111 (suggested skill skeleton constraints). |
| `tests/cli/test_init_lite.py` | Focused behavior tests using `click.testing.CliRunner` against `superclaude.cli.main:main`. Covers token estimate, surface discovery, dry-run no-write, default report with marker, scaffold opt-in, CLAUDE.md byte preservation, idempotency, help flags, no-`.claude/`-writes. | research-notes.md:29; research/04-test-verification.md:20-31 (10 required test cases); research/01-cli-registration.md:32-33 (live-Click invocation pattern). |

## Source Files To Modify

| Path | Change | Evidence |
|------|--------|----------|
| `src/superclaude/cli/main.py` | Append deferred-import + `main.add_command(...)` for the `init-lite` command, matching the existing pattern at lines 400-426. | `src/superclaude/cli/main.py:400-426` (existing additive registration block); research/01-cli-registration.md:24 (additive registrations evidence). |
| `src/superclaude/cli/install_skills.py` | Update `_has_corresponding_command` so a directory named `sc-<command>-protocol` maps to `commands/<command>.md` (treated as command-backed). Preserve existing `sc-<command>` behavior. Keep stale-removal path and accuracy of output messages. | `src/superclaude/cli/install_skills.py:19-30` (current strip-`sc-` only); `src/superclaude/cli/install_skills.py:58-68` (skip + stale removal); research/02-command-skill-patterns.md:88 (current behavior produces wrong mapping for `sc-init-lite-protocol`); research/02-command-skill-patterns.md:117 (TASK-DECISION: either rename or fix installer — task scope chooses the fix). |
| `tests/cli/test_cli_registration.py` | Add `"init-lite"` to `EXPECTED_TOP_LEVEL_COMMANDS` frozenset; add a focused test asserting `init-lite --help` exposes required flags (`--context-optimized`, `--dry-run`, `--output`, `--project-root`, `--scaffold`, `--force`). | `tests/cli/test_cli_registration.py:31-48` (frozen roster); `tests/cli/test_cli_registration.py:107-118` (smoke help loop already covers any added command); research/01-cli-registration.md:30,33; research/04-test-verification.md:29-30. |

## Tests To Create Or Modify

| Path | Action | Evidence |
|------|--------|----------|
| `tests/cli/test_init_lite.py` | Create. 10 required behavior tests (see Source Files To Create row above). | research/04-test-verification.md:20-31. |
| `tests/cli/test_cli_registration.py` | Modify roster + add flag-help test. | `tests/cli/test_cli_registration.py:29-48`, `:73-82`, `:108-119`. |
| `tests/cli/test_init_lite.py` (installer mapping section) | Add installer mapping coverage proving `sc-init-lite-protocol` resolves to `commands/init-lite.md` and is treated as command-backed; `sc-<command>` mapping still works; unrelated skills without matching commands still install normally. Co-locating with `test_init_lite.py` is acceptable per task Step 3.3 ("even if they live inside `tests/cli/test_init_lite.py`"). No existing pure-unit module covers `_has_corresponding_command` directly (`tests/cli/test_install_failures.py:1-50` covers a different invariant; `tests/unit/test_cli_install.py` does not exercise `install_skills`). | `src/superclaude/cli/install_skills.py:19-30,58-68`; `tests/cli/test_install_failures.py:1-50`; task file Step 3.3 acceptance note. |

## Safety Invariants

| Invariant | Source |
|-----------|--------|
| Default discovery scope is project-local only: `CLAUDE.md`, `.mcp.json`, `.claude/settings.json`, `.claude/commands/**`, `.claude/skills/**/SKILL.md`, `.claude/agents/*.md`. | research/03-report-scaffold-behavior.md:27. |
| `--dry-run` writes nothing and does not create `.dev/superclaude/`. | research/03-report-scaffold-behavior.md:21,36; research/04-test-verification.md:24. |
| Default run writes only the report at `.dev/superclaude/context-audit.md` (or `--output`) with marker `<!-- generated-by: superclaude init-lite context-audit v1 -->`. | research/03-report-scaffold-behavior.md:22,37; research/04-test-verification.md:25. |
| `--scaffold` creates only `.dev/superclaude/project-guidance/SKILL.md` and `.dev/superclaude/project-guidance/refs/README.md` under `.dev/superclaude/`. | research/03-report-scaffold-behavior.md:22; research/04-test-verification.md:26. |
| `--force` may overwrite owned report/scaffold paths under `.dev/superclaude/` only. NEVER overwrites `CLAUDE.md`, `.mcp.json`, `.claude/settings.json`, `.claude/commands/**`, `.claude/skills/**`, `.claude/agents/**`. | research/03-report-scaffold-behavior.md:23,37. |
| If existing output file lacks the generated marker and `--force` is false, fail with a clear Click error rather than overwriting. | research/03-report-scaffold-behavior.md:37. |
| Token estimate formula is deterministic `ceil(bytes / 4)`; thresholds: low < 1000, medium 1000-4000, high > 4000. These thresholds are NEW (no prior code) and tests pin them. | research/03-report-scaffold-behavior.md:28; research/04-test-verification.md:22. |
| `CLAUDE.md` byte identity preserved across dry-run/default/scaffold/force modes. | research/04-test-verification.md:27. |
| `.claude/` mirrors under target project never created or modified by the feature. | research/03-report-scaffold-behavior.md:23; research/04-test-verification.md:31. |
| `Edit` is not in `allowed-tools` of the protocol skill (report/audit-style skill). | research/02-command-skill-patterns.md:111. |
| `.claude/` mirrors at IronClaude development level changed only by `make sync-dev`; never instruct staging of `.claude/` paths. | research-notes.md:21,38; CLAUDE.md (project) absolute rule. |

## Validation Commands

Use UV/make only. From repo root (the worktree root in this execution):

1. `uv run pytest tests/cli/test_init_lite.py tests/cli/test_cli_registration.py -v` — focused CLI behavior + registration regression. (Source: research/04-test-verification.md:37; pyproject.toml:64-66.)
2. `uv run pytest <installer-test-selection> -v` — targeted installer mapping coverage. Selection = node IDs inside `tests/cli/test_init_lite.py` (or `tests/cli/test_cli_registration.py`) added by this task. (Source: task file Step 4.2; research/02-command-skill-patterns.md:84-89.)
3. `make sync-dev` — sync `src/superclaude/{skills,agents,commands}` into `.claude/`. (Source: research/04-test-verification.md:38; Makefile:108-136.)
4. `make verify-sync` — confirm `src/` and `.claude/` are in sync after edits. (Source: research/04-test-verification.md:39; CLAUDE.md project absolute-rule on `.claude/` discipline.)
5. `make lint` — ruff lint via UV. (Source: research/04-test-verification.md:40; Makefile:47-50.)

## Installer Mapping Decision

**Decision: Fix `install_skills.py` (do NOT rename the skill directory).**

- Keep the requested protocol-skill directory name `sc-init-lite-protocol/` because the existing convention in this codebase already uses `sc-<command>-protocol/` (e.g., `sc-recommend-protocol/`, `sc-pm-protocol/`, `sc-roadmap-protocol/`, `sc-cli-portify-protocol/`).
- Update `_has_corresponding_command` to also recognise `sc-<command>-protocol` and map it to `commands/<command>.md`. Order of checks: try `sc-<name>` against `commands/<name>.md` first; if `name` ends in `-protocol`, also try `commands/<name without -protocol suffix>.md`.
- Net effect: a directory named `sc-init-lite-protocol` will resolve to `commands/init-lite.md` and be treated as command-backed (skipped from standalone install with stale removal). Unrelated `sc-<command>` skills without a `-protocol` suffix continue to use the existing path. Skills without a matching command (no `sc-` prefix, or no command file) still install normally.

Evidence for this decision:

- Existing convention uses `sc-<command>-protocol` widely: research/02-command-skill-patterns.md:89 lists current protocol skills.
- Existing installer behavior misses this mapping: `src/superclaude/cli/install_skills.py:19-30` strips only the literal `sc-` prefix.
- The task file Step 2.3 directly mandates this fix.

## Open Questions / Risks

- The CLI module shape inside `src/superclaude/cli/init_lite.py` may need internal helper extraction to keep the Click command readable. The task scope allows helper functions within the same module — no subpackage is required for this small feature (research-notes.md:42).
- The `--output` flag accepts a path; ownership check uses the generated marker (research/03-report-scaffold-behavior.md:37). The implementation must reject non-marker existing outputs without `--force` rather than overwriting.
- Tests use temporary directories; assertions for "no `.claude/` writes" must verify both creation (when absent) and content stability (when present).
