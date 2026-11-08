---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: deep
slug: TASK-WF-designSpec-20261108-165559
version: "1"
priority: Medium
created_date: "2026-11-08"
---

# Build the L2 pre-push guard and the switched-off IR-7 refusal path (issue #441)

Source: ./source.md
Goal: A governed agent's push to `refs/heads/main` or `refs/heads/master` from a claimed worktree is refused by an owned git `pre-push` hook installed on claim, human pushes stay unrestricted, the claim report states the real L2 state, and the IR-7 refusal path exists in its own last commit with `IR7_REFUSE = False`, delivered as local commits A, B, C, D, E in the order of source §8.2.

## Constraints

- Owner decision OD-1: L2 covers only the tested local Bash surface. The B-CTX gaps (Monitor, a `setsid` child, a killed supervisor) stay documented limits (source §9.1, LIM-1..LIM-3, LIM-10); no task closes them.
- Owner decision OD-2: an `unknown` identity refuses only pushes whose destination is exactly `refs/heads/main` or `refs/heads/master`, with a diagnostic, and allows every other push (source §7.1, sequence §4.3).
- Owner decision OD-3: the IR-7 refusal code path is built but OFF. `IR7_REFUSE = False`, `W-L2-ABSENT` stays a warning, and the code goes in its own clearly marked commit E after every L2 commit. Turning it on is out of scope.
- The requirements are `.dev/brainstorms/20261108-094705-l2-pre-push-guard/merged-requirements.md` ("the spec"; FR, NFR, AC, LIM and T IDs refer to it). The design (./source.md) adds no requirement; where code and spec disagree, use the proposed resolution in source §12 and list it in that commit's body for owner review.
- Placement (source §1): one shared, owned `hooks/pre-push` found by git's default lookup. Never replace a foreign hook, migrate `core.hooksPath`, forward to another hook, install stubs, or change `hooks.json` or any git configuration. Publish files without replacing an existing file.
- Each UNVERIFIED item in source §11 (U-1..U-14) is settled by the check that item names, in the task that needs it; never assume an answer. A test that needs a second uid (U-7) is `skipif` with a reason when none is available.
- Edit sources under `src/superclaude/` and their `plugins/superclaude/` byte mirrors, then run `make sync-dev` and `make verify-sync`. Never stage any `.claude/` path. Stage only `src/`, `plugins/`, `tests/`, `docs/` and `.dev/tasks/` paths; `.dev/tasks/` is always staged with `git add .dev/tasks`.
- Installed primitives name only `~/.claude/...` or `${0%/*}` paths (NFR-003): `grep -rn 'src/superclaude' src/superclaude/{commands,skills,agents,core,hooks}` gains no hit.
- Read only, never edited: `tests/hooks/test_launch_level_guard.py` (NFR-009, #440) and `.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/`.
- Commits are local only, each ending with the line `Co-Authored-By: Claude Code <noreply@anthropic.com>`. No push and no pull request.
- Python runs through `uv run` only.

## Phase 1: Selector reports why an identity is unknown

## Task 1: Add the FR-025 reason and record to the selector's unknown line

Change `identify()` in `src/superclaude/hooks/scripts/launch-job-identity.sh` so the unknown output carries a reason and the record path as specified in source §6.2 and §7.2 and spec FR-025, splitting the single stale-supervisor branch (about `:224-244`) into `orphaned` (Z state or pid gone) and `stale` (start or boot mismatch, and the sid mismatch), the source §12 OC-3 proposed resolution. Copy the result byte for byte to `plugins/superclaude/hooks/scripts/launch-job-identity.sh`. Settle U-12 by grepping `"unknown"` in `tests/hooks/test_launch_job_identity.py`, and U-14(b) by grepping the repo for any non-test reader of `"status": "unknown"`; move every test that asserts the old plain unknown line where a record exists to the FR-025 shape. Settle U-6 against `proc()` and `boot()` in the same script and keep the stale `rm` remedy wording only if that check holds.

Acceptance criteria:
- `identify()` emits the FR-025 unknown shape with a reason (`orphaned`, `stale`, `foreign`, `unreadable` or the spec's other classes) and the record path, and still emits the old plain shape where no record exists.
- `cmp src/superclaude/hooks/scripts/launch-job-identity.sh plugins/superclaude/hooks/scripts/launch-job-identity.sh` reports no difference.
- `uv run pytest tests/hooks/test_launch_job_identity.py` passes, and the lines found by the U-12 grep are listed in `./artifacts/t1-unknown-shape.md` with the U-6 and U-14(b) findings.

## Phase 2: The pre-push hook and its packaging

## Task 2: Write the C1 pre-push hook and its mirror

Depends on: Task 1

Create `src/superclaude/hooks/scripts/launch-level-pre-push.sh` from the contracts in source §2.2 (push data flow), §5.1-§5.3 (files, data file `pre-push.launch-level`, constants including `L2_VERSION_LINE`), §6.1 (functions `l2_split`, `l2_check` and the rest), §7.1 (exit codes and verdict table with precedence and exit 2), §7.2 (the selector output shapes it accepts) and §7.3 (diagnostic IDs and text), covering spec FR-001..FR-010, FR-020..FR-023 (no environment variable, branch or path changes the actor), NFR-001 (humans are never touched), NFR-004 (no new dependency), NFR-007 (Linux only) and NFR-010 (stdin read in bounded streaming fashion): shebang `#!/bin/bash -p`, actor decided first and ordinary pushes silent, the selector called through `env -i` with `LC_ALL=C`, `UV_NO_CONFIG=1` and the HOME and `uv` directory pinned in the data file, malformed records exiting 2 after reading stdin to EOF, exact protected names only, no bypass named in any diagnostic, arguments ignored and no side effects. Copy it byte for byte to `plugins/superclaude/hooks/scripts/launch-level-pre-push.sh` and make both executable. Settle U-4 (whether `env -i` with HOME, PATH and `UV_NO_CONFIG` is enough for `uv run`) with a clean-HOME run and record the result.

Acceptance criteria:
- Both hook files exist, are executable, start with `#!/bin/bash -p` followed by a newline, carry the `L2_VERSION_LINE` from source §5.3, and `cmp` reports no difference between them.
- `bash -n` passes on the hook, and the hook names no `src/superclaude` path.
- `./artifacts/t2-env-check.md` records the U-4 clean-HOME result and any extra variable it required.

## Task 3: Package the hook for install and pin it

Depends on: Task 2

Add the hook to `_FRESHNESS_SCRIPTS` in `src/superclaude/cli/install_hooks.py` (spec FR-030, source §6.4). In `tests/cli/test_install_hooks.py`, extend the `_FRESHNESS_SCRIPTS` pin (about `:104-105`) with the new name, and add a packaging, mirror and executable test modelled on the existing one near `:930` that asserts the hook's own shebang `#!/bin/bash -p\n` without changing the guard's `#!/bin/bash\n` pin (source §12 OC-5) and keeps the source and plugins copies identical (spec NFR-002, mirror parity), plus the sha256 pin next to `L2_VERSION_LINE` (T-23, NFR-008). Settle U-14(a) by placing the sha256 pin in this file unless the grep finds an existing owner.

Acceptance criteria:
- `uv run pytest tests/cli/test_install_hooks.py` passes, including the new packaging, mirror, executable and sha256 tests.
- Changing one byte of either hook copy makes the sha256 or mirror test fail (shown once by hand, result noted in `./artifacts/t3-pin-check.md`, then reverted).

## Phase 3: Hook behaviour tests and commit A

## Task 4: Write the hook test matrix

Depends on: Task 3

Create `tests/hooks/test_launch_level_pre_push.py` as the spec FR-100 hook test matrix, covering T-01..T-24, T-16a/b/c, T-STALE-1 and the FR-101 leak pins, using the fixture rules in source §10.1 (real git with `GIT_CONFIG_GLOBAL` and `GIT_CONFIG_SYSTEM` set to `/dev/null`, a temporary HOME, `git worktree add` in tmp, remote `for-each-ref` checked before and after every push, a governed actor from the selector's `prepare`/`run` with a fake store, modelled on `LocalPushFixture` in `tests/hooks/test_launch_job_identity.py:1175-1283` but defined in the new file). Until Task 8, place the hook with a direct test-local copy (source §8.2). Map each test to its requirement as in source §10.2 and §10.4 (AC-1..AC-4, AC-7).

Acceptance criteria:
- A governed push to `refs/heads/main` and to `refs/heads/master` is refused and the remote refs are unchanged; the same pushes by a human succeed (AC-1, AC-2).
- An unknown identity is refused only for main and master and allowed for any other branch, with the FR-008 diagnostic (AC-3, OD-2).
- `uv run pytest tests/hooks/test_launch_level_pre_push.py` passes; tests needing a second uid are `skipif` with a stated reason when none exists.

## Task 5: Write the direct-hook record tests and make commit A

Depends on: Task 4

Create `tests/hooks/test_launch_level_pre_push_records.py` with T-D1..T-D5 (spec FR-003, FR-004, FR-006, FR-010, FR-022; source §10.1), including the proposed case of a remote named like an option. Then run `make sync-dev` and `make verify-sync`, stage only the Task 1-5 `src/`, `plugins/` and `tests/` paths plus `.dev/tasks`, and make local commit A with a `feat(hooks): ...` subject describing the hook, the FR-025 selector line, packaging and hook tests (source §8.2).

Acceptance criteria:
- `uv run pytest tests/hooks/test_launch_level_pre_push_records.py tests/hooks/test_launch_level_pre_push.py tests/hooks/test_launch_job_identity.py tests/cli/test_install_hooks.py` passes.
- `make verify-sync` passes and `git show --stat HEAD` lists no `.claude/` path and no file outside rows 1-9 of source §8.1 except `.dev/tasks`.

## Phase 4: Install the hook on claim and report its state

## Task 6: Add the L2 install helpers to orca_worktree.py

Depends on: Task 5

In `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py`, add the source §6.3 symbols for install: an `env=` parameter on `run()` (about `:123-125`, which has none today), `clean_git_env`, `publish_no_replace`, `l2_data_expected`, `L2_VERSION_LINE` and `install_l2(wt)` following the internal flow S1..S4 and T4 in source §3.3 (spec FR-031..FR-039, NFR-006 supported git versions, NFR-011 concurrent installers converge on one identical pair). Take the data file's HOME from `home_dir()` (about `:874`, source §12 OC-8), after settling U-8 by reading the Orca launch path to see whether `cmd_launch` sets the agent's HOME; report an unsafe hooks directory and a git config read error as `unsupported` (OC-9, OC-10); report a differing data file as `conflict` without overwriting (OC-12). Settle U-1 from the git release notes and put the floor in the installer reason text; pick the self-test timeout under `DEFAULT_TIMEOUT` (about `:79`) and document it (U-14(c)); propose reason wording for the states in U-13.

Acceptance criteria:
- `install_l2` publishes the hook and data file without replacing any existing file, leaves `pre-commit` and sample hooks unchanged, leaves no private subdirectory behind, and returns one of the source §7.4 states with a reason.
- `uv run python -c "import ast,sys; ast.parse(open(sys.argv[1]).read())" src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` succeeds, and the U-1, U-8, U-13 and U-14(c) findings and choices are written in `./artifacts/t6-install-choices.md`.

## Task 7: Make l2_status, the session report and cmd_launch use the real L2 state

Depends on: Task 6

In the same `orca_worktree.py`, change `l2_status(wt)` to the read-only re-check of source §3.4 returning a `(state, reason)` tuple (spec FR-024, FR-041), change `session_report` to take that tuple and print its line (about `:1032`, `:1061-1067`, callers near `:1311-1312` and `:1376`; source §12 OC-2), set `L2_ABSENT_WHY` and `REMEDY["W-L2-ABSENT"]` (FR-043..FR-045), rewrite the comment near `:794-795` and the docstring near `:49-51`, and add steps 4-6 of the `cmd_launch` order in source §3.2. The `present-unverified` state is removed (AC-6) and a `core.hooksPath` case reports `unsupported` (OC-6). `W-L2-ABSENT` stays a warning.

Acceptance criteria:
- `l2_status` and `install_l2` report the same state for the same tree, including `conflict` and `unsupported`.
- `grep -rn present-unverified src tests` prints nothing once Task 8's test and claim.md edits land; the remaining hits are listed in `./artifacts/t7-present-unverified.md` until then.
- `cmd_launch` still launches when L2 is absent and prints the `W-L2-ABSENT` warning.

## Task 8: Test install and status, update claim.md, and make commit B

Depends on: Task 7

Create `tests/skills/test_issue_l2_install.py` with FR-102 and its forgery and publication subgroups (spec FR-024, FR-030..FR-045; this satisfies AC-5). In `tests/skills/test_issue_orca_worktree.py`, update `test_ir6_l2_status_follows_the_git_hook_path` (about `:1686-1730`), the remedy assertion near `:1728` (OC-6), the `present-unverified` claim.md assertion near `:1672` (OC-4) and the `W-L2-ABSENT` text assertions (FR-105). Update the `:127` remedy row and `:129` paragraph of `src/superclaude/skills/sc-issue-protocol/refs/claim.md` (OC-4 moves this edit into B). Switch the hook placement in `tests/hooks/test_launch_level_pre_push.py` from the test-local copy to `install_l2`. Run `make sync-dev` and `make verify-sync`, stage only these paths plus `.dev/tasks`, and make local commit B with a `feat(issue): ...` subject; the body records the OC-2, OC-4, OC-6, OC-8, OC-9, OC-10 and OC-12 resolutions and the `core.hooksPath` behaviour change for owner review.

Acceptance criteria:
- `uv run pytest tests/skills/test_issue_l2_install.py tests/skills/test_issue_orca_worktree.py tests/skills/test_issue_protocol.py tests/hooks/test_launch_level_pre_push.py` passes; `tests/skills/test_issue_protocol.py` is unchanged and still lists `W-L2-ABSENT`.
- `grep -rn present-unverified src tests` prints nothing (AC-6).
- `make verify-sync` passes and commit B lists no `.claude/` path.

## Phase 5: L1 guard recognises the L2 hook files

## Task 9: Add the L2 tamper tokens to the L1 guard and make commit C

Depends on: Task 8

Settle U-2 first: check whether #440 has changed `src/superclaude/hooks/scripts/launch-level-guard.sh` on `origin/master` and, if so, stop and record the conflict instead of editing. Otherwise add the second tamper `case` (spec FR-050..FR-052) and the LL-TAMPER text that names the git hook files (FR-054; current `b=` text near `:94-97`) as in source §7.5, copy the file byte for byte to `plugins/superclaude/hooks/scripts/launch-level-guard.sh`, and create `tests/hooks/test_launch_level_guard_l2_tokens.py` with FR-104 (FR-050..FR-055). Run `make sync-dev` and `make verify-sync`, and make local commit C with a `feat(hooks): ...` subject.

Acceptance criteria:
- `uv run pytest tests/hooks/test_launch_level_guard_l2_tokens.py` passes and the two guard copies match under `cmp`.
- `git diff --stat HEAD~1 -- tests/hooks/test_launch_level_guard.py` is empty (NFR-009), and the U-2 result is recorded in `./artifacts/t9-u2-check.md`.

## Phase 6: Documents and the limits re-test

## Task 10: Update the docs to the built L2 and the OFF refusal

Depends on: Task 9

Edit the lines listed in spec §8 and source §8.1 rows 16-21: `docs/designs/sc-issue-launch-level-hook.md` §19.1 `:493`, §19.2 `:508-514`, §19.3 `:516-520`, §19.5 `:528-534`, §19.8 `:567-578`, and `:6`, `:34`, `:355`, rewording §19.2 and the IR-7 definition so the refusal is described as built but OFF until the #442 observations pass (source §12 OC-1); `docs/designs/sc-issue-claim-pipeline-flag.md` `:4`, `:60`, `:135`, `:291`, `:349`, `:381` only where a grep shows they claim no L2 exists (U-11); `src/superclaude/skills/sc-issue-protocol/SKILL.md` `:92`, `:136`, `:150`; `src/superclaude/commands/issue.md` `:16`; `docs/user-guide/commands.md` `:381`. Measure the per-push selector cost and record it in design §19.8 (NFR-005, AC-12, U-3).

Acceptance criteria:
- No edited doc says an absent L2 refuses the launch, and each says `W-L2-ABSENT` is a warning while `IR7_REFUSE` is `False`.
- §19.8 of `docs/designs/sc-issue-launch-level-hook.md` holds the measured selector cost and how it was measured; no test asserts a latency bound.
- The NFR-003 grep gains no hit and `make verify-sync` passes (AC-9).

## Task 11: Write the limits re-test table and make commit D

Depends on: Task 10

Write `./artifacts/final-check-retest.md` (source §8.1 row 22): one row per documented limit in spec §6 and source §9.1 with its current status and evidence, listing OB-H3 (a real claim's install against a disposable local bare destination, design §19.5 `:534`) and U-10 as pending for the owner, not done (AC-11), and the owner-machine observations U-5 (the recorded `uv` directory versus a human pusher's `uv`) and U-9 (remote case folding of `Main`/`MAIN`, LIM-18) as open, not fixed. Run `make sync-dev` and `make verify-sync`, stage the Task 10 doc paths plus `.dev/tasks`, and make local commit D with a `docs: ...` subject.

Acceptance criteria:
- `./artifacts/final-check-retest.md` covers every limit ID in spec §6 and marks OB-H3 pending.
- Commit D changes only `docs/`, `src/superclaude/skills/sc-issue-protocol/SKILL.md`, `src/superclaude/commands/issue.md` and `.dev/tasks` paths, and no `.claude/` path.

## Phase 7: IR-7 refusal path, switched off

## Task 12: Build the IR-7 refusal path OFF and make the separate commit E

Depends on: Task 11

In `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py`, add `IR7_REFUSE = False`, `remedy()`, the two `launch_result` lookups and the IR-7 line in `cmd_launch` that replaces the comment near `:1307-1310` (source §5.3, §6.3 `remedy`, §3.2 step 7, §8.1 row 23; spec FR-060..FR-064). Add FR-103 to `tests/skills/test_issue_l2_install.py` in both switch positions (the `True` position by patching the constant inside the test) plus a source assertion that `IR7_REFUSE is False`. Run `make sync-dev` and `make verify-sync`, then make local commit E, last and separate, with the subject `feat(issue): add the IR-7 W-L2-ABSENT refusal path, switched off`; its body states that E changes no behaviour while `IR7_REFUSE` is `False` and lists the FR-065 turn-on preconditions (owner-recorded PASS for #442 OB-H1 item 1, OB-H2 and OB-H3 including the real-claim disposable-bare-remote check; owner approval; the docs moved from warning to refusal in the same commit; an upgrade path for stale hooks or the owner's acceptance of the re-claim cost).

Acceptance criteria:
- With `IR7_REFUSE = False`, a launch with L2 absent proceeds and prints the `W-L2-ABSENT` warning; with the constant patched to `True` in the test, the same launch is refused (AC-8).
- `uv run pytest tests/hooks/test_launch_level_pre_push.py tests/hooks/test_launch_level_pre_push_records.py tests/hooks/test_launch_level_guard_l2_tokens.py tests/skills/test_issue_l2_install.py tests/skills/test_issue_orca_worktree.py tests/skills/test_issue_protocol.py tests/cli/test_install_hooks.py tests/hooks/test_launch_job_identity.py` passes (AC-10), with output saved to `./artifacts/t12-ac10.log`.
- `git log --oneline -5` shows commits A, B, C, D, E in that order with E on top, `git diff HEAD~5 --stat -- tests/hooks/test_launch_level_guard.py` is empty, and nothing has been pushed.
