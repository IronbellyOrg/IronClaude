---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: quick
slug: TASK-WF-makeInstallCoreS-20261119-013812
version: "1"
priority: Medium
created_date: "2026-11-19"
---

# Make install_core use the cache-safe same_content

Source: ./source.md
Goal: `install_core_files` no longer reports a changed kept file as identical because of `filecmp`'s stale result cache.

## Constraints

- Change only `src/superclaude/cli/install_core.py` and one test in `tests/cli/test_how_we_work_install.py`; `src/superclaude/cli/install_keep.py` already has the fix and stays as it is.
- Nothing is committed or pushed; this is the issue 606 branch.

## Phase 1: Share the safe comparison

## Task 1: Replace install_core's private comparison with install_keep.same_content

In `src/superclaude/cli/install_core.py`, delete the private `_same_content` (lines 121-125), add `from .install_keep import same_content` beside the other imports, and change its only caller (line 97, the `stale` list in `install_core_files`) to call `same_content`. Remove `import filecmp` (line 8), because line 123 is its only use in that file.

Acceptance criteria:
- `install_core.py` has no `filecmp` import and no `_same_content`; `install_core_files` calls `same_content` from `install_keep` for the stale list.
- Existing callers and tests keep working: `uv run pytest tests/cli -q -k install` passes, including `tests/cli/test_how_we_work_install.py::test_skip_without_force_names_only_stale_files`.

## Task 2: Prove a same-size same-mtime rewrite is reported as stale

Depends on: Task 1

In `tests/cli/test_how_we_work_install.py`, add a test next to `test_skip_without_force_names_only_stale_files`. Seed `target / "PRINCIPLES.md"` with the shipped bytes of `install_core._get_core_source() / "PRINCIPLES.md"` and call `install_core.install_core_files(target_path=target, force=False)` (this fills the stdlib comparison cache with "identical"). Then rewrite the target with different bytes of the same length, restore its old modification time with `os.utime(path, ns=(st_atime_ns, st_mtime_ns))`, call `install_core_files` again, and assert `PRINCIPLES.md` is listed in `message.split("NOT updated")[1]`. Add `import os` if the file lacks it.

Acceptance criteria:
- The new test passes with Task 1 applied and fails when the old `filecmp.cmp` comparison is put back (check by running it with `filecmp.clear_cache` disabled through a throwaway pytest plugin, not by editing the source).
- `uv run pytest tests/cli/test_how_we_work_install.py -q` and `uv run ruff check src/superclaude/cli/install_core.py tests/cli/test_how_we_work_install.py` pass.
