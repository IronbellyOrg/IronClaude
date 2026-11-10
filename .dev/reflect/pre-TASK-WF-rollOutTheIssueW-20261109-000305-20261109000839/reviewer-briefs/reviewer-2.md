# Reviewer 2 brief (persona: qa, model: haiku, UC-1 pre-execution plan review)

You review a proposed plan before it runs. You are read-only: Read, Grep, Glob and codegraph only; no file writes, no shell. Start from an adversarial position: assume the plan misses requirements or carries risks the Tier 1 card missed. Plan: `/home/coder/workspaces/worktrees/IronClaude/issue-450/.dev/tasks/to-do/TASK-WF-rollOutTheIssueW-20261109-000305/TASK-WF-rollOutTheIssueW-20261109-000305.md` (121 lines). Your lens: coverage of the spec, acceptance criteria that can actually be checked, and data-exposure or safety risk (Tasks 3 and 5, Constraints, owner-run list). Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding. Read files at most 100 lines at a time.

## T1 card excerpt

## Coverage
All 10 inferred requirements map to a task or to the owner-run list (artifacts/coverage-matrix.md). No parsed IDs exist.

- F2 (data exposure risk): Task 5 reads owner-captured replies from `./artifacts/captured/` inside the package, and `.dev/tasks/` is always staged, so those files land in git; the token grep in Task 5 AC 2 covers only `tests/issue_watch/fixtures/`, not `./artifacts/captured/`. Severity: medium.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-09T00:14:00Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-450 projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-450

### .dev/tasks/to-do/TASK-WF-rollOutTheIssueW-20261109-000305/source.md:1-47

Spec body (47 lines). Read it whole from `/home/coder/workspaces/worktrees/IronClaude/issue-450/.dev/tasks/to-do/TASK-WF-rollOutTheIssueW-20261109-000305/source.md`. Requirement-bearing lines include 7 (inline prompt), 22 (what the issue asks for), 24 (owner-only steps), 30-42 (cheatsheet, including line 32 "must still pass after the fixture swap" and line 42 persisted `state_dir`).

```markdown
Roll out the issue watcher (issue #450, follow-up to #331): replace the _assumed_shape fixtures with captured real gh and Orca output after the owner-run live test (FU-1), fix the stale status line and the 59-name reason table in docs/designs/issue-watcher.md, prepare the shadow-run, lock, restart and cron steps (FU-2) as owner-run checklist items, keep enabled false until the owner flips it. Spec and runbook: docs/designs/issue-watcher.md, docs/designs/issue-watcher-setup.md. Code: src/superclaude/cli/issue_watch/, tests/issue_watch/
```

### .dev/tasks/to-do/TASK-WF-rollOutTheIssueW-20261109-000305/TASK-WF-rollOutTheIssueW-20261109-000305.md:108

```markdown
This task can start only after the owner-run live test. Precondition, checked first: `docs/designs/issue-watcher-live-test.md` exists in the checkout, and `./artifacts/captured/` in this package holds the redacted replies the owner captured, one file per fixture name from the Task 3 list. If the precondition fails, the task stops as blocked, writes the missing items to `./artifacts/t5-blocked.md`, and changes no file.
```

### .dev/tasks/to-do/TASK-WF-rollOutTheIssueW-20261109-000305/TASK-WF-rollOutTheIssueW-20261109-000305.md:116-120

```markdown
Acceptance criteria:
- Every fixture with a captured file has `"_assumed_shape": false` and a `source` naming `docs/designs/issue-watcher-live-test.md`; the list of swapped and unswapped fixtures is saved to `./artifacts/t5-swap-list.md`, and every unswapped one appears as uncaptured in the live-test record.
- No fixture contains a token-shaped string: `grep -r -E "gh[pousr]_[A-Za-z0-9]{20,}|github_pat_" tests/issue_watch/fixtures/` prints nothing.
- `uv run pytest tests/issue_watch/ -q` passes; its output is saved to `./artifacts/t5-pytest.log`.
- `git diff --name-only` for this task lists only files under `tests/issue_watch/fixtures/_assumed_shape/` and `tests/issue_watch/test_github.py`.
```

Also check yourself: plan lines 17-34 (Constraints, owner-run list), 70-85 (Task 3), 102-115 (Task 5 body); `tests/issue_watch/fixtures/_assumed_shape/` (19 files); `tests/issue_watch/test_github.py` (the test `test_every_assumed_shape_fixture_parses_and_is_labelled`); `docs/designs/issue-watcher-setup.md` around lines 576-596 (section 14.1). Verify the card's own citations too.

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|--------------------|---------|--------|-----------|
| INF-001: replace _assumed_shape fixtures with captured output (FU-1) | Task 5; Task 3 sheet | covered, exposure risk (F2) | source.md:7 |
| INF-006: live-test doc written by the owner | owner-run list; Task 5 precondition | covered | source.md:22 |
| INF-008: watcher tests still pass after the swap | Task 5 AC 3 | covered | source.md:32 |
| INF-009: shadow run, lock and restart tests before enabled=true | Task 4 checklist; owner-run list | covered | source.md:22 |

Return in your final message only: a list of findings, each with `id`, `severity` (high|medium|low), `deviation_class` (UC-1: use `plan-gap`), `claim`, `evidence` (file:line plus a verbatim quote of at most 2 lines), and `recommendation`; then `self_reported_confidence: <0-1>`. Confirm or refute F2 explicitly, and list any spec span missing from the coverage slice.
