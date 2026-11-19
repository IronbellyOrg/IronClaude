<!-- Provenance: This document was produced by /sc:adversarial via /sc:reflect (Wave 4) -->
<!-- Base: Variant 1 (opus-class alias, analyzer) -->
<!-- Merge date: 2026-11-19 -->

<!-- Source: Base (original, modified) - header now names both source reviewers and the merge outcome per refactor-plan Overview and outline -->
persona: analyzer (reviewer 1, base) merged with persona: qa (reviewer 2)
model_class: opus (reviewer 1); haiku (reviewer 2)
model: claude-gw-tier1a (opus-class alias); claude-gw-tier2 (haiku alias; reviewer 2 self-reported "GPT-5")

Merged from 2 reviewer cards by adversarial Mode A, base Variant 1. Converged 9 of 9 debate points after round 2. Invariant probe gate: not blocked (0 HIGH unaddressed).

## Findings

<!-- Source: Base (original, modified) - F5 extension split out and promoted to lead finding per Change 2; settled facts merged from debate C-001, X-002 -->
- **minor**: The new test fails with an `IndexError` instead of a readable assertion. Without the fix, no "NOT updated" section is printed, so `message.split("NOT updated")[1]` raises `IndexError`. The task plan itself prescribes that expression (plan:36), and `t2-checks.log:8-10` shows the `IndexError`. The older test uses the same pattern at `tests/cli/test_how_we_work_install.py:113`, so a consistent fix covers both lines. This is a readability weakness only: the supplied negative control still fails, so the bug is still detected. Cites: `.dev/tasks/done/TASK-WF-makeInstallCoreS-20261119-013812/TASK-WF-makeInstallCoreS-20261119-013812.md:36`, `artifacts/t2-checks.log:8-10`, `tests/cli/test_how_we_work_install.py:134`, `tests/cli/test_how_we_work_install.py:113`.

<!-- Source: Base (original, modified) - severity changed from minor to note per Change 1 (debate X-001, V1 advocate concession) -->
- **note**: I confirm F1. Task 1 points to places by bare line numbers: "lines 121-125", "line 97" and "line 8". Those numbers move as soon as Task 1's own edits begin. The helper was at 121-125 before the change, and today `same_content` is called at line 98 and imported at line 12. Each number comes with a name (`_same_content`, the `stale` list, `import filecmp`), so the edit is still unambiguous. This is a form problem only; it is a wording point that cannot cause a wrong edit, because each number comes with a symbol name and plan:36 sets a measurable requirement. Cites: `.dev/tasks/done/TASK-WF-makeInstallCoreS-20261119-013812/TASK-WF-makeInstallCoreS-20261119-013812.md:26`, `src/superclaude/cli/install_core.py:12`, `src/superclaude/cli/install_core.py:98`.

<!-- Source: Base (original, modified) - severity changed from minor to note per Change 1; non-empty PRINCIPLES.md qualifier appended per Change 7 (debate A-003) -->
- **note**: I confirm F2. Task 2 asks for "different bytes of the same length" but does not say how to make them. Whoever wrote the test filled that in by flipping one bit of the first byte (`shipped[0] ^ 1`). That works because PRINCIPLES.md is not empty. No decision depends on this, and it is a wording point that cannot cause a wrong edit. The byte change `shipped[0] ^ 1` (test:128) is valid while `PRINCIPLES.md` is shipped and non-empty (its line 1 is `# Software Engineering Principles`); no test guards that, and an empty file would raise `IndexError` before the installer is exercised. Cites: `TASK-WF-makeInstallCoreS-20261119-013812.md:36`, `tests/cli/test_how_we_work_install.py:128`.

<!-- Source: Base (original) -->
- **note**: I confirm F3. The relative import sits in its own block after the standard-library imports, which is the order ruff expects. Cite: `src/superclaude/cli/install_core.py:8-12`.

<!-- Source: Base (original) -->
- **note**: I confirm F4. `same_content` empties the `filecmp` result cache, which is shared by the whole process, on every call. That costs speed only; the cache is just a speed-up. Cite: `src/superclaude/cli/install_keep.py:20-22`.

<!-- Source: Base (original, modified) - IndexError extension removed from this bullet and moved to the lead finding per Change 2 -->
- **note**: I confirm F5. Turning off `filecmp.clear_cache` in a throwaway pytest plugin is the correct way to bring back the old behaviour. Before the change, `_same_content` was the same `try: filecmp.cmp(...) except OSError: return False` without the cache clear. With the clear turned off, the shared function behaves exactly like the old one. The old body is quoted in `artifacts/retries/T1/prompt-1-1.md:30-34`, a diff recorded during the run; I did not read the pre-change file myself. Extension: this check is a one-off manual step and is not kept as a test. Cites: `TASK-WF-makeInstallCoreS-20261119-013812.md:39`, `tests/cli/test_how_we_work_install.py:134`.

<!-- Source: Base (original) -->
- **note (new)**: Switching to the shared function does not change behaviour on unreadable files. The old private helper already turned `OSError` into False, so an unreadable kept file was already reported as stale. The only behaviour change is the cache clear. Cites: `artifacts/retries/T1/prompt-1-1.md:31-34`, `src/superclaude/cli/install_keep.py:23-26`.

<!-- Source: Base (original, modified) - downgraded to an optional investigation lead per Change 6 (debate C-003, X-002) -->
- **note (new, advisory, outside the spec, optional investigation lead)**: The same stale-cache flaw may exist in a copy of this comparison logic elsewhere in the repo. `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` calls `filecmp.cmp(..., shallow=False)` without clearing the cache at lines 480, 500 and 1682. The spec covers only `install_core`, so this is not a gap in the plan. [INFERRED] I found the lines with Grep and did not open the file to check whether repeated comparisons can actually happen there. Verified context: line 500 follows `shutil.copyfile` at line 499, which writes a new modification time, so no stale hit is expected there. No path was found that gives a wrong answer. A caller that runs `copy_issue_dir` and `stale_prompt` twice in one process was not checked.

### Carried over from the invariant probe (not from either reviewer)

<!-- Source: invariant probe INV-001 -->
- **MEDIUM (from the invariant probe, INV-001, unaddressed)**: `filecmp.cmp` empties its whole cache once it holds more than 100 entries (the parent re-checked this against CPython source). The second call compares 8 files that sort before `PRINCIPLES.md` (`install_core.py:15-29, :59`). In a long test process with a full cache the purge could hide the old bug. The supplied failing run executed only this test (`t2-checks.log:7`, `-k same_size`).

<!-- Source: invariant probe INV-002 -->
- **MEDIUM (from the invariant probe, INV-002, unaddressed)**: `test_how_we_work_install.py:125` ignores the first call's result; nothing checks that `PRINCIPLES.md` was skipped as identical, and lines 128-129 do not check that size and mtime still match `before` after the rewrite.

<!-- Source: invariant probe INV-003 -->
- **MEDIUM (from the invariant probe, INV-003, unaddressed)**: No shipped CLI path compares the same pair twice in one process (`main.py:178` calls `install_core_files` once; `update` passes `force=True` at `main.py:365`, which copies without comparing, `install_core.py:71-77`). The bug is reachable only in-process. This changes priority, not correctness.

<!-- Source: invariant probe INV-008 -->
- **MEDIUM (from the invariant probe, INV-008, unaddressed, outside this plan's scope)**: `install_keep.py:3-7` says `install --force` and `update` back up a differing file first; `install_core.py:71-77` copies with `shutil.copy2` and no backup, and `update` always forces, so a user-edited `~/.claude/RULES.md` is overwritten with no copy (the parent re-checked this; `install_agents.py:56` and `install_templates.py:76` also copy without backup).

## Coverage verdict

<!-- Source: Base (original) -->
Yes, the plan covers every requirement in the spec:
- **The shared function is used**: Task 1 makes `install_core` use it. The import is at `install_core.py:12` and the call at `:98`.
- **The stale cache is gone**: `install_core` itself has no `filecmp` left. Grep over `src` finds `filecmp` only in `install_keep.py` and `orca_worktree.py`.
- **A test in `tests/cli`**: Task 2 adds it, at `tests/cli/test_how_we_work_install.py:118-134`.
- **Same-size, same-time rewrite is reported as different**: the test checks this at `:127-134`. It restores the old modification time to the nanosecond with `os.utime(..., ns=...)`. That recreates the exact (size, modification time) key the cache uses, so a cache lookup would hit if the fix were missing.
- **Existing `tests/cli -k install` tests stay green**: Task 1's acceptance criteria require this (plan line 30). I could not run tests, so I have not confirmed that they pass.

<!-- Source: Variant 2 (haiku-class alias, qa), Section Coverage verdict - merged per Change 3 -->
Requirement-to-check mapping and log evidence:
- The complete spec requires the shared comparison, removal of stale-cache answers, an installer test, a same-size same-mtime rewrite detected as different, and preservation of existing install tests. Source: `/home/coder/workspaces/worktrees/IronClaude/issue-606/.dev/tasks/done/TASK-WF-makeInstallCoreS-20261119-013812/source.md:1`.
- Task 1 explicitly requires importing the shared function, replacing the caller, removing the duplicate implementation, and passing the existing install tests. These are observable acceptance checks. Source: `/home/coder/workspaces/worktrees/IronClaude/issue-606/.dev/tasks/done/TASK-WF-makeInstallCoreS-20261119-013812/TASK-WF-makeInstallCoreS-20261119-013812.md:24-30`.
- Task 2 specifies an initial identical comparison, a different replacement of equal length, restoration of the original modification time, and an assertion against the stale-file report. It also requires a negative control with cache clearing disabled. Sources: `/home/coder/workspaces/worktrees/IronClaude/issue-606/.dev/tasks/done/TASK-WF-makeInstallCoreS-20261119-013812/TASK-WF-makeInstallCoreS-20261119-013812.md:32-40`; `/home/coder/workspaces/worktrees/IronClaude/issue-606/tests/cli/test_how_we_work_install.py:118-134`.
- The supplied verification log records nine passing file-level tests, passing lint checks, failure of the new test when cache clearing is disabled, and 352 passing existing install tests with one skip. Source: `/home/coder/workspaces/worktrees/IronClaude/issue-606/.dev/tasks/done/TASK-WF-makeInstallCoreS-20261119-013812/artifacts/t2-checks.log:1-16`.

<!-- Source: Variant 2 (haiku-class alias, qa), Section Coverage verdict and closing note - merged per Change 4 (debate A-001) -->
Provenance of the evidence: the test, lint and negative-control results are supplied evidence, corroborated by the logs agreeing with each other (351 then 352 passed is one new test) and with the code (the predicted `IndexError`), and not independently repeated by any reviewer.

<!-- Source: Base (original) -->
The plan's file limits hold. Grep shows no `_same_content` left anywhere in `src` or `tests`. `install_keep.py` was not changed.

## Risks the first run missed

<!-- Source: Base (original, modified) - first bullet is now the readability weakness from Change 2; sibling-file lead downgraded per Change 6 -->
- The new test fails without the fix with an `IndexError` rather than an assertion (minor). The negative control still fails, so the bug is still detected; the issue is readability (see the lead Finding).
- Optional investigation lead, not a defect: the uncleared `filecmp.cmp` calls in `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` (see the advisory Finding).
- The four MEDIUM items carried over from the invariant probe above (INV-001, INV-002, INV-003, INV-008), which neither reviewer raised.
- Nothing else. What I checked:
  - **Import cycle**: `install_keep` imports only `filecmp`, `shutil`, `datetime` and `pathlib`, so importing it from `install_core` creates no cycle (`install_keep.py:10-15`).
  - **Other callers of `_same_content`**: Grep finds none.
  - **The other installers**: they already used the shared function (`install_commands.py:61`, `install_user_setup.py:90`).
  - **Test setup**: the new test's first install call uses `force=False`, so it fills the cache with "identical" without overwriting the kept file (`test_how_we_work_install.py:124-125`).

<!-- Source: Variant 2 (haiku-class alias, qa), Section Risks - merged per Change 5 (debate C-002, U-004) -->
Checked and fine (existing-test safeguards, kept as counter-evidence against overstating risk):
- **Unreadable or missing files:** The shared comparison catches `OSError` and returns false; an existing helper test covers a missing file. Sources: `/home/coder/workspaces/worktrees/IronClaude/issue-606/src/superclaude/cli/install_keep.py:18-26`; `/home/coder/workspaces/worktrees/IronClaude/issue-606/tests/cli/test_install_keep.py:38-45`. The spec does not require a new installer-level error test.
- **Missing destination and forced installation:** These use the copying branch, not the changed comparison. Source: `/home/coder/workspaces/worktrees/IronClaude/issue-606/src/superclaude/cli/install_core.py:68-79`. Existing tests exercise forced installation and preservation of unshipped files under both force settings. Source: `/home/coder/workspaces/worktrees/IronClaude/issue-606/tests/cli/test_how_we_work_install.py:28-34,79-99`.
- **False-positive stale reports:** The existing test checks that an identical kept file is excluded while a differing kept file is included. Source: `/home/coder/workspaces/worktrees/IronClaude/issue-606/tests/cli/test_how_we_work_install.py:102-115`.

## Recommendation

<!-- Source: Base (original, modified) - restated as one concrete optional action per Change 8; backlog-issue action dropped per Change 6 -->
Accept the plan and the implementation as they are. One optional, non-blocking follow-up: in `tests/cli/test_how_we_work_install.py`, add `assert "NOT updated" in message, message` before line 134 and before line 113, so the old behaviour fails with a readable assertion instead of an `IndexError`. The one-site version (line 134 only) is the minimum. To verify, run `uv run pytest tests/cli/test_how_we_work_install.py -q`.

## Open items

<!-- Source: Base (original, modified) - new section assembled from the plan's Open items outline per Change 10 -->
- Whether to add the assert at one site or two (Recommendation).
- Whether INV-001 warrants running the new test in a full suite with the fix reverted.
- Whether INV-008 (no backup in `install_core`) should be filed as a separate issue.
- Whether the `orca_worktree.py` lead is worth a look.

<!-- Source: invariant probe INV-006 -->
- LOW (from the invariant probe, INV-006, unaddressed): comments say "(size, mtime)" but the real key is (path 1, path 2, type, size, mtime) (`install_keep.py:20`, `test:119`).

<!-- Source: invariant probe INV-012 -->
- LOW (from the invariant probe, INV-012, unaddressed): zero skipped files and exactly one stale file behave correctly; no defect found (`install_core.py:88`, lines 101-103).

<!-- Source: invariant probe INV-010 -->
- Caveat (from the invariant probe, INV-010): the failing control run at `t2-checks.log:7` is a bare `pytest`, possibly another environment; the throwaway plugin was not saved; the one skipped test is unidentified.

<!-- Source: Base (original) -->
reviewer_model_self_report: claude-gw-tier1a (Claude, opus-class alias)

(Reviewer 1's own closing note: it did not run the tests, and it relied on the diff quoted in artifacts/retries/T1/prompt-1-1.md for the pre-change file. None of its findings block the work.)

<!-- Source: Variant 2 (haiku-class alias, qa), closing note - merged per Change 4 -->
reviewer_model_self_report (reviewer 2): GPT-5.

(Reviewer 2's closing note: it did not execute tests or inspect the temporary negative-control plugin; its recorded failure is supplied evidence, not an independently repeated result.)
