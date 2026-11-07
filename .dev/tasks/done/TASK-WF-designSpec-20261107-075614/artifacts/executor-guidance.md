# Executor guidance for plan TASK-WF-designSpec-20261107-075614 (owner decision A, 2026-11-07)

Source: advisory review 3 of this plan, report `.dev/reflect/pre-designSpec-20261107075755/REPORT.md`. The coordinator accepted option A: build this plan now, close the one blocking finding during the build, apply the low notes as guidance, and record both in the final report. The plan file is not edited.

## Blocking finding R1-1 (closed during the build)

- Task 3 fold: for every `settled(..., skipped, <cause>)` event the fold copies the event's `cause` into `disabled_cause` (so `user_override` and `already_draft` both set it; `not_applied` is handled by its own row and does not set it).
- Task 3 tests: a fold case that `settled(any, skipped, user_override)` gives `DISABLED`, `owned_draft` false and `disabled_cause == "user_override"`; a case that `guard_status(fold_draft_guard(events), mode, ordinal)` returns `"user_override"` for that log (fold output fed into `guard_status`, not a hand-built dict).
- Task 11 external-toggle scenario also asserts the `user_override` status from the real `RunLog`.

## Low notes (apply while writing the code and tests)

- Task 4 resume row 4 re-entry: a published cycle passes at least 1 as `applied_edits`; test `RELEASE(pushed)` and a HOLD on a moved head (`head_sha != target_sha`).
- Task 4 `classify_toggles`: add observed equal to `run_toggles` with `failed_mutations=1` (ok), observed `run_toggles + 2` with `failed_mutations=1` (foreign), and a pending phase with either draft flag (ok).
- Task 4: assert that `engage_decision` notes carry `auto_merge_armed`.
- Task 7: skip guard when `jq` or `bash` is missing, like `tests/pr_submit/test_conflict_scripts.py`; the static repo-scope scan reuses `_command_lines` and `_repo_scoped` from `tests/pr_submit/test_static_grep.py` and the fake-`gh` runs always pass `--repo`.
- Tasks 7, 8, 12: classification keys use the verb text as the scanner joins it (`gh pr+gh api` when a line has both); every line `WRITE_VERB_RE` matches needs an entry, git write verbs included.
- Tasks 9 and 10: the new Wave bullets are new physical lines (the existing Wave 0, 3, 6 and 8 lines stay byte-identical because they are exact classification keys). The Wave 0 negative checks target the exact gating phrases on the loading sentence (`L3 only`, `only at L3`, `--merge-guard draft`); the `at L3 with --merge-guard off` sentence is allowed to say L3. Also assert the bullet names "when the run log already holds guard events" and "before any edit, release or re-trigger". The pinned S5a and Wave 6 pre-push sentences are compared as full-sentence string constants.
- Task 10: the Wave 3 bullet says the kind is `ci` for a CI-fix cycle and defers to the Wave 8 bullet; a test asserts the Wave 8 text contains "kind `ci`" and `ci-<n>`; Task 11 adds a `ci` cycle that engages once with id `ci-1`.
- Task 8 and Task 11: the Pre-push section applies whatever the guard phase is, including `DISABLED`; add a scenario with a `DISABLED` guard and a merged PR that halts `pr_not_open`.
- Task 12: the section heading is "Merge guard"; verify it with a case-insensitive grep or the protocol test, not the `merge-guard` grep alone.
- Tasks 8, 9, 10 (found in Task 4): `resume_decision` takes keyword parameters beyond the plan's list: `applied_edits` (default 1), `target_sha` (default None) and `cycle_id` (default None). Row 4 re-enters `release_decision`, whose row 8 needs `read.head_sha == target_sha`, so the Resume text in `refs/merge-guard.md` and the Wave 0 bullet must pass the held cycle's `target_sha` (from its `push_completed` event or the recovered push record); without it row 4 always holds with `head_mismatch`. `read` may be `None` (the live read failed): rows 3, 4 and 8 treat it as unreadable and hold.
- Tasks 8 to 13 (found in Tasks 1 and 3): the `FOLDER`, `PKG` and `DOC` cards in `./artifacts/pre-build-gate.md` list text rules that reach new files (for example the severity-wording tests over every tracked file under `src/`, the model-id and Tavily text tests over `src/` and `docs/`, the retired-link test over every `.md`); read them before writing protocol, command or guide text.
- Task 13 / Task 1: the full suite takes about 10 minutes (run it in the background). On the unchanged base it gave 16916 passed, 25 failed, 16 errors; most failures are `.claude/` mirror tests, so run `make sync-dev` before judging them, and record the base ids after that sync as well.
