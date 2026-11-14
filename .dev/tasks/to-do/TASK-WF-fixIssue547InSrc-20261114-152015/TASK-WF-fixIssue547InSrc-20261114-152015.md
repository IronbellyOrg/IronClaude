---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-fixIssue547InSrc-20261114-152015
version: "1"
priority: Medium
created_date: "2026-11-14"
---

# Stop `superclaude sweep` git calls from running repository-configured programs (issue 547)

Source: ./source.md
Goal: No command that repository configuration or the inherited environment defines runs during any git call the sweep makes; a worktree where a git filter could run is reported as `unscanned` instead of being read; the full-page truncation rule counts raw rows. Evidence for every claim below is in ./artifacts/validation.md (measured routes, host numbers, owner design A).

## Constraints

- Owner design A (2026-11-14): `--ignore-submodules=all` goes into the status template; a submodule's own changes are no longer reported. No new JSON key and no new file other than this package and tests; the refusal reuses the existing `unscanned` source row (`SourceCoverage(name, "unscanned", None, reason)` built by `_failed_worktree` in `src/superclaude/cli/sweep/probes.py`).
- The owner-signed git allow-list (`ALLOWED_GIT`) may change only by the three read-only entries named in Task 2; any other allow-list change is not authorized. `ALLOWED_ORCA` and `FORBIDDEN_TOKENS` stay untouched.
- The git-status scope stays separate from the contract allow-list and the transcript scans: `_worktree_paths` and the shared `paths` list in `collect` are not filtered.
- Out of scope: `CLAUDE.md`, `tests/core/test_claude_md_worktree_rule.py`, anything under `.claude/`, wording or alignment edits, new JSON keys, sidecar files.
- Python only through UV: `uv run pytest tests/sweep -q`, `uv run ruff check`, `uv run ruff format`. Never `python -m`, bare `python`, or `pip`.
- Stage named paths only (`git add -- <paths>`, never `git add -A` or `git add .`); the plan package under `.dev/tasks/` is staged with the T2 commit. Commit locally on the current branch with conventional messages ending with the line `Co-Authored-By: Claude Code <noreply@anthropic.com>`. The executor commits only; it never pushes, opens a PR or writes to GitHub (the owner's session pushes afterwards).
- T2 (Tasks 1 to 5) and T1 (Task 6) are two separate commits. The sweep tests forbid a real subprocess unless a test carries the `integration` mark (`tests/sweep/conftest.py` autouse guard); real-git tests must carry that mark.

## Phase 1: T2 regression tests that fail on the current code

## Task 1: Add real-git regression tests for the git-config routes

Create `tests/sweep/test_git_config_hole.py` (module-level `pytestmark = pytest.mark.integration`). Each test builds a throwaway repository under `tmp_path` with a linked worktree (use `git init -b main`, a seed commit, `git worktree add`, with `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1` and a fixed identity set through `monkeypatch.setenv`, as `_FIXED_IDENTITY` in `tests/sweep/test_readonly.py` does), plants a command that writes a marker file under `tmp_path`, then calls `probes.read_worktree(worktree_path, probes.Budget())` (the real seam, no fake) and asserts the marker file does not exist. Method details are in ./artifacts/experiments/repro.sh, repro2.sh, repro3.sh and repro4.sh; a filter test makes the tracked file stat-dirty with `os.utime` and same-size content so git re-reads it. Cases, each its own test:
- `core.fsmonitor` command in the shared `.git/config`.
- `core.fsmonitor` set through a file named by `include.path`.
- per-worktree `core.fsmonitor` (`extensions.worktreeConfig=true`, then `git config --worktree`).
- `GIT_CONFIG_COUNT`, `GIT_CONFIG_KEY_0`, `GIT_CONFIG_VALUE_0` naming `core.fsmonitor` and the `GIT_CONFIG_PARAMETERS` form, both set with `monkeypatch.setenv`.
- `filter.<d>.clean` with `* filter=<d>` in `.gitattributes` and a tracked file: marker absent and the returned coverage row is `unscanned`.
- `filter.<d>.process`, same shape.
- a filter defined in a submodule's own config with the submodule modified (use `protocol.file.allow=always` for `git submodule add`): marker absent.
- a submodule's own `core.fsmonitor`: marker absent.
- control that must keep working: a filter defined but selected by no tracked path (the way `/etc/gitconfig` defines `lfs`): coverage is `read`, the branch is parsed, and no marker exists.
- positive controls: for the `core.fsmonitor` and filter cases, a plain `git status --porcelain=v1 -z --branch --untracked-files=all` run in the test itself does create the marker, so the test can detect a leak.
The file must not edit any existing test. Save the failing run of the new file to `./artifacts/t1-red.log` (command `uv run pytest tests/sweep/test_git_config_hole.py -q`).

Acceptance criteria:
- tests/sweep/test_git_config_hole.py exists and every route case above is a separate test with a docstring naming its route.
- Run on the unchanged `src/superclaude/cli/sweep/probes.py`, the leak tests (fsmonitor, include, per-worktree, environment, both filter forms, both submodule forms) fail because the marker exists; the unselected-filter control and the positive controls pass. The log ./artifacts/t1-red.log shows this.
- No marker file or temporary repository is left outside `tmp_path`.

## Phase 2: T2 git seam and allow-list

## Task 2: Change the git seam, the status template and the allow-list in probes.py

Edit `src/superclaude/cli/sweep/probes.py` only. In `ALLOWED_GIT` (currently one status template, `probes.py:65-67`): append `--ignore-submodules=all` to the status template, and add exactly three read-only templates: `("config", "--show-origin", "--list", "-z")`, `("ls-files", "-z")` and `("check-attr", "--stdin", "-z", "filter")`. Update the comment above the tuple (it says "one allowed git call"). In `_git` (`probes.py:301-326`): build the argv as `git --no-optional-locks -C <cwd> -c core.fsmonitor=false *args` (the `-c` pair comes after `-C <cwd>` so the existing `argv[:3]` and `argv[3]` pins still hold); add keyword parameters `stdin: bytes | None = None` (passed to `subprocess.run` as `input=`) and `binary: bool = False` (return the raw stdout bytes instead of decoded text, so paths that are not valid UTF-8 survive a round trip into `check-attr`). Keep `check_git_args` first, the `GIT_OPTIONAL_LOCKS=0` environment, the timeout and `OUTPUT_LIMIT` handling, and the `GitCallFailed` messages unchanged. Update the `_git` docstring to say fsmonitor is always disabled because repository configuration could otherwise start a program (measured in ./artifacts/validation.md).

Acceptance criteria:
- `probes.ALLOWED_GIT` holds exactly four templates in the order status, config, ls-files, check-attr; `probes.check_git_args` accepts each and still rejects every other argv.
- A real `_git` call builds argv `["git", "--no-optional-locks", "-C", <cwd>, "-c", "core.fsmonitor=false", *args]`, passes `input=stdin` when given and returns bytes when `binary=True`.
- The fsmonitor, include, per-worktree and environment cases of tests/sweep/test_git_config_hole.py now pass (the filter and submodule-filter cases need Task 4 for the filter refusal and pass for the submodule cases through `--ignore-submodules=all`).
- `_read_worktree`'s status call still uses `ALLOWED_GIT[0]` unchanged in position.

## Task 3: Update the pinned tests and the git fake that the seam change forces

Depends on: Task 2

Edit only where Task 2 forces it, and list each edit with its reason in the commit body. `tests/sweep/test_probes_allowlist.py`: the `GIT_STATUS` constant (line 94) gains `"--ignore-submodules=all"` as its last element; the pin `probes.ALLOWED_GIT == (GIT_STATUS,)` (line 364) becomes the four-entry tuple (add constants for the three new templates); the argv assertion in `test_the_one_git_call_is_accepted` (line 503) now expects `["git", "--no-optional-locks", "-C", "/work/tree-a", "-c", "core.fsmonitor=false", *GIT_STATUS]`; the per-path argv assertion near lines 594 to 596 slices `a[6:]` instead of `a[4:]`; add positive checks that each new template passes `check_git_args` and that `status` with `--ignore-submodules=all` missing is now rejected. `tests/sweep/test_readonly.py`: `argv[4:] == list(STATUS_ARGS)` at lines 88 and 157 become `argv[6:]` and each asserts `argv[4:6] == ["-c", "core.fsmonitor=false"]`. `tests/sweep/conftest.py`: the `argv` the fake records (line 71) gains the `-c core.fsmonitor=false` pair; `GitFake.__call__` gains `stdin=None` and `binary=False` keyword parameters, records calls whose args are not the status template in a new list `precheck_calls` instead of `calls` (so the existing "one git call per worktree" assertions keep counting status calls only), and for those pre-check templates returns `""` (empty bytes when `binary`) unless `responses` holds an entry for the key `(str(cwd), args[0])`.

Acceptance criteria:
- `uv run pytest tests/sweep -q` passes except the tests that depend on Task 4 (the two filter-refusal cases of tests/sweep/test_git_config_hole.py).
- No assertion in these files is weakened: each changed line still pins the exact argv or tuple it pinned before, now including the new flag.
- tests/sweep/test_readonly.py `test_collect_makes_one_git_call_per_worktree_that_ps_reports` still passes with `len(patch_git.calls) == extra + 1`.

## Phase 3: T2 filter refusal, documentation and the T2 commit

## Task 4: Refuse to read a worktree where a filter selected by a tracked path could run

Depends on: Task 3

In `src/superclaude/cli/sweep/probes.py` add `_filter_blocks_status(path: Path, timeout: float) -> bool` and call it in `_read_worktree` (`probes.py:921-945`) after the `budget.call_timeout()` check and before the status `_git` call, inside the same `try` so a `GitCallFailed` from any pre-check call is handled by the existing `except GitCallFailed` branch (reason "worktree not readable", or the budget reason on a timeout). Behaviour: run `_git(path, *CONFIG_LIST, timeout=timeout, binary=True)` and parse the `-z --show-origin` output as pairs (origin, then `key\nvalue`); a driver name is a key shaped `filter.<name>.clean` or `filter.<name>.process` (split on the first `filter.` and the last `.clean`/`.process`; keep the driver name's case, git keeps subsection case) with a non-empty value; no such driver means return False with no further call. Otherwise run `_git(path, *LS_FILES, binary=True)` and feed its bytes unchanged to `_git(path, *CHECK_ATTR, stdin=<those bytes>, binary=True)`; parse the `-z` output as triples (path, attribute, value) and return True when any value equals a driver name. Any parse surprise (a triple count that is not a multiple of three, a non-zero exit) fails closed: raise `GitCallFailed`. When it returns True, `_read_worktree` does not run status; it returns `_failed_worktree(path, packages, name, "git filter could run a program")` plus the package rows, exactly as the other failure branches do. Name the three template tuples as module constants next to `ALLOWED_GIT` entries by indexing (`ALLOWED_GIT[1]`, `[2]`, `[3]`), not by repeating the literals. Add a one-line `# shortcut:` comment noting that a filter named only in a submodule's own config is closed by `--ignore-submodules=all`, not by this check. Add unit tests in `tests/sweep/test_probes_allowlist.py` using `patch_git` responses (keys `(str(path), "config")` etc.): no driver means one status call and no ls-files; a driver with no selecting path means status runs; a driver selected by a path means no status call, coverage `unscanned`, reason "git filter could run a program"; a mixed-case driver name matches; a config failure produces "worktree not readable"; a non-UTF-8 tracked path is passed to check-attr byte-for-byte.

Acceptance criteria:
- tests/sweep/test_git_config_hole.py passes in full, including both filter cases (marker absent, coverage `unscanned`) and the unselected-filter control (coverage `read`).
- A filter defined only in `/etc/gitconfig` (the `lfs` shape) and selected by no tracked path leaves the worktree readable; measured against this host's worktrees the new check refuses none (see ./artifacts/validation.md, section "Stage 2").
- The new unit tests pass and the existing `tests/sweep/test_probes_allowlist.py::test_collect_*` source-row tests still pass without editing; the `unscanned` row has no new JSON key (`tests/sweep/test_cli_contract.py` and the report tests are untouched and green).
- `collect` (`probes.py:1217`) and `read_worktree` (`probes.py:948`), the two callers of `_read_worktree`, both get the new behaviour with no change to their own code.

## Task 5: Update the design document where the git call is described and commit T2

Depends on: Task 4

Edit `docs/designs/orchestrator-mode.md` only where a sentence became false: line 67 (GQ-110 says exactly one `git status` per worktree: it now runs up to three read-only inspection calls and then one status, with fsmonitor disabled and submodules ignored), line 542 (the `ALLOWED_GIT` listing), lines 255 and 310 (the argv shown in the diagrams) and line 613 only if it still reads true. Do not touch `docs/designs/orchestrator-mode-review-1.md` (a dated review). Then run `uv run ruff format` and `uv run ruff check` on the changed Python files, `uv run pytest tests/sweep -q`, stage named paths (`src/superclaude/cli/sweep/probes.py`, `tests/sweep/test_git_config_hole.py`, `tests/sweep/test_probes_allowlist.py`, `tests/sweep/test_readonly.py`, `tests/sweep/conftest.py`, `docs/designs/orchestrator-mode.md`, and `.dev/tasks`) and commit locally with the subject `fix(sweep): stop git calls from running repository-configured programs (issue 547)`, a body listing each pinned test edited and why, and the Co-Authored-By line. Save the green run output to `./artifacts/t2-green.log`.

Acceptance criteria:
- `git show --stat HEAD` lists only the named paths and the plan package; no `.claude/` path is staged.
- `uv run pytest tests/sweep -q` passes and `uv run ruff check` reports no error on the changed files; ./artifacts/t2-green.log holds the output.
- docs/designs/orchestrator-mode.md no longer says "exactly one `git status`" without the added inspection calls, and still names no JSON key that does not exist.

## Phase 4: T1 truncation count

## Task 6: Count raw worker rows for the 100-row truncation rule and commit T1

Depends on: Task 5

Add the regression test first, in `tests/sweep/test_probes_allowlist.py` next to `test_collect_worker_list_source_rows_and_truncated` (line 1175): ninety-nine valid worker rows from `_rows([did(i) for i in range(99)])` plus the string `"not-an-object"`, delivered through `patch_orca.respond(wl(RUN1), {"workers": <those 100>, "page": {"limit": 100, "hasMore": False}})` after `_stock_run(patch_orca, RUN1, <the 99 rows>)`; assert `inp.truncated is True`. Run it on the unchanged code and save the failing output to `./artifacts/t6-red.log`. Then fix `_orca_reads` in `src/superclaude/cli/sweep/probes.py` (the `worker-list` block around lines 1049 to 1056): compute the raw count as `len(raw) if isinstance(raw, list) else 0` and use it in `if raw_count >= WORKER_LIST_PAGE or more:`; the `workers` list keeps filtering to objects for later use. Run `uv run pytest tests/sweep -q`, `uv run ruff format`, `uv run ruff check`, stage the two Python files by name and commit locally with the subject `fix(sweep): count raw worker rows for the full-page truncation rule (issue 547)` and the Co-Authored-By line. Do not close the issue and do not push.

Acceptance criteria:
- The new test fails before the fix (./artifacts/t6-red.log) and passes after; the existing 100-row and 99-row cases in `test_collect_worker_list_source_rows_and_truncated` still pass.
- `_orca_reads` callers (`collect`) are unchanged and `uv run pytest tests/sweep -q` passes.
- `git log --oneline -3` shows the T1 commit after the T2 commit, each touching only its own files.
