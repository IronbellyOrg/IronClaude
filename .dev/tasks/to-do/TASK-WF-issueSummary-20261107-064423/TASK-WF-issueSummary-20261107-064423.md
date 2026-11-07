---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: deep
slug: TASK-WF-issueSummary-20261107-064423
version: "1"
priority: Medium
created_date: "2026-11-07"
---

# pr-submit: late conflict re-sync during the CI wait (P3 of #305, issue #361)

Source: ./source.md
Goal: While `/sc:pr-submit` waits on CI (Wave 8), a PR that turns conflicting is detected from the CI poll and the Wave 8a conflict step runs once more under `SYNC_CAP = 1` (Tier 0 and Tier 1 only; a late Tier 2 conflict halts with reason `late_conflict`), with the protocol text, user docs and tests agreeing.

## Constraints

- Edit canonical sources under `src/superclaude/` only, then run `make sync-dev`; the `.claude/` mirrors are generated and are never staged.
- Use `uv run ...` for every Python and pytest call; no bare `python` or `pip`.
- Every existing push-safety rule stays as it is: `src/superclaude/pr_submit/fsm.py`, `src/superclaude/pr_submit/run_log.py`, `src/superclaude/pr_submit/models.py` and `src/superclaude/pr_submit/ci.py` are not edited. `classify_checks` keeps its current results for every existing payload, and the late trigger decision lives in `src/superclaude/pr_submit/conflicts.py` beside `mergeability_hint`, because `ci.py` must not depend on conflict code.
- No new `EventType`, no new hook label, no new `ConflictAction` row: the late pass reuses `conflict_action(hook="wave8a", ...)`, so the router stays the only conflict routing decision and `SYNC_CAP = 1` is enforced by `prior_conflict_cycles` exactly as it is for the first Wave 8a.
- Payload decision (the source leaves the value open): `merge_state` is an object `{"mergeable": <string>, "status": <string>}` holding GitHub's `mergeable` and `mergeStateStatus` values, with empty strings when they are unavailable, appended after the existing keys of the poll JSON line. The poll script holds no logic; `mergeability_hint` normalises the pair.
- Router outcomes stay as they are today and are documented, not changed: Tier 2 at the late pass halts `late_conflict`; a spent cap halts `sync_cap`; a probe that finds no conflict while GitHub reports one halts `github_disagrees`; Tier 3 follows `conflict_tier3`; L1 proposes and L2 leaves a validated uncommitted merge exactly as the first Wave 8a does.
- Non-goal: the go/no-go gate of the source (one real run where the base moved during the CI wait, or a maintainer waiver) is a release decision. Nothing in this plan runs against a real PR; the final report states the gate as still open.
- Non-goal: `.dev/brainstorms/issue-305-pr-submit-conflict-resolution/merged-requirements.md` and `.dev/designs/issue-305-pr-submit-conflict-resolution/DESIGN.md` are historical records of the #305 release and are not edited.
- Several tests pin exact lines of the files this plan edits: `tests/skills/test_worker_contract.py` (an inventory keyed by exact file line, with a stale-entry check), `tests/pr_submit/test_conflict_sync_protocol.py` (fragments E9 and E10) and `tests/pr_submit/test_static_grep.py`. Each task that changes a pinned line updates the pin in the same task.

## Phase 1: Poll payload reports the merge state

## Task 1: Append `merge_state` to the poll JSON line in `poll-ci-checks.sh`

Edit `src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh` (pr mode only; evidence mode is untouched).

- Add `mergeable,mergeStateStatus` to the `--json` field list of both `gh pr view "$PR" --repo "$REPO"` calls (`PR_JSON` and the re-sample `PR_AFTER`). Keep `--repo "$REPO"` on every `gh` line.
- The early-return payload (first `gh pr view` fails) becomes `{pr, head_sha:"", source:"ci", state:"polling", checks:[], merge_state:{mergeable:"", status:""}}`.
- The final `jq` output appends `merge_state:{mergeable:(.mergeable // ""), status:(.mergeStateStatus // "")}` after `checks`, read from the latest `PR_JSON` (the re-sampled one when it succeeded). The existing keys keep their names, values and order.
- Update the header comment block (the Output line) to document the new key. Do not add a comment line that mentions `gh pr` or `gh api` unless its inventory row is added below.
- Update `tests/skills/test_worker_contract.py`: replace the inventory rows keyed to the old `PR_JSON=...` and `PR_AFTER=...` lines of `poll-ci-checks.sh` with rows for the new lines (same `never-worker` classification and reason text as the neighbouring rows), and add a row for any other new or changed line the scanner reports for that file. Rows for lines that no longer exist are deleted.

Acceptance criteria:
- `poll-ci-checks.sh --pr N --repo R` against a stub where `gh pr view` returns `"mergeable":"CONFLICTING","mergeStateStatus":"DIRTY"` prints one JSON line whose last key is `merge_state` with `{"mergeable":"CONFLICTING","status":"DIRTY"}`, and the keys `pr`, `head_sha`, `source`, `state`, `checks` come first in that order.
- When the first `gh pr view` fails the printed line has `merge_state` with two empty strings and the script exits 0.
- `uv run pytest tests/skills/test_worker_contract.py tests/pr_submit/test_static_grep.py tests/pr_submit/test_conflict_sync_protocol.py -q` passes, including `test_every_write_verb_hit_is_classified`, `test_classification_table_has_no_stale_entries` and `test_gh_command_lines_are_repo_scoped`.

## Task 2: Test the poll payload shape with a stubbed `gh`

Depends on: Task 1

Add tests to `tests/pr_submit/test_conflict_scripts.py` in the `poll-ci-checks.sh` section (after the `--evidence-sha` tests, reusing `make_repos`, `Repos` and `ProbeRun`).

- Add a helper that installs a recording `gh` stub serving `pr checks --repo <R> --help` (prints a line containing `--json`), `pr view <N> --repo <R> --json ...` (prints the content of an environment variable, or fails when it holds `FAIL`), and `pr checks <N> --repo <R> [--required] --json ...` (prints environment values); any other call exits 1.
- Table-driven cases for the `merge_state` value: `CONFLICTING`/`DIRTY`, `MERGEABLE`/`CLEAN`, `MERGEABLE`/`BEHIND`, `UNKNOWN`/`UNKNOWN`, fields missing from the view JSON, and a failing first `gh pr view`.
- Name every new test function with `poll` in its name so the `-k poll` selection below finds it.
- One case asserting the key order of the printed object and that a changed head between the two views still yields `state: polling` while `merge_state` comes from the second view.

Acceptance criteria:
- `uv run pytest tests/pr_submit/test_conflict_scripts.py -q -k "poll"` passes and includes at least the six value cases and the key-order case above.
- The new tests fail if `merge_state` is removed from the script's final `jq` expression (checked by running them once against a temporary copy of the script without the key, not by committing that copy).
- The existing C1 to C4 evidence tests and `test_poll_ci_evidence_mode_static_rules` still pass unchanged.

## Phase 2: Late trigger decision in the deterministic core

## Task 3: Add `late_conflict_trigger` to `conflicts.py`

In `src/superclaude/pr_submit/conflicts.py`, directly after `needs_probe`, add `late_conflict_trigger(payload: object) -> bool`.

- Returns `True` only when `payload` is a dict, `payload["merge_state"]` is a dict, and `mergeability_hint(merge_state.get("mergeable"), merge_state.get("status"))` is `"conflicting"`. Every other input (not a dict, key missing as in an old payload, wrong types, `unknown`, `behind`, `blocked`, `clean`) returns `False`. It never raises and does not look at `state` or `checks`, so it covers both the payload that carries `CONFLICTING` and the wait that is stuck at `polling` with no checks.
- The docstring states the contract in two sentences and cites FR-24 and FR-25.
- Re-export it from `src/superclaude/pr_submit/__init__.py` the way `mergeability_hint` and `needs_probe` are (the import list and `__all__`).
- Add table-driven tests to `tests/pr_submit/test_conflicts_core.py` beside the `mergeability_hint` tests: conflicting payload with checks, conflicting payload with `state: polling` and `checks: []`, conflicting payload that is otherwise `clean`, `DIRTY` status with `MERGEABLE`, lowercase values, `BEHIND`, `BLOCKED`, `CLEAN`, `UNKNOWN`, empty strings, no `merge_state` key, `merge_state` not a dict, payload `None`, a list, and junk values.

Acceptance criteria:
- `late_conflict_trigger({"state": "polling", "checks": [], "merge_state": {"mergeable": "CONFLICTING", "status": "DIRTY"}})` is `True`; the same payload with `"MERGEABLE"`/`"CLEAN"` is `False`; a payload without `merge_state` is `False`.
- `uv run pytest tests/pr_submit/test_conflicts_core.py -q` passes, including the existing router tables unchanged.
- `uv run ruff check src/superclaude/pr_submit/conflicts.py tests/pr_submit/test_conflicts_core.py` reports no findings.

## Task 4: Pin the late pass to the existing router and leave the classifier alone

Depends on: Task 3

Add tests only; no source change.

- In `tests/pr_submit/test_conflicts_core.py` add a test `test_late_pass_reuses_the_wave8a_router` driving `conflict_action(hook="wave8a", ...)` with `github_conflicting=True` for the late pass: L3 Tier 1 with `prior_conflict_cycles=0` gives `resolve_push` with `push_kind="sync"`; the same with `prior_conflict_cycles=1` gives a halt with reason `sync_cap` and `skip_ci`; Tier 2 gives `late_conflict`; Tier 0 gives `github_disagrees`; L1 gives `propose`; L2 gives `resolve_local`; entering outcomes `halt_max_rounds` and `no_response` keep the terminal status (action `report`).
- In `tests/pr_submit/test_ci_classify.py` add the payload-shape tests of requirements FR-25: a payload that carries `merge_state` classifies exactly like the same payload without it (pending, all-pass, fail, empty with `expect_checks` true and false, stale head), and `classify_checks` still returns `polling` for `state: polling` with no checks when `merge_state` is conflicting (the trigger is not the classifier's job).

Acceptance criteria:
- `uv run pytest tests/pr_submit/test_conflicts_core.py tests/pr_submit/test_ci_classify.py -q` passes, with every pre-existing test in both files unchanged.
- The late-pass test asserts the six router outcomes named above by `(action, reason, status, skip_ci)` values.

## Phase 3: Wave 8 and Wave 8a protocol text

## Task 5: Describe the late second Wave 8a pass in `SKILL.md`

Depends on: Task 1, Task 3

Edit `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md`, the Wave 8 bullet and the Wave 8a bullet.

- Wave 8 bullet: append a sentence after the existing text (the whole existing text stays byte-identical, so fragments E9 of `test_conflict_sync_protocol.py` and the wait-only sentence pinned by `test_wait_only_sentences_name_the_one_sync_exception` keep passing). The sentence says: on every poll payload, before acting on its classification, evaluate `superclaude.pr_submit.conflicts.late_conflict_trigger(payload)`; when true, run Wave 8a once more with the same entering outcome; the pass is limited by `conflict_action` (Tier 0 and Tier 1 only; a spent `SYNC_CAP = 1` ends `terminal_halted` with reason `sync_cap`; a late Tier 2 ends `terminal_halted` with reason `late_conflict`); after a pushed sync the CI wait continues on the new head with `expect_checks`; every other result ends the CI wait with the status `conflict_action` returns; no round, no re-trigger, no reply, no resolve. The late pass runs at most once per run: the SKILL keeps a run-local "late pass done" flag that is set when the pass starts and is not persisted (a `--resume` may run one more late pass, still bounded by `SYNC_CAP` for pushes). Wave 8a re-reads `mergeable` itself, so a stale `CONFLICTING` reading in the payload that Wave 8a does not confirm (hint `clean`, `behind` or `blocked`) ends the late pass with no action and the CI wait goes on, and the trigger is not evaluated again.
- Wave 8a bullet: replace the closing clause "(late re-sync: #361)" with a pointer that the Wave 8 late trigger re-enters this step; the rest of the bullet is unchanged.
- Update `tests/pr_submit/test_conflict_sync_protocol.py`: the E10 fragment now ends with the new clause; add a new pin (E13) for the Wave 8 late-trigger sentence. E9 stays byte-identical.
- Update `tests/skills/test_worker_contract.py`: replace the inventory row keyed to the old Wave 8a `SKILL.md` line (the row whose key line begins `- **Wave 8a (L1+`) with a row for the new line, same classification and reason text, and add a row for the changed Wave 8 bullet only if `test_every_write_verb_hit_is_classified` reports one (today no row is keyed to the Wave 8 bullet).

Acceptance criteria:
- `rg -n "late re-sync: #361" src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` finds nothing, and `rg -n "late_conflict_trigger" src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` finds the new sentence.
- The new Wave 8 sentence states the once-per-run rule, and the new E13 pin asserts the words "at most once per run".
- `uv run pytest tests/pr_submit/test_conflict_sync_protocol.py tests/pr_submit/test_static_grep.py tests/skills/test_worker_contract.py tests/pr_submit/test_skill_parse.py -q` passes.

## Phase 4: Supporting protocol refs

## Task 6: Document the payload and the trigger in `refs/ci-poll.md`

Depends on: Task 1, Task 5

Edit `src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md`.

- In "Poll surfaces", add `mergeable,mergeStateStatus` to the documented `gh pr view` field list and document the `merge_state` object (shape, empty strings when unavailable, appended after `checks`).
- Add a section "Late conflict trigger (P3)" after "Wave 8 entry": the trigger is `late_conflict_trigger(payload)` on every poll; it fires for a payload that carries a conflicting state and for a wait stuck at `polling` with no checks; it never changes `classify_checks`; `UNKNOWN` or missing values never fire it. The `pr_conflicting` skip sentence stays and is reconciled with the new section.
- Keep the wait-only sentence pinned at `test_wait_only_sentences_name_the_one_sync_exception` byte-identical.
- Update the `tests/skills/test_worker_contract.py` inventory row keyed to the old `gh pr view <N> --repo <owner/repo> --json number,url,headRefOid` line of this ref.

Acceptance criteria:
- `uv run pytest tests/pr_submit/test_static_grep.py tests/skills/test_worker_contract.py tests/pr_submit/test_conflict_sync_protocol.py -q` passes.
- A new assertion in `tests/pr_submit/test_static_grep.py` pins the documented `merge_state` shape and the words "Late conflict trigger" in `refs/ci-poll.md`.

## Task 7: Reconcile `refs/conflict-mechanical.md` with the late pass

Depends on: Task 5

Edit `src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md`.

- Section 8 "After the push", the "End of the CI wait" bullet: keep the final `mergeable` re-read and its `late_conflict` halt as the backstop, and replace "late re-sync is #361" with a pointer to the Wave 8 late trigger.
- Halt-reason table, the `late_conflict` row: replace "Late re-sync is #361." with text saying a Tier 1 conflict seen during the CI wait gets the one remaining sync under `SYNC_CAP`, and only a Tier 2 conflict or a re-read after the cap halts here.
- Add one paragraph to section 1 ("When this ref applies") stating that the late trigger re-enters the `wave8a` hook (same cycle-id scheme, `conflict_cycle_id` continues from `sync_cycles`, `--resume` restarts it like any open `wave8a` cycle) and introduces no hook label.
- Do not add or change any `gh` or `git` command line in this ref (so no inventory row changes); prohibited-operation scans (`FR-21`) must still pass.

Acceptance criteria:
- `rg -n "#361" src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md` finds nothing.
- `uv run pytest tests/pr_submit/test_conflict_sync_protocol.py tests/pr_submit/test_static_grep.py tests/skills/test_worker_contract.py -q` passes, including `MECHANICAL_PINS` and the prohibited-operation scan.

## Task 8: Add the late pass to `refs/state-machine.md` section 5.2d

Depends on: Task 5

Edit `src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md`, section 5.2d: add one sentence to the Tier 1 bullet saying the sync can also run once from the Wave 8 late trigger when no sync landed earlier, still with no FSM edge, no round and no re-trigger. Do not change the wait-only sentence pinned by `test_wait_only_sentences_name_the_one_sync_exception` and add no `git` or `gh` token.

Acceptance criteria:
- `uv run pytest tests/pr_submit/test_static_grep.py tests/pr_submit/test_autonomy_gates.py tests/pr_submit/test_conflict_sync_protocol.py -q` passes.
- The edited section still states `SYNC_CAP = 1` and that the sync counts in `sync_push_count`, never in `push_count`.

## Phase 5: User-facing docs

## Task 9: Update the command summary and the user guides

Depends on: Task 5

Edit `src/superclaude/commands/pr-submit.md` (the "Merge-conflict handling" paragraph at the sentence "There is at most one conflict cycle per run across both resolving tiers. Late text conflicts halt..."), `docs/user-guide/commands.md` and `docs/user-guide/flags.md` (the paragraphs ending "late text conflicts halt").

- Keep the phrases pinned by `test_user_guides_document_conflict_cap_and_limits` and `test_command_summarizes_conflict_protocol_without_replacing_activation` ("at most one conflict cycle per run", "late text conflicts halt", "two remaining", "eight text-conflict files", "not a sandbox", "no review round", and the others listed there).
- Add one sentence to each: a conflict that first appears while the CI wait is running gets one more Tier 1 sync when no sync landed earlier in the run; a late text (Tier 2) conflict, or a second conflict after the cap, halts.

Acceptance criteria:
- `uv run pytest tests/pr_submit/test_conflict_sync_protocol.py -q` passes.
- Each of the three files contains the new sentence (checked with `rg -n "CI wait" <file>` showing it) and the previous pinned phrases are still present.

## Phase 6: Release notes and final sync

## Task 10: Add the changelog entry and sync the dev copies

Depends on: Task 2, Task 4, Task 5, Task 6, Task 7, Task 8, Task 9

Edit `CHANGELOG.md`: under `## [Unreleased]` add a "pr-submit late conflict re-sync (P3, #361)" entry under `#### Added` or the section the file already uses for features, stating the `merge_state` poll field, the second Wave 8a pass limits (Tier 0 and Tier 1, `SYNC_CAP = 1`, late Tier 2 halts `late_conflict`), and that the real-run go/no-go gate is still open. Edit the earlier sentence "Late re-sync during the CI wait is #361." so it no longer reads as future work. Then run `make sync-dev`.

Acceptance criteria:
- `make sync-dev` succeeds and `make verify-sync` passes.
- `uv run pytest tests/pr_submit tests/skills/test_worker_contract.py tests/unit/test_cli_install.py -q` passes, and `make lint` reports no findings.
- `git diff --name-only` (tracked files modified in the working tree) lists only paths under `src/superclaude/`, `tests/`, `docs/user-guide/` and `CHANGELOG.md`, and `git diff --cached --name-only` lists no `.claude/` path.
