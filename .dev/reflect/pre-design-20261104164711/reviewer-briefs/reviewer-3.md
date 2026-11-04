# Reviewer 3 brief (refactorer) - sc:reflect UC-1, issue #305 plan

## T1 card excerpt

````yaml
structural_signals:
  S_scope: 20            # tasklist items
  S_domains: 3           # code (src/superclaude/pr_submit), tests, docs (SKILL/refs/command/CHANGELOG)
  S_dev_density: 0.0345  # union denominator

grounding:
  citations_total: 32
  citations_failed: 0
  citations_with_range_notes: 3   # models.py:23-33 (docstring ends :36), loop-guard.md:86-99 (list ends :103), test_ci_classify.py:20-70 (last test ends :72)

best_practice_grade: 4   # 0-5
best_practice_rationale:
  - "Grounded: every task names exact files, source sections and an observable acceptance criterion with a saved log (for example TL:45, TL:60, TL:82, TL:122)."
  - "Grounded: all 32 repo file:line citations in the tasklist resolve to the content the task describes (artifacts/grounding.yaml)."
  - "Grounded: parsed coverage is complete (574/574) and the out-of-scope items are declared (TL:30)."
  - "Grounded: the dependency graph has four missing edges (G2, G3, G4, G5) and one plan-level contradiction with the spec's run order (G1); these keep the grade at 4."
  - "[INFERRED] Task 4 and Task 8 are large (15 functions plus property tests; 13+ new recovery tests) and would be easier to verify split."

risks:
  - id: R1
    severity: medium
    claim: "An import-time failure in superclaude/pr_submit/__init__.py (Task 9 adds a conflicts import that itself imports fsm and models) would break the reflect contract-status CLI (src/superclaude/cli/reflect/commands.py:99) and go undetected by Task 20's subset run (TL:306)."
    tag: "Grounded (import site); [INFERRED] (failure mode)"
  - id: R2
    severity: medium
    claim: "A dependency-driven or parallel executor could run Task 13 before Task 10 (missing test file and make_repos), Task 15's record check before Task 4, and Task 20 before Tasks 6 and 9 (G2, G3, G5). /sc:implement walks tasks in file order, which hides these edges today."
    tag: "Grounded (edges); [INFERRED] (executor ordering)"
  - id: R3
    severity: low
    claim: "poll-ci-checks.sh:30 dies with 'missing required --pr <N>' before the gh/jq checks (:31-32). Task 13 says evidence mode needs no --pr (TL:217), but no acceptance criterion invokes C1-C4 without --pr (TL:220), so a half-done refactor that still passes --pr in the tests would not be caught."
    tag: Grounded
  - id: R4
    severity: low
    claim: "Resume-planner state dicts in Task 4 could drift from the Task 7 fold (G6). Task 8 partly mitigates this because its N1 and B2 tests feed a real RunLog into conflict_resume_plan (SRC:1340)."
    tag: Grounded
  - id: R5
    severity: low
    claim: "X1 depends on real offline 'uv lock' succeeding (SRC:129, verified by the design author for a zero-dependency pyproject). It skips only when uv is absent (TL:291), so a host whose uv cannot resolve offline would fail rather than skip; X2 (stub uv) still runs."
    tag: "[INFERRED]"
  - id: R6
    severity: low
    claim: "The force-push scan covers every .md and .sh in the skill folder (tests/pr_submit/test_static_grep.py:773-776). Every new ref and script (Tasks 10-16) is therefore in scope, and each of those tasks already runs test_static_grep.py (TL:192, TL:235, TL:246, TL:261). Residual risk is low."
    tag: Grounded

````

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-04T17:06:00Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-305-pr-submit-conflicts projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-305-pr-submit-conflicts

### .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:1-307

````markdown
---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-design-20261104-164423
version: "1"
priority: Medium
created_date: "2026-11-04"
---

# sc:pr-submit merge-conflict resolution release (issue #305)

Source: ./source.md
Goal: `/sc:pr-submit` detects merge conflicts on a PR, reports a tiered plan before any edit, regenerates a conflicted root `uv.lock` (Tier 1) and publishes it as one merge commit pushed fast-forward, halts on Tier 3, resolves text conflicts by stated intent only behind `--conflict-max-tier 2` (Tier 2, off by default), and no longer rebases or halts on the create path at L1+, all proven by hermetic real-git tests, with every existing push safeguard unchanged.

## Constraints

- The design in `./source.md` is the specification. Every section reference below (for example "source section 5.3") points into it. Where a task and the source disagree, the source wins; record the disagreement in the task's evidence.
- Never force-push, and never write a force flag after the words "git push" on any line of a `.md` or `.sh` file in `src/superclaude/skills/sc-pr-submit-protocol/` (the force-push scan in `tests/pr_submit/test_static_grep.py:758-776` covers every such file). The only push text is `git push origin <target_sha>:<HEAD_BRANCH>`; prohibitions are written in words.
- `push_parent_ok`, `evaluate_push_decision`, `push_fail_state`, `push_idempotency_key`, `needs_rebase` and every existing `transition()` edge in `src/superclaude/pr_submit/fsm.py` stay byte-identical (source section 6.1). `resolve_crash_window` in `recovery.py` keeps its signature and return value.
- T-N50: no `git` or `gh` token (regex `\bgh\b|\bgit\b`), docstrings and comments included, in `conflicts.py`, `fsm.py`, `ci.py`, `refs/state-machine.md`, `refs/loop-guard.md` and every other file in `CORE_PURE_FILES` (`tests/pr_submit/test_static_grep.py:37-51`).
- Installed primitives (`SKILL.md`, refs, scripts, `commands/pr-submit.md`) never name a `src/superclaude/` path in new text.
- Every `gh` call in new text carries `--repo "$REPO"` or a `repos/<owner/repo>/` path. Nothing contacts `SuperClaude-Org/SuperClaude_Framework`.
- Never stash, never use a hook-skipping flag, never amend, never stage everything; stage exact paths only.
- `SKILL.md` keeps exactly one python code block (`tests/pr_submit/test_cosmos_protocol.py:36`, `tests/pr_submit/test_codex_reviews.py:688`) and grows by at most 15 lines (source section 8.1).
- Edit `src/superclaude/`, then run `make sync-dev`; never stage `.claude/` paths except `.claude/settings.json`. `.dev/tasks/` is always staged (`git add .dev/tasks`), including this package and its `artifacts/`.
- Python through UV only (`uv run pytest ...`, `uv run python ...`). Run the tests each task names plus `tests/pr_submit/`, `tests/unit/test_cli_install.py` and `tests/commands/`; do not run the full suite (`make test`) or `tests/cli/eval/` as a directory (orchestrator brief; this overrides the `make test` step of source section 12.5).
- Real-git tests run only inside pytest temporary directories with a local bare repository as `origin`, a `gh` stub on `PATH`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`, and for real `uv` `UV_OFFLINE=1`, `UV_NO_CONFIG=1`, `UV_CACHE_DIR=<tmp>` (source section 12 preamble). No test touches the network or `~/.claude`.
- Out of scope: P3 late re-sync (#361) and the post-release verification follow-ups V1 to V8 of source section 14; they are not implemented by this plan.
- Task evidence (test logs, grep output) goes under `./artifacts/` in this package.

## Phase 1: Precursor and event enum

## Task 1: Stop the L1+ create path from rebasing or halting when behind base

Implement step 1 of source section 13 in `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` and `tests/pr_submit/test_static_grep.py`:

- Apply edit E2 (STOP block at `SKILL.md:220-223`), the rebase-sentence part only of edit E5 (the replacement substring of the Wave 0 bullet at `SKILL.md:267`, without the new operation-check sentence, which Task 17 adds), the first two replacement rows of edit E12 (Error Handling row at `SKILL.md:315`: "Wrong origin / wrong-owner URL" and "Behind base branch (create path at L1+, or `--pr`)"), and edit E13 (head-binding HALT message at `SKILL.md:268`), exactly as written in source section 8.1.
- Rewrite `tests/pr_submit/test_static_grep.py:654-661` exactly as source section 12.2 specifies (keep the asserts at `:656` and `:657` verbatim; replace `:658` and `:659-661`).

Acceptance criteria:
- `SKILL.md` contains "rebase if behind `origin/<base>` only at L0", "Being behind the base branch is not a STOP at L1+", "this skill never rewrites a published branch", and no longer contains "branch (`origin/<default-branch>`) on the create path" or "needs a force-push".
- The pinned fragments "rebase if behind `origin/<base>`" and "with `--pr <N>`, at any level, do not rebase" are still present verbatim; the AC-1 sentence of the Wave 0 bullet is unchanged.
- `uv run pytest tests/pr_submit/test_static_grep.py tests/pr_submit/test_edge_cases.py -q` passes; log saved to `./artifacts/t1-tests.log`.

## Task 2: Add the two conflict-cycle run-log events (41 to 43)

Implement step 2 of source section 13 per source sections 6.5 and 12.2:

- `src/superclaude/pr_submit/models.py`: add `SYNC_STARTED = "sync_started"` and `SYNC_CONCLUDED = "sync_concluded"` after `REVIEWER_INCOMPLETE` with the comment line from source section 6.5; update the module docstring (`:3-7`) and the class docstring (`:23-33`) from 41 to 43 members.
- `src/superclaude/pr_submit/run_log.py:111`: docstring "one of the 41 closed" becomes "one of the 43 closed".
- `src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md:86-99`: heading, "EXACTLY 43 members" sentence and the event list per source section 8.6 items 1 and 2 (token-free).
- `tests/pr_submit/test_run_log.py:165-169`: rename the test, update its docstring and both asserts to 43, add the two value asserts (source section 12.2).
- `tests/pr_submit/test_codex_reviews.py:441`: `== 41` becomes `== 43`.

Acceptance criteria:
- `len(EventType) == 43` and `EventType.SYNC_STARTED.value == "sync_started"`, `EventType.SYNC_CONCLUDED.value == "sync_concluded"`.
- `grep -rn '\b41\b' src/superclaude/pr_submit tests/pr_submit src/superclaude/skills/sc-pr-submit-protocol` shows no event-count hit (the PR-number literal in `test_run_log.py` `RunLog(41, ...)` excepted); output saved to `./artifacts/t2-grep.txt`.
- `uv run pytest tests/pr_submit/test_run_log.py tests/pr_submit/test_codex_reviews.py tests/pr_submit/test_static_grep.py -q` passes.

## Phase 2: Pure conflict core

## Task 3: Create `conflicts.py` with parsing, classification and planning

Depends on: Task 2

Create `src/superclaude/pr_submit/conflicts.py` per source sections 5.1, 5.2 and the parsing, classification and planning rows of 5.3, with the rules of source section 4.3:

- Module rules of source section 5.1 (standard library `base64`, `re`, `dataclasses`, `typing` only; internal imports `from .models import MonitorState` and `from .fsm import run_validation_gates`; never import `recovery`; no I/O; T-N50 clean; fail closed).
- Every constant and data type of source section 5.2 (including `REPORT_REASONS`, `HALT_REASONS`, the three `BRANCH_*` literals, `MechanicalRule`, `MECHANICAL_RULES`, `StageRecord`, `MergeTreeListing`, `ProbeResult`, `ConflictEntry`, `PathClass`, `ConflictPlan`, `ConflictAction`, `SyncDecision`, `ResumePlan` with `target_sha` and `hook`).
- Functions `mergeability_hint`, `needs_probe`, `parse_stage_records`, `parse_numstat_binary`, `parse_probe`, `group_entries`, `classify_path` (the 14-row first-match table of source section 4.3) and `conflict_plan` (the plan-tier table of source section 4.3; never takes the cap).
- Create the fixture `tests/pr_submit/fixtures/merge_tree_conflict.z` from a scratch repository under a temporary directory (one content conflict `f.txt` with stages 1/2/3, one modify/delete `d.txt` with stages 1/2), and put the capture recipe as a comment at the top of the test file.
- Create `tests/pr_submit/test_conflicts_core.py` with the Hint, Parse, Classify, Plan and Purity cases of source section 12.1.
- Append `PR_SUBMIT_PKG / "conflicts.py",` to `CORE_PURE_FILES` in `tests/pr_submit/test_static_grep.py:37-51` with the comment from source section 12.2.

Acceptance criteria:
- `parse_stage_records` on the fixture returns the exact records; every malformed shape listed in source section 12.1 raises `ValueError`.
- One parametrized test row per classification rule 0 to 13 passes, including the boundary rows of source section 12.1 (`pkg/uv.lock`, root `uv.lock` without `uv`, `uv.lock` with stages `"12"`, a path with a tab, `__snapshots__/x.snap`).
- Plan rows: 8 text paths give Tier 2, 9 give Tier 3 `too_many_files`; regen plus text is Tier 2; `probe_failed` and `merge_tree_unsupported` give tier `None`; a malformed probe gives Tier 3 `probe_malformed`.
- The AST purity test shows `conflicts.py` imports only the allowed modules; T-N50 and T-N41 in `test_static_grep.py` pass with `conflicts.py` in `CORE_PURE_FILES`.
- `uv run pytest tests/pr_submit/test_conflicts_core.py tests/pr_submit/test_static_grep.py -q` passes; log saved to `./artifacts/t3-tests.log`.

## Task 4: Add routing, gates, records, messages and resume planners to `conflicts.py`

Depends on: Task 3

Extend `src/superclaude/pr_submit/conflicts.py` with the remaining functions of source section 5.3 and their tests in `tests/pr_submit/test_conflicts_core.py`:

- `conflict_action` with the domain guard, the L0 row and every row of the `wave0`, `c_initial` and `wave8a` tables of source section 4.4 (including `tier1_l1_preserved` and `tier1_l2_preserved`).
- `merge_preflight_ok`, `merge_parent_ok`, `evaluate_sync_decision`, `sync_fail_state`, `conflict_validation_status`, `conflict_cycle_id`, `is_conflict_cycle`, `prior_conflict_cycles`, `finish_manifest`, `parse_resolution_record`, `resolution_record_ok`, `merge_commit_message`.
- `crash_resume_plan` (source section 4.8 second table, plus the `sync` / `ci` rules below it) and `conflict_resume_plan` (source section 4.8 first table in evaluation order: rows 1, 2, 3, 3b, 4c, 4, 4b, 4b', 5, 6, 7, 8, with the closing rule and the `prior_conflict_cycles` rule). Both are pure: they append nothing.
- Tests: the Router, Gates, Cycle ids, Record and message, and Resume cases of source section 12.1 (resume tests build `state` dicts directly; the run-log integration is Task 8). Include the ordinal-monotonicity property exactly as stated in source section 4.4, the `c_initial` default-row assertion, the Wave 8a Tier 1 preserved column, the `merge_parent_ok` matrix and the disjointness property with `fsm.push_parent_ok`, the `evaluate_sync_decision` truth tables and cross-gate property, the branch-literal equality with `recovery.BRANCH_A_LANDED` / `BRANCH_B_NOT_LANDED` / `BRANCH_C_AMBIGUOUS`, and `REPORT_REASONS & HALT_REASONS` equal to the eight-reason set of source section 5.2.

Acceptance criteria:
- Every reachable router row is asserted against a literal expected table; every domain violation returns `ConflictAction("halt", "router_unreachable", "terminal_halted", skip_ci=True)`.
- The monotonicity property passes over the full product of in-domain inputs for hooks `wave0` and `wave8a`.
- `merge_parent_ok` accepts only `[pre_push_sha, base_sha]` in that order with distinct 40-hex ids; `push_parent_ok` is false for every list `merge_parent_ok` accepts.
- `conflict_resume_plan` returns the source section 4.8 directive for each row, with `cycle_id`, `hook`, `review_terminal`, `target_sha` and `expect_checks` (true when missing) populated as specified; `prior_conflict_cycles(["sync-1"], "sync-1") == 0`.
- `uv run pytest tests/pr_submit/test_conflicts_core.py -q` passes; log saved to `./artifacts/t4-tests.log`.

## Phase 3: Changes to the existing core modules

## Task 5: Add the flag, `should_retrigger`, push-triad keywords and the P2 edge to `fsm.py`

Depends on: Task 4

Implement step 4 of source section 13 in `src/superclaude/pr_submit/fsm.py` per source section 6.1 items 1 to 8:

- `DEFAULT_CONFLICT_MAX_TIER = 1`; `SkillArgs.conflict_max_tier` appended last; `--conflict-max-tier` in `build_arg_parser` with `choices=[0, 1, 2]`; `parse_args` passes it through.
- `should_retrigger(applied_edits, push_kind=None)` after `push_fail_state`.
- `build_push_triad` keyword-only `push_kind`, `base_sha`, `review_terminal`, `expect_checks` (defaults `None`; byte-identical output when all are `None`; `ValueError` on an unknown `push_kind`; predicates from `decision.audit_predicates` for a non-`PushDecision`).
- The `(S2_CLASSIFY, "conflicting")` edge right after the `findings` edge; the `fsm.py:1137` condition becomes `should_retrigger(result.applied_edits)`.
- Tests per source section 12.2: `test_conflict_max_tier_default_and_bounds` in `tests/pr_submit/test_skill_parse.py`; `test_transition_conflicting_edge` in `tests/pr_submit/test_autonomy_gates.py`; `test_should_retrigger_zero_edit_pair` in `tests/pr_submit/test_loop_guard.py`; the Triad cases of source section 12.1 in `tests/pr_submit/test_conflicts_core.py` (the default call equals a literal three-record list captured from the current `build_push_triad` before editing it).

Acceptance criteria:
- `parse_args([]).conflict_max_tier == 1`; `--conflict-max-tier 3` and `x` raise `SystemExit`.
- `transition(S2_CLASSIFY, "conflicting")` gives `S3_FIXING` at L3 with budget, `HALT_MAX_ROUNDS` on a spent budget, `PROPOSED` at L1, `HALT_HUMAN` with `needs_human_decision`; `(S2_CLASSIFY, "findings")` still gives `S2B_VERIFY`.
- `should_retrigger(0, "merge")` is true and false for `fix`, `None`, `sync`, `ci`; `run_skill` zero-edit rows keep `rereview_request_count == 0`.
- The default `build_push_triad` call equals the recorded pre-change output; a `sync` call adds `kind`, `base_sha`, `review_terminal` and `expect_checks` where source section 6.1 says.
- `git diff` of `fsm.py` shows no change inside `evaluate_push_decision`, `push_fail_state`, `push_idempotency_key`, `push_parent_ok` or `needs_rebase`; T-N50 passes.
- `uv run pytest tests/pr_submit -q` passes; log saved to `./artifacts/t5-tests.log`.

## Task 6: Add `expect_checks` to CI classification in `ci.py`

Implement step 5 of source section 13 in `src/superclaude/pr_submit/ci.py` per source section 6.2:

- `classify_checks(payload, *, wait_sha=None, expect_checks=False)`: unchanged body when false; when true a non-dict payload and an empty or missing chosen list return `polling`.
- `expect_checks_after_push(*, checks_seen_this_run, pre_push_evidence, base_evidence)` with the fail-closed rule of source section 6.2 item 2; module docstring sentence, token-free.
- Tests in `tests/pr_submit/test_ci_classify.py`: every new function listed in source section 12.2; existing tests at `:20-70` unmodified.

Acceptance criteria:
- Empty list with `expect_checks=True` and a matching head is `polling`; a nonempty all-pass list is `clean`; `expect_checks=False` keeps empty as `clean`; head mismatch is `polling`; non-dict payload with `expect_checks=True` is `polling`.
- `expect_checks_after_push` is false only when `checks_seen_this_run` is false and both evidence values are 0; `-1` and `None` give true.
- `uv run pytest tests/pr_submit/test_ci_classify.py tests/pr_submit/test_static_grep.py -q` passes; log saved to `./artifacts/t6-tests.log`.

## Task 7: Make the run-log fold kind-aware and conflict-cycle aware in `run_log.py`

Depends on: Task 2

Implement step 6 of source section 13 in `src/superclaude/pr_submit/run_log.py` `rebuild_state` per source section 6.3 items 1 to 6:

- New state keys `sync_push_count`, `conflict_cycles`, `open_conflict_cycle`, `push_rejected`; fold branches for `sync_started`, `sync_concluded`, `push_initiated` (open-cycle flags, `target_sha`, `expect_checks` stored as `True` when missing or non-bool, `superseded` for other open cycles), the kind-aware `push_completed`, and `push_aborted_or_not_landed` with `rejected is True`; `IDEMPOTENCY_SETS` unchanged; docstring updated.
- Tests in `tests/pr_submit/test_run_log.py`: every new function listed for that file in source section 12.2, including the recorded legacy-log fixture test and the redaction test.

Acceptance criteria:
- A legacy log without `kind` or conflict events rebuilds with every pre-existing key equal and the new keys at their defaults.
- A `sync` push increments `sync_push_count` and not `push_count`; `fix`, `ci`, `merge` and kind-less pushes increment `push_count`.
- `conflict_cycles` keeps first-seen order and counts a resume restart's reused id once; `open_conflict_cycle` carries `hook` and `review_terminal`; a later push of another cycle marks the open cycle `superseded`.
- `len(IDEMPOTENCY_SETS) == 7` (`tests/pr_submit/test_idempotency.py:89`) still passes.
- `uv run pytest tests/pr_submit/test_run_log.py tests/pr_submit/test_idempotency.py -q` passes; log saved to `./artifacts/t7-tests.log`.

## Task 8: Add kind-aware crash recovery to `recovery.py`

Depends on: Task 4, Task 7

Implement step 7 of source section 13 in `src/superclaude/pr_submit/recovery.py` per source section 6.4:

- Add `"kind"` and `"base_sha"` to the copied key tuple (`:98-110`), copied only when present.
- Add `resolve_crash_window_plan(run_log, dangling, *, remote_reachable, observed_remote_sha=None)` exactly as in source section 6.4 item 2, so Branch A and C and halt directives close an open conflict cycle once with `sync_concluded{recovered: true}`; Branch B leaves closing to the SKILL; module docstring paragraph, token-free.
- Tests in `tests/pr_submit/test_crash_recovery.py`: every new function listed for that file in source section 12.2 (by-kind parametrization, recovered record copies, legacy byte-equality, rejected-push record, cycle closing, conflict crash then fix crash, restart row with recorded `review_terminal`, both N1 re-drive tests, row 1 closing, row 4 `expect_checks` default, Branch B landed close, Branch C event order).

Acceptance criteria:
- For kinds `fix` and absent, the returned plan and the appended events are byte-equal to today's `resolve_crash_window` behaviour; existing tests in `test_crash_recovery.py`, `test_augment_review_remediation.py:145` and `test_codex_reviews.py:489` pass unmodified.
- `sync` and `ci` never resume into `S4_PUSHING`, S5a or S5; a second wrapper call appends nothing.
- After a recovered conflict crash, a later fix-push crash window is returned by `detect_crash_window` and `conflict_resume_plan` returns `none`.
- `uv run pytest tests/pr_submit/test_crash_recovery.py tests/pr_submit/test_augment_review_remediation.py tests/pr_submit/test_codex_reviews.py -q` passes; log saved to `./artifacts/t8-tests.log`.

## Task 9: Export the conflict core from the package

Depends on: Task 5, Task 6

Edit `src/superclaude/pr_submit/__init__.py` per source section 6.6: the docstring clause naming `conflicts`, the `from .conflicts import (...)` block with every listed name, `should_retrigger` added to the existing `fsm` import, and an `__all__` group `# merge conflicts (issue #305)` with the same names. `ci.py` exports are not changed by this task.

Acceptance criteria:
- `uv run python -c "from superclaude.pr_submit import conflict_action, should_retrigger, merge_parent_ok, prior_conflict_cycles"` exits 0.
- Every name in the new `__all__` group resolves; no import cycle (`conflicts` imports `fsm` and `models`; `fsm`, `models`, `run_log`, `ci` never import `conflicts`).
- `uv run pytest tests/pr_submit -q` passes; log saved to `./artifacts/t9-tests.log`.

## Phase 4: Scripts

## Task 10: Create the read-only probe `probe-merge.sh`

Depends on: Task 3

Create `src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh` (git mode 100755) per the script rules at the top of source section 7 and source section 7.1 (both modes, all 14 full-mode steps, base64 transport, the JSON contract and the `PROBE_FAIL` reasons). Create `tests/pr_submit/test_conflict_scripts.py` with the `make_repos(tmp_path)` fixture helper of source section 12.4 and cases P1 to P12, parsing probe output with `conflicts.parse_probe` / `conflict_plan`, and a module-level capability skip unless `git merge-tree --write-tree HEAD HEAD` works in a scratch repository.

Acceptance criteria:
- P1 to P12 of source section 12.4 pass; P8 proves `git status --porcelain=v1 -z` and `HEAD` are unchanged by the probe.
- `--repo` not matching origin gives exit 2 and `PROBE_FAIL origin_mismatch` with no fetch.
- The script has no `git push` line, no stash, no config write, no hook-skipping flag and no `src/superclaude/` text; `git ls-files -s` shows mode 100755.
- `uv run pytest tests/pr_submit/test_conflict_scripts.py tests/pr_submit/test_static_grep.py -q` passes; log saved to `./artifacts/t10-tests.log`.

## Task 11: Create the finish gate `finish-merge.sh`

Depends on: Task 10

Create `src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh` (mode 100755) per source section 7.2: precheck mode (`--base-sha` only; any commit-mode option is `FINISH_FAIL usage`) and commit mode with all nine steps in order (merge ownership, unmerged, tree, introduced markers, staged-set equality with the merge-tree blob, `git commit -F` with hooks on, exact parents, clean after, JSON output). Add cases F1 to F12 of source section 12.4 to `tests/pr_submit/test_conflict_scripts.py`.

Acceptance criteria:
- F1 to F12 pass, including F9 (failing `pre-commit` hook: `FINISH_FAIL hook_rejected`, hook output verbatim on stderr, no commit, `MERGE_HEAD` still present) and F10 (exactly two parents `[old HEAD, base_sha]` and `merge_parent_ok` true).
- The script commits only through one `git commit -F`; it contains no push, stash, amend, hook-skipping flag or `src/superclaude/` text.
- `uv run pytest tests/pr_submit/test_conflict_scripts.py -q` passes; log saved to `./artifacts/t11-tests.log`.

## Task 12: Create the Tier 2 evidence collector `collect-conflict-evidence.sh`

Depends on: Task 10

Create `src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh` (mode 100755) per source section 7.3 (ownership check, empty `--out`, the seven evidence files with the truncation marker, 60 s bound, JSON output, `EVIDENCE_FAIL` reasons). Add cases E1 to E4 of source section 12.4 to `tests/pr_submit/test_conflict_scripts.py`.

Acceptance criteria:
- E1 writes exactly `stage1`, `stage2`, `stage3`, `worktree`, `log.txt`, `diff-ours.txt`, `diff-theirs.txt`; E2 lists the missing stage; E3 writes the truncation marker and `truncated: true`; E4 gives `EVIDENCE_FAIL out_not_empty` and writes nothing.
- `uv run pytest tests/pr_submit/test_conflict_scripts.py -q` passes; log saved to `./artifacts/t12-tests.log`.

## Task 13: Add commit-scoped check evidence to `poll-ci-checks.sh`

Edit `src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh` per source section 7.4: accept `--evidence-sha <40hex>` (no `--pr` needed), validate it before the `gh pr checks --help` probe, read `gh api "repos/${REPO}/commits/${SHA}/check-runs?per_page=1" --jq .total_count` and the `/status` count, print `{"evidence_sha": ..., "evidence_checks": <n>, "source": "ci"}` with `n = -1` on any failed or unparsable read; extend the header comment; leave the existing poll path and the pre-existing header line `:14` unchanged. Add cases C1 to C4 of source section 12.4 to `tests/pr_submit/test_conflict_scripts.py` with a `gh` stub.

Acceptance criteria:
- C1 gives `evidence_checks: 2`, C2 gives 0, C3 gives -1, C4 exits 2; no `gh pr checks` call is made in evidence mode.
- Existing poll tests (`tests/pr_submit/test_cosmos_poll.py` and the CI poll cases in `tests/pr_submit/test_static_grep.py`) pass unmodified.
- `uv run pytest tests/pr_submit/test_conflict_scripts.py tests/pr_submit/test_cosmos_poll.py tests/pr_submit/test_static_grep.py -q` passes; log saved to `./artifacts/t13-tests.log`.

## Phase 5: Refs, skill and command text

## Task 14: Write `refs/conflict-mechanical.md`

Depends on: Task 11, Task 12, Task 13

Create `src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md` with the thirteen sections of source section 8.2, carrying the normative order of source section 4.6 (steps 0 to 13), the resume rules of source section 4.8 and the halt reasons and messages of source section 9. Fenced code uses `bash` or `text` only; every command line matches the scripts of Tasks 10 to 13; every pinned phrase and order pin listed at the end of source section 8.2 appears.

Acceptance criteria:
- Every pinned phrase of source section 8.2 is present verbatim, and the order pins hold (head check and `merge_preflight_ok` before `sync_started`, before the merge command; head re-read before `merge_parent_ok`, before `--is-ancestor`, before "The deterministic core DECIDES", before the push line).
- Every `git push` line is exactly `git push origin <target_sha>:<HEAD_BRANCH>`; every `gh` line is repo-scoped; no `src/superclaude/` text; no force flag.
- `uv run pytest tests/pr_submit/test_static_grep.py -q` passes (force-push scan included); log saved to `./artifacts/t14-tests.log`.

## Task 15: Write `refs/conflict-intent.md`

Depends on: Task 12

Create `src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md` with the ten sections of source section 8.3 (scope, evidence one file at a time, high-suspicion checklist, kind rules, intent rules, the resolution-record format matching `parse_resolution_record` / `resolution_record_ok` from Task 4, the `evidence-validator` grounding check with one revision pass, the commit message, after the merge push with configured reviewers, findings after a merge with `base_authored`).

Acceptance criteria:
- Every pinned phrase listed at the end of source section 8.3 is present, and the record field names appear in the order `kind`, `root_cause`, `ours_intent`, `theirs_intent`, `resolution`, `behavior_after`, `dropped`, `evidence`.
- A sample `resolution.md` written in the format the ref describes parses with `parse_resolution_record` and passes `resolution_record_ok` (checked in a scratch test or script run; output saved to `./artifacts/t15-record-check.txt`).
- No `src/superclaude/` text, no force flag, every `gh` line repo-scoped; `uv run pytest tests/pr_submit/test_static_grep.py -q` passes.

## Task 16: Update `state-machine.md`, `ci-poll.md` and `loop-guard.md`

Depends on: Task 2

Edit three existing refs under `src/superclaude/skills/sc-pr-submit-protocol/refs/`:

- `state-machine.md`: the wait-only sentence at `:144-146` and the new section 5.2d inserted after 5.2c, exactly as in source section 8.4 (token-free; the INV-016 blockquote at `:161-179` untouched).
- `ci-poll.md`: items 1 to 4 of source section 8.5 (the `:21` sentence, the Wave 8 entry table cells at `:28-29`, the `pr_conflicting` sentence, the new "Expected checks after a push" section).
- `loop-guard.md`: item 3 of source section 8.6 (the reserved cycle-id prefix sentence in the run-log schema section; items 1 and 2 were done in Task 2).

Acceptance criteria:
- T-N50 passes for `state-machine.md` and `loop-guard.md`; the pins at `tests/pr_submit/test_static_grep.py:746-750` pass unmodified.
- Both new `gh api` lines in `ci-poll.md` carry a `repos/<owner/repo>/` path.
- `uv run pytest tests/pr_submit/test_static_grep.py -q` passes; log saved to `./artifacts/t16-tests.log`.

## Task 17: Finish the `SKILL.md` and command edits

Depends on: Task 1, Task 14, Task 15, Task 16

Apply the remaining edits of source section 8.1 to `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md`: E1, E3, E4, the operation-check sentence of E5, E6, E7, E8, E9 (substring replacements a to e), E10, E11, and the last three rows of E12. Apply source section 8.7 items 1 to 4 to `src/superclaude/commands/pr-submit.md` (argument hint, options row, activation context, Will Not text; `version: "1.0"` not bumped).

Acceptance criteria:
- `SKILL.md` has exactly one python code block and its line count grew by at most 15 against `master` (`git diff --stat` saved to `./artifacts/t17-diffstat.txt`).
- The pinned substrings named in source section 8.1 (E8 note, E9 note, the force-push bullet at `SKILL.md:305`) and the command clause pinned at `tests/pr_submit/test_static_grep.py:755` are unchanged.
- No `src/superclaude/` text or force flag in the new text; every new `gh` line is repo-scoped.
- `uv run pytest tests/pr_submit -q` passes; log saved to `./artifacts/t17-tests.log`.

## Phase 6: Protocol tests, end-to-end tests and release notes

## Task 18: Add the static protocol and install tests

Depends on: Task 17

Create `tests/pr_submit/test_conflict_sync_protocol.py` with every case listed for it in source section 12.1 (pinned phrases and order pins of sections 8.2 and 8.3, edits E1 to E13 present, one python block, Tier 2 labelling, the evidence script named only in `conflict-intent.md`, repo-scoped `gh` lines, exact `git push` form, the FR-21 prohibited-operation regex scan, no `src/superclaude` text, the allowed-tools test, the static call ceilings) and the byte-identical fragment regression test of source section 12.2 (last paragraph). Add `test_wait_only_sentences_name_the_one_sync_exception` and `test_s5a_retrigger_widened_for_merge_cycles_only` to `tests/pr_submit/test_static_grep.py`, `test_push_parent_ok_still_rejects_a_valid_merge_commit` to `tests/pr_submit/test_pre_pr_checks.py`, and the five new installed file names to the expected list in `tests/unit/test_cli_install.py:248-262`.

Acceptance criteria:
- `uv run pytest tests/pr_submit/test_conflict_sync_protocol.py tests/pr_submit/test_static_grep.py tests/pr_submit/test_pre_pr_checks.py tests/unit/test_cli_install.py -q` passes; log saved to `./artifacts/t18-tests.log`.
- The prohibited-operation scan fails when a forbidden command is added to a scratch copy of a new ref (demonstrated once and recorded in `./artifacts/t18-negative-check.txt`).

## Task 19: Add the end-to-end conflict scenarios

Depends on: Task 5, Task 8, Task 11, Task 12

Create `tests/pr_submit/test_conflict_e2e.py` with cases X1, X2 and X3 of source section 12.4, reusing `make_repos` from `tests/pr_submit/test_conflict_scripts.py`: X1 Tier 1 with real `uv` (skip only when `uv` is absent), X2 Tier 1 with a stub `uv`, X3 Tier 2 with a scripted resolution, including the rejected `semantic` variant.

Acceptance criteria:
- X1 and X2: the bare origin's branch tip equals `merge_sha`, parents `[pr_head, base_sha]`, `uv lock --check` passes on the pushed tree, `rebuild_state()` gives `push_count == 0`, `sync_push_count == 1`, `conflict_cycles == ["sync-1"]`, `round_counter == 0`, `open_conflict_cycle is None`, and the `gh` stub saw no re-trigger call.
- X3: FSM states in order `S3_FIXING`, `S7_VALIDATING`, `S4_PUSHING`, `S6_REPLYING`, `RESOLVING`, `S5A_RETRIGGER_REVIEW`; `push_count == 1`, `sync_push_count == 0`; the commit body lists both files with `kind`, `resolution`, `dropped` and no file content; the `semantic` variant is rejected before any commit.
- `uv run pytest tests/pr_submit/test_conflict_e2e.py -q` passes with X2 always run; log saved to `./artifacts/t19-tests.log`.

## Task 20: Add the CHANGELOG entry and sync the dev copies

Depends on: Task 18, Task 19

Insert the entry of source section 15 under `## [Unreleased]` in `CHANGELOG.md` (no package version bump, per the version note in source section 15). Run `make sync-dev` so `.claude/` mirrors the edited skill, refs, scripts and command (do not stage `.claude/`).

Acceptance criteria:
- `CHANGELOG.md` contains "### sc:pr-submit: merge-conflict detection and resolution (#305)" under `## [Unreleased]`; `pyproject.toml` version is unchanged.
- `make verify-sync` passes; `make lint` passes; `uv run ruff format --check src/ tests/` passes; `uv run pytest tests/pr_submit tests/unit/test_cli_install.py tests/commands -q` passes; outputs saved to `./artifacts/t20-checks.log`.
- `git status --porcelain` lists no staged `.claude/` path other than `.claude/settings.json`.
````

### .dev/reflect/pre-design-20261104164711/artifacts/grounding.yaml:1-167

````yaml
# sc:reflect UC-1 Wave 1A grounding: every repo file:line the TASKLIST cites, re-Read this run.
# Tasklist: .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md
# Worktree: /home/coder/workspaces/worktrees/IronClaude/issue-305-pr-submit-conflicts (HEAD 119622e3, tracked tree clean)
schema: reflect-grounding/1
mode: UC-1
wave: 1A
status: complete
citation_budget_policy: full_reread
citations_total: 32
citations_verified: 32
citations_failed: 0
citations_with_range_notes: 3
evidence_chain_note: "Floor chain used (Read + Grep). Each cited range was Read with offset/limit in this run; no cited file was modified during the run."
citations:
  # ---------------- Constraints block
  - citation: tests/pr_submit/test_static_grep.py:758-776
    cited_by: Constraints (line 20); C1
    verified: true
    note: "test_skill_forbids_force_push: regex \\bgit push\\b[^`\\n]*?(\\s--force\\b|\\s-f\\b|\\s\\+\\S) scanned over every .md/.sh under SKILL_DIR (rglob at :773-776)."
  - citation: tests/pr_submit/test_static_grep.py:37-51
    cited_by: Constraints (line 22); Task 3
    verified: true
    note: "CORE_PURE_FILES list: state-machine.md, severity-routing.md, loop-guard.md, auggie-fallback.md, fsm.py, severity_router.py, loop_guard.py, ci.py. Task 3 appends conflicts.py here."
  - citation: tests/pr_submit/test_cosmos_protocol.py:36
    cited_by: Constraints (line 26)
    verified: true
    note: "assert len(blocks) == 1, 'keep one executable snapshot gate, not parallel parsers'"
  - citation: tests/pr_submit/test_codex_reviews.py:688
    cited_by: Constraints (line 26)
    verified: true
    note: "assert len(blocks) == 1, 'keep one executable snapshot gate'"
  # ---------------- Task 1
  - citation: src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:220-223
    cited_by: Task 1 (E2)
    verified: true
    note: "STOP block; :221-222 holds 'a branch behind the base branch (`origin/<default-branch>`) on the create path'. Four lines, matching E2's four-for-four replacement."
  - citation: src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:267
    cited_by: Task 1 (E5 rebase sentence); Task 17 (E5 operation check)
    verified: true
    note: "Wave 0 bullet holds the exact E5 old substring 'and rebase if behind `origin/<base>` (with `--pr <N>`, at any level, do not rebase: ... instead).' and the AC-1 sentence at its end."
  - citation: src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:315
    cited_by: Task 1 (E12 rows 1-2)
    verified: true
    note: "'| Wrong origin / behind base branch (create path) / wrong-owner URL | HALT; instruct operator to close the misrouted PR (FM-11). |'"
  - citation: src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:268
    cited_by: Task 1 (E13)
    verified: true
    note: "Head-binding bullet holds the exact E13 old substring '(push if you are ahead; a branch Wave 0 rebased needs a force-push, which this skill never does for you; `git pull --ff-only` if you are behind)'."
  - citation: tests/pr_submit/test_static_grep.py:654-661
    cited_by: Task 1
    verified: true
    note: ":654-655 comment; :656 '--pr' pin and :657 rebase pin (kept verbatim); :658 create-path pin; :659-661 Error Handling row pin (replaced)."
  # ---------------- Task 2
  - citation: src/superclaude/pr_submit/models.py:3-7
    cited_by: Task 2
    verified: true
    note: "Module docstring 'exactly 41 members ... reviewer_absent and reviewer_incomplete'."
  - citation: src/superclaude/pr_submit/models.py:23-33
    cited_by: Task 2
    verified: true
    range_note: "The EventType docstring runs to :36 (closing quotes); the count text sits in :23-33 as cited."
    note: "'Closed enum of run-log event types — EXACTLY 41 members.' at :23."
  - citation: src/superclaude/pr_submit/models.py:90
    cited_by: Task 2 ('after REVIEWER_INCOMPLETE')
    verified: true
    note: "REVIEWER_INCOMPLETE = 'reviewer_incomplete' is the last enum member (:89-90; comment 'the 40th-41st' at :88)."
  - citation: src/superclaude/pr_submit/run_log.py:111
    cited_by: Task 2
    verified: true
    note: "'Raises :class:`ValueError` if ``event_type`` is not one of the 41 closed'."
  - citation: src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md:86-99
    cited_by: Task 2
    verified: true
    range_note: "Heading :86 and the 'EXACTLY 41 members' sentence :88 are in range, but the event list ends at :103 ('`reviewer_incomplete`.'), where 8.6 item 2 appends the two names. The cited range stops 4 lines short of the edit point."
    note: "Heading 'The 41 event types (§11.3 + §12.1 + V1.1 §6.1 + silence + reviewers)'."
  - citation: tests/pr_submit/test_run_log.py:165-169
    cited_by: Task 2
    verified: true
    note: "test_eventtype_is_41_members_with_silence_and_reviewer_events; docstring :166-167; asserts == 41 at :168 and :169."
  - citation: tests/pr_submit/test_run_log.py:204
    cited_by: Task 2 AC ('RunLog(41, ...)' exception)
    verified: true
    note: "rl = RunLog(41, tmp_path), a PR number, not an event count. The QA-6 grep also hits fixture JSON line numbers (finding-max.json:405,416; codex-findings-pr336.json:438,449,534,545,825,828), which are not event counts either; the AC names only the RunLog exception."
  - citation: tests/pr_submit/test_codex_reviews.py:441
    cited_by: Task 2
    verified: true
    note: "assert len(EventType) == 41"
  # ---------------- Task 5
  - citation: src/superclaude/pr_submit/fsm.py:1137
    cited_by: Task 5
    verified: true
    note: "'if result.applied_edits > 0:' inside run_skill's S5a block (:1133-1139)."
  # ---------------- Task 6
  - citation: tests/pr_submit/test_ci_classify.py:20-70
    cited_by: Task 6
    verified: true
    range_note: "The last existing test in the region, test_classify_required_fallback, spans :64-72; ':20-70' cuts its body. Read as 'the existing tests at the top of the file'."
    note: "Includes the empty-is-clean pins test_classify_empty (:36-38) and test_classify_empty_polling_is_not_clean (:41-42) that expect_checks=False must keep."
  # ---------------- Task 7
  - citation: tests/pr_submit/test_idempotency.py:89
    cited_by: Task 7
    verified: true
    note: "assert len(IDEMPOTENCY_SETS) == 7"
  # ---------------- Task 8
  - citation: src/superclaude/pr_submit/recovery.py:98-110
    cited_by: Task 8
    verified: true
    note: "common = {k: dangling[k] for k in (run_id, cycle_id, idempotency_key, pre_push_sha, target_sha, target_branch, target_remote) if k in dangling}. Branch literals at :28-30; Branch C append at :161-171."
  - citation: tests/pr_submit/test_augment_review_remediation.py:145
    cited_by: Task 8
    verified: true
    note: "branch, resume_state = resolve_crash_window(rl, dangling, remote_reachable=True)"
  - citation: tests/pr_submit/test_codex_reviews.py:489
    cited_by: Task 8
    verified: true
    note: "branch, resume_state = resolve_crash_window(rl, dangling, remote_reachable=True)"
  # ---------------- Task 13
  - citation: src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh:14
    cited_by: Task 13; C7
    verified: true
    note: "'# Source of truth lives in src/superclaude/; do not edit the .claude/ mirror.' (pre-existing). Adjacent fact relevant to Task 13: :30 enforces '--pr' BEFORE the gh/jq checks (:31-32) and REPO resolution (:34-36), so evidence mode must bypass :30; the --help probe is at :39-43; the script uses blanket 'set -euo pipefail' at :16."
  # ---------------- Task 16
  - citation: src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md:144-146
    cited_by: Task 16 (8.4 item 1)
    verified: true
    note: "Hard-wrapped 'A spent round budget and a silence terminal permit **waiting only**: CI findings are `REPORT_ONLY`, never an additional fix or push.' across :144-146. Section 5.2c at :140; '## 5.3' at :159 (the 5.2d insertion point)."
  - citation: src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md:161-179
    cited_by: Task 16
    verified: true
    note: "INV-016 blockquote; holds 'exactly one parent, that same SHA' (:174) and 'The parent check applies only when the cycle applied edits' (:177-178)."
  - citation: src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md:21
    cited_by: Task 16 (8.5 item 1)
    verified: true
    note: "'only two parsed empty arrays justify `clean`.'"
  - citation: src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md:28-29
    cited_by: Task 16 (8.5 item 2)
    verified: true
    note: "HALT_MAX_ROUNDS row ends 'No: CI findings → `REPORT_ONLY`'; TERMINAL_AUGMENT_NO_RESPONSE row ends '| No |'."
  - citation: tests/pr_submit/test_static_grep.py:746-750
    cited_by: Task 16
    verified: true
    note: "Prose-join of state-machine.md and the two pins ('exactly one parent, that same SHA'; 'The parent check applies only when the cycle applied edits')."
  # ---------------- Task 17
  - citation: src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:305
    cited_by: Task 17
    verified: true
    note: "'Force-push (`--force`, `--force-with-lease`, or a `+` refspec): ...' Will Not bullet, pinned at test_static_grep.py:761."
  - citation: tests/pr_submit/test_static_grep.py:755
    cited_by: Task 17
    verified: true
    note: "assert \"push any commit besides the cycle's one fix commit\" in will_not (pr-submit.md Will Not section)."
  # ---------------- Task 18
  - citation: tests/unit/test_cli_install.py:248-262
    cited_by: Task 18
    verified: true
    note: "Whitespace-separated expected list; sc-pr-submit-protocol entries run from the end of :248 (SKILL.md) to the start of :262 (retrigger-review.sh). The five new names (2 refs, 3 scripts) go into this block in sorted position."
supporting_facts_checked:
  - fact: "fsm.py defines DEFAULT_MAX_ROUNDS (:32), gate_edit (:147), should_halt_rounds (:152), build_push_triad (:238), run_validation_gates (:453), push_parent_ok (:582), needs_rebase (:603), transition (:716) and the findings edge (:741)."
    used_by: "Tasks 3, 4, 5 (imports and edge placement)"
  - fact: "test_static_grep.py defines _command_lines (:67) and _repo_scoped (:103), which source 12.1 reuses for the new protocol test."
    used_by: "Task 18"
  - fact: "ci.py classify_checks signature at :22 is (payload, *, wait_sha=None); ci.py imports only re, .classifier and .models."
    used_by: "Task 6"
  - fact: "src/superclaude/cli/reflect/commands.py:99 imports superclaude.pr_submit.contract_setup, which runs superclaude/pr_submit/__init__.py (edited by Task 9). tests/cli/reflect/test_contract_status_cli.py exercises it and is outside Task 20's test subset."
    used_by: "Gap G1 / Risk R1"
side_effects:
  - "Running 'uv run python' created .venv/ in the worktree (gitignored at .gitignore:56). No tracked file changed; 'git status --porcelain' shows only the pre-existing untracked .dev/ folders."
````

## Coverage slice

Matrix summary (verbatim):

````yaml
parsed_count: 574
inferred_count: 34
parsed_matched: 574
inferred_matched: 13
coverage_pct: 1.0
coverage_pct_union: 0.9655
unmapped_requirements: []
unmapped_requirements_union:
- INF-001
- INF-002
- INF-003
- INF-006
- INF-007
- INF-008
- INF-009
- INF-012
- INF-013
- INF-014
- INF-015
- INF-016
- INF-021
- INF-022
- INF-024
- INF-025
- INF-026
- INF-029
- INF-031
- INF-032
- INF-034
unmapped_count_parsed: 0
unmapped_count_union: 21
coverage_degraded: null
coverage_undefined: false
S_dev_density: 0.0345
partial_mappings:
- 6.5-site-1
- 6.5-site-2
- sec-8
- sec-12
- sec-12.5
- 13-step-14
out_of_scope_count: 15
out_of_scope_ids:
- OOS-P3-#361
- FR-25
- 2.1-out-live-gates
- 2.1-out-default-flip
- V1
- V2
- V3
- V4
- V5
- V6
- V7
- V8
- 11-8-R-19
- 11-9-R-20
- 11-31-R-161
inferred_dropped_count: 0
telemetry_literal_reference_rows: 352
telemetry_literal_reference_pct: 0.6132
anchor_validation_problems: []
````

| Requirement | Source | Mapped tasks | Status | Grounding |
|---|---|---|---|---|
| E1 | parsed | Task 17 | mapped | source.md:869-873 |
| E2 | parsed | Task 1 | mapped | source.md:875-882 |
| E3 | parsed | Task 17 | mapped | source.md:884-891 |
| E4 | parsed | Task 17 | mapped | source.md:893-899 |
| E5 | parsed | Task 1, Task 17 | mapped | source.md:901-909 |
| E6 | parsed | Task 17 | mapped | source.md:911-915 |
| E7 | parsed | Task 17 | mapped | source.md:917-919 |
| E8 | parsed | Task 17 | mapped | source.md:921-929 |
| E9 | parsed | Task 17 | mapped | source.md:931-941 |
| E10 | parsed | Task 17 | mapped | source.md:943-947 |
| E11 | parsed | Task 17 | mapped | source.md:949-959 |
| E12 | parsed | Task 1, Task 17 | mapped | source.md:961-969 |
| E13 | parsed | Task 1 | mapped | source.md:971-979 |
| 12.1-row-1 | parsed | Task 3, Task 4, Task 5 | mapped | source.md:1322 |
| 12.1-row-2 | parsed | Task 3 | mapped | source.md:1323 |
| 12.1-row-3 | parsed | Task 18 | mapped | source.md:1324 |
| 12.1-row-4 | parsed | Task 10, Task 11, Task 12, Task 13 | mapped | source.md:1325 |
| 12.1-row-5 | parsed | Task 19 | mapped | source.md:1326 |
| 12.2-row-1 | parsed | Task 2 | mapped | source.md:1332 |
| 12.2-row-2 | parsed | Task 2 | mapped | source.md:1333 |
| 12.2-row-3 | parsed | Task 7 | mapped | source.md:1334 |
| 12.2-row-4 | parsed | Task 2 | mapped | source.md:1335 |
| 12.2-row-5 | parsed | Task 3 | mapped | source.md:1336 |
| 12.2-row-6 | parsed | Task 1 | mapped | source.md:1337 |
| 12.2-row-7 | parsed | Task 18 | mapped | source.md:1338 |
| 12.2-row-8 | parsed | Task 18 | mapped | source.md:1339 |
| 12.2-row-9 | parsed | Task 8 | mapped | source.md:1340 |
| 12.2-row-10 | parsed | Task 5 | mapped | source.md:1341 |
| 12.2-row-11 | parsed | Task 5 | mapped | source.md:1342 |
| 12.2-row-12 | parsed | Task 5 | mapped | source.md:1343 |
| 12.2-row-13 | parsed | Task 6 | mapped | source.md:1344 |
| 12.2-row-14 | parsed | Task 18 | mapped | source.md:1345 |
| 12.2-row-15 | parsed | Task 18 | mapped | source.md:1346 |
| 12.4-P1 | parsed | Task 10 | mapped | source.md:1362 |
| 12.4-P2 | parsed | Task 10 | mapped | source.md:1363 |
| 12.4-P3 | parsed | Task 10 | mapped | source.md:1364 |
| 12.4-P4 | parsed | Task 10 | mapped | source.md:1365 |
| 12.4-P5 | parsed | Task 10 | mapped | source.md:1366 |
| 12.4-P6 | parsed | Task 10 | mapped | source.md:1367 |
| 12.4-P7 | parsed | Task 10 | mapped | source.md:1368 |
| 12.4-P8 | parsed | Task 10 | mapped | source.md:1369 |
| 12.4-P9 | parsed | Task 10 | mapped | source.md:1370 |
| 12.4-P10 | parsed | Task 10 | mapped | source.md:1371 |
| 12.4-P11 | parsed | Task 10 | mapped | source.md:1372 |
| 12.4-P12 | parsed | Task 10 | mapped | source.md:1373 |
| 12.4-F1 | parsed | Task 11 | mapped | source.md:1379 |
| 12.4-F2 | parsed | Task 11 | mapped | source.md:1380 |
| 12.4-F3 | parsed | Task 11 | mapped | source.md:1381 |
| 12.4-F4 | parsed | Task 11 | mapped | source.md:1382 |
| 12.4-F5 | parsed | Task 11 | mapped | source.md:1383 |
| 12.4-F6 | parsed | Task 11 | mapped | source.md:1384 |
| 12.4-F7 | parsed | Task 11 | mapped | source.md:1385 |
| 12.4-F8 | parsed | Task 11 | mapped | source.md:1386 |
| 12.4-F9 | parsed | Task 11 | mapped | source.md:1387 |
| 12.4-F10 | parsed | Task 11 | mapped | source.md:1388 |
| 12.4-F11 | parsed | Task 11 | mapped | source.md:1389 |
| 12.4-F12 | parsed | Task 11 | mapped | source.md:1390 |
| 12.4-EV1 | parsed | Task 12 | mapped | source.md:1392 |
| 12.4-EV2 | parsed | Task 12 | mapped | source.md:1392 |
| 12.4-EV3 | parsed | Task 12 | mapped | source.md:1392 |
| 12.4-EV4 | parsed | Task 12 | mapped | source.md:1392 |
| 12.4-CI1 | parsed | Task 13 | mapped | source.md:1394 |
| 12.4-CI2 | parsed | Task 13 | mapped | source.md:1394 |
| 12.4-CI3 | parsed | Task 13 | mapped | source.md:1394 |
| 12.4-CI4 | parsed | Task 13 | mapped | source.md:1394 |
| 12.4-X1 | parsed | Task 19 | mapped | source.md:1400 |
| 12.4-X2 | parsed | Task 19 | mapped | source.md:1401 |
| 12.4-X3 | parsed | Task 19 | mapped | source.md:1402 |
| 13-step-1 | parsed | Task 1 | mapped | source.md:1416 |
| 13-step-2 | parsed | Task 2 | mapped | source.md:1417 |
| 13-step-3 | parsed | Task 3, Task 4 | mapped | source.md:1418 |
| 13-step-4 | parsed | Task 5 | mapped | source.md:1419 |
| 13-step-5 | parsed | Task 6 | mapped | source.md:1420 |
| 13-step-6 | parsed | Task 7 | mapped | source.md:1421 |
| 13-step-7 | parsed | Task 4, Task 8 | mapped | source.md:1422 |
| 13-step-8 | parsed | Task 9 | mapped | source.md:1423 |
| 13-step-9 | parsed | Task 10, Task 11, Task 12, Task 13 | mapped | source.md:1424 |
| 13-step-10 | parsed | Task 14, Task 15, Task 16 | mapped | source.md:1425 |
| 13-step-11 | parsed | Task 17 | mapped | source.md:1426 |
| 13-step-12 | parsed | Task 18 | mapped | source.md:1427 |
| 13-step-13 | parsed | Task 19 | mapped | source.md:1428 |
| 13-step-14 | parsed | Task 20 | mapped | source.md:1429 |
| 6.5-site-1 | parsed | Task 2 | mapped | source.md:728 |
| 6.5-site-2 | parsed | Task 2 | mapped | source.md:729 |
| sec-8 | parsed | Task 14, Task 15, Task 16, Task 17, Task 20 | mapped | source.md:861-864 |
| sec-12 | parsed | Task 3, Task 10, Task 19 | mapped | source.md:1314-1317 |
| sec-12.5 | parsed | Task 20 | mapped | source.md:1406-1409 |
| 13-step-14 | parsed | Task 20 | mapped | source.md:1429 |
