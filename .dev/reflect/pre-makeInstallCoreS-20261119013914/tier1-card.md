# Tier 1 reflection card (UC-1, pre-execution)

**Spec**: .dev/tasks/to-do/TASK-WF-makeInstallCoreS-20261119-013812/source.md (an unlabelled prose request)
**Tasklist**: .dev/tasks/to-do/TASK-WF-makeInstallCoreS-20261119-013812/TASK-WF-makeInstallCoreS-20261119-013812.md (2 tasks)
**Timestamp**: 2026-11-19T01:40:30Z
**Self-reported confidence**: 0.92

## Requirement extraction

Pass 1 (labelled IDs): 0. Pass 2 (inferred, quote-pinned): 5 rows. Because inferred (5) exceeds parsed (0), `coverage_degraded: parsed-sparse` fires (Step 1B.2b).

| id | source | quote (source.md line 1) | task | match |
|---|---|---|---|---|
| INF-001 | inferred | "Make install_core._same_content use the fixed install_keep.same_content" | Task 1 | mapped: Task 1 replaces the private function with an import of `same_content` |
| INF-002 | inferred | "so it no longer answers from filecmp's stale cache" | Task 1, Task 2 | mapped: Task 1 removes the `filecmp` call from install_core; Task 2 proves it |
| INF-003 | inferred | "a test in tests/cli for install_core" | Task 2 | mapped: new test in tests/cli/test_how_we_work_install.py |
| INF-004 | inferred | "a same-size same-mtime rewrite is reported as different by install_core" | Task 2 | mapped: Task 2 acceptance 1 and the described test |
| INF-005 | inferred | "existing tests/cli -k install stay green" | Task 1 | mapped: Task 1 acceptance 2 |

coverage_pct (parsed-only): null (zero parsed rows). coverage_pct_union: 5/5 = 1.00. unmapped_requirements_union: none. S_dev_density: 0.0.

## Grounded checks of the plan against the repo (all Read in this run)

- `src/superclaude/cli/install_core.py:8` is `import filecmp`; its only use is line 123 inside `_same_content` (lines 121-125). The plan's Task 1 removes both, which is correct.
- The only caller of `_same_content` is `install_core.py:97` (the `stale` list in `install_core_files`); a grep of `src`, `tests` and `docs` finds no other reference, so no test patches the private name.
- `src/superclaude/cli/install_keep.py:10-15` imports only `__future__`, `filecmp`, `shutil`, `datetime` and `pathlib`: importing it from `install_core` adds no import cycle. `install_keep.same_content` calls `filecmp.clear_cache()` first (verified earlier in this issue's work).
- `tests/cli/test_how_we_work_install.py` exists, has no `import os` (lines 1-22), and holds `test_skip_without_force_names_only_stale_files` at line 101 using `install_core._get_core_source() / "PRINCIPLES.md"`; `src/superclaude/core/PRINCIPLES.md` exists. The plan's Task 2 design is sound: the first `install_core_files` call fills the stdlib cache with "identical" for (shipped path, target path, signatures); the same-length rewrite with the old mtime restored then keeps the key, so only the fix returns the right answer.
- Plan frontmatter and body pass the quick gate (no checkbox or numbered lines; `slug` matches the directory; 2 tasks, each with acceptance criteria).

## Findings (none blocking)

- F1 (minor, test adequacy): Task 2 relies on the first call to `install_core_files` priming the cache. That holds only if `PRINCIPLES.md` is in the skipped list on the first call, which it is because it is seeded before the call; the task says so. No change needed.
- F2 (minor, wording): Task 1 cites bare line numbers (8, 97, 121-125). They are exact now, but they shift as soon as the task's own edits start; an implementer should locate by symbol. Matches the recurring plan-defect class in `docs/memory/reflect/deviation-patterns-IronClaude.md` ("bare line citations drift").
- F3 (minor): Task 2's "fails when the old comparison is put back" check disables `filecmp.clear_cache` through a throwaway plugin, which exercises the install_keep fix; it does not restore `install_core._same_content`. That is the right check for the behaviour, since Task 1 deletes that function. No change needed.
- F4 (note, process): the source is an unlabelled prose request, so Pass 1 finds zero IDs and the parse-density guard forces Tier 2 by protocol. Tier 2 was not run (see REPORT).

## Rubric inputs

S_scope: 2 files. S_domains: 2 (code, tests). S_dev_density: 0.0. Calibrated confidence: from the independent calibrator.
