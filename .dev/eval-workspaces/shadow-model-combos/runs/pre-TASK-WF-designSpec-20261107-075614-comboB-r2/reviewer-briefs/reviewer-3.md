# Reviewer brief 3

## T1 card excerpt

### Findings

F1 MAJOR, contradiction (Task 7). The acceptance criterion asks that a static scan assert "every `gh` line carries `--repo` or a `repos/` path" (plan line 113) and also that the new script join `_RESOLUTION_SCRIPTS` and pass its tests (plan line 108, 113). Those tests require a line containing `gh repo view --json nameWithOwner` (tests/pr_submit/test_static_grep.py:549, inside the tests that use `_RESOLUTION_SCRIPTS` at :481), which carries neither `--repo` nor `repos/`; the model script has exactly that line (scripts/retrigger-review.sh:50). Both cannot hold unless the new scan reuses the existing `_repo_scoped` predicate, which accepts the resolution idiom (test_static_grep.py:35, :107). The plan names the stricter wording instead.

F2 MAJOR, under-specified signature (Task 4, spec 4.1). `resume_decision` row 4 is "re-enter `release_decision` with `push_completed=True`" (source.md:166), but `resume_decision`'s documented parameters (source.md:109, plan line 70) omit `cycle_id`, `applied_edits` and `target_sha`, which `release_decision` needs (source.md:107). No `GuardAction` value stands for "re-enter" (source.md:82-85). The acceptance criterion (plan line 77) cannot be written as stated. An implementer who omits the head proof would release without confirming the head, breaking the rule that release needs a confirmed push.

F3 MAJOR, report gap (Task 3, Task 8). The spec says a halt with reason `draft_guard_unavailable` reports `unavailable` (source.md:112, :68), but `guard_status(guard, mode, ordinal)` has no halt input, and plan line 61 pins "no record at ordinal 3 gives `released`". An engage that halts because the read or the timeline failed writes no guard event, so the run reports `released` for a halt. No task (Task 8 Exit report, plan line 124; Task 11) assigns the halt-reason override or tests it.

F4 MINOR, untested fold field (Task 3). `guard_status` maps `DISABLED` + `user_override` to `user_override` (source.md:112), but the fold table row for `settled(any, skipped, user_override)` (source.md:206) does not say `disabled_cause` is set, and Task 3's fold criterion (plan line 60) tests `already_draft` only. A fold that leaves the cause empty passes Task 3 and mis-reports.

F5 MINOR, weak baseline (Task 1, Task 13). Task 1 records the base failures before any `make sync-dev` (plan line 33). The repo notes that fresh worktrees fail about 43 mirror/ruff tests until `make install` and `make sync-dev` run and to record the baseline after both (docs/memory/reflect/deviation-patterns-post-release-v5.0.0.md:7). Task 13 passes when no failing id is "absent from the base-commit record" (plan line 199), so a feature-caused mirror failure that is also in the stale baseline is hidden; only two files are re-run separately.

F6 MINOR, unowned mapping (spec 4.1/4.4). `GuardRead` fields (`is_draft`, `head_sha`, `auto_merge_armed`; source.md:88-91) differ from the script's JSON keys (`isDraft`, `headRefOid`, `autoMergeRequest`; source.md:230). No task or function does the conversion, and the SKILL has no python fence to do it.

F7 MINOR, test wording (Task 9). The Wave 0 bullet must name the `--merge-guard off` L3 case (plan line 137) yet its test must fail on "L3 or `draft` gate wording" (plan line 140); a sentence "no draft call is made" contains the word `draft`.

### Recommendations

R1 Task 7: reuse `_repo_scoped` from test_static_grep.py for the new scan instead of the literal wording.
R2 Task 4/spec 4.1: add `cycle_id`, `applied_edits`, `target_sha` to `resume_decision` (or return a `RELEASE_CHECK` action) and say what row 4 returns.
R3 Task 3/8: add a status override for the `draft_guard_unavailable` halt, with a test.
R4 Task 3: add a `disabled_cause == user_override` fold assertion.
R5 Task 1: run `make install` and `make sync-dev` before recording the baseline.
R6 Add a one-line read-JSON-to-`GuardRead` mapping to the Resume/Exit section of the ref, with a test.
R7 Task 9: state that the test checks gate wording of the print rule, not the word `draft` in general.

End your card with a ## Findings block holding one fenced findings-v2 block: JSON lines, one object per line, never a table. Fields: id (F1, F2, ...), severity (CRITICAL, MAJOR or MINOR), blocking (true or false; a MINOR finding is never blocking), category (one of contradiction, data-loss, missing-requirement, other, safety, unpassable-check), lens "reflect-pre", claim (one line, at most 300 characters), refs (requirement ids, may be empty) and citations (1 to 8 objects, each with role plan or spec, a repo-relative path, line_start, line_end and an optional quote). Example line: {"id":"F1","severity":"MAJOR","blocking":false,"category":"contradiction","lens":"reflect-pre","claim":"Task 3 says X but task 5 says Y.","refs":["R-1"],"citations":[{"role":"plan","path":"plan.md","line_start":10,"line_end":12}]}. After the block add a reviewer_model_self_report line stating the model you are running as in one line.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-13T04:10:31Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:212-256

````markdown
### 4.3 `fsm.py`: the flag

- `DEFAULT_MERGE_GUARD = "draft"`; `build_arg_parser` adds `--merge-guard` with `dest="merge_guard"`, `choices=["draft", "off"]` (same shape as `--conflict-max-tier`, F5).
- `SkillArgs.merge_guard: str = DEFAULT_MERGE_GUARD`; `parse_args` passes `ns.merge_guard`.
- Effective only at `--monitor 3`; accepted and inert below. `off` makes the skill print one line: "Remediation is unprotected: --merge-guard off."
- `RunConfig` and `run_skill` do not change (F5): the guard is SKILL-orchestrated.

### 4.4 `scripts/set-draft-state.sh` (new; all GitHub I/O)

Modelled on `scripts/retrigger-review.sh`: `set -euo pipefail`, same `die`, same `--repo` resolution from the origin remote, numeric `--pr` check, exit 127 when `gh` or `jq` is missing.

```text
set-draft-state.sh --pr <N> [--repo <owner/repo>] --read
set-draft-state.sh --pr <N> [--repo <owner/repo>] --to draft|ready
```

| Mode | Calls (every one repo-scoped, F7) | Output (one JSON line) |
|---|---|---|
| `--read` | `gh pr view "$PR" --repo "$REPO" --json state,isDraft,headRefOid,autoMergeRequest`; `gh api --paginate "repos/${REPO}/issues/${PR}/timeline" --jq '.[] \| select(.event=="convert_to_draft" or .event=="ready_for_review") \| .event'` counted with `wc -l` | `{"ok":true,"state":"OPEN","isDraft":false,"headRefOid":"<sha>","autoMergeRequest":false,"transitions":3,"complete":true,"error":null}`; when the timeline call fails: `"transitions":null,"complete":false` |
| `--to draft` | re-read `state,isDraft`; if not `OPEN`, emit `ok:false,error:"not_open"`; if already draft, `changed:false`; else `gh pr ready "$PR" --repo "$REPO" --undo`; re-read to verify | `{"ok":true,"state":"OPEN","isDraft":true,"headRefOid":"<sha>","changed":true,"error":null}` |
| `--to ready` | same with `gh pr ready "$PR" --repo "$REPO"` | same shape |

Exit codes: 0 success; 1 `gh` failure or failed verification (the JSON line is still printed with `ok:false`); 2 usage; 127 missing dependency. `--to` is idempotent, so a retry or a resume re-issue is safe. A verification mismatch after a mutation is `ok:false, error:"verify_failed"`, and the SKILL settles it `failed`.

### 4.5 Protocol and docs

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

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:92-200

```markdown
## Phase 2: Flag and script

## Task 6: Add the `--merge-guard` flag

Depends on: Task 1

Edit `src/superclaude/pr_submit/fsm.py` following ./source.md section 4.3: `DEFAULT_MERGE_GUARD = "draft"`, a `--merge-guard` argument with `dest="merge_guard"` and `choices=["draft", "off"]` placed beside `--conflict-max-tier` in `build_arg_parser`, `SkillArgs.merge_guard: str = DEFAULT_MERGE_GUARD`, and `parse_args` passing `ns.merge_guard`. Leave `RunConfig` and `run_skill` unchanged. Add a test beside `test_conflict_max_tier_default_and_bounds` in `tests/pr_submit/test_skill_parse.py`.

Acceptance criteria:
- `parse_args([]).merge_guard == "draft"`, `parse_args(["--merge-guard", "off"]).merge_guard == "off"`, `SkillArgs().merge_guard == "draft"`, and `--merge-guard label` exits with an argparse error (`SystemExit`).
- `fsm.py` still contains no whole word `gh` or `git` (the static purity test passes) and every existing test in `tests/pr_submit/test_skill_parse.py` and `tests/pr_submit/test_autonomy_gates.py` passes unchanged.

## Task 7: Create the GitHub I/O script `set-draft-state.sh`

Depends on: Task 1

Create `src/superclaude/skills/sc-pr-submit-protocol/scripts/set-draft-state.sh` following ./source.md section 4.4 and modelled on `scripts/retrigger-review.sh` (same `die`, `--repo` resolution from the origin remote, numeric `--pr` check, exit 127 when `gh` or `jq` is missing, executable bit). Modes `--read` and `--to draft|ready` with the exact calls, the one-line JSON shapes and the exit codes 0, 1, 2, 127 of section 4.4; every `gh` call carries `--repo "$REPO"` or a `repos/${REPO}/...` path; the timeline count uses `gh api --paginate` with a `jq` filter on `convert_to_draft` and `ready_for_review` piped to `wc -l`; `--to` re-reads state first (non-`OPEN` gives `error:"not_open"`), is idempotent (`changed:false` when already in the target state) and verifies after the mutation (`verify_failed`). Create `tests/pr_submit/test_set_draft_state.py` using a fake `gh` on `PATH` that logs its arguments (the fake-executable approach of `tests/pr_submit/test_conflict_scripts.py`), exposing the fake as a helper or fixture that other test files may import. Add the script to `_RESOLUTION_SCRIPTS` in `tests/pr_submit/test_static_grep.py` only after reading the purpose of that list (Task 1 O2), and to any script list that Task 1 O2 shows is required for a new script. As the last step, once the script text is final, add one `WRITE_VERB_CLASSIFICATION` entry in `tests/skills/test_worker_contract.py` for every line of the script that matches `gh pr` or `gh api` (exact stripped line, category `never-worker`, the standard pr-submit reason). Run `make sync-dev`.

Acceptance criteria:
- Fake-`gh` tests assert: `--read` prints one JSON line with `ok`, `state`, `isDraft`, `headRefOid`, `autoMergeRequest`, `transitions`, `complete`; a failing timeline call prints `transitions: null` and `complete: false`; `--to draft` on a draft PR makes no `pr ready` call and prints `changed:false`; `--to ready` on a merged PR prints `ok:false` with `error:"not_open"`; a mismatch after the mutation prints `ok:false` with `error:"verify_failed"`.
- Exit codes are asserted: 0 on success, 1 on a failing `gh` (JSON still printed with `ok:false`), 2 for a missing or non-numeric `--pr` and for an unknown argument, 127 with `gh` absent from `PATH` and a separate case with `jq` absent from `PATH`.
- The recorded fake-`gh` argument log shows `--repo` or a `repos/` path on every call, and `test_set_draft_state.py` also statically scans the script and asserts every `gh` line carries `--repo` or a `repos/` path (the existing `test_t105_runtime_repo_pin` covers only the poll script and is not the proof); the script passes the `_RESOLUTION_SCRIPTS` origin-URL resolution tests.
- `uv run pytest tests/pr_submit/test_set_draft_state.py tests/pr_submit/test_static_grep.py tests/pr_submit/test_conflict_sync_protocol.py tests/skills/test_worker_contract.py -q` passes (the classification and stale-entry tests included) and `make verify-sync` exits 0.

## Phase 3: Protocol text

## Task 8: Write the protocol reference `refs/merge-guard.md`

Depends on: Task 1
Depends on: Task 4
Depends on: Task 7

Create `src/superclaude/skills/sc-pr-submit-protocol/refs/merge-guard.md` from ./source.md sections 3, 4.1, 4.5, 4.6 and 5, as protocol steps (read with `scripts/set-draft-state.sh --read`, decide with `superclaude.pr_submit.merge_guard`, append the `draft_guard_requested` event with fsync before the call, run `scripts/set-draft-state.sh --to`, append `draft_guard_settled`) for: Engage at the end of Wave 3 (L3, only when at least one verified finding of Medium severity or higher is routed to a fix, once per cycle id; review-fix cycles and CI-fix cycles; mints the cycle id with `fix_cycle_id` in the single place named by Task 1 O1 and reuses it as the `cycle_id` of the push triad and of `rereview_requested`; prints the clear command `gh pr ready <N> --repo "$REPO"` once); Pre-push (the script `--read` must show `OPEN` at the pre-push head guard step before `push_decision`, otherwise halt `pr_not_open`, push nothing, report the local commit); Release (after `push_completed`, head equals `target_sha`, or zero-edit proof with this cycle's applied-edit count, before reply, resolve and the S5a re-trigger; one retry; `already in target state` counts as confirmed); Foreign toggle and unreadable timeline handling; Exit report (the `merge_guard` field mapping of `guard_status`, the held-exit list with the clear command, and for the L2 line a pointer to the SKILL.md output table, which carries the literal text; the ref holds no second copy of it); Resume, loaded from Wave 0 at every ordinal and in both modes (`resume_decision` rows, the three `RECONCILE` reasons, the `landed`, `not_landed` and `ambiguous` branch strings, `published` computed with `held_cycle_published` so that a push that completed normally before the crash also releases, and held-guard reporting when the mode is `off` or the ordinal is below 3). Every fenced command line starts with `gh`, `git`, `uv`, `make`, `jq` or a `scripts/` path that exists; every `gh` line is repo-scoped; the text contains no `src/superclaude` string, no python fence and no `file:NNN` pointer. Create `tests/pr_submit/test_merge_guard_protocol.py` with the static checks. As the last step, once the ref text is final, add one `WRITE_VERB_CLASSIFICATION` entry in `tests/skills/test_worker_contract.py` for every line of the ref that matches `gh pr` or `gh api` (exact stripped line, category `never-worker`, the standard pr-submit reason). Run `make sync-dev`.

Acceptance criteria:
- The ref has a section for each of Engage, Pre-push, Release, Exit report and Resume, states the single place where the guard-enabled cycle id is minted (matching the O1 finding in `./artifacts/pre-build-gate.md`), and the Resume section states that it also runs on `--resume` below ordinal 3 and with `--merge-guard off`.
- `tests/pr_submit/test_merge_guard_protocol.py` asserts: the ref exists, its fenced commands pass the allowed-program rule, every `gh` line passes the repo-scope check used in `tests/pr_submit/test_static_grep.py`, `scripts/set-draft-state.sh` is a file, and the ref does not contain `src/superclaude`; the test passes under `uv run pytest tests/pr_submit/test_merge_guard_protocol.py -q`.
- The ref states that engage failure and an unreadable timeline at engage halt with `terminal_halted` reason `draft_guard_unavailable` before any edit, that an exit with unpublished or uncertain work leaves the PR draft and reports `held`, that the Engage section names the Medium-or-higher routed-finding trigger and "once per cycle", and that Resume uses `published` and the recovery branch strings; the protocol test asserts each of these phrases is present.
- `uv run pytest tests/skills/test_worker_contract.py -q` passes and `make verify-sync` exits 0.

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

## Task 10: Wire the Wave 3, Wave 6 and Wave 8 bullets into `SKILL.md` and the overlay note into `refs/state-machine.md`

Depends on: Task 9

Edit `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` additively: one new bullet under each of Wave 3, Wave 6 and Wave 8 that loads `refs/merge-guard.md` only at L3 with `--merge-guard` `draft`, written as new sentences after, never inside, the pinned sentences. The Wave 3 bullet states that engage happens at the end of Wave 3 only when at least one verified finding of Medium severity or higher is routed to a fix, once per cycle id, and mints the cycle id; the Wave 6 bullet states that Pre-push runs at the pre-push head guard step before `push_decision` and that Release runs after `push_completed` and before reply, resolve and the S5a re-trigger; the Wave 8 bullet states that a CI-fix cycle engages with kind `ci` and releases after `push_completed` before the CI re-poll. The S5a re-trigger sentence and the Wave 6 pre-push sentence stay byte-identical. Edit `src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md` with a short overlay note that guard phases are folded values, not `MonitorState` members, without the words `gh` or `git` and outside the wait-only sentences pinned for that file. Avoid `gh pr` and `gh api` on new lines (refer to "the clear command from the ref"); add a `WRITE_VERB_CLASSIFICATION` entry as the last step for any new line that cannot avoid them. Extend `tests/pr_submit/test_merge_guard_protocol.py` with one test per bullet (each gated on L3 and `draft`) and one for the overlay note. Run `make sync-dev`.

Acceptance criteria:
- The Wave 3 bullet test asserts the sentence names the Medium-or-higher routed-finding trigger and "once per cycle" and fails when either phrase is deleted (an unconditional "engage at the end of Wave 3" does not pass); the Wave 6 test asserts the Pre-push sentence and the Release-before-reply-resolve-re-trigger order; the Wave 8 test asserts the CI-fix sentence; each test fails when its sentence is removed.
- The S5a re-trigger sentence and the Wave 6 pre-push sentence are asserted byte-identical by comparing the live text with string constants (the literal start text recorded in `./artifacts/pre-build-gate.md`, as the existing pins write them), not with `git show HEAD:`; `SKILL.md` has one python fence and no `src/superclaude` string; no new line contains `evidence-validator` or `conflict-intent.md`.
- `uv run pytest tests/pr_submit -q` and `uv run pytest tests/skills/test_worker_contract.py -q` pass and `make verify-sync` exits 0.

## Phase 4: Scenario tests

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

## Phase 5: Command and user docs

## Task 12: Document the flag in the command file

Depends on: Task 6
Depends on: Task 8

Edit `src/superclaude/commands/pr-submit.md`, using the pins recorded in `./artifacts/pre-build-gate.md`: add `[--merge-guard {draft,off}]` to the `argument-hint` front matter line (after `--conflict-max-tier`), a row `--merge-guard {draft,off}` with default `draft` in the Options table (effective only at `--monitor 3`; `off` prints "Remediation is unprotected: --merge-guard off."), and a short "Merge guard" section next to "Merge-conflict handling" covering: when the PR becomes a draft, when it becomes ready, the held outcome and the clear command, the unreadable-timeline rule, and that drafts and ready transitions may affect reviewers and workflows (gates G4 and G5 are OPEN and not claimed verified, the PR body states the release gate). The text must not contain `src/superclaude`. Extend `tests/pr_submit/test_merge_guard_protocol.py` with assertions for the flag row, the argument-hint entry and the new section. As the last step, once the command text is final, add one `WRITE_VERB_CLASSIFICATION` entry in `tests/skills/test_worker_contract.py` for every line of the file that newly matches `gh pr` or `gh api` (exact stripped line, category `never-worker`, the standard pr-submit reason). Run `make sync-dev`.

Acceptance criteria:
- `grep -n "merge-guard" src/superclaude/commands/pr-submit.md` shows the argument-hint entry, the Options row and the section heading, and the section states default-on at monitor 3, the exact clear command and that the behaviour is unverified until the owner's disposable-PR run.
- `uv run pytest tests/pr_submit -q` passes, including the command-file checks in `tests/pr_submit/test_conflict_sync_protocol.py`, `uv run pytest tests/skills/test_worker_contract.py -q` passes (every new `gh pr` line classified, none stale), and `make verify-sync` exits 0.

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

### tests/pr_submit/test_static_grep.py:35-36

```python
_REPO_RESOLVE = re.compile(r"\bgh\s+repo\s+view\b")
# The T-N50 core-pure file set.
```

### tests/pr_submit/test_static_grep.py:107-132

```python
def _repo_scoped(line: str) -> bool:
    """A gh command line is repo-scoped if it pins a whole-token ``--repo``, is a
    ``gh api`` call carrying a ``repos/<owner/repo>/`` path or ``graphql``, or IS the
    ``gh repo view`` resolution idiom.

    This is the generalized safety property: the prior implementation required the
    literal fork slug, but the repo is now RESOLVED at runtime — so "scoped" means the
    call carries an explicit repo reference (computed, not bare), never a hardcoded
    owner/repo. A bare `gh pr`/`gh api` with none of these would silently default onto
    an upstream parent → the defect.

    The match is structure-anchored, NOT a loose substring (D3 hardening): a trailing
    ``#`` comment is stripped first (so ``gh pr create … # see repos/docs`` does NOT
    pass), ``--repo`` is matched as a whole token (so ``--reposcope`` does NOT pass), and
    ``repos/``/``graphql`` only count when they ride on an actual ``gh api`` command (so
    an incidental ``# graphql`` mention does NOT pass). These three holes were real
    bypasses of the prior unanchored ``in``-substring predicate.
    """
    code = re.sub(r"\s+#.*$", "", line)  # strip a trailing shell / markdown comment
    if re.search(r"--repo\b", code):  # whole-token --repo (gh pr / gh repo)
        return True
    if _REPO_RESOLVE.search(code) is not None:  # the `gh repo view` resolution idiom
        return True
    # repos/ path or graphql must be on an actual `gh api` invocation, not anywhere.
    if re.search(r"\bgh\s+api\b", code) and ("repos/" in code or "graphql" in code):
        return True
```

### tests/pr_submit/test_static_grep.py:481-487

```python
_RESOLUTION_SCRIPTS = (
    SKILL_DIR / "scripts" / "poll-augment-review.sh",
    SKILL_DIR / "scripts" / "poll-ci-checks.sh",
    SKILL_DIR / "scripts" / "retrigger-review.sh",
    SKILL_DIR / "scripts" / "reply-resolve-thread.sh",
    SKILL_DIR / "scripts" / "set-draft-state.sh",
)
```

### tests/pr_submit/test_static_grep.py:540-552

```python
            i
            for i, line in enumerate(lines)
            if line.lstrip().startswith(("REPO=", "[ -n"))
            and "git remote get-url origin" in line
        )
        gh_view_at = next(
            i
            for i, line in enumerate(lines)
            if line.lstrip().startswith(("REPO=", "[ -n"))
            and "gh repo view --json nameWithOwner" in line
        )
        assert origin_at < gh_view_at, (
            f"{script.name}: `gh repo view` is tried before the origin remote"
```

### src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh:46-51

```bash
# Resolve the target repo (owner/repo). The SKILL normally passes --repo; absent it,
# resolve from the current checkout (the origin remote, then gh repo view). The
# issue-comment POST target is COMPUTED — never a literal owner/repo (de-hardcoded).
REPO="${REPO:-$(git remote get-url origin 2>/dev/null | sed -E 's#^ssh://[^/]+/##; s#^git@[^:]+:##; s#^https?://[^/]+/##; s#\.git$##' || true)}"
[ -n "$REPO" ] || REPO="$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || true)"
[ -n "$REPO" ] || die "could not resolve target repo (pass --repo <owner/repo>)" 2
```

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|--------------------|---------|--------|-----------|
| INF-038: `RunConfig` and `run_skill` do not change (F5): the guard is SKILL-orchestrated. | none | UNMAPPED by rule (none 0.429) | source.md:217 |
| INF-039: `set -euo pipefail`, same `die`, same `--repo` resolution from the origin remote, numer... | Task 7 | covered (containment 0.882) | source.md:221 |
| INF-040: gh api --paginate "repos/${REPO}/issues/${PR}/timeline" | Task 7 | covered (containment 0.875) | source.md:230 |
| INF-041: if not `OPEN`, emit `ok:false,error:"not_open"`; if already draft, `changed:false` | Task 7 | covered (containment 0.889) | source.md:231 |
| INF-042: `--to` is idempotent, so a retry or a resume re-issue is safe. | none | UNMAPPED by rule (none 0.5) | source.md:234 |
| INF-043: Loaded lazily at L3 Wave 3, Wave 6 and Wave 8. | Task 8 | covered (containment 0.75) | source.md:240 |
| INF-044: No new python fence | Goal+Constraints | covered (containment 1.0) | source.md:241 |
| INF-045: update it to 45 and name `draft_guard_requested` and `draft_guard_settled`, without the... | Task 2 | covered (containment 1.0) | source.md:242 |
| INF-046: the guard phases are fold values, not `MonitorState` members | Task 10 | covered (containment 0.833) | source.md:243 |
| INF-047: Flag row and a paragraph: what it does, the clear command, `held` meaning, default on. | Task 13 | covered (containment 0.778) | source.md:245 |
| INF-048: The SKILL mints it at the end of Wave 3 | Task 8 | covered (containment 1.0) | source.md:251 |
| INF-049: The entries are added after the text of each file is final, as the last step of the tas... | Goal+Constraints | covered (containment 0.7) | source.md:255 |
| INF-050: Acceptance trace (must appear in this order in the run log) | Task 11 | covered (containment 0.833) | source.md:270 |
| INF-051: Without `published` no row would match and the PR would stay draft. | Task 3 | covered (containment 0.714) | source.md:280 |
| INF-052: halt `pr_not_open`, nothing pushed, report the local commit `<target_sha>`. | Task 8 | covered (containment 0.875) | source.md:281 |
| INF-053: Run `make sync-dev` at the end of every task that edits a file under `src/superclaude/s... | Goal+Constraints | covered (containment 1.0) | source.md:301 |
| INF-054: the final task runs the FULL suite (`uv run pytest -q tests`) and compares its failures... | Task 1 | covered (containment 0.857) | source.md:301 |
| INF-055: Never stage `.claude/`. | Goal+Constraints | covered (containment 1.0) | source.md:301 |
| INF-056: No task makes a live PR call, and the run that opens the PR must not enable the feature... | Task 1 | covered (containment 0.833) | source.md:326 |
| INF-057: A static test asserts `merge_guard.py` has no `gh` or `git` word. | Task 3 | covered (containment 1.0) | source.md:322 |
| INF-058: the script test for a missing `jq` (exit 127) | Task 7 | covered (containment 1.0) | source.md:322 |
| INF-059: Cite tests and constants by symbol name | Goal+Constraints | covered (containment 1.0) | source.md:362 |
| INF-060: Update the 43-member enumeration in `refs/loop-guard.md` in the event-enum task. | Task 2 | covered (containment 0.909) | source.md:368 |
| INF-061: Protocol prose written by the plan never carries `file:NNN` pointers | Goal+Constraints | covered (containment 0.889) | source.md:369 |
| INF-062: a crash after a normal `push_completed` (no dangling window, `published` true) releases... | Task 11 | covered (containment 1.0) | source.md:318 |
| INF-063: Add the acceptance trace of section 5 as a fixture over `RunLog`. | Task 11 | covered (containment 0.857) | source.md:322 |
| INF-064: a settled `not_applied` of either direction returns to `phase_before_request` | Task 3 | covered (containment 0.833) | source.md:376 |
