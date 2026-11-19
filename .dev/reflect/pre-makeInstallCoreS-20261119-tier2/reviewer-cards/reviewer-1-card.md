persona: analyzer
model_class: opus
model: claude-gw-tier1a (opus-class alias)

reviewer: 1 persona: analyzer

## Findings

- **minor**: I confirm F1. Task 1 points to places by bare line numbers: "lines 121-125", "line 97" and "line 8". Those numbers move as soon as Task 1's own edits begin. The helper was at 121-125 before the change, and today `same_content` is called at line 98 and imported at line 12. Each number comes with a name (`_same_content`, the `stale` list, `import filecmp`), so the edit is still unambiguous. This is a form problem only. Cites: `.dev/tasks/done/TASK-WF-makeInstallCoreS-20261119-013812/TASK-WF-makeInstallCoreS-20261119-013812.md:26`, `src/superclaude/cli/install_core.py:12`, `src/superclaude/cli/install_core.py:98`.
- **minor**: I confirm F2. Task 2 asks for "different bytes of the same length" but does not say how to make them. Whoever wrote the test filled that in by flipping one bit of the first byte (`shipped[0] ^ 1`). That works because PRINCIPLES.md is not empty. No decision depends on this, so it is minor. Cites: `TASK-WF-makeInstallCoreS-20261119-013812.md:36`, `tests/cli/test_how_we_work_install.py:128`.
- **note**: I confirm F3. The relative import sits in its own block after the standard-library imports, which is the order ruff expects. Cite: `src/superclaude/cli/install_core.py:8-12`.
- **note**: I confirm F4. `same_content` empties the `filecmp` result cache, which is shared by the whole process, on every call. That costs speed only; the cache is just a speed-up. Cite: `src/superclaude/cli/install_keep.py:20-22`.
- **note**: I confirm F5 and extend it. Turning off `filecmp.clear_cache` in a throwaway pytest plugin is the correct way to bring back the old behaviour. Before the change, `_same_content` was the same `try: filecmp.cmp(...) except OSError: return False` without the cache clear. With the clear turned off, the shared function behaves exactly like the old one. The old body is quoted in `artifacts/retries/T1/prompt-1-1.md:30-34`, a diff recorded during the run; I did not read the pre-change file myself. Extension: this check is a one-off manual step and is not kept as a test. Also, without the fix the new test fails with an `IndexError` on `message.split("NOT updated")[1]`, because no "NOT updated" section is printed. It does not fail with an assertion message, so the failure is harder to read. It still fails, which is what matters. Cites: `TASK-WF-makeInstallCoreS-20261119-013812.md:39`, `tests/cli/test_how_we_work_install.py:134`.
- **note (new)**: Switching to the shared function does not change behaviour on unreadable files. The old private helper already turned `OSError` into False, so an unreadable kept file was already reported as stale. The only behaviour change is the cache clear. Cites: `artifacts/retries/T1/prompt-1-1.md:31-34`, `src/superclaude/cli/install_keep.py:23-26`.
- **note (new, advisory, outside the spec)**: The same stale-cache flaw exists in a copy of this comparison logic elsewhere in the repo. `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` calls `filecmp.cmp(..., shallow=False)` without clearing the cache at lines 480, 500 and 1682. The spec covers only `install_core`, so this is not a gap in the plan. [INFERRED] I found the lines with Grep and did not open the file to check whether repeated comparisons can actually happen there.

## Coverage verdict

Yes, the plan covers every requirement in the spec:
- **The shared function is used**: Task 1 makes `install_core` use it. The import is at `install_core.py:12` and the call at `:98`.
- **The stale cache is gone**: `install_core` itself has no `filecmp` left. Grep over `src` finds `filecmp` only in `install_keep.py` and `orca_worktree.py`.
- **A test in `tests/cli`**: Task 2 adds it, at `tests/cli/test_how_we_work_install.py:118-134`.
- **Same-size, same-time rewrite is reported as different**: the test checks this at `:127-134`. It restores the old modification time to the nanosecond with `os.utime(..., ns=...)`. That recreates the exact (size, modification time) key the cache uses, so a cache lookup would hit if the fix were missing.
- **Existing `tests/cli -k install` tests stay green**: Task 1's acceptance criteria require this (plan line 30). I could not run tests, so I have not confirmed that they pass.

The plan's file limits hold. Grep shows no `_same_content` left anywhere in `src` or `tests`. `install_keep.py` was not changed.

## Risks the first run missed

- The copy of the flaw in `orca_worktree.py` described above. It is outside this spec and should be raised as a separate issue.
- The failure without the fix being an `IndexError` rather than an assertion (minor).
- Nothing else. What I checked:
  - **Import cycle**: `install_keep` imports only `filecmp`, `shutil`, `datetime` and `pathlib`, so importing it from `install_core` creates no cycle (`install_keep.py:10-15`).
  - **Other callers of `_same_content`**: Grep finds none.
  - **The other installers**: they already used the shared function (`install_commands.py:61`, `install_user_setup.py:90`).
  - **Test setup**: the new test's first install call uses `force=False`, so it fills the cache with "identical" without overwriting the kept file (`test_how_we_work_install.py:124-125`).

## Recommendation

Accept the plan and the implementation as they are. If you want a follow-up, add one line to `tests/cli/test_how_we_work_install.py` before line 134: `assert "NOT updated" in message, message`. Then the old behaviour fails with a readable assertion instead of an `IndexError`. To verify, run `uv run pytest tests/cli/test_how_we_work_install.py -q`. Separately, open a small backlog issue for the uncleared `filecmp.cmp` calls in `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` (lines 480, 500, 1682).

reviewer_model_self_report: claude-gw-tier1a (Claude, opus-class alias)

(Reviewer's own closing note: it did not run the tests, and it relied on the diff quoted in artifacts/retries/T1/prompt-1-1.md for the pre-change file. None of its findings block the work.)
