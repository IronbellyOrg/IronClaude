# Reviewer 3 brief (persona: refactorer)

Task: audit the PLAN against its driving SPEC before any execution (UC-1 pre-execution reflection). Find where the plan contradicts the spec, omits a spec requirement, or carries an acceptance criterion that cannot fail or cannot pass. Audit only the evidence supplied here plus what you can Read, Grep or Glob. Return your card as text; do not edit anything.

Plan: .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md
Spec: .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md

## T1 card excerpt

Orchestrator Tier 1 card (verbatim lines, persona slice). Full card: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/eval-workspaces/shadow-model-combos/runs/pre-TASK-WF-designSpec-20261107-075614-comboC-r2/t1-card.md

# Tier 1 reflection card (UC-1, pre-execution)

Spec: `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md` (378 lines, design spec v3 for the pr-submit merge guard).
Plan: `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md` (200 lines, 13 tasks, 5 phases).

- **T1-F6 (MINOR, other).** Plan line 25 says the scope limits are "non-goals of ./source.md". source.md has no non-goals section; "no labels, commit statuses or rulesets" and "a second concurrent run ... is unsupported" appear nowhere in it (grep of the spec found only the word "label" in the owner-decision line 6).
- **T1-F8 (MINOR, other).** Task 13 says `git status --short` lists "gitignored `.claude/` mirrors" (plan line 200); git status never lists ignored files.
- **T1-F9 (MINOR, other).** `Phase` string values are never defined in Task 3 (spec line 80 lists names only); Task 5 pins lowercase strings (`held`, `engage_pending`) in its criteria (plan line 90).
## Grounding notes
- The feature is already present in this working tree (`src/superclaude/pr_submit/merge_guard.py`, `scripts/set-draft-state.sh`, `refs/merge-guard.md`, `EventType` has 45 members). Grounding therefore reads post-implementation code; every combo of the experiment sees the same tree.
- Held: all 12 test names of spec section 7 appear in Task 11; every file of spec section 6 has a task; Task 2 names the test in the repo (`test_eventtype_is_45_members_...` now).

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

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:283-301

```markdown
## 6. Files to change

| File | Kind | Notes |
|---|---|---|
| `src/superclaude/pr_submit/merge_guard.py` | new | section 4.1 |
| `src/superclaude/pr_submit/models.py` | edit | 2 members, docstring and count |
| `src/superclaude/pr_submit/run_log.py` | edit | `rebuild_state` key, append docstring count |
| `src/superclaude/pr_submit/fsm.py` | edit | flag, `SkillArgs`, `parse_args` |
| `src/superclaude/pr_submit/__init__.py` | edit | export the public guard names |
| `src/superclaude/skills/sc-pr-submit-protocol/scripts/set-draft-state.sh` | new | section 4.4 |
| `.../refs/merge-guard.md` | new | section 4.5 |
| `.../SKILL.md`, `.../refs/state-machine.md`, `.../refs/loop-guard.md` | edit | additive only (loop-guard: the 43 to 45 enumeration text) |
| `src/superclaude/commands/pr-submit.md` | edit | flag and section |
| `docs/user-guide/commands.md`, `docs/user-guide/flags.md` | edit | flag and paragraph |
| `tests/pr_submit/test_merge_guard.py`, `test_set_draft_state.py` | new | section 7 |
| `tests/skills/test_worker_contract.py` | edit | one `WRITE_VERB_CLASSIFICATION` entry per new hit line (section 4.7); added last in each task that writes a file with hits |
| `tests/pr_submit/test_run_log.py`, `test_codex_reviews.py`, `test_static_grep.py`, `test_skill_parse.py` | edit | count 43 to 45 at `test_run_log.py:171-175` and `test_codex_reviews.py:441`; `"draft_guard": None` at `test_run_log.py:312`; `merge_guard.py` into the zero-token file set; script lists only after checking each list's purpose; flag default and choices test mirroring `--conflict-max-tier` |

After editing under `src/superclaude/`: `make sync-dev`, then `make verify-sync`. Run `make sync-dev` at the end of every task that edits a file under `src/superclaude/skills/` or `src/superclaude/commands/`, because `tests/cli/test_verify_sync_hooks.py` runs `make verify-sync` inside the full suite; the final task also runs `uv run pytest tests/cli/test_verify_sync_hooks.py tests/unit/test_cli_install.py -q`. A repo-wide pin (F12) escaped two reviews because only `tests/pr_submit` was run, so the final task runs the FULL suite (`uv run pytest -q tests`) and compares its failures with the base-commit record. Record `make lint`, `uv run ruff format --check src/ tests/` and the full-suite result (`uv run pytest -q tests`: pass count and every failing test id) on the base commit before the first code edit (pre-existing failures are not this feature's). Never stage `.claude/`. Unchanged and must still pass: `test_idempotency.py:89` (7 sets), the one-python-fence tests, `test_conflict_sync_protocol.py:576` (no `src/superclaude` text in skill or command files).
```

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:358-378

```markdown
## 10. Plan authoring notes (for the workflow that builds the plan from this design)

These come from a review of the first plan built from this design; they are requirements on the plan, not on the code.

- Cite tests and constants by symbol name (for example `_NEW_KEY_DEFAULTS`, `_RESOLUTION_SCRIPTS`, the test that asserts the event count), never by bare line number: earlier tasks edit the same files and line numbers drift.
- Declare dependencies completely, one `Depends on:` line per dependency: a task depends on every earlier task whose output it imports or consumes (the run-log wiring task and the scenario-test task both need the decision functions; the protocol tasks need the pre-build record).
- The protocol wiring covers the Wave 0 resume and `off` hook as well as Waves 3, 6 and 8 (section 4.5), with a test for each bullet.
- Run `make sync-dev` at the end of each task that edits `src/superclaude/skills/` or `src/superclaude/commands/`, and run the sync-hook tests named in section 6 in the final task.
- The fold, `guard_status`, resume-reason and per-cycle `applied_edits` rules of sections 3 and 4.1 each get an acceptance criterion that a wrong implementation would fail.
- The pre-build record task states the release-gate decision of section 8 and records the base-commit lint result.
- Update the 43-member enumeration in `refs/loop-guard.md` in the event-enum task.
- Protocol prose written by the plan never carries `file:NNN` pointers and never contains the words `evidence-validator` or `conflict-intent.md` on a new SKILL.md line.

Added in v3 (from the review of the second plan):

- Classification entries (section 4.7): the task that writes `scripts/set-draft-state.sh`, the task that writes `refs/merge-guard.md`, the task that edits `src/superclaude/commands/pr-submit.md` and any task that adds a `SKILL.md` line with `gh pr` or `gh api` each ends with adding its `WRITE_VERB_CLASSIFICATION` entries (exact stripped line, category `never-worker`) and runs `uv run pytest tests/skills/test_worker_contract.py -q`. The final task runs the full suite and compares it with the base-commit record.
- The L2 line is written into the SKILL.md output table; its acceptance criterion is a test that the literal line is in `SKILL.md`, and a fresh L2 run must not depend on loading the ref.
- Resume: the plan passes `published` and the recovery branch strings of F13; the crash scenario tests derive branches from a real `RunLog` through `detect_crash_window` and `resolve_crash_window`, never by injecting `"A"`, `"B"` or `"C"`.
- Fold: the plan states that a settled `not_applied` of either direction returns to `phase_before_request` and that a first record erased by it makes the next request a first request again; the acceptance criteria test both directions and the fresh baseline.
- Test hygiene: scenario tests import only helpers and fixtures from `test_set_draft_state.py`, never `test_*` functions (pytest would collect them twice); "no push after a `pr_not_open` halt" is asserted on `RunLog.read_events()` (no `push_initiated` or `push_completed` after the halt), because the fake `gh` log cannot see a `git push`; the byte-identical checks for the pinned S5a and Wave 6 pre-push sentences compare against literal string constants taken from the existing pins, not against `git show HEAD:`; the repo-pin proof for the new script is the recorded fake-`gh` argument log plus a static scan inside `test_set_draft_state.py` that every `gh` line carries `--repo` or a `repos/` path (the `test_t105_runtime_repo_pin` test covers only the poll script).
- The Wave 3 and Wave 0 bullet acceptance criteria assert wording and position, not headings: the Wave 3 bullet names the routed-finding trigger and "once per cycle"; the Wave 0 bullet sits before the Wave 1 bullet and has no L3 or `draft` condition.
```

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:40-56

```markdown
## Task 2: Add the two guard events to the closed event enum and the enumeration texts

Depends on: Task 1

Edit `src/superclaude/pr_submit/models.py`: add `DRAFT_GUARD_REQUESTED = "draft_guard_requested"` and `DRAFT_GUARD_SETTLED = "draft_guard_settled"` to `EventType` (a comment block like the conflict-cycle one), and change the module docstring and the `EventType` class docstring from "exactly 43 members" to 45, naming the new events. Edit the `RunLog.append` docstring in `src/superclaude/pr_submit/run_log.py` that says "43 closed" to 45. Edit `src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md`: its heading "The 43 event types" and the sentence that says the enum has EXACTLY 43 members become 45 and name `draft_guard_requested` and `draft_guard_settled`, without the whole words `gh` or `git` (the file is in `CORE_PURE_FILES`). Update `tests/pr_submit/test_run_log.py` (the test `test_eventtype_is_43_members_with_silence_reviewer_and_conflict_events`: rename it to describe 45 members, assert both lengths are 45 and both new values are present) and the `len(EventType)` assertion in `tests/pr_submit/test_codex_reviews.py` to 45. Leave `tests/pr_submit/test_idempotency.py` (7 sets) unchanged. Run `make sync-dev`.

Acceptance criteria:
- `uv run pytest tests/pr_submit/test_run_log.py tests/pr_submit/test_codex_reviews.py tests/pr_submit/test_idempotency.py tests/pr_submit/test_static_grep.py -q` passes with `len(EventType) == 45` and the two new values asserted.
- `RunLog.append` accepts an event with `event_type: "draft_guard_requested"` and still rejects an unknown type, with the updated count in the error message.
- `grep -rn "43" src/superclaude/pr_submit/models.py src/superclaude/pr_submit/run_log.py src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md` shows no remaining claim that the enum has 43 members, and `refs/loop-guard.md` names both new event values.
- `make verify-sync` exits 0 after the sync.

## Task 3: Create `merge_guard.py` types, cycle ids, fold, pending matcher, published check and status mapping

Depends on: Task 2

Create `src/superclaude/pr_submit/merge_guard.py` following ./source.md sections 4.1, 4.2 and 4.6: `GuardMode`, `Direction`, `Phase`, `GuardAction`, `GuardRead`, `GuardDecision`; the string constants `BRANCH_LANDED = "landed"`, `BRANCH_NOT_LANDED = "not_landed"`, `BRANCH_AMBIGUOUS = "ambiguous"`; `fix_cycle_id(kind, n)` and `next_cycle_number(events, kind)` (never colliding with `CONFLICT_CYCLE_PREFIXES` from `src/superclaude/pr_submit/conflicts.py`); `fold_draft_guard(events)` implementing every row of the section 4.2 effect table (fields `phase, phase_before_request, cycle_id, original_is_draft, baseline, run_toggles, unsettled, failed_mutations, owned_draft, disabled_cause`; `None` when no guard record exists; `original_is_draft` taken only from the first guard record or a first skip, never from a later read); `pending_requests(events)` matching requests to settles by `idempotency_key`; `held_cycle_published(events, guard)` (true when a `push_completed` event, normal or recovered, carries the guard's `cycle_id`); `guard_status(guard, mode, ordinal)` implementing the first-match mapping of section 4.1 (`off`, `released`, `held`, `user_override`, `unavailable`). The module imports only `enum`, `dataclasses`, `re` and `is_conflict_cycle` from `.conflicts`, and contains no `gh` or `git` word on any line. Create `tests/pr_submit/test_merge_guard.py` with table tests for these functions.
```

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:146-156

```markdown
## Task 10: Wire the Wave 3, Wave 6 and Wave 8 bullets into `SKILL.md` and the overlay note into `refs/state-machine.md`

Depends on: Task 9

Edit `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` additively: one new bullet under each of Wave 3, Wave 6 and Wave 8 that loads `refs/merge-guard.md` only at L3 with `--merge-guard` `draft`, written as new sentences after, never inside, the pinned sentences. The Wave 3 bullet states that engage happens at the end of Wave 3 only when at least one verified finding of Medium severity or higher is routed to a fix, once per cycle id, and mints the cycle id; the Wave 6 bullet states that Pre-push runs at the pre-push head guard step before `push_decision` and that Release runs after `push_completed` and before reply, resolve and the S5a re-trigger; the Wave 8 bullet states that a CI-fix cycle engages with kind `ci` and releases after `push_completed` before the CI re-poll. The S5a re-trigger sentence and the Wave 6 pre-push sentence stay byte-identical. Edit `src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md` with a short overlay note that guard phases are folded values, not `MonitorState` members, without the words `gh` or `git` and outside the wait-only sentences pinned for that file. Avoid `gh pr` and `gh api` on new lines (refer to "the clear command from the ref"); add a `WRITE_VERB_CLASSIFICATION` entry as the last step for any new line that cannot avoid them. Extend `tests/pr_submit/test_merge_guard_protocol.py` with one test per bullet (each gated on L3 and `draft`) and one for the overlay note. Run `make sync-dev`.

Acceptance criteria:
- The Wave 3 bullet test asserts the sentence names the Medium-or-higher routed-finding trigger and "once per cycle" and fails when either phrase is deleted (an unconditional "engage at the end of Wave 3" does not pass); the Wave 6 test asserts the Pre-push sentence and the Release-before-reply-resolve-re-trigger order; the Wave 8 test asserts the CI-fix sentence; each test fails when its sentence is removed.
- The S5a re-trigger sentence and the Wave 6 pre-push sentence are asserted byte-identical by comparing the live text with string constants (the literal start text recorded in `./artifacts/pre-build-gate.md`, as the existing pins write them), not with `git show HEAD:`; `SKILL.md` has one python fence and no `src/superclaude` string; no new line contains `evidence-validator` or `conflict-intent.md`.
- `uv run pytest tests/pr_submit -q` and `uv run pytest tests/skills/test_worker_contract.py -q` pass and `make verify-sync` exits 0.

```

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:188-200

```markdown
## Task 13: Document the flag in the user guides, sync, and run the final checks

Depends on: Task 2
Depends on: Task 10
Depends on: Task 11
Depends on: Task 12

Edit `docs/user-guide/commands.md`: add `[--merge-guard {draft,off}]` to the `/sc:pr-submit` usage line and a paragraph after the "Merge conflicts" paragraph describing the guard, its default, the `held` state, the clear command `gh pr ready <N> --repo <REPO>` and that draft behaviour is unverified until the owner runs the disposable-PR gate. Edit `docs/user-guide/flags.md`: add a `--merge-guard` row beside the `--conflict-max-tier` row with values `draft` (default) and `off`. Then run `make sync-dev`, `make verify-sync`, `make lint`, `uv run ruff format --check src/ tests/`, the full suite `uv run pytest -q tests`, and `uv run pytest tests/cli/test_verify_sync_hooks.py tests/unit/test_cli_install.py -q`, and write the outputs, the full-suite pass count and every failing test id (compared with the base-commit record of Task 1) to `./artifacts/final-checks.md`.

Acceptance criteria:
- `grep -n "merge-guard" docs/user-guide/commands.md docs/user-guide/flags.md` shows the usage entry, the paragraph and the flags row; the paragraph names the clear command and the unverified-until-release-gate statement.
- `make verify-sync` exits 0, the full suite `uv run pytest -q tests` shows no failing test id that is absent from the base-commit record of Task 1, and `uv run pytest tests/cli/test_verify_sync_hooks.py tests/unit/test_cli_install.py -q` passes; `make lint` and `uv run ruff format --check src/ tests/` exit 0, or every remaining failure is listed in `./artifacts/final-checks.md` as present in the base-commit record of Task 1.
- `git status --short` lists changes only under `src/superclaude/`, `tests/`, `docs/user-guide/`, `.dev/` and gitignored `.claude/` mirrors; no `.claude/` path other than `.claude/settings.json` is staged, and `.dev/tasks` is staged with `git add .dev/tasks`.
```

## Coverage slice

Rows from spec sections 4.5 to 10 (protocol, docs, test hygiene, plan-authoring notes).

| Requirement | Spec cite | Status | Best task (ratio) |
|---|---|---|---|
| INF-051: Loaded lazily at L3 Wave 3, Wave 6 and Wave 8. | source.md:240 | covered by Task 8 | Task 8 (0.75) |
| INF-052: The Wave 0 bullet is a flat line placed before the Wave 1 bullet and c | source.md:241 | covered by Task 9 | Task 9 (1.0) |
| INF-053: it must not contain the words `evidence-validator` or `conflict-intent | source.md:241 | covered by Task 9 | Task 9 (0.8571) |
| INF-054: No new python fence | source.md:241 | covered by Task 9 | Task 9 (1.0) |
| INF-055: update it to 45 and name `draft_guard_requested` and `draft_guard_sett | source.md:242 | covered by Task 2 | Task 2 (1.0) |
| INF-056: Respect the wait-only sentences pinned at `test_static_grep.py:791`. | source.md:243 | covered by Task 1 | Task 1 (0.7143) |
| INF-057: `--merge-guard {draft,off}` in the argument-hint and the Options table | source.md:244 | covered by Task 12 | Task 12 (1.0) |
| INF-058: A `held` report always carries the reason and `gh pr ready <N> --repo  | source.md:247 | covered by Task 8 | Task 8 (0.8889) |
| INF-059: uses the same id as the `cycle_id` of the push triad (`push_idempotenc | source.md:251 | covered by Task 8 | Task 8 (0.8571) |
| INF-060: With `--merge-guard off` nothing changes. | source.md:251 | covered by Task 8 | Task 8 (0.8) |
| INF-062: Acceptance trace (must appear in this order in the run log) | source.md:270 | covered by Task 11 | Task 11 (0.8333) |
| INF-063: Message names `--merge-guard off` and prints the clear command. | source.md:274 | covered by Task 8 | Task 8 (0.875) |
| INF-064: phase stays `HELD`; report `merge_guard: held` plus the clear command. | source.md:275 | covered by Task 8 | Task 8 (0.625) |
| INF-065: W6 blocks the push (INV-016 predicate 5), `release_decision=RELEASE(no | source.md:276 | unmapped | Task 4 (0.3333) |
| INF-066: `classify_toggles == foreign` -> `settled(skipped, user_override)` ->  | source.md:277 | unmapped | Task 3 (0.4545) |
| INF-067: the request settles `skipped/not_applied`, the phase returns to `phase | source.md:278 | covered by Task 3 | Task 3 (0.7273) |
| INF-068: `not_landed` keeps the PR draft (row 5); `ambiguous` holds (row 6). | source.md:279 | covered by Task 4 | Task 4 (0.8571) |
| INF-069: The SKILL passes `published = held_cycle_published(events, guard)`, wh | source.md:280 | covered by Task 3 | Task 3 (0.8) |
| INF-070: `state != OPEN` -> halt `pr_not_open`, nothing pushed, report the loca | source.md:281 | covered by Task 8 | Task 8 (0.9) |
| INF-071: count 43 to 45 at `test_run_log.py:171-175` and `test_codex_reviews.py | source.md:299 | covered by Task 2 | Task 2 (0.6667) |
| INF-072: Record `make lint`, `uv run ruff format --check src/ tests/` and the f | source.md:301 | covered by Task 1 | Task 1 (0.9231) |
| INF-073: Never stage `.claude/`. | source.md:301 | unmapped | Task 3 (0.3333) |
| INF-074: Unchanged and must still pass: `test_idempotency.py:89` (7 sets), the  | source.md:301 | covered by Task 2 | Task 2 (0.6364) |
| INF-075: never injected strings | source.md:318 | covered by Task 8 | Task 8 (0.6667) |
| INF-076: A static test asserts `merge_guard.py` has no `gh` or `git` word. | source.md:322 | covered by Task 3 | Task 3 (1.0) |
| INF-077: the script test for a missing `jq` (exit 127) | source.md:322 | covered by Task 7 | Task 7 (1.0) |
| INF-078: No task makes a live PR call, and the run that opens the PR must not e | source.md:326 | covered by Task 1 | Task 1 (0.8333) |
| INF-079: The user guide states that draft behaviour is unverified until then, a | source.md:326 | covered by Task 1 | Task 1 (1.0) |
| INF-081: one `Depends on:` line per dependency | source.md:363 | covered by Task 7 | Task 7 (0.75) |
| INF-082: The protocol wiring covers the Wave 0 resume and `off` hook as well as | source.md:364 | unmapped | Task 9 (0.5833) |
| INF-083: Protocol prose written by the plan never carries `file:NNN` pointers | source.md:369 | unmapped | Task 8 (0.5556) |
| INF-084: scenario tests import only helpers and fixtures from `test_set_draft_s | source.md:377 | covered by Task 11 | Task 11 (0.7) |
| INF-085: "no push after a `pr_not_open` halt" is asserted on `RunLog.read_event | source.md:377 | covered by Task 11 | Task 11 (0.8333) |
| INF-086: its acceptance criterion is a test that the literal line is in `SKILL. | source.md:374 | covered by Task 1 | Task 1 (0.8571) |
