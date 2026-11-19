# Reflect report (pre-execution): make install_core use the cache-safe same_content

**Mode**: pre (UC-1) | **Tier reached**: 1 | **Status**: partial | **Calibrated confidence**: 0.79 (independent calibrator; self-reported 0.92) | **Coverage (union)**: 1.00 (5 of 5 requirements)
**Spec**: `.dev/tasks/to-do/TASK-WF-makeInstallCoreS-20261119-013812/source.md` | **Tasklist**: `.dev/tasks/to-do/TASK-WF-makeInstallCoreS-20261119-013812/TASK-WF-makeInstallCoreS-20261119-013812.md`
**Citations**: 6 total, 6 verified, 0 dropped (evidence validator agent)

## Why partial

Two independent triggers require Tier 2 (two or more heterogeneous reviewers and an adversarial merge), and Tier 2 was not run:

1. The source is an unlabelled prose request: zero labelled IDs, five inferred, so the parse-density guard (`coverage_degraded: parsed-sparse`, inferred 5 > parsed 0) forbids a Tier 1 stop.
2. The calibrated confidence is 0.79, below the 0.85 floor (rule 6, `low_confidence`).

This review is the advisory last step of plan generation for a two-task, two-file change and no tier was pinned; the calibrator itself says the plan is correct and low risk and that escalation here is protocol, not a plan defect. The plan is not blocked. Re-run with `--depth deep` for the full ensemble.

## Coverage matrix (inferred requirements, each quote-pinned to `source.md` line 1)

| id | requirement | task | result |
|---|---|---|---|
| INF-001 | install_core uses the fixed `install_keep.same_content` | Task 1 | mapped |
| INF-002 | no answer from filecmp's stale cache | Task 1, Task 2 | mapped |
| INF-003 | a test in tests/cli for install_core | Task 2 | mapped |
| INF-004 | same-size same-mtime rewrite reported as different | Task 2 | mapped |
| INF-005 | existing `tests/cli -k install` stay green | Task 1 | mapped |

Unmapped: none. Dev density: 0.0. The calibrator confirmed the five rows and the mapping (INF-001 and INF-002 overlap; nothing is lost).

## Evidence

- `src/superclaude/cli/install_core.py:8` — `import filecmp`; its only use is line 123 inside `_same_content` (lines 121-125), so Task 1 can remove the import.
- `src/superclaude/cli/install_core.py:97` — `n for n in skipped if not _same_content(core_source / n, target_path / n)`; the only caller. A repo-wide grep (excluding `.dev`) finds only lines 97 and 121 of this file, and there is no other copy of `install_core.py` in the tree.
- `src/superclaude/cli/install_keep.py:12-15` — imports only `filecmp`, `shutil`, `datetime`, `pathlib`; no cycle with `install_core`.
- `tests/cli/test_how_we_work_install.py:101` — `def test_skip_without_force_names_only_stale_files(tmp_path):`, the neighbour for Task 2, which uses `install_core._get_core_source() / "PRINCIPLES.md"`; the file has no `import os` (lines 1-12), which Task 2 covers.
- `src/superclaude/core/PRINCIPLES.md` exists.

## Findings (none blocking; for the implementer)

- Minor: Task 1 cites bare line numbers (8, 97, 121-125) that shift as soon as its edits start; locate by symbol. Matches a recurring plan-defect class in `docs/memory/reflect/deviation-patterns-IronClaude.md`.
- Minor: put the new `from .install_keep import same_content` in its own block after the stdlib imports. The project selects ruff's import-order rules, and `install_user_setup.py:31-32` does it this way; Task 2's `ruff check` acceptance would catch a miss.
- Minor: in Task 2, make the rewrite differ for real (flip one byte of the shipped content), since "different bytes of the same length" is otherwise unspecified.
- Note: the shared `same_content` clears the process-wide `filecmp` cache on every call, a speed cost only, for about a dozen core files.
- Note: Task 2's design is sound. The first `install_core_files` call fills the stdlib cache with "identical"; the same-length rewrite with the old mtime restored keeps the cache key, so only the fix gives the right answer. The throwaway-plugin check exercises the `install_keep` fix, which is the right check because Task 1 deletes `_same_content`.

## Deviation classification

No deviation: the tasklist is aligned with its source (none of Authorized, Necessary, Drift or Regression applies in a pre-execution review).

## Grounding Gaps

- Tier 2 required by the guard and the 0.79 calibration, not run (see "Why partial").
- Structural assertions of the validator and calibrator were skipped (troubleshoot-only inputs).
- Nothing was executed for this pre-check; every check is a read of the repo and plan, plus one repo-wide grep.

## Recommendation

Proceed with `/sc:implement` on the plan; no change to the tasklist is needed. Fold the three minor points above into the implementation.
