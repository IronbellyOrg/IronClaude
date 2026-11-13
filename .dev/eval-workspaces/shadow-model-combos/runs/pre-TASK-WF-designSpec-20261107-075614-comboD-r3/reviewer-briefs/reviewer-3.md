# Reviewer brief 3: refactorer

## T1 card excerpt

- Spec: `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md` (378 lines)
- Plan: `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md` (200 lines, 13 tasks)
- Authored by: orchestrator inline (requirements-analyst fallback; `hypothesis_source: inline-fallback`)
- Card tier: 1. Mode: pre. Requirement extraction: Pass 1 found 0 labelled IDs; Pass 2 found 62 quote-pinned requirement rows (`INF-001..INF-062`).

## Structural and tech-debt (refactorer slice)

- Cycle-id minting appears in two tasks. Task 8 says the ref mints it "in the single place named by Task 1 O1" (plan line 124); Task 10 says the Wave 3 bullet "mints the cycle id" (plan line 150). Task 10's criteria do not require the two places to be the same (plan lines 153-155), against spec line 251 ("keep exactly one source for it").
- Dependencies: Task 10 depends only on Task 9 (which depends on Tasks 6 and 8); Task 11 depends on Tasks 3, 4, 5 and 7; Task 13 depends on Tasks 2, 10, 11 and 12. No cycle, and each task's inputs are covered, directly or through an earlier task.
- Sync cadence: every task that edits a file under `src/superclaude/skills/` or `src/superclaude/commands/` ends with `make sync-dev` (Tasks 2, 7, 8, 9, 10, 12), as spec line 301 requires.
- The scenario tests drive the pure core through a test-written driver (plan line 166), because the spec makes the SKILL the impure orchestrator (spec line 51). The shipped protocol wording is checked only by wording assertions (Tasks 8, 9, 10).

## Grounding results (Wave 1A, base commit e8db2fe6)

- All 14 code symbols and test names the plan cites exist at the base commit `e8db2fe6` (checked with `git grep`): `test_eventtype_is_43_members_with_silence_reviewer_and_conflict_events`, `_NEW_KEY_DEFAULTS`, `_RESOLUTION_SCRIPTS`, `CORE_PURE_FILES`, `WRITE_VERB_CLASSIFICATION`, `test_allowed_tools_cover_every_program`, `test_conflict_max_tier_default_and_bounds`, `test_tn50_core_pure_no_gh_git_tokens`, `test_t105_runtime_repo_pin`, `test_intent_and_validator_lines_say_tier_2`, `test_skill_forbids_force_push`, `detect_crash_window`, `resolve_crash_window`, `BRANCH_A_LANDED`.
- All 13 plan-cited files exist at the base commit. `plugins/superclaude/` holds 121 tracked files at the base commit and none concern `pr-submit`, so there is no plugin-mirror drift for this plan.
- Attribution: the feature this plan implements landed after the base commit (commit `0b8a5801d`, 2026-11-07, PR #428). Working-tree code is post-execution; judge the plan against the spec and the pre-existing code.
- Codegraph: index_state fresh (0 changes since index). Unused for definitions: the audited artifacts are documents.

End your card with a ## Findings block holding one fenced findings-v2 block: JSON lines, one object per line, never a table. Fields: id (F1, F2, ...), severity (CRITICAL, MAJOR or MINOR), blocking (true or false; a MINOR finding is never blocking), category (one of contradiction, data-loss, missing-requirement, other, safety, unpassable-check), lens "reflect-pre", claim (one line, at most 300 characters), refs (requirement ids, may be empty) and citations (1 to 8 objects, each with role plan or spec, a repo-relative path, line_start, line_end and an optional quote). Example line: {"id":"F1","severity":"MAJOR","blocking":false,"category":"contradiction","lens":"reflect-pre","claim":"Task 3 says X but task 5 says Y.","refs":["R-1"],"citations":[{"role":"plan","path":"plan.md","line_start":10,"line_end":12}]}. After the block add a reviewer_model_self_report line stating the model you are running as in one line.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-13T05:17:27Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:12-27

````markdown
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
````

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:238-255

````markdown
| File | Change |
|---|---|
| `skills/sc-pr-submit-protocol/refs/merge-guard.md` (new) | The procedure of sections 3 and 4.1 to 4.4 as protocol steps (read, decide, request, mutate, settle) for Engage, Pre-push, Release, Exit report and Resume. Loaded lazily at L3 Wave 3, Wave 6 and Wave 8. Uses `scripts/...` and `superclaude.pr_submit.merge_guard` names only. |
| `SKILL.md` | One short bullet under each of Wave 0, Wave 3, Wave 6 and Wave 8, written as new sentences after, never inside, the pinned sentences. The Wave 0 bullet applies at every ordinal and in both modes: on `--resume`, or when the run log holds guard events, it loads the ref (Resume and Exit report) before Wave 1 and before any edit, release or re-trigger; at L3 with `--merge-guard off` it prints the unprotected line once. The Wave 3, Wave 6 and Wave 8 bullets load the ref only at L3 with `draft`: the Wave 3 bullet states that engage happens at the end of Wave 3 only when at least one verified finding of Medium severity or higher is routed to a fix, and once per cycle id (it must not contain the words `evidence-validator` or `conflict-intent.md`, which a line-content test allows only on lines that also say "Tier 2"); the Wave 6 bullet states that Pre-push runs at the pre-push head guard step before `push_decision` and Release runs after `push_completed` before reply, resolve and the re-trigger; the Wave 8 bullet states that a CI-fix cycle engages with kind `ci` and releases after `push_completed` before the CI re-poll. Also one `--merge-guard {draft,off}` row in the Required Input flag table beside `--conflict-max-tier`; one row `merge_guard` in the output table, which also carries the literal L2 line "PR #N is still mergeable; this run's fixes are local only." so that a fresh L2 run prints it without loading the ref; one line in the wave structure list. The Wave 0 bullet is a flat line placed before the Wave 1 bullet and contains no L3 or `draft` condition (the Wave bullets are flat lines, not headings, so the test checks position and wording). No new python fence (the one-fence tests, `test_cosmos_protocol.py:34-44`, `test_codex_reviews.py:685-697`). |
| `refs/loop-guard.md` | Its event-type enumeration says the enum has 43 members; update it to 45 and name `draft_guard_requested` and `draft_guard_settled`, without the words `gh` or `git` (the file is in `CORE_PURE_FILES`). |
| `refs/state-machine.md` | Overlay note: the guard phases are fold values, not `MonitorState` members. Respect the wait-only sentences pinned at `test_static_grep.py:791`. |
| `commands/pr-submit.md` | `--merge-guard {draft,off}` in the argument-hint and the Options table; a short "Merge guard" section next to "Merge-conflict handling". |
| `docs/user-guide/commands.md`, `docs/user-guide/flags.md` | Flag row and a paragraph: what it does, the clear command, `held` meaning, default on. |

Output field `merge_guard`: `off`, `released`, `held`, `user_override`, `unavailable`. A `held` report always carries the reason and `gh pr ready <N> --repo <REPO>` (formatted by the SKILL, never by the core, because the core cannot contain `gh`). At L2 the final report adds: "PR #N is still mergeable; this run's fixes are local only." (the literal line lives in the SKILL.md output table; the ref's Exit report section refers to it and does not carry its own copy).

### 4.6 Cycle identity

`fix_cycle_id` gives guard-enabled cycles an explicit id: `fix-<n>` for review-fix cycles and `ci-<n>` for CI-fix cycles, `n` from `next_cycle_number`. The SKILL mints it at the end of Wave 3 and uses the same id as the `cycle_id` of the push triad (`push_idempotency_key`) and of `rereview_requested`, so the guard, the push and the re-trigger of one cycle share a key. With `--merge-guard off` nothing changes. The build must first confirm where the SKILL assigns a fix cycle's id today and keep exactly one source for it (open item O1).

### 4.7 Pinned write-verb classification (F12)

Every new line under `src/superclaude/skills/`, `src/superclaude/commands/` or `src/superclaude/agents/` that contains `gh pr`, `gh api` or a git write verb is a hit of `WRITE_VERB_RE` and needs one entry in `WRITE_VERB_CLASSIFICATION` in `tests/skills/test_worker_contract.py`: the key is the repo-relative path, the verb text (`gh pr`, `gh api`) and the exact stripped line; the value is category `never-worker` with the standard pr-submit reason text used by the neighbouring entries (the pr-submit monitor is on the never-as-worker list). The entries are added after the text of each file is final, as the last step of the task that writes the file, because a later edit of a classified line makes the entry stale and fails `test_classification_table_has_no_stale_entries`. The new files that carry hits are `scripts/set-draft-state.sh`, `refs/merge-guard.md`, `src/superclaude/commands/pr-submit.md` and any new `SKILL.md` line; a new line that does not need the words `gh pr` (for example "print the clear command from the ref") avoids an entry. The `read-only` category is not used for these calls (a `gh pr ready` mutation is never read-only). `docs/user-guide/` is outside the scanned roots.
````

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:358-378

````markdown
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
````

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|--------------------|---------|--------|-----------|
| INF-038: `SkillArgs.merge_guard: str = DEFAULT_MERGE_GUARD` | Task 6 | covered (containment 1.0) | source.md:215 |
| INF-039: `RunConfig` and `run_skill` do not change (F5) | - | lexically unmapped (best 0.5) | source.md:217 |
| INF-040: Exit codes: 0 success; 1 `gh` failure or failed verification | - | lexically unmapped (best 0.571) | source.md:234 |
| INF-041: `--to` is idempotent, so a retry or a resume re-issue is safe. | - | lexically unmapped (best 0.5) | source.md:234 |
| INF-042: A verification mismatch after a mutation is `ok:false, error:"verify_failed"` | Task 7 | covered (containment 0.857) | source.md:234 |
| INF-043: No new python fence | Task 9 | covered (containment 1.0) | source.md:241 |
| INF-044: update it to 45 and name `draft_guard_requested` and `draft_guard_settled` | Task 2 | covered (containment 1.0) | source.md:242 |
| INF-046: keep exactly one source for it (open item O1) | - | lexically unmapped (best 0.571) | source.md:251 |
| INF-047: needs one entry in `WRITE_VERB_CLASSIFICATION` | Task 9 | covered (containment 1.0) | source.md:255 |
| INF-048: The `read-only` category is not used for these calls | Task 1 | covered (containment 0.75) | source.md:255 |
| INF-051: Never stage `.claude/`. | - | lexically unmapped (best 0.333) | source.md:301 |
| INF-052: Run `make sync-dev` at the end of every task that edits a file under `src/superclaude/skills/` or `src/superclaude/commands/` | Task 8 | covered (containment 0.917) | source.md:301 |
| INF-056: Cite tests and constants by symbol name | Task 1 | covered (containment 0.6) | source.md:362 |
| INF-057: Declare dependencies completely, one `Depends on:` line per dependency | - | lexically unmapped (best 0.429) | source.md:363 |
| INF-058: Update the 43-member enumeration in `refs/loop-guard.md` in the event-enum task. | Task 2 | covered (containment 0.909) | source.md:368 |
| INF-059: Protocol prose written by the plan never carries `file:NNN` pointers | - | lexically unmapped (best 0.556) | source.md:369 |
| INF-061: the plan states that a settled `not_applied` of either direction returns to `phase_before_request` | Task 3 | covered (containment 0.625) | source.md:376 |
| INF-062: scenario tests import only helpers and fixtures from `test_set_draft_state.py`, never `test_*` functions | Task 11 | covered (containment 0.7) | source.md:377 |
