# QA Report - Gate B, gate-command-reproduction lens

**Topic:** issue-watch implementation, Phases 4 and 5 (record and launch modules, conftest parts 2 and 3, five test files, two Orca fixtures)
**Date:** 2026-11-08
**Phase:** task-integrity / gate reproduction (report only, `fix_authorization: false`)
**Fix cycle:** N/A (first review)

---

## Overall Verdict: PASS (no blocking findings, 2 minor notes)

Every gate command was re-run from the repository root and reproduced the recorded result exactly. I looked for the 15 expected errors and found none that are blocking. I did not invent findings to reach the number.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Change-set file list and line counts | PASS | `wc -l` of the 8 Python files matched the change set (record 858, launch 348, conftest 230, test_record 2002, test_launch 746, parity 286, origin 176, marker 53). The two fixtures exist in `fixtures/_assumed_shape/` with 14 and 7 lines. |
| 2 | G-1 (P5): `uv run pytest tests/issue_watch/ -v` | PASS | Exit 0, `1372 passed in 2.53s`, 1372 collected. Recorded: `1372 passed` (p5-g1-summary.md, p5-g1-raw.txt line 1383). |
| 3 | Test-ID set equals the recorded P5 run | PASS | A sorted diff of PASSED lines, durations stripped, between `p5-g1-raw.txt` and my run was empty. |
| 4 | No skipped, xfailed, xpassed, failed or errored test | PASS | My run: 1372 PASSED lines and 0 lines matching FAILED, ERROR, SKIPPED, XFAIL or XPASS. The 11 "warning" text hits are test names, not pytest warnings, and there is no warnings summary. |
| 5 | No collection warning | PASS | The collection line reads `collected 1372 items` with nothing else around it. |
| 6 | G-1 (P4) count of 1094 is consistent | PASS | P4 state cannot be re-run, because Phase 5 changed the tree. The numbers are consistent: `test_record.py` collects 408 tests, the four Phase 5 files collect 278, and 1372 - 278 = 1094, which matches p4-g1-summary.md and p4-g1-raw.txt line 1105. |
| 7 | Flakiness | PASS | Three more runs with `-q` all printed `1372 passed` (2.47s, 2.69s, 2.53s), including the real-subprocess timeout tests in `test_runner.py`. |
| 8 | Environment independence | PASS | A run under `env -i` with an empty HOME and a PATH of only uv, `/usr/bin` and `/bin` also gave `1372 passed`. The tests do not need `gh` or `orca` on PATH. |
| 9 | G-4 (P5): `make lint` | PASS | Exit 0. Architecture lint printed 0 errors and 5 warnings: brainstorm.md, reflect.md, spawn.md, spec-panel.md and troubleshoot.md, all Check 3 line-count warnings. `issue_watch` appears 0 times in the output. `uv run ruff check .` printed `All checks passed!`. A diff against `p5-g4-raw.txt` showed only the recorded `EXIT=0` line missing. |
| 10 | G-5 (P5): pinned ruff (0.15.20) on the Phase 5 files | PASS | `uvx --offline ruff@0.15.20 format --check` on the 7 files (launch, conftest, test_launch, both parity tests, marker contract, test_github) gave `7 files already formatted`. This matches p5-ruff.txt. |
| 11 | G-5 (P4): pinned ruff on record.py, test_record.py, conftest.py | PASS | `All checks passed!` and `3 files already formatted`, both exit 0. This matches p4-ruff.txt. |
| 12 | Pinned ruff check and format on all 8 change-set Python files | PASS | `ruff 0.15.20` (`--version` exit 0): `check` printed `All checks passed!` and `format --check` printed `8 files already formatted`, both exit 0. |
| 13 | Project ruff (0.17.3 via `uv run`) as a cross-check | PASS | `uv run ruff format --check src/superclaude/cli/issue_watch tests/issue_watch` gave `18 files already formatted`, exit 0. |
| 14 | pytest config effects | PASS | `pyproject.toml` `addopts` is `-v --strict-markers --tb=short`. There is no `filterwarnings` override that could hide a warning. |
| 15 | Dependence on untracked files | PASS | `grep` of `tests/issue_watch/*.py` found no read of `docs/designs/issue-watcher.md` or any `.dev/` path. The only hits are comments that say `.dev/` is never read. |
| 16 | Working tree unchanged by my runs | PASS | I ran pytest with `-p no:cacheprovider` and removed my `/tmp` outputs. `git status` shows no new modified file. |

## Summary

- Checks passed: 16 / 16
- Checks failed: 0
- Critical issues: 0
- Blocking findings: 0
- Minor notes: 2
- Issues fixed in-place: 0 (report only)

## Issues Found

### Findings table

| id | severity | command or file | evidence | expected versus actual |
|----|----------|-----------------|----------|------------------------|
| (none) | - | - | - | - |

No blocking finding exists. The "at least 15 errors" assumption in the prompt did not hold for gate-command reproduction.

### Minor notes (not rechecked, do not fail the gate)

1. **Pin gap between the `make lint` ruff and the pinned ruff.** `make lint` runs `uv run ruff check .` with ruff 0.17.3. The recorded `p4-ruff.txt` and `p5-ruff.txt` come from pinned 0.15.20. Both versions pass on all files, so there is no defect today. Neither the recorded file nor the change set names the version, so a reader cannot tell which one produced `p4-ruff.txt` and `p5-ruff.txt`. I confirmed 0.15.20 only because my run of it matches the recorded output.
2. **`p5-g4-raw.txt` has an `EXIT=0` line that the `make lint` output does not.** It is the recorder's own marker. The rest of the file is identical to my run. The file `p5-ruff.txt` lists its files only by count (`7 files`), not by name, so the file list behind that count is inferred. The 7 files I used are launch, conftest, test_launch, both parity tests, the marker contract and test_github, and they also pass.

## Actions Taken

None. I wrote only this report. Temporary files in `/tmp` were removed.

## Recommendations

- Proceed. The gate-command results recorded for Gate B are true and reproducible.

## Confidence

Verified: 16/16 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

(The P4 count in item 6 is verified by arithmetic over collect-only counts, not by re-running the Phase 4 state, which no longer exists.)

**Tool engagement:** Read: 7 | Grep: 1 | Glob: 1 | Bash: 9 (the grep count excludes in-shell greps)

## QA Complete
