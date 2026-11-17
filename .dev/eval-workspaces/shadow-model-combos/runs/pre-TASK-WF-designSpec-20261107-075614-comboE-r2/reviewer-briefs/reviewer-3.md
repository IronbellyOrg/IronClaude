## T1 card excerpt

Persona: refactorer. You audit structure and technical debt in the plan: task ordering and dependencies, scope the spec lists that no task owns, tasks that bundle too much for one pass, pins and sync steps that a later task can break, and mirrors or copies that drift.

Attribution note: this package already executed (landed in commit 0b8a5801d, parent 0e486ab8d). The spec facts F1-F13 were re-read at the parent commit and hold there (EventType has 43 members at the parent, `conflicts.py` imports only `.fsm` and `.models`, `fsm.py` does not import `run_log`, `recovery.py` defines `BRANCH_A_LANDED`, `BRANCH_B_NOT_LANDED`, `BRANCH_C_AMBIGUOUS`, the enum already has `FIX_APPLIED`, `PUSH_COMPLETED`, `REREVIEW_REQUESTED`, `TERMINAL_HALTED`). HEAD now carries the implementation, so a citation of HEAD text as a plan defect or as a gap must be checked against 0e486ab8d (`git show 0e486ab8d:<path>` is not available to you; if you cannot check, say so and mark the claim as inferred). You audit the PLAN and SPEC text, not the shipped code. Rules for claims: before you say an acceptance criterion "cannot fail" or "is missing", quote the criterion text first; a constraint stated in task prose without an acceptance criterion is a MINOR gap unless a wrong outcome follows.

Coverage (Step 1B.0): 0 parsed requirement IDs (the spec uses FR/F/G/O labels), 48 inferred rows INF-001..INF-048 with verbatim quotes (artifacts/coverage-matrix.json); containment matching covered 42 of 48 (`coverage_pct_union` 0.875). `coverage_degraded: parsed-sparse`, so no Tier-1 stop. Unmatched rows are partly matcher noise: INF-007, INF-012, INF-015, INF-026, INF-029, INF-046.

Candidate gaps from Tier 1 for your lens (hypotheses; verify or refute each, then add what is missing):
- H5. Byte-identical pins checked against start text only: Task 1 records "the literal start text" of the S5a sentence and the Wave 6 pre-push sentence (plan:33); Task 10 AC (plan:154) says byte-identical by comparing with those constants; a prefix constant cannot detect an edit inside the sentence.
- H8. Task 7 text makes `_RESOLUTION_SCRIPTS` conditional (plan:108) while its AC (plan:113) is unconditional.
- H9. Dependency order is acyclic and every spec file of section 6 (source.md:285-299) has a task; no missing-file gap found. Check whether any `Depends on:` line is missing (for example Task 5 and Task 8 against the files they edit or import).

Write the literal heading `## Findings block` and under it ONE fence opened with exactly ```findings-v2 (never ```json, never a table), JSON lines, one object per line. Fields: id (F1, F2, ...), severity (only CRITICAL, MAJOR or MINOR; a MINOR finding is never blocking), blocking (true or false), category (one of contradiction, data-loss, missing-requirement, other, safety, unpassable-check), lens "reflect-pre", claim (one line, at most 300 characters), refs (requirement ids such as INF-012 or spec labels, may be empty) and citations (1 to 8 objects, each with role plan or spec, a repo-relative path, line_start, line_end and an optional quote of at most 200 characters; use the exact repo-relative paths printed in the H3 headings of your grounding hunks, and take line numbers from those headings). Example line: {"id":"F1","severity":"MAJOR","blocking":false,"category":"contradiction","lens":"reflect-pre","claim":"Task 3 says X but task 5 says Y.","refs":["INF-012"],"citations":[{"role":"plan","path":"plan.md","line_start":10,"line_end":12}]}. After the block add a line `coverage_rows_checked:` listing the INF row ids of your coverage slice you verified (comma separated), then a line `reviewer_model_self_report:` stating the model you are running as in one line. Return the whole card as your reply text; do not write or edit any file.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-13T04:08:07Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:212-301

`````markdown
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

## 5. Sequences

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
`````

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:29-50

`````markdown
## Phase 1: Contracts and pure core

## Task 1: Write the pre-build record `./artifacts/pre-build-gate.md`

Create `./artifacts/pre-build-gate.md` in this package from ./source.md sections 6, 8 and 10. First record the base-commit state: run `make lint`, `uv run ruff format --check src/ tests/` and the full suite `uv run pytest -q tests` before any code edit and write each exit code, the pass count and every failing test id (or "clean") into the file, so later failures can be told apart from this feature's. Then record the release-gate decision of ./source.md section 8 in the owner's words: the build proceeds with no GitHub calls (fake `gh` in tests); gates G1 (live part), G2 (live part), G4, G5 and G6 are a release gate that the owner runs on a disposable fork PR before the feature is merged or turned on by default; the user guide states that draft behaviour is unverified until then; the PR body states the gate plainly; the run that opens the PR must pass `--merge-guard off`. Then close the open items by reading the code: O1, where `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` (Wave 3 to Wave 6 and Wave 8 text) and `refs/loop-guard.md` assign a fix or CI cycle's `cycle_id` today and whether any test under `tests/pr_submit/` pins a value; O2, how scripts are granted and invoked in the SKILL front matter and what `test_allowed_tools_cover_every_program` in `tests/pr_submit/test_conflict_sync_protocol.py` and the `_RESOLUTION_SCRIPTS` tests in `tests/pr_submit/test_static_grep.py` require of a new script; O3, every exact-text pin and line-content rule (for example `test_intent_and_validator_lines_say_tier_2`, `test_skill_forbids_force_push`, the wait-only sentences pinned for `refs/state-machine.md`, and the `WRITE_VERB_CLASSIFICATION` table with its stale-entry test in `tests/skills/test_worker_contract.py`) on `SKILL.md`, `refs/state-machine.md`, `refs/loop-guard.md` and `src/superclaude/commands/pr-submit.md` that the later additive edits must avoid; O4, that the S5a re-trigger sentence in `SKILL.md` stays unchanged and where the new release sentence goes relative to it; and the literal start text of the S5a sentence and of the Wave 6 pre-push sentence as the existing pins write them, so later tests can compare against string constants.

Acceptance criteria:
- `./artifacts/pre-build-gate.md` has the base-commit record (three commands, exit codes, the full-suite pass count and failing test ids, or "clean") and one row each for G1 to G6: G1 to G3 `CONFIRMED` for the locally verifiable part with the evidence named in ./source.md, G1 and G2 live parts, G4, G5 and G6 `OPEN` as a release gate with the owner decision quoted.
- O1 to O4 each carry the finding with the file and symbol read in this task (no bare line numbers); O1 names one single place where the guard-enabled cycle id is minted so the push triad and `rereview_requested` use the same id, or states that no id is minted today and which sentence will mint it.
- The file lists every exact-text pin and line-content rule found for O3, including the classification table rule (exact line key, category, stale-entry test), and the literal start text of the two pinned sentences of O4, so Tasks 7 to 13 can avoid or reuse them; no GitHub or network call is made.

## Task 2: Add the two guard events to the closed event enum and the enumeration texts

Depends on: Task 1

Edit `src/superclaude/pr_submit/models.py`: add `DRAFT_GUARD_REQUESTED = "draft_guard_requested"` and `DRAFT_GUARD_SETTLED = "draft_guard_settled"` to `EventType` (a comment block like the conflict-cycle one), and change the module docstring and the `EventType` class docstring from "exactly 43 members" to 45, naming the new events. Edit the `RunLog.append` docstring in `src/superclaude/pr_submit/run_log.py` that says "43 closed" to 45. Edit `src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md`: its heading "The 43 event types" and the sentence that says the enum has EXACTLY 43 members become 45 and name `draft_guard_requested` and `draft_guard_settled`, without the whole words `gh` or `git` (the file is in `CORE_PURE_FILES`). Update `tests/pr_submit/test_run_log.py` (the test `test_eventtype_is_43_members_with_silence_reviewer_and_conflict_events`: rename it to describe 45 members, assert both lengths are 45 and both new values are present) and the `len(EventType)` assertion in `tests/pr_submit/test_codex_reviews.py` to 45. Leave `tests/pr_submit/test_idempotency.py` (7 sets) unchanged. Run `make sync-dev`.

Acceptance criteria:
- `uv run pytest tests/pr_submit/test_run_log.py tests/pr_submit/test_codex_reviews.py tests/pr_submit/test_idempotency.py tests/pr_submit/test_static_grep.py -q` passes with `len(EventType) == 45` and the two new values asserted.
- `RunLog.append` accepts an event with `event_type: "draft_guard_requested"` and still rejects an unknown type, with the updated count in the error message.
- `grep -rn "43" src/superclaude/pr_submit/models.py src/superclaude/pr_submit/run_log.py src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md` shows no remaining claim that the enum has 43 members, and `refs/loop-guard.md` names both new event values.
- `make verify-sync` exits 0 after the sync.
`````

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:92-156

`````markdown
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

`````

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:175-200

`````markdown
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
`````

## Coverage slice

You are responsible for the rows INF-025 to INF-048 (script, protocol text, docs, sync and test hygiene).

| Requirement | Matched task | Status | Grounding |
|---|---|---|---|
| INF-025: `build_arg_parser` adds `--merge-guard` with `dest="merge_guard"`, `choices=["draft", "off | Task 6 | covered (containment 0.8889) | .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:214 |
| INF-026: `RunConfig` and `run_skill` do not change (F5): the guard is SKILL-orchestrated. | none | unmatched (best ratio 0.4286) | .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:217 |
| INF-027: `set -euo pipefail`, same `die`, same `--repo` resolution from the origin remote, numeric  | Task 7 | covered (containment 0.875) | .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:221 |
| INF-028: gh api --paginate "repos/${REPO}/issues/${PR}/timeline" | Task 7 | covered (containment 0.875) | .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:230 |
| INF-029: `--to` is idempotent, so a retry or a resume re-issue is safe. | none | unmatched (best ratio 0.5) | .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:234 |
| INF-030: A verification mismatch after a mutation is `ok:false, error:"verify_failed"`, and the SKI | Task 7 | covered (containment 0.6) | .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:234 |
| INF-031: The Wave 0 bullet is a flat line placed before the Wave 1 bullet and contains no L3 or `dr | Task 9 | covered (containment 1.0) | .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:241 |
| INF-032: it must not contain the words `evidence-validator` or `conflict-intent.md` | Task 9 | covered (containment 0.8571) | .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:241 |
| INF-033: Its event-type enumeration says the enum has 43 members; update it to 45 and name `draft_g | Task 2 | covered (containment 1.0) | .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:242 |
| INF-034: `--merge-guard {draft,off}` in the argument-hint and the Options table; a short "Merge gua | Task 12 | covered (containment 1.0) | .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:244 |
| INF-035: Flag row and a paragraph: what it does, the clear command, `held` meaning, default on. | Task 13 | covered (containment 0.7778) | .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:245 |
| INF-036: A `held` report always carries the reason and `gh pr ready <N> --repo <REPO>` | Task 8 | covered (containment 0.9) | .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:247 |
| INF-037: The SKILL mints it at the end of Wave 3 and uses the same id as the `cycle_id` of the push | Task 8 | covered (containment 0.9091) | .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:251 |
| INF-038: Every new line under `src/superclaude/skills/`, `src/superclaude/commands/` or `src/superc | Task 8 | covered (containment 0.75) | .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:255 |
| INF-039: Acceptance trace (must appear in this order in the run log): `draft_guard_requested(draft) | Task 11 | covered (containment 0.9412) | .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:270 |
| INF-040: `terminal_halted(draft_guard_unavailable)`, no edit. Message names `--merge-guard off` and | Task 8 | covered (containment 0.9091) | .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:274 |
| INF-041: next checkpoint: `state != OPEN` -> halt `pr_not_open`, nothing pushed, report the local c | Task 8 | covered (containment 0.75) | .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:281 |
| INF-042: Run `make sync-dev` at the end of every task that edits a file under `src/superclaude/skil | Task 8 | covered (containment 0.9286) | .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:301 |
| INF-043: the final task runs the FULL suite (`uv run pytest -q tests`) and compares its failures wi | Task 1 | covered (containment 0.8571) | .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:301 |
| INF-044: No task makes a live PR call, and the run that opens the PR must not enable the feature (` | Task 1 | covered (containment 0.8462) | .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:326 |
| INF-045: The user guide states that draft behaviour is unverified until then, and the PR body state | Task 1 | covered (containment 1.0) | .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:326 |
| INF-046: Cite tests and constants by symbol name (for example `_NEW_KEY_DEFAULTS`, `_RESOLUTION_SCR | none | unmatched (best ratio 0.5625) | .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:362 |
| INF-047: scenario tests import only helpers and fixtures from `test_set_draft_state.py`, never `tes | Task 11 | covered (containment 0.7) | .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:377 |
| INF-048: "no push after a `pr_not_open` halt" is asserted on `RunLog.read_events()` | Task 11 | covered (containment 0.8333) | .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:377 |
