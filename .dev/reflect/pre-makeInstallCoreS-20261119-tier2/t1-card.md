# Tier 1 reflection card (UC-1, pre-execution review, forced to Tier 2 by --depth deep)

**Spec**: .dev/tasks/done/TASK-WF-makeInstallCoreS-20261119-013812/source.md (one unlabelled prose line)
**Tasklist**: .dev/tasks/done/TASK-WF-makeInstallCoreS-20261119-013812/TASK-WF-makeInstallCoreS-20261119-013812.md (2 tasks)
**Timestamp**: 2026-11-19T02:06:00Z
**Self-reported confidence**: 0.90 (not used as input anywhere)
**Context**: this is the second-opinion run on a plan that was already implemented and archived. The first run (`.dev/reflect/pre-makeInstallCoreS-20261119013914/REPORT.md`) stopped at Tier 1 (partial, calibrated 0.79) because the parse-density guard and the 0.85 floor both required Tier 2. This run is that Tier 2.

## Requirement extraction

Pass 1 (labelled IDs): 0. Pass 2 (inferred, quote-pinned to source.md line 1): 5 rows. Inferred (5) exceeds parsed (0), so `coverage_degraded: parsed-sparse` fires (Step 1B.2b).

| id | quote (source.md line 1) | task | match |
|---|---|---|---|
| INF-001 | "Make install_core._same_content use the fixed install_keep.same_content" | Task 1 | mapped |
| INF-002 | "so it no longer answers from filecmp's stale cache" | Task 1, Task 2 | mapped |
| INF-003 | "a test in tests/cli for install_core" | Task 2 | mapped |
| INF-004 | "a same-size same-mtime rewrite is reported as different by install_core" | Task 2 | mapped |
| INF-005 | "existing tests/cli -k install stay green" | Task 1 | mapped |

coverage_pct (parsed-only): null. coverage_pct_union: 5/5 = 1.00. unmapped_requirements_union: none. S_dev_density: 0.0. S_scope: 2 files. S_domains: 2 (code, tests).

## Grounded checks (all Read in this run, against the CURRENT files)

- The plan's Task 1 cites bare line numbers (8, 97, 121-125). After implementation they are stale by design: `src/superclaude/cli/install_core.py:12` now holds `from .install_keep import same_content` and `:98` holds the call `same_content(core_source / n, target_path / n)`. A reviewer judging the plan as a plan must read those numbers against the file as it stood before the work (git history), not against today's file.
- `src/superclaude/cli/install_keep.py:18-26` holds `same_content`, which calls `filecmp.clear_cache()` first (line 22) and keeps `OSError` to False (lines 25-26). It imports only the standard library (lines 12-15), so importing it from `install_core` adds no cycle.
- `tests/cli/test_how_we_work_install.py:118-134` is the Task 2 test; `:102-115` is the neighbour test it sits beside; `import os` is at line 5.
- The only caller of the removed private function was the stale list; a repo-wide grep (excluding `.dev`) finds no remaining `_same_content`.

## Findings (none blocking at Tier 1)

- F1 (minor, plan wording): bare line numbers in Task 1 drift; locate by symbol.
- F2 (minor, plan wording): Task 2 says "different bytes of the same length" without saying how; the delivered test flips one byte of the shipped content.
- F3 (note, lint): the new relative import must sit in its own block after the standard-library imports (the project selects ruff's import-order rules); the plan does not say so.
- F4 (note, side effect): `same_content` clears the process-wide `filecmp` cache on every call; a speed cost only, for about a dozen core files.
- F5 (note, test design): Task 2 acceptance 1 proves the old behaviour by disabling `filecmp.clear_cache` in a throwaway plugin; this exercises the `install_keep` fix, which is the right check because Task 1 deletes `_same_content`.

## Rubric inputs

S_scope: 2. S_domains: 2. S_dev_density: 0.0. Calibrated confidence for the Tier 1 card: carried from the first run's independent calibrator (0.79, ESCALATE); not re-run because `--depth deep` forces Tier 2 regardless (disclosed in REPORT.md).
