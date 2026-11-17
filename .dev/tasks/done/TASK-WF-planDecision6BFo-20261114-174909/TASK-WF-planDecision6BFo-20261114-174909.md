---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-planDecision6BFo-20261114-174909
version: "1"
priority: Medium
created_date: "2026-11-14"
---

# Issue watcher: hand a claimed issue to a coordinator-started worker (Decision 6 = B)

Source: ./source.md
Goal: A person-opened coordinator can start the plan-writing agent as a supervised Orca worker for a watcher-claimed issue, approve its plan through Orca's own ask and reply, and accept an approval from the issue's label or an "approved" comment without ever starting the stage twice.

## Constraints

- Plan only. The owner approved this plan with fixes on 2026-11-15 and asked for the review changes on the same day; every owner decision in Task 19 is answered, and what stays open are facts the first live test must measure (Task 8), not decisions. Running `/sc:implement` from this plan still needs the owner's separate go. No push, PR, GitHub write or Orca write verb is authorized by this plan.
- This is Plan A of two. It holds only work that can run now, in this file order: Task 16 first (its own branch from origin/master, its own pull request later), then Tasks 1, 2, 8 (a document only), 3, 4, 5, 6, 7 and 19. Task numbers are stable across both plans, so they are not contiguous here. `/sc:implement` runs items in file order and ignores `Depends on` and `Start condition` text, so the order of the items is the gate. A `Depends on` line names only a task that appears earlier in this file. Plan B lives in its own package folder, `.dev/tasks/to-do/TASK-WF-planDecision6BFo-20261114-174909-planB/plan-b-gated-tasks.md` (Tasks 20, 9, 10, 11, 12, 13, 14, 15, 17, 18). It opens with an owner-run gate item, the first live test recorded in docs/designs/issue-pipeline-fu1.md, and is not run from this file.
- Archive. Plan B sits in its own package folder, so archiving this plan's folder when it completes does not move Plan B.
- Owner input O-1 (not chosen by this plan): the number of one GitHub issue that the owner wrote, which Task 4 records real GitHub responses for. It is written by the owner into `tests/issue_pipeline/fixtures/recorded/OWNER-INPUT.md` as one line `ISSUE: <number>`. An executor that finds no such line stops at Task 4 and never picks an issue.
- Rebase first. This plan was written on base 0406ef5b0. origin/master is now d4d1662a8 and already holds PR #539 (sweep) and PR #548 (the D2 "claim-only" superseded note in docs/designs/issue-watcher.md). Every task below starts from a worktree based on current origin/master.
- Evidence for every factual claim is in ./artifacts/validation.md (read-only measurements, file and line citations, and what is UNVERIFIED). Real code locations are in ./artifacts/codegraph-grounding.md.
- Chosen claim-side change: B1b, the watcher claims with `--pipeline none` and the coordinator runs the existing `orca_worktree.py worktree` step, then `worker-start --worktree path:<that worktree>`. The owner confirmed it on 2026-11-14 and again on 2026-11-15 (Q35 = B1b; the first reply wrote "Q53 b1b" next to "2. Approved", read as Q35). B2, a new claim level, is not built.
- Owner answers: see Task 19.
- Owner decision Q34 (2026-11-14): the plan-writing worker runs without the launch-level guard (G1) for ONE test issue only. The written acceptance must cover the loss of the guard itself (no block on commit, push, merge, GitHub writes or /sc:implement), the owner writes that issue's text, and it is not stretched from the Decision 1 acceptance of permission checks off. Before any other issue runs through this flow, the guard is changed (G2, Plan B Tasks 13 to 15).
- Accepted earlier and carried here: only the coordinator tells the worker to proceed; one person-opened coordinator owns all watcher-claimed issues on this host with a lock per issue; nothing starts while the coordinator is down; one grant row per pipeline issue; one GitHub login on this host means an agent could apply the approval label or post the approval comment (Decision 4, accepted).
- New code goes in a new package `src/superclaude/cli/issue_pipeline/` and tests in `tests/issue_pipeline/`. The tests in tests/issue_watch/test_module_boundaries.py pin what each issue_watch module may import, and tests/issue_watch/test_no_text.py forbids a gh call that asks for comment text, so issue_pipeline imports from issue_watch and never the reverse.
- Never edit `.claude/` mirrors; edit `src/superclaude/` and run `make sync-dev`. Always stage `.dev/tasks` and the `src/` changes, never `.claude/`; commit only when the owner asks.
- The merged requirements file in the brainstorm folder is not edited by any task; Task 19 writes the change list for it inside this package.
- Every command is run with `uv run`.

## Phase 1: Remove the plain `approved` route (own branch from origin/master, own pull request later)

## Task 16: Remove the plain `approved` route from every worktree-level claim

Remove the way a person or an agent releases a governed worktree-level agent by typing `approved`. The owner decided this on 2026-11-14 (Q39, restated that day): it applies to every worktree-level claim, now, and replaces the earlier default of keeping it for person-run claims until G2 exists. The task has no dependency on the first live test, on a coordinator, on G2 or on any other task of this plan.

The mechanism lives in two places, and both change:
- The guard hook `src/superclaude/hooks/scripts/launch-level-guard.sh` and its plugin copy `plugins/superclaude/hooks/scripts/launch-level-guard.sh`. At level worktree it accepts a whole prompt `approved`, `approved.` or `approved!` (trimmed and lower-cased) as the release, by writing the session's `.ok` file (lines 349-354, the match at line 353; the comment at lines 341-346 describes it). That match is removed. The other accepted form stays: a prompt whose first line starts `/sc:implement`, `/sc:task` or `/task` (the regex at line 347).
- The launch prompt template `src/superclaude/skills/sc-issue-protocol/templates/launch-prompt.md`, worktree block, line 23: "A human approves by replying `approved` in this session or by running the printed implement command." becomes a sentence that a human approves only by running the printed implement command in this session, a prompt whose first line starts `/sc:implement`, `/sc:task` or `/task`.

After the change a governed worktree-level agent is released only by a prompt whose first line starts `/sc:implement`, `/sc:task` or `/task`. Typing `approved` does nothing.

Wording that repeats the old route changes with it: the LL-IMPL hint in the guard (line 45, "or reply approved, in this session"); `src/superclaude/skills/sc-issue-protocol/refs/claim.md` line 140 (final output: "reply `approved` in its tab to let it continue"); and the sentences that describe the route in `docs/designs/sc-issue-claim-pipeline-flag.md` (lines 162 and 232), `docs/designs/sc-issue-launch-level-hook.md` (line 236, the LL-IMPL row), `docs/user-guide/commands.md` (line 377) and `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md` (line 320). These stay as they are: the `.ok` state label `worktree (approved)` (guard line 117) and the tests that block `approved` text sent through `CronCreate`, `SendMessage`, `tmux` or `orca terminal send` (the LL-TURN and LL-ESCAPE cases), because they are other blocks, not the release.

Tests and fixtures that pin the old wording, all changed in the same commit (line numbers are at base d4d1662a8 and are found again after any rebase):
- `tests/hooks/test_launch_level_guard.py`, the approval cases from line 3673 on: the accepted list at lines 3685-3689 (`approved`, `Approved.`, `approved\n` and `\t\r\napproved!\r\n`) becomes a rejected list; the rejected list at 3703-3711 stays rejected; the `.ok` check at 3723-3729, the parametrized cases at 3741 and 3750 and the cases at 3760-3764 lose the `approved` value and keep `/sc:implement x` and `/task y`.
- `tests/hooks/test_launch_level_guard_l2_tokens.py` (lines 149-151), which requires the plugin copy to be byte-identical to the source guard.
- The fixture `tests/hooks/fixtures/launch_level/ob_h1/item5-monitor-approved-line.json` and its row in `tests/hooks/fixtures/launch_level/ob_h1/README.md` (line 15): the prompt `approved` stays a valid input, and a test now asserts it releases nothing.
- A new test in `tests/skills/test_issue_orca_worktree.py` renders the launch prompt for level worktree and fails if it tells the agent to wait for a reply of `approved`.

Risks, stated in the touched texts and in the pull request description:
- A person with no coordinator can no longer release a governed agent by typing `approved`. They type `/sc:implement <plan path>`, `/sc:task` or `/task` themselves, or later use the coordinator route of Tasks 14 and 15, which this task does not wait for.
- A governed worktree-level agent already waiting for `approved` when the installed guard is refreshed with `superclaude install` can then be released only by one of those three prompts. Before installing, check `ls ~/.claude/state/launch-level/sessions/` for sessions in flight.
- A session that already has its `.ok` file stays released.
- The guard is a security hook, so this change gets its own independent review before merge (Task 13 states the same rule for G2). Tasks 14 and 15 later edit the same guard file and its plugin copy, so whichever lands second rebases onto the other.

Runs first in this plan, on its own branch from origin/master, with its own pull request later (opened only on the owner's go, through `/sc:pr-submit --monitor 3`). Start condition: can start now; it does not wait for the first live test, a coordinator, Plan B Task 13, or Plan B Tasks 14 and 15.

Acceptance criteria:
- After the change no template, guard match, guard hint or final-output line tells a person or an agent that typing `approved` lets the agent proceed, at any worktree-level claim; a search for the word `approved` in the two guard copies, the launch prompt template and `refs/claim.md` finds only the `worktree (approved)` label and the unrelated LL-TURN and LL-ESCAPE text.
- A hook test shows that at level worktree the prompts `approved`, `Approved.` and `approved!` write no `.ok` file and a later `/sc:implement` skill call is still blocked with LL-IMPL, and that a prompt whose first line starts `/sc:implement`, `/sc:task` or `/task` writes the `.ok` file and then allows `/sc:implement`.
- `uv run pytest tests/hooks/ tests/skills/test_issue_protocol.py tests/skills/test_issue_orca_worktree.py -v` passes with the old-route cases changed as listed, and `make sync-dev` followed by `make verify-sync` passes with no staged `.claude/` path.

## Phase 2: Approval core and the live-test runbook (no dependency on the first live test)

## Task 1: Add the plan-hash function and the `issue-pipeline` command group

Create `src/superclaude/cli/issue_pipeline/__init__.py`, `src/superclaude/cli/issue_pipeline/plan_hash.py` and `src/superclaude/cli/issue_pipeline/cli.py`, register the group as `issue-pipeline` in `src/superclaude/cli/main.py` next to the `issue_watch_group` registration (main.py:563-565), and add `tests/issue_pipeline/test_plan_hash.py`.

`plan_hash.compute(report_dir, names)` returns the SHA-256 over a named list of plan files. Names are relative to the report directory, sorted by their bytes, each file contributing its name, its length and its bytes (so moving bytes between two files changes the hash). It refuses an absolute name, a name with `..`, a symlink, a missing file and a file outside the directory. The `plan-hash <report-dir> <name>...` verb prints the file list and the hash; this is what the coordinator puts in the plan reply and what the worker recomputes.

Start condition: can start now.

Acceptance criteria:
- `uv run superclaude issue-pipeline plan-hash <dir> a.md b.md` prints the ordered file list and a 64-character lowercase hex hash, and the same inputs in a different argument order print the same hash.
- A test shows that changing one byte, renaming a file, swapping bytes between two files, or adding a file each change the hash.
- A test shows that a symlink, an absolute name, a `..` name and a missing file each exit non-zero with a closed reason and print no file text.
- `uv run pytest tests/issue_pipeline/test_plan_hash.py -v` passes, and a test in tests/cli confirms the `issue-pipeline` group is registered without changing any existing registration test.

## Task 2: Define the approval line and add the `check-approval` verb

Depends on: Task 1

Create `src/superclaude/cli/issue_pipeline/approval_line.py` and add the verb to `src/superclaude/cli/issue_pipeline/cli.py`, with `tests/issue_pipeline/test_approval_line.py`.

One module owns the only two accepted approval texts: the short form `approved` and the long form `approved <record-id> plan-sha256=<64 hex>`, matched as the whole text with no trimming. The record id is `ap-<issue>-plan-<first 12 hex of the plan hash>`, so it is the same for the same (issue, stage, plan version). `check-approval <report-dir> <name>... --line "<text>"` is what the worker runs: it recomputes the hash with Task 1, returns `ok` for the long form only when the id and the hash both match, returns `refused:mismatch` for any other hash, and treats a bare `approved` as acceptable only for the comment channel (the coordinator, not the worker, converts it to the long form before it replies).

Start condition: can start now.

Acceptance criteria:
- A test table accepts `approved` and `approved ap-9-plan-0123456789ab plan-sha256=<64 hex>` and rejects every variant: leading or trailing space, upper case, a second line, a wrong id shape, a 63-character hash, a 65-character hash, and text after the hash.
- `check-approval` against a plan directory returns `ok` for the matching long form, `refused:mismatch` after one byte of a plan file changes, and `refused:bare` for a bare `approved` sent to the worker.
- No function in this module reads or prints anything except the closed result words.
- `uv run pytest tests/issue_pipeline/test_approval_line.py -v` passes.

## Task 8: Write the first-live-test runbook for B, including the guard-loss acceptance

Depends on: Task 1

This task writes a document only; it needs no code from Tasks 3 to 7 (Task 1 is named only because the runbook tells the coordinator and the worker to compute the plan hash with it).

Create `docs/designs/issue-pipeline-fu1.md`. It lists preconditions a to k, each with its exact read-only or throwaway step, the value to record, and what a failure means. Preconditions a to j come from section 7 of ./artifacts/validation.md: the real `worker-start` argv and permission flags; `worker-start --worktree path:<exact existing worktree a script created>` and exactly one terminal afterwards; the `ask` and `reply` round trip for a worker started with a spec, including whether the reply arrives as type `status` and a narrow `--types` filter misses it; the launch receipt shape and the Dispatch id; the plan hash computed identically by coordinator and worker; guard interaction under G1; `ask` timeout and resume by message ID; a worker staying in `ask` while the coordinator is down; worktree reuse when the claim runs twice; and the GitHub stage facts (who moved a Project Status, label event shape). Precondition k is new: whether a comment typed in the GitHub web editor round-trips as exactly `approved`, and what a comment edit does to `lastEditedAt`.

The runbook also holds the written acceptance the owner must give before the test, worded to cover the guard loss: "I accept, for test issue #<N> only, that the plan-writing worker runs with permission checks off and with no launch-level guard (nothing blocks a commit, push, merge, GitHub write or /sc:implement), reading issue text that I wrote myself. This is separate from my 2026-11-14 acceptance of permission checks off." The test issue text is written by the owner. The runbook names the existing gates that still apply (a separate live-test grant, a reachable Orca, a named owner of the watcher worktree, the claim's own hook check).

The runbook ends with a record section that holds exactly eleven lines, one per precondition, each written `PENDING: <letter> <short name>`. The owner replaces each with `RECORDED: <letter> <value>` (the measured value, the Orca build string from `orca-ide --version`, the date) and adds one line `RUN BY OWNER: <name>` when the run is done. Plan B Task 20 checks that record.

Start condition: can be written now; running it waits for the owner's acceptance, a live-test grant and a running coordinator, and the agent that writes it never runs it. The run uses a hand-written throwaway brief (no Task 7 builder, no worker-approval rule, no coordinator duties) on a throwaway issue's worktree, so that Plan B Tasks 9 and 10 are written after its receipt.

Acceptance criteria:
- The document lists preconditions a to k each with a step, a recorded value and a failure meaning, and states that no step in it is run by the agent that writes it.
- The record section holds the eleven `PENDING:` lines and no `RUN BY OWNER:` line yet: `grep -c "^PENDING: [a-k] " docs/designs/issue-pipeline-fu1.md` prints 11 and `grep -c "^RUN BY OWNER: " docs/designs/issue-pipeline-fu1.md` prints 0.
- The document says that the worker can also post the approval label or the approval comment as the same GitHub login, and that nothing tells the two apart (Decision 4, accepted); GitHub approvals stay accepted inputs.
- The acceptance sentence appears word for word and names the guard, and the check is a command, not a test file (the four files in tests/docs pin other documents, and no test in the repository pins the issue-watcher documents): `test -f docs/designs/issue-pipeline-fu1.md && grep -cF "no launch-level guard (nothing blocks a commit, push, merge, GitHub write or /sc:implement)" docs/designs/issue-pipeline-fu1.md` prints 1 or more. The same `grep -cF` form run on `./artifacts/validation.md` with the words `launch-level guard` prints 1 today, which shows the command works.
- `grep -n "FU-1" docs/designs/issue-pipeline-fu1.md` shows the link to the first live test of docs/designs/issue-watcher-setup.md section 8.5.

## Task 3: Build the locked, write-ahead approval record helper

Depends on: Task 1, Task 2

Create `src/superclaude/cli/issue_pipeline/approval_record.py` and its verbs (`init`, `adopt-create`, `adopt-mark`, `record-create`, `record-show`, `record-mark`) in `src/superclaude/cli/issue_pipeline/cli.py`, with `tests/issue_pipeline/test_approval_record.py`, `tests/issue_pipeline/test_approval_concurrency.py` and `tests/issue_pipeline/test_approval_crash.py`.

The helper keeps two kinds of row in an approvals directory of its own, never inside the watcher's state directory and never touching `dispatch.json`. An adoption row is keyed (issue, stage) and is created before any plan exists, so no plan hash is needed: it is the per-issue reservation that stops a second start (state `reserved`, then `started` with the Dispatch id, or `uncertain` when `worker-start` did not report ready; an `uncertain` row is settled by a person or by reading `worker-list`, never by starting again). An approval row is keyed (issue, stage, plan hash) and hangs under the adoption row. `init <dir>` creates the directory (0700) and its `lock` file (0600), because `FileStore.lock()` opens an existing file with no create flag and raises `lock_missing` otherwise (record.py:391-397). It takes the lock with `FileStore(<approvals dir>).lock()` from src/superclaude/cli/issue_watch/record.py:381 (an exclusive non-blocking `flock`, so a second concurrent caller gets `LockHeld` at once and the verbs say "retry the append", never "lost"; the lock is held only for one call, so it is not what spans adoption: the adoption row is), and writes with `write_prepared_bytes` from `superclaude.cli.swarm.atomic` followed by a directory sync, the same way `FileStore.save` does (record.py:370 and `_fsync_dir` at record.py:310). `record.py` itself is not edited. Row fields: record id, issue, stage, plan hash, evidence list (channel, event or comment or message id, actor id, time), state (`recorded`, `instructed`, `acked`, `revoked`), times. A second approval for the same key, from any channel, appends evidence to the existing row and returns the existing row, so a label plus a comment can never produce two rows. A re-approval of the same plan after `revoked` reopens the same row.

Start condition: can start now.

Acceptance criteria:
- A test with two processes calling `record-create` for the same key at once shows exactly one row and one winner; the loser gets the existing row or a lock-held result, never a second row.
- A test shows that a label approval followed by a comment approval for the same key leaves one row with two evidence entries, and that a different plan hash for the same issue makes a different row.
- A crash test (kill after the write, before the caller proceeds) shows the row is on disk and `record-show` returns state `recorded`, mirroring tests/issue_watch/test_crash_injection.py.
- `record-create` in a directory that `init` never ran in fails with a closed reason (not a traceback), and after `init` the first call succeeds; a concurrent second call reports `lock-held, retry` and the evidence is appended on the retry.
- Adoption tests: two callers of `adopt-create` for one issue get one row and one `reserved` winner; a kill between `worker-start` and `adopt-mark started` leaves the row `reserved`, and the next `adopt-create` refuses a second start with the reason `uncertain-launch`; a duplicate approval, sequential or concurrent, and a crash between the row write and the `reply` each yield at most one start and at most one continuation instruction, asserted on the adoption and approval row states, not on a row count.
- `record-mark` accepts only the forward moves `recorded` to `instructed` to `acked`, and `revoked` from any of them, and refuses every other move with a closed reason.
- `git diff --stat` shows no change to src/superclaude/cli/issue_watch/record.py, and `uv run pytest tests/issue_pipeline/ tests/issue_watch/test_record.py tests/issue_watch/test_module_boundaries.py -v` passes.

## Phase 3: Read-only stage status (real fixtures are recorded first)

## Task 4: Write the stage predicates for the label and the "approved" comment

Depends on: Task 2

First step, before any predicate is written: record real GitHub responses. Plan rules allow only lower-numbered dependencies, so this is the first step and the first acceptance criterion of this task (no renumbering). Read the issue number from owner input O-1 (`tests/issue_pipeline/fixtures/recorded/OWNER-INPUT.md`, one line `ISSUE: <number>`, an issue the owner wrote; never pick one). Save, with read-only GET calls only and the same `gh api` argv shapes that `argv_events`, `argv_comments` (the new comments read of Task 5) and `argv_edits` of src/superclaude/cli/issue_watch/github.py build, the raw responses for that one issue: its comments, its timeline events and the edits GraphQL query. Save them as files under `tests/issue_pipeline/fixtures/recorded/` and write the call list and date in `tests/issue_pipeline/fixtures/recorded/README.md`. The predicate tests below, and the tests of Tasks 5 and 6, then run against those recorded files as well as against hand-built cases, so a wrong field name shows up before the first live test.

Create `src/superclaude/cli/issue_pipeline/stage_predicates.py` and `tests/issue_pipeline/test_stage_predicates.py`. These are pure functions over the evidence types already defined in src/superclaude/cli/issue_watch/predicates.py (`LabelEvent`, `CommentEdit`, `EditEvidence`); the existing `approval_of` and `unchanged_since` are not reused as they are, because `unchanged_since` skips comments written by the host login (predicates.py:253-255) and the coordinator posts the plan reply as that login, so an edited plan reply would go unseen, and `approval_of` orders an approval against the trigger label and the store creation time, not against a plan reply.

Rules the predicates implement, written once here:
- The plan reply is the latest comment by the host login that carries the hidden marker `<!-- sc:stage:plan id=<record-id> plan=<64 hex> -->`. It must be unedited since it was posted, and the plan files must still hash to the marker's value.
- Label channel: the approval label was applied after the plan reply, still applied, the actor is a `User` and not a bot, and the actor is the assignee or in the approvers file. The assignee is a login (`DiscoveredIssue.assignees`, predicates.py:85) and the approvers file holds ids, so the actor's login is compared with the assignee and the actor's id with the file; `LabelEvent` carries both (predicates.py:90-99), while `CommentEdit` carries only the author login (:133-139), so a comment author's id and type come from the Task 5 projection. A Status move is the visible sign of the approval (owner decision 3 of the approval-flow record, answer A): it is read where the code can and reported as `status_seen`, never required, because no code reads who moved a Project Status.
- Comment channel: the comment is exactly `approved` or `approved <record-id> plan-sha256=<hash>`; its author is the issue assignee or a listed approver, is a `User` and not a bot, and every other commenter is ignored because the repository is public; it was created after the latest plan reply; it has never been edited; the long form's hash equals the latest plan reply's hash; the short form binds by position to the latest plan reply's hash. A comment created before a newer plan reply never counts for the newer plan.
- Both channels map to the same key (issue, stage, plan hash), so Task 3 can return one row for both.
- Revocation: removing the approval label after the record exists is a revocation signal; deleting or editing an approving comment is not (the record stands), and a Status move back alone is reported, never acted on.
- Facts that the code cannot check are carried as flags in the result, not hidden: the actor equals the host login (an agent on this host could have posted it, Decision 4), and the assignee is the host login after a claim.

Start condition: can start now.

Acceptance criteria:
- Real fixtures exist before the predicates do: `grep -c "^ISSUE: [1-9][0-9]*$" tests/issue_pipeline/fixtures/recorded/OWNER-INPUT.md` prints 1, `tests/issue_pipeline/fixtures/recorded/` holds the raw comments, timeline events and edits responses for that issue plus a README with the call list, every call in the README is a GET (or the fixed edits GraphQL query), and `tests/issue_pipeline/test_stage_predicates.py` has at least one test that loads a recorded file. If the O-1 line is missing the executor stops here and picks no issue.
- `tests/issue_pipeline/test_stage_predicates.py` has one test per rule and one negative per clause: bot author, non-assignee non-approver author, comment before the plan reply, comment after a newer plan reply for an older hash, edited comment, edited plan reply, plan file changed after the reply, wrong hash in the long form, label applied then removed, comment text with trailing space.
- A test shows a label and a comment for the same plan produce the same key, and a test shows an approval for plan version A is ignored once plan reply B exists.
- A test shows a label with no Status move is still accepted and reports `status_seen: false`, and a label with a Status move reports `status_seen: true`; neither changes the key.
- A test shows the host-login flag is set when the actor is the host login and the result is still accepted, as Decision 4 states.
- `uv run pytest tests/issue_pipeline/test_stage_predicates.py -v` passes.

## Task 5: Add the GitHub reads that turn comment text into booleans

Depends on: Task 4

Create `src/superclaude/cli/issue_pipeline/reads.py` and `tests/issue_pipeline/test_reads.py`. The reads reuse `argv_events`, `argv_edits` (a fixed GraphQL query that `gh api graphql` sends as a POST, github.py:106-108 and :228-244) and the call budget of src/superclaude/cli/issue_watch/github.py (:218, :242, :437), build the comments argv with `_argv_rest_page(n, "comments", page, <new jq>)` as `argv_comments` does (:201-225), and add one comments projection in jq, in the same manner as `MARKER_JQ` (github.py:61): the body never leaves jq. The projection returns per comment the id, author login, author id, author type, created time, and three values computed inside jq: whether the whole body matches the short or long approval line, the record id and hash captured from a long line, and whether the body carries the plan-reply marker with its hash. Python re-validates every captured value against a fixed hex or id pattern before it is used.

Start condition: can start now; field names are pinned by the real recorded fixtures of Task 4 and re-checked in FU-1 (Task 8).

Acceptance criteria:
- A test runs the jq projection over the recorded comments file of Task 4 and shows every projected field is present with the expected type.
- A test with a hostile comment body (a canary string, markup, a very long line) shows the canary appears in no output, no argv and no file, in the same way as tests/issue_watch/test_no_text.py, and a second test shows the new gh argv asks for no body field.
- A test shows the jq projection returns `matches_approval_line: true` only for the two exact forms, and returns false for trailing newline, trailing space, a quoted line and a reply that merely contains the word approved.
- A test shows the call cap and page cap of `CallBudget` are respected across the events, comments and edits reads, and a transient gh failure returns a closed reason instead of a partial approval.
- `uv run pytest tests/issue_pipeline/test_reads.py -v` passes.

## Task 6: Add the read-only `stage-status` command

Depends on: Task 3, Task 4, Task 5

Add the `stage-status <issue> --json` verb to src/superclaude/cli/issue_pipeline/cli.py with `tests/issue_pipeline/test_stage_status.py`. It reads GitHub through Task 5, applies Task 4, looks up the row of Task 3, and prints a closed set of keys: the latest plan hash and plan reply id, the approvals found per channel with their reason codes, the row state, and the flags from Task 4. It writes nothing to GitHub, the row store or Orca, and it prints no GitHub text.

Start condition: can start now.

Acceptance criteria:
- A test feeds the recorded events, comments and edits files of Task 4 through the injected runner and shows `stage-status` prints only closed keys for that issue.
- A test table covers: no plan reply yet; plan reply and no approval; label only; comment only; label and comment (one key, one row); plan changed after approval; approval label removed; approver not listed; every case prints only closed keys and values.
- A test, run over the real argv builders of Task 5 and the watcher's `argv_edits`, shows the command never passes a `--method` other than GET, never calls a mutation or a write endpoint (the fixed GraphQL queries are allowed, as tests/issue_watch/test_security_invariants.py:239-241 already allows them), and never calls `orca`, by asserting over the recorded argv of the injected runner.
- `uv run pytest tests/issue_pipeline/test_stage_status.py -v` passes and `uv run superclaude issue-pipeline stage-status --help` exits 0.

## Phase 4: Worker brief and the change list for the merged requirements

## Task 7: Build the worker brief from fixed templates

Depends on: Task 1

Create `src/superclaude/cli/issue_pipeline/brief.py`, `src/superclaude/cli/issue_pipeline/templates/worker-brief.txt` and `tests/issue_pipeline/test_brief.py`. The builder emits the Task spec the coordinator passes to `worker-start --spec`, in the brief layout of src/superclaude/core/WORKER-CONTRACT.md (the guard line, the chain line, `On a blocked gate: report blocked`, `Local commit: not authorized`, a report directory unique to the Task, the worktree line, `Outward actions: none`, and one `Command:` line per step with `--unattended` and exactly one report directory). Its only inputs are the issue number (a validated integer) and two values read from the claim's summary: the type (`feature` or `bug`) and the complexity (`simple`, `medium` or `complex`), each checked against the closed set. The builder builds the three Feature rows only. For type `bug` it refuses with the closed reason `type-not-supported` and produces no brief; no Bug row, no bug symptom phrase and no `--scope` handling are built. The three rows come from the Feature rows of src/superclaude/skills/sc-issue-protocol/refs/chains.md and stop before `/sc:implement` or `/task`: simple is `/sc:brainstorm` quick then `/sc:workflow` quick; medium is `/sc:brainstorm` with `--blind`, `/sc:design` and `/sc:workflow` standard; complex is `/sc:brainstorm` deep with codebase research and `--blind`, `/sc:design` and `/sc:workflow` deep. Every `Command:` line carries `--unattended`, one report directory and (for workflow) `--handoff none`.

`/sc:design` requires `--type <architecture|api|component|database>` and the rows add `--format spec`. The builder uses a fixed `--type architecture` in the medium and complex rows; it adds no third enum, because the type only steers the shape of the design document and the issue's text never chooses it. Command text never contains issue words: the topic is the fixed phrase `issue <N>` with `@.dev/issues/<N>/issue-summary.md`.

Start condition: the builder can be written now; the coordinator uses its output only after the two-copy test in WORKER-CONTRACT.md passes for each command in the rows. `/sc:brainstorm`, `/sc:design` and `/sc:workflow` are all in the default converted set of the first conversion phase (WORKER-CONTRACT.md line 317), so no extra live check is needed for them; the P2 sentence (line 318) names only the later commands such as `/sc:troubleshoot`, which no row uses.

Acceptance criteria:
- A golden test per Feature row (three rows: simple, medium, complex) compares the full brief text, the medium and complex rows contain `/sc:design` with `--type architecture`, and a property test shows the output contains only template characters plus the validated integer, for any input including hostile titles, labels and summary text.
- A test shows any value outside the enums, a non-integer issue number, or type `bug` makes the builder refuse with a closed reason (`type-not-supported` for `bug`) and produce no brief.
- A test shows no row contains `/sc:implement`, `/task`, `git commit`, `git push` or `/sc:pr-submit`, and no `Command:` line lacks `--unattended`.
- A test shows the template's Guard, Chain, `Local commit`, `Outward actions` and blocked-gate lines equal the brief template in section 5 of src/superclaude/core/WORKER-CONTRACT.md (the template block is lines 302-311, the Guard line is 303) word for word, so the two copies cannot drift; the `Worktree:` slot (line 308) is the one place the builder differs (it uses `path:<existing worktree>`, see Plan B Task 9).
- `uv run pytest tests/issue_pipeline/test_brief.py -v` passes.

## Task 19: Write the change list for the merged requirements and close the open decisions

Create `./artifacts/merged-spec-change-list.md` in this package. It names, without editing the merged requirements file in the brainstorm folder: WA-01 (claim level: take the "--pipeline none" branch, now with the coordinator handoff); WA-02 (the #450 edits list gains B); WA-03 (runbook step); WA-04 (FU-1 record adds preconditions a to k and the guard-loss acceptance); WA-07 (moves from deferred to live under B, blocked-by SW-13 removed or restated); SW-13 (the supervised-worker route is now the delivery path, no longer a later redesign); OB-09 (a dashboard approval is only a message to the coordinator); section 6.3 roles (a worker row for the plan-writing worker); section 6.4 rule 10 (permission mode of every started session, now including the guard loss); section 6.8 (a per-pipeline-issue grant row shape: plan reply, marker comment, mention, label and Status writes); and new items for Tasks 1 to 16 (the adoption row of Task 3, the `pending` subcommand of Task 15 and the `Worktree:` slot change of Task 9 included). It then lists the owner decisions below, each with options, a recommended answer and the owner's answer, written for a person who has not seen the project.

Owner decisions (Q34 and Q41 were answered on 2026-11-14; Q35 to Q40 were answered on 2026-11-14 and restated by the owner on 2026-11-15, relayed by the orchestrating session; each line below records the answer, and none is open). Each is written for a person who has not seen the project:
- Q35, the claim-side change. Options: B1b, the watcher claims with `--pipeline none` and the coordinator runs the existing worktree step (recommended; no claim code changes, only the watcher prompt and tests); B2, a new claim level that creates the worktree and copies files without an agent (about six more test files, and a worktree with no agent until the coordinator starts one). ANSWERED 2026-11-15 (first 2026-11-14): B1b (the first reply said "Q53 b1b" and "2. Approved", read as Q35).
- Q36, approval latency under Q31 (no recurring timer). The coordinator reads GitHub only at gates and wakes, so an approval given on GitHub waits until the next read, which can be hours. Options: A, accept the delay and make Orca the fast path (the person approves in the coordinator session, which is immediate); B, allow a narrow timed read only for pipeline issues that are waiting for approval (reverses Q31 for that one case); C, the person types "check now" in the coordinator session after approving on GitHub. Recommended: A together with C. ANSWERED 2026-11-15 (first 2026-11-14 as "accepted delay"): option A, approve in the coordinator; the "check now" command (option C) is NOT selected and is not built.
- Q37, where the worker's plan-approval rule lives. Options: a new rule in WORKER-CONTRACT.md next to WC-3 (recommended, written once); only in each brief (no contract edit, but every brief repeats it). ANSWERED 2026-11-15 (first 2026-11-14): the rule goes in WORKER-CONTRACT.md next to WC-3.
- Q38, how a coordinator approval releases a guarded worker (G2). Options: A, the coordinator writes the session's release file after recording the approval (needs the worker's session id, UNVERIFIED); B, the guard reads a coordinator-signed approval file (more code in the guard). Recommended: A if the first live test shows the session id can be found, else B. ANSWERED 2026-11-15 (first 2026-11-14 as "default until G2"): the default. G2 is not built, so only the one G1 test issue can run; no release route is chosen now, and the route is chosen in Task 13 after the first live test.
- Q39, the scope of removing plain `approved` (Decision 9). Options: remove it for every worktree-level claim (closes the self-approval hole, but a person with no coordinator then has only `/sc:implement` typed in the session); keep it for person-run claims until G2 exists (my earlier recommendation, not taken). ANSWERED 2026-11-15: remove it now, for every worktree-level claim, with no person-run carve-out and no wait for G2 or the live test (Task 16).
- Q40, the design amendment order. #548 is merged. Options: one follow-up documentation PR for Tasks 17 and 18 (recommended); fold them into the code PR of Task 11. ANSWERED 2026-11-15 (first 2026-11-14): one follow-up documentation PR for Tasks 17 and 18, opened only after the owner reads the plan. No PR is opened from this plan, and Tasks 17 and 18 wait on Task 11.
- Q41, the worktree with no agent. The claim script creates `issue-<N>` with no agent (`orca_worktree.py:681-697`), so for a moment the worktree has none, against the project rule that every worktree gets an agent; the coordinator's `worker-start` supplies one right after. If the coordinator is down in between, the worktree sits empty. Options: A, accept it and say so in the claim text (recommended: the script closes the plain first tab, nothing runs in the empty worktree, and nothing starts while the coordinator is down anyway); B, change the script to create the worktree with an agent (more claim code, and a second agent instead of the worker); C, let `worker-start` create the worktree itself, which skips the script's copy step and reuse lookup (rejected in the design session). ANSWERED 2026-11-14: A (accept it and say so in the claim text).

Open points that remain (facts, not owner decisions; the first live test of Task 8 must measure each): the real `worker-start` argv and permission flags; whether `worker-start` accepts an exact existing worktree that the script created and leaves exactly one terminal; the `ask` and `reply` round trip, including whether the reply is stored as type `status` and a narrow `--types` filter misses it; the launch receipt shape and the Dispatch id; how a worker's session id can be found (it decides the G2 release route in Task 13); `ask` timeout and resume by message ID; a worker staying in `ask` while the coordinator is down; worktree reuse when the claim runs twice; the GitHub label event shape; whether a comment typed in the GitHub web editor arrives as exactly `approved`; and what a comment edit does to `lastEditedAt`.

Start condition: can be written now.

Acceptance criteria:
- The artifact lists every merged-requirements item named above with the change in one sentence, and lists Q35 to Q41 each with options, a recommended answer, and the owner's answer or a default.
- A grep of the merged requirements file shows no modification (`git status` of the brainstorm folder is clean for that file).
