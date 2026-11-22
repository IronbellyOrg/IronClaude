# Explanation (advanced): issue-pipeline approval core

Source: origin/master, `src/superclaude/cli/issue_pipeline/` (read via `git show origin/master:<path>`). Codegraph not used (graph:stale).

## One-paragraph model

A person-opened coordinator starts a plan-writing agent for a GitHub issue. The agent writes plan files. A human approves the plan in one of three ways: an Orca reply to the worker's `ask`, an approval label on the issue, or a comment that is exactly `approved`. This package decides, from facts only, whether an approval is real, ties it to a hash of the plan files, and records it once so the next stage never starts twice.

## Layers, bottom to top

1. `plan_hash.py`: SHA-256 over sorted plan files. Each file adds an 8-byte length of its name, the name, an 8-byte length of the bytes, the bytes (lines 77-90). Refuses absolute names, `..`, symlinks, missing, outside-dir, non-files (lines 24-36, 39-74). Returns only closed reason words.
2. `approval_line.py`: two accepted texts, matched whole with no trimming: `approved` (short) and `approved ap-<issue>-plan-<12 hex> plan-sha256=<64 hex>` (long). `check` recomputes the hash from the plan files and compares (lines 43-62). Short form returns `refused:bare` here, because a bare word is valid only on the comment channel, where the position in time binds it to the plan.
3. `approval_record.py`: a file-based ledger in its own directory (0700, `lock` file 0600). Two row kinds. Adoption row keyed (issue, stage): `reserved`, then `started` (with Dispatch id) or `uncertain`. Approval row keyed (issue, stage, plan hash): `recorded`, `instructed`, `acked`, `revoked`. Every mutation takes the watcher's `FileStore.lock()` (non-blocking flock, a second caller gets `lock-held`, exit 75). Rows are validated against fixed regexes on every read; any deviation is `row-invalid`. A label plus a comment for one plan append evidence to one row, never make two (lines 313-371). Replaying the same (channel, id) evidence changes nothing, so a replay cannot undo a revoke (lines 360-365).
4. `stage_predicates.py`: pure function `evaluate` over projected facts. Plan reply = latest comment by the host login with a hidden marker `<!-- sc:stage:plan id=... plan=... -->`; it must be unedited, and the live plan files must still hash to the marker. Label channel and comment channel each have closed reasons. Equal timestamps never count as "after" (fail closed). Result states: `no-plan-reply`, `plan-reply-invalid`, `plan-changed`, `awaiting-approval`, `approved`, `revoked`.
5. `reads.py`: GitHub reads reuse the watcher's budgeted, paged `gh` helpers. The comment body is reduced to booleans and fixed-pattern ids inside the `jq` expression (`COMMENTS_JQ`), so comment text never reaches Python; Python re-validates each captured value. Events, comments and edits are read under one call budget; any failure returns a closed reason, never a partial approval.
6. `cli.py`: the `superclaude issue-pipeline` group: `plan-hash`, `check-approval`, `init`, `adopt-create`, `adopt-mark`, `record-create`, `record-show`, `record-mark`, `stage-status`. All verbs print closed words or JSON. `stage-status` writes nothing.
7. `brief.py` + `templates/worker-brief.txt`: builds the Task spec for the plan-writing worker from a fixed template; only an integer issue number and an enum complexity reach it. Type `bug` is refused. The rows stop before `/sc:implement` and `/task`.

## Why the design looks this way

- Trust boundary: the repo is public, so only the assignee or listed approver ids count, and only account type `User`.
- Known unfixable risk: the worker shares the host's single GitHub login, so it could approve its own plan. The code carries flags (`actor_is_host_login`, `assignee_is_host_login`) instead of hiding this (Decision 4).
- Write-ahead: the adoption row is written (`reserved`) before `worker-start`, so a crash between start and mark leaves `reserved`, and the next caller gets `uncertain-launch`, never a second start.
- Fail closed: unknown edit evidence, equal timestamps, partial reads, unreadable plan files all deny approval.

## Built versus not built

Built: everything above plus tests. Not built: Plan B (the coordinator route that calls these verbs, and guard change G2), and the brief builder has no CLI verb (only a Python function and tests). The FU-1 runbook was run on throwaway issue 452 on 2026-11-17 and its record is filled in.
