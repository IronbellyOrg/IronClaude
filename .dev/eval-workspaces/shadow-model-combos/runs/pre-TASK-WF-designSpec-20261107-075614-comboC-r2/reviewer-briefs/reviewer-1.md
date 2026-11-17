# Reviewer 1 brief (persona: analyzer)

Task: audit the PLAN against its driving SPEC before any execution (UC-1 pre-execution reflection). Find where the plan contradicts the spec, omits a spec requirement, or carries an acceptance criterion that cannot fail or cannot pass. Audit only the evidence supplied here plus what you can Read, Grep or Glob. Return your card as text; do not edit anything.

Plan: .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md
Spec: .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md

## T1 card excerpt

Orchestrator Tier 1 card (verbatim lines, persona slice). Full card: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/eval-workspaces/shadow-model-combos/runs/pre-TASK-WF-designSpec-20261107-075614-comboC-r2/t1-card.md

# Tier 1 reflection card (UC-1, pre-execution)

Spec: `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md` (378 lines, design spec v3 for the pr-submit merge guard).
Plan: `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md` (200 lines, 13 tasks, 5 phases).

- **T1-F1 (MAJOR, contradiction).** Task 9 requires the Wave 0 bullet to say that "at L3 with `--merge-guard off`" the line is printed once (plan line 137), yet the same bullet must "carry no L3 or `draft` condition" and its criterion says the test "fails ... when it names an L3 or `draft` condition" (plan line 140). A bullet that satisfies the first sentence names L3. Source: spec line 59 and line 241 hold the same tension, so the plan copies it.
- **T1-F2 (MAJOR, missing-requirement).** The FR-16 retry (spec line 315: "one retry, `already_in_state` counts as confirmed, `release_pending`") has no decision-table row, no fold rule and no acceptance criterion. Task 8 puts "one retry" into the ref prose (plan line 124), and Task 11 only names `test_guard_release_failure_retries_once_and_reports` (plan line 169).
- **T1-F3 (MAJOR, missing-requirement).** No criterion checks that the guard, the push triad and `rereview_requested` share one `cycle_id` (spec line 251). Task 11's trace asserts event order only (plan line 170) and Task 8 only requires the ref to name the minting place (plan line 127).
- **T1-F5 (MAJOR, other).** `engage_decision` row 6 returns `HOLD(ownership_unproven)` and `settled(draft, failed)` leaves the phase at `RELEASE_PENDING` with `owned_draft` false (spec lines 138, 199). After a failed engage every later engage returns HOLD. Neither spec nor plan says whether edits continue on a HOLD at engage, so a non-draft PR could be edited. Task 4 and Task 8 test rows, not this consequence.

End your card with a ## Findings block holding one fenced findings-v2 block: JSON lines, one object per line, never a table. Fields: id (F1, F2, ...), severity (CRITICAL, MAJOR or MINOR), blocking (true or false; a MINOR finding is never blocking), category (one of contradiction, data-loss, missing-requirement, other, safety, unpassable-check), lens "reflect-pre", claim (one line, at most 300 characters), refs (requirement ids, may be empty) and citations (1 to 8 objects, each with role plan or spec, a repo-relative path, line_start, line_end and an optional quote). Example line: {"id":"F1","severity":"MAJOR","blocking":false,"category":"contradiction","lens":"reflect-pre","claim":"Task 3 says X but task 5 says Y.","refs":["R-1"],"citations":[{"role":"plan","path":"plan.md","line_start":10,"line_end":12}]}. After the block add a reviewer_model_self_report line stating the model you are running as in one line.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-13T04:06:00Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:12-27

```markdown
# Implement the /sc:pr-submit merge guard (issue #375)

Source: ./source.md
Goal: With `/sc:pr-submit --monitor 3`, a PR is turned into a draft as soon as a verified Medium-or-higher finding is routed to a fix, and is marked ready again only when that cycle's fix push is confirmed on the PR head (or a zero-edit cycle is proven), with every failure, override, crash, resume and exit path leaving the PR in a known, reported state.

## Constraints

- Edit canonical files under `src/superclaude/` only, then run `make sync-dev`; do not stage `.claude/` mirror files. Use UV for every Python command (`uv run pytest ...`, `uv run ruff ...`).
- The new pure module `src/superclaude/pr_submit/merge_guard.py` and every file already listed in `CORE_PURE_FILES` of `tests/pr_submit/test_static_grep.py` (including `refs/state-machine.md` and `refs/loop-guard.md`) must contain no whole word `gh` or `git` on any line, comments included. The module must not import `recovery` (an import cycle through `run_log`).
- Protocol and command text must not contain the string `src/superclaude`; `SKILL.md` must keep exactly one python code fence; edits to `SKILL.md` and `refs/state-machine.md` are additive sentences, bullets and rows placed after, never inside, the sentences pinned by `tests/pr_submit/test_static_grep.py` and `tests/pr_submit/test_conflict_sync_protocol.py`. A new `SKILL.md` line must not name `evidence-validator` or `conflict-intent.md` (a line-content test allows those words only on lines that also say "Tier 2") and must not use wording that the forbidden-force-push line test rejects; Task 1 lists the exact line-content rules before any edit.
- Every new line under `src/superclaude/skills/`, `src/superclaude/commands/` or `src/superclaude/agents/` that contains `gh pr`, `gh api` or a git write verb needs one entry in `WRITE_VERB_CLASSIFICATION` in `tests/skills/test_worker_contract.py` (key: repo-relative path, verb text, exact stripped line; category `never-worker` with the standard pr-submit reason text of the neighbouring entries). Add each entry last in the task that writes the file, because editing a classified line later makes the entry stale and fails `test_classification_table_has_no_stale_entries`; run `uv run pytest tests/skills/test_worker_contract.py -q` in that task.
- Cite tests and constants by symbol name (for example `_NEW_KEY_DEFAULTS`, `_RESOLUTION_SCRIPTS`, `CORE_PURE_FILES`, `WRITE_VERB_CLASSIFICATION`), never by line number, in plan text, task artifacts and the protocol prose this plan produces. Protocol prose carries no `file:NNN` pointers.
- No test or task may call GitHub. Script tests use a fake `gh` executable on `PATH`. The behaviour that needs a disposable fork PR (gates G1 live part, G2 live part, G4, G5 and G6 of ./source.md section 8) is recorded as OPEN and is a release gate, never claimed verified.
- Scope limits (non-goals of ./source.md): no labels, commit statuses or rulesets; ordinals 0 to 2 change only by one report line; conflict-merge cycles (Tier 1 and Tier 2) are never engaged; the guard is not held through re-review or CI; a second concurrent run on the same PR is unsupported.
- Owner decisions already accepted (listed in the ./source.md header and section 8) are fixed: draft not label; engage at the end of Wave 3; default on at `--monitor 3`; release on the confirmed push before replies and the re-trigger; unreadable timeline or unpublished exit keeps the PR draft; build now with no GitHub calls, release gate for G4 and G5.
- Run `make sync-dev` at the end of every task that edits a file under `src/superclaude/skills/` or `src/superclaude/commands/`, because the full test suite runs `make verify-sync` through `tests/cli/test_verify_sync_hooks.py`.
```

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:132-144

```markdown
## Task 9: Wire the Wave 0 resume and `off` hook, the flag row, the output row and the wave line into `SKILL.md`

Depends on: Task 6
Depends on: Task 8

Edit `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` additively, using the pins and line-content rules recorded in `./artifacts/pre-build-gate.md`: one new bullet under Wave 0, written as a flat line before the Wave 1 bullet, that applies at every ordinal and in both modes and carries no L3 or `draft` condition; it states that on `--resume`, or when the run log already holds guard events, the ref `refs/merge-guard.md` (Resume and Exit report) is loaded before Wave 1 and before any edit, release or re-trigger, and that at L3 with `--merge-guard off` the line "Remediation is unprotected: --merge-guard off." is printed once and no draft call is made. Add one `--merge-guard {draft,off}` row to the Required Input flag table beside `--conflict-max-tier`; one row `merge_guard` to the output table (values `off`, `released`, `held`, `user_override`, `unavailable`) that also carries the literal L2 line "PR #N is still mergeable; this run's fixes are local only." so a fresh L2 run prints it without loading the ref; and one line in the wave-structure list. No new python fence. Where a new line would contain `gh pr` or `gh api`, rephrase it (for example "print the clear command from the ref") so that no classification entry is needed; if one is unavoidable, add its `WRITE_VERB_CLASSIFICATION` entry as the last step. Extend `tests/pr_submit/test_merge_guard_protocol.py` with a test for the Wave 0 bullet (it names `--resume`, sits before the Wave 1 bullet, contains no `L3 only` or `draft` gate wording and contains the literal `off` line), one for the flag row, one for the output row including the literal L2 line, and one for the wave-structure line. Run `make sync-dev`.

Acceptance criteria:
- The Wave 0 test fails when the bullet is placed after the Wave 1 bullet, when it names an L3 or `draft` condition, or when the literal `off` line is missing, and passes on the real file.
- A test asserts the literal text "PR #N is still mergeable; this run's fixes are local only." is present in `SKILL.md` itself (not only in the ref), so a fresh L2 run needs no ref load.
- `uv run pytest tests/pr_submit/test_static_grep.py tests/pr_submit/test_conflict_sync_protocol.py tests/pr_submit/test_cosmos_protocol.py tests/pr_submit/test_codex_reviews.py tests/pr_submit/test_merge_guard_protocol.py tests/skills/test_worker_contract.py -q` passes with no edit to any existing test expectation other than those listed in Tasks 2, 5, 7 and 8.
- `SKILL.md` still has exactly one python code fence and no `src/superclaude` string, and the new lines contain neither `evidence-validator` nor `conflict-intent.md`.
- `make verify-sync` exits 0.
```

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:159-173

```markdown
## Task 11: Write the scenario tests over the run log

Depends on: Task 3
Depends on: Task 4
Depends on: Task 5
Depends on: Task 7

Create `tests/pr_submit/test_merge_guard_scenarios.py` with a small test driver that applies the pure decisions of `merge_guard.py`, appends events to a real `RunLog` in a temporary directory and runs `scripts/set-draft-state.sh` against a fake `gh`; it imports only the fake-`gh` helper or fixture from `tests/pr_submit/test_set_draft_state.py`, never a `test_*` function (pytest would collect it twice). Implement the twelve test names of ./source.md section 7 and the acceptance trace of section 5. Cover the cases of the section 5 table: engage failure halts before any edit, validation failure leaves phase `held`, zero-edit cycle releases with `no_edits` (including a zero-edit cycle after a fixing cycle), foreign toggle disables the guard and the run continues, crash between request and settle reconciles on resume (including `not_applied` followed by a normal re-engage, and a ready request settled `not_applied` that stays `HELD` and is released after the publication check), crash after a dangling `push_initiated` with branch strings produced by the real `detect_crash_window` and `resolve_crash_window` (`landed` releases, `not_landed` holds, `ambiguous` holds), crash after a normal `push_completed` (no dangling window, `published` true) releases before the re-trigger, merged PR halts `pr_not_open`, ordinals 0 to 2 and `off` make no call, an originally draft PR is never made ready, an engage, crash, resume with live draft true stays `held` and is released after the push, and a conflict-cycle id never engages.

Acceptance criteria:
- The test file defines `test_guard_modes_ordinals_and_resume_authority`, `test_attach_and_create_preserve_preexisting_draft`, `test_guard_engages_at_routed_finding_once_per_cycle`, `test_guard_releases_only_after_publication_or_zero_edit_proof`, `test_guard_holds_on_unpublished_or_uncertain_exits`, `test_guard_engage_failure_blocks_edits`, `test_guard_release_failure_retries_once_and_reports`, `test_guard_external_toggle_and_roundtrip_disable`, `test_guard_missing_timeline_or_ambiguous_intent_never_readies`, `test_guard_crash_boundaries_and_push_recovery_abc`, `test_guard_closed_merged_or_moved_head_forbids_mutation` and `test_guard_script_contract_scoping_and_legacy_fold` (the last asserts the legacy-log fold and the script scoping through shared helpers, with no imported `test_*` function).
- The acceptance-trace test asserts the exact event order `draft_guard_requested(draft)`, `draft_guard_settled(confirmed)`, `fix_applied`, `push_completed`, `draft_guard_requested(ready)`, `draft_guard_settled(confirmed)`, `rereview_requested` from `RunLog.read_events()` and asserts no `rereview_requested` appears before the release settle.
- The crash tests build the dangling window by appending a real `push_initiated` event and calling `detect_crash_window` and `resolve_crash_window`; none of them passes a hand-written branch string to `resume_decision`, and the normal-`push_completed` test asserts `detect_crash_window` returns `None` and `published` is true.
- Forbidden-call assertions: the fake `gh` log never contains `pr ready` without `--undo` for an originally draft PR and never contains any `pr ready` call at ordinal 2 or with `off`; after a `pr_not_open` halt the test asserts on `RunLog.read_events()` that no `push_initiated` or `push_completed` event follows the halt (the fake `gh` log cannot see a `git push` and is not used for this check).
- `uv run pytest tests/pr_submit -q` passes in full.
```

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:53-69

```markdown
## 3. Behaviour in one table

| Moment | Guard action |
|---|---|
| Ordinal < 3, `--merge-guard off`, or a conflict-merge cycle | Nothing mutates. A held guard found in the log is reported with the clear command. |
| `--resume` at any ordinal and in either mode, or a run log that already holds guard events | Wave 0 loads the ref (Resume and Exit report) before Wave 1: unsettled requests are reconciled before any edit, release or re-trigger; a held guard is reported with the clear command. |
| `--merge-guard off` at L3 | Wave 0 prints once: "Remediation is unprotected: --merge-guard off." No draft call is made. |
| A fresh `--monitor 2` run (no `--resume`, no guard events) that applies fixes and halts before the push | The final report prints "PR #N is still mergeable; this run's fixes are local only." The line is written in the SKILL.md output table, which every run loads, not only in the guard ref. |
| End of Wave 3 at L3: at least one verified, Medium-or-higher finding routed to a fix (review-fix cycle, or CI-fix cycle from Wave 8) | Read, decide, request, `--to draft`, settle. Print the clear command once. |
| First engage of the run finds the PR already draft | Settle `skipped/already_draft`, phase `disabled`, never mutate. |
| Diagnosis ends with no edit (`applied_edits == 0`) | Release, cause `no_edits`. |
| Pre-push head guard (Wave 6) | Script `--read` must show `state == OPEN`; otherwise halt `pr_not_open`, push nothing. |
| After `push_completed`, head equals `target_sha` | Release, cause `pushed`, before reply, resolve and the S5a re-trigger. |
| Foreign toggle seen at a checkpoint | Settle `skipped/user_override`, phase `disabled`, no more draft calls, keep pushing, report. |
| Timeline unreadable at a checkpoint after engage | Do not release; report `held (timeline unreadable)`; keep pushing. |
| Engage fails, or timeline unreadable at engage | Halt before any edit: `terminal_halted`, reason `draft_guard_unavailable`. |
| Any exit after engage with no confirmed push and no zero-edit proof | PR stays draft; report `held` with the clear command. |
```

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:129-171

```markdown
`engage_decision`, first matching row wins:

| # | Condition | Decision |
|---|---|---|
| 1 | `mode == OFF`, or `ordinal < 3`, or `is_conflict_cycle(cycle_id)` | `NOOP` (reason `mode_off`, `ordinal`, `conflict_cycle`) |
| 2 | `guard.phase == DISABLED` | `NOOP(disabled)` |
| 3 | `not read.ok` | `HALT_UNAVAILABLE(read_failed)` |
| 4 | `read.state != "OPEN"` | `HALT_PR_NOT_OPEN` |
| 5 | `guard.phase == RELEASE_PENDING` and `guard.owned_draft` | `RETRY_RELEASE` (release first, then re-decide) |
| 6 | `guard.phase == RELEASE_PENDING` and not `owned_draft` | `HOLD(ownership_unproven)` |
| 7 | `guard.phase == HELD` | `NOOP(already_held)` |
| 8 | `not read.complete` or `read.transitions is None` | `HALT_UNAVAILABLE(timeline_unreadable)` |
| 9 | `guard` exists and `classify_toggles == "foreign"` | `SKIP_USER_OVERRIDE` |
| 10 | `guard is None` and `read.is_draft` | `SKIP_ALREADY_DRAFT` |
| 11 | otherwise | `ENGAGE`; `notes` carries `auto_merge_armed` when set |

`release_decision`, first matching row wins:

| # | Condition | Decision |
|---|---|---|
| 1 | `mode == OFF`, `ordinal < 3`, or conflict cycle | `NOOP` |
| 2 | `guard is None` or `guard.phase not in (HELD, RELEASE_PENDING)` | `NOOP(not_held)` |
| 3 | `not read.ok` | `HOLD(read_failed)` |
| 4 | `read.state != "OPEN"` | `HALT_PR_NOT_OPEN` |
| 5 | `classify_toggles == "unreadable"` | `HOLD(timeline_unreadable)` |
| 6 | `classify_toggles == "foreign"` | `SKIP_USER_OVERRIDE` |
| 7 | `applied_edits == 0` | `RELEASE(cause=no_edits)` |
| 8 | `push_completed` and `read.head_sha == target_sha` | `RELEASE(cause=pushed)` |
| 9 | otherwise | `HOLD(head_mismatch or push_not_completed)` |

`resume_decision`, first matching row wins:

| # | Condition | Decision |
|---|---|---|
| 1 | `guard is None` | `NOOP` |
| 2 | `(ordinal < 3 or mode == OFF)` and phase not in (`RELEASED`, `DISABLED`) | `REPORT_HELD` (no mutation; prints the clear command) |
| 3 | `pending` non-empty | `RECONCILE`, with `reason` one of `resume_reconciled`, `not_applied`, `ambiguous`: live draft state and `classify_toggles` decide; live state matching the request's direction and `observed == run_toggles + 1` settles `confirmed, changed: true, cause: resume_reconciled`; live state not matching settles `skipped, cause: not_applied`; anything else is `ambiguous` and holds. Each reason has its own test. |
| 4 | phase `HELD` and (`dangling_branch == "landed"` or `published`) | re-enter `release_decision` with `push_completed=True` (`landed` is a push recovery just completed; `published` is a push that completed normally before the crash) |
| 5 | `dangling_branch == "not_landed"` and phase `HELD` | `NOOP(held_through_redrive)` |
| 6 | `dangling_branch == "ambiguous"` | `HOLD(ambiguous_remote_tip)` |
| 7 | phase `RELEASE_PENDING` and `owned_draft` | `RETRY_RELEASE` |
| 8 | phase `RELEASE_PENDING` and not `owned_draft`, live draft | `HOLD(ownership_unproven)` |
| 9 | otherwise | `NOOP` |
```

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:195-208

```markdown
|---|---|
| `requested(to=draft)` | `phase = ENGAGE_PENDING`; remember the key as pending; first request sets `baseline` and `original_is_draft` |
| `requested(to=ready)` | `phase = RELEASE_PENDING`; remember the key |
| `settled(draft, confirmed, changed)` | `phase = HELD`, `owned_draft = True`, `run_toggles += 1` |
| `settled(draft, failed)` | `phase = RELEASE_PENDING`, `failed_mutations += 1`, `owned_draft` unchanged |
| `settled(draft, skipped, already_draft)` | `phase = DISABLED`, `disabled_cause = already_draft`; a first skip also sets `original_is_draft` |
| `settled(any direction, skipped, not_applied)` | the pending key is cleared and the phase returns to `phase_before_request`; `owned_draft` and the toggle counters are unchanged. For a draft request that was the first guard record, the whole record is erased (the fold returns `None`, including `baseline` and `original_is_draft`), so the next request is a first request again and takes a fresh baseline and a fresh `original_is_draft`; this is safe because `not_applied` means no toggle landed. For a ready request the phase returns to `HELD` (or `RELEASE_PENDING` when a failed release preceded it), and the next `release_decision` re-checks publication before a new request is made. It is NOT `DISABLED`, so a crash before the call does not leave later cycles unguarded. |
| `settled(draft, confirmed, not changed)` | `phase = HELD`, `owned_draft = True`, no toggle (a retry that finds the PR already draft after a call that failed on the client but landed) |
| `settled(ready, confirmed, changed)` | `phase = RELEASED`, `owned_draft = False`, `run_toggles += 1` |
| `settled(ready, confirmed, not changed)` | `phase = RELEASED`, `owned_draft = False`, no toggle |
| `settled(ready, failed)` | `phase = RELEASE_PENDING`, `failed_mutations += 1` |
| `settled(any, skipped, user_override)` | `phase = DISABLED`, `owned_draft = False` |

`unsettled` is the count of remembered keys with no settle. A corrupt line still raises, as it does today. `original_is_draft` is never read from GitHub after the first record, so a resumed run cannot mistake its own draft for an original one.
```

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:259-281

```markdown
Happy path, ordinal 3:

```text
W3 end : read -> engage_decision=ENGAGE -> requested(draft) fsync -> to draft -> settled(confirmed)
W4/W5  : diagnose, edit, validate               (PR is draft; clear command already printed)
W6     : fix commit -> pre-push guard (+ read.state == OPEN) -> push_decision -> push_initiated(fsync)
         -> push -> push_completed
         -> read -> release_decision=RELEASE(pushed) -> requested(ready) fsync -> to ready -> settled(confirmed)
         -> reply -> resolve -> S5a re-trigger (reviewers see a ready PR)
```

Acceptance trace (must appear in this order in the run log): `draft_guard_requested(draft)`, `draft_guard_settled(confirmed)`, `fix_applied`, `push_completed`, `draft_guard_requested(ready)`, `draft_guard_settled(confirmed)`, `rereview_requested`.

| Case | Trace |
|---|---|
| Engage fails | `requested(draft)` -> `--to draft` fails -> `settled(failed)` -> `terminal_halted(draft_guard_unavailable)`, no edit. Message names `--merge-guard off` and prints the clear command. |
| Validation fails after engage | `terminal_halted` or `VALIDATION_FAIL`; phase stays `HELD`; report `merge_guard: held` plus the clear command. |
| Zero-edit cycle | engage at W3 end, no edit, W6 blocks the push (INV-016 predicate 5), `release_decision=RELEASE(no_edits)`. |
| Foreign toggle | at release `classify_toggles == foreign` -> `settled(skipped, user_override)` -> phase `DISABLED`; the push and reply continue; report `user_override`. |
| Crash between request and settle | `--resume`: Wave 0 loads the ref, `pending_requests` is non-empty, `RECONCILE` runs with a live read before any edit. If the live PR is not draft, the request settles `skipped/not_applied`, the phase returns to `phase_before_request`, and the next cycle engages normally. |
| Crash after `push_initiated`, before `push_completed`, push landed | `detect_crash_window` finds the dangling push; recovery returns `landed` and synthesizes `push_completed`; `resume_decision` row 4 (`dangling_branch == "landed"`) releases first, then the S5a logic of `refs/review-retrigger.md` runs. `not_landed` keeps the PR draft (row 5); `ambiguous` holds (row 6). |
| Crash after a normal `push_completed`, before release | No dangling window (`detect_crash_window` returns `None`), so there is no branch. The SKILL passes `published = held_cycle_published(events, guard)`, which is true; row 4 releases first, then the S5a logic runs. Without `published` no row would match and the PR would stay draft. |
| PR merged while held | next checkpoint: `state != OPEN` -> halt `pr_not_open`, nothing pushed, report the local commit `<target_sha>`. |
```

## Coverage slice

Rows this reviewer owns: the 14 spec rows the deterministic match left unmapped, plus the decision-table and sequence rows.

| Requirement | Spec cite | Status | Best task (ratio) |
|---|---|---|---|
| INF-005: Rule: the core DECIDES and the SKILL performs, the same split as the p | source.md:51 | unmapped | Task 1 (0.5385) |
| INF-006: Nothing mutates. A held guard found in the log is reported with the cl | source.md:57 | unmapped | Task 8 (0.5556) |
| INF-015: Settle `skipped/user_override`, phase `disabled`, no more draft calls, | source.md:66 | unmapped | Task 3 (0.5455) |
| INF-024: whether written by the push triad or synthesized by recovery (`recover | source.md:108 | unmapped | Task 1 (0.375) |
| INF-025: a test imports both modules and asserts equality, because the core can | source.md:109 | unmapped | Task 3 (0.4545) |
| INF-028: `mode == OFF`, or `ordinal < 3`, or `is_conflict_cycle(cycle_id)` | source.md:133 | covered by Task 3 | Task 3 (1.0) |
| INF-029: `RETRY_RELEASE` (release first, then re-decide) | source.md:137 | covered by Task 1 | Task 1 (0.6) |
| INF-030: `HALT_UNAVAILABLE(timeline_unreadable)` | source.md:140 | unmapped | null (0.0) |
| INF-031: `ENGAGE`; `notes` carries `auto_merge_armed` when set | source.md:143 | covered by Task 4 | Task 4 (0.8) |
| INF-032: `push_completed` and `read.head_sha == target_sha` | source.md:156 | covered by Task 4 | Task 4 (0.75) |
| INF-033: `HOLD(head_mismatch or push_not_completed)` | source.md:157 | unmapped | Task 4 (0.3333) |
| INF-034: `(ordinal < 3 or mode == OFF)` and phase not in (`RELEASED`, `DISABLED | source.md:164 | covered by Task 3 | Task 3 (1.0) |
| INF-035: `RECONCILE`, with `reason` one of `resume_reconciled`, `not_applied`,  | source.md:165 | covered by Task 4 | Task 4 (1.0) |
| INF-036: re-enter `release_decision` with `push_completed=True` | source.md:166 | covered by Task 4 | Task 4 (1.0) |
| INF-044: Effective only at `--monitor 3`; accepted and inert below. | source.md:216 | unmapped | Task 12 (0.4) |
| INF-045: `RunConfig` and `run_skill` do not change (F5) | source.md:217 | unmapped | Task 6 (0.4) |
| INF-062: Acceptance trace (must appear in this order in the run log) | source.md:270 | covered by Task 11 | Task 11 (0.8333) |
| INF-063: Message names `--merge-guard off` and prints the clear command. | source.md:274 | covered by Task 8 | Task 8 (0.875) |
| INF-064: phase stays `HELD`; report `merge_guard: held` plus the clear command. | source.md:275 | covered by Task 8 | Task 8 (0.625) |
| INF-065: W6 blocks the push (INV-016 predicate 5), `release_decision=RELEASE(no | source.md:276 | unmapped | Task 4 (0.3333) |
| INF-066: `classify_toggles == foreign` -> `settled(skipped, user_override)` ->  | source.md:277 | unmapped | Task 3 (0.4545) |
| INF-067: the request settles `skipped/not_applied`, the phase returns to `phase | source.md:278 | covered by Task 3 | Task 3 (0.7273) |
| INF-068: `not_landed` keeps the PR draft (row 5); `ambiguous` holds (row 6). | source.md:279 | covered by Task 4 | Task 4 (0.8571) |
| INF-069: The SKILL passes `published = held_cycle_published(events, guard)`, wh | source.md:280 | covered by Task 3 | Task 3 (0.8) |
| INF-070: `state != OPEN` -> halt `pr_not_open`, nothing pushed, report the loca | source.md:281 | covered by Task 8 | Task 8 (0.9) |
| INF-073: Never stage `.claude/`. | source.md:301 | unmapped | Task 3 (0.3333) |
| INF-082: The protocol wiring covers the Wave 0 resume and `off` hook as well as | source.md:364 | unmapped | Task 9 (0.5833) |
| INF-083: Protocol prose written by the plan never carries `file:NNN` pointers | source.md:369 | unmapped | Task 8 (0.5556) |
