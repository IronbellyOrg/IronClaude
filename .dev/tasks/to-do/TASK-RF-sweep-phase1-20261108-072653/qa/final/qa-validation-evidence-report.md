# QA Report: Final gate, validation-evidence lens

**Date:** 2026-11-12
**Reviewer:** validation-evidence lens (T318)
**fix_authorization:** false (this report is the only file written)
**Base commit:** `5dc29d23b15eb7db4ead50623bb409f696a0d7d3` (`artifacts/base-commit.txt`, equals HEAD)

Scope: `phase14-sync.md`, `phase14-lint.md`, `phase14-scoped-pytest.md`, `phase14-full-pytest.md` (+ `phase14-full-pytest-output.txt`), `step-1.28-grep.md`, `artifacts/sweep-help-pipx.txt` and `sweep-help-pipx-warmup.txt`, all under `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/`.

## Re-run results (this review, 2026-11-12)

| Command | Recorded | Re-run now | Reproduces |
|---|---|---|---|
| `make verify-sync` | exit 0, "All components in sync" | exit 0, "All components in sync", 0 failure marks, `sc-sweep-protocol` and `sweep.md` listed in sync | Yes |
| `uv run ruff check .` | "All checks passed!" | "All checks passed!", exit 0 | Yes |
| `uv run ruff format --check src/ tests/` | exit 1, 12 files, 1823 formatted | exit 1, 12 files, 1823 formatted; the 12 paths match the recorded list exactly | Yes |
| `uv run pytest tests/sweep tests/commands tests/core tests/skills tests/recommend` | 3220 passed, exit 0 | 3220 passed in 57.93s, exit 0, no FAILED or ERROR line | Yes |
| step 1.28 scoped grep | no output, `exit=1` | no output, `exit=1` | Yes |
| step 1.28 full-tree count | 168 now, 168 at base | 168 now, 168 at base; the sorted `path:line:text` hit sets are identical (`diff` empty), so no hit was swapped | Yes |
| `git diff --cached --name-only -- .claude/`, `git status --short -- .claude/` | empty | empty | Yes |
| step 1.29 help text | `Commands: run`, `exit=0` | `uv run superclaude sweep --help` from /tmp prints the same usage, description and `run` command, exit 0; no file under `src/`, `tests/` or `pyproject.toml` is newer than `sweep-help-pipx.txt` | Yes |

Freshness: files under `src/`, `tests/`, `docs/`, `plugins/` newer than `phase14-sync.md` (14:36) are only `src/superclaude/hooks/hooks.json`, `src/superclaude/hooks/scripts/auggie-flag-clear.sh` and `src/superclaude/cli/install_hooks.py` (mtime 14:39 to 14:40); `git status` and `git diff HEAD` show no content change for all three, so the recorded runs are not stale.

## Analysis of the recorded failures

**12 format failures (phase14-lint.md check 3).** All 12 are Markdown files with embedded Python blocks. For each: `git diff --quiet <base> -- <file>` is clean, `git status --short` is empty and `git cat-file -e <base>:<file>` succeeds. Ruff's verdict depends only on file bytes and config, so they fail at base too. None is among the Python files this change created or edited (`src/superclaude/cli/sweep/*`, `src/superclaude/cli/main.py`, `tests/sweep/*`, `tests/commands/test_sweep_command.py`, `tests/core/test_how_we_work_routing_table.py`, `tests/recommend/test_routing_refresh.py`, `tests/skills/test_worker_contract.py`), which are all inside the 1823 formatted files. Evidence is sufficient.

**Full-run failure 1 and 2 (`test_ruff_flags_synthetic_anthropic_import_under_cli_eval`, `test_ruff_passes_on_real_adapter_module`).** `phase14-full-pytest-output.txt:25423` and `:25429` show stderr `.venv/bin/python: No module named ruff` for `sys.executable -m ruff` (test source `tests/cli/eval/test_claude_process_adapter.py:437-439` and `:468-470`). I confirmed there is no `ruff` entry in `.venv/lib/python*/site-packages` and `uv run ruff --version` prints 0.17.3 (a tool install). `git diff --stat <base> -- src/superclaude/cli/eval tests/cli/eval tests/hooks src/superclaude/hooks` is empty and `git status` on those paths is empty. The cause is the environment, independent of this change. Evidence is sufficient.

**Full-run failure 3 (`test_speed_large_commands[1MB-big]`).** `phase14-full-pytest-output.txt:25433-25434` shows `AssertionError: T-SPD-5 1MB-big: slowest run 1.129 s`, `assert 1.129 < 1.0`. It is a wall-clock assertion on a 1 MB hook input, in a test whose code (`tests/hooks`, `src/superclaude/hooks`) has no diff against base, and which references none of the sweep, WORKER-CONTRACT, HOW-WE-WORK or output-style files. The recorded "passed when re-run alone" is not backed by a saved output file, and I did not re-run it (the test is outside the folders this gate allows me to run). The causal chain (timing test, unchanged code, no shared files) holds without it, so the failure is accepted as not caused by this change, with the gap noted as V-2.

## Step 1.28 and 1.29 pass rules

* 1.28 rule (task item 14.5): scoped grep prints nothing with `exit=1`, and the full-tree count is unchanged at 168. Met, and stronger than the rule: the hit sets match line for line. Extra scope (`src/superclaude/templates`, `plugins/superclaude`) also unchanged at 16 hits now and at base.
* 1.29 rule (REPORT:1300 as restated in item 14.8): run from a non-uv-project directory, 30 s limit, exit 0, help lists `run`. `sweep-help-pipx.txt` ends `exit=0` and lists `run`; the warm-up file shows `installing superclaude from spec '<worktree>'`, `SuperClaude, version 5.0.0`, `exit=0`. The owner chose option (A) (`phase-outputs/plans/OQ-10-pipx-decision.md`, `status: RESOLVED`, decision source cited), and the saved output is for the worktree build (the `sweep` group exists only in this branch; my fresh help output is identical). Met.

## Findings

| id | severity | evidence | what is wrong | smallest fix |
|---|---|---|---|---|
| V-1 | MINOR | `phase-outputs/test-results/phase14-lint.md:109` and `phase14-full-pytest.md:25` say the failures are "logged in `### Phase 14 Findings`"; `TASK-RF-sweep-phase1-20261108-072653.md:3012-3014` reads "No findings yet." | The named section was never populated. The failures are recorded with test ids, causes and base comparison in the two phase14 evidence files and in `.dev/implement/task-rf-sweep-phase1-202-c7ea3265/followups.md:20-22`, so evidence exists; only the cross-reference is wrong. | Add the 12-file format finding and the 3 test findings to `### Phase 14 Findings`, or correct the sentence to point at `followups.md`. |
| V-2 | MINOR | `phase14-full-pytest.md:23` | "Passed when re-run alone (4 passed in the isolated run)" has no saved output; only the failing assertion text is on disk. | Save the isolated run output next to `phase14-full-pytest-output.txt`, or reword to "timing assertion, unchanged code, not re-run". |
| V-3 | MINOR | `phase14-full-pytest.md:3`, `:9` | Full `uv run pytest` (3 failed, 25252 passed) was not re-run here (about 17 minutes, folders outside this gate's allowance). Only the 3220-test scoped subset was reproduced; every failure line in the saved output is one of the 3 analysed above. | None needed. |

No BLOCKING or MAJOR finding.

## Checks

| id | check | result |
|---|---|---|
| C1 | `make verify-sync` re-run reproduces recorded PASS | PASS |
| C2 | `uv run ruff check .` re-run reproduces recorded PASS | PASS |
| C3 | `uv run ruff format --check src/ tests/` reproduces the recorded 12-file failure, same list | PASS |
| C4 | All 12 format failures are untouched by this change and exist at base | PASS |
| C5 | Every Python file this change created or edited passes the format check | PASS |
| C6 | Scoped pytest re-run reproduces 3220 passed, exit 0 | PASS |
| C7 | Recorded runs are not stale (no content change after the 14:36 sync run) | PASS |
| C8 | Full-run failures 1 and 2 are environment-caused with evidence (no ruff module in venv, no diff) | PASS |
| C9 | Full-run failure 3 is a timing failure on unchanged code (assertion text on disk, no diff); isolated re-run unsaved | PASS (with V-2) |
| C10 | Step 1.28 scoped grep: no output, exit 1 | PASS |
| C11 | Step 1.28 full-tree count 168 equals base 168, hit sets identical | PASS |
| C12 | Step 1.29 pass rule: `exit=0`, help lists `run`, option (A) owner decision recorded | PASS |
| C13 | Step 1.29 saved output matches the current build's help (not stale) | PASS |
| C14 | `.claude/` has nothing staged or untracked | PASS |
| C15 | Failures logged where the evidence files say they are logged | FAIL (MINOR, V-1) |

Confidence: Verified 15/15 checks with tool evidence, 0 unverifiable, 0 unchecked. Tool engagement: Read 8, Grep 7, Glob 1, Bash 9. Not re-run: `make lint` (not in this lens's command list) and the full `uv run pytest`.

Verdict: PASS
Blocking count: 0
