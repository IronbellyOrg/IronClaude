# Reviewer 1 brief (persona: analyzer, model: sonnet, UC-1 pre-execution plan review)

You review a proposed plan before it runs. You are read-only: Read, Grep, Glob and codegraph only; no file writes, no shell. Start from an adversarial position: assume the plan has defects the Tier 1 card missed. Plan: `/home/coder/workspaces/worktrees/IronClaude/issue-450/.dev/tasks/to-do/TASK-WF-rollOutTheIssueW-20261109-000305/TASK-WF-rollOutTheIssueW-20261109-000305.md` (121 lines). Your lens: are the plan's edits and acceptance criteria correct against the real docs and code (Tasks 1, 2, 4)? Read files at most 100 lines at a time.

## T1 card excerpt

- F1 (acceptance criterion may be unsatisfiable): Task 2 AC 4 loops over every backticked name in the 4.3 table and requires zero misses, but the table's Meaning column for exit 7 backticks status words `failed`, `unknown`, `abandoned` (`docs/designs/issue-watcher.md:163`), which are entry statuses, not reason keys (grep of `src/superclaude/cli/issue_watch/audit.py` for `"failed":` etc. finds none; `"cycle_complete":` is at line 64, `"spawn_error":` at 87). Plan line 65 states the check. As written the check would report 3 misses. Severity: medium.
- F3 (wording): Task 4 AC 1 uses `grep -c` (a line count) to mean "one in 8.7 plus the 15.3 row"; correct only if 8.7 states the schedule on one line. Severity: low.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-09T00:14:00Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-450 projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-450

### docs/designs/issue-watcher.md:155-164

```markdown
| Code | Meaning | Reasons that produce it |
|---|---|---|
| 0 | Cycle complete (any number of launches), `disabled`, `disabled_mid_cycle`, `not_enabled` | `disabled`, `disabled_mid_cycle`, `not_enabled`; every skip reason |
| 2 | Usage, config, platform, origin, Orca probe | `config_invalid`, `approvers_invalid`, `platform_unsupported`, `worktree_invalid`, `origin_mismatch`, `orca_not_found`, `account_id_mismatch` |
| 3 | GitHub auth, scope, timeout, non-JSON | `login_invalid`, `gh_auth_failed`, `gh_timeout`, `gh_non_json`, `project_read_failed` |
| 4 | Discovery truncated or duplicated | `truncated`, `discovery_duplicate` |
| 5 | Rate limited | `rate_limited`, `rate_limit_clamped` |
| 6 | Store or lock | `store_invalid`, `store_missing`, `lock_missing`, `lock_invalid`, `state_dir_unwritable` |
| 7 | An entry was written `failed`, `unknown` or `abandoned` `spawn_error` this cycle | `prompt_invalid`, `revalidation_transient`, `launch_unknown`, `spawn_error` |
| 75 | Lock held or the lock inode changed | `lock_held` |
```

### .dev/tasks/to-do/TASK-WF-rollOutTheIssueW-20261109-000305/TASK-WF-rollOutTheIssueW-20261109-000305.md:61-65

```markdown
Acceptance criteria:
- `grep -c "cycle_complete" docs/designs/issue-watcher.md` and `grep -c "cycle_crashed" docs/designs/issue-watcher.md` each print at least 2.
- `grep -n "spec reason table\|equal to the spec's reason table" docs/designs/issue-watcher.md` prints nothing.
- The section 4.3 table has a row whose first cell is `1` naming `cycle_crashed`, and its exit 0 row names `cycle_complete`.
- Every reason name in section 4.3 of the design is a key of `REASON_TABLE`: the check (a loop over the backticked names in that table, each tested with `grep -c "\"<name>\":" src/superclaude/cli/issue_watch/audit.py`) and its output are saved to `./artifacts/t2-reason-check.log`, with zero misses.
```

### src/superclaude/cli/issue_watch/audit.py:64

```python
    "cycle_complete": ("cycle", 0),
```

### src/superclaude/cli/issue_watch/cycle.py:228

```python
    enabled = raw.get("enabled", False)
```

Also check yourself: plan lines 38-46 (Task 1), 87-100 (Task 4), `docs/designs/issue-watcher.md` around lines 1-5 and 697-722, `docs/designs/issue-watcher-setup.md` around lines 268-284 and 598-649, and `src/superclaude/cli/issue_watch/audit.py:26-103` (`REASON_TABLE`, 59 names). Verify the card's own citations too.

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|--------------------|---------|--------|-----------|
| INF-002: fix the stale status line | Task 1 | covered | source.md:7; issue-watcher.md:3 |
| INF-003: fix the 59-name reason table | Task 2 | covered, AC 4 suspect (F1) | source.md:7; issue-watcher.md:709, 718, 155-164 |
| INF-004: shadow-run, lock, restart, cron as owner-run checklist | Task 4 | covered | source.md:7; plan 87-100 |
| INF-005: keep enabled false | Constraints; Task 4 AC 3 | covered | source.md:7; cycle.py:228 |
| INF-007: cron `0 */5 * * * *` | Task 4 (8.7) | covered, AC 1 wording (F3) | source.md:22 |
| INF-010: persisted `state_dir` | Task 4 (8.7) | covered | source.md:42 |

Return in your final message only: a list of findings, each with `id`, `severity` (high|medium|low), `deviation_class` (UC-1: use `plan-gap`), `claim`, `evidence` (file:line plus a verbatim quote of at most 2 lines), and `recommendation`; then `self_reported_confidence: <0-1>`. Confirm or refute F1 and F3 explicitly.
