# QA Report - Final gate, lens gate-command-reproduction

**Topic:** issue-watch implementation, whole change set (nine source files, `main.py` registry edit, test suite and conftest, 19 assumed-shape fixtures, owner runbook)
**Date:** 2026-11-08
**Phase:** Final gate (report only, `fix_authorization: false`)
**Fix cycle:** 1 (first review of this lens at the Final gate)

---

## Overall Verdict: FAIL (1 blocking finding, 7 minor notes)

The blocking finding is F-1: the repository's `detect-secrets` pre-commit hook rejects three lines of the change set, and the plan's "hook-equivalent checks" (G-11 and OQ-44) never ran that hook, so no earlier gate saw it. Every command in the final gate record reproduces exactly (section 1). The prompt asks me to assume at least 20 errors; in this lens I found one blocking defect and seven minor notes, not 20, and I say so rather than pad the table.

## 1. Command reproduction table

Every command was run from the repository root on 2026-11-08, after the newest source/test edit (02:16:30) and after the recorded p9 files (02:20:30 to 02:21:16). Raw outputs are in `/tmp/qa-gcr/` (outside the repository). `make sync-dev` was not run (instructed).

| Gate | Command | Recorded | Reproduced | Match |
|---|---|---|---|---|
| G-1 | `uv run pytest tests/issue_watch/ -v` | exit 0, 2628 passed, 0 skipped | exit 0, `2628 passed in 17.54s`; 2628 `PASSED` lines; 0 SKIPPED/XFAIL/XPASS/ERROR/FAILED; no `warnings summary`, no `Warning:` line | yes |
| G-1 ids | sorted test-id list of the fresh run vs `p9-g1-raw.txt` | 2628 ids | 2628 ids, `diff` empty | yes |
| G-2 | `uv run pytest tests/issue_watch/ tests/skills/test_model_alias_policy.py tests/docs/test_retired_docs_absent.py tests/cli/test_cli_registration.py tests/swarm/test_cli_registration.py tests/recommend/test_cli_registration.py -v -rs` | exit 0, 2658 passed, 1 skipped | exit 0, `2658 passed, 1 skipped`; the one skip is `tests/swarm/test_cli_registration.py:127` "got empty parameter set for (subcommand)" (the allowed pre-existing skip); id list identical to `p9-g2-raw.txt` (2659 lines each) | yes |
| G-3 | `uv run --offline --with "pytest-xdist>=3.5,<4" pytest -n auto tests/issue_watch/` | exit 0, 2628 passed, 0 skipped | exit 0, `2628 passed in 7.14s`, 0 skips, 0 warnings. Repeated three more times with `-n auto`, plus `-n 3` and `-n 32` (28 CPUs): 2628 passed every time | yes |
| G-4 | `make lint` | exit 0, 5 pre-existing warnings, none in issue_watch | exit 0, `Errors: 0`, `Warnings: 5`, `ruff check .` all checks passed; `Errors:`/`Warnings:` lines identical to `p9-g4-raw.txt`; no line mentions `issue_watch` | yes |
| G-5a | `uvx --offline ruff@0.15.20 check src/superclaude/cli/issue_watch src/superclaude/cli/main.py tests/issue_watch` | exit 0 | exit 0, `All checks passed!` | yes |
| G-5b | same paths, `format --check` | exit 0, 31 files | exit 0, `31 files already formatted` (9 package + `main.py` + 21 test py = 31) | yes |
| G-5c | `uvx --offline ruff@0.15.20 format --check src/ tests/` | exit 0, 1234 files | exit 0, `1234 files already formatted` | yes |
| G-5d (extra: the CI command, `.github/workflows/test.yml:100-102`) | `uvx --offline ruff@0.15.20 check src/ tests/ --no-cache` | not recorded | `All checks passed!` | n/a, clean |
| G-6a | `make verify-deps` | exit 0 | exit 0, "installed packages are a subset of the AC3 allow-list" | yes |
| G-6c | `make verify-sync` (sync-dev already run) | exit 0, no drift | exit 0, only headings and check marks, no drift line | yes |
| G-7 | the plan's `grep -rnE 'tomllib\|...\|fromisoformat' src/superclaude/cli/issue_watch/ tests/issue_watch/` | one hit, `predicates.py:30` docstring, justified | one text hit `predicates.py:30` (docstring "DF-35: no ``fromisoformat``"), plus four "binary file matches" lines for stale `__pycache__/predicates.cpython-31{0,1}*.pyc` (see N-2) | yes for source; the record used `--include=*.py` |
| G-8 | `grep -rnE 'shell=True\|os\.system' src/superclaude/cli/issue_watch/` | exit 1 (NO_MATCH) | exit 1, no output | yes |
| G-9 | `uv run superclaude issue-watch --help` | exit 0; exactly check-config, init-state, once, reset, status | exit 0; the `Commands:` block lists exactly those five | yes |
| G-10a | `git diff --exit-code pyproject.toml Makefile` | 0 | 0 | yes |
| G-10b | `git diff --exit-code -- .github/` | 0 | 0 | yes |
| G-10c | `git diff --cached --name-only`, `.claude/` filter | 0 paths | 161 staged paths, 0 outside `.dev/tasks/`, 0 under `.claude/`, `.dev/issues/` or `.dev/brainstorms/` | yes |
| G-11 | trailing space (`.py`, `.json`), CR, final newline | no hit, 48 files, 0 problems | trailing-space grep exit 1; CR grep exit 1; `git ls-files -co --exclude-standard` over the two trees plus the runbook = 50 files, 2 zero-byte `__init__.py`, so 48 non-empty checked, 0 problems; runbook has 0 CR | yes |

## 2. Count and record cross-checks

| Claim (source) | Check | Result |
|---|---|---|
| 9 source files, 4743 lines (`final-change-set.md` section 2) | `wc -l` over `git ls-files -co --exclude-standard -- src/superclaude/cli/issue_watch` | 9 files, 4743; all 9 per-file counts in section 1 of the change set match |
| 21 test Python files, 19243 lines | `wc -l` over the test `.py` files | 21 files, 19243; all 21 per-file counts match |
| 19 fixtures, 291 lines | `wc -l` over `*.json` | 19, 291 |
| runbook 651 lines | `wc -l` | 651 |
| 844 test functions (`ac-trace.md`) | `grep -rE '^\s*(async )?def test_' tests/issue_watch` | 844 |
| `main.py` diff adds 4 lines (import, blank, registration, blank) | `git diff --stat` and `git diff` | 4 insertions; text identical to section 4 of the change set |
| p9 files are newer than the last edit | `find -printf %T` | newest source/test edit 02:16:30; `p9-g1-raw` 02:20:30; `p9-g11` 02:21:16 |
| Gate A to D post-fix counts 686 / 1577 / 2243 / 2628 | read the four `gate-*-postfix*.txt` files | each file says the claimed count; they describe earlier tree states and cannot be re-run, only the last (2628) equals today's count |

## 3. Extra reproduction experiments (read-only runs or /tmp copies)

| Experiment | Result |
|---|---|
| `--collect-only -W error` and a full run with `-W error` | 2628 collected, 2628 passed; no warning |
| Fake `HOME`, `PATH=/usr/local/bin:/usr/bin:/bin` (no `gh`, no `orca` on PATH), empty `GH_TOKEN` | 2628 passed; nothing written under the fake HOME; no new file in the repository |
| Working directory `tests/issue_watch` | 2628 passed |
| /tmp copy of `src/` and `tests/issue_watch/` on the real CPython 3.10.20 (`uv run --offline --no-project --python 3.10`, stub `jsonschema`, pure-Python libs copied from the repo venv) | 2625 passed, 3 failed. The three are the `test_cli_e2e.py` tests that start `sys.executable -m superclaude.cli.main` in a scrubbed environment; the child prints `No module named 'superclaude'`, an artefact of my copy (the package is not installed in that interpreter). Not a defect; the record's "2628 passed on 3.10.20" is therefore only 2625/2628 confirmed by me (N-7) |
| Six skip-guarded tests with `os.geteuid` forced to 0 | 7 tests skip (F-2) |
| markdownlint-cli 0.38.0 from `~/.cache/pre-commit`, repo `.markdownlint.json`, on a /tmp copy of the runbook | exit 0, no finding |
| `check-json` equivalent on the 19 fixtures, `detect-private-key` grep, 1000 kB size limit, case-conflict | all clean |
| `detect-secrets-hook` 1.5.0 (`uvx --offline`), /tmp copy of `.secrets.baseline`, over the whole change set | exit 1, three findings (F-1) |
| Full suite, `pytest -q -n auto --maxfail=30 --ignore=tests/cli/test_verify_sync_hooks.py` (the CI command, `.github/workflows/test.yml:46`; DF-05 left it to CI) | 19575 passed, 137 skipped, 2 xpassed, 4 failed in 61 s. The four failures do not touch `issue_watch`: two `test_claude_process_adapter.py::test_ruff_*` (no `ruff` module in the tool environment: "No module named ruff"), `test_schema_id_rejection.py::test_no_fs_write_when_cli_describe_rejects` (shared `/tmp/eval-runs` seen by another session), `test_parallel.py::...runs_on_separate_threads` (xdist thread-id assertion). Re-run alone, three of the four pass; the ruff one fails for the missing module. None names the new group, so the registration in `main.py` breaks no other test (N-6) |

## 4. Findings

| ID | Severity | Command or file | Evidence | Expected versus actual |
|---|---|---|---|---|
| F-1 | BLOCKING | `.pre-commit-config.yaml:26-42` (detect-secrets hook, `--baseline .secrets.baseline`) against `tests/issue_watch/test_cli.py:633`, `tests/issue_watch/test_cycle.py:381`, `tests/issue_watch/test_origin_parity.py:54`; plan claim in `TASK-RF-...md:968` (OQ-44) and `final-gate-record.md` line 21 | `uvx --offline --from detect-secrets detect-secrets-hook --baseline <tmp copy of .secrets.baseline> <change-set files>` exits 1: "Secret Keyword" at test_cli.py:633 (`secret = "issue title that must never reach the output"`), "Secret Keyword" at test_cycle.py:381 (`secret = "SECRET-PROJECT-VALUE"`), "Basic Auth Credentials" at test_origin_parity.py:54 (`"https://user:token@github.com/IronbellyOrg/IronClaude.git"`). No `pragma: allowlist secret` exists in `tests/issue_watch/`. The baseline (version 1.4.0) lists `KeywordDetector` and `BasicAuthDetector`, so the pinned hook v1.4.0 has the same two plugins; I ran 1.5.0 because 1.4.0 is not in the offline cache | Expected: the hook-equivalent checks the record cites (G-11, JSON parse, runbook reading) cover every hook that would run, or the hook runs clean. Actual: OQ-44 says detect-secrets "is not installed locally" and that "its rules are applied by G-11"; G-11 only checks whitespace, CR and final newline, and detect-secrets is runnable offline and fails on three lines. The Phase 10 commit (and any `pre-commit run`) will be rejected. Fix: add `# pragma: allowlist secret` to the three lines (or a baseline update) and re-run the hook |

## 5. Minor notes (do not fail the gate)

| ID | Where | Note |
|---|---|---|
| N-1 / F-2 | `tests/issue_watch/test_cli.py:892,995 (NOT_ROOT at 1184, 1552, 1578)`, `test_record.py:739`, `test_cycle.py:735`, `test_cycle.py:4644` | Six skip sites make "0 skipped" environment-dependent: with `os.geteuid()` forced to 0, 7 tests skip; on a non-Linux host `test_the_real_proc_mountinfo_gives_a_filesystem_type_for_the_root__df52_c13` skips. The plan says "no SKIP" for G-3 (`research/06-gap-fill-decisions.md:42,48`); the Task Log line at `TASK-RF-...md:1035` admits the sites. A Gate B reviewer (`qa/gate-b/qa-structural-module-boundaries-report.md` M6) asked for the root guard, so this is a known trade-off. The CI runner (Ubuntu, non-root) and this host both skip nothing. Graded minor for that reason; the gate record's "0 skipped" should say "as a non-root user on Linux" |
| N-2 | `p9-g7.txt` vs the plan's G-7 command | The record ran the grep with `--include=*.py` (the file says so). The plan's literal command also prints four "binary file matches" lines from stale `.pyc` files (docstring text is inside bytecode). Harmless and justified, but the justification sits in `p9-g7.txt`, not in the Task Log as the G-7 row of `research/06-gap-fill-decisions.md:52` asks |
| N-3 | `TASK-RF-...md:968` (OQ-44), `TASK-RF-...md:1035` ("markdownlint not installed") | markdownlint 0.38.0 is in `~/.cache/pre-commit/reposcxph1ch`; run by hand against the repo config it exits 0 on the runbook. The claim "not installed" is stale; the result is clean |
| N-4 | `phase-outputs/reports/ac-trace.md` last paragraph | Says the p9 files "predate these docstring edits, so Steps 9.4 to 9.16 must be re-run". They were re-run (timestamps 02:20 to 02:21 follow the 02:16 edits; the final gate record says so). The sentence is a stale step note, contradicting the final record |
| N-5 | `tests/issue_watch/__pycache__/` | Stale bytecode for four scratch test names with no source: `test_dbg_tmp`, `test_smoke_x`, `test_tmp_orig`, `test_zz_scratch_world`. Git-ignored and not collected, never staged; shows scratch files were created and deleted. Not a deliverable defect |
| N-6 | full suite (section 3) | The full suite was left to CI by DF-05. Running it here shows 4 failures none of which is caused by this change set; CI on Python 3.10 may differ (the thread-id and `/tmp/eval-runs` tests are environment-sensitive). Informational |
| N-7 | 3.10 run | My 3.10 harness reproduced 2625 of the 2628; the three e2e tests need an installed package in the child interpreter. The Gate D record of a full 3.10 pass was not independently reproduced; the `grep` for 3.11-only APIs (G-7) is clean |

Side effect of my own experiments: the full-suite run created two git-ignored directories (`relative-home/`, `.dev/sprint-state/`); I removed both. No tracked or staged file changed; I wrote only this report.

## 6. Self-audit and confidence

Checklist counted for this lens: 18 gate-command rows in section 1 (G-1 ids counted with G-1), 8 record cross-checks in section 2, 9 extra experiments in section 3 = 35 items.

- **Confidence:** Verified: 34/35 | Unverifiable: 1 (full Python 3.10 pass of all 2628 tests: harness limit, N-7) | Unchecked: 0 | Confidence: 100.0% of the checkable items (34 of 34)
- **Tool engagement:** Read: 9 | Grep: 6 | Glob: 0 | Bash: about 45 (pytest runs, ruff, make, git, grep, `wc`, `find`, uvx hook tools; each mapped to a row above). Bash outputs are not tracked Reads; no file other than this report was edited.
- **Web research:** none (tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0)
- If I told the user I found one blocking issue in this lens, the evidence is the three hook lines with the exact command, so the claim is checkable. The reason the count is far below the "at least 20 errors" the prompt asks me to assume is that the recorded results all reproduced; I did not invent findings.

## QA Complete
