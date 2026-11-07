---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: deep
slug: TASK-WF-p3Requirements-20261107-070713
version: "1"
priority: Medium
created_date: "2026-11-07"
---

# pr-submit: late conflict re-sync during the CI wait (P3 of #305, issue #361)

Source: ./source.md
Goal: While `/sc:pr-submit` waits on CI (Wave 8), a PR that turns conflicting is detected from the CI poll and the Wave 8a conflict step runs once more under the existing router (`SYNC_CAP = 1`, Tier 0 and Tier 1 only; a late Tier 2 conflict halts), with the protocol text, user docs and tests agreeing with the code. Requirements R-001 to R-014 in `./source.md` are the contract; each task names the ones it satisfies.

## Constraints

- Edit canonical sources under `src/superclaude/` only, then run `make sync-dev`; the `.claude/` mirrors are generated and are never staged.
- Use `uv run ...` for every Python and pytest call; no bare `python` or `pip`.
- `src/superclaude/pr_submit/fsm.py`, `run_log.py`, `models.py` and `ci.py` are not edited, no new `EventType` is added and every existing push-safety rule stays as it is (R-003, R-004).
- `src/superclaude/pr_submit/conflicts.py` and `src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md` are in the core-pure file set of `tests/pr_submit/test_static_grep.py`: neither may contain the standalone words `gh` or `git` on any line, comments and docstrings included.
- Several tests pin exact lines of the files this plan edits: `tests/skills/test_worker_contract.py` (an inventory keyed by exact file line, with a stale-entry check), `tests/pr_submit/test_conflict_sync_protocol.py` (fragments E1 to E13, order pins) and `tests/pr_submit/test_static_grep.py`. Each task that changes a pinned line updates the pin in the same task. The router outcomes any prose describes are the table in R-005 of `./source.md`, which `_WAVE8A_ROWS` in `tests/pr_submit/test_conflicts_core.py` already pins, so no router row is added anywhere in this plan.
- Every new prose deliverable gets its own positive assertion scoped to that text (R-012 part d), so that removing only that text fails exactly that assertion.
- Non-goal: the go/no-go gate of the issue (one real run where the base moved, or a maintainer waiver) is a release sign-off item and stays open (R-014). Nothing in this plan runs against a real PR.
- Non-goal: `.dev/brainstorms/issue-305-pr-submit-conflict-resolution/merged-requirements.md` and `.dev/designs/issue-305-pr-submit-conflict-resolution/DESIGN.md` are historical records and are not edited.
- Owner authorization (2026-11-07, relayed by the coordinator): after the third advisory review left two word-level blocking findings (the "unconditional" end-of-wait re-read in R-010 and Task 7, and the over-general status bullet in R-005), the owner allowed word edits to `./source.md` and this plan, with the listed minor guardrails, and no fourth review. The corrections are in R-005, R-010, Task 7 and the guardrails of Tasks 1, 2, 6, 7, 9 and 10; the report is `.dev/reflect/pre-TASK-WF-p3Requirements-20261107-070713-20261107070932/REPORT.md`.

## Phase 1: Poll payload reports the merge state

## Task 1: Append `merge_state` to the poll JSON line in `poll-ci-checks.sh`

Satisfies: R-001, R-009 (poll script rows).

Edit `src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh` (pr mode only; evidence mode is untouched).

- Add `mergeable,mergeStateStatus` to the `--json` field list of both `gh pr view "$PR" --repo "$REPO"` calls (`PR_JSON` at line 71 and `PR_AFTER` at line 108). Keep `--repo "$REPO"` on every `gh` line.
- The early-return payload (first `gh pr view` fails, line 73) becomes `{pr, head_sha:"", source:"ci", state:"polling", checks:[], merge_state:{mergeable:"", status:""}}`.
- The final `jq` output (lines 115 to 118) appends `merge_state:{mergeable:(.mergeable // ""), status:(.mergeStateStatus // "")}` after `checks`, read from the latest `PR_JSON` (the re-sampled one when it succeeded). The existing keys keep their names, values and order.
- Update the header comment block (the Output lines 8 to 9 only) to document the key; line 16 of the script (the comment line that quotes `gh pr checks --json`) is the key of an inventory row in `tests/skills/test_worker_contract.py` and stays byte-identical. The new comment must not contain the word "force" (any case) or the literal text `gh pr checks --repo`, and must not mention `gh pr` or `gh api`.
- In `tests/skills/test_worker_contract.py` replace the inventory rows keyed to the old `PR_JSON=...` (row near line 1806) and `PR_AFTER=...` (row near line 1838) lines of `poll-ci-checks.sh` with rows for the new lines, using the same `never-worker` classification and reason text as the neighbouring rows. Delete rows whose lines no longer exist.

Acceptance criteria:
- With a stub where `gh pr view` returns `"mergeable":"CONFLICTING","mergeStateStatus":"DIRTY"`, `poll-ci-checks.sh --pr N --repo R` prints one JSON line whose keys are, in order, `pr`, `head_sha`, `source`, `state`, `checks`, `merge_state`, and `merge_state` is `{"mergeable":"CONFLICTING","status":"DIRTY"}`.
- When the first `gh pr view` fails the printed line has `merge_state` with two empty strings and the script exits 0.
- `uv run pytest tests/skills/test_worker_contract.py tests/pr_submit/test_static_grep.py tests/pr_submit/test_conflict_sync_protocol.py tests/pr_submit/test_conflict_scripts.py -q` passes, including `test_every_write_verb_hit_is_classified`, `test_classification_table_has_no_stale_entries`, `test_gh_command_lines_are_repo_scoped` and `test_poll_ci_evidence_mode_static_rules`.

## Task 2: Test the poll payload shape with a stubbed `gh`

Depends on: Task 1

Satisfies: R-012 (part a).

Add tests to `tests/pr_submit/test_conflict_scripts.py` in the `poll-ci-checks.sh` section after the `--evidence-sha` tests, reusing `make_repos`, `Repos` and `ProbeRun`. Name every new test function with `poll` in its name.

- Add new helpers named `install_pr_poll_gh_stub` and `run_pr_poll` (do not reuse or shadow `install_ci_gh_stub` and `run_evidence_poll`, which carry evidence-mode semantics for the C1 to C4 tests); the module-level skip of `test_conflict_scripts.py` applies to the new tests. `install_pr_poll_gh_stub` installs a recording `gh` stub serving `pr checks --repo <R> --help` (prints a line containing `--json`), `pr view <N> --repo <R> --json ...` (a counter file in the stub directory makes the first and second call return the content of two different environment variables, and a value `FAIL` makes that call exit 1), and `pr checks <N> --repo <R> [--required] --json ...` (prints environment values); any other call exits 1.
- Table-driven cases for the `merge_state` value: `CONFLICTING`/`DIRTY`, `MERGEABLE`/`CLEAN`, `MERGEABLE`/`BEHIND`, `UNKNOWN`/`UNKNOWN`, fields missing from the view JSON, and a failing first `gh pr view`.
- One case with different `headRefOid` values in the two views: `state` is `polling` and `merge_state` comes from the second view.
- One case asserting the key order of the printed object.

Acceptance criteria:
- `uv run pytest tests/pr_submit/test_conflict_scripts.py -q -k poll` passes and runs at least the six value cases, the changed-head case and the key-order case.
- Running the new tests once against a temporary copy of the script without `merge_state` in its final `jq` expression fails them (checked by hand, the copy is not kept).
- The existing C1 to C4 evidence tests and `test_poll_ci_evidence_mode_static_rules` still pass unchanged.

## Phase 2: Late trigger decision in the deterministic core

## Task 3: Add `late_conflict_trigger` to `conflicts.py` and export it

Satisfies: R-002, R-012 (part b).

In `src/superclaude/pr_submit/conflicts.py`, directly after `needs_probe`, add `late_conflict_trigger(payload: object, wait_sha: object = None) -> bool` exactly as R-002 of `./source.md` describes: true only for a dict payload whose `merge_state` dict yields `mergeability_hint(mergeable, status) == "conflicting"`; false for every other input, including a `wait_sha` that is a non-empty string different from a non-empty `payload["head_sha"]` (an empty or non-string `head_sha` or `wait_sha` gives no mismatch information, as in `classify_checks`); it never raises. The docstring is two sentences, cites FR-24 and FR-25, and contains no standalone `gh` or `git` word. Re-export the function in `src/superclaude/pr_submit/__init__.py` the way `mergeability_hint` and `needs_probe` are (import list and `__all__`).

Add table-driven tests to `tests/pr_submit/test_conflicts_core.py` beside the `mergeability_hint` tests: conflicting payload with checks, conflicting payload with `state: polling` and `checks: []`, conflicting payload that is otherwise `clean`, `DIRTY` status with `MERGEABLE`, lowercase values, `BEHIND`, `BLOCKED`, `CLEAN`, `UNKNOWN`, empty strings, no `merge_state` key, `merge_state` not a dict, payload `None`, a list, junk values, and `wait_sha` equal, different, empty and absent, plus a non-string `head_sha` and a non-string `wait_sha`.

Acceptance criteria:
- `late_conflict_trigger({"head_sha": "a", "state": "polling", "checks": [], "merge_state": {"mergeable": "CONFLICTING", "status": "DIRTY"}}, wait_sha="a")` is `True`; the same call with `wait_sha="b"` is `False`; the same payload with `"MERGEABLE"`/`"CLEAN"` is `False`; a payload without `merge_state` is `False`.
- `uv run pytest tests/pr_submit/test_conflicts_core.py tests/pr_submit/test_static_grep.py -q` passes, including `test_tn50_core_pure_no_gh_git_tokens` and the existing router tables unchanged.
- `uv run ruff check src/superclaude/pr_submit/conflicts.py src/superclaude/pr_submit/__init__.py tests/pr_submit/test_conflicts_core.py` reports no findings.

## Task 4: Guard the classifier against the new payload key

Depends on: Task 3

Satisfies: R-003, R-005 (no router change), R-012 (part c).

Add tests only; no source change, and no router row (`_WAVE8A_ROWS` at lines 929 to 1044 of `tests/pr_submit/test_conflicts_core.py` already pins every outcome of R-005).

- In `tests/pr_submit/test_ci_classify.py` add the R-003 payload-shape tests: a payload that carries `merge_state` classifies exactly like the same payload without it for pending, all-pass, fail, empty with `expect_checks` true and false, and a stale head, and `state: polling` with no checks stays `polling` when `merge_state` is conflicting. Say in a docstring that these are regression guards (they pass on today's code).

Acceptance criteria:
- `uv run pytest tests/pr_submit/test_ci_classify.py tests/pr_submit/test_conflicts_core.py -q` passes with every pre-existing test in both files unchanged and no tuple added to `_WAVE8A_ROWS`.
- Mutation check by hand: in a scratch copy where `classify_checks` returns `polling` whenever the payload's `merge_state` is conflicting, at least one of the new tests fails (the copy is not kept).

## Phase 3: Wave 8 and Wave 8a protocol text

## Task 5: Describe the late second Wave 8a pass in `SKILL.md` and move the pins

Depends on: Task 1, Task 3

Satisfies: R-004, R-005, R-006, R-007, R-008, R-009 (SKILL pins), R-012 (part d, Wave 8 sentences).

Edit `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md`, the Wave 8 bullet and the Wave 8a bullet.

- Wave 8 bullet: append sentences after the existing text, which stays byte-identical so fragment E9 of `tests/pr_submit/test_conflict_sync_protocol.py` and the wait-only sentence pinned by `test_wait_only_sentences_name_the_one_sync_exception` keep passing. The appended text states R-004 (evaluate `late_conflict_trigger(payload, wait_sha=...)` on every payload before acting on its classification), R-005 (outcomes in words, exactly as the corrected R-005 of `./source.md` words them: `terminal_halted` after `clean` or `report_only` and the retained status after a preserved outcome for the halt and report outcomes, status `proposed` for the L1 proposal, status `halt_before_push` for the L2 local resolution, and the continue-wait results of `resolve_push` and of a Tier 0 `none`), R-006 (the run-local "late pass confirmed" flag, set only when `conflict_action` returns something other than `none`, not persisted, a fired trigger counts as a hook that read `conflicting` for the end-of-wait re-read), R-007 (no conflict cycle started earlier) and R-008 (cap of at least 1 at every monitor level, `tier_above_cap` at cap 0, monitor 1 proposes and monitor 2 leaves an uncommitted merge only after `clean` or `report_only`, only monitor 3 pushes).
- Wave 8a bullet: replace the closing clause "(late re-sync: #361)" with a pointer saying the Wave 8 late trigger re-enters this step; the rest of the bullet is unchanged.
- `tests/pr_submit/test_conflict_sync_protocol.py`: fragment E10 now ends with the new clause; add a new pin named E14 made of full-sentence substrings of the appended Wave 8 text (not bare words), keep E13 as it is, change `test_skill_edits_cover_e1_to_e13` into an E1 to E14 check (range(1, 15)) with a new name, update the module docstring on line 5 ("thirteen ... E1 to E13") and the section comment on line 229.
- `tests/skills/test_worker_contract.py`: replace the inventory row keyed to the old Wave 8a `SKILL.md` line (key line begins `- **Wave 8a (L1+`, row near line 1191) with a row for the new line, same classification and reason text. Add a row for the changed Wave 8 bullet only if `test_every_write_verb_hit_is_classified` reports one (today none is keyed to it).

Acceptance criteria:
- `rg -n "late re-sync: #361" src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` finds nothing, and `rg -n "late_conflict_trigger" src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` finds the new sentence.
- Removing only the appended Wave 8 sentences from `SKILL.md` makes `test_skill_edit_present[E14]` fail while E9, E13 and the other pins still pass; `rg -n "E1 to E13|thirteen" tests/pr_submit/test_conflict_sync_protocol.py` finds no stale text.
- `uv run pytest tests/pr_submit/test_conflict_sync_protocol.py tests/pr_submit/test_static_grep.py tests/skills/test_worker_contract.py tests/pr_submit/test_skill_parse.py -q` passes, with E9 and the original E13 pin still asserted.

## Phase 4: Supporting protocol refs

## Task 6: Document the payload and the trigger in `refs/ci-poll.md`

Depends on: Task 1, Task 5

Satisfies: R-010 (`ci-poll.md`), R-009 (ci-poll rows), R-012 (part d).

Edit `src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md`.

- In "Poll surfaces" add `mergeable,mergeStateStatus` to the documented `gh pr view` field list and document the `merge_state` object (shape, empty strings when unavailable, appended after `checks`).
- Update the "Division of labour" bullet that says the script returns "a coarse `state` plus the raw `checks` array" so it names `merge_state`.
- Add a section "Late conflict trigger (P3)" after "Wave 8 entry": the trigger is `late_conflict_trigger(payload, wait_sha=...)` on every poll; it fires for a payload that carries a conflicting state, including a wait stuck at `polling` with no checks; it never changes `classify_checks`; `UNKNOWN`, missing values and a payload for another head never fire it. Reconcile the `pr_conflicting` skip sentence with the new section.
- The wait-only sentence pinned in `tests/pr_submit/test_static_grep.py` (lines 791 to 808) stays byte-identical, and the table row on line 28 of the ref that holds it stays on one line.
- In `tests/skills/test_worker_contract.py` replace or delete every inventory row whose keyed `refs/ci-poll.md` text changed (the `gh pr view <N> --repo <owner/repo> --json number,url,headRefOid` line row near 1654, and the line-21 paragraph row near 1223 to 1230 if that paragraph is reworded) and add a never-worker row for every new line of the ref that the scanner reports.

Acceptance criteria:
- Four new assertions in `tests/pr_submit/test_static_grep.py`, each run on `_prose(path)` of the ref (the helper takes the file `Path`), pin separately: the documented `merge_state` shape, the updated "Division of labour" bullet, the reconciled `pr_conflicting` skip sentence, and the "Late conflict trigger (P3)" section heading together with its trigger sentence; removing only one of the four texts fails only its assertion.
- `uv run pytest tests/pr_submit/test_static_grep.py tests/skills/test_worker_contract.py tests/pr_submit/test_conflict_sync_protocol.py -q` passes, including the stale-entry check.

## Task 7: Reconcile `refs/conflict-mechanical.md` with the late pass

Depends on: Task 5, Task 6

Run serially: Tasks 6 to 9 edit the same test files.

Satisfies: R-010 (`conflict-mechanical.md`), R-007, R-008, R-012 (part d).

Edit `src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md`.

- Section 8, bullet "End of the CI wait" (line 214): keep the final `mergeable` re-read, which runs when any hook this run read `conflicting` or the run was resumed, and its `late_conflict` halt as the backstop, add that a fired late trigger counts as a hook that read `conflicting`, and replace "late re-sync is #361" with a pointer to the Wave 8 late trigger. Do not call the re-read unconditional.
- Section 12, halt-reason table row `late_conflict` (line 289): replace "Late re-sync is #361." and list both causes: a Tier 2 conflict at the late pass with `--conflict-max-tier 2`, and the end-of-wait re-read that reads `CONFLICTING` (which needs no earlier conflict cycle, only an earlier `conflicting` read or a resume). Say that a Tier 1 conflict seen during the CI wait gets the one allowed cycle only under R-007 and R-008, and that a preserved review outcome is reported with its terminal status retained.
- Section 1 ("When this ref applies"): add one paragraph saying the late trigger re-enters hook `wave8a`, the cycle id is `conflict_cycle_id(plan.tier, len(conflict_cycles) + 1)` as in Step 3, and `--resume` restarts an open `wave8a` cycle at step 1. The paragraph must not contain any token of the order pins at `tests/pr_submit/test_conflict_sync_protocol.py` lines 116 to 133 (among them `sync_started`, `merge_preflight_ok`, the merge command, `merge_parent_ok(` and `--is-ancestor`), and any new line that names `conflict-intent.md` or `evidence-validator` must contain "Tier 2" (lines 412 to 427 of the same file).
- Add no new `gh` or `git` command line; the prohibited-operation scan (FR-21) must still pass.

Acceptance criteria:
- `rg -n "#361" src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md` finds nothing and `rg -n "sync_cycles" src` finds nothing.
- Three new assertions in `tests/pr_submit/test_conflict_sync_protocol.py` pin separately the section 8 bullet clause (the words "fired late trigger"), the two causes in the `late_conflict` row, and the section 1 paragraph (the words "len(conflict_cycles) + 1" and "wave8a"); removing only one text fails only its assertion.
- `uv run pytest tests/pr_submit/test_conflict_sync_protocol.py tests/pr_submit/test_static_grep.py tests/skills/test_worker_contract.py -q` passes, including `MECHANICAL_PINS` and the order pins.

## Task 8: Add the late pass to `refs/state-machine.md` section 5.2d

Depends on: Task 5, Task 7

Run serially: Tasks 6 to 9 edit the same test files.

Satisfies: R-010 (`state-machine.md`), R-007, R-008, R-012 (part d).

Edit `src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md`, section 5.2d: add one sentence to the Tier 1 bullet saying the sync can also run once from the Wave 8 late trigger, still with no FSM edge, no round and no re-trigger, and stating the R-007 cap wording and the R-008 preconditions (cap of at least 1 at every monitor level, only monitor 3 pushes, monitors 1 and 2 act only after `clean` or `report_only`). Leave the wait-only sentence pinned by `test_wait_only_sentences_name_the_one_sync_exception` byte-identical and add no standalone `gh` or `git` word.

Acceptance criteria:
- A new assertion in `tests/pr_submit/test_static_grep.py` runs on `_prose(path)` of the file (the helper takes the file `Path`) and pins the new sentence ("late trigger", "conflict cycle started earlier", "`--conflict-max-tier` of at least 1"); removing only that sentence fails it, and the section still states `SYNC_CAP = 1`, `sync_push_count` and that the sync never counts in `push_count`.
- `uv run pytest tests/pr_submit/test_static_grep.py tests/pr_submit/test_autonomy_gates.py tests/pr_submit/test_conflict_sync_protocol.py -q` passes, including `test_tn50_core_pure_no_gh_git_tokens`.

## Phase 5: User-facing docs

## Task 9: Update the command summary and the user guides

Depends on: Task 5, Task 8

Run serially: Tasks 6 to 9 edit the same test files.

Satisfies: R-011, R-007, R-008, R-012 (part d).

Edit `src/superclaude/commands/pr-submit.md` (the paragraph at line 72 ending "Late text conflicts halt..."), `docs/user-guide/commands.md` (the paragraph at line 501) and `docs/user-guide/flags.md` (the paragraph at line 214). Add one sentence to each: a conflict that first appears while the CI wait is running gets one more Tier 1 sync only when no conflict cycle started earlier in the run; it needs `--conflict-max-tier` of at least 1 at every monitor level (with the default cap of 0 it ends with `tier_above_cap`); with a cap of at least 1 monitor 1 only proposes and monitor 2 only leaves a validated uncommitted merge, both only after a `clean` or `report_only` review, and only monitor 3 pushes; a late text (Tier 2) conflict halts. Keep the phrases that tests pin (listed in R-011 of `./source.md`).

Acceptance criteria:
- `uv run pytest tests/pr_submit/test_conflict_sync_protocol.py -q` passes.
- A new test in `tests/pr_submit/test_conflict_sync_protocol.py` asserts, per file and on its prose-normalised text, that each of the three files contains the full new sentence as written in that file (a full-sentence substring, not bare words, because "tier_above_cap" and "only after" may occur elsewhere in the same file) and, as a second check, the phrase "conflict cycle started earlier"; removing the new sentence from any one file fails only that file's case.

## Phase 6: Release notes and final sync

## Task 10: Add the changelog entry and sync the dev copies

Depends on: Task 2, Task 4, Task 5, Task 6, Task 7, Task 8, Task 9

Satisfies: R-013, R-014, R-012 (part d).

Edit `CHANGELOG.md`: add a bullet "pr-submit late conflict re-sync (P3, #361)" under `#### Added (pr-submit conflicts)` of the `### sc:pr-submit: merge-conflict detection and resolution (#305)` block (line 131 onward). It states the `merge_state` poll field, the late second Wave 8a pass, its limits per R-007 and R-008, that a late Tier 2 conflict halts as `late_conflict` with a cap of 2 and as `tier_above_cap` below it, and that the real-run go/no-go gate is still open. Rewrite the sentence "Late re-sync during the CI wait is #361." (line 146 of the same block) in place so it no longer reads as future work. Add a new test with a clear name (for example in `tests/pr_submit/test_conflict_sync_protocol.py`) with three separate assertions: `CHANGELOG.md` contains "late conflict re-sync", does not contain "is #361", and contains the rewritten sentence in full (so deleting the old sentence without a replacement fails). Then run `make sync-dev`.

Acceptance criteria:
- `rg -n "late conflict re-sync" CHANGELOG.md` finds the new bullet, `rg -n "is #361" CHANGELOG.md` finds nothing, and each of the three assertions of the new test fails when only its text is removed.
- `make sync-dev` succeeds and `make verify-sync` passes.
- `uv run pytest tests/pr_submit tests/skills/test_worker_contract.py tests/unit/test_cli_install.py -q` passes and `make lint` reports no findings.
- `git diff --name-only` lists only paths under `src/superclaude/`, `tests/`, `docs/user-guide/`, `CHANGELOG.md` and `.dev/tasks/`, and `git diff --cached --name-only` lists no `.claude/` path.
