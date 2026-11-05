# Issue #302 handoff: 03 implement report

- Task: task_81fa7346d9b9 (dispatch ctx_5d16ae12c2f5)
- Branch: ironbelly/feat-sc-issue-command
- Command: `/sc:implement .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/TASK-WF-scIssueCommand-20261104-064713.md`

## 1. Final package path

`.dev/tasks/done/TASK-WF-scIssueCommand-20261104-064713/` (the archive helper reported `{"status": "archived", ...}`). The fresh independent FINAL review returned `pass` for all 17 tasks; the ledger ends with `FINAL: pass ... state=8680a4f9...` and the helper's `ARCHIVE: start` line. `<package>` below means this folder.

## 2. Per-task status

Every task has a `complete verdict=compliant` line in the ledger (`progress.md`). Each verdict came from a fresh reviewer subagent (17 first reviews plus one re-review), never from the implementer.

| Task | What | Status | Note |
|---|---|---|---|
| T1 | `scripts/origin_repo.py` + `tests/skills/test_issue_repo_resolution.py` (includes the C2 `E-FOREIGN-REPO` claim-URL check) | passed | First review found one blocking finding (scheme-less `github.com/...` claim URLs got a wrong code and a docstring that disagreed); fixed once, re-review passed (`artifacts/retries/T1/review-1.md`, `probe-1-1.md`) |
| T2 | `scripts/clickup_claim.py` + `tests/skills/test_clickup_claim.py` | passed | Endpoint and field shapes taken from the ClickUp v2 reference (first page is 0) |
| T3 | three `issue-worker-t*` agents + `tests/skills/test_issue_worker_agents.py` | passed | C1 applied |
| T4 | fourteen templates | passed | |
| T5 | five refs | passed | |
| T6 | `SKILL.md` (153 lines) | passed | |
| T7 | `tests/skills/test_issue_protocol.py` | passed | Also changed two f-strings in `origin_repo.py` that held the literal brace placeholder text the new test bans (same output) |
| T8 | `commands/issue.md` (100 lines) + `tests/commands/test_issue_command.py` | passed | |
| T9 | guard test replaced; `issue` added to `_POST_REFRESH_ADDITIONS` | passed | |
| T10 | routing guide row, plugin byte copy, `_OTHER_COMMANDS` | passed | |
| T11 | developer guide 4.1 and 4.3 | passed | |
| T12 | user command reference row and section | passed | |
| T13 | `make sync-dev`, `make verify-sync`, path grep vs `origin/master` | passed | 168 hits on both sides, none in the new primitives |
| T14 | targeted suite, full suite, lint, verify-sync | passed | |
| T15 | worker smoke spawns | passed as a record; the checks themselves are **pending** | C3: agents load at session start; this session predates `make sync-dev` |
| T16 | ClickUp smoke claim | passed as a record; the check itself is **pending** | `CLICKUP_*` not set; C3 |
| T17 | section 20 acceptance record + runbook | passed with 3 minor notes | Notes in `artifacts/retries/T17/notes.md` (an ambiguous test-name shorthand in row 4, an unused `t16-input.md` instruction in runbook step 1, and step 5 not saying how to start a session without `CLICKUP_API_TOKEN`). Minors are recorded, not edited, under the protocol |

Ledger slips: two evidence line numbers in the T2 and T4 ledger lines were wrong; the corrections are in `artifacts/ledger-errata.md` (the ledger is append-only).

## 3. Full test suite

| Run | Passed | Failed | Skipped | Errors | Other | Log |
|---|---|---|---|---|---|---|
| `uv run pytest` (full) | 14830 | 0 | 136 | 0 | 2 xpassed, 32 warnings; rc=0; 469 s | `<package>/artifacts/t14-full-pytest.log` (outcome line 15072) |
| `uv run pytest tests/commands tests/core tests/skills tests/recommend tests/cli/test_issue_body_templates.py` | 1411 | 0 | 0 | 0 | rc=0 | `<package>/artifacts/t14-targeted.log` (line 1423) |
| `uv run pytest tests/core tests/commands` | 299 | 0 | 0 | 0 | rc=0 | `<package>/artifacts/t10-core-commands.log` (line 312) |

No failure, so no master comparison worktree was needed (`artifacts/t14-failures.md`).

Side effect handled: the full suite rewrites the tracked file `.dev/releases/current/cliEval/evidence/T02.15/perf.json` (an existing perf test, `tests/cli/eval/test_perf_home_setup.py`). It was restored with `git restore` so the branch carries no unrelated change.

## 4. Lint and verify-sync

- `make lint`: `All checks passed!`, rc=0 (`artifacts/t14-lint.log`). Ruff was missing from this worktree's `.venv`; `make install` (the project's setup target) was run first (`artifacts/t14-make-install.log`). No project file changed.
- `make verify-sync`: `All components in sync.`, rc=0 (`artifacts/t13-verify-sync.log`, `artifacts/t14-verify-sync.log`).
- `make sync-dev` ran in Task 13 (`artifacts/t13-sync-dev.log`). Nothing under `.claude/` is staged.

## 5. Files created or changed

Created (unstaged; nothing committed):

- `src/superclaude/commands/issue.md`
- `src/superclaude/skills/sc-issue-protocol/SKILL.md`
- `src/superclaude/skills/sc-issue-protocol/refs/{claim,create,chains,labels,tiers}.md`
- `src/superclaude/skills/sc-issue-protocol/templates/` (14 files: `issue-feature-simple.md`, `issue-feature-complex.md`, `issue-bug-simple.md`, `issue-bug-complex.md`, `summary.md`, `accuracy-check-comment.md`, `claim-comment.md`, `next-steps.md`, `scout-report.md`, `recommend-record.md`, `description.md`, `flags-decision.md`, `draft-notes.md`, `create-review-comment.md`)
- `src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py`, `scripts/clickup_claim.py`
- `src/superclaude/agents/issue-worker-t3.md`, `issue-worker-t2.md`, `issue-worker-t1.md`
- `tests/skills/test_issue_repo_resolution.py`, `test_clickup_claim.py`, `test_issue_worker_agents.py`, `test_issue_protocol.py`
- `tests/commands/test_issue_command.py`

Changed (unstaged):

- `src/superclaude/core/HOW-WE-WORK.md` and its byte copy `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` (one "Other commands" row)
- `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` (sections 4.1 and 4.3)
- `docs/user-guide/commands.md` (UTILITIES row and `/sc:issue` section)
- `tests/cli/test_issue_body_templates.py`, `tests/core/test_how_we_work_routing_table.py`, `tests/recommend/test_routing_refresh.py`

Generated by `make sync-dev` (gitignored, never staged): the `.claude/` dev copies of the command, skill and agents.

Package bookkeeping (staged with `git add .dev/tasks`): `progress.md` and `artifacts/` of the plan package, plus this report.

## 6. Pending live checks and runbook

Runbook: the "Post-restart runbook" section at the end of `<package>/artifacts/t17-acceptance.md`. Pending, in runbook order:

1. Prepare: export `CLICKUP_API_TOKEN`, `CLICKUP_WORKSPACE_ID` and `CLICKUP_LIST_IDS` (the test task's list) in your own shell; pre-approve scratch test issues; start a new Claude Code session in this checkout.
2. Worker smoke spawns for `issue-worker-t3`, `-t2`, `-t1` (Task 15, acceptance item 7 second half).
3. ClickUp smoke claim, run twice (Task 16, item 5 second half).
4. Live foreign-repo claim `/sc:issue --claim https://github.com/IronbellyOrg/no-such-repo-sc-issue-probe/issues/999999999` (item 4 live; the check itself is already verified by unit tests).
5. Live claims on approved scratch issues (items 1, 2, 3, 5 first half, 8).
6. Three live creates at quick, standard and deep (item 6).

Acceptance status: items 4 and 9 run; items 7 and 8 static halves run; items 1, 2, 3, 5 and 6 pending. Known runbook gaps (T17 minor notes): step 1's `t16-input.md` file is not read by any step, and step 5 does not say that its first claim needs a session started without `CLICKUP_API_TOKEN` exported (start that session before step 1's exports, or unset the variable and restart).

## 7. How coordinator constraints C1 to C4 were applied

- **C1** (no read-only permission mode on workers): the three agent files have no `permissionMode` key; `tests/skills/test_issue_worker_agents.py::test_no_permission_mode` asserts it is absent. Recorded in `<package>/artifacts/coordinator-constraints.md` and as T3.AC4.
- **C2** (no live run; deterministic `E-FOREIGN-REPO` check): `origin_repo.py --claim` checks the claim argument against `origin` (exit 3 `E-FOREIGN-REPO`, distinct from exit 1 `E-NO-ORIGIN`; exit 4 `E-NOT-AN-ISSUE` for `/pull/<N>`). Unit tests cover same repo, foreign owner, same owner with a different repo, repo-name and owner-name prefixes, `/pull/<N>`, trailing slash, fragment and query, scheme-less and `git@` forms, and digits in owner or repo never becoming N. Claim Wave 0 calls it (`SKILL.md`, `refs/claim.md`). No `/sc:issue` claim or create was run against anything; item 4 is recorded as run by those tests, with the live run pending.
- **C3** (no mid-run asks): Tasks 15 and 16 and every live acceptance item are recorded pending with reasons; Task 17's artifact ends with the runbook above.
- **C4** (other minors only as in-task correctness fixes): applied F-03, F-05, F-08, F-13, F-16, F-17, F-18 (plus F-01, F-02, F-06, F-11, F-12, F-14 through C1-C3); not applied F-04, F-07, F-09, F-10, F-15. Per-finding reasons: `<package>/artifacts/round2-minor-findings.md`.

Repo rules: UV only; no `gh` write and no upstream interaction (the only network git call was `git fetch origin` in Task 13); nothing committed or pushed; HEAD is still `119622e3`.
