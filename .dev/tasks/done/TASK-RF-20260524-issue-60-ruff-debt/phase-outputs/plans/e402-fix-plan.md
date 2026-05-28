# E402 Fix Plan — Phase 4.1

**Generated:** 2026-05-25 03:42
**Total instances:** 38

## Per-File Classification

| File | Lines | Class | Fix Action | Rationale |
|------|-------|-------|-----------|-----------|
| `src/superclaude/cli/audit/dependency_graph.py` | 116, 117 | TBD | Read & decide | TBD |
| `src/superclaude/cli/cli_portify/executor.py` | 26,28,35-37,42,43,56-59 (11) | CLASS-E (TypeVar interleaving) | Move `_T = TypeVar("_T")` AFTER all imports | TypeVar definition split the import block; consolidating preserves semantics |
| `src/superclaude/cli/cli_portify/steps/validate_config.py` | 43 | TBD | Read & decide | TBD |
| `src/superclaude/cli/main.py` | 400, 404, 408, 412, 416, 420, 424 (7) | CLASS-B (intentional circular-avoidance) | Add `# noqa: E402  # intentional: deferred subcommand registration to avoid circular imports between cli.main and subcommand modules` to each | Click subcommand modules import from main; loading them at top would create cycles |
| `tests/cli_portify/test_failures.py` | 377 | CLASS-A or CLASS-E | Read & decide | TBD |
| `tests/pipeline/test_full_flow.py` | 343-360, 472 (8) | CLASS-E (mid-file section imports) | Add `# noqa: E402  # late import for test section grouping (anti-instinct gate suite)` | Section organization documented with comment dividers |
| `tests/roadmap/test_models.py` | 206 | Likely CLASS-E or CLASS-A | Read & decide | TBD |
| `tests/sprint/diagnostic/test_level_0.py` | 13 | CLASS-A (pytestmark before imports) | Move `pytestmark = [...]` AFTER all imports | Pattern: import pytest → pytestmark → other imports; reorder fixes it |
| `tests/sprint/diagnostic/test_level_1.py` | 12 | CLASS-A | Move pytestmark | Same pattern |
| `tests/sprint/diagnostic/test_level_2.py` | 12, 18 | CLASS-A | Move pytestmark | Same pattern |
| `tests/sprint/diagnostic/test_level_3.py` | 13, 19 | CLASS-A | Move pytestmark | Same pattern |
| `tests/sprint/diagnostic/test_negative.py` | 16, 23 | CLASS-A | Move pytestmark | Same pattern |

## Strategy

1. **CLASS-A (pytestmark moves)**: 5 sprint/diagnostic files — most mechanical, do first.
2. **CLASS-B (cli/main.py deferred subcommand registrations)**: 7 noqa entries with consistent rationale.
3. **CLASS-E (executor.py TypeVar)**: 1 file, move `_T = TypeVar("_T")` after imports.
4. **CLASS-E (test_full_flow.py section imports)**: 8 noqa entries with section-grouping rationale.
5. **Other small fixes**: 5 files (dependency_graph, validate_config, test_failures, test_models) — read & decide.

## Verification

After all fixes:
```bash
uv run ruff check . --select E402 2>&1 | tail -3
```
Should report "All checks passed!"
