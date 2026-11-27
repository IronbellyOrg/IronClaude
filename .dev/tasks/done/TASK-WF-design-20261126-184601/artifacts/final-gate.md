# Task 38 final gate evidence

Date: 2026-11-26. Checkout: /home/coder/workspaces/worktrees/IronClaude/issue-326, branch clayphi/issue-326.
Recorded base commit: 862384852faebe3255c2876527103696cfd3cf3b (from `./artifacts/baseline-tests.log`).
Task 38 is verify-only. No product file was changed and no plugin twin had to be refreshed (every twin was already identical). No formatting fix was needed (see step 3). Nothing was staged or committed. `make sync-dev` wrote only gitignored `.claude/` copies.
Abbreviations: pkg = `src/superclaude`, plugin = `plugins/superclaude`.

## Command results, steps 1 to 5

### Step 1. Source files against plugin twins

| Pair | Result |
|---|---|
| `cmp pkg/commands/implement.md plugin/commands/implement.md` | identical |
| `cmp pkg/commands/git.md plugin/commands/git.md` | identical |
| `cmp pkg/core/HOW-WE-WORK.md plugin/skills/sc-recommend/refs/HOW-WE-WORK.md` | identical |
| `cmp` of sc-implement-protocol `SKILL.md`, `refs/commit-step.md`, `refs/ledger.md`, `refs/retry.md`, `refs/qa.md`, `refs/managed-workspace.md`, `scripts/archive_workspace.py` with their twins | all 7 identical |
| `diff -r -x __pycache__ pkg/skills/sc-implement-protocol plugin/skills/sc-implement-protocol` | no output, rc=0 |
| `diff -r -x __pycache__ pkg/skills/sc-git-protocol plugin/skills/sc-git-protocol` | no output, rc=0 |

### Step 2. Sync and architecture

- `make sync-dev`: rc=0 (28 skill dirs, 49 agents, 36 commands, 17 hooks, 52 templates copied to the ignored `.claude/`).
- `make verify-sync`: rc=0, last line "All components in sync."
- `make lint-architecture`: rc=0, "PASS - architecture policy compliant (4 warning(s))", 0 errors. The 4 warnings are Check 3 line-count warnings for brainstorm.md, reflect.md, spec-panel.md, troubleshoot.md (none is a file of this work).

### Step 3. Ruff

- `uv run ruff check src/ tests/`: rc=0, "All checks passed!"
- `uv run ruff format --check src/ tests/`: rc=1, "6 files would be reformatted, 1576 files already formatted". All 6 are Markdown files (ruff formats their code blocks), none touched by this work:
  - src/superclaude/examples/release-spec-template.md
  - src/superclaude/skills/sc-cleanup-audit-protocol/rules/dynamic-use-checklist.md
  - src/superclaude/skills/sc-pr-submit-protocol/SKILL.md
  - src/superclaude/skills/sc-reflect-protocol/refs/grader-extensions.md
  - src/superclaude/skills/sc-validate-tests-protocol/SKILL.md
  - src/superclaude/templates/documents/release-spec-template.md
- Base comparison (`git archive 862384852... src tests pyproject.toml` into /tmp/base326, same ruff 0.17.3, `ruff format --check --no-cache src/ tests/`): rc=1, "6 files would be reformatted, 1541 files already formatted". The sorted flagged-file lists of base and head are IDENTICAL (diff printed nothing). So the format failure is PRE-EXISTING; this work adds 35 files that are formatted and flags none. `git status` shows none of the 6 files modified. No formatting fix was made. The "exit 0" criterion for `ruff format --check` therefore cannot be met by this task's rules and is reported as a pre-existing failure.
- /tmp/base326 was deleted after the comparison.

### Step 4. Final-gate tests

Command: `uv run pytest tests/core tests/commands tests/skills tests/recommend tests/docs tests/vcs tests/worktree_cleanup -q -p no:cacheprovider -o addopts="--strict-markers --tb=line" -rs -rx` (log: /tmp/t38-gate.log)
Result: `4725 passed, 16 skipped, 2 xfailed in 315.84s`, exit=0. 0 failures (baseline: 3779 passed, 2 skipped, 0 failures, without tests/vcs).
- The 2 xfails are the two known strict xfails in tests/skills/test_implement_commit_rules.py: `test_no_sc_git_protocol_file_contains_the_flag` (FR-052) and `test_legacy_whole_list_review_names_the_current_delivery_files` (FR-079/T-24).
- Skips: 14 are identified from the per-file runs and come from a missing tool (10 in tests/vcs/test_check_message.py: conventional-pre-commit not installed; 1 in tests/vcs/test_precommit_spike.py and 3 in tests/vcs/test_worktree_protection.py: pre-commit not on PATH). The other 2 equal the baseline's 2 skips by count; they were not listed individually in this run (the second `-r` flag replaced `-rs`). Real-framework hook behavior stays UNVERIFIED; the emulator tests for it pass.
- `tests/commands/test_workflow_command.py` passes (28 passed together with test_routing_plugin_parity.py and tests/docs/test_retired_docs_absent.py).

### Step 5. Base-commit check

`git diff --quiet 862384852faebe3255c2876527103696cfd3cf3b -- scripts/worktree_cleanup.py src/superclaude/commands/worktrees.md src/superclaude/hooks/scripts/launch-level-guard.sh src/superclaude/skills/sc-implement-protocol/scripts/archive_workspace.py` -> rc=0. The AC-11 form against `origin/integration` (first three paths) also rc=0.

## AC-01 to AC-21

Verdict key: PASS = observed here by the command or file shown. UNVERIFIED = could not be observed here, reason given.
Per-AC test runs used `uv run pytest <files> -q` (counts below); the whole set also passed in step 4.

| AC | Verdict | Evidence |
|---|---|---|
| AC-01 | PASS | `grep -c '^## Activation' pkg/commands/git.md` -> 1; `grep -c '^## Unattended mode'` -> 0; `grep -c '^> Skill sc:git-protocol'` -> 1 (line 71). Front matter name/category/complexity/argument-hint at lines 1-9; Usage forms at lines 23-27. `tests/commands/test_git_command.py`: 20 passed. |
| AC-02 | PASS | `ls pkg/skills/sc-git-protocol/refs` -> branch.md commit.md safety.md status.md submodule.md; SKILL.md has the operation registry (line 31) and the extension checklist (steps at lines 106-110). `tests/skills/test_git_protocol.py` (registry rows resolve to refs, verbs in `--help`) with test_primitive_dual_surface_lookup.py: 28 passed. |
| AC-03 | PASS | `uv run --no-project python pkg/skills/sc-git-protocol/scripts/vcs.py --help` lists seven verbs: preflight, submodules, stage-plan, verify, reconcile, resolve-check, check-message. `tests/vcs/test_helper_readonly.py`, `test_argv_shape.py`, `test_vcs_entry.py`: 55 passed. |
| AC-04 | UNVERIFIED (index part only) | Passes on disk: `cmp`/`diff -r` of git.md and sc-git-protocol print nothing; `make verify-sync` rc=0; `ls commands/sc-git.md` -> "No such file"; parity test with `git` in its parametrization (tests/commands/test_routing_plugin_parity.py:41) passes (28 passed with its neighbours). The literal observation (`git ls-files commands/sc-git.md` prints nothing and `git ls-files commands/ \| wc -l` prints 20) does NOT hold yet: it prints `commands/sc-git.md` and 21, because the deletion is unstaged (` D commands/sc-git.md` in `git status`) and this task may not run `git add`. It holds once the deletion is staged. |
| AC-05 | UNVERIFIED (live run); helper and static parts PASS | The observation is a live two-task `--commit-tasks` run in a fixture repository, which is agent-driven and was not run here. Covered by tests: stage-plan and boundary tests (tests/vcs/test_stage_plan.py, test_eligibility.py: 277 passed, including `test_sequential_tasks_give_one_boundary_each`), crash-point and commit-line tests (tests/vcs/test_crash_points.py), static commit-step rules (tests/skills/test_implement_commit_rules.py, test_implement_commit_option.py: 51 passed, 2 xfailed). |
| AC-06 | PASS | `test_a_three_member_batch_is_one_boundary_listing_every_member` and `test_a_batch_with_an_unfinished_member_is_not_complete` (test_eligibility.py), `test_a_resumed_batch_makes_one_commit_listing_every_member` (test_crash_points.py); commit-step.md:122 states one commit after every member is `complete`. These run inside the 277 and 316 passed groups. |
| AC-07 | PASS (real hook UNVERIFIED) | tests/vcs/test_hook_refusal.py, test_check_message.py, test_only_semantics.py: 109 passed, 10 skipped (conventional-pre-commit not installed). Behavior of the real `pre-commit` and `conventional-pre-commit` hooks stays UNVERIFIED; the emulator tests pass. |
| AC-08 | PASS | `test_without_a_sidecar_and_without_the_flag_nothing_is_listed_or_written`, `test_an_unflagged_run_may_record_a_proved_existing_commit_but_never_commits`, `test_an_unflagged_resume_after_a_flagged_run_appends_no_commit_and_loses_no_pin` (test_crash_points.py); `test_skill_step_6b_loads_part_one_for_an_unflagged_run_with_a_sidecar` and the static rules (test_implement_commit_rules.py). All in the passing runs. |
| AC-09 | PASS | SKILL.md:75 STOPs `E-COMMIT-PRECONDITION reason=<token>` with `unattended` in its token list; commit-step.md:96 handles the unattended case. `git diff 862384852 -- tests/skills/test_worker_contract.py \| grep NEVER_AS_WORKER` -> no hit (the set is unchanged). tests/skills/test_worker_contract.py passes (1015 passed with tests/core and tests/recommend). |
| AC-10 | PASS (`file://` on CI UNVERIFIED) | tests/vcs/test_submodules.py: 69 passed (local superproject plus `file://` submodule, `protocol.file.allow=always` only in its own temporary repos). Behavior on the CI image stays UNVERIFIED. |
| AC-11 | PASS | `git diff --quiet 862384852 -- scripts/worktree_cleanup.py pkg/commands/worktrees.md pkg/hooks/scripts/launch-level-guard.sh` rc=0 (also against `origin/integration`, rc=0). `tests/worktree_cleanup/`: 595 passed. Scan of the helper scripts for `-D`/`--delete`: only the deny-list `FORBIDDEN_FLAGS` (vcs_rules.py:46-47); no branch-deletion or `update-ref` argv is built. |
| AC-12 | PASS | tests/skills/test_workflow_archive.py: 186 passed (package with `commits.md` archives; `E-ARCHIVE-BLOCKED reason=unsettled-boundary` is in refs/managed-workspace.md:52). See known gap 3. |
| AC-13 | PASS | `cmp pkg/core/HOW-WE-WORK.md plugin/skills/sc-recommend/refs/HOW-WE-WORK.md` prints nothing. `uv run pytest tests/core tests/recommend tests/skills/test_worker_contract.py`: 1015 passed. |
| AC-14 | PASS | `grep -rc 'src/superclaude'` over pkg/{commands,skills,agents,core,hooks}: per-file hit counts identical to base 862384852 (48 files, `diff` printed nothing); the plugin tree is identical to base too. 0 hits in sc-git-protocol, commit-step.md, git.md. The only edited file with hits is `pkg/commands/README.md`, a maintainer note that is not installed, and its hit count did not change. tests/skills/test_primitive_dual_surface_lookup.py passes. |
| AC-15 | PASS with a pre-existing caveat | `make verify-sync` rc=0, `ruff check` rc=0, final-gate pytest exit=0 (4725 passed, 0 failed), `tests/skills/test_worker_contract.py` included. `ruff format --check` rc=1 on 6 pre-existing Markdown files (step 3); it is the same list at the base commit. |
| AC-16 | PASS | `test_a_crash_at_each_point_then_two_resumes_gives_one_commit`, `test_a_commit_before_the_terminal_line_is_recovered_not_repeated`, `test_a_person_committing_on_top_of_the_boundary_commit_is_uncertain` (tests/vcs/test_crash_points.py); the 9-file group (crash points, worktree protection, resolution, emulator, preflight, contract, rules, precommit spike, fixtures) gave 316 passed, 4 skipped (pre-commit not on PATH). |
| AC-17 | PASS (real hook UNVERIFIED) | tests/vcs/test_worktree_protection.py and test_hook_emulator.py are in the 316-passed group; the 3 real-framework tests in test_worktree_protection.py (line 753) skip because `pre-commit` is not on PATH, so the real-framework case stays UNVERIFIED. |
| AC-18 | PASS | `test_every_unsettled_state_offers_abandon_in_a_flagged_and_an_unflagged_run` (tests/vcs/test_resolution.py:147) passes; commit-step.md:86 says `abandon` is always offered. |
| AC-19 | PASS | `test_a_task_completed_outside_an_on_segment_is_never_committed` (test_crash_points.py:389) and `test_a_batch_with_members_in_mixed_segments_is_not_eligible` (test_eligibility.py:607) pass. |
| AC-20 | PASS | Row by row below. |
| AC-21 | PASS | Same observation as AC-14: the NFR-010 `grep` gains no new hit (counts identical to base); T-13 (tests/skills/test_git_protocol.py) passes. |

### AC-20: each seed constraint of section 1.8

| Constraint | Verdict | Check run or read |
|---|---|---|
| `/sc:git` never pushes, merges or opens a PR | PASS | git.md:54 refuses push, pull, fetch, merge, rebase, reset and others as operations and points at `/sc:pr-submit`; git.md:105 Will Not; tests/commands/test_git_command.py 20 passed (T-12). |
| No central relay | PASS | The only `/sc:git` mentions in sc-implement-protocol and implement.md are the "not a required step" list at SKILL.md:219 and prose that names the helper, not a call (commit-step.md:127, SKILL.md:199, implement.md:108); T-09 in test_implement_commit_rules.py passes. |
| PRs stay with `/sc:pr-submit` | PASS | git.md:54, :105, :116 name `/sc:pr-submit`. |
| PR 711 cleanup reused, nothing deletes a remote branch | PASS | Step 5 and AC-11 (rc=0); tests/worktree_cleanup 595 passed; no deletion argv in the helper. |
| No `.claude/` path other than `settings.json` staged | PASS | `git diff --cached --name-only \| grep '^\.claude/' \| grep -v settings.json` -> 0 lines; `git ls-files --others --exclude-standard .claude` -> 0. |
| `.dev/tasks` always staged, evidence committed | PASS | refs/commit.md:14, :46, :59 run `git add -- .dev/tasks`; commit-step.md:11, :135, :139 stage the managed package and the terminal line; T-05 test_only_semantics.py passes. |
| No installed primitive names `src/<package>/` | PASS | AC-14. |
| No commit without authorization | PASS | Authorizing-prefix rule at sc-git-protocol SKILL.md:21; grant-provenance cases in test_crash_points.py and test_eligibility.py pass; AC-09. |
| Destructive operations need confirmation | PASS | `branch cleanup` only prints the `/sc:worktrees` route (git.md:43, :101); `/sc:worktrees` unchanged (step 5), so `--apply` stays; clone URL repeat in refs/submodule.md:53, :61 and tests/vcs/test_submodules.py (69 passed); owner answers: tests/vcs/test_resolution.py passes. |
| Commit step outside the task body, never inside a batch | PASS | commit-step.md:122 (one commit after every member `complete`; never while a task is `halt` or `blocked`); T-19 tests pass. |
| Behavior changes have tests | PASS | tests/vcs has 18 test files plus conftest; static pins in tests/commands/test_git_command.py, tests/skills/test_git_protocol.py, test_implement_commit_rules.py, test_implement_commit_option.py, test_workflow_archive.py; all pass in the gate. |

## Forbidden-token scan (Constraint on `--no-verify`, `--amend`, `commit-tree`, `SKIP=`)

`grep -rnE -- '--no-verify|--amend|commit-tree|SKIP='` over sc-git-protocol, commit-step.md, git.md and implement.md: hits are only the deny-list (`vcs_rules.py:41,43`, `refs/safety.md:8`) and the sentence that forbids them (`refs/commit-step.md:160`). The `refs/safety.md:79` hit is a match of the pattern on ordinary prose text, not a command; it was cut off in the output and not read closely.

## Known follow-up gaps (recorded, not fixed here)

1. Strict xfail 1 (observed in the gate run): helper scripts name the `--commit-tasks` flag, which FR-052 says only the FR-052 files may do: `sc-git-protocol/scripts/vcs.py:83` (docstring) and `:730` (argparse help), `vcs_plan.py:839` and `:2564` (docstrings). Test: `test_no_sc_git_protocol_file_contains_the_flag`.
2. Strict xfail 2 (observed): the legacy whole-list review wording in sc-implement-protocol SKILL.md ("Legacy sources" paragraph of Whole-list review) lacks the current-delivery-files clause of FR-079 / T-24; only `refs/qa.md` states it, for the managed FINAL. Test: `test_legacy_whole_list_review_names_the_current_delivery_files`.
3. `E-ARCHIVE-BLOCKED reason=unsettled-boundary` appears in sc-implement-protocol only in `refs/managed-workspace.md:52` (grep observed). The `refs/qa.md` closed list and the SKILL.md STOP table do not list it.
4. `sc-git-protocol/SKILL.md` step 2 (preflight) versus the preflight narrowing in `refs/branch.md` and `refs/submodule.md`: recorded as reported by the caller; not re-examined in this task.
5. The stop names used by `refs/safety.md` that the SKILL.md refusal catalog lacks: recorded as reported by the caller; not re-examined in this task.
6. `vcs verify` does not fit a plain `/sc:git` commit: recorded as reported by the caller; not re-examined in this task.
7. AC-04 index state: the deletion of `commands/sc-git.md` is unstaged; stage the deletion before the PR so the `git ls-files` observation holds (count 20).
8. Pre-existing, not from this work: `ruff format --check` flags 6 Markdown files at the base commit too (step 3).
9. Still UNVERIFIED by design: real `pre-commit` and `conventional-pre-commit` hook behavior (14 skips), `file://` submodule tests on the CI image, git version floor for `--pathspec-from-file`, `-c core.fsmonitor=false` coverage, the 5-second latency target of NFR-008. Checks that read `git ls-files` see new files only after they are committed, so the pull request's CI run repeats them.
