---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-implementPartAOf-20261120-040502
version: "1"
priority: Medium
created_date: "2026-11-20"
---

# Write the claim launch result to a file (issue 691, Part A)

Source: ./source.md
Goal: After `orca_worktree.py launch` runs, the full launch JSON is also saved as `launch-result.json` in the issue folder, for a launched and for a failed launch, so a script can read the terminal, layers and release values without reading the claiming agent's text.

## Constraints

- Edit distributable files only under `src/superclaude/` and tests under `tests/`; then run `make sync-dev` and `make verify-sync`. The `.claude/` copies are never staged, and no installed primitive may name a `src/superclaude/` path.
- Work on a branch cut from `origin/master` in its own Orca worktree, which the person starting the work creates with an agent in it (`orca worktree create --base-branch origin/master --agent claude`); the executor never creates worktrees. This package is copied into that worktree's task folder (the `to-do` folder under `.dev/tasks/`) before `/sc:implement` runs. Part A has no dependency on pull request 685.
- `.dev/tasks/` (this package and its `./artifacts/`) is always staged with `git add .dev/tasks`; the `.claude/` copies and the project-root `artifacts/` folder are never staged.
- Part B is out of scope and is not planned here: `.dev/issues/442/scripts/session-gov.sh`, the observation runbook, `superclaude install` and the live OB-H2 rerun wait for pull request 685 and the owner's yes in chat. A verbatim-print rule for the claiming agent is also out of scope.
- Every `gh` call names `--repo IronbellyOrg/IronClaude`; the pull request is opened with `/sc:pr-submit --monitor 3` and nothing is pushed to or opened against the upstream project.
- The file is best-effort: a failed write never changes the JSON the `launch` subcommand prints, and the existing launch JSON keys keep their names and values.

## Phase 1: The result file is written

## Task 1: Add write_launch_result and call it from cmd_launch

In `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` add a module constant `LAUNCH_RESULT_NAME = "launch-result.json"` next to `RECORD_NAME`, and a function `write_launch_result(source: Path, result: dict) -> None` that writes `json.dumps(result, indent=2) + "\n"` to `source / LAUNCH_RESULT_NAME` through `atomic_write_text` and swallows `OSError` (best-effort, no new warning code, no change to the printed result). In `cmd_launch` route the result of every path that ends `launched` or `failed` through one local helper that calls `write_launch_result(source, result)` and then `emit(result)`: the no-usable-record failure, the stale-prompt failure, the `W-ENFORCEMENT-ABSENT` refusal, the `W-L2-ABSENT` refusal under `IR7_REFUSE`, the launch-record write failure, the failed `orca agent launch`, and the final `launched` result (write it after the `unrecorded` detail text is added, so the file equals what is printed). The `already_launched` path keeps calling `emit` alone, so an earlier result file is never overwritten by a repeat claim. Make the helper a function nested inside `cmd_launch`, so `cmd_launch` is the only caller of `write_launch_result`. A `failed` result of the no-usable-record path (line 1702) also replaces an earlier file: that is intended, because it is the newest result of a launch attempt that ran, and Task 3 says so in the docs.

In `copy_issue_dir` (orca_worktree.py:466-467) change the skip from `rel.as_posix() == RECORD_NAME` to `rel.as_posix() in (RECORD_NAME, LAUNCH_RESULT_NAME)`, so a re-claim of the same issue never copies an earlier `launch-result.json` into a worktree (the copy would otherwise leave a stale machine record there and could create a `.prev` file next to it).

Acceptance criteria:
- After a `launched` call, `<source>/launch-result.json` parses to the same object the `launch` subcommand printed; after a refused or failed call it holds that failed object; after an `already_launched` call the file from the earlier launch is unchanged.
- A `worktree` step run after a launch does not copy `launch-result.json` into `<wt>/.dev/issues/<N>/` and creates no `launch-result.json.prev`, and `worktree.json` is still not copied.
- `launch_result`, `session_report`, `record_launch` and `build_parser` are unchanged, and `cmd_launch` is the only caller of `write_launch_result`.
- `tests/skills/test_issue_orca_worktree.py::test_ir6_launched_result_states_the_release_and_both_layers` and `tests/skills/test_issue_l2_install.py` (which calls `cmd_launch` directly, around line 620) still pass.

## Phase 2: Tests and documentation

## Task 2: Test the result file and update the no-new-file test

Depends on: Task 1

In `tests/skills/test_issue_orca_worktree.py`, next to the `ir6` tests, add four tests that use `launch_scene` and `run_launch`, and a fifth next to `test_fo16_worktree_json_is_never_copied_and_keeps_its_launch_entry` (line 799), named `test_fo16_launch_result_file_is_never_copied_into_the_worktree`, that puts a `launch-result.json` in the issue folder, runs the `worktree` step as `test_fo16` does, and asserts the file is not in `<wt>/.dev/issues/302/` and no `launch-result.json.prev` exists. The four launch tests are: a launched result is written and equals the printed JSON (compare `json.loads` of the file with the returned dict); a refused launch (`launch_scene(..., hook=None)`) writes a `failed` file with `enforcement_hook` `missing`; a second `run_launch` after a launched one returns `already_launched` and leaves the file's bytes identical; a write failure (create a directory named `launch-result.json` in the issue folder before the launch, so the rename in `atomic_write_text` raises `OSError`; do not monkeypatch `atomic_write_text` itself, because `record_launch` also uses it) still prints the launched JSON and exits 0, and the printed dict is unchanged: assert `status` `launched`, `warning` `W-L2-ABSENT` (the scene has no pre-push hook, as `test_la6` shows), `enforcement_hook` `installed`, `terminal` `term_abc` (the handle `LAUNCH_OK` returns), `layers[0]` starting with `L1 guard: effective`, `release` starting with `to release this session` (as the `ir6` test's text shows), and that `detail` does not contain `launch-result`. Name the five tests so each contains `launch_result_file`. Then change `test_launch_creates_no_file_in_the_worktree_or_the_source_directory` (line 2136) so the worktree listing and `git status --porcelain` stay unchanged but the source directory listing gains exactly `launch-result.json`, and rename it `test_launch_adds_only_the_launch_result_file_to_the_source_directory`.

Acceptance criteria:
- `uv run pytest tests/skills/test_issue_orca_worktree.py -k launch_result_file` passes with the five new tests and the renamed one, removing the `write_launch_result` call from the `launched` path makes the first new test fail, and removing `LAUNCH_RESULT_NAME` from the skip in `copy_issue_dir` makes the copy test fail.
- The rest of `tests/skills/test_issue_orca_worktree.py` and `tests/skills/test_issue_l2_install.py` pass unchanged.

## Task 3: Document the file in the claim text and test the docs

Depends on: Task 1

In `src/superclaude/skills/sc-issue-protocol/refs/claim.md`, in the Wave 8 paragraph that describes the launch JSON, add one sentence: the script also writes that same JSON, with `terminal`, `layers` and `release`, to `<D>/launch-result.json` for a `launched` and a `failed` result (never for `already_launched`; a later `failed` result replaces an earlier file), best-effort, so a script can read it instead of the agent's text; the file is separate from the pending record and the `launch` entry of `worktree.json`, which a refusal still does not write (this keeps the paragraph's "no agent and no launch record" wording true). In the same file, in the Wave 7 sentence that says the script never copies `worktree.json` into the worktree (line 104), make it say it never copies `launch-result.json` either. In `src/superclaude/skills/sc-issue-protocol/SKILL.md`, in the Return contract section next to the `enforcement_hook` and `launch_status` text, add one sentence naming `<D>/launch-result.json`, saying it holds the full launch JSON of a `launched` or `failed` launch (never of `already_launched`) and that the agent's printed text is not the machine record. In `src/superclaude/commands/issue.md` add `launch-result.json` (the full launch JSON of a launched or failed launch; never copied into the worktree; not written for `--pipeline none`) to the claim row of the file inventory (line 80). Add a test to `tests/skills/test_issue_protocol.py` beside `test_st9_final_output_lists_the_launch_results_and_every_launch_code` that asserts `launch-result.json` appears in `claim.md` and `SKILL.md`, and that in each the line naming it also contains `launched` and `failed`; add an assertion to `test_claim_outputs_and_examples_cover_the_new_flags` in `tests/commands/test_issue_command.py` (line 169) that the claim row names `launch-result.json`.

Acceptance criteria:
- `claim.md`, `SKILL.md` and the claim row of `commands/issue.md` each name `launch-result.json`, and no distributable file names a `src/superclaude/` path for it (check with `grep -rn --include='*.md' --include='*.py' 'src/superclaude' src/superclaude/skills/sc-issue-protocol src/superclaude/commands/issue.md`, which must show no new line).
- `uv run pytest tests/skills/test_issue_protocol.py tests/commands/test_issue_command.py` passes, including the new test and the new assertion, and `test_st9_final_output_lists_the_launch_results_and_every_launch_code` still passes.

## Phase 3: Ship

## Task 4: Sync the dev copies and open the pull request

Depends on: Task 2, Task 3

Run `make sync-dev` and `make verify-sync` (must exit 0), stage `src/`, `tests/` and `.dev/tasks` (this package and its `./artifacts/`) and never a `.claude/` path, commit on the work branch, rebase on `origin/master`, and open the pull request with `/sc:pr-submit --monitor 3` (head the work branch, base `master`, repo `IronbellyOrg/IronClaude`). The body names issue 691 Part A, states that Part B waits for pull request 685, and states that no agent-printing rule was added. Write the sync and test outputs to `./artifacts/t4-sync.log` (the artifacts folder of this package, not the project-root `artifacts/`).

Acceptance criteria:
- `./artifacts/t4-sync.log` shows `make verify-sync` exiting 0 and the four test files named in Tasks 2 and 3 (`tests/skills/test_issue_orca_worktree.py`, `tests/skills/test_issue_l2_install.py`, `tests/skills/test_issue_protocol.py`, `tests/commands/test_issue_command.py`) passing, and `git status` shows no `.claude/` path staged and `.dev/tasks` staged.
- The returned pull request URL starts with `https://github.com/IronbellyOrg/IronClaude/pull/`.
