## T1 card excerpt

Persona: refactorer. You audit structure and tech debt in the plan: task dependency order, test-pin hazards (stale classification entries, line-number citations, double-collected tests), and constraints that no AC checks.

Attribution note: this package already executed (landed in commit 0b8a5801d, parent 0e486ab8d). The spec's facts F1-F13 were
re-read at the parent commit 0e486ab8d and hold there (EventType 43 members, `_NEW_KEY_DEFAULTS`, `_RESOLUTION_SCRIPTS`,
`CORE_PURE_FILES`, `WRITE_VERB_CLASSIFICATION`, `BRANCH_*` constants, fsm.py has 1246 lines so the 900-943 cite is valid). HEAD
now carries the implementation, so a citation of HEAD text as a plan defect or as a gap must be checked against 0e486ab8d.


## Candidate gaps (hypotheses for the reviewers; none is final)

1. Task 11 acceptance criteria assert that twelve test NAMES exist, a trace order, and forbidden calls, but not the behaviour
   of most listed scenarios (foreign toggle continues the run, engage failure halts before any edit; the merged-PR case does carry a behaviour AC about push events). A test
   with the right name and an empty body would satisfy the name AC.
2. Spec 4.6 says the guard, the push triad and `rereview_requested` of one cycle share one `cycle_id`. No AC asserts the
   shared id; Task 8 AC says only that the ref names the minting place.
3. Task 8 text says "no `file:NNN` pointer" and spec section 10 requires it; no AC checks it (constraint without AC).
4. Task 2 AC3 says `grep 43 ...` "shows no remaining claim that the enum has 43 members"; models.py keeps the comment "the
   42nd-43rd", so the grep output is never empty and the AC is a judgment call.
5. Task 7 prose requires `gh api --paginate`; no AC feeds a multi-page timeline to the fake `gh` (spec F9, gate G2).


Treat the T1 candidate gaps as hypotheses to test against the files, not as conclusions.

Before you file an "un-AC-d", "no gate" or "cannot fail" claim, quote the acceptance-criteria or constraint text you judged against; a claim whose quoted AC does cover the point is dropped. The package already executed (see the attribution note): judge the PLAN against the spec; never cite post-execution files (merge_guard.py, refs/merge-guard.md, set-draft-state.sh, tests/pr_submit/test_merge_guard*.py) as plan defects.

End your card with a ## Findings block holding one fenced findings-v2 block: JSON lines, one object per line, never a table. Fields: id (F1, F2, ...), severity (CRITICAL, MAJOR or MINOR), blocking (true or false; a MINOR finding is never blocking), category (one of contradiction, data-loss, missing-requirement, other, safety, unpassable-check), lens "reflect-pre", claim (one line, at most 300 characters), refs (requirement ids, may be empty) and citations (1 to 8 objects, each with role plan or spec, a repo-relative path, line_start, line_end and an optional quote). Example line: {"id":"F1","severity":"MAJOR","blocking":false,"category":"contradiction","lens":"reflect-pre","claim":"Task 3 says X but task 5 says Y.","refs":["R-1"],"citations":[{"role":"plan","path":"plan.md","line_start":10,"line_end":12}]}. After the block add a reviewer_model_self_report line stating the model you are running as in one line.

Write the heading exactly "## Findings block" (two hash signs, then the words) and open the fence with exactly three backticks followed by findings-v2 (not json). Cite repo-relative paths only (the plan is .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md, the spec is .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md); a bare "source.md" path does not resolve.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-13T03:04:39Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:17-27
```markdown
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

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:253-255
```markdown
### 4.7 Pinned write-verb classification (F12)

Every new line under `src/superclaude/skills/`, `src/superclaude/commands/` or `src/superclaude/agents/` that contains `gh pr`, `gh api` or a git write verb is a hit of `WRITE_VERB_RE` and needs one entry in `WRITE_VERB_CLASSIFICATION` in `tests/skills/test_worker_contract.py`: the key is the repo-relative path, the verb text (`gh pr`, `gh api`) and the exact stripped line; the value is category `never-worker` with the standard pr-submit reason text used by the neighbouring entries (the pr-submit monitor is on the never-as-worker list). The entries are added after the text of each file is final, as the last step of the task that writes the file, because a later edit of a classified line makes the entry stale and fails `test_classification_table_has_no_stale_entries`. The new files that carry hits are `scripts/set-draft-state.sh`, `refs/merge-guard.md`, `src/superclaude/commands/pr-submit.md` and any new `SKILL.md` line; a new line that does not need the words `gh pr` (for example "print the clear command from the ref") avoids an entry. The `read-only` category is not used for these calls (a `gh pr ready` mutation is never read-only). `docs/user-guide/` is outside the scanned roots.
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

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:104-114
```markdown
## Task 7: Create the GitHub I/O script `set-draft-state.sh`

Depends on: Task 1

Create `src/superclaude/skills/sc-pr-submit-protocol/scripts/set-draft-state.sh` following ./source.md section 4.4 and modelled on `scripts/retrigger-review.sh` (same `die`, `--repo` resolution from the origin remote, numeric `--pr` check, exit 127 when `gh` or `jq` is missing, executable bit). Modes `--read` and `--to draft|ready` with the exact calls, the one-line JSON shapes and the exit codes 0, 1, 2, 127 of section 4.4; every `gh` call carries `--repo "$REPO"` or a `repos/${REPO}/...` path; the timeline count uses `gh api --paginate` with a `jq` filter on `convert_to_draft` and `ready_for_review` piped to `wc -l`; `--to` re-reads state first (non-`OPEN` gives `error:"not_open"`), is idempotent (`changed:false` when already in the target state) and verifies after the mutation (`verify_failed`). Create `tests/pr_submit/test_set_draft_state.py` using a fake `gh` on `PATH` that logs its arguments (the fake-executable approach of `tests/pr_submit/test_conflict_scripts.py`), exposing the fake as a helper or fixture that other test files may import. Add the script to `_RESOLUTION_SCRIPTS` in `tests/pr_submit/test_static_grep.py` only after reading the purpose of that list (Task 1 O2), and to any script list that Task 1 O2 shows is required for a new script. As the last step, once the script text is final, add one `WRITE_VERB_CLASSIFICATION` entry in `tests/skills/test_worker_contract.py` for every line of the script that matches `gh pr` or `gh api` (exact stripped line, category `never-worker`, the standard pr-submit reason). Run `make sync-dev`.

Acceptance criteria:
- Fake-`gh` tests assert: `--read` prints one JSON line with `ok`, `state`, `isDraft`, `headRefOid`, `autoMergeRequest`, `transitions`, `complete`; a failing timeline call prints `transitions: null` and `complete: false`; `--to draft` on a draft PR makes no `pr ready` call and prints `changed:false`; `--to ready` on a merged PR prints `ok:false` with `error:"not_open"`; a mismatch after the mutation prints `ok:false` with `error:"verify_failed"`.
- Exit codes are asserted: 0 on success, 1 on a failing `gh` (JSON still printed with `ok:false`), 2 for a missing or non-numeric `--pr` and for an unknown argument, 127 with `gh` absent from `PATH` and a separate case with `jq` absent from `PATH`.
- The recorded fake-`gh` argument log shows `--repo` or a `repos/` path on every call, and `test_set_draft_state.py` also statically scans the script and asserts every `gh` line carries `--repo` or a `repos/` path (the existing `test_t105_runtime_repo_pin` covers only the poll script and is not the proof); the script passes the `_RESOLUTION_SCRIPTS` origin-URL resolution tests.
- `uv run pytest tests/pr_submit/test_set_draft_state.py tests/pr_submit/test_static_grep.py tests/pr_submit/test_conflict_sync_protocol.py tests/skills/test_worker_contract.py -q` passes (the classification and stale-entry tests included) and `make verify-sync` exits 0.
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

After the Findings block also add one line "coverage_rows_checked: INF-001, INF-002, ..." listing the Coverage slice rows you actually verified. An empty Findings block is allowed only if you checked every assigned row and found no defect.

| Requirement (inferred row) | Spec citation | Match | Matched task |
|---|---|---|---|
| INF-012: `original_is_draft` is never read from GitHub after the first record | source.md:208 | containment | Task 3 |
| INF-013: Effective only at `--monitor 3`; accepted and inert below. | source.md:216 | none | - |
| INF-014: `RunConfig` and `run_skill` do not change (F5): the guard is SKILL-orchestrated. | source.md:217 | none | - |
| INF-015: `--to` is idempotent, so a retry or a resume re-issue is safe. | source.md:234 | none | - |
| INF-016: Loaded lazily at L3 Wave 3, Wave 6 and Wave 8. | source.md:240 | containment | Task 8 |
| INF-017: No new python fence | source.md:241 | containment | Task 9 |
| INF-018: A `held` report always carries the reason and | source.md:247 | containment | Task 8 |
| INF-019: keep exactly one source for it (open item O1) | source.md:251 | none | - |
| INF-020: The `read-only` category is not used for these calls | source.md:255 | containment | Task 1 |
| INF-021: Acceptance trace (must appear in this order in the run log) | source.md:270 | containment | Task 11 |
| INF-022: Run `make sync-dev` at the end of every task that edits a file under | source.md:301 | containment | Task 8 |
| INF-023: the run that opens the PR must not enable the feature (`--merge-guard off`) | source.md:326 | containment | Task 1 |
| INF-024: A static test asserts `merge_guard.py` has no `gh` or `git` word. | source.md:322 | containment | Task 3 |
| INF-025: Cite tests and constants by symbol name | source.md:362 | containment | Task 1 |
| INF-026: Protocol prose written by the plan never carries `file:NNN` pointers | source.md:369 | none | - |
| INF-027: The L2 line is written into the SKILL.md output table | source.md:374 | containment | Task 9 |
| INF-028: a settled `not_applied` of either direction returns to `phase_before_request` | source.md:376 | containment | Task 3 |
