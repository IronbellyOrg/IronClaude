---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: deep
slug: TASK-WF-p3Requirements-20261107-065757
version: "1"
priority: Medium
created_date: "2026-11-07"
---

# pr-submit: late conflict re-sync during the CI wait (P3 of #305, issue #361)

Source: ./source.md
Goal: While `/sc:pr-submit` waits on CI (Wave 8), a PR that turns conflicting is detected from the CI poll and the Wave 8a conflict step runs once more under the existing router (`SYNC_CAP = 1`, Tier 0 and Tier 1 only; a late Tier 2 conflict halts with reason `late_conflict`), with the protocol text, user docs and tests agreeing with the code. Requirements R-001 to R-014 in `./source.md` are the contract; each task names the ones it satisfies.

## Constraints

- Edit canonical sources under `src/superclaude/` only, then run `make sync-dev`; the `.claude/` mirrors are generated and are never staged.
- Use `uv run ...` for every Python and pytest call; no bare `python` or `pip`.
- `src/superclaude/pr_submit/fsm.py`, `run_log.py`, `models.py` and `ci.py` are not edited, no new `EventType` is added and every existing push-safety rule stays as it is (R-003, R-004).
- `src/superclaude/pr_submit/conflicts.py` and `src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md` are in the core-pure file set of `tests/pr_submit/test_static_grep.py`: neither may contain the standalone words `gh` or `git` on any line, comments and docstrings included.
- Several tests pin exact lines of the files this plan edits: `tests/skills/test_worker_contract.py` (an inventory keyed by exact file line, with a stale-entry check), `tests/pr_submit/test_conflict_sync_protocol.py` (fragments E1 to E13) and `tests/pr_submit/test_static_grep.py`. Each task that changes a pinned line updates the pin in the same task, and the router outcomes it describes follow the table in R-005 of `./source.md`.
- Non-goal: the go/no-go gate of the issue (one real run where the base moved, or a maintainer waiver) is a release sign-off item and stays open (R-014). Nothing in this plan runs against a real PR.
- Non-goal: `.dev/brainstorms/issue-305-pr-submit-conflict-resolution/merged-requirements.md` and `.dev/designs/issue-305-pr-submit-conflict-resolution/DESIGN.md` are historical records and are not edited.

## Phase 1: Poll payload reports the merge state

## Task 1: Append `merge_state` to the poll JSON line in `poll-ci-checks.sh`

Satisfies: R-001, R-009 (poll script rows).

Edit `src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh` (pr mode only; evidence mode is untouched).

- Add `mergeable,mergeStateStatus` to the `--json` field list of both `gh pr view "$PR" --repo "$REPO"` calls (`PR_JSON` at line 71 and `PR_AFTER` at line 108). Keep `--repo "$REPO"` on every `gh` line.
- The early-return payload (first `gh pr view` fails) becomes `{pr, head_sha:"", source:"ci", state:"polling", checks:[], merge_state:{mergeable:"", status:""}}`.
- The final `jq` output appends `merge_state:{mergeable:(.mergeable // ""), status:(.mergeStateStatus // "")}` after `checks`, read from the latest `PR_JSON` (the re-sampled one when it succeeded). The existing keys keep their names, values and order.
- Update the header comment block (the Output line) to document the key. The new comment must not contain the word "force" (any case) or the literal text `gh pr checks --repo`, and must not mention `gh pr` or `gh api`.
- In `tests/skills/test_worker_contract.py` replace the inventory rows keyed to the old `PR_JSON=...` (row near line 1806) and `PR_AFTER=...` (row near line 1838) lines of `poll-ci-checks.sh` with rows for the new lines, using the same `never-worker` classification and reason text as the neighbouring rows. Delete rows whose lines no longer exist.

Acceptance criteria:
- With a stub where `gh pr view` returns `"mergeable":"CONFLICTING","mergeStateStatus":"DIRTY"`, `poll-ci-checks.sh --pr N --repo R` prints one JSON line whose keys are, in order, `pr`, `head_sha`, `source`, `state`, `checks`, `merge_state`, and `merge_state` is `{"mergeable":"CONFLICTING","status":"DIRTY"}`.
- When the first `gh pr view` fails the printed line has `merge_state` with two empty strings and the script exits 0.
- `uv run pytest tests/skills/test_worker_contract.py tests/pr_submit/test_static_grep.py tests/pr_submit/test_conflict_sync_protocol.py tests/pr_submit/test_conflict_scripts.py -q` passes, including `test_every_write_verb_hit_is_classified`, `test_classification_table_has_no_stale_entries`, `test_gh_command_lines_are_repo_scoped` and `test_poll_ci_evidence_mode_static_rules`.

## Task 2: Test the poll payload shape with a stubbed `gh`

Depends on: Task 1

Satisfies: R-012 (part a).

Add tests to `tests/pr_submit/test_conflict_scripts.py` in the `poll-ci-checks.sh` section after the `--evidence-sha` tests, reusing `make_repos`, `Repos` and `ProbeRun`. Name every new test function with `poll` in its name.

- Add a helper that installs a recording `gh` stub serving `pr checks --repo <R> --help` (prints a line containing `--json`), `pr view <N> --repo <R> --json ...` (a counter file in the stub directory makes the first and second call return the content of two different environment variables, and a value `FAIL` makes that call exit 1), and `pr checks <N> --repo <R> [--required] --json ...` (prints environment values); any other call exits 1.
- Table-driven cases for the `merge_state` value: `CONFLICTING`/`DIRTY`, `MERGEABLE`/`CLEAN`, `MERGEABLE`/`BEHIND`, `UNKNOWN`/`UNKNOWN`, fields missing from the view JSON, and a failing first `gh pr view`.
- One case with different `headRefOid` values in the two views: `state` is `polling` and `merge_state` comes from the second view.
- One case asserting the key order of the printed object.

Acceptance criteria:
- `uv run pytest tests/pr_submit/test_conflict_scripts.py -q -k poll` passes and runs at least the six value cases, the changed-head case and the key-order case.
- Running the new tests once against a temporary copy of the script without `merge_state` in its final `jq` expression fails them (checked by hand, the copy is not kept).
- The existing C1 to C4 evidence tests and `test_poll_ci_evidence_mode_static_rules` still pass unchanged.

## Phase 2: Late trigger decision in the deterministic core

## Task 3: Add `late_conflict_trigger` to `conflicts.py` and export it

Satisfies: R-002, R-012 (part b, trigger tests).

In `src/superclaude/pr_submit/conflicts.py`, directly after `needs_probe`, add `late_conflict_trigger(payload: object, wait_sha: object = None) -> bool` exactly as R-002 of `./source.md` describes: true only for a dict payload whose `merge_state` dict yields `mergeability_hint(mergeable, status) == "conflicting"`; false for every other input, including a `wait_sha` that is a non-empty string different from a non-empty `payload["head_sha"]`; it never raises. The docstring is two sentences, cites FR-24 and FR-25, and contains no standalone `gh` or `git` word. Re-export the function in `src/superclaude/pr_submit/__init__.py` the way `mergeability_hint` and `needs_probe` are (import list and `__all__`).

Add table-driven tests to `tests/pr_submit/test_conflicts_core.py` beside the `mergeability_hint` tests: conflicting payload with checks, conflicting payload with `state: polling` and `checks: []`, conflicting payload that is otherwise `clean`, `DIRTY` status with `MERGEABLE`, lowercase values, `BEHIND`, `BLOCKED`, `CLEAN`, `UNKNOWN`, empty strings, no `merge_state` key, `merge_state` not a dict, payload `None`, a list, junk values, and `wait_sha` equal, different, empty and absent.

Acceptance criteria:
- `late_conflict_trigger({"head_sha": "a", "state": "polling", "checks": [], "merge_state": {"mergeable": "CONFLICTING", "status": "DIRTY"}}, wait_sha="a")` is `True`; the same call with `wait_sha="b"` is `False`; the same payload with `"MERGEABLE"`/`"CLEAN"` is `False`; a payload without `merge_state` is `False`.
- `uv run pytest tests/pr_submit/test_conflicts_core.py tests/pr_submit/test_static_grep.py -q` passes, including `test_tn50_core_pure_no_gh_git_tokens` and the existing router tables unchanged.
- `uv run ruff check src/superclaude/pr_submit/conflicts.py src/superclaude/pr_submit/__init__.py tests/pr_submit/test_conflicts_core.py` reports no findings.

## Task 4: Pin the late pass to the existing router and leave the classifier alone

Depends on: Task 3

Satisfies: R-003, R-005, R-012 (parts b and c).

Add tests only; no source change.

- In `tests/pr_submit/test_conflicts_core.py` first confirm that the `_WAVE8A_ROWS` table (lines 943 to 1032) already pins these late-pass outcomes and add only what it lacks: a row for Tier 1 with `conflict_max_tier=0` giving `tier_above_cap` (halt after `clean`, report after `no_response`), and a row for Tier 2 with `conflict_max_tier=1` giving `tier_above_cap` beside the existing `late_conflict` rows (which use cap 2). One short test documents, by calling `conflict_action(hook="wave8a", ...)` with `github_conflicting=True`, the R-005 table end to end.
- In `tests/pr_submit/test_ci_classify.py` add the R-003 payload-shape tests: a payload that carries `merge_state` classifies exactly like the same payload without it for pending, all-pass, fail, empty with `expect_checks` true and false, and a stale head, and `state: polling` with no checks stays `polling` when `merge_state` is conflicting.

Acceptance criteria:
- `uv run pytest tests/pr_submit/test_conflicts_core.py tests/pr_submit/test_ci_classify.py -q` passes with every pre-existing test in both files unchanged.
- The new `tier_above_cap` rows assert `(action, reason, status, skip_ci)` values taken from the router, and the R-005 test names the preserved-outcome rule (action `report`, no status) for `sync_cap` and `late_conflict` and `resolve_push` for an eligible L3 Tier 1 sync.

## Phase 3: Wave 8 and Wave 8a protocol text

## Task 5: Describe the late second Wave 8a pass in `SKILL.md` and move the pins

Depends on: Task 1, Task 3, Task 4

Satisfies: R-004, R-005, R-006, R-007, R-008, R-009 (SKILL pins), R-012 (part d, Wave 8 sentence).

Edit `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md`, the Wave 8 bullet and the Wave 8a bullet.

- Wave 8 bullet: append sentences after the existing text, which stays byte-identical so fragment E9 of `tests/pr_submit/test_conflict_sync_protocol.py` and the wait-only sentence pinned by `test_wait_only_sentences_name_the_one_sync_exception` keep passing. The appended text states R-004, R-005 (including the status per entering outcome), R-006 (the "late pass confirmed" flag, not persisted, unconfirmed readings leave it unset, a fired trigger counts as a hook that read `conflicting` for the end-of-wait re-read), R-007 (cap wording: no conflict cycle started earlier) and R-008 (L3 and `--conflict-max-tier` of at least 1; otherwise `tier_above_cap`, propose at L1, uncommitted merge at L2).
- Wave 8a bullet: replace the closing clause "(late re-sync: #361)" with a pointer saying the Wave 8 late trigger re-enters this step; the rest of the bullet is unchanged.
- `tests/pr_submit/test_conflict_sync_protocol.py`: fragment E10 now ends with the new clause; add a new pin named E14 for the appended Wave 8 sentences, keep E13 as it is, change `test_skill_edits_cover_e1_to_e13` into an E1 to E14 check (range(1, 15)) with a new name, and update the module docstring that says E1 to E13.
- `tests/skills/test_worker_contract.py`: replace the inventory row keyed to the old Wave 8a `SKILL.md` line (key line begins `- **Wave 8a (L1+`, row near line 1191) with a row for the new line, same classification and reason text. Add a row for the changed Wave 8 bullet only if `test_every_write_verb_hit_is_classified` reports one (today none is keyed to it).

Acceptance criteria:
- `rg -n "late re-sync: #361" src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` finds nothing, and `rg -n "late_conflict_trigger" src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` finds the new sentence.
- The E14 pin asserts the words "late_conflict_trigger", "at most once", "conflict cycle", "tier_above_cap" and the retained-terminal-status clause; removing any of them from `SKILL.md` makes `test_skill_edit_present[E14]` fail.
- `uv run pytest tests/pr_submit/test_conflict_sync_protocol.py tests/pr_submit/test_static_grep.py tests/skills/test_worker_contract.py tests/pr_submit/test_skill_parse.py -q` passes, with E9 and the original E13 pin still asserted.

## Phase 4: Supporting protocol refs

## Task 6: Document the payload and the trigger in `refs/ci-poll.md`

Depends on: Task 1, Task 5

Satisfies: R-010 (`ci-poll.md`), R-009 (ci-poll row), R-012 (part d).

Edit `src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md`.

- In "Poll surfaces" add `mergeable,mergeStateStatus` to the documented `gh pr view` field list and document the `merge_state` object (shape, empty strings when unavailable, appended after `checks`).
- Add a section "Late conflict trigger (P3)" after "Wave 8 entry": the trigger is `late_conflict_trigger(payload, wait_sha=...)` on every poll; it fires for a payload that carries a conflicting state, including a wait stuck at `polling` with no checks; it never changes `classify_checks`; `UNKNOWN`, missing values and a payload for another head never fire it. Reconcile the `pr_conflicting` skip sentence with the new section.
- The wait-only sentence pinned in `tests/pr_submit/test_static_grep.py` (lines 791 to 808) stays byte-identical.
- In `tests/skills/test_worker_contract.py` replace the inventory row keyed to the old `gh pr view <N> --repo <owner/repo> --json number,url,headRefOid` line of this ref (row near line 1654) and add a never-worker row for every new line of `refs/ci-poll.md` that the scanner reports.

Acceptance criteria:
- A new assertion in `tests/pr_submit/test_static_grep.py` pins the words "Late conflict trigger" and the documented `merge_state` shape in `refs/ci-poll.md` and fails when either is removed.
- `uv run pytest tests/pr_submit/test_static_grep.py tests/skills/test_worker_contract.py tests/pr_submit/test_conflict_sync_protocol.py -q` passes.

## Task 7: Reconcile `refs/conflict-mechanical.md` with the late pass

Depends on: Task 5

Satisfies: R-010 (`conflict-mechanical.md`), R-007, R-012 (part d).

Edit `src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md`.

- Section 8, bullet "End of the CI wait" (line 214): keep the final `mergeable` re-read and its `late_conflict` halt as the backstop, say that a fired late trigger counts as a hook that read `conflicting`, and replace "late re-sync is #361" with a pointer to the Wave 8 late trigger.
- Section 12, halt-reason table row `late_conflict` (line 289): replace "Late re-sync is #361." with text saying a Tier 1 conflict seen during the CI wait gets the one allowed cycle when none started earlier (L3, `--conflict-max-tier` of at least 1), and only a Tier 2 conflict or a re-read after a cycle started halts here.
- Section 1 ("When this ref applies"): add one paragraph saying the late trigger re-enters hook `wave8a`, the cycle id is `conflict_cycle_id(plan.tier, len(conflict_cycles) + 1)` as in Step 3, and `--resume` restarts an open `wave8a` cycle at step 1.
- Add no new `gh` or `git` command line; the prohibited-operation scan (FR-21) must still pass.

Acceptance criteria:
- `rg -n "#361" src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md` finds nothing and `rg -n "sync_cycles" src` finds nothing.
- A new assertion in `tests/pr_submit/test_conflict_sync_protocol.py` pins the section 1 paragraph (the words "len(conflict_cycles) + 1" and "wave8a") and the changed `late_conflict` row, and fails when either is removed.
- `uv run pytest tests/pr_submit/test_conflict_sync_protocol.py tests/pr_submit/test_static_grep.py tests/skills/test_worker_contract.py -q` passes, including `MECHANICAL_PINS`.

## Task 8: Add the late pass to `refs/state-machine.md` section 5.2d

Depends on: Task 5

Satisfies: R-010 (`state-machine.md`), R-007, R-012 (part d).

Edit `src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md`, section 5.2d: add one sentence to the Tier 1 bullet saying the sync can also run once from the Wave 8 late trigger when no conflict cycle started earlier, still with no FSM edge, no round and no re-trigger. Leave the wait-only sentence pinned by `test_wait_only_sentences_name_the_one_sync_exception` byte-identical and add no standalone `gh` or `git` word.

Acceptance criteria:
- `uv run pytest tests/pr_submit/test_static_grep.py tests/pr_submit/test_autonomy_gates.py tests/pr_submit/test_conflict_sync_protocol.py -q` passes, including `test_tn50_core_pure_no_gh_git_tokens`.
- A new assertion in `tests/pr_submit/test_static_grep.py` pins the new sentence (the words "late trigger" and "conflict cycle started earlier") and fails when it is removed; the section still states `SYNC_CAP = 1`, `sync_push_count` and that the sync never counts in `push_count`.

## Phase 5: User-facing docs

## Task 9: Update the command summary and the user guides

Depends on: Task 5

Satisfies: R-011, R-007, R-008, R-012 (part d).

Edit `src/superclaude/commands/pr-submit.md` (the paragraph at line 72 ending "Late text conflicts halt..."), `docs/user-guide/commands.md` (the paragraph at line 501) and `docs/user-guide/flags.md` (the paragraph at line 214). Add one sentence to each: a conflict that first appears while the CI wait is running gets one more Tier 1 sync only when no conflict cycle started earlier in the run, at monitor 3 with `--conflict-max-tier` of at least 1 (with the default cap of 0 it halts as `tier_above_cap`, at monitor 1 it is proposed, at monitor 2 it is left as a validated uncommitted merge); a late text (Tier 2) conflict halts. Keep the phrases that tests pin (listed in R-011 of `./source.md`).

Acceptance criteria:
- `uv run pytest tests/pr_submit/test_conflict_sync_protocol.py -q` passes.
- A new test in `tests/pr_submit/test_conflict_sync_protocol.py` asserts that each of the three files contains the words "CI wait", "conflict cycle started earlier" and "tier_above_cap", and fails when the new sentence is removed from any one of them.

## Phase 6: Release notes and final sync

## Task 10: Add the changelog entry and sync the dev copies

Depends on: Task 2, Task 4, Task 5, Task 6, Task 7, Task 8, Task 9

Satisfies: R-013, R-014, R-012 (part d).

Edit `CHANGELOG.md`: under `## [Unreleased]` add an entry "pr-submit late conflict re-sync (P3, #361)" in the section the file already uses for features, stating the `merge_state` poll field, the late second Wave 8a pass and its limits (Tier 0 and Tier 1, no conflict cycle started earlier, monitor 3 with `--conflict-max-tier` of at least 1, late Tier 2 halts `late_conflict`), and that the real-run go/no-go gate is still open. Edit the earlier sentence "Late re-sync during the CI wait is #361." so it no longer reads as future work. Then run `make sync-dev`.

Acceptance criteria:
- `rg -n "late conflict re-sync" CHANGELOG.md` finds the new entry, a test or the assertion in `tests/pr_submit/test_conflict_sync_protocol.py` fails when the entry is removed, and `rg -n "is #361" CHANGELOG.md` finds nothing.
- `make sync-dev` succeeds and `make verify-sync` passes.
- `uv run pytest tests/pr_submit tests/skills/test_worker_contract.py tests/unit/test_cli_install.py -q` passes and `make lint` reports no findings.
- `git diff --name-only` lists only paths under `src/superclaude/`, `tests/`, `docs/user-guide/`, `CHANGELOG.md` and `.dev/tasks/`, and `git diff --cached --name-only` lists no `.claude/` path.
