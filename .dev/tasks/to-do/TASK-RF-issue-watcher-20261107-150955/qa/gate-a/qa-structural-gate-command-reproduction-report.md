# QA Report - Gate A, lens: gate-command-reproduction

**Topic:** issue-watch implementation (Phases 2 and 3)
**Date:** 2026-11-08
**Phase:** task-integrity / gate-command reproduction (report only, fix_authorization: false)
**Fix cycle:** N/A

---

## Overall Verdict: PASS (with minor notes)

No blocking finding. Every recorded gate result was reproduced with an identical outcome. The prompt told me to assume at least 15 errors; I looked for them and did not find any in this lens, so I am not inventing them.

## Commands re-run (repository root)

| # | Command | Recorded result | Re-run result | Match |
|---|---|---|---|---|
| 1 | `uv run pytest tests/issue_watch/ -v` | P3 G-1: 373 passed, exit 0 (P2 G-1: 183 passed) | exit 0, `373 passed in 1.02s`, 373 `PASSED` lines, 0 skipped / xfail / xpass / deselected / errors | yes |
| 2 | `make lint` | P3 G-4: exit 0, 5 architecture warnings, none naming issue_watch, `ruff check .` clean | exit 0, `Errors: 0`, `Warnings: 5` (brainstorm.md, reflect.md, spawn.md, spec-panel.md, troubleshoot.md; same 5 as lines 57-61 of p3-g4-raw.txt), `grep -c issue_watch` = 0, `All checks passed!` | yes |
| 3 | `uvx --offline ruff@0.15.20 check` on the 11 Python files in the change set | P2: 9 files clean; P3: 3 files clean | `All checks passed!`, exit 0 (ruff 0.15.20) | yes |
| 4 | `uvx --offline ruff@0.15.20 format --check` on the same 11 files | P2: `9 files already formatted`; P3: `3 files already formatted` | `11 files already formatted`, exit 0 | yes |
| 5 | `grep -rnE 'shell=True\|os\.system' src/superclaude/cli/issue_watch/` | P3 G-8: exit 1, NO_MATCH | exit 1, no output | yes |

## Additional cross-checks

| Check | Evidence | Result |
|---|---|---|
| Node-id identity, recorded vs fresh run | Sorted `PASSED` node ids from `p3-g1-raw.txt` and from my run, `diff` showed them identical, 373 each | PASS |
| Per-file count arithmetic | test_audit 104 + test_predicates 68 + test_runner 11 = 183 (P2 raw, `collected 183 items`); plus test_github 190 = 373 (P3) | PASS |
| Collection warnings | `--collect-only -q` gave `373 tests collected`; no `PytestCollectionWarning`; the recorded raw files contain no `Warning` | PASS |
| Warnings as errors / stability | 3 runs of `pytest -q -W error -p no:cacheprovider` gave 373 passed each (0.98-1.01 s); `--strict-markers --strict-config -rsxX` gave 373 passed and no skip/xfail section | PASS |
| Exit-code lines in recorded raws | p2-g1-raw, p3-g1-raw, p3-g4-raw each end `EXIT=0` | PASS |
| Change-set line counts | `wc -l` on all 10 .py files and 11 fixtures equals the change-set table (e.g. github.py 901, test_github.py 1250, runner.py 120) | PASS |
| File inventory | `find` on both trees (excluding .pyc) returns exactly the 5 src + 5 test + 11 fixture paths in the change set; none missing, none extra | PASS |
| Ruff over the directories, not just the file list | Pinned ruff `check` and `format --check` on `src/superclaude/cli/issue_watch tests/issue_watch` came back clean | PASS |
| Venv ruff (what `uv run ruff` uses) | `uv run ruff check` and `format --check` on the two directories came back clean, 11 files formatted | PASS |
| Broader process-spawn grep (beyond G-8's two patterns) | `grep -rnE 'shell\s*=\|os\.(popen\|system\|exec\|spawn)\|\bPopen\b\|subprocess\.'` matched only runner.py lines 67, 72, 83, 85 (`shell=False`), 89, 92; no other spawn path | PASS |

## Summary
- Checks passed: 15 / 15 (5 gate commands + 10 cross-checks)
- Checks failed: 0
- Critical issues: 0; blocking issues: 0
- Issues fixed in-place: 0 (report only)

## Findings table

| id | Severity | Command or file | Evidence | Expected vs actual |
|---|---|---|---|---|
| (none) | - | - | - | No blocking finding. Every command reproduced as recorded. |

## Minor notes (do not fail the gate)

1. `uv run ruff` resolves to `/usr/local/bin/ruff` version 0.17.3 (`uv run which ruff`, `uv run ruff --version`), while `pyproject.toml` line 54 pins `ruff==0.15.20` in the dev extra. So G-4 (`make lint`) ran ruff 0.17.3, not the pinned version. Both versions pass on all 11 files (I ran both), and `p3-g4-summary.md` does not state the version. Step 3.9 only asks to record a finding in an untouched file, so this is not a missed deliverable; a one-line version mention in the summary would help.
2. The G-8 grep pattern covers only `shell=True` and `os.system`. The broader grep above shows the only spawn site is `runner.py` with `shell=False`, so the narrow pattern is adequate for the current code. The AST test `test_no_shell.py` planned for Phase 8 is meant to widen it.
3. `src/superclaude/cli/issue_watch/` and `tests/issue_watch/` are untracked in git (`git status --short` shows `??`). Reproduction relies on the working tree. Outside this lens; recorded only so the later staging step is not forgotten.
4. `make lint` prints 5 architecture warnings in files this task did not touch (listed above); recorded as in the P3 summary, nothing to fix.

## Confidence
- **Confidence:** Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 11 | Grep: 2 | Glob: 1 | Bash: 9 (each Bash call re-ran a recorded gate or compared a recorded file against fresh output)
- No web research performed (tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0).
- Limit: pytest ran 5 times in total (1 verbose run, 3 with `-W error`, 1 strict run) and `make lint` once; a flake rarer than about 1 in 5 runs would not show.

## QA Complete
