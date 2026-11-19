# Evidence Validation Report (persisted by the parent from the evidence-validator agent's returned report)

**Report under validation**: REPORT.md.draft (this folder) | **Timestamp**: 2026-11-19T02:25:00Z
**Total citations**: 37 (30 file:line, 2 whole-file logs, 5 process-table files; the validator counts each distinct cited range) | **Verified**: 37 | **Dropped**: 0 | **Marked [INFERRED]** (counted, not re-read): 3
**Suggested report status**: success on citations alone (the report stays `partial` for the protocol reasons named in REPORT.md)

## Verified
1. The five Pass 2 quotes appear verbatim in `.dev/tasks/done/TASK-WF-makeInstallCoreS-20261119-013812/source.md` line 1.
2. install_core.py:8-12, :59, :71-77, :97-99; install_keep.py:3-7, :20-22, :23-26; install_commands.py:68 and install_user_setup.py:95 call `backup_if_differs`; install_agents.py:56 and install_templates.py:76 only `shutil.copy2`; main.py:178 (`force=force`) and :365 (`force=True`); orca_worktree.py:480, 499, 500, 1682 (and no `clear_cache` anywhere in the file).
3. test_how_we_work_install.py:113, :125 (result ignored), :128-129, :134; plan lines 26 and 36.
4. Logs: t2-checks.log:8-10 IndexError, :7 the `-k same_size` run, :5-6 ruff clean; t1-checks.log 351 passed, 1 skipped; t2-checks.log 352 passed, 1 skipped.
5. Process-table files exist under `.dev/reflect/pre-makeInstallCoreS-20261119-tier2/`; numbers re-read: 0.961 and 0.822 (`adversarial/base-selection.md:159-160`), calibrations 0.88 and 0.75, 6 unaddressed probe findings of which 4 MEDIUM.
6. CPython `filecmp.cmp` clears its cache when `len(_cache) > 100` (system Python 3.13, `/usr/lib/python3.13/filecmp.py:65`; the parent also printed the source of the project's own interpreter).

## Dropped
None.

## True but imprecisely cited (fixed in REPORT.md)
- INV-001 cited `install_core.py:15-29` (the `KNOWN_CORE_FILES` set, only used for listing); the better cites are :59 (the glob), :71-73 (the skip) and :97-99 (the compare). The "8 files sort before PRINCIPLES.md" claim is true.
- "ruff is clean" (Notes) rests on `t2-checks.log:5-6`, now cited.

## Not verifiable by read
- "Switching to the shared function does not change behaviour on unreadable files": the old `_same_content` is deleted from the working tree. The parent Read the old function before it was removed in this session (`except OSError: return False` over `filecmp.cmp(a, b, shallow=False)`), and it is quoted in `artifacts/retries/T1/prompt-1-1.md:30-34`.
- Merge-log figures (10 of 10, 7 of 7), the 9-of-9 convergence, the 32-of-32 calibrator citation count and the memory-persist note were not re-read by the validator.

## Notes
- Counting rule: the draft header said `citations_total: 24`; the validator's rule counts each distinct range (37). REPORT.md now states 37 with the rule.
- Drop rate: 0 of 37. A zero-drop pass is an audit flag, not a clean signal (SKILL.md §11.2): the two items above are where a reviewer could still push back.
- No structural assertions input was supplied, so no A-rule checks ran.
