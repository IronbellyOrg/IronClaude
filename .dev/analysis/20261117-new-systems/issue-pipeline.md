# Issue pipeline approval core (issue-watcher claim handoff)

Source: origin/master as of 2026-11-17. Read-only analysis. Footer token: graph:stale.

## 1. What it is

The issue-pipeline is the approval core for one specific handoff: the issue-watcher (a cron poller that finds approved GitHub issues) launches a claim session, and a person-opened Orca coordinator then starts a plan-writing worker for that issue and waits for a human to approve the plan. This package supplies the parts that must not go wrong: a hash that pins the plan, strict rules for what counts as approval (a label or an `approved` comment, or an Orca reply), a locked on-disk record so approval is recorded once and the stage never starts twice, a read-only status verb, and a fixed worker brief. It prints only closed words and never relays GitHub text.

**PRs (all merged to origin/master):**
- #548, 2026-11-14: docs only. Records the owner's "option 3" claim-level decision: the claim keeps its default `worktree` level, so the old D2 "claim-only" is marked superseded, and downstream sessions per approval go from one to two (`docs/designs/issue-watcher.md:41`, `:46`; `issue-watcher-setup.md:629`).
- #584, 2026-11-17 04:00Z ("Plan A, Decision 6 = B"): the code, tests, recorded fixtures and the FU-1 runbook.
- #585, 2026-11-17 05:03Z: narrows the D2 amendment wording: a person gives a Ruling in chat and the agent in that session records the Ruling line; the person is never required to write a Ruling line into a file (`src/superclaude/core/WORKER-CONTRACT.md`, `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md`). Other owner records (grant row, pass record) are still written by the owner.

**Entry points:** CLI group `superclaude issue-pipeline` (registered at `src/superclaude/cli/main.py:567-569`) with verbs `plan-hash`, `check-approval`, `init`, `adopt-create`, `adopt-mark`, `record-create`, `record-show`, `record-mark`, `stage-status`. Library entry: `brief.build(issue, type, complexity)`. Files: `src/superclaude/cli/issue_pipeline/{approval_record,approval_line,plan_hash,stage_predicates,reads,brief,cli}.py`, `templates/worker-brief.txt`; tests in `tests/issue_pipeline/` and `tests/cli/test_issue_pipeline_registered.py`; runbook `docs/designs/issue-pipeline-fu1.md`.

**Built versus document-only:** the code, tests and fixtures are built. The runbook `issue-pipeline-fu1.md` is headed "runbook only" (line 3), but its section 6 now holds `RECORDED:` lines a to k dated 2026-11-17 on throwaway issue 452 and a closing `RUN BY OWNER: ironbelly` line (lines 108-119), so the live test was run and recorded (steps a to j by an agent on the owner's chat instruction, k by the owner in a browser). Not built: "Plan B" (the coordinator route that calls these verbs, and the launch-guard change G2); the PR body says so, and nothing outside `cli.py` and `main.py` references the package (grep of `src` and `plugins` on origin/master).

## 2. How it works

**Flow.** (1) Coordinator runs `init` once, then `adopt-create` for (issue, stage). Only a `created` result may call `worker-start`. (2) Coordinator starts the worker with the brief, then `adopt-mark --state started --dispatch-id ...` (or `uncertain` if Orca did not report ready). (3) Worker writes plan files; the coordinator computes `plan-hash` and posts a plan reply carrying a hidden marker `<!-- sc:stage:plan id=<record-id> plan=<64 hex> -->`. (4) A human approves. (5) `stage-status` (read-only) or the coordinator calls `record-create` with the channel, evidence id and actor; then `record-mark` to `instructed` and `acked`. Steps 1, 2 and 5 are the not-yet-built Plan B caller; this package supplies the verbs.

**Plan hash** (`plan_hash.py:77-90`): names sorted by bytes; per file, 8-byte length plus name, then 8-byte length plus content, so moving bytes between files changes the hash. Refusal words (`REASONS`, lines 24-36) include symlink, dotdot-name, outside-dir. FU-1 step e recorded identical hashes on both sides (`472a3bed...81b6`).

**Approval line** (`approval_line.py:18-62`): only `approved` or `approved ap-<N>-plan-<12 hex> plan-sha256=<64 hex>`, whole text. `check-approval` returns `ok`, `refused:bare` (short form is valid only on the comment channel), `refused:mismatch`, `refused:malformed` or a plan-hash reason.

**Locked write-ahead record** (`approval_record.py`):
- Directory 0700 and `lock` file 0600, created only by `init_dir` (lines 81-98), refusing symlinks.
- Every mutation runs under `FileStore(dir).lock()`, a non-blocking exclusive flock (`issue_watch/record.py:381-403`); contention maps to `lock-held`, and the CLI exits 75 with "lock-held, retry" (`cli.py:25`, `:33-35`).
- Adoption states move only `reserved` to `started` or `uncertain`, and `uncertain` to `started` (lines 287-292). An existing row blocks a second `adopt_create`: `already-started` or `uncertain-launch` (lines 248-253). This is the "never start twice" guarantee; `uncertain` is settled by a person or by reading `worker-list`, never by starting again.
- Approval states move forward only: `recorded`, `instructed`, `acked`; `revoked` from any non-revoked state (lines 408-412). A second approval on the same key from either channel appends evidence to one row; a replay of the same (channel, id) is a no-op, so it cannot undo a revoke; new evidence reopens a revoked row (lines 360-368).
- Every row is validated on read against exact key sets and fixed regexes; a bad row is `row-invalid` (lines 177-222). Writes use `write_prepared_bytes` plus a directory fsync (lines 225-229).

**Stage predicates** (`stage_predicates.py`; pure, no I/O). Approval label versus approved comment:

| Rule | Label channel | Comment channel |
|---|---|---|
| Order | Applied after the plan reply, and no later `unlabeled` | Created after the plan reply (`comment-before-plan`) |
| Who | `User` type, and assignee login or listed approver id | Same; any other commenter is ignored (public repo) |
| Edits | not applicable | Never edited (`edit-unknown` fails closed; `comment-edited`) |
| Plan binding | by position (after the reply) | short form by position; long form must carry the latest reply's record id and hash (`hash-mismatch`) |
| Revocation | Removing the label is a revocation signal | Deleting or editing an approving comment is not |

Both channels give the same key (issue, stage, plan hash) (lines 247-301). The plan reply itself must be unedited and the live plan files must still hash to the marker, otherwise state is `plan-changed`. Equal timestamps never count as "after". A Project Status move is reported as `status_seen` but is never required. The code reports, rather than hides, `actor_is_host_login` and `assignee_is_host_login` (Decision 4: the worker shares the host's one GitHub login and could approve itself).

**Reads** (`reads.py`): the `COMMENTS_JQ` projection (lines 44-55) turns each body into booleans, a form, record id, hash and marker values inside `gh --jq`, so comment text never reaches Python; Python re-checks each value against a fixed pattern (lines 78-104). Events, comments and edits are read under one shared call budget and page cap; any failure returns a closed reason (lines 130-151).

**stage-status** (`cli.py:242-371`): reads the host login, the issue snapshot (assignees), the evidence, optionally recomputes the plan hash from `--plan-dir` and `--plan-file`, evaluates, and merges adoption and row state read without writing. Without plan files it uses the marker's own hash and says so (`plan_files_checked: false`). An unreadable plan counts as changed. It takes the approval label and approver ids from the watcher's config (`cli.py:201-204`). The tests assert it never calls Orca (`test_stage_status.py:451`).

**Worker brief** (`brief.py`, `templates/worker-brief.txt`): the only inputs are a validated issue integer and a complexity from `simple|medium|complex`; type `bug` is refused (`brief.py:47-59`). The template holds a head (Guard, Chain, `On a blocked gate: report blocked`, `Local commit: not authorized`, report dir `.dev/issues/{N}/worker-plan`, `Outward actions: none`) and per-complexity command rows: simple = brainstorm quick then workflow quick; medium = brainstorm blind, design, workflow standard; complex = deep brainstorm, design, workflow deep. All rows are `--unattended` and stop before `/sc:implement`. A test keeps the fixed lines equal to section 5 of `WORKER-CONTRACT.md` (`tests/issue_pipeline/test_brief.py:154`).

**Tests:** concurrency (one winner under parallel `record_create` and `adopt_create`), crash (a killed write; a kill between `worker-start` and `adopt-mark` blocks a second start), line, hash, predicates (equal timestamps, edited comments, revocation), reads (hostile body never reaches output; page and call caps), status (recorded fixtures, closed keys only), brief. Fixtures are real GitHub responses for throwaway issue 452 (`tests/issue_pipeline/fixtures/recorded/README.md`). PR #584 reports 2831 tests passing across issue_pipeline, issue_watch and CLI registration tests (not re-run here).

**FU-1 findings that shaped behaviour** (runbook record): `worker-start` runs claude with permissions off; the reply to an `ask` is stored as type `status`; `ask` resumes by message id; the claim worktree step is idempotent (`reused`); label and Status events show actor and type; a web-typed `approved` arrives as exactly `approved` and an edit sets `lastEditedAt`.

## 3. Where it could be integrated in future

The reusable idea is "a human approval gate on an agent-produced artifact, proven from public facts, bound to a content hash, recorded once". Candidate system types:

- **Other supervised-worker stages.** A later stage (implement, PR submit) needing a person's go after a plan or diff. The key is already (issue, stage, hash), and `stage` is a parameter (`approval_record._STAGE`), though `stage_predicates.STAGE` is hardcoded to `plan`. Why: the same never-start-twice and replay-safe record applies.
- **Any pipeline with a "wait for owner" step that currently relies on chat memory**, such as roadmap or sprint phase gates. Why: a hash-pinned, ledgered approval replaces "the agent says the owner said yes".
- **Public-repo bots and review bots** that act only on the maintainer's comment or label. Why: the rules (User type, allowed ids, no edits, order after a marker, fail-closed on unknown edit state) are a ready threat model.
- **Release or deploy gates** keyed to an artifact hash (changed artifact voids the approval). Why: `plan-changed` is exactly this.
- **Idempotent launch guards** for any "start an expensive worker once" job: the adoption row alone (reserved, started, uncertain) solves double starts after a crash.
- **Prompt-safe worker briefs** for any dispatcher that must not let user text into an agent prompt: the template-with-enums approach in `brief.py`.

## 4. Integration guide

Best path: call it through the CLI from a coordinator, not by importing internals, because every verb prints closed words and uses stable exit codes (0 ok, 1 refused, 2 config, 75 lock held).

1. **Once per workspace:** `uv run superclaude issue-pipeline init <approvals_dir>`. Keep the directory separate from the watcher's state dir and never touch `dispatch.json`.
2. **Before starting a worker:** `adopt-create <dir> --issue N --stage plan`. Proceed only on `result: created`. `already-started` or `uncertain-launch` means stop and ask a person or read `worker-list`. Exit 75 means retry.
3. **Build the brief** with `brief.build(N, "feature", complexity)` (Python call; there is no CLI verb). Take type and complexity from the claim's summary file. Pass the output to `worker-start --spec`.
4. **After the start receipt:** `adopt-mark --state started --dispatch-id <id>` (id field from the receipt: runbook d says the Dispatch id is a key of the receipt result, `dispatchId`). On a not-ready start, `--state uncertain`.
5. **When the plan files exist:** `plan-hash <report_dir> <names...>`; post the plan reply with the marker line using the printed hash and `ap-<N>-plan-<first 12 hex>`.
6. **Polling for approval:** `stage-status N --approvals-dir <dir> --plan-dir <dir> --plan-file a.md ...`. Act only when `state` is `approved`; when it is, `record-create --channel label|comment|reply --evidence-id ... --actor ...` for each accepted channel, then send the Orca instruction, `record-mark --state instructed`, then `acked` after the worker's ack. For an Orca reply, use `check-approval` on the line first.
7. **Revocation:** `state: revoked` or `plan-changed` maps to `record-mark --state revoked`.

Reuse: `FileStore.lock`, the watcher's `gh` helpers and `CallBudget`, `write_prepared_bytes`, the closed-word convention.

Pitfalls:
- Do not feed GitHub text into any prompt; read only the closed JSON keys.
- `plan-hash` prints `plan-sha256: <hash>` (colon, space); the approval line uses `plan-sha256=<hash>` (runbook e, line 64).
- The reply to `ask` is stored as type `status`; do not read with a narrow `--types question` filter (runbook c).
- `gh --jq` runs gojq, tests ran under jq 1.7; re-check the projection against a live reply (PR body; `reads.py` docstring). Runbook j and k record the label and web-comment shapes but I did not find an explicit gojq-versus-jq check in the record (UNVERIFIED).
- Equal timestamps fail closed, so an approval in the same second as the plan reply is refused; tell humans to wait a second.
- The worker and the person share one GitHub login; the label or comment channel cannot tell them apart.
- The flag `actor_is_host_login` should be surfaced to the person, not ignored.

Tests to add in a new caller: a crash between `adopt-create` and `worker-start`; two coordinators racing on one issue (copy `test_approval_concurrency.py`); a plan edited after approval; a stage other than `plan` (the predicate constant is hardcoded); a round trip through `stage-status` with the recorded fixtures as the fake `gh` runner (`test_stage_status.py` shows the `World` fixture).

## 5. IronClaude fit

Looked at: `src/superclaude/cli/` packages on origin/master (issue_watch, swarm, sweep, sprint, roadmap and others), `commands/issue.md`, `core/WORKER-CONTRACT.md`, and `skills/sc-implement-protocol/refs/qa.md`. A grep for approval gates in `cli/sprint` and `cli/roadmap` found only the unrelated `PRE_APPROVED` deviation class in `roadmap/executor.py` and `gates.py`, and a grep in the pr-submit skill and CLI found no approval gate. So there is no good fit there.

Ranked proposals:

1. **Finish the claim handoff it was built for (Plan B).**
   - Target: `src/superclaude/cli/issue_watch/` (cycle and claim path) and `src/superclaude/commands/issue.md` (`--pipeline` default `worktree`, line 43), plus the coordinator steps in `src/superclaude/core/WORKER-CONTRACT.md`.
   - Change: a coordinator script or skill that runs the integration guide steps 1 to 7 and the launch-guard change G2 named in the runbook.
   - Value: high, since without it the package is dormant. Effort: medium to high. Risk: medium to high: the plan worker runs with permission checks off and no launch guard (runbook section 2, lines 16-18), and the owner accepted that for test issue 452 only. The runbook says no other issue runs through the flow until the guard changes.
2. **Template-built briefs for other coordinator-started workers.**
   - Target: `src/superclaude/core/WORKER-CONTRACT.md` section 5 (brief layout, lines 303-316) and any coordinator that hand-writes briefs.
   - Change: generalize `brief.py` (closed enums, one validated integer, fixed template, a test that copies fixed lines from the contract) into a shared builder.
   - Value: medium (removes prompt-injection and drift). Effort: low to medium. Risk: low.
3. **Hash-pinned record for Ruling confirmations in `/sc:implement`.**
   - Target: `src/superclaude/skills/sc-implement-protocol/refs/qa.md` (Halt table, lines 247-249) and `refs/ledger.md` (UNVERIFIED: not read).
   - Change: store each Ruling as a row keyed (task, verdict hash) with evidence, so a changed verdict voids it.
   - Value: low to medium. Effort: medium. Risk: medium. Poor match: a Ruling is a chat confirmation from the person (as amended by #585), not a GitHub fact the predicates can prove, so only the record and hash pieces fit and the predicates do not. Do this only if Ruling reuse across a changed task has actually been a problem (no evidence found).

Not recommended: using the stage predicates for sprint or roadmap gates, since those flows have no GitHub-side approval.

## 6. Limits, open questions, UNVERIFIED

**Limits**
- Only the `plan` stage and Feature briefs are built; type `bug` is refused (`brief.py:53-54`); `stage_predicates.STAGE = "plan"` is a constant.
- Self-approval risk is accepted, not solved (Decision 4): the worker shares the host login. The code flags it and nothing more. The worker also runs with permissions off in the live test.
- The package has no caller in `src` beyond its own CLI; Plan B (coordinator route, guard G2) is not merged.
- Runbook steps a to j were run by an agent on the owner's chat instruction; only k was done by the owner in a browser. The runbook's status line still says "runbook only", and its text says the agent that wrote it runs nothing, which sits oddly beside the filled record. The record is real; the header is stale.
- Approvals directory is plain files on one host; there is no multi-host story.

**Open questions**
- Does the jq projection behave the same under gojq (what `gh --jq` runs)? The PR body and `reads.py` docstring defer this to the live run. I found no explicit gojq result in the runbook record (UNVERIFIED), though live step k read a real comment through the REST call.
- Whether the owner's acceptance of permission-checks-off covers the second agent is stated as not confirmed (`issue-watcher-setup.md:629`).
- Whether `refused:bare` for the short form in `check-approval` will confuse callers on the reply channel (design intent per `approval_line.py:51`).

**UNVERIFIED**
- I did not run the test suite; the 2831 figure comes from the PR body.
- Did not read `skills/sc-implement-protocol/refs/ledger.md`, `commands/issue.md` beyond lines 1-56, or the full WORKER-CONTRACT.
- Line numbers refer to origin/master at read time (2026-11-17); the repo moves fast.
- Codegraph was not used (graph:stale), so callers were found by `git grep` only.

---
Footer: graph:stale. Companion explanation: `/home/coder/workspaces/IronClaude/.dev/analysis/20261117-new-systems/issue-pipeline-explain.md`.
