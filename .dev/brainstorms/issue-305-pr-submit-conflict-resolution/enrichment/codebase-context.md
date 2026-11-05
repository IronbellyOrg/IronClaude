# Codebase context: sc:pr-submit merge-conflict resolution (issue #305)

Retrieval tier: codegraph index healthy (1958 files, 0 pending changes at 2026-11-04), then Read/Grep. Auggie was not available. Paths are relative to the repo root. GitHub API behaviour not in the repo is marked **[external]**.

## 1. Waves, refs, scripts, command flags

- The ordinal `--monitor {0,1,2,3}` is a ceiling on one FSM. The Python core owns the decisions. SKILL.md owns sequencing, the poll loop, the `gh`/`git` I/O and the VAL gates (`src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:36-41`).
- Wave table (`SKILL.md:252-265`). Each wave lazy-loads its own ref and never pre-loads: W0 open/attach (no ref), W1 `detection-contract.md` + `augment-poll.md`, W2 `severity-routing.md`, W3 `finding-verify.md`, W4 `troubleshoot-dispatch.md`, W5 VAL (inline), W6 `thread-reply.md` + `review-retrigger.md`, W6b `auggie-fallback.md`, W7 `loop-guard.md`, W8 `ci-poll.md`. A new conflict wave would add a row here plus its own `refs/<name>.md`, which loads only in that wave.
- The refs folder holds 11 files, including `state-machine.md` and `auggie-fallback.md`. No SKILL.md wave loads `state-machine.md` directly; the purpose section cites it (`SKILL.md:37`).
- Scripts (all take `--repo`, so all `gh` I/O is repo-pinned):
  - `scripts/poll-augment-review.sh` takes one snapshot (reviews, comments, threads) that serves both reviewers. Its PR read is `--json number,url,headRefName,headRefOid,baseRefName` (`poll-augment-review.sh:38`), and the payload it emits has `head_sha` and `base` (`:162`).
  - `scripts/poll-ci-checks.sh` polls CI for Wave 8 and prints one JSON line (`poll-ci-checks.sh:3-11`, `:92`).
  - `scripts/retrigger-review.sh` posts the S5a re-trigger comment (`retrigger-review.sh:3-17`).
  - `scripts/reply-resolve-thread.sh` replies to a thread first, then resolves it (`reply-resolve-thread.sh:3-16`).
  - None of these scripts reads `mergeable` or `mergeStateStatus`.
- Command flags (`src/superclaude/commands/pr-submit.md:8`, `:42-56`): `--monitor --max-rounds --poll-interval --timeout --silence-timeout --base --head --pr --title --body --output-dir --resume`. The parser accepts exactly these flags (`src/superclaude/pr_submit/fsm.py:73-99`), so a new flag (for example a conflict tier cap) needs `SkillArgs`, `parse_args` and the command table.

## 2. The push path

- **Fix commit (Wave 6, `SKILL.md:274`)**:
  - Exactly one commit per cycle, made only when `applied_edits > 0` and VAL is green.
  - It stages only `git add -- <paths>` (never `-A` or `.`) and commits with `git commit --only -- <paths>`.
  - It refuses any path in `OPERATOR_PENDING`. Both a refused path and a failed commit end in `terminal_halted` with reason `fix_commit_failed`.
  - **[external]** git refuses `git commit --only <paths>` while a merge is in progress ("cannot do a partial commit during a merge"). So a merge resolution cannot use the current commit recipe as written.
- **Pre-push head guard (`SKILL.md:274`)**: it re-reads `gh pr view --json headRefName,headRefOid,isCrossRepository` and requires `pr_head_ok(local_branch, pre_push_sha, ...)` plus `headRefName == HEAD_BRANCH`.
  - `pr_head_ok` requires an exact branch match and an equal 40-hex SHA, compared case-insensitively (`fsm.py:555-579`). The branch check itself is `pr_branch_ok` (`fsm.py:528-552`).
  - A mismatch halts with reason `pr_head_mismatch`, and no push record is written.
- **`push_parent_ok` (`fsm.py:582-600`)**: `len(target_parents) != 1` fails (`:593`). The single parent must also equal `pre_push_sha`. The docstring says a merge commit (two parents) fails closed (`:588-590`), and a test pins this (`tests/pr_submit/test_pre_pr_checks.py:216-222`, id `merge`). It exists because a fast-forward push publishes every commit between the PR head and `target_sha` (`fsm.py:585-587`). A failure halts with reason `push_range_mismatch` (`SKILL.md:274`, `:317`).
- **`evaluate_push_decision` (`fsm.py:173-204`)** is the INV-016 conjunction: ordinal >= 3, validated, no human decision, `round_counter < max_rounds`, `applied_edits > 0`. `push_fail_state` maps each block to a terminal (`fsm.py:207-219`).
- **Idempotency key and triad**: the key is `push:<run_id>:<cycle_id>:<pre_push_sha>:<target_branch>` (`fsm.py:227-235`). `build_push_triad` emits `push_decision`, `push_initiated`, `push_completed` in that order. The records carry no field that says what kind of push it was (fix or merge) (`fsm.py:238-288`). The SKILL runs `git push origin <target_sha>:<target_branch>` and never force-pushes (`SKILL.md:274`, `:305`).
- **Run-log**:
  - `RunLog.append` rejects any `event_type` outside the closed `EventType` enum (`run_log.py:108-119`). That enum has 41 members (`models.py:22-90`).
  - `rebuild_state` adds every `push_completed` to `push_count` and `pushed_commit_shas` (`run_log.py:238-241`). So a conflict-resolution push would count against the Output Contract's `push_count` (`SKILL.md:239`, "== max_rounds at most") and against INV-R2's `push_count <= max_rounds + 1` (`SKILL.md:275`).
  - There are 7 idempotency sets (`run_log.py:26-35`).
- **Recovery** (`src/superclaude/pr_submit/recovery.py`):
  - `detect_crash_window` matches an unfinished `push_initiated` by its key (`:57-80`).
  - Branch A means the push landed. Recovery writes `push_completed{recovered}` and resumes at S5a or S5, depending on whether `rereview_requested` exists for the cycle (`:112-147`).
  - Branch B means the push did not land. Recovery re-drives the push without recomputing the fix (`:149-159`). The SKILL skips the fix commit and runs the pre-push guard with the record's `pre_push_sha` (`SKILL.md:268`).
  - Branch C means the remote tip is ambiguous, so recovery stops at `HALT_HUMAN` (`:161-171`).
  - Recovery does not tell a fix push from a merge push.

## 3. Behind-base handling today

- `needs_rebase(commits_behind) -> commits_behind > 0` is the only pure helper for this (`fsm.py:603-610`), and its test is `test_pre_pr_checks.py:64-72`.
- **Create path**: Wave 0 rebases if the branch is behind `origin/<base>` **before** creating the PR (`SKILL.md:267`). But the STOP block lists "a branch behind the base branch ... on the create path" as a HALT (`SKILL.md:220-223`), and so does the Error Handling row (`SKILL.md:315`). These conflict today: one says rebase, the other says halt.
- **`--pr <N>` path**: never rebase; only report how many commits behind (`SKILL.md:267`). The head-binding message warns that "a branch Wave 0 rebased needs a force-push, which this skill never does for you" (`SKILL.md:268`).
- **GitHub mergeability**: a grep of `src/superclaude/pr_submit/`, the skill folder, the command and `tests/pr_submit/` for `mergeable|mergeStateStatus|DIRTY|CONFLICTING` returns **zero hits**. Nothing reads GitHub's conflict state today. **[external]** `mergeable` is MERGEABLE/CONFLICTING/UNKNOWN and is computed asynchronously, so the first read can be UNKNOWN. `mergeStateStatus` includes DIRTY and BEHIND. GitHub does not run `pull_request` workflows while the PR has a merge conflict, so a Wave 8 CI wait on a conflicted PR may only ever report `polling`.

## 4. FSM shape

- `MonitorState` has 23 members (`models.py:103-138`):
  - Working states: S0_IDLE, S2_CLASSIFY, S2b_VERIFY, S3_DIAGNOSE, S3_FIXING, S7_VALIDATING, S4_PUSHING, S4_HALT_BEFORE_PUSH, S6_REPLYING, RESOLVING, S5_AWAITING_REREVIEW, S5a/S5b/S5c, PROPOSED, REPORT_ONLY.
  - Terminals: TERMINAL_CLEAN, HALT_MAX_ROUNDS, HALT_HUMAN, VALIDATION_FAIL, TERMINAL_TIMEOUT, TERMINAL_AUGMENT_NO_RESPONSE, TERMINAL_FAILED.
- `transition()` is a flat `(state, event)` table. The `needs_human_decision` check runs first (`fsm.py:716-731`). An unknown edge "stays put" (`fsm.py:801-802`), so a new event silently does nothing until it gets an edge.
- Gates are one-liners: `gate_arm` is ordinal >= 1 and `gate_edit` is ordinal >= 2 (`fsm.py:142-149`). G-push is ordinal >= 3 plus the conjunction (`state-machine.md:70-84`).
- **Loop guard**:
  - `should_halt_rounds` calls `loop_guard.should_halt`, which is `round_counter >= max_rounds` (`fsm.py:152-159`, `loop_guard.py:23-30`).
  - The counter ticks only on the attributed re-review edge, S5 to S2 (`fsm.py:776-777`, `:1174`; `state-machine.md:91-93`).
  - `clamp_max_rounds` handles the fallback budget (`fsm.py:162-170`).
- `state-machine.md` calls itself "the COMPLETE single-source enumeration of reachable states" (`state-machine.md:135-138`). Codex was added without any new state, by merging reviewer outcomes before the FSM sees them (`state-machine.md:62-68`), and the CI phase added "no new FSM edges" (`state-machine.md:140-157`). A new conflict state or event must therefore update `models.py`, `transition()`, `state-machine.md` and the tests. Alternatively, it can follow the Codex/CI pattern and stay SKILL-owned, outside the FSM.

## 5. Validation and staging rules

- VAL runs in order (`SKILL.md:279-291`):
  - VG-1 targeted tests, plus advisory impact tests (`:284`).
  - VG-2 runs `make test` when the change is cross-cutting (`:285`). `is_cross_cutting` treats `fsm.py` and `run_log` as shared, so they force VG-2 (`fsm.py:613-642`, markers at `:623`).
  - VG-3 lint (`:286`).
  - VG-4 `ruff format --check`, kept separate from lint (`:287`).
  - VG-5 verify-sync (`:288`).
  - VG-6 PR target (`:289`).
- `run_validation_gates` returns validated only when every gate that ran passed and VG-1, VG-3 and VG-4 were all present (`fsm.py:441-474`). A retry does not tick the round counter (`SKILL.md:291`).
- `OPERATOR_PENDING` is captured once per cycle, before the first edit, from `git status --porcelain=v1 -z --untracked-files=all`. It covers modified, staged and untracked files and both sides of a rename (`SKILL.md:272`). The fix commit refuses any of these paths before staging (`SKILL.md:274`).
- **[external]** `git merge` refuses to start when local changes would be overwritten. The seed brief rules out stashing because worktrees share one stash stack.
- At L2, the run stops before any commit: S3_FIXING, then S7_VALIDATING, then S4' (`SKILL.md:273`, `state-machine.md:95-106`). A merge resolution is a commit by nature, so L2 needs an explicit rule: either leave the merge unconcluded or allow a local-only commit.

## 6. Test conventions and break points

- Pure helpers are tested with direct calls, often parametrized fail-closed shapes (`test_pre_pr_checks.py:201-230`). The FSM is driven through `run_skill(RunConfig)` with injected seams (`fsm.py:836-879`; `test_autonomy_gates.py:56-141`). Recovery tests use a real `RunLog` under `tmp_path` (`test_crash_recovery.py:208-347`).
- Static-grep pins in `tests/pr_submit/test_static_grep.py`:
  - **T-N50**: no `\bgh\b` or `\bgit\b` token anywhere, docstrings included, in `CORE_PURE_FILES`: `state-machine.md`, `severity-routing.md`, `loop-guard.md`, `auggie-fallback.md`, `fsm.py`, `severity_router.py`, `loop_guard.py`, `ci.py` (`:37-51`, `:132-143`). New conflict helpers in `fsm.py`, or new prose in `state-machine.md`, must avoid the word "git".
  - **T-N41**: no `anthropic` import in any `pr_submit/*.py` (`:146-155`).
  - **Head-binding and push test** (`:627-755`), which pins literal substrings and their order:
    - the rebase wording (`:656-661`);
    - head check before parent check before "The deterministic core DECIDES" (`:664-676`);
    - the staging recipe (`:713-717`);
    - the OPERATOR_PENDING text (`:724-736`);
    - the state-machine parent sentence (`:749-750`);
    - the command's Will Not sentence "push any commit besides the cycle's one fix commit" (`:754-755`).
  - **Force push**: no force form of `git push` anywhere in the skill folder (`:758-776`).
- SKILL.md must contain **exactly one** python code block, which the tests execute (`test_cosmos_protocol.py:33-45` at `:36`; `test_codex_reviews.py:685-697` at `:688`). A second python block for conflict logic breaks both tests.
- The closed enum count is pinned: `len(EventType) == 41` (`test_run_log.py:168-169`; `test_codex_reviews.py:441`). Any new run-log event means editing both tests.
- Ref fragment pins: `test_cosmos_protocol.py:209-258` covers `SKILL.md` and the refs `detection-contract`, `augment-poll`, `review-retrigger`, `severity-routing` and `thread-reply`. `test_codex_reviews.py:718-749` pins the A5 fragments and the per-reviewer event list.
- Other readers:
  - `test_edge_cases.py:263-267` matches "Wrong origin" / "behind" / "wrong-owner".
  - `tests/commands/test_impact_command.py:327-345` requires SKILL.md and `refs/troubleshoot-dispatch.md` to keep `Skill sc:impact-protocol` and `--caller sc-pr-submit-protocol`.
  - `tests/unit/test_cli_install.py:248-262` lists the installed skill files. It is a presence check only (`:496-500`), so adding a ref or script passes and renaming one fails.
- Files that read SKILL.md, refs or the command: `test_static_grep.py`, `test_cosmos_protocol.py`, `test_codex_reviews.py`, `test_edge_cases.py`, `tests/commands/test_impact_command.py`, `tests/unit/test_cli_install.py`. Scripts are also exercised by `test_cosmos_poll.py:16` and `test_codex_reviews.py:516`.

## 7. Reusable pieces

- `evidence-validator` agent: read-only (`tools: Read, Grep, Glob`, `permissionMode: plan`), and it re-reads every file:line citation (`src/superclaude/agents/evidence-validator.md:1-9`, `:18-30`). It suits checking a resolution record's cited hunks. It cannot run git.
- `troubleshoot-analyst` agent: read-only plus codegraph and auggie (`troubleshoot-analyst.md:2-5`). `root-cause-analyst` is the general-purpose version. `merge-executor` merges adversarial-debate artifacts, not git branches (`merge-executor.md:3`).
- `/sc:troubleshoot` dispatch contract (`refs/troubleshoot-dispatch.md`):
  - The seed is issue, scope and type (`:9-24`), built by `seed_troubleshoot` (`fsm.py:372-388`).
  - The route is `--fix` or `--depth deep --fix`, never `--depth quick --fix` (`:35-40`; `sc-troubleshoot-protocol/SKILL.md:180`).
  - Troubleshoot diagnoses but does not apply edits. pr-submit applies them in S3_FIXING (`:51-60`). This is the natural seam for semantic conflicts.
- Templates: `src/superclaude/templates/` holds only `documents/`, `workflow/` and `modularization-template-review/`. None is a resolution record or HALT template. HALT messages live inline in the SKILL text (`SKILL.md:268`, `:274`), where tests pin them verbatim.

## 8. Integration points and risks

- **Hook points**:
  - (a) Wave 0, after head binding on `--pr`. Today it only reports commits behind (`SKILL.md:267-268`). A GitHub conflict read could be added there or in the poll snapshot (`poll-augment-review.sh:38`). Add fields after `isCrossRepository`, because `test_static_grep.py:636` pins the substring `--json headRefName,headRefOid,isCrossRepository`.
  - (b) Before Wave 1, so reviewers review a conflict-free head.
  - (c) Wave 8. The base can move during the run, and CI may never start on a conflicted PR (**[external]**).
- **Must not change silently**:
  - no force push (`SKILL.md:305`);
  - the head-check, then parent-check, then `push_decision` order (`state-machine.md:173-179`);
  - the one-fix-commit rule;
  - the L0 AC-1 sentence (`test_static_grep.py:650-653`);
  - the `--repo` pin;
  - the single python block;
  - core purity.
- **Design choices required**:
  - Publishing a merge commit (parents `[pre_push_sha, origin/<base>]`) needs a new tested helper next to `push_parent_ok`, not a loosened one. It also needs a decision on whether a merge push and a fix push may share one cycle.
  - Is a conflict push counted in `push_count`, `round_counter` or the `applied_edits` predicate (`fsm.py:191-196`)?
  - The triad and recovery need a push-kind marker so Branch B re-drives the right commit.
  - The merge-in-progress commit cannot use `--only`.
  - L2 semantics need a rule.
  - The existing create-path rebase-vs-HALT contradiction (§3) should be settled at the same time.
