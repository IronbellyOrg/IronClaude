# Issue watcher handoff, Plan B: the tasks that wait on the first live test

Source: ./source.md
Goal: Everything that cannot start before the owner has run and recorded the first live test: the coordinator and worker rules, the watcher prompt change, the claim handoff text, the guard work for later issues (G2) and the design documents. Plan A (`.dev/tasks/to-do/TASK-WF-planDecision6BFo-20261114-174909/TASK-WF-planDecision6BFo-20261114-174909.md`, in the sibling package, which may be archived under `.dev/tasks/done/` by then) holds the work that runs now.

## Constraints

- Plan only. This is Plan B of two; Plan A (package `TASK-WF-planDecision6BFo-20261114-174909`) holds Tasks 16, 1, 2, 8, 3 to 7 and 19. The owner decisions are answered in Plan A Task 19; what stays open are facts the first live test must measure (Plan A Task 8). Task numbers are stable across both plans, so they are not contiguous here.
- File order is the gate. `/sc:implement` runs items in file order and ignores `Depends on` and `Start condition` text, so Task 20 (the owner-run gate: the first live test run and recorded in docs/designs/issue-pipeline-fu1.md) comes first and no later item runs before the owner has recorded it. This file has no managed-plan front matter on purpose, so `/sc:implement` cannot run it as a managed plan; run it only on the owner's separate go (it is already in its own package, so Plan A's archive does not touch it). A `Depends on` line names only a task earlier in this file or a task of Plan A. No push, PR, GitHub write or Orca write verb is authorized by this plan.
- Rebase first. This plan was written on base 0406ef5b0. origin/master is now d4d1662a8 and already holds PR #539 (sweep) and PR #548 (the D2 "claim-only" superseded note in docs/designs/issue-watcher.md). Every task below starts from a worktree based on current origin/master.
- Evidence for every factual claim is in ./artifacts/validation.md (read-only measurements, file and line citations, and what is UNVERIFIED). Real code locations are in ./artifacts/codegraph-grounding.md.
- Chosen claim-side change: B1b, the watcher claims with `--pipeline none` and the coordinator runs the existing `orca_worktree.py worktree` step, then `worker-start --worktree path:<that worktree>`. The owner confirmed it on 2026-11-14 and again on 2026-11-15 (Q35 = B1b; the first reply wrote "Q53 b1b" next to "2. Approved", read as Q35). B2, a new claim level, is not built.
- Owner answers: see Plan A Task 19.
- Owner decision Q34 (2026-11-14): the plan-writing worker runs without the launch-level guard (G1) for ONE test issue only. The written acceptance must cover the loss of the guard itself (no block on commit, push, merge, GitHub writes or /sc:implement), the owner writes that issue's text, and it is not stretched from the Decision 1 acceptance of permission checks off. Before any other issue runs through this flow, the guard is changed (G2, Tasks 13 to 15 of this file).
- Accepted earlier and carried here: only the coordinator tells the worker to proceed; one person-opened coordinator owns all watcher-claimed issues on this host with a lock per issue; nothing starts while the coordinator is down; one grant row per pipeline issue; one GitHub login on this host means an agent could apply the approval label or post the approval comment (Decision 4, accepted).
- New code goes in a new package `src/superclaude/cli/issue_pipeline/` and tests in `tests/issue_pipeline/`. The tests in tests/issue_watch/test_module_boundaries.py pin what each issue_watch module may import, and tests/issue_watch/test_no_text.py forbids a gh call that asks for comment text, so issue_pipeline imports from issue_watch and never the reverse.
- Never edit `.claude/` mirrors; edit `src/superclaude/` and run `make sync-dev`. Always stage `.dev/tasks` and the `src/` changes, never `.claude/`; commit only when the owner asks.
- The merged requirements file in the brainstorm folder is not edited by any task; Plan A Task 19 writes the change list for it inside this package.
- Every command is run with `uv run`.

## Phase 1: Gate (owner-run): the first live test is run and recorded

## Task 20: Gate: the owner runs the first live test and records it in docs/designs/issue-pipeline-fu1.md

Depends on: Task 8

This item is a gate, not work an agent does. The owner runs the first live test by the runbook of Task 8 (`docs/designs/issue-pipeline-fu1.md`), in a session the owner opens, with the owner's written acceptance for the one test issue (guard loss included), a separate live-test grant, a reachable Orca and a named owner of the watcher worktree, and writes each result into the runbook's record section by replacing its `PENDING:` line with a `RECORDED:` line (the value measured, the Orca build string from `orca-ide --version`, the date). An executor that reaches this item finds the record missing and stops here: it never runs the test, never runs an Orca write verb and never fills in a result. `/sc:implement` runs items in file order and ignores `Depends on` and `Start condition` lines, so the position of this item, first in this file, is what keeps every later item from running before the record exists; each later item also names it in its `Depends on` line.

Start condition: owner-run; waits on the owner.

Acceptance criteria:
- `docs/designs/issue-pipeline-fu1.md` holds one `RECORDED:` line for each of the preconditions a to k and no `PENDING:` line: `grep -c "^RECORDED: [a-k] " docs/designs/issue-pipeline-fu1.md` prints 11 and `grep -c "^PENDING: " docs/designs/issue-pipeline-fu1.md` prints 0. A precondition that could not be measured is recorded as `RECORDED: <letter> NOT MEASURABLE: <reason>`, with the owner's name.
- The record names who ran it: `grep -c "^RUN BY OWNER: " docs/designs/issue-pipeline-fu1.md` prints 1.

## Phase 2: Coordinator and worker rules

## Task 9: Add the issue-pipeline duties to the coordinator rules

Depends on: Task 3, Task 6, Task 7, Task 20

Edit `src/superclaude/core/WORKER-CONTRACT.md` section 4 and its pin test `tests/skills/test_worker_contract.py`; run `make sync-dev` and stage only the `src/` side. Add a subsection "Issue pipeline duties" stating, in the contract's style: adopt a claimed issue from sources that exist after a `--pipeline none` claim, which writes no `worktree.json` and creates no worktree (`refs/claim.md:93`): the watcher store's `claimed` entry in `dispatch.json`, read-only, and `.dev/issues/<N>/issue-summary.md` and `next-steps.md` in the checkout that ran the claim; take the per-issue reservation by creating the adoption row (Task 3) before `worker-start`, mark it `started` with the Dispatch id when `worker-start` returns ready and `uncertain` when it does not, and never start again for an `uncertain` row (settle it by reading `worker-list`); create the plan-hash approval row only when the worker's `ask` carries the plan hash; run the existing `orca_worktree.py worktree` step from the installed skill and then `worker-start --worktree path:<exact path> --agent claude --spec <Task 7 brief>`; read the worker's `ask`, post the plan reply with the hash and file list and mention the assignee, then read GitHub through `stage-status` at each gate or wake; on approval write the row, then `reply` with `approved <record-id> plan-sha256=<hash>`, then mirror the label and Status; mark the row from the worker's ack. It adds to the never-list: never tell a worker to pass its plan boundary without a row, never act on a Status move alone, never relaunch a dead worker by itself, never post an issue write without the issue's grant row. It does not add any exception to "never answer a person prompt", because route B needs none. It also extends the `Worktree:` slot of the brief template in section 5 (WORKER-CONTRACT.md line 308, inside the template block of lines 302-311), which today allows only the shared feature worktree or `new-child`, to allow `path:<existing worktree>`, a form section 4 already uses for resume Tasks (line 280).

Start condition: waits on the recorded first live test (Task 20) showing the `ask` and `reply` round trip, and on a coordinator existing.

Acceptance criteria:
- WORKER-CONTRACT.md has the new subsection and the new never-list lines, and no line that permits typing into a worker's prompt.
- The adoption sentence names only sources that exist after a `--pipeline none` claim, and a pin test in tests/skills/test_worker_contract.py fails if `worktree.json` is named as an adoption source; the `Worktree:` slot at line 308 allows `path:<existing worktree>` and Task 7's template test still passes against it.
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

## Phase 3: Watcher prompt and claim handoff

## Task 11: Change the watcher's claim prompt to `--pipeline none`

Depends on: Task 9, Task 10, Task 20

Edit `src/superclaude/cli/issue_watch/launch.py`: `PROMPT_PATTERN` (:33) becomes `^/sc:issue --claim [1-9][0-9]{0,8} --pipeline none$`, `build_claim_prompt` (:84) returns `/sc:issue --claim <n> --pipeline none`, and the docstrings that quote the old prompt are updated. `launch_argv` stays a 12-element list and `retry_argv` inherits the new prompt. `src/superclaude/cli/issue_watch/record.py` and the at-most-once `dispatch.json` are not touched. Callers that change behaviour only through the prompt string: `_launch` (cycle.py:1026) and `status_report` (cycle.py:1270). Update every test that quotes the prompt: tests/issue_watch/test_launch.py (:41, :47, :54, :67, :75, :95, :102, :141, :152, :805, :817, :841, :913), tests/issue_watch/test_security_invariants.py (:451, :522, :584, :621, :697, :921), tests/issue_watch/test_no_text.py (:464), tests/issue_watch/test_cli.py (:582), tests/issue_watch/test_cycle.py, tests/issue_watch/test_cli_e2e.py, tests/issue_watch/test_crash_injection.py and tests/issue_watch/conftest.py (:279). The prompt constants and input lists change too: `PROMPT` (test_launch.py:36), `PROMPT_SHAPE` (test_no_text.py:66), `_PROMPT_RE` (test_security_invariants.py:67) and the accepted and rejected input lists (test_security_invariants.py:79-111, test_launch.py:89 and :121-134), where `/sc:issue --claim 1` (test_security_invariants.py:81) moves from accepted to rejected; these line numbers are at base 0406ef5b0 and are found again after the rebase. A grep for `--claim`, `PROMPT_PATTERN` and `build_claim_prompt` found 113 mentions in 11 files, which also include docs/designs/issue-watcher.md, docs/designs/issue-watcher-setup.md, launch.py and cycle.py, so the test list above is part of that set, not all of it. This is the last code change that switches the watcher off the governed agent, so it ships only when a coordinator is running, because after it no agent starts for a claimed issue until the coordinator starts the worker.

Start condition: waits on the recorded first live test (Task 20) and on a running coordinator that has the duties of Task 9. Q35 is answered B1b.

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

## Phase 4: The launch-level guard for later issues (G2)

## Task 13: Write the G2 design note for the governed worker

Depends on: Task 20

Create `docs/designs/issue-pipeline-guard-g2.md`. It states the two collisions measured in ./artifacts/validation.md and chooses the release route (Q38 is answered: the default stands, so no route is chosen before this note). Collision one: `launch-level-guard.sh` blocks every `orca` command except a short read-only list (lines 458-478), so a bound worker cannot run `orchestration send` or `ask`. Collision two: the guard lifts its blocks only on a typed user prompt `approved` or `/sc:implement` (lines 347-364), while B's approval arrives as the result of the worker's `ask`. The note works out how a worker is bound (a `[sc-launch:v1:<nonce>]` marker in its Task spec matches the guard's strict marker rule at line 318, with a `pending/<nonce>` file the coordinator creates) and how a coordinator approval releases it (route A: the coordinator writes the session's `.ok` file after recording the approval, which needs the worker's session id and is UNVERIFIED; route B: a signed approval file the guard reads). It lists the facts to measure before choosing.

The note also decides the address a bound worker may send to. Letting a bound worker run `orchestration send` and `ask` would otherwise let it message another worker or every worker (`@all`). The note chooses a coordinator-only address: the allow-list admits `orchestration send` and `ask` only when the command either has no `--to` (the coordinator is the default recipient for heartbeat, status and `worker_done`) or names the run's own coordinator address (`run:<id>`, used for blockers), and refuses `--to dispatch:<other>` and `@all`. If the first live test shows the guard cannot check the address (the address forms are UNVERIFIED), the note instead states the residual risk in one paragraph: a bound worker could message another worker, and the coordinator treats any message it did not ask for as untrusted data.

Start condition: can be written once the recorded first live test (Task 20) has shown how a worker's session id can be found.

Acceptance criteria:
- The note names both routes with the exact guard lines each changes, the facts to measure, the tests it would add, and a recommendation.
- The note states the coordinator-only address rule (or the residual risk) in words that Task 14 turns into a test.
- It states that the guard is a security hook and that any change needs its own independent review before merge.

## Task 14: Change the guard so a bound worker can ask and be released

Depends on: Task 13

Edit `src/superclaude/hooks/scripts/launch-level-guard.sh` and the guard tests `tests/hooks/test_launch_level_guard.py` (73 approval-related mentions), `tests/hooks/test_launch_level_guard_with_identity.py`, `tests/hooks/test_launch_level_observations.py` and `tests/hooks/test_launch_level_guard_l2_tokens.py` (which requires the plugin copy `plugins/superclaude/hooks/scripts/launch-level-guard.sh` to be byte-identical to the source guard, :149-151, so that copy changes in the same commit), plus a coordinator-side release helper chosen in Task 13. The allow-list for `orca` words (guard lines 474-478) gains only `orchestration send` and `orchestration ask`, only for a bound session; every other orca word stays an ESCAPE block. The release route chosen in Task 13 is implemented. Binding a worker to the guard in production (the brief's marker line and the `pending` subcommand the coordinator calls) is Task 15, a separate reviewable change that depends on this one. So that the release of a bound worker is complete and tested here, the hook tests of this task bind their test worker the way the guard binds any session: a first prompt that holds `[sc-launch:v1:<32 hex>]` and a matching `pending/<nonce>` record written by the test (`launch-level-guard.sh:318-330`, `:376-387`), never a `sessions/<id>` file written by hand. The guard still blocks commit, push, merge, GitHub writes and `/sc:implement` until the release, and the pre-push hook (`launch-level-pre-push.sh`) is unchanged.

Start condition: waits on Task 13, which chooses the release route (Q38 stands at its default until then). Required before the flow is used on any issue other than the one G1 test issue.

Acceptance criteria:
- The hook tests create the bound worker through the marker path (a prompt holding the marker and a pending record), and one test runs the whole chain on that worker: bound, `orchestration send` and `ask` allowed, `/sc:implement` blocked, release, `/sc:implement` allowed.
- A bound worker session in the hook tests can run `orchestration send` and `ask` to the coordinator address chosen in Task 13 and is still blocked from `git push`, `gh pr create`, `/sc:implement` and every other orca verb.
- Negative test (when Task 13 chose the coordinator-only address rule): a bound worker running `orchestration send --to dispatch:<other worker>` and one addressed to `@all` are each blocked; when Task 13 instead recorded the residual risk, a test pins that sentence in the design note.
- After the release step the worker can run `/sc:implement`; before it, it cannot; a forged release from the worker's own session is blocked as tampering (LL-TAMPER).
- `uv run pytest tests/hooks/ -k launch_level -v` passes with all existing cases unchanged, including the byte-identity test of the plugin copy.

## Task 15: Bind a governed worker to the guard with the launch marker

Depends on: Task 7, Task 14

Add a `pending --level <word>` subcommand to `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` that exposes the existing `publish_pending` (defined at :1485 and called only inside `launch`, at :1747; the subcommands are `preflight`, `worktree`, `prompt` and `launch`, :1849-1866) and prints the nonce, so no package code re-implements the 0600 and 0700 pending-record logic (package code cannot import an installed skill script). The brief builder of Task 7 (`src/superclaude/cli/issue_pipeline/brief.py`, `templates/worker-brief.txt`, `tests/issue_pipeline/test_brief.py`) then carries one `[sc-launch:v1:<nonce>]` marker line for a governed worker only, so the guard's strict marker rule (`launch-level-guard.sh:318-330`, `:376-387`) binds the worker's session; the coordinator calls `pending` and passes the nonce to the builder. The brief for the one G1 test issue carries no marker. No plugin copy of `orca_worktree.py` exists (checked 2026-11-15: `plugins/superclaude/skills/` holds only `confidence-check`, `sc-implement-protocol`, `sc-recommend` and `sc-workflow-protocol`), so only the `src/` file changes; the executor repeats that `ls` and stops to ask if a copy has appeared.

Start condition: waits on Task 14 (the release route is chosen in Task 13; Q38 stands at its default until then).

Acceptance criteria:
- A test in `tests/skills/test_issue_orca_worktree.py` shows `orca_worktree.py pending --level worktree` writes one 0600 record under `~/.claude/state/launch-level/pending/` (in a temporary HOME) and prints its nonce, and that a second call prints a different nonce.
- A brief built for a governed worker carries exactly one marker line and a brief for the G1 test issue carries none; a hook test shows a worker whose prompt holds the marker becomes bound (a `sessions/<id>` file appears) and one without it does not.
- `uv run pytest tests/skills/test_issue_orca_worktree.py tests/issue_pipeline/test_brief.py tests/hooks/ -k "launch_level or orca_worktree or brief" -v` passes.

## Phase 5: Design documents

## Task 17: Amend the watcher design for the coordinator handoff

Depends on: Task 20

This task edits documents only and needs no code from Tasks 11 to 15; it follows the gate so that the text states recorded facts.

Edit `docs/designs/issue-watcher.md` on the rebased base that holds PR #548. #548 superseded D2 "claim-only" on 2026-11-14 for option 3 (the claim's default level and a second governed agent). B reverses part of that: the watcher's claim returns to claim-only (`--pipeline none`) plus a coordinator handoff, so the section 2.1 D2 row (line 46 on origin/master), the supersede note (line 41), the downstream-sessions text (line 816) and FU-7 (line 864) are revised in the same way #548 did, keeping the history. The text records the guard decision (G1 for the test issue, G2 before any other), the two approval inputs (the approval label, with the Status move as its visible sign that is reported and not required, and the "approved" comment with its rules), that the watcher itself never reads the approval, and the latency note from Q36 (accepted: a GitHub approval waits until the coordinator's next gate or wake, and approving in the coordinator session is immediate). Also check `docs/designs/sc-issue-claim-pipeline-flag.md`, `docs/designs/sc-issue-command.md`, `docs/designs/sc-issue-launch-level-hook.md` and `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md` (lines 261-268, which say the watcher launches `/sc:issue --claim <n>` with no `--pipeline none` and that its sessions carry no launch marker, and a "no worker start" statement near :377) for sentences that the amendment makes false.

Start condition: can be drafted after the rebase; the pull request is merged only with or after Task 11 (a merge order, not an item dependency).

The new D2 wording uses two exact phrases: `claim-only again, with a coordinator handoff` (the watcher's claim returns to `--pipeline none` and a coordinator starts the worker) and `no launch-level guard for the one test issue` (the G1 decision of Q34, with G2 before any other issue).

Acceptance criteria:
- The document states the new D2 wording with both exact phrases, keeps the original wording marked superseded, and says the poller still never assigns, comments or moves Project items.
- Command checks replace a test file (no test in the repository pins the issue-watcher documents), each run against the document as it stands on origin/master (checked 2026-11-15 on base d4d1662a8): `grep -cF "claim-only again, with a coordinator handoff" docs/designs/issue-watcher.md` prints 0 before the amendment and 1 or more after; `grep -cF "no launch-level guard for the one test issue" docs/designs/issue-watcher.md` prints 0 before and 1 or more after; `grep -c "SUPERSEDED" docs/designs/issue-watcher.md` prints 1 before (the D2 row at line 46) and 1 or more after; `grep -cF "never assigns, comments or moves Project items" docs/designs/issue-watcher.md` prints 1 before and 1 or more after; and `git diff --stat origin/master -- docs/designs/issue-watcher.md` lists the file.
- A grep for `second agent` in the document finds only text that matches the new behaviour.

## Task 18: Update the setup runbook for the coordinator precondition

Depends on: Task 8, Task 20

Edit `docs/designs/issue-watcher-setup.md`: section 6 (setup order for each issue) gains the step that a coordinator must be running before the cron entry of section 8.7 is installed, because nothing starts while it is down; section 8.5 (the live-test record) gains the preconditions of Task 8 and the guard-loss acceptance; the owner-acceptance paragraph near line 629 on origin/master is extended to say that the first session is the claim and the second is a worker with no guard. The existing line that says the claim now starts a second agent is revised.

Start condition: can be drafted after the gate on the rebased base; the pull request is merged with Task 11 (a merge order, not an item dependency).

The exact new phrase is `a coordinator must be running before the cron entry`.

Acceptance criteria:
- Sections 6, 8.5 and the acceptance paragraph carry the new text, each pointing at docs/designs/issue-pipeline-fu1.md.
- `grep -cF "a coordinator must be running before the cron entry" docs/designs/issue-watcher-setup.md` prints 0 before the edit and 1 or more after (checked 2026-11-15: 0 today).
- `grep -F "second agent" docs/designs/issue-watcher-setup.md | grep -vc "superseded"` prints 1 before the edit (checked 2026-11-15) and 0 after, so every remaining `second agent` line is marked superseded or reworded.

