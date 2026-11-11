# Evidence record: pr-submit monitor, issues #381, #382, #456

Incremental record. Every number below comes from a saved run under `runs/` or a saved file named next to it.

## 1. Source revision

- Worktree: `/home/coder/workspaces/worktrees/IronClaude/pr-monitor-381-382-456`
- Branch: `clayphi/pr-monitor-381-382-456`
- Base: `0c2b41f8e440b306d4af317ccfaed06820a57179` (equal to `origin/master` when the baseline was taken; `git fetch origin` run first)
- Local interpreter: CPython 3.13.5 (CI uses 3.10; a difference to keep in mind, not a failure)

## 2. Baseline on unmodified master (taken BEFORE the first edit to `src/` or `tests/`)

Command set: `runs/run_suite.sh baseline` (`.dev/issues/381-382-456/run_suite.sh`), which runs the `.github/workflows/test.yml`
commands: `make sync-dev`; `pytest -v --tb=short -n auto --ignore=tests/cli/test_verify_sync_hooks.py` (no `--maxfail`);
swarm lanes `-m imm` and `-m inv`; `ruff check`, `ruff format --check`, plugin-loaded and fixtures checks, `make verify-deps`,
`make verify-sync`, `make lint-architecture`, the serial `tests/cli/test_verify_sync_hooks.py`; plus `git diff --check`.
A temporary HOME was used. Logs: `runs/baseline/*.log`; per-test results: `runs/baseline/*-results.txt`.

| Step | Result on master |
|---|---|
| Full suite (`-n auto`) | **1 failed, 25073 passed, 157 skipped, 2 xpassed** (925.98 s) |
| Swarm `-m imm` | 84 passed |
| Swarm `-m inv` | 107 passed |
| `tests/cli/test_verify_sync_hooks.py` (serial) | 7 passed |
| ruff check / ruff format --check | exit 0 / exit 0 |
| verify-deps, verify-sync, lint-architecture, plugin-loaded, fixtures, git diff --check | all exit 0 |

**Pre-existing failure (not mine):** `tests/unit/test_ccsession_tiers.py::test_shim_outlives_the_terminal_that_started_it`
(`runs/baseline/failing-ids.txt`). It also fails when run alone on unmodified master in this sandbox
(`assert _is_running(...)` is False: a process-lifetime check). It is counted in neither the "mine" nor the "regression" column.

## 3. #381 finding: not reproducible on current master

Replaying the real PR 377 data (review 5776286053 at 21:44:59Z, inline comment 4473733769 at 21:45:00Z, fetched with
`gh api`, saved as `tests/pr_submit/fixtures/cosmos-pr377-late-comment.json`) through UNMODIFIED master gives
`findings` with 1 actionable root, `findings` after 0 s in a simulated poll loop (`e2e/e2e-results.txt`, section B).
Cause: since PR 337 (commit `d4ac8a3d`, 2026-10-31) `_completion_time` (`classifier.py`) stretches completion to the
creation of the same reviewer's own roots of that review (same review id, same commit), so line 411
(`created > completed_at`) does not reject them. The issue text describes the line, not the behaviour.
Differential replay: all 11 real reviews with a late inline comment (gap at most 1 s) already classify as `findings`
under master in every open-thread case (`differential/analysis.txt`). The original stall's real cause is UNVERIFIED
(possibly an older installed copy; not determinable from the PR data).
Decision: NO code change for #381 and NO time gap (a gap would loosen a rule that already works and could
accept a root of another review). 8 tests pin the behaviour; all 8 PASS on unmodified master
(`runs/before-fix/late-comment.log`: 8 passed). The "must fail before" requirement cannot hold for #381 and is not claimed.

## 4. #382 and #456: the rule chosen

- Strict parse unchanged. Option 2 of #456 (accept a marker missing its `}`) NOT taken: the marker is the only
  evidence of `head` and `unresolved_count`; a guessed repair could turn a truncated body into a false clean.
- New `augment_marker_defect()` (classifier) names the case: newest formal Augment review of the expected head, snapshot
  complete, `classify` still `polling`, Cosmos token exactly once, marker unreadable (`marker_not_valid_json`,
  `marker_not_an_object`, `marker_comment_unreadable`). `augment_wait_outcome(..., marker_defect=)` turns `pending`
  into `incomplete` once the review is 60 s old.
- **Why a 60 s grace, not "stop at once":** the data shows Augment posting a corrected review seconds later on the same
  head: PR 455 malformed 18:29:51Z then well formed 18:30:18Z (27 s); PR 398 malformed 17:42:57Z then well formed
  17:43:12Z (15 s). Stopping on first sight would drop those. 60 s = at most two polls at the 30 s minimum.
- **After the grace:** the run continues with Codex alone (`reviewer_incomplete{reviewer: "augment", reason:
  "marker_malformed", detail}`) or ends as `timeout` when Codex is absent. A later readable review of the same head is
  still accepted (unchanged `classify`). The reason is reported on the first poll. `open_threads` lists the review's open
  Augment roots so findings are surfaced, never hidden.
- Not changed: `fsm.py`, the poll script (byte-identical to master), decline handling, round cap, autonomy ordinals.

## 5. New tests: failing before, passing after

- `tests/pr_submit/test_marker_malformed.py` (35 tests; real review bodies in 3 fixtures): on unmodified source
  **32 failed, 3 passed** (`runs/before-fix/marker-malformed.log`); the 3 that pass are the fixture check and the two
  "strict parse still polls" guards, which must hold before and after. After the fix: **35 passed**
  (`runs/after-fix/new-tests.log`).
- `tests/pr_submit/test_late_inline_comment.py` (8 tests): 8 passed before and 8 after (see section 3).

## 6. Differential replay over real data (read-only `gh api`, last 70 PRs)

Files: `differential/differential.csv` (full table), `differential-summary.json`, `analysis.txt`, scripts alongside.
Input: the real poll script's snapshot for each of the 70 PRs; every Augment review replayed at two moments
(+20 s inside the grace, +120 s after), with threads as on GitHub now and forced open (as they were), and three
watermark settings: 132 reviews, 1584 cases. Old = master copy extracted with `git archive`.

- 13 reviews with a malformed marker and 11 with a late inline comment: the same counts the coordinator found.
- `classify` result and selected findings: **identical in all 1584 cases** (0 differences).
- Healthy reviews (109; 1308 cases): **0 differences**, 0 defects reported.
- Only difference: 16 cases from 4 reviews (PR 377 5776522857, PR 430 5814185025, PR 448 5816979494, PR 455 5819041100),
  all malformed with no readable successor, all in the +120 s observation: Augment wait `pending` -> `incomplete`;
  round with Codex absent `polling` -> `timeout`; with Codex clean `polling` -> `clean` (Codex's result).
- The other 9 malformed reviews show no change: in the replay a readable review of the same head wins (for example PR 398,
  15 s later; PR 455 5819088356, 27 s later), or the case is still inside the 60 s grace at +20 s. The per-review
  table is `differential/analysis.txt`.
- The 11 late-comment reviews: `findings` under both old and new.

## 7. End to end through the real poll script (PRs 377 and 455)

`e2e/poll-pr377.json`, `e2e/poll-pr455.json` are real `poll-augment-review.sh` output (read-only, `--repo
IronbellyOrg/IronClaude`); `e2e/e2e-results.txt` is the monitor decision per entry point (`classify`,
`actionable_finding_comments`, `classify_codex`, `reviewer_activity`, `poll_outcome`, `augment_wait_outcome`,
`codex_wait_outcome`, `merge_wait`), OLD vs NEW, with a simulated 30 s poll loop and `--timeout 600`:

| Case | OLD (master) | NEW |
|---|---|---|
| PR 377 malformed review, Codex absent | `timeout` after 600 s, no reason | `timeout` after 60 s, reason line at first poll |
| PR 377 malformed review, Codex clean (stand-in) | `clean` after 600 s | `clean` after 60 s; Augment `reviewer_incomplete` |
| PR 455 first review (1 suggestion), Codex clean (as the issue reports) | `clean` after 600 s | `clean` after 60 s; reason + open thread 4507253589 listed |
| PR 455 first review, Codex absent | `timeout` after 600 s | `timeout` after 60 s |
| PR 455 malformed then well formed 27 s later | `findings` after 30 s | `findings` after 30 s (the later review is accepted) |
| PR 377 with the REAL Codex data | `timeout` after 600 s | `timeout` after 600 s (reason named at first poll) |
| 136 polls over every repo fixture, elapsed 0/30/300/600, with and without watermark | | identical in all 136 |
| `poll_outcome` over 4 states x 24 elapsed x 2 silence x 4 autonomy ordinals | | identical in all 768 |

PR 455's Codex state during the original stall cannot be recovered (Codex edits its summary comment in place); the
"Codex clean" rows use the issue's own report as an input and say so.

**Not fixed here:** on PR 377's real data Codex is active but its marker never reaches the final head, so Codex stays
`pending` and the round still waits the full 600 s. That is a Codex-side wait, a separate cause; this change only names
Augment's cause at the first poll there.

## 8. After the change: identical commands, test-by-test comparison

Full table: `runs/comparison.md`. Same commands as section 2 (`runs/after/*.log`).

| | Baseline (master) | After |
|---|---|---|
| Full suite | 1 failed, 25073 passed, 157 skipped, 2 xpassed | 2 failed, 25115 passed, 157 skipped, 2 xpassed |
| Test ids | 25076 | 25119 (+43: exactly the two new files, 8 + 35) |
| Ids that disappeared | | 0 |
| Swarm `imm` / `inv` / serial hook tests | 84 / 107 / 7 passed | 84 / 107 / 7 passed |
| ruff check, ruff format --check, verify-deps, verify-sync, lint-architecture, plugin, fixtures, git diff --check | all exit 0 | all exit 0 |

25073 - 1 + 43 = 25115. The one test that passed at baseline and failed after is
`tests/cli/test_install_keep.py::test_same_content_is_true_only_for_identical_readable_files`. It is a **timing flake
that exists on master**: it writes a file, compares, rewrites it with the same size and compares again, and
`filecmp.cmp` caches by size and modification time. On a pristine `git archive` copy of master's source it failed 4 of
6 runs; on this branch 6 of 6 in one batch and 1 of 3 passing in another. Nothing in this diff touches it
(`src/superclaude/cli/install_keep.py`, from #480). It is not fixed here (out of scope) and is not counted as caused by this
change. The other failure, `test_shim_outlives_the_terminal_that_started_it`, fails identically on master.
