# QA Report: Registration lens (impl-cli gate)

**Topic:** `superclaude sweep` registration in `src/superclaude/cli/main.py` and the lazy export in `src/superclaude/cli/sweep/__init__.py`
**Date:** 2026-11-12
**Phase:** code gate, registration lens (task item T202)
**Fix authorization:** false (no file edited except this report)
**Fix cycle:** N/A (first review)

## Scope and method

Read `src/superclaude/cli/main.py:500-574`, `src/superclaude/cli/sweep/__init__.py` (all 12 lines), `src/superclaude/cli/recommend/__init__.py` (the pattern DESIGN names), `src/superclaude/cli/sweep/commands.py:1-288` in two chunks, `git diff -- src/superclaude/cli/main.py`, `step-1.7-help.txt`, `phase9-validation.md`, and DESIGN (`docs/designs/orchestrator-mode.md`) lines 28, 196-216, 351-362, 937 and 973.
Ran only read-only checks: `ruff check --no-cache`, `ruff format --check --no-cache`, `superclaude sweep --help`, `superclaude sweep run --help`, `superclaude --help`, and three scratch snippets run with `uv run python -I` from a private `/tmp/regqa.*` folder (deleted afterwards; `ls /tmp | grep -c regqa` printed 0). No live Orca command was run.

## Findings

No BLOCKING or MAJOR finding. Three MINOR notes.

### R-1 (MINOR) The "no import until read" property cannot be seen through a plain import in a real interpreter

- Evidence: scratch snippet 1 (`import superclaude.cli.sweep`, fresh `-I` interpreter) showed `superclaude.cli.sweep.models`, `probes`, `classify`, `report` and `commands` all already in `sys.modules` after the package import, and `sweep_group` not in `vars(pkg)`. Cause: `src/superclaude/cli/__init__.py:12` is `from .main import main`, so importing any `superclaude.cli.*` module first runs `main.py`, and `main.py:567-569` reads `sweep_group` at import time. This is the same for every other group in `main.py:519-569`.
- The property itself holds where it can be tested: with the parent stubbed out (snippet 2, loading `sweep/__init__.py` alone) no sweep submodule was loaded; after purging `superclaude.cli.sweep*` from `sys.modules` and re-importing (snippet 3) the list of loaded sweep submodules was empty, and reading `sweep_group` then loaded `commands` and returned a `click.Group` named `sweep`.
- Consequence: the planned test at task item 10.6 (`TASK-RF-sweep-phase1-20261108-072653.md:1818-1821`) must purge `sys.modules` first, as that item already says. A test that only does `import superclaude.cli.sweep` would see `commands` loaded and fail.
- Smallest fix: none in production code. When the test is written, keep the `monkeypatch.delitem(sys.modules, ..., raising=False)` purge and do not assert that the re-imported group `is` the one registered on `main` (snippet 3 printed `same object as registered: False`; the re-import builds a new group).

### R-2 (MINOR) Nothing in the repository pins the registration yet

- Evidence: `ls tests/sweep` shows `__init__.py`, `conftest.py`, `fixtures`, `test_readonly.py` and no `test_cli_registration.py`; `grep -rn "sweep_group\|'sweep'" tests --include=*.py` matched nothing. DESIGN line 741 and the task file schedule that test at item 10.6 (step 1.13), a later phase, so this is not a missing deliverable at this gate.
- Smallest fix: none now; confirm item 10.6 lands. The existing `tests/cli/test_cli_registration.py` snapshot of top-level names is documented as optional for `sweep`.

### R-3 (MINOR) `main.py` now needs the untracked `sweep/` package to import at all

- Evidence: `git status --short` shows ` M src/superclaude/cli/main.py`, `?? src/superclaude/cli/sweep/` and `?? tests/sweep/`. `main.py:567` runs at import time, so a commit or PR that carries `main.py` without the whole `sweep/` package would make every `superclaude` command fail with `ModuleNotFoundError`, not just `sweep`. The same coupling exists for all deferred registrations; it is only new here because the package is still untracked.
- Smallest fix: stage `src/superclaude/cli/sweep/` in the same commit as the `main.py` change. Not a defect in the files reviewed.

## Checks

| Check | Question | Result |
|---|---|---|
| C1 | The sweep pair sits after the issue-watch pair (`main.py:563-565` issue-watch, `main.py:567-569` sweep, nothing between) | PASS |
| C2 | The sweep import line copies the noqa comment exactly (`# noqa: E402,I001  # intentional: deferred subcommand registration to avoid circular imports`, compare `main.py:563` and `main.py:567`) | PASS |
| C3 | The import goes through the package (`from superclaude.cli.sweep import sweep_group`, `main.py:567`), not `...sweep.commands`, so `__getattr__` runs | PASS |
| C4 | `main.add_command(sweep_group, name="sweep")` matches the pair shape and the group's own name (`commands.py:214` `@click.group("sweep")`) | PASS |
| C5 | Every other registration line is unchanged: `git diff` is one hunk `@@ -566,0 +567,4 @@`, 4 insertions and 0 deletions (`git diff --stat`); lines 1-565 are identical to HEAD | PASS |
| C6 | Order and set of registered commands: AST list of `add_command` calls at lines 521-569 ends with `issue-watch` (565) then `sweep` (569); `main.commands` lists 19 names with `sweep` last and no duplicate | PASS |
| C7 | `sweep/__init__.py` matches the `recommend/__init__.py:12-20` pattern: `__getattr__` returns `sweep_group` via `from .commands import sweep_group` inside the function, raises `AttributeError` with the module name otherwise, `__all__ = ["sweep_group"]`; no module-level import (DESIGN line 208 boundary) | PASS |
| C8 | Importing the package does not import `commands` until `sweep_group` is read (isolated load and sys.modules purge, snippets 2 and 3) | PASS (see R-1 for the plain-import caveat) |
| C9 | Unknown attribute raises `AttributeError` (snippet 1 printed `module 'superclaude.cli.sweep' has no attribute 'nope'`); `from superclaude.cli.sweep import *` yields `['sweep_group']` | PASS |
| C10 | No circular import: no sweep module imports `superclaude.cli.main` or the `superclaude.cli` package (grep over `sweep/*.py` returned nothing); `import superclaude.cli.sweep.commands` as the first import in a fresh interpreter works and prints group name `sweep` | PASS |
| C11 | `ruff check --no-cache` on `main.py` and `sweep/`: "All checks passed!"; `ruff format --check`: "7 files already formatted" | PASS |
| C12 | `superclaude sweep --help` and `sweep run --help` exit 0 and print text identical to `step-1.7-help.txt` (and the `--help` block in `phase9-validation.md:32-42`); `superclaude --help` lists `sweep` | PASS |
| C13 | The placement matches DESIGN as revised: step 1.7 and the rollback row say "after line 565" (`orchestrator-mode.md:937`, `:973`), line 28 names `issue-watch` (563, 565) as the last pair | PASS |
| C14 | Registration is not read-only-unsafe: `main.py:567-569` only imports and adds a click group; `commands.py` runs no subprocess or write at import time (module top level holds imports, constants, `_PublishError` and function definitions, `commands.py:11-288`) | PASS |

## Summary

- Checks passed: 14 / 14
- BLOCKING: 0, MAJOR: 0, MINOR: 3 (R-1, R-2, R-3; notes only)
- Confidence: Verified: 14/14 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- Tool engagement: Read: 9 | Grep: 2 | Glob: 0 | Bash: 7 (git diff and status, ruff, help, three scratch snippets, cleanup)

Verdict: PASS
Blocking count: 0
