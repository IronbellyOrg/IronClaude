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

- Plan only. The owner approved this plan with fixes on 2026-11-15; every owner decision in Task 19 is answered, and what stays open are facts the first live test must measure (Task 8), not decisions. Running `/sc:implement` from this plan still needs the owner's separate go, and a task whose start condition names a gate (the live test, a coordinator, Task 11) does not start before that gate. No push, PR, GitHub write or Orca write verb is authorized by this plan.
- Rebase first. This plan was written on base 0406ef5b0. origin/master is now d4d1662a8 and already holds PR #539 (sweep) and PR #548 (the D2 "claim-only" superseded note in docs/designs/issue-watcher.md). Every task below starts from a worktree based on current origin/master.
- Evidence for every factual claim is in ./artifacts/validation.md (read-only measurements, file and line citations, and what is UNVERIFIED). Real code locations are in ./artifacts/codegraph-grounding.md.
- Chosen claim-side change: B1b, the watcher claims with `--pipeline none` and the coordinator runs the existing `orca_worktree.py worktree` step, then `worker-start --worktree path:<that worktree>`. The owner confirmed it on 2026-11-14 and again on 2026-11-15 (Q35 = B1b; the first reply wrote "Q53 b1b" next to "2. Approved", read as Q35). B2, a new claim level, is not built.
- Owner answers that shape this plan (first given 2026-11-14, restated by the owner on 2026-11-15 and relayed by the orchestrating session): Q36 option A, approve in the coordinator (no recurring timer; the "check now" command is not selected); Q37 the worker's plan-approval rule goes in WORKER-CONTRACT.md next to WC-3; Q38 the default stands, so G2 is not built and only the one G1 test issue can run; Q39 plain `approved` is removed now, for every worktree-level claim, with no person-run carve-out and no wait for G2 or the live test (Task 16); Q40 Tasks 17 and 18 ship as one follow-up documentation PR, opened only after the owner reads the plan.
- Owner decision Q34 (2026-11-14): the plan-writing worker runs without the launch-level guard (G1) for ONE test issue only. The written acceptance must cover the loss of the guard itself (no block on commit, push, merge, GitHub writes or /sc:implement), the owner writes that issue's text, and it is not stretched from the Decision 1 acceptance of permission checks off. Before any other issue runs through this flow, the guard is changed (G2, Phase 6).
- Accepted earlier and carried here: only the coordinator tells the worker to proceed; one person-opened coordinator owns all watcher-claimed issues on this host with a lock per issue; nothing starts while the coordinator is down; one grant row per pipeline issue; one GitHub login on this host means an agent could apply the approval label or post the approval comment (Decision 4, accepted).
- New code goes in a new package `src/superclaude/cli/issue_pipeline/` and tests in `tests/issue_pipeline/`. The tests in tests/issue_watch/test_module_boundaries.py pin what each issue_watch module may import, and tests/issue_watch/test_no_text.py forbids a gh call that asks for comment text, so issue_pipeline imports from issue_watch and never the reverse.
- Never edit `.claude/` mirrors; edit `src/superclaude/` and run `make sync-dev`. Stage `.dev/tasks` only as the project rule says; this plan stages and commits nothing.
- The merged requirements file in the brainstorm folder is not edited by any task; Task 19 writes the change list for it inside this package.
- Every command is run with `uv run`.

## Phase 1: Approval core (can start now, no Orca facts needed)

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

## Phase 2: Read-only stage status (can start now; GitHub field shapes pinned by fixtures, confirmed in FU-1)

## Task 4: Write the stage predicates for the label and the "approved" comment

Depends on: Task 2

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
- `tests/issue_pipeline/test_stage_predicates.py` has one test per rule and one negative per clause: bot author, non-assignee non-approver author, comment before the plan reply, comment after a newer plan reply for an older hash, edited comment, edited plan reply, plan file changed after the reply, wrong hash in the long form, label applied then removed, comment text with trailing space.
- A test shows a label and a comment for the same plan produce the same key, and a test shows an approval for plan version A is ignored once plan reply B exists.
- A test shows a label with no Status move is still accepted and reports `status_seen: false`, and a label with a Status move reports `status_seen: true`; neither changes the key.
- A test shows the host-login flag is set when the actor is the host login and the result is still accepted, as Decision 4 states.
- `uv run pytest tests/issue_pipeline/test_stage_predicates.py -v` passes.

## Task 5: Add the GitHub reads that turn comment text into booleans

Depends on: Task 4

Create `src/superclaude/cli/issue_pipeline/reads.py` and `tests/issue_pipeline/test_reads.py`. The reads reuse `argv_events`, `argv_edits` (a fixed GraphQL query that `gh api graphql` sends as a POST, github.py:106-108 and :228-244) and the call budget of src/superclaude/cli/issue_watch/github.py (:218, :242, :437), build the comments argv with `_argv_rest_page(n, "comments", page, <new jq>)` as `argv_comments` does (:201-225), and add one comments projection in jq, in the same manner as `MARKER_JQ` (github.py:61): the body never leaves jq. The projection returns per comment the id, author login, author id, author type, created time, and three values computed inside jq: whether the whole body matches the short or long approval line, the record id and hash captured from a long line, and whether the body carries the plan-reply marker with its hash. Python re-validates every captured value against a fixed hex or id pattern before it is used.

Start condition: can start now; field names are pinned by recorded fixtures and re-checked in FU-1 (Task 8).

Acceptance criteria:
- A test with a hostile comment body (a canary string, markup, a very long line) shows the canary appears in no output, no argv and no file, in the same way as tests/issue_watch/test_no_text.py, and a second test shows the new gh argv asks for no body field.
- A test shows the jq projection returns `matches_approval_line: true` only for the two exact forms, and returns false for trailing newline, trailing space, a quoted line and a reply that merely contains the word approved.
- A test shows the call cap and page cap of `CallBudget` are respected across the events, comments and edits reads, and a transient gh failure returns a closed reason instead of a partial approval.
- `uv run pytest tests/issue_pipeline/test_reads.py -v` passes.

## Task 6: Add the read-only `stage-status` command

Depends on: Task 3, Task 4, Task 5

Add the `stage-status <issue> --json` verb to src/superclaude/cli/issue_pipeline/cli.py with `tests/issue_pipeline/test_stage_status.py`. It reads GitHub through Task 5, applies Task 4, looks up the row of Task 3, and prints a closed set of keys: the latest plan hash and plan reply id, the approvals found per channel with their reason codes, the row state, and the flags from Task 4. It writes nothing to GitHub, the row store or Orca, and it prints no GitHub text.

Start condition: can start now.

Acceptance criteria:
- A test table covers: no plan reply yet; plan reply and no approval; label only; comment only; label and comment (one key, one row); plan changed after approval; approval label removed; approver not listed; every case prints only closed keys and values.
- A test, run over the real argv builders of Task 5 and the watcher's `argv_edits`, shows the command never passes a `--method` other than GET, never calls a mutation or a write endpoint (the fixed GraphQL queries are allowed, as tests/issue_watch/test_security_invariants.py:239-241 already allows them), and never calls `orca`, by asserting over the recorded argv of the injected runner.
- `uv run pytest tests/issue_pipeline/test_stage_status.py -v` passes and `uv run superclaude issue-pipeline stage-status --help` exits 0.

## Phase 3: Worker brief and the live-test runbook (written now, run later)

## Task 7: Build the worker brief from fixed templates

Depends on: Task 1

Create `src/superclaude/cli/issue_pipeline/brief.py`, `src/superclaude/cli/issue_pipeline/templates/worker-brief.txt` and `tests/issue_pipeline/test_brief.py`. The builder emits the Task spec the coordinator passes to `worker-start --spec`, in the brief layout of src/superclaude/core/WORKER-CONTRACT.md (the guard line, the chain line, `On a blocked gate: report blocked`, `Local commit: not authorized`, a report directory unique to the Task, the worktree line, `Outward actions: none`, and one `Command:` line per step with `--unattended` and exactly one report directory). Its only inputs are the issue number (a validated integer) and two enums read from the claim's summary (type feature or bug, complexity simple, medium or complex), each checked against the closed set. It maps them to the fixed chain rows of src/superclaude/skills/sc-issue-protocol/refs/chains.md up to the plan boundary (every row stops before `/sc:implement` or `/task`). Command text never contains issue words: the topic is the fixed phrase `issue <N>` with `@.dev/issues/<N>/issue-summary.md`, and the bug symptom is a fixed phrase of at least ten words that points at the summary file. A `--scope` value is accepted only when it is a repo-relative path that `git ls-files` lists and matches a strict pattern; otherwise the builder refuses and the coordinator asks the person.

Start condition: the builder can be written now; its output may be used only after the two-copy test in WORKER-CONTRACT.md passes for each command in the rows, and `/sc:troubleshoot` and `/sc:brainstorm` carry the P2 rule that they are not in the default converted set until a phase 2 live check passes.

Acceptance criteria:
- A golden test per chain row (six rows) compares the full brief text, and a property test shows the output contains only template characters plus the validated integer, for any input including hostile titles, labels and summary text.
- A test shows any value outside the enums, a non-integer issue number or a scope that is not a tracked path makes the builder refuse with a closed reason and produce no brief.
- A test shows no row contains `/sc:implement`, `/task`, `git commit`, `git push` or `/sc:pr-submit`, and no `Command:` line lacks `--unattended`.
- A test shows the template's Guard, Chain, `Local commit`, `Outward actions` and blocked-gate lines equal the brief template in section 5 of src/superclaude/core/WORKER-CONTRACT.md (:296-307) word for word, so the two copies cannot drift; the `Worktree:` slot is the one place the builder differs (it uses `path:<existing worktree>`, see Task 9).
- `uv run pytest tests/issue_pipeline/test_brief.py -v` passes.

## Task 8: Write the first-live-test runbook for B, including the guard-loss acceptance

Depends on: Task 3, Task 6, Task 7

Create `docs/designs/issue-pipeline-fu1.md`. It lists preconditions a to k, each with its exact read-only or throwaway step, the value to record, and what a failure means. Preconditions a to j come from section 7 of ./artifacts/validation.md: the real `worker-start` argv and permission flags; `worker-start --worktree path:<exact existing worktree a script created>` and exactly one terminal afterwards; the `ask` and `reply` round trip for a worker started with a spec, including whether the reply arrives as type `status` and a narrow `--types` filter misses it; the launch receipt shape and the Dispatch id; the plan hash computed identically by coordinator and worker; guard interaction under G1; `ask` timeout and resume by message ID; a worker staying in `ask` while the coordinator is down; worktree reuse when the claim runs twice; and the GitHub stage facts (who moved a Project Status, label event shape). Precondition k is new: whether a comment typed in the GitHub web editor round-trips as exactly `approved`, and what a comment edit does to `lastEditedAt`.

The runbook also holds the written acceptance the owner must give before the test, worded to cover the guard loss: "I accept, for test issue #<N> only, that the plan-writing worker runs with permission checks off and with no launch-level guard (nothing blocks a commit, push, merge, GitHub write or /sc:implement), reading issue text that I wrote myself. This is separate from my 2026-11-14 acceptance of permission checks off." The test issue text is written by the owner. The runbook names the existing gates that still apply (a separate live-test grant, a reachable Orca, a named owner of the watcher worktree, the claim's own hook check).

Start condition: can be written now; running it waits for the owner's acceptance, a live-test grant and a running coordinator. The run uses a hand-written throwaway brief (no Task 7 builder, no Task 10 rule, no Task 9 duties) on a throwaway issue's worktree, so that Tasks 9 and 10 are written after its receipt; the Depends lines of Tasks 9 and 10 name Task 7 and Task 3 for code, not for the run.

Acceptance criteria:
- The document lists preconditions a to k each with a step, a recorded value and a failure meaning, and states that no step in it is run by the agent that writes it.
- The acceptance sentence appears word for word and names the guard, and the check is a command, not a test file (the four files in tests/docs pin other documents, and no test in the repository pins the issue-watcher documents): `test -f docs/designs/issue-pipeline-fu1.md && grep -cF "no launch-level guard (nothing blocks a commit, push, merge, GitHub write or /sc:implement)" docs/designs/issue-pipeline-fu1.md` prints 1 or more. The same `grep -cF` form run on `./artifacts/validation.md` with the words `launch-level guard` prints 1 today, which shows the command works.
- `grep -n "FU-1" docs/designs/issue-pipeline-fu1.md` shows the link to the first live test of docs/designs/issue-watcher-setup.md section 8.5.

## Phase 4: Coordinator and worker rules (waits on the first live test and on a coordinator)

## Task 9: Add the issue-pipeline duties to the coordinator rules

Depends on: Task 3, Task 6, Task 7

Edit `src/superclaude/core/WORKER-CONTRACT.md` section 4 and its pin test `tests/skills/test_worker_contract.py`; run `make sync-dev` and stage only the `src/` side. Add a subsection "Issue pipeline duties" stating, in the contract's style: adopt a claimed issue from sources that exist after a `--pipeline none` claim, which writes no `worktree.json` and creates no worktree (`refs/claim.md:93`): the watcher store's `claimed` entry in `dispatch.json`, read-only, and `.dev/issues/<N>/issue-summary.md` and `next-steps.md` in the checkout that ran the claim; take the per-issue reservation by creating the adoption row (Task 3) before `worker-start`, mark it `started` with the Dispatch id when `worker-start` returns ready and `uncertain` when it does not, and never start again for an `uncertain` row (settle it by reading `worker-list`); create the plan-hash approval row only when the worker's `ask` carries the plan hash; run the existing `orca_worktree.py worktree` step from the installed skill and then `worker-start --worktree path:<exact path> --agent claude --spec <Task 7 brief>`; read the worker's `ask`, post the plan reply with the hash and file list and mention the assignee, then read GitHub through `stage-status` at each gate or wake; on approval write the row, then `reply` with `approved <record-id> plan-sha256=<hash>`, then mirror the label and Status; mark the row from the worker's ack. It adds to the never-list: never tell a worker to pass its plan boundary without a row, never act on a Status move alone, never relaunch a dead worker by itself, never post an issue write without the issue's grant row. It does not add any exception to "never answer a person prompt", because route B needs none. It also extends the `Worktree:` slot of the brief template in section 5 (WORKER-CONTRACT.md:304), which today allows only the shared feature worktree or `new-child`, to allow `path:<existing worktree>`, a form section 4 already uses for resume Tasks (:280).

Start condition: waits on a coordinator existing and on the first live test (Task 8 run) showing the `ask` and `reply` round trip.

Acceptance criteria:
- WORKER-CONTRACT.md has the new subsection and the new never-list lines, and no line that permits typing into a worker's prompt.
- The adoption sentence names only sources that exist after a `--pipeline none` claim, and a pin test in tests/skills/test_worker_contract.py fails if `worktree.json` is named as an adoption source; the `Worktree:` slot at :304 allows `path:<existing worktree>` and Task 7's template test still passes against it.
- `uv run pytest tests/skills/test_worker_contract.py -v` passes with new pins for the subsection heading and for the sentence that route B adds no exception.
- `make verify-sync` passes and `git status` shows no staged `.claude/` path.

## Task 10: Add the worker's plan-approval rule

Depends on: Task 2, Task 7, Task 9

Edit `src/superclaude/core/WORKER-CONTRACT.md` section 3 (a new rule after WC-3) and `tests/skills/test_worker_contract.py`. WC-3 lets a worker ask at most once per Task and only at a gate whose answer fits an existing flag; a plan-approval ask is a different, intended wait. The new rule states: after writing the plan the worker runs `issue-pipeline plan-hash`, asks once with the plan path, file list and hash, waits (resuming the same message ID on timeout, as WC-3 already says), runs `check-approval` on the reply, sends `ack <message_id> applied` or `ack <message_id> refused`, continues only on `applied`, and never treats a bare `approved` or any text that is not the reply to its own ask as approval. The rule lives in the contract, written once (owner answer Q37, 2026-11-14); the brief only points at it.

Start condition: waits on Task 9.

Acceptance criteria:
- The contract has the rule with the exact order of steps and the sentence that a mismatch is refused and reported, not retried silently.
- The brief template of Task 7 carries a line that points at the rule, and a golden test in tests/issue_pipeline/test_brief.py is updated for it.
- `uv run pytest tests/skills/test_worker_contract.py tests/issue_pipeline/test_brief.py -v` passes.

## Phase 5: Watcher prompt and claim handoff (waits on the first live test and a running coordinator)

## Task 11: Change the watcher's claim prompt to `--pipeline none`

Depends on: Task 8, Task 9, Task 10

Edit `src/superclaude/cli/issue_watch/launch.py`: `PROMPT_PATTERN` (:33) becomes `^/sc:issue --claim [1-9][0-9]{0,8} --pipeline none$`, `build_claim_prompt` (:84) returns `/sc:issue --claim <n> --pipeline none`, and the docstrings that quote the old prompt are updated. `launch_argv` stays a 12-element list and `retry_argv` inherits the new prompt. `src/superclaude/cli/issue_watch/record.py` and the at-most-once `dispatch.json` are not touched. Callers that change behaviour only through the prompt string: `_launch` (cycle.py:1026) and `status_report` (cycle.py:1270). Update every test that quotes the prompt: tests/issue_watch/test_launch.py (:41, :47, :54, :67, :75, :95, :102, :141, :152, :805, :817, :841, :913), tests/issue_watch/test_security_invariants.py (:451, :522, :584, :621, :697, :921), tests/issue_watch/test_no_text.py (:464), tests/issue_watch/test_cli.py (:582), tests/issue_watch/test_cycle.py, tests/issue_watch/test_cli_e2e.py, tests/issue_watch/test_crash_injection.py and tests/issue_watch/conftest.py (:279). The prompt constants and input lists change too: `PROMPT` (test_launch.py:36), `PROMPT_SHAPE` (test_no_text.py:66), `_PROMPT_RE` (test_security_invariants.py:67) and the accepted and rejected input lists (test_security_invariants.py:79-111, test_launch.py:89 and :121-134), where `/sc:issue --claim 1` (test_security_invariants.py:81) moves from accepted to rejected; these line numbers are at base 0406ef5b0 and are found again after the rebase. A grep for `--claim`, `PROMPT_PATTERN` and `build_claim_prompt` found 113 mentions in 11 files, which also include docs/designs/issue-watcher.md, docs/designs/issue-watcher-setup.md, launch.py and cycle.py, so the test list above is part of that set, not all of it. This is the last code change that switches the watcher off the governed agent, so it ships only when a coordinator is running, because after it no agent starts for a claimed issue until the coordinator starts the worker.

Start condition: waits on the first live test passing (Task 8 run) and on a running coordinator that has the duties of Task 9. Q35 is answered B1b.

Acceptance criteria:
- `uv run pytest tests/issue_watch/ -v` passes with the full suite, including `test_prompt_regex_property` (security invariants :451) generating only the new form and the NFR-001 tests rejecting every other input.
- A test pins the 12-element argv with the longer prompt, the `retry_argv` form with `--retry-launch <id>` before `--json`, and that `dispatch.json` entries have the same keys as before.
- A test asserts that `build_claim_prompt(9)` returns exactly `/sc:issue --claim 9 --pipeline none`, that the old form `/sc:issue --claim 9` no longer matches `PROMPT_PATTERN`, and that `launch_argv` refuses it.
- Two grep checks, each run before and after the change, replace the earlier pattern that could not match the f-string in the source. `grep -nF -- '--claim {n}' src/superclaude/cli/issue_watch/launch.py | grep -vc 'pipeline none'` and `grep -nF 'claim [1-9]' src/superclaude/cli/issue_watch/launch.py | grep -vc 'pipeline none'` each print 1 before the change (they match `build_claim_prompt` at line 92 and `PROMPT_PATTERN` at line 33 at base d4d1662a8) and must print 0 after it.

## Task 12: Document the coordinator handoff in the claim command and protocol

Depends on: Task 11

Edit `src/superclaude/commands/issue.md` (the `--pipeline none` row and Outputs text, lines 16 and 43-44), `src/superclaude/skills/sc-issue-protocol/SKILL.md` (Wave 6 ending for `none`, Wave 7) and `src/superclaude/skills/sc-issue-protocol/refs/claim.md` (final output for `none`), with `tests/skills/test_issue_protocol.py`, `tests/skills/test_issue_orca_worktree.py` and `tests/commands/test_issue_command.py` (which pins the `--pipeline` row at :112-113, the claim row's `launch-prompt.md` and `worktree.json` text at :172 and the `--pipeline none` example at :174). No claim code changes under B1b. The text says: a claim at `--pipeline none` leaves its files in the checkout that ran it; when a coordinator owns the issue it runs `orca_worktree.py worktree --repo <R> --number <N> --base origin/<B> --source <that folder>` and starts the worker in the printed path; the script creates the worktree with no agent (`orca_worktree.py:681-697` passes no `--agent`, so it is not seen by the require-orca-worktree-agent hook) and closes the plain first tab, so the coordinator must run `worker-start` straight after it, which supplies the agent the project rule asks for; the text says this openly (the owner accepted it as Q41, answer A); its reuse lookup (marker, record, basename, branch) prevents a second `issue-<N>`.

Why B1b needs a worktree with no agent: the script must create the worktree and copy `.dev/issues/<N>/` into it before any agent starts, and a create that carries an agent would start that agent before the copy (the script's own docstring gives this reason, `orca_worktree.py:30-31`). The coordinator's `worker-start --worktree path:<that worktree>` then supplies the agent moments later, so the project rule that every worktree gets an agent is met by the coordinator, not by the script. Risk and mitigation: if the coordinator is down, or crashes between the script and `worker-start`, the worktree sits empty, with no agent and no terminal (the script closed the plain first tab), and nothing runs in it. Nothing starts while the coordinator is down (Decision 5), and the adoption row of Task 3 is still `reserved`, so on its next wake the coordinator finds the row, reuses the worktree through the script's reuse lookup instead of creating a second one, and then runs `worker-start`. A person sees the empty worktree in `orca worktree ps` with an empty `agents` list and can start the coordinator or remove the worktree with `orca worktree rm`.

Also check and, where a sentence becomes false, revise `docs/designs/sc-issue-claim-pipeline-flag.md`, `docs/designs/sc-issue-command.md` and `docs/designs/sc-issue-launch-level-hook.md`, which describe the `--pipeline` levels and the guard. The text keeps `--pipeline worktree` and `full` unchanged for a person who claims without a coordinator.

Start condition: waits on Task 11.

Acceptance criteria:
- The three files describe the handoff in the same words, say that the script creates the worktree without an agent, why (the copy must come first), that `worker-start` follows at once, and what an empty worktree means when the coordinator is down and how the coordinator recovers it, and the three design documents named above have no sentence that contradicts the new handoff. The existing 27 flag and level checks in tests/skills/test_issue_protocol.py still pass with a new check for the handoff paragraph.
- `uv run pytest tests/skills/test_issue_protocol.py tests/skills/test_issue_orca_worktree.py tests/commands/test_issue_command.py tests/hooks/test_require_orca_worktree_agent.py -v` passes, and `make sync-dev` followed by `make verify-sync` passes with no staged `.claude/` path.

## Phase 6: The launch-level guard (Tasks 13 to 15, the G2 work, wait on the first live test and are required before any issue after the test issue; Task 16 can start now)

## Task 13: Write the G2 design note for the governed worker

Depends on: Task 8

Create `docs/designs/issue-pipeline-guard-g2.md`. It states the two collisions measured in ./artifacts/validation.md and chooses the release route (Q38 is answered: the default stands, so no route is chosen before this note). Collision one: `launch-level-guard.sh` blocks every `orca` command except a short read-only list (lines 458-478), so a bound worker cannot run `orchestration send` or `ask`. Collision two: the guard lifts its blocks only on a typed user prompt `approved` or `/sc:implement` (lines 347-364), while B's approval arrives as the result of the worker's `ask`. The note works out how a worker is bound (a `[sc-launch:v1:<nonce>]` marker in its Task spec matches the guard's strict marker rule at line 318, with a `pending/<nonce>` file the coordinator creates) and how a coordinator approval releases it (route A: the coordinator writes the session's `.ok` file after recording the approval, which needs the worker's session id and is UNVERIFIED; route B: a signed approval file the guard reads). It lists the facts to measure before choosing.

Start condition: can be written once the first live test has shown how a worker's session id can be found.

Acceptance criteria:
- The note names both routes with the exact guard lines each changes, the facts to measure, the tests it would add, and a recommendation.
- It states that the guard is a security hook and that any change needs its own independent review before merge.

## Task 14: Change the guard so a bound worker can ask and be released

Depends on: Task 13

Edit `src/superclaude/hooks/scripts/launch-level-guard.sh` and the guard tests `tests/hooks/test_launch_level_guard.py` (73 approval-related mentions), `tests/hooks/test_launch_level_guard_with_identity.py`, `tests/hooks/test_launch_level_observations.py` and `tests/hooks/test_launch_level_guard_l2_tokens.py` (which requires the plugin copy `plugins/superclaude/hooks/scripts/launch-level-guard.sh` to be byte-identical to the source guard, :149-151, so that copy changes in the same commit), plus a coordinator-side release helper chosen in Task 13. The allow-list for `orca` words (guard lines 474-478) gains only `orchestration send` and `orchestration ask`, only for a bound session; every other orca word stays an ESCAPE block. The release route chosen in Task 13 is implemented. Binding a worker to the guard in production (the brief's marker line and the `pending` subcommand the coordinator calls) is Task 15, a separate reviewable change that depends on this one. So that the release of a bound worker is complete and tested here, the hook tests of this task bind their test worker the way the guard binds any session: a first prompt that holds `[sc-launch:v1:<32 hex>]` and a matching `pending/<nonce>` record written by the test (`launch-level-guard.sh:318-330`, `:376-387`), never a `sessions/<id>` file written by hand. The guard still blocks commit, push, merge, GitHub writes and `/sc:implement` until the release, and the pre-push hook (`launch-level-pre-push.sh`) is unchanged.

Start condition: waits on Task 13, which chooses the release route (Q38 stands at its default until then). Required before the flow is used on any issue other than the one G1 test issue.

Acceptance criteria:
- The hook tests create the bound worker through the marker path (a prompt holding the marker and a pending record), and one test runs the whole chain on that worker: bound, `orchestration send` and `ask` allowed, `/sc:implement` blocked, release, `/sc:implement` allowed.
- A bound worker session in the hook tests can run `orchestration send` and `ask` and is still blocked from `git push`, `gh pr create`, `/sc:implement` and every other orca verb.
- After the release step the worker can run `/sc:implement`; before it, it cannot; a forged release from the worker's own session is blocked as tampering (LL-TAMPER).
- `uv run pytest tests/hooks/ -k launch_level -v` passes with all existing cases unchanged, including the byte-identity test of the plugin copy.

## Task 15: Bind a governed worker to the guard with the launch marker

Depends on: Task 7, Task 14

Add a `pending --level <word>` subcommand to `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` that exposes the existing `publish_pending` (defined at :1485 and called only inside `launch`, at :1747; the subcommands are `preflight`, `worktree`, `prompt` and `launch`, :1849-1866) and prints the nonce, so no package code re-implements the 0600 and 0700 pending-record logic (package code cannot import an installed skill script). The brief builder of Task 7 (`src/superclaude/cli/issue_pipeline/brief.py`, `templates/worker-brief.txt`, `tests/issue_pipeline/test_brief.py`) then carries one `[sc-launch:v1:<nonce>]` marker line for a governed worker only, so the guard's strict marker rule (`launch-level-guard.sh:318-330`, `:376-387`) binds the worker's session; the coordinator calls `pending` and passes the nonce to the builder. The brief for the one G1 test issue carries no marker. The skill script's plugin copy, if one exists under `plugins/superclaude/skills/sc-issue-protocol/scripts/`, changes in the same commit.

Start condition: waits on Task 14 (the release route is chosen in Task 13; Q38 stands at its default until then).

Acceptance criteria:
- A test in `tests/skills/test_issue_orca_worktree.py` shows `orca_worktree.py pending --level worktree` writes one 0600 record under `~/.claude/state/launch-level/pending/` (in a temporary HOME) and prints its nonce, and that a second call prints a different nonce.
- A brief built for a governed worker carries exactly one marker line and a brief for the G1 test issue carries none; a hook test shows a worker whose prompt holds the marker becomes bound (a `sessions/<id>` file appears) and one without it does not.
- `uv run pytest tests/skills/test_issue_orca_worktree.py tests/issue_pipeline/test_brief.py tests/hooks/ -k "launch_level or orca_worktree or brief" -v` passes.

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

Start condition: can start now; it does not wait for the first live test, a coordinator, Task 13, or Tasks 14 and 15.

Acceptance criteria:
- After the change no template, guard match, guard hint or final-output line tells a person or an agent that typing `approved` lets the agent proceed, at any worktree-level claim; a search for the word `approved` in the two guard copies, the launch prompt template and `refs/claim.md` finds only the `worktree (approved)` label and the unrelated LL-TURN and LL-ESCAPE text.
- A hook test shows that at level worktree the prompts `approved`, `Approved.` and `approved!` write no `.ok` file and a later `/sc:implement` skill call is still blocked with LL-IMPL, and that a prompt whose first line starts `/sc:implement`, `/sc:task` or `/task` writes the `.ok` file and then allows `/sc:implement`.
- `uv run pytest tests/hooks/ tests/skills/test_issue_protocol.py tests/skills/test_issue_orca_worktree.py -v` passes with the old-route cases changed as listed, and `make sync-dev` followed by `make verify-sync` passes with no staged `.claude/` path.

## Phase 7: Design documents and spec change list (documents can start after the rebase; some wait on code)

## Task 17: Amend the watcher design for the coordinator handoff

Depends on: Task 11

Edit `docs/designs/issue-watcher.md` on the rebased base that holds PR #548. #548 superseded D2 "claim-only" on 2026-11-14 for option 3 (the claim's default level and a second governed agent). B reverses part of that: the watcher's claim returns to claim-only (`--pipeline none`) plus a coordinator handoff, so the section 2.1 D2 row (line 46 on origin/master), the supersede note (line 41), the downstream-sessions text (line 816) and FU-7 (line 864) are revised in the same way #548 did, keeping the history. The text records the guard decision (G1 for the test issue, G2 before any other), the two approval inputs (the approval label, with the Status move as its visible sign that is reported and not required, and the "approved" comment with its rules), that the watcher itself never reads the approval, and the latency note from Q36 (accepted: a GitHub approval waits until the coordinator's next gate or wake, and approving in the coordinator session is immediate). Also check `docs/designs/sc-issue-claim-pipeline-flag.md`, `docs/designs/sc-issue-command.md`, `docs/designs/sc-issue-launch-level-hook.md` and `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md` (lines 261-268, which say the watcher launches `/sc:issue --claim <n>` with no `--pipeline none` and that its sessions carry no launch marker, and a "no worker start" statement near :377) for sentences that the amendment makes false.

Start condition: can be drafted after the rebase; merged only with or after Task 11.

Acceptance criteria:
- The document states the new D2 wording, keeps the original wording marked superseded, and says the poller still never assigns, comments or moves Project items.
- Command checks replace a test file (no test in the repository pins the issue-watcher documents), each verified to run against the document as it stands on origin/master: `grep -c "SUPERSEDED" docs/designs/issue-watcher.md` prints 1 or more before and after the amendment (the old wording stays marked superseded; it matches the D2 row at line 46 today); `grep -cF "never assigns, comments or moves Project items" docs/designs/issue-watcher.md` prints 1 or more before and after (it matches line 46 today); and `git diff --stat origin/master -- docs/designs/issue-watcher.md` lists the file, which shows the D2 row and its note were amended.
- A grep for `second agent` in the document finds only text that matches the new behaviour.

## Task 18: Update the setup runbook for the coordinator precondition

Depends on: Task 8, Task 11

Edit `docs/designs/issue-watcher-setup.md`: section 6 (setup order for each issue) gains the step that a coordinator must be running before the cron entry of section 8.7 is installed, because nothing starts while it is down; section 8.5 (the live-test record) gains the preconditions of Task 8 and the guard-loss acceptance; the owner-acceptance paragraph near line 629 on origin/master is extended to say that the first session is the claim and the second is a worker with no guard. The existing line that says the claim now starts a second agent is revised.

Start condition: can be drafted now on the rebased base; merged with Task 11.

Acceptance criteria:
- Sections 6, 8.5 and the acceptance paragraph carry the new text, each pointing at docs/designs/issue-pipeline-fu1.md.
- `grep -n "second agent" docs/designs/issue-watcher-setup.md` shows only revised text.

## Task 19: Write the change list for the merged requirements and close the open decisions

Depends on: Task 9, Task 15

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
