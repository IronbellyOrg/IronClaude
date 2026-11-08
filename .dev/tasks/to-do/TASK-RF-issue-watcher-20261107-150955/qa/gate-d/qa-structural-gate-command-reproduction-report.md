# QA Report - Gate D, lens gate-command-reproduction

**Topic:** issue-watch Phase 8 (conftest part 5 and seven cross-cutting test files)
**Date:** 2026-11-08
**Phase:** gate review, report only (fix_authorization: false)
**Fix cycle:** 1 (first review)
**Lens:** gate-command-reproduction (rf-qa)

---

## Overall Verdict: PASS (with minor notes)

Blocking findings: 0. Minor notes: 4.

Every Phase 8 gate command was re-run from the repository root and reproduced the recorded result exactly. No skipped or xfailed test, no collection warning, no flaky result, no count mismatch. No file other than this report was written (a find for files newer than the run marker, excluding cache directories, printed nothing; `git status --short` was identical before and after).

## Commands re-run and comparison with the recorded files

| # | Command (repo root) | Recorded | Reproduced | Match |
|---|---|---|---|---|
| 1 | `uv run pytest tests/issue_watch/ -v` (G-1) | `p8-g1-*`: exit 0, 2616 passed, 16.86s | exit 0, 2616 passed, 16.89s | yes |
| 2 | `uv run --offline --with "pytest-xdist>=3.5,<4" pytest -n auto tests/issue_watch/` (G-3), run A | `p8-g3-*`: exit 0, 2616 passed, 6.40s, 28 workers | exit 0, 2616 passed, 6.28s, 28 workers | yes |
| 3 | same, run B | (second-run flake check) | exit 0, 2616 passed, 6.77s | yes |
| 4 | same with `-n 3` (different worker count, extra flake check) | n/a | exit 0, 2616 passed, 7.97s | yes |
| 5 | `grep -rnE 'shell=True\|os\.system' src/superclaude/cli/issue_watch/` (G-8) | `p8-g8.txt`: EXIT=1, NO_MATCH | no output, grep exit 1 | yes |
| 6 | `uvx --offline ruff@0.15.20 check` then `format --check` on the 8 Phase 8 files (G-5) | `p8-ruff.txt`: "All checks passed!", "31 files already formatted", both EXIT=0 | check exit 0; format exit 0, "8 files already formatted" | yes on verdict; file-count differs, see M-1 |
| 7 | ruff check and format --check on `src/superclaude/cli/issue_watch tests/issue_watch src/superclaude/cli/main.py` | 31 files | check exit 0; "31 files already formatted" | yes (this scope reproduces 31) |
| 8 | the seven Phase 8 test files alone | n/a | 373 passed | consistent with 2616 - 2243 (Gate C cycle 2 total) |

Further checks made:

- Test id sets: the 2616 `PASSED tests/...` ids of the recorded G-3 raw output, G-3 run A and G-3 run B are byte-identical after sort (`cmp`); the G-1 recorded and reproduced `PASSED` line sets are identical after timing and percent normalisation (empty diff). The `-n 3` run also lists 2616 ids.
- Skips: grep for `SKIPPED|XFAIL|XPASS|xfailed|xpassed` as a status in all my outputs returns 0; the pytest summary lines name no skipped, xfailed or warnings category. (A loose `skipped|warning` grep matches only test names such as `..._warning_line_...`; those are PASSED lines.)
- Collection warnings: `--collect-only -q` reports "2616 tests collected" with no warnings summary; `-W error --co` also collects 2616 cleanly.
- Duplicate test ids in the G-1 output: none.
- Side effects: `git status --short` before and after the runs is identical; nothing newer than the run marker outside caches (`.pytest_cache` and `__pycache__` are gitignored).
- Change-set numbers (spot checks): line counts of the 8 files (1155, 443, 961, 373, 275, 191, 961, 375), the two 961-line files being different (32824 and 34121 bytes), empty `find -perm /111`, 21 test python files, 19 `_assumed_shape` fixtures, 9 source files, and the four stale bytecode names all match. Recorded pass counts quoted from the fix reports (Gate A 684 and 686, Gate B 1577, Gate C 2242 and 2243, 59-name pin) match the fix report text; the Gate B cycle 2 report reads "skipped: cycle 2 not selected".

## Findings table (blocking)

| id | severity | command or file | evidence | expected versus actual |
|---|---|---|---|---|
| none | - | - | - | - |

No blocking finding. I looked specifically for: a command that fails, a recorded result that cannot be reproduced, SKIPPED or xfailed tests under xdist, flakiness across repeated xdist runs, collection warnings, count mismatches, and strays written by the test run. None found.

## Minor notes (carried forward, not rechecked)

| id | severity | file | note |
|---|---|---|---|
| M-1 | minor | `phase-outputs/test-results/p8-ruff.txt` | The file records only the outputs ("31 files already formatted"), not the command or the file list, and step 8.12 names 8 files. The 8-file command gives "8 files already formatted"; 31 is reproduced only by a wider scope (`src/superclaude/cli/issue_watch` 9 files + `tests/issue_watch` 21 python files + `src/superclaude/cli/main.py`). `gate-d-change-set.md` explains the mismatch as "consistent with" including earlier files, which is an inference, not a recorded fact. Verdict is unaffected (both scopes pass). Suggest recording the command line in the file. |
| M-2 | minor | `tests/issue_watch/test_cli.py:889,992`, `test_record.py:739`, `test_cycle.py:735,4635` (earlier phases, not Phase 8 files) | Five conditional skips (`skipif geteuid()==0`, `/proc/self/mountinfo` Linux-only). With uid 1000 (this environment) there are 0 skips, so the "zero skips" xdist gate holds; run as root or on a non-Linux host the G-3 "no SKIP" criterion would fail. Environment-dependent, not a defect here. |
| M-3 | minor | `phase-outputs/test-results/p8-g1-summary.md` | The `git status --short` sentence lists the paths the run left untouched but omits the pre-existing untracked `.dev/brainstorms/20261107-064825-github-issue-watcher/` and `.dev/issues/331/` (mtimes 2026-11-07 14:41 and 06:48, before the run), so the sentence is slightly incomplete, not wrong about the run. |
| M-4 | minor | `phase-outputs/test-results/p8-g1-raw.txt` and `p8-g3-raw.txt` | Both include a trailing `EXIT=0` line from the step's `echo`, as the step requires; the xdist raw file names `uv`'s ephemeral venv path in its header, so byte-for-byte reproduction is impossible by design (paths and timings differ). Informational only. |

## Confidence Gate

Checklist for this lens: (1) G-1 reproduces, (2) G-3 reproduces, (3) G-3 second run no flake, (4) zero skips/xfail, (5) zero collection warnings, (6) count parity with recorded, (7) G-8 reproduces, (8) G-5 check, (9) G-5 format, (10) recorded-file vs step command consistency, (11) no stray file written by runs, (12) change-set numbers vs reality.

- **Confidence:** Verified: 12/12 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 3 | Grep: 2 | Glob: 0 | Bash: 10 (all targeted at the checks above; test and lint runs from the repo root with PYTHONDONTWRITEBYTECODE=1, outputs to /tmp only). Web research: none (tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0).
- Tool-count note: Read+Grep+Glob (5) is below the 12 checklist items because most verifications were Bash command runs, the primary evidence for a command-reproduction lens; each Bash call maps to a named row above.

## Self-audit

The prompt expects at least 10 errors; I found zero blocking. The evidence is the eight command rows above (three xdist runs with identical id sets, a serial run with an empty diff against the recorded lines, ruff in two scopes, grep, collect-only with and without `-W error`, before/after `git status`). I did not find a defect, and I did not invent one.

## QA Complete
