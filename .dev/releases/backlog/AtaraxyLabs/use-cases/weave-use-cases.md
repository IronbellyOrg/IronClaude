# Weave Use-Case Report for IronClaude/SuperClaude

> Produced: 2026-06-04. Grounded in actual repo structure, branch history, and dev model.

---

## What Weave Brings to IronClaude

IronClaude's development model is **heavy parallel worktree usage**: CLAUDE.md mandates `git worktree` for running multiple Claude Code sessions simultaneously, the repo currently has **7 active worktrees** plus the main tree and an external worktree, and developers routinely edit the same `src/superclaude/` Python package from independent branches (e.g., `feat/sprint-auto-resume-v435`, `feat/sc-reflect-v3-serena-low-impl`, `refactor/roadmap-pipeline-r0-r1-rewrite`) that converge onto `integration` and then `master`. When two sessions independently modify different functions in the same Python file (e.g., one edits `src/superclaude/cli/sprint/executor.py` while another edits `src/superclaude/cli/sprint/process.py` -- both under `cli/sprint/`), Git's line-based merge produces false conflicts on adjacent imports, docstrings, and blank lines. Weave's entity-level merge using tree-sitter parses Python into functions/classes and merges at that granularity, eliminating these false conflicts entirely. The value is concentrated in the **~247 Python files** under `src/superclaude/`; the ~70,000 `.md` files (mostly `.dev/` artifacts and skill definitions) fall back to line-merge, which is weave's weakest area.

---

## Concrete Use Cases (ranked by value)

### UC-1: Parallel Sprint + Roadmap CLI Development (Highest Value)

**Scenario:** Two Claude sessions in separate worktrees each work on a different CLI subpackage -- one on `src/superclaude/cli/sprint/executor.py` (e.g., adding auto-resume logic on branch `feat/sprint-auto-resume-v435`) and another on `src/superclaude/cli/roadmap/executor.py` (e.g., brittleness fixes on `refactor/roadmap-pipeline-r0-r1-rewrite`). Both touch their respective `executor.py` files, but both packages also import from shared modules like `src/superclaude/cli/pipeline/models.py` and `src/superclaude/cli/__init__.py`. When both branches merge to `integration`, Git sees line-level conflicts on the shared import blocks and top-of-file headers even though the actual code changes are in completely independent functions.

**Weave command:** `weave setup --local` in each worktree before merging into `integration`. Use `weave preview` first to verify no false conflicts on shared modules.

**Status-quo pain:** Manual resolution of import-block conflicts, header/diff conflicts, and `__init__.py` rebase collisions. In the recent history, 152 commits touched Python files since May 2026, many on parallel branches (sprint fixes on `fix/sprint-fake-popen-stdin-*` while roadmap work happened on `refactor/roadmap-*`). Each false-conflict merge costs 5-15 minutes of careful reading to confirm "these are adjacent-line touches, not semantic collisions."

**Net value:** Eliminates false conflicts on entity-disjoint Python edits. For a repo with 247 Python files and 7+ concurrent worktree branches touching overlapping file neighborhoods (sprint has 19 `.py` files, roadmap has 26, pipeline has 23, all sharing `cli/` imports), this could save 30+ minutes per merge cycle across the ~30 merge commits visible in recent history.

**Caveat:** If both sessions edit the *same function* (e.g., both modify `execute_phase()` in `src/superclaude/cli/sprint/executor.py`), weave correctly preserves the true conflict with semantic markers. This is the desired behavior -- true conflicts must surface. Also, weave falls back to line-merge for files >1MB (not a concern for Python here).

---

### UC-2: `make sync-dev` Mirror Drift Resolution

**Scenario:** The `make sync-dev` target (Makefile lines 109-163) copies `src/superclaude/skills/` into `.claude/skills/`, `src/superclaude/agents/` into `.claude/agents/`, and `src/superclaude/commands/` into `.claude/commands/sc/`. When a developer on one worktree edits a skill's `src/superclaude/skills/sc-sprint-protocol/SKILL.md` and another edits `src/superclaude/skills/sc-roadmap-protocol/SKILL.md`, both run `make sync-dev` which overwrites the `.claude/` mirrors. If `.claude/settings.json` is also edited in both trees (hook registrations, permission changes), the subsequent merge into `integration` hits conflicts on the generated `.claude/` files.

**Weave command:** `weave setup --local` scoped to the worktree. `weave preview` on the merge into `integration`.

**Status-quo pain:** The `.claude/` directory contains generated mirrors that both-modify during parallel sync-dev runs. While `.claude/` is mostly gitignored (only `settings.json` is tracked), the `settings.json` file accumulates edits from concurrent hook-wiring work. Conflicts on this single file require manual resolution to merge independent hook registrations.

**Net value:** Weave's tree-sitter JSON parsing cleanly merges independent edits to `settings.json` (adding different hook entries or permissions). For the settings.json file specifically, this eliminates the "which hook registration wins" manual inspection.

**Caveat:** The bulk of `.claude/` (skills, commands, agents) is generated and gitignored -- weave doesn't help there because Git never tracks them. The value is concentrated on the one tracked file: `.claude/settings.json`. This is a small surface.

---

### UC-3: Multi-Feature PR Integration onto `integration` Branch

**Scenario:** The branch structure is `master` <- `integration` <- `feature/*, fix/*, docs/*`. Multiple feature branches land on `integration` in quick succession: `feat/sc-reflect-v3-serena-low-impl`, `feat/sprint-auto-resume-v435`, `feat/sc-recommend-lookup-cache`, plus fix branches like `fix/sprint-fake-popen-stdin-attr`. When `integration` absorbs 3-4 PRs in a day, the merge commits (30+ in recent history) routinely produce conflicts on:

- `src/superclaude/cli/sprint/models.py` -- dataclass additions by different branches
- `src/superclaude/cli/roadmap/models.py` -- same pattern
- `src/superclaude/cli/pipeline/models.py` -- shared pipeline schema
- Test files under `tests/` -- ~449 Python test files growing independently

**Weave command:** `weave setup --local` on the `integration` branch worktree. `weave preview` before each feature merge.

**Status-quo pain:** Each merge-to-integration requires reading conflict markers to distinguish "same function modified" (true conflict) from "adjacent function/class added" (false conflict). The `models.py` files with their dataclass definitions are especially prone to false conflicts when two branches add different dataclasses. Manual resolution takes 5-20 minutes per merge depending on PR size.

**Net value:** Weave's Python entity recognition cleanly merges independent class/function additions. For a merge absorbing 4 feature branches touching the same `models.py` file, each adding different dataclasses, weave eliminates all false conflicts. Estimated 10-15 minutes saved per integration merge.

**Caveat:** True conflicts (both branches modifying the same dataclass or function) are preserved correctly. The `--local` scope is mandatory -- never global `weave setup` per the merged-requirements spec. If `integration` merge produces a true conflict, the developer still resolves it manually; weave just eliminates the noise.

---

### UC-4: Test Suite Parallel Development

**Scenario:** The `tests/` directory contains 449 Python test files. When multiple worktrees independently add tests for different modules (e.g., one worktree adds `tests/cli/test_init_lite.py` with 385 lines of new tests while another fixes `tests/unit/test_cli_install.py`), the test directories grow in parallel. Additionally, test files under `tests/cli/sprint/`, `tests/roadmap/`, and `tests/unit/` are modified alongside their corresponding source files in separate worktrees.

**Weave command:** `weave setup --local` on whichever worktree performs the merge. `weave preview` to verify clean entity-level merge.

**Status-quo pain:** Test files often import from the same conftest fixtures, share setup code, or modify adjacent test classes. Git's line merge produces conflicts on import blocks, fixture definitions, and class boundaries even when the actual test additions are semantically independent.

**Net value:** Weave's Python parsing recognizes test function/class boundaries, merging independent test additions cleanly. For parallel test development across 7 worktrees, this reduces false-conflict resolution on test files.

**Caveat:** Weave's Python support is strong (tree-sitter-python is mature), but the value per file is lower than source code because test files are typically more append-heavy (adding new test functions) rather than modifying existing ones. Git handles pure appends well; weave helps most when there are structural additions near existing code that git misreads as conflicts.

---

### UC-5: `sc:git` Skill Integration as Advisory Merge Assistant

**Scenario:** The `sc:git` skill (`src/superclaude/commands/git.md`) already provides "intelligent commit messages" and "guided merge with conflict resolution." Weave integrates here as an opt-in merge driver: when `weave setup --local` is active in a worktree, the `sc:git merge` flow can offer `weave preview` output before attempting a native git merge, showing the developer whether entity-level merge would produce clean results.

**Weave command:** `weave preview` invoked by the `sc:git` skill as a pre-merge advisory step. `weave setup --local` to enable the driver.

**Status-quo pain:** Currently, merge conflicts are discovered after `git merge` fails, requiring the developer to enter merge state, inspect conflicts, and decide whether to abort. This is reactive and disruptive.

**Net value:** Proactive `weave preview` in the `sc:git` flow tells the developer "this merge will be clean at the entity level" before committing to it. For a repo with 7+ active worktrees and frequent merges, this provides confidence and saves the time of entering/exiting failed merge states.

**Caveat:** This requires weaving `weave preview` into the `sc:git` skill definition (`.md` file), which is exactly the kind of Markdown change weave is weakest on. The skill file itself would be edited manually; weave only helps with the Python CLI code that might implement the weave preview invocation. Additionally, MCP tool names for weave are undocumented -- the skill would need to invoke the CLI, not an MCP tool, until names are enumerated.

---

## Where Weave Does NOT Help

### Markdown Skill Files (Weakest Area)

The repo contains **~230 `.md` files under `src/superclaude/`** (skills, commands, agents, core docs) and **~70,000 `.md` files total** (dominated by `.dev/` artifacts, release notes, task files, research). Weave's tree-sitter parsers handle code languages well but Markdown support is explicitly its weakest area. The SKILL.md files that comprise the framework's behavior (e.g., `sc-auggie-review-protocol`, `sc-reflect-protocol`, `sc-brainstorm-protocol`) are Markdown with YAML frontmatter. When two sessions independently edit different sections of the same SKILL.md, weave will likely fall back to line-merge -- which is what Git already does. **No value here.**

### Generated `.claude/` Mirrors

The `.claude/skills/`, `.claude/commands/`, `.claude/agents/` directories are **gitignored** generated output of `make sync-dev`. Weave only helps with tracked files during git merge. The only tracked file under `.claude/` is `settings.json`, limiting this surface to one file.

### True Semantic Conflicts

When two developers genuinely modify the same function (e.g., both edit `run_classifier()` in `src/superclaude/cli/sprint/classifiers.py`), weave correctly preserves the conflict with semantic markers. This is correct behavior but provides no time savings over Git -- the developer still resolves it manually. Weave's value is exclusively in eliminating **false** conflicts (independent edits to the same file).

### >1MB Files and Binaries

Weave falls back to line-merge for files >1MB and all binary files. The repo has no Python files approaching this size, so this is not a practical concern.

### Branch Creation and Daily Work

Weave only activates at merge time. It does nothing for the daily work of editing, committing, or pushing. The value is realized entirely when branches converge -- feature into integration, integration into master, or worktree reconciliation.

---

## Summary: Value Concentration

Weave's value in IronClaude is **highly concentrated in Python merges across parallel worktrees**:

| Surface | Python Files | Weave Benefit | Markdown Files | Weave Benefit |
|---------|-------------|---------------|----------------|---------------|
| `src/superclaude/cli/` | ~170 | High | -- | -- |
| `src/superclaude/skills/` | ~20 (init/__init__) | Low | ~210 | None (weakest) |
| `src/superclaude/pm_agent/` | 4 | Medium | -- | -- |
| `src/superclaude/execution/` | 3 | Medium | -- | -- |
| `tests/` | 449 | Medium | -- | -- |
| `.claude/settings.json` | -- | -- | 1 (JSON) | Low |
| `.dev/` | ~30 | Medium | ~70,000 | None |

The business case: **7 active worktrees + 152 Python commits since May + 30 merge commits = frequent false-conflict opportunities on shared Python files**. Weave `setup --local` + `preview` addresses this cleanly for the Python substrate, while providing no benefit for the Markdown-heavy skill ecosystem that comprises the bulk of the framework's behavior.
