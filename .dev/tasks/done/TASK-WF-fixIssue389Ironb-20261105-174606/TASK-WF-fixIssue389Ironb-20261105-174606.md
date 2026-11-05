---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-fixIssue389Ironb-20261105-174606
version: "1"
priority: Medium
created_date: "2026-11-05"
---

# Route the ccsession status lines to standard error (issue 389)

Source: ./source.md
Goal: A scripted `claude` call that goes through `ccsession-orca` and `ccsession` (`--version`, `mcp list`, `-p` with stream-json) gets only Claude's own output on standard output, the `[ccsession]` status lines appear on standard error instead, and `superclaude eval` reads the real Claude version from that output. This is the change that unblocks Coder PR 458 (issue 389 is a dependency blocker for merging it).

## Constraints

- Scope is the launcher scripts `src/superclaude/skills/ccsession-tag/ccsession` and `src/superclaude/skills/ccsession-tag/ccsession-orca`, the tests that read their output, `CHANGELOG.md` and the skill `README.md`. `src/superclaude/skills/ccsession-tag/models.py` is not edited: its two `[ccsession]` notes (line 313 `model list updated`, line 837 `model data check`) are routed to standard error at their one call site in `ccsession` (line 1733), so the documented `ccsession --refresh-models` report keeps printing on standard output.
- `src/superclaude/cli/eval/commands.py` (the version probe and `_parse_version`) is not edited. Hardening it (treat a non-zero exit code as "not callable", prefer the `X.Y.Z (Claude Code)` form) is a separate pending decision and must not be added here. Its failure-path behavior (stdout empty because the launcher exited early) is deliberately not pinned by any test in this plan.
- These stay on standard output because the shell captures them: every `models.py` print captured with `$(...)` in `ccsession` (the `PROFILE_*=` lines, digests, shim port, tier lists, compact settings, the `models` and `status` reports), and the values printed by `ccsession --ask`, `--auto-name`, `--list`, `--rm`, `--refresh-models` and `--models-status`.
- Existing `>&2` warnings and errors (`ccsession` lines 823, 944, 973, 980, 1002, 1013, 1080, 1856; `ccsession-orca` lines 136, 211) are correct and stay as they are.
- Edit only under `src/superclaude/skills/ccsession-tag/`, `tests/` and `CHANGELOG.md`. Do not edit `.claude/` mirrors by hand; `make sync-dev` is the only way they change and they are never staged.
- Hardening closure for this fix: the replay run recorded in Task 2 is the positive witness (the negative witness was run before this plan on the unfixed tree), Task 8 supplies the parser fixtures, and the executor's final independent review is the off-path review.
- Evidence the tasks name (logs, outputs) is written under `./artifacts/` in this package.

## Phase 1: Capture the failing replay on the unfixed tree

## Task 1: Add the permanent replay test and record it failing on the unfixed tree

Add `test_version_through_orca_keeps_stdout_clean(tmp_path)` to `tests/unit/test_ccsession_tag.py`, in the ccsession-orca section after the `_orca_no_tty` helper (the helper starts at line 1470; `_orca_env` is at line 1316 and `ORCA` at line 1304). Model it on the throwaway replay at `.dev/troubleshoot/bug-ccsession-prints-status-lines-stdout-20261105170635/artifacts/test_negative_witness.py`, but use the file's own helpers instead of loading the module by path. Build the environment with `_orca_env(tmp_path)`, overwrite the stand-in `tools/claude-record` (the file `_orca_env` creates) with a shell script that only prints `2.1.318 (Claude Code)`, make it executable, then run `subprocess.run([str(ORCA), "--version"], env=env, cwd=tmp_path / "work", stdin=subprocess.DEVNULL, text=True, capture_output=True, timeout=60)`. Do not use `_orca_no_tty`: it joins stdout and stderr and could not tell the streams apart. Import `_parse_version` from `superclaude.cli.eval.commands` at the top of the test file.

Assert, in this order: the return code is 0; `result.stdout == "2.1.318 (Claude Code)\n"`; `"[ccsession] Starting untagged session" in result.stderr`; and `_parse_version(result.stdout + result.stderr) == (2, 1, 318)`.

Run only this test on the tree as it is now, before any launcher edit, and keep the output.

Acceptance criteria:
- The new test exists in `tests/unit/test_ccsession_tag.py` and uses `subprocess.run(..., capture_output=True)` directly, with stdout and stderr read separately.
- Run on the unfixed tree with `uv run pytest tests/unit/test_ccsession_tag.py::test_version_through_orca_keeps_stdout_clean -q -p no:cacheprovider`, it FAILS on the stdout assertion, and the failure output shows three `[ccsession]` lines (tier line, `Shim already running on 127.0.0.1:4555 (reusing)`, `Starting untagged session`) ahead of Claude's line. That output is saved to `./artifacts/t1-negative.log`.

## Phase 2: Route the launcher status lines to standard error

## Task 2: Redirect the informational lines in ccsession to standard error

Depends on: Task 1

Edit `src/superclaude/skills/ccsession-tag/ccsession` (line numbers are those at commit 8b4858f7; re-read each before editing):
- Add `>&2` to the ten informational `echo` lines: 965 (`Shim already running ... (reusing)`), 969 (`A shim with other settings or older code ...`), 984 (`Starting model-alias shim ...`), 1195, 1197 and 1199 (the `$what` profile and tier lines in `export_selection`), 1796 (`Starting untagged session`), 1840 (`... has no saved conversation; starting a new one`), 1849 (`Resuming ...`) and 1864 (`Starting new session labeled ...`).
- Change line 1028 from `python3 - <<'PY'` to `python3 - >&2 <<'PY'` so the Python `print` at line 1077 (`Cached N curated gateway models before launch`) goes to standard error, and add one comment line above the `if ! CC_CACHE_BASE_URL=...` command (line 1024) saying that status goes to standard error so standard output carries only Claude's output.
- Change line 1733 from `python3 "$CCSESSION_MODELS" refresh --wait "${CCSESSION_MODELS_WAIT:-2}" || true` to put `>&2` before `|| true`, so the two `models.py` notes it can print reach standard error without editing `models.py`.
- Do not touch any line that already ends in `>&2`, any `$(...)` capture of `models.py`, or the `--ask`, `--auto-name`, `--list`, `--rm`, `--refresh-models` and `--models-status` paths.

Acceptance criteria:
- `bash -n src/superclaude/skills/ccsession-tag/ccsession` exits 0.
- `grep -n 'echo "\[ccsession\]' src/superclaude/skills/ccsession-tag/ccsession | grep -v '>&2'` prints nothing, and line 1028 reads `python3 - >&2 <<'PY'`.
- The replay test from Task 1, run on the tree with this change, PASSES; its output is saved to `./artifacts/t2-positive.log`. This is the positive witness for the fix.

## Task 3: Redirect the Reopening notices in ccsession-orca and record which tests now fail

Depends on: Task 2

Edit `src/superclaude/skills/ccsession-tag/ccsession-orca`: add `>&2` to the two `echo` lines at 185 (`Reopening this tab's session '$name'`) and 188 (`Reopening this tab's session ${session:0:8}`). These are reachable only when stdin and stdout are terminals and `ORCA_PANE_KEY` is set; the change keeps every `[ccsession]` status line on one stream. Lines 136 and 211 already use `>&2`.

Then run `uv run pytest tests/unit/test_ccsession_tag.py tests/unit/test_ccsession_tiers.py -q -p no:cacheprovider` with only the source edits of Tasks 2 and 3 applied.

Acceptance criteria:
- `bash -n src/superclaude/skills/ccsession-tag/ccsession-orca` exits 0, and `grep -n 'echo "\[ccsession\]' src/superclaude/skills/ccsession-tag/ccsession-orca | grep -v '>&2'` prints nothing.
- The set of failing tests in that run is recorded in `./artifacts/t3-expected-failures.log` and is exactly these six: `test_shim_is_detected_without_lsof`, `test_label_with_missing_transcript_starts_new_session`, `test_default_tier_sets_model_and_tier_window`, `test_a_busy_shim_is_never_stopped_by_a_new_launch`, `test_upgraded_code_starts_a_new_shim_and_keeps_the_old` and `test_model_outside_tier_mode_stays_where_it_was_typed` (the two shim tests may be skipped instead of failing on a machine without a usable shim, and the new replay test must pass). A different failing set means a stdout reader was missed; read that test and handle it in Task 4 or Task 5 before going on.

## Phase 3: Update the existing tests that read these lines from standard output

## Task 4: Update the ccsession tests in tests/unit/test_ccsession_tag.py that read status lines from stdout

Depends on: Task 3

In `tests/unit/test_ccsession_tag.py`:
- `test_shim_is_detected_without_lsof` (stand-in claude `echo launched` at lines 399-401): change line 431 to `assert "Starting model-alias shim" in first.stderr` and line 441 to `assert "already running" in second.stderr`, and add `assert first.stdout == "launched\n"` and `assert second.stdout == "launched\n"` next to them.
- `_label_launch` (lines 1158-1193) returns only `result.stdout`. Split it: add `_label_run(tmp_path, transcript, args=("demo",))` with the same body returning `(result, label_kept)` where `result` is the `subprocess.CompletedProcess`, and make `_label_launch` call it and return `(result.stdout, label_kept)` so its other callers (lines 1226, 1252, 1277, 1294 and any others) need no change.
- `test_label_with_missing_transcript_starts_new_session` (lines 1218-1222): use `_label_run`; assert `"has no saved conversation; starting a new one" in result.stderr`, `"[ccsession]" not in result.stdout`, that `"--resume"` is not in `json.loads(result.stdout.strip().splitlines()[-1])`, and that the label is not kept.
- `test_label_with_saved_transcript_resumes` (lines 1225-1229): keep it on `_label_launch`; it reads the last stdout line, which is still Claude's JSON.
- Leave `test_models_refresh_*`-style tests that call `models.py refresh` directly (line 1054 asserts `model list updated to ...` in stdout and `second.stdout == ""`) unchanged: `models.py` is not edited.

Acceptance criteria:
- `test_shim_is_detected_without_lsof` (or its skip, on a machine without a usable shim) and `test_label_with_missing_transcript_starts_new_session` pass, and no test in `tests/unit/test_ccsession_tag.py` that passed before Task 2 fails now.
- `uv run pytest tests/unit/test_ccsession_tag.py -q -p no:cacheprovider` passes; its output is saved to `./artifacts/t4-tag-tests.log`.

## Task 5: Update the ccsession tier tests in tests/unit/test_ccsession_tiers.py that read status lines from stdout

Depends on: Task 3

In `tests/unit/test_ccsession_tiers.py`:
- `test_default_tier_sets_model_and_tier_window` (line 400): `_launch` returns `(returncode, out, err, seen)` and the stand-in claude prints nothing. Change line 412 to assert `"tier2" in err and "muse-spark-1.3" in err` and add `assert out == ""`. If `out` is not empty, find which write reaches standard output and report it instead of weakening the assertion.
- `_real_launch` (lines 1465-1497) ends with `return proc.stdout, (tmp_path / "seen").read_text().strip()`: add `assert proc.stdout == ""` after the existing return-code assertion, return `proc.stderr` instead of `proc.stdout`, and update its docstring to say the first value is the launcher's standard error (its status lines). The callers `test_a_busy_shim_is_never_stopped_by_a_new_launch` (assertion at line 1523, `"leaving it running" in out`) and `test_upgraded_code_starts_a_new_shim_and_keeps_the_old` (assertions at lines 1918 `"older code" in out` and 1922 `"reusing" in out`) then need no change to their assertion text.
- `test_model_outside_tier_mode_stays_where_it_was_typed` (line 2051): change line 2060 so `"labeled 'work'"` is asserted in `err` (the second `_launch` already unpacks `err`).
- Leave every other test in the file unchanged: tests that read a pty or `stdout + stderr` (for example lines 449-479 and 509), the `--models-status` and `--help` tests, and the `workspace owner unknown` count at line 2526.

Acceptance criteria:
- The four tests named above pass (the two shim tests may skip on a machine without a usable shim), and no other test in `tests/unit/test_ccsession_tiers.py` that passed before Task 2 fails now.
- `uv run pytest tests/unit/test_ccsession_tiers.py -q -p no:cacheprovider` passes; its output is saved to `./artifacts/t5-tiers-tests.log`.

## Phase 4: Pin the stream contract with new tests

## Task 6: Add stream-pinning tests for launch variants, the model refresh note and the refresh report

Depends on: Task 4

In `tests/unit/test_ccsession_tag.py`, using the `_label_run` helper from Task 4:
- Add `test_launch_status_lines_are_on_stderr_only`, parametrized with the same six `(args, transcript)` cases as `test_every_launch_restores_grep_and_glob` (lines 1232-1242). For each case assert that `result.stdout.strip().splitlines()` has exactly one line (the stand-in's JSON argument list), that `"[ccsession]" not in result.stdout`, and that `"[ccsession]" in result.stderr`. Set `CC_CLAUDE_FLAGS` the way the neighbouring test does (`monkeypatch.delenv("CC_CLAUDE_FLAGS", raising=False)`).
- Add a test that the model list update note reaches standard error at launch: follow `test_private_addon_profiles_never_download_model_data` (around line 1259) and its `_DataServer` helper to serve a newer model data version, leave `CCSESSION_MODELS_REFRESH` unset, point `CCSESSION_MODELS_URL` at the server, launch `ccsession --profile claude` with the stand-in claude, and assert `"model list updated"` is in `result.stderr` and not in `result.stdout`. Read the neighbouring tests first and reuse their environment helpers instead of building a new one.
- Add a guard that `ccsession --refresh-models` (handled at `ccsession` lines 1676-1678, with `CCSESSION_MODELS_VERBOSE` set by the script) keeps its `model data check: ...` report on standard output, using the same `_DataServer` pattern, so nobody later moves `models.py` line 837 to standard error.

Acceptance criteria:
- The three new tests pass on the fixed tree and each uses separate captures of stdout and stderr (no `stdout + stderr` join).
- The parametrized test is a real stream pin: its `"[ccsession]" not in result.stdout` assertion is the one that the pre-fix output recorded in `./artifacts/t1-negative.log` (three `[ccsession]` lines on standard output) would violate, and each of the six cases prints at least one `[ccsession]` line on the fixed tree.
- `uv run pytest tests/unit/test_ccsession_tag.py -q -p no:cacheprovider` passes; its output is saved to `./artifacts/t6-tag-tests.log`.

## Task 7: Add a source guard test for the status echoes that tests cannot reach

Depends on: Task 3

Add `test_status_lines_in_launcher_scripts_go_to_stderr` to `tests/unit/test_ccsession_tag.py`. It reads the text of `ccsession` and `ccsession-orca` (use the `SKILL_DIR` constant the file already defines) and asserts: every line that contains `echo "[ccsession]` also contains `>&2`; the cache warm-up heredoc line is `python3 - >&2 <<'PY'` (so the Python print for `Cached N curated gateway models` cannot return to standard output); and the `refresh --wait` line in `ccsession` has `>&2` before `|| true`. This covers the sites a launch test cannot reach in a scratch environment: the Reopening notices (terminal and `ORCA_PANE_KEY` only) and the model cache print (no gateway in the test environment).

Acceptance criteria:
- The test passes on the fixed tree and fails if any one of the lines edited in Tasks 2 and 3 loses its `>&2` (check by confirming the assertion message names the offending file and line).
- `uv run pytest tests/unit/test_ccsession_tag.py::test_status_lines_in_launcher_scripts_go_to_stderr -q -p no:cacheprovider` passes; its output is saved to `./artifacts/t7-source-guard.log`.

## Task 8: Add eval version-check tests for wrapped launcher output

Depends on: Task 2

In `tests/cli/eval/test_doctor_version.py` (the file imports `_check_claude_version` and `doctor_module`; its existing cases pass lambda probes), add:
- A pure parser test: `_parse_version` (import it from `superclaude.cli.eval.commands`) applied to the text Claude's real output then the launcher's standard error, `"2.1.318 (Claude Code)\n[ccsession] Shim already running on 127.0.0.1:4078 (reusing)"`, returns `(2, 1, 318)`. Write the expected text as a single Python string literal so no line of the test file starts with a digit.
- A parser fixture that keeps the old formats working: `claude 0.5.0` and `claude 0.7.3 (build 12)` still parse to `(0, 5, 0)` and `(0, 7, 3)`.
- A real-probe test: create a stand-in `claude` shell script in `tmp_path` that prints `2.1.318 (Claude Code)` on standard output and `[ccsession] Shim already running on 127.0.0.1:4078 (reusing)` on standard error, make it executable, put `tmp_path` first on `PATH` with `monkeypatch.setenv`, call `_check_claude_version()` with no probe (so the real `_default_claude_version_probe` runs) and assert `status.passed is True` and `status.detail == "claude 2.1.318"`.

Do not add a test for the case where standard output is empty; that behavior belongs to the separate eval hardening decision.

Acceptance criteria:
- The three tests pass on the fixed launcher scripts (they do not start `ccsession`, so they also pass on the unfixed tree: they are contract guards for the stdout-first ordering that makes the fix work, not failing-first tests).
- `uv run pytest tests/cli/eval -q -p no:cacheprovider` passes; its output is saved to `./artifacts/t8-eval-tests.log`.

## Phase 5: Document the change and run the full checks

## Task 9: Add the CHANGELOG entry and README sentence, then run the full ccsession and eval test files

Depends on: Task 5, Task 6, Task 7, Task 8

In `CHANGELOG.md`, add a new section at the top of `## [Unreleased]` in the file's existing style: a heading `### ccsession: status lines go to standard error (#389)` and a `#### Fixed (ccsession output streams)` list. The bullets say: every informational `[ccsession]` line (shim, profile and tier, session start and resume, the model cache and model list notes, and the Orca reopen notices) now goes to standard error, so a scripted `claude --version`, `claude mcp list` or `claude -p ... --output-format stream-json` that runs through `ccsession-orca` gets only Claude's own output on standard output; `superclaude eval` therefore reads the real Claude version instead of `127.0.0` taken from the shim address `127.0.0.1:<port>`, because its probe reads standard output first; the lines still show in a terminal; the values printed by `--ask`, `--auto-name`, `--list`, `--rm`, `--refresh-models` and `--models-status`, and the `models.py` output the launcher captures, stay on standard output; redirecting `ccsession` standard output to a file no longer collects the status lines; and the fix reaches a workspace only after `superclaude install` is run again. Add a `#### Added (ccsession output streams)` bullet naming the new tests. Say that it unblocks IronbellyOrg/Coder PR 458.

In `src/superclaude/skills/ccsession-tag/README.md`, add one sentence near the line that says `--ask` prints the question on the terminal and only the answer on standard output (around line 366): ccsession prints its own status lines (`[ccsession] ...`) on standard error, so standard output carries only Claude's output and the results of commands such as `--ask`, `--auto-name` and `--list`; on a terminal both streams look the same. Do not write any `src/superclaude/` path in the README.

Then run the checks: `uv run pytest tests/unit/test_ccsession_tag.py tests/unit/test_ccsession_tiers.py tests/cli/eval -q -p no:cacheprovider`, `uv run ruff check tests/unit/test_ccsession_tag.py tests/unit/test_ccsession_tiers.py tests/cli/eval/test_doctor_version.py`, `uv run ruff format --check` on the same three files, and `make sync-dev` followed by `make verify-sync`.

Acceptance criteria:
- `CHANGELOG.md` has the new `### ccsession: status lines go to standard error (#389)` section as the first entry under `## [Unreleased]`, and the README has the new sentence without a `src/superclaude/` path.
- The full pytest run passes with the replay test passing and the six updated tests passing; its output is saved to `./artifacts/t9-full-run.log`, together with the ruff and `make verify-sync` results in `./artifacts/t9-lint-sync.log`.
- `git status --short` shows changes only under `src/superclaude/skills/ccsession-tag/`, `tests/unit/`, `tests/cli/eval/`, `CHANGELOG.md` and the plan package (no `.claude/` path is staged or edited by hand), and `src/superclaude/skills/ccsession-tag/models.py` and `src/superclaude/cli/eval/commands.py` are unchanged.
