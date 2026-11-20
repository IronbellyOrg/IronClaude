---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-designSpec-20261107-072120
version: "1"
priority: Medium
created_date: "2026-11-07"
---

# Implement the /sc:pr-submit merge guard (issue #375)

Source: ./source.md
Goal: With `/sc:pr-submit --monitor 3`, a PR is turned into a draft as soon as a verified Medium-or-higher finding is routed to a fix, and is marked ready again only when that cycle's fix push is confirmed on the PR head (or a zero-edit cycle is proven), with every failure, override, crash and exit path leaving the PR in a known, reported state.

## Constraints

- Edit canonical files under `src/superclaude/` only, then run `make sync-dev`; do not stage `.claude/` mirror files. Use UV for every Python command (`uv run pytest ...`, `uv run ruff ...`).
- The new pure module `src/superclaude/pr_submit/merge_guard.py` and every file already in `CORE_PURE_FILES` of `tests/pr_submit/test_static_grep.py` (including `refs/state-machine.md`) must contain no whole word `gh` or `git` on any line, comments included.
- Protocol and command text must not contain the string `src/superclaude`; `SKILL.md` must keep exactly one python code fence; edits to `SKILL.md` and `refs/state-machine.md` are additive sentences, bullets and rows only, outside the sentences pinned by `tests/pr_submit/test_static_grep.py` and `tests/pr_submit/test_conflict_sync_protocol.py`.
- No test or task may call GitHub. Script tests use a fake `gh` executable on `PATH`. The behaviour that needs a disposable fork PR (gates G4 and G5 of ./source.md section 8) is recorded as OPEN, never claimed verified.
- Scope limits (non-goals of ./source.md): no labels, commit statuses or rulesets; ordinals 0 to 2 change only by one report line; conflict-merge cycles (Tier 1 and Tier 2) are never engaged; the guard is not held through re-review or CI; a second concurrent run on the same PR is unsupported.
- Owner decisions already accepted (listed in ./source.md header) are fixed: draft not label; engage at the end of Wave 3; default on at `--monitor 3`; release on the confirmed push before replies and the re-trigger; unreadable timeline or unpublished exit keeps the PR draft.

## Phase 1: Contracts and pure core

## Task 1: Write the pre-build gate record `./artifacts/pre-build-gate.md`

Create `./artifacts/pre-build-gate.md` in this package from ./source.md section 8 (gates G1 to G6 and open items O1 to O4). For O1, find in `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` (Wave 6, push triad text) and `refs/loop-guard.md` lines 119 to 120 where a fix or CI cycle's `cycle_id` is assigned today and whether any test under `tests/pr_submit/` pins a value. For O2, record how `scripts/...` paths appear in fenced commands of the refs and what `test_allowed_tools_cover_every_program` in `tests/pr_submit/test_conflict_sync_protocol.py` requires of a new script. For O3, grep `tests/pr_submit/` for exact-text pins on the SKILL.md Wave 3, Wave 6, Wave 8 sentences, the output table, the wave-structure list, `refs/state-machine.md` and `src/superclaude/commands/pr-submit.md`, and list each pin that the later additive edits must avoid. For O4, confirm the S5a re-trigger sentence in SKILL.md stays unchanged.

Acceptance criteria:
- `./artifacts/pre-build-gate.md` has one row each for G1 to G6 with a status: G1 to G3 `CONFIRMED` with the evidence named in ./source.md, G4 and G5 `OPEN (needs a disposable fork PR run by the owner)`, G6 `OPEN (script checks state first, so only the error text is affected)`.
- O1 to O4 each carry the finding with `file:line` references read in this task; O1 states a single place where the guard-enabled cycle id will be minted so the push triad and `rereview_requested` use the same id.
- No GitHub or network call is made; the file says which gates remain for the owner.

## Task 2: Add the two guard events to the closed event enum

Edit `src/superclaude/pr_submit/models.py`: add `DRAFT_GUARD_REQUESTED = "draft_guard_requested"` and `DRAFT_GUARD_SETTLED = "draft_guard_settled"` to `EventType` (a comment block like the conflict-cycle one), change the module docstring count at line 3 and the class docstring "EXACTLY 43 members" to 45 and name the new events. Edit the text in `src/superclaude/pr_submit/run_log.py` `RunLog.append` docstring that says "43 closed enum values" to 45. Update `tests/pr_submit/test_run_log.py` (the test at lines 171 to 175, renamed to describe 45 members and asserting both new values) and `tests/pr_submit/test_codex_reviews.py` (the assertion at line 441) to 45. Leave `tests/pr_submit/test_idempotency.py` (7 sets) unchanged.

Acceptance criteria:
- `uv run pytest tests/pr_submit/test_run_log.py tests/pr_submit/test_codex_reviews.py tests/pr_submit/test_idempotency.py -q` passes with `len(EventType) == 45` and the two new values asserted.
- `RunLog.append` accepts an event with `event_type: "draft_guard_requested"` and still rejects an unknown type with the updated count in the message.
- `grep -n "43" src/superclaude/pr_submit/models.py src/superclaude/pr_submit/run_log.py` shows no remaining claim that the enum has 43 members.

## Task 3: Create `merge_guard.py` types, cycle ids, fold and status

Depends on: Task 2

Create `src/superclaude/pr_submit/merge_guard.py` following ./source.md sections 4.1 and 4.2: `GuardMode`, `Direction`, `Phase`, `GuardAction`, `GuardRead`, `GuardDecision`; `fix_cycle_id(kind, n)` and `next_cycle_number(events, kind)` (section 4.6, never colliding with `CONFLICT_CYCLE_PREFIXES` from `src/superclaude/pr_submit/conflicts.py`); `fold_draft_guard(events)` implementing the full event-effect table of section 4.2 (fields `phase, cycle_id, original_is_draft, baseline, run_toggles, unsettled, failed_mutations, owned_draft, disabled_cause`, `None` when no guard record exists, `original_is_draft` taken only from the first guard record); `pending_requests(events)` matching requests to settles by `idempotency_key`; `guard_status(guard, mode, ordinal)` returning `off`, `released`, `held`, `user_override` or `unavailable`. No `gh` or `git` word anywhere in the file. Create `tests/pr_submit/test_merge_guard.py` with table tests for these functions.

Acceptance criteria:
- `fix_cycle_id("fix", 2) == "fix-2"`, `fix_cycle_id("ci", 1) == "ci-1"`, `ValueError` for kind `sync` and for `n == 0`, and `is_conflict_cycle(fix_cycle_id(...))` is false for both kinds; `next_cycle_number` returns 1 on an empty log and 3 after `fix-1` and `fix-2`.
- A parametrized fold test covers every row of the section 4.2 effect table, including `settled(ready, confirmed, not changed)` adding no toggle, `settled(draft, failed)` leaving `owned_draft` unchanged, a skip without a request setting `original_is_draft`, and a log with no guard events returning `None`.
- `pending_requests` returns exactly the requests whose key has no settle, with retries distinguished by the `:a<k>` suffix.
- `uv run pytest tests/pr_submit/test_merge_guard.py -q` passes and `uv run ruff check` and `uv run ruff format --check` are clean for both new files.

## Task 4: Add the toggle classifier and the three decision functions

Depends on: Task 3

In `src/superclaude/pr_submit/merge_guard.py` add `classify_toggles(guard, read)` (the exact rule of ./source.md section 4.1: `unreadable` for a failed, incomplete or short timeline, `foreign` when observed transitions exceed `run_toggles + unsettled + failed_mutations` or the live draft flag contradicts a `HELD` or `RELEASED` phase), `engage_decision(*, mode, ordinal, cycle_id, guard, read)` (all 11 rows, first match wins, `notes` carries `auto_merge_armed`), `release_decision(*, mode, ordinal, cycle_id, guard, read, applied_edits, target_sha, push_completed)` (all 9 rows) and `resume_decision(*, mode, ordinal, guard, read, pending, dangling_branch)` (all 9 rows). Extend `tests/pr_submit/test_merge_guard.py` with one parametrized case per table row, the ready-then-draft round trip, and a failed-on-client-but-landed mutation that must not classify as foreign.

Acceptance criteria:
- Each row of the three decision tables has a test that names the row number and asserts the returned `action`, `reason` and `cause`; the engage test at ordinal 2, with `mode=OFF`, and with cycle id `sync-1` and `conflict-1` all return `NOOP`.
- `classify_toggles` returns `unreadable` for `complete=False`, `transitions=None` and for observed below `run_toggles`, `foreign` for one extra transition and for a `HELD` phase with a ready PR, and `ok` when observed equals `run_toggles + failed_mutations`.
- `release_decision` returns `HOLD` for a head different from `target_sha`, `RELEASE(no_edits)` for `applied_edits == 0`, and `HALT_PR_NOT_OPEN` for a merged state; an originally draft PR (phase `DISABLED`) never yields `RELEASE` or `ENGAGE`.
- `uv run pytest tests/pr_submit/test_merge_guard.py -q` passes with ruff clean.

## Task 5: Fold the guard into the run log and export the public names

Depends on: Task 3

Edit `src/superclaude/pr_submit/run_log.py` `rebuild_state()` so `state["draft_guard"]` is `fold_draft_guard(events)` (default `None`, documented in the method docstring beside the #305 keys), importing from `src/superclaude/pr_submit/merge_guard.py`. Add the guard names to `src/superclaude/pr_submit/__init__.py` imports and `__all__`. Update `tests/pr_submit/test_run_log.py`: add `"draft_guard": None` to `_NEW_KEY_DEFAULTS` (line 312) and a test that a legacy log rebuilds every old key unchanged with `draft_guard` `None`, and that a log with a request and a confirmed settle rebuilds `phase: held`. Add `src/superclaude/pr_submit/merge_guard.py` to `CORE_PURE_FILES` in `tests/pr_submit/test_static_grep.py`.

Acceptance criteria:
- `uv run pytest tests/pr_submit/test_run_log.py tests/pr_submit/test_static_grep.py tests/pr_submit/test_idempotency.py -q` passes, including `test_tn50_core_pure_no_gh_git_tokens` over the new file and the exact key-set assertions at lines 403 to 404.
- `from superclaude.pr_submit import fold_draft_guard, engage_decision, release_decision, resume_decision, fix_cycle_id` works in a fresh interpreter run through `uv run python -c`.
- Rebuilding a log that holds `requested(draft)` then `settled(draft, confirmed, changed=True)` returns `state["draft_guard"]["phase"] == "held"` and `owned_draft` true; a log that ends after only the request returns `unsettled == 1`.

## Phase 2: Flag and script

## Task 6: Add the `--merge-guard` flag

Depends on: Task 5

Edit `src/superclaude/pr_submit/fsm.py` following ./source.md section 4.3: `DEFAULT_MERGE_GUARD = "draft"`, a `--merge-guard` argument with `dest="merge_guard"`, `choices=["draft", "off"]` placed beside `--conflict-max-tier`, `SkillArgs.merge_guard: str = DEFAULT_MERGE_GUARD`, and `parse_args` passing `ns.merge_guard`. Leave `RunConfig` and `run_skill` unchanged. Add a test beside `test_conflict_max_tier_default_and_bounds` in `tests/pr_submit/test_skill_parse.py`.

Acceptance criteria:
- `parse_args([]).merge_guard == "draft"`, `parse_args(["--merge-guard", "off"]).merge_guard == "off"`, `SkillArgs().merge_guard == "draft"`, and `--merge-guard label` exits with an argparse error (`SystemExit`).
- `fsm.py` still contains no whole word `gh` or `git` (static purity test passes) and every existing test in `tests/pr_submit/test_skill_parse.py` and `tests/pr_submit/test_autonomy_gates.py` passes unchanged.

## Task 7: Create the GitHub I/O script `set-draft-state.sh`

Create `src/superclaude/skills/sc-pr-submit-protocol/scripts/set-draft-state.sh` following ./source.md section 4.4 and modelled on `scripts/retrigger-review.sh` (same `die`, `--repo` resolution from the origin remote, numeric `--pr` check, exit 127 when `gh` or `jq` is missing, executable bit). Modes `--read` and `--to draft|ready` with the exact calls, the one-line JSON shapes and the exit codes 0, 1, 2, 127 of section 4.4; every `gh` call carries `--repo "$REPO"` or a `repos/${REPO}/...` path; the timeline count uses `gh api --paginate` with a `jq` filter on `convert_to_draft` and `ready_for_review` piped to `wc -l`; `--to` re-reads state first (non-`OPEN` gives `error:"not_open"`), is idempotent (`changed:false` when already in the target state) and verifies after the mutation (`verify_failed`). Create `tests/pr_submit/test_set_draft_state.py` using a fake `gh` on `PATH` that logs its arguments (the same fake-executable approach as `tests/pr_submit/test_conflict_scripts.py`). Add the script to `_RESOLUTION_SCRIPTS` in `tests/pr_submit/test_static_grep.py` (lines 480 to 483).

Acceptance criteria:
- Fake-`gh` tests assert: `--read` prints one JSON line with `ok`, `state`, `isDraft`, `headRefOid`, `autoMergeRequest`, `transitions`, `complete`; a failing timeline call prints `transitions: null` and `complete: false`; `--to draft` on a draft PR makes no `pr ready` call and prints `changed:false`; `--to ready` on a merged PR prints `ok:false` with `error:"not_open"`.
- Exit codes are asserted: 0 on success, 1 on a failing `gh` (JSON still printed with `ok:false`), 2 for a missing or non-numeric `--pr` and for an unknown argument, 127 with `gh` absent from `PATH`.
- The recorded fake-`gh` argument log shows `--repo` or a `repos/` path on every call, and the script passes the `_RESOLUTION_SCRIPTS` origin-URL resolution tests and the T-105 style repo-pin static check.
- `uv run pytest tests/pr_submit/test_set_draft_state.py tests/pr_submit/test_static_grep.py -q` passes.

## Phase 3: Protocol text

## Task 8: Write the protocol reference `refs/merge-guard.md`

Depends on: Task 4
Depends on: Task 7

Create `src/superclaude/skills/sc-pr-submit-protocol/refs/merge-guard.md` from ./source.md sections 3, 4.1, 4.5, 4.6 and 5, as protocol steps (read, decide with `superclaude.pr_submit.merge_guard`, append the `draft_guard_requested` event with fsync before the call, run `scripts/set-draft-state.sh`, append `draft_guard_settled`) for: Engage at the end of Wave 3 (L3, review-fix cycles and CI-fix cycles; mints the cycle id with `fix_cycle_id` and reuses it as the `cycle_id` of the push triad and of `rereview_requested`; prints the clear command `gh pr ready <N> --repo "$REPO"` once); Pre-push (the script `--read` must show `OPEN`, otherwise halt `pr_not_open`, push nothing, report the local commit); Release (after `push_completed`, head equals `target_sha`, or zero-edit proof, before reply, resolve and the S5a re-trigger; one retry; `already in target state` counts as confirmed); Foreign toggle and unreadable timeline handling; Exit report (the `merge_guard` field and the held-exit list of D7 with the clear command); Resume (`resume_decision` and the Branch A, B, C rows). Every fenced command line starts with `gh`, `git`, `uv`, `make`, `jq` or a `scripts/` path that exists; every `gh` line is repo-scoped; the text contains no `src/superclaude` string and no python fence.

Acceptance criteria:
- The ref has a section for each of Engage, Pre-push, Release, Exit report and Resume, and states the single place where the guard-enabled cycle id is minted, matching the finding recorded for O1 in `./artifacts/pre-build-gate.md`.
- A static test added in this task (in a new `tests/pr_submit/test_merge_guard_protocol.py`) asserts: the ref exists, its fenced commands pass the allowed-program rule, every `gh` line passes the repo-scope check used in `tests/pr_submit/test_static_grep.py`, `scripts/set-draft-state.sh` is a file, and the ref does not contain `src/superclaude`.
- The ref states that engage failure and an unreadable timeline at engage halt with `terminal_halted` reason `draft_guard_unavailable` before any edit, and that an exit with unpublished or uncertain work leaves the PR draft.

## Task 9: Wire the ref into `SKILL.md` and `refs/state-machine.md`

Depends on: Task 8

Edit `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` additively: one new bullet under each of Wave 3, Wave 6 and Wave 8 in the wave list that loads `refs/merge-guard.md` at L3 when `--merge-guard` is `draft` (new sentences placed after, not inside, the pinned Wave 3, Wave 4, Wave 6 and Wave 8 sentences found in Task 1 O3); one row `merge_guard` in the output table (values `off`, `released`, `held`, `user_override`, `unavailable`, plus the L2 line "PR #N is still mergeable; this run's fixes are local only."); one line in the wave-structure code list for the merge guard. Edit `src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md` with a short overlay note that guard phases are folded values, not `MonitorState` members, without the words `gh` or `git`. Extend `tests/pr_submit/test_merge_guard_protocol.py` with assertions for the three bullets, the output row and the overlay note.

Acceptance criteria:
- `uv run pytest tests/pr_submit/test_static_grep.py tests/pr_submit/test_conflict_sync_protocol.py tests/pr_submit/test_cosmos_protocol.py tests/pr_submit/test_codex_reviews.py tests/pr_submit/test_merge_guard_protocol.py -q` passes with no edit to any existing test expectation other than those listed in Tasks 2, 5 and 7.
- `SKILL.md` still has exactly one python code fence and no `src/superclaude` string; the S5a re-trigger sentence and the Wave 6 pre-push sentence are byte-identical to before.
- The Wave 6 bullet states that release happens before reply, resolve and the S5a re-trigger, and the Wave 3 bullet states that engage happens at the end of Wave 3.

## Phase 4: Scenario tests

## Task 10: Write the scenario tests over the run log

Depends on: Task 5
Depends on: Task 7

Create `tests/pr_submit/test_merge_guard_scenarios.py` with a small test driver that applies the pure decisions, appends events to a real `RunLog` in a temporary directory and runs `scripts/set-draft-state.sh` against a fake `gh` (reuse the fake from `tests/pr_submit/test_set_draft_state.py`). Implement the twelve test names listed in ./source.md section 7 that are not already fully covered by Tasks 3, 4 and 7, and the acceptance trace of section 5: the run log order `draft_guard_requested(draft)`, `draft_guard_settled(confirmed)`, `fix_applied`, `push_completed`, `draft_guard_requested(ready)`, `draft_guard_settled(confirmed)`, `rereview_requested`. Cover the cases of the section 5 table: engage failure halts before any edit, validation failure leaves phase `held`, zero-edit cycle releases with `no_edits`, foreign toggle disables the guard and the run continues, crash between request and settle reconciles on resume, crash after `push_completed` releases on Branch A and holds on Branch B and C, merged PR halts `pr_not_open`, ordinals 0 to 2 and `off` make no call, an originally draft PR is never made ready, an engage, crash, resume with live draft true stays `held` and is released after the push, and a conflict-cycle id never engages.

Acceptance criteria:
- The test file defines `test_guard_modes_ordinals_and_resume_authority`, `test_attach_and_create_preserve_preexisting_draft`, `test_guard_engages_at_routed_finding_once_per_cycle`, `test_guard_releases_only_after_publication_or_zero_edit_proof`, `test_guard_holds_on_unpublished_or_uncertain_exits`, `test_guard_engage_failure_blocks_edits`, `test_guard_release_failure_retries_once_and_reports`, `test_guard_external_toggle_and_roundtrip_disable`, `test_guard_missing_timeline_or_ambiguous_intent_never_readies`, `test_guard_crash_boundaries_and_push_recovery_abc`, `test_guard_closed_merged_or_moved_head_forbids_mutation` and `test_guard_script_contract_scoping_and_legacy_fold` (the last may import the Task 7 tests by reference rather than duplicate them).
- The acceptance-trace test asserts the exact event order above from `RunLog.read_events()` and asserts no `rereview_requested` appears before the release settle.
- Forbidden-call assertions: the fake `gh` log never contains `pr ready` (without `--undo`) for an originally draft PR, never contains any `pr ready` call at ordinal 2, and never contains a push-related call after a `pr_not_open` halt.
- `uv run pytest tests/pr_submit -q` passes in full.

## Phase 5: Command and user docs

## Task 11: Document the flag in the command file

Depends on: Task 6
Depends on: Task 8

Edit `src/superclaude/commands/pr-submit.md`: add `[--merge-guard {draft,off}]` to the `argument-hint` front matter line (after `--conflict-max-tier`), a row `--merge-guard {draft,off}` with default `draft` in the Options table (effective only at `--monitor 3`; `off` prints a warning that remediation is unprotected), and a short "Merge guard" section next to "Merge-conflict handling" covering: when the PR becomes a draft, when it becomes ready, the held outcome and the clear command, the unreadable-timeline rule, and that drafts and ready transitions may affect reviewers and workflows (OPEN gates G4 and G5, not claimed verified). The text must not contain `src/superclaude`. Extend `tests/pr_submit/test_merge_guard_protocol.py` with assertions for the flag row, the argument-hint entry and the new section.

Acceptance criteria:
- `grep -n "merge-guard" src/superclaude/commands/pr-submit.md` shows the argument-hint entry, the Options row and the section heading, and the section states default-on at monitor 3 and the exact clear command.
- `uv run pytest tests/pr_submit -q` passes, including the command-file checks in `tests/pr_submit/test_conflict_sync_protocol.py`.

## Task 12: Document the flag in the user guides and sync the copies

Depends on: Task 9
Depends on: Task 11

Edit `docs/user-guide/commands.md`: add `[--merge-guard {draft,off}]` to the usage line at line 490 and a paragraph after the "Merge conflicts" paragraph (line 493) describing the guard, its default, the held state and the clear command. Edit `docs/user-guide/flags.md`: add a `--merge-guard` row beside the `--conflict-max-tier` row (line 211) with values `draft` (default) and `off`. Then run `make sync-dev` so the `.claude/` development copies match `src/superclaude/`.

Acceptance criteria:
- `grep -n "merge-guard" docs/user-guide/commands.md docs/user-guide/flags.md` shows the usage entry, the paragraph and the flags row; the paragraph names the clear command `gh pr ready <N> --repo <REPO>`.
- `make verify-sync` exits 0, `make lint` exits 0, `uv run ruff format --check src/ tests/` exits 0, and `uv run pytest tests/pr_submit -q` passes.
- `git status --short` lists changes only under `src/superclaude/`, `tests/pr_submit/`, `docs/user-guide/`, `.dev/` and gitignored `.claude/` mirrors; no `.claude/` path other than `.claude/settings.json` is staged.
